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
    total_with_out_dis = fields.Float(string='Total With Out Discount', readonly=True, compute='_amount_all_with_dis',
                                      store=True)
    amount_untaxed = fields.Float(string='Total After Discount', readonly=True, compute='_amount_all', store=True)
    tax = fields.Float(string='Tax', readonly=True, compute='_compute_tax', store=True)
    total = fields.Float(string='Total', readonly=True, compute='_compute_total', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.promotion.sequence') or _('New')
        result = super(SalesPromotion, self).create(vals)
        return result

    @api.depends('order_items_ids.price_unit','order_items_ids.order_qty')
    def _amount_all_with_dis(self):
        """
              compute the all total of the order items with out discount
        """
        for order in self:
            total_with_out_dis = 0.0
            for line in order.order_items_ids:
                total_with_out_dis += line.price_unit * line.order_qty
            order.update({
                'total_with_out_dis': total_with_out_dis,
            })

    @api.depends('order_items_ids.price_subtotal')
    def _amount_all(self):
        """
              compute the all total of the order items
        """
        for order in self:
            amount_untaxed = 0.0
            for line in order.order_items_ids:
                amount_untaxed += line.price_subtotal
            order.update({
                'amount_untaxed': amount_untaxed,
            })

    @api.depends('amount_untaxed')
    def _compute_tax(self):
        """
                compute the tax for all total price
        """
        for line in self:
            line.tax = (line.amount_untaxed * 14) / 100

    @api.depends('amount_untaxed', 'total')
    def _compute_total(self):
        for line in self:
            line.total = line.amount_untaxed + line.tax

    @api.multi
    def apply_promotion(self):
        for order in self:
            for line in order.order_items_ids:
                if line.order_qty > 3:
                    line.discount = ((line.price_unit * (-50)) / 100) * (line.order_qty - 3)
                else:
                    line.discount = 0.0


class SalesItems(models.Model):
    _name = 'sales.items'

    order_id = fields.Many2one(comodel_name="sales.promotion", string="Order Items")
    items = fields.Char(string="Items", required=True, )
    order_qty = fields.Integer(string="Order Qty", required=True, )
    price_unit = fields.Float('Unit Price', required=True, default=0.0)
    discount = fields.Float('Discount', required=True, default=0.0)
    price_subtotal = fields.Float(compute='_compute_amount_subtotal', string='Subtotal', readonly=True, store=True)

    @api.depends('order_qty', 'price_unit', 'discount')
    def _compute_amount_subtotal(self):
        """
                compute the subtotal of the order item
        """
        for lines in self:
            lines.price_subtotal = (lines.price_unit * lines.order_qty) + lines.discount
