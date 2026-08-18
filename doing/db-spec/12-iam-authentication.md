# `iam_` — Xác thực · Người dùng

> Sinh tự động từ [`ldm-Authentication.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-Authentication.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**10 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> tại entity khi epic cần; thư viện đặt tên chuẩn (Rule 4) sẽ ban hành sau.

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `GoiDichVu` | `iam_goi_dich_vu` | — | C — tạo mới | Bảng nghiệp vụ — GOI DICH VU Các trường dưới đây chỉ mang tính chất tham khảo, định nghĩa chi tiết sẽ được triển khai trong epic Quản lý gói… |
| 2 | `Subscription` | `iam_subscription` | — | C — tạo mới | Bảng nghiệp vụ — SUBSCRIPTION Các trường dưới đây chỉ mang tính chất tham khảo |
| 3 | `TenantModule` | `iam_tenant_module` | — | C — tạo mới | Bảng nghiệp vụ — TENANT MODULE Các trường dưới đây chỉ mang tính chất tham khảo |
| 4 | `NhatKyWebhookHub` | `iam_nhat_ky_webhook_hub` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 5 | `NguoiDung` | `iam_tai_khoan` | `iam_tai_khoan` | A — có code | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 6 | `TokenXacThuc` | `iam_token_xac_thuc` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 7 | `OTP` | `iam_otp` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 8 | `PhienDangNhap` | `iam_phien_dang_nhap` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 9 | `NhatKyHoatDong` | `iam_nhat_ky_hoat_dong` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 10 | `ThamSoHeThong` | `iam_tham_so_he_thong` | — | C — tạo mới | Bảng nghiệp vụ — THAM SO HE THONG (System Parameters) Lưu các tham số cấu hình động cho rate limit, security, email, session,... Các tham số… |

---

## 1. `iam_goi_dich_vu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `GoiDichVu` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | GOI DICH VU · Các trường dưới đây chỉ mang tính chất tham khảo, định nghĩa chi tiết sẽ được triển khai trong epic Quản lý gói dịch vụ. Các trường này có thể được điều chỉnh theo yêu cầu thực tế. |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TenGoi` | `ten_goi` | `text` | Y | — | *(LDM chưa mô tả)* |
| 2 | `MoTa` | `mo_ta` | `text` | Y | — | *(LDM chưa mô tả)* |
| 3 | `TrangThai` | `trang_thai` | `text` | Y | — | *(LDM chưa mô tả)* |
| 4 | `CreatedAt` | `created_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 5 | `UpdatedAt` | `updated_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |

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

## 2. `iam_subscription`

| Mục | Nội dung |
|---|---|
| Entity LDM | `Subscription` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | SUBSCRIPTION · Các trường dưới đây chỉ mang tính chất tham khảo |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NgayBatDau` | `ngay_bat_dau` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 2 | `NgayKetThuc` | `ngay_ket_thuc` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 3 | `CreatedAt` | `created_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 4 | `UpdatedAt` | `updated_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |

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

## 3. `iam_tenant_module`

| Mục | Nội dung |
|---|---|
| Entity LDM | `TenantModule` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | TENANT MODULE · Các trường dưới đây chỉ mang tính chất tham khảo |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `IsEnabled` | `is_enabled` | `boolean` | Y | `false` | *(LDM chưa mô tả)* |
| 2 | `ActivatedAt` | `activated_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 3 | `ExpiredAt` | `expired_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 4 | `CreatedAt` | `created_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 5 | `UpdatedAt` | `updated_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |

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

## 4. `iam_nhat_ky_webhook_hub`

| Mục | Nội dung |
|---|---|
| Entity LDM | `NhatKyWebhookHub` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `MaHopDongHub` | `ma_hop_dong_hub` | `text` | Y | — | Mã hợp đồng Hub `unique` |
| 2 | `LoaiSuKien` | `loai_su_kien` | `text` | Y | — | Loại sự kiện |
| 3 | `DuLieuJson` | `du_lieu_json` | `text` | Y | — | Dữ liệu JSON |
| 4 | `ChuKyWebhook` | `chu_ky_webhook` | `text` | Y | — | Chữ ký webhook |
| 5 | `TrangThaiXuLy` | `trang_thai_xu_ly` | `text` CHECK | Y | — | Trạng thái xử lý (DaNhan \| ThatBai \| ThanhCong) |
| 6 | `MaLoi` | `ma_loi` | `text` | Y | — | Mã lỗi |
| 7 | `NoiDungLoi` | `noi_dung_loi` | `text` | Y | — | Nội dung lỗi |
| 8 | `SoLanThuLai` | `so_lan_thu_lai` | `integer` | Y | `0` | Số lần thử lại |
| 9 | `ThoiDiemNhan` | `thoi_diem_nhan` | `timestamptz` | Y | — | Thời điểm nhận |
| 10 | `ThoiDiemXuLy` | `thoi_diem_xu_ly` | `timestamptz` | Y | — | Thời điểm xử lý |
| 11 | `AlertJson` | `alert_json` | `text` | Y | — | Alert log (JSON) khi vượt ngưỡng hạ tầng |

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

## 5. `iam_tai_khoan`

| Mục | Nội dung |
|---|---|
| Entity LDM | `NguoiDung` |
| Base class | `TenantedEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `iam_tai_khoan` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `iam_token_xac_thuc` · `iam_otp` · `iam_phien_dang_nhap` · `iam_nhat_ky_hoat_dong` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Code` | `code` | `varchar(50)` | N | — | Mã người dùng, tự sinh dạng NV + 4 chữ số tuần tự (NV0001, NV0002...) `unique` |
| 2 | `TenTaiKhoan` | `ten_tai_khoan` | `text` | Y | — | Tên tài khoản (chuẩn từ epic NguoiDung 14552; đăng nhập chỉ qua Email/SoDienThoai) `unique` |
| 3 | `MatKhau` | `mat_khau` | `text` | Y | — | Mật khẩu (PII, băm một chiều bcrypt/Argon2; NULL = chưa đặt MK — BR-DKWEB-07) |
| 4 | `Salt` | `salt` | `text` | Y | — | Salt (PII, mã hóa) |
| 5 | `Email` | `email` | `text` | N | — | Email (PII, mã hóa at-rest) `unique` |
| 6 | `SoDienThoai` | `so_dien_thoai` | `text` | Y | — | Số điện thoại (PII, mã hóa at-rest) `unique` |
| 7 | `HoTen` | `ho_ten` | `text` | N | — | Họ tên (PII) |
| 8 | `NgaySinh` | `ngay_sinh` | `date` | Y | — | Ngày sinh |
| 9 | `GioiTinh` | `gioi_tinh` | `text` | Y | — | Giới tính (Nam/Nu/Khac) |
| 10 | `DiaChiChiTiet` | `dia_chi_chi_tiet` | `text` | Y | — | Địa chỉ chi tiết |
| 11 | `TinhThanhPhoId` | `tinh_thanh_pho_id` | `uuid` | Y | — | Mã Tỉnh/Thành phố (reference ENT_TinhThanhPho) `FK` |
| 12 | `PhuongXaId` | `phuong_xa_id` | `uuid` | Y | — | Mã Phường/Xã (reference ENT_PhuongXa) `FK` |
| 13 | `AvatarUrl` | `avatar_url` | `text` | Y | — | Ảnh đại diện |
| 14 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | Trạng thái (ChoXacThucEmail \| DangHoatDong \| TamKhoa \| DaXoa) |
| 15 | `BatMFA` | `bat_mfa` | `boolean` | Y | `false` | Cờ bật xác thực 2 yếu tố (MFA) |
| 16 | `LanDangNhapCuoi` | `lan_dang_nhap_cuoi` | `timestamptz` | Y | — | Lần đăng nhập cuối |
| 17 | `SoLanDangNhapSai` | `so_lan_dang_nhap_sai` | `integer` | Y | `0` | Bộ đếm đăng nhập sai |
| 18 | `ThoiDiemKhoaTaiKhoan` | `thoi_diem_khoa_tai_khoan` | `timestamptz` | Y | — | Thời điểm khóa tài khoản |
| 19 | `SoLanNhapSaiOTP` | `so_lan_nhap_sai_otp` | `integer` | Y | `0` | Bộ đếm OTP sai |
| 20 | `ThoiDiemKhoaOTP` | `thoi_diem_khoa_otp` | `timestamptz` | Y | — | Thời điểm khóa OTP |
| 21 | `MatKhauDoiLanCuoi` | `mat_khau_doi_lan_cuoi` | `timestamptz` | Y | — | Mật khẩu đổi lần cuối |
| 22 | `ThoiDiemXacThucEmail` | `thoi_diem_xac_thuc_email` | `timestamptz` | Y | — | Thời điểm xác thực email |

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

**Đối chiếu `iam_tai_khoan` (11 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 19 | `code`, `ten_tai_khoan`, `mat_khau`, `salt`, `so_dien_thoai`, `ho_ten`, `ngay_sinh`, `gioi_tinh`, `dia_chi_chi_tiet`, `tinh_thanh_pho_id`, `phuong_xa_id`, `avatar_url`, `bat_mfa`, `lan_dang_nhap_cuoi`, `so_lan_dang_nhap_sai`, `thoi_diem_khoa_tai_khoan`, `so_lan_nhap_sai_otp`, `thoi_diem_khoa_otp`, `thoi_diem_xac_thuc_email` |
| DB có — LDM **không khai** | 6 | `ma`, `so_cccd`, `mfa_enabled`, `phien_ban`, `token_kich_hoat`, `han_kich_hoat` |

---

## 6. `iam_token_xac_thuc`

| Mục | Nội dung |
|---|---|
| Entity LDM | `TokenXacThuc` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `iam_tai_khoan` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | Y | — | Khóa ngoại (reference ENT_NguoiDung) `FK` |
| 2 | `MaBamTokenXacThuc` | `ma_bam_token_xac_thuc` | `text` | Y | — | Hash của token xác thực `unique` |
| 3 | `LoaiToken` | `loai_token` | `text` | Y | — | Loại token (XacThucEmail) |
| 4 | `HetHanLuc` | `het_han_luc` | `timestamptz` | Y | — | Thời điểm hết hạn |
| 5 | `ThoiDiemSuDung` | `thoi_diem_su_dung` | `timestamptz` | Y | — | Thời điểm sử dụng |

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

## 7. `iam_otp`

| Mục | Nội dung |
|---|---|
| Entity LDM | `OTP` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `iam_tai_khoan` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | Y | — | Khóa ngoại (reference ENT_NguoiDung) `FK` |
| 2 | `Loai` | `loai` | `text` CHECK | Y | — | Loại OTP (XacThucMFA \| DoiMatKhau) |
| 3 | `MaOTP` | `ma_otp` | `text` | Y | — | Mã OTP (hash bcrypt/Argon2) |
| 4 | `HetHanLuc` | `het_han_luc` | `timestamptz` | Y | — | Thời điểm hết hạn |
| 5 | `ThoiDiemSuDung` | `thoi_diem_su_dung` | `timestamptz` | Y | — | Thời điểm sử dụng |
| 6 | `IP` | `ip` | `text` | Y | — | IP client |

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

## 8. `iam_phien_dang_nhap`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhienDangNhap` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `iam_tai_khoan` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | Y | — | Khóa ngoại (reference ENT_NguoiDung) `FK` |
| 2 | `MaBamRefreshToken` | `ma_bam_refresh_token` | `text` | Y | — | Refresh Token hash (bcrypt/Argon2) `unique` |
| 3 | `ThietBi` | `thiet_bi` | `text` | Y | — | Thiết bị / User-Agent |
| 4 | `HetHanLuc` | `het_han_luc` | `timestamptz` | Y | — | Thời điểm hết hạn |
| 5 | `TrangThai` | `trang_thai` | `text` CHECK | Y | — | Trạng thái (DangHoatDong \| DaThuHoi; tối đa 1 session DangHoatDong/account — BR-CORE-SES02) |
| 6 | `ThoiDiemThuHoi` | `thoi_diem_thu_hoi` | `timestamptz` | Y | — | Thời điểm thu hồi |

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

## 9. `iam_nhat_ky_hoat_dong`

| Mục | Nội dung |
|---|---|
| Entity LDM | `NhatKyHoatDong` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `iam_tai_khoan` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | Y | — | Khóa ngoại (reference ENT_NguoiDung) `FK` |
| 2 | `ThoiDiem` | `thoi_diem` | `timestamptz` | Y | — | Thời điểm |
| 3 | `IP` | `ip` | `text` | Y | — | IP client |
| 4 | `LoaiSuKien` | `loai_su_kien` | `text` | Y | — | Loại sự kiện |
| 5 | `ThongTinTrinhDuyet` | `thong_tin_trinh_duyet` | `text` | Y | — | Thông tin trình duyệt (User-Agent) |
| 6 | `GiaTriTruoc` | `gia_tri_truoc` | `text` | Y | — | Giá trị trước thay đổi (PII, mã hóa at-rest) |
| 7 | `GiaTriSau` | `gia_tri_sau` | `text` | Y | — | Giá trị sau thay đổi (PII, mã hóa at-rest) |

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

## 10. `iam_tham_so_he_thong`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThamSoHeThong` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | THAM SO HE THONG (System Parameters) · Lưu các tham số cấu hình động cho rate limit, security, email, session,... · Các tham số được tham chiếu bởi Business Rules và Messages (placeholders) · Chờ chuẩn Rule 4 ban hành định nghĩa chính thức. |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `CreatedAt` | `created_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |
| 2 | `UpdatedAt` | `updated_at` | `timestamptz` | Y | — | *(LDM chưa mô tả)* |

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

