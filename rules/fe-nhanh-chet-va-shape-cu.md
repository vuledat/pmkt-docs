# FE — nhánh chết & hai shape module đã đóng băng

Tách khỏi `../../client/CLAUDE.md` §4 (2026-08-14) để giữ file rule gọn. Đọc khi: sắp sửa một
module `features/` có sẵn, hoặc thấy module lạ shape không giống §5.

## 4.1 Trước khi sửa: kiểm màn đó có đang chạy không

Trong `src/features/` có nhánh **đã bị thay thế nhưng chưa xoá** — nhìn từ code không phân biệt được với
nhánh sống: vẫn có `routes.tsx`, `index.ts`, test, màn dựng đầy đủ.

**Cách kiểm duy nhất đáng tin: `app/router/RootRoutes.tsx`.** Domain nào không nằm trong cây route ở đó
thì màn của nó không chạy — sửa vào là công cốc, chạy test vẫn xanh mà UI không đổi một pixel.

Trạng thái đo **2026-08-08** (kiểm lại bằng chính `RootRoutes.tsx`, đừng tin bảng này khi nó cũ):

| Nhánh `features/` | Đang chạy? |
|---|---|
| `banHangBackup` · `heThong` · `muaHang` · `tienGui` · `tienMat` | ✅ qua `gateByHandle(<domain>Routes)` |
| `rbacConsole` · `quyen3Truc` | ⚠ chỉ có ở route bàn thử `__rbac-console` / `__quyen-3-truc`, và chỉ khi `SHOWCASE_ENABLED` |
| **`danhMuc`** | ❌ **nhánh chết** — `/danh-muc/*` đang do `@legacy/features/danhMuc/LegacyDanhMucRoutes` phục vụ. 129/194 lỗi typecheck của repo nằm ở đây |

⚠ Bẫy của nhánh chết `danhMuc`: `app/layouts/shell/danhMucHub.tsx` **vẫn** deep-import `paths.ts` +
`permissions.ts` của nó (chỉ hằng số, không kéo page graph) — nên nhánh này "chết mà chưa gỡ được".
Sửa page/component trong đó là công cốc; đụng `paths.ts`/`permissions.ts` thì lại vỡ hub. Muốn dọn phải
hỏi trước.

⚠ Đừng dùng `git log` để đoán: commit `chore: init` gồm 41.297 file, nên "chỉ bị chạm bởi init" đúng với
gần như mọi thư mục, kể cả các domain đang chạy.

Phát hiện nhánh chết → **không sửa, không lấy làm mẫu, không import.** Muốn kích hoạt lại phải hỏi trước.

## 4.2 Shape phẳng cũ — ĐÓNG BĂNG

Một số module cũ đổ hết file ra gốc (`XxxTab.tsx` + `XxxListTable.tsx` + `XxxModal.tsx` +
`api/columns/model/queries/status/mock`). Đây là bản dựng UI **trước khi có API thật** — dấu hiệu nhận
biết là `mock.ts`.

- **Không mở module mới theo shape này** — module mới theo §5.
- Khi nối API thật: chuyển sang engine `@domain-kit`, tách lớp theo §5, **gỡ `mock.ts`**.
- `mock.ts` chỉ được tồn tại khi API chưa sẵn sàng. Còn `mock.ts` = còn nợ.

## 4.3 Shape tách theo hành vi — CŨNG ĐÓNG BĂNG

Shape thứ hai đã bị gỡ (ngày 2026-08-11, chính là `chungTuBanHang`): một màn bị bổ thành
`danhSach/` + `themMoi/` + `_shared/`, mỗi nhánh lại có `api/ components/ fields/ helpers/ i18n/`
riêng và hai namespace i18n.

Triệu chứng nhận biết: có thư mục con đặt tên theo **hành vi** (`danhSach` · `themMoi` · `chinhSua` ·
`xemChiTiet`), có `_shared/` mà domain chỉ có một màn, và import `../../_shared/...` khắp nơi.

**Không mở module mới theo shape này** — một màn hình là một module phẳng, §5.
