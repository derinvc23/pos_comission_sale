from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError


class Commission(models.Model):
    _name = 'pos.commission'
    _description = 'POS Commission Record'
    _order = 'date desc'

    name = fields.Char(string='Referencia', readonly=True, copy=False, default='New')
    partner_id = fields.Many2one('res.partner', string='Agente', required=True)
    origin = fields.Char(string='Origen', readonly=True)
    liquidation_date = fields.Date(string='Fecha de liquidación')
    product_id = fields.Many2one('product.product', string='Producto', required=True)
    amount = fields.Float(string='Valor', required=True)
    commission_amount = fields.Float(string='Comisión', compute='_compute_commission', store=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado')
    ], string='State', default='draft')
    payment_state = fields.Selection([
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
    ], string='Estado de Pago', default='pending',
        compute='_compute_state_payment', store=True)
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    commission_type_id = fields.Many2one('pos.commission.type', string='Tipo de Comisión', required=True)
    pos_order_id = fields.Many2one('pos.order', string='Pedido POS')
    invoice_id = fields.Many2one('account.move', string='Factura', readonly=True, copy=False)
    commission_type_value = fields.Float(string='Valor Comisión %', related='commission_type_id.value', store=True, readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pos.commission') or 'New'
        return super(Commission, self).create(vals)

    @api.depends('amount', 'commission_type_id')
    def _compute_commission(self):
        for record in self:
            if record.commission_type_id and record.amount:
                if record.commission_type_id.commission_type == 'percentage':
                    record.commission_amount = (record.amount * record.commission_type_id.value) / 100
                else:  # fixed
                    record.commission_amount = record.commission_type_id.value
            else:
                record.commission_amount = 0.0

    @api.depends('invoice_id.payment_state')
    def _compute_state_payment(self):
        if self.invoice_id:
            if self.invoice_id.payment_state == 'paid':
                self.payment_state = 'paid'
                self.liquidation_date = fields.Date.today()

    def action_create_supplier_invoice(self):
        """
        Crear factura para la comisión
        """
        self.ensure_one()

        if self.invoice_id:
            raise UserError('La factura ya ha sido creada para esta comisión!')

        if self.state != 'confirmed':
            raise UserError('Only confirmed commissions can be invoiced!')

        if not self.partner_id.property_account_payable_id:
            raise UserError('Debe configurar una cuenta por pagar para el agente!')

        # Crear la factura
        invoice_vals = {
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f'Comision: {self.name} - {self.origin}',
                'quantity': 1.0,
                'price_unit': self.commission_amount,
                'product_id': self.commission_type_id.product_id.id,
            })],
        }

        invoice = self.env['account.move'].create(invoice_vals)
        self.write({
            'invoice_id': invoice.id,
            'payment_state': 'paid' if invoice.payment_state == 'paid' else 'pending'
        })

        # Devolver una acción para ver la factura creada
        return {
            'name': 'Factura de Proveedor',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }
