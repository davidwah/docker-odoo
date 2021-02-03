from odoo import fields, api, models
import math
from collections import Counter

class Competency(models.Model):
	_name = "asc.base"

	name = fields.Char(string="Kompetensi Dasar", compute="get_name", store=True)
	number = fields.Char(string="Nomor Kompetensi", required=True)
	description = fields.Text(string="Deskripsi", required=True)
	course_id = fields.Many2one("asa.courses", ondelete="cascade", string="Pelajaran")

	@api.one
	@api.depends("number", "description")
	def get_name(self):
		self.name = "%s %s" % (self.number, self.description)

class Assesment(models.Model):
	_name = "asc.assesments"

	report_id = fields.Many2one("asa.reports", ondelete="cascade")
	category_id = fields.Many2one("asc.categories", ondelete="set null", string="Kategori Penilaian", required=True)
	description = fields.Char(string="Deskripsi", required=True)
	is_excellence = fields.Boolean(string="Excellent")
	is_good = fields.Boolean(string="Good")
	is_less = fields.Boolean(string="Need Practice")
	is_lacking = fields.Boolean(string="Experience Difficulty")

class AssesmentCatNote(models.Model):
	_name = "asc.asses_notes"

	report_id = fields.Many2one("asa.reports", ondelete="cascade")
	category_id = fields.Many2one("asc.categories", ondelete="set null", string="Kategori Penilaian")
	description = fields.Text(string="Deskripsi")

class AssesmentCategory(models.Model):
	_name = "asc.categories"

	name = fields.Char(string="Nama", compute="get_name", store=True)
	title = fields.Char(string="Nama Kategori", required=True)
	subtitle = fields.Char(string="Sub Nama Kategory")

	@api.one
	@api.depends("title", "subtitle")
	def get_name(self):
		if self.subtitle:
			self.name = "%s - %s" % (self.title, self.subtitle)
		else:
			self.name = self.title

class AttitudeCompentency(models.Model):
	_name = "asc.attitudes"

	name = fields.Char(compute="get_name", store=True)
	spiritual_final_grade = fields.Char(string="Nilai Akhir KD-1", compute="get_predicate", store=True)
	social_final_grade = fields.Char(string="Nilai Akhir KD-2", compute="get_predicate", store=True)
	spiritual_ids = fields.One2many("asc.spirituals", "parent_id", string="Nilai-nilai KD-1")
	social_ids = fields.One2many("asc.socials", "parent_id", string="Nilai-nilai KD-2")

	@api.one
	@api.depends("spiritual_ids", "social_ids")
	def get_predicate(self):
		if len(list(self.spiritual_ids)) > 0:
			spiritual_list = [i['grade'] for i in self.spiritual_ids]
			self.spiritual_final_grade = Counter(spiritual_list).most_common(1)[0][0]
		else:
			self.spiritual_final_grade = "Null"
		if len(list(self.social_ids)) > 0:
			social_list = [i['grade'] for i in self.social_ids]
			self.social_final_grade = Counter(social_list).most_common(1)[0][0]
		else:
			self.social_final_grade = "Null"

	@api.one
	@api.depends("spiritual_final_grade", "social_final_grade")
	def get_name(self):
		self.name = "Spiritual: %s - Sosial: %s" % (self.spiritual_final_grade, self.social_final_grade)

class SpiritualCompetency(models.Model):
	_name = "asc.spirituals"

	parent_id = fields.Many2one("asc.attitudes", ondelete="cascade")
	competency_id = fields.Many2one("asc.base", ondelete="cascade", domain="[('name', '=like', '1.%')]")
	grade = fields.Selection([
		('A', 'A'),
		('B', 'B'),
		('C', 'C'),
		('D', 'D')
	], required=True)

class SocialCompetency(models.Model):
	_name = "asc.socials"

	parent_id = fields.Many2one("asc.attitudes", ondelete="cascade")
	competency_id = fields.Many2one("asc.base", ondelete="cascade", domain="[('name', '=like', '2.%')]")
	grade = fields.Selection([
		('A', 'A'),
		('B', 'B'),
		('C', 'C'),
		('D', 'D')
	], required=True)

class GradeCompetency(models.Model):
	_name = "asc.grades"

	user_id = fields.Many2one("res.users", ondelete="set null", string="Dibuat Oleh", readonly=True, default=lambda self: self.env.user)
	report_id = fields.Many2one("asa.reports", ondelete="cascade")
	course_id = fields.Many2one("asa.courses", ondelete="cascade", string="Pelajaran", compute="get_course", store=True)
	grade_range_id = fields.Many2one("asa.grade_range", ondelete="set null", required=True)
	knowledge_final_grade = fields.Integer(string="Nilai Akhir KD-3", compute="get_knowledge_final", store=True)
	skill_final_grade = fields.Integer(string="Nilai Akhir KD-4", compute="get_skill_final", store=True)
	knowledge_predicate = fields.Char(string="Predikat Pengetahuan (KD-3)", compute="get_predicate", store=True)
	skill_predicate = fields.Char(string="Predikat Keterampilan (KD-4)", compute="get_predicate", store=True)
	knowledge_ids = fields.One2many("asc.knowledges", "parent_id", string="Nilai-nilai KD-3")
	skill_ids = fields.One2many("asc.skills", "parent_id", string="Nilai-nilai KD-4")
	can_access = fields.Boolean(compute="get_access")

	@api.depends("user_id")
	def get_access(self):
		for i in self:
			if i.user_id:
				if i.user_id == self.env.user:
					i.can_access = True
				else:
					i.can_access = False
			else:
				i.can_access = True

	@api.one
	@api.depends("user_id")
	def get_course(self):
		self.course_id = self.user_id.course_id

	# @api.one
	# @api.depends("user_id"):
	# def get_course(self):
	# 	self.course_id = self.user_id.course_id

	@api.one
	@api.depends("knowledge_final_grade", "skill_final_grade", "grade_range_id")
	def get_predicate(self):
		if self.grade_range_id:
			if self.knowledge_final_grade <= self.grade_range_id.max_d:
				self.knowledge_predicate = "D"
			elif self.knowledge_final_grade <= self.grade_range_id.max_c:
				self.knowledge_predicate = "C"
			elif self.knowledge_final_grade <= self.grade_range_id.max_b:
				self.knowledge_predicate = "B"
			else:
				self.knowledge_predicate = "A"

			if self.skill_final_grade <= self.grade_range_id.max_d:
				self.skill_predicate = "D"
			elif self.skill_final_grade <= self.grade_range_id.max_c:
				self.skill_predicate = "C"
			elif self.skill_final_grade <= self.grade_range_id.max_b:
				self.skill_predicate = "B"
			else:
				self.skill_predicate = "A"
		else:
			self.knowledge_predicate = "Null"
			self.skill_predicate = "Null"

	@api.one
	@api.depends("knowledge_ids")
	def get_knowledge_final(self):
		total, count = 0, 0
		for i in self.knowledge_ids:
			total += i.final_grade
			count += 1
		if count > 0:
			self.knowledge_final_grade = round(total/count)
		else:
			self.knowledge_final_grade = 0

	@api.one
	@api.depends("skill_ids")
	def get_skill_final(self):
		total, count = 0, 0
		for i in self.skill_ids:
			total += i.final_grade
			count += 1
		if count > 0:
			self.skill_final_grade = round(total/count)
		else:
			self.skill_final_grade = 0
					
class KnowledgeCompetency(models.Model):
	_name = "asc.knowledges"

	parent_id = fields.Many2one("asc.grades", ondelete="cascade")
	course_id = fields.Many2one("asa.courses", ondelete="cascade")
	competency_id = fields.Many2one("asc.base", ondelete="cascade", domain="[('course_id', '=', course_id), ('name', '=like', '3.%')]")
	daily_one = fields.Integer(string="PH1", required=True)
	daily_two = fields.Integer(string="PH2")
	daily_three = fields.Integer(string="PH3")
	daily_average = fields.Float(string="Rata-rata PH", compute="get_average_ph", store=True)
	remedial = fields.Integer(string="Remidi")
	daily_final = fields.Float(string="Nilai Akhir PH", compute="get_final_ph", store=True)
	mid_term = fields.Integer(string="Nilai Tengah Semester")
	final_term = fields.Integer(string="Nilai Akhir Semester")
	final_grade = fields.Integer(string="Nilai KD 3.n", compute="get_final_grade", store=True)

	@api.one
	@api.depends("daily_one", "daily_two", "daily_three")
	def get_average_ph(self):
		grades = []
		if self.daily_one > 0:
			grades.append(self.daily_one)
		if self.daily_two > 0:
			grades.append(self.daily_two)
		if self.daily_three > 0:
			grades.append(self.daily_three)
		if len(grades) > 0:
			average = sum(grades) / len(grades)
			self.daily_average = round(average, 1)
		else:
			self.daily_average = 0

	@api.one
	@api.depends("daily_average")
	def get_final_ph(self):
		self.daily_final = self.daily_average

	@api.one
	@api.depends("daily_final", "mid_term", "final_term")
	def get_final_grade(self):
		grades = []
		if self.daily_final > 0:
			grades.append(self.daily_final/2)
		if self.mid_term > 0:
			grades.append(self.mid_term/4)
		if self.final_term > 0:
			grades.append(self.final_term/4)
		temp = str(round(sum(grades), 2))
		index = temp.find(".")
		index += 1
		if int(temp[index]) == 5:
			result = float(temp)
			self.final_grade = math.ceil(result)
		else:
			result = float(temp)
			self.final_grade = round(result)

class SkillCompetency(models.Model):
	_name = "asc.skills"

	parent_id = fields.Many2one("asc.grades", ondelete="cascade")
	course_id = fields.Many2one("asa.courses", ondelete="cascade")
	competency_id = fields.Many2one("asc.base", ondelete="cascade", domain="[('course_id', '=', course_id), ('name', '=like', '4.%')]")
	practice_one = fields.Integer(string="Praktik 1")
	practice_two = fields.Integer(string="Praktik 2")
	product_one = fields.Integer(string="Produk 1")
	product_two = fields.Integer(string="Produk 2")
	project_one = fields.Integer(string="Proyek 1")
	project_two = fields.Integer(string="Proyek 2")
	portfolio = fields.Integer(string="Portfolio")
	final_grade = fields.Integer(string="Nilai KD 4.n", compute="get_final_grade", store=True)

	@api.one
	@api.depends("practice_one", "practice_two", 'product_one', 'product_two', 'project_one', 'project_two')
	def get_final_grade(self):
		if self.practice_one >= self.practice_two:
			practice = self.practice_one
		else:
			practice = self.practice_two
		if self.product_one >= self.product_two:
			product = self.product_one
		else:
			product = self.product_two
		if self.project_one >= self.project_two:
			project = self.project_one
		else:
			project = self.project_two
		grades = []
		if practice > 0:
			grades.append(practice)
		if product > 0:
			grades.append(product)
		if project > 0:
			grades.append(project)
		if len(grades) > 0:
			total = sum(grades)/len(grades)
			self.final_grade = round(total)
		else:
			self.final_grade = 0