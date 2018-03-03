odoo.define('ncf_pos.invoices', function (require) {
    "use strict";
    var screens = require('point_of_sale.screens');
    
    var QueryInvoicesButton = screens.ActionButtonWidget.extend({
        template: 'QueryInvoicesButton',
        button_click: function(){
            alert("Aqui va la llamada a la pantalla");
        },
    });
    
    screens.define_action_button({
        'name': 'invoices_query',
        'widget': QueryInvoicesButton,
        'condition': function(){
            return true;
        },
    });
    
    });