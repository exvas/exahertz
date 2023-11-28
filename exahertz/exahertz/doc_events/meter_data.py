import frappe
import json

@frappe.whitelist()
def delete_meter_data(doc, method=None):
    frappe.db.sql(
		"""
		DELETE FROM `tabInvoice Meter Details`
		WHERE `customer` = '{customer}'""".format(customer=doc.customer_id)
	)