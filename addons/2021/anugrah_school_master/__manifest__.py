# -*- coding: utf-8 -*-
{
    'name': "Anugrah School - Master",

    'summary': """
        Included are containers of master students and classes""",

    'description': """
        Listing every student's registration form and school's classes
    """,

    'author': "Troisindo",
    'website': "http://www.troisindo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/inherited.xml',
        'views/report.xml',
        'company/filler.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}