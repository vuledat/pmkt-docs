# IMPLEMENT — PMKT-E-06469 Trả lại hàng bán (FE)

## 1. Ngày · phạm vi đã code

**2026-08-12** — code THẲNG từ PYC `pmkt-docs/ba/PMKT-E-06469_TraLaiHangBan/` (user chọn bỏ bước
`/plan-fe`; vì vậy §1 + §2 của `/plan-fe` — đọc bắt buộc và khảo sát reuse có bằng chứng — được làm
đầy đủ và ghi ở §3 dưới đây).

Đã code:

| Màn / use case | Trạng thái |
| --- | --- |
| SCR_DanhSachTraLaiHangBan (U-06470 Xem danh sách) | ✅ đủ |
| SCR_ThemMoiTraLaiHangBan (U-06471 Thêm mới) | ✅ đủ khung + luật; phần chọn nguồn chờ API (§5) |
| SCR_SuaTraLaiHangBan (U-06472 Sửa) | ✅ đủ (dùng chung popup, khóa Số/Ngày chứng từ) |
| U-06473 Xóa | ✅ đủ (hộp xác nhận MSG_212 / BR19 bộ chứng từ) |
| U-06474 Nhân bản | ✅ đủ (`toFormValuesNhanBan`) |
| U-06475 Ghi sổ · U-06476 Bỏ ghi sổ (một chứng từ) | ✅ đủ (hộp xác nhận MSG_207) |
| SCR_XemChiTietTraLaiHangBan (U-06477) | ✅ đủ (chế độ `view`, khóa toàn bộ ô nhập) |
| BR14 · BR15 · BR16 — ghi sổ / bỏ ghi sổ / xóa **HÀNG LOẠT** | ⚠ mới lọc điều kiện, chưa chạy (§5) |

## 2. Danh sách file đã tạo / sửa

### Tạo mới — `client/src/features/banHang/traLaiHangBan/` (51 file · ~10.900 dòng)

| File | Vai trò |
| --- | --- |
| `index.ts` | Cửa ra duy nhất của module (file DUY NHẤT ở gốc) |
| `api/model.ts` | Hợp đồng wire Zod của `ChungTuTraLaiHangBan` + chi tiết + dòng tổng |
| `api/traLaiHangBanApi.ts` | Adapter BASE CRUD + `toSearchRequest` + ghi sổ/bỏ ghi sổ + tra nhanh chứng từ nguồn |
| `api/mock.ts` | **NỢ** — adapter giả trong bộ nhớ, thay cho module BE chưa có |
| `api/queries.ts` | Hook react-query có phạm vi tenant |
| `api/lookups.ts` | Danh mục thật (`/api/master-data/*`) cho mọi select của popup |
| `api/payload.ts` | Form store → thân request (gộp tab về header phẳng, loại dòng trắng) |
| `api/formDetail.ts` | Chiều ngược: wire → form store; kèm biến thể **Nhân bản** |
| `constants/constants.ts` | Enum wire · nhãn cột · khóa tab · hình học · `MAX_LEN` |
| `constants/paths.ts` | Re-export path từ `banHang/_shared/constants/banHangTabs.ts` |
| `constants/permissions.ts` | Mã quyền `TraLaiHangBan.*` (BR25) |
| `fields/types.ts` | Hình dạng form store + `NguCanhAnHien` (bản dựng sẵn của ma trận) |
| `fields/columns.ts` | 8 cột màn danh sách |
| `fields/chiTietFields.ts` | ~30 cột lưới chi tiết + cascade tính lại |
| `fields/nguonColumns.ts` | Cột của hai popup chọn nguồn |
| `fields/tabColumns.ts` | Cột tab Thuế · tab Hạch toán |
| `fields/options.ts` · `fields/status.ts` · `fields/texts.ts` | Option enum · registry trạng thái · bundle chữ cho `@base` |
| `helpers/trangThai.ts` | Giá trị wire trạng thái + BR11/BR12/BR13 |
| `helpers/tinhToan.ts` | Số học một dòng (thành tiền · thuế · giá vốn · quy đổi) |
| `helpers/tongHop.ts` | Khối tổng + tab Thuế + **bút toán tự sinh** (3 bước của SCR) |
| `helpers/anHien.ts` | Bản CODE của ma trận ẩn/hiện (4 cột × 8 điều kiện + mức dòng) |
| `helpers/nguon.ts` | **BR1 · BR2 · BR5** — nạp/sắp/validate popup nguồn, đổ dòng sang lưới |
| `helpers/kiemTra.ts` | Kiểm tra trước khi lưu (MSG_104…MSG_112 + BR4) |
| `helpers/dongBo.ts` | Luật liên trường thuần (diễn giải · đồng bộ nhóm · kế thừa · hình thức TT) |
| `hooks/useDanhMucTraLai.ts` | Gom mọi danh mục + hệ số quy đổi + TK ngầm định theo tiền tố |
| `hooks/useDongBoTab.ts` | Nối luật liên trường vào form thật |
| `components/TraLaiHangBanTab.tsx` | State của màn danh sách + 3 luồng vòng đời |
| `components/TraLaiHangBanListTable.tsx` | Bảng danh sách (trình bày) |
| `components/TraLaiHangBanThemMoiModal.tsx` | KHUNG popup Thêm/Sửa/Xem/Nhân bản: form instance · nạp chứng từ · header/footer · lưu · 2 popup nguồn |
| `components/ThanThemMoi.tsx` | THÂN popup: hàng tùy chọn · thẻ "Nhập" · lưới · dải tổng. Tách ra vì mọi `Form.useWatch` phải chạy ở component CON của `<Form>` — xem §4 L10 |
| `components/GhiGiamCongNoTab.tsx` · `PhieuNhapKhoTab.tsx` · `ChiTienTab.tsx` · `HoaDonTab.tsx` | Thân 4 nhóm tab |
| `components/ChonChungTuNguonModal.tsx` · `ChonHoaDonDieuChinhModal.tsx` | Hai popup chọn nguồn |
| `components/GridHeaderActions.tsx` · `TongHopPanel.tsx` | Góc phải thanh tab lưới · khối Tổng cộng |
| `i18n/vi.ts` · `i18n/en.ts` · `i18n/registerTraLaiHangBanI18n.ts` | MỘT namespace `traLaiHangBan` |
| `test/i18n.test.ts` | **Chốt chặn khóa i18n dựng ĐỘNG** — xem §4 L8 |
| `pages/TraLaiHangBanPage.tsx` · `pages/traLaiHangBan.css` | Entry lazy + stylesheet của màn |
| `test/themMoiModal.render.test.tsx` | **Ghim cấu trúc popup theo Figma 15756:47126** — thứ tự tab · thứ tự cột lưới · cột ẩn (§4 L10) |
| `test/*` (7 file · 105 case) | api · nguồn · tính toán+ẩn hiện · payload · render danh sách · i18n · render popup |

### Sửa file có sẵn (3 file, diff nhỏ)

| File | Sửa gì |
| --- | --- |
| `features/banHang/_shared/constants/banHangTabs.ts` | Thêm `traLaiHangBan → /ban-hang/tra-lai-hang-ban` vào `BAN_HANG_TAB_PATHS` + cập nhật ghi chú |
| `features/banHang/routes.tsx` | Thêm route `traLaiHangBan` (lazy) |
| — | `app/router/RootRoutes.tsx` **không phải sửa**: `gateByHandle(banHangRoutes)` đã có sẵn |

## 3. Đã reuse gì (khảo sát có bằng chứng)

Mẫu tham chiếu đọc TRƯỚC khi code: `client/src/features/banHang/chungTuBanHang/` (toàn bộ 20 file
nguồn) + `hoaDonBanHang/pages/HoaDonBanHangPage.tsx` + `_shared/constants/banHangTabs.ts`.

**Component `@base` dùng lại — không tự viết cái nào:**

| Component | Dùng ở |
| --- | --- |
| `CommonListTable` | danh sách · tab Thuế · tab Hạch toán · 2 lưới popup nguồn |
| `CommonEditableGrid` | lưới chi tiết hàng hóa |
| `CommonModalShell` | popup Thêm/Sửa/Xem + 2 popup nguồn |
| `CommonConfirmModal` | xóa · ghi sổ · bỏ ghi sổ · xác nhận kế thừa |
| `HeaderControls` | cụm "Chọn chứng từ" trên thanh tiêu đề (3 nguồn của Figma) |
| `TabMenu2Level` · `TabMenuChild` | thanh 4 tab nhóm Bán hàng · tab trong popup |
| `useListFilter` · `CommonFilterPanel` | phễu ngày + lọc nâng cao + chip (BR11) |
| `RowActionButtons` · `CommonActionMenu` | con mắt + menu ⋮ |
| `TotalBreakdown` | khối Tổng cộng (chế độ 2 cột khi ngoại tệ) |
| `CommonSelectBox` · `CommonTextBox` · `CommonTextArea` · `CommonNumberInput` · `CommonDatePicker` · `CommonCheckbox` · `FieldLabel` · `CommonButton` · `Card` · `CommonEmpty` · `Tooltip` | mọi ô nhập/nhãn |
| `createSearchApi` · `createSearchQueries` (`@platform`) | toàn bộ vòng đời CRUD |
| `PERIOD_PRESET` · `formatNumber` (`@core`) | preset phễu ngày · định dạng số dòng tổng |

**Không có component nào phải tự viết mới ngoài component riêng của màn** (4 tab thân + 2 popup
nguồn + panel tổng + 2 bảng) — đó đều là UI mang nghiệp vụ của riêng màn này nên đúng chỗ ở
`<module>/components/`.

**Không thêm prop nào vào `@base`** trong lần này.

## 4. Lệch so với tài liệu / thiết kế

| # | Lệch gì | Vì sao | Ảnh hưởng |
| --- | --- | --- | --- |
| L1 | **Figma ↔ Ma trận — hai cột chiết khấu của lưới.** Figma (biến thể "Không chiết khấu") KHÔNG vẽ "Chiết khấu %" / "Tiền chiết khấu"; Ma trận ghi `Show` ở cả 4 cột tổ hợp. | Chọn theo **Ma trận** (nguồn sự thật cho behavior): cột luôn hiển thị, chỉ **khóa ô** khi Loại chiết khấu = "Không chiết khấu" — cùng quy ước với `chungTuBanHang`. | Cần BA/Design chốt: ẩn cột hay khóa ô. `helpers/anHien.khoaOChietKhauDong` là chỗ duy nhất phải sửa. |
| L2 | **Mã hàng trên lưới** — Ma trận ghi `Show`, BR5 ghi "Disable, không cho sửa" (Điểm cần xác nhận #2 của chính ma trận). | Code đọc HỢP NHẤT cả hai: lập TAY → sửa được; lập TỪ chứng từ nguồn → khóa (vẫn xóa được cả dòng, đúng ghi chú BR5). | Chờ BA chốt. `helpers/anHien.khoaMaHang`. |
| L3 | **"Tự động áp giá"** — Ma trận ghi `Disable` (bảng trường nói N), BR14 mô tả NSD tự tick (Điểm cần xác nhận #3). | Code theo **BR14** (cho tick), vì ô này là công tắc bật/tắt của chính BR14 — để `Disable` thì BR14 không còn nhánh nào chạy được. | Chờ BA chốt. `fields/chiTietFields.ts` cột `giaTrungBinh`. |
| L4 | **Cột "Chiết khấu thương mại"** — BR13 tham chiếu ô tick này nhưng bảng trường lưới KHÔNG có cột (Điểm cần xác nhận #4). | Đã dựng cột (BR13 cần nó mới diễn đạt được). | Nếu BA nói không có, xóa 1 cột + 2 predicate. |
| L5 | **Vị trí màn** — Figma vẽ "Trả lại hàng bán" là TAB của trang Chứng từ bán hàng. | Luật tầng cấm leaf import leaf anh em → mỗi tab là một route riêng. Đã dùng đúng cơ chế `_shared/constants/banHangTabs.ts` mà repo vừa dựng cho `hoaDonBanHang`: thanh tab vẫn đủ 4 mục, bấm tab khác là ĐIỀU HƯỚNG. | Không — người dùng thấy đúng như Figma. |
| L6 | **Nhãn quyền** — tài liệu ghi `PMKT.E06469.DanhSach` / `.ThemMoi`; code dùng `TraLaiHangBan.View` / `.Create`… | Mã backend thật là `MaChucNang.TRA_LAI_HANG_BAN` + hằng `QuyenChecker` — đó mới là chuỗi `useHasPermission` so sánh. | Nếu BA chốt bộ `PMKT.*`, sửa đúng `constants/permissions.ts`. |
| L9 | **Đã sửa LÂY sang 2 module anh em** — `dieuChinhGiaHangBan` và `hoaDonBanHang` dính đúng lỗi preset (camelCase thay vì UPPER_SNAKE). | Cùng một builder `t(\`…filter.presets.${id}\`)`, cùng một cách đặt tên sai. | Đã sửa `vi.ts`/`en.ts` của cả hai + thêm `test/i18n.test.ts` cho mỗi module (đã kiểm ngược). Không đụng file nào khác của hai module đó. ⚠ Hai module này đang được phiên khác dựng dở — báo lại để tránh sửa chồng. |
| L8 | **Đã sửa: khóa i18n dựng ĐỘNG bị trượt** — dropdown "Kỳ" và viên thuốc kỳ in ra `filter.presets.MONTH_TO_DATE`; toast của hai lỗi chiết khấu in ra `msg.phanTramCkVuot100`. | Khóa preset phải trùng NGUYÊN VĂN id `PERIOD_PRESET` (UPPER_SNAKE), tôi đặt camelCase; hai mã của `MA_LOI` thì nằm nhầm nhánh `themMoi.tb.*` thay vì `msg.*`. Không lỗi biên dịch/lint nào bắt được. | Đã sửa cả `vi.ts`/`en.ts` **và** thêm `test/i18n.test.ts` chặn cứng: đối chiếu mọi khóa động với chính hằng số sinh ra nó + khớp khóa `vi` ⇄ `en` 1-1. Đã kiểm ngược (đổi lại camelCase → test đỏ đúng chỗ). |
| L7 | **Enum wire chưa đối chiếu được với BE** (`PHUONG_THUC_LAP_HOA_DON`, `PHUONG_THUC_THANH_TOAN`, `LOAI_CHIET_KHAU`, `NGUON_CHUNG_TU`, `LOAI_DIEU_CHINH`). | cell-app chưa có module `tra_lai_hang_ban` nên không có `GiaTriDb` nào để đối chiếu; lấy NGUYÊN VĂN SCR. | Khi BE lên phải đối chiếu TRƯỚC — lệch một dấu là chứng từ chỉ hỏng lúc COMMIT. |
| L10 | **Đã sửa: popup Thêm mới bám lại Figma node 15756:47126** (user đối chiếu và báo lệch). | Bản dựng đầu bám node 15756:46675 — cùng màn nhưng khác biến thể. | Xem bảng "L10 — đã sửa gì" ngay dưới. |
| L11 | **"Loại tiền" ở góc phải thanh tab lưới — Figma KHÔNG vẽ**, chỉ có "Chiết khấu". | Cả hai node (46675 · 47126) đều là biến thể VND. Bỏ ô này thì `đk-QĐ`/BR18 mất công tắc: không còn cách chọn ngoại tệ nên tỷ giá + 4 cột quy đổi + 2 dòng tổng quy đổi thành code chết. | **Đang giữ ô Loại tiền**, chờ user/BA chốt. Bỏ = sửa `components/GridHeaderActions.tsx` + gỡ nhánh `ngoaiTe`. |

| L12 | **Đã bật panel "Chi tiết hàng hóa" dưới danh sách** (user báo thiếu so với ba màn chứng từ còn lại). | Descriptor từng khai `capabilities.listCon = false` với lý do "SCR không vẽ panel" — SCR thật sự chỉ tả bảng CHA, nhưng đây là bố cục chung của mọi màn chứng từ và bảng cha không mang dòng hàng, nên không có panel thì muốn xem trả lại những gì phải mở popup từng chứng từ. | Bỏ `capabilities`, khai `chiTietTabLabelKey`, thêm `fields/chiTietPanelColumns.ts` (11 cột) + `hooks/useNhanDongChiTiet.ts` (3 lookup, không phải 12 như popup) và tiêm `lineColumns` từ `TraLaiHangBanTab`. Ghim bằng 1 ca render đầu-cuối + 5 ca thuần. |

**L10 — đã sửa gì (theo Figma 15756:47126):**

| Chỗ | Trước | Sau |
| --- | --- | --- |
| Thứ tự tab thẻ "Nhập" | Ghi giảm công nợ · Phiếu nhập kho · chi tiền · Hóa đơn | Ghi giảm công nợ · **chi tiền** · Phiếu nhập kho · Hóa đơn |
| Hàng tùy chọn | có kẻ dọc ngăn nhóm | bốn ô tick/chọn chạy liền mạch, **không kẻ dọc** |
| Tab Ghi giảm công nợ · Phiếu nhập kho | "Mã số thuế" nằm cạnh Tên khách hàng | "Mã số thuế" xuống **cột trái** hàng 2; nhãn NV bán hàng đủ chữ |
| Tab Hóa đơn | bố cục riêng | dùng CHUNG `.pmkt-tlhb-tm-body` (lưới 2 cột · kẻ dọc · cột phải 300) + thanh chọn hóa đơn (ô chọn khóa + nút ≡🔍) + dải thông tin nền xanh |
| Mẫu số hóa đơn | ô nhập chữ | **select** (`useMauSoHoaDonLookup`) |
| Cột lưới | có "TK giá vốn" · "Chiết khấu thương mại" | ẩn hai cột Figma không vẽ; hai cột CK ẩn theo biến thể "Không chiết khấu" |

**Kèm theo L10 — một lớp lỗi của antd v6 đã ghim bằng test:** `Form.useWatch` bỏ qua lần đăng ký
đầu khi được gọi từ **chính component đang dựng `<Form>`** (`formInstance._init` còn false ở render
đó, cả hai effect của `useWatch` `return` sớm) — ma trận ẩn/hiện vì thế chỉ đúng từ lần re-render
sau. Đã tách toàn bộ khối watch xuống `components/ThanThemMoi.tsx` (con của `<Form>`) và cụm chọn
nguồn ở header xuống `ChonNguonHeader`. Ngoài ra `WatcherCenter` của antd v6 gom thông báo watch vào
**một macro task** (`MessageChannel`), nên test phải nhường một nhịp sau mỗi `fireEvent.click` —
`test/themMoiModal.render.test.tsx` có helper `tich()` làm đúng việc đó, kèm ghi chú.

## 5. Nợ kỹ thuật

| # | Nợ | Chi tiết |
| --- | --- | --- |
| N1 | **`api/mock.ts` — còn mock = còn nợ** | cell-app chưa có `/api/ban-hang/tra-lai-hang-ban`. Adapter thật đã dựng sẵn theo BASE CRUD v1; gỡ nợ = đối chiếu `api/model.ts`, đổi `DUNG_MOCK` → `false`, xóa `mock.ts`. |
| N2 | **Hai popup chọn nguồn chưa có dữ liệu** | Lưới cần endpoint tra DÒNG HÀNG của chứng từ nguồn (kèm SL đã trả lại) và DANH SÁCH HÓA ĐƠN; `/chung-tu-ban-hang/search` chỉ trả header. Hàm nạp được TIÊM qua props (`useNguonChuaCoApi`) nên nối API là sửa đúng một hook. Popup mở/lọc/validate được, hiện "Không tìm thấy dòng hàng nào". |
| N3 | **Thao tác HÀNG LOẠT (BR14 · BR15 · BR16)** | Mới lọc điều kiện + báo "không có gì để làm". Cả ba endpoint trả kết quả THÀNH CÔNG MỘT PHẦN nên cần popup "Danh sách không xử lý được" riêng — và BE chưa có endpoint nào. |
| N4 | **Tab "Đính kèm" · "Tham chiếu"** | Dùng đặc tả chung (`Common/NguonDuLieu`), chưa dựng — hiện `CommonEmpty` có chữ giải thích. |
| N5 | **Ba danh mục chưa có endpoint** | Vụ việc · Hợp đồng · Số phiếu xuất (BR15) — cột vẫn dựng theo Figma, danh sách rỗng. |
| N6 | **"Hình thức TT" của tab Hóa đơn chưa cho nhập tay** | SCR cho phép nhập giá trị ngoài 3 mục; `CommonSelectBox` chưa có chế độ free-text một-giá-trị. Cần thêm prop vào `@base` hoặc chốt bỏ yêu cầu. |
| N7 | **"Lập HĐ điều chỉnh" · "Lập phiếu nhập kho"** | Hai mục ⋮ rời sang module khác (hóa đơn điều chỉnh / kho) — cả hai chưa dựng; hiện báo "đang phát triển". Mã quyền của chúng là GIẢ ĐỊNH. |

## 6. Kết quả cổng nghiệm thu

### Lần 2 — chạy 2026-08-13 (sau L8 · L9 · L10)

| Lệnh | Kết quả | Đối chiếu baseline |
| --- | --- | --- |
| `npx tsc -p tsconfig.app.json --noEmit` | **172 lỗi**, **0 lỗi** trong `src/features/banHang/**` | Baseline tài liệu 194 → không xấu hơn (phiên khác đã dọn bớt) |
| `npm run lint` | **11 vấn đề (9 lỗi + 2 cảnh báo)**, tất cả ở `src/legacy/` | Baseline 12 → không xấu hơn |
| `npx eslint src/features/banHang/traLaiHangBan` | **sạch (exit 0)**, `--max-warnings=0` | — |
| `npm run lint:boundaries` | **76 lỗi** = 74 "rule not found" + 2 `axios` trần trong `legacy` | Đúng baseline; `npx eslint src/features/banHang --config eslint.boundaries.config.js` → **exit 0** |
| `npx vitest run src/features/banHang/{traLaiHangBan,dieuChinhGiaHangBan,hoaDonBanHang}` | **19 file · 323 case PASS** (riêng `traLaiHangBan`: 7 file · 105 case) | — |
| `npx vite build` | ✓ built in 1.05s | — |

⚠ **Chưa kiểm được bằng mắt trên trình duyệt**: dev server chạy được nhưng app chặn ở màn Đăng nhập
và tôi không nhập tài khoản của user. Bằng chứng thay thế là `test/themMoiModal.render.test.tsx` —
render THẬT popup rồi đọc DOM (thứ tự tab · thứ tự cột · cột ẩn).

### Lần 1 — chạy 2026-08-12

| Lệnh | Kết quả | Đối chiếu baseline |
| --- | --- | --- |
| `npm run typecheck` | **192 lỗi** — 129 `features/danhMuc` · 39 `muaHang` · 16 `tienMat` · 6 `base/domainKit` · 2 khác. **0 lỗi trong `traLaiHangBan/`, `banHang/routes.tsx`, `banHang/_shared/`** | Baseline tài liệu 193–194 → **không xấu hơn** |
| `npm run lint` | **12 vấn đề (10 lỗi + 2 cảnh báo)**, TẤT CẢ ở `src/legacy/` | Đúng baseline tài liệu |
| `npx eslint src/features/banHang/traLaiHangBan src/features/banHang/routes.tsx src/features/banHang/_shared` | **sạch (exit 0)** — không dùng `eslint-disable` nào | — |
| `npm run lint:boundaries` | **76 lỗi** = 74 "rule not found" + 2 `axios` trần trong `legacy` | Đúng baseline; `npx eslint src/features/banHang --config eslint.boundaries.config.js` → **exit 0** (không sinh vi phạm tầng mới) |
| `npx vitest run src/features/banHang/traLaiHangBan` | **6 file · 99 case PASS** (chạy lại 3 lần, ổn định) | — |
| `npx vitest run` (toàn bộ) | 438 file · **4090 pass / 8 fail** — 8 ca đỏ nằm ở `app/layouts` (2), `app/router` — nhánh muaHang (1), `base/components` (2), `legacy` (3). **Không ca nào thuộc `banHang`** | Đỏ sẵn / việc dở của phiên khác |
| `npm run build` | `tsc -b` đỏ theo baseline repo (không phải file của module này); **`npx vite build` ✓ built in 1.19s** — app đóng gói được kèm module mới | — |

**Chưa chạy `npm run check:committed`**: chưa commit gì (client/CLAUDE.md §14 — không tự commit).
`git status` còn `?? src/features/banHang/traLaiHangBan/`. Trước khi commit phải `git add` TOÀN BỘ
thư mục module TRƯỚC, rồi mới commit `banHang/routes.tsx` + `_shared/constants/banHangTabs.ts` —
ngược lại là đúng công thức sinh lỗi `[UNRESOLVED_IMPORT]` ở CI (client/CLAUDE.md §15.1).

## 7. BR đã áp dụng

**Common BR (`pmkt-docs/ba/Common/business_rules.md`)**

| BR | Áp ở đâu |
| --- | --- |
| BR1 phân trang | `DANH_SACH_PAGE_SIZE = 20`, phân trang server |
| BR2 hiển thị & sắp xếp | `fields/columns.ts`, `DEFAULT_SORT` (BR17 của SCR) |
| BR3 popup | `CommonModalShell` + hộp xác nhận bỏ dở |
| BR5 combogrid | `HeaderControls` + `CommonSelectBox showSearch` |
| BR7 precision & làm tròn | `format: 'currency'`, `GIA_TRI_THUE_GTGT.precision` |
| BR8 khoảng thời gian | phễu ngày `useListFilter({ showTime })` |
| BR11 tìm kiếm/lọc/sắp xếp | `traLaiHangBanAdvFilterFields` + `persistKey` |
| BR12 trạng thái chứng từ | `helpers/trangThai.ts` (5 trạng thái, không phải 2) |
| BR13 nút thao tác | menu ⋮ theo trạng thái + quyền |
| BR14 chế độ & hành vi form | 4 chế độ `create/edit/view/clone` |
| BR15 validation | `helpers/kiemTra.ts` + rule của `CommonEditableGrid` |
| BR16 cảnh báo nghiệp vụ | BR4 số lượng vượt = cảnh báo, không chặn |
| BR17 kỳ kế toán | MSG_203/204 đã có chuỗi; **server quyết định** |
| BR18 ngoại tệ | `đk-QĐ` — tỷ giá + toàn bộ cột/tổng quy đổi |
| BR19 kiểm tra trùng | MSG_213 (số hóa đơn trùng) — chuỗi sẵn, server quyết |
| BR20 số chứng từ | ô Số chứng từ + khóa khi Sửa |
| BR21 grid chi tiết con | `CommonEditableGrid` |
| BR24 tooltip/help text | `FieldLabel tooltip` cho Mã số ĐVQHNS · CCCD |
| BR25 phân quyền | `constants/permissions.ts` + `gates` |
| BR26 toast/notification | `useToast` cho mọi luồng |
| BR28 multi-tenant | khóa react-query có phạm vi công ty/kỳ |
| BR29 chính sách xóa | soft delete + token khóa lạc quan `updatedAt` |
| BR30 ẩn/hiện cột | `showSettings` + `columnConfigKey` |
| BR31 dòng tổng | `summary` server-side, lùi về tổng trang |
| BR32 copy · BR38 group · BR39 xuất Excel | do `CommonListTable` cấp sẵn |
| BR33 màu trạng thái | `fields/status.ts` (green/gold/blue/default) |
| BR36 ghi sổ · BR42 bỏ ghi sổ | luồng xác nhận + `ghiSoChungTu`/`boGhiSoChungTu` |
| BR37 ngày hạch toán | đồng bộ sang mọi tab; SCR dòng 284 một chiều |
| BR43 trim · BR44 truncate | `chu()` ở payload · `textMode` ở cột |
| BR45 thao tác hàng loạt | ⚠ chưa đạt — xem N3 |
| BR46 trường hệ thống bắt buộc | `updatedAt` round-trip |

**BR riêng của epic**: BR1 · BR2 · BR3 · BR4 · BR5 · BR10–BR17 của SCR_DanhSach ·
BR_KhongTongHopToKhaiGTGT · BR-TLH-SAISOT · BR19 (bộ chứng từ, phần cảnh báo xóa).

**BR chưa đạt**

| BR | Lý do |
| --- | --- |
| BR45 / BR14–BR16 hàng loạt | Chờ endpoint hàng loạt + popup "thành công một phần" (N3) |
| BR17 kỳ kế toán (chặn thật) | FE chỉ có chuỗi thông báo; kiểm kỳ là việc của server |
| BR19 kiểm tra trùng số hóa đơn | Như trên — MSG_213 sẵn sàng, server quyết định |
| BR-CORE-FREEZESIGN | Cần cờ `DaKeKhai` trên chi tiết hóa đơn — wire chưa có |
