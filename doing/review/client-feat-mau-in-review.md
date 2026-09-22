# Review nhanh — `client` / `feat/mau-in`

## Phạm vi và snapshot

- Chế độ: **nhanh** — yêu cầu kiểm tra nghiệp vụ nút `In` / menu `Mẫu tùy chỉnh`; không chạy build hay test.
- HEAD: `75a27e272ef20659dabab63b4108de2f09a8bcbe` (`feat: mẫu in`).
- `origin/develop`: `77f5578a628138bba81e6e4a40b9e46461808a59`; merge-base: `aba54c41a00976304670d3dd7040cd40832e667b`.
- Working tree có 18 file sửa, gồm `NutInChungTu.tsx`, modal xem trước và chỗ mount tại chứng từ bán hàng. Không sửa code trong review này.
- Nguồn nghiệp vụ: `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/02-rules.md`, đặc biệt R-TLMI-023…033 và R-TLMI-259…271. Package BA gốc của epic nằm Phase 2; không đọc trực tiếp trong lượt này.

## Kết luận

**REJECT — có Blocker.** Menu có đúng thứ tự/nhãn và `Mẫu tùy chỉnh` đã đi vào màn xem trước, nhưng đường chạy khi API chưa sẵn sàng vi phạm nghiệp vụ dựng bản in và bỏ qua quyền In riêng của nghiệp vụ.

## Findings

### Blocker — lỗi API lại mở bản in bằng dữ liệu mock

- Bằng chứng: `client/src/base/domainKit/mauIn/constants/constants.ts:185` đặt `DUNG_MOCK_KHI_BE_LOI = true`; `components/modal/XemTruocBanInModal.tsx:62-63` thay A1/A5 lỗi bằng `hieuLucMock` và `duLieuInMock`.
- Trigger: endpoint mẫu hiệu lực hoặc dữ liệu chứng từ trả lỗi/không tồn tại — chính chú thích ở `api/mauInApi.ts:7` xác nhận BE chưa có endpoint đúng hợp đồng.
- Actual: UI vẫn mở preview theo dữ liệu/chứng từ mẫu tĩnh, thay vì trả về form và báo lỗi.
- Expected: R-TLMI-270 yêu cầu lỗi hệ thống khi dựng bản in phải báo `MSG_PMKT-E-14549_21_003` và **không mở** màn xem trước; R-TLMI-259 yêu cầu bản in dùng mẫu và dữ liệu của chứng từ đang mở.
- Hậu quả: người dùng nhìn/in dữ liệu không thuộc chứng từ đang thao tác, đồng thời trạng thái BE thiếu API bị che lấp.

### Blocker — không có cổng quyền `In` của nghiệp vụ trước khi dựng bản tùy chỉnh

- Bằng chứng: `components/NutInChungTu.tsx:35,63,89` chỉ nhận và kiểm `quyenXemChiTiet`; điều kiện sửa mẫu ở dòng 70 dùng `HTMauIn.Edit`. Chỗ mount ở `features/banHang/chungTuBanHang/components/ChungTuBanHangThemMoiModal.tsx:1560-1562` cũng chỉ truyền quyền `View.Detail`.
- Trigger: người dùng có quyền xem chi tiết nhưng không có quyền In của nghiệp vụ.
- Actual: nút/menu vẫn render và nhấn chính mở bản xem trước; khi A1/A5 lỗi, Blocker trên còn biến nó thành preview mock.
- Expected: BA chứng từ hiện hữu quy định quyền `*.Print`; R-TLMI-033 chỉ cho phép `Mẫu tùy chỉnh` khi có **quyền In** (không có quyền Thiết lập mẫu in vẫn được in), và backend phải chặn gọi thẳng API không đủ quyền.
- Hậu quả: cổng phân quyền in không được thể hiện ở FE và không có BE hợp đồng để chứng minh cổng server.

### Major — endpoint và mẫu cố định chưa được nối hoàn chỉnh

- Bằng chứng: `api/mauInApi.ts:7` ghi rõ BE chưa có A1…A6; `NutInChungTu.tsx:110` disable mọi mẫu cố định khi không truyền `onInMauCoDinh`, trong khi chỗ mount ở `ChungTuBanHangThemMoiModal.tsx:1553-1568` không truyền callback này.
- Expected: R-TLMI-013 yêu cầu mẫu cố định vẫn in như cũ; R-TLMI-023 yêu cầu menu nhận các mẫu cố định nghiệp vụ trước mục `Mẫu tùy chỉnh`.
- Giới hạn: chưa đủ bằng chứng để kết luận chứng từ bán hàng hiện phải có mẫu cố định nào; đây là thiếu hoàn chỉnh tích hợp, không khẳng định thiếu một mẫu cụ thể.

## Các phần đúng trong phạm vi đọc

- `NutInChungTu.tsx:101-115` dựng đúng thứ tự: mẫu cố định → phân cách → `Mẫu tùy chỉnh` → `Thiết lập mẫu in…`.
- Nhấn nửa chính nút In hay chọn `Mẫu tùy chỉnh` đều mở cùng màn xem trước (`NutInChungTu.tsx:76-80,125`).
- Chưa có bản ghi mẫu dùng mẫu chuẩn và hiện `MSG_..._103` một lần mỗi lần mở (`XemTruocBanInModal.tsx:83-96`), đúng R-TLMI-260 nếu dữ liệu A1/A5 là thật.
- Nút `Thiết lập mẫu in…` / `Sửa mẫu` được ẩn thay vì disable khi thiếu quyền sửa mẫu (`NutInChungTu.tsx:70,113-117`; `XemTruocBanInModal.tsx:173-178`), đúng R-TLMI-032 ở mức giao diện.

## Bốn lớp và bảy lỗi thường gặp

| Hạng mục | Kết quả |
|---|---|
| Cổng cứng | Blocker: nghiệp vụ/permission và mock nêu trên |
| Kiến trúc thư mục | N/A — không có file mới trong diff đã đọc |
| Migration | N/A — phạm vi FE |
| Test sau merge | NOT-RUN — review nhanh |
| N+1 FE | Không thấy trong lối vào In đã đọc |
| Base FE | Không thấy vi phạm trong lối vào đã đọc |
| Constant | `DUNG_MOCK_KHI_BE_LOI` là cờ nợ kỹ thuật nhưng gây Blocker khi bật production |

## Kiểm chứng chưa chạy

- `trace.sh` và `msg.sh`: NOT-RUN — máy hiện không có `bash`; `msg.sh` còn yêu cầu PYC BA nằm trong vùng Phase 2 đóng băng.
- Typecheck, lint, test, build: NOT-RUN theo chế độ nhanh.
- Không kiểm chứng UI chạy thật; ảnh đính kèm chỉ xác nhận menu đang hiển thị đúng hai nhãn.
