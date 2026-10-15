from datetime import date

from odoo import models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "posted_before", "state", "journal_id", "date", "move_type", "payment_id"
    )
    def _compute_name(self):
        # Igual que el núcleo, pero un asiento sin fecha (p. ej. uno nuevo en un
        # formulario) no puede compararse con los que sí la tienen: lanzaba
        # TypeError. Se ordena al principio; el orden de los demás no cambia.
        self = self.sorted(lambda m: (m.date or date.min, m.ref or "", m._origin.id or 0))

        for move in self:
            if move.state == "cancel":
                continue

            move_has_name = move.name and move.name != "/"
            if move_has_name or move.state != "posted":
                if not move.posted_before and not move._sequence_matches_date():
                    if move._get_last_sequence():
                        move.name = False
                        continue
                else:
                    if (
                        move_has_name
                        and move.posted_before
                        or not move_has_name
                        and move._get_last_sequence()
                    ):
                        continue
            if move.date and (not move_has_name or not move._sequence_matches_date()):
                move._set_next_sequence()

        self.filtered(lambda m: not m.name and not m.quick_edit_mode).name = "/"
        self._inverse_name()

        for move in self.filtered(
                lambda x:
                x.country_code == "DO"
                and x.move_type in (
                        "out_invoice",
                        "out_refund",
                        "in_invoice",
                        "in_refund",
                )
                and x.l10n_latam_use_documents
                and x.l10n_latam_document_type_id
                and not x.l10n_latam_manual_document_number
                and not x.l10n_do_enable_first_sequence
                and x.state == "posted"
                and not x.l10n_do_fiscal_number
        ):
            move.with_context(is_l10n_do_seq=True)._set_next_sequence()
