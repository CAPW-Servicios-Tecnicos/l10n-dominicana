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

    view_discount_in_account = fields.Boolean(
        string='Visualizar descuentos',
        config_parameter='l10n_dominicana.view_discount_in_account',
        required=False)
    
    view_delivered_received = fields.Boolean(
        string='Delivered/Received',
        config_parameter='l10n_do_accounting.view_delivered_received',
        required=False)
