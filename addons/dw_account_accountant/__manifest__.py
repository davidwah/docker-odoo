# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo 13 Accounting',
    'version': '13.0.2.0.2',
    'category': 'Accounting',
    'summary': 'Accounting Reports, Asset Management and Account Budget For Odoo13 Community Edition',
    'live_test_url': 'https://www.youtube.com/',
    'sequence': '8',
    'website': '',
    'author': 'Odoo DWP',
    'license': 'LGPL-3',
    'website': '',
    'depends': ['accounting_pdf_reports', 'om_account_asset', 'om_account_budget'],
    'demo': [],
    'data': [
        'views/account.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'qweb': [],
}
