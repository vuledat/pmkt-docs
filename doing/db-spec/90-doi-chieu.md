# Ma trận đối chiếu — LDM entity × bảng DB × code

> Sinh tự động. `A` = đã code (sửa đắt) · `B` = có schema chưa code (sửa rẻ) · `C` = phải tạo mới.
**Tổng: 206 entity — A: 14 · B: 121 · C: 70**


| Module | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Hành động |
|---|---|---|---|---|---|
| Xác thực · Người dùng | `GoiDichVu` | `iam_goi_dich_vu` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `Subscription` | `iam_subscription` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `TenantModule` | `iam_tenant_module` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `NhatKyWebhookHub` | `iam_nhat_ky_webhook_hub` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `NguoiDung` | `iam_tai_khoan` | `iam_tai_khoan` | A | VÁ + sửa code |
| Xác thực · Người dùng | `TokenXacThuc` | `iam_token_xac_thuc` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `OTP` | `iam_otp` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `PhienDangNhap` | `iam_phien_dang_nhap` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `NhatKyHoatDong` | `iam_nhat_ky_hoat_dong` | — | C | TẠO MỚI |
| Xác thực · Người dùng | `ThamSoHeThong` | `iam_tham_so_he_thong` | — | C | TẠO MỚI |
| Bán hàng | `HopDongBanHang` | `sal_hop_dong_ban_hang` | — | C | TẠO MỚI |
| Bán hàng | `ChiTietHopDongBanHang` | `sal_hop_dong_ban_hang_chi_tiet` | — | C | TẠO MỚI |
| Bán hàng | `DieuKhoanThanhToanHopDong` | `sal_dieu_khoan_thanh_toan_hop_dong` | — | C | TẠO MỚI |
| Bán hàng | `DonDatHang` | `sal_don_dat_hang` | — | C | TẠO MỚI |
| Bán hàng | `ChiTietDonDatHang` | `sal_don_dat_hang_chi_tiet` | — | C | TẠO MỚI |
| Bán hàng | `ChungTuBan` | `sal_chung_tu_ban_hang` | `sal_chung_tu_ban_hang` | A | VÁ + sửa code |
| Bán hàng | `ChiTietChungTuBan` | `sal_chung_tu_ban_hang_chi_tiet` | `sal_chi_tiet_chung_tu_ban_hang` | A | VÁ + sửa code |
| Bán hàng | `HoaDonBan` | `sal_hoa_don_ban_hang` | — | C | TẠO MỚI |
| Bán hàng | `ChiTietHoaDonBan` | `sal_hoa_don_ban_hang_chi_tiet` | `sal_chi_tiet_hd_ban_hang` | B | ĐỔI TÊN + VÁ |
| Báo cáo tài chính | `BaoCaoTaiChinh` | `rpt_bao_cao_tai_chinh` | `rpt_bao_cao_tai_chinh` | B | VÁ |
| Báo cáo tài chính | `BaoCaoTinhHinhTaiChinhChiTiet` | `rpt_bao_cao_tinh_hinh_tai_chinh_chi_tiet` | `rpt_bc_tinh_hinh_tai_chinh_chi_tiet` | B | ĐỔI TÊN + VÁ |
| Báo cáo tài chính | `BaoCaoKetQuaHoatDongKinhDoanhChiTiet` | `rpt_bao_cao_ket_qua_hoat_dong_kinh_doanh_chi_tiet` | `rpt_bc_ket_qua_hdkd_chi_tiet` | B | ĐỔI TÊN + VÁ |
| Báo cáo tài chính | `BaoCaoLuuChuyenTienTeTrucTiepChiTiet` | `rpt_bao_cao_luu_chuyen_tien_te_truc_tiep_chi_tiet` | — | C | TẠO MỚI |
| Báo cáo tài chính | `BaoCaoLuuChuyenTienTeGianTiepChiTiet` | `rpt_bao_cao_luu_chuyen_tien_te_gian_tiep_chi_tiet` | `rpt_bc_luu_chuyen_tt_gian_tiep_chi_tiet` | B | ĐỔI TÊN + VÁ |
| Báo cáo tài chính | `ThietLapChiTieu` | `rpt_thiet_lap_chi_tieu` | `rpt_thiet_lap_chi_tieu` | B | VÁ |
| Báo cáo tài chính | `ThietLapCongThuc` | `rpt_thiet_lap_cong_thuc` | `rpt_thiet_lap_cong_thuc` | B | VÁ |
| Báo cáo tài chính | `HoatDongChungTu` | `rpt_hoat_dong_chung_tu` | `rpt_hoat_dong_chung_tu` | B | VÁ |
| Báo cáo tài chính | `HoatDongSoDuCongNo` | `rpt_hoat_dong_so_du_cong_no` | `rpt_hoat_dong_so_du_cong_no` | B | VÁ |
| Báo cáo tài chính | `HoatDongSoDuTaiKhoan` | `rpt_hoat_dong_so_du_tai_khoan` | `rpt_hoat_dong_so_du_tai_khoan` | B | VÁ |
| Công cụ dụng cụ | `CongCuDungCu` | `ccdc_cong_cu_dung_cu` | `ccdc_cong_cu_dung_cu` | B | VÁ |
| Công cụ dụng cụ | `DonViQuanLyCCDC` | `ccdc_don_vi_quan_ly` | `ccdc_don_vi_quan_ly_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `NhomHeSoPhanBoCCDC` | `ccdc_nhom_he_so_phan_bo` | — | C | TẠO MỚI |
| Công cụ dụng cụ | `HeSoPhanBoCongCuDungCu` | `ccdc_he_so_phan_bo` | `ccdc_he_so_phan_bo_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `ThamChieuThuCongCCDC` | `ccdc_tham_chieu_thu_cong` | `?` | * | RÀ TAY |
| Công cụ dụng cụ | `PhieuKiemKeCCDC` | `ccdc_phieu_kiem_ke` | `ccdc_phieu_kiem_ke_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `PhieuKiemKeCCDC_DonVi` | `ccdc_phieu_kiem_ke_don_vi` | — | C | TẠO MỚI |
| Công cụ dụng cụ | `NguoiKiemKeCCDC` | `ccdc_phieu_kiem_ke_nguoi_kiem_ke` | `ccdc_chi_tiet_nguoi_kiem_ke` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `ChiTietKiemKeCCDC` | `ccdc_phieu_kiem_ke_chi_tiet` | `ccdc_chi_tiet_kiem_ke_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `PhieuDieuChinhCCDC` | `ccdc_phieu_dieu_chinh` | `ccdc_phieu_dieu_chinh_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `ChiTietPhieuDieuChinhCCDC` | `ccdc_phieu_dieu_chinh_chi_tiet` | `ccdc_chi_tiet_phieu_dieu_chinh_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `PhieuDieuChuyenCCDC` | `ccdc_phieu_dieu_chuyen` | `ccdc_phieu_dieu_chuyen_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `ChiTietPhieuDieuChuyenCCDC` | `ccdc_phieu_dieu_chuyen_chi_tiet` | `ccdc_chi_tiet_phieu_dieu_chuyen_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `PhieuGhiGiamCCDC` | `ccdc_phieu_ghi_giam` | `ccdc_phieu_ghi_giam_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `ChiTietPhieuGhiGiamCCDC` | `ccdc_phieu_ghi_giam_chi_tiet` | `ccdc_chi_tiet_phieu_ghi_giam_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `PhieuPhanBoCCDC` | `ccdc_phieu_phan_bo` | `ccdc_phieu_phan_bo_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `ChiTietPhieuPhanBoCCDC` | `ccdc_phieu_phan_bo_chi_tiet` | `ccdc_chi_tiet_phieu_phan_bo_ccdc` | B | ĐỔI TÊN + VÁ |
| Công cụ dụng cụ | `TamDungPhanBoCCDC` | `ccdc_tam_dung_phan_bo` | `ccdc_tam_dung_phan_bo_ccdc` | B | ĐỔI TÊN + VÁ |
| Chi phí trả trước | `KhaiBaoChiPhiTraTruoc` | `cptt_khai_bao_chi_phi_tra_truoc` | `cptt_khai_bao_chi_phi_tra_truoc` | B | VÁ |
| Chi phí trả trước | `ChungTuGocKhaiBaoChiPhiTraTruoc` | `cptt_chung_tu_goc_khai_bao_chi_phi_tra_truoc` | `cptt_chung_tu_goc_khai_bao` | B | ĐỔI TÊN + VÁ |
| Chi phí trả trước | `ThietLapPhanBoChiPhiTraTruoc` | `cptt_thiet_lap_phan_bo_chi_phi_tra_truoc` | `cptt_thiet_lap_phan_bo_chi_phi` | B | ĐỔI TÊN + VÁ |
| Chi phí trả trước | `KeHoachPhanBoChiPhiTraTruoc` | `cptt_ke_hoach_phan_bo_chi_phi_tra_truoc` | — | C | TẠO MỚI |
| Chi phí trả trước | `ChungTuPhanBoChiPhiTraTruoc` | `cptt_chung_tu_phan_bo_chi_phi_tra_truoc` | `cptt_chung_tu_phan_bo_chi_phi` | B | ĐỔI TÊN + VÁ |
| Chi phí trả trước | `ChiTietPhanBoChiPhiTraTruoc` | `cptt_chung_tu_phan_bo_chi_phi_tra_truoc_chi_tiet` | `cptt_chi_tiet_phan_bo_chi_phi` | B | ĐỔI TÊN + VÁ |
| Đánh giá lại ngoại tệ | `PhieuDanhGiaLaiNgoaiTe` | `fx_phieu_danh_gia_lai_ngoai_te` | — | C | TẠO MỚI |
| Đánh giá lại ngoại tệ | `ChiTietDanhGiaLaiNgoaiTe_SoDu` | `fx_phieu_danh_gia_lai_ngoai_te_so_du` | — | C | TẠO MỚI |
| Đánh giá lại ngoại tệ | `ChiTietDanhGiaLaiNgoaiTe_CongNo` | `fx_phieu_danh_gia_lai_ngoai_te_cong_no` | — | C | TẠO MỚI |
| Đánh giá lại ngoại tệ | `ChiTietDanhGiaLaiNgoaiTe_HachToan` | `fx_phieu_danh_gia_lai_ngoai_te_hach_toan` | — | C | TẠO MỚI |
| Đánh giá lại ngoại tệ | `KetQuaTinhTyGiaXuatQuy` | `fx_ket_qua_tinh_ty_gia_xuat_quy` | — | C | TẠO MỚI |
| Điều chỉnh giá hàng bán | `ChungTuDieuChinhGiaHangBan` | `sal_chung_tu_dieu_chinh_gia_hang_ban` | `sal_dieu_chinh_gia_hang_ban` | B | ĐỔI TÊN + VÁ |
| Điều chỉnh giá hàng bán | `ChiTietDieuChinhGiaHangBan` | `sal_chung_tu_dieu_chinh_gia_hang_ban_chi_tiet` | `sal_chi_tiet_dieu_chinh_gia_hang_ban` | B | ĐỔI TÊN + VÁ |
| Điều chỉnh giá hàng mua | `ChungTuDieuChinhGiaHangMua` | `pur_chung_tu_dieu_chinh_gia_hang_mua` | `pur_chung_tu_dieu_chinh_gia_mua` | B | ĐỔI TÊN + VÁ |
| Điều chỉnh giá hàng mua | `ChiTietChungTuDieuChinhGiaHangMua` | `pur_chung_tu_dieu_chinh_gia_hang_mua_chi_tiet` | `pur_chi_tiet_dieu_chinh_gia_mua` | B | ĐỔI TÊN + VÁ |
| Đối trừ công nợ | `ChungTuDoiTru` | `pur_chung_tu_doi_tru` | `pur_chung_tu_doi_tru` | B | VÁ |
| Đối trừ công nợ | `ChiTietChungTuDoiTru` | `pur_chung_tu_doi_tru_chi_tiet` | `pur_chi_tiet_chung_tu_doi_tru` | B | ĐỔI TÊN + VÁ |
| Giá thành | `CauHinhGiaThanh` | `cst_cau_hinh_gia_thanh` | `cst_cau_hinh_gia_thanh` | B | VÁ |
| Giá thành | `ThietLapHeSoTyLe` | `cst_thiet_lap_he_so_ty_le` | `cst_thiet_lap_he_so_ty_le` | B | VÁ |
| Giá thành | `KyTinhGiaThanh` | `cst_ky_tinh_gia_thanh` | `cst_ky_tinh_gia_thanh` | B | VÁ |
| Giá thành | `DoDangDauKy` | `cst_do_dang_dau_ky` | `cst_do_dang_dau_ky` | B | VÁ |
| Giá thành | `DoDangCuoiKy` | `cst_do_dang_cuoi_ky` | `cst_do_dang_cuoi_ky` | B | VÁ |
| Giá thành | `ChiTietDoDangCuoiKy` | `cst_do_dang_cuoi_ky_chi_tiet` | `cst_chi_tiet_do_dang_cuoi_ky` | B | ĐỔI TÊN + VÁ |
| Giá thành | `PhanBoChiPhi` | `cst_phan_bo_chi_phi` | `cst_phan_bo_chi_phi` | B | VÁ |
| Giá thành | `PhanBoChiPhi_DoiTuong` | `cst_phan_bo_chi_phi_doi_tuong` | — | C | TẠO MỚI |
| Giá thành | `HeSoPhanBo` | `cst_he_so_phan_bo` | `cst_he_so_phan_bo` | B | VÁ |
| Giá thành | `ChiTietPhanBoChiPhi` | `cst_phan_bo_chi_phi_chi_tiet` | `cst_chi_tiet_phan_bo_chi_phi` | B | ĐỔI TÊN + VÁ |
| Giá thành | `PhanBoChungTu` | `cst_phan_bo_chung_tu` | `cst_phan_bo_chung_tu` | B | VÁ |
| Giá thành | `GiaThanhSanPham` | `cst_gia_thanh_san_pham` | `cst_gia_thanh_san_pham` | B | VÁ |
| Giá thành | `ChungTuGiaThanh` | `cst_chung_tu_gia_thanh` | `cst_chung_tu_gia_thanh` | B | VÁ |
| Giá thành | `ChiTietChungTuGiaThanh` | `cst_chung_tu_gia_thanh_chi_tiet` | `cst_chi_tiet_chung_tu_gia_thanh` | B | ĐỔI TÊN + VÁ |
| Giá thành | `GiaThanhCongTrinh` | `cst_gia_thanh_cong_trinh` | — | C | TẠO MỚI |
| Giá thành | `PhieuNghiemThuCongTrinh` | `cst_phieu_nghiem_thu_cong_trinh` | — | C | TẠO MỚI |
| Giá thành | `ChiTietPhieuNghiemThuCongTrinh` | `cst_phieu_nghiem_thu_cong_trinh_chi_tiet` | — | C | TẠO MỚI |
| Giá thành | `DinhMucGiaThanh` | `cst_dinh_muc_gia_thanh` | `cst_dinh_muc_gia_thanh` | B | VÁ |
| Hệ thống · Tenant · Vai trò | `Tenant` | `iam_tenant` | `iam_tenant` | A | VÁ + sửa code |
| Hệ thống · Tenant · Vai trò | `Tenant_LinhVucHoatDong` | `iam_tenant_linh_vuc_hoat_dong` | — | C | TẠO MỚI |
| Hệ thống · Tenant · Vai trò | `VaiTro` | `iam_vai_tro` | `iam_vai_tro` | A | VÁ + sửa code |
| Hệ thống · Tenant · Vai trò | `VaiTroQuyen` | `iam_vai_tro_quyen` | `iam_vai_tro_quyen` | A | VÁ + sửa code |
| Hệ thống · Tenant · Vai trò | `NguoiDungVaiTro` | `iam_tai_khoan_vai_tro` | `iam_tai_khoan_vai_tro` | A | VÁ + sửa code |
| Hệ thống · Tenant · Vai trò | `CauHinhEmail` | `cfg_cau_hinh_email` | — | C | TẠO MỚI |
| Kết chuyển lãi lỗ | `ButToanKetChuyen` | `ktth_but_toan_ket_chuyen` | — | C | TẠO MỚI |
| Kết chuyển lãi lỗ | `PhieuKetChuyenLaiLo` | `ktth_phieu_ket_chuyen_lai_lo` | — | C | TẠO MỚI |
| Kết chuyển lãi lỗ | `ChiTietPhieuKetChuyenLaiLo` | `ktth_phieu_ket_chuyen_lai_lo_chi_tiet` | — | C | TẠO MỚI |
| Kho | `PhieuNhapKho` | `inv_phieu_nhap_kho` | `inv_phieu_nhap_kho_module_kho` | B | ĐỔI TÊN + VÁ |
| Kho | `ChiTietPhieuNhapKho` | `inv_phieu_nhap_kho_chi_tiet` | `inv_chi_tiet_phieu_nhap_kho` | B | ĐỔI TÊN + VÁ |
| Kho | `TonKho` | `inv_ton_kho` | `inv_ton_kho` | B | VÁ |
| Kho | `CostLayer` | `inv_lop_gia_von` | — | C | TẠO MỚI |
| Kho | `PhieuXuatKho` | `inv_phieu_xuat_kho` | `inv_phieu_xuat_kho_module_kho` | B | ĐỔI TÊN + VÁ |
| Kho | `ChiTietPhieuXuatKho` | `inv_phieu_xuat_kho_chi_tiet` | `inv_chi_tiet_phieu_xuat_kho` | B | ĐỔI TÊN + VÁ |
| Kho | `PhieuXuatDieuChuyen` | `inv_phieu_xuat_dieu_chuyen` | `inv_phieu_xuat_dieu_chuyen` | B | VÁ |
| Kho | `ChiTietPhieuXuatDieuChuyen` | `inv_phieu_xuat_dieu_chuyen_chi_tiet` | `inv_chi_tiet_phieu_xuat_dieu_chuyen` | B | ĐỔI TÊN + VÁ |
| Kho | `PhieuNhapDieuChuyen` | `inv_phieu_nhap_dieu_chuyen` | `inv_phieu_nhap_dieu_chuyen` | B | VÁ |
| Kho | `ChiTietPhieuNhapDieuChuyen` | `inv_phieu_nhap_dieu_chuyen_chi_tiet` | `inv_chi_tiet_phieu_nhap_dieu_chuyen` | B | ĐỔI TÊN + VÁ |
| Kho | `PhieuDieuChuyenDieuChinh` | `inv_phieu_dieu_chuyen_dieu_chinh` | `inv_phieu_dieu_chuyen_dieu_chinh` | B | VÁ |
| Kho | `ChiTietPhieuDieuChuyenDieuChinh` | `inv_phieu_dieu_chuyen_dieu_chinh_chi_tiet` | `inv_chi_tiet_phieu_dieu_chuyen_dieu_chinh` | B | ĐỔI TÊN + VÁ |
| Kho | `PhieuKiemKeKho` | `inv_phieu_kiem_ke_kho` | `inv_phieu_kiem_ke` | B | ĐỔI TÊN + VÁ |
| Kho | `ChiTietPhieuKiemKeKho` | `inv_phieu_kiem_ke_kho_chi_tiet` | `inv_chi_tiet_kiem_ke` | B | ĐỔI TÊN + VÁ |
| Kho | `ChiTietNguoiKiemKe` | `inv_phieu_kiem_ke_kho_nguoi_kiem_ke` | — | C | TẠO MỚI |
| Kho | `ChiTietTonKhoSnapShot` | `inv_phieu_kiem_ke_kho_ton_kho_snapshot` | — | C | TẠO MỚI |
| Kho | `LenhLapRapThaoDo` | `inv_lenh_lap_rap_thao_do` | — | C | TẠO MỚI |
| Kho | `DauVaoLenhLapRapThaoDo` | `inv_lenh_lap_rap_thao_do_dau_vao` | — | C | TẠO MỚI |
| Kho | `ThanhPhamSauLapRapThaoDo` | `inv_lenh_lap_rap_thao_do_thanh_pham_sau_lap_rap_thao_do` | — | C | TẠO MỚI |
| Kho | `LuotTinhGiaXuatKho` | `inv_luot_tinh_gia_xuat_kho` | `inv_luot_tinh_gia_xuat_kho` | B | VÁ |
| Kho | `KetQuaTinhGiaXuatKho` | `inv_ket_qua_tinh_gia_xuat_kho` | `inv_ket_qua_tinh_gia_xuat_kho` | B | VÁ |
| Kho | `ChiTietApGiaXuatKho` | `inv_ket_qua_tinh_gia_xuat_kho_chi_tiet` | `inv_chi_tiet_ap_gia_xuat_kho` | B | ĐỔI TÊN + VÁ |
| Kho | `DinhMucNVL` | `inv_dinh_muc_nguyen_vat_lieu` | — | C | TẠO MỚI |
| Kho | `ChiTietDinhMucNVL` | `inv_dinh_muc_nguyen_vat_lieu_chi_tiet` | — | C | TẠO MỚI |
| Kho | `LenhSanXuat` | `inv_lenh_san_xuat` | — | C | TẠO MỚI |
| Kho | `ChiTietLenhSanXuat_ThanhPham` | `inv_lenh_san_xuat_thanh_pham` | — | C | TẠO MỚI |
| Kho | `ChiTietLenhSanXuat_NguyenVatLieu` | `inv_lenh_san_xuat_nguyen_vat_lieu` | — | C | TẠO MỚI |
| Kho | `LoaiTruNguyenVatLieuLenhSanXuat` | `inv_loai_tru_nguyen_vat_lieu_lenh_san_xuat` | — | C | TẠO MỚI |
| Khóa sổ kế toán | `ThietLapKhoaSo` | `cfg_thiet_lap_khoa_so` | `cfg_thiet_lap_khoa_so` | A | VÁ + sửa code |
| Khóa sổ kế toán | `ChiTietThietLapKhoaSoChungTu` | `cfg_thiet_lap_khoa_so_chung_tu` | `cfg_thiet_lap_khoa_so_chung_tu` | A | VÁ + sửa code |
| Khóa sổ kế toán | `ChiTietThietLapKhoaSoNguoiDung` | `cfg_thiet_lap_khoa_so_nguoi_dung` | `cfg_thiet_lap_khoa_so_nguoi_dung` | A | VÁ + sửa code |
| Mua hàng | `ChungTuMuaHang` | `pur_chung_tu_mua_hang` | `pur_chung_tu_mua_hang` | A | VÁ + sửa code |
| Mua hàng | `ChiTietChungTuMuaHang` | `pur_chung_tu_mua_hang_chi_tiet` | `pur_chi_tiet_chung_tu_mua_hang` | A | VÁ + sửa code |
| Mua hàng | `HoaDonMua` | `pur_hoa_don_mua` | `pur_hoa_don_mua` | B | VÁ |
| Mua hàng | `ChungTuNhanHoaDon` | `pur_chung_tu_nhan_hoa_don` | `pur_chung_tu_nhan_hoa_don` | B | VÁ |
| Mua hàng | `ChiTietHoaDon` | `pur_hoa_don_mua_chi_tiet` | `pur_chi_tiet_hoa_don` | B | ĐỔI TÊN + VÁ |
| Mua hàng | `ChiPhiMuaHang` | `pur_chi_phi_mua_hang` | `pur_chi_phi_mua_hang` | B | VÁ |
| Mua hàng | `ChiPhiNhapKhau` | `pur_chi_phi_nhap_khau` | `pur_chi_phi_nhap_khau` | B | VÁ |
| Mua hàng | `PhanBoChiPhiMuaHang` | `pur_phan_bo_chi_phi_mua_hang` | `pur_phan_bo_chi_phi_mua_hang` | B | VÁ |
| Ngân quỹ (tiền mặt · tiền gửi) | `PhieuThu` | `cb_phieu_thu` | `cb_phieu_thu` | B | VÁ |
| Ngân quỹ (tiền mặt · tiền gửi) | `ChiTietPhieuThu` | `cb_phieu_thu_chi_tiet` | `cb_chi_tiet_phieu_thu` | B | ĐỔI TÊN + VÁ |
| Ngân quỹ (tiền mặt · tiền gửi) | `PhieuChi` | `cb_phieu_chi` | `cb_phieu_chi` | B | VÁ |
| Ngân quỹ (tiền mặt · tiền gửi) | `ChiTietPhieuChi` | `cb_phieu_chi_chi_tiet` | `cb_chi_tiet_phieu_chi` | B | ĐỔI TÊN + VÁ |
| Ngân quỹ (tiền mặt · tiền gửi) | `ChiTietBangKeHoaDon` | `cb_phieu_chi_bang_ke_hoa_don` | `cb_chi_tiet_bang_ke_hoa_don` | B | ĐỔI TÊN + VÁ |
| Ngân quỹ (tiền mặt · tiền gửi) | `ChuyenTienNoiBo` | `cb_chuyen_tien_noi_bo` | — | C | TẠO MỚI |
| Ngân quỹ (tiền mặt · tiền gửi) | `ChiTietChuyenTienNoiBo` | `cb_chuyen_tien_noi_bo_chi_tiet` | — | C | TẠO MỚI |
| Phiếu kế toán tổng hợp | `PhieuKeToanTongHop` | `ktth_phieu_ke_toan_tong_hop` | `ktth_phieu_ke_toan_tong_hop` | B | VÁ |
| Phiếu kế toán tổng hợp | `ChiTietPhieuKTTH_HachToan` | `ktth_phieu_ke_toan_tong_hop_hach_toan` | `ktth_chi_tiet_phieu_ktth_hach_toan` | B | ĐỔI TÊN + VÁ |
| Phiếu kế toán tổng hợp | `ChiTietPhieuKTTH_HoaDon` | `ktth_phieu_ke_toan_tong_hop_hoa_don` | `ktth_chi_tiet_phieu_ktth_hoa_don` | B | ĐỔI TÊN + VÁ |
| Hồ sơ người dùng trong tenant | `NguoiDung_Tenant` | `iam_tai_khoan_tenant` | `iam_tai_khoan_tenant` | A | VÁ + sửa code |
| Hồ sơ người dùng trong tenant | `YeuCauXoaTaiKhoan` | `iam_yeu_cau_xoa_tai_khoan` | — | C | TẠO MỚI |
| Số dư ban đầu | `SoDuBanDauTaiKhoan` | `sdbd_so_du_ban_dau_tai_khoan` | `sdbd_so_du_ban_dau_tai_khoan` | B | VÁ |
| Số dư ban đầu | `ChiTietSDBD_TaiKhoan` | `sdbd_so_du_ban_dau_tai_khoan_chi_tiet` | `sdbd_chi_tiet_sdbd_tai_khoan` | B | ĐỔI TÊN + VÁ |
| Số dư ban đầu | `SoDuBanDauTKNganHang` | `sdbd_so_du_ban_dau_tai_khoan_ngan_hang` | `sdbd_so_du_ban_dau_tk_ngan_hang` | B | ĐỔI TÊN + VÁ |
| Số dư ban đầu | `SoDuBanDauKhachHang` | `sdbd_so_du_ban_dau_khach_hang` | `sdbd_so_du_ban_dau_khach_hang` | B | VÁ |
| Số dư ban đầu | `ChiTietSDBD_KH_HoaDon` | `sdbd_so_du_ban_dau_khach_hang_chi_tiet` | `sdbd_chi_tiet_sdbd_kh_hoa_don` | B | ĐỔI TÊN + VÁ |
| Số dư ban đầu | `SoDuBanDauNCC` | `sdbd_so_du_ban_dau_nha_cung_cap` | `sdbd_so_du_ban_dau_ncc` | B | ĐỔI TÊN + VÁ |
| Số dư ban đầu | `ChiTietSDBD_NCC_HoaDon` | `sdbd_so_du_ban_dau_nha_cung_cap_chi_tiet` | `sdbd_chi_tiet_sdbd_ncc_hoa_don` | B | ĐỔI TÊN + VÁ |
| Số dư ban đầu | `SoDuBanDauNhanVien` | `sdbd_so_du_ban_dau_nhan_vien` | `sdbd_so_du_ban_dau_nhan_vien` | B | VÁ |
| Số dư ban đầu | `SoDuBanDauVatTu` | `sdbd_so_du_ban_dau_vat_tu` | `sdbd_so_du_ban_dau_vat_tu` | B | VÁ |
| Sổ kế toán (sổ cái · sổ kho) | `SoCai` | `acc_so_cai` | `acc_so_cai` | A | VÁ + sửa code |
| Sổ kế toán (sổ cái · sổ kho) | `SoKho` | `acc_so_kho` | `acc_so_xuat_nhap_tong_hop` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `ChungTuGhiGiamTSCD` | `fa_chung_tu_ghi_giam_tai_san_co_dinh` | `fa_chung_tu_ghi_giam_tscd` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `ChiTietGhiGiamTSCD` | `fa_chung_tu_ghi_giam_tai_san_co_dinh_chi_tiet` | `fa_chi_tiet_ghi_giam_tscd` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `HachToanGhiGiamTSCD` | `fa_hach_toan_ghi_giam_tai_san_co_dinh` | `fa_hach_toan_ghi_giam_tscd` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `ChungTuNgungKhauHao` | `fa_chung_tu_ngung_khau_hao` | `fa_chung_tu_ngung_khau_hao` | B | VÁ |
| Tài sản cố định | `ChiTietNgungKhauHao` | `fa_chung_tu_ngung_khau_hao_chi_tiet` | `fa_chi_tiet_ngung_khau_hao` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `KiemKeTaiSanCoDinh` | `fa_kiem_ke_tai_san_co_dinh` | `fa_kiem_ke_tai_san_co_dinh` | B | VÁ |
| Tài sản cố định | `ChiTietKiemKeTaiSanCoDinh` | `fa_kiem_ke_tai_san_co_dinh_chi_tiet` | `fa_chi_tiet_kiem_ke_tai_san_co_dinh` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `ThanhVienKiemKeTaiSanCoDinh` | `fa_kiem_ke_tai_san_co_dinh_thanh_vien` | `fa_thanh_vien_kiem_ke_tai_san_co_dinh` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `DieuChinhTaiSanCoDinh` | `fa_dieu_chinh_tai_san_co_dinh` | `fa_dieu_chinh_tai_san_co_dinh` | B | VÁ |
| Tài sản cố định | `ThanhVienDieuChinhTaiSanCoDinh` | `fa_dieu_chinh_tai_san_co_dinh_thanh_vien` | `fa_thanh_vien_dieu_chinh_tai_san_co_dinh` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `ChiTietDieuChinhTaiSanCoDinh` | `fa_dieu_chinh_tai_san_co_dinh_chi_tiet` | `fa_chi_tiet_dieu_chinh_tai_san_co_dinh` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `HachToanDieuChinhTaiSanCoDinh` | `fa_hach_toan_dieu_chinh_tai_san_co_dinh` | `fa_hach_toan_dieu_chinh_tai_san_co_dinh` | B | VÁ |
| Tài sản cố định | `TaiSanCoDinh` | `fa_tai_san_co_dinh` | `fa_tai_san_co_dinh` | B | VÁ |
| Tài sản cố định | `ChiTietNguonVonTaiSanCoDinh` | `fa_tai_san_co_dinh_nguon_von` | `fa_tai_san_co_dinh_nguon_von` | B | VÁ |
| Tài sản cố định | `ChiTietPhanBoTaiSanCoDinh` | `fa_tai_san_co_dinh_phan_bo` | `fa_tai_san_co_dinh_phan_bo` | B | VÁ |
| Tài sản cố định | `LichSuPhanBoTaiSanCoDinh` | `fa_tai_san_co_dinh_lich_su_phan_bo` | `fa_lich_su_phan_bo` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `PhuTungTaiSanCoDinh` | `fa_phu_tung_tai_san_co_dinh` | `fa_tai_san_co_dinh_phu_tung` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `BoPhanCauThanhTaiSanCoDinh` | `fa_bo_phan_cau_thanh_tai_san_co_dinh` | `fa_tai_san_co_dinh_bo_phan_cau_thanh` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `ThongTinKhacTaiSanCoDinh` | `fa_thong_tin_khac_tai_san_co_dinh` | `fa_tai_san_co_dinh_thong_tin_khac` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `LienKetChungTuTaiSanCoDinh` | `fa_lien_ket_chung_tu_tai_san_co_dinh` | `fa_tai_san_co_dinh_lien_ket_chung_tu` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `KhaiBaoSanLuong` | `fa_khai_bao_san_luong` | `fa_khai_bao_san_luong` | B | VÁ |
| Tài sản cố định | `ChiTietKhaiBaoSanLuong` | `fa_khai_bao_san_luong_chi_tiet` | `fa_chi_tiet_khai_bao_san_luong` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `DieuChuyenTaiSan` | `fa_dieu_chuyen_tai_san` | `fa_dieu_chuyen_tai_san` | B | VÁ |
| Tài sản cố định | `ChiTietDieuChuyenTaiSan` | `fa_dieu_chuyen_tai_san_chi_tiet` | `fa_chi_tiet_dieu_chuyen` | B | ĐỔI TÊN + VÁ |
| Tài sản cố định | `LichSuDieuChuyenTaiSan` | `fa_tai_san_co_dinh_lich_su_dieu_chuyen` | — | C | TẠO MỚI |
| Tài sản cố định | `KhauHaoTaiSan` | `fa_khau_hao_tai_san` | `fa_khau_hao_tai_san` | B | VÁ |
| Tài sản cố định | `ChiTietKhauHaoTaiSan` | `fa_khau_hao_tai_san_chi_tiet` | `fa_chi_tiet_khau_hao_tai_san` | B | ĐỔI TÊN + VÁ |
| Thuế | `ThietLapThongTinThue` | `tax_thiet_lap_thong_tin_thue` | — | C | TẠO MỚI |
| Thuế | `DangKyToKhaiThue` | `tax_dang_ky_to_khai_thue` | — | C | TẠO MỚI |
| Thuế | `KhoiTaoToKhai` | `tax_khoi_tao_to_khai` | — | C | TẠO MỚI |
| Thuế | `ToKhaiThue01GTGT` | `tax_to_khai_thue_01_gtgt` | `tax_to_khai_thue_01_gtgt` | B | VÁ |
| Thuế | `BangKeBanRa` | `tax_bang_ke_ban_ra` | — | C | TẠO MỚI |
| Thuế | `BangKeMuaVao` | `tax_bang_ke_mua_vao` | — | C | TẠO MỚI |
| Thuế | `PhuLucGiamThue` | `tax_phu_luc_giam_thue` | — | C | TẠO MỚI |
| Thuế | `PhuLucGiamThue_MuaVao` | `tax_phu_luc_giam_thue_mua_vao` | — | C | TẠO MỚI |
| Thuế | `PhuLucGiamThue_BanRa` | `tax_phu_luc_giam_thue_ban_ra` | — | C | TẠO MỚI |
| Thuế | `PhuLuc01_6GTGT` | `tax_phu_luc_01_6_gtgt` | — | C | TẠO MỚI |
| Thuế | `PhuLuc01_6GTGT_TheoTinh` | `tax_phu_luc_01_6_gtgt_theo_tinh` | — | C | TẠO MỚI |
| Thuế | `PhuLuc01_6GTGT_ChiTiet` | `tax_phu_luc_01_6_gtgt_chi_tiet` | — | C | TẠO MỚI |
| Thuế | `ToKhaiBoSung01KHBS` | `tax_to_khai_bo_sung_01_khbs` | — | C | TẠO MỚI |
| Thuế | `ToKhaiBoSung01KHBS_PhuLucPhanBo` | `tax_to_khai_bo_sung_01_khbs_phu_luc_phan_bo` | — | C | TẠO MỚI |
| Thuế | `BanGiaiTrinh01_1KHBS` | `tax_to_khai_bo_sung_01_khbs_1_khbs` | — | C | TẠO MỚI |
| Thuế | `BanGiaiTrinh01_1KHBS_TaiLieuDinhKem` | `tax_to_khai_bo_sung_01_khbs_1_khbs_tai_lieu_dinh_kem` | — | C | TẠO MỚI |
| Thuế | `ToKhaiThue04GTGT` | `tax_to_khai_thue_04_gtgt` | — | C | TẠO MỚI |
| Thuế | `ChiTietToKhai04GTGT_ChiTieu` | `tax_to_khai_thue_04_gtgt_chi_tieu` | — | C | TẠO MỚI |
| Thuế | `ChiTietToKhai04GTGT_KhoanThuHo` | `tax_to_khai_thue_04_gtgt_khoan_thu_ho` | — | C | TẠO MỚI |
| Thuế | `PhuLucGiamThue04GTGT` | `tax_phu_luc_giam_thue_04_gtgt` | — | C | TẠO MỚI |
| Thuế | `ChiTietPhuLucGiamThue04GTGT` | `tax_phu_luc_giam_thue_04_gtgt_chi_tiet` | — | C | TẠO MỚI |
| Trả lại hàng bán | `ChungTuTraLaiHangBan` | `sal_chung_tu_tra_lai_hang_ban` | `sal_chung_tu_tra_lai_hang_ban` | B | VÁ |
| Trả lại hàng bán | `ChiTietTraLaiHangBan` | `sal_chung_tu_tra_lai_hang_ban_chi_tiet` | `sal_chi_tiet_chung_tu_tra_lai_hang_ban` | B | ĐỔI TÊN + VÁ |
| Trả lại hàng mua | `ChungTuTraLaiHangMua` | `pur_chung_tu_tra_lai_hang_mua` | `pur_chung_tu_tra_lai_hang_mua` | B | VÁ |
| Trả lại hàng mua | `PhieuXuatKhoTraLaiHangMua` | `pur_phieu_xuat_kho_tra_lai_hang_mua` | — | C | TẠO MỚI |
| Trả lại hàng mua | `ChiTietChungTuTraLaiHangMua` | `pur_chung_tu_tra_lai_hang_mua_chi_tiet` | `pur_chi_tiet_chung_tu_tra_lai_hang_mua` | B | ĐỔI TÊN + VÁ |
