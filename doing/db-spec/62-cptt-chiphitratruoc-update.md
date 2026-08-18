# `cptt_` — Chi phí trả trước

> Sinh tự động từ [`ldm-ChiPhiTraTruoc-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-ChiPhiTraTruoc-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**6 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> Chuyển hóa bảo thủ từ ldm-ChiPhiTraTruoc.puml: Entity dùng prefix ENT_ và tên PascalCase. Dấu * chỉ dùng cho khóa chính; dấu ! thể hiện trường bắt buộc. Tham chiếu danh mục lưu ID và Name snapshot; không lưu Code. Field hệ thống dùng chung không khai báo trong từng entity.

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `KhaiBaoChiPhiTraTruoc` | `cptt_khai_bao_chi_phi_tra_truoc` | `cptt_khai_bao_chi_phi_tra_truoc` | B — có schema, chưa code | Cấu hình / thiết lập — 1. Khai báo chi phí trả trước |
| 2 | `ChungTuGocKhaiBaoChiPhiTraTruoc` | `cptt_chung_tu_goc_khai_bao_chi_phi_tra_truoc` | `cptt_chung_tu_goc_khai_bao` | B — có schema, chưa code | Đầu chứng từ — 2. Chứng từ gốc hình thành chi phí trả trước |
| 3 | `ThietLapPhanBoChiPhiTraTruoc` | `cptt_thiet_lap_phan_bo_chi_phi_tra_truoc` | `cptt_thiet_lap_phan_bo_chi_phi` | B — có schema, chưa code | Cấu hình / thiết lập — 3. Thiết lập phân bổ chi phí |
| 4 | `KeHoachPhanBoChiPhiTraTruoc` | `cptt_ke_hoach_phan_bo_chi_phi_tra_truoc` | — | C — tạo mới | Kết quả / số dư luân chuyển — 4. Kế hoạch phân bổ chi phí |
| 5 | `ChungTuPhanBoChiPhiTraTruoc` | `cptt_chung_tu_phan_bo_chi_phi_tra_truoc` | `cptt_chung_tu_phan_bo_chi_phi` | B — có schema, chưa code | Đầu chứng từ — 5. Chứng từ phân bổ chi phí |
| 6 | `ChiTietPhanBoChiPhiTraTruoc` | `cptt_chung_tu_phan_bo_chi_phi_tra_truoc_chi_tiet` | `cptt_chi_tiet_phan_bo_chi_phi` | B — có schema, chưa code | Dòng chi tiết của `cptt_chung_tu_phan_bo_chi_phi_tra_truoc` — 6. Chi tiết bút toán phân bổ |

---

## 1. `cptt_khai_bao_chi_phi_tra_truoc`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KhaiBaoChiPhiTraTruoc` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cptt_khai_bao_chi_phi_tra_truoc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 1. Khai báo chi phí trả trước |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng con | `cptt_chung_tu_goc_khai_bao_chi_phi_tra_truoc` · `cptt_thiet_lap_phan_bo_chi_phi_tra_truoc` · `cptt_ke_hoach_phan_bo_chi_phi_tra_truoc` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `MaChiPhi` | `ma_chi_phi` | `text` | N | — | Mã khai báo chi phí, duy nhất trong đơn vị `UNIQUE` |
| 2 | `TenChiPhi` | `ten_chi_phi` | `text` | N | — | Tên chi phí trả trước |
| 3 | `TaiKhoanChoPhanBoId` | `tai_khoan_cho_phan_bo_id` | `uuid` | N | — | ID tài khoản chờ phân bổ, tham chiếu HeThongTaiKhoan `FK` |
| 4 | `TenTaiKhoanChoPhanBo` | `ten_tai_khoan_cho_phan_bo` | `text` | N | — | Snapshot tên tài khoản chờ phân bổ |
| 5 | `NgayBatDauPhanBo` | `ngay_bat_dau_phan_bo` | `date` | N | — | Ngày bắt đầu phân bổ, xác định kỳ phân bổ đầu tiên |
| 6 | `NgayKetThucPhanBo` | `ngay_ket_thuc_phan_bo` | `date` | N | — | Ngày kết thúc phân bổ |
| 7 | `KieuPhanBo` | `kieu_phan_bo` | `text` CHECK | N | — | Kiểu phân bổ: TheoThang \| HaiLan |
| 8 | `LaCPTTDauKy` | `la_cptt_dau_ky` | `boolean` | Y | `false` | Cờ CPTT đầu kỳ |
| 9 | `TongSoTien` | `tong_so_tien` | `money_foreign` ≈ | N | `0` | Tổng số tiền chi phí, phải lớn hơn 0 |
| 10 | `SoKyPhanBo` | `so_ky_phan_bo` | `money_foreign` ≈ | Y | `0` | Số kỳ phân bổ |
| 11 | `SoTienPhanBoHangKy` | `so_tien_phan_bo_hang_ky` | `money_foreign` ≈ | N | `0` | Số tiền phân bổ hằng kỳ |
| 12 | `SoTienDaPhanBo` | `so_tien_da_phan_bo` | `money_foreign` ≈ | Y | `0` | Số tiền đã phân bổ |
| 13 | `SoKyPhanBoConLai` | `so_ky_phan_bo_con_lai` | `money_foreign` ≈ | Y | `0` | Số kỳ phân bổ còn lại |
| 14 | `SoTienPhanBoConLai` | `so_tien_phan_bo_con_lai` | `money_foreign` ≈ | Y | `0` | Số tiền phân bổ còn lại = TongSoTien - SoTienDaPhanBo |
| 15 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | ChuaPB \| DangPB \| DungPB \| DaPB |

**Trường base — `TenantedEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `cptt_khai_bao_chi_phi_tra_truoc` (24 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `tai_khoan_cho_phan_bo_id`, `ten_tai_khoan_cho_phan_bo`, `so_tien_phan_bo_hang_ky`, `so_tien_da_phan_bo`, `so_ky_phan_bo_con_lai`, `so_tien_phan_bo_con_lai` |
| DB có — LDM **không khai** | 6 | `tai_khoan_cho_pb_id`, `so_tien_pb_hang_ky`, `so_tien_da_pb`, `so_ky_pb_con_lai`, `so_tien_pb_con_lai`, `phien_ban` |

---

## 2. `cptt_chung_tu_goc_khai_bao_chi_phi_tra_truoc`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuGocKhaiBaoChiPhiTraTruoc` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cptt_chung_tu_goc_khai_bao` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 2. Chứng từ gốc hình thành chi phí trả trước |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `cptt_khai_bao_chi_phi_tra_truoc` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhaiBaoChiPhiTraTruocId` | `khai_bao_chi_phi_tra_truoc_id` | `uuid` | N | — | ID khai báo chi phí trả trước `FK` |
| 2 | `ChungTuId` | `chung_tu_id` | `uuid` | N | — | ID chứng từ gốc `FK` |
| 3 | `TenLoaiChungTu` | `ten_loai_chung_tu` | `text` | N | — | Snapshot tên loại chứng từ |
| 4 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải chứng từ gốc |
| 5 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | Giá trị đưa vào chi phí trả trước |

**Trường base — `BaseChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4 |
| `phien_ban` | `integer` | N | `1` | Khóa lạc quan `@Version`. `AggregateRootEntity` |
| `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4 |
| `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4 |
| `giao_dich_chung_tu_id` | `uuid` | Y | — | Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity` |
| `so_chung_tu` | `varchar(50)` | N | — | Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20 |
| `ngay_chung_tu` | `date` | N | — | Ngày lập chứng từ. `BaseChungTuEntity` |
| `ngay_hach_toan` | `date` | N | — | Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37 |
| `status` | `text` | N | `NHAP` | Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12 |
| `nguoi_duyet_id` | `uuid` | Y | — | Người duyệt. `BaseChungTuEntity` |
| `ngay_duyet` | `timestamptz` | Y | — | Thời điểm duyệt. `BaseChungTuEntity` |
| `nguoi_ghi_so` | `uuid` | Y | — | Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `thoi_gian_ghi_so` | `timestamptz` | Y | — | Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo, gán một lần. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo, gán một lần. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `cptt_chung_tu_goc_khai_bao` (18 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `khai_bao_chi_phi_tra_truoc_id`, `chung_tu_id`, `ten_loai_chung_tu` |
| DB có — LDM **không khai** | 3 | `khai_bao_id`, `chung_tu_goc_id`, `loai_chung_tu` |

---

## 3. `cptt_thiet_lap_phan_bo_chi_phi_tra_truoc`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThietLapPhanBoChiPhiTraTruoc` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cptt_thiet_lap_phan_bo_chi_phi` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 3. Thiết lập phân bổ chi phí |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng cha | `cptt_khai_bao_chi_phi_tra_truoc` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhaiBaoChiPhiTraTruocId` | `khai_bao_chi_phi_tra_truoc_id` | `uuid` | N | — | ID khai báo chi phí trả trước `FK` |
| 2 | `LanPhanBo` | `lan_phan_bo` | `money_foreign` ≈ | Y | `0` | Số thứ tự lần phân bổ |
| 3 | `Nam` | `nam` | `integer` | Y | `0` | Năm bắt đầu áp dụng |
| 4 | `Thang` | `thang` | `integer` | Y | `0` | Tháng bắt đầu áp dụng, từ 1 đến 12 |
| 5 | `HeSo` | `he_so` | `exchange_rate` ≈ | N | `0` | Hệ số phân bổ |
| 6 | `SoTienPhanBoHangKy` | `so_tien_phan_bo_hang_ky` | `money_foreign` ≈ | N | `0` | Số tiền phân bổ hằng kỳ của dòng |
| 7 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản chi phí Nợ, tham chiếu HeThongTaiKhoan `FK` |
| 8 | `TenTaiKhoanNo` | `ten_tai_khoan_no` | `text` | N | — | Snapshot tên tài khoản Nợ |
| 9 | `DonViId` | `don_vi_id` | `uuid` | Y | — | ID đơn vị sử dụng, tham chiếu DonVi `FK` |
| 10 | `TenDonVi` | `ten_don_vi` | `text` | Y | — | Snapshot tên đơn vị |
| 11 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | ID đối tượng tập hợp chi phí `FK` |
| 12 | `TenDoiTuongTapHopChiPhi` | `ten_doi_tuong_tap_hop_chi_phi` | `text` | Y | — | Snapshot tên đối tượng tập hợp chi phí |
| 13 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID công trình/vụ việc `FK` |
| 14 | `TenCongTrinh` | `ten_cong_trinh` | `text` | Y | — | Snapshot tên công trình/vụ việc |
| 15 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 16 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |
| 17 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

**Trường base — `TenantedEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `cptt_thiet_lap_phan_bo_chi_phi` (22 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 7 | `khai_bao_chi_phi_tra_truoc_id`, `ten_tai_khoan_no`, `don_vi_id`, `ten_don_vi`, `ten_doi_tuong_tap_hop_chi_phi`, `ten_cong_trinh`, `ten_khoan_muc_chi_phi` |
| DB có — LDM **không khai** | 3 | `khai_bao_id`, `don_vi_su_dung_id`, `phien_ban` |

---

## 4. `cptt_ke_hoach_phan_bo_chi_phi_tra_truoc`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KeHoachPhanBoChiPhiTraTruoc` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 4. Kế hoạch phân bổ chi phí |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |
| Bảng cha | `cptt_khai_bao_chi_phi_tra_truoc` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhaiBaoChiPhiTraTruocId` | `khai_bao_chi_phi_tra_truoc_id` | `uuid` | N | — | ID khai báo chi phí trả trước `FK` |
| 2 | `KyPhanBo` | `ky_phan_bo` | `date` | N | — | Kỳ phân bổ |
| 3 | `SoTienDuKien` | `so_tien_du_kien` | `money_foreign` ≈ | N | `0` | Số tiền dự kiến phân bổ |
| 4 | `SoTienThucTe` | `so_tien_thuc_te` | `money_foreign` ≈ | Y | `0` | Số tiền thực tế phân bổ |
| 5 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | ChuaSinhCT \| DaSinhCT \| DaGhiSo \| DaHuy |

**Trường base — `TenantedEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

---

## 5. `cptt_chung_tu_phan_bo_chi_phi_tra_truoc`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuPhanBoChiPhiTraTruoc` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cptt_chung_tu_phan_bo_chi_phi` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 5. Chứng từ phân bổ chi phí |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `cptt_chung_tu_phan_bo_chi_phi_tra_truoc_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KyPhanBo` | `ky_phan_bo` | `date` | N | — | Kỳ phân bổ |
| 2 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | ChuaGhiSo \| DaGhiSo \| DaHuy |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

**Trường base — `BaseChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4 |
| `phien_ban` | `integer` | N | `1` | Khóa lạc quan `@Version`. `AggregateRootEntity` |
| `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4 |
| `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4 |
| `giao_dich_chung_tu_id` | `uuid` | Y | — | Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity` |
| `so_chung_tu` | `varchar(50)` | N | — | Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20 |
| `ngay_chung_tu` | `date` | N | — | Ngày lập chứng từ. `BaseChungTuEntity` |
| `ngay_hach_toan` | `date` | N | — | Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37 |
| `status` | `text` | N | `NHAP` | Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12 |
| `nguoi_duyet_id` | `uuid` | Y | — | Người duyệt. `BaseChungTuEntity` |
| `ngay_duyet` | `timestamptz` | Y | — | Thời điểm duyệt. `BaseChungTuEntity` |
| `nguoi_ghi_so` | `uuid` | Y | — | Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `thoi_gian_ghi_so` | `timestamptz` | Y | — | Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo, gán một lần. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo, gán một lần. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `cptt_chung_tu_phan_bo_chi_phi` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 1 | `mo_ta` |

---

## 6. `cptt_chung_tu_phan_bo_chi_phi_tra_truoc_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhanBoChiPhiTraTruoc` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cptt_chi_tiet_phan_bo_chi_phi` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 6. Chi tiết bút toán phân bổ |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cptt_chung_tu_phan_bo_chi_phi_tra_truoc` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cptt_chung_tu_phan_bo_chi_phi_tra_truoc` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuPhanBoChiPhiTraTruocId` | `chung_tu_phan_bo_chi_phi_tra_truoc_id` | `uuid` | N | — | ID chứng từ phân bổ `FK` |
| 2 | `KhaiBaoChiPhiTraTruocId` | `khai_bao_chi_phi_tra_truoc_id` | `uuid` | N | — | ID khai báo chi phí trả trước `FK` |
| 3 | `KeHoachPhanBoChiPhiTraTruocId` | `ke_hoach_phan_bo_chi_phi_tra_truoc_id` | `uuid` | N | — | ID kế hoạch phân bổ `FK` |
| 4 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản Nợ, tham chiếu HeThongTaiKhoan `FK` |
| 5 | `TenTaiKhoanNo` | `ten_tai_khoan_no` | `text` | N | — | Snapshot tên tài khoản Nợ |
| 6 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản Có, tham chiếu HeThongTaiKhoan `FK` |
| 7 | `TenTaiKhoanCo` | `ten_tai_khoan_co` | `text` | N | — | Snapshot tên tài khoản Có |
| 8 | `HeSo` | `he_so` | `exchange_rate` ≈ | Y | `0` | Hệ số phân bổ tại thời điểm sinh chứng từ |
| 9 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | Số tiền phân bổ thực tế |
| 10 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |
| 11 | `DonViId` | `don_vi_id` | `uuid` | Y | — | ID đơn vị sử dụng `FK` |
| 12 | `TenDonVi` | `ten_don_vi` | `text` | Y | — | Snapshot tên đơn vị |
| 13 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | ID đối tượng tập hợp chi phí `FK` |
| 14 | `TenDoiTuongTapHopChiPhi` | `ten_doi_tuong_tap_hop_chi_phi` | `text` | Y | — | Snapshot tên đối tượng tập hợp chi phí |
| 15 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID công trình/vụ việc `FK` |
| 16 | `TenCongTrinh` | `ten_cong_trinh` | `text` | Y | — | Snapshot tên công trình/vụ việc |
| 17 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 18 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `cptt_chi_tiet_phan_bo_chi_phi` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 11 | `chung_tu_phan_bo_chi_phi_tra_truoc_id`, `khai_bao_chi_phi_tra_truoc_id`, `ke_hoach_phan_bo_chi_phi_tra_truoc_id`, `ten_tai_khoan_no`, `ten_tai_khoan_co`, `he_so`, `don_vi_id`, `ten_don_vi`, `ten_doi_tuong_tap_hop_chi_phi`, `ten_cong_trinh`, `ten_khoan_muc_chi_phi` |
| DB có — LDM **không khai** | 3 | `chung_tu_phan_bo_id`, `khai_bao_id`, `don_vi_su_dung_id` |

