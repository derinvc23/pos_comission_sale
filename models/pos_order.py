from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    agent_partner_id = fields.Many2one('res.partner', string='Agente', domain=[('is_agent', '=', True)])
    commission_percentage = fields.Float(string='Commission Percentage')
    commission_amount = fields.Float(string='Commission Amount', compute='_compute_commission_amount')

    @api.depends('amount_total', 'commission_percentage')
    def _compute_commission_amount(self):
        for order in self:
            order.commission_amount = order.amount_total * (order.commission_percentage / 100.0)

    # def _process_order(self, order):
    #     res = super()._process_order(order)
    #     if order.get('agent_id'):
    #         self.write({
    #             'agent_id': order['agent_id'],
    #             'commission_percentage': order['commission_percentage'],
    #         })
    #     return res