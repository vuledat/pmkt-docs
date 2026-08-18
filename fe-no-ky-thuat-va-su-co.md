# FE — nợ kỹ thuật đang đếm được & hai sự cố đã trả giá

Tách khỏi `client/CLAUDE.md` (2026-08-14) để file rule chỉ còn LUẬT. Đây là **số liệu trạng thái**
(mục nhanh, kiểm lại trước khi trích) và **bằng chứng** cho các luật tương ứng.

## A. Nợ hiện tại — đo 2026-08-11

| Vùng | Đã theo chuẩn | Chưa chuyển |
|---|---|---|
| `src/features/**` (47 module có `…Page.tsx`/`…Tab.tsx`) | **1** — `banHang/chungTuBanHang` | **46** |
| `src/base/domainKit/**` (6 engine) | **0** (`chungTu` gần chuẩn, còn `kernel/` + 3 file lạc ở gốc) | **6** |

**Mẫu DUY NHẤT được phép nhân bản: `features/banHang/chungTuBanHang/`.** 46 module còn lại đều chưa
đạt — không lấy cái khác làm mẫu, kể cả khi nó cũng là màn chứng từ hay màn danh mục.

Nợ đi kèm còn đếm được: **9 `mock.ts`** trong `features/` (mỗi cái là một màn chưa nối API thật).

Luật áp **từ nay về sau**: module mới phải đủ chuẩn; module cũ chuyển dần khi có việc chạm vào. Không mở
đợt refactor toàn bộ nếu không được giao — 52 module là việc lớn, phải lên kế hoạch riêng.

`i18n/` cấp module hiện **chỉ `chungTuBanHang` có** (14 namespace còn lại đang nằm ở
`<nhóm>/_shared/i18n/`). Module mới tạo `i18n/` riêng; module cũ giữ nguyên tới khi chuyển.

## B. Thí nghiệm `test.projects` thất bại — 2026-08-13

Đã thử và đã hoàn tác (2026-08-13). Tách hai project `node`/`dom` trong `vite.config.ts` làm:
full suite **202s → 375s** (mỗi project mở pool worker riêng → 12 worker trên 8 core, CPU 311%,
timeout 5s hàng loạt: 11 → 56 test đỏ), và **hỏng bộ lọc theo đường dẫn** —
`npx vitest run src/features/tongHop/khoaSo` trả "no tests", phải viết
`npx vitest run --project dom <path>` mới chạy. Docblock ở §13.1 cho cùng lợi ích mà không mất gì.

## C. Sự cố "xanh local, đỏ deploy" — file mới quên `git add`

`typecheck` · `lint` · `test` · `build` đều chạy trên **working tree**, nơi file mới vẫn nằm trên đĩa
dù chưa `git add`. CI (`deploy/.github/workflows/build-deploy.yml`) thì
`git reset --hard origin/<branch>` rồi build trên **cây commit**. Chênh lệch đó tạo ra một lớp lỗi
**xanh 100% ở máy local, đỏ 100% ở deploy**:

```
[UNRESOLVED_IMPORT] Could not resolve './components/fields/CommonTimeInput' in src/base/index.ts
```

(sự cố thật: `src/base/index.ts` được commit kèm dòng `export … from './components/fields/CommonTimeInput'`
nhưng `CommonTimeInput.tsx` chưa được `git add` — build deploy đỏ ngay ở bước transform.)

**Luật:**

1. **Thêm file mới thì `git add` chính file đó TRƯỚC, rồi mới sửa barrel/`index.ts` trỏ tới nó.**
   Thứ tự ngược lại là cách sinh ra đúng lỗi trên.
2. **Sau mỗi commit đụng `client/`, chạy `npm run check:committed`** — script duyệt đúng cây commit
   (`git ls-tree`, `git cat-file`) và kiểm mọi import/export tương đối trong `src/` có resolve được về
   file **cũng nằm trong cây commit** hay không. ~0,7 giây, không cần `node_modules`.
   Kiểm nhánh đã đẩy lên: `npm run check:committed -- origin/<branch>`.
3. **`git status` phải sạch trước khi báo hoàn thành hoặc trước khi push.** Còn dòng `??` nào trong
   `src/` là còn nguy cơ đúng lỗi này — script in kèm danh sách đó để soát.
4. Đây cũng là lý do **không đổi barrel `src/base/index.ts` chung một commit với việc tạo component
   mới rồi push vội** — barrel là điểm gãy tập trung: một dòng export hỏng làm đỏ toàn bộ app
   (`src/base/index.ts` → `switchOverlay.ts` → `main.tsx` → `index.html`).

## D. Số đo môi trường test — vì sao có luật docblock `node` (2026-08-13)

Vitest dựng **một jsdom riêng cho TỪNG file test** (~5s/file), trong khi phần chạy test thật của nhóm
logic thuần chỉ tính bằng mili-giây. A/B trên đúng 116 file logic thuần của repo, chạy liền nhau:

| | Thời gian | `environment` cộng dồn | `tests` cộng dồn | Kết quả |
|---|---|---|---|---|
| jsdom (mặc định) | **28,1s** | 102,5s | 1,24s | 116 file / 1381 test xanh |
| `// @vitest-environment node` | **14,5s** | 11ms | 1,20s | 116 file / 1381 test xanh |

Không file nào đỏ thêm. Sau khi áp: **162/174** file `.test.ts` ngoài legacy khai `node`; 12 file còn
lại thật sự cần DOM (`switchOverlay` · `i18n` · `tenantStore` · `exportReportXlsx` · `tokenVault` ·
`registry` · `motionPreference` · `columnConfig` · `stickyHaiTang` · `checkboxColors` · `isolation` ·
`dieuKhoanThanhToan/columns`).

Chi phí lớn thứ hai của suite là `import` (955s cộng dồn) — do test import barrel `@base`. Đó là lý do
có luật "không import barrel trong test" ở `client/CLAUDE.md §13.3`.

## E. Sự cố CSS làm đỏ bundle — 2026-08-13

`khoaSo.css` có comment chứa chuỗi `**13**/22`; cụm `*/` bên trong đóng comment CSS sớm, phần còn
lại thành selector rỗng. Hệ quả kép: `lightningcss` chết ở bước minify (`Invalid empty selector`)
nên `vite build` đỏ, VÀ trình duyệt nuốt luôn rule `.pmkt-khoa-so-ht` ngay sau đó nên thanh công cụ
màn Khoá sổ vỡ bố cục lúc chạy dev. Bài học: `npx vite build` (2,3s) là cổng duy nhất bắt được lớp
lỗi này — `npm run build` không tới được bước đó vì `tsc -b` đỏ trước.
