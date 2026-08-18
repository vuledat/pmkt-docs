# `fa_` — Tài sản cố định

> Sinh tự động từ [`ldm-TaiSanCoDinh-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-TaiSanCoDinh-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**27 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> Chuyển hóa bảo thủ từ ldm-TaiSanCoDinh.puml: LoaiTaiSanCoDinh và NguonVon tham chiếu ldm-DanhMuc-Update.puml. LenhSanXuat tham chiếu ldm-Kho.puml, không định nghĩa trùng tại đây. Dấu * chỉ dùng cho khóa chính; dấu ! thể hiện trường bắt buộc. Tham chiếu danh mục lưu ID và Name snapshot; không lưu Code. Field hệ thống dùng chung không khai báo trong từng entity.

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ChungTuGhiGiamTSCD` | `fa_chung_tu_ghi_giam_tai_san_co_dinh` | `fa_chung_tu_ghi_giam_tscd` | B — có schema, chưa code | Đầu chứng từ — 1. Chứng từ ghi giảm TSCĐ |
| 2 | `ChiTietGhiGiamTSCD` | `fa_chung_tu_ghi_giam_tai_san_co_dinh_chi_tiet` | `fa_chi_tiet_ghi_giam_tscd` | B — có schema, chưa code | Dòng chi tiết của `fa_chung_tu_ghi_giam_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 3 | `HachToanGhiGiamTSCD` | `fa_hach_toan_ghi_giam_tai_san_co_dinh` | `fa_hach_toan_ghi_giam_tscd` | B — có schema, chưa code | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 4 | `ChungTuNgungKhauHao` | `fa_chung_tu_ngung_khau_hao` | `fa_chung_tu_ngung_khau_hao` | B — có schema, chưa code | Đầu chứng từ — 2. Khai báo thôi/tạm dừng khấu hao TSCĐ |
| 5 | `ChiTietNgungKhauHao` | `fa_chung_tu_ngung_khau_hao_chi_tiet` | `fa_chi_tiet_ngung_khau_hao` | B — có schema, chưa code | Dòng chi tiết của `fa_chung_tu_ngung_khau_hao` — ⚠ *LDM chưa mô tả bảng này* |
| 6 | `KiemKeTaiSanCoDinh` | `fa_kiem_ke_tai_san_co_dinh` | `fa_kiem_ke_tai_san_co_dinh` | B — có schema, chưa code | Bảng nghiệp vụ — 3. Kiểm kê TSCĐ |
| 7 | `ChiTietKiemKeTaiSanCoDinh` | `fa_kiem_ke_tai_san_co_dinh_chi_tiet` | `fa_chi_tiet_kiem_ke_tai_san_co_dinh` | B — có schema, chưa code | Dòng chi tiết của `fa_kiem_ke_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 8 | `ThanhVienKiemKeTaiSanCoDinh` | `fa_kiem_ke_tai_san_co_dinh_thanh_vien` | `fa_thanh_vien_kiem_ke_tai_san_co_dinh` | B — có schema, chưa code | Dòng chi tiết của `fa_kiem_ke_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 9 | `DieuChinhTaiSanCoDinh` | `fa_dieu_chinh_tai_san_co_dinh` | `fa_dieu_chinh_tai_san_co_dinh` | B — có schema, chưa code | Đầu chứng từ — 4. Điều chỉnh TSCĐ |
| 10 | `ThanhVienDieuChinhTaiSanCoDinh` | `fa_dieu_chinh_tai_san_co_dinh_thanh_vien` | `fa_thanh_vien_dieu_chinh_tai_san_co_dinh` | B — có schema, chưa code | Dòng chi tiết của `fa_dieu_chinh_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 11 | `ChiTietDieuChinhTaiSanCoDinh` | `fa_dieu_chinh_tai_san_co_dinh_chi_tiet` | `fa_chi_tiet_dieu_chinh_tai_san_co_dinh` | B — có schema, chưa code | Dòng chi tiết của `fa_dieu_chinh_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 12 | `HachToanDieuChinhTaiSanCoDinh` | `fa_hach_toan_dieu_chinh_tai_san_co_dinh` | `fa_hach_toan_dieu_chinh_tai_san_co_dinh` | B — có schema, chưa code | Bảng nghiệp vụ — ⚠ *LDM chưa mô tả bảng này* |
| 13 | `TaiSanCoDinh` | `fa_tai_san_co_dinh` | `fa_tai_san_co_dinh` | B — có schema, chưa code | Đầu chứng từ — 5. Ghi tăng và thông tin TSCĐ |
| 14 | `ChiTietNguonVonTaiSanCoDinh` | `fa_tai_san_co_dinh_nguon_von` | `fa_tai_san_co_dinh_nguon_von` | B — có schema, chưa code | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 15 | `ChiTietPhanBoTaiSanCoDinh` | `fa_tai_san_co_dinh_phan_bo` | `fa_tai_san_co_dinh_phan_bo` | B — có schema, chưa code | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 16 | `LichSuPhanBoTaiSanCoDinh` | `fa_tai_san_co_dinh_lich_su_phan_bo` | `fa_lich_su_phan_bo` | B — có schema, chưa code | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 17 | `PhuTungTaiSanCoDinh` | `fa_phu_tung_tai_san_co_dinh` | `fa_tai_san_co_dinh_phu_tung` | B — có schema, chưa code | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 18 | `BoPhanCauThanhTaiSanCoDinh` | `fa_bo_phan_cau_thanh_tai_san_co_dinh` | `fa_tai_san_co_dinh_bo_phan_cau_thanh` | B — có schema, chưa code | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 19 | `ThongTinKhacTaiSanCoDinh` | `fa_thong_tin_khac_tai_san_co_dinh` | `fa_tai_san_co_dinh_thong_tin_khac` | B — có schema, chưa code | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 20 | `LienKetChungTuTaiSanCoDinh` | `fa_lien_ket_chung_tu_tai_san_co_dinh` | `fa_tai_san_co_dinh_lien_ket_chung_tu` | B — có schema, chưa code | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 21 | `KhaiBaoSanLuong` | `fa_khai_bao_san_luong` | `fa_khai_bao_san_luong` | B — có schema, chưa code | Cấu hình / thiết lập — 6. Khai báo sản lượng |
| 22 | `ChiTietKhaiBaoSanLuong` | `fa_khai_bao_san_luong_chi_tiet` | `fa_chi_tiet_khai_bao_san_luong` | B — có schema, chưa code | Dòng chi tiết của `fa_khai_bao_san_luong` — ⚠ *LDM chưa mô tả bảng này* |
| 23 | `DieuChuyenTaiSan` | `fa_dieu_chuyen_tai_san` | `fa_dieu_chuyen_tai_san` | B — có schema, chưa code | Đầu chứng từ — 7. Điều chuyển TSCĐ |
| 24 | `ChiTietDieuChuyenTaiSan` | `fa_dieu_chuyen_tai_san_chi_tiet` | `fa_chi_tiet_dieu_chuyen` | B — có schema, chưa code | Dòng chi tiết của `fa_dieu_chuyen_tai_san` — ⚠ *LDM chưa mô tả bảng này* |
| 25 | `LichSuDieuChuyenTaiSan` | `fa_tai_san_co_dinh_lich_su_dieu_chuyen` | — | C — tạo mới | Dòng chi tiết của `fa_tai_san_co_dinh` — ⚠ *LDM chưa mô tả bảng này* |
| 26 | `KhauHaoTaiSan` | `fa_khau_hao_tai_san` | `fa_khau_hao_tai_san` | B — có schema, chưa code | Đầu chứng từ — 8. Khấu hao TSCĐ |
| 27 | `ChiTietKhauHaoTaiSan` | `fa_khau_hao_tai_san_chi_tiet` | `fa_chi_tiet_khau_hao_tai_san` | B — có schema, chưa code | Dòng chi tiết của `fa_khau_hao_tai_san` — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `fa_chung_tu_ghi_giam_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuGhiGiamTSCD` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chung_tu_ghi_giam_tscd` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 1. Chứng từ ghi giảm TSCĐ |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `fa_chung_tu_ghi_giam_tai_san_co_dinh_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | Lý do ghi giảm (reference ENT_TaiKhoanNgamDinh) `FK` |
| 2 | `TenTaiKhoanNgamDinh` | `ten_tai_khoan_ngam_dinh` | `text` | Y | — | Tên lý do ghi giảm (snapshot) |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải lý do ghi giảm |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | Y | — | Trạng thái ghi sổ (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `fa_chung_tu_ghi_giam_tscd` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `tai_khoan_ngam_dinh_id`, `ten_tai_khoan_ngam_dinh`, `dien_giai` |
| DB có — LDM **không khai** | 2 | `ly_do_tang_giam_id`, `mo_ta` |

---

## 2. `fa_chung_tu_ghi_giam_tai_san_co_dinh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietGhiGiamTSCD` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chi_tiet_ghi_giam_tscd` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_chung_tu_ghi_giam_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_chung_tu_ghi_giam_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuGhiGiamTSCDId` | `chung_tu_ghi_giam_tscd_id` | `uuid` | Y | — | ID chứng từ ghi giảm TSCĐ `FK` |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | N | — | ID TSCĐ `FK` |
| 3 | `TaiKhoanXuLyGTCLId` | `tai_khoan_xu_ly_gtcl_id` | `uuid` | Y | — | ID tài khoản xử lý giá trị còn lại `FK` |
| 4 | `TenTaiKhoanXuLyGTCL` | `ten_tai_khoan_xu_ly_gtcl` | `text` | Y | — | Snapshot tên tài khoản xử lý giá trị còn lại |

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

**Đối chiếu `fa_chi_tiet_ghi_giam_tscd` (13 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `tai_khoan_xu_ly_gtcl_id`, `ten_tai_khoan_xu_ly_gtcl` |
| DB có — LDM **không khai** | 2 | `tai_khoan_xu_ly_gtcl`, `phien_ban` |

---

## 3. `fa_hach_toan_ghi_giam_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HachToanGhiGiamTSCD` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_hach_toan_ghi_giam_tscd` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChiTietGhiGiamTSCDId` | `chi_tiet_ghi_giam_tscd_id` | `uuid` | Y | — | ID chi tiết ghi giảm TSCĐ `FK` |
| 2 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản Nợ `FK` |
| 3 | `TenTaiKhoanNo` | `ten_tai_khoan_no` | `text` | N | — | Snapshot tên tài khoản Nợ |
| 4 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản Có `FK` |
| 5 | `TenTaiKhoanCo` | `ten_tai_khoan_co` | `text` | N | — | Snapshot tên tài khoản Có |
| 6 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | Số tiền hạch toán |
| 7 | `GhiChu` | `ghi_chu` | `text` | N | — | Diễn giải hạch toán |
| 8 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 9 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |

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

**Đối chiếu `fa_hach_toan_ghi_giam_tscd` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `ten_tai_khoan_no`, `ten_tai_khoan_co`, `ghi_chu`, `ten_khoan_muc_chi_phi` |
| DB có — LDM **không khai** | 2 | `chu_thich`, `phien_ban` |

---

## 4. `fa_chung_tu_ngung_khau_hao`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuNgungKhauHao` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chung_tu_ngung_khau_hao` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 2. Khai báo thôi/tạm dừng khấu hao TSCĐ |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `fa_chung_tu_ngung_khau_hao_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Loai` | `loai` | `text` CHECK | N | — | ThoiKhauHao \| TamDungKhauHao |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải lý do khai báo |

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

**Đối chiếu `fa_chung_tu_ngung_khau_hao` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 1 | `mo_ta` |

---

## 5. `fa_chung_tu_ngung_khau_hao_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietNgungKhauHao` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chi_tiet_ngung_khau_hao` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_chung_tu_ngung_khau_hao` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_chung_tu_ngung_khau_hao` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuNgungKhauHaoId` | `chung_tu_ngung_khau_hao_id` | `uuid` | Y | — | ID chứng từ ngừng khấu hao `FK` |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | N | — | ID TSCĐ `FK` |
| 3 | `NgayHieuLuc` | `ngay_hieu_luc` | `date` | N | — | Ngày hiệu lực |
| 4 | `NgayHetHieuLuc` | `ngay_het_hieu_luc` | `date` | Y | — | Ngày hết hiệu lực |

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

**Đối chiếu `fa_chi_tiet_ngung_khau_hao` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 6. `fa_kiem_ke_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KiemKeTaiSanCoDinh` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_kiem_ke_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 3. Kiểm kê TSCĐ |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `fa_kiem_ke_tai_san_co_dinh_chi_tiet` · `fa_kiem_ke_tai_san_co_dinh_thanh_vien` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `SoPhieu` | `so_phieu` | `text` | N | — | Số phiếu kiểm kê |
| 2 | `NgayKiemKe` | `ngay_kiem_ke` | `timestamptz` | N | — | Ngày kiểm kê |
| 3 | `NoiDungKiemKe` | `noi_dung_kiem_ke` | `text` | Y | — | Nội dung kiểm kê |
| 4 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

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

**Đối chiếu `fa_kiem_ke_tai_san_co_dinh` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 3 | `phong_ban`, `mo_ta`, `phien_ban` |

---

## 7. `fa_kiem_ke_tai_san_co_dinh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietKiemKeTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chi_tiet_kiem_ke_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_kiem_ke_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_kiem_ke_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KiemKeTaiSanCoDinhId` | `kiem_ke_tai_san_co_dinh_id` | `uuid` | N | — | ID biên bản kiểm kê `FK` |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | N | — | ID TSCĐ `FK` |
| 3 | `KiemDem` | `kiem_dem` | `boolean` | N | `false` | TSCĐ còn tồn tại hay không |
| 4 | `TinhTrang` | `tinh_trang` | `text` CHECK | N | — | Tot \| Kem \| Hong \| KhongXacDinh |
| 5 | `DienGiai` | `dien_giai` | `text` | Y | — | Ghi chú |

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

**Đối chiếu `fa_chi_tiet_kiem_ke_tai_san_co_dinh` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `tai_san_co_dinh_id`, `dien_giai` |
| DB có — LDM **không khai** | 3 | `ma_tai_san_co_dinh_id`, `mo_ta`, `phien_ban` |

---

## 8. `fa_kiem_ke_tai_san_co_dinh_thanh_vien`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThanhVienKiemKeTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_thanh_vien_kiem_ke_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_kiem_ke_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_kiem_ke_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KiemKeTaiSanCoDinhId` | `kiem_ke_tai_san_co_dinh_id` | `uuid` | N | — | ID biên bản kiểm kê `FK` |
| 2 | `HoTen` | `ho_ten` | `text` | N | — | Họ tên người kiểm kê |
| 3 | `ChucDanh` | `chuc_danh` | `text` | Y | — | Chức danh người kiểm kê |
| 4 | `DaiDien` | `dai_dien` | `text` | Y | — | Thông tin đại diện |
| 5 | `DienGiai` | `dien_giai` | `text` | Y | — | Ghi chú bổ sung |

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

**Đối chiếu `fa_thanh_vien_kiem_ke_tai_san_co_dinh` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 2 | `mo_ta`, `phien_ban` |

---

## 9. `fa_dieu_chinh_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DieuChinhTaiSanCoDinh` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_dieu_chinh_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 4. Điều chỉnh TSCĐ |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `fa_dieu_chinh_tai_san_co_dinh_thanh_vien` · `fa_dieu_chinh_tai_san_co_dinh_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | Lý do điều chỉnh/đánh giá lại (reference ENT_TaiKhoanNgamDinh) `FK` |
| 2 | `TenTaiKhoanNgamDinh` | `ten_tai_khoan_ngam_dinh` | `text` | Y | — | Tên lý do điều chỉnh (snapshot) |
| 3 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | Trạng thái ghi sổ (ChuaGhiSo \| DaGhiSo) |
| 4 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải lý do khác |

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

**Đối chiếu `fa_dieu_chinh_tai_san_co_dinh` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `tai_khoan_ngam_dinh_id`, `ten_tai_khoan_ngam_dinh`, `dien_giai` |
| DB có — LDM **không khai** | 3 | `ly_do_tang_giam_id`, `noi_dung`, `mo_ta` |

---

## 10. `fa_dieu_chinh_tai_san_co_dinh_thanh_vien`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThanhVienDieuChinhTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_thanh_vien_dieu_chinh_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_dieu_chinh_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_dieu_chinh_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DieuChinhTaiSanCoDinhId` | `dieu_chinh_tai_san_co_dinh_id` | `uuid` | N | — | ID chứng từ điều chỉnh `FK` |
| 2 | `HoTen` | `ho_ten` | `text` | N | — | Họ tên thành viên |
| 3 | `ChucDanh` | `chuc_danh` | `text` | Y | — | Chức danh thành viên |
| 4 | `DaiDien` | `dai_dien` | `text` | Y | — | Thông tin đại diện |

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

**Đối chiếu `fa_thanh_vien_dieu_chinh_tai_san_co_dinh` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 11. `fa_dieu_chinh_tai_san_co_dinh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDieuChinhTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chi_tiet_dieu_chinh_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_dieu_chinh_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_dieu_chinh_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DieuChinhTaiSanCoDinhId` | `dieu_chinh_tai_san_co_dinh_id` | `uuid` | N | — | ID chứng từ điều chỉnh `FK` |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | N | — | ID TSCĐ `FK` |
| 3 | `NguonVonId` | `nguon_von_id` | `uuid` | N | — | ID nguồn vốn `FK` |
| 4 | `TenNguonVon` | `ten_nguon_von` | `text` | N | — | Snapshot tên nguồn vốn |
| 5 | `GiaTriConLaiTruocDC` | `gia_tri_con_lai_truoc_dc` | `money_foreign` ≈ | Y | `0` | Giá trị còn lại trước điều chỉnh |
| 6 | `GiaTriConLaiSauDC` | `gia_tri_con_lai_sau_dc` | `money_foreign` ≈ | N | `0` | Giá trị còn lại sau điều chỉnh |
| 7 | `ChenhLechGiaTriConLai` | `chenh_lech_gia_tri_con_lai` | `money_foreign` ≈ | Y | `0` | Chênh lệch giá trị còn lại |
| 8 | `ThoiGianSuDungTruocDC` | `thoi_gian_su_dung_truoc_dc` | `numeric(18,4)` ⚠ | Y | `0` | Thời gian sử dụng còn lại trước điều chỉnh, tính theo tháng |
| 9 | `ThoiGianSuDungSauDC` | `thoi_gian_su_dung_sau_dc` | `numeric(18,4)` ⚠ | N | `0` | Thời gian sử dụng còn lại sau điều chỉnh, tính theo tháng |
| 10 | `ChenhLechThoiGianSuDung` | `chenh_lech_thoi_gian_su_dung` | `numeric(18,4)` ⚠ | Y | `0` | Chênh lệch thời gian sử dụng |
| 11 | `HaoMonLuyKeTruocDC` | `hao_mon_luy_ke_truoc_dc` | `money_foreign` ≈ | Y | `0` | Hao mòn lũy kế trước điều chỉnh |
| 12 | `HaoMonLuyKeSauDC` | `hao_mon_luy_ke_sau_dc` | `money_foreign` ≈ | N | `0` | Hao mòn lũy kế sau điều chỉnh |
| 13 | `ChenhLechHaoMonLuyKe` | `chenh_lech_hao_mon_luy_ke` | `money_foreign` ≈ | Y | `0` | Chênh lệch hao mòn lũy kế |
| 14 | `TaiKhoanChiPhiHaoMonId` | `tai_khoan_chi_phi_hao_mon_id` | `uuid` | N | — | ID tài khoản chi phí khấu hao `FK` |
| 15 | `TenTaiKhoanChiPhiHaoMon` | `ten_tai_khoan_chi_phi_hao_mon` | `text` | N | — | Snapshot tên tài khoản chi phí khấu hao |
| 16 | `TaiKhoanDoiUngHaoMonId` | `tai_khoan_doi_ung_hao_mon_id` | `uuid` | N | — | ID tài khoản đối ứng điều chỉnh hao mòn lũy kế `FK` |
| 17 | `TenTaiKhoanDoiUngHaoMon` | `ten_tai_khoan_doi_ung_hao_mon` | `text` | N | — | Snapshot tên tài khoản đối ứng hao mòn |
| 18 | `NguyenGiaTruocDC` | `nguyen_gia_truoc_dc` | `money_foreign` ≈ | Y | `0` | Nguyên giá trước điều chỉnh |
| 19 | `NguyenGiaSauDC` | `nguyen_gia_sau_dc` | `money_foreign` ≈ | Y | `0` | Nguyên giá sau điều chỉnh |
| 20 | `ChenhLechNguyenGia` | `chenh_lech_nguyen_gia` | `money_foreign` ≈ | Y | `0` | Chênh lệch nguyên giá |
| 21 | `TaiKhoanDieuChinhNguyenGiaId` | `tai_khoan_dieu_chinh_nguyen_gia_id` | `uuid` | N | — | ID tài khoản điều chỉnh nguyên giá `FK` |
| 22 | `TenTaiKhoanDieuChinhNguyenGia` | `ten_tai_khoan_dieu_chinh_nguyen_gia` | `text` | N | — | Snapshot tên tài khoản điều chỉnh nguyên giá |
| 23 | `TaiKhoanDoiUngNguyenGiaId` | `tai_khoan_doi_ung_nguyen_gia_id` | `uuid` | N | — | ID tài khoản đối ứng điều chỉnh nguyên giá `FK` |
| 24 | `TenTaiKhoanDoiUngNguyenGia` | `ten_tai_khoan_doi_ung_nguyen_gia` | `text` | N | — | Snapshot tên tài khoản đối ứng nguyên giá |
| 25 | `SanLuongTruocDC` | `san_luong_truoc_dc` | `numeric(18,4)` ⚠ | Y | `0` | Sản lượng còn lại trước điều chỉnh |
| 26 | `SanLuongSauDC` | `san_luong_sau_dc` | `numeric(18,4)` ⚠ | Y | `0` | Sản lượng còn lại sau điều chỉnh |
| 27 | `ChenhLechSanLuong` | `chenh_lech_san_luong` | `numeric(18,4)` ⚠ | Y | `0` | Chênh lệch sản lượng |

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

**Đối chiếu `fa_chi_tiet_dieu_chinh_tai_san_co_dinh` (34 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `tai_san_co_dinh_id`, `ten_nguon_von`, `ten_tai_khoan_chi_phi_hao_mon`, `ten_tai_khoan_doi_ung_hao_mon`, `ten_tai_khoan_dieu_chinh_nguyen_gia`, `ten_tai_khoan_doi_ung_nguyen_gia` |
| DB có — LDM **không khai** | 4 | `ma_tai_san_co_dinh_id`, `loai_dieu_chinh`, `mo_ta`, `phien_ban` |

---

## 12. `fa_hach_toan_dieu_chinh_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HachToanDieuChinhTaiSanCoDinh` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_hach_toan_dieu_chinh_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChiTietDieuChinhTaiSanCoDinhId` | `chi_tiet_dieu_chinh_tai_san_co_dinh_id` | `uuid` | N | — | ID chi tiết chứng từ điều chỉnh `FK` |
| 2 | `Loai` | `loai` | `text` CHECK | N | — | DieuChinhNguyenGia \| DieuChinhHaoMonLuyKe |
| 3 | `DieuHuong` | `dieu_huong` | `text` CHECK | N | — | Tang \| Giam |
| 4 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản Nợ `FK` |
| 5 | `TenTaiKhoanNo` | `ten_tai_khoan_no` | `text` | N | — | Snapshot tên tài khoản Nợ |
| 6 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản Có `FK` |
| 7 | `TenTaiKhoanCo` | `ten_tai_khoan_co` | `text` | N | — | Snapshot tên tài khoản Có |
| 8 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | Số tiền điều chỉnh |
| 9 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải bút toán |
| 10 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 11 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |
| 12 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID công trình `FK` |
| 13 | `TenCongTrinh` | `ten_cong_trinh` | `text` | Y | — | Snapshot tên công trình |

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

**Đối chiếu `fa_hach_toan_dieu_chinh_tai_san_co_dinh` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `ten_tai_khoan_no`, `ten_tai_khoan_co`, `dien_giai`, `ten_khoan_muc_chi_phi`, `vu_viec_id`, `ten_cong_trinh` |
| DB có — LDM **không khai** | 4 | `references`, `mo_ta`, `cong_trinh_id`, `phien_ban` |

---

## 13. `fa_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `TaiSanCoDinh` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_tai_san_co_dinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 5. Ghi tăng và thông tin TSCĐ |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `fa_tai_san_co_dinh_nguon_von` · `fa_tai_san_co_dinh_phan_bo` · `fa_tai_san_co_dinh_lich_su_phan_bo` · `fa_phu_tung_tai_san_co_dinh` · `fa_bo_phan_cau_thanh_tai_san_co_dinh` · `fa_thong_tin_khac_tai_san_co_dinh` · `fa_lien_ket_chung_tu_tai_san_co_dinh` · `fa_tai_san_co_dinh_lich_su_dieu_chuyen` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NgayGhiTang` | `ngay_ghi_tang` | `date` | N | — | Ngày hạch toán ghi tăng |
| 2 | `SoDuDauKy` | `so_du_dau_ky` | `boolean` | N | `false` | Có số dư đầu kỳ hay không |
| 3 | `MaTaiSan` | `ma_tai_san` | `text` | N | — | Mã tài sản `UNIQUE` |
| 4 | `TenTaiSan` | `ten_tai_san` | `text` | N | — | Tên tài sản |
| 5 | `LoaiTaiSanCoDinhId` | `loai_tai_san_co_dinh_id` | `uuid` | N | — | ID loại TSCĐ `FK` |
| 6 | `TenLoaiTaiSanCoDinh` | `ten_loai_tai_san_co_dinh` | `text` | N | — | Snapshot tên loại TSCĐ |
| 7 | `BoPhanQuanLyId` | `bo_phan_quan_ly_id` | `uuid` | N | — | ID bộ phận/phòng ban quản lý `FK` |
| 8 | `TenBoPhanQuanLy` | `ten_bo_phan_quan_ly` | `text` | N | — | Snapshot tên bộ phận/phòng ban quản lý |
| 9 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | HoatDong \| TamDungKhauHao \| ThoiKhauHao \| HoanThanhKhauHao \| DaGhiGiam |
| 10 | `NguonGocHinhThanhId` | `nguon_goc_hinh_thanh_id` | `uuid` | Y | — | ID nguồn gốc hình thành `FK` |
| 11 | `TenNguonGocHinhThanh` | `ten_nguon_goc_hinh_thanh` | `text` | Y | — | Snapshot tên nguồn gốc hình thành |
| 12 | `NgayBatDauKhauHao` | `ngay_bat_dau_khau_hao` | `date` | N | — | Ngày bắt đầu tính khấu hao |
| 13 | `ThoiGianKhauHao` | `thoi_gian_khau_hao` | `money_foreign` ≈ | N | `0` | Thời gian khấu hao |
| 14 | `TaiKhoanNguyenGiaId` | `tai_khoan_nguyen_gia_id` | `uuid` | N | — | ID tài khoản nguyên giá `FK` |
| 15 | `TenTaiKhoanNguyenGia` | `ten_tai_khoan_nguyen_gia` | `text` | N | — | Snapshot tên tài khoản nguyên giá |
| 16 | `NguyenGia` | `nguyen_gia` | `money_foreign` ≈ | N | `0` | Nguyên giá tổng |
| 17 | `GiaTriTinhKhauHao` | `gia_tri_tinh_khau_hao` | `money_foreign` ≈ | N | `0` | Giá trị tính khấu hao |
| 18 | `TaiKhoanKhauHaoId` | `tai_khoan_khau_hao_id` | `uuid` | N | — | ID tài khoản khấu hao `FK` |
| 19 | `TenTaiKhoanKhauHao` | `ten_tai_khoan_khau_hao` | `text` | N | — | Snapshot tên tài khoản khấu hao |
| 20 | `TaiKhoanChiPhiMacDinhId` | `tai_khoan_chi_phi_mac_dinh_id` | `uuid` | N | — | ID tài khoản chi phí mặc định `FK` |
| 21 | `TenTaiKhoanChiPhiMacDinh` | `ten_tai_khoan_chi_phi_mac_dinh` | `text` | N | — | Snapshot tên tài khoản chi phí mặc định |
| 22 | `PhuongPhapKhauHao` | `phuong_phap_khau_hao` | `text` CHECK | N | — | Phương pháp khấu hao (DuongThang \| SanLuong \| SoDuGiamDanCoDieuChinh) |
| 23 | `TyLeKhauHaoNam` | `ty_le_khau_hao_nam` | `percent_rate` | Y | `0` | Tỷ lệ khấu hao năm |
| 24 | `GiaTriKhauHaoNam` | `gia_tri_khau_hao_nam` | `money_foreign` ≈ | Y | `0` | Giá trị khấu hao năm |
| 25 | `TyLeKhauHaoThang` | `ty_le_khau_hao_thang` | `percent_rate` | Y | `0` | Tỷ lệ khấu hao tháng |
| 26 | `GiaTriKhauHaoThang` | `gia_tri_khau_hao_thang` | `money_foreign` ≈ | Y | `0` | Giá trị khấu hao tháng |
| 27 | `TongSanLuong` | `tong_san_luong` | `money_foreign` ≈ | Y | `0` | Tổng sản lượng/công suất thiết kế |
| 28 | `TyLeKhauHaoHangNam` | `ty_le_khau_hao_hang_nam` | `percent_rate` | Y | `0` | Tỷ lệ khấu hao hằng năm |
| 29 | `HeSoDieuChinh` | `he_so_dieu_chinh` | `numeric(18,4)` ⚠ | Y | `0` | Hệ số điều chỉnh |
| 30 | `TyLeKhauHaoNhanh` | `ty_le_khau_hao_nhanh` | `percent_rate` | Y | `0` | Tỷ lệ khấu hao nhanh |

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

**Đối chiếu `fa_tai_san_co_dinh` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 26 | `ngay_ghi_tang`, `ma_tai_san`, `ten_tai_san`, `loai_tai_san_co_dinh_id`, `ten_loai_tai_san_co_dinh`, `bo_phan_quan_ly_id`, `ten_bo_phan_quan_ly`, `ten_nguon_goc_hinh_thanh`, `ngay_bat_dau_khau_hao`, `thoi_gian_khau_hao`, `tai_khoan_nguyen_gia_id`, `ten_tai_khoan_nguyen_gia`, `nguyen_gia`, `gia_tri_tinh_khau_hao`, `tai_khoan_khau_hao_id`, `ten_tai_khoan_khau_hao`, `tai_khoan_chi_phi_mac_dinh_id`, `ten_tai_khoan_chi_phi_mac_dinh`, `ty_le_khau_hao_nam`, `gia_tri_khau_hao_nam`, `ty_le_khau_hao_thang`, `gia_tri_khau_hao_thang`, `tong_san_luong`, `ty_le_khau_hao_hang_nam`, `he_so_dieu_chinh`, `ty_le_khau_hao_nhanh` |
| DB có — LDM **không khai** | 3 | `hao_mon_luy_ke`, `ma`, `ten` |

---

## 14. `fa_tai_san_co_dinh_nguon_von`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietNguonVonTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_tai_san_co_dinh_nguon_von` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 2 | `NguonVonId` | `nguon_von_id` | `uuid` | Y | — | ID nguồn vốn `FK` |
| 3 | `TenNguonVon` | `ten_nguon_von` | `text` | Y | — | Snapshot tên nguồn vốn |
| 4 | `NguyenGia` | `nguyen_gia` | `money_foreign` ≈ | Y | `0` | Nguyên giá theo nguồn vốn |
| 5 | `GiaTriTinhKhauHao` | `gia_tri_tinh_khau_hao` | `money_foreign` ≈ | Y | `0` | Giá trị tính khấu hao theo nguồn vốn |
| 6 | `GiaTriDaKhauHao` | `gia_tri_da_khau_hao` | `money_foreign` ≈ | Y | `0` | Giá trị đã khấu hao |
| 7 | `GiaTriConLai` | `gia_tri_con_lai` | `money_foreign` ≈ | Y | `0` | Giá trị còn lại |
| 8 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải chi tiết |
| 9 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID công trình/vụ việc `FK` |
| 10 | `TenCongTrinh` | `ten_cong_trinh` | `text` | Y | — | Snapshot tên công trình/vụ việc |
| 11 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 12 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |
| 13 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | ID hợp đồng `FK` |
| 14 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | Y | — | ID lệnh sản xuất, tham chiếu LenhSanXuat trong ldm-Kho.puml `FK` |

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

**Đối chiếu `fa_tai_san_co_dinh_nguon_von` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `ten_nguon_von`, `gia_tri_tinh_khau_hao`, `ten_cong_trinh`, `ten_khoan_muc_chi_phi` |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 15. `fa_tai_san_co_dinh_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhanBoTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_tai_san_co_dinh_phan_bo` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 2 | `DonViId` | `don_vi_id` | `uuid` | N | — | ID đơn vị sử dụng/chịu phí `FK` |
| 3 | `TenDonVi` | `ten_don_vi` | `text` | N | — | Snapshot tên đơn vị |
| 4 | `HeSo` | `he_so` | `exchange_rate` ≈ | N | `0` | Hệ số/tỷ lệ phân bổ |
| 5 | `TaiKhoanChoPhanBoId` | `tai_khoan_cho_phan_bo_id` | `uuid` | Y | — | ID tài khoản chờ phân bổ/Tài khoản Có `FK` |
| 6 | `TenTaiKhoanChoPhanBo` | `ten_tai_khoan_cho_phan_bo` | `text` | Y | — | Snapshot tên tài khoản chờ phân bổ |
| 7 | `TaiKhoanChiPhiId` | `tai_khoan_chi_phi_id` | `uuid` | N | — | ID tài khoản chi phí/Tài khoản Nợ `FK` |
| 8 | `TenTaiKhoanChiPhi` | `ten_tai_khoan_chi_phi` | `text` | N | — | Snapshot tên tài khoản chi phí |
| 9 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID công trình/vụ việc `FK` |
| 10 | `TenCongTrinh` | `ten_cong_trinh` | `text` | Y | — | Snapshot tên công trình/vụ việc |
| 11 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 12 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |
| 13 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | ID hợp đồng `FK` |
| 14 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | Y | — | ID lệnh sản xuất, tham chiếu LenhSanXuat trong ldm-Kho.puml `FK` |
| 15 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

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

**Đối chiếu `fa_tai_san_co_dinh_phan_bo` (23 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 5 | `ten_don_vi`, `ten_tai_khoan_cho_phan_bo`, `ten_tai_khoan_chi_phi`, `ten_cong_trinh`, `ten_khoan_muc_chi_phi` |
| DB có — LDM **không khai** | 4 | `ngay_co_hieu_luc`, `loai_chung_tu_goc`, `id_chung_tu_goc`, `phien_ban` |

---

## 16. `fa_tai_san_co_dinh_lich_su_phan_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `LichSuPhanBoTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_lich_su_phan_bo` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoangThoiGianSuDung` | `khoang_thoi_gian_su_dung` | `text` | N | — | Khoảng thời gian đơn vị sử dụng TSCĐ |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 3 | `DonViId` | `don_vi_id` | `uuid` | N | — | ID đơn vị `FK` |
| 4 | `TenDonVi` | `ten_don_vi` | `text` | N | — | Snapshot tên đơn vị |
| 5 | `HeSo` | `he_so` | `exchange_rate` ≈ | N | `0` | Hệ số phân bổ |
| 6 | `TaiKhoanChiPhiId` | `tai_khoan_chi_phi_id` | `uuid` | N | — | ID tài khoản chi phí `FK` |
| 7 | `TenTaiKhoanChiPhi` | `ten_tai_khoan_chi_phi` | `text` | N | — | Snapshot tên tài khoản chi phí |
| 8 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID công trình/vụ việc `FK` |
| 9 | `TenCongTrinh` | `ten_cong_trinh` | `text` | Y | — | Snapshot tên công trình/vụ việc |
| 10 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 11 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |
| 12 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | ID hợp đồng `FK` |
| 13 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | Y | — | ID lệnh sản xuất, tham chiếu LenhSanXuat trong ldm-Kho.puml `FK` |
| 14 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |

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

**Đối chiếu `fa_lich_su_phan_bo` (21 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `ten_don_vi`, `ten_tai_khoan_chi_phi`, `ten_cong_trinh`, `ten_khoan_muc_chi_phi` |
| DB có — LDM **không khai** | 2 | `phien_ban`, `ngay_co_hieu_luc` |

---

## 17. `fa_phu_tung_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhuTungTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_tai_san_co_dinh_phu_tung` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 2 | `TenPhuTung` | `ten_phu_tung` | `text` | Y | — | Tên phụ tùng |
| 3 | `DonViTinh` | `don_vi_tinh` | `text` | Y | — | Đơn vị tính |
| 4 | `SoLuong` | `so_luong` | `quantity` | Y | `0` | Số lượng |
| 5 | `GiaTri` | `gia_tri` | `money_foreign` ≈ | Y | `0` | Giá trị ước tính |

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

**Đối chiếu `fa_tai_san_co_dinh_phu_tung` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 18. `fa_bo_phan_cau_thanh_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `BoPhanCauThanhTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_tai_san_co_dinh_bo_phan_cau_thanh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 2 | `TenBoPhan` | `ten_bo_phan` | `text` | Y | — | Tên bộ phận cấu thành |
| 3 | `DonViTinh` | `don_vi_tinh` | `text` | Y | — | Đơn vị tính |
| 4 | `SoLuong` | `so_luong` | `quantity` | Y | `0` | Số lượng |
| 5 | `ThoiHanBaoHanh` | `thoi_han_bao_hanh` | `text` | Y | — | Thời hạn bảo hành riêng |

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

**Đối chiếu `fa_tai_san_co_dinh_bo_phan_cau_thanh` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 19. `fa_thong_tin_khac_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThongTinKhacTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_tai_san_co_dinh_thong_tin_khac` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 2 | `NhaSanXuat` | `nha_san_xuat` | `text` | Y | — | Nhà sản xuất |
| 3 | `NamSanXuat` | `nam_san_xuat` | `integer` | Y | `0` | Năm sản xuất |
| 4 | `NuocSanXuat` | `nuoc_san_xuat` | `text` | Y | — | Nước sản xuất |
| 5 | `CongSuat` | `cong_suat` | `text` | Y | — | Công suất |
| 6 | `ThoiHanBaoHanh` | `thoi_han_bao_hanh` | `text` | Y | — | Thời hạn bảo hành |
| 7 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | Y | — | ID nhà cung cấp, tham chiếu DoiTuong `FK` |
| 8 | `TenNhaCungCap` | `ten_nha_cung_cap` | `text` | Y | — | Snapshot tên nhà cung cấp |
| 9 | `DieuKienBaoHanh` | `dieu_kien_bao_hanh` | `text` | Y | — | Điều kiện bảo hành |
| 10 | `BienBanBanGiao` | `bien_ban_ban_giao` | `text` | Y | — | Số biên bản bàn giao |
| 11 | `NgayBienBan` | `ngay_bien_ban` | `date` | Y | — | Ngày biên bản bàn giao |

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

**Đối chiếu `fa_tai_san_co_dinh_thong_tin_khac` (19 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `ten_nha_cung_cap`, `ngay_bien_ban` |
| DB có — LDM **không khai** | 1 | `phien_ban` |

---

## 20. `fa_lien_ket_chung_tu_tai_san_co_dinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `LienKetChungTuTaiSanCoDinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_tai_san_co_dinh_lien_ket_chung_tu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 2 | `ChungTuId` | `chung_tu_id` | `uuid` | Y | — | ID chứng từ gốc `FK` |
| 3 | `TenLoaiChungTu` | `ten_loai_chung_tu` | `text` | Y | — | Snapshot tên loại chứng từ |

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

**Đối chiếu `fa_tai_san_co_dinh_lien_ket_chung_tu` (15 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `chung_tu_id`, `ten_loai_chung_tu` |
| DB có — LDM **không khai** | 5 | `chung_tu_tham_chieu_id`, `loai_chung_tu_id`, `so_chung_tu`, `ngay_chung_tu`, `phien_ban` |

---

## 21. `fa_khai_bao_san_luong`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KhaiBaoSanLuong` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_khai_bao_san_luong` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 6. Khai báo sản lượng |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng con | `fa_khai_bao_san_luong_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Thang` | `thang` | `integer` | N | `0` | Tháng khai báo, từ 1 đến 12 |
| 2 | `Nam` | `nam` | `integer` | N | `0` | Năm tài chính |

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

**Đối chiếu `fa_khai_bao_san_luong` (13 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 2 | `mo_ta`, `phien_ban` |

---

## 22. `fa_khai_bao_san_luong_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietKhaiBaoSanLuong` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chi_tiet_khai_bao_san_luong` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_khai_bao_san_luong` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_khai_bao_san_luong` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhaiBaoSanLuongId` | `khai_bao_san_luong_id` | `uuid` | N | — | ID phiếu khai báo sản lượng `FK` |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | N | — | ID TSCĐ `FK` |
| 3 | `SanLuongThangNay` | `san_luong_thang_nay` | `numeric(18,4)` ⚠ | Y | `0` | Sản lượng thực tế trong tháng, phải lớn hơn hoặc bằng 0 |

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

**Đối chiếu `fa_chi_tiet_khai_bao_san_luong` (13 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `san_luong_thang_nay` |
| DB có — LDM **không khai** | 2 | `san_luong_ky_nay`, `phien_ban` |

---

## 23. `fa_dieu_chuyen_tai_san`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DieuChuyenTaiSan` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_dieu_chuyen_tai_san` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 7. Điều chuyển TSCĐ |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `fa_dieu_chuyen_tai_san_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NgayDieuChuyen` | `ngay_dieu_chuyen` | `date` | N | — | Ngày hiệu lực điều chuyển |
| 2 | `NguoiGiao` | `nguoi_giao` | `text` | N | — | Tên người giao |
| 3 | `NguoiNhan` | `nguoi_nhan` | `text` | N | — | Tên người nhận |
| 4 | `LyDo` | `ly_do` | `text` | Y | — | Lý do điều chuyển |

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

**Đối chiếu `fa_dieu_chuyen_tai_san` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `trang_thai` |

---

## 24. `fa_dieu_chuyen_tai_san_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDieuChuyenTaiSan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chi_tiet_dieu_chuyen` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_dieu_chuyen_tai_san` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_dieu_chuyen_tai_san` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DieuChuyenTaiSanId` | `dieu_chuyen_tai_san_id` | `uuid` | N | — | ID phiếu điều chuyển `FK` |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | N | — | ID TSCĐ `FK` |
| 3 | `DonViBanGiaoId` | `don_vi_ban_giao_id` | `uuid` | Y | — | ID đơn vị bàn giao `FK` |
| 4 | `TenDonViBanGiao` | `ten_don_vi_ban_giao` | `text` | Y | — | Snapshot tên đơn vị bàn giao |
| 5 | `DonViNhanId` | `don_vi_nhan_id` | `uuid` | N | — | ID đơn vị nhận `FK` |
| 6 | `TenDonViNhan` | `ten_don_vi_nhan` | `text` | N | — | Snapshot tên đơn vị nhận |
| 7 | `TaiKhoanChiPhiMoiId` | `tai_khoan_chi_phi_moi_id` | `uuid` | Y | — | ID tài khoản chi phí mới `FK` |
| 8 | `TenTaiKhoanChiPhiMoi` | `ten_tai_khoan_chi_phi_moi` | `text` | Y | — | Snapshot tên tài khoản chi phí mới |
| 9 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú chi tiết |

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

**Đối chiếu `fa_chi_tiet_dieu_chuyen` (14 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `dieu_chuyen_tai_san_id`, `ten_don_vi_ban_giao`, `ten_don_vi_nhan`, `tai_khoan_chi_phi_moi_id`, `ten_tai_khoan_chi_phi_moi`, `ghi_chu` |
| DB có — LDM **không khai** | 2 | `dieu_chuyen_id`, `phien_ban` |

---

## 25. `fa_tai_san_co_dinh_lich_su_dieu_chuyen`

| Mục | Nội dung |
|---|---|
| Entity LDM | `LichSuDieuChuyenTaiSan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_tai_san_co_dinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_tai_san_co_dinh` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | Y | — | ID TSCĐ `FK` |
| 2 | `KhoangThoiGianSuDung` | `khoang_thoi_gian_su_dung` | `text` | N | — | Khoảng thời gian đơn vị sử dụng TSCĐ |
| 3 | `DonViBanGiaoId` | `don_vi_ban_giao_id` | `uuid` | N | — | ID đơn vị bàn giao `FK` |
| 4 | `TenDonViBanGiao` | `ten_don_vi_ban_giao` | `text` | N | — | Snapshot tên đơn vị bàn giao |
| 5 | `DonViNhanId` | `don_vi_nhan_id` | `uuid` | N | — | ID đơn vị nhận `FK` |
| 6 | `TenDonViNhan` | `ten_don_vi_nhan` | `text` | N | — | Snapshot tên đơn vị nhận |

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

## 26. `fa_khau_hao_tai_san`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KhauHaoTaiSan` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_khau_hao_tai_san` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | 8. Khấu hao TSCĐ |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `fa_khau_hao_tai_san_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `Thang` | `thang` | `integer` | N | `0` | Tháng tính khấu hao |
| 2 | `Nam` | `nam` | `integer` | N | `0` | Năm tính khấu hao |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải chung |

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

**Đối chiếu `fa_khau_hao_tai_san` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 1 | `trang_thai` |

---

## 27. `fa_khau_hao_tai_san_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietKhauHaoTaiSan` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `fa_chi_tiet_khau_hao_tai_san` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `fa_khau_hao_tai_san` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `fa_khau_hao_tai_san` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhauHaoTaiSanId` | `khau_hao_tai_san_id` | `uuid` | N | — | ID phiếu khấu hao `FK` |
| 2 | `TaiSanCoDinhId` | `tai_san_co_dinh_id` | `uuid` | N | — | ID TSCĐ `FK` |
| 3 | `SoTienKhauHao` | `so_tien_khau_hao` | `money_foreign` ≈ | N | `0` | Số tiền khấu hao chốt |
| 4 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID công trình/vụ việc `FK` |
| 5 | `TenCongTrinh` | `ten_cong_trinh` | `text` | Y | — | Snapshot tên công trình/vụ việc |
| 6 | `DonViId` | `don_vi_id` | `uuid` | Y | — | ID đơn vị `FK` |
| 7 | `TenDonVi` | `ten_don_vi` | `text` | Y | — | Snapshot tên đơn vị |
| 8 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | ID đối tượng tập hợp chi phí `FK` |
| 9 | `TenDoiTuongTapHopChiPhi` | `ten_doi_tuong_tap_hop_chi_phi` | `text` | Y | — | Snapshot tên đối tượng tập hợp chi phí |
| 10 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | ID hợp đồng `FK` |
| 11 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí `FK` |
| 12 | `TenKhoanMucChiPhi` | `ten_khoan_muc_chi_phi` | `text` | Y | — | Snapshot tên khoản mục chi phí |
| 13 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | Y | — | ID lệnh sản xuất, tham chiếu LenhSanXuat trong ldm-Kho.puml `FK` |

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

**Đối chiếu `fa_chi_tiet_khau_hao_tai_san` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 10 | `khau_hao_tai_san_id`, `vu_viec_id`, `ten_cong_trinh`, `don_vi_id`, `ten_don_vi`, `doi_tuong_tap_hop_chi_phi_id`, `ten_doi_tuong_tap_hop_chi_phi`, `hop_dong_id`, `ten_khoan_muc_chi_phi`, `lenh_san_xuat_id` |
| DB có — LDM **không khai** | 4 | `khau_hao_id`, `tai_khoan_no_id`, `tai_khoan_co_id`, `phien_ban` |

