# FE — Cổng kiểm tra trước khi báo hoàn thành

> Tách khỏi `client/CLAUDE.md` để file rule chính nhẹ hơn. Nội dung giữ **nguyên văn**.
> Đọc khi đụng đúng vùng này, không đọc trước.

## 15. Cổng kiểm tra trước khi báo hoàn thành

Cổng mặc định là **cổng nhẹ** — ~3,5 giây cộng thời gian test của đúng module đang sửa:

```bash
npx vitest run src/features/<domain>/<module> --reporter=dot   # ~30-60s
npx vite build                                                  # ~2,3s
npm run check:committed                                         # ~1,2s — chỉ khi có commit
```

⚠ **`npx vite build`, KHÔNG phải `npm run build`.** `npm run build` chạy `tsc -b` trước và luôn đỏ ở
192 lỗi nền → **chưa bao giờ chạy tới bước bundle**. `npx vite build` mới đúng thứ CI dựng, và là thứ
bắt được sự cố CSS 2026-08-13 (`docs/rules/fe-no-ky-thuat-va-su-co.md §E`).

### 15.0 Bốn lệnh nặng — KHÔNG chạy mặc định (user chốt 2026-08-13)

`npm run typecheck` (~55s, nền 192 lỗi) · `npm run lint` (~60s, nền 9+2) · `npm run lint:boundaries`
(~60s, nền 76) · `npx vitest run --exclude 'src/legacy/**'` (~4,5 phút, nền 16 test đỏ / 370 file).

Chỉ chạy khi **user yêu cầu**, hoặc khi vừa đụng đúng vùng chúng canh:

| Vừa làm gì | Chạy thêm |
|---|---|
| đụng `src/base/index.ts` hoặc barrel bất kỳ | `typecheck` |
| thêm import xuyên tầng / alias mới | `lint:boundaries` |
| sửa `@base` hoặc engine `@domain-kit` dùng chung | full suite |
| chuẩn bị mở PR / release | cả bốn |

Khi chạy: ba lệnh đầu độc lập → phát **3 tool call Bash song song**, đừng nối `&&`. Full suite cần
**timeout ≥ 25 phút**.

⚠ **CI không gánh hộ** — `deploy/.github/workflows/build-deploy.yml` chỉ dựng bundle, không
typecheck/lint/test. Bỏ bốn lệnh trên nghĩa là lỗi kiểu và hồi quy ngoài module đang sửa **không còn
lưới nào bắt**; đó là đánh đổi có chủ ý.

**Luật:**

1. **Không làm xấu hơn baseline** — không lệnh nào được tăng số lỗi so với số nền ở trên.
2. **File bạn chạm phải sạch** — 0 lỗi typecheck, 0 lỗi lint trên file đó. Cổng nhẹ **không** kiểm
   kiểu, nên sửa file nằm trong đường đi của barrel thì vẫn nên chạy `typecheck`.
3. **Không tạo vi phạm tầng mới** — `boundaries/*` + `no-restricted-imports` giữ nguyên mức nợ cũ (**2**).
4. **Không `eslint-disable` để dập lint** — mỗi comment disable là thêm một lỗi ở cổng boundaries.
5. Lệnh fail thì **dán output thật**; **lệnh nào không chạy thì nói là không chạy**, không suy ra
   "chắc vẫn xanh". Cấm viết "đã qua cổng nghiệm thu" khi mới chạy cổng nhẹ.
