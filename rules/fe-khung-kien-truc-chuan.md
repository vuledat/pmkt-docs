# FE — Khung kiến trúc chuẩn cho một phiếu yêu cầu

Bản trích từ `../../client/src` (đo ngày 2026-08-11). Đây là **khung bắt buộc**: mọi phiếu yêu cầu
(feature / màn hình / API mới) làm ở frontend phải sinh ra đúng bộ artefact dưới đây, đúng vị trí,
đúng tên. Không có ngoại lệ cho "màn nhỏ".

**Module tham chiếu — bản chuẩn hoá ngày 2026-08-11:**
`../../client/src/features/banHang/chungTuBanHang`. Đây là module DUY NHẤT trong repo đủ chuẩn §3; dựng
màn mới thì mở nó ra đọc, đừng đi tìm mẫu khác.

SSOT chi tiết: [client/CLAUDE.md](../../client/CLAUDE.md) · luật tầng ép bằng máy ở
`../../client/eslint.boundaries.js`.

---

## 1. Bản đồ tầng — biết mình được viết ở đâu

```
src/
├── app/          TIER 4 · router · guard · layout · provider · i18n app
├── features/     TIER 3 · nghiệp vụ (nơi 90% phiếu yêu cầu đáp xuống)
├── base/         TIER 2 · design system            @base
│   └── domainKit/  TIER 2.5 · engine nghiệp vụ     @domain-kit
├── platform/     TIER 2 · http · auth · rbac · query · tenant · i18n · config
├── utils/        TIER 1 · kernel thuần             @core
└── legacy/       VÙNG KHOÁ — không đọc/tham khảo   @legacy
```

```
app → features → domain-kit → base / platform → core     import CHỈ đi xuống
base ⊄ platform và platform ⊄ base                       hai anh em, không gọi nhau
core không import gì của dự án
```

Alias bắt buộc (không `../../..` xuyên tầng): `@core`=`src/utils` · `@base` · `@platform` ·
`@domain-kit`=`src/base/domainKit` · `@features/*` · `@app/*` · `@test/*` · `@legacy/*`.

Ba lệnh cấm: import `axios` ngoài `src/platform/` · import `@app/*` từ tầng dưới ·
deep-import `antd/es/*`.

---

## 2. Cây thư mục chuẩn của một phiếu yêu cầu

```
features/<domain>/
├── routes.tsx                      ← route contribution, handle DATA-ONLY, eager → phải mỏng
├── _shared/                        ← CHỈ tạo khi domain đã có ≥2 module thật cần dùng chung
└── <module>/                       ← MỘT màn hình = MỘT module (§3)
```

**Một màn hình = MỘT module.** Không có tầng `<nhóm>` trung gian, không tách màn theo hành vi
(`danhSach/` · `themMoi/` · `chinhSua/` · `xemChiTiet/`). Popup Thêm / Sửa / Xem là **component của
cùng module**, nằm ở `components/` — nó dùng chung `types`, `constants`, `api`, `helpers`, i18n với
màn danh sách, tách ra chỉ đẻ thêm `_shared/` và một mớ `../../..`.

`_shared/` là cơ chế dùng chung **giữa các module có thật**, không phải cấu trúc dựng sẵn. Domain mới
chỉ có một màn → **không tạo `_shared/`**.

### 3. Cấu trúc chuẩn của `<module>/` — BẮT BUỘC

Áp cho cả `src/features/**` và `src/base/domainKit/**`.
Module tham chiếu: **`../../client/src/features/banHang/chungTuBanHang`** — đọc file đó trước khi dựng mới.

```
<module>/
├── index.ts          ← FILE DUY NHẤT ở gốc module. Cửa ra duy nhất, ngoài chỉ import qua đây
├── api/              I/O + hợp đồng Zod với BE          chungTuBanHangApi · model · queries · lookups · payload
├── components/       MỌI .tsx của màn — list, tab, popup Thêm/Sửa/Xem, panel con
├── constants/        constants.ts · paths.ts · permissions.ts
├── fields/           mô tả cột · ô lưới · option · badge · texts  +  types.ts
├── helpers/          hàm thuần BIẾT nghiệp vụ — không React, không mạng, không t()
├── hooks/            mọi state / effect / request
├── i18n/             vi.ts · en.ts · registerXxxI18n.ts  (MỘT namespace cho cả module)
├── pages/            <Tên>Page.tsx (chỉ ráp, không logic)  +  <tên>.css của màn
└── test/             mọi test của module
```

**Luật cứng — gốc module chỉ có ĐÚNG MỘT file: `index.ts`.** Không `Page.tsx`, không `types.ts`,
không `constants.ts`, không `.css`, không `paths.ts`/`permissions.ts` ở gốc. Thấy file thứ hai ở gốc
là sai chuẩn.

Lớp nào chưa có nội dung thì **không tạo thư mục rỗng** — luật là *"không có file lạc ra gốc"*,
không phải *"phải đủ 9 thư mục"*.

`kernel/` **không phải** lớp hợp lệ (dùng `helpers/`). `utils/` cấp màn hình cũng **không** — tiện ích
kỹ thuật thuần (format ngày/số/chuỗi) thuộc `@core`.

### 3.1 Bốn hệ quả phải nhớ

| Thứ | Ở đâu | Vì sao |
|---|---|---|
| `types.ts` | **`fields/types.ts`** | kiểu của module đi cùng nơi khai báo hình dạng dữ liệu hiển thị; `api/`, `helpers/`, `hooks/`, `components/` đều import xuống đây |
| `paths.ts` · `permissions.ts` | **`constants/`** | vẫn là hằng số. Ngoài module **deep-import thẳng**, KHÔNG qua `index.ts`: `@features/<domain>/<module>/constants/paths.ts` — giữ chunk eager của `routes.tsx` và menu shell không kéo theo page graph |
| CSS của màn | **`pages/<tên>.css`** | một module một stylesheet. Nhiều khối UI (danh sách + popup) thì tách bằng **tiền tố class** (`.pmkt-ctbh-*` vs `.pmkt-ctbh-tm-*`), không tách file |
| i18n | **`i18n/` — MỘT namespace** | chữ của popup là **nhánh con** trong cùng cây khóa (`themMoi.*`), không mở namespace thứ hai. Namespace thứ hai buộc phải có `vi.ts`/`en.ts` thứ hai → lại đẻ thư mục con |

### 3.2 File mới đặt đâu — cây quyết định (dừng ở dòng đầu tiên đúng)

```
Có JSX?                          → components/   (Page thì → pages/)
Có useState/useEffect/useQuery?  → hooks/
Gọi http?                        → api/
Trả về mô tả cột / ô / option?   → fields/
Công thức, luật, đổi shape A→B?  → helpers/
Là type / interface dùng chung?  → fields/types.ts
Chỉ là giá trị cố định?          → constants/constants.ts
```

### 3.3 Import trong module

- Cùng thư mục: `./<file>` — ví dụ `components/ChungTuBanHangTab.tsx` → `'./ChungTuBanHangListTable'`.
- Khác lớp: `../<lớp>/<file>` — ví dụ `helpers/anHien.ts` → `'../fields/types'`.
- Alias tuyệt đối `@features/<domain>/<module>/<lớp>/<file>` cũng hợp lệ (module tham chiếu dùng cho
  `constants/`).
- **TUYỆT ĐỐI không `../../..`.** Cây phẳng một bậc khiến `../../..` chỉ xuất hiện khi đặt file sai chỗ —
  gặp nó là dấu hiệu module đang bị tách sai.

### 3.4 Phân biệt 3 lớp dễ nhầm — hỏi "ai gõ cửa bắt sửa file này"

| Ai nói | Câu | Sửa ở |
|---|---|---|
| Designer | "cột này rộng thêm 20px" | `fields/` |
| Backend | "anh đổi tên trường JSON" | `api/` + `helpers/` |
| Kế toán / BA | "công thức thuế đổi rồi" | `helpers/` |

Một file phải sửa vì cả ba người nói → nó ôm ba việc, phải tách.

---

## 4. Trước khi gõ dòng đầu tiên — 4 câu hỏi bắt buộc trong phiếu

| # | Câu hỏi | Trả lời quyết định điều gì |
|---|---|---|
| 0 | **Code ở đâu?** | **Mọi PYC code mới → `src/features/`.** Không mở màn mới, không thêm tính năng mới ở `src/legacy/` (vùng khoá, §10) |
| 1 | Màn này thuộc loại nào? | **Danh mục** → `@domain-kit/catalog` · **Chứng từ** → `@domain-kit/chungTu` · **Báo cáo** → `@domain-kit/report` · **Khác** → `features/` theo §3. Cả 4 đều nằm trong `features/<domain>/` |
| 2 | Đã có engine chưa? | Có → **dùng descriptor, không viết lại khung**. Engine đã lo: tìm nhanh, phễu ngày, lọc nâng cao, phân trang/sort server-side, dòng tổng, cấu hình cột, panel chi tiết, confirm+toast+invalidate, máy trạng thái nút, chữ khung vi+en |
| 3 | Component đã có ở `@base` chưa? | ~130 component / 21 họ đã export qua barrel `@base`. Tra ở `src/base/index.ts` hoặc route `/__components` khi chạy dev. Thiếu prop nhỏ → **thêm prop vào `base`**, không copy ra feature |
| 4 | Màn định sửa có đang chạy không? | Kiểm **duy nhất** ở `app/router/RootRoutes.tsx`. Domain không nằm trong cây route = nhánh chết → không sửa, không lấy làm mẫu, không import. Đang chạy (2026-08-08): `banHangBackup` · `heThong` · `muaHang` · `tienGui` · `tienMat`. **`features/danhMuc` là nhánh chết** (`/danh-muc/*` do legacy phục vụ) |

---

## 5. Bộ artefact tối thiểu của một phiếu — checklist sinh file

| # | Artefact | Đường dẫn | Bắt buộc |
|---|---|---|---|
| 1 | Hợp đồng BE (Zod schema + hàm gọi) | `<module>/api/` | ✅ |
| 2 | Kiểu dùng chung | `<module>/fields/types.ts` | ✅ |
| 3 | Hằng số nghiệp vụ (không magic value) | `<module>/constants/constants.ts` | ✅ |
| 4 | Cột / ô lưới / option / badge | `<module>/fields/` | ✅ nếu có grid/form |
| 5 | Logic nghiệp vụ thuần | `<module>/helpers/` | ✅ nếu có công thức/luật |
| 6 | State & request | `<module>/hooks/` | ✅ |
| 7 | Component riêng của màn (kể cả popup Thêm/Sửa/Xem) | `<module>/components/` | ✅ nếu có UI riêng |
| 8 | Entry màn hình + CSS của màn | `<module>/pages/` | ✅ |
| 9 | i18n `vi` + `en` + register (MỘT namespace) | `<module>/i18n/` | ✅ |
| 10 | Cửa ra | `<module>/index.ts` | ✅ (file DUY NHẤT ở gốc) |
| 11 | Test | `<module>/test/` | ✅ |
| 12 | Mã quyền | `<module>/constants/permissions.ts` | ✅ |
| 13 | Đường dẫn | `<module>/constants/paths.ts` | ✅ |
| 14 | Route + `handle` (perm, crumbKeys) | `features/<domain>/routes.tsx` | ✅ |
| 15 | Nối tay vào cây route | `app/router/RootRoutes.tsx` | ✅ (không có cơ chế tự nạp) |

`mock.ts` chỉ tồn tại khi API chưa sẵn sàng — **còn `mock.ts` = còn nợ**, phải gỡ khi nối API thật.

---

## 6. Khung code mẫu (copy làm sườn)

### 6.1 `routes.tsx` — eager, phải mỏng

```tsx
import type { RouteObject } from 'react-router-dom'
import type { PermissionKey } from '@platform'
import { XXX_PATHS } from '@features/<domain>/<module>/constants/paths.ts'
import { XXX_PERM } from '@features/<domain>/<module>/constants/permissions.ts'

export interface XxxRouteHandle {
  perm: PermissionKey            // app/router tự bọc <RequirePermission>
  crumbKeys: string[]            // khoá i18n breadcrumb, cha → con
}

export const xxxRoutes: RouteObject[] = [
  {
    path: XXX_PATHS.manHinh,
    handle: { perm: XXX_PERM.view, crumbKeys: ['app:shell.menu.xxx', 'xxx:menu.manHinh'] },
    lazy: async () => ({ Component: (await import('./<module>')).XxxPage }),
  },
]
```

Cấm: import guard của `app`, import page graph (chỉ type + deep-import `constants/paths`/`constants/permissions`).

### 6.2 `api/` — parse Zod, không ép kiểu

```ts
import { z } from 'zod'
import { http } from '@platform'

export const xxxRowSchema = z.object({ id: z.string(), soChungTu: z.string() })
export type XxxRow = z.infer<typeof xxxRowSchema>

export async function layDanhSach(params: XxxSearchParams): Promise<XxxRow[]> {
  const res = await http.get('/api/xxx/search', { params })
  return z.array(xxxRowSchema).parse(res.data.data)   // ApiResponse<T> → .data
}
```

### 6.3 `i18n/registerXxxI18n.ts` — side-effect, idempotent

```ts
import { addTranslations } from '@platform'
import { xxxVi } from './vi.ts'
import { xxxEn } from './en.ts'

export const XXX_NS = 'xxx'

addTranslations('vi', XXX_NS, xxxVi)
addTranslations('en', XXX_NS, xxxEn)
```

Namespace phải đi cùng chunk lazy của màn (Page side-effect import file này) — nhét chữ nghiệp vụ
vào ns của `app` là sai, phá lazy-chunk.

### 6.4 `index.ts` — cửa ra duy nhất, và là FILE DUY NHẤT ở gốc module

```ts
export { XxxPage } from './pages/XxxPage.tsx'
export type { XxxRow } from './fields/types.ts'
```

Ngoài module chỉ import qua barrel. Ngoại lệ deep-import **cố ý**: `constants/paths.ts` và
`constants/permissions.ts` (giữ chunk eager không kéo page graph).

### 6.5 `i18n/vi.ts` — một module, một namespace, popup là nhánh con

```ts
export const xxxVi = {
  menu: { … },          // chữ của màn danh sách nằm ở gốc cây khóa
  list: { … },

  /** Popup Thêm/Sửa/Xem — nhánh riêng để không đụng khóa của màn danh sách. */
  themMoi: {
    tabs: { … },        // `t('xxx:themMoi.tabs.hoaDon')`
  },
}
```

Hai từ điển `vi`/`en` phải khớp khóa 1-1. **Không** mở namespace thứ hai cho popup — namespace thứ hai
kéo theo cặp `vi.ts`/`en.ts` thứ hai, và đó chính là thứ đẻ ra thư mục con.

---

## 7. Luật cứng áp cho mọi phiếu

1. **Không hardcode magic value** — mọi số/chuỗi nghiệp vụ là constant có tên, đặt gần nơi dùng nhất.
2. **Không hardcode text UI** — mọi chuỗi người dùng thấy có key i18n ở **cả** `vi.ts` và `en.ts`.
   Chuỗi động dùng interpolation `t('key', { name })`, không cộng chuỗi.
   Key phân tầng `<module>.<màn hình>.<thành phần>`.
   *Ngoại lệ có chủ đích:* chữ pháp định tiếng Việt trên chứng từ in (mẫu số, chức danh ký, câu thông
   tư) là **hằng số**, không phải chuỗi i18n.
3. **Không `any`, không `@ts-ignore`** — dùng `unknown` + type guard, hoặc Zod parse.
   Mọi dữ liệu từ ngoài vào (API, `localStorage`, query param, postMessage) **phải Zod parse**.
   ⚠ Lint để `no-explicit-any` ở mức `warn` → lint xanh **không** chứng minh là sạch, phải tự soát.
4. **Import bằng alias**, chỉ đi xuống tầng dưới, qua barrel công khai.
5. **TS đang bật**: `strict` · `noUncheckedIndexedAccess` · `erasableSyntaxOnly` (**không** `enum`,
   **không** `namespace`) · `verbatimModuleSyntax` (`import type`) · `noUnusedLocals/Parameters`.
6. **Đặt tên**: `.tsx` PascalCase · `.ts` camelCase · thư mục camelCase · constant
   SCREAMING_SNAKE_CASE · hook `useXxx` · prop `onXxx` / handler `handleXxx` · ưu tiên named export.
   Ngoại lệ: `.tsx` không export component (`routes.tsx`, `columns.tsx`) giữ camelCase.
7. **Không tự commit / push / checkout / stash / reset.** Đổi tên file dùng `git mv`.

---

## 8. Quy chuẩn nghiệp vụ (BR) phải đối chiếu

Mọi phiếu phải code theo [pmkt-docs/ba/Common/business_rules.md](../../pmkt-docs/ba/Common/business_rules.md).
Epic chỉ mô tả phần đặc thù; phần chung **mặc định lấy theo BR**. Epic không nhắc BR ≠ được bỏ BR.

| Phạm vi phiếu | BR phải đọc |
|---|---|
| Màn danh sách (grid) | BR1 · BR2 · BR11 · BR13.1 · BR30 · BR31 · BR32 · BR38 · BR39 · BR44 · BR45 |
| Danh mục dạng cây | BR2 · BR22 · BR40 · BR23 |
| Form / popup | BR3 · BR13.2 · BR14 · BR15 · BR24 · BR34 · BR43 |
| Combogrid / chọn dữ liệu | BR5 · BR6 · BR10 |
| Chứng từ & hạch toán | BR4 · BR9 · BR12 · BR17 · BR33 · BR36 · BR37 · BR41 · BR42 |
| Số liệu / tiền tệ | BR7 · BR18 |
| Ngày tháng / kỳ | BR8 |
| Thông báo & cảnh báo | BR16 · BR26 · BR27 |
| Entity / API | BR7 · BR19 · BR20 · BR28 · BR29 · BR46 |
| Quyền | BR25 |
| Grid chi tiết con | BR21 |

Text theo BR vẫn đi qua i18n — giữ **nguyên văn tiếng Việt** của BR làm giá trị trong `vi.ts`.

---

## 9. Cổng nghiệm thu (DoD) — chạy trước khi báo hoàn thành

```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test && npm run build
```

Repo **đỏ sẵn** (baseline đo lại 2026-08-11): `typecheck` **193 lỗi** (đa số ở `features/danhMuc` —
nhánh chết, rồi `muaHang`, `tienMat`, `domainKit`) · `lint` **10 lỗi + 2 warning** ·
`lint:boundaries` **76** (74 "rule not found" + **2 vi phạm thật**: `axios` trần trong `legacy`).

Luật nghiệm thu:

1. **Không làm xấu hơn baseline** — không lệnh nào được tăng số lỗi.
2. **File mình chạm phải sạch** — 0 lỗi typecheck, 0 lỗi lint trên file đó.
3. **Không sinh vi phạm tầng mới** — `boundaries/*` và `no-restricted-imports` giữ nguyên mức nợ cũ (2).
4. **Không dùng `eslint-disable` để dập lint** — mỗi comment disable là thêm một lỗi ở cổng này.
5. Lệnh nào fail thì **dán output thật**, không báo "đã xong".
6. Báo cáo hoàn thành phải **liệt kê BR đã áp dụng** và BR chưa đạt (kèm lý do).

---

## 10. Vùng cấm

| Vùng | Luật |
|---|---|
| `cell-app/**/master_data/**` | Không đọc để tham khảo, không sao chép kiến trúc, không dùng làm mẫu. Deny cứng ở `../../.claude/settings.json` |
| **`../../client/src/legacy` — VÙNG KHOÁ** | ✗ **Không đọc** để tham khảo (grep toàn repo thì bỏ qua kết quả rơi vào đây) · ✗ **Không sao chép** kiến trúc / pattern / code · ✗ **Không dùng làm mẫu** cho màn mới, kể cả màn danh mục · ✗ **Không sửa** khi user chưa cho phép trực tiếp cho đúng lần đó · ✗ Không thêm tính năng mới, không mở màn mới |
| `src/legacy/` khi ĐÃ được cho phép sửa | Chỉ vá lỗi màn đang chạy, không mở rộng diff. Đi qua `@platform`, cấm `axios` trần. Test đặt cạnh file nguồn (`<Tên>.rules.test.ts`). Báo rõ cho user là đang chạm vùng khoá |
| Shape phẳng cũ (`XxxTab.tsx` + `api/columns/model/queries/mock` ở gốc) | Không mở module mới theo shape này |
| Shape tách theo hành vi (`danhSach/` · `themMoi/` · `_shared/` cho MỘT màn) | Không mở module mới theo shape này — §2. Đây là shape `chungTuBanHang` đã gỡ ngày 2026-08-11 |
| Nhánh `features/` đã chết (không có trong `RootRoutes.tsx`) | Không sửa, không lấy làm mẫu, không import |

**Nợ hiện tại (đo 2026-08-11)** — module đủ lớp §3: `features` **1/47** · `domainKit` **0/6**
(`chungTu` gần nhất nhưng còn `kernel/` + 3 file lạc ở gốc).

**Mẫu DUY NHẤT được phép copy: `../../client/src/features/banHang/chungTuBanHang`.** Mọi module khác trong
`features/` đều chưa đạt chuẩn — không lấy cái khác làm mẫu, kể cả khi nó cũng là màn chứng từ.

Nợ kèm theo: 9 `mock.ts` · 413 import `../../..` xuyên tầng (133 chỗ đáng lẽ là `@domain-kit`) ·
14 chỗ `any` ngoài legacy.

Luật áp **từ nay về sau**: module mới đủ chuẩn; module cũ chuyển dần khi có việc chạm vào.
Không mở đợt refactor toàn bộ nếu không được giao.
