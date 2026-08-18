# `sal_` — Trả lại hàng bán

> Sinh tự động từ [`ldm-TraLaiHangBan.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-TraLaiHangBan.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**2 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ChungTuTraLaiHangBan` | `sal_chung_tu_tra_lai_hang_ban` | `sal_chung_tu_tra_lai_hang_ban` | B — có schema, chưa code | Đầu chứng từ — ⚠ *LDM chưa mô tả bảng này* |
| 2 | `ChiTietTraLaiHangBan` | `sal_chung_tu_tra_lai_hang_ban_chi_tiet` | `sal_chi_tiet_chung_tu_tra_lai_hang_ban` | B — có schema, chưa code | Dòng chi tiết của `sal_chung_tu_tra_lai_hang_ban` — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `sal_chung_tu_tra_lai_hang_ban`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuTraLaiHangBan` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sal_chung_tu_tra_lai_hang_ban` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `sal_chung_tu_tra_lai_hang_ban_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Chứng từ]** Diễn giải |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Chứng từ]** Loại tiền (reference ENT_LoaiTien) `FK` |
| 3 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Chứng từ]** Tỷ giá |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Chứng từ]** Trạng thái (ChuaGhiSo \| DaGhiSo) |
| 5 | `PhuongThucLapHoaDon` | `phuong_thuc_lap_hoa_don` | `text` CHECK | N | — | **[Điều khiển nghiệp vụ]** (NguoiMuaXuatHoaDon \| NguoiBanXuatHoaDonDieuChinh \| KhongCoHoaDon) |
| 6 | `ThanhToanNgay` | `thanh_toan_ngay` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Thanh toán ngay |
| 7 | `PhuongThucThanhToan` | `phuong_thuc_thanh_toan` | `text` CHECK | Y | — | **[Điều khiển nghiệp vụ]** (PhieuChi \| UyNhiemChi \| SecChuyenKhoan \| SecTienMat) |
| 8 | `LapKemPhieuNhapKho` | `lap_kem_phieu_nhap_kho` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Lập kèm phiếu nhập kho |
| 9 | `LapKemHoaDonDieuChinh` | `lap_kem_hoa_don_dieu_chinh` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Lập kèm hóa đơn điều chỉnh |
| 10 | `KhachHangId` | `khach_hang_id` | `uuid` | N | — | **[Khách hàng]** Khách hàng (reference ENT_DoiTuong) `FK` |
| 11 | `TenKhachHang` | `ten_khach_hang` | `text` | N | — | **[Khách hàng]** Tên khách hàng (snapshot) |
| 12 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | **[Khách hàng]** Mã số thuế khách hàng |
| 13 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Khách hàng]** Địa chỉ khách hàng |
| 14 | `NguoiGiaoHang` | `nguoi_giao_hang` | `text` | Y | — | **[Khách hàng]** Người giao hàng |
| 15 | `NhanVienBanHangId` | `nhan_vien_ban_hang_id` | `uuid` | Y | — | **[Khách hàng]** Nhân viên bán hàng (reference ENT_DoiTuong) `FK` |
| 16 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | Y | — | **[Chiết khấu]** Loại chiết khấu (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon) |
| 17 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu, 0-100 |
| 18 | `PhieuNhapKhoId` | `phieu_nhap_kho_id` | `uuid` | Y | — | **[Chứng từ sinh kèm]** Phiếu nhập kho sinh kèm (reference ENT_PhieuNhapKho) `FK` |
| 19 | `HoaDonDieuChinhId` | `hoa_don_dieu_chinh_id` | `uuid` | Y | — | **[Chứng từ sinh kèm]** Hóa đơn điều chỉnh sinh kèm (reference ENT_HoaDonBanHang) `FK` |
| 20 | `ChungTuThanhToanId` | `chung_tu_thanh_toan_id` | `uuid` | Y | — | **[Chứng từ sinh kèm]** Phiếu chi/UNC/Séc sinh kèm (reference ENT_PhieuChi) `FK` |

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

**Đối chiếu `sal_chung_tu_tra_lai_hang_ban` (53 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 10 | `dien_giai`, `trang_thai`, `phuong_thuc_lap_hoa_don`, `phuong_thuc_thanh_toan`, `lap_kem_phieu_nhap_kho`, `lap_kem_hoa_don_dieu_chinh`, `nguoi_giao_hang`, `ty_le_chiet_khau`, `hoa_don_dieu_chinh_id`, `chung_tu_thanh_toan_id` |
| DB có — LDM **không khai** | 30 | `tai_khoan_tien_id`, `muc_dich_thu_chi_id`, `so_chung_tu_phieu_chi`, `lap_kem_phieu_chi`, `kiem_phieu_nhap_kho`, `hoa_don_ban_hang_id`, `references`, `nguoi_mua_hang`, `ma_so_dvqhns`, `cccd`, `ho_chieu`, `gia_tri_chiet_khau`, `nguoi_lien_he`, `so_dien_thoai`, `mo_ta`, `nguoi_giao`, `hinh_thuc_thanh_toan`, `phieu_chi_id`, `nguoi_nhan`, `tai_khoan_ngan_hang_chi_id`, `dieu_chinh_hoa_don_ban_hang_id`, `tong_tien_hang_hoa`, `tong_tien_chiet_khau`, `tong_tien_truoc_thue`, `tong_tien_thue_gtgt`, `tong_tien_sau_thue`, `tong_tien_thanh_toan`, `so_tien_da_thanh_toan`, `trang_thai_chung_tu`, `da_nhap_kho` |

---

## 2. `sal_chung_tu_tra_lai_hang_ban_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietTraLaiHangBan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sal_chi_tiet_chung_tu_tra_lai_hang_ban` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sal_chung_tu_tra_lai_hang_ban` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sal_chung_tu_tra_lai_hang_ban` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuTraLaiHangBanId` | `chung_tu_tra_lai_hang_ban_id` | `uuid` | N | — | Chứng từ trả lại hàng bán (reference ENT_ChungTuTraLaiHangBan) `FK` |
| 2 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | Dòng hàng khi true, dòng ghi chú khi false |
| 3 | `ChungTuBanHangId` | `chung_tu_ban_hang_id` | `uuid` | Y | — | **[Chứng từ bán hàng gốc]** Chứng từ bán hàng gốc (reference ENT_ChungTuBan — đã gộp bán hàng + dịch vụ) `FK` |
| 4 | `ChiTietChungTuBanHangId` | `chi_tiet_chung_tu_ban_hang_id` | `uuid` | Y | — | **[Chứng từ bán hàng gốc]** Dòng hàng gốc (reference ENT_ChiTietChungTuBan) `FK` |
| 5 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Hàng hóa]** Mã hàng (reference ENT_VatTu) `FK` |
| 6 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa]** Tên hàng (snapshot) |
| 7 | `LoaiVatTuId` | `loai_vat_tu_id` | `uuid` | Y | — | **[Hàng hóa]** Tính chất hàng hóa dịch vụ (reference ENT_LoaiVatTu) `FK` |
| 8 | `LaHangKhuyenMai` | `la_hang_khuyen_mai` | `boolean` | Y | `false` | **[Hàng hóa]** Là hàng khuyến mại. Khi true thì Đơn giá = 0 |
| 9 | `KhoId` | `kho_id` | `uuid` | Y | — | **[Hàng hóa]** Kho nhập lại (reference ENT_Kho) `FK` |
| 10 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | Y | — | **[Hàng hóa]** Đơn vị tính (reference ENT_DonViTinh) `FK` |
| 11 | `DonViTinhChinhId` | `don_vi_tinh_chinh_id` | `uuid` | Y | — | **[Hàng hóa]** Đơn vị tính chính của vật tư (reference ENT_DonViTinh) `FK` |
| 12 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | Y | `0` | **[Hàng hóa]** Hệ số quy đổi về đơn vị tính chính |
| 13 | `SoLuongTheoDVC` | `so_luong_theo_dvc` | `quantity` | Y | `0` | **[Hàng hóa]** Số lượng theo đơn vị tính chính |
| 14 | `TaiKhoanDoanhThuId` | `tai_khoan_doanh_thu_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK doanh thu trả lại (reference ENT_HeThongTaiKhoan) `FK` |
| 15 | `TaiKhoanCongNoId` | `tai_khoan_cong_no_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK công nợ phải thu (reference ENT_HeThongTaiKhoan) `FK` |
| 16 | `TaiKhoanKhoId` | `tai_khoan_kho_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK kho (reference ENT_HeThongTaiKhoan) `FK` |
| 17 | `TaiKhoanGiaVonId` | `tai_khoan_gia_von_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK giá vốn (reference ENT_HeThongTaiKhoan) `FK` |
| 18 | `TaiKhoanThueGTGTId` | `tai_khoan_thue_gtgt_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK thuế GTGT đầu ra (reference ENT_HeThongTaiKhoan) `FK` |
| 19 | `TaiKhoanChietKhauId` | `tai_khoan_chiet_khau_id` | `uuid` | Y | — | **[Tài khoản hạch toán]** TK chiết khấu thương mại (reference ENT_HeThongTaiKhoan) `FK` |
| 20 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Số lượng và giá trị]** Số lượng trả lại, > 0 |
| 21 | `DonGia` | `don_gia` | `money_foreign` ≈ | Y | `0` | **[Số lượng và giá trị]** Đơn giá bán |
| 22 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Số lượng và giá trị]** Thành tiền |
| 23 | `TuDongApGia` | `tu_dong_ap_gia` | `boolean` | Y | `false` | **[Giá vốn]** Tự động áp giá vốn |
| 24 | `DonGiaVon` | `don_gia_von` | `money_foreign` ≈ | Y | `0` | **[Giá vốn]** Đơn giá vốn |
| 25 | `TienVon` | `tien_von` | `money_foreign` ≈ | Y | `0` | **[Giá vốn]** Tiền vốn |
| 26 | `SoPhieuXuatId` | `so_phieu_xuat_id` | `uuid` | Y | — | **[Giá vốn]** Phiếu xuất kho gốc (reference ENT_PhieuXuatKho). Dùng trả hàng theo PP đích danh `FK` |
| 27 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Chiết khấu]** Loại chiết khấu dòng (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon) |
| 28 | `ChietKhauPhanTram` | `chiet_khau_phan_tram` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu |
| 29 | `ChietKhau` | `chiet_khau` | `numeric(18,4)` ⚠ | Y | `0` | **[Chiết khấu]** Tiền chiết khấu |
| 30 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | N | — | **[Thuế GTGT]** (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 31 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | Y | `0` | **[Thuế GTGT]** Giá trị thuế suất thực tế |
| 32 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Thuế GTGT]** Tiền thuế GTGT |
| 33 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | **[Thuế GTGT]** Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5 — danh mục mới bỏ entity, dùng enum như ldm-MuaHang) |
| 34 | `KhongTongHopToKhaiGTGT` | `khong_tong_hop_to_khai_gtgt` | `boolean` | Y | `false` | **[Thuế GTGT]** Không tổng hợp trên tờ khai GTGT |
| 35 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[Thuế GTGT]** Diễn giải thuế |
| 36 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | **[Thông tin bổ sung]** Số lô |
| 37 | `HanSuDung` | `han_su_dung` | `date` | Y | — | **[Thông tin bổ sung]** Hạn sử dụng |
| 38 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đơn vị (reference ENT_DonVi) `FK` |
| 39 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 40 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Vụ việc (reference ENT_CongTrinh) `FK` |
| 41 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đối tượng THCP (reference ENT_DoiTuongTapHopChiPhi) `FK` |

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

**Đối chiếu `sal_chi_tiet_chung_tu_tra_lai_hang_ban` (45 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 22 | `loai_dong_hang`, `chung_tu_ban_hang_id`, `chi_tiet_chung_tu_ban_hang_id`, `vat_tu_id`, `ten_vat_tu`, `loai_vat_tu_id`, `la_hang_khuyen_mai`, `don_vi_tinh_chinh_id`, `he_so_quy_doi`, `so_luong_theo_dvc`, `tai_khoan_doanh_thu_id`, `tai_khoan_chiet_khau_id`, `tu_dong_ap_gia`, `tien_von`, `so_phieu_xuat_id`, `loai_chiet_khau`, `thue_suat_gtgt`, `thue_suat_khac`, `nhom_hhdv_mua_vao`, `khong_tong_hop_to_khai_gtgt`, `dien_giai_thue`, `doi_tuong_tap_hop_chi_phi_id` |
| DB có — LDM **không khai** | 16 | `chi_tiet_hoa_don_dieu_chinh_id`, `references`, `phieu_nhap_kho_id`, `chi_tiet_phieu_nhap_kho_id`, `chung_tu_ban_id`, `hoa_don_ban_hang_id`, `chi_tiet_hd_ban_hang_id`, `hang_hoa_id`, `ten_hang`, `gia_von`, `tai_khoan_tra_lai_id`, `thue_suat_gtgt_id`, `tu_nhap_don_gia_von`, `hang_khuyen_mai`, `hop_dong_id`, `phien_ban` |

