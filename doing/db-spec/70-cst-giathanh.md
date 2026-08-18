# `cst_` — Giá thành

> Sinh tự động từ [`ldm-GiaThanh.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-GiaThanh.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**18 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> Mọi trường kiểu numeric đều NOT NULL (numeric!). Với các trường chỉ dùng cho một phương pháp/tình huống cụ thể, trường hợp không sử dụng mang giá trị 0 (không dùng NULL) để bảo đảm mọi phép cộng và phép SUM luôn cho kết quả xác định. Bộ trường hệ thống (DaXoa, NguoiTao, ThoiGianTao, NguoiCapNhat, ThoiGianCapNhat, NguoiGhiSo, ThoiGianGhiSo, NguoiXoa, ThoiGianXoa) áp dụng

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `CauHinhGiaThanh` | `cst_cau_hinh_gia_thanh` | `cst_cau_hinh_gia_thanh` | B — có schema, chưa code | Cấu hình / thiết lập — Cấu hình giá thành (yếu tố chi phí theo phương pháp tính) |
| 2 | `ThietLapHeSoTyLe` | `cst_thiet_lap_he_so_ty_le` | `cst_thiet_lap_he_so_ty_le` | B — có schema, chưa code | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Thiết lập hệ số, tỷ lệ theo kỳ (phương pháp Hệ số, tỷ lệ) |
| 3 | `KyTinhGiaThanh` | `cst_ky_tinh_gia_thanh` | `cst_ky_tinh_gia_thanh` | B — có schema, chưa code | Kết quả / số dư luân chuyển — Kỳ tính giá thành |
| 4 | `DoDangDauKy` | `cst_do_dang_dau_ky` | `cst_do_dang_dau_ky` | B — có schema, chưa code | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Dở dang đầu kỳ |
| 5 | `DoDangCuoiKy` | `cst_do_dang_cuoi_ky` | `cst_do_dang_cuoi_ky` | B — có schema, chưa code | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Dở dang cuối kỳ (Master) |
| 6 | `ChiTietDoDangCuoiKy` | `cst_do_dang_cuoi_ky_chi_tiet` | `cst_chi_tiet_do_dang_cuoi_ky` | B — có schema, chưa code | Dòng chi tiết của `cst_do_dang_cuoi_ky` — Chi tiết dở dang cuối kỳ theo sản phẩm (Detail) |
| 7 | `PhanBoChiPhi` | `cst_phan_bo_chi_phi` | `cst_phan_bo_chi_phi` | B — có schema, chưa code | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Phân bổ chi phí (thiết lập và số tiền phân bổ của một tài khoản tập hợp trong kỳ) |
| 8 | `PhanBoChiPhi_DoiTuong` | `cst_phan_bo_chi_phi_doi_tuong` | — | C — tạo mới | Dòng chi tiết của `cst_phan_bo_chi_phi` — Đối tượng nhận phân bổ (Link) |
| 9 | `HeSoPhanBo` | `cst_he_so_phan_bo` | `cst_he_so_phan_bo` | B — có schema, chưa code | Dòng chi tiết của `cst_phan_bo_chi_phi` — Hệ số phân bổ nhập tay (khi tiêu thức = Hệ số) |
| 10 | `ChiTietPhanBoChiPhi` | `cst_phan_bo_chi_phi_chi_tiet` | `cst_chi_tiet_phan_bo_chi_phi` | B — có schema, chưa code | Dòng chi tiết của `cst_phan_bo_chi_phi` — Kết quả phân bổ cho từng đối tượng (Detail) |
| 11 | `PhanBoChungTu` | `cst_phan_bo_chung_tu` | `cst_phan_bo_chung_tu` | B — có schema, chưa code | Kết quả / số dư luân chuyển — Lũy kế đã phân bổ theo từng chứng từ chi phí |
| 12 | `GiaThanhSanPham` | `cst_gia_thanh_san_pham` | `cst_gia_thanh_san_pham` | B — có schema, chưa code | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Kết quả tính giá thành sản phẩm |
| 13 | `ChungTuGiaThanh` | `cst_chung_tu_gia_thanh` | `cst_chung_tu_gia_thanh` | B — có schema, chưa code | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Chứng từ kết chuyển chi phí (Master - mỗi kỳ một chứng từ) |
| 14 | `ChiTietChungTuGiaThanh` | `cst_chung_tu_gia_thanh_chi_tiet` | `cst_chi_tiet_chung_tu_gia_thanh` | B — có schema, chưa code | Dòng chi tiết của `cst_chung_tu_gia_thanh` — Dòng bút toán kết chuyển (Detail) |
| 15 | `GiaThanhCongTrinh` | `cst_gia_thanh_cong_trinh` | — | C — tạo mới | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Kết quả tập hợp chi phí theo công trình vụ việc (phương pháp Công trình vụ việc - Bước 4) |
| 16 | `PhieuNghiemThuCongTrinh` | `cst_phieu_nghiem_thu_cong_trinh` | — | C — tạo mới | Dòng chi tiết của `cst_ky_tinh_gia_thanh` — Phiếu nghiệm thu công trình vụ việc (Master - mỗi kỳ tối đa một phiếu) (phương pháp Công trình vụ việc - Bước 6) |
| 17 | `ChiTietPhieuNghiemThuCongTrinh` | `cst_phieu_nghiem_thu_cong_trinh_chi_tiet` | — | C — tạo mới | Dòng chi tiết của `cst_phieu_nghiem_thu_cong_trinh` — Dòng chi tiết phiếu nghiệm thu công trình vụ việc (Detail) |
| 18 | `DinhMucGiaThanh` | `cst_dinh_muc_gia_thanh` | `cst_dinh_muc_gia_thanh` | B — có schema, chưa code | Cấu hình / thiết lập — Định mức giá thành theo sản phẩm |

---

## 1. `cst_cau_hinh_gia_thanh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `CauHinhGiaThanh` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_cau_hinh_gia_thanh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Cấu hình giá thành (yếu tố chi phí theo phương pháp tính) |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuongPhapTinh` | `phuong_phap_tinh` | `text` CHECK | N | — | Phương pháp tính giá thành (TrucTiep \| HeSoTyLe \| CongTrinhVuViec \| DonHang \| HopDong) |
| 2 | `LoaiYeuTo` | `loai_yeu_to` | `text` CHECK | N | — | Yếu tố chi phí (NguyenVatLieu \| NhanCong \| SanXuatChung) |
| 3 | `TaiKhoanTapHopChiPhiId` | `tai_khoan_tap_hop_chi_phi_id` | `uuid` | N | — | ID tài khoản tập hợp chi phí (reference ENT_HeThongTaiKhoan) `FK` |
| 4 | `TieuThucPhanBo` | `tieu_thuc_phan_bo` | `text` CHECK | N | — | Tiêu thức phân bổ mặc định (SanLuongNhapKho \| HeSo \| TaiKhoan \| ChiPhiNVL \| ChiPhiNVLVaNhanCong) |
| 5 | `TaiKhoanKetChuyenId` | `tai_khoan_ket_chuyen_id` | `uuid` | N | — | ID tài khoản kết chuyển (reference ENT_HeThongTaiKhoan). Bất biến: mọi bản ghi cùng (TenantId, ChiNhanhId, PhuongPhapTinh) phải có cùng giá trị, bất kể LoaiYeuTo `FK` |
| 6 | `ChiPhiDua1Lan` | `chi_phi_dua_1_lan` | `boolean` | N | `false` | Chi phí đưa vào 1 lần ngay từ đầu sản xuất. Bất biến: mọi bản ghi cùng (TenantId, PhuongPhapTinh, LoaiYeuTo) phải có cùng giá trị |

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

**Đối chiếu `cst_cau_hinh_gia_thanh` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `chi_phi_dua_1_lan` |
| DB có — LDM **không khai** | 2 | `co_yeu_to_do_dang`, `phien_ban` |

---

## 2. `cst_thiet_lap_he_so_ty_le`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThietLapHeSoTyLe` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_thiet_lap_he_so_ty_le` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Thiết lập hệ số, tỷ lệ theo kỳ (phương pháp Hệ số, tỷ lệ) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | N | — | ID đối tượng tập hợp chi phí (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 3 | `Loai` | `loai` | `text` CHECK | N | — | Phương pháp (HeSo \| TyLe) |
| 4 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID sản phẩm chi tiết của đối tượng (reference ENT_VatTu) `FK` |
| 5 | `HeSo` | `he_so` | `exchange_rate` ≈ | N | `0` | Hệ số của sản phẩm |
| 6 | `ChiPhiNVLDinhMuc` | `chi_phi_nvl_dinh_muc` | `money_foreign` ≈ | N | `0` | Định mức giá thành nguyên vật liệu |
| 7 | `ChiPhiNhanCongDinhMuc` | `chi_phi_nhan_cong_dinh_muc` | `money_foreign` ≈ | N | `0` | Định mức giá thành nhân công |
| 8 | `ChiPhiSanXuatChungDinhMuc` | `chi_phi_san_xuat_chung_dinh_muc` | `money_foreign` ≈ | N | `0` | Định mức giá thành sản xuất chung |
| 9 | `TyLePhanBoGiaThanh` | `ty_le_phan_bo_gia_thanh` | `percent_rate` | N | `0` | Tỷ lệ phân bổ giá thành của sản phẩm |

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

**Đối chiếu `cst_thiet_lap_he_so_ty_le` (18 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `ty_le_phan_bo_gia_thanh` |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 3. `cst_ky_tinh_gia_thanh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KyTinhGiaThanh` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_ky_tinh_gia_thanh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Kỳ tính giá thành |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |
| Bảng con | `cst_thiet_lap_he_so_ty_le` · `cst_do_dang_dau_ky` · `cst_do_dang_cuoi_ky` · `cst_phan_bo_chi_phi` · `cst_gia_thanh_san_pham` · `cst_chung_tu_gia_thanh` · `cst_gia_thanh_cong_trinh` · `cst_phieu_nghiem_thu_cong_trinh` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Ten` | `ten` | `text` | N | — | Tên kỳ tính giá thành |
| 2 | `Tu` | `tu` | `date` | N | — | Từ ngày |
| 3 | `Den` | `den` | `date` | N | — | Đến ngày |
| 4 | `PhuongPhapTinh` | `phuong_phap_tinh` | `text` CHECK | N | — | Phương pháp tính (TrucTiep \| HeSoTyLe \| CongTrinhVuViec \| DonHang \| HopDong) |
| 5 | `PhuongPhapDanhGiaDoDang` | `phuong_phap_danh_gia_do_dang` | `text` CHECK | Y | — | Phương pháp đánh giá dở dang cuối kỳ (SanPhamHoanThanhTuongDuong \| NguyenVatLieuTrucTiep \| DinhMucGiaThanh) |
| 6 | `ThoiDiemTinhGanNhat` | `thoi_diem_tinh_gan_nhat` | `timestamptz` | Y | — | Thời điểm tính giá thành gần nhất |
| 7 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | Trạng thái kỳ (ChuaThucHien \| DangThucHien \| DaHoanThanh) |

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

**Đối chiếu `cst_ky_tinh_gia_thanh` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `phuong_phap_danh_gia_do_dang` |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 4. `cst_do_dang_dau_ky`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DoDangDauKy` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_do_dang_dau_ky` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dở dang đầu kỳ |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Đối tượng dở dang - chọn đúng một trường theo phương pháp tính của kỳ]** ID đối tượng dở dang (reference ENT_DoiTuongTapHopChiPhi). Bắt buộc với phương pháp TrucTiep và HeSoTyLe; để trống với phương pháp CongTrinhVuViec `FK` |
| 3 | `CongTrinhId` | `cong_trinh_id` | `uuid` | Y | — | **[Đối tượng dở dang - chọn đúng một trường theo phương pháp tính của kỳ]** ID công trình vụ việc dở dang (reference ENT_CongTrinh). Bắt buộc với phương pháp CongTrinhVuViec; để trống với phương pháp khác. Chỉ nhận công trình vụ việc KHÔNG có cấp con `FK` |
| 4 | `ChiPhiNVLDoDangDauKy` | `chi_phi_nvl_do_dang_dau_ky` | `money_foreign` ≈ | N | `0` | **[Đối tượng dở dang - chọn đúng một trường theo phương pháp tính của kỳ]** Chi phí nguyên vật liệu dở dang đầu kỳ. Với phương pháp CongTrinhVuViec mang nghĩa LŨY KẾ chi phí nguyên vật liệu của công trình vụ việc tính đến đầu kỳ |
| 5 | `ChiPhiNhanCongDoDangDauKy` | `chi_phi_nhan_cong_do_dang_dau_ky` | `money_foreign` ≈ | N | `0` | **[Đối tượng dở dang - chọn đúng một trường theo phương pháp tính của kỳ]** Chi phí nhân công dở dang đầu kỳ. Với phương pháp CongTrinhVuViec mang nghĩa LŨY KẾ chi phí nhân công của công trình vụ việc tính đến đầu kỳ |
| 6 | `ChiPhiSXChungDoDangDauKy` | `chi_phi_sx_chung_do_dang_dau_ky` | `money_foreign` ≈ | N | `0` | **[Đối tượng dở dang - chọn đúng một trường theo phương pháp tính của kỳ]** Chi phí sản xuất chung dở dang đầu kỳ. Với phương pháp CongTrinhVuViec mang nghĩa LŨY KẾ chi phí sản xuất chung của công trình vụ việc tính đến đầu kỳ |
| 7 | `TongChiPhi` | `tong_chi_phi` | `money_foreign` ≈ | N | `0` | **[Đối tượng dở dang - chọn đúng một trường theo phương pháp tính của kỳ]** Tổng chi phí dở dang đầu kỳ (= ChiPhiNVLDoDangDauKy + ChiPhiNhanCongDoDangDauKy + ChiPhiSXChungDoDangDauKy) |
| 8 | `SoDaNghiemThu` | `so_da_nghiem_thu` | `numeric(18,4)` ⚠ | N | `0` | **[Đối tượng dở dang - chọn đúng một trường theo phương pháp tính của kỳ]** Lũy kế giá trị công trình vụ việc đã nghiệm thu tính đến đầu kỳ, người dùng nhập tay MỘT SỐ TỔNG (chỉ dùng cho phương pháp CongTrinhVuViec). KHÔNG tách và KHÔNG lưu chi tiết theo yếu tố chi phí |

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

**Đối chiếu `cst_do_dang_dau_ky` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `cong_trinh_id`, `so_da_nghiem_thu` |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 5. `cst_do_dang_cuoi_ky`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DoDangCuoiKy` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_do_dang_cuoi_ky` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dở dang cuối kỳ (Master) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |
| Bảng con | `cst_do_dang_cuoi_ky_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | N | — | ID đối tượng dở dang (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 3 | `ChiPhiNVLDoDangCuoiKy` | `chi_phi_nvl_do_dang_cuoi_ky` | `money_foreign` ≈ | N | `0` | Chi phí nguyên vật liệu dở dang cuối kỳ |
| 4 | `ChiPhiNhanCongDoDangCuoiKy` | `chi_phi_nhan_cong_do_dang_cuoi_ky` | `money_foreign` ≈ | N | `0` | Chi phí nhân công dở dang cuối kỳ |
| 5 | `ChiPhiSanXuatChungDoDangCuoiKy` | `chi_phi_san_xuat_chung_do_dang_cuoi_ky` | `money_foreign` ≈ | N | `0` | Chi phí sản xuất chung dở dang cuối kỳ |
| 6 | `TongChiPhi` | `tong_chi_phi` | `money_foreign` ≈ | N | `0` | Tổng chi phí dở dang cuối kỳ |

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

**Đối chiếu `cst_do_dang_cuoi_ky` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 6. `cst_do_dang_cuoi_ky_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDoDangCuoiKy` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_chi_tiet_do_dang_cuoi_ky` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết dở dang cuối kỳ theo sản phẩm (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_do_dang_cuoi_ky` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_do_dang_cuoi_ky` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DoDangCuoiKyId` | `do_dang_cuoi_ky_id` | `uuid` | N | — | ID dở dang cuối kỳ (reference ENT_DoDangCuoiKy) `FK` |
| 2 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID sản phẩm dở dang (reference ENT_VatTu) `FK` |
| 3 | `SoLuong` | `so_luong` | `quantity` | N | `0` | Số lượng dở dang cuối kỳ |
| 4 | `TyLeHoanThanh` | `ty_le_hoan_thanh` | `percent_rate` | N | `0` | Tỷ lệ hoàn thành (%) |
| 5 | `DinhMucNVL` | `dinh_muc_nvl` | `numeric(18,4)` ⚠ | N | `0` | Định mức nguyên vật liệu |
| 6 | `DinhMucNhanCong` | `dinh_muc_nhan_cong` | `money_foreign` ≈ | N | `0` | Định mức nhân công |
| 7 | `DinhMucSXChung` | `dinh_muc_sx_chung` | `numeric(18,4)` ⚠ | N | `0` | Định mức sản xuất chung |
| 8 | `TongDonGiaDinhMuc` | `tong_don_gia_dinh_muc` | `money_foreign` ≈ | N | `0` | Tổng đơn giá định mức |

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

**Đối chiếu `cst_chi_tiet_do_dang_cuoi_ky` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `dinh_muc_nhan_cong`, `dinh_muc_sx_chung`, `tong_don_gia_dinh_muc` |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 7. `cst_phan_bo_chi_phi`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhanBoChiPhi` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_phan_bo_chi_phi` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phân bổ chi phí (thiết lập và số tiền phân bổ của một tài khoản · tập hợp trong kỳ) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |
| Bảng con | `cst_phan_bo_chi_phi_doi_tuong` · `cst_he_so_phan_bo` · `cst_phan_bo_chi_phi_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `TaiKhoanId` | `tai_khoan_id` | `uuid` | N | — | ID tài khoản tập hợp chi phí được phân bổ (reference ENT_HeThongTaiKhoan) `FK` |
| 3 | `TieuThucPhanBo` | `tieu_thuc_phan_bo` | `text` CHECK | N | — | Tiêu thức phân bổ (SanLuongNhapKho \| HeSo \| TaiKhoan \| ChiPhiNVL \| ChiPhiNVLVaNhanCong) |
| 4 | `TaiKhoanTieuThucId` | `tai_khoan_tieu_thuc_id` | `uuid` | Y | — | ID tài khoản làm tiêu thức (reference ENT_HeThongTaiKhoan; chỉ có giá trị khi TieuThucPhanBo = TaiKhoan) `FK` |
| 5 | `TongChiPhi` | `tong_chi_phi` | `money_foreign` ≈ | N | `0` | Tổng chi phí cần phân bổ của tài khoản trong kỳ, chốt tại thời điểm thực hiện phân bổ |
| 6 | `ChiPhiDaPhanBo` | `chi_phi_da_phan_bo` | `money_foreign` ≈ | N | `0` | Số tiền phân bổ kỳ này |

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

**Đối chiếu `cst_phan_bo_chi_phi` (18 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 3 | `loai_yeu_to`, `doi_tuong_phan_bo`, `phien_ban` |

---

## 8. `cst_phan_bo_chi_phi_doi_tuong`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhanBoChiPhi_DoiTuong` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Đối tượng nhận phân bổ (Link) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_phan_bo_chi_phi` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_phan_bo_chi_phi` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhanBoChiPhiId` | `phan_bo_chi_phi_id` | `uuid` | N | — | ID thiết lập phân bổ (reference ENT_PhanBoChiPhi) `FK` |
| 2 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** ID đối tượng nhận phân bổ (reference ENT_DoiTuongTapHopChiPhi). Bắt buộc với phương pháp TrucTiep và HeSoTyLe; để trống với phương pháp CongTrinhVuViec `FK` |
| 3 | `DoiTuongPhanBoCongTrinhId` | `doi_tuong_phan_bo_cong_trinh_id` | `uuid` | Y | — | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** ID công trình vụ việc nhận phân bổ (reference ENT_CongTrinh). Bắt buộc với phương pháp CongTrinhVuViec; để trống với phương pháp khác. Chỉ nhận công trình vụ việc KHÔNG có cấp con và đang Hoạt động `FK` |

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

---

## 9. `cst_he_so_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HeSoPhanBo` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_he_so_phan_bo` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Hệ số phân bổ nhập tay (khi tiêu thức = Hệ số) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_phan_bo_chi_phi` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_phan_bo_chi_phi` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhanBoChiPhiId` | `phan_bo_chi_phi_id` | `uuid` | N | — | ID thiết lập phân bổ (reference ENT_PhanBoChiPhi) `FK` |
| 2 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** ID đối tượng nhận phân bổ (reference ENT_DoiTuongTapHopChiPhi). Bắt buộc với phương pháp TrucTiep và HeSoTyLe; để trống với phương pháp CongTrinhVuViec `FK` |
| 3 | `DoiTuongPhanBoCongTrinhId` | `doi_tuong_phan_bo_cong_trinh_id` | `uuid` | Y | — | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** ID công trình vụ việc nhận phân bổ (reference ENT_CongTrinh). Bắt buộc với phương pháp CongTrinhVuViec; để trống với phương pháp khác `FK` |
| 4 | `HeSo` | `he_so` | `exchange_rate` ≈ | N | `0` | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** Hệ số phân bổ, phải > 0. Một đối tượng chỉ được khai đúng một hệ số trong cùng một thiết lập phân bổ |

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

**Đối chiếu `cst_he_so_phan_bo` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `doi_tuong_phan_bo_cong_trinh_id` |
| DB có — LDM **không khai** | 2 | `loai_yeu_to`, `phien_ban` |

---

## 10. `cst_phan_bo_chi_phi_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhanBoChiPhi` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_chi_tiet_phan_bo_chi_phi` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Kết quả phân bổ cho từng đối tượng (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_phan_bo_chi_phi` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_phan_bo_chi_phi` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhanBoChiPhiId` | `phan_bo_chi_phi_id` | `uuid` | N | — | ID thiết lập phân bổ (reference ENT_PhanBoChiPhi) `FK` |
| 2 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** ID đối tượng nhận phân bổ (reference ENT_DoiTuongTapHopChiPhi). Bắt buộc với phương pháp TrucTiep và HeSoTyLe; để trống với phương pháp CongTrinhVuViec `FK` |
| 3 | `ChiTietPhanBoCongTrinhId` | `chi_tiet_phan_bo_cong_trinh_id` | `uuid` | Y | — | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** ID công trình vụ việc nhận phân bổ (reference ENT_CongTrinh). Bắt buộc với phương pháp CongTrinhVuViec; để trống với phương pháp khác `FK` |
| 4 | `ChiPhiNVLPhanBo` | `chi_phi_nvl_phan_bo` | `money_foreign` ≈ | N | `0` | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** Chi phí nguyên vật liệu được phân bổ |
| 5 | `ChiPhiNhanCongPhanBo` | `chi_phi_nhan_cong_phan_bo` | `money_foreign` ≈ | N | `0` | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** Chi phí nhân công được phân bổ |
| 6 | `ChiPhiSanXuatChungPhanBo` | `chi_phi_san_xuat_chung_phan_bo` | `money_foreign` ≈ | N | `0` | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** Chi phí sản xuất chung được phân bổ |
| 7 | `TongChiPhiPhanBo` | `tong_chi_phi_phan_bo` | `money_foreign` ≈ | N | `0` | **[Đối tượng nhận phân bổ - chọn đúng một trường theo phương pháp tính của kỳ]** Tổng chi phí được phân bổ |

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

**Đối chiếu `cst_chi_tiet_phan_bo_chi_phi` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `chi_tiet_phan_bo_cong_trinh_id`, `chi_phi_san_xuat_chung_phan_bo` |
| DB có — LDM **không khai** | 2 | `chi_phi_sx_chung_phan_bo`, `phien_ban` |

---

## 11. `cst_phan_bo_chung_tu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhanBoChungTu` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_phan_bo_chung_tu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Lũy kế đã phân bổ theo từng chứng từ chi phí |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuId` | `chung_tu_id` | `uuid` | N | — | ID chứng từ chi phí trên Sổ cái (khớp SoCai.ChungTuId) |
| 2 | `SoTienDaPhanBo` | `so_tien_da_phan_bo` | `money_foreign` ≈ | N | `0` | Số tiền của chứng từ đã được phân bổ lũy kế |

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

**Đối chiếu `cst_phan_bo_chung_tu` (13 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 2 | `loai_chung_tu_id`, `phien_ban` |

---

## 12. `cst_gia_thanh_san_pham`

| Mục | Nội dung |
|---|---|
| Entity LDM | `GiaThanhSanPham` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_gia_thanh_san_pham` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Kết quả tính giá thành sản phẩm |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | N | — | ID đối tượng tập hợp chi phí chứa sản phẩm (reference ENT_DoiTuongTapHopChiPhi). Trực tiếp: đối tượng loại sản phẩm; Hệ số tỷ lệ: phân xưởng, quy trình sản xuất, nhóm sản phẩm `FK` |
| 3 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID sản phẩm được tính giá thành (reference ENT_VatTu) `FK` |
| 4 | `ChiPhiNVL` | `chi_phi_nvl` | `money_foreign` ≈ | N | `0` | Chi phí nguyên vật liệu trong giá thành |
| 5 | `ChiPhiNhanCong` | `chi_phi_nhan_cong` | `money_foreign` ≈ | N | `0` | Chi phí nhân công trong giá thành |
| 6 | `ChiPhiSXChung` | `chi_phi_sx_chung` | `money_foreign` ≈ | N | `0` | Chi phí sản xuất chung trong giá thành |
| 7 | `TongChiPhi` | `tong_chi_phi` | `money_foreign` ≈ | N | `0` | Tổng giá thành |
| 8 | `SoLuongNhapKho` | `so_luong_nhap_kho` | `quantity` | N | `0` | Số lượng nhập kho trong kỳ tại thời điểm tính |
| 9 | `GiaThanh` | `gia_thanh` | `numeric(18,4)` ⚠ | N | `0` | Giá thành đơn vị |

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

**Đối chiếu `cst_gia_thanh_san_pham` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 2 | `thoi_diem_tinh`, `phien_ban` |

---

## 13. `cst_chung_tu_gia_thanh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuGiaThanh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_chung_tu_gia_thanh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chứng từ kết chuyển chi phí (Master - mỗi kỳ một chứng từ) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |
| Bảng con | `cst_chung_tu_gia_thanh_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |
| 3 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Đầu chứng từ]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `cst_chung_tu_gia_thanh` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 5 | `so_chung_tu`, `ngay_chung_tu`, `ngay_hach_toan`, `mo_ta`, `phien_ban` |

---

## 14. `cst_chung_tu_gia_thanh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietChungTuGiaThanh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_chi_tiet_chung_tu_gia_thanh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng bút toán kết chuyển (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_chung_tu_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_chung_tu_gia_thanh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuGiaThanhId` | `chung_tu_gia_thanh_id` | `uuid` | N | — | ID chứng từ kết chuyển (reference ENT_ChungTuGiaThanh) `FK` |
| 2 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản kết chuyển, vế Nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 3 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản tập hợp chi phí, vế Có (reference ENT_HeThongTaiKhoan) `FK` |
| 4 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | Số tiền kết chuyển |
| 5 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | ID đối tượng tập hợp chi phí của dòng bút toán (reference ENT_DoiTuongTapHopChiPhi). Bắt buộc với phương pháp TrucTiep và HeSoTyLe; LUÔN để trống với phương pháp CongTrinhVuViec `FK` |
| 6 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 7 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Trường tự do]** ID đơn vị (reference ENT_DonVi) `FK` |
| 8 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Trường tự do]** ID vụ việc (reference ENT_CongTrinh). Với phương pháp TrucTiep và HeSoTyLe là trường thống kê tự do, mặc định trống; với phương pháp CongTrinhVuViec là KHÓA NGHIỆP VỤ của dòng, hệ thống sinh, bắt buộc có giá trị `FK` |

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

**Đối chiếu `cst_chi_tiet_chung_tu_gia_thanh` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `khoan_muc_chi_phi_id`, `don_vi_id`, `vu_viec_id` |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 15. `cst_gia_thanh_cong_trinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `GiaThanhCongTrinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Kết quả tập hợp chi phí theo công trình vụ việc · (phương pháp Công trình vụ việc - Bước 4) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `CongTrinhId` | `cong_trinh_id` | `uuid` | N | — | ID công trình vụ việc (reference ENT_CongTrinh). Chỉ tạo bản ghi cho công trình vụ việc KHÔNG có cấp con `FK` |
| 3 | `ChiPhiNVLPhatSinhTrongKy` | `chi_phi_nvl_phat_sinh_trong_ky` | `money_foreign` ≈ | N | `0` | **[Không bao gồm dở dang đầu kỳ và không phải giá trị lũy kế.]** Chi phí nguyên vật liệu phát sinh trong kỳ (chi phí trực tiếp gắn công trình vụ việc + chi phí được phân bổ) |
| 4 | `ChiPhiNhanCongPhatSinhTrongKy` | `chi_phi_nhan_cong_phat_sinh_trong_ky` | `money_foreign` ≈ | N | `0` | **[Không bao gồm dở dang đầu kỳ và không phải giá trị lũy kế.]** Chi phí nhân công phát sinh trong kỳ |
| 5 | `ChiPhiSXChungPhatSinhTrongKy` | `chi_phi_sx_chung_phat_sinh_trong_ky` | `money_foreign` ≈ | N | `0` | **[Không bao gồm dở dang đầu kỳ và không phải giá trị lũy kế.]** Chi phí sản xuất chung phát sinh trong kỳ |
| 6 | `TongChiPhiPhatSinhTrongKy` | `tong_chi_phi_phat_sinh_trong_ky` | `money_foreign` ≈ | N | `0` | **[Không bao gồm dở dang đầu kỳ và không phải giá trị lũy kế.]** Tổng chi phí phát sinh trong kỳ (= tổng 3 trường phát sinh trên) |
| 7 | `TongChiPhiNghiemThuTrongKy` | `tong_chi_phi_nghiem_thu_trong_ky` | `money_foreign` ≈ | N | `0` | **[Số nghiệm thu của kỳ - do bước Nghiệm thu công trình vụ việc ghi.]** Số tiền nghiệm thu trong kỳ của công trình vụ việc. KHÔNG tách và KHÔNG lưu chi tiết theo yếu tố chi phí. Bị đặt về 0 khi Bỏ ghi sổ phiếu nghiệm thu |

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

---

## 16. `cst_phieu_nghiem_thu_cong_trinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuNghiemThuCongTrinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu nghiệm thu công trình vụ việc (Master - mỗi kỳ tối đa một phiếu) · (phương pháp Công trình vụ việc - Bước 6) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_ky_tinh_gia_thanh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_ky_tinh_gia_thanh` — FK `ON DELETE CASCADE` |
| Bảng con | `cst_phieu_nghiem_thu_cong_trinh_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyTinhGiaThanhId` | `ky_tinh_gia_thanh_id` | `uuid` | N | — | ID kỳ tính giá thành (reference ENT_KyTinhGiaThanh) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải, mặc định "Nghiệm thu giá vốn {Tên kỳ tính giá thành}" |
| 3 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Đầu chứng từ]** Trạng thái phiếu (ChuaGhiSo \| DaGhiSo). Phiếu luôn được tạo mới ở trạng thái DaGhiSo; ChuaGhiSo chỉ đạt tới bằng thao tác Bỏ ghi sổ |

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

---

## 17. `cst_phieu_nghiem_thu_cong_trinh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuNghiemThuCongTrinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng chi tiết phiếu nghiệm thu công trình vụ việc (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cst_phieu_nghiem_thu_cong_trinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cst_phieu_nghiem_thu_cong_trinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuNghiemThuCongTrinhId` | `phieu_nghiem_thu_cong_trinh_id` | `uuid` | N | — | ID phiếu nghiệm thu (reference ENT_PhieuNghiemThuCongTrinh) `FK` |
| 2 | `CongTrinhId` | `cong_trinh_id` | `uuid` | N | — | ID công trình vụ việc được nghiệm thu (reference ENT_CongTrinh). Mỗi công trình vụ việc chỉ có đúng 1 dòng trên phiếu `FK` |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải dòng, mặc định "Nghiệm thu công trình {Tên công trình vụ việc}" |
| 4 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản ghi Nợ, mặc định tài khoản giá vốn 632 cấp cuối (reference ENT_HeThongTaiKhoan) `FK` |
| 5 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản ghi Có, mặc định CauHinhGiaThanh.TaiKhoanKetChuyenId (reference ENT_HeThongTaiKhoan). Chỉ được chọn tài khoản đó hoặc tài khoản cấp con của nó `FK` |
| 6 | `SoChuaNghiemThu` | `so_chua_nghiem_thu` | `numeric(18,4)` ⚠ | N | `0` | Số chưa nghiệm thu của công trình vụ việc tại thời điểm lập phiếu, ĐƯỢC PHÉP ÂM |
| 7 | `TyLeNghiemThu` | `ty_le_nghiem_thu` | `percent_rate` | N | `0` | Tỷ lệ nghiệm thu (%, 0 đến 100, mặc định 100). Chỉ là công cụ nhập liệu và hiển thị |
| 8 | `SoTienNghiemThu` | `so_tien_nghiem_thu` | `money_foreign` ≈ | N | `0` | Số tiền nghiệm thu của dòng - SỐ CHUẨN được lưu và hạch toán. Cùng dấu và không vượt SoChuaNghiemThu về giá trị tuyệt đối, ĐƯỢC PHÉP ÂM |
| 9 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 10 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Trường tự do]** ID đơn vị (reference ENT_DonVi) `FK` |

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

---

## 18. `cst_dinh_muc_gia_thanh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DinhMucGiaThanh` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cst_dinh_muc_gia_thanh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Định mức giá thành theo sản phẩm |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID sản phẩm (reference ENT_VatTu) `FK` |
| 2 | `DinhMucNVL` | `dinh_muc_nvl` | `numeric(18,4)` ⚠ | N | `0` | Định mức chi phí nguyên vật liệu |
| 3 | `DinhMucNhanCong` | `dinh_muc_nhan_cong` | `money_foreign` ≈ | N | `0` | Định mức chi phí nhân công |
| 4 | `DinhMucSXChung` | `dinh_muc_sx_chung` | `numeric(18,4)` ⚠ | N | `0` | Định mức chi phí sản xuất chung |
| 5 | `TongDinhMuc` | `tong_dinh_muc` | `money_foreign` ≈ | N | `0` | Tổng định mức |

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

**Đối chiếu `cst_dinh_muc_gia_thanh` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

