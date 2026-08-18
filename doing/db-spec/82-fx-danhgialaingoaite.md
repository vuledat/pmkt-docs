# `fx_` — Đánh giá lại ngoại tệ

> Sinh tự động từ [`ldm-DanhGiaLaiNgoaiTe.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-DanhGiaLaiNgoaiTe.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**5 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> Mọi trường kiểu numeric đều NOT NULL (numeric!). Bộ trường hệ thống (DaXoa, NguoiTao, ThoiGianTao, NguoiCapNhat, ThoiGianCapNhat, NguoiGhiSo, ThoiGianGhiSo, NguoiXoa, ThoiGianXoa) áp dụng cho mọi entity theo BR46 - Common/business_rules.md, không khai báo lại ở đây. Trường đa hình (DoiTuongId, DoiTuongNoId, DoiTuongCoId, ChungTuGocId) luôn lưu kèm trường phân loại tương ứng làm discriminator.

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `PhieuDanhGiaLaiNgoaiTe` | `fx_phieu_danh_gia_lai_ngoai_te` | — | C — tạo mới | Đầu chứng từ — Phiếu đánh giá lại tài khoản ngoại tệ (Master) |
| 2 | `ChiTietDanhGiaLaiNgoaiTe_SoDu` | `fx_phieu_danh_gia_lai_ngoai_te_so_du` | — | C — tạo mới | Liên kết N–N — Chi tiết số dư ngoại tệ (Detail) |
| 3 | `ChiTietDanhGiaLaiNgoaiTe_CongNo` | `fx_phieu_danh_gia_lai_ngoai_te_cong_no` | — | C — tạo mới | Đầu chứng từ — Chi tiết chứng từ công nợ và thanh toán (Detail) |
| 4 | `ChiTietDanhGiaLaiNgoaiTe_HachToan` | `fx_phieu_danh_gia_lai_ngoai_te_hach_toan` | — | C — tạo mới | Liên kết N–N — Chi tiết hạch toán chênh lệch tỷ giá (Detail) |
| 5 | `KetQuaTinhTyGiaXuatQuy` | `fx_ket_qua_tinh_ty_gia_xuat_quy` | — | C — tạo mới | Kết quả / số dư luân chuyển — Kết quả tính tỷ giá xuất quỹ theo kỳ |

---

## 1. `fx_phieu_danh_gia_lai_ngoai_te`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuDanhGiaLaiNgoaiTe` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu đánh giá lại tài khoản ngoại tệ (Master) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `fx_phieu_danh_gia_lai_ngoai_te_so_du` · `fx_phieu_danh_gia_lai_ngoai_te_cong_no` · `fx_phieu_danh_gia_lai_ngoai_te_hach_toan` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tham số đánh giá lại]** ID loại ngoại tệ được đánh giá lại (reference ENT_LoaiTien) `FK` |
| 2 | `DenNgay` | `den_ngay` | `date` | N | — | **[Tham số đánh giá lại]** Đánh giá số dư đến ngày |
| 3 | `TyGiaDanhGiaLai` | `ty_gia_danh_gia_lai` | `exchange_rate` | N | `1` | **[Tham số đánh giá lại]** Tỷ giá đánh giá lại |
| 4 | `TaiKhoanLaiId` | `tai_khoan_lai_id` | `uuid` | N | — | **[Tham số đánh giá lại]** ID tài khoản xử lý lãi chênh lệch tỷ giá (reference ENT_HeThongTaiKhoan) `FK` |
| 5 | `TaiKhoanLoId` | `tai_khoan_lo_id` | `uuid` | N | — | **[Tham số đánh giá lại]** ID tài khoản xử lý lỗ chênh lệch tỷ giá (reference ENT_HeThongTaiKhoan) `FK` |
| 6 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |
| 7 | `TongTien` | `tong_tien` | `money_foreign` ≈ | N | `0` | **[Đầu chứng từ]** Tổng số tiền các bút toán |
| 8 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Đầu chứng từ]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

**Trường base — `BaseChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4 |
| `phien_ban` | `integer` | N | `1` | Khóa lạc quan `@Version`. `AggregateRootEntity` |
| `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4 |
| `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4 |
| `giao_dich_chung_tu_id` | `uuid` | Y | — | Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity` |
| `so_chung_tu` | `varchar(50)` | N | — | Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20 |
| `ngay_chung_tu` | `date` | N | — | Ngày lập chứng từ. `BaseChungTuEntity` |
| `ngay_hach_toan` | `date` | N | — | Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37 |
| `status` | `text` | N | `NHAP` | Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12 |
| `nguoi_duyet_id` | `uuid` | Y | — | Người duyệt. `BaseChungTuEntity` |
| `ngay_duyet` | `timestamptz` | Y | — | Thời điểm duyệt. `BaseChungTuEntity` |
| `nguoi_ghi_so` | `uuid` | Y | — | Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `thoi_gian_ghi_so` | `timestamptz` | Y | — | Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo, gán một lần. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo, gán một lần. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

---

## 2. `fx_phieu_danh_gia_lai_ngoai_te_so_du`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDanhGiaLaiNgoaiTe_SoDu` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết số dư ngoại tệ (Detail) |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `fx_phieu_danh_gia_lai_ngoai_te` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuDanhGiaLaiNgoaiTeId` | `phieu_danh_gia_lai_ngoai_te_id` | `uuid` | N | — | ID phiếu đánh giá lại (reference ENT_PhieuDanhGiaLaiNgoaiTe) `FK` |
| 2 | `DaChon` | `da_chon` | `boolean` | Y | `false` | Dòng được tích chọn tham gia sinh bút toán |
| 3 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | **[Khóa đánh giá lại]** ID tài khoản được đánh giá lại (reference ENT_HeThongTaiKhoan) `FK` |
| 4 | `TaiKhoanNganHangId` | `tai_khoan_ngan_hang_id` | `uuid` | Y | — | **[Khóa đánh giá lại]** ID tài khoản ngân hàng (reference ENT_TaiKhoanNganHang) `FK` |
| 5 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Khóa đánh giá lại]** ID đối tượng (reference ENT_DoiTuong) `FK` |
| 6 | `LoaiDoiTuong` | `loai_doi_tuong` | `text` CHECK | Y | — | **[Khóa đánh giá lại]** Loại đối tượng (KhachHang \| NhaCungCap \| NhanVien) |
| 7 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Khóa đánh giá lại]** Tên đối tượng |
| 8 | `TyGiaDanhGiaLai` | `ty_gia_danh_gia_lai` | `exchange_rate` | N | `1` | **[Số dư Nợ]** Tỷ giá đánh giá lại của dòng |
| 9 | `SoDuNoNguyenTe` | `so_du_no_nguyen_te` | `money_foreign` ≈ | N | `0` | **[Số dư Nợ]** Số dư Nợ nguyên tệ |
| 10 | `SoDuNoQuyDoi` | `so_du_no_quy_doi` | `money_vnd` | N | `0` | **[Số dư Nợ]** Số dư Nợ quy đổi |
| 11 | `DanhGiaLaiNo` | `danh_gia_lai_no` | `money_foreign` ≈ | N | `0` | **[Số dư Nợ]** Giá trị đánh giá lại vế Nợ |
| 12 | `ChenhLechNo` | `chenh_lech_no` | `money_foreign` ≈ | N | `0` | **[Số dư Nợ]** Chênh lệch vế Nợ |
| 13 | `SoDuCoNguyenTe` | `so_du_co_nguyen_te` | `money_foreign` ≈ | N | `0` | **[Số dư Có]** Số dư Có nguyên tệ |
| 14 | `SoDuCoQuyDoi` | `so_du_co_quy_doi` | `money_vnd` | N | `0` | **[Số dư Có]** Số dư Có quy đổi |
| 15 | `DanhGiaLaiCo` | `danh_gia_lai_co` | `money_foreign` ≈ | N | `0` | **[Số dư Có]** Giá trị đánh giá lại vế Có |
| 16 | `ChenhLechCo` | `chenh_lech_co` | `money_foreign` ≈ | N | `0` | **[Số dư Có]** Chênh lệch vế Có |

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

## 3. `fx_phieu_danh_gia_lai_ngoai_te_cong_no`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDanhGiaLaiNgoaiTe_CongNo` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết chứng từ công nợ và thanh toán (Detail) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `fx_phieu_danh_gia_lai_ngoai_te` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuDanhGiaLaiNgoaiTeId` | `phieu_danh_gia_lai_ngoai_te_id` | `uuid` | N | — | ID phiếu đánh giá lại (reference ENT_PhieuDanhGiaLaiNgoaiTe) `FK` |
| 2 | `ChungTuGocId` | `chung_tu_goc_id` | `uuid` | N | — | **[Chứng từ công nợ gốc]** ID chứng từ công nợ gốc |
| 3 | `LoaiChungTuGoc` | `loai_chung_tu_goc` | `text` CHECK | N | — | **[Chứng từ công nợ gốc]** Loại chứng từ gốc (ChungTuBan \| ChungTuMuaHang \| PhieuThu \| PhieuChi \| PhieuKeToanTongHop) — theo tên entity đã gộp: ChungTuBan gộp bán hàng + dịch vụ, ChungTuMuaHang gộp mua dịch vụ, PhieuThu/PhieuChi gộp tiền mặt + tiền gửi (phân biệt bằng PhuongThucThanhToan) |
| 4 | `SoHoaDon` | `so_hoa_don` | `varchar(50)` | Y | — | **[Chứng từ công nợ gốc]** Số hóa đơn |
| 5 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Chứng từ công nợ gốc]** Diễn giải |
| 6 | `TaiKhoanCongNoId` | `tai_khoan_cong_no_id` | `uuid` | N | — | **[Khóa tổng hợp lên tab Số dư ngoại tệ]** ID tài khoản công nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 7 | `DoiTuongId` | `doi_tuong_id` | `uuid` | N | — | **[Khóa tổng hợp lên tab Số dư ngoại tệ]** ID đối tượng công nợ (reference ENT_DoiTuong) `FK` |
| 8 | `LoaiDoiTuong` | `loai_doi_tuong` | `text` CHECK | N | — | **[Khóa tổng hợp lên tab Số dư ngoại tệ]** Loại đối tượng (KhachHang \| NhaCungCap \| NhanVien) |
| 9 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Khóa tổng hợp lên tab Số dư ngoại tệ]** Tên đối tượng |
| 10 | `TyGiaTrenCT` | `ty_gia_tren_ct` | `exchange_rate` | N | `1` | **[Số liệu đánh giá lại]** Tỷ giá trên chứng từ gốc |
| 11 | `TyGiaDanhGiaLaiGanNhat` | `ty_gia_danh_gia_lai_gan_nhat` | `exchange_rate` | N | `1` | **[Số liệu đánh giá lại]** Tỷ giá đánh giá lại gần nhất |
| 12 | `SoChuaDoiTru` | `so_chua_doi_tru` | `numeric(18,4)` ⚠ | N | `0` | **[Số liệu đánh giá lại]** Số chưa đối trừ nguyên tệ |
| 13 | `SoChuaDoiTruQuyDoi` | `so_chua_doi_tru_quy_doi` | `money_vnd` | N | `0` | **[Số liệu đánh giá lại]** Số chưa đối trừ quy đổi |
| 14 | `DanhGiaLai` | `danh_gia_lai` | `numeric(18,4)` ⚠ | N | `0` | **[Số liệu đánh giá lại]** Giá trị đánh giá lại |
| 15 | `ChenhLech` | `chenh_lech` | `numeric(18,4)` ⚠ | N | `0` | **[Số liệu đánh giá lại]** Chênh lệch |

**Trường base — `BaseChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4 |
| `phien_ban` | `integer` | N | `1` | Khóa lạc quan `@Version`. `AggregateRootEntity` |
| `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4 |
| `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4 |
| `giao_dich_chung_tu_id` | `uuid` | Y | — | Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity` |
| `so_chung_tu` | `varchar(50)` | N | — | Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20 |
| `ngay_chung_tu` | `date` | N | — | Ngày lập chứng từ. `BaseChungTuEntity` |
| `ngay_hach_toan` | `date` | N | — | Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37 |
| `status` | `text` | N | `NHAP` | Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12 |
| `nguoi_duyet_id` | `uuid` | Y | — | Người duyệt. `BaseChungTuEntity` |
| `ngay_duyet` | `timestamptz` | Y | — | Thời điểm duyệt. `BaseChungTuEntity` |
| `nguoi_ghi_so` | `uuid` | Y | — | Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `thoi_gian_ghi_so` | `timestamptz` | Y | — | Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo, gán một lần. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo, gán một lần. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

---

## 4. `fx_phieu_danh_gia_lai_ngoai_te_hach_toan`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDanhGiaLaiNgoaiTe_HachToan` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết hạch toán chênh lệch tỷ giá (Detail) |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `fx_phieu_danh_gia_lai_ngoai_te` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuDanhGiaLaiNgoaiTeId` | `phieu_danh_gia_lai_ngoai_te_id` | `uuid` | N | — | ID phiếu đánh giá lại (reference ENT_PhieuDanhGiaLaiNgoaiTe) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Bút toán]** Diễn giải dòng |
| 3 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Bút toán]** ID tài khoản Nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 4 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Bút toán]** ID tài khoản Có (reference ENT_HeThongTaiKhoan) `FK` |
| 5 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | **[Bút toán]** Số tiền |
| 6 | `TaiKhoanNganHangId` | `tai_khoan_ngan_hang_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID tài khoản ngân hàng (reference ENT_TaiKhoanNganHang) `FK` |
| 7 | `DoiTuongNoId` | `doi_tuong_no_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID đối tượng nợ (reference ENT_DoiTuong) `FK` |
| 8 | `LoaiDoiTuongNo` | `loai_doi_tuong_no` | `text` CHECK | Y | — | **[Đối tượng theo dõi]** Loại đối tượng nợ (KhachHang \| NhaCungCap \| NhanVien) |
| 9 | `TenDoiTuongNo` | `ten_doi_tuong_no` | `text` | Y | — | **[Đối tượng theo dõi]** Tên đối tượng nợ |
| 10 | `DoiTuongCoId` | `doi_tuong_co_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID đối tượng có (reference ENT_DoiTuong) `FK` |
| 11 | `LoaiDoiTuongCo` | `loai_doi_tuong_co` | `text` CHECK | Y | — | **[Đối tượng theo dõi]** Loại đối tượng có (KhachHang \| NhaCungCap \| NhanVien) |
| 12 | `TenDoiTuongCo` | `ten_doi_tuong_co` | `text` | Y | — | **[Đối tượng theo dõi]** Tên đối tượng có |

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

## 5. `fx_ket_qua_tinh_ty_gia_xuat_quy`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KetQuaTinhTyGiaXuatQuy` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Kết quả tính tỷ giá xuất quỹ theo kỳ |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Nam` | `nam` | `integer` | N | `0` | **[Kỳ tính]** Năm của kỳ tính |
| 2 | `Thang` | `thang` | `integer` | N | `0` | **[Kỳ tính]** Tháng của kỳ tính |
| 3 | `HinhThucTien` | `hinh_thuc_tien` | `text` CHECK | N | — | **[Kỳ tính]** Hình thức tiền (TienMat \| TienGui) |
| 4 | `PhuongPhapTinh` | `phuong_phap_tinh` | `text` CHECK | N | — | **[Kỳ tính]** Phương pháp tính (BinhQuanTucThoi \| BinhQuanCuoiKy) |
| 5 | `SapXepThuTruocChiSauCungNgay` | `sap_xep_thu_truoc_chi_sau_cung_ngay` | `boolean` | N | `false` | **[Kỳ tính]** Trong cùng ngày sắp xếp thu trước chi sau |
| 6 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | **[Khóa tính tỷ giá]** ID tài khoản tiền ngoại tệ (reference ENT_HeThongTaiKhoan) `FK` |
| 7 | `TaiKhoanNganHangId` | `tai_khoan_ngan_hang_id` | `uuid` | Y | — | **[Khóa tính tỷ giá]** ID tài khoản ngân hàng (reference ENT_TaiKhoanNganHang) `FK` |
| 8 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Khóa tính tỷ giá]** ID loại ngoại tệ (reference ENT_LoaiTien) `FK` |
| 9 | `TyGiaXuatQuy` | `ty_gia_xuat_quy` | `exchange_rate` | N | `1` | **[Kết quả]** Tỷ giá xuất quỹ của kỳ |
| 10 | `NguyenTeDauKy` | `nguyen_te_dau_ky` | `numeric(18,4)` ⚠ | N | `0` | **[Kết quả]** Số dư nguyên tệ đầu kỳ |
| 11 | `QuyDoiDauKy` | `quy_doi_dau_ky` | `numeric(18,4)` ⚠ | N | `0` | **[Kết quả]** Số dư quy đổi đầu kỳ |
| 12 | `NguyenTeNhapTrongKy` | `nguyen_te_nhap_trong_ky` | `numeric(18,4)` ⚠ | N | `0` | **[Kết quả]** Tổng nguyên tệ nhập trong kỳ |
| 13 | `QuyDoiNhapTrongKy` | `quy_doi_nhap_trong_ky` | `numeric(18,4)` ⚠ | N | `0` | **[Kết quả]** Tổng quy đổi nhập trong kỳ |

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

