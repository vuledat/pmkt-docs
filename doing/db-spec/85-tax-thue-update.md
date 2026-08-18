# `tax_` — Thuế

> Sinh tự động từ [`ldm-Thue-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-Thue-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**21 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> LDM THUẾ (UPDATE) — thiết kế lại từ đầu theo tài liệu các epic phân hệ Thuế, KHÔNG kế thừa logic ldm-Thue cũ. Nguồn tài liệu (function-breakdown, crud-matrix, UC, SCR, messages, Matrix, Mapping_Entity_ChungTu.md, XML_LDM_Mapping.md của): PMKT-E-07522 Thuế (Thiết lập thông tin khai báo thuế · Đăng ký sử dụng tờ khai · 3 báo cáo: Bảng kê HĐ đầu vào / đầu ra / BTH quyết toán thuế GTGT)

**Epic nguồn:** PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ThietLapThongTinThue` | `tax_thiet_lap_thong_tin_thue` | — | C — tạo mới | Cấu hình / thiết lập — kiện UC): KhoiTaoToKhai giữ FK ThietLapThongTinThueId. Khối Đại lý thuế: 8 trường bắt buộc CÓ ĐIỀU KIỆN khi… |
| 2 | `DangKyToKhaiThue` | `tax_dang_ky_to_khai_thue` | — | C — tạo mới | Cấu hình / thiết lập — đã lập giữ kỳ cũ (BR03) → KhoiTaoToKhai tự mang kỳ riêng, không FK động. Tập kỳ hợp lệ theo mã tờ khai: 01/GTGT · 02/GTGT ·… |
| 3 | `KhoiTaoToKhai` | `tax_khoi_tao_to_khai` | — | C — tạo mới | Bảng nghiệp vụ — và xác định [22] = [43] tờ khai kỳ liền trước. Chuẩn hóa tên field CQT nộp: dùng ChiCucThueNopToKhaiId / CoQuanThueNopToKhaiId… |
| 4 | `ToKhaiThue01GTGT` | `tax_to_khai_thue_01_gtgt` | `tax_to_khai_thue_01_gtgt` | B — có schema, chưa code | Bảng nghiệp vụ — → cần dấu vết KHBS-đã-kê (KeKhaiVaoToKhaiId trên ToKhaiBoSung01KHBS). [21] checked → zero hóa + khóa [23]–[33],[32a]. Đối… |
| 5 | `BangKeBanRa` | `tax_bang_ke_ban_ra` | — | C — tạo mới | Đầu chứng từ — 5 nhóm: KCT→[26] · 0%→[29] · 5%→[30]/[31] · 10%(gồm 8%)→[32]/[33] · KhongTinhThue→[32a] (nhóm 5 chỉ tổng hợp, KHÔNG hiển thị… |
| 6 | `BangKeMuaVao` | `tax_bang_ke_mua_vao` | — | C — tạo mới | Đầu chứng từ — HienThiNhom4... = true. Tổng hợp: Σ[6]→[23] · Σ[6] nhập khẩu→[23a] · Σ[7]→[24] · Σ[7] nhập khẩu→[24a] · Σ[7] tính chất… |
| 7 | `PhuLucGiamThue` | `tax_phu_luc_giam_thue` | — | C — tạo mới | Bảng nghiệp vụ — Chỉ chọn được với kỳ từ 07/2024 (tháng) / Q3-2024 (quý) trở đi; sau Làm mới → KHÓA [32]/[33] trên tờ khai; xóa phụ lục → mở… |
| 8 | `PhuLucGiamThue_MuaVao` | `tax_phu_luc_giam_thue_mua_vao` | — | C — tạo mới | Liên kết N–N — ⚠ *LDM chưa mô tả bảng này* |
| 9 | `PhuLucGiamThue_BanRa` | `tax_phu_luc_giam_thue_ban_ra` | — | C — tạo mới | Liên kết N–N — ⚠ *LDM chưa mô tả bảng này* |
| 10 | `PhuLuc01_6GTGT` | `tax_phu_luc_01_6_gtgt` | — | C — tạo mới | Liên kết N–N — Chỉ tick được khi NganhNgheKinhDoanh = SXKDThongThuong (BR07); khởi tạo RỖNG. 2 phương pháp: a = round(1%×[14] + 2%×[15]) mỗi… |
| 11 | `PhuLuc01_6GTGT_TheoTinh` | `tax_phu_luc_01_6_gtgt_theo_tinh` | — | C — tạo mới | Liên kết N–N — ⚠ *LDM chưa mô tả bảng này* |
| 12 | `PhuLuc01_6GTGT_ChiTiet` | `tax_phu_luc_01_6_gtgt_chi_tiet` | — | C — tạo mới | Liên kết N–N — ⚠ *LDM chưa mô tả bảng này* |
| 13 | `ToKhaiBoSung01KHBS` | `tax_to_khai_bo_sung_01_khbs` | — | C — tạo mới | Bảng nghiệp vụ — Tổng hợp TKBS (UC 14608) CHỈ tính trên UI; ghi CSDL (TKBS + BGT + PLPB) trong MỘT transaction tại UC_LuuToKhai (BR12). Chênh… |
| 14 | `ToKhaiBoSung01KHBS_PhuLucPhanBo` | `tax_to_khai_bo_sung_01_khbs_phu_luc_phan_bo` | — | C — tạo mới | Liên kết N–N — ⚠ *LDM chưa mô tả bảng này* |
| 15 | `BanGiaiTrinh01_1KHBS` | `tax_to_khai_bo_sung_01_khbs_1_khbs` | — | C — tạo mới | Liên kết N–N — (giải trình TỪNG DÒNG VẬT LÝ, không gộp — khác 01/KHBS A.I.2) → PL Giảm thuế (chỉ dòng TỔNG, cột (7) = 0). Khối không có chênh… |
| 16 | `BanGiaiTrinh01_1KHBS_TaiLieuDinhKem` | `tax_to_khai_bo_sung_01_khbs_1_khbs_tai_lieu_dinh_kem` | — | C — tạo mới | Liên kết N–N — ⚠ *LDM chưa mô tả bảng này* |
| 17 | `ToKhaiThue04GTGT` | `tax_to_khai_thue_04_gtgt` | — | C — tạo mới | Bảng nghiệp vụ — phương pháp sau onboarding (QĐ5). Ràng buộc trùng (BR-12): cùng kỳ + cùng CQT → duy nhất 1 tờ khai HĐKD (tháng/quý) + 1 tờ… |
| 18 | `ChiTietToKhai04GTGT_ChiTieu` | `tax_to_khai_thue_04_gtgt_chi_tieu` | — | C — tạo mới | Liên kết N–N — nhóm ngành nghề (0/1/5/3/2), CHO SỬA TAY, cho số âm; cộng trực tiếp từ bản ghi chi tiết gốc rồi làm tròn (I3). Chỉ tiêu thuế… |
| 19 | `ChiTietToKhai04GTGT_KhoanThuHo` | `tax_to_khai_thue_04_gtgt_khoan_thu_ho` | — | C — tạo mới | Liên kết N–N — ENTITY CHI TIẾT: Khoản thu hộ — Mục B tờ khai 04/GTGT ([33]–[35]) Danh mục Khoản thu hộ (H2): {Chịu thuế GTGT 5% \| Chịu thuế… |
| 20 | `PhuLucGiamThue04GTGT` | `tax_phu_luc_giam_thue_04_gtgt` | — | C — tạo mới | Liên kết N–N — ENTITY: Phụ lục giảm thuế GTGT của tờ khai 04 (Mẫu số 01 — NĐ 174/2025) CHỈ Mục II bán ra (Mục I mua vào 8% không nhập trên tờ… |
| 21 | `ChiTietPhuLucGiamThue04GTGT` | `tax_phu_luc_giam_thue_04_gtgt_chi_tiet` | — | C — tạo mới | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `tax_thiet_lap_thong_tin_thue`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThietLapThongTinThue` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | kiện UC): KhoiTaoToKhai giữ FK ThietLapThongTinThueId. · Khối Đại lý thuế: 8 trường bắt buộc CÓ ĐIỀU KIỆN khi HienThiThongTinDaiLy = true · (MSG_105/107/111–116); phân cấp danh mục 3 cấp Tỉnh → (Xã, CCT) → CQT, đổi cha · reset con (BR3). |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng con | `tax_khoi_tao_to_khai` · `tax_to_khai_thue_04_gtgt` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TinhThanhPhoId` | `tinh_thanh_pho_id` | `uuid` | N | — | **[Địa bàn hoạt động và cơ quan thuế]** ID tỉnh/thành phố (reference đến ENT_TinhThanhPho) `FK` |
| 2 | `XaPhuongId` | `xa_phuong_id` | `uuid` | N | — | **[Địa bàn hoạt động và cơ quan thuế]** ID xã/phường/đặc khu (reference đến ENT_PhuongXa) `FK` |
| 3 | `ChiCucThueKhuVucId` | `chi_cuc_thue_khu_vuc_id` | `uuid` | N | — | **[Địa bàn hoạt động và cơ quan thuế]** ID thuế tỉnh/chi cục thuế khu vực (reference đến ENT_ChiCucThue) `FK` |
| 4 | `CoQuanThueQuanLyId` | `co_quan_thue_quan_ly_id` | `uuid` | N | — | **[Địa bàn hoạt động và cơ quan thuế]** ID cơ quan thuế quản lý (reference đến ENT_CoQuanThue). Nguồn <maCQTNoiNop> XML khi NganhNgheKinhDoanh = SXKDThongThuong `FK` |
| 5 | `MaSoThueDaiLy` | `ma_so_thue_dai_ly` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Mã số thuế đại lý |
| 6 | `TenDaiLyThue` | `ten_dai_ly_thue` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Tên đại lý thuế |
| 7 | `DiaChiDaiLy` | `dia_chi_dai_ly` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Địa chỉ đại lý |
| 8 | `TinhThanhPhoDaiLyId` | `tinh_thanh_pho_dai_ly_id` | `uuid` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** ID tỉnh/TP của đại lý (reference đến ENT_TinhThanhPho) `FK` |
| 9 | `XaPhuongDaiLyId` | `xa_phuong_dai_ly_id` | `uuid` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** ID xã/phường của đại lý (reference đến ENT_PhuongXa) `FK` |
| 10 | `DienThoaiDaiLy` | `dien_thoai_dai_ly` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Điện thoại đại lý |
| 11 | `EmailDaiLy` | `email_dai_ly` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Email đại lý |
| 12 | `HopDongSo` | `hop_dong_so` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** [08] Số hợp đồng đại lý |
| 13 | `NgayHopDong` | `ngay_hop_dong` | `date` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Ngày hợp đồng đại lý |
| 14 | `NhanVienDaiLyThue` | `nhan_vien_dai_ly_thue` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Tên nhân viên/người đại diện đại lý thuế |
| 15 | `ChungChiHanhNgheSoDaiLy` | `chung_chi_hanh_nghe_so_dai_ly` | `text` | Y | — | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Số chứng chỉ hành nghề đại lý |
| 16 | `HienThiThongTinDaiLy` | `hien_thi_thong_tin_dai_ly` | `boolean` | Y | `false` | **[Đại lý thuế (chỉ khi HienThiThongTinDaiLy = true)]** Hiển thị thông tin đại lý lên tờ khai |
| 17 | `SoChungChiHanhNgheDVKT` | `so_chung_chi_hanh_nghe_dvkt` | `text` | Y | — | **[Đơn vị cung cấp dịch vụ kế toán]** Số chứng chỉ hành nghề |
| 18 | `TenDonViCungCapDVKT` | `ten_don_vi_cung_cap_dvkt` | `text` | Y | — | **[Đơn vị cung cấp dịch vụ kế toán]** Tên đơn vị cung cấp dịch vụ kế toán |

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

## 2. `tax_dang_ky_to_khai_thue`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DangKyToKhaiThue` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | đã lập giữ kỳ cũ (BR03) → KhoiTaoToKhai tự mang kỳ riêng, không FK động. · Tập kỳ hợp lệ theo mã tờ khai: 01/GTGT · 02/GTGT · 03/GTGT · 04/GTGT (D1 epic · 14792) · 01/TAIN: Tháng/Quý/Không — 05/KK-TNCN: Tháng/Quý/Không — · 05/QTT-TNCN · 03/TNDN: Năm/Không — 01/TTDB: Tháng/Từng lần phát sinh/Không. |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ToKhaiThue` | `to_khai_thue` | `text` CHECK | N | — | (01/GTGT \| 02/GTGT \| 03/GTGT \| 04/GTGT \| 05/KK-TNCN \| 05/QTT-TNCN \| 03/TNDN \| 01/TTDB \| 01/TAIN) |
| 2 | `KyKeKhai` | `ky_ke_khai` | `text` CHECK | N | — | (TheoThang \| TheoQuy \| TheoNam \| TheoTungLanPhatSinh \| Khong). Nguồn <kieuKy> XML |

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

## 3. `tax_khoi_tao_to_khai`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KhoiTaoToKhai` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | và xác định [22] = [43] tờ khai kỳ liền trước. · Chuẩn hóa tên field CQT nộp: dùng ChiCucThueNopToKhaiId / CoQuanThueNopToKhaiId · (SCR_KhoiTaoToKhai); CRUD matrix ghi ThueTinhCCTId / CoQuanThueNoiNopToKhaiId — · cùng một trường (lệch tên tài liệu, đã ghi nhận). |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `tax_thiet_lap_thong_tin_thue` — FK `ON DELETE CASCADE` |
| Bảng con | `tax_to_khai_thue_01_gtgt` · `tax_bang_ke_ban_ra` · `tax_bang_ke_mua_vao` · `tax_phu_luc_giam_thue` · `tax_phu_luc_01_6_gtgt` · `tax_to_khai_bo_sung_01_khbs` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ThietLapThongTinThueId` | `thiet_lap_thong_tin_thue_id` | `uuid` | N | — | ID thiết lập thông tin thuế (snapshot nguồn — reference đến ENT_ThietLapThongTinThue) `FK` |
| 2 | `DangKyToKhaiThueId` | `dang_ky_to_khai_thue_id` | `uuid` | N | — | ID đăng ký tờ khai (reference đến ENT_DangKyToKhaiThue — xác định kiểu kỳ Tháng/Quý) `FK` |
| 3 | `KyTinhThue` | `ky_tinh_thue` | `integer` | N | `0` | **[Kỳ & ngành nghề]** Kỳ tính thuế (1-12 theo tháng / 1-4 theo quý) |
| 4 | `NamTinhThue` | `nam_tinh_thue` | `integer` | N | `0` | **[Kỳ & ngành nghề]** Năm tính thuế |
| 5 | `NganhNgheKinhDoanh` | `nganh_nghe_kinh_doanh` | `text` CHECK | N | — | **[Kỳ & ngành nghề]** (SXKDThongThuong \| ThamDoKhaiThacDauKhi \| XoSoKienThiet \| DuAnDauTuCSHTKhacTinh \| NhaMayDienKhacTinh). Mapping tiểu mục hạch toán: SXKD/CSHT/điện → 1701; dầu khí → 1704; xổ số → 1705 |
| 6 | `TinhThanhPhoId` | `tinh_thanh_pho_id` | `uuid` | Y | — | **[Địa bàn nộp (chỉ với ngành nghề khác địa bàn tỉnh trụ sở)]** ID tỉnh/TP nơi nộp (reference đến ENT_TinhThanhPho) `FK` |
| 7 | `XaPhuongDacKhuId` | `xa_phuong_dac_khu_id` | `uuid` | Y | — | **[Địa bàn nộp (chỉ với ngành nghề khác địa bàn tỉnh trụ sở)]** ID xã/phường/đặc khu nơi nộp (reference đến ENT_PhuongXa) `FK` |
| 8 | `ChiCucThueNopToKhaiId` | `chi_cuc_thue_nop_to_khai_id` | `uuid` | Y | — | **[Địa bàn nộp (chỉ với ngành nghề khác địa bàn tỉnh trụ sở)]** ID thuế tỉnh/CCT nơi nộp (reference đến ENT_ChiCucThue) `FK` |
| 9 | `CoQuanThueNopToKhaiId` | `co_quan_thue_nop_to_khai_id` | `uuid` | Y | — | **[Địa bàn nộp (chỉ với ngành nghề khác địa bàn tỉnh trụ sở)]** ID CQT nơi nộp tờ khai (reference đến ENT_CoQuanThue). Nguồn <maCQTNoiNop> XML với ngành nghề khác địa bàn `FK` |
| 10 | `LanDau` | `lan_dau` | `boolean` | N | `false` | **[Loại tờ khai]** true: tờ khai lần đầu (XML loaiTKhai = C); false: bổ sung (= B) |
| 11 | `LanBoSung` | `lan_bo_sung` | `numeric(18,4)` ⚠ | Y | `0` | **[Loại tờ khai]** Lần bổ sung thứ n |
| 12 | `NgayLapToKhaiBoSung` | `ngay_lap_to_khai_bo_sung` | `date` | Y | — | **[Loại tờ khai]** Ngày lập tờ khai bổ sung |
| 13 | `MaGiaoDichDienTu` | `ma_giao_dich_dien_tu` | `text` | Y | — | **[Loại tờ khai]** [02] Mã giao dịch điện tử (tờ 01/KHBS) |
| 14 | `HanNopToKhaiChinhThuc` | `han_nop_to_khai_chinh_thuc` | `date` | Y | — | **[Loại tờ khai]** Hạn nộp tờ khai chính thức |
| 15 | `TenDonViPhuThuoc` | `ten_don_vi_phu_thuoc` | `text` | Y | — | **[Đơn vị phụ thuộc / địa điểm KD khác tỉnh (chỉ tiêu [09]–[11c])]** [09] Tên đơn vị phụ thuộc/địa điểm KD khác tỉnh trụ sở |
| 16 | `MaSoThueDonViPhuThuoc` | `ma_so_thue_don_vi_phu_thuoc` | `text` | Y | — | **[Đơn vị phụ thuộc / địa điểm KD khác tỉnh (chỉ tiêu [09]–[11c])]** [10] MST ĐVPT (13 số) hoặc mã ĐĐKD (5 số) |
| 17 | `DiaChiDonViPhuThuoc` | `dia_chi_don_vi_phu_thuoc` | `text` | Y | — | **[Đơn vị phụ thuộc / địa điểm KD khác tỉnh (chỉ tiêu [09]–[11c])]** [11] Địa chỉ nơi có hoạt động SXKD khác tỉnh |
| 18 | `XaPhuongDonViPhuThuocId` | `xa_phuong_don_vi_phu_thuoc_id` | `uuid` | Y | — | **[Đơn vị phụ thuộc / địa điểm KD khác tỉnh (chỉ tiêu [09]–[11c])]** [11a] Xã/phường/đặc khu (reference đến ENT_PhuongXa) `FK` |
| 19 | `TinhThanhPhoDonViPhuThuocId` | `tinh_thanh_pho_don_vi_phu_thuoc_id` | `uuid` | Y | — | **[Đơn vị phụ thuộc / địa điểm KD khác tỉnh (chỉ tiêu [09]–[11c])]** [11c] Tỉnh/thành phố (reference đến ENT_TinhThanhPho) `FK` |
| 20 | `HienThiNhom4HangHoaDichVuKhongDuDieuKienKhauTru` | `hien_thi_nhom_4_hang_hoa_dich_vu_khong_du_dieu_kien_khau_tru` | `boolean` | Y | `false` | **[Tùy chọn hiển thị/tổng hợp]** Hiển thị tính chất 4 (HHDV không đủ ĐK khấu trừ) trên bảng kê mua vào |
| 21 | `CongGopDongHoaDonMuaVaoTrungNhau` | `cong_gop_dong_hoa_don_mua_vao_trung_nhau` | `boolean` | Y | `false` | **[Tùy chọn hiển thị/tổng hợp]** Cộng gộp dòng hóa đơn mua vào trùng nhau |
| 22 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Trạng thái nộp]** (ChuaNop \| DaNopCQT \| CQTChapNhan) |

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

## 4. `tax_to_khai_thue_01_gtgt`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ToKhaiThue01GTGT` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `tax_to_khai_thue_01_gtgt` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | → cần dấu vết KHBS-đã-kê (KeKhaiVaoToKhaiId trên ToKhaiBoSung01KHBS). · [21] checked → zero hóa + khóa [23]–[33],[32a]. · Đối chiếu khi Lưu: có PL giảm thuế → [33] = [32]×10% − PhuLucGiamThue.TongThue · DuocGiam (MSG_202); không PL → [33] vs [32]×10% (MSG_210). |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `tax_khoi_tao_to_khai` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoiTaoToKhaiId` | `khoi_tao_to_khai_id` | `uuid` | N | — | ID khởi tạo tờ khai (reference đến ENT_KhoiTaoToKhai — 1-1) `FK` `UNIQUE` |
| 2 | `ToKhaiKyTruocId` | `to_khai_ky_truoc_id` | `uuid` | Y | — | ID tờ khai kỳ liền trước (self-reference — nguồn chỉ tiêu [22]) `FK` |
| 3 | `KhongPhatSinhHoatDongTrongKy` | `khong_phat_sinh_hoat_dong_trong_ky` | `boolean` | Y | `false` | [21] Không phát sinh hoạt động mua bán trong kỳ (ct21: 0/1) |
| 4 | `ThueGTGTKyTruoc` | `thue_gtgt_ky_truoc` | `money_foreign` ≈ | Y | `0` | **[Khấu trừ kỳ trước]** [22] Thuế GTGT còn được khấu trừ kỳ trước chuyển sang (ct22) |
| 5 | `GiaTriHangMuaVao` | `gia_tri_hang_mua_vao` | `money_foreign` ≈ | Y | `0` | **[Mua vào (nguồn BangKeMuaVao)]** [23] Giá trị HHDV mua vào chưa thuế (ct23) |
| 6 | `GiaTriHangNhapKhau` | `gia_tri_hang_nhap_khau` | `money_foreign` ≈ | Y | `0` | **[Mua vào (nguồn BangKeMuaVao)]** [23a] Trong đó: giá trị HHDV nhập khẩu (ct23a) |
| 7 | `ThueGTGTHangMuaVao` | `thue_gtgt_hang_mua_vao` | `money_foreign` ≈ | Y | `0` | **[Mua vào (nguồn BangKeMuaVao)]** [24] Thuế GTGT của HHDV mua vào (ct24) |
| 8 | `ThueGTGTHangNhapKhau` | `thue_gtgt_hang_nhap_khau` | `money_foreign` ≈ | Y | `0` | **[Mua vào (nguồn BangKeMuaVao)]** [24a] Trong đó: thuế GTGT hàng nhập khẩu (ct24a) |
| 9 | `ThueGTGTHangMuaVaoDuocKhauTru` | `thue_gtgt_hang_mua_vao_duoc_khau_tru` | `money_foreign` ≈ | Y | `0` | **[Mua vào (nguồn BangKeMuaVao)]** [25] Thuế GTGT mua vào được khấu trừ kỳ này (ct25) |
| 10 | `GiaTriHangBanRaKCT` | `gia_tri_hang_ban_ra_kct` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [26] Doanh thu HHDV không chịu thuế GTGT (ct26) |
| 11 | `GiaTriHangBanRaChiuThue` | `gia_tri_hang_ban_ra_chiu_thue` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [27] Tổng doanh thu bán ra chịu thuế = [29]+[30]+[32]+[32a] (ct27) |
| 12 | `ThueGTGTHangBanRaChiuThue` | `thue_gtgt_hang_ban_ra_chiu_thue` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [28] Tổng thuế GTGT phát sinh = [31]+[33] (ct28) |
| 13 | `GiaTriHangBanRaThue0` | `gia_tri_hang_ban_ra_thue_0` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [29] Doanh thu chịu thuế suất 0% (ct29) |
| 14 | `GiaTriHangBanRaThue5` | `gia_tri_hang_ban_ra_thue_5` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [30] Doanh thu chịu thuế suất 5% (ct30) |
| 15 | `ThueGTGTHangBanRaThue5` | `thue_gtgt_hang_ban_ra_thue_5` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [31] Thuế GTGT 5% (ct31) |
| 16 | `GiaTriHangBanRaThue10` | `gia_tri_hang_ban_ra_thue_10` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [32] Doanh thu chịu thuế suất 10% (ct32) |
| 17 | `ThueGTGTHangBanRaThue10` | `thue_gtgt_hang_ban_ra_thue_10` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [33] Thuế GTGT 10% (ct33) |
| 18 | `GiaTriHangBanRaKKKNT` | `gia_tri_hang_ban_ra_kkknt` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [32a] HHDV bán ra không tính thuế (ct32a) |
| 19 | `TongDoanhThuHangBanRa` | `tong_doanh_thu_hang_ban_ra` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [34] Tổng doanh thu bán ra = [26]+[27] (ct34) |
| 20 | `TongThueGTGTHangBanRa` | `tong_thue_gtgt_hang_ban_ra` | `money_foreign` ≈ | Y | `0` | **[Bán ra (nguồn BangKeBanRa)]** [35] Tổng thuế GTGT phát sinh = [28] (ct35) |
| 21 | `ThueGTGTPhatSinhTrongKy` | `thue_gtgt_phat_sinh_trong_ky` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [36] = [35] − [25] (ct36) |
| 22 | `ThueGTGTDieuChinhGiam` | `thue_gtgt_dieu_chinh_giam` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [37] Điều chỉnh giảm thuế khấu trừ kỳ trước (ct37) |
| 23 | `ThueGTGTDieuChinhTang` | `thue_gtgt_dieu_chinh_tang` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [38] Điều chỉnh tăng thuế khấu trừ kỳ trước (ct38) |
| 24 | `ThueGTGTNhanBanGiaoDuocKhauTru` | `thue_gtgt_nhan_ban_giao_duoc_khau_tru` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [39a] Thuế GTGT nhận bàn giao được khấu trừ (ct39a) |
| 25 | `ThueGTGTPhaiNopSXKD` | `thue_gtgt_phai_nop_sxkd` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [40a] Thuế phải nộp của HĐSXKD = MAX(0, [36]−[22]+[37]−[38]−[39a]) (ct40a) |
| 26 | `ThueGTGTMuaVaoDuAnDauTu` | `thue_gtgt_mua_vao_du_an_dau_tu` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [40b] Thuế mua vào dự án đầu tư được bù trừ (ct40b) |
| 27 | `ThuePhaiNop` | `thue_phai_nop` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [40] Số thuế GTGT phải nộp = [40a] − [40b] (ct40) |
| 28 | `ThueGTGTChuaKhauTru` | `thue_gtgt_chua_khau_tru` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [41] Thuế chưa khấu trừ hết = MAX(0, −([36]−[22]+[37]−[38]−[39a])) (ct41) |
| 29 | `ThueGTGTDeNghiHoan` | `thue_gtgt_de_nghi_hoan` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [42] Thuế đề nghị hoàn = [42a]+[42b] (ct42) |
| 30 | `ThueGTGTDeNghiHoan1331` | `thue_gtgt_de_nghi_hoan_1331` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [42a] Đề nghị hoàn TK 1331 |
| 31 | `ThueGTGTDeNghiHoan1332` | `thue_gtgt_de_nghi_hoan_1332` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [42b] Đề nghị hoàn TK 1332 |
| 32 | `ThueGTGTChuyenKySau` | `thue_gtgt_chuyen_ky_sau` | `money_foreign` ≈ | Y | `0` | **[Xác định nghĩa vụ]** [43] Còn được khấu trừ chuyển kỳ sau = [41] − [42] (ct43) |
| 33 | `NguoiKy` | `nguoi_ky` | `text` | N | — | **[Người ký]** Người ký (<nguoiKy> XML) |
| 34 | `NgayKy` | `ngay_ky` | `date` | N | — | **[Người ký]** Ngày ký |

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

**Đối chiếu `tax_to_khai_thue_01_gtgt` (11 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 34 | `khoi_tao_to_khai_id`, `to_khai_ky_truoc_id`, `khong_phat_sinh_hoat_dong_trong_ky`, `thue_gtgt_ky_truoc`, `gia_tri_hang_mua_vao`, `gia_tri_hang_nhap_khau`, `thue_gtgt_hang_mua_vao`, `thue_gtgt_hang_nhap_khau`, `thue_gtgt_hang_mua_vao_duoc_khau_tru`, `gia_tri_hang_ban_ra_kct`, `gia_tri_hang_ban_ra_chiu_thue`, `thue_gtgt_hang_ban_ra_chiu_thue`, `gia_tri_hang_ban_ra_thue_0`, `gia_tri_hang_ban_ra_thue_5`, `thue_gtgt_hang_ban_ra_thue_5`, `gia_tri_hang_ban_ra_thue_10`, `thue_gtgt_hang_ban_ra_thue_10`, `gia_tri_hang_ban_ra_kkknt`, `tong_doanh_thu_hang_ban_ra`, `tong_thue_gtgt_hang_ban_ra`, `thue_gtgt_phat_sinh_trong_ky`, `thue_gtgt_dieu_chinh_giam`, `thue_gtgt_dieu_chinh_tang`, `thue_gtgt_nhan_ban_giao_duoc_khau_tru`, `thue_gtgt_phai_nop_sxkd`, `thue_gtgt_mua_vao_du_an_dau_tu`, `thue_phai_nop`, `thue_gtgt_chua_khau_tru`, `thue_gtgt_de_nghi_hoan`, `thue_gtgt_de_nghi_hoan_1331`, `thue_gtgt_de_nghi_hoan_1332`, `thue_gtgt_chuyen_ky_sau`, `nguoi_ky`, `ngay_ky` |
| DB có — LDM **không khai** | 4 | `ma`, `ten`, `trang_thai`, `phien_ban` |

---

## 5. `tax_bang_ke_ban_ra`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BangKeBanRa` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 5 nhóm: KCT→[26] · 0%→[29] · 5%→[30]/[31] · 10%(gồm 8%)→[32]/[33] · · KhongTinhThue→[32a] (nhóm 5 chỉ tổng hợp, KHÔNG hiển thị trên bảng kê). · Nguồn dòng: 3 popup chọn HĐ (trong kỳ / kỳ sau / điều chỉnh khác kỳ) + nhập · tay; mỗi popup khi Xác nhận chỉ đồng bộ dòng do chính nó tạo. |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `tax_khoi_tao_to_khai` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoiTaoToKhaiId` | `khoi_tao_to_khai_id` | `uuid` | N | — | ID khởi tạo tờ khai (reference đến ENT_KhoiTaoToKhai) `FK` |
| 2 | `HoaDonId` | `hoa_don_id` | `uuid` | Y | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** ID hóa đơn nguồn (ENT_HoaDonBanHang \| ENT_DieuChinhHoaDonBanHang \| ENT_HoaDonMua (NguonTraLai) \| ENT_HoaDonDieuChinh \| ENT_PhieuKeToanTongHop \| ENT_PhieuChi — theo Mapping_Entity_ChungTu) |
| 3 | `ChiTietHoaDonId` | `chi_tiet_hoa_don_id` | `uuid` | Y | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** ID dòng chi tiết nguồn (ENT_ChiTietHoaDonBanHang \| ENT_ChiTietHoaDonDieuChinh \| ENT_ChiTietHoaDon \| ENT_ChiTietChungTuTraLaiHangMua \| ENT_ChiTietPhieuKTTH_HoaDon \| ENT_ChiTietBangKeHoaDon) |
| 4 | `NguonGocDong` | `nguon_goc_dong` | `text` CHECK | N | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** (ChonHDTrongKy \| ChonHDKySau \| ChonHDDieuChinhKhacKy \| ChonHDKhongTinhThue \| NhapTay) |
| 5 | `NhomThueSuat` | `nhom_thue_suat` | `text` CHECK | N | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** (KhongChiuThue \| ThueSuat0 \| ThueSuat5 \| ThueSuat10 \| KhongTinhThue) — nhóm phân bổ lên chỉ tiêu tờ khai: KCT→[26] · 0%→[29] · 5%→[30]/[31] · 10%→[32]/[33] · KKKNT→[32a] |
| 6 | `SoHoaDon` | `so_hoa_don` | `varchar(50)` | N | — | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [2] Số hóa đơn |
| 7 | `NgayHoaDon` | `ngay_hoa_don` | `date` | N | — | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [3] Ngày lập hóa đơn |
| 8 | `TenNguoiMua` | `ten_nguoi_mua` | `text` | N | — | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [4] Tên người mua |
| 9 | `MaSoThueNguoiMua` | `ma_so_thue_nguoi_mua` | `text` | Y | — | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [5] MST người mua |
| 10 | `GiaTriHangBanRa` | `gia_tri_hang_ban_ra` | `money_foreign` ≈ | N | `0` | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [6] Doanh thu chưa có thuế GTGT |
| 11 | `ThueGTGTHangBanRa` | `thue_gtgt_hang_ban_ra` | `money_foreign` ≈ | N | `0` | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [7] Thuế GTGT = [6] × thuế suất của NhomThueSuat |
| 12 | `GhiChu` | `ghi_chu` | `text` | Y | — | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [8] Ghi chú |
| 13 | `TrangThai` | `trang_thai` | `text` CHECK | Y | — | **[Thông tin hiển thị (denormalized theo nguồn / nhập tay)]** [9] (HoaDonMoi \| HoaDonBiDieuChinh \| HoaDonDieuChinh) |

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

## 6. `tax_bang_ke_mua_vao`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BangKeMuaVao` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | HienThiNhom4... = true. Tổng hợp: Σ[6]→[23] · Σ[6] nhập khẩu→[23a] · · Σ[7]→[24] · Σ[7] nhập khẩu→[24a] · Σ[7] tính chất 1,2,3→[25]. · Điều kiện load: NgayHoaDon VÀ NgayHachToan ≤ ngày cuối kỳ; có Số HĐ + Ngày HĐ; · DaKeKhai = false; KhongTongHopToKhaiGTGT = false; nhóm HHDV mua vào ∈ {1,2,4}. |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `tax_khoi_tao_to_khai` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoiTaoToKhaiId` | `khoi_tao_to_khai_id` | `uuid` | N | — | ID khởi tạo tờ khai (reference đến ENT_KhoiTaoToKhai) `FK` |
| 2 | `HoaDonId` | `hoa_don_id` | `uuid` | Y | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** ID hóa đơn nguồn (ENT_HoaDonMua \| ENT_HoaDonDieuChinh \| ENT_HoaDonBanHang (trả lại hàng mua người mua xuất) \| ENT_DieuChinhHoaDonBanHang \| ENT_PhieuKeToanTongHop \| ENT_PhieuChi) |
| 3 | `ChiTietHoaDonId` | `chi_tiet_hoa_don_id` | `uuid` | Y | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** ID dòng chi tiết nguồn (ENT_ChiTietHoaDon \| ENT_ChiTietChungTuTraLaiHangMua \| ENT_ChiTietChungTuDieuChinhGiaHangMua \| ENT_ChiTietHoaDonBanHang \| ENT_ChiTietHoaDonDieuChinh \| ENT_ChiTietPhieuKTTH_HoaDon \| ENT_ChiTietBangKeHoaDon) |
| 4 | `NguonGocDong` | `nguon_goc_dong` | `text` CHECK | N | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** (ChonHDTrongKy \| ChonHDDieuChinhKhacKy \| NhapTay) |
| 5 | `TinhChatThue` | `tinh_chat_thue` | `text` CHECK | N | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** (TC1_DungRiengSXKDChiuThue \| TC2_DungChung \| TC3_DuAnDauTu \| TC4_KhongDuDieuKienKhauTru) — nguồn tính [25] gồm tính chất 1, 2, 3 |
| 6 | `SoHoaDon` | `so_hoa_don` | `varchar(50)` | N | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [2] Số hóa đơn |
| 7 | `NgayHoaDon` | `ngay_hoa_don` | `date` | N | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [3] Ngày lập hóa đơn |
| 8 | `TenNguoiBan` | `ten_nguoi_ban` | `text` | N | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [4] Tên người bán |
| 9 | `MaSoThueNguoiBan` | `ma_so_thue_nguoi_ban` | `text` | Y | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [5] MST người bán |
| 10 | `GiaTriHangMuaVao` | `gia_tri_hang_mua_vao` | `money_foreign` ≈ | Y | `0` | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [6] Giá trị HHDV mua vào chưa thuế |
| 11 | `ThueGTGTHangMuaVao` | `thue_gtgt_hang_mua_vao` | `money_foreign` ≈ | Y | `0` | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [7] Thuế GTGT |
| 12 | `LaChungTuNhapKhau` | `la_chung_tu_nhap_khau` | `boolean` | Y | `false` | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [8] Là chứng từ nhập khẩu HHDV — nguồn [23a]/[24a] |
| 13 | `GhiChu` | `ghi_chu` | `text` | Y | — | **[Nguồn dòng (đa hình — NULL với dòng nhập tay)]** [9] Ghi chú |

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

## 7. `tax_phu_luc_giam_thue`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuLucGiamThue` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chỉ chọn được với kỳ từ 07/2024 (tháng) / Q3-2024 (quý) trở đi; sau Làm mới → · KHÓA [32]/[33] trên tờ khai; xóa phụ lục → mở khóa, [33] = [32] × 10%. · Gom dòng chi tiết 8% theo TÊN HHDV, sắp tăng dần; loại trừ dòng nhập tay bảng kê. · Đối chiếu [33] dùng TongThueDuocGiam (KHÔNG dùng ChenhLechThuePhaiNop [08]). |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `tax_khoi_tao_to_khai` — FK `ON DELETE CASCADE` |
| Bảng con | `tax_phu_luc_giam_thue_mua_vao` · `tax_phu_luc_giam_thue_ban_ra` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoiTaoToKhaiId` | `khoi_tao_to_khai_id` | `uuid` | N | — | ID khởi tạo tờ khai (1-0..1) `FK` `UNIQUE` |
| 2 | `TongGiaTriChuaThueMuaVao` | `tong_gia_tri_chua_thue_mua_vao` | `money_foreign` ≈ | Y | `0` | Tổng [3] Mục I — giá trị mua vào 8% chưa thuế |
| 3 | `TongThueGTGTMuaVao` | `tong_thue_gtgt_mua_vao` | `money_foreign` ≈ | Y | `0` | Tổng [4] Mục I — thuế GTGT mua vào được khấu trừ |
| 4 | `TongDoanhThuBanRa` | `tong_doanh_thu_ban_ra` | `money_foreign` ≈ | Y | `0` | Tổng [3] Mục II — doanh thu bán ra được giảm |
| 5 | `TongThueDuocGiam` | `tong_thue_duoc_giam` | `money_foreign` ≈ | Y | `0` | Tổng [6] Mục II — thuế GTGT được giảm |
| 6 | `ChenhLechThuePhaiNop` | `chenh_lech_thue_phai_nop` | `money_foreign` ≈ | Y | `0` | [08] Mục III = TongThueDuocGiam − TongThueGTGTMuaVao (XML ct9) |

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

## 8. `tax_phu_luc_giam_thue_mua_vao`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuLucGiamThue_MuaVao` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_phu_luc_giam_thue` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuLucGiamThueId` | `phu_luc_giam_thue_id` | `uuid` | N | — | ID phụ lục giảm thuế (reference đến ENT_PhuLucGiamThue) `FK` |
| 2 | `TenHangMuaVao` | `ten_hang_mua_vao` | `text` | Y | — | [2] Tên hàng hóa dịch vụ mua vào |
| 3 | `GiaTriChuaThueMuaVao` | `gia_tri_chua_thue_mua_vao` | `money_foreign` ≈ | Y | `0` | [3] Giá trị mua vào chưa thuế được khấu trừ trong kỳ |
| 4 | `ThueGTGTMuaVao` | `thue_gtgt_mua_vao` | `money_foreign` ≈ | Y | `0` | [4] Thuế GTGT mua vào được khấu trừ = [3] × 8% |

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

## 9. `tax_phu_luc_giam_thue_ban_ra`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuLucGiamThue_BanRa` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_phu_luc_giam_thue` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuLucGiamThueId` | `phu_luc_giam_thue_id` | `uuid` | N | — | ID phụ lục giảm thuế (reference đến ENT_PhuLucGiamThue) `FK` |
| 2 | `TenHangBanRa` | `ten_hang_ban_ra` | `text` | N | — | [2] Tên hàng hóa dịch vụ bán ra |
| 3 | `GiaTriChuaThueBanRa` | `gia_tri_chua_thue_ban_ra` | `money_foreign` ≈ | N | `0` | [3] Giá trị chưa có thuế GTGT |
| 4 | `ThueSuatGoc` | `thue_suat_goc` | `percent_rate` | Y | `0` | [4] Thuế suất theo quy định |
| 5 | `ThueSuatSauGiam` | `thue_suat_sau_giam` | `percent_rate` | Y | `0` | [5] Thuế suất sau giảm |
| 6 | `ThueDuocGiam` | `thue_duoc_giam` | `money_foreign` ≈ | Y | `0` | [6] Thuế GTGT được giảm = [3] × ([4] − [5]) |

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

## 10. `tax_phu_luc_01_6_gtgt`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuLuc01_6GTGT` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chỉ tick được khi NganhNgheKinhDoanh = SXKDThongThuong (BR07); khởi tạo RỖNG. · 2 phương pháp: a = round(1%×[14] + 2%×[15]) mỗi dòng; Σa ≤ [06] → PP1 dùng · [17]/[18]/[19]/[20] (nhóm THK = 0); Σa > [06] → PP2 dùng [21]=round([06]×[16]/[07]). · [11] Quận/Huyện: disable, KHÔNG lưu. |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_khoi_tao_to_khai` — FK `ON DELETE CASCADE` |
| Bảng con | `tax_phu_luc_01_6_gtgt_theo_tinh` · `tax_phu_luc_01_6_gtgt_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoiTaoToKhaiId` | `khoi_tao_to_khai_id` | `uuid` | N | — | ID khởi tạo tờ khai (1-0..1) `FK` `UNIQUE` |
| 2 | `HoatDongPhanBo` | `hoat_dong_phan_bo` | `text` | Y | — | [01a] Hoạt động phân bổ |
| 3 | `SoThuePhaiNop` | `so_thue_phai_nop` | `money_foreign` ≈ | N | `0` | [06] Số thuế phải nộp của CSSX |
| 4 | `TongDoanhThuChuaThue` | `tong_doanh_thu_chua_thue` | `money_foreign` ≈ | N | `0` | [07] Tổng doanh thu chưa thuế của sản phẩm sản xuất |
| 5 | `SoThuePhaiNopTheoCacTinh` | `so_thue_phai_nop_theo_cac_tinh` | `money_foreign` ≈ | Y | `0` | [19] = Σ[17] (PP1) |
| 6 | `SoThuePhaiNopNoiDongTruSoChinh` | `so_thue_phai_nop_noi_dong_tru_so_chinh` | `money_foreign` ≈ | Y | `0` | [20] = [06] − [19] (PP1) |
| 7 | `SoThuePhaiNopTheoCacTinhTHK` | `so_thue_phai_nop_theo_cac_tinh_thk` | `money_foreign` ≈ | Y | `0` | [23] = Σ[21] (PP2 — XML ct23) |
| 8 | `SoThuePhaiNopNoiDongTruSoChinhTHK` | `so_thue_phai_nop_noi_dong_tru_so_chinh_thk` | `money_foreign` ≈ | Y | `0` | [24] = [06] − [23] (PP2 — XML ct24) |

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

## 11. `tax_phu_luc_01_6_gtgt_theo_tinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuLuc01_6GTGT_TheoTinh` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_phu_luc_01_6_gtgt` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuLuc01_6GTGTId` | `phu_luc_01_6_gtgt_id` | `uuid` | N | — | ID phụ lục (reference đến ENT_PhuLuc01_6GTGT) `FK` |
| 2 | `TinhThanhPhoId` | `tinh_thanh_pho_id` | `uuid` | N | — | ID tỉnh/TP (reference đến ENT_TinhThanhPho) `FK` |
| 3 | `SoThuePhaiNopTheoTinh` | `so_thue_phai_nop_theo_tinh` | `money_foreign` ≈ | Y | `0` | [18] = Σ[17] các dòng cùng tỉnh (XML ct18 + ct18_tinh_ma) |
| 4 | `SoThuePhaiNopTheoTinhTHK` | `so_thue_phai_nop_theo_tinh_thk` | `money_foreign` ≈ | Y | `0` | [22] = Σ[21] các dòng cùng tỉnh (XML ct22) |

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

## 12. `tax_phu_luc_01_6_gtgt_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuLuc01_6GTGT_ChiTiet` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_phu_luc_01_6_gtgt` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuLuc01_6GTGTId` | `phu_luc_01_6_gtgt_id` | `uuid` | N | — | ID phụ lục (reference đến ENT_PhuLuc01_6GTGT) `FK` |
| 2 | `PhuLuc01_6GTGT_TheoTinhId` | `phu_luc_01_6_gtgt_theo_tinh_id` | `uuid` | N | — | ID dòng tổng theo tỉnh (reference đến ENT_PhuLuc01_6GTGT_TheoTinh) `FK` |
| 3 | `ChiTieu` | `chi_tieu` | `text` | N | — | [09] Chỉ tiêu (tên CSSX) |
| 4 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | [10] MST 10/13 số hoặc mã ĐĐKD 5 ký tự |
| 5 | `TinhThanhPhoId` | `tinh_thanh_pho_id` | `uuid` | N | — | [12] ID tỉnh/TP (reference đến ENT_TinhThanhPho) `FK` |
| 6 | `XaPhuongId` | `xa_phuong_id` | `uuid` | N | — | Xã/phường/đặc khu (reference đến ENT_PhuongXa — XML ma_xa) `FK` |
| 7 | `ChiCucThueKhuVucId` | `chi_cuc_thue_khu_vuc_id` | `uuid` | N | — | [13a] Chi cục thuế khu vực (reference đến ENT_ChiCucThue) `FK` |
| 8 | `CoQuanThueId` | `co_quan_thue_id` | `uuid` | N | — | [13] CQT trực tiếp quản lý (reference đến ENT_CoQuanThue) `FK` |
| 9 | `DoanhThuHH5` | `doanh_thu_hh_5` | `money_foreign` ≈ | Y | `0` | [14] Doanh thu hàng hóa chịu thuế suất 5% |
| 10 | `DoanhThuHH10` | `doanh_thu_hh_10` | `money_foreign` ≈ | Y | `0` | [15] Doanh thu hàng hóa chịu thuế suất 10% |
| 11 | `TongDoanhThuHH` | `tong_doanh_thu_hh` | `money_foreign` ≈ | Y | `0` | [16] = [14] + [15] (XML ct16) |
| 12 | `SoThuePhaiNop` | `so_thue_phai_nop` | `money_foreign` ≈ | Y | `0` | [17] = 1%×[14] + 2%×[15] (PP1) |
| 13 | `SoThuePhaiNopTHK` | `so_thue_phai_nop_thk` | `money_foreign` ≈ | Y | `0` | [21] = round([06] × [16] / [07]) (PP2 — XML ct21) |

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

## 13. `tax_to_khai_bo_sung_01_khbs`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ToKhaiBoSung01KHBS` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Tổng hợp TKBS (UC 14608) CHỈ tính trên UI; ghi CSDL (TKBS + BGT + PLPB) trong · MỘT transaction tại UC_LuuToKhai (BR12). Chênh lệch khấu trừ của KHBS được kê · vào [37]/[38] của tờ khai kỳ chứa NgayLapToKhaiBoSung — mỗi KHBS chỉ kê 1 lần · (KeKhaiVaoToKhaiId — dấu vết, tài liệu yêu cầu nhưng chưa đặt tên field). |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `tax_khoi_tao_to_khai` — FK `ON DELETE CASCADE` |
| Bảng con | `tax_to_khai_bo_sung_01_khbs_phu_luc_phan_bo` · `tax_to_khai_bo_sung_01_khbs_1_khbs` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoiTaoToKhaiId` | `khoi_tao_to_khai_id` | `uuid` | N | — | ID khởi tạo tờ khai bổ sung (reference đến ENT_KhoiTaoToKhai) `FK` `UNIQUE` |
| 2 | `ToKhaiLanDauId` | `to_khai_lan_dau_id` | `uuid` | Y | — | ID tờ khai lần đầu cùng kỳ (reference đến ENT_ToKhaiThue01GTGT). Nguồn so sánh khi bổ sung lần 1 `FK` |
| 3 | `ToKhaiBoSungLienKeTruocId` | `to_khai_bo_sung_lien_ke_truoc_id` | `uuid` | Y | — | ID tờ khai bổ sung liền kề trước (reference đến ENT_ToKhaiThue01GTGT). Nguồn so sánh khi bổ sung lần n ≥ 2 `FK` |
| 4 | `ToKhaiLienQuanId` | `to_khai_lien_quan_id` | `uuid` | Y | — | ID tờ khai có sai sót được chọn để bổ sung (reference đến ENT_ToKhaiThue01GTGT) `FK` |
| 5 | `KeKhaiVaoToKhaiId` | `ke_khai_vao_to_khai_id` | `uuid` | Y | — | ID tờ khai đã nhận chênh lệch khấu trừ vào [37]/[38] (reference đến ENT_ToKhaiThue01GTGT) `FK` |
| 6 | `MauToKhaiBoSung` | `mau_to_khai_bo_sung` | `text` | Y | — | [01] Mẫu tờ khai bổ sung |
| 7 | `TieuMucDieuChinhSoThuePhaiNop` | `tieu_muc_dieu_chinh_so_thue_phai_nop` | `text` | Y | — | **[A.I Số thuế phải nộp điều chỉnh]** [02] Tiểu mục theo ngành nghề (1701 \| 1704 \| 1705) |
| 8 | `SoThuePhaiNopDieuChinh` | `so_thue_phai_nop_dieu_chinh` | `money_foreign` ≈ | Y | `0` | **[A.I Số thuế phải nộp điều chỉnh]** [03] = [40] tờ khai hiện tại − [40] tờ khai so sánh |
| 9 | `TongSoThuePhaiNopDieuChinh` | `tong_so_thue_phai_nop_dieu_chinh` | `money_foreign` ≈ | Y | `0` | **[A.I Số thuế phải nộp điều chỉnh]** [10] Tổng số thuế phải nộp điều chỉnh |
| 10 | `TongSoThuePhaiNopDieuChinhPLPB` | `tong_so_thue_phai_nop_dieu_chinh_plpb` | `money_foreign` ≈ | Y | `0` | **[A.I Số thuế phải nộp điều chỉnh]** [11] Tổng điều chỉnh theo phụ lục phân bổ CSSX |
| 11 | `SoNgayChamNop` | `so_ngay_cham_nop` | `integer` | Y | `0` | **[A.I.3 Tiền chậm nộp]** [a] Số ngày chậm nộp = NgayLapToKhaiBoSung − hạn nộp |
| 12 | `SoTienChamNopDieuChinh` | `so_tien_cham_nop_dieu_chinh` | `money_foreign` ≈ | Y | `0` | **[A.I.3 Tiền chậm nộp]** [b] = chênh lệch phải nộp tăng × 0.03% × [a] |
| 13 | `TieuMucDieuChinhSoThueDuocKhauTru` | `tieu_muc_dieu_chinh_so_thue_duoc_khau_tru` | `text` | Y | — | **[A.II Khấu trừ điều chỉnh]** Tên tiểu mục điều chỉnh khấu trừ |
| 14 | `SoThueDuocKhauTruDieuChinh` | `so_thue_duoc_khau_tru_dieu_chinh` | `money_foreign` ≈ | Y | `0` | **[A.II Khấu trừ điều chỉnh]** = [43] tờ khai hiện tại − [43] tờ khai so sánh |
| 15 | `TongSoThueDuocKhauTruDieuChinh` | `tong_so_thue_duoc_khau_tru_dieu_chinh` | `money_foreign` ≈ | Y | `0` | **[A.II Khấu trừ điều chỉnh]** [12] Tổng điều chỉnh khấu trừ |
| 16 | `TieuMucDieuChinhSoThueDeNghiHoan` | `tieu_muc_dieu_chinh_so_thue_de_nghi_hoan` | `text` | Y | — | **[A.III Đề nghị hoàn điều chỉnh]** Tên tiểu mục điều chỉnh đề nghị hoàn |
| 17 | `SoThueDeNghiHoanDieuChinh` | `so_thue_de_nghi_hoan_dieu_chinh` | `money_foreign` ≈ | Y | `0` | **[A.III Đề nghị hoàn điều chỉnh]** = [42] tờ khai hiện tại − [42] tờ khai so sánh |
| 18 | `TongSoThueDeNghiHoanDieuChinh` | `tong_so_thue_de_nghi_hoan_dieu_chinh` | `money_foreign` ≈ | Y | `0` | **[A.III Đề nghị hoàn điều chỉnh]** [13] Tổng điều chỉnh đề nghị hoàn |
| 19 | `SoThueThuHoiHoan` | `so_thue_thu_hoi_hoan` | `money_foreign` ≈ | Y | `0` | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** [B.I.1] Số tiền thu hồi hoàn |
| 20 | `SoQuyetDinhHoanThue` | `so_quyet_dinh_hoan_thue` | `text` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** Số quyết định hoàn thuế |
| 21 | `NgayQuyetDinhHoanThue` | `ngay_quyet_dinh_hoan_thue` | `date` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** Ngày quyết định hoàn thuế |
| 22 | `TinhThanhPhoHoanThueId` | `tinh_thanh_pho_hoan_thue_id` | `uuid` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** Tỉnh/TP của CQT hoàn thuế (reference đến ENT_TinhThanhPho) `FK` |
| 23 | `XaPhuongHoanThueId` | `xa_phuong_hoan_thue_id` | `uuid` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** Xã/phường của CQT hoàn thuế (reference đến ENT_PhuongXa) `FK` |
| 24 | `CoQuanThueCapCucHoanThueId` | `co_quan_thue_cap_cuc_hoan_thue_id` | `uuid` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** CQT cấp Cục ra quyết định hoàn (reference đến ENT_CoQuanThue) `FK` |
| 25 | `CoQuanThueCapChiCucHoanThueId` | `co_quan_thue_cap_chi_cuc_hoan_thue_id` | `uuid` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** CQT cấp Chi cục (reference đến ENT_ChiCucThue) `FK` |
| 26 | `SoLenhHoanThue` | `so_lenh_hoan_thue` | `text` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** Số lệnh hoàn thuế |
| 27 | `NgayLenhHoanThue` | `ngay_lenh_hoan_thue` | `date` | Y | — | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** Ngày lệnh hoàn thuế |
| 28 | `SoNgayNhanTienHoanThue` | `so_ngay_nhan_tien_hoan_thue` | `integer` | Y | `0` | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** [B.II.1] Số ngày nhận tiền hoàn = NgayLapToKhaiBoSung − NgayLenhHoanThue |
| 29 | `SoTienChamNop` | `so_tien_cham_nop` | `money_foreign` ≈ | Y | `0` | **[B Thu hồi hoàn + chậm nộp (chỉ khi [13] ≠ 0)]** [B.II.2] = SoThueThuHoiHoan × 0.03% × [B.II.1] (XML ct3b) |

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

## 14. `tax_to_khai_bo_sung_01_khbs_phu_luc_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ToKhaiBoSung01KHBS_PhuLucPhanBo` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_to_khai_bo_sung_01_khbs` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ToKhaiBoSung01KHBSId` | `to_khai_bo_sung_01_khbs_id` | `uuid` | N | — | ID tờ khai bổ sung (reference đến ENT_ToKhaiBoSung01KHBS) `FK` |
| 2 | `PhuLuc016GTGTChiTietId` | `phu_luc_016_gtgt_chi_tiet_id` | `uuid` | Y | — | ID dòng chi tiết phụ lục CSSX liên quan (reference đến ENT_PhuLuc01_6GTGT_ChiTiet) `FK` |
| 3 | `HoatDongPhanBo` | `hoat_dong_phan_bo` | `text` | Y | — | Hoạt động phân bổ |
| 4 | `TieuMucDieuChinhSoThuePhaiNopPLPB` | `tieu_muc_dieu_chinh_so_thue_phai_nop_plpb` | `text` | Y | — | [02] Tên tiểu mục điều chỉnh |
| 5 | `SoThuePhaiNopDieuChinhPLPB` | `so_thue_phai_nop_dieu_chinh_plpb` | `money_foreign` ≈ | Y | `0` | [07] = ([17]+[21]) tờ khai đang lập − ([17]+[21]) tờ khai so sánh; dòng trụ sở chính = Δ([20]+[24]) |

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

## 15. `tax_to_khai_bo_sung_01_khbs_1_khbs`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BanGiaiTrinh01_1KHBS` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | (giải trình TỪNG DÒNG VẬT LÝ, không gộp — khác 01/KHBS A.I.2) → PL Giảm thuế · (chỉ dòng TỔNG, cột (7) = 0). Khối không có chênh lệch → không hiển thị. · Cột (7) DieuChinhTangGiam chỉ ≠ 0 với [40],[42],[43] và [20],[24] (CSSX). · Tổng hợp lại → xóa toàn bộ Lý do đã nhập (BR23). |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_to_khai_bo_sung_01_khbs` — FK `ON DELETE CASCADE` |
| Bảng con | `tax_to_khai_bo_sung_01_khbs_1_khbs_tai_lieu_dinh_kem` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ToKhaiBoSung01KHBSId` | `to_khai_bo_sung_01_khbs_id` | `uuid` | N | — | ID tờ khai bổ sung (reference đến ENT_ToKhaiBoSung01KHBS) `FK` |
| 2 | `TenChiTieu` | `ten_chi_tieu` | `text` | N | — | (2) Tên chỉ tiêu điều chỉnh / tên HHDV |
| 3 | `MaChiTieu` | `ma_chi_tieu` | `text` | Y | — | (3) Mã số chỉ tiêu (XML ct3_ma) |
| 4 | `SoDaKeKhai` | `so_da_ke_khai` | `numeric(18,4)` ⚠ | Y | `0` | (4) Số đã kê khai (tờ khai so sánh) |
| 5 | `SoDieuChinh` | `so_dieu_chinh` | `numeric(18,4)` ⚠ | Y | `0` | (5) Số điều chỉnh (tờ khai đang lập) |
| 6 | `ChenhLech` | `chenh_lech` | `numeric(18,4)` ⚠ | Y | `0` | (6) = (5) − (4) |
| 7 | `DieuChinhTangGiam` | `dieu_chinh_tang_giam` | `numeric(18,4)` ⚠ | Y | `0` | (7) Điều chỉnh tăng/giảm nghĩa vụ thuế |
| 8 | `LyDo` | `ly_do` | `text` | Y | — | (8) Lý do điều chỉnh |
| 9 | `TongDieuChinhPhaiNop` | `tong_dieu_chinh_phai_nop` | `money_foreign` ≈ | Y | `0` | **[3 dòng tổng của bản giải trình]** [07] = Δ[40] + Δ([17]+[21]+[20]+[24]) PL CSSX |
| 10 | `TongDieuChinhKhauTru` | `tong_dieu_chinh_khau_tru` | `money_foreign` ≈ | Y | `0` | **[3 dòng tổng của bản giải trình]** [08] = Δ[43] (khớp [12] của 01/KHBS) |
| 11 | `TongDieuChinhDeNghiHoan` | `tong_dieu_chinh_de_nghi_hoan` | `money_foreign` ≈ | Y | `0` | **[3 dòng tổng của bản giải trình]** [09] = Δ[42] (khớp [13] của 01/KHBS) |

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

## 16. `tax_to_khai_bo_sung_01_khbs_1_khbs_tai_lieu_dinh_kem`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BanGiaiTrinh01_1KHBS_TaiLieuDinhKem` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_to_khai_bo_sung_01_khbs_1_khbs` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `BanGiaiTrinh01_1KHBSId` | `ban_giai_trinh_01_1_khbs_id` | `uuid` | N | — | ID bản giải trình (reference đến ENT_BanGiaiTrinh01_1KHBS) `FK` |
| 2 | `TaiLieuDinhKem` | `tai_lieu_dinh_kem` | `text` | Y | — | Tên/mô tả tài liệu đính kèm (mục B) |

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

## 17. `tax_to_khai_thue_04_gtgt`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ToKhaiThue04GTGT` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | phương pháp sau onboarding (QĐ5). Ràng buộc trùng (BR-12): cùng kỳ + cùng CQT · → duy nhất 1 tờ khai HĐKD (tháng/quý) + 1 tờ khai thu hộ; theo lần phát sinh · không giới hạn. Trạng thái nộp + KHBS: kế thừa hành vi 01/GTGT (FR-08/FR-09; · số năm khai bổ sung + khoảng hiệu lực phụ lục giảm: THAM SỐ HÓA, không hard-code). |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `tax_thiet_lap_thong_tin_thue` — FK `ON DELETE CASCADE` |
| Bảng con | `tax_to_khai_thue_04_gtgt_chi_tieu` · `tax_to_khai_thue_04_gtgt_khoan_thu_ho` · `tax_phu_luc_giam_thue_04_gtgt` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ThietLapThongTinThueId` | `thiet_lap_thong_tin_thue_id` | `uuid` | Y | — | ID thiết lập thông tin thuế (reference đến ENT_ThietLapThongTinThue — nguồn [04]–[08]) `FK` |
| 2 | `DangKyToKhaiThueId` | `dang_ky_to_khai_thue_id` | `uuid` | Y | — | ID đăng ký tờ khai (reference đến ENT_DangKyToKhaiThue, ToKhaiThue = 04/GTGT) `FK` |
| 3 | `LoaiKy` | `loai_ky` | `text` CHECK | N | — | **[Kỳ tính thuế [01]]** (Thang \| Quy \| TungLanPhatSinh) |
| 4 | `KyTinhThue` | `ky_tinh_thue` | `integer` | Y | `0` | **[Kỳ tính thuế [01]]** Kỳ tính thuế (1-12 theo tháng / 1-4 theo quý) |
| 5 | `NamTinhThue` | `nam_tinh_thue` | `integer` | N | `0` | **[Kỳ tính thuế [01]]** Năm tính thuế |
| 6 | `NgayPhatSinh` | `ngay_phat_sinh` | `date` | Y | — | **[Kỳ tính thuế [01]]** Ngày phát sinh. Chỉ LoaiKy = TungLanPhatSinh |
| 7 | `LanDau` | `lan_dau` | `boolean` | N | `false` | **[Loại khai [02]/[03]]** true: lần đầu; false: bổ sung lần thứ n |
| 8 | `LanBoSung` | `lan_bo_sung` | `numeric(18,4)` ⚠ | Y | `0` | **[Loại khai [02]/[03]]** Lần bổ sung thứ n |
| 9 | `KhaiRiengKhoanThuHo` | `khai_rieng_khoan_thu_ho` | `boolean` | N | `false` | **[Thu hộ]** Khai riêng khoản thu hộ — true → chỉ khai Mục B |
| 10 | `CoQuanThueNopToKhaiId` | `co_quan_thue_nop_to_khai_id` | `uuid` | Y | — | **[CQT nộp + đơn vị phụ thuộc [09]–[11] (chỉ khi CQT nộp khác tỉnh trụ sở)]** ID cơ quan thuế nơi nộp (reference đến ENT_CoQuanThue) `FK` |
| 11 | `TenDonViPhuThuoc` | `ten_don_vi_phu_thuoc` | `text` | Y | — | **[CQT nộp + đơn vị phụ thuộc [09]–[11] (chỉ khi CQT nộp khác tỉnh trụ sở)]** [09] Tên đơn vị phụ thuộc/ĐĐKD khác tỉnh |
| 12 | `MaSoThueDonViPhuThuoc` | `ma_so_thue_don_vi_phu_thuoc` | `text` | Y | — | **[CQT nộp + đơn vị phụ thuộc [09]–[11] (chỉ khi CQT nộp khác tỉnh trụ sở)]** [10] MST 13 số hoặc mã ĐĐKD 5 số |
| 13 | `XaPhuongDonViPhuThuocId` | `xa_phuong_don_vi_phu_thuoc_id` | `uuid` | Y | — | **[CQT nộp + đơn vị phụ thuộc [09]–[11] (chỉ khi CQT nộp khác tỉnh trụ sở)]** [11a] Xã/phường/đặc khu (reference đến ENT_PhuongXa) `FK` |
| 14 | `TinhThanhPhoDonViPhuThuocId` | `tinh_thanh_pho_don_vi_phu_thuoc_id` | `uuid` | Y | — | **[CQT nộp + đơn vị phụ thuộc [09]–[11] (chỉ khi CQT nộp khác tỉnh trụ sở)]** [11c] Tỉnh/TP (reference đến ENT_TinhThanhPho) `FK` |
| 15 | `TongDoanhThuChiuThue` | `tong_doanh_thu_chiu_thue` | `money_foreign` ≈ | Y | `0` | **[Tổng Mục A]** [30] = [22]+[24]+[26]+[28] |
| 16 | `TongThuePhaiNop` | `tong_thue_phai_nop` | `money_foreign` ≈ | Y | `0` | **[Tổng Mục A]** [31] = [23]+[25]+[27]+[29] |
| 17 | `TongDoanhThu` | `tong_doanh_thu` | `money_foreign` ≈ | Y | `0` | **[Tổng Mục A]** [32] = [21]+[30] |
| 18 | `TongDoanhThuThuHo` | `tong_doanh_thu_thu_ho` | `money_foreign` ≈ | Y | `0` | **[Tổng Mục B (thu hộ)]** [36] = Σ[33] |
| 19 | `TongThueThuHo` | `tong_thue_thu_ho` | `money_foreign` ≈ | Y | `0` | **[Tổng Mục B (thu hộ)]** [37] = Σ[35] |
| 20 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Trạng thái]** (ChuaNop \| DaNopCQT \| CQTChapNhan) |
| 21 | `NgayLap` | `ngay_lap` | `date` | N | — | **[Trạng thái]** Ngày lập tờ khai |

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

## 18. `tax_to_khai_thue_04_gtgt_chi_tieu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietToKhai04GTGT_ChiTieu` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | nhóm ngành nghề (0/1/5/3/2), CHO SỬA TAY, cho số âm; cộng trực tiếp từ bản ghi · chi tiết gốc rồi làm tròn (I3). Chỉ tiêu thuế ([23],[25],[27],[29]): KHÓA, · tự tính = doanh thu × tỷ lệ − Σ(6) phụ lục giảm cùng tỷ lệ (BR-03/BR-07). · Ràng buộc: doanh thu ≥ tổng cột (3) phụ lục giảm cùng tỷ lệ (BR-05). |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_to_khai_thue_04_gtgt` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ToKhaiThue04GTGTId` | `to_khai_thue_04_gtgt_id` | `uuid` | N | — | ID tờ khai 04/GTGT (reference đến ENT_ToKhaiThue04GTGT) `FK` |
| 2 | `MaChiTieu` | `ma_chi_tieu` | `text` | N | — | Mã chỉ tiêu ([21]–[29]) |
| 3 | `TyLePhanTram` | `ty_le_phan_tram` | `percent_rate` | Y | `0` | Tỷ lệ % tương ứng (0 \| 1 \| 2 \| 3 \| 5) — khóa phân nhóm chỉ tiêu |
| 4 | `GiaTriHeThong` | `gia_tri_he_thong` | `money_foreign` ≈ | Y | `0` | Giá trị hệ thống tự tổng hợp |
| 5 | `GiaTri` | `gia_tri` | `money_foreign` ≈ | N | `0` | Giá trị hiện hành (= GiaTriHeThong khi chưa sửa tay) |
| 6 | `SuaTay` | `sua_tay` | `boolean` | N | `false` | Cờ người dùng đã sửa tay |

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

## 19. `tax_to_khai_thue_04_gtgt_khoan_thu_ho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietToKhai04GTGT_KhoanThuHo` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Khoản thu hộ — Mục B tờ khai 04/GTGT ([33]–[35]) · Danh mục Khoản thu hộ (H2): {Chịu thuế GTGT 5% \| Chịu thuế GTGT 10%}. · [34] tự hiển thị 5%/10%; = 8% khi đính kèm phụ lục giảm + khoản thu hộ 10% (BR-08). · MVP có thể chỉ hiển thị ô tích + chặn (Q1 treo — Should). |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_to_khai_thue_04_gtgt` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ToKhaiThue04GTGTId` | `to_khai_thue_04_gtgt_id` | `uuid` | N | — | ID tờ khai 04/GTGT (reference đến ENT_ToKhaiThue04GTGT) `FK` |
| 2 | `LoaiKhoanThuHo` | `loai_khoan_thu_ho` | `text` CHECK | N | — | (ChiuThueGTGT5 \| ChiuThueGTGT10) |
| 3 | `DoanhThuChuaThue` | `doanh_thu_chua_thue` | `money_foreign` ≈ | N | `0` | [33] Doanh thu chưa có thuế GTGT |
| 4 | `ThueSuat` | `thue_suat` | `percent_rate` | Y | `0` | [34] Thuế suất (5 \| 10; = 8 khi có phụ lục giảm và LoaiKhoanThuHo = ChiuThueGTGT10) |
| 5 | `ThuePhaiNop` | `thue_phai_nop` | `money_foreign` ≈ | Y | `0` | [35] = [33] × [34] |

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

## 20. `tax_phu_luc_giam_thue_04_gtgt`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuLucGiamThue04GTGT` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Phụ lục giảm thuế GTGT của tờ khai 04 (Mẫu số 01 — NĐ 174/2025) · CHỈ Mục II bán ra (Mục I mua vào 8% không nhập trên tờ 04). Chỉ chọn khi kỳ · thuộc khoảng hiệu lực CẤU HÌNH ĐƯỢC (hiện hành 07/2024 → hết 12/2026); phụ lục · đã chọn không được rỗng (BR-11). Tỷ lệ sau giảm = tỷ lệ theo quy định × 80% (BR-06). |
| Vai trò | Bảng liên kết N–N |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng. |
| Bảng cha | `tax_to_khai_thue_04_gtgt` — FK `ON DELETE CASCADE` |
| Bảng con | `tax_phu_luc_giam_thue_04_gtgt_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ToKhaiThue04GTGTId` | `to_khai_thue_04_gtgt_id` | `uuid` | N | — | ID tờ khai 04/GTGT (1-0..1) `FK` `UNIQUE` |
| 2 | `TongGiaTri` | `tong_gia_tri` | `money_foreign` ≈ | Y | `0` | [07] Tổng cột (3) — giá trị HHDV được giảm |
| 3 | `TongThueDuocGiam` | `tong_thue_duoc_giam` | `money_foreign` ≈ | Y | `0` | [08] Tổng cột (6) — thuế GTGT được giảm |

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

## 21. `tax_phu_luc_giam_thue_04_gtgt_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhuLucGiamThue04GTGT` |
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
| Bảng cha | `tax_phu_luc_giam_thue_04_gtgt` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-07522 · PMKT-E-10978 · PMKT-E-14792 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuLucGiamThue04GTGTId` | `phu_luc_giam_thue_04_gtgt_id` | `uuid` | N | — | ID phụ lục (reference đến ENT_PhuLucGiamThue04GTGT) `FK` |
| 2 | `TenHHDV` | `ten_hhdv` | `text` | N | — | (2) Tên hàng hóa dịch vụ |
| 3 | `GiaTri` | `gia_tri` | `money_foreign` ≈ | N | `0` | (3) Giá trị HHDV chưa thuế / doanh thu chịu thuế |
| 4 | `TyLeTheoQuyDinh` | `ty_le_theo_quy_dinh` | `percent_rate` | N | `0` | (4) Tỷ lệ theo quy định (1 \| 2 \| 3 \| 5; khoản thu hộ = 10) |
| 5 | `TyLeSauGiam` | `ty_le_sau_giam` | `percent_rate` | Y | `0` | (5) = (4) × 80% |
| 6 | `ThueDuocGiam` | `thue_duoc_giam` | `money_foreign` ≈ | Y | `0` | (6) = (3) × [(4) − (5)] |

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

