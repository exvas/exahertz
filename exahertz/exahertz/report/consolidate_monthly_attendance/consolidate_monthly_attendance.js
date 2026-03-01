// Copyright (c) 2025, sammish and contributors
// For license information, please see license.txt


frappe.query_reports["Consolidate Monthly Attendance"] = {
	"filters": [
		{
			'fieldname': 'from_date',
			'label': __('From Date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.month_start(),  // First day of the current month
		},
		{
			'fieldname': 'to_date',
			'label': __('To Date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.get_today(),  // Today's date
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
	],

	"onload": function(report) {
	let legend_html = `
		<div id="attendance-legend" style="margin-top: 10px; margin-bottom: 10px; padding: 10px; font-weight: bold; background: #000080; color: #FFFFFF; border: 1px solid #ddd; border-radius: 5px;">
			PR - Present || AB - Absent ||  HL - Holiday || SL - Sick Leave ||  AL - Annual Leave || NP - No Pay Leave || EL - Emergency Leave || SD - Site Duty || Study Leave || ML - Maternity Leave || HDL - Half Day Leave || LOP - Leave Without Pay || 
			BH - Base Hours || OT - Overtime || OT-2 - Overtime on Holidays || UT - Under Time 
		</div>
	`;

	// Ensure legend is added only once
	setTimeout(() => {
		let $report_area = $(".page-form");  // Targeting the area above the report
		if (!$("#attendance-legend").length) {
			$report_area.after(legend_html);
		}
	}, 500);
}

};
