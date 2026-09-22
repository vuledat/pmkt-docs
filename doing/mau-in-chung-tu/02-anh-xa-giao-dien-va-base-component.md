# Ánh xạ giao diện — mock `ThietLapMauIn.html` → hệ thống (style · `@base` · CSS cục bộ)

> **Trạng thái:** BẢN NHÁP CHỜ CHỐT (Q18–Q20 ở [00-plan-tong-the.md §14](00-plan-tong-the.md)). **Ngày:** 2026-09-17.
> **Chốt của user (2026-09-17):** *dùng base; nếu cần thì phối CSS riêng trong cụm màn này cho phù hợp vì màn hiển thị
> rất nhiều thông tin* → §3.
>
> Nguyên tắc: **bố cục và hành vi giữ 1:1 theo mock; phong cách theo hệ thống** (Roboto · brand red · radius 6/8 ·
> token antd v6 · toast góc phải trên). Mọi control là `@base`; ba khoảng trống được **bổ sung vào `@base`** (§4)
> chứ không import antd trần trong engine.

---

## 1. Token: giá trị của mock → token hệ thống

| Vai trò trong mock | Mock | Hệ thống | Nguồn |
|---|---|---|---|
| `--acc` nhấn: nút primary, segment đang chọn, eye bật, mục outline active | `#2b5f9e` | `BRAND_RED` `#EE0033` · hover `PRIMARY.hover` `#FF6272` · pressed `PRIMARY.pressed` `#A40027` | `base/theme/tokens.ts:26,221-227` |
| `--acc-l` nền mục active / hover menu | `#e8f0fa` | `PRIMARY.bg` `#FFF4F6` (`--color-primary-bg`) | `tokens.ts:226`, `base.css` |
| `--sel` viền + tag khối đang chọn | `#f59e0b` | viền 2px `BRAND_RED`, nền `--ui-brand-soft` `rgba(238,0,51,.12)`, tag nền `BRAND_RED` chữ `--ui-brand-contrast` | `base.css` |
| `--bg` nền ngoài | `#eef1f5` | `BODY_BG` `#F5F5F5` = `token.colorBgLayout` | `tokens.ts:59`, `antdTheme.ts:44` |
| `--line` viền panel / bảng | `#dfe3e8` | `token.colorBorderSecondary` `#E5E7EB` (`--ui-divider`); viền card `#D9D9D9` (`--ui-border`) | `antdTheme.ts:34-35` |
| `--text` | `#1f2329` | `--ui-text` `rgba(0,0,0,.88)` · `TEXT.main` `#1F1F1F` | `base.css`, `tokens.ts:233` |
| `--muted` (`.hint`, `.panel-h`, `.src`) | `#6b7280` | `--ui-text-secondary` `rgba(0,0,0,.65)`; hint nhỏ dùng `TEXT.description` `#8C8C8C` | `tokens.ts:237` |
| `--green / --amber / --red` (checks, tag) | `#15803d / #b45309 / #c62828` | `ALERT_TONES.success/warning/error` · `TAG_TONES.green/gold/red` · icon `FEEDBACK_STATUS_ICON` | `tokens.ts:183-189,315-320`, `feedback/feedbackIcons.ts` |
| `.tag.blue` | `#e8f0fa / #2b5f9e` | `ListTag tone="blue"` (`TAG_TONES.blue` `#E6F4FF / #1677FF`) | `status/CommonStatusTag.tsx` |
| font giao diện | Segoe UI 13 / 12,5px | `--ui-font-family` Roboto Variable; **chế độ dày** 12–13px (`FONT_SIZE.xs/sm`) chỉ trong `.pmkt-mau-in` | `base.css`, `tokens.ts:352` |
| radius | input 5px · nút 6px · panel 8px | field `small` 4 / `default` 6 · nút `default` 6 / `small` 4 · card 8 | `FIELD_SIZE`, `BUTTON_SIZE`, `--ui-button-*` |
| hover nút | `#f5f7fa` | `--ui-surface-hover` `#0000000A` | `base.css` |
| bóng giấy | `0 2px 14px rgba(0,0,0,.18)` | giữ nguyên (thuộc "giấy", không phải UI) | — |
| toast | góc phải **dưới**, nền tối | `useToast()` — antd notification góc phải **trên**, 343px (BR26) | `notification/useToast.tsx`, `antdTheme.ts Notification` |
| modal | 520px, viền head/foot | `UiModal width={520}` (mặc định 412) · `CommonConfirmModal` 412 | `feedback/UiModal.tsx`, `modal/CommonConfirmModal.tsx` |
| **giấy** (`#paper`) | Times New Roman, chữ đen | **giữ nguyên** — đó là bản in theo mẫu, không phải giao diện | — |
| icon ⠿ 👁 ✕ ↶ ↷ ⚙ − + | ký tự Unicode | `@phosphor-icons` qua barrel `base/icons`: `DotsSixVerticalIcon · EyeIcon · XIcon · ArrowUUpLeftIcon · GearSixIcon · MinusIcon · PlusIcon · PrinterIcon · MagnifyingGlassIcon · TrashIcon`; **thiếu** `EyeSlashIcon`, `ArrowUUpRightIcon`, `ArrowsOutIcon` → thêm vào barrel (§4) | `base/icons/index.ts` |

---

## 2. Ánh xạ control theo từng vùng của mock

Ký hiệu: ✅ có sẵn trong `@base` · ➕ bổ sung vào `@base` (§4) · 🧩 dựng trong engine bằng phần tử `@base` + CSS cục bộ.

### 2.1 Thanh trên (`#top`)

| Mock | Hệ thống | Props / ghi chú |
|---|---|---|
| crumb + `h1` "Thiết lập mẫu in: Chứng từ mua dịch vụ" | ✅ `PageHeader` (`title`, `actions`); breadcrumb do `AppLayout` vẽ từ `handle.crumbKeys` — **không** vẽ lại trong trang | `layout/PageHeader.tsx` |
| tag "Một mẫu riêng cho loại chứng từ này…", "Dựa trên mẫu chuẩn hệ thống", "Đã lưu / Chưa lưu" | ✅ `ListTag tone="blue"` · `tone="default"` · dirty → `tone="gold"` "Chưa lưu" | chữ qua `t()` ns `mauIn` |
| ↶ ↷ (`title` Ctrl+Z / Ctrl+Y) | ✅ `CommonButton variant="text" iconLeft={<ArrowUUpLeftIcon size={16}/>} ariaLabel disabled` bọc `Tooltip` | redo dùng `ArrowUUpRightIcon` (➕ barrel) |
| "Đặt lại mẫu chuẩn", "Đóng" | ✅ `CommonButton variant="default"` | |
| "Lưu ⌘ Ctrl+S" | ✅ `CommonButton variant="primary" title="Ctrl+S"`; **bỏ chip kbd** trong nút (design system không có) | `disabled` khi còn lỗi (R-MAUIN-0xx) |

### 2.2 Cột trái (`#left`, 250px)

| Mock | Hệ thống | Ghi chú |
|---|---|---|
| `.panel-h` "BỐ CỤC MẪU" / "KIỂM TRA TRƯỚC KHI LƯU" | 🧩 `CommonText size="xs" weight="semibold" tone="description"` + `.pmkt-mau-in-panel-h` (uppercase, letter-spacing .5px, padding 10px 14px 6px) | |
| `ul.ol > li` (grip · eye · tên · count · ✕) | 🧩 `.pmkt-mau-in-outline-row` = `useSortable` (dnd-kit) · grip `DotsSixVerticalIcon size={16}` màu `TEXT.disabled` (ẩn với khối `khoa.viTri`) · eye `CommonButton variant="text" size="small" iconLeft={<EyeIcon/>|<EyeSlashIcon/>} ariaLabel` · tên `CommonText` · count `CommonText size="xs" tone="description"` · ✕ `CommonButton variant="text" size="small" danger iconLeft={<XIcon/>}` (chỉ `TU_DO`) | active: nền `PRIMARY.bg` + viền trái 3px `BRAND_RED`, chữ 600; ẩn: chữ `TEXT.disabled` + `line-through`; hàng 32px |
| `.tag.gray` "tự do" cạnh tên | ✅ `ListTag tone="default"` + CSS cục bộ hạ font 10px/line-height 16px | |
| `#addFree` "+ Thêm khối tự do" | ✅ `CommonButton variant="default" size="small" iconLeft={<PlusIcon size={16}/>}` | |
| `#checks` (⛔ / ⚠ / ✓ + câu) | 🧩 `.pmkt-mau-in-checks` (viền `--ui-divider`, radius 8, padding 8px 10px): mỗi dòng icon `FEEDBACK_STATUS_ICON.error/warning/success` 16px + `CommonText size="xs"` màu `ALERT_TONES.*.text/icon` | **không** dùng `CommonAlert` mỗi dòng (cao 40px+/dòng, panel tràn) |
| `.hint` hướng dẫn cuối cột | ✅ `CommonText size="xs" tone="description"` | |

### 2.3 Cột giữa (`#ctb` + `#pv`)

| Mock | Hệ thống | Ghi chú |
|---|---|---|
| `#ctb` thanh công cụ canvas | ✅ `Toolbar gap={8}` (nền `token.colorBgContainer`, viền dưới `token.colorBorderSecondary`) | `layout/Toolbar.tsx` |
| `.seg` "Chứng từ đang mở / Dữ liệu mẫu" · A4/A5 · Dọc/Ngang | ➕ **`CommonSegmented size="small"`** | phương án thay: `CommonRadio.Group optionType="button"` — nhưng `fields/radio.css` chưa style biến thể nút; bieuMau đang dùng antd `Segmented` trần (`KieuDangForm.tsx:6`) ⇒ đưa vào base |
| `#pickVoucher` "Chứng từ khác…" + modal `.vlist` | ✅ **`CommonComboGrid`** (single) đặt ngay trên toolbar — lưới trong dropdown: Số CT · Ngày · Diễn giải · Tổng tiền; nguồn A5 (20 chứng từ gần nhất + tìm) | docblock `picker/CommonComboGrid.tsx`: chọn MỘT bản ghi từ danh sách tra cứu → ComboGrid, không cần popup; `ReferencePickerModal` là multi-select có bộ lọc kỳ — quá nặng cho việc này |
| `− 100% +` · "Vừa khung" | ✅ `CommonButton variant="text" size="small" iconLeft={<MinusIcon/>}` · `CommonText size="sm"` (min-width 42) · `PlusIcon` · `CommonButton variant="default" size="small" iconLeft={<ArrowsOutIcon/>}` | giữ nút ± như mock (bieuMau dùng Select mốc zoom — hai cách đều hợp lệ, chọn theo mock) |
| `#paper` | 🧩 `MauInPaper` trong `.pmkt-mau-in-giay` (nền trắng, bóng, `transform: scale(zoom)`, `transform-origin: top center`) | renderer dùng chung cho in |
| `.blk` hover / `.blk.sel` / `.tagb` | 🧩 CSS cục bộ: hover viền dashed `TEXT.disabled` + nền `--ui-surface-hover`; chọn viền 2px `BRAND_RED` + nền `--ui-brand-soft`; tag nhãn góc phải trên nền `BRAND_RED`, chữ 10px Roboto 600, radius 3px 3px 0 0 | kéo trực tiếp (F14): tay cầm `DotsSixVerticalIcon` hiện ở mép trái khối khi hover, `useSortable` cùng `DndContext` với outline |

### 2.4 Cột phải (`#ins`, 370px) — inspector

| Mock | Hệ thống | Ghi chú |
|---|---|---|
| `h3` + `.sub` | ✅ `CommonTitle level={5}` + `CommonText size="xs" tone="description"` | |
| `.sec` + `b.t` | ➕ **`PropSection`** (đưa lên `@base/components/layout/`) | bản gốc `bieuMau/thietKeBieuMau/components/PropField.tsx` (TIER 3) — sao lên base để hai màn dùng chung |
| `.f` (label 96px + control) | ➕ **`PropField labelWidth={96}`** | thêm prop `labelWidth` khi đưa lên base |
| `input[type=text]` (nhãn, nội dung, tên khối, ghi chú chân trang) | ✅ `CommonTextBox size="small" maxLength allowClear={false}` | 24px, radius 4 |
| `input[type=number]` (lề, cỡ chữ, cỡ tiêu đề, rộng %) | ✅ `CommonNumberInput size="small" locale={getActiveLocale()} grouped={false} min max step` width 64–72 | `locale` bắt buộc — `getActiveLocale` từ `@platform` |
| `select` (font, "Nửa dòng/Cả dòng" → `span`, căn cột) | ✅ `CommonSelectBox size="small" options width` | |
| `.seg2` (khổ/hướng, căn, cỡ logo, kiểu nền, kẻ ô, chỗ ký) | ➕ `CommonSegmented size="small"` | |
| `label.chk` | ✅ `CommonCheckbox`{nhãn} | |
| `.sw` 10 ô màu + ô hex | ➕ **`CommonColorPicker size="small" presets={MAU_CHU_GOI_Y} showText format="hex"`** | bieuMau dùng antd `ColorPicker` trần (`KieuDangForm.tsx:6`); wrapper chuẩn hoá `#rrggbb` 7 ký tự (R-MAUIN-012) |
| `input[type=range]` độ đậm nền | ✅ `CommonSlider showInputNumber locale min={5} max={100} inputNumberWidth={64}` | |
| `.search` "Tìm trường…" / "Tìm cột…" | ✅ `CommonTextBox size="small" prefix={<MagnifyingGlassIcon size={16}/>} allowClear placeholder` | |
| `table.fl` (grip · ☐ · nguồn · nhãn · rộng · kiểu/căn · B/I · cộng · ✕) | 🧩 **`BangDongKeoTha`** (engine): mỗi hàng là CSS grid `.pmkt-mau-in-row` + `useSortable`; anatomy theo `table/ColumnConfigDrawer.tsx` (grip `DotsSixVerticalIcon`, `CommonCheckbox`, `CommonTextBox size="small"`, `CommonNumberInput size="small"`); B/I = `CommonButton size="small" variant={on ? 'secondary' : 'default'}` 24×24; ✕ = `CommonButton variant="text" size="small" danger` | header cột `CommonText size="xs" tone="description"`; hàng 28px, hàng ẩn `opacity .55`; hàng đang kéo `opacity .35`; đích thả gạch trên 2px `BRAND_RED` |
| `.tag.gray/.blue` "tự do" / "dữ liệu" trong bảng | ✅ `ListTag tone="default" / "blue"` | |
| `.src` giá trị xem thử dưới nhãn | ✅ `CommonText size="xxs" tone="description" ellipsis` | |
| nút cuối mục: "+ Thêm dòng chữ tự do", "Chia đều về 100%", "+ Thêm trường dữ liệu…", "+ Thêm ô ký tự do", "Xóa khối này" | ✅ `CommonButton size="small"` — `variant="default"`; xoá khối `variant="text" danger` | |
| `<a data-goto="company">` "Cập nhật ở Thông tin công ty" | ✅ `CommonButton variant="link" size="small"` → `navigate(HE_THONG_PATHS.thongTinCongTy)` (chỉ tenant; super admin ẩn) | |
| "Chọn ảnh…" (nền ảnh) | ✅ `CommonImageUpload` / `ButtonUpload` — **Q7**: v1 chưa làm | |

### 2.5 Hộp thoại & thông báo

| Mock | Hệ thống | Ghi chú |
|---|---|---|
| `confirmBox` xoá khối tự do | ✅ `CommonConfirmModal tone="warning" icon={<TrashIcon/>}` — chữ theo khuôn BR3 "Xác nhận xóa … Thao tác này không thể hoàn tác." `closeLabel` bắt buộc | |
| `confirmBox` "Đặt lại mẫu chuẩn" | ✅ `CommonConfirmModal tone="warning"` | |
| `confirmBox` "Đóng khi chưa lưu" — mock **3 nút** (Lưu và đóng / Không lưu / Ở lại) | ✅ `useDiscardGuard` + `CommonConfirmModal` — **2 nút** theo BR3 ("Xác nhận đóng": *Dữ liệu đã có thay đổi. Bạn có chắc chắn muốn đóng? Thay đổi sẽ không được lưu.*) | lệch mock → **Q18** |
| `pickDataFields` (tìm + checkbox theo nhóm, trường đã có thì mờ) | ✅ `UiModal width={520} closeLabel footer={…}` + `CommonTextBox` tìm + nhóm `CommonCheckbox checked disabled` cho trường đã dùng + footer `CommonButton` "Thêm"/"Hủy" | |
| modal chọn chứng từ | thay bằng `CommonComboGrid` (§2.3) | |
| `toast()` | ✅ `useToast().success / error / warning / info` | góc phải trên; ≤3 toast (BR26) |
| `.menu` In (demo) | ✅ `CommonDropdownButtonTwofold` (`NutInChungTu`) — mục 🔒 cố định, "Mẫu tùy chỉnh", separator, "⚙ Thiết lập mẫu in…" | icon `PrinterIcon`, `GearSixIcon`, `LockIcon` |

---

## 3. CSS cục bộ — "chế độ dày" cho cụm màn mẫu in

Chốt của user: dùng base, phối CSS riêng trong cụm màn này khi cần. Áp theo **4 bậc, dừng ở bậc đầu tiên đủ**:

| Bậc | Làm gì | Ví dụ |
|---|---|---|
| 1 | **Prop có sẵn** của base | `size="small"` (field 24px), `variant`, `tone`, `weight` |
| 2 | **CSS trên phần tử của mình** trong `mauIn.css`, tiền tố `.pmkt-mau-in-*`, chỉ dùng biến `--ui-*` / `token.*` qua inline style như bieuMau (`theme.useToken()`) — **không hex trần** ngoài khối giấy | grid hàng `BangDongKeoTha`, outline, checks, panel-h, giấy |
| 3 | Base **thiếu prop** → **thêm prop vào base** (luật §6 `client/CLAUDE.md`), không copy component ra engine | `PropField labelWidth`, `CommonSegmented size` |
| 4 | Cuối cùng mới **ghi đè class antd**, chỉ trong phạm vi `.pmkt-mau-in`, chỉ selector **antd v6** còn tồn tại (kiểm ở `/__design-system`), kèm ghi chú lý do ngay trên rule | vd thu padding item của `Segmented` nhỏ trong bảng cột |

Thông số chế độ dày (chỉ trong `.pmkt-mau-in`, không rò ra ngoài):

| Thứ | Giá trị | Vì sao |
|---|---|---|
| Khung 3 cột | trái **250** · giữa `minmax(0,1fr)` · phải **370** (đúng mock); `min-width: 1280px`; full-bleed khỏi padding 16px của `AppLayout` | panel phải chứa bảng 7 cột; bieuMau (280/320) hẹp hơn vì bảng của nó ít cột |
| Chữ | inspector/outline 12px (`FONT_SIZE.xs`, line-height 18); tiêu đề mục 13px 600; hint 11–12px `TEXT.description` | mock 12–13px; body app 14px quá thưa cho 20 dòng trường |
| Field | `size="small"` 24px, radius 4 (`FIELD_SIZE.small`); số rộng 64–72px | |
| Hàng bảng | 28px; gap cột 4px; header 24px | mock `td padding 4px` |
| Nút nhỏ | `size="small"` 24px; icon 16px (`ICON_SIZE.action`) | |
| Khoảng cách | `SPACE.xxs/xs` 4/8; mục `.sec` padding 10px 0, viền trên `--ui-divider` | |
| Giấy | `KHO` px @96dpi, `CM_PX` 37,8; font/cỡ/màu theo JSON; `@media print` ẩn toàn bộ chrome, `@page` theo khổ/lề | |
| Full-bleed | đề nghị thêm `handle.fullBleed` cho `AppLayout` (bỏ padding 16) thay vì `margin:-16px` như `thietKeBieuMau.css` — **Q20** | tránh hack lặp lần 2 |

Class semantic (`docs/rules/fe-semantic-class-rule.md`) gắn thêm ở phần tử gốc của từng vùng:
`he-thong` › `thiet-lap-mau-in` › `bo-cuc | xem-truoc | thuoc-tinh` › `<khoi>`; class trình bày vẫn là `.pmkt-mau-in-*`.

---

## 4. Khoảng trống phải bổ sung vào `@base` (làm ở **client**, sao nguyên sang **client-admin**)

| Thành phần | Đặt ở | Vì sao vào base chứ không để trong engine | Ước lượng |
|---|---|---|---|
| `CommonSegmented` (bọc antd `Segmented`: `size`, `options`, `value/onChange`, `testId`, `ariaLabel`) | `base/components/fields/CommonSegmented.tsx` + `segmented.css` | dùng ≥2 màn (bieuMau + mauIn); brand red cho mục chọn theo token | 0,5 ngày |
| `CommonColorPicker` (bọc antd `ColorPicker`: `presets`, `showText`, chuẩn hoá `#rrggbb`, `allowClear`) | `base/components/fields/CommonColorPicker.tsx` | như trên | 0,5 ngày |
| `PropField` (+`labelWidth`, `docDong`) · `PropSection` | `base/components/layout/PropField.tsx` | bieuMau có bản TIER 3 riêng; mauIn cần y hệt → sao lên base, bieuMau chuyển sau (ngoài phạm vi) | 0,5 ngày |
| icon `EyeSlashIcon`, `ArrowUUpRightIcon`, `ArrowsOutIcon` | `base/icons/index.ts` | barrel icon là điểm nhập duy nhất | 0,1 ngày |
| `AppLayout` `handle.fullBleed` (tuỳ chọn, Q20) | `app/layouts/AppLayout.tsx` (client & client-admin) | bỏ hack margin âm | 0,5 ngày |
| Showcase ở `/__design-system` (Data Entry) cho 2 control mới | `app/pages/template/designSystemPages/` | để tester đối chiếu, giống các control khác | 0,3 ngày |

Tổng ≈ **2 ngày** — đã cộng vào WBS GĐ1 FE của `00-plan-tong-the.md §12`. Barrel `client-admin/src/base/index.ts`
đang lệch `client` ở 3 export (`CommonNumberText`, `DATE_DISPLAY_MASK_FORMAT` chỉ có ở client; `makeNumberFormatter…`
chỉ có ở client-admin) — engine **không** dùng ba thứ đó; khi sao 4 file mới sang phải thêm export ở cả hai barrel.

---

## 5. Checklist nghiệm thu giao diện (đưa vào DoD của GĐ1)

- [ ] Đặt cạnh mock: đủ 3 cột, đúng thứ tự panel/mục/control, đúng hành vi từng nút (F1–F10 của plan).
- [ ] `rg "#2b5f9e|#1f4877|#e8f0fa|#eef1f5|#dfe3e8|#f59e0b|Segoe UI" client/src/base/domainKit/mauIn` → **0 kết quả**.
- [ ] Hex trần trong `mauIn.css` chỉ nằm trong khối `.pmkt-mau-in-giay*` (giấy) — mọi thứ khác qua `--ui-*`/token.
- [ ] `rg "from 'antd'" client/src/base/domainKit/mauIn` chỉ còn `theme` và `import type` — không control antd trần.
- [ ] Mọi input · number · select · checkbox · slider · segmented · màu · nút · tag · modal · toast đều là `Common*`/`Ui*` từ `@base`.
- [ ] Toast góc phải trên; xác nhận đóng/xoá theo chữ BR3; Esc = Đóng; click ngoài = huỷ; focus không thoát popup.
- [ ] Đối chiếu tại `/__design-system` (Button · Text Field · Data Entry · Feedback) và `/__components`.
- [ ] `client-admin`: cùng engine sao nguyên, `npx vite build` xanh, màn super admin hiển thị giống màn tenant (khác mỗi tag phạm vi và nguồn dữ liệu xem thử).
- [ ] Zoom 40–160 % không vỡ layout; 1280px vẫn không cuộn ngang panel.
