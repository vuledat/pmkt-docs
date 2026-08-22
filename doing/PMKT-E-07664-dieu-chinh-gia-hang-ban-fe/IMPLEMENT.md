# IMPLEMENT — PMKT-E-07664 Điều chỉnh giá hàng bán (FE)

Nhật ký sinh code của `/gen-fe`. Nguồn: `pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan` +
Figma section “Điều chỉnh giá hàng bán” (`ymMyg329ejsgCWg28CNmGl`, node `15810-60793`).

---

## 0. Nhật ký cập nhật — soát lại 2026-08-20

Bản gốc của tài liệu này viết ngày **2026-08-12**. Soát lại hôm nay: **cả tài liệu BA lẫn code đều đã
đổi**, và ba kết luận của bản gốc **không còn đúng**. Mục này là delta; các mục bên dưới đã được sửa
theo trạng thái mới, chỗ nào lệch bản gốc đều ghi rõ.

### 0.1 Tài liệu BA đã đổi — `pmkt-docs` đã pull (HEAD `8e559f800`, 2026-08-20)

Ba commit chạm epic sau ngày code:

| Commit | Ngày | Nội dung |
|---|---|---|
| `b15f479bc` | 2026-08-15 | refactor(ba): **chuẩn hóa kiểu Control và Max length toàn bộ tài liệu** |
| `715907142` | 2026-08-16 | cập nhật entity |
| `d23d1e20d` | 2026-08-17 | đồng bộ tên entity LDM ↔ SCR field |

Diff `0705d142d..HEAD` trên thư mục epic: **9 file, 155 dòng đổi**. Phân loại:

**(a) Đổi tên ENTITY — không ảnh hưởng FE.**
`ENT_ChiTietDieuChinhGiaHangBan` → `ENT_sal_chung_tu_dieu_chinh_gia_hang_ban_chi_tiet`,
`ENT_HoaDonBanHang` → `ENT_sal_hoa_don_ban_hang`, `ENT_HeThongTaiKhoan` → `ENT_mst_he_thong_tai_khoan`
(6 file UC + `3.crud-matrix.puml`). FE không tham chiếu tên entity ở đâu ngoài comment → **không phải
sửa code**, chỉ là tên bảng cho BE.

**(b) Chuẩn hóa từ vựng CONTROL — ⚠ ảnh hưởng THẬT, hiện code đang lệch.**

| Tài liệu cũ (lúc code) | Tài liệu MỚI | Code hiện dùng |
|---|---|---|
| `combogrid search` · `Combogrid search + button` | **`CombogridSearchFlatGrid`** | `CommonSelectBox` ❌ |
| `textbox` · `text` | `TextField` | `CommonTextBox` ✅ |
| `number` | `InputNumber` | `CommonNumberInput` (qua `editor: 'number'`) ✅ |
| `select` · `Dropdown` | `Select` | `CommonSelectBox` ✅ |
| `readonly` | `TextField` (Cho phép sửa vẫn = N) | `displayOnly` ✅ |

`CombogridSearchFlatGrid` **là tên có thật trong design system** — nó nằm ở
`src/base/components/picker/comboGrid.css`, tức component `CommonComboGrid` của `@base`. Nghĩa là
tài liệu **đã chốt** thứ mà bản gốc §8 còn ghi là *“cần chốt với BA/Design có bắt buộc dạng combogrid
không”*. Câu trả lời: **có**. Xem nợ **5.3(a)**.

Danh sách ô phải chuyển sang combogrid (13 ô): Mã KH (4 tab) · Nhân viên bán hàng (4 tab) ·
Tài khoản tiền · Tài khoản nhận tiền · Tài khoản chi tiền · Tài khoản NH (tab HĐ) · **Mẫu số HĐ** ·
và 5 cột lưới chi tiết (Mã hàng · TK công nợ · TK doanh thu · TK giảm giá · Tài khoản CK · TK thuế GTGT).

**(c) Sửa Max length — ⚠ 6 hằng số trong `constants.ts` đang sai.**

| Ô | `MAX_LEN` trong code | Tài liệu MỚI | Việc phải làm |
|---|---|---|---|
| `nguoiNop` · `nguoiNhan` · `nguoiLinhTien` · `nguoiMuaHang` | `100` | **255** | nới lên 255 |
| `chungTuGoc` | `500` | **255** | **siết xuống 255** — đang cho nhập quá giới hạn |
| `mauSoHoaDon` | `1` (ô text) | `-` (đổi thành combogrid) | bỏ `maxLength`, ô thành combogrid |
| `maKhachHang` · `nhanVienBanHang` · `taiKhoan*` · `maHang` | `50` | `-` | bỏ `maxLength` (ô chọn id, không phải ô gõ) |
| `taiKhoanNganHang` (tab HĐ) | `50`→doc cũ `30` | `-` | bỏ |
| Thành tiền (CL) quy đổi | `TIEN_QUY_DOI_PRECISION = 6` (từ `21,6`) | `-` | **giữ nguyên** — bỏ precision là mất chữ số thập phân của tiền quy đổi; đây là chỗ tài liệu mới KÉM chính xác hơn bản cũ, cần BA xác nhận |

`SCR_DanhSachDieuChinhGia.md` **xóa hẳn cột “Max length”**, và đổi Control của `Ngày từ`/`Ngày đến`
từ `date` → `Text`. Cái sau là **artifact của đợt chuẩn hóa** (ô lọc ngày mà là text thì mất
date-picker) — code giữ `CommonDatePicker`, **cố ý không làm theo**.

### 0.2 Code đã đổi — phiên song song viết lại màn danh sách trên ENGINE

Bản gốc §3 ghi *“cố ý KHÔNG dùng `@domain-kit/chungTu`”*. **Quyết định đó đã bị đảo** (2026-08-14, bởi
phiên làm việc song song trong cùng domain). Trạng thái hiện tại:

| Thứ | Trước (bản gốc) | Nay |
|---|---|---|
| Khung danh sách | `DieuChinhGiaTab` tự dựng bằng `useListFilter` + `createSearchQueries` | `api/chungTuModule.tsx` — `defineChungTu` + `createChungTuModule`; `DieuChinhGiaTab` rút còn ~90 dòng, chỉ giữ mục ⋮ “Nhân bản” + popup |
| `components/DieuChinhGiaListTable.tsx` | lưới danh sách | ~~MỒ CÔI~~ → **đã xóa 2026-08-20** (299 dòng) |
| `components/DieuChinhGiaQuickDetail.tsx` | panel Xem nhanh | ~~MỒ CÔI~~ → **đã xóa 2026-08-20** (162 dòng) |
| Tab “Hạch toán” của panel Xem nhanh | có | **đã gỡ** 2026-08-14, cùng lý do với `chungTuBanHang` (panel xem NHANH dòng chứng từ; bút toán có chỗ riêng) — lệch Figma **có chủ ý** |
| Câu xác nhận Bỏ ghi sổ | câu ĐẶC THÙ của epic (“…Hóa đơn điều chỉnh được sinh ra cũng bị xóa”) | ~~tạm mất~~ → **đã trả lại 2026-08-20** qua `descriptor.confirmMessageKeys` |

File mới xuất hiện trong module (3): `api/chungTuModule.tsx` · `components/TabChuaDung.tsx` ·
`test/i18n.test.ts` (7 ca — kiểm khóa i18n dựng động resolve được, và `vi`/`en` khớp 1-1).

Module: **51 file · 9.868 dòng** (bản gốc: 48 file · 9.969 dòng).

⚠ **`api/chungTuModule.tsx` là `.tsx` nằm trong `api/`** — lệch cây quyết định `client/CLAUDE.md`
§5 (*có JSX → `components/`*). Nó có JSX thật (`render: () => <TabChuaDung />`). Xem nợ **5.3(b)**.

### 0.3 Cả 4 tab nhóm Bán hàng nay đều là module thật

`traLaiHangBan` và `hoaDonBanHang` đã hoàn thiện (có `pages/` + `index.ts` + test) và **đã được đăng
ký trong `routes.tsx`**. Thanh 4 tab của màn này giờ điều hướng được **cả bốn**, không còn tab nào rơi
vào “đang phát triển”. `_shared/constants/banHangTabs.ts` đã khai đủ 4 path.

### 0.4 Việc còn phải làm sau đợt soát này — **ĐÃ LÀM 2026-08-20**

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Chuyển ô chọn danh mục sang `CommonComboGrid` theo Control mới | ✅ **xong** — 14 ô (8 form + 6 cột lưới), cộng ô ngày Bước 1 sang `DateRangePicker` |
| 2 | Sửa `MAX_LEN` (đặc biệt `chungTuGoc` 500 → 255) | ✅ **xong** — viết lại cả bảng theo tài liệu mới |
| 3 | Xóa 2 file mồ côi (461 dòng) | ✅ **xong** — cộng dọn CSS chết theo |
| 4 | Chuyển `api/chungTuModule.tsx` → `components/` | ❌ **KHÔNG làm — tiền đề sai**, xem §0.5 |
| 5 | Trả lại câu cảnh báo Bỏ ghi sổ đặc thù | ✅ **xong** — thêm điểm mở rộng `confirmMessageKeys` cho engine |
| 6 | Hỏi BA: bỏ precision `21,6` của tiền quy đổi | ⏳ vẫn là câu hỏi cho BA (§6 mục 7) |

### 0.5 Vì sao KHÔNG chuyển `api/chungTuModule.tsx` sang `components/`

Bản soát ban đầu ghi đây là "lệch cây quyết định §5 (có JSX → `components/`)". Kiểm lại thì **tiền đề
đó sai về mặt quy ước nhà**:

| Module | Vị trí descriptor | Đuôi |
|---|---|---|
| `chungTuBanHang` (**module tham chiếu DUY NHẤT đạt §5**) | `api/chungTuModule.tsx` | `.tsx` — cùng lý do: `chiTietTabs` có `render: () => <TabChuaDung />` |
| `traLaiHangBan` | `api/chungTuModule.ts` | `.ts` — không khai `chiTietTabs` nên không có JSX |
| `hoaDonBanHang` | `api/chungTuModule.ts` | `.ts` — cùng lý do |
| `dieuChinhGiaHangBan` | `api/chungTuModule.tsx` | `.tsx` |

Cả **bốn** module đặt descriptor ở `api/`, và module tham chiếu cũng là `.tsx` vì đúng một lý do với
module này. Chuyển riêng module này sang `components/` sẽ biến nó thành ngoại lệ duy nhất của domain —
mất nhiều hơn được. Hai cách "sửa" khác cũng không giải quyết gì thật:

* bỏ JSX bằng `createElement` chỉ đổi CÚ PHÁP; `api/` vẫn import một component từ `components/`;
* tách `chiTietTabs` ra file khác thì phụ thuộc vẫn nguyên, chỉ dời chỗ.

→ Ghi lại thành **câu hỏi quy ước cho cả repo** (descriptor engine thuộc lớp nào), không phải lỗi của
module này. Muốn đổi thì đổi đồng loạt cả 4 module trong một lần.


## 1. Ngày · phạm vi đã code

**2026-08-12.** Chạy `/gen-fe` **không có plan FE** — user chọn “code thẳng từ PYC” (§0.2 của skill),
nên §1 + §2 của `/plan-fe` (đọc bắt buộc + khảo sát reuse có bằng chứng) được làm trước dòng code đầu
tiên và ghi lại ở mục 3 dưới đây.

Phạm vi user chốt: **toàn bộ 4 màn của PYC**.

| Màn (SCR) | Trạng thái |
|---|---|
| `SCR_DanhSachDieuChinhGia` | ✅ đủ — lưới 8 cột, phễu ngày + lọc nâng cao + tìm nhanh, dòng tổng, phân trang/sắp xếp server, panel Xem nhanh, nút thao tác theo trạng thái, xóa · ghi sổ · bỏ ghi sổ. **Từ 2026-08-14 khung này do engine `@domain-kit/chungTu` dựng** (§0.2); panel Xem nhanh còn **4 tab** (tab Hạch toán đã gỡ) |
| `SCR_ThemMoiDieuChinhGia` (Bước 1 — chọn nguồn) | ⚠ đủ khung, **chưa có dữ liệu** — endpoint nguồn chưa tồn tại (mục 5) |
| `SCR_ThemMoiDieuChinhGia` (Bước 2 — form) | ✅ đủ — hàng tùy chọn, 2-3 tab động theo ma trận, lưới chi tiết 22 cột, tab Thuế/Hạch toán tính thật, khối tổng |
| `SCR_SuaDieuChinhGia` | ✅ đủ — cùng component, khóa “Số chứng từ” |
| `SCR_XemChiTietDieuChinhGia` | ✅ đủ — cùng component, khóa mọi ô, bộ nút theo trạng thái |

Bản gốc sinh 48 file · 9.969 dòng. **Hiện tại: 51 file · 9.868 dòng** — xem §0.2.

---

## 2. File đã tạo / sửa

### Tạo mới — `client/src/features/banHang/dieuChinhGiaHangBan/`

| File | Vai trò |
|---|---|
| `index.ts` | cửa ra duy nhất của module (file DUY NHẤT ở gốc) |
| `api/model.ts` | hợp đồng Zod của `ENT_DieuChinhGiaHangBan` + chi tiết + hai chứng từ con |
| `api/dieuChinhGiaApi.ts` | base path · `toSearchRequest` · adapter BASE CRUD · ghi sổ / bỏ ghi sổ · cờ `DUNG_MOCK` |
| `api/mock.ts` | **NỢ** — adapter giả, kho rỗng, gỡ khi BE lên |
| `api/queries.ts` | hook react-query theo tenant + hai mutation chuyển trạng thái |
| `api/lookups.ts` | 10 nguồn danh mục cho popup (khách hàng · tài khoản · vật tư · …) |
| `api/nguonApi.ts` | I/O của Bước 1 — lưới nguồn, combo chọn nhanh, nạp dòng của một chứng từ |
| `api/formDetail.ts` | wire → form store; **BR5** nguồn → form |
| `api/payload.ts` | form store → thân request `POST` / `PUT` |
| `constants/constants.ts` | enum wire · khóa tab · giới hạn nhập · số đo Figma |
| `constants/paths.ts` | re-export path từ `_shared` (xem mục 4) |
| `constants/permissions.ts` | 7 mã quyền `DieuChinhGiaHangBan.*` theo `DanhSachQuyen.md` §B4.6 |
| `fields/types.ts` | form store · `NguCanhAnHien` · dòng nguồn |
| `fields/columns.ts` | 8 cột màn danh sách (bề rộng đọc từ Figma) |
| `fields/chiTietColumns.ts` | cột bảng panel Xem nhanh |
| `fields/chiTietFields.ts` | 22 cột lưới chi tiết + cascade BR10/BR15 |
| `fields/nguonFields.ts` | 16 cột lưới popup Bước 1 + cascade BR3 |
| `fields/tabColumns.ts` | cột tab Thuế và tab Hạch toán |
| `fields/status.ts` | registry nhãn + tông màu cho hai cột enum |
| `fields/options.ts` | option enum · thuế suất · nguồn chứng từ |
| `fields/texts.ts` | gói chữ cho component `@base` + bộ lọc nâng cao |
| `helpers/trangThai.ts` | giá trị wire trạng thái + 4 vị từ BR2/BR3 |
| `helpers/tinhToan.ts` | BR2 · BR3 · BR10 · BR15 · thuế · khối tổng |
| `helpers/anHien.ts` | bản code của ma trận ẩn/hiện (chính + phụ) |
| `helpers/hachToan.ts` | bút toán dự kiến 2 nhánh + bảng thuế |
| `helpers/kiemTra.ts` | validate liên trường (bảng Validate dòng 572-586) |
| `helpers/nguon.ts` | BR1 validate chọn nguồn + áp bộ ba BR3 |
| `hooks/useDanhMucDieuChinhGia.ts` | gom danh mục + TK tiền/thuế mặc định |
| `hooks/useDongBoTab.ts` | luật “Đồng bộ nhóm” (dòng 235-250) |
| `i18n/vi.ts` · `en.ts` · `registerDieuChinhGiaI18n.ts` | namespace DUY NHẤT `dieuChinhGia`; `en` khóa theo `vi` bằng kiểu, lệch khóa là lỗi biên dịch |
| `components/DieuChinhGiaTab.tsx` | thân màn danh sách — state, truy vấn, 4 luồng hành động |
| `components/DieuChinhGiaListTable.tsx` | lưới danh sách (trình bày) |
| `components/DieuChinhGiaQuickDetail.tsx` | panel Xem nhanh 5 tab |
| `components/DieuChinhGiaThemMoiModal.tsx` | popup Thêm/Sửa/Xem/Nhân bản (4 chế độ, 1 component) |
| `components/ChonNguonModal.tsx` | popup Bước 1 |
| `components/CongNoTab.tsx` · `ThanhToanTab.tsx` · `HoaDonTab.tsx` | thân ba nhóm tab |
| `components/TongHopPanel.tsx` | khối Tổng cộng |
| `pages/DieuChinhGiaHangBanPage.tsx` + `dieuChinhGiaHangBan.css` | entry lazy + stylesheet của màn |
| `test/*` (5 file, 90 ca) | số học · ma trận · wire · bút toán/validate · render |

### Bổ sung / đổi trạng thái sau 2026-08-14 (phiên song song — xem §0.2)

| File | Trạng thái |
|---|---|
| `api/chungTuModule.tsx` | **MỚI** — descriptor `defineChungTu` + `createChungTuModule`. ⚠ `.tsx` đặt trong `api/`, lệch cây quyết định §5 |
| `components/TabChuaDung.tsx` | **MỚI** — thân tab panel Xem nhanh chưa dựng (`render` của engine chỉ nhận `{ locale }`, không có `t`) |
| `test/i18n.test.ts` | **MỚI** — 7 ca: khóa i18n dựng động resolve được, `vi`/`en` khớp 1-1 |
| `components/DieuChinhGiaTab.tsx` | **VIẾT LẠI** — còn ~90 dòng, chỉ giữ mục ⋮ “Nhân bản” + popup |
| `components/DieuChinhGiaListTable.tsx` | **MỒ CÔI** (299 dòng) — engine thay thế |
| `components/DieuChinhGiaQuickDetail.tsx` | **MỒ CÔI** (162 dòng) — engine thay thế |

### Sửa file có sẵn (2 file, đều là sửa CỘNG THÊM, không đổi hành vi cũ)

| File | Sửa gì |
|---|---|
| `features/banHang/routes.tsx` | thêm 1 route `/ban-hang/dieu-chinh-gia-hang-ban` |
| `features/banHang/_shared/constants/banHangTabs.ts` | thêm 1 mục `dieuChinhHangBan` vào `BAN_HANG_TAB_PATHS` |

`app/router/RootRoutes.tsx` **không phải sửa**: `banHangRoutes` đã được nối tay từ trước.

---

## 3. Khảo sát reuse (thay cho §2 của `/plan-fe`) — đã reuse gì

### Dùng lại nguyên vẹn từ `@base` / `@platform` / `@core`

| Thứ | Dùng ở |
|---|---|
| `CommonListTable` | lưới danh sách · panel Xem nhanh · tab Thuế · tab Hạch toán |
| `CommonEditableGrid` | lưới chi tiết hàng hóa · lưới popup Bước 1 |
| `CommonModalShell` | popup Thêm/Sửa/Xem · popup Chọn nguồn |
| `CommonFilterPanel` · `useListFilter` · `PERIOD_PRESET` | phễu ngày + lọc nâng cao + chip |
| `TabMenu2Level` · `TabMenuChild` | thanh 4 tab nhóm · thanh tab trong popup và panel |
| `CommonActionMenu` · `RowActionButtons` · `Tooltip` | cột Chức năng |
| `CommonConfirmModal` · `useToast` | 3 luồng xác nhận + toast |
| `TotalBreakdown` | khối Tổng cộng (chế độ 2 cột khi ngoại tệ) |
| `CommonSelectBox` · `CommonTextBox` · `CommonTextArea` · `CommonDatePicker` · `CommonCheckbox` · `CommonButton` · `CommonAlert` · `CommonEmpty` · `Card` · `FieldLabel` | toàn bộ ô nhập |
| `createSearchApi` · `createSearchQueries` · `pageResponseSchema` · `http` · `useT` · `useHasPermission` · `useTenant` · `describeApiError` | tầng dữ liệu |
| `formatNumber` (`@core`) | ô tiền của dòng tổng |

**Không component nào phải viết mới ở `@base`, và `@base` không bị sửa.** Mọi `.tsx` trong
`components/` đều mang logic nghiệp vụ riêng của màn (ma trận ẩn/hiện, BR5, BR6, BR8), không phải
component trình bày dùng lại được — nên chúng đúng chỗ ở feature.

### Bổ sung 2026-08-20 — reuse thêm khi chuyển sang Control mới

| Thứ | Dùng ở |
|---|---|
| `CommonComboGrid` (`@base`) | 14 ô chọn danh mục, qua wrapper `components/DanhMucComboGrid.tsx` |
| `CommonDatePicker.RangePicker` (`@base`) | ô "Ngày hạch toán" của popup Bước 1 (`DateRangePicker` theo doc mới) |
| `ChungTuDescriptor.confirmMessageKeys` (`@domain-kit/chungTu`) | **prop MỚI tôi thêm vào engine** — xem §5.3(d) |

`DanhMucComboGrid` là component tự viết DUY NHẤT của đợt này, có ghi lý do ngay đầu file: `@base`
không biết `LookupSource` (base không fetch, không có khái niệm "danh mục") và `@domain-kit` không cấp
ô nhập nào; 14 lần lặp cùng một bộ 9 prop là 14 chỗ để một sửa đổi bị bỏ sót.

### Cố ý KHÔNG dùng

| Thứ | Lý do |
|---|---|
| ~~`@domain-kit/chungTu` (engine chứng từ)~~ | ⚠ **QUYẾT ĐỊNH NÀY ĐÃ BỊ ĐẢO ngày 2026-08-14** — xem §0.2. Lý do ban đầu: mẫu tham chiếu `chungTuBanHang` cũng không dùng, và engine đòi descriptor trỏ vào BE chưa tồn tại. Cách gỡ mà phiên song song chọn: khai đủ `endpoints` thật rồi **override Nhóm A/B bằng `api/mock.ts`**, gỡ nợ là đặt `DUNG_MOCK = false` và xoá hai khối override. Hướng đó đúng hơn hướng ban đầu |
| `@domain-kit/chungTuNguon` | engine đó phục vụ ô “Chọn chứng từ” trên **thanh tiêu đề** (`HeaderControls` + `defineSource`), còn Bước 1 của epic này là một **popup toàn màn** có tham số lọc riêng, ô tick từng dòng và ba cột nhập BR3 — khác hình dạng, không phải khác cấu hình |
| `@test/renderWithProviders` | luật tầng bịt `features/` khỏi `src/test`; harness dựng tay như `chungTuBanHang.render.test.tsx` |
| `features/muaHang/chungTuMuaHang/dieuChinhGia/` | tên gần giống nhưng là **điều chỉnh giá hàng MUA**, và module đó theo shape phẳng cũ đã đóng băng (`client/CLAUDE.md` §4.2) |

### Viết mới vì không có sẵn

Mọi file trong `helpers/` — đó là nghiệp vụ của riêng epic (BR2 · BR3 · BR5 · BR6 · BR8 · BR10 ·
BR15 · bút toán). `api/lookups.ts` và `hooks/useDongBoTab.ts` dựng lại bộ tối thiểu **local trong
leaf** vì luật tầng cấm hai `leaf` import chéo (cùng cách `chungTuBanHang` và `traLaiHangBan` làm).

---

## 4. Lệch so với tài liệu · quyết định đã chốt

### 4.1 Vị trí màn hình — **user đã chốt**

Figma vẽ màn này là **tab thứ ba** của thanh 4 tab nhóm Bán hàng (breadcrumb “Bán hàng › Điều chỉnh
hàng bán”), tức cùng một màn với `chungTuBanHang`. BA thì tách thành màn riêng có bộ quyền riêng
`DieuChinhGiaHangBan.*`.

→ **Module riêng + route riêng** (user chọn). Page tự vẽ lại thanh 4 tab; bấm tab khác là ĐIỀU HƯỚNG.
Cách này về sau trùng khớp với hai module `traLaiHangBan` / `hoaDonBanHang` đang được dựng song song.

### 4.2 Xung đột nhãn Figma ↔ BA (3 chỗ) — đã xử lý, **cần BA/Design xác nhận lại**

| Chỗ | Figma | BA | Đã chọn | Vì sao |
|---|---|---|---|---|
| Tiêu đề cột | “Loại điều chỉnh” | “Phương thức điều chỉnh” | **BA** | màn này CÒN một trường tên “Loại điều chỉnh” khác hẳn (tab Hóa đơn: Điều chỉnh giá / Sai sót / Khác) — và `6.messages.md` tách hẳn hai thông báo `MSG_102` (“phương thức”) vs `MSG_207` (“loại điều chỉnh trên tab Hóa đơn”). Dùng chung một nhãn là bẫy đọc |
| Giá trị cột | “Điều chỉnh tăng/giảm” | “Tăng/Giảm giá hàng bán” | **cả hai** | chuỗi BA là giá trị WIRE, nhãn Figma là chữ hiển thị (qua registry) |
| Cột “Hình thức thanh toán” | 3 nhãn: Điều chỉnh công nợ · Thu tiền ngay · Chi tiền ngay | 2 giá trị | **cả hai** | nhãn suy từ `thanhToanNgay` + `huongDieuChinhGia` ngay tại cột, không bịa thêm enum ba giá trị |
| Tiêu đề cột tiền | “Tổng tiền thanh toán **(VNĐ)**” | “Tổng tiền thanh toán” | **BA** | đồng tiền hạch toán là cấu hình của từng tenant; in cứng “VNĐ” là nói sai với công ty hạch toán bằng đồng tiền khác. Cột vẫn là số đã quy đổi |
| Cột thứ 3 panel Xem nhanh | “TK tiền” (mẫu: 111) | “TK công nợ” (BR7 → nhóm 131) | **BA** | 111 là tài khoản tiền mặt, không phải tài khoản công nợ — nhãn khung hình mâu thuẫn với chính nghiệp vụ nó minh họa |

### 4.3 Số đo Figma còn thiếu

Lưới popup Bước 1: khung hình chỉ vẽ **12 trong 16 cột** (bảng có thanh cuộn ngang). Sáu cột khớp
chắc chắn lấy số đo thật (44 · 53 · 118 · 127 · 99 · 99); các cột còn lại lấy bề rộng theo loại dữ
liệu. **Cần Design xác nhận.**

---

## 5. Nợ kỹ thuật

### 5.1 `api/mock.ts` — **nợ chính**

cell-app **chưa có module `dieu_chinh_gia_hang_ban`** (`cell/` chỉ có `chung_tu_ban_hang` và
`chung_tu_mua_hang`). Toàn bộ màn chạy trên adapter giả.

Gỡ nợ khi BE lên, đúng 3 bước ghi ở đầu `api/mock.ts`:
1. đối chiếu `api/model.ts` với DTO thật (và `formDetail.ts` · `payload.ts` — ba file này là TOÀN BỘ
   mặt tiếp xúc hợp đồng);
2. đổi `DUNG_MOCK` ở `api/dieuChinhGiaApi.ts` thành `false`;
3. xóa `api/mock.ts` và mọi import tới nó.

Kho của mock **bắt đầu rỗng** (giống `traLaiHangBan/api/mock.ts`): nó cấp LUỒNG (phân trang, lọc,
ghi sổ, xóa) chứ không cấp SỐ LIỆU — một bảng số kế toán bịa trông y hệt số thật nguy hiểm hơn hẳn
một màn trống.

**Hệ quả nhìn thấy được:** popup Bước 1 luôn trả lưới rỗng, và combo “Chọn nhanh chứng từ” luôn rỗng.
BR1/BR2 là phép tính trên lịch sử chứng từ bán hàng + hóa đơn điều chỉnh + chứng từ trả lại của khách
hàng (có quy đổi ĐVT giữa các chứng từ) — không mô phỏng được ở FE mà không bịa ra một “số lượng chưa
trả lại” không dựa trên gì.

### 5.2 Endpoint đã khai sẵn, chờ BE dựng đúng tên

```
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/search
GET    /api/ban-hang/dieu-chinh-gia-hang-ban/cot
GET    /api/ban-hang/dieu-chinh-gia-hang-ban/{id}
POST   /api/ban-hang/dieu-chinh-gia-hang-ban
PUT    /api/ban-hang/dieu-chinh-gia-hang-ban/{id}
DELETE /api/ban-hang/dieu-chinh-gia-hang-ban/{id}
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/{id}/ghi-so
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/{id}/bo-ghi-so
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/nguon/search
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/nguon/chung-tu
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/nguon/chung-tu/{id}/dong
```

7 mã quyền `DieuChinhGiaHangBan.{View, View.Detail, Create, Edit, Delete, Post, Unpost}` cũng chưa
được seed trong `iam_quyen` → hiện mọi `has(...)` trả false với người dùng không phải chủ sở hữu.

### 5.3 Nợ phát sinh sau đợt soát 2026-08-20 — **(a)–(e) đã xử lý cùng ngày**

| | Nợ | Chi tiết |
|---|---|---|
| (a) ✅ | ~~13 ô chưa phải combogrid~~ | Tài liệu (bản 2026-08-15) chốt Control `CombogridSearchFlatGrid` cho Mã KH · NV bán hàng · 4 ô tài khoản · Mẫu số HĐ · 5 cột tài khoản của lưới. Code đang dùng `CommonSelectBox`. Component có sẵn: `CommonComboGrid` (`@base`). `traLaiHangBan` đã bắt đầu chuyển (1 file) |
| (b) ❌ | ~~`api/chungTuModule.tsx` sai lớp~~ | **Tiền đề sai** — cả 4 module banHang đặt descriptor ở `api/`, và module tham chiếu `chungTuBanHang` cũng là `.tsx` vì đúng lý do này. Xem §0.5 |
| (c) ✅ | ~~2 file mồ côi, 461 dòng~~ | `DieuChinhGiaListTable.tsx` · `DieuChinhGiaQuickDetail.tsx` — không file nào import sau khi chuyển sang engine. Xoá hoặc nối lại, không để lơ lửng |
| (d) ✅ | ~~Mất câu cảnh báo Bỏ ghi sổ đặc thù~~ | Engine hỏi bằng câu chuẩn; câu của epic (“…Hóa đơn điều chỉnh được sinh ra cũng bị xóa” — UC_BoGhiSo bước 5) chưa có chỗ cắm. Chuỗi i18n **vẫn còn** ở `confirm.boGhiSo.message`, chỉ là chưa ai đọc nó |
| (e) ✅ | ~~6 hằng số `MAX_LEN` lệch tài liệu mới~~ | Bảng chi tiết ở §0.1(c). Nặng nhất: `chungTuGoc` đang cho nhập 500 trong khi tài liệu chốt 255 |

### 5.4 Phần chưa dựng (ngoài phạm vi hoặc chờ module khác)

| Phần | Lý do |
|---|---|
| Nút **“Chọn hóa đơn cần điều chỉnh”** trên tab Hóa đơn (dòng 400-407) | tham chiếu chức năng cùng tên của màn **Hóa đơn điều chỉnh** (`PMKT-E-06197`) — một popup tra cứu của module khác. Ô hiện chỉ hiển thị hóa đơn gốc đã chọn + dải mô tả “Điều chỉnh cho hóa đơn Mẫu số… ngày…” |
| Tab **Tham chiếu** trong khối lưới | dùng chung đặc tả `Common/NguonDuLieu/SCR_ThamChieuCT.md`, chưa dựng |
| Tab **Thuế · Hạch toán · Đính kèm · Tham chiếu** của panel Xem nhanh | Figma chỉ vẽ tab đầu; bốn tab kia hiện “đang phát triển” thay vì một bố cục tự nghĩ ra |
| Khối **III. Tính toán & Phân bổ chiết khấu** (dòng 436-438) | tài liệu chỉ ghi “Tham khảo phần chiết khấu của chứng từ bán hàng” — không có đặc tả riêng. Lưới vẫn có đủ cột `Chiết khấu %` · `Tiền chiết khấu` · `Tài khoản CK` và tính đúng BR10; **chưa có** popup Phân bổ chiết khấu và nút “Áp dụng” |
| **BR13** ĐVT khác chuẩn (dòng 487) — hiện thêm trường ĐVT quy đổi | một dòng duy nhất trong tài liệu, không có bảng trường; cần BA đặc tả |
| **BR14** Chiết khấu thương mại (dòng 488-493) | bảng trường của lưới KHÔNG có ô tick “Chiết khấu thương mại”; BR mô tả hành vi cho một ô không tồn tại — cần BA làm rõ |

---

## 6. Điểm chờ BA / Design

Sáu “Điểm cần xác nhận” của ma trận **chưa có trả lời**; dưới đây là cách đã chọn để code chạy được,
kèm chỗ phải sửa nếu BA quyết khác.

| # | Điểm | Đã chọn | Sửa ở đâu nếu khác |
|---|---|---|---|
| 1 | Trục cột ma trận (I1 × I2 = 4 cột, HTTT đưa xuống `(đk-HTTT)`) | theo ma trận | — |
| 2 | `(sl)` Ẩn cột TK doanh thu / TK giảm giá theo loại điều chỉnh | **ẩn cột không dùng** (BR8) — để cả hai thì màn Tăng bắt nhập một TK giảm giá không bao giờ được hạch toán | `helpers/anHien.hienCotTkDoanhThu` / `hienCotTkGiamGia` |
| 3 | Mâu thuẫn “Mã hàng”: Cho phép sửa = Y (dòng 446) vs BR5 “Disable” | **khóa khi có nguồn**, mở khi lập tay | `helpers/anHien.khoaMaHang` |
| 4 | `[CXM]` Tab **Ủy nhiệm chi** không có bảng trường | dùng chung bộ ô của các tab ngân hàng khác | `components/ThanhToanTab.tsx` |
| 5 | Loại tiền là input hay readonly | autofill từ nguồn, **không** cho sửa tay (BR5 dòng 184) | `components/DieuChinhGiaThemMoiModal.tsx` |
| 6 | Quy ước `Disable` = xám read-only | hiện xám read-only | — |

**Câu hỏi MỚI sau đợt soát 2026-08-20:**

7. **Bỏ precision của tiền quy đổi có đúng ý không?** Bản cũ khai “Thành tiền (CL) quy đổi” Max length
   `21,6` (21 chữ số nguyên, 6 thập phân); bản 2026-08-15 đổi thành `-`. Code đang giữ
   `TIEN_QUY_DOI_PRECISION = 6` — bỏ đi là mất phần thập phân của tiền quy đổi ngoại tệ. Đây là chỗ
   tài liệu mới **kém chính xác hơn** bản cũ, nên chưa làm theo.
8. **`Ngày từ` / `Ngày đến` của màn danh sách đổi Control `date` → `Text`** — code giữ
   `CommonDatePicker`. Nhiều khả năng là artifact của đợt chuẩn hóa, cần BA xác nhận.

**Ba mâu thuẫn NỘI TẠI của tài liệu phát hiện thêm trong lúc code:**

1. **MSG_105/106 vs BR2/BR3 — mâu thuẫn thật.** Bảng Validate bắt “Số lượng phải lớn hơn 0” và “Đơn
   giá phải lớn hơn 0”, trong khi BR2 (dòng 112-115) và BR3 (dòng 137-139) mô tả dòng **Dịch vụ** có
   `SL = Đơn giá = 0`, `Thành tiền ≠ 0` và khóa hai ô đó ở 0. Áp thẳng bảng Validate thì **không bao
   giờ lưu được chứng từ điều chỉnh giá dịch vụ**. → đã **miễn hai luật cho dòng dịch vụ**
   (`helpers/kiemTra.ts`, có test). Cần BA chốt.
2. **BR5 nhánh Hóa đơn điều chỉnh, mục “Thanh toán ngay”** (dòng 212-216) suy từ *hình thức thanh
   toán trên hóa đơn nguồn*, mà dòng nguồn không mang trường đó. → đặt `thanhToanNgay = false` (mặc
   định của form) thay vì đoán; đoán một giá trị thanh toán là thay người dùng quyết định một bút
   toán tiền (`api/formDetail.toFormValuesTuNguon`).
3. **Số chứng từ ở màn Sửa** — tài liệu ghi “không cho phép sửa” nhưng số chứng từ có mặt trên nhiều
   tab. → khóa ô Số chứng từ của **cả tab Công nợ lẫn tab thanh toán**; ma trận cũng nêu đúng câu hỏi
   này ở “Điểm cần xác nhận” #1 của `SCR_SuaDieuChinhGia_MaTranAnHien.md`.

---

## 7. Cổng nghiệm thu — output thật

### 7.1 Đo lại **2026-08-20** — SAU khi làm mục 1·2·3·5

| Lệnh | Kết quả | Của module này |
|---|---|---|
| `npm run typecheck` | **184 lỗi** — **y hệt trước khi sửa**, không tăng một lỗi nào | **0** |
| `npx eslint <module> + <engine đã chạm>` | **sạch** | **0** |
| `npm run lint:boundaries` | **79** = 76 "rule not found" + **3 vi phạm thật** | **0** |
| `npx vitest run <module> + <engine>` | **28 file · 490/490 PASS** (module 100 · engine 390) | ✅ |

⚠ **`lint:boundaries` 76 → 79 KHÔNG phải do việc này.** Ba lỗi tăng thêm nằm ở file của phiên song
song; vi phạm tầng THẬT duy nhất mới là `boundaries/dependencies` ở
`features/danhMucChungTu/taiKhoanNgamDinh/test/DongTaiKhoanTable.test.tsx` (leaf → `test`). Module này
và `domainKit/chungTu` đóng góp **0** lỗi boundary.

**Kiểm chéo có chủ đích:** 4 ca đỏ ở `chungTuBanHang.render.test.tsx` đã được xác minh bằng cách TẠM
GỠ thay đổi engine của tôi rồi chạy lại — **vẫn đỏ đúng 4 ca**, tức chúng đến từ việc đang dở của
phiên song song (cùng chỗ với lỗi typecheck `ThuTienTM.Create` ở `ChungTuBanHangTab.tsx`), không phải
từ `confirmMessageKeys`.

### 7.2 Đo trước khi làm mục 1·2·3·5 (cùng ngày)

| Lệnh | Kết quả | Của module này |
|---|---|---|
| `npm run typecheck` | **184 lỗi** — 129 `features/danhMuc` · 21 `chiPhiTraTruoc` · 7 `congCuDungCu` · 6 `soDuBanDau` · 6 `base/domainKit` · 5 `muaHang` · 5 `app/layouts` · 2 `phanQuyen` · 2 `base/components` · 1 `banHang` | **0** |
| `npx eslint <module> + routes.tsx + _shared` | **sạch** | **0** |
| `npx vitest run src/features/banHang/dieuChinhGiaHangBan` | **6 file · 97/97 PASS** | ✅ |

Lỗi `features/banHang` duy nhất nằm ở `chungTuBanHang/components/ChungTuBanHangTab.tsx` (quyền
`ThuTienTM.Create`/`ThuTienTG.Create`) — của phiên song song, **không phải module này**.

⚠ Nền repo đã đổi nhiều so với lần đo trước: xuất hiện thêm `chiPhiTraTruoc`, `congCuDungCu`,
`soDuBanDau`, `phanQuyen`; `tienMat`/`tienGui` đã sạch. Tổng lỗi **giảm** 192 → 184.

### 7.3 Đo lần đầu 2026-08-12 (giữ để đối chiếu)

| Lệnh | Kết quả | Của module này |
|---|---|---|
| `npm run typecheck` | 192 lỗi | 0 |
| `npm run lint` | 9 lỗi + 2 warning (`CommonSlider` + `legacy/**`) | 0 |
| `npm run lint:boundaries` | 76 lỗi (74 “rule not found” + 2 nợ cũ `axios` trong `legacy`) | 0 |
| `vitest` module | 5 file · 90/90 PASS | ✅ |
| `npm run build` | ĐỎ — `tsc -b` dừng ở đúng số lỗi nền | 0 |

`npm run build` đỏ là **trạng thái nền của repo**, không phải hồi quy: `build` chạy `tsc -b` trên toàn
bộ `src/`, mà `features/danhMuc` (nhánh chết) một mình đã 129 lỗi.

**Cổng cây commit:** module vẫn **chưa commit** (`?? src/features/banHang/dieuChinhGiaHangBan/`). Khi
commit phải `git add` toàn bộ file mới **TRƯỚC**, rồi mới commit hai file sửa (`routes.tsx`,
`_shared/constants/banHangTabs.ts`) — cả hai đều trỏ tới file mới, đúng kịch bản “xanh local, đỏ
deploy” ở `client/CLAUDE.md` §15.1. Sau đó chạy `npm run check:committed`.

## 8. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| **BR1** Phân trang | `DANH_SACH_PAGE_SIZE = 10` (SCR_DanhSach BR1) · `CHI_TIET_PAGE_SIZE = 20` |
| **BR2** Hiển thị & sắp xếp | `DEFAULT_SORT` = Ngày hạch toán ↓ · Ngày chứng từ ↓ · Số chứng từ ↓ |
| **BR3** Popup | `CommonModalShell` + hộp xác nhận “bỏ thay đổi” khi form bẩn |
| **BR7** Precision & làm tròn | `TIEN_QUY_DOI_PRECISION` cho ô tiền quy đổi (cột Max length `21,6`) |
| **BR8** Khoảng thời gian | phễu ngày `useListFilter({ showTime })`, mặc định “Đầu tháng đến hiện tại” |
| **BR11** Tìm kiếm / lọc / sắp xếp | tìm nhanh + 3 tiêu chí nâng cao + phễu ngày, tất cả server-side; nhớ bộ lọc theo phiên |
| **BR12** Trạng thái chứng từ | `helpers/trangThai.ts` — 5 giá trị của `core.entity.TrangThaiChungTu` |
| **BR13.1** Nút thao tác | con mắt + menu ⋮, lọc theo quyền **và** theo trạng thái dòng |
| **BR13.2** Nút trên form | Hủy · Lưu · Lưu và ghi sổ (Xem: Đóng) |
| **BR14** Chế độ & hành vi form | 4 chế độ `create/clone/edit/view` trên một component |
| **BR15** Validation | `helpers/kiemTra.ts` + `rules` của từng `Form.Item`; BR15.3 so sánh ngày |
| **BR16** Cảnh báo nghiệp vụ | cảnh báo khác tỷ giá (cho đi tiếp) vs chặn khác loại tiền |
| **BR17** Kỳ kế toán | `MSG_203` — **server quyết định**, FE hiển thị nguyên văn lỗi |
| **BR18** Ngoại tệ | `(đk-LT)` — khối cột + khối tổng quy đổi, `quyDoiTien` |
| **BR20** Số chứng từ | ô bắt buộc, khóa ở màn Sửa; kiểm trùng ở server (`MSG_109`) |
| **BR21** Grid chi tiết con | `CommonEditableGrid` — thêm/xóa dòng, dòng tổng, phân trang |
| **BR5 · BR6 · BR10** Combogrid | ✅ **đạt 2026-08-20** — 14 ô chọn danh mục dùng `CommonComboGrid` (popup bảng nhiều cột, tìm trong ô, phân trang), đúng Control `CombogridSearchFlatGrid` của tài liệu |
| **BR24** Tooltip / help text | 4 tooltip nguyên văn tài liệu ở tab Hóa đơn |
| **BR25** Phân quyền | 7 mã `DieuChinhGiaHangBan.*`; nút thiếu quyền **ẩn hẳn**, không để bấm rồi 403 |
| **BR26** Toast / notification | `useToast` cho cả 6 thông báo kết quả |
| **BR29** Chính sách xóa | chỉ xóa chứng từ chưa ghi sổ; xác nhận trước; token khóa lạc quan |
| **BR30** Ẩn/hiện cột | `showSettings` + `columnConfigKey` |
| **BR31** Dòng tổng | `summary` server-side trên toàn tập lọc, lùi về tổng trang khi chưa có |
| **BR32** Copy | mặc định của `CommonListTable` |
| **BR33** Màu trạng thái | `fields/status.ts` — xanh “đã xong”, vàng “chưa xong”, xám “huỷ” |
| **BR34** Sửa từ màn xem | popup Xem có nút Chỉnh sửa khi chưa ghi sổ (BR1 của SCR_XemChiTiet) |
| **BR36** Ghi sổ · **BR42** Bỏ ghi sổ | `useGhiSo` / `useBoGhiSo` + xác nhận (bỏ ghi sổ cảnh báo nguyên văn về hóa đơn điều chỉnh bị xóa) |
| **BR37** Ngày hạch toán | validate `Ngày hạch toán ≥ Ngày chứng từ` (`MSG_205`) |
| **BR43** Trim | `laDongCoDuLieu` + `toSearchRequest` coi chuỗi trắng là rỗng |
| **BR44** Truncate text | `textMode` theo từng cột |
| **BR45** Thao tác hàng loạt | Ghi sổ · Bỏ ghi sổ · Xóa, lọc trước theo trạng thái, chạy tuần tự |
| **BR46** Trường hệ thống | `updatedAt` làm token khóa lạc quan trên PUT / DELETE / ghi sổ |

### BR chưa đạt

| BR | Lý do |
|---|---|
| **BR38** Group dữ liệu trên lưới | Figma không vẽ; `CommonListTable` chưa bật nhóm cho màn này |
| **BR39** Xuất Excel | `DanhSachQuyen.md` §B4.6 **không bật** quyền Xuất Excel cho chức năng này |
| **BR19** Kiểm trùng · **BR17** kỳ kế toán | thuộc server (`MSG_109` · `MSG_301` · `MSG_203`); FE hiển thị nguyên văn lỗi trả về |

| **BR22 / BR23 / BR40** Danh mục cây | không thuộc phạm vi màn chứng từ |
| **BR27** Trang hệ thống | thuộc `app/` |
| **BR28** Multi-tenant | do `@platform` lo (mọi query khóa theo `congTyId`/`kyKeToanId`) |
