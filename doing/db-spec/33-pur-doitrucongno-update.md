# `pur_` — Đối trừ công nợ

> Sinh tự động từ [`ldm-DoiTruCongNo-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-DoiTruCongNo-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**2 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ChungTuDoiTru` | `pur_chung_tu_doi_tru` | `pur_chung_tu_doi_tru` | B — có schema, chưa code | Đầu chứng từ — CHỨNG TỪ ĐỐI TRỪ CÔNG NỢ (phải thu PMKT-E-14621 + phải trả PMKT-E-14622) |
| 2 | `ChiTietChungTuDoiTru` | `pur_chung_tu_doi_tru_chi_tiet` | `pur_chi_tiet_chung_tu_doi_tru` | B — có schema, chưa code | Dòng chi tiết của `pur_chung_tu_doi_tru` — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `pur_chung_tu_doi_tru`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuDoiTru` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chung_tu_doi_tru` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | KHỐI 1 — CHỨNG TỪ ĐỐI TRỪ CÔNG NỢ (phải thu PMKT-E-14621 + phải trả PMKT-E-14622) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `pur_chung_tu_doi_tru_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhachHangId` | `khach_hang_id` | `uuid` | Y | — | **[Đối tượng công nợ (mỗi phiếu chỉ dùng một trong hai khóa theo loại đối trừ)]** ID khách hàng (reference đến ENT_DoiTuong vai trò Khách hàng; dùng cho đối trừ công nợ phải thu, NULL với phiếu phải trả) `FK` |
| 2 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | Y | — | **[Đối tượng công nợ (mỗi phiếu chỉ dùng một trong hai khóa theo loại đối trừ)]** ID nhà cung cấp (reference đến ENT_DoiTuong vai trò Nhà cung cấp; dùng cho đối trừ công nợ phải trả, NULL với phiếu phải thu) `FK` |
| 3 | `TaiKhoanCongNoId` | `tai_khoan_cong_no_id` | `uuid` | N | — | **[Đối tượng công nợ (mỗi phiếu chỉ dùng một trong hai khóa theo loại đối trừ)]** Tài khoản công nợ đối trừ (reference đến ENT_HeThongTaiKhoan; theo loại đối trừ phải thu / phải trả) `FK` |
| 4 | `NgayDoiTru` | `ngay_doi_tru` | `date` | N | — | **[Thông tin chứng từ]** Ngày thực hiện đối trừ |
| 5 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin chứng từ]** Diễn giải nội dung đối trừ |
| 6 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ và chênh lệch tỷ giá]** Loại tiền đối trừ (reference đến ENT_LoaiTien) `FK` |
| 7 | `TaiKhoanLaiTyGiaId` | `tai_khoan_lai_ty_gia_id` | `uuid` | Y | — | **[Tiền tệ và chênh lệch tỷ giá]** TK xử lý chênh lệch lãi tỷ giá (reference đến ENT_HeThongTaiKhoan) `FK` |
| 8 | `TaiKhoanLoTyGiaId` | `tai_khoan_lo_ty_gia_id` | `uuid` | Y | — | **[Tiền tệ và chênh lệch tỷ giá]** TK xử lý chênh lệch lỗ tỷ giá (reference đến ENT_HeThongTaiKhoan) `FK` |
| 9 | `PhieuKeToanChenhLechId` | `phieu_ke_toan_chenh_lech_id` | `uuid` | Y | — | **[Tiền tệ và chênh lệch tỷ giá]** Phiếu kế toán tổng hợp xử lý chênh lệch tỷ giá sinh kèm (reference đến ENT_PhieuKeToanTongHop; NULL khi không phát sinh chênh lệch) `FK` |
| 10 | `TongTienDoiTru` | `tong_tien_doi_tru` | `money_foreign` ≈ | N | `0` | **[Tổng hợp]** Tổng số tiền đã đối trừ của phiếu (hệ thống tính) |

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

**Đối chiếu `pur_chung_tu_doi_tru` (29 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `dien_giai` |
| DB có — LDM **không khai** | 8 | `loai_doi_tru`, `ten_doi_tuong`, `ten_tai_khoan_cong_no`, `ma_loai_tien`, `ty_gia`, `mo_ta`, `tong_tien_co`, `ma_nha_cung_cap` |

---

## 2. `pur_chung_tu_doi_tru_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietChungTuDoiTru` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chi_tiet_chung_tu_doi_tru` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_chung_tu_doi_tru` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_chung_tu_doi_tru` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuDoiTruId` | `chung_tu_doi_tru_id` | `uuid` | N | — | ID chứng từ đối trừ cha (reference đến ENT_ChungTuDoiTru) `FK` |
| 2 | `ChungTuThanhToanId` | `chung_tu_thanh_toan_id` | `uuid` | Y | — | **[Chứng từ tham chiếu (mỗi dòng chỉ dùng một trong hai khóa)]** Chứng từ thanh toán nguồn tiền (phải thu: ENT_PhieuThu / ENT_PhieuKeToanTongHop; phải trả: ENT_PhieuChi / ENT_PhieuKeToanTongHop; NULL với dòng công nợ) `FK` |
| 3 | `ChungTuCongNoId` | `chung_tu_cong_no_id` | `uuid` | Y | — | **[Chứng từ tham chiếu (mỗi dòng chỉ dùng một trong hai khóa)]** Chứng từ công nợ đích phân bổ (phải thu: ENT_ChungTuBan / ENT_PhieuKeToanTongHop; phải trả: ENT_ChungTuMuaHang (đã gộp mua dịch vụ) / ENT_HoaDonMua / ENT_PhieuKeToanTongHop; NULL với dòng nguồn tiền) `FK` |
| 4 | `LoaiChungTu` | `loai_chung_tu` | `text` CHECK | N | — | **[Chứng từ tham chiếu (mỗi dòng chỉ dùng một trong hai khóa)]** Entity gốc của chứng từ tham chiếu (PhieuThu \| PhieuChi \| ChungTuBan \| ChungTuMuaHang \| HoaDonMua \| PhieuKeToanTongHop) — nguồn hiển thị cột Loại chứng từ |
| 5 | `SoTienDoiTru` | `so_tien_doi_tru` | `money_foreign` ≈ | N | `0` | **[Số tiền]** Số tiền đối trừ của dòng |
| 6 | `SoTienDoiTruQuyDoi` | `so_tien_doi_tru_quy_doi` | `money_vnd` | N | `0` | **[Số tiền]** Số tiền đối trừ quy đổi |

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

**Đối chiếu `pur_chi_tiet_chung_tu_doi_tru` (27 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 0 | *(không)* |
| DB có — LDM **không khai** | 11 | `vai_tro`, `so_chung_tu`, `ngay`, `dien_giai`, `so_tien`, `so_hoa_don`, `ngay_hoa_don`, `han_thanh_toan`, `con_no`, `phien_ban`, `ngay_chung_tu` |

