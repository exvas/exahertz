frappe.ui.form.on('Sales Invoice', {
    onload:function(frm){
        frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_print_er", {"from_cur": frm.doc.currency, "to_cur": "USD"}).then(data=>{
            frm.set_value("custom_print_exchange_rate", data)
        });
        frm.trigger('get_meter_list');
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
    },
    customer:function(frm){
        frm.set_value("custom_account_no", "")
        frm.set_value("custom_meter_no", "")
        frm.trigger('get_meter_list');
    },
    get_meter_list:function(frm){
        frm.set_query('custom_account_no', function(){
            if(frm.doc.customer){
                return {
                    query: "exahertz.exahertz.doc_events.sales_invoice.get_meter_list",
                    filters: {
                        customer: frm.doc.customer
                    }
                }
            }
        })
    },
    custom_account_no:function(frm){
        if(frm.doc.custom_account_no){
            frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_meter_number", {"doc_name":frm.doc.custom_account_no}).then(data=>{
                if(data){
                    frm.set_value("custom_meter_no", data)
                }else{
                    frappe.msgprint("Meter number not found")
                }
            })
        }
    }
})