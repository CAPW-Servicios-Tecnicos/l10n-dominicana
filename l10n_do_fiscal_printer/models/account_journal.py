from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    fiscal_printer_payment_type = fields.Selection([(u'cash', u'Efectivo'),
                                                    (u'Check', u'Cheque'),
                                                    (u'credit_card', u'Tarjeta de crédito'),
                                                    (u'debit_card', u'Tarjeta de debito'),
                                                    (u'card', u'Tarjeta'),
                                                    (u'coupon', u'Cupón'),
                                                    (u'other', u'Otros'),
                                                    (u'credit_note', u'Nota de crédito')],
                                                   string=u'Formas de pago impresora fiscal', required=False,
                                                   default="other",
                                                   help=u"Esta configuracion se encuantra internamente en la "
                                                        u"impresora fiscal y debe de especificar esta opecion. "
                                                        u"Esta es la forma en que la impresora fiscal registra el "
                                                        u"pago en los libros.")
