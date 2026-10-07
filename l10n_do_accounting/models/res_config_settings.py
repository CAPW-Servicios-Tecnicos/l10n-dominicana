from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_do_require_buyer_vat = fields.Boolean(
        related="company_id.l10n_do_require_buyer_vat", readonly=False)
    l10n_do_consumer_vat_threshold = fields.Float(
        related="company_id.l10n_do_consumer_vat_threshold", readonly=False)
