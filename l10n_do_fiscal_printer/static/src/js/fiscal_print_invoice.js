odoo.define('account.move', function (require) {
"use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var dom_ready = require('web.dom_ready');
    var field_registry = require('web.field_registry');
    var field_utils = require('web.field_utils');
    var ajax = require('web.ajax');

    var button = $('#print_fiscal_invoice');

    var _onButton = function(e) {
        console.log(e);
    }

    button.click(_onButton);
});