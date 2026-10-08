# Kết quả bổ sung phân trang — 2026-10-08

Đầu vào: [ra-soat-phan-trang-2026-10-07.md](ra-soat-phan-trang-2026-10-07.md). Phạm vi: `client` + `cell-app`.
Trạng thái: **chưa commit**, nằm trên working tree nhánh `develop` của cả hai repo (client 391 file, cell-app 274 file; không còn `??`).

Loại trừ theo yêu cầu: nhóm E (xem dữ liệu ghi sổ / thông tin hạch toán / xem trước của 1 chứng từ).
Ngoài phạm vi: nhóm F (super-admin, tenant-provisioning, report-service, client-admin), D7 (`features/danhMuc` là nhánh chết), A7 (cây tham số báo cáo — chờ BA).

## Cổng kiểm tra

| Lệnh | Kết quả |
|---|---|
| `cd cell-app && ./gradlew unitTest` | 6571 test, 5 đỏ → sửa 1 (`KhaiBaoCpttEndpointMappingTest`, do gỡ route `/tai-khoan`), **4 còn lại đỏ y hệt trên bản HEAD sạch**: `HandlerAuthorizationArchTest` (chỉ `BieuMauProxyController`), `ChiPhiTraTruocModularityTest` (thông điệp trùng HEAD), `DcgmMauInTest`, `LoaiChungTuSearchTest` |
| `cd client && npx vite build` | ✓ |
| Test FE nghi vấn (14 file) | Chạy song song trên HEAD sạch và working tree: đỏ trùng nhau (nợ nền). 1 test mới đỏ (`nganQuy/_shared/test/lamMoiSauKhiLuu.cache.test.tsx`, do khoá cache Đính kèm đổi sang dạng trang) — đã sửa, xanh |
| Test hẹp từng cụm | Xanh (chi tiết theo cụm bên dưới) |
| **Chưa chạy** | IT Testcontainers (cần Docker: `TimUngVienSqlIT`, `PhanLoaiChungTuIT`, `PhanLoaiSoDuIT`, `LuuChuyenTienTe*IT`, `BuTruCongNoApiE2eTest`, `UngVienBuTruIntegrationTest`…); `npm run typecheck` / lint / full suite FE; test tay trên UI |

## Đã làm (theo ID trong báo cáo quét)

- **Tầng chung FE**: A1 `CommonComboGrid` chế độ `serverPagination` + hook `useServerComboGrid`; A3 mặc định 20/trang (`BR1_PAGE_SIZE`) + tự gắn tổng ở nhánh server; A4 JSDoc `listAll` chỉ cho xuất Excel; A5 `ReferencePickerModal` chế độ server; A6 `SourceSearch` có trang; A9 panel Đính kèm phân trang server.
- **Popup chọn chứng từ/nguồn**: B1 Tham chiếu (SQL 1 câu UNION ALL + LIMIT/OFFSET), B2 ô đối tượng Đối trừ, B3–B6 bán hàng, B7–B10 mua hàng, B11 CPTT, B12 nguồn hình thành TSCĐ, B13 hóa đơn giảm thuế, B15–B16 phân loại BCTC, B17–B19 kho, B20 khoá sổ, B21 `gia-tri-cot`.
- **Picker danh mục**: C1, C2 (+ sửa N+1), C3, C4 (một phần), C5, C6, C7, C8 (CPTT + giá thành), C9, C10, C11.
- **Lưới màn chính**: D1, D2, D3, D4 (nhập kho TP), D6, D8 (tính giá thành, chi tiết kỳ).
- **A2 (tải hết danh mục)**: xong ở tổng hợp, ngân quỹ, số dư ban đầu, CPTT, giá thành, TSCĐ (một phần); **một phần** ở bán hàng, mua hàng, kho.

## Chưa làm / làm một phần — cần quyết định

1. **A2 trong form chứng từ bán hàng, mua hàng, kho (và `ghiTangTSCD`, `dieuChinhTSCD`)** — ô select/lưới vẫn nạp cả danh mục vì logic tự điền đọc `byId` trên toàn bảng (hệ số quy đổi BR16, luật MST, tồn kho). Cần một lượt refactor riêng từng popup (~40 điểm gọi ở bán hàng).
2. **C4 tồn kho**: popup Xuất kho, Xuất điều chuyển vẫn gọi `/ton-kho` không lọc (ghi tồn đồng bộ lúc chọn mã hàng).
3. **B2 lưới `chung-tu-kha-dung`** giữ phân trang client: BR02 tự phân bổ, BR03 cân tổng, "chọn tất cả theo ngân sách" chạy trên toàn tập.
4. **B14 chọn hóa đơn bảng kê**: vẫn cắt trang trong RAM (gộp 11 module nguồn), đã thêm `@Max(200)`.
5. **B12**: loại "đã dùng" bằng tham số `uuid[]`, chưa `NOT EXISTS` (muốn vậy phải đảo ranh giới Modulith).
6. **A9 tab Đính kèm Sửa/Xem**: vẫn phân trang client vì `gan-doi-tuong` ghi đè cả danh sách (đã sửa lỗi mất tệp > 100).
7. **D6 bù trừ, wizard thu/trả tiền theo hóa đơn**: cắt trang trong RAM / tải hết vì nguồn `so_cong_no` chưa có tham số trang.
8. **Giữ nguyên có lý do**: D5 (đạt BR40), D4 phân bổ `/danh-sach`, D8 cấu hình hệ số tỷ lệ (cây, client theo gốc), nhập Excel số dư ban đầu (master_data không tra theo danh sách mã).

## Lệch BR / cần BA chốt

- "Chọn tất cả" (header lưới) chỉ chọn trang đang xem ở popup Tham chiếu; "mặc định chọn tất cả dòng thỏa mãn" ở popup nguồn TLHB/DCG chỉ áp cho trang đã mở.
- Dòng tổng chỉ cộng trang đang xem: popup chọn nguồn điều chỉnh giá bán; chưa có dòng tổng FE ở Tính giá thành + Xem chứng từ phân bổ (BE đã trả `summary`).
- Phân loại BCTC: tìm/phễu cột phân loại chỉ khớp giá trị đã lưu; tổng Bước 2 chưa tính nháp; API lưu thêm `macDinhTheoKy` (server tự ghi giá trị chọn sẵn).
- Khai báo sản lượng: BE tự thêm dòng 0 cho tài sản không gửi lên (suy từ SCR).
- B7 lọc theo ngày chứng từ (FE cũ lọc ngày hạch toán).
- Mặc định 10/trang giữ theo epic/Figma: Nhập kho thành phẩm, panel chọn chứng từ gốc CPTT.
- Hiển thị: ô Đơn vị tiếp nhận (điều chuyển TSCĐ) chỉ hiện mã; cột Đơn vị (người dùng/vai trò) chỉ hiện tên.

## Hợp đồng API đổi (FE trong repo đã sửa theo)

Nhiều endpoint đổi `ApiResponse<List>` → `PageResponse` (thêm `page`/`pageSize`, có trần 200), bỏ tham số `gioiHan`. Route bị **gỡ**: `GET /api/gia-thanh/cau-hinh-gia-thanh/tai-khoan`, `GET /api/chi-phi-tra-truoc/khai-bao/tai-khoan` (thay bằng `/tai-khoan/trang`). Trường bị bỏ: `khachHang`/`nhaCungCap` trong `…/doi-tru-chung-tu/lookups`. Chữ ký Java đổi: `*LookupPort.danhSachChon(...)` (kho), `NguonThamChieuPort.dem(...)` mới, `TieuChiNguon` bỏ `gioiHan`. Chi tiết từng endpoint xem báo cáo từng cụm (lịch sử phiên làm việc).

## Bug ngoài phạm vi phát hiện (chưa sửa)

- `BieuMauProxyController` tắt `@PreAuthorize` từ 2026-09-09 → `/api/bieu-mau/**` không kiểm quyền.
- Nguồn "Hóa đơn điều chỉnh" của Trả lại hàng bán luôn rỗng (`doiSang` lấy trị tuyệt đối, bộ lọc giữ `thanhTien < 0`).
- `HoaDonBanHangBanRaBangKeRepository.map()` đọc `c[9]` thay vì `c[10]` → `trangThaiHoaDon` luôn `DIEU_CHINH`.
- GET `/phan-bo-chi-phi/danh-sach` ghi DB.
- super-admin gọi `/internal/identity/users/search` không tồn tại trong `identity`.
- Audit log `/export` chỉ xuất tối đa 200 dòng.
