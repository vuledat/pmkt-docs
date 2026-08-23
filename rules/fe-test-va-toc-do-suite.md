# FE — Test và tốc độ suite

> Tách khỏi `client/CLAUDE.md` để file rule chính nhẹ hơn. Nội dung giữ **nguyên văn**.
> Đọc khi đụng đúng vùng này, không đọc trước.

## 13. Test

- Đặt trong thư mục `test/` cạnh code. Legacy theo lệ riêng (§9).
- Vitest gom `src/**/*.{test,spec}.{ts,tsx}`, môi trường **mặc định jsdom**, setup `src/test/setup.ts`.
- Render kèm provider thật → `renderWithProviders` từ `@test`.

### 13.1 LUẬT CỨNG — test logic thuần phải khai `// @vitest-environment node`

**Dòng đầu tiên** của mọi `*.test.ts` không chạm DOM:

```ts
// @vitest-environment node
```

Vitest dựng **một jsdom riêng cho TỪNG file**, ~5s/file. Đo trên 116 file logic thuần của repo:
**28,1s → 14,5s**, chi phí `environment` 102,5s → 11ms (chi tiết: `docs/rules/fe-no-ky-thuat-va-su-co.md §D`).

- File `.ts` thử hàm thuần / mapper / schema Zod / cột / payload / hằng số → **luôn** khai `node`.
- File `.tsx`, hoặc `.ts` có `render()` · `document` · `window` · `localStorage` · `matchMedia` ·
  `ResizeObserver` · `@testing-library/*` → **không** khai, để mặc định jsdom.
- Không chắc → cứ khai `node` rồi chạy file đó; đỏ vì thiếu DOM thì gỡ dòng đó ra.

Hiện **162/174** file `.test.ts` ngoài legacy đã khai `node`; 12 file còn lại thật sự cần DOM — đừng
"dọn" nốt.

### 13.2 Chạy test — hẹp trước, toàn suite sau

```bash
npx vitest run src/features/<domain>/<module> --reporter=dot   # ~30-60s — mặc định khi đang code
npx vitest related --run <file lá vừa sửa> --reporter=dot       # CHỈ cho file lá
npx vitest run --exclude 'src/legacy/**' --reporter=dot         # toàn suite ~4,5 phút, một lần ở cuối
```

- **Luôn `--reporter=dot`** — reporter mặc định in hàng nghìn dòng.
- ⚠ **Không `related` trên file dùng chung** (`index.ts`, `@base`, `@core`, i18n gốc): đo thực tế
  `related --run src/utils/index.ts` kéo **217 file, 3 phút 54**.
- Suite flaky khi chạy song song → chạy test của file mình sửa, đừng chạy `npm run test` trần rồi
  kết luận mình làm hỏng.

### 13.3 Viết test sao cho suite không chậm thêm

- **Không import barrel trong test** — `from '@base'` kéo 290 dòng export (~219 component + antd +
  exceljs + recharts) vào mọi worker; đây là chi phí `import` lớn nhất của suite. Import đường dẫn cụ thể.
- Logic thuần test bằng `.test.ts` + `node`, **đừng** test lại qua `render()` một màn hình.
- Chỉ `render()` cho `components/` và `pages/`.
