# Review PR #20 — report-service

`[Bugfix] Core báo cáo: mã quyền, xuất file BR39, E2E, SPI`
https://github.com/ospgroupvn-pmkt/report-service/pull/20

| | |
|---|---|
| Chế độ | **NHANH** (chỉ đọc + kiểm tĩnh bằng git/grep — KHÔNG chạy test/build, KHÔNG worktree) |
| Head | `f49c391` (`bugfix/core-bao-cao`) |
| Base | `origin/develop` = `caec7c3` (merge-base trùng đúng đỉnh develop) |
| Diff | 32 file · +347 / −109 · 0 file mới · 0 migration |
| Working tree | sạch (`git status --porcelain` rỗng) |
| Đã đọc | toàn bộ 20 file `src/main` + `build.gradle.kts` + `application.yml` + `jrxml`; 12 file test đọc phần diff |
| Chưa đăng lên PR | user yêu cầu rõ KHÔNG comment lên PR |

## Tổng kết findings

| Mức | Số lượng | Mã |
|---|---|---|
| Blocker | 0 | — |
| Major | 4 | M1 M2 M3 M4 |
| Minor | 8 | m1…m8 |
| Nit | 3 | n1 n2 n3 |

**Kết luận: REQUEST CHANGES** (có Major). Lưu ý: cổng `./gradlew :report-service:build` / `unitTest`
**chưa chạy** trong lượt này (chế độ nhanh) — kết luận chỉ nói về phạm vi đã đọc.

---

## Major

### M1 — Mượn mã quyền của epic khác cho báo cáo Phân bổ CPTT theo năm
`src/main/java/vn/vtt/pmkt/cell/reporting/internal/service/definitions/PhanBoTheoThangReportDefinition.java:43-46`

- **Nguồn**: CLAUDE.md gốc luật 9 "Không tự quyết nghiệp vụ" + §Cổng đặc tả luật 2.
- **Actual**: `PERMISSION = "BCPhanBoCPTT.View"`, kèm comment tự khai *"Mã MƯỢN của C7.3 (PMKT-E-10603).
  Báo cáo này là PMKT-E-10601 … DanhSachQuyen.md §C7 không cấp mã riêng"*.
- **Expected**: tài liệu im lặng ⇒ mở mục `OPEN` trong sổ mâu thuẫn và hỏi BA, không tự gán.
- **Hậu quả**: hai báo cáo thuộc hai epic dùng chung một mã quyền ⇒ cấp quyền C7.3 là mở luôn C7.1;
  không thể thu hồi riêng. Đây là quyết định phân quyền, không phải quyết định kỹ thuật.
- **Đã xác minh**: `BCPhanBoCPTT.View` có thật trong `cell-app/.../V2__seed_data.sql:839`
  (mô tả "Xem bảng PB CPTT"), `BCPhanBoTheoThang.View` không tồn tại ⇒ 403 là đúng. Vấn đề nằm ở
  cách *chọn* mã thay thế, không ở việc phát hiện lỗi.
- 3 mã còn lại (`BCKeChungTu` · `BCChiPhiBoPhan` · `BCNhatKyThuTien`) đã đối chiếu catalog: **đúng**,
  đây là đổi tên thật sau baseline. Toàn bộ 9 mã `BC*.View` ở head đều tồn tại trong `iam_quyen`.

### M2 — Đổi mặc định `kyBaoCao` = "ThangNay", trích sai nguồn BR1
`src/main/java/vn/vtt/pmkt/cell/reporting/internal/service/definitions/ReportDefinitionSupport.java:79-80`

- **Actual**: `defaultValue` từ `null` → `"ThangNay"`, comment `// BR1 mọi báo cáo: kỳ mặc định "Tháng này"`;
  commit `aa085e6 fix(reporting): kỳ báo cáo mặc định "Tháng này" (BR1)`.
- **Expected**: BR1 trong `pmkt-docs/ba/Common/business_rules.md` là **"Phân trang dữ liệu"**
  (20 bản ghi/trang, ô "Tới … Trang") — không có một chữ nào về kỳ báo cáo mặc định. Đã đọc trực tiếp
  bằng `./docs/rules/br.sh 1`.
- **Hậu quả**: thay đổi hành vi mặc định của **mọi** báo cáo dùng `periodParams` với nguồn không kiểm
  chứng được. Nếu "BR1" ở đây là BR nội bộ của một file `SCR_*` thì phải ghi rõ file nào (CLAUDE.md gốc
  cảnh báo đúng cái bẫy `BRnn` nội bộ màn ≠ BR chung); nếu không có thì là luật tự đặt.
- Test mới `BangKeChungTuReportDefinitionTest:80` khoá cứng hành vi này và cũng chú thích "BR1".

### M3 — SPI `grandTotalTop` hiện thực một luật tự nhận là đang xung đột với BR31/BR39.5
`src/main/java/vn/vtt/pmkt/cell/reporting/api/dto/ReportGrouping.java:16-22, 45-49`

- **Actual**: thêm field `grandTotalTop` + factory `serverGrandTotalTop()`; javadoc do chính tác giả viết:
  *"XUNG ĐỘT CHƯA GIẢI QUYẾT với BR31 … nguồn duy nhất cho `true` là quan sát trên Figma"*.
- **Nguồn**: BR31 "dòng tổng (Footer Row) **tại cuối danh sách**" và BR39.5 "dòng Tổng cộng **ở cuối
  báo cáo**" — đã đọc nguyên văn. Cổng đặc tả luật 2: không tự đặt luật, mở `OPEN` rồi hỏi.
- **Hậu quả kép**:
  1. API công khai chở sẵn một hành vi trái BR, không definition nào dùng (dead SPI) — người sau sẽ
     gọi `serverGrandTotalTop()` mà không đọc javadoc.
  2. Nếu ai bật cờ, **BR39.5 vỡ im lặng**: `PoiXlsxRenderer.writeBody` nhận diện dòng tổng bằng
     `i == lastIndex && kind == TOTAL` (`PoiXlsxRenderer.java:388-392`) ⇒ dòng tổng ghim ĐẦU sẽ không
     được tô nền `#F2F2F2`, chỉ còn in đậm.
- Đề nghị: tách khỏi PR bugfix, chờ BA chốt (xem thêm m8).

### M4 — Hai hành vi BR39 chính không có test tự động nào
`PoiXlsxRenderer.java:316-320` (AutoFilter, BR39.3) · `PoiXlsxRenderer.java:572-576` (nền `#F2F2F2`, BR39.5)

- **Bằng chứng**: `git grep -l "AutoFilter|F2F2F2|FillForegroundColor" -- src/test` chỉ trả về
  `bieu_mau/NhapExcelTest.java` — không file test nào của `reporting` chạm hai hành vi này.
  `PoiXlsxRendererTest` chỉ được sửa để chạy tiếp (thêm tham số `false`) + đổi 2 assert tên file / IN HOA.
- **Nguồn**: `review-hanh-vi.md` §Test — assert expected state, không chỉ "chạy được".
- **Hậu quả**: bằng chứng duy nhất cho BR39.3/39.5 là `ManualVisualQaGeneratorTest`, mà chính PR này
  thêm `useJUnitPlatform { excludeTags("manual") }` (`build.gradle.kts:129-134`) ⇒ nó **không bao giờ**
  chạy trong `test`. Hai luật này sẽ không đỏ khi bị phá.
- POI đọc lại được cả hai (`sheet.getCTWorksheet().getAutoFilter()`, `XSSFCellStyle.getFillForegroundColorColor()`),
  nên viết test là rẻ.

---

## Minor

- **m1** `ReportRunService.java:388-392` — chuỗi `"Tất cả"` hardcode trong `switch`, không phải hằng số
  có tên, không đi qua `textResolver`. Nhãn cạnh nó (`labelKey`) **có** i18n ⇒ file xuất locale `en` sẽ
  ra `"Account: Tất cả"`. (Có tiền lệ `"Có"/"Không"` ở `formatParamValue` nên chỉ Minor, nhưng tiền lệ
  sai không phải lý do nhân bản — luật 1 / 7 lỗi #7.)
- **m2** `PoiXlsxRenderer.java:316-320` — range AutoFilter là `[firstBodyRow-1 … lastBodyRow]`, tức
  **bao cả dòng Tổng cộng**. Excel coi dòng cuối range là dữ liệu ⇒ người dùng lọc bất kỳ là dòng Tổng
  bị ẩn/lọc theo, ngược BR39.5 ("làm nổi bật", luôn thấy). Range nên dừng ở `lastBodyRow - 1` khi dòng
  cuối là `TOTAL`.
- **m3** `ReportRunService.java:368-376` — `emptyFilterDisplay` in `"Tất cả"` cho **mọi** field
  `SELECT/MULTI_SELECT/LOOKUP`, không xét `visibleWhen`/`enabledWhen`. Field bị ẩn theo điều kiện vẫn
  hiện một dòng "điều kiện lọc" mà người dùng chưa từng thấy. Hiện latent (chưa definition nào set
  `visibleWhen` khác `null` — đã grep), nhưng `SoNhatKyChungReportDefinition:185-186` đã truyền tiếp hai
  trường này nên chỉ là chuyện thời gian.
- **m4** `AbstractReportE2eTest.java:75` — `LATEST_MIGRATION_MARKER = "V1110__fa_chi_tiet_bo_sung_chi_nhanh_id.sql"`
  ghim cứng tên file migration của **repo khác** (`cell-app`), phải sửa tay mỗi đợt. `cell-app` hiện đã
  có `V1111__iam_quyen_bieu_mau.sql` ⇒ marker lạc hậu ngay lúc merge; và bất kỳ checkout `cell-app`
  đứng trước V1110 sẽ làm toàn bộ E2E ném ở static initializer. Ý tưởng "thà ném lỗi còn hơn migrate
  schema cũ" là đúng; cách đo nên là "có ít nhất N migration / có bảng X", không phải một tên file.
- **m5** `ExportSupport.java:120-128` — nhánh fallback `DEFAULT_FILE_NAME` thực tế **chết**: khi i18n
  miss, `textResolver.resolve` trả về chính khoá, nên `title` không bao giờ `null/blank`. Chính test của
  PR khẳng định điều đó: `assertThat(artifact.fileName()).matches("test\.title_\d{8}_\d{6}\.xlsx")`
  (`PoiXlsxRendererTest:139`). Hậu quả thật: thiếu key i18n ⇒ người dùng tải về file tên `bangKe.title_….xlsx`.
- **m6** `ExportSupport.java:126-127` — dấu thời gian tên file lấy `ZoneId.systemDefault()` của server.
  BR39.4 nói "Ngày xuất / Giờ xuất" (của người dùng). Nhất quán với `resolveGeneratedDateText` sẵn có nên
  chỉ Minor, nhưng cả hai chỗ đều nên đi qua timezone của tenant/người dùng.
- **m7** `ExportSupport.java:115-118` — `request.suggestedFileName()` vẫn thắng tuyệt đối và không được
  sanitize (chỉ nhánh BE tự dựng mới qua `sanitizeFileName`). FE truyền tên tuỳ ý là BR39.4 bị vượt mặt.
  (Đã kiểm: `ReportController.java:66` dùng `.filename(name, UTF_8)` ⇒ không vỡ header với dấu tiếng Việt.)
- **m8** PR gắn nhãn `[Bugfix]` nhưng chứa `541bc48 feat(bao-cao): SPI control combogrid + ghim dòng Tổng`
  — tính năng mới (M3) trộn vào PR sửa lỗi. Tách ra thì phần bugfix merge được ngay, phần SPI chờ BA.

## Nit

- **n1** `src/main/resources/templates/report-template.jrxml` — sinh lại **toàn bộ** `uuid` (1 report + 8
  element) trong khi thay đổi thật chỉ là `hTextAlign=Left` + `textAdjust="StretchHeight"` ở một element.
  Diff 20 dòng nhiễu che mất 2 dòng có nghĩa.
- **n2** `gradlew` đổi mode `100644 → 100755` (commit riêng `77e869b`) — đúng nhưng ngoài phạm vi PR bugfix.
- **n3** `CLAUDE.md` thêm mục "Báo cáo cha-con — phân trang theo dòng CHA". Nội dung **đúng nguồn**
  (đã đối chiếu BR40.1 và BR38.5 nguyên văn), nhưng là tài liệu cho việc chưa làm trong PR này.

---

## Bảng 7 lỗi hay gặp (Lớp B)

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ không vi phạm — mọi file sửa nằm đúng `api/` (DTO hợp đồng) và `internal/{repository,service,service/renders}`; không có file phẳng ra gốc module, không thêm `api/` mới. |
| 2 | Không đánh lại version migration | ✅ N/A — diff **không có** file nào dưới `db/migration` (`git diff --name-status` xác nhận 0/32). Liên quan gián tiếp: m4. |
| 3 | Chưa test lại sau khi merge | ✅ N/A — `git rev-list --count caec7c30..origin/develop` = **0**, merge-base trùng đỉnh `develop` (PR đã merge develop ở `051a76c`). Không có file giao nhau vì không tụt commit nào. |
| 4 | N+1 / chưa tối ưu | ✅ không vi phạm — `PhanBoTheoThangRepository` chỉ đổi **tên bảng** trong 2 native query, vẫn `sum()+GROUP BY` một lượt. `resolveLookupDisplay` nhánh mới khớp `field.options()` **trong bộ nhớ**, không thêm truy vấn; nhánh `tai-khoan` giữ nguyên. |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ N/A — PR không thêm CRUD/entity/chứng từ; toàn bộ đi qua khung `ReportDefinition`/`ReportRenderer` sẵn có, đúng hướng tái sử dụng. |
| 6 | Chưa tận dụng base FE | ✅ N/A — 0 file FE. |
| 7 | Constant đặt sai chỗ | ⚠ **m1** (`"Tất cả"` hardcode trong `switch`). Phần còn lại đạt: `GRAND_TOTAL_RGB`, `FILE_NAME_TIMESTAMP`, `VIETNAMESE_LOCALE`, `LATEST_MIGRATION_MARKER` đều là `private static final` có tên. |

## Lớp A — cổng cứng

| Mục | Kết quả |
|---|---|
| Secret trong diff | ✅ không có. `application.yml` chỉ thêm `timeout: ${REDIS_TIMEOUT:500ms}`. |
| Hardcode magic value | ⚠ m1 (`"Tất cả"`), M2 (`"ThangNay"` — trị số đã có sẵn trong `KY_BAO_CAO_OPTIONS`, nên là literal lặp). |
| Phân tầng BE (Controller→Service→Repository) | ✅ không vi phạm — không đụng Controller ngoài test; `ReportRunService` không gọi thẳng `EntityManager`. |
| `ApiResponse<T>` / `@RestControllerAdvice` / nuốt exception | ✅ không vi phạm — `requireRenderer` vẫn ném `ApiException.notFound`; không thêm try/catch trả lỗi thủ công. `resolveTaiKhoanLabel` bắt `IllegalArgumentException` để hạ cấp nhãn — có chủ đích, ghi rõ AD-4, không phải nuốt lỗi nghiệp vụ. |
| Vùng đóng băng | ✅ không chạm `master_data/**`, `client/legacy/**`, `pmkt-docs/ba/Phase_2/**`. Lượt review này cũng không đọc Phase 2. |
| Commit thẳng master/develop · PR trộn loại | ⚠ m8 — nhánh `bugfix/core-bao-cao` đúng chuẩn, 12 commit đều đúng `<type>(<scope>): <mô tả>`, nhưng trộn 1 commit `feat`. |
| **Nghiệp vụ không có nguồn** | ⚠ **M1 · M2 · M3** — xem ba mục Major. |

## Lớp C — nghiệp vụ & truy vết

- `trace.sh` · `msg.sh`: **NOT-RUN** — không tồn tại thư mục spec nào cho report-service trong
  `docs/doing/` (đã liệt kê: toàn bộ là `PMKT-E-0xxxx-*` của cell-app/client), và diff trải trên
  nhiều báo cáo thuộc nhiều epic (PMKT-E-10601, C7.x…) nên **không có một thư mục PYC đơn** để truyền vào.
  Không đoán bừa PYC.
- **BR đã đọc** (bằng `./docs/rules/br.sh`): **BR1** (bác nguồn của M2) · **BR31** (căn cứ M3) ·
  **BR38** (kiểm mục 38.5 mà CLAUDE.md trích) · **BR39** (toàn bộ 39.1–39.5, trục chính của PR) ·
  **BR40** (kiểm mục 40.1 mà CLAUDE.md trích).
- **BR chưa đọc**: BR2 (dateOrder — chỉ chạm gián tiếp qua `validateRules` không đổi); không cần cho
  finding nào ở trên.
- **Đối chiếu BR39 từng mục**:

| BR39 | Hiện thực | Đánh giá |
|---|---|---|
| 39.3 Tên báo cáo IN HOA | `ExportSupport.resolveTitle` + `toUpperCase(Locale "vi")` | ✅ đạt (locale tường minh là đúng, tránh bẫy Turkish) |
| 39.3 Mỗi tham số một dòng | `resolveConditionsText` join `"\n"` + `applyConditionsWrap` (xlsx) + `textAdjust=StretchHeight` (pdf) | ✅ đạt; CSV **không** xuất khối tiêu đề (tồn tại từ trước, ngoài phạm vi) |
| 39.3 Freeze header | `createFreezePane(0, firstBodyRow)` — đã có, PR không đổi | ✅ đạt |
| 39.3 Filter trên dòng header | `setAutoFilter` mới | ⚠ m2 (range trùm dòng Tổng) · M4 (không test) |
| 39.4 Tên file `[Tên]_[Ngày]_[Giờ]` | `resolveFileName` + `yyyyMMdd_HHmmss` | ⚠ m5 m6 m7 |
| 39.5 Dòng Tổng nổi bật | in đậm (có sẵn) + nền `#F2F2F2` mới | ⚠ M3 (vỡ nếu ghim đầu) · M4 (không test) |

## Kiểm tĩnh đã chạy (§3a)

```
git merge-base origin/develop origin/pr/20           -> caec7c30 (= đỉnh develop)
git rev-list --count caec7c30..origin/develop        -> 0          (lỗi #3: N/A)
git diff --name-status                               -> 32 M, 0 A  (không file mới => cổng cây commit N/A)
git status --porcelain                               -> rỗng
git grep "new ReportGrouping(" @head                 -> 12 call site, TẤT CẢ đã cập nhật 6 tham số
git grep "BC<Ten>.<HanhDong>" @head                  -> 9 mã, đối chiếu iam_quyen: 9/9 tồn tại
git grep "AutoFilter|F2F2F2|FillForeground" src/test -> 0 kết quả trong module reporting (M4)
```

- **Compile-break do đổi chữ ký**: `ReportGrouping` từ 5 → 6 component — đã soát **toàn bộ** call site
  (12 chỗ, gồm 8 trong test) đều đã sửa ⇒ không gãy. `ReportParamField` từ 14 → 15 component có
  constructor tương thích ngược 14 tham số ⇒ call site cũ không gãy. **Không kiểm được** caller ngoài
  repo (FE / cell-app) — hai record này nằm trong `api/`, JSON thêm field là non-breaking, nhưng
  `paramsDisplay` **thêm dòng mới** ("Tất cả") là thay đổi dữ liệu FE đang render (liên quan m3).
- **Migration**: không có file migration trong diff ⇒ bỏ qua bước quét remote branch giành số.

## Chưa chạy / giới hạn lượt này

- `./gradlew unitTest` · `./gradlew :report-service:build`: **NOT-RUN — chế độ nhanh**.
- E2E Testcontainers: **NOT-RUN** (cần Docker, CLAUDE.md gốc cấm) — khẳng định "E2E 6 báo cáo xanh"
  trong mô tả PR **chưa được kiểm chứng độc lập** ở lượt này.
- `ManualVisualQaGeneratorTest` (`@Tag("manual")`): **NOT-RUN**, và xem M4 — nó cũng không chạy trong CI.
- Phần đọc lướt: `ReportE2eFixtures.java` và các file `*E2eTest` chỉ đọc phần diff, không đọc toàn file.

## Đề nghị xử lý trước khi merge

1. M1 · M2 · M3 → cần câu trả lời của BA, không phải sửa code (mở mục `OPEN`).
2. M4 · m2 → sửa được ngay trong PR, chi phí thấp (một test POI + một phép trừ trong range AutoFilter).
3. m8 → cân nhắc tách commit `541bc48` sang PR riêng để phần bugfix đi trước.

> Không đăng comment lên PR theo yêu cầu của user. Không sửa code, không commit, không approve.
