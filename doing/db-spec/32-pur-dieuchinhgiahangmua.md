# `pur_` — Điều chỉnh giá hàng mua

> Sinh tự động từ [`ldm-DieuChinhGiaHangMua.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-DieuChinhGiaHangMua.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**2 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ChungTuDieuChinhGiaHangMua` | `pur_chung_tu_dieu_chinh_gia_hang_mua` | `pur_chung_tu_dieu_chinh_gia_mua` | B — có schema, chưa code | Đầu chứng từ — Chứng từ điều chỉnh giá hàng mua Một bộ chứng từ gồm chứng từ điều chỉnh công nợ, chứng từ thu tiền khi giảm giá có thanh toán… |
| 2 | `ChiTietChungTuDieuChinhGiaHangMua` | `pur_chung_tu_dieu_chinh_gia_hang_mua_chi_tiet` | `pur_chi_tiet_dieu_chinh_gia_mua` | B — có schema, chưa code | Dòng chi tiết của `pur_chung_tu_dieu_chinh_gia_hang_mua` — Dòng chi tiết chứng từ điều chỉnh giá hàng mua |

---

## 1. `pur_chung_tu_dieu_chinh_gia_hang_mua`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuDieuChinhGiaHangMua` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chung_tu_dieu_chinh_gia_mua` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chứng từ điều chỉnh giá hàng mua · Một bộ chứng từ gồm chứng từ điều chỉnh công nợ, chứng từ thu tiền khi giảm giá · có thanh toán ngay hoặc chứng từ chi tiền khi tăng giá có thanh toán ngay, và · hóa đơn điều chỉnh khi có hóa đơn. |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `pur_chung_tu_dieu_chinh_gia_hang_mua_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Chứng từ]** Diễn giải |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | Y | — | **[Chứng từ]** Loại tiền (reference ENT_LoaiTien) `FK` |
| 3 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Chứng từ]** Tỷ giá |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Chứng từ]** Trạng thái (ChuaGhiSo \| DaGhiSo) |
| 5 | `LyDoDieuChinh` | `ly_do_dieu_chinh` | `text` CHECK | N | — | **[Điều khiển nghiệp vụ]** Lý do điều chỉnh (GiamGiaHangMua \| TangGiaHangMua) |
| 6 | `DieuChinhGiaTriHangNhapKho` | `dieu_chinh_gia_tri_hang_nhap_kho` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Điều chỉnh vào giá trị hàng đã nhập kho. Quyết định cặp tài khoản Nợ Có và việc hiện cột kho, số lô, hạn sử dụng |
| 7 | `KhongCoHoaDon` | `khong_co_hoa_don` | `boolean` | N | `false` | **[Điều khiển nghiệp vụ]** Chứng từ không có hóa đơn |
| 8 | `ThanhToanNgay` | `thanh_toan_ngay` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Thanh toán ngay khi true, điều chỉnh công nợ khi false |
| 9 | `HinhThucThanhToan` | `hinh_thuc_thanh_toan` | `text` CHECK | Y | — | **[Điều khiển nghiệp vụ]** Hình thức thanh toán (PhieuThu \| GiayBaoCo \| PhieuChi \| UyNhiemChi \| SecTienMat \| SecChuyenKhoan) |
| 10 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | Y | — | **[Nhà cung cấp]** Nhà cung cấp (reference ENT_DoiTuong, đối tượng có vai trò NhaCungCap) `FK` |
| 11 | `TenNhaCungCap` | `ten_nha_cung_cap` | `text` | N | — | **[Nhà cung cấp]** Tên nhà cung cấp |
| 12 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | **[Nhà cung cấp]** Mã số thuế nhà cung cấp |
| 13 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Nhà cung cấp]** Địa chỉ nhà cung cấp |
| 14 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | **[Nhà cung cấp]** Nhân viên mua hàng (reference ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |
| 15 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Chiết khấu]** Loại chiết khấu (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon) |
| 16 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu, đơn vị phần trăm, từ 0 đến 100 |
| 17 | `HoaDonDieuChinhId` | `hoa_don_dieu_chinh_id` | `uuid` | Y | — | **[Chứng từ sinh kèm trong bộ]** Hóa đơn điều chỉnh (reference ENT_HoaDonDieuChinh) `FK` |
| 18 | `ChungTuThuTienId` | `chung_tu_thu_tien_id` | `uuid` | Y | — | **[Chứng từ sinh kèm trong bộ]** Phiếu thu hoặc giấy báo có (reference ENT_PhieuThu) `FK` |
| 19 | `PhieuChiId` | `phieu_chi_id` | `uuid` | Y | — | **[Chứng từ sinh kèm trong bộ]** Phiếu chi, ủy nhiệm chi hoặc séc (reference ENT_PhieuChi) `FK` |

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

**Đối chiếu `pur_chung_tu_dieu_chinh_gia_mua` (56 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 5 | `dien_giai`, `khong_co_hoa_don`, `nhan_vien_id`, `hoa_don_dieu_chinh_id`, `chung_tu_thu_tien_id` |
| DB có — LDM **không khai** | 29 | `trang_thai_hoa_don`, `mau_so_hoa_don`, `ky_hieu_hoa_don`, `so_hoa_don`, `ngay_hoa_don`, `tai_khoan_tien_id`, `muc_dich_thu_chi_id`, `phieu_thu_id`, `so_chung_tu_phieu_thu_chi`, `lich_su_sua`, `tong_tien_chiet_khau`, `nhan_vien_mua_id`, `tt_tai_khoan_ngan_hang_chi_id`, `tt_ten_ngan_hang_chi`, `tt_tai_khoan_ngan_hang_thu_id`, `tt_ten_ngan_hang_thu`, `tt_mo_ta`, `tt_ngay_chung_tu`, `tt_ngay_hach_toan`, `tt_nguoi_nop_nhan`, `tt_nguoi_linh_tien`, `tt_so_giay_to`, `tt_ngay_cap`, `tt_noi_cap`, `tt_kem_theo`, `tt_chung_tu_goc`, `chung_tu_mua_hang_id`, `mo_ta`, `tong_chenh_lech_vnd` |

---

## 2. `pur_chung_tu_dieu_chinh_gia_hang_mua_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietChungTuDieuChinhGiaHangMua` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chi_tiet_dieu_chinh_gia_mua` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng chi tiết chứng từ điều chỉnh giá hàng mua |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_chung_tu_dieu_chinh_gia_hang_mua` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_chung_tu_dieu_chinh_gia_hang_mua` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuDieuChinhGiaHangMuaId` | `chung_tu_dieu_chinh_gia_hang_mua_id` | `uuid` | N | — | Chứng từ điều chỉnh giá hàng mua (reference ENT_ChungTuDieuChinhGiaHangMua) `FK` |
| 2 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | Dòng hàng khi true, dòng ghi chú khi false |
| 3 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | Y | — | **[Chứng từ mua hàng gốc: chỉ có khi lập từ chứng từ gốc]** Chứng từ mua hàng gốc của dòng (reference ENT_ChungTuMuaHang) `FK` |
| 4 | `ChiTietChungTuMuaHangId` | `chi_tiet_chung_tu_mua_hang_id` | `uuid` | Y | — | **[Chứng từ mua hàng gốc: chỉ có khi lập từ chứng từ gốc]** Dòng hàng gốc trên chứng từ mua hàng (reference ENT_ChiTietChungTuMuaHang) `FK` |
| 5 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Hàng hóa]** Mã hàng (reference ENT_VatTu). Khóa sửa khi dòng lấy từ chứng từ gốc `FK` |
| 6 | `TenVatTu` | `ten_vat_tu` | `text` | Y | — | **[Hàng hóa]** Tên hàng. Tự điền theo mã hàng; là nội dung ghi chú khi LoaiDongHang = false |
| 7 | `LoaiVatTuId` | `loai_vat_tu_id` | `uuid` | Y | — | **[Hàng hóa]** Tính chất hàng hóa dịch vụ của mã hàng (reference ENT_LoaiVatTu) `FK` |
| 8 | `KhoId` | `kho_id` | `uuid` | Y | — | **[Hàng hóa]** Kho (reference ENT_Kho) `FK` |
| 9 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | Y | — | **[Hàng hóa]** Đơn vị tính (reference ENT_DonViTinh) `FK` |
| 10 | `DonViTinhChinhId` | `don_vi_tinh_chinh_id` | `uuid` | Y | — | **[Hàng hóa]** Đơn vị tính chính của vật tư (reference ENT_DonViTinh) `FK` |
| 11 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | Y | `0` | **[Hàng hóa]** Hệ số quy đổi về đơn vị tính chính, lấy theo DonViQuyDoiVatTu.HeSoQuyDoi |
| 12 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Tài khoản hạch toán]** Tài khoản Nợ (reference ENT_HeThongTaiKhoan). Giảm giá lấy tài khoản công nợ phải trả; tăng giá lấy tài khoản vật tư khi điều chỉnh vào giá trị nhập kho, tài khoản chi phí khi không điều chỉnh `FK` |
| 13 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Tài khoản hạch toán]** Tài khoản Có (reference ENT_HeThongTaiKhoan). Giảm giá lấy tài khoản vật tư hoặc tài khoản chi phí; tăng giá lấy tài khoản công nợ phải trả `FK` |
| 14 | `SoLuong` | `so_luong` | `quantity` | Y | `0` | **[Số lượng và giá trị điều chỉnh]** Số lượng |
| 15 | `DonGia` | `don_gia` | `money_foreign` ≈ | Y | `0` | **[Số lượng và giá trị điều chỉnh]** Đơn giá điều chỉnh, không âm |
| 16 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | N | `0` | **[Số lượng và giá trị điều chỉnh]** Thành tiền, bằng SoLuong nhân DonGia. Sửa tay thì tính ngược DonGia |
| 17 | `ChietKhauPhanTram` | `chiet_khau_phan_tram` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu, đơn vị phần trăm, từ 0 đến 100 |
| 18 | `ChietKhau` | `chiet_khau` | `numeric(18,4)` ⚠ | Y | `0` | **[Chiết khấu]** Tiền chiết khấu, không vượt quá ThanhTien |
| 19 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | **[Thuế GTGT: ẩn khi KhongCoHoaDon = true]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 20 | `ThueSuatKhac` | `thue_suat_khac` | `percent_rate` | Y | `0` | **[Thuế GTGT: ẩn khi KhongCoHoaDon = true]** Giá trị thuế suất GTGT thực tế, đơn vị phần trăm |
| 21 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Thuế GTGT: ẩn khi KhongCoHoaDon = true]** Tiền thuế GTGT, bằng ThanhTien trừ ChietKhau rồi nhân ThueSuatKhac chia 100 |
| 22 | `TaiKhoanThueGTGTId` | `tai_khoan_thue_gtgt_id` | `uuid` | Y | — | **[Thuế GTGT: ẩn khi KhongCoHoaDon = true]** Tài khoản thuế GTGT (reference ENT_HeThongTaiKhoan) `FK` |
| 23 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | **[Thuế GTGT: ẩn khi KhongCoHoaDon = true]** Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5) |
| 24 | `KhongTongHopToKhaiGTGT` | `khong_tong_hop_to_khai_gtgt` | `boolean` | N | `false` | **[Thuế GTGT: ẩn khi KhongCoHoaDon = true]** Hàng hóa không tổng hợp trên tờ khai thuế GTGT |
| 25 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[Thuế GTGT: ẩn khi KhongCoHoaDon = true]** Diễn giải thuế |
| 26 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | **[Thông tin bổ sung]** Số lô |
| 27 | `HanSuDung` | `han_su_dung` | `date` | Y | — | **[Thông tin bổ sung]** Hạn sử dụng |
| 28 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đơn vị (reference ENT_DonVi) `FK` |
| 29 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 30 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Vụ việc (reference ENT_CongTrinh) `FK` |
| 31 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thông tin bổ sung]** Đối tượng tập hợp chi phí (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 32 | `ChiPhiKhongHopLy` | `chi_phi_khong_hop_ly` | `boolean` | Y | `false` | **[Thông tin bổ sung]** Chi phí không hợp lý |

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

**Đối chiếu `pur_chi_tiet_dieu_chinh_gia_mua` (35 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 15 | `chung_tu_dieu_chinh_gia_hang_mua_id`, `loai_dong_hang`, `chung_tu_mua_hang_id`, `ten_vat_tu`, `loai_vat_tu_id`, `don_vi_tinh_chinh_id`, `he_so_quy_doi`, `thanh_tien`, `chiet_khau`, `thue_suat_gtgt`, `thue_suat_khac`, `tien_thue_gtgt`, `nhom_hhdv_mua_vao`, `khong_tong_hop_to_khai_gtgt`, `dien_giai_thue` |
| DB có — LDM **không khai** | 8 | `tien_thue_gtgt_vnd`, `tien_chiet_khau`, `tinh_chat_thue_gtgt_id`, `chung_tu_dieu_chinh_gia_mua_id`, `ten_hang`, `so_tien_chenh_lech_vnd`, `dien_giai`, `phien_ban` |

