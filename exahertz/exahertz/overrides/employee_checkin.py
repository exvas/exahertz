# Copyright (c) 2024, Exahertz and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, get_datetime, time_diff_in_hours, add_days


def on_employee_checkin_submit(doc, method=None):
	"""
	Hook: after_insert on Employee Checkin.

	For late-synced checkins (device was offline and synced later),
	triggers attendance creation for that past date as a background job.
	"""
	checkin_date = getdate(doc.time)
	sync_date = getdate(doc.creation)

	if checkin_date < sync_date:
		frappe.logger().info(
			f"Late-synced checkin: {doc.name} | Punch: {checkin_date} | Synced: {sync_date}"
		)
		frappe.enqueue(
			"exahertz.exahertz.overrides.employee_checkin.create_attendance_from_checkins",
			queue="short",
			timeout=300,
			target_date=checkin_date,
			now=False,
		)


def daily_attendance_from_checkins():
	"""
	Daily fallback scheduler job (runs at 11:45 PM).

	Creates attendance from Employee Checkins for employees who have
	checkins but no attendance record yet (missed by HRMS auto attendance).
	Checks today and yesterday to catch any gaps.
	"""
	today = getdate()
	yesterday = add_days(today, -1)

	for dt in [yesterday, today]:
		try:
			stats = create_attendance_from_checkins(dt)
			if stats.get("created"):
				frappe.logger().info(f"Attendance fallback {dt}: {stats}")
		except Exception:
			frappe.log_error(title=f"Attendance Fallback Error - {dt}")

	frappe.db.commit()


def create_attendance_from_checkins(target_date):
	"""
	Fallback: For a given date, find employees who have Employee Checkins
	but no Attendance record, and create Attendance from their checkins.

	Uses first check-in as IN time and last check-in as OUT time.
	Determines Present/Half Day/Absent based on Shift Type thresholds.

	Args:
		target_date: Date to process

	Returns:
		dict with stats
	"""
	target_date = getdate(target_date)
	created = 0
	skipped = 0
	errors = 0

	# Find employees with checkins on this date but no attendance
	employees_with_checkins = frappe.db.sql(
		"""
		SELECT DISTINCT ec.employee
		FROM `tabEmployee Checkin` ec
		WHERE DATE(ec.time) = %s
		AND NOT EXISTS (
			SELECT 1 FROM `tabAttendance` att
			WHERE att.employee = ec.employee
			AND att.attendance_date = %s
			AND att.docstatus < 2
		)
		""",
		(target_date, target_date),
		as_dict=True,
	)

	if not employees_with_checkins:
		return {"created": 0, "skipped": 0, "errors": 0}

	for row in employees_with_checkins:
		employee = row.employee
		try:
			# Get all checkins for this employee on this date ordered by time
			checkins = frappe.db.sql(
				"""
				SELECT name, time, log_type, shift
				FROM `tabEmployee Checkin`
				WHERE employee = %s AND DATE(time) = %s
				ORDER BY time ASC
				""",
				(employee, target_date),
				as_dict=True,
			)

			if not checkins:
				skipped += 1
				continue

			first_checkin = checkins[0]
			last_checkin = checkins[-1]

			in_time = first_checkin.time
			out_time = last_checkin.time if len(checkins) > 1 else None

			# Calculate working hours
			working_hours = 0
			if in_time and out_time and in_time != out_time:
				working_hours = time_diff_in_hours(out_time, in_time)

			# Get shift from checkin or shift assignment
			shift_name = first_checkin.shift
			if not shift_name:
				shift_name = frappe.db.get_value(
					"Shift Assignment",
					{
						"employee": employee,
						"docstatus": 1,
						"start_date": ("<=", target_date),
					},
					"shift_type",
					order_by="start_date desc",
				)

			# Determine status based on shift thresholds
			status = "Present"
			if shift_name and out_time:
				shift_type = frappe.get_cached_doc("Shift Type", shift_name)
				absent_threshold = float(shift_type.working_hours_threshold_for_absent or 0)
				half_day_threshold = float(shift_type.working_hours_threshold_for_half_day or 0)

				if absent_threshold and working_hours < absent_threshold:
					status = "Absent"
				elif half_day_threshold and working_hours < half_day_threshold:
					status = "Half Day"

			company = frappe.db.get_value("Employee", employee, "company")

			attendance = frappe.get_doc(
				{
					"doctype": "Attendance",
					"employee": employee,
					"attendance_date": target_date,
					"status": status,
					"shift": shift_name,
					"in_time": in_time,
					"out_time": out_time if (out_time and out_time != in_time) else None,
					"working_hours": working_hours,
					"company": company,
				}
			)
			attendance.insert(ignore_permissions=True)
			attendance.submit()

			# Link checkins to this attendance
			checkin_names = [c.name for c in checkins]
			if checkin_names:
				frappe.db.sql(
					"""
					UPDATE `tabEmployee Checkin`
					SET attendance = %s
					WHERE name IN %s
					""",
					(attendance.name, checkin_names),
				)

			created += 1

		except Exception:
			errors += 1
			frappe.log_error(title=f"Attendance Fallback - {employee} on {target_date}")

	if created:
		frappe.db.commit()

	return {"created": created, "skipped": skipped, "errors": errors}
