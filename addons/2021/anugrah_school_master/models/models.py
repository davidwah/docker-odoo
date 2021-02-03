# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime

class MasterStudent(models.Model):
	_name = 'asm.students'
	_rec_name = "full_name"

	nias = fields.Char(string="Nomor Induk Anugerah School")
	full_name = fields.Char(string="Nama Lengkap", required=True)
	nipd = fields.Char(string="NIS/Nomor Induk PD")
	gender = fields.Selection([('L', 'Laki-laki'), ('P', 'Perempuan')], default="L", string="Jenis Kelamin", required=True)
	nisn = fields.Char(string="NISN")
	birth_place = fields.Char(string="Tempat Lahir", required=True)
	birth_date = fields.Date(string="Tanggal Lahir", required=True)
	nik = fields.Char(string="NIK/No. KITAS")
	religion = fields.Selection([
		('01', 'Islam'), 
		('02', 'Kristen/Protestan'), 
		('03', 'Katolik'), 
		('04', 'Hindu'), 
		('05', 'Budha'), 
		('06', 'Khonghucu'), 
		('07', 'Kepercayaan Terhadap Tuhan YME')
	], default='01', string="Agama", required=True)
	address = fields.Char(string="Alamat Lengkap", required=True)
	rt = fields.Char(string="RT")
	rw = fields.Char(string="RW")
	village = fields.Char(string="Nama Dusun", default="-")
	sub_district = fields.Char(string="Nama Kelurahan/Desa", default="-")
	district = fields.Char(string="Kecamatan", default="-")
	zip_code = fields.Char(string="Kode Pos")
	address_type = fields.Selection([('01', 'Bersama Orang Tua'), ('02', 'Wali'), ('03', 'Kos'), ('04', 'Asrama'), ('05', 'Panti Asuhan'), ('99', 'Lainnya')], string="Jenis Tempat Tinggal", default="01")
	transportation = fields.Selection([
		('01', 'Jalan Kaki'),
		('02', 'Kendaraan Pribadi'),
		('03', 'Kendaraan Umum/Angkot/Pete-Pete'),
		('04', 'Jemputan Sekolah'),
		('05', 'Kereta Api'),
		('06', 'Ojek'),
		('07', 'Andong/Bendi/Sado/Dokar/Delman/Beca'),
		('08', 'Perahu Penyebrangan/Rakit/Getek'),
		('99', 'Lainnya'),
	], string="Transportasi", default="01")
	home_phone_number = fields.Char(string="Nomor Telepon Rumah")
	cellphone_number = fields.Char(string="Nomor HP")
	email = fields.Char(string="Email")
	skhun_number = fields.Char(string="Nomor SKHUN SMP/MTs")
	receive_kps = fields.Selection([('1', 'Ya'), ('0', 'Tidak')], string="Penerima KPS", default="1")
	kps_number = fields.Char(string="Nomor KPS")	

	father_name = fields.Char(string="Nama Ayah Kandung")
	father_nik = fields.Char(string="NIK Ayah")
	father_birth_year = fields.Integer(string="Tahun Lahir Ayah")
	father_education = fields.Selection([
		('01', 'Tidak Sekolah'),
		('02', 'Putus SD'),
		('03', 'SD Sederajat'),
		('04', 'SMP Sederajat'),
		('05', 'SMA Sederajat'),
		('06', 'D1'),
		('07', 'D2'),
		('08', 'D3'),
		('09', 'D4/S1'),
		('10', 'S2'),
		('11', 'S3'),
		('99', 'Lainnya')
	], string="Pendidikan Ayah", default="01")
	father_work = fields.Selection([
		('01', 'Tidak Bekerja'),
		('02', 'Nelayan'),
		('03', 'Petani'),
		('04', 'Peternak'),
		('05', 'PNS/TNI/Polri'),
		('06', 'Karyawan Swasta'),
		('07', 'Pedagang Kecil'),
		('08', 'Pedagang Besar'),
		('09', 'Wiraswasta'),
		('10', 'Wirausaha'),
		('11', 'Buruh'),
		('12', 'Pensiunan'),
		('99', 'Lainnya'),
	], string="Pekerjaan Ayah", default="01")	
	father_income = fields.Selection([
		('01', '< Rp.500.000'),
		('02', 'Rp.500.000 - Rp.999.999'),
		('03', 'Rp.1.000.000 - Rp.1.999.999'),
		('04', 'Rp.2.000.000 - Rp.4.999.999'),
		('05', 'Rp.5.000.000 - Rp.20.000.000'),
		('06', '> Rp.20.000.000'),
		('07', 'Tidak Berpenghasilan'),
	], string="Penghasilan Ayah", default="01")	

	mother_name = fields.Char(string="Nama Ibu Kandung")
	mother_nik = fields.Char(string="NIK Ibu")
	mother_birth_year = fields.Integer(string="Tahun Lahir Ibu")
	mother_education = fields.Selection([
		('01', 'Tidak Sekolah'),
		('02', 'Putus SD'),
		('03', 'SD Sederajat'),
		('04', 'SMP Sederajat'),
		('05', 'SMA Sederajat'),
		('06', 'D1'),
		('07', 'D2'),
		('08', 'D3'),
		('09', 'D4/S1'),
		('10', 'S2'),
		('11', 'S3'),
		('99', 'Lainnya')
	], string="Pendidikan Ibu", default="01")
	mother_work = fields.Selection([
		('01', 'Tidak Bekerja'),
		('02', 'Nelayan'),
		('03', 'Petani'),
		('04', 'Peternak'),
		('05', 'PNS/TNI/Polri'),
		('06', 'Karyawan Swasta'),
		('07', 'Pedagang Kecil'),
		('08', 'Pedagang Besar'),
		('09', 'Wiraswasta'),
		('10', 'Wirausaha'),
		('11', 'Buruh'),
		('12', 'Pensiunan'),
		('99', 'Lainnya'),
	], string="Pekerjaan Ibu", default="01")	
	mother_income = fields.Selection([
		('01', '< Rp.500.000'),
		('02', 'Rp.500.000 - Rp.999.999'),
		('03', 'Rp.1.000.000 - Rp.1.999.999'),
		('04', 'Rp.2.000.000 - Rp.4.999.999'),
		('05', 'Rp.5.000.000 - Rp.20.000.000'),
		('06', '> Rp.20.000.000'),
		('07', 'Tidak Berpenghasilan'),
	], string="Penghasilan Ibu", default="01")	

	guardian_name = fields.Char(string="Nama Wali")
	guardian_nik = fields.Char(string="NIK Wali")
	guardian_birth_year = fields.Integer(string="Tahun Lahir Wali")
	guardian_education = fields.Selection([
		('01', 'Tidak Sekolah'),
		('02', 'Putus SD'),
		('03', 'SD Sederajat'),
		('04', 'SMP Sederajat'),
		('05', 'SMA Sederajat'),
		('06', 'D1'),
		('07', 'D2'),
		('08', 'D3'),
		('09', 'D4/S1'),
		('10', 'S2'),
		('11', 'S3'),
		('99', 'Lainnya')
	], string="Pendidikan Wali", default="01")
	guardian_work = fields.Selection([
		('01', 'Tidak Bekerja'),
		('02', 'Nelayan'),
		('03', 'Petani'),
		('04', 'Peternak'),
		('05', 'PNS/TNI/Polri'),
		('06', 'Karyawan Swasta'),
		('07', 'Pedagang Kecil'),
		('08', 'Pedagang Besar'),
		('09', 'Wiraswasta'),
		('10', 'Wirausaha'),
		('11', 'Buruh'),
		('12', 'Pensiunan'),
		('99', 'Lainnya')
	], string="Pekerjaan Wali", default="01")	
	guardian_income = fields.Selection([
		('01', '< Rp.500.000'),
		('02', 'Rp.500.000 - Rp.999.999'),
		('03', 'Rp.1.000.000 - Rp.1.999.999'),
		('04', 'Rp.2.000.000 - Rp.4.999.999'),
		('05', 'Rp.5.000.000 - Rp.20.000.000'),
		('06', '> Rp.20.000.000'),
		('07', 'Tidak Berpenghasilan'),
	], string="Penghasilan Wali", default="01")	

	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", compute="get_current_class", store=True)
	class_ids = fields.Many2many("asm.classes")
	current_class = fields.Char(string="Kelas Saat Ini", compute="get_current_class", store=True)
	national_exam_number = fields.Char(string="Nomor Peserta UN SMP/MTs")
	diploma_number = fields.Char(string="Nomor Seri Ijazah SMP/MTs")
	receive_kip = fields.Selection([('1', 'Ya'), ('0', 'Tidak')], string="Menerima KIP", default="0")
	kip_number = fields.Char(string="Nomor KIP")
	kip_behalf_name = fields.Char(string="Nama di KIP")
	kks_number = fields.Char(string="Nomor KKS")
	birth_cert_number = fields.Char(string="No. Registrasi Akta Lahir")
	bank = fields.Char(string="Bank")
	bank_account_number = fields.Char(string="Nomor Rekening Bank")
	bank_behalf_name = fields.Char(string="Rekening Atas Nama")
	needs_pip = fields.Selection([('1', 'Ya'), ('0', 'Tidak')], string="Layak PIP", default="0")	
	reason_need_pip = fields.Char(string="Alasan Layak PIP")
	special_needs = fields.Selection([
		('none', 'Tidak Ada'),
		('a', 'Netra'),
		('b', 'Rungu'),
		('c', 'Grahita Ringan'),
		('c1', 'Grahita Sedang'),
		('d', 'Daksa Ringan'),
		('d1', 'Daksa Sedang'),
		('e', 'Laras'),
		('f', 'Wicara'),
		('g', 'Tuna Ganda'),
		('h', 'Hiper Aktif'),
		('i', 'Cerdas Istimewa'),
		('j', 'Bakat Istimewa'),
		('k', 'Kesulitan Belajar'),
		('n', 'Narkoba'),
		('o', 'Indigo'),
		('p', 'Down Syndrome'),
		('q', 'Autisme')
	], string="Kebutuhan Khusus", default="none")
	previous_school = fields.Char(string="Sekolah Asal")
	child_number = fields.Integer(string="Anak Ke-", default=1)
	latitude = fields.Float(string="Lintang", default=0)
	longitude = fields.Float(string="Bujur", default=0)
	kk = fields.Char(string="No. KK")
	weight = fields.Char(string="Berat Badan")
	height = fields.Char(string="Tinggi Badan")
	head_circumference = fields.Char(string="Lingkar Kepala")
	sibling_count = fields.Integer(string="Jumlah Saudara Kandung", default=0)
	spp_monthly = fields.Integer(string="SPP/Bulan", default=0)
	spp_total = fields.Integer(string="Total SPP", compute="get_total_spp", store=True)
	base_dpp = fields.Integer(string="Uang Pendidikan Dasar", default=0)
	## Uang Pengembangan 
	base_kembang = fields.Integer(string="Uang Pengembangan", default=0)
	development_price = fields.Integer(string="Uang Gedung", default=0)
	reregistration_price = fields.Integer(string="Uang Daftar Ulang", default=0)
	## Buku Paket
	book_price = fields.Integer(string="Uang Buku Paket", default=0)
	form_price = fields.Integer(string="Uang Formulir", default=0)
	dpp_total = fields.Integer(string="Total Uang Pendidikan Dasar", compute="get_dpp_total", store=True)
	unpaid_spp = fields.Integer(string="Tunggakan SPP Saat Ini", default=0)

	state = fields.Selection([
		('registered', 'Calon Siswa'),
		('active', 'Siswa'),
		('inactive', 'Batal'),
		('graduate', 'Lulus'),
		('mutation', 'Mutasi')
	], string="Status Kesiswaan", default="registered")
	company_id = fields.Many2one("res.company", ondelete="set null", string="Instansi", compute="get_company", store=True)

	@api.one
	@api.depends("stage")
	def get_company(self):
		if self.stage:
			stage = self.stage[2:]
			if stage == 'PG' or stage == 'TK':
				self.company_id = self.env['res.company'].search([('name', '=', 'PG TK Anugerah School')], limit=1)
			elif stage == 'SD':
				self.company_id = self.env['res.company'].search([('name', '=', 'SD Anugerah School')], limit=1)
			elif stage == 'SMP':
				self.company_id = self.env['res.company'].search([('name', '=', 'SMP Anugerah School')], limit=1)
			else:
				self.company_id = None

	@api.one
	def add_unpaid(self):
		if self.unpaid_spp > 0:
			self.write({
				'unpaid_spp': 0
			})
		else:
			self.write({
				'unpaid_spp': self.spp_monthly
			})

	@api.one
	@api.depends("spp_monthly")
	def get_total_spp(self):
		self.spp_total = self.spp_monthly * 12

	@api.one
	@api.depends("base_dpp", "base_kembang", "development_price", "reregistration_price", "book_price")
	def get_dpp_total(self):
		self.dpp_total = self.base_dpp + self.base_kembang +self.development_price + self.reregistration_price + self.book_price

	@api.one
	@api.depends("class_ids")
	def get_current_class(self):
		array = []
		if self.class_ids:
			for i in self.class_ids:
				array.append(i.name)
			classes = self.env['asm.classes'].search([('name', 'in', array)], order="stage,name asc")

			if classes:
				for i in classes:
					self.current_class = i.name
					self.stage = i.stage
		else:
			self.current_class = "Not Assigned to a Class."
			self.stage = None

	@api.model
	def create(self, values):
		res = super(MasterStudent, self).create(values)
		student_payment = self.env['ir.module.module'].search([('name', '=', 'anugrah_school_payment')])
		if student_payment.state == "installed" and res['state'] == 'active':
			sp = self.env['asp.student_payments'].create({
				'student_payment_code': None,
				'student_id': res['id'],
				'student_nipd': None,
				'form_returned_date': date.today(),
				'stage': None,
				'current_class': None,
				'term': date.today().strftime("%Y"),
				'bank_account_number': None,
				'spp_monthly': res['spp_monthly'],
				'spp_total': None,
				'dpp_total': None,
				'development_total': None,
				'reregistration_total': None,
				'book_total': None,
				'form_total': None,
				'spp_paid': None,
				'dpp_paid': None,
				'development_paid': None,
				'reregistration_paid': None,
				'book_paid': None,
				'form_paid': None,
				'spp_unpaid': None,
				'dpp_unpaid': None,
				'development_unpaid': None,
				'reregistration_unpaid': None,
				'book_unpaid': None,
				'form_unpaid': None,
				'payment_record_ids': {}
			})
		return res

	@api.multi
	def write(self, values):
		res = super(MasterStudent, self).write(values)
		sp = self.env['ir.module.module'].search([('name', '=', 'anugrah_school_payment')])
		if sp.state == "installed":
			student_payment = self.env['asp.student_payments'].search([('student_id', '=', self.id)], limit=1)
			if student_payment:
				student_payment.spp_monthly = self.spp_monthly
			if not student_payment and self.state == 'active':
				rec = self.env['asp.student_payments'].create({
					'student_payment_code': None,
					'student_id': self.id,
					'student_nipd': None,
					'form_returned_date': date.today(),
					'stage': None,
					'current_class': None,
					'term': date.today().strftime("%Y"),
					'bank_account_number': None,
					'spp_monthly': self.spp_monthly,
					'spp_total': None,
					'dpp_total': None,
					'spp_paid': None,
					'dpp_paid': None,
					'spp_unpaid': None,
					'dpp_unpaid': None,
					'payment_record_ids': {}
				})
		return res

	_sql_constraints = [
		('nias_unique', 'unique(nias)', "NIPD value already exists. It must be unique number."),
		('nisn_unique', 'unique(nisn)', "NISN value already exists. It must be unique number.")
	]

	# citizenship = fields.Selection([('WNI', 'Indonesia (WNI)'), ('WNA', 'Asing (WNA)')], string="Kewarganegaraan", default="WNI")
	# country = fields.Char(string="Nama Negara")

	# welfare_type = fields.Selection([
	# 	('01', 'PKH'),
	# 	('02', 'PIP'),
	# 	('03', 'Kartu Perlindungan Sosial'),
	# 	('04', 'Kartu Keluarga Sejahtera'),
	# 	('05', 'Kartu Kesehatan')
	# ], string="Jenis Kesejahteraan", default="01")
	# welfare_card_number = fields.Integer(string="Nomor Kartu")
	# welfare_behalf = fields.Char(string="Nama di Kartu")
	# skill_major = fields.Char(string="Kompetensi Keahlian")
	# registration_type = fields.Selection([
	# 	('01', 'Siswa Baru'),
	# 	('02', 'Pindahan'),
	# 	('03', 'Kembali Bersekolah')
	# ], string="Jenis Pendaftaran", default="01")
	# entry_date = fields.Date(string="Tanggal Masuk Sekolah")
	# distance_to_school = fields.Selection([('01', 'Kurang dari 1KM'), ('02', 'Lebih dari 1KM')], string="Jarak Rumah ke Sekolah")
	# distance = fields.Integer(string="Jarak (KM)")
	# time_to_school_hour = fields.Integer(string="Waktu Tempuh Ke Sekolah (Jam)")
	# time_to_school_minute = fields.Integer(string="Waktu Tempuh Ke Sekolah (Menit)")
	# mother_special_needs = fields.Selection([
	# 	('none', 'Tidak Ada'),
	# 	('a', 'Netra'),
	# 	('b', 'Rungu'),
	# 	('c', 'Grahita Ringan'),
	# 	('c1', 'Grahita Sedang'),
	# 	('d', 'Daksa Ringan'),
	# 	('d1', 'Daksa Sedang'),
	# 	('e', 'Laras'),
	# 	('f', 'Wicara'),
	# 	('g', 'Tuna Ganda'),
	# 	('h', 'Hiper Aktif'),
	# 	('i', 'Cerdas Istimewa'),
	# 	('j', 'Bakat Istimewa'),
	# 	('k', 'Kesulitan Belajar'),
	# 	('n', 'Narkoba'),
	# 	('o', 'Indigo'),
	# 	('p', 'Down Syndrome'),
	# 	('q', 'Autisme')
	# ], string="Kebutuhan Khusus Ibu", default="none")
	# father_special_needs = fields.Selection([
	# 	('none', 'Tidak Ada'),
	# 	('a', 'Netra'),
	# 	('b', 'Rungu'),
	# 	('c', 'Grahita Ringan'),
	# 	('c1', 'Grahita Sedang'),
	# 	('d', 'Daksa Ringan'),
	# 	('d1', 'Daksa Sedang'),
	# 	('e', 'Laras'),
	# 	('f', 'Wicara'),
	# 	('g', 'Tuna Ganda'),
	# 	('h', 'Hiper Aktif'),
	# 	('i', 'Cerdas Istimewa'),
	# 	('j', 'Bakat Istimewa'),
	# 	('k', 'Kesulitan Belajar'),
	# 	('n', 'Narkoba'),
	# 	('o', 'Indigo'),
	# 	('p', 'Down Syndrome'),
	# 	('q', 'Autisme')
	# ], string="Kebutuhan Khusus Ayah", default="none")
	# has_kip = fields.Selection([('1', 'Ya'), ('0', 'Tidak')], string="Punya KIP", default="0")
	# reason_pip_denied = fields.Selection([('01', 'Dilarang Pemda Karena Menerima Bantuan Serupa'), ('02', 'Menolak'), ('03', 'Sudah Mampu')], string="Alasan Menolak PIP", default="0")	
