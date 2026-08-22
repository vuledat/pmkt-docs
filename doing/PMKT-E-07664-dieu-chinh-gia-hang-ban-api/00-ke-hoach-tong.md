# Kế hoạch triển khai API — Điều chỉnh giá hàng bán (PMKT-E-07664)

> **Trạng thái:** BẢN NHÁP CHỜ REVIEW — **F1 (danh sách) đã code xong**, F2 mới có phần header, F3–F8 chưa code
> **Ngày cập nhật:** 2026-08-21 (rà lại toàn bộ sau đợt refactor V5 của repo)
> **Bản trước:** 2026-08-14 — xem §-1 để biết cái gì đã đổi và quyết định nào bị huỷ
> **Người review cần có:** 1 BA (chốt §12) + 1 Dev BE/DBA (chốt §7, §9, §10)

| Mục | Nội dung |
|---|---|
| Use case | PMKT-U-07665 Xem danh sách · U-07666 Thêm mới · U-07667 Xem chi tiết · U-07668 Xóa · U-07669 Ghi sổ · U-07670 Bỏ ghi sổ · U-07671 Sửa |
| Màn hình | `SCR_DanhSachDieuChinhGia` · `SCR_ThemMoiDieuChinhGia` · `SCR_SuaDieuChinhGia` · `SCR_XemChiTietDieuChinhGia` |
| Tài liệu nguồn | `pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/` + `pmkt-docs/ba/Common/business_rules.md` (**BR1…BR49**) + **`pmkt-docs/ba/Common/LDM_update/ldm-DieuChinhGiaHangBan.puml`** (mới) |
| Module BE | `cell-app/src/main/java/vn/vtt/pmkt/cell/dieu_chinh_gia_hang_ban/` — **đã tồn tại, 17 file** |
| Bảng DB | `sal_chung_tu_dieu_chinh_gia_hang_ban` (**69 cột**) · `…_chi_tiet` (**39 cột**) |
| FE đối ứng | `client/src/features/banHang/dieuChinhGiaHangBan/` — **đã tắt mock** (`DUNG_MOCK = false`), đang gọi BE thật cho màn danh sách |

---

## -1. CÁI GÌ ĐÃ ĐỔI TỪ BẢN 2026-08-14

Repo đã qua một đợt refactor lớn (`ManhDT/RefactorV5`) + 34 migration mới. Bảy thay đổi làm sai bản kế hoạch cũ:

| # | Thay đổi | Ảnh hưởng lên plan |
|---|---|---|
| 1 | **Base package đổi `vn.dopai.pmkt` → `vn.vtt.pmkt`** | mọi đường dẫn đã sửa trong cả 10 file |
| 2 | **Module `dieu_chinh_gia_hang_ban` ĐÃ ĐƯỢC DỰNG** — 17 file, màn danh sách chạy được | §2 chuyển từ *greenfield* sang *brownfield*; F1 xong, F2 dở |
| 3 | **`BaseChungTuEntity` bỏ cột `status`** — trạng thái nay là `trangThaiChungTu` (cột `trang_thai_chung_tu`), enum còn **2 giá trị** `CHUA_GHI_SO`/`DA_GHI_SO` | **D7 huỷ** (không DROP cột nữa) · phát sinh **lỗi thật ở entity hiện tại**, xem §2.4-L1 |
| 4 | **Engine đánh số chứng từ** (PMKT-U-16693) — `SoChungTuApi.sinhSo(entity, soNguoiDungGo)` + 3 bảng cấu hình, đã seed **4 quy tắc cho `DCGB`** | **D12 huỷ** — số chứng từ do engine cấp, không phải "người dùng tự nhập" |
| 5 | **Mã loại chứng từ `DCGB` đã tồn tại** trong `mst_loai_chung_tu` | **§12-Q1 ĐÃ TRẢ LỜI** — không phải hỏi BA nữa, không phải seed |
| 6 | **Migration đánh số theo timestamp** từ 2026-08-20 (`docs/rules/migration-danh-so-theo-timestamp.md`) | **§10 viết lại** — không còn `V3`; `V3__gop_thay_doi_sau_baseline.sql` đã bị dùng |
| 7 | **BA bổ sung BR47/48/49** và **LDM riêng cho epic** (`ldm-DieuChinhGiaHangBan.puml`) | **D6 huỷ** (LDM dùng cột phẳng) · thêm A18 (BR48) · §14 thêm BR48/BR49 |
| 8 | **Các module lân cận đã có**: `hoa_don_ban_hang`, `tra_lai_hang_ban`, `tien_mat_tien_gui`, và **`dieu_chinh_gia_hang_mua` (bản sinh đôi, code ĐẦY ĐỦ)** | **D3 đổi lý do** — không còn "thiếu module", mà là "thiếu `api/`" · có mẫu code 1:1 để bám (§2.3) |
| 9 | **`sal_chung_tu_ban_dich_vu` đã gộp vào `sal_chung_tu_ban_hang`** (V1012, `loai_nghiep_vu = 'Bán dịch vụ'`) | **F8 đơn giản hơn** — bỏ `UNION ALL` |

---

## 0. Các quyết định đã chốt

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Module `cell/dieu_chinh_gia_hang_ban/` shape Modulith `internal/`, phần ĐỌC kế thừa `BaseCrudController`, phần GHI sẽ chuyển sang `BaseChungTuController` + `ChungTuTemplate` | **Đã cài một nửa**: controller hiện `extends BaseCrudController<…, Void, Void>` và **chặn tường minh** 3 endpoint ghi. Khi làm F3 phải đổi sang `extends BaseChungTuController<E, D, CD, C, U>` — đây là một **breaking change nội bộ**, xem §8 bước 3 |
| **D2** | Dùng chung tiền tố bảng `sal_` với `chung_tu_ban_hang` | ✅ giữ nguyên, đã ghi lý do ở `package-info.java` của module |
| **D3** | Ghi sổ **chỉ sinh bút toán sổ cái** + đổi trạng thái. **KHÔNG** tạo Phiếu thu/Chi, Hóa đơn điều chỉnh | **Lý do đã đổi**: `tien_mat_tien_gui` (49 file) và `hoa_don_ban_hang` (19 file) **nay đã tồn tại**, nhưng **cả hai không có package `api/`** ⇒ Modulith cấm gọi vào. Muốn sinh phiếu/HĐ thì hai module đó phải mở `api/` trước — xem §12-Q2 (đã đổi nội dung) |
| **D4** | Liên kết nguồn qua `QuanHeChungTuApi`, **mức DÒNG**, loại đích `LoaiChungTu.SAL_DIEU_CHINH_GIA_HANG_BAN` | ✅ giữ nguyên. `laTieuThu() = false` nên không áp ràng buộc "Σ tiêu thụ ≤ SL nguồn" |
| **D5** | Module phải cài `DongChungTuPort` cho loại của mình | ✅ giữ nguyên — nhưng **hợp đồng đổi** theo D6: `laySoLuong` trả thẳng `so_luong` chứ không `COALESCE(tang, giam)` nữa. Javadoc của port ([DongChungTuPort.java:54](../../cell-app/src/main/java/vn/vtt/pmkt/cell/quan_he_chung_tu/api/DongChungTuPort.java)) vẫn ghi COALESCE ⇒ **phải sửa javadoc đó cùng lúc**, nếu không hai chỗ nói ngược nhau |
| ~~**D6**~~ | ~~Giữ cặp cột `*_tang`/`*_giam`, DTO phẳng do mapper chọn khối~~ | **HUỶ.** LDM mới (`ldm-DieuChinhGiaHangBan.puml` dòng 96-98) khai **một bộ phẳng** `SoLuong`/`DonGia`/`ThanhTien`, và cả `ChietKhauPhanTram`/`ChietKhau` cũng phẳng. Thay bằng **D6′** |
| **D6′** | **Chuyển bảng chi tiết sang cột phẳng**: thêm `so_luong`, `don_gia`, `thanh_tien`, `chiet_khau_phan_tram`, `chiet_khau` + backfill từ 10 cột `*_tang`/`*_giam`, và **deprecate 10 cột cũ** (không xoá lần này) | Bảng chi tiết chưa có dòng nghiệp vụ nào (module chưa cài luồng ghi) nên backfill rẻ. Hướng Tăng/Giảm đã nằm ở header `loai_dieu_chinh` — hai khối cột là mã hoá **thừa** cùng một thông tin, và mọi công thức của SCR đều viết trên một bộ số. **Không chọn** giữ hai khối: mọi truy vấn phải `COALESCE`, và `DonChungTuPort` của base đã phải viết riêng một ngoại lệ cho đúng bảng này |
| ~~**D7**~~ | ~~DROP cột `trang_thai_chung_tu`~~ | **HUỶ.** Base đã tự đổi: cột `trang_thai_chung_tu text NOT NULL DEFAULT 'CHUA_GHI_SO'` **chính là** cột trạng thái chuẩn, cột `status` đã biến mất khỏi `BaseChungTuEntity` |
| **D8** | Thuế suất lưu **enum text** (`thue_suat_gtgt_mac_dinh` + `gia_tri_thue_gtgt`), `thue_suat_gtgt_id` deprecate | ✅ giữ nguyên; LDM xác nhận (`ThueSuatGTGT: enum!` + `ThueSuatKhac`) |
| **D9** | Enum `ThueSuatGtgt` khai lại trong `internal/model/` | ✅ giữ nguyên — `chung_tu_ban_hang` vẫn không có `api/` cho enum này (`api/` của nó chỉ có `GiaVonBanHangApi`) |
| **D10** | Ba endpoint `/nguon/*` trong cùng controller, đúng tên FE đã khai | ⚠ **Sửa cách cài**: `chung_tu_mua_hang` đã mở `ChungTuMuaHangNguonApi` cho đúng bài toán này ([file](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_mua_hang/api/ChungTuMuaHangNguonApi.java)). Bản bán hàng phải làm **đối xứng**: mở `chung_tu_ban_hang/api/ChungTuBanHangNguonApi` thay vì bắn SQL native xuyên bảng của module khác — xem D13 |
| ~~**D11**~~ | ~~`maLoaiChungTu = "CTDG"`, seed mới~~ | **HUỶ — dùng `DCGB`**, đã seed sẵn tại [V1032:153](../../cell-app/src/main/resources/db/migration/V1032__tknd_va_cau_hinh_danh_so.sql). Sinh đôi mua hàng dùng `DCGM` ([DieuChinhGiaMuaSupport.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/dieu_chinh_gia_hang_mua/internal/DieuChinhGiaMuaSupport.java)) |
| ~~**D12**~~ | ~~Số chứng từ người dùng nhập, không tự sinh~~ | **HUỶ.** Engine đánh số (PMKT-U-16693) đã lên: template gọi `SoChungTuApi.sinhSo(entity, soNguoiDungGo)` — ô để trống ⇒ cấp số kế tiếp, có chữ ⇒ đi 7 bước BR04. Xoá chứng từ phải gọi `thuHoi(...)` để trả số về pool (BR10) |
| **D13** | **Đọc dữ liệu nguồn qua `api/` của module chủ sở hữu**, không SQL native xuyên bảng | Cần mở `chung_tu_ban_hang/api/ChungTuBanHangNguonApi` (đối xứng bản mua) và `tra_lai_hang_ban` phải cấp được "SL đã trả lại theo dòng nguồn". **Không chọn** SQL native như bản kế hoạch cũ: khi ấy các bảng đó chưa có chủ, nay đã có — bắn SQL vào bảng của module khác là đi vòng qua ranh giới Modulith mà lint không bắt được |
| **D14** | **Bổ sung A18 `POST /xem-du-lieu-ghi-so`** — form "Xem dữ liệu ghi sổ" hai chế độ theo **BR48** | Chế độ *Dữ liệu sổ* dùng lại A10; chế độ *Xem trước* phải **tính bút toán tại chỗ từ dữ liệu form**, kể cả chứng từ chưa Lưu lần nào ⇒ phải là `POST` mang body, không phải `GET /{id}` |
| **D15** | **Chiết khấu mức header** (`LoaiChietKhau` + `TyLeChietKhau` của LDM) đưa vào phạm vi | LDM khai hai trường này ở header; SCR chỉ ghi "Tham khảo phần chiết khấu của chứng từ bán hàng" (dòng 436-438). Lấy theo LDM vì nó cụ thể hơn, và `chung_tu_ban_hang` đã có sẵn cặp `loai_chiet_khau`/`gia_tri_chiet_khau` để bám |

> ⚠️ **Cảnh báo môi trường:** `cell-app/CLAUDE.md` vẫn ghi *"Migration: `V<N>__…`, N tăng dần"* — **đã lỗi thời** từ 2026-08-20, luật đúng nằm ở [docs/rules/migration-danh-so-theo-timestamp.md](../../docs/rules/migration-danh-so-theo-timestamp.md). Có arch-test `MigrationNamingArchTest` bắt lỗi này ở `unitTest`.

---

## 1. Phạm vi

### 1.1 Trong phạm vi

| # | Chức năng | Nguồn | File con | Tình trạng |
|---|---|---|---|---|
| F1 | Xem danh sách + lọc/sắp xếp/phân trang + dòng tổng | UC-07665 | [01](01-xem-danh-sach.md) | ✅ **ĐÃ CODE** — còn 1 lỗi §2.4-L1 |
| F2 | Xem chi tiết + dòng chi tiết + bút toán + nhân bản | UC-07667 | [02](02-xem-chi-tiet.md) | 🟡 header xong; thiếu `chiTiet`, `/dong-chi-tiet`, `/thong-tin-hach-toan`, `/nhan-ban` |
| F3 | Thêm mới (Lưu / Lưu và ghi sổ) | UC-07666 | [03](03-them-moi.md) | ❌ endpoint bị chặn tường minh |
| F4 | Chỉnh sửa chứng từ chưa ghi sổ | UC-07671 | [04](04-chinh-sua.md) | ❌ như trên |
| F5 | Xóa (đơn + hàng loạt) | UC-07668 | [05](05-xoa.md) | ❌ như trên |
| F6 | Ghi sổ (đơn + hàng loạt) | UC-07669 | [06](06-ghi-so.md) | ❌ |
| F7 | Bỏ ghi sổ (đơn + hàng loạt) | UC-07670 | [07](07-bo-ghi-so.md) | ❌ |
| F8 | Chọn chứng từ nguồn (Bước 1) | SCR_ThemMoi Bước 1 | [08](08-chon-nguon-chung-tu.md) | ❌ |
| **F10** | **Xem dữ liệu ghi sổ** (2 chế độ) — **MỚI, BR48** | BR48 | [06 §5](06-ghi-so.md) | ❌ |
| F9 | Migration bổ sung cột + chuyển cột phẳng | §9, §10 | [09](09-thiet-ke-db.md) | ❌ |

### 1.2 NGOÀI phạm vi (không cài lần này)

| Bị loại | Bằng chứng | Endpoint kế thừa trả gì |
|---|---|---|
| Sinh bản ghi **Phiếu thu / Phiếu chi / Giấy báo / Séc / UNC** khi Thanh toán ngay | `tien_mat_tien_gui` có 49 file nhưng **không có package `api/`** (`find … -type d -name api` không trúng) ⇒ không có hợp đồng để gọi | `/ghi-so` vẫn 200; bút toán vế tiền sinh đủ từ `tai_khoan_tien_id`; cột `phieu_thu_id`/`phieu_chi_id`/… giữ `NULL` |
| Sinh **Hóa đơn điều chỉnh** khi tick "Lập kèm HĐ điều chỉnh" | `hoa_don_ban_hang` có 19 file, cũng **không có `api/`** | cờ + toàn bộ trường tab Hóa đơn được lưu; `hoa_don_dieu_chinh_id` giữ `NULL`; validate `MSG_206` vẫn chạy |
| **Cập nhật sổ thuế đầu ra** | không có module sổ thuế trong `cell/` | cột `khong_tong_hop_to_khai_gtgt` được lưu cho module thuế sau này |
| **BR49** Di chuyển chứng từ trước–sau ở màn chi tiết | BR mới, thuần điều hướng | FE tự làm từ danh sách đang cầm (cùng `sort` với A1). BE **không** thêm endpoint — xem §12-Q11 |
| Tab **Thuế · Hạch toán · Đính kèm · Tham chiếu** | FE cũng chưa dựng (`IMPLEMENT.md` §5.3) | — |
| **Xuất / Nhập Excel** | `DanhSachQuyen.md §B4.6` không bật quyền | `/export`, `/import` kế thừa nhưng **403** |
| **Chiết khấu thương mại** (BR14 của SCR), **ĐVT quy đổi** (BR13 của SCR) | bảng trường của lưới không có ô tương ứng | §12-Q6, Q7 |
| **`LoaiDongHang`** (dòng hàng / dòng ghi chú — LDM), `SoLo`, `HanSuDung`, `NhomHHDVMuaVao`, `DienGiaiThue` | có trong LDM nhưng **không có trong SCR** của epic | §12-Q12 |

---

## 2. Hiện trạng đã khảo sát (đo 2026-08-21)

### 2.1 Code hiện có — **BROWNFIELD**

```bash
find cell-app/src/main/java/vn/vtt/pmkt/cell/dieu_chinh_gia_hang_ban -name "*.java" | wc -l
```
```
17
```

| Lớp | File | Ghi chú |
|---|---|---|
| controller | `DieuChinhGiaHangBanController` | `extends BaseCrudController<DieuChinhGiaHangBan, Dto, Void, Void>`; **override `create`/`update`/`delete` để ném 400 `CHUA_HO_TRO`** |
| entity | `DieuChinhGiaHangBan` | chỉ HEADER; **chưa có** `ChiTietDieuChinhGiaHangBan` |
| dto | `DieuChinhGiaHangBanDto` (44 trường, phẳng), `TongHopDieuChinhGiaDto` | **chưa có** `chiTiet`, `chungTuThanhToan`, `hoaDon`, request DTO |
| model | `HuongDieuChinhGia`, `HinhThucThanhToanDcg`, `NguonChungTu`, `LyDoDieuChinhNguon`, `TrangThaiHoaDonDcg`, `MaDb`, `MaLoiDieuChinhGia` | đủ 6 enum + mã lỗi |
| repository | `…Repository` + `…RepositoryCustom` + `…Impl` | có `tongHop(spec)` cho dòng tổng |
| service | `DieuChinhGiaHangBanCrudService`, `business/DieuChinhGiaMapper` | `extends AbstractCrudService`, **chưa** `AbstractChungTuCrudService` |

**Kết luận:** F1 chạy được thật (FE đã tắt mock). Phần GHI chưa có gì và **cố ý bị chặn** — javadoc controller ghi rõ lý do: `BaseCrudController` gọi thẳng `repository.save`, đúng cho danh mục nhưng sai cho chứng từ kế toán.

### 2.2 Hiện trạng DB

```bash
ls cell-app/src/main/resources/db/migration/ | wc -l   # 36
ls cell-app/src/main/resources/db/migration/ | sort -V | tail -1   # V1032__tknd_va_cau_hinh_danh_so.sql
```

⚠ **Số hiệu mới KHÔNG phải `V1033`.** Từ 2026-08-20 lấy bằng `date +V%Y%m%d%H%M%S` — xem §10.

Baseline đã đổi tên: `V1__baseline.sql` → **`V1__create_database.sql`** (squash V1 + V3…V7), kèm `V2__seed_data.sql`.

**Bảng chính nay 69 cột** — 6 cột trong §9.2 của bản kế hoạch cũ **đã được thêm** (`thanh_toan_ngay`, `lap_kem_hoa_don_dieu_chinh`, `nguon_chung_tu`, `ly_do_dieu_chinh_nguon`, 4 cột `tong_*_quy_doi`), 2 CHECK đã có, và **2 index đề xuất cũng đã tạo** (`idx_sal_dcg_danh_sach`, `idx_sal_dcg_khach_hang`). **Bảng chi tiết vẫn nguyên 39 cột** — chưa động gì. Chi tiết: [09](09-thiet-ke-db.md).

### 2.3 Hạ tầng base — cái gì có sẵn, và **mẫu code 1:1**

| Cần | Đã có ở base | Vị trí |
|---|---|---|
| **Bản sinh đôi ĐÃ CODE ĐỦ** của chính nghiệp vụ này (bên mua) | `dieu_chinh_gia_hang_mua/` — 22 file: template 5 luồng, `DinhKhoan…`, `KiemTra…`, `TinhToan…`, `GhiSo`/`BoGhiSo`, `HangLoatService`, `…Support` | [dieu_chinh_gia_hang_mua/](../../cell-app/src/main/java/vn/vtt/pmkt/cell/dieu_chinh_gia_hang_mua/) — **đọc trước khi code F3–F7** |
| 8 endpoint CRUD + tìm kiếm động | `BaseCrudController` | [core/controller/BaseCrudController.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/core/controller/BaseCrudController.java) |
| Ghi sổ / bỏ ghi sổ / nhân bản / bút toán / dòng chi tiết / 3 thao tác hàng loạt | `BaseChungTuController` | [:95, :104, :121, :141, :158, :174, :183, :192](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/controller/BaseChungTuController.java) |
| Trình tự 5 luồng bất biến | `ChungTuTemplate.thucThi` | [accounting_core/chung_tu/service/ChungTuTemplate.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java) |
| Ghi/gỡ bút toán | `GhiSoApi` (`ghiSo`/`boGhiSo`/`daGhiSo`) | [hach_toan/api/GhiSoApi.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/GhiSoApi.java) |
| Đọc sổ cái | `SoCaiApi.theoChungTu(id)` | [hach_toan/api/SoCaiApi.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/SoCaiApi.java) — ⚠ **thiếu lọc theo loại chứng từ**, xem §2.4-L2 |
| **Đánh số chứng từ (MỚI)** | `SoChungTuApi.sinhSo(chungTu, soNguoiDungGo)` · `.thuHoi(chungTu, ngayHachToan)` | [hach_toan/api/SoChungTuApi.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/SoChungTuApi.java) |
| **Tài khoản ngầm định (MỚI)** | `master_data/tai_khoan_ngam_dinh/api/TaiKhoanNgamDinhApi` | dùng cho BR7/BR8 của SCR (TK công nợ · doanh thu · giảm giá) thay vì tự tra danh mục |
| Kiểm kỳ kế toán | `KyKeToanApi.kiemTraKyMo` — **kernel tự gọi** | [hach_toan/api/KyKeToanApi.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/KyKeToanApi.java) |
| Liên kết chứng từ | `QuanHeChungTuApi` + `LoaiChungTu.SAL_DIEU_CHINH_GIA_HANG_BAN` | [quan_he_chung_tu/api/](../../cell-app/src/main/java/vn/vtt/pmkt/cell/quan_he_chung_tu/api/) |
| **Mẫu `api/` cho dữ liệu nguồn** | `ChungTuMuaHangNguonApi.layNguonDieuChinhGia(id)` + 2 record | [chung_tu_mua_hang/api/ChungTuMuaHangNguonApi.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_mua_hang/api/ChungTuMuaHangNguonApi.java) — D13 |
| Envelope, quyền, whitelist lọc | `PageResponse` · `ApiResponse` · `QuyenChecker` · `@Searchable` | `core/` |

**Quyền:** 7 mã `DieuChinhGiaHangBan.{View, View.Detail, Create, Edit, Delete, Post, Unpost}` đã seed. **`.Clone` vẫn CHƯA seed** ⇒ A11 sẽ 403 (§10).

### 2.4 Lỗi/nợ phát hiện khi rà lại — **cần xử lý**

| # | Vấn đề | Bằng chứng | Xử lý |
|---|---|---|---|
| **L1** | Entity khai `@Searchable(alias = "trangThaiChungTu", **path = "status"**)` nhưng `BaseChungTuEntity` **không còn field `status`** (`grep -n "status" BaseChungTuEntity.java` → rỗng) ⇒ lọc/sắp xếp theo trạng thái của màn danh sách **trỏ vào một property không tồn tại** | [DieuChinhGiaHangBan.java:49-50](../../cell-app/src/main/java/vn/vtt/pmkt/cell/dieu_chinh_gia_hang_ban/internal/entity/DieuChinhGiaHangBan.java) | **Xoá cả annotation** — base nay đã đặt tên field đúng bằng `trangThaiChungTu` nên alias thừa. `tra_lai_hang_ban/internal/entity/TraLaiHangBan.java:34` **dính y hệt** ⇒ báo để chủ module đó sửa, không tự sửa sang module khác |
| **L2** | `SoCaiApi.theoChungTu(chungTuId)` chỉ lọc theo `chungTuId`, trong khi **BR48.3 bắt buộc lọc đồng thời `ChungTuId` + `LoaiChungTuId`** — hai chứng từ khác loại có thể trùng `ChungTuId` | [SoCaiApi.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/SoCaiApi.java) vs `business_rules.md` BR48.3 | Không tự sửa `accounting_core`. **Mở ticket cho chủ kernel**, và ghi rõ ở [02](02-xem-chi-tiet.md) rằng A10/A18 đang thiếu vế lọc thứ hai |
| **L3** | Quy tắc đánh số seed cho `DCGB` chỉ có **4 dòng, đều là "Giảm giá"** — không có dòng nào cho **Tăng giá** | [V1032:1166-1169](../../cell-app/src/main/resources/db/migration/V1032__tknd_va_cau_hinh_danh_so.sql) | Chứng từ Tăng giá sẽ ném `QUY_TAC_KHONG_TON_TAI` lúc Lưu. Phải seed bổ sung — §10, và **§12-Q13** hỏi BA tên quy tắc |
| **L4** | `dieu_kien` của quy tắc đánh số dùng `{"hinhThucThanhToan": "CHI_TIEN_MAT"}` (SCREAMING_SNAKE) trong khi CHECK của bảng là `'ChiTienMat'` (PascalCase) | [V1032:1167](../../cell-app/src/main/resources/db/migration/V1032__tknd_va_cau_hinh_danh_so.sql) vs [V1:16387](../../cell-app/src/main/resources/db/migration/V1__create_database.sql) | Phải xác định engine so bằng **tên hằng Java** hay **giá trị DB** trước khi cài F3; sai là mọi chứng từ Thanh toán ngay không cấp được số. **§12-Q14** |
| **L5** | Javadoc `DongChungTuPort.laySoLuong` chỉ đích danh bảng này với `COALESCE(so_luong_tang, so_luong_giam)` | [DongChungTuPort.java:54](../../cell-app/src/main/java/vn/vtt/pmkt/cell/quan_he_chung_tu/api/DongChungTuPort.java) | Theo **D6′** thì câu đó thành sai — sửa javadoc **cùng PR** với migration chuyển cột phẳng |

---

## 3. Kiến trúc

### 3.1 Phân tầng đích (sau F3)

```
DieuChinhGiaHangBanController          extends BaseChungTuController<E, D, CD, C, U>
        │  (hiện tại: BaseCrudController<E, D, Void, Void> — phải ĐỔI ở bước F3)
        │  + A15/A16/A17 /nguon/*   + A18 /xem-du-lieu-ghi-so
        ▼
DieuChinhGiaHangBanCrudService         extends AbstractChungTuCrudService<E, D, CD, C, U>
        │  (hiện tại: AbstractCrudService — phải ĐỔI)
        │  └── uỷ quyền: LuuDieuChinhGiaTemplate  (5 luồng, ChungTuTemplate)
        ▼
DieuChinhGiaHangBanRepository (+Custom/Impl)     NguonDieuChinhGiaService → ChungTuBanHangNguonApi
        ▼
DieuChinhGiaHangBan  ──1..n──▶  ChiTietDieuChinhGiaHangBan   (cả hai extends Base…Entity)
```

### 3.2 Lựa chọn kiến trúc + lý do

| | Phương án A — giữ `BaseCrudController`, tự viết ghi sổ | **Phương án B (CHỌN) — chuyển sang `BaseChungTuController` + `ChungTuTemplate`** |
|---|---|---|
| Endpoint phải viết | 17 | 6 |
| Trình tự ghi sổ | tự giữ | base cưỡng chế, 5 luồng `private` |
| Đánh số chứng từ (BR04) | tự gọi `SoChungTuApi` ở 5 chỗ | template gọi một lần |
| Có mẫu 1:1 để bám | không | **có** — `dieu_chinh_gia_hang_mua` |
| Chi phí đổi | 0 | phải đổi generic của controller + service (1 lần, ~2 file) |
| Rủi ro | trôi khỏi chuẩn | đổi generic làm gãy `create/update/delete` đang ném 400 — phải xoá 3 override đó cùng lúc |

### 3.3 Cấu trúc thư mục đích

```
cell/dieu_chinh_gia_hang_ban/
├── package-info.java                      ✅ đã có (cập nhật lại phần "Phạm vi ĐANG cài" khi F3 xong)
└── internal/
    ├── DieuChinhGiaSupport.java           ➕ gom repo + mapper + tinhToan + kiemTra + dinhKhoan (mẫu: DieuChinhGiaMuaSupport)
    ├── adapter/DongDieuChinhGiaAdapter.java   ➕ cài DongChungTuPort (D5)
    ├── controller/DieuChinhGiaHangBanController.java   ✏️ đổi base class
    ├── dto/  ✅ DieuChinhGiaHangBanDto · TongHopDieuChinhGiaDto
    │         ➕ ChiTietDieuChinhGiaDto · ChungTuThanhToanDto · HoaDonDieuChinhDto
    │         ➕ LuuDieuChinhGiaRequest · LuuChiTietRequest
    │         ➕ NguonDongDto · NguonChungTuDto · TimNguonRequest
    │         ➕ XemDuLieuGhiSoRequest · DongButToanDto        (BR48 — D14)
    ├── entity/  ✅ DieuChinhGiaHangBan   ➕ ChiTietDieuChinhGiaHangBan
    ├── model/   ✅ 6 enum + MaDb + MaLoiDieuChinhGia   ➕ ThueSuatGtgt · LoaiDieuChinhHoaDon · LoaiChietKhau
    ├── repository/  ✅ 3 file   ➕ ChiTietRepository (nếu cần đọc riêng)
    └── service/
        ├── DieuChinhGiaHangBanCrudService.java    ✏️ đổi base class
        ├── DieuChinhGiaHangLoatService.java       ➕
        ├── NguonDieuChinhGiaService.java          ➕
        ├── XemDuLieuGhiSoService.java             ➕ (BR48)
        └── business/
            ├── DieuChinhGiaMapper.java            ✅ (mở rộng)
            ├── LuuDieuChinhGiaTemplate.java + Tao/Sua/Xoa/GhiSo/BoGhiSo/NhanBan   ➕
            ├── DinhKhoanDieuChinhGia.java · TinhToanDieuChinhGia.java · KiemTraDieuChinhGia.java   ➕
            └── LienKetNguonDieuChinhGia.java      ➕
```

---

## 4. Danh mục API mục tiêu

Base path **`/api/ban-hang/dieu-chinh-gia-hang-ban`** · Mã chức năng **`DieuChinhGiaHangBan`** · Mã loại chứng từ **`DCGB`**

| # | Nguồn | Method | Path | Quyền | Trạng thái | File con |
|---|---|---|---|---|---|---|
| A1 | base | POST | `/search` | `.View` | ✅ chạy | [01](01-xem-danh-sach.md) |
| A2 | base | GET | `/cot` | `.View` | ✅ chạy | [01](01-xem-danh-sach.md) |
| A3 | base | GET | `/{id}` | `.View.Detail` | 🟡 thiếu `chiTiet` | [02](02-xem-chi-tiet.md) |
| A4 | override | POST | `/them-moi` | `.Create` | ❌ **400 CHUA_HO_TRO** | [03](03-them-moi.md) |
| A5 | override | PUT | `/{id}` | `.Edit` | ❌ 400 | [04](04-chinh-sua.md) |
| A6 | override | DELETE | `/{id}` | `.Delete` | ❌ 400 | [05](05-xoa.md) |
| A7 | base | POST | `/{id}/ghi-so` | `.Post` | ❌ chưa có | [06](06-ghi-so.md) |
| A8 | base | POST | `/{id}/bo-ghi-so` | `.Unpost` | ❌ | [07](07-bo-ghi-so.md) |
| A9 | base | GET | `/{id}/dong-chi-tiet` | `.View.Detail` | ❌ | [02](02-xem-chi-tiet.md) |
| A10 | base | GET | `/{id}/thong-tin-hach-toan` | `.View.Detail` | ❌ | [02](02-xem-chi-tiet.md) |
| A11 | base | GET | `/{id}/nhan-ban` | `.Clone` ⚠ chưa seed | ❌ | [02](02-xem-chi-tiet.md) |
| A12-A14 | base | POST | `/ghi-so-hang-loat` · `/bo-ghi-so-hang-loat` · `/xoa-hang-loat` | `.Post`/`.Unpost`/`.Delete` | ❌ | [05](05-xoa.md), [06](06-ghi-so.md), [07](07-bo-ghi-so.md) |
| A15-A17 | mới | POST | `/nguon/search` · `/nguon/chung-tu` · `/nguon/chung-tu/{id}/dong` | `.Create` | ❌ | [08](08-chon-nguon-chung-tu.md) |
| **A18** | **mới (D14)** | POST | `/xem-du-lieu-ghi-so` | kế thừa quyền màn gọi (BR48.1) | ❌ | [06 §5](06-ghi-so.md) |
| — | base | POST | `/export`, `/import` | `.Export`/`.Import` | **403** cố ý | — |

⚠ **Đường dẫn thêm mới:** bản kế hoạch cũ ghi `POST /` (rỗng) theo FE. **Sinh đôi mua hàng dùng `POST /them-moi`** (đường dẫn chuẩn của base). Phải chốt một đường — §12-Q15.

**Envelope lỗi:** `ApiResponse` + `GlobalExceptionHandler`; lỗi nghiệp vụ ném `ApiException.badRequest/conflict(maLoi, messageId, chiTiet)`.

**Quy ước enum trên wire:** **TÊN HẰNG Java**, chuỗi xuống DB là `MaDb.maDb()` — đã cài và ghi rõ ở `package-info.java` của module. Lý do: bộ lọc động ép giá trị bằng `Enum.valueOf(name)`.

---

## 5. Ma trận UC → endpoint → tài liệu

| UC | Tên | Endpoint | File con | Tình trạng |
|---|---|---|---|---|
| PMKT-U-07665 | Xem danh sách | A1, A2 | 01 | ✅ |
| PMKT-U-07666 | Thêm mới | A4 (+A15-A17) | 03, 08 | ❌ |
| PMKT-U-07667 | Xem chi tiết | A3, A9, A10, A11 | 02 | 🟡 |
| PMKT-U-07668 | Xóa | A6, A14 | 05 | ❌ |
| PMKT-U-07669 | Ghi sổ | A7, A12 (+A18 BR48) | 06 | ❌ |
| PMKT-U-07670 | Bỏ ghi sổ | A8, A13 | 07 | ❌ |
| PMKT-U-07671 | Sửa | A5 | 04 | ❌ |

---

## 6. Luồng tổng thể

```mermaid
flowchart TD
    N[POST /nguon/search · /nguon/chung-tu · /{id}/dong] -->|D13: qua ChungTuBanHangNguonApi| F[FE dựng form]
    F --> C1[POST /them-moi · ghiSo=false]
    F --> C2[POST /them-moi · ghiSo=true]
    C1 --> T[ChungTuTemplate.thucThi]
    C2 --> T
    T --> V[kiemTraNghiepVu]
    V --> S[truocKhiLuu: TinhToan + SoChungTuApi.sinhSo]
    S --> L[luuEntity: header + chi tiết]
    L --> K[sauKhiLuu: QuanHeChungTuApi.lienKet + DinhKhoan]
    K --> G{ghiSo?}
    G -- không --> KY[kiemTraKyMo — BR17.1]
    G -- có --> GS[GhiSoApi.ghiSo]
    GS --> ST[trangThaiChungTu = DA_GHI_SO]
    ST -.-> BG[POST /{id}/bo-ghi-so] --> X[GhiSoApi.boGhiSo — xoá vật lý] --> Z[về CHUA_GHI_SO]
    F -.BR48.-> P[POST /xem-du-lieu-ghi-so<br/>chưa ghi sổ ⇒ tính tại chỗ · đã ghi sổ ⇒ đọc acc_so_cai]
```

---

## 7. Migration dự kiến

| # | Việc | Vì sao bắt buộc |
|---|---|---|
| 1 | **Bảng chi tiết → cột phẳng** (D6′): thêm `so_luong`, `don_gia`, `thanh_tien`, `chiet_khau_phan_tram`, `chiet_khau` + backfill + deprecate 10 cột `*_tang`/`*_giam` | LDM mới khai một bộ; giữ hai khối là mã hoá thừa cùng thông tin |
| 2 | Thêm 11 cột chi tiết còn thiếu (thuế enum, 3 cột quy đổi, cờ tờ khai, 4 chiều phân tích, `chung_tu_nguon_id`) | SCR + LDM có, DB chưa |
| 3 | Thêm cột header còn thiếu: 12 cột tab thanh toán/Hóa đơn + 2 cột chiết khấu header (D15) | 6 cột đã được thêm ở đợt trước — chỉ còn phần này |
| 4 | **Seed quy tắc đánh số cho DCGB nhánh Tăng giá** (L3) | thiếu ⇒ `QUY_TAC_KHONG_TON_TAI` khi Lưu chứng từ Tăng giá |
| 5 | Seed quyền `DieuChinhGiaHangBan.Clone` | không seed ⇒ nút Nhân bản 403 với mọi người |
| — | ~~DROP `trang_thai_chung_tu`~~ | **HUỶ** (D7) |
| — | ~~Seed `mst_loai_chung_tu` mã `CTDG`~~ | **HUỶ** — `DCGB` đã có (D11) |
| — | ~~2 index sắp xếp/lọc~~ | **ĐÃ CÓ** — `idx_sal_dcg_danh_sach`, `idx_sal_dcg_khach_hang` |

Đánh số: **`date +V%Y%m%d%H%M%S`**, prefix `sal_`. SQL đầy đủ: [09](09-thiet-ke-db.md) §10.

---

## 8. Thứ tự thực hiện

1. **Sửa L1 ngay** (xoá `@Searchable(path = "status")`) — 1 dòng, đang làm hỏng bộ lọc trạng thái của màn đang chạy.
2. Đọc **`dieu_chinh_gia_hang_mua/`** từ đầu đến cuối — đó là bản sinh đôi đã chạy được.
3. **Migration** (§7) → chạy Flyway trên DB dev, kiểm bằng `mcp__idea__execute_sql_query`.
4. `model/` bổ sung (`ThueSuatGtgt`, `LoaiDieuChinhHoaDon`, `LoaiChietKhau`) + unit test converter.
5. `entity/ChiTietDieuChinhGiaHangBan` + quan hệ cascade trên header + test pin whitelist `@Searchable`.
6. **Đổi base class** của controller + service (`BaseChungTuController` / `AbstractChungTuCrudService`), xoá 3 override ném 400 — làm **một lần, một commit**.
7. `business/`: `TinhToan` → `KiemTra` → `DinhKhoan` → `LienKetNguon` → `LuuTemplate` → `Tao/Sua/Xoa/GhiSo/BoGhiSo/NhanBan`.
8. `NguonDieuChinhGiaService` + **mở `chung_tu_ban_hang/api/ChungTuBanHangNguonApi`** (D13) — phối hợp với chủ module bán hàng.
9. `XemDuLieuGhiSoService` (A18, BR48).
10. `./gradlew unitTest` → smoke test trên DB dev qua IntelliJ → xuất Postman → PR.

**Phụ thuộc:** 09 (DB) chặn 5-9 · bước 6 chặn 7 · 08 (nguồn) làm song song được sau bước 3.

---

## 9. Rủi ro kỹ thuật

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| **R1** | Ghi sổ không sinh Phiếu thu/Chi và HĐĐT vì hai module đó chưa mở `api/` (D3) | **Cao** | §12-Q2; header đã có sẵn cột `phieu_thu_id`/… để module sau điền vào mà không đổi schema |
| **R2** | Công thức BR2 (SL chưa trả lại + quy đổi ĐVT) cần dữ liệu của `tra_lai_hang_ban` — module đó **có 14 file nhưng chưa có luồng ghi và chưa có `api/`** | **Cao** | D13: mở `api/` hai chiều; nếu chưa kịp thì tạm đọc `ctu_quan_he_chung_tu` qua `QuanHeChungTuApi.daTieuThu` và **ghi rõ sai số** — xem [08 §7-N1](08-chon-nguon-chung-tu.md) |
| **R3** | Đổi base class ở bước 6 làm gãy 3 endpoint đang trả 400 có kiểm soát | TB | Làm một commit riêng, chạy `unitTest` + smoke `/search` trước/sau |
| **R4** | Engine đánh số: quy tắc DCGB thiếu nhánh Tăng giá (L3) và lệch dạng giá trị `hinhThucThanhToan` (L4) | **Cao** | Chốt Q13/Q14 **trước** khi code F3; viết integration test cấp số cho cả 2 hướng × 2 hình thức |
| **R5** | Migration timestamp + `out-of-order` — nhánh sống lâu có thể chạy lệch thứ tự trên DB rỗng | TB | Renumber lúc rebase bằng `git mv` (§4.1 của luật đánh số) |
| **R6** | Không có Docker ⇒ test Testcontainers không chạy | TB | Cổng xanh là `./gradlew unitTest`; báo rõ phần chưa chạy |
| **R7** | `SoCaiApi` thiếu vế lọc `LoaiChungTuId` (L2) ⇒ A10/A18 có thể trộn bút toán của chứng từ khác loại trùng id | TB | Ticket cho `accounting_core`; test dựng 2 chứng từ khác loại cùng `chungTuId` để chứng minh |
| **R8** | Enum `ThueSuatGtgt` khai lại ở ≥2 module (D9) | Thấp | Test đồng bộ đọc CHECK constraint |

---

## 10. Quyền

| Mã quyền | Đã seed? | Dùng ở |
|---|---|---|
| `.View` · `.View.Detail` · `.Create` · `.Edit` · `.Delete` · `.Post` · `.Unpost` | ✅ `db/seed/iam_quyen_full_639_ba.sql` | A1-A10, A12-A18 |
| **`.Clone`** | ❌ **CHƯA** | A11 — phải seed, nếu không nút Nhân bản 403 với mọi người kể cả Admin |
| `.Export` / `.Import` | ❌ cố ý | endpoint kế thừa vẫn tồn tại nhưng 403 |

A18 **không có mã quyền riêng** — kế thừa quyền màn gọi (BR48.1).

---

## 11. Mã thông báo

Bảng 26 mã giữ nguyên như bản trước (lấy nguyên văn từ [6.messages.md](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/6.messages.md)) — file BA này **không đổi** trong đợt vừa rồi. Hằng đặt ở `MaLoiDieuChinhGia` (đã tồn tại).

Bổ sung 3 mã lỗi **của engine đánh số** mà module sẽ nhận và phải chuyển tiếp nguyên văn (không bọc lại):

| Mã lỗi engine | HTTP | Khi nào |
|---|---|---|
| `QUY_TAC_KHONG_TON_TAI` | 400 | chưa seed quy tắc cho tổ hợp (loại · hướng · hình thức TT) — L3 |
| `SO_KHONG_KHOP_QUY_TAC` (`MSG_PMKT-U-14741_025`) | 400 | người dùng gõ số không khớp mẫu và không tách lại được |
| `SO_CHUNG_TU_DA_TON_TAI` | **409** | BR19.1 — chặn, **không** nhảy số. ⚠ khác `MSG_109` (400) mà epic khai — §12-Q16 |

---

## 12. ⚠️ Điểm cần BA / Dev xác nhận

| # | Vấn đề | Bằng chứng | Xử lý tạm |
|---|---|---|---|
| ~~Q1~~ | ~~Mã loại chứng từ~~ | **ĐÃ TRẢ LỜI: `DCGB`** — [V1032:153](../../cell-app/src/main/resources/db/migration/V1032__tknd_va_cau_hinh_danh_so.sql) | đóng |
| **Q2** | Ghi sổ có phải sinh **Phiếu thu/Chi + HĐ điều chỉnh** ngay lần này? (nội dung đã đổi) | UC_GhiSo "Ràng buộc nguyên tử" liệt kê 6 tác động · `tien_mat_tien_gui` và `hoa_don_ban_hang` **đã có** nhưng **không có `api/`** ⇒ Modulith chặn | D3: chỉ bút toán + trạng thái. Nếu BA/PO bắt buộc ⇒ phải mở `api/` ở hai module đó **trước**, là việc của chủ module |
| **Q3** | `MSG_202` (HĐ đã ký phát hành) và `MSG_301` (trùng số HĐ theo KH) | `hoa_don_ban_hang` nay **đã có entity + `TrangThaiPhatHanh`** nhưng không có `api/` | cài `HoaDonDieuChinhPort` trong module mình, adapter mặc định trả "không có hóa đơn" |
| **Q4** | `MSG_105/106` (SL, ĐG > 0) vs dòng **Dịch vụ** (`SL = ĐG = 0`) | SCR dòng 582-583 vs 112-115 & 137-139 | miễn trừ cho dòng dịch vụ — **cùng cách FE đã code** |
| **Q5** | Hai câu thông báo của UC không có mã trong `6.messages.md` | UC_GhiSo (trùng số trước ghi sổ) · UC_BoGhiSo (cảnh báo xoá HĐĐT) | dùng lại `MSG_109`; câu bỏ ghi sổ là của FE |
| **Q6** | BR14 "Chiết khấu thương mại" tả hành vi cho ô không có trong bảng trường | SCR dòng 488-493 vs 444-465 | không cài |
| **Q7** | BR13 "ĐVT khác chuẩn ⇒ thêm trường quy đổi" — một dòng chữ | SCR dòng 487 · LDM **có** `DonViTinhChinhId` + `HeSoQuyDoi` | **LDM cụ thể hơn ⇒ theo LDM**, thêm 2 cột. Cần BA xác nhận |
| ~~Q8~~ | ~~"Thanh toán ngay" là cột riêng?~~ | **ĐÃ GIẢI QUYẾT** — cột `thanh_toan_ngay` đã tồn tại | đóng |
| **Q9** | "Phương thức điều chỉnh" vs "Loại điều chỉnh" (tab HĐ) | DB chỉ có `loai_dieu_chinh` (Tăng/Giảm) · LDM khai **cả hai**: `PhuongThucDieuChinh` + `LoaiDieuChinh` | thêm cột `loai_dieu_chinh_hoa_don` (§9.2) |
| **Q10** | SCR liệt kê BR lệch số +1 so với `business_rules.md` | SCR dòng 635-651 | đọc theo `business_rules.md` |
| **Q11** | **BR49** (di chuyển chứng từ trước–sau) BE có phải cấp endpoint không? | BR49.2 nói thứ tự "giống hệt màn danh sách" ⇒ FE tự suy từ trang đang cầm; nhưng chứng từ **đầu/cuối trang** thì FE phải gọi lại `/search` | tạm: **không** thêm endpoint, FE tự xử. Nếu BA muốn mượt tuyệt đối thì thêm `GET /{id}/lien-ke?huong=truoc|sau` |
| **Q12** | LDM có 6 trường **không có trong SCR**: `LoaiDongHang`, `SoLo`, `HanSuDung`, `NhomHHDVMuaVao`, `DienGiaiThue`, `LoaiVatTuId` | `ldm-DieuChinhGiaHangBan.puml` dòng 74, 111-113, 116-117 vs `SCR_ThemMoi` bảng lưới dòng 444-465 | **không cài lần này** (§1.2). Nếu BA xác nhận cần thì là một đợt cột mới |
| **Q13** | Quy tắc đánh số **DCGB nhánh Tăng giá** chưa seed (L3) | [V1032:1166-1169](../../cell-app/src/main/resources/db/migration/V1032__tknd_va_cau_hinh_danh_so.sql) — 4 dòng đều "Giảm giá hàng bán" | seed thêm 2-4 dòng "Tăng giá hàng bán – …"; **cần BA đặt tên quy tắc** cho khớp bộ chuẩn |
| **Q14** | Dạng giá trị trong `dieu_kien` của quy tắc đánh số: `CHI_TIEN_MAT` hay `ChiTienMat`? (L4) | V1032 dùng SCREAMING_SNAKE · CHECK bảng dùng PascalCase | **Dev kernel đánh số chốt.** Sai là chứng từ Thanh toán ngay không cấp được số |
| **Q15** | Đường dẫn thêm mới: `POST /` (FE đã khai) hay `POST /them-moi` (chuẩn base, sinh đôi mua hàng dùng) | `IMPLEMENT.md` dòng 181 vs [DieuChinhGiaMuaController.java:49](../../cell-app/src/main/java/vn/vtt/pmkt/cell/dieu_chinh_gia_hang_mua/internal/controller/DieuChinhGiaMuaController.java) | đề xuất **`/them-moi`** cho đồng bộ toàn repo; FE sửa 1 dòng trong `dieuChinhGiaApi.ts` |
| **Q16** | Trùng số chứng từ: epic khai `MSG_109` (400) nhưng engine ném `SO_CHUNG_TU_DA_TON_TAI` (**409**) | `6.messages.md` vs [SoChungTuApi javadoc](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/hach_toan/api/SoChungTuApi.java) | trả nguyên 409 của engine, gắn kèm `messageId = MSG_PMKT-E-07664_109` để FE hiển thị đúng câu |

---

## 13. Điều kiện nghiệm thu

### BA xác nhận
- [ ] Đủ 7 UC + form "Xem dữ liệu ghi sổ" (BR48) hai chế độ.
- [ ] Bốn kịch bản bút toán đúng SCR dòng 528-559 và UC_GhiSo.
- [ ] Trả lời Q2–Q7, Q9–Q16.

### Dev BE xác nhận
- [ ] L1 đã sửa; L2/L3/L4/L5 đã có ticket hoặc đã xử lý.
- [ ] Controller không gọi repository; Entity không lọt ra ngoài.
- [ ] Dùng lại `SearchRequest` · `PageResponse` · `QuyenChecker` · `GhiSoApi` · **`SoChungTuApi`** · `QuanHeChungTuApi` · **`TaiKhoanNgamDinhApi`**.
- [ ] Migration đặt tên bằng `date +V%Y%m%d%H%M%S`; `MigrationNamingArchTest` xanh.
- [ ] Module **0 vi phạm ranh giới Modulith**.
- [ ] `./gradlew unitTest` xanh; phần Testcontainers **báo rõ chưa chạy**.

---

## 14. Quy chuẩn nghiệp vụ (BR) áp dụng

Giữ nguyên bảng của bản trước, **thêm/sửa 5 dòng**:

| BR | Áp ở đâu |
|---|---|
| **BR04 / BR09 / BR10 / BR12 / BR19.1** (đánh số chứng từ) | **MỚI** — toàn bộ nằm sau `SoChungTuApi.sinhSo`/`thuHoi`; module không tự sinh số, không tự kiểm trùng |
| **BR12** Trạng thái chứng từ | `trangThaiChungTu` — enum nay đúng **2 giá trị** `CHUA_GHI_SO`/`DA_GHI_SO`, khớp BR12 |
| **BR48** Xem dữ liệu ghi sổ | **MỚI** — A18, hai chế độ (D14); ⚠ vế lọc `LoaiChungTuId` của BR48.3 hiện base chưa có (L2) |
| **BR49** Di chuyển chứng từ trước–sau | **MỚI** — §1.2, §12-Q11: FE xử lý, BE giữ nguyên thứ tự sắp xếp của A1 |
| **BR7 / BR18** | precision theo domain DB; cột `*_quy_doi` = gốc × tỷ giá |

Các BR còn lại (BR1, BR2, BR5, BR8, BR10, BR11, BR13, BR15, BR16, BR17, BR20, BR21, BR25, BR28, BR29, BR31, BR36, BR37, BR41, BR42, BR45, BR46) giữ nguyên như bản trước.

**BR chưa xử lý được:** BR38 · BR39 (quyền Excel không bật) · BR22/BR23/BR40 (danh mục cây) · BR32/BR44 (thuần FE) · BR47 (danh mục mặc định — không thuộc màn chứng từ) · phần sổ thuế/HĐĐT/phiếu thu-chi của BR36 (D3).

---

## 15. Tài liệu tham chiếu

- `pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/**`
- **`pmkt-docs/ba/Common/LDM_update/ldm-DieuChinhGiaHangBan.puml`** (mới — nguồn sự thật về hình dạng dữ liệu)
- `pmkt-docs/ba/Common/business_rules.md` — BR1…**BR49**
- `CLAUDE.md` · `cell-app/CLAUDE.md` · `docs/rules/be-khung-kien-truc-chuan.md` · `docs/rules/conventions.md` · **`docs/rules/migration-danh-so-theo-timestamp.md`**
- Mẫu code: **`cell/dieu_chinh_gia_hang_mua/`** (sinh đôi, đủ luồng) · `cell/chung_tu_ban_hang/` · `accounting_core/` · `core/`
- FE: `docs/doing/PMKT-E-07664-dieu-chinh-gia-hang-ban-fe/IMPLEMENT.md` + `client/src/features/banHang/dieuChinhGiaHangBan/api/model.ts`
