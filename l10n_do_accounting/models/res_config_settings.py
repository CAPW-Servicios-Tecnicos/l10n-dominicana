from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    financial_currency = fields.Boolean(
        string='Financial Currency',
        related='company_id.financial_currency',
        readonly=False,)

    manual_change_currency = fields.Boolean(
        string='Manual Change Currency',
        related='company_id.manual_change_currency',
        readonly=False,)
