# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import datetime
import json
import os
import logging

import odoo

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
