frappe.ui.form.on('Sales Invoice', {
    onload:function(frm){
        if(!frm.doc.custom_print_exchange_rate && frm.doc.docstatus == 0){
            frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_print_er", {"from_cur": frm.doc.currency, "to_cur": "USD"}).then(data=>{
                if(data){
                    frm.set_value("custom_print_exchange_rate", data)
                }
            });
            frm.trigger('get_meter_list');
        }
        
    },
    custom_print_currency: function(frm){
        frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_print_er", {"from_cur": frm.doc.currency, "to_cur": frm.doc.custom_print_currency}).then(data=>{
            frm.set_value("custom_print_exchange_rate", data)
        })
    },
    // The saved values are set on the server (set_print_amount) after ERPNext
    // has recalculated the totals. This only keeps the form preview in step.
    disable_rounded_total: function(frm){
        frm.trigger('set_print_amount');
    },
    custom_print_exchange_rate: function(frm){
        frm.trigger('set_print_amount');
    },
    set_print_amount: function(frm){
        if(frm.doc.docstatus != 0) return;
        let total = (!cint(frm.doc.disable_rounded_total) && flt(frm.doc.rounded_total)) || flt(frm.doc.grand_total);
        let amount = total * flt(frm.doc.custom_print_exchange_rate);
        frm.set_value("custom_print_amount_usd", amount);
        if(amount && frm.doc.custom_print_currency){
            frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_print_tw", {"amount": amount, curr: frm.doc.custom_print_currency}).then(data=>{
                frm.set_value("custom_print_in_words", data);
            });
        }
    },
    customer:function(frm){
        frm.set_value("custom_account_no", "")
        frm.set_value("custom_meter_no", "")
        frm.trigger('get_meter_list');
    },
    get_meter_list:function(frm){
        if(frm.doc.customer){
            frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_meter_list",{
                customer: frm.doc.customer
            }).then(data=>{
                if(data){
                    frm.set_df_property("custom_account_no", "options", data);
                }
            })
        }
    },
    custom_account_no:function(frm){
        if(frm.doc.custom_account_no){
            frappe.xcall("exahertz.exahertz.doc_events.sales_invoice.get_meter_number", {"account_no":frm.doc.custom_account_no}).then(data=>{
                if(data){
                    frm.set_value("custom_meter_no", data)
                }else{
                    frappe.msgprint("Meter number not found")
                }
            })
        }
    }
})