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
    stock_move_ids = fields.Many2many('stock.move', string='Movimientos de Stock', default=lambda self: self._default_stock_moves())

    @api.model
    def _default_stock_moves(self):
        # Obtener los movimientos desde el contexto (si existen)
        return self.env['stock.move'].browse(self.env.context.get('default_stock_move_ids', []))

    def generate_accounting_entries(self):
        """Generar asientos contables para los movimientos seleccionados."""
        for move in self.stock_move_ids:
            move._create_accounting_entries()  # Llama al método que genera los asientos contables
        return {'type': 'ir.actions.act_window_close'}
