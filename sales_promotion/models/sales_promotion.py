# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SalesPromotion(models.Model):
    _name = 'sales.promotion'
    _rec_name = 'name'
    _description = 'Sales Promotion'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    customer = fields.Char(string="Customer", required=True, )
    promotion_date = fields.Datetime(string="Promotion Date", required=True, )

    state = fields.Selection(string="Get Offer",
                             selection=[('buy_x_get_y', 'Buy X Items and get Y free'),
                                        ('get_disc', 'Discount'), ], )
    items = fields.Char(string="Items", required=True, )
    free_item = fields.Char(string="Free Items" , required=True,)
    item_qty = fields.Integer(string="Items Qty", required=True, )
    discount = fields.Float('Discount', required=True, default=0.0)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.promotion.sequence') or _('New')
        result = super(SalesPromotion, self).create(vals)
        return result
