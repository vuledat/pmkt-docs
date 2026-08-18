# `cb_` — Ngân quỹ (tiền mặt · tiền gửi)

> Sinh tự động từ [`ldm-NganQuy-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-NganQuy-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**7 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `PhieuThu` | `cb_phieu_thu` | `cb_phieu_thu` | B — có schema, chưa code | Đầu chứng từ — PHIẾU THU (tiền mặt + tiền gửi/giấy báo có) |
| 2 | `ChiTietPhieuThu` | `cb_phieu_thu_chi_tiet` | `cb_chi_tiet_phieu_thu` | B — có schema, chưa code | Dòng chi tiết của `cb_phieu_thu` — ⚠ *LDM chưa mô tả bảng này* |
| 3 | `PhieuChi` | `cb_phieu_chi` | `cb_phieu_chi` | B — có schema, chưa code | Đầu chứng từ — PHIẾU CHI (tiền mặt + chi tiền gửi: ủy nhiệm chi/séc chuyển khoản/séc tiền mặt) |
| 4 | `ChiTietPhieuChi` | `cb_phieu_chi_chi_tiet` | `cb_chi_tiet_phieu_chi` | B — có schema, chưa code | Dòng chi tiết của `cb_phieu_chi` — ⚠ *LDM chưa mô tả bảng này* |
| 5 | `ChiTietBangKeHoaDon` | `cb_phieu_chi_bang_ke_hoa_don` | `cb_chi_tiet_bang_ke_hoa_don` | B — có schema, chưa code | Dòng chi tiết của `cb_phieu_chi` — ⚠ *LDM chưa mô tả bảng này* |
| 6 | `ChuyenTienNoiBo` | `cb_chuyen_tien_noi_bo` | — | C — tạo mới | Đầu chứng từ — CHUYỂN TIỀN NỘI BỘ (một chứng từ, hiển thị ở cả danh sách thu và chi) |
| 7 | `ChiTietChuyenTienNoiBo` | `cb_chuyen_tien_noi_bo_chi_tiet` | — | C — tạo mới | Dòng chi tiết của `cb_chuyen_tien_noi_bo` — ⚠ *LDM chưa mô tả bảng này* |

---

## 1. `cb_phieu_thu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuThu` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cb_phieu_thu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | KHỐI 1 — PHIẾU THU (tiền mặt + tiền gửi/giấy báo có) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `cb_phieu_thu_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuongThucThanhToan` | `phuong_thuc_thanh_toan` | `text` CHECK | N | — | **[Tùy chọn nghiệp vụ]** Phương thức thanh toán (Tiền mặt — phiếu thu tiền mặt; Chuyển khoản — thu tiền gửi/giấy báo có) |
| 2 | `IsThuNhieuDoiTuong` | `is_thu_nhieu_doi_tuong` | `boolean` | Y | `false` | **[Tùy chọn nghiệp vụ]** Thu từ nhiều đối tượng (đối tượng nhập theo dòng hạch toán) |
| 3 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng nộp tiền]** ID đối tượng nộp tiền (reference đến ENT_DoiTuong) `FK` |
| 4 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng nộp tiền]** Tên đối tượng |
| 5 | `NguoiNopTien` | `nguoi_nop_tien` | `text` | Y | — | **[Đối tượng nộp tiền]** Người nộp tiền |
| 6 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Đối tượng nộp tiền]** Địa chỉ |
| 7 | `NhanVienThuNoId` | `nhan_vien_thu_no_id` | `uuid` | Y | — | **[Đối tượng nộp tiền]** Nhân viên thu nợ (reference đến ENT_DoiTuong vai trò Nhân viên) `FK` |
| 8 | `TaiKhoanNhanId` | `tai_khoan_nhan_id` | `uuid` | Y | — | **[Tài khoản ngân hàng nhận (thu tiền gửi)]** Tài khoản ngân hàng nhận tiền (reference đến ENT_TaiKhoanNganHang) `FK` |
| 9 | `TenNganHangNhan` | `ten_ngan_hang_nhan` | `text` | Y | — | **[Tài khoản ngân hàng nhận (thu tiền gửi)]** Tên ngân hàng nhận |
| 10 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | **[Thông tin chứng từ]** Mục đích thu (reference ENT_TaiKhoanNgamDinh) `FK` |
| 11 | `LyDoThu` | `ly_do_thu` | `text` | Y | — | **[Thông tin chứng từ]** Lý do thu |
| 12 | `KemTheo` | `kem_theo` | `numeric(18,4)` ⚠ | Y | `0` | **[Thông tin chứng từ]** Số lượng chứng từ gốc kèm theo |
| 13 | `ChungTuGoc` | `chung_tu_goc` | `text` | Y | — | **[Thông tin chứng từ]** Chứng từ gốc |
| 14 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ]** Loại tiền (reference đến ENT_LoaiTien) `FK` |
| 15 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Tiền tệ]** Tỷ giá quy đổi |
| 16 | `TongSoTienThu` | `tong_so_tien_thu` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng thu tiền theo hóa đơn)]** Tổng số tiền thu |
| 17 | `TongSoTienThuQuyDoi` | `tong_so_tien_thu_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng thu tiền theo hóa đơn)]** Tổng số tiền thu quy đổi |
| 18 | `TongSoTienChietKhau` | `tong_so_tien_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng thu tiền theo hóa đơn)]** Tổng tiền chiết khấu thanh toán (luồng thu tiền theo hóa đơn) |
| 19 | `TongSoTienChietKhauQuyDoi` | `tong_so_tien_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng thu tiền theo hóa đơn)]** Tổng tiền chiết khấu quy đổi |
| 20 | `SoTienDaDoiTru` | `so_tien_da_doi_tru` | `money_foreign` ≈ | N | `0` | **[Số liệu đối trừ (hệ thống cộng dồn)]** Số tiền đã đối trừ công nợ (hệ thống cộng dồn) |
| 21 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Trạng thái]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `cb_phieu_thu` (12 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 19 | `phuong_thuc_thanh_toan`, `is_thu_nhieu_doi_tuong`, `doi_tuong_id`, `ten_doi_tuong`, `nguoi_nop_tien`, `dia_chi`, `nhan_vien_thu_no_id`, `tai_khoan_nhan_id`, `ten_ngan_hang_nhan`, `tai_khoan_ngam_dinh_id`, `ly_do_thu`, `chung_tu_goc`, `loai_tien_id`, `ty_gia`, `tong_so_tien_thu`, `tong_so_tien_thu_quy_doi`, `tong_so_tien_chiet_khau`, `tong_so_tien_chiet_khau_quy_doi`, `so_tien_da_doi_tru` |
| DB có — LDM **không khai** | 3 | `ma`, `ten`, `hinh_thuc_tien` |

---

## 2. `cb_phieu_thu_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuThu` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cb_chi_tiet_phieu_thu` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cb_phieu_thu` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cb_phieu_thu` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuThuId` | `phieu_thu_id` | `uuid` | N | — | ID phiếu thu cha (reference đến ENT_PhieuThu) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hạch toán]** Diễn giải dòng |
| 3 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Hạch toán]** TK Nợ (reference đến ENT_HeThongTaiKhoan) `FK` |
| 4 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Hạch toán]** TK Có (reference đến ENT_HeThongTaiKhoan) `FK` |
| 5 | `SoTienThu` | `so_tien_thu` | `money_foreign` ≈ | N | `0` | **[Hạch toán]** Số tiền |
| 6 | `SoTienThuQuyDoi` | `so_tien_thu_quy_doi` | `money_vnd` | N | `0` | **[Hạch toán]** Số tiền quy đổi |
| 7 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng theo dòng (khi Thu từ nhiều đối tượng)]** ID đối tượng của dòng (reference đến ENT_DoiTuong) `FK` |
| 8 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng theo dòng (khi Thu từ nhiều đối tượng)]** Tên đối tượng |
| 9 | `ChungTuBanId` | `chung_tu_ban_id` | `uuid` | Y | — | **[Liên kết chứng từ công nợ (phiếu sinh kèm thu tiền ngay và thu tiền theo hóa đơn)]** ID chứng từ bán được thu tiền của dòng (reference đến ENT_ChungTuBan; NULL khi thu không theo chứng từ) `FK` |
| 10 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đơn vị (reference đến ENT_DonVi) `FK` |
| 11 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Vụ việc/công trình (reference đến ENT_CongTrinh) `FK` |
| 12 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 13 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 14 | `IsChiPhiKhongHopLy` | `is_chi_phi_khong_hop_ly` | `boolean` | Y | `false` | **[Cột thống kê (thông tin tự do)]** Chi phí không hợp lý |

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

**Đối chiếu `cb_chi_tiet_phieu_thu` (30 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `dien_giai`, `chung_tu_ban_id`, `is_chi_phi_khong_hop_ly` |
| DB có — LDM **không khai** | 10 | `chung_tu_ban_hang_id`, `chung_tu_ban_dich_vu_id`, `mo_ta`, `la_chi_phi_khong_hop_ly`, `tien_chiet_khau`, `tien_ck_quy_doi`, `tien_chenh_lech`, `tien_chenh_lech_quy_doi`, `tk_chiet_khau_id`, `phien_ban` |

---

## 3. `cb_phieu_chi`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuChi` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cb_phieu_chi` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | KHỐI 2 — PHIẾU CHI (tiền mặt + chi tiền gửi: ủy nhiệm chi/séc chuyển khoản/séc tiền mặt) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `cb_phieu_chi_chi_tiet` · `cb_phieu_chi_bang_ke_hoa_don` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhuongThucThanhToan` | `phuong_thuc_thanh_toan` | `text` CHECK | N | — | **[Tùy chọn nghiệp vụ]** Phương thức thanh toán (Tiền mặt — phiếu chi tiền mặt; Ủy nhiệm chi, Séc chuyển khoản, Séc tiền mặt — chi tiền gửi) |
| 2 | `IsChiNhieuDoiTuong` | `is_chi_nhieu_doi_tuong` | `boolean` | Y | `false` | **[Tùy chọn nghiệp vụ]** Chi cho nhiều đối tượng (đối tượng nhập theo dòng hạch toán) |
| 3 | `IsHachToanGopNhieuHoaDon` | `is_hach_toan_gop_nhieu_hoa_don` | `boolean` | Y | `false` | **[Tùy chọn nghiệp vụ]** Hạch toán gộp nhiều hóa đơn (dùng với chi mua ngoài có hóa đơn) |
| 4 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng nhận tiền]** ID đối tượng nhận tiền (reference đến ENT_DoiTuong) `FK` |
| 5 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng nhận tiền]** Tên đối tượng |
| 6 | `NguoiNhanTien` | `nguoi_nhan_tien` | `text` | Y | — | **[Đối tượng nhận tiền]** Người nhận/lĩnh tiền |
| 7 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Đối tượng nhận tiền]** Địa chỉ |
| 8 | `NhanVienTraNoId` | `nhan_vien_tra_no_id` | `uuid` | Y | — | **[Đối tượng nhận tiền]** Nhân viên trả nợ (reference đến ENT_DoiTuong vai trò Nhân viên) `FK` |
| 9 | `SoCCCD` | `so_cccd` | `text` | Y | — | **[Giấy tờ người lĩnh tiền (séc tiền mặt)]** Số CCCD người lĩnh tiền |
| 10 | `NgayCap` | `ngay_cap` | `date` | Y | — | **[Giấy tờ người lĩnh tiền (séc tiền mặt)]** Ngày cấp |
| 11 | `NoiCap` | `noi_cap` | `text` | Y | — | **[Giấy tờ người lĩnh tiền (séc tiền mặt)]** Nơi cấp |
| 12 | `TaiKhoanChiId` | `tai_khoan_chi_id` | `uuid` | Y | — | **[Tài khoản ngân hàng (chi tiền gửi)]** Tài khoản ngân hàng chi tiền (reference đến ENT_TaiKhoanNganHang) `FK` |
| 13 | `TenNganHangChi` | `ten_ngan_hang_chi` | `text` | Y | — | **[Tài khoản ngân hàng (chi tiền gửi)]** Tên ngân hàng chi |
| 14 | `TaiKhoanNhanId` | `tai_khoan_nhan_id` | `uuid` | Y | — | **[Tài khoản ngân hàng (chi tiền gửi)]** Tài khoản nhận của đối tượng (reference đến ENT_TaiKhoanNganHang) `FK` |
| 15 | `TenNganHangNhan` | `ten_ngan_hang_nhan` | `text` | Y | — | **[Tài khoản ngân hàng (chi tiền gửi)]** Tên ngân hàng nhận |
| 16 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | **[Thông tin chứng từ]** Mục đích chi (reference ENT_TaiKhoanNgamDinh) `FK` |
| 17 | `LyDoChi` | `ly_do_chi` | `text` | Y | — | **[Thông tin chứng từ]** Lý do chi/nội dung thanh toán |
| 18 | `KemTheo` | `kem_theo` | `numeric(18,4)` ⚠ | Y | `0` | **[Thông tin chứng từ]** Số lượng chứng từ gốc kèm theo |
| 19 | `ChungTuGoc` | `chung_tu_goc` | `text` | Y | — | **[Thông tin chứng từ]** Chứng từ gốc |
| 20 | `Nam` | `nam` | `integer` | Y | `0` | **[Thông tin chứng từ]** Năm nộp thuế TNDN tạm tính |
| 21 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ]** Loại tiền (reference đến ENT_LoaiTien) `FK` |
| 22 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Tiền tệ]** Tỷ giá quy đổi |
| 23 | `TongSoTienChi` | `tong_so_tien_chi` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng trả tiền theo hóa đơn)]** Tổng số tiền chi |
| 24 | `TongSoTienChiQuyDoi` | `tong_so_tien_chi_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng trả tiền theo hóa đơn)]** Tổng số tiền chi quy đổi |
| 25 | `TongTienThueGTGT` | `tong_tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng trả tiền theo hóa đơn)]** Tổng tiền thuế GTGT (khi có bảng kê hóa đơn) |
| 26 | `TongTienThueGTGTQuyDoi` | `tong_tien_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng trả tiền theo hóa đơn)]** Tổng tiền thuế GTGT quy đổi |
| 27 | `TongSoTienChietKhau` | `tong_so_tien_chiet_khau` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng trả tiền theo hóa đơn)]** Tổng tiền chiết khấu thanh toán (luồng trả tiền theo hóa đơn) |
| 28 | `TongSoTienChietKhauQuyDoi` | `tong_so_tien_chiet_khau_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính; chiết khấu tổng hợp từ dòng hạch toán chiết khấu của luồng trả tiền theo hóa đơn)]** Tổng tiền chiết khấu quy đổi |
| 29 | `SoTienDaDoiTru` | `so_tien_da_doi_tru` | `money_foreign` ≈ | N | `0` | **[Số liệu đối trừ (hệ thống cộng dồn)]** Số tiền đã đối trừ công nợ (hệ thống cộng dồn) |
| 30 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Trạng thái]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `cb_phieu_chi` (39 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 9 | `is_chi_nhieu_doi_tuong`, `is_hach_toan_gop_nhieu_hoa_don`, `nhan_vien_tra_no_id`, `tai_khoan_ngam_dinh_id`, `kem_theo`, `tong_tien_thue_gtgt`, `tong_tien_thue_gtgt_quy_doi`, `tong_so_tien_chiet_khau_quy_doi`, `so_tien_da_doi_tru` |
| DB có — LDM **không khai** | 5 | `so_tai_khoan_nhan`, `hinh_thuc_tien`, `nhan_vien_id`, `muc_dich_thu_chi_id`, `la_chi_nhieu_doi_tuong` |

---

## 4. `cb_phieu_chi_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuChi` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cb_chi_tiet_phieu_chi` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cb_phieu_chi` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cb_phieu_chi` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuChiId` | `phieu_chi_id` | `uuid` | N | — | ID phiếu chi cha (reference đến ENT_PhieuChi) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hạch toán]** Diễn giải dòng |
| 3 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Hạch toán]** TK Nợ (reference đến ENT_HeThongTaiKhoan) `FK` |
| 4 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Hạch toán]** TK Có (reference đến ENT_HeThongTaiKhoan) `FK` |
| 5 | `SoTienChi` | `so_tien_chi` | `money_foreign` ≈ | N | `0` | **[Hạch toán]** Số tiền |
| 6 | `SoTienChiQuyDoi` | `so_tien_chi_quy_doi` | `money_vnd` | N | `0` | **[Hạch toán]** Số tiền quy đổi |
| 7 | `TyGiaXuatQuy` | `ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** Tỷ giá xuất quỹ (hệ thống tính) |
| 8 | `QuyDoiTheoTyGiaXuatQuy` | `quy_doi_theo_ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** Quy đổi theo tỷ giá xuất quỹ (hệ thống tính) |
| 9 | `ChenhLechTyGiaXuatQuy` | `chenh_lech_ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** Chênh lệch tỷ giá xuất quỹ (dương lỗ, âm lãi; hệ thống tính) |
| 10 | `TaiKhoanXuLyChenhLechId` | `tai_khoan_xu_ly_chenh_lech_id` | `uuid` | Y | — | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** TK xử lý chênh lệch tỷ giá (reference đến ENT_HeThongTaiKhoan) `FK` |
| 11 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng theo dòng (khi Chi cho nhiều đối tượng)]** ID đối tượng của dòng (reference đến ENT_DoiTuong) `FK` |
| 12 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng theo dòng (khi Chi cho nhiều đối tượng)]** Tên đối tượng |
| 13 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | Y | — | **[Liên kết chứng từ công nợ (phiếu sinh kèm thanh toán ngay và trả tiền theo hóa đơn; mỗi dòng chỉ dùng một trong ba khóa)]** ID chứng từ mua hàng/mua dịch vụ được trả tiền của dòng (reference đến ENT_ChungTuMuaHang — LDM Mua hàng đã gộp mua dịch vụ; NULL khi chi không theo chứng từ) `FK` |
| 14 | `HoaDonMuaId` | `hoa_don_mua_id` | `uuid` | Y | — | **[Liên kết chứng từ công nợ (phiếu sinh kèm thanh toán ngay và trả tiền theo hóa đơn; mỗi dòng chỉ dùng một trong ba khóa)]** ID hóa đơn mua được trả tiền của dòng (reference đến ENT_HoaDonMua; NULL khi chi không theo chứng từ) `FK` |
| 15 | `TaiKhoanNganHangId` | `tai_khoan_ngan_hang_id` | `uuid` | Y | — | **[Gửi tiền vào ngân hàng (phiếu chi tiền mặt)]** Tài khoản ngân hàng nhận tiền gửi (reference đến ENT_TaiKhoanNganHang) `FK` |
| 16 | `TenNganHang` | `ten_ngan_hang` | `text` | Y | — | **[Gửi tiền vào ngân hàng (phiếu chi tiền mặt)]** Tên ngân hàng |
| 17 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đơn vị (reference đến ENT_DonVi) `FK` |
| 18 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Vụ việc/công trình (reference đến ENT_CongTrinh) `FK` |
| 19 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 20 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 21 | `IsChiPhiKhongHopLy` | `is_chi_phi_khong_hop_ly` | `boolean` | Y | `false` | **[Cột thống kê (thông tin tự do)]** Chi phí không hợp lý |

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

**Đối chiếu `cb_chi_tiet_phieu_chi` (30 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 9 | `dien_giai`, `ty_gia_xuat_quy`, `quy_doi_theo_ty_gia_xuat_quy`, `chenh_lech_ty_gia_xuat_quy`, `tai_khoan_xu_ly_chenh_lech_id`, `hoa_don_mua_id`, `tai_khoan_ngan_hang_id`, `ten_ngan_hang`, `is_chi_phi_khong_hop_ly` |
| DB có — LDM **không khai** | 9 | `chung_tu_mua_dich_vu_id`, `mo_ta`, `la_chi_phi_khong_hop_ly`, `tien_chiet_khau`, `tien_ck_quy_doi`, `tien_chenh_lech`, `tien_chenh_lech_quy_doi`, `tk_chiet_khau_id`, `phien_ban` |

---

## 5. `cb_phieu_chi_bang_ke_hoa_don`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietBangKeHoaDon` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `cb_chi_tiet_bang_ke_hoa_don` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cb_phieu_chi` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cb_phieu_chi` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuChiId` | `phieu_chi_id` | `uuid` | N | — | ID phiếu chi cha (reference đến ENT_PhieuChi) `FK` |
| 2 | `ChiTietHachToanId` | `chi_tiet_hach_toan_id` | `uuid` | Y | — | **[Liên kết dòng hạch toán]** ID dòng hạch toán tương ứng (reference đến ENT_ChiTietPhieuChi; 1-1 khi không gộp, NULL khi Hạch toán gộp nhiều hóa đơn) `FK` |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hóa đơn đầu vào]** Diễn giải |
| 4 | `CoHoaDon` | `co_hoa_don` | `boolean` | Y | `false` | **[Hóa đơn đầu vào]** Dòng có hóa đơn (luôn true khi hạch toán gộp) |
| 5 | `MauSoHoaDonId` | `mau_so_hoa_don_id` | `uuid` | Y | — | **[Hóa đơn đầu vào]** Mẫu số hóa đơn (reference đến ENT_MauSoHoaDon) `FK` |
| 6 | `KyHieu` | `ky_hieu` | `text` | Y | — | **[Hóa đơn đầu vào]** Ký hiệu hóa đơn |
| 7 | `SoHoaDon` | `so_hoa_don` | `varchar(50)` | Y | — | **[Hóa đơn đầu vào]** Số hóa đơn |
| 8 | `NgayHoaDon` | `ngay_hoa_don` | `date` | Y | — | **[Hóa đơn đầu vào]** Ngày hóa đơn |
| 9 | `GiaTriChuaThue` | `gia_tri_chua_thue` | `money_foreign` ≈ | N | `0` | **[Thuế GTGT đầu vào]** Giá trị hàng hóa dịch vụ chưa thuế (nhập khi hạch toán gộp; không gộp thì lấy theo dòng hạch toán) |
| 10 | `GiaTriChuaThueQuyDoi` | `gia_tri_chua_thue_quy_doi` | `money_vnd` | N | `0` | **[Thuế GTGT đầu vào]** Giá trị chưa thuế quy đổi |
| 11 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | **[Thuế GTGT đầu vào]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 12 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | N | `0` | **[Thuế GTGT đầu vào]** Tiền thuế GTGT |
| 13 | `TienThueGTGTQuyDoi` | `tien_thue_gtgt_quy_doi` | `money_vnd` | N | `0` | **[Thuế GTGT đầu vào]** Tiền thuế GTGT quy đổi |
| 14 | `TaiKhoanThueId` | `tai_khoan_thue_id` | `uuid` | Y | — | **[Thuế GTGT đầu vào]** TK thuế (reference đến ENT_HeThongTaiKhoan) `FK` |
| 15 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | **[Thuế GTGT đầu vào]** Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5) |
| 16 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | Y | — | **[Nhà cung cấp (khi Chi cho nhiều đối tượng)]** ID nhà cung cấp (reference đến ENT_DoiTuong vai trò Nhà cung cấp) `FK` |
| 17 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Nhà cung cấp (khi Chi cho nhiều đối tượng)]** Tên nhà cung cấp |
| 18 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | **[Nhà cung cấp (khi Chi cho nhiều đối tượng)]** Mã số thuế |
| 19 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Nhà cung cấp (khi Chi cho nhiều đối tượng)]** Địa chỉ |

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

**Đối chiếu `cb_chi_tiet_bang_ke_hoa_don` (26 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `chi_tiet_hach_toan_id`, `dien_giai`, `co_hoa_don`, `mau_so_hoa_don_id`, `gia_tri_chua_thue`, `gia_tri_chua_thue_quy_doi` |
| DB có — LDM **không khai** | 4 | `chi_tiet_phieu_chi_id`, `mo_ta`, `mau_so`, `phien_ban` |

---

## 6. `cb_chuyen_tien_noi_bo`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChuyenTienNoiBo` |
| Base class | `BaseChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | KHỐI 3 — CHUYỂN TIỀN NỘI BỘ (một chứng từ, hiển thị ở cả danh sách thu và chi) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `cb_chuyen_tien_noi_bo_chi_tiet` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin chứng từ]** Lý do chuyển |
| 2 | `NhanVienId` | `nhan_vien_id` | `uuid` | Y | — | **[Thông tin chứng từ]** Nhân viên (reference đến ENT_DoiTuong vai trò Nhân viên) `FK` |
| 3 | `TaiKhoanChiId` | `tai_khoan_chi_id` | `uuid` | N | — | **[Tài khoản ngân hàng chuyển - nhận]** Tài khoản ngân hàng chi (reference đến ENT_TaiKhoanNganHang; khác Tài khoản nhận) `FK` |
| 4 | `TenNganHangChi` | `ten_ngan_hang_chi` | `text` | N | — | **[Tài khoản ngân hàng chuyển - nhận]** Tên ngân hàng chi |
| 5 | `TaiKhoanNhanId` | `tai_khoan_nhan_id` | `uuid` | N | — | **[Tài khoản ngân hàng chuyển - nhận]** Tài khoản ngân hàng nhận (reference đến ENT_TaiKhoanNganHang) `FK` |
| 6 | `TenNganHangNhan` | `ten_ngan_hang_nhan` | `text` | N | — | **[Tài khoản ngân hàng chuyển - nhận]** Tên ngân hàng nhận |
| 7 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | **[Tiền tệ]** Loại tiền (reference đến ENT_LoaiTien) `FK` |
| 8 | `TyGia` | `ty_gia` | `exchange_rate` | Y | `1` | **[Tiền tệ]** Tỷ giá quy đổi |
| 9 | `TongSoTien` | `tong_so_tien` | `money_foreign` ≈ | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng số tiền |
| 10 | `TongSoTienQuyDoi` | `tong_so_tien_quy_doi` | `money_vnd` | N | `0` | **[Tổng tiền (hệ thống tính từ chi tiết)]** Tổng số tiền quy đổi |
| 11 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Trạng thái]** Trạng thái chứng từ (ChuaGhiSo \| DaGhiSo) |

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

---

## 7. `cb_chuyen_tien_noi_bo_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietChuyenTienNoiBo` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `cb_chuyen_tien_noi_bo` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `cb_chuyen_tien_noi_bo` — FK `ON DELETE CASCADE` |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChuyenTienNoiBoId` | `chuyen_tien_noi_bo_id` | `uuid` | N | — | ID chứng từ cha (reference đến ENT_ChuyenTienNoiBo) `FK` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hạch toán]** Diễn giải dòng |
| 3 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Hạch toán]** TK Nợ (reference đến ENT_HeThongTaiKhoan) `FK` |
| 4 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Hạch toán]** TK Có (reference đến ENT_HeThongTaiKhoan) `FK` |
| 5 | `SoTien` | `so_tien` | `money_foreign` ≈ | N | `0` | **[Hạch toán]** Số tiền |
| 6 | `SoTienQuyDoi` | `so_tien_quy_doi` | `money_vnd` | N | `0` | **[Hạch toán]** Số tiền quy đổi |
| 7 | `TyGiaXuatQuy` | `ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** Tỷ giá xuất quỹ (hệ thống tính) |
| 8 | `QuyDoiTheoTyGiaXuatQuy` | `quy_doi_theo_ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** Quy đổi theo tỷ giá xuất quỹ (hệ thống tính) |
| 9 | `ChenhLechTyGiaXuatQuy` | `chenh_lech_ty_gia_xuat_quy` | `exchange_rate` | Y | `1` | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** Chênh lệch tỷ giá xuất quỹ (dương lỗ, âm lãi; hệ thống tính) |
| 10 | `TaiKhoanXuLyChenhLechId` | `tai_khoan_xu_ly_chenh_lech_id` | `uuid` | Y | — | **[Tỷ giá xuất quỹ (dòng chi ngoại tệ)]** TK xử lý chênh lệch tỷ giá (reference đến ENT_HeThongTaiKhoan) `FK` |
| 11 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đơn vị (reference đến ENT_DonVi) `FK` |
| 12 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Vụ việc/công trình (reference đến ENT_CongTrinh) `FK` |
| 13 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 14 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Cột thống kê (thông tin tự do)]** Đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 15 | `IsChiPhiKhongHopLy` | `is_chi_phi_khong_hop_ly` | `boolean` | Y | `false` | **[Cột thống kê (thông tin tự do)]** Chi phí không hợp lý |

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

