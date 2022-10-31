from odoo import fields, models, api


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    _description = 'Description'

    converted = fields.Float(readonly=False, store=True, digits=(2, 2))

    @api.onchange("converted")
    def _get_converted(self):
        for con in self:
            if con.converted > 0:
                con.rate = 1 / con.converted

    @api.onchange("rate")
    def _get_rate(self):
        for val in self:
            if val.rate > 0:
                val.converted = 1 / val.rate

    # def name_get(self):
    #     result = []
    #     for rate in self:
    #         result.append(
    #             (rate.id, "{} | Tasa: {}".format(rate.name, rate.converted)))
    #     return result
