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

# @frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
# def get_meter_list(doctype, txt, searchfield, start, page_len, filters):
#     query = ""
#     if txt:
#         query += "AND account_no LIKE '%{txt}%'".format(txt=txt)
#     data = frappe.db.sql("""
#         SELECT name
#         FROM `tabInvoice Meter Details`
#         WHERE customer = "{customer}"
#         {query}
#     """.format(customer=filters.get("customer"), query=query))
#     print(data)
#     return data

# @frappe.whitelist()
# def get_meter_number(doc_name):
#     return frappe.db.get_value("Meter Details", doc_name, "meter_id")