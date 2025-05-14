from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    agent_partner_id = fields.Many2one('res.partner', string='Agente', domain=[('is_agent', '=', True)])
    commision_value_id = fields.Many2one('pos.commission.type', string='Tipo de Comisión')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _process_order(self, order, draft, existing_order):
        res = super(PosOrder, self)._process_order(order, draft, existing_order)
        order_id = self.browse(res)

        for line_data in order['data'].get('lines', []):
            line = order_id.lines.filtered(lambda l: l.uuid == line_data[2].get('uuid'))
            if line and line_data[2].get('agent_id'):
                line.write({
                    'agent_partner_id': line_data[2]['agent_id'],
                    'commision_value_id': line_data[2]['commision_value_id'],
                })
                commision_type = self.env['pos.commission.type'].browse(line_data[2]['commision_value_id'])
                if commision_type.start_datetime <= order_id.date_order <= commision_type.end_datetime:
                    vals = {
                        'partner_id': line_data[2]['agent_id'],
                        'origin': order_id.name,
                        'product_id': line.product_id.id,
                        'amount': line.price_subtotal_incl,
                        'commission_type_id': line_data[2]['commision_value_id'],
                        'state': 'confirmed',
                        'pos_order_id': order_id.id,
                        'date': fields.Datetime.now(),
                    }
                    self.env['pos.commission'].create(vals)

        return res
