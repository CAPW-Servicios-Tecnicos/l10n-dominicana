{
    "name": "Fiscal Accounting (Rep. Dominicana) Plus",
    "summary": """
        Este módulo implementa una extencion de nuevas opciones para la localizacion dominicana.""",
    "author": "CAPW Servicios Tecnicos",
    "category": "Localization",
    "website": "https://capw.com.do",
    "version": "15.0.1",
    # any module necessary for this one to work correctly
    "depends": ["l10n_latam_invoice_document", "l10n_do"],
    # always loaded
    "data": [
        "views/account_payment.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}