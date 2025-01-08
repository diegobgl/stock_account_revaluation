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
    ], string='Tipo de Movimiento', required=False)

    def search_stock_moves_without_accounting(self):
        """Buscar movimientos de stock sin valorización."""
        domain = [
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('state', '=', 'done'),
            ('account_move_ids', '=', False)  # Movimientos sin asiento contable
        ]
        if self.move_type:
            domain.append(('picking_type_id.code', '=', self.move_type))
        
        stock_moves = self.env['stock.move'].search(domain)
        
        # Retornar una acción para mostrar los resultados en una vista tree con opción de acción masiva
        return {
            'type': 'ir.actions.act_window',
            'name': 'Movimientos Sin Valorización',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', stock_moves.ids)],
            'context': {'create': False},  # Evitar creación de nuevos movimientos desde esta vista
        }
