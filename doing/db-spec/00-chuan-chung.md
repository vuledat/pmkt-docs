# Chuẩn chung cho toàn bộ đặc tả bảng

> **Trạng thái:** `CHỜ BA + DBA + DEV BE CHỐT`
> Áp dụng cho **mọi** bảng trong thư mục này. Bảng nào lệch chuẩn phải ghi rõ lý do tại chính bảng đó.
> Kế hoạch tổng: [`../plan-gen-db.md`](../plan-gen-db.md)

---

## 1. Đặt tên bảng

```
<module>_<nghiệp vụ>[_<bảng con>]
   │          │            └── chi_tiet · tham_chieu · lien_ket · nguoi_kiem_ke · …
   │          └── viết đầy đủ, không viết tắt, không lặp lại tiền tố module
   └── prefix module
```

| Prefix | Phân hệ | Prefix | Phân hệ |
|---|---|---|---|
| `acc_` | Sổ kế toán (sổ cái · sổ kho · sổ thuế) | `inv_` | Kho |
| `agg_` | Bảng tổng hợp / rollup | `iam_` | Người dùng · vai trò · quyền · tenant |
| `aud_` | Nhật ký kiểm toán | `ktth_` | Kế toán tổng hợp · kết chuyển lãi lỗ |
| `cb_` | Ngân quỹ (tiền mặt · tiền gửi) | `mst_` | Danh mục *(ngoài phạm vi)* |
| `ccdc_` | Công cụ dụng cụ | `ops_` | Vận hành · webhook |
| `cfg_` | Cấu hình hệ thống | `pur_` | Mua hàng |
| `core_` | Hạ tầng dùng chung | `rpt_` | Báo cáo tài chính |
| `cptt_` | Chi phí trả trước | `sal_` | Bán hàng |
| `cst_` | Giá thành | `sdbd_` | Số dư ban đầu |
| `ctu_` | Quan hệ chứng từ | `str_` | Lưu trữ tệp |
| `fa_` | Tài sản cố định | `tax_` | Thuế |
| `fx_` | Đánh giá lại ngoại tệ **(prefix mới — chờ chốt Q8)** | | |

Hai luật cứng — theo [`../../chuan-hoa-ten-bang-chung-tu.md`](../../chuan-hoa-ten-bang-chung-tu.md):

**Luật 1 — `chi_tiet` là hậu tố, không phải tiền tố.** Tên bảng con luôn là `<tên bảng cha>_<vai trò>`:

| Entity LDM | ✅ Đúng | ❌ Sai |
|---|---|---|
| `ChiTietHopDongBanHang` | `sal_hop_dong_ban_hang_chi_tiet` | `sal_chi_tiet_hop_dong_ban_hang` |
| `ChiTietChungTuBan` | `sal_chung_tu_ban_hang_chi_tiet` | `sal_chi_tiet_chung_tu_ban_hang` |
| `NguoiKiemKeCCDC` | `ccdc_phieu_kiem_ke_nguoi_kiem_ke` | `ccdc_chi_tiet_nguoi_kiem_ke` |
| `ChiTietPhieuKTTH_HachToan` | `ktth_phieu_ke_toan_tong_hop_hach_toan` | `ktth_chi_tiet_phieu_ktth_hach_toan` |

**Vai trò mặc định là `chi_tiet`.** Chỉ thay bằng vai trò khác khi bảng cha có **nhiều hơn một** bảng con cần phân biệt:

| Bảng cha | Số bảng con | Vai trò | Kết quả |
|---|---:|---|---|
| `SoDuBanDauKhachHang` | 1 | `chi_tiet` | `sdbd_so_du_ban_dau_khach_hang_chi_tiet` |
| `SoDuBanDauNCC` | 1 | `chi_tiet` | `sdbd_so_du_ban_dau_nha_cung_cap_chi_tiet` |
| `PhieuKeToanTongHop` | 2 | `hach_toan` · `hoa_don` | `ktth_phieu_ke_toan_tong_hop_hach_toan` · `…_hoa_don` |
| `PhieuDanhGiaLaiNgoaiTe` | 3 | `so_du` · `cong_no` · `hach_toan` | `fx_phieu_danh_gia_lai_ngoai_te_so_du` · … |
| `PhieuKiemKeCCDC` | 3 | `chi_tiet` · `don_vi` · `nguoi_kiem_ke` | `ccdc_phieu_kiem_ke_chi_tiet` · `…_don_vi` · `…_nguoi_kiem_ke` |

> Hậu tố trong tên entity LDM (`ChiTietSDBD_KH_**HoaDon**`) **không** tự động thành vai trò — nó chỉ mô tả nội dung dòng. Khi cha chỉ có một bảng con thì vai trò vẫn là `chi_tiet`.

**Luật 2 — không viết tắt trong phần nghiệp vụ, không lặp tiền tố module:**

| Viết tắt | Giãn thành | | Lặp tiền tố module | Bỏ |
|---|---|---|---|---|
| `tscd` | `tai_san_co_dinh` | | `ccdc_phieu_kiem_ke_ccdc` | `ccdc_phieu_kiem_ke` |
| `tk` | `tai_khoan` | | `ccdc_tam_dung_phan_bo_ccdc` | `ccdc_tam_dung_phan_bo` |
| `ncc` | `nha_cung_cap` | | `ccdc_don_vi_quan_ly_ccdc` | `ccdc_don_vi_quan_ly` |
| `kh` | `khach_hang` | | `inv_phieu_nhap_kho_module_kho` | `inv_phieu_nhap_kho` |
| `hd` | `hoa_don` | | `ktth_chi_tiet_phieu_**ktth**_hach_toan` | `ktth_phieu_ke_toan_tong_hop_hach_toan` |
| `dv` | `dich_vu` | | `sdbd_chi_tiet_**sdbd**_tai_khoan` | `sdbd_so_du_ban_dau_tai_khoan_chi_tiet` |
| `nvl` | `nguyen_vat_lieu` | | | |

Prefix module (`fa_`, `ccdc_`, `ktth_`, `cptt_`, `sdbd_`) **giữ nguyên** vì là mã module, không phải viết tắt nghiệp vụ.

**Ngoại lệ — giữ nguyên vì là mã chuẩn ngoài hệ thống:** `gtgt` · `khbs` · `01_6` · `04_gtgt` (mã tờ khai / phụ lục thuế do cơ quan thuế quy định).

> Cột **"Bảng đề xuất"** trong các file đặc tả **đã áp dụng** hai luật này. Cột **"Bảng hiện có"** là tên đang chạy trong DB. Hai cột khác nhau ⇒ bảng đó nằm trong đợt rename — **74 bảng** có tên đề xuất khác tên đang chạy, phần lớn do vi phạm luật 1.

---

## 2. Đặt tên cột

| Loại | Quy tắc | Ví dụ |
|---|---|---|
| Khóa chính | `id` | `id` |
| Khóa ngoại | `<thực_thể>_id` | `nha_cung_cap_id` · `vat_tu_id` · `don_vi_tinh_id` |
| Snapshot tên đi kèm FK *(Rule 2)* | `ten_<thực_thể>` | `ten_nha_cung_cap` · `ten_vat_tu` |
| Ngày (không giờ) | tiền tố `ngay_` | `ngay_chung_tu` · `ngay_hach_toan` |
| Mốc thời gian (có giờ) | tiền tố `thoi_gian_` | `thoi_gian_ghi_so` |
| Số tiền | hậu tố mô tả bản chất — **cấm** `so_tien` trần | `thanh_tien_xuat` · `tong_tien_thanh_toan` |
| Số tiền quy về đồng hạch toán | hậu tố `_quy_doi` — **không** dùng `_vnd` | `thanh_tien_quy_doi` |
| Số lượng | tiền tố `so_luong_` | `so_luong_xuat` · `so_luong_ton` |
| Cờ boolean | tiền tố `is_` / `cho_phep_` / `da_` | `is_auto` · `cho_phep_sua` · `da_ghi_so` |
| Trạng thái vòng đời chứng từ | `status` | `status` |

**Nguyên tắc bất biến — một khái niệm ⇒ một tên cột xuyên suốt.** `vat_tu_id` phải giống hệt ở `sal_chung_tu_ban_hang_chi_tiet`, `inv_phieu_xuat_kho_chi_tiet`, `acc_so_cai`, `acc_so_kho`.

> Đang vi phạm: `ma_hang_id` (bán hàng) vs `vat_tu_id` (mua hàng) cho cùng một thứ; `ma_don_vi_id`/`ma_vu_viec_id`/`ma_doi_tuong_id` (sổ cái) vs `don_vi_id`/`vu_viec_id`/`doi_tuong_id` (nơi khác).

**Ngoại lệ Rule 2 đã chốt trong LDM:** `tk` / `tk_doi_ung` / `tk_vat_tu` / `tk_gia_von` — sổ cái và sổ kho **có** lưu mã tài khoản, vì mã TK là định danh in trên sổ sách và không được đổi khi đã phát sinh.

---

## 3. Bộ trường base

### 3.1 Bốn tầng base class *(đã có sẵn ở `cell-app/.../core/entity/` — không dựng lại)*

| Base class | Cột mang theo |
|---|---|
| `BaseEntity` | `id` · `ngay_tao` · `ngay_cap_nhat` · `da_xoa` · `ngay_xoa` · `nguoi_tao` · `nguoi_cap_nhat` · `nguoi_xoa` |
| `TenantedEntity` *(extends BaseEntity)* | `tenant_id` |
| `AggregateRootEntity` *(extends TenantedEntity)* | `phien_ban` (`@Version`) |
| `BaseChungTuEntity` *(extends AggregateRootEntity)* | `chi_nhanh_id` · `loai_chung_tu_id` · `giao_dich_chung_tu_id` · `so_chung_tu` · `ngay_chung_tu` · `ngay_hach_toan` · `status` · `nguoi_duyet_id` · `ngay_duyet` · `nguoi_ghi_so` · `thoi_gian_ghi_so` |
| `BaseChiTietChungTuEntity` *(extends TenantedEntity)* | `thu_tu` + `getChungTuId()` abstract |

### 3.2 Loại bảng nào dùng base nào

| Loại bảng | Base | Cột riêng bắt buộc khai thêm |
|---|---|---|
| Header chứng từ | `BaseChungTuEntity` | trường nghiệp vụ |
| Dòng chi tiết | `BaseChiTietChungTuEntity` | `<cha>_id` NOT NULL + FK `ON DELETE CASCADE` |
| Bảng cháu (người kiểm kê, đơn vị được kiểm kê…) | `TenantedEntity` | `<cha>_id` NOT NULL + FK |
| **Bảng sổ** (`acc_so_cai`, `acc_so_kho`) | `TenantedEntity` + `@Immutable` | `chi_nhanh_id` · `is_auto` · `nguoi_ghi_so` · `thoi_gian_ghi_so` · `request_hash` |
| Bảng kết quả / snapshot (`inv_ton_kho`, `CostLayer`…) | `TenantedEntity` | — |
| Cấu hình (`cfg_*`, `iam_tenant`) | `AggregateRootEntity` | — |
| Bảng link N-N | `TenantedEntity` | UNIQUE trên cặp khóa |

> ⚠ Entity chứng từ **không được** khai `@AttributeOverride` đổi tên cột thời gian sang `thoi_gian_*`. `ddl-auto: none` nên Hibernate không đối chiếu cột lúc khởi động — sai tên cột thì app vẫn boot, test vẫn xanh, chỉ vỡ khi người dùng mở màn hình. Đã phải rút lại một lần (V345–V349 → V351).

### 3.3 Bốn cách đặt tên trường base đang tồn tại — **Q1 phải chốt**

| Khái niệm | BR46 | Header LDM nhóm 1 ¹ | Header LDM nhóm 2 ² | **Cột DB đang chạy** |
|---|---|---|---|---|
| Cờ xóa mềm | `DaXoa` | `DaXoa` | `IsDeleted` | `da_xoa` |
| Người xóa | `NguoiXoaId` | `NguoiXoa` | — | `nguoi_xoa` |
| Thời điểm xóa | `NgayXoa` | `ThoiGianXoa` | `DeletedAt` | `ngay_xoa` |
| Người tạo | `NguoiTaoId` | `NguoiTao` | `CreatedBy` | `nguoi_tao` |
| Thời điểm tạo | `NgayTao` | `ThoiGianTao` | `CreatedAt` | `ngay_tao` |
| Người sửa | `NguoiCapNhatId` | `NguoiCapNhat` | `UpdatedBy` | `nguoi_cap_nhat` |
| Thời điểm sửa | `NgayCapNhat` | `ThoiGianCapNhat` | `UpdatedAt` | `ngay_cap_nhat` |
| Người ghi sổ | `NguoiGhiSoId` | `NguoiGhiSo` | — | `nguoi_ghi_so` |
| Thời điểm ghi sổ | `ThoiGianGhiSo` | `ThoiGianGhiSo` | — | `thoi_gian_ghi_so` |

¹ `ldm-DanhGiaLaiNgoaiTe` · `ldm-GiaThanh` · `ldm-KetChuyenLaiLo` — dẫn chiếu BR46 nhưng viết tên khác BR46.
² `ldm-BanHang-Update` · `ldm-Authentication`.

**Toàn bộ đặc tả trong thư mục này đang dùng cột DB đang chạy** (cột phải cùng). Nếu chốt ngược lại thì phải sinh lại toàn bộ và tính thêm một đợt migration đổi tên cột trên 237 bảng.

### 3.4 `tenant_id` / `chi_nhanh_id` — BR46.4

| Trường | Bắt buộc ở | Ràng buộc |
|---|---|---|
| `tenant_id` | **Mọi** bảng nghiệp vụ | NOT NULL · `updatable = false` · gán từ `TenantContext` lúc persist · khóa của RLS policy `tenant_isolation` · **cấm** tham chiếu chéo tenant |
| `chi_nhanh_id` | Bảng **gốc do người dùng lập** | **Không** tự gán từ context — chứng từ điều chuyển hợp lệ khi lập cho chi nhánh khác. Service phải `setChiNhanhId()` tường minh và kiểm quyền theo phạm vi đơn vị (`iam_tai_khoan_quyen_don_vi` / `iam_pham_vi_hieu_luc`) |

Bảng **dẫn xuất** (`inv_ton_kho`, `CostLayer`) không mang `chi_nhanh_id` — suy ra từ `Kho`.
Bảng **chi tiết** thừa hưởng nghiệp vụ qua bảng cha nhưng **vẫn mang `tenant_id`** vì RLS bám cột này.

---

## 4. Kiểu dữ liệu — domain type theo BR7

DB đã có sẵn 5 domain, **bắt buộc dùng**, cấm khai `numeric(x,y)` trần:

```sql
CREATE DOMAIN public.money_vnd     AS numeric(18,2);  -- Tiền theo đồng hạch toán
CREATE DOMAIN public.money_foreign AS numeric(18,4);  -- Tiền nguyên tệ
CREATE DOMAIN public.exchange_rate AS numeric(18,6);  -- Tỷ giá, hệ số quy đổi
CREATE DOMAIN public.quantity      AS numeric(18,3);  -- Số lượng
CREATE DOMAIN public.percent_rate  AS numeric(5,2);   -- Phần trăm, thuế suất
```

| Kiểu LDM | Kiểu DB | Ghi chú |
|---|---|---|
| `uuid` | `uuid` | FK đa hình (`chung_tu_id`, `chi_tiet_chung_tu_id`) **không** ràng buộc FK ở DB |
| `string` | `text` | Trừ số chứng từ / mã danh mục: `varchar(50)` theo BR20 |
| `date` | `date` | |
| `datetime` | `timestamptz` | |
| `boolean` | `boolean` | NOT NULL DEFAULT `false` |
| `enum` | `text` + `CHECK` | **Không** dùng enum native Postgres (thêm giá trị phải `ALTER TYPE`). JPA: `@Enumerated(STRING)` |
| `numeric` tiền nguyên tệ | `money_foreign` | |
| `numeric` tiền quy đổi (`*QuyDoi`) | `money_vnd` | Tên domain giữ `_vnd` vì đã dùng rộng; nghĩa là "đồng tiền hạch toán" |
| `numeric` số lượng | `quantity` | |
| `numeric` tỷ giá / hệ số quy đổi | `exchange_rate` | |
| `numeric` % · thuế suất | `percent_rate` | |
| `numeric` STT · số dòng · số ngày | `integer` | |

**NOT NULL DEFAULT 0:** LDM quy định *"mọi trường numeric đều NOT NULL, mặc định 0"*. Đặc tả áp dụng cho **bảng mới**. Với `acc_so_cai` đang chạy (code ghi `null` ở vế đối ứng), đổi sang NOT NULL là **thay đổi phá vỡ** — xếp riêng vào Pha 5, không làm lẻ.

**Ngoại lệ NULL đã chốt trong LDM Kho:** `ty_le_phan_bo` (ở `inv_phieu_nhap_kho_chi_tiet`, `ThanhPhamSauLapRapThaoDo`, `ChiTietDinhMucNVL`) để NULL — NULL nghĩa là dòng **không tham gia phân bổ**, khác hẳn tỷ lệ bằng 0.

### 4.1 Ký hiệu suy luận kiểu trong các file đặc tả

| Ký hiệu | Nghĩa | Số lượng |
|---|---|---:|
| *(không có)* | Kiểu suy trực tiếp từ kiểu LDM — tin được | ~2.300 |
| `≈` | Kiểu suy **theo tên trường** (ví dụ tên chứa `TongTien` ⇒ `money_foreign`) — nên soát | 383 |
| `⚠` | **Không suy được** — đang tạm để `numeric(18,4)`, **phải chốt tay** | 60 |

---

## 5. Hạ tầng bắt buộc trên mỗi bảng

| # | Mục | Chuẩn |
|---|---|---|
| 1 | Khóa chính | `id uuid NOT NULL DEFAULT gen_random_uuid()`; bảng partition: PK gồm cả khóa phân vùng |
| 2 | RLS | `ENABLE ROW LEVEL SECURITY` + `FORCE` + policy `tenant_isolation` → `fn_current_tenant()` |
| 3 | Trigger audit | `trg_audit_<bảng>` → `fn_audit` |
| 4 | Index dẫn đầu tenant | `(tenant_id, …) WHERE da_xoa = false` |
| 5 | FK cha–con | `ON DELETE CASCADE` cho bảng chi tiết; **không** đặt FK cho liên kết đa hình |
| 6 | Kiểm trùng (BR19) | UNIQUE `(tenant_id, so_chung_tu)` cho chứng từ · `(tenant_id, ma)` cho danh mục — partial `WHERE da_xoa = false` |
| 7 | Comment | `COMMENT ON TABLE` + `COMMENT ON COLUMN` lấy **nguyên văn** mô tả từ LDM |

Riêng **bảng sổ** thêm:

| # | Mục | Chuẩn |
|---|---|---|
| 8 | Partition | `PARTITION BY RANGE(ngay_hach_toan)` + partition `_default` |
| 9 | Idempotency | cột `request_hash` + UNIQUE trên **cột trần** (partition không nhận unique index dạng biểu thức/partial) |
| 10 | Trigger immutable | chặn UPDATE dòng sổ |
| 11 | Trigger period-guard | chặn ghi vào kỳ đã khóa (BR17) |

---

## 6. Cách đọc một file đặc tả

Mỗi file mở đầu bằng **"Phân hệ này phục vụ nghiệp vụ gì"** — phạm vi nghiệp vụ và epic nguồn của cả phân hệ, lấy nguyên văn từ header `.puml`.

Mỗi bảng gồm 5 khối:

| Khối | Nội dung | Nguồn |
|---|---|---|
| **Đầu bảng** | Entity LDM · base class · nhóm · bảng hiện có | Suy từ LDM + khảo sát DB |
| **Mục đích & phạm vi nghiệp vụ** | Bảng này dùng để làm gì · vai trò trong mô hình · đơn vị 1 dòng · bảng cha/con · epic | Mô tả LDM + suy từ vai trò |
| **Trường nghiệp vụ** | Từng trường LDM → cột DB → kiểu → NULL → mặc định → mô tả | **Nguyên văn LDM** |
| **Trường base** | Cột hệ thống tự quản lý, không hiển thị trên form (BR46) | §3 tài liệu này |
| **Đối chiếu** | Cột LDM có mà DB thiếu · cột DB có mà LDM không khai | Diff tự động |

Năm **vai trò** một bảng có thể mang, quyết định cách nó được ghi và ai được ghi:

| Vai trò | Ai ghi | Đặc trưng |
|---|---|---|
| **Đầu chứng từ (header)** | Người dùng, qua màn hình nghiệp vụ | Ghi sổ ⇒ sinh bút toán `acc_so_cai` (+ `acc_so_kho` nếu có dòng vật tư). Khóa sửa/xóa sau ghi sổ (BR12 · BR42) |
| **Dòng chi tiết** | Theo chứng từ cha | `ON DELETE CASCADE`. Một dòng sinh ≥1 bút toán, phân biệt bằng `stt_but_toan` |
| **Sổ kế toán** | **Chỉ kernel ghi sổ** | Append-only · `@Immutable` · partition theo `ngay_hach_toan`. Nguồn duy nhất cho mọi báo cáo |
| **Bảng cấu hình / thiết lập** | Người dùng, khai một lần | Không phát sinh bút toán; nghiệp vụ đọc để lấy tham số khi lập và khi ghi sổ |
| **Bảng kết quả / số dư luân chuyển** | Hệ thống tính | Cập nhật tại chỗ sau mỗi lần ghi sổ hoặc chạy tính theo kỳ. Dùng tra cứu nhanh, **không** thay sổ gốc |
| **Bảng liên kết N–N** | Theo bản ghi cha | Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa |

Nhóm:

| Nhóm | Nghĩa | Cách xử lý | Chi phí |
|---|---|---|---|
| **A** | Có LDM · có schema · **có code** | `ALTER` + sửa entity + sửa FE + migrate dữ liệu | **Cao** |
| **B** | Có LDM · có schema · **chưa có code** | `ALTER` / `DROP+CREATE` tự do, chưa có dữ liệu thật | **Thấp** |
| **C** | Có LDM · **chưa có schema** | `CREATE TABLE` mới theo đúng chuẩn | Thấp |
| **?** | Chưa rà được | Pha 1 đối chiếu tay | — |

> Cột **"DB có — LDM không khai"** trong khối Đối chiếu **không** đồng nghĩa "phải xóa cột". Có ba khả năng: (a) cột hạ tầng không thuộc LDM — giữ; (b) LDM đặt tên khác cho cùng khái niệm — đổi tên; (c) cột chết — DROP. Phải phân loại tay từng cột.

---

## 7. Sinh lại

Toàn bộ file `1x-…` … `8x-…` và `90-doi-chieu.md` **sinh tự động từ `.puml`** — sửa LDM rồi sinh lại, **không sửa tay**.

Chỉ hai file được viết tay: `00-chuan-chung.md` (file này) và `README.md`.
