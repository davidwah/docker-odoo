# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ASMInventory(models.Model):
	_name = 'asm.inventories'

	name = fields.Char(string="Nama Barang", required=True)
	quantity = fields.Integer(string="Stok Barang", default=0)
	sell_price = fields.Integer(string="Harga Jual", default=0)
	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", default="1 PG")

	@api.model
	def create(self, values):
		res = super(ASMInventory, self).create(values)
		res['name'] = res['name'].upper()
		return res

	@api.multi
	def name_get(self):
	    result = []
	    for record in self:
	        name = "%s (%s)" % (record.name, record.stage.upper())
	        result.append((record.id, name))
	    return result

class InventoryHistory(models.Model):
	_name = "asi.history"

	name = fields.Char(string="Nama Barang", required=True)
	date = fields.Date(string="Tanggal Riwayat", required=True)
	state = fields.Selection([
		('no', 'None'),
		('in', 'Barang Masuk'),
		('out', 'Barang Keluar')
	], string="Jenis Riwayat", default="none")
	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", default="1 PG")
	quantity = fields.Integer(string="Jumlah")

class InventoryWizard(models.TransientModel):
	_name = "asw.inventories"

	start_date = fields.Date(string="Tanggal Awal", required=True)
	end_date = fields.Date(string="Tanggal Akhir", required=True)
	stage = fields.Selection([
		("1 PG", "PG"),
		("2 TK", "TK"),
		("3 SD", "SD"),
		("4 SMP", "SMP"),
	], string="Jenjang", default=None, required=True)

	@api.multi
	def get_report(self):
		data = {
			'ids': self.ids,
			'model': self._name,
			'form': {
				'date_start': self.start_date,
				'date_end': self.end_date,
				'stage': self.stage,
			},
		}
		return self.env.ref('anugrah_school_inventory.inventory_recap').report_action(self, data=data)

class InventoryReport(models.AbstractModel):
	_name = 'report.anugrah_school_inventory.inventory_recap_template'

	@api.model
	def _get_report_values(self, docids, data=None):
		date_start = data['form']['date_start']
		date_end = data['form']['date_end']
		stage = data['form']['stage']

		docs = []
		finances = self.env['asi.history'].search([('date', '>=', date_start), ('date', '<=', date_end), ('stage', '=', stage)])
		for i in finances:
			docs.append({
				'name': i.name,
				'date': i.date,
				'state': i.state,
				'stage': i.stage,
				'quantity': i.quantity,
			})

		return {
			'doc_ids': data['ids'],
			'doc_model': data['model'],
			'date_start': date_start,
			'date_end': date_end,
			'stage': stage,
			'docs': docs,
		}