# `sal_` — Điều chỉnh giá hàng bán

> Sinh tự động từ [`ldm-DieuChinhGiaHangBan.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-DieuChinhGiaHangBan.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**2 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ChungTuDieuChinhGiaHangBan` | `sal_chung_tu_dieu_chinh_gia_hang_ban` | `sal_dieu_chinh_gia_hang_ban` | B — có schema, chưa code | Đầu chứng từ — ⚠ *LDM chưa mô tả bảng này* |
| 2 | `ChiTietDieuChinhGiaHangBan` | `sal_chung_tu_dieu_chinh_gia_hang_ban_chi_tiet` | `sal_chi_tiet_dieu_chinh_gia_hang_ban` | B — có schema, chưa code | Dòng chi tiết của `sal_chung_tu_dieu_chinh_gia_hang_ban` — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `sal_chung_tu_dieu_chinh_gia_hang_ban`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuDieuChinhGiaHangBan` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sal_dieu_chinh_gia_hang_ban` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `sal_chung_tu_dieu_chinh_gia_hang_ban_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Chứng từ]** Diễn giải |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | Y | — | **[Chứng từ]** Loại tiền (reference ENT_LoaiTien) `FK` |
| 3 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Chứng từ]** Tỷ giá |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Chứng từ]** Trạng thái (ChuaGhiSo \| DaGhiSo) |
| 5 | `PhuongThucDieuChinh` | `phuong_thuc_dieu_chinh` | `text` CHECK | N | — | **[Điều khiển nghiệp vụ]** Hướng điều chỉnh (TangGiaHangBan \| GiamGiaHangBan) |
| 6 | `ThanhToanNgay` | `thanh_toan_ngay` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Thanh toán ngay |
| 7 | `PhuongThucThanhToan` | `phuong_thuc_thanh_toan` | `text` CHECK | Y | — | **[Điều khiển nghiệp vụ]** (PhieuThu \| GiayBaoCo \| PhieuChi \| UyNhiemChi \| SecTienMat \| SecChuyenKhoan) |
| 8 | `LapKemHoaDonDieuChinh` | `lap_kem_hoa_don_dieu_chinh` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Lập kèm HĐ điều chỉnh |
| 9 | `KhachHangId` | `khach_hang_id` | `uuid` | N | — | **[Khách hàng & Thanh toán]** Khách hàng (reference ENT_DoiTuong) `FK` |
| 10 | `TenKhachHang` | `ten_khach_hang` | `text` | N | — | **[Khách hàng & Thanh toán]** Tên khách hàng (snapshot) |
| 11 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | **[Khách hàng & Thanh toán]** Mã số thuế |
| 12 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Khách hàng & Thanh toán]** Địa chỉ |
| 13 | `NhanVienBanHangId` | `nhan_vien_ban_hang_id` | `uuid` | Y | — | **[Khách hàng & Thanh toán]** Nhân viên bán hàng (reference ENT_DoiTuong) `FK` |
| 14 | `NguoiGiaoDich` | `nguoi_giao_dich` | `text` | Y | — | **[Khách hàng & Thanh toán]** Người nộp / Người nhận / Người lĩnh tiền |
| 15 | `SoGiayTo` | `so_giay_to` | `text` | Y | — | **[Khách hàng & Thanh toán]** Số giấy tờ (Séc tiền mặt) |
| 16 | `NgayCap` | `ngay_cap` | `date` | Y | — | **[Khách hàng & Thanh toán]** Ngày cấp |
| 17 | `NoiCap` | `noi_cap` | `text` | Y | — | **[Khách hàng & Thanh toán]** Nơi cấp |
| 18 | `TaiKhoanTienId` | `tai_khoan_tien_id` | `uuid` | Y | — | **[Khách hàng & Thanh toán]** Tài khoản tiền (reference ENT_HeThongTaiKhoan) `FK` |
| 19 | `TaiKhoanNganHangId` | `tai_khoan_ngan_hang_id` | `uuid` | Y | — | **[Khách hàng & Thanh toán]** Tài khoản ngân hàng nhận/chi (reference ENT_TaiKhoanNganHang) `FK` |
| 20 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Chiết khấu]** Loại chiết khấu (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon) |
| 21 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu, 0-100 |
| 22 | `HinhThucThanhToanHoaDon` | `hinh_thuc_thanh_toan_hoa_don` | `text` | Y | — | **[Thông tin Hóa đơn]** Hình thức thanh toán (Tiền mặt \| Chuyển khoản \| TM/CK) |
| 23 | `TaiKhoanNganHangThuId` | `tai_khoan_ngan_hang_thu_id` | `uuid` | Y | — | **[Thông tin Hóa đơn]** Tài khoản NH thu (reference ENT_TaiKhoanNganHang) `FK` |
| 24 | `LoaiDieuChinh` | `loai_dieu_chinh` | `text` CHECK | Y | — | **[Thông tin Hóa đơn]** (DieuChinhGia \| SaiSot \| Khac) |
| 25 | `LyDoDieuChinh` | `ly_do_dieu_chinh` | `text` | Y | — | **[Thông tin Hóa đơn]** Lý do điều chỉnh |
| 26 | `MauSoHoaDon` | `mau_so_hoa_don` | `text` | Y | — | **[Thông tin Hóa đơn]** Mẫu số HĐ |
| 27 | `KyHieuHoaDon` | `ky_hieu_hoa_don` | `text` | Y | — | **[Thông tin Hóa đơn]** Ký hiệu HĐ |
| 28 | `SoHoaDonDC` | `so_hoa_don_dc` | `text` | Y | — | **[Thông tin Hóa đơn]** Số hóa đơn điều chỉnh |
| 29 | `NgayHoaDonDC` | `ngay_hoa_don_dc` | `date` | Y | — | **[Thông tin Hóa đơn]** Ngày lập HĐ điều chỉnh |
| 30 | `NguoiMuaHang` | `nguoi_mua_hang` | `text` | Y | — | **[Thông tin Hóa đơn]** Người mua hàng |
| 31 | `MaSoDVQHNS` | `ma_so_dvqhns` | `text` | Y | — | **[Thông tin Hóa đơn]** Mã số đơn vị có QHNS |
| 32 | `CCCD` | `cccd` | `text` | Y | — | **[Thông tin Hóa đơn]** Số căn cước công dân |
| 33 | `HoChieu` | `ho_chieu` | `text` | Y | — | **[Thông tin Hóa đơn]** Số hộ chiếu |
| 34 | `DienThoai` | `dien_thoai` | `text` | Y | — | **[Thông tin Hóa đơn]** Điện thoại |
| 35 | `HoaDonCanDieuChinhId` | `hoa_don_can_dieu_chinh_id` | `uuid` | Y | — | **[Chứng từ sinh kèm]** Hóa đơn cần điều chỉnh (reference ENT_HoaDonBanHang) `FK` |
| 36 | `HoaDonDieuChinhId` | `hoa_don_dieu_chinh_id` | `uuid` | Y | — | **[Chứng từ sinh kèm]** Hóa đơn điều chỉnh sinh kèm (reference ENT_HoaDonBanHang) `FK` |
| 37 | `ChungTuThanhToanId` | `chung_tu_thanh_toan_id` | `uuid` | Y | — | **[Chứng từ sinh kèm]** Phiếu thu/chi sinh kèm (reference ENT_PhieuThu / ENT_PhieuChi theo chiều điều chỉnh) `FK` |

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

**Đối chiếu `sal_dieu_chinh_gia_hang_ban` (55 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 21 | `dien_giai`, `trang_thai`, `phuong_thuc_dieu_chinh`, `thanh_toan_ngay`, `phuong_thuc_thanh_toan`, `lap_kem_hoa_don_dieu_chinh`, `nguoi_giao_dich`, `so_giay_to`, `ngay_cap`, `noi_cap`, `tai_khoan_ngan_hang_id`, `loai_chiet_khau`, `ty_le_chiet_khau`, `hinh_thuc_thanh_toan_hoa_don`, `ly_do_dieu_chinh`, `mau_so_hoa_don`, `so_hoa_don_dc`, `ngay_hoa_don_dc`, `dien_thoai`, `hoa_don_can_dieu_chinh_id`, `chung_tu_thanh_toan_id` |
| DB có — LDM **không khai** | 26 | `muc_dich_thu_chi_id`, `so_chung_tu_phieu_thu_chi`, `trang_thai_hoa_don`, `hinh_thuc_thanh_toan`, `chung_tu_ban_hang_id`, `references`, `chung_tu_ban_dich_vu_id`, `hoa_don_ban_hang_id`, `mo_ta`, `mau_so_hoa_don_id`, `so_hoa_don_dieu_chinh`, `ngay_hoa_don_dieu_chinh`, `phieu_thu_id`, `phieu_chi_id`, `giay_bao_co_id`, `giay_bao_no_id`, `sec_tien_mat_id`, `sec_chuyen_khoan_id`, `tai_khoan_ngan_hang_chi_id`, `tong_tien_hang_chenh_lech`, `tong_tien_chiet_khau_chenh_lech`, `tong_tien_truoc_thue_chenh_lech`, `tong_tien_thue_gtgt_chenh_lech`, `tong_tien_sau_thue_chenh_lech`, `tong_thanh_toan_chenh_lech`, `trang_thai_chung_tu` |

---

## 2. `sal_chung_tu_dieu_chinh_gia_hang_ban_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDieuChinhGiaHangBan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `sal_chi_tiet_dieu_chinh_gia_hang_ban` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `sal_chung_tu_dieu_chinh_gia_hang_ban` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `sal_chung_tu_dieu_chinh_gia_hang_ban` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuDieuChinhGiaHangBanId` | `chung_tu_dieu_chinh_gia_hang_ban_id` | `uuid` | N | — | CT ĐCGhB (reference ENT_ChungTuDieuChinhGiaHangBan) `FK` |
| 2 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | Dòng hàng khi true, dòng ghi chú khi false |
| 3 | `ChungTuBanHangId` | `chung_tu_ban_hang_id` | `uuid` | Y | — | **[Chứng từ bán hàng gốc]** CT bán hàng gốc (reference ENT_ChungTuBan — đã gộp bán hàng + dịch vụ) `FK` |
| 4 | `ChiTietChungTuBanHangId` | `chi_tiet_chung_tu_ban_hang_id` | `uuid` | Y | — | **[Chứng từ bán hàng gốc]** Dòng hàng gốc (reference ENT_ChiTietChungTuBan) `FK` |
| 5 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Hàng hóa]** Mã hàng (reference ENT_VatTu) `FK` |
| 6 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa]** Tên hàng (snapshot) |
| 7 | `LoaiVatTuId` | `loai_vat_tu_id` | `uuid` | Y | — | **[Hàng hóa]** Tính chất HHDV (reference ENT_LoaiVatTu) `FK` |
| 8 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | Y | — | **[Hàng hóa]** ĐVT (reference ENT_DonViTinh) `FK` |
| 9 | `DonViTinhChinhId` | `don_vi_tinh_chinh_id` | `uuid` | Y | — | **[Hàng hóa]** ĐVT chính (reference ENT_DonViTinh) `FK` |
| 10 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | Y | `0` | **[Hàng hóa]** Hệ số quy đổi |
| 11 | `TaiKhoanDoanhThuId` | `tai_khoan_doanh_thu_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK doanh thu/giảm giá (reference ENT_HeThongTaiKhoan) `FK` |
| 12 | `TaiKhoanCongNoId` | `tai_khoan_cong_no_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK công nợ phải thu (reference ENT_HeThongTaiKhoan) `FK` |
| 13 | `TaiKhoanThueGTGTId` | `tai_khoan_thue_gtgt_id` | `uuid` | N | — | **[Tài khoản hạch toán]** TK thuế GTGT đầu ra (reference ENT_HeThongTaiKhoan) `FK` |
| 14 | `TaiKhoanChietKhauId` | `tai_khoan_chiet_khau_id` | `uuid` | Y | — | **[Tài khoản hạch toán]** TK chiết khấu (reference ENT_HeThongTaiKhoan) `FK` |
| 15 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Số lượng và giá trị]** Số lượng điều chỉnh, > 0 |
| 16 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | **[Số lượng và giá trị]** Đơn giá điều chỉnh |
| 17 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Số lượng và giá trị]** Thành tiền |
| 18 | `ChietKhauPhanTram` | `chiet_khau_phan_tram` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu |
| 19 | `ChietKhau` | `chiet_khau` | `numeric(18,4)` ⚠ | Y | `0` | **[Chiết khấu]** Tiền chiết khấu |
| 20 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | N | — | **[Thuế GTGT]** (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 21 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | Y | `0` | **[Thuế GTGT]** Giá trị thuế suất thực tế |
| 22 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Thuế GTGT]** Tiền thuế GTGT |
| 23 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | **[Thuế GTGT]** Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5 — danh mục mới bỏ entity, dùng enum như ldm-MuaHang) |
| 24 | `KhongTongHopToKhaiGTGT` | `khong_tong_hop_to_khai_gtgt` | `boolean` | Y | `false` | **[Thuế GTGT]** Không tổng hợp trên tờ khai thuế GTGT |
| 25 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[Thuế GTGT]** Diễn giải thuế |
| 26 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | **[Thông tin bổ sung]** Số lô |
| 27 | `HanSuDung` | `han_su_dung` | `date` | Y | — | **[Thông tin bổ sung]** Hạn sử dụng |
| 28 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đơn vị (reference ENT_DonVi) `FK` |
| 29 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 30 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Vụ việc (reference ENT_CongTrinh) `FK` |
| 31 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đối tượng THCP (reference ENT_DoiTuongTapHopChiPhi) `FK` |

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

**Đối chiếu `sal_chi_tiet_dieu_chinh_gia_hang_ban` (39 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 23 | `chung_tu_dieu_chinh_gia_hang_ban_id`, `loai_dong_hang`, `chung_tu_ban_hang_id`, `loai_vat_tu_id`, `don_vi_tinh_chinh_id`, `he_so_quy_doi`, `so_luong`, `don_gia`, `thanh_tien`, `chiet_khau_phan_tram`, `chiet_khau`, `thue_suat_gtgt`, `thue_suat_khac`, `tien_thue_gtgt`, `nhom_hhdv_mua_vao`, `khong_tong_hop_to_khai_gtgt`, `dien_giai_thue`, `so_lo`, `han_su_dung`, `don_vi_id`, `khoan_muc_chi_phi_id`, `vu_viec_id`, `doi_tuong_tap_hop_chi_phi_id` |
| DB có — LDM **không khai** | 21 | `dieu_chinh_gia_hang_ban_id`, `references`, `chi_tiet_chung_tu_ban_dich_vu_id`, `chi_tiet_hd_ban_hang_id`, `so_luong_tang`, `don_gia_tang`, `thanh_tien_tang`, `chiet_khau_phan_tram_tang`, `chiet_khau_tien_tang`, `so_luong_giam`, `don_gia_giam`, `thanh_tien_giam`, `chiet_khau_phan_tram_giam`, `chiet_khau_tien_giam`, `thue_suat_gtgt_id`, `tien_thue_gtgt_chenh_lech`, `ngay_chung_tu_goc`, `so_chung_tu_goc`, `so_hoa_don_goc`, `phien_ban`, `tai_khoan_giam_gia_id` |

