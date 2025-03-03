from odoo import models, fields, api
class PhongBan(models.Model):
    _name = 'phong_ban'
    _describe = 'Phòng ban của nhân viên'

    ma_phong_ban = fields.Char("Mã phòng ban", reuired=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)