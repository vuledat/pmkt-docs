# 01 — Danh sách Chứng từ bán hàng

## 1. Header

- **Mã màn**: SCR_CTBH_DanhSach
- **SCR nguồn**: `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_DanhSach.md`
- **UC nguồn**: UC_CTBH_DanhSach, UC_CTBH_GhiSo (luồng hàng loạt), UC_CTBH_BoGhiSo (luồng hàng loạt)
- **Node Figma**: `node-id=58263-112028`
- **Route**: `client/src/features/banHang/routes.tsx` → tab "Chứng từ bán hàng" của màn Bán hàng
- **File chính**: `client/src/features/banHang/chungTuBanHang/components/ChungTuBanHangTab.tsx` (khung do `@domain-kit/chungTu` dựng qua `chungTuBanHangModule.Page`, xem `api/chungTuModule.tsx`)

## 2. Bố cục

Header (tìm kiếm, dropdown Thêm mới, nút Làm mới/Xóa lọc) → lưới danh sách (14 cột + Chức năng) → dòng tổng → khu vực chi tiết dưới lưới (BR08, panel "Xem nhanh" 4 tab). Không có Figma riêng cho khu vực chi tiết dưới lưới trong tài liệu — suy ra từ SCR.

## 3. Đặc tả UI từ Figma

Không đo lại — màn đã build đúng khung Figma node trên, không có thay đổi UI từ 2 commit BA mới (chỉ đổi luật ẩn/hiện nút, không đổi layout).

## 4. Ma trận ẩn/hiện · required · disabled

Không có file Matrix riêng cho DanhSach. BR04 của SCR đóng vai trò ma trận nút:

| Nút | Điều kiện hiện | Trạng thái code |
|---|---|---|
| Xem | có quyền `viewDetail` | ✅ đúng — `components/ChungTuBanHangTab.tsx:50` |
| Sửa | `trangThaiChungTu = CHUA_GHI_SO` AND quyền `edit` | ✅ đúng — kernel dùng `trangThai.chuaGhiSo` |
| Bỏ ghi sổ | `trangThaiChungTu = DA_GHI_SO` AND quyền `boGhiSo` | ✅ đúng — kernel dùng `trangThai.daGhiSo` |
| Ghi sổ | `trangThaiChungTu = CHUA_GHI_SO` AND quyền `ghiSo` | ✅ đúng |
| Xóa | `trangThaiChungTu = CHUA_GHI_SO` AND quyền `delete`; nếu đã dùng nghiệp vụ khác vẫn hiện, báo lỗi khi click (MSG_111) | ✅ đúng qua kernel (D6) |
| Thu tiền | `trangThaiThanhToan ∈ {Chưa thanh toán, Đã thanh toán một phần}` AND `trangThaiChungTu = DA_GHI_SO` AND quyền | ⚠️ hiện theo quyền, chưa lọc theo 2 trạng thái — **NGOÀI phạm vi D4** (toast "đang phát triển", chưa nối màn đích, không sửa điều kiện hiện tới khi màn đích có) |
| **Lập hóa đơn** | `trangThaiLapHoaDon ∈ {Chưa lập, Đã lập một phần}` AND quyền — **không phụ thuộc ghi sổ** | ❌ **F7 — chỉ lọc theo quyền, D4 sẽ sửa** |
| **Lập phiếu xuất kho** | `trangThaiXuatHang ∈ {Chưa xuất hàng, Đã xuất một phần}` AND quyền AND `loaiNghiepVu ≠ Bán dịch vụ` — không phụ thuộc ghi sổ | ❌ **F8 — chưa có nút, D4 sẽ thêm mới** |
| Ghi sổ hàng loạt | có ≥1 chứng từ "Chưa ghi sổ" trong dòng đã chọn AND quyền | ✅ đúng qua kernel bulk |
| Bỏ ghi sổ hàng loạt | có ≥1 chứng từ "Đã ghi sổ" trong dòng đã chọn AND quyền | ✅ đúng qua kernel bulk |
| Xóa hàng loạt | ≥1 dòng đã chọn AND quyền, **không** disable theo trạng thái dòng | ✅ đúng qua kernel bulk `XOA` |

## 5. Bảng cột / trường

| Tên hiển thị | Khoá i18n | Field API | Kiểu | Sort | Trạng thái code |
|---|---|---|---|---|---|
| Ngày hạch toán | `list.col.ngayHachToan` | `ngayHachToan` | date | server | ✅ `fields/columns.ts:56` |
| Ngày chứng từ | `list.col.ngayChungTu` | `ngayChungTu` | date | server | ✅ `fields/columns.ts:57` |
| Số chứng từ | `list.col.soChungTu` | `soChungTu` | link | server | ✅ `fields/columns.ts:58-67` |
| **Số hóa đơn** | — | `sal_hoa_don_ban_hang.SoHoaDon` (join) | text | N | ❌ **F9 — thiếu, chặn bởi BE** (`fields/columns.ts:10-14`, comment tự nhận gap) |
| Khách hàng | `list.col.khachHang` | `tenKhachHang` | text | N | ✅ `fields/columns.ts:68` |
| Thành tiền | `list.col.thanhTien` | `tongTienHangHoaQuyDoi` | currency | N | ✅ `fields/columns.ts:70-75` |
| Tiền chiết khấu | `list.col.tienChietKhau` | `tongTienChietKhauQuyDoi` | currency | N | ✅ `fields/columns.ts:76-82` |
| Tiền thuế GTGT | `list.col.tienThueGTGT` | `tongTienThueGtgtQuyDoi` | currency | N | ✅ `fields/columns.ts:83-89` |
| Tổng tiền thanh toán | `list.col.tongTienThanhToan` | `tongTienThanhToanQuyDoi` | currency | N | ✅ `fields/columns.ts:90-96` |
| Trạng thái lập hóa đơn | `list.col.trangThaiHoaDon` | `trangThaiHoaDon` | status | N | ✅ `fields/columns.ts:97` |
| Trạng thái thanh toán | `list.col.trangThaiThanhToan` | `trangThaiThanhToan` | status | N | ✅ `fields/columns.ts:98` |
| Trạng thái xuất hàng | `list.col.trangThaiXuatHang` | `trangThaiXuatHang` | status | N | ✅ `fields/columns.ts:99` |
| Trạng thái chứng từ | `list.col.trangThaiChungTu` | `trangThaiChungTu` | status | N | ✅ (xem F6 — tên field) `fields/columns.ts:100` |

Dòng tổng: `Tổng tiền chiết khấu · Tổng tiền thuế GTGT · Tổng thanh toán` — ✅ đã dựng qua `summary` (`fields/columns.ts:39-46`).

## 6. Hành vi & sự kiện

- **D4a — Lập hóa đơn**: sửa `visible` của mục `lapHoaDon` trong `rowActionsThem` (`components/ChungTuBanHangTab.tsx:85-90`) thành hàm nhận `row: ChungTuBanHangRow`, trả `canLapHoaDon && TRANG_THAI_HOA_DON_CHUA_DU.includes(row.trangThaiHoaDon)`. Cần kiểm tra kiểu `ChungTuRowActionThem.visible` của `@domain-kit` có nhận callback theo dòng hay chỉ boolean tĩnh — nếu chỉ boolean tĩnh, việc này phải nâng lên `@domain-kit/chungTu` (báo lại BA/dev nếu vậy, KHÔNG tự nới rộng scope engine).
- **D4b — Lập phiếu xuất kho**: thêm hằng `lapPhieuXuat: 'lapPhieuXuat'` vào `ROW_ACTION_THEM`, thêm phần tử vào `rowActionsThem` với `visible` theo `trangThaiXuatHang` + `loaiNghiepVu !== LOAI_NGHIEP_VU.banDichVu`, `onRowActionThem` giữ hành vi "đang phát triển" (toast) cho tới khi màn Tạo phiếu xuất kho tự động điền có thật.
- Các hành vi còn lại (Ghi sổ/Bỏ ghi sổ đơn lẻ + hàng loạt, Xóa, Sửa, Xem) — không đổi, do kernel xử lý.

## 7. Validation phía FE

Không có validate riêng ở màn danh sách — mọi điều kiện chặn (ghi sổ chứng từ đã ghi sổ, xóa chứng từ đã dùng nghiệp vụ khác…) là BE-side, hiển thị qua `apiError.ts` (D3).

## 8. Luồng xử lý

Không đổi — kernel `@domain-kit/chungTu` xử lý toàn bộ (search/sort/filter server-side, bulk actions, confirm+toast+invalidate). Chỉ thêm điều kiện `visible` tĩnh cho 2 nút D4a/D4b, không thêm request mới.

## 9. Phân bổ file

| Việc | File |
|---|---|
| D4a, D4b — điều kiện `visible` | `components/ChungTuBanHangTab.tsx` |
| D4b — hằng số hành động mới | `components/ChungTuBanHangTab.tsx` (`ROW_ACTION_THEM`) |
| D4b — mã quyền (chờ Q3) | `constants/permissions.ts` |
| D4a/D4b — nhãn nút mới | `i18n/vi.ts`, `i18n/en.ts` (`list.rowAction.lapPhieuXuat`) |

## 10. Kiểm thử

| Case | Input → kỳ vọng | Loại |
|---|---|---|
| Lập hóa đơn ẩn khi Đã lập đủ | `row.trangThaiHoaDon = 'Đã lập đủ'` → nút không hiện trong `rowActionsThem` | `*.test.ts`, `node` — logic thuần nếu tách hàm điều kiện ra `helpers/` |
| Lập hóa đơn hiện khi Đã lập một phần | `row.trangThaiHoaDon = 'Đã lập một phần'` AND quyền → hiện | idem |
| Lập phiếu xuất ẩn với Bán dịch vụ | `loaiNghiepVu = 'Bán dịch vụ'`, `trangThaiXuatHang = 'Chưa xuất hàng'` → ẩn | idem |
| Lập phiếu xuất hiện với Bán hàng trong nước chưa xuất đủ | `loaiNghiepVu = 'Bán hàng trong nước'`, `trangThaiXuatHang = 'Đã xuất một phần'` AND quyền → hiện | idem |

Khuyến nghị: tách điều kiện `visible` của 2 nút này thành hàm thuần trong `helpers/trangThai.ts` (cạnh `coTheGhiSo`/`coTheBoGhiSo`) để test được bằng `node`, không cần `render()`.

## 11. BR đã áp dụng

`BR01` (nguồn dữ liệu, không đổi) · `BR02` (lọc mặc định, không đổi) · `BR03` (hiển thị trạng thái, không đổi) · `BR04` (ẩn/hiện nút — **D4 sửa 2 dòng "Lập hóa đơn"/"Lập phiếu xuất"**) · `BR05` (dòng tổng, không đổi) · `BR07` (trạng thái lập hóa đơn theo counter, không phụ thuộc ghi sổ — nguồn của D4a) · `BR08` (khu vực chi tiết, không đổi) · `BR23` (nguồn của điều kiện D4b).

**BR chưa đạt**: `BR01` cột "Số hóa đơn" (F9, chặn BE).
