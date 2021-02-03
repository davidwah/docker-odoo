from odoo import api, models, fields
from datetime import date

class Finances(models.Model):
	_name = "asm.finances"
	_rec_name = "payment_code"

	payment_record_id = fields.Many2one("asp.payment_records", ondelete="cascade")
	payment_expense_id = fields.Many2one("asp.payment_expenses", ondelete="cascade")
	state = fields.Selection([
		('in', 'Income'),
		('out', 'Outcome')
	], string="Tipe Transaksi", compute="get_state", store=True)
	payment_code = fields.Char(string="Kode Transaksi", compute="get_payment_code", store=True)
	payment_date = fields.Date(string="Tanggal Transaksi", readonly=True, compute="get_payment_date", store=True)
	note = fields.Char(string="Keterangan", compute="get_description", store=True)
	income = fields.Integer(string="Dana Masuk", compute="get_payment_value", store=True)
	outcome = fields.Integer(string="Dana Keluar", compute="get_payment_value", store=True)
	balance = fields.Integer(string="Saldo")
	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", default="1 PG")

	@api.multi
	def recalculate_balance(self):
		records = self.env['asm.finances'].search([])
		for i in records:
			if i.id == 1:
				i.balance = i.income - i.outcome
			else:
				previous = self.env['asm.finances'].search([('id', '<', i.id)], order="id desc", limit=1)
				i.balance = previous.balance + i.income - i.outcome

	@api.one
	@api.depends("payment_record_id", "payment_expense_id")
	def get_state(self):
		if self.payment_record_id:
			self.state = 'in'
		if self.payment_expense_id:
			self.state = 'out'

	@api.one
	@api.depends("payment_record_id", "payment_expense_id")
	def get_payment_code(self):
		if self.payment_record_id:
			self.payment_code = self.payment_record_id.transaction_code
		if self.payment_expense_id:
			self.payment_code = self.payment_expense_id.transaction_code

	@api.model
	def create(self, values):
		res = super(Finances, self).create(values)
		prev = self.env['asm.finances'].search([('id', '<', res['id'])], order="id desc", limit=1)
		res['balance'] = prev.balance + res['income'] - res['outcome']
		return res

	@api.one
	@api.depends("payment_record_id")
	def get_description(self):
		if self.payment_record_id:
			state = self.payment_record_id.state
			if state == "spp":
				self.note = "Pemasukan SPP"
			elif state == "dpp":
				self.note = "Pemasukan DPP"
			elif state == "form":
				self.note = "Pembayaran Form Registrasi"
			elif state == "development":
				self.note = "Pembayaran Uang Gedung"
			elif state == "reregister":
				self.note = "Uang Daftar Ulang"
			elif state == "book":
				self.note = "Pembayaran Buku Paket"
			elif state == "uniform":
				self.note = "Penjualan Seragam"
			elif state == "bos":
				self.note = "Dana Bantuan Operasional Sekolah"
			else:
				self.note = "Pemasukan Dana Lain"
		if self.payment_expense_id:
			state = self.payment_expense_id.expense_category
			if state == "hardware":
				self.note = "Pembelian Barang Penunjang Pembelajaran"
			elif state == "payroll":
				self.note = "Pembayaran Gaji Karyawan"
			elif state == "electrical":
				self.note = "Pembayaran Bulanan Listrik"
			elif state == "internet":
				self.note = "Pembayaran Bulanan Internet"
			else:
				self.note = "Pengeluaran Dana Lain"

	@api.one
	@api.depends("payment_record_id")
	def get_payment_value(self):
		if self.payment_record_id:
			if self.payment_record_id.spp_payment_type != 'cash':
				self.income = self.payment_record_id.payment_value
			else:
				self.income = self.payment_record_id.payment_value + self.payment_record_id.spp_cash_fine
			self.outcome = 0
		if self.payment_expense_id:
			self.outcome = self.payment_expense_id.payment_value
			self.income = 0

	@api.one
	@api.depends("payment_record_id", "payment_expense_id")
	def get_payment_date(self):
		if self.payment_record_id:
			self.payment_date = self.payment_record_id.payment_date
		if self.payment_expense_id:
			self.payment_date = self.payment_expense_id.payment_date

class FinanceWizard(models.TransientModel):
	_name = "asw.finances"

	start_date = fields.Date(string="Tanggal Awal", required=True)
	end_date = fields.Date(string="Tanggal Akhir", required=True)

	@api.multi
	def get_report(self):
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'date_start': self.start_date,
				'date_end': self.end_date,
			},
		}
		return self.env.ref('anugrah_school_payment.finance_recap').report_action(self, data=data)

class FinanceReport(models.AbstractModel):
	_name = 'report.anugrah_school_payment.finance_recap_template'

	@api.model
	def _get_report_values(self, docids, data=None):
		date_start = data['form']['date_start']
		date_end = data['form']['date_end']

		docs = []
		finances = self.env['asm.finances'].search([('payment_date', '>=', date_start), ('payment_date', '<=', date_end)])
		total_income, total_outcome = 0, 0

		for i in finances:
			docs.append({
				'state': i.state,
				'payment_code': i.payment_code,
				'payment_date': i.payment_date.strftime("%d-%m-%Y"),
				'income': '{0:,}'.format(i.income),
				'outcome': '{0:,}'.format(i.outcome),
				'note': i.note,
			})
			total_income += i.income
			total_outcome += i.outcome

		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'date_start': date_start,
			'date_end': date_end,
			'docs': docs,
			'total_income': '{0:,}'.format(total_income),
			'total_outcome': '{0:,}'.format(total_outcome)
		}