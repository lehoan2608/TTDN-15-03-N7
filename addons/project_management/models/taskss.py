from datetime import date
from odoo import models, fields, api

class Taskss(models.Model):
    _name = 'taskss'
    _description = 'Quản lý công việc'

    taskss_name = fields.Char('Tên công việc',required=True)
    projects_id = fields.Many2one('projects', string='Dự án')

    # assigned_to = fields.Char('Người Phụ Trách')
    # Một công việc thuộc về một nhân viên
    assigned_to = fields.Many2one('employees', string='Người phụ trách')

    start_date = fields.Date('Ngày bắt đầu')
    deadline = fields.Date('Hạn Chót')

    priority = fields.Selection(
        selection=[
            ('low', 'Thấp'),
            ('medium', 'Trung bình'),
            ('high', 'Cao'),
        ],
    string = 'Mức độ ưu tiên'
    )

    progress = fields.Float('Tiến Độ (%)', compute='_compute_progress', store=True)

    status = fields.Selection(
        selection=[
            ('not_started', 'Chưa bắt đầu'),
            ('in_progress', 'Đang thực hiện'),
            ('completed', 'Hoàn thành'),
        ], 
        string='Trạng thái'
    )


    @api.depends('start_date', 'deadline')
    def _compute_progress(self):
        today = date.today()
        for project in self:
            if project.start_date and project.deadline:
                total_days = (project.deadline - project.start_date).days
                elapsed_days = (today - project.start_date).days

                if total_days > 0:
                    project.progress = max(0, min(100, (elapsed_days / total_days) * 100))
                else:
                    project.progress = 100 if today >= project.deadline else 0
            else:
                project.progress = 0