import json
import re
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    manual_currency_rate = fields.Float(string="Currency Rate")
    is_currency_manual = fields.Boolean(string="is_currency_manual", )
    total_descontado = fields.Monetary(string="Total Descontado", compute='calculo_total_descontado')
    total_without_discount = fields.Float(string='Total_without_discount')
    received_delivered = fields.Boolean(string="received/delivered", compute='get_received_delivered')
    label_report_one = fields.Char(string='Label_report_one', compute='get_received_delivered')
    label_report_two = fields.Char(string='Label_report_two', compute='get_received_delivered')
    fiscal_type_name = fields.Char(string='Name_fiscal_type', compute='call_name_type_fiscal')

    def call_name_type_fiscal(self):
        for rec in self:
            rec.fiscal_type_name = rec.l10n_latam_document_type_id.id

    def get_invoice_payment_widget(self, invoice_id):
        j = json.loads(invoice_id.invoice_payments_widget)
        return j['content'] if j else []

    def convert_to_fiscal_invoice(self):
        for invoice in self:
            payments = []
            if invoice.journal_id.l10n_latam_use_documents:
                raise ValidationError(
                    "This invoice is associated with a fiscal journal %s you cannot convert it to fiscal again." % invoice.journal_id.name)
            else:
                if invoice.get_invoice_payment_widget(invoice):
                    for payment in invoice.get_invoice_payment_widget(invoice):
                        payments.append(payment['payment_id'])
                        print(payment)
                    invoice.button_cancel()
                    new_invoice = invoice.copy()
                    new_invoice.invoice_date = invoice.invoice_date
                    new_invoice.journal_id = invoice.company_id.fiscal_journal_sale
                    new_invoice.action_post()
                    action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
                    action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
                    action['res_id'] = new_invoice.id
                else:
                    invoice.button_cancel()
                    new_invoice = invoice.copy()
                    new_invoice.invoice_date = invoice.invoice_date
                    new_invoice.journal_id = invoice.company_id.fiscal_journal_sale
                    new_invoice.action_post()
                    action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
                    action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
                    action['res_id'] = new_invoice.id
                return action

    def calculo_total_descontado(self):
        total = 0
        total_imponible = 0
        self.total_descontado = 0.00
        params = self.env['ir.config_parameter'].sudo().search(
            [('key', '=', 'l10n_dominicana.view_discount_in_account')])
        if params:
            for invoice in self:
                for i in invoice.invoice_line_ids:
                    total = i.quantity * i.price_unit
                    to_discount = total * i.discount
                    res = to_discount / 100.0
                    invoice.total_descontado += res
                    total_imponible += i.quantity * i.price_unit
                invoice.total_without_discount = total_imponible
        else:
            self.total_descontado = 0.00

    # def action_post(self):
    # result = super(AccountMove, self).action_post()
    # control = self.env['ir.config_parameter'].sudo().get_param('l10n_dominicana.with_localization_control')
    # if control != 'False':
    #     limit_date = self.env['ir.config_parameter'].sudo().get_param(
    #         'l10n_dominicana.expiration_date_localization')
    #     for rec in self:
    #         latam_use = rec.journal_id.l10n_latam_use_documents
    #         if latam_use:
    #             actual_date = fields.Date.today()
    #             expiration_date = datetime.strptime(limit_date, '%Y-%m-%d').date()
    #             if actual_date > expiration_date:
    #                 raise ValidationError(
    #                     _(
    #                         "Please Contact the Administrator, "
    #                         "The Dominican Localization Plan is Expired"
    #                     )
    #                 )
    # if self.partner_id:
    #     invoice_totals = json.loads(self.tax_totals_json)
    #     if invoice_totals['amount_total'] == 0.0:
    #         raise ValidationError(
    #             "Para confirmar la factura debe ser mayor que %s" % invoice_totals['amount_total'])
    # return result

    def get_received_delivered(self):
        self.received_delivered = False
        self.label_report_one = ''
        self.label_report_two = ''
        params = self.env['ir.config_parameter'].sudo().search(
            [('key', '=', 'l10n_do_accounting.view_delivered_received')])
        params_label_one = self.env['ir.config_parameter'].sudo().search(
            [('key', '=', 'l10n_do_accounting.label_one_report')])
        params_label_two = self.env['ir.config_parameter'].sudo().search(
            [('key', '=', 'l10n_do_accounting.label_one_report_2')])
        if params:
            self.received_delivered = True
            self.label_report_one = params_label_one.value
            self.label_report_two = params_label_two.value

    # def _get_sequence_format_param(self, previous):
    #
    #     if not self._context.get("is_l10n_do_seq", False):
    #         return super(AccountMove, self)._get_sequence_format_param(previous)
    #
    #     regex = self._l10n_do_sequence_fixed_regex
    #
    #     format_values = re.match(regex, previous).groupdict()
    #     format_values["seq_length"] = len(format_values["seq"])
    #     format_values["seq"] = int(format_values.get("seq") or 0)
    #     if self.l10n_do_fiscal_number:
    #         format_fiscal_number = re.match(regex, self.l10n_do_fiscal_number).groupdict()
    #         if self.l10n_latam_document_type_id.doc_code_prefix != format_fiscal_number["prefix1"]:
    #             raise ValidationError(_("You can't change the document type, please verify your selections"))
    #
    #     placeholders = re.findall(r"(prefix\d|seq\d?)", regex)
    #     format = "".join(
    #         "{seq:0{seq_length}d}" if s == "seq" else "{%s}" % s for s in placeholders
    #     )
    #     return format, format_values
    #
    # def _set_next_sequence(self):
    #     self.ensure_one()
    #
    #     if not self._context.get("is_l10n_do_seq", False):
    #         return super(AccountMove, self)._set_next_sequence()
    #
    #     last_sequence = self._get_last_sequence()
    #     new = not last_sequence
    #     if new:
    #         last_sequence = (
    #                 self._get_last_sequence(relaxed=True) or self._get_starting_sequence()
    #         )
    #
    #     format, format_values = self._get_sequence_format_param(last_sequence)
    #     if new:
    #         format_values["seq"] = 0
    #     format_values["seq"] = format_values["seq"] + 1
    #
    #     if self.company_id.l10n_do_fiscal_sequence_control:
    #         if self.state != "draft" and not self[self._l10n_do_sequence_field]:
    #             for inv in self:
    #                 new_seq = format_values["seq"]
    #                 doc_type = self.env['account.fiscal.sequence'].search(
    #                     [('document_type', '=', inv.l10n_latam_document_type_id.id)])
    #
    #             limit_set = int(doc_type.l10n_do_limit_vouchers)
    #             warning_seq = int(doc_type.l10n_do_warning_vouchers)
    #             if new_seq == warning_seq:
    #                 inv.notification_warning_seq()
    #             elif new_seq > limit_set:
    #                 raise ValidationError(
    #                     _("Fiscal invoices sequence is not available, please contact the Administrator"))
    #
    #     if (
    #             self.env.context.get("prefetch_seq")
    #             or self.state != "draft"
    #             and not self[self._l10n_do_sequence_field]
    #     ):
    #         self[
    #             self._l10n_do_sequence_field
    #         ] = self.l10n_latam_document_type_id._format_document_number(
    #             format.format(**format_values)
    #         )
    #     self._compute_split_sequence()
    #
    # @api.onchange("l10n_latam_document_type_id", "l10n_latam_document_number")
    # def _inverse_l10n_latam_document_number(self):
    #     for con in self:
    #         if con.move_type != 'entry':
    #             con.ref = con.l10n_latam_document_number
    #     for rec in self.filtered("l10n_latam_document_type_id"):
    #         if not rec.l10n_latam_document_number:
    #             rec.l10n_do_fiscal_number = ""
    #         else:
    #             document_type_id = rec.l10n_latam_document_type_id
    #             if self.fiscal_type_name == str(document_type_id.id) or self.name == "/":
    #                 if document_type_id.l10n_do_ncf_type:
    #                     document_number = document_type_id._format_document_number(
    #                         rec.l10n_latam_document_number
    #                     )
    #                 else:
    #                     document_number = rec.l10n_latam_document_number
    #
    #                 if rec.l10n_latam_document_number != document_number:
    #                     rec.l10n_latam_document_number = document_number
    #                 rec.l10n_do_fiscal_number = document_number
    #             else:
    #                 self.l10n_latam_document_number = ""
    #             self.fiscal_type_name = self.l10n_latam_document_type_id.id
    #         super(
    #             AccountMove, self.filtered(lambda m: m.country_code != "DO")
    #         )._inverse_l10n_latam_document_number()
