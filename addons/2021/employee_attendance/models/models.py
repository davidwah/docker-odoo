from odoo import models, fields, api

class Attendance(models.Model):
	_name = "ase.attendance"

	employee_id = fields.Many2one("asm.employee", ondelete="cascade", string="Karyawan")
	pin = fields.Char(string="PIN", related="employee_id.pin")
	check_in = fields.Datetime(string="Jam Masuk")
	check_out = fields.Datetime(string="Jam Keluar")

class EmployeeInherit(models.Model):
	_inherit = "asm.employee"

	pin = fields.Char(string="PIN Absensi")
	shift = fields.Many2one("asm.shift", ondelete="restrict", string="Jam Kerja")
	attendance_ids = fields.One2many("ase.attendance", "employee_id", string="Absensi")

class Shift(models.Model):
	_name = "asm.shift"

	name = fields.Char(compute="_get_name", store=True)
	work_hour = fields.Float(string="Jam Kerja/Hari", required=True)

	@api.multi
	@api.depends("work_hour")
	def _get_name(self):
		for i in self:
			i.name = "%d Jam/Hari" % i.work_hour