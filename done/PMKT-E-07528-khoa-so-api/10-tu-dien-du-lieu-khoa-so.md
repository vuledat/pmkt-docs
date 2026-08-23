# Từ điển dữ liệu — 3 bảng khoá sổ

Trạng thái schema **sau V358** (đã tính các migration đổi tên V3 `is_deleted→da_xoa`, V6
`created_*→ngay_tao/nguoi_tao…` + `version→phien_ban`, V16 dọn cột audit trùng).
Nguồn: `V1__baseline.sql:1145-1257` · `V358__cfg_thiet_lap_khoa_so_theo_ba_khoa_so.sql` ·
entity `accounting_core/khoa_so/internal/entity/`.

---

## 1. `cfg_thiet_lap_khoa_so` — bảng cha

Entity: `ThietLapKhoaSo` (extends `AggregateRootEntity`).

> **Một bảng chứa hai loại dòng.** `nhom_ban_ghi = 2` là dòng **THIẾT LẬP** (cấu hình lịch chạy
> tự động, không mang mốc khoá); `nhom_ban_ghi = 1` là dòng **KẾT QUẢ** (mốc khoá đang có hiệu
> lực, do người dùng chốt tay hoặc do job sinh ra). Hai nhóm ghép với nhau qua `pham_vi_hash`.

### Trường nghiệp vụ

| Cột | Kiểu | Null | Field Java | Mô tả |
|---|---|---|---|---|
| `id` | uuid | ✗ | `id` | Khoá chính, `gen_random_uuid()` |
| `tenant_id` | uuid | ✗ | `tenantId` | Multi-tenant (BR28); RLS **FORCE** trên bảng này |
| `loai_doi_tuong` | integer | ✗ | `loaiDoiTuong` | BR02 — `1` = Toàn hệ thống, `2` = Chọn chứng từ. `1` ⇒ áp cho **mọi** loại chứng từ, bảng con `_chung_tu` để rỗng |
| `loai_chon_nguoi_dung` | integer | ✓ | `loaiChonNguoiDung` | BR02 — `1` = Tất cả, `2` = Chọn người dùng. **NULL khi `loai_doi_tuong = 1`**. V358 chuyển cột này từ bảng con lên cha: nó là radio cấp form, không phải thuộc tính của từng người dùng |
| `chi_nhanh_id` | uuid | ✓ | `chiNhanhId` | Chi nhánh (`mst_don_vi`) áp khoá. **NULL = khoá cấp pháp nhân (toàn tenant)**. Tham gia `pham_vi_hash`. API/UI **chưa lộ** trường này (BA chưa có) ⇒ mọi bản ghi sinh từ UI hiện đều NULL — câu hỏi mở Q15 |
| `loai_khoa_so` | integer | ✗ | `loaiKhoaSo` | BR03 — `1` = Thủ công, `2` = Thiết lập (lịch tự động), `3` = Tự động (kết quả job) |
| `nhom_ban_ghi` | integer | ✗ | `nhomBanGhi` | **Cột SINH** (`GENERATED ALWAYS … STORED`), read-only ở Java: `loai_khoa_so = 2 → 2` (THIẾT LẬP), còn lại `→ 1` (KẾT QUẢ). Tồn tại để khoá chống trùng phạm vi tách được theo nhóm |
| `ngay_khoa_so` | timestamptz | ✓ | `ngayKhoaSo` | **Mốc khoá sổ** — bút toán có `ngay_hach_toan <= mốc` bị chặn. Bắt buộc trên dòng KẾT QUẢ, luôn NULL trên dòng THIẾT LẬP (`ck_cfg_tlks_ngay_khoa`) |
| `la_mac_dinh` | boolean | ✗ | `laMacDinh` | BR04 — bản ghi mặc định sinh lúc provisioning tenant, **không cho xoá** (`ck_cfg_tlks_mac_dinh_khong_xoa`). Mặc định `false` |
| `pham_vi_hash` | char(64) | ✗ | `phamViHash` | SHA-256 hex thường của phạm vi đã chuẩn hoá (loại đối tượng × tập loại chứng từ × cách chọn người dùng × tập user × chi nhánh). Tính ở Java (`PhamViKhoaSoHasher`), **không** phải cột sinh vì hai tập con nằm ở bảng khác. Công thức: `09-thiet-ke-db.md §4.2` |

### Trường lịch chạy tự động (chỉ có nghĩa trên dòng THIẾT LẬP)

| Cột | Kiểu | Null | Field Java | Mô tả |
|---|---|---|---|---|
| `is_tu_dong` | boolean | ✗ | `tuDong` | Bật/tắt lịch. Ràng buộc `ck_cfg_tlks_tu_dong`: **luôn** bằng `(loai_khoa_so = 2)` — hai cột nói cùng một sự thật, không được lệch |
| `ky_khoa_so` | integer | ✓ | `kyKhoaSo` | BR06 — `1` = Hàng ngày, `2` = Hàng tuần, `3` = Hàng tháng |
| `gia_tri_ky` | integer | ✓ | `giaTriKy` | BR06 — tuần: `1..7` (T2..CN) · tháng: `1..31`, **`32` = ngày cuối tháng** (chốt Q2). CHECK hiện chỉ chặn `1..32`; siết chặt theo từng chu kỳ chờ Q1 |
| `do_tre_thuc_thi` | integer | ✓ | `doTreThucThi` | BR06 — số ngày trễ so với mốc chốt dữ liệu, `-31..31` |
| `gio_thuc_thi` | time | ✓ | `gioThucThi` | BR06 — giờ chạy trong ngày. `is_tu_dong = true` ⇒ bắt buộc có `ky_khoa_so` **và** `gio_thuc_thi` (`ck_cfg_tlks_lich`) |
| `moc_chay_ke_tiep` | timestamptz | ✓ | `mocChayKeTiep` | Thời điểm job phải chạy lần tới = mốc chốt dữ liệu + độ trễ + giờ (BR07). Là khoá lọc của truy vấn tới hạn (`idx_cfg_tlks_job`, poll mỗi 5 phút) |
| `lan_chay_gan_nhat` | timestamptz | ✓ | `lanChayGanNhat` | Lần job chạy gần nhất — truy vết + chống chạy lặp trong cùng chu kỳ |

### Trường hệ thống (BR46, từ `BaseEntity` / `AggregateRootEntity`)

`phien_ban` (optimistic lock, NOT NULL, default 1) · `ngay_tao` · `nguoi_tao` · `ngay_cap_nhat` ·
`nguoi_cap_nhat` · `da_xoa` (NOT NULL default false) · `ngay_xoa` · `nguoi_xoa`.

### Ràng buộc & index

| Tên | Nội dung |
|---|---|
| `ck_cfg_tlks_loai_doi_tuong` | `loai_doi_tuong IN (1,2)` |
| `ck_cfg_tlks_loai_khoa_so` | `loai_khoa_so IN (1,2,3)` |
| `ck_cfg_tlks_tu_dong` | `(loai_khoa_so = 2) = is_tu_dong` |
| `ck_cfg_tlks_ngay_khoa` | dòng KẾT QUẢ phải có `ngay_khoa_so` (miễn cho `la_mac_dinh`) |
| `ck_cfg_tlks_pham_vi_user` | `loai_doi_tuong = 1` **hoặc** `loai_chon_nguoi_dung IN (1,2)` |
| `ck_cfg_tlks_ky_khoa_so` / `_gia_tri_ky` / `_do_tre` / `_lich` | miền giá trị lịch, xem bảng trên |
| `ck_cfg_tlks_mac_dinh_khong_xoa` | `NOT (la_mac_dinh AND da_xoa)` |
| `uq_cfg_tlks_pham_vi` | UNIQUE `(tenant_id, nhom_ban_ghi, pham_vi_hash) WHERE da_xoa = false` — BR03 ghi đè |
| `idx_cfg_tlks_job` | `(moc_chay_ke_tiep) WHERE da_xoa = false AND loai_khoa_so = 2 AND is_tu_dong` |

---

## 2. `cfg_thiet_lap_khoa_so_chung_tu` — phạm vi loại chứng từ

Entity: `ThietLapKhoaSoChungTu` (extends `TenantedEntity`).

| Cột | Kiểu | Null | Field Java | Mô tả |
|---|---|---|---|---|
| `id` | uuid | ✗ | `id` | Khoá chính |
| `thiet_lap_id` | uuid | ✗ | `thietLap` | FK → `cfg_thiet_lap_khoa_so(id)` **ON DELETE RESTRICT** (BR29.1 cấm xoá vật lý; RESTRICT là hàng rào chống script vá tay) |
| `ma_loai_chung_tu` | text | ✗ | `maLoaiChungTu` | FK → `mst_loai_chung_tu(code)` RESTRICT. Ví dụ `MUA_HANG`, `BAN_HANG`. Java vẫn kiểm trước (`LoaiChungTuLookup.idTheoMa` ném 400 với mã lạ) để lỗi có message đọc được |
| `tenant_id` | uuid | ✗ | `tenantId` | RLS FORCE |

Trường hệ thống: `phien_ban`, `ngay_tao`, `nguoi_tao`, `ngay_cap_nhat`, `nguoi_cap_nhat`, `da_xoa`,
`ngay_xoa`, `nguoi_xoa`.

Index: `uq_cfg_tlks_ct` UNIQUE `(thiet_lap_id, ma_loai_chung_tu) WHERE da_xoa = false`.

**0 dòng con** ⇔ phạm vi toàn hệ thống (`loai_doi_tuong = 1`) ⇒ áp cho mọi loại chứng từ.

---

## 3. `cfg_thiet_lap_khoa_so_nguoi_dung` — phạm vi người dùng

Entity: `ThietLapKhoaSoNguoiDung` (extends `TenantedEntity`).

| Cột | Kiểu | Null | Field Java | Mô tả |
|---|---|---|---|---|
| `id` | uuid | ✗ | `id` | Khoá chính |
| `thiet_lap_id` | uuid | ✗ | `thietLap` | FK → `cfg_thiet_lap_khoa_so(id)` ON DELETE RESTRICT |
| `user_id` | uuid | ✗ | `userId` | Người dùng thuộc phạm vi khoá. **Siết NOT NULL ở V358**: phạm vi "Tất cả" nay biểu diễn bằng `cha.loai_chon_nguoi_dung = 1` với **0 dòng con**, không phải bằng một dòng `user_id NULL` |
| `tenant_id` | uuid | ✗ | `tenantId` | RLS FORCE |

Trường hệ thống: giống bảng `_chung_tu`.

Index: `uq_cfg_tlks_nd` UNIQUE `(thiet_lap_id, user_id) WHERE da_xoa = false`.

Cột `loai_chon_nguoi_dung` **đã bị DROP ở V358** — chuyển lên bảng cha.

---

## 4. Ai đọc 3 bảng này

| Nơi đọc | Cách đọc |
|---|---|
| `KyKeToanChecker` → `KhoaSoRepository.SQL_MOC_KHOA` (Java) | Lấy `MAX(ngay_khoa_so)` của các dòng phủ `(loại chứng từ, người đang đăng nhập, chi nhánh)` |
| Trigger `acc_so_cai_period_guard` (V359 chiều người dùng, V362 chiều chi nhánh) | Cùng logic, đọc thẳng 3 bảng ở tầng DB — chốt chặn cuối cho mọi đường ghi không qua service |
| `KhoaSoTuDongXuLy` (job) | `FOR UPDATE SKIP LOCKED` trên dòng THIẾT LẬP, rồi ghi đè dòng KẾT QUẢ cùng `pham_vi_hash` |
| `fn_khoa_so_thiet_lap_toi_han` (V361) | Truy vấn thiết lập tới hạn cho poller |
