# IMPLEMENT — nhật ký sinh code FE cho PMKT-E-14294 Bù trừ công nợ

| | |
|---|---|
| **Ngày** | 2026-08-11 |
| **Nguồn** | plan trong chính thư mục này (`00`…`06`) |
| **Module** | `client/src/features/tongHop/buTruCongNo/` — 42 file, 5.573 dòng |
| **Trạng thái** | ✅ Code xong luồng UI đầy đủ · ⚠ **chạy trên dữ liệu giả** (BE chưa có endpoint nào) |

---

## 1. Phạm vi đã code

| File plan | Màn | Trạng thái |
|---|---|---|
| `01-danh-sach-chung-tu-bu-tru.md` | `SCR_BTCN_DanhSach` | ⛔ **Không code** — ngoài phạm vi theo D3 của plan (màn của epic PMKT-E-09980). Thay vào đó `index.ts` export sẵn popup + hook để module đó cắm vào. |
| `02-popup-bu-tru-cong-no.md` | `SCR_BTCN_BuTru` | ✅ Đầy đủ |
| `03-popup-chung-tu-bu-tru-them-moi.md` | `SCR_BTCN_ChungTu_ThemMoi` | ✅ Đầy đủ, trừ 2 tab giữ chỗ (xem §5) |
| `04-popup-chung-tu-bu-tru-xem-chi-tiet.md` | `SCR_BTCN_ChungTu_XemChiTiet` | ✅ Chế độ `view` + Ghi sổ / Bỏ ghi. Trừ Điều hướng trước/sau · In · Tiện ích (ngoài phạm vi, Q6) |
| `05-popup-xac-nhan-xoa.md` | `SCR_BTCN_PopupXacNhanXoa` | ✅ Đầy đủ |
| `06-hop-dong-api-va-i18n.md` | — | ✅ Zod + i18n vi/en + hằng số + quyền + paths |

---

## 2. File đã tạo / sửa

### Tạo mới — `client/src/features/tongHop/buTruCongNo/`

| Lớp | File | Vai trò |
|---|---|---|
| gốc | `index.ts` | Cửa ra duy nhất; export thêm popup + hook để bàn giao cho epic 09980 |
| `api/` | `model.ts` | Zod schema khai theo `z.ZodType<T>` với `T` lấy từ `fields/types.ts` |
| | `buTruCongNoApi.ts` | 8 hàm I/O; mỗi hàm có `// TODO(BE)` kèm **nguyên câu `http` + `parse`** sẽ dùng |
| | `mock.ts` | ⚠ **NỢ** — dữ liệu giả bám mẫu Figma, có kiểm token khoá lạc quan |
| | `queries.ts` | `useQuery`/`useMutation` khóa theo `congTyId` (BR28) |
| | `payload.ts` | State form → body `POST {BASE}`; chọn trường tường minh |
| `constants/` | `constants.ts` · `paths.ts` · `permissions.ts` | Hằng số nghiệp vụ · slug route · mã quyền |
| `fields/` | `types.ts` | Toàn bộ kiểu của module (chiều phụ thuộc duy nhất `api → fields`) |
| | `buTruColumns.ts` | 15 cột, dùng chung hai bên qua prop `ben` |
| | `hachToanColumns.ts` · `chungTuCongNoColumns.ts` | Cột hai tab; tab cặp ghép dùng `ListField.children` (nhóm cha–con) |
| | `options.ts` · `texts.ts` | Option dropdown + chữ khung cho component `@base` |
| `helpers/` | `phanBo.ts` | **BR02** — phân bổ tự động |
| | `ghepCap.ts` | Dựng cặp ghép + bồi cột quy đổi cho chế độ xem |
| | `hachToan.ts` | Dựng 1–2 dòng bút toán + chênh lệch tỷ giá |
| | `quyDoi.ts` | **Điểm làm tròn duy nhất** của module (BR7) |
| | `anHien.ts` | Dịch 3 ma trận Ẩn/Hiện thành cờ |
| | `kiemTra.ts` | BR01/BR03/BR04 + validate popup chứng từ; trả **khóa i18n**, không trả câu chữ |
| `hooks/` | `useBuTruSetup.ts` | State popup thiết lập (filter · 2 bảng · tick · phân bổ · tổng) |
| | `useChungTuBuTruForm.ts` | 5 trường nhập + **BR37** + Lưu / Lưu và ghi sổ |
| | `useBuTruActions.ts` | Ghi sổ · Bỏ ghi · Xóa (confirm + toast + invalidate) |
| `i18n/` | `vi.ts` · `en.ts` · `registerBuTruCongNoI18n.ts` | MỘT namespace `buTruCongNo`; `en.ts` bị ép cùng kiểu `vi.ts` ⇒ thiếu khóa là lỗi biên dịch |
| `components/` | 8 file `.tsx` | Xem §3 |
| `pages/` | `BuTruCongNoPage.tsx` · `buTruCongNo.css` | Entry (chỉ ráp) + stylesheet của màn |
| `test/` | 6 file | 56 test |

### Sửa file có sẵn

| File | Sửa gì | Vì sao |
|---|---|---|
| `client/src/features/tongHop/routes.tsx` | +1 route `/tong-hop/bu-tru-cong-no` | Route contribution của domain |
| `client/src/base/theme/tokens.ts` | +`MODAL_WIDTH_WIDE = 1392` | D10 — Figma dùng bề rộng 1392, hai token có sẵn là 800/1200. Thêm vào `@base` thay vì hardcode trong feature |
| `client/src/base/index.ts` | export `MODAL_WIDTH_WIDE` | như trên |

`app/router/RootRoutes.tsx` **không cần sửa** — `tongHopRoutes` đã được nối ở dòng 166 từ trước, route mới ăn theo.

---

## 3. Đã reuse gì

| Cần | Dùng lại | Bằng chứng |
|---|---|---|
| Khung popup (×, Esc, guard bỏ dở, khóa khi gọi API, xếp lớp) | `CommonModalShell` | `base/index.ts:264`; dùng `zIndex` · `busy` · `dirty`+`discardConfirm` |
| Footer nhiều nút | `CommonModalFooter` (qua `footer` của shell) | `mode:'edit'` cho 3 nút lưu, `mode:'view'` cho chế độ xem |
| Bảng chứng từ: checkbox · **giữ tick qua trang** · dòng Tổng toàn tập · tìm nhanh · Reload · phân trang · cấu hình cột | `CommonListTable` | `selectable`+`preserveSelectedRowKeys`+`showSummary`+`summaryScope='all'`+`columnConfigKey` — **không thiếu prop nào**, không phải thêm gì vào base |
| Nhóm cột cha–con tab cặp ghép | `ListField.children` | `base/components/table/listTableFormat.ts:47-56` |
| Combogrid Đối tượng (BR5) | `CommonComboGrid` | `base/index.ts:568` |
| Dropdown · ngày · chữ · số · nhãn có `*` | `CommonSelectBox` · `CommonDateInput` · `CommonTextBox` · `CommonNumberInput` · `FieldLabel` | |
| Tab gạch chân | `TabMenuChild` | `base/index.ts:150` (không dùng `TabMenu2Level` — đó là tab thư mục của thanh cấp 2) |
| Popup xác nhận (BR3) | `CommonConfirmModal` | `base/index.ts:276` |
| Toast + map lỗi API | `useToast` + `describeApiError` | `base/index.ts:49`, `@platform` |
| Làm tròn tiền tệ | `roundMoney` · `scaleMoney` · `sumMoney` · `equalMoney` · `PRECISION` từ `@core` | `src/utils/index.ts:19-28` |

### Viết mới — 8 component, mỗi cái vì mang nghiệp vụ riêng của màn

| Component | Vì sao không reuse được |
|---|---|
| `BuTruCongNoModal` | Ráp riêng của màn: 3 khối + luật mở popup con |
| `BuTruHeaderFilter` | Hàng 6 ô với bề rộng Figma cố định + luật highlight trường thiếu |
| `ChungTuBuTruTable` | Bọc `CommonListTable` để nhúng ô nhập "Số tiền bù trừ" và cột động theo loại tiền |
| `ChungTuBuTruModal` | Popup 2 chế độ với footer đổi theo trạng thái chứng từ |
| `ThongTinChungBuTru` | Bố cục 2 cột + kẻ dọc riêng của Figma |
| `HachToanTab` · `ChungTuCongNoTab` | Lưới con gắn với bộ cột nghiệp vụ riêng |
| `XacNhanBuTruModal` | Bọc `CommonConfirmModal`, chọn tone/chữ theo hành động |

**Chỉ một thứ phải thêm vào `@base`:** token `MODAL_WIDTH_WIDE`. Không copy component nào ra feature.

---

## 4. Lệch so với plan

| # | Lệch gì | Vì sao | Ảnh hưởng |
|---|---|---|---|
| L1 | Plan gộp test thành `kiemTra.test.ts` + `anHien.test.ts` riêng; code gộp thành **`kiemTraVaAnHien.test.ts`** | Hai bộ này kiểm cùng một lớp "luật thuần → cờ", tách ra chỉ nhân đôi phần dựng fixture | Không |
| L2 | Plan ghi `helpers/anHien.ts` chỉ trả cờ `coQuyDoi`; code thêm `TRANG_THAI_WIRE` + `tinhCoNutChungTu` | Engine `@domain-kit/chungTu` **cấm hardcode chuỗi trạng thái** rải rác; gom vào một chỗ là cách rẻ nhất để tuân luật đó mà chưa cần khai descriptor | Tốt hơn plan |
| L3 | Plan dự tính dùng `useEffect` điền giá trị mặc định của filter; code **dẫn xuất** bằng `useMemo` | `react-hooks/set-state-in-effect` chặn, và dẫn xuất còn bỏ được một khung hình ba ô trống | Không |
| L4 | Mock ban đầu để hai bên lệch tổng; đã cân lại cho tổng **Số chưa thu = Số còn nợ = 10.727.248** | Nếu không, luồng hạnh phúc không chạy được — bấm "Bù trừ" luôn bị BR03 chặn | Chỉ ảnh hưởng dữ liệu giả |
| L5 | Nút **Ghi sổ / Bỏ ghi** ở chế độ xem đặt trong thân popup, không ở footer | `CommonModalFooter` `mode='view'` chỉ có sẵn Đóng · Sửa · Xóa · Nhân bản · In — mà màn này **không có nút Sửa** lại cần hai nút chuyển trạng thái | Cần Design xác nhận vị trí (thêm vào Q6) |

**Không có lệch nào đổi hợp đồng API hay đổi nghiệp vụ.**

---

## 5. Nợ kỹ thuật

| # | Nợ | Chi tiết |
|---|---|---|
| **N1** | **`api/mock.ts` — toàn bộ 8 endpoint là dữ liệu giả** | `cell-app` chưa có module `bu_tru_cong_no`. Mỗi hàm trong `buTruCongNoApi.ts` có `// TODO(BE)` kèm đúng câu `http` + `parse` sẽ thay vào. **Còn `mock.ts` = còn nợ.** |
| **N2** | Endpoint danh mục **Đối tượng** chưa xác định | Chưa rõ path và tên cờ lọc "vừa là khách hàng vừa là nhà cung cấp" — cần BE |
| **N3** | Endpoint **cấu hình TK chênh lệch tỷ giá** chưa xác định | Không có nó thì `MSG_..._016` lùi về bước Lưu, mất yêu cầu chặn sớm của UC |
| **N4** | Tab **Đính kèm** · **Tham chiếu** là chỗ giữ | Figma vẽ 4 tab, SCR mô tả 2 — chờ **Q3** |
| **N5** | **Điều hướng trước/sau · In · Tiện ích** chưa dựng | Không có Figma; SCR tự ghi nút In để tài liệu riêng — chờ **Q6** |
| **N6** | Màn không vào được từ menu | Leaf `tong-hop` đang `disabled: true` (`app/layouts/shell/menuRegistry.tsx:177`); submenu 3 cấp mà BA mô tả thì shell chưa hỗ trợ — chờ **Q2**. Hiện deep-link được bằng `/tong-hop/bu-tru-cong-no` |
| **N7** | Nền sau popup trống | Figma vẽ popup phủ lên danh sách Phiếu KTTH — màn đó thuộc epic 09980, chưa có (**Q1/R1**) |
| **N8** | Q11 chưa chốt | "Lưu và ghi sổ" nguyên tử hay 2 pha. Code hiện xử lý: request ném lỗi ⇒ coi như chưa lưu, giữ popup mở. Nếu BE chốt 2 pha và trả `id` kèm lỗi thì phải đóng popup — đã ghi `TODO` tại `ChungTuBuTruModal.onLuu` |
| **N9** | Bề rộng cột hai bảng là số **tạm** | Figma không cho số đo từng cột (**Q9**); hằng `COT_BU_TRU_WIDTH` gom một chỗ để đổi một lần |

---

## 6. Kết quả cổng nghiệm thu

```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test && npm run build
```

| Lệnh | Kết quả | So với baseline |
|---|---|---|
| `npm run typecheck` | **193 lỗi**, **0 lỗi trong file mới** | = baseline (`docs/fe-khung-kien-truc-chuan.md:303` ghi 193) — **không tăng** |
| `npm run lint` | **9 lỗi + 2 warning**, **0 của module mới** | Baseline tài liệu ghi 10+2; đo thực tế 9+2. 9 lỗi còn lại đều ở `base/components/fields/CommonSlider.tsx` và `legacy/**` — **không phải của việc này** |
| `npm run lint:boundaries` | **76** (74 "rule not found" + **2 vi phạm thật**) | = baseline. Hai vi phạm thật vẫn đúng hai chỗ cũ: `legacy/features/danhMuc/DanhMucCrud.rules.test.ts` và `legacy/lib/apiError.ts`. **Không sinh vi phạm tầng mới** |
| Test của module | **6 file · 56 test · PASS** | mới |
| `npm run build` | ⚠ **Đỏ ở bước `tsc -b`** với đúng 193 lỗi nền, **0 lỗi trong file mới** | Build đã đỏ sẵn trước việc này. `npx vite build` chạy riêng **thành công**, sinh đúng chunk lazy `dist/assets/buTruCongNo-*.js` + `.css` ⇒ chứng minh `routes.tsx` vẫn eager-tiny |

### Về việc chạy test rộng hơn

Chạy `vitest run src/base/components/table src/base/components/modal src/features/tongHop` (39 file,
464 test) thì **`src/base/components/table/test/CommonListTable.test.tsx` đỏ 1–3 test, số lượng đổi
theo từng lần chạy**. Đã kiểm chứng đó **không** phải hồi quy do việc này:

| Cách chạy | Kết quả |
|---|---|
| Riêng `CommonListTable.test.tsx` | **52/52 PASS** |
| Cả `src/base/components/table` + `modal` (28 file) | **356/356 PASS** |
| Gộp thêm `src/features/tongHop` (39 file) | 1–3 test của `CommonListTable` đỏ, **khác nhau giữa các lần** (3 → 1 → 2) |

Đây đúng hiện tượng `client/CLAUDE.md §13` cảnh báo (*"suite hay flaky khi chạy song song"*).
File đó **không bị việc này chạm** — thay đổi ở `@base` chỉ là **thêm một hằng export**.

**Test của module thì đã làm cho vững**, không để trôi theo may rủi: lần chạy rộng đầu tiên có 2–4
test render của module đỏ vì timeout. Nguyên nhân thật là chi phí, không phải logic — mỗi test đi qua
`napDuLieu` mount **hai** `CommonListTable` đầy đủ rồi chạy một chuỗi thao tác dài. Đã sửa gốc:

1. `MOCK_DELAY_MS` 350 → **80** (độ trễ giả nhân lên qua hàng chục lượt gọi liên tiếp);
2. khai `{ timeout: 30_000 }` cho đúng các test đi qua `napDuLieu` — **khai chi phí thật**, không phải
   giấu lỗi.

Sau đó module xanh **9/9 render · 56/56 tổng** qua **hai lần chạy rộng liên tiếp**.

**Không dùng `eslint-disable`, không nới rule, không `any`, không `@ts-ignore`.**

11 lỗi lint do việc này sinh ra ban đầu đã được sửa **tận gốc**:
- 3 tham số `_body` không dùng → cho mock **dùng thật** token khoá lạc quan (mô phỏng 409);
- 7 biến `_a.._g` của destructure-để-loại → đổi thành **chọn trường tường minh**;
- 1 `set-state-in-effect` → bỏ `useEffect`, **dẫn xuất** filter hiệu lực bằng `useMemo`.

---

## 7. BR đã áp dụng

BR1 (phân trang 10/20/50/100) · BR2 (STT, checkbox, sắp xếp Ngày chứng từ ↑, sticky header) ·
BR3 (popup: ×/Esc, hủy trái–action phải, xác nhận đóng khi dirty, popup xác nhận xóa) ·
BR4 · BR09 (cột Loại chứng từ, danh sách Tham chiếu) · BR5 (combogrid Đối tượng) ·
BR7 (precision 2/4/6 + làm tròn ở kết quả cuối, điểm làm tròn duy nhất) · BR11.1 (tìm nhanh 2 bảng) ·
BR12 (hai trạng thái + token khoá lạc quan) · BR13.1 (nút Reload) ·
BR13.2 (Lưu/Lưu và ghi sổ/Ghi sổ không hỏi xác nhận) · BR14.1 (chế độ form) ·
BR14.4 (chặn cứng maxLength 500/50/500) · BR15.1/15.2/15.4 (bắt buộc, ≥0, border đỏ, highlight) ·
BR18.2/18.4 (công thức quy đổi, **ẩn hẳn** cột quy đổi khi = ĐTHT) · BR19.1 · BR20 (≤50 ký tự) ·
BR21 (lưới chi tiết con **chỉ đọc** — lệch có chủ đích khỏi BR21.1, theo SCR) ·
BR25 (route gác bằng `BuTruCongNo.Create`; thiếu quyền → **ẩn** nút) · BR26 (toast) ·
BR28 (khóa query theo `congTyId`) · BR29.1 (xóa mềm — BE) · BR30 (cấu hình ẩn/hiện cột) ·
BR31 (dòng Tổng ở 4 lưới) · BR32 (copy từ grid — sẵn có) · BR33 (trạng thái) ·
BR36 (không gộp bút toán — FE gửi đúng số dòng đã dựng) · BR37 (đồng bộ Ngày hạch toán ↔ Ngày chứng từ) ·
BR41 (**không** áp — quan hệ bù trừ là ràng buộc nghiệp vụ, BR41 tự loại trừ) · BR42 (Bỏ ghi chỉ khi Đã ghi sổ) ·
BR43 (trim khi submit) · BR44 (`identity` cho số chứng từ, `long` cho diễn giải).

### Lệch BR có chủ đích (đã ghi rõ)

| BR | Lệch gì | Căn cứ |
|---|---|---|
| **BR1** | Page size mặc định **10**, không phải 20 | Figma vẽ "10 / trang" ở cả hai bảng (`41323:660816`) — epic thắng trong phạm vi epic |
| **BR13.2** | **Bỏ ghi CÓ** popup xác nhận (BR nói không) | `SCR_BTCN_ChungTu_XemChiTiet.md:40` + `UC_BTCN_GhiSoBoGhi.md:17` bắt hiện `MSG_..._102`; BR16 cho phép cảnh báo nghiệp vụ có mã MSG riêng |
| **BR21.1** | Lưới chi tiết con **không có** nút Thêm/Xóa dòng | Hai dòng bút toán do hệ thống dựng (`SCR_BTCN_ChungTu_ThemMoi.md:35`) |

### BR chưa đạt

| BR | Lý do |
|---|---|
| BR38 · BR39 | Figma đặt `hidden` cho nút excel/print của hai bảng; SCR không yêu cầu |
| BR45 | Thao tác hàng loạt thuộc màn danh sách Phiếu KTTH — ngoài phạm vi (D3) |
| BR17 · BR19.1 · BR36 (phần ghi sổ) | Ràng buộc **BE**; FE chỉ hiển thị lỗi trả về — chưa kiểm chứng được vì chưa có endpoint |
| BR34 | **Không áp dụng** — chứng từ bù trừ không cho sửa ở mọi trạng thái |

---

## 8. Cách chạy thử

```bash
cd client && npm run dev
```

Mở `http://localhost:5173/tong-hop/bu-tru-cong-no` (chưa vào được từ menu — N6).

Kịch bản thử luồng đầy đủ:
1. Chọn **Đối tượng** bất kỳ → bấm **Lấy dữ liệu** → hai bảng có 5 dòng mỗi bên.
2. Tick checkbox header **cả hai bảng** → phân bổ tự động chạy, hai tổng đều 10.727.248, dải dưới hiện "Số tiền bù trừ 10.727.248".
3. Bấm **Bù trừ** → popup "Phiếu kế toán tổng hợp" mở, Số chứng từ **để trống**.
4. Nhập Số chứng từ → **Lưu** hoặc **Lưu và ghi sổ**.
5. Đổi **Loại tiền** sang `USD` rồi lặp lại → xuất hiện cột Tỷ giá + 3 cột quy đổi mỗi bảng, tab Hạch toán có **dòng 2 "Xử lý chênh lệch tỷ giá"**, tab Chứng từ công nợ có cột **Chênh lệch tỷ giá**.
6. Bỏ tick một dòng để thử ca chặn `MSG_..._007` (tổng hai bảng không bằng nhau).
