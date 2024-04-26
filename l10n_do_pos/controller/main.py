# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import http, models, fields, _
from odoo.http import request

logger = logging.getLogger(__name__)


class Pos(http.Controller):

    @http.route('/get_ncf', type='json', auth='public')
    def get_ncf_order(self, order):
        pos_order_id = request.env['pos.order'].search([('pos_reference', '=', order)], limit=1)

        if pos_order_id:
            if pos_order_id.account_move:
                pos_order_id.write({'l10n_latam_document_number': pos_order_id.account_move.l10n_latam_document_number})

    class DGIIController(http.Controller):
        @http.route('/dgii/get_contribuyentes', type='json', auth='user', methods=['POST'])
        def get_contribuyentes(self, vat):
            if not vat:
                return {'error': 'VAT is missing'}

            result = request.env['res.partner'].sudo().get_contribuyentes(vat)
            return result

    class PosOrderController(http.Controller):
        @http.route('/pos/my_orders', type='json', auth='user')
        def get_pos_orders(self):
            # Busca todos los pedidos POS para la sesión POS activa y en estado 'draft'
            pos_session = request.env['pos.session'].search([('state', '=', 'opened'), ('user_id', '=', request.uid)],
                                                            limit=1)
            if pos_session:
                orders = request.env['pos.order'].search([
                    ('session_id', '=', pos_session.id),
                    ('state', '=', 'draft')
                ])
                orders_data = [{
                    'id': order.id,
                    'name': order.name,
                    'total': order.amount_total
                } for order in orders]
                return {'orders': orders_data}
            else:
                return {'error': 'No active POS session found'}

    @http.route('/check_invoices', type='json', auth='user')
    def check_invoices(self, partner_id=None, **kwargs):
        if partner_id:
            invoices = request.env['account.move'].sudo().search(
                [('partner_id', '=', partner_id), ('state', '=', 'posted')])
            return {'has_invoices': bool(invoices)}
        return {'has_invoices': False}
