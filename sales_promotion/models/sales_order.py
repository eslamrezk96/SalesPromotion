# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SalesOrder(models.Model):
    _name = 'sales.order'
    _rec_name = 'name'
    _description = 'Sales Order'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    customer = fields.Char(string="Customer", required=True, )
    order_date = fields.Datetime(string="Order Date", required=True, )
    order_items_ids = fields.One2many(comodel_name="sales.items", inverse_name="order_id", string='Order Items')
    amount_untaxed = fields.Float(string='Total Untaxed', readonly=True, compute='_amount_all', store=True)
    tax = fields.Float(string='Tax', readonly=True, compute='_compute_tax', store=True)
    total = fields.Float(string='Total', readonly=True, compute='_compute_total', store=True)
    promotion = fields.Many2one(comodel_name="sales.promotion", string="Promotion")
    hide = fields.Boolean(string='Hide', compute="apply_promotion")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.order.sequence') or _('New')
        result = super(SalesOrder, self).create(vals)
        return result

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
        order_items = self.env['sales.items']
        for record in self:
            order_count = order_items.search_count([('order_id','=', record.id)])
        if order_count > 2:
            self.hide = True
        else:
            self.hide = False


class SalesItems(models.Model):
    _name = 'sales.items'

    order_id = fields.Many2one(comodel_name="sales.order", string="Order Items")
    items = fields.Many2one(comodel_name="items", string="Items", required=True, )
    order_qty = fields.Integer(string="Order Qty", required=True,)
    price_unit = fields.Float('Unit Price', required=True, default=0.0, related='items.price_item')
    price_subtotal = fields.Float(compute='_compute_amount_subtotal', string='Subtotal', readonly=True, store=True)

    @api.depends('order_qty', 'price_unit')
    def _compute_amount_subtotal(self):
        """
                compute the subtotal of the order item
        """
        for lines in self:
            lines.price_subtotal = lines.price_unit * lines.order_qty

