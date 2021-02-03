from odoo import api, fields, models

class Course(models.Model):
	_name = "asa.courses"

	name = fields.Char(string="Nama Pelajaran", required=True)
	is_extra = fields.Boolean(string="Extrakurikuler", default=False)

class GradeRange(models.Model):
	_name = "asa.grade_range"

	name = fields.Char(string="Nama", compute="get_range", store="true")
	minimum_grade = fields.Integer(string="KKM")
	max_a = fields.Integer(string="Nilai Maks. A", compute="get_range", store=True, help="Nilai maksimal yang dicapai dalam jangkauan predikat A. Contoh: Nilai Maks. A >= X > Nilai Maks. B")
	max_b = fields.Integer(string="Nilai Maks. B", compute="get_range", store=True, help="Nilai maksimal yang dicapai dalam jangkauan predikat B. Contoh: Nilai Maks. B >= X > Nilai Maks. C")
	max_c = fields.Integer(string="Nilai Maks. C", compute="get_range", store=True, help="Nilai maksimal yang dicapai dalam jangkauan predikat C. Contoh: Nilai Maks. C >= X > Nilai Maks. D")
	max_d = fields.Integer(string="Nilai Maks. D", compute="get_range", store=True, help="Nilai maksimal yang dicapai dalam jangkauan predikat D. Contoh: Nilai Maks. D >= X >= 0")

	@api.one
	@api.depends("minimum_grade")
	def get_range(self):
		interval = (100 - self.minimum_grade) / 3
		self.max_d = self.minimum_grade - 1
		self.max_c = round(self.max_d + (interval))
		self.max_b = round(self.max_d + (interval * 2))
		self.max_a = 100
		self.name = "KKM - %d" % self.minimum_grade

class UsersInherit(models.Model):
	_inherit = "res.users"

	course_id = fields.Many2one("asa.courses", ondelete="set null", string="Mengajar Pelajaran")