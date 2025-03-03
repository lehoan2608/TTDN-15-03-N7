from odoo import models, fields

class Expenses(models.Model):
    _name = 'expenses'
    _description = 'Chi phí thực tế'

    # budgets_id = fields.Many2one('budgets', string='Ngân Sách')
    # expenses_name = fields.Char(string='Mô Tả Chi Phí')
    # amount = fields.Float(string='Số Tiền')
    # date = fields.Date(string='Ngày Chi')

    expenses_name = fields.Char(string="Tên Khoản Chi", required=True)
    projects_id = fields.Many2one('projects', string="Dự án", ondelete='cascade')
    budgets_id = fields.Many2one('budgets', string="Ngân sách")
    amount = fields.Float(string="Số tiền", required=True)
    date = fields.Date(string="Ngày chi tiêu", required=True, default=fields.Date.today)
