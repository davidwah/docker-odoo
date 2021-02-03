from odoo import api, fields, models
from datetime import date, datetime

class UnpaidStudents(models.Model):
	_name = "asp.unpaid_spp_students"

	student_payment_id = fields.Many2one("asp.student_payments", ondelete="set null")
	name = fields.Char(string="Nama Siswa", related="student_payment_id.student_id.full_name")
	late_days = fields.Integer(string="Keterlambatan (Hari)", readonly=True)
	value = fields.Integer(string="Nominal Tunggakan", readonly=True)

	@api.one
	@api.depends("student_payment_id")
	def get_late_days(self):
		today_date = date.today().strftime("%d")
		int_today = int(today_date)
		if int_today > 15:
			self.late_days = int_today - 15
		else:
			self.late_days = 0

	@api.model
	def update_late_time(self):
		records = self.env['asp.unpaid_spp_students'].search([])
		for i in records:
			i['late_days'] += 1