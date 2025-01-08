from odoo import models, fields, api

class GenerateAccountingEntriesWizard(models.TransientModel):
    _name = 'generate.accounting.entries.wizard'
    _description = 'Buscar Movimientos Sin Valorización'

    start_date = fields.Date(string='Fecha Inicio', required=True)
    end_date = fields.Date(string='Fecha Fin', required=True)
    move_type = fields.Selection([
        ('incoming', 'Entrada'),
        ('outgoing', 'Salida'),
        ('internal', 'Interno')
    ], string='Tipo de Movimiento', required=False)

    def search_stock_moves_without_valuation(self):
        """Buscar movimientos de stock sin capas de valoración."""
        domain = [
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('state', '=', 'done'),
            ('stock_valuation_layer_ids', '=', False)  # Movimientos sin capas de valoración
        ]
        if self.move_type:
            domain.append(('picking_type_id.code', '=', self.move_type))

        stock_moves = self.env['stock.move'].search(domain)

        # Retornar una acción para mostrar los resultados en una vista tree
        return {
            'type': 'ir.actions.act_window',
            'name': 'Movimientos Sin Valorización',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', stock_moves.ids)],
            'context': {'create': False},  # Evitar creación de nuevos registros desde esta vista
        }
