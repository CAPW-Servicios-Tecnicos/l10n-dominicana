from odoo import fields, models
# from wsmovildgii import get_contribuyentes


class ResCompany(models.Model):
    _inherit = "res.company"

    financial_currency = fields.Boolean(string='Financial Currency')
    manual_change_currency = fields.Boolean(string='Manual Change Currency')
    date_equal_to_invoice_retention = fields.Boolean(string='Date Retention Equal to Date Invoice')
    l10n_do_fiscal_sequence_control = fields.Boolean(string='Activate Fiscal Sequence Control', readonly=False)
    fiscal_journal_sale = fields.Many2one(comodel_name='account.journal',
                                          domain=([('type', '=', 'sale'), ('l10n_latam_use_documents', '=', True)]),
                                          readonly=False,
                                          string='Fiscal_journal_sale')
