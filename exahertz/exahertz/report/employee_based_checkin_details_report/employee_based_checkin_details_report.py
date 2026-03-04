# Copyright (c) 2026, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, get_time, format_datetime, time_diff_in_hours


def execute(filters=None):
	if not filters:
		filters = {}

	validate_filters(filters)
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)

	return columns, data, None, chart


def validate_filters(filters):
	if not filters.get("from_date"):
		frappe.throw(_("From Date is required"))
	if not filters.get("to_date"):
		frappe.throw(_("To Date is required"))
	if getdate(filters.get("from_date")) > getdate(filters.get("to_date")):
		frappe.throw(_("From Date cannot be after To Date"))


def get_columns():
	return [
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 110,
		},
		{
			"label": _("Employee ID"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 130,
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 220,
		},
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Link",
			"options": "Department",
			"width": 140,
		},
		{
			"label": _("Shift"),
			"fieldname": "shift",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Shift Start"),
			"fieldname": "shift_start",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("Shift End"),
			"fieldname": "shift_end",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("#"),
			"fieldname": "checkin_seq",
			"fieldtype": "Int",
			"width": 45,
		},
		{
			"label": _("Log Type"),
			"fieldname": "log_type",
			"fieldtype": "Data",
			"width": 70,
		},
		{
			"label": _("Time"),
			"fieldname": "checkin_time",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Device ID"),
			"fieldname": "device_id",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("First In"),
			"fieldname": "first_in",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("Last Out"),
			"fieldname": "last_out",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("Total Punches"),
			"fieldname": "total_punches",
			"fieldtype": "Int",
			"width": 60,
		},
		{
			"label": _("Working Hrs"),
			"fieldname": "working_hours",
			"fieldtype": "Data",
			"width": 95,
		},
		{
			"label": _("Late By"),
			"fieldname": "late_by",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("Early Exit"),
			"fieldname": "early_exit",
			"fieldtype": "Data",
			"width": 90,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Checkin ID"),
			"fieldname": "checkin_name",
			"fieldtype": "Link",
			"options": "Employee Checkin",
			"width": 200,
		},
	]


def get_data(filters):
	conditions, values = build_conditions(filters)

	# Fetch all individual checkin records
	checkins = frappe.db.sql("""
		SELECT
			ec.name AS checkin_name,
			DATE(ec.time) AS date,
			ec.employee,
			ec.employee_name,
			ec.time AS checkin_time,
			ec.log_type,
			ec.device_id,
			emp.department,
			emp.designation,
			sa.shift_type AS shift,
			st.start_time AS shift_start,
			st.end_time AS shift_end,
			st.late_entry_grace_period,
			st.early_exit_grace_period
		FROM `tabEmployee Checkin` ec
		LEFT JOIN `tabEmployee` emp ON emp.name = ec.employee
		LEFT JOIN `tabShift Assignment` sa ON sa.employee = ec.employee
			AND sa.docstatus = 1
			AND sa.start_date <= DATE(ec.time)
			AND (sa.end_date IS NULL OR sa.end_date >= DATE(ec.time))
		LEFT JOIN `tabShift Type` st ON st.name = sa.shift_type
		WHERE DATE(ec.time) BETWEEN %(from_date)s AND %(to_date)s
		{conditions}
		ORDER BY ec.employee, DATE(ec.time), ec.time
	""".format(conditions=conditions), values, as_dict=True)

	if not checkins:
		return []

	# Group checkins by (employee, date) for summary calculations
	from collections import OrderedDict
	groups = OrderedDict()
	for row in checkins:
		key = (row.employee, str(row.date))
		if key not in groups:
			groups[key] = []
		groups[key].append(row)

	# Build output rows
	data = []
	for (employee, date_str), rows in groups.items():
		first_row = rows[0]
		times = [r.checkin_time for r in rows]
		first_in = min(times)
		last_out = max(times) if len(times) > 1 else None
		total_punches = len(rows)

		# Calculate working hours
		working_hours = ""
		if first_in and last_out and len(times) > 1:
			hrs = time_diff_in_hours(last_out, first_in)
			if hrs > 0:
				h = int(hrs)
				m = int((hrs - h) * 60)
				working_hours = f"{h}h {m:02d}m"

		# Format shift times
		shift_start_display = format_shift_time(first_row.shift_start)
		shift_end_display = format_shift_time(first_row.shift_end)

		# Calculate late by
		late_by = compute_late_by(first_in, first_row.shift_start, first_row.late_entry_grace_period)

		# Calculate early exit
		early_exit = compute_early_exit(last_out, first_row.shift_end, first_row.early_exit_grace_period)

		# Determine status
		status = determine_status(total_punches, late_by, early_exit, working_hours)

		first_in_display = format_datetime(first_in, "hh:mm a") if first_in else ""
		last_out_display = format_datetime(last_out, "hh:mm a") if last_out else ""

		for seq, row in enumerate(rows, 1):
			entry = {
				"checkin_name": row.checkin_name,
				"date": row.date if seq == 1 else "",
				"employee": row.employee if seq == 1 else "",
				"employee_name": row.employee_name if seq == 1 else "",
				"department": row.department if seq == 1 else "",
				"shift": row.shift if seq == 1 else "",
				"shift_start": shift_start_display if seq == 1 else "",
				"shift_end": shift_end_display if seq == 1 else "",
				"checkin_seq": seq,
				"log_type": row.log_type or "IN",
				"checkin_time": format_datetime(row.checkin_time, "hh:mm:ss a") if row.checkin_time else "",
				"device_id": row.device_id or "",
				"first_in": first_in_display if seq == 1 else "",
				"last_out": last_out_display if seq == 1 else "",
				"total_punches": total_punches if seq == 1 else "",
				"working_hours": working_hours if seq == 1 else "",
				"late_by": late_by if seq == 1 else "",
				"early_exit": early_exit if seq == 1 else "",
				"status": status if seq == 1 else "",
				"_employee": row.employee,
				"_date": str(row.date),
				"_is_first": seq == 1,
				"_total_punches": total_punches,
			}
			data.append(entry)

	return data


def build_conditions(filters):
	conditions = ""
	values = {
		"from_date": filters.get("from_date"),
		"to_date": filters.get("to_date"),
	}

	if filters.get("employee"):
		conditions += " AND ec.employee = %(employee)s"
		values["employee"] = filters.get("employee")

	if filters.get("department"):
		conditions += " AND emp.department = %(department)s"
		values["department"] = filters.get("department")

	if filters.get("designation"):
		conditions += " AND emp.designation = %(designation)s"
		values["designation"] = filters.get("designation")

	if filters.get("shift"):
		conditions += " AND sa.shift_type = %(shift)s"
		values["shift"] = filters.get("shift")

	return conditions, values


def format_shift_time(time_val):
	"""Format a shift time (timedelta or time) into readable format."""
	if not time_val:
		return ""
	from datetime import timedelta, time as dt_time

	if isinstance(time_val, timedelta):
		total_seconds = int(time_val.total_seconds())
		hours = total_seconds // 3600
		minutes = (total_seconds % 3600) // 60
		period = "AM" if hours < 12 else "PM"
		display_hours = hours % 12 or 12
		return f"{display_hours}:{minutes:02d} {period}"
	elif isinstance(time_val, dt_time):
		return time_val.strftime("%I:%M %p")
	return str(time_val)


def compute_late_by(first_in, shift_start, grace_period):
	"""Compute how late an employee was."""
	if not first_in or not shift_start:
		return ""

	from datetime import timedelta, time as dt_time, datetime

	checkin_dt = first_in
	checkin_date = checkin_dt.date() if hasattr(checkin_dt, 'date') else getdate(checkin_dt)

	# Convert shift_start to time
	if isinstance(shift_start, timedelta):
		total_seconds = int(shift_start.total_seconds())
		hours = total_seconds // 3600
		minutes = (total_seconds % 3600) // 60
		seconds = total_seconds % 60
		shift_start_time = dt_time(hours, minutes, seconds)
	elif isinstance(shift_start, dt_time):
		shift_start_time = shift_start
	else:
		shift_start_time = get_time(shift_start)

	shift_start_dt = datetime.combine(checkin_date, shift_start_time)

	# Add grace period
	grace = int(grace_period or 0)
	if grace:
		shift_start_dt += timedelta(minutes=grace)

	if checkin_dt > shift_start_dt:
		diff = (checkin_dt - shift_start_dt).total_seconds()
		if diff > 60:  # Only show if late by more than 1 minute
			h = int(diff // 3600)
			m = int((diff % 3600) // 60)
			if h > 0:
				return f"{h}h {m:02d}m"
			return f"{m} min{'s' if m != 1 else ''}"

	return "On Time"


def compute_early_exit(last_out, shift_end, grace_period):
	"""Compute if employee left early."""
	if not last_out or not shift_end:
		return ""

	from datetime import timedelta, time as dt_time, datetime

	checkout_dt = last_out
	checkout_date = checkout_dt.date() if hasattr(checkout_dt, 'date') else getdate(checkout_dt)

	# Convert shift_end to time
	if isinstance(shift_end, timedelta):
		total_seconds = int(shift_end.total_seconds())
		hours = total_seconds // 3600
		minutes = (total_seconds % 3600) // 60
		seconds = total_seconds % 60
		shift_end_time = dt_time(hours, minutes, seconds)
	elif isinstance(shift_end, dt_time):
		shift_end_time = shift_end
	else:
		shift_end_time = get_time(shift_end)

	shift_end_dt = datetime.combine(checkout_date, shift_end_time)

	# Subtract grace period
	grace = int(grace_period or 0)
	if grace:
		shift_end_dt -= timedelta(minutes=grace)

	if checkout_dt < shift_end_dt:
		diff = (shift_end_dt - checkout_dt).total_seconds()
		if diff > 60:  # Only show if early by more than 1 minute
			h = int(diff // 3600)
			m = int((diff % 3600) // 60)
			if h > 0:
				return f"{h}h {m:02d}m"
			return f"{m} min{'s' if m != 1 else ''}"

	return "On Time"


def determine_status(total_punches, late_by, early_exit, working_hours):
	"""Determine the employee's status for the day."""
	issues = []
	if late_by and late_by != "On Time" and late_by != "":
		issues.append("Late")
	if early_exit and early_exit != "On Time" and early_exit != "":
		issues.append("Early Exit")
	if total_punches == 1:
		issues.append("Missing Punch")

	if issues:
		return ", ".join(issues)

	if not working_hours:
		return "Incomplete"

	return "Regular"


def get_chart(data):
	"""Generate a chart summarizing daily checkin patterns."""
	if not data:
		return None

	# Count statuses from first-row entries only
	status_counts = {}
	for row in data:
		if row.get("_is_first") and row.get("status"):
			status = row["status"]
			# Simplify compound statuses
			if "Late" in status:
				status_counts["Late"] = status_counts.get("Late", 0) + 1
			elif "Early Exit" in status:
				status_counts["Early Exit"] = status_counts.get("Early Exit", 0) + 1
			elif "Missing Punch" in status:
				status_counts["Missing Punch"] = status_counts.get("Missing Punch", 0) + 1
			elif status == "Regular":
				status_counts["Regular"] = status_counts.get("Regular", 0) + 1
			else:
				status_counts["Other"] = status_counts.get("Other", 0) + 1

	if not status_counts:
		return None

	labels = list(status_counts.keys())
	values = list(status_counts.values())
	colors = []
	color_map = {
		"Regular": "#28a745",
		"Late": "#dc3545",
		"Early Exit": "#fd7e14",
		"Missing Punch": "#6c757d",
		"Other": "#adb5bd",
	}
	for label in labels:
		colors.append(color_map.get(label, "#adb5bd"))

	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": _("Employee Days"), "values": values}],
		},
		"type": "donut",
		"colors": colors,
		"height": 280,
	}
