from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


class FiscalPrinterConfig(models.Model):
    _name = 'fiscal.printer.config'

    name = fields.Char("Descripcion", required=True)
    host = fields.Char("Host", required=True)
    print_copy = fields.Boolean("Imprimir con copia", default=False)
    subsidiary = fields.Char(string="Sucursal", required=True)
    daily_book_ids = fields.One2many("daily.sales.book", "printer_id", string="Libros Diarios")
    state = fields.Selection([("deactivate", "Desactivada"), ("active", "Activa")], default="deactivate")
