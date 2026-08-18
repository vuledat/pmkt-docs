# Kế hoạch triển khai API — Điều chỉnh giá hàng bán (PMKT-E-07664)

> **Trạng thái:** BẢN NHÁP CHỜ REVIEW — chưa code gì
> **Ngày cập nhật:** 2026-08-14
> **Người review cần có:** 1 BA (chốt §12) + 1 Dev BE/DBA (chốt §7, §9, §10)

| Mục | Nội dung |
|---|---|
| Use case | PMKT-U-07665 Xem danh sách · U-07666 Thêm mới · U-07667 Xem chi tiết · U-07668 Xóa · U-07669 Ghi sổ · U-07670 Bỏ ghi sổ · U-07671 Sửa |
| Màn hình | `SCR_DanhSachDieuChinhGia` · `SCR_ThemMoiDieuChinhGia` · `SCR_SuaDieuChinhGia` · `SCR_XemChiTietDieuChinhGia` |
| Tài liệu nguồn | `pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/` + `pmkt-docs/ba/Common/business_rules.md` |
| Module BE | `cell-app/src/main/java/vn/dopai/pmkt/cell/dieu_chinh_gia_hang_ban/` (**tạo mới**) |
| Bảng DB | `sal_chung_tu_dieu_chinh_gia_hang_ban` (**đã có 63 cột**) · `sal_chung_tu_dieu_chinh_gia_hang_ban_chi_tiet` (**đã có 39 cột**) |
| Kế hoạch FE đối ứng | `docs/doing/PMKT-E-07664-dieu-chinh-gia-hang-ban-fe/IMPLEMENT.md` — FE **đã code xong trên mock**, đã khai sẵn 11 endpoint |

---

## 0. Các quyết định đã chốt

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Module mới `cell/dieu_chinh_gia_hang_ban/` theo shape Modulith `internal/` (KHÔNG có `api/`), kế thừa `BaseChungTuController` + `AbstractChungTuCrudService` + `ChungTuTemplate` y như `chung_tu_ban_hang/` | 11/17 endpoint là kế thừa, không viết lại (§4). Luồng ghi/sửa/xoá/ghi sổ đi qua `ChungTuTemplate.thucThi` ([ChungTuTemplate.java:103](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)) → thứ tự bước là bất biến, không tự viết. **Không chọn** đặt màn này thành sub-package của `chung_tu_ban_hang/`: module đó đang là shape `internal/` đầy đủ nhưng gộp vào sẽ biến nó thành module hai nghiệp vụ, và mọi entity/DTO của điều chỉnh giá sẽ nhìn thấy `internal/` của bán hàng — mất đúng ranh giới mà Modulith giữ |
| **D2** | Module mới **dùng chung tiền tố bảng `sal_`** với `chung_tu_ban_hang` | Lệch quy ước "mỗi module một tiền tố" (`docs/be-khung-kien-truc-chuan.md` §6). Lý do: hai bảng đã tồn tại trong baseline với tên `sal_chung_tu_dieu_chinh_gia_hang_ban*` ([V1__baseline.sql:16257](../../cell-app/src/main/resources/db/migration/V1__baseline.sql), :16411) và đã có RLS/policy/trigger/FK gắn theo tên đó. **Không chọn** đổi tên bảng sang tiền tố mới: một lần rename kéo theo 2 policy set, 4 trigger, 6 FK, 5 index và toàn bộ comment — chi phí lớn hơn giá trị của một tiền tố. Phải ghi rõ ở `package-info.java` |
| **D3** | Ghi sổ **chỉ sinh bút toán sổ cái** qua `GhiSoApi` ([GhiSoApi.java:31](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/hach_toan/api/GhiSoApi.java)). **KHÔNG** tạo bản ghi Phiếu thu / Phiếu chi / Giấy báo / Séc / Hóa đơn điều chỉnh | UC_GhiSo yêu cầu 6 tác động nguyên tử, nhưng BE hiện **không có** module nào của `cb_phieu_thu`, `cb_phieu_chi`, `sal_hoa_don_ban_hang`, `sal_dieu_chinh_hoa_don_ban_hang` (bằng chứng §2.1). Bút toán 2 (Nợ 131 / Có TK tiền, hoặc ngược lại) **vẫn sinh đủ** từ `tai_khoan_tien_id` trên header, nên sổ cái đúng; phần thiếu là *bản ghi phiếu* để người dùng thấy ở màn Tiền mặt. Xem §1.2, R1, §12-Q2 |
| **D4** | Liên kết chứng từ nguồn ↔ chứng từ điều chỉnh đi qua `QuanHeChungTuApi`, **mức DÒNG**, loại đích `LoaiChungTu.SAL_DIEU_CHINH_GIA_HANG_BAN` ([LoaiChungTu.java:31](../../cell-app/src/main/java/vn/dopai/pmkt/cell/quan_he_chung_tu/api/LoaiChungTu.java)) | "Lưu ý quan trọng §1" của SCR (dòng 610-611) đòi liên kết cả 3 chứng từ để tính được giá trị còn lại của từng dòng — khoá liên kết phải ở mức dòng. `laTieuThu()` của loại này là `false` ([LoaiChungTu.java:65](../../cell-app/src/main/java/vn/dopai/pmkt/cell/quan_he_chung_tu/api/LoaiChungTu.java)) nên **không** áp ràng buộc "Σ tiêu thụ ≤ số lượng nguồn" — một dòng bán hàng được điều chỉnh giá nhiều lần là hợp lệ. **Không chọn** chỉ dùng cột FK `chi_tiet_chung_tu_ban_hang_id` trên bảng chi tiết: cột đó chỉ nối được 2 chứng từ, không mô tả được chuỗi CTBH → HĐ điều chỉnh → CT điều chỉnh giá |
| **D5** | Module phải cài `DongChungTuPort` cho loại của mình | Bắt buộc — `laySoLuong` của bảng này trả `COALESCE(so_luong_tang, so_luong_giam)`, đúng như javadoc của port đã ghi sẵn ([DongChungTuPort.java:54](../../cell-app/src/main/java/vn/dopai/pmkt/cell/quan_he_chung_tu/api/DongChungTuPort.java)). Thiếu bean này thì tab "Chứng từ liên quan" của CTBH không hiển thị được chứng từ điều chỉnh giá |
| **D6** | Giữ nguyên cặp cột `so_luong_tang/giam`, `don_gia_tang/giam`, `thanh_tien_tang/giam`, `chiet_khau_*_tang/giam` của bảng chi tiết; DTO **phẳng** (`soLuong`, `donGia`, `thanhTien`) do mapper chọn khối theo `loai_dieu_chinh` của header | Khớp `model.ts` của FE (`dieuChinhGiaChiTietSchema` — `soLuong`/`donGia`/`thanhTien` một bộ). **Không chọn** thêm cặp cột phẳng mới: base `DongChungTuPort` đã viết sẵn quy ước COALESCE cho đúng bảng này, đổi shape là làm hỏng hợp đồng đã có |
| **D7** | Cột `trang_thai_chung_tu text NOT NULL CHECK ('Chưa ghi sổ','Đã ghi sổ')` bị **DROP** ở migration V3; trạng thái chỉ còn ở cột `status` (`TrangThaiChungTu`) do `BaseChungTuEntity` quản | Có tiền lệ: cột cùng tên của luồng bán hàng đã bị DROP ở V309 (ghi trong javadoc [TrangThaiChungTu.java](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/entity/TrangThaiChungTu.java)). Giữ cả hai = hai nguồn sự thật cho cùng một trạng thái, và `NOT NULL` + CHECK chuỗi tiếng Việt sẽ nổ ngay ở INSERT đầu tiên của entity mới |
| **D8** | Thuế suất lưu bằng **enum text** (`thue_suat_gtgt_mac_dinh` + `gia_tri_thue_gtgt`) như `sal_chung_tu_ban_hang_chi_tiet`, cột `thue_suat_gtgt_id` hiện có để **deprecate** (không dùng, không xoá lần này) | FE gửi `thueSuatGtgt: '0'\|'5'\|'8'\|'10'\|'KCT'\|'KKKNT'\|'KHAC'` + `giaTriThueGtgt`, và `BR_KhongTongHopToKhaiGTGT` quyết định theo chính bộ mã đó. **Không chọn** FK vào danh mục thuế suất: mọi luật của epic (`KHAC`/`KKKNT` ⇒ tick "không tổng hợp tờ khai") viết theo mã, tra danh mục để suy ra mã là thêm một chỗ lệch được |
| **D9** | Enum `ThueSuatGtgt` **khai lại** trong `internal/model/` của module mới | `chung_tu_ban_hang/internal/model/ThueSuatGtgt.java` nằm trong `internal/` của module khác — Modulith cấm import. **Không chọn** import xuyên `internal/`: module mới phải sạch tuyệt đối về ranh giới ngay từ đầu (`be-khung-kien-truc-chuan.md` §7 luật 2). Đề xuất nâng enum lên `accounting_core` là ticket riêng — xem R4 |
| **D10** | Ba endpoint "chọn nguồn" (`/nguon/*`) đặt trong **cùng controller**, đúng tên FE đã khai | FE đã code và khai cứng 11 đường dẫn (`IMPLEMENT.md` dòng 178-188). Đổi tên đường dẫn = FE phải sửa 3 file hợp đồng. **Không chọn** tách controller riêng: chúng phục vụ đúng một màn và dùng chung mã quyền `DieuChinhGiaHangBan.Create` |
| **D11** | Mã loại chứng từ (`maLoaiChungTu`) = **`CTDG`**, seed mới vào `mst_loai_chung_tu` | `ChungTuTemplate.maLoaiChungTu()` là bắt buộc với mọi chứng từ kể cả loại không sinh bút toán ([ChungTuTemplate.java:272](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)); chốt chặn kỳ khoá ở cả Java lẫn trigger DB đọc mã này. Danh sách seed hiện có 20 mã, **không có mã nào cho điều chỉnh giá** (§2.2), BR09 cũng không liệt kê → **`CTDG` là đề xuất của dev, cần BA chốt (§12-Q1)** |
| **D12** | Số chứng từ **do người dùng nhập** (không tự sinh) | BR20.2: "Cho phép user nhập tay"; SCR khai ô "Số chứng từ" bắt buộc, max 50, ở cả tab Công nợ lẫn tab thanh toán. Vì vậy **không** gọi `sinhSoChungTu` ([ChungTuTemplate.java:322](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)); chống trùng dựa vào unique index đã có `uq_sal_dcg_so_ct` ([V1__baseline.sql:23661](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)) + kiểm sớm ở service để trả `MSG_PMKT-E-07664_109` |

> ⚠️ **Cảnh báo môi trường:** repo có **việc song song** trong cùng domain bán hàng (`traLaiHangBan`, `hoaDonBanHang` phía FE — ghi ở `IMPLEMENT.md` §7). Trước khi code, đọc lại chữ ký `BaseChungTuController`, `ChungTuTemplate`, `QuanHeChungTuApi` — đây là ba lớp base mà kế hoạch này bám chặt nhất.

---

## 1. Phạm vi

### 1.1 Trong phạm vi

| # | Chức năng | Nguồn | File con |
|---|---|---|---|
| F1 | Xem danh sách + tìm kiếm/lọc/sắp xếp/phân trang + dòng tổng | UC-07665, `SCR_DanhSachDieuChinhGia` | [01](01-xem-danh-sach.md) |
| F2 | Xem chi tiết + dòng chi tiết + bút toán đã ghi + nhân bản | UC-07667, `SCR_XemChiTietDieuChinhGia` | [02](02-xem-chi-tiet.md) |
| F3 | Thêm mới (Lưu / Lưu và ghi sổ) | UC-07666, `SCR_ThemMoiDieuChinhGia` | [03](03-them-moi.md) |
| F4 | Chỉnh sửa chứng từ chưa ghi sổ | UC-07671, `SCR_SuaDieuChinhGia` | [04](04-chinh-sua.md) |
| F5 | Xóa (đơn + hàng loạt) | UC-07668 | [05](05-xoa.md) |
| F6 | Ghi sổ (đơn + hàng loạt) | UC-07669 | [06](06-ghi-so.md) |
| F7 | Bỏ ghi sổ (đơn + hàng loạt) | UC-07670 | [07](07-bo-ghi-so.md) |
| F8 | Chọn chứng từ nguồn (Bước 1 của màn Thêm mới) | `SCR_ThemMoiDieuChinhGia` Bước 1 (dòng 18-172) | [08](08-chon-nguon-chung-tu.md) |
| F9 | Migration + seed (mã loại chứng từ, quyền `.Clone`) | §7, §10 | [09](09-thiet-ke-db.md) |

### 1.2 NGOÀI phạm vi (không cài lần này)

Không có UC nào bị loại nguyên vẹn — bảy UC đều được cài. Bị loại là các **tác động phụ** mà UC_GhiSo/UC_BoGhiSo mô tả nhưng không có module BE để đáp:

| Bị loại | Bằng chứng | Endpoint kế thừa trả gì |
|---|---|---|
| Sinh bản ghi **Phiếu thu / Phiếu chi / Giấy báo Có / Séc TM / Séc CK / UNC** khi "Thanh toán ngay" (UC_GhiSo, Hậu điều kiện) | `grep -rl "PhieuThu" --include="*.java"` chỉ trúng `chung_tu_ban_hang` (dùng cột `phieu_thu_id`), **không có module `cb_*`** — §2.1 | `/ghi-so` vẫn 200; bút toán 2 sinh đủ; các cột `phieu_thu_id`/`phieu_chi_id`/… giữ `NULL` |
| Sinh **Hóa đơn điều chỉnh** khi tick "Lập kèm hóa đơn điều chỉnh" (SCR "Lưu ý quan trọng" §2) | Không có module Java nào của `sal_dieu_chinh_hoa_don_ban_hang` / `sal_hoa_don_ban_hang` — §2.1 | Cờ `lapKemHoaDonDieuChinh` + toàn bộ trường tab Hóa đơn **được lưu**; `hoa_don_dieu_chinh_id` giữ `NULL`; validate `MSG_206` vẫn chạy |
| **Cập nhật sổ thuế đầu ra** (UC_GhiSo, Hậu điều kiện) | Không có module sổ thuế trong `cell/` | Cột `khong_tong_hop_to_khai_gtgt` **được lưu** để module thuế sau này đọc |
| **Cập nhật tồn quỹ / ngân hàng** | Hệ quả của việc không sinh phiếu thu/chi | — |
| Tab **Thuế · Hạch toán · Đính kèm · Tham chiếu** (SCR dòng 563-568 — "tham chiếu tab của chứng từ bán hàng") | FE cũng chưa dựng (`IMPLEMENT.md` §5.3) | Bút toán *đã ghi* vẫn đọc được qua `/thong-tin-hach-toan` |
| **Xuất Excel / Nhập Excel** | `DanhSachQuyen.md §B4.6` không bật quyền Xuất Excel (dẫn ở `IMPLEMENT.md` dòng 312) | `/export`, `/import` kế thừa từ `BaseCrudController` ([:171](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/controller/BaseCrudController.java), [:197](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/controller/BaseCrudController.java)) vẫn tồn tại nhưng **403** vì `DieuChinhGiaHangBan.Export/.Import` không được seed |
| **Chiết khấu thương mại** (BR14, SCR dòng 488-493) và **ĐVT quy đổi** (BR13, dòng 487) | Bảng trường của lưới không có ô "Chiết khấu thương mại"; BR13 chỉ có một dòng chữ | §12-Q6, Q7 |

---

## 2. Hiện trạng đã khảo sát

### 2.1 Code hiện có — **GREENFIELD ở tầng Java**

```bash
grep -rniE "dieu_chinh_gia|dieuchinhgia" cell-app/src/main -l
```
```
cell-app/src/main/resources/db/seed/iam_quyen_full_639_ba.sql
cell-app/src/main/resources/db/migration/V1__baseline.sql
cell-app/src/main/resources/db/migration/V2__seed_toan_cuc.sql
cell-app/src/main/java/.../quan_he_chung_tu/api/LoaiChungTu.java
cell-app/src/main/java/.../quan_he_chung_tu/api/DongChungTuPort.java
cell-app/src/main/java/.../quan_he_chung_tu/api/QuanHeChungTuApi.java
cell-app/src/main/java/.../common/constant/MaChucNang.java
cell-app/src/main/java/.../master_data/...   ← vùng đóng băng, BỎ QUA
```

**Kết luận:** không có module Java nào cho nghiệp vụ này. Ba file `quan_he_chung_tu/api/*` chỉ **nhắc tên** chứng từ điều chỉnh giá trong enum/javadoc — tức hạ tầng liên kết đã dọn sẵn chỗ, chưa có ai cắm vào.

```bash
ls cell-app/src/main/java/vn/dopai/pmkt/cell/
```
```
accounting_core  chung_tu_ban_hang  chung_tu_mua_hang  common  core
integration_ops  master_data  platform_iam  quan_he_chung_tu  reporting
```

**Kết luận thứ hai (quyết định D3):** không có module nào cho phiếu thu/chi (`cb_*`), hóa đơn bán hàng (`sal_hoa_don_ban_hang`), hóa đơn điều chỉnh (`sal_dieu_chinh_hoa_don_ban_hang`), chứng từ bán dịch vụ, hay chứng từ trả lại hàng bán. Bảng của chúng **đã có trong baseline** nhưng chưa có tầng Java.

Hệ quả trực tiếp lên §8 (chọn nguồn): công thức BR2 của SCR ("Số lượng = SL trên CTBH − SL đã trả lại", có quy đổi ĐVT) phải đọc `sal_chung_tu_tra_lai_hang_ban_chi_tiet` **bằng SQL native / view**, vì không có repository nào của module đó để gọi.

### 2.2 Hiện trạng DB

```bash
ls cell-app/src/main/resources/db/migration/
```
```
V1__baseline.sql   V2__seed_toan_cuc.sql
```

**Số hiệu migration lớn nhất hiện tại: `V2` ⇒ file mới là `V3`.**

⚠ `db/rollback/` còn giữ file mang số tới `V340` — đó là **rollback của các migration đã bị squash vào baseline**, không phải migration đang chạy. Đừng đánh số theo thư mục đó.

Hai bảng chính **đã tồn tại đầy đủ** trong `V1__baseline.sql` (chi tiết ở [09-thiet-ke-db.md](09-thiet-ke-db.md)):

| Bảng | Dòng trong baseline | Số cột | Đã có |
|---|---|---|---|
| `sal_chung_tu_dieu_chinh_gia_hang_ban` | :16257 | 63 | PK, 4 CHECK, 1 CHECK status, unique `uq_sal_dcg_so_ct` (:23661), 3 index, RLS + policy phạm vi đơn vị (:29662, :30017, :30510), trigger audit (:25478) + trigger phạm vi (:26080, :26255), 6 FK |
| `sal_chung_tu_dieu_chinh_gia_hang_ban_chi_tiet` | :16411 | 39 | PK, index `idx_sal_ct_dcg_parent` (:21750), RLS tenant (:31677), trigger audit (:25436), FK cha `ON DELETE CASCADE` (:27985) + 3 FK nguồn |

| Bảng phụ (chỉ ĐỌC) | Vai trò | Cột khoá nối |
|---|---|---|
| `sal_chung_tu_ban_hang` + `_chi_tiet` | nguồn Bước 1 (loại "Chứng từ bán hàng, dịch vụ") | `chung_tu_ban_hang_id`, `chi_tiet_chung_tu_ban_hang_id` |
| `sal_chung_tu_ban_dich_vu` + `sal_chi_tiet_chung_tu_ban_dv` | nguồn Bước 1 (loại dịch vụ) | `chung_tu_ban_dich_vu_id`, `chi_tiet_chung_tu_ban_dich_vu_id` |
| `sal_dieu_chinh_hoa_don_ban_hang` + `sal_chi_tiet_hoa_don_dieu_chinh` | nguồn Bước 1 (loại "Hóa đơn điều chỉnh") | `hoa_don_dieu_chinh_id`, `chi_tiet_hd_ban_hang_id` |
| `sal_chung_tu_tra_lai_hang_ban_chi_tiet` | trừ ra "số lượng đã trả lại" (BR2) | `chung_tu_ban_id`, `chi_tiet_hd_ban_hang_id` |
| `ctu_quan_he_chung_tu` | liên kết dòng nguồn ↔ dòng đích (D4) | qua `QuanHeChungTuApi` |
| `mst_loai_chung_tu` | mã loại chứng từ (D11) | `code` |
| `iam_quyen` | 7 mã quyền đã seed, thiếu `.Clone` | `ma_quyen` |

### 2.3 Hạ tầng base đã có sẵn những gì

| Cần | Đã có ở base | Vị trí |
|---|---|---|
| 8 endpoint CRUD + tìm kiếm động + `/cot` + export/import | `BaseCrudController` | [core/controller/BaseCrudController.java:121-198](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/controller/BaseCrudController.java) |
| Ghi sổ / bỏ ghi sổ / nhân bản / bút toán đã ghi / dòng chi tiết / 3 thao tác hàng loạt | `BaseChungTuController` | [accounting_core/chung_tu/controller/BaseChungTuController.java:93,102,119,139,147,159,168,177](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/controller/BaseChungTuController.java) |
| Trình tự bất biến 5 luồng chứng từ | `ChungTuTemplate.thucThi` | [ChungTuTemplate.java:103](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java) (luồng: :149 tạo · :171 sửa · :194 xoá · :212 ghi sổ · :231 bỏ ghi sổ) |
| Hợp đồng service chứng từ (`ghiSo`/`boGhiSo`/`nhanBan`/`layDongChiTiet`/`traSoChungTu`/`kiemTraTonTai`) | `AbstractChungTuCrudService` | [accounting_core/chung_tu/service/AbstractChungTuCrudService.java:35-89](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/AbstractChungTuCrudService.java) |
| Ghi/gỡ bút toán sổ cái (đường DUY NHẤT) | `GhiSoApi.ghiSo` / `.boGhiSo` / `.daGhiSo` | [GhiSoApi.java:31,48,51](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/hach_toan/api/GhiSoApi.java) |
| Kiểm kỳ kế toán (BR17) | `KyKeToanApi.kiemTraKyMo` — **kernel tự gọi**, module không gọi lại | [KyKeToanApi.java:39](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/hach_toan/api/KyKeToanApi.java) |
| Định khoản Nợ/Có (kernel tự tách 2 dòng sổ cái → BR36) | `DinhKhoan.cua(...)`, `.voiChiTiet(...)`, `.voiNgoaiTe(...)` | [hach_toan/api/dto/DinhKhoan.java:56,68,79](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/hach_toan/api/dto/DinhKhoan.java) |
| Body tìm kiếm chuẩn (`page/pageSize/sort/keyword/filters/logic`) | `SearchRequest` | [core/request/SearchRequest.java:33](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/request/SearchRequest.java) |
| Envelope danh sách `{data, pagination, summary}` (BR31) | `PageResponse` | [core/response/PageResponse.java:20](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/response/PageResponse.java) |
| Whitelist lọc/sắp xếp | `@Searchable` + `SearchExecutor` + `DynamicSpecification` | `core/shared/search/` |
| Cột chứng từ dùng chung + `@Searchable` sẵn (`soChungTu`, `ngayChungTu`, `ngayHachToan`, `status`, `chiNhanhId`) | `BaseChungTuEntity` | [core/entity/BaseChungTuEntity.java:44-85](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/entity/BaseChungTuEntity.java) |
| Kiểm quyền `<MaChucNang>.<HanhDong>` | `QuyenChecker.require` | [core/controller/QuyenChecker.java:61](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/controller/QuyenChecker.java) |
| Mã chức năng đã khai sẵn | `MaChucNang.DIEU_CHINH_GIA_HANG_BAN = "DieuChinhGiaHangBan"` | [common/constant/MaChucNang.java:229](../../cell-app/src/main/java/vn/dopai/pmkt/cell/common/constant/MaChucNang.java) |
| Liên kết chứng từ đa hình | `QuanHeChungTuApi` + `LoaiChungTu.SAL_DIEU_CHINH_GIA_HANG_BAN` | [QuanHeChungTuApi.java:17](../../cell-app/src/main/java/vn/dopai/pmkt/cell/quan_he_chung_tu/api/QuanHeChungTuApi.java), [LoaiChungTu.java:31](../../cell-app/src/main/java/vn/dopai/pmkt/cell/quan_he_chung_tu/api/LoaiChungTu.java) |
| Dòng tổng toàn tập lọc (mẫu) | `ChungTuBanHangRepositoryImpl.tongHop` | [chung_tu_ban_hang/internal/repository/ChungTuBanHangRepositoryImpl.java:30,49](../../cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/internal/repository/ChungTuBanHangRepositoryImpl.java) |

**Quyền đã seed:** 7 mã, tại [iam_quyen_full_639_ba.sql:263-269](../../cell-app/src/main/resources/db/seed/iam_quyen_full_639_ba.sql) — `DieuChinhGiaHangBan.{Create, Delete, Edit, Post, Unpost, View, View.Detail}`.
⚠ `IMPLEMENT.md` của FE (dòng 191-192) ghi "7 mã quyền … chưa được seed" — **thông tin đó đã cũ**, chúng có trong file seed. Thiếu thật là `.Clone` (§10).

---

## 3. Kiến trúc

### 3.1 Phân tầng

```
DieuChinhGiaHangBanController                       extends BaseChungTuController<…>
        │  kế thừa 11 endpoint, override 3 CRUD chỉ để gắn messageId
        │  + 3 endpoint /nguon/* viết mới (D10)
        ▼
DieuChinhGiaHangBanCrudService                      extends AbstractChungTuCrudService<…>
        │  ├── kế thừa : search / cot / get / export (phần ĐỌC của core)
        │  ├── override: create · update · delete · ghiSo · boGhiSo · nhanBan · layDongChiTiet
        │  └── uỷ quyền: LuuDieuChinhGiaTemplate (5 hành động) — ChungTuTemplate
        ▼
DieuChinhGiaHangBanRepository                       extends BaseRepository<DieuChinhGiaHangBan>
   + DieuChinhGiaHangBanRepositoryCustom/Impl       (dòng tổng, nạp kèm chi tiết)
   + NguonDieuChinhGiaRepository                    (SQL native cho Bước 1 — §08)
        ▼
DieuChinhGiaHangBan                                 extends BaseChungTuEntity
   @Table("sal_chung_tu_dieu_chinh_gia_hang_ban")
   └─ @OneToMany cascade=ALL orphanRemoval  ChiTietDieuChinhGiaHangBan
                                            @Table("…_chi_tiet")
```

### 3.2 Lựa chọn kiến trúc + lý do

| | Phương án A — service tự viết CRUD + tự gọi `GhiSoApi` | **Phương án B (CHỌN) — kế thừa `BaseChungTuController` + `ChungTuTemplate`** |
|---|---|---|
| Số endpoint phải viết | 17 | 6 (3 override CRUD chỉ để gắn messageId + 3 endpoint nguồn) |
| Trình tự ghi sổ / bỏ ghi sổ | tự giữ, dễ lệch | bất biến do base cưỡng chế; 5 luồng `private`, lớp con không đảo được ([ChungTuTemplate.java:149-247](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)) |
| Kiểm kỳ kế toán (BR17) | phải tự nhớ gọi ở 5 chỗ | kernel `GhiSoApi` tự kiểm với đúng cặp (ngày, mã loại) sắp INSERT |
| Đối soát cờ trạng thái ↔ sổ cái | không có | `doiSoatVoiSoCai` chạy ở luồng sửa/xoá, trả 409 khi lệch |
| Thao tác hàng loạt (BR45) | tự viết 3 endpoint | có sẵn `HangLoatChungTuService` |
| Rủi ro | trôi khỏi chuẩn ngay từ sprint đầu | phải cài đủ hook trừu tượng, sai một hook là 500 lúc chạy → chốt bằng unit test cho từng hook (§16 các file con) |

### 3.3 Cấu trúc thư mục

```
cell/dieu_chinh_gia_hang_ban/
├── package-info.java                 @ApplicationModule(displayName = "dieu_chinh_gia_hang_ban")
│                                     + ghi rõ dùng chung tiền tố sal_ (D2)
└── internal/
    ├── adapter/
    │   └── DongDieuChinhGiaAdapter.java        cài DongChungTuPort (D5)
    ├── controller/
    │   └── DieuChinhGiaHangBanController.java  package-private
    ├── dto/
    │   ├── DieuChinhGiaHangBanDto.java
    │   ├── ChiTietDieuChinhGiaHangBanDto.java
    │   ├── ChungTuThanhToanDto.java            object con — tab thanh toán
    │   ├── HoaDonDieuChinhDto.java             object con — tab Hóa đơn
    │   ├── LuuDieuChinhGiaHangBanRequest.java
    │   ├── LuuChiTietDieuChinhGiaRequest.java
    │   ├── TongHopDieuChinhGiaDto.java         dòng tổng (BR31)
    │   ├── NguonDongDto.java   NguonChungTuDto.java   TimNguonRequest.java
    ├── entity/
    │   ├── DieuChinhGiaHangBan.java
    │   └── ChiTietDieuChinhGiaHangBan.java
    ├── model/
    │   ├── HuongDieuChinhGia.java     TangGia | GiamGia
    │   ├── HinhThucThanhToanDcg.java  8 giá trị theo CHECK của bảng
    │   ├── NguonChungTu.java          CTBH | HOA_DON_DIEU_CHINH
    │   ├── LoaiDieuChinhHoaDon.java   Điều chỉnh giá | Sai sót | Khác
    │   ├── ThueSuatGtgt.java          khai lại (D9)
    │   └── MaLoiDieuChinhGia.java     mã lỗi + messageId của epic
    ├── repository/
    │   ├── DieuChinhGiaHangBanRepository.java
    │   ├── DieuChinhGiaHangBanRepositoryCustom.java / …Impl.java
    │   └── NguonDieuChinhGiaRepository.java
    └── service/
        ├── DieuChinhGiaHangBanCrudService.java
        ├── DieuChinhGiaHangLoatService.java
        ├── NguonDieuChinhGiaService.java
        └── business/
            ├── LuuDieuChinhGiaTemplate.java   TaoDieuChinhGia · SuaDieuChinhGia · XoaDieuChinhGia
            ├── GhiSoDieuChinhGia.java  BoGhiSoDieuChinhGia.java  NhanBanDieuChinhGia.java
            ├── DinhKhoanDieuChinhGia.java     4 kịch bản bút toán
            ├── TinhToanDieuChinhGia.java      BR3 · BR10 · BR15 · BR18
            ├── KiemTraDieuChinhGia.java       ma trận validation
            ├── DieuChinhGiaMapper.java
            └── LienKetNguonDieuChinhGia.java  D4
```

---

## 4. Danh mục API mục tiêu

Base path: **`/api/ban-hang/dieu-chinh-gia-hang-ban`** · Mã chức năng: **`DieuChinhGiaHangBan`**

| # | Nguồn | Method | Path | Quyền | Trả về | File con |
|---|---|---|---|---|---|---|
| A1 | base | POST | `/search` | `.View` | `PageResponse<DieuChinhGiaHangBanDto>` | [01](01-xem-danh-sach.md) |
| A2 | base | GET | `/cot` | `.View` | `ApiResponse<List<CotMoTa>>` | [01](01-xem-danh-sach.md) |
| A3 | base (override) | GET | `/{id}` | `.View.Detail` | `ApiResponse<…Dto>` (kèm `chiTiet`) | [02](02-xem-chi-tiet.md) |
| A4 | base (override) | POST | `` (rỗng) | `.Create` | `201 ApiResponse<…Dto>` | [03](03-them-moi.md) |
| A5 | base (override) | PUT | `/{id}` | `.Edit` | `ApiResponse<…Dto>` | [04](04-chinh-sua.md) |
| A6 | base (override) | DELETE | `/{id}` | `.Delete` | `ApiResponse<Void>` | [05](05-xoa.md) |
| A7 | base | POST | `/{id}/ghi-so` | `.Post` | `ApiResponse<…Dto>` | [06](06-ghi-so.md) |
| A8 | base | POST | `/{id}/bo-ghi-so` | `.Unpost` | `ApiResponse<…Dto>` | [07](07-bo-ghi-so.md) |
| A9 | base | GET | `/{id}/dong-chi-tiet` | `.View.Detail` | `ApiResponse<List<ChiTiet…Dto>>` | [02](02-xem-chi-tiet.md) |
| A10 | base | GET | `/{id}/thong-tin-hach-toan` | `.View.Detail` | `ApiResponse<List<DongSoCaiDto>>` | [02](02-xem-chi-tiet.md) |
| A11 | base | GET | `/{id}/nhan-ban` | `.Clone` | `ApiResponse<…Dto>` | [02](02-xem-chi-tiet.md) |
| A12 | base | POST | `/ghi-so-hang-loat` | `.Post` | `ApiResponse<KetQuaHangLoatDto>` | [06](06-ghi-so.md) |
| A13 | base | POST | `/bo-ghi-so-hang-loat` | `.Unpost` | `ApiResponse<KetQuaHangLoatDto>` | [07](07-bo-ghi-so.md) |
| A14 | base | POST | `/xoa-hang-loat` | `.Delete` | `ApiResponse<KetQuaHangLoatDto>` | [05](05-xoa.md) |
| A15 | **mới** | POST | `/nguon/search` | `.Create` | `PageResponse<NguonDongDto>` | [08](08-chon-nguon-chung-tu.md) |
| A16 | **mới** | POST | `/nguon/chung-tu` | `.Create` | `PageResponse<NguonChungTuDto>` | [08](08-chon-nguon-chung-tu.md) |
| A17 | **mới** | POST | `/nguon/chung-tu/{id}/dong` | `.Create` | `ApiResponse<List<NguonDongDto>>` | [08](08-chon-nguon-chung-tu.md) |
| — | base, **không dùng** | POST | `/export`, `/import` | `.Export`, `.Import` | **403** — quyền không seed (§1.2) | — |
| — | base, **không dùng** | POST | `/them-moi` | `.Create` | trùng chức năng với A4; FE dùng A4 | — |

**Envelope lỗi**: `ApiResponse` chuẩn của dự án, dựng tập trung ở `core/config/GlobalExceptionHandler.java`; lỗi nghiệp vụ ném `ApiException.badRequest/conflict(maLoi, messageId, chiTiet)`.

**Quy ước enum trên wire**: **tên hằng Java** cho `trangThaiChungTu` (`NHAP`/`DA_GHI_SO`/… — FE đã chốt ở `model.ts` dòng 237) và cho `huongDieuChinhGia` (`TangGia`/`GiamGia` — đúng CHECK của DB tại [V1__baseline.sql:16322](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)), `hinhThucThanhToan` (8 giá trị theo CHECK tại :16321). Dùng chung cho cả `filters[].field/value` lẫn `data` — vì `DynamicSpecification` chuyển giá trị lọc bằng chính converter của cột, một bảng dịch riêng cho tầng lọc là chỗ lệch âm thầm.

---

## 5. Ma trận UC → endpoint → tài liệu

| UC | Tên | Endpoint | Màn hình | File con |
|---|---|---|---|---|
| PMKT-U-07665 | Xem danh sách | A1, A2 | SCR_DanhSachDieuChinhGia | 01 |
| PMKT-U-07666 | Thêm mới | A4 (+ A15/A16/A17 cho Bước 1) | SCR_ThemMoiDieuChinhGia | 03, 08 |
| PMKT-U-07667 | Xem chi tiết | A3, A9, A10, A11 | SCR_XemChiTietDieuChinhGia | 02 |
| PMKT-U-07668 | Xóa | A6, A14 | SCR_DanhSachDieuChinhGia | 05 |
| PMKT-U-07669 | Ghi sổ | A7, A12 | SCR_DanhSachDieuChinhGia | 06 |
| PMKT-U-07670 | Bỏ ghi sổ | A8, A13 | SCR_DanhSachDieuChinhGia | 07 |
| PMKT-U-07671 | Sửa | A5 | SCR_SuaDieuChinhGia | 04 |

---

## 6. Luồng tổng thể

```mermaid
flowchart TD
    subgraph B1["Bước 1 — chọn nguồn (A15/A16/A17)"]
        N1[FE: chọn nguồn CTBH hoặc HĐ điều chỉnh] --> N2[POST /nguon/search<br/>lọc KH + khoảng ngày]
        N2 --> N3[Chọn dòng → FE tự tính Tỷ lệ ĐC · Đơn giá ĐC · Giá trị ĐC theo BR3]
    end
    B1 --> C1[POST / — Lưu, ghiSo=false]
    B1 --> C2[POST / — Lưu và ghi sổ, ghiSo=true]

    C1 --> T[ChungTuTemplate.thucThi]
    C2 --> T
    T --> V[kiemTraNghiepVu — ma trận validate §03]
    V --> L[luuEntity: header + chi tiết + liên kết nguồn]
    L --> S{coGhiSoNgay?}
    S -- không --> K[kiemTraKyMo — BR17.1 lưu nháp]
    S -- có --> D[sauKhiLuu: dựng DinhKhoan theo 4 kịch bản]
    D --> G[GhiSoApi.ghiSo — kernel tự kiểm kỳ, tự chống ghi trùng]
    G --> ST[status = DA_GHI_SO]
    ST --> A[NhatKyKiemToan — trong transaction]

    ST -.-> BG[POST /{id}/bo-ghi-so]
    BG --> X[GhiSoApi.boGhiSo — xoá VẬT LÝ dòng sổ cái]
    X --> Y[goToanBoTheoDich — gỡ liên kết nguồn]
    Y --> Z[status = NHAP · nguoiGhiSo/thoiGianGhiSo = null]
```

---

## 7. Migration dự kiến `V3`

File: `cell-app/src/main/resources/db/migration/V3__sal_dieu_chinh_gia_hang_ban_bo_sung.sql`

| # | Việc | Vì sao bắt buộc |
|---|---|---|
| 1 | DROP cột `trang_thai_chung_tu` (D7) | `NOT NULL` + CHECK chuỗi tiếng Việt sẽ chặn INSERT của entity mới (entity dùng cột `status`) |
| 2 | Thêm 12 cột header (tab thanh toán, cờ nghiệp vụ, tổng quy đổi) | SCR có trường, DB chưa có cột — §9.2 ở [09](09-thiet-ke-db.md) |
| 3 | Thêm 11 cột chi tiết (thuế enum, cột quy đổi, chiều phân tích, `khong_tong_hop_to_khai_gtgt`) | BR_KhongTongHopToKhaiGTGT + BR18 + panel Xem nhanh |
| 4 | Index `(tenant_id, ngay_hach_toan DESC, so_chung_tu DESC)` | sắp xếp mặc định BR2 / SCR_DanhSach dòng 37 |
| 5 | Seed `mst_loai_chung_tu` mã `CTDG` (D11) | `maLoaiChungTu()` bắt buộc; chốt chặn kỳ khoá đọc mã này |
| 6 | Seed quyền `DieuChinhGiaHangBan.Clone` | `BaseChungTuController.nhanBan` gọi `QuyenChecker.CLONE`; không seed = 403 cho mọi người kể cả Admin |
| 7 | Kiểm dữ liệu trước khi DROP/ALTER | Bảng có thể đã có dữ liệu ở tenant dev — §9.6 |

Chi tiết SQL: [09-thiet-ke-db.md](09-thiet-ke-db.md).

**File có sẵn phải sửa kèm:** không có. `MaChucNang.DIEU_CHINH_GIA_HANG_BAN` đã tồn tại ([:229](../../cell-app/src/main/java/vn/dopai/pmkt/cell/common/constant/MaChucNang.java)); `LoaiChungTu.SAL_DIEU_CHINH_GIA_HANG_BAN` đã tồn tại ([:31](../../cell-app/src/main/java/vn/dopai/pmkt/cell/quan_he_chung_tu/api/LoaiChungTu.java)).

---

## 8. Thứ tự thực hiện

1. Đọc lại chữ ký `BaseChungTuController` · `ChungTuTemplate` · `QuanHeChungTuApi` (cảnh báo §0).
2. **Migration V3** + seed → chạy Flyway trên DB dev, kiểm bằng `mcp__idea__execute_sql_query`.
3. `model/` (6 enum + mã lỗi) + unit test converter — **không phụ thuộc gì**.
4. `entity/` + whitelist `@Searchable` + test pin whitelist.
5. `repository/` (gồm `NguonDieuChinhGiaRepository` — SQL native).
6. `service/business/` theo thứ tự: `TinhToanDieuChinhGia` → `KiemTraDieuChinhGia` → `DinhKhoanDieuChinhGia` → `LienKetNguonDieuChinhGia` → `LuuDieuChinhGiaTemplate` → `GhiSo`/`BoGhiSo`/`NhanBan`. Mỗi lớp một bộ unit test.
7. `service/` điều phối + `adapter/DongDieuChinhGiaAdapter` (D5).
8. `controller/` + 3 endpoint nguồn.
9. `./gradlew unitTest` → smoke test trên DB dev qua IntelliJ → xuất Postman → PR.

**Phụ thuộc giữa các file con:** 09 (DB) chặn tất cả · 03 (thêm mới) chặn 04/05/06/07 vì dùng chung `LuuDieuChinhGiaTemplate` · 08 (nguồn) độc lập, làm song song được · 01/02 chỉ cần entity + mapper.

---

## 9. Rủi ro kỹ thuật

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| **R1** | UC_GhiSo đòi 6 tác động nguyên tử, ta chỉ làm được 2 (bút toán + trạng thái) vì thiếu module phiếu thu/chi và hóa đơn (D3) | **Cao** | Ghi rõ ở §1.2 và §12-Q2; header đã có sẵn cột `phieu_thu_id`/`phieu_chi_id`/`hoa_don_dieu_chinh_id` để module sau điền vào mà không phải đổi schema. Bút toán vẫn đủ nên **sổ cái không sai** |
| **R2** | Công thức BR2 (số lượng chưa trả lại + quy đổi ĐVT) phải viết SQL native đọc bảng của module chưa có Java | **Cao** | Cô lập trong đúng một lớp `NguonDieuChinhGiaRepository`; viết integration test trên DB thật; **không** phát tán SQL ra service |
| **R3** | Không có Docker trên máy dev ⇒ 25 test Testcontainers không chạy được | TB | Cổng xanh là `./gradlew unitTest`; test tích hợp chạy ở CI. Báo cáo phải nói rõ phần chưa chạy (`CLAUDE.md` §"CHẠY CODE") |
| **R4** | Enum `ThueSuatGtgt` bị khai lại ở 2 module (D9) — sửa một chỗ quên chỗ kia | TB | Test đồng bộ đọc CHECK constraint của cả hai bảng chi tiết và so với enum; mở ticket nâng enum lên `accounting_core` |
| **R5** | `ApplicationModules.verify()` chưa chạy trần được (96 vi phạm có sẵn) | TB | Viết test kiểu `ProxyModularityTest` chỉ soi vi phạm có nhắc tên `dieu_chinh_gia_hang_ban` — module mới giữ chuẩn tuyệt đối |
| **R6** | FE đã code xong trên mock với tên trường tự suy (`model.ts` dòng 6-11 tự khai "HỢP ĐỒNG CHƯA ĐƯỢC BE XÁC NHẬN") | TB | Kế hoạch này bám đúng `model.ts`; mọi lệch tên được liệt kê ở §5 của từng file con để FE sửa **một lần** ở 3 file (`model.ts`, `payload.ts`, `formDetail.ts`) |
| **R7** | Bảng đã có dữ liệu ở DB dev với `trang_thai_chung_tu` NOT NULL — DROP cột là không đảo ngược | Thấp | Query kiểm trước (§9.6 của [09](09-thiet-ke-db.md)); có file rollback tương ứng |

---

## 10. Quyền

| Mã quyền | Đã seed? | Dùng ở |
|---|---|---|
| `DieuChinhGiaHangBan.View` | ✅ [seed:268](../../cell-app/src/main/resources/db/seed/iam_quyen_full_639_ba.sql) | A1, A2 |
| `DieuChinhGiaHangBan.View.Detail` | ✅ :269 | A3, A9, A10 |
| `DieuChinhGiaHangBan.Create` | ✅ :263 | A4, A15, A16, A17 |
| `DieuChinhGiaHangBan.Edit` | ✅ :265 | A5 |
| `DieuChinhGiaHangBan.Delete` | ✅ :264 | A6, A14 |
| `DieuChinhGiaHangBan.Post` | ✅ :266 | A7, A12 |
| `DieuChinhGiaHangBan.Unpost` | ✅ :267 | A8, A13 |
| **`DieuChinhGiaHangBan.Clone`** | ❌ **CHƯA** | A11 — **phải seed ở V3**, nếu không nút "Nhân bản" của `SCR_XemChiTiet` trả 403 với mọi người dùng kể cả Admin |
| `DieuChinhGiaHangBan.Export` / `.Import` | ❌ cố ý không seed | endpoint kế thừa vẫn tồn tại nhưng 403 — đúng ý `DanhSachQuyen.md §B4.6` |

BR25: thiếu quyền → 403 kèm body; FE ẩn nút chứ không để bấm rồi mới báo (`IMPLEMENT.md` dòng 292).

---

## 11. Mã thông báo

Lấy **nguyên văn** từ [`6.messages.md`](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/6.messages.md).

| Hằng (đề xuất, trong `MaLoiDieuChinhGia`) | messageId | Nội dung nguyên văn | Dùng ở |
|---|---|---|---|
| `MSG_TAO_THANH_CONG` | `MSG_PMKT-E-07664_001` | Thêm mới chứng từ điều chỉnh giá thành công | A4 |
| `MSG_SUA_THANH_CONG` | `MSG_PMKT-E-07664_002` | Cập nhật chứng từ điều chỉnh giá thành công | A5 |
| `MSG_XOA_THANH_CONG` | `MSG_PMKT-E-07664_003` | Xóa chứng từ điều chỉnh giá thành công | A6, A14 |
| `MSG_GHI_SO_THANH_CONG` | `MSG_PMKT-E-07664_004` | Ghi sổ thành công | A7, A12 |
| `MSG_BO_GHI_SO_THANH_CONG` | `MSG_PMKT-E-07664_005` | Bỏ ghi sổ thành công | A8, A13 |
| `MSG_LOI_HE_THONG` | `MSG_PMKT-E-07664_006` | Lỗi hệ thống | `GlobalExceptionHandler` |
| `MSG_KHONG_CO_QUYEN` | `MSG_PMKT-E-07664_007` | Không có quyền truy cập | 403 mọi endpoint |
| `MSG_KHONG_CO_DU_LIEU` | `MSG_PMKT-E-07664_008` | Không tìm thấy dữ liệu | A1 (FE hiển thị, BE trả list rỗng) |
| `MSG_THIEU_SO_CHUNG_TU` | `MSG_PMKT-E-07664_101` | Số chứng từ không được để trống | A4, A5 |
| `MSG_THIEU_PHUONG_THUC` | `MSG_PMKT-E-07664_102` | Vui lòng chọn phương thức điều chỉnh | A4, A5 |
| `MSG_NGAY_CT_KHONG_HOP_LE` | `MSG_PMKT-E-07664_103` | Ngày chứng từ không hợp lệ | A4, A5 |
| `MSG_THIEU_DONG_CHI_TIET` | `MSG_PMKT-E-07664_104` | Vui lòng nhập ít nhất một dòng chi tiết điều chỉnh | A4, A5 |
| `MSG_SO_LUONG_KHONG_HOP_LE` | `MSG_PMKT-E-07664_105` | Số lượng phải lớn hơn 0 | A4, A5 |
| `MSG_DON_GIA_KHONG_HOP_LE` | `MSG_PMKT-E-07664_106` | Đơn giá phải lớn hơn 0 | A4, A5 |
| `MSG_THIEU_NGAY_CHUNG_TU` | `MSG_PMKT-E-07664_107` | Vui lòng nhập ngày chứng từ | A4, A5 |
| `MSG_TRUNG_SO_CHUNG_TU` | `MSG_PMKT-E-07664_109` | Số chứng từ đã tồn tại, vui lòng nhập số khác | A4, A5, A7 |
| `MSG_THIEU_LY_DO` | `MSG_PMKT-E-07664_110` | Vui lòng nhập lý do điều chỉnh | A4, A5 |
| `MSG_DA_GHI_SO` | `MSG_PMKT-E-07664_201` | Chứng từ đã ghi sổ | A5, A6, A7 |
| `MSG_HOA_DON_DA_KY_PHAT_HANH` | `MSG_PMKT-E-07664_202` | Hóa đơn đã ký phát hành | A8 — **chưa kiểm được**, xem §12-Q3 |
| `MSG_KY_KE_TOAN_DONG` | `MSG_PMKT-E-07664_203` | Ngày hạch toán không thuộc kỳ kế toán đang mở | A4, A5, A7, A8 (kernel ném `PeriodLockedException`, map sang mã này) |
| `MSG_CHUNG_TU_GOC_KHONG_TON_TAI` | `MSG_PMKT-E-07664_204` | Chứng từ gốc không tồn tại | A4, A5 |
| `MSG_NGAY_HT_NHO_HON_NGAY_CT` | `MSG_PMKT-E-07664_205` | Ngày hạch toán không được nhỏ hơn ngày chứng từ | A4, A5 |
| `MSG_THIEU_HOA_DON_GOC` | `MSG_PMKT-E-07664_206` | Bạn cần chọn hóa đơn gốc trên tab Hóa đơn | A4, A5 |
| `MSG_THIEU_LOAI_DIEU_CHINH` | `MSG_PMKT-E-07664_207` | Vui lòng chọn loại điều chỉnh trên tab Hóa đơn | A4, A5 |
| `MSG_XAC_NHAN_XOA` | `MSG_PMKT-E-07664_300` | Bạn có chắc chắn muốn xóa chứng từ này? | FE (confirm), BE không dùng |
| `MSG_TRUNG_SO_HOA_DON` | `MSG_PMKT-E-07664_301` | Số hóa đơn [{soHD}] đã tồn tại cho khách hàng này. Vui lòng kiểm tra lại | A4, A5 — **chưa kiểm được**, xem §12-Q3 |

⚠ Hai mã **không có trong `6.messages.md`** nhưng SCR/UC dùng: câu ghi sổ trùng số ("Số chứng từ {SoChungTu} đã tồn tại. Vui lòng kiểm tra lại trước khi ghi sổ." — UC_GhiSo) và câu xác nhận bỏ ghi sổ ("Nếu bỏ ghi sổ … Hóa đơn điều chỉnh được sinh ra cũng bị xóa…" — UC_BoGhiSo). Xem §12-Q5.

---

## 12. ⚠️ Điểm cần BA xác nhận

| # | Vấn đề | Bằng chứng mâu thuẫn / thiếu | Xử lý tạm để code chạy tiếp |
|---|---|---|---|
| **Q1** | **Mã loại chứng từ** cho điều chỉnh giá hàng bán là gì? | BR09 (`business_rules.md:283-312`) liệt kê 27 mã, **không có** mã nào cho điều chỉnh giá hàng bán · seed `20_loai_chung_tu.sql:8-29` có 20 mã, cũng không có. Trong khi `ChungTuTemplate.maLoaiChungTu()` ([:272](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)) là **bắt buộc** và chốt chặn kỳ khoá đọc mã này | Dùng `CTDG` (D11), seed ở V3. Đổi mã sau = sửa 1 hằng + 1 dòng seed |
| **Q2** | Ghi sổ có **bắt buộc** sinh Phiếu thu/Phiếu chi/Giấy báo và Hóa đơn điều chỉnh ngay lần này không? | UC_GhiSo "Ràng buộc nguyên tử" liệt kê 6 tác động phải thành công đồng thời · nhưng BE **không có module** nào của `cb_phieu_thu`, `cb_phieu_chi`, `sal_dieu_chinh_hoa_don_ban_hang` (§2.1) — không có gì để gọi | Ghi sổ chỉ sinh bút toán + đổi trạng thái (D3). Nếu BA/PO bắt buộc có, phải mở phiếu yêu cầu cho module Phiếu thu/chi + Hóa đơn điều chỉnh trước |
| **Q3** | Hai luật **chưa kiểm được ở BE**: `MSG_202` "Hóa đơn đã ký phát hành, không thể bỏ ghi sổ" và `MSG_301` "Số hóa đơn đã tồn tại cho khách hàng này" | Cả hai đọc trạng thái/số của **hóa đơn**, mà bảng `sal_hoa_don_ban_hang` chưa có tầng Java và `sal_dieu_chinh_hoa_don_ban_hang.trang_thai_phat_hanh_hoa_don` ([V1__baseline.sql](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)) chưa được module nào ghi | Cài **cấu trúc kiểm** (interface `HoaDonPort`) nhưng cài đặt mặc định trả "không có hóa đơn" ⇒ hai luật này không chặn ai. Ghi rõ ở [07](07-bo-ghi-so.md) |
| **Q4** | **Số lượng / Đơn giá phải > 0** (`MSG_105`, `MSG_106`) mâu thuẫn với dòng **Dịch vụ** | SCR dòng 582-583 (bảng Validate): "Số lượng phải lớn hơn 0", "Đơn giá phải lớn hơn 0" · SCR dòng 112-115 (BR2) và 137-139 (BR3): dòng Dịch vụ có `SL = ĐG = 0`, `Thành tiền ≠ 0`, và hai ô đó **disable, luôn = 0`. Áp thẳng bảng Validate thì **không bao giờ lưu được** chứng từ điều chỉnh giá dịch vụ | Miễn hai luật cho dòng có `soLuong == 0 && donGia == 0 && thanhTien != 0` — **giống hệt cách FE đã chọn** (`IMPLEMENT.md` §6 mục 1). Hai bên phải cùng luật, nếu không FE cho lưu mà BE chặn |
| **Q5** | Hai câu thông báo dùng ở UC nhưng **không có mã** trong `6.messages.md` | UC_GhiSo mục "Kiểm tra trùng số chứng từ": *"Số chứng từ {SoChungTu} đã tồn tại. Vui lòng kiểm tra lại trước khi ghi sổ."* — khác câu của `MSG_109` · UC_BoGhiSo bước 5: *"Nếu bỏ ghi sổ chứng từ điều chỉnh giá hàng bán [Số chứng từ] thì Hóa đơn điều chỉnh được sinh ra cũng bị xóa…"* — không có mã nào | Ghi sổ trùng số dùng lại `MSG_109`; câu xác nhận bỏ ghi sổ là **của FE** (popup), BE không trả. Cần BA cấp mã hoặc xác nhận cách này |
| **Q6** | BR14 "Chiết khấu thương mại" (SCR dòng 488-493) mô tả hành vi cho một ô **không tồn tại** trong bảng trường của lưới (dòng 444-465) | Bảng trường 20 cột không có ô "Chiết khấu thương mại" · BR14 lại mô tả tick nó thì thành tiền âm, disable chiết khấu, disable hàng khuyến mại | Không cài BR14 lần này (§1.2). FE cũng không dựng (`IMPLEMENT.md` §5.3) |
| **Q7** | BR13 "ĐVT khác chuẩn ⇒ hiển thị thêm các trường ĐVT quy đổi" (SCR dòng 487) — một dòng chữ, không có bảng trường | Bảng chi tiết DB chỉ có `don_vi_tinh_id`, không có cột hệ số/ĐVT quy đổi | Không cài; lưu `don_vi_tinh_id` như nguồn đưa sang. Nếu BA cần, phải bổ sung cột `he_so_quy_doi` + `don_vi_tinh_goc_id` — ảnh hưởng cả công thức BR2 |
| **Q8** | **Trường "Thanh toán ngay"** là cột riêng hay suy từ `hinh_thuc_thanh_toan`? | SCR khai `Thanh toán ngay` (checkbox) **và** `Hình thức thanh toán` (dropdown, chỉ hiện khi checkbox = true) là hai trường · CHECK của DB gộp cả hai vào một cột: `hinh_thuc_thanh_toan ∈ {DieuChinhCongNo, ThanhToanNgay, ThuTienMat, GiayBaoCo, ChiTienMat, UyNhiemChi, SecChuyenKhoan, SecTienMat}` ([V1__baseline.sql:16321](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)) · FE gửi **cả hai** (`model.ts` dòng 193-195) | Thêm cột `thanh_toan_ngay boolean` (§9.2) và giữ `hinh_thuc_thanh_toan` mang giá trị cụ thể; `thanhToanNgay = false` ⇒ `hinh_thuc_thanh_toan = 'DieuChinhCongNo'`. Suy ngược được nhưng lưu tường minh để khớp FE và tránh phải đoán |
| **Q9** | Cột `loai_dieu_chinh` của DB (`TangGia`/`GiamGia`) đang mang **"Phương thức điều chỉnh"** của SCR, còn "Loại điều chỉnh" của tab Hóa đơn (Điều chỉnh giá/Sai sót/Khác) chưa có cột | SCR dòng 264: "Phương thức điều chỉnh" — field `HuongDieuChinhGia`, 2 giá trị Tăng/Giảm · SCR dòng 422: "Loại điều chỉnh" — field `LoaiDieuChinh`, 3 giá trị · DB chỉ có một cột `loai_dieu_chinh` với CHECK 2 giá trị | Giữ `loai_dieu_chinh` = hướng Tăng/Giảm (DTO tên `huongDieuChinhGia` theo FE), **thêm** cột `loai_dieu_chinh_hoa_don` cho 3 giá trị của tab Hóa đơn (§9.2). Tên cột DB lệch tên BA — đánh dấu ở §5 của [03](03-them-moi.md) |
| **Q10** | BR mà SCR liệt kê ở cuối (dòng 635-651) **lệch số** so với `business_rules.md` | SCR ghi "BR26. Phân quyền", "BR30. Chính sách xóa dữ liệu", "BR31. Tùy biến giao diện", "BR35. Chỉnh sửa từ màn Xem", "BR37. Ghi nhận bút toán", "BR38. Kiểm tra kỳ kế toán" · `business_rules.md` thật: BR25 phân quyền, BR29 xóa, BR30 ẩn/hiện cột, BR34 sửa từ màn xem, BR36 ghi bút toán, BR17 kỳ kế toán. Toàn bộ lệch +1 | Đọc theo **`business_rules.md`** (nguồn sự thật). §14 của kế hoạch này ghi số đúng |

---

## 13. Điều kiện nghiệm thu

### BA xác nhận
- [ ] Đủ 7 UC, đúng điều kiện hiển thị/ẩn nút theo trạng thái (BR12, BR13, BR42).
- [ ] Bộ lọc, thứ tự sắp xếp mặc định, dòng tổng đúng `SCR_DanhSachDieuChinhGia`.
- [ ] Bốn kịch bản bút toán (§06) đúng "Cách hạch toán" của SCR dòng 528-559 và UC_GhiSo.
- [ ] Trả lời Q1…Q10 (§12).

### Dev BE xác nhận
- [ ] Controller không gọi repository; business logic ở service; Entity không lọt ra ngoài.
- [ ] Dùng lại `SearchRequest` · `DynamicSpecification` · `PageResponse` · `ApiResponse` · `QuyenChecker` · `GhiSoApi` · `QuanHeChungTuApi` thay vì tự viết.
- [ ] Mọi filter/sort đều whitelist `@Searchable`; tenant / phạm vi đơn vị / soft-delete không nhận từ client.
- [ ] Mọi handler gọi `quyen.require(...)`.
- [ ] Không hardcode magic value; enum có converter + test đồng bộ với CHECK constraint.
- [ ] Không N+1: dòng chi tiết nạp bằng `join fetch`, dòng tổng là query riêng.
- [ ] Module mới **0 vi phạm ranh giới Modulith**.
- [ ] `./gradlew unitTest` xanh; phần Testcontainers **báo rõ là chưa chạy** (không có Docker).

---

## 14. Quy chuẩn nghiệp vụ (BR) áp dụng

| BR | Áp ở đâu |
|---|---|
| **BR1** Phân trang | A1 — mặc định **10** bản ghi/trang theo `SCR_DanhSach` BR1 (lệch mặc định 20 của BR1 chung; epic thắng trong phạm vi màn này) |
| **BR2** Hiển thị & sắp xếp | A1 — sort mặc định `ngayHachToan desc, soChungTu desc` ([01](01-xem-danh-sach.md) §6.2) |
| **BR3** Popup | FE |
| **BR5 / BR10** Combogrid, chọn nguồn | A15/A16/A17 ([08](08-chon-nguon-chung-tu.md)) |
| **BR7** Precision & làm tròn | domain DB: `money_vnd numeric(18,2)`, `quantity numeric(18,3)`, `percent_rate numeric(5,2)`, `exchange_rate numeric(18,6)` — đúng bảng 7.1 ([09](09-thiet-ke-db.md) §9.4) |
| **BR8** Khoảng thời gian | A1 lọc theo `ngayHachToan`; A15 mặc định "từ đầu tháng tới hiện tại" |
| **BR11** Tìm kiếm / lọc / sắp xếp | A1 — server-side toàn tập, whitelist `@Searchable` |
| **BR12** Trạng thái chứng từ | `status` (`TrangThaiChungTu`); sửa/xoá/ghi sổ chỉ khi chưa ghi sổ; bỏ ghi sổ chỉ khi đã ghi sổ |
| **BR13** Nút thao tác | DTO trả đủ cờ để FE ẩn/hiện ([01](01-xem-danh-sach.md) §5.3) |
| **BR15** Validation | ma trận đầy đủ ở [03](03-them-moi.md) §5 |
| **BR16** Cảnh báo nghiệp vụ | `MSG_COMMON_001` cho thao tác sai trạng thái (BR42.1) |
| **BR17** Kỳ kế toán | kernel `GhiSoApi`/`KyKeToanApi` kiểm; template tự kiểm ở ca lưu nháp |
| **BR18** Ngoại tệ | cột `*_quy_doi` = gốc × tỷ giá; sổ cái ghi bằng tiền hạch toán + `DinhKhoan.voiNgoaiTe` |
| **BR19** Kiểm trùng số chứng từ | unique `uq_sal_dcg_so_ct` + kiểm sớm → `MSG_109` |
| **BR20** Số chứng từ | nhập tay, ≤ 50 ký tự, không dấu tiếng Việt (D12) |
| **BR21** Grid chi tiết con | `thu_tu` lưu thứ tự dòng; cascade + orphanRemoval |
| **BR25** Phân quyền | §10 |
| **BR28** Multi-tenant | RLS `tenant_isolation` + policy phạm vi đơn vị đã có sẵn trên cả hai bảng |
| **BR29** Chính sách xóa | xóa mềm `da_xoa` + `nguoi_xoa` + `ngay_xoa`; dòng con cascade theo cha |
| **BR31** Dòng tổng | `summary` của `PageResponse`, tính trên **toàn tập sau lọc** |
| **BR36** Ghi bút toán, không gộp dòng | mỗi cặp TK là một `DinhKhoan` riêng; kernel tách 2 dòng sổ cái |
| **BR37** Ngày hạch toán | validate `ngayHachToan ≥ ngayChungTu` → `MSG_205` |
| **BR41** Tham chiếu chéo | quan hệ nguồn↔đích của epic này là **ràng buộc nghiệp vụ**, KHÔNG thuộc BR41 (BR41 tự loại trừ "chứng từ điều chỉnh trỏ chứng từ gốc") |
| **BR42** Bỏ ghi sổ | chỉ chứng từ đã ghi sổ; hàng loạt tự bỏ qua chứng từ chưa ghi sổ |
| **BR45** Thao tác hàng loạt | A12/A13/A14 trả `KetQuaHangLoatDto` (thành công/thất bại từng dòng) |
| **BR46** Trường hệ thống | `BaseEntity`/`BaseChungTuEntity` quản `nguoi_tao`/`ngay_tao`/`nguoi_cap_nhat`/`ngay_cap_nhat`/`nguoi_xoa`/`ngay_xoa`/`nguoi_ghi_so`/`thoi_gian_ghi_so` |

**BR chưa xử lý được:** BR38 (nhóm cột), BR39 (xuất Excel — quyền không bật), BR22/BR23/BR40 (danh mục cây — không thuộc màn chứng từ), BR32/BR44 (thuần FE).

---

## 15. Tài liệu tham chiếu

- `pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/1.function-breakdown.md` · `2.usecase.puml` · `3.crud-matrix.puml` · `4.usecases/**` · `5.screens/**` · `6.messages.md` · `Matrix/**`
- `pmkt-docs/ba/Common/business_rules.md` — BR1, BR2, BR5, BR7, BR8, BR10, BR11, BR12, BR13, BR15, BR16, BR17, BR18, BR19, BR20, BR21, BR25, BR28, BR29, BR31, BR36, BR37, BR41, BR42, BR45, BR46
- `CLAUDE.md` · `cell-app/CLAUDE.md` · `docs/conventions.md` · `docs/be-khung-kien-truc-chuan.md` · `docs/_bieu-mau-plan-api.md`
- Kế hoạch FE đối ứng: `docs/doing/PMKT-E-07664-dieu-chinh-gia-hang-ban-fe/IMPLEMENT.md` + `client/src/features/banHang/dieuChinhGiaHangBan/api/model.ts`
- Mẫu code tham khảo: `cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/**` · `accounting_core/**` · `core/**`
