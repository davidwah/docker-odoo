# -*- coding: utf-8 -*-
from odoo import http

# class AnugrahSchoolInventory(http.Controller):
#     @http.route('/anugrah_school_inventory/anugrah_school_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anugrah_school_inventory/anugrah_school_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anugrah_school_inventory.listing', {
#             'root': '/anugrah_school_inventory/anugrah_school_inventory',
#             'objects': http.request.env['anugrah_school_inventory.anugrah_school_inventory'].search([]),
#         })

#     @http.route('/anugrah_school_inventory/anugrah_school_inventory/objects/<model("anugrah_school_inventory.anugrah_school_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anugrah_school_inventory.object', {
#             'object': obj
#         })