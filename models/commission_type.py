from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CommissionType(models.Model):
    _name = 'pos.commission.type'
    _description = 'Commission Type'

    name = fields.Char(string='Nombre', required=True)
    commission_type = fields.Selection([
        ('percentage', 'Porcentaje'),
        ('fixed', 'Importe Fijo')
    ], string='Tipo de comisión', required=True, default='percentage')
    value = fields.Float(string='Valor', required=True)
    active = fields.Boolean(string='Activo', default=True)
    start_datetime = fields.Datetime(string='Fecha de Inicio')
    end_datetime = fields.Datetime(string='Fecha Final')
    product_id = fields.Many2one('product.product', string='Producto para factura', required=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError('Start date must be before end date')

    @api.constrains('value', 'commission_type')
    def _check_value(self):
        for record in self:
            if record.commission_type == 'percentage' and (record.value < 0 or record.value > 100):
                raise ValidationError('Percentage must be between 0 and 100')
            elif record.commission_type == 'fixed' and record.value < 0:
                raise ValidationError('Fixed amount cannot be negative')
