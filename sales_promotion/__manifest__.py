# -*- coding: utf-8 -*-
{
    'name': "Sales Promotion",
    'summary': """ Module for managing the sales """,
    'author': "Eslam Mohamed Rezk",
    'category': 'Sales',
    'version': '12.0.1.0.0',
    'installable': True,
    'application': True,
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sales_order.xml',
        'views/sales_promotion.xml',
        'views/items.xml',
        'data/sequence.xml',
        'data/data.xml',
        'reports/order_report_templates.xml',
        'reports/report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
