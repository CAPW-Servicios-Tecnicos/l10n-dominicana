from odoo import fields, models, api


class MonthlySalesBook(models.Model):
    _name = 'monthly.sales.book'
    _order = 'date'
    _description = 'Description'

    name = fields.Char("file name", readonly=True)

    id_line = fields.Integer("ID Línea")
    hash_book = fields.Binary(string="HASH",  help=""" Se usará el algoritmo SHA-1.
    Para generar el HASH se tomaran en cuenta todas las líneas del archivo, incluyendo los HASH
    de los libros diarios.""")
    doc_qty = fields.Integer("Número de Registros Archivo")

    total_sales = fields.Float("Total", digits=(14, 2))
    total_tax = fields.Float("Total Itbis", digits=(14, 2))
    total_tax1 = fields.Float("Monto Total ITBIS Tasa 1 Archivo", digits=(14, 2))
    total_tax2 = fields.Float("Monto Total ITBIS Tasa 2 Archivo", digits=(14, 2))
    total_tax3 = fields.Float("Monto Total ITBIS Tasa 3 Archivo", digits=(14, 2))
    total_tax4 = fields.Float("Monto Total ITBIS Tasa 4 Archivo", digits=(14, 2))
    total_tax5 = fields.Float("Monto Total ITBIS Tasa 5 Archivo", digits=(14, 2))
    total_sales_cof = fields.Float("Monto Total Venta Consumidor Final Archivo", digits=(14, 2))
    total_tax_cof = fields.Float("Monto Total ITBIS Consumidor Final Archivo", digits=(14, 2))
    total_sales_crf = fields.Float("Monto Total Venta Credito Fiscal Archivo", digits=(14, 2))
    total_tax_crf = fields.Float("Monto Total ITBIS Credito Fiscal Archivo", digits=(14, 2))
    total_sales_ncof = fields.Float("Monto Total Nota de Credito Consumidor Final Archivo", digits=(14, 2))
    total_tax_ncof = fields.Float("Monto Total ITBIS  Nota de Credito Consumidor Final Archivo", digits=(14, 2))
    total_sales_ncrf = fields.Float("Monto Total Nota de Credito Credito Fiscal Archivo", digits=(14, 2))
    total_tax_ncrf = fields.Float("Monto Total ITBIS Nota de Credito Credito Fiscal Archivo", digits=(14, 2))


class DailySalesBook(models.Model):
    _name = 'daily.sales.book'
    _order = 'date'
    _description = 'Description'

    name = fields.Char("file name", readonly=True)

    id_line = fields.Integer("ID Línea")
    printer_id = fields.Many2one("fiscal.printer.config", string="Printer", readonly=True)
    hash_book = fields.Binary(string="HASH",  help=""" Se usará el algoritmo SHA-1.
    Para generar el HASH se tomaran en cuenta todas las líneas del archivo, incluyendo los HASH
    de los libros diarios.""")
    doc_qty = fields.Integer("Número de Registros Archivo")

    total_sales = fields.Float("Total", digits=(14, 2))
    total_tax = fields.Float("Total Itbis", digits=(14, 2))
    total_tax1 = fields.Float("Monto Total ITBIS Tasa 1 Archivo", digits=(14, 2))
    total_tax2 = fields.Float("Monto Total ITBIS Tasa 2 Archivo", digits=(14, 2))
    total_tax3 = fields.Float("Monto Total ITBIS Tasa 3 Archivo", digits=(14, 2))
    total_tax4 = fields.Float("Monto Total ITBIS Tasa 4 Archivo", digits=(14, 2))
    total_tax5 = fields.Float("Monto Total ITBIS Tasa 5 Archivo", digits=(14, 2))
    total_sales_cof = fields.Float("Monto Total Venta Consumidor Final Archivo", digits=(14, 2))
    total_tax_cof = fields.Float("Monto Total ITBIS Consumidor Final Archivo", digits=(14, 2))
    total_sales_crf = fields.Float("Monto Total Venta Credito Fiscal Archivo", digits=(14, 2))
    total_tax_crf = fields.Float("Monto Total ITBIS Credito Fiscal Archivo", digits=(14, 2))
    total_sales_ncof = fields.Float("Monto Total Nota de Credito Consumidor Final Archivo", digits=(14, 2))
    total_tax_ncof = fields.Float("Monto Total ITBIS  Nota de Credito Consumidor Final Archivo", digits=(14, 2))
    total_sales_ncrf = fields.Float("Monto Total Nota de Credito Credito Fiscal Archivo", digits=(14, 2))
    total_tax_ncrf = fields.Float("Monto Total ITBIS Nota de Credito Credito Fiscal Archivo", digits=(14, 2))
