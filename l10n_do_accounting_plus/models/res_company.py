from odoo import fields, models
# from wsmovildgii import get_contribuyentes


class ResCompany(models.Model):
    _inherit = "res.company"

    financial_currency = fields.Boolean(string='Financial Currency')
    manual_change_currency = fields.Boolean(string='Manual Change Currency')
    date_equal_to_invoice_retention = fields.Boolean(string='Date Retention Equal to Date Invoice')
    l10n_do_fiscal_sequence_control = fields.Boolean(string='Activate Fiscal Sequence Control')
    fiscal_journal_sale = fields.Many2one('account.journal', string='Fiscal_journal_sale')
