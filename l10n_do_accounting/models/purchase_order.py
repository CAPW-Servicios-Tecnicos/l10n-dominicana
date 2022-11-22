from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order'

    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        self.invoice_ids.l10n_do_expense_type = self.partner_id.l10n_do_expense_type
        return res