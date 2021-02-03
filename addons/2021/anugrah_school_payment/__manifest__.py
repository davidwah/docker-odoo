# -*- coding: utf-8 -*-
{
    'name': "Anugrah School - Transaksi",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Troisindo",
    'website': "http://www.troisindo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'anugrah_school_master', 'anugrah_school_inventory'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/income_report.xml',
        'views/outcome_report.xml',
        'views/views.xml',
        'views/scheduler.xml',
        'views/inherited.xml',
        'views/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}