# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SalesPromotion(models.Model):
    _name = 'sales.promotion'
    _rec_name = 'name'
    _description = 'Sales Promotion'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.promotion.sequence') or _('New')
        result = super(SalesPromotion, self).create(vals)
        return result

    customer = fields.Char(string="Customer", required=True, )
    promotion_date = fields.Datetime(string="Promotion Date", required=True, )
    state = fields.Selection(string="Get Offer",
                             selection=[('buy_x_get_y', 'Buy X Items and get Y free'),
                                        ('get_disc', 'Discount'), ], )
    items = fields.Many2one(comodel_name="items", string="Items", required=True, )
    price_unit = fields.Float('Unit Price', required=True, default=0.0, related='items.price_item')
    free_item = fields.Many2one(comodel_name="items", string="Free Items", )
    item_qty = fields.Integer(string="Items Qty", required=True, default=0.0)
    discount = fields.Float('Discount %', required=True, default=0.0)
    total = fields.Float('Total', required=True, default=0.0, compute='compute_total', sort=True)

    @api.depends('price_unit', 'item_qty', 'discount')
    def compute_total(self):
        for lines in self:
            if lines.state == 'buy_x_get_y':
                lines.total = lines.price_unit * lines.item_qty
            elif lines.state == 'get_disc':
                sub_total = lines.price_unit * lines.item_qty
                sub_discount = (sub_total * lines.discount) / 100
                lines.total = sub_total - sub_discount
