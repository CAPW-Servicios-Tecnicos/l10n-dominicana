{
    "name": "Fiscal Accounting (Rep. Dominicana) Plus",
    "summary": """
        Este módulo implementa una extencion de nuevas opciones para la localizacion dominicana.""",
    "author": "CAPW Servicios Tecnicos",
    "category": "Localization",
    "license": "LGPL-3",
    "website": "https://capw.com.do",
    "version": "15.0.4",
    # any module necessary for this one to work correctly
    "depends": ["l10n_do_accounting"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/account_fiscal_sequence.xml",
        "views/account_journal_views.xml",
        "views/account_move_views.xml",
        "views/account_payment.xml",
        "views/report_invoice.xml",
        "views/res_config_settings_view.xml",
        "views/res_partner.xml",
        # "views/res_company_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
