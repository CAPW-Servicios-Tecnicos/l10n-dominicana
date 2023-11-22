from odoo import fields, models, api


class PosSession(models.Model):
    _inherit = "pos.session"

    def action_pos_session_close(self, balancing_account, amount_to_balance, bank_payment_method_diffs):
        self.config_id._check_company_journal()
        return super(PosSession, self).action_pos_session_close(balancing_account, amount_to_balance,
                                                                bank_payment_method_diffs)
