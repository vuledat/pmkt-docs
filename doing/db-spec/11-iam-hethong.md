# `iam_` — Hệ thống · Tenant · Vai trò

> Sinh tự động từ [`ldm-HeThong.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-HeThong.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**6 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `Tenant` | `iam_tenant` | `iam_tenant` | A — có code | Bảng nghiệp vụ — Tenant - Đơn vị kế toán và toàn bộ thiết lập (Onboarding, Cấu hình chi tiết, Thông tin công ty, Định dạng số) |
| 2 | `Tenant_LinhVucHoatDong` | `iam_tenant_linh_vuc_hoat_dong` | — | C — tạo mới | Liên kết N–N — Lĩnh vực hoạt động của tenant (Link - lựa chọn nhiều giá trị) |
| 3 | `VaiTro` | `iam_vai_tro` | `iam_vai_tro` | A — có code | Bảng nghiệp vụ — Vai trò trong tenant |
| 4 | `VaiTroQuyen` | `iam_vai_tro_quyen` | `iam_vai_tro_quyen` | A — có code | Dòng chi tiết của `iam_vai_tro` — Quyền được tích của vai trò (mã quyền theo DanhSachQuyen.md) |
| 5 | `NguoiDungVaiTro` | `iam_tai_khoan_vai_tro` | `iam_tai_khoan_vai_tro` | A — có code | Dòng chi tiết của `iam_vai_tro` — Gán người dùng vào vai trò (Link) |
| 6 | `CauHinhEmail` | `cfg_cau_hinh_email` | — | C — tạo mới | Cấu hình / thiết lập — Cấu hình email (tài khoản SMTP gửi thư của tenant; Screen đang đặt tên entity là EmailConfig) |

---

## 1. `iam_tenant`

| Mục | Nội dung |
|---|---|
| Entity LDM | `Tenant` |
| Base class | `TenantedEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `iam_tenant` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Tenant - Đơn vị kế toán và toàn bộ thiết lập · (Onboarding, Cấu hình chi tiết, Thông tin công ty, Định dạng số) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `iam_tenant_linh_vuc_hoat_dong` · `iam_vai_tro` · `cfg_cau_hinh_email` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TenDonVi` | `ten_don_vi` | `text` | N | — | **[Định danh và trạng thái]** Tên doanh nghiệp / hộ kinh doanh |
| 2 | `LoaiDonVi` | `loai_don_vi` | `text` | N | — | **[Định danh và trạng thái]** Loại đơn vị (Doanh nghiệp, Hộ kinh doanh) |
| 3 | `MST` | `mst` | `text` | N | — | **[Định danh và trạng thái]** Mã số thuế |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Định danh và trạng thái]** Trạng thái hoạt động của tenant (HoatDong \| NgungHoatDong) |
| 5 | `DaHoanThanhOnboarding` | `da_hoan_thanh_onboarding` | `boolean` | N | `false` | **[Định danh và trạng thái]** Đã hoàn thành thiết lập onboarding |
| 6 | `NganhNgheId` | `nganh_nghe_id` | `uuid` | N | — | **[Onboarding Bước 1]** ID ngành nghề kinh doanh (reference ENT_NganhNghe) `FK` |
| 7 | `CoChiNhanh` | `co_chi_nhanh` | `boolean` | N | `false` | **[Onboarding Bước 1]** Có chi nhánh |
| 8 | `CheDoKeToanId` | `che_do_ke_toan_id` | `uuid` | N | — | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** ID chế độ kế toán (reference ENT_ThongTu) `FK` |
| 9 | `NgayBatDauDuLieu` | `ngay_bat_dau_du_lieu` | `date` | N | — | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** Ngày bắt đầu dữ liệu |
| 10 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** ID đồng tiền hạch toán (reference ENT_LoaiTienDungChung) `FK` |
| 11 | `CoPhatSinhNgoaiTe` | `co_phat_sinh_ngoai_te` | `boolean` | N | `false` | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** Có phát sinh ngoại tệ |
| 12 | `LoaiPhuongPhapTinhGiaXuatKho` | `loai_phuong_phap_tinh_gia_xuat_kho` | `text` CHECK | N | — | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** Cách áp phương pháp tính giá xuất kho (DungChungMotPhuongPhap \| MoiVatTuMotPhuongPhap) |
| 13 | `PhuongPhapTinhGiaXuatKho` | `phuong_phap_tinh_gia_xuat_kho` | `text` CHECK | Y | — | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** Phương pháp tính giá xuất kho dùng chung (NhapTruocXuatTruoc \| BinhQuanCuoiKy \| BinhQuanTucThoi \| DichDanh) |
| 14 | `PhuongPhapTinhThueGTGT` | `phuong_phap_tinh_thue_gtgt` | `text` CHECK | N | — | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** Phương pháp tính thuế GTGT (KhauTru \| TrucTiepTrenDoanhThu) |
| 15 | `CoSuDungHDDT` | `co_su_dung_hddt` | `boolean` | N | `false` | **[Onboarding Bước 2 - Thông tin dữ liệu kế toán]** Có sử dụng hóa đơn điện tử |
| 16 | `NgayBatDauNamTaiChinh` | `ngay_bat_dau_nam_tai_chinh` | `text` CHECK | N | — | **[Cấu hình chi tiết - Sổ sách và niên độ]** Ngày bắt đầu năm tài chính (Ngay0101 \| Ngay0104 \| Ngay0107 \| Ngay0110) |
| 17 | `HinhThucGhiSoKeToan` | `hinh_thuc_ghi_so_ke_toan` | `text` CHECK | N | — | **[Cấu hình chi tiết - Sổ sách và niên độ]** Hình thức ghi sổ kế toán (NhatKyChung \| NhatKySoCai \| ChungTuGhiSo) |
| 18 | `CanhBaoChiQuaTonQuy` | `canh_bao_chi_qua_ton_quy` | `text` CHECK | Y | — | **[Cấu hình chi tiết - Tiền tệ]** Cảnh báo khi chi quá số tồn TK 111, 112 (KhongCanhBao \| CanhBaoChoPhepGhiSo \| CanhBaoKhongChoPhepGhiSo) |
| 19 | `PhuongPhapTinhTyGiaXuatQuy` | `phuong_phap_tinh_ty_gia_xuat_quy` | `text` CHECK | Y | — | **[Cấu hình chi tiết - Tiền tệ]** Phương pháp tính tỷ giá xuất quỹ (BinhQuanTucThoi \| BinhQuanCuoiKy) |
| 20 | `SapXepThuTruocChiSauCungNgay` | `sap_xep_thu_truoc_chi_sau_cung_ngay` | `boolean` | Y | `false` | **[Cấu hình chi tiết - Tiền tệ]** Trong cùng một ngày sắp xếp thu trước chi sau |
| 21 | `TaiKhoanLaiCLTGXuatQuyId` | `tai_khoan_lai_cltg_xuat_quy_id` | `uuid` | Y | — | **[Cấu hình chi tiết - Tiền tệ]** ID TK xử lý lãi chênh lệch tỷ giá khi xuất quỹ (reference ENT_HeThongTaiKhoan) `FK` |
| 22 | `TaiKhoanLoCLTGXuatQuyId` | `tai_khoan_lo_cltg_xuat_quy_id` | `uuid` | Y | — | **[Cấu hình chi tiết - Tiền tệ]** ID TK xử lý lỗ chênh lệch tỷ giá khi xuất quỹ (reference ENT_HeThongTaiKhoan) `FK` |
| 23 | `TaiKhoanLaiCLTGThanhToanId` | `tai_khoan_lai_cltg_thanh_toan_id` | `uuid` | Y | — | **[Cấu hình chi tiết - Tiền tệ]** ID TK xử lý lãi chênh lệch tỷ giá khi thu/trả tiền (reference ENT_HeThongTaiKhoan) `FK` |
| 24 | `TaiKhoanLoCLTGThanhToanId` | `tai_khoan_lo_cltg_thanh_toan_id` | `uuid` | Y | — | **[Cấu hình chi tiết - Tiền tệ]** ID TK xử lý lỗ chênh lệch tỷ giá khi thu/trả tiền (reference ENT_HeThongTaiKhoan) `FK` |
| 25 | `ChoPhepTonKhoAm` | `cho_phep_ton_kho_am` | `boolean` | Y | `false` | **[Cấu hình chi tiết - Kho, phân bổ, khác]** Cho phép xuất kho âm |
| 26 | `CauHinhPhanBo` | `cau_hinh_phan_bo` | `text` CHECK | N | — | **[Cấu hình chi tiết - Kho, phân bổ, khác]** Cấu hình phân bổ CCDC/CPTT (TheoNgay \| TheoThang) |
| 27 | `PhanBoHetGTVaoKyCuoi` | `phan_bo_het_gt_vao_ky_cuoi` | `boolean` | N | `false` | **[Cấu hình chi tiết - Kho, phân bổ, khác]** Phân bổ hết giá trị vào kỳ cuối |
| 28 | `CauHinhPhanBoThangDauTien` | `cau_hinh_phan_bo_thang_dau_tien` | `text` CHECK | N | — | **[Cấu hình chi tiết - Kho, phân bổ, khác]** Cấu hình phân bổ tháng đầu tiên (TheoNgay \| TheoThang) |
| 29 | `CanhBaoKeHoachNganSach` | `canh_bao_ke_hoach_ngan_sach` | `text` CHECK | N | — | **[Cấu hình chi tiết - Kho, phân bổ, khác]** Cảnh báo kế hoạch ngân sách (Khong \| CanhBaoVaKhongGhi \| CanhBaoVaGhi) |
| 30 | `Email` | `email` | `text` | N | — | **[Thông tin công ty - Liên hệ và địa chỉ]** Email liên hệ |
| 31 | `SoDienThoai` | `so_dien_thoai` | `text` | N | — | **[Thông tin công ty - Liên hệ và địa chỉ]** Số điện thoại liên hệ |
| 32 | `TaiKhoanNganHangId` | `tai_khoan_ngan_hang_id` | `uuid` | Y | — | **[Thông tin công ty - Liên hệ và địa chỉ]** ID tài khoản ngân hàng mặc định (reference ENT_TaiKhoanNganHang) `FK` |
| 33 | `TinhThanhPhoId` | `tinh_thanh_pho_id` | `uuid` | Y | — | **[Thông tin công ty - Liên hệ và địa chỉ]** ID tỉnh thành phố (reference ENT_TinhThanhPho) `FK` |
| 34 | `PhuongXaId` | `phuong_xa_id` | `uuid` | Y | — | **[Thông tin công ty - Liên hệ và địa chỉ]** ID phường xã (reference ENT_PhuongXa) `FK` |
| 35 | `DiaChiChiTiet` | `dia_chi_chi_tiet` | `text` | Y | — | **[Thông tin công ty - Liên hệ và địa chỉ]** Địa chỉ chi tiết |
| 36 | `TieuDeNguoiKyGiamDoc` | `tieu_de_nguoi_ky_giam_doc` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tiêu đề người ký chức danh Giám đốc |
| 37 | `TenNguoiKyGiamDoc` | `ten_nguoi_ky_giam_doc` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tên người ký chức danh Giám đốc |
| 38 | `TieuDeNguoiKyKeToanTruong` | `tieu_de_nguoi_ky_ke_toan_truong` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tiêu đề người ký chức danh Kế toán trưởng |
| 39 | `TenNguoiKyKeToanTruong` | `ten_nguoi_ky_ke_toan_truong` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tên người ký chức danh Kế toán trưởng |
| 40 | `TieuDeNguoiKyThuKho` | `tieu_de_nguoi_ky_thu_kho` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tiêu đề người ký chức danh Thủ kho |
| 41 | `TenNguoiKyThuKho` | `ten_nguoi_ky_thu_kho` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tên người ký chức danh Thủ kho |
| 42 | `TieuDeNguoiKyThuQuy` | `tieu_de_nguoi_ky_thu_quy` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tiêu đề người ký chức danh Thủ quỹ |
| 43 | `TenNguoiKyThuQuy` | `ten_nguoi_ky_thu_quy` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tên người ký chức danh Thủ quỹ |
| 44 | `TieuDeNguoiKyNguoiLapPhieu` | `tieu_de_nguoi_ky_nguoi_lap_phieu` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tiêu đề người ký chức danh Người lập phiếu |
| 45 | `TenNguoiKyNguoiLapPhieu` | `ten_nguoi_ky_nguoi_lap_phieu` | `text` | Y | — | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Tên người ký chức danh Người lập phiếu |
| 46 | `InTenNguoiKyTrenChungTu` | `in_ten_nguoi_ky_tren_chung_tu` | `boolean` | N | `false` | **[Thông tin công ty - Người ký chứng từ, báo cáo]** In tên người ký trên chứng từ, báo cáo |
| 47 | `LayTenNguoiLapPhieuTuNguoiDungDangNhap` | `lay_ten_nguoi_lap_phieu_tu_nguoi_dung_dang_nhap` | `boolean` | Y | `false` | **[Thông tin công ty - Người ký chứng từ, báo cáo]** Lấy tên người lập phiếu từ người dùng đăng nhập |
| 48 | `NganCachHangNghinTrenGiaoDien` | `ngan_cach_hang_nghin_tren_giao_dien` | `text` CHECK | N | — | **[Định dạng số - Ký tự ngăn cách]** Ngăn cách hàng nghìn trên giao diện (DauCham \| DauPhay) |
| 49 | `NganCachHangThapPhanTrenGiaoDien` | `ngan_cach_hang_thap_phan_tren_giao_dien` | `text` CHECK | N | — | **[Định dạng số - Ký tự ngăn cách]** Ngăn cách thập phân trên giao diện (DauCham \| DauPhay) |
| 50 | `NganCachHangNghinTrenBaoCao` | `ngan_cach_hang_nghin_tren_bao_cao` | `text` CHECK | N | — | **[Định dạng số - Ký tự ngăn cách]** Ngăn cách hàng nghìn trên báo cáo (DauCham \| DauPhay) |
| 51 | `NganCachHangThapPhanTrenBaoCao` | `ngan_cach_hang_thap_phan_tren_bao_cao` | `text` CHECK | N | — | **[Định dạng số - Ký tự ngăn cách]** Ngăn cách thập phân trên báo cáo (DauCham \| DauPhay) |
| 52 | `SoChuSoThapPhanTienQuyDoi` | `so_chu_so_thap_phan_tien_quy_doi` | `integer` | N | `0` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của tiền quy đổi |
| 53 | `SoChuSoThapPhanTienNgoaiTe` | `so_chu_so_thap_phan_tien_ngoai_te` | `integer` | N | `0` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của tiền ngoại tệ |
| 54 | `SoChuSoThapPhanDonGiaQuyDoi` | `so_chu_so_thap_phan_don_gia_quy_doi` | `integer` | N | `0` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của đơn giá quy đổi |
| 55 | `SoChuSoThapPhanDonGiaNgoaiTe` | `so_chu_so_thap_phan_don_gia_ngoai_te` | `integer` | N | `0` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của đơn giá ngoại tệ |
| 56 | `SoChuSoThapPhanSoLuong` | `so_chu_so_thap_phan_so_luong` | `quantity` | N | `0` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của số lượng |
| 57 | `SoChuSoThapPhanTyGia` | `so_chu_so_thap_phan_ty_gia` | `exchange_rate` | N | `1` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của tỷ giá |
| 58 | `SoChuSoThapPhanHeSoTyLe` | `so_chu_so_thap_phan_he_so_ty_le` | `percent_rate` | N | `0` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của hệ số, tỷ lệ |
| 59 | `SoChuSoThapPhanSoCong` | `so_chu_so_thap_phan_so_cong` | `integer` | N | `0` | **[Định dạng số - Số chữ số phần thập phân]** Số chữ số thập phân của số công |
| 60 | `CachTheHienSoAmKyHieu` | `cach_the_hien_so_am_ky_hieu` | `text` CHECK | N | — | **[Định dạng số - Cách thể hiện số âm]** Ký hiệu số âm (DauTru \| NgoacDon) |
| 61 | `CachTheHienSoAmMauSac` | `cach_the_hien_so_am_mau_sac` | `text` CHECK | N | — | **[Định dạng số - Cách thể hiện số âm]** Màu chữ số âm (Do \| Den) |

**Trường base — `TenantedEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `iam_tenant` (76 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `canh_bao_ke_hoach_ngan_sach` |
| DB có — LDM **không khai** | 8 | `ma`, `ten`, `linh_vuc_hoat_dong`, `trang_thai_tenant`, `phien_ban`, `tenant_cha_id`, `nhom_goc_id`, `cap` |

---

## 2. `iam_tenant_linh_vuc_hoat_dong`

| Mục | Nội dung |
|---|---|
| Entity LDM | `Tenant_LinhVucHoatDong` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Lĩnh vực hoạt động của tenant (Link - lựa chọn nhiều giá trị) |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `iam_tenant` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LinhVucHoatDongId` | `linh_vuc_hoat_dong_id` | `uuid` | N | — | ID lĩnh vực hoạt động (reference ENT_LinhVucHoatDong) `FK` |

**Trường base — `TenantedEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

---

## 3. `iam_vai_tro`

| Mục | Nội dung |
|---|---|
| Entity LDM | `VaiTro` |
| Base class | `TenantedEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `iam_vai_tro` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Vai trò trong tenant |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `iam_tenant` — FK `ON DELETE CASCADE` |
| Bảng con | `iam_vai_tro_quyen` · `iam_tai_khoan_vai_tro` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Ma` | `ma` | `varchar(50)` | N | — | Mã vai trò |
| 2 | `Ten` | `ten` | `text` | N | — | Tên vai trò |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | Mô tả vai trò |
| 4 | `LaAdmin` | `la_admin` | `boolean` | N | `false` | Vai trò Admin mặc định của tenant |

**Trường base — `TenantedEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `iam_vai_tro` (11 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 2 | `mo_ta`, `phien_ban` |

---

## 4. `iam_vai_tro_quyen`

| Mục | Nội dung |
|---|---|
| Entity LDM | `VaiTroQuyen` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `iam_vai_tro_quyen` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Quyền được tích của vai trò (mã quyền theo DanhSachQuyen.md) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `iam_vai_tro` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `iam_vai_tro` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `VaiTroId` | `vai_tro_id` | `uuid` | N | — | ID vai trò (reference ENT_VaiTro) `FK` |
| 2 | `MaQuyen` | `ma_quyen` | `varchar(50)` | N | — | Mã quyền chức năng |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `iam_vai_tro_quyen` (11 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `ma_quyen` |
| DB có — LDM **không khai** | 4 | `permission_id`, `pham_vi_loai`, `phien_ban`, `ma_chuc_nang` |

---

## 5. `iam_tai_khoan_vai_tro`

| Mục | Nội dung |
|---|---|
| Entity LDM | `NguoiDungVaiTro` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `iam_tai_khoan_vai_tro` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Gán người dùng vào vai trò (Link) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `iam_vai_tro` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `iam_vai_tro` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | N | — | ID người dùng (reference ENT_NguoiDung) `FK` |
| 2 | `VaiTroId` | `vai_tro_id` | `uuid` | N | — | ID vai trò được gán (reference ENT_VaiTro) `FK` |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `iam_tai_khoan_vai_tro` (6 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `nguoi_dung_id` |
| DB có — LDM **không khai** | 2 | `tai_khoan_id`, `phien_ban` |

---

## 6. `cfg_cau_hinh_email`

| Mục | Nội dung |
|---|---|
| Entity LDM | `CauHinhEmail` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Cấu hình email (tài khoản SMTP gửi thư của tenant; · Screen đang đặt tên entity là EmailConfig) |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng cha | `iam_tenant` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Email` | `email` | `text` | N | — | Địa chỉ email gửi thư |
| 2 | `TenHienThi` | `ten_hien_thi` | `text` | N | — | Tên người gửi hiển thị |
| 3 | `SmtpServer` | `smtp_server` | `text` | N | — | Hostname/IP của máy chủ SMTP |
| 4 | `Port` | `port` | `integer` | N | `0` | Cổng kết nối SMTP |
| 5 | `Protocol` | `protocol` | `text` CHECK | N | — | Giao thức bảo mật (NONE \| SSL \| TLS \| STARTTLS) |
| 6 | `Username` | `username` | `text` | N | — | Tài khoản đăng nhập máy chủ SMTP |
| 7 | `Password` | `password` | `text` | N | — | Mật khẩu tài khoản gửi mail (mã hóa) |
| 8 | `IsDefault` | `is_default` | `boolean` | Y | `false` | Cấu hình mặc định của tenant |
| 9 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | Trạng thái (HoatDong \| NgungHoatDong) |

**Trường base — `TenantedEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

