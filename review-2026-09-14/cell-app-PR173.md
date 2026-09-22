# Review — cell-app PR #173 · `feat(vai-tro): tầng định tài khoản theo vai trò xuyên thông tư`

| | |
|---|---|
| PR | https://github.com/ospgroupvn-pmkt/cell-app/pull/173 (OPEN, tác giả `truongnq98`) |
| **Base** | **`bugfix/httk-gop-tang-dung-chung`** (KHÔNG phải `develop`) — `acfe532c` |
| Head | `feat/tai-khoan-theo-vai-tro` — `557925ec` |
| Merge-base | `acfe532c` = đúng tip của base ⇒ nhánh **không tụt** so với base (0 commit behind) |
| Diff | +1334 / −60 · 26 file (12 main Java/SQL, 11 test, 1 package-info, 2 migration) |
| Chế độ | **NHANH** — chỉ đọc + kiểm tĩnh bằng `git`/`grep`. **KHÔNG** chạy `gradlew`/test/build, **KHÔNG** worktree, **KHÔNG** merge thử, **KHÔNG** sửa code, **KHÔNG** đăng comment lên PR. |
| Đối chiếu base | Mọi `git diff`/`git show` trong lượt này đều dùng `acfe532c..557925ec`, không dùng `develop`. |

> ⚠ PR này **stacked** trên nhánh `bugfix/httk-gop-tang-dung-chung` (PR #163), không nhắm `develop`.
> Mọi kết luận về số migration dưới đây tính theo `max` của **base thật**, không theo `develop`
> (`develop` max hiện là V1122 — nếu chấm nhầm theo develop sẽ bỏ sót Blocker B1).

---

## Kết luận

**REJECT** — 1 Blocker (B1), 4 Major (M1–M4).

- Blocker: **B1**
- Major: **M1 · M2 · M3 · M4**
- Cổng test/build **chưa chạy** (chế độ nhanh): `./gradlew unitTest`, `compileJava`, migration apply
  thật đều `NOT-RUN`. Kết luận này chỉ phủ phần đã đọc tĩnh.

| Mức | Số lượng |
|---|---|
| Blocker | 1 |
| Major | 4 |
| Minor | 5 |
| Nit | 3 |
| **Tổng** | **13** |

---

## Blocker

### B1 — Migration V1132/V1133 **thấp hơn** `max` của nhánh đích (V1134) ⇒ Flyway chặn boot

`src/main/resources/db/migration/V1132__vai_tro_tai_khoan_va_map.sql`,
`V1133__tknd_dung_chung_default_theo_vai_tro.sql`

- **Nguồn**: `bon-lop.md` lỗi #2 + `checklist-be.md §C` — "Mọi migration **A** (added) có số **>
  max của nhánh đích** … Trùng/nhỏ hơn → Blocker".
- **Đo được**:
  ```
  base  origin/bugfix/httk-gop-tang-dung-chung: … V1130, V1131, V1134   ⇒ max = 1134
  head  feat/tai-khoan-theo-vai-tro:            … V1131, V1132, V1133, V1134
  ```
  Base đã tự dời số của mình lên 1134 (`1efd2322` 2026-09-13 `fix(migration): doi so V1132 thanh
  V1134, tranh trung nhanh khac`) **sau khi** PR này renumber xuống 1132/1133 (`68baa0c5`
  2026-09-12) — nên hiện trạng là PR chèn hai số **vào khoảng trống dưới** một migration đã có ở base.
- **Cơ chế hỏng**: `src/main/resources/application.yml:46` → `out-of-order:
  ${SPRING_FLYWAY_OUT_OF_ORDER:false}` (mặc định **false** ở mọi profile trừ `local`). Chính PR body
  ra lệnh "Thứ tự deploy **CỨNG**: #163 PHẢI merge/deploy TRƯỚC" ⇒ môi trường sẽ apply tới **V1134**
  trước, rồi mới nhận V1132/V1133 ⇒ Flyway `validate` fail *"Detected resolved migration not applied
  to database"* ⇒ **app không boot**.
- **Hậu quả**: chặn khởi động service ở đúng môi trường mà PR body yêu cầu deploy theo thứ tự đó.
- **Fix**: `git mv` V1132→V1135, V1133→V1136 (giữ nguyên nội dung), và **kiểm lại `max` một lần nữa
  ngay trước lúc merge** — dải 1129–1134 đang bị nhiều nhánh giành (`origin/bugfix/bug-sheet-he-thong-be`
  giữ một `V1131__cap_nhat_mo_ta_thong_tu.sql` **khác nội dung** với `V1131__lan_toa_bao_loi_khi_khong_thay_thong_tu.sql`
  của base — va chạm sẵn có, ngoài phạm vi PR này nhưng sẽ nổ khi hai nhánh gặp nhau).

---

## Major

### M1 — TT133 reroute `641 → 642` là nghiệp vụ **không có nguồn** (BA nói "lọc bỏ", không nói "đổi")

`ke_toan_tong_hop/internal/service/ButToanKetChuyenSeeder.java:105-127`

- **Nguồn**: `pmkt-docs/ba/PMKT-E-14031_KhaiBaoButToanKetChuyen/5.screens/SCR_KhaiBaoButToanKetChuyen/SCR_KhaiBaoButToanKetChuyen_ThemMoi.md:99`
  — "Tùy thuộc chế độ kế toán của Tenant (TT99 hoặc TT133) … mà hệ thống **lọc bỏ** các tài khoản
  không tồn tại."
- **Trigger**: onboard tenant chế độ TT133.
- **Expected (BA)**: dòng #6 (`641→911`) bị **lọc bỏ**. **Actual (PR)**: `map_vai_tro_thong_tu` seed
  `CP_BAN_HANG/TT133 = '642'` ⇒ dòng #6 được seed thành `642→911`.
- **Hậu quả**: tenant TT133 có thêm một bút toán kết chuyển mà tài liệu không yêu cầu; sai thì chỉ lộ
  lúc kết chuyển cuối kỳ. Đây đúng mục Lớp A "Nghiệp vụ tự bịa" + luật 9 (không tự quyết nghiệp vụ).
- Cùng họ: whitelist CCDC TT133 đổi `{242,642}` → `{242,642,154}` — PR body tự khai **đang chờ BA**
  xác nhận "154 là nguồn ghi tăng CCDC TT133", nhưng code đã LIVE hành vi đó.
- **Fix**: chốt BA trước khi merge; nếu BA giữ "lọc bỏ" thì bỏ dòng `CP_BAN_HANG/TT133` khỏi map.

### M2 — Tái dùng mã message `MSG_PMKT-E-05897_010` **đã được BA gán cho việc khác**

`cst_gia_thanh/cau_hinh/internal/constant/MaLoiCauHinhGiaThanh.java:72-75`

- **Nguồn**: `pmkt-docs/ba/PMKT-E-05897_CauHinhGiaThanh/6.messages.md:16` —
  `MSG_PMKT-E-05897_010 | Lỗi khi xóa dòng cấu hình | "Xóa dòng cấu hình không thành công. Vui lòng
  thử lại."` (được `SCR_CauHinhGiaThanh_SuaCauHinh.md:171` tham chiếu cho hành động **Xóa dòng**).
- **Actual**: PR gán `_010` cho `VAI_TRO_CHUA_ANH_XA` với văn bản *"Vai trò tài khoản … chưa được ánh
  xạ số hiệu cho chế độ kế toán hiện tại…"* (`GiaTriMacDinhGiaThanh.java:124-128`). Comment trong
  code ghi "mã RIÊNG" — nhưng `_010` **không** còn trống (BA đã dùng tới `_010`).
- **Hậu quả**: một mã message trỏ hai nội dung khác nhau — `msg.sh` sẽ chấm `LECH`, FE map i18n sai,
  telemetry theo mã lỗi trộn hai ca.
- **Fix**: xin BA mint mã mới (`_011`…) rồi cập nhật `6.messages.md`; không tự chọn số.

### M3 — TT133: bút toán sống sót mang **tên sai** ("Kết chuyển chi phí bán hàng" cho TK 642)

`ButToanKetChuyenSeeder.java:83-89` + `:121-127`

- **Trigger**: tenant TT133 — `CP_BAN_HANG` và `CP_QLDN` **cùng** map ra `642`.
- **Cơ chế**: vòng lặp seed theo thứ tự mảng; dòng #6 chèn trước với `ten = "Kết chuyển chi phí bán
  hàng"`, `thu_tu_ket_chuyen = 6`. Dòng #7 ("Kết chuyển chi phí quản lý doanh nghiệp") bị `not exists
  (e.ket_chuyen_tu_id = tu.id and e.ket_chuyen_den_id = den.id)` loại.
- **Actual vs expected**: tenant TT133 thấy tên bút toán "chi phí bán hàng" trên tài khoản 642 (ở
  TT133 là *chi phí quản lý kinh doanh*). Người thắng được chọn theo **thứ tự mảng Java**, không theo
  quy tắc nghiệp vụ nào.
- **Hậu quả**: nhãn sai trên màn khai báo bút toán kết chuyển của mọi tenant TT133 mới.
- **Fix**: BA chốt tên + thứ tự cho TT133; nếu giữ reroute thì phải chọn survivor tường minh, không
  dựa vào thứ tự khai báo.

### M4 — TKND: `tai_khoan_mac_dinh` chuyển sang vai trò nhưng `loc_tai_khoan` vẫn là uuid COA-global cũ

`master_data/tai_khoan_ngam_dinh/internal/repository/SeedTaiKhoanNgamDinhRepository.java`
(`SQL_MOT_TAI_KHOAN` sửa · `SQL_PHAM_VI_LOC` **không** sửa)

- **Hợp đồng bị chạm**: bất biến "TK ngầm định phải nằm trong bộ lọc của chính dòng đó", đang được
  ghim bởi `SeedTaiKhoanNgamDinhIntegrationTest#tk_ngam_dinh_nam_trong_bo_loc_cua_chinh_dong_do:140`
  (`assertThat(locTaiKhoan(...)).contains(ngam)`) — nhưng test đó **chỉ chạy trên fixture TT200**.
- **Trigger**: tenant TT133, dòng bộ chuẩn thuộc phạm vi vai trò (vd `CP_NVL_TT`).
- **Actual**: vế ưu tiên 1 (mới) resolve default theo thông tư tenant ⇒ ra `154`. `SQL_PHAM_VI_LOC`
  vẫn expand `ct.loc_tai_khoan` (uuid trỏ `mst_he_thong_tai_khoan_dung_chung`, ghim TT200 — PR body
  tự khai "mọi dòng template ghim TT200") ⇒ với COA TT133, `like '621%'` không khớp gì ⇒ **bộ lọc
  rỗng**.
- **Expected**: default ∈ bộ lọc của dòng. **Hậu quả**: popup chọn tài khoản mở ra **rỗng** trong khi
  ô đã có sẵn giá trị `154` — người dùng không sửa lại được, và bất biến trên bị phá âm thầm. Trước
  PR thì cả hai cùng rỗng (nhất quán); sau PR mới sinh trạng thái lệch.
- **Fix**: đưa `loc_tai_khoan` qua cùng tầng vai trò, hoặc chốt với BA rằng dòng vai trò ở TT133 được
  phép có default ngoài bộ lọc. Không có test nào trong PR phủ ca này (`SeedTkndTheoVaiTroIntegrationTest`
  dựng fixture `loc_tai_khoan = NULL`).

---

## Minor

- **m1** — `kho/api/NguonGhiTangCcdcApi.java:78` `DAU_TAI_KHOAN_GHI_TANG` giữ **nguyên tên** nhưng
  nội dung đổi từ số hiệu (`"242","641"…`) sang **mã vai trò**. Tên nằm trong `api/` (hợp đồng liên
  module) mà nghĩa đã khác hẳn → dễ dùng nhầm như prefix tài khoản. Đổi tên thành
  `VAI_TRO_NGUON_GHI_TANG`. (Đã kiểm: chưa caller nào ngoài `kho` dùng ⇒ chưa gãy compile.)
- **m2** — `arch/ProxyModularityTest.java:141-152` `vaiTroTaiKhoanKhongCoViPhamRanhGioiNao` là test
  **rỗng theo cấu trúc**: module `vai_tro_tai_khoan` không còn class Java nào ngoài `package-info`
  (package-info tự thừa nhận điều này), nên test xanh vì "không có gì để vi phạm". Javadoc của test
  còn nói "Task 1 chỉ thêm migration + **repository nội bộ**" — repository đó đã bị xoá ⇒ javadoc sai
  hiện trạng.
- **m3** — Phụ thuộc xuyên module đi bằng **SQL JOIN** thay vì `api/`: `master_data`,
  `ke_toan_tong_hop`, `cst_gia_thanh`, `kho` đều JOIN thẳng `map_vai_tro_thong_tu` (bảng của
  `vai_tro_tai_khoan`) **và** `iam_tenant` (bảng của `platform_iam`). Modulith không quan sát được
  cạnh này ⇒ `ProxyModularityTest` xanh giả. Có ADR
  (`dev-plan/truongnq/doing/httk-gop-tang-dung-chung/04-adr-sql-join-xuyen-module.md`) nên không nâng
  lên Major, nhưng cần tech-lead ký nhận trước khi nhân rộng idiom này ra module khác.
- **m4** — Hai ô map seed **giá trị đoán trong khi chờ BA**: `CP_THUE_TNDN/TT133='821'` và
  `CP_MAY_THI_CONG/TT133='154'` (`V1132`:75, :86). Luật 9 yêu cầu dừng và hỏi, không seed mặc định rồi
  sửa sau — nhất là khi sửa lại phải bằng migration mới (không được sửa V1132 sau merge).
- **m5** — Chạm **vùng đóng băng** `cell/master_data/tai_khoan_ngam_dinh/**` (1 file main + 3 file
  test). PR body có khai báo ngoại lệ "được user cấp". Cần user/lead xác nhận lại trên PR, vì
  CLAUDE.md gốc coi đây là ngoại lệ **một lần, có xin phép**, không phải quyền thường trực.

## Nit

- **n1** — Test mới dùng literal `"CP_NVL_TT"` / `"GIAM_TRU_DT"`
  (`GiaTriMacDinhGiaThanhTest.java:167,183,198`, `SeedTkndTheoVaiTroIntegrationTest.java:46`) trong khi
  đã có `MaVaiTroTaiKhoan` — đúng thứ mà chính javadoc của hằng đó nói là muốn tránh.
- **n2** — `SeedTaiKhoanNgamDinhRepository.java` javadoc nhắc *"(review PR173)"*: tham chiếu vòng đời
  review vào code sản phẩm, sẽ vô nghĩa sau khi merge.
- **n3** — PR body vẫn mô tả migration là **V1129/V1130** ở nhiều chỗ (TL;DR, Risks) trong khi file
  thực tế là V1132/V1133 — người đọc đối chiếu số sẽ lạc; và nếu fix B1 thì phải cập nhật lần nữa.

---

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục Modulith | ✅ Đạt — file main mới đều ở `internal/…` đúng ngăn (`repository/`, `service/business/`, `constant/`); module mới `vai_tro_tai_khoan` có `package-info.java` khai `@ApplicationModule`; không tạo `api/` "cho chắc"; base package `vn.vtt.pmkt` đúng. `MaVaiTroTaiKhoan` đặt ở `common` — module `Type.OPEN` (đã kiểm `common/package-info.java`) nên hợp lệ. Xem **m3** cho phần ranh giới đi bằng SQL. |
| 2 | Không đánh lại version migration | ❌ **Blocker B1** |
| 3 | Chưa test lại sau khi merge nhánh đích | ✅ N/A — `git rev-list --count 557925ec..origin/bugfix/httk-gop-tang-dung-chung` = **0** (nhánh đã ôm trọn base, merge-base = tip base) ⇒ không có file giao nhau để xét. |
| 4 | N+1 / chưa tối ưu | ✅ Đạt trong phạm vi đọc — `SQL_MOT_TAI_KHOAN` là subquery tương quan trong **một** câu `INSERT…SELECT` (không phải N lượt JDBC); `ButToanKetChuyenSeeder` lặp **11 lần cố định** (đúng như trước PR); `soHieuTheoVaiTro` của CCDC là **1** query thêm mỗi request popup, có early-return khi rỗng. Không tìm được đường chạy sinh N truy vấn. |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ N/A — PR không thêm Controller/Entity/Repository JPA mới; toàn bộ là native SQL trong repository sẵn có + seeder. Không có CRUD tự viết. |
| 6 | Chưa tận dụng base FE | ✅ N/A — 0 file `client/`. |
| 7 | Constant đặt sai chỗ | ⚠ Một phần — `MaVaiTroTaiKhoan` gom đúng vào `common/constant/` (dùng ≥ 2 module, `common` là OPEN) ✅; mã message thì **sai giá trị**, xem **M2**; hằng `DAU_TAI_KHOAN_GHI_TANG` sai nghĩa tên, xem **m1**. |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ⚠ 1 mục: "Nghiệp vụ tự bịa" → **M1** (+ **m4** seed giá trị chờ BA). Không có secret trong diff; không có Controller chạm Repository / trả Entity; không `try/catch` nuốt lỗi (lỗi ném qua `ApiException` cho `@RestControllerAdvice`); không field injection mới; chạm vùng đóng băng có khai báo → **m5**. |
| B — Kiến trúc & 7 lỗi | Xem bảng trên: **B1**, **m1**, **m2**, **m3**. |
| C — Nghiệp vụ & truy vết | ⚠ **M1**, **M2**, **M3**, **M4**. `trace.sh` / `msg.sh`: **NOT-RUN** — không có thư mục `docs/doing/<slug>-spec` cho việc này, và diff trải trên **4 epic** (`PMKT-E-14031` kết chuyển · `PMKT-E-05897` giá thành · CCDC/`kho` · TKND `master_data`) nên không có một thư mục PYC đơn để truyền vào. Đối chiếu nghiệp vụ vì vậy làm tay, trực tiếp trên tài liệu BA (xem nguồn trích ở M1/M2). |
| D — Vệ sinh diff & Git | ✅ chủ yếu đạt — commit message đúng `<type>(<scope>): <mô tả>`, nhánh `feat/tai-khoan-theo-vai-tro` đúng dạng; không commit thẳng `develop`; không có TODO trần; migration đổi số bằng `git mv` (lịch sử `68baa0c5` giữ nguyên nội dung). Cổng cây commit: mọi file mới đã tracked ở head (đọc được bằng `git show`), không còn `??` trong `src/`. Nit **n2**, **n3**. |

## BR đã đọc / chưa đọc

- **Đọc**: BA epic `PMKT-E-14031` (`SCR_KhaiBaoButToanKetChuyen_ThemMoi.md` bảng 11 bút toán + ghi
  chú lọc theo chế độ kế toán) · BA epic `PMKT-E-05897` (`6.messages.md`,
  `SCR_CauHinhGiaThanh_SuaCauHinh.md` — bảng mã message).
- **Chưa đọc** (không chặn kết luận, ghi để minh bạch): `business_rules.md` BR5/BR6/BR7 bản chung —
  diff không mang mã `BR` chung nào; các `BR…` xuất hiện trong code là **BR nội bộ màn** của hai epic
  trên, đã tra thẳng tại file SCR tương ứng. Tài liệu §3 nguồn ghi tăng CCDC và
  `cau-hoi-ba/PMKT-E-05897_CauHinhGiaThanh.md` chưa mở.

## Lệnh đã chạy

```
gh pr view 173 --json …
git fetch origin; git rev-parse / merge-base origin/bugfix/httk-gop-tang-dung-chung origin/feat/tai-khoan-theo-vai-tro
git diff --stat / --name-status acfe532c..557925ec
git ls-tree -r --name-only <base|head> -- src/main/resources/db/migration      # đo max migration
for b in $(git branch -r …); git ls-tree … | grep -E "V113[0-9]__"            # quét va chạm số
git show 557925ec:<path>  (migration, package-info, repository, seeder, test)
git diff acfe532c..557925ec -- <từng nhóm file>
git grep -n "<symbol>" 557925ec -- src                                        # soát compile-break
git rev-list --count 557925ec..origin/bugfix/httk-gop-tang-dung-chung         # = 0
grep -rn "PMKT-E-05897_0…" pmkt-docs/ba --exclude-dir=Phase_2                 # đối chiếu mã message
```

## Phần CHƯA kiểm

- **Cổng test/build: NOT-RUN — chế độ nhanh.** `./gradlew unitTest`, `compileJava`, và lượt apply
  migration thật đều chưa chạy. 2 test unit mới (`NguonGhiTangCcdcAdapterTest`,
  `GiaTriMacDinhGiaThanhTest`) có `@Tag("unit")` ⇒ vào được làn `unitTest`; 5 test còn lại
  (`SeedTkndTheoVaiTroIntegrationTest`, `SeedGiaThanhTheoVaiTroIntegrationTest`,
  `NguonGhiTangCcdcTheoVaiTroTest`, `MapVaiTroThongTuIntegrationTest`, `CauHinhGiaThanhControllerIT`)
  là **Testcontainers ⇒ không chạy được trên máy này** (cấm Docker).
- `trace.sh` / `msg.sh`: NOT-RUN, lý do ở Lớp C.
- File chưa đọc chi tiết (chỉ liếc qua `--stat`/tên): `CoaFixture.java`,
  `TenantConfigServiceIntegrationTest.java`, `CauHinhGiaThanhServiceTaoBanGhiMacDinhTest.java`,
  `MapVaiTroThongTuIntegrationTest.java`, `SeedGiaThanhTheoVaiTroIntegrationTest.java` — đều là
  fixture/test, không đổi hành vi sản phẩm.
- Không đăng comment lên PR (theo yêu cầu của lượt này).
