# -*- coding: utf-8 -*-
from odoo import http

# class PassDocsEmail(http.Controller):
#     @http.route('/pass_docs_email/pass_docs_email/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pass_docs_email/pass_docs_email/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pass_docs_email.listing', {
#             'root': '/pass_docs_email/pass_docs_email',
#             'objects': http.request.env['pass_docs_email.pass_docs_email'].search([]),
#         })

#     @http.route('/pass_docs_email/pass_docs_email/objects/<model("pass_docs_email.pass_docs_email"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pass_docs_email.object', {
#             'object': obj
#         })