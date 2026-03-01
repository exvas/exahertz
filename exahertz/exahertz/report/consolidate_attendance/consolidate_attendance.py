# Copyright (c) 2025, sammish and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data



# import frappe


# def execute(filters=None):
#   columns = get_columns()
#   data = get_data(filters)
#   return columns, data

# def get_columns():
#     return [
#         {
#             'fieldname': 'attendance_date',
#             'label': 'Date',
#             'fieldtype': 'Date',
#         },
#         {
#             'fieldname': 'employee',
#             'label': 'Employee Code',
#             'fieldtype': 'Link',
#             'options': 'Employee',
#             'width': 300
#         },
       
#         {
#             'fieldname': 'status',
#             'label': 'Att Code',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'in_time',
#             'label': 'In Time',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'out_time',
#             'label': 'Out Time',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'base_hour',
#             'label': 'Base Hrs',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'working_hours',
#             'label': 'Work Hrs',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'working_hours',
#             'label': 'Total Hrs',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'ot1',
#             'label': 'OT1',
#             'fieldtype': 'int',
#             'width': 100
#         },
#         {
#             'fieldname': 'ot2',
#             'label': 'OT2',
#             'fieldtype': 'int',
#             'width': 100
#         },
#     ]

# def get_data(filters):
#     query = """
#         SELECT 
#             employee,employee_name,attendance_date,TIME_FORMAT(in_time, '%h:%i %p') AS in_time,TIME_FORMAT(out_time, '%h:%i %p') AS out_time,working_hours,
#             CASE WHEN status = 'Present' THEN 'PR' ELSE status END AS status
#         from 
#             `tabAttendance` qi
#     """
#     conditions = []
#     if filters.from_date and filters.to_date:
#         conditions.append(f"qi.attendance_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'")
#     if filters.employee:
#         employee_str = ", ".join(f"'{emp}'" for emp in filters.employee)
#         conditions.append(f"qi.employee in ({employee_str})")

#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)
#     data = frappe.db.sql(query, as_dict=True)

#     base_hour = frappe.db.get_single_value("HR Settings","standard_working_hours")
#     for item in data:
#         item["base_hour"] = base_hour
#         if item["working_hours"] > item["base_hour"]:
#             item["ot1"] = round(item["working_hours"] - item["base_hour"],2)
#     return data






# import frappe


# def execute(filters=None):
#   columns = get_columns()
#   data = get_data(filters)
#   return columns, data

# def get_columns():
#     return [
#         {
#             'fieldname': 'attendance_date',
#             'label': 'Date',
#             'fieldtype': 'Date',
#         },
#         {
#             'fieldname': 'employee',
#             'label': 'Employee Name',
#             'fieldtype': 'Link',
#             'options': 'Employee',
#             'width': 200
#         },
# # {
# #             'fieldname': 'employee_name',
# #             'label': 'Employee Name',
# #             'fieldtype': 'Link',
# #             'options': 'Employee',
# #             'width': 200
# #         },
#         {
#             'fieldname': 'status',
#             'label': 'Att Code',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'in_time',
#             'label': 'In Time',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'out_time',
#             'label': 'Out Time',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'base_hour',
#             'label': 'Base Hrs',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'working_hours',
#             'label': 'Work Hrs',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'working_hours',
#             'label': 'Total Hrs',
#             'fieldtype': 'Data',
#             'width': 100
#         },
#         {
#             'fieldname': 'ot1',
#             'label': 'OT1',
#             'fieldtype': 'int',
#             'width': 100
#         },
#         {
#             'fieldname': 'ot2',
#             'label': 'OT2',
#             'fieldtype': 'int',
#             'width': 100
#         },
#         {
#             'fieldname': 'early_exit',
#             'label': 'Early Exit',
#             'fieldtype': 'Check',
#             'width': 90
#         },
#         {
#             'fieldname': 'late_entry',
#             'label': 'Late Entry',
#             'fieldtype': 'Check',
#             'width': 90
#         },
#     ]

# def get_data(filters):
#     query = """
#         SELECT 
#             employee,employee_name,attendance_date,TIME_FORMAT(in_time, '%h:%i %p') AS in_time,TIME_FORMAT(out_time, '%h:%i %p') AS out_time,working_hours,late_entry,early_exit,
#             CASE WHEN status = 'Present' THEN 'PR' ELSE status END AS status
#         from 
#             `tabAttendance` qi
#     """
#     conditions = []
#     if filters.from_date and filters.to_date:
#         conditions.append(f"qi.attendance_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'")
#     if filters.employee:
#         employee_str = ", ".join(f"'{emp}'" for emp in filters.employee)
#         conditions.append(f"qi.employee in ({employee_str})")

#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)

#     query += " ORDER BY qi.attendance_date DESC"
#     data = frappe.db.sql(query, as_dict=True)

#     base_hour = frappe.db.get_single_value("HR Settings","standard_working_hours")
#     for item in data:
#         item["base_hour"] = base_hour
#         if item["working_hours"] > item["base_hour"]:
#             item["ot1"] = round(item["working_hours"] - item["base_hour"],2)
#     return data





import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            'fieldname': 'attendance_date',
            'label': 'Date',
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'employee',
            'label': 'Employee ID',
            'fieldtype': 'Data',
            # 'options': 'Employee',
            'width': 90
        },
        {
            'fieldname': 'employee_name',
            'label': 'Employee Name',
            'fieldtype': 'Data',
            'width': 260
        },
        {
            'fieldname': 'department',
            'label': 'Department',
            'fieldtype': 'Data',
            'width': 150
        },
        {
            'fieldname': 'status',
            'label': 'Att Code',
            'fieldtype': 'Data',
            'width': 70
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
            'fieldname': 'base_hour',
            'label': 'Base Hrs',
            'fieldtype': 'Data',
            'width': 80
        },
        {
            'fieldname': 'working_hours',
            'label': 'Work Hrs',
            'fieldtype': 'Data',
            'width': 90
        },
        {
            'fieldname': 'ot1',
            'label': 'OT1',
            'fieldtype': 'Float',
            'width': 80
        },
        {
            'fieldname': 'ot2',
            'label': 'OT2',
            'fieldtype': 'Float',
            'width': 80
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
            'fieldname': 'ut',
            'label': 'UT',
            'fieldtype': 'Data',
            'width': 90
        }
    ]
# def get_data(filters):
#     query = """
#         SELECT 
#             employee, 
#             employee_name, 
#             department, 
#             attendance_date, 
#             TIME_FORMAT(in_time, '%h:%i %p') AS in_time, 
#             TIME_FORMAT(out_time, '%h:%i %p') AS out_time, 
#             working_hours, 
#             late_entry, 
#             early_exit,
#             CASE WHEN status = 'Present' THEN 'PR' ELSE status END AS status
#         FROM `tabAttendance` qi
#     """
    
#     conditions = []
    
#     if filters.from_date and filters.to_date:
#         conditions.append(f"qi.attendance_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'")
    
#     if filters.employee:
#         employee_str = ", ".join(f"'{emp}'" for emp in filters.employee)
#         conditions.append(f"qi.employee IN ({employee_str})")
    
#     if filters.department:
#         conditions.append(f"qi.department = '{filters.department}'")

#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)

#     query += " ORDER BY qi.attendance_date DESC"
#     data = frappe.db.sql(query, as_dict=True)

#     base_hour = frappe.db.get_single_value("HR Settings", "standard_working_hours")
    
#     for item in data:
#         item["base_hour"] = base_hour
#         if item["working_hours"] and item["working_hours"] > item["base_hour"]:
#             item["ot1"] = round(item["working_hours"] - item["base_hour"], 2)
#         else:
#             item["ot1"] = 0

#     return data
# //////////////////////////////////////////////////////////////////////////////////////// use normal format no multi select upper code////////below avoid multiselect//

# def get_data(filters):
#     query = """
#         SELECT 
#             employee, 
#             employee_name, 
#             department, 
#             attendance_date, 
#             TIME_FORMAT(in_time, '%h:%i %p') AS in_time, 
#             TIME_FORMAT(out_time, '%h:%i %p') AS out_time, 
#             working_hours, 
#             late_entry, 
#             early_exit,
#             CASE WHEN status = 'Present' THEN 'PR' ELSE status END AS status
#         FROM `tabAttendance` qi
#     """
    
#     conditions = []
    
#     if filters.from_date and filters.to_date:
#         conditions.append(f"qi.attendance_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'")
    
#     if filters.employee:
#         conditions.append(f"qi.employee = '{filters.employee}'")  # Changed for single selection
    
#     if filters.department:
#         conditions.append(f"qi.department = '{filters.department}'")

#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)

#     query += " ORDER BY qi.attendance_date DESC"
#     data = frappe.db.sql(query, as_dict=True)

#     base_hour = frappe.db.get_single_value("HR Settings", "standard_working_hours")
    
#     for item in data:
#         item["base_hour"] = base_hour
#         if item["working_hours"] and item["working_hours"] > item["base_hour"]:
#             item["ot1"] = round(item["working_hours"] - item["base_hour"], 2)
#         else:
#             item["ot1"] = 0

#     return data
# /////////////////////////////////////////////////////////////////here use employe based filter//////////////////////////////////////////////


# /////////////////////////////////////////addd ut in the above code////////////////////////////////////////////

# def get_data(filters):
#     query = """
#         SELECT 
#             employee, 
#             employee_name, 
#             department, 
#             attendance_date, 
#             TIME_FORMAT(in_time, '%h:%i %p') AS in_time, 
#             TIME_FORMAT(out_time, '%h:%i %p') AS out_time, 
#             working_hours, 
#             late_entry, 
#             early_exit,
#             CASE WHEN status = 'Present' THEN 'PR' ELSE status END AS status
#         FROM `tabAttendance` qi
#     """
    
#     conditions = []
    
#     if filters.from_date and filters.to_date:
#         conditions.append(f"qi.attendance_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'")
    
#     if filters.employee:
#         conditions.append(f"qi.employee = '{filters.employee}'")  # Changed for single selection
    
#     if filters.department:
#         conditions.append(f"qi.department = '{filters.department}'")

#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)

#     query += " ORDER BY qi.employee, qi.attendance_date ASC"
#     data = frappe.db.sql(query, as_dict=True)

#     base_hour = frappe.db.get_single_value("HR Settings", "standard_working_hours")
    
#     for item in data:
#         item["base_hour"] = base_hour
#         item["ot1"] = max(0, round(item["working_hours"] - base_hour, 2)) if item["working_hours"] else 0
#         item["ut"] = max(0, round(base_hour - item["working_hours"], 2)) if item["working_hours"] else "A"

#     return data





def get_data(filters):
    query = """
        SELECT 
            employee, 
            employee_name, 
            department, 
            attendance_date, 
            TIME_FORMAT(in_time, '%h:%i %p') AS in_time, 
            TIME_FORMAT(out_time, '%h:%i %p') AS out_time, 
            working_hours, 
            late_entry, 
            early_exit,
            CASE WHEN status = 'Present' THEN 'PR' ELSE status END AS status
        FROM `tabAttendance` qi
    """
    
    conditions = []
    
    if filters.from_date and filters.to_date:
        conditions.append(f"qi.attendance_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'")
    
    if filters.employee:
        conditions.append(f"qi.employee = '{filters.employee}'")  # Changed for single selection
    
    if filters.department:
        conditions.append(f"qi.department = '{filters.department}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Order by department alphabetically first, then employee, then attendance_date
    query += " ORDER BY qi.department ASC, qi.employee, qi.attendance_date ASC"
    
    data = frappe.db.sql(query, as_dict=True)

    base_hour = frappe.db.get_single_value("HR Settings", "standard_working_hours")
    
    for item in data:
        item["base_hour"] = base_hour
        item["ot1"] = max(0, round(item["working_hours"] - base_hour, 2)) if item["working_hours"] else 0
        item["ut"] = max(0, round(base_hour - item["working_hours"], 2)) if item["working_hours"] else "A"

    return data








