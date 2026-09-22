# IMPLEMENT — PMKT-E-14549_21 · Thiết lập mẫu in chứng từ (FE)

| | |
|---|---|
| Ngày | 2026-09-19 |
| Nhánh | `feat/mau-in` (client) — xuất phát từ `0d515b6e8` (bản cứu hộ dựng từ mock HTML) |
| Kế hoạch | [`00-ke-hoach-tong.md`](00-ke-hoach-tong.md) + 9 file con |
| Đặc tả | [`../PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/`](../PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/) — 271 luật · **0 mục `OPEN`** |
| Module | `client/src/base/domainKit/mauIn/` — **95 tệp** (91 `.ts`/`.tsx` + 3 fixture JSON + 1 CSS) |
| Trạng thái | 🟡 **HOÀN THÀNH MỘT PHẦN** — lô 0…5 xong, **cổng truy vết đã `DAT` (244/244)**; **lô 6 chưa làm** (chờ BE lên endpoint thật) |

---

## 1. Phạm vi đã code

| Lô | Nội dung | Trạng thái |
|---|---|---|
| **0** | Dọn nền: revert 6 file phục vụ route đã bỏ (D1), xoá `features/heThong/thietLapMauIn/` (20 file), xoá/đổi tên các file engine chốt BỎ | ✅ xong |
| **1** | `api/model.ts` (Zod) · `constants/*` · 12 helper thuần · `hooks/mauInStore.ts` (zustand + immer + zundo 60) · `i18n/` đủ 2 ngôn ngữ · fixture `bh.*` · `api/mock.ts` | ✅ xong |
| **2** | Khung màn: `pages/ThietLapMauInScreen.tsx` · `components/modal/ThietLapMauInModal.tsx` · cột trái · thanh Xem trước · `BanInPaper` · badge · 3 hộp xác nhận · `useLuuMau` · `useDongMan` · `useDatLaiMauChuan` · `mauIn.css` | ✅ xong |
| **3** | Bốn bảng chỉnh khối chuẩn (Thiết lập mẫu · Đầu trang · Tiêu đề · Bảng · Chữ ký) | ✅ xong |
| **4** | Khối tự do: lưới ô Excel, thanh công cụ 15 nút, menu chuột phải 10 mục, hộp chọn trường, kho trường | ✅ xong |
| **5** | Lối vào: `NutInChungTu` · `XemTruocBanInModal` · gắn vào **Chứng từ bán hàng** | ✅ xong |
| **6** | Nối mua dịch vụ, gỡ `api/mock.ts` khi BE xong, một vòng `/qa-flow` trên trình duyệt thật | ⛔ **chưa làm** |

---

## 2. Cây tệp đã sinh

```
client/src/base/domainKit/mauIn/
├── index.ts                      cửa ra duy nhất của engine
├── api/
│   ├── model.ts                  hợp đồng Zod + type (⚠ nhóm kế thừa .optional(), CẤM .default)
│   ├── mauInApi.ts               A1…A6, mọi phản hồi qua Zod
│   ├── queries.ts                query key + 4 hook TanStack
│   └── mock.ts                   ⚠ NỢ — dữ liệu tạm khi BE chưa có endpoint
├── components/
│   ├── BoCucMauPane · DongKhoiBoCuc · ChuThichBoCuc      cột trái "Bố cục mẫu"
│   ├── ThanhXemTruoc · XemTruocPane                      cột giữa (undo/redo · khổ · hướng · zoom)
│   ├── BanInPaper                 renderer giấy DUY NHẤT (trang xem trước + bản in)
│   ├── LuoiTuDo · OLuoi           lưới ô kiểu Excel, gộp/tách, kéo thả, phím tắt
│   ├── ThanhCongCuTuDo · MenuChuotPhaiO                  15 nút + 10 mục menu
│   ├── BadgeTrangThai             Đã lưu · Chưa lưu · Có lỗi
│   ├── NutInChungTu               lối vào (split button In ▾)
│   ├── SortableList               GIỮ NGUYÊN từ bản cũ (sortable tự dựng trên @dnd-kit/core)
│   ├── inspector/                 InspectorPane + 11 bảng chỉnh
│   └── modal/                     8 popup
├── constants/  constants.ts · paths.ts · permissions.ts
├── fields/     types.ts · boCucKhoiFields · cotBangFields · chuKyFields · khoTruongFields · texts
├── helpers/    luoiTuDo · doRongCot · keThua · truongDungChung · kiemTraMau · chuanHoaMau ·
│               mauChuan · hopNhatVoiCatalog · thaoTacKhoi · dinhDangGiaTri · trangGiay · inBanIn ·
│               keoTha  ← bảng quyết định kéo–thả, tách khỏi `LuoiTuDo.tsx` để gọi thẳng được
├── hooks/      mauInStore · MauInStoreProvider · useMauInStore · useVungChon · useKeoThaO ·
│               useLuuMau · useDongMan · useDatLaiMauChuan
├── i18n/       vi.ts · en.ts · registerMauInI18n.ts   (MỘT namespace `mauIn`)
├── pages/      ThietLapMauInScreen.tsx · mauIn.css
└── test/       19 tệp test + 3 fixture `bh.*`
```

**6 tệp test thêm ở đợt đóng cổng truy vết** (không phải test độn — mỗi tệp đóng một nhóm luật thật):

| Tệp | Đóng nhóm luật nào |
|---|---|
| `BanInPaper.test.tsx` | 58 khẳng định trên **renderer giấy** — phần lớn nhóm `064…105` (tiêu đề · bảng · chữ ký) và `177…220` |
| `trangGiay.test.ts` | khổ giấy · hướng · lề · `R-TLMI-054…062` |
| `hopDongDuLieu.test.ts` | **hình dạng schema** cho các luật "luôn theo thiết lập chung" (`037` · `046`…) và hợp đồng A1/A5 |
| `XemTruocBanInModal.test.tsx` | `R-TLMI-269` · `R-TLMI-270` — nhánh dựng bản in lỗi, có tắt cờ nợ `DUNG_MOCK_KHI_BE_LOI` |
| `keoTha.test.tsx` | `R-TLMI-149` · `154` · `205` · `206` — gọi thẳng `helpers/keoTha.ts` + bộ xử lý `onDragEnd` cấp màn |
| `luuMau.test.tsx` | bốn nhánh Lưu (200 · 403 · 409 · 5xx) — `R-TLMI-034` · `111` · `246` · `248` · `249` · `250` · `252` · `258` |

**Gắn vào nghiệp vụ** — đúng một chỗ:
`client/src/features/banHang/chungTuBanHang/components/ChungTuBanHangThemMoiModal.tsx`
(+1 import `@domain-kit/mauIn`, +1 `<NutInChungTu …/>`), cộng 2 khoá i18n `tenNghiepVu` (vi + en).

---

## 3. Đã reuse gì

| Dùng lại | Ở đâu |
|---|---|
| `CommonModalShell` (`size="full"`) · `CommonModalFooter` · `CommonConfirmModal` | vỏ hai modal, 3 hộp xác nhận 2 nút |
| `PropSection` · `PropField` (bản chưa commit, GIỮ) | mọi bảng chỉnh cột phải |
| `CommonSegmented` (bản chưa commit, GIỮ) | cụm `Căn` của lưới cột |
| `CommonNumberInput` · `CommonTextBox` · `CommonSelectBox` · `CommonCheckbox` · `CommonRadio` · `CommonButton` | mọi ô nhập |
| `CommonDropdownButtonTwofold` · `CommonDropdownBasic` | split button `In ▾`, menu chuột phải |
| `useToast` (BR26.1) · `useHasPermission` (BR25) · `useT` · `createResourceKeys` | toast, quyền, i18n, query |
| `matchesQuickSearch` (`@core`) | lọc không phân biệt dấu (R-TLMI-116 · 151 · 168) |
| `SortableList.tsx` (bản cũ, **giữ nguyên**) | kéo thứ tự khối · cột bảng · ô ký — repo KHÔNG có `@dnd-kit/sortable` |
| `@base/icons` (18 icon bổ sung, GIỮ) | toàn màn |

**Viết mới** — mỗi tệp có comment `// đã kiểm @base/@domain-kit — không có sẵn vì…`:
lưới ô Excel có `rowSpan/colSpan` sửa tại chỗ · thanh công cụ ngữ cảnh · renderer giấy · cột trái
Bố cục mẫu · thanh zoom/undo · badge 3 trạng thái · 12 helper thuần · store editor + 5 hook.

---

## 4. Lệch so với kế hoạch

| # | Lệch gì | Vì sao | Ảnh hưởng |
|---|---|---|---|
| L-FE-1 | **Không phải MỘT `DndContext` duy nhất** (plan D8) | `SortableList` được chốt "GIỮ NGUYÊN" và nó **tự mang** `DndContext`; gỡ ra là viết lại một component đang chạy | Không đổi hành vi. ⚠ Đã phải chia lại trách nhiệm: K2 và K3-cùng-khối do `LuoiTuDo` nghe bằng `useDndMonitor`, `useKeoThaO` chỉ còn K3-khác-khối và K4 — nếu cả hai cùng xử lý thì ô đổi nội dung **hai lần** và hoá ra không đổi |
| L-FE-2 | ~~Nút In ở slot `filter` của header popup~~ → **ĐÃ SỬA 2026-09-21: nút nằm ở CHÂN popup**, cùng hàng với Lưu / Chỉnh sửa | Kết luận ban đầu **sai**: `CommonModalFooter` đã có sẵn slot `rightExtraNode` nhận ReactNode tự do — thêm 2026-08-24 cho đúng ca này (split button `In ▾` của phiếu thu/chi `nganQuy`). Chỉ thiếu ở `mode: 'edit'`, đã mở | **ĐÓNG** — Dat chốt 2026-09-21 |
| L-FE-3 | **Khoá i18n của thông báo là CHÍNH MÃ MESSAGE** (`'MSG_PMKT-E-14549_21_201'`), không phải `msg.e201` như `08-hop-dong-api-va-i18n.md §3.12` | `docs/rules/truy-vet-luat.md §6` quy định khoá i18n **chính là mã** | Tốt cho truy vết; bảng trong plan nên sửa theo |
| L-FE-4 | **3 fixture** `bh.catalog/chung/du-lieu`; `bh.mau-chuan` **dẫn xuất** từ `helpers/mauChuan.ts` | một nguồn sự thật — mẫu chuẩn sinh từ đặc tả form (R-TLMI-006) | Test mẫu chuẩn kiểm thẳng hàm dựng |
| L-FE-5 | `BoCucMauPane.test.tsx` / `ThanhXemTruoc.test.tsx` thành `describe` trong `ThietLapMauInScreen.test.tsx`; thêm `NutInChungTu.test.tsx` | hai vùng đó đọc store qua Provider của màn, không dựng tách được | Plan §13.1 dự tính 13 tệp; thực tế **19 tệp** sau đợt đóng cổng truy vết (bảng ở §2) |
| L-FE-6 | `fields/khoTruongFields.tsx` → **`.ts`** | `react-refresh/only-export-components` — tệp vừa export component vừa export hàm là lỗi lint | — |
| L-FE-7 | `MuaDichVuModal.tsx` **revert về `origin/develop`** (gỡ nút In cũ) | bản cũ gọi `duongDanThietLapMauIn()` đã bỏ theo D1 | Mua dịch vụ tạm KHÔNG có nút In — **lô 6** |
| L-FE-8 | **`CommonColorPicker` không được dùng** dù plan §3.1 ghi "Dùng lại, SỬA" | Figma frame 1 vẽ **10 ô màu + ô hex**, không có trigger picker; `R-TLMI-066` đòi gõ `#rrggbb` và báo `MSG_210` khi rời ô — antd `ColorPicker` không làm được. `RiengCuaMauGroup` dựng 10 nút preset + `CommonTextBox` | ✅ **ĐÃ XỬ LÝ** — `grep` toàn `client/src` (trừ `legacy/`) cho thấy **không consumer nào** ngoài chính barrel, nên `git rm src/base/components/fields/CommonColorPicker.tsx` + gỡ 2 dòng export khỏi `src/base/index.ts` |
| L-FE-9 | `Căn` của khối **Tiêu đề** là `CommonSelectBox`, không phải `CommonSegmented` | Figma frame 5 vẽ dropdown "Giữa"; `03-panel-…md §B2` cũng ghi `select`. Cụm `Căn` của **cột bảng** thì đúng là `CommonSegmented` 3 icon (Figma frame 2) | — |
| L-FE-10 | Lưới khối tự do vẽ bằng `<table>` + `<colgroup>`, không phải CSS grid như plan §3.2 | `R-TLMI-180` đòi ô gộp chiếm ĐÚNG số dòng/cột ở cả màn lẫn bản in — chỉ `rowSpan`/`colSpan` thật làm được | `R-TLMI-131` vẫn đúng nhờ `table-layout: fixed` + `<col>` đều nhau |
| L-FE-11 | `+ Dòng` / `+ Cột` **không mờ** khi chạm trần 20/6 (plan §4 ghi Disable) | V08/V09 nói `MSG_…_208`/`216` phát **khi bấm** nút — nút mờ thì message không bao giờ tới người dùng. Bấm được → chặn + toast nguyên văn. Sàn 1 dòng/1 cột (C20) **vẫn mờ** đúng `R-TLMI-135` | — |
| L-FE-12 | Ba ô nhập bỏ prop `help` của `CommonTextBox`, tự vẽ dòng lỗi `role="alert"` | `help` bọc thêm `<div>` quanh ô ⇒ ô unmount/remount đúng lúc lỗi bật–tắt, **mất con trỏ giữa lúc gõ** (đã bắt được ca này khi test) | — |

---

## 5. Nợ kỹ thuật

| # | Nợ | Chi tiết |
|---|---|---|
| **N1** | **`api/mock.ts` còn nguyên** | BE chưa có endpoint đúng hợp đồng A1…A6. Hai modal rơi về mock khi query lỗi (`TODO nợ:` đánh dấu tại chỗ). **Lô 6 xoá tệp này**; cổng cuối kiểm `grep -rn "mock" …/mauIn/api/` ⇒ rỗng |
| **N2** | **Tải ảnh nền chưa gọi mạng** | `taiAnhNen`/`xoaAnhNen` đã viết đúng hợp đồng A3/A4 nhưng UI mới chỉ ghi `nen.tenTep` vào store |
| **N3** | **`Xuất file` trên màn Xem trước đang mờ** | Ngoài phạm vi FE theo §1 kế hoạch tổng — việc của BE |
| **N4** | **`R-TLMI-026` hiện thực MỘT PHẦN** — menu In ở **màn danh sách** chưa mount | Pilot chỉ gắn vào popup chứng từ. Theo `docs/rules/truy-vet-luat.md`, mã luật được đặt **đúng chỗ sẽ hiện thực** — docblock của `components/NutInChungTu.tsx` — kèm lý do hoãn, không tự chế dấu riêng. Engine **không phụ thuộc popup nào**: `NutInChungTu` chỉ cần `chungTuId` của dòng, nên mount vào hành động dòng màn danh sách là đủ; `NutInChungTu.test.tsx` đã chứng minh nó chạy được với một `chungTuId` rời (không có popup nào mở). Việc mount thật thuộc **lô 6** |
| **N5** | **Thumbnail / số trang bản in là tĩnh** (`Trang 1 / 1`) | Chưa có cơ chế đo ngắt trang phía FE |
| **N6** | **Logo đơn vị chưa có ảnh thật** (Q5) | `CompanyInfoResponse` chưa có trường logo; FE vẽ ô tick + khung `[LOGO] cỡ vừa` như Figma frame 4 |
| **N7** | **Hai link `Mở Cấu hình báo cáo chứng từ` đang ẩn** (Q4) | Epic `_20` chưa có màn; theo đề xuất Q4 là **ẩn link, không để link chết**. Comment đánh dấu đúng chỗ bật lại |
| **N8** | **Link `Thiết lập người ký` đang ẩn** (`R-TLMI-052`) | Màn đích có thật (`features/heThong/thongTinCongTy`) nhưng `domain-kit` **không được import `@features/*`** (lint tầng). Cần host truyền handler xuống |
| **N9** | **K2 / K3 chưa có test DOM** (`R-TLMI-149` · `R-TLMI-154`) | Mô phỏng một phiên kéo thật của `@dnd-kit` trong jsdom (PointerEvent + `DragOverlay`) không đáng tin. Đã **rút bảng quyết định ra `helpers/keoTha.ts`** và gọi thẳng trong `keoTha.test.tsx` — thứ dễ sai là bảng theo `data.current.loai`, và nó nay kiểm được chính xác. Còn lại là cử chỉ chuột thật ⇒ QA `/qa-flow` (lô 6) |
| **N12** | **Cờ `DUNG_MOCK_KHI_BE_LOI = true`** ở `constants/constants.ts` | Cùng gốc với N1: query lỗi thì rơi về `api/mock.ts` thay vì báo lỗi thật. `R-TLMI-270` (không mở màn xem trước khi dựng bản in hỏng) **đã hiện thực thật**, và `XemTruocBanInModal.test.tsx` mock cờ về `false` để chạy đúng đường sau lô 6. Lô 6: đặt cờ `false` → xoá cờ + `api/mock.ts` |
| **N10** | **`msg.sh` chưa chạy** | Thư mục PYC nằm trong vùng đóng băng `pmkt-docs/ba/Phase_2/**` — phiên này bị cấm mở. Đã đối chiếu tay: đủ **26 mã** ở CẢ `vi.ts` và `en.ts` |
| **N11** | **5 chuỗi chưa có mã `MSG_`** (L-4, L-5) | 2 tooltip nút In disable · xung đột phiên bản · thiếu quyền In. Đang mượn `MSG_COMMON_001`/`003` + khoá i18n cục bộ. Chờ BA cấp mã (`04-quyet-dinh-ban-giao.md §7.1`) |

---

## 6. Kết quả cổng

### 6.1 Typecheck — **KHÔNG thêm lỗi mới**

```
$ ELECTRON_RUN_AS_NODE=1 "$CODE" node_modules/typescript/bin/tsc -b --noEmit
239 lỗi          (baseline develop: 239)

$ diff <(sort tsc-baseline-develop.txt) <(sort tsc-hien-tai.txt)
(rỗng)
```

239 lỗi nền nằm ở `features/danhMuc` (129) · `muaHang` (26) · `giaThanh` (16) · `taiSanCoDinh` (13)… —
**0 lỗi đến từ code mẫu in**, kiểm chứng bằng `diff` chứ không bằng số đếm.

### 6.2 Vitest — module `mauIn`

```
$ ELECTRON_RUN_AS_NODE=1 "$CODE" node_modules/vitest/vitest.mjs run src/base/domainKit/mauIn --reporter=dot
 Test Files  19 passed (19)
      Tests  368 passed (368)
   Duration  44.65s
```

### 6.3 ESLint

```
$ ELECTRON_RUN_AS_NODE=1 "$CODE" node_modules/eslint/bin/eslint.js \
    src/base/domainKit/mauIn src/base/index.ts \
    src/features/banHang/chungTuBanHang/components/ChungTuBanHangThemMoiModal.tsx
exit=0            # 0 lỗi · 0 cảnh báo
```

18 lỗi lint phát sinh lúc đầu đã sửa THẬT, không tắt rule:
`react-hooks/refs` (10 — tay cầm kéo thành prop tuỳ chọn) ·
`react-hooks/set-state-in-effect` (5 — chuyển sang "điều chỉnh state ngay trong render") ·
`react-refresh/only-export-components` (3 — tách component khỏi tệp `fields/`).

Đợt đóng cổng truy vết phát sinh thêm 2 lỗi, cũng sửa thật:
`react-refresh/only-export-components` trên `LuoiTuDo.tsx` (hàm `quyetDinhThaVaoO` chuyển sang
`helpers/keoTha.ts` — vừa hết lỗi vừa gọi thẳng được trong test) ·
`@typescript-eslint/consistent-type-imports` trên `XemTruocBanInModal.test.tsx`
(`typeof import(...)` nội tuyến → `import type * as HangSoNs` + `type HangSoModule`).

### 6.4 Cây commit

```
$ git -C client status --porcelain | grep '^??' | wc -l
0
```

Mọi tệp mới đã `git add`. ⚠ **Chưa commit** — `client/CLAUDE.md §14` cấm tự commit khi user không yêu cầu.
`npm run check:committed` **không chạy** (báo lỗi giả trên Windows — R9; dùng `git status` thay thế).

### 6.5 Lệnh KHÔNG chạy

| Lệnh | Vì sao |
|---|---|
| `npm run lint:boundaries` | `npm` không có trên PATH ở máy này. Kiểm tay: **0** `../../` xuyên tầng trong module, **0** import `@features/*` · `@app/*` · `axios` · `antd/es/*` từ `domainKit/mauIn` |
| `npm run build` / `npx vite build` | như trên |
| `./docs/rules/msg.sh <PYC> fe` | PYC nằm trong vùng đóng băng — xem N10 |
| `/qa-flow` trên trình duyệt thật | thuộc lô 6 |

---

## 7. BR đã áp dụng

⚠ Chức năng này chạy bộ BR **Phase 2** (quyết định **Q-02** của user).

| BR | Áp ở đâu |
|---|---|
| BR50.6 | `R-TLMI-004/005/035` — mẫu không khai `ChiNhanhId` |
| BR50.7 | `R-TLMI-165/166` — kho trường phẳng (`helpers/hopNhatVoiCatalog.ts`, `fields/khoTruongFields.ts`) |
| BR51.5 | `R-TLMI-001/005` |
| BR3 | `MSG_402/403/404` dùng `CommonConfirmModal` 2 nút. ⚠ `MSG_401` **cố ý lệch BR3** — 3 nút (D11 · Q12), dựng riêng ở `HopThayDoiChuaLuuModal.tsx` |
| BR7 | `helpers/dinhDangGiaTri.ts` — tiền/số theo cấu hình tenant, mặt `baoCao` |
| BR8 | `tachNgay()` + dòng `Ngày … tháng … năm …` |
| BR13 | mọi bảng chỉnh kiểm **khi rời ô** (`R-TLMI-230`) |
| BR14 | `Ctrl+S` · `Ctrl+Z` · `Ctrl+Y` · `Esc` · phím tắt lưới (mũi tên · Delete · Enter/F2) |
| BR25 | `constants/permissions.ts` + `NutInChungTu` — thiếu quyền **ẩn hẳn**, không mờ |
| BR26.1 | toast góc phải trên cho `MSG_101/102/103/104` |
| BR30 | chốt C18 — khối đang ẩn thì bỏ qua validate của khối đó |
| BR35 | `R-TLMI-029/030` — đóng màn về đúng nơi vừa mở ra |

**BR chưa đạt / cố ý lệch:** BR3 (xem trên) · BR51.6 cộng gộp mặt hàng là tầng **BE**, ngoài phạm vi FE.

---

## 8. Bảng truy vết luật

Bảng sinh **bằng máy**, không viết tay:

```bash
./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec fe
```

```
Tong 244 luat (tang=fe): OK 244 · NO-TEST 0 · MISSING 0 · BLOCKED 0 · VI-PHAM 0

KET LUAN: DAT.
```

Đường đi của con số: `OK 0 · MISSING 244` (trước khi code) → `OK 155 · NO-TEST 88 · MISSING 1`
(hết lô 5) → **`OK 244`** (đợt đóng cổng). **0 `VI-PHAM`** và **0 `BLOCKED`** — không luật nào bị
chặn bởi mâu thuẫn `OPEN` (sổ mâu thuẫn đã đóng hết).

### 8.1 Luật kiểm bằng cách KHÁC hành vi — đọc trước khi tin cổng

`trace.sh` chỉ đếm "mã luật có mặt trong tệp test". Bảng dưới liệt kê **mọi luật mà test không dựng
lại được hành vi người dùng**, kèm cách kiểm thay thế. Ghi ra để không ai đọc `DAT` thành "đã kiểm
như thật".

| Luật | Vì sao không dựng lại được hành vi | Kiểm bằng cách nào thay thế |
|---|---|---|
| `R-TLMI-178` · `200` · `265` · `181` · `194` · `195` | Nằm hoàn toàn trong `@media print` / `break-inside` / `word-break`. **jsdom không có engine phân trang**, cũng không chạy `@media print` | `BanInPaper.test.tsx` **đọc thẳng `pages/mauIn.css` từ đĩa** rồi khẳng định đúng khai báo CSS đang có (`readFileSync(resolve(cwd, '…/mauIn.css'))`). Chứng minh được "luật cài bằng CSS chứ không bằng nhánh JS", **không** chứng minh được trình duyệt ngắt trang đúng ⇒ vẫn cần `/qa-flow` |
| `R-TLMI-075` · `263` | Thứ tự vẽ (`z-index`, hình nền dưới mọi khối) là kết quả layout, jsdom không tính | DOM: hình nền là **phần tử đầu tiên** của trang; + khẳng định cặp quy tắc CSS `position: relative; z-index: 1` |
| `R-TLMI-149` · `154` (cùng khối) | Một phiên kéo thật của `@dnd-kit` cần PointerEvent + `DragOverlay`; mô phỏng trong jsdom cho kết quả không đáng tin | `helpers/keoTha.ts` là **bảng quyết định thuần**, `keoTha.test.tsx` gọi thẳng với đủ 6 hình dạng `data.current`. Cử chỉ chuột thật ⇒ QA (N9) |
| `R-TLMI-044` | antd v6 `Select` không lái được trong jsdom (`click` lên `role="option"` không commit) | Đổi giá trị qua `capNhatTrang` rồi đọc kết quả hiệu dụng trên `.thanh-xem-truoc .kho-giay`; nhánh kế thừa phủ ở `keThua.test.ts` · `mauInStore.test.ts`. Docblock của test ghi rõ hạn chế này |
| `R-TLMI-003` · `037` · `046` · `047` · `048` · `049` · `101` · `165` · `182` · `219` | Là **hợp đồng dữ liệu** ("luôn theo thiết lập chung", "payload không mang khoá kế thừa"), không có hành vi màn hình để bấm | `hopDongDuLieu.test.ts` khẳng định **hình dạng schema Zod** (khoá `.optional()` chứ không `.default()`) và `luuMau.test.tsx` đọc payload thật gửi lên A5 |
| `R-TLMI-026` | Chưa mount ở màn danh sách (**N4**) | Mã luật đặt tại docblock `NutInChungTu.tsx` — đúng nơi sẽ hiện thực; test chứng minh engine chạy được chỉ với `chungTuId`, không cần popup |
| `R-TLMI-269` · `270` | Cần cửa sổ in thật / lỗi mạng thật | `XemTruocBanInModal.test.tsx` mock `../api/mauInApi` cho query lỗi **và** mock cờ `DUNG_MOCK_KHI_BE_LOI: false` để chạy đúng đường sau lô 6; khẳng định màn **không mở** và toast `MSG_…_003` bật |
| `R-TLMI-249` | Rollback là hành vi của **BE** | FE chỉ chịu trách nhiệm "không âm thầm coi là đã ghi": `luuMau.test.tsx` khẳng định sau 5xx badge vẫn `Chưa lưu` |

**Kết luận trung thực:** cổng `trace.sh` đã `DAT`, nhưng **lô 6 chưa làm** ⇒ trạng thái tổng vẫn là
**"hoàn thành một phần"**, không phải "xong".

### Phụ lục — toàn bộ bảng truy vết

Chạy lệnh trên để in đủ 244 dòng; bảng đổi theo code nên **không chép cứng vào đây**.

---

## 9. Việc phải làm tiếp (theo thứ tự)

1. **Lô 6** — nối `chungTuMuaHang/MuaDichVuModal.tsx`; mount `NutInChungTu` vào hành động dòng màn
   danh sách (đóng nốt `R-TLMI-026`, **N4**); đặt `DUNG_MOCK_KHI_BE_LOI = false` rồi gỡ
   `api/mock.ts` khi BE lên endpoint thật (**N1** · **N12**); chạy `/qa-flow` để phủ nhóm luật ở §8.1
   (bản in, ngắt trang, cử chỉ kéo–thả thật).
2. **BA trả lời** Q1 (5 mã `MSG_` còn thiếu) · Q4 (link epic `_20`) · Q5 (trường logo) ·
   Q7/Q8 (mẫu chuẩn có kèm khối tự do không — đã chốt X5/X6 theo luật, BA xác nhận lại).
3. ~~Design xác nhận vị trí nút `In ▾`~~ — **đã chốt 2026-09-21: chân popup**, cùng hàng với Lưu /
   Chỉnh sửa, qua `rightExtraNode` (L-FE-2 đóng). `CommonColorPicker` (L-FE-8) **đã gỡ** — không cần
   hỏi nữa.
4. **`/verify-spec`** sau khi lô 6 xong, để chấm lại 244 luật trên code đã đủ.
