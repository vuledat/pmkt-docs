# 01 — Danh sách Hóa đơn bán hàng

## 1. Header

- **Mã màn:** `SCR_HDBanHang_DanhSach`
- **`SCR_*` nguồn:** `pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/5.screens/SCR_HDBanHang_DanhSach.md`
- **UC nguồn:** `4.usecases/PMKT-u-06456_DanhSach/UC_HDBanHang_DanhSach.md`
- **Node Figma:** `58263:162967`
- **Route:** `/ban-hang/hoa-don-ban-hang` (`constants/paths.ts:19-21`, gom về
  `banHang/_shared/constants/banHangTabs.ts`)
- **Component:** `components/HoaDonBanHangTab.tsx` (state) + `HoaDonBanHangListTable.tsx` (trình bày)
  + `HoaDonBanHangQuickDetail.tsx` (panel Xem nhanh)
- **Trạng thái code:** ĐÃ CÓ, khớp Matrix `_scope.md` (SKIP — không phải form nên không có ma trận
  Ẩn/Hiện riêng).

## 2. Bố cục

Bốn khối, trên xuống dưới:

1. **Toolbar** — Thêm mới · Tìm kiếm · Xóa bộ lọc · Làm mới · phễu ngày · lọc nâng cao · chip lọc.
2. **Bảng chính** — 7 cột dữ liệu + cột Chức năng ghim phải (BR01), chọn hàng loạt (checkbox đầu
   dòng), dòng tổng (BR31).
3. **Nút hàng loạt** — hiện khi có dòng được tick: Xóa hàng loạt (BR45), Lập chứng từ bán hàng/dịch vụ
   (BR04/BR05) — theo `SCR_HDBanHang_DanhSach.md §Chức năng`.
4. **Khu vực chi tiết dưới lưới (BR09)** — panel "Xem nhanh", tách khỏi tick-chọn, theo tiêu điểm dòng
   (focus row) chứ không theo checkbox — dựng ở `HoaDonBanHangQuickDetail.tsx`, chỉ đưa xuống ĐÚNG MỘT
   section "Bảng chi tiết hàng hóa" ở chế độ readonly, có nhãn liên kết + phân trang riêng.

## 3. Đặc tả UI từ Figma

| Thành phần | Component `@base` | Kích thước/spacing | Ghi chú |
| :-- | :-- | :-- | :-- |
| Bảng + toolbar + chip lọc + dòng tổng + chọn hàng loạt | `CommonListTable` (`src/base/index.ts:310`) | theo khung Figma node 58263:162967 | width từng cột lấy trực tiếp từ frame (`fields/columns.ts:58-134`) |
| Phễu ngày + lọc nâng cao | `useListFilter` · `CommonFilterPanel` (`:501`, `:476`) | — | lọc theo Ngày hóa đơn (BR8) |
| Panel Xem nhanh (tay nắm thu/mở) | markup cục bộ trong `HoaDonBanHangQuickDetail.tsx` | 76×20 viên thuốc vắt mép thẻ | **Viết mới có lý do**: không component `@base` nào vẽ hình dạng này; `IconButton` là ô vuông 32×32 có viền, khác hẳn — đã kiểm `@base` trước khi viết mới |
| Cột "Số hóa đơn" | `format: 'link'`, `textMode: 'identity'` (BR44 — không cắt định danh) | width 116 | mở popup Xem chi tiết |
| Thẻ trạng thái Lập chứng từ / Phát hành | `format: 'status'` qua `hoaDonStatusRegistry` (`fields/status.ts:27-53`) | width 170/205 | tone gold/blue/green theo BR02, BR03 |
| Cột "Trạng thái hóa đơn" | TEXT TRẦN (không thẻ màu — Figma vẽ khác 2 cột trên) | width 130 | BR06, `fields/columns.ts:92-107` |

Không có link Figma riêng cho khu vực Xem nhanh trong PYC — layout suy từ node danh sách chung
(58263:162967) + mô tả BR09 của `SCR_HDBanHang_DanhSach.md`.

## 4. Ma trận ẩn/hiện · required · disabled

`_scope.md` xếp `SCR_HDBanHang_DanhSach` vào nhóm **SKIP** — không phải form, không có ma trận
Ẩn/Hiện/Disable dạng cột theo trục input (đúng theo A5 trong `docs/fe-khung-kien-truc-chuan.md`).
Điều kiện hiện/ẩn của màn này nằm ở **cấp NÚT**, dịch từ `SCR_HDBanHang_DanhSach.md §Chức năng` +
`§Rule`:

| Thành phần | Điều kiện hiện | Điều kiện disable | Nguồn |
| :-- | :-- | :-- | :-- |
| Icon Xem chi tiết | có quyền `LapHoaDonBan.View.Detail` | — | BR01 |
| Icon Chỉnh sửa | có quyền `LapHoaDonBan.Edit` **và** trạng thái = "Chưa phát hành" | — | BR01 |
| Icon Xóa | có quyền `LapHoaDonBan.Delete` **và** trạng thái = "Chưa phát hành" | — | BR01 |
| Nút "Xóa hàng loạt" | ≥1 dòng được tick | disable nếu ≥1 hóa đơn đã phát hành **hoặc** trạng thái lập chứng từ ≠ "Chưa lập" | §Chức năng dòng 48 (⚠ xem mâu thuẫn nội bộ ở §7 dưới) |
| Nút "Lập chứng từ bán hàng" | trạng thái lập chứng từ ∈ {"Chưa lập", "Đã lập 1 phần"} | — | BR04 |
| Nút "Lập chứng từ bán dịch vụ" | như trên **và** có ≥1 dòng hàng "Dịch vụ" | — | BR05 |
| Khu vực chi tiết (Xem nhanh) | có quyền `LapHoaDonBan.View.Detail` | — | BR09 — không có quyền thì **ẩn toàn bộ khu vực**, không chỉ ẩn nội dung; server kiểm quyền trước khi trả data |

⚠ **Mâu thuẫn nội bộ tài liệu (đã ghi ở `IMPLEMENT.md §4.2 #7`, vẫn còn nguyên sau khi rà lại):**
`§Chức năng` nói nút "Xóa hàng loạt" **disable** nếu có ≥1 hóa đơn đã phát hành; nhưng
`SCR_HDBanHang_Xoa.md` BR7 nói hệ thống **chỉ xóa** hóa đơn "Chưa phát hành", hóa đơn "Đã phát hành"
**được liệt kê trong popup kết quả** (nghĩa là nút vẫn bấm được, server tự lọc). Code đã chọn
**BR7 + BR45 §2** (cho chạy rồi báo cáo) — xem file `03-popup-xoa.md`. Giữ nguyên lựa chọn này, đã
báo BA ở lần code trước, chưa có phản hồi mới.

## 5. Bảng cột / trường

| Tên hiển thị | Khoá i18n | Field API | Kiểu | Định dạng | Rộng | Sort | Lọc | Mặc định ẩn/hiện |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Ngày hóa đơn | `list.col.ngayHoaDon` | `ngayHoaDon` | date | `format: 'date'` | 110 | server | keyword | hiện |
| Số hóa đơn | `list.col.soHoaDon` | `soHoaDon` | string | link, `textMode: 'identity'` (BR44) | 116 | server | keyword | hiện |
| Tên khách hàng | `list.col.tenKhachHang` | `tenKhachHang` | string | `textMode: 'long'` (BR44) | 140 | server | keyword | hiện |
| Trạng thái lập chứng từ | `list.col.trangThaiLapChungTu` | `trangThaiLapChungTu` | enum | `format: 'status'` | 170 | server | eq | hiện |
| Trạng thái phát hành HĐ | `list.col.trangThaiPhatHanhHoaDon` | `trangThaiPhatHanhHoaDon` | enum | `format: 'status'` | 205 | server | eq | hiện |
| Tiền thuế GTGT | `list.col.tienThueGtgt` | `tongTienThueGtgtQuyDoi` | number | `format: 'currency'` (BR7), có `summary` (BR31) | 126 | — (BA đánh N) | — | hiện |
| Trạng thái hóa đơn | `list.col.trangThaiHoaDon` | `trangThaiHoaDon` | enum (text trần) | hàm dịch nhãn qua `nhanTrangThaiHoaDon` | 130 | server | eq | hiện |
| Hóa đơn liên quan | `list.col.hoaDonLienQuan` | `hoaDonLienQuan[]` | mảng quan hệ | join bằng dấu phẩy — **nợ N5**: chưa bấm được (BR07 đòi mỗi số là 1 link) | 150 | — (BA đánh N) | keyword | hiện |

Field `ngayHoaDon` cũng là cột mặc định sắp xếp + phễu ngày (`DEFAULT_SORT`,
`hoaDonBanHangApi.ts:51`, `DATE_FILTER_FIELD`, `:71`).

## 6. Hành vi & sự kiện

| Thao tác | Điều kiện hiện | Điều kiện disable | Việc làm | Confirm | Toast | Invalidate |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Thêm mới | quyền `Create` | — | mở `HoaDonBanHangThemMoiModal` mode `create` | — | thành công → MSG_001 | query list |
| Tìm kiếm | luôn | — | gọi `toSearchRequest` → `POST /tim-kiem` | — | — | — |
| Xóa bộ lọc | luôn | — | reset `useListFilter` | — | — | query list |
| Làm mới | luôn | — | refetch, giữ bộ lọc | — | — | query list |
| Click "Số hóa đơn" | luôn | — | `onOpen` → mở popup Xem chi tiết | — | — | — |
| Icon Sửa | quyền + trạng thái Chưa phát hành | — | mở popup mode `edit`; nếu HĐ đã lập chứng từ → cảnh báo MSG_056 trước (BR02 của CapNhat) | Yes/No | thành công → MSG_002 | query list + detail |
| Icon Xóa | quyền + trạng thái Chưa phát hành | — | mở `03-popup-xoa.md` | Yes/No, đổi câu nếu đã lập chứng từ (BR10) | MSG_003 / MSG_010 | query list |
| Xóa hàng loạt | ≥1 dòng tick | theo §4 (đang mâu thuẫn nội bộ, đã chọn BR7) | `xoaHoaDonHangLoat` → luôn mở popup Kết quả (BR8) | MSG_027/MSG_055 tuỳ dòng | MSG_054 | query list, đóng popup mới reload (BR9) |
| Lập chứng từ bán hàng | BR04 | — | mở màn Thêm mới CTBH kèm auto-fill | — | — | ⚠ hiện báo "đang phát triển" — leaf anh em, xem §9 |
| Lập chứng từ bán dịch vụ | BR05 | — | mở màn Thêm mới CTBDV | — | — | ⚠ như trên, module CTBDV còn chưa tồn tại ở `features/` |
| Đổi dòng focus (Xem nhanh) | luôn | — | nạp lại panel theo tiêu điểm dòng, KHÔNG theo checkbox (BR09) | — | — | query detail-quick |

## 7. Validation phía FE

Màn danh sách không có validate nhập liệu — chỉ có điều kiện hiện/disable ở §4 và điều kiện lọc dữ
liệu server-side (BR11: search/filter/sort đều đi qua `toSearchRequest`, không tự lọc phía client).

## 8. Luồng xử lý

1. Mount `HoaDonBanHangPage` → `HoaDonBanHangTab` → gọi `createSearchQueries` (theo tenant) với
   `toSearchRequest(params)` mặc định (không filter, sort = `ngayHoaDon:desc,soHoaDon:asc`).
2. Loading → skeleton của `CommonListTable`; Error → banner lỗi chuẩn của `@base`; Empty → trạng thái
   rỗng chuẩn.
3. Chọn dòng / gõ tìm kiếm / đổi phễu ngày / đổi trang → build lại `SearchRequest`, refetch.
4. Focus dòng (mount lần đầu = dòng 1) → gọi `GET /{id}` cho panel Xem nhanh (BR09), độc lập phân
   trang với lưới chính.
5. Bấm nút hành động → theo bảng §6.

## 9. Phân bổ file

| Việc | File |
| :-- | :-- |
| State: query, lọc, chọn, 3 luồng xóa/sửa | `components/HoaDonBanHangTab.tsx` |
| Trình bày bảng | `components/HoaDonBanHangListTable.tsx` |
| Panel Xem nhanh | `components/HoaDonBanHangQuickDetail.tsx` |
| Cột bảng | `fields/columns.ts` |
| Cột panel Xem nhanh | `fields/chiTietColumns.ts` |
| Registry màu trạng thái | `fields/status.ts` |
| Nhãn "Hóa đơn gốc/…" (BR06) | `fields/texts.ts` (`nhanTrangThaiHoaDon`) |
| Máy trạng thái nút (BR01) | `helpers/trangThai.ts` (`coTheSua`/`coTheXoa`) |
| Query wire | `api/hoaDonBanHangApi.ts`, `api/queries.ts`, `api/model.ts` |
| Xóa hàng loạt | `api/hoaDonBanHangApi.ts:140-147` (`xoaHoaDonHangLoat`) |

## 10. Kiểm thử

Đã có (12/08), giữ nguyên — không cần viết thêm cho lần rà soát này:

| Case | Loại | File |
| :-- | :-- | :-- |
| `toSearchRequest` — build filter/sort/keyword đúng hợp đồng wire | logic thuần (`node`) | `test/payload.test.ts`* |
| `coTheSua`/`coTheXoa` theo trạng thái | logic thuần (`node`) | `test/kiemTra.test.ts` |
| Render bảng, panel Xem nhanh, điều hướng route | DOM | `test/hoaDonBanHang.render.test.tsx` |
| Cân bằng khoá i18n vi/en | logic thuần (`node`) | `test/i18n.test.ts` |

\* `toSearchRequest` hiện được test lẫn trong `payload.test.ts` — nếu tách riêng thì theo đúng luật
"file mới đặt đâu" của §5 `client/CLAUDE.md`, không bắt buộc phải tách trong phạm vi PYC này.

## 11. BR đã áp dụng

BR1 (phân trang) · BR2 (hiển thị & sắp xếp) · BR7 (precision tiền tệ) · BR8 (phễu ngày) · BR11 (tìm
kiếm/lọc/sắp xếp) · BR13.1 (nút thao tác) · BR30 (ẩn/hiện cột — qua `showSettings`) · BR31 (dòng
tổng) · BR44 (truncate — `textMode`) · BR45 (thao tác hàng loạt) của Common; BR01-BR09 riêng của
`SCR_HDBanHang_DanhSach`. Chi tiết áp dụng ở đâu: xem `00-ke-hoach-tong.md §14` (không lặp lại).
