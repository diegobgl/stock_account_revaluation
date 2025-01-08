from odoo import models, fields, api

class GenerateAccountingEntriesWizard(models.TransientModel):
    _name = 'generate.accounting.entries.wizard'
    _description = 'Generar Asientos Contables'

    start_date = fields.Date(string='Fecha Inicio', required=True)
    end_date = fields.Date(string='Fecha Fin', required=True)
    move_type = fields.Selection([
        ('incoming', 'Entrada'),
        ('outgoing', 'Salida'),
        ('internal', 'Interno')
    ], string='Tipo de Movimiento', required=True)
    stock_move_ids = fields.Many2many('stock.move', string='Movimientos de Stock')

    @api.onchange('start_date', 'end_date', 'move_type')
    def _onchange_stock_moves(self):
        domain = [
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('picking_type_id.code', '=', self.move_type),
            ('missing_accounting_entries', '=', True),
            ('state', '=', 'done')
        ]
        self.stock_move_ids = self.env['stock.move'].search(domain)

    def generate_accounting_entries(self):
        for move in self.stock_move_ids:
            move._create_accounting_entries()
        return {'type': 'ir.actions.act_window_close'}
