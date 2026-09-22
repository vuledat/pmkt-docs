# Review cell-app PR #145 — Feat/chi phi tra truoc

**Chế độ:** NHANH (chỉ đọc + kiểm tĩnh bằng git; **không** chạy test/build, **không** worktree,
**không** đo baseline, **không** merge thử).

| Mục | Giá trị |
|---|---|
| PR | https://github.com/ospgroupvn-pmkt/cell-app/pull/145 · OPEN · tác giả `tichvd-osp` |
| head | `023c57b930f64b51ebdd493f9bf18c9e4e58e6fe` (`feat/chi-phi-tra-truoc`) |
| base | `origin/develop` = `ce79f419` (đã xác minh từ metadata PR, không suy từ tên nhánh) |
| merge-base | `c6cb948ecb67faf13c3c9e59edc321664522c7c1` |
| Phạm vi | 115 file · +11 428 / −122 · 4 commit |
| Vùng đóng băng | không có file nào rơi vào `master_data/**`, `legacy/**`, `Phase_2/**` |

Epic: **PMKT-E-05853 Chi phí trả trước** — sub-module mới `chi_phi_tra_truoc/khai_bao/`
(53 file mới), sửa `chi_phi_tra_truoc/phan_bo/`, cộng 4 file kernel
(`ChungTuTemplate`, `GhiSoRequest`, `DinhKhoanValidator`, `GhiSoService`), 6 file
`tham_chieu_chung_tu/`, 2 migration mới.

---

## Kết luận

**🔴 REJECT** — 1 Blocker (B1), 3 Major (M1–M3).

Chất lượng code trong phạm vi đã đọc là **cao khác thường**: kiến trúc Modulith đúng khuôn,
dùng lại trọn `BaseCrudController` / `AbstractCrudService` / `@Searchable` / `ChungTuTemplate` /
`GhiSoApi`, tra danh mục theo mẻ (không N+1), có 3 arch test tự viết để bịt đúng những lớp lỗi
đã từng gây sự cố. Các finding dưới đây **không** phải lỗi logic nghiệp vụ mà là lỗi **cổng
tích hợp** (số migration), **bằng chứng quyết định** và **độ phủ test cho phần kernel bị nới**.

⚠ Chế độ nhanh: `./gradlew unitTest` **chưa chạy**. Không dùng báo cáo này thay cổng test.

---

## Findings

### 🚫 B1 — Trùng số migration `V1111`/`V1112` với **hai** nhánh chưa merge

**File:** `src/main/resources/db/migration/V1111__cptt_phan_bo_chi_tiet_don_dat_hang_hop_dong.sql:1`
· `V1112__acc_so_cai_la_ve_no_khoa_duy_nhat.sql:1`
**Nguồn:** bảng bảy lỗi #2 (`references/bon-lop.md`) · SKILL §3a "Đụng số với nhánh chưa merge"
**Trigger:**

```
origin/bugfix/httk-theo-thong-tu:  V1111__httk_dung_chung_theo_thong_tu.sql
                                   V1112__trang_thai_danh_muc_default_hoat_dong.sql
origin/feat/chung-tu-ban-hang-2:   V1111__iam_quyen_bieu_mau.sql
origin/feat/chi-phi-tra-truoc:     V1111__cptt_...  V1112__acc_so_cai_...
origin/develop (max):              V1110__fa_chi_tiet_bo_sung_chi_nhanh_id.sql
```

**Actual / Expected:** ba nhánh cùng giành `V1111`, hai nhánh cùng giành `V1112` / mỗi nhánh một
dải số riêng.
**Hậu quả:** nhánh nào merge **sau** sẽ vỡ Flyway trên môi trường đã chạy nhánh trước —
`checksum mismatch` hoặc `Found more than one migration with version 1111`, service không boot.
Đây đúng cơ chế đã làm hỏng dải `V1064+` trước đây.
**Đề xuất:** thống nhất thứ tự merge rồi đánh lại số cho nhánh sau; xem
`docs/rules/migration-danh-so-theo-timestamp.md`. Không phải lỗi riêng của PR này, nhưng là chặn
merge có thật.

---

### ⚠️ M1 — Bằng chứng "BA đã chốt" cho hai thay đổi kernel **không có trong repo**

**File:** `src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/dto/GhiSoRequest.java:48`
· `chi_phi_tra_truoc/phan_bo/internal/service/business/DinhKhoanPhanBoCptt.java:12`
**Nguồn:** CLAUDE.md luật 9 + §Cổng đặc tả luật 1 ("`CLOSED-BA` thiếu tên người hoặc thiếu ngày
thì tính như `OPEN`")
**Trigger:**

```bash
git ls-tree --name-only 023c57b9        # không có thư mục dev-plan/
git show 023c57b9:.gitignore | grep dev-plan   # cũng KHÔNG bị ignore
```

Hai quyết định nặng cùng viện dẫn một file duy nhất
`dev-plan/tichvd/trao-doi-ba/tra-loi/PMKT-E-05853-cptt-2026-09-08.md`:

1. `DinhKhoanValidator:87` — **nới luật "TK Nợ ≠ TK Có" của toàn hệ thống** thành cờ opt-in.
2. `DinhKhoanPhanBoCptt:83` — **đảo chiều bút toán**: `new ChieuNoCo(taiKhoanChoPhanBoId,
   taiKhoanChiPhiId)` thay cho `(taiKhoanChiPhiId, taiKhoanChoPhanBoId)`, tức Nợ 242 / Có 6xx —
   ngược TT200 và ngược cài đặt của module CCDC.

**Actual / Expected:** người review không mở được nguồn quyết định / quyết định lệch chuẩn kế
toán phải để lại bằng chứng kiểm chứng được trong cây commit.
**Hậu quả:** mỗi lần phân bổ làm **tăng** dư Nợ 242 thay vì rút dần — nếu bản chốt bị hiểu sai
thì sai lệch chỉ lộ ra ở quyết toán. Chính javadoc thừa nhận BA ghi *"không phải kết luận rằng
chiều này là hướng dẫn kế toán chuẩn"*.
**Đề xuất:** commit file trả lời BA vào repo (hoặc `pmkt-docs/`), hoặc dán nguyên văn kết luận +
tên người chốt + ngày vào javadoc để `CLOSED-BA` đủ điều kiện.

---

### ⚠️ M2 — Cờ `chapNhanNoCoTrung` nới chốt chặn kernel mà **không có test nào**

**File:** `src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/internal/ghi_so/DinhKhoanValidator.java:87`
**Nguồn:** bảng bảy lỗi #5 (bất biến của kernel) · `truy-vet-luat.md` (luật P0 phải có test hồi quy)
**Trigger:**

```bash
git grep -l "chapNhanNoCoTrung" 023c57b9 -- src/test   # → 0 kết quả
```

**Actual / Expected:** 0 test / tối thiểu 2 unit test trên `DinhKhoanValidator`
(`false` → ném `tài khoản Nợ trùng tài khoản Có`; `true` → đi qua), cộng 1 test khẳng định
`GhiSoRequest` dạng 8 tham số mặc định `false`.
**Hậu quả:** luật chống bút toán vô nghĩa (Nợ = Có, sổ cái không đổi một đồng) áp cho **mọi**
loại chứng từ nay có đường vòng, và không có gì đỏ nếu một template khác vô tình override
`chapNhanNoCoTrung()` thành `true`. Constructor phụ 8 tham số giữ 7 nơi gọi cũ đứng yên là lựa
chọn đúng, nhưng nó cũng làm mất luôn áp lực compile buộc người thêm module mới phải cân nhắc cờ.

---

### ⚠️ M3 — Ba mã message do dev tự cấp, không có trong `6.messages.md`, FE cũng chưa có key

**File:** `chi_phi_tra_truoc/khai_bao/internal/model/MaLoiKhaiBaoCptt.java:84,98` ·
`chi_phi_tra_truoc/phan_bo/internal/model/MaLoiPhanBoCptt.java:75`
**Nguồn:** CLAUDE.md luật 9 + §Cổng đặc tả luật 2 ("Không tự đặt luật mới → mở mục `OPEN` và hỏi")
· `truy-vet-luat.md` (message phải mang **chính mã** của BA)
**Trigger:** đối chiếu mã trong code (head PR) với `pmkt-docs/ba/PMKT-E-05853_ChiPhiTraTruoc/6.messages.md`:

```
Trong code mà KHÔNG có trong doc: _052 _053 _204
Trong doc mà chưa dùng trong code: _014 (trùng nghĩa _110 — chấp nhận được) · _111 (cảnh báo, FE lo)
```

Chính javadoc đã tự khai: *"`_052` là mã mới do dev cấp… **cần bổ sung vào 6.messages.md**"*.
`grep` trên `client/src` cho cả ba mã = **0 kết quả**.
**Actual / Expected:** 3 mã không có nguồn / mọi `messageId` phải có dòng tương ứng trong
`6.messages.md` do BA cấp.
**Hậu quả:** toast của ba luật này không có bản dịch — người dùng thấy mã thô hoặc chuỗi rỗng;
và BA không có đường biết ba luật đó tồn tại. Đây là 2/59 mã còn lại thì rất tốt (57/59 khớp
nguyên văn), nhưng ba mã tự cấp vẫn phải qua BA.

---

### 🔸 m1 — A3 cắt `LIMIT` **trước** khi loại trừ BR01 → mất ứng viên hợp lệ

**File:** `chung_tu_mua_hang/internal/repository/UngVienChungTuGocCpttQuery.java:96` (`LIMIT :gioiHan`)
· `chi_phi_tra_truoc/khai_bao/internal/service/UngVienChungTuGocService.java:98-101`
**Trigger:** khoảng ngày rộng, > 500 dòng mua dịch vụ đã ghi sổ, phần lớn đã được khai báo CPTT
khác dùng.
**Actual / Expected:** SQL lấy 500 dòng đầu → service bỏ dòng đã dùng → còn rất ít / người dùng
phải thấy đủ 500 ứng viên **còn dùng được**.
**Hậu quả:** popup hiển thị ít dòng một cách khó hiểu và **không có đường tới các dòng phía sau**
— popup cố ý không phân trang phía server (F2-D3), nên trần là lối duy nhất. Sửa bằng
`NOT EXISTS` trên `ref_chung_tu_tham_chieu` ngay trong SQL, hoặc lấy dư rồi mới cắt.

### 🔸 m2 — `NativeSqlCotTonTaiTest` bỏ sót đúng các câu native mà PR này thêm

**File:** `src/test/java/vn/vtt/pmkt/cell/arch/NativeSqlCotTonTaiTest.java:60-63`
**Trigger:** `@ValueSource` chỉ liệt kê 3 file ("ba câu native ra đời cùng A3"), trong khi PR còn
thêm: `TrangThaiPhanBoKhaiBaoRepository.SQL_KY`, `TraCuuDanhMucKhaiBaoCpttRepository` (6 câu),
`ThongKePhanBoCpttRepository.namConPhaiPhanBo`.
**Hậu quả:** đúng lớp lỗi mà test này sinh ra để bắt (sai TÊN cột → 500 lúc chạy, xanh lúc build)
vẫn còn cửa. Cụ thể `SQL_KY` join `cptt_chung_tu_phan_bo_chi_phi_tra_truoc_khai_bao` —
bảng/cột được tạo rải ở `V1` + `V1011`, không có gì kiểm hộ. Thêm 3 đường dẫn vào `@ValueSource`
là đủ.

### 🔸 m3 — `V1112` viết lại toàn bộ `acc_so_cai` + mọi partition, `lock_timeout=10s`

**File:** `src/main/resources/db/migration/V1112__acc_so_cai_la_ve_no_khoa_duy_nhat.sql:53`
**Trigger:** `ADD COLUMN … GENERATED ALWAYS AS (…) STORED` trên bảng partition RANGE.
**Actual / Expected:** migration khoá `ACCESS EXCLUSIVE` và rewrite toàn bảng; `lock_timeout=10s`
làm nó **thất bại nhanh** (đúng ý đồ) thay vì treo — nhưng trên môi trường có tải thì Flyway sẽ
dừng nửa chừng và service không boot.
**Hậu quả:** cần cửa sổ bảo trì. File đã tự cảnh báo; ghi ở đây để người deploy không bỏ sót.
Không phải lỗi code.

### 🔸 m4 — Hardcode giá trị DB của `TrangThaiKhaiBao` trong câu native của sub-module khác

**File:** `chi_phi_tra_truoc/phan_bo/internal/repository/ThongKePhanBoCpttRepository.java`
(hằng `TRANG_THAI_CON_PHAN_BO = List.of("ChuaPB", "DangPB")`)
**Nguồn:** CLAUDE.md luật 1 (không hardcode magic value)
**Actual / Expected:** chuỗi thô / lấy từ `TrangThaiKhaiBao.CHUA_PB.giaTri()` (enum có sẵn
`JpaConverter`, tức đã có `giaTri()`).
**Hậu quả:** enum đổi giá trị lưu DB thì câu này **im lặng** trả danh sách năm rỗng — màn Phân bổ
mất ô chọn năm mà không lỗi. Là hằng số có tên nên không phải vi phạm nặng, nhưng nguồn sự thật
đang bị nhân đôi.

### 🔸 m5 — Popup "Chọn chứng từ gốc" gác `.Create`, nhưng cũng mở từ màn Sửa

**File:** `chi_phi_tra_truoc/khai_bao/internal/controller/KhaiBaoCpttController.java:181`
(`quyen.require(maChucNang(), QuyenChecker.CREATE)`)
**Trigger:** người dùng chỉ được cấp `GhiTangCPTT.Edit` (không có `.Create`) mở popup ở màn Chỉnh sửa.
**Actual / Expected:** 403 / popup mở được.
**Hậu quả:** nhóm quyền "chỉ sửa" không dùng nổi tab Chứng từ gốc. Javadoc đã tự ghi nợ
(*"cần `requireAny` ở `QuyenChecker`"*) nhưng không có ticket kèm theo — nợ không có mã ticket
thì không ai đòi.

### 💬 n1 — `feat: init chi phi tra truoc` thiếu `scope`

**Nguồn:** CLAUDE.md luật 8 (`<type>(<scope>): <mô tả>`). Ba commit còn lại đúng chuẩn
(`fix(cptt): …`). Tiêu đề PR "Feat/chi phi tra truoc" là tên nhánh, không phải mô tả.

### 💬 n2 — `FileGroup.GHI_TANG_CPTT` thiếu dòng trắng trước javadoc kế tiếp

**File:** `common/storage/api/FileGroup.java:164` — hằng mới dán sát javadoc của
`DIEU_CHINH_TSCD` phía dưới, lệch định dạng so với phần còn lại của enum.

---

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| **A — Cổng cứng** | ✅ không có secret · ✅ không `any`/`@ts-ignore` (không có diff FE) · ✅ Controller không chứa logic, không gọi Repository, không trả Entity · ✅ mọi response bọc `ApiResponse<T>` · ✅ lỗi qua `ApiException` + `@RestControllerAdvice` · ✅ không chạm vùng đóng băng (`TraCuuDanhMucKhaiBaoCpttRepository` cố ý đọc `mst_*` bằng native SQL thay vì import `master_data` — đúng lối thoát đã ghi) · ⚠ "nghiệp vụ tự bịa": xem **M1** (đảo chiều Nợ/Có) và **M3** (3 mã message tự cấp) |
| **B — Kiến trúc & 7 lỗi** | xem bảng dưới |
| **C — Nghiệp vụ & truy vết** | `trace.sh` **NOT-RUN** — không có `docs/doing/*05853*-spec/`, epic này chưa qua `/audit-spec`. `msg.sh` chạy được nhưng **kết quả không dùng được** (nó đọc working tree, đang ở nhánh khác); đã thay bằng đối chiếu trực tiếp trên head PR — kết quả ở **M3** |
| **D — Vệ sinh diff & Git** | ✅ `git status --porcelain` sạch · ✅ không có file `??` trong `src/` · ✅ không rename bằng `mv` trần · ✅ diff không trộn refactor hàng loạt · ⚠ n1 (commit message) |

## Bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ đúng khuôn `<module>/api|internal/` — `chi_phi_tra_truoc/api/` + `api/dto/` đều có `package-info.java` khai `@NamedInterface`, mọi thứ còn lại nằm trong `internal/`; không có file phẳng ở gốc module. `ChiPhiTraTruocModularityTest` ghim lại |
| 2 | Không đánh lại version migration | 🚫 **B1** — `V1111`/`V1112` trùng với 2 nhánh chưa merge |
| 3 | Chưa test lại sau khi merge | ✅ N/A — `git rev-list --count c6cb948e..origin/develop` = **2** commit, `comm -12` giao nhau = **0 file**. Không cần merge thử |
| 4 | N+1 | ✅ tra danh mục theo mẻ (`Set<UUID>` → `Map`, 5 câu cố định); `thongKe` gộp 8 số vào 1 lần quét bằng `SUM(CASE…)`; `ChungTuPhanBoCpttRepository` tách `@EntityGraph` thành 2 query để né MultipleBagFetch — là cải thiện |
| 5 | Chưa tận dụng Base | ✅ `BaseCrudController` (6 endpoint kế thừa, chỉ override hook thông báo) · `AbstractCrudService` · `@Searchable` · `ChungTuTemplate` · ghi sổ qua `GhiSoApi`. ⚠ chỗ kernel bị **nới** thì thiếu test → **M2** |
| 6 | Chưa tận dụng base FE | ✅ N/A — PR không chạm `client/` |
| 7 | Constant đặt sai chỗ | ✅ `HangSoKhaiBaoCptt` / `MaLoiKhaiBaoCptt` nằm ở `internal/model/`, đúng khuôn sub-module `phan_bo` đã ship; mọi `MSG_…` đều là hằng số có tên. ⚠ m4 (chuỗi trạng thái lặp lại) và M3 (3 mã không có nguồn) |

## Cổng đã chạy

| Cổng | Kết quả |
|---|---|
| `trace.sh` | `NOT-RUN` — không có thư mục spec cho PMKT-E-05853 |
| `msg.sh` | `NOT-RUN` như một cổng (chạy trên working tree sai nhánh); thay bằng đối chiếu tay trên head PR: **57/59 mã của BA đã dùng đúng nguyên văn**, 3 mã tự cấp (**M3**) |
| Version migration | ✅ đã chạy — kết quả **B1** |
| Quét nhánh remote giành số | ✅ đã chạy (`git ls-tree` trên mọi `origin/*`) |
| Compile-break do đổi chữ ký | ✅ `GhiSoRequest` giữ constructor 8 tham số cho 7 nơi gọi cũ; `DongThamChieuDto.cuaChuSoHuu` giữ overload 11 tham số; `ThamChieuChungTu.capNhatSnapshot` đổi chữ ký nhưng chỉ 1 nơi gọi (`ThamChieuChungTuService`) đã sửa kèm |
| Cổng cây commit | ✅ `git status --porcelain` rỗng |
| `./gradlew unitTest` | **NOT-RUN — chế độ nhanh** |
| `./gradlew build` / Testcontainers | **NOT-RUN — chế độ nhanh** (và Testcontainers bị cấm: không Docker) |

## BR đã đọc

- **Đã đọc:** BR41 (tham chiếu chéo — nền của thay đổi `tham_chieu_chung_tu`), BR29 (chính sách
  xoá — luồng `delete` xoá mềm cả cụm), BR19 (chống trùng).
- **Chưa đọc (ghi rõ để lượt sau bù):** BR6, BR7, BR8, BR16, BR28, BR43, BR46 — được diff nhắc
  tới trong javadoc nhưng không finding nào phụ thuộc nguyên văn của chúng.
- BR nội bộ màn (`BR00`…`BR11` của `SCR_*KhaiBaoChiPhiTraTruoc`) **không** phải BR chung; chưa
  đối chiếu từng luật vì đó là việc của `/verify-spec` sau khi có thư mục spec.

## Phần chưa đọc

Đọc **~30/115 file**, chọn theo thứ tự kernel → hợp đồng API → service nghiệp vụ → repository
native → test. Chưa đọc chi tiết:

- `service/business/`: `KiemTraKhaiBaoCptt` (467 dòng, 19 luật), `DiffThietLapPhanBo` (253),
  `TinhToanKhaiBaoCptt`, `KhaiBaoCpttTinhToan`, `PhamViSuaKhaiBao`, `KiemTraPhamViTaiKhoan`,
  `TraCuuTaiKhoanNgamDinh`, `KhaiBaoCpttMapper`, `ThietLapPhanBoMapper`, `DungCumKhaiBaoCptt`
  → đây là nơi ở của **luật nghiệp vụ BR01/BR04/BR07/BR08/BR09/BR11**; cần `/verify-spec` để
  chấm độ phủ, review này **không** khẳng định chúng đúng.
- 18 file test mới trong `chi_phi_tra_truoc/khai_bao/**` (đã ghi nhận có tồn tại, chưa đọc nội dung).
- `SoCaiDaNguonSchemaIntegrationTest`, `BangChungTuNguonTest`, `DinhKemBanHangBr02Test`.

## Lệnh đã chạy

```bash
gh pr view 145 --json …
git fetch origin develop 'refs/pull/145/head:refs/pmkt-review/pr145'
git merge-base origin/develop refs/pmkt-review/pr145
git diff --stat / --name-status c6cb948e 023c57b9
git ls-tree -r --name-only origin/develop src/main/resources/db/migration | sort -V | tail
for b in $(git branch -r); do git ls-tree -r --name-only $b … | grep -E "V111[0-9]__"; done
git rev-list --count c6cb948e..origin/develop
comm -12 <(git diff --name-only c6cb948e origin/develop|sort) <(git diff --name-only c6cb948e 023c57b9|sort)
git grep -l "chapNhanNoCoTrung" 023c57b9 -- src/test
git grep -ho "MSG_PMKT-E-05853_[0-9]*" 023c57b9 -- src/main/java | sort -u   # so với 6.messages.md
./docs/rules/br.sh 41 29 19
git status --porcelain
```

## Tài nguyên lượt này tạo

- Ref tạm `refs/pmkt-review/pr145` (chưa xoá — giữ để lượt review sau dùng lại; xoá bằng
  `git update-ref -d refs/pmkt-review/pr145`).
- Không tạo worktree, không checkout, không sửa nhánh nào của người dùng.
