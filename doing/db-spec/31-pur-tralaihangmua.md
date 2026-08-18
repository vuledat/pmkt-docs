# `pur_` — Trả lại hàng mua

> Sinh tự động từ [`ldm-TraLaiHangMua.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-TraLaiHangMua.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**3 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ChungTuTraLaiHangMua` | `pur_chung_tu_tra_lai_hang_mua` | `pur_chung_tu_tra_lai_hang_mua` | B — có schema, chưa code | Đầu chứng từ — Chứng từ trả lại hàng mua |
| 2 | `PhieuXuatKhoTraLaiHangMua` | `pur_phieu_xuat_kho_tra_lai_hang_mua` | — | C — tạo mới | Đầu chứng từ — Phiếu xuất kho của chứng từ trả lại hàng mua |
| 3 | `ChiTietChungTuTraLaiHangMua` | `pur_chung_tu_tra_lai_hang_mua_chi_tiet` | `pur_chi_tiet_chung_tu_tra_lai_hang_mua` | B — có schema, chưa code | Dòng chi tiết của `pur_chung_tu_tra_lai_hang_mua` — Dòng chi tiết chứng từ trả lại hàng mua |

---

## 1. `pur_chung_tu_tra_lai_hang_mua`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuTraLaiHangMua` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chung_tu_tra_lai_hang_mua` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chứng từ trả lại hàng mua |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `pur_phieu_xuat_kho_tra_lai_hang_mua` — FK `ON DELETE CASCADE` |
| Bảng con | `pur_phieu_xuat_kho_tra_lai_hang_mua` · `pur_chung_tu_tra_lai_hang_mua_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | Loại tiền (reference ENT_LoaiTien) `FK` |
| 3 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | Tỷ giá |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | Trạng thái (ChuaGhiSo \| DaGhiSo) |
| 5 | `ThuTienNgay` | `thu_tien_ngay` | `boolean` | N | `false` | **[Điều khiển nghiệp vụ]** Thu tiền ngay khi true, giảm trừ công nợ khi false |
| 6 | `HinhThucThanhToan` | `hinh_thuc_thanh_toan` | `text` CHECK | Y | — | **[Điều khiển nghiệp vụ]** Phương thức thanh toán (TienMat \| ChuyenKhoan) |
| 7 | `TraLaiHangTrongKho` | `tra_lai_hang_trong_kho` | `boolean` | N | `false` | **[Điều khiển nghiệp vụ]** Trả lại hàng đang trong kho. Quyết định có sinh phiếu xuất kho và có hiện cột kho, số lô, hạn sử dụng |
| 8 | `PhuongThucLapHoaDon` | `phuong_thuc_lap_hoa_don` | `text` CHECK | N | — | **[Điều khiển nghiệp vụ]** Phương thức lập hóa đơn (NguoiBanXuatHoaDonDieuChinh \| NguoiMuaXuatHoaDon \| KhongCoHoaDon) |
| 9 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | N | — | **[Nhà cung cấp]** Nhà cung cấp (reference ENT_DoiTuong, đối tượng có vai trò NhaCungCap) `FK` |
| 10 | `TenNhaCungCap` | `ten_nha_cung_cap` | `text` | N | — | **[Nhà cung cấp]** Tên nhà cung cấp |
| 11 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | **[Nhà cung cấp]** Mã số thuế nhà cung cấp |
| 12 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Nhà cung cấp]** Địa chỉ nhà cung cấp |
| 13 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | **[Nhà cung cấp]** Nhân viên mua hàng (reference ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |
| 14 | `PhieuXuatKhoTraLaiHangMuaId` | `phieu_xuat_kho_tra_lai_hang_mua_id` | `uuid` | Y | — | **[Chứng từ sinh kèm trong bộ]** Phiếu xuất kho sinh kèm (reference ENT_PhieuXuatKhoTraLaiHangMua) `FK` |
| 15 | `HoaDonDieuChinhId` | `hoa_don_dieu_chinh_id` | `uuid` | Y | — | **[Chứng từ sinh kèm trong bộ]** Hóa đơn điều chỉnh (reference ENT_HoaDonDieuChinh) `FK` |
| 16 | `HoaDonBanHangId` | `hoa_don_ban_hang_id` | `uuid` | Y | — | **[Chứng từ sinh kèm trong bộ]** Hóa đơn bán hàng sinh sang luồng Bán hàng (reference ENT_HoaDonBanHang) `FK` |
| 17 | `ChungTuThuTienId` | `chung_tu_thu_tien_id` | `uuid` | Y | — | **[Chứng từ sinh kèm trong bộ]** Phiếu thu hoặc giấy báo có sinh kèm (reference ENT_PhieuThu) `FK` |

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

**Đối chiếu `pur_chung_tu_tra_lai_hang_mua` (53 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 5 | `dien_giai`, `phieu_xuat_kho_tra_lai_hang_mua_id`, `hoa_don_dieu_chinh_id`, `hoa_don_ban_hang_id`, `chung_tu_thu_tien_id` |
| DB có — LDM **không khai** | 28 | `tai_khoan_tien_id`, `muc_dich_thu_chi_id`, `tai_khoan_nhan_id`, `ten_ngan_hang_nhan`, `phieu_thu_id`, `so_chung_tu_phieu_thu`, `nguoi_nhan`, `ma_so_dvqhns`, `cccd`, `ho_chieu`, `hinh_thuc_tt_hoa_don`, `tai_khoan_ngan_hang_id`, `ngay_hoa_don`, `mau_so_hoa_don`, `ky_hieu_hoa_don`, `so_hoa_don`, `ly_do_nop`, `nguoi_nhan_hang`, `mo_ta`, `chung_tu_mua_hang_id`, `tong_tien_hang_hoa`, `tong_tien_chiet_khau`, `tong_tien_thue_gtgt`, `tong_tien_thanh_toan`, `tong_tien_hang_hoa_quy_doi`, `tong_tien_chiet_khau_quy_doi`, `tong_tien_thue_gtgt_quy_doi`, `tong_tien_thanh_toan_quy_doi` |

---

## 2. `pur_phieu_xuat_kho_tra_lai_hang_mua`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuXuatKhoTraLaiHangMua` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu xuất kho của chứng từ trả lại hàng mua |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `pur_chung_tu_tra_lai_hang_mua` — FK `ON DELETE CASCADE` |
| Bảng con | `pur_chung_tu_tra_lai_hang_mua` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | Y | — | Loại tiền (reference ENT_LoaiTien) `FK` |
| 3 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | Tỷ giá |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | Trạng thái (ChuaGhiSo \| DaGhiSo) |
| 5 | `ChungTuTraLaiHangMuaId` | `chung_tu_tra_lai_hang_mua_id` | `uuid` | N | — | Chứng từ trả lại hàng mua (reference ENT_ChungTuTraLaiHangMua) `FK` |
| 6 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | N | — | Nhà cung cấp (reference ENT_DoiTuong, đối tượng có vai trò NhaCungCap) `FK` |
| 7 | `TenNhaCungCap` | `ten_nha_cung_cap` | `text` | N | — | Tên nhà cung cấp |
| 8 | `NguoiNhan` | `nguoi_nhan` | `text` | Y | — | Người nhận hàng trả lại. Tự điền theo người liên hệ của nhà cung cấp |
| 9 | `DiaChi` | `dia_chi` | `text` | Y | — | Địa chỉ nhà cung cấp |
| 10 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | Nhân viên mua hàng (reference ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |

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

## 3. `pur_chung_tu_tra_lai_hang_mua_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietChungTuTraLaiHangMua` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chi_tiet_chung_tu_tra_lai_hang_mua` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng chi tiết chứng từ trả lại hàng mua |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_chung_tu_tra_lai_hang_mua` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_chung_tu_tra_lai_hang_mua` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuTraLaiHangMuaId` | `chung_tu_tra_lai_hang_mua_id` | `uuid` | N | — | Chứng từ trả lại hàng mua (reference ENT_ChungTuTraLaiHangMua) `FK` |
| 2 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | Dòng hàng khi true, dòng ghi chú khi false |
| 3 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | Y | — | **[Chứng từ mua hàng gốc: chỉ có khi lập từ chứng từ gốc]** Chứng từ mua hàng gốc của dòng (reference ENT_ChungTuMuaHang) `FK` |
| 4 | `ChiTietChungTuMuaHangId` | `chi_tiet_chung_tu_mua_hang_id` | `uuid` | Y | — | **[Chứng từ mua hàng gốc: chỉ có khi lập từ chứng từ gốc]** Dòng hàng gốc trên chứng từ mua hàng (reference ENT_ChiTietChungTuMuaHang). Căn cứ tính số lượng đã trả lại `FK` |
| 5 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Hàng hóa]** Mã hàng (reference ENT_VatTu). Khóa sửa khi dòng lấy từ chứng từ gốc `FK` |
| 6 | `TenVatTu` | `ten_vat_tu` | `text` | Y | — | **[Hàng hóa]** Tên hàng. Tự điền theo mã hàng; là nội dung ghi chú khi LoaiDongHang = false |
| 7 | `LoaiVatTuId` | `loai_vat_tu_id` | `uuid` | Y | — | **[Hàng hóa]** Tính chất hàng hóa dịch vụ của mã hàng (reference ENT_LoaiVatTu) `FK` |
| 8 | `KhoId` | `kho_id` | `uuid` | Y | — | **[Hàng hóa]** Kho xuất trả lại (reference ENT_Kho) `FK` |
| 9 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Hàng hóa]** Đơn vị tính (reference ENT_DonViTinh) `FK` |
| 10 | `DonViTinhChinhId` | `don_vi_tinh_chinh_id` | `uuid` | Y | — | **[Hàng hóa]** Đơn vị tính chính của vật tư (reference ENT_DonViTinh) `FK` |
| 11 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | Y | `0` | **[Hàng hóa]** Hệ số quy đổi về đơn vị tính chính, lấy theo DonViQuyDoiVatTu.HeSoQuyDoi |
| 12 | `SoLuongTheoDVC` | `so_luong_theo_dvc` | `quantity` | Y | `0` | **[Hàng hóa]** Số lượng theo đơn vị tính chính, dùng quy số lượng đã trả lại về đơn vị tính của chứng từ gốc |
| 13 | `TaiKhoanNo` | `tai_khoan_no` | `uuid` | N | — | **[Tài khoản hạch toán]** Tài khoản công nợ phải trả (reference ENT_HeThongTaiKhoan) `FK` |
| 14 | `TaiKhoanCo` | `tai_khoan_co` | `uuid` | N | — | **[Tài khoản hạch toán]** Tài khoản kho khi trả lại hàng trong kho, tài khoản giá vốn khi không qua kho (reference ENT_HeThongTaiKhoan) `FK` |
| 15 | `SoLuong` | `so_luong` | `quantity` | Y | `0` | **[Số lượng và giá trị]** Số lượng trả lại |
| 16 | `DonGia` | `don_gia` | `money_foreign` ≈ | Y | `0` | **[Số lượng và giá trị]** Đơn giá, không âm |
| 17 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Số lượng và giá trị]** Thành tiền, bằng SoLuong nhân DonGia. Sửa tay thì tính ngược DonGia |
| 18 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Chiết khấu: màn này khai loại chiết khấu ở cấp dòng]** Loại chiết khấu của dòng (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon) |
| 19 | `ChietKhauPhanTram` | `chiet_khau_phan_tram` | `percent_rate` | Y | `0` | **[Chiết khấu: màn này khai loại chiết khấu ở cấp dòng]** Tỷ lệ chiết khấu, đơn vị phần trăm |
| 20 | `ChietKhau` | `chiet_khau` | `numeric(18,4)` ⚠ | Y | `0` | **[Chiết khấu: màn này khai loại chiết khấu ở cấp dòng]** Tiền chiết khấu |
| 21 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | **[Thuế GTGT: ẩn khi PhuongThucLapHoaDon = KhongCoHoaDon]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 22 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | Y | `0` | **[Thuế GTGT: ẩn khi PhuongThucLapHoaDon = KhongCoHoaDon]** Giá trị thuế suất GTGT thực tế, đơn vị phần trăm |
| 23 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Thuế GTGT: ẩn khi PhuongThucLapHoaDon = KhongCoHoaDon]** Tiền thuế GTGT, bằng ThanhTien trừ ChietKhau rồi nhân ThueSuatKhac chia 100 |
| 24 | `TaiKhoanThueGTGTId` | `tai_khoan_thue_gtgt_id` | `uuid` | Y | — | **[Thuế GTGT: ẩn khi PhuongThucLapHoaDon = KhongCoHoaDon]** Tài khoản thuế GTGT (reference ENT_HeThongTaiKhoan) `FK` |
| 25 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | **[Thuế GTGT: ẩn khi PhuongThucLapHoaDon = KhongCoHoaDon]** Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5). Trống khi người mua xuất hóa đơn |
| 26 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[Thuế GTGT: ẩn khi PhuongThucLapHoaDon = KhongCoHoaDon]** Diễn giải thuế |
| 27 | `KhongTongHopToKhaiGTGT` | `khong_tong_hop_to_khai_gtgt` | `boolean` | Y | `false` | **[Thuế GTGT: ẩn khi PhuongThucLapHoaDon = KhongCoHoaDon]** Hàng hóa không tổng hợp trên tờ khai thuế GTGT |
| 28 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | **[Thông tin bổ sung]** Số lô |
| 29 | `HanSuDung` | `han_su_dung` | `date` | Y | — | **[Thông tin bổ sung]** Hạn sử dụng |
| 30 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đơn vị (reference ENT_DonVi) `FK` |
| 31 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 32 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Vụ việc (reference ENT_CongTrinh) `FK` |
| 33 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đối tượng tập hợp chi phí (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 34 | `ChiPhiKhongHopLy` | `chi_phi_khong_hop_ly` | `boolean` | Y | `false` | **[Thông tin bổ sung]** Chi phí không hợp lý |

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

**Đối chiếu `pur_chi_tiet_chung_tu_tra_lai_hang_mua` (39 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 18 | `loai_dong_hang`, `vat_tu_id`, `ten_vat_tu`, `loai_vat_tu_id`, `don_vi_tinh_chinh_id`, `so_luong_theo_dvc`, `tai_khoan_no`, `tai_khoan_co`, `loai_chiet_khau`, `chiet_khau_phan_tram`, `thue_suat_khac`, `nhom_hhdv_mua_vao`, `dien_giai_thue`, `khong_tong_hop_to_khai_gtgt`, `khoan_muc_chi_phi_id`, `vu_viec_id`, `doi_tuong_tap_hop_chi_phi_id`, `chi_phi_khong_hop_ly` |
| DB có — LDM **không khai** | 13 | `tinh_chat_thue_gtgt_id`, `hang_hoa_id`, `ma_hang`, `ten_hang`, `loai_vat_tu`, `tai_khoan_no_id`, `tai_khoan_co_id`, `don_gia_quy_doi`, `thanh_tien_quy_doi`, `ty_le_chiet_khau`, `chiet_khau_quy_doi`, `tien_thue_gtgt_quy_doi`, `phien_ban` |

