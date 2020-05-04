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
    order_items_ids = fields.One2many(comodel_name="sales.items", inverse_name="order_id", string='Order Items')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.promotion.sequence') or _('New')
        result = super(SalesPromotion, self).create(vals)
        return result


class SalesItems(models.Model):
    _name = 'sales.items'

    order_id = fields.Many2one(comodel_name="sales.promotion", string="Order Items")
    items = fields.Char(string="Items", required=True, )
    order_qty = fields.Integer(string="Order Qty", required=True, )
    unit_price = fields.Float(string="Unit Price",  required=True, )
