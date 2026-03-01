

# import frappe
# import calendar
# from datetime import datetime

# def execute(filters=None):
#     columns = get_columns(filters)
#     data = get_data(filters)
#     return columns, data

# def get_columns(filters):
#     month_days = calendar.monthrange(int(filters.year), int(filters.month))[1]
#     columns = [
#         # {"label": "No", "fieldname": "no", "fieldtype": "Data", "width": 50},
#         {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 100}
#     ]
    
#     for day in range(1, month_days + 1):
#         columns.append({
#             "label": str(day),
#             "fieldname": f"day_{day}",
#             "fieldtype": "Data",
#             "width": 140
#         })

#     return columns

# def get_data(filters):
#     month_days = calendar.monthrange(int(filters.year), int(filters.month))[1]
#     data = []

#     conditions = f"attendance_date BETWEEN '{filters.year}-{int(filters.month):02d}-01' AND '{filters.year}-{int(filters.month):02d}-{month_days}'"
#     if filters.employee:
#         conditions += f" AND employee = '{filters.employee}'"
#     if filters.department:
#         conditions += f" AND employee IN (SELECT name FROM `tabEmployee` WHERE department = '{filters.department}')"
    
#     attendances = frappe.db.sql(f"""
#         SELECT employee, attendance_date, TIME(in_time) AS in_time, TIME(out_time) AS out_time
#         FROM `tabAttendance`
#         WHERE {conditions}
#     """, as_dict=True)

#     # Fetch holidays
#     holidays = frappe.db.sql(f"""
#         SELECT holidays.holiday_date, holiday_list.name AS holiday_list
#         FROM `tabHoliday` AS holidays
#         JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
#         WHERE holiday_date BETWEEN '{filters.year}-{int(filters.month):02d}-01' AND '{filters.year}-{int(filters.month):02d}-{month_days}'
#     """, as_dict=True)

#     holiday_dates = {holiday.holiday_date: 'WO' for holiday in holidays}

#     employee_data = {}
    
#     for att in attendances:
#         key = att.employee
#         if key not in employee_data:
#             employee_data[key] = {"employee": key, **{f"day_{d}": holiday_dates.get(datetime(filters.year, int(filters.month), d).date(), "") for d in range(1, month_days + 1)}}
        
#         day = att.attendance_date.day
#         employee_data[key][f"day_{day}"] = f"{att.in_time or ''} / {att.out_time or ''}"

#     for i, emp in enumerate(employee_data.values(), 1):
#         emp["no"] = i
#         data.append(emp)

#     return data


# ///////////////////////////////////////////////////////////////////////////////////////////////


# import frappe
# import calendar
# from datetime import datetime, timedelta

# def execute(filters=None):
#     columns = get_columns(filters)
#     data = get_data(filters)
#     return columns, data

# def get_columns(filters):
#     month_days = calendar.monthrange(int(filters.year), int(filters.month))[1]
#     columns = [
#         {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 90},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150}
#     ]
    
#     for day in range(1, month_days + 1):
#         columns.append({
#             "label": str(day),
#             "fieldname": f"day_{day}",
#             "fieldtype": "Data",
#             "width": 140
#         })

#     return columns

# def get_data(filters):
#     month_days = calendar.monthrange(int(filters.year), int(filters.month))[1]
#     data = []
#     conditions = f"attendance_date BETWEEN '{filters.year}-{int(filters.month):02d}-01' AND '{filters.year}-{int(filters.month):02d}-{month_days}'"
    
#     if filters.employee:
#         conditions += f" AND employee = '{filters.employee}'"
#     if filters.department:
#         conditions += f" AND employee IN (SELECT name FROM `tabEmployee` WHERE department = '{filters.department}')"
    
#     attendances = frappe.db.sql(f"""
#         SELECT employee, attendance_date, TIME(in_time) AS in_time, TIME(out_time) AS out_time
#         FROM `tabAttendance`
#         WHERE {conditions}
#     """, as_dict=True)

#     # Fetch holidays
#     holidays = frappe.db.sql(f"""
#         SELECT holidays.holiday_date
#         FROM `tabHoliday` AS holidays
#         JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
#         WHERE holiday_date BETWEEN '{filters.year}-{int(filters.month):02d}-01' AND '{filters.year}-{int(filters.month):02d}-{month_days}'
#     """, as_dict=True)
    
#     holiday_dates = {holiday.holiday_date: 'WO' for holiday in holidays}
    
#     # Fetch leave applications
#     leave_applications = frappe.db.sql(f"""
#         SELECT employee, from_date, to_date, leave_type
#         FROM `tabLeave Application`
#         WHERE from_date <= '{filters.year}-{int(filters.month):02d}-{month_days}'
#         AND to_date >= '{filters.year}-{int(filters.month):02d}-01'
#     """, as_dict=True)
    
#     leave_dates = {}
#     for leave in leave_applications:
#         current_date = leave.from_date
#         while current_date <= leave.to_date:
#             leave_code = "LOP" if leave.leave_type == "Leave Without Pay" else "SL" if leave.leave_type == "Sick Leave" else "LV"
#             leave_code = "LOP" if leave.leave_type == "Leave Without Pay" else "SL" if leave.leave_type == "Sick Leave" else "CL" if leave.leave_type == "Casual Leave" else "LV"
#             leave_dates.setdefault(leave.employee, {})[current_date] = leave_code
#             current_date += timedelta(days=1)
    
#     employee_data = {}
    
#     for att in attendances:
#         key = att.employee
#         if key not in employee_data:
#             employee_data[key] = {"employee": key, **{f"day_{d}": holiday_dates.get(datetime(filters.year, int(filters.month), d).date(), "") for d in range(1, month_days + 1)}}
        
#         day = att.attendance_date.day
#         employee_data[key][f"day_{day}"] = f"{att.in_time or ''} / {att.out_time or ''}"
       
    
#     # Update leave details
#     for emp, leave_days in leave_dates.items():
#         if emp not in employee_data:
#             employee_data[emp] = {"employee": emp, **{f"day_{d}": holiday_dates.get(datetime(filters.year, int(filters.month), d).date(), "") for d in range(1, month_days + 1)}}
        
#         for leave_date, leave_code in leave_days.items():
#             day = leave_date.day
#             employee_data[emp][f"day_{day}"] = leave_code
    
#     for i, emp in enumerate(employee_data.values(), 1):
#         emp["no"] = i
#         data.append(emp)
    
#     return data


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import frappe
import calendar
from datetime import datetime, timedelta

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    month_days = calendar.monthrange(int(filters.year), int(filters.month))[1]
    columns = [
        {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Data",  "width": 70},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 130}
    ]
    
    for day in range(1, month_days + 1):
        columns.append({
            "label": str(day),
            "fieldname": f"day_{day}",
            "fieldtype": "Data",
            "width": 90
        })

    return columns

def get_data(filters):
    month_days = calendar.monthrange(int(filters.year), int(filters.month))[1]
    data = []
    conditions = f"attendance_date BETWEEN '{filters.year}-{int(filters.month):02d}-01' AND '{filters.year}-{int(filters.month):02d}-{month_days}'"
    
    if filters.employee:
        conditions += f" AND employee = '{filters.employee}'"
    if filters.department:
        conditions += f" AND employee IN (SELECT name FROM `tabEmployee` WHERE department = '{filters.department}')"
    
    attendances = frappe.db.sql(f"""
        SELECT employee, employee_name, attendance_date, 
        DATE_FORMAT(in_time, '%H:%i') AS in_time, 
        DATE_FORMAT(out_time, '%H:%i') AS out_time
        FROM `tabAttendance`
        WHERE {conditions}
        """, as_dict=True)


    # Fetch holidays
    holidays = frappe.db.sql(f"""
        SELECT holidays.holiday_date
        FROM `tabHoliday` AS holidays
        JOIN `tabHoliday List` AS holiday_list ON holidays.parent = holiday_list.name
        WHERE holiday_date BETWEEN '{filters.year}-{int(filters.month):02d}-01' AND '{filters.year}-{int(filters.month):02d}-{month_days}'
    """, as_dict=True)
    
    holiday_dates = {holiday.holiday_date: 'WO' for holiday in holidays}
    
    # Fetch leave applications
    leave_applications = frappe.db.sql(f"""
        SELECT employee, from_date, to_date, leave_type
        FROM `tabLeave Application`
        WHERE from_date <= '{filters.year}-{int(filters.month):02d}-{month_days}'
        AND to_date >= '{filters.year}-{int(filters.month):02d}-01'
    """, as_dict=True)
    
    leave_dates = {}
    for leave in leave_applications:
        current_date = leave.from_date
        while current_date <= leave.to_date:
            leave_code = (
                "LOP" if leave.leave_type == "Leave Without Pay" else
                "SL" if leave.leave_type == "Sick Leave" else
                "CL" if leave.leave_type == "Casual Leave" else
                "AL" if leave.leave_type == "Annual Leave" else
                "EL" if leave.leave_type == "Emergency Leave" else
                "ML" if leave.leave_type == "Maternity Leave" else
                ''
            )

            leave_dates.setdefault(leave.employee, {})[current_date] = leave_code
            current_date += timedelta(days=1)
    
    employee_data = {}
    
    for att in attendances:
        key = att.employee
        if key not in employee_data:
            employee_data[key] = {"employee": key, "employee_name": att.employee_name, **{f"day_{d}": holiday_dates.get(datetime(filters.year, int(filters.month), d).date(), "") for d in range(1, month_days + 1)}}
        
        day = att.attendance_date.day
        employee_data[key][f"day_{day}"] = f"{att.in_time or ''} / {att.out_time or ''}"
       
    # Update leave details
    for emp, leave_days in leave_dates.items():
        if emp not in employee_data:
            employee_data[emp] = {"employee": emp, "employee_name": frappe.db.get_value('Employee', emp, 'employee_name'), **{f"day_{d}": holiday_dates.get(datetime(filters.year, int(filters.month), d).date(), "") for d in range(1, month_days + 1)}}
        
        for leave_date, leave_code in leave_days.items():
            day = leave_date.day
            employee_data[emp][f"day_{day}"] = leave_code
    
    for i, emp in enumerate(employee_data.values(), 1):
        emp["no"] = i
        data.append(emp)
    
    return data
