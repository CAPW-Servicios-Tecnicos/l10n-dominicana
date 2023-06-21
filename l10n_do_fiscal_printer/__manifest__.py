{
    'name': 'Modulo de Impresora Fiscal Epson (Rep. Dominicana)',
    'version': '15.0.0.1',
    'summary': 'Summery',
    'description': ''' Este módulo implementa la administración y gestión de los números de
         comprobantes fiscales para el cumplimento de la norma 06-18 de la
         Dirección de Impuestos Internos en la República Dominicana ''',
    'category': 'Localization',
    'author': 'CAPW Servicios Tecnicos',
    'website': 'www.capw.com.do',
    'depends': ['l10n_do'],
    'data': [
        'security/ir.model.access.csv',
        'views/fiscal_printer_config.xml',
        'views/account_move.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_do_fiscal_printer/static/src/js/fiscal_print_invoice.js'
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
