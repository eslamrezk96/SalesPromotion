# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SalesPromotion(models.Model):
    _name = 'sales.promotion'
    _rec_name = 'name'
    _description = 'Sales Promotion'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    customer = fields.Char(string="Customer", required=True, )
    order_date = fields.Datetime(string="Order Date", required=True, )
    state = fields.Selection(string="Get Sales Promotion",
                             selection=[('buy_2_get_1', 'Buy 2 Items and get 1 free'),
                                        ('get_disc', 'Get Discount'), ],)
    items = fields.Char(string="Items", required=True, )
    free_items = fields.Integer(string="Free Items", required=True, )
    order_qty = fields.Integer(string="Order Qty", required=True, )
    price_unit = fields.Float('Unit Price', required=True, default=0.0)
    discount = fields.Float('Discount', required=True, default=0.0)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.promotion.sequence') or _('New')
        result = super(SalesPromotion, self).create(vals)
        return result
