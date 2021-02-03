# -*- coding: utf-8 -*-
from odoo import http

# class AnugrahSchoolMaster(http.Controller):
#     @http.route('/anugrah_school_master/anugrah_school_master/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anugrah_school_master/anugrah_school_master/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anugrah_school_master.listing', {
#             'root': '/anugrah_school_master/anugrah_school_master',
#             'objects': http.request.env['anugrah_school_master.anugrah_school_master'].search([]),
#         })

#     @http.route('/anugrah_school_master/anugrah_school_master/objects/<model("anugrah_school_master.anugrah_school_master"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anugrah_school_master.object', {
#             'object': obj
#         })