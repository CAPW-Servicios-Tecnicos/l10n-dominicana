from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    financial_currency = fields.Boolean(
        string='Financial Currency', )

    manual_change_currency = fields.Boolean(
        string='Manual Change Currency', )
