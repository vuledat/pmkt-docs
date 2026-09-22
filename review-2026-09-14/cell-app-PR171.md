# Review PR #171 — cell-app — `Feat: Báo cáo sổ nhật ký thu/chi tiền`

| Mục | Giá trị |
|---|---|
| Repo | `ospgroupvn-pmkt/cell-app` |
| PR | [#171](https://github.com/ospgroupvn-pmkt/cell-app/pull/171) — tác giả `datnt5920`, state OPEN |
| Head | `cdd900ade7d8cf229891af2bde2b6322a3d651a5` (`feature/sonhatkythutien`) |
| Base | `origin/develop` = `aab533e76732342535e01fae0613067f3c745377` |
| Merge-base | `8b7fe3a9292b1aba2bff6739d8f2c6587a390d79` |
| Quy mô | 2 file · +17 / −5 · 2 commit |
| Working tree | sạch (`git status --porcelain` rỗng) |
| **Chế độ** | **NHANH** — chỉ đọc + kiểm tĩnh bằng git/grep. KHÔNG chạy test/build/gradlew, KHÔNG tạo worktree, KHÔNG merge thật, KHÔNG sửa code, KHÔNG đăng comment lên PR (theo yêu cầu người gọi). |

## Nội dung thay đổi

1. `ReportPermissionRegistry`: `so-nhat-ky-thu-tien` đổi mã quyền `BCSoNhatKyThuTien.View` → `BCNhatKyThuTien.View`; thêm dòng mới `so-nhat-ky-chi-tien` → `BCNhatKyChiTien.View`.
2. `ReportPermissionRegistryTest`: rút `NO_CHUA_SEED` từ 3 → 2 mục, sửa `hasSize(3)` → `hasSize(2)`, thêm 2 test khẳng định mã quyền của thu tiền / chi tiền.

Phần **nội dung nghiệp vụ của bản vá là ĐÚNG** khi xét riêng nhánh: cả `BCNhatKyThuTien.View` (V2 dòng 800) và `BCNhatKyChiTien.View` (V2 dòng 803) đều có thật trong catalog `iam_quyen` của `V2__seed_data.sql`, kèm hàng `iam_pham_vi_hieu_luc` (dòng 11250–11255). Mã cũ `BCSoNhatKyThuTien.View` không tồn tại trong seed ⇒ đúng là façade 403 mọi người. Hai mục còn lại trong `NO_CHUA_SEED` (`BCChiPhiTheoBoPhan.View`, `BCPhanBoTheoThang.View`) vẫn 0 lần xuất hiện trong seed ⇒ test `khongCoMucLoiThoiTrongDanhSachNo` tự nhất quán trên nhánh này.

**Nhưng** toàn bộ việc này đã được làm — và làm rộng hơn — trên `develop` rồi (xem B1).

## Bảng finding

| Mức | Số lượng |
|---|---|
| Blocker | 1 |
| Major | 1 |
| Minor | 2 |
| Nit | 2 |
| **Tổng** | **6** |

---

## Blocker

### B1 — Nhánh tụt hậu, xung đột cứng ở CẢ HAI file, và merge ẩu sẽ **lùi 3 mã quyền đã sửa trên develop** (lỗi #3)

- **File**: `src/main/java/vn/vtt/pmkt/cell/reporting/internal/service/ReportPermissionRegistry.java:26-33` · `src/test/java/vn/vtt/pmkt/cell/reporting/internal/service/ReportPermissionRegistryTest.java:32-36,81-84`
- **Nguồn**: `bon-lop.md` §Lớp B lỗi #3 (Major, **Blocker khi giao nhau ở file cấu hình / cổng dùng chung**) · CLAUDE.md §Cổng cây commit.
- **Đo được**:

```
merge-base            = 8b7fe3a9
develop đi trước      = 4 commit
file giao nhau        = 2/2 (đúng cả hai file của PR)
git merge-tree develop pr/171 → CONFLICT (content) ở CẢ HAI file
```

- **Trigger**: `develop` đã nhận `aab533e7 [Bugfix] Core báo cáo: mã quyền façade + Redis timeout (#176)`, commit này sửa **4** mã quyền sai chứ không chỉ 1:

| reportId | develop (#176) | PR #171 (dựa trên bản cũ) |
|---|---|---|
| `bang-ke-chung-tu` | `BCKeChungTu.View` | `BCBangKe.View` ← **lùi** |
| `bao-cao-chi-phi-theo-bo-phan` | `BCChiPhiBoPhan.View` | `BCChiPhiTheoBoPhan.View` ← **lùi**, mã này 0 lần trong seed |
| `phan-bo-theo-thang` | `BCPhanBoCPTT.View` | `BCPhanBoTheoThang.View` ← **lùi**, mã này 0 lần trong seed |
| `so-nhat-ky-thu-tien` | `BCNhatKyThuTien.View` | `BCNhatKyThuTien.View` (**trùng lặp — develop đã làm rồi**) |

  Tương ứng, `develop` đã đưa `NO_CHUA_SEED` về **rỗng** (`isEmpty()`), còn PR đưa về **2 mục** (`hasSize(2)`) — vi phạm chính luật mà file test tự đặt: *"Nợ chỉ được ngắn đi"*.

- **Actual vs expected**: PR không merge được tự động; nếu người resolve chọn nhầm phía "ours", hai báo cáo *Chi phí theo bộ phận* và *Phân bổ theo tháng* quay lại trạng thái **403 cho mọi người kể cả chủ tenant** (mã không nằm trong catalog thì không ai gán được), và `bang-ke-chung-tu` trỏ về mã không canonical. Expected: rebase/merge `develop` vào nhánh, giữ nguyên 4 mã canonical + `NO_CHUA_SEED` rỗng, **chỉ còn lại đúng một dòng mới** là `so-nhat-ky-chi-tien` → `BCNhatKyChiTien.View` cùng test của nó.
- **Hậu quả**: mất quyền truy cập 2 báo cáo đã được sửa; test `danhSachNoChuaSeedKhongDuocDaiThem` sẽ đỏ hoặc bị sửa ngược cho xanh.

---

## Major

### M1 — Sau khi rebase, phần lớn diff là no-op; commit `b27829aa` trùng hoàn toàn với #176

- **File**: `ReportPermissionRegistry.java:32` (`so-nhat-ky-thu-tien`), test `soNhatKyThuTienDungMaDaSeed`, và cả phần sửa `NO_CHUA_SEED`.
- **Nguồn**: `conventions-chung.md` §4.1 "1 commit = 1 ý nghĩa"; `bon-lop.md` §Lớp D "boy-scout đúng phạm vi".
- **Trigger**: commit `b27829aa fix(reporting): mã quyền Sổ nhật ký thu tiền về BCNhatKyThuTien.View (PMKT-E-10784)` sửa đúng thứ `aab533e7` trên `develop` đã sửa.
- **Actual vs expected**: PR hiện mang 2 commit, trong đó 1 commit trùng lặp; expected là PR chỉ còn `cdd900ad` (chi tiền) sau khi rebase.
- **Hậu quả**: diff giả, che mất thay đổi thật (một dòng chi tiền), và là nguyên nhân trực tiếp của xung đột ở B1. Sau rebase phải kiểm lại còn nội dung gì mới không — nếu chỉ còn 1 dòng + 1 test thì PR rất gọn và duyệt nhanh.

---

## Minor

### m1 — `reportId` `so-nhat-ky-chi-tien` chưa có bằng chứng khớp với `report-service`

- **File**: `ReportPermissionRegistry.java:33`
- Javadoc của chính lớp này ghi registry là "bản SAO tay của `ReportDefinition.permission()` bên `report-service`", hai repo **không có cơ chế đồng bộ**. Slug `so-nhat-ky-chi-tien` không kiểm chứng được trong repo `cell-app`, và PR **body rỗng** nên không có link/ảnh chứng minh.
- Sai slug ⇒ báo cáo trả **404 `REPORT_UNKNOWN`** (fail-closed, không mở toang) — không nguy hiểm nhưng là lỗi câm. Đề nghị tác giả dán bằng chứng `reportId` từ `report-service`, hoặc một lượt gọi thật `GET /reports/so-nhat-ky-chi-tien/params`.

### m2 — FE chưa đăng ký báo cáo chi tiền ⇒ tính năng chưa tới người dùng

- **File (repo khác, tham chiếu)**: `client/src/app/pages/baoCao/reportCatalog.ts` — 24 mục, có `so-nhat-ky-thu-tien` → `BCNhatKyThuTien.View` (khớp PR), **không có** mục nào cho chi tiền.
- Hậu quả: merge PR này xong, *Sổ nhật ký chi tiền* vẫn không xuất hiện trên UI. Không phải lỗi của diff BE, nhưng cần PR FE đi kèm; nêu để đừng đóng epic PMKT-E-10786 sớm.

---

## Nit

### n1 — Tên nhánh sai chuẩn

`feature/sonhatkythutien` — `conventions-chung.md` §4.2/4.3 quy định tiền tố `feat/` và tên **chữ thường phân cách bằng `-`**. Đúng phải là `feat/so-nhat-ky-thu-chi-tien`. Tên nhánh cũng chỉ nhắc "thu tiền" trong khi PR làm cả chi tiền.

### n2 — PR body rỗng

Không mô tả, không link epic (PMKT-E-10784 / PMKT-E-10786 chỉ nằm trong commit message và javadoc test). Người review phải tự suy ra phạm vi.

---

## Lớp A — Cổng cứng

| Mục | Kết quả |
|---|---|
| Secret trong diff | ✅ không có |
| Hardcode magic value | ✅ N/A — hai chuỗi thêm vào là **dữ liệu của chính bảng tra** `PERMISSION_BY_REPORT_ID`, đúng chỗ constant |
| i18n (FE) | ✅ N/A — diff thuần Java, không có text UI mới |
| `any` / `@ts-ignore` / `../../` | ✅ N/A — không chạm `client/` |
| BE phân tầng Controller→Service→Repository | ✅ `ReportProxyController` gọi `ReportProxyService`, registry là `@Component` tầng service; diff không đụng controller |
| `ApiResponse<T>` | ✅ N/A — façade proxy chuyển tiếp nguyên byte của `report-service` (AD-40, thiết kế có sẵn); lỗi vẫn ném `ApiException` cho `@RestControllerAdvice` |
| Nuốt exception / try-catch thủ công | ✅ không có |
| Vùng đóng băng (`master_data`, `legacy`, `Phase_2`) | ✅ không chạm — mọi grep đều giới hạn trong `cell-app/src`, `client/src`, `docs/` |
| Nghiệp vụ tự bịa | ✅ không — mã quyền đối chiếu thẳng với seed `V2__seed_data.sql` |
| Base package | ✅ `vn.vtt.pmkt` đúng chuẩn của `cell-app` |

## Lớp B — Bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ đúng shape Modulith: file nằm trong `reporting/internal/service/`, `reporting/package-info.java` tồn tại, không tạo `api/` thừa |
| 2 | Không đánh lại version migration | ✅ N/A — diff **không có** file migration nào. Không cần quét tranh số Flyway |
| 3 | Chưa test lại sau khi merge | ⚠ **B1** — develop +4 commit, **2/2 file giao nhau**, `merge-tree` CONFLICT cả hai |
| 4 | N+1 / query trong vòng lặp | ✅ N/A — không có JPA/repository/truy vấn nào trong diff; registry là `Map` tĩnh trong bộ nhớ |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ N/A — không có CRUD/entity/chứng từ mới |
| 6 | Chưa tận dụng base FE | ✅ N/A — không chạm FE |
| 7 | Constant đặt sai chỗ | ✅ giá trị mới nằm trong đúng bảng tra `private static final Map` của lớp chuyên trách |

## Lớp C — Nghiệp vụ & truy vết

| Cổng | Kết quả |
|---|---|
| `trace.sh` | **NOT-RUN** — không tồn tại thư mục spec `docs/doing/*-spec` cho PMKT-E-10784 / PMKT-E-10786 |
| `msg.sh` | **NOT-RUN** — diff trải trên **hai** epic (`pmkt-docs/ba/PMKT-E-10784_SoNhatKyThuTien` và `PMKT-E-10786_SoNhatKyChiTien`), không có một thư mục PYC đơn để truyền vào; ngoài ra diff không thêm message hiển thị nào |
| `01-conflict.md` P0/P1 OPEN | N/A — chưa có spec |
| BR đã đọc | **không BR nào** — diff không nhắc mã `BR…`, không có luật `R-…` liên quan; mọi finding đều dựa trên bằng chứng kỹ thuật đo được (seed SQL, `git merge-tree`). BR chưa đọc: toàn bộ (có chủ đích, theo §BR "đọc theo diff") |

## Lớp D — Vệ sinh diff & Git

| Mục | Kết quả |
|---|---|
| Commit message | ✅ `feat(reporting): …` / `fix(reporting): …` đúng `<type>(<scope>): <mô tả>`, có mã epic |
| Tên nhánh | ⚠ **n1** |
| Không commit thẳng master/develop | ✅ |
| Code debug / TODO không ticket | ✅ không có |
| Cổng cây commit (file `??` trong `src/`) | ✅ `git status --porcelain` rỗng; không có barrel/`index.ts` trong diff |
| Đổi chữ ký public | ✅ N/A — `requirePermission` giữ nguyên; caller chỉ gồm `ReportProxyService` + test |
| Rename bằng `mv` trần | ✅ N/A |

## Đã đọc / chưa đọc

**Đã đọc**: cả 2 file của diff (bản head đầy đủ) · `ReportProxyService.java` · phần `iam_quyen` / `iam_pham_vi_hieu_luc` liên quan của `V2__seed_data.sql` · `client/src/app/pages/baoCao/reportCatalog.ts` (grep) · diff của `develop` trên đúng 2 file đó.

**Chưa đọc / chưa chạy**: `ReportProxyServiceTest.java` (không nằm trong diff, chỉ grep tên) · `ReportServiceClient` · tài liệu BA `PMKT-E-10784/10786` · **toàn bộ cổng test/build** (`./gradlew unitTest`, `compileJava`) — **NOT-RUN, chế độ nhanh**.

## Lệnh đã chạy

```bash
gh pr view 171 --json ...            gh pr diff 171
git show origin/pr/171:<file>        git ls-tree -r --name-only origin/pr/171 ...
git merge-base origin/develop origin/pr/171
git rev-list --count $MB..origin/develop                       # = 4
comm -12 (diff develop) (diff pr/171)                          # = 2 file giao nhau
git merge-tree --write-tree --name-only origin/develop origin/pr/171   # CONFLICT x2
git diff $MB origin/develop -- <2 file>
git status --porcelain
git grep -n "BCSoNhatKy|SoNhatKyThuTien|so-nhat-ky" origin/pr/171 -- src
grep -n "NhatKyThuTien|NhatKyChiTien" src/main/resources/db/migration/
```

---

## Kết luận — **REJECT**

Có Blocker **B1**. Nội dung nghiệp vụ của bản vá đúng, nhưng nhánh dựa trên `develop` cũ và **xung đột cứng ở cả hai file với `#176` đã merge**; resolve sai một nhịp là lùi 3 mã quyền, trong đó 2 mã đưa báo cáo về trạng thái 403 cho toàn bộ người dùng.

Việc cần làm: rebase lên `origin/develop`, giữ nguyên 4 mã canonical và `NO_CHUA_SEED` rỗng, chỉ để lại đúng dòng `so-nhat-ky-chi-tien` + test `soNhatKyChiTienDungMaDaSeed`, bỏ `soNhatKyThuTienDungMaDaSeed` nếu `develop` đã có bài tương đương. Kèm thêm: **M1**, **m1**, **m2**, **n1**, **n2**.

> ⚠ Review chạy ở **chế độ NHANH** — **cổng test/build chưa chạy** (`./gradlew unitTest` NOT-RUN). Kết luận dựa hoàn toàn trên đọc code và đo bằng git. Không đăng comment lên PR theo yêu cầu của người gọi.
