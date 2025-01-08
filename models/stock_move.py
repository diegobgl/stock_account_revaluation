from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_generate_valuation_and_accounting(self):
        """Generar valorizaciones y asientos contables para los movimientos seleccionados."""
        for move in self:
            # Crear la capa de valoración si no existe
            if not move.stock_valuation_layer_ids:
                move._create_valuation_layer()
            
            # Crear los asientos contables
            if not move.account_move_ids:
                move._create_accounting_entries()
        return True
