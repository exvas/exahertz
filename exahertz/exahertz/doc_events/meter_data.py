import frappe
import json

@frappe.whitelist()
def make_inv_meter_data(meter_list=None, customer=None):
    if not meter_list:
        return
    meter_list = json.loads(meter_list)
    frappe.db.sql(
		"""
		DELETE FROM `tabInvoice Meter Details`
		WHERE `customer` = '{customer}'""".format(customer=customer)
	)
    for data in meter_list:
        if not frappe.db.exists("Invoice Meter Details", {"meter_details":data.get("name")}):
            imd = frappe.new_doc("Invoice Meter Details")
            imd.meter_details = data.get("name")
            imd.account_no = data.get("account_no")
            imd.meter_no = data.get("meter_id")
            imd.customer = customer
            imd.save(ignore_permissions=True)

@frappe.whitelist()
def delete_meter_data(doc, method=None):
    frappe.db.sql(
		"""
		DELETE FROM `tabInvoice Meter Details`
		WHERE `customer` = '{customer}'""".format(customer=doc.customer_name)
	)