from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError

from itertools import groupby
import re


class AccountMove(models.Model):
    _inherit = "account.move"

    # ==== Fields to set the sequence, on the first invoice of the journal ====

    # l10n_latam_document_number = fields.Char(
    #     compute='_compute_l10n_latam_document_number', inverse='_inverse_l10n_latam_document_number',
    #     string='Document Number', readonly=True, states={'draft': [('readonly', False)]})

    invoice_sequence_number_next = fields.Char(string='Next Number',
                                               compute='_compute_invoice_sequence_number_next',
                                               inverse='_inverse_invoice_sequence_number_next')
    invoice_sequence_number_next_prefix = fields.Char(string='Next Number Prefix',
                                                      compute="_compute_invoice_sequence_number_next")

    manual_currency_rate = fields.Float(string="Currency Rate")
    is_currency_manual = fields.Boolean(string="is_currency_manual")

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------

    @api.onchange('currency_id')
    def compute_manual_currency_rate(self):
        currency_company = self.company_id.currency_id
        currency_id = self.currency_id
        manual_currency_active = self.company_id.manual_change_currency
        if manual_currency_active and currency_company != currency_id:
            self.is_currency_manual = False
        else:
            self.is_currency_manual = True

    # -------------------------------------------------------------------------
    # BUSINESS METHODS
    # -------------------------------------------------------------------------

    def _get_document_type_sequence(self):
        """ Return the match sequences for the given journal and invoice """
        self.ensure_one()
        if (
                self.journal_id.l10n_latam_use_documents
                and self.l10n_latam_country_code == "DO"
        ):
            res = self.journal_id.l10n_do_sequence_ids.filtered(
                lambda x: x.l10n_latam_document_type_id
                          == self.l10n_latam_document_type_id
            )
            if (
                    not res
                    and self.move_type == "in_refund"
                    and self.is_l10n_do_internal_sequence
            ):
                journal = self.with_context(
                    default_move_type="out_invoice"
                )._get_default_journal()
                res = journal and journal.l10n_do_sequence_ids.filtered(
                    lambda x: x.l10n_latam_document_type_id
                              == self.l10n_latam_document_type_id
                )
            return res
        return super()._get_document_type_sequence()

    @api.depends('state', 'journal_id', 'date', 'invoice_date')
    def _compute_invoice_sequence_number_next(self):
        """ computes the prefix of the number that will be assigned to the first invoice/bill/refund of a journal, in order to
        let the user manually change it.
        """
        # Check user group.
        system_user = self.env.is_system()
        if not system_user:
            self.invoice_sequence_number_next_prefix = False
            self.invoice_sequence_number_next = False
            return

        # Check moves being candidates to set a custom number next.
        moves = self.filtered(lambda move: move.is_invoice() and move.name == '/')
        if not moves:
            self.invoice_sequence_number_next_prefix = False
            self.invoice_sequence_number_next = False
            return

        treated = self.browse()
        for key, group in groupby(moves, key=lambda move: (move.journal_id, move._get_sequence())):
            journal, sequence = key
            domain = [('journal_id', '=', journal.id), ('state', '=', 'posted')]
            if self.ids:
                domain.append(('id', 'not in', self.ids))
            if journal.type == 'sale':
                domain.append(('type', 'in', ('out_invoice', 'out_refund')))
            elif journal.type == 'purchase':
                domain.append(('type', 'in', ('in_invoice', 'in_refund')))
            else:
                continue
            if self.search_count(domain):
                continue

            for move in group:
                sequence_date = move.date or move.invoice_date
                prefix, dummy = sequence._get_prefix_suffix(date=sequence_date, date_range=sequence_date)
                number_next = sequence._get_current_sequence(sequence_date=sequence_date).number_next_actual
                move.invoice_sequence_number_next_prefix = prefix
                move.invoice_sequence_number_next = '%%0%sd' % sequence.padding % number_next
                treated |= move
        remaining = (self - treated)
        remaining.invoice_sequence_number_next_prefix = False
        remaining.invoice_sequence_number_next = False

    def _inverse_invoice_sequence_number_next(self):
        ''' Set the number_next on the sequence related to the invoice/bill/refund'''
        # Check user group.
        if not self.env.is_admin():
            return

        # Set the next number in the sequence.
        for move in self:
            if not move.invoice_sequence_number_next:
                continue
            sequence = move._get_sequence()
            nxt = re.sub("[^0-9]", '', move.invoice_sequence_number_next)
            result = re.match("(0*)([0-9]+)", nxt)
            if result and sequence:
                sequence_date = move.date or move.invoice_date
                date_sequence = sequence._get_current_sequence(sequence_date=sequence_date)
                date_sequence.number_next_actual = int(result.group(2))

    def _get_sequence(self):
        ''' Return the sequence to be used during the post of the current move.
        :return: An ir.sequence record or False.
        '''
        self.ensure_one()

        journal = self.journal_id
        if self.move_type in (
                'entry', 'out_invoice', 'in_invoice', 'out_receipt', 'in_receipt') or not journal.refund_sequence:
            return journal.sequence_id
        if not journal.refund_sequence_id:
            return
        return journal.refund_sequence_id

    def _post(self, soft=True):
        res = super()._post(soft)
        for move in self:
            if move.name == '/':
                # Get the journal's sequence.
                sequence = move._get_sequence()
                if not sequence:
                    raise UserError(_('Please define a sequence on your journal.'))

                # Consume a new number.
                to_write['name'] = sequence.with_context(ir_sequence_date=move.date).next_by_id()
