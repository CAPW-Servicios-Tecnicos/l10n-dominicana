# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    module_l10n_do_partner_autocomplete = fields.Boolean("DGII Partner Autocomplete", config_parameter='l10n_do_partner_autocomplete.dgii_autocomplete')
