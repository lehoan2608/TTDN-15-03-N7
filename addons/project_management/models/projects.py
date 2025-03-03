from odoo import models, fields, api
from datetime import date, datetime

class Projects(models.Model):
    _name = 'projects'
    _description = 'Quản lý dự án'

    projects_id = fields.Char("Mã dự án", required=True)
    projects_name = fields.Char("Tên dự án", required=True)
    
    # manager_id = fields.Many2one(string="Quản lý dự án")

    start_date = fields.Date("Ngày bắt đầu")
    # end_date = fields.Date("Thời gian dự kiến hoàn thành")
    actual_end_date = fields.Date("Ngày kết thúc thực tế")

    progress = fields.Float("Tiến độ (%)", compute='_compute_progress', store=True)
    status = fields.Selection(
        selection=[
            ('not_started', 'Chưa bắt đầu'),
            ('in_progress', 'Đang thực hiện'),
            ('completed', 'Hoàn thành'),
            ('delayed', 'Trì hoãn'),
            ('cancelled', 'Hủy bỏ')
        ], 
        string='Trạng thái'
    )

    task_ids = fields.One2many('taskss', inverse_name='projects_id', String='Công việc') 

    @api.depends('start_date', 'actual_end_date')
    def _compute_progress(self):
        today = date.today()
        for project in self:
            if project.start_date and project.actual_end_date:
                total_days = (project.actual_end_date - project.start_date).days
                elapsed_days = (today - project.start_date).days

                if total_days > 0:
                    project.progress = max(0, min(100, (elapsed_days / total_days) * 100))
                else:
                    project.progress = 100 if today >= project.actual_end_date else 0
            else:
                project.progress = 0



    # Thiết lập mối quan hệ Many2many với model 'employees'
    employees_ids = fields.Many2many('employees', string='Thành viên tham gia', help='Chọn các thành viên tham gia dự án')

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.projects_id} - {record.projects_name}"
            result.append((record.id, name))
        return result
    


    # Thiết lập mối quan hệ với budgets và expenses
    budget_ids = fields.One2many('budgets', inverse_name='projects_id', string="Ngân sách Dự án")
    expense_ids = fields.One2many('expenses', inverse_name='projects_id', string="Chi phí Dự án")
