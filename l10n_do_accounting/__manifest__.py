{
    "name": "Fiscal Accounting (Rep. Dominicana)",
    "summary": """
        Este módulo implementa la administración y gestión de los números de
         comprobantes fiscales para el cumplimento de la norma 06-18 de la
         Dirección de Impuestos Internos en la República Dominicana.""",
    "author": "iterativo LLC, " "Indexa, " "CAPW Servicios Tecnicos",
    "category": "Localization",
    "website": "https://github.com/odoo-dominicana",
<<<<<<< HEAD
    "version": "15.0.0.10.7",
=======
    "version": "15.0.0.12.0",
>>>>>>> 996e4b32a2c582a1b6cebc1348689df6b0bd0fb5
    # any module necessary for this one to work correctly
    "depends": ["l10n_latam_invoice_document", "l10n_do"],
    # always loaded
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "data/l10n_latam.document.type.csv",
        "data/ir_config_parameter_data.xml",
        "wizard/account_move_reversal_views.xml",
        "wizard/account_move_cancel_views.xml",
        "wizard/account_debit_note_views.xml",
        "views/account_fiscal_sequence.xml",
        "views/res_config_settings_view.xml",
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
        "views/account_dgii_menuitem.xml",
        "views/account_journal_views.xml",
        "views/l10n_latam_document_type_views.xml",
        "views/report_templates.xml",
        "views/report_invoice.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/res_partner_demo.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}