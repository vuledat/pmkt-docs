# 10 · Bảng truy vết luật → code → test (tầng BE)

| | |
|---|---|
| Nguồn | `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/02-rules.md` — 271 luật · 12 bất biến |
| Lọc | Tầng `BE` **hoặc** `CẢ HAI` ⇒ **163 luật** (34 `BE` + 129 `CẢ HAI`); 108 luật tầng `FE` thuần **không** thuộc phạm vi file này |
| Cổng kiểm | `./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec be` |
| Quy ước | `docs/rules/truy-vet-luat.md` — mã luật để lại **đúng hai chỗ**: nơi hiện thực chính + tên test |

---

## §1. ⛔ Việc phải làm TRƯỚC khi `/gen-be` — nếu không, cổng `trace.sh` đỏ dù code đúng

`docs/rules/truy-vet-luat.md §4` quy định: luật mang trạng thái **`CHỜ C<nn>`** trong `02-rules.md` mà **code chạm vào** ⇒ `trace.sh` in **`VI-PHAM`** và trả exit code ≠ 0.

`01-conflict.md` đã đóng **toàn bộ 36 mục** (`0 OPEN`, 32 `CLOSED-BA` có tên người + ngày), nhưng **`02-rules.md` chưa được cập nhật theo**: **8 luật** còn mang `CHỜ C<nn>` và dấu `⛔ BỊ CHẶN`.

| Luật | Trạng thái hiện tại trong `02-rules.md` | Mục đã đóng | Quyết định chốt (ở `04-quyet-dinh-ban-giao.md`) |
|---|---|---|---|
| `R-TLMI-021` | `CHỜ C02` | `C02` `CLOSED-BA` | So sánh nội dung — bằng mẫu chuẩn ⇒ xoá bản ghi (`D5`) |
| `R-TLMI-046` | `CHỜ C04` | `C04` `CLOSED-BA` | Tiêu đề in ra **mẫu sửa riêng được**; tên người ký + cờ in tên **luôn theo chung** |
| `R-TLMI-082` | `CHỜ C03` | `C03` `CLOSED-BA` | **CÓ** — Logo là ô tick thứ 7 |
| `R-TLMI-119` | `CHỜ C01` | `C01` `CLOSED-BA` | Khoá gộp **CÓ thuế suất** (`D14`) |
| `R-TLMI-188` | `CHỜ C04` | `C04` `CLOSED-BA` | như `R-TLMI-046` |
| `R-TLMI-199` | `CHỜ C05` | `C05` `CLOSED-BA` | Chi nhánh **ghi trên chứng từ** |
| `R-TLMI-258` | `CHỜ C06` | `C06` `CLOSED-BA` | Khoá lạc quan bằng `phienBan` (`D6`) |
| `R-TLMI-266` | `CHỜ C01` | `C01` `CLOSED-BA` | như `R-TLMI-119` |

**Việc phải làm:** với mỗi luật trên, trong `02-rules.md`:

1. Đổi cột `Trạng thái` ở bảng tổng: `**CHỜ C<nn>**` → `CHỐT`.
2. Xoá dòng `> ⛔ **BỊ CHẶN bởi C<nn>** …` trong thân luật.
3. Thay hai "cách hiểu" bằng **một** phát biểu `THEN` đã chốt, kèm một dòng `Ghi chú: chốt tại 04-quyet-dinh-ban-giao.md <mục> (Dat · 2026-09-19)`.

> Đây là sửa **tài liệu đặc tả**, không phải sửa code — nhưng nó là **điều kiện cần** để cổng nghiệm thu chạy được. Làm trước `/gen-be`.

---

## §2. Phân loại vai trò của BE

| Vai trò | Nghĩa | Số luật |
|---|---|---|
| **HIỆN THỰC** | BE quyết định hành vi; mã luật nằm trong hàm quyết định | **114** |
| **KIỂM** | Hành vi do FE tạo ra, BE **chỉ chấp nhận / từ chối** JSON kết quả (`R-TLMI-246` — không được tin FE đã kiểm) | **34** |
| **CẤP DỮ LIỆU** | Luật thuần **pixel / ngắt trang**; BE cấp đủ dữ liệu, FE dựng — quyết định `D3`, **§12 `Q3`** của [00](00-ke-hoach-tong.md) | **15** |
| | **Tổng** | **163 / 163** |

**15 luật `CẤP DỮ LIỆU`:** `R-TLMI-073` `074` `075` `096` `097` `098` `099` `100` `180` `181` `194` `195` `200` `263` `265`.

> ⚠ Với nhóm `CẤP DỮ LIỆU`, mã luật **vẫn phải xuất hiện** trong code BE (ở record JSON hoặc ở hàm dựng dữ liệu) để `trace.sh` không báo `MISSING`, và **đồng thời** xuất hiện ở FE nơi thật sự dựng trang. Đây là ngoại lệ duy nhất của quy tắc "một luật gắn 1–2 điểm".

---

## §3. Bảng truy vết đầy đủ — 163 luật

Cột **Test** ghi `<ClassTest>.R_TLMI_<nnn>_…` — hậu tố mô tả do người code đặt, nhưng **tiền tố `R_TLMI_<nnn>` là bắt buộc** (`docs/rules/truy-vet-luat.md §3`). Đường dẫn file bỏ tiền tố `cell-app/src/main/java/vn/vtt/pmkt/`.

| Luật | Tầng | Sev | Vai trò BE | File dự kiến | Test dự kiến |
|---|---|---|---|---|---|
| `R-TLMI-001` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/entity/MauInTuyChinh.java · internal/repository/MauInTuyChinhRepository.java · V1158` | `MauInServiceTest.R_TLMI_001_…` |
| `R-TLMI-002` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/model/MaNghiepVuMauIn.java · api/dto/NghiepVuMauIn.java` | `DangKyProviderTest.R_TLMI_002_…` |
| `R-TLMI-003` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/model/MaNghiepVuMauIn.java · api/dto/NghiepVuMauIn.java` | `DangKyProviderTest.R_TLMI_003_…` |
| `R-TLMI-004` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/entity/MauInTuyChinh.java · internal/repository/MauInTuyChinhRepository.java · V1158` | `MauInServiceTest.R_TLMI_004_…` |
| `R-TLMI-005` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/entity/MauInTuyChinh.java · internal/repository/MauInTuyChinhRepository.java · V1158` | `MauInServiceTest.R_TLMI_005_…` |
| `R-TLMI-006` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_006_…` |
| `R-TLMI-007` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_007_…` |
| `R-TLMI-008` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_008_…` |
| `R-TLMI-009` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_009_…` |
| `R-TLMI-010` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_010_…` |
| `R-TLMI-011` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/controller/MauInController.java · internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_011_…` |
| `R-TLMI-012` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/controller/MauInController.java · internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_012_…` |
| `R-TLMI-013` | CẢ HAI | P0 | KIỂM | `cell/mau_in/api/MauInProvider.java (mauCoDinh)` | `DungBanInServiceTest.R_TLMI_013_…` |
| `R-TLMI-014` | CẢ HAI | P1 | KIỂM | `cell/mau_in/api/dto/MoTaMauIn.java (maChucNang) · internal/service/business/DangKyProvider.java` | `DangKyProviderTest.R_TLMI_014_…` |
| `R-TLMI-018` | CẢ HAI | P0 | KIỂM | `cell/mau_in/internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_018_…` |
| `R-TLMI-019` | CẢ HAI | P0 | KIỂM | `cell/mau_in/internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_019_…` |
| `R-TLMI-021` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/MauInService.java (luu)` | `MauInServiceTest.R_TLMI_021_…` |
| `R-TLMI-022` | BE | P1 | HIỆN THỰC | `cell/mau_in/internal/service/MauInService.java (luu)` | `MauInServiceTest.R_TLMI_022_…` |
| `R-TLMI-025` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java (menu)` | `DungBanInServiceTest.R_TLMI_025_…` |
| `R-TLMI-028` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/controller/MauInController.java · internal/model/MaQuyenMauIn.java` | `MauInControllerQuyenTest.R_TLMI_028_…` |
| `R-TLMI-031` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/controller/MauInController.java · internal/model/MaQuyenMauIn.java` | `MauInControllerQuyenTest.R_TLMI_031_…` |
| `R-TLMI-033` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/controller/MauInController.java · internal/model/MaQuyenMauIn.java` | `MauInControllerQuyenTest.R_TLMI_033_…` |
| `R-TLMI-034` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/controller/MauInController.java · internal/model/MaQuyenMauIn.java` | `MauInControllerQuyenTest.R_TLMI_034_…` |
| `R-TLMI-035` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/controller/MauInController.java · internal/model/MaQuyenMauIn.java` | `MauInControllerQuyenTest.R_TLMI_035_…` |
| `R-TLMI-036` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_036_…` |
| `R-TLMI-037` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_037_…` |
| `R-TLMI-038` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/HopNhatThietLapChung.java` | `HopNhatThietLapChungTest.R_TLMI_038_…` |
| `R-TLMI-039` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_039_…` |
| `R-TLMI-044` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_044_…` |
| `R-TLMI-046` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/HopNhatThietLapChung.java` | `HopNhatThietLapChungTest.R_TLMI_046_…` |
| `R-TLMI-047` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/HopNhatThietLapChung.java` | `HopNhatThietLapChungTest.R_TLMI_047_…` |
| `R-TLMI-048` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/HopNhatThietLapChung.java` | `HopNhatThietLapChungTest.R_TLMI_048_…` |
| `R-TLMI-049` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/HopNhatThietLapChung.java` | `HopNhatThietLapChungTest.R_TLMI_049_…` |
| `R-TLMI-054` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/GioiHanMauIn.java` | `KiemTraMauGiayVaChuTest.R_TLMI_054_…` |
| `R-TLMI-055` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/GioiHanMauIn.java` | `KiemTraMauGiayVaChuTest.R_TLMI_055_…` |
| `R-TLMI-056` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/GioiHanMauIn.java` | `KiemTraMauGiayVaChuTest.R_TLMI_056_…` |
| `R-TLMI-057` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/GioiHanMauIn.java` | `KiemTraMauGiayVaChuTest.R_TLMI_057_…` |
| `R-TLMI-058` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/GiaiHuongGiay.java` | `GiaiHuongGiayTest.R_TLMI_058_…` |
| `R-TLMI-059` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/GiaiHuongGiay.java` | `GiaiHuongGiayTest.R_TLMI_059_…` |
| `R-TLMI-060` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/GiaiHuongGiay.java` | `GiaiHuongGiayTest.R_TLMI_060_…` |
| `R-TLMI-061` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/GioiHanMauIn.java` | `KiemTraMauGiayVaChuTest.R_TLMI_061_…` |
| `R-TLMI-062` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/GioiHanMauIn.java` | `KiemTraMauGiayVaChuTest.R_TLMI_062_…` |
| `R-TLMI-063` | BE | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/GioiHanMauIn.java` | `KiemTraMauGiayVaChuTest.R_TLMI_063_…` |
| `R-TLMI-064` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/TrangJson.java` | `KiemTraMauNenTest.R_TLMI_064_…` |
| `R-TLMI-065` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/TrangJson.java` | `KiemTraMauNenTest.R_TLMI_065_…` |
| `R-TLMI-066` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/TrangJson.java` | `KiemTraMauNenTest.R_TLMI_066_…` |
| `R-TLMI-067` | CẢ HAI | P2 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/TrangJson.java` | `KiemTraMauNenTest.R_TLMI_067_…` |
| `R-TLMI-068` | CẢ HAI | P2 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/TrangJson.java` | `KiemTraMauNenTest.R_TLMI_068_…` |
| `R-TLMI-069` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/AnhService.java` | `AnhServiceTest.R_TLMI_069_…` |
| `R-TLMI-072` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/TrangJson.java` | `KiemTraMauNenTest.R_TLMI_072_…` |
| `R-TLMI-073` | CẢ HAI | P2 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_073_…` |
| `R-TLMI-074` | CẢ HAI | P2 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_074_…` |
| `R-TLMI-075` | CẢ HAI | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_075_…` |
| `R-TLMI-076` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | `DungKhoiDauTrangTest.R_TLMI_076_…` |
| `R-TLMI-077` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiDauTrangJson.java · internal/service/business/HopNhatThietLapChung.java` | `HopNhatThietLapChungTest.R_TLMI_077_…` |
| `R-TLMI-078` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | `DungKhoiDauTrangTest.R_TLMI_078_…` |
| `R-TLMI-079` | BE | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | `DungKhoiDauTrangTest.R_TLMI_079_…` |
| `R-TLMI-080` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | `DungKhoiDauTrangTest.R_TLMI_080_…` |
| `R-TLMI-082` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | `DungKhoiDauTrangTest.R_TLMI_082_…` |
| `R-TLMI-083` | BE | P2 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | `DungKhoiDauTrangTest.R_TLMI_083_…` |
| `R-TLMI-084` | BE | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiDauTrang.java` | `DungKhoiDauTrangTest.R_TLMI_084_…` |
| `R-TLMI-085` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/KhoiTieuDeJson.java` | `KiemTraMauTieuDeTest.R_TLMI_085_…` |
| `R-TLMI-086` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/KhoiTieuDeJson.java` | `KiemTraMauTieuDeTest.R_TLMI_086_…` |
| `R-TLMI-087` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/KhoiTieuDeJson.java` | `KiemTraMauTieuDeTest.R_TLMI_087_…` |
| `R-TLMI-088` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/KhoiTieuDeJson.java` | `KiemTraMauTieuDeTest.R_TLMI_088_…` |
| `R-TLMI-089` | CẢ HAI | P2 | KIỂM | `cell/mau_in/internal/service/business/KiemTraMau.java · internal/model/json/KhoiTieuDeJson.java` | `KiemTraMauTieuDeTest.R_TLMI_089_…` |
| `R-TLMI-090` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_090_…` |
| `R-TLMI-091` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_091_…` |
| `R-TLMI-092` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiBangJson.java · internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_092_…` |
| `R-TLMI-093` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/HopNhatCatalog.java` | `HopNhatCatalogTest.R_TLMI_093_…` |
| `R-TLMI-094` | CẢ HAI | P2 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiBangJson.java · internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_094_…` |
| `R-TLMI-095` | CẢ HAI | P2 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiBangJson.java · internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_095_…` |
| `R-TLMI-096` | CẢ HAI | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/KhoiBangJson.java` | `DungBanInServiceTest.R_TLMI_096_…` |
| `R-TLMI-097` | CẢ HAI | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/KhoiBangJson.java` | `DungBanInServiceTest.R_TLMI_097_…` |
| `R-TLMI-098` | CẢ HAI | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/KhoiBangJson.java` | `DungBanInServiceTest.R_TLMI_098_…` |
| `R-TLMI-099` | CẢ HAI | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/KhoiBangJson.java` | `DungBanInServiceTest.R_TLMI_099_…` |
| `R-TLMI-100` | CẢ HAI | P2 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/KhoiBangJson.java` | `DungBanInServiceTest.R_TLMI_100_…` |
| `R-TLMI-101` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiBangJson.java · internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_101_…` |
| `R-TLMI-102` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_102_…` |
| `R-TLMI-103` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_103_…` |
| `R-TLMI-104` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_104_…` |
| `R-TLMI-105` | CẢ HAI | P2 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiBangJson.java · internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_105_…` |
| `R-TLMI-106` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiBangJson.java · internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_106_…` |
| `R-TLMI-107` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/KhoiBangJson.java · internal/service/business/MauChuanBuilder.java` | `MauChuanBuilderTest.R_TLMI_107_…` |
| `R-TLMI-108` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_108_…` |
| `R-TLMI-109` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | `ChiaDeuDoRongTest.R_TLMI_109_…` |
| `R-TLMI-111` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | `ChiaDeuDoRongTest.R_TLMI_111_…` |
| `R-TLMI-112` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | `ChiaDeuDoRongTest.R_TLMI_112_…` |
| `R-TLMI-113` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | `ChiaDeuDoRongTest.R_TLMI_113_…` |
| `R-TLMI-114` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/ChiaDeuDoRong.java` | `ChiaDeuDoRongTest.R_TLMI_114_…` |
| `R-TLMI-119` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/CongGopDong.java` | `CongGopDongTest.R_TLMI_119_…` |
| `R-TLMI-121` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_121_…` |
| `R-TLMI-122` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_122_…` |
| `R-TLMI-123` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_123_…` |
| `R-TLMI-125` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_125_…` |
| `R-TLMI-126` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_126_…` |
| `R-TLMI-129` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_129_…` |
| `R-TLMI-130` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_130_…` |
| `R-TLMI-131` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_131_…` |
| `R-TLMI-143` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/OLuoiJson.java` | `DungBanInServiceTest.R_TLMI_143_…` |
| `R-TLMI-144` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/OLuoiJson.java` | `DungBanInServiceTest.R_TLMI_144_…` |
| `R-TLMI-145` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/OLuoiJson.java` | `DungBanInServiceTest.R_TLMI_145_…` |
| `R-TLMI-146` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/OLuoiJson.java` | `DungBanInServiceTest.R_TLMI_146_…` |
| `R-TLMI-147` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java · internal/model/json/OLuoiJson.java` | `DungBanInServiceTest.R_TLMI_147_…` |
| `R-TLMI-153` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_153_…` |
| `R-TLMI-156` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/ThuocTinhTruongJson.java · internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_156_…` |
| `R-TLMI-157` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/ThuocTinhTruongJson.java · internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_157_…` |
| `R-TLMI-158` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/ThuocTinhTruongJson.java · internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_158_…` |
| `R-TLMI-159` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/ThuocTinhTruongJson.java · internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_159_…` |
| `R-TLMI-160` | CẢ HAI | P2 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_160_…` |
| `R-TLMI-161` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_161_…` |
| `R-TLMI-164` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/model/json/ThuocTinhTruongJson.java · internal/service/business/ChuanHoaMau.java` | `ChuanHoaMauTest.R_TLMI_164_…` |
| `R-TLMI-165` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/api/dto/MoTaMauIn.java · internal/service/business/HopNhatCatalog.java` | `HopNhatCatalogTest.R_TLMI_165_…` |
| `R-TLMI-167` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/api/dto/MoTaMauIn.java · internal/service/business/HopNhatCatalog.java` | `HopNhatCatalogTest.R_TLMI_167_…` |
| `R-TLMI-176` | CẢ HAI | P1 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_176_…` |
| `R-TLMI-178` | CẢ HAI | P0 | KIỂM | `cell/mau_in/internal/model/json/KhoiTuDoJson.java · internal/model/json/OLuoiJson.java · internal/service/business/KiemTraMau.java` | `KiemTraLuoiTuDoTest.R_TLMI_178_…` |
| `R-TLMI-180` | BE | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/model/json/OLuoiJson.java` | `KiemTraLuoiTuDoTest.R_TLMI_180_…` |
| `R-TLMI-181` | BE | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/model/json/OLuoiJson.java` | `KiemTraLuoiTuDoTest.R_TLMI_181_…` |
| `R-TLMI-182` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_182_…` |
| `R-TLMI-183` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_183_…` |
| `R-TLMI-184` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_184_…` |
| `R-TLMI-185` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_185_…` |
| `R-TLMI-186` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_186_…` |
| `R-TLMI-187` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_187_…` |
| `R-TLMI-188` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_188_…` |
| `R-TLMI-189` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_189_…` |
| `R-TLMI-190` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_190_…` |
| `R-TLMI-191` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_191_…` |
| `R-TLMI-192` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_192_…` |
| `R-TLMI-193` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_193_…` |
| `R-TLMI-194` | BE | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/business/DungKhoiChuKy.java` | `DungKhoiChuKyTest.R_TLMI_194_…` |
| `R-TLMI-195` | BE | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/business/DungKhoiChuKy.java` | `DungKhoiChuKyTest.R_TLMI_195_…` |
| `R-TLMI-196` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/port/HoSoDonViPort.java · internal/service/adapter/HoSoDonViTheoTenant.java` | `DungKhoiChuKyTest.R_TLMI_196_…` |
| `R-TLMI-197` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_197_…` |
| `R-TLMI-198` | CẢ HAI | P2 | HIỆN THỰC | `cell/mau_in/internal/service/business/DungKhoiChuKy.java · internal/model/json/KhoiChuKyJson.java` | `DungKhoiChuKyTest.R_TLMI_198_…` |
| `R-TLMI-199` | BE | P1 | HIỆN THỰC | `cell/mau_in/internal/port/HoSoDonViPort.java · internal/service/adapter/HoSoDonViTheoTenant.java` | `DungKhoiChuKyTest.R_TLMI_199_…` |
| `R-TLMI-200` | BE | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/business/DungKhoiChuKy.java` | `DungKhoiChuKyTest.R_TLMI_200_…` |
| `R-TLMI-207` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_207_…` |
| `R-TLMI-208` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_208_…` |
| `R-TLMI-209` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_209_…` |
| `R-TLMI-210` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_210_…` |
| `R-TLMI-212` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_212_…` |
| `R-TLMI-236` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_236_…` |
| `R-TLMI-237` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_237_…` |
| `R-TLMI-238` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_238_…` |
| `R-TLMI-239` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_239_…` |
| `R-TLMI-243` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/KiemTraMau.java` | `KiemTraMauTest.R_TLMI_243_…` |
| `R-TLMI-246` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_246_…` |
| `R-TLMI-247` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_247_…` |
| `R-TLMI-248` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_248_…` |
| `R-TLMI-249` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_249_…` |
| `R-TLMI-258` | BE | P1 | HIỆN THỰC | `cell/mau_in/internal/entity/MauInTuyChinh.java (@Version) · internal/service/MauInService.java` | `MauInServiceTest.R_TLMI_258_…` |
| `R-TLMI-259` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_259_…` |
| `R-TLMI-260` | CẢ HAI | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_260_…` |
| `R-TLMI-261` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_261_…` |
| `R-TLMI-262` | BE | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_262_…` |
| `R-TLMI-263` | BE | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_263_…` |
| `R-TLMI-264` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_264_…` |
| `R-TLMI-265` | BE | P1 | CẤP DỮ LIỆU | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_265_…` |
| `R-TLMI-266` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/service/business/CongGopDong.java · internal/service/DungBanInService.java` | `CongGopDongTest.R_TLMI_266_…` |
| `R-TLMI-267` | BE | P0 | HIỆN THỰC | `cell/mau_in/internal/port/HoSoDonViPort.java` | `DungBanInServiceTest.R_TLMI_267_…` |
| `R-TLMI-270` | CẢ HAI | P0 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java` | `DungBanInServiceTest.R_TLMI_270_…` |
| `R-TLMI-271` | BE | P1 | HIỆN THỰC | `cell/mau_in/internal/service/DungBanInService.java (@Transactional readOnly)` | `DungBanInServiceTest.R_TLMI_271_…` |

---

## §4. Bảng truy vết 12 bất biến `INV-TLMI-nnn`

`02-rules.md §X` yêu cầu: **mỗi bất biến bắt buộc có ít nhất một test mang chính mã** `INV-TLMI-nnn` trong tên; thiếu ⇒ `/verify-spec` chấm FAIL.

| Bất biến | Nơi cưỡng chế | Test dự kiến |
|---|---|---|
| `INV-TLMI-001` | `V1158` — unique index `(tenant_id, ma_loai_chung_tu, ma_nghiep_vu) WHERE da_xoa = false` | `MauInMigrationTest.INV_TLMI_001_unique_index_gom_du_ba_cot` |
| `INV-TLMI-002` | `MauInService.luu` bước 6 (`D5`) | `MauInServiceTest.INV_TLMI_002_mau_bang_chuan_thi_khong_ton_tai_ban_ghi` |
| `INV-TLMI-003` | `ChuanHoaMau` (xoá khoá `null`) + cấm gọi `HopNhatThietLapChung` từ luồng Lưu | `ChuanHoaMauTest.INV_TLMI_003_o_theo_chung_thi_khoa_vang_mat` |
| `INV-TLMI-004` | `KiemTraMau` V03 | `KiemTraMauTest.INV_TLMI_004_bang_dang_bat_luon_con_it_nhat_mot_cot` |
| `INV-TLMI-005` | `ChuanHoaMau` → `ChiaDeuDoRong` | `ChiaDeuDoRongTest.INV_TLMI_005_do_rong_da_luu_luon_tong_bang_100` |
| `INV-TLMI-006` | `KiemTraMau` V06…V09 | `KiemTraLuoiTuDoTest.INV_TLMI_006_tran_va_san_cua_khoi_tu_do` |
| `INV-TLMI-007` | `KiemTraMau` | `KiemTraLuoiTuDoTest.INV_TLMI_007_mot_truong_toi_da_mot_o_trong_mot_khoi` |
| `INV-TLMI-008` | `KiemTraMau` (đếm theo `loai`) | `KiemTraMauTest.INV_TLMI_008_bon_loai_khoi_chuan_luon_ton_tai` |
| `INV-TLMI-009` | Cấu trúc `truong` là **map** — đúng theo kiểu dữ liệu | `ChuanHoaMauTest.INV_TLMI_009_thuoc_tinh_truong_duy_nhat_trong_mau` |
| `INV-TLMI-010` | `KiemTraMau` V12 | `KiemTraMauTest.INV_TLMI_010_o_ky_tu_do_dang_bat_luon_co_tieu_de` |
| `INV-TLMI-011` | Không có khoá `chiNhanhId` trong schema; repository không lọc chi nhánh | `MauInServiceTest.INV_TLMI_011_mau_khong_mang_pham_vi_chi_nhanh` |
| `INV-TLMI-012` | `@Transactional` trên `MauInService.luu` | `MauInServiceTest.INV_TLMI_012_luu_la_all_or_nothing` |

---

## §5. Danh sách class test — tất cả `@Tag("unit")`

Máy này **cấm Docker** ⇒ **không** viết test Testcontainers trong phiếu này. Mọi nghiệp vụ đẩy xuống `business/` để unit-test thuần. Migration kiểm bằng cách **đọc nội dung file `.sql`** (cách `MauInMigrationTest` bản cũ đã làm).

### 5.1 Class mới

| Class | Vị trí | Số test tối thiểu | Phủ luật |
|---|---|---|---|
| `ChiaDeuDoRongTest` | `mau_in/internal/service/business/` | 7 | `109` `111` `112` `113` `114` · `INV-TLMI-005` |
| `GiaiHuongGiayTest` | `mau_in/internal/service/business/` | 5 | `058` `059` `060` |
| `CongGopDongTest` | `mau_in/internal/service/business/` | 5 | `119` `266` |
| `HopNhatThietLapChungTest` | `mau_in/internal/service/business/` | 8 | `036`…`052` · `077` |
| `KiemTraMauGiayVaChuTest` | `mau_in/internal/service/business/` | 11 | `053`…`063` |
| `KiemTraMauNenTest` | `mau_in/internal/service/business/` | 8 | `064`…`075` |
| `KiemTraMauTieuDeTest` | `mau_in/internal/service/business/` | 7 | `085`…`091` |
| `KiemTraLuoiTuDoTest` | `mau_in/internal/service/business/` | 20 | `120`…`181` · `INV-TLMI-006` `007` |
| `ChuanHoaMauBoCucTest` | `mau_in/internal/service/business/` | 8 | `201`…`216` |
| `DungKhoiDauTrangTest` | `mau_in/internal/service/business/` | 7 | `076`…`084` |
| `DungKhoiChuKyTest` | `mau_in/internal/service/business/` | 10 | `182`…`200` |
| `XemTruocServiceTest` | `mau_in/internal/service/` | 6 | `217`…`229` |
| `DungBanInServiceTest` | `mau_in/internal/service/` | 15 | `023`…`027` · `090` `091` `096`…`100` · `143`…`147` · `207`…`209` · `259`…`271` |
| `ThietLapChungServiceTest` | `mau_in/internal/service/` | 6 | `F06` — [02 §5](02-hop-dong-json-thiet-lap-chung.md) |
| `AnhServiceTest` | `mau_in/internal/service/` | 6 | `069` `071` |
| `HoSoDonViTheoTenantTest` | `mau_in/internal/service/adapter/` | 5 | `078` `196` `199` `267` |

### 5.2 Class sửa lại từ bản cũ

| Class | Bản cũ | Sau khi sửa |
|---|---|---|
| `MauInServiceTest` | 13 test, tên `A1…A7` | ~20 test, tên `R_TLMI_*` + 4 `INV_TLMI_*` |
| `MauInControllerQuyenTest` | 5 test gate quyền | ~7 test, thêm tầng quyền `<ChucNang>.View.Detail` |
| `KiemTraMauTest` | 13 test luật cũ | ~18 test theo 17 dòng của `R-TLMI-239` + thứ tự lỗi đầu tiên |
| `ChuanHoaMauTest` | 5 | ~12 — [07 §7](07-chuan-hoa-kiem-tra-va-thuat-toan.md) |
| `MauChuanBuilderTest` | 5 | ~8 |
| `HopNhatCatalogTest` | 6 | ~8 |
| `MauInJsonCodecTest` | 4 | 4 (đổi `schemaVersion` 1 → 2) |
| `DangKyProviderTest` | 2 | 5 (thêm 3 kiểm `nghiepVu()`) |
| `MauInMigrationTest` | 4 | ~11 — [08 §10](08-thiet-ke-db.md) |
| `MauInTestData` | fixture v1 | fixture v2 |
| `XuatCatalogMauInTest` | 2 | 2 (thêm `maNghiepVu`) |
| `arch/MauInModularityTest` | 1 | 1 — giữ nguyên, càng cần sau khi thêm `internal/port/` |
| `MauInLichSuServiceTest` | 8 | ~4 (chỉ giữ phần **ghi**) |
| Provider test × 6 (`BH` `MDV` `PT/PC`) | 30 | ~30 (catalog v2) |

### 5.3 Class bỏ

`MacDinhHeThongCacheTest` · `MacDinhHeThongRestTest` · `GiaiMauHieuLucTest` — theo code của kênh super-admin và chuỗi 3 tầng (`D13`).

**Ước lượng tổng: ~200 test `@Tag("unit")`**, chạy trong cổng `./gradlew unitTest` (~1 phút, không cần Docker).

---

## §6. Cách gắn mã luật vào code — ví dụ mẫu

**Nơi hiện thực chính:**

```java
/**
 * R-TLMI-114 — Thuật toán chia đều về 100%: làm tròn XUỐNG, phần thiếu dồn vào cột in cuối cùng,
 * cột < 3 nâng lên 3 và trừ vào cột rộng nhất. GIỮ NGUYÊN TỶ LỆ, không chia bằng nhau.
 * (nguồn: 02-rules.md R-TLMI-114; ba ca chốt của BA: 40/40/40→33/33/34, 50/30→62/38)
 */
static List<KhoiBangJson.Cot> chiaDeuVe100(List<KhoiBangJson.Cot> cot) { … }
```

**Test:**

```java
@Test
@Tag("unit")
@DisplayName("R-TLMI-114 · chia 40/40/40 thành 33/33/34")
void R_TLMI_114_chia_40_40_40_thanh_33_33_34() { … }
```

**Luật chỉ thể hiện qua cấu hình** — gắn ở đúng dòng:

```java
public record TrangJson(
        String kho,                    // R-TLMI-054 — A3/A4/A5; VẮNG = theo thiết lập chung
        String huong,                  // R-TLMI-055 — DOC/NGANG/TU_DONG; VẮNG = theo thiết lập chung
        Integer soCotTuDongNgang,      // R-TLMI-057 — 1..50, chỉ có nghĩa khi huong = TU_DONG
        …) { }
```

**Bất biến** — gắn ở nơi **cưỡng chế**, không phải nơi gọi:

```java
/** INV-TLMI-003 — ô theo thiết lập chung ⇒ KHOÁ VẮNG MẶT trong JSON đã lưu, không bao giờ là null. */
private static ObjectNode boKhoaNull(ObjectNode node) { … }
```

---

## §7. Cổng nghiệm thu

```bash
# 1. Cập nhật 8 luật CHỜ → CHỐT trong 02-rules.md   (§1 — LÀM TRƯỚC)
# 2. Cổng test
cd cell-app && ./gradlew unitTest

# 3. Cổng truy vết
./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec be
./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec be --missing

# 4. Cổng cây commit
git -C cell-app status          # KHÔNG còn dòng '??' trong src/
```

| Trạng thái `trace.sh` | Được báo "xong"? |
|---|---|
| `OK` | ✅ |
| `NO-TEST` | ❌ với `P0` · ⚠ với `P1`/`P2` — ghi nợ tường minh trong báo cáo bàn giao |
| `MISSING` | ❌ — **luật chưa được hiện thực**, bất kể code trông có vẻ đúng |
| `VI-PHAM` | ❌ — code chạm luật đang `CHỜ`; xử lý ở §1 |

**Cổng `msg.sh` chưa chạy được** — nó cần đường dẫn PYC trong `pmkt-docs/ba/`, mà PYC này nằm trong vùng đóng băng `Phase_2`. Xem §12 `Q6` của [00](00-ke-hoach-tong.md).

**Testcontainers không chạy** (máy cấm Docker) ⇒ RLS, `GRANT`, và hành vi thật của unique index **chưa được kiểm trên Postgres thật**. Phải **báo rõ** điều này khi bàn giao.
