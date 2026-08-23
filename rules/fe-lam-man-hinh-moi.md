# FE — Làm màn hình mới: quyết định trước khi gõ

> Tách khỏi `client/CLAUDE.md` để file rule chính nhẹ hơn. Nội dung giữ **nguyên văn**.
> Đọc khi đụng đúng vùng này, không đọc trước.

## 4. Làm màn hình mới — quyết định trước khi gõ

**Bước 0 — LUẬT CỨNG: mọi phiếu yêu cầu (PYC) code mới đều làm trong `src/features/`.**
Không mở màn mới, không thêm tính năng mới ở `src/legacy/` — kể cả màn danh mục, kể cả khi
legacy "đã có sẵn cái gần giống". Legacy là vùng khoá (§9).

**Bước 1: kiểm màn này đã có engine chưa.**

| Loại màn | Làm ở đâu |
|---|---|
| **Danh mục** (CRUD một bảng) | `features/<domain>/`, dựng trên engine `@domain-kit/catalog` |
| **Chứng từ** | `features/<domain>/`, dựng trên engine `@domain-kit/chungTu` |
| **Báo cáo** | `features/<domain>/`, dựng trên engine `@domain-kit/report` |
| Khác (cấu hình, console…) | `features/<domain>/`, cấu trúc chuẩn §5 |

**Bước 2: dùng engine, đừng viết lại.** `@domain-kit` đã lo khung: tìm nhanh, phễu ngày, lọc nâng
cao, phân trang & sort server-side, dòng tổng, cấu hình cột, panel chi tiết, confirm + toast +
invalidate, máy trạng thái nút, chữ khung vi+en. Cái gì **kernel BE bảo đảm** thì engine giữ; cái gì
kernel không định nghĩa thì module tự khai qua descriptor — hợp đồng đọc ở `*Descriptor.ts` /
`define*.ts` của engine, đừng chép vào đây.

⚠ **Danh mục mới — đọc kỹ:** `/danh-muc/*` hiện do legacy phục vụ (§9) và `features/danhMuc` là nhánh
chết (§4.1). Nên màn danh mục mới **không** ghép vào cây route cũ: dựng module mới trong
`features/<domain>/` trên `@domain-kit/catalog`, khai `paths.ts` + `permissions.ts` riêng, đóng góp
route qua `features/<domain>/routes.tsx` rồi nối tay ở `RootRoutes.tsx` (§7). Nếu PYC yêu cầu màn mới
phải xuất hiện trong hub danh mục cũ → **hỏi user trước**, vì hub đang đọc hằng số của nhánh chết.

**Bước 3: cấu trúc module theo §5.** Không có ngoại lệ nào cho "màn nhỏ".

### 4.1–4.3 Nhánh chết & hai shape đã đóng băng — xem `docs/rules/fe-nhanh-chet-va-shape-cu.md`

Trong `features/` có nhánh **đã bị thay thế nhưng chưa xoá** (nhìn từ code không phân biệt được:
vẫn có `routes.tsx`, `index.ts`, test đầy đủ) và hai shape module cũ đã bị cấm nhân bản.

**Ba luật rút gọn — chi tiết + bằng chứng ở file trên:**

1. **Trước khi sửa một module có sẵn, kiểm nó có đang chạy không** — cách duy nhất đáng tin là
   `app/router/RootRoutes.tsx`. Domain không nằm trong cây route đó thì sửa vào là công cốc
   (hiện `features/danhMuc` là nhánh chết — `/danh-muc/*` do `@legacy` phục vụ).
2. **Không mở module mới theo shape phẳng cũ** (đổ hết file ra gốc, dấu hiệu là `mock.ts`).
3. **Không tách màn theo hành vi** (`danhSach/` · `themMoi/` · `chinhSua/`) — §5 luật cứng 2.
