# Review PR #208 — `ospgroupvn-pmkt/client`

**Chế độ: NHANH** (chỉ đọc + kiểm tĩnh bằng git/grep). KHÔNG chạy `typecheck` / `lint` /
`test` / `build`, KHÔNG tạo worktree, KHÔNG merge thử, KHÔNG sửa code, KHÔNG đăng comment lên PR
(user yêu cầu rõ). Kết luận dưới đây **không thay thế cổng test/build**.

| | |
|---|---|
| PR | #208 — "Feat: Báo cáo sổ nhật ký thu/chi tiền" (`datnt5920`, OPEN) |
| Nhánh | `feature/sonhatkythutien` → `develop` |
| head | `69ba7dc16` · base `7f52a7239` · merge-base `a4d3277e2` |
| Diff | 5 file · +160 / −19 |
| Commit | `789879a77` feat(bao-cao): i18n Sổ nhật ký thu tiền … · `69ba7dc16` feat(baoCao): Sổ nhật ký chi tiền PMKT-E-10786 — catalog + i18n |
| Epic | PMKT-E-10786 (chi tiền) + sửa lây sang PMKT-E-10784 (thu tiền) |

File trong diff:

```
M src/app/i18n/en.ts
M src/app/i18n/vi.ts
M src/app/pages/baoCao/reportCatalog.ts
M src/app/pages/baoCao/test/reportCatalog.soChiTietTaiKhoan.test.ts
A src/app/pages/baoCao/test/reportCatalog.soNhatKyChiTien.test.ts
```

Toàn bộ diff đã đọc — không có phần bỏ sót.

---

## Tổng hợp findings

| Mức | Số lượng | Mã |
|---|---|---|
| Blocker | 1 | B1 |
| Major | 4 | M1 · M2 · M3 · M4 |
| Minor | 4 | m1 · m2 · m3 · m4 |
| Nit | 4 | n1 · n2 · n3 · n4 |

**Kết luận: REJECT** (có Blocker). Cổng `typecheck`/`lint`/`lint:boundaries`/`test`/`build`
**chưa chạy** ở lượt này.

---

## Blocker

### B1 — Tiêu đề báo cáo tự đặt mã hiệu `S03a1-DN` / `S03a2-DN` và tự chẻ biến thể DN/DNN, không tài liệu Phase 1 nào quy định

- **File**: `client/src/app/i18n/vi.ts:804` (`soNhatKyThu.title`), `vi.ts:826` (`soNhatKyChi.title`);
  bản en tương ứng `en.ts:743` và `en.ts:765`.
- **Diff**:
  ```ts
  -    title: 'Sổ nhật ký thu tiền',
  +    title: { s03a1Dn: 'S03a1-DN: Sổ nhật ký thu tiền', s03a1Dnn: 'S03a1-DNN: Sổ nhật ký thu tiền' },
  ...
  +  soNhatKyChi: {
  +    title: { s03a2Dn: 'S03a2-DN: Sổ nhật ký chi tiền', s03a2Dnn: 'S03a2-DNN: Sổ nhật ký chi tiền' },
  ```
- **Nguồn ngược lại**: `pmkt-docs/ba/PMKT-E-10786_SoNhatKyChiTien/5.screens/SCR_SoNhatKyChiTien_KetQua.md:17`
  — *"**Header** - Tên báo cáo: Sổ nhật ký chi tiền"*. Không có tiền tố mã hiệu, không có biến
  thể theo thông tư.
- **Bằng chứng đếm được**: `grep -rn "S03a1\|S03a2" pmkt-docs/ba --exclude-dir=Phase_2` → **0 kết
  quả**. Các báo cáo khác có mã hiệu đều ghi rõ trong SCR (`SCR_SoNhatKyChung_KetQua.md:57-60`
  `S03a-DN`/`S03a-DNN`, `SCR_SoCai_KetQua.md:54` `S03b-DNN`, `SCR_SoChiTietTaiKhoan_KetQua.md:130`
  `S19-DNN`) — và ở những chỗ đó mã hiệu thuộc **mẫu in**, không phải header màn hình.
  Commit message `789879a77` viện dẫn "theo SCR PMKT-E-10784 (mã hiệu S03a1-DN/DNN)" nhưng SCR đó
  không chứa chuỗi `S03a1`.
- **Hậu quả**: `ReportRunnerPage.tsx:140` (`const title = spec.titleKey ? t(spec.titleKey) : reportId`)
  dùng chuỗi này làm **header màn hình** và `ReportRunnerPage.tsx:296` dùng làm **tên file Excel**
  (`a.download = \`${title}.xlsx\``). Người dùng và file xuất ra mang một mã biểu mẫu mà BA chưa
  chốt; nếu mã sai chuẩn thông tư thì đây là sai sót trên chứng từ/báo cáo nộp ra ngoài.
- **Luật**: CLAUDE.md gốc §"9 luật" luật 9 (*Không tự quyết nghiệp vụ — tài liệu im lặng thì dừng
  và hỏi*) và `bon-lop.md` Lớp A *"Nghiệp vụ tự bịa"*.
- **Cần làm**: BA xác nhận mã hiệu + quy tắc chọn DN/DNN, hoặc trả tiêu đề về đúng nguyên văn SCR.
  Ngoài ra không có nơi nào trong `client/` biết chế độ thông tư (`grep -rn "thongTu\|TT133\|TT200\|cheDoKeToan" client/src/platform client/src/app` → 0 kết quả), nên FE không tự chọn được
  giữa hai key — phải ghi rõ BE là bên chọn.

---

## Major

### M1 — Đổi `soNhatKyThu.title` từ `string` sang object là **breaking change** cho báo cáo Thu tiền đã chạy, không có bằng chứng BE đổi theo

- **File**: `client/src/app/i18n/vi.ts:804` · `en.ts:743`.
- **Cơ chế**: `ReportRunnerPage.tsx:140` gọi `t(spec.titleKey)` với `titleKey` do
  `report-service` phát. Nếu BE vẫn phát `soNhatKyThu.title` (giá trị đang chạy trên develop),
  key giờ trỏ vào một **object** → i18next không trả chuỗi, header hiển thị raw key và
  `${title}.xlsx` thành tên file rác.
- **Bằng chứng**: PR body **rỗng**, không link PR BE nào; `report-service` không nằm trong repo
  này nên không kiểm chứng được tại chỗ. Không có test nào chạm `soNhatKyThu.*`
  (`git ls-tree 69ba7dc src/app/pages/baoCao/test` — 5 file test, không file nào pin block này).
- **Hậu quả**: báo cáo Thu tiền đang `implemented: true` trên develop có thể vỡ tiêu đề ngay khi
  merge FE mà BE chưa lên.
- **Cần làm**: xác nhận PR BE tương ứng đã merge/đi cùng, và thêm test pin `soNhatKyThu.*`
  (mirror của `SO_NHAT_KY_CHI_KEYS`).

### M2 — Xoá 4 key i18n của báo cáo Thu tiền đang chạy, không thay thế, không test

- **File**: `client/src/app/i18n/vi.ts` / `en.ts`, block `soNhatKyThu`.
- **Key bị xoá**: `maTaiKhoanDoiUng`, `tenTaiKhoanDoiUng`, `ghiNo`, `ghiCoOverflow`.
- **Cơ chế**: `reportTableAdapter.ts:29` — `title: c.titleKey ? translate(c.titleKey) : (c.title ?? c.key)`.
  `translate` của i18next trả **chính key** khi không tìm thấy → cột nào BE còn phát các titleKey
  trên sẽ hiện `soNhatKyThu.ghiNo` làm tiêu đề cột, **không có lỗi nào bật lên**.
- **Ghi chú**: cột tiền của chính TK tiền ("Ghi nợ TK 111" cho Thu / "Ghi có TK 111" cho Chi, xem
  `SCR_SoNhatKyChiTien_KetQua.md:38`) **không còn key nào** ở cả hai block — nếu BE không gửi
  `title` literal thì cột này mất nhãn.
- **Cần làm**: đối chiếu danh sách `titleKey` thực tế `SoNhatKyTienReportDefinition` phát ra, rồi
  pin bằng test như block `soNhatKyChi`.

### M3 — Tham số mới `Tài khoản ngân hàng` (BR04) không có lookup resource ở FE → dropdown rỗng âm thầm

- **File**: `client/src/app/pages/baoCao/reportLookupOptions.ts:232-246` (`LOOKUP_FETCHERS`) —
  PR **không chạm** file này.
- **Nguồn**: `SCR_SoNhatKyChiTien_ChonThamSo.md` BR04 — dropdown lấy từ danh mục Tài khoản ngân
  hàng, chỉ TK "Đang hoạt động", enable/disable theo TK 111 hay 112.
- **Bằng chứng**: `grep -rn "tai-khoan-ngan-hang" client/src/app client/src/base` → 0.
  `neededLookupResources()` (`reportLookupOptions.ts:249-257`) **bỏ qua** mọi
  `lookupResource` không có fetcher, nên field vẫn render nhưng `options = []`.
- **Hậu quả**: đúng cái bẫy mà chính file này đã ghi chú hai lần ("dropdown rỗng âm thầm, không ai
  thấy sai" — chú thích `fetchLoaiChungTuOptions` và `fetchLyDoNhapOptions"). BR04 mất hẳn.
- **Thêm**: BR04 còn đòi enable/disable Tài khoản ngân hàng **theo giá trị** của tham số Tài khoản
  (111 → disable + clear, 112 → enable). `ReportParamsForm.tsx` không có cơ chế phụ thuộc giữa các
  field (`case 'lookup'` chỉ nhận `disabled` từ ngoài) — cần nêu rõ ai chịu trách nhiệm.

### M4 — BR02 giới hạn dropdown Tài khoản ở 111/112 + cấp con; fetcher hiện trả **toàn bộ** hệ thống tài khoản

- **File**: `client/src/app/pages/baoCao/reportLookupOptions.ts:37-45` (`fetchTaiKhoanOptions`,
  `GET TAI_KHOAN_BASE` không tham số lọc).
- **Nguồn**: `SCR_SoNhatKyChiTien_ChonThamSo.md` BR02 — *"Dropdown hiển thị các giá trị: '111',
  '112' và các tài khoản cấp con của 111, 112"*, mặc định `111`, single-select.
- **Hậu quả**: kế toán chọn được TK 331/511… → BE lọc theo TK không phải TK tiền → báo cáo rỗng,
  không kèm lỗi.
- **Lưu ý**: đây là wiring dùng chung, đã tồn tại từ `so-nhat-ky-thu-tien`; PR này mở rộng cùng
  wiring sang màn mới mà không nêu. Nếu BE đã khai một `lookupResource` hẹp hơn thì phải bổ sung
  fetcher tương ứng — chứ FE hiện chỉ có `'tai-khoan'`.

---

## Minor

- **m1 — BR03 thiếu lựa chọn "Tổng hợp" cho Loại tiền.** `reportLookupOptions.ts:56-61`
  (`fetchLoaiTienOptions`) chỉ map danh mục `ENT_mst_loai_tien`; BR03 (`SCR_..._ChonThamSo.md`)
  yêu cầu có thêm giá trị "Tổng hợp" (lấy toàn bộ chứng từ, quy đổi về đồng tiền hạch toán). Nếu
  BE không tự chèn option này thì tham số thiếu một nhánh nghiệp vụ.
- **m2 — `msg.sh`: 7/7 message của PMKT-E-10786 chưa có trong code FE.**
  `./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10786_SoNhatKyChiTien fe` → `OK 0 · THIEU 7`
  (`_001`, `_003`, `_201`, `_301`…`_304`). **Bối cảnh**: epic Thu tiền đã merge cũng `THIEU 4/4`
  — đây là hệ quả của màn runner dùng key chung, không phải lỗi PR này gây ra. Nên ghi nhận thành
  ticket riêng thay vì chặn merge.
- **m3 — `ghiCoTrong` / `ghiNoTrong` = `'----'` giống hệt nhau ở cả `vi.ts` lẫn `en.ts`.**
  Đây là chuỗi độn, không phải bản dịch. SCR đòi tiêu đề động "Ghi có TK [Tài khoản]" — theo luật
  2 phải là `t('key', { taiKhoan })`, không phải một literal. Nếu BE gửi `title` literal cho cột
  động thì hai key này là **dead key**, nên xoá.
- **m4 — Test chỉ pin danh sách key "chép tay".** `reportCatalog.soNhatKyChiTien.test.ts`
  (`SO_NHAT_KY_CHI_KEYS`, chú thích *"danh sách chép tay từ ChieuTien.CHI + messages.properties"*)
  không phát hiện được key BE thêm/đổi tên, và **không có** test đối xứng cho `soNhatKyThu` — đúng
  block mà PR này viết lại nhiều nhất (xem M1/M2).

## Nit

- **n1** — `reportCatalog.soNhatKyChiTien.test.ts:4-5` dùng `../../../i18n/vi` (3 cấp `../`), lệch
  luật 4 (path alias). Giống hệt 3 test anh em cùng thư mục → nợ kỹ thuật sẵn có, không phải lỗi PR.
- **n2** — Hàm `readPath()` nay bị sao chép ở **4** file test (`soNhatKyChiTien`,
  `soChiTietTaiKhoan`, `soNhatKyChung`, `tongHopTscd`); nên tách ra một helper dùng chung.
- **n3** — PR body **rỗng**: không link epic, không link PR `report-service` đi kèm. Với PR mà
  toàn bộ rủi ro nằm ở hợp đồng titleKey với BE (M1/M2), thiếu link là thiếu bằng chứng.
- **n4** — Tên nhánh `feature/sonhatkythutien`: sai nội dung (PR giao **chi** tiền), không
  kebab-case. Scope commit lệch nhau giữa hai commit (`bao-cao` vs `baoCao`).

---

## Lớp A–D

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ⚠ **B1** nghiệp vụ tự bịa (mã hiệu S03a1/S03a2, biến thể DN/DNN). Không secret · không `any`/`@ts-ignore` mới · i18n có đủ ở **cả** `vi.ts` và `en.ts` (đã đối chiếu tên key hai bên: khớp 100% cho cả `soNhatKyThu` và `soNhatKyChi`) · không chạm vùng đóng băng. |
| B — 7 lỗi hay gặp | bảng dưới |
| C — Nghiệp vụ & truy vết | `trace.sh` **NOT-RUN** — không có `docs/doing/*-spec` cho PMKT-E-10786 (`ls docs/doing` đã kiểm). `msg.sh` đã chạy → m2. BR đối chiếu tay từ SCR → B1, M3, M4, m1. |
| D — Vệ sinh diff & Git | ✅ commit message đúng `<type>(<scope>): <mô tả>`, không commit thẳng develop, không file `??` (head đã commit đủ 5 file, `git ls-tree` xác nhận `reportCatalog.soNhatKyChiTien.test.ts` có mặt). Nit n3, n4. |

### Bảng 7 lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ N/A — diff chỉ chạm `src/app/i18n/` và `src/app/pages/baoCao/` (tier app, không phải `features/<domain>/<module>/`); test nằm đúng `test/`. |
| 2 | Không đánh lại version migration | ✅ N/A — repo FE, không có thư mục migration. |
| 3 | Chưa test lại sau khi merge | ✅ N/A — nhánh tụt **2 commit** so với `develop` (`git rev-list --count a4d3277..7f52a72` = 2) nhưng **0 file giao nhau** (`comm -12` giữa hai danh sách `--name-only` → rỗng). Không cần merge thử. |
| 4 | Chưa tối ưu / N+1 | ✅ N/A — diff không thêm request nào. (Lưu ý ngoài diff: `useReportLookupOptions` đã cache `staleTime` 5 phút.) |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ N/A — không có code Java. |
| 6 | Chưa tận dụng base FE | ✅ — dùng đúng runner chung `ReportRunnerPage` + `@domain-kit/report`, không dựng màn riêng. Phần **thiếu** wiring lookup là M3/M4, không phải tự dựng lại base. |
| 7 | Constant đặt sai chỗ | ✅ — không có magic value mới; entry catalog và chuỗi UI đều qua `REPORT_CATALOG` / key i18n. Mã `MSG_…` chưa thành hằng số → xem m2. |

---

## Lệnh đã chạy

```bash
gh pr view 208 --json ...
git diff <merge-base> 69ba7dc --stat / --name-status / -- <từng file>
git show 69ba7dc:<file>                     # reportLookupOptions.ts, ReportParamsForm.tsx, test/*
git ls-tree -r --name-only 69ba7dc src/app/pages/baoCao
git rev-list --count a4d3277..7f52a72 ; comm -12 <(...) <(...)
grep -rn "soNhatKyThu|soNhatKyChi|tai-khoan-ngan-hang|thongTu|TT133" client/src
grep -rn "S03a1|S03a2|BCNhatKyChiTien" pmkt-docs/ba --exclude-dir=Phase_2
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10786_SoNhatKyChiTien fe
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10784_SoNhatKyThuTien fe     # đối chứng
./docs/rules/br.sh 25
```

## BR / tài liệu đã đọc

- BR chung: **BR25** (phân quyền) — xác nhận mô hình ẩn menu / 403 khớp `REPORT_VIEW_PERMISSIONS`
  + `ReportRunnerPage` trả `<Forbidden/>`.
- BR nội bộ màn (Phase 1): `SCR_SoNhatKyChiTien_ChonThamSo.md` BR01–BR05 (đọc đủ);
  `SCR_SoNhatKyChiTien_KetQua.md` BR01 + bảng cột (đọc 110/175 dòng).
- **Chưa đọc**: `SCR_SoNhatKyChiTien_KetQua.md` dòng 110–175 (BR02 tách dòng/cột động, BR03
  hyperlink), `SCR_SoNhatKyThuTien_KetQua.md`, `UC_*` của cả hai epic, BR chung **BR8** (kỳ báo
  cáo), **BR7/BR18** (định dạng số tiền), **BR16/26/27** (message) — nằm ở tầng render chung, ngoài
  diff.

## Chưa kiểm chứng

- `typecheck` · `lint` · `lint:boundaries` · `test` · `build` — **NOT-RUN, chế độ nhanh**.
- Hợp đồng `titleKey`/`lookupResource` thực tế của `report-service` (repo khác, không có ở workspace)
  → M1, M2, M3, M4, m1 đều cần một lượt đối chiếu với BE trước khi kết luận cuối.
- `implemented: true` cho `so-nhat-ky-chi-tien` — chú thích của `reportCatalog.ts` đòi "verified
  against the running BE"; không xác minh được ở chế độ nhanh. Nếu BE chưa có ReportDefinition,
  `ReportRunnerPage` sẽ gọi API và lỗi thay vì hiện "coming soon".

**Chưa đăng lên PR — user yêu cầu rõ không comment.**
