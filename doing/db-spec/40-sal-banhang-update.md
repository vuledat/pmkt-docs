# `sal_` — Bán hàng

> Sinh tự động từ [`ldm-BanHang-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-BanHang-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**9 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> LDM BÁN HÀNG — BẢN DỰNG LẠI (thay thế ldm-BanHang.puml) Nguồn: 14700 Hợp đồng bán hàng · 14699 Đơn đặt hàng · 06194 Chứng từ bán hàng · 06195 Bán dịch vụ (gộp vào ChungTuBan) · 06196 Hóa đơn bán hàng. Phần điều chỉnh và trả lại (06197 Hóa đơn điều chỉnh, 07664 Điều chỉnh giá hàng bán, 06469 Trả lại hàng bán) do người khác phụ trách, không thuộc file này. Tên thuộc tính đặt lại theo nghiệp vụ, không dùng lại cột Field cũ.

**Epic nguồn:** PMKT-U-16693

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `HopDongBanHang` | `sal_hop_dong_ban_hang` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* (mục LDM: QUẢN TRỊ BÁN HÀNG) |
| 2 | `ChiTietHopDongBanHang` | `sal_hop_dong_ban_hang_chi_tiet` | — | C — tạo mới | Dòng chi tiết của `sal_hop_dong_ban_hang` — ⚠ *LDM chưa mô tả bảng này* |
| 3 | `DieuKhoanThanhToanHopDong` | `sal_dieu_khoan_thanh_toan_hop_dong` | — | C — tạo mới | Dòng chi tiết của `sal_hop_dong_ban_hang` — ⚠ *LDM chưa mô tả bảng này* |
| 4 | `DonDatHang` | `sal_don_dat_hang` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 5 | `ChiTietDonDatHang` | `sal_don_dat_hang_chi_tiet` | — | C — tạo mới | Dòng chi tiết của `sal_don_dat_hang` — ⚠ *LDM chưa mô tả bảng này* |
| 6 | `ChungTuBan` | `sal_chung_tu_ban_hang` | `sal_chung_tu_ban_hang` | A — có code | Đầu chứng từ — CHỨNG TỪ BÁN (gộp 06194 Chứng từ bán hàng + 06195 Bán dịch vụ: phân biệt bằng LoaiNghiepVu; dòng dịch vụ không dùng Kho/tồn kho) |
| 7 | `ChiTietChungTuBan` | `sal_chung_tu_ban_hang_chi_tiet` | `sal_chi_tiet_chung_tu_ban_hang` | A — có code | Dòng chi tiết của `sal_chung_tu_ban_hang` — ⚠ *LDM chưa mô tả bảng này* |
| 8 | `HoaDonBan` | `sal_hoa_don_ban_hang` | — | C — tạo mới | Đầu chứng từ — ⚠ *LDM chưa mô tả bảng này* |
| 9 | `ChiTietHoaDonBan` | `sal_hoa_don_ban_hang_chi_tiet` | `sal_chi_tiet_hd_ban_hang` | B — có schema, chưa code | Dòng chi tiết của `sal_hoa_don_ban_hang` — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `sal_hop_dong_ban_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HopDongBanHang` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | KHỐI 1 — QUẢN TRỊ BÁN HÀNG |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `sal_hop_dong_ban_hang_chi_tiet` · `sal_dieu_khoan_thanh_toan_hop_dong` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `SoHopDong` | `so_hop_dong` | `varchar(50)` | N | — | **[Thông tin chung hợp đồng]** Số hợp đồng (tự sinh, cho sửa, duy nhất theo Tenant) |
| 2 | `NgayKy` | `ngay_ky` | `date` | N | — | **[Thông tin chung hợp đồng]** Ngày ký hợp đồng |
| 3 | `KhachHangId` | `khach_hang_id` | `uuid` | N | — | **[Thông tin chung hợp đồng]** ID khách hàng (reference đến ENT_DoiTuong vai trò Khách hàng) `FK` |
| 4 | `TenKhachHang` | `ten_khach_hang` | `text` | N | — | **[Thông tin chung hợp đồng]** Tên khách hàng |
| 5 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Thông tin chung hợp đồng]** Địa chỉ khách hàng |
| 6 | `NguoiLienHe` | `nguoi_lien_he` | `text` | Y | — | **[Thông tin chung hợp đồng]** Người liên hệ phía khách hàng |
| 7 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ & giá trị]** Loại tiền của hợp đồng (reference đến ENT_LoaiTien) `FK` |
| 8 | `TyGia` | `ty_gia` | `exchange_rate` | N | `1` | **[Tiền tệ & giá trị]** Tỷ giá quy đổi về đồng hạch toán |
| 9 | `GiaTriHopDong` | `gia_tri_hop_dong` | `money_foreign` ≈ | N | `0` | **[Tiền tệ & giá trị]** Giá trị hợp đồng theo Loại tiền (hệ thống tính) |
| 10 | `GiaTriHopDongQuyDoi` | `gia_tri_hop_dong_quy_doi` | `money_vnd` | N | `0` | **[Tiền tệ & giá trị]** Giá trị hợp đồng quy đổi |
| 11 | `TinhTrangHopDong` | `tinh_trang_hop_dong` | `text` CHECK | N | — | **[Tình trạng & thời hạn]** Tình trạng hợp đồng (Chưa thực hiện, Đang thực hiện, Đã thanh lý, Hủy bỏ) |
| 12 | `TinhTrangGiaoHang` | `tinh_trang_giao_hang` | `text` CHECK | N | — | **[Tình trạng & thời hạn]** Tình trạng giao hàng (Chưa giao, Đang giao, Đã giao đủ) |
| 13 | `TinhTrangXuatHoaDon` | `tinh_trang_xuat_hoa_don` | `text` CHECK | Y | — | **[Tình trạng & thời hạn]** Tình trạng xuất hóa đơn (Chưa xuất hóa đơn, Đã xuất một phần, Đã xuất đủ hóa đơn — hệ thống tính, không lưu) |
| 14 | `HanGiaoHang` | `han_giao_hang` | `date` | Y | — | **[Tình trạng & thời hạn]** Hạn giao hàng |
| 15 | `HanThanhToan` | `han_thanh_toan` | `date` | Y | — | **[Tình trạng & thời hạn]** Hạn thanh toán |
| 16 | `TuDongChuyenDaThanhLy` | `tu_dong_chuyen_da_thanh_ly` | `boolean` | Y | `false` | **[Tình trạng & thời hạn]** Tự động chuyển tình trạng Đã thanh lý khi thu đủ và giao đủ |
| 17 | `TrichYeu` | `trich_yeu` | `text` | Y | — | **[Thông tin mở rộng]** Trích yếu nội dung hợp đồng |
| 18 | `DonViThucHienId` | `don_vi_thuc_hien_id` | `uuid` | Y | — | **[Thông tin mở rộng]** Đơn vị thực hiện (reference đến ENT_DonVi) `FK` |
| 19 | `NguoiThucHienId` | `nguoi_thuc_hien_id` | `uuid` | Y | — | **[Thông tin mở rộng]** Người thực hiện (reference đến ENT_DoiTuong vai trò Nhân viên) `FK` |
| 20 | `GiaTriThanhLy` | `gia_tri_thanh_ly` | `money_foreign` ≈ | N | `0` | **[Thông tin mở rộng]** Giá trị thanh lý |
| 21 | `GiaTriThanhLyQuyDoi` | `gia_tri_thanh_ly_quy_doi` | `money_vnd` | N | `0` | **[Thông tin mở rộng]** Giá trị thanh lý quy đổi |
| 22 | `NgayThanhLyHuyBo` | `ngay_thanh_ly_huy_bo` | `date` | Y | — | **[Thông tin mở rộng]** Ngày thanh lý hoặc hủy bỏ |
| 23 | `LyDoThanhLyHuyBo` | `ly_do_thanh_ly_huy_bo` | `text` | Y | — | **[Thông tin mở rộng]** Lý do thanh lý/hủy bỏ |
| 24 | `DieuKhoanKhac` | `dieu_khoan_khac` | `text` | Y | — | **[Thông tin mở rộng]** Điều khoản khác |
| 25 | `DiaChiGiaoHang` | `dia_chi_giao_hang` | `text` | Y | — | **[Thông tin mở rộng]** Địa chỉ giao hàng |
| 26 | `TinhGiaThanh` | `tinh_gia_thanh` | `boolean` | Y | `false` | **[Thông tin mở rộng]** Hợp đồng là đối tượng tập hợp chi phí tính giá thành |
| 27 | `DaXuatHoaDon` | `da_xuat_hoa_don` | `boolean` | Y | `false` | **[Thông tin mở rộng]** Chỉ báo đã có hóa đơn (hệ thống tính) |
| 28 | `LaHopDongPhatSinhTruoc` | `la_hop_dong_phat_sinh_truoc` | `boolean` | Y | `false` | **[Thông tin mở rộng]** Hợp đồng phát sinh trước khi dùng phần mềm |
| 29 | `SoDaThu` | `so_da_thu` | `money_foreign` ≈ | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là hợp đồng phát sinh trước)]** Số đã thu đầu kỳ |
| 30 | `SoDaThuQuyDoi` | `so_da_thu_quy_doi` | `money_vnd` | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là hợp đồng phát sinh trước)]** Số đã thu đầu kỳ quy đổi |
| 31 | `SoDaChi` | `so_da_chi` | `money_foreign` ≈ | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là hợp đồng phát sinh trước)]** Số đã chi đầu kỳ |
| 32 | `DoanhThu` | `doanh_thu` | `money_foreign` ≈ | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là hợp đồng phát sinh trước)]** Doanh thu đầu kỳ |
| 33 | `GiaVonBanHang` | `gia_von_ban_hang` | `money_foreign` ≈ | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là hợp đồng phát sinh trước)]** Giá vốn hàng bán đầu kỳ |
| 34 | `ChiPhiKhac` | `chi_phi_khac` | `money_foreign` ≈ | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là hợp đồng phát sinh trước)]** Chi phí khác đầu kỳ |
| 35 | `ThucThu` | `thuc_thu` | `money_foreign` ≈ | Y | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Thực thu nguyên tệ (hệ thống cộng dồn từ các kênh thu tiền) |
| 36 | `SoConPhaiThu` | `so_con_phai_thu` | `money_foreign` ≈ | Y | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Số còn phải thu (hệ thống tính) |
| 37 | `GiaTriDaXuatHoaDon` | `gia_tri_da_xuat_hoa_don` | `money_foreign` ≈ | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Giá trị đã xuất hóa đơn (hệ thống cộng dồn) |
| 38 | `GiaTriDaXuatHoaDonQuyDoi` | `gia_tri_da_xuat_hoa_don_quy_doi` | `money_vnd` | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Giá trị đã xuất hóa đơn quy đổi |
| 39 | `TongTienHangHoa` | `tong_tien_hang_hoa` | `money_foreign` ≈ | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Tổng tiền hàng |
| 40 | `TongTienChietKhau` | `tong_tien_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Tổng chiết khấu |
| 41 | `TongTienThueGTGT` | `tong_tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Tổng thuế GTGT |
| 42 | `TongTienHangHoaQuyDoi` | `tong_tien_hang_hoa_quy_doi` | `money_vnd` | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Tổng tiền hàng quy đổi |
| 43 | `TongTienChietKhauQuyDoi` | `tong_tien_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Tổng chiết khấu quy đổi |
| 44 | `TongTienThueGTGTQuyDoi` | `tong_tien_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Số liệu tổng hợp (hệ thống tính, không nhập)]** Tổng thuế GTGT quy đổi |

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

## 2. `sal_hop_dong_ban_hang_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietHopDongBanHang` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sal_hop_dong_ban_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sal_hop_dong_ban_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `HopDongBanHangId` | `hop_dong_ban_hang_id` | `uuid` | N | — | ID hợp đồng cha (reference đến ENT_HopDongBanHang) `FK` |
| 2 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Hàng hóa]** ID hàng hóa/dịch vụ (reference đến ENT_VatTu) `FK` |
| 3 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa]** Tên hàng hiển thị |
| 4 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Hàng hóa]** Đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 5 | `SoLuongYeuCau` | `so_luong_yeu_cau` | `quantity` | N | `0` | **[Số lượng & giá]** Số lượng cam kết theo hợp đồng |
| 6 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | **[Số lượng & giá]** Đơn giá theo Loại tiền |
| 7 | `DonGiaQuyDoi` | `don_gia_quy_doi` | `money_vnd` | N | `0` | **[Số lượng & giá]** Đơn giá quy đổi |
| 8 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Số lượng & giá]** Thành tiền dòng |
| 9 | `ThanhTienQuyDoi` | `thanh_tien_quy_doi` | `money_vnd` | N | `0` | **[Số lượng & giá]** Thành tiền quy đổi |
| 10 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu dòng (%) |
| 11 | `TienChietKhau` | `tien_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu dòng |
| 12 | `TienChietKhauQuyDoi` | `tien_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu quy đổi |
| 13 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | N | — | **[Thuế GTGT]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 14 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | N | `0` | **[Thuế GTGT]** % thuế tự nhập khi Thuế suất = KHAC |
| 15 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT |
| 16 | `TienThueGTGTQuyDoi` | `tien_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT quy đổi |
| 17 | `DonDatHangId` | `don_dat_hang_id` | `uuid` | Y | — | **[Liên kết nguồn & thống kê]** ID đơn đặt hàng nguồn của dòng (reference đến ENT_DonDatHang) `FK` |
| 18 | `ChiTietDonDatHangId` | `chi_tiet_don_dat_hang_id` | `uuid` | Y | — | **[Liên kết nguồn & thống kê]** ID dòng đơn đặt hàng nguồn (reference đến ENT_ChiTietDonDatHang) `FK` |
| 19 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Liên kết nguồn & thống kê]** Công trình/vụ việc (reference đến ENT_CongTrinh) `FK` |
| 20 | `SoLuongDaGiao` | `so_luong_da_giao` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã giao |
| 21 | `SoLuongDaGiaoNamTruoc` | `so_luong_da_giao_nam_truoc` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã giao các năm trước (nhập khi hợp đồng phát sinh trước) |
| 22 | `SoLuongDaBan` | `so_luong_da_ban` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã lập chứng từ bán |
| 23 | `SoLuongDaDatHang` | `so_luong_da_dat_hang` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã đưa vào đơn đặt hàng |
| 24 | `SoLuongTraLai` | `so_luong_tra_lai` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng trả lại (chỉ theo dõi) |

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

## 3. `sal_dieu_khoan_thanh_toan_hop_dong`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DieuKhoanThanhToanHopDong` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sal_hop_dong_ban_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sal_hop_dong_ban_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `HopDongBanHangId` | `hop_dong_ban_hang_id` | `uuid` | N | — | ID hợp đồng cha (reference đến ENT_HopDongBanHang) `FK` |
| 2 | `DotThanhToan` | `dot_thanh_toan` | `text` | N | — | **[Thông tin đợt thanh toán]** Tên/số thứ tự đợt thanh toán |
| 3 | `TyLeThanhToan` | `ty_le_thanh_toan` | `percent_rate` | N | `0` | **[Thông tin đợt thanh toán]** Tỷ lệ thanh toán của đợt (%) |
| 4 | `GiaTriThanhToan` | `gia_tri_thanh_toan` | `money_foreign` ≈ | N | `0` | **[Thông tin đợt thanh toán]** Giá trị phải thu của đợt |
| 5 | `HanThanhToan` | `han_thanh_toan` | `date` | Y | — | **[Thông tin đợt thanh toán]** Hạn thanh toán của đợt |
| 6 | `NgayThanhToan` | `ngay_thanh_toan` | `date` | Y | — | **[Thông tin đợt thanh toán]** Ngày thực thu của đợt (hệ thống tính) |
| 7 | `SoDaThu` | `so_da_thu` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp thu tiền (hệ thống tính; liên kết mềm tới chứng từ thu tiền)]** Số đã thu của đợt (hệ thống cộng dồn, nguyên tệ) |
| 8 | `SoDaThuNamTruoc` | `so_da_thu_nam_truoc` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp thu tiền (hệ thống tính; liên kết mềm tới chứng từ thu tiền)]** Số đã thu các năm trước (nhập khi hợp đồng phát sinh trước) |
| 9 | `SoConPhaiThu` | `so_con_phai_thu` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp thu tiền (hệ thống tính; liên kết mềm tới chứng từ thu tiền)]** Số còn phải thu của đợt (hệ thống tính) |
| 10 | `DanhSachChungTuThuTien` | `danh_sach_chung_tu_thu_tien` | `text` | Y | — | **[Tổng hợp thu tiền (hệ thống tính; liên kết mềm tới chứng từ thu tiền)]** Danh sách số chứng từ thu tiền gán vào đợt, ngăn cách dấu ";" |

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

## 4. `sal_don_dat_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DonDatHang` |
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
| Bảng con | `sal_don_dat_hang_chi_tiet` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `SoDonHang` | `so_don_hang` | `varchar(50)` | N | — | **[Thông tin chung đơn hàng]** Số đơn hàng (tự sinh, cho sửa, duy nhất theo Tenant) |
| 2 | `NgayDonHang` | `ngay_don_hang` | `date` | N | — | **[Thông tin chung đơn hàng]** Ngày đơn hàng |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin chung đơn hàng]** Diễn giải đơn hàng |
| 4 | `NhanVienBanHangId` | `nhan_vien_ban_hang_id` | `uuid` | Y | — | **[Thông tin chung đơn hàng]** Nhân viên bán hàng (reference đến ENT_DoiTuong vai trò Nhân viên) `FK` |
| 5 | `KhachHangId` | `khach_hang_id` | `uuid` | N | — | **[Khách hàng]** ID khách hàng (reference đến ENT_DoiTuong vai trò Khách hàng) `FK` |
| 6 | `TenKhachHang` | `ten_khach_hang` | `text` | N | — | **[Khách hàng]** Tên khách hàng |
| 7 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | **[Khách hàng]** Mã số thuế khách hàng |
| 8 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Khách hàng]** Địa chỉ khách hàng |
| 9 | `NguoiNhanHang` | `nguoi_nhan_hang` | `text` | Y | — | **[Khách hàng]** Người nhận hàng |
| 10 | `DieuKhoanThanhToanId` | `dieu_khoan_thanh_toan_id` | `uuid` | Y | — | **[Thanh toán & tình trạng]** Điều khoản thanh toán (reference đến ENT_DieuKhoanThanhToan) `FK` |
| 11 | `SoNgayDuocNo` | `so_ngay_duoc_no` | `integer` | Y | `0` | **[Thanh toán & tình trạng]** Số ngày được nợ |
| 12 | `HanGiaoHang` | `han_giao_hang` | `date` | Y | — | **[Thanh toán & tình trạng]** Hạn giao hàng |
| 13 | `TinhTrangDonHang` | `tinh_trang_don_hang` | `text` CHECK | N | — | **[Thanh toán & tình trạng]** Tình trạng đơn hàng (Chưa thực hiện, Đang thực hiện, Hoàn thành, Đã hủy) |
| 14 | `TinhTrangGiaoHang` | `tinh_trang_giao_hang` | `text` CHECK | N | — | **[Thanh toán & tình trạng]** Tình trạng giao hàng (Chưa giao, Đang giao, Đã giao đủ) |
| 15 | `TinhTrangXuatHoaDon` | `tinh_trang_xuat_hoa_don` | `text` CHECK | Y | — | **[Thanh toán & tình trạng]** Tình trạng xuất hóa đơn (Chưa xuất hóa đơn, Đã xuất một phần, Đã xuất đủ hóa đơn — hệ thống tính, không lưu) |
| 16 | `TinhGiaThanh` | `tinh_gia_thanh` | `boolean` | Y | `false` | **[Thanh toán & tình trạng]** Đơn hàng là đối tượng tập hợp chi phí tính giá thành |
| 17 | `LaDonHangPhatSinhTruoc` | `la_don_hang_phat_sinh_truoc` | `boolean` | Y | `false` | **[Thanh toán & tình trạng]** Đơn đặt hàng phát sinh trước khi dùng phần mềm |
| 18 | `DaGuiEmail` | `da_gui_email` | `boolean` | Y | `false` | **[Thanh toán & tình trạng]** Đã gửi email đơn hàng cho khách |
| 19 | `NgayGuiEmailGanNhat` | `ngay_gui_email_gan_nhat` | `timestamptz` | Y | — | **[Thanh toán & tình trạng]** Ngày gửi email gần nhất |
| 20 | `SoHopDong` | `so_hop_dong` | `varchar(50)` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Số hợp đồng (nhập tự do; liên kết hợp đồng nguồn ở cấp dòng — một đơn lập được từ nhiều hợp đồng) |
| 21 | `NgayHopDong` | `ngay_hop_dong` | `date` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Ngày hợp đồng |
| 22 | `DiaDiemGiao` | `dia_diem_giao` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Địa điểm giao hàng |
| 23 | `DiaDiemNhan` | `dia_diem_nhan` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Địa điểm nhận hàng |
| 24 | `SoVanDon` | `so_van_don` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Số vận đơn |
| 25 | `SoContainer` | `so_container` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Số container |
| 26 | `DonViVanChuyen` | `don_vi_van_chuyen` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Đơn vị vận chuyển |
| 27 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ & chiết khấu]** Loại tiền (reference đến ENT_LoaiTien) `FK` |
| 28 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Tiền tệ & chiết khấu]** Tỷ giá quy đổi |
| 29 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Tiền tệ & chiết khấu]** Loại chiết khấu (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon \| TheoMatHangVaHoaDon) |
| 30 | `TyLeChietKhauChung` | `ty_le_chiet_khau_chung` | `percent_rate` | Y | `0` | **[Tiền tệ & chiết khấu]** % chiết khấu trên tổng hóa đơn (khi Loại chiết khấu = Theo % hóa đơn) |
| 31 | `TienChietKhauChung` | `tien_chiet_khau_chung` | `money_foreign` ≈ | N | `0` | **[Tiền tệ & chiết khấu]** Tiền chiết khấu trên tổng hóa đơn (khi Loại chiết khấu = Theo số tiền trên tổng hóa đơn) |
| 32 | `SoDaThu` | `so_da_thu` | `money_foreign` ≈ | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là đơn hàng phát sinh trước)]** Số đã thu đầu kỳ |
| 33 | `SoDaThuQuyDoi` | `so_da_thu_quy_doi` | `money_vnd` | Y | `0` | **[Số dư đầu kỳ (chỉ nhập khi Là đơn hàng phát sinh trước)]** Số đã thu đầu kỳ quy đổi |
| 34 | `TongTienHang` | `tong_tien_hang` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng tiền hàng |
| 35 | `TongChietKhau` | `tong_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng chiết khấu |
| 36 | `TongChietKhauTheoHang` | `tong_chiet_khau_theo_hang` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng chiết khấu theo mặt hàng |
| 37 | `TongChietKhauTheoHoaDon` | `tong_chiet_khau_theo_hoa_don` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng chiết khấu phân bổ theo hóa đơn |
| 38 | `TongThueGTGT` | `tong_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng thuế GTGT |
| 39 | `TongThanhToan` | `tong_thanh_toan` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng thanh toán |
| 40 | `TongTienHangQuyDoi` | `tong_tien_hang_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng tiền hàng quy đổi |
| 41 | `TongChietKhauQuyDoi` | `tong_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng chiết khấu quy đổi |
| 42 | `TongChietKhauTheoHangQuyDoi` | `tong_chiet_khau_theo_hang_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng chiết khấu theo mặt hàng quy đổi |
| 43 | `TongChietKhauTheoHoaDonQuyDoi` | `tong_chiet_khau_theo_hoa_don_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng chiết khấu theo hóa đơn quy đổi |
| 44 | `TongThueGTGTQuyDoi` | `tong_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng thuế GTGT quy đổi |
| 45 | `TongThanhToanQuyDoi` | `tong_thanh_toan_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết, lưu trên đơn)]** Tổng thanh toán quy đổi |

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

## 5. `sal_don_dat_hang_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDonDatHang` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sal_don_dat_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sal_don_dat_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DonDatHangId` | `don_dat_hang_id` | `uuid` | N | — | ID đơn hàng cha (reference đến ENT_DonDatHang) `FK` |
| 2 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Hàng hóa & kho]** ID hàng hóa/dịch vụ (reference đến ENT_VatTu) `FK` |
| 3 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa & kho]** Tên hàng hiển thị |
| 4 | `KhoId` | `kho_id` | `uuid` | Y | — | **[Hàng hóa & kho]** Kho dự kiến xuất (reference đến ENT_Kho; NULL với dòng dịch vụ) `FK` |
| 5 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Hàng hóa & kho]** Đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 6 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Số lượng & giá]** Số lượng đặt |
| 7 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | **[Số lượng & giá]** Đơn giá theo Loại tiền |
| 8 | `DonGiaQuyDoi` | `don_gia_quy_doi` | `money_vnd` | N | `0` | **[Số lượng & giá]** Đơn giá quy đổi |
| 9 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Số lượng & giá]** Thành tiền dòng hàng |
| 10 | `ThanhTienQuyDoi` | `thanh_tien_quy_doi` | `money_vnd` | N | `0` | **[Số lượng & giá]** Thành tiền quy đổi |
| 11 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu dòng (%) |
| 12 | `TienChietKhau` | `tien_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu dòng |
| 13 | `TienChietKhauQuyDoi` | `tien_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu quy đổi |
| 14 | `TyLeChietKhauTheoHang` | `ty_le_chiet_khau_theo_hang` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu theo mặt hàng (%) |
| 15 | `TienChietKhauTheoHang` | `tien_chiet_khau_theo_hang` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo mặt hàng |
| 16 | `TienChietKhauTheoHangQuyDoi` | `tien_chiet_khau_theo_hang_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo mặt hàng quy đổi |
| 17 | `TyLeChietKhauTheoHoaDon` | `ty_le_chiet_khau_theo_hoa_don` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu phân bổ theo hóa đơn (%) |
| 18 | `TienChietKhauTheoHoaDon` | `tien_chiet_khau_theo_hoa_don` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu phân bổ theo hóa đơn |
| 19 | `TienChietKhauTheoHoaDonQuyDoi` | `tien_chiet_khau_theo_hoa_don_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo hóa đơn quy đổi |
| 20 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | N | — | **[Thuế GTGT]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 21 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | N | `0` | **[Thuế GTGT]** % thuế tự nhập khi Thuế suất = KHAC |
| 22 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT |
| 23 | `TienThueGTGTQuyDoi` | `tien_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT quy đổi |
| 24 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | **[Theo dõi lô]** Số lô |
| 25 | `HanSuDung` | `han_su_dung` | `date` | Y | — | **[Theo dõi lô]** Hạn sử dụng |
| 26 | `HopDongBanHangId` | `hop_dong_ban_hang_id` | `uuid` | Y | — | **[Liên kết nguồn (dòng hợp đồng kế thừa)]** ID hợp đồng bán hàng nguồn (reference đến ENT_HopDongBanHang) `FK` |
| 27 | `ChiTietHopDongBanHangId` | `chi_tiet_hop_dong_ban_hang_id` | `uuid` | Y | — | **[Liên kết nguồn (dòng hợp đồng kế thừa)]** ID dòng hợp đồng nguồn (reference đến ENT_ChiTietHopDongBanHang) `FK` |
| 28 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đơn vị (reference đến ENT_DonVi) `FK` |
| 29 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Vụ việc/công trình (reference đến ENT_CongTrinh) `FK` |
| 30 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 31 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Hợp đồng thống kê chi phí (reference đến ENT_HopDongBanHang; khác liên kết hợp đồng nguồn ở nhóm trên) `FK` |
| 32 | `SoLuongDaBan` | `so_luong_da_ban` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã lập chứng từ bán |
| 33 | `SoLuongDaXuat` | `so_luong_da_xuat` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã xuất kho |
| 34 | `SoLuongDaDuaVaoHopDong` | `so_luong_da_dua_vao_hop_dong` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã đưa vào hợp đồng bán hàng |
| 35 | `SoLuongTraLai` | `so_luong_tra_lai` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng trả lại (chỉ theo dõi) |

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

## 6. `sal_chung_tu_ban_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuBan` |
| Base class | `BaseChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `sal_chung_tu_ban_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | KHỐI 2 — CHỨNG TỪ BÁN (gộp 06194 Chứng từ bán hàng + 06195 Bán dịch vụ: · phân biệt bằng LoaiNghiepVu; dòng dịch vụ không dùng Kho/tồn kho) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `sal_chung_tu_ban_hang_chi_tiet` · `sal_hoa_don_ban_hang` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiNghiepVu` | `loai_nghiep_vu` | `text` CHECK | N | — | **[Tùy chọn nghiệp vụ (header options)]** Loại nghiệp vụ (Bán hàng trong nước, Bán hàng xuất khẩu, Bán dịch vụ — bán dịch vụ không dùng kho/xuất hàng) |
| 2 | `KiemPhieuXuatKho` | `kiem_phieu_xuat_kho` | `boolean` | Y | `false` | **[Tùy chọn nghiệp vụ (header options)]** Lập kiêm phiếu xuất kho (sinh phiếu xuất kho liên kết bên phân hệ Kho; không dùng với bán dịch vụ) |
| 3 | `LapKemHoaDon` | `lap_kem_hoa_don` | `boolean` | Y | `false` | **[Tùy chọn nghiệp vụ (header options)]** Lập kèm hóa đơn (sinh ENT_HoaDonBan liên kết) |
| 4 | `ThuTienNgay` | `thu_tien_ngay` | `boolean` | Y | `false` | **[Tùy chọn nghiệp vụ (header options)]** Thu tiền ngay (sinh phiếu thu/giấy báo có liên kết bên phân hệ Tiền) |
| 5 | `HinhThucThanhToan` | `hinh_thuc_thanh_toan` | `text` CHECK | Y | — | **[Tùy chọn nghiệp vụ (header options)]** Hình thức thanh toán khi thu tiền ngay (Tiền mặt, Chuyển khoản) |
| 6 | `KhachHangId` | `khach_hang_id` | `uuid` | N | — | **[Khách hàng]** ID khách hàng (reference đến ENT_DoiTuong vai trò Khách hàng) `FK` |
| 7 | `TenKhachHang` | `ten_khach_hang` | `text` | Y | — | **[Khách hàng]** Tên khách hàng |
| 8 | `MaSoThueCCCD` | `ma_so_thue_cccd` | `text` | Y | — | **[Khách hàng]** Mã số thuế hoặc CCCD chủ hộ |
| 9 | `NguoiLienHe` | `nguoi_lien_he` | `text` | Y | — | **[Khách hàng]** Người liên hệ |
| 10 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Khách hàng]** Địa chỉ khách hàng |
| 11 | `NhanVienBanHangId` | `nhan_vien_ban_hang_id` | `uuid` | Y | — | **[Khách hàng]** Nhân viên bán hàng (reference đến ENT_DoiTuong vai trò Nhân viên) `FK` |
| 12 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin chứng từ]** Diễn giải chứng từ |
| 13 | `DieuKhoanThanhToanId` | `dieu_khoan_thanh_toan_id` | `uuid` | Y | — | **[Thông tin chứng từ]** Điều khoản thanh toán (reference đến ENT_DieuKhoanThanhToan) `FK` |
| 14 | `SoNgayDuocNo` | `so_ngay_duoc_no` | `integer` | Y | `0` | **[Thông tin chứng từ]** Số ngày được nợ |
| 15 | `HanThanhToan` | `han_thanh_toan` | `date` | Y | — | **[Thông tin chứng từ]** Hạn thanh toán (hệ thống tính) |
| 16 | `DaLapHoaDon` | `da_lap_hoa_don` | `boolean` | Y | `false` | **[Thông tin chứng từ]** Đã lập hóa đơn cho chứng từ |
| 17 | `SoHopDong` | `so_hop_dong` | `varchar(50)` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Số hợp đồng (nhập tự do) |
| 18 | `NgayHopDong` | `ngay_hop_dong` | `date` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Ngày hợp đồng |
| 19 | `DiaDiemGiao` | `dia_diem_giao` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Địa điểm giao hàng (chọn từ ENT_DiaChiGiaoHang hoặc nhập tự do, lưu dạng text) |
| 20 | `DiaDiemNhan` | `dia_diem_nhan` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Địa điểm nhận hàng |
| 21 | `SoVanDon` | `so_van_don` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Số vận đơn |
| 22 | `SoContainer` | `so_container` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Số container |
| 23 | `DonViVanChuyen` | `don_vi_van_chuyen` | `text` | Y | — | **[Thông tin bổ sung (hợp đồng, giao nhận, vận chuyển)]** Đơn vị vận chuyển |
| 24 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ & chiết khấu]** Loại tiền (reference đến ENT_LoaiTien) `FK` |
| 25 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Tiền tệ & chiết khấu]** Tỷ giá quy đổi |
| 26 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Tiền tệ & chiết khấu]** Loại chiết khấu (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon \| TheoMatHangVaHoaDon) |
| 27 | `TyLeChietKhauChung` | `ty_le_chiet_khau_chung` | `percent_rate` | Y | `0` | **[Tiền tệ & chiết khấu]** % chiết khấu trên tổng hóa đơn (khi Loại chiết khấu = Theo % hóa đơn) |
| 28 | `TongTienHang` | `tong_tien_hang` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng tiền hàng |
| 29 | `TongChietKhau` | `tong_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu |
| 30 | `TongChietKhauTheoHang` | `tong_chiet_khau_theo_hang` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu theo mặt hàng |
| 31 | `TongChietKhauTheoHoaDon` | `tong_chiet_khau_theo_hoa_don` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu phân bổ theo hóa đơn |
| 32 | `TongThueGTGT` | `tong_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế GTGT |
| 33 | `TongThueXK` | `tong_thue_xk` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế xuất khẩu (nghiệp vụ xuất khẩu) |
| 34 | `TongThanhToan` | `tong_thanh_toan` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thanh toán |
| 35 | `TongTienHangQuyDoi` | `tong_tien_hang_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng tiền hàng quy đổi |
| 36 | `TongChietKhauQuyDoi` | `tong_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu quy đổi |
| 37 | `TongChietKhauTheoHangQuyDoi` | `tong_chiet_khau_theo_hang_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu theo mặt hàng quy đổi |
| 38 | `TongChietKhauTheoHoaDonQuyDoi` | `tong_chiet_khau_theo_hoa_don_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu theo hóa đơn quy đổi |
| 39 | `TongThueGTGTQuyDoi` | `tong_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế GTGT quy đổi |
| 40 | `TongThueXKQuyDoi` | `tong_thue_xk_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế xuất khẩu quy đổi |
| 41 | `TongThanhToanQuyDoi` | `tong_thanh_toan_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thanh toán quy đổi |
| 42 | `SoChungTuXuatKho` | `so_chung_tu_xuat_kho` | `text` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuXuatKho; dữ liệu kho lấy trực tiếp từ ChiTietChungTuBan)]** Số chứng từ của phần xuất kho (cấp theo quy tắc đánh số loại chứng từ Xuất kho) |
| 43 | `NgayChungTuXuatKho` | `ngay_chung_tu_xuat_kho` | `date` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuXuatKho; dữ liệu kho lấy trực tiếp từ ChiTietChungTuBan)]** Ngày chứng từ của phần xuất kho |
| 44 | `NguoiNhanHang` | `nguoi_nhan_hang` | `text` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuXuatKho; dữ liệu kho lấy trực tiếp từ ChiTietChungTuBan)]** Người nhận hàng |
| 45 | `SoChungTuThuTien` | `so_chung_tu_thu_tien` | `text` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuThu)]** Số chứng từ của phần thu tiền (cấp theo quy tắc đánh số loại chứng từ Thu tiền mặt / Thu tiền gửi) |
| 46 | `NgayChungTuThuTien` | `ngay_chung_tu_thu_tien` | `date` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuThu)]** Ngày chứng từ của phần thu tiền |
| 47 | `NguoiNopTien` | `nguoi_nop_tien` | `text` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuThu)]** Người nộp tiền |
| 48 | `LyDoThu` | `ly_do_thu` | `text` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuThu)]** Lý do thu |
| 49 | `TaiKhoanTienId` | `tai_khoan_tien_id` | `uuid` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuThu)]** TK tiền ghi Nợ khi thu (reference đến ENT_HeThongTaiKhoan; 111x khi Tiền mặt, 112x khi Chuyển khoản) `FK` |
| 50 | `TaiKhoanNhanId` | `tai_khoan_nhan_id` | `uuid` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuThu)]** Tài khoản ngân hàng nhận tiền của đơn vị (reference đến ENT_TaiKhoanNganHang; chỉ khi Chuyển khoản) `FK` |
| 51 | `TenNganHangNhan` | `ten_ngan_hang_nhan` | `text` | Y | — | **[KHÔNG sinh bản ghi ENT_PhieuThu)]** Tên ngân hàng nhận (denormalized theo TaiKhoanNhanId) |
| 52 | `SoTienDaThanhToan` | `so_tien_da_thanh_toan` | `money_foreign` ≈ | N | `0` | **[Số liệu thu tiền (hệ thống cộng từ chứng từ thu gắn với chứng từ bán)]** Số tiền đã thu (hệ thống cộng dồn từ chứng từ thu tiền và bút toán đối trừ công nợ) |
| 53 | `SoTienDaThanhToanQuyDoi` | `so_tien_da_thanh_toan_quy_doi` | `money_vnd` | N | `0` | **[Số liệu thu tiền (hệ thống cộng từ chứng từ thu gắn với chứng từ bán)]** Số tiền đã thu quy đổi |
| 54 | `TrangThaiGhiSo` | `trang_thai_ghi_so` | `text` CHECK | N | — | **[Trạng thái]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |
| 55 | `TrangThaiLapHoaDon` | `trang_thai_lap_hoa_don` | `text` CHECK | Y | — | **[Trạng thái]** Trạng thái lập hóa đơn (ChuaLap \| DaLapMotPhan \| DaLapDu — hệ thống tính) |
| 56 | `TrangThaiThanhToan` | `trang_thai_thanh_toan` | `text` CHECK | Y | — | **[Trạng thái]** Trạng thái thanh toán (ChuaThanhToan \| DaThanhToanMotPhan \| DaThanhToan) |
| 57 | `TrangThaiXuatHang` | `trang_thai_xuat_hang` | `text` CHECK | Y | — | **[Trạng thái]** Trạng thái xuất hàng (ChuaXuatHang \| DaXuatMotPhan \| DaXuatDu — hệ thống tính; NULL với bán dịch vụ) |

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

**Đối chiếu `sal_chung_tu_ban_hang` (75 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 28 | `ma_so_thue_cccd`, `dien_giai`, `ty_le_chiet_khau_chung`, `tong_tien_hang`, `tong_chiet_khau`, `tong_chiet_khau_theo_hang`, `tong_chiet_khau_theo_hoa_don`, `tong_thue_gtgt`, `tong_thue_xk`, `tong_thanh_toan`, `tong_tien_hang_quy_doi`, `tong_chiet_khau_quy_doi`, `tong_chiet_khau_theo_hang_quy_doi`, `tong_chiet_khau_theo_hoa_don_quy_doi`, `tong_thue_gtgt_quy_doi`, `tong_thue_xk_quy_doi`, `tong_thanh_toan_quy_doi`, `so_chung_tu_xuat_kho`, `ngay_chung_tu_xuat_kho`, `nguoi_nhan_hang`, `so_chung_tu_thu_tien`, `ngay_chung_tu_thu_tien`, `nguoi_nop_tien`, `ly_do_thu`, `tai_khoan_nhan_id`, `ten_ngan_hang_nhan`, `trang_thai_ghi_so`, `trang_thai_lap_hoa_don` |
| DB có — LDM **không khai** | 32 | `nguoi_mua_hang`, `ma_so_dvqhns`, `cccd`, `ho_chieu`, `gia_tri_chiet_khau`, `tong_tien_chiet_khau_hang`, `tong_tien_chiet_khau_hang_quy_doi`, `tong_tien_chiet_khau_hoa_don`, `tong_tien_chiet_khau_hoa_don_quy_doi`, `so_dien_thoai`, `ma_so_thue`, `mo_ta`, `phieu_xuat_kho_id`, `nguoi_nhan`, `phieu_thu_id`, `mieu_ta_phieu_thu`, `nguoi_nop`, `tai_khoan_ngan_hang_thu_id`, `tong_tien_hang_hoa`, `tong_tien_chiet_khau`, `tong_tien_thue_gtgt`, `tong_tien_sau_thue`, `tong_tien_thanh_toan`, `tong_tien_hang_hoa_quy_doi`, `tong_tien_chiet_khau_quy_doi`, `tong_tien_thue_gtgt_quy_doi`, `tong_tien_sau_thue_quy_doi`, `tong_tien_thanh_toan_quy_doi`, `trang_thai_chung_tu`, `trang_thai_hoa_don`, `la_giao_dich_noi_bo_tap_doan`, `doi_tac_tenant_id` |

---

## 7. `sal_chung_tu_ban_hang_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietChungTuBan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `sal_chi_tiet_chung_tu_ban_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sal_chung_tu_ban_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sal_chung_tu_ban_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuBanId` | `chung_tu_ban_id` | `uuid` | N | — | ID chứng từ cha (reference đến ENT_ChungTuBan) `FK` |
| 2 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | **[Phân loại dòng]** Loại dòng: True = dòng hàng, False = dòng ghi chú (chỉ nhập Tên hàng, không tham gia tính toán). Hàng hóa hay Dịch vụ suy từ VatTu.LoaiVatTu, không lưu ở đây |
| 3 | `LaChietKhauThuongMai` | `la_chiet_khau_thuong_mai` | `boolean` | Y | `false` | **[Phân loại dòng]** Dòng là chiết khấu thương mại |
| 4 | `LaHangKhuyenMai` | `la_hang_khuyen_mai` | `boolean` | Y | `false` | **[Phân loại dòng]** Dòng là hàng khuyến mại, không doanh thu |
| 5 | `VatTuId` | `vat_tu_id` | `uuid` | Y | — | **[Hàng hóa, kho & tài khoản doanh thu]** ID hàng hóa/dịch vụ (reference đến ENT_VatTu) `FK` |
| 6 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa, kho & tài khoản doanh thu]** Tên hàng hiển thị |
| 7 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hàng hóa, kho & tài khoản doanh thu]** Diễn giải dòng |
| 8 | `KhoId` | `kho_id` | `uuid` | Y | — | **[Hàng hóa, kho & tài khoản doanh thu]** Kho xuất (reference đến ENT_Kho; NULL với dòng dịch vụ) `FK` |
| 9 | `TaiKhoanCongNoId` | `tai_khoan_cong_no_id` | `uuid` | Y | — | **[Hàng hóa, kho & tài khoản doanh thu]** TK công nợ của dòng (reference đến ENT_HeThongTaiKhoan) `FK` |
| 10 | `TaiKhoanDoanhThuId` | `tai_khoan_doanh_thu_id` | `uuid` | Y | — | **[Hàng hóa, kho & tài khoản doanh thu]** TK doanh thu của dòng (reference đến ENT_HeThongTaiKhoan) `FK` |
| 11 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | Y | — | **[Đơn vị tính & số lượng (các cột quy đổi ĐVT là giá trị tính khi hiển thị, không lưu)]** Đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 12 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Đơn vị tính & số lượng (các cột quy đổi ĐVT là giá trị tính khi hiển thị, không lưu)]** Số lượng theo ĐVT chọn |
| 13 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | **[Đơn giá & thành tiền]** Đơn giá theo Loại tiền |
| 14 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Đơn giá & thành tiền]** Thành tiền dòng |
| 15 | `ThanhTienQuyDoi` | `thanh_tien_quy_doi` | `money_vnd` | N | `0` | **[Đơn giá & thành tiền]** Thành tiền quy đổi |
| 16 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu dòng (%) |
| 17 | `TienChietKhau` | `tien_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu dòng |
| 18 | `TienChietKhauQuyDoi` | `tien_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu quy đổi |
| 19 | `TyLeChietKhauTheoHang` | `ty_le_chiet_khau_theo_hang` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu theo mặt hàng (%) |
| 20 | `TienChietKhauTheoHang` | `tien_chiet_khau_theo_hang` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo mặt hàng |
| 21 | `TienChietKhauTheoHangQuyDoi` | `tien_chiet_khau_theo_hang_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo mặt hàng quy đổi |
| 22 | `TyLeChietKhauTheoHoaDon` | `ty_le_chiet_khau_theo_hoa_don` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu phân bổ theo hóa đơn (%) |
| 23 | `TienChietKhauTheoHoaDon` | `tien_chiet_khau_theo_hoa_don` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu phân bổ theo hóa đơn |
| 24 | `TienChietKhauTheoHoaDonQuyDoi` | `tien_chiet_khau_theo_hoa_don_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo hóa đơn quy đổi |
| 25 | `TaiKhoanChietKhauId` | `tai_khoan_chiet_khau_id` | `uuid` | Y | — | **[Chiết khấu]** TK chiết khấu (reference đến ENT_HeThongTaiKhoan) `FK` |
| 26 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | **[Thuế GTGT]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC; nghiệp vụ xuất khẩu chỉ 0 và KCT) |
| 27 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | N | `0` | **[Thuế GTGT]** % thuế tự nhập khi Thuế suất = KHAC |
| 28 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT |
| 29 | `TienThueGTGTQuyDoi` | `tien_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT quy đổi |
| 30 | `TaiKhoanThueGTGTId` | `tai_khoan_thue_gtgt_id` | `uuid` | Y | — | **[Thuế GTGT]** TK thuế GTGT (reference đến ENT_HeThongTaiKhoan) `FK` |
| 31 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[Thuế GTGT]** Diễn giải thuế |
| 32 | `KhongTongHopToKhaiGTGT` | `khong_tong_hop_to_khai_gtgt` | `boolean` | Y | `false` | **[Thuế GTGT]** Hàng hóa không tổng hợp lên tờ khai thuế GTGT |
| 33 | `TuNhapDonGiaVon` | `tu_nhap_don_gia_von` | `boolean` | Y | `false` | **[Giá vốn & xuất kho (chỉ dùng khi Kiêm phiếu xuất kho)]** Người dùng tự nhập đơn giá vốn thay vì hệ thống tính |
| 34 | `DonGiaVon` | `don_gia_von` | `money_foreign` ≈ | N | `0` | **[Giá vốn & xuất kho (chỉ dùng khi Kiêm phiếu xuất kho)]** Đơn giá vốn |
| 35 | `TienVon` | `tien_von` | `money_foreign` ≈ | N | `0` | **[Giá vốn & xuất kho (chỉ dùng khi Kiêm phiếu xuất kho)]** Tiền vốn |
| 36 | `TaiKhoanGiaVonId` | `tai_khoan_gia_von_id` | `uuid` | Y | — | **[Giá vốn & xuất kho (chỉ dùng khi Kiêm phiếu xuất kho)]** TK giá vốn (reference đến ENT_HeThongTaiKhoan) `FK` |
| 37 | `TaiKhoanKhoId` | `tai_khoan_kho_id` | `uuid` | Y | — | **[Giá vốn & xuất kho (chỉ dùng khi Kiêm phiếu xuất kho)]** TK kho (reference đến ENT_HeThongTaiKhoan) `FK` |
| 38 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | **[Giá vốn & xuất kho (chỉ dùng khi Kiêm phiếu xuất kho)]** Số lô |
| 39 | `HanSuDung` | `han_su_dung` | `date` | Y | — | **[Giá vốn & xuất kho (chỉ dùng khi Kiêm phiếu xuất kho)]** Hạn sử dụng |
| 40 | `GiaTriTinhThueXK` | `gia_tri_tinh_thue_xk` | `money_foreign` ≈ | N | `0` | **[Thuế xuất khẩu (nghiệp vụ xuất khẩu)]** Giá trị tính thuế xuất khẩu (nguyên tệ) |
| 41 | `GiaTriTinhThueXKQuyDoi` | `gia_tri_tinh_thue_xk_quy_doi` | `money_vnd` | N | `0` | **[Thuế xuất khẩu (nghiệp vụ xuất khẩu)]** Giá trị tính thuế xuất khẩu quy đổi |
| 42 | `ThueSuatXK` | `thue_suat_xk` | `percent_rate` | N | `0` | **[Thuế xuất khẩu (nghiệp vụ xuất khẩu)]** Thuế suất xuất khẩu (%) |
| 43 | `TienThueXK` | `tien_thue_xk` | `money_foreign` ≈ | N | `0` | **[Thuế xuất khẩu (nghiệp vụ xuất khẩu)]** Tiền thuế xuất khẩu (nguyên tệ) |
| 44 | `TienThueXKQuyDoi` | `tien_thue_xk_quy_doi` | `money_vnd` | N | `0` | **[Thuế xuất khẩu (nghiệp vụ xuất khẩu)]** Tiền thuế xuất khẩu quy đổi |
| 45 | `TaiKhoanThueXKId` | `tai_khoan_thue_xk_id` | `uuid` | Y | — | **[Thuế xuất khẩu (nghiệp vụ xuất khẩu)]** TK thuế xuất khẩu (reference đến ENT_HeThongTaiKhoan) `FK` |
| 46 | `DonDatHangId` | `don_dat_hang_id` | `uuid` | Y | — | **[Liên kết nguồn (dòng đơn đặt hàng kế thừa)]** ID đơn đặt hàng nguồn (reference đến ENT_DonDatHang) `FK` |
| 47 | `ChiTietDonDatHangId` | `chi_tiet_don_dat_hang_id` | `uuid` | Y | — | **[Liên kết nguồn (dòng đơn đặt hàng kế thừa)]** ID dòng đơn đặt hàng nguồn (reference đến ENT_ChiTietDonDatHang) `FK` |
| 48 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đơn vị (reference đến ENT_DonVi) `FK` |
| 49 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Vụ việc/công trình (reference đến ENT_CongTrinh) `FK` |
| 50 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 51 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 52 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Hợp đồng thống kê (reference đến ENT_HopDongBanHang) `FK` |
| 53 | `SoLuongDaXuatHoaDon` | `so_luong_da_xuat_hoa_don` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã xuất hóa đơn |
| 54 | `SoLuongDaXuatKho` | `so_luong_da_xuat_kho` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã xuất kho |
| 55 | `SoLuongDaXuatKhoQuyDoi` | `so_luong_da_xuat_kho_quy_doi` | `quantity` | N | `0` | **[Tổng hợp thực hiện (hệ thống tính)]** Số lượng đã xuất kho quy đổi về ĐVT chính |

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

**Đối chiếu `sal_chi_tiet_chung_tu_ban_hang` (69 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 29 | `chung_tu_ban_id`, `la_chiet_khau_thuong_mai`, `la_hang_khuyen_mai`, `vat_tu_id`, `ten_vat_tu`, `dien_giai`, `tai_khoan_cong_no_id`, `tai_khoan_doanh_thu_id`, `ty_le_chiet_khau`, `tien_chiet_khau`, `tien_chiet_khau_quy_doi`, `ty_le_chiet_khau_theo_hang`, `tien_chiet_khau_theo_hang`, `tien_chiet_khau_theo_hang_quy_doi`, `ty_le_chiet_khau_theo_hoa_don`, `tien_chiet_khau_theo_hoa_don`, `tien_chiet_khau_theo_hoa_don_quy_doi`, `thue_suat_gtgt`, `thue_suat_khac`, `dien_giai_thue`, `khong_tong_hop_to_khai_gtgt`, `tien_von`, `gia_tri_tinh_thue_xk`, `gia_tri_tinh_thue_xk_quy_doi`, `thue_suat_xk`, `don_dat_hang_id`, `chi_tiet_don_dat_hang_id`, `doi_tuong_tap_hop_chi_phi_id`, `so_luong_da_xuat_hoa_don` |
| DB có — LDM **không khai** | 33 | `so_con_no_vnd`, `so_con_no_nt`, `tong_no_phai_thu_vnd`, `tong_no_phai_thu_nt`, `mo_ta`, `chung_tu_ban_hang_id`, `references`, `so_luong_da_xuat_hd`, `hoa_don_ban_hang_id`, `ma_hang_id`, `ten_hang`, `don_gia_quy_doi`, `chiet_khau`, `chiet_khau_quy_doi`, `chiet_khau_phan_tram`, `tien_chiet_khau_hang`, `tien_chiet_khau_hang_quy_doi`, `tien_chiet_khau_hoa_don`, `tien_chiet_khau_hoa_don_quy_doi`, `hang_khuyen_mai`, `chiet_khau_thuong_mai`, `tai_khoan_no_id`, `tai_khoan_co_id`, `thue_suat_gtgt_mac_dinh`, `gia_tri_thue_gtgt`, `phan_tram_thue_xk`, `don_gia_von_quy_doi`, `tong_gia_tri_von`, `tong_gia_tri_von_quy_doi`, `phien_ban`, `don_gia_thue_xk`, `phan_tram_chiet_khau_hang`, `phan_tram_chiet_khau_hoa_don` |

---

## 8. `sal_hoa_don_ban_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HoaDonBan` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `sal_chung_tu_ban_hang` — FK `ON DELETE CASCADE` |
| Bảng con | `sal_hoa_don_ban_hang_chi_tiet` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiNghiepVu` | `loai_nghiep_vu` | `text` CHECK | N | — | **[Liên kết nguồn]** Loại nghiệp vụ (Bán hàng trong nước, Bán hàng xuất khẩu, Bán dịch vụ — kế thừa từ chứng từ bán nguồn) |
| 2 | `ChungTuBanId` | `chung_tu_ban_id` | `uuid` | Y | — | **[Liên kết nguồn]** ID chứng từ bán nguồn (reference đến ENT_ChungTuBan; NULL nếu lập hóa đơn trước, chứng từ sau) `FK` |
| 3 | `KhachHangId` | `khach_hang_id` | `uuid` | N | — | **[Người mua]** ID người mua (reference đến ENT_DoiTuong vai trò Khách hàng) `FK` |
| 4 | `TenKhachHang` | `ten_khach_hang` | `text` | N | — | **[Người mua]** Tên đơn vị/người mua trên hóa đơn |
| 5 | `MaSoThueCCCD` | `ma_so_thue_cccd` | `text` | Y | — | **[Người mua]** Mã số thuế hoặc CCCD chủ hộ |
| 6 | `NguoiMuaHang` | `nguoi_mua_hang` | `text` | Y | — | **[Người mua]** Họ tên người mua hàng |
| 7 | `MaSoDVQHNS` | `ma_so_dvqhns` | `text` | Y | — | **[Người mua]** Mã số đơn vị quan hệ ngân sách |
| 8 | `SoCCCD` | `so_cccd` | `text` | Y | — | **[Người mua]** Số CCCD người mua |
| 9 | `HoChieu` | `ho_chieu` | `text` | Y | — | **[Người mua]** Số hộ chiếu người mua |
| 10 | `DienThoai` | `dien_thoai` | `text` | Y | — | **[Người mua]** Số điện thoại người mua |
| 11 | `DiaChi` | `dia_chi` | `text` | N | — | **[Người mua]** Địa chỉ trên hóa đơn |
| 12 | `HinhThucThanhToan` | `hinh_thuc_thanh_toan` | `text` CHECK | N | — | **[Người mua]** Hình thức thanh toán trên hóa đơn (Tiền mặt, Chuyển khoản, TM/CK; cho nhập giá trị ngoài danh sách) |
| 13 | `TaiKhoanNganHangThuId` | `tai_khoan_ngan_hang_thu_id` | `uuid` | Y | — | **[Người mua]** Tài khoản ngân hàng nhận tiền (reference đến ENT_TaiKhoanNganHang) `FK` |
| 14 | `NhanVienBanHangId` | `nhan_vien_ban_hang_id` | `uuid` | Y | — | **[Người mua]** Nhân viên bán hàng (reference đến ENT_DoiTuong vai trò Nhân viên) `FK` |
| 15 | `MauSoHoaDonId` | `mau_so_hoa_don_id` | `uuid` | N | — | **[Thông tin hóa đơn]** Mẫu số hóa đơn (reference đến ENT_MauSoHoaDon) `FK` |
| 16 | `KyHieuHoaDon` | `ky_hieu_hoa_don` | `text` | N | — | **[Thông tin hóa đơn]** Ký hiệu hóa đơn |
| 17 | `NgayHoaDon` | `ngay_hoa_don` | `date` | N | — | **[Thông tin hóa đơn]** Ngày hóa đơn |
| 18 | `SoHoaDon` | `so_hoa_don` | `varchar(50)` | N | — | **[Thông tin hóa đơn]** Số hóa đơn (nhập thủ công — chưa kết nối cổng phát hành CQT) |
| 19 | `SoHopDong` | `so_hop_dong` | `varchar(50)` | Y | — | **[Thông tin xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Số hợp đồng (nhập tự do) |
| 20 | `NgayHopDong` | `ngay_hop_dong` | `date` | Y | — | **[Thông tin xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Ngày hợp đồng |
| 21 | `DiaDiemGiao` | `dia_diem_giao` | `text` | Y | — | **[Thông tin xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Địa điểm giao hàng (chọn từ ENT_DiaChiGiaoHang hoặc nhập tự do, lưu dạng text) |
| 22 | `DiaDiemNhan` | `dia_diem_nhan` | `text` | Y | — | **[Thông tin xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Địa điểm nhận hàng |
| 23 | `SoVanDon` | `so_van_don` | `text` | Y | — | **[Thông tin xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Số vận đơn |
| 24 | `SoContainer` | `so_container` | `text` | Y | — | **[Thông tin xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Số container |
| 25 | `DonViVanChuyen` | `don_vi_van_chuyen` | `text` | Y | — | **[Thông tin xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Đơn vị vận chuyển |
| 26 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ & chiết khấu]** Loại tiền (reference đến ENT_LoaiTien) `FK` |
| 27 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Tiền tệ & chiết khấu]** Tỷ giá quy đổi |
| 28 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Tiền tệ & chiết khấu]** Loại chiết khấu (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon \| TheoMatHangVaHoaDon) |
| 29 | `TyLeChietKhauChung` | `ty_le_chiet_khau_chung` | `percent_rate` | Y | `0` | **[Tiền tệ & chiết khấu]** % chiết khấu trên tổng hóa đơn (khi Loại chiết khấu = Theo % hóa đơn) |
| 30 | `TongTienHang` | `tong_tien_hang` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng tiền hàng |
| 31 | `TongChietKhau` | `tong_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu |
| 32 | `TongThueGTGT` | `tong_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế GTGT (bán hàng trong nước) |
| 33 | `TongThueXK` | `tong_thue_xk` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế xuất khẩu (bán hàng xuất khẩu) |
| 34 | `TongThanhToan` | `tong_thanh_toan` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thanh toán |
| 35 | `TongTienHangQuyDoi` | `tong_tien_hang_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng tiền hàng quy đổi |
| 36 | `TongChietKhauQuyDoi` | `tong_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng chiết khấu quy đổi |
| 37 | `TongThueGTGTQuyDoi` | `tong_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế GTGT quy đổi |
| 38 | `TongThueXKQuyDoi` | `tong_thue_xk_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thuế xuất khẩu quy đổi |
| 39 | `TongThanhToanQuyDoi` | `tong_thanh_toan_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng thanh toán quy đổi |
| 40 | `TrangThaiPhatHanh` | `trang_thai_phat_hanh` | `text` CHECK | N | — | **[Trạng thái]** Trạng thái phát hành (ChuaPhatHanh \| DaPhatHanh — luồng phát hành đặc tả riêng) |
| 41 | `TrangThaiLapChungTu` | `trang_thai_lap_chung_tu` | `text` CHECK | Y | — | **[Trạng thái]** Trạng thái lập chứng từ (ChuaLap \| DaLapMotPhan \| DaLapDu) |
| 42 | `TrangThaiHoaDon` | `trang_thai_hoa_don` | `text` CHECK | Y | — | **[Trạng thái]** Trạng thái hóa đơn (HoaDonGoc \| HoaDonDieuChinh \| HoaDonBiDieuChinh \| HoaDonThayThe \| HoaDonBiThayThe) |

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

## 9. `sal_hoa_don_ban_hang_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietHoaDonBan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sal_chi_tiet_hd_ban_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sal_hoa_don_ban_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sal_hoa_don_ban_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-U-16693 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `HoaDonBanId` | `hoa_don_ban_id` | `uuid` | N | — | ID hóa đơn cha (reference đến ENT_HoaDonBan) `FK` |
| 2 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | **[Phân loại dòng]** Loại dòng: True = dòng hàng, False = dòng ghi chú (chỉ nhập Tên hàng, không tham gia tính toán) |
| 3 | `LaChietKhauThuongMai` | `la_chiet_khau_thuong_mai` | `boolean` | Y | `false` | **[Phân loại dòng]** Dòng là chiết khấu thương mại |
| 4 | `LaHangKhuyenMai` | `la_hang_khuyen_mai` | `boolean` | Y | `false` | **[Phân loại dòng]** Dòng là hàng khuyến mại |
| 5 | `ChiTietChungTuBanId` | `chi_tiet_chung_tu_ban_id` | `uuid` | Y | — | **[Liên kết nguồn]** ID dòng chứng từ bán nguồn (reference đến ENT_ChiTietChungTuBan) `FK` |
| 6 | `VatTuId` | `vat_tu_id` | `uuid` | Y | — | **[Hàng hóa]** ID hàng hóa/dịch vụ (reference đến ENT_VatTu) `FK` |
| 7 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa]** Tên hàng hiển thị trên hóa đơn |
| 8 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hàng hóa]** Diễn giải dòng |
| 9 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | Y | — | **[Hàng hóa]** Đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 10 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Số lượng & giá]** Số lượng |
| 11 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | **[Số lượng & giá]** Đơn giá |
| 12 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Số lượng & giá]** Thành tiền |
| 13 | `ThanhTienQuyDoi` | `thanh_tien_quy_doi` | `money_vnd` | N | `0` | **[Số lượng & giá]** Thành tiền quy đổi |
| 14 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu dòng (%) |
| 15 | `TienChietKhau` | `tien_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu dòng |
| 16 | `TienChietKhauQuyDoi` | `tien_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu quy đổi |
| 17 | `TyLeChietKhauTheoHang` | `ty_le_chiet_khau_theo_hang` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu theo mặt hàng (%) |
| 18 | `TienChietKhauTheoHang` | `tien_chiet_khau_theo_hang` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo mặt hàng |
| 19 | `TienChietKhauTheoHangQuyDoi` | `tien_chiet_khau_theo_hang_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo mặt hàng quy đổi |
| 20 | `TyLeChietKhauTheoHoaDon` | `ty_le_chiet_khau_theo_hoa_don` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu phân bổ theo hóa đơn (%) |
| 21 | `TienChietKhauTheoHoaDon` | `tien_chiet_khau_theo_hoa_don` | `money_foreign` ≈ | N | `0` | **[Chiết khấu]** Tiền chiết khấu phân bổ theo hóa đơn |
| 22 | `TienChietKhauTheoHoaDonQuyDoi` | `tien_chiet_khau_theo_hoa_don_quy_doi` | `money_vnd` | N | `0` | **[Chiết khấu]** Tiền chiết khấu theo hóa đơn quy đổi |
| 23 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | **[Thuế GTGT]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC; nghiệp vụ xuất khẩu chỉ 0 và KCT) |
| 24 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | N | `0` | **[Thuế GTGT]** % thuế tự nhập khi Thuế suất = KHAC |
| 25 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT |
| 26 | `TienThueGTGTQuyDoi` | `tien_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT quy đổi |
| 27 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[Thuế GTGT]** Diễn giải thuế |
| 28 | `KhongTongHopToKhaiGTGT` | `khong_tong_hop_to_khai_gtgt` | `boolean` | Y | `false` | **[Thuế GTGT]** Hàng hóa không tổng hợp lên tờ khai thuế GTGT |
| 29 | `GiaTriTinhThueXK` | `gia_tri_tinh_thue_xk` | `money_foreign` ≈ | N | `0` | **[Thuế xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Giá trị tính thuế xuất khẩu (nguyên tệ) |
| 30 | `GiaTriTinhThueXKQuyDoi` | `gia_tri_tinh_thue_xk_quy_doi` | `money_vnd` | N | `0` | **[Thuế xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Giá trị tính thuế xuất khẩu quy đổi |
| 31 | `ThueSuatXK` | `thue_suat_xk` | `percent_rate` | N | `0` | **[Thuế xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Thuế suất xuất khẩu (%) |
| 32 | `TienThueXK` | `tien_thue_xk` | `money_foreign` ≈ | N | `0` | **[Thuế xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Tiền thuế xuất khẩu (nguyên tệ) |
| 33 | `TienThueXKQuyDoi` | `tien_thue_xk_quy_doi` | `money_vnd` | N | `0` | **[Thuế xuất khẩu (khi Loại nghiệp vụ = Bán hàng xuất khẩu)]** Tiền thuế xuất khẩu quy đổi |

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

**Đối chiếu `sal_chi_tiet_hd_ban_hang` (48 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 23 | `hoa_don_ban_id`, `la_chiet_khau_thuong_mai`, `la_hang_khuyen_mai`, `chi_tiet_chung_tu_ban_id`, `vat_tu_id`, `ten_vat_tu`, `dien_giai`, `ty_le_chiet_khau`, `tien_chiet_khau`, `tien_chiet_khau_quy_doi`, `ty_le_chiet_khau_theo_hang`, `tien_chiet_khau_theo_hang`, `tien_chiet_khau_theo_hang_quy_doi`, `ty_le_chiet_khau_theo_hoa_don`, `tien_chiet_khau_theo_hoa_don`, `tien_chiet_khau_theo_hoa_don_quy_doi`, `thue_suat_gtgt`, `thue_suat_khac`, `dien_giai_thue`, `khong_tong_hop_to_khai_gtgt`, `gia_tri_tinh_thue_xk`, `gia_tri_tinh_thue_xk_quy_doi`, `thue_suat_xk` |
| DB có — LDM **không khai** | 28 | `hoa_don_ban_hang_id`, `references`, `chung_tu_ban_hang_id`, `chung_tu_ban_dich_vu_id`, `chi_tiet_chung_tu_ban_hang_id`, `chi_tiet_chung_tu_ban_dich_vu_id`, `ma_hang_id`, `ten_hang`, `don_gia_quy_doi`, `chiet_khau`, `chiet_khau_quy_doi`, `chiet_khau_phan_tram`, `tien_chiet_khau_hang`, `tien_chiet_khau_hang_quy_doi`, `tien_chiet_khau_hoa_don`, `tien_chiet_khau_hoa_don_quy_doi`, `so_lo`, `han_su_dung`, `hang_khuyen_mai`, `chiet_khau_thuong_mai`, `thue_suat_gtgt_mac_dinh`, `gia_tri_thue_gtgt`, `phan_tram_thue_xk`, `hop_dong_id`, `don_vi_id`, `khoan_muc_chi_phi_id`, `vu_viec_id`, `phien_ban` |

