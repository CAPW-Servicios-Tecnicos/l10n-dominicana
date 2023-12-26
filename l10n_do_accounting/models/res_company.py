from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_do_dgii_start_date = fields.Date("Activities Start Date")

    l10n_do_default_client = fields.Selection(
        selection=[("non_payer", "Final Consumer"), ("taxpayer", "Fiscal Consumer")],
        default=lambda self: self._context.get("l10n_do_default_client", "non_payer"),
        string="Default Customer",
    )
    l10n_do_ecf_issuer = fields.Boolean(
        "Is e-CF issuer",
        help="When activating this field, NCF issuance is disabled.",
    )
    l10n_do_ecf_deferred_submissions = fields.Boolean(
        "Deferred submissions",
        help="Identify taxpayers who have been previously authorized "
        "to have sales through offline mobile devices such as "
        "sales with Handheld, enter others.",
    )
    financial_currency = fields.Boolean(
        string='Financial Currency',)
    manual_change_currency = fields.Boolean(
        string='Manual Change Currency',)
    fiscal_journal_sale = fields.Many2one('account.journal', string='Fiscal_journal_sale')

    def _localization_use_documents(self):
        """ Dominican localization uses documents """
        self.ensure_one()
        return (
            True
            if self.country_id == self.env.ref("base.do")
            else super()._localization_use_documents()
        )
