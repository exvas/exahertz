# Copyright (c) 2025, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, get_time
from datetime import datetime, timedelta
import re


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    # Add summary row for performance metrics
    summary = get_summary(data) if data else None

    return columns, data, None, None, summary

def get_columns():
    return [
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Date',
            'width': 120
        },
        {
            'fieldname': 'employee_id',
            'label': 'Employee ID',
            'fieldtype': 'Link',
            'options': 'Employee',
            'width': 120
        },
        {
            'fieldname': 'employee_name',
            'label': 'Employee Name',
            'fieldtype': 'Data',
            'width': 300
        },
        {
            'fieldname': 'shift_type',
            'label': 'Shift Type',
            'fieldtype': 'Link',
            'options': 'Shift Type',
            'width': 200
        },
        {
            'fieldname': 'status',
            'label': 'Att Code',
            'fieldtype': 'HTML',
            'width': 140
        },
        {
            'fieldname': 'in_time',
            'label': 'In Time',
            'fieldtype': 'Data',
            'width': 90
        },
        {
            'fieldname': 'out_time',
            'label': 'Out Time',
            'fieldtype': 'Data',
            'width': 90
        },
        {
            'fieldname': 'base_hours',
            'label': 'Base Hrs',
            'fieldtype': 'Duration',
            'width': 90
        },
        {
            'fieldname': 'total_working_hours',
            'label': 'Work Hrs',
            'fieldtype': 'Duration',
            'width': 120
        },
        {
            'fieldname': 'ot1',
            'label': 'OT',
            'fieldtype': 'Duration',
            'width': 100
        },
        {
            'fieldname': 'ut',
            'label': 'UT',
            'fieldtype': 'Duration',
            'width': 90
        },
        {
            'fieldname': 'early_exit',
            'label': 'Early Exit',
            'fieldtype': 'Check',
            'width': 90
        },
        {
            'fieldname': 'late_entry',
            'label': 'Late Entry',
            'fieldtype': 'Check',
            'width': 90
        },
        {
            'fieldname': 'attendance_reference',
            'label': 'Attendance Ref.',
            'fieldtype': 'Link',
            'options': 'Attendance',
            'width': 150
        },
        {
            'fieldname': 'employee_checkin_references',
            'label': 'Checkin Refs.',
            'fieldtype': 'Data',
            'width': 400
        }
    ]


def get_data(filters):
    # Ensure filters is a frappe._dict
    if not isinstance(filters, frappe._dict):
        filters = frappe._dict(filters or {})

    # Clean filter values
    for key in list(filters.keys()):
        value = filters[key]
        if isinstance(value, str):
            if key in ['from_date', 'to_date']:
                cleaned_value = ''.join(c for c in value if c in '0123456789-')
                try:
                    parsed_date = datetime.strptime(cleaned_value, '%Y-%m-%d').strftime('%Y-%m-%d')
                    filters[key] = parsed_date
                except (ValueError, TypeError):
                    frappe.logger().warning(f"Invalid date format for {key}: {cleaned_value}")
                    del filters[key]
            else:
                filters[key] = value.rstrip('%').rstrip().rstrip('*')

    if not filters.get('from_date'):
        frappe.throw("From Date is required")
    if not filters.get('to_date'):
        frappe.throw("To Date is required")

    # Get all active employees based on filters
    employee_query = "SELECT name as employee_id, employee_name FROM `tabEmployee` WHERE status = 'Active'"
    params = []
    if filters.get('employee_id'):
        employee_query += " AND name = %s"
        params.append(filters.get('employee_id'))
    if filters.get('department'):
        employee_query += " AND department = %s"
        params.append(filters.get('department'))

    employees = frappe.db.sql(employee_query, tuple(params) if params else (), as_dict=True)
    if not employees:
        return []

    # Build shift assignment lookup: employee -> shift_type
    emp_ids = [e['employee_id'] for e in employees]
    placeholders_emp = ','.join(['%s'] * len(emp_ids))
    shift_assignments = frappe.db.sql(f"""
        SELECT employee, shift_type, start_date, end_date
        FROM `tabShift Assignment`
        WHERE employee IN ({placeholders_emp})
        AND docstatus = 1
        AND start_date <= %s
        AND (end_date IS NULL OR end_date >= %s)
        ORDER BY start_date DESC
    """, emp_ids + [filters.to_date, filters.from_date], as_dict=True)

    employee_shift_lookup = {}
    for sa in shift_assignments:
        if sa.employee not in employee_shift_lookup:
            employee_shift_lookup[sa.employee] = sa.shift_type

    # --- Get Attendance records (status, leave_type, etc.) ---
    attendance_query = """
        SELECT
            a.attendance_date as date,
            a.employee as employee_id,
            e.employee_name as employee_name,
            a.shift as shift_type,
            a.in_time as att_in_time,
            a.out_time as att_out_time,
            a.status as original_status,
            a.leave_type as attendance_leave_type,
            a.name as attendance_reference,
            a.late_entry,
            a.early_exit,
            a.working_hours as att_working_hours
        FROM `tabAttendance` a
        LEFT JOIN `tabEmployee` e ON a.employee = e.name
        WHERE a.attendance_date BETWEEN %s AND %s
        AND a.docstatus = 1
    """
    att_params = [filters.from_date, filters.to_date]
    if filters.get('employee_id'):
        attendance_query += " AND a.employee = %s"
        att_params.append(filters.get('employee_id'))
    if filters.get('department'):
        attendance_query += " AND e.department = %s"
        att_params.append(filters.get('department'))
    if filters.get('shift_type'):
        attendance_query += " AND a.shift = %s"
        att_params.append(filters.get('shift_type'))

    attendance_records = frappe.db.sql(attendance_query, tuple(att_params), as_dict=True)

    # Create attendance lookup by (employee, date)
    attendance_lookup = {}
    for att in attendance_records:
        key = f"{att['employee_id']}_{att['date']}"
        attendance_lookup[key] = att

    # --- Get Employee Checkin data (first IN, last OUT per employee per day) ---
    checkin_query = """
        WITH checkin_data AS (
            SELECT
                DATE(time) as date,
                employee,
                time,
                log_type,
                name as checkin_name,
                COUNT(*) OVER (PARTITION BY DATE(time), employee) as checkin_count,
                ROW_NUMBER() OVER (PARTITION BY DATE(time), employee ORDER BY time) as checkin_order,
                ROW_NUMBER() OVER (PARTITION BY DATE(time), employee ORDER BY time DESC) as reverse_order
            FROM `tabEmployee Checkin`
            WHERE DATE(time) BETWEEN %s AND %s
        )
        SELECT
            cd.date,
            cd.employee as employee_id,
            e.employee_name as employee_name,
            sa.shift_type as shift_type,
            MIN(CASE WHEN cd.checkin_order = 1 THEN cd.time END) as in_time,
            CASE
                WHEN cd.checkin_count > 1 THEN MAX(CASE WHEN cd.reverse_order = 1 THEN cd.time END)
                ELSE NULL
            END as out_time,
            CASE
                WHEN cd.checkin_count > 1 THEN
                    TIMESTAMPDIFF(SECOND,
                        MIN(CASE WHEN cd.checkin_order = 1 THEN cd.time END),
                        MAX(CASE WHEN cd.reverse_order = 1 THEN cd.time END)
                    )
                ELSE 0
            END as working_hours_seconds,
            GROUP_CONCAT(DISTINCT cd.checkin_name ORDER BY cd.time) as employee_checkin_references
        FROM checkin_data cd
        LEFT JOIN `tabEmployee` e ON cd.employee = e.name
        LEFT JOIN `tabShift Assignment` sa ON sa.employee = cd.employee
            AND sa.docstatus = 1
            AND sa.start_date <= cd.date
            AND (sa.end_date IS NULL OR sa.end_date >= cd.date)
    """

    checkin_params = [filters.from_date, filters.to_date]
    if filters.get('employee_id'):
        checkin_query += " AND cd.employee = %s"
        checkin_params.append(filters.get('employee_id'))
    if filters.get('department'):
        checkin_query += " AND e.department = %s"
        checkin_params.append(filters.get('department'))
    if filters.get('shift_type'):
        checkin_query += " AND sa.shift_type = %s"
        checkin_params.append(filters.get('shift_type'))

    checkin_query += " GROUP BY cd.date, cd.employee, e.employee_name, sa.shift_type, cd.checkin_count ORDER BY cd.employee, cd.date"

    checkin_records = frappe.db.sql(checkin_query, tuple(checkin_params), as_dict=True)

    # --- Build merged lookup: combine checkin data with attendance data ---
    merged_lookup = {}

    # First pass: populate from checkin records
    for record in checkin_records:
        key = f"{record['employee_id']}_{record['date']}"

        # Format in_time
        in_time_str = ''
        if record['in_time']:
            try:
                in_time_str = get_time(record['in_time']).strftime('%I:%M %p')
            except Exception:
                pass

        # Format out_time (only if different from in_time at minute level)
        out_time_str = ''
        if record['out_time']:
            try:
                out_time_obj = get_time(record['out_time'])
                out_formatted = out_time_obj.strftime('%I:%M %p')
                # Compare formatted strings so 06:57:21 and 06:57:22 are treated as same
                if in_time_str and out_formatted != in_time_str:
                    out_time_str = out_formatted
            except Exception:
                pass

        # Working hours from checkin data (in seconds)
        work_seconds = int(record.get('working_hours_seconds') or 0)
        if work_seconds < 0 or work_seconds > 86400:
            work_seconds = 0
        # Zero working hours if out_time was cleared (double-punch / same-minute checkins)
        if not out_time_str:
            work_seconds = 0

        merged = {
            'date': record['date'],
            'employee_id': record['employee_id'],
            'employee_name': record['employee_name'],
            'shift_type': record.get('shift_type') or '',
            'in_time': in_time_str,
            'out_time': out_time_str,
            'total_working_hours': work_seconds,
            'late_entry': 0,
            'early_exit': 0,
            'original_status': None,
            'attendance_leave_type': '',
            'attendance_reference': '',
            'employee_checkin_references': record.get('employee_checkin_references') or '',
        }

        # Merge with attendance data if available
        if key in attendance_lookup:
            att = attendance_lookup[key]
            merged['shift_type'] = att.get('shift_type') or merged['shift_type']
            merged['original_status'] = att['original_status']
            merged['attendance_leave_type'] = att.get('attendance_leave_type') or ''
            merged['attendance_reference'] = att.get('attendance_reference') or ''
            merged['late_entry'] = att.get('late_entry', 0)
            merged['early_exit'] = att.get('early_exit', 0)
            # Only use attendance working_hours as fallback when checkin-based is 0
            if not work_seconds and att.get('att_working_hours'):
                merged['total_working_hours'] = int(float(att['att_working_hours']) * 3600)

        merged_lookup[key] = merged

    # Second pass: add attendance-only records (no checkins, e.g. On Leave, Absent)
    for key, att in attendance_lookup.items():
        if key not in merged_lookup:
            in_time_str = ''
            out_time_str = ''
            if att.get('att_in_time'):
                try:
                    in_time_str = get_time(att['att_in_time']).strftime('%I:%M %p')
                except Exception:
                    pass
            if att.get('att_out_time'):
                try:
                    out_obj = get_time(att['att_out_time'])
                    in_obj = get_time(att['att_in_time']) if att.get('att_in_time') else None
                    if in_obj and out_obj != in_obj:
                        out_time_str = out_obj.strftime('%I:%M %p')
                    elif not in_obj:
                        out_time_str = out_obj.strftime('%I:%M %p')
                except Exception:
                    pass

            merged_lookup[key] = {
                'date': att['date'],
                'employee_id': att['employee_id'],
                'employee_name': att['employee_name'],
                'shift_type': att.get('shift_type') or employee_shift_lookup.get(att['employee_id'], ''),
                'in_time': in_time_str,
                'out_time': out_time_str,
                'total_working_hours': int(float(att.get('att_working_hours') or 0) * 3600),
                'late_entry': att.get('late_entry', 0),
                'early_exit': att.get('early_exit', 0),
                'original_status': att['original_status'],
                'attendance_leave_type': att.get('attendance_leave_type') or '',
                'attendance_reference': att.get('attendance_reference') or '',
                'employee_checkin_references': '',
            }

    # --- Generate all employee x date combinations ---
    start_date = datetime.strptime(str(filters.from_date).strip(), '%Y-%m-%d').date()
    end_date = datetime.strptime(str(filters.to_date).strip(), '%Y-%m-%d').date()

    data = []
    for employee in employees:
        current_date = start_date
        while current_date <= end_date:
            key = f"{employee['employee_id']}_{current_date}"
            if key in merged_lookup:
                row = merged_lookup[key]
            else:
                # Placeholder: no checkins and no attendance
                row = {
                    'date': current_date,
                    'employee_id': employee['employee_id'],
                    'employee_name': employee['employee_name'],
                    'shift_type': employee_shift_lookup.get(employee['employee_id'], ''),
                    'in_time': '',
                    'out_time': '',
                    'total_working_hours': 0,
                    'late_entry': 0,
                    'early_exit': 0,
                    'original_status': None,
                    'attendance_leave_type': '',
                    'attendance_reference': '',
                    'employee_checkin_references': '',
                }
            data.append(row)
            current_date += timedelta(days=1)

    # --- Build lookup tables for holidays and leaves ---
    holiday_lookup = {}
    weekoff_lookup = {}
    leave_lookup = {}

    if data:
        employees_list = list(set([row['employee_id'] for row in data]))
        placeholders = ','.join(['%s'] * len(employees_list))

        # Leave applications
        leave_apps = frappe.db.sql(f"""
            SELECT employee as employee_id, from_date, to_date, leave_type
            FROM `tabLeave Application`
            WHERE employee IN ({placeholders})
            AND docstatus = 1
            AND from_date <= %s
            AND to_date >= %s
        """, employees_list + [filters.to_date, filters.from_date], as_dict=True)

        for la in leave_apps:
            d = la.from_date
            while d <= la.to_date:
                leave_lookup[(la.employee_id, d)] = la.leave_type
                d += timedelta(days=1)

        # Holidays and weekly offs
        try:
            holiday_data = frappe.db.sql(f"""
                SELECT
                    e.name as employee_id,
                    h.holiday_date,
                    h.weekly_off
                FROM `tabEmployee` e
                LEFT JOIN `tabHoliday List` hl ON e.holiday_list = hl.name
                LEFT JOIN `tabHoliday` h ON hl.name = h.parent
                WHERE e.name IN ({placeholders})
                AND h.holiday_date BETWEEN %s AND %s
            """, employees_list + [filters.from_date, filters.to_date], as_dict=True)

            for holiday in holiday_data:
                holiday_lookup[(holiday.employee_id, holiday.holiday_date)] = True
                if holiday.weekly_off == 1:
                    day_name = holiday.holiday_date.strftime('%A')
                    weekoff_lookup[(holiday.employee_id, day_name)] = True
        except Exception as e:
            frappe.log_error(f"Error fetching holiday data: {str(e)}")

    # --- Shift base hours and late entry config lookup ---
    shift_base_hours = {}
    shift_late_config = {}  # {shift_name: {'start_seconds': int, 'grace_minutes': int}}
    all_shifts = frappe.db.sql(
        "SELECT name, start_time, end_time, late_entry_grace_period FROM `tabShift Type`",
        as_dict=True
    )
    for shift in all_shifts:
        if shift.start_time and shift.end_time:
            diff_seconds = shift.end_time.total_seconds() - shift.start_time.total_seconds()
            if diff_seconds < 0:
                diff_seconds += 86400  # Handle overnight shifts
            shift_base_hours[shift.name] = int(diff_seconds)
            shift_late_config[shift.name] = {
                'start_seconds': int(shift.start_time.total_seconds()),
                'grace_minutes': int(shift.late_entry_grace_period or 0),
            }
        else:
            shift_base_hours[shift.name] = 0

    # Fallback: standard working hours from HR Settings
    standard_working_hours = frappe.db.get_single_value('HR Settings', 'standard_working_hours') or 8
    standard_working_hours_seconds = int(standard_working_hours * 3600)

    # --- Process each record: determine status, calculate OT/UT ---
    for row in data:
        # Base hours from Shift Type
        shift_name = row.get('shift_type', '')
        row['base_hours'] = shift_base_hours.get(shift_name, standard_working_hours_seconds)

        # Holiday / Week-off detection
        is_holiday_date = (row['employee_id'], row['date']) in holiday_lookup
        row_weekday = row['date'].strftime('%A')
        is_week_off = (row['employee_id'], row_weekday) in weekoff_lookup

        # Determine attendance status
        is_present_day = False  # Flag for OT/UT calculation

        if is_holiday_date and is_week_off:
            row['status'] = format_attendance_status('Week Off (Holiday)')
            row['leave_type'] = ''
            row['total_working_hours'] = 0
            row['base_hours'] = 0

        elif is_holiday_date:
            if row['original_status'] in ['Present', 'On Leave', 'Absent']:
                if row['in_time'] or row['out_time']:
                    row['status'] = format_attendance_status(f"Holiday ({row['original_status']})")
                else:
                    row['status'] = format_attendance_status('Holiday')
            else:
                row['status'] = format_attendance_status('Holiday')
            row['leave_type'] = ''

        elif is_week_off:
            row['status'] = format_attendance_status('Week Off')
            row['leave_type'] = ''
            row['total_working_hours'] = 0
            row['base_hours'] = 0

        elif row['original_status'] == 'Present':
            row['status'] = format_attendance_status('Present')
            row['leave_type'] = ''
            is_present_day = True

        elif row['original_status'] == 'Half Day':
            row['status'] = format_attendance_status('Half Day')
            row['leave_type'] = row.get('attendance_leave_type') or ''
            is_present_day = True

        elif row['original_status'] == 'On Leave':
            leave_type = (row.get('attendance_leave_type') or '').strip()
            if not leave_type:
                leave_type = leave_lookup.get((row['employee_id'], row['date']), '')
            if leave_type:
                row['status'] = format_attendance_status(leave_type)
                row['leave_type'] = leave_type
            else:
                row['status'] = format_attendance_status('On Leave')
                row['leave_type'] = ''

        elif row['original_status'] is None:
            # No Attendance record - determine status from checkins or leave
            leave_type = leave_lookup.get((row['employee_id'], row['date']))
            if leave_type:
                row['status'] = format_attendance_status(leave_type)
                row['leave_type'] = leave_type
            else:
                has_checkins = row.get('in_time') or row.get('employee_checkin_references')
                if has_checkins:
                    if row.get('in_time') and row.get('out_time'):
                        # Both IN and OUT exist -> Present
                        row['status'] = format_attendance_status('Present')
                        is_present_day = True
                    elif row.get('in_time') and not row.get('out_time'):
                        row['status'] = format_attendance_status('Missing Checkout')
                    elif not row.get('in_time') and row.get('out_time'):
                        row['status'] = format_attendance_status('Missing Checkin')
                    else:
                        row['status'] = format_attendance_status('Pending')
                    row['leave_type'] = ''
                else:
                    row['status'] = format_attendance_status('Absent')
                    row['leave_type'] = ''

        else:
            # Other statuses (Absent, etc.)
            row['leave_type'] = (row.get('attendance_leave_type') or '').strip()
            row['status'] = format_attendance_status(row['original_status'] or 'Absent')

        # Calculate OT and UT (only for present/working days)
        base_seconds = row['base_hours']
        work_seconds = row.get('total_working_hours') or 0

        if is_present_day and base_seconds > 0 and work_seconds > 0:
            if work_seconds > base_seconds:
                row['ot1'] = work_seconds - base_seconds
                row['ut'] = 0
            elif work_seconds < base_seconds:
                row['ut'] = base_seconds - work_seconds
                row['ot1'] = 0
            else:
                row['ot1'] = 0
                row['ut'] = 0
        else:
            row['ot1'] = 0
            row['ut'] = 0

        # Calculate late_entry from checkin data when not already set from Attendance
        if not row.get('late_entry') and row.get('in_time') and shift_name in shift_late_config:
            config = shift_late_config[shift_name]
            try:
                in_time_obj = datetime.strptime(row['in_time'], '%I:%M %p')
                in_seconds = in_time_obj.hour * 3600 + in_time_obj.minute * 60
                threshold = config['start_seconds'] + (config['grace_minutes'] * 60)
                # Only mark late if within 4 hours of shift start (avoid marking OUT punches as late)
                if in_seconds > threshold and (in_seconds - config['start_seconds']) < 14400:
                    row['late_entry'] = 1
            except (ValueError, TypeError):
                pass

    # Apply att_code filter if provided
    if filters.get('att_code'):
        att_code_filter = filters.get('att_code').strip()
        filtered_data = []
        for row in data:
            status = str(row.get('status', ''))
            plain_status = re.sub(r'<[^>]+>', '', status).strip()
            if (att_code_filter.lower() in status.lower() or
                att_code_filter.lower() in plain_status.lower()):
                filtered_data.append(row)
        data = filtered_data

    return data


def format_attendance_status(status):
    """Format attendance status with colors and bold text."""
    if not status:
        return status

    color_map = {
        'Week Off': '<span style="color: blue; font-weight: bold;">Week Off</span>',
        'Week Off (Holiday)': '<span style="color: blue; font-weight: bold;">Week Off (Holiday)</span>',
        'PR': '<span style="color: green; font-weight: bold;">Present</span>',
        'Present': '<span style="color: green; font-weight: bold;">Present</span>',
        'Absent': '<span style="color: red; font-weight: bold;">Absent</span>',
        'Pending': '<span style="color: orange; font-weight: bold;">Pending</span>',
        'Missing Checkout': '<span style="color: orange; font-weight: bold;">Missing Checkout</span>',
        'Missing Checkin': '<span style="color: orange; font-weight: bold;">Missing Checkin</span>',
        'Holiday': '<span style="color: purple; font-weight: bold;">Holiday</span>',
        'Mis-Punch': '<span style="color: orange; font-weight: bold;">Mis-Punch</span>',
        'On Leave': '<span style="color: blue; font-weight: bold;">On Leave</span>',
        'Half Day': '<span style="color: #FF6600; font-weight: bold;">Half Day</span>',
        'Work From Home': '<span style="color: #0099CC; font-weight: bold;">Work From Home</span>'
    }

    # Handle Holiday with punch status (e.g., "Holiday (Present)")
    if status.startswith('Holiday (') and status.endswith(')'):
        return f'<span style="color: purple; font-weight: bold;">{status}</span>'

    # Check if status is a leave type (not in predefined statuses)
    if status not in color_map:
        return f'<span style="color: blue; font-weight: bold;">{status}</span>'

    return color_map.get(status, status)


def get_summary(data):
    """Generate summary statistics for the report."""
    if not data:
        return []

    total_records = len(data)
    week_off_count = len([d for d in data if 'Week Off' in str(d.get("status", ""))])
    present_count = len([d for d in data if 'Present' in str(d.get("status", "")) and 'Holiday' not in str(d.get("status", ""))])
    absent_count = len([d for d in data if 'Absent' in str(d.get("status", "")) and 'Week Off' not in str(d.get("status", ""))])
    holiday_count = len([d for d in data if 'Holiday' in str(d.get("status", "")) and 'Week Off' not in str(d.get("status", ""))])

    return [
        {
            "label": "Total Records",
            "value": total_records,
            "indicator": "Blue"
        },
        {
            "label": "Week Off",
            "value": week_off_count,
            "indicator": "Orange"
        },
        {
            "label": "Present",
            "value": present_count,
            "indicator": "Green"
        },
        {
            "label": "Holiday",
            "value": holiday_count,
            "indicator": "Purple"
        },
        {
            "label": "Absent",
            "value": absent_count,
            "indicator": "Red"
        }
    ]
