{
    'name': 'Fiscal accounting Plus (Rep. Dominicana)',
    'version': '15.0.0.1.1',
    'summary': """Este modulo se implementa para aumentar las opciones de configuraciones de la localizacion,
                Configuracion de secuencias de comprobantes por ir.sequence, conciliacion bancaria sin cuentas puentes (Outstanding)
    """,
    'description': '',
    'category': 'Localization',
    'author': 'CAPW Servicios Tecnicos',
    'website': 'https://capw.com.do',
    'license': 'LGPL-3',
    'depends': ['l10n_do_accounting'],
    'data': ["views/account_move_views.xml",
             "views/account_payment.xml",
             "views/account_journal_views.xml",
             ],
    'installable': True,
    'auto_install': False,
}
