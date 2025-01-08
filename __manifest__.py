{
    'name': 'Stock Accounting Revaluation',
    'version': '1.0',
    'summary': 'Regenera asientos contables para movimientos de inventario sin valorización',
    'description': "Este módulo permite generar asientos contables para movimientos de inventario que no los generaron debido a cambios en la configuración de valorización automática.",
    'author': 'Tu Nombre',
    'depends': ['stock', 'stock_account'],
    'data': [
        'views/wizard_generate_accounting_entries_views.xml',
        'views/stock_move_action_views.xml',
        'views/stock_picking_menu_views.xml',

    ],
    'installable': True,
    'application': False,
}