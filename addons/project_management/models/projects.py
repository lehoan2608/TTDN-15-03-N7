from odoo import models, fields, api
from datetime import date, datetime

class Projects(models.Model):
    _name = 'projects'
    _description = 'Quản lý dự án'

    projects_id = fields.Char("Mã dự án")
    projects_name = fields.Char("Tên dự án")
    
    manager_name = fields.Many2one('nhan_vien', string="Quản lý dự án")

    start_date = fields.Date("Ngày bắt đầu")
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
        string='Trạng thái', store=True
    )

    ly_do_1 = fields.Text(string="Lý do hủy bỏ", help="Lý do hủy bỏ công việc")

    # status_class = fields.Char(string='Status Class', compute='_compute_status_class', store=True)

    # @api.depends('status')
    # def _compute_status_class(self):
    #     for record in self:
    #         if record.status == 'not_started':
    #             record.status_class = 'status-not-started'
    #         elif record.status == 'in_progress':
    #             record.status_class = 'status-in-progress'
    #         elif record.status == 'completed':
    #             record.status_class = 'status-completed'
    #         elif record.status == 'delayed':
    #             record.status_class = 'status-delayed'
    #         elif record.status == 'cancelled':
    #             record.status_class = 'status-cancelled'
    #         else:
    #             record.status_class = ''

    # status_display = fields.Html(string="Status Display", compute="_compute_status_display", sanitize=False)


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

    # nhan_vien_ids = fields.Many2many('nhan_vien', string='Thành viên tham gia', help='Chọn các thành viên tham gia dự án')

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.projects_id}"

            result.append((record.id, name))
        return result
    
    budget_ids = fields.One2many('budgets', inverse_name='projects_id', string="Ngân sách Dự án")

    def action_view_task_chart(self):
        self.ensure_one()  # Đảm bảo phương thức chỉ xử lý một bản ghi
        return {
            'type': 'ir.actions.act_window',
            'name': 'Biểu Đồ Công Việc Công Việc',
            'res_model': 'taskss',
            'view_mode': 'graph',
            'domain': [('projects_id', '=', self.id)],  # Lọc công việc theo dự án hiện tại
            # Đặt giá trị mặc định cho trường projects_id
            'context': {'search_default_group_by_projects_id': self.id},
            'target': 'current',
        }