from odoo import models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "posted_before", "state", "journal_id", "date", "move_type", "origin_payment_id"
    )
    def _compute_name(self):
        # Solo las compañías con numeración fiscal dominicana usan este cálculo;
        # el resto (España, México, ...) conserva el comportamiento estándar de
        # Odoo, que no asigna número a los borradores.
        do_moves = self.filtered(lambda m: m.company_id.l10n_do_fiscal_numbering)
        other_moves = self - do_moves
        if other_moves:
            super(AccountMove, other_moves)._compute_name()

        # Bypass para IDs temporales (NewId) - No pueden generar secuencias fiscales
        # ya que los métodos SQL posteriores requieren IDs enteros reales
        self = do_moves.filtered(
            lambda m: isinstance(m.id, int)
        ).sorted(
            lambda m: (m.date, m.ref or "", m._origin.id))

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
            lambda x: x.country_code == "DO"
            and x.l10n_latam_document_type_id
            and not x.l10n_latam_manual_document_number
            and not x.l10n_do_enable_first_sequence
            and x.state == "posted"
            and not x.l10n_do_fiscal_number
        ):
            move.with_context(is_l10n_do_seq=True)._set_next_sequence()
