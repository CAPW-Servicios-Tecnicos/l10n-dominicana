from odoo import fields, models, api


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    _description = 'Description'

    converted = fields.Float(readonly=False, digits=(2, 2))

    @api.onchange("converted")
    def _get_converted(self):
        if self.converted > 0:
            self.rate = 1 / self.converted
