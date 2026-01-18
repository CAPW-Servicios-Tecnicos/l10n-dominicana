from odoo import fields, models


class ResConfigSettings(models.Model):
    _inherit = "res.config.settings"

    module_l10n_do_partner_autocomplete = fields.Boolean(
        string='    module_l10n_do_partner_autocomplete', 
        required=False)