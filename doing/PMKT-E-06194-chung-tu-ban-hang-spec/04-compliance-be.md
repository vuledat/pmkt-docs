# PMKT-E-06194 Chứng từ bán hàng — Đối chiếu code ↔ đặc tả (BE)

| | |
|---|---|
| Đặc tả | `docs/doing/PMKT-E-06194-chung-tu-ban-hang-spec/02-rules.md` |
| Commit spec | `8cf9606ea` |
| Code chấm tại | `cell-app` @ `c6cb948e` — nhánh `feat/chung-tu-ban-hang-2` |
| Ngày chấm | 2026-09-08 |
| Phạm vi | Nhóm ghi sổ R-CTBH-091…112 và các bất biến/kịch bản liên quan S-066…S-079 |
| **Kết luận** | **FAIL** — luồng ghi sổ lõi có code, nhưng chưa phủ đủ nghiệp vụ bỏ ghi sổ và xem dữ liệu ghi sổ |

## 1. Bảng chấm nhóm ghi sổ

| Luật | Mức | Code | Test | Ghi chú |
|---|---|---|---|---|
| R-CTBH-091 | ⚠️ | `accounting_core/chung_tu/service/ChungTuTemplate.java:419-420`; route `BaseChungTuController.java:111-114` | `BanHangSinhCongNoIntegrationTest.java:60` | Có kiểm quyền Post, chưa có test thiếu quyền trực tiếp |
| R-CTBH-092 | ❌ | `ChungTuTemplate.java:272-283`, `:658` | — | Ghi/bỏ ghi có kiểm kỳ qua kernel, nhưng luồng Xóa không gọi kiểm kỳ dù luật yêu cầu chặn cả Xóa |
| R-CTBH-093 | ⚠️ | `DinhKhoanBanHang.java:149-199` | `TinhToanVaDinhKhoanBanHangTest.java:61-159`, `QuyTacMoiBanHang2026Test.java:167-229` | #1–#5 và #7 có ca kiểm; chưa có test end-to-end chứng minh đủ 5 bút toán và nhánh #6 cho CTBH |
| R-CTBH-094 | ✅ | `GhiSoService.java:147-175` | `GhiSoServiceTest.java:79-120` | Mỗi `DinhKhoan` tách đúng hai vế đảo nhau |
| R-CTBH-095 | ✅ | `DinhKhoanBanHang.java:249-263` | `QuyTacMoiBanHang2026Test.java:167-229` | Giữ `chiTietChungTuId`, `sttDongChiTiet`, `sttButToan` và chiều phân tích theo dòng |
| R-CTBH-096 | ⚠️ | `HangLoatChungTuService.java:44-87` | — | Có partial success theo từng transaction, chưa có test 3 thành công/2 thất bại và message popup |
| R-CTBH-097 | ⚠️ | `LuuChungTuBanHangTemplate.java:220-226`; `GhiSoChungTuBanHang.java:111-153` | `BanHangSinhCongNoIntegrationTest.java:270-348` | Đã có nhóm phiếu thu; chưa có test đầy đủ CTBH + PXK + phiếu thu trong cùng giao dịch |
| R-CTBH-098 | ⚠️ | `ChungTuTemplate.java:125-177`; `LapPhieuXuatKhoTuChungTuBan.java:90-103` | — | Transaction rollback được thiết kế, chưa có test lỗi PXK làm rollback toàn nhóm |
| R-CTBH-099 | ⚠️ | `GhiSoChungTuBanHang.java:111-153` | `BanHangSinhCongNoIntegrationTest.java:414-429` | Không gọi ghi sổ hóa đơn, nhưng chưa có test snapshot trạng thái hóa đơn trước/sau Ghi/Bỏ ghi |
| R-CTBH-100 | ⚠️ | `ChungTuTemplate.java:419-420`; `BoGhiSoChungTuBanHang.java:68-76` | — | Có chặn trạng thái và quyền qua template, thiếu test trực tiếp quyền Unpost và mã lỗi |
| R-CTBH-101 | ❌ | `BoGhiSoChungTuBanHang.java:91-104`; `SoCongNoBanHangService.java:101-105` | `BanHangSinhCongNoIntegrationTest.java:394-410` | Luồng công nợ dùng `MSG_PMKT-E-06194_014`, trong khi rule yêu cầu `_049` cho phiếu thu lập riêng đã ghi sổ; chưa phân biệt chắc chắn phiếu thu riêng/kiêm ở guard này |
| R-CTBH-102 | ❌ | `SoCongNoBanHangService.java:101-105` | `BanHangSinhCongNoIntegrationTest.java:394-410` | Có chặn đối trừ nhưng trả mã dùng chung `_014`, không phải `MSG_PMKT-E-06194_052` theo rule |
| R-CTBH-103 | ❌ | `BoGhiSoChungTuBanHang.java:96-104` | — | `coChungTuConLapRiengDaGhiSo(ct)` làm bỏ ghi sổ bị chặn khi PXK lập riêng đã ghi sổ, trái rule yêu cầu PXK lập riêng không chặn |
| R-CTBH-104 | ⚠️ | `ChungTuTemplate.java:272-283`, `SoCaiRepository.java:54-67`; `BoGhiSoChungTuBanHang.java:115-129` | `BanHangSinhCongNoIntegrationTest.java:360-370` | Có xóa sổ cái, công nợ và con kiêm; chưa có test đầy đủ cả nhóm PXK + phiếu thu + sổ kho |
| R-CTBH-105 | ⚠️ | `BoGhiSoChungTuBanHang.java:123-129` | — | Không gọi cập nhật trạng thái xuất hàng/HĐ trong luồng bỏ ghi, nhưng chưa có test chứng minh counter/trạng thái giữ nguyên |
| R-CTBH-106 | ⚠️ | `BoGhiSoChungTuBanHang.java:117-125`; `SoCongNoBanHangService.java:140-149` | `BanHangSinhCongNoIntegrationTest.java:322-348` | Có gỡ phiếu thu kiêm trước dòng gốc; chưa assert trực tiếp `SoTienDaThanhToan` và cả ba trạng thái thanh toán |
| R-CTBH-108 | ❌ | `BaseChungTuController.java:157-164` | — | Endpoint chỉ đọc sổ cái đã ghi; không có nhánh chọn Xem trước theo trạng thái chứng từ |
| R-CTBH-109 | ❌ | `BaseChungTuController.java:157-164`; `SoCaiDocService.java:29-33` | — | Chưa có API preview dùng dữ liệu form và chưa chứng minh không cấp số/không ghi `acc_so_cai` |
| R-CTBH-110 | ❌ | `SoCaiDocService.java:29-33`; `SoCaiRepository.java:28-34` | — | Chỉ đọc theo một `chungTuId`, không gom bút toán của CTBH + PXK + phiếu thu trong nhóm |
| R-CTBH-111 | ❌ | `BaseChungTuController.java:157-164` | — | Không có luồng preview để bỏ riêng bút toán thiếu tài khoản mà vẫn trả các bút toán còn lại |
| R-CTBH-112 | ❌ | `SoCaiRepository.java:28-34` | — | SQL sắp theo `taiKhoanId`; không bảo đảm vế Nợ đứng trước vế Có theo đặc tả, đồng thời chưa sắp theo toàn nhóm |

## 2. Findings chặn hoàn thành

### R-CTBH-103 ❌ PXK lập riêng đang bị chặn bỏ ghi sổ

`BoGhiSoChungTuBanHang.java:96-104` đưa `coChungTuConLapRiengDaGhiSo(ct)` vào điều kiện ném lỗi. Rule R-CTBH-103 yêu cầu PXK lập riêng có trạng thái bất kỳ không được chặn bỏ ghi sổ CTBH; hai chứng từ có vòng đời ghi sổ độc lập. Hậu quả là CTBH không thể bỏ ghi sổ để điều chỉnh khi đã có PXK lập riêng đã ghi sổ.

### R-CTBH-101/R-CTBH-102 ❌ Mã lỗi không phân biệt đúng nghiệp vụ

`SoCongNoBanHangService.kiemTraTruocKhiGo()` dùng `MSG_PMKT-E-06194_014` cho mọi trường hợp đang bị đối trừ. Đặc tả yêu cầu `_049` cho phiếu thu lập riêng đã ghi sổ và `_052` cho chứng từ đang tham gia đối trừ. FE không thể hiển thị hoặc xử lý đúng theo nguyên nhân.

### R-CTBH-108…112 ❌ Chưa có đầy đủ luồng xem dữ liệu ghi sổ

`BaseChungTuController.thongTinHachToan()` chỉ gọi `soCai.theoChungTu(id)`. Vì vậy hiện thiếu cả chế độ Xem trước, phạm vi cả nhóm liên kết, xử lý dòng thiếu tài khoản và thứ tự hiển thị Nợ trước Có. Đây là thiếu chức năng BE, không chỉ thiếu test.

### R-CTBH-092 ❌ Xóa trong kỳ khóa chưa được chặn

`ChungTuTemplate.luongXoa()` không gọi `kiemTraKyKeToan()` hoặc một kiểm tra tương đương. Rule R-CTBH-092 áp dụng cho Ghi sổ, Bỏ ghi sổ và Xóa.

## 3. Bất biến và kịch bản

| Mục | Mức | Bằng chứng |
|---|---|---|
| INV-001 cân đối Nợ = Có | ✅ | `GhiSoServiceTest.java:79-120` |
| INV-002 ghi sổ nhóm nguyên tử | ⚠️ | Có `@Transactional` ở `ChungTuTemplate.java:125`, nhưng chưa có test lỗi PXK/nhóm chứng minh rollback toàn bộ |
| INV-003 thanh toán không âm và khớp trạng thái | ⚠️ | Có test service công nợ, chưa có test xuyên suốt Bỏ ghi sổ CTBH + phiếu thu kiêm |
| INV-014 không ghi vào kỳ khóa | ⚠️ | Kernel có `kiemTraKyMo`, chưa có test module cho Ghi/Bỏ ghi và Xóa |
| S-066 | ⚠️ | Có đường kiểm kỳ trong kernel, thiếu test kịch bản |
| S-067/S-068 | ⚠️ | Có test định khoản rời, chưa có test DB xác nhận số dòng `acc_so_cai` theo đúng kịch bản |
| S-069 | ⚠️ | Có code hàng loạt, chưa có test kết quả 3/2 |
| S-070 | ⚠️ | Có test công nợ/phiếu thu, chưa assert trạng thái cả nhóm và hóa đơn không đổi |
| S-071 | ⛔ | Chưa tìm thấy test rollback khi PXK thiếu tồn |
| S-072/S-073 | ⚠️ | Có guard công nợ, nhưng mã lỗi riêng chưa đúng/không được assert |
| S-074 | ❌ | Code đang chặn PXK lập riêng, trái expected của scenario |
| S-075/S-076 | ⚠️ | Có test một phần, thiếu assert đủ sổ cái, kho, công nợ và trạng thái thanh toán |
| S-077/S-078/S-079 | ⛔ | Chưa có luồng BE preview/nhóm tương ứng |

## 4. Nghiệp vụ không có nguồn hoặc có nguy cơ chặn rộng hơn đặc tả

| Code | Hành vi | Đánh giá |
|---|---|---|
| `BoGhiSoChungTuBanHang.java:96-104` | Chặn bỏ ghi sổ khi chi tiết có `hoaDonBanHangId` | R-CTBH-099 chỉ yêu cầu hóa đơn không đồng bộ ghi sổ; đặc tả không quy định đây là điều kiện chặn bỏ ghi sổ. Cần BA xác nhận hoặc thu hẹp điều kiện. |
| `SoCongNoBanHangService.java:101-105` | Dùng một mã `_014` cho nhiều nguyên nhân chặn | Không khớp bộ message nguyên tử của R-CTBH-101/R-CTBH-102. |

## 5. Kết quả cổng

- `cd cell-app; ./gradlew unitTest`: **BUILD SUCCESSFUL**; 5 task up-to-date.
- Test DB/Testcontainers: chưa chạy trong lượt này vì môi trường không chạy Docker.
- `trace.sh ... be`: `Tong 93 luat (tang=be): OK 0 · NO-TEST 2 · MISSING 84 · BLOCKED 7 · VI-PHAM 0`.
- `msg.sh ... be`: `Tong 60 message (tang=be): OK 31 · LECH 0 · THIEU-VI 0 · CHUA-DAT 0 · THIEU 29`.

`trace.sh` là baseline truy vết mã luật; nhiều luật cũ chưa có marker nên không dùng riêng kết quả `MISSING` để kết luận. Các kết luận ❌ ở trên đều có bằng chứng code cụ thể.

