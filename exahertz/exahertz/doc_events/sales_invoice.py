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
    