// Copyright (c) 2026, sammish and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Based Checkin Details Report"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(), -30),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
		},
		{
			fieldname: "designation",
			label: __("Designation"),
			fieldtype: "Link",
			options: "Designation",
		},
		{
			fieldname: "shift",
			label: __("Shift Type"),
			fieldtype: "Link",
			options: "Shift Type",
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (!data) return value;

		// Late By - red bold
		if (column.fieldname === "late_by" && data.late_by && data.late_by !== "On Time" && data.late_by !== "") {
			value = `<span style="color:#c0392b;font-weight:600;">${data.late_by}</span>`;
		}

		// Early Exit - orange bold
		if (column.fieldname === "early_exit" && data.early_exit && data.early_exit !== "On Time" && data.early_exit !== "") {
			value = `<span style="color:#e67e22;font-weight:600;">${data.early_exit}</span>`;
		}

		// On Time - green
		if ((column.fieldname === "late_by" || column.fieldname === "early_exit") && value && data[column.fieldname] === "On Time") {
			value = `<span style="color:#27ae60;">${data[column.fieldname]}</span>`;
		}

		// Status column coloring
		if (column.fieldname === "status" && data.status) {
			if (data.status.includes("Late")) {
				value = `<span style="color:#c0392b;font-weight:600;">${data.status}</span>`;
			} else if (data.status.includes("Early Exit")) {
				value = `<span style="color:#e67e22;font-weight:600;">${data.status}</span>`;
			} else if (data.status.includes("Missing Punch")) {
				value = `<span style="color:#7f8c8d;font-weight:600;">${data.status}</span>`;
			} else if (data.status === "Regular") {
				value = `<span style="color:#27ae60;font-weight:600;">${data.status}</span>`;
			} else if (data.status === "Incomplete") {
				value = `<span style="color:#95a5a6;">${data.status}</span>`;
			}
		}

		// Log Type coloring
		if (column.fieldname === "log_type" && data.log_type) {
			if (data.log_type === "IN") {
				value = `<span style="color:#27ae60;font-weight:600;">IN</span>`;
			} else if (data.log_type === "OUT") {
				value = `<span style="color:#2980b9;font-weight:600;">OUT</span>`;
			}
		}

		// Dim sub-rows (non-first checkins in a group) for grouped columns
		let grouped_fields = ["date", "employee", "employee_name", "department", "shift",
			"shift_start", "shift_end", "first_in", "last_out", "total_punches",
			"working_hours", "late_by", "early_exit", "status"];
		if (grouped_fields.includes(column.fieldname) && !data._is_first && !data[column.fieldname]) {
			value = "";
		}

		return value;
	},
};
