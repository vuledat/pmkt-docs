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
cùng module**, nằm ở `components/modal/` (§3 luật cứng 4) — nó dùng chung `types`, `constants`, `api`,
`helpers`, i18n với màn danh sách, tách ra chỉ đẻ thêm `_shared/` và một mớ `../../..`.

`_shared/` là cơ chế dùng chung **giữa các module có thật**, không phải cấu trúc dựng sẵn. Domain mới
chỉ có một màn → **không tạo `_shared/`**. Khi đã có ≥2 module: chữ dùng chung của chúng đặt ở
`<domain>/_shared/i18n/`, chữ riêng vẫn ở `<module>/i18n/`.

### 3. Cấu trúc chuẩn của `<module>/` — BẮT BUỘC

Áp cho cả `src/features/**` và `src/base/domainKit/**`.
Module tham chiếu: **`../../client/src/features/banHang/chungTuBanHang`** — đọc file đó trước khi dựng mới.

```
<module>/
├── index.ts          ← FILE DUY NHẤT ở gốc module. Cửa ra duy nhất, ngoài chỉ import qua đây
├── api/              I/O + hợp đồng Zod với BE          chungTuBanHangApi · model · queries · lookups · payload
├── components/       MỌI .tsx của màn — list, tab, panel con
│   └── modal/        MỌI popup (Thêm / Sửa / Xem / xác nhận / chọn nguồn) — thư mục con DUY NHẤT được phép
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

**Luật cứng — popup nằm ở `components/modal/`**, thư mục con **DUY NHẤT** được phép trong
`components/`. Một màn thường có 1 list + 3-5 popup; để phẳng hết thì thân màn chìm nghỉm. KHÔNG mở
thêm `tabs/`, `panels/`, `common/`… — ranh giới của chúng mờ hơn ranh giới "có phải popup không".

`kernel/` **không phải** lớp hợp lệ (dùng `helpers/`) — engine `chungTu` đã đổi sang `helpers/`, thấy
`kernel/` ở đâu là code chưa chuyển. `utils/` cấp màn hình cũng **không** — tiện ích kỹ thuật thuần
(format ngày/số/chuỗi) thuộc `@core`; dùng ≥2 màn thì đẩy lên `@core`, chỉ 1 file dùng thì để private
trong chính file đó.

⚠ **Nợ hiện tại:** `chungTuBanHang` là module DUY NHẤT đạt chuẩn này — 46 module `features/` và 6 engine
`domainKit/` còn lại đều **chưa** đạt, đừng lấy cái khác làm mẫu. Bản thân nó cũng đang chuyển dở
`components/modal/` (2 modal còn phẳng ở `components/`). Còn **9 `mock.ts`** và 14 namespace i18n nằm sai
chỗ — số liệu ở [`fe-no-ky-thuat-va-su-co.md §A`](fe-no-ky-thuat-va-su-co.md). Luật áp **từ nay về sau**:
module mới phải đủ chuẩn, module cũ chuyển dần khi có việc chạm vào; không mở đợt refactor toàn bộ nếu
không được giao.

### 3.1 Năm hệ quả phải nhớ

| Thứ | Ở đâu | Vì sao |
|---|---|---|
| `types.ts` | **`fields/types.ts`** | kiểu của module đi cùng nơi khai báo hình dạng dữ liệu hiển thị; `api/`, `helpers/`, `hooks/`, `components/` đều import xuống đây |
| `paths.ts` · `permissions.ts` | **`constants/`** | vẫn là hằng số. Ngoài module **deep-import thẳng**, KHÔNG qua `index.ts`: `@features/<domain>/<module>/constants/paths.ts` — giữ chunk eager của `routes.tsx` và menu shell không kéo theo page graph |
| Popup | **`components/modal/`** | luật cứng 4 — thư mục con duy nhất được phép trong `components/` |
| CSS của màn | **`pages/<tên>.css`** | một module một stylesheet. Nhiều khối UI (danh sách + popup) thì tách bằng **tiền tố class** (`.pmkt-ctbh-*` vs `.pmkt-ctbh-tm-*`), không tách file |
| i18n | **`i18n/` — MỘT namespace** | chữ của popup là **nhánh con** trong cùng cây khóa (`themMoi.*`), không mở namespace thứ hai. Namespace thứ hai buộc phải có `vi.ts`/`en.ts` thứ hai → lại đẻ thư mục con |

### 3.2 File mới đặt đâu — cây quyết định (dừng ở dòng đầu tiên đúng)

```
Có JSX?                          → components/   (popup → components/modal/ · Page → pages/)
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

## 7. Luật cứng · BR · cổng nghiệm thu · vùng cấm — KHÔNG lặp lại ở đây

Bốn mục này từng được chép lại trong file này và **đã lệch khỏi bản gốc** (cổng nghiệm thu ở đây còn
giữ bộ lệnh nặng đã bị bãi bỏ 2026-08-13; bảng BR còn thiếu BR35 và BR47–49). Từ nay đọc thẳng bản gốc:

| Cần gì | Bản gốc (SSOT) |
|---|---|
| Luật cứng (hardcode · i18n · `any` · alias · commit · phân trang) | [`CLAUDE.md` §8 luật](../../CLAUDE.md) |
| Chi tiết FE của các luật đó (TS đang bật · đặt tên · i18n) | [`client/CLAUDE.md`](../../client/CLAUDE.md) §8 §10 §11 |
| BR phải đối chiếu + cách trích | [`CLAUDE.md` §BR](../../CLAUDE.md) → `./docs/rules/br.sh <số BR>` |
| Cổng nghiệm thu FE | [`fe-cong-nghiem-thu.md`](fe-cong-nghiem-thu.md) — cổng nhẹ `npx vite build`, **KHÔNG** `npm run build` |
| Luật test FE | [`fe-test-va-toc-do-suite.md`](fe-test-va-toc-do-suite.md) |
| Vùng cấm (`master_data/**`, `src/legacy/**`) | [`CLAUDE.md` §Vùng đóng băng](../../CLAUDE.md) · [`client/CLAUDE.md` §9](../../client/CLAUDE.md) |

Hai điều **riêng của phiếu FE**, không có ở nơi khác:

1. Báo cáo hoàn thành phải **liệt kê BR đã áp dụng** và BR chưa đạt (kèm lý do).
2. *Ngoại lệ i18n có chủ đích:* chữ pháp định tiếng Việt trên chứng từ in (mẫu số, chức danh ký, câu
   thông tư) là **hằng số**, không phải chuỗi i18n.
