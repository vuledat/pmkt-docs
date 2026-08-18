# PMKT-E-06194 — Chứng từ bán hàng (API) — Kế hoạch tổng

> **Trạng thái:** `ĐÃ CODE (xem IMPLEMENT.md) — ĐÃ ĐỐI CHIẾU LẠI TÀI LIỆU 2026-08-18, CÒN 12 KHOẢNG CÁCH Ở §17`
> **Ngày lập:** 2026-08-15 · **Người lập:** AI (skill `/plan-be`)
> **Thay thế** bản plan cũ (khảo sát 2026-08-07, đối chiếu code 2026-08-10) — bản cũ đã lệch tài liệu,
> lý do ghi ở [§0.1](#01-vì-sao-phải-viết-lại-thay-vì-cập-nhật).

| Hạng mục | Giá trị |
|---|---|
| Tài liệu nguồn | `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/` @ commit `1a928c53b` (2026-08-13 09:23) + `pmkt-docs/ba/Common/business_rules.md` @ `de31106d2` (2026-08-12 15:03) |
| UC trong phạm vi | PMKT-U-06396 · 06397–06399 · 06400–06402 · 06403–06405 · 06406–06408 · 06430 · 06431 · 06461 · 06966 · 06982–06985 |
| Màn hình nguồn | `SCR_CTBH_DanhSach` · `SCR_CTBH_ThemMoi` · `SCR_CTBH_CapNhat` · `SCR_CTBH_XemChiTiet` · `SCR_CTBH_PopupXacNhanXoa` · `SCR_CTBH_PBCK` · `SCR_CTBH_PBCK_MHHD` |
| Module BE | `cell/chung_tu_ban_hang/` (Modulith, đã tồn tại) |
| Bảng DB | `sal_chung_tu_ban_hang` (87 cột) · `sal_chung_tu_ban_hang_chi_tiet` |
| Code base @ | nhánh `feat/chung-tu-ban-hang-2`, commit `4f350a1e` (2026-08-16 13:15), base package **`vn.vtt.pmkt`** — xem [§2.0](#20-mốc-đối-chiếu-code) |
| Đối chiếu lại | **2026-08-16** — tài liệu BA không đổi; code đổi lớn, chi tiết [§2.0](#20-mốc-đối-chiếu-code) |
| Đối chiếu lại (2) | **2026-08-18** — tài liệu BA đổi 3 commit (BR20 viết lại, bỏ lọc trạng thái danh mục, đổi tên entity); code đã merge. Bảng khoảng cách: [§17](#17-đối-chiếu-tài-liệu--code-2026-08-18) |

---

## 0. Quyết định đã chốt

### 0.1. Vì sao phải viết lại thay vì cập nhật

Bản plan cũ khảo sát ngày 07–10/08. Sau đó PYC bị **viết lại lớn**:

| Commit | Ngày | Nội dung chạm 06194 |
|---|---|---|
| `289d5079d` | 12/08 17:53 | `SCR_CTBH_ThemMoi.md` **+1031/−638 dòng**; `SCR_CTBH_DanhSach.md` +81/−51; 7 UC + 4 Matrix sửa theo |
| `1a928c53b` | 13/08 09:23 | Cập nhật link Figma + cách ghi công thức dòng tổng cộng |

`SCR_CTBH_DanhSach.md` còn **đổi cấu trúc bảng đặc tả**: bỏ các cột `Field` / `Max length` / `Bắt buộc` /
`Giá trị mặc định`, chỉ còn `Control` + `Tham chiếu`. Mọi trích dẫn field-level của plan cũ trỏ vào
bảng **không còn tồn tại** → sửa từng dòng tốn hơn viết lại.

### 0.2. Bảng quyết định

| # | Quyết định | Hệ quả lên code | Vì sao KHÔNG chọn phương án kia |
|---|---|---|---|
| **D1** | **GỘP một bảng** — `sal_chung_tu_ban_hang` là bảng sống sót, đóng vai `ENT_ChungTuBan`; `sal_chung_tu_ban_dich_vu` + `sal_chi_tiet_chung_tu_ban_dv` được **di trú dữ liệu rồi DROP**. Phân biệt hai loại bằng `loai_nghiep_vu`. *(BA chốt 2026-08-16 — [Q1](#q1--ent_chungtuban-một-bảng-hay-hai))* | `LoaiNghiepVuBanHang` thêm giá trị **`DICH_VU("Bán dịch vụ")`** (hiện chỉ có `TRONG_NUOC` · `XUAT_KHAU` — [LoaiNghiepVuBanHang.java:12-13](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/model/LoaiNghiepVuBanHang.java)); sửa `CHECK` constraint của cột; module `chung_tu_ban_hang/` sở hữu cả hai nghiệp vụ; **một** endpoint `search` phục vụ cả màn dùng chung. | Giữ 2 bảng thì màn danh sách phải `UNION` hai cấu trúc lệch nhau, và mọi báo cáo/đối trừ/counter sau này đều phải viết hai nhánh. **Chi phí gộp thấp hơn ước tính ban đầu**: chưa có module Java nào cho CTBDV (`grep -rl "BanDichVu" src/main/java` chỉ ra 1 hằng mã quyền ở `common/constant/MaChucNang.java`), và bảng DV chỉ có **30 bản ghi seed** trên DB dev — không phải dữ liệu thật. |
| **D2** | Phần **ĐỌC** (search · `/cot` · chi tiết · export) tiếp tục dùng nguyên `core.controller.BaseCrudController` ([BaseCrudController.java:121-198](../../cell-app/src/main/java/vn/vtt/pmkt/cell/core/controller/BaseCrudController.java)); phần **GHI** đi qua `accounting_core.chung_tu.service.ChungTuTemplate` ([ChungTuTemplate.java:70](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)). | Không viết lại khung; chỉ cài 5 hook trừu tượng `kiemTraNghiepVu` / `luuEntity` / `taoKetQua` / `bangGoc` / `maLoaiChungTu` ([ChungTuTemplate.java:248-272](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)). | Tự viết CRUD = mất `DynamicSpecification`, `PageResponse`, whitelist `@Searchable`, và mất bất biến "gỡ bút toán cũ → lưu → sinh bút toán mới" của template. |
| **D3** | Ghi sổ / bỏ ghi sổ **chỉ** qua `accounting_core.hach_toan.api.GhiSoApi` ([GhiSoApi.java:16-51](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/GhiSoApi.java)). | `ghiSo()` idempotent theo nội dung, `boGhiSo()` **xoá vật lý** dòng sổ cái (chốt tại V56, không sinh bút toán đảo) — khớp BR21 mục 3 "xóa toàn bộ định khoản đã sinh". | Tự insert `acc_so_cai` là vi phạm luật cứng của repo (`GhiSoApi` là nơi DUY NHẤT được insert). |
| **D4** | **Sổ kho do chính chứng từ bán ghi** khi `KiemPhieuXuatKho = True` (BR20 mục Sổ kho), ghi vào `acc_so_kho` — bảng **đã tồn tại** trong `V1__create_database.sql`. | Cần một port ghi sổ kho tương tự `GhiSoApi`; nếu chưa có thì đây là hạng mục mới của epic. | Sinh bản ghi `ENT_PhieuXuatKho` là **sai BR18**: BA nói rõ "KHÔNG sinh bản ghi". |
| **D5** | **BR16 (Định khoản ngầm định) tách khỏi phạm vi đợt này** — tài khoản lấy theo ưu tiên 1 của BR16 mục 3 (danh mục vật tư / khách hàng), không có thì **để trống kèm comment `// BR16 — chờ ENT_TaiKhoanNgamDinh, xem plan §12-Q2`** tại đúng chỗ sẽ tra định khoản. *(BA chốt 2026-08-16 — [Q2](#q2--định-khoản-ngầm-định-br16-chưa-có-bảng))* | Cột TK trên dòng nhận giá trị người dùng gửi lên; không tra `ChiTietTaiKhoanNgamDinh`; không validate `MSG_PMKT-E-06194_107`. | Hai bảng `tai_khoan_ngam_dinh` / `chi_tiet_tai_khoan_ngam_dinh` **không tồn tại** (§2.2) — code BR16 lúc này là code chống lại một danh mục chưa có. Comment tại chỗ để lần sau grep ra ngay, thay vì chỉ ghi trong plan rồi quên. |
| **D9** | **Nguồn khách hàng giữ `mst_khach_hang_to_chuc` / `mst_khach_hang_ca_nhan`**, KHÔNG chờ `ENT_DoiTuong` + `DoiTuong_VaiTro` của BR01. *(BA chốt 2026-08-16 — [Q3](#q3--nguồn-khách-hàng-ent_doituong-hay-mst_khach_hang_))* | Auto-fill BR01 mục 2 ánh xạ sang cột tương ứng của `mst_khach_hang_*`; trường nào mô hình cũ không có (`DoiTuong_VaiTro.TaiKhoanCongNoPhaiThuId`, `.SoNgayDuocNo`, `.LoaiTienId`) thì để trống, người dùng tự chọn. | Chờ danh mục Đối tượng mới = chặn cả epic vì một thay đổi thuộc epic danh mục. Đây là **lệch BR01 có chủ ý**, ghi ở §14. |
| **D10** | **Giữ nguyên tên cột DB hiện có** (`nguoi_tao` · `nguoi_cap_nhat` · `nguoi_xoa` · `nguoi_ghi_so`), KHÔNG đổi sang hậu tố `Id` như BR46 bản 12/08. *(BA chốt 2026-08-16 — [Q6](#q6--br46-đổi-tên-trường-hệ-thống-sang-hậu-tố-id))* | Migration V1002 không đụng bộ trường hệ thống; `BaseEntity` / `BaseChungTuEntity` giữ nguyên. | Đổi tên = migration diện rộng trên **toàn bộ** bảng nghiệp vụ, vượt xa phạm vi 06194. Coi BR46 là tên **logic**, tên vật lý giữ nguyên. |
| **D6** | Trạng thái chứng từ dùng `core.entity.TrangThaiChungTu` **hai giá trị** `CHUA_GHI_SO` / `DA_GHI_SO`, cột `trang_thai_chung_tu`. **✅ Đã là hiện trạng code từ 16/08** — không còn việc phải làm. | Khớp BR22 dòng "Ghi sổ" (Chưa ghi sổ · Đã ghi sổ). | Bản 5 trạng thái (`NHAP` · `CHO_DUYET` · `DA_DUYET` · `HUY`) không có trong BR nào và đã bị gỡ ([§2.0](#20-mốc-đối-chiếu-code) mục 3). |
| **D7** | Bốn trạng thái BR22 là **trường dẫn xuất**, BE tính lại tại đúng các mốc BA liệt kê, **không** nhận giá trị client gửi lên. | DTO ghi không có 4 trường này; service tính từ counter `SoLuongDaXuatHoaDon` / `SoLuongDaXuatKho` / `SoTienDaThanhToan`. | Nhận từ client = client thành nguồn sự thật của trạng thái kế toán; hai màn khác nhau sẽ ghi ra hai kết quả khác nhau. |
| **D8** | Chiết khấu: BE **tính lại toàn bộ** `TienChietKhau` / `TienThueGTGT` / các tổng trước khi lưu, không tin số client gửi. | `TinhToanBanHang` mở rộng theo BR12 (4 loại CK) + BR13 (thuế) + BR14 (thuế XK). | BR12 mục f là **ràng buộc chặn lưu** ở mức từng dòng — validate mà không tự tính lại thì client sửa số là lách được. |

---

## 1. Phạm vi

### Trong phạm vi

| Mã | Chức năng | UC | File con |
|---|---|---|---|
| **F01** | Xem danh sách (dùng chung CTBH + CTBDV, dòng tổng cộng, lọc mặc định đầu tháng) | U-06396 | [01-xem-danh-sach.md](01-xem-danh-sach.md) |
| **F02** | Xem chi tiết (4 biến thể kiêm) | U-06400 · 06401 · 06402 · 06985 | [02-xem-chi-tiet.md](02-xem-chi-tiet.md) |
| **F03** | Thêm mới (gồm xuất khẩu, chứng từ ghi nợ, kiêm xuất kho / hóa đơn / phiếu thu) | U-06397–06399 · 06461 · 06982 | [03-them-moi.md](03-them-moi.md) |
| **F04** | Chỉnh sửa | U-06403–06405 · 06983 | [04-chinh-sua.md](04-chinh-sua.md) |
| **F05** | Xóa (đơn lẻ + hàng loạt) | U-06406–06408 · 06984 | [05-xoa.md](05-xoa.md) |
| **F06** | Ghi sổ (đơn lẻ + hàng loạt) | U-06430 | [06-ghi-so.md](06-ghi-so.md) |
| **F07** | Bỏ ghi sổ (đơn lẻ + hàng loạt) | U-06431 | [07-bo-ghi-so.md](07-bo-ghi-so.md) |
| **F08** | Chiết khấu + 2 popup phân bổ | U-06966 | [08-chiet-khau.md](08-chiet-khau.md) |
| **F09** | Counter số lượng đã xuất HĐ / xuất kho (BR23) | (xuyên suốt) | [09-counter-so-luong.md](09-counter-so-luong.md) |
| **F10** | Sinh bút toán + sổ kho khi ghi sổ (BR20) | U-06430 | [10-hach-toan.md](10-hach-toan.md) |
| **F11** | Thiết kế DB | — | [11-thiet-ke-db.md](11-thiet-ke-db.md) |

### NGOÀI phạm vi

- **U-06462 Lập CTBH từ Phiếu xuất kho** và **U-06463 Lập CTBH từ Hóa đơn** — `SCR_CTBH_ThemMoi.md:5-6`
  khai là dùng chung màn, nhưng nguồn dữ liệu là module Kho (PMKT-E-03646) và Hóa đơn (PMKT-E-06196);
  đợt này chỉ mở API nhận `nguonId` chứ không tự đọc sang module khác.
- **Nút Thu tiền** (BR06 màn danh sách) — điều hướng sang màn tìm kiếm chứng từ của PMKT-E-06219 /
  06222. BE của 06194 không cấp endpoint nào cho việc này.
- **Tính giá xuất kho** — BR19 nói rõ do **PMKT-E-03629** định nghĩa, "không mô tả lại tại đây". Đợt
  này chỉ ghi `DonGiaVon` / `TienVon` do người dùng nhập hoặc = 0 chờ 03629 cập nhật.
- **Phát hành hóa đơn điện tử** — `SCR_CTBH_ThemMoi.md:9` ghi rõ chưa kết nối API cơ quan thuế.
- **BR16 Định khoản ngầm định** — tách theo [D5](#02-bảng-quyết-định).
- Hai endpoint `POST /export` · `POST /import` do base làm lộ ([BaseCrudController.java:171-198](../../cell-app/src/main/java/vn/vtt/pmkt/cell/core/controller/BaseCrudController.java)):
  export **giữ**, import **override trả 400 `CHUA_HO_TRO`** sau khi gọi `quyen.require(...)`.

---

## 2. Hiện trạng đã khảo sát

### 2.0. Mốc đối chiếu code

Chốt theo `cell-app` nhánh **`feat/chung-tu-ban-hang-2`**, commit **`4f350a1e`** (2026-08-16 13:15),
working tree sạch (chỉ có `V1011__ccdc.sql` đã `git add`).

**Bốn thay đổi so với lần khảo sát 2026-08-15 — đã cập nhật vào plan này:**

| # | Thay đổi | Tác động lên plan |
|---|---|---|
| 1 | **Base package `vn.dopai.pmkt` → `vn.vtt.pmkt`** (commit `1266deb0`); `vn/dopai` còn 0 file, `vn/vtt` có 1.052 file | Mọi đường dẫn `file:dòng` trong plan đã đổi theo; **số dòng không đổi** |
| 2 | **Migration đánh số lại**: hiện có `V1` · `V2` · `V3__gop_thay_doi_sau_baseline` · `V1000__moc_chan_code_cu_phai_pull_lai` · `V1011__ccdc` | Migration của epic này là **`V1012`**, không phải `V3` như bản 15/08 — xem [§7](#7-migration-dự-kiến) |
| 3 | **Refactor trạng thái chứng từ đã commit**: `TrangThaiChungTu` còn đúng 2 giá trị `CHUA_GHI_SO` / `DA_GHI_SO` ([TrangThaiChungTu.java:30,33](../../cell-app/src/main/java/vn/vtt/pmkt/cell/core/entity/TrangThaiChungTu.java)), `BaseChungTuEntity` map cột `trang_thai_chung_tu` ([BaseChungTuEntity.java:72](../../cell-app/src/main/java/vn/vtt/pmkt/cell/core/entity/BaseChungTuEntity.java)) | **[D6](#02-bảng-quyết-định) từ "đề xuất" thành "hiện trạng"** — không còn là việc phải làm |
| 4 | **Catalog quyền refactor** (commit `bbe55286`): `grep -c BanHangHoa V2__seed_data.sql` từ 9 → **49** | §2.4 · §10 vẫn đúng, chỉ là danh mục chi tiết hơn |

**Không đổi:** tên 12 bảng `sal_*`, `sal_chung_tu_ban_hang` vẫn **87 cột**, `acc_so_cai` + `acc_so_kho`
vẫn có, và toàn bộ số dòng của `BaseCrudController` · `ChungTuTemplate` · `GhiSoApi` giữ nguyên.

**Tài liệu BA không đổi** — `pmkt-docs` vẫn ở `2d8d62393`, PYC 06194 vẫn ở `1a928c53b`. Toàn bộ
BR01–BR24 và Q1…Q6 giữ nguyên hiệu lực.

### 2.2. Bảng DB — cái gì đã có, cái gì chưa

Lệnh đã chạy: `grep -c "CREATE TABLE public.<tên> " cell-app/src/main/resources/db/migration/V1__create_database.sql`

| Bảng BA yêu cầu | Tên trong DB | Có? | Ghi chú |
|---|---|:--:|---|
| `ENT_ChungTuBan` (header) | `sal_chung_tu_ban_hang` | ✅ | 87 cột (`V1__create_database.sql:16025`) |
| `ENT_ChiTietChungTuBan` | `sal_chung_tu_ban_hang_chi_tiet` | ✅ | `V1:16171` |
| `ENT_HoaDonBan` | `sal_hoa_don_ban_hang` | ✅ | `V1:16919` |
| `ENT_SoCai` | `acc_so_cai` | ✅ | |
| `ENT_SoKho` | `acc_so_kho` | ✅ | phục vụ [D4](#02-bảng-quyết-định) |
| `ENT_TaiKhoanNgamDinh` | — | ❌ | **0 kết quả** → chặn BR16, xem [Q2](#q2--định-khoản-ngầm-định-br16-chưa-có-bảng). Chính `V1011__ccdc.sql:112-113` cũng ghi nhận: *"toàn bộ schema hiện KHÔNG có bảng `*_tai_khoan_ngam_dinh` (đã grep V1 + V3, 0 kết quả)"* |
| `ENT_ChiTietTaiKhoanNgamDinh` | — | ❌ | **0 kết quả** |
| `ENT_DoiTuong` + `DoiTuong_VaiTro` | — | ❌ | Danh mục KH hiện là `mst_khach_hang_to_chuc` / `mst_khach_hang_ca_nhan`; chỉ có bảng vệ tinh `mst_doi_tuong_dia_chi_giao_hang`, `mst_doi_tuong_nhom`, `mst_doi_tuong_tk_ngan_hang`. Xem [Q3](#q3--nguồn-khách-hàng-ent_doituong-hay-mst_khach_hang_) |
| `ENT_DonViQuyDoiVatTu` | `mst_don_vi_quy_doi_vat_tu` | ✅ | phục vụ BR10 |

**Cột BR18 (`SoChungTuXuatKho` · `NgayChungTuXuatKho` · `SoChungTuThuTien` · `NgayChungTuThuTien` ·
`NguoiNopTien` · `LyDoThu` · `TaiKhoanNhanId` · `TenNganHangNhan`) — CHƯA CÓ** trên
`sal_chung_tu_ban_hang`; bảng hiện đi theo mô hình cũ `phieu_xuat_kho_id` / `phieu_thu_id` (FK sang
chứng từ lập riêng). Đây là thay đổi schema chính của đợt này — chi tiết ở [11-thiet-ke-db.md](11-thiet-ke-db.md).

**Cột BR23 `so_luong_da_xuat_kho_quy_doi` — đã có** trên bảng chi tiết (1 kết quả).

### 2.3. Base đã có sẵn — không viết lại

| Cần | Đã có ở base | `file:dòng` |
|---|---|---|
| 8 endpoint CRUD + tìm kiếm động | `BaseCrudController` | [BaseCrudController.java:121-198](../../cell-app/src/main/java/vn/vtt/pmkt/cell/core/controller/BaseCrudController.java) |
| Luồng ghi chứng từ (bất biến kế toán) | `ChungTuTemplate.thucThi()` | [ChungTuTemplate.java:103](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java) |
| Ghi sổ / bỏ ghi sổ / kiểm đã ghi sổ | `GhiSoApi.ghiSo` · `.boGhiSo` · `.daGhiSo` | [GhiSoApi.java:31,47,50](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/GhiSoApi.java) |
| Ghi sổ / bỏ ghi sổ / nhân bản / hàng loạt (REST) | `BaseChungTuController` | `accounting_core/chung_tu/controller/BaseChungTuController.java` |
| Kiểm quyền | `QuyenChecker` | `core/controller/QuyenChecker.java` |

### 2.4. Quyền

`grep -c "BanHangHoa" V2__seed_data.sql` → **9** kết quả ⇒ bộ mã `BanHangHoa.View` · `.View.Detail` ·
`.Create` · `.Edit` · `.Delete` · `.Post` · `.Unpost` · `.Clone` · `.Export` **đã seed**, không cần
migration quyền mới cho các chức năng hiện có. Endpoint hợp nhất mới ở [D1](#02-bảng-quyết-định) dùng
lại `BanHangHoa.View` + `BanDichVu.View` (kiểm cả hai, lọc theo quyền có được).

---

## 3. Kiến trúc

Phân tầng bắt buộc: `Controller → Service → Repository → Entity`. Module giữ nguyên shape Modulith
hiện có, **không** thêm `api/` (module khác chưa cần gọi vào — đúng luật 1 của `cell-app/CLAUDE.md`).

```
cell/chung_tu_ban_hang/
├── package-info.java                    @ApplicationModule(displayName = "chung_tu_ban_hang")
└── internal/
    ├── controller/   ChungTuBanHangController · ChungTuBanController (đọc hợp nhất — D1)
    ├── dto/          LuuChungTuBanHangRequest · ChungTuBanHangDto · ChiTietChungTuBanHangDto
    │                 + PhanBoChietKhauRequest · TongHopThueDto (mới)
    ├── entity/       ChungTuBanHang · ChiTietChungTuBanHang
    ├── model/        LoaiNghiepVuBanHang · LoaiChietKhau · ThueSuatGtgt · HinhThucThanhToan · MaLoiBanHang
    ├── port/         GhiSoKhoPort (mới — D4)
    ├── repository/   ChungTuBanHangRepository (+Custom/+Impl cho dòng tổng & đọc hợp nhất)
    └── service/
        ├── ChungTuBanHangCrudService.java
        └── business/  TinhToanBanHang · DinhKhoanBanHang · KiemTraBanHang · ChungTuBanHangMapper
                       · PhanBoChietKhau (mới) · CounterXuatHang (mới)
```

---

## 4. Danh mục API mục tiêu

| Mã | Method · Path | UC | Quyền | File con |
|---|---|---|---|---|
| **A1** | `POST /api/ban-hang/chung-tu-ban-hang/search` — phục vụ **cả** CTBH và CTBDV, lọc bằng `loaiNghiepVu` ([D1](#02-bảng-quyết-định)) | U-06396 | `BanHangHoa.View` (dòng `Bán dịch vụ` cần thêm `BanDichVu.View`) | F01 |
| ~~A2~~ | ~~endpoint hợp nhất riêng~~ — **bỏ**: gộp một bảng nên A1 đã là endpoint dùng chung | — | — | — |
| **A3** | `GET /api/ban-hang/chung-tu-ban-hang/cot` | U-06396 | `BanHangHoa.View` | F01 |
| **A4** | `POST /api/ban-hang/chung-tu-ban-hang/tong-hop` *(dòng tổng cộng BR05)* | U-06396 | `BanHangHoa.View` | F01 |
| **A5** | `GET /api/ban-hang/chung-tu-ban-hang/{id}` | U-06400–06402 · 06985 | `BanHangHoa.View.Detail` | F02 |
| **A6** | `POST /api/ban-hang/chung-tu-ban-hang` | U-06397–06399 · 06461 · 06982 | `BanHangHoa.Create` (+`.Post` khi `ghiSo=true`) | F03 |
| **A7** | `PUT /api/ban-hang/chung-tu-ban-hang/{id}` | U-06403–06405 · 06983 | `BanHangHoa.Edit` | F04 |
| **A8** | `DELETE /api/ban-hang/chung-tu-ban-hang/{id}` | U-06406–06408 · 06984 | `BanHangHoa.Delete` | F05 |
| **A9** | `POST /api/ban-hang/chung-tu-ban-hang/xoa-hang-loat` | U-06406–06408 | `BanHangHoa.Delete` | F05 |
| **A10** | `POST /api/ban-hang/chung-tu-ban-hang/{id}/ghi-so` | U-06430 | `BanHangHoa.Post` | F06 |
| **A11** | `POST /api/ban-hang/chung-tu-ban-hang/ghi-so-hang-loat` | U-06430 | `BanHangHoa.Post` | F06 |
| **A12** | `POST /api/ban-hang/chung-tu-ban-hang/{id}/bo-ghi-so` | U-06431 | `BanHangHoa.Unpost` | F07 |
| **A13** | `POST /api/ban-hang/chung-tu-ban-hang/bo-ghi-so-hang-loat` | U-06431 | `BanHangHoa.Unpost` | F07 |
| **A14** | `POST /api/ban-hang/chung-tu-ban-hang/phan-bo-chiet-khau` | U-06966 | `BanHangHoa.Create`/`.Edit` | F08 |
| **A15** | `POST /api/ban-hang/chung-tu-ban-hang/lookup` | — | `BanHangHoa.View` | F03 |
| **A16** | `POST /api/ban-hang/chung-tu-ban-hang/export` | U-06396 | `BanHangHoa.Export` | F01 |

---

## 5. Ma trận UC → endpoint → tài liệu

| UC | Tên | Endpoint | Tài liệu nguồn |
|---|---|---|---|
| U-06396 | Xem danh sách | A1 · A2 · A3 · A4 · A16 | `UC_CTBH_DanhSach.md` · `SCR_CTBH_DanhSach.md` |
| U-06397 | Thêm mới kiêm phiếu xuất | A6 | `UC_CTBH_ThemMoi.md` · `SCR_CTBH_ThemMoi.md` BR17·BR18 |
| U-06398 | Thêm mới kiêm hóa đơn | A6 | BR05 · BR06 · BR18 mục 6 |
| U-06399 | Thêm mới kiêm phiếu thu | A6 | BR18 mục 1 · BR22 mục 2 |
| U-06461 | CTBH xuất khẩu | A6 | BR13 mục 5 · BR14 |
| U-06982 | Thêm mới chứng từ ghi nợ | A6 | Tab Chứng từ ghi nợ |
| U-06400–06402 · 06985 | Xem chi tiết (4 biến thể) | A5 | `UC_CTBH_XemChiTiet.md` |
| U-06403–06405 · 06983 | Chỉnh sửa (4 biến thể) | A7 | `UC_CTBH_ChinhSua.md` · `SCR_CTBH_CapNhat.md` |
| U-06406–06408 · 06984 | Xóa (4 biến thể) | A8 · A9 | `UC_CTBH_Xoa.md` · `SCR_CTBH_PopupXacNhanXoa.md` |
| U-06430 | Ghi sổ | A10 · A11 | `UC_CTBH_GhiSo.md` · BR20 · BR21 |
| U-06431 | Bỏ ghi sổ | A12 · A13 | `UC_CTBH_BoGhiSo.md` · BR21 mục 3 |
| U-06966 | Chứng từ có chiết khấu | A14 | BR12 · `SCR_CTBH_PBCK.md` · `SCR_CTBH_PBCK_MHHD.md` |

---

## 6. Luồng tổng thể — Lưu và ghi sổ

```
Controller.create(ghiSo=true)
  → quyen.require(BanHangHoa.Create) [+ .Post]
  → ChungTuTemplate.thucThi(lenh)
      1. kiemTraNghiepVu   — BR01 MST/CCCD · BR06 trùng hóa đơn · BR12.f Tiền CK ≤ Thành tiền
                              · BR16.4 TK còn hợp lệ · BR23 SoLuong_nhap ≤ còn lại
      2. gỡ bút toán cũ    — GhiSoApi.boGhiSo(id)          (sửa/ghi lại mới có)
      3. tính lại tiền     — TinhToanBanHang: BR11 → BR12 → BR13 → BR14 → tổng BR-Section
      4. luuEntity         — header + chi tiết (orphanRemoval)
      5. khởi tạo counter  — BR23 mục 4 (CHỈ khi tạo mới)
      6. sinh bút toán     — DinhKhoanBanHang theo BR20 (#1…#7) → GhiSoApi.ghiSo(...)
      7. ghi sổ kho        — GhiSoKhoPort (D4) khi KiemPhieuXuatKho = True, BR17 lọc dòng
      8. tính 4 trạng thái — BR22
      9. kiểm kỳ khoá      — PeriodLockedException từ GhiSoApi
  → taoKetQua → ApiResponse<ChungTuBanHangDto>
```

---

## 7. Migration dự kiến

⚠ Số hiệu hiện có: `V1__create_database` · `V2__seed_data` · `V3__gop_thay_doi_sau_baseline` ·
`V1000__moc_chan_code_cu_phai_pull_lai` · `V1011__ccdc`. Dải `V1000+` là dải đang dùng cho code mới
sau mốc chặn, nên migration của epic này là **`V1012__sal_ctbh_kiem_xuat_kho_thu_tien.sql`**.

Nội dung dự kiến (chi tiết + SQL đầy đủ ở [11-thiet-ke-db.md](11-thiet-ke-db.md)):

1. **Gộp bảng theo [D1](#02-bảng-quyết-định)** — thứ tự bắt buộc:
   a. Nới `CHECK` của `loai_nghiep_vu` để nhận thêm `'Bán dịch vụ'`.
   b. `INSERT … SELECT` di trú **30 bản ghi** `sal_chung_tu_ban_dich_vu` → `sal_chung_tu_ban_hang`
      (gán `loai_nghiep_vu = 'Bán dịch vụ'`), và `sal_chi_tiet_chung_tu_ban_dv` → `sal_chung_tu_ban_hang_chi_tiet`.
      Cột nào bảng DV không có thì để `NULL`; cột nào DV có mà bảng đích không có thì **liệt kê rõ trong
      file DB và hỏi lại BA** trước khi bỏ.
   c. Đối chiếu số bản ghi trước/sau, rồi mới `DROP TABLE` hai bảng DV.
2. Thêm cột BR18 lên `sal_chung_tu_ban_hang`: `so_chung_tu_xuat_kho`, `ngay_chung_tu_xuat_kho`,
   `so_chung_tu_thu_tien`, `ngay_chung_tu_thu_tien`, `nguoi_nop_tien`, `ly_do_thu`,
   `tai_khoan_nhan_id`, `ten_ngan_hang_nhan` — hiện **chưa có cột nào** trong số này (§2.2).
3. Thêm cột BR14 (thuế XK) còn thiếu trên bảng chi tiết + cột BR12 nhóm CK theo mặt hàng/hóa đơn.
4. Index phục vụ BR02 (lọc mặc định đầu tháng): `(tenant_id, ngay_hach_toan DESC, ngay_chung_tu DESC, so_chung_tu)`.
5. **Không** DROP `phieu_xuat_kho_id` / `phieu_thu_id` — còn dùng cho luồng "lập riêng" (BR18 mục 5).
6. **Không** đụng bộ trường hệ thống ([D10](#02-bảng-quyết-định)).

---

## 8. Thứ tự thực hiện

| Bước | Nội dung | Phụ thuộc |
|---|---|---|
| **B1** | ~~Chốt Q1·Q2·Q3 với BA~~ — **xong 2026-08-16**, đáp án ở [§12](#12-điểm-cần-ba-xác-nhận--✅-đã-có-đáp-án-đủ-66-2026-08-16) | — |
| **B2** | Migration V3 + entity + mapper | B1 |
| **B3** | F01 danh sách + F02 chi tiết (đọc, rủi ro thấp) | B2 |
| **B4** | F08 chiết khấu + F09 counter (thuần tính toán, test unit được ngay) | B2 |
| **B5** | F03 thêm mới + F04 sửa | B4 |
| **B6** | F10 hạch toán + F06 ghi sổ + F07 bỏ ghi sổ | B5 |
| **B7** | F05 xóa (đơn lẻ + hàng loạt) | B6 |

---

## 9. Rủi ro kỹ thuật

| # | Rủi ro | Giảm thiểu |
|---|---|---|
| **R1** | **Code đang refactor dở** (§2.0): 17 file lõi sửa chưa commit, 323 migration vừa squash. Plan trỏ `file:dòng` có thể lệch sau khi commit tiếp. | Chốt mốc trong plan; soát lại §2.2 + §2.3 ngay trước khi bắt đầu B2. |
| **R2** | ~~BR01 mô tả một entity dùng chung trong khi DB có 2 bảng~~ — **đã giải quyết**: BA chốt gộp một bảng ([Q1](#q1--ent_chungtuban-một-bảng-hay-hai)). Rủi ro còn lại chuyển sang **R7**. | — |
| **R7** | **Migration gộp bảng có bước DROP** (`sal_chung_tu_ban_dich_vu`, `sal_chi_tiet_chung_tu_ban_dv`). Chạy sai thứ tự hoặc thiếu ánh xạ cột = mất 30 bản ghi và không rollback được. | Migration tách 3 bước a→b→c ([§7](#7-migration-dự-kiến)); bước c chỉ chạy sau khi đối chiếu số bản ghi khớp. `DROP` đặt ở **migration riêng chạy sau**, để nếu bước b sai thì còn bảng gốc mà đối chiếu. |
| **R8** | Cột `loai_nghiep_vu` sau khi gộp có **3 giá trị**, nhưng `SCR_CTBH_ThemMoi.md:27` chỉ khai combo 2 giá trị (Trong nước · Xuất khẩu) cho màn này. Màn CTBH không được phép tạo chứng từ `Bán dịch vụ`. | Chặn ở validate: `POST /chung-tu-ban-hang` từ chối `loaiNghiepVu = Bán dịch vụ` (màn CTBDV mới được tạo) — ghi rõ ở file con F03. |
| **R3** | ~~BR20 yêu cầu 2 bản ghi `SoCai` cho mỗi bút toán — sợ kernel chỉ sinh 1 dòng~~ — **đã kiểm 2026-08-16: KHÔNG phải rủi ro.** Javadoc `GhiSoRequest` ghi rõ *"Kernel tách mỗi `DinhKhoan` thành hai dòng sổ cái (vế Nợ + vế Có)"*, `DinhKhoan` cũng nói *"kernel tự TÁCH… hoán vị tài khoản/đối ứng"*. Chứng từ chỉ khai cặp TK + số tiền. | Không cần làm gì. Rủi ro còn lại về **trường thiếu** chuyển sang cảnh báo [C6](#15-cảnh-báo-bàn-giao). |
| **R4** | BR19 mục 7 ghi rõ **PMKT-E-03629 phải sửa** để lấy dòng `ChiTietChungTuBan` có `KhoId ≠ NULL` vào batch tính giá. Không sửa 03629 thì giá vốn của chứng từ kiêm **không bao giờ được tính**. | Đưa vào Q4 — cần BA/PO xác nhận ai làm phần 03629 và ở đợt nào. |
| **R5** | BR23 mục 3.3 đòi cập nhật counter **nguyên tử**; hai người cùng lập hóa đơn từ một CTBH có thể xuất vượt. | Khoá dòng `SELECT … FOR UPDATE` như `DongChungTuBanHangPort` đang làm, hoặc optimistic lock ở header. |
| **R6** | BR11 mục 2 (Số lượng = 0 nhưng giữ Thành tiền) và BR12 mục g (tổng thanh toán âm) là **hai ngoại lệ dễ bị "sửa cho đúng"** khi code. | Ghi thành test unit bắt buộc ở F08 trước khi implement. |

---

## 10. Quyền

Đã seed đủ (§2.4). Áp theo BR25:

| Endpoint | Mã quyền |
|---|---|
| A1–A4, A15, A16 | `BanHangHoa.View` (A16 thêm `.Export`) |
| A5 | `BanHangHoa.View.Detail` |
| A6 | `BanHangHoa.Create` — thêm `BanHangHoa.Post` khi `ghiSo = true` |
| A7 | `BanHangHoa.Edit` |
| A8, A9 | `BanHangHoa.Delete` |
| A10, A11 | `BanHangHoa.Post` |
| A12, A13 | `BanHangHoa.Unpost` |
| A2 (hợp nhất) | `BanHangHoa.View` **và/hoặc** `BanDichVu.View` — lọc kết quả theo quyền thực có |

---

## 11. Mã thông báo

Nguyên văn từ `6.messages.md` — trích các mã plan này dùng tới:

| Mã | Tình huống |
|---|---|
| `MSG_PMKT-E-06194_044` | Tiền CK vượt Thành tiền của dòng (BR12 mục f) — dòng thường: chặn; dòng KM/CKTM: cảnh báo |
| `MSG_PMKT-E-06194_049` | Chặn bỏ ghi sổ khi còn phiếu thu / đối trừ lập riêng đã ghi sổ (BR22 mục 2) |
| `MSG_PMKT-E-06194_050` | Sai định dạng MST tổ chức (10 số hoặc 10 số + "-" + 3 số) — BR01 mục d |
| `MSG_PMKT-E-06194_051` | Sai định dạng CCCD chủ hộ (12 số) — BR01 mục d |
| `MSG_PMKT-E-06194_101` | Trùng hóa đơn theo khóa Số HĐ + Ký hiệu + Mẫu số (BR06 mục b) |
| `MSG_PMKT-E-06194_107` | Tài khoản đang chọn không còn hợp lệ (BR16 mục 4) |

> Các mã còn lại trong `6.messages.md` được trích **nguyên văn** tại từng file con nơi phát sinh.

---

## 12. Điểm cần BA xác nhận — ✅ đã có đáp án đủ 6/6 (2026-08-16)


### Q1 — `ENT_ChungTuBan`: một bảng hay hai?

> ✅ **ĐÃ CHỐT 2026-08-16 — GỘP MỘT BẢNG.** Chứng từ bán hàng và bán dịch vụ dùng chung một bảng,
> phân biệt bằng `LoaiNghiepVu`. Đã áp vào [D1](#02-bảng-quyết-định) · [§3](#3-kiến-trúc) ·
> [§7](#7-migration-dự-kiến).


**Bằng chứng phía BA** — `SCR_CTBH_DanhSach.md:98`:
> "Màn danh sách **dùng chung** cho Chứng từ bán hàng và Chứng từ bán dịch vụ — lấy toàn bộ bản ghi
> **ENT_ChungTuBan** của tenant, phân biệt hai loại bằng `ChungTuBan.LoaiNghiepVu`"

**Bằng chứng phía code/DB** — `V1__create_database.sql:16025` và `:15904` là **hai bảng riêng biệt**
(`sal_chung_tu_ban_hang` 87 cột · `sal_chung_tu_ban_dich_vu` 64 cột), hai module Java riêng, và
`SCR_CTBH_ThemMoi.md:27` vẫn khai `Loại nghiệp vụ` chỉ có *Bán hàng trong nước* / *Bán hàng xuất khẩu*
— **không có** giá trị "Bán dịch vụ" trong combo của màn này, trong khi BR13/BR16/BR24 lại nhắc
"Bán dịch vụ" như một giá trị của cùng trường.

**Cần chốt:** (a) gộp thật thành một bảng — chấp nhận migration phá huỷ + viết lại 2 module; hay
(b) giữ 2 bảng, chỉ hợp nhất ở tầng đọc ([D1](#02-bảng-quyết-định))? Plan này đang giả định **(b)**.

### Q2 — Định khoản ngầm định (BR16) chưa có bảng

> ✅ **ĐÃ CHỐT 2026-08-16 — TẠM ĐỂ TRỐNG KÈM COMMENT.** Không tra định khoản ngầm định ở đợt này;
> chỗ nào sẽ tra thì để trống + comment trỏ về mục này. Đã áp vào [D5](#02-bảng-quyết-định).


BR16 quy định **mọi** cột tài khoản trên chứng từ lấy theo `ENT_TaiKhoanNgamDinh` /
`ENT_ChiTietTaiKhoanNgamDinh`, kèm bộ lọc `LocTaiKhoan` và mã lỗi `MSG_PMKT-E-06194_107`. Khảo sát
§2.2: **cả hai bảng đều không tồn tại** trong `V1__create_database.sql`.

**Cần chốt:** BR16 thuộc epic nào và làm ở đợt nào? Trước khi có nó, chứng từ bán hàng lấy TK theo
thứ tự ưu tiên 1 + 3 của BR16 mục 3 (danh mục vật tư / khách hàng, không có thì để trống) — đúng như
[D5](#02-bảng-quyết-định). **Đây là lệch BR16 có chủ ý và phải được BA ghi nhận.**

### Q3 — Nguồn khách hàng: `ENT_DoiTuong` hay `mst_khach_hang_*`?

> ✅ **ĐÃ CHỐT 2026-08-16 — DÙNG `mst_khach_hang_*`.** Giữ danh mục hiện có, không chờ `ENT_DoiTuong`.
> Đã áp vào [D9](#02-bảng-quyết-định).


BR01 mục 1 mô tả nguồn là **ENT_DoiTuong** lọc theo `DoiTuong_VaiTro.VaiTro = KhachHang`, và auto-fill
lấy `DoiTuong_VaiTro.TaiKhoanCongNoPhaiThuId` · `.NhanVienPhuTrachId` · `.DieuKhoanThanhToanId` ·
`.SoNgayDuocNo` · `.LoaiTienId`. DB hiện không có `mst_doi_tuong` lẫn bảng vai trò; danh mục khách
hàng là `mst_khach_hang_to_chuc` / `mst_khach_hang_ca_nhan` (mô hình cũ, tách 2 entity — đúng thứ
BR01 nói *"không tách thành 2 entity"*).

**Cần chốt:** epic nào chịu trách nhiệm chuyển danh mục sang `ENT_DoiTuong`, và 06194 chờ hay code
tạm trên `mst_khach_hang_*` rồi đổi sau?

### Q4 — Ai sửa PMKT-E-03629 cho luồng kiêm phiếu xuất kho?

> ⚠️ **ĐÃ CHỐT 2026-08-16 — NGOÀI PHẠM VI, NGƯỜI KHÁC LÀM.** Epic 06194 KHÔNG xử lý luồng này.
> **Phải nêu lại thành cảnh báo khi bàn giao** — xem [§15](#15-cảnh-báo-bàn-giao).


`SCR_CTBH_ThemMoi.md:1077` ghi **"Đối ứng cần bổ sung ở PMKT-E-03629"**: batch tính giá đang lấy giao
dịch từ `ChiTietPhieuXuatKho`, phải lấy thêm dòng `ChiTietChungTuBan` có `KhoId ≠ NULL`. Nếu 03629
không sửa, giá vốn của mọi chứng từ kiêm xuất kho **đứng nguyên ở 0**.

### Q5 — BR11 mới của `business_rules.md` cấm sắp xếp đồng thời nhiều cột

> ⚠️ **ĐÃ CHỐT 2026-08-16 — LÀM THEO PLAN NÀY** (giữ sort mặc định 3 cột theo epic).
> **Phải nêu lại thành cảnh báo khi bàn giao** — xem [§15](#15-cảnh-báo-bàn-giao).


`business_rules.md` @ `716ec3100` (12/08) đổi *"cho phép sắp xếp **đồng thời nhiều cột**"* thành
**"sắp xếp từng cột (không sắp xếp đồng thời nhiều cột)"**. Nhưng `SCR_CTBH_DanhSach.md:89` vẫn quy
định sắp mặc định **3 cột đồng thời** (Ngày hạch toán ↓ → Ngày chứng từ ↓ → Số chứng từ ↑).

**Cần chốt:** BR11 mới cấm *người dùng* sắp nhiều cột, hay cấm cả sort mặc định của server? Plan này
giữ sort mặc định 3 cột theo epic (epic thắng trong phạm vi epic) và **ghi nhận đang lệch BR11**.

### Q6 — BR46 đổi tên trường hệ thống sang hậu tố `Id`

> ✅ **ĐÃ CHỐT 2026-08-16 — TÔN TRỌNG THIẾT KẾ DB HIỆN CÓ, KHÔNG ĐỔI TÊN.**
> Đã áp vào [D10](#02-bảng-quyết-định).


`business_rules.md` @ `05d4f5a61` (12/08) đổi `NguoiTao` → `NguoiTaoId`, `NguoiCapNhat` →
`NguoiCapNhatId`, `NguoiXoa` → `NguoiXoaId`, `NguoiGhiSo` → `NguoiGhiSoId`. DB hiện dùng `nguoi_tao`,
`nguoi_cap_nhat`, `nguoi_xoa`, `nguoi_ghi_so` trên **toàn bộ** bảng nghiệp vụ.

**Cần chốt:** đổi tên cột toàn hệ thống (migration diện rộng, ngoài phạm vi 06194) hay coi BR46 là
tên **logic** còn tên cột vật lý giữ nguyên? Plan này giả định **giữ tên cột hiện có**.

---

## 13. Điều kiện nghiệm thu

**BA xác nhận:** Q1…Q6 đã có câu trả lời · ma trận UC §5 phủ đủ UC trong `1.functions-breakdown.md` ·
mã thông báo §11 khớp nguyên văn `6.messages.md`.

**Dev BE xác nhận:** `cd cell-app && ./gradlew unitTest` xanh · không thêm vi phạm ranh giới Modulith
mới (`ProxyModularityTest`) · mọi endpoint có `quyen.require(...)` (`HandlerAuthorizationArchTest`) ·
không insert `acc_so_cai` ngoài `GhiSoApi`.

---

## 14. Quy chuẩn nghiệp vụ (BR) áp dụng

| BR chung | Áp ở đâu |
|---|---|
| BR1 phân trang · BR2 hiển thị/sắp xếp · BR11 tìm kiếm/lọc | F01 — qua `BaseCrudController` + `@Searchable` |
| BR7 precision & làm tròn | F08 — mọi phép tính tiền; scale theo loại tiền |
| BR12 trạng thái chứng từ · BR33 màu trạng thái | F06 · F07 — `TrangThaiChungTu` 2 giá trị (D6) |
| BR17 kỳ kế toán · BR37 ngày hạch toán | F06 — `PeriodLockedException` từ `GhiSoApi` |
| BR18 ngoại tệ | F03 · F08 — cặp cột nguyên tệ / quy đổi |
| BR19 kiểm tra trùng · BR20 số chứng từ | F03 — trùng hóa đơn (BR06 epic) + cấp số chứng từ |
| BR25 phân quyền | §10 |
| BR28 multi-tenant · BR29 chính sách xóa · BR46 trường hệ thống | F11 |
| BR31 dòng tổng · BR39 xuất Excel · BR45 thao tác hàng loạt | F01 · F05 · F06 · F07 |
| BR36 ghi sổ · BR42 bỏ ghi sổ | F10 · F07 |

**BR chưa xử lý được ở đợt này** (chi tiết + cảnh báo bàn giao ở [§15](#15-cảnh-báo-bàn-giao)): BR11 (sắp xếp đồng thời — Q5) · BR46 (hậu tố `Id` — Q6) · BR47
(dữ liệu mặc định danh mục — không thuộc phạm vi chứng từ) · BR16 của epic (định khoản ngầm định — Q2).

---

## 15. Cảnh báo bàn giao

> Các mục dưới đây là **quyết định có chủ ý lệch tài liệu**, đã được BA / user đồng ý. Bắt buộc nhắc
> lại trong báo cáo khi hoàn thành code và trong mô tả PR — nếu không, người đọc code sau sẽ tưởng
> là bug.
>
> **Mục gắn 🔍 là điểm user yêu cầu đánh dấu để tự kiểm tra lại sau.** Trong code, mỗi chỗ tương ứng
> mang comment `// TODO-C<n> — xem plan §15` để grep ra ngay.

| # | Cảnh báo | Nguồn |
|---|---|---|
| **C1** | ⚠ **ĐÃ ĐỔI 2026-08-18 — nút thắt không còn là PMKT-E-03629.** Module `tinh_gia_xuat_kho/` **đã được cài** (commit `d60de30a`) và cấp [`TinhGiaXuatKhoRealtimeApi`](../../cell-app/src/main/java/vn/vtt/pmkt/cell/tinh_gia_xuat_kho/api/TinhGiaXuatKhoRealtimeApi.java) với `sauKhiGhiSoPhieuXuat(UUID phieuXuatKhoId)` — API nhận **id phiếu xuất kho**, không đọc dòng CTBH, tức 03629 **không cần sửa gì** như C1 bản cũ giả định. Nút thắt chuyển sang **G6**: chứng từ bán chưa sinh bản ghi `inv_phieu_xuat_kho` nên không có gì để 03629 tính giá. Xem [§17](#17-đối-chiếu-tài-liệu--code-2026-08-18). | [Q4](#q4--ai-sửa-pmkt-e-03629-cho-luồng-kiêm-phiếu-xuất-kho) · §17 G6 · G7 |
| **C2** | **Màn danh sách sắp xếp mặc định 3 cột đồng thời** (Ngày hạch toán ↓ → Ngày chứng từ ↓ → Số chứng từ ↑) theo `SCR_CTBH_DanhSach.md:89`, trong khi `business_rules.md` bản 12/08 đã đổi BR11 thành *"sắp xếp từng cột (không sắp xếp đồng thời nhiều cột)"*. Epic thắng trong phạm vi epic — **đang lệch BR11 có chủ ý**. | [Q5](#q5--br11-mới-của-business_rulesmd-cấm-sắp-xếp-đồng-thời-nhiều-cột) |
| **C3** | **Tên cột hệ thống giữ nguyên** `nguoi_tao` / `nguoi_cap_nhat` / `nguoi_xoa` / `nguoi_ghi_so`, **không** theo hậu tố `Id` của BR46 bản 12/08. Coi BR46 là tên logic. | [Q6](#q6--br46-đổi-tên-trường-hệ-thống-sang-hậu-tố-id) · [D10](#02-bảng-quyết-định) |
| **C4** | **BR16 chưa cài** — mọi chỗ lẽ ra tra định khoản ngầm định đang để trống kèm comment. Chứng từ vẫn lưu và ghi sổ được, nhưng người dùng phải tự chọn tài khoản trên từng dòng. | [Q2](#q2--định-khoản-ngầm-định-br16-chưa-có-bảng) · [D5](#02-bảng-quyết-định) |
| **C5** | **Auto-fill khách hàng thiếu 3 trường** so với BR01 (`TaiKhoanCongNoPhaiThuId` · `SoNgayDuocNo` · `LoaiTienId` của vai trò Khách hàng) vì mô hình `mst_khach_hang_*` không có. Người dùng tự nhập. | [Q3](#q3--nguồn-khách-hàng-ent_doituong-hay-mst_khach_hang_) · [D9](#02-bảng-quyết-định) |
| **C7** | 🔍 **SAI KHUNG — SỬA LẠI 2026-08-18.** Tài liệu (bản 08-13 **và** bản 08-17) nói rõ **chứng từ bán KHÔNG ghi `acc_so_kho`** — phiếu xuất kho mới là bên ghi (BR18 mục 4 · BR20 mục 4: *"Chứng từ bán **không sinh** bản ghi `acc_so_kho`"*). Vậy "sổ kho không được ghi" **không phải lỗi của module bán hàng**, và **không cần** cấp `GhiSoKhoApi` ở `accounting_core` như C7 bản cũ đề xuất. Lỗi thật nằm ở **G6** — chưa sinh `inv_phieu_xuat_kho`. Comment `TODO-C7` tại [GhiSoChungTuBanHang.java:79](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/service/business/GhiSoChungTuBanHang.java) đang mô tả sai, cần viết lại. | BR18 mục 4 · BR20 mục 4 · §17 G5 |
| **C6** | 🔍 **THU HẸP 2026-08-18 — 3 trong 6 trường thật ra truyền được, code chỉ quên gọi.** Kernel `DinhKhoan` **CÓ** `voiThuTu(sttDongChiTiet, sttButToan)` và `voiKhoanMucChiPhi(...)`; bảng `acc_so_cai` **CÓ** cột `stt_dong_chi_tiet` / `stt_but_toan` (thêm ở `V1001__pur_bao_toan_identity_va_concurrency.sql:23`) và `stt_but_toan` nằm trong **unique index chống ghi trùng**. `DinhKhoanBanHang.sangDinhKhoan` chỉ gọi `voiChiTiet` + `voiDoiTuong` → **sửa được mà không đụng core** (§17 G2, G3). Phần còn thiếu thật: `VuViecId` · `DonViId` · `DoiTuongTapHopChiPhiId` · `HopDongId` · `VatTuId`/`TenVatTu` — kernel không có tham số, **vẫn cần ticket `accounting_core`**; riêng `DoiTuongTapHopChiPhiId` và `DonHangId` thì **bảng chi tiết CTBH cũng chưa có cột** (§17 G4). | [D3](#02-bảng-quyết-định) · BR20 mục 2a · §17 G2–G4 |

---

## 16. Tài liệu tham chiếu

- PYC: `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/` (7 UC · 7 SCR · 6 Matrix · `6.messages.md`)
- BR chung: `pmkt-docs/ba/Common/business_rules.md`
- Khung BE: `docs/be-khung-kien-truc-chuan.md` · `docs/conventions.md` · `cell-app/CLAUDE.md`
- Epic liên quan: PMKT-E-06196 (Hóa đơn bán hàng) · PMKT-E-03629 (Tính giá xuất kho) ·
  PMKT-E-03646 (Phiếu xuất kho) · PMKT-E-06219 / 06222 (Phiếu thu)

---

## 17. Đối chiếu tài liệu ↔ code (2026-08-18)

> Rà lại sau khi tài liệu BA có bản mới. **Mốc so sánh:** tài liệu `715907142` (2026-08-16 14:36 — bản
> plan này dựa vào) → `1d1fc6152` (2026-08-18 08:29). Code: nhánh `feat/chung-tu-ban-hang-2`,
> commit `a25b3f07`, cây làm việc sạch (phần code của epic đã commit & merge).
>
> **Lượt rà thứ hai (2026-08-18, xuất phát từ câu hỏi "3 loại nghiệp vụ khác gì nhau"):** thêm
> **G13** · **G14** vào bảng dưới. Cả hai đến từ việc soi nhánh `Loại nghiệp vụ` của màn Thêm mới,
> không phải từ tài liệu đổi — tài liệu 06194 **không đổi dòng nào** kể từ mốc trên.

### 17.1. Tài liệu đổi những gì

Ba commit chạm 06194 / 06195 sau mốc plan:

| Commit | Giờ | Nội dung ảnh hưởng tới code |
|---|---|---|
| `8b7fac043` | 08-17 10:59 | **Bỏ điều kiện `TrangThai = Hoạt động`** ở BR01 (nguồn khách hàng) và BR16 mục 4 (danh sách tài khoản); MSG_PMKT-E-06194_107 **không còn** chặn lưu vì lý do "ngừng hoạt động" — chỉ còn chặn khi lệch bộ lọc hoặc không phải TK cấp cuối. |
| `25f9a7ca6` | 08-17 11:27 | **BR20 viết lại thành 6 mục** — gom mọi mô tả bút toán về một nguồn sự thật. Bổ sung bảng **b** (trường khác nhau giữa vế Nợ / vế Có, gồm `PSNo` · `PSNoQuyDoi` · `PSCo` · `PSCoQuyDoi`), bảng **c** (trường nguồn lấy số tiền), mục **4** (cặp TK + nguồn số tiền của phiếu xuất kho / phiếu thu), thêm `VatTuId` · `TenVatTu` vào mapping, khai `TKNganHangId` = `KheUocId` = NULL. BR18 đổi tên thành *"Chứng từ kiêm — phiếu xuất kho, phiếu thu và hóa đơn"*; BR19 mục 6 rút gọn. |
| `d23d1e20d` | 08-17 16:56 | Đổi tên entity trong tài liệu sang **tên bảng thật** (`ChungTuBan` → `sal_chung_tu_ban`, `SoCai` → `acc_so_cai`, `DoiTuong.Ma` → `mst_doi_tuong.Code`…). Không ảnh hưởng code theo [Q6](#q6--br46-đổi-tên-trường-hệ-thống-sang-hậu-tố-id) — chỉ lưu ý tài liệu gọi bảng là `sal_chung_tu_ban`, DB thật là `sal_chung_tu_ban_hang`. |

**Không có BR nào mới** và **không BR nào bị bỏ**. BR24 (phạm vi `LoaiNghiepVu` theo màn khởi tạo)
giữ nguyên — khớp với `R8` đã cài ở `LoaiNghiepVuBanHang.hopLeChoManBanHang()`.

### 17.2. Khoảng cách code — bảng G

| # | Khoảng cách | Bằng chứng | Sửa được ngay? |
|---|---|---|---|
| **G1** | **Chứng từ bán vẫn tự sinh bút toán giá vốn (#6) và thu tiền ngay (#7).** BR18 mục 4 và BR20 mục 1 · 3 · 4 nói rõ hai bút toán này **do phiếu xuất kho / phiếu thu ghi**, chứng từ bán *"không sinh hộ"*. | `QuyTacBanHang.java` khai đủ 7 quy tắc; `DinhKhoanBanHang.dungDong` nạp `NV_GIA_VON` khi `laKiemPhieuXuatKho()` và `NV_THU_TIEN` khi `laThuTienNgay()` | ✅ — bỏ 2 quy tắc + 2 nhánh nạp tiền. **Nhưng phải làm cùng G6**, nếu không thì bỏ xong sẽ không còn ai ghi hai bút toán đó. |
| **G2** | `STTButToan` / `STTDongChiTiet` **không được truyền**, dù kernel có `DinhKhoan.voiThuTu(...)` và `acc_so_cai` có cột. BR20 bảng **c** chốt số thứ tự cố định 1→5. Cột `stt_but_toan` nằm trong **unique index chống ghi trùng** nên để kernel tự cấp là rủi ro idempotency. | `DinhKhoanBanHang.sangDinhKhoan` chỉ gọi `voiChiTiet` + `voiDoiTuong` · `V1001__pur_bao_toan_identity_va_concurrency.sql:23,86` | ✅ không đụng core |
| **G3** | `KhoanMucChiPhiId` **không được truyền**, dù kernel có `voiKhoanMucChiPhi(...)` và dòng chi tiết có cột `khoan_muc_chi_phi_id`. BR20 mục 2a yêu cầu. | như trên | ✅ không đụng core |
| **G4** | 4 trường BR20 mục 2a **thật sự** không truyền được: `VuViecId` · `DonViId` · `DoiTuongTapHopChiPhiId` · `HopDongId`, cộng `VatTuId` / `TenVatTu` mới thêm ngày 08-17. Nặng hơn: `sal_chung_tu_ban_hang_chi_tiet` **chưa có cột** `doi_tuong_tap_hop_chi_phi_id` và `don_dat_hang_id` → kể cả mở rộng kernel vẫn chưa có nguồn. | `DinhKhoan.java` (record 12 tham số) · cột bảng chi tiết | ❌ cần ticket `accounting_core` + 1 migration |
| **G5** | Comment `TODO-C7` mô tả **sai** nghĩa vụ: nó nói chứng từ bán phải ghi `acc_so_kho`, tài liệu nói ngược lại. | [GhiSoChungTuBanHang.java:79](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/service/business/GhiSoChungTuBanHang.java) vs BR20 mục 4 | ✅ viết lại comment |
| **G6** | **BR18 mục 1 chưa cài** — Lưu **không** sinh `inv_phieu_xuat_kho` / `cash_phieu_thu` / `sal_hoa_don_ban_hang`. Đây là gốc của C1, C7 và G1. Ba vật cản: ① `kho/` có entity `PhieuXuatKho` nhưng `create` · `update` · `ghiSo` · `boGhiSo` đều `throw chuaHoTro(...)`; ② `kho/` và `hoa_don_ban_hang/` **không có package `api/`** → Modulith chặn `chung_tu_ban_hang` gọi vào; ③ **không có module `cash_phieu_thu`** nào trong `cell/`. | `PhieuXuatKhoCrudService.java:179` · `find … -path '*api*'` trên `kho/`, `hoa_don_ban_hang/` → rỗng | ❌ liên module, cần ticket riêng |
| **G7** | `inv_phieu_xuat_kho_chi_tiet` **thiếu cột** `nguon_id` / `chi_tiet_nguon_id` mà BR18 mục 1 đòi để tra ngược về dòng CTBH. (Bảng cha thì **đã có** `nguon_id` + `loai_chung_tu_nguon`, CHECK đã nhận `'CHUNG_TU_BAN'` ✅.) | `V1__create_database.sql` — khối `CREATE TABLE public.inv_phieu_xuat_kho_chi_tiet` | ❌ cần migration (bảng của module khác) |
| **G8** | Lọc tài khoản **vẫn ràng `TrangThai = ACTIVE`**, trái BR16 mục 4 bản 08-17 → tài khoản bị ngừng hoạt động sau khi chọn sẽ **chặn lưu oan** bằng MSG_107. | [TraCuuDanhMucRepository.java:48,147](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/repository/TraCuuDanhMucRepository.java) | ✅ bỏ tham số trạng thái, giữ `cho_phep_hach_toan` |
| **G9** | BR20 mục 5 chốt **hai cột luôn có số** (`TyGia` = 1 thì hai cột bằng nhau). Code chỉ gắn nguyên tệ khi `tyGia ≠ 1` → chứng từ VND để `so_tien_phat_sinh_no_ngoai_te` = NULL. | `DinhKhoanBanHang.sangDinhKhoan` — biến `ngoaiTe` | ⚠ cần chốt với BA: đây là đánh đổi có chủ ý của kernel (tránh nhân đôi giá trị trùng lặp trên mọi dòng sổ cái) |
| **G10** | **`acc_so_cai` thật thiếu nhiều cột BR20 mục 2a khai**: `ChiNhanhId` · `TienTeHachToanId`/`TienTeHachToan` · `TK`/`TKDoiUng` (số hiệu snapshot) · `DienGiaiDong` · `VatTuId`/`TenVatTu` · `TKNganHangId` · `KheUocId` · `IsAuto` · `NguoiGhiSoId`/`ThoiGianGhiSo`. Tài liệu tự nhận *"phủ 41/42 trường của `ENT_acc_so_cai`"* — con số đó tính trên **LDM**, không phải bảng đang chạy. | khối `CREATE TABLE public.acc_so_cai` — 39 cột | ❌ việc của `accounting_core` / BA, ngoài phạm vi epic |
| **G11** | Plan `R7` hẹn migration DROP hai bảng bán dịch vụ ở **`V1003`** — số này **đã bị chiếm** (`V1003__inv_tinh_gia_xuat_kho_runtime.sql`), hiện dùng tới `V1010`. Số trống kế tiếp: **`V1011`**. | `ls src/main/resources/db/migration/` | ✅ đổi số |
| **G12** | `client/src/features/banHang/chungTuBanHang/api/model.ts` (sửa `trangThaiXuatHang` → `nullish`) **chưa commit**. Theo *Cổng cây commit* của `CLAUDE.md`, còn dòng `M` trong `src/` là còn rủi ro lệch giữa local và deploy. | `git status --short` trong `client/` | ✅ commit |
| **G13** | **Hai trường BR14 không lộ ra API.** Entity `ChiTietChungTuBanHang` đã có `giaTriTinhThueXk` (nguyên tệ) + `giaTriTinhThueXkQuyDoi` và `TinhToanBanHang` tính đúng hai luồng, **nhưng cả DTO đọc lẫn DTO ghi đều không khai hai trường này**. Hệ quả: BR14 *"sửa `Giá trị tính thuế XK` để khớp Tờ khai Hải quan"* **không thực hiện được** — FE gửi gì cũng bị BE tính lại từ `thanhTien − chietKhau`. Nặng hơn: cột `donGiaThueXk` (thứ FE đang gắn nhãn "Giá trị tính thuế XK") bị **ghi đè** bằng `giaTriTinhThueXkQuyDoi` ở cuối `tinhThueXuatKhau` → người dùng gõ số theo tờ khai rồi mất trắng, không lỗi nào báo. | [`ChiTietChungTuBanHangDto.java:59-63`](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/dto/ChiTietChungTuBanHangDto.java) · [`LuuChiTietChungTuBanHangRequest.java:72-76`](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/dto/LuuChiTietChungTuBanHangRequest.java) · [`ChiTietChungTuBanHang.java:177,187`](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/entity/ChiTietChungTuBanHang.java) · [`TinhToanBanHang.java:290`](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/service/business/TinhToanBanHang.java) | ✅ — thêm 2 trường vào 2 DTO + mapper. Gọn trong `chung_tu_ban_hang/`, không đụng core. **Chặn FE**: chưa có thì lưới không dựng nổi đủ 6 cột BR14. |
| **G14** | **`POST /lookup` quảng cáo giá trị mà chính controller đó từ chối.** Trả `GiaTriDb.danhSach(LoaiNghiepVuBanHang)` = **cả 3** giá trị kể cả `Bán dịch vụ`, trong khi `hopLeChoManBanHang()` chặn `DICH_VU` ở tạo/sửa. Người dùng chọn một mục trông hợp lệ rồi ăn lỗi ở bước Lưu — sau khi đã gõ xong cả chứng từ. | [`ChungTuBanHangController.java:173`](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/controller/ChungTuBanHangController.java) vs [`LoaiNghiepVuBanHang.hopLeChoManBanHang()`](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/internal/model/LoaiNghiepVuBanHang.java) | ✅ — **FE đã chặn tạm** bằng `loaiNghiepVuHopLe()` (2026-08-18). BE nên lọc tại nguồn để hai màn cùng đọc một sự thật, thay vì mỗi màn tự nhớ. |

### 17.3. Đọc bảng G thế nào

- **G1 + G6 là một việc, không phải hai.** Bỏ bút toán giá vốn / thu tiền ra khỏi chứng từ bán mà
  chưa có ai sinh phiếu thật thì hai nghiệp vụ đó **biến mất khỏi sổ cái** — tệ hơn hiện trạng.
  Thứ tự đúng: G6 trước (sinh phiếu), G1 sau (thôi ghi hộ).
- **G2 · G3 · G5 · G8 · G11 · G12 làm được ngay**, nằm gọn trong `chung_tu_ban_hang/` và không
  chạm core — đây là phần "bổ sung" thực chất mà epic này còn nợ.
- **G4 · G6 · G7 · G10 vượt biên module**, phải mở ticket cho `accounting_core` / `kho` /
  `hoa_don_ban_hang` và một module `cash_phieu_thu` chưa tồn tại.
- **G9** là câu hỏi cho BA, không phải bug.
- **G13 chặn FE, ưu tiên cao nhất trong nhóm "làm được ngay".** Lưới chi tiết hàng hóa của FE hiện
  chỉ có 4 trong 6 trường BR14, và trường đang gắn nhãn "Giá trị tính thuế XK" thì ghi vào
  `donGiaThueXk` — thứ BE ghi đè. Đây là **mất dữ liệu người dùng nhập, im lặng**, không phải thiếu
  tính năng. Sửa DTO xong FE mới bổ sung được 2 cột quy đổi và trỏ lại cột nguyên tệ cho đúng.
- **G14 đã được FE chặn tạm** nên không còn là lỗi người dùng gặp; giữ trong bảng vì gốc nằm ở BE và
  màn Chứng từ bán dịch vụ (06195) sắp tới sẽ cần đúng cơ chế ngược lại (chỉ nhận `Bán dịch vụ`).
