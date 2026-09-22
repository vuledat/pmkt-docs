# Review PR #10 — ospgroupvn-pmkt/report-service

**Tiêu đề:** Cell merging, page fitting and border fixes for xlsx/PDF exports
**Tác giả:** sangnv92 · **Trạng thái:** OPEN · **Base:** `develop` · **Head:** `feat/gop-o-ngang-doc-cho-file-xuat` @ `1e71e4e`
**merge-base:** `da5f557` · **develop:** `caec7c3` (20 commit trước head)
**Quy mô:** 36 file · +2.908 / −355

> **CHẾ ĐỘ NHANH** — chỉ đọc + kiểm tĩnh bằng git/grep. KHÔNG chạy test, KHÔNG build,
> KHÔNG tạo worktree, KHÔNG sửa code, KHÔNG đăng comment lên PR (user yêu cầu rõ).

Lưu ý cấu trúc: head là **merge commit của PR #11** ("Cap conditions-text item list"), PR #11 nhắm
thẳng vào nhánh này và đã MERGED, nên diff PR #10 bao gồm luôn nội dung PR #11 (finding M2 đến từ đó).

## Tổng hợp findings

| Mức | Số lượng |
|---|---|
| Blocker | 1 |
| Major | 5 |
| Minor | 6 |
| Nit | 4 |

## Blocker

### B1 — Nhánh tụt 20 commit sau develop, merge thử vỡ 11 file (lỗi #3)

Đo bằng git, không chạy test:

- `git rev-list --count da5f557..origin/develop` = **20**
- `comm -12` trên tên file thô: `build.gradle.kts`, `src/main/resources/messages.properties`,
  `src/main/resources/templates/report-template.jrxml`
- `git merge-tree --write-tree --name-only origin/develop origin/pr/10` → **11 file xung đột**:
  `ReportRunService.java`, `SoCaiReportDefinition.java`, `SoNhatKyThuTienReportDefinition.java`,
  `ExportSupport.java`, `JasperPdfRenderer.java`, `messages.properties`, `report-template.jrxml`,
  cộng 4 file test (`ExportSupportTest`, `JasperPdfRendererTest`, `PdfTemplateScaffoldGeneratorTest`,
  `PoiXlsxRendererTest`).

Nặng hơn con số xung đột: `develop` đã đổi base package **vn.dopai.pmkt → vn.vtt.pmkt** cho **toàn
bộ** file mà PR này sửa (`git diff --name-status -M da5f557 origin/develop` cho R079–R099 trên mọi
file `reporting/**`). PR vẫn nằm trên cây `vn/dopai/`. Rename-detection cứu được phần auto-merge,
nhưng 11 file trên phải giải tay và mọi import `vn.dopai` mới thêm trong PR đều sai package sau merge.

Develop còn thêm code mới tiêu thụ cùng API mà PR đổi chữ ký: `SoChiTietTaiKhoanReportDefinition`,
`SoNhatKyChungReportDefinition`, `bangtonghopphatsinh/**` — chúng chưa biết `ReportColumn.leaves()`,
`withPrecision()`, `ReportLayout.Orientation.AUTO`, `SheetColumn` 10 tham số, `BodyRow` 6 tham số.
Auto-merge không báo xung đột ở đó, nên sẽ **đỏ lúc compile**, không phải lúc merge.

Hậu quả: xanh 100% trên nhánh, đỏ lúc merge vào develop.
Mức: bảng bảy lỗi #3 là Major, nâng **Blocker** vì giao nhau ở file cấu hình/tài nguyên
(`messages.properties`, `report-template.jrxml`).
Yêu cầu: merge develop vào nhánh, đổi package sang `vn.vtt.pmkt`, chạy lại cổng.

## Major

### M1 — @SuppressWarnings("unchecked") lạc chỗ, page() mất suppression

`src/main/java/vn/dopai/pmkt/cell/reporting/internal/repository/BangKeChungTuRepository.java:124`

Thứ tự hiện tại trong file: `@SuppressWarnings("unchecked")` → khối javadoc → `public enum SortColumn`
→ (không còn annotation) `public List<Row> page(...)`, bên trong có
`List<Object[]> raw = q.getResultList();`

- Trigger: enum mới được chèn vào **giữa** annotation và `page()`.
- Actual: annotation áp cho `enum SortColumn` (vô nghĩa ở đó); `page()` — nơi thật sự có unchecked
  conversion từ `Query.getResultList()` — mất suppression. Khối javadoc nằm **sau** annotation nên
  javadoc tool cũng không nhận nó là javadoc của enum.
- Expected: annotation ngay trên `page()`; javadoc ngay trên enum.
- Hậu quả: warning compile quay lại (checkstyle đang `isIgnoreFailures = true` nên build không đỏ);
  tài liệu enum biến mất khỏi javadoc.
- Đối chiếu: cùng thay đổi ở `BangCanDoiTaiKhoanRepository.java` đặt **đúng** — enum trước,
  annotation sau, ngay trên `page()`. Chỉ một trong hai file bị lỗi.

### M2 — Hardcode text UI tiếng Việt + cắt danh sách điều kiện lọc không có nguồn

`src/main/java/vn/dopai/pmkt/cell/reporting/internal/service/ReportRunService.java:68,115`

Code: `private static final int MAX_DISPLAY_ITEMS = 5;` và trong `joinCollection`:
`if (collection.size() > MAX_DISPLAY_ITEMS) { return "Đã chọn " + collection.size() + " mục"; }`

- Nguồn: CLAUDE.md gốc luật 2 — không hardcode text UI, chuỗi động phải qua key + tham số, **không
  cộng chuỗi**. Repo có sẵn `messages.properties` + `ReportTextResolver`, và chính PR này còn thêm
  key mới `common.pdfCatChu` vào đó, nên đường đi đúng đã có sẵn.
- Nghiệp vụ không có nguồn: vượt 5 mục thì dòng "điều kiện lọc" trên bản in **không còn nêu tên tài
  khoản/đối tượng nào đã chọn**. Với báo cáo kế toán, dòng điều kiện là bằng chứng bản in được lập
  theo tiêu chí gì. Không BR nào, không spec nào trong diff yêu cầu ngưỡng 5.
- Hậu quả: hai người chạy hai bộ lọc khác nhau cùng ra một dòng "Đã chọn 12 mục"; không đối chiếu
  lại được bản in với tham số đã chạy.
- Đề xuất: đưa chuỗi vào `messages.properties` với tham số {0}; ngưỡng cắt cần BA chốt.

### M3 — Đổi hợp đồng API ngoài phạm vi, không có nguồn BR/spec

`ReportRunService.java:186-243` · `SoCaiReportDefinition.java:178-189` ·
`SoNhatKyThuTienReportDefinition.java:132-143`

- `requireSortableColumn` / `requireSearchableColumn`: request từng trả **200** (bỏ qua `sort` lặng
  lẽ) nay ném **400 VALIDATION_ERROR**.
- `SoCai` và `SoNhatKyThuTien` đổi `searchMode` từ mặc định **server → client** — FE phải tự lọc.
- Vấn đề không phải quyết định sai (lập luận trong javadoc hợp lý), mà là: (a) nằm hoàn toàn ngoài
  phạm vi "cell merging, page fitting and border fixes" mà tiêu đề PR khai; (b) mô tả PR không nhắc
  một chữ về hai thay đổi này; (c) không trích BR/spec/UC nào.
- Nguồn: luật 9 + Lớp A "Nghiệp vụ tự bịa"; Lớp D "mở rộng diff".
- Hậu quả: client đang gửi `sort=` hoặc `search=` hợp lệ trước đây sẽ vỡ sau deploy.

### M4 — Trần dòng xuất tụt 20 lần, không nêu trong mô tả, không override được bằng env

`PoiXlsxRenderer.java:85,113-118` · `CsvRenderer.java:54,62-67`

| Kênh | Trước | Sau |
|---|---|---|
| xlsx | `ExportSupport.EXCEL_ROW_LIMIT` = 1.048.576 | **50.000** |
| csv | `ExportSupport.EXCEL_ROW_LIMIT` = 1.048.576 | **200.000** |

- Trigger: người dùng xuất báo cáo 60.000 dòng ra Excel.
- Actual: `RendererCapabilities.maxRows` = 50.000 nên `ReportRunService` trả **413**.
  Expected (hành vi cũ): file xuất bình thường.
- Hai key cấu hình mới `pmkt.reporting.xlsx.max-rows` và `pmkt.reporting.csv.max-rows` **không được
  khai trong `application.yml`**, trong khi key đồng cấp đã có thì khai kèm biến môi trường:
  `max-rows: ${PMKT_REPORTING_PDF_MAX_ROWS:5000}`. Ops **không nâng được trần bằng env var** trên
  container — chỉ sửa được bằng build lại image hoặc chèn SPRING_APPLICATION_JSON.
- Hậu quả: một regression hạ trần 20 lần được giấu trong một PR về gộp ô và viền, không có đường
  thoát vận hành. Lập luận OOM trong javadoc đáng tin, nhưng xứng đáng một ticket riêng.

### M5 — Mã message MSG_ là literal lặp, không thành hằng số, không có key i18n

- `"MSG_REPORT_SORT_INVALID"` xuất hiện **4 lần** dưới dạng chuỗi thô: `ReportRunService.java:160`,
  `:208`, `BangCanDoiTaiKhoanReportDefinition.java:238`, `BangKeChungTuReportDefinition.java:280`.
- `"MSG_REPORT_SEARCH_UNSUPPORTED"` — `ReportRunService.java:238` (PR mới thêm).
- `git grep` trong `src/main/resources/messages.properties`: **không có key nào** cho hai mã này,
  client nhận `messageId` không tra ngược được về thông báo tiếng Việt.
- Nguồn: bảng bảy lỗi #7 (Major).
- Đối chiếu: cùng PR làm ĐÚNG ở chỗ khác — `JasperPdfRenderer.PDF_TRUNCATED_CODE` /
  `PDF_TRUNCATED_MESSAGE_KEY` là hằng số có tên và key có thật trong `messages.properties`.

## Minor

### m1 — literalExpression không escape xuống dòng, PDF chết lúc compile design

`GenericPdfDesignBuilder.literalExpression` chỉ replace dấu backslash và dấu nháy kép, **không** xử
lý xuống dòng. Notice chứa ký tự xuống dòng sinh literal Java không đóng chuỗi, nên
`JasperCompileManager.compileReport` ném `JRException` — **500 cho mọi lần xuất PDF của báo cáo đó**,
chứ không phải mất một dòng cảnh báo. Hiện chưa notice nào chứa xuống dòng nên chưa nổ.

### m2 — CsvRenderer tự mâu thuẫn: javadoc nói CSV không có trần cấu trúc, code vẫn kẹp trần Excel

`CsvRenderer.java:42-54` viết "CSV không có giới hạn cấu trúc nào", nhưng `CsvRenderer.java:66`:
`this.maxRows = Math.min(maxRows, ExportSupport.EXCEL_ROW_LIMIT);`. Ops nâng
`pmkt.reporting.csv.max-rows` lên trên 1.048.576 sẽ bị kẹp âm thầm. Chưa gây hại (mặc định 200.000)
nhưng code và lý do đã ghi ngược nhau.

### m3 — Hai javadoc trong cùng file nói ngược nhau về precision mặc định của tiền VND

`ReportColumn.java`: `MONEY_VND_PRECISION` viết "đúng scale mà CSDL khai, KHÔNG phải giả định đồng là
đơn vị nhỏ nhất nên không có thập phân"; còn `withPrecision(int)` ngay dưới lại viết "Không khai thì
cột số hiện dạng số nguyên, đúng cho tiền VND (đồng là đơn vị nhỏ nhất đang lưu hành)". Javadoc thứ
hai là bản cũ chưa cập nhật; câu sai đó còn lặp lại ở `ReportSheetModel.SheetColumn.precision`.

### m4 — Javadoc blankCellsCoveredByBanner mô tả một nhánh không bao giờ chạy

`ReportSheetModel.java` — javadoc nói "Vòng lặp giữ lại để chuẩn hoá chuỗi rỗng / khoảng trắng về
null". Nhưng `spanUntilFirstFilledCell` kẹp dải theo `values.get(index) != null`, tức chuỗi rỗng được
coi là ô **đã có giá trị** và dải dừng **trước** nó. Ô rỗng không bao giờ lọt vào trong dải, nên
nhánh được mô tả là nhánh chết. Hoặc sửa javadoc, hoặc đổi điều kiện kẹp sang kiểm blank.

### m5 — Số tiền lẻ đổi hình trên mọi báo cáo hiện có

`ExportSupport.numberFormatPattern` dùng chữ số **tuỳ chọn** (mẫu `#,##0.##`). Giá trị 1500000.50 nay
in ra `1.500.000,5` (mất số 0 cuối). BR7 không quy định bắt buộc đệm 0 nên không phải vi phạm luật,
nhưng mô tả PR nói "Optional digits keep whole amounts looking exactly as before" — điều đó chỉ đúng
với số **chẵn**; số có phần lẻ đổi hình và lệch quy ước trình bày tiền 2 chữ số của chứng từ. Cân
nhắc mẫu `0.00` cho cột money, giữ chữ số tuỳ chọn cho tỷ giá / số lượng.

### m6 — Hai thay đổi ngoài phạm vi, không nêu trong mô tả PR

- `ExportSupport.REPORT_ZONE`: `resolveGeneratedDateText` chuyển từ `ZoneId.systemDefault()` sang
  `Asia/Ho_Chi_Minh` (sửa lỗi lùi một ngày trong container UTC).
- `build.gradle.kts`: `excludeTags("manual")` để `LocalEnvInitTool` thôi chạy trong `./gradlew build`.

Cả hai đều đúng và đáng làm, nhưng không liên quan gì tới "cell merging / page fitting / border
fixes" và mô tả PR không nhắc. Lớp D — mở rộng diff, khó review và khó revert độc lập.

## Nit

- **n1** — import `SearchMode` chèn **trước** `ReportResult`/`ReportRow`, phá thứ tự alphabet của
  khối import ở 3 file: `ReportRunService.java:25`, `SoCaiReportDefinition.java:22`,
  `SoNhatKyThuTienReportDefinition.java:20`.
- **n2** — còn **hai dòng trống liên tiếp** ở chỗ xoá `validateSortKey`: `SoCaiReportDefinition.java`
  (sau `build()`), `SoNhatKyThuTienReportDefinition.java` (sau `children()`).
- **n3** — `report-template.jrxml` bị **tái sinh toàn bộ UUID** (8/8 phần tử) kèm 2 thay đổi thật
  (`textAdjust="StretchHeight"`). Nhiễu diff, và chính là 1 trong 11 file xung đột ở B1. Ghi nhận PR
  đã gắn cổng `-DregenPdfTemplate=true` để lần sau không tái diễn.
- **n4** — dòng dài > 100 cột: `BangKeChungTuRepository.page` (chuỗi orderBy nối trên một dòng),
  `PoiXlsxRendererTest.java:61`, `JasperPdfRendererTest.java:597`. Checkstyle đang
  `isIgnoreFailures = true` nên không chặn.

## Điểm làm tốt (ghi nhận)

- **51 test mới**, phủ đúng các nhánh khó: dải nhãn bị kẹp khi ẩn cột, viền vệt gộp dọc trong xlsx,
  cờ applyBorder/applyFill của template, cảnh báo cắt chữ PDF, precision/nullDisplay/negativeStyle.
- **Xoá đường dẫn tuyệt đối của máy lập trình viên** khỏi file commit: `ManualVisualQaGeneratorTest`
  từng trỏ vào `C:/Users/sangnv/AppData/Local/Temp/claude/...`, nay là `build/qa-reports`.
- **Chặn SQL injection theo kiểu**: ORDER BY đổi từ `String` sang `enum SortColumn` ở cả hai
  repository, chuỗi thô của client không còn tới được chỗ nối SQL.
- **Sửa lỗi production thật**: thiếu `jasperreports-jdt` làm mọi `/run?format=pdf` chết trong fat jar.
- **Gắn cổng cho công cụ chạy tay**: `PdfTemplateScaffoldGeneratorTest` thôi ghi đè file nguồn mỗi
  lần build.

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục (BE) | OK — không thêm/di chuyển package, shape `api/` + `internal/` giữ nguyên, không tạo `api/` "cho chắc" |
| 2 | Không đánh lại version migration | N/A — PR không chạm file migration nào; repo chỉ có `src/main/resources/db/bieu_mau/V20260908210000__bm_bieu_mau.sql`, không nhánh remote nào giành số |
| 3 | Chưa test lại sau khi merge code | **B1** — tụt 20 commit, 11 file xung đột, toàn bộ file bị đổi package trên develop |
| 4 | N+1 / chưa tối ưu | OK — không thêm query trong vòng lặp; `MAX_DISPLAY_ITEMS` còn giảm số lần resolve ID qua `TaiKhoanRepository` (mặt nghiệp vụ xem M2) |
| 5 | Chưa tận dụng BaseController / BaseEntity | N/A — report-service là engine báo cáo chỉ-đọc, không có entity CRUD; repo này không có `BaseCrudController`/`ChungTuTemplate`/`GhiSoApi`. PR đi qua `ReportDefinition`/`ReportRenderer` đúng khung sẵn có |
| 6 | Chưa tận dụng base FE | N/A — không chạm `client/` |
| 7 | Constant / mã message đặt sai chỗ | **M5** (mã message literal lặp 4 chỗ, không có key i18n) và **M2** (text UI hardcode) |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | **M2** (hardcode text UI + cộng chuỗi, luật 2), **M3** (nghiệp vụ không có nguồn, luật 9). Không có secret trong diff. Không chạm vùng đóng băng. Phân tầng Controller/Service/Repository giữ đúng; response vẫn qua `ApiResponse<T>`; lỗi vẫn ném `ApiException` cho `@RestControllerAdvice`; không try/catch thủ công, không nuốt exception |
| B — Kiến trúc & 7 lỗi | xem bảng trên |
| C — Nghiệp vụ & truy vết | `trace.sh` / `msg.sh` **NOT-RUN** — report-service không có thư mục `docs/doing/*-spec`, PR không gắn PYC nào, và diff trải trên 5 báo cáo khác nhau nên không có một PYC đơn để truyền vào. Không đoán bừa một PYC |
| D — Vệ sinh diff & Git | **m6** (mở rộng diff), **n1–n4**. Nhánh `feat/gop-o-ngang-doc-cho-file-xuat` đúng chuẩn. Không commit thẳng develop. Không có `System.out` / `printStackTrace` / TODO không mã ticket trong diff. Working tree local sạch (`git status --porcelain` rỗng) |

## BR đã đối chiếu

- **BR7** (hiển thị & làm tròn số thập phân) — đọc đủ. `MONEY_VND_PRECISION=2`, `TY_GIA_PRECISION=6`,
  `NGOAI_TE_PRECISION=4` **khớp** bảng 7.1 (decimal 18,2 / 18,6 / 18,4). BR7.3 "chỉ làm tròn khi
  hiển thị" — PR đi đúng hướng (bỏ `doubleValue()`, format thẳng `BigDecimal`). Xem m5.
- **BR18** (chuyển đổi ngoại tệ) — đọc đủ. Lập luận "làm tròn tỷ giá thì ngoại tệ nhân tỷ giá lệch
  cột VND ngay trên cùng dòng" khớp công thức 18.2. Không vi phạm.

**BR chưa đọc:** phần còn lại của `business_rules.md`. Lý do: diff nằm trọn ở tầng kết xuất
(PDF/xlsx/CSV) và tầng validate tham số, không chạm màn hình / form / chứng từ / quyền.

## Lệnh thực sự đã chạy

    gh pr view 10 / gh pr view 11
    git merge-base origin/develop origin/pr/10
    git diff --stat / --name-status da5f557 origin/pr/10
    git diff --name-status -M da5f557 origin/develop
    git rev-list --count da5f557..origin/develop
    comm -12 (git diff --name-only ...) (git diff --name-only ...)
    git merge-tree --write-tree --name-only origin/develop origin/pr/10
    git diff da5f557 origin/pr/10 -- <từng file>
    git show origin/pr/10:<path>
    git grep -n MAX_ROWS / MSG_REPORT / pdfCatChu  (origin/pr/10 và origin/develop)
    git status --porcelain
    ./docs/rules/br.sh 7 18
    grep -n orientation/searchMode client/src/base/domainKit/report/reportModel.ts

## Phạm vi chưa đọc / chưa kiểm

- **Chưa chạy `./gradlew unitTest` / `./gradlew build`** — chế độ nhanh. Mọi kết luận về biên dịch là
  suy từ chữ ký hàm, không phải từ compiler.
- Chưa đọc chi tiết nội dung 51 test mới (chỉ đọc tên và đếm): `JasperPdfRendererTest` (+825 dòng),
  `PoiXlsxRendererTest` (+215), `ReportSheetModelTest` (+145), `ReportRowGroupingTest` (+104).
- Chưa đọc phần giữa của `GenericPdfDesignBuilder` (`computeUniformShrinkLayout`, `buildHeaderBand`,
  `spanWidth`, `cumulativeOffsets`) — đã đọc phần thay đổi nhiều nhất.
- `report-template.xlsx` là binary, không đọc được nội dung; chỉ đối chiếu qua javadoc và tên test
  `templateStylesCarryTheApplyFlagsThatPoiNeedsToSeeBordersAndFill`.
- **Đã kiểm và loại**: `ReportLayout.Orientation.AUTO` là giá trị mới trên wire, nhưng FE **đã** khai
  `z.enum(['portrait','landscape','auto'])` tại
  `client/src/base/domainKit/report/reportModel.ts:142` — không phải breaking change, không tính
  thành finding.
- **i18n**: `messages.properties` là bundle duy nhất của repo (không có `messages_en.properties`) —
  thiết kế sẵn có, không phải thiếu sót do PR này gây ra.

## Kết luận

**REJECT** — có Blocker B1.

- Blocker: **B1**
- Major: **M1, M2, M3, M4, M5**
- Minor: **m1, m2, m3, m4, m5, m6**
- Nit: **n1, n2, n3, n4**

Phần kỹ thuật kết xuất (gộp ô dọc/ngang, co giãn band theo khổ giấy, precision, fat-jar PDF) làm
chắc tay, có test, có lý do ghi lại rõ ràng. Thứ chặn merge không nằm ở đó mà ở **B1** (nhánh không
merge được với develop hiện tại, kể cả về mặt package) và ở **nhóm thay đổi ngoài phạm vi không khai
báo** (M2, M3, M4) — chúng đổi hành vi API và trần xuất file mà mô tả PR không hề nhắc tới.

**Cổng test/build CHƯA CHẠY** (chế độ nhanh). Kết luận REJECT dựa hoàn toàn trên kiểm tĩnh; trước khi
merge vẫn phải chạy `cd report-service && ./gradlew build` trên cây **đã merge develop**.

*Chưa đăng lên PR — user yêu cầu rõ không đăng comment (`gh pr comment` / `gh pr review`).*
