from odoo import models, fields, api, _
from .wsmovildgii import get_contribuyentes


class Partner(models.Model):
    _inherit = "res.partner"

    @api.onchange('vat')
    def get_contribuyentes(self):
        get_contribuyentes(self)
        return get_contribuyentes(self)
