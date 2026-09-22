# Review — cell-app PR #179 · `feat: init bao cao ccdc`

- **Chế độ**: NHANH (chỉ đọc + kiểm tĩnh). KHÔNG chạy test/build/gradlew, KHÔNG worktree, KHÔNG sửa code, KHÔNG đăng comment lên PR (theo yêu cầu người gọi).
- **Repo**: `ospgroupvn-pmkt/cell-app` · base `develop` (`aab533e7`) · head `feat/bao-cao-ccdc` (`2d14cae5`) · merge-base = `aab533e7`
- **Quy mô**: 3 file, +56 / -0 (1 file `main`, 2 file `test`)
- **Tác giả**: tichvd-osp · PR body: rỗng
- **Phạm vi đã đọc**: 100% diff + `ReportProxyController`, `ReportProxyService`, seed `V2`/`V3`/`iam_quyen_full_639_ba.sql`, `client/src/app/pages/baoCao/reportCatalog.ts`, BA `PMKT-E-10810`, `PMKT-E-14616`.

## Nội dung thay đổi

Đăng ký 2 báo cáo CCDC vào `ReportPermissionRegistry` (façade proxy sang `report-service`):

| reportId | mã quyền | epic |
|---|---|---|
| `bao-cao-chi-tiet-ccdc` | `BCChiTietCCDC.View` | PMKT-E-10810 |
| `bang-tinh-phan-bo-ccdc` | `BCPhanBoCCDC.View` | PMKT-E-14616 |

Cộng 3 test ở `ReportProxyServiceTest` + 1 test ở `ReportPermissionRegistryTest`, và cập nhật javadoc lỗi thời của registry (ghi chú "[2026-08-05] bean KHÔNG được gọi" → "[2026-09-10] ĐANG được gọi").

## Bảng đếm finding

| Mức | Số lượng |
|---|---|
| Blocker | 0 |
| Major | 1 |
| Minor | 4 |
| Nit | 4 |

## Major

### M1 — `reportId` mới KHÔNG có trong FE `reportCatalog.ts`, và javadoc khẳng định ngược lại

- **File**: `src/test/java/vn/vtt/pmkt/cell/reporting/internal/service/ReportPermissionRegistryTest.java:110-111`
- **Nguồn/hợp đồng**: chính javadoc của test — "Mã quyền phải khớp CHÍNH XÁC … và chuỗi trong `client/src/app/pages/baoCao/reportCatalog.ts`".
- **Trigger**: `grep -rn "bang-tinh-phan-bo-ccdc\|bao-cao-chi-tiet-ccdc" client/src` → **0 kết quả**; `reportCatalog.ts` (90 dòng) không có nhóm/mục CCDC nào.
- **Expected**: reportId có mặt ở cả hai phía để người dùng vào được báo cáo từ hub `BaoCaoHubPage`.
- **Actual**: chỉ có ở BE. Javadoc viện dẫn một chuỗi không tồn tại → người đọc sau tin là đã khớp mà không kiểm.
- **Hậu quả**: hai báo cáo CCDC không truy cập được từ UI sau khi merge PR này; test "chứng minh" một hợp đồng chéo repo mà nó không hề assert. Nếu FE được giao ở PR `client` đi kèm thì cần ghi rõ trong PR body (đang rỗng) và sửa javadoc cho khớp thực tế.
- Ghi chú: `bang-ke-phieu-nhap`, `so-chi-tiet-tai-khoan` trong registry cũng vắng ở `reportCatalog.ts` — vấn đề có tiền lệ, nhưng không làm PR này hết thiếu.

## Minor

### m1 — Javadoc lớp test vẫn nói cổng quyền đang TẮT

- **File**: `src/test/java/vn/vtt/pmkt/cell/reporting/ReportProxyServiceTest.java:42-44`
- Nội dung: "[2026-08-05] Kiểm quyền theo từng báo cáo đang TẮT ở `ReportProxyService` (comment lời gọi, không xoá)".
- Thực tế đã xác minh: `ReportProxyController:33,41` gác cả hai endpoint bằng `@PreAuthorize("@reportProxyService.duocPhepXemBaoCao(#reportId, authentication)")`, và `ReportProxyService:78` gọi `permissions.requirePermission(reportId)`.
- PR đã sửa đúng ghi chú lỗi thời này ở class chính (`ReportPermissionRegistry`) nhưng bỏ sót bản sao ở file test — chính file mà PR đang sửa. Ghi chú sai ở file test là mồi cho lần "dọn test chết" sau.

### m2 — Test mới trùng lặp test đã có

- **File**: `ReportProxyServiceTest.java:202-213` (`duocPhepXemBaoCao_unregisteredReportId_throwsNotFound`) so với `:170-181` (`unregisteredReportId_isNotFoundRatherThanForbidden`).
- Hai test giống hệt nhau về assert (404 + `REPORT_UNKNOWN`), chỉ khác chuỗi reportId lạ (`bao-cao-chua-dang-ky` vs `so-nhat-ky-chung-chua-dang-ky`) và quyền trong token (không ảnh hưởng nhánh chạy — registry ném trước khi so quyền).
- Không phủ thêm gì cho CCDC; tăng chi phí bảo trì của file test.

### m3 — Toàn bộ mã message của hai epic chưa xuất hiện trong code

```
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-14616_BangTinhPhanBoCCDC be  → THIEU 6/6
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10810_BCChiTietCCDC     be  → THIEU 2/2
```

Đáng chú ý `MSG_PMKT-E-14616_301` / `MSG_PMKT-E-10810_301` "Không có quyền xem báo cáo": cổng `@PreAuthorize` trả `false` ⇒ Spring Security dựng 403 chung, **không** mang mã message của BA. PR "init" nên thiếu là dự kiến được, nhưng phải ghi rõ đây là phần còn nợ, không phải đã xong.

### m4 — Hai test `@Disabled` mâu thuẫn với chính comment PR vừa thêm

- **File**: `ReportProxyServiceTest.java` — comment mới ở `:183-184` xác nhận "Hai test `@Disabled` ở trên nhắm lời gọi CŨ trong thân service".
- Lời gọi cũ đó không còn tồn tại (đã chuyển lên `@PreAuthorize`), nên hai test đó vĩnh viễn không bao giờ bật lại được ở dạng hiện tại. PR chọn mô tả thay vì dọn — để lại test chết kèm javadoc lớp sai (m1).

## Nit

- **n1** — Commit message `feat: init bao cao ccdc` thiếu `(<scope>)`; chuẩn là `<type>(<scope>): <mô tả>` (`docs/rules/conventions-chung.md:68`). Ví dụ: `feat(reporting): dang ky bao cao CCDC vao registry`.
- **n2** — PR body rỗng; không nêu PR `client`/`report-service` đi kèm (liên quan trực tiếp M1).
- **n3** — Phủ test không đối xứng: `bao-cao-chi-tiet-ccdc` chỉ có test ở tầng service, `bang-tinh-phan-bo-ccdc` chỉ có test ở `ReportPermissionRegistryTest`. Nên đối xứng hoặc gộp thành `@ParameterizedTest`.
- **n4** — Khối comment `:183` gắn nhãn `PMKT-E-10810` cho cả 3 test, nhưng test thứ ba (`unregisteredReportId`) là hành vi chung của registry, không thuộc epic đó.

## Bảy lỗi hay gặp

| # | Mục | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục (Modulith `api/`–`internal/`) | ✅ File nằm đúng `reporting/internal/service/`; không tạo `api/` thừa; `package-info.java` của module đã có sẵn, không đụng. |
| 2 | Không đánh lại version migration | ✅ N/A — diff không có file migration nào (`git diff --name-status` chỉ 3 file .java). Đã kiểm chéo: mã quyền đã tồn tại trong `V2__seed_data.sql:830,909` và `V3__gop_thay_doi_sau_baseline.sql:1312-1318` từ trước, PR không cần migration mới. |
| 3 | Chưa test lại sau merge | ✅ N/A — `git rev-list --count <merge-base>..origin/develop` = **0** (merge-base đúng bằng `origin/develop`), không có file giao nhau. |
| 4 | N+1 / chưa tối ưu | ✅ N/A — thay đổi chỉ là 2 entry trong `Map.ofEntries` tĩnh, không có query. |
| 5 | Chưa tận dụng BaseController / BaseEntity | ✅ N/A — đây là façade proxy stream, không phải CRUD; `ChungTuTemplate`/`GhiSoApi` không liên quan. |
| 6 | Chưa tận dụng base FE | ✅ N/A — không chạm `client/`. |
| 7 | Constant đặt sai chỗ | ✅ Cặp `reportId → mã quyền` nằm trong hằng `PERMISSION_BY_REPORT_ID` của chính registry — đúng nơi duy nhất của repo này giữ ánh xạ đó. |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ✅ Không secret; không hardcode magic value ngoài hằng có tên; không `@RestControllerAdvice` bị vòng qua; Controller không chứa business logic, không gọi Repository, không trả Entity; không chạm vùng đóng băng (`master_data`, `legacy`, `Phase_2`). Không có "nghiệp vụ tự bịa": `BCChiTietCCDC.View` được BA quy định trực tiếp (`PMKT-E-10810/4.usecases/PMKT-U-10810_ChonThamSo/UC_ChonThamSo_BCChiTietCCDC.md:22`); `BCPhanBoCCDC.View` không có dòng `Permission:` trong BA 14616 nhưng đã tồn tại trong catalog `iam_quyen` với mô tả "Xem bảng tính PB CCDC" — nguồn chấp nhận được, không phải mã bịa. |
| B — Kiến trúc & 7 lỗi | ⚠ Xem bảng trên — không lỗi kiến trúc. |
| C — Nghiệp vụ & truy vết | ⚠ `trace.sh`: **NOT-RUN** — không tồn tại thư mục `docs/doing/*-spec` cho hai epic này (`ls docs/doing` không có mục CCDC/14616/10810), chưa chạy `/audit-spec`. `msg.sh`: đã chạy, THIEU 8/8 → m3. |
| D — Vệ sinh diff & Git | ⚠ n1, n2. Cổng cây commit: `git status --porcelain` sạch; không có file mới (3 file đều `M`), không đụng barrel/`index.ts` ⇒ không có rủi ro "xanh local đỏ deploy". |

## Kiểm tĩnh đã chạy

```bash
gh pr view 179 --json ...
git merge-base origin/develop 2d14cae5           # = aab533e7 (không tụt so với develop)
git diff --stat / --name-status aab533e7 2d14cae5
git rev-list --count aab533e7..origin/develop    # 0
git status --porcelain                            # sạch
git show 2d14cae5:<ReportPermissionRegistry|ReportProxyController|ReportProxyService|2 test>
grep -rn "BCPhanBoCCDC\|BCChiTietCCDC" cell-app/src/main/resources/
grep -rn "bang-tinh-phan-bo-ccdc\|bao-cao-chi-tiet-ccdc" client/src   # 0 kết quả → M1
for b in $(git branch -r); do ... grep bang-tinh-phan-bo-ccdc ...      # chỉ origin/feat/bao-cao-ccdc
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-14616_BangTinhPhanBoCCDC be
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10810_BCChiTietCCDC     be
```

## Chưa kiểm chứng

- `./gradlew unitTest` — **NOT-RUN, chế độ nhanh**. Suy luận tĩnh: 4 test mới chỉ dùng API sẵn có (`assertThatThrownBy`, `ApiException` đã import; `requirePermission` package-private, test cùng package `…internal.service`; `quyenTheoBaoCao()` đọc field qua reflection nên 2 entry mới tự động vào `moiMaQuyenTrongRegistryDeuCoTrongCatalogIamQuyen`, và cả hai mã đều có trong seed ⇒ test đó vẫn xanh).
- `report-service` là repo khác, không có trong workspace ⇒ **không xác minh được** hai chuỗi `reportId` khớp `ReportDefinition.id()` bên đó. Đây chính là rủi ro mà javadoc của registry cảnh báo; PR không bổ sung cơ chế chống lệch nào.
- Không chạy `trace.sh` (không có spec), không đo baseline, không merge thử, không chạy màn thật.

## Kết luận

**REQUEST CHANGES** — 1 Major (M1). Các Minor m1/m2/m4 nên xử lý trong cùng lượt vì đều nằm ở đúng file PR đang sửa.

Không có Blocker; kiến trúc, phân tầng, migration, N+1 và cổng cây commit đều sạch. ⚠ Cổng test/build (`./gradlew unitTest`) **chưa chạy** — kết luận này chỉ ở phạm vi đã đọc tĩnh, không phải APPROVE.
