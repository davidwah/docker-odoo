from odoo import models, fields, api

class Employee(models.Model):
	_name = "asm.employee"

	name = fields.Char(string="Nama Lengkap", required=True)
	address = fields.Char(string="Alamat")
	email = fields.Char(string="Email")
	phone = fields.Char(string="No. HP")
	user_id = fields.Many2one("res.users", ondelete="set null", string="User Ref.")

	base_salary = fields.Integer(string="Gaji Pokok")
	attendance_salary = fields.Integer(string="Gaji Absensi/Hari")
	overtime_salary = fields.Integer(string="Gaji Lembur")
	other_salary_ids = fields.One2many("ase.salary", "employee_id", string="Gaji Lain-lain", help="Gaji lain-lainya yang akan selalu didapatkan oleh karyawan dan nominalnya tidak akan berubah.")

class SalaryCategory(models.Model):
	_name = "ase.salary_category"

	name = fields.Char(string="Jenis Gaji")

class Salary(models.Model):
	_name = "ase.salary"

	name = fields.Many2one("ase.salary_category", ondelete="cascade", string="Jenis Gaji", required=True)
	amount = fields.Integer(string="Nominal", required=True)
	employee_id = fields.Many2one("asm.employee", ondelete="cascade", string="For Employee")

