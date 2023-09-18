from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    financial_currency = fields.Boolean(
        string='Financial Currency', )

    manual_change_currency = fields.Boolean(
        string='Manual Change Currency', )

    date_equal_to_invoice_retention = fields.Boolean(
        string='Date Retention Equal to Date Invoice',
        readonly=False, )

    l10n_do_fiscal_sequence_control = fields.Boolean(
        string='Activate Fiscal Sequence Control',
        readonly=False, )
