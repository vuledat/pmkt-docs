# Kế hoạch thiết kế bộ bảng dữ liệu theo `ba/Common/LDM_update`

> **Trạng thái:** `BẢN NHÁP CHỜ BA + DBA + DEV BE CHỐT`
> **Ngày khảo sát:** 2026-08-13
> **Nguồn chuẩn:** [`pmkt-docs/ba/Common/LDM_update/`](../ba/Common/LDM_update/) — 24 file `.puml` (trừ `ldm-DanhMuc-Update.puml`) + [`QuytacmotaEntity.md`](../ba/Common/LDM_update/QuytacmotaEntity.md)
> **Đối chiếu code:** `cell-app` @ migration V363, 235 bảng sống, 71 bảng có JPA entity

---

## 0. Tóm tắt điều hành

| Chỉ số | Giá trị | Ghi chú |
|---|---:|---|
| Entity trong LDM_update (trong phạm vi) | **206** | 24 file, đã trừ `ldm-DanhMuc-Update.puml` |
| Bảng đang sống trong DB (đã trừ bảng DROP, bảng đã RENAME đi, và partition con) | **235** | |
| Bảng có JPA entity (đã code) | **71** | |
| Trong đó thuộc `mst_*` (danh mục — **ngoài phạm vi**) | **51** | vùng đóng băng `master_data/**` |
| **Bảng ngoài danh mục thực sự đã code nghiệp vụ** | **20** | 6 `iam_` · 4 `cfg_` · 2 `sal_` · 2 `pur_` · 2 `core_` · 1 `acc_` · 1 `ctu_` · 1 `str_` · 1 `ops_` |
| Bảng ngoài danh mục **đã có schema nhưng chưa có code** | **162** | `fa_` 27 · `inv_` 18 · `pur_` 15 · `cst_` 16 · `ccdc_` 15 · `sal_` 9 · `sdbd_` 9 · `rpt_` 9 · `cb_` 8 · `cptt_` 5 · `ktth_` 4 … |

**Ba kết luận chi phối toàn bộ kế hoạch:**

1. **Hệ thống đang có ba tầng lệch nhau** — LDM (BA), schema DB (đã tạo trước, phần lớn chưa dùng), và code nghiệp vụ (chỉ 20 bảng). Việc "thiết kế bảng theo LDM" **không phải** dựng mới từ số 0, mà chủ yếu là **đối chiếu — vá — chuẩn hóa** 162 bảng đã có schema nhưng chưa bị code khóa cứng. Đây là **cửa sổ chi phí thấp duy nhất**: sửa bảng chưa có code rẻ hơn nhiều lần so với sau khi đã có JPA entity + FE + dữ liệu thật.

2. **Bộ trường base đang có 4 cách đặt tên khác nhau** cho cùng một khái niệm (BR46 ↔ header từng file LDM ↔ `BaseEntity` ↔ `BaseChungTuEntity`). Phải chốt **một** bộ trước khi sinh bất kỳ bảng nào — xem [§3.3](#33-bộ-trường-base-bắt-buộc) và [Q1](#4-xung-đột--câu-hỏi-phải-chốt-trước-khi-code).

3. **Có ít nhất một điểm lệch ngữ nghĩa gây hỏng số liệu âm thầm**: `SoCai.PSNo` trong LDM là **nguyên tệ**, còn `acc_so_cai.so_tien_phat_sinh_no` trong code là **đồng tiền hạch toán**. Map tên theo trực giác sẽ đảo ngược sổ cái mà không có lỗi biên dịch nào báo — xem [§2.4](#24-điểm-lệch-nguy-hiểm-nhất--phải-xử-lý-trước).

---

## 1. Phạm vi

### 1.1 Trong phạm vi

24 file LDM, 206 entity:

| File LDM | Entity | Prefix bảng đề xuất | Trạng thái schema DB |
|---|---:|---|---|
| `ldm-Kho-Update.puml` | 28 | `inv_` | 18 bảng có, thiếu ~11 |
| `ldm-TaiSanCoDinh-Update.puml` | 27 | `fa_` | 27 bảng có |
| `ldm-Thue-Update.puml` | 21 | `tax_` | **1 bảng có** — thiếu 20 |
| `ldm-CCDC.puml` | 18 | `ccdc_` | 15 bảng có |
| `ldm-GiaThanh.puml` | 18 | `cst_` | 16 bảng có |
| `ldm-BaoCaoTaiChinh.puml` | 10 | `rpt_` | 9 bảng có |
| `ldm-Authentication.puml` | 10 | `iam_` | 1 phần (`iam_tai_khoan`, `iam_tenant`) — thiếu ~8 |
| `ldm-BanHang-Update.puml` | 9 | `sal_` | 9 bảng có (2 đã code) |
| `ldm-SoDuBanDau.puml` | 9 | `sdbd_` | 9 bảng có |
| `ldm-MuaHang-Update.puml` | 8 | `pur_` | 8 bảng có (2 đã code) |
| `ldm-NganQuy-Update.puml` | 7 | `cb_` | 7 bảng có |
| `ldm-ChiPhiTraTruoc-Update.puml` | 6 | `cptt_` | 5 bảng có |
| `ldm-HeThong.puml` | 6 | `iam_` / `cfg_` | 3 bảng có (đã code) |
| `ldm-DanhGiaLaiNgoaiTe.puml` | 5 | `fx_` (mới) | **0** |
| `ldm-KetChuyenLaiLo.puml` | 3 | `ktth_` / `cls_` (mới) | **0** |
| `ldm-KhoaSo-Update.puml` | 3 | `cfg_` | 3 bảng có (đã code) |
| `ldm-PhieuKTTH.puml` | 3 | `ktth_` | 3 bảng có |
| `ldm-TraLaiHangMua.puml` | 3 | `pur_` | 2 bảng có |
| `ldm-DieuChinhGiaHangBan.puml` | 2 | `sal_` | 2 bảng có |
| `ldm-DieuChinhGiaHangMua.puml` | 2 | `pur_` | 2 bảng có |
| `ldm-DoiTruCongNo-Update.puml` | 2 | `pur_` | 2 bảng có |
| `ldm-ProfileManagement.puml` | 2 | `iam_` | **0** |
| `ldm-SoKeToan-Update.puml` | 2 | `acc_` | 2 bảng có (1 đã code) |
| `ldm-TraLaiHangBan.puml` | 2 | `sal_` | 2 bảng có |

> Cột "Trạng thái schema DB" là **kết quả đối sánh tự động theo tên** (`ldm_entities` × `tbl_live`), độ khớp trung bình. **Bắt buộc đối chiếu tay ở Pha 1** trước khi lấy làm căn cứ ước lượng — không dùng trực tiếp bảng này để lập backlog.

### 1.2 Ngoài phạm vi

| Mục | Lý do |
|---|---|
| `ldm-DanhMuc-Update.puml` (1.069 dòng) | User loại trừ — danh mục đang dùng chung. **Nhưng vẫn phải đọc** để lấy khối `CoAudit`, `ENT_FileDinhKem`, `ENT_ChungTuLienQuan`, `ENT_QuyTacDanhSo`, `ENT_LoaiChungTu` mà 24 file trong phạm vi đều tham chiếu tới |
| `master_data/**` (51 bảng `mst_*`) | Vùng đóng băng theo `CLAUDE.md` |
| `agg_*` (5 bảng), `aud_*`, `ops_*`, `event_publication` | Bảng rollup/hạ tầng, không có entity tương ứng trong LDM |
| Viết code Java (entity/repository/service/controller) | Kế hoạch này chỉ ra **đặc tả bảng + migration**. Code đi theo `/plan-be` từng epic |

### 1.3 Đầu ra của kế hoạch

| # | Sản phẩm | Trạng thái | Định dạng |
|---|---|---|---|
| O1 | [`db-spec/<NN>-<module>.md`](db-spec/README.md) — đặc tả 206 bảng: tên bảng, cột, kiểu, NULL, mặc định, mô tả nghiệp vụ, nguồn dữ liệu, diff với DB hiện tại | ✅ **đã sinh** — 24 file, 2.675 trường | Markdown, template [§3.6](#36-template-đặc-tả-một-bảng) |
| O2 | [`db-spec/00-chuan-chung.md`](db-spec/00-chuan-chung.md) — trường base, domain type, quy tắc đặt tên, hạ tầng bắt buộc | ✅ **đã viết** | Markdown |
| O3 | [`db-spec/90-doi-chieu.md`](db-spec/90-doi-chieu.md) — ma trận LDM entity × bảng DB × JPA entity + hành động | ✅ **đã sinh** — 206 dòng | Markdown |
| O4 | Migration `V364+` theo từng module | ⬜ Pha 3–4 | `.sql` |
| O5 | Quyết định đã chốt Q1–Q12 + BR bị lệch | ⬜ Pha 0 | Markdown, gắn vào O2 |

> O1/O2/O3 **sinh tự động từ `.puml`** — sửa LDM rồi sinh lại, không sửa tay (giảm thiểu rủi ro **R2**).

---

## 2. Hiện trạng — ba tầng lệch nhau

### 2.1 Ba tầng

```
Tầng 1 — LDM (BA)          206 entity     ← nguồn chuẩn, cập nhật 2026-08-13
Tầng 2 — Schema DB          235 bảng      ← dựng trước theo một bản thiết kế 2026-06 (DESIGN-ONLY)
Tầng 3 — Code nghiệp vụ      71 bảng      ← trong đó 51 là mst_ (đóng băng) ⇒ chỉ 20 bảng nghiệp vụ thật
```

> Bản thiết kế nguồn của Tầng 2 được các migration dẫn chiếu là `docs/sysem-design/schema_design/*.sql`
> (ví dụ header của `V245__acc_so_xuat_nhap_tong_hop.sql` trỏ tới `40-acc.sql`), nhưng **thư mục này không
> tồn tại trong repo**. Pha 1 phải xác minh: hoặc tìm lại bản gốc, hoặc coi schema hiện tại là nguồn duy
> nhất của Tầng 2 và gỡ các dẫn chiếu chết trong migration.

Tầng 2 sinh ra trước Tầng 1 bản `_Update`. Vì thế **phần lớn lệch là "schema cũ vs LDM mới"**, không phải "code sai".

### 2.2 Phân loại bảng theo trạng thái — quyết định cách xử lý

| Nhóm | Định nghĩa | Số lượng | Cách xử lý | Chi phí |
|---|---|---:|---|---|
| **A** | Có LDM · có schema · **có code** | **13** | `ALTER` + sửa entity + sửa FE + migrate dữ liệu | **Cao** |
| **B** | Có LDM · có schema · **chưa có code** | **122** | `ALTER` / `DROP+CREATE` tự do, không có dữ liệu thật | **Thấp** |
| **C** | Có LDM · **chưa có schema** | **70** | `CREATE TABLE` mới theo đúng chuẩn | Thấp |
| **?** | Chưa rà được | **1** | `ThamChieuThuCongCCDC` — Pha 1 đối chiếu tay | — |
| **D** | **Không có trong LDM** · có schema | ~40 | Xác minh: bảng hạ tầng (giữ) hay bảng chết (DROP) | Thấp |

> A/B/C/? là **kết quả đối chiếu đã chốt tay từng entity**, xem [`db-spec/90-doi-chieu.md`](db-spec/90-doi-chieu.md).
> Riêng nhóm D còn là ước lượng — Pha 1 phải rà từng bảng DB không có entity LDM tương ứng.

**Đặc tả chi tiết 206 bảng — 2.675 trường nghiệp vụ — đã sinh sẵn tại [`db-spec/`](db-spec/README.md).**

**Nhóm B là trọng tâm của kế hoạch này.** 140 bảng đang ở trạng thái sửa được gần như miễn phí. Mỗi epic được code lên một bảng nhóm B sẽ chuyển nó sang nhóm A và nhân chi phí sửa lên nhiều lần.

### 2.3 20 bảng nhóm A — danh sách đầy đủ

| Bảng | Module Java | LDM tương ứng | Mức lệch |
|---|---|---|---|
| `acc_so_cai` | `accounting_core/hach_toan` | `SoCai` | **Nặng** — xem §2.4 |
| `sal_chung_tu_ban_hang` | `chung_tu_ban_hang` | `ChungTuBan` | **Nặng** |
| `sal_chi_tiet_chung_tu_ban_hang` | `chung_tu_ban_hang` | `ChiTietChungTuBan` | **Nặng** |
| `pur_chung_tu_mua_hang` | `chung_tu_mua_hang` | `ChungTuMuaHang` | **Nặng** |
| `pur_chi_tiet_chung_tu_mua_hang` | `chung_tu_mua_hang` | `ChiTietChungTuMuaHang` | Trung bình |
| `cfg_thiet_lap_khoa_so` | `accounting_core/khoa_so` | `ThietLapKhoaSo` | Nhẹ |
| `cfg_thiet_lap_khoa_so_chung_tu` | `accounting_core/khoa_so` | `ChiTietThietLapKhoaSoChungTu` | Nhẹ (tên bảng con) |
| `cfg_thiet_lap_khoa_so_nguoi_dung` | `accounting_core/khoa_so` | `ChiTietThietLapKhoaSoNguoiDung` | Nhẹ (tên bảng con) |
| `cfg_cau_hinh_he_thong` | `common/cau_hinh_he_thong` | *(không có trong LDM)* | Nhóm D — xác minh |
| `iam_vai_tro` | `platform_iam/vai_tro` | `VaiTro` | Nhẹ |
| `iam_vai_tro_quyen` | `platform_iam/vai_tro` | `VaiTroQuyen` | Nhẹ |
| `iam_tai_khoan` | `platform_iam/nguoi_dung` | `NguoiDung` | Trung bình (tên bảng) |
| `iam_tai_khoan_vai_tro` | `platform_iam/nguoi_dung` | `NguoiDungVaiTro` | Trung bình (tên bảng) |
| `iam_tai_khoan_tenant` | `platform_iam/nguoi_dung` | `NguoiDung_Tenant` | Trung bình (tên bảng) |
| `iam_quyen` | `platform_iam/quyen` | *(không có trong LDM)* | Nhóm D |
| `ctu_quan_he_chung_tu` | `quan_he_chung_tu` | *(không có trong LDM)* | Nhóm D — hạ tầng, giữ |
| `core_cau_hinh_cot` | `common/ui_config` | *(không có trong LDM)* | Nhóm D — hạ tầng, giữ |
| `core_mau_excel` | `common/mau_excel` | *(không có trong LDM)* | Nhóm D — hạ tầng, giữ |
| `str_file` | `common/storage` | `ENT_FileDinhKem` (ở DanhMuc) | Cần đối chiếu |
| `ops_webhook_delivery` | `integration_ops` | `NhatKyWebhookHub` | Cần đối chiếu |

### 2.4 Điểm lệch nguy hiểm nhất — phải xử lý trước

#### 2.4.1 `SoCai` — đảo ngược ngữ nghĩa nguyên tệ / quy đổi

| | LDM `SoCai` | Code `acc_so_cai` |
|---|---|---|
| Nguyên tệ (đồng tiền giao dịch) | `PSNo` | `so_tien_phat_sinh_no_ngoai_te` |
| Đồng tiền hạch toán | `PSNoQuyDoi` | `so_tien_phat_sinh_no` |

Nguồn: `cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/dto/DongSoCaiDto.java` — *"số phát sinh Nợ theo ĐỒNG TIỀN HẠCH TOÁN"*; LDM [`ldm-SoKeToan-Update.puml:55`](../ba/Common/LDM_update/ldm-SoKeToan-Update.puml) — *"Phát sinh nợ theo NGUYÊN TỆ"*.

⚠ Đổi tên `PSNo → so_tien_phat_sinh_no` theo trực giác sẽ **đảo ngược toàn bộ sổ cái ngoại tệ**. Không có lỗi biên dịch, không có test nào chặn. Phải chốt hướng đặt tên ở [Q4](#4-xung-đột--câu-hỏi-phải-chốt-trước-khi-code) trước khi động vào bảng này.

#### 2.4.2 `SoCai` — 21 trường LDM chưa có trong code

Code map 19 cột nghiệp vụ; LDM đặc tả 42 trường. Thiếu:

`ChiNhanhId`¹ · `ChiNhanhDoiUngId` · `STTDongChiTiet` · `STTButToan` · `VatTuId` · `TenVatTu` · `TK` (mã) · `TKDoiUng` (mã) · `TienTeHachToan` (tên) · `DienGiaiDong` · `VuViecId` · `DonViId` · `DoiTuongTapHopChiPhiId` · `TenDoiTuong` · `TKNganHangId` · `KheUocId` · `DonHangId` · `HopDongId` · `IsAuto` · `NguoiGhiSoId` · `ThoiGianGhiSo`

¹ Code có `ma_don_vi_id` — cần xác minh đây là `ChiNhanhId` hay `DonViId`; LDM tách **hai** trường riêng biệt.

Hệ quả: **mọi sổ chi tiết theo vụ việc / đơn vị / đối tượng tập hợp chi phí / khế ước đều chưa lên được** từ `acc_so_cai` hiện tại. Đây là chặn cứng cho phân hệ Báo cáo và Giá thành.

#### 2.4.3 `SoKho` — LDM đặt lại bảng, schema đang mang tên và cấu trúc khác

| | LDM | DB hiện tại |
|---|---|---|
| Tên | `SoKho` | `acc_so_xuat_nhap_tong_hop` (V245) |
| Cột nhập/xuất | `LoaiNhapXuat` enum (0=Nhập, 1=Xuất) | `kieu_nhap_xuat boolean` |
| Kho | `KhoId` (1 cột) | `ma_kho_nhap_id` + `ma_kho_xuat_id` (2 cột) |
| Quy đổi ĐVT | `DonViTinhChinhId`, `HeSoQuyDoi`, `SoLuongNhapChinh`, `SoLuongXuatChinh` | `he_so_quy_doi`, `don_vi_tinh_chuan` (text), `so_luong_nhap_quy_doi` |
| Cấu phần giá nhập | `ChiPhiPhanBoQuyDoi`, `ThueNhapKhauQuyDoi`, `ThueBVMTQuyDoi`, `ThueTTDBQuyDoi`, `ThueCBPGQuyDoi` | cần đối chiếu |

Đã có `docs/doing/ghi-so-kho-kernel-plan.md` chốt dùng `acc_so_xuat_nhap_tong_hop` làm bảng sổ kho. **Hai tài liệu này mâu thuẫn** — phải hòa giải ở [Q5](#4-xung-đột--câu-hỏi-phải-chốt-trước-khi-code) trước khi kernel ghi sổ kho được code.

#### 2.4.4 `ChungTuBan` vs `sal_chung_tu_ban_hang` — lệch tên và lệch mô hình

| LDM | Code | Loại lệch |
|---|---|---|
| `TongTienHang` | `tong_tien_hang_hoa` | Tên |
| `TongChietKhau` / `TongChietKhauTheoHang` / `TongChietKhauTheoHoaDon` | `tong_tien_chiet_khau` / `..._hang` / `..._hoa_don` | Tên |
| `TyLeChietKhauChung` | `gia_tri_chiet_khau` | **Tên + ngữ nghĩa** (tỷ lệ vs giá trị) |
| `MaSoThueCCCD` (1 cột) | `ma_so_thue` + `cccd` + `ho_chieu` + `ma_so_dvqhns` (4 cột) | **Mô hình** |
| `TongThueXK`, `TongThueXKQuyDoi` | *(không có ở header)* | Thiếu |
| `SoChungTuXuatKho` / `NgayChungTuXuatKho` / `NguoiNhanHang` | `phieu_xuat_kho_id` | **Mô hình** — LDM: KHÔNG sinh bản ghi `PhieuXuatKho`; code: sinh và trỏ FK |
| `SoChungTuThuTien` / `NgayChungTuThuTien` / `NguoiNopTien` / `LyDoThu` / `TenNganHangNhan` | `phieu_thu_id` + `mieu_ta_phieu_thu` | **Mô hình** — như trên |
| `TrangThaiGhiSo` enum (ChuaGhiSo\|DaGhiSo) | `status` `TrangThaiChungTu` (5 giá trị) | **Mô hình** — LDM không có CHO_DUYET / DA_DUYET / HUY |
| — | `la_giao_dich_noi_bo_tap_doan`, `doi_tac_tenant_id`, `nguoi_nhan`, `nguoi_nop`, `mo_ta` | Code thừa so với LDM |

Dòng chi tiết: `TaiKhoanCongNoId`/`TaiKhoanDoanhThuId` (LDM) vs `tai_khoan_no_id`/`tai_khoan_co_id` (code); `GiaTriTinhThueXK`/`ThueSuatXK` vs `don_gia_thue_xk`/`phan_tram_thue_xk`; LDM có `DoiTuongTapHopChiPhiId` mà code chưa có.

**Hai lệch mô hình (chứng từ kiêm phiếu xuất kho / kiêm phiếu thu, và tập trạng thái) là quyết định nghiệp vụ, không phải quyết định kỹ thuật** — phải do BA chốt, xem [Q6](#4-xung-đột--câu-hỏi-phải-chốt-trước-khi-code) và [Q7](#4-xung-đột--câu-hỏi-phải-chốt-trước-khi-code).

#### 2.4.5 `ChungTuMuaHang` — hậu tố `_vnd` vs `QuyDoi`

Code dùng `tong_tien_hang_vnd`, `tong_thue_gtgt_vnd`, `gia_tri_nhap_kho_vnd`… LDM dùng hậu tố `QuyDoi`. Cùng nghĩa (giá trị theo đồng tiền hạch toán) nhưng `_vnd` hardcode giả định đồng tiền hạch toán là VND — sai với tenant hạch toán bằng ngoại tệ (`Tenant.LoaiTienId` cho phép chọn). Nên đổi sang `_quy_doi` khi vá bảng.

---

## 3. Chuẩn thiết kế bảng — phải chốt trước khi sinh bảng đầu tiên

### 3.1 Quy tắc đặt tên bảng

Kế thừa `docs/chuan-hoa-ten-bang-chung-tu.md` (đang là bản nháp chờ chốt — kế hoạch này **phụ thuộc** vào nó):

```
<module>_<nghiệp vụ>[_<bảng con>]
   │          │            └── chi_tiet · tham_chieu · lien_ket · nguoi_kiem_ke · …
   │          └── viết đầy đủ, không viết tắt, không lặp lại tiền tố module
   └── prefix module (bảng dưới)
```

| Prefix | Phân hệ | Prefix | Phân hệ |
|---|---|---|---|
| `acc_` | Sổ kế toán (sổ cái, sổ thuế, sổ kho) | `inv_` | Kho |
| `agg_` | Bảng tổng hợp / rollup | `iam_` | Người dùng, vai trò, quyền, tenant |
| `aud_` | Nhật ký kiểm toán | `ktth_` | Kế toán tổng hợp |
| `cb_` | Ngân quỹ (tiền mặt, tiền gửi) | `mst_` | Danh mục *(ngoài phạm vi)* |
| `ccdc_` | Công cụ dụng cụ | `ops_` | Vận hành, webhook |
| `cfg_` | Cấu hình hệ thống | `pur_` | Mua hàng |
| `core_` | Hạ tầng dùng chung | `rpt_` | Báo cáo tài chính |
| `cptt_` | Chi phí trả trước | `sal_` | Bán hàng |
| `cst_` | Giá thành | `sdbd_` | Số dư ban đầu |
| `ctu_` | Quan hệ chứng từ | `str_` | Lưu trữ tệp |
| `fa_` | Tài sản cố định | `tax_` | Thuế |

**Prefix mới cần chốt** ([Q8](#4-xung-đột--câu-hỏi-phải-chốt-trước-khi-code)): `fx_` (đánh giá lại ngoại tệ, 5 entity) và nơi đặt 3 entity kết chuyển lãi lỗ.

Hai luật cứng:

1. `chi_tiet` là **hậu tố**: `sal_chung_tu_ban_hang_chi_tiet`, không phải `sal_chi_tiet_chung_tu_ban_hang`.
2. Không viết tắt trong phần nghiệp vụ: `tscd` → `tai_san_co_dinh`, `hd` → `hoa_don`, `dv` → `dich_vu`. Prefix module giữ nguyên vì là mã module.

### 3.2 Quy tắc đặt tên cột

| Loại | Quy tắc | Ví dụ cột DB |
|---|---|---|
| Khóa chính | `id` | `id` |
| Khóa ngoại | `<thực_thể>_id` | `nha_cung_cap_id`, `vat_tu_id`, `don_vi_tinh_id` |
| Snapshot tên đi kèm FK (Rule 2) | `ten_<thực_thể>` | `ten_nha_cung_cap`, `ten_vat_tu` |
| Ngày (không giờ) | tiền tố `ngay_` | `ngay_chung_tu`, `ngay_hach_toan` |
| Mốc thời gian (có giờ) | tiền tố `thoi_gian_` | `thoi_gian_ghi_so` |
| Số tiền | hậu tố mô tả bản chất, **cấm** `so_tien` trần | `thanh_tien_xuat`, `tong_tien_thanh_toan` |
| Số tiền quy về đồng hạch toán | hậu tố `_quy_doi` (**không** `_vnd`) | `thanh_tien_quy_doi` |
| Số lượng | tiền tố `so_luong_` | `so_luong_xuat`, `so_luong_ton` |
| Cờ boolean | tiền tố `is_` / `cho_phep_` / `da_` | `is_auto`, `cho_phep_sua`, `da_ghi_so` |
| Trạng thái workflow | `status` (đã dùng ở `BaseChungTuEntity`) | `status` |

**Nguyên tắc bất biến:** một khái niệm nghiệp vụ ⇒ **một** tên cột xuyên suốt mọi bảng. `vat_tu_id` phải giống hệt ở `sal_chung_tu_ban_hang_chi_tiet`, `inv_phieu_xuat_kho_chi_tiet`, `acc_so_cai`, `acc_so_kho`. Hiện đang vi phạm: `ma_hang_id` (bán hàng) vs `vat_tu_id` (mua hàng) cho cùng một thứ.

**Ngoại lệ Rule 2 đã chốt ở LDM:** `TK` / `TKDoiUng` / `TKVatTu` / `TKGiaVon` — sổ cái và sổ kho **có** lưu mã tài khoản, vì mã TK là định danh in trên sổ sách và không được đổi khi đã phát sinh.

### 3.3 Bộ trường base bắt buộc

#### 3.3.1 Bốn cách đặt tên đang tồn tại — phải chọn một

| Khái niệm | BR46 (business_rules.md) | Header LDM nhóm 1 ¹ | Header LDM nhóm 2 ² | Code `BaseEntity` |
|---|---|---|---|---|
| Cờ xóa mềm | `DaXoa` | `DaXoa` | `IsDeleted` | `da_xoa` ✅ |
| Người xóa | `NguoiXoaId` | `NguoiXoa` | — | `nguoi_xoa` |
| Thời điểm xóa | `NgayXoa` | `ThoiGianXoa` | `DeletedAt` | `ngay_xoa` |
| Người tạo | `NguoiTaoId` | `NguoiTao` | `CreatedBy` | `nguoi_tao` |
| Thời điểm tạo | `NgayTao` | `ThoiGianTao` | `CreatedAt` | `ngay_tao` |
| Người sửa | `NguoiCapNhatId` | `NguoiCapNhat` | `UpdatedBy` | `nguoi_cap_nhat` |
| Thời điểm sửa | `NgayCapNhat` | `ThoiGianCapNhat` | `UpdatedAt` | `ngay_cap_nhat` |
| Người ghi sổ | `NguoiGhiSoId` | `NguoiGhiSo` | — | `nguoi_ghi_so` ³ |
| Thời điểm ghi sổ | `ThoiGianGhiSo` | `ThoiGianGhiSo` | — | `thoi_gian_ghi_so` ³ |

¹ `ldm-DanhGiaLaiNgoaiTe`, `ldm-GiaThanh`, `ldm-KetChuyenLaiLo` — dẫn chiếu BR46 nhưng viết tên khác BR46.
² `ldm-BanHang-Update`, `ldm-Authentication`.
³ Khai ở `BaseChungTuEntity`, không có ở `BaseEntity`.

**Đề xuất (chờ chốt [Q1](#4-xung-đột--câu-hỏi-phải-chốt-trước-khi-code)):** giữ nguyên tên cột DB đang chạy (`nguoi_tao`, `ngay_tao`, …) và **sửa BR46 + header LDM** cho khớp, thay vì đổi 235 bảng. Lý do:

- Đổi tên cột đụng RLS policy, trigger `fn_audit`, index, view, native query — chi phí gấp nhiều lần lợi ích.
- `_id` chỉ là hậu tố mô tả kiểu, không mang nghĩa nghiệp vụ mới.
- `ngay_tao` mang kiểu `timestamptz` nên vẫn đúng nghĩa "thời điểm"; đổi sang `thoi_gian_tao` là thay đổi thuần hình thức.

**Nếu BA yêu cầu ngược lại** (đổi DB theo BR46) thì phải tính vào Pha 0 như một đợt migration riêng, chạy trước mọi việc khác, và **không** làm xen kẽ với các pha sau.

#### 3.3.2 Bốn tầng base class — bảng nào kế thừa gì

Đã có sẵn trong `cell-app/src/main/java/vn/vtt/pmkt/cell/core/entity/`, **không dựng lại**:

| Base class | Cột thêm vào | Dùng cho |
|---|---|---|
| `BaseEntity` | `id` (uuid, default `gen_random_uuid()`) · `ngay_tao` · `ngay_cap_nhat` · `da_xoa` · `ngay_xoa` · `nguoi_tao` · `nguoi_cap_nhat` · `nguoi_xoa` | Nền của mọi bảng |
| `TenantedEntity` *(extends BaseEntity)* | `tenant_id` (NOT NULL, không sửa được, khóa RLS) | Mọi bảng nghiệp vụ |
| `AggregateRootEntity` *(extends TenantedEntity)* | `phien_ban` (`@Version`, optimistic lock) | Chứng từ, danh mục có sửa đồng thời |
| `BaseChungTuEntity` *(extends AggregateRootEntity)* | `chi_nhanh_id` · `loai_chung_tu_id` · `giao_dich_chung_tu_id` · `so_chung_tu` · `ngay_chung_tu` · `ngay_hach_toan` · `status` · `nguoi_duyet_id` · `ngay_duyet` · `nguoi_ghi_so` · `thoi_gian_ghi_so` | **Header** mọi chứng từ |
| `BaseChiTietChungTuEntity` *(extends TenantedEntity)* | `thu_tu` + `getChungTuId()` abstract | **Dòng chi tiết** mọi chứng từ |

**Quy tắc chọn base:**

| Loại bảng trong LDM | Base bắt buộc | Cột riêng phải khai thêm |
|---|---|---|
| Header chứng từ (`ChungTuBan`, `PhieuNhapKho`, `PhieuThu`…) | `BaseChungTuEntity` | trường nghiệp vụ |
| Dòng chi tiết (`ChiTiet*`) | `BaseChiTietChungTuEntity` | `<cha>_id` NOT NULL + FK ON DELETE CASCADE |
| Bảng cháu (`ChiTietNguoiKiemKe`, `PhieuKiemKeCCDC_DonVi`…) | `TenantedEntity` | `<cha>_id` NOT NULL + FK |
| Sổ (`SoCai`, `SoKho`) | `TenantedEntity` + `@Immutable` | `chi_nhanh_id` · `is_auto` · `nguoi_ghi_so` · `thoi_gian_ghi_so` · `request_hash` |
| Bảng kết quả / snapshot (`TonKho`, `CostLayer`, `KetQuaTinhGiaXuatKho`) | `TenantedEntity` | — |
| Cấu hình (`ThietLapKhoaSo`, `CauHinhEmail`, `Tenant`) | `AggregateRootEntity` | — |
| Bảng link N-N (`Tenant_LinhVucHoatDong`, `VaiTroQuyen`) | `TenantedEntity` | UNIQUE trên cặp khóa |

> **Cảnh báo bắt buộc đọc:** entity chứng từ **không được** khai `@AttributeOverride` đổi tên cột thời gian sang `thoi_gian_*`. `ddl-auto: none` nên Hibernate không đối chiếu cột lúc khởi động — sai tên cột thì app vẫn boot, test vẫn xanh, chỉ vỡ khi người dùng mở màn hình. Ghi chú này đã có sẵn trong javadoc `BaseChungTuEntity`, lặp lại ở đây vì đã từng phải rút lại một lần (V345–V349 → V351).

#### 3.3.3 `TenantId` / `ChiNhanhId` — BR46.4

| Trường | Bắt buộc ở | Ràng buộc |
|---|---|---|
| `tenant_id` | **Mọi** bảng nghiệp vụ | NOT NULL · `updatable = false` · gán từ `TenantContext` lúc persist · là khóa của RLS policy `tenant_isolation` · **cấm** tham chiếu chéo tenant |
| `chi_nhanh_id` | Mọi bảng **gốc do người dùng lập** | Không tự gán từ context (chứng từ điều chuyển hợp lệ khi lập cho chi nhánh khác) — **service phải `setChiNhanhId()` tường minh** và kiểm quyền theo phạm vi đơn vị (`iam_tai_khoan_quyen_don_vi` / `iam_pham_vi_hieu_luc`) |

> ⚠ Javadoc của `BaseChungTuEntity` hiện còn trỏ tới bảng `iam_nguoi_dung_chi_nhanh` — bảng này **đã bị DROP ở V35**, thay bằng mô hình phạm vi quyền `iam_pham_vi_*` (V308/V309). Sửa ghi chú này khi chạm vào lớp base.

Bảng **dẫn xuất** (`TonKho`, `CostLayer`) không mang `chi_nhanh_id` — suy ra từ `Kho`. Bảng **chi tiết** thừa hưởng qua bảng cha nhưng **vẫn mang `tenant_id`** vì RLS bám cột này.

### 3.4 Kiểu dữ liệu chuẩn — domain type theo BR7

DB đã có sẵn 5 domain, **bắt buộc dùng**, cấm khai `numeric(x,y)` trần:

```sql
CREATE DOMAIN public.money_vnd     AS numeric(18,2);  -- Tiền tệ (đồng hạch toán)
CREATE DOMAIN public.money_foreign AS numeric(18,4);  -- Ngoại tệ
CREATE DOMAIN public.exchange_rate AS numeric(18,6);  -- Tỷ giá
CREATE DOMAIN public.quantity      AS numeric(18,3);  -- Số lượng
CREATE DOMAIN public.percent_rate  AS numeric(5,2);   -- Phần trăm
```

| Kiểu LDM | Kiểu DB | Ghi chú |
|---|---|---|
| `uuid` | `uuid` | FK đa hình (`ChungTuId`, `ChiTietChungTuId`) **không** ràng buộc FK ở DB |
| `string` | `text` | Trừ `so_chung_tu` / mã danh mục: `varchar(50)` theo BR20 |
| `date` | `date` | |
| `datetime` | `timestamptz` | |
| `boolean` | `boolean` | NOT NULL DEFAULT false |
| `enum` | `text` + `CHECK` | **Không** dùng enum native của Postgres — thêm giá trị phải `ALTER TYPE`; JPA dùng `@Enumerated(STRING)` |
| `numeric` (tiền, nguyên tệ) | `money_foreign` | |
| `numeric` (tiền, quy đổi) | `money_vnd` | Tên domain giữ `_vnd` vì đã dùng rộng; nghĩa là "đồng tiền hạch toán" |
| `numeric` (số lượng) | `quantity` | |
| `numeric` (tỷ giá) | `exchange_rate` | |
| `numeric` (%) | `percent_rate` | |
| `numeric` (STT, số dòng) | `integer` | |

**Quy tắc NOT NULL của LDM:** "mọi trường numeric đều NOT NULL, mặc định 0". Áp dụng cho bảng **mới**. Với `acc_so_cai` đang chạy, code đang ghi `null` ở vế đối ứng ⇒ đổi sang NOT NULL DEFAULT 0 là **thay đổi phá vỡ**, phải backfill + sửa `GhiSoService` — xếp vào Pha 5, không làm lẻ.

**Ngoại lệ NULL đã chốt ở LDM Kho:** `TyLePhanBo` (ở `ChiTietPhieuNhapKho`, `ThanhPhamSauLapRapThaoDo`, `ChiTietDinhMucNVL`) để NULL — NULL nghĩa là dòng không tham gia phân bổ, khác hẳn tỷ lệ bằng 0.

### 3.5 Hạ tầng bắt buộc trên mỗi bảng

Mọi bảng nghiệp vụ mới/vá phải có đủ 7 mục:

| # | Mục | Chuẩn |
|---|---|---|
| 1 | Khóa chính | `id uuid NOT NULL DEFAULT gen_random_uuid()`; bảng partition: PK gồm cả khóa phân vùng |
| 2 | RLS | `ENABLE ROW LEVEL SECURITY` + `FORCE` + policy `tenant_isolation` → `fn_current_tenant()` |
| 3 | Trigger audit | `trg_audit_<bảng>` → `fn_audit` |
| 4 | Index dẫn đầu tenant | `(tenant_id, …) WHERE da_xoa = false` |
| 5 | FK cha–con | `ON DELETE CASCADE` cho bảng chi tiết; **không** đặt FK cho liên kết đa hình |
| 6 | Kiểm trùng (BR19) | UNIQUE `(tenant_id, so_chung_tu)` cho chứng từ; `(tenant_id, ma)` cho danh mục — partial `WHERE da_xoa = false` |
| 7 | `COMMENT ON TABLE` / `COMMENT ON COLUMN` | Lấy **nguyên văn** mô tả từ LDM — đây là nơi mô tả trường sống cùng schema |

Riêng bảng **sổ** (`acc_so_cai`, `acc_so_kho`) thêm:

| # | Mục | Chuẩn |
|---|---|---|
| 8 | Partition | `PARTITION BY RANGE(ngay_hach_toan)` + partition `_default` |
| 9 | Idempotency | cột `request_hash` + UNIQUE trên **cột trần** (partition không nhận unique index dạng biểu thức/partial) |
| 10 | Trigger immutable | chặn UPDATE dòng sổ |
| 11 | Trigger period-guard | chặn ghi vào kỳ đã khóa (BR17) |

### 3.6 Template đặc tả một bảng

Mỗi bảng trong O1 viết theo đúng khối dưới đây. Cột `Mô tả` **bắt buộc** nêu nguồn dữ liệu theo Rule 1/Rule 3 của `QuytacmotaEntity.md`, không chỉ mô tả nghiệp vụ.

````markdown
### `acc_so_kho` — Sổ kho (biến động số lượng/giá trị vật tư)

| Mục | Nội dung |
|---|---|
| LDM | `ldm-SoKeToan-Update.puml` › `SoKho` |
| Base | `TenantedEntity` + `@Immutable` |
| Nhóm | B (có schema `acc_so_xuat_nhap_tong_hop`, chưa có code) |
| Hành động | ĐỔI TÊN + VÁ |
| Đơn vị 1 dòng | 1 dòng chi tiết vật tư trên chứng từ |

| # | Cột | Kiểu | Null | Mặc định | Mô tả & nguồn dữ liệu |
|---|---|---|---|---|---|
| 1 | `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. *(BaseEntity)* |
| 2 | `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Gán từ `TenantContext` lúc persist; khóa RLS. *(TenantedEntity, BR46.4)* |
| 3 | `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh. Nguồn: `mst_don_vi` [`loai_don_vi = ChiNhanh`]. |
| 4 | `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ sinh ra dòng. Nguồn: `mst_loai_chung_tu`. Là discriminator của `chung_tu_id`. |
| 5 | `chung_tu_id` | `uuid` | N | — | Chứng từ gốc (header). **Liên kết đa hình** — bảng đích xác định bởi `loai_chung_tu_id`, không đặt FK ở DB. |
| … | | | | | |
| 20 | `so_luong_nhap_chinh` | `quantity` | N | `0` | Số lượng nhập quy về ĐVT chính = `so_luong_nhap × he_so_quy_doi`. Dùng thống nhất khi tính tồn kho. |

**Index & ràng buộc**

| Tên | Định nghĩa | Mục đích |
|---|---|---|
| `pk_acc_so_kho` | `PRIMARY KEY (id, ngay_hach_toan)` | Bảng partition |
| `uq_acc_so_kho_idem` | `UNIQUE (tenant_id, request_hash, chi_tiet_chung_tu_id, kho_id, vat_tu_id, so_lo)` | Idempotency ghi sổ; `so_lo` ghi `''` thay NULL |
| `ix_acc_so_kho_ton` | `(tenant_id, kho_id, vat_tu_id, ngay_hach_toan) WHERE da_xoa = false` | Truy vấn tồn kho |

**Điểm lệch với hiện trạng**

| LDM | DB hiện tại | Hành động |
|---|---|---|
| `LoaiNhapXuat` enum | `kieu_nhap_xuat boolean` | Đổi kiểu |
| `KhoId` (1 cột) | `ma_kho_nhap_id` + `ma_kho_xuat_id` | Gộp về 1 cột |
````

---

## 4. Xung đột & câu hỏi phải chốt trước khi code

Không câu nào được để "quyết sau" — mỗi câu chặn một khối công việc.

| # | Câu hỏi | Chặn | Đề xuất |
|---|---|---|---|
| **Q1** | Bộ trường base lấy theo **BR46** (`NguoiTaoId`/`NgayTao`) hay theo **cột DB đang chạy** (`nguoi_tao`/`ngay_tao`)? Header LDM còn có 2 biến thể nữa (`ThoiGianTao`, `CreatedAt`) | **Toàn bộ** | Giữ cột DB, sửa BR46 + header LDM cho khớp |
| **Q2** | `ldm-BanHang-Update` dẫn chiếu khối `CoAudit` của `ldm-DanhMuc-Update.puml`, nhưng file đó **không có** khối tên `CoAudit`. Khối chuẩn thật nằm ở đâu? | Bán hàng, Auth | BA bổ sung khối vào `ldm-DanhMuc-Update.puml` hoặc trỏ về BR46 |
| **Q3** | LDM có nhắc `ENT_FileDinhKem`, `ENT_ChungTuLienQuan`, `ENT_QuyTacDanhSo`, `ENT_LoaiChungTu`, `ENT_KheUoc`, `ENT_DonDatHang`, `ENT_HopDong` nhưng chúng nằm ở `ldm-DanhMuc-Update.puml` — user loại trừ phần danh mục. Có đưa vào phạm vi không? | Nhiều module | **Có** — 24 file trong phạm vi phụ thuộc trực tiếp; nếu không đưa vào thì không thiết kế nổi FK |
| **Q4** | `SoCai`: giữ tên `PSNo`/`PSNoQuyDoi` (LDM) hay `so_tien_phat_sinh_no`/`..._ngoai_te` (code)? Hai bên **đảo ngược ngữ nghĩa** | Sổ cái, Báo cáo, Giá thành | Giữ tên code, **sửa LDM**; nếu đổi theo LDM thì phải đổi đồng thời cột + code + backfill trong **một** migration |
| **Q5** | Sổ kho: `acc_so_xuat_nhap_tong_hop` (đã có, kernel plan đã chốt) hay `acc_so_kho` theo LDM `SoKho`? | Kho, kernel ghi sổ kho | Đổi tên bảng thành `acc_so_kho` + vá cột theo LDM **trước** khi code kernel — bảng chưa có Java nên rẻ |
| **Q6** | `ChungTuBan` "kiêm phiếu xuất kho / kiêm phiếu thu": LDM nói **không** sinh bản ghi `PhieuXuatKho`/`PhieuThu`; code đang sinh và giữ `phieu_xuat_kho_id`/`phieu_thu_id` | Bán hàng, Kho, Ngân quỹ | BA chốt. Ảnh hưởng đến sổ kho (nguồn `chung_tu_id`) và báo cáo quỹ |
| **Q7** | Trạng thái chứng từ: LDM `ChungTuBan.TrangThaiGhiSo` chỉ 2 giá trị; code `status` có 5 (`NHAP`/`CHO_DUYET`/`DA_DUYET`/`DA_GHI_SO`/`HUY`) theo BR12 | Mọi chứng từ | Giữ 5 giá trị theo BR12, **sửa LDM** — LDM không được thu hẹp BR |
| **Q8** | Prefix cho `ldm-DanhGiaLaiNgoaiTe` (5 entity) và `ldm-KetChuyenLaiLo` (3 entity) — chưa có bảng nào | 2 module | `fx_` cho đánh giá lại ngoại tệ; kết chuyển lãi lỗ vào `ktth_` |
| **Q9** | `ldm-Authentication` khai `GoiDichVu`, `Subscription`, `TenantModule`, `NhatKyWebhookHub` — thuộc `cell-app` hay `tenant-provisioning`/`identity`? | Auth, hạ tầng | Thuộc service ngoài `cell-app`; ghi rõ vào O3 để không tạo nhầm bảng trong `cell-app` |
| **Q10** | Đợt chuẩn hóa tên bảng ở `docs/chuan-hoa-ten-bang-chung-tu.md` (52 bảng) **chạy trước hay sau** kế hoạch này? | Toàn bộ | **Trước** — nếu không, mọi đặc tả trong O1 phải viết hai lần tên bảng |
| **Q11** | 22 bảng nhóm D (có schema, không có trong LDM): giữ, hay DROP? Ví dụ `cst_phuong_phap_danh_gia_do_dang_cuoi_ky`, `iam_tenant_to_chuc_loi`, `pur_dcgm_tham_chieu`, `inv_phieu_nhap_xuat` | Dọn schema | Rà từng bảng ở Pha 1; bảng hạ tầng (`ctu_`, `core_`, `agg_`, `aud_`, `ops_`) giữ nguyên |
| **Q12** | `numeric NOT NULL DEFAULT 0` cho bảng **đang chạy** (`acc_so_cai` đang ghi `null` ở vế đối ứng) — có backfill không? | Sổ cái | Có, nhưng tách thành đợt riêng ở Pha 5 |

---

## 5. Kế hoạch thực hiện

### Pha 0 — Chốt chuẩn *(1 tuần · BA + DBA + Dev BE)*

| # | Việc | Đầu ra | Nghiệm thu |
|---|---|---|---|
| 0.1 | Họp chốt Q1–Q12 | Bảng quyết định ký nhận | 12/12 câu có quyết định, không còn "để sau" |
| 0.2 | Viết `00-chuan-chung.md` (O2) | §3 của tài liệu này, đã áp quyết định | DBA duyệt |
| 0.3 | Cập nhật BR46 + header 24 file LDM cho thống nhất theo Q1 | Commit vào `pmkt-docs` | `grep` không còn 2 cách đặt tên trong LDM |
| 0.4 | Chốt lịch với đợt rename `docs/chuan-hoa-ten-bang-chung-tu.md` theo Q10 | Lịch | Không chồng lấn cửa sổ bảo trì |

> **Cổng chặn:** không sang Pha 1 khi Q1, Q4, Q5, Q10 chưa chốt.

### Pha 1 — Đối chiếu toàn bộ *(2 tuần · 1 BA + 1 Dev BE)*

| # | Việc | Đầu ra |
|---|---|---|
| 1.1 | Dump schema thật từ DB (`information_schema.columns`) ra `.tsv` | `schema_dump.tsv` |
| 1.2 | Đối chiếu **tay** 206 entity LDM × 235 bảng: xác định nhóm A/B/C/D cho từng entity | `90-doi-chieu.md` (O3) |
| 1.3 | Với nhóm A và B: liệt kê từng cột lệch (thiếu / thừa / khác tên / khác kiểu / khác nghĩa) | Cột "Điểm lệch" trong O3 |
| 1.4 | Đánh dấu mọi lệch **ngữ nghĩa** (như §2.4.1) bằng cờ ⚠ riêng | Danh sách ⚠ để BA duyệt từng dòng |
| 1.5 | Chốt lại số lượng thật của A/B/C/D | Cập nhật §0 và §2.2 |

> Đối sánh tự động trong tài liệu này chỉ dùng để **ước lượng khối lượng**. Pha 1.2 phải làm tay vì tên entity LDM và tên bảng DB lệch nhau nhiều (`SoKho` ↔ `acc_so_xuat_nhap_tong_hop`, `NguoiDung` ↔ `iam_tai_khoan`).

### Pha 2 — Đặc tả bảng nhóm C + B *(4–6 tuần · 2 người, chia module)*

Thứ tự ưu tiên: **module chặn nhiều module khác trước**.

| Đợt | Module | Entity | Lý do ưu tiên |
|---|---|---:|---|
| 2.1 | `acc_` — `SoCai`, `SoKho` | 2 | Chặn Kho, Báo cáo, Giá thành, Công nợ |
| 2.2 | `iam_` + `cfg_` — `Tenant`, `VaiTro`, `NguoiDung`, `ProfileManagement` | 18 | Chặn mọi thứ (tenant, phân quyền) |
| 2.3 | `inv_` — Kho | 28 | Nhiều entity nhất, chặn Giá thành + Giá vốn |
| 2.4 | `tax_` — Thuế | 21 | **Gần như trắng** (1/21 bảng) |
| 2.5 | `fa_` + `ccdc_` | 45 | Schema đủ, chỉ vá |
| 2.6 | `cst_` + `cptt_` + `ktth_` + `fx_` | 30 | |
| 2.7 | `sdbd_` + `rpt_` | 19 | Phụ thuộc 2.1 |
| 2.8 | `cb_` — Ngân quỹ | 7 | Phụ thuộc Q6 |

Mỗi đợt sinh: `db-spec/<module>.md` (O1) + migration `V364+` **chỉ cho bảng nhóm B và C**.

### Pha 3 — Migration nhóm B & C *(song song Pha 2, mỗi module một PR)*

Nhóm B/C chưa có Java ⇒ được phép `DROP TABLE` + `CREATE TABLE` lại thay vì chuỗi `ALTER` dài, **với điều kiện** xác minh bảng rỗng:

```sql
-- Chạy TRƯỚC mỗi DROP, phải trả về 0
SELECT count(*) FROM <bảng>;
-- Và xác nhận không có Java tham chiếu
-- grep -rn "<tên bảng>" cell-app/src/main/java  ⇒ rỗng
```

Mỗi PR gồm: migration + `COMMENT ON` đầy đủ + cập nhật O1 + cập nhật O3.

### Pha 4 — Vá nhóm A *(sau Pha 3, từng bảng một PR)*

20 bảng, làm theo thứ tự rủi ro tăng dần:

| Đợt | Bảng | Rủi ro |
|---|---|---|
| 4.1 | `iam_*`, `cfg_thiet_lap_khoa_so*` | Thấp — chủ yếu đổi tên bảng con |
| 4.2 | `pur_chung_tu_mua_hang` + chi tiết (`_vnd` → `_quy_doi`) | Trung bình |
| 4.3 | `sal_chung_tu_ban_hang` + chi tiết | Cao — Q6, Q7 |
| 4.4 | `acc_so_cai` (21 cột thiếu + Q4 + Q12) | **Rất cao** — có dữ liệu thật, có partition, có trigger immutable |

Mỗi PR: migration + sửa JPA entity + sửa DTO/mapper + sửa FE nếu đổi tên trường API + `./gradlew unitTest` + regression test chứng từ.

### Pha 5 — Dọn & siết *(1 tuần)*

| # | Việc |
|---|---|
| 5.1 | DROP bảng nhóm D đã xác nhận chết (Q11) |
| 5.2 | Backfill `NOT NULL DEFAULT 0` cho cột numeric của `acc_so_cai` (Q12) |
| 5.3 | Rà `COMMENT ON COLUMN` đủ 100% cột nghiệp vụ |
| 5.4 | Khôi phục `permissions.deny` cho `master_data/**` trong `.claude/settings.json` nếu đã gỡ |

---

## 6. Phạm vi ảnh hưởng

### 6.1 Code Java

| Vùng | Số file ước tính | Ảnh hưởng |
|---|---:|---|
| `chung_tu_ban_hang/` | ~25 | Entity + DTO + mapper + service + controller đổi theo `sal_*` (Pha 4.3) |
| `chung_tu_mua_hang/` | ~20 | Đổi hậu tố `_vnd` → `_quy_doi` (Pha 4.2) |
| `accounting_core/hach_toan/` | ~15 | `SoCaiEntity` +21 cột; `GhiSoService`, `TaoDinhKhoanService`, `DongSoCaiDto`, `ButToanSoCai` đổi chữ ký (Pha 4.4) |
| `accounting_core/ton_kho/` | *(chưa tồn tại)* | `docs/doing/ghi-so-kho-kernel-plan.md` phải viết lại §3, §6 theo Q5 |
| `platform_iam/` | ~12 | Đổi tên bảng `iam_tai_khoan` → theo LDM `NguoiDung` (nếu Q1 chọn hướng LDM) |
| `core/entity/` | 6 | **Chỉ đổi nếu Q1 chọn đổi theo BR46** — khi đó chạm mọi entity trong hệ thống |
| `master_data/**` | 3 native query | `LyDoNhapXuatRepository.java:74` (`inv_phieu_xuat_kho_module_kho`), `TaiKhoanNganHangRepository.java:30,34`, `MucDichThuChiServiceImpl.java:33` — **vùng đóng băng, phải xin phép gỡ `permissions.deny`** |

### 6.2 Database

| Hạng mục | Khối lượng |
|---|---|
| Bảng `CREATE` mới | ~45 (nhóm C) |
| Bảng `ALTER`/tái tạo | ~140 (nhóm B) + 20 (nhóm A) |
| Bảng `RENAME` | **74** — tên đề xuất khác tên đang chạy. Nhiều hơn con số 52 của `docs/chuan-hoa-ten-bang-chung-tu.md` vì bản đó chỉ phủ bảng chứng từ; LDM còn kéo theo `acc_so_xuat_nhap_tong_hop` → `acc_so_kho`, nhóm `ccdc_*` lặp tiền tố, và các bảng vai trò (`ccdc_chi_tiet_nguoi_kiem_ke` → `ccdc_phieu_kiem_ke_nguoi_kiem_ke`) |
| Bảng `DROP` | ~22 (nhóm D, sau xác minh) |
| RLS policy phải đặt lại | mỗi bảng mới/đổi tên |
| Trigger `fn_audit` phải gắn lại | mỗi bảng mới |
| Partition phải dựng | `acc_so_kho` (nếu đổi tên, partition con đi theo) |

**Rủi ro DB:** `ALTER TABLE … RENAME` lấy `ACCESS EXCLUSIVE lock`. Postgres **giữ nguyên tên cũ** của constraint/index sau khi rename bảng ⇒ phải rename thủ công từng cái, và kiểm tên ≤ 63 ký tự (Postgres cắt âm thầm).

### 6.3 Frontend (`client/`)

Chỉ ảnh hưởng khi **tên trường API** đổi, không phải khi tên cột DB đổi.

| Màn hình | Ảnh hưởng |
|---|---|
| `features/banHang/chungTuBanHang/` | `api/` (Zod schema) + `fields/` + `i18n/` nếu Pha 4.3 đổi tên trường |
| `features/muaHang/…` | Tương tự nếu `_vnd` → `_quy_doi` lộ ra API |
| Các màn chưa code | Không ảnh hưởng — nên **ưu tiên xong DB trước khi code FE** cho các module còn lại |

### 6.4 Rủi ro & giảm thiểu

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| R1 | Đảo ngược ngữ nghĩa nguyên tệ/quy đổi ở sổ cái (§2.4.1) | **Nghiêm trọng** | Q4 chốt trước; test đối chiếu số dư trước/sau migration trên bản sao production |
| R2 | Đặc tả 206 bảng làm tay ⇒ lệch với LDM khi LDM cập nhật tiếp | Cao | Sinh O1 bằng script từ `.puml` thay vì gõ tay; LDM là nguồn duy nhất |
| R3 | Bảng nhóm B bị code lên trong lúc đang thiết kế ⇒ chuyển thành nhóm A, chi phí tăng | Cao | **Đóng băng code mới lên bảng nhóm B** cho tới khi module đó xong Pha 3 |
| R4 | Đợt rename 52 bảng và kế hoạch này giẫm chân nhau | Cao | Q10 chốt thứ tự; hai đợt không chạy song song |
| R5 | Chạm `master_data/**` (3 native query) | Trung bình | Xin phép user gỡ `permissions.deny`, khôi phục ngay sau merge |
| R6 | Tên constraint/index vượt 63 ký tự bị Postgres cắt âm thầm | Trung bình | Query kiểm `length(conname) >= 63` sau mỗi PR |
| R7 | `ddl-auto: none` ⇒ sai tên cột không lộ lúc boot, chỉ vỡ khi mở màn hình | Trung bình | Bắt buộc có integration test chạm DB thật cho mỗi bảng nhóm A đã vá |
| R8 | Máy dev không có Docker ⇒ `./gradlew build` luôn đỏ ở ~25 test Testcontainers | Thấp | Dùng `./gradlew unitTest` làm cổng xanh tại chỗ; `build` đầy đủ chạy trên CI |

---

## 7. Nghiệm thu

### 7.1 Nghiệm thu từng bảng

- [ ] Có mục trong `db-spec/<module>.md` theo đúng template §3.6
- [ ] **Mọi** cột có mô tả nghiệp vụ **và** nguồn dữ liệu (Rule 1/Rule 3)
- [ ] Có đủ bộ trường base theo §3.3, đúng base class theo bảng phân loại
- [ ] Có `tenant_id` (+ `chi_nhanh_id` nếu là bảng gốc do người dùng lập)
- [ ] Mọi cột numeric dùng domain type §3.4, không có `numeric(x,y)` trần
- [ ] Đủ 7 mục hạ tầng §3.5 (11 mục nếu là bảng sổ)
- [ ] `COMMENT ON TABLE` + `COMMENT ON COLUMN` khớp nguyên văn LDM
- [ ] Dòng tương ứng trong `90-doi-chieu.md` đã cập nhật trạng thái

### 7.2 Nghiệm thu từng PR migration

```bash
cd cell-app && ./gradlew unitTest
```

- [ ] `grep -rn "<tên bảng cũ>" cell-app/src` không còn kết quả ngoài chính file migration
- [ ] `git status` sạch — không còn file `??` trong `src/main/java` hay `src/main/resources`
- [ ] Migration chạy được **và** rollback được trên bản sao production
- [ ] Query kiểm constraint/index còn mang tên cũ (§6.1 của `docs/chuan-hoa-ten-bang-chung-tu.md`) trả về rỗng
- [ ] Đo được thời gian giữ `ACCESS EXCLUSIVE lock`

### 7.3 Nghiệm thu toàn kế hoạch

- [ ] 206/206 entity LDM có dòng trong `90-doi-chieu.md` với hành động rõ ràng
- [ ] Không còn bảng nhóm B nào lệch LDM
- [ ] 12/12 câu Q1–Q12 đã chốt và ghi vào `00-chuan-chung.md`
- [ ] Mọi BR bị lệch đã được báo cho user và ghi rõ trong tài liệu

---

## 8. BR đã áp dụng

| BR | Áp dụng ở |
|---|---|
| **BR7** — Precision & làm tròn | §3.4 — 5 domain type khớp đúng bảng 7.1 |
| **BR12** — Trạng thái chứng từ | §3.3.2 `BaseChungTuEntity.status`; Q7 |
| **BR17** — Kiểm tra kỳ kế toán | §3.5 mục 11 — trigger period-guard |
| **BR19** — Kiểm tra trùng | §3.5 mục 6 — UNIQUE partial `WHERE da_xoa = false` |
| **BR20** — Số chứng từ & mã danh mục | §3.4 — `varchar(50)` |
| **BR28** — Multi-tenant | §3.3.3, §3.5 mục 2 — `tenant_id` + RLS |
| **BR29** — Chính sách xóa | §3.3.2 — xóa mềm qua `da_xoa`/`ngay_xoa`/`nguoi_xoa` ở `BaseEntity` |
| **BR36** — Ghi nhận bút toán vào Sổ cái | §2.4.1, §2.4.2, Pha 2.1 |
| **BR42** — Bỏ ghi sổ | §3.3.2 — `nguoi_ghi_so`/`thoi_gian_ghi_so` về `null` |
| **BR46** — Trường hệ thống bắt buộc | §3.3 toàn bộ |
| **BR46.4** — `TenantId`/`ChiNhanhId` | §3.3.3 |
| **BR47** — Dữ liệu mặc định danh mục | Ngoài phạm vi (thuộc `ldm-DanhMuc-Update.puml`) |

**BR chưa đạt / cần user quyết:**

| BR | Vấn đề |
|---|---|
| **BR46** | LDM và code đang lệch tên trường base theo 4 cách khác nhau — Q1 |
| **BR7** | LDM yêu cầu numeric NOT NULL DEFAULT 0; `acc_so_cai` đang ghi `null` — Q12 |
| **BR12** | `ldm-BanHang-Update` thu hẹp trạng thái còn 2 giá trị, hẹp hơn BR12 — Q7 |

---

## 9. Tham chiếu

- [`pmkt-docs/ba/Common/LDM_update/`](../ba/Common/LDM_update/) — nguồn chuẩn 206 entity
- [`pmkt-docs/ba/Common/LDM_update/QuytacmotaEntity.md`](../ba/Common/LDM_update/QuytacmotaEntity.md) — Rule 1–5
- [`pmkt-docs/ba/Common/business_rules.md`](../ba/Common/business_rules.md) — BR1–BR47
- `docs/chuan-hoa-ten-bang-chung-tu.md` — đợt rename 52 bảng (phụ thuộc Q10)
- `docs/doing/ghi-so-kho-kernel-plan.md` — kernel ghi sổ kho (mâu thuẫn ở Q5)
- `docs/be-khung-kien-truc-chuan.md` — khung kiến trúc backend
- `docs/conventions.md` — quy ước đặt tên
- `cell-app/src/main/java/vn/vtt/pmkt/cell/core/entity/` — 5 base class đang chạy

---

## 10. Dọn bảng thừa & dựng lại bộ migration sạch

> **Trạng thái:** `CHỜ USER DUYỆT — CHƯA CHẠY BẤT KỲ LỆNH NÀO`
> **Khảo sát:** migration V373 · 323 file · 39.037 dòng · 235 bảng sống
> Mục tiêu user đặt ra: *xóa hết bảng thừa và sai tên, giữ bảng chuẩn đang dùng, tạo lại bộ migration sạch.*

### 10.0. Cổng go/no-go — ba câu phải trả lời trước khi chạy

Không câu nào tự suy ra được từ code; đây là thông tin chỉ phía vận hành có.

| # | Câu hỏi | Vì sao chặn |
|---|---|---|
| **G1** | **Có môi trường nào đang mang dữ liệu thật không** (production · staging · UAT · demo khách hàng)? | Quyết định toàn bộ cách làm. Có dữ liệu thật ⇒ **không** được squash rồi wipe; phải đi đường B (§10.3) chậm và hẹp hơn nhiều. Repo chỉ thấy `deploy/k8s-sim`, `deploy/lightsail-sim`, `SPRING_PROFILES_ACTIVE=local` — **không đủ để kết luận là chưa có prod**. |
| **G2** | Ai được phép `DROP TABLE` và trong cửa sổ nào? Có bản backup khôi phục được không, đã test restore chưa? | `DROP` không rollback được bằng migration. Không có backup đã test restore ⇒ không chạy. |
| **G3** | Đợt rename 52 bảng ở `docs/chuan-hoa-ten-bang-chung-tu.md` (Q10) gộp vào đợt này hay chạy riêng? | Gộp thì rẻ hơn nhiều (một lần dựng lại baseline là xong cả rename). Tách thì phải rename hai lần. |

**Chưa có G1 và G2 thì dừng ở đây.** Mọi bước dưới đều giả định đã trả lời.

### 10.1. Vì sao KHÔNG chốt được danh sách xóa bằng phân tích tĩnh

Tôi đã chạy thử phép lọc "bảng không có entity LDM + không có JPA entity + không bị Java nhắc tên" → ra **32 ứng viên xóa**. Rà tiếp thì **14/32 vẫn đang sống**:

| Bảng | Bằng chứng còn sống |
|---|---|
| `sal_chi_tiet_chung_tu_ban_dv` · `sal_chi_tiet_hoa_don_dieu_chinh` | migration **V367** vừa động vào |
| `ccdc_chung_tu_lien_quan` · `pur_hoa_don_tham_chieu` · `pur_dcgm_tham_chieu` | migration **V366** |
| `mst_khach_hang_to_chuc` · `mst_nha_cung_cap_to_chuc` · `mst_to_chuc` | migration **V365** |
| `mst_giao_dich_chung_tu` | **V354** — và là nguồn của `giao_dich_chung_tu_id` trên `BaseChungTuEntity` |
| `inv_phieu_nhap_xuat` | **V351** |
| `iam_bang_pham_vi` (15 lượt) · `iam_bang_khong_pham_vi` · `iam_don_vi_cay` · `iam_tenant_to_chuc_loi` | **V312–V330** — bộ máy phạm vi quyền, dùng từ **SQL function/view**, không phải từ Java |
| `event_publication` | Bảng của **Spring Modulith**, framework tự dùng — xóa là vỡ event |

**Bài học cho kế hoạch:** một bảng có thể sống hoàn toàn ở tầng SQL (function · view · RLS policy · trigger) mà không xuất hiện dòng Java nào. Grep Java là **điều kiện cần, không đủ**. Danh sách xóa cuối cùng bắt buộc phải có **bằng chứng từ DB thật** (§10.6 bước 2), không được chốt từ đọc code.

Cùng lúc phát hiện một sai số trong chính bản khảo sát này: **235 bảng sống, không phải 237** — `am_cong_cu_dung_cu` và `cst_doi_tuong_tap_hop_vat_tu` đã `RENAME TO` sang tên khác nên không còn tồn tại dưới tên cũ, nhưng bị đếm hai lần. Đã sửa ở §0 và §2.

### 10.2. Bốn tập bảng — trạng thái sau khi rà

| Tập | Nghĩa | Số lượng | Hành động |
|---|---|---:|---|
| **GIỮ** | Có entity LDM **hoặc** có JPA entity **hoặc** bị Java/SQL nhắc | ~203 | Bê nguyên sang baseline mới |
| **ĐỔI TÊN** | Tên hiện tại lệch chuẩn ([`db-spec/90-doi-chieu.md`](db-spec/90-doi-chieu.md)) | **74** | Dựng thẳng bằng tên mới trong baseline — **không** cần `ALTER … RENAME` |
| **XÓA** | Ứng viên chết, còn phải xác minh bằng dữ liệu thật | ≤ 18 | Chỉ xóa sau khi qua §10.6 bước 2 |
| **TẠO MỚI** | Có trong LDM, chưa có bảng | **70** | Nằm ngoài đợt này — thuộc Pha 2/3 của §5 |

> **Không gộp "tạo mới 70 bảng" vào đợt dọn.** Dọn + đổi tên là thao tác *cơ học, kiểm chứng được*. Tạo bảng mới là *thiết kế*, phụ thuộc Q1–Q12 chưa chốt. Trộn hai loại vào một đợt thì khi hỏng không biết hỏng vì đâu.

### 10.3. Hai kịch bản — chọn theo G1

#### Đường A — chưa có dữ liệu thật *(nhanh, sạch, khuyến nghị nếu G1 = không)*

Squash toàn bộ 323 migration thành **một baseline mới `V1__baseline.sql`**, dựng thẳng bằng tên chuẩn, bỏ hẳn bảng chết.

| Bước | Việc |
|---|---|
| A1 | Dựng DB trống → chạy hết 323 migration hiện có → có schema "thật" đang chạy |
| A2 | `DROP` các bảng đã xác minh chết (§10.6 bước 2) · `ALTER … RENAME` 74 bảng sai tên |
| A3 | `pg_dump --schema-only --no-owner --no-privileges` → **đây là baseline mới** |
| A4 | Ghép seed (32 file, 8.355 dòng) thành `V2__seed.sql` |
| A5 | Xóa 323 file cũ, thay bằng 2 file mới; giữ `db/rollback/` làm lịch sử |
| A6 | Dựng lại DB trống từ baseline mới → **so schema với A2 phải khớp 100%** |

#### Đường B — có dữ liệu thật *(bắt buộc nếu G1 = có)*

**Không squash.** Lịch sử migration là hợp đồng với các DB đang chạy — thay nó thì Flyway `validate` đỏ toàn bộ, và `flyway repair` chỉ vá được checksum chứ không vá được schema đã lệch.

| Bước | Việc |
|---|---|
| B1 | Migration mới `V374+`: `DROP TABLE` từng bảng chết, mỗi bảng một câu, có `COMMENT` nêu bằng chứng |
| B2 | Migration `V375+`: `ALTER … RENAME` 74 bảng, chia theo module mỗi module một file (theo `docs/chuan-hoa-ten-bang-chung-tu.md` §6) |
| B3 | Rename xong phải rename luôn constraint/index/policy — Postgres **giữ nguyên tên cũ** sau khi rename bảng |
| B4 | Squash để sau, khi có cửa sổ dựng lại toàn bộ môi trường |

> Đường B **không đạt được** mục tiêu "bộ migration sạch không thừa" — chỉ đạt "bảng sạch". Số file migration sẽ tăng chứ không giảm. Đây là cái giá của việc đã có dữ liệu thật.

### 10.4. Dựng baseline bằng `pg_dump`, KHÔNG gộp tay

39.037 dòng SQL tích lũy qua 323 file, trong đó rất nhiều lệnh `ALTER` chồng lên nhau (thêm cột rồi đổi kiểu rồi đổi tên). Gộp tay là chép lại lịch sử, không phải chép lại kết quả — và chắc chắn sai ở đâu đó không ai phát hiện được.

**Chỉ `pg_dump` mới bảo đảm baseline == schema thật.** Đây là lý do bước A6 (dựng lại rồi so schema) là bắt buộc, không phải tùy chọn.

### 10.5. Checklist bảo toàn — thứ dễ mất khi squash

`pg_dump --schema-only` bắt được phần lớn, nhưng phải soát tay đủ 9 mục:

| # | Đối tượng | Số lượng | Rủi ro nếu mất |
|---|---|---:|---|
| 1 | `CREATE FUNCTION` | 108 | Trigger/policy gọi vào sẽ vỡ lúc chạy, không vỡ lúc migrate |
| 2 | `CREATE POLICY` (RLS) | 240 | **Rò dữ liệu xuyên tenant** — hỏng nghiêm trọng nhất, và im lặng |
| 3 | `CREATE TRIGGER` | 228 | Mất audit · mất period-guard · mất chặn sửa dòng sổ |
| 4 | `CREATE INDEX` | 502 | Không sai kết quả, nhưng chậm dần tới mức không dùng được |
| 5 | `CREATE VIEW` | 12 | Báo cáo vỡ |
| 6 | `CREATE DOMAIN` | 5 | Mất chuẩn precision BR7 (§3.4) |
| 7 | `CREATE TYPE` | 2 | |
| 8 | Bảng partition | 6 — `acc_so_cai` · `acc_so_thue_dau_ra` · `acc_so_thue_dau_vao` · `acc_so_xuat_nhap_tong_hop` · `aud_audit_log` · `ops_outbox_event` | Mất partition con ⇒ dữ liệu rơi hết vào `_default`, truy vấn theo kỳ chậm dần |
| 9 | Role & password | `pmkt_app` / `pmkt_dev` | `V1__baseline` hiện tạo role kèm password literal rồi `FlywayConfig` rotate lại. Baseline mới **phải giữ nguyên cơ chế này**, tuyệt đối không nhúng secret vào SQL versioned |

> Mục 2 là mục nguy hiểm nhất: thiếu một `CREATE POLICY` thì không có lỗi nào báo — chỉ là tenant này đọc được dữ liệu tenant kia. Nghiệm thu phải đếm policy trước/sau, không chỉ đếm bảng.

### 10.6. Trình tự thực hiện

| Bước | Việc | Đầu ra | Ai |
|---|---|---|---|
| 1 | Trả lời G1–G3 | Quyết định đường A hay B | User + vận hành |
| 2 | **Xác minh bảng chết bằng dữ liệu thật** — với mỗi ứng viên: `count(*)`, `pg_stat_user_tables.seq_scan + idx_scan`, và tra `pg_depend` xem có function/view/FK nào phụ thuộc | Danh sách xóa **cuối cùng**, mỗi dòng kèm bằng chứng | Dev BE + DBA |
| 3 | User duyệt danh sách xóa | Ký nhận từng bảng | User |
| 4 | Backup + **test restore** trên máy khác | Bản backup đã chứng minh khôi phục được | DBA |
| 5 | Chạy đường A hoặc B | Migration mới | Dev BE |
| 6 | Nghiệm thu §10.7 | Báo cáo đối chiếu | Dev BE |

**Bước 2 là bước tốn công nhất và không rút ngắn được.** Kết quả §10.1 cho thấy rà bằng mắt trên code sai 14/32 lần.

### 10.7. Nghiệm thu

- [ ] Dựng DB trống từ bộ migration mới → schema **khớp 100%** với schema sau bước A2 (so bằng `pg_dump --schema-only` rồi `diff`, không so bằng mắt)
- [ ] Số lượng khớp: bảng · **policy (240)** · trigger (228) · function (108) · index (502) · domain (5) · partition con
- [ ] `cd cell-app && ./gradlew unitTest` xanh
- [ ] `./gradlew build` xanh trên CI có Docker — máy dev không có Docker thì ~25 test Testcontainers luôn đỏ, đối chiếu danh sách lớp lỗi trước khi kết luận
- [ ] `grep -rn "<tên bảng cũ>" cell-app/src` rỗng với cả 74 bảng đổi tên
- [ ] Không còn tên constraint/index mang tên bảng cũ; không tên nào ≥ 63 ký tự
- [ ] App khởi động, mở được màn chứng từ bán hàng và mua hàng (hai luồng đã có code) — `ddl-auto: none` nên sai cột chỉ lộ lúc mở màn hình
- [ ] Kiểm RLS bằng test thật: đăng nhập tenant A, xác nhận **không** đọc được dữ liệu tenant B

### 10.8. Việc KHÔNG làm trong đợt này

| Không làm | Vì sao |
|---|---|
| Tạo 70 bảng nhóm C | Phụ thuộc Q1–Q12 chưa chốt; là thiết kế chứ không phải dọn dẹp |
| Đổi tên **cột** theo BR46 (Q1) | Đợt riêng, chạm mọi entity Java |
| Vá 29 cột thiếu của `acc_so_cai` | Pha 4.4 — có dữ liệu thật, rủi ro cao nhất, làm riêng |
| Xóa bảng chỉ vì "không thấy trong LDM" | LDM không phủ bảng hạ tầng (`event_publication`, `agg_*`, `aud_*`, `ctu_*`) |
| Sửa `master_data/**` | Vùng đóng băng — trừ khi user cho phép gỡ `permissions.deny` |
