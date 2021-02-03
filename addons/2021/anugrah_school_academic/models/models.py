# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class ReportCard(models.Model):
	_name = "asa.reports"

	selected_format = fields.Selection([
		('pg', 'PG'),
		('tk', 'TK'),
		('sd', 'SD'),
		('smp', 'SMP'),
	], string="Jenis Raport", default="sd")
	mid_semester = fields.Boolean(string="Tengah Semester")

	student_id = fields.Many2one("asm.students", ondelete="cascade")
	current_class = fields.Char(string="Kelas", compute="get_class", store=True)
	term_id = fields.Many2one("asa.terms", ondelete="set null", string="Tahun Ajaran")
	semester = fields.Selection([
		('odd', 'Ganjil'),
		('even', 'Genap')
	], string="Semester", default="odd")
	report_date = fields.Date(string="Tanggal Tertanda", default=lambda *a: (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%d"))
	graduated = fields.Boolean(string="Naik Kelas", default=False)
	advices = fields.Text(string="Saran-saran", required=True, default="Keep it up!")

	total_in = fields.Integer(string="Masuk Sekolah", compute="calculate_attendance", store=True)
	total_sick = fields.Integer(string="Sakit", compute="calculate_attendance", store=True)
	total_absent = fields.Integer(string="Tidak Masuk Sekolah", compute="calculate_attendance", store=True)
	total_permitted = fields.Integer(string="Ijin Sekolah", compute="calculate_attendance", store=True)

	attitude_id = fields.Many2one("asc.attitudes", ondelete="set null", string="Nilai Sikap")
	grade_ids = fields.One2many("asc.grades", "report_id", string="Nilai Pelajaran")
	assesment_ids = fields.One2many("asc.assesments", "report_id", string="Penilaian Akhir Semester")
	assesment_note_ids = fields.One2many("asc.asses_notes", "report_id", string="Penilaian Tengah Semester")
	teacher_comment = fields.Text(string="Komentar Guru")

	health_welfare_ids = fields.One2many("asa.health_welfares", "report_id", string="Kesehatan Fisik")
	prestige_ids = fields.One2many("asa.prestiges", "report_id", string="Prestasi")

	create_uid = fields.Many2one("res.users", ondelete="set null", string="Dibuat oleh", readonly=True)
	write_uid = fields.Many2one("res.users", ondelete="set null", string="Diubah oleh", readonly=True)
	company_id = fields.Many2one('res.company', 'Company', compute="get_company", store=True)
	can_access = fields.Boolean(compute="get_access")

	@api.depends("create_uid")
	def get_access(self):
		for i in self:
			if i.create_uid:
				if i.create_uid == self.env.user:
					i.can_access = True
				else:
					i.can_access = False
			else:
				i.can_access = True
	
	@api.one
	@api.depends("student_id")
	def get_company(self):
		if self.student_id:
			self.company_id = self.student_id.company_id

	def name_get(self):
		if self.semester == "odd":
			semester = "GANJIL"
		else:
			semester = "GENAP"
		record_name = "%s %s - %s" % (self.student_id.full_name, self.term_id.name, semester)
		return [(self.id, record_name)]

	@api.one
	@api.depends("student_id")
	def get_class(self):
		self.current_class = self.student_id.current_class

	@api.one
	@api.depends("student_id")
	def calculate_attendance(self):
		records = self.env['asa.students'].search([('student_id', '=', self.student_id.id), ('current_class', '=', self.student_id.current_class)])
		self.total_in = len(list(filter(lambda x: x.is_in==True, records)))
		self.total_absent = len(list(filter(lambda x: x.is_absent==True, records)))
		self.total_permitted = len(list(filter(lambda x: x.is_permitted==True, records)))
		self.total_sick = len(list(filter(lambda x: x.is_sick==True, records)))

	@api.multi
	def unlink(self):
		for i in self:
			if i.create_uid == self.env.user:
				return models.Model.unlink(self)
			else:
				raise exceptions.ValidationError("Sorry you are not the creator of this record therefore you are not elligible to delete it.")

class ReportAbstract(models.AbstractModel):
	_name = 'report.anugrah_school_academic.student_report_card'

	@api.model
	def _get_report_values(self, docids, data=None):
		assesment = {}
		record = self.env['asa.reports'].search([('id', '=', docids)])
		for i in record.assesment_ids:
			if i.category_id.name in assesment:
				assesment[i.category_id.name].append(i)
			else:
				assesment[i.category_id.name] = [i]

		return {
			'doc_ids': docids,
			'docs': record,
			'assesments': assesment,
		}

class MidReportAbstract(models.AbstractModel):
	_name = 'report.anugrah_school_academic.mid_card'

	@api.model
	def _get_report_values(self, docids, data=None):
		record = self.env['asa.reports'].search([('id', '=', docids)])
		return {
			'doc_ids': docids,
			'docs': record,
		}

class StudentInheritReport(models.Model):
	_inherit = "asm.students"

	report_ids = fields.One2many("asa.reports", "student_id", string="Laporan Akademik")