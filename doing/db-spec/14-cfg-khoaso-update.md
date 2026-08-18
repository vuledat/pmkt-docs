# `cfg_` — Khóa sổ kế toán

> Sinh tự động từ [`ldm-KhoaSo-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-KhoaSo-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**3 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> Chuyển hóa bảo thủ từ ldm-KhoaSo.puml: Không bổ sung entity hoặc thay đổi logic nghiệp vụ khi chưa có yêu cầu. Dấu * chỉ dùng cho khóa chính; dấu ! thể hiện trường bắt buộc. Tham chiếu danh mục lưu ID và Name snapshot; không lưu Code. Field hệ thống dùng chung không khai báo trong từng entity.

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ThietLapKhoaSo` | `cfg_thiet_lap_khoa_so` | `cfg_thiet_lap_khoa_so` | A — có code | Cấu hình / thiết lập — 1. Thiết lập khóa sổ |
| 2 | `ChiTietThietLapKhoaSoChungTu` | `cfg_thiet_lap_khoa_so_chung_tu` | `cfg_thiet_lap_khoa_so_chung_tu` | A — có code | Dòng chi tiết của `cfg_thiet_lap_khoa_so` — 2. Chi tiết phạm vi loại chứng từ |
| 3 | `ChiTietThietLapKhoaSoNguoiDung` | `cfg_thiet_lap_khoa_so_nguoi_dung` | `cfg_thiet_lap_khoa_so_nguoi_dung` | A — có code | Dòng chi tiết của `cfg_thiet_lap_khoa_so` — 3. Chi tiết phạm vi người dùng |

---

## 1. `cfg_thiet_lap_khoa_so`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThietLapKhoaSo` |
| Base class | `TenantedEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `cfg_thiet_lap_khoa_so` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 1. Thiết lập khóa sổ |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng con | `cfg_thiet_lap_khoa_so_chung_tu` · `cfg_thiet_lap_khoa_so_nguoi_dung` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiDoiTuong` | `loai_doi_tuong` | `text` CHECK | N | — | Phạm vi khóa sổ (ToanHeThong \| ChonChungTu) |
| 2 | `LoaiKhoaSo` | `loai_khoa_so` | `text` CHECK | N | — | Loại khóa sổ (ThuCong \| TuDong) |
| 3 | `NgayKhoaSo` | `ngay_khoa_so` | `timestamptz` | N | — | Mốc khóa sổ hoặc ngày bắt đầu hiệu lực |
| 4 | `IsTuDong` | `is_tu_dong` | `boolean` | N | `false` | Trạng thái bật/tắt khóa sổ tự động |
| 5 | `KyKhoaSo` | `ky_khoa_so` | `text` CHECK | Y | — | Kỳ khóa sổ tự động (HangNgay \| HangTuan \| HangThang; NULL nếu thủ công) |
| 6 | `GiaTriKy` | `gia_tri_ky` | `money_foreign` ≈ | Y | `0` | Thứ 2 đến Chủ nhật hoặc ngày 1-31; 32 là ngày cuối tháng |
| 7 | `DoTreThucThi` | `do_tre_thuc_thi` | `numeric(18,4)` ⚠ | Y | `0` | Số ngày trễ so với kỳ khóa sổ, từ 0 đến 7 |
| 8 | `GioThucThi` | `gio_thuc_thi` | `time` ⚠ | Y | — | Thời điểm job chạy trong ngày, ví dụ 18:00 |

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

**Đối chiếu `cfg_thiet_lap_khoa_so` (28 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 14 | `nam_tai_chinh`, `ky`, `trang_thai`, `ngay_khoa`, `chi_nhanh_id`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `deleted_at`, `loai_chon_nguoi_dung`, `nhom_ban_ghi` |

---

## 2. `cfg_thiet_lap_khoa_so_chung_tu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietThietLapKhoaSoChungTu` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `cfg_thiet_lap_khoa_so_chung_tu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 2. Chi tiết phạm vi loại chứng từ |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cfg_thiet_lap_khoa_so` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cfg_thiet_lap_khoa_so` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ThietLapKhoaSoId` | `thiet_lap_khoa_so_id` | `uuid` | N | — | ID thiết lập khóa sổ `FK` |
| 2 | `TenLoaiChungTu` | `ten_loai_chung_tu` | `text` | N | — | Snapshot tên loại chứng từ |

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

**Đối chiếu `cfg_thiet_lap_khoa_so_chung_tu` (11 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `thiet_lap_khoa_so_id`, `ten_loai_chung_tu` |
| DB có — LDM **không khai** | 9 | `thiet_lap_id`, `ma_loai_chung_tu`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `deleted_at` |

---

## 3. `cfg_thiet_lap_khoa_so_nguoi_dung`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietThietLapKhoaSoNguoiDung` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `cfg_thiet_lap_khoa_so_nguoi_dung` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 3. Chi tiết phạm vi người dùng |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cfg_thiet_lap_khoa_so` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cfg_thiet_lap_khoa_so` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ThietLapKhoaSoId` | `thiet_lap_khoa_so_id` | `uuid` | N | — | ID thiết lập khóa sổ `FK` |
| 2 | `LoaiChonNguoiDung` | `loai_chon_nguoi_dung` | `text` CHECK | N | — | Phạm vi người dùng (TatCaNguoiDung \| ChonNguoiDungCuThe) |
| 3 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | Y | — | ID người dùng `FK` |
| 4 | `TenNguoiDung` | `ten_nguoi_dung` | `text` | Y | — | Snapshot tên người dùng |

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

**Đối chiếu `cfg_thiet_lap_khoa_so_nguoi_dung` (12 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `thiet_lap_khoa_so_id`, `nguoi_dung_id`, `ten_nguoi_dung` |
| DB có — LDM **không khai** | 9 | `thiet_lap_id`, `user_id`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `deleted_at` |

