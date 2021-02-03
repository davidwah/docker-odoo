from odoo import fields, models, api

class StudentClass(models.Model):
	_name = "asm.classes"

	name = fields.Char(string="Nama Kelas", required=True)
	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", default="1 PG", required=True)