{
    "name": "Fiscal Accounting (Rep. Dominicana) Plus",
    "summary": """
        Este módulo implementa una extencion de nuevas opciones para la localizacion dominicana.""",
    "author": "CAPW Servicios Tecnicos",
    "category": "Localization",
    "website": "https://capw.com.do",
    "version": "15.0.3",
    # any module necessary for this one to work correctly
    "depends": ["l10n_do_accounting"],
    # always loaded
    "data": [
        "views/account_fiscal_sequence.xml",
        "views/account_journal_views.xml",
        "views/account_move_views.xml",
        "views/account_payment.xml",
        # "views/res_company_views.xml",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}