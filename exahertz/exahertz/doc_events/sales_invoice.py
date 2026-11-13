import frappe
from frappe.utils import cint, flt, money_in_words

@frappe.whitelist()
def get_print_er(from_cur, to_cur):
    if frappe.db.exists("Currency Exchange", {"from_currency": from_cur, "to_currency": to_cur}):
        doc = frappe.get_last_doc("Currency Exchange", {"from_currency": from_cur, "to_currency": to_cur})
        return doc.exchange_rate

@frappe.whitelist()
def get_print_tw(amount, curr):
    return money_in_words(amount, curr)

def get_print_base_total(doc):
    """Amount the print currency figures are based on.

    The rounded total is only used when rounding is enabled on the invoice;
    with "Disable Rounded Total" ticked the grand total is used as is.
    """
    if not cint(doc.get("disable_rounded_total")) and flt(doc.get("rounded_total")):
        return flt(doc.rounded_total)
    return flt(doc.get("grand_total"))

def set_print_amount(doc, method=None):
    """Sales Invoice validate: runs after ERPNext has recalculated the totals,
    so the print currency amount always follows the saved grand / rounded total."""
    if not doc.get("custom_print_currency"):
        return

    if not flt(doc.get("custom_print_exchange_rate")):
        doc.custom_print_exchange_rate = get_print_er(doc.currency, doc.custom_print_currency)

    amount = get_print_base_total(doc) * flt(doc.get("custom_print_exchange_rate"))
    doc.custom_print_amount_usd = amount
    doc.custom_print_in_words = money_in_words(amount, doc.custom_print_currency) if amount else ""

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