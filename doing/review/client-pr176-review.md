# Review client PR #176 — ngân quỹ thu/chi: tab Tham chiếu phiếu kiêm theo dòng hàng

- **Chế độ**: **SÂU**. Lý do: PR đi cặp với `cell-app#124` (đổi hợp đồng wire), diff 42 file /
  +930 dòng chạm `_shared/` dùng chung hai module — cần chạy cổng và đo baseline từng lỗi.
- **Phạm vi nghiệp vụ**: user yêu cầu **không check nghiệp vụ** ⇒ bỏ đối chiếu BR / `trace.sh` /
  `msg.sh`. Không có `docs/doing/*-spec` cho epic ngân quỹ thu/chi.

## 1. Phạm vi đã khoanh

| Mục | Giá trị |
|---|---|
| PR | `https://github.com/ospgroupvn-pmkt/client/pull/176` |
| Head SHA | `26a5d66e0225e616491fc0cb71caea800a880630` |
| Nhánh head | `origin/feature/thuchifullmua-clean` |
| Base (xác minh) | `origin/develop` = `093d8ce9776fc58a071d854f7e63d97677cb2d54` |
| Merge-base | `093d8ce9…` — **bằng đúng tip develop**, nhánh KHÔNG tụt |
| Commit | 1 · `feat(nganQuy): ngân quỹ thu/chi — tab Tham chiếu phiếu kiêm theo dòng hàng, sửa phiếu kiêm từ màn tiền, TTTHD theo TKNĐ, ẩn tỷ giá VND` |
| Quy mô | 42 file · +930 / −234 (1 file mới: `_shared/test/mucDichWizardKhongChonTay.render.test.tsx`) |
| Vùng đóng băng | 0 file rơi vào `src/legacy/**` |
| Working tree khi review | worktree detached `.review-client-pr176`, sạch |

Working tree `client/` của user đang ở nhánh khác (`feat/chung-tu-ban-hang-2`, 23 file dirty) —
**không đụng tới**; toàn bộ cổng chạy trên worktree detached riêng với `node_modules` sao chép
(lockfile không đổi giữa base và head nên bản sao hợp lệ).

## 2. Findings

### 🟠 Major 1 — Chặn mục đích wizard bằng **TÊN hiển thị**, tenant đổi tên là chốt tự mở

- **File**: `src/features/nganQuy/_shared/components/modal/PhieuThuChiFormModal.tsx:221-226`
  (`TEN_MUC_DICH_CHI_WIZARD`) và `:377-390` (`mucDichOptionsHienThi`).
- **Hợp đồng bị phá**: luật đã ghi thành văn ở đúng domain này —
  `cell-app/.../ChungTuThuChiCrudService.java:309-313`: *"Cố ý dùng sự tồn tại của dòng phân bổ làm
  marker chứ **không so tên mục đích thu/chi — tên đó là chuỗi tenant sửa được**"*.
- **Trigger**: tenant vào master data Tài khoản ngầm định và sửa tên định khoản
  `"Thu tiền khách hàng theo hóa đơn"` (thêm dấu cách cuối cũng đủ nếu không `trim()`, đổi chữ thì
  chắc chắn) → mở popup Thêm mới phiếu thu.
- **Actual**: `TEN_MUC_DICH_CHI_WIZARD.has(ten)` trả `false` ⇒ mục đích của wizard **quay lại
  dropdown**; người dùng chọn tay được. Phiếu tạo ra mang mục đích TTTHD nhưng **không có dòng phân
  bổ công nợ** ⇒ cờ "theo hoá đơn" của cả FE lẫn BE đều không bật (BE chấm cờ đó bằng sự tồn tại
  của dòng phân bổ, `ChungTuThuChiCrudService:309-317`).
- **Expected**: chốt phải đọc dữ kiện ổn định (cờ/id/sự tồn tại của dòng), không đọc chuỗi hiển thị.
- **Hậu quả**: hỏng **im lặng** — không lỗi, không log, chỉ là một phiếu sai loại nằm trong sổ.
- **Ghi nhận**: tác giả đã nêu rõ đây là giải pháp tạm ("Lọc theo TÊN vì TKNĐ chưa có cờ 'chỉ hệ
  thống gán' — tạm ở FE, chờ BA/master_data"). Vẫn giữ mức Major vì chế độ hỏng là im lặng và luật
  ngược lại đã tồn tại thành văn trong cùng domain. Đề nghị tối thiểu: gắn `TODO` có mã ticket và
  một test ghim hành vi khi tên bị đổi.

### 🔵 Minor 2 — Hai cảnh báo lint **mới** về dependency của hook

Đo bằng baseline từng lỗi (không so tổng số): lint đi từ **132 → 133** problem; sau khi trừ các dòng
chỉ dịch số dòng, phần **thực sự mới** là:

| File:dòng | Cảnh báo |
|---|---|
| `_shared/components/modal/PhieuThuChiFormModal.tsx:1251` | `useMemo` thiếu dep `chiTietPhieu.row?.laPhieuKiem` |
| `_shared/components/modal/ThuTraTienTheoHoaDonModal.tsx:640` | `useCallback` thiếu dep `mucDich?.taiKhoanChietKhauId` |

Cả hai đều nằm đúng trên đường PR vừa thêm (nhãn tab + bộ cột phiếu kiêm; TK chiết khấu theo TKNĐ).

**Đã phản biện — không nâng lên Major**: `useDanhMucPhieuThuChi` trả về **object literal mới mỗi
render** (không `useMemo`, `useDanhMucPhieuThuChi.ts:461`), nên `danhMuc` trong dep array đổi
identity mỗi render và callback ở `:640` luôn bắt được `mucDich` mới. Với `:1251`, `chiTietPhieu.row`
và `chiTietPhieu.congNo` cùng đến từ một lượt response nên `congNo` (đang có trong deps) đổi
identity cùng lúc. Không dựng được kịch bản sai thật ⇒ giữ Minor: **nợ mới trên cổng đang dùng để
đo baseline**, nên đóng lại thay vì để trôi.

### 🔵 Minor 3 — Khối lọc cột phiếu kiêm nhân bản 3 lần, `giu` set đã lệch nhau

- `_shared/fields/congNoColumns.ts:764-786` (`congNoDaLuuColumns`)
- `chungTuTienMat/fields/panelColumns.ts:268-290` (`congNoColumns`)
- `chungTuTienGui/fields/panelColumns.ts:268-290` (`congNoColumns`) — **byte-identical** với bản tiền mặt

Ba khối cùng một logic (`if (!phieuKiem) return cot` + `Set` tên cột giữ lại + `flatMap` chèn
`nguonTenHang` sau `nguonSoChungTu`), khác nhau đúng một phần tử: `_shared` giữ `'tkPhaiThu'` còn
hai bản panel giữ `'taiKhoanCongNo'`. Hai bản panel đã hoàn toàn trùng nhau ⇒ thêm một cột cho phiếu
kiêm sau này là ba chỗ phải sửa, và bài `congNoDongBoPanelPopup.test.ts` chỉ canh **panel ⇄ popup**
của tiền mặt, không canh tiền mặt ⇄ tiền gửi. Domain `nganQuy` đã có `_shared/` hợp lệ (2 module
thật) — chỗ đúng để gom.

### 🔵 Minor 4 — Test hồi quy mới sát ngưỡng timeout 5s ⇒ nguy cơ flaky trên CI

`_shared/test/mucDichPhieuKiem.render.test.tsx:149` — bài
*"phiếu kiêm ⇒ có Chỉnh sửa, không có Xóa · Ghi sổ; phiếu thường cùng props ⇒ có đủ"* **đỏ**
(`Test timed out in 5000ms`) ở lượt chạy cả cụm, **xanh** khi chạy riêng với `--testTimeout=60000`.
Bài này render `PhieuThuChiFormModal` **hai lần** trong một `it`. Xem §5 để biết vì sao đây không
phải lỗi code. Nên tách thành hai `it` hoặc nâng timeout tại chỗ.

### 🔵 Minor 5 — Commit scope không phủ hết diff

Scope `nganQuy` nhưng PR sửa 5 file trong `src/features/banHang/chungTuBanHang/` (`formDetail.ts`,
`soChungTuGoiY.ts`, `ChungTuBanHangThemMoiModal.tsx` + 2 test). Phần đó là hệ quả trực tiếp của thay
đổi BE nên gộp chung hợp lý, nhưng scope nên phản ánh (`feat(nganQuy,banHang): …`) hoặc tách commit.

### 🔵 Minor 6 — Tên nhánh lệch quy ước

`feature/thuchifullmua-clean`. `conventions-chung.md §4.2` khai tiền tố `feat/*` (không `feature/`);
`§4.3` yêu cầu chữ thường phân cách bằng `-`. Đúng phải là `feat/thu-chi-full-mua`.

### ⚪ Nit 7 — Cảnh báo lint mới trên file test mới

`_shared/test/mucDichWizardKhongChonTay.render.test.tsx:27` — `` `import()` type annotations are
forbidden `` (`@typescript-eslint/consistent-type-imports`). Chép nguyên pattern từ file anh em
`mucDichPhieuKiem.render.test.tsx:28` vốn đã có cùng cảnh báo, nên là nợ được nhân bản chứ không
phải nợ mới về bản chất.

### ⚪ Nit 8 — So sánh kiểu không nhất quán trong cùng một biểu thức

`PhieuThuChiFormModal.tsx:381-383`: dòng trên dùng `String(o.value)` (phòng `value: string | number`
của `CommonSelectBoxOption`), dòng dưới lại `o.value === id` với `id: string`. Chạy đúng vì id mục
đích là UUID chuỗi, nhưng hai dòng liền nhau phòng thủ khác nhau.

## 3. Bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục FE | ✅ Không vi phạm. File mới duy nhất là test, nằm đúng `_shared/test/`. Không file lạc gốc module, không tách màn theo hành vi, không `mock.ts`. `_shared/` hợp lệ (domain `nganQuy` có 2 module thật). Không `../../` mới trong module. |
| 2 | Không đánh lại version migration | N/A — PR frontend, không có migration. |
| 3 | Chưa test lại sau khi merge | ✅ N/A — merge-base **bằng đúng** tip `develop`, nhánh không tụt commit nào, không có file giao nhau cần merge thử. |
| 4 | Request thừa / N+1 phía FE | ✅ Không vi phạm. Không thêm lời gọi API nào trong vòng lặp render; tên hàng đọc từ `vatTu` **BE trả kèm** trong cùng response (`dongCongNoWireSchema.vatTu`), không request per-row. Xem Minor 2 cho phần dependency hook. |
| 5 | Chưa tận dụng BaseController/BaseEntity | N/A — PR frontend. |
| 6 | Chưa tận dụng base FE | ✅ Không vi phạm. Lưới vẫn `CommonListTable` của `@base`, ô chọn vẫn `CommonSelectBox`, điều hướng chứng từ gốc vẫn qua `@domain-kit/chungTuGoc`, quyền vẫn qua `@platform`. Không `<Table>` AntD trần, không fetch tự chế. |
| 7 | Constant đặt sai chỗ | ✅ Không vi phạm. `TEN_MUC_DICH_CHI`, `TEN_MUC_DICH_THU_THEO_HOA_DON`, `HINH_THUC_THANH_TOAN` đều import từ `constants/constants`; `VAI_TRO_TK.chietKhau` khai cạnh hai vai trò cũ trong `api/dinhKhoanNgamDinhApi.ts`. `TEN_MUC_DICH_CHI_WIZARD` khai đầu file nơi dùng duy nhất — hợp lệ theo `conventions-chung §1.2`. |

### i18n (cổng cứng luật 2)

✅ Khoá mới `tenHang` có ở **cả** `vi.ts` và `en.ts`, và ở **cả hai** namespace con
(`thuTien.congNo` + `traTien.congNo`) — `_shared/i18n/vi.ts:354,446` · `en.ts:290,366`. Không chuỗi
UI hardcode mới, không cộng chuỗi. Nhãn tab phiếu kiêm dùng khoá có sẵn
`nganQuy:phieuChi.tabs.thamChieu`.

### Cổng cứng khác

✅ Không `any` / `@ts-ignore` / `eslint-disable` mới (đã grep diff bằng mắt + đối chiếu lint).
✅ Không import `../../` vượt cấp mới; `boundaries` head = base (94 = 94), không lỗi mới.
✅ Dữ liệu wire mới parse qua Zod (`dongCongNoWireSchema.vatTuId/vatTu`), không ép kiểu mù.

### Cổng cây commit

✅ `git status` worktree PR sạch. File `_shared/helpers/phamViTaiKhoan.ts` được `ThuTraTienTheoHoaDonModal`
import mới — đã kiểm nằm trong cây commit (`git ls-tree 26a5d66e`), không phải file `??` quên
`git add`. `npx vite build` xanh, **0 `UNRESOLVED_IMPORT`** — đúng cổng bắt kiểu lỗi này.
`npm run check:committed` không áp dụng ở lượt review PR đã đẩy (kiểm bằng cây commit thật ở trên).

## 4. Cổng đã chạy

Lệnh thực tế (worktree `.review-client-pr176` @ `26a5d66e`, baseline `.review-client-base` @ `093d8ce9`):

```bash
npm run typecheck ; npm run lint ; npm run lint:boundaries
npx vitest run src/features/banHang/chungTuBanHang/test src/features/nganQuy
npx vite build
```

| Cổng | Head | Baseline (`develop`) | Kết luận |
|---|---|---|---|
| `typecheck` | **179 lỗi** | **179 lỗi** | So **từng lỗi**: tập hợp **giống hệt** (0 chỉ-ở-head, 0 chỉ-ở-base). 100% lỗi nền. |
| `lint` | 133 problem | 132 problem | 2 warning missing-dep + 1 warning `import()` là **mới** (Minor 2, Nit 7). Phần còn lại chỉ dịch số dòng. |
| `lint:boundaries` | 94 | 94 | Giống hệt, không lỗi mới. |
| `vitest` (có mục tiêu, 103 file) | 2 failed / 1238 | 3 failed / 1212 | Xem phân tích §5. |
| `vite build` | ✅ xanh, 0 unresolved import | — | Không cần baseline (head xanh). |
| `npm run test` (đủ 1093 file) | **NOT-RUN** | **NOT-RUN** | Xem §5. |
| `npm run build` | **NOT-RUN** trọn vẹn | — | `build = tsc -b && vite build`; `tsc -b` đỏ vì đúng 179 lỗi nền giống base ⇒ không phải lỗi PR. Phần bundler đã chạy riêng và xanh. |

## 5. Vì sao bộ test đầy đủ NOT-RUN, và hai bài đỏ nghĩa là gì

Chạy `npm run test` (1093 file test) song song trên head và base: sau ~40 phút **log không tăng
thêm một dòng nào** trong khi CPU vẫn leo — treo, không phải chậm. Đã dừng đúng 4 tiến trình node
thuộc hai worktree review (không đụng tiến trình nào khác của máy) và chuyển sang chạy **có mục
tiêu** trên toàn bộ `features/nganQuy` + `features/banHang/chungTuBanHang/test` = **103 file /
1238 test**, phủ trọn 17 file test mà PR chạm.

Kết quả so từng bài:

| Bài | Head | Base | Kết luận |
|---|---|---|---|
| `PhieuChiForm.render.test.tsx` › *mở được với tiêu đề và ba nút của Figma* | ❌ timeout 5000ms | ❌ timeout 5000ms | **Lỗi nền**, file không nằm trong diff |
| `mucDichPhieuKiem.render.test.tsx` › *phiếu kiêm ⇒ có Chỉnh sửa, không có Xóa · Ghi sổ…* | ❌ timeout 5000ms | ✅ (bài chưa tồn tại dạng này) | **Chậm máy, không phải lỗi code** — xem dưới |
| `loiLuuHienThi.test.ts` › *VALIDATION_ERROR…* | ✅ | ❌ | **PR sửa lỗi nền** |
| `loiLuuHienThi.test.ts` › *body là CHUỖI thuần…* | ✅ | ❌ | **PR sửa lỗi nền** |

Cả hai bài đỏ đều là `Test timed out in 5000ms`, **không phải assertion sai**. Chạy lại riêng với
`--testTimeout=60000`:

```
mucDichPhieuKiem.render.test.tsx   →  Test Files 1 passed | Tests 6 passed
PhieuChiForm.render.test.tsx       →  Test Files 1 passed | Tests 21 passed
```

⇒ **Không có lỗi code**; đây là ngưỡng timeout mặc định gặp máy chậm (các file render nặng trong
lượt này mất 15–52 giây/file). Ghi lại thành Minor 4 vì bài mới của PR sát ngưỡng.

## 6. Điểm làm tốt

- Sửa `chungTuCongNoApi.ts:242` từ `value: 'DaThanhToan'` → `'DA_THANH_TOAN'` là **đúng và quan
  trọng**. Đã kiểm chứng ở BE: `ValueConverter.java:72` dịch giá trị lọc bằng
  `Enum.valueOf(target, s)` — cần **tên hằng**, còn `'DaThanhToan'` là `maDb` của
  `TrangThaiThanhToanMuaHang`. Gửi mã wire ⇒ `INVALID_FILTER` ⇒ wizard trống trơn.
- Đổi hợp đồng `useMoChungTuGocThuChi` từ `boolean` sang union
  `{ daXuLy: true } | { daXuLy: false; cheDo }` buộc mọi chỗ gọi xử lý nhánh mới ở tầng **biên
  dịch**, không dựa vào ai nhớ đọc comment. Cả hai chỗ gọi (tiền mặt, tiền gửi) đã cập nhật.
- Test đọc **trạng thái mong đợi** chứ không đếm số lần gọi mock: `congNoDongBoPanelPopup.test.ts`
  ghim đúng danh sách + **thứ tự** 8 cột và đối chiếu panel ⇄ popup; `soChungTuGoiY.test.ts` phủ cả
  vế ngược (PT ⇒ tab GBC "chưa có số" và ngược lại).
- `phieuKiemLa()` tách thành helper thuần trong `helpers/` (không React, không mạng, không `t()`) —
  đúng ngăn theo khung FE.

## 7. Chưa đọc / chưa kiểm

- **990 file test còn lại** của `npm run test` (ngoài `nganQuy` + `chungTuBanHang`) — bộ đầy đủ treo
  trên máy này. Rủi ro sót: thấp — diff chỉ chạm `features/nganQuy/**` và
  `features/banHang/chungTuBanHang/**`, không sửa file nào ở `@base`/`@core`/`@platform`/`@domain-kit`,
  và `boundaries` xác nhận không có phụ thuộc mới ra ngoài hai vùng đó.
- `npm run build` trọn vẹn (chặn bởi 179 lỗi typecheck nền, đã chứng minh giống hệt base).
- Không đối chiếu BR / spec / `trace.sh` / `msg.sh` — user yêu cầu bỏ phần nghiệp vụ.
- Không kiểm UI thật (`qa-flow`) — đọc JSX không phải bằng chứng đã chạy màn.

## 8. Kết luận

**REQUEST CHANGES** — 1 Major (không Blocker).

Cổng cứng sạch: không `any`/`@ts-ignore`/`eslint-disable` mới, i18n đủ `vi` + `en` cả hai namespace,
không import vượt tầng (`boundaries` 94 = 94), typecheck **không thêm một lỗi nào** so với develop,
`vite build` xanh không có unresolved import, cây commit sạch. Hai bài test đỏ đều đã chứng minh là
timeout môi trường chứ không phải lỗi code, và PR còn sửa xanh 2 bài đỏ nền.

Major duy nhất là chốt **lọc mục đích wizard bằng tên hiển thị** — hỏng im lặng khi tenant đổi tên,
và đi ngược đúng luật đã ghi thành văn ở BE cùng domain. Tác giả đã đánh dấu là giải pháp tạm; cần
tối thiểu một mã ticket + test ghim trước khi merge.

## 9. Liên đới

PR này đi cặp với `cell-app#124` (hợp đồng `vatTuId` / `dienGiai` / cờ phiếu kiêm). Xem
[cell-app-pr124-review.md](cell-app-pr124-review.md) — 2 Major bên đó, trong đó Major 2 (đổi hình
thức thanh toán đòi thêm quyền `Delete`) chạm đúng luồng mà FE này vừa mở nút Sửa cho phiếu kiêm.
