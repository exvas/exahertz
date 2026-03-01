
frappe.query_reports["Employee Monthwise"] = {
    filters: [
        {
            fieldname: "employee",
            label: __("Employee"),
            fieldtype: "Link",
            options: "Employee",
            reqd: 0
        },
        {
            fieldname: "month",
            label: __("Month"),
            fieldtype: "Select",
            options: [
                { "value": 1, "label": "January" },
                { "value": 2, "label": "February" },
                { "value": 3, "label": "March" },
                { "value": 4, "label": "April" },
                { "value": 5, "label": "May" },
                { "value": 6, "label": "June" },
                { "value": 7, "label": "July" },
                { "value": 8, "label": "August" },
                { "value": 9, "label": "September" },
                { "value": 10, "label": "October" },
                { "value": 11, "label": "November" },
                { "value": 12, "label": "December" }
            ],
            reqd: 1
        },
        {
            fieldname: "year",
            label: __("Year"),
            fieldtype: "Int",
            default: new Date().getFullYear(),
            reqd: 1
        },
        {
            fieldname: "department",
            label: __("Department"),
            fieldtype: "Link",
            options: "Department",
            reqd: 0
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

