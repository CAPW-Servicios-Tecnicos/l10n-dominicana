from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = ['account.journal']

    l10n_do_sequence_ids = fields.One2many(
        "ir.sequence",
        "l10n_latam_journal_id",
        string="Sequences",
    )



