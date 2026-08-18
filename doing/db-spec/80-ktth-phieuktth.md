# `ktth_` — Phiếu kế toán tổng hợp

> Sinh tự động từ [`ldm-PhieuKTTH.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-PhieuKTTH.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**3 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `PhieuKeToanTongHop` | `ktth_phieu_ke_toan_tong_hop` | `ktth_phieu_ke_toan_tong_hop` | B — có schema, chưa code | Đầu chứng từ — Phiếu kế toán tổng hợp (Master) |
| 2 | `ChiTietPhieuKTTH_HachToan` | `ktth_phieu_ke_toan_tong_hop_hach_toan` | `ktth_chi_tiet_phieu_ktth_hach_toan` | B — có schema, chưa code | Dòng chi tiết của `ktth_phieu_ke_toan_tong_hop` — Chi tiết hạch toán (Detail - tab Hạch toán) |
| 3 | `ChiTietPhieuKTTH_HoaDon` | `ktth_phieu_ke_toan_tong_hop_hoa_don` | `ktth_chi_tiet_phieu_ktth_hoa_don` | B — có schema, chưa code | Dòng chi tiết của `ktth_phieu_ke_toan_tong_hop` — Chi tiết kê khai hóa đơn và hạch toán thuế (Detail - tab 2) |

---

## 1. `ktth_phieu_ke_toan_tong_hop`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuKeToanTongHop` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ktth_phieu_ke_toan_tong_hop` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu kế toán tổng hợp (Master) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ktth_phieu_ke_toan_tong_hop_hach_toan` · `ktth_phieu_ke_toan_tong_hop_hoa_don` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiPhieu` | `loai_phieu` | `text` CHECK | N | — | Loại nghiệp vụ (HachToanThueTNDN \| HachToanChiPhiLuong \| ChungTuNghiepVuKhac \| KetChuyenLaiLoDauNam \| BuTruCongNo \| XuLyChenhLechTyGia \| VayNganHangChuyenTraNCC) |
| 2 | `Thang` | `thang` | `integer` | Y | `0` | Tháng (loại Xử lý chênh lệch tỷ giá) |
| 3 | `Nam` | `nam` | `integer` | Y | `0` | Năm (loại Kết chuyển lãi lỗ đầu năm, Xử lý chênh lệch tỷ giá) |
| 4 | `TongTien` | `tong_tien` | `money_foreign` ≈ | N | `0` | Tổng tiền của phiếu |
| 5 | `HachToanGopNhieuHoaDon` | `hach_toan_gop_nhieu_hoa_don` | `boolean` | Y | `false` | Hạch toán gộp nhiều hóa đơn (MVP2) |
| 6 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |
| 7 | `LoaiTienId` | `loai_tien_id` | `uuid` | Y | — | **[Đầu chứng từ]** ID loại tiền (reference ENT_LoaiTien) `FK` |
| 8 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Đầu chứng từ]** Tỷ giá |
| 9 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Đầu chứng từ]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `ktth_phieu_ke_toan_tong_hop` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `thang`, `hach_toan_gop_nhieu_hoa_don`, `dien_giai` |
| DB có — LDM **không khai** | 1 | `mo_ta` |

---

## 2. `ktth_phieu_ke_toan_tong_hop_hach_toan`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuKTTH_HachToan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ktth_chi_tiet_phieu_ktth_hach_toan` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết hạch toán (Detail - tab Hạch toán) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ktth_phieu_ke_toan_tong_hop` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ktth_phieu_ke_toan_tong_hop` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKeToanTongHopId` | `phieu_ke_toan_tong_hop_id` | `uuid` | N | — | ID phiếu kế toán tổng hợp (reference ENT_PhieuKeToanTongHop) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải dòng |
| 3 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản Nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 4 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản Có (reference ENT_HeThongTaiKhoan) `FK` |
| 5 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | Số tiền nguyên tệ |
| 6 | `SoTienQuyDoi` | `so_tien_quy_doi` | `money_vnd` | Y | `0` | Số tiền quy đổi |
| 7 | `ChiPhiKhongHopLy` | `chi_phi_khong_hop_ly` | `boolean` | Y | `false` | Chi phí không hợp lý |
| 8 | `DoiTuongNoId` | `doi_tuong_no_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID đối tượng nợ (reference ENT_DoiTuong) `FK` |
| 9 | `TenDoiTuongNo` | `ten_doi_tuong_no` | `text` | Y | — | **[Đối tượng theo dõi]** Tên đối tượng nợ |
| 10 | `DoiTuongCoId` | `doi_tuong_co_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID đối tượng có (reference ENT_DoiTuong) `FK` |
| 11 | `TenDoiTuongCo` | `ten_doi_tuong_co` | `text` | Y | — | **[Đối tượng theo dõi]** Tên đối tượng có |
| 12 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID nhân viên (reference ENT_DoiTuong, vai trò NhanVien) `FK` |
| 13 | `TaiKhoanNganHangId` | `tai_khoan_ngan_hang_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID tài khoản ngân hàng (reference ENT_TaiKhoanNganHang) `FK` |
| 14 | `KheUocId` | `khe_uoc_id` | `uuid` | Y | — | **[Đối tượng theo dõi]** ID khế ước đi vay (reference ENT_KheUoc) `FK` |
| 15 | `LoaiTienId` | `loai_tien_id` | `uuid` | Y | — | **[Tỷ giá xuất quỹ (loại Xử lý chênh lệch tỷ giá)]** ID loại tiền của dòng (reference ENT_LoaiTien) `FK` |
| 16 | `SoTienDaXuat` | `so_tien_da_xuat` | `money_foreign` ≈ | Y | `0` | **[Tỷ giá xuất quỹ (loại Xử lý chênh lệch tỷ giá)]** Số tiền ngoại tệ đã xuất |
| 17 | `SoQuyDoiTheoCTGoc` | `so_quy_doi_theo_ct_goc` | `numeric(18,4)` ⚠ | Y | `0` | **[Tỷ giá xuất quỹ (loại Xử lý chênh lệch tỷ giá)]** Số quy đổi theo chứng từ gốc |
| 18 | `TyGiaXuatQuy` | `ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (loại Xử lý chênh lệch tỷ giá)]** Tỷ giá xuất quỹ |
| 19 | `QuyDoiTheoTyGiaXuatQuy` | `quy_doi_theo_ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (loại Xử lý chênh lệch tỷ giá)]** Quy đổi theo tỷ giá xuất quỹ |
| 20 | `ChenhLechTyGiaXuatQuy` | `chenh_lech_ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (loại Xử lý chênh lệch tỷ giá)]** Chênh lệch tỷ giá xuất quỹ |
| 21 | `TaiKhoanXuLyChenhLechId` | `tai_khoan_xu_ly_chenh_lech_id` | `uuid` | Y | — | **[Tỷ giá xuất quỹ (loại Xử lý chênh lệch tỷ giá)]** ID tài khoản xử lý chênh lệch (reference ENT_HeThongTaiKhoan) `FK` |
| 22 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Trường tự do]** ID đơn vị (reference ENT_DonVi) `FK` |
| 23 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID đối tượng tập hợp chi phí (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 24 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Trường tự do]** ID vụ việc (reference ENT_CongTrinh) `FK` |
| 25 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 26 | `DonDatHangId` | `don_dat_hang_id` | `uuid` | Y | — | **[Trường tự do]** ID đơn đặt hàng (reference ENT_DonDatHang) `FK` |
| 27 | `HopDongBanHangId` | `hop_dong_ban_hang_id` | `uuid` | Y | — | **[Trường tự do]** ID hợp đồng bán hàng (reference ENT_HopDongBanHang) `FK` |

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

**Đối chiếu `ktth_chi_tiet_phieu_ktth_hach_toan` (28 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 14 | `phieu_ke_toan_tong_hop_id`, `dien_giai`, `ten_doi_tuong_no`, `ten_doi_tuong_co`, `tai_khoan_ngan_hang_id`, `khe_uoc_id`, `so_tien_da_xuat`, `so_quy_doi_theo_ct_goc`, `ty_gia_xuat_quy`, `quy_doi_theo_ty_gia_xuat_quy`, `chenh_lech_ty_gia_xuat_quy`, `tai_khoan_xu_ly_chenh_lech_id`, `don_dat_hang_id`, `hop_dong_ban_hang_id` |
| DB có — LDM **không khai** | 6 | `phieu_ktth_id`, `mo_ta`, `ty_gia`, `doi_tuong_no`, `doi_tuong_co`, `phien_ban` |

---

## 3. `ktth_phieu_ke_toan_tong_hop_hoa_don`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuKTTH_HoaDon` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ktth_chi_tiet_phieu_ktth_hoa_don` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết kê khai hóa đơn và hạch toán thuế (Detail - tab 2) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ktth_phieu_ke_toan_tong_hop` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ktth_phieu_ke_toan_tong_hop` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKeToanTongHopId` | `phieu_ke_toan_tong_hop_id` | `uuid` | N | — | ID phiếu kế toán tổng hợp (reference ENT_PhieuKeToanTongHop) `FK` |
| 2 | `ChiTietHachToanId` | `chi_tiet_hach_toan_id` | `uuid` | Y | — | ID dòng hạch toán liên kết (reference ENT_ChiTietPhieuKTTH_HachToan) `FK` |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |
| 4 | `CoHoaDon` | `co_hoa_don` | `boolean` | Y | `false` | Có hóa đơn |
| 5 | `LoaiThue` | `loai_thue` | `text` CHECK | Y | — | Loại thuế (TangThueDauVao \| GiamThueDauVao \| TangThueDauRa \| GiamThueDauRa) |
| 6 | `GiaTriChuaThue` | `gia_tri_chua_thue` | `money_foreign` ≈ | Y | `0` | Giá trị chưa thuế nguyên tệ |
| 7 | `GiaTriChuaThueQuyDoi` | `gia_tri_chua_thue_quy_doi` | `money_vnd` | Y | `0` | Giá trị chưa thuế quy đổi |
| 8 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 9 | `GiaTriThueSuatKhac` | `gia_tri_thue_suat_khac` | `percent_rate` | Y | `0` | Phần trăm thuế suất thực tế |
| 10 | `TienThue` | `tien_thue` | `money_foreign` ≈ | N | `0` | Tiền thuế GTGT |
| 11 | `TienThueQuyDoi` | `tien_thue_quy_doi` | `money_vnd` | N | `0` | Tiền thuế GTGT quy đổi |
| 12 | `TaiKhoanThueId` | `tai_khoan_thue_id` | `uuid` | Y | — | ID tài khoản thuế GTGT (reference ENT_HeThongTaiKhoan) `FK` |
| 13 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | Y | — | ID tài khoản Nợ của bút toán thuế (reference ENT_HeThongTaiKhoan) `FK` |
| 14 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | Y | — | ID tài khoản Có của bút toán thuế (reference ENT_HeThongTaiKhoan) `FK` |
| 15 | `SoHoaDon` | `so_hoa_don` | `varchar(50)` | Y | — | Số hóa đơn |
| 16 | `NgayHoaDon` | `ngay_hoa_don` | `date` | Y | — | Ngày hóa đơn |
| 17 | `KyHieuHoaDon` | `ky_hieu_hoa_don` | `text` | Y | — | Ký hiệu hóa đơn |
| 18 | `MauSoHoaDonId` | `mau_so_hoa_don_id` | `uuid` | Y | — | ID mẫu số hóa đơn (reference ENT_MauSoHoaDon) `FK` |
| 19 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5 — danh mục mới bỏ entity TinhChatThueGTGT, dùng enum như ldm-MuaHang) |
| 20 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | ID đối tượng của hóa đơn (reference ENT_DoiTuong) `FK` |
| 21 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | Tên đối tượng |
| 22 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | Mã số thuế của đối tượng |

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

**Đối chiếu `ktth_chi_tiet_phieu_ktth_hoa_don` (32 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `phieu_ke_toan_tong_hop_id`, `dien_giai`, `nhom_hhdv_mua_vao` |
| DB có — LDM **không khai** | 4 | `phieu_ktth_id`, `mo_ta`, `nhom_hhdv_mua_vao_id`, `phien_ban` |

