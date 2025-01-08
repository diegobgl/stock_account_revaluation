from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    missing_accounting_entries = fields.Boolean(
        string='Faltan Asientos Contables',
        compute='_compute_missing_accounting_entries',
        store=True
    )

    def _compute_missing_accounting_entries(self):
        for move in self:
            move.missing_accounting_entries = not move.account_move_ids
