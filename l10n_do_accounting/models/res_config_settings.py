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

    date_equal_to_invoice_retention = fields.Boolean(
        string='Date Retention Equal to Date Invoice',
        related='company_id.date_equal_to_invoice_retention',
        readonly=False, )

    view_discount_in_account = fields.Boolean(
        string='Visualizar descuentos',
        config_parameter='l10n_dominicana.view_discount_in_account',
        required=False)
    
    view_delivered_received = fields.Boolean(
        string='Delivered/Received',
        config_parameter='l10n_do_accounting.view_delivered_received',
        required=False)
    
    label_one_report = fields.Char(
        string='Show name in report label left',
        config_parameter='l10n_do_accounting.label_one_report',
        required=False)

    label_one_report_2 = fields.Char(
        string='Show name in report label right',
        config_parameter='l10n_do_accounting.label_one_report_2',
        required=False)
