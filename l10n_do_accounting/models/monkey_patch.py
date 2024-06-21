from odoo import models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "posted_before", "state", "journal_id", "date", "move_type", "payment_id"
    )
    def _compute_name(self):
<<<<<<< HEAD
        self = self.sorted(lambda m: (m.date, m.ref or "", m.id))
=======
        self = self.sorted(lambda m: (m.date, m.ref or "", m._origin.id))
>>>>>>> 94bec61b7b67a86cb93f2d74afcef9e29110c0ed

        for move in self:
            if move.state == "cancel":
                continue

            move_has_name = move.name and move.name != "/"
            if move_has_name or move.state != "posted":
                if not move.posted_before and not move._sequence_matches_date():
<<<<<<< HEAD
                    if move._get_last_sequence(lock=False):
=======
                    if move._get_last_sequence():
>>>>>>> 94bec61b7b67a86cb93f2d74afcef9e29110c0ed
                        move.name = False
                        continue
                else:
                    if (
                        move_has_name
                        and move.posted_before
                        or not move_has_name
<<<<<<< HEAD
                        and move._get_last_sequence(lock=False)
=======
                        and move._get_last_sequence()
>>>>>>> 94bec61b7b67a86cb93f2d74afcef9e29110c0ed
                    ):
                        continue
            if move.date and (not move_has_name or not move._sequence_matches_date()):
                move._set_next_sequence()

        self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = "/"
        self._inverse_name()

        for move in self.filtered(
            lambda x: x.country_code == "DO"
            and x.l10n_latam_document_type_id
            and not x.l10n_latam_manual_document_number
            and not x.l10n_do_enable_first_sequence
            and x.state == "posted"
            and not x.l10n_do_fiscal_number
        ):
            move.with_context(is_l10n_do_seq=True)._set_next_sequence()
