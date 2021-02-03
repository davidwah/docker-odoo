# -*- coding: utf-8 -*-
from odoo import http

# class AnugrahSchoolPayment(http.Controller):
#     @http.route('/anugrah_school_payment/anugrah_school_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anugrah_school_payment/anugrah_school_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anugrah_school_payment.listing', {
#             'root': '/anugrah_school_payment/anugrah_school_payment',
#             'objects': http.request.env['anugrah_school_payment.anugrah_school_payment'].search([]),
#         })

#     @http.route('/anugrah_school_payment/anugrah_school_payment/objects/<model("anugrah_school_payment.anugrah_school_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anugrah_school_payment.object', {
#             'object': obj
#         })