from odoo import models, fields, api
from datetime import date


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'
 
    nhan_vien_id = fields.Char("Nhân viên", required=True)
    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten = fields.Char("Họ và tên", compute='_tinh_ho_va_ten', store=True) #Luu vao CSDL
    ngay_sinh = fields.Date("Ngày sinh", compute='_tinh_tuoi', store=True)
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    lich_su_lam_viec_ids = fields.One2many('lich_su_lam_viec', inverse_name='nhan_vien_id', string='Danh sách LSLV')
    # chuc_vu_ids = fields.One2many('chuc_vu', inverse_name='nhan_vien_id', string='Danh sách CV')
    # phong_ban_ids = fields.One2many('phong_ban', inverse_name='nhan_vien_id', string='Danh sách PB')

    gioi_tinh = fields.Selection(
        selection=[
            ('nam', 'Nam'),
            ('nu', 'Nữ'),
            ('khac', "Khác"),
        ],
    string="Giới tính"
    )

    ho_ten_dem = fields.Char("Họ tên đệm")
    ten = fields.Char("Tên")
    tuoi = fields.Integer("Tuổi")

    @api.depends("ho_ten_dem", "ten")
    def _tinh_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_ten = record.ho_ten_dem + ' ' + record.ten

    @api.onchange("ho_ten_dem", "ten")
    def _tinh_ma_dinh_danh(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                chu_cai_dau = ''.join([tu[0][0] for tu in record.ho_ten_dem.lower().split()])
                record.ma_dinh_danh = record.ten.lower() + chu_cai_dau

    @api.depends("tuoi")
    def _tinh_tuoi(self):
        today = date.today()
        for record in self:
            if record.tuoi:
                record.tuoi = today.year - record.ngay_sinh.year - ((today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day))
            else:
                return 0