# Review PR #217 — `ospgroupvn-pmkt/client`

| Mục | Giá trị |
|---|---|
| PR | #217 — `feat: init bao cao ccdc` · tác giả `tichvd-osp` · trạng thái OPEN |
| Nhánh | `feat/bao-cao-ccdc` → `develop` |
| Head SHA | `7ad3b6e79117bd16b35eb2e2967fec0129793efb` |
| Merge-base | `7f52a72397a904f255b7c129a7131c7aea5ba1e9` |
| Quy mô | 10 file · +585 / −1 · 1 commit |
| Chế độ review | **NHANH** — chỉ đọc + kiểm tĩnh bằng git/grep. **KHÔNG** chạy test/build/npm, **KHÔNG** worktree, **KHÔNG** sửa code, **KHÔNG** đăng comment lên PR (theo yêu cầu người gọi). |
| Epic liên quan | PMKT-E-10810 (BC chi tiết CCDC) · PMKT-E-14616 (Bảng tính phân bổ CCDC) |

## Kết luận

**REQUEST CHANGES** — 0 Blocker, 3 Major (M1, M2, M3), 5 Minor, 4 Nit.

Chế độ nhanh: cổng `typecheck / lint / lint:boundaries / test / build` **CHƯA CHẠY**. Kết luận chỉ
có hiệu lực trong phạm vi đã đọc (toàn bộ 10 file của diff + các file phụ thuộc nêu ở §Đã đọc).

| Mức | Số lượng |
|---|---|
| Blocker | 0 |
| Major | 3 |
| Minor | 5 |
| Nit | 4 |

---

## Nội dung diff (tóm tắt)

1. `reportCatalog.ts` — thêm nhóm `cong-cu-dung-cu` với 2 báo cáo `bao-cao-chi-tiet-ccdc`,
   `bang-tinh-phan-bo-ccdc`, cả hai `implemented: true`.
2. `reportLookupOptions.ts` — thêm fetcher `fetchLoaiCongCuDungCuOptions` + đăng ký resource
   `loai-cong-cu-dung-cu` vào `LOOKUP_FETCHERS`.
3. `reportParamDefaults.ts` (mới) + `ReportRunnerPage.tsx` — dẫn xuất `values` từ `storedValues`
   bằng `withSpecDefaults`, để `defaultValue` mà BE phát trong `ReportParamSpec` thực sự được dùng
   (trước đây `reportModel.ts` parse rồi bỏ — đã xác minh: không consumer nào đọc `defaultValue`).
4. `i18n/vi.ts` + `en.ts` — 2 namespace mới `bcChiTietCcdc` (28 khóa) và `bcPhanBoCcdc` (29 khóa),
   cộng `baoCao.group.congCuDungCu` và 2 khóa `baoCao.report.*`.
5. 4 file test mới trong `src/app/pages/baoCao/test/`.

---

## Findings

### M1 — Major · 2 `reportId` mới chưa đăng ký ở façade `cell-app` ⇒ 404 `REPORT_UNKNOWN`

- **File**: `client/src/app/pages/baoCao/reportCatalog.ts:83-95`
- **Nguồn/hợp đồng**: `cell-app/src/main/java/vn/vtt/pmkt/cell/reporting/internal/controller/ReportProxyController.java:32,39`
  → `@PreAuthorize("@reportProxyService.duocPhepXemBaoCao(#reportId, authentication)")` →
  `ReportProxyService.java:78` → `ReportPermissionRegistry.requirePermission` (**fail-closed**).
- **Trigger**: người dùng có quyền `BCChiTietCCDC.View` bấm báo cáo ở hub.
- **Actual**: `git show origin/develop:.../ReportPermissionRegistry.java` chỉ có 11 entry
  (`so-cai` … `so-chi-tiet-tai-khoan`); **không** có `bao-cao-chi-tiet-ccdc` và
  **không** có `bang-tinh-phan-bo-ccdc`. `requirePermission` ném `ApiException.notFound("REPORT_UNKNOWN")`.
- **Expected**: `implemented: true` chỉ được bật khi façade đã đăng ký `reportId` tương ứng.
- **Hậu quả**: cả hai mục hiện lên hub, bấm vào → `fetchReportParamSpec` 404 → màn báo lỗi. Tính năng
  chết end-to-end cho tới khi `cell-app` có PR bổ sung 2 dòng `Map.entry`.
- **Thêm**: comment ở `reportCatalog.ts:88-89` viết *"`permission` chép thẳng từ
  `cell-app ReportPermissionRegistry.java:38`"* — dòng đó **không tồn tại** trên `origin/develop`
  của `cell-app`. Mã quyền `BCChiTietCCDC.View` / `BCPhanBoCCDC.View` thì **đúng** (đã đối chiếu
  `cell-app/src/main/resources/db/migration/V2__seed_data.sql:830, 907-909`) — nhưng comment
  `mã đã seed V3:1315` cũng sai file (xem N2).
- **Hướng xử lý**: hoặc sequence merge sau PR `cell-app`, hoặc tạm để `implemented: false`.

### M2 — Major · `LOAI_CCDC_BASE` mâu thuẫn với hằng đang dùng của màn danh mục; sai path thì dropdown rỗng im lặng

- **File**: `client/src/app/pages/baoCao/reportLookupOptions.ts:38-48` (`LOAI_CCDC_BASE = '/api/master-data/loai-ccdc'`)
- **Xung đột**: `client/src/features/danhMuc/taiSanCongCu/loaiCongCuDungCu/api.ts:17` khai
  `LOAI_CONG_CU_DUNG_CU_BASE = '/api/master-data/loai-cong-cu-dung-cu'` và đang phục vụ một màn danh
  mục **đang chạy** (có route test ở `src/app/router/test/Router.test.tsx:535`). Hai path cho cùng
  một resource — **một trong hai chắc chắn sai**.
- **Actual**: comment của PR khẳng định path của module danh mục 404 `NoResourceFoundException` và
  controller thật map ở `/loai-ccdc`. **Không xác minh được trong lượt review này**:
  `cell-app/src/main/java/.../cell/master_data/**` là vùng đóng băng, lệnh `grep` vào đó bị hook
  `pmkt-gate.py` từ chối (đã thử, bị deny — không gỡ rule).
- **Hậu quả nếu path mới sai**: `useReportLookupOptions` (`reportLookupOptions.ts:305-325`) nuốt lỗi
  — `results[i]?.data ?? []` — nên người dùng thấy combobox "Loại CCDC" **rỗng, không báo lỗi**.
  Test mới không bảo vệ được: nó mock `http.get` nên pass với bất kỳ chuỗi path nào.
- **Yêu cầu**: tác giả dán bằng chứng `@RequestMapping` của `LoaiCongCuDungCuController` (hoặc log
  request thật) vào PR. Nếu path mới đúng thì màn danh mục Loại CCDC **đang hỏng** → mở ticket riêng
  (comment đã ghi nhận, nhưng không có mã ticket — xem m4).

### M3 — Major · Bỏ lọc `trangThai` phía server rồi lọc client trên trang 200 dòng ⇒ có thể mất loại CCDC đang hoạt động

- **File**: `client/src/app/pages/baoCao/reportLookupOptions.ts:107-115`
- **Trigger**: tenant có > 200 bản ghi `loai_cong_cu_dung_cu` (hoặc ≤ 200 nhưng nhiều dòng
  `NgungHoatDong` chiếm chỗ trong trang đầu).
- **Actual**: gọi `{ params: { pageSize: 200 } }` rồi `.filter(r => r.trangThai === 'HoatDong')`.
  Trang đầu bị các dòng ngừng hoạt động chiếm chỗ ⇒ loại CCDC đang hoạt động nằm ngoài 200 dòng đầu
  **biến mất khỏi combobox, không cảnh báo**.
- **Expected**: gửi `trangThai: 'HoatDong'` như 3 fetcher anh em trong **chính file này** —
  `fetchDoiTuongOptions:46`, `fetchLoaiTaiSanOptions:63`, `fetchBoPhanOptions:75` đều gửi
  `trangThai: 'HoatDong'` và đang chạy thật.
- **Phản biện lý do trong comment**: comment viết *"nothing pins which string its enum binder takes"*
  — nhưng 3 call site cùng file đã chứng minh chuỗi `'HoatDong'` bind được ở các controller
  master-data khác, và `mapper.ts:23` của `congTrinh` cũng dùng đúng chuỗi đó. Lý do nêu ra không
  đứng vững; lọc client ở đây là đánh đổi kèm mất dữ liệu chứ không phải "nhánh không thể thất bại
  âm thầm".
- **Ghi chú**: BR5 (Nhóm 5) yêu cầu combogrid "Loại công cụ dụng cụ" hiển thị *Mã, Tên loại công cụ
  dụng cụ, Trạng thái* — lọc chỉ-hoạt-động là cách các lookup khác đang làm, chấp nhận được; vấn đề
  chỉ nằm ở chỗ lọc SAU khi phân trang.

---

### m1 — Minor · Import `../../../` thay vì alias `@app/*` (luật 4)

`test/reportCatalog.bangTinhPhanBoCcdc.test.ts:4-5` và `test/reportCatalog.chiTietCcdc.test.ts:4-5`
dùng `from '../../../i18n/vi'` / `'../../../i18n/en'`. Alias `@app/*` có sẵn
(`client/tsconfig.app.json:38`). Hạ xuống Minor vì **có tiền lệ đã merge** cùng shape
(`test/reportCatalog.tongHopTscd.test.ts:4-5`) — nhưng code mới phải tuân thủ 100%.

### m2 — Minor · Hằng số `CATALOG_ACTIVE_STATUS` khai mới nhưng không thay literal cùng file

`reportLookupOptions.ts:50` khai `CATALOG_ACTIVE_STATUS = 'HoatDong'`, trong khi ba literal
`'HoatDong'` ở dòng 46, 63, 75 của **cùng file** vẫn giữ nguyên. Một giá trị nghiệp vụ có hai cách
viết trong một file = nợ mới (luật 1 · `conventions-chung.md §1.2`). Nếu M3 được sửa theo hướng gửi
`trangThai` server-side thì hằng này dùng luôn cho cả 4 chỗ.

### m3 — Minor · Reset không tái áp khoảng ngày ⇒ preset hiện "Tháng này" mà Từ/Đến ngày rỗng

- `ReportRunnerPage.tsx:497` — `onReset={() => setValues({})}`.
- `values` dẫn xuất sẽ seed lại `kyBaoCao = 'ThangNay'`, nhưng effect backfill `fillsFrom`/`fillsTo`
  ở `base/domainKit/report/ReportParamsForm.tsx:292-308` có dep `[spec]` — `spec` không đổi nên
  effect **không chạy lại** ⇒ `tuNgay`/`denNgay` ở lại rỗng.
- Hậu quả: sau Reset, UI cho biết kỳ là "Tháng này" nhưng request gửi đi không có khoảng ngày.
  Không phải hồi quy (trước PR cũng rỗng), nhưng là mâu thuẫn hiển thị mới do PR tạo ra. Cần xác
  nhận BE có tự suy khoảng ngày từ `kyBaoCao` hay không trước khi chốt mức.

### m4 — Minor · Truy vết message: 8/8 mã `MSG_` của hai epic đều `THIEU`

```
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-14616_BangTinhPhanBoCCDC fe → OK 0 · THIEU 6
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10810_BCChiTietCCDC     fe → OK 0 · THIEU 2
```

Gồm `..._001/002` (xuất Excel/in thành công), `..._301/302/303` (không có quyền xem / Đến ngày ≥ Từ
ngày / không có quyền xuất), `..._201` (không có dữ liệu). Runner hiện dùng chuỗi chung
`baoCao.runner.*` không mang mã luật. PR tự nhận là "init" nên chấp nhận nợ, **nhưng phải ghi vào
mô tả PR** phần còn lại thay vì để trống body.

### m5 — Minor · Commit message thiếu `<scope>`

`feat: init bao cao ccdc` — chuẩn là `<type>(<scope>): <mô tả>` (luật 8), ví dụ
`feat(bao-cao): init báo cáo CCDC`. Tên nhánh `feat/bao-cao-ccdc` đạt chuẩn. Body PR để trống.

---

### N1 — Nit · Ép kiểu trong helper test

`test/reportParamDefaults.test.ts:7` — `return { … } as ReportParamField`. Không phải `any` nên không
chạm cổng cứng, nhưng `as` bỏ qua kiểm kiểu; nên dựng object đủ field hoặc dùng `satisfies`.

### N2 — Nit · Comment dẫn nguồn sai file seed

`reportCatalog.ts:92` ghi *"mã đã seed `V3:1315`"*; thực tế ở
`cell-app/src/main/resources/db/migration/V2__seed_data.sql:907-909`.

### N3 — Nit · Comment test mâu thuẫn với diff

`test/reportCatalog.bangTinhPhanBoCcdc.test.ts` ghi *"Nhóm `cong-cu-dung-cu` đã có từ PMKT-E-10810 —
không tạo nhóm mới"*, trong khi chính PR này tạo nhóm đó (`reportCatalog.ts:83`).

### N4 — Nit · Bản EN giữ viết tắt tiếng Việt

`en.ts` — `bangTinhPhanBoCcdc: 'CCDC Allocation Worksheet'` và `bcPhanBoCcdc.title` tương tự, lệch với
`chiTietCcdc: 'Tool & equipment detail report'` ngay bên cạnh (đã dịch "Tool & equipment").

---

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ✅ Không có secret · không `any` / `@ts-ignore` / `eslint-disable` mới · không `../../` **trong module features** (2 test dùng `../../../` ở `src/app` → m1) · i18n có ở **cả** `vi.ts` và `en.ts`, khóa khớp 1-1 (đã diff bằng script) · không chạm vùng đóng băng |
| B — Kiến trúc & 7 lỗi | Xem bảng dưới |
| C — Nghiệp vụ & truy vết | `trace.sh` **NOT-RUN** — không có thư mục `docs/doing/*-spec` cho hai epic này. `msg.sh` đã chạy: 8 mã `THIEU` (m4). Nghiệp vụ tự bịa: **không phát hiện** — nhãn cột `vi.ts` chép nguyên văn BA và có test khẳng định (`'ĐVT'`, `'Lũy kế đã PB'`, `'Đối tượng THCP'`, `'Không lấy CCDC đã hết giá trị tính đến đầu kỳ'`) |
| D — Vệ sinh diff & Git | `git status --porcelain` **sạch** (cổng cây commit ✅ — 4 file mới đều đã commit, không có `??` trong `src/`). Không code debug / `console.*` / `TODO` không mã. Diff đúng phạm vi `feat`, không refactor kèm. Commit message thiếu scope (m5) |

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ Không vi phạm. Diff nằm trong `src/app/pages/baoCao/` — shape sẵn có của report runner (không phải một màn `features/`), file mới đặt đúng ngăn: logic thuần → `reportParamDefaults.ts` cạnh các module anh em, test → `test/`. Không tách theo hành vi, không `mock.ts` |
| 2 | Version migration | ✅ N/A — PR thuần FE, không có file migration |
| 3 | Chưa test lại sau merge | ✅ N/A — `git rev-list --count 7f52a72..origin/develop` = **0** (nhánh đích không tiến thêm), tập file giao nhau **rỗng** |
| 4 | N+1 / request thừa | ⚠ Xem **M3** (lọc client sau phân trang). Không có request trong vòng lặp; `useQueries` có `queryKey` ổn định `['reportLookup', resource, congTyId, kyKeToanId]` + `staleTime` 5 phút. Lưu ý nhỏ: `withSpecDefaults` trả **object mới mỗi render** khi có default được seed — không gây refetch (không nằm trong queryKey nào) nhưng phá memo theo tham chiếu ở component con |
| 5 | Chưa tận dụng BaseController / BaseEntity | ✅ N/A — FE |
| 6 | Chưa tận dụng base FE | ✅ Không vi phạm — tái dùng `ReportParamsDrawer` / `ReportParamsForm` / `ReportResults` của `@domain-kit/report`, `http` của `@platform`; không dựng `<Table>` AntD trần, không copy từ `src/legacy/**` |
| 7 | Constant đặt sai chỗ | ⚠ Xem **m2**. `LOAI_CCDC_BASE` / `CATALOG_ACTIVE_STATUS` / `LOOKUP_PAGE_SIZE` khai đầu file dùng-một-chỗ là hợp lệ theo `conventions-chung.md §1.2`; vấn đề chỉ là literal trùng chưa gom |

## Điểm làm tốt

- `withSpecDefaults` tách thành hàm thuần, test được không cần dựng trang; đúng hướng "dẫn xuất khi
  render" thay vì `setState` trong effect.
- Giữ đúng ngữ nghĩa "người dùng thắng": chỉ điền khóa `undefined`, nên `localStorage` và thao tác
  bỏ tích (`ReportParamsForm.tsx:361` set `false` tường minh) không bị ghi đè — có test phủ
  (`defaultValue = false vẫn được seed`, `không đột biến object đầu vào`).
- i18n hai ngôn ngữ khóa khớp tuyệt đối, có test `it.each` khóa từng cột, và test khẳng định nguyên
  văn nhãn BA.
- Đã xác minh: `defaultValue` thật sự là code chết trước PR (`grep defaultValue` chỉ ra
  `reportModel.ts:275` khai Zod và 1 comment, không consumer nào) ⇒ mô tả vấn đề của PR là đúng.

---

## Đã chạy / chưa chạy

**Đã chạy (kiểm tĩnh)**

```bash
gh pr view 217 --json …
git diff --stat / --name-status 7f52a72..7ad3b6e7
git show 7ad3b6e7:<từng file>
git status --porcelain                      # sạch
git rev-list --count 7f52a72..origin/develop   # 0
comm -12 <(…develop) <(…head)                  # rỗng
git show origin/develop:…/ReportPermissionRegistry.java   (cell-app)
./docs/rules/msg.sh  pmkt-docs/ba/PMKT-E-14616_BangTinhPhanBoCCDC fe
./docs/rules/msg.sh  pmkt-docs/ba/PMKT-E-10810_BCChiTietCCDC      fe
./docs/rules/br.sh 5 8
diff khóa i18n vi ↔ en cho bcChiTietCcdc / bcPhanBoCcdc   # SAME cả hai
```

**Chưa chạy (chế độ nhanh)** — `npm run typecheck` · `lint` · `lint:boundaries` · `test` · `build` ·
`check:committed` · `trace.sh` (không có thư mục spec).

**Chưa xác minh được**: path thật của `LoaiCongCuDungCuController` (M2) — nằm trong
`cell-app/.../cell/master_data/**`, vùng đóng băng, lệnh grep bị hook chặn và **không** gỡ rule.

**BR đã đọc**: BR5, BR8. **BR chưa đọc trong phạm vi**: BR2/BR22/BR23/BR40 (danh mục dạng cây — liên
quan Q7 "cây trả phẳng" mà PR tự ghi nhận), BR6, BR25 (quyền), BR16/26/27 (thông báo — liên quan m4).

**Đã đọc**: cả 10 file của diff, cộng `base/domainKit/report/ReportParamsForm.tsx`,
`ReportParamsDrawer.tsx`, `reportModel.ts`, `features/danhMuc/taiSanCongCu/loaiCongCuDungCu/api.ts`,
`features/congCuDungCu/ghiTang/api/danhMucGhiTangCCDCApi.ts`,
`cell-app .../reporting/internal/{controller/ReportProxyController,service/ReportProxyService,service/ReportPermissionRegistry}.java`.

**Chưa đăng lên PR** — người gọi yêu cầu tuyệt đối không comment lên PR trong lượt này.
