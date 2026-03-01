# Copyright (c) 2025, sammish and contributors
# For license information, please see license.txt


import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
     return [
        {'fieldname': 'employee', 'label': 'Employee ID', 'fieldtype': 'Data', 'width': 90},
        {'fieldname': 'employee_name', 'label': 'Employee Name', 'fieldtype': 'Data', 'width': 260},
        {'fieldname': 'department', 'label': 'Department', 'fieldtype': 'Link', 'options': 'Department', 'width': 100},
        {'fieldname': 'present', 'label': 'PR', 'fieldtype': 'Int', 'width': 60},  # Count of Present days
       
    
  
       
       
       
        {
            'fieldname': 'off',
            'label': 'AB',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'hollyday',
            'label': 'HL',
            'fieldtype': 'Data',
            'width': 70
        },
        {
            'fieldname': 'anual_leave',
            'label': 'AL',
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
            'fieldname': 'nopay_leave',
            'label': 'NP',
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
            'fieldname': 'site_duty',
            'label': 'SD',
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
            'label': 'Study Leave',
            'fieldtype': 'Data',
            'width': 70
        },
        {
            'fieldname': 'half_day_leave',
            'label': 'HDL',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'leave_with_out_pay',
            'label': 'LOP',
            'fieldtype': 'Data',
            'width': 60
        },
         {
            'fieldname': 'bh',
            'label': 'BH',
            'fieldtype': 'Data',
            'width': 50
        },
         {
            'fieldname': 'ot',
            'label': 'OT',
            'fieldtype': 'Data',
            'width': 50
        },
           {
            'fieldname': 'ot_2',
            'label': 'OT-2',
            'fieldtype': 'Data',
            'width': 60
        },
        {
            'fieldname': 'ut',
            'label': 'UT',
            'fieldtype': 'Data',
            'width': 60
        },
         {'fieldname': 'total_hr', 'label': 'Total Hr', 'fieldtype': 'Float', 'width': 90}, # Total working hours
       
    ]



# def get_data(filters):
#     standard_working_hours = frappe.db.get_single_value('HR Settings', 'standard_working_hours') or 8  # Default to 8 hours
    
#     conditions = []
#     if filters.get("from_date"):
#         conditions.append(f"attendance.attendance_date >= '{filters.get('from_date')}'")
#     if filters.get("to_date"):
#         conditions.append(f"attendance.attendance_date <= '{filters.get('to_date')}'")
#     if filters.get("employee"):
#         conditions.append(f"attendance.employee = '{filters.get('employee')}'")
#     if filters.get("department"):
#         conditions.append(f"attendance.department = '{filters.get('department')}'")

#     where_clause = " AND ".join(conditions) if conditions else "1=1"

#     query = f'''
#         SELECT 
#             attendance.employee, 
#             attendance.employee_name, 
#             attendance.department, 
#             COUNT(CASE WHEN attendance.status = 'Present' THEN 1 END) AS present,
#             COUNT(CASE WHEN attendance.status = 'Absent' THEN 1 END) AS off,
#             COUNT(CASE WHEN attendance.status = 'Half Day' THEN 1 END) AS half_day_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Sick Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Sick Leave' THEN 1 ELSE 0 END) AS sick_leave,        
#             SUM(CASE WHEN attendance.leave_type = 'Maternity Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Maternity Leave' THEN 1 ELSE 0 END) AS maternity_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Emergency Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Emergency Leave' THEN 1 ELSE 0 END) AS emergency_leave,
#             SUM(CASE WHEN attendance.leave_type = 'No Pay Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'No Pay Leave' THEN 1 ELSE 0 END) AS nopay_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Site Duty' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Site Duty' THEN 1 ELSE 0 END) AS site_duty,
#             COUNT(CASE WHEN attendance.leave_type = 'Anual Leave' THEN 1 END) AS anual_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Leave Without Pay' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Leave Without Pay' THEN 1 ELSE 0 END) AS leave_with_out_pay,
#             SUM(attendance.working_hours) AS total_hr,
#             SUM(CASE WHEN attendance.working_hours > {standard_working_hours} THEN attendance.working_hours - {standard_working_hours} ELSE 0 END) AS ot,
#             SUM(CASE WHEN attendance.working_hours < {standard_working_hours} THEN {standard_working_hours} - attendance.working_hours ELSE 0 END) AS ut,
            
#             -- Count holidays from the linked Holiday List
#             (SELECT COUNT(holidays.holiday_date) 
#              FROM `tabHoliday` AS holidays 
#              JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
#              WHERE holiday_list.name = employee.holiday_list
#              AND holidays.holiday_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'
#             ) AS hollyday
            
#         FROM `tabAttendance` AS attendance
#         LEFT JOIN `tabEmployee` AS employee ON attendance.employee = employee.name
#         WHERE {where_clause}
#         GROUP BY attendance.employee, attendance.employee_name, employee.holiday_list
#     '''
    
#     data = frappe.db.sql(query, as_dict=True)
#     return data
# //////////////////////////////////////////////////////////////////////////////////////perfect///////////////////////////////////////////////////


# def get_data(filters):
#     standard_working_hours = frappe.db.get_single_value('HR Settings', 'standard_working_hours') or 8  # Default to 8 hours

#     conditions = []
#     if filters.get("from_date"):
#         conditions.append(f"attendance.attendance_date >= '{filters.get('from_date')}'")
#     if filters.get("to_date"):
#         conditions.append(f"attendance.attendance_date <= '{filters.get('to_date')}'")
#     if filters.get("employee"):
#         conditions.append(f"attendance.employee = '{filters.get('employee')}'")
#     if filters.get("department"):
#         conditions.append(f"attendance.department = '{filters.get('department')}'")

#     where_clause = " AND ".join(conditions) if conditions else "1=1"

#     query = f'''
#         SELECT 
#             attendance.employee, 
#             attendance.employee_name, 
#             attendance.department, 
#             COUNT(CASE WHEN attendance.status = 'Present' THEN 1 END) AS present,
#             COUNT(CASE WHEN attendance.status = 'Absent' THEN 1 END) AS off,
#             COUNT(CASE WHEN attendance.status = 'Half Day' THEN 1 END) AS half_day_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Sick Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Sick Leave' THEN 1 ELSE 0 END) AS sick_leave,        
#             SUM(CASE WHEN attendance.leave_type = 'Maternity Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Maternity Leave' THEN 1 ELSE 0 END) AS maternity_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Study Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Study Leave' THEN 1 ELSE 0 END) AS study_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Emergency Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Emergency Leave' THEN 1 ELSE 0 END) AS emergency_leave,
#             SUM(CASE WHEN attendance.leave_type = 'No Pay Leave' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'No Pay Leave' THEN 1 ELSE 0 END) AS nopay_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Site Duty' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Site Duty' THEN 1 ELSE 0 END) AS site_duty,
#             COUNT(CASE WHEN attendance.leave_type = 'Anual Leave' THEN 1 END) AS anual_leave,
#             SUM(CASE WHEN attendance.leave_type = 'Leave Without Pay' AND attendance.status = 'Half Day' THEN 0.5 
#                      WHEN attendance.leave_type = 'Leave Without Pay' THEN 1 ELSE 0 END) AS leave_with_out_pay,
#             SUM(attendance.working_hours) AS total_hr,
#             SUM(CASE WHEN attendance.working_hours > {standard_working_hours} THEN attendance.working_hours - {standard_working_hours} ELSE 0 END) AS ot,
#             SUM(CASE WHEN attendance.working_hours < {standard_working_hours} THEN {standard_working_hours} - attendance.working_hours ELSE 0 END) AS ut,
            
#             -- Fetch custom base hour from Employee
#             emp.custom_base_hour AS bh,
            
#             -- Count holidays from the linked Holiday List
#             (SELECT COUNT(holidays.holiday_date) 
#              FROM `tabHoliday` AS holidays 
#              JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
#              WHERE holiday_list.name = emp.holiday_list
#              AND holidays.holiday_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'
#             ) AS hollyday,

#             -- Calculate OT-2 for hours worked on holidays
#             SUM(CASE WHEN attendance.attendance_date IN (
#                 SELECT holidays.holiday_date 
#                 FROM `tabHoliday` AS holidays 
#                 JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
#                 WHERE holiday_list.name = emp.holiday_list
#                 AND holidays.holiday_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'
#             ) THEN attendance.working_hours ELSE 0 END) AS ot_2

#         FROM `tabAttendance` AS attendance
#         LEFT JOIN `tabEmployee` AS emp ON attendance.employee = emp.name
#         WHERE {where_clause}
#         GROUP BY attendance.employee, attendance.employee_name, emp.holiday_list
#     '''
    
#     data = frappe.db.sql(query, as_dict=True)
#     return data




# /////////////////////////////////////////////////////////ot based on shift////////////////////////////////////////////////////////////////////////////////

def get_data(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append(f"attendance.attendance_date >= '{filters.get('from_date')}'")
    if filters.get("to_date"):
        conditions.append(f"attendance.attendance_date <= '{filters.get('to_date')}'")
    if filters.get("employee"):
        conditions.append(f"attendance.employee = '{filters.get('employee')}'")
    if filters.get("department"):
        conditions.append(f"attendance.department = '{filters.get('department')}'")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f'''
        SELECT 
            attendance.employee, 
            attendance.employee_name, 
            attendance.department, 
            COUNT(CASE WHEN attendance.status = 'Present' THEN 1 END) AS present,
            COUNT(CASE WHEN attendance.status = 'Absent' THEN 1 END) AS off,
            COUNT(CASE WHEN attendance.status = 'Half Day' THEN 1 END) AS half_day_leave,
            SUM(CASE WHEN attendance.leave_type = 'Sick Leave' AND attendance.status = 'Half Day' THEN 0.5 
                     WHEN attendance.leave_type = 'Sick Leave' THEN 1 ELSE 0 END) AS sick_leave,        
            SUM(CASE WHEN attendance.leave_type = 'Maternity Leave' AND attendance.status = 'Half Day' THEN 0.5 
                     WHEN attendance.leave_type = 'Maternity Leave' THEN 1 ELSE 0 END) AS maternity_leave,
            SUM(CASE WHEN attendance.leave_type = 'Study Leave' AND attendance.status = 'Half Day' THEN 0.5 
                     WHEN attendance.leave_type = 'Study Leave' THEN 1 ELSE 0 END) AS study_leave,
            SUM(CASE WHEN attendance.leave_type = 'Emergency Leave' AND attendance.status = 'Half Day' THEN 0.5 
                     WHEN attendance.leave_type = 'Emergency Leave' THEN 1 ELSE 0 END) AS emergency_leave,
            SUM(CASE WHEN attendance.leave_type = 'No Pay Leave' AND attendance.status = 'Half Day' THEN 0.5 
                     WHEN attendance.leave_type = 'No Pay Leave' THEN 1 ELSE 0 END) AS nopay_leave,
            SUM(CASE WHEN attendance.leave_type = 'Site Duty' AND attendance.status = 'Half Day' THEN 0.5 
                     WHEN attendance.leave_type = 'Site Duty' THEN 1 ELSE 0 END) AS site_duty,
            COUNT(CASE WHEN attendance.leave_type = 'Anual Leave' THEN 1 END) AS anual_leave,
            SUM(CASE WHEN attendance.leave_type = 'Leave Without Pay' AND attendance.status = 'Half Day' THEN 0.5 
                     WHEN attendance.leave_type = 'Leave Without Pay' THEN 1 ELSE 0 END) AS leave_with_out_pay,
            SUM(attendance.working_hours) AS total_hr,

            -- Calculate Standard Working Hours dynamically from Shift Type
            TIMESTAMPDIFF(HOUR, shift.start_time, shift.end_time) AS standard_working_hours,

            -- Calculate OT and UT based on dynamic working hours
            SUM(CASE WHEN attendance.working_hours > TIMESTAMPDIFF(HOUR, shift.start_time, shift.end_time) 
                     THEN attendance.working_hours - TIMESTAMPDIFF(HOUR, shift.start_time, shift.end_time) ELSE 0 END) AS ot,

            SUM(CASE WHEN attendance.working_hours < TIMESTAMPDIFF(HOUR, shift.start_time, shift.end_time) 
                     THEN TIMESTAMPDIFF(HOUR, shift.start_time, shift.end_time) - attendance.working_hours ELSE 0 END) AS ut,

            -- Fetch custom base hour from Employee
            emp.custom_base_hour AS bh,

            -- Count holidays from the linked Holiday List
            (SELECT COUNT(holidays.holiday_date) 
             FROM `tabHoliday` AS holidays 
             JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
             WHERE holiday_list.name = emp.holiday_list
             AND holidays.holiday_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'
            ) AS hollyday,

            -- Calculate OT-2 for hours worked on holidays
            SUM(CASE WHEN attendance.attendance_date IN (
                SELECT holidays.holiday_date 
                FROM `tabHoliday` AS holidays 
                JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
                WHERE holiday_list.name = emp.holiday_list
                AND holidays.holiday_date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'
            ) THEN attendance.working_hours ELSE 0 END) AS ot_2

        FROM `tabAttendance` AS attendance
        LEFT JOIN `tabEmployee` AS emp ON attendance.employee = emp.name
        LEFT JOIN `tabShift Type` AS shift ON attendance.shift = shift.name  -- Join to fetch shift details
        WHERE {where_clause}
        GROUP BY attendance.employee, attendance.employee_name
    '''
    
    data = frappe.db.sql(query, as_dict=True)
    return data
