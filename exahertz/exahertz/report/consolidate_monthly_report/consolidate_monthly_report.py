# Copyright (c) 2026, sammish and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
     return [
        {'fieldname': 'employee_id', 'label': 'Employee ID', 'fieldtype': 'Link', 'options': 'Employee', 'width': 90},
        {'fieldname': 'employee_name', 'label': 'Employee Name', 'fieldtype': 'Data', 'width': 260},
        {'fieldname': 'department', 'label': 'Department', 'fieldtype': 'Link', 'options': 'Department', 'width': 100},
        {'fieldname': 'present', 'label': 'PR', 'fieldtype': 'Int', 'width': 60},
        {
            'fieldname': 'off',
            'label': 'AB',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'wo',
            'label': 'WO',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'holiday_count',
            'label': 'HL',
            'fieldtype': 'Data',
            'width': 70,
            'default': 0
        },
        {
            'fieldname': 'annual_leave',
            'label': 'ANLL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'sick_leave',
            'label': 'SL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'normal_leave',
            'label': 'NL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'unpaid_leave',
            'label': 'UPL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'emergency_leave',
            'label': 'EL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'official_assignment',
            'label': 'OA',
            'fieldtype': 'Data',
            'width': 50
        },
        {
            'fieldname': 'maternity_leave',
            'label': 'ML',
            'fieldtype': 'Data',
            'width': 50
        },
         {
            'fieldname': 'study_leave',
            'label': 'STL',
            'fieldtype': 'Data',
            'width': 70
        },
        {
            'fieldname': 'miss_punch',
            'label': 'MP',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'examination_leave',
            'label': 'EXL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'accompanying_leave',
            'label': 'AL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'bereavement_leave',
            'label': 'BL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'marriage_leave',
            'label': 'MRL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'hajj_leave',
            'label': 'HJL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'paternity_leave',
            'label': 'PL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'compensatory_leave',
            'label': 'CL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'ot',
            'label': 'OT',
            'fieldtype': 'Duration',
            'width': 50
        },
        {
            'fieldname': 'ut',
            'label': 'UT',
            'fieldtype': 'Duration',
            'width': 60
        },
         {'fieldname': 'total_hr', 'label': 'Total Hr', 'fieldtype': 'Duration', 'width': 90},
    ]


def get_data(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append(f"attendance.attendance_date >= '{filters.get('from_date')}'")
    if filters.get("to_date"):
        conditions.append(f"attendance.attendance_date <= '{filters.get('to_date')}'")
    if filters.get("employee"):
        conditions.append(f"attendance.employee = '{filters.get('employee')}'")
    if filters.get("department"):
        conditions.append(f"emp.department = '{filters.get('department')}'")

    from_date = filters.get('from_date')
    to_date = filters.get('to_date')

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f'''
        SELECT
            attendance.employee AS employee_id,
            attendance.employee_name,
            emp.department,
            COUNT(CASE WHEN attendance.status = 'Present' THEN 1 END) AS present,
            COUNT(CASE WHEN attendance.status = 'Absent' AND attendance.leave_type IS NULL THEN 1 END) AS off,
            COUNT(CASE WHEN attendance.status = 'Half Day' THEN 1 END) AS half_day,
            COUNT(CASE WHEN attendance.status = 'Mis-Punch' THEN 1 END) AS miss_punch,
            SUM(CASE WHEN attendance.leave_type = 'Sick Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Sick Leave' THEN 1 ELSE 0 END) AS sick_leave,
            SUM(CASE WHEN attendance.leave_type = 'Normal Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Normal Leave' THEN 1 ELSE 0 END) AS normal_leave,
            SUM(CASE WHEN attendance.leave_type = 'Maternity Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Maternity Leave' THEN 1 ELSE 0 END) AS maternity_leave,
            SUM(CASE WHEN attendance.leave_type = 'Study Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Study Leave' THEN 1 ELSE 0 END) AS study_leave,
            SUM(CASE WHEN attendance.leave_type = 'Unpaid Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Unpaid Leave' THEN 1 ELSE 0 END) AS unpaid_leave,
            SUM(CASE WHEN attendance.leave_type = 'Emergency Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Emergency Leave' THEN 1 ELSE 0 END) AS emergency_leave,
            SUM(CASE WHEN attendance.leave_type = 'Examination Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Examination Leave' THEN 1 ELSE 0 END) AS examination_leave,
            SUM(CASE WHEN attendance.leave_type = 'Official Assignment' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Official Assignment' THEN 1 ELSE 0 END) AS official_assignment,
            SUM(CASE WHEN attendance.leave_type = 'Accompanying Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Accompanying Leave' THEN 1 ELSE 0 END) AS accompanying_leave,
            SUM(CASE WHEN attendance.leave_type = 'Annual Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Annual Leave' THEN 1 ELSE 0 END) AS annual_leave,
            SUM(CASE WHEN attendance.leave_type = 'Bereavement Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Bereavement Leave' THEN 1 ELSE 0 END) AS bereavement_leave,
            SUM(CASE WHEN attendance.leave_type = 'Marriage Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Marriage Leave' THEN 1 ELSE 0 END) AS marriage_leave,
            SUM(CASE WHEN attendance.leave_type = 'Hajj Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Hajj Leave' THEN 1 ELSE 0 END) AS hajj_leave,
            SUM(CASE WHEN attendance.leave_type = 'Paternity Leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Paternity Leave' THEN 1 ELSE 0 END) AS paternity_leave,
            SUM(CASE WHEN attendance.leave_type = 'Compensatory leave' AND attendance.status = 'Half Day' THEN 0.5
                    WHEN attendance.leave_type = 'Compensatory leave' THEN 1 ELSE 0 END) AS compensatory_leave,
            SUM(attendance.working_hours) AS total_hr
        FROM `tabAttendance` AS attendance
        LEFT JOIN `tabEmployee` AS emp ON attendance.employee = emp.name
        WHERE {where_clause}
        AND attendance.docstatus = 1
        GROUP BY attendance.employee, emp.department
    '''
    data = frappe.db.sql(query, as_dict=True)

    # Get standard working hours from HR Settings (in hours, default 8)
    standard_working_hours = frappe.db.get_single_value("HR Settings", "standard_working_hours") or 8

    for row in data:
        employee = row.get("employee_id")
        holiday_list = frappe.db.get_value("Employee", employee, "holiday_list")

        # Count weekly off days per employee from their holiday list
        wo_count = 0
        holiday_count = 0
        if holiday_list:
            wo_count = frappe.db.count("Holiday", filters={
                "parent": holiday_list,
                "weekly_off": 1,
                "holiday_date": ["between", [from_date, to_date]]
            })
            holiday_count = frappe.db.count("Holiday", filters={
                "parent": holiday_list,
                "weekly_off": 0,
                "holiday_date": ["between", [from_date, to_date]]
            })
        row["wo"] = wo_count
        row["holiday_count"] = holiday_count

        # Calculate OT and UT based on standard working hours
        present_days = int(row.get("present") or 0)
        total_worked_hours = float(row.get("total_hr") or 0)

        if present_days > 0 and total_worked_hours > 0:
            expected_hours = present_days * float(standard_working_hours)
            total_worked_seconds = total_worked_hours * 3600
            expected_seconds = expected_hours * 3600

            if total_worked_seconds > expected_seconds:
                row["ot"] = total_worked_seconds - expected_seconds
                row["ut"] = 0
            elif total_worked_seconds < expected_seconds:
                row["ot"] = 0
                row["ut"] = expected_seconds - total_worked_seconds
            else:
                row["ot"] = 0
                row["ut"] = 0
        else:
            row["ot"] = 0
            row["ut"] = 0

        # Convert total_hr from float hours to seconds for Duration fieldtype
        row["total_hr"] = total_worked_hours * 3600 if total_worked_hours else 0

    return data
