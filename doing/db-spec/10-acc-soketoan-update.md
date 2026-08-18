# `acc_` — Sổ kế toán (sổ cái · sổ kho)

> Sinh tự động từ [`ldm-SoKeToan-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-SoKeToan-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**2 bảng.**

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `SoCai` | `acc_so_cai` | `acc_so_cai` | A — có code | Sổ kế toán (append-only) — ChungTuId / ChiTietChungTuId là liên kết đa hình (entity xác định bởi LoaiChungTuId) → không ràng buộc FK ở DB, ứng dụng tự… |
| 2 | `SoKho` | `acc_so_kho` | `acc_so_xuat_nhap_tong_hop` | B — có schema, chưa code | Sổ kế toán (append-only) — SỔ KHO — ghi nhận từng dòng biến động số lượng/giá trị vật tư trong kho. 1 dòng SoKho = 1 dòng chi tiết vật tư trên chứng từ;… |

---

## 1. `acc_so_cai`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoCai` |
| Base class | `TenantedEntity` + `@Immutable` (bảng sổ — append-only, partition theo `ngay_hach_toan`) |
| Nhóm | A — có code |
| Bảng hiện có | `acc_so_cai` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | ChungTuId / ChiTietChungTuId là liên kết đa hình (entity xác định bởi LoaiChungTuId) · → không ràng buộc FK ở DB, ứng dụng tự đảm bảo toàn vẹn. · Chứng từ Số dư đầu kỳ (nhóm SDDK_*) được miễn một số ràng buộc bắt buộc — · quy tắc và danh sách trường nằm trong tài liệu nghiệp vụ của chính epic số dư tương ứng. |
| Vai trò | Sổ kế toán — append-only |
| Đơn vị 1 dòng | 1 dòng = 1 bút toán Nợ/Có |
| Dùng để làm gì | KHÔNG do người dùng nhập. Chỉ kernel ghi sổ được ghi vào, và chỉ khi chứng từ chuyển sang `DA_GHI_SO`. Bảng bất biến (`@Immutable`) + partition theo `ngay_hach_toan`. Là **nguồn duy nhất** cho mọi sổ sách, báo cáo và tra cứu số dư. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChiNhanhId` | `chi_nhanh_id` | `uuid` | N | — | **[Phạm vi đơn vị]** ID định danh chi nhánh (reference đến ENT_DonVi, đơn vị loại ChiNhanh) `FK` |
| 2 | `ChiNhanhDoiUngId` | `chi_nhanh_doi_ung_id` | `uuid` | Y | — | **[Phạm vi đơn vị]** Chi nhánh đối ứng, chỉ có giá trị khi là giao dịch nội bộ (TK 136/336). Tạm thời để trống, sau dùng cho giao dịch giữa các chi nhánh (reference đến ENT_DonVi) `FK` |
| 3 | `LoaiChungTuId` | `loai_chung_tu_id` | `uuid` | N | — | **[Liên kết chứng từ gốc (đa hình)]** ID loại chứng từ (reference đến ENT_LoaiChungTu) `FK` |
| 4 | `ChungTuId` | `chung_tu_id` | `uuid` | N | — | **[Liên kết chứng từ gốc (đa hình)]** ID chứng từ gốc (header) sinh ra bút toán này; entity xác định bởi LoaiChungTuId |
| 5 | `ChiTietChungTuId` | `chi_tiet_chung_tu_id` | `uuid` | N | — | **[Liên kết chứng từ gốc (đa hình)]** ID dòng chi tiết chứng từ gốc; entity chi tiết tương ứng LoaiChungTuId |
| 6 | `STTDongChiTiet` | `stt_dong_chi_tiet` | `integer` | N | `0` | **[Liên kết chứng từ gốc (đa hình)]** Số thứ tự dòng chi tiết trong phiếu |
| 7 | `STTButToan` | `stt_but_toan` | `integer` | N | `0` | **[Liên kết chứng từ gốc (đa hình)]** Số thứ tự bút toán trong cùng 1 dòng hạch toán (1 dòng chi tiết có thể sinh nhiều bút toán: giá vốn, doanh thu, thuế...) |
| 8 | `SoChungTu` | `so_chung_tu` | `varchar(50)` | N | — | **[Thông tin chứng từ (denormalized từ master)]** Số chứng từ |
| 9 | `NgayChungTu` | `ngay_chung_tu` | `date` | N | — | **[Thông tin chứng từ (denormalized từ master)]** Ngày chứng từ |
| 10 | `NgayHachToan` | `ngay_hach_toan` | `timestamptz` | N | — | **[Thông tin chứng từ (denormalized từ master)]** Ngày ghi sổ, có thể khác ngày chứng từ |
| 11 | `VatTuId` | `vat_tu_id` | `uuid` | Y | — | **[Thông tin vật tư]** ID vật tư/hàng hóa (reference đến ENT_VatTu) `FK` |
| 12 | `TenVatTu` | `ten_vat_tu` | `text` | Y | — | **[Thông tin vật tư]** Tên vật tư/hàng hóa (snapshot theo VatTuId) |
| 13 | `TKId` | `tk_id` | `uuid` | N | — | **[Tài khoản hạch toán]** ID tài khoản hạch toán (reference đến ENT_HeThongTaiKhoan) `FK` |
| 14 | `TKDoiUngId` | `tk_doi_ung_id` | `uuid` | N | — | **[Tài khoản hạch toán]** ID tài khoản đối ứng (reference đến ENT_HeThongTaiKhoan) `FK` |
| 15 | `TK` | `tk` | `text` | N | — | **[Tài khoản hạch toán]** Mã tài khoản, lấy theo TKId (ngoại lệ Rule 2 — có lưu mã) |
| 16 | `TKDoiUng` | `tk_doi_ung` | `text` | N | — | **[Tài khoản hạch toán]** Mã tài khoản đối ứng, lấy theo TKDoiUngId (ngoại lệ Rule 2 — có lưu mã) |
| 17 | `PSNo` | `ps_no` | `money_foreign` ≈ | N | `0` | **[Số tiền phát sinh]** Phát sinh nợ theo NGUYÊN TỆ (đồng tiền giao dịch trên chứng từ). Có giá trị ở dòng vế Nợ, = 0 ở dòng vế Có |
| 18 | `PSNoQuyDoi` | `ps_no_quy_doi` | `money_vnd` | N | `0` | **[Số tiền phát sinh]** Phát sinh nợ quy đổi về đồng tiền hạch toán = PSNo × TyGia |
| 19 | `PSCo` | `ps_co` | `money_foreign` ≈ | N | `0` | **[Số tiền phát sinh]** Phát sinh có theo NGUYÊN TỆ. Có giá trị ở dòng vế Có, = 0 ở dòng vế Nợ |
| 20 | `PSCoQuyDoi` | `ps_co_quy_doi` | `money_vnd` | N | `0` | **[Số tiền phát sinh]** Phát sinh có quy đổi về đồng tiền hạch toán = PSCo × TyGia |
| 21 | `TienTeHachToanId` | `tien_te_hach_toan_id` | `uuid` | N | — | **[Tiền tệ & tỷ giá]** ID loại tiền hạch toán (reference đến ENT_LoaiTien) `FK` |
| 22 | `TienTeHachToan` | `tien_te_hach_toan` | `text` | N | — | **[Tiền tệ & tỷ giá]** Tên tiền tệ hạch toán (snapshot theo TienTeHachToanId) |
| 23 | `TyGia` | `ty_gia` | `exchange_rate` | N | `1` | **[Tiền tệ & tỷ giá]** Tỷ giá quy đổi từ nguyên tệ về đồng tiền hạch toán; bằng 1 khi giao dịch cùng đồng tiền hạch toán |
| 24 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Diễn giải]** Diễn giải lấy từ chứng từ master |
| 25 | `DienGiaiDong` | `dien_giai_dong` | `text` | Y | — | **[Diễn giải]** Diễn giải lấy từ dòng chi tiết chứng từ |
| 26 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID vụ việc (reference đến ENT_CongTrinh) `FK` |
| 27 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID đơn vị (reference đến ENT_DonVi) `FK` |
| 28 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 29 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID khách hàng/nhà cung cấp/nhân viên, có giá trị khi hạch toán công nợ (reference đến ENT_DoiTuong) `FK` |
| 30 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** Tên đối tượng (snapshot theo DoiTuongId) |
| 31 | `TKNganHangId` | `tk_ngan_hang_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID tài khoản ngân hàng, có giá trị khi bút toán gắn với một tài khoản ngân hàng cụ thể (tiền gửi, báo có/báo nợ, séc, số dư đầu kỳ TK ngân hàng) — reference đến ENT_TaiKhoanNganHang `FK` |
| 32 | `KheUocId` | `khe_uoc_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID khế ước đi vay, có giá trị khi bút toán gắn với một khế ước (Phiếu KTTH Loại 7 "Vay ngân hàng chuyển trả cho NCC" — BR22 tại epic PMKT-E-09980); sổ chi tiết khoản vay dùng trường này để theo dõi dư nợ theo từng khế ước — reference đến ENT_KheUoc `FK` |
| 33 | `DonHangId` | `don_hang_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID đơn hàng (reference đến ENT_DonDatHang) `FK` |
| 34 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID hợp đồng (reference đến ENT_HopDong) `FK` |
| 35 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID khoản mục chi phí/thu nhập (reference đến ENT_KhoanMucChiPhi) `FK` |
| 36 | `IsAuto` | `is_auto` | `boolean` | N | `false` | **[Nguồn gốc & vết ghi sổ]** Bút toán sinh tự động hay không (mặc định 0 — do người dùng lập) |
| 37 | `NguoiGhiSoId` | `nguoi_ghi_so_id` | `uuid` | Y | — | **[Nguồn gốc & vết ghi sổ]** Người ghi sổ, bắt buộc khi đã ghi sổ (reference đến ENT_NguoiDung) `FK` |
| 38 | `ThoiGianGhiSo` | `thoi_gian_ghi_so` | `timestamptz` | Y | — | **[Nguồn gốc & vết ghi sổ]** Thời điểm ghi sổ, bắt buộc khi đã ghi sổ |

**Trường base — `TenantedEntity` + `@Immutable` (bảng sổ — append-only, partition theo `ngay_hach_toan`)** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. Bảng partition ⇒ PK là `(id, ngay_hach_toan)`. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu dòng sổ. Khóa RLS. `TenantedEntity` · BR46.4 |
| `request_hash` | `varchar(64)` | N | — | Vân tay nội dung của lần ghi sổ — nền tảng **idempotency**. UNIQUE trên cột trần (bảng partition không nhận unique index dạng biểu thức/partial). *(không có trong LDM — hạ tầng bắt buộc)* |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo dòng sổ (LDM: `ThoiGianTao`). `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | N | — | Người tạo dòng sổ (LDM: `NguoiTaoId`). `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `acc_so_cai` (38 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 29 | `chi_nhanh_id`, `stt_dong_chi_tiet`, `stt_but_toan`, `vat_tu_id`, `ten_vat_tu`, `tk_id`, `tk_doi_ung_id`, `tk`, `tk_doi_ung`, `ps_no`, `ps_no_quy_doi`, `ps_co`, `ps_co_quy_doi`, `tien_te_hach_toan_id`, `tien_te_hach_toan`, `dien_giai_dong`, `vu_viec_id`, `don_vi_id`, `doi_tuong_tap_hop_chi_phi_id`, `doi_tuong_id`, `ten_doi_tuong`, `tk_ngan_hang_id`, `khe_uoc_id`, `don_hang_id`, `hop_dong_id`, `khoan_muc_chi_phi_id`, `is_auto`, `nguoi_ghi_so_id`, `thoi_gian_ghi_so` |
| DB có — LDM **không khai** | 26 | `tai_khoan_id`, `tai_khoan_doi_ung_id`, `loai_tien_id`, `so_tien_phat_sinh_no_ngoai_te`, `so_tien_phat_sinh_no`, `so_tien_phat_sinh_co_ngoai_te`, `so_tien_phat_sinh_co`, `ma_vu_viec_id`, `ma_don_vi_id`, `ma_doi_tuong_id`, `loai_doi_tuong`, `ma_hop_dong_id`, `ma_khoan_muc_chi_phi_id`, `ma_doi_tuong_tap_hop_chi_phi_id`, `la_noi_bo`, `internal_transaction_id`, `reversal_of_id`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `deleted_at`, `da_dao`, `dao_luc` |

---

## 2. `acc_so_kho`

| Mục | Nội dung |
|---|---|
| Entity LDM | `SoKho` |
| Base class | `TenantedEntity` + `@Immutable` (bảng sổ — append-only, partition theo `ngay_hach_toan`) |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `acc_so_xuat_nhap_tong_hop` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | SỔ KHO — ghi nhận từng dòng biến động số lượng/giá trị vật tư trong kho. · 1 dòng SoKho = 1 dòng chi tiết vật tư trên chứng từ; thông tin master lặp lại. · Cột ...Chinh = giá trị đã quy về ĐVT chính của vật tư, dùng thống nhất khi tính tồn kho. |
| Vai trò | Sổ kế toán — append-only |
| Đơn vị 1 dòng | 1 dòng = 1 dòng biến động kho |
| Dùng để làm gì | KHÔNG do người dùng nhập. Chỉ kernel ghi sổ được ghi vào, và chỉ khi chứng từ chuyển sang `DA_GHI_SO`. Bảng bất biến (`@Immutable`) + partition theo `ngay_hach_toan`. Là **nguồn duy nhất** cho mọi sổ sách, báo cáo và tra cứu số dư. |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChiNhanhId` | `chi_nhanh_id` | `uuid` | N | — | **[Phạm vi đơn vị]** ID định danh chi nhánh (reference đến ENT_DonVi, đơn vị loại ChiNhanh) `FK` |
| 2 | `ChiNhanhDoiUngId` | `chi_nhanh_doi_ung_id` | `uuid` | Y | — | **[Phạm vi đơn vị]** Chi nhánh đối ứng, chỉ có giá trị khi chuyển kho liên chi nhánh (reference đến ENT_DonVi) `FK` |
| 3 | `LoaiChungTuId` | `loai_chung_tu_id` | `uuid` | N | — | **[Liên kết chứng từ gốc (đa hình)]** ID loại chứng từ (reference đến ENT_LoaiChungTu) `FK` |
| 4 | `ChungTuId` | `chung_tu_id` | `uuid` | N | — | **[Liên kết chứng từ gốc (đa hình)]** ID chứng từ gốc (header) sinh ra dòng này; entity xác định bởi LoaiChungTuId |
| 5 | `ChiTietChungTuId` | `chi_tiet_chung_tu_id` | `uuid` | N | — | **[Liên kết chứng từ gốc (đa hình)]** ID dòng chi tiết chứng từ gốc; entity chi tiết tương ứng LoaiChungTuId |
| 6 | `STTDongChiTiet` | `stt_dong_chi_tiet` | `integer` | N | `0` | **[Liên kết chứng từ gốc (đa hình)]** Số thứ tự dòng chi tiết trong phiếu |
| 7 | `SoChungTu` | `so_chung_tu` | `varchar(50)` | N | — | **[Thông tin chứng từ (denormalized từ master)]** Số chứng từ |
| 8 | `NgayChungTu` | `ngay_chung_tu` | `date` | N | — | **[Thông tin chứng từ (denormalized từ master)]** Ngày chứng từ |
| 9 | `NgayHachToan` | `ngay_hach_toan` | `timestamptz` | N | — | **[Thông tin chứng từ (denormalized từ master)]** Ngày ghi nhận biến động kho, có thể khác ngày chứng từ |
| 10 | `LoaiNhapXuat` | `loai_nhap_xuat` | `text` CHECK | N | — | **[Kho & vật tư]** Chiều biến động kho (0 = Nhập \| 1 = Xuất) |
| 11 | `KhoId` | `kho_id` | `uuid` | N | — | **[Kho & vật tư]** ID kho phát sinh giao dịch (reference đến ENT_Kho) `FK` |
| 12 | `VatTuId` | `vat_tu_id` | `uuid` | N | — | **[Kho & vật tư]** ID vật tư/hàng hóa (reference đến ENT_VatTu) `FK` |
| 13 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Kho & vật tư]** Tên vật tư/hàng hóa (snapshot theo VatTuId) |
| 14 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | N | — | **[Đơn vị tính & quy đổi]** ID đơn vị tính lúc nhập liệu chứng từ (reference đến ENT_DonViTinh) `FK` |
| 15 | `DonViTinhChinhId` | `don_vi_tinh_chinh_id` | `uuid` | N | — | **[Đơn vị tính & quy đổi]** ID đơn vị tính chính của vật tư (reference đến ENT_DonViTinh, lấy theo ENT_VatTu) `FK` |
| 16 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | N | `0` | **[Đơn vị tính & quy đổi]** Hệ số quy đổi từ ĐVT nhập liệu ra ĐVT chính của vật tư (reference đến ENT_DonViQuyDoiVatTu) |
| 17 | `SoLuongNhap` | `so_luong_nhap` | `quantity` | N | `0` | **[Số lượng]** Số lượng nhập theo ĐVT nhập liệu |
| 18 | `SoLuongNhapChinh` | `so_luong_nhap_chinh` | `quantity` | N | `0` | **[Số lượng]** Số lượng nhập quy về ĐVT chính = SoLuongNhap × HeSoQuyDoi, dùng thống nhất khi tính tồn kho |
| 19 | `SoLuongXuat` | `so_luong_xuat` | `quantity` | N | `0` | **[Số lượng]** Số lượng xuất theo ĐVT nhập liệu |
| 20 | `SoLuongXuatChinh` | `so_luong_xuat_chinh` | `quantity` | N | `0` | **[Số lượng]** Số lượng xuất quy về ĐVT chính = SoLuongXuat × HeSoQuyDoi, dùng thống nhất khi tính tồn kho |
| 21 | `DonGiaNhapQuyDoi` | `don_gia_nhap_quy_doi` | `money_vnd` | N | `0` | **[Đơn giá & thành tiền (đã quy đổi về đồng tiền hạch toán)]** Đơn giá nhập theo ĐVT nhập liệu |
| 22 | `DonGiaNhapQuyDoiChinh` | `don_gia_nhap_quy_doi_chinh` | `money_foreign` ≈ | N | `0` | **[Đơn giá & thành tiền (đã quy đổi về đồng tiền hạch toán)]** Đơn giá nhập theo ĐVT chính = DonGiaNhapQuyDoi ÷ HeSoQuyDoi |
| 23 | `DonGiaXuatQuyDoi` | `don_gia_xuat_quy_doi` | `money_vnd` | N | `0` | **[Đơn giá & thành tiền (đã quy đổi về đồng tiền hạch toán)]** Đơn giá xuất (giá vốn) theo ĐVT nhập liệu |
| 24 | `DonGiaXuatQuyDoiChinh` | `don_gia_xuat_quy_doi_chinh` | `money_foreign` ≈ | N | `0` | **[Đơn giá & thành tiền (đã quy đổi về đồng tiền hạch toán)]** Đơn giá xuất theo ĐVT chính = DonGiaXuatQuyDoi ÷ HeSoQuyDoi |
| 25 | `ThanhTienNhapQuyDoi` | `thanh_tien_nhap_quy_doi` | `money_vnd` | N | `0` | **[Đơn giá & thành tiền (đã quy đổi về đồng tiền hạch toán)]** Thành tiền nhập = SoLuongNhap × DonGiaNhapQuyDoi |
| 26 | `ThanhTienXuatQuyDoi` | `thanh_tien_xuat_quy_doi` | `money_vnd` | N | `0` | **[Đơn giá & thành tiền (đã quy đổi về đồng tiền hạch toán)]** Thành tiền xuất = SoLuongXuat × DonGiaXuatQuyDoi, cũng là giá trị vốn xuất kho |
| 27 | `TuNhapDonGia` | `tu_nhap_don_gia` | `boolean` | Y | `false` | **[Cách lấy giá trên dòng chứng từ gốc]** Người dùng tự nhập giá vốn khi xuất |
| 28 | `TuDongApGia` | `tu_dong_ap_gia` | `boolean` | Y | `false` | **[Cách lấy giá trên dòng chứng từ gốc]** Lấy giá nhập theo giá trung bình |
| 29 | `TienTeHachToanId` | `tien_te_hach_toan_id` | `uuid` | N | — | **[Tiền tệ]** ID loại tiền hạch toán, áp dụng hàng nhập khẩu (reference đến ENT_LoaiTien) `FK` |
| 30 | `TyGia` | `ty_gia` | `exchange_rate` | N | `1` | **[Tiền tệ]** Tỷ giá quy đổi về đồng tiền hạch toán; bằng 1 khi giao dịch cùng đồng tiền hạch toán. Cần để truy ngược giá trị nguyên tệ từ các cột đã quy đổi |
| 31 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Tiền tệ]** Diễn giải |
| 32 | `ChiPhiPhanBoQuyDoi` | `chi_phi_phan_bo_quy_doi` | `money_vnd` | N | `0` | **[Cấu phần giá nhập bổ sung (chỉ hàng nhập khẩu / có phân bổ chi phí)]** Chi phí mua hàng phân bổ cho dòng, đã quy đổi |
| 33 | `ThueNhapKhauQuyDoi` | `thue_nhap_khau_quy_doi` | `money_vnd` | N | `0` | **[Cấu phần giá nhập bổ sung (chỉ hàng nhập khẩu / có phân bổ chi phí)]** Thuế nhập khẩu tính vào giá nhập, đã quy đổi |
| 34 | `ThueBVMTQuyDoi` | `thue_bvmt_quy_doi` | `money_vnd` | N | `0` | **[Cấu phần giá nhập bổ sung (chỉ hàng nhập khẩu / có phân bổ chi phí)]** Thuế bảo vệ môi trường tính vào giá nhập, đã quy đổi |
| 35 | `ThueTTDBQuyDoi` | `thue_ttdb_quy_doi` | `money_vnd` | N | `0` | **[Cấu phần giá nhập bổ sung (chỉ hàng nhập khẩu / có phân bổ chi phí)]** Thuế tiêu thụ đặc biệt tính vào giá nhập, đã quy đổi |
| 36 | `ThueCBPGQuyDoi` | `thue_cbpg_quy_doi` | `money_vnd` | N | `0` | **[Cấu phần giá nhập bổ sung (chỉ hàng nhập khẩu / có phân bổ chi phí)]** Thuế chống bán phá giá tính vào giá nhập, đã quy đổi; bút toán thuế CBPG ghi Nợ vào TK kho nên cũng cấu thành giá nhập |
| 37 | `TKVatTuId` | `tk_vat_tu_id` | `uuid` | N | — | **[Tài khoản kế toán]** ID tài khoản vật tư (reference đến ENT_HeThongTaiKhoan) `FK` |
| 38 | `TKGiaVonId` | `tk_gia_von_id` | `uuid` | N | — | **[Tài khoản kế toán]** ID tài khoản giá vốn (reference đến ENT_HeThongTaiKhoan) `FK` |
| 39 | `TKVatTu` | `tk_vat_tu` | `text` | N | — | **[Tài khoản kế toán]** Mã tài khoản vật tư, lấy theo TKVatTuId (ngoại lệ Rule 2 — có lưu mã) |
| 40 | `TKGiaVon` | `tk_gia_von` | `text` | N | — | **[Tài khoản kế toán]** Mã tài khoản giá vốn, lấy theo TKGiaVonId (ngoại lệ Rule 2 — có lưu mã) |
| 41 | `DoiTuongId` | `doi_tuong_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID khách hàng/nhà cung cấp liên quan, có giá trị khi nhập mua hoặc xuất bán (reference đến ENT_DoiTuong) `FK` |
| 42 | `TenDoiTuong` | `ten_doi_tuong` | `text` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** Tên đối tượng (snapshot theo DoiTuongId) |
| 43 | `VuViecId` | `vu_viec_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID vụ việc/dự án (reference đến ENT_CongTrinh) `FK` |
| 44 | `DonViId` | `don_vi_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID bộ phận (reference đến ENT_DonVi) `FK` |
| 45 | `DoiTuongTapHopChiPhiId` | `doi_tuong_tap_hop_chi_phi_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID đối tượng tập hợp chi phí (reference đến ENT_DoiTuongTapHopChiPhi) `FK` |
| 46 | `DonHangId` | `don_hang_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID đơn hàng (reference đến ENT_DonDatHang) `FK` |
| 47 | `HopDongId` | `hop_dong_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID hợp đồng (reference đến ENT_HopDong) `FK` |
| 48 | `KhoanMucChiPhiId` | `khoan_muc_chi_phi_id` | `uuid` | Y | — | **[Đối tượng thống kê kèm theo (nullable)]** ID khoản mục chi phí, có giá trị khi xuất dùng nội bộ (reference đến ENT_KhoanMucChiPhi) `FK` |
| 49 | `IsAuto` | `is_auto` | `boolean` | N | `false` | **[Nguồn gốc & vết ghi sổ]** Dòng sinh tự động hay không (mặc định 0 — do người dùng lập) |
| 50 | `NguoiGhiSoId` | `nguoi_ghi_so_id` | `uuid` | Y | — | **[Nguồn gốc & vết ghi sổ]** Người ghi sổ, bắt buộc khi đã ghi sổ (reference đến ENT_NguoiDung) `FK` |
| 51 | `ThoiGianGhiSo` | `thoi_gian_ghi_so` | `timestamptz` | Y | — | **[Nguồn gốc & vết ghi sổ]** Thời điểm ghi sổ, bắt buộc khi đã ghi sổ |

**Trường base — `TenantedEntity` + `@Immutable` (bảng sổ — append-only, partition theo `ngay_hach_toan`)** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. Bảng partition ⇒ PK là `(id, ngay_hach_toan)`. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu dòng sổ. Khóa RLS. `TenantedEntity` · BR46.4 |
| `request_hash` | `varchar(64)` | N | — | Vân tay nội dung của lần ghi sổ — nền tảng **idempotency**. UNIQUE trên cột trần (bảng partition không nhận unique index dạng biểu thức/partial). *(không có trong LDM — hạ tầng bắt buộc)* |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo dòng sổ (LDM: `ThoiGianTao`). `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | N | — | Người tạo dòng sổ (LDM: `NguoiTaoId`). `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `acc_so_xuat_nhap_tong_hop` (81 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 36 | `chi_nhanh_id`, `chi_nhanh_doi_ung_id`, `stt_dong_chi_tiet`, `loai_nhap_xuat`, `kho_id`, `ten_vat_tu`, `don_vi_tinh_id`, `don_vi_tinh_chinh_id`, `so_luong_nhap_chinh`, `so_luong_xuat_chinh`, `don_gia_nhap_quy_doi_chinh`, `don_gia_xuat_quy_doi_chinh`, `thanh_tien_nhap_quy_doi`, `thanh_tien_xuat_quy_doi`, `tu_nhap_don_gia`, `tu_dong_ap_gia`, `tien_te_hach_toan_id`, `chi_phi_phan_bo_quy_doi`, `thue_nhap_khau_quy_doi`, `thue_bvmt_quy_doi`, `thue_ttdb_quy_doi`, `thue_cbpg_quy_doi`, `tk_vat_tu_id`, `tk_gia_von_id`, `tk_vat_tu`, `tk_gia_von`, `doi_tuong_id`, `ten_doi_tuong`, `vu_viec_id`, `don_vi_id`, `doi_tuong_tap_hop_chi_phi_id`, `don_hang_id`, `khoan_muc_chi_phi_id`, `is_auto`, `nguoi_ghi_so_id`, `thoi_gian_ghi_so` |
| DB có — LDM **không khai** | 59 | `kieu_nhap_xuat`, `ma_kho_nhap_id`, `ma_khu_vuc_kho_nhap_id`, `ma_kho_xuat_id`, `ma_khu_vuc_kho_xuat_id`, `ma_vat_tu`, `don_vi_tinh`, `don_vi_tinh_chuan`, `so_lo`, `han_su_dung`, `so_luong_nhap_quy_doi`, `so_luong_xuat_quy_doi`, `loai_tien_id`, `don_gia_mua_ngoai_te`, `thanh_tien_mua_ngoai_te`, `don_gia_mua`, `thanh_tien_mua`, `don_gia_nhap_ngoai_te`, `thanh_tien_nhap_ngoai_te`, `don_gia_nhap`, `thanh_tien_nhap`, `don_gia_nhap_ngoai_te_quy_doi`, `chi_phi_phan_bo_ngoai_te`, `chi_phi_phan_bo`, `don_gia_ban_ngoai_te`, `thanh_tien_ban_ngoai_te`, `don_gia_ban_ngoai_te_quy_doi`, `don_gia_ban`, `thanh_tien_ban`, `don_gia_ban_quy_doi`, `don_gia_xuat`, `thanh_tien_xuat`, `gia_dich_danh`, `thue_suat_gtgt_id`, `tien_thue_suat_gtgt`, `tien_thue_nhap_khau`, `tien_thue_gtgt_xuat_khau`, `thue_tieu_thu_dac_biet_id`, `tien_thue_tieu_thu_dac_biet`, `tien_thue_bvmt`, `tien_thue_gtgt`, `tai_khoan_vat_tu_id`, `tai_khoan_gia_von_id`, `tai_khoan_doi_ung_id`, `tai_khoan_doanh_thu_id`, `ma_vu_viec_id`, `ma_don_vi_id`, `ma_khe_uoc_id`, `nhan_vien_ban_hang_id`, `ma_doi_tuong_id`, `loai_doi_tuong`, `ma_nha_cung_cap_id`, `ma_nhan_vien_id`, `lenh_san_xuat_id`, `ma_khoan_muc_chi_phi_id`, `ma_doi_tuong_tap_hop_chi_phi_id`, `phien_ban`, `ngay_cap_nhat`, `nguoi_cap_nhat` |

