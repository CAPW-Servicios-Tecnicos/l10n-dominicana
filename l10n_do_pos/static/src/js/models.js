// © 2015-2018 Eneldo Serrata <eneldo@marcos.do>
// © 2017-2018 Gustavo Valverde <gustavo@iterativo.do>
// © 2018 Francisco Peñaló <frankpenalo24@gmail.com>
// © 2018 Kevin Jiménez <kevinjimenezlorenzo@gmail.com>
// © 2019-2020 Raul  Ovalle <raulovallet@gmail.com>
// © 2021-2022 Alejandro Capellan <acapellan@capw.com.do>

// This file is part of NCF Manager.

// NCF Manager is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// NCF Manager is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with NCF Manager.  If not, see <https://www.gnu.org/licenses/>.

odoo.define('l10n_do_pos.models', function (require) {
    "use strict";

var models = require('point_of_sale.models');
var _super_order = models.Order.prototype;
var _super_posmodel = models.PosModel.prototype;
var rpc = require('web.rpc');

models.load_fields('account.move', ['name', 'l10n_do_fiscal_number']);

//models.Order = models.Order.extend({
//    export_for_printing: function() {
//        var order = _super_order.export_for_printing.apply(this,arguments);
//        order.l10n_do_fiscal_number = this.env.pos.account_move.l10n_do_fiscal_number;
//        return order;
//    },
//});

});
