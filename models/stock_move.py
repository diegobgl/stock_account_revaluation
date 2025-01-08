from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_generate_accounting_entries(self):
        """Generar valorizaciones y asientos contables para los movimientos seleccionados."""
        for move in self:
            # Verifica si ya tiene asientos contables
            if not move.account_move_ids:
                # Método nativo para crear las valorizaciones y los asientos
                move._create_accounting_entries()
        return True
