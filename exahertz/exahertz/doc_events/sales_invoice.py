import frappe
from frappe.utils import money_in_words

@frappe.whitelist()
def get_print_er(from_cur, to_cur):
    if frappe.db.exists("Currency Exchange", {"from_currency": from_cur, "to_currency": to_cur}):
        doc = frappe.get_last_doc("Currency Exchange", {"from_currency": from_cur, "to_currency": to_cur})
        return doc.exchange_rate

@frappe.whitelist()
def get_print_tw(amount, curr):
    return money_in_words(amount, curr)

@frappe.whitelist()
def get_meter_list(customer):
    acc_list =  frappe.db.get_list("Meter Details", {"parent":customer}, ["account_no"], pluck="account_no", ignore_permissions=True)
    acc = [""]
    if acc_list:
        return acc + acc_list
    else:
        return []

@frappe.whitelist()
def get_meter_number(account_no):
    return frappe.db.get_value("Meter Details", {"account_no": account_no}, "meter_id")