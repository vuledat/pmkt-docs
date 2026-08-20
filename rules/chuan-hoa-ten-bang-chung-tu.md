# Chuẩn hóa tên bảng chứng từ — toàn bộ `cell-app`

> **Trạng thái:** BẢN NHÁP CHỜ USER/DBA CHỐT
> **Ngày khảo sát:** 2026-08-09 · **Migration lớn nhất:** V353 (307 file, 275 bảng)
> **Cập nhật 2026-08-09 (sau họp):** **bỏ yêu cầu tiền tố `chung_tu`.** Phạm vi giảm từ 70 → 52 bảng.
> **Phạm vi:** toàn hệ thống — phương án (a) của DB-Q6 trong
> [10-thiet-ke-db.md](doing/PMKT-E-06194-chung-tu-ban-hang-api/10-thiet-ke-db.md) §2

## 1. Quy ước

```
<module>_<nghiệp vụ>[_<bảng con>]
   │          │            └── chi_tiet · tham_chieu · lien_ket · …
   │          └── viết đầy đủ, không viết tắt, không lặp lại tiền tố module
   └── sal_ · pur_ · inv_ · cb_ · fa_ · ccdc_ · cst_ · cptt_ · ktth_ · am_
```

Hai luật:

1. **`chi_tiet` là hậu tố**, không phải tiền tố — `sal_chi_tiet_chung_tu_ban_hang` → `sal_chung_tu_ban_hang_chi_tiet`. Tên bảng con luôn là `<tên bảng cha>_<vai trò>`.
2. **Không viết tắt, không lặp, không thừa** trong phần nghiệp vụ — `hd` → `hoa_don`, `dv` → `dich_vu`, `tscd` → `tai_san_co_dinh`; bỏ phần lặp lại tiền tố module (`ccdc_phieu_dieu_chinh_ccdc`) và phần thừa vô nghĩa (`inv_phieu_xuat_kho_module_kho`). Tiền tố module (`fa_`, `ccdc_`, `ktth_`, `cptt_`) giữ nguyên vì là mã module, không phải viết tắt nghiệp vụ.

> ~~Luật cũ: bắt buộc tiền tố `chung_tu` ngay sau tiền tố module.~~ **Đã bỏ sau cuộc họp 2026-08-09.**
> Bảng nào **đang có** `chung_tu` trong tên thì **giữ nguyên** (`sal_chung_tu_ban_hang`,
> `pur_chung_tu_mua_hang`, `cst_chung_tu_gia_thanh`…) — "không bắt buộc" không có nghĩa là phải bỏ đi.
> Hệ quả: tên bảng chứng từ sẽ không đồng nhất về mặt có/không có `chung_tu`. Nếu sau này muốn đồng
> nhất theo hướng ngược lại (bỏ hết `chung_tu`), đó là một đợt chuẩn hóa khác — xem **Q-A7**.

**Bảng mới thuộc module quan hệ chứng từ:** `ctu_quan_he_chung_tu` — đặt đúng chuẩn ngay từ đầu nên
không nằm trong danh sách đổi tên. `ctu_` là tiền tố module mới (xem
[thiet-ke-quan-he-chung-tu.md](../done/thiet-ke-quan-he-chung-tu.md) §1.1 và §10-A).

**Không áp dụng cho:** danh mục (`mst_*`), phân quyền (`iam_*`), cấu hình (`cfg_*`), báo cáo
(`rpt_*` — đã dùng hậu tố `_chi_tiet` đúng chuẩn), tổng hợp (`agg_*`, `acc_so_cai*`), audit (`aud_*`),
vận hành (`ops_*`), số dư đầu kỳ (`sdbd_*`), và hồ sơ tài sản (`fa_tai_san_co_dinh`,
`ccdc_cong_cu_dung_cu`) — là hồ sơ, không phải chứng từ, dù có cột `ngay_hach_toan`.

## 2. Khối lượng

| Chỉ số | Sau khi bỏ luật `chung_tu` | *(trước đó)* |
|---|---:|---:|
| Bảng đổi tên | **52** (9 header + 43 chi tiết) | *70* |
| Lượt tham chiếu `.sql` | **1.038** | *1.483* |
| File `.java` phải sửa | **13** | *24* |
| Module Java bị chạm | `chung_tu_ban_hang`, `chung_tu_mua_hang`, **`master_data`** | nt |

🚫 **`master_data/**` là vùng đóng băng** theo `../../CLAUDE.md`. Rename không hoàn tất được nếu không sửa
các native query có tên bảng cứng ở đó (đã biết: `LyDoNhapXuatRepository.java:74` →
`inv_phieu_xuat_kho_module_kho`; `TaiKhoanNganHangRepository.java:30,34` → `cb_phieu_thu`,
`sal_hoa_don_ban_hang`; `MucDichThuChiServiceImpl.java:33`). User **đã đồng ý** sửa `master_data` cho
đợt chuẩn hóa ⇒ gỡ tạm `permissions.deny` trong [.claude/settings.json](../../.claude/settings.json),
khôi phục ngay sau khi PR merge.

> Sau khi bỏ luật `chung_tu`, hai trong ba file trên (`TaiKhoanNganHangRepository`,
> `MucDichThuChiServiceImpl`) **không còn bị ảnh hưởng** — `cb_phieu_thu` và `sal_hoa_don_ban_hang`
> giữ nguyên tên. Chỉ còn `LyDoNhapXuatRepository.java:74` phải sửa.

⚠️ Đây là **đổi tên, không đổi kiến trúc**. Vẫn cấm sao chép pattern/kiến trúc từ `master_data`.

## 3. Bảng header đổi tên (9)

| # | Tên hiện tại | Tên mới | Luật |
|---|---|---|---|
| 1 | `fa_chung_tu_ghi_giam_tscd` | `fa_chung_tu_ghi_giam_tai_san_co_dinh` | 2 — `tscd` |
| 2 | `fa_chung_tu_ghi_giam_tscd_lien_ket_chung_tu` | `fa_chung_tu_ghi_giam_tai_san_co_dinh_lien_ket` | 2 — `tscd` + `_chung_tu` thừa |
| 3 | `inv_phieu_nhap_kho_module_kho` | `inv_phieu_nhap_kho` | 2 — `_module_kho` thừa |
| 4 | `inv_phieu_xuat_kho_module_kho` | `inv_phieu_xuat_kho` | 2 — `_module_kho` thừa |
| 5 | `ccdc_phieu_dieu_chinh_ccdc` | `ccdc_phieu_dieu_chinh` | 2 — lặp `ccdc` |
| 6 | `ccdc_phieu_dieu_chuyen_ccdc` | `ccdc_phieu_dieu_chuyen` | 2 — lặp `ccdc` |
| 7 | `ccdc_phieu_ghi_giam_ccdc` | `ccdc_phieu_ghi_giam` | 2 — lặp `ccdc` |
| 8 | `ccdc_phieu_kiem_ke_ccdc` | `ccdc_phieu_kiem_ke` | 2 — lặp `ccdc` |
| 9 | `ccdc_phieu_phan_bo_ccdc` | `ccdc_phieu_phan_bo` | 2 — lặp `ccdc` |

**Giữ nguyên** (18 header còn lại): `sal_chung_tu_ban_hang`, `sal_chung_tu_ban_dich_vu`,
`sal_chung_tu_tra_lai_hang_ban`, `sal_hoa_don_ban_hang`, `sal_dieu_chinh_gia_hang_ban`,
`sal_dieu_chinh_hoa_don_ban_hang`, `pur_chung_tu_mua_hang`, `pur_chung_tu_doi_tru`,
`pur_chung_tu_dieu_chinh_gia_mua`, `pur_chung_tu_tra_lai_hang_mua`, `pur_chung_tu_nhan_hoa_don`,
`pur_hoa_don_mua`, `cb_phieu_thu`, `cb_phieu_chi`, `cb_phan_bo_cong_no`, `cst_chung_tu_gia_thanh`,
`cst_phan_bo_chi_phi`, `cst_do_dang_cuoi_ky`, `cptt_chung_tu_phan_bo_chi_phi`,
`am_chung_tu_phan_bo_chi_phi`, `fa_chung_tu_ngung_khau_hao`, `fa_dieu_chinh_tai_san_co_dinh`,
`fa_dieu_chuyen_tai_san`, `fa_khau_hao_tai_san`, `fa_khai_bao_san_luong`,
`fa_kiem_ke_tai_san_co_dinh`, `inv_phieu_kiem_ke`, `inv_phieu_nhap_dieu_chuyen`,
`inv_phieu_xuat_dieu_chuyen`, `inv_phieu_dieu_chuyen_dieu_chinh`, `ktth_phieu_ke_toan_tong_hop`.

> **Q-A2 (cũ) đã tự tiêu** — không còn phải chọn giữ hay bỏ chữ `phieu`, vì header nào đang có
> `phieu` thì giữ nguyên.

## 4. Bảng chi tiết đổi tên (43)

Quy tắc máy móc: **tên mới = `<tên bảng cha (sau §3)>_chi_tiet`**.

| # | Tên hiện tại | Tên mới |
|---|---|---|
| 1 | `cb_chi_tiet_phieu_thu` | `cb_phieu_thu_chi_tiet` |
| 2 | `cb_chi_tiet_phieu_chi` | `cb_phieu_chi_chi_tiet` ⚠️ **Q-A8** |
| 3 | `cb_chi_tiet_bang_ke_hoa_don` | `cb_phieu_chi_bang_ke_hoa_don` ⚠️ **Q-A3** |
| 4 | `ccdc_chi_tiet_phieu_dieu_chinh_ccdc` | `ccdc_phieu_dieu_chinh_chi_tiet` |
| 5 | `ccdc_chi_tiet_phieu_dieu_chuyen_ccdc` | `ccdc_phieu_dieu_chuyen_chi_tiet` |
| 6 | `ccdc_chi_tiet_phieu_ghi_giam_ccdc` | `ccdc_phieu_ghi_giam_chi_tiet` |
| 7 | `ccdc_chi_tiet_phieu_phan_bo_ccdc` | `ccdc_phieu_phan_bo_chi_tiet` |
| 8 | `ccdc_chi_tiet_kiem_ke_ccdc` | `ccdc_phieu_kiem_ke_chi_tiet` |
| 9 | `ccdc_chi_tiet_nguoi_kiem_ke` | `ccdc_phieu_kiem_ke_nguoi_kiem_ke` ⚠️ **Q-A3** |
| 10 | `ccdc_chung_tu_lien_quan` | *(chưa đổi)* ⚠️ **Q-A4** |
| 11 | `cptt_chi_tiet_phan_bo_chi_phi` | `cptt_chung_tu_phan_bo_chi_phi_chi_tiet` |
| 12 | `cst_chi_tiet_chung_tu_gia_thanh` | `cst_chung_tu_gia_thanh_chi_tiet` |
| 13 | `cst_chi_tiet_phan_bo_chi_phi` | `cst_phan_bo_chi_phi_chi_tiet` |
| 14 | `cst_chi_tiet_do_dang_cuoi_ky` | `cst_do_dang_cuoi_ky_chi_tiet` |
| 15 | `fa_chi_tiet_ghi_giam_tscd` | `fa_chung_tu_ghi_giam_tai_san_co_dinh_chi_tiet` |
| 16 | `fa_chi_tiet_dieu_chinh_tai_san_co_dinh` | `fa_dieu_chinh_tai_san_co_dinh_chi_tiet` |
| 17 | `fa_chi_tiet_dieu_chuyen` | `fa_dieu_chuyen_tai_san_chi_tiet` |
| 18 | `fa_chi_tiet_khau_hao_tai_san` | `fa_khau_hao_tai_san_chi_tiet` |
| 19 | `fa_chi_tiet_khai_bao_san_luong` | `fa_khai_bao_san_luong_chi_tiet` |
| 20 | `fa_chi_tiet_kiem_ke_tai_san_co_dinh` | `fa_kiem_ke_tai_san_co_dinh_chi_tiet` |
| 21 | `fa_chi_tiet_ngung_khau_hao` | `fa_chung_tu_ngung_khau_hao_chi_tiet` |
| 22 | `inv_chi_tiet_phieu_nhap_kho` | `inv_phieu_nhap_kho_chi_tiet` |
| 23 | `inv_chi_tiet_phieu_xuat_kho` | `inv_phieu_xuat_kho_chi_tiet` |
| 24 | `inv_chi_tiet_kiem_ke` | `inv_phieu_kiem_ke_chi_tiet` |
| 25 | `inv_chi_tiet_phieu_nhap_dieu_chuyen` | `inv_phieu_nhap_dieu_chuyen_chi_tiet` |
| 26 | `inv_chi_tiet_phieu_xuat_dieu_chuyen` | `inv_phieu_xuat_dieu_chuyen_chi_tiet` |
| 27 | `inv_chi_tiet_phieu_dieu_chuyen_dieu_chinh` | `inv_phieu_dieu_chuyen_dieu_chinh_chi_tiet` |
| 28 | `inv_chi_tiet_ap_gia_xuat_kho` | *(giữ — cha là `inv_ket_qua_tinh_gia_xuat_kho`, không phải chứng từ)* ⚠️ **Q-A5** |
| 29 | `ktth_chi_tiet_phieu_ktth_hach_toan` | `ktth_phieu_ke_toan_tong_hop_hach_toan` |
| 30 | `ktth_chi_tiet_phieu_ktth_hoa_don` | `ktth_phieu_ke_toan_tong_hop_hoa_don` |
| 31 | `pur_chi_tiet_chung_tu_mua_hang` | `pur_chung_tu_mua_hang_chi_tiet` |
| 32 | `pur_chi_tiet_chung_tu_doi_tru` | `pur_chung_tu_doi_tru_chi_tiet` |
| 33 | `pur_chi_tiet_chung_tu_tra_lai_hang_mua` | `pur_chung_tu_tra_lai_hang_mua_chi_tiet` |
| 34 | `pur_chi_tiet_dieu_chinh_gia_mua` | `pur_chung_tu_dieu_chinh_gia_mua_chi_tiet` |
| 35 | `pur_chi_tiet_hoa_don` | `pur_hoa_don_mua_chi_tiet` |
| 36 | `sal_chi_tiet_chung_tu_ban_hang` | `sal_chung_tu_ban_hang_chi_tiet` |
| 37 | `sal_chi_tiet_chung_tu_ban_dv` | `sal_chung_tu_ban_dich_vu_chi_tiet` (luật 2: `dv`) |
| 38 | `sal_chi_tiet_hd_ban_hang` | `sal_hoa_don_ban_hang_chi_tiet` (luật 2: `hd`) |
| 39 | `sal_chi_tiet_chung_tu_tra_lai_hang_ban` | `sal_chung_tu_tra_lai_hang_ban_chi_tiet` |
| 40 | `sal_chi_tiet_dieu_chinh_gia_hang_ban` | `sal_dieu_chinh_gia_hang_ban_chi_tiet` |
| 41 | `sal_chi_tiet_hoa_don_dieu_chinh` | `sal_dieu_chinh_hoa_don_ban_hang_chi_tiet` |
| 42-44 | `sdbd_chi_tiet_sdbd_*` (3 bảng) | *(ngoài phạm vi — số dư đầu kỳ)* |

Tên dài nhất sau đổi: `fa_chung_tu_ghi_giam_tai_san_co_dinh_chi_tiet` (45 ký tự) —
dưới giới hạn 63 của Postgres. Nhưng **tên constraint/index sinh ra từ chúng có thể vượt 63 và bị cắt
âm thầm** — xem §6 mục 3.

## 5. Câu hỏi cần chốt

| # | Câu hỏi | Mặc định trong tài liệu |
|---|---|---|
| ~~Q-A1~~ | ~~`cb_phan_bo_cong_no`, `cst_do_dang_cuoi_ky` có phải chứng từ?~~ | **tự tiêu** — cả hai giữ nguyên tên |
| ~~Q-A2~~ | ~~Giữ hay bỏ chữ `phieu`?~~ | **tự tiêu** — giữ nguyên tên đang có |
| **Q-A3** | Bảng cháu (`cb_chi_tiet_bang_ke_hoa_don`, `ccdc_chi_tiet_nguoi_kiem_ke`) đặt tên theo ông (chứng từ) hay theo cha trực tiếp? | theo chứng từ gốc |
| **Q-A4** | `ccdc_chung_tu_lien_quan` là bảng liên kết dùng chung hay của riêng phiếu kiểm kê? | chưa đổi, chờ xác nhận |
| **Q-A5** | `inv_ket_qua_tinh_gia_xuat_kho` + `inv_chi_tiet_ap_gia_xuat_kho`: bảng kết quả tính giá, có coi là chứng từ? | không đổi |
| **Q-A6** | Có đổi tên **entity/class Java** theo không (`ChiTietChungTuBanHang` → `ChungTuBanHangChiTiet`)? | **không** — chỉ đổi `@Table(name=…)` |
| **Q-A7** | Có muốn đợt sau **bỏ hết** `chung_tu` khỏi tên bảng để đồng nhất theo hướng ngược lại? | không — giữ nguyên bảng đang có |
| **Q-A8** | `cb_chi_tiet_phieu_chi` → `cb_phieu_chi_chi_tiet` đọc bị lặp "chi_chi". Chấp nhận, hay đặt `cb_phieu_chi_dong`? | chấp nhận `_chi_tiet` cho nhất quán máy móc |

## 6. Kế hoạch thực hiện

Chia **theo module, mỗi module một PR**, không gộp — để review và revert độc lập:

| Đợt | Module | Bảng | Ghi chú |
|---|---|---:|---|
| 1 | `sal_` | 6 | có Java thật (`chung_tu_ban_hang`), làm trước để rút kinh nghiệm |
| 2 | `pur_` | 5 | có Java thật (`chung_tu_mua_hang`) |
| 3 | `inv_` + `cb_` | 12 | chạm `master_data` (`LyDoNhapXuatRepository.java:74`) |
| 4 | `fa_` + `ccdc_` | 19 | nhiều bảng nhất, chưa có Java |
| 5 | `cst_` + `cptt_` + `ktth_` | 10 | |

Mỗi PR gồm:

1. `ALTER TABLE … RENAME TO …` — **không** `IF EXISTS`; bảng thiếu thì migration phải đỏ.
2. `ALTER TABLE … RENAME CONSTRAINT …` + `ALTER INDEX … RENAME TO …` — Postgres **giữ nguyên tên cũ** sau khi rename bảng.
3. Kiểm tên constraint/index mới **≤ 63 ký tự**; vượt thì đặt tên rút gọn tường minh, không để Postgres tự cắt.
4. Rà và đổi tên `CREATE POLICY` (RLS) — policy bám OID nên không vỡ, nhưng tên chứa tên bảng cũ.
5. `COMMENT ON TABLE` cập nhật.
6. Sửa `@Table(name=…)` và **mọi native/`@Query` có tên bảng cứng** trong Java.
7. **Không** tạo view tương thích tên cũ — giữ hai tên song song sẽ khiến code mới tiếp tục dùng tên cũ.

Rename là thao tác metadata (không rewrite dữ liệu) nhưng lấy `ACCESS EXCLUSIVE lock` → chạy trong
cửa sổ bảo trì, và **không** chạy song song với migration khác.

### 6.1 Query rà soát trước mỗi đợt

```sql
-- view/materialized view còn tham chiếu bảng sắp đổi tên
SELECT c.relname, c.relkind
FROM pg_class c
JOIN pg_rewrite r ON r.ev_class = c.oid
JOIN pg_depend  d ON d.objid = r.oid
JOIN pg_class   t ON t.oid = d.refobjid
WHERE t.relname = ANY($1) AND c.relkind IN ('v','m');

-- sau rename: constraint/index còn mang tên cũ
SELECT conname, conrelid::regclass FROM pg_constraint WHERE conname ~ '<mảnh tên cũ>'
UNION ALL
SELECT indexname, tablename FROM pg_indexes WHERE indexname ~ '<mảnh tên cũ>';

-- tên vượt giới hạn định danh
SELECT conname, length(conname) FROM pg_constraint WHERE length(conname) >= 63;
```

### 6.2 Nghiệm thu mỗi PR

- [ ] `grep -rn "<tên bảng cũ>" cell-app/src` không còn kết quả nào ngoài chính file migration rename.
- [ ] `cd cell-app && ./gradlew unitTest` xanh.
- [ ] `./gradlew build` xanh trên CI có Docker (máy dev không có Docker → test Testcontainers luôn đỏ, đối chiếu danh sách lớp lỗi trước khi kết luận).
- [ ] Query §6.1 chạy trên bản sao DB production, không còn kết quả.
- [ ] Đo được thời gian giữ `ACCESS EXCLUSIVE lock` trên bản sao production.
- [ ] Sau đợt cuối: khôi phục `permissions.deny` cho `master_data/**` trong `../../.claude/settings.json`.

## 7. Tham chiếu

- [docs/conventions.md](conventions.md) — bổ sung quy ước §1 vào mục đặt tên DB sau khi chốt.
- [thiet-ke-quan-he-chung-tu.md](../done/thiet-ke-quan-he-chung-tu.md) — bảng `ctu_quan_he_chung_tu`; **đợt rename 1 (`sal_`) và 2 (`pur_`) phải xong trước pha P1** của tài liệu đó, không chồng lấn.
- [CLAUDE.md](../../CLAUDE.md) — vùng đóng băng `master_data/**`.
- [10-thiet-ke-db.md](doing/PMKT-E-06194-chung-tu-ban-hang-api/10-thiet-ke-db.md) §2 — nguồn gốc quyết định.
- `../../pmkt-docs/ba/Common/business_rules.md` — BR28 (multi-tenant), BR29 (chính sách xóa).
