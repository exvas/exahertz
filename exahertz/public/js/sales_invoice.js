frappe.ui.form.on('Sales Invoice', {
    onload:function(frm){
        frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_print_er", {"from_cur": frm.doc.currency, "to_cur": "USD"}).then(data=>{
            frm.set_value("custom_print_exchange_rate", data)
        })
    },
    custom_print_currency: function(frm){
        frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_print_er", {"from_cur": frm.doc.currency, "to_cur": frm.doc.custom_print_currency}).then(data=>{
            frm.set_value("custom_print_exchange_rate", data)
        })
    },
    validate:function(frm){
        let total = frm.doc.rounded_total || frm.doc.grand_total
        frm.set_value("custom_print_amount_usd", total * frm.doc.custom_print_exchange_rate)
        frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_print_tw", {"amount": total*frm.doc.custom_print_exchange_rate, curr: frm.doc.custom_print_currency}).then(data=>{
            frm.set_value("custom_print_in_words", data)
        })
    }
})