# Kế hoạch sửa lỗi build — `../../client`

> Trạng thái tại thời điểm khảo sát: **`npm run build` FAIL**.
> Nguồn số liệu: chạy thực tế `npm run typecheck`, `npm run build`, `npm run lint`, `npm run lint:boundaries`, `npm run test` trong `../../client`.

## 0. Tóm tắt tình trạng

| Cổng kiểm tra | Kết quả | Số lỗi |
|---|---|---|
| `npm run build` (`tsc -b && vite build`) | **FAIL** — dừng ở bước `tsc`, chưa từng chạy tới `vite build` | 193 |
| `npm run typecheck` | **FAIL** | 193 (63 ở source, 130 ở `**/test/**`) |
| `npm run lint` | **FAIL** | 4 |
| `npm run lint:boundaries` | **FAIL** | 1 (lỗi cấu hình, không phải lỗi kiến trúc) |
| `npm run test` | **FAIL** | 9/2267 test · 5/270 file |

Phân bố mã lỗi TS:

| Mã | Số | Nằm ở |
|---|---|---|
| TS18048 / TS2532 (possibly undefined) | 124 | **chỉ trong `test/`** — hệ quả của `noUncheckedIndexedAccess` |
| TS2322 (không gán được kiểu) | 20 | source + test |
| TS2352 (cast không hợp lệ) | 18 | source |
| TS6133 (khai báo thừa) | 10 | source |
| TS2769 / TS2345 (sai tham số) | 14 | source |
| TS2344 / TS2349 / TS2554 / TS2367 | 7 | source |

**Lưu ý quan trọng:** `tsconfig.app.json` có `"include": ["src"]` nên **file test cũng nằm trong build**. Không thể chỉ sửa 63 lỗi source rồi build — phải xử lý cả 130 lỗi test (Nhóm G).

---

## 1. Thứ tự thực hiện

Sắp theo tỉ lệ *số lỗi khử được / công sức*. Mỗi nhóm là một commit riêng.

| # | Nhóm | Lỗi khử | Rủi ro | Ghi chú |
|---|---|---|---|---|
| 1 | **G** — `noUncheckedIndexedAccess` trong test | 124 | Thấp | Cơ học, 1 helper dùng chung |
| 2 | **B** — thiếu index signature khi cast `Record<string, unknown>` | 18 | Thấp | Mẫu lặp 10 chỗ |
| 3 | **C** — `string \| null` vs `string \| undefined` ở 7 Tab | 14 | Thấp–TB | Có sẵn hook chuẩn để thay |
| 4 | **A** — `EnumOption` không tương thích option type | 20 | Thấp | Sửa 1 interface × 2 file |
| 5 | **D** — biến/import thừa | 10 | Thấp | Xóa, hoặc dùng cho đúng |
| 6 | **E** — icon Phosphor | 6 | Thấp | Đổi kiểu |
| 7 | **F** — lỗi lẻ | 4 | **TB–Cao** | Có bug logic thật, cần quyết định |
| 8 | **H** — lint | 5 | TB | Có 1 bug hook thật |
| 9 | **I** — test fail | 9 test | TB | Chưa rõ nguyên nhân, cần điều tra |

Nhóm 1–6 là cơ học. Nhóm 7–9 cần đọc kỹ nghiệp vụ.

---

## 2. Chi tiết từng nhóm

### Nhóm A — `EnumOption` thiếu index signature (20 lỗi, TS2322)

**Nguyên nhân.** `EnumOption` được khai báo trùng lặp ở 2 nơi:
- `src/features/muaHang/chungTuMuaHang/muaDichVu/options.ts:10`
- `src/features/tienMat/chungTuTienMat/thuTien/options.ts:12`

Cả hai đều là `{ value: string; label: string }`. Nhưng hai type đích đều có index signature:
- `EditableSelectOption` (`src/base/components/entry/editableGridModel.ts:16`) — `{ label: ReactNode; value: string | number; [key: string]: unknown }`
- `CommonSelectBoxOption` (`src/base/components/picker/CommonSelectBox.tsx:78`)

TypeScript không cho gán type không có index signature vào type có index signature.

**Cách sửa (khuyến nghị).** Bỏ `EnumOption` tự chế, dùng thẳng type của `@base`:

```ts
// options.ts — thay vì tự khai báo interface EnumOption
import type { CommonSelectBoxOption } from '@base'
export type EnumOption = CommonSelectBoxOption
```

Nếu `CommonSelectBoxOption` và `EditableSelectOption` không tương thích 2 chiều thì phương án thay thế là thêm index signature vào `EnumOption`:

```ts
export interface EnumOption {
  value: string
  label: string
  [key: string]: unknown
}
```

> Cần kiểm tra `CommonSelectBoxOption` trước khi chọn — ưu tiên phương án 1 vì nó xóa được type trùng lặp, đúng tinh thần "constant/type đặt gần nơi dùng nhưng không nhân bản".

**Điểm lỗi:**
- `muaDichVu/grid.ts:67,76,84,174,183`
- `thuTien/grid.ts:31,40,59`
- `MuaDichVuModal.tsx:339`
- `PhieuThuModal.tsx:273,291,305`
- (+ các lỗi kéo theo trong `muaDichVu/test/grid.test.ts`)

---

### Nhóm B — Row type thiếu index signature khi cast (18 lỗi, TS2352 + TS2344)

**Nguyên nhân.** Mẫu sort động bị copy-paste y hệt vào 8 file `api.ts`:

```ts
function compareBy(field: string, dir: 1 | -1) {
  return (a: ThuTienRow, b: ThuTienRow): number => {
    const av = (a as Record<string, unknown>)[field]   // ← TS2352
    const bv = (b as Record<string, unknown>)[field]
    ...
```

`ThuTienRow` là interface không có index signature nên cast trực tiếp bị chặn.

**Cách sửa.** Cast qua `unknown` (đúng gợi ý của TS, không vi phạm luật "không `any`"):

```ts
const av = (a as unknown as Record<string, unknown>)[field]
```

Vì mẫu này lặp ở 8 file, **nên trích một helper dùng chung** thay vì sửa 16 chỗ:

```ts
// src/base/domainKit/list/compareBy.ts (hoặc @core)
export function compareBy<Row>(field: string, dir: 1 | -1) {
  return (a: Row, b: Row): number => {
    const av = (a as unknown as Record<string, unknown>)[field]
    const bv = (b as unknown as Record<string, unknown>)[field]
    if (typeof av === 'number' && typeof bv === 'number') return (av - bv) * dir
    return String(av ?? '').localeCompare(String(bv ?? '')) * dir
  }
}
```

**Điểm lỗi TS2352 (dòng ~22-26 mỗi file):**
`muaHang/chungTuMuaHang/_shared/api.ts` · `dieuChinhGia/api.ts` · `doiTruChungTu/api.ts` · `hoaDonMua/api.ts` · `muaDichVu/api.ts` · `traLaiHangMua/api.ts` · `tienMat/chungTuTienMat/thuTien/api.ts` · `danhMuc/vatTuHangHoa/loaiVatTu/mapper.ts:23`

**Điểm lỗi TS2344 (generic constraint `Record<string, unknown>`):**
- `PhieuThuModal.tsx:383` — `HachToanLine`
- `MuaDichVuModal.tsx:420` — `MuaDichVuServiceLine`
- `vatTu/DonViQuyDoiTab.tsx:67` — `DonViQuyDoiRow`

Ba chỗ này khác: chúng truyền row type vào **generic có ràng buộc** `Record<string, unknown>`. Cast không giải quyết được — phải **thêm `[key: string]: unknown` vào chính interface row**, hoặc nới ràng buộc generic của component nhận vào.

---

### Nhóm C — `string | null` vs `string | undefined` ở 7 list Tab (14 lỗi, TS2769 + TS2345)

**Nguyên nhân — đây là nhóm đáng chú ý nhất.** `filter.timeRange` trả `{ from: string | null; to: string | null }`, nhưng 7 Tab tự viết tay:

```ts
const dateRangeRef = useRef<{ from?: string; to?: string }>({ from: appliedFrom, to: appliedTo })  // ← TS2769
const resetPageForDateRange = useCallback((from?: string, to?: string) => { ... }, [])
useEffect(() => {
  resetPageForDateRange(appliedFrom, appliedTo)   // ← TS2345
}, [resetPageForDateRange, appliedFrom, appliedTo])
```

**Đã có hook chuẩn sẵn:** `src/base/domainKit/list/useServerListState.ts` — được viết ra ĐÚNG để thay thế đoạn copy-paste này (docblock của nó ghi rõ: *"chứng từ list tabs (which hand-rolled an identical copy — see `ThuTienTab.tsx`) can share it too"*). Hook này khai báo đúng:

```ts
export interface ServerListDateRange { from: string | null; to: string | null }
const dateRangeRef = useRef<ServerListDateRange>({ from: appliedFrom, to: appliedTo })
const resetPageForDateRange = useCallback((from: string | null, to: string | null) => { ... }, [])
```

Grep cho thấy hook này **hiện chưa có nơi nào dùng** — nó được trích ra nhưng các Tab chưa được migrate. Đó chính là lý do build vỡ.

**Cách sửa (khuyến nghị).** Migrate 7 Tab sang `useServerListState`, xóa toàn bộ state paging/sort/search/dateRange viết tay:

```ts
const { page, pageSize, params, setSearch, onTableChange } = useServerListState<ThuTienRow>({
  filter,
  defaultSort: DEFAULT_SORT,
})
```

Kiểm tra `ServerListParams.dateRange` (`{from: string|null; to: string|null} | null`) khớp với `ChungTuMuaHangListParams.dateRange` (`_shared/model.ts:58` — cùng shape ✅).

**Cách sửa tối thiểu** (nếu chưa muốn migrate): đổi kiểu local thành `string | null`, khớp `ServerListDateRange`.

**Điểm lỗi (2 lỗi/file):**
`MuaHangHoaTab.tsx:63,71` · `TraLaiHangMuaTab.tsx:56,64` · `ThuTienTab.tsx:71,79` · `DieuChinhGiaTab.tsx:56,64` · `DoiTruChungTuTab.tsx:54,62` · `HoaDonMuaTab.tsx:55,63` · `MuaDichVuTab.tsx:66,74`

---

### Nhóm D — Khai báo thừa (10 lỗi, TS6133)

`tsconfig` bật `noUnusedLocals` + `noUnusedParameters` nên đây là lỗi build, không phải cảnh báo.

| File | Dòng | Ký hiệu |
|---|---|---|
| `thuTien/PhieuThuModal.tsx` | 26 | `CommonEmpty` (import) |
| | 43 | `STUB_LOAI_TIEN` (import) |
| | 109 | `locale` |
| | 155, 156 | `gridFields`, `gridTexts` |
| `muaDichVu/MuaDichVuModal.tsx` | 199, 200 | `gridFields`, `gridTexts` |
| `vatTu/DonViQuyDoiTab.tsx` | 23, 26 | `locale`, `fields` |
| `base/components/dataEntry/UiComboGrid.tsx` | 54 | `toGridTrack` |

**Cách sửa.** Trước khi xóa, kiểm tra xem có phải code còn dở không — `gridFields`/`gridTexts` xuất hiện ở cả hai modal cùng lúc, khả năng cao là phần i18n cho grid **chưa được nối vào JSX**. Nếu đúng thì phải nối vào chứ không phải xóa (xóa sẽ để lại text hardcode, vi phạm luật 2).

---

### Nhóm E — Icon Phosphor (6 lỗi, TS2322)

`src/features/danhMuc/vatTuHangHoa/vatTu/TinhChatSection.tsx:31-38`

```ts
const TINH_CHAT_ICON: Record<TinhChatVatTu, (props: IconProps) => ReactElement> = {
  HangHoa: PackageIcon,   // ← TS2322 ×6
  ...
}
```

`@phosphor-icons/react` export icon với kiểu `Icon` (là `ForwardRefExoticComponent`, không phải plain function component), nên không gán được vào `(props: IconProps) => ReactElement`.

**Cách sửa.** Dùng thẳng kiểu `Icon` do thư viện export:

```ts
import { type Icon } from '@phosphor-icons/react'
const TINH_CHAT_ICON: Record<TinhChatVatTu, Icon> = { ... }
```

Kiểm tra `TinhChatGlyph` (dòng 40-43) vẫn render được — `<Icon size weight color />` hợp lệ với type `Icon`.

---

### Nhóm F — Lỗi lẻ (4 lỗi) ⚠️ có bug thật

**F1. `VatTuFormBody.tsx:70` — TS2554: Expected 2 arguments, but got 1**

```ts
queryFn: () => api.detail(sourceId as string),
```

`CrudApi.detail` (`src/platform/query/createCrudQueries.ts:44`) có signature `detail(id: string, scope: QueryScope)`. Biến `scope` đã có sẵn trong scope hàm (dùng ở `vatTuKeys.detail(scope, sourceId)` ngay dòng trên).

→ Sửa: `api.detail(sourceId as string, scope)`

**F2. `vatTu/mapper.ts:38` — TS2367: so sánh luôn `false`** ⚠️ **BUG LOGIC**

```ts
(phepTinh == null || phepTinh === '')
```

`PhepTinhQuyDoi = 'Nhan' | 'Chia'` (`model.ts:31`), field khai `phepTinh?: PhepTinhQuyDoi | null`. Không bao giờ là `''`.

→ Sửa: bỏ nhánh `=== ''`, chỉ giữ `phepTinh == null`. **Nhưng phải xác nhận trước**: nếu form thực tế có trả `''` khi người dùng clear select thì phải sửa **type** (`PhepTinhQuyDoi | '' | null`) chứ không phải bỏ điều kiện — bỏ nhầm sẽ khiến `isBlankQuyDoi` trả `false` cho dòng rỗng và mapper sẽ gửi rác lên server.

**F3. `MuaDichVuModal.tsx:124` — TS2322: truyền cả object token màu** ⚠️ **BUG**

```ts
color: r.strong ? ACCOUNTING_COLOR : TEXT.main,
```

`ACCOUNTING_COLOR` (`src/base/theme/semanticTokens.ts`) là **object** `{ amountNegative, totalPositive, preTaxEmphasis, posted, pending, deltaNegative, deltaPositive }`, không phải chuỗi màu. Hiện tại CSS `color` đang nhận `[object Object]` → dòng "strong" trong bảng tổng **đang mất màu**.

→ Sửa: chọn đúng token con. Đối chiếu Figma để quyết định — nhiều khả năng là `ACCOUNTING_COLOR.totalPositive` (dòng tổng) hoặc `ACCOUNTING_COLOR.preTaxEmphasis` (dòng trước thuế). **Cần người có thiết kế xác nhận.**

**F4. TS2349** (2 lỗi, trong test) — gộp vào Nhóm G.

---

### Nhóm G — `noUncheckedIndexedAccess` trong file test (124 lỗi)

**Nguyên nhân.** `tsconfig.app.json` bật `noUncheckedIndexedAccess: true` → mọi truy cập index/destructure mảng cho ra `T | undefined`. Test dùng mẫu này rất nhiều:

```ts
const [ma, ten, soNgay, thoiHan, tyLe, trangThai] = fields
expect(ma.uppercaseCode).toBe(true)   // ← TS18048: 'ma' is possibly 'undefined'
```

**Cách sửa (khuyến nghị).** Thêm một helper assert dùng chung, đặt ở `src/test/`:

```ts
// src/test/at.ts
/** Lấy phần tử theo index và khẳng định nó tồn tại — thay cho `!` rải rác trong test. */
export function at<T>(arr: readonly T[], index: number): T {
  const item = arr[index]
  if (item === undefined) throw new Error(`Expected element at index ${index}, got undefined`)
  return item
}
```

rồi đổi `const [ma, ten] = fields` → `const ma = at(fields, 0)`, hoặc gọn hơn cho khối destructure:

```ts
export function take<T, N extends number>(arr: readonly T[], n: N): T[] { ... }
```

> Không dùng `!` hàng loạt: nó im lặng khi index sai và làm test báo lỗi khó hiểu. Helper `at()` fail sớm với thông báo rõ ràng.

**Phân bố (số lỗi / file):**

| File | Lỗi |
|---|---|
| `danhMuc/chungTuThanhToan/dieuKhoanThanhToan/test/columns.test.ts` | 19 |
| `danhMuc/nganHangTienTe/nganHang/test/columns.test.ts` | 14 |
| `danhMuc/chungTuThanhToan/lyDoTangGiam/test/catalogConfig.test.tsx` | 14 |
| `danhMuc/doiTuong/nhomKhNcc/test/catalogConfig.test.tsx` | 13 |
| `danhMuc/vatTuHangHoa/donViTinh/test/columns.test.ts` | 11 |
| `danhMuc/nganHangTienTe/loaiTien/test/columns.test.ts` | 10 |
| `danhMuc/kho/nhomKho/test/columns.test.ts` | 9 |
| `danhMuc/chungTuThanhToan/mauSoHoaDon/test/catalogConfig.test.tsx` | 8 |
| `danhMuc/vatTuHangHoa/vatTu/test/columns.test.ts` | 6 |
| `danhMuc/doiTuong/chucDanh/test/catalogConfig.test.tsx` | 6 |
| `base/domainKit/catalog/test/catalogTree.test.ts` | 6 |
| `muaHang/chungTuMuaHang/muaDichVu/test/grid.test.ts` | 5 |
| `danhMuc/nganHangTienTe/taiKhoanNganHang/test/columns.test.ts` | 3 |
| `danhMuc/doiTuong/nhomKhNcc/test/api.test.ts` | 2 |
| `danhMuc/chiPhiCongTrinh/doiTuongTapHopChiPhi/test/catalogConfig.test.tsx` | 2 |
| `base/components/fields/test/CommonDatePicker.test.tsx` | 2 |

**Phương án thay thế (KHÔNG khuyến nghị):** tách `tsconfig.test.json` nới `noUncheckedIndexedAccess` cho `**/test/**` và loại test khỏi build. Nhanh hơn nhiều nhưng đánh mất một lớp an toàn kiểu và làm lệch cấu hình giữa test/source. Chỉ dùng nếu cần build gấp, và phải mở ticket trả nợ.

---

### Nhóm H — Lint (5 lỗi)

**H1. `CommonSlider.tsx:59` — `react-hooks/rules-of-hooks`** ⚠️ **BUG RUNTIME THẬT**

```ts
export function CommonSlider(props: CommonSliderProps) {
  ...
  if (!showInputNumber) {
    return <Slider ... />          // ← early return
  }
  ...
  const [inner, setInner] = useState<number>(defaultValue ?? min)   // ← dòng 59, sau early return
```

`useState` bị gọi có điều kiện. Nếu `showInputNumber` đổi giá trị giữa các lần render, React sẽ lệch thứ tự hook → crash hoặc state hỏng.

→ **Cách sửa:** tách thành 2 component riêng, giữ hook trong nhánh có hook:

```tsx
export function CommonSlider(props: CommonSliderProps) {
  if (!props.showInputNumber) return <PlainSlider {...props} />
  return <SliderWithInput {...props} />
}
```

Đây là fix đúng: mỗi component có tập hook cố định, và union prop type vốn đã tách sẵn thành `CommonSliderPlainProps | CommonSliderWithInputProps`.

**H2. `CommonSlider.tsx:37`** — `_locale`, `_w` unused. Sau khi tách component ở H1, đoạn destructure này biến mất luôn.

**H3. `UiComboGrid.tsx:54`** — `toGridTrack` unused (trùng với Nhóm D).

**H4. `lint:boundaries` — `Quyen3TrucPage.tsx:90`**

```
error  Definition for rule 'react-hooks/exhaustive-deps' was not found
```

Đây là **lỗi cấu hình**, không phải vi phạm boundary. File có comment `eslint-disable react-hooks/exhaustive-deps`, nhưng `eslint.boundaries.config.js` không nạp plugin `react-hooks` nên ESLint không nhận ra tên rule.

→ **Cách sửa:** thêm `plugins: { 'react-hooks': reactHooks }` vào `eslint.boundaries.config.js`. Đừng xóa comment disable trong `Quyen3TrucPage.tsx` — nó đang cần cho `npm run lint`.

---

### Nhóm I — Test fail (9 test / 5 file)

Các test này **không chặn build** nhưng chặn checklist §5. Cần điều tra riêng — chưa xác định nguyên nhân.

| File | Test | Ghi chú |
|---|---|---|
| `app/router/test/Router.test.tsx` | route lazy **Kho** với crumbs + `.View` | 1 |
| | route lazy **Tài sản cố định** với crumbs + `.View` | 1 |
| `base/domainKit/catalog/test/catalog.test.tsx` | read-only clone + lưu inline edit | 1 |
| `base/domainKit/catalog/test/catalogGates.test.tsx` | dòng khóa vẫn có Đóng, không có Chỉnh sửa/Xóa | 1 |
| | `rowReadOnly` ẩn hẳn Edit/Delete | 1 |
| `banHang/.../chungTuBanHangModal.render.test.tsx` | không chép số CT / 2 ô ngày / cờ "Đã lập hóa đơn" | **timeout 5000ms** |
| | đổ nguyên bản ghi vào form khi xem chi tiết | **timeout 5000ms** |
| | (+ 2 test khác cùng file) | timeout |

**Hướng điều tra:**
1. Nhóm `chungTuBanHangModal` (4 test) đều là **timeout 5000ms**, không phải assert sai. Nghi vấn: modal chờ một query không bao giờ resolve (mock thiếu), hoặc `userEvent.setup()` + fake timer xung đột. Chạy riêng file với `--testTimeout=20000` để phân biệt "chậm thật" và "treo".
2. Nhóm `catalogGates` / `catalog` cùng chạm cơ chế `rowReadOnly` + detail modal → nhiều khả năng **một regression chung**, sửa một chỗ là hết cả 3.
3. `Router.test.tsx` (2 test) chỉ fail đúng 2 route lazy Kho + TSCĐ → nghi ngờ lazy import path hoặc permission key của 2 module này.

Chạy riêng để lấy diff assert:
```bash
cd client
npx vitest run src/base/domainKit/catalog/test/catalogGates.test.tsx --reporter=verbose
npx vitest run src/app/router/test/Router.test.tsx --reporter=verbose
npx vitest run src/features/banHang/chungTuBanHang/chungTu/test/chungTuBanHangModal.render.test.tsx --testTimeout=20000
```

---

## 3. Các điểm cần người quyết định (không tự sửa được)

| # | Vấn đề | Cần xác nhận |
|---|---|---|
| 1 | `MuaDichVuModal.tsx:124` — `ACCOUNTING_COLOR` là object | Dòng "strong" trong bảng tổng dùng token màu nào? (`totalPositive` / `preTaxEmphasis` / khác) — đối chiếu Figma |
| 2 | `vatTu/mapper.ts:38` — `phepTinh === ''` không bao giờ đúng | Form có trả `''` khi clear select không? Nếu có → sửa **type**; nếu không → bỏ điều kiện |
| 3 | `gridFields` / `gridTexts` thừa ở 2 modal | Là i18n chưa nối vào JSX (phải nối) hay tàn dư (xóa)? |
| 4 | Nhóm G | Sửa test bằng helper `at()` (đúng, ~124 chỗ) hay tách `tsconfig.test.json` (nhanh, mất an toàn kiểu)? |
| 5 | Nhóm C | Migrate hẳn 7 Tab sang `useServerListState` (đúng ý đồ thiết kế, diff rộng hơn) hay chỉ vá kiểu `string \| null` (diff hẹp)? |

---

## 4. Kiểm tra sau mỗi commit

```bash
cd client
npm run typecheck        # phải về 0 lỗi sau nhóm A–G
npm run lint             # phải về 0 lỗi sau nhóm H
npm run lint:boundaries  # phải về 0 lỗi sau H4
npm run test             # phải xanh sau nhóm I
npm run build            # cổng cuối — tsc + vite build
```

Sau nhóm 1–6 thì `npm run build` phải qua. Nhóm 7–9 là để đạt checklist §5 (`../conventions.md`), không chặn build.

---

## 5. Ghi chú tuân thủ quy ước

- **Luật 3 (không `any`, không `@ts-ignore`)** — mọi cách sửa ở trên đều không dùng `any`/`@ts-ignore`. Nhóm B dùng `as unknown as Record<string, unknown>` (cast 2 bước hợp lệ). Nhóm G dùng helper assert thay `!`.
- **Luật 2 (không hardcode text UI)** — khi xử lý `gridTexts`/`gridFields` ở Nhóm D, không được thay bằng chuỗi cứng; nếu nối i18n thì bổ sung key ở **cả** `vi.ts` và `en.ts`.
- **"Code cũ chỉ dọn trong phạm vi đang sửa"** — Nhóm C nếu chọn migrate `useServerListState` là mở rộng diff có chủ đích và có lý do (hook đã được trích sẵn cho đúng việc này); các nhóm còn lại giữ diff tối thiểu, không refactor lan.
