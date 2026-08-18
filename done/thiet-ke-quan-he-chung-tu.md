# Bảng `ctu_quan_he_chung_tu` — quan hệ chứng từ nguồn ↔ đích ở mức dòng

> **Trạng thái:** BẢN NHÁP CHỜ USER/DBA CHỐT
> **Ngày khảo sát:** 2026-08-10 · **Migration lớn nhất:** V353
> **Người review:** 1 DBA (§3, §5, §7) + 1 Dev BE (§4, §6) + 1 BA (§8-C)

---

## 1. Vì sao có bảng này

### 1.1 Nghiệp vụ hiện tại đã chạy được

> *"Hàng hóa trong 1 hóa đơn thuộc nhiều chứng từ mua hàng khác nhau — DB đáp ứng chưa?"*

**Schema: rồi.** Mỗi dòng `pur_chi_tiet_hoa_don` mang cặp `(chung_tu_mua_hang_id, chi_tiet_chung_tu_mua_hang_id)` riêng (`V61:122-123`), nên 1 hóa đơn 10 dòng lấy hàng từ 10 chứng từ mua khác nhau. `V352:109-110` ghi thẳng *"một hoá đơn có thể gom nhiều chứng từ"*. BA xác nhận ở `SCR_HDMH_ThemMoi.md:5`.

**Java: chưa** — nhưng vì module hóa đơn/PXK/phiếu thu chưa tồn tại ở tầng Java, không phải vì thiếu quan hệ.

### 1.2 Ba khiếm khuyết thật

| # | Vấn đề | Bằng chứng |
|---|---|---|
| **L1** | Dòng **nguồn** chỉ nhớ được 1 chứng từ đích — xuất làm 2 hóa đơn là mất vết cái thứ hai | `sal_chung_tu_ban_hang_chi_tiet.hoa_don_ban_hang_id` (`V75:126`), `pur_chi_tiet_chung_tu_mua_hang.hoa_don_mua_id` (`V60:88`) |
| **L2** | Số cột nguồn tăng theo số loại chứng từ: 2 → 3 → 4 → **6** | `V61:122-128`, `V81:107-112`, `V77:130-137`, `V80:99-106` + `V182:7-9` |
| **L3** | Mỗi cặp nguồn→đích một câu SQL riêng — ~19 cặp trên 46 epic chứng từ | — |

Bảng này giải cả ba, và **không đụng tới cách tính số lượng** (§4).

### 1.3 Quyết định đã chốt

| # | Quyết định |
|---|---|
| **Q1** | **Không gộp dòng** — mỗi dòng đích ứng đúng 1 dòng nguồn. Hàng từ 2 chứng từ thì tách 2 dòng đích |
| **Q2** | Bảng **đa hình dùng chung** toàn hệ thống, thay các cột FK nguồn rời rạc |
| **Q3** | **Không lưu số lượng.** Cần số lượng thì đọc từ dòng chi tiết của chứng từ liên quan |
| **Q4** | Bỏ counter `so_luong_da_xuat_*` — tổng đã tiêu thụ tính bằng `SUM` |

### 1.4 Xung đột kiến trúc — đã báo, user chọn tiếp tục

Dự án đã 4 lần từ chối hướng gộp chung: `V281:6-8` · `V273:12-13` · `V345:113-116` · `BaseChiTietChungTuEntity.java:12-16`. Tiền lệ generic `mst_chung_tu_lien_quan` (`V2:80-90`) **đã chết** vì thiếu tenant/RLS/audit/soft-delete — §3.4 học đúng bốn lỗi đó.

---

## 2. Bảng — 17 cột

```
ctu_quan_he_chung_tu
├─ id, tenant_id                                          định danh
├─ loai_chung_tu_nguon, chung_tu_nguon_id, dong_nguon_id  đầu nguồn
├─ loai_chung_tu_dich,  chung_tu_dich_id,  dong_dich_id   đầu đích
└─ phien_ban, da_xoa, + 6 cột audit                       chuẩn hệ thống BR46
```

Một dòng đọc là: ***"dòng Y của chứng từ đích B đến từ dòng X của chứng từ nguồn A."***

| Cột | Kiểu | NULL | Default | Ai ghi | Ghi chú |
|---|---|:---:|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | server | PK |
| `tenant_id` | `uuid` | N | — | **server** (`fn_current_tenant()`) | DTO không có trường này |
| `loai_chung_tu_nguon` | `text` | N | — | server | mã ổn định, CHECK whitelist |
| `chung_tu_nguon_id` | `uuid` | N | — | server | header nguồn |
| `dong_nguon_id` | `uuid` | Y | — | server | dòng chi tiết nguồn; NULL ⇔ quan hệ mức header |
| `loai_chung_tu_dich` | `text` | N | — | server | |
| `chung_tu_dich_id` | `uuid` | N | — | server | |
| `dong_dich_id` | `uuid` | Y | — | server | |
| `phien_ban` | `integer` | N | `1` | server | optimistic lock |
| `da_xoa` | `boolean` | N | `false` | server | soft-delete |
| `ngay_tao`, `nguoi_tao`, `ngay_cap_nhat`, `nguoi_cap_nhat`, `ngay_xoa`, `nguoi_xoa` | | | | server | audit chuẩn |

Kèm `ENABLE` + **`FORCE`** `ROW LEVEL SECURITY`, policy `tenant_isolation` (cả `USING` và `WITH CHECK`), trigger `trg_audit_*` gọi `fn_audit()`, `GRANT … TO pmkt_app` — nguyên mẫu `V77:110-119`.

### 2.1 Vì sao lưu cả header id lẫn dòng id

Không có `chung_tu_nguon_id`, câu *"chứng từ này đã sinh ra gì / có được xóa không"* (BR17 §9, `SCR_CTBH_ThemMoi.md:954`) phải join ngược qua bảng chi tiết của **từng** loại chứng từ — mất đúng cái lợi thế "một query cho mọi cặp".

### 2.2 Những cột đã cân nhắc rồi bỏ

Ghi lại để người review biết đã xét, không phải bị quên:

| Cột | Vốn để làm gì | Vì sao bỏ |
|---|---|---|
| `luong` (HOA_DON/KHO/TIEN…) | tách luồng để không cộng nhầm | suy được từ `loai_chung_tu_dich`; ánh xạ nằm ở enum Java |
| `so_luong` và 7 cột số lượng khác | lưu lượng tiêu thụ theo cặp | **Q3** — đọc từ dòng đích (§4) |
| `khoa_yeu_cau` | chống retry cộng đôi số lượng | không còn số lượng để cộng; unique U1 đã idempotent (§3.2) |
| `nguon_ban_ghi` | đánh dấu dòng backfill kém chất lượng về số lượng | backfill giờ chỉ copy con trỏ, không có "gần đúng" |
| 4 cột snapshot số/ngày chứng từ | grid khỏi join 46 bảng | port đọc đa hình đã bắt buộc phải có (§4), lấy thêm số/ngày gần như miễn phí |
| `ghi_chu` | client nhập tự do | không màn hình BA nào yêu cầu |
| `chi_nhanh_id` | lọc/báo cáo theo chi nhánh | chưa có màn hình yêu cầu |
| `tu_dong` | phân biệt link sinh kèm / lập sau | **không đổi hành vi nào.** Link tồn tại ⇒ chứng từ con có thật trong hệ thống; hóa đơn ngoài hệ thống thì không có link, chỉ có cờ `da_lap_hoa_don` trên header. Chính sách xóa đã chốt là **chặn** cho mọi cặp (§8-C) nên không cần biết link sinh kèm hay lập sau |

Cả 8 nhóm này thêm lại sau đều là `ALTER TABLE ADD COLUMN` thuần, không phá dữ liệu.

---

## 3. Ràng buộc

### 3.1 Khóa chính
`PRIMARY KEY (id)` — không dùng PK tự nhiên composite vì `dong_*_id` nullable và JPA/audit toàn hệ thống giả định `id uuid` đơn.

### 3.2 Unique
```sql
U1  UNIQUE (tenant_id, dong_dich_id)
      WHERE da_xoa = false AND dong_dich_id IS NOT NULL;

U2  UNIQUE (tenant_id, loai_chung_tu_nguon, chung_tu_nguon_id,
                       loai_chung_tu_dich,  chung_tu_dich_id)
      WHERE da_xoa = false AND dong_dich_id IS NULL;
```

**U1 là hiện thân của quyết định Q1** — mỗi dòng đích đến từ đúng một dòng nguồn. Điều này giờ là index thật, không phải luật ngầm ở tầng ứng dụng.

U1 cũng **thay luôn idempotency key**: gửi lại cùng một dòng đích → conflict → `ON CONFLICT DO NOTHING`. Không cần `khoa_yeu_cau`.

`WHERE da_xoa = false` bắt buộc — không có nó, gỡ liên kết rồi liên kết lại sẽ vỡ unique. Đúng pattern `V77:103-106`, `V182:15-17`.

### 3.3 CHECK
```sql
CHECK (loai_chung_tu_nguon IN (…whitelist…))
CHECK (loai_chung_tu_dich  IN (…whitelist…))
CHECK ((dong_nguon_id IS NULL) = (dong_dich_id IS NULL))              -- grain đồng nhất hai đầu
CHECK ((chung_tu_nguon_id, dong_nguon_id)
    IS DISTINCT FROM (chung_tu_dich_id, dong_dich_id))                -- chống tự trỏ
```

Whitelist dùng **mã ổn định** (`SAL_CHUNG_TU_BAN_HANG`, `PUR_CHUNG_TU_MUA_HANG`, `INV_PHIEU_XUAT_KHO`…), trùng `mst_giao_dich_chung_tu.code` (`V344:42-45`) ở chỗ trùng nghĩa.

**Không** đặt FK vào `mst_loai_chung_tu`: bảng đó toàn cục không tenant/RLS (`V1:1951-1955`), `id` là uuid ngẫu nhiên nên không viết được CHECK, không đọc được khi debug, và một dòng bị xóa trong danh mục sẽ làm mọi tenant mất khả năng phân giải. Repo đã bỏ hướng này — `cfg_thiet_lap_khoa_so_chung_tu` dùng `ma_loai_chung_tu` trỏ vào `.code` chứ không `.id` (`V1:1237`).

### 3.4 Khóa ngoại — không có, và bốn hàng rào thay thế

Cột định danh đa hình nên không `REFERENCES` được. `mst_chung_tu_lien_quan` chết vì đúng bốn lỗi, nên bốn hàng rào:

1. **`tenant_id NOT NULL` + RLS `FORCE`** — không có `FORCE` thì owner bảng bỏ qua policy
2. **Server luôn gán tenant**, client gửi lên là bug
3. **Trigger `trg_kiem_tra_tenant_quan_he`** (BEFORE INSERT/UPDATE): phân giải `loai_chung_tu_*` → tên bảng qua whitelist, `EXECUTE format('SELECT tenant_id FROM %I WHERE id = $1')`, raise nếu lệch tenant hoặc không tồn tại. Đây là thứ thay cho FK. 4 lookup mỗi INSERT — chấp nhận được vì ghi theo lô nhỏ
4. **Soft-delete + audit** — liên kết gỡ nhầm còn truy được ai gỡ

Mọi index dẫn đầu `tenant_id` để RLS predicate đẩy được vào index scan.

**Hệ quả mất `ON DELETE`:** chính sách xóa chuyển lên ứng dụng. Điều này **đúng** với BR17 §9 (`:954`) — xóa chứng từ nguồn đã có liên kết phải **chặn** kèm `MSG_PMKT-E-06194_014`, không cascade.

⚠️ **Nhưng mất một thứ đang chạy thật:** `sal_chi_tiet_dieu_chinh_gia_hang_ban.chi_tiet_chung_tu_ban_hang_id` hiện là `ON DELETE RESTRICT` (`V81:108`) — DB đang chặn thật. Phải thay bằng guard `coLienKet()` ở service, **kèm test hồi quy trước khi drop cột** (R2).

---

## 4. Số lượng đọc từ đâu

Bảng này không lưu số lượng. Câu hỏi *"dòng nguồn X đã bị tiêu thụ bao nhiêu"* trả lời bằng:

```
quan hệ (theo dong_nguon_id) → danh sách dong_dich_id → đọc số lượng trên từng bảng đích
```

### 4.1 Khảo sát: bảng đích có sẵn số lượng không

| Bảng chi tiết đích | Cột số lượng | Nghiệp vụ cần SL? |
|---|---|---|
| `sal_hoa_don_ban_hang_chi_tiet` | `so_luong` (`V77:141`) | ✅ |
| `inv_phieu_xuat_kho_chi_tiet` | `so_luong_xuat`, `so_luong_xuat_quy_doi`, `he_so_quy_doi` (`V70:78-82`) | ✅ |
| `sal_chi_tiet_chung_tu_tra_lai_hang_ban` | `so_luong` | ✅ |
| `sal_chi_tiet_dieu_chinh_gia_hang_ban` | `so_luong_tang`, `so_luong_giam` | ✅ |
| `pur_chi_tiet_hoa_don` | ❌ không có (`V61:122-147`) | ❌ **không cần** — BA dùng cờ trọn dòng (`SCR_HDMH_ThemMoi.md:200`) |
| `cb_chi_tiet_phieu_thu` | ❌ không có | ❌ **không cần** — luồng tiền đo bằng tiền |

Hai bảng thiếu số lượng đúng là hai chỗ nghiệp vụ không cần. **Phương án không bị chặn.**

Với hóa đơn mua, **sự tồn tại của dòng quan hệ chính là cờ "đã nhận hóa đơn"** — cột `pur_chi_tiet_chung_tu_mua_hang.da_nhan_hoa_don` (`V60:87`) trở nên thừa.

### 4.2 Lợi ích lớn nhất: xóa sạch logic delta

BR17 §5.3/5.4 (`:899-909`) quy định sửa/xóa chứng từ con phải tính `-cũ +mới` rồi cập nhật counter. **Toàn bộ phần này biến mất.**

Người dùng sửa dòng hóa đơn từ 6 → 4? Không phải làm gì cả — lần `SUM` sau tự đúng. Rủi ro "retry cộng đôi" (vốn là rủi ro mức Cao) không còn tồn tại về mặt cấu trúc.

### 4.4 Không phải quan hệ nào cũng là "tiêu thụ"

Ràng buộc `Σ ≤ so_luong` **chỉ áp cho quan hệ lấy hàng đi khỏi dòng nguồn**. Điều chỉnh giá không lấy
đi hàng — cùng một dòng bán hàng có thể bị điều chỉnh giá nhiều lần; áp ràng buộc vào đó là sai bản chất.

| Loại chứng từ đích | Là tiêu thụ? | Áp `Σ ≤ so_luong`? |
|---|:---:|:---:|
| `SAL_HOA_DON_BAN_HANG` | ✅ | **có** |
| `INV_PHIEU_XUAT_KHO` | ✅ | **có** |
| `SAL_CHUNG_TU_TRA_LAI_HANG_BAN` | ✅ (không trả quá số đã bán) | **có** |
| `SAL_DIEU_CHINH_GIA_HANG_BAN` | ❌ | **không** |
| `CB_PHIEU_THU` | ❌ (đo bằng tiền) | **không** |

Cờ này khai ngay trong enum `LoaiChungTu` (§6.2), không rải điều kiện trong service.

### 4.3 Ba điều kiện phải xử lý

| # | Vấn đề | Cách xử lý |
|---|---|---|
| **Đ1** | Tên cột số lượng khác nhau ở mỗi bảng đích: `so_luong`, `so_luong_xuat`, `so_luong_tang`/`so_luong_giam` — không viết được một câu SUM chung | Port per-loại (§6.2). **Không phát sinh kiến trúc mới** — port này đã cần cho việc khóa dòng nguồn |
| **Đ2** | `sal_chi_tiet_dieu_chinh_gia_hang_ban` có **hai** cột tăng/giảm | Chốt luật lấy cột nào (hoặc hiệu hai cột) trước khi code — §8-B |
| ~~Đ3~~ | ✅ Đã chốt — thêm `he_so_quy_doi` vào `sal_hoa_don_ban_hang_chi_tiet`, xem §8-A |

---

## 5. Index

Mọi index dẫn đầu `tenant_id`, partial `WHERE da_xoa = false`.

| # | Index | Phục vụ |
|---|---|---|
| I1 | `(tenant_id, dong_nguon_id, loai_chung_tu_dich)` `WHERE dong_nguon_id IS NOT NULL` | tra xuôi: dòng nguồn này đã đi những đâu → đầu vào của mọi phép tính tồn |
| I2 | `(tenant_id, loai_chung_tu_nguon, chung_tu_nguon_id)` | chặn xóa nguồn (BR17 `:954`); tab "Chứng từ liên quan" |
| I3 | `(tenant_id, loai_chung_tu_dich, chung_tu_dich_id)` | tab "Nguồn" của chứng từ đích; gỡ toàn bộ liên kết khi xóa/bỏ ghi sổ đích |
| — | U1 đã phủ tra cứu theo `dong_dich_id` | — |

### 5.1 ⚠️ Điểm yếu hiệu năng: màn "chọn nguồn còn lại > 0"

BR17 §6.1 (`:924-926`) và `SCR_NguonCT_TongHop.md:131` yêu cầu chỉ hiện dòng có `SoLuong − SoLuongDaXuat > 0`.

| | Trước (có counter) | Nay |
|---|---|---|
| Câu query | index scan với partial index trên chính bảng dòng nguồn | JOIN `ctu_quan_he_chung_tu` → bảng đích (đa hình) → aggregate → mới lọc `> 0` |
| Lọc trước được? | Có | **Không** — vị ngữ nằm trên kết quả aggregate |

**Giảm thiểu:** thu hẹp tập ứng viên bằng vị ngữ có index trước (khách hàng + `status='DA_GHI_SO'` + khoảng ngày), rồi mới aggregate trên tập nhỏ.

**Đây là cổng quyết định ở P0** (§7). Không đạt ⇒ phải xem lại Q3/Q4.

### 5.2 Cột trạng thái header vẫn giữ

`trang_thai_hoa_don`, `trang_thai_thanh_toan`, `trang_thai_xuat_hang` (`V75:68-73`) là cột **lọc và sắp xếp** của màn danh sách (F01, BR03) — không tính động trong `WHERE`/`ORDER BY` được. Giữ nguyên cột, **tính lại từ aggregate** sau mỗi thao tác ghi. Công thức giữ đúng BR17 §7 (`:933-943`).

---

## 6. Đồng thời và Java

### 6.1 Chống xuất vượt

BR17 §3.3 (`:870`) yêu cầu kiểm tra nguyên tử, chống hai người cùng lập gây xuất vượt. Không còn counter để `UPDATE … WHERE counter + delta <= so_luong`, nên:

```
1. Khóa dòng nguồn:  SELECT id, so_luong FROM <bảng dòng nguồn>
                      WHERE id = ANY(:ids) AND da_xoa = false
                      ORDER BY id            ← chống deadlock
                      FOR UPDATE             ← điểm serialize, dù KHÔNG ghi hàng này

2. Đọc đã tiêu thụ:  quan hệ theo dong_nguon_id → dong_dich_id
                      → gọi port lấy số lượng trên từng bảng đích → cộng

3. Kiểm:             đã tiêu thụ + lượng mới <= so_luong
                      vi phạm → MSG_PMKT-E-06194_102

4. Ghi:              INSERT … ON CONFLICT (U1) DO NOTHING

5. commit (thả khóa)
```

Bước 1 là điểm mấu chốt: giao dịch thứ hai bị chặn tại hàng nguồn tới khi giao dịch thứ nhất commit, rồi mới chạy bước 2 và thấy tổng đã tăng. Không có cửa sổ TOCTOU. **Khóa hàng mà không ghi hàng là hợp lệ.**

**Không chọn `SERIALIZABLE`** — phải xử lý retry `40001` ở mọi endpoint chứng từ cho một bất biến cục bộ.

⚠️ **Bất biến `Σ tiêu thụ ≤ so_luong` không cưỡng chế được ở DB.** Trước đây counter nằm cùng hàng với `so_luong` nên `CHECK` nội-hàng ép được thật. Nay chỉ còn cơ chế khóa ở trên + job quét ban đêm. Nghĩa là script/migration ghi thẳng, bỏ qua tầng service, sẽ phá bất biến mà không gì báo. **Ghi vào `COMMENT ON TABLE`.**

### 6.2 Module Modulith mới

```
vn.dopai.pmkt.cell.quan_he_chung_tu/
├── package-info.java          @ApplicationModule
├── api/                       ← duy nhất được import từ ngoài
│   ├── QuanHeChungTuApi.java
│   ├── LoaiChungTu.java       enum ↔ whitelist CHECK trong DB
│   ├── DongChungTuPort.java   ← SPI, module nguồn/đích implement
│   └── LenhLienKet · TieuThuDto
└── internal/  entity · repository · service · DoiSoatJob
```

**`DongChungTuPort`** — một interface giải cả hai bài toán đa hình:
- `LoaiChungTu loaiHoTro()`
- `Map<UUID,BigDecimal> khoaVaLaySoLuong(List<UUID> dongIds)` — `SELECT … ORDER BY id FOR UPDATE` trên bảng của chính module đó (bước 1)
- `Map<UUID,BigDecimal> laySoLuong(List<UUID> dongIds)` — đọc số lượng, mỗi module biết tên cột của mình (bước 2, giải Đ1)
- `Map<UUID,ThongTinDong> layThongTin(List<UUID> dongIds)` — số/ngày chứng từ cho grid (thay 4 cột snapshot đã bỏ)

Mỗi module nguồn/đích đăng ký một `@Component`. `QuanHeChungTuService` build `Map<LoaiChungTu, DongChungTuPort>` từ danh sách bean. Phụ thuộc một chiều: `<module nghiệp vụ> → quan_he_chung_tu.api`, không chu trình.

**Vì sao không đặt trong `accounting_core`:** package-info của nó khai phạm vi hẹp — *"nơi DUY NHẤT được ghi vào sổ cái"*; quan hệ chứng từ không chạm sổ cái (`V77:101` ghi rõ hóa đơn "KHÔNG hạch toán"). **Không đặt trong `chung_tu_ban_hang`/`chung_tu_mua_hang`** — sẽ buộc `inv_`/`cst_` phụ thuộc `sal_`, sai chiều. **Không đặt trong `common`** — đó là tiện ích không nghiệp vụ.

### 6.3 API

`lienKet(...)` · `goLienKet(...)` / `goToanBoTheoDich(...)` · `daTieuThu(dongNguonIds)` · `theoNguon(...)` / `theoDich(...)` · `coLienKet(loaiNguon, chungTuNguonId)` → **guard xóa**, thay `ON DELETE RESTRICT` đã mất.

Không có `capNhatLienKet(...)` — sửa số lượng là sửa dòng đích, bảng quan hệ không đổi (§4.2).

Tuân CLAUDE.md: Controller → Service → Repository → Entity (luật 5); entity không lọt khỏi `internal`; `ApiResponse<T>` (luật 6); message i18n giữ nguyên văn BR (luật 2).

### 6.4 Job đối soát

Mất FK và mất CHECK nên cần quét ban đêm (per tenant, trong ngữ cảnh RLS):

1. **Mồ côi** — dòng quan hệ trỏ tới `dong_nguon_id`/`dong_dich_id` không tồn tại hoặc đã `da_xoa` *(thay cho FK)*
2. **Vượt nguồn** — `Σ tiêu thụ > dòng_nguồn.so_luong` *(thay cho CHECK)*
3. **Lệch trạng thái** — `trang_thai_*` trên header vs aggregate thật

Chênh lệch → log `WARN` + ghi bảng ops, **không tự sửa** lần đầu (tự sửa im lặng che mất bug ghi).

---

## 7. Migration — 4 pha

| Pha | Nội dung | Cổng |
|---|---|---|
| **P0** | Tạo bảng + 3 index + RLS FORCE + trigger tenant-guard + audit + GRANT. Chưa ai ghi. **Benchmark §5.1**. Kèm `DROP TABLE mst_chung_tu_lien_quan` (§7.4) | benchmark đạt; không đạt ⇒ xem lại Q3/Q4 |
| **P1** | Backfill + **dual-write** (ghi cả cột FK cũ và dòng quan hệ, cùng transaction; đọc vẫn từ cột cũ) | chạy song song **≥1 chu kỳ đóng sổ** — sai sót chỉ lộ khi đối chiếu, không lộ trong smoke test |
| **P2** | Chuyển đọc sang `QuanHeChungTuApi`; trạng thái header tính từ aggregate; ngừng ghi cột cũ; `COMMENT … DEPRECATED`; **guard `coLienKet()` thay `ON DELETE RESTRICT` của `V81:108`** | test hồi quy xóa xanh |
| **P3** | `DROP COLUMN` — migration riêng, sau ≥1 release ổn định | `grep` sạch trên `../../cell-app/src` |

**Không gộp P3 vào P2** — P3 là breaking cho entity JPA và mọi native query.

### 7.1 Backfill

Chỉ copy con trỏ, không suy số lượng ⇒ **không có "gần đúng"**, mọi cặp đều chính xác:

| Từ | Số cột phải quét |
|---|---|
| `sal_hoa_don_ban_hang_chi_tiet` (`V77:134,136`) | 2 |
| `sal_chi_tiet_chung_tu_tra_lai_hang_ban` (`V80:99-106`, `V182:7-9`) | 6 — dòng có ≥2 cột non-null là **dữ liệu bẩn**, dump ra bảng ops |
| `sal_chi_tiet_dieu_chinh_gia_hang_ban` (`V81:107-112`) | 3 |
| `pur_chi_tiet_hoa_don` (`V61:127`) | 1 |

**Không backfill được:** liên kết mức header không có dòng id — `pur_hoa_don_mua.chung_tu_mua_hang_id` (`V61:102`, *"chỉ khi gom đúng 1 CT"*). Mất mát chấp nhận được: những dòng đó vốn không có thông tin line-level nào để mất.

### 7.2 Cột bị xóa ở P3 — 23 cột trên 7 bảng

| Bảng | Cột | Số |
|---|---|---|
| `sal_chung_tu_ban_hang_chi_tiet` | 3 counter `so_luong_da_xuat_*` + `hoa_don_ban_hang_id` | 4 |
| `sal_hoa_don_ban_hang_chi_tiet` | 4 cột nguồn | 4 |
| `sal_chi_tiet_chung_tu_tra_lai_hang_ban` | 6 cột nguồn | 6 |
| `sal_chi_tiet_dieu_chinh_gia_hang_ban` | 3 cột nguồn | 3 |
| `pur_chi_tiet_hoa_don` | 2 cột nguồn | 2 |
| `pur_chi_tiet_chung_tu_mua_hang` | `da_nhan_hoa_don`, `hoa_don_mua_id` | 2 |
| `sal_chung_tu_ban_hang` | `phieu_xuat_kho_id`, `phieu_thu_id` | 2 |

**Giữ lại:** 3 cột `trang_thai_*` trên header (§5.2).

### 7.4 Dọn `mst_chung_tu_lien_quan`

Bảng generic đầu tiên của dự án, tạo ở `V2:80-90`, **chết từ đầu**: không `tenant_id`, không RLS,
không audit, không soft-delete — `V2:76-79` tự ghi nhận rủi ro rò rỉ cross-tenant và *"hiện chưa có
module nào tham chiếu"*.

Khảo sát 2026-08-10 xác nhận: **không một tham chiếu nào** trong `../../cell-app/src` ngoài chính V2 tạo ra
nó. `DROP TABLE public.mst_chung_tu_lien_quan;` đi kèm P0.

Không dùng `IF EXISTS` — bảng không tồn tại thì migration phải đỏ để biết môi trường đã lệch.

### 7.3 Thứ tự với đợt chuẩn hóa tên bảng

[chuan-hoa-ten-bang-chung-tu.md](../chuan-hoa-ten-bang-chung-tu.md) (52 bảng) và migration này **không được chồng lấn** — câu backfill tham chiếu tên bảng cũ sẽ vỡ giữa chừng. Chạy xong **đợt 1 (`sal_`) và đợt 2 (`pur_`)** rồi mới vào P1. Bảng mới đặt đúng chuẩn tên ngay từ P0.

---

## 8. Còn phải chốt

| # | Vấn đề | Mặc định |
|---|---|---|
| ~~A~~ | ✅ **Đã chốt: thêm `he_so_quy_doi numeric(18,6) NOT NULL DEFAULT 1` vào `sal_hoa_don_ban_hang_chi_tiet`.** Không cấm khác ĐVT — `inv_phieu_xuat_kho_chi_tiet` đã có sẵn hệ số (`V70:78-80`), cấm ở hóa đơn sẽ làm hai bảng đích hành xử khác nhau vô cớ. Lưu hệ số tại dòng đích ⇒ đóng băng tại thời điểm lập, số lịch sử không trôi. *(Cột thuộc phạm vi team module hóa đơn — phải báo họ)* | — |
| ~~B~~ | ✅ **Đã chốt: `COALESCE(so_luong_tang, so_luong_giam)`** — bảng có hai khối đối xứng (`V81:117-125`), một dòng chỉ dùng một khối. Kèm §4.4 | — |
| **C** | Chính sách xóa cho 18 cặp còn lại. BR41 nói *"theo quy tắc riêng từng epic"* (`business_rules.md:921-922`), BR17 chốt **chặn** cho CTBH (`:954`). Cần bảng quyết định trước khi code, nếu không mỗi epic tự chọn khác nhau | chặn, như BR17 |
| **D** | Tên bảng `ctu_quan_he_chung_tu` (theo ADR-05 phải có tiền tố module) hay `quan_he_chung_tu` (không prefix) | `ctu_` |
| **E** | Quan hệ mức header (`dong_*` NULL) có dùng cho luồng tiền/đối trừ không, hay để `pur_chi_tiet_chung_tu_doi_tru` (`V230:74-105`) sống riêng? | giai đoạn 1 **chỉ hàng hóa**; không đụng module đối trừ đang chạy |

---

## 9. Rủi ro

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| R1 | **Không cưỡng chế được `Σ tiêu thụ ≤ so_luong` ở DB** — hệ quả của Q4 | **Cao** | khóa `FOR UPDATE` (§6.1); job quét vượt nguồn (§6.4-2); test 2 transaction song song **bắt buộc** |
| R2 | **Mất `ON DELETE RESTRICT`** đang chạy thật (`V81:108`) | **Cao** | guard `coLienKet()` + test hồi quy **trước** khi drop cột; chỉ drop ở P3 |
| R3 | **Không FK ⇒ mồ côi / sai tenant** — đúng vết `mst_chung_tu_lien_quan` (`V2:76-79`) | **Cao** | 4 hàng rào §3.4; job quét mồ côi; test cross-tenant trong CI |
| R4 | **Màn chọn nguồn chậm** — aggregate đa hình, không index được (§5.1) | **Cao** | benchmark P0 **trước khi** cam kết; thu hẹp tập ứng viên trước |
| R5 | Đọc số lượng thành **N+1** khi grid liệt kê nhiều dòng quan hệ | TB | port nhận `List<UUID>` và gom theo loại đích — batch một lần mỗi loại, không lặp từng dòng |
| R6 | Deadlock khi một lần lưu chạm nhiều dòng nguồn | TB | `ORDER BY id` trước `FOR UPDATE` |
| R7 | Trôi số lịch sử do hệ số quy đổi đổi trong danh mục (Đ3) | TB | chốt §8-A |
| R8 | Whitelist DB lệch enum Java khi thêm loại chứng từ | TB | test đồng bộ query `pg_constraint`; không có test này thì lỗi chỉ lộ ở production |
| R9 | Trigger tenant-guard đắt (4 lookup + dynamic SQL mỗi INSERT) | TB | benchmark P0; hạ xuống chỉ kiểm 2 header id nếu cần |
| R10 | Dev nhầm bảng này với 5 bảng tham chiếu mềm BR41 | Thấp | `COMMENT ON TABLE` nói rõ ranh giới (§10) |
| R11 | Xung đột với đợt rename 52 bảng | TB | xếp tuần tự (§7.3) |

> So với bản trước (34 cột): rủi ro **"retry cộng đôi"** và **"lệch counter ↔ bảng"** đã biến mất về mặt cấu trúc — không còn số liệu trùng lặp để lệch.

---

## 10. Ranh giới với tham chiếu mềm BR41 — không gộp

`Common/business_rules.md:919-922` tách bạch hai nhóm:

| | Tham chiếu mềm (BR41) | Bảng này |
|---|---|---|
| Bản chất | liên kết thông tin, truy vết | quan hệ nghiệp vụ có ràng buộc |
| Khi xóa/bỏ ghi sổ nguồn | **tự gỡ ngầm**, không cảnh báo | **chặn hoặc cảnh báo** theo từng epic |
| Bảng | `pur_chung_tu_tham_chieu` (`V60:198`), `cb_phieu_thu_tham_chieu` (`V266`), `pur_hoa_don_tham_chieu` (`V273`), `pur_dcgm_tham_chieu` (`V281`), `ccdc_chung_tu_lien_quan` (`V241`) | `ctu_quan_he_chung_tu` |

Hai chính sách xóa **trái ngược nhau** — gộp sẽ cần cột `la_tham_chieu_mem` và hai nhánh xử lý ngược chiều. Giữ riêng, ghi rõ trong `COMMENT ON TABLE`.

---

## 11. Kiểm thử

### 11.1 Cổng quyết định — benchmark P0

Sinh ~1 triệu dòng quan hệ trên một tenant, đo p95 của: (a) màn chọn nguồn còn lại > 0 · (b) tính trạng thái header một chứng từ 50 dòng · (c) `daTieuThu()` cho 50 dòng nguồn. So với baseline có counter.

**Không đạt ⇒ báo lại user, cân nhắc giữ counter.**

### 11.2 Test bắt buộc

| # | Test | Kiểm gì |
|---|---|---|
| 1 | **Đồng thời** (cần Docker) | hai transaction cùng lập chứng từ con từ một dòng nguồn `so_luong=10`, mỗi bên 6 → đúng một bên thành công, bên kia nhận `MSG_PMKT-E-06194_102`. Bắt buộc cho BR17 `:870` |
| 2 | **Idempotent** | gửi lại cùng dòng đích → `ON CONFLICT DO NOTHING`, không sinh bản ghi thứ hai |
| 3 | **Cross-tenant** | insert quan hệ trỏ tới dòng nguồn của tenant khác → trigger raise |
| 4 | **Đồng bộ enum ↔ CHECK** | query `pg_constraint`, so với `LoaiChungTu.values()` |
| 5 | **Hồi quy xóa** | xóa CTBH đã có ĐCGHB liên kết → bị chặn, đúng như `ON DELETE RESTRICT` cũ |
| 6 | **Sửa dòng đích** | sửa số lượng dòng hóa đơn 6 → 4, **không đụng bảng quan hệ**, `daTieuThu()` trả về 4 |
| 7 | **Modulith** | `ApplicationModules.verify()` xanh; không module nào import `quan_he_chung_tu.internal` |

### 11.3 Lệnh chạy trước khi báo hoàn thành

```bash
cd cell-app && ./gradlew unitTest
```

```bash
cd cell-app && ./gradlew build
```

`../../cell-app` là Gradle project độc lập (wrapper riêng); repo root không có `gradlew`. Máy dev chưa có Docker thì `build` luôn đỏ ở test Testcontainers — đối chiếu danh sách lớp lỗi trước khi kết luận hồi quy.

---

## 12. Tham chiếu

- Migration: V1, V2, V57, V60, V61, V70, V75, V77, V80, V81, V182, V230, V241, V266, V273, V281, V344, V352.
- BA: `PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_ThemMoi.md:847-957` (BR17) · `PMKT-E-00542-HoaDonMuaHang/5.screens/SCR_HDMH_ThemMoi.md:5,198-205` · `Common/NguonDuLieu/SCR_NguonCT_TongHop.md:131` · `Common/business_rules.md:907-924` (BR41).
- BR: BR17 · BR19 · BR28 · BR29 · BR41 · BR46.
- Liên quan: [10-thiet-ke-db.md](../doing/PMKT-E-06194-chung-tu-ban-hang-api/10-thiet-ke-db.md) · [09-chung-tu-lien-quan.md](../doing/PMKT-E-06194-chung-tu-ban-hang-api/09-chung-tu-lien-quan.md) · [chuan-hoa-ten-bang-chung-tu.md](../chuan-hoa-ten-bang-chung-tu.md) · `../../CLAUDE.md` · `../conventions.md`.
