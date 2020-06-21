# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Items(models.Model):
    _name = 'items'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    price_item = fields.Float(string="Price",)
