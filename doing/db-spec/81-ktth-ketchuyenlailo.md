# `ktth_` — Kết chuyển lãi lỗ

> Sinh tự động từ [`ldm-KetChuyenLaiLo.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-KetChuyenLaiLo.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**3 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> Phạm vi: PMKT-E-14031_KhaiBaoButToanKetChuyen + PMKT-E-14030_KetChuyenLaiLo Hậu tố ! = trường bắt buộc (NOT NULL). Mọi trường kiểu numeric đều NOT NULL (numeric!). Bộ trường hệ thống (DaXoa, NguoiTao, ThoiGianTao, NguoiCapNhat, ThoiGianCapNhat, NguoiGhiSo, ThoiGianGhiSo, NguoiXoa, ThoiGianXoa) áp dụng cho mọi entity theo BR46 - Common/business_rules.md, không khai báo lại ở đây.

**Epic nguồn:** PMKT-E-14030 · PMKT-E-14031

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ButToanKetChuyen` | `ktth_but_toan_ket_chuyen` | — | C — tạo mới | Bảng nghiệp vụ — Khai báo bút toán kết chuyển (danh mục cấu hình - PMKT-E-14031) |
| 2 | `PhieuKetChuyenLaiLo` | `ktth_phieu_ket_chuyen_lai_lo` | — | C — tạo mới | Đầu chứng từ — Phiếu kết chuyển lãi lỗ - phần Master (PMKT-E-14030) |
| 3 | `ChiTietPhieuKetChuyenLaiLo` | `ktth_phieu_ket_chuyen_lai_lo_chi_tiet` | — | C — tạo mới | Bảng nghiệp vụ — Chi tiết phiếu kết chuyển lãi lỗ - phần Detail (PMKT-E-14030) Mỗi dòng chi tiết khi ghi sổ sinh 2 dòng Sổ cái (1 Nợ, 1 Có)… |

---

## 1. `ktth_but_toan_ket_chuyen`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ButToanKetChuyen` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Khai báo bút toán kết chuyển (danh mục cấu hình - PMKT-E-14031) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Epic nghiệp vụ | PMKT-E-14030 · PMKT-E-14031 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ThuTuKetChuyen` | `thu_tu_ket_chuyen` | `integer` | N | `0` | **[Thông tin khai báo]** Thứ tự thực hiện kết chuyển, số nguyên > 0, tối đa 4 chữ số, duy nhất trong phạm vi Tenant. Khi thêm mới hệ thống tự sinh bằng số nguyên dương nhỏ nhất chưa dùng (BR3 - SCR_KhaiBaoButToanKetChuyen_ThemMoi) |
| 2 | `TenButToan` | `ten_but_toan` | `text` | N | — | **[Thông tin khai báo]** Tên bút toán kết chuyển, tối đa 250 ký tự |
| 3 | `KieuKetChuyen` | `kieu_ket_chuyen` | `text` CHECK | N | — | **[Thông tin khai báo]** Kiểu kết chuyển (KetChuyenNo \| KetChuyenCo \| KetChuyenHaiBen) |
| 4 | `KetChuyenTuId` | `ket_chuyen_tu_id` | `uuid` | N | — | **[KieuKetChuyen KHÔNG thuộc khóa duy nhất (BR4 - SCR_KhaiBaoButToanKetChuyen_ThemMoi)]** ID tài khoản nguồn kết chuyển; cho phép chọn cả tài khoản cha và tài khoản con, khi là tài khoản cha thì bút toán được nổ chi tiết tới tài khoản con cấp nhỏ nhất (reference ENT_HeThongTaiKhoan) `FK` |
| 5 | `KetChuyenDenId` | `ket_chuyen_den_id` | `uuid` | N | — | **[KieuKetChuyen KHÔNG thuộc khóa duy nhất (BR4 - SCR_KhaiBaoButToanKetChuyen_ThemMoi)]** ID tài khoản đích kết chuyển; bắt buộc là tài khoản con, không được chọn tài khoản cha vì không hạch toán vào tài khoản cha (reference ENT_HeThongTaiKhoan) `FK` |

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

## 2. `ktth_phieu_ket_chuyen_lai_lo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuKetChuyenLaiLo` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu kết chuyển lãi lỗ - phần Master (PMKT-E-14030) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ktth_phieu_ket_chuyen_lai_lo_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-14030 · PMKT-E-14031 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | N | — | **[Thông tin chứng từ]** Diễn giải phiếu, tối đa 250 ký tự |
| 2 | `KetChuyenDenNgay` | `ket_chuyen_den_ngay` | `date` | N | — | **[Thông tin kết chuyển]** Mốc thời gian tính số dư để kết chuyển |
| 3 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Thông tin kết chuyển]** Trạng thái phiếu (ChuaGhiSo \| DaGhiSo). Chỉ phiếu ChuaGhiSo mới được sửa/xóa; khi ghi sổ sinh dữ liệu phát sinh vào ENT_SoCai, khi bỏ ghi xóa dữ liệu phát sinh tương ứng |

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

## 3. `ktth_phieu_ket_chuyen_lai_lo_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuKetChuyenLaiLo` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết phiếu kết chuyển lãi lỗ - phần Detail (PMKT-E-14030) · Mỗi dòng chi tiết khi ghi sổ sinh 2 dòng Sổ cái (1 Nợ, 1 Có) theo BR7 · SCR_KetChuyenLaiLo_ThemMoi và Common/TaiLieuMappingSoCai.md. |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `ktth_phieu_ket_chuyen_lai_lo` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-14030 · PMKT-E-14031 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKetChuyenLaiLoId` | `phieu_ket_chuyen_lai_lo_id` | `uuid` | N | — | ID phiếu kết chuyển lãi lỗ (reference ENT_PhieuKetChuyenLaiLo) `FK` |
| 2 | `ButToanKetChuyenId` | `but_toan_ket_chuyen_id` | `uuid` | Y | — | ID bút toán kết chuyển cấu hình đã sinh ra dòng này (reference ENT_ButToanKetChuyen; NULL với dòng người dùng tự thêm thủ công) `FK` |
| 3 | `DienGiaiChiTiet` | `dien_giai_chi_tiet` | `text` | N | — | **[Thông tin định khoản]** Diễn giải dòng chi tiết, tối đa 250 ký tự |
| 4 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Thông tin định khoản]** ID tài khoản hạch toán vế Nợ, xác định theo KieuKetChuyen (reference ENT_HeThongTaiKhoan) `FK` |
| 5 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Thông tin định khoản]** ID tài khoản hạch toán vế Có, xác định theo KieuKetChuyen (reference ENT_HeThongTaiKhoan) `FK` |
| 6 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | **[Thông tin định khoản]** Số tiền kết chuyển, >= 0; tính theo số dư tài khoản nguồn tại KetChuyenDenNgay, dòng có số tiền = 0 không hiển thị và không lưu (BR3, BR4); người dùng được sửa tay và giá trị sửa tay được ưu tiên khi lưu (BR6) |

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

