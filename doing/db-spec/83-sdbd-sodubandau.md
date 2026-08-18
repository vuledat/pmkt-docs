# `sdbd_` — Số dư ban đầu

> Sinh tự động từ [`ldm-SoDuBanDau.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-SoDuBanDau.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**9 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `SoDuBanDauTaiKhoan` | `sdbd_so_du_ban_dau_tai_khoan` | `sdbd_so_du_ban_dau_tai_khoan` | B — có schema, chưa code | Bảng nghiệp vụ — Số dư ban đầu Tài khoản (Master) |
| 2 | `ChiTietSDBD_TaiKhoan` | `sdbd_so_du_ban_dau_tai_khoan_chi_tiet` | `sdbd_chi_tiet_sdbd_tai_khoan` | B — có schema, chưa code | Dòng chi tiết của `sdbd_so_du_ban_dau_tai_khoan` — Chi tiết số dư ban đầu Tài khoản theo đối tượng thống kê (Detail) |
| 3 | `SoDuBanDauTKNganHang` | `sdbd_so_du_ban_dau_tai_khoan_ngan_hang` | `sdbd_so_du_ban_dau_tk_ngan_hang` | B — có schema, chưa code | Bảng nghiệp vụ — Số dư ban đầu Tài khoản ngân hàng |
| 4 | `SoDuBanDauKhachHang` | `sdbd_so_du_ban_dau_khach_hang` | `sdbd_so_du_ban_dau_khach_hang` | B — có schema, chưa code | Bảng nghiệp vụ — Số dư ban đầu Khách hàng (Master) |
| 5 | `ChiTietSDBD_KH_HoaDon` | `sdbd_so_du_ban_dau_khach_hang_chi_tiet` | `sdbd_chi_tiet_sdbd_kh_hoa_don` | B — có schema, chưa code | Dòng chi tiết của `sdbd_so_du_ban_dau_khach_hang` — Chi tiết số dư ban đầu Khách hàng - Hóa đơn (Detail) |
| 6 | `SoDuBanDauNCC` | `sdbd_so_du_ban_dau_nha_cung_cap` | `sdbd_so_du_ban_dau_ncc` | B — có schema, chưa code | Bảng nghiệp vụ — Số dư ban đầu Nhà cung cấp (Master) |
| 7 | `ChiTietSDBD_NCC_HoaDon` | `sdbd_so_du_ban_dau_nha_cung_cap_chi_tiet` | `sdbd_chi_tiet_sdbd_ncc_hoa_don` | B — có schema, chưa code | Dòng chi tiết của `sdbd_so_du_ban_dau_nha_cung_cap` — Chi tiết số dư ban đầu NCC - Hóa đơn (Detail) |
| 8 | `SoDuBanDauNhanVien` | `sdbd_so_du_ban_dau_nhan_vien` | `sdbd_so_du_ban_dau_nhan_vien` | B — có schema, chưa code | Bảng nghiệp vụ — Số dư ban đầu Nhân viên |
| 9 | `SoDuBanDauVatTu` | `sdbd_so_du_ban_dau_vat_tu` | `sdbd_so_du_ban_dau_vat_tu` | B — có schema, chưa code | Bảng nghiệp vụ — Số dư ban đầu Vật tư |

---

## 1. `sdbd_so_du_ban_dau_tai_khoan`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoDuBanDauTaiKhoan` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_so_du_ban_dau_tai_khoan` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Số dư ban đầu Tài khoản (Master) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `sdbd_so_du_ban_dau_tai_khoan_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản (reference ENT_HeThongTaiKhoan) `FK` |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | ID loại tiền (reference ENT_LoaiTien) `FK` |
| 3 | `DuNo` | `du_no` | `money_foreign` ≈ | Y | `0` | Dư Nợ |
| 4 | `DuNoQuyDoi` | `du_no_quy_doi` | `money_vnd` | Y | `0` | Dư Nợ quy đổi |
| 5 | `DuCo` | `du_co` | `money_foreign` ≈ | Y | `0` | Dư Có |
| 6 | `DuCoQuyDoi` | `du_co_quy_doi` | `money_vnd` | Y | `0` | Dư Có quy đổi |

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

**Đối chiếu `sdbd_so_du_ban_dau_tai_khoan` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 2. `sdbd_so_du_ban_dau_tai_khoan_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietSDBD_TaiKhoan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_chi_tiet_sdbd_tai_khoan` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết số dư ban đầu Tài khoản theo đối tượng thống kê (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sdbd_so_du_ban_dau_tai_khoan` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sdbd_so_du_ban_dau_tai_khoan` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `SoDuBanDauTaiKhoanId` | `so_du_ban_dau_tai_khoan_id` | `uuid` | N | — | ID số dư ban đầu tài khoản (reference ENT_SoDuBanDauTaiKhoan) `FK` |
| 2 | `DuNo` | `du_no` | `money_foreign` ≈ | Y | `0` | **[Số dư]** Dư Nợ |
| 3 | `DuNoQuyDoi` | `du_no_quy_doi` | `money_vnd` | Y | `0` | **[Số dư]** Dư Nợ quy đổi |
| 4 | `DuCo` | `du_co` | `money_foreign` ≈ | Y | `0` | **[Số dư]** Dư Có |
| 5 | `DuCoQuyDoi` | `du_co_quy_doi` | `money_vnd` | Y | `0` | **[Số dư]** Dư Có quy đổi |
| 6 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Đối tượng thống kê]** ID đối tượng tập hợp chi phí (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 7 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Đối tượng thống kê]** ID đơn vị (reference ENT_DonVi) `FK` |
| 8 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Đối tượng thống kê]** ID khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 9 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Đối tượng thống kê]** ID vụ việc (reference ENT_CongTrinh) `FK` |
| 10 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đối tượng thống kê]** Diễn giải chi tiết |

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

**Đối chiếu `sdbd_chi_tiet_sdbd_tai_khoan` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 3. `sdbd_so_du_ban_dau_tai_khoan_ngan_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoDuBanDauTKNganHang` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_so_du_ban_dau_tk_ngan_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Số dư ban đầu Tài khoản ngân hàng |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản (reference ENT_HeThongTaiKhoan) `FK` |
| 2 | `TKNganHangId` | `tk_ngan_hang_id` | `uuid` | N | — | ID tài khoản ngân hàng (reference ENT_TaiKhoanNganHang) `FK` |
| 3 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | ID loại tiền (reference ENT_LoaiTien) `FK` |
| 4 | `DuNo` | `du_no` | `money_foreign` ≈ | Y | `0` | Dư Nợ |
| 5 | `DuNoQuyDoi` | `du_no_quy_doi` | `money_vnd` | Y | `0` | Dư Nợ quy đổi |
| 6 | `DuCo` | `du_co` | `money_foreign` ≈ | Y | `0` | Dư Có |
| 7 | `DuCoQuyDoi` | `du_co_quy_doi` | `money_vnd` | Y | `0` | Dư Có quy đổi |

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

**Đối chiếu `sdbd_so_du_ban_dau_tk_ngan_hang` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 4. `sdbd_so_du_ban_dau_khach_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoDuBanDauKhachHang` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_so_du_ban_dau_khach_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Số dư ban đầu Khách hàng (Master) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `sdbd_so_du_ban_dau_khach_hang_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản công nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 2 | `KhachHangId` | `khach_hang_id` | `uuid` | N | — | ID khách hàng (reference ENT_DoiTuong, vai trò KhachHang) `FK` |
| 3 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | ID loại tiền (reference ENT_LoaiTien) `FK` |
| 4 | `DuNo` | `du_no` | `money_foreign` ≈ | Y | `0` | Dư Nợ |
| 5 | `DuNoQuyDoi` | `du_no_quy_doi` | `money_vnd` | Y | `0` | Dư Nợ quy đổi |
| 6 | `DuCo` | `du_co` | `money_foreign` ≈ | Y | `0` | Dư Có |
| 7 | `DuCoQuyDoi` | `du_co_quy_doi` | `money_vnd` | Y | `0` | Dư Có quy đổi |

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

**Đối chiếu `sdbd_so_du_ban_dau_khach_hang` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 5. `sdbd_so_du_ban_dau_khach_hang_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietSDBD_KH_HoaDon` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_chi_tiet_sdbd_kh_hoa_don` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết số dư ban đầu Khách hàng - Hóa đơn (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sdbd_so_du_ban_dau_khach_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sdbd_so_du_ban_dau_khach_hang` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `SoDuBanDauKhachHangId` | `so_du_ban_dau_khach_hang_id` | `uuid` | N | — | ID số dư ban đầu khách hàng (reference ENT_SoDuBanDauKhachHang) `FK` |
| 2 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Thông tin hóa đơn]** Tỷ giá |
| 3 | `GiaTriHoaDon` | `gia_tri_hoa_don` | `money_foreign` ≈ | Y | `0` | **[Thông tin hóa đơn]** Giá trị hóa đơn |
| 4 | `GiaTriHoaDonQuyDoi` | `gia_tri_hoa_don_quy_doi` | `money_vnd` | Y | `0` | **[Thông tin hóa đơn]** Giá trị hóa đơn quy đổi |
| 5 | `ConPhaiThu` | `con_phai_thu` | `money_foreign` ≈ | Y | `0` | **[Thông tin hóa đơn]** Còn phải thu |
| 6 | `ConPhaiThuQuyDoi` | `con_phai_thu_quy_doi` | `money_vnd` | Y | `0` | **[Thông tin hóa đơn]** Còn phải thu quy đổi |
| 7 | `DaThu` | `da_thu` | `numeric(18,4)` ⚠ | Y | `0` | **[Thông tin hóa đơn]** Đã thu |
| 8 | `DaThuQuyDoi` | `da_thu_quy_doi` | `money_vnd` | Y | `0` | **[Thông tin hóa đơn]** Đã thu quy đổi |
| 9 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | **[Thông tin hóa đơn]** ID nhân viên phụ trách (reference ENT_DoiTuong, vai trò NhanVien) `FK` |

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

**Đối chiếu `sdbd_chi_tiet_sdbd_kh_hoa_don` (21 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 3 | `ngay_chung_tu`, `so_chung_tu`, `phien_ban` |

---

## 6. `sdbd_so_du_ban_dau_nha_cung_cap`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoDuBanDauNCC` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_so_du_ban_dau_ncc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Số dư ban đầu Nhà cung cấp (Master) |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `sdbd_so_du_ban_dau_nha_cung_cap_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản công nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 2 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | N | — | ID nhà cung cấp (reference ENT_DoiTuong, vai trò NhaCungCap) `FK` |
| 3 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | ID loại tiền (reference ENT_LoaiTien) `FK` |
| 4 | `DuNo` | `du_no` | `money_foreign` ≈ | Y | `0` | Dư Nợ |
| 5 | `DuNoQuyDoi` | `du_no_quy_doi` | `money_vnd` | Y | `0` | Dư Nợ quy đổi |
| 6 | `DuCo` | `du_co` | `money_foreign` ≈ | Y | `0` | Dư Có |
| 7 | `DuCoQuyDoi` | `du_co_quy_doi` | `money_vnd` | Y | `0` | Dư Có quy đổi |

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

**Đối chiếu `sdbd_so_du_ban_dau_ncc` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 7. `sdbd_so_du_ban_dau_nha_cung_cap_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietSDBD_NCC_HoaDon` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_chi_tiet_sdbd_ncc_hoa_don` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết số dư ban đầu NCC - Hóa đơn (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sdbd_so_du_ban_dau_nha_cung_cap` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sdbd_so_du_ban_dau_nha_cung_cap` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `SoDuBanDauNCCId` | `so_du_ban_dau_ncc_id` | `uuid` | N | — | ID số dư ban đầu nhà cung cấp (reference ENT_SoDuBanDauNCC) `FK` |
| 2 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Thông tin hóa đơn]** Tỷ giá |
| 3 | `GiaTriHoaDon` | `gia_tri_hoa_don` | `money_foreign` ≈ | Y | `0` | **[Thông tin hóa đơn]** Giá trị hóa đơn |
| 4 | `GiaTriHoaDonQuyDoi` | `gia_tri_hoa_don_quy_doi` | `money_vnd` | Y | `0` | **[Thông tin hóa đơn]** Giá trị hóa đơn quy đổi |
| 5 | `ConPhaiTra` | `con_phai_tra` | `money_foreign` ≈ | Y | `0` | **[Thông tin hóa đơn]** Còn phải trả |
| 6 | `ConPhaiTraQuyDoi` | `con_phai_tra_quy_doi` | `money_vnd` | Y | `0` | **[Thông tin hóa đơn]** Còn phải trả quy đổi |
| 7 | `DaTra` | `da_tra` | `numeric(18,4)` ⚠ | Y | `0` | **[Thông tin hóa đơn]** Đã trả |
| 8 | `DaTraQuyDoi` | `da_tra_quy_doi` | `money_vnd` | Y | `0` | **[Thông tin hóa đơn]** Đã trả quy đổi |
| 9 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | **[Thông tin hóa đơn]** ID nhân viên phụ trách (reference ENT_DoiTuong, vai trò NhanVien) `FK` |

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

**Đối chiếu `sdbd_chi_tiet_sdbd_ncc_hoa_don` (21 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 3 | `ngay_chung_tu`, `so_chung_tu`, `phien_ban` |

---

## 8. `sdbd_so_du_ban_dau_nhan_vien`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoDuBanDauNhanVien` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_so_du_ban_dau_nhan_vien` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Số dư ban đầu Nhân viên |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản công nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 2 | `NhanVienId` | `nhan_vien_id` | `uuid` | N | — | ID nhân viên (reference ENT_DoiTuong, vai trò NhanVien) `FK` |
| 3 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | ID loại tiền (reference ENT_LoaiTien) `FK` |
| 4 | `DuNo` | `du_no` | `money_foreign` ≈ | Y | `0` | Dư Nợ |
| 5 | `DuNoQuyDoi` | `du_no_quy_doi` | `money_vnd` | Y | `0` | Dư Nợ quy đổi |
| 6 | `DuCo` | `du_co` | `money_foreign` ≈ | Y | `0` | Dư Có |
| 7 | `DuCoQuyDoi` | `du_co_quy_doi` | `money_vnd` | Y | `0` | Dư Có quy đổi |

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

**Đối chiếu `sdbd_so_du_ban_dau_nhan_vien` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 9. `sdbd_so_du_ban_dau_vat_tu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoDuBanDauVatTu` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sdbd_so_du_ban_dau_vat_tu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Số dư ban đầu Vật tư |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID vật tư (reference ENT_VatTu) `FK` |
| 2 | `KhoId` | `kho_id` | `uuid` | N | — | ID kho (reference ENT_Kho) `FK` |
| 3 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | ID đơn vị tính đã chọn (reference ENT_DonViTinh) `FK` |
| 4 | `DonViQuyDoiVatTuId` | `don_vi_quy_doi_vat_tu_id` | `uuid` | Y | — | ID bản ghi đơn vị quy đổi của vật tư (reference ENT_DonViQuyDoiVatTu) `FK` |
| 5 | `SoLuongTon` | `so_luong_ton` | `quantity` | N | `0` | Số lượng tồn theo đơn vị tính đã chọn |
| 6 | `GiaTriTon` | `gia_tri_ton` | `money_foreign` ≈ | Y | `0` | Giá trị tồn |
| 7 | `TyLeChuyenDoi` | `ty_le_chuyen_doi` | `percent_rate` | N | `0` | Tỷ lệ chuyển đổi về đơn vị chính |
| 8 | `PhepTinh` | `phep_tinh` | `text` | Y | — | Phép tính quy đổi (Nhân, Chia) |
| 9 | `SoLuongTonDonViChinh` | `so_luong_ton_don_vi_chinh` | `quantity` | N | `0` | Số lượng tồn theo đơn vị tính chính |
| 10 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | Số lô |
| 11 | `HanSuDung` | `han_su_dung` | `date` | Y | — | Hạn sử dụng của lô |

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

**Đối chiếu `sdbd_so_du_ban_dau_vat_tu` (21 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

