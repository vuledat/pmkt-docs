# Review PR #146 — cell-app

`fix(danh-muc): tách TK dùng chung theo thông tư, chuẩn hoá trạng thái`

| | |
|---|---|
| **Chế độ** | **NHANH** — chỉ đọc + kiểm tĩnh bằng git. Không chạy test/build, không worktree, không baseline, không merge thử. |
| PR | https://github.com/ospgroupvn-pmkt/cell-app/pull/146 · tác giả `truongnq98` · OPEN, không draft |
| head | `dc8ae0cd2edc4638166a77214b5407dc63555e5f` |
| base | `origin/develop` = `c6cb948ecb67faf13c3c9e59edc321664522c7c1` |
| merge-base | `c6cb948…` — **trùng đúng `origin/develop`**, PR không tụt commit nào |
| Quy mô | 37 file · +1824 −148 · 24 commit · `mergeable: MERGEABLE` |
| Working tree | sạch (`git status --porcelain` = 0 dòng) |

## Phạm vi & vùng đóng băng

18/37 file nằm trong `cell-app/src/main/java/vn/vtt/pmkt/cell/master_data/**` — vùng đóng
băng theo CLAUDE.md, chặn cứng ở `.claude/settings.json`. **User đã cho phép review cả
phần này** (ngoại lệ "user yêu cầu trực tiếp"). Diff đọc qua `git diff`/`git show`, không
gỡ rule `deny`, không lấy kiến trúc `master_data` làm mẫu cho việc khác.

**Đã đọc**: toàn bộ 24 file main (3 migration SQL, 21 file Java), `.gitignore`,
`TenantMasterDataSeederRunner` (ngoài diff, để xác minh đường chạy).
**Chưa đọc**: 8 file test (chỉ kiểm `@Tag`), `db/seed/_gen_httk_theo_thong_tu.py` (149
dòng, generator một lần), 578 dòng `INSERT INTO tmp_httk` trong V1111 (dữ liệu thuần, đã
xem mẫu ~50 dòng đầu).

---

## Findings

### ⚠️ M1 — Major — V1111 khối ③ bị RLS chặn, và guard ⑥ mù đúng lỗi nó định bắt

**File:** `src/main/resources/db/migration/V1111__httk_dung_chung_theo_thong_tu.sql:67-71`
(UPDATE) và `:821-833` (guard).

**Nguồn / tiền lệ trong repo:** `V1032__tknd_va_cau_hinh_danh_so.sql:935-937` — *"Phải
`set_config('app.tenant_id')` từng vòng: … có FORCE ROW LEVEL SECURITY nên policy áp cả
với owner — không bind thì WITH CHECK chặn sạch, INSERT 0 dòng và KHÔNG báo lỗi"*, và
`:971` — *"Đếm bằng superuser view thì vướng RLS, nên dùng chính vòng bind như trên"*.

**Trigger:**
1. `V1__create_database.sql:12259` — `mst_thong_tu_tai_khoan_dung_chung FORCE ROW LEVEL SECURITY`
   (FORCE ⇒ áp cả owner).
2. `:31440` — `CREATE POLICY tenant_isolation … USING (tenant_id = fn_current_tenant())`,
   **không** `FOR UPDATE` ⇒ policy áp cho **mọi** lệnh, gồm `SELECT`.
3. `fn_current_tenant()` = `NULLIF(current_setting('app.tenant_id', true), '')::uuid`
   (`:345-349`) → trong phiên Flyway, `app.tenant_id` chưa set ⇒ **NULL** ⇒ `tenant_id = NULL`
   ⇒ không dòng nào qua policy.
4. V1111 **không** có `set_config` / `row_security = off` — cả file chỉ có
   `SET LOCAL lock_timeout` (`:32`).

**Actual vs expected:** khối ③ `UPDATE … SET so_hieu_tai_khoan = d.so_hieu_tai_khoan
WHERE … IS NULL` chạm **0 dòng** thay vì backfill toàn bộ bảng nối tenant. Guard ⑥ đếm
`SELECT count(*) … WHERE so_hieu_tai_khoan IS NULL` **trên cùng bảng, cùng phiên chưa
bind** nên cũng thấy 0 ⇒ `v_httk_tenant_null = 0` ⇒ **migration báo thành công**.

**Hậu quả:** cột `so_hieu_tai_khoan` trên `mst_thong_tu_tai_khoan_dung_chung` vẫn NULL cho
mọi tenant đã onboard; unique index `uq_mst_ttkdc_tenant_thong_tu_so_hieu` (`:806-808`)
lập trên cột toàn NULL nên **không ràng buộc gì** (NULL không xung đột trong unique
index). Đây đúng là kiểu hỏng âm thầm mà comment `:821-823` tuyên bố muốn chặn — thông
điệp lỗi *"nghi RLS chan UPDATE khoi 3"* sẽ không bao giờ in ra.

**Hướng sửa:** dùng lại khuôn `V1032:942-966` — `FOR r IN SELECT id FROM iam_tenant LOOP
PERFORM set_config('app.tenant_id', r.id::text, true); … END LOOP;` cho **cả** UPDATE lẫn
câu đếm của guard.

---

### ⚠️ M2 — Major — Seeder chuyển từ 1 câu set-based sang ~1.156 round-trip mỗi tenant mỗi lần khởi động

**File:** `src/main/java/vn/vtt/pmkt/cell/master_data/internal/TenantMasterDataSeeder.java:751-830`
(vòng lặp mới) — thay cho `seedThongTuTaiKhoanDungChung()` cũ (một `INSERT … SELECT` duy
nhất, bị xoá ở dòng `-806`).

**Nguồn:** `bon-lop.md` lỗi hay gặp #4 · `checklist-be.md §E` ("gọi repository/query bên
trong vòng lặp").

**Trigger — đường chạy cụ thể:** `TenantMasterDataSeederRunner implements ApplicationRunner`
(`:23`, `:36`) → `for (UUID tenantId : seeder.allTenantIds()) seeder.seedDefaults(tenantId)`
→ `seedHeThongTaiKhoanDungChung`. Chạy **mỗi lần khởi động cell**, cho **mọi tenant**.

**Actual vs expected:** vòng `for (Object[] row : rows)` lặp **578 dòng/tenant**, mỗi dòng
phát 2 native query (`insert … returning id` + `insert` bảng nối), cộng
`resolveTaiKhoanId` (query thứ 3) cho mọi dòng đã tồn tại — tức **từ lần khởi động thứ hai
trở đi, gần như toàn bộ 578 dòng đi đủ 3 query**. Trước PR: 578 insert + **1** câu
set-based cho toàn bộ ánh xạ.

**Hậu quả:** ~1.156–1.734 round-trip/tenant/lần boot. 10 tenant ⇒ ~12–17 nghìn query mỗi
lần khởi động, trên đường startup đồng bộ.

**Ghi nhận cho tác giả:** javadoc `:686-702` có lý do kỹ thuật thật — cha phải có bảng nối
trước khi con resolve cha theo đúng thông tư, và (số hiệu, tên) không phân biệt được hai
thông tư. Commit `43ed82d3` cho thấy N+1 đã được nêu ở vòng review trước. Nhưng ràng buộc
đó chỉ bắt buộc **thứ tự cha-trước-con**, không bắt buộc **per-row**: vẫn làm được 3 pass
set-based (insert toàn bộ tài khoản với `tai_khoan_tong_hop_id = NULL` → insert bảng nối
theo `(so_hieu, ma_thong_tu)` → `UPDATE` gán cha theo bảng nối), đúng cách V1111 tự làm ở
`:745-767`. Nếu giữ per-row thì nên nêu rõ trong PR là chấp nhận đánh đổi.

---

### ⚠️ M3 — Major — Chuỗi trạng thái và điều kiện SQL lặp lại dạng literal, trong khi hằng số dùng chung đã có

**Nguồn:** luật 1 (CLAUDE.md — "mọi số/chuỗi nghiệp vụ phải là constant có tên") ·
`bon-lop.md` lỗi #7 · `checklist-be.md §F` ("constant dùng ≥ 2 module → `shared-kernel`").

**Trigger:** điều kiện `not in ('NgungHoatDong','INACTIVE')` xuất hiện **8 lần nguyên văn**
ở 4 file thuộc 3 module khác nhau:

| File | Dòng |
|---|---|
| `cong_cu_dung_cu/phan_bo/internal/repository/TraCuuDanhMucQuery.java` | 57 |
| `hoa_don_mua/internal/service/HoaDonMuaService.java` | 1501, 1595 |
| `ke_toan_tong_hop/doi_tru_cong_no/internal/repository/TraCuuDanhMucDoiTruRepository.java` | 87, 120, 127, 232 |
| `cong_cu_dung_cu/ghi_tang/internal/repository/DanhMucGhiTangQuery.java` | 88 (biến thể có `coalesce`) |

Và literal Java:

| File:dòng | Code |
|---|---|
| `master_data/tai_khoan/entity/HeThongTaiKhoan.java:33` | `private String trangThai = "HoatDong";` |
| `master_data/doi_tuong_tap_hop_chi_phi/entity/DoiTuongTapHopChiPhi.java:27` | `private String trangThai = "HoatDong";` |
| `master_data/tai_khoan/service/TaiKhoanServiceImpl.java:407` | `… ? "NgungHoatDong" : "HoatDong"` |
| `master_data/…/DoiTuongTapHopChiPhiServiceImpl.java:165-172` | `List.of("HoatDong","ACTIVE")` / `List.of("NgungHoatDong","INACTIVE")` |
| `platform_iam/…/OnboardingCompletionServiceImpl.java:149` | `src.isTrangThai() ? "HoatDong" : "NgungHoatDong"` |

**Actual vs expected:** `master_data/internal/DanhMucSupport.java:25-26` đã có
`public static final String HOAT_DONG` và `:41-43` `statusToEnum(boolean)` làm **đúng** phép
ánh xạ mà `OnboardingCompletionServiceImpl:149` viết lại bằng literal — chính comment ngay
trên dòng đó nhắc *"Contract danh mục (DanhMucSupport.HOAT_DONG)"* rồi vẫn không dùng.
5 file trong `master_data` dùng được `DanhMucSupport` trực tiếp (đã có tiền lệ:
`CoCauToChucServiceImpl:130`, `CongTrinhServiceImpl:117`).

**Hậu quả:** đợt chuẩn hoá tiếp theo (bỏ hẳn legacy, hoặc thêm trạng thái thứ ba) phải sửa
tay ≥13 chỗ ở 6 module; sót một chỗ là lệch âm thầm — đúng loại bug PR này đang đi dọn.

**Lưu ý phạm vi:** `OnboardingCompletionServiceImpl` thuộc `platform_iam`, import
`master_data.internal.DanhMucSupport` sẽ **vi phạm ranh giới Modulith** — chỗ đó cần hằng
số riêng (hoặc đưa cặp giá trị lên `shared-kernel`), không phải import chéo. Chuỗi điều
kiện SQL dùng ở 3 module cũng thuộc diện `shared-kernel` theo `checklist-be §F`.
`DanhMucGhiTangQuery` đã có sẵn mẫu đúng: hằng số `DIEU_KIEN_TAI_KHOAN_HOAT_DONG` (`:45`).

---

### 🔸 m1 — Minor — Hai cách xử lý NULL khác nhau cho cùng một điều kiện

`DanhMucGhiTangQuery.java:88` viết `coalesce(goc.trang_thai, '') not in ('NgungHoatDong','INACTIVE')`,
7 chỗ còn lại (M3) viết `trang_thai not in (…)` trần. Trong SQL, `NULL not in (…)` → NULL →
dòng **bị loại**; bản `coalesce` thì **giữ**. Hai ngữ nghĩa ngược nhau cho cùng một ý
"không phải ngừng hoạt động". Cột đang `NOT NULL` nên chưa nổ, nhưng nếu một bảng danh mục
khác không có ràng buộc đó thì hai chỗ cho hai kết quả. Chọn một cách rồi dùng thống nhất
(gộp luôn vào hằng số của M3).

### 🔸 m2 — Minor — Đổi allowlist → denylist khiến giá trị rác được coi là "đang hoạt động"

Trước: `trang_thai = 'ACTIVE'` — chỉ giá trị biết trước mới lọt. Sau:
`not in ('NgungHoatDong','INACTIVE')` — **mọi** giá trị khác đều lọt, kể cả rác hoặc một
trạng thái thứ ba thêm sau này. `TaiKhoanServiceImpl.chuanHoaTrangThai` (`:398-408`) chặn
rác nhưng chỉ trên đường ghi qua API; đường seeder/migration/import không đi qua đó. Nếu
BR chỉ có đúng hai trạng thái (BR23.1) thì `in ('HoatDong','ACTIVE')` giữ được tính chặt
của bản cũ mà vẫn nhận cả hai bộ giá trị.

### 🔸 m3 — Minor — Guard ghim số tuyệt đối gắn chặt vào workbook

`V1111:829-831` ghim `578/235/206/137` và `159/135/88`; `V1113:41-44` ghim `47`. Fail-fast
là đúng hướng, nhưng các số này đến từ `Danh mục mặc định.xlsx` qua
`_gen_httk_theo_thong_tu.py`. Workbook đổi ⇒ migration đã merge **không được sửa** (checksum
Flyway) ⇒ phải ra migration mới. Comment `:817-820` có nhắc "chạy lại generator nếu workbook
đổi"; nên ghi thêm ràng buộc này vào tài liệu quy trình để người sau không sửa file cũ.

### 💬 n1 — Nit — Nới visibility chỉ để test gọi

`TaiKhoanServiceImpl.java:398` đổi `private static` → `static` (package-private) cho
`chuanHoaTrangThai`, phục vụ `TrangThaiChuanHoaTest`. Chấp nhận được, nhưng gọi qua API
công khai của service sẽ giữ được đóng gói.

### 💬 n2 — Nit — Commit message lẫn hai ngôn ngữ, phần lớn không theo `<type>(<scope>)`

24 commit: một số đúng chuẩn (`test(danh-muc): …`), phần lớn là câu tiếng Anh tự do
(`Fix preview off-by-one and missed ACTIVE-only account check`, `Renumber migrations
V1100-V1102 to V1111-V1113`). Luật 8 yêu cầu `<type>(<scope>): <mô tả>`. Nhánh
`bugfix/httk-theo-thong-tu` **đúng** chuẩn.

---

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ Không file Java mới; test mới đặt đúng cây `src/test/java/…`. `master_data` vốn là shape cũ đã đóng băng — không tính vào PR này. |
| 2 | Không đánh lại version migration | ✅ V1111–V1113 > max `V1110` của develop; nhánh đã tự renumber từ V1100–V1102 (commit `f8d15976`). ⚠ Xem ghi chú va chạm bên dưới. |
| 3 | Chưa test lại sau khi merge | ✅ **N/A** — `git rev-list --count c6cb948..origin/develop` = **0**; merge-base trùng đúng đầu develop. Không cần merge thử. |
| 4 | N+1 / chưa tối ưu | ⚠ **M2** |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ N/A — không controller/entity/repository **mới**. `DoiTuongTapHopChiPhiRepository extends JpaRepository` là code sẵn có, PR chỉ sửa JPQL trong đó. |
| 6 | Chưa tận dụng base FE | ✅ N/A — PR không chạm `client/`. |
| 7 | Constant đặt sai chỗ | ⚠ **M3** |

### Ghi chú lỗi #2 — va chạm số với `origin/feat/tscd` (không quy cho PR này)

`origin/feat/tscd` cũng giữ V1111/V1112/V1113 với **tên khác**. Kiểm ra:
`git merge-base --is-ancestor` ⇒ nhánh đó **chưa** merge, còn 24 commit riêng, commit cuối
`b0c864b8` ngày 2026-09-08. Nhưng blob của 3 file đó **trùng byte-for-byte** với
`V1104/V1105/V1106` đã có trên develop (PR #117 đã MERGED) — tức là bản cũ chưa rebase.
Khi `feat/tscd` merge develop, họ phải xoá 3 file trùng; nếu quên thì Flyway báo
*"Found more than one migration with version 1111"*. **Rủi ro nằm ở nhánh kia**, PR #146
đánh số đúng theo develop.

## Cổng đã chạy

| Cổng | Kết quả |
|---|---|
| `git status --porcelain` (cổng cây commit) | ✅ sạch, 0 dòng; không file `??` trong `src/` |
| Quét trùng số migration trên **mọi** remote branch | ✅ chạy — kết quả ở ghi chú lỗi #2 |
| Độ tụt so với nhánh đích (`git rev-list --count`) | ✅ 0 commit |
| `trace.sh` | `NOT-RUN` — không có thư mục spec nào trong `docs/doing/` khớp phạm vi PR (đã kiểm: không có spec httk / tài khoản / thông tư / trạng thái danh mục). Không đoán bừa một PYC. |
| `msg.sh` | `NOT-RUN` — cùng lý do; PR không thêm mã `MSG_PMKT-E-xxxxx_nnn` nào. |
| `./gradlew unitTest` | `NOT-RUN` — **chế độ nhanh** |
| Build / merge thử / baseline | `NOT-RUN` — chế độ nhanh; merge thử không cần (lỗi #3 = N/A) |

**Về test:** chỉ **2/8** file test mang `@Tag("unit")` (`DoiTuongTapHopChiPhiServiceImplBranchTest`,
`TrangThaiChuanHoaTest`) — tức chỉ hai file này vào làn `./gradlew unitTest`. Sáu file còn
lại là Integration (Testcontainers) nên **không chạy được trên máy này** (không có Docker,
theo CLAUDE.md) kể cả khi chuyển sang chế độ sâu. Phần lớn bằng chứng đúng-sai của PR —
đặc biệt hành vi seeder và kết quả migration — nằm ở nhóm test không kiểm chứng được ở đây.

## BR đã đối chiếu

Đọc **BR2, BR23, BR47** (chọn theo mã BR xuất hiện trong diff và theo phạm vi "danh mục —
dữ liệu mặc định"). Kết quả:

- **BR47.3** ✅ — *"Sửa/Xóa dữ liệu mặc định KHÔNG làm thay đổi dữ liệu đang có tại tenant;
  chỉ Thêm mới mới lan xuống"*. V1111 giữ nguyên dữ liệu tenant (quyết định D1) và V1113
  soft-delete bản chuẩn nhưng giữ 49 dòng của tenant cũ — **khớp đúng BR47.3**, không phải
  thiếu sót. Phần "Thêm mới lan xuống tenant" do seeder ở lần khởi động sau đảm nhiệm.
- **BR23.1** ✅ — trạng thái mặc định là "Hoạt động"; V1112 đổi `DEFAULT` hai bảng về
  `'HoatDong'`, entity đổi field default tương ứng.
- **BR2** ✅ — *"bản ghi không hoạt động luôn sắp xuống dưới cùng"*; JPQL DTCP
  `order by case when e.trangThai in ('NgungHoatDong','INACTIVE') then 1 else 0 end` giữ
  đúng quy tắc cho **cả hai** bộ giá trị (bản cũ chỉ bắt `'INACTIVE'` nên bản ghi mới lưu
  `NgungHoatDong` sẽ không bị đẩy xuống — PR sửa đúng chỗ này).

**Chưa đọc:** BR5 (combogrid — `TraCuuDanhMucQuery`/`TraCuuDanhMucDoiTruRepository` phục vụ
ô chọn, BR5 có quy tắc riêng về bản ghi Ngừng hoạt động trong combogrid, khác BR2), BR22/40
(danh mục dạng cây — cây tài khoản), BR29 (chính sách xóa — liên quan soft-delete V1113).

---

## Kết luận

# 🟠 REQUEST CHANGES

Ba finding mức Major: **M1** (RLS làm hỏng backfill và guard không bắt được), **M2** (N+1
trên đường khởi động), **M3** (literal trạng thái lặp ở 6 module). Minor: m1, m2, m3.
Nit: n1, n2.

M1 là finding đáng xử lý trước khi merge — nó làm một phần mục tiêu của chính migration
không đạt mà vẫn báo thành công.

Phần còn lại của PR có chất lượng cao: migration ghi rõ ruling và lý do giữ id, fail-fast
có chủ đích, quyết định giữ dữ liệu tenant khớp đúng BR47.3, và các sửa đường đọc bao được
cả hai bộ giá trị trạng thái.

⚠ **Chế độ nhanh — chưa chạy cổng test/build nào.** Không đủ căn cứ để APPROVE kể cả khi
các finding trên được sửa. Muốn chấm để merge, chạy lại với `sâu` — nhưng lưu ý 6/8 test
của PR cần Testcontainers nên vẫn không chạy được trên máy này.
