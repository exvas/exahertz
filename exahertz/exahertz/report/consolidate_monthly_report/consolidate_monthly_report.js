// Copyright (c) 2026, sammish and contributors
// For license information, please see license.txt

frappe.query_reports["Consolidate Monthly Report"] = {
	"filters": [
		{
			'fieldname': 'from_date',
			'label': __('From Date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.month_start(),
		},
		{
			'fieldname': 'to_date',
			'label': __('To Date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.get_today(),
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
			PR - Present || AB - Absent || WO - Weekly Off || HL - Holiday || SL - Sick Leave || NL - Normal Leave || ANLL - Annual Leave || UPL - Unpaid Leave || EL - Emergency Leave || EXL - Examination Leave ||
			STL - Study Leave || ML - Maternity Leave || AL - Accompanying Leave || BL - Bereavement Leave || MRL - Marriage Leave || HJL - Hajj Leave || PL - Paternity Leave || CL - Compensatory Leave || OA - Official Assignment ||
			BH - Base Hours || UT - Under Time || MP - Mis-Punch
		</div>
	`;

	// Ensure legend is added only once
	setTimeout(() => {
		let $report_area = $(".page-form");
		if (!$("#attendance-legend").length) {
			$report_area.after(legend_html);
		}
	}, 500);
}

};
