# -*- coding: utf-8 -*-
from odoo import http

# class Salary(http.Controller):
#     @http.route('/salary/salary/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salary/salary/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salary.listing', {
#             'root': '/salary/salary',
#             'objects': http.request.env['salary.salary'].search([]),
#         })

#     @http.route('/salary/salary/objects/<model("salary.salary"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salary.object', {
#             'object': obj
#         })