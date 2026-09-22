# Review — cell-app PR #129 (Cấu hình giá thành + Kỳ tính giá thành)

**Chế độ: NHANH** — chỉ đọc + kiểm tĩnh bằng git/grep. KHÔNG chạy `unitTest`, KHÔNG build,
KHÔNG worktree, KHÔNG merge thử, KHÔNG đo baseline.

## 1. Phạm vi

| Mục | Giá trị |
|---|---|
| PR | https://github.com/ospgroupvn-pmkt/cell-app/pull/129 |
| Head | `d439a6cf` (nhánh `feat/logic-cau-hinh-gia-thanh`) — lấy qua `refs/pull/129/head` |
| Base | `origin/develop` `332e9769` — **giả định**, không có `gh` CLI để đọc metadata PR; xác minh bằng merge-base nhỏ nhất (8 commit / 59 file) so với các ứng viên khác |
| Merge-base | `622dd2d9` |
| Diff | 59 file, +4852 / −4 (47 file `src/main`, 12 file test) |
| Working tree | sạch (`git status --porcelain` rỗng); tree đang ở nhánh khác (`feat/chung-tu-ban-hang-2`) |
| Vùng đóng băng | không có file nào thuộc `master_data/**`, `legacy/**`, `Phase_2/**` |
| Epic | PMKT-E-05897 (Cấu hình giá thành) + PMKT-E-05908 (Kỳ tính giá thành) |

Commit: 8 (2 merge, 4 `feat`, 1 `fix`, 1 `refactor`).

---

## 2. Findings

### B1 — Blocker · Migration `V1099` đụng số ba chiều, Flyway vỡ ngay khi merge

- **File**: `src/main/resources/db/migration/V1099__cst_ky_tinh_gt_unique_theo_phuong_phap.sql`
- **Nguồn**: CLAUDE.md §"Không đánh lại version migration"; Flyway `DuplicateMigrationVersion`
- **Bằng chứng**:
  ```
  origin/develop : V1099__cash_map_vat_tu_id.sql          (10c4cd2a "Fix bug phiếu kiêm #124")
                   V1099__ktth_btcn_chi_nhanh_theo_v1097.sql (284752b8 "Sổ công nợ Phase 1 #120")
  PR #129        : V1099__cst_ky_tinh_gt_unique_theo_phuong_phap.sql
  ```
  Cả hai file V1099 trên develop đều được thêm **sau** merge-base → nhánh này chưa thấy chúng.
- **Trigger**: merge PR vào develop → Flyway `validate/migrate` gặp 3 file cùng version 1099.
- **Actual vs expected**: app không boot (`Found more than one migration with version 1099`) /
  version phải > `max` của nhánh đích.
- **Hậu quả**: chặn mọi deploy trên develop.
- **Kèm theo (không phải lỗi của PR này, nhưng phải xử lý cùng)**: `origin/develop` **đã tự vỡ**
  với 2 file V1099 do #120 và #124 cùng lấy số. Đánh lại số cho PR này phải tính cả việc dọn 2 file
  đó — đề xuất PR dùng `V1101`/`V1102`.
- **Nhánh khác đang giành cùng số**: `origin/feat/logic-do-dang-dau-ky` mang **y hệt** cặp
  `V1099__cst_ky_tinh_gt…` + `V1100__cst_cau_hinh_gia_thanh…` (nhánh con của nhánh này) — đổi số
  phải đồng bộ cả hai.

### B2 — Blocker · BR7.3 "đồng bộ Tài khoản kết chuyển chéo yếu tố" không bao giờ chạy

- **File**: `cst_gia_thanh/cau_hinh/internal/service/CauHinhGiaThanhService.java:171`
- **Nguồn**: `SCR_CauHinhGiaThanh_SuaCauHinh.md` BR7.3 (dòng 126–132) — "sửa `Tài khoản kết chuyển`
  ở màn hình của bất kỳ yếu tố chi phí nào, giá trị mới được áp dụng cho toàn bộ các yếu tố còn lại
  của cùng phương pháp tính, trong cùng một giao dịch".
- **Cơ chế**: `hienTai` và `canGhi` **dùng chung đối tượng entity** (`theoId` được dựng từ chính
  `hienTai`). Vòng ghi ở dòng 152–167 đã gán giá trị mới:
  ```java
  entity.setTaiKhoanKetChuyenId(request.taiKhoanKetChuyenId());   // dòng 164 — sửa luôn phần tử của hienTai
  ...
  UUID taiKhoanKetChuyenCu = hienTai.get(0).getTaiKhoanKetChuyenId();  // dòng 171 — đã là giá trị MỚI
  if (!request.taiKhoanKetChuyenId().equals(taiKhoanKetChuyenCu)) {    // dòng 172 — luôn false
  ```
- **Trigger**: mở yếu tố Nhân công, giữ nguyên các dòng cũ, chỉ đổi `Tài khoản kết chuyển`
  154 → 1541, bấm Lưu.
- **Actual vs expected**: chỉ nhóm Nhân công đổi sang 1541; NVL và SXC vẫn giữ 154 / cả 3 yếu tố
  phải là 1541.
- **Hậu quả**: vi phạm bất biến BR7.1 ngay trên luồng chính. Theo BR7.2, chi phí dở dang nằm rải ở
  nhiều đầu tài khoản → nhập kho thành phẩm tách sai dòng hạch toán. Lỗi im lặng: API vẫn trả 200.
- **Chỉ chạy đúng** khi `hienTai.get(0)` là dòng **bị xoá** trong lần lưu đó (không nằm trong
  `dong[]`) — trường hợp hiếm, nên bug ẩn.
- **Test đã viết nhưng chưa từng chạy**: `CauHinhGiaThanhControllerIT#luu_doiTkKetChuyen_dongBoCa3YeuTo`
  (Testcontainers — máy cấm Docker) phủ đúng kịch bản này và sẽ **đỏ**.
- **Sửa**: đọc `taiKhoanKetChuyenCu` **trước** vòng ghi (ngay sau khi `hienTai` được load).

### B3 — Blocker · Hai sub-module lệch chuỗi `PhuongPhapTinh` → cột "Phát sinh trong kỳ" luôn 0

- **File**: `ky_tinh_gia_thanh/internal/repository/KyTinhGiaThanhAggregateRepository.java:119`
  ↔ `cau_hinh/internal/model/PhuongPhapTinh.java:21`
- **Nguồn**: BR2 `SCR_KyTinhGiaThanh_DanhSach` (cột Phát sinh trong kỳ); CHECK constraint
  `V1__create_database.sql:6710` và `:7084`.
- **Bằng chứng**:
  | Enum | Giá trị `HE_SO_TY_LE` | Bảng đích |
  |---|---|---|
  | `cau_hinh.PhuongPhapTinh` | `"Hệ số, tỷ lệ"` (**có dấu phẩy**) | `cst_cau_hinh_gia_thanh` |
  | `ky_tinh_gia_thanh.PhuongPhapTinh` | `"Hệ số tỷ lệ"` (**không dấu phẩy**) | `cst_ky_tinh_gia_thanh` |

  `SQL_PHAT_SINH_TRONG_KY` lọc `cst_cau_hinh_gia_thanh.phuong_phap_tinh = :ppConfig` nhưng truyền
  `ky.phuongPhapTinh().giaTri()` — tức chuỗi của bảng **kỳ tính**.
- **Trigger**: mở màn Danh sách kỳ tính giá thành route `/api/cst-gia-thanh/he-so-ty-le/ky-tinh-gia-thanh`.
- **Actual vs expected**: subquery tài khoản rỗng → `SUM = 0` cho mọi kỳ / phải bằng tổng phát sinh
  Nợ−Có của các TK tập hợp chi phí đã cấu hình. Route "Trực tiếp" không bị (chuỗi trùng nhau).
- **Hậu quả**: số liệu sai im lặng trên màn danh sách của cả một phương pháp tính.
- **Chính javadoc của file này (dòng 35–42) đã cảnh báo phải sửa "trước/khi merge" hai nhánh** —
  PR #129 **chính là** lượt merge đó, và fix chưa được áp dụng.
- **Không test nào bắt được**: `KyTinhGiaThanhCrudServiceTest#search_ghep_dung_theo_tung_ky` mock
  `aggregateRepository`, không chạm SQL.

### M1 — Major · Toàn bộ luận cứ thiết kế trỏ tới tài liệu không tồn tại trong repo

- **File**: rải khắp (`00-ke-hoach-tong.md` được nhắc ở ~40 file), ví dụ
  `CauHinhGiaThanhService.java:28`, `KyTinhGiaThanhCrudService.java:238`.
- **Bằng chứng**:
  - Không có `docs/doing/PMKT-E-05897-*` hay `PMKT-E-05908-*` (đã `find`).
  - Không có `dev-plan/` trong repo — `KyTinhGiaThanhCrudService.java:238` trỏ tới
    `dev-plan/anpq/doing/PMKT-E-05908-ky-tinh-gia-thanh-api/00-ke-hoach-tong.md`.
  - Không có `cau-hoi-ba/PMKT-E-05897_CauHinhGiaThanh.md` (Q1…Q7).
  - Không có `docs/doing/<slug>-spec/` cho cả 2 epic → **cổng đặc tả `/audit-spec` chưa từng chạy**.
- **Hậu quả**: mọi quyết định D1–D17 và câu hỏi mở Q1–Q7 (kể cả các mục làm sai lệch BR — xem M2, M3)
  **không kiểm chứng được**. Reviewer buộc phải tin javadoc. Vi phạm CLAUDE.md §Cổng đặc tả luật 3
  (báo hoàn thành phải kèm bảng truy vết Rule → Code → Test).
- **Kèm theo — javadoc trỏ migration không tồn tại**: `KyTinhGiaThanhAggregateRepository.java:29,117`
  và `KyTinhGiaThanh.java:19` viện dẫn `V1050` (fix chuỗi phương pháp tính) và
  `V1051__cst_bo_chi_nhanh_id_ky_tinh_gia_thanh.sql`. Ở head, `V1050`/`V1051` là
  `inv_pndc_them_cot_nguoi_van_chuyen` / `inv_pndc_quyen_create_va_chuan_hoa_loai_phieu` — **không
  liên quan**. Đây chính là gốc của B3: giả định "V1050 đã sửa chuỗi" là **sai**.

### M2 — Major · BR7.1 / BR46.4 bị thu hẹp bỏ `ChiNhanhId`, lý do hoãn đã lỗi thời

- **File**: `CauHinhGiaThanh.java:37-44`, `CauHinhGiaThanhService.java:41-46`,
  `CauHinhGiaThanhRepository.java:18-21`, `V1100__…sql` (khối "LỊCH SỬ chi_nhanh_id").
- **Nguồn**: BR7.1 `SCR_CauHinhGiaThanh_SuaCauHinh.md:118` — bất biến theo
  `(TenantId, ChiNhanhId, PhuongPhapTinh)`; BR46.4 `business_rules.md` — `ChiNhanhId` là trường xác
  định phạm vi dữ liệu khai trực tiếp trên entity, "bắt buộc lọc khi truy vấn".
- **Actual vs expected**: nhóm/unique/finder chạy phạm vi `(Tenant, PhuongPhapTinh)` / phải có
  `ChiNhanhId`.
- **Lý do hoãn ghi trong code (D15, 2026-09-02)**: "app chưa có `ChiNhanhSwitcher`/`ChiNhanhContext`
  toàn cục". **Tiền đề này không còn đúng ở head**: `core/shared/tenant/TenantContext.java:122` đã có
  `chiNhanhId()`, `V1097__chi_nhanh_nen_tang_don_vi_user_chi_tiet.sql` đã ở develop, và 148 file
  `src/main` đang dùng `chiNhanhId`.
- **Hậu quả**: một quyết định nghiệp vụ (đảo ngược điều BA đã xác nhận trực tiếp — chính javadoc thừa
  nhận "BA xác nhận trực tiếp ChiNhanhId là bắt buộc") do dev tự chốt vì "lý do sản phẩm" → luật 9
  CLAUDE.md. Bản ghi quyết định D14/D15 không có trong repo (M1) nên không ai kiểm được BA đã đồng ý
  hoãn hay chưa.
- **Đề nghị**: BA/PO xác nhận bằng văn bản việc hoãn, ghi vào `01-conflict.md`, hoặc bổ sung
  `chiNhanhId` vì hạ tầng đã sẵn sàng.

### M3 — Major · `messageId` dùng sai ngữ cảnh so với `6.messages.md`

- **File**: `cau_hinh/internal/model/MaLoiCauHinhGiaThanh.java:56,59,30`;
  `CauHinhGiaThanhValidator.java:84-85`
- **Nguồn**: `pmkt-docs/ba/PMKT-E-05897_CauHinhGiaThanh/6.messages.md`

  | messageId | Nội dung theo BA | Code dùng cho |
  |---|---|---|
  | `_009` | "Lưu dòng cấu hình không thành công. Vui lòng thử lại." | TK tập hợp không tồn tại / không cấp cuối (V7) |
  | `_006` | "Tài khoản kết chuyển là bắt buộc…" | **hai** ca: thiếu TK kết chuyển (V4) **và** TK kết chuyển không cấp cuối (V8) |
  | `_003` | "Không thể tải thông tin cấu hình giá thành…" | 404 "Không tìm thấy cấu hình giá thành" |
  | `_005` | "Tiêu thức phân bổ là bắt buộc…" | **hai** ca: thiếu tiêu thức (V4) **và** tiêu thức ngoài tập cho phép (V5) |

- **Hậu quả**: FE dịch theo `messageId` → người dùng chọn tài khoản cấp cha sẽ thấy "Tài khoản kết
  chuyển là bắt buộc" dù đã chọn; hai lỗi khác nhau không phân biệt được ở FE.
- Javadoc thừa nhận đây là "mã dùng TẠM, chờ Q5". Q5 vẫn mở → theo cổng đặc tả, phải chốt với BA
  (xin cấp `_011`, `_012`…) trước khi merge, không tự dùng lại mã sai ngữ cảnh.

### m1 — Minor · N+1: `existsBy…` gọi trong vòng lặp theo từng dòng request

`CauHinhGiaThanhValidator.java:106` — 1 query/dòng `dong[]`, số dòng do người dùng thêm. Gom thành
một truy vấn `… taiKhoanTapHopChiPhiId IN (:ids)` là đủ.

### m2 — Minor · N+1: `phatSinhTrongKy` chạy 1 query/dòng của trang

`KyTinhGiaThanhAggregateRepository.java:113` — trang 20 dòng ⇒ 20 lượt quét `acc_so_cai` kèm 2
subquery. Javadoc tự nhận "chấp nhận được ở Phase 1"; ghi nhận để không trôi sang Phase 2.

### m3 — Minor · Lưu với `dong[]` rỗng trả 404 sai bản chất

`CauHinhGiaThanhService.java:128,181` — mọi dòng bị xoá mềm, `timNhom` sau đó ném
`NOT_FOUND` "Không tìm thấy cấu hình giá thành cho yếu tố …" (transaction rollback nên không mất dữ
liệu). Nên chặn tường minh "phải còn ít nhất 1 dòng" ở validator thay vì để lộ 404 gây hiểu nhầm là
dữ liệu biến mất.

### m4 — Minor · `khoiPhucMacDinh` không kiểm `lockToken`

`CauHinhGiaThanhService.java:187` — `luuCauHinh` có khoá lạc quan cấp nhóm (D9) nhưng A3 thì không.
Hai người dùng đồng thời: một người Lưu, một người Khôi phục → ghi đè im lặng.

### m5 — Minor · `while (true)` đệ quy cây tài khoản không có chặn độ sâu

`GiaTriMacDinhGiaThanh.java:82-88` — dữ liệu `mst_he_thong_tai_khoan.tk_cha_id` tạo chu trình
(A→B→A) sẽ treo request vô hạn kèm query liên tục. Thêm giới hạn cấp (ví dụ 10) + ném lỗi rõ ràng.

### m6 — Minor · Hai thông báo trạng thái kỳ tính không có mã BA

`MaLoiKyTinhGiaThanh.MSG_CHI_SUA_KHI_CHUA_THUC_HIEN` / `MSG_KHONG_XOA_KHI_DA_HOAN_THANH` là chuỗi
tiếng Việt tự đặt, **không có** trong `6.messages.md` của PMKT-E-05908; hai lời gọi truyền
`messageId = null`. Tên hằng tiền tố `MSG_` trùng quy ước messageId của các hằng khác trong cùng lớp
→ dễ dùng nhầm. Cần BA cấp mã (hoặc đổi tên hằng thành `TEXT_…`).

### m7 — Minor · Prefix route lệch nhau giữa hai sub-module cùng module

`/api/gia-thanh/cau-hinh-gia-thanh` (+ `/api/gia-thanh/he-so-ty-le/cau-hinh-gia-thanh`) vs
`/api/cst-gia-thanh/truc-tiep/ky-tinh-gia-thanh`. Hai quy ước (`gia-thanh` / `cst-gia-thanh`, và vị
trí segment phương pháp tính) trong cùng một module → hợp đồng FE khó đoán. Chốt một quy ước trước
khi FE bám vào.

### m8 — Minor · Hằng số mã lỗi đặt ở `internal/model/` thay vì `internal/constant/`

`MaLoiCauHinhGiaThanh.java`, `MaLoiKyTinhGiaThanh.java` — mẫu tham chiếu mà chính javadoc viện dẫn là
`ban_hang/chung_tu_ban_hang/internal/constant/MaLoiBanHang.java`. Không gây lỗi, nhưng lệch mẫu.

### n1 — Nit · Hằng số chết

`MaLoiCauHinhGiaThanh.CAP_NHAT_LOI` / `MSG_CAP_NHAT_LOI` (`_007`) không được dùng ở bất kỳ đâu
(`git grep` toàn `src`).

### n2 — Nit · Commit message không theo chuẩn

`merge: hop nhat origin/develop vao …` (type `merge` không thuộc bộ chuẩn),
`Merge feat/logic-ky-tinh-gia-thanh vao feat/logic-cau-hinh-gia-thanh` (không có type/scope),
`feat(gia-thanh): add mandatory chiNhanhId branch scoping` (mô tả tiếng Anh, lẫn với các commit
tiếng Việt còn lại).

### n3 — Nit · PR gộp 2 epic + 1 refactor cấu trúc module

PMKT-E-05897 + PMKT-E-05908 + `refactor(gia-thanh): dua cau_hinh vao trong cst_gia_thanh`. Diff 59
file khiến việc quy trách khi hồi quy khó hơn cần thiết.

### n4 — Nit · Index gần trùng

`V1100` tạo `idx_cst_cau_hinh_gt_loai_yeu_to (tenant_id, phuong_phap_tinh, loai_yeu_to)` trong khi
baseline đã có `idx_cst_cau_hinh_gt_tenant (tenant_id, phuong_phap_tinh)` — index sau là prefix của
index trước, có thể bỏ index cũ.

---

## 3. Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ Đúng. `cst_gia_thanh/package-info.java` khai `@ApplicationModule`; `cau_hinh/` + `ky_tinh_gia_thanh/` là sub-module; mọi thứ nằm trong `internal/`; `cau_hinh/api/` có `package-info.java` khai `@NamedInterface("cau_hinh")` và chỉ lộ đúng 1 SPI. Không có file phẳng ở gốc module. `ProxyModularityTest#giaThanhKhongCoViPhamRanhGioiNao` được bổ sung. |
| 2 | Không đánh lại version migration | ⚠ **B1** |
| 3 | Chưa test lại sau khi merge | ⚠ Minor. Đo: `git rev-list --count 622dd2d9..origin/develop` = **3**; `comm -12` = **1 file giao nhau** — `DoiTruChungTuServiceTest.java`. Hai bên sửa **cùng** hunk `KhoanNo(… , UUID)` giống hệt nhau; develop sửa thêm hunk `DinhTuyenTaiKhoanCongNo(…)` mà nhánh này không chạm → 3-way merge tự giải quyết được, không thấy nguy cơ compile. Vẫn nên rebase/merge develop trước khi merge vì B1 buộc phải đụng migration. |
| 4 | Code chưa tối ưu / N+1 | ⚠ **m1**, **m2**. Không có `FetchType.EAGER`, không có lazy-access ngoài transaction, không `findAll` rồi lọc trong Java (trừ `findAllIdTen` — có chủ ý, BR2 so trùng sau chuẩn hoá không diễn đạt được bằng SQL). |
| 5 | Chưa tận dụng BaseController / BaseEntity | ✅ Chấp nhận. `KyTinhGiaThanh` extends `AggregateRootEntity` + `@Searchable` + `AbstractCrudService`; `KyTinhGiaThanhBaseController` copy 6 endpoint có lý do ghi rõ (mã quyền chỉ có `AllPermission`, và `search` trả DTO khác `get/create/update`) — đối chiếu `core/controller/BaseCrudController` xác nhận `PageResponse<D> search` cũng **không** bọc `ApiResponse`, nên đây là theo mẫu chứ không phải vi phạm luật 6. `CauHinhGiaThanh` là bespoke có lý do (ghi nhiều dòng 1 transaction). Không phải chứng từ kế toán ⇒ không cần `ChungTuTemplate`/`GhiSoApi`. |
| 6 | Chưa tận dụng base FE | N/A — PR không chạm `client/`. |
| 7 | Constant đặt sai chỗ | ⚠ **m8** (đặt ở `internal/model/` thay vì `internal/constant/`). Mã `MSG_…` đều là hằng số có tên, không rải chuỗi tại chỗ ném. |

## 4. Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | Không có secret trong diff. Không hardcode magic value (`"154"`, `"621"`… đều là hằng có tên trong `GiaTriMacDinhGiaThanh`; whitelist thông tư là `Set.of` hằng). Controller không chứa business logic, không gọi Repository, không trả Entity. Response bọc `ApiResponse<T>` (trừ `search` — theo mẫu base, xem #5). Không try/catch nuốt exception. Không chạm vùng đóng băng. Không commit thẳng `develop`. ⚠ **B1** (migration) và ⚠ **M2** (nghiệp vụ đảo ngược xác nhận BA) thuộc lớp này. |
| B — Kiến trúc & 7 lỗi | xem bảng trên |
| C — Nghiệp vụ & truy vết | ⚠ **B2**, **B3**, **M1**, **M2**, **M3**. Phần đối chiếu được thì **đúng**: BR1 `SCR_SuaCauHinh` (tập tiêu thức theo yếu tố) khớp từng giá trị với `TIEU_THUC_CHO_PHEP`; BR2 (khoá duy nhất `(PhuongPhapTinh, TaiKhoanTapHopChiPhiId)`) khớp unique index mới của `V1100`; BR3 (5 phương pháp tính, "Hệ số, tỷ lệ" trong phạm vi màn) hợp thức hoá route mới D16; BR7.4 (mặc định 154 → đệ quy con nhỏ nhất tới cấp cuối) khớp `timTaiKhoanCapCuoiMacDinh`; messageId của PMKT-E-05908 khớp **nguyên văn** `6.messages.md` (105/106/107/108/109/111/117/101/102/116). |
| D — Vệ sinh diff & Git | Nhánh `feat/logic-cau-hinh-gia-thanh` ✅. Cổng cây commit ✅ — `git status` sạch, không file `??`. Không `TODO` thiếu ticket; các chỗ "chưa triển khai" ném `UnsupportedOperationException` có mã Q1 kèm theo (cách làm tốt). ⚠ **n2**, **n3**. |

## 5. Kiểm chứng đã chạy

| Kiểm | Kết quả |
|---|---|
| `git ls-tree` migration trên `origin/develop` + quét **toàn bộ** remote branch cho `V1099`/`V1100` | ✅ chạy — ra **B1** |
| Đối chiếu `V1099`/`V1100` với tên index/constraint gốc trong `V1__create_database.sql` | ✅ khớp (`uq_cst_ky_tinh_gt_tenant_ten`, `idx_cst_cau_hinh_gt_tenant_range`, `cst_cau_hinh_gia_thanh_tieu_thuc_phan_bo_check` đều tồn tại) |
| Đối chiếu migration ↔ entity ↔ CHECK constraint | ✅ chạy — ra **B3** |
| `git rev-list --count` + `comm -12` (lỗi #3) | ✅ chạy — 3 commit / 1 file giao nhau |
| `git status --porcelain` (cổng cây commit) | ✅ sạch |
| `git grep` chữ ký core (`QuyenChecker.check`, `ApiResponse.ok`, `ApiException.*`, `AbstractCrudService`, `MaChucNang.GT_HE_SO_TY_LE`, quyền seed `V2:740-741`) | ✅ tồn tại đủ, không thấy nguy cơ compile-break |
| `br.sh --list` + `br.sh 46 29 19` | ✅ đọc BR46, BR29, BR19 |
| `scr.sh --stat/--br/--sec` trên `SCR_CauHinhGiaThanh_SuaCauHinh.md` | ✅ trích BR1, BR2, BR3, BR7.1–7.5 |
| Đối chiếu tay `6.messages.md` (cả 2 epic) với `MaLoi*` | ✅ chạy — ra **M3**, **m6** |
| `trace.sh` | **NOT-RUN** — không tồn tại `docs/doing/<slug>-spec/` cho PMKT-E-05897 / PMKT-E-05908 (cổng đặc tả chưa chạy, xem M1) |
| `msg.sh` | **NOT-RUN** — script quét `cell-app/src` của **working tree**, mà tree đang ở nhánh khác (`feat/chung-tu-ban-hang-2`); chế độ nhanh không tạo worktree ⇒ kết quả sẽ là dương tính giả toàn bộ. Đã thay bằng đối chiếu tay ở trên. |
| `./gradlew unitTest`, build, merge thử, baseline | **NOT-RUN — chế độ nhanh** |

**BR đã đọc**: BR46, BR29, BR19 (chung) + BR1, BR2, BR3, BR7.1–7.5 (nội bộ `SCR_CauHinhGiaThanh_SuaCauHinh`).
**BR chưa đọc** (liên quan nhưng chưa mở): BR20, BR23, BR25, BR26, BR27, BR28, BR47 (chung);
toàn bộ BR nội bộ của `SCR_CauHinhGiaThanh_DanhSach`, `SCR_CauHinhGiaThanh_XemChiTiet`,
`SCR_CauHinhGiaThanh_KhoiPhucCaiDatGoc`, và 4 màn của PMKT-E-05908.

## 6. Phần chưa đọc

- **Test (12 file)**: chỉ đọc tên test + `CauHinhGiaThanhControllerIT#luu_doiTkKetChuyen_dongBoCa3YeuTo`.
  Chưa soát nội dung assert của `CauHinhGiaThanhValidatorTest`, `CauHinhGiaThanhMapperTest`,
  `GiaTriMacDinhGiaThanhTest`, `KyTinhGiaThanhCrudServiceTest`, `KyTinhGiaThanhIntegrationTest`,
  `CauHinhGiaThanhServiceTaoBanGhiMacDinhTest`, `CauHinhGiaThanhMacDinhProvisionerTest`,
  `CauHinhGiaThanhServiceLayDanhMucTaiKhoanTest`, `KyTinhGiaThanhControllerRouteTest`.
- **Main**: `TaiKhoanRefDto.java`, `KyTinhGiaThanhDto.java`, `GiaTriDbGiaThanh.java` (3 file DTO/enum
  hạ tầng, đã suy được hợp đồng qua nơi dùng).
- **Chưa chạy màn thật** — không dùng `qa-flow`; mọi kết luận hành vi đều suy từ code + đặc tả.

---

## 7. Kết luận

**REJECT** — 3 Blocker (**B1**, **B2**, **B3**) + 3 Major (**M1**, **M2**, **M3**).

B1 chặn deploy; B2 và B3 là hai lỗi số liệu im lặng nằm đúng trên luồng chính của hai màn, đều có
test đã viết nhưng chưa từng chạy (Testcontainers, máy cấm Docker). B3 đã được chính javadoc trong PR
cảnh báo phải xử lý ở lượt merge này.

⚠ Cổng test/build **chưa chạy** (chế độ nhanh). Sau khi sửa, cần chạy `cd cell-app && ./gradlew unitTest`,
và chạy `CauHinhGiaThanhControllerIT` + `KyTinhGiaThanhIntegrationTest` ở môi trường **có Docker** —
đây là hai bộ test duy nhất có khả năng bắt B2/B3.
