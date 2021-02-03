from odoo import api, fields, models

class HealthWelfare(models.Model):
	_name = "asa.health_welfares"

	report_id = fields.Many2one("asa.reports", ondelete="cascade")
	name = fields.Char(string="Nama Aspek", required=True)
	note = fields.Text(string="Keterangan", required=True)

class Prestige(models.Model):
	_name = "asa.prestiges"

	report_id = fields.Many2one("asa.reports", ondelete="cascade")
	name = fields.Char(string="Nama Prestasi", required=True)
	note = fields.Text(string="Keterangan", required=True)

class SchoolYear(models.Model):
	_name = "asa.terms"

	name = fields.Char(string="Tahun Ajaran", required=True)
