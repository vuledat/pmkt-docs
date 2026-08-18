# `iam_` — Hồ sơ người dùng trong tenant

> Sinh tự động từ [`ldm-ProfileManagement.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-ProfileManagement.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**2 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `NguoiDung_Tenant` | `iam_tai_khoan_tenant` | `iam_tai_khoan_tenant` | A — có code | Liên kết N–N — ⚠ *LDM chưa mô tả bảng này* |
| 2 | `YeuCauXoaTaiKhoan` | `iam_yeu_cau_xoa_tai_khoan` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `iam_tai_khoan_tenant`

| Mục | Nội dung |
|---|---|
| Entity LDM | `NguoiDung_Tenant` |
| Base class | `TenantedEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `iam_tai_khoan_tenant` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | Y | — | Tham chiếu người dùng (reference ENT_NguoiDung) `FK` |
| 2 | `TenHienThi` | `ten_hien_thi` | `text` | N | — | Họ và tên (trong workspace) |
| 3 | `ChucDanh` | `chuc_danh` | `text` | Y | — | Chức danh (trong workspace) |
| 4 | `DonViId` | `don_vi_id` | `uuid` | Y | — | Đơn vị công tác trong tenant (reference ENT_DonVi) `FK` |
| 5 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | Nhân viên liên kết trong tenant (reference ENT_NhanVien - danh mục Nhân viên; duy nhất trong tenant: 1 nhân viên chỉ gắn 1 người dùng, NULL nếu chưa liên kết) `FK` |
| 6 | `TrangThai` | `trang_thai` | `text` CHECK | Y | — | Trạng thái thành viên (ChoKichHoat \| DangHoatDong \| DaKhoa) |
| 7 | `LaChuSoHuu` | `la_chu_so_huu` | `boolean` | Y | `false` | Quyền chủ sở hữu |
| 8 | `LaTenantMacDinh` | `la_tenant_mac_dinh` | `boolean` | Y | `false` | Tenant mặc định |

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

**Đối chiếu `iam_tai_khoan_tenant` (8 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `nguoi_dung_id`, `ten_hien_thi`, `chuc_danh`, `nhan_vien_id`, `la_chu_so_huu`, `la_tenant_mac_dinh` |
| DB có — LDM **không khai** | 2 | `tai_khoan_id`, `phien_ban` |

---

## 2. `iam_yeu_cau_xoa_tai_khoan`

| Mục | Nội dung |
|---|---|
| Entity LDM | `YeuCauXoaTaiKhoan` |
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
| 1 | `NguoiDungId` | `nguoi_dung_id` | `uuid` | Y | — | Tham chiếu người dùng (reference ENT_NguoiDung) `FK` |
| 2 | `ThoiDiemXacNhan` | `thoi_diem_xac_nhan` | `timestamptz` | Y | — | Thời điểm xác nhận |
| 3 | `ThoiDiemKetThucThoiGianGiaHan` | `thoi_diem_ket_thuc_thoi_gian_gia_han` | `timestamptz` | Y | — | Thời điểm kết thúc thời gian gia hạn |
| 4 | `DaGuiEmail` | `da_gui_email` | `boolean` | Y | `false` | Đã gửi email |
| 5 | `SoLanThuGuiEmail` | `so_lan_thu_gui_email` | `integer` | Y | `0` | Số lần thử gửi email |
| 6 | `LanThuGuiEmailCuoi` | `lan_thu_gui_email_cuoi` | `timestamptz` | Y | — | Lần thử gửi email cuối |
| 7 | `LyDoGuiEmailThatBai` | `ly_do_gui_email_that_bai` | `text` | Y | — | Lý do gửi email thất bại |
| 8 | `TrangThai` | `trang_thai` | `text` CHECK | Y | — | Trạng thái request (ChoXuLy \| GuiEmailThatBai \| DaXacNhan \| DaHuy \| HoanTat; DangXuLy là marker tạm thời của Soft Delete Job) |
| 9 | `NoiDungLoi` | `noi_dung_loi` | `text` | Y | — | Chi tiết lỗi cuối cùng của job xóa mềm |
| 10 | `HoanTatLuc` | `hoan_tat_luc` | `timestamptz` | Y | — | Thời điểm hoàn tất xóa mềm |

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

