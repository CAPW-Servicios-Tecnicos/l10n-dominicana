from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_do_dgii_start_date = fields.Date("Activities Start Date")
    l10n_do_ecf_issuer = fields.Boolean(
        "Is e-CF issuer",
        help="When activating this field, NCF issuance is disabled.",
    )
    l10n_do_ecf_deferred_submissions = fields.Boolean(
        "Deferred submissions",
        help="Identify taxpayers who have been previously authorized "
        "to have sales through offline mobile devices such as "
        "sales with Handheld, enter others.",
    )

    l10n_do_require_buyer_vat = fields.Boolean(
        "Require buyer RNC/Cédula",
        default=True,
        help="Al confirmar una factura de venta fiscal, exige el RNC/Cédula del cliente cuando "
             "la DGII lo requiere: comprobantes de crédito fiscal, gubernamental, regímenes "
             "especiales, exportación y notas, y las facturas de consumo desde el umbral. "
             "Evita emitir comprobantes que la DGII rechazaría. Solo afecta facturas que se "
             "confirman de ahora en adelante; no cambia las ya emitidas.",
    )
    l10n_do_consumer_vat_threshold = fields.Float(
        "Consumer invoice threshold (RD$)",
        default=250000.0,
        help="Monto desde el cual una factura de consumo (B02 / e-CF 32) debe identificar al "
             "comprador con su RNC/Cédula. En la B02 se compara el monto sin ITBIS; en el e-CF 32, "
             "el monto total (Formato e-CF de la DGII). Por debajo de este monto el e-CF 32 se "
             "reporta con el resumen de factura de consumo (RFCE). Hoy es RD$250,000; cámbielo "
             "solo si la DGII modifica el umbral.",
    )

    def _localization_use_documents(self):
        """Dominican localization uses documents"""
        self.ensure_one()
        return (
            True
            if self.country_id == self.env.ref("base.do")
            else super()._localization_use_documents()
        )
