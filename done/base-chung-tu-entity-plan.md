# `BaseChungTuEntity` / `BaseChiTietChungTuEntity` — kế hoạch & tình trạng

> **v5 — ĐÃ TRIỂN KHAI ĐỢT 1 + ĐỢT 2 (luồng bán hàng).** Phần §5 ghi rõ việc đã làm và việc còn lại.
> Đợt 1: các bảng chứng từ CHƯA CÓ CODE NGHIỆP VỤ (V304–V308).
> Đợt 2 (§6): luồng Chứng từ bán hàng — hạng mục H của đợt 1 (V309).
> `cell-app`. Cập nhật: 2026-08-03.

---

## 1. Phạm vi

### 1.1 Trong phạm vi — 74 bảng

| Module | Prefix | Header | Detail |
|---|---|---|---|
| Bán hàng | `sal_` | 4 | 5 |
| Mua hàng | `pur_` | 6 | 5 |
| Kho | `inv_` | 7 | 7 |
| TSCĐ | `fa_` | 6 | 9 |
| CCDC | `ccdc_` | 5 | 6 |
| Tiền mặt / Ngân hàng | `cb_` | 2 | 2 |
| Chi phí trả trước | `cptt_` | 1 | 1 |
| Giá thành | `cst_` | 2 | 3 |
| KT tổng hợp | `ktth_` | 1 | 2 |
| **Tổng** | | **34** | **40** |

Danh sách đầy đủ: [Phụ lục A](#phụ-lục-a--danh-sách-74-bảng).

### 1.2 Ngoài phạm vi

| Nhóm | Bảng | Lý do |
|---|---|---|
| **Luồng Chứng từ bán hàng** | `sal_chung_tu_ban_hang`, `sal_chi_tiet_chung_tu_ban_hang` | **Đã có code nghiệp vụ đang chạy** (entity + service + màn FE). Đổi tên cột sẽ vỡ mapping — tách ticket riêng kèm test hồi quy |
| Sổ cái | `acc_so_cai`, `acc_so_cai_2025…2028`, `acc_so_cai_default` | **Sổ**, không phải chứng từ. Bất biến theo thiết kế (`trg_acc_so_cai_immutable`) |
| Sổ thuế, sổ kho tổng hợp | `acc_so_thue_dau_ra/vao`, `acc_so_xuat_nhap_tong_hop` | Sổ / bảng kê |
| Số dư ban đầu | `sdbd_*` | Khai báo đầu kỳ, không có vòng đời duyệt/ghi sổ |
| Bảng liên kết | `*_lien_ket_chung_tu`, `*_chung_tu_lien_quan` | Junction table |
| Danh mục, IAM, báo cáo | `mst_*`, `iam_*`, `agg_*`, `rpt_*` | Không phải chứng từ |
| Đã bị xoá | `am_chung_tu_phan_bo_chi_phi` | `DROP` ở V127 (đổi tên sang `ccdc_`/`cptt_`) |
| Chưa rõ phân loại | `cptt_chung_tu_goc_khai_bao` | ❓ Cần BA xác nhận có phải chứng từ không |

### 1.3 Phạm vi phần code

68 entity toàn `cell-app`, trong đó chỉ **2** map tới 76 bảng chứng từ — cả hai thuộc luồng bán
hàng, và cả hai **nằm ngoài phạm vi** theo yêu cầu. ⇒ 74 bảng trong phạm vi **không có entity nào**.

Phần code của đợt này vì thế là **dựng sẵn 2 lớp base cho các luồng sắp code hoá**, không phải sửa
code đang chạy. Rủi ro hồi quy gần bằng 0.

### 1.4 Ảnh hưởng đã đo

| Hạng mục | Số lượng |
|---|---|
| Entity Java phải sửa | **0** |
| Index dùng cột `ngay_tao/ngay_cap_nhat/ngay_xoa` trên 74 bảng | **0** |
| View / function / trigger chạm 74 bảng | **0** |
| Native SQL / JPQL hard-code cột đổi tên | **0** — 20 chỗ hard-code đều ở `master_data` |
| File seed test phải sửa | **24** |
| Chỗ FE phải sửa | **0** |

---

## 2. Quyết định đã chốt

### 2.1 `GiaoDichChungTuID` → bảng master

Chọn **bảng `mst_giao_dich_chung_tu`** (toàn cục, không tenant/RLS, cùng kiểu `mst_loai_chung_tu`).
Lý do: spec đặt tên trường có hậu tố `ID`, và phân loại này thuộc về sản phẩm chứ không thuộc từng
công ty nên không nhân bản theo tenant.

> ⚠️ **Seed hiện tại là tập TỐI THIỂU** — 31 dòng, mỗi luồng chứng từ một giao dịch. Danh mục nghiệp
> vụ đầy đủ (tách trong nước / nhập khẩu / nội bộ…) **vẫn chờ BA**. Bổ sung bằng migration mới,
> không sửa V304.
>
> ⚠️ Cần BA làm rõ quan hệ với `mst_ly_do_nhap_xuat.loai_giao_dich` (`NhapKho`/`XuatKho`) và
> `cap_giao_dich` đang có sẵn, tránh hai chiều dữ liệu song song.

### 2.2 `Status` → 5 giá trị, lưu tên hằng

```
NHAP → CHO_DUYET → DA_DUYET → DA_GHI_SO → (HUY)
```

Lưu **tên hằng ASCII** (`'DA_GHI_SO'`) trong cột `text` + `CHECK`, không dùng `enum` native
PostgreSQL (thêm giá trị sẽ phải `ALTER TYPE`), cũng không dùng chuỗi tiếng Việt như
`trang_thai_chung_tu` của V75 — cột `status` là cột mới nên không bị ràng buộc bởi CHECK cũ, và tên
hằng bỏ được hẳn tầng converter.

> ⚠️ Tập giá trị này **do tôi đề xuất**, chưa có BA duyệt. Nếu vòng đời thật khác, sửa CHECK +
> enum Java là đủ — chưa có dữ liệu nào dùng.

### 2.3 Tên cột thời gian → `@AttributeOverride`

Spec yêu cầu `thoi_gian_tao / thoi_gian_cap_nhat / thoi_gian_xoa`; `BaseEntity` map `ngay_*` cho
toàn bộ entity còn lại. Giải: override **tên cột** tại 2 lớp base, giữ nguyên **tên field**.

Nhờ vậy: 66 entity ngoài phạm vi không phải sửa; callback `@PrePersist`/`@PreUpdate` của lớp cha
thao tác trên field nên chạy y nguyên; alias `@SearchableAudit` mà FE đang lọc/sắp xếp (`ngayTao`)
bám tên field nên hợp đồng API không đổi. Khi làm đợt đổi tên tổng sau này, chỉ việc đổi tại
`BaseEntity` rồi xoá dần các override.

### 2.4 `phien_ban` — giữ, dù không có trong spec

Là `@Version`, chống hai người ghi đè nhau khi cùng sửa một chứng từ. Coi là trường kỹ thuật ngoài
spec nghiệp vụ. Do đó `BaseChungTuEntity` kế thừa `AggregateRootEntity`.

### 2.5 FK của bảng detail — không đổi tên

40 bảng detail đang đặt tên FK khác nhau (`chung_tu_ban_hang_id`, `dieu_chuyen_id`,
`phieu_kiem_ke_ccdc_id`…). Đổi tên sẽ phá khoá ngoại và index đang chạy. Lớp cha chỉ khai
`abstract getChungTuId()`; bảng detail **mới** thống nhất `chung_tu_id`.

---

## 3. Thiết kế

```
BaseEntity → TenantedEntity → SoftDeletableEntity → AggregateRootEntity
                                      │                      │
                                      │                      └→ BaseChungTuEntity        (MỚI)
                                      └→ BaseChiTietChungTuEntity                        (MỚI)
```

### 3.1 `BaseChungTuEntity extends AggregateRootEntity`

| Field Java | Cột | Kiểu |
|---|---|---|
| `chiNhanhId` | `chi_nhanh_id` | UUID |
| `loaiChungTuId` | `loai_chung_tu_id` | UUID |
| `giaoDichChungTuId` | `giao_dich_chung_tu_id` | UUID |
| `soChungTu` | `so_chung_tu` | text(50) |
| `ngayChungTu` | `ngay_chung_tu` | date |
| `ngayHachToan` | `ngay_hach_toan` | date |
| `status` | `status` | enum STRING |
| `nguoiDuyetId` / `ngayDuyet` | `nguoi_duyet_id` / `ngay_duyet` | UUID / timestamptz |
| `nguoiGhiSo` / `thoiGianGhiSo` | `nguoi_ghi_so` / `thoi_gian_ghi_so` | UUID / timestamptz |

Kế thừa: `id`, `tenant_id`, `phien_ban`, `da_xoa`, `nguoi_tao/cap_nhat/xoa`, và 3 cột thời gian đã
remap.

Hành vi: `duyet()` / `boDuyet()`, `ghiSo()` / `boGhiSo()`, `daDuyet()`, `daGhiSo()`, `choPhepSua()`.

Hai điểm bám quy ước sẵn có của codebase:
- **Không gọi `Instant.now()` trong entity** — lint P0-D13 cấm đọc đồng hồ tường trong mã nghiệp vụ,
  và entity không inject được `Clock`. Mốc `ngay_duyet` / `thoi_gian_ghi_so` đóng ở `@PreUpdate`
  bằng cách lấy lại `getNgayCapNhat()` mà `BaseEntity.onUpdate()` vừa đóng. Callback lớp cha chạy
  trước lớp con nên giá trị đã sẵn sàng, và các mốc khớp nhau thay vì lệch vài mili giây. Đây đúng
  là cách `SoftDeletableEntity.dongDauNgayXoa()` đang làm.
- **Không tự gán `chiNhanhId` từ context.** `TenantContext` hiện chỉ mang `tenantId`/`userId`, chưa
  có chi nhánh. Và ngay cả khi có, chứng từ điều chuyển vẫn hợp lệ khi lập cho chi nhánh khác —
  quyền theo chi nhánh nằm ở `iam_nguoi_dung_chi_nhanh`, phải kiểm ở tầng service. Tenant thì khác:
  là khoá cách ly RLS, lệch là rò dữ liệu, nên `TenantedEntity` mới chặn. ⇒ **service tạo chứng từ
  phải `setChiNhanhId(...)` tường minh.**

### 3.2 `BaseChiTietChungTuEntity extends SoftDeletableEntity`

`stt` + `abstract getChungTuId()` + cùng bộ `@AttributeOverride`. **Không** khai `@Version` —
optimistic lock đặt ở header; hai `@Version` sẽ tạo hai mốc phiên bản cạnh tranh trên cùng một lần
lưu. Sửa chỉ chạm dòng con thì header gọi `touch()`.

---

## 4. Migration

| File | Nội dung |
|---|---|
| `V304__mst_giao_dich_chung_tu_va_helper_doi_ten_cot.sql` | Master `mst_giao_dich_chung_tu` + seed 31 dòng + helper `fn_doi_ten_cot_neu_can` |
| `V305__chung_tu_chuan_cot_sal_pur.sql` | 10 header + 10 detail |
| `V306__chung_tu_chuan_cot_inv.sql` | 7 + 7 |
| `V307__chung_tu_chuan_cot_fa_ccdc.sql` | 11 + 15 |
| `V308__chung_tu_chuan_cot_cb_cst_cptt_ktth.sql` | 6 + 8 |

Ba quyết định kỹ thuật trong DDL:

1. **Danh sách bảng khai tường minh**, không quét động theo pattern tên bảng — quét động tóm nhầm
   `acc_so_cai_*` và `sdbd_*` (có `so_chung_tu` nhưng là SỔ). Bảng khai sai tên thì
   `RAISE EXCEPTION` dừng migration chứ không bỏ qua im lặng.
2. **Đổi tên trước, thêm cột sau.** Nếu thêm `stt` trước thì lệnh `RENAME thu_tu → stt` sẽ đụng cột
   vừa tạo. Helper `fn_doi_ten_cot_neu_can` bỏ qua khi không có gì để đổi, nhưng **dừng** khi cả tên
   cũ lẫn tên mới cùng tồn tại — tình huống đó phải gộp dữ liệu bằng tay, chọn bừa một cột là mất
   dữ liệu im lặng.
3. **Cột để NULL, `CHECK` đặt `NOT VALID`.** Siết ràng buộc ngay sẽ chặn dữ liệu cũ. `CHECK NOT VALID`
   vẫn áp cho mọi dòng INSERT/UPDATE mới — đã kiểm chứng — chỉ bỏ qua dòng cũ.

Mỗi file kết thúc bằng khối kiểm chứng đọc `information_schema.columns`, `RAISE EXCEPTION` nếu thiếu
cột.

---

## 5. Tình trạng

### ✅ Đã làm

| # | Việc | Kết quả |
|---|---|---|
| 1 | `core/entity/TrangThaiChungTu.java` | 5 giá trị + `choPhepSua()` |
| 2 | `core/entity/BaseChungTuEntity.java` | 11 cột + 7 hành vi vòng đời |
| 3 | `core/entity/BaseChiTietChungTuEntity.java` | `stt` + `abstract getChungTuId()` |
| 4 | 5 file migration V304–V308 | 74 bảng |
| 5 | Sửa 24 file seed test | 63 tham chiếu cột |

**Kiểm chứng đã chạy:**
- `./gradlew build` (cell-app) — **BUILD SUCCESSFUL**. Checkstyle: 13 warning trên 10 file, **toàn
  bộ là code cũ**, không file nào của đợt này.
- Flyway chạy **toàn bộ 263 migration** trên PostgreSQL 16 sạch (container tạm) — thành công tới
  v308.
- Kiểm chứng trên DB sau migration: 74 bảng có `thoi_gian_tao`; **0** bảng còn sót `ngay_tao`; 34
  header đủ 8 cột mới; 40 detail có `stt`; 31 dòng seed master.
- Xác nhận `sal_chung_tu_ban_hang` và `sal_chi_tiet_chung_tu_ban_hang` **giữ nguyên** `ngay_tao` /
  `ngay_cap_nhat` / `ngay_xoa` / `thu_tu`, không có `status` / `stt` — đúng yêu cầu loại trừ.
- Chạy lại 4 file seed đại diện (`tscd-ghi-giam`, `ccdc-kiem-ke`, `chung-tu-mua-hang`,
  `cash-vouchers`) trên schema mới — OK.
- Smoke test: INSERT `status = 'DA_GHI_SO'` thành công; INSERT `status = 'RAC'` bị
  `ck_..._status` chặn đúng.

### ⏳ Còn lại

| # | Việc | Chặn bởi |
|---|---|---|
| A | Seed đầy đủ `mst_giao_dich_chung_tu` | BA chốt danh mục giao dịch (§2.1) |
| B | Xác nhận tập giá trị `Status` | BA (§2.2) |
| C | Phân loại `cptt_chung_tu_goc_khai_bao` | BA (§1.2) |
| D | Backfill `chi_nhanh_id` / `status`; `SET NOT NULL`; FK; index `(tenant_id, chi_nhanh_id, ngay_hach_toan)`; `VALIDATE CONSTRAINT` | Sau khi các luồng bắt đầu ghi dữ liệu |
| E | Rule ArchUnit chặn entity chứng từ khai lại `ngay_*` | — |
| ~~F~~ | ~~Unit test cho 2 lớp base~~ | ✅ Xong ở đợt 2 (`VongDoiChungTuBanHangTest`) |
| G | `SoChungTuService` nhận `(loaiChungTuId, chiNhanhId, nam)`; helper duyệt/ghi sổ ra `core`; `BaseRepository` filter `chi_nhanh_id` | — |
| ~~H~~ | ~~**Chuyển luồng bán hàng sang base**~~ | ✅ Xong ở đợt 2 — xem §6 |

### ⚠️ Chưa kiểm chứng

- **Chưa test trên dữ liệu production.** Chỉ chạy trên DB rỗng dựng từ migration. Trước khi deploy
  thật phải chạy lại trên bản dump có dữ liệu và đối chiếu số bản ghi trước/sau từng bảng.
- **Repo không có test Flyway tự động** (không có Testcontainers). Việc kiểm chứng ở trên là thủ
  công bằng container tạm — nên bổ sung thành test tự động (hạng mục riêng).
- 20 file seed còn lại chưa chạy thử, chỉ 4 file đại diện.

---

## 6. Đợt 2 — luồng Chứng từ bán hàng (hạng mục H)

Hai bảng `sal_chung_tu_ban_hang` / `sal_chi_tiet_chung_tu_ban_hang` nay đã vào chuẩn. Tổng cộng
**76/76 bảng chứng từ** dùng chung một bộ cột.

### 6.1 Quyết định chốt: hợp nhất trạng thái, KHÔNG giữ song song

`trang_thai_chung_tu` (2 giá trị chuỗi tiếng Việt, CHECK của V75) bị **DROP**; nguồn sự thật duy
nhất là `status` của lớp cha. Ánh xạ dữ liệu: `'Chưa ghi sổ' → NHAP`, `'Đã ghi sổ' → DA_GHI_SO`.

Phương án thay thế đã cân nhắc và loại: giữ cả hai cột, `status` là nguồn sự thật còn
`trang_thai_chung_tu` thành cột dẫn xuất cho FE cũ. Rẻ hơn về hợp đồng API, nhưng để lại hai nguồn
sự thật phải đồng bộ tay ở MỌI nhánh ghi — loại lỗi chỉ lộ ra sau khi số liệu đã sai. FE chưa có màn
bán hàng nên chi phí đổi hợp đồng bằng 0.

### 6.2 Thay đổi hợp đồng API (breaking, đã đo là an toàn)

| Trước | Sau | Ảnh hưởng FE |
|---|---|---|
| `trangThaiChungTu: "Chưa ghi sổ" \| "Đã ghi sổ"` | `status: "NHAP" \| "CHO_DUYET" \| "DA_DUYET" \| "DA_GHI_SO" \| "HUY"` | **0** — `../../client/src/features` chưa có màn bán hàng |
| dòng chi tiết `thuTu` | `stt` | **0** |

Đã cập nhật theo: `PMKT-chung-tu-ban-hang.postman_collection.json` (filter, assertion, mô tả).

### 6.3 Việc đã làm

| # | Việc | Kết quả |
|---|---|---|
| 1 | `V309__sal_ctbh_chuan_cot_chung_tu.sql` | 8 cột header mới + `thu_tu→stt` (numeric→integer) + `ngay_*→thoi_gian_*` + backfill `status` + DROP `trang_thai_chung_tu` + seed `SAL_BAN_HANG` (V304 thiếu vì luồng này ngoài phạm vi đợt 1) |
| 2 | `ChungTuBanHang extends BaseChungTuEntity` | Bỏ 4 field trùng (`soChungTu`, `ngayChungTu`, `ngayHachToan`, `trangThaiChungTu`) + `daGhiSo()` tự khai |
| 3 | `ChiTietChungTuBanHang extends BaseChiTietChungTuEntity` | Bỏ `thuTu`, cài `getChungTuId()` |
| 4 | `@Searchable` chuyển lên `BaseChungTuEntity` | Nếu không, entity con kế thừa xong MẤT bộ lọc số/ngày chứng từ mà không có lỗi biên dịch nào báo |
| 5 | `@PrePersist` đóng dấu mốc duyệt/ghi sổ | "Lưu và ghi sổ" chứng từ MỚI đi thẳng INSERT, `@PreUpdate` không chạy → `thoi_gian_ghi_so` null vĩnh viễn |
| 6 | Service dùng hành vi lớp cha | `ghiSo()` / `boGhiSo()` thay cho gán trạng thái tay ở 3 chỗ |
| 7 | Xoá `chung_tu_ban_hang/internal/model/TrangThaiChungTu.java` | Enum 2 giá trị + converter chuỗi tiếng Việt |
| 8 | `VongDoiChungTuBanHangTest` — 7 ca | Vòng đời + hai nhánh đóng dấu mốc + thứ tự `stt` + `getChungTuId()` |

### 6.4 Cố ý KHÔNG làm

- **Không `@AttributeOverride` để giữ `nullable = false`** cho `so_chung_tu` / `ngay_chung_tu` /
  `ngay_hach_toan` / `stt`. DB vẫn NOT NULL từ V75, và ràng buộc bắt buộc thật sự do
  `KiemTraBanHang` kiểm — nơi duy nhất trả về được mã lỗi nghiệp vụ. Thêm tầng override chỉ để đổi
  thông điệp lỗi không đáng với rủi ro ghi đè nhầm override cột thời gian của lớp cha.
- **Không backfill `chi_nhanh_id` / `loai_chung_tu_id` / `giao_dich_chung_tu_id`** — vẫn NULL, đúng
  như hạng mục D. `TenantContext` chưa mang chi nhánh; gán trị nào là quyết định nghiệp vụ.

### 6.5 Chưa kiểm chứng

- **V309 chưa chạy trên PostgreSQL thật.** Máy phát triển hiện không có Docker và repo chưa có test
  Flyway tự động, nên migration mới chỉ được soát bằng mắt. Trước khi merge phải chạy trên bản dump
  có dữ liệu và đối chiếu: số bản ghi trước/sau, phân bố `status` khớp `trang_thai_chung_tu` cũ.
- Hệ quả: **ánh xạ entity ⇄ schema chưa được Hibernate xác thực** (`ddl-auto: none`). Build xanh chỉ
  chứng minh code biên dịch và unit test đúng, không chứng minh tên cột khớp DB.

---

## Phụ lục A — Danh sách 74 bảng

### Bán hàng `sal_` — 4 H + 5 D
```
H  sal_chung_tu_ban_dich_vu              D  sal_chi_tiet_chung_tu_ban_dv
H  sal_chung_tu_tra_lai_hang_ban         D  sal_chi_tiet_chung_tu_tra_lai_hang_ban
H  sal_dieu_chinh_gia_hang_ban           D  sal_chi_tiet_dieu_chinh_gia_hang_ban
H  sal_dieu_chinh_hoa_don_ban_hang       D  sal_chi_tiet_hoa_don_dieu_chinh
                                         D  sal_chi_tiet_hd_ban_hang
```

### Mua hàng `pur_` — 6 H + 5 D
```
H  pur_chung_tu_mua_hang                 D  pur_chi_tiet_chung_tu_mua_hang
H  pur_chung_tu_tra_lai_hang_mua         D  pur_chi_tiet_chung_tu_tra_lai_hang_mua
H  pur_chung_tu_dieu_chinh_gia_mua       D  pur_chi_tiet_dieu_chinh_gia_mua
H  pur_chung_tu_doi_tru                  D  pur_chi_tiet_chung_tu_doi_tru
H  pur_chung_tu_nhan_hoa_don             D  pur_chi_tiet_hoa_don
H  pur_chung_tu_tham_chieu
```

### Kho `inv_` — 7 H + 7 D
```
H  inv_phieu_nhap_kho_module_kho         D  inv_chi_tiet_phieu_nhap_kho
H  inv_phieu_xuat_kho_module_kho         D  inv_chi_tiet_phieu_xuat_kho
H  inv_phieu_nhap_dieu_chuyen            D  inv_chi_tiet_phieu_nhap_dieu_chuyen
H  inv_phieu_xuat_dieu_chuyen            D  inv_chi_tiet_phieu_xuat_dieu_chuyen
H  inv_phieu_dieu_chuyen_dieu_chinh      D  inv_chi_tiet_phieu_dieu_chuyen_dieu_chinh
H  inv_phieu_kiem_ke                     D  inv_chi_tiet_kiem_ke
H  inv_phieu_nhap_xuat                   D  inv_chi_tiet_ap_gia_xuat_kho
```

### TSCĐ `fa_` — 6 H + 9 D
```
H  fa_chung_tu_ghi_giam_tscd             D  fa_chi_tiet_ghi_giam_tscd
H  fa_chung_tu_ngung_khau_hao            D  fa_chi_tiet_ngung_khau_hao
H  fa_dieu_chinh_tai_san_co_dinh         D  fa_chi_tiet_dieu_chinh_tai_san_co_dinh
H  fa_dieu_chuyen_tai_san                D  fa_chi_tiet_dieu_chuyen
H  fa_khau_hao_tai_san                   D  fa_chi_tiet_khau_hao_tai_san
H  fa_hach_toan_dieu_chinh_tai_san_co_dinh
                                         D  fa_chi_tiet_kiem_ke_tai_san_co_dinh
                                         D  fa_chi_tiet_khai_bao_san_luong
                                         D  fa_thanh_vien_dieu_chinh_tai_san_co_dinh
                                         D  fa_thanh_vien_kiem_ke_tai_san_co_dinh
```

### CCDC `ccdc_` — 5 H + 6 D
```
H  ccdc_phieu_dieu_chinh_ccdc            D  ccdc_chi_tiet_phieu_dieu_chinh_ccdc
H  ccdc_phieu_dieu_chuyen_ccdc           D  ccdc_chi_tiet_phieu_dieu_chuyen_ccdc
H  ccdc_phieu_ghi_giam_ccdc              D  ccdc_chi_tiet_phieu_ghi_giam_ccdc
H  ccdc_phieu_kiem_ke_ccdc               D  ccdc_chi_tiet_kiem_ke_ccdc
H  ccdc_phieu_phan_bo_ccdc               D  ccdc_chi_tiet_phieu_phan_bo_ccdc
                                         D  ccdc_chi_tiet_nguoi_kiem_ke
```

### Tiền mặt / Ngân hàng `cb_` — 2 H + 2 D
```
H  cb_phieu_chi                          D  cb_chi_tiet_phieu_chi
H  cb_phieu_thu                          D  cb_chi_tiet_phieu_thu
```

### Chi phí trả trước `cptt_` — 1 H + 1 D
```
H  cptt_chung_tu_phan_bo_chi_phi         D  cptt_chi_tiet_phan_bo_chi_phi
```

### Giá thành `cst_` — 2 H + 3 D
```
H  cst_chung_tu_gia_thanh                D  cst_chi_tiet_chung_tu_gia_thanh
H  cst_phan_bo_chung_tu                  D  cst_chi_tiet_phan_bo_chi_phi
                                         D  cst_chi_tiet_do_dang_cuoi_ky
```

### KT tổng hợp `ktth_` — 1 H + 2 D
```
H  ktth_phieu_ke_toan_tong_hop           D  ktth_chi_tiet_phieu_ktth_hach_toan
                                         D  ktth_chi_tiet_phieu_ktth_hoa_don
```
