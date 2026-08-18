# `ccdc_` — Công cụ dụng cụ

> Sinh tự động từ [`ldm-CCDC.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-CCDC.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**18 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `CongCuDungCu` | `ccdc_cong_cu_dung_cu` | `ccdc_cong_cu_dung_cu` | B — có schema, chưa code | Đầu chứng từ — Công cụ dụng cụ (Master - chứng từ ghi tăng, đồng thời là master data) |
| 2 | `DonViQuanLyCCDC` | `ccdc_don_vi_quan_ly` | `ccdc_don_vi_quan_ly_ccdc` | B — có schema, chưa code | Dòng chi tiết của `ccdc_cong_cu_dung_cu` — Đơn vị quản lý CCDC (Detail - tab Đơn vị quản lý) |
| 3 | `NhomHeSoPhanBoCCDC` | `ccdc_nhom_he_so_phan_bo` | — | C — tạo mới | Dòng chi tiết của `ccdc_cong_cu_dung_cu` — Nhóm hệ số phân bổ (tab Thiết lập phân bổ) |
| 4 | `HeSoPhanBoCongCuDungCu` | `ccdc_he_so_phan_bo` | `ccdc_he_so_phan_bo_ccdc` | B — có schema, chưa code | Bảng nghiệp vụ — Dòng hệ số phân bổ trong nhóm |
| 5 | `ThamChieuThuCongCCDC` | `ccdc_tham_chieu_thu_cong` | *?* | **? — chưa rà, Pha 1 đối chiếu tay** | Dòng chi tiết của `ccdc_cong_cu_dung_cu` — Dòng tham chiếu thủ công (tab Tham chiếu; dòng từ nguồn phiếu lưu tại ENT_ChungTuLienQuan) |
| 6 | `PhieuKiemKeCCDC` | `ccdc_phieu_kiem_ke` | `ccdc_phieu_kiem_ke_ccdc` | B — có schema, chưa code | Đầu chứng từ — Phiếu kiểm kê CCDC (Master) |
| 7 | `PhieuKiemKeCCDC_DonVi` | `ccdc_phieu_kiem_ke_don_vi` | — | C — tạo mới | Dòng chi tiết của `ccdc_phieu_kiem_ke` — Đơn vị được kiểm kê của phiếu (Link) |
| 8 | `NguoiKiemKeCCDC` | `ccdc_phieu_kiem_ke_nguoi_kiem_ke` | `ccdc_chi_tiet_nguoi_kiem_ke` | B — có schema, chưa code | Dòng chi tiết của `ccdc_phieu_kiem_ke` — Người kiểm kê (Detail) |
| 9 | `ChiTietKiemKeCCDC` | `ccdc_phieu_kiem_ke_chi_tiet` | `ccdc_chi_tiet_kiem_ke_ccdc` | B — có schema, chưa code | Dòng chi tiết của `ccdc_phieu_kiem_ke` — Chi tiết kiểm kê (Detail - mỗi dòng một CCDC theo đơn vị quản lý) |
| 10 | `PhieuDieuChinhCCDC` | `ccdc_phieu_dieu_chinh` | `ccdc_phieu_dieu_chinh_ccdc` | B — có schema, chưa code | Đầu chứng từ — Phiếu điều chỉnh CCDC (Master) |
| 11 | `ChiTietPhieuDieuChinhCCDC` | `ccdc_phieu_dieu_chinh_chi_tiet` | `ccdc_chi_tiet_phieu_dieu_chinh_ccdc` | B — có schema, chưa code | Dòng chi tiết của `ccdc_phieu_dieu_chinh` — Chi tiết điều chỉnh (Detail - mỗi dòng một CCDC) |
| 12 | `PhieuDieuChuyenCCDC` | `ccdc_phieu_dieu_chuyen` | `ccdc_phieu_dieu_chuyen_ccdc` | B — có schema, chưa code | Đầu chứng từ — Phiếu điều chuyển CCDC (Master) |
| 13 | `ChiTietPhieuDieuChuyenCCDC` | `ccdc_phieu_dieu_chuyen_chi_tiet` | `ccdc_chi_tiet_phieu_dieu_chuyen_ccdc` | B — có schema, chưa code | Dòng chi tiết của `ccdc_phieu_dieu_chuyen` — Chi tiết điều chuyển (Detail - mỗi dòng một CCDC) |
| 14 | `PhieuGhiGiamCCDC` | `ccdc_phieu_ghi_giam` | `ccdc_phieu_ghi_giam_ccdc` | B — có schema, chưa code | Đầu chứng từ — Phiếu ghi giảm CCDC (Master) |
| 15 | `ChiTietPhieuGhiGiamCCDC` | `ccdc_phieu_ghi_giam_chi_tiet` | `ccdc_chi_tiet_phieu_ghi_giam_ccdc` | B — có schema, chưa code | Dòng chi tiết của `ccdc_phieu_ghi_giam` — Chi tiết ghi giảm (Detail - mỗi dòng một CCDC theo đơn vị sử dụng) |
| 16 | `PhieuPhanBoCCDC` | `ccdc_phieu_phan_bo` | `ccdc_phieu_phan_bo_ccdc` | B — có schema, chưa code | Đầu chứng từ — Phiếu phân bổ CCDC (Master - mỗi cặp Năm/Tháng một phiếu) |
| 17 | `ChiTietPhieuPhanBoCCDC` | `ccdc_phieu_phan_bo_chi_tiet` | `ccdc_chi_tiet_phieu_phan_bo_ccdc` | B — có schema, chưa code | Dòng chi tiết của `ccdc_phieu_phan_bo` — Chi tiết phân bổ (Detail - tab Xác định chi phí và phân bổ; tab Hạch toán là preview gom nhóm từ các dòng này) |
| 18 | `TamDungPhanBoCCDC` | `ccdc_tam_dung_phan_bo` | `ccdc_tam_dung_phan_bo_ccdc` | B — có schema, chưa code | Dòng chi tiết của `ccdc_cong_cu_dung_cu` — Tạm dừng / Tiếp tục phân bổ (popup từ màn danh sách CCDC) |

---

## 1. `ccdc_cong_cu_dung_cu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `CongCuDungCu` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_cong_cu_dung_cu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Công cụ dụng cụ (Master - chứng từ ghi tăng, đồng thời là master data) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ccdc_don_vi_quan_ly` · `ccdc_nhom_he_so_phan_bo` · `ccdc_tham_chieu_thu_cong` · `ccdc_tam_dung_phan_bo` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Code` | `code` | `varchar(50)` | N | — | **[Thông tin CCDC]** Mã CCDC |
| 2 | `Ten` | `ten` | `text` | N | — | **[Thông tin CCDC]** Tên CCDC |
| 3 | `DonViTinh` | `don_vi_tinh` | `text` | Y | — | **[Thông tin CCDC]** Đơn vị tính |
| 4 | `LoaiCongCuDungCuId` | `loai_cong_cu_dung_cu_id` | `uuid` | Y | — | **[Thông tin CCDC]** ID loại CCDC (reference ENT_LoaiCongCuDungCu) `FK` |
| 5 | `NguonVonId` | `nguon_von_id` | `uuid` | Y | — | **[Thông tin CCDC]** ID nguồn vốn (reference ENT_NguonVon) `FK` |
| 6 | `SoDuDauKy` | `so_du_dau_ky` | `boolean` | N | `false` | **[Thông tin CCDC]** Là CCDC đầu kỳ |
| 7 | `KieuPhanBo` | `kieu_phan_bo` | `text` CHECK | N | — | **[Phương thức phân bổ]** Kiểu phân bổ (TheoThang \| HaiLan) |
| 8 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Phương thức phân bổ]** Số lượng |
| 9 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | **[Phương thức phân bổ]** Đơn giá |
| 10 | `TongGiaTriBanDau` | `tong_gia_tri_ban_dau` | `money_foreign` ≈ | N | `0` | **[Phương thức phân bổ]** Tổng giá trị ban đầu |
| 11 | `TaiKhoanChoPhanBoId` | `tai_khoan_cho_phan_bo_id` | `uuid` | N | — | **[Phương thức phân bổ]** ID tài khoản chờ phân bổ (reference ENT_HeThongTaiKhoan) `FK` |
| 12 | `SoKyPhanBo` | `so_ky_phan_bo` | `money_foreign` ≈ | N | `0` | **[Phương thức phân bổ]** Số kỳ phân bổ |
| 13 | `NgayTinhPhanBo` | `ngay_tinh_phan_bo` | `date` | N | — | **[Phương thức phân bổ]** Ngày bắt đầu phân bổ |
| 14 | `NgayKetThucPhanBo` | `ngay_ket_thuc_phan_bo` | `date` | N | — | **[Phương thức phân bổ]** Ngày kết thúc phân bổ |
| 15 | `GiaTriPhanBoMoiKy` | `gia_tri_phan_bo_moi_ky` | `money_foreign` ≈ | Y | `0` | **[Phương thức phân bổ]** Số tiền phân bổ mỗi kỳ |
| 16 | `GiaTriDaPhanBo` | `gia_tri_da_phan_bo` | `money_foreign` ≈ | N | `0` | **[Lũy kế phân bổ]** Giá trị đã phân bổ |
| 17 | `GiaTriConLai` | `gia_tri_con_lai` | `money_foreign` ≈ | N | `0` | **[Lũy kế phân bổ]** Giá trị phân bổ còn lại |
| 18 | `SoKyPhanBoConLai` | `so_ky_phan_bo_con_lai` | `money_foreign` ≈ | Y | `0` | **[Lũy kế phân bổ]** Số kỳ phân bổ còn lại |
| 19 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Lũy kế phân bổ]** Trạng thái CCDC (ChuaPhanBo \| DangPhanBo \| TamDungPhanBo \| HoanThanhPhanBo \| DaGhiGiam) |
| 20 | `LyDoGhiTang` | `ly_do_ghi_tang` | `text` | Y | — | **[Đầu chứng từ]** Lý do ghi tăng, người dùng nhập tay |
| 21 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |

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

**Đối chiếu `ccdc_cong_cu_dung_cu` (1 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 20 | `code`, `ten`, `loai_cong_cu_dung_cu_id`, `nguon_von_id`, `so_du_dau_ky`, `kieu_phan_bo`, `so_luong`, `don_gia`, `tong_gia_tri_ban_dau`, `tai_khoan_cho_phan_bo_id`, `so_ky_phan_bo`, `ngay_tinh_phan_bo`, `ngay_ket_thuc_phan_bo`, `gia_tri_phan_bo_moi_ky`, `gia_tri_da_phan_bo`, `gia_tri_con_lai`, `so_ky_phan_bo_con_lai`, `trang_thai`, `ly_do_ghi_tang`, `dien_giai` |
| DB có — LDM **không khai** | 0 | *(không)* |

---

## 2. `ccdc_don_vi_quan_ly`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DonViQuanLyCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_don_vi_quan_ly_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Đơn vị quản lý CCDC (Detail - tab Đơn vị quản lý) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_cong_cu_dung_cu` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_cong_cu_dung_cu` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC (reference ENT_CongCuDungCu) `FK` |
| 2 | `DonViId` | `don_vi_id` | `uuid` | N | — | ID đơn vị quản lý (reference ENT_DonVi) `FK` |
| 3 | `SoLuong` | `so_luong` | `quantity` | N | `0` | Số lượng CCDC phân cho đơn vị |
| 4 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

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

**Đối chiếu `ccdc_don_vi_quan_ly_ccdc` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 3 | `references`, `mo_ta`, `phien_ban` |

---

## 3. `ccdc_nhom_he_so_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `NhomHeSoPhanBoCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Nhóm hệ số phân bổ (tab Thiết lập phân bổ) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_cong_cu_dung_cu` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_cong_cu_dung_cu` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC (reference ENT_CongCuDungCu) `FK` |
| 2 | `NamTu` | `nam_tu` | `integer` | N | `0` | Năm bắt đầu áp dụng nhóm |
| 3 | `KyTu` | `ky_tu` | `integer` | N | `0` | Tháng bắt đầu áp dụng nhóm |

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

---

## 4. `ccdc_he_so_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HeSoPhanBoCongCuDungCu` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_he_so_phan_bo_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng hệ số phân bổ trong nhóm |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NhomHeSoPhanBoId` | `nhom_he_so_phan_bo_id` | `uuid` | N | — | ID nhóm hệ số phân bổ (reference ENT_NhomHeSoPhanBoCCDC) `FK` |
| 2 | `HeSo` | `he_so` | `exchange_rate` ≈ | N | `0` | Hệ số phân bổ |
| 3 | `TaiKhoanChiPhiId` | `tai_khoan_chi_phi_id` | `uuid` | N | — | ID tài khoản chi phí (reference ENT_HeThongTaiKhoan) `FK` |
| 4 | `DonViSuDungId` | `don_vi_su_dung_id` | `uuid` | Y | — | **[Trường tự do]** ID đơn vị sử dụng (reference ENT_DonVi) `FK` |
| 5 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID đối tượng tập hợp chi phí (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 6 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Trường tự do]** ID vụ việc (reference ENT_CongTrinh) `FK` |
| 7 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 8 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Trường tự do]** Diễn giải |

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

**Đối chiếu `ccdc_he_so_phan_bo_ccdc` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `nhom_he_so_phan_bo_id`, `don_vi_su_dung_id`, `dien_giai` |
| DB có — LDM **không khai** | 6 | `cong_cu_dung_cu_id`, `nam_tu`, `ky_tu`, `don_vi_id`, `mo_ta`, `phien_ban` |

---

## 5. `ccdc_tham_chieu_thu_cong`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThamChieuThuCongCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | **? — chưa rà, Pha 1 đối chiếu tay** |
| Bảng hiện có | *chưa rà — Pha 1* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng tham chiếu thủ công (tab Tham chiếu; dòng từ nguồn phiếu · lưu tại ENT_ChungTuLienQuan) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_cong_cu_dung_cu` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_cong_cu_dung_cu` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC (reference ENT_CongCuDungCu) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

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

---

## 6. `ccdc_phieu_kiem_ke`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuKiemKeCCDC` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_phieu_kiem_ke_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu kiểm kê CCDC (Master) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ccdc_phieu_kiem_ke_don_vi` · `ccdc_phieu_kiem_ke_nguoi_kiem_ke` · `ccdc_phieu_kiem_ke_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KiemKeDenNgay` | `kiem_ke_den_ngay` | `date` | N | — | Kiểm kê đến ngày |
| 2 | `NoiDungKiemKe` | `noi_dung_kiem_ke` | `text` | Y | — | Nội dung kiểm kê |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải chung của phiếu |

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

**Đối chiếu `ccdc_phieu_kiem_ke_ccdc` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 2 | `don_vi_ids`, `mota` |

---

## 7. `ccdc_phieu_kiem_ke_don_vi`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuKiemKeCCDC_DonVi` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Đơn vị được kiểm kê của phiếu (Link) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_phieu_kiem_ke` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_phieu_kiem_ke` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKiemKeCCDCId` | `phieu_kiem_ke_ccdc_id` | `uuid` | N | — | ID phiếu kiểm kê (reference ENT_PhieuKiemKeCCDC) `FK` |
| 2 | `DonViId` | `don_vi_id` | `uuid` | N | — | ID đơn vị cần kiểm kê (reference ENT_DonVi) `FK` |

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

---

## 8. `ccdc_phieu_kiem_ke_nguoi_kiem_ke`

| Mục | Nội dung |
|---|---|
| Entity LDM | `NguoiKiemKeCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_chi_tiet_nguoi_kiem_ke` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Người kiểm kê (Detail) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_phieu_kiem_ke` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_phieu_kiem_ke` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKiemKeCCDCId` | `phieu_kiem_ke_ccdc_id` | `uuid` | N | — | ID phiếu kiểm kê (reference ENT_PhieuKiemKeCCDC) `FK` |
| 2 | `NguoiKiemKe` | `nguoi_kiem_ke` | `text` | N | — | Họ tên người kiểm kê |
| 3 | `ChucDanh` | `chuc_danh` | `text` | Y | — | Chức danh |
| 4 | `DaiDien` | `dai_dien` | `text` | Y | — | Đại diện cho đơn vị |

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

**Đối chiếu `ccdc_chi_tiet_nguoi_kiem_ke` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 9. `ccdc_phieu_kiem_ke_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietKiemKeCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_chi_tiet_kiem_ke_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết kiểm kê (Detail - mỗi dòng một CCDC theo đơn vị quản lý) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_phieu_kiem_ke` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_phieu_kiem_ke` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKiemKeCCDCId` | `phieu_kiem_ke_ccdc_id` | `uuid` | N | — | ID phiếu kiểm kê (reference ENT_PhieuKiemKeCCDC) `FK` |
| 2 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC được kiểm kê (reference ENT_CongCuDungCu) `FK` |
| 3 | `DonViId` | `don_vi_id` | `uuid` | N | — | ID đơn vị quản lý CCDC của dòng kiểm kê (reference ENT_DonVi) `FK` |
| 4 | `SoLuongThucTe` | `so_luong_thuc_te` | `quantity` | N | `0` | Số lượng thực tế |
| 5 | `SoLuongTot` | `so_luong_tot` | `quantity` | N | `0` | Số lượng tốt |
| 6 | `SoLuongKem` | `so_luong_kem` | `quantity` | N | `0` | Số lượng kém |
| 7 | `SoLuongHong` | `so_luong_hong` | `quantity` | N | `0` | Số lượng hỏng |
| 8 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

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

**Đối chiếu `ccdc_chi_tiet_kiem_ke_ccdc` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `don_vi_id`, `dien_giai` |
| DB có — LDM **không khai** | 2 | `mo_ta`, `phien_ban` |

---

## 10. `ccdc_phieu_dieu_chinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuDieuChinhCCDC` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_phieu_dieu_chinh_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu điều chỉnh CCDC (Master) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ccdc_phieu_dieu_chinh_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | **[Đầu chứng từ]** Lý do điều chỉnh (reference ENT_TaiKhoanNgamDinh) `FK` |
| 2 | `TenTaiKhoanNgamDinh` | `ten_tai_khoan_ngam_dinh` | `text` | Y | — | **[Đầu chứng từ]** Tên lý do điều chỉnh (snapshot) |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |

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

**Đối chiếu `ccdc_phieu_dieu_chinh_ccdc` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `tai_khoan_ngam_dinh_id`, `ten_tai_khoan_ngam_dinh`, `dien_giai` |
| DB có — LDM **không khai** | 3 | `ngay_dieu_chinh`, `ly_do_tang_giam_id`, `trang_thai` |

---

## 11. `ccdc_phieu_dieu_chinh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuDieuChinhCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_chi_tiet_phieu_dieu_chinh_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết điều chỉnh (Detail - mỗi dòng một CCDC) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_phieu_dieu_chinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_phieu_dieu_chinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuDieuChinhCCDCId` | `phieu_dieu_chinh_ccdc_id` | `uuid` | N | — | ID phiếu điều chỉnh (reference ENT_PhieuDieuChinhCCDC) `FK` |
| 2 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC được điều chỉnh (reference ENT_CongCuDungCu) `FK` |
| 3 | `GiaTriPBConLaiMoi` | `gia_tri_pb_con_lai_moi` | `money_foreign` ≈ | N | `0` | Giá trị phân bổ còn lại sau điều chỉnh |
| 4 | `ChenhLechGiaTri` | `chenh_lech_gia_tri` | `money_foreign` ≈ | Y | `0` | Chênh lệch giá trị |
| 5 | `SoKyPhanBoConLaiMoi` | `so_ky_phan_bo_con_lai_moi` | `money_foreign` ≈ | N | `0` | Kỳ phân bổ còn lại sau điều chỉnh |
| 6 | `ChenhLechSoKy` | `chenh_lech_so_ky` | `numeric(18,4)` ⚠ | Y | `0` | Chênh lệch kỳ |
| 7 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải chi tiết điều chỉnh |

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

**Đối chiếu `ccdc_chi_tiet_phieu_dieu_chinh_ccdc` (13 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `gia_tri_pb_con_lai_moi`, `dien_giai` |
| DB có — LDM **không khai** | 2 | `gia_tri_con_lai_moi`, `mo_ta_chi_tiet_dieu_chinh` |

---

## 12. `ccdc_phieu_dieu_chuyen`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuDieuChuyenCCDC` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_phieu_dieu_chuyen_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu điều chuyển CCDC (Master) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ccdc_phieu_dieu_chuyen_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LyDoDieuChuyen` | `ly_do_dieu_chuyen` | `text` | Y | — | Lý do điều chuyển |
| 2 | `NguoiBanGiao` | `nguoi_ban_giao` | `text` | Y | — | Người bàn giao |
| 3 | `NguoiTiepNhan` | `nguoi_tiep_nhan` | `text` | Y | — | Người tiếp nhận |
| 4 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |

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

**Đối chiếu `ccdc_phieu_dieu_chuyen_ccdc` (18 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `nguoi_tiep_nhan`, `dien_giai` |
| DB có — LDM **không khai** | 4 | `ngay_dieu_chuyen`, `don_vi_ban_giao_id`, `don_vi_tiep_nhan_id`, `trang_thai` |

---

## 13. `ccdc_phieu_dieu_chuyen_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuDieuChuyenCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_chi_tiet_phieu_dieu_chuyen_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết điều chuyển (Detail - mỗi dòng một CCDC) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_phieu_dieu_chuyen` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_phieu_dieu_chuyen` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuDieuChuyenCCDCId` | `phieu_dieu_chuyen_ccdc_id` | `uuid` | N | — | ID phiếu điều chuyển (reference ENT_PhieuDieuChuyenCCDC) `FK` |
| 2 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC được điều chuyển (reference ENT_CongCuDungCu) `FK` |
| 3 | `DonViHienTaiId` | `don_vi_hien_tai_id` | `uuid` | N | — | ID đơn vị bàn giao (reference ENT_DonVi) `FK` |
| 4 | `DonViTiepNhanId` | `don_vi_tiep_nhan_id` | `uuid` | N | — | ID đơn vị tiếp nhận (reference ENT_DonVi) `FK` |
| 5 | `SoLuongDieuChuyen` | `so_luong_dieu_chuyen` | `quantity` | N | `0` | Số lượng điều chuyển |

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

**Đối chiếu `ccdc_chi_tiet_phieu_dieu_chuyen_ccdc` (11 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `don_vi_hien_tai_id` |
| DB có — LDM **không khai** | 1 | `don_vi_ban_giao_id` |

---

## 14. `ccdc_phieu_ghi_giam`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuGhiGiamCCDC` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_phieu_ghi_giam_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu ghi giảm CCDC (Master) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ccdc_phieu_ghi_giam_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | **[Đầu chứng từ]** Lý do ghi giảm (reference ENT_TaiKhoanNgamDinh) `FK` |
| 2 | `TenTaiKhoanNgamDinh` | `ten_tai_khoan_ngam_dinh` | `text` | Y | — | **[Đầu chứng từ]** Tên lý do ghi giảm (snapshot) |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Đầu chứng từ]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `ccdc_phieu_ghi_giam_ccdc` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `tai_khoan_ngam_dinh_id`, `ten_tai_khoan_ngam_dinh`, `dien_giai` |
| DB có — LDM **không khai** | 3 | `ngay_ghi_giam`, `ly_do_tang_giam_id`, `tai_khoan_xu_ly_gtcl` |

---

## 15. `ccdc_phieu_ghi_giam_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuGhiGiamCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_chi_tiet_phieu_ghi_giam_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết ghi giảm (Detail - mỗi dòng một CCDC theo đơn vị sử dụng) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_phieu_ghi_giam` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_phieu_ghi_giam` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuGhiGiamCCDCId` | `phieu_ghi_giam_ccdc_id` | `uuid` | N | — | ID phiếu ghi giảm (reference ENT_PhieuGhiGiamCCDC) `FK` |
| 2 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC được ghi giảm (reference ENT_CongCuDungCu) `FK` |
| 3 | `DonViSuDungId` | `don_vi_su_dung_id` | `uuid` | N | — | ID đơn vị sử dụng (reference ENT_DonVi) `FK` |
| 4 | `SoLuongGiam` | `so_luong_giam` | `quantity` | N | `0` | Số lượng ghi giảm |
| 5 | `TaiKhoanXuLyGTCLId` | `tai_khoan_xu_ly_gtcl_id` | `uuid` | N | — | ID tài khoản xử lý giá trị còn lại (reference ENT_HeThongTaiKhoan) `FK` |

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

**Đối chiếu `ccdc_chi_tiet_phieu_ghi_giam_ccdc` (10 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `so_luong_giam`, `tai_khoan_xu_ly_gtcl_id` |
| DB có — LDM **không khai** | 1 | `tai_khoan_xu_ly_gtcl` |

---

## 16. `ccdc_phieu_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuPhanBoCCDC` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_phieu_phan_bo_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Phiếu phân bổ CCDC (Master - mỗi cặp Năm/Tháng một phiếu) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `ccdc_phieu_phan_bo_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Nam` | `nam` | `integer` | N | `0` | Năm phân bổ |
| 2 | `Thang` | `thang` | `integer` | N | `0` | Tháng phân bổ |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Đầu chứng từ]** Diễn giải |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Đầu chứng từ]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `ccdc_phieu_phan_bo_ccdc` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 0 | *(không)* |

---

## 17. `ccdc_phieu_phan_bo_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuPhanBoCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_chi_tiet_phieu_phan_bo_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chi tiết phân bổ (Detail - tab Xác định chi phí và phân bổ; · tab Hạch toán là preview gom nhóm từ các dòng này) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_phieu_phan_bo` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_phieu_phan_bo` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuPhanBoCCDCId` | `phieu_phan_bo_ccdc_id` | `uuid` | N | — | ID phiếu phân bổ (reference ENT_PhieuPhanBoCCDC) `FK` |
| 2 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC được phân bổ (reference ENT_CongCuDungCu) `FK` |
| 3 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản chi phí, vế Nợ (reference ENT_HeThongTaiKhoan) `FK` |
| 4 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | Y | — | ID tài khoản chờ phân bổ, vế Có (reference ENT_HeThongTaiKhoan) `FK` |
| 5 | `HeSo` | `he_so` | `exchange_rate` ≈ | N | `0` | Hệ số phân bổ |
| 6 | `GiaTriPhanBoKy` | `gia_tri_phan_bo_ky` | `money_foreign` ≈ | N | `0` | Giá trị phân bổ kỳ này |
| 7 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Trường tự do]** ID đơn vị sử dụng (reference ENT_DonVi) `FK` |
| 8 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID đối tượng tập hợp chi phí (reference ENT_DoiTuongTapHopChiPhi) `FK` |
| 9 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Trường tự do]** ID vụ việc (reference ENT_CongTrinh) `FK` |
| 10 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Trường tự do]** ID khoản mục chi phí (reference ENT_KhoanMucChiPhi) `FK` |
| 11 | `DonDatHangId` | `don_dat_hang_id` | `uuid` | Y | — | **[Trường tự do]** ID đơn đặt hàng (reference ENT_DonDatHang) `FK` |
| 12 | `HopDongBanHangId` | `hop_dong_ban_hang_id` | `uuid` | Y | — | **[Trường tự do]** ID hợp đồng bán hàng (reference ENT_HopDongBanHang) `FK` |

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

**Đối chiếu `ccdc_chi_tiet_phieu_phan_bo_ccdc` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 7 | `he_so`, `gia_tri_phan_bo_ky`, `don_vi_id`, `doi_tuong_tap_hop_chi_phi_id`, `vu_viec_id`, `don_dat_hang_id`, `hop_dong_ban_hang_id` |
| DB có — LDM **không khai** | 4 | `he_so_phan_bo`, `so_tien_phan_bo`, `don_vi_su_dung_id`, `dien_giai` |

---

## 18. `ccdc_tam_dung_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `TamDungPhanBoCCDC` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `ccdc_tam_dung_phan_bo_ccdc` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Tạm dừng / Tiếp tục phân bổ (popup từ màn danh sách CCDC) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `ccdc_cong_cu_dung_cu` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `ccdc_cong_cu_dung_cu` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `CongCuDungCuId` | `cong_cu_dung_cu_id` | `uuid` | N | — | ID CCDC tạm dừng phân bổ (reference ENT_CongCuDungCu) `FK` |
| 2 | `NgayTamDung` | `ngay_tam_dung` | `date` | N | — | Ngày tạm dừng phân bổ |
| 3 | `NgayTiepTuc` | `ngay_tiep_tuc` | `date` | Y | — | Ngày tiếp tục phân bổ |

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

**Đối chiếu `ccdc_tam_dung_phan_bo_ccdc` (13 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `ngay_tam_dung`, `ngay_tiep_tuc` |
| DB có — LDM **không khai** | 3 | `ngay_tam_dung_phan_bo`, `ngay_tiep_tuc_phan_bo`, `phien_ban` |

