from odoo import api, fields, models
from datetime import datetime, date, time

class PaymentScheduler(models.Model):
	_name = "asp.cron"

	@api.model
	def update_monthly(self):
		records = self.env['asm.students'].search([('state', 'in', ['active', 'registered'])])
		for i in records:
			i['unpaid_spp'] = i['spp_monthly']

	@api.model
	def update_half_month(self):
		records = self.env['asm.students'].search([('state', '=', 'active')])
		curr_month = date.today().strftime("%B")
		curr_year = date.today().strftime("%Y")
		for i in records:
			existing = self.env['asp.unpaid_spp_students'].search([('name', '=', i.full_name)], limit=1)
			already_paid = self.env['asp.payment_records'].search([('student_id', '=', i.id), ('state', '=', 'spp'), ('spp_month', '=', curr_month), ('spp_year', '=', curr_year)], limit=1)
			if existing:
				if not already_paid:
					existing.value += i.spp_monthly
			else:
				if not already_paid:
					student_payment = self.env['asp.student_payments'].search([('student_id', '=', i.id)], limit=1)
					if i.unpaid_spp > 0:
						new_record = self.env['asp.unpaid_spp_students'].create({
							'student_payment_id': student_payment.id,
							'name': None,
							'late_days': None,
							'value': i.unpaid_spp
						})
					else:
						new_record = self.env['asp.unpaid_spp_students'].create({
							'student_payment_id': student_payment.id,
							'name': None,
							'late_days': None,
							'value': i.spp_monthly
						})