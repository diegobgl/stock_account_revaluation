from odoo import models, fields, api

class GenerateAccountingEntriesWizard(models.TransientModel):
    _name = 'generate.accounting.entries.wizard'
    _description = 'Generar Asientos Contables'

    start_date = fields.Date(string='Fecha Inicio')
    end_date = fields.Date(string='Fecha Fin')
    move_type = fields.Selection([
        ('incoming', 'Entrada'),
        ('outgoing', 'Salida'),
        ('internal', 'Interno')
    ], string='Tipo de Movimiento')
    stock_move_ids = fields.Many2many('stock.move', string='Movimientos de Stock', default=lambda self: self._default_stock_moves())

    def _default_stock_moves(self):
        # Obtener movimientos preseleccionados desde el contexto
        return self.env['stock.move'].browse(self.env.context.get('default_stock_move_ids', []))

    @api.onchange('start_date', 'end_date', 'move_type')
    def _onchange_stock_moves(self):
        """Filtrar movimientos basados en los criterios de fecha y tipo."""
        domain = [('state', '=', 'done')]
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        if self.end_date:
            domain.append(('date', '<=', self.end_date))
        if self.move_type:
            domain.append(('picking_type_id.code', '=', self.move_type))
        self.stock_move_ids = self.env['stock.move'].search(domain)

    def generate_accounting_entries(self):
        """Generar asientos contables para los movimientos seleccionados."""
        for move in self.stock_move_ids:
            move._create_accounting_entries()
        return {'type': 'ir.actions.act_window_close'}
