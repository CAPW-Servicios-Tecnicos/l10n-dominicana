from odoo import fields, models, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    hidden_payment_form = fields.Boolean(
        string='Payment Form With Method Lines',
        required=False)


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method.line'

    def _get_l10n_do_payment_form(self):
        """ Return the list of payment forms allowed by DGII. """
        return [
            ("cash", _("Cash")),
            ("bank", _("Check / Transfer")),
            ("card", _("Credit Card")),
            ("credit", _("Credit")),
            ("swap", _("Swap")),
            ("bond", _("Bonds or Gift Certificate")),
            ("others", _("Other Sale Type")),
        ]

    l10n_do_payment_form = fields.Selection(
        string='Payment Form',
        selection='_get_l10n_do_payment_form',
        required=False, )


class AccountFiscalSequence(models.Model):
    _name = 'account.fiscal.sequence'
    _description = "Account Fiscal Sequence"

    l10n_do_warning_vouchers = fields.Char(
        string='Warning Sequence',
        required=False)

    l10n_do_limit_vouchers = fields.Char(
        string='Limit Sequence',
        required=False)

    document_type = fields.Many2one(
        comodel_name='l10n_latam.document.type',
        string='Document Type',
        required=False)

    code = fields.Char(related='document_type.doc_code_prefix')

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)

    _sql_constraints = [
        ('document_type', 'unique (code, company_id)',
         'You only can use one document type per company')
    ]