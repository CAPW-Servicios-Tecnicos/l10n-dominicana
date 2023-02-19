{
    "name": "Fiscal POS (Rep. Dominicana)",
    "summary": """Incorpora funcionalidades de facturación con NCF al POS.""",
    "author": "Xmarts, " "Indexa, " "Iterativo SRL, " "CAPW Servicios Tecnicos",
    "license": "LGPL-3",
    "website": "https://github.com/odoo-dominicana",
    "category": "Localization",
    "version": "15.0.0.0.1",
    "depends": [
        "point_of_sale",
        "l10n_do_accounting",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/pos_config_views.xml",
        "views/pos_order_views.xml",
    ],
    'assets': {
        'point_of_sale.assets': [
            'l10n_do_pos/static/src/js/models.js',
            # 'l10n_do_pos/static/src/js/PaymentScreen.js',
            'l10n_do_pos/static/src/css/pos.css',
        ],
        'web.assets_qweb': [
            'l10n_do_pos/static/src/xml/**/*',
        ],
    },
    'installable': True,
}
