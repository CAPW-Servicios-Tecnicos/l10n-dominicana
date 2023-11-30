from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = ['account.payment']

    manual_currency_rate = fields.Float(string="Currency Rate",)
    is_currency_manual = fields.Boolean(string="is_currency_manual",)

    # @api.onchange('currency_id')
    # def compute_manual_currency_rate(self):
    #     currency_company = self.company_id.currency_id
    #     currency_id = self.currency_id
    #     financial_currency = self.company_id.financial_currency
    #     if financial_currency and currency_company != currency_id:
    #         self.is_currency_manual = False
    #     else:
    #         self.is_currency_manual = True
