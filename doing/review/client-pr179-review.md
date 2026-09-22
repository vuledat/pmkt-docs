# Review PR client#179 — Giá thành (Cấu hình giá thành + Kỳ tính giá thành)

**Chế độ: NHANH** (mặc định) — chỉ đọc + kiểm tĩnh bằng git. KHÔNG chạy typecheck/lint/test/build,
không worktree, không baseline, không merge thử.

| Mục | Giá trị |
|---|---|
| Repo | `client` (`https://github.com/ospgroupvn-pmkt/client`) |
| Head | `f8bc20cc` (`refs/pull/179/head`) — nhánh `feat/giao-dien-cau-hinh-gia-thanh` |
| Base | `origin/develop` @ `0092030d` (lấy từ parent1 của `refs/pull/179/merge`, không suy từ tên PR) |
| Merge-base | `3a18971f` |
| Diff | 79 file · +5070 / −68 · 11 commit |
| Working tree | sạch (`git status --porcelain` rỗng); checkout hiện tại là nhánh khác (`feat/chung-tu-ban-hang-2`) nên mọi kiểm chứng chạy trên ref `f8bc20cc`, không trên cây làm việc |
| Vùng đóng băng | không có file nào thuộc `legacy/`·`master_data/`·`Phase_2/` trong diff |

Phạm vi: 2 module FE mới `features/giaThanh/{cauHinhGiaThanh,kyTinhGiaThanh}` + `_shared`, 3 seam
mới ở `@domain-kit/catalog` (`filters`, `allowSaveAndAdd`), mở khoá mục menu "Giá thành", 2 proxy
entry ở `vite.config.ts`.

---

## Findings

### B1 · Blocker — `components/modal/` là bậc thư mục thứ hai trong module ⇒ 5 import `../../`

- `src/features/giaThanh/cauHinhGiaThanh/components/modal/CauHinhGiaThanhModal.tsx:29-33`
  (và `DoiTaiKhoanKetChuyenConfirm.tsx:10-11`, `KhoiPhucCaiDatGocConfirm.tsx:16-18`,
  `XoaDongConfirm.tsx:10`)
- Nguồn: CLAUDE.md gốc §Cấu trúc module Frontend luật 3 — “Không `../../` trong module — cây phẳng
  một bậc, `../../` = đặt file sai chỗ”; `bon-lop.md` lỗi #1 (mức mặc định Blocker).
- Actual: `components/modal/*.tsx` → `import … from '../../hooks/useCauHinhGiaThanhForm'`.
  Expected: 4 file này nằm thẳng ở `components/`, import `../hooks/…`.
- Hậu quả: quy ước, không phải lỗi chạy. Sửa rẻ: `git mv` 4 file lên `components/` + đổi `../../`
  thành `../` (module mẫu `banHang/chungTuBanHang/` để mọi popup phẳng trong `components/`).

### M1 · Major — màn Kỳ tính giá thành gọi 2 request danh sách mỗi lần mở (1 request thừa cho phương pháp không hiển thị)

- `src/features/giaThanh/kyTinhGiaThanh/pages/KyTinhGiaThanhPage.tsx:42-44`
- Trigger: mở `/gia-thanh/truc-tiep/ky-tinh-gia-thanh` (hoặc route hệ số tỷ lệ).
- Actual: gọi **cả hai** controller rồi mới chọn một. Mỗi controller là một `useCatalog` riêng và
  `createCrudQueries.useList` chỉ tắt theo tenant (`src/platform/query/createCrudQueries.ts:88`
  — `enabled: scope.congTyId != null`), nên `POST {base}/tim-kiem` bắn cho **cả** `truc-tiep` lẫn
  `he-so-ty-le`. Comment ngay trên dòng đó viết “bắt buộc gọi ĐÚNG MỘT trong hai controller… không
  gọi cả hai” — code làm ngược lại comment.
- Expected: chỉ fetch phương pháp đang render (lỗi #4 — request thừa).
- Hậu quả: gấp đôi request list mỗi lần vào màn và mỗi lần invalidate; với người dùng chỉ có
  `GTTT.AllPermission`, request thứ hai trả 403 im lặng (useCatalog không toast `listError`) — nhiễu
  log và tốn round-trip. Hướng sửa: tách `KyTinhGiaThanhPage` thành 2 component mỏng (mỗi cái gọi
  đúng controller của mình), hoặc thêm cờ `enabled` vào seam `useCatalog`.

### M2 · Major — mã message không mang mã đầy đủ ⇒ truy vết không đếm được (18/18 THIEU)

- `src/features/giaThanh/cauHinhGiaThanh/i18n/vi.ts:127-144` (và `en.ts` tương ứng)
- Nguồn: CLAUDE.md gốc §“Truy vết phải đếm được”; `docs/rules/truy-vet-luat.md:99` — “FE: key i18n
  **chính là mã** — `'MSG_PMKT-E-06194_043': '…'`”.
- Actual: key là `toast.msg001 … toast.msg205`. Expected: `MSG_PMKT-E-05897_001 …_205`.
- Bằng chứng: `msg.sh pmkt-docs/ba/PMKT-E-05897_CauHinhGiaThanh fe` → **18 message, THIEU 18, OK 0**
  (chạy trên cây làm việc — xem giới hạn ở §Kiểm chứng; `git grep MSG_PMKT` trên `f8bc20cc` cũng chỉ
  ra 3 lần nhắc trong **comment**, không có key nào).
- Hậu quả: cổng `msg.sh` đỏ vĩnh viễn cho epic này; không máy nào đối chiếu được câu chữ với
  `6.messages.md`. Nội dung tiếng Việt hiện đã khớp nghĩa tài liệu — chỉ cần đổi tên key.

### M3 · Major — `eslint-disable` mới trong diff

- `src/features/giaThanh/cauHinhGiaThanh/components/modal/CauHinhGiaThanhModal.tsx:95`
  (`react-hooks/exhaustive-deps`, effect toast-lỗi-rồi-đóng theo `c.status`).
- Nguồn: `checklist-fe.md` §A (mục này liệt ở mức Blocker). Hạ xuống Major vì có comment giải thích
  và không che một lỗi thật: deps thiếu là `toast/onClose/t/c.errorMessage`, thêm vào sẽ chạy lại
  effect mỗi render vì `onClose` là closure mới.
- Hướng sửa: giữ `onClose`/`toast` trong `useRef` (hoặc `useEffectEvent`) rồi khai đủ deps.

### M4 · Major — magic string trạng thái tài khoản đặt trong component, constant khai ra lại không ai dùng

- `src/features/giaThanh/cauHinhGiaThanh/fields/TaiKhoanCauHinhPicker.tsx:53`
  (`return trangThai !== 'NgungHoatDong'`) vs
  `src/features/giaThanh/cauHinhGiaThanh/constants/constants.ts:24`
  (`TRANG_THAI_TAI_KHOAN_HOAT_DONG = 'HoatDong'` — `git grep` xác nhận **0** nơi dùng).
- Nguồn: 9 luật §1 + `bon-lop.md` lỗi #7 / `checklist-fe.md` §D.
- Hậu quả: hai chỗ định nghĩa cùng khái niệm, chỉ một chỗ có hiệu lực; đổi wire value ở BE thì
  constant vẫn “đúng” mà picker vẫn sai. Wire value đã đối chiếu BE (`TaiKhoanPickerDto`, nhánh
  `origin/feat/logic-cau-hinh-gia-thanh`): `"HoatDong"`/`"NgungHoatDong"` — giá trị hiện đúng.

### m1 · Minor — `api/mock.ts` còn nguyên dù `DUNG_MOCK = false`

- `src/features/giaThanh/cauHinhGiaThanh/api/mock.ts:1-11` (203 dòng) — chính docblock của nó ghi
  “bước 3: XÓA file này và mọi import tới nó (client/CLAUDE.md §4.2 — còn `mock.ts` = còn nợ)”, và
  `cauHinhGiaThanhApi.ts:27` vẫn import 4 hàm mock.
- `checklist-fe.md` §B: “còn `mock.ts` = còn nợ, ghi finding”. Hậu quả: dead code đi vào chunk lazy;
  cờ `DUNG_MOCK` có thể bị bật lại vô tình.

### m2 · Minor — FE bật backend thật trong khi module BE chưa merge vào `develop`

- `src/features/giaThanh/cauHinhGiaThanh/api/cauHinhGiaThanhApi.ts:59` (`DUNG_MOCK = false`).
- Quét `cell-app` (mọi remote branch): package `cell/gia_thanh` + `cell/cst_gia_thanh` **chỉ** tồn tại
  ở `origin/feat/logic-cau-hinh-gia-thanh` (43 file), `origin/feat/logic-ky-tinh-gia-thanh` (17),
  `origin/feat/logic-do-dang-dau-ky` (64) — **không có** trên `develop`/`staging`.
- Hậu quả: merge FE trước BE thì cả 4 route Giá thành lỗi trên dev (404 từ front door). Không phải
  lỗi code — cần chốt thứ tự merge với BE trong mô tả PR.

### m3 · Minor — `TAI_KHOAN_CATALOG_PAGE_SIZE` chỉ nằm trong queryKey, không đi vào request

- `src/features/giaThanh/cauHinhGiaThanh/api/queries.ts:98` dùng hằng số này làm phần tử khóa, nhưng
  `fetchTaiKhoanCauHinhCatalog` (`cauHinhGiaThanhApi.ts:101-106`) gọi `http.get(TAI_KHOAN_BASE)`
  **không** `params`. Mẫu tham chiếu `heThong/cauHinhChiTiet/api/cauHinhChiTietApi.ts:76` gửi
  `params: { pageSize: CATALOG_PAGE_SIZE, … }`.
- Đã kiểm BE: `CauHinhGiaThanhTaiKhoanController.danhMucTaiKhoan()` trả `List` không phân trang ⇒
  **hiện không mất dữ liệu**. Vấn đề còn lại là hằng số gây hiểu nhầm “đã giới hạn 500 dòng”.

### m4 · Minor — focus nhảy sau khi **xóa** dòng, không chỉ khi thêm dòng

- `src/features/giaThanh/cauHinhGiaThanh/components/modal/CauHinhGiaThanhModal.tsx:255`
  (`onRowsChange={() => focusLastRowFirstEditor(gridBoxRef.current)}`) + hàm ở dòng 65-74.
- Trigger: xác nhận xóa một dòng giữa lưới → `onRowsChange` bắn → focus nhảy vào ô "Tài khoản tập
  hợp chi phí" của dòng **cuối cùng**, dù người dùng không thêm gì. Expected (theo chính docblock
  AC3): chỉ focus dòng **vừa thêm**. Hướng sửa: so số dòng trước/sau, chỉ focus khi tăng.

### m5 · Minor — file gốc module là `index.tsx`, không phải `index.ts`

- `src/features/giaThanh/cauHinhGiaThanh/index.tsx`, `src/features/giaThanh/kyTinhGiaThanh/index.tsx`
  (mỗi file chứa 2 wrapper JSX đóng cứng `phuongPhap`).
- CLAUDE.md gốc: “Gốc module **chỉ có `index.ts`**”. Hướng sửa: đưa 2 wrapper vào `pages/` và để
  `index.ts` chỉ re-export.

### Nit

- `KhoiPhucCaiDatGocConfirm.tsx:58` `zIndex={1050}`, `CauHinhGiaThanhModal.tsx:290` `background:'#fff'`
  / `border '1px solid #d9d9d9'` / `gap 8` inline — magic value, nên lấy token `@base`.
- `kyTinhGiaThanh/helpers/tenKyMacDinh.ts:16` chuỗi `'Kỳ tính giá thành '` nội suy trực tiếp; đúng là
  dữ liệu do BE sinh (không phải nhãn UI ⇒ không cần i18n) nhưng nên là constant có tên.
- `app/layouts/shell/AppSidebar.tsx:50,65,147` — reformat + đổi tên biến `c`→`l` ngoài phạm vi tính
  năng (mở rộng diff).
- `TaiKhoanCauHinhPicker.tsx:85` sort thuần theo `soTaiKhoan`; BR5 Common yêu cầu bản ghi “Ngừng hoạt
  động” xuống cuối. Chỉ chạm ca duy nhất còn sót (giá trị đã chọn bị lọc rớt được ghép lại), nên ảnh
  hưởng rất hẹp.

---

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ⚠ `eslint-disable` mới (M3) · `../../` trong module (B1). Không secret, không `any`/`@ts-ignore` mới (grep toàn bộ file diff), không import ngược tầng, response API đều Zod-parse, không chạm vùng đóng băng. |
| B — Kiến trúc & 7 lỗi | xem bảng dưới |
| C — Nghiệp vụ & truy vết | ⚠ M2 (mã message). `trace.sh` NOT-RUN (không có `docs/doing/*gia-thanh*-spec`). BR34/BR5-nội-bộ-màn đối chiếu đạt (xem §BR). |
| D — Vệ sinh diff & Git | ✅ cây commit sạch, file mới đều đã `git add` (toàn bộ là `A` trong `--name-status`); commit message đúng `<type>(<scope>):`; nhánh `feat/…`. ⚠ Nit reformat AppSidebar. |

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ⚠ **B1** (`components/modal/` bậc 2) + m5 (`index.tsx` ở gốc). `_shared/` hợp lệ (domain có 2 module thật). |
| 2 | Version migration | ✅ N/A — diff FE thuần, không có file `db/migration`. |
| 3 | Chưa test lại sau merge | ✅ N/A đo được: `git rev-list --count 3a18971f..origin/develop` = **3**; `comm -12` giữa file develop đổi và file PR đổi = **0 file giao nhau**. |
| 4 | N+1 / request thừa | ⚠ **M1**. Ngoài ra query key đều tenant-scoped ổn định, không có request trong vòng lặp render. |
| 5 | BaseController / BaseEntity | ✅ N/A (BE). |
| 6 | Chưa tận dụng base FE | ✅ `kyTinhGiaThanh` đi qua `@domain-kit` (`createCatalogModule`/`CatalogFormModal`) + `@base` (`CommonListTable`, `useListFilter`); bỏ `CatalogPage` có lý do ghi rõ (hai ngưỡng trạng thái Sửa/Xóa khác nhau). `cauHinhGiaThanh` dùng `CommonModalShell`/`CommonEditableGrid`/`CommonComboGrid`. Hai seam thêm vào `@domain-kit` (`filters`, `allowSaveAndAdd`) đều opt-in, mặc định giữ nguyên hành vi mọi catalog cũ. |
| 7 | Constant đặt sai chỗ | ⚠ **M2** (mã message) + **M4** (magic string trạng thái) + m3. Còn lại `constants/{constants,paths,permissions}.ts` đủ ba file chuẩn ở cả hai module. |

## BR đã đọc / chưa đọc

Đọc: **BR34** (Chỉnh sửa từ màn Xem chi tiết) — code đạt: `CauHinhGiaThanhPage.tsx:74-81` giữ
`openedFrom` và quay lại Xem chi tiết sau khi Lưu. **BR5** (Hiển thị Combogrid) — picker có cột
Trạng thái, tìm kiếm theo mã+tên; **lệch có nguồn**: BR5 chung cho chọn cả bản ghi “Ngừng hoạt động”
kèm cảnh báo, còn epic quy định riêng (`SCR_CauHinhGiaThanh_SuaCauHinh.md` §BR5 nội bộ: tài khoản
ngừng hoạt động làm cấu hình **không hợp lệ**) nên lọc bỏ hẳn là đúng — epic thắng trong phạm vi
epic. **BR26** (toast) — mọi thông báo đi qua `useToast`.

Chưa đọc (ngoài phạm vi bằng chứng của các finding trên): BR1·BR2·BR11·BR13·BR25·BR30·BR44
(nhóm màn danh sách/grid của `kyTinhGiaThanh`), BR3·BR14·BR15·BR43 (form/popup), BR16.

## Kiểm chứng đã chạy

```
git fetch origin refs/pull/179/{head,merge}          # base lấy từ parent1 của merge ref
git merge-base origin/develop f8bc20cc               # 3a18971f
git rev-list --count 3a18971f..origin/develop        # 3
comm -12 <(...develop) <(...head)                    # rỗng → lỗi #3 N/A
git grep -nE 'as any|: any|@ts-ignore|eslint-disable|from ../../' f8bc20cc -- <file diff>
git grep -c MSG_PMKT f8bc20cc -- src/features/giaThanh
comm vi/en keys × 3 namespace                        # parity đủ, 0 lệch
./docs/rules/br.sh --list ; ./docs/rules/br.sh 34 5 26
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-05897_CauHinhGiaThanh fe
cell-app: quét mọi remote branch tìm package gia_thanh
```

Giới hạn:
- `msg.sh` chạy trên **cây làm việc** của `client` (đang ở nhánh khác), không chạy được trên ref
  `f8bc20cc` mà không tạo worktree — chế độ nhanh cấm. Kết luận M2 vì vậy được kiểm chứng lại độc
  lập bằng `git grep MSG_PMKT f8bc20cc` (0 key) + đọc `i18n/vi.ts` ở head.
- `trace.sh`: **NOT-RUN** — không tồn tại `docs/doing/<slug>-spec` cho PMKT-E-05897/05908, và diff
  trải trên 2 epic nên không có một PYC đơn. Không đoán bừa spec.
- Cổng test/build (`typecheck`·`lint`·`lint:boundaries`·`test`·`build`·`check:committed`):
  **NOT-RUN — chế độ nhanh**.
- Chưa đọc (đã đọc phần cốt lõi: api/model/queries/hooks/components chính/routes/menu/i18n):
  `kyTinhGiaThanh/{fields/columns.ts, fields/formFields.tsx, components/KyTinhGiaThanhXemChiTietModal.tsx,
  helpers/dayjsValue.ts}`, `cauHinhGiaThanh/{api/mock.ts thân hàm, fields/tieuThucPhanBoOptions.ts,
  pages/*.css}`, và toàn bộ 12 file `test/**` của hai module.

## Kết luận

**REJECT** — có B1 (Blocker theo bảng lỗi #1), kèm 4 Major (M1–M4).

Ngay cả khi hạ B1 xuống Major, kết luận vẫn là **REQUEST CHANGES**: M1 (request thừa + comment sai
sự thật) và M2 (truy vết message đỏ 18/18) cần sửa trước khi merge; m2 là vấn đề **thứ tự merge với
BE**, không phải lỗi code.

Cổng test/build chưa chạy ở lượt này — muốn chấm để APPROVE thì chạy lại `/review-code sâu`.
