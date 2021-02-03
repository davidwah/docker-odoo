from odoo import api, fields, models, exceptions
from datetime import date, datetime, timedelta

class StudentPayment(models.Model):
	_name = "asp.student_payments"
	_rec_name = "student_id"

	student_payment_code = fields.Char(string="Kode Pembayaran Siswa", readonly=True)
	student_id = fields.Many2one("asm.students", ondelete="cascade")
	student_nipd = fields.Char(string="NIPD", compute="get_student_detail", store=True)
	form_returned_date = fields.Date(string="Tanggal Pengembalian Formulir")
	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", compute="get_student_detail", store=True)
	current_class = fields.Char(string="Kelas", compute="get_student_detail", store=True)
	term = fields.Char(string="Tahun Ajaran", required=True)
	bank_account_number = fields.Char(string="Nomor Rekening Bank", related="student_id.bank_account_number")
	spp_monthly = fields.Integer(string="SPP/Bulan")
	spp_total = fields.Integer(string="Total SPP", compute="get_spp_total", store=True)
	dpp_total = fields.Integer(string="Total Uang Pendidikan Dasar", related="student_id.base_dpp")
	## Uang Pengembangan
	kembang_total = fields.Integer(string="Total Uang Pengembangan", related="student_id.base_kembang")
	development_total = fields.Integer(string="Total Uang Gedung", related="student_id.development_price")
	reregistration_total = fields.Integer(string="Total Biaya Daftar Ulang", related="student_id.reregistration_price")
	## Buku Paket 
	book_total = fields.Integer(string="Total Biaya Buku Paket", related="student_id.book_price")
	form_total = fields.Integer(string="Total Biaya Formulir", related="student_id.form_price")
	spp_paid = fields.Integer(string="SPP Terbayar", compute="get_paid_spp", store=True)
	dpp_paid = fields.Integer(string="Uang Pendidikan Dasar Terbayar", compute="get_paid_dpp", store=True)
	## Uang Pengembangan
	kembang_paid = fields.Integer(string="Uang Pengembangan Terbayar", compute="get_paid_kembang", store=True)
	development_paid = fields.Integer(string="Uang Gedung Terbayar", compute="get_paid_development", store=True)
	reregistration_paid = fields.Integer(string="Biaya Daftar Ulang Terbayar", compute="get_paid_reregistration", store=True)
	## Buku Paket
	book_paid = fields.Integer(string="Biaya Buku Paket Terbayar", compute="get_paid_book", store=True)
	form_paid = fields.Integer(string="Biaya Formulir Terbayar", compute="get_paid_form", store=True)
	spp_unpaid = fields.Integer(string="SPP Belum Bayar", compute="get_unpaid_spp", store=True)
	dpp_unpaid = fields.Integer(string="Uang Pendidikan Dasar Belum Bayar", compute="get_unpaid_dpp", store=True)
	## Uang Pengembangan
	kembang_unpaid = fields.Integer(string="Uang Pengembangan Belum Bayar", compute="get_unpaid_kembang", store=True)
	development_unpaid = fields.Integer(string="Uang Gedung Belum Bayar", compute="get_unpaid_development", store=True)
	reregistration_unpaid = fields.Integer(string="Biaya Daftar Ulang Belum Bayar", compute="get_unpaid_reregistration", store=True)
	## Buku Paket
	book_unpaid = fields.Integer(string="Biaya Buku Paket Belum Bayar", compute="get_unpaid_book", store=True)
	form_unpaid = fields.Integer(string="Biaya Formulir Belum Bayar", compute="get_unpaid_form", store=True)
	payment_record_ids = fields.One2many("asp.payment_records", "student_payment_id", store=True)
	file = fields.Binary(string="Upload")
	filename = fields.Char(string="File Name")

	@api.one
	@api.depends("student_id", "spp_monthly")
	def get_student_detail(self):
		self.student_nipd = self.student_id.nipd
		self.current_class = self.student_id.current_class
		self.stage = self.student_id.stage

	@api.one
	@api.depends("student_id", "spp_monthly")
	def get_spp_total(self):
		payment_records = self.env['asp.payment_records'].search_count([('student_id', '=', self.student_id.id), ('state', '=', 'spp'), ('student_class', '=', self.student_id.current_class)])
		if payment_records == 0:
			self.spp_total = 12 * self.student_id.spp_monthly
		else:
			payment_made = self.env['asp.payment_records'].search_count([('student_id', '=', self.student_id.id), ('state', '=', 'spp'), ('spp_base', '!=', self.student_id.spp_monthly), ('student_class', '=', self.student_id.current_class)])
			self.spp_total = (12 - payment_made) * self.student_id.spp_monthly

	@api.model
	def create(self, values):
		res = super(StudentPayment, self).create(values)
		now = date.today().strftime("%Y%m%d")
		res["student_payment_code"] = "%dSP/%d%s" % (res['id'], res["student_id"]["id"], now)
		return res

	@api.one
	@api.depends("payment_record_ids", "current_class")
	def get_paid_spp(self):
		total = 0
		for i in self.payment_record_ids:
			if i.state == "spp":
				if i.student_class == self.current_class:
					total += i.payment_value
		self.spp_paid = total

	@api.one
	@api.depends("payment_record_ids")
	def get_paid_dpp(self):
		total = 0
		for i in self.payment_record_ids:
			if i.state == "dpp":
				if i.student_class == self.current_class:
					total += i.payment_value
		self.dpp_paid = total
	
	## Uang Pengembangan
	@api.one
	@api.depends("payment_record_ids")
	def get_paid_kembang(self):
		total = 0
		for i in self.payment_record_ids:
			if i.state == "kembang":
				if i.student_class == self.current_class:
					total += i.payment_value
		self.kembang_paid = total

	@api.one
	@api.depends("payment_record_ids")
	def get_paid_development(self):
		total = 0
		for i in self.payment_record_ids:
			if i.state == "development":
				if i.student_class == self.current_class:
					total += i.payment_value
		self.development_paid = total

	@api.one
	@api.depends("payment_record_ids")
	def get_paid_reregistration(self):
		total = 0
		for i in self.payment_record_ids:
			if i.state == "reregister":
				if i.student_class == self.current_class:
					total += i.payment_value
		self.reregistration_paid = total

	## book_paid - Buku Paket
	@api.one
	@api.depends("payment_record_ids")
	def get_paid_book(self):
		total = 0
		for i in self.payment_record_ids:
			if i.state == "book":
				if i.student_class == self.current_class:
					total += i.payment_value
		self.book_paid = total

	@api.one
	@api.depends("payment_record_ids")
	def get_paid_form(self):
		total = 0
		for i in self.payment_record_ids:
			if i.state == "form":
				if i.student_class == self.current_class:
					total += i.payment_value
		self.form_paid = total

	@api.one
	@api.depends("spp_paid")
	def get_unpaid_spp(self):
		self.spp_unpaid = self.spp_total - self.spp_paid

	@api.one
	@api.depends("dpp_paid")
	def get_unpaid_dpp(self):
		self.dpp_unpaid = self.dpp_total - self.dpp_paid
	
	## Uang Pengembangan
	@api.one
	@api.depends("kembang_paid")
	def get_unpaid_kembang(self):
		self.kembang_unpaid = self.kembang_total - self.kembang_paid

	@api.one
	@api.depends("development_paid")
	def get_unpaid_development(self):
		self.development_unpaid = self.development_total - self.development_paid

	@api.one
	@api.depends("reregistration_paid")
	def get_unpaid_reregistration(self):
		self.reregistration_unpaid = self.reregistration_total - self.reregistration_paid

	## book_unpaid - Buku Paket
	@api.one
	@api.depends("book_paid")
	def get_unpaid_book(self):
		self.book_unpaid = self.book_total - self.book_paid

	@api.one
	@api.depends("form_paid")
	def get_unpaid_form(self):
		self.form_unpaid = self.form_total - self.form_paid

class ItemLines(models.Model):
	_name = "asp.item_lines"
	_rec_name = "inventory_id"

	inventory_id = fields.Many2one("asm.inventories", ondelete="set null")
	inventory_quantity = fields.Integer(string="Stok Tersedia", related="inventory_id.quantity")
	price = fields.Integer(string="Harga/Unit", required=True, default=0)
	quantity = fields.Integer(string="Jumlah Unit", required=True, default=0)
	tax = fields.Integer(string="Pajak (%)", default=0)
	subtotal = fields.Integer(string="Subtotal", compute="get_subtotal", store=True)
	expense_id = fields.Many2one("asp.payment_expenses", ondelete="cascade")
	payment_record_id = fields.Many2one("asp.payment_records", ondelete="cascade")

	@api.one
	@api.depends("price", "quantity", "tax")
	def get_subtotal(self):
		tax = (100 + self.tax) / 100
		self.subtotal = int(self.price * self.quantity * tax)

class Expense(models.Model):
	_name ="asp.payment_expenses"
	_rec_name = "transaction_code"

	transaction_code = fields.Char(string="Kode Transaksi", readonly=True)
	expense_category = fields.Selection([
		('hardware', 'Pembelian Barang Penunjang Sekolah'),
		('payroll', 'Gaji Karyawan/Guru/Lain-lain'),
		('electrical', 'Listrik Bulanan'),
		('internet', 'Internet Bulanan'),
		('renovation', 'Renovasi Gedung'),
		('other', 'Pengeluaran Lain-lainnya')
	], string="Kategori Pengeluaran", default="hardware", required=True)
	item_ids = fields.One2many("asp.item_lines", "expense_id")
	hardware_value = fields.Integer(string="Total Pembayaran", compute="get_total_payment", store=True)
	other_value = fields.Integer(string="Total Pembayaran")
	payment_value = fields.Integer(string="Total Biaya", compute="get_grand_total", store=True)
	payment_date = fields.Date(string="Tanggal Pembelian", readonly=True, default=lambda *a: (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%d"))
	price_cut = fields.Integer(string="Potongan Harga", default=0)
	discount = fields.Integer(string="Diskon (%)", default=0)
	file = fields.Binary(string="Upload")
	filename = fields.Char(string="File Name")
	note = fields.Text(string="Keterangan")
	receiver = fields.Char(string="Nama Penerima Uang", required=True)
	created_by = fields.Many2one("res.users", ondelete="set null", default=lambda self: self.env.user)
	stage = fields.Selection([
		(None, ""),
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", default=None)
	confirmation = fields.Boolean(string="Confirmation", required=True)
	
	@api.constrains('confirmation')
	def check_confirmation(self):
		if self.confirmation:
			return True
		else:
			return False

	_constraints = [(check_confirmation, "Harap centang persetujuan di paling bawah form.", ['confirmation'])]

	@api.one
	@api.depends("hardware_value", "other_value")
	def get_grand_total(self):
		if self.hardware_value > 0:
			self.payment_value = self.hardware_value
		if self.other_value > 0:
			self.payment_value = self.other_value

	@api.one
	@api.depends("item_ids", "price_cut", "discount")
	def get_total_payment(self):
		total = 0
		for i in self.item_ids:
			total += i.subtotal
		if self.discount > 0:
			discount = (100 - self.discount) / 100
			total = int(total * discount)
		if self.price_cut > 0:
			total -= self.price_cut
		self.hardware_value = total

	@api.model
	def create(self, values):
		res = super(Expense, self).create(values)
		now = date.today().strftime("%y%m")
		zId = str(res['id']).zfill(6)
		res["transaction_code"] = "00%s%s01" % (now, zId)
		finance = self.env['asm.finances'].create({
			'payment_record_id': None,
			'payment_expense_id': res['id'],
			'payment_code': None,
			'payment_date': res['payment_date'],
			'note': None,
			'income': None,
			'outcome': None,
			'balance': None,
			'stage': res['stage'],
		})
		if len(res['item_ids']) > 0 and res['expense_category'] == 'hardware':
			for i in res['item_ids']:
				i.inventory_id.quantity += i.quantity
				history = self.env['asi.history'].create({
					'name': "%s (%s)" % (i.inventory_id.name, i.inventory_id.stage[2:]),
					'date': date.today(),
					'state': 'in',
					'stage': res['stage'],
					'quantity': i.quantity
				})
		return res

class PaymentRecord(models.Model):
	_name = "asp.payment_records"
	_rec_name = "transaction_code"

	transaction_code = fields.Char(string="Kode Transaksi", readonly=True)
	student_id = fields.Many2one("asm.students", ondelete="set null", domain="[('state', 'in', ['active', 'registered'])]")
	student_class = fields.Char(string="Kelas Siswa", compute="get_student_detail", store=True)
	student_nipd = fields.Char(string="NIPD", compute="get_student_detail", store=True)
	student_payment_id = fields.Many2one("asp.student_payments", ondelete="cascade", compute="get_student_payment", store=True)
	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", compute="get_student_detail", store=True)
	
	payment_value = fields.Integer(string="Nominal Pembayaran", required=True)
	preview_value = fields.Integer(string="Preview Nominal", compute="process_value")
	payment_date = fields.Date(string="Tanggal Pembayaran", default=lambda *a: (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%d"))
	state = fields.Selection([
		('spp', 'SPP'),
		('dpp', 'UPD'),
		('kembang', 'Uang Pengembangan'),
		('development', 'Uang Gedung'),
		('form', 'Pembelian Formulir'),
		('reregister', 'Daftar Ulang'),
		('book', 'Buku Paket'),
		('bos', 'Bantuan Operasional Sekolah'),
		('unas', 'Pembayaran Ujian Nasional (KHUSUS KELAS 6)'),
		('trip', 'Field Trip Siswa'),
		('hardware', 'Perlengkapan & Seragam Sekolah'),
		('extra', 'Extra'),
		('canteen', 'Setoran Kantin'),
		('kawai', 'Kawai Piano'),
		('other', 'Lain-lainnya')
	], string="Jenis Pembayaran", default="spp", required=True)
	note = fields.Text(string="Keterangan")
	receiver = fields.Char(string="Nama Penerima Uang", required=True, default="Anugerah School Sidoarjo")
	created_by = fields.Many2one("res.users", ondelete="set null", default=lambda self: self.env.user)

	spp_month = fields.Selection([
		('January', 'Januari'),
		('February', 'Februari'),
		('March', 'Maret'),
		('April', 'April'),
		('May', 'Mei'),
		('June', 'Juni'),
		('July', 'Juli'),
		('August', 'Agustus'),
		('September', 'September'),
		('October', 'Oktober'),
		('November', 'November'),
		('December', 'Desember')
	], string="Periode SPP (Bulan)", default=lambda self: self.get_current_month())
	spp_year = fields.Char(string="Periode SPP (Tahun)", default=lambda self: self.get_current_year())
	spp_base = fields.Integer(string="SPP/Bulan Siswa", compute="get_base_spp", store=True)
	spp_final_spp_value = fields.Integer(string="Total Pembayaran SPP", compute="get_final_spp", store=True, help="Total yang harus dibayar untuk bulan ini. Sudah termasuk SPP Pokok dan tunggakan bulan sebelumnya.")
	spp_payment_type = fields.Selection([
		('auto', 'Autodebet'),
		('debit', 'Debit'),
		('cash', 'Tunai'),
		('transfer', 'Transfer ATM')
	], string="Cara Pembayaran", default="auto", required=True)
	spp_unpaid_value = fields.Integer(string="Tunggakan", compute="get_current_unpaid", store=True)
	spp_late_fine = fields.Integer(string="Denda Keterlambatan")
	spp_cash_fine = fields.Integer(string="Denda Pembayaran Tunai")

	dpp_payment_number = fields.Integer(string="Cicilan Ke-", compute="get_payment_number", store=True)
	## Uang Pengembangan
	kembang_payment_number = fields.Integer(string="Cicilan Ke-", compute="get_payment_number", store=True)

	item_ids = fields.One2many('asp.item_lines', 'payment_record_id')
	confirmation = fields.Boolean(string="Confirmation", required=True)

	@api.one
	@api.depends("payment_value")
	def process_value(self):
		self.preview_value = self.payment_value

	@api.one
	@api.depends("student_id")
	def get_student_detail(self):
		self.student_class = self.student_id.current_class
		self.student_nipd = self.student_id.nipd
		self.stage = self.student_id.stage

	@api.model
	def get_current_month(self):
		return date.today().strftime("%B")

	@api.model
	def get_current_year(self):
		return date.today().strftime("%Y")

	@api.one
	@api.depends("student_id")
	def get_base_spp(self):
		self.spp_base = self.student_id.spp_monthly

	@api.one
	@api.depends("student_payment_id")
	def get_final_spp(self):
		self.spp_final_spp_value = self.student_id.unpaid_spp

	@api.model
	def create(self, values):
		res = super(PaymentRecord, self).create(values)
		if res['student_id']['state'] in ['registered', 'active']:
			if res['state'] in ['form', 'development', 'spp', 'dpp', 'kembang' , 'reregister', 'book', 'unas', 'trip']:
				res['student_id']['state'] = 'active'
		zId = str(res['id']).zfill(8)
		insignia = "1"
		if res['state'] == 'spp':
			record = self.env['asp.unpaid_spp_students'].search([('student_payment_id', '=', res['student_payment_id']['id'])], limit=1)
			res['student_id']['unpaid_spp'] = res['spp_unpaid_value']
			if res['spp_unpaid_value'] > 0:
				if record:
					record.unlink()
				insignia += "2"
			elif res['spp_unpaid_value'] == 0:
				if record:
					record.unlink()
				insignia += "1"
			else:
				if record:
					record.unlink()
				insignia += "1"
		else:
			insignia += "0"
		res["transaction_code"] = "%s%s" % (insignia, zId)
		finance = self.env['asm.finances'].create({
			'payment_record_id': res['id'],
			'payment_expense_id': None,
			'payment_code': None,
			'payment_date': res['payment_date'],
			'note': None,
			'income': None,
			'outcome': None,
			'balance': None,
			'stage': res['stage'],
		})
		if res["state"] == "hardware":
			for i in res["item_ids"]:
				i.inventory_id.quantity -= i.quantity
				history = self.env['asi.history'].create({
					'name': i.inventory_id.name,
					'date': date.today(),
					'state': 'out',
					'stage': res['stage'],
					'quantity': i.quantity
				})
		return res

	@api.one
	@api.depends("student_id", "state")
	def get_payment_number(self):
		records = self.env["asp.payment_records"].search([('student_id', '=', self.student_id.id), ('state', '=', 'dpp'), ('student_class', '=', self.student_class)], order="id desc")
		record = None
		for i in records:
			if i.state == 'dpp':
				record = i
		if record is not None:
			self.dpp_payment_number = record.dpp_payment_number + 1
		else:
			self.dpp_payment_number = 1
	
	## Uang Pengembangan
	@api.one
	@api.depends("student_id", "state")
	def get_payment_number(self):
		records = self.env["asp.payment_records"].search([('student_id', '=', self.student_id.id), ('state', '=', 'kembang'), ('student_class', '=', self.student_class)], order="id desc")
		record = None
		for i in records:
			if i.state == 'kembang':
				record = i
		if record is not None:
			self.kembang_payment_number = record.kembang_payment_number + 1
		else:
			self.kembang_payment_number = 1

	@api.one
	@api.depends("student_id")
	def get_student_payment(self):
		if not self.student_id:
			pass
		else:
			records = self.env['asp.student_payments'].search([('student_id', '=', self.student_id.id)])
			if not records:
				self.student_payment_id = self.env['asp.student_payments'].create({
					'student_id': self.student_id.id,
					'student_nipd': None,
					'form_returned_date': date.today().strftime('%Y-%m-%d'),
					'stage': None,
					'current_class': None,
					'term': date.today().strftime('%Y'),
					'bank_account_number': None,
					'spp_total': None,
					'dpp_total': None,
					'kembang_total': None,
					'spp_paid': None,
					'dpp_paid': None,
					'kembang_paid': None,
					'spp_unpaid': None,
					'dpp_unpaid': None,
					'kembang_unpaid': None,
					'payment_record_ids': {}
				})
			else:
				self.student_payment_id = records

	@api.one
	@api.depends("spp_final_spp_value", "payment_value")
	def get_current_unpaid(self):
		self.spp_unpaid_value = self.spp_final_spp_value - self.payment_value

	@api.constrains('confirmation')
	def check_confirmation(self):
		if self.confirmation:
			return True
		else:
			return False

	_constraints = [(check_confirmation, "Harap centang persetujuan di paling bawah form.", ['confirmation'])]