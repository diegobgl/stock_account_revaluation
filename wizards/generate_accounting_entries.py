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
        """Buscar movimientos de stock sin capas de valoración que cumplan con condiciones específicas."""
        # Dominio base
        domain = [
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date),
            ('state', '=', 'done'),
            ('stock_valuation_layer_ids', '=', False)  # Movimientos sin capas de valoración
        ]

        # Subdominios para las condiciones de ubicación
        condition_transit_to_production = [
            ('location_id.usage', '=', 'transit'),
            ('location_dest_id.usage', '=', 'production')
        ]
        condition_internal_to_production = [
            ('location_id.usage', '=', 'internal'),
            ('location_dest_id.usage', '=', 'production')
        ]
        condition_production_to_production = [
            ('location_id.usage', '=', 'production'),
            ('location_dest_id.usage', '=', 'production')
        ]
        condition_production_to_transit = [
            ('location_id.usage', '=', 'production'),
            ('location_dest_id.usage', '=', 'transit')
        ]

        # Construcción del dominio combinando los subdominios
        location_conditions = [
            '|',
            '|',
            '|',
            condition_transit_to_production,
            condition_internal_to_production,
            condition_production_to_production,
            condition_production_to_transit
        ]

        # Agregar las condiciones de ubicación al dominio principal
        domain.extend(location_conditions)

        # Buscar los movimientos según el dominio actualizado
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
