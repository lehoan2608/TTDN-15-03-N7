from odoo import models, fields, api


class LichSuLamViec(models.Model):
    _name = 'lich_su_lam_viec'
    _description = 'Bảng chứa thông tin lịch sử làm việc'

    ten_cong_viec = fields.Char("Tên công việc đã làm", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ma_phong_ban = fields.Many2one('phong_ban', string="Phòng ban", required=True)
    
    def name_get(self):
        result = []
        for record in self:
            name = record.ten_cong_viec
            result.append((record.id, name))
        return result