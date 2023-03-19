{
    "name": "Fiscal POS (Rep. Dominicana)",
    "summary": """Incorpora funcionalidades de facturación con NCF al POS.""",
    "author": "Easicoders",
    "license": "LGPL-3",
    "website": "https://github.com/odoo-dominicana",
    "category": "Localization",
    "version": "15.0.1.1.2",
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
            'l10n_do_pos/static/src/js/screens.js',
            'l10n_do_pos/static/src/js/Popup.js',
            'l10n_do_pos/static/src/css/pos.css',

        ],
        'web.assets_qweb': [
            ('replace', 'point_of_sale/static/src/xml/Screens/ProductScreen/ActionpadWidget.xml', 'l10n_do_pos/static/src/xml/pos.xml'),
            ('replace', 'point_of_sale/static/src/xml/Screens/PaymentScreen/PaymentScreen.xml', 'l10n_do_pos/static/src/xml/PaymentScreen.xml'),
            'l10n_do_pos/static/src/xml/posticket.xml',
        ],
    },
    "installable": True,
}
