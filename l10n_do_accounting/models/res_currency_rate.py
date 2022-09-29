from odoo import fields, models, api


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    _description = 'Description'

    @api.depends("rate")
    def _get_converted(self):
        for rec in self:
            if rec.rate > 0:
                rec.converted = 1 / rec.rate

    converted = fields.Float(compute=_get_converted, readonly=True, digits=(12, 12))

    def name_get(self):
        result = []
        for rate in self:
            result.append(
                (rate.id, "{} | Tasa: {}".format(rate.name, rate.converted)))
        return result

    rate = fields.Float(
        digits=(2, 2),
        help='The rate of the currency to the currency of rate 1')
