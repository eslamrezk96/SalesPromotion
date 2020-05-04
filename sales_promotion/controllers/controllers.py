# -*- coding: utf-8 -*-
from odoo import http

# class SalesPromotion(http.Controller):
#     @http.route('/sales_promotion/sales_promotion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_promotion/sales_promotion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_promotion.listing', {
#             'root': '/sales_promotion/sales_promotion',
#             'objects': http.request.env['sales_promotion.sales_promotion'].search([]),
#         })

#     @http.route('/sales_promotion/sales_promotion/objects/<model("sales_promotion.sales_promotion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_promotion.object', {
#             'object': obj
#         })