# Review PR #14 — `ospgroupvn-pmkt/report-service`

| | |
|---|---|
| PR | #14 — "HoanVN: create kiem ke kho" · tác giả `vuhoan-tsbt` · OPEN |
| Nhánh | `feature/kiem_ke_kho` → `develop` |
| head | `e0fe4c71151ad59594f6f9a787a7c28ea27ff434` |
| base | `ccbca42bd0b8df5d51a910a6a1b727e7737f3128` = merge-base với `origin/develop` (đã xác minh) |
| Quy mô | 22 file · +4271 / −443 |
| Chế độ review | **NHANH** — chỉ đọc + kiểm tĩnh bằng git/grep. KHÔNG chạy test/build, không worktree, không merge thử |
| Working tree | sạch (`git status --porcelain` rỗng) |

**Nội dung thực tế của PR** (khác hẳn tiêu đề): (1) thêm 2 báo cáo mới *Bảng kê phiếu nhập kho*
(PMKT-E-10478) và *Bảng kê phiếu xuất kho* (PMKT-E-10529); (2) viết lại *Sổ cái* từ một-tài-khoản
sang nhiều-tài-khoản, phân trang theo tài khoản, đổi mốc lũy kế sang năm tài chính; (3) thêm bộ lọc
**Chi nhánh** cho cả ba báo cáo; (4) thay `TaiKhoanRepository` bằng `LookupLabelRepository` tổng
quát 13 tài nguyên. Không có "kiểm kê kho".

---

## Tổng hợp findings

| Mức | Số lượng | Mã |
|---|---|---|
| Blocker | 2 | B1, B2 |
| Major | 7 | M1…M7 |
| Minor | 7 | m1…m7 |
| Nit | 4 | n1…n4 |

**Kết luận: REJECT** (có Blocker). Cổng test/build **chưa chạy** (chế độ nhanh) — sau khi xử lý các
mục dưới đây vẫn phải chạy `./gradlew :report-service:build` trước khi merge.

---

## Blocker

### B1 — Toàn bộ tính năng "Chi nhánh" dựa trên BR50 / BR5 **Phase 2**, trong khi repo đang làm Phase 1

- Nguồn: CLAUDE.md gốc §BR — "Repo đang làm Phase 1… Không có BR50 trong phạm vi Phase 1 — thấy tài
  liệu nhắc BR50 thì đó là tài liệu Phase 2, bỏ qua"; `./docs/rules/br.sh --list` dừng ở **BR49**.
  `pmkt-docs/ba/Phase_2/**` là vùng đóng băng.
- Diff tự khai nguồn là Phase 2 ở nhiều chỗ:
  - `ReportDefinitionSupport.java:28` — "Khoá tham số Chi nhánh (BR50, Phase 2)"
  - `CauHinhChiNhanhRepository.java:14` — "`iam_tenant.co_chi_nhanh` — BR50.1 của Phase 2"
  - `SoCaiReportDefinition.java` javadoc — "Chi nhánh (BR5 Phase 2 / BR50)"
  - `BangKePhieuNhapRepository.Filters` — "BR50 — chi nhánh, so khớp ĐÚNG BẰNG"
- Hậu quả: tính năng nghiệp vụ ngoài phạm vi Phase 1 vào 3 báo cáo, cộng hạ tầng dùng chung
  `ReportDefinitionSupport.chiNhanhParam` mà javadoc nói sẽ áp cho 8 báo cáo. Đúng dạng "nghiệp vụ
  không có nguồn" của Lớp A — chạy êm cho tới lúc đối chiếu số liệu.
- Cần: BA xác nhận bằng văn bản rằng report-service được phép cài BR50 sớm, **hoặc** tách phần Chi
  nhánh ra khỏi PR này.

### B2 — Xuất file Sổ cái: trần dòng và ngân sách nạp bị vô hiệu do đổi đơn vị `totalItems`

- `SoCaiReportDefinition.fetchRows` (cuối hàm): `ReportPage.of(rows, tongSoTaiKhoan, totals)` —
  `totalItems` nay là **số TÀI KHOẢN**, không còn là số dòng; `pg.getPageSize()` cũng được hiểu là
  số tài khoản.
- `ReportRunService.java:515-527` (không đổi trong PR) giả định đơn vị là **DÒNG**:
  `fetchSize = maxRows + 1` truyền thẳng vào `PageRequest.of(0, fetchSize)`, và guard
  `if (rowCap != null && page.totalItems() > rowCap) → 413 REPORT_EXPORT_TOO_LARGE`.
- Trigger: xuất xlsx/csv Sổ cái với tham số mặc định (bỏ trống tài khoản = **tất cả**; javadoc của
  chính PR ghi DB dev có 926 tài khoản).
- Actual: nạp tới `maxRows + 1` **tài khoản**, mỗi tài khoản nở ra 5 dòng băng + N dòng chi tiết →
  số dòng thực tế gấp nhiều lần trần; guard so số tài khoản với trần dòng nên **không bao giờ bắn 413**.
- Expected: trần dòng của renderer phải chặn được đúng số dòng sinh ra.
- Hậu quả: OOM / treo request / file xuất khổng lồ. Hồi quy do PR gây ra (bản cũ một tài khoản,
  `totalItems = rows.size()`).

---

## Major

### M1 — Sổ cái: hai cột vừa được mở sortable nhưng repository **bỏ qua** cột sắp xếp
- `SoCaiReportDefinition`: `COT_SAP_XEP = Set.of(C_SO_CHUNG_TU, C_NGAY_HACH_TOAN, C_NGAY_CHUNG_TU)`;
  `ngayChungTu` và `soChungTu` được thêm `.withServerSortable()`.
- `fetchRows`: gọi `validateSortKey(p.sortKey().orElse(null))` rồi **vứt bỏ** sortKey — chỉ chiều
  (`tangDan`) đi xuống `soCaiRepository.chiTiet(…, tangDan)`.
- `SoCaiRepository.CHI_TIET_TEMPLATE`: `ORDER BY tk.so_tai_khoan, sc.ngay_hach_toan %s, sc.so_chung_tu`
  — cột sắp xếp **hardcode** là `ngay_hach_toan`.
- Trigger: người dùng bấm sắp xếp cột "Số chứng từ" hoặc "Ngày chứng từ".
- Actual: 200 OK, thứ tự **không đổi**. Expected: sắp theo cột đã chọn.
- Hậu quả: tính năng câm — không lỗi, không log, người dùng tưởng dữ liệu đúng thứ tự mình chọn.

### M2 — Sổ cái: dòng "Tổng cộng" chỉ cộng **trang hiện tại**, trong khi `totalItems` là toàn bộ
- `fetchRows`: `tongNo`/`tongCo` cộng dồn trong vòng `for (… : trang)` — chỉ tài khoản của trang.
- Đối chiếu: `BangKePhieuNhapRepository.totals(filters)` trong cùng PR cố ý chạy trên **toàn bộ tập
  đã lọc** ("trên TOÀN BỘ tập đã lọc, không phải trang hiện tại (BR03c)"). Hai báo cáo cùng PR dùng
  hai quy ước ngược nhau.
- Hậu quả: báo cáo nhiều hơn một trang → dòng Tổng cộng **sai**. Kèm theo `dataVersion` dùng
  `fetchedPage.totals()` nên vân tay dữ liệu đổi khi lật trang → cảnh báo `STALE_REPORT_RUN` giả.

### M3 — Chưa test lại sau khi merge: **xung đột thật** với `develop` (lỗi hay gặp #3)
Đo bằng git, không chạy test:
- `git rev-list --count <MB>..origin/develop` → **11** commit.
- `comm -12` → **2 file giao nhau**: `…/definitions/ReportDefinitionSupport.java` và
  `src/main/resources/messages.properties`.
- `git merge-tree --write-tree origin/develop origin/pr/14` →
  `CONFLICT (content): Merge conflict in src/main/resources/messages.properties`.

`develop` đã đổi `ReportDefinitionSupport` thành `public` (đợt Sổ nhật ký chung / Sổ chi tiết tài
khoản) và thêm ~37 dòng vào `messages.properties`. Phải rebase/merge `develop` rồi chạy lại cổng.

### M4 — Thiếu key i18n phía FE (luật 2)
Javadoc của chính PR yêu cầu "khoá này phải có mặt ở CẢ BA nơi: `vi.ts`, `en.ts` và
`messages.properties`". Kiểm `client/src/app/i18n/`:

| Khoá | vi.ts | en.ts |
|---|---|---|
| `bangKePhieuNhap.*` (33 khoá) | KHÔNG CÓ | KHÔNG CÓ |
| `bangKePhieuXuat.*` (33 khoá) | KHÔNG CÓ | KHÔNG CÓ |
| `soCai.chiNhanh` | KHÔNG CÓ | KHÔNG CÓ |
| `soCai.taiKhoan` (cột chi tiết mới) | KHÔNG CÓ | KHÔNG CÓ |

Hậu quả: mở màn hai báo cáo mới, FE hiện **khoá thô** (`bangKePhieuNhap.ngayHachToan`) trên mọi tiêu
đề cột và nhãn tham số. Cần PR đồng hành ở `client/` trước khi deploy.

### M5 — Sửa nhãn Sổ cái ngoài phạm vi, và làm **lệch** file xuất so với màn hình
`messages.properties`: `soCai.maTaiKhoanDoiUng` đổi từ "TK đối ứng" → "Tài khoản đối ứng";
`soCai.tenTaiKhoanDoiUng` đổi từ "Tên TK đối ứng" → "Tên tài khoản đối ứng".
`client/src/app/i18n/vi.ts:559` vẫn là `maTaiKhoanDoiUng: 'Mã TK đối ứng'`. Chính PR này viết "Chữ
PHẢI trùng từng ký tự với vi.ts". Actual: header Excel khác header màn hình. Ngoài ra đây là thay
đổi không thuộc phạm vi PR, không có yêu cầu nghiệp vụ kèm theo.

### M6 — Lọc chi nhánh **nới rộng hơn** quy định BA (rò dữ liệu ngoài phạm vi được cấp)
`SoCaiRepository.locChiNhanh` javadoc tự khai: "Rỗng ở đây nghĩa là 'mọi chi nhánh của tenant',
KHÔNG phải 'mọi chi nhánh trong phạm vi người dùng được cấp' như BR5 mô tả… với tenant nhiều chi
nhánh và người dùng bị giới hạn thì đây là chỗ nới rộng hơn BA".
Trigger: tenant nhiều chi nhánh, người dùng chỉ được cấp 1 chi nhánh, chạy Sổ cái không chọn chi nhánh.
Actual: thấy số liệu **mọi chi nhánh**. Luật 9 / cổng đặc tả: thiếu hạ tầng thì mở mục OPEN và hỏi,
không code theo cách hiểu rộng hơn rồi ghi chú lại.

### M7 — PR trộn nhiều việc không liên quan; tiêu đề/nhánh/body không phản ánh nội dung
- 2 commit: `HoanVN: create kiem ke kho`, `HoanVN: create kiem ke kho and so cai`.
- Nội dung: 2 báo cáo mới + viết lại Sổ cái (đổi hợp đồng tham số `taiKhoanId` → `taiKhoanIds`, đổi
  đơn vị phân trang, đổi mốc lũy kế từ 01/01 dương lịch sang **năm tài chính** `dauNamTaiChinh`) +
  refactor `TaiKhoanRepository` → `LookupLabelRepository` (ảnh hưởng mọi báo cáo) + đổi
  `filterVisibleColumns` dùng chung.
- PR body **rỗng**; không chỗ nào giải thích vì sao mốc lũy kế đổi, hay nguồn BA cho việc đó.
- Lớp A: "PR trộn feat + refactor". Hậu quả: không review/rollback từng phần được.

---

## Minor

- **m1** — Commit message sai chuẩn luật 8 `<type>(<scope>): <mô tả>`: "HoanVN: create kiem ke kho".
- **m2** — 4 file test mới (`BangKePhieuNhapChiNhanhTest`, `BangKePhieuXuatReportDefinitionTest`,
  `SoCaiTinhChatTaiKhoanTest`, `LookupLabelRepositoryTest`) **không gắn `@Tag("unit")`** → không vào
  làn nhanh `./gradlew unitTest` (`build.gradle.kts:112` `includeTags("unit")`). Chúng đều là test
  thuần mock/hằng số, đủ điều kiện vào làn đó.
- **m3** — `ManualVisualQaGeneratorTest.java:96-98` vẫn gửi `"taiKhoanId"` cho `so-cai` (tham số nay
  không còn tồn tại → bị bỏ qua lặng lẽ, sinh QA artifact cho *tất cả* tài khoản); comment "lọc theo
  MỘT tài khoản" đã lỗi thời.
- **m4** — `ReportRunService.filterVisibleColumns` đổi hành vi **dùng chung cho mọi báo cáo** (cột
  `hidden` không bao giờ vào file xuất). Có test mới bao (`runExportNeverIncludesHiddenColumns…`,
  `runExportDropsHiddenColumnsEvenWhenTheFeListsThem`) nên không nâng mức, nhưng là thay đổi hợp
  đồng xuất file nằm ngoài phạm vi PR — nên tách PR riêng.
- **m5** — `BangKePhieuNhapReportDefinition.fetchRows`: `Map.of("soLuong", …)` dùng **chuỗi literal**
  thay vì hằng `C_SO_LUONG`; bản Bảng kê phiếu **xuất** (dòng 409) đã dùng đúng hằng → hai file song
  sinh lệch nhau, đúng thứ javadoc của chính file cảnh báo.
- **m6** — Tìm kiếm trong `BangKePhieuNhapRepository.FROM_WHERE_TEMPLATE`:
  `LIKE bo_dau(lower('%' || :kw || '%'))` — không escape `%` / `_`. Người dùng gõ `%` hoặc `_` thành
  ký tự đại diện, ra kết quả rộng bất thường (cùng vấn đề ở bản phiếu xuất).
- **m7** — Nhãn hiển thị hardcode trong repository: `LY_DO_NHAP_MUA = "Nhập mua"`,
  `LY_DO_NHAP_DIEU_CHINH_GIA = "Điều chỉnh giá hàng nhập kho"` — đây là **giá trị ô** của cột "Lý do
  nhập", không qua `messages.properties`/i18n như mọi giá trị khác của cùng cột (luồng Kho lấy
  `pnk.ten_ly_do_nhap` từ DB). Không dịch được sang `en`.

## Nit

- **n1** — Nhánh `feature/kiem_ke_kho`: snake_case (chuẩn là kebab `tên-mo-ta`) và tiền tố `feature/`
  trong khi repo đang dùng lẫn `feat/`.
- **n2** — PR body rỗng.
- **n3** — `SoCaiReportDefinition.java` còn hai dòng trống thừa sau khai báo `P_TAI_KHOAN_IDS`.
- **n4** — Nhãn dòng tổng hợp Sổ cái ("Số dư đầu kỳ", "Cộng phát sinh trong kỳ", …) và nhãn option
  ("Ghi sổ", "Mẫu số lượng và giá trị", …) là chuỗi tiếng Việt hardcode trong Java. Đúng theo mẫu
  sẵn có của repo (`ReportDefinitionSupport` trên `develop` cũng vậy) nên chỉ ghi nhận, không tính
  là vi phạm mới.

---

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | OK — file mới đều nằm đúng `internal/repository`, `internal/service/definitions`, `internal/service/utils`; không có file phẳng ra gốc module, không tạo `api/` thừa. Ghi chú: `report-service/CLAUDE.md` khai base package `vn.vtt.pmkt.report` nhưng cả repo dùng `vn.vtt.pmkt.cell.reporting` — lệch **có sẵn**, không do PR. |
| 2 | Không đánh lại version migration | N/A — PR không thêm/sửa migration nào; repo chỉ có `src/main/resources/db/bieu_mau/V20260908210000__bm_bieu_mau.sql`. Rủi ro liên quan: `iam_tenant.co_chi_nhanh` và `iam_tenant.ngay_bat_dau_nam_tai_chinh` được đọc nhưng schema do service khác quản — cần xác nhận cột đã có trên mọi môi trường. |
| 3 | Chưa test lại sau merge | VI PHẠM — **M3**: tụt 11 commit, 2 file giao nhau, `merge-tree` báo CONFLICT ở `messages.properties`. |
| 4 | N+1 / chưa tối ưu | OK về hướng: Sổ cái gom từ ~4 truy vấn/tài khoản xuống 5 truy vấn/trang; `LookupLabelRepository.nhanTheoId` một truy vấn cho cả danh sách id. NHƯNG xem **B2**: ngân sách nạp khi xuất file bị hỏng. |
| 5 | Chưa tận dụng BaseController / BaseEntity | N/A — không có Controller/Entity mới; các repository là reader native-SQL của `reporting`, đúng mẫu sẵn có (`SoNhatKyChungRepository`, `BangTongHopPhatSinhTaiKhoanRepository`). |
| 6 | Chưa tận dụng base FE | N/A — PR không chạm `client/`. (Nhưng xem **M4**: thiếu phần FE đi kèm.) |
| 7 | Constant đặt sai chỗ | VI PHẠM nhẹ — **m5** (literal `"soLuong"` thay vì hằng), **m7** (nhãn hiển thị làm hằng trong repository thay vì i18n). Còn lại: khoá cột/tham số đều đã `private static final`; enum dùng chung đặt ở `service/utils` có lý do ghi rõ — chấp nhận được. |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | VI PHẠM: **B1** (nghiệp vụ Phase 2 không có nguồn trong Phase 1), **M7** (PR trộn feat + refactor), **M4** (thiếu i18n). Không có secret trong diff. Không có Controller mới nên các mục Controller / `ApiResponse<T>` / `@RestControllerAdvice` là N/A; lỗi nghiệp vụ vẫn ném qua `ApiException.badRequest`, không try/catch thủ công, không nuốt exception. Không chạm vùng đóng băng — `master_data` chỉ bị ĐỌC qua tên bảng `mst_*` trong native SQL, đúng thông lệ sẵn có của `reporting`, không copy kiến trúc. |
| B — Kiến trúc & 7 lỗi | xem bảng trên. |
| C — Nghiệp vụ & truy vết | `trace.sh` · `msg.sh`: **NOT-RUN** — không có thư mục spec cho PMKT-E-10478 / PMKT-E-10529 / Sổ cái trong `docs/doing/`, và diff trải trên ≥3 epic nên không có một thư mục PYC đơn để truyền vào; không đoán bừa PYC. Đối chiếu nghiệp vụ vì vậy dựa trên CLAUDE.md gốc §BR (BR1…BR49), javadoc tự khai nguồn trong diff, và hợp đồng kỹ thuật của `ReportRunService`. |
| D — Vệ sinh diff & Git | VI PHẠM nhẹ: **m1** (commit message), **n1** (tên nhánh), **n2** (body rỗng), **M5/m4** (boy-scout ngoài phạm vi). Cổng cây commit OK: `git status --porcelain` rỗng, không file `??` trong `src/`; file bị xoá (`TaiKhoanRepository.java`) không còn tham chiếu treo — `git grep` ở head chỉ ra các lớp tên khác (`BangTongHopPhatSinhTaiKhoanRepository`, `SoChiTietTaiKhoanRepository`). |

## BR đã đọc / chưa đọc

- Đã dùng: `./docs/rules/br.sh --list` (mục lục; xác nhận dãy dừng ở **BR49** — cơ sở cho B1).
- KHÔNG kéo nội dung BR chi tiết: mọi mã `BR01…BR11`, `BR1.3`, `BR1.4`, `BR50.x` trong diff đều là
  **BR nội bộ màn** của các file `SCR_*` (Bảng kê phiếu nhập/xuất, Sổ cái) hoặc BR Phase 2, không
  phải BR chung của `business_rules.md`.
- **Chưa đối chiếu được** (không có trong repo hoặc thuộc Phase 2): `SCR_BangKePhieuNhap*`,
  `SCR_BangKePhieuXuat*`, `SCR_SoCai_ChonThamSo`, `SCR_SoCai_KetQua`, `1.function-breakdown.md`,
  `pmkt-docs/ba/SoCai.md`, BR50. Các quyết định nghiệp vụ trong diff (hai mẫu báo cáo, quy tắc tính
  chất tài khoản quyết định cột Nợ/Có, ba luồng nguồn của Bảng kê, mốc lũy kế theo năm tài chính)
  **chưa được xác minh bằng nguồn** — cần BA rà.

## Lệnh đã chạy

- `gh pr view 14 --json …`
- `git merge-base origin/develop origin/pr/14`
- `git diff --stat` / `--name-status <MB> origin/pr/14`
- `git status --porcelain` (rỗng)
- `git rev-list --count <MB>..origin/develop` → 11
- `comm -12` trên hai danh sách `git diff --name-only` → 2 file
- `git merge-tree --write-tree origin/develop origin/pr/14` → CONFLICT `messages.properties`
- `git show origin/pr/14:<các file chính>`
- `git grep -n` cho `TaiKhoanRepository` và `"taiKhoanId"` ở head
- `grep -rn` cho `bangKePhieuNhap` / `bangKePhieuXuat` / `maTaiKhoanDoiUng` trong `client/src/app/i18n/`
- `./docs/rules/br.sh --list`

## Chưa đọc / chưa kiểm

- **Cổng test/build: NOT-RUN — chế độ nhanh.** `./gradlew :report-service:build` và `unitTest` chưa chạy.
- Đã đọc đầy đủ: `BangKePhieuNhapRepository`, `BangKePhieuNhapReportDefinition`,
  `LookupLabelRepository`, `CauHinhChiNhanhRepository`, `SoCaiRepository`, `SoCaiTinhChatTaiKhoan`,
  `BangKeMauBaoCao`, `BangKeTrangThai`, `messages.properties`, diff `ReportRunService` /
  `SoCaiReportDefinition` / `SoCaiE2eTest`.
- Chỉ đọc lướt (đối chiếu chênh lệch với bản "phiếu nhập" song sinh): `BangKePhieuXuatRepository.java`
  (504 dòng), `BangKePhieuXuatReportDefinition.java`. B2/M1/M2 không áp cho hai file này; m5/m6 có áp.
- Chưa đọc: `BangKePhieuXuatReportDefinitionTest.java`, `SoCaiReportDefinitionTest.java`,
  `SoCaiTinhChatTaiKhoanTest.java`, `BangKePhieuNhapChiNhanhTest.java` (chỉ xem phần đầu để kiểm
  `@Tag`), phần lớn diff `ReportControllerTest.java`.

---

**Kết luận: REJECT** — B1, B2. Sau khi xử lý xong Blocker thì còn M1…M7 ở mức REQUEST CHANGES.
Cổng test/build chưa chạy ở lượt này.

*Không đăng comment lên PR theo yêu cầu của lượt chạy này.*
