// Copyright (c) 2025, sammish and contributors
// For license information, please see license.txt

// frappe.query_reports["Consolidate Attendance"] = {
//     "filters": [
//     {
//     fieldname:'from_date',
//     label:__('From Date'),
//     fieldtype:'Date',
//     },
//     {
//     fieldname:'to_date',
//     label:__('To Date'),
//     fieldtype:'Date',
//     },
//     {
//     'fieldname': 'employee',
//     'label': 'Employee',
//     'fieldtype': 'MultiSelectList',
//     'get_data': function() {
//       return frappe.db.get_link_options('Employee')
//       }
//     }
//   ]
// };


// frappe.query_reports["Consolidate Attendance"] = {
//   "filters": [
//     {
//     fieldname:'from_date',
//     label:__('From Date'),
//     fieldtype:'Date',
//     },
//     {
//     fieldname:'to_date',
//     label:__('To Date'),
//     fieldtype:'Date',
//     },
//     {
//     'fieldname': 'employee',
//     'label': 'Employee',
//     'fieldtype': 'MultiSelectList',
//     'get_data': function() {
//       return frappe.db.get_link_options('Employee')
//       }
//     },
//     {
//       'fieldname': 'department',
//       'label': 'Department',
//       'fieldtype': 'Link',
//       'options': 'Department',
     
//       }
//   ]
// };



frappe.query_reports["Consolidate Attendance"] = {
  "filters": [
    {
      fieldname: 'from_date',
      label: __('From Date'),
      fieldtype: 'Date',
    },
    {
      fieldname: 'to_date',
      label: __('To Date'),
      fieldtype: 'Date',
    },
    {
      'fieldname': 'employee',
      'label': 'Employee',
      'fieldtype': 'Link',
      'options': 'Employee',
    },
    {
      'fieldname': 'department',
      'label': 'Department',
      'fieldtype': 'Link',
      'options': 'Department',
    }
  ]
};
