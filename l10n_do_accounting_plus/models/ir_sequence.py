from odoo import models, fields


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    l10n_latam_journal_id = fields.Many2one('account.journal', 'Journal')
    l10n_latam_document_type_id = fields.Many2one('l10n_latam.document.type', 'Document Type')

    l10n_do_expiration_date = fields.Date(
        string="NCF Expiration date",
        default=fields.Date.end_of(
            fields.Date.today().replace(year=fields.Date.today().year + 1), "year"
        ),
    )

    mail_template = fields.Many2one(
        comodel_name='mail.template',
        string='Mail_template',
        required=False)

    l10n_do_warning_ncf = fields.Integer(string="NCF de alerta")
