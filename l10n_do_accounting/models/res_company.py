from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_do_dgii_start_date = fields.Date("Activities Start Date")
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

    l10n_do_fiscal_numbering = fields.Boolean(
        "Numeración fiscal dominicana",
        compute="_compute_l10n_do_fiscal_numbering",
        store=True,
        readonly=False,
        precompute=True,
        help="Usa el cálculo de numeración de la localización dominicana (NCF/e-CF) "
        "para las facturas de esta compañía. Se activa solo en compañías de "
        "República Dominicana; las demás usan la numeración estándar de Odoo.",
    )

    @api.depends("country_id")
    def _compute_l10n_do_fiscal_numbering(self):
        for company in self:
            company.l10n_do_fiscal_numbering = company.country_id.code == "DO"

    def _localization_use_documents(self):
        """Dominican localization uses documents"""
        self.ensure_one()
        return (
            True
            if self.country_id == self.env.ref("base.do")
            else super()._localization_use_documents()
        )
