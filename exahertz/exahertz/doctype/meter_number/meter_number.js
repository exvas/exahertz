// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Meter Number", {
	after_save(frm) {
        frappe.xcall("exahertz.exahertz.doc_events.meter_data.make_inv_meter_data", {
            meter_list: frm.doc.meter_details,
            customer: frm.doc.customer_name
        })
	},
});
