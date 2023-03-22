from odoo import fields, models, api, _


class AccountJournal(models.Model):
    _inherit = ['account.journal']

    # ==== Business fields ====

    l10n_latam_country_code = fields.Char("Country Code (LATAM)",
                                          related='company_id.country_id.code',
                                          help='Technical field used to hide/show fields regarding the localization')

    l10n_do_sequence_ids = fields.One2many(
        "ir.sequence",
        "l10n_latam_journal_id",
        string="Sequences",
    )

    manage_sequence_internal = fields.Boolean(
        string='Manage Sequence in Ir Sequence',
        required=False)

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # BUSINESS METHODS
    # -------------------------------------------------------------------------

    @api.model
    def create(self, values):
        """ Create Document sequences after create the journal """
        sequence_internal = values['manage_sequence_internal']
        if sequence_internal:
            res2 = super().create(values)
            res2._l10n_do_create_document_sequences()
            return res2
        else:
            res2 = super().create(values)
            return res2

    def write(self, values):
        """ Update Document sequences after update journal """
        to_check = {"type", "l10n_latam_use_documents"}
        res = super().write(values)
        if to_check.intersection(set(values.keys())):
            for rec in self:
                rec.with_context(
                    use_documents=values.get("l10n_latam_use_documents")
                )._l10n_do_create_document_sequences()
        return res

    # def _l10n_do_create_document_sequences(self):
    #     """IF DGII Configuration changes try to review if this can be done
    #     and then create / update the document sequences"""
    #     self.ensure_one()
    #     if self.company_id.country_id != self.env.ref("base.do"):
    #         return True
    #     if not self.l10n_latam_use_documents:
    #         return False
    #
    #     sequences = self.l10n_do_sequence_ids
    #     sequences.unlink()
    #
    #     # Create Sequences
    #     ncf_types = self._get_journal_ncf_types()
    #     internal_types = ["invoice", "in_invoice", "debit_note", "credit_note"]
    #     domain = [
    #         ("country_id.code", "=", "DO"),
    #         ("internal_type", "in", internal_types),
    #         ("active", "=", True),
    #         "|",
    #         ("l10n_do_ncf_type", "=", False),
    #         ("l10n_do_ncf_type", "in", ncf_types),
    #     ]
    #
    #     documents = self.env["l10n_latam.document.type"].search(domain)
    #     for document in documents:
    #         sequences |= (
    #             self.env["ir.sequence"]
    #             .sudo()
    #             .create(document._get_document_sequence_vals(self))
    #         )
    #     return sequences

    def _l10n_do_create_document_sequences(self):
        """IF DGII Configuration changes try to review if this can be done
        and then create / update the document sequences"""
        self.ensure_one()

        if (
                not self.l10n_latam_use_documents
                or self.company_id.country_id != self.env.ref("base.do")
        ):
            return

        sequences = self.l10n_do_sequence_ids
        sequences.unlink()

        document_types = self.l10n_do_document_type_ids
        fiscal_types = self._get_journal_ncf_types()

        if self.type == "purchase":
            fiscal_types = [
                ftype
                for ftype in fiscal_types
                if ftype not in ("fiscal", "credit_note")
            ]

        domain = [
            ("country_id.code", "=", "DO"),
            ("l10n_do_ncf_type", "in", fiscal_types),
        ]

        documents = self.env["l10n_latam.document.type"].search(domain)
        for document in documents:
            sequences |= (
                self.env["ir.sequence"]
                .sudo()
                .create(document._get_document_sequence_vals(self))
            )
        return sequences
