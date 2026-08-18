# `inv_` — Kho

> Sinh tự động từ [`ldm-Kho-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-Kho-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**28 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> LDM KHO — nguồn: PMKT-E-03585 Phiếu nhập kho · 03646 Phiếu xuất kho · 03589/03593/05969 Điều chuyển kho · 03635 Kiểm kê kho · 03629 Tính giá xuất kho · 14626 Lắp ráp - Tháo dỡ · 14636 Định mức NVL · 16371 Lệnh sản xuất. Danh mục dùng chung: ldm-DanhMuc-Update.puml. Entity <<ChiTiet>> thừa hưởng TenantId + ChiNhanhId qua entity cha. Mọi entity gốc do người dùng lập đều có ChiNhanhId (chi nhánh sở hữu bản ghi). Entity dẫn xuất (TonKho, CostLayer) không có — chi nhánh suy ra từ Kho.

**Epic nguồn:** PMKT-E-03585

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `PhieuNhapKho` | `inv_phieu_nhap_kho` | `inv_phieu_nhap_kho_module_kho` | B — có schema, chưa code | Đầu chứng từ — ENTITY CHÍNH: Phiếu nhập kho |
| 2 | `ChiTietPhieuNhapKho` | `inv_phieu_nhap_kho_chi_tiet` | `inv_chi_tiet_phieu_nhap_kho` | B — có schema, chưa code | Dòng chi tiết của `inv_phieu_nhap_kho` — ENTITY CHI TIẾT: Chi tiết phiếu nhập kho |
| 3 | `TonKho` | `inv_ton_kho` | `inv_ton_kho` | B — có schema, chưa code | Kết quả / số dư luân chuyển — ENTITY: Tồn kho (số dư live) — khóa TenantId + KhoId + VatTuId |
| 4 | `CostLayer` | `inv_lop_gia_von` | — | C — tạo mới | Kết quả / số dư luân chuyển — ENTITY: Lớp giá tồn kho (Cost Layer — FIFO) |
| 5 | `PhieuXuatKho` | `inv_phieu_xuat_kho` | `inv_phieu_xuat_kho_module_kho` | B — có schema, chưa code | Đầu chứng từ — ENTITY: Phiếu xuất kho |
| 6 | `ChiTietPhieuXuatKho` | `inv_phieu_xuat_kho_chi_tiet` | `inv_chi_tiet_phieu_xuat_kho` | B — có schema, chưa code | Dòng chi tiết của `inv_phieu_xuat_kho` — ENTITY CHI TIẾT: Chi tiết phiếu xuất kho |
| 7 | `PhieuXuatDieuChuyen` | `inv_phieu_xuat_dieu_chuyen` | `inv_phieu_xuat_dieu_chuyen` | B — có schema, chưa code | Đầu chứng từ — ENTITY: Phiếu xuất điều chuyển |
| 8 | `ChiTietPhieuXuatDieuChuyen` | `inv_phieu_xuat_dieu_chuyen_chi_tiet` | `inv_chi_tiet_phieu_xuat_dieu_chuyen` | B — có schema, chưa code | Dòng chi tiết của `inv_phieu_xuat_dieu_chuyen` — ⚠ *LDM chưa mô tả bảng này* |
| 9 | `PhieuNhapDieuChuyen` | `inv_phieu_nhap_dieu_chuyen` | `inv_phieu_nhap_dieu_chuyen` | B — có schema, chưa code | Đầu chứng từ — ENTITY: Phiếu nhập điều chuyển |
| 10 | `ChiTietPhieuNhapDieuChuyen` | `inv_phieu_nhap_dieu_chuyen_chi_tiet` | `inv_chi_tiet_phieu_nhap_dieu_chuyen` | B — có schema, chưa code | Dòng chi tiết của `inv_phieu_nhap_dieu_chuyen` — ⚠ *LDM chưa mô tả bảng này* |
| 11 | `PhieuDieuChuyenDieuChinh` | `inv_phieu_dieu_chuyen_dieu_chinh` | `inv_phieu_dieu_chuyen_dieu_chinh` | B — có schema, chưa code | Đầu chứng từ — ENTITY: Phiếu điều chuyển điều chỉnh (PMKT-E-05969) |
| 12 | `ChiTietPhieuDieuChuyenDieuChinh` | `inv_phieu_dieu_chuyen_dieu_chinh_chi_tiet` | `inv_chi_tiet_phieu_dieu_chuyen_dieu_chinh` | B — có schema, chưa code | Dòng chi tiết của `inv_phieu_dieu_chuyen_dieu_chinh` — ⚠ *LDM chưa mô tả bảng này* |
| 13 | `PhieuKiemKeKho` | `inv_phieu_kiem_ke_kho` | `inv_phieu_kiem_ke` | B — có schema, chưa code | Đầu chứng từ — ENTITY: Phiếu kiểm kê kho |
| 14 | `ChiTietPhieuKiemKeKho` | `inv_phieu_kiem_ke_kho_chi_tiet` | `inv_chi_tiet_kiem_ke` | B — có schema, chưa code | Dòng chi tiết của `inv_phieu_kiem_ke_kho` — ENTITY CHI TIẾT: Chi tiết phiếu kiểm kê kho |
| 15 | `ChiTietNguoiKiemKe` | `inv_phieu_kiem_ke_kho_nguoi_kiem_ke` | — | C — tạo mới | Dòng chi tiết của `inv_phieu_kiem_ke_kho` — ENTITY: Người kiểm kê (nhập tay tự do — KHÔNG FK danh mục nhân viên) |
| 16 | `ChiTietTonKhoSnapShot` | `inv_phieu_kiem_ke_kho_ton_kho_snapshot` | — | C — tạo mới | Dòng chi tiết của `inv_phieu_kiem_ke_kho` — ENTITY: Snapshot tồn kho lúc lập phiếu kiểm kê |
| 17 | `LenhLapRapThaoDo` | `inv_lenh_lap_rap_thao_do` | — | C — tạo mới | Bảng nghiệp vụ — ENTITY: Lệnh lắp ráp - tháo dỡ |
| 18 | `DauVaoLenhLapRapThaoDo` | `inv_lenh_lap_rap_thao_do_dau_vao` | — | C — tạo mới | Dòng chi tiết của `inv_lenh_lap_rap_thao_do` — ENTITY CHI TIẾT: Đầu vào lệnh (linh kiện lắp ráp / hàng hóa tháo dỡ) |
| 19 | `ThanhPhamSauLapRapThaoDo` | `inv_lenh_lap_rap_thao_do_thanh_pham_sau_lap_rap_thao_do` | — | C — tạo mới | Dòng chi tiết của `inv_lenh_lap_rap_thao_do` — ENTITY CHI TIẾT: Thành phẩm sau lắp ráp / sau tháo dỡ |
| 20 | `LuotTinhGiaXuatKho` | `inv_luot_tinh_gia_xuat_kho` | `inv_luot_tinh_gia_xuat_kho` | B — có schema, chưa code | Kết quả / số dư luân chuyển — ENTITY: Lượt tính giá xuất kho Một lượt xử lý đồng thời nhiều phương pháp; phương pháp lưu ở cấp batch (KetQuaTinhGiaXuatKho).… |
| 21 | `KetQuaTinhGiaXuatKho` | `inv_ket_qua_tinh_gia_xuat_kho` | `inv_ket_qua_tinh_gia_xuat_kho` | B — có schema, chưa code | Dòng chi tiết của `inv_luot_tinh_gia_xuat_kho` — ENTITY: Kết quả tính giá xuất kho (tổng hợp theo batch vật tư + kho) |
| 22 | `ChiTietApGiaXuatKho` | `inv_ket_qua_tinh_gia_xuat_kho_chi_tiet` | `inv_chi_tiet_ap_gia_xuat_kho` | B — có schema, chưa code | Dòng chi tiết của `inv_luot_tinh_gia_xuat_kho` — ENTITY: Chi tiết áp giá xuất kho |
| 23 | `DinhMucNVL` | `inv_dinh_muc_nguyen_vat_lieu` | — | C — tạo mới | Cấu hình / thiết lập — ENTITY: Định mức nguyên vật liệu |
| 24 | `ChiTietDinhMucNVL` | `inv_dinh_muc_nguyen_vat_lieu_chi_tiet` | — | C — tạo mới | Dòng chi tiết của `inv_dinh_muc_nguyen_vat_lieu` — ENTITY CHI TIẾT: Chi tiết định mức nguyên vật liệu |
| 25 | `LenhSanXuat` | `inv_lenh_san_xuat` | — | C — tạo mới | Bảng nghiệp vụ — ENTITY CHÍNH: Lệnh sản xuất |
| 26 | `ChiTietLenhSanXuat_ThanhPham` | `inv_lenh_san_xuat_thanh_pham` | — | C — tạo mới | Dòng chi tiết của `inv_lenh_san_xuat` — ENTITY CHI TIẾT: Dòng thành phẩm của lệnh sản xuất (tab Thành phẩm) |
| 27 | `ChiTietLenhSanXuat_NguyenVatLieu` | `inv_lenh_san_xuat_nguyen_vat_lieu` | — | C — tạo mới | Dòng chi tiết của `inv_lenh_san_xuat` — ENTITY CHI TIẾT: Dòng nguyên vật liệu của lệnh sản xuất (tab Nguyên vật liệu) |
| 28 | `LoaiTruNguyenVatLieuLenhSanXuat` | `inv_loai_tru_nguyen_vat_lieu_lenh_san_xuat` | — | C — tạo mới | Dòng chi tiết của `inv_lenh_san_xuat` — ENTITY: Dấu loại trừ dòng NVL tự động (BR4 — người dùng đã xóa dòng auto, re-fill không sinh lại) |

---

## 1. `inv_phieu_nhap_kho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuNhapKho` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_phieu_nhap_kho_module_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHÍNH: Phiếu nhập kho |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `inv_phieu_nhap_kho_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TinhChatNghiepVu` | `tinh_chat_nghiep_vu` | `text` CHECK | N | — | **[Phân loại nghiệp vụ]** (NhapThanhPham \| NhapHangBanTraLai \| NhapKhac \| NhapMua \| NhapXuLyChenhLech \| NhapThanhPhamLapRap \| NhapThanhPhamThaoDo) |
| 2 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | **[Thông tin chứng từ]** Lý do nhập kho (reference ENT_TaiKhoanNgamDinh) `FK` |
| 3 | `TenTaiKhoanNgamDinh` | `ten_tai_khoan_ngam_dinh` | `text` | Y | — | **[Thông tin chứng từ]** Tên lý do nhập (denormalized) |
| 4 | `ChungTuGocKemTheo` | `chung_tu_goc_kem_theo` | `text` | Y | — | **[Thông tin chứng từ]** Số chứng từ gốc kèm theo |
| 5 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin chứng từ]** Diễn giải |
| 6 | `NguoiGiaoHangId` | `nguoi_giao_hang_id` | `uuid` | Y | — | **[Giao nhận (mọi tính chất nghiệp vụ)]** ID người giao hàng (reference đến ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |
| 7 | `TenNguoiGiaoHang` | `ten_nguoi_giao_hang` | `text` | Y | — | **[Giao nhận (mọi tính chất nghiệp vụ)]** Tên người giao hàng |
| 8 | `NguoiNhanHangId` | `nguoi_nhan_hang_id` | `uuid` | Y | — | **[Giao nhận (mọi tính chất nghiệp vụ)]** ID người nhận hàng (reference đến ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |
| 9 | `TenNguoiNhanHang` | `ten_nguoi_nhan_hang` | `text` | Y | — | **[Giao nhận (mọi tính chất nghiệp vụ)]** Tên người nhận hàng |
| 10 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng của phiếu (dùng chung mọi tính chất — KHÔNG tách trường riêng theo vai trò)]** ID đối tượng (reference đến ENT_DoiTuong) `FK` |
| 11 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng của phiếu (dùng chung mọi tính chất — KHÔNG tách trường riêng theo vai trò)]** Tên đối tượng theo mã đã chọn |
| 12 | `NhanVienBanHangId` | `nhan_vien_ban_hang_id` | `uuid` | Y | — | **[Nhân sự phụ trách theo nghiệp vụ]** ID nhân viên bán hàng (reference đến ENT_DoiTuong, đối tượng có vai trò NhanVien). Chỉ TinhChatNghiepVu = NhapHangBanTraLai `FK` |
| 13 | `NhanVienMuaHangId` | `nhan_vien_mua_hang_id` | `uuid` | Y | — | **[Nhân sự phụ trách theo nghiệp vụ]** ID nhân viên mua hàng (reference đến ENT_DoiTuong, đối tượng có vai trò NhanVien). Chỉ TinhChatNghiepVu = NhapMua `FK` |
| 14 | `NguonId` | `nguon_id` | `uuid` | Y | — | **[NhapKhac            → NULL]** ID chứng từ nguồn sinh ra phiếu nhập (đa hình; entity xác định bởi LoaiChungTuNguon) |
| 15 | `LoaiChungTuNguon` | `loai_chung_tu_nguon` | `text` CHECK | Y | — | **[NhapKhac            → NULL]** (ChungTuTraLaiHangBan \| ChungTuMuaHang \| LenhSanXuat \| PhieuKiemKeKho \| LenhLapRapThaoDo) |
| 16 | `SoChungTuNguon` | `so_chung_tu_nguon` | `text` | Y | — | **[NhapKhac            → NULL]** Số chứng từ / số lệnh nguồn (denormalized) |
| 17 | `TongTien` | `tong_tien` | `money_foreign` ≈ | N | `0` | **[Tổng hợp]** Tổng tiền phiếu nhập = Σ ChiTietPhieuNhapKho.ThanhTienNhap |
| 18 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Trạng thái]** (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `inv_phieu_nhap_kho_module_kho` (24 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 16 | `tinh_chat_nghiep_vu`, `tai_khoan_ngam_dinh_id`, `ten_tai_khoan_ngam_dinh`, `chung_tu_goc_kem_theo`, `dien_giai`, `nguoi_giao_hang_id`, `ten_nguoi_giao_hang`, `nguoi_nhan_hang_id`, `ten_nguoi_nhan_hang`, `nhan_vien_ban_hang_id`, `nhan_vien_mua_hang_id`, `nguon_id`, `loai_chung_tu_nguon`, `so_chung_tu_nguon`, `tong_tien`, `trang_thai` |
| DB có — LDM **không khai** | 9 | `ly_do_nhap_id`, `nguoi_giao_hang`, `nguoi_nhan_hang`, `mo_ta`, `trang_thai_chung_tu`, `loai_nguon_id`, `so_chung_tu_goc`, `tong_gia_tri_nhap_kho`, `tong_gia_tri_nhap_kho_quy_doi` |

---

## 2. `inv_phieu_nhap_kho_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuNhapKho` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_chi_tiet_phieu_nhap_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Chi tiết phiếu nhập kho |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_nhap_kho` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_nhap_kho` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuNhapKhoId` | `phieu_nhap_kho_id` | `uuid` | N | — | ID phiếu nhập kho (reference đến ENT_PhieuNhapKho) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Vật tư & kho]** ID mã vật tư (reference đến ENT_VatTu) `FK` |
| 4 | `TenVatTuNhapKho` | `ten_vat_tu_nhap_kho` | `text` | N | — | **[Vật tư & kho]** Tên vật tư trên dòng phiếu |
| 5 | `KhoNhapId` | `kho_nhap_id` | `uuid` | N | — | **[Vật tư & kho]** ID kho nhập (reference đến ENT_Kho) `FK` |
| 6 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Tài khoản kế toán]** ID tài khoản nợ (reference đến ENT_HeThongTaiKhoan) `FK` |
| 7 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Tài khoản kế toán]** ID tài khoản có (reference đến ENT_HeThongTaiKhoan) `FK` |
| 8 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Đơn vị tính & quy đổi]** ID đơn vị tính đã chọn (reference đến ENT_DonViTinh) `FK` |
| 9 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | **[Đơn vị tính & quy đổi]** Hệ số quy đổi về ĐVT chuẩn (reference đến ENT_DonViQuyDoiVatTu) |
| 10 | `SoLuongNhap` | `so_luong_nhap` | `quantity` | N | `0` | **[Đơn vị tính & quy đổi]** Số lượng nhập theo ĐVT đã chọn |
| 11 | `SoLuongNhapQuyDoi` | `so_luong_nhap_quy_doi` | `quantity` | N | `0` | **[Đơn vị tính & quy đổi]** Số lượng quy đổi về ĐVT chuẩn = SoLuongNhap × HeSoQuyDoi |
| 12 | `TuDongApGia` | `tu_dong_ap_gia` | `boolean` | Y | `false` | **[Giá nhập]** Tự động áp giá (field màn: GiaTrungBinh). Không áp dụng khi TinhChatNghiepVu = NhapThanhPham |
| 13 | `DonGiaNhap` | `don_gia_nhap` | `money_foreign` ≈ | N | `0` | **[Giá nhập]** Đơn giá nhập |
| 14 | `DonGiaNhapQuyDoi` | `don_gia_nhap_quy_doi` | `money_vnd` | N | `0` | **[Giá nhập]** Đơn giá quy đổi về ĐVT chuẩn = DonGiaNhap × HeSoQuyDoi |
| 15 | `ThanhTienNhap` | `thanh_tien_nhap` | `money_foreign` ≈ | N | `0` | **[Giá nhập]** Thành tiền = SoLuongNhap × DonGiaNhap |
| 16 | `NguonId` | `nguon_id` | `uuid` | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng ThanhPhamSauLapRapThaoDo — chỉ NhapThanhPhamLapRap/ThaoDo]** ID chứng từ nguồn của dòng (đa hình; có thể khác NguonId của phiếu) |
| 17 | `LoaiChungTuNguon` | `loai_chung_tu_nguon` | `text` CHECK | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng ThanhPhamSauLapRapThaoDo — chỉ NhapThanhPhamLapRap/ThaoDo]** (PhieuXuatKho \| LenhSanXuat \| PhieuKiemKeKho \| LenhLapRapThaoDo) |
| 18 | `ChiTietNguonId` | `chi_tiet_nguon_id` | `uuid` | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng ThanhPhamSauLapRapThaoDo — chỉ NhapThanhPhamLapRap/ThaoDo]** ID dòng chi tiết nguồn (entity theo LoaiChungTuNguon) |
| 19 | `SoChungTuNguon` | `so_chung_tu_nguon` | `text` | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng ThanhPhamSauLapRapThaoDo — chỉ NhapThanhPhamLapRap/ThaoDo]** Số chứng từ / số lệnh nguồn (denormalized; field màn: SoPhieuXuat khi NhapHangBanTraLai, LenhSanXuat khi NhapThanhPham) |
| 20 | `DauVaoLenhLapRapThaoDoId` | `dau_vao_lenh_lap_rap_thao_do_id` | `uuid` | Y | — | **[Lắp ráp - tháo dỡ (không phải dòng nguồn)]** ID dòng hàng hóa được tháo dỡ (reference đến ENT_DauVaoLenhLapRapThaoDo). Chỉ TinhChatNghiepVu = NhapThanhPhamThaoDo `FK` |
| 21 | `TyLePhanBo` | `ty_le_phan_bo` | `percent_rate` | Y | `0` | **[Lắp ráp - tháo dỡ (không phải dòng nguồn)]** Tỷ lệ phân bổ giá trị (%). Chỉ TinhChatNghiepVu = NhapThanhPhamThaoDo |
| 22 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | **[Hợp đồng / Đơn hàng]** ID hợp đồng bán hàng (reference đến ENT_HopDongBanHang) `FK` |
| 23 | `DonHangId` | `don_hang_id` | `uuid` | Y | — | **[Hợp đồng / Đơn hàng]** ID đơn đặt hàng (reference đến ENT_DonDatHang) `FK` |
| 24 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 25 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID đơn vị (reference đến ENT_DonVi) `FK` |
| 26 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Thống kê dòng]** ID vụ việc (reference đến ENT_CongTrinh) `FK` |
| 27 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 28 | `GhiChu` | `ghi_chu` | `text` | Y | — | **[Thống kê dòng]** Ghi chú |

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

**Đối chiếu `inv_chi_tiet_phieu_nhap_kho` (30 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 13 | `so_thu_tu`, `tu_dong_ap_gia`, `nguon_id`, `loai_chung_tu_nguon`, `chi_tiet_nguon_id`, `so_chung_tu_nguon`, `dau_vao_lenh_lap_rap_thao_do_id`, `ty_le_phan_bo`, `don_hang_id`, `doi_tuong_tap_hop_chi_phi_id`, `don_vi_id`, `vu_viec_id`, `khoan_muc_chi_phi_id` |
| DB có — LDM **không khai** | 5 | `chi_tiet_phieu_xuat_kho_goc_id`, `gia_trung_binh`, `so_lo`, `han_su_dung`, `phien_ban` |

---

## 3. `inv_ton_kho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `TonKho` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_ton_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Tồn kho (số dư live) — khóa TenantId + KhoId + VatTuId |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoId` | `kho_id` | `uuid` | N | — | ID kho (reference đến ENT_Kho) `FK` |
| 2 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID vật tư (reference đến ENT_VatTu) `FK` |
| 3 | `DonViTinhChuanId` | `don_vi_tinh_chuan_id` | `uuid` | N | — | ID đơn vị tính chuẩn của vật tư (reference đến ENT_DonViTinh) `FK` |
| 4 | `SoLuongTon` | `so_luong_ton` | `quantity` | N | `0` | Số lượng tồn theo ĐVT chuẩn của vật tư |
| 5 | `GiaTriTon` | `gia_tri_ton` | `money_foreign` ≈ | N | `0` | Giá trị tồn (đồng tiền hạch toán) |

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

**Đối chiếu `inv_ton_kho` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `don_vi_tinh_chuan_id` |
| DB có — LDM **không khai** | 3 | `so_lo`, `gia_binh_quan`, `phien_ban` |

---

## 4. `inv_lop_gia_von`

| Mục | Nội dung |
|---|---|
| Entity LDM | `CostLayer` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Lớp giá tồn kho (Cost Layer — FIFO) |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `KhoId` | `kho_id` | `uuid` | N | — | ID kho (reference đến ENT_Kho) `FK` |
| 2 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID vật tư (reference đến ENT_VatTu) `FK` |
| 3 | `LoaiChungTuNhap` | `loai_chung_tu_nhap` | `text` CHECK | N | — | (PhieuNhapKho \| PhieuNhapDieuChuyen \| ChungTuMuaHang \| ChungTuDieuChinhGiaHangMua \| PhanBoChiPhiMuaHang) |
| 4 | `ChungTuNhapId` | `chung_tu_nhap_id` | `uuid` | N | — | ID chứng từ nhập nguồn |
| 5 | `ChiTietChungTuNhapId` | `chi_tiet_chung_tu_nhap_id` | `uuid` | N | — | ID dòng chi tiết nguồn |
| 6 | `NgayNhap` | `ngay_nhap` | `timestamptz` | N | — | Ngày hạch toán của chứng từ nguồn |
| 7 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | Đơn giá lớp theo ĐVT chuẩn (= đơn giá nhập quy đổi của dòng nguồn) |
| 8 | `SoLuongGoc` | `so_luong_goc` | `quantity` | N | `0` | Số lượng nhập gốc của lớp (= số lượng nhập quy đổi của dòng nguồn) |
| 9 | `GiaTriGoc` | `gia_tri_goc` | `money_foreign` ≈ | N | `0` | Giá trị nhập gốc của lớp (= thành tiền nhập của dòng nguồn) |
| 10 | `SoLuongConLai` | `so_luong_con_lai` | `quantity` | N | `0` | Số lượng còn lại của lớp |
| 11 | `GiaTriConLai` | `gia_tri_con_lai` | `money_foreign` ≈ | N | `0` | Giá trị còn lại của lớp |

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

## 5. `inv_phieu_xuat_kho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuXuatKho` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_phieu_xuat_kho_module_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Phiếu xuất kho |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `inv_phieu_xuat_kho_chi_tiet` · `inv_lenh_lap_rap_thao_do` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TinhChatNghiepVu` | `tinh_chat_nghiep_vu` | `text` CHECK | N | — | **[Phân loại nghiệp vụ]** (XuatBan \| XuatSanXuat \| XuatSuDungCCDC \| XuatKhac \| XuatXuLyChenhLech \| XuatLapRap \| XuatThaoDo) |
| 2 | `TaiKhoanNgamDinhId` | `tai_khoan_ngam_dinh_id` | `uuid` | N | — | **[Thông tin chứng từ]** Lý do xuất kho (reference ENT_TaiKhoanNgamDinh) `FK` |
| 3 | `TenTaiKhoanNgamDinh` | `ten_tai_khoan_ngam_dinh` | `text` | Y | — | **[Thông tin chứng từ]** Tên lý do xuất (denormalized) |
| 4 | `ChungTuGocKemTheo` | `chung_tu_goc_kem_theo` | `text` | Y | — | **[Thông tin chứng từ]** Số chứng từ gốc kèm theo |
| 5 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin chứng từ]** Diễn giải |
| 6 | `NguoiGiaoHangId` | `nguoi_giao_hang_id` | `uuid` | Y | — | **[Giao nhận (đồng nhất mô hình với PhieuNhapKho)]** ID người giao hàng (reference đến ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |
| 7 | `TenNguoiGiaoHang` | `ten_nguoi_giao_hang` | `text` | Y | — | **[Giao nhận (đồng nhất mô hình với PhieuNhapKho)]** Tên người giao hàng |
| 8 | `NguoiNhanHangId` | `nguoi_nhan_hang_id` | `uuid` | Y | — | **[Giao nhận (đồng nhất mô hình với PhieuNhapKho)]** ID người nhận hàng (reference đến ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |
| 9 | `TenNguoiNhanHang` | `ten_nguoi_nhan_hang` | `text` | Y | — | **[Giao nhận (đồng nhất mô hình với PhieuNhapKho)]** Tên người nhận hàng |
| 10 | `BoPhanNhanHangId` | `bo_phan_nhan_hang_id` | `uuid` | Y | — | **[Giao nhận (đồng nhất mô hình với PhieuNhapKho)]** ID bộ phận nhận hàng (reference đến ENT_DonVi, LoaiDonVi = PhongBan). Chỉ TinhChatNghiepVu = XuatSanXuat `FK` |
| 11 | `TenBoPhanNhanHang` | `ten_bo_phan_nhan_hang` | `text` | Y | — | **[Giao nhận (đồng nhất mô hình với PhieuNhapKho)]** Tên bộ phận nhận hàng |
| 12 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng của phiếu (dùng chung XuatBan/XuatKhac/XuatSuDungCCDC — KHÔNG tách trường riêng theo vai trò)]** ID đối tượng (reference đến ENT_DoiTuong) `FK` |
| 13 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng của phiếu (dùng chung XuatBan/XuatKhac/XuatSuDungCCDC — KHÔNG tách trường riêng theo vai trò)]** Tên đối tượng theo mã đã chọn |
| 14 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Đối tượng của phiếu (dùng chung XuatBan/XuatKhac/XuatSuDungCCDC — KHÔNG tách trường riêng theo vai trò)]** Địa chỉ |
| 15 | `DiaDiemGiaoHang` | `dia_diem_giao_hang` | `text` | Y | — | **[Đối tượng của phiếu (dùng chung XuatBan/XuatKhac/XuatSuDungCCDC — KHÔNG tách trường riêng theo vai trò)]** Địa điểm giao hàng |
| 16 | `NhanVienBanHangId` | `nhan_vien_ban_hang_id` | `uuid` | Y | — | **[Đối tượng của phiếu (dùng chung XuatBan/XuatKhac/XuatSuDungCCDC — KHÔNG tách trường riêng theo vai trò)]** ID nhân viên bán hàng (reference đến ENT_DoiTuong, đối tượng có vai trò NhanVien) `FK` |
| 17 | `NguonId` | `nguon_id` | `uuid` | Y | — | **[= ChungTuBan chỉ dùng cho phiếu xuất LẬP RIÊNG từ chứng từ bán (không kiêm).]** ID chứng từ nguồn sinh ra phiếu xuất (đa hình; entity xác định bởi LoaiChungTuNguon) |
| 18 | `LoaiChungTuNguon` | `loai_chung_tu_nguon` | `text` CHECK | Y | — | **[= ChungTuBan chỉ dùng cho phiếu xuất LẬP RIÊNG từ chứng từ bán (không kiêm).]** (ChungTuBan \| LenhSanXuat \| PhieuKiemKeKho \| LenhLapRapThaoDo) |
| 19 | `SoChungTuNguon` | `so_chung_tu_nguon` | `text` | Y | — | **[= ChungTuBan chỉ dùng cho phiếu xuất LẬP RIÊNG từ chứng từ bán (không kiêm).]** Số chứng từ / số lệnh nguồn (denormalized) |
| 20 | `TongTien` | `tong_tien` | `money_foreign` ≈ | N | `0` | **[Tổng hợp & trạng thái]** Tổng tiền = Σ ChiTietPhieuXuatKho.ThanhTienXuat |
| 21 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Tổng hợp & trạng thái]** (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `inv_phieu_xuat_kho_module_kho` (26 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 16 | `tinh_chat_nghiep_vu`, `tai_khoan_ngam_dinh_id`, `ten_tai_khoan_ngam_dinh`, `chung_tu_goc_kem_theo`, `dien_giai`, `nguoi_giao_hang_id`, `ten_nguoi_giao_hang`, `nguoi_nhan_hang_id`, `ten_nguoi_nhan_hang`, `bo_phan_nhan_hang_id`, `ten_bo_phan_nhan_hang`, `nguon_id`, `loai_chung_tu_nguon`, `so_chung_tu_nguon`, `tong_tien`, `trang_thai` |
| DB có — LDM **không khai** | 8 | `ly_do_xuat_id`, `trang_thai_chung_tu`, `khach_hang_id`, `nguoi_nhan_hang`, `mo_ta`, `loai_nguon_id`, `bo_phan_nhan_hang`, `tong_gia_tri_xuat_kho` |

---

## 6. `inv_phieu_xuat_kho_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuXuatKho` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_chi_tiet_phieu_xuat_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Chi tiết phiếu xuất kho |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_xuat_kho` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_xuat_kho` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuXuatKhoId` | `phieu_xuat_kho_id` | `uuid` | N | — | ID phiếu xuất kho (reference đến ENT_PhieuXuatKho) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Vật tư & kho]** ID mã vật tư (reference đến ENT_VatTu) `FK` |
| 4 | `TenVatTuXuatKho` | `ten_vat_tu_xuat_kho` | `text` | N | — | **[Vật tư & kho]** Tên vật tư trên dòng phiếu |
| 5 | `KhoXuatId` | `kho_xuat_id` | `uuid` | N | — | **[Vật tư & kho]** ID kho xuất (reference đến ENT_Kho) `FK` |
| 6 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | **[Tài khoản kế toán]** ID tài khoản nợ (reference đến ENT_HeThongTaiKhoan) `FK` |
| 7 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | **[Tài khoản kế toán]** ID tài khoản có (reference đến ENT_HeThongTaiKhoan) `FK` |
| 8 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Đơn vị tính & quy đổi]** ID đơn vị tính đã chọn (reference đến ENT_DonViTinh) `FK` |
| 9 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | **[Đơn vị tính & quy đổi]** Hệ số quy đổi về ĐVT chuẩn (reference đến ENT_DonViQuyDoiVatTu) |
| 10 | `SoLuongXuat` | `so_luong_xuat` | `quantity` | N | `0` | **[Đơn vị tính & quy đổi]** Số lượng xuất theo ĐVT đã chọn |
| 11 | `SoLuongXuatQuyDoi` | `so_luong_xuat_quy_doi` | `quantity` | N | `0` | **[Đơn vị tính & quy đổi]** Số lượng quy đổi về ĐVT chuẩn = SoLuongXuat × HeSoQuyDoi |
| 12 | `TuNhapDonGia` | `tu_nhap_don_gia` | `boolean` | Y | `false` | **[Giá xuất (= giá vốn)]** Tự nhập đơn giá (field màn: GiaDichDanh) |
| 13 | `DonGiaXuat` | `don_gia_xuat` | `money_foreign` ≈ | N | `0` | **[Giá xuất (= giá vốn)]** Đơn giá xuất kho theo ĐVT đã chọn, cũng là đơn giá vốn của dòng |
| 14 | `DonGiaXuatQuyDoi` | `don_gia_xuat_quy_doi` | `money_vnd` | N | `0` | **[Giá xuất (= giá vốn)]** Đơn giá quy đổi về ĐVT chuẩn = DonGiaXuat × HeSoQuyDoi |
| 15 | `ThanhTienXuat` | `thanh_tien_xuat` | `money_foreign` ≈ | N | `0` | **[Giá xuất (= giá vốn)]** Thành tiền = SoLuongXuat × DonGiaXuat, cũng là giá trị vốn xuất kho |
| 16 | `NguonId` | `nguon_id` | `uuid` | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng DauVaoLenhLapRapThaoDo — chỉ XuatLapRap/XuatThaoDo]** ID chứng từ nguồn của dòng (đa hình) |
| 17 | `LoaiChungTuNguon` | `loai_chung_tu_nguon` | `text` CHECK | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng DauVaoLenhLapRapThaoDo — chỉ XuatLapRap/XuatThaoDo]** (ChungTuBan \| LenhSanXuat \| PhieuKiemKeKho \| LenhLapRapThaoDo) |
| 18 | `ChiTietNguonId` | `chi_tiet_nguon_id` | `uuid` | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng DauVaoLenhLapRapThaoDo — chỉ XuatLapRap/XuatThaoDo]** ID dòng chi tiết nguồn (entity theo LoaiChungTuNguon) |
| 19 | `SoChungTuNguon` | `so_chung_tu_nguon` | `text` | Y | — | **[LenhLapRapThaoDo   → lệnh + dòng DauVaoLenhLapRapThaoDo — chỉ XuatLapRap/XuatThaoDo]** Số chứng từ / số lệnh nguồn (denormalized; field màn: ChungTuBanHang khi XuatBan, LenhSanXuat khi XuatSanXuat) |
| 20 | `ThanhPhamSauLapRapThaoDoId` | `thanh_pham_sau_lap_rap_thao_do_id` | `uuid` | Y | — | **[Lắp ráp - tháo dỡ (không phải dòng nguồn)]** ID dòng thành phẩm mà linh kiện gắn với (reference đến ENT_ThanhPhamSauLapRapThaoDo). Chỉ TinhChatNghiepVu = XuatLapRap `FK` |
| 21 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | **[Tồn kho theo lô (đặt chỗ phase sau)]** Số lô |
| 22 | `HanSuDung` | `han_su_dung` | `date` | Y | — | **[Tồn kho theo lô (đặt chỗ phase sau)]** Hạn sử dụng |
| 23 | `ChiPhiKhongHopLy` | `chi_phi_khong_hop_ly` | `boolean` | Y | `false` | **[Thống kê dòng]** Chi phí không hợp lý |
| 24 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | **[Thống kê dòng]** ID hợp đồng bán hàng (reference đến ENT_HopDongBanHang) `FK` |
| 25 | `ChiTietHopDongBanHangId` | `chi_tiet_hop_dong_ban_hang_id` | `uuid` | Y | — | **[Thống kê dòng]** ID dòng chi tiết hợp đồng bán hàng nguồn (reference đến ENT_ChiTietHopDongBanHang) `FK` |
| 26 | `DonHangId` | `don_hang_id` | `uuid` | Y | — | **[Thống kê dòng]** ID đơn đặt hàng (reference đến ENT_DonDatHang) `FK` |
| 27 | `ChiTietDonDatHangId` | `chi_tiet_don_dat_hang_id` | `uuid` | Y | — | **[Thống kê dòng]** ID dòng chi tiết đơn đặt hàng nguồn (reference đến ENT_ChiTietDonDatHang) `FK` |
| 28 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 29 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID đơn vị (reference đến ENT_DonVi) `FK` |
| 30 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Thống kê dòng]** ID vụ việc (reference đến ENT_CongTrinh) `FK` |
| 31 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 32 | `GhiChu` | `ghi_chu` | `text` | Y | — | **[Thống kê dòng]** Ghi chú |

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

**Đối chiếu `inv_chi_tiet_phieu_xuat_kho` (35 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 10 | `so_thu_tu`, `nguon_id`, `loai_chung_tu_nguon`, `chi_tiet_nguon_id`, `so_chung_tu_nguon`, `thanh_pham_sau_lap_rap_thao_do_id`, `so_lo`, `han_su_dung`, `chi_tiet_hop_dong_ban_hang_id`, `chi_tiet_don_dat_hang_id` |
| DB có — LDM **không khai** | 3 | `gia_dich_danh`, `lenh_san_xuat_id`, `phien_ban` |

---

## 7. `inv_phieu_xuat_dieu_chuyen`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuXuatDieuChuyen` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_phieu_xuat_dieu_chuyen` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Phiếu xuất điều chuyển |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `inv_phieu_nhap_dieu_chuyen` — FK `ON DELETE CASCADE` |
| Bảng con | `inv_phieu_xuat_dieu_chuyen_chi_tiet` · `inv_phieu_nhap_dieu_chuyen` · `inv_phieu_dieu_chuyen_dieu_chinh` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiPhieu` | `loai_phieu` | `text` CHECK | N | — | (XuatChuyenKhoNoiBo \| XuatKhoKiemVanChuyenNoiBo) |
| 2 | `LenhDieuDong` | `lenh_dieu_dong` | `text` | Y | — | Lệnh điều động. Chỉ LoaiPhieu = XuatKhoKiemVanChuyenNoiBo |
| 3 | `KhoXuatId` | `kho_xuat_id` | `uuid` | N | — | ID kho xuất (reference đến ENT_Kho, LaKhoAo = false) `FK` |
| 4 | `KhoNhapId` | `kho_nhap_id` | `uuid` | N | — | ID kho nhập (reference đến ENT_Kho, LaKhoAo = false) `FK` |
| 5 | `KhoHangDiDuongId` | `kho_hang_di_duong_id` | `uuid` | Y | — | ID kho hàng đi đường (reference đến ENT_Kho, LaKhoAo = true). Chỉ LoaiPhieu = XuatKhoKiemVanChuyenNoiBo `FK` |
| 6 | `DiaDiemKhoXuat` | `dia_diem_kho_xuat` | `text` | Y | — | Địa điểm kho xuất |
| 7 | `DiaDiemKhoNhap` | `dia_diem_kho_nhap` | `text` | Y | — | Địa điểm kho nhập |
| 8 | `NguoiXuatHang` | `nguoi_xuat_hang` | `text` | Y | — | Người xuất hàng |
| 9 | `NguoiNhanHang` | `nguoi_nhan_hang` | `text` | Y | — | Người nhận hàng |
| 10 | `NguoiVanChuyen` | `nguoi_van_chuyen` | `text` | Y | — | Người vận chuyển |
| 11 | `PhuongTienVanChuyen` | `phuong_tien_van_chuyen` | `text` | Y | — | Phương tiện vận chuyển. Chỉ LoaiPhieu = XuatKhoKiemVanChuyenNoiBo |
| 12 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |
| 13 | `TongTien` | `tong_tien` | `money_foreign` ≈ | N | `0` | Tổng tiền = Σ ChiTietPhieuXuatDieuChuyen.ThanhTienXuat |
| 14 | `TrangThaiGhiSo` | `trang_thai_ghi_so` | `text` CHECK | N | — | (ChuaGhiSo \| DaGhiSo) |
| 15 | `TrangThaiPhieu` | `trang_thai_phieu` | `text` CHECK | N | — | (DaLapChungTu \| DangDieuChuyen \| DangDieuChinh \| HoanThanh) |
| 16 | `PhieuNhapDieuChuyenId` | `phieu_nhap_dieu_chuyen_id` | `uuid` | Y | — | ID phiếu nhập điều chuyển liên kết (reference đến ENT_PhieuNhapDieuChuyen) `FK` `UNIQUE` |
| 17 | `PhieuDieuChuyenDieuChinhId` | `phieu_dieu_chuyen_dieu_chinh_id` | `uuid` | Y | — | ID phiếu điều chỉnh liên kết (reference đến ENT_PhieuDieuChuyenDieuChinh) `FK` `UNIQUE` |

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

**Đối chiếu `inv_phieu_xuat_dieu_chuyen` (30 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `dien_giai`, `tong_tien`, `trang_thai_ghi_so` |
| DB có — LDM **không khai** | 3 | `trang_thai_chung_tu`, `mo_ta`, `tong_gia_tri_xuat_kho` |

---

## 8. `inv_phieu_xuat_dieu_chuyen_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuXuatDieuChuyen` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_chi_tiet_phieu_xuat_dieu_chuyen` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_xuat_dieu_chuyen` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_xuat_dieu_chuyen` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuXuatDieuChuyenId` | `phieu_xuat_dieu_chuyen_id` | `uuid` | N | — | ID phiếu xuất điều chuyển (reference đến ENT_PhieuXuatDieuChuyen) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID mã vật tư (reference đến ENT_VatTu) `FK` |
| 4 | `TenVatTu` | `ten_vat_tu` | `text` | Y | — | Tên vật tư |
| 5 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | ID đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 6 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | Hệ số quy đổi về ĐVT chuẩn |
| 7 | `TonKhoXuat` | `ton_kho_xuat` | `numeric(18,4)` ⚠ | N | `0` | Số lượng tồn kho xuất tại thời điểm lập phiếu (ĐVT đã chọn) |
| 8 | `SoLuongDieuChuyen` | `so_luong_dieu_chuyen` | `quantity` | N | `0` | Số lượng điều chuyển theo ĐVT đã chọn |
| 9 | `SoLuongDieuChuyenQuyDoi` | `so_luong_dieu_chuyen_quy_doi` | `quantity` | N | `0` | Số lượng quy đổi về ĐVT chuẩn = SoLuongDieuChuyen × HeSoQuyDoi |
| 10 | `TuNhapDonGia` | `tu_nhap_don_gia` | `boolean` | Y | `false` | Tự nhập đơn giá (field màn: GiaDichDanh) |
| 11 | `DonGiaXuat` | `don_gia_xuat` | `money_foreign` ≈ | N | `0` | Đơn giá xuất |
| 12 | `DonGiaQuyDoi` | `don_gia_quy_doi` | `money_vnd` | N | `0` | Đơn giá quy đổi về ĐVT chuẩn = DonGiaXuat × HeSoQuyDoi |
| 13 | `ThanhTienXuat` | `thanh_tien_xuat` | `money_foreign` ≈ | N | `0` | Thành tiền = SoLuongDieuChuyen × DonGiaXuat |
| 14 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản nợ (reference đến ENT_HeThongTaiKhoan) `FK` |
| 15 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản có (reference đến ENT_HeThongTaiKhoan) `FK` |
| 16 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | ID hợp đồng bán hàng (reference đến ENT_HopDongBanHang) `FK` |
| 17 | `DonHangId` | `don_hang_id` | `uuid` | Y | — | ID đơn đặt hàng (reference đến ENT_DonDatHang) `FK` |
| 18 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | Y | — | ID lệnh sản xuất (reference đến ENT_LenhSanXuat) `FK` |
| 19 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 20 | `DonViId` | `don_vi_id` | `uuid` | Y | — | ID đơn vị (reference đến ENT_DonVi) `FK` |
| 21 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID vụ việc (reference đến ENT_CongTrinh) `FK` |
| 22 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 23 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú |

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

**Đối chiếu `inv_chi_tiet_phieu_xuat_dieu_chuyen` (32 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `so_thu_tu`, `ton_kho_xuat`, `tu_nhap_don_gia`, `don_gia_quy_doi` |
| DB có — LDM **không khai** | 3 | `gia_dich_danh`, `don_gia_xuat_quy_doi`, `phien_ban` |

---

## 9. `inv_phieu_nhap_dieu_chuyen`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuNhapDieuChuyen` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_phieu_nhap_dieu_chuyen` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Phiếu nhập điều chuyển |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `inv_phieu_xuat_dieu_chuyen` — FK `ON DELETE CASCADE` |
| Bảng con | `inv_phieu_xuat_dieu_chuyen` · `inv_phieu_nhap_dieu_chuyen_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuXuatDieuChuyenId` | `phieu_xuat_dieu_chuyen_id` | `uuid` | N | — | ID phiếu xuất điều chuyển nguồn (reference đến ENT_PhieuXuatDieuChuyen) `FK` `UNIQUE` |
| 2 | `NguoiNhanHang` | `nguoi_nhan_hang` | `text` | Y | — | Người nhận hàng |
| 3 | `NguoiVanChuyen` | `nguoi_van_chuyen` | `text` | Y | — | Người vận chuyển |
| 4 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |
| 5 | `TongTien` | `tong_tien` | `money_foreign` ≈ | N | `0` | Tổng tiền = Σ ChiTietPhieuNhapDieuChuyen.ThanhTienNhap |
| 6 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | (ChuaGhiSo \| DaGhiSo) |
| 7 | `PhieuDieuChuyenDieuChinhId` | `phieu_dieu_chuyen_dieu_chinh_id` | `uuid` | Y | — | ID phiếu điều chỉnh liên kết (reference đến ENT_PhieuDieuChuyenDieuChinh) `FK` |

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

**Đối chiếu `inv_phieu_nhap_dieu_chuyen` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 4 | `nguoi_van_chuyen`, `dien_giai`, `tong_tien`, `trang_thai` |
| DB có — LDM **không khai** | 4 | `lenh_dieu_dong`, `mo_ta`, `trang_thai_chung_tu`, `tong_gia_tri_nhap_kho` |

---

## 10. `inv_phieu_nhap_dieu_chuyen_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuNhapDieuChuyen` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_chi_tiet_phieu_nhap_dieu_chuyen` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_nhap_dieu_chuyen` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_nhap_dieu_chuyen` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuNhapDieuChuyenId` | `phieu_nhap_dieu_chuyen_id` | `uuid` | N | — | ID phiếu nhập điều chuyển (reference đến ENT_PhieuNhapDieuChuyen) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `ChiTietPhieuXuatDieuChuyenId` | `chi_tiet_phieu_xuat_dieu_chuyen_id` | `uuid` | N | — | ID dòng PXĐC nguồn (reference đến ENT_ChiTietPhieuXuatDieuChuyen) `FK` |
| 4 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | Hệ số quy đổi về ĐVT chuẩn |
| 5 | `SoLuongThucNhan` | `so_luong_thuc_nhan` | `quantity` | N | `0` | Số lượng thực nhận |
| 6 | `SoLuongThucNhanQuyDoi` | `so_luong_thuc_nhan_quy_doi` | `quantity` | N | `0` | Số lượng quy đổi về ĐVT chuẩn = SoLuongThucNhan × HeSoQuyDoi |
| 7 | `ThanhTienNhap` | `thanh_tien_nhap` | `money_foreign` ≈ | N | `0` | Thành tiền nhập |
| 8 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | N | — | ID tài khoản nợ (reference đến ENT_HeThongTaiKhoan) `FK` |
| 9 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | N | — | ID tài khoản có (reference đến ENT_HeThongTaiKhoan) `FK` |
| 10 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | ID hợp đồng bán hàng (reference đến ENT_HopDongBanHang) `FK` |
| 11 | `DonHangId` | `don_hang_id` | `uuid` | Y | — | ID đơn đặt hàng (reference đến ENT_DonDatHang) `FK` |
| 12 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | Y | — | ID lệnh sản xuất (reference đến ENT_LenhSanXuat) `FK` |
| 13 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 14 | `DonViId` | `don_vi_id` | `uuid` | Y | — | ID đơn vị (reference đến ENT_DonVi) `FK` |
| 15 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | ID vụ việc (reference đến ENT_CongTrinh) `FK` |
| 16 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | ID khoản mục chi phí (reference đến ENT_KhoanMucChiPhi) `FK` |
| 17 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú |

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

**Đối chiếu `inv_chi_tiet_phieu_nhap_dieu_chuyen` (32 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 1 | `so_thu_tu` |
| DB có — LDM **không khai** | 6 | `vat_tu_id`, `ten_vat_tu`, `don_vi_tinh_id`, `don_gia_nhap`, `don_gia_nhap_quy_doi`, `phien_ban` |

---

## 11. `inv_phieu_dieu_chuyen_dieu_chinh`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuDieuChuyenDieuChinh` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_phieu_dieu_chuyen_dieu_chinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Phiếu điều chuyển điều chỉnh (PMKT-E-05969) |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `inv_phieu_xuat_dieu_chuyen` — FK `ON DELETE CASCADE` |
| Bảng con | `inv_phieu_dieu_chuyen_dieu_chinh_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuXuatDieuChuyenId` | `phieu_xuat_dieu_chuyen_id` | `uuid` | N | — | ID phiếu xuất điều chuyển gốc (reference đến ENT_PhieuXuatDieuChuyen) `FK` `UNIQUE` |
| 2 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải |
| 3 | `TongTienDieuChinh` | `tong_tien_dieu_chinh` | `money_foreign` ≈ | N | `0` | Tổng tiền điều chỉnh = Σ ChiTietPhieuDieuChuyenDieuChinh.ThanhTienDieuChinh |
| 4 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | (ChuaGhiSo \| DaGhiSo) |

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

**Đối chiếu `inv_phieu_dieu_chuyen_dieu_chinh` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 3 | `dien_giai`, `tong_tien_dieu_chinh`, `trang_thai` |
| DB có — LDM **không khai** | 3 | `lenh_dieu_dong`, `mo_ta`, `trang_thai_chung_tu` |

---

## 12. `inv_phieu_dieu_chuyen_dieu_chinh_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuDieuChuyenDieuChinh` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_chi_tiet_phieu_dieu_chuyen_dieu_chinh` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_dieu_chuyen_dieu_chinh` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_dieu_chuyen_dieu_chinh` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuDieuChuyenDieuChinhId` | `phieu_dieu_chuyen_dieu_chinh_id` | `uuid` | N | — | ID phiếu điều chỉnh (reference đến ENT_PhieuDieuChuyenDieuChinh) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `ChiTietPhieuXuatDieuChuyenId` | `chi_tiet_phieu_xuat_dieu_chuyen_id` | `uuid` | N | — | ID dòng PXĐC gốc (reference đến ENT_ChiTietPhieuXuatDieuChuyen) `FK` |
| 4 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | Hệ số quy đổi về ĐVT chuẩn |
| 5 | `SoLuongDieuChinh` | `so_luong_dieu_chinh` | `quantity` | N | `0` | Số lượng điều chỉnh giảm |
| 6 | `SoLuongDieuChinhQuyDoi` | `so_luong_dieu_chinh_quy_doi` | `quantity` | N | `0` | Số lượng quy đổi về ĐVT chuẩn = SoLuongDieuChinh × HeSoQuyDoi |
| 7 | `DonGiaDieuChinh` | `don_gia_dieu_chinh` | `money_foreign` ≈ | N | `0` | Đơn giá điều chỉnh (= đơn giá dòng PXĐC gốc) |
| 8 | `ThanhTienDieuChinh` | `thanh_tien_dieu_chinh` | `money_foreign` ≈ | N | `0` | Thành tiền = SoLuongDieuChinh × DonGiaDieuChinh |
| 9 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú |

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

**Đối chiếu `inv_chi_tiet_phieu_dieu_chuyen_dieu_chinh` (23 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `so_thu_tu`, `don_gia_dieu_chinh` |
| DB có — LDM **không khai** | 6 | `vat_tu_id`, `ten_vat_tu`, `don_vi_tinh_id`, `don_gia_xuat_dieu_chinh`, `don_gia_xuat_dieu_chinh_quy_doi`, `phien_ban` |

---

## 13. `inv_phieu_kiem_ke_kho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhieuKiemKeKho` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_phieu_kiem_ke` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Phiếu kiểm kê kho |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `inv_phieu_kiem_ke_kho_chi_tiet` · `inv_phieu_kiem_ke_kho_nguoi_kiem_ke` · `inv_phieu_kiem_ke_kho_ton_kho_snapshot` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `NgayKiemKe` | `ngay_kiem_ke` | `date` | N | — | Ngày kiểm kê |
| 2 | `TonKhoDenNgay` | `ton_kho_den_ngay` | `date` | N | — | Ngày chốt số liệu tồn kho sổ sách |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | Mục đích kiểm kê |
| 4 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú |
| 5 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | (Khop \| ChuaXuLy \| DangXuLy \| DaXuLy) |

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

**Đối chiếu `inv_phieu_kiem_ke` (16 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `ton_kho_den_ngay`, `ghi_chu` |
| DB có — LDM **không khai** | 1 | `kho_id` |

---

## 14. `inv_phieu_kiem_ke_kho_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietPhieuKiemKeKho` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_chi_tiet_kiem_ke` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Chi tiết phiếu kiểm kê kho |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_kiem_ke_kho` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_kiem_ke_kho` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKiemKeKhoId` | `phieu_kiem_ke_kho_id` | `uuid` | N | — | ID phiếu kiểm kê (reference đến ENT_PhieuKiemKeKho) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `ChiTietTonKhoSnapShotId` | `chi_tiet_ton_kho_snap_shot_id` | `uuid` | Y | — | ID dòng snapshot tồn kho nguồn (reference đến ENT_ChiTietTonKhoSnapShot) `FK` |
| 4 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID mã vật tư (reference đến ENT_VatTu) `FK` |
| 5 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | Tên vật tư |
| 6 | `NhomVatTuId` | `nhom_vat_tu_id` | `uuid` | Y | — | ID nhóm vật tư (reference đến ENT_NhomVatTu) `FK` |
| 7 | `KhoId` | `kho_id` | `uuid` | N | — | ID kho (reference đến ENT_Kho) `FK` |
| 8 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | ID đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 9 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | Hệ số quy đổi về ĐVT chuẩn |
| 10 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | Số lô |
| 11 | `HanSuDung` | `han_su_dung` | `date` | Y | — | Hạn sử dụng |
| 12 | `DongHeThong` | `dong_he_thong` | `boolean` | N | `false` | true: dòng hệ thống sinh từ tồn kho; false: dòng người dùng thêm |
| 13 | `SoLuongSoSach` | `so_luong_so_sach` | `quantity` | N | `0` | Số lượng tồn sổ sách tại TonKhoDenNgay |
| 14 | `SoLuongThucTe` | `so_luong_thuc_te` | `quantity` | N | `0` | Số lượng thực tế kiểm đếm |
| 15 | `SoLuongTot` | `so_luong_tot` | `quantity` | N | `0` | Số lượng Tốt |
| 16 | `SoLuongKem` | `so_luong_kem` | `quantity` | N | `0` | Số lượng Kém |
| 17 | `SoLuongHong` | `so_luong_hong` | `quantity` | N | `0` | Số lượng Hỏng |
| 18 | `SoLuongChenhLech` | `so_luong_chenh_lech` | `quantity` | N | `0` | Số lượng chênh lệch = SoLuongThucTe − SoLuongSoSach |
| 19 | `XuLy` | `xu_ly` | `text` CHECK | N | — | (NhapKho \| XuatKho \| Khop) |
| 20 | `SoLuongXuLyChenhLech` | `so_luong_xu_ly_chenh_lech` | `quantity` | N | `0` | Số lượng chênh lệch đã xử lý |
| 21 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú |

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

**Đối chiếu `inv_chi_tiet_kiem_ke` (27 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 9 | `phieu_kiem_ke_kho_id`, `so_thu_tu`, `chi_tiet_ton_kho_snap_shot_id`, `nhom_vat_tu_id`, `kho_id`, `he_so_quy_doi`, `dong_he_thong`, `xu_ly`, `so_luong_xu_ly_chenh_lech` |
| DB có — LDM **không khai** | 5 | `phieu_kiem_ke_id`, `don_gia`, `gia_tri_chenh_lech`, `ly_do`, `phien_ban` |

---

## 15. `inv_phieu_kiem_ke_kho_nguoi_kiem_ke`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietNguoiKiemKe` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Người kiểm kê (nhập tay tự do — KHÔNG FK danh mục nhân viên) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_kiem_ke_kho` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_kiem_ke_kho` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKiemKeKhoId` | `phieu_kiem_ke_kho_id` | `uuid` | N | — | ID phiếu kiểm kê (reference đến ENT_PhieuKiemKeKho) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `HoVaTen` | `ho_va_ten` | `text` | Y | — | Họ và tên người kiểm kê |
| 4 | `ChucDanh` | `chuc_danh` | `text` | Y | — | Chức danh |
| 5 | `DaiDien` | `dai_dien` | `text` | Y | — | Đại diện |

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

## 16. `inv_phieu_kiem_ke_kho_ton_kho_snapshot`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietTonKhoSnapShot` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Snapshot tồn kho lúc lập phiếu kiểm kê |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_phieu_kiem_ke_kho` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_phieu_kiem_ke_kho` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `PhieuKiemKeKhoId` | `phieu_kiem_ke_kho_id` | `uuid` | N | — | ID phiếu kiểm kê (reference đến ENT_PhieuKiemKeKho) `FK` |
| 2 | `KhoId` | `kho_id` | `uuid` | N | — | ID kho (reference đến ENT_Kho) `FK` |
| 3 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID vật tư (reference đến ENT_VatTu) `FK` |
| 4 | `SoLo` | `so_lo` | `varchar(50)` | Y | — | Số lô ghi nhận khi kiểm kê |
| 5 | `HanSuDung` | `han_su_dung` | `date` | Y | — | Hạn sử dụng ghi nhận khi kiểm kê |
| 6 | `Serial` | `serial` | `text` | Y | — | Serial ghi nhận khi kiểm kê |
| 7 | `SoLuongTon` | `so_luong_ton` | `quantity` | N | `0` | Số lượng tồn sổ sách tại TonKhoDenNgay (ĐVT chuẩn) |
| 8 | `GiaTriTon` | `gia_tri_ton` | `money_foreign` ≈ | N | `0` | Giá trị tồn tại thời điểm snapshot |

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

## 17. `inv_lenh_lap_rap_thao_do`

| Mục | Nội dung |
|---|---|
| Entity LDM | `LenhLapRapThaoDo` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Lệnh lắp ráp - tháo dỡ |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng cha | `inv_phieu_xuat_kho` — FK `ON DELETE CASCADE` |
| Bảng con | `inv_lenh_lap_rap_thao_do_dau_vao` · `inv_lenh_lap_rap_thao_do_thanh_pham_sau_lap_rap_thao_do` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LoaiLenh` | `loai_lenh` | `text` CHECK | N | — | (LapRap \| ThaoDo) |
| 2 | `SoLenhLapRapThaoDo` | `so_lenh_lap_rap_thao_do` | `text` | N | — | Số lệnh |
| 3 | `NgayLapLenh` | `ngay_lap_lenh` | `date` | N | — | Ngày lập lệnh |
| 4 | `TuDongTinhGiaTheoTyLe` | `tu_dong_tinh_gia_theo_ty_le` | `boolean` | Y | `false` | Tự động tính giá theo tỷ lệ. Chỉ LoaiLenh = ThaoDo |
| 5 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải nghiệp vụ |
| 6 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | (DaLap \| DaXuatKho \| HoanThanh) |
| 7 | `PhieuXuatKhoId` | `phieu_xuat_kho_id` | `uuid` | Y | — | ID phiếu xuất kho liên kết (reference đến ENT_PhieuXuatKho) `FK` `UNIQUE` |
| 8 | `PhieuNhapKhoId` | `phieu_nhap_kho_id` | `uuid` | Y | — | ID phiếu nhập kho liên kết (reference đến ENT_PhieuNhapKho) `FK` `UNIQUE` |

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

## 18. `inv_lenh_lap_rap_thao_do_dau_vao`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DauVaoLenhLapRapThaoDo` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Đầu vào lệnh (linh kiện lắp ráp / hàng hóa tháo dỡ) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_lenh_lap_rap_thao_do` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_lenh_lap_rap_thao_do` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LenhLapRapThaoDoId` | `lenh_lap_rap_thao_do_id` | `uuid` | N | — | ID lệnh (reference đến ENT_LenhLapRapThaoDo) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID mã hàng (reference đến ENT_VatTu) `FK` |
| 4 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | Tên hàng |
| 5 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | ID đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 6 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | Hệ số quy đổi về ĐVT chuẩn |
| 7 | `SoLuong` | `so_luong` | `quantity` | N | `0` | Số lượng |
| 8 | `SoLuongQuyDoi` | `so_luong_quy_doi` | `quantity` | N | `0` | Số lượng quy đổi về ĐVT chuẩn = SoLuong × HeSoQuyDoi |

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

## 19. `inv_lenh_lap_rap_thao_do_thanh_pham_sau_lap_rap_thao_do`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ThanhPhamSauLapRapThaoDo` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Thành phẩm sau lắp ráp / sau tháo dỡ |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_lenh_lap_rap_thao_do` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_lenh_lap_rap_thao_do` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LenhLapRapThaoDoId` | `lenh_lap_rap_thao_do_id` | `uuid` | N | — | ID lệnh (reference đến ENT_LenhLapRapThaoDo) `FK` |
| 2 | `DauVaoLenhLapRapThaoDoId` | `dau_vao_lenh_lap_rap_thao_do_id` | `uuid` | Y | — | ID dòng hàng hóa tháo dỡ nguồn (reference đến ENT_DauVaoLenhLapRapThaoDo). Chỉ LoaiLenh = ThaoDo `FK` |
| 3 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 4 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID mã hàng (reference đến ENT_VatTu) `FK` |
| 5 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | Tên hàng |
| 6 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | ID đơn vị tính (reference đến ENT_DonViTinh) `FK` |
| 7 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | Hệ số quy đổi về ĐVT chuẩn |
| 8 | `SoLuong` | `so_luong` | `quantity` | N | `0` | Số lượng |
| 9 | `SoLuongQuyDoi` | `so_luong_quy_doi` | `quantity` | N | `0` | Số lượng quy đổi về ĐVT chuẩn = SoLuong × HeSoQuyDoi |
| 10 | `TyLePhanBo` | `ty_le_phan_bo` | `percent_rate` | Y | `0` | Tỷ lệ phân bổ giá trị (%). Chỉ LoaiLenh = ThaoDo |

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

## 20. `inv_luot_tinh_gia_xuat_kho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `LuotTinhGiaXuatKho` |
| Base class | `TenantedEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_luot_tinh_gia_xuat_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Lượt tính giá xuất kho · Một lượt xử lý đồng thời nhiều phương pháp; phương pháp lưu ở cấp batch · (KetQuaTinhGiaXuatKho). Batch = vật tư (+ kho khi TinhGiaTheoKho = true) |
| Vai trò | Bảng kết quả / số dư luân chuyển |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc. |
| Bảng con | `inv_ket_qua_tinh_gia_xuat_kho` · `inv_ket_qua_tinh_gia_xuat_kho_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `TuNgay` | `tu_ngay` | `date` | N | — | Từ ngày |
| 2 | `DenNgay` | `den_ngay` | `date` | N | — | Đến ngày |
| 3 | `TinhGiaTheoKho` | `tinh_gia_theo_kho` | `boolean` | N | `false` | Tính giá theo kho |
| 4 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú |
| 5 | `TuDong` | `tu_dong` | `boolean` | N | `false` | Lượt kích hoạt tự động khi Ghi sổ |
| 6 | `TongSoVatTu` | `tong_so_vat_tu` | `money_foreign` ≈ | N | `0` | Tổng số batch cần tính giá của lượt |
| 7 | `SoVatTuHoanThanh` | `so_vat_tu_hoan_thanh` | `numeric(18,4)` ⚠ | N | `0` | Số batch đã tính giá xong |
| 8 | `ThoiGianBatDau` | `thoi_gian_bat_dau` | `timestamptz` | Y | — | Thời điểm bắt đầu xử lý lượt |
| 9 | `ThoiGianKetThuc` | `thoi_gian_ket_thuc` | `timestamptz` | Y | — | Thời điểm kết thúc xử lý lượt |
| 10 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | (DangChay \| HoanThanh \| HoanThanhCoLoi \| Loi \| DaHuy) |

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

**Đối chiếu `inv_luot_tinh_gia_xuat_kho` (20 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `tinh_gia_theo_kho`, `ghi_chu`, `tong_so_vat_tu`, `so_vat_tu_hoan_thanh`, `thoi_gian_bat_dau`, `thoi_gian_ket_thuc` |
| DB có — LDM **không khai** | 7 | `phuong_phap`, `hinh_thuc_tinh_gia`, `tong_batch`, `batch_thanh_cong`, `batch_loi`, `thong_bao`, `phien_ban` |

---

## 21. `inv_ket_qua_tinh_gia_xuat_kho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `KetQuaTinhGiaXuatKho` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_ket_qua_tinh_gia_xuat_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Kết quả tính giá xuất kho (tổng hợp theo batch vật tư + kho) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_luot_tinh_gia_xuat_kho` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_luot_tinh_gia_xuat_kho` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LuotTinhGiaXuatKhoId` | `luot_tinh_gia_xuat_kho_id` | `uuid` | N | — | ID lượt tính giá (reference đến ENT_LuotTinhGiaXuatKho) `FK` |
| 2 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID vật tư của batch (reference đến ENT_VatTu) `FK` |
| 3 | `KhoId` | `kho_id` | `uuid` | Y | — | ID kho của batch (reference đến ENT_Kho) `FK` |
| 4 | `PhuongPhapTinhGia` | `phuong_phap_tinh_gia` | `text` CHECK | N | — | (BinhQuanCuoiKy \| BinhQuanTucThoi \| FIFO \| DichDanh) |
| 5 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | (ThanhCong \| Loi) |
| 6 | `DonGiaXuatKho` | `don_gia_xuat_kho` | `money_foreign` ≈ | N | `0` | Đơn giá xuất kho của batch |
| 7 | `LoaiLoi` | `loai_loi` | `text` CHECK | Y | — | (VoNghiem \| VoSoNghiem \| MauSoBang0) |
| 8 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải nguyên nhân lỗi |

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

**Đối chiếu `inv_ket_qua_tinh_gia_xuat_kho` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 5 | `luot_tinh_gia_xuat_kho_id`, `phuong_phap_tinh_gia`, `don_gia_xuat_kho`, `loai_loi`, `dien_giai` |
| DB có — LDM **không khai** | 5 | `luot_tinh_gia_id`, `ky`, `thong_bao_loi`, `so_giao_dich`, `phien_ban` |

---

## 22. `inv_ket_qua_tinh_gia_xuat_kho_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietApGiaXuatKho` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `inv_chi_tiet_ap_gia_xuat_kho` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Chi tiết áp giá xuất kho |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_luot_tinh_gia_xuat_kho` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_luot_tinh_gia_xuat_kho` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LuotTinhGiaXuatKhoId` | `luot_tinh_gia_xuat_kho_id` | `uuid` | N | — | ID lượt tính giá (reference đến ENT_LuotTinhGiaXuatKho) `FK` |
| 2 | `LoaiChungTuXuat` | `loai_chung_tu_xuat` | `text` CHECK | N | — | (PhieuXuatKho \| PhieuXuatDieuChuyen \| Khac) |
| 3 | `ChiTietChungTuXuatId` | `chi_tiet_chung_tu_xuat_id` | `uuid` | N | — | ID dòng chi tiết chứng từ xuất |
| 4 | `CostLayerId` | `cost_layer_id` | `uuid` | Y | — | ID cost layer đã tiêu dùng (reference đến ENT_CostLayer). Chỉ PhuongPhapTinhGia = FIFO `FK` |
| 5 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | ID vật tư (reference đến ENT_VatTu) `FK` |
| 6 | `KhoId` | `kho_id` | `uuid` | Y | — | ID kho (reference đến ENT_Kho) `FK` |
| 7 | `SoLuongApGia` | `so_luong_ap_gia` | `quantity` | N | `0` | Số lượng xuất được áp từ layer/batch này (ĐVT chuẩn) |
| 8 | `DonGia` | `don_gia` | `money_foreign` ≈ | N | `0` | Đơn giá áp |
| 9 | `GiaTri` | `gia_tri` | `money_foreign` ≈ | N | `0` | Giá trị xuất = SoLuongApGia × DonGia |

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

**Đối chiếu `inv_chi_tiet_ap_gia_xuat_kho` (31 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 6 | `luot_tinh_gia_xuat_kho_id`, `loai_chung_tu_xuat`, `chi_tiet_chung_tu_xuat_id`, `cost_layer_id`, `so_luong_ap_gia`, `gia_tri` |
| DB có — LDM **không khai** | 18 | `ket_qua_id`, `chung_tu_id`, `chi_tiet_id`, `bang_goc`, `loai_chung_tu`, `chieu`, `so_chung_tu`, `ngay_chung_tu`, `ngay_hach_toan`, `so_luong`, `thanh_tien`, `ton_truoc`, `gia_tri_truoc`, `gia_bq_truoc`, `ton_sau`, `gia_tri_sau`, `gia_bq_sau`, `phien_ban` |

---

## 23. `inv_dinh_muc_nguyen_vat_lieu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `DinhMucNVL` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Định mức nguyên vật liệu |
| Vai trò | Bảng cấu hình / thiết lập |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ. |
| Bảng con | `inv_dinh_muc_nguyen_vat_lieu_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Sản phẩm áp dụng định mức]** ID sản phẩm (reference đến ENT_VatTu) `FK` |
| 2 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Sản phẩm áp dụng định mức]** ID đơn vị tính định mức của sản phẩm (reference đến ENT_DonViTinh) `FK` |
| 3 | `BoPhanId` | `bo_phan_id` | `uuid` | Y | — | **[Sản phẩm áp dụng định mức]** ID bộ phận sử dụng định mức (reference đến ENT_DonVi, LoaiDonVi = PhongBan) `FK` |
| 4 | `NgayApDung` | `ngay_ap_dung` | `date` | Y | — | **[Hiệu lực]** Ngày bắt đầu áp dụng |
| 5 | `NgayHetHieuLuc` | `ngay_het_hieu_luc` | `date` | Y | — | **[Hiệu lực]** Ngày hết hiệu lực |
| 6 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hiệu lực]** Diễn giải định mức |
| 7 | `TrangThai` | `trang_thai` | `text` CHECK | N | — | **[Hiệu lực]** (DangApDung \| NgungApDung) |

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

## 24. `inv_dinh_muc_nguyen_vat_lieu_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietDinhMucNVL` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Chi tiết định mức nguyên vật liệu |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_dinh_muc_nguyen_vat_lieu` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_dinh_muc_nguyen_vat_lieu` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DinhMucNVLId` | `dinh_muc_nvl_id` | `uuid` | N | — | ID định mức (reference đến ENT_DinhMucNVL) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `NguyenVatLieuId` | `nguyen_vat_lieu_id` | `uuid` | N | — | ID nguyên vật liệu (reference đến ENT_VatTu) `FK` |
| 4 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | ID đơn vị tính định mức của NVL (reference đến ENT_DonViTinh) `FK` |
| 5 | `SoLuong` | `so_luong` | `quantity` | N | `0` | Số lượng NVL cần dùng |
| 6 | `TyLeHaoHut` | `ty_le_hao_hut` | `percent_rate` | N | `0` | Tỷ lệ hao hụt dự kiến (%) |
| 7 | `TyLePhanBo` | `ty_le_phan_bo` | `percent_rate` | Y | `0` | Tỷ lệ phân bổ (%) |
| 8 | `GhiChu` | `ghi_chu` | `text` | Y | — | Ghi chú |

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

## 25. `inv_lenh_san_xuat`

| Mục | Nội dung |
|---|---|
| Entity LDM | `LenhSanXuat` |
| Base class | `TenantedEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHÍNH: Lệnh sản xuất |
| Vai trò | Bảng nghiệp vụ |
| Đơn vị 1 dòng | 1 dòng = 1 bản ghi |
| Dùng để làm gì | Bảng dữ liệu nghiệp vụ của phân hệ. |
| Bảng con | `inv_lenh_san_xuat_thanh_pham` · `inv_lenh_san_xuat_nguyen_vat_lieu` · `inv_loai_tru_nguyen_vat_lieu_lenh_san_xuat` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `SoLenhSanXuat` | `so_lenh_san_xuat` | `text` | N | — | **[Thông tin chứng từ]** Số lệnh sản xuất, tự sinh dạng LSX + số thứ tự, cho sửa (duy nhất theo Tenant — BR1) `UNIQUE` |
| 2 | `NgayLenh` | `ngay_lenh` | `date` | N | — | **[Thông tin chứng từ]** Ngày lệnh sản xuất, mặc định ngày hiện tại; là mốc chọn bản định mức còn hiệu lực (BR11) |
| 3 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin chứng từ]** Diễn giải lệnh sản xuất, tối đa 500 ký tự (BR12) |
| 4 | `TinhTrang` | `tinh_trang` | `text` CHECK | N | — | **[Trạng thái & tiến độ]** (ChuaThucHien \| DangThucHien \| TamDung \| HoanThanh \| HuyBo). Mặc định DangThucHien khi tạo mới (BR6) |
| 5 | `DaXuatDuNVL` | `da_xuat_du_nvl` | `boolean` | N | `false` | **[Trạng thái & tiến độ]** Đã xuất đủ NVL; giá trị tính lại theo tiến độ phiếu xuất kho đã ghi sổ, mặc định false (BR7) |
| 6 | `DaNhapDuThanhPham` | `da_nhap_du_thanh_pham` | `boolean` | N | `false` | **[Trạng thái & tiến độ]** Đã nhập đủ thành phẩm; giá trị tính lại theo tiến độ phiếu nhập kho đã ghi sổ, mặc định false (BR7) |

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

## 26. `inv_lenh_san_xuat_thanh_pham`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietLenhSanXuat_ThanhPham` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Dòng thành phẩm của lệnh sản xuất (tab Thành phẩm) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_lenh_san_xuat` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_lenh_san_xuat` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | N | — | ID lệnh sản xuất (reference đến ENT_LenhSanXuat) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `ThanhPhamId` | `thanh_pham_id` | `uuid` | N | — | **[Thành phẩm]** ID thành phẩm cần sản xuất (reference đến ENT_VatTu) `FK` |
| 4 | `TenThanhPham` | `ten_thanh_pham` | `text` | N | — | **[Thành phẩm]** Tên thành phẩm trên dòng lệnh (denormalized) |
| 5 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Đơn vị tính & số lượng]** ID đơn vị tính đã chọn (reference đến ENT_DonViTinh) `FK` |
| 6 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | Y | `0` | **[Đơn vị tính & số lượng]** Hệ số quy đổi về ĐVT chính (reference đến ENT_DonViQuyDoiVatTu); = 1 khi chọn ĐVT chính (BR8) |
| 7 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Đơn vị tính & số lượng]** Số lượng thành phẩm cần sản xuất theo ĐVT đã chọn, phải lớn hơn 0 (BR14) |
| 8 | `SoLuongQuyDoi` | `so_luong_quy_doi` | `quantity` | Y | `0` | **[Đơn vị tính & số lượng]** Số lượng quy đổi về ĐVT chính = SoLuong × HeSoQuyDoi |
| 9 | `SoLuongDaNhap` | `so_luong_da_nhap` | `quantity` | Y | `0` | **[Đơn vị tính & số lượng]** Lũy kế số lượng đã nhập kho (ĐVT chính) từ các phiếu nhập kho đã ghi sổ; hoàn trả khi bỏ ghi sổ / xóa phiếu (BR7) |
| 10 | `NguonId` | `nguon_id` | `uuid` | Y | — | **[loại trừ lẫn nhau ở BR2; dòng nhập tay để trống cả ba trường.]** ID chứng từ nguồn của dòng (đa hình; entity xác định bởi LoaiChungTuNguon) |
| 11 | `LoaiChungTuNguon` | `loai_chung_tu_nguon` | `text` CHECK | Y | — | **[loại trừ lẫn nhau ở BR2; dòng nhập tay để trống cả ba trường.]** (DonDatHang \| HopDongBanHang) |
| 12 | `ChiTietNguonId` | `chi_tiet_nguon_id` | `uuid` | Y | — | **[loại trừ lẫn nhau ở BR2; dòng nhập tay để trống cả ba trường.]** ID dòng chi tiết nguồn (entity theo LoaiChungTuNguon) |
| 13 | `SoChungTuNguon` | `so_chung_tu_nguon` | `text` | Y | — | **[loại trừ lẫn nhau ở BR2; dòng nhập tay để trống cả ba trường.]** Số đơn hàng / số hợp đồng nguồn (denormalized; field màn: Đơn đặt hàng khi DonDatHang, Hợp đồng bán khi HopDongBanHang) |
| 14 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi); chỉ chọn đối tượng có gắn thành phẩm này qua ENT_DoiTuongTapHopChiPhi_VatTu (BR5) `FK` |

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

## 27. `inv_lenh_san_xuat_nguyen_vat_lieu`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietLenhSanXuat_NguyenVatLieu` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY CHI TIẾT: Dòng nguyên vật liệu của lệnh sản xuất (tab Nguyên vật liệu) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_lenh_san_xuat` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_lenh_san_xuat` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | N | — | ID lệnh sản xuất (reference đến ENT_LenhSanXuat) `FK` |
| 2 | `SoThuTu` | `so_thu_tu` | `numeric(18,4)` ⚠ | N | `0` | Số thứ tự dòng (field màn: Stt) |
| 3 | `NguyenVatLieuId` | `nguyen_vat_lieu_id` | `uuid` | N | — | **[Nguyên vật liệu]** ID nguyên vật liệu (reference đến ENT_VatTu) `FK` |
| 4 | `TenNguyenVatLieu` | `ten_nguyen_vat_lieu` | `text` | N | — | **[Nguyên vật liệu]** Tên nguyên vật liệu trên dòng lệnh (denormalized) |
| 5 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Đơn vị tính & số lượng]** ID đơn vị tính đã chọn (reference đến ENT_DonViTinh) `FK` |
| 6 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | Y | `0` | **[Đơn vị tính & số lượng]** Hệ số quy đổi về ĐVT chính (reference đến ENT_DonViQuyDoiVatTu) (BR8) |
| 7 | `SoLuong` | `so_luong` | `quantity` | N | `0` | **[Đơn vị tính & số lượng]** Số lượng NVL theo ĐVT đã chọn, phải lớn hơn 0 (BR14) |
| 8 | `SoLuongQuyDoi` | `so_luong_quy_doi` | `quantity` | Y | `0` | **[Đơn vị tính & số lượng]** Số lượng quy đổi về ĐVT chính = SoLuong × HeSoQuyDoi |
| 9 | `SoLuongDaXuat` | `so_luong_da_xuat` | `quantity` | Y | `0` | **[Đơn vị tính & số lượng]** Lũy kế số lượng đã xuất kho (ĐVT chính) từ các phiếu xuất kho đã ghi sổ; hoàn trả khi bỏ ghi sổ / xóa phiếu (BR7) |
| 10 | `ChiTietLenhSanXuatThanhPhamId` | `chi_tiet_lenh_san_xuat_thanh_pham_id` | `uuid` | Y | — | **[Truy vết nguồn sinh dòng (phục vụ re-fill idempotent — BR4, BR23)]** ID dòng thành phẩm đã sinh ra dòng NVL này (reference đến ENT_ChiTietLenhSanXuat_ThanhPham); NULL với dòng nhập tay `FK` |
| 11 | `DinhMucNVLId` | `dinh_muc_nvl_id` | `uuid` | Y | — | **[Truy vết nguồn sinh dòng (phục vụ re-fill idempotent — BR4, BR23)]** ID bản định mức đã dùng để fill dòng (reference đến ENT_DinhMucNVL); NULL với dòng nhập tay hoặc dòng auto đã bị sửa tay `FK` |
| 12 | `LaDongThuCong` | `la_dong_thu_cong` | `boolean` | N | `false` | **[Truy vết nguồn sinh dòng (phục vụ re-fill idempotent — BR4, BR23)]** Dòng do người dùng thêm/sửa tay; re-fill không đụng tới dòng này, mặc định false (BR4) |
| 13 | `NgoaiDinhMuc` | `ngoai_dinh_muc` | `boolean` | N | `false` | **[Truy vết nguồn sinh dòng (phục vụ re-fill idempotent — BR4, BR23)]** Dòng được giữ lại dù không còn trong định mức mới vì đã phát sinh xuất kho, mặc định false (BR23) |
| 14 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Thống kê dòng]** ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi); mặc định kế thừa từ dòng thành phẩm tương ứng (BR4) `FK` |

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

## 28. `inv_loai_tru_nguyen_vat_lieu_lenh_san_xuat`

| Mục | Nội dung |
|---|---|
| Entity LDM | `LoaiTruNguyenVatLieuLenhSanXuat` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | C — tạo mới |
| Bảng hiện có | *(chưa có)* |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ENTITY: Dấu loại trừ dòng NVL tự động (BR4 — người dùng đã xóa dòng auto, re-fill không sinh lại) |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `inv_lenh_san_xuat` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `inv_lenh_san_xuat` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-03585 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LenhSanXuatId` | `lenh_san_xuat_id` | `uuid` | N | — | ID lệnh sản xuất (reference đến ENT_LenhSanXuat) `FK` |
| 2 | `ChiTietLenhSanXuatThanhPhamId` | `chi_tiet_lenh_san_xuat_thanh_pham_id` | `uuid` | N | — | ID dòng thành phẩm nguồn (reference đến ENT_ChiTietLenhSanXuat_ThanhPham) `FK` |
| 3 | `DinhMucNVLId` | `dinh_muc_nvl_id` | `uuid` | N | — | ID bản định mức nguồn (reference đến ENT_DinhMucNVL) `FK` |
| 4 | `NguyenVatLieuId` | `nguyen_vat_lieu_id` | `uuid` | N | — | ID nguyên vật liệu bị loại trừ (reference đến ENT_VatTu) `FK` |
| 5 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | ID đơn vị tính của dòng bị loại trừ (reference đến ENT_DonViTinh) `FK` |
| 6 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | ID đối tượng tập hợp chi phí của dòng bị loại trừ (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |

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

