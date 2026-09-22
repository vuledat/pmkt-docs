# Review cell-app PR #117 — `feat/tscd` → `develop`

**Chế độ: NHANH** (mặc định) — chỉ đọc + kiểm tĩnh bằng git/grep. **KHÔNG** chạy test/build,
không worktree, không baseline, không merge thử.

> **Lượt 2** (08/09/2026). Lượt 1 chấm head `838abf45` và kết luận REJECT. Tác giả đã đẩy 3 commit
> sửa + merge `develop`. Báo cáo này thay thế bản cũ; §"Trạng thái finding lượt 1" ghi lại kết cục
> từng mục, **có đối chiếu bằng chứng mới chứ không nhận lại kết luận cũ**.

| Mục | Giá trị |
|---|---|
| Head | **`b0c864b8`** (`origin/feat/tscd`) — *Correct the phienBan comment to match the guard*, 08/09/2026 11:21 |
| Base | `origin/develop` `969c3892` |
| Merge-base | `73d3ffaf` (PR đã merge `develop` vào ở `dc45f3ef`) |
| Diff vs merge-base | **514 file · +39.618 / −3.295** · 24 commit |
| Working tree | sạch |
| Metadata PR | vẫn **không lấy được** (`gh` chưa cài, API 404 — repo private). Base `develop` là suy ra, ref đã xác minh |

---

## Trạng thái finding lượt 1

| Mã | Lượt 1 | Kết cục — bằng chứng lượt 2 |
|---|---|---|
| B1 | Blocker — `V1116` backfill dưới FORCE RLS rồi `SET NOT NULL` | **BÁC BỎ — tiền đề của tôi sai.** Xem §"Về nhóm RLS" |
| B2 | Blocker — thiếu `FileGroup.GHI_GIAM_TSCD` | **✅ đã sửa** — `41b3ffd5` thêm hằng `GHI_GIAM_TSCD(MaChucNang.GHI_GIAM_TSCD)`, javadoc dẫn đúng cả hai vế (yml + FE constants) |
| M1 · M2 | Major — hai backfill khớp 0 dòng | **BÁC BỎ — cùng lý do B1** |
| m1 | Minor — javadoc `phienBan` trái hành vi guard | **✅ đã sửa** — `b0c864b8` viết lại đúng: null ở luồng Sửa ⇒ 400 `THIEU_PHIEN_BAN`, fail-safe |
| m2 | Minor — 3 file giao nhau với develop, chưa test sau merge | **✅ hết** — PR đã merge `develop` (`dc45f3ef`); đo lại: **0 file giao nhau**, develop chỉ còn đi trước 2 commit |
| n1 | Nit — khối `[GhiGiamTSCD]` thiếu comment | **✅ đã sửa** — `application.yml:197-198` |

### Về nhóm RLS (B1/M1/M2) — tôi sai, và cách sửa tôi đề xuất cũng sai

Commit `fca6ce4c` **gỡ bỏ** mọi cặp `NO FORCE`/`FORCE` (V1111, V1114) thay vì thêm vào, kèm số đo trên
DB dev: `flyway_schema_history.installed_by = pmkt` cho cả 102 migration đã apply, **`pmkt` là
superuser**, role thay thế `pmkt_dev` có **BYPASSRLS** — cả hai bỏ qua RLS bất kể FORCE. Tác giả replay
9 migration trên clone DB dev: mọi backfill khớp đúng số dòng, `SET NOT NULL` thành công.

Tôi không có datasource để đo lại (`list_database_connections` → rỗng), nhưng **kiểm được cơ chế của
lập luận thứ hai** trong commit message và nó đúng: `V1__create_database.sql:24694` có
`CREATE TRIGGER trg_audit_fa_tai_san AFTER INSERT OR DELETE OR UPDATE ON public.fa_tai_san_co_dinh`, và
`aud_audit_log` cũng `FORCE ROW LEVEL SECURITY` với `WITH CHECK (tenant_id = fn_current_tenant())`
(`:4668`, `:30887`). Nên dưới một role **không** bypass, việc bọc `NO FORCE` chỉ cho `UPDATE` đi qua để
rồi chết ở trigger audit — **tệ hơn không bọc**, đúng như commit message nói. Cách sửa tôi đề xuất ở
lượt 1 sẽ không cứu được gì.

Trạng thái hiện tại nhất quán: 9 migration **không còn** dòng `NO FORCE` nào; hai dòng `FORCE ROW LEVEL
SECURITY` còn lại (V1114:82, V1115:110) là phần **dựng bảng mới**, đúng chỗ.

Còn lại một điều kiện vận hành, ghi thành **m3** dưới đây.

---

## Findings lượt 2

### 🟡 m3 — Minor · quyền của role Flyway mới chỉ đo trên DB dev

`fca6ce4c` đo `pmkt` (superuser) và `pmkt_dev` (BYPASSRLS) trên **DB dev**. Chín migration này còn phải
chạy ở staging/production, nơi `DB_MIGRATION_USER` (`application.yml:32`) có thể là role khác.

**Trigger**: apply V1109–V1117 bằng một role không superuser và không BYPASSRLS.
**Actual**: mọi `INSERT`/`UPDATE` chạm bảng `fa_*` có trigger audit đều chết ở `aud_audit_log`
(policy `WITH CHECK` không thoả) — không riêng backfill.
**Expected**: xác nhận role migration của staging/prod có bypass, hoặc `SET app.tenant_id` phù hợp
trong phiên migration.
**Hậu quả**: không phải lỗi code — là điều kiện triển khai cần chốt trước khi deploy. Đề nghị ghi một
dòng vào `deploy/env/` hoặc IMPLEMENT.md thay vì để ngầm.

### 🟡 m4 — Minor · `TinhKhauHaoThemMoiCalculator` tồn tại **hai bản**, bản cũ là dead code và là bẫy resolve im lặng

| Đường dẫn | Chữ ký `tinhDuongThang` | Caller |
|---|---|---|
| `tai_san_co_dinh/ghi_tang/internal/TinhKhauHaoThemMoiCalculator.java` (49 dòng) | `(giaTri, thoiGianNam, **soChuSoTien**)` + có `tinhSanLuong` | 3 file main + 1 test |
| `…/ghi_tang/internal/**service**/TinhKhauHaoThemMoiCalculator.java` (33 dòng) | `(giaTri, thoiGianNam)` — **hardcode `setScale(2)`** | **0** |

Bản `internal/` là bản đúng; javadoc của nó nói rõ mục đích: *"soChuSoTien … trước hardcode 2, gây lệch
BE↔FE khi tenant cấu hình khác 2 (vd VND = 0 chữ số)"* — tức bản `internal/service/` chính là bản lỗi mà
nó ra đời để thay. `git grep "ghi_tang.internal.service.TinhKhauHaoThemMoiCalculator"` → 0 kết quả; test
tương ứng đã bị xoá trong diff. File main thì còn.

**Trigger**: một dev sau này viết code trong package `…ghi_tang.internal.service` (nơi có
`TaiSanCoDinhCrudService`, `PhanBoKhauHaoService`) gọi `TinhKhauHaoThemMoiCalculator.tinhDuongThang(a, b)`.
**Actual**: Java resolve về bản **cùng package** trước, không cần import, **không cảnh báo gì** — nhận
scale 2 cứng.
**Expected**: chỉ còn một bản; bản `internal/service/` bị xoá cùng test của nó.
**Hậu quả**: hôm nay 0 caller nên chưa sai số; đây là bẫy để lại, và là mảnh sót của đợt rename
`fixed_asset` → `tai_san_co_dinh` (kiểm: **0** đường dẫn/`import` nào còn `fixed_asset`, chỉ sót file này).

### ⚪ n2 — Nit · `TongPhatSinhSoCaiDto` nhân bản y hệt ở hai slice

`ghi_giam/internal/dto/` và `khau_hao/internal/dto/` cùng khai
`record TongPhatSinhSoCaiDto(BigDecimal tongPhatSinhNo, BigDecimal tongPhatSinhCo)`; `dieu_chinh/` có bản
thứ ba đổi tên (`TongPhatSinhSoCaiDieuChinhDto`). Cả hai bản đầu **đều có caller** nên không phải dead
code, nhưng các slice nằm trong **cùng một** Modulith module và `package-info.java` của module nói rõ
chúng đọc thẳng `internal` của nhau — không có ranh giới nào buộc phải nhân bản. Gộp về một chỗ dùng
chung khi tiện.

### ⚪ n3 — Nit · javadoc `SinhButToanGhiGiam#apDung` còn nói B1 bị BLOCKED

`ghi_giam/internal/service/business/SinhButToanGhiGiam.java` — javadoc **lớp** nói B1 đã bật (*"Nay đọc
`TaiKhoanNgamDinhApi.traCuu` theo `ct.getTaiKhoanNgamDinhId()`"*) và code làm đúng thế
(`tknDTheoVaiTro` được gọi trong `xayDungDongHachToan`), nhưng javadoc của `apDung` ngay dưới vẫn viết
*"KHÔNG đọc `taiKhoanNgamDinhId`/'Lý do ghi giảm' … BLOCKED PMKT-E-00093"*. Hai đoạn nói ngược nhau
trong cùng một file; kết luận *"xây lại luôn cho kết quả giống hệt"* cũng không còn đúng sau B1 (đổi Lý
do ghi giảm ⇒ đổi TK ⇒ đổi bút toán). Hành vi code đúng, chỉ chú thích lạc hậu.

---

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| 1. Hợp đồng & ranh giới | ✅ `FileGroup` ↔ `application.yml` ↔ FE constants nay khớp cả 4 màn TSCĐ; `SoChungTuApi.choPhepSuaSo` đã kiểm caller (một test double duy nhất, đã cập nhật) |
| 2. Nghiệp vụ | ✅ trong phạm vi đã đọc — BR12 khớp `XungDotSuaGuard`; công thức ghi giảm (`SinhButToanGhiGiam`) cân: Có 211 = HMLK + GTCL, ước tính TH1 kẹp trần theo GTCL nên hai vế đối xứng; `LoaiChungTuChu` ↔ CHECK V1110 đồng bộ một chiều đúng, có test ghim. ⚠ n3 (chú thích) |
| 3. Kỹ thuật/dữ liệu | ✅ nhóm RLS đã được đo và gỡ nhất quán; ⚠ m3 (điều kiện role ở môi trường khác dev) |
| 4. Vận hành & tương thích | ✅ 0 file giao nhau với develop; version migration không tranh chấp |

## Bảng bảy lỗi

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Trùng version migration | ✅ develop max = **V1101**; V1109–V1117 chỉ `feat/tscd` giữ (quét toàn bộ remote branch). Ghi chú: cặp `V1099` trùng của develop ở lượt 1 đã tự hết sau merge #130/#131 |
| 2 | Viết lại khung có sẵn | ⚠ **m4** — bản sao thứ hai của `TinhKhauHaoThemMoiCalculator`. Còn lại ✅ (`BaseCrudController`, `ChungTuTemplate`, `SoChungTuApi`) |
| 3 | Chưa test lại sau merge | ✅ N/A — `comm -12` cho **0 file** giao nhau; develop đi trước merge-base 2 commit |
| 4 | Sai tầng kiến trúc | ✅ 0/7 controller `public`, không controller nào gọi Repository |
| 5 | N+1 | ✅ không thấy qua quét tĩnh (không có `Repository.find*/save` trong thân vòng lặp ở `*/internal/service/**`); `SinhButToanGhiGiam` gom `layThongTin(ids)` + 2 truy vấn tập hợp thay vì hỏi từng tài sản |
| 6 | Hardcode magic value / i18n | ✅ trong phạm vi đã đọc — hệ số BR_GTTSCD_12, nhãn nghiệp vụ, mã lỗi đều là hằng có tên; message đi qua `MaLoi*` + messageId |
| 7 | Cấu trúc module | ✅ `@ApplicationModule` neo ở `tai_san_co_dinh`, 8 slice con cố ý không khai module lồng (ghi rõ lý do); `master_data/*/api/` có `@NamedInterface` và có tiền lệ trên develop. ⚠ n2 (DTO nhân bản) |

## Trace / message

| Cổng | Kết quả |
|---|---|
| `trace.sh` | **NOT-RUN** — không có `docs/doing/*-spec` cho TSCĐ |
| `msg.sh` | **NOT-RUN** — diff trải **7 epic**, không có thư mục PYC đơn. (Lượt 1 đã thử chạy cho một epic và kết quả vô hiệu vì working tree đứng ở nhánh khác — không lặp lại.) Thay bằng đếm trên đúng ref `b0c864b8`: 02535 **41** mã · 02547 **27** · 02569 **32** · 02578 **29** · 02600 **29** · 02606 **20** · 03000 **17**. Chỉ dấu hiện diện, không thay được đối chiếu nguyên văn |

## BR đã đọc

`br.sh --list` + **BR12** (đối chiếu nguyên văn với `XungDotSuaGuard` — khớp).
**Chưa đọc**: BR02, BR17, BR25, BR41, và các BR nội bộ màn `BR_GGTSCD_*` / `BR_GTTSCD_*` của `SCR_*`
(đọc gián tiếp qua trích dẫn trong javadoc, **không** mở file SCR gốc). Diff trải 7 epic nên vượt trần
10 BR của quy trình.

## Lệnh đã chạy

```
git fetch origin refs/pull/117/head:refs/tmp/review-pr117-r2   → b0c864b8 (đổi so với lượt 1)
git log --oneline 838abf45..<head>                             → 3 commit sửa + merge develop
git show fca6ce4c / 41b3ffd5 / b0c864b8                        → soát từng commit sửa
git merge-base origin/develop <head>                           → 73d3ffaf
git rev-list --count <MB>..origin/develop                      → 2
comm -12 <(…develop) <(…head)                                  → 0 file
git ls-tree origin/develop <db/migration> | sort -V | tail     → max V1101
for b in $(git branch -r …) … grep -E "V11(09|1[0-7])__"       → chỉ feat/tscd
git show <head>:V11xx__*.sql | grep -E "UPDATE|INSERT|FORCE"   → 9/9 migration
git grep -n "TinhKhauHaoThemMoiCalculator|fixed_asset|TongPhatSinhSoCaiDto" <head>
git ls-tree -r --name-only <head> … | sed 's#.*/##' | sort | uniq -d   → 3 tên trùng
git status --porcelain                                          → sạch
./docs/rules/br.sh --list · br.sh 12
```

Không chạy: `./gradlew unitTest`, `build`, worktree, merge thử, baseline — **chế độ nhanh**.
Không xác minh được quyền role trên DB (không có datasource IntelliJ) — xem m3.

## Chưa đọc

Thêm so với lượt 1, lượt này đã đọc: `SinhButToanGhiGiam` (toàn bộ công thức HMLK/GTCL + ước tính TH1/TH2),
cả hai bản `TinhKhauHaoThemMoiCalculator`, `PhanBoKhauHaoService` (phần công thức), 3 commit sửa.

**Vẫn chưa đọc (≈ 290 file main)**: `TaiSanCoDinhCrudService` (111 KB — mới đọc `update()`),
`DieuChuyenTaiSanCrudService`, `KhauHaoTaiSanCrudService`, `KhauHaoThemMoiService`,
`BienDongTrongKyQuery`, `PhanBoHieuLucCalculator`, `TinhKhauHaoEngineImpl`, `GhiGiamValidator`,
`SuaDieuChinhTaiSanCoDinh`, toàn bộ mapper/repository và **120 file test**. Engine tính khấu hao hàng kỳ
**vẫn chưa được review**.

---

## Kết luận: **REQUEST CHANGES** (không còn Blocker)

Hai Blocker và hai Major của lượt 1 đã hết: B2/m1/m2/n1 được sửa đúng, còn B1/M1/M2 là **kết luận sai
của tôi** — tác giả đã đo trên DB thật và bác bỏ tiền đề, kèm lập luận về audit trigger mà tôi kiểm lại
được là đúng.

Còn lại: **m4** (bản sao calculator hardcode scale — nên xoá trước khi merge), **m3** (chốt quyền role
migration cho staging/prod), **n2**, **n3**.

Không APPROVE ở chế độ nhanh: `./gradlew unitTest` và build **chưa chạy**, và ~290 file nghiệp vụ —
đáng kể nhất là engine tính khấu hao hàng kỳ — chưa được đọc.
