# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, date, timedelta

class Attendance(models.Model):
	_name = "asa.attendances"

	date = fields.Date(string="Tanggal Absensi",  default=lambda *a: (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%d"))
	class_id = fields.Many2one("asm.classes", ondelete="set null", string="Kelas", required=True)
	current_class = fields.Char(compute="get_class_name", store=True)
	student_ids = fields.One2many("asa.students", "attendance_id", string="Daftar Kehadiran")
	create_uid = fields.Many2one("res.users", string="Dibuat oleh", ondelete="set null", readonly=True)
	write_uid = fields.Many2one("res.users", string="Diubah oleh", ondelete="set null", readonly=True)
	per_month_id = fields.Many2one("asa.per_months", ondelete="cascade", readonly=True)
	
	@api.model
	def create(self, values):
		res = super(Attendance, self).create(values)
		name = res['date'].strftime("%B %Y")
		existing = self.env['asa.per_months'].search([('name', '=', name)])
		if existing:
			res['per_month_id'] = existing.id
		else:
			new = self.env['asa.per_months'].create({
				'name': None,
				'month': res['date'].strftime('%B'),
				'year': res['date'].strftime('%Y'),
				'total_in': None,
				'total_sick': None,
				'total_absent': None,
				'total_permitted': None,
				'attendance_ids': None
			})
			res['per_month_id'] = new.id
		return res

	@api.onchange("current_class")
	def populate_students(self):
		self.ensure_one()
		if self.current_class:
			records = self.env['asm.students'].search([('current_class', '=', self.current_class)])
			arr = []
			for i in records:
				arr.append(i.id)
			if self.student_ids:
				self.student_ids = (5, 0, 0)
				self.student_ids = [(0, 0, {
					'student_id': i.id,
					'is_in': True,
					'is_sick': None,
					'is_absent': None,
					'is_permitted': None,
					'note': None,
				}) for i in records]
			else:
				self.student_ids = [(0, 0, {
					'student_id': i.id,
					'is_in': True,
					'is_sick': None,
					'is_absent': None,
					'is_permitted': None,
					'note': None,
				}) for i in records]

	@api.one
	@api.depends("class_id")
	def get_class_name(self):
		self.current_class = self.class_id.name

	def name_get(self):
		day_month = self.date.strftime("%d %B")
		year = self.date.strftime("%Y")
		name = self.class_id.name
		record_name = "%s %s %s" % (day_month, name, year)
		return [(self.id, record_name)]

class StudentAttendance(models.Model):
	_name = "asa.students"
	_rec_name = "student_id"

	attendance_id = fields.Many2one("asa.attendances", ondelete="cascade", readonly=True)
	student_id = fields.Many2one("asm.students", ondelete="set null", string="Siswa")
	current_class = fields.Char(compute="get_class", store=True)
	is_in = fields.Boolean(string="Masuk", default=True)
	is_sick = fields.Boolean(string="Sakit", default=True)
	is_absent = fields.Boolean(string="Tidak Masuk")
	is_permitted = fields.Boolean(string="Ijin")
	note = fields.Text(string="Keterangan")

	@api.one
	@api.depends("student_id")
	def get_class(self):
		self.current_class = self.student_id.current_class

class AttendancePerMonth(models.Model):
	_name = "asa.per_months"

	name = fields.Char(string="Periode", compute="get_periode", store=True)
	month = fields.Selection([
		("January", "January"),
		("February", "February"),
		("March", "March"),
		("April", "April"),
		("May", "May"),
		("June", "June"),
		("July", "July"),
		("August", "August"),
		("September", "September"),
		("October", "October"),
		("November", "November"),
		("December", "December")
	], string="Bulan", readonly=True)
	year = fields.Selection([(str(year), str(year)) for year in range(2000, 2200)], string="Tahun", readonly=True)
	total_in = fields.Integer(string="Total Masuk", compute="get_total", store=True)
	total_sick = fields.Integer(string="Total Sakit", compute="get_total", store=True)
	total_absent = fields.Integer(string="Total Tidak Masuk", compute="get_total", store=True)
	total_permitted = fields.Integer(string="Total Ijin", compute="get_total", store=True)
	attendance_ids = fields.One2many("asa.attendances", "per_month_id", string="Presensi Bulan Ini")

	@api.one
	@api.depends("month", "year")
	def get_periode(self):
		self.name = "%s %s" % (self.month, self.year)

	@api.one
	@api.depends("attendance_ids.student_ids")
	def get_total(self):
		total_in, total_sick, total_absent, total_permitted = 0, 0, 0, 0
		# if len(self.attendance_ids) > 0:
		for i in self.attendance_ids:
			for j in i.student_ids:
				if j.is_in:
					total_in += 1
				if j.is_sick:
					total_sick += 1
				if j.is_absent:
					total_absent += 1
				if j.is_permitted:
					total_permitted += 1
		self.total_in = total_in
		self.total_sick = total_sick
		self.total_permitted = total_permitted
		self.total_absent = total_absent

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#WIZARDS
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
class ClassAttendanceWizard(models.TransientModel):
	_name = "asw.attendance_per_class"

	start_date = fields.Date(string="Tanggal Awal", required=True)
	end_date = fields.Date(string="Tanggal Akhir", required=True)
	class_selected = fields.Many2one("asm.classes", ondelete="set null", required=True)

	@api.multi
	def get_report(self):
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'date_start': self.start_date,
				'date_end': self.end_date,
				'class_selected': self.class_selected.name,
			},
		}
		return self.env.ref('anugrah_school_attendance.attendance_recap_per_class').report_action(self, data=data)

class AttendancePerClassReport(models.AbstractModel):
	_name = 'report.anugrah_school_attendance.recap_class_template'

	@api.model
	def _get_report_values(self, docids, data=None):
		date_start = data['form']['date_start']
		date_end = data['form']['date_end']
		class_selected = data['form']['class_selected']

		docs = []
		records = self.env['asa.attendances'].search([('date', '>=', date_start), ('date', '<=', date_end), ('current_class', '=', class_selected)], order="date asc")
		for i in records:	
			# total_in = self.env['asa.students'].search_count([('attendance_id', '=', i.id), ('is_in', '=', True)])
			# total_absent = self.env['asa.students'].search_count([('attendance_id', '=', i.id), ('is_absent', '=', True)])
			# total_permitted = self.env['asa.students'].search_count([('attendance_id', '=', i.id), ('is_permitted', '=', True)])
			docs.append({
				'date': i.date,
				'current_class': i.current_class,
				'class_id': i.class_id,
				'student_ids': i.student_ids,
				'total_in': len(list(filter(lambda x: x.is_in == True, i.student_ids))),
				'total_sick': len(list(filter(lambda x: x.is_sick == True, i.student_ids))),
				'total_absent': len(list(filter(lambda x: x.is_absent == True, i.student_ids))),
				'total_permitted': len(list(filter(lambda x: x.is_permitted == True, i.student_ids))),
			})

		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'docs': docs,
			'date_start': date_start,
			'date_end': date_end,
			'class_selected': class_selected,
		}

class StudentAttendanceWizard(models.TransientModel):
	_name = "asw.attendance_per_student"

	start_date = fields.Date(string="Tanggal Awal", required=True)
	end_date = fields.Date(string="Tanggal Akhir", required=True)
	student_selected = fields.Many2one("asm.students", ondelete="set null", required=True)

	@api.multi
	def get_report(self):
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'date_start': self.start_date,
				'date_end': self.end_date,
				'student_selected': self.student_selected.id,
				'student_class': self.student_selected.current_class,
			},
		}
		return self.env.ref('anugrah_school_attendance.attendance_recap_per_student').report_action(self, data=data)

class AttendancePerStudentReport(models.AbstractModel):
	_name = 'report.anugrah_school_attendance.recap_student_template'

	@api.model
	def _get_report_values(self, docids, data=None):
		date_start = data['form']['date_start']
		date_end = data['form']['date_end']
		student_selected = data['form']['student_selected']
		student_class = data['form']['student_class']

		docs = []
		records = self.env['asa.attendances'].search([('date', '<=', date_end), ('date', '>=', date_start)], order="date asc")
		for i in records:
			for j in i.student_ids:
				if j.student_id.id == student_selected:
					docs.append({
						'date': i.date,
						'is_in': j.is_in,
						'is_sick': j.is_sick,
						'is_absent': j.is_absent,
						'is_permitted': j.is_permitted,
						'note': j.note,
					})
		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'docs': docs,
			'date_start': date_start,
			'date_end': date_end,
			'student': self.env['asm.students'].search([('id', '=', student_selected)]).full_name,
		}