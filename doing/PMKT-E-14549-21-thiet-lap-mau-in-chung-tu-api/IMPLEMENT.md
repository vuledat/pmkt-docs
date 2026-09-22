# IMPLEMENT — PMKT-E-14549_21 Thiết lập mẫu in chứng từ (BE)

| | |
|---|---|
| Ngày | 2026-09-19 |
| Người làm | AI (`/gen-be`) |
| Kế hoạch | [00-ke-hoach-tong.md](00-ke-hoach-tong.md) — 11 file con |
| Đặc tả | `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/` — 271 luật, **0 `OPEN`** ⇒ cổng MỞ |
| Nhánh | `cell-app` › `feat/mau-in`, nền `37303112` (= `origin/develop`) + điểm cứu hộ `7e4b504a` |
| Trạng thái | **HOÀN THÀNH** phần BE — 6/6 lô đã code · `trace.sh be` **DAT** (156/156 `OK`) · `msg.sh be` `OK 20 · LECH 0` · cổng `unitTest` không còn lỗi nào thuộc phiếu này. Nợ còn lại là việc VẬN HÀNH và việc của BA (§6), không phải code |

---

## 1. Phạm vi đã code

| Lô | Nội dung | Trạng thái |
|---|---|---|
| **L0** — nền | `V1158`…`V1160` · `MaNghiepVuMauIn` · `MaQuyenMauIn` · `GioiHanMauIn` viết lại · `MaLoiMauIn` sang bộ `MSG_PMKT-E-14549_21_nnn` · entity + `maNghiepVu` + 3 cột ảnh nền | ✅ xong |
| **L1** — hợp đồng JSON | 11 record `internal/model/json/**` · `MauInJsonCodec` (schema v2, mapper chặt) · `ChuanHoaMau` (15 bước) | ✅ xong |
| **L2** — thiết lập chung + cổng đơn vị | `ThietLapChungJson` · `ThietLapChungService` · `CauHinhInRepository` · `A10` `A11` · `HoSoDonViPort` + `HoSoDonViTheoTenant` · logo (`A12`) | ✅ xong |
| **L3** — nghiệp vụ mẫu | `KiemTraMau` (17 dòng) · `ChiaDeuDoRong` · `GiaiHuongGiay` · `CongGopDong` · `MauChuanBuilder` · `HopNhatCatalog` · `HopNhatThietLapChung` · `DungKhoiDauTrang` · `DungKhoiChuKy` | ✅ xong |
| **L4** — API | `MauInController` (`A1`–`A9`) · `ThietLapChungInController` (`A10`–`A12`) · `MauInService` · `XemTruocService` · `DungBanInService` · `AnhService` | ✅ xong |
| **L5** — provider đợt đầu | `MDV` · `BH` · `PT` · `PC` chuyển sang SPI v2 (`nghiepVu()`, `moTa(String)`, `trangThaiIn(UUID)`, `thuocDienCongGop()`; bỏ `duLieuMau()`) | ✅ xong |

**Ngoài phạm vi, KHÔNG làm** (đúng kế hoạch §1): dựng PDF/ngắt trang phía máy chủ (D3) · kênh
super-admin mẫu mặc định (D13) · endpoint lịch sử phiên bản (§12 `Q5`) · bảng `cfg_chi_nhanh` ·
mẫu in cố định theo quy định · seed mã quyền theo nghiệp vụ · hệ `bieuMau`.

---

## 2. File đã tạo / sửa

### 2.1 Migration (3 file MỚI)

| File | Vai trò |
|---|---|
| `V1158__prn_mau_in_khoa_nghiep_vu.sql` | Xoá sạch dữ liệu schema v1 · thêm `ma_nghiep_vu` cho cả hai bảng `prn_*` · dựng lại unique index `(tenant_id, ma_loai_chung_tu, ma_nghiep_vu) WHERE da_xoa = false` và index lịch sử · `schema_version` default 2 · đánh dấu hai cột `mac_dinh_*` NGỪNG DÙNG |
| `V1159__prn_mau_in_anh_nen.sql` | `anh_nen bytea` + `anh_nen_kieu_tep` + `anh_nen_ten_tep` + CHECK hai kiểu tệp |
| `V1160__iam_tenant_logo.sql` | `logo bytea` + `logo_kieu_tep` + `logo_ten_tep` trên `iam_tenant` + CHECK |

### 2.2 `cell/mau_in/api/` — SPI

| File | Vai trò |
|---|---|
| `MauInProvider.java` 🔧 | SPI v2: thêm `nghiepVu()`, `moTa(String)`, `trangThaiIn(UUID)`, `thuocDienCongGop()`; **bỏ** `duLieuMau()` (R-TLMI-219) |
| `dto/MoTaMauIn.java` 🔧 | Catalog v2: thêm `maNghiepVu`, `LuoiCatalog` (đổi tên từ `BangCatalog`), `CotCatalog.rongForm`; **bỏ** `tongHop` (gộp vào `truong` — R-TLMI-165), `TruongCatalog.nhom`, `CotCatalog.can/congDuoc`; rút gọn `MacDinhMauIn` còn một trường `tieuDe` |
| `dto/MucMenuIn.java` 🔧 | Enum `Loai` thêm `DUONG_KE` và `THIET_LAP` (R-TLMI-023) |
| `dto/NghiepVuMauIn.java` ➕ | Một nghiệp vụ của loại chứng từ (Q-16) |
| `dto/TrangThaiInChungTu.java` ➕ | `daGhiSo` · `daKhoaSo` · `chiNhanhId` (R-TLMI-261 · 267) |
| `dto/DuLieuChungTu.java` · `KieuTruong` · `VaiTroKy` · `ChungTuTomTat` · 2 `package-info` | ✅ tái dùng nguyên |

### 2.3 `cell/mau_in/internal/model/` — hằng số & enum

`GioiHanMauIn` (viết lại phần lớn — 13 hằng lệch bản cũ) · `MaLoiMauIn` (thay toàn bộ `MSG_MAUIN_nnn`
bằng bộ `MSG_PMKT-E-14549_21_nnn` nguyên văn `6.messages.md`) · `LoaiKhoi` (7 → **5**, `DON_VI` →
`DAU_TRANG`) · `NguonMau` (3 → **2**) · `LoaiO` ➕ · `MaNghiepVuMauIn` ➕ · `MaQuyenMauIn` ➕ ·
`HanhDongLichSu` · `GioiHanLichSuMauIn` (giữ nguyên).

### 2.4 `internal/model/json/` — hợp đồng JSON v2

`MauInJson` · `TrangJson` (4 lề PHẲNG) · `KhoiJson` (sealed, 5 nhánh) · `KhoiDauTrangJson` ➕
(thay `KhoiDonViJson`) · `KhoiTieuDeJson` · `KhoiBangJson` · `KhoiChuKyJson` · `KhoiTuDoJson`
(viết lại — ma trận ô có toạ độ) · `OLuoiJson` ➕ · `ThuocTinhTruongJson` ➕ · `ThietLapChungJson` ➕.

**Đã `git rm`:** `KhoiDonViJson` · `KhoiThongTinJson` · `KhoiTongHopJson` · `TruongInJson` ·
`BoCucBangJson` · `KhoaJson`.

### 2.5 `internal/service/` và `business/`

| File | Vai trò |
|---|---|
| `MauInService` 🔧 | A1 mở màn · A2 Lưu (7 bước của D5) · A4 chứng từ gần đây |
| `XemTruocService` ➕ | A3 — mẫu hiệu lực + dữ liệu thật |
| `DungBanInService` ➕ | A8 menu In · A9 dựng bản in (11 bước của §6.2) |
| `ThietLapChungService` ➕ | A10 · A11 + kiểm miền giá trị |
| `AnhService` ➕ | A5 · A6 · A7 · A12 + kiểm magic bytes |
| `MauInLichSuService` 🔧 | Chỉ còn phần GHI; bỏ `danhSach()` / `chiTiet()` |
| `adapter/HoSoDonViTheoTenant` ➕ | Hiện thực `HoSoDonViPort` (thay `DonViInService`) |
| `business/ChuanHoaMau` 🔧 | 15 bước; bẫy "không xoá khoá bằng mặc định" đã xử lý |
| `business/KiemTraMau` 🔧 | 17 dòng R-TLMI-239 viết lại hoàn toàn + thứ tự lỗi C21 |
| `business/MauChuanBuilder` 🔧 | Viết lại — 4 loại khối, nhóm Giấy-và-chữ để TRỐNG |
| `business/HopNhatCatalog` 🔧 | Thêm quyết định C10 (`CanhBaoMau`) |
| `business/DangKyProvider` 🔧 | Khoá theo CẶP + 3 kiểm fail-fast mới |
| `business/MauInJsonCodec` 🔧 | Schema v2 + `SORT_PROPERTIES_ALPHABETICALLY = false` + đọc/ghi thiết lập chung |
| `business/ChiaDeuDoRong` ➕ · `GiaiHuongGiay` ➕ · `CongGopDong` ➕ · `HopNhatThietLapChung` ➕ · `DungKhoiDauTrang` ➕ · `DungKhoiChuKy` ➕ · `CanhBaoMau` ➕ | Ba thuật toán + hai bộ dựng khối |

**Đã `git rm`:** `GiaiMauHieuLuc` · `DonViInService` · `internal/client/MacDinhHeThong{Cache,Client,Rest}`.

### 2.6 `internal/controller/`, `dto/`, `entity/`, `repository/`, `port/`

`MauInController` (viết lại đường dẫn, giữ cách gate tường minh) · `ThietLapChungInController` ➕ ·
`MauInManHinhResponse` ➕ · `KetQuaLuuDto` 🔧 · `XemTruocResponse` ➕ · `BanInResponse` ➕ ·
`MenuInResponse` ➕ · `ThietLapChungResponse` ➕ · `LuuThietLapChungRequest` ➕ · `AnhDto` ➕ ·
`DuLieuInDto` 🔧 · `MauInTuyChinh` 🔧 · `MauInLichSu` 🔧 · `MauInTuyChinhRepository` 🔧 +
`MauInBanGon` ➕ · `MauInLichSuRepository` 🔧 · `CauHinhInRepository` ➕ · `TraCuuMauInRepository` 🔧
(thêm tra tài khoản ngân hàng) · `port/HoSoDonViPort` + `HoSoDonVi` ➕ · `package-info` 🔧.

**Đã `git rm`:** `LoaiChungTuMauInDto` · `MauInHieuLucDto` · `DuLieuInResponse` ·
`MauInLichSuDto` · `MauInLichSuChiTietDto`.

### 2.7 File sửa NGOÀI module

| File | Sửa gì |
|---|---|
| `common/constant/MaChucNang.java` | Cập nhật javadoc `HT_MAU_IN` sang spec mới; **thêm** hằng `HT_THONG_TIN_CONG_TY` (trước đó là chuỗi literal trong `TenantConfigController`) |
| `platform_iam/tenant/api/TenantConfigApi.java` | `ThongTinDonViIn` thêm `taiKhoanNganHangId` + `coLogo`; **thêm** `logoDonVi()` và `luuLogoDonVi(...)` — ⚠ xem §5 lệch L-9 |
| `platform_iam/tenant/internal/entity/Tenant.java` | Thêm 3 cột logo (`V1160`) + `datLogo(...)` |
| `platform_iam/tenant/internal/adapter/TenantConfigAdapter.java` | Hiện thực hai method logo; inject `TenantRepository` |
| 4 provider + 3 catalog của `MDV` · `BH` · `PT` · `PC` | Chuyển sang SPI v2 + catalog v2 |

---

## 3. Đã kế thừa gì từ base

| Thứ | Lấy ở đâu |
|---|---|
| Bọc response | `cell/core/response/ApiResponse.java` — mọi endpoint JSON |
| Kiểm quyền | `cell/core/controller/QuyenChecker.java` (`require` / `check`) — gọi TƯỜNG MINH trong thân method, đúng lý do ghi ở chính lớp đó |
| Lỗi có `status` + `messageId` | `cell/core/shared/error/ApiException.java` (`badRequest` / `unprocessable` / `conflict` / `notFound`) |
| Entity gốc audit + `da_xoa` + `@Version` | `cell/core/entity/AggregateRootEntity.java` |
| Repository nền | `cell/core/repository/BaseRepository.java` |
| Kỳ khoá sổ | `accounting_core/hach_toan/api/KyKeToanApi#kyDangMo` — 4 provider hỏi qua đây, KHÔNG tự đọc bảng khoá sổ |
| Trạng thái ghi sổ | `cell/core/entity/TrangThaiChungTu.DA_GHI_SO` |
| Đọc số thành chữ | `cell/core/shared/text/SoTienBangChu.java` (catalog của provider dùng) |
| Hồ sơ doanh nghiệp + 5 người ký | `platform_iam/tenant/api/TenantConfigApi` |

**Viết mới, kèm lý do không kế thừa được:**

| Viết mới | Vì sao |
|---|---|
| `MauInController` không dùng `BaseCrudController` | Không phải CRUD trên một entity tìm kiếm được: khoá tự nhiên là CẶP mã trên path, và `PUT` vừa có thể GHI vừa có thể XOÁ bản ghi (R-TLMI-021) |
| `MauInJsonCodec` có `ObjectMapper` riêng | Cấu hình toàn cục của Spring (bỏ qua thuộc tính lạ, ghi null…) là thứ có thể đổi mà không ai nghĩ tới mẫu in; R-TLMI-037 và R-TLMI-246 phụ thuộc trực tiếp vào hai cờ đó |
| `CauHinhInRepository` (native query) | `CauHinhHeThongApi` CỐ Ý chỉ mở phần đọc và không lộ `phien_ban`, trong khi A11 cần cả ghi lẫn khoá lạc quan — xem §5 lệch L-10 |
| Không dùng `ChungTuTemplate` / `GhiSoApi` | Phiếu này KHÔNG tạo và KHÔNG ghi sổ chứng từ; R-TLMI-271 cấm đổi dữ liệu |

---

## 4. Migration đã thêm

| Version | Bảng/cột đụng tới | Đã chạy chưa |
|---|---|---|
| `V1158` | `prn_mau_in_tuy_chinh` (+`ma_nghiep_vu`, đổi unique index, `schema_version` default 2) · `prn_mau_in_lich_su` (+`ma_nghiep_vu`, dựng lại index) · **DELETE** dữ liệu schema v1 của cả hai bảng | ❌ **CHƯA** — máy dev cấm Docker, không dựng được Postgres |
| `V1159` | `prn_mau_in_tuy_chinh` + `anh_nen` · `anh_nen_kieu_tep` · `anh_nen_ten_tep` + CHECK | ❌ chưa |
| `V1160` | `iam_tenant` + `logo` · `logo_kieu_tep` · `logo_ten_tep` + CHECK | ❌ chưa |

⛔ **Trước khi chạy `V1158` trên BẤT KỲ môi trường nào:** chạy
`SELECT count(*) FROM prn_mau_in_tuy_chinh;`. Kết quả `> 0` ⇒ **DỪNG, hỏi user** — `V1158` xoá dữ
liệu, và giả định "chưa có bản ghi thật" dựa trên việc module Java chưa từng được deploy.

**Không cần seed quyền** (D10): `HTMauIn.View` / `HTMauIn.Edit` đã seed ở `V1149`, đang trên
`origin/develop`. Chưa seed quyền nào theo nghiệp vụ ⇒ phải cấp quyền thủ công trước khi test (BR25).

---

## 5. Lệch so với kế hoạch

| # | Lệch gì | Vì sao | Ảnh hưởng |
|---|---|---|---|
| **L-9** | Mở thêm **hai method GHI** trên `TenantConfigApi` (`luuLogoDonVi`) và thêm hai trường vào `ThongTinDonViIn` — API đó tự khai là "cố ý chỉ mở phần đọc" | Q-03 bắt làm tầng thiết lập chung tối thiểu, trong đó có LOGO; logo là cột của `iam_tenant` thuộc module `platform_iam`. Không có cửa ghi thì `mau_in` phải hoặc import `internal` của module khác (cấm), hoặc dựng bảng mới (user đã cấm) | Cửa hẹp đúng một trường, vẫn gate `HTThongTinCongTy.Edit` ở controller. **BA/dev soát lại nếu muốn cách khác** |
| **L-10** | `mau_in` đọc/ghi `cfg_cau_hinh_he_thong` bằng **native query** thay vì qua `CauHinhHeThongApi` | API đó chỉ có phần ĐỌC và không lộ `phien_ban`, mà A11 cần khoá lạc quan. Mở rộng API của module khác vì nhu cầu của mình là đổi thiết kế của họ | Đi đúng lối ngoại lệ mà `TraCuuMauInRepository` đã ghi; đã khai ở `cell/mau_in/package-info.java` |
| **L-11** | `nhom` của dòng cấu hình là **`IN_AN`**, không phải `IN` như kế hoạch viết | `CauHinhHeThongSupport.NHOM` là whitelist đóng và **không có** giá trị `IN`; dùng `IN` là dựng dữ liệu mà màn Cấu hình hệ thống không mở được | Không ảnh hưởng nghiệp vụ; mã cấu hình vẫn là `IN_CHUNG_CHUNG_TU` |
| **L-12** | KHÔNG sửa `spring.servlet.multipart.max-file-size` về `2MB` như kế hoạch | `application.yml` đã có `10MB / 15MB` từ trước; hạ xuống 2MB là **thu hẹp** giới hạn của các màn khác (`VatTuAnhController` cho phép 5MB) | Giới hạn 1MB của mẫu in vẫn được `AnhService` cưỡng chế và trả đúng `MSG_…_209` |
| **L-13** | KHÔNG hoàn tác `ProxyTargetId.SUPER_ADMIN` và khối `pmkt.proxy.targets.super-admin` trong `application.yml` như kế hoạch §4 đề nghị | Hai thứ đó là **hằng/cấu hình của module khác**, không bị `mau_in` tham chiếu nữa nên không gây lỗi; gỡ chúng làm diff lan sang `integration_ops` ngoài phạm vi phiếu | Còn một hằng chưa ai dùng — nên dọn ở phiếu dọn dẹp riêng |
| **L-14** | `BhMauInProvider.trangThaiIn` trả `chiNhanhId = null` | `ChungTuBanHangDto` chưa mang chi nhánh | Không ảnh hưởng hiện tại: `HoSoDonViTheoTenant` vốn BỎ QUA tham số (L-7). Khi `cfg_chi_nhanh` ra đời phải bổ sung trường vào DTO bán hàng |
| **L-15** | `XuatCatalogMauInTest` (task xuất snapshot catalog cho super-admin) đã **xoá** | D13 cắt kênh super-admin; snapshot đó chỉ phục vụ console super admin và phụ thuộc `duLieuMau()` đã bị bỏ khỏi SPI | `docs/doing/mau-in-chung-tu/sync-catalog.sh` tạm thời không có nguồn — ghi nợ, không chặn |

Tám mục lệch tài liệu đã chốt từ trước (`04-quyet-dinh-ban-giao.md` §5 L-1…L-8) và quyết định `D3`
(7 luật layout chuyển sang FE dựng) **giữ nguyên**, không phát sinh thêm.

---

## 6. Nợ kỹ thuật

1. **Chưa chạy migration** trên môi trường nào (cấm Docker) — xem §4.
2. **Chưa đối chiếu Postman với app đang chạy**: collection dựng từ hợp đồng API trong kế hoạch
   (cách 2 của `references/swagger-va-postman.md`), vì không boot được `cell-app` kèm Postgres.
3. ~~`msg.sh` chưa chạy~~ — **ĐÃ CHẠY** trên bản sao tài liệu nằm ngoài vùng đóng băng:

   ```
   Tong 26 message (tang=be): OK 20 · LECH 0 · THIEU-VI 0 · CHUA-DAT 0 · THIEU 6
   ```

   **`LECH` 0** ⇒ 20 message BE phát ra đúng NGUYÊN VĂN `6.messages.md`. Sáu mã `THIEU` là `_101`
   `_103` `_104` `_401`…`_404` — message của hộp thoại và toast **phía FE**; BE không có là đúng,
   không phải lỗi. §12 `Q6` coi như đã đóng.
4. **Ba mã `MSG_` BA chưa cấp** (L-4 · L-5): xung đột phiên bản dùng tạm `MSG_COMMON_001`, thiếu
   quyền In dùng `MSG_COMMON_003`, hai tooltip nút In disable chỉ có nguyên văn trong
   `MaLoiMauIn.TXT_CAM_IN_*` (FE đặt key i18n).
5. **§12 `Q1` `Q2` `Q8` chưa có câu trả lời của BA**: 4 provider đợt đầu tạm khai một nghiệp vụ
   `MAC_DINH`; `BhMauInProvider.thuocDienCongGop()` tạm `false` vì BA chưa map "hoá đơn" sang mã
   `mst_loai_chung_tu`. **Bật cờ đó lên là đổi hành vi bản in** nên cố ý chờ BA.
6. ~~50 luật P1/P2 thiếu test hồi quy~~ — **ĐÃ TRẢ XONG**: `trace.sh be` ⇒ `OK 156 · NO-TEST 0`,
   `KET LUAN: DAT`. Ba lớp test mới + 5 ca bổ sung, xem §7.2.
7. **Không có test Testcontainers nào chạy được** — RLS/GRANT sau `ADD COLUMN`, unique index thật,
   `@Transactional` rollback thật đều cần Postgres.
8. `docs/doing/mau-in-chung-tu/sync-catalog.sh` mất nguồn sau khi bỏ `XuatCatalogMauInTest` (L-15).

---

## 7. Kết quả cổng

### 7.1 `./gradlew unitTest`

**Lượt chạy CUỐI (sau khi bù 50 test hồi quy) — output thật:**

```
ChiPhiTraTruocModularityTest > moiVongCoCpttDeuDiQuaDungHaiCuaCuaA3() FAILED
HandlerAuthorizationArchTest > everyHandlerIsAuthorizationGated() FAILED
PhieuChiMuaHangRulesTest > giu_rieng_nguyen_te_va_quy_doi_va_phan_loai_tien_gui() FAILED
5770 tests completed, 3 failed
> Task :unitTest FAILED
BUILD FAILED in 6m 31s
```

**Cả ba lỗi đều ĐỎ SẴN, ngoài phạm vi** — xem bảng cuối mục này.
**Không lỗi nào thuộc `mau_in`.**

Diễn biến ba lượt chạy:

| Lượt | Kết quả | Ghi chú |
|---|---|---|
| 1 | `5712 tests completed, 7 failed` (25m 15s) | 4 lỗi thuộc phiếu này (bảng dưới) + 3 đỏ sẵn |
| 2 | `5718 tests completed, 3 failed` (10m 59s) | đã sửa 4 lỗi; chỉ còn 3 đỏ sẵn |
| **3** | **`5770 tests completed, 3 failed`** (6m 31s) | **+52 test hồi quy** bù 50 luật `NO-TEST`; vẫn đúng 3 đỏ sẵn |

Bốn lỗi thuộc phạm vi phiếu này ở lượt 1 **đã sửa**:

| Test | Nguyên nhân | Đã sửa |
|---|---|---|
| `ChuanHoaMauTest.R_TLMI_037_xoaMoiKhoaNull` | Assertion `doesNotContain("\"coChu\"")` sai: khối Tiêu đề VẪN có `coChu` riêng (R-TLMI-086) | Đổi sang khẳng định trên `trang.*` |
| `MauInServiceTest.R_TLMI_258_lechPhienBanThiKhongGhi` | `UnfinishedStubbingException` — stub `mock()` lồng trong `thenAnswer` của stub khác | Thay `mock(MauInTuyChinh)` bằng lớp con `MauInGia` |
| `BhMoTaMauInTest` · `PhieuThuChiMoTaMauInTest` | Số trường của catalog tăng vì R-TLMI-165 gộp ô tổng cuối form vào kho trường | Đổi `containsExactly` → `startsWith` / `hasSize` đúng |

Ba lỗi còn lại **ĐỎ SẴN, ngoài phạm vi** — ba file liên quan **byte-identical với `origin/develop`**
(`git diff --stat 37303112` trên chúng ⇒ rỗng), nên kết quả không thể phụ thuộc thay đổi của phiếu này:

| Test | Nội dung |
|---|---|
| `arch.HandlerAuthorizationArchTest.everyHandlerIsAuthorizationGated` | Handler duy nhất chưa gate là `bieu_mau_proxy…BieuMauProxyController#chuyenTiep` — **không** thuộc `mau_in` |
| `arch.ChiPhiTraTruocModularityTest.moiVongCoCpttDeuDiQuaDungHaiCuaCuaA3` | Ranh giới Modulith của `chi_phi_tra_truoc` |
| `chung_tu_mua_hang…PhieuChiMuaHangRulesTest.giu_rieng_nguyen_te_va_quy_doi_va_phan_loai_tien_gui` | Luật nguyên tệ/quy đổi của phiếu chi mua hàng |

Lượt chạy hẹp sau khi sửa (`--tests '*mau_in*' --tests '*MauIn*' --tests '*MoTaMauIn*'
--tests '*PhieuThuChiMauInProviderTest'`): **BUILD SUCCESSFUL in 3m 47s** — 314 test, toàn bộ test
của phiếu này xanh. `arch.MauInModularityTest` chạy riêng cũng **BUILD SUCCESSFUL** ⇒ module
`mau_in` KHÔNG mang vi phạm ranh giới Modulith nào, kể cả sau khi thêm `port/` và hai cạnh mới
(`mau_in → platform_iam.tenant.api`, `provider → accounting_core.hach_toan.api`).

⚠ **Phần tích hợp Testcontainers CHƯA CHẠY** (máy cấm Docker): `RedisCache*`, `FileStorage*`,
`ToChucNhomCellMigrationTest`, và mọi test cần Postgres thật.

### 7.2 `./docs/rules/trace.sh … be`

```
Tong 156 luat (tang=be): OK 156 · NO-TEST 0 · MISSING 0 · BLOCKED 0 · VI-PHAM 0

KET LUAN: DAT.
```

**Mọi luật tầng BE đều có mã trong code VÀ có test hồi quy mang chính mã đó.** Không luật nào
`MISSING`, `NO-TEST`, `BLOCKED` hay `VI-PHAM`.

Đợt bù 50 luật `NO-TEST` (42 P1 + 8 P2) thêm ba lớp test và bổ sung năm ca vào lớp có sẵn:

| Lớp test | Luật phủ |
|---|---|
| `MauChuanMacDinhTest` ➕ | 064 · 072 · 087 · 088 · 089 · 090 · 091 · 092 · 094 · 096 · 097 · 098 · 099 · 100 · 101 · 103 · 123 · 131 · 183 · 185 · 190 · 197 · 198 · 207 · 212 |
| `HopDongJsonMauInTest` ➕ | 046 · 048 · 084 · 126 · 145 · 156 · 158 · 159 · 160 · 161 · 209 |
| `DungBanInNoiDungTest` ➕ | 065 · 068 · 073 · 074 · 075 · 122 · 144 · 146 · 199 |
| `ThietLapChungServiceTest` 🔧 | 055 · 062 |
| `KiemTraMauTest` 🔧 | 157 · 237 |
| `MauInControllerQuyenTest` 🔧 | 248 |

### 7.2b Luật mà BE chỉ CẤP CỜ — test khẳng định phần nào

**Không luật nào trong 156 luật tầng BE phải bỏ sang nhóm "chỉ kiểm được với Docker".** Nhưng 8 luật
dưới đây có một nửa là PIXEL, thuộc FE theo quyết định **D3**; test của BE vì thế khẳng định đúng nửa
của BE (cờ sinh ra đúng giá trị, đúng miền, đi nguyên vẹn vào response), không giả vờ kiểm nửa kia.

| Luật | Nửa của BE — test khẳng định gì | Nửa của FE (không kiểm ở đây) |
|---|---|---|
| `R-TLMI-068` | `nen.kieu = KHUNG_VIEN` và `trang.mauChu` cùng có mặt trong `mauHieuLuc` | kẻ khung quanh mép trang, độ dày nét |
| `R-TLMI-073` | `canAnh = GIUA_TRANG` đi nguyên vẹn vào bản in | "ảnh giữ tỷ lệ, chiếm **khoảng** nửa trang" — đặc tả tự ghi là không có công thức |
| `R-TLMI-074` | `canAnh = TOAN_TRANG` đi nguyên vẹn vào bản in | kéo giãn phủ kín phần giấy trong lề |
| `R-TLMI-075` | số khối và thứ tự khối KHÔNG đổi khi có nền | vẽ nền dưới mọi khối |
| `R-TLMI-096` | `inStt = true` trong mẫu chuẩn | đánh số 1, 2, 3… khi vẽ bảng |
| `R-TLMI-099` | `lapTieuDeMoiTrang = true`, cờ đi nguyên vào bản in | ngắt trang và lặp dòng tiêu đề cột |
| `R-TLMI-100` | `keO = DAY_DU`, miền đúng hai giá trị | vẽ đường ngang/dọc |
| `R-TLMI-198` | `choTrongKy = VUA`, miền đúng ba giá trị | chừa khoảng **khoảng** 1 / 2 / 3 cm |

Bốn luật cần **DB thật** (`R-TLMI-004` · `005` · `035` và RLS/GRANT sau `ADD COLUMN`) đã được phủ ở
mức đo được bằng `MauInMigrationTest` (đọc chính file `.sql`: unique index đủ ba cột, `WHERE da_xoa
= false`, không cột `chi_nhanh`) cộng `MauInServiceTest` (repository không sinh điều kiện chi nhánh).
Phần "policy còn hiệu lực thật trên Postgres" vẫn là test Testcontainers — xem §6 mục 7.

### 7.3 Cây commit

```
$ git -C cell-app status --porcelain | wc -l
129
$ git -C cell-app status --porcelain | grep '^??' | wc -l
0
```

Mọi file mới đã `git add`; **không còn dòng `??` trong `src/main/java/`, `src/test/java/` hay
`src/main/resources/db/migration/`**. Migration nằm cùng cây với code dùng nó.

---

## 8. Endpoint đã hiện thực

| # | Method · Path | Quyền | Trạng thái |
|---|---|---|---|
| `A1` | `GET /api/mau-in/{maLoai}/{maNghiepVu}` | `HTMauIn.View` + `<ChucNang>.View.Detail` | ✅ |
| `A2` | `PUT /api/mau-in/{maLoai}/{maNghiepVu}` | `HTMauIn.Edit` + `<ChucNang>.View.Detail` | ✅ |
| `A3` | `GET …/{maNghiepVu}/chung-tu/{chungTuId}/xem-truoc` | `HTMauIn.View` + `<ChucNang>.View.Detail` | ✅ |
| `A4` | `GET …/{maNghiepVu}/chung-tu-gan-day?q=&gioiHan=` | `HTMauIn.View` + `<ChucNang>.View` | ✅ |
| `A5` | `POST …/{maNghiepVu}/anh-nen` (`multipart`) | `HTMauIn.Edit` | ✅ |
| `A6` | `GET …/{maNghiepVu}/anh-nen` (bytes thô) | `HTMauIn.View` | ✅ |
| `A7` | `DELETE …/{maNghiepVu}/anh-nen` | `HTMauIn.Edit` | ✅ |
| `A8` | `GET …/{maNghiepVu}/chung-tu/{chungTuId}/menu-in` | `<ChucNang>.<hanhDongIn()>` | ✅ |
| `A9` | `GET …/{maNghiepVu}/chung-tu/{chungTuId}/ban-in` | `<ChucNang>.<hanhDongIn()>` | ✅ |
| `A10` | `GET /api/mau-in/thiet-lap-chung` | `HTThongTinCongTy.View.Detail` | ✅ |
| `A11` | `PUT /api/mau-in/thiet-lap-chung` | `HTThongTinCongTy.Edit` | ✅ |
| `A12` | `POST` · `GET` · `DELETE /api/mau-in/thiet-lap-chung/logo` | `.Edit` / `.View.Detail` | ✅ |

**Endpoint bản cũ đã BỎ:** `GET /api/mau-in/loai-chung-tu` · `DELETE /api/mau-in/{ma}` ·
`GET /{ma}/lich-su` · `GET /{ma}/lich-su/{id}`.

---

## 9. Postman

`docs/json/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu.postman_collection.json` —
**7 nhóm · 26 request** (`0. Auth` · `1. Mở màn & lưu mẫu` · `2. Chọn chứng từ xem thử` ·
`3. Ảnh nền` · `4. In chứng từ` · `5. Thiết lập chung + logo` · `6. Ca kiểm thử kỳ vọng lỗi`).

Import: Postman › Import › chọn file › sửa biến `baseUrl` · `identityUrl` · `username` · `password`
› chạy `0. Auth > Login`. Dựng bằng **cách 2** (từ hợp đồng API trong kế hoạch), chưa đối chiếu với
app đang chạy — xem §6 mục 2.

---

## 10. BR đã áp dụng

| BR | Áp ở đâu | Đạt |
|---|---|---|
| **BR50.6** (Phase 2) | `INV-TLMI-011` — repository và gate quyền KHÔNG lọc `chi_nhanh_id`; mẫu xếp nhóm 1 (cấu hình hệ thống) | ✅ |
| **BR50.7** (Phase 2) | `HoSoDonViPort.theoChiNhanh(chungTu.chiNhanhId)` là cổng DUY NHẤT | ⚠ điểm nối đã có, hiện thực còn bỏ qua tham số (L-7) |
| **BR51.5** (Phase 2) | Ba quy tắc in · cộng gộp giới hạn 3 loại chứng từ · hướng giấy Tự động | ⚠ `thuocDienCongGop()` của `BH` còn `false` chờ `Q8` |
| BR7 | `ChiaDeuDoRong` làm tròn XUỐNG, `rong` là `Integer`; `CongGopDong` cộng bằng `BigDecimal` | ✅ |
| BR20 | `ma_loai_chung_tu varchar(20)` · `ma_nghiep_vu varchar(50)`; `DangKyProvider` fail-fast mã trống/trùng | ✅ |
| BR25 | Gate hai tầng ở mọi endpoint; `MaQuyenMauIn` gom một chỗ (Q-15) | ✅ |
| BR26 | `MSG_…_101` toast thành công; `MSG_…_201`…`216` lỗi tại chỗ | ✅ |
| BR28 | RLS `tenant_isolation` giữ nguyên; KHÔNG truy vấn nào mang `tenant_id` từ client | ✅ |
| BR29 | ⚠ **lệch có chủ ý** — hard delete khi mẫu bằng mẫu chuẩn (R-TLMI-021 · INV-TLMI-002); cột `da_xoa` và mệnh đề `WHERE da_xoa = false` vẫn giữ. Lý do: [08 §6](08-thiet-ke-db.md) | ⚠ lệch có tài liệu |
| BR46 | Trường hệ thống áp cho BẢN GHI (qua `AggregateRootEntity`), không áp cho từng nhánh JSON | ✅ |

**BR chưa xử lý được:** BR50 (Chi nhánh) đầy đủ — `cfg_chi_nhanh` chưa tồn tại trong repo.

---

## 11. Bảng truy vết luật → code → trạng thái

Ký hiệu: ✅ có code + có test · ⚠️ có code, thiếu test hồi quy · ⛔ chưa làm · 🚫 bị chặn.
Cột **Code** in nơi hiện thực CHÍNH (bỏ tiền tố `cell-app/src/{main,test}/java/vn/vtt/pmkt/`);
bảng đầy đủ **mọi** luật `Tầng = BE | CẢ HAI` — 156 dòng, sinh bằng
`./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec be`.

| Luật | Tầng | Sev | Code | Trạng thái |
|---|---|---|---|---|
| `R-TLMI-001` | BE | P0 | `cell/mau_in/api/MauInProvider.java` | ✅ OK |
| `R-TLMI-002` | CẢ HAI | P0 | `cell/ban_hang/chung_tu_ban_hang/internal/service/business/BhMauInProvider.java` | ✅ OK |
| `R-TLMI-003` | CẢ HAI | P0 | `cell/chung_tu_mua_hang/internal/service/business/MdvMauInProvider.java` | ✅ OK |
| `R-TLMI-004` | BE | P0 | `cell/mau_in/internal/entity/MauInLichSu.java` | ✅ OK |
| `R-TLMI-005` | BE | P0 | `cell/mau_in/internal/entity/MauInTuyChinh.java` | ✅ OK |
| `R-TLMI-006` | BE | P0 | `cell/mau_in/api/MauInProvider.java` | ✅ OK |
| `R-TLMI-007` | CẢ HAI | P0 | `cell/mau_in/internal/dto/BanInResponse.java` | ✅ OK |
| `R-TLMI-008` | CẢ HAI | P0 | `cell/mau_in/api/dto/MoTaMauIn.java` | ✅ OK |
| `R-TLMI-009` | CẢ HAI | P0 | `cell/mau_in/api/MauInProvider.java` | ✅ OK |
| `R-TLMI-010` | CẢ HAI | P1 | `cell/mau_in/internal/model/LoaiKhoi.java` | ✅ OK |
| `R-TLMI-011` | CẢ HAI | P0 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-012` | CẢ HAI | P0 | `cell/mau_in/internal/service/MauInService.java` | ✅ OK |
| `R-TLMI-013` | CẢ HAI | P0 | `cell/mau_in/api/MauInProvider.java` | ✅ OK |
| `R-TLMI-014` | CẢ HAI | P1 | `cell/ban_hang/chung_tu_ban_hang/internal/service/business/BhMauInProvider.java` | ✅ OK |
| `R-TLMI-018` | CẢ HAI | P0 | `cell/mau_in/internal/service/MauInService.java` | ✅ OK |
| `R-TLMI-019` | CẢ HAI | P0 | `cell/mau_in/internal/service/MauInService.java` | ✅ OK |
| `R-TLMI-021` | BE | P0 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-022` | BE | P1 | `cell/mau_in/internal/service/MauInServiceTest.java` | ✅ OK |
| `R-TLMI-025` | CẢ HAI | P1 | `cell/mau_in/internal/service/DungBanInService.java` | ✅ OK |
| `R-TLMI-028` | CẢ HAI | P0 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-031` | CẢ HAI | P0 | `cell/common/constant/MaChucNang.java` | ✅ OK |
| `R-TLMI-033` | CẢ HAI | P0 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-034` | BE | P0 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-035` | BE | P0 | `cell/mau_in/internal/model/MaQuyenMauIn.java` | ✅ OK |
| `R-TLMI-036` | CẢ HAI | P0 | `cell/mau_in/internal/controller/ThietLapChungInController.java` | ✅ OK |
| `R-TLMI-037` | BE | P0 | `cell/mau_in/internal/dto/MauInManHinhResponse.java` | ✅ OK |
| `R-TLMI-038` | BE | P0 | `cell/mau_in/internal/controller/ThietLapChungInController.java` | ✅ OK |
| `R-TLMI-039` | BE | P0 | `cell/mau_in/internal/service/business/ChuanHoaMau.java` | ✅ OK |
| `R-TLMI-044` | CẢ HAI | P0 | `cell/mau_in/internal/service/business/ChuanHoaMau.java` | ✅ OK |
| `R-TLMI-046` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/DungKhoiChuKy.java` | ✅ OK |
| `R-TLMI-047` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/ThietLapChungJson.java` | ✅ OK |
| `R-TLMI-048` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-049` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiDauTrangJson.java` | ✅ OK |
| `R-TLMI-054` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-055` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-056` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/TrangJson.java` | ✅ OK |
| `R-TLMI-057` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-058` | CẢ HAI | P1 | `cell/mau_in/internal/dto/BanInResponse.java` | ✅ OK |
| `R-TLMI-059` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/GiaiHuongGiay.java` | ✅ OK |
| `R-TLMI-060` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/GiaiHuongGiay.java` | ✅ OK |
| `R-TLMI-061` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-062` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-063` | BE | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-064` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-065` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/TrangJson.java` | ✅ OK |
| `R-TLMI-066` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-067` | CẢ HAI | P2 | `cell/mau_in/internal/dto/BanInResponse.java` | ✅ OK |
| `R-TLMI-068` | CẢ HAI | P2 | `cell/mau_in/internal/model/json/TrangJson.java` | ✅ OK |
| `R-TLMI-069` | CẢ HAI | P1 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-072` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-073` | CẢ HAI | P2 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-074` | CẢ HAI | P2 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-075` | CẢ HAI | P1 | `cell/mau_in/internal/dto/BanInResponse.java` | ✅ OK |
| `R-TLMI-076` | CẢ HAI | P1 | `cell/mau_in/internal/dto/DuLieuInDto.java` | ✅ OK |
| `R-TLMI-077` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-078` | BE | P0 | `cell/mau_in/api/dto/TrangThaiInChungTu.java` | ✅ OK |
| `R-TLMI-079` | BE | P1 | `cell/mau_in/internal/port/HoSoDonVi.java` | ✅ OK |
| `R-TLMI-080` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | ✅ OK |
| `R-TLMI-082` | CẢ HAI | P1 | `cell/mau_in/internal/controller/ThietLapChungInController.java` | ✅ OK |
| `R-TLMI-083` | BE | P2 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-084` | BE | P1 | `cell/mau_in/internal/model/json/KhoiDauTrangJson.java` | ✅ OK |
| `R-TLMI-085` | CẢ HAI | P1 | `cell/mau_in/api/dto/MoTaMauIn.java` | ✅ OK |
| `R-TLMI-086` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-087` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-088` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiTieuDeJson.java` | ✅ OK |
| `R-TLMI-089` | CẢ HAI | P2 | `cell/mau_in/internal/model/json/KhoiTieuDeJson.java` | ✅ OK |
| `R-TLMI-090` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiTieuDeJson.java` | ✅ OK |
| `R-TLMI-091` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiTieuDeJson.java` | ✅ OK |
| `R-TLMI-092` | CẢ HAI | P1 | `cell/ban_hang/chung_tu_ban_hang/internal/service/business/BhMoTaMauIn.java` | ✅ OK |
| `R-TLMI-093` | CẢ HAI | P0 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-094` | CẢ HAI | P2 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-095` | CẢ HAI | P2 | `cell/mau_in/api/dto/MoTaMauIn.java` | ✅ OK |
| `R-TLMI-096` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-097` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-098` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-099` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-100` | CẢ HAI | P2 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-101` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-102` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-103` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiBangJson.java` | ✅ OK |
| `R-TLMI-104` | CẢ HAI | P1 | `cell/mau_in/internal/model/MaLoiMauIn.java` | ✅ OK |
| `R-TLMI-105` | CẢ HAI | P2 | `cell/mau_in/api/dto/MoTaMauIn.java` | ✅ OK |
| `R-TLMI-106` | CẢ HAI | P1 | `cell/mau_in/api/dto/MoTaMauIn.java` | ✅ OK |
| `R-TLMI-107` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/MauChuanBuilder.java` | ✅ OK |
| `R-TLMI-108` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-109` | CẢ HAI | P1 | `cell/mau_in/api/dto/MoTaMauIn.java` | ✅ OK |
| `R-TLMI-111` | CẢ HAI | P1 | `cell/mau_in/internal/dto/KetQuaLuuDto.java` | ✅ OK |
| `R-TLMI-112` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | ✅ OK |
| `R-TLMI-113` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | ✅ OK |
| `R-TLMI-114` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | ✅ OK |
| `R-TLMI-119` | BE | P0 | `cell/mau_in/api/MauInProvider.java` | ✅ OK |
| `R-TLMI-121` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-122` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/KiemTraMau.java` | ✅ OK |
| `R-TLMI-123` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiTuDoJson.java` | ✅ OK |
| `R-TLMI-125` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-126` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiTuDoJson.java` | ✅ OK |
| `R-TLMI-129` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-130` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-131` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiTuDoJson.java` | ✅ OK |
| `R-TLMI-143` | CẢ HAI | P1 | `cell/mau_in/internal/model/LoaiO.java` | ✅ OK |
| `R-TLMI-144` | CẢ HAI | P1 | `cell/mau_in/internal/model/LoaiO.java` | ✅ OK |
| `R-TLMI-145` | CẢ HAI | P1 | `cell/mau_in/internal/model/LoaiO.java` | ✅ OK |
| `R-TLMI-146` | CẢ HAI | P1 | `cell/mau_in/internal/model/LoaiO.java` | ✅ OK |
| `R-TLMI-147` | CẢ HAI | P1 | `cell/mau_in/internal/model/MaLoiMauIn.java` | ✅ OK |
| `R-TLMI-153` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/KiemTraMau.java` | ✅ OK |
| `R-TLMI-156` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/MauInJson.java` | ✅ OK |
| `R-TLMI-157` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-158` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/OLuoiJson.java` | ✅ OK |
| `R-TLMI-159` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/OLuoiJson.java` | ✅ OK |
| `R-TLMI-160` | CẢ HAI | P2 | `cell/mau_in/internal/model/json/OLuoiJson.java` | ✅ OK |
| `R-TLMI-161` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-164` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/ThuocTinhTruongJson.java` | ✅ OK |
| `R-TLMI-165` | CẢ HAI | P1 | `cell/ban_hang/chung_tu_ban_hang/internal/service/business/BhMoTaMauIn.java` | ✅ OK |
| `R-TLMI-167` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/HopNhatCatalog.java` | ✅ OK |
| `R-TLMI-176` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiTuDoJson.java` | ✅ OK |
| `R-TLMI-178` | CẢ HAI | P0 | `cell/mau_in/internal/dto/BanInResponse.java` | ✅ OK |
| `R-TLMI-182` | CẢ HAI | P1 | `cell/mau_in/api/dto/MoTaMauIn.java` | ✅ OK |
| `R-TLMI-183` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/DungKhoiChuKy.java` | ✅ OK |
| `R-TLMI-184` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-185` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-186` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-187` | CẢ HAI | P1 | `cell/mau_in/internal/service/adapter/HoSoDonViTheoTenant.java` | ✅ OK |
| `R-TLMI-188` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-189` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-190` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-191` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/DungKhoiChuKyTest.java` | ✅ OK |
| `R-TLMI-192` | CẢ HAI | P0 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-193` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-196` | CẢ HAI | P1 | `cell/mau_in/internal/dto/DuLieuInDto.java` | ✅ OK |
| `R-TLMI-197` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiChuKyJson.java` | ✅ OK |
| `R-TLMI-198` | CẢ HAI | P2 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-199` | BE | P1 | `cell/mau_in/internal/port/HoSoDonViPort.java` | ✅ OK |
| `R-TLMI-207` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiJson.java` | ✅ OK |
| `R-TLMI-208` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiJson.java` | ✅ OK |
| `R-TLMI-209` | CẢ HAI | P1 | `cell/mau_in/internal/model/json/KhoiJson.java` | ✅ OK |
| `R-TLMI-210` | CẢ HAI | P0 | `cell/mau_in/internal/model/json/KhoiJson.java` | ✅ OK |
| `R-TLMI-212` | CẢ HAI | P1 | `cell/mau_in/internal/model/GioiHanMauIn.java` | ✅ OK |
| `R-TLMI-236` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/KiemTraMau.java` | ✅ OK |
| `R-TLMI-237` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/KiemTraMau.java` | ✅ OK |
| `R-TLMI-238` | CẢ HAI | P1 | `cell/mau_in/internal/service/business/KetQuaKiemTra.java` | ✅ OK |
| `R-TLMI-239` | CẢ HAI | P0 | `cell/mau_in/internal/service/MauInService.java` | ✅ OK |
| `R-TLMI-243` | CẢ HAI | P0 | `cell/mau_in/internal/service/MauInService.java` | ✅ OK |
| `R-TLMI-246` | BE | P0 | `cell/mau_in/internal/dto/AnhDto.java` | ✅ OK |
| `R-TLMI-247` | BE | P0 | `cell/mau_in/internal/service/MauInLichSuService.java` | ✅ OK |
| `R-TLMI-248` | CẢ HAI | P1 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-249` | CẢ HAI | P0 | `cell/mau_in/internal/model/MaLoiMauIn.java` | ✅ OK |
| `R-TLMI-258` | BE | P1 | `cell/mau_in/internal/dto/LuuMauInRequest.java` | ✅ OK |
| `R-TLMI-259` | BE | P0 | `cell/mau_in/internal/controller/MauInController.java` | ✅ OK |
| `R-TLMI-260` | CẢ HAI | P1 | `cell/mau_in/internal/dto/BanInResponse.java` | ✅ OK |
| `R-TLMI-261` | CẢ HAI | P0 | `cell/ban_hang/chung_tu_ban_hang/internal/service/business/BhMauInProvider.java` | ✅ OK |
| `R-TLMI-262` | BE | P1 | `cell/mau_in/internal/service/DungBanInService.java` | ✅ OK |
| `R-TLMI-264` | BE | P0 | `cell/mau_in/internal/service/ThietLapChungService.java` | ✅ OK |
| `R-TLMI-266` | BE | P0 | `cell/ban_hang/chung_tu_ban_hang/internal/service/business/BhMauInProvider.java` | ✅ OK |
| `R-TLMI-267` | BE | P0 | `cell/ban_hang/chung_tu_ban_hang/internal/service/business/BhMauInProvider.java` | ✅ OK |
| `R-TLMI-270` | CẢ HAI | P0 | `cell/mau_in/internal/model/MaLoiMauIn.java` | ✅ OK |
| `R-TLMI-271` | BE | P1 | `cell/mau_in/internal/dto/BanInResponse.java` | ✅ OK |

---

## 12. Việc cho người tiếp theo

1. **Chạy migration** trên môi trường dev sau khi đếm bản ghi (§4) — đây là việc phải làm trước khi
   test bằng Postman.
2. **Trả lời `Q1` `Q2` `Q8`** để 4 provider khai đúng nghiệp vụ và đúng diện cộng gộp.
3. **Cấp ba mã `MSG_` còn thiếu** (§6 mục 4) rồi thay hằng ở `MaLoiMauIn` — đổi một chỗ.
4. **Khi có Docker**: chạy nhóm Testcontainers để phủ nốt phần DB thật (RLS/GRANT còn hiệu lực sau
   `ADD COLUMN`, unique index một phần, rollback `@Transactional` thật) — §7.2b.
5. **FE**: `client/src/base/domainKit/mauIn/` phải đồng bộ theo hợp đồng JSON v2 —
   `GioiHanMauIn.java` là gương của `gioiHan.ts`, `schemas.ts` là gương của
   `internal/model/json/**`. ⚠ Nhóm `⟨kế thừa⟩` **cấm** `.default()` ở cả Zod lẫn Java.
