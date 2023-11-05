from odoo import fields, models, _


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
