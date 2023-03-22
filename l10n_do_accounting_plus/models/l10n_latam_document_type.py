from odoo import models, _


class L10nLatamDocumentType(models.Model):
    _inherit = "l10n_latam.document.type"

    def _get_document_sequence_vals(self, journal):
        """ Values to create the sequences """
        # values = self._get_document_sequence_vals(journal)
        values = self.env['ir.sequence']
        # if self.country_id != self.env.ref("base.do"):
        #     return values
        values.create(
            {
                "name": '%s - %s' % (journal.name, self.name),
                "padding": 10 if str(self.l10n_do_ncf_type).startswith("e-") else 8,
                "implementation": "no_gap",
                "prefix": self.doc_code_prefix,
                "l10n_latam_document_type_id": self.id,
                "l10n_latam_journal_id": journal.id,
            }
        )
        return values
