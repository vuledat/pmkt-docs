# `rpt_` — Báo cáo tài chính

> Sinh tự động từ [`ldm-BaoCaoTaiChinh.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-BaoCaoTaiChinh.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**10 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `BaoCaoTaiChinh` | `rpt_bao_cao_tai_chinh` | `rpt_bao_cao_tai_chinh` | B — có schema, chưa code | Bảng nghiệp vụ — Báo cáo tài chính (một lần lập báo cáo cho một kỳ; các mẫu B01-DN, B02-DN, B03-DN được chọn ở popup chọn kỳ và lưu ở các… |
| 2 | `BaoCaoTinhHinhTaiChinhChiTiet` | `rpt_bao_cao_tinh_hinh_tai_chinh_chi_tiet` | `rpt_bc_tinh_hinh_tai_chinh_chi_tiet` | B — có schema, chưa code | Bảng nghiệp vụ — Chi tiết báo cáo Tình hình tài chính - mẫu B01-DN (Detail) |
| 3 | `BaoCaoKetQuaHoatDongKinhDoanhChiTiet` | `rpt_bao_cao_ket_qua_hoat_dong_kinh_doanh_chi_tiet` | `rpt_bc_ket_qua_hdkd_chi_tiet` | B — có schema, chưa code | Kết quả / số dư luân chuyển — Chi tiết báo cáo Kết quả hoạt động kinh doanh - mẫu B02-DN (Detail) |
| 4 | `BaoCaoLuuChuyenTienTeTrucTiepChiTiet` | `rpt_bao_cao_luu_chuyen_tien_te_truc_tiep_chi_tiet` | — | C — tạo mới | Bảng nghiệp vụ — Chi tiết báo cáo Lưu chuyển tiền tệ - phương pháp trực tiếp (Detail) |
| 5 | `BaoCaoLuuChuyenTienTeGianTiepChiTiet` | `rpt_bao_cao_luu_chuyen_tien_te_gian_tiep_chi_tiet` | `rpt_bc_luu_chuyen_tt_gian_tiep_chi_tiet` | B — có schema, chưa code | Bảng nghiệp vụ — Chi tiết báo cáo Lưu chuyển tiền tệ - phương pháp gián tiếp (Detail) |
| 6 | `ThietLapChiTieu` | `rpt_thiet_lap_chi_tieu` | `rpt_thiet_lap_chi_tieu` | B — có schema, chưa code | Cấu hình / thiết lập — Thiết lập chỉ tiêu báo cáo (danh sách chỉ tiêu của từng mẫu báo cáo) |
| 7 | `ThietLapCongThuc` | `rpt_thiet_lap_cong_thuc` | `rpt_thiet_lap_cong_thuc` | B — có schema, chưa code | Cấu hình / thiết lập — Thiết lập công thức của chỉ tiêu (mỗi dòng là một thành phần công thức) |
| 8 | `HoatDongChungTu` | `rpt_hoat_dong_chung_tu` | `rpt_hoat_dong_chung_tu` | B — có schema, chưa code | Bảng nghiệp vụ — Phân loại hoạt động/nghiệp vụ cho chứng từ, ở mức TỪNG DÒNG BÚT TOÁN (dùng cho Chọn hoạt động - LCTT và Chọn nghiệp vụ -… |
| 9 | `HoatDongSoDuCongNo` | `rpt_hoat_dong_so_du_cong_no` | `rpt_hoat_dong_so_du_cong_no` | B — có schema, chưa code | Bảng nghiệp vụ — Phân loại hoạt động cho số dư ban đầu của tài khoản chi tiết theo đối tượng (Bước 1 - Lưu chuyển tiền tệ gián tiếp) |
| 10 | `HoatDongSoDuTaiKhoan` | `rpt_hoat_dong_so_du_tai_khoan` | `rpt_hoat_dong_so_du_tai_khoan` | B — có schema, chưa code | Bảng nghiệp vụ — Phân bổ hoạt động cho số dư ban đầu của tài khoản không chi tiết theo đối tượng (Bước 2 - Lưu chuyển tiền tệ gián tiếp) |

---

## 1. `rpt_bao_cao_tai_chinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BaoCaoTaiChinh` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_bao_cao_tai_chinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Báo cáo tài chính (một lần lập báo cáo cho một kỳ; các mẫu B01-DN, · B02-DN, B03-DN được chọn ở popup chọn kỳ và lưu ở các entity chi tiết) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `rpt_bao_cao_tinh_hinh_tai_chinh_chi_tiet` · `rpt_bao_cao_ket_qua_hoat_dong_kinh_doanh_chi_tiet` · `rpt_bao_cao_luu_chuyen_tien_te_truc_tiep_chi_tiet` · `rpt_bao_cao_luu_chuyen_tien_te_gian_tiep_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Ten` | `ten` | `text` | N | — | **[Thông tin chung của báo cáo]** Tên báo cáo, tối đa 255 ký tự |
| 2 | `Loai` | `loai` | `text` CHECK | N | — | **[Thông tin chung của báo cáo]** Loại báo cáo (BaoCaoTaiChinh \| ThuyetMinh \| BaoCaoTaiChinhGiuaNienDo); 4 epic lập BCTC hiện tại luôn gán BaoCaoTaiChinh |
| 3 | `NgayLap` | `ngay_lap` | `date` | N | — | **[Thông tin chung của báo cáo]** Ngày lập báo cáo |
| 4 | `NguoiLap` | `nguoi_lap` | `text` | N | — | **[Thông tin chung của báo cáo]** Người lập báo cáo, tối đa 100 ký tự |
| 5 | `KeToanTruong` | `ke_toan_truong` | `text` | N | — | **[Thông tin chung của báo cáo]** Kế toán trưởng, tối đa 100 ký tự |
| 6 | `NguoiDaiDienPhapLuat` | `nguoi_dai_dien_phap_luat` | `text` | N | — | **[Thông tin chung của báo cáo]** Người đại diện pháp luật (Giám đốc), tối đa 100 ký tự |
| 7 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Thông tin chung của báo cáo]** Trạng thái nộp cơ quan thuế (ChuaNop \| DaNopCQT \| CQTChapNhan — miền thống nhất với tờ khai bên ldm-Thue-Update) |
| 8 | `Nam` | `nam` | `integer` | N | `0` | **[Tham số kỳ báo cáo đã chọn (giữ lại để tính lại số liệu và hiển thị tiêu đề cột)]** Năm của kỳ báo cáo |
| 9 | `KhoangThoiGian` | `khoang_thoi_gian` | `text` CHECK | N | — | **[Tham số kỳ báo cáo đã chọn (giữ lại để tính lại số liệu và hiển thị tiêu đề cột)]** Khoảng thời gian kỳ báo cáo (Nam \| Quy1 \| Quy2 \| Quy3 \| Quy4 \| SauThangDauNam \| SauThangCuoiNam \| Thang1 \| Thang2 \| Thang3 \| Thang4 \| Thang5 \| Thang6 \| Thang7 \| Thang8 \| Thang9 \| Thang10 \| Thang11 \| Thang12 \| TuyChon) |
| 10 | `NgayTu` | `ngay_tu` | `date` | N | — | **[Tham số kỳ báo cáo đã chọn (giữ lại để tính lại số liệu và hiển thị tiêu đề cột)]** Từ ngày của kỳ này |
| 11 | `NgayDen` | `ngay_den` | `date` | N | — | **[Tham số kỳ báo cáo đã chọn (giữ lại để tính lại số liệu và hiển thị tiêu đề cột)]** Đến ngày của kỳ này |
| 12 | `ThietLapKyTruoc` | `thiet_lap_ky_truoc` | `boolean` | Y | `false` | **[Tham số kỳ báo cáo đã chọn (giữ lại để tính lại số liệu và hiển thị tiêu đề cột)]** Có thiết lập chi tiết khoảng thời gian kỳ trước hay không |
| 13 | `NgayTuKyTruoc` | `ngay_tu_ky_truoc` | `date` | Y | — | **[Tham số kỳ báo cáo đã chọn (giữ lại để tính lại số liệu và hiển thị tiêu đề cột)]** Từ ngày của kỳ trước |
| 14 | `NgayDenKyTruoc` | `ngay_den_ky_truoc` | `date` | Y | — | **[Tham số kỳ báo cáo đã chọn (giữ lại để tính lại số liệu và hiển thị tiêu đề cột)]** Đến ngày của kỳ trước |

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

**Đối chiếu `rpt_bao_cao_tai_chinh` (23 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `khoang_thoi_gian`, `thiet_lap_ky_truoc` |
| DB có — LDM **không khai** | 2 | `ma_mau_bao_cao`, `phien_ban` |

---

## 2. `rpt_bao_cao_tinh_hinh_tai_chinh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BaoCaoTinhHinhTaiChinhChiTiet` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_bc_tinh_hinh_tai_chinh_chi_tiet` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết báo cáo Tình hình tài chính - mẫu B01-DN (Detail) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `rpt_bao_cao_tai_chinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `BaoCaoTaiChinhId` | `bao_cao_tai_chinh_id` | `uuid` | N | — | ID báo cáo tài chính (reference ENT_BaoCaoTaiChinh) `FK` |
| 2 | `ThietLapChiTieuId` | `thiet_lap_chi_tieu_id` | `uuid` | N | — | ID chỉ tiêu của mẫu Tình hình tài chính đã dùng để lập báo cáo (reference ENT_ThietLapChiTieu) `FK` |
| 3 | `MaChiTieu` | `ma_chi_tieu` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã chỉ tiêu (mã số) |
| 4 | `TenChiTieu` | `ten_chi_tieu` | `text` | N | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu |
| 5 | `TenChiTieuTiengAnh` | `ten_chi_tieu_tieng_anh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu bằng tiếng Anh |
| 6 | `MaThuyetMinh` | `ma_thuyet_minh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã thuyết minh của chỉ tiêu |
| 7 | `In` | `in` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Hiển thị chỉ tiêu trên báo cáo |
| 8 | `InDam` | `in_dam` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in đậm |
| 9 | `InNghieng` | `in_nghieng` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in nghiêng |
| 10 | `SoCuoiNam` | `so_cuoi_nam` | `numeric(18,4)` ⚠ | N | `0` | **[Số liệu báo cáo]** Số cuối năm/cuối quý/cuối kỳ, tính theo công thức tại thời điểm NgayDen; mặc định 0 |
| 11 | `SoDauNam` | `so_dau_nam` | `numeric(18,4)` ⚠ | N | `0` | **[Số liệu báo cáo]** Số đầu năm/đầu quý/đầu kỳ, tính theo công thức tại thời điểm NgayTu - 1; mặc định 0 |

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

**Đối chiếu `rpt_bc_tinh_hinh_tai_chinh_chi_tiet` (18 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `ten_chi_tieu_tieng_anh`, `in`, `in_dam`, `in_nghieng` |
| DB có — LDM **không khai** | 2 | `thu_tu`, `phien_ban` |

---

## 3. `rpt_bao_cao_ket_qua_hoat_dong_kinh_doanh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BaoCaoKetQuaHoatDongKinhDoanhChiTiet` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_bc_ket_qua_hdkd_chi_tiet` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết báo cáo Kết quả hoạt động kinh doanh - mẫu B02-DN (Detail) |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |
| Bảng cha | `rpt_bao_cao_tai_chinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `BaoCaoTaiChinhId` | `bao_cao_tai_chinh_id` | `uuid` | N | — | ID báo cáo tài chính (reference ENT_BaoCaoTaiChinh) `FK` |
| 2 | `ThietLapChiTieuId` | `thiet_lap_chi_tieu_id` | `uuid` | N | — | ID chỉ tiêu của mẫu Kết quả hoạt động kinh doanh đã dùng để lập báo cáo (reference ENT_ThietLapChiTieu) `FK` |
| 3 | `MaChiTieu` | `ma_chi_tieu` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã chỉ tiêu (mã số) |
| 4 | `TenChiTieu` | `ten_chi_tieu` | `text` | N | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu |
| 5 | `TenChiTieuTiengAnh` | `ten_chi_tieu_tieng_anh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu bằng tiếng Anh |
| 6 | `MaThuyetMinh` | `ma_thuyet_minh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã thuyết minh của chỉ tiêu |
| 7 | `In` | `in` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Hiển thị chỉ tiêu trên báo cáo |
| 8 | `InDam` | `in_dam` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in đậm |
| 9 | `InNghieng` | `in_nghieng` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in nghiêng |
| 10 | `SoNamNay` | `so_nam_nay` | `integer` | N | `0` | **[Số liệu báo cáo]** Số năm nay/quý này/kỳ này, tính theo khoảng thời gian kỳ này; mặc định 0 |
| 11 | `SoNamTruoc` | `so_nam_truoc` | `integer` | N | `0` | **[Số liệu báo cáo]** Số năm trước/quý trước/kỳ trước, tính theo khoảng thời gian kỳ trước; mặc định 0 |

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

**Đối chiếu `rpt_bc_ket_qua_hdkd_chi_tiet` (18 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `ten_chi_tieu_tieng_anh`, `in`, `in_dam`, `in_nghieng` |
| DB có — LDM **không khai** | 2 | `thu_tu`, `phien_ban` |

---

## 4. `rpt_bao_cao_luu_chuyen_tien_te_truc_tiep_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BaoCaoLuuChuyenTienTeTrucTiepChiTiet` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết báo cáo Lưu chuyển tiền tệ - phương pháp trực tiếp (Detail) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `rpt_bao_cao_tai_chinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `BaoCaoTaiChinhId` | `bao_cao_tai_chinh_id` | `uuid` | N | — | ID báo cáo tài chính (reference ENT_BaoCaoTaiChinh) `FK` |
| 2 | `ThietLapChiTieuId` | `thiet_lap_chi_tieu_id` | `uuid` | N | — | ID chỉ tiêu của mẫu Lưu chuyển tiền tệ trực tiếp đã dùng để lập báo cáo (reference ENT_ThietLapChiTieu) `FK` |
| 3 | `MaChiTieu` | `ma_chi_tieu` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã chỉ tiêu (mã số) |
| 4 | `TenChiTieu` | `ten_chi_tieu` | `text` | N | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu |
| 5 | `TenChiTieuTiengAnh` | `ten_chi_tieu_tieng_anh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu bằng tiếng Anh |
| 6 | `MaThuyetMinh` | `ma_thuyet_minh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã thuyết minh của chỉ tiêu |
| 7 | `In` | `in` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Hiển thị chỉ tiêu trên báo cáo |
| 8 | `InDam` | `in_dam` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in đậm |
| 9 | `InNghieng` | `in_nghieng` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in nghiêng |
| 10 | `SoNamNay` | `so_nam_nay` | `integer` | N | `0` | **[Số liệu báo cáo]** Số năm nay/quý này/kỳ này, tính theo khoảng thời gian kỳ này; mặc định 0 |
| 11 | `SoNamTruoc` | `so_nam_truoc` | `integer` | N | `0` | **[Số liệu báo cáo]** Số năm trước/quý trước/kỳ trước, tính theo khoảng thời gian kỳ trước; mặc định 0 |

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

## 5. `rpt_bao_cao_luu_chuyen_tien_te_gian_tiep_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BaoCaoLuuChuyenTienTeGianTiepChiTiet` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_bc_luu_chuyen_tt_gian_tiep_chi_tiet` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết báo cáo Lưu chuyển tiền tệ - phương pháp gián tiếp (Detail) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `rpt_bao_cao_tai_chinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `BaoCaoTaiChinhId` | `bao_cao_tai_chinh_id` | `uuid` | N | — | ID báo cáo tài chính (reference ENT_BaoCaoTaiChinh) `FK` |
| 2 | `ThietLapChiTieuId` | `thiet_lap_chi_tieu_id` | `uuid` | N | — | ID chỉ tiêu của mẫu Lưu chuyển tiền tệ gián tiếp đã dùng để lập báo cáo (reference ENT_ThietLapChiTieu) `FK` |
| 3 | `MaChiTieu` | `ma_chi_tieu` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã chỉ tiêu (mã số) |
| 4 | `TenChiTieu` | `ten_chi_tieu` | `text` | N | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu |
| 5 | `TenChiTieuTiengAnh` | `ten_chi_tieu_tieng_anh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Tên chỉ tiêu bằng tiếng Anh |
| 6 | `MaThuyetMinh` | `ma_thuyet_minh` | `text` | Y | — | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Mã thuyết minh của chỉ tiêu |
| 7 | `In` | `in` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Hiển thị chỉ tiêu trên báo cáo |
| 8 | `InDam` | `in_dam` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in đậm |
| 9 | `InNghieng` | `in_nghieng` | `boolean` | N | `false` | **[Snapshot chỉ tiêu tại thời điểm lập báo cáo, giữ nguyên khi thiết lập bị sửa về sau]** Định dạng in nghiêng |
| 10 | `SoNamNay` | `so_nam_nay` | `integer` | N | `0` | **[Số liệu báo cáo]** Số năm nay/quý này/kỳ này, tính theo khoảng thời gian kỳ này; mặc định 0 |
| 11 | `SoNamTruoc` | `so_nam_truoc` | `integer` | N | `0` | **[Số liệu báo cáo]** Số năm trước/quý trước/kỳ trước, tính theo khoảng thời gian kỳ trước; mặc định 0 |

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

**Đối chiếu `rpt_bc_luu_chuyen_tt_gian_tiep_chi_tiet` (18 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `ten_chi_tieu_tieng_anh`, `in`, `in_dam`, `in_nghieng` |
| DB có — LDM **không khai** | 2 | `thu_tu`, `phien_ban` |

---

## 6. `rpt_thiet_lap_chi_tieu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThietLapChiTieu` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_thiet_lap_chi_tieu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Thiết lập chỉ tiêu báo cáo (danh sách chỉ tiêu của từng mẫu báo cáo) |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng con | `rpt_thiet_lap_cong_thuc` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiBaoCao` | `loai_bao_cao` | `text` CHECK | N | — | Mẫu báo cáo áp dụng thiết lập (TinhHinhTaiChinh \| KetQuaHoatDongKinhDoanh \| LuuChuyenTienTeTrucTiep \| LuuChuyenTienTeGianTiep) |
| 2 | `MaChiTieu` | `ma_chi_tieu` | `text` | Y | — | **[Nội dung chỉ tiêu]** Mã chỉ tiêu, duy nhất trong cùng một mẫu báo cáo khi khác rỗng |
| 3 | `TenChiTieu` | `ten_chi_tieu` | `text` | N | — | **[Nội dung chỉ tiêu]** Tên chỉ tiêu |
| 4 | `TenChiTieuTiengAnh` | `ten_chi_tieu_tieng_anh` | `text` | Y | — | **[Nội dung chỉ tiêu]** Tên chỉ tiêu bằng tiếng Anh |
| 5 | `ThuyetMinh` | `thuyet_minh` | `text` | Y | — | **[Nội dung chỉ tiêu]** Mã thuyết minh của chỉ tiêu (VD: V.1, VI.2) |
| 6 | `LoaiChiTieu` | `loai_chi_tieu` | `text` CHECK | N | — | **[Nội dung chỉ tiêu]** Loại chỉ tiêu (TongHop \| ChiTiet \| ChiTietChiLayGiaTriLonHonKhong) |
| 7 | `In` | `in` | `boolean` | Y | `false` | **[Định dạng hiển thị và in]** Hiển thị chỉ tiêu ra màn hình báo cáo |
| 8 | `InDam` | `in_dam` | `boolean` | Y | `false` | **[Định dạng hiển thị và in]** Định dạng in đậm |
| 9 | `InNghieng` | `in_nghieng` | `boolean` | Y | `false` | **[Định dạng hiển thị và in]** Định dạng in nghiêng |
| 10 | `DaSuaCT` | `da_sua_ct` | `boolean` | N | `false` | **[Định dạng hiển thị và in]** Công thức của chỉ tiêu đã khác giá trị mặc định của hệ thống, không cho người dùng sửa |

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

**Đối chiếu `rpt_thiet_lap_chi_tieu` (11 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 9 | `ma_chi_tieu`, `ten_chi_tieu`, `ten_chi_tieu_tieng_anh`, `thuyet_minh`, `loai_chi_tieu`, `in`, `in_dam`, `in_nghieng`, `da_sua_ct` |
| DB có — LDM **không khai** | 4 | `ma`, `ten`, `trang_thai`, `phien_ban` |

---

## 7. `rpt_thiet_lap_cong_thuc`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThietLapCongThuc` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_thiet_lap_cong_thuc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Thiết lập công thức của chỉ tiêu (mỗi dòng là một thành phần công thức) |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng cha | `rpt_thiet_lap_chi_tieu` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ThietLapChiTieuId` | `thiet_lap_chi_tieu_id` | `uuid` | N | — | ID chỉ tiêu được thiết lập công thức (reference ENT_ThietLapChiTieu) `FK` |
| 2 | `PhepTinh` | `phep_tinh` | `text` CHECK | N | — | Phép tính của dòng công thức (Cong \| Tru) |
| 3 | `MaThamSo` | `ma_tham_so` | `text` | Y | — | **[Dòng công thức của chỉ tiêu loại Chi tiết]** Mã tham số theo danh sách tham số của từng mẫu báo cáo (VD: DU_NO, DU_CO_TK_DT, PS_CO, PS_DU_KD, DUNOCK_ChiTietTheoHD_SXKD) |
| 4 | `TenThamSo` | `ten_tham_so` | `text` | Y | — | **[Dòng công thức của chỉ tiêu loại Chi tiết]** Tên tham số tương ứng với Mã tham số |
| 5 | `TaiKhoanNo` | `tai_khoan_no` | `text` | Y | — | **[Dòng công thức của chỉ tiêu loại Chi tiết]** Số hiệu tài khoản nợ, cho phép nhập một phần ký tự đầu và đối chiếu theo dạng like (ánh xạ sang ENT_HeThongTaiKhoan) |
| 6 | `TaiKhoanCo` | `tai_khoan_co` | `text` | Y | — | **[Dòng công thức của chỉ tiêu loại Chi tiết]** Số hiệu tài khoản có, cho phép nhập một phần ký tự đầu và đối chiếu theo dạng like (ánh xạ sang ENT_HeThongTaiKhoan) |
| 7 | `MaChiTieu` | `ma_chi_tieu` | `text` | Y | — | **[Dòng công thức của chỉ tiêu loại Tổng hợp]** Mã chỉ tiêu được tham chiếu trong công thức tổng hợp |
| 8 | `TenChiTieu` | `ten_chi_tieu` | `text` | Y | — | **[Dòng công thức của chỉ tiêu loại Tổng hợp]** Tên chỉ tiêu được tham chiếu, tự động fill theo Mã chỉ tiêu |

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

**Đối chiếu `rpt_thiet_lap_cong_thuc` (19 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 2 | `thu_tu`, `phien_ban` |

---

## 8. `rpt_hoat_dong_chung_tu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HoatDongChungTu` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_hoat_dong_chung_tu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phân loại hoạt động/nghiệp vụ cho chứng từ, ở mức TỪNG DÒNG BÚT TOÁN · (dùng cho Chọn hoạt động - LCTT và Chọn nghiệp vụ - KQHĐKD; lưu độc lập với · từng lần lập báo cáo). Khóa duy nhất: ChiTietChungTuId |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChiTietChungTuId` | `chi_tiet_chung_tu_id` | `uuid` | N | — | ID dòng bút toán được phân loại, duy nhất, mỗi dòng bút toán là một bản ghi, các dòng bút toán giống nhau không gộp (FK đa hình — dòng hạch toán của chứng từ ghi sổ, entity xác định theo loại chứng từ) `FK` |
| 2 | `ChungTuId` | `chung_tu_id` | `uuid` | N | — | ID chứng từ chứa dòng bút toán, dùng để lọc theo kỳ báo cáo và sắp xếp danh sách (FK đa hình — chứng từ ghi sổ, entity xác định theo loại chứng từ) `FK` |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin dòng bút toán hiển thị trên danh sách phân loại]** Diễn giải của dòng bút toán |
| 4 | `TaiKhoanNo` | `tai_khoan_no` | `text` | Y | — | **[Thông tin dòng bút toán hiển thị trên danh sách phân loại]** Số hiệu tài khoản nợ của dòng bút toán |
| 5 | `TaiKhoanCo` | `tai_khoan_co` | `text` | Y | — | **[Thông tin dòng bút toán hiển thị trên danh sách phân loại]** Số hiệu tài khoản có của dòng bút toán |
| 6 | `HoatDong` | `hoat_dong` | `text` CHECK | Y | — | **[Kết quả phân loại]** Loại hoạt động lưu chuyển tiền tệ (KinhDoanh \| DauTu \| TaiChinh \| DanhGiaChenhLechTyGia \| Trong) |
| 7 | `NghiepVu` | `nghiep_vu` | `text` CHECK | Y | — | **[Kết quả phân loại]** Loại nghiệp vụ phát sinh (ThanhLyNhuongBanTSCD \| BanBatDongSanDauTu \| DanhGiaLaiTaiSanGopVonDauTu \| BanThuHoiDauTuTaiChinh \| LaiChoVayLaiTienGuiCoTucLoiNhuanDuocChia \| ChiPhiLaiVayChiTraLaiVay \| DanhGiaLaiTaiKhoanNgoaiTe \| ChenhLechTyGiaKhiThanhToanDauTuTaiChinh \| Trong) |

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

**Đối chiếu `rpt_hoat_dong_chung_tu` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `dien_giai`, `tai_khoan_no`, `tai_khoan_co` |
| DB có — LDM **không khai** | 2 | `loai_chung_tu_id`, `phien_ban` |

---

## 9. `rpt_hoat_dong_so_du_cong_no`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HoatDongSoDuCongNo` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_hoat_dong_so_du_cong_no` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phân loại hoạt động cho số dư ban đầu của tài khoản chi tiết theo · đối tượng (Bước 1 - Lưu chuyển tiền tệ gián tiếp) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản của dòng số dư công nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 2 | `LoaiDoiTuong` | `loai_doi_tuong` | `text` CHECK | N | — | Loại đối tượng công nợ, xác định danh mục mà DoiTuongId trỏ tới (KhachHangCaNhan \| KhachHangToChuc \| NhaCungCapCaNhan \| NhaCungCapToChuc \| NhanVien) |
| 3 | `DoiTuongId` | `doi_tuong_id` | `uuid` | N | — | ID đối tượng công nợ, theo LoaiDoiTuong (reference ENT_DoiTuong vai trò Khách hàng / Nhà cung cấp / Nhân viên) `FK` |
| 4 | `LoaiHoatDong` | `loai_hoat_dong` | `text` CHECK | Y | — | Loại hoạt động lưu chuyển tiền tệ của số dư (KinhDoanh \| DauTu \| TaiChinh \| Trong) |

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

**Đối chiếu `rpt_hoat_dong_so_du_cong_no` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 10. `rpt_hoat_dong_so_du_tai_khoan`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HoatDongSoDuTaiKhoan` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `rpt_hoat_dong_so_du_tai_khoan` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phân bổ hoạt động cho số dư ban đầu của tài khoản không chi tiết theo · đối tượng (Bước 2 - Lưu chuyển tiền tệ gián tiếp) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản được phân bổ số dư (reference ENT_HeThongTaiKhoan) `FK` |
| 2 | `SoTienKinhDoanh` | `so_tien_kinh_doanh` | `money_foreign` ≈ | N | `0` | Số tiền số dư phân bổ cho hoạt động kinh doanh; mặc định 0 |
| 3 | `SoTienDauTu` | `so_tien_dau_tu` | `money_foreign` ≈ | N | `0` | Số tiền số dư phân bổ cho hoạt động đầu tư; mặc định 0 |
| 4 | `SoTienTaiChinh` | `so_tien_tai_chinh` | `money_foreign` ≈ | N | `0` | Số tiền số dư phân bổ cho hoạt động tài chính; mặc định 0 |

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

**Đối chiếu `rpt_hoat_dong_so_du_tai_khoan` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

