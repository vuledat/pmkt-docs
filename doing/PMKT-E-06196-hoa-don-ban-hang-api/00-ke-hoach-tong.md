# Kế hoạch triển khai API — Hóa đơn bán hàng (PMKT-E-06196)

> **Trạng thái:** `BẢN NHÁP CHỜ REVIEW` — F1 (danh sách) đã có code, F2–F6 (thêm/sửa/xóa/chi tiết/lập chứng từ) **chưa cài đặt**, controller chặn tường minh (xem §0-bis bên dưới).
> **Ngày cập nhật:** 2026-08-20 (rà soát lại lần 2 — đối chiếu commit BA `d23d1e20d`, `25f9a7ca6` ngày 17/08 + code Java hiện có; lần đầu 2026-08-14)
> **Người review cần có:** 1 BA (chốt §12) + 1 Dev BE/DBA (chốt §7, §9, §10)

| Mục | Nội dung |
|---|---|
| Use case | `PMKT-U-06456 DanhSach` · `PMKT-U-06457 ThemMoi` (thư mục `ThemMoi/`, BA chưa đánh mã — xem §12-Q1) · `PMKT-U-06466 ChiTiet` · `PMKT-U-06458 CapNhat` · `PMKT-U-06459 Xoa` |
| Màn hình | `SCR_HDBanHang_DanhSach.md` · `SCR_HDBanHang_ThemMoi.md` · `SCR_HDBanHang_ChiTiet.md` · `SCR_HDBanHang_CapNhat.md` · `SCR_HDBanHang_Xoa.md` |
| Tài liệu nguồn | `pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/` + `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_ThemMoi.md` (logic chuẩn) + `pmkt-docs/ba/Common/business_rules.md` |
| Module BE | `cell-app/src/main/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/` (**đã scaffold** — entity/dto/repository/controller/service của **F1 danh sách** đã có code; F2–F6 chưa cài, xem §0-bis) |
| Bảng DB | `sal_hoa_don_ban_hang` (**đã có, 57 cột**) · `sal_hoa_don_ban_hang_chi_tiet` (**đã có, 47 cột**) — thiếu 11 cột so với BA, xem [07-thiet-ke-db.md](07-thiet-ke-db.md) |

**Bộ file của kế hoạch này**

| File | Nội dung |
|---|---|
| `00-ke-hoach-tong.md` | file này — quyết định, phạm vi, kiến trúc, danh mục endpoint, rủi ro, câu hỏi BA |
| [`01-xem-danh-sach-hoa-don.md`](01-xem-danh-sach-hoa-don.md) | F1 — `POST /search`, `GET /cot`, `POST /export`; 9 cột BA, 2 cột dẫn xuất |
| [`02-them-moi-hoa-don.md`](02-them-moi-hoa-don.md) | F2 — `POST /them-moi`; toàn bộ tính toán CK/thuế/quy đổi + check trùng |
| [`03-xem-chi-tiet-hoa-don.md`](03-xem-chi-tiet-hoa-don.md) | F3 — `GET /{id}`; field điều khiển ẩn/hiện nút của FE |
| [`04-cap-nhat-hoa-don.md`](04-cap-nhat-hoa-don.md) | F4 — `PUT /{id}`; hệ quả BR02 khi HĐ đã lập chứng từ |
| [`05-xoa-hoa-don.md`](05-xoa-hoa-don.md) | F5 — `DELETE /{id}` + `POST /xoa-hang-loat` |
| [`06-lap-chung-tu-tu-hoa-don.md`](06-lap-chung-tu-tu-hoa-don.md) | F6 — nạp dữ liệu HĐ sang màn CTBH + đồng bộ `TrangThaiLapChungTu` |
| [`07-thiet-ke-db.md`](07-thiet-ke-db.md) | migration `V3`, cột thêm mới, sửa CHECK, sửa unique index |

---

## 0-bis. Cập nhật so với code hiện tại (rà soát 2026-08-20)

Chạy lại `/plan-be` vì tài liệu BA của epic đổi sau ngày sinh plan lần đầu (14/08), qua hai commit
17/08 trong `pmkt-docs`:

- `d23d1e20d` — "đồng bộ tên entity ldm - scr field": đổi cách viết tên field BA từ bí danh
  `HoaDonBan.X` sang tên bảng/entity chuẩn LDM `sal_hoa_don_ban_hang.X` (và `mst_mau_so_hoa_don`,
  `sal_hoa_don_ban_hang_chi_tiet`) trong `5.screens/SCR_HDBanHang_DanhSach.md`,
  `5.screens/SCR_HDBanHang_ThemMoi.md`, `Matrix/…/SCR_HDBanHang_ThemMoi_MaTranAnHien.md`.
- `25f9a7ca6` — "gom mô tả sinh bút toán về BR20…": phía 06196 chỉ sửa 2 dòng ghi chú (bỏ "Tab Hạch
  toán" khỏi danh sách tab bị lược trong `Matrix/…/_scope.md` và
  `SCR_HDBanHang_ThemMoi_MaTranAnHien.md`) vì màn Hóa đơn **không có** tab này.

**Kết luận: cả hai commit đều là chuẩn hóa CÁCH VIẾT tài liệu, KHÔNG đổi logic/trường/luật nghiệp
vụ nào của 06196.** Đối chiếu cụ thể:

| # | Điểm kiểm | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | Code Java (`HoaDonBanHang.java`, `HoaDonBanHangDto.java`) có dùng tên field/bảng sai chuẩn LDM không? | **KHÔNG có drift.** Entity đã `@Table(name = "sal_hoa_don_ban_hang")` và mọi `@Column` map đúng snake_case của bảng thật (vd `so_hoa_don`, `ngay_hoa_don`, `trang_thai_lap_chung_tu`…) theo đúng quy ước Java (`cell-app/CLAUDE.md` §Đặt tên), độc lập với việc tài liệu BA gọi bảng bằng bí danh `HoaDonBan` hay tên chuẩn `sal_hoa_don_ban_hang` — hai cách viết chỉ là bề mặt tài liệu, quy về cùng một bảng/cột vật lý. | `cell-app/src/main/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/internal/entity/HoaDonBanHang.java:21,37,44,55,69` |
| 2 | Code có giả định sai "Hóa đơn có Tab Hạch toán" không? | **KHÔNG.** Entity kế thừa `AggregateRootEntity` chứ không `BaseChungTuEntity` (đúng D2 §0), không có field/logic ghi sổ, không import `hach_toan`/`GhiSoApi`; comment ở `package-info.java` và entity nói rõ "không có ghi sổ/bỏ ghi sổ". Controller cũng chưa cài luồng ghi nào có thể sinh bút toán. | `cell-app/src/main/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/package-info.java:8-12` · `internal/entity/HoaDonBanHang.java:23-27` · `internal/controller/HoaDonBanHangController.java:70-88` |
| 3 | Plan cũ (00, 01, 07) có trích dẫn `file:dòng` bằng bí danh `HoaDonBan.X` đã lỗi thời không? | **CÓ, đã sửa trong bản này** — thuần túy cập nhật cách trích dẫn cho khớp tài liệu BA mới nhất, không đổi bất kỳ quyết định/thiết kế nào. | Xem danh sách sửa bên dưới |
| 4 | Plan cũ có giả định "Tab Hạch toán" ở đâu không? | **KHÔNG** — grep toàn bộ `docs/doing/PMKT-E-06196-hoa-don-ban-hang-api/*.md` cũ không có chuỗi "Tab Hạch toán". D2 (§0) đã đúng ngay từ đầu: Hóa đơn không hạch toán. | — |
| 5 | Package Java trong plan cũ đúng chưa? | **SAI, đã sửa trong bản này** — 5 chỗ ở `00-ke-hoach-tong.md` và `06-lap-chung-tu-tu-hoa-don.md` ghi package `vn.dopai.pmkt…` (theo `CLAUDE.md` gốc, đã lỗi thời), trong khi code thật và `cell-app/CLAUDE.md` dùng `vn.vtt.pmkt`. Lỗi này **không liên quan** hai commit BA — là sai sót còn sót lại từ lần sinh plan đầu. | `cell-app/src/main/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/package-info.java:1` (thực tế) so với `00-ke-hoach-tong.md:12,94,241,505` và `06-lap-chung-tu-tu-hoa-don.md:210` (cũ) |
| 6 | Phạm vi code đã cài so với 6 chức năng (F1–F6) trong plan? | Chỉ **F1 (xem danh sách)** có code chạy được (`HoaDonBanHangController` kế thừa `BaseCrudController` cho `search`/`cot`/`{id}`/`export`). **F2 (thêm mới), F4 (cập nhật), F5 (xóa)** bị chặn tường minh — `create()`/`update()`/`delete()` override ném `ApiException.badRequest(MaLoiHoaDonBanHang.CHUA_HO_TRO, …)`. **F3 (chi tiết)** dùng chung endpoint `GET /{id}` của base nhưng response DTO đầy đủ 41 field (`HoaDonBanHangDto`) kể cả phần "chỉ có nghĩa cho Thêm/Sửa" — cần đối chiếu lại với `03-xem-chi-tiet-hoa-don.md` khi cài thật. **F6 (lập chứng từ từ hóa đơn)** chưa có endpoint nào. | `internal/controller/HoaDonBanHangController.java:70-88` |

**Sửa cụ thể trong lần rà soát này** (đổi bí danh field, không đổi nội dung/quyết định):

| File | Vị trí | Trước | Sau |
|---|---|---|---|
| `00-ke-hoach-tong.md` | dòng mermaid "Chiều 2" | `HoaDonBan.TrangThaiLapChungTu` | `sal_hoa_don_ban_hang.TrangThaiLapChungTu` |
| `00-ke-hoach-tong.md` | bảng migration `V3` mục 1 | `HoaDonBan.ChungTuBanId` | `sal_hoa_don_ban_hang.ChungTuBanId` |
| `01-xem-danh-sach-hoa-don.md` | bảng "Ánh xạ cột BA ↔ DB ↔ DTO" (mục 2–9) | `HoaDonBan.NgayHoaDon`, `.SoHoaDon`, `.TenKhachHang`, `.TrangThaiLapChungTu`, `.TrangThaiPhatHanh`, `.TongThueGTGT`/`.TongThueGTGTQuyDoi`, `.TrangThaiHoaDon` | đổi tiền tố `HoaDonBan.` → `sal_hoa_don_ban_hang.` cho toàn bộ 7 dòng |
| `07-thiet-ke-db.md` | bảng "Cột thiếu" — cột `chung_tu_ban_id` | `HoaDonBan.ChungTuBanId`; trích `SCR_CTBH_ThemMoi.md:1305` | `sal_hoa_don_ban_hang.ChungTuBanId`; trích dòng đã cập nhật `SCR_CTBH_ThemMoi.md:1436` (số dòng đổi vì tài liệu 06194 đã được viết lại nhiều đợt kể từ 14/08) |
| `00-ke-hoach-tong.md` · `06-lap-chung-tu-tu-hoa-don.md` | 5 chỗ package Java | `vn.dopai.pmkt…` | `vn.vtt.pmkt…` |

Không sửa gì khác trong §0 (quyết định D1–D9), §1 (phạm vi), §3–§11: nội dung nghiệp vụ của các mục
này vẫn đúng với BA mới nhất, chỉ là cách trích dẫn field cần cập nhật.

---

## 0. Các quyết định đã chốt

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Tạo **module Modulith mới** `cell/hoa_don_ban_hang/` với tiền tố bảng `sal_` (dùng chung tiền tố với `chung_tu_ban_hang` vì hai bảng đã mang tiền tố `sal_` từ baseline — `V1__baseline.sql:16795`, `:16874`). KHÔNG nhét vào `chung_tu_ban_hang/`. | Thư mục mới + `package-info.java` khai `@ApplicationModule`. `chung_tu_ban_hang` không phải sửa gì trừ việc gỡ chú thích "module Hoá đơn chưa có" ở `ChiTietChungTuBanHang.java:213`. Ranh giới Modulith phải **sạch tuyệt đối** (cell-app/CLAUDE.md §Ranh giới). |
| **D2** | Kế thừa **`core.controller.BaseCrudController`**, **KHÔNG** kế thừa `accounting_core.chung_tu.controller.BaseChungTuController`. | Hóa đơn bán hàng **không hạch toán** (`UC_HDBanHang_ThemMoi.md:20`, `SCR_HDBanHang_ThemMoi.md:69`) → không có ghi sổ/bỏ ghi sổ/số chứng từ/kỳ khóa. Bảng `sal_hoa_don_ban_hang` cũng **không có** cột `so_chung_tu`/`ngay_hach_toan`/`status`/`loai_chung_tu_id` mà `BaseChungTuEntity` đòi (đối chiếu `sal_dieu_chinh_hoa_don_ban_hang` — `V1__baseline.sql:16738-16747` — thì CÓ). **Vì sao không chọn `BaseChungTuController`:** nó sẽ lộ ra `/ghi-so`, `/bo-ghi-so`, `/nhan-ban` — 3 endpoint vô nghĩa với chứng từ thương mại, và ép entity mang 8 cột không tồn tại trong DB. |
| **D3** | Entity `HoaDonBanHang extends core.entity.AggregateRootEntity` (`core/entity/AggregateRootEntity.java:18`), chi tiết là `@OneToMany(cascade = ALL, orphanRemoval = true)` — **không** có repository riêng cho dòng chi tiết. | Bảng đã có `phien_ban integer DEFAULT 1 NOT NULL` (`V1__baseline.sql:16845`) đúng hợp đồng `@Version` của lớp này. Sửa chỉ chạm dòng con vẫn phải `touch()` header (mẫu: `ChungTuBanHang.java:32-36`). |
| **D4** | Phần **GHI** (thêm/sửa/xóa) **override toàn bộ** `AbstractCrudService`, đi qua 4 template `TaoHoaDonBan`/`SuaHoaDonBan`/`XoaHoaDonBan` + `LuuHoaDonBanTemplate`. Phần **ĐỌC** (search/cột/chi tiết/export) dùng nguyên base. | Cùng kiến trúc lai của `ChungTuBanHangCrudService.java:28-33`. Lý do: thứ tự "validate trùng → tính lại tiền → kiểm số lượng nguồn → lưu → cập nhật liên kết/counter" là bất biến, `AbstractCrudService.create` chỉ biết `repository.save`. |
| **D5** | Toàn bộ **tính toán tiền** (thành tiền, chiết khấu 4 loại, thuế GTGT, thuế XK, quy đổi tỷ giá) **tính lại ở BE khi lưu**, không tin số FE gửi lên — trừ các trường BA cho phép sửa tay (`Tiền thuế GTGT`, `Tiền thuế XK`, `Giá trị tính thuế XK`, các cột quy đổi) thì **giữ nguyên giá trị client gửi**. | `TinhToanHoaDonBan` là lớp thuần JVM, test `@Tag("unit")`. Danh sách chính xác trường nào tính lại / trường nào tôn trọng client: [02-them-moi-hoa-don.md §4](02-them-moi-hoa-don.md). **Vì sao không tính toàn bộ ở BE:** `SCR_CTBH_ThemMoi.md:695-701` (BR11 mục 5) và `:855-865` (BR14) nói rõ người dùng sửa tay cột quy đổi/thuế thì **không tính ngược**, ghi đè hết là làm sai BA. |
| **D6** | **KHÔNG viết lại** logic tính toán của `chung_tu_ban_hang` — copy có chọn lọc sang `TinhToanHoaDonBan` của module mới thay vì import chéo. | `chung_tu_ban_hang/internal/service/business/TinhToanBanHang.java` nằm trong `internal/` → import chéo là vi phạm Modulith. Tách chung ra `accounting_core` cũng sai vì HĐ không hạch toán. Trùng lặp có kiểm soát ~200 dòng, chấp nhận và ghi vào §11-R4. |
| **D7** | Liên kết **HĐ ↔ chứng từ** đi qua `quan_he_chung_tu.api.QuanHeChungTuApi` (`quan_he_chung_tu/api/QuanHeChungTuApi.java:36`), **không** tự viết bảng liên kết. Riêng chiều **HĐ là nguồn của CTBH** hiện `LoaiChungTu.SAL_CHUNG_TU_BAN_HANG(true, false)` (`LoaiChungTu.java:19`) chưa cho phép làm đích → phải mở rộng enum + CHECK constraint. | Migration `V3` sửa `ck_ctu_qhct_loai_dich`; enum sửa thành `SAL_CHUNG_TU_BAN_HANG(true, true)`. Chi tiết + rủi ro: [06-lap-chung-tu-tu-hoa-don.md](06-lap-chung-tu-tu-hoa-don.md), §11-R2. |
| **D8** | `TrangThaiLapChungTu` của hóa đơn dùng **3 giá trị** `Chưa lập` / `Đã lập 1 phần` / `Đã lập đủ` theo `SCR_HDBanHang_DanhSach.md:61-63`, **không** dùng 2 giá trị của CHECK constraint hiện tại. | Migration `V3` phải `DROP` rồi `ADD` lại `sal_hoa_don_ban_hang_trang_thai_lap_chung_tu_check` + backfill dữ liệu cũ. Xem [07-thiet-ke-db.md §2](07-thiet-ke-db.md). **Xung đột nội bộ tài liệu BA** — `UC_HDBanHang_ThemMoi.md:39` và `SCR_HDBanHang_ThemMoi.md:96` lại nói 2 giá trị (`"Chưa lập chứng từ"` / `"Đã lập chứng từ"`) → §12-Q2. |
| **D9** | **Phát hành hóa đơn điện tử NGOÀI phạm vi.** Trường `trang_thai_phat_hanh_hoa_don` chỉ được BE set = `"Chưa phát hành"` lúc tạo, và chỉ **đọc** để chặn Sửa/Xóa. | Quyền `LapHoaDonBan.PhatHanh` đã seed (`db/seed/iam_quyen_full_639_ba.sql:650`) nhưng **không** có endpoint nào dùng lần này. `SCR_HDBanHang_ThemMoi.md:7`: "chưa kết nối API CQT để phát hành (sẽ triển khai sau)". |
| **D10** | **Không mở `POST /import`.** `cotMacDinh(LoaiMau.IMPORT)` trả `List.of()` → base tự trả 400 `IMPORT_NOT_SUPPORTED` (`BaseCrudController.java:113-116`). Mở `POST /export`. | Cùng lý do với `ChungTuBanHangController.java:183-185`. Quyền `.Export` **chưa seed** cho `LapHoaDonBan` → migration `V3` phải seed, nếu không mọi user kể cả Admin nhận 403 (§10). |
| **D11** | Hai chiều **HĐ→CTBH** và **CTBH→HĐ** là **hai counter khác nhau**, không gộp. `sal_chung_tu_ban_hang_chi_tiet.so_luong_da_xuat_hd` (`ChiTietChungTuBanHang.java:204`) là counter của chiều CTBH→HĐ; `TrangThaiLapChungTu` của hóa đơn là chiều HĐ→CTBH. | Hai luồng nghiệp vụ độc lập, xem sơ đồ §6. Nhầm hai chiều này là lỗi thiết kế đắt nhất của epic — ghi rõ vào §11-R1. |

> ⚠️ **Cảnh báo môi trường:** `db/migration/` vừa bị **squash về `V1__baseline.sql` + `V2__seed_toan_cuc.sql`** (ngày file: 2026-08-13). Thư mục `db/rollback/` vẫn còn file tới `V340__…` — **đó là lịch sử cũ, không phải migration đang chạy**. Số hiệu migration mới là **`V3`**, không phải `V341`. Đọc lại `ls db/migration/` ngay trước khi code.

---

## 1. Phạm vi

### 1.1 Trong phạm vi

| # | Chức năng | Nguồn | File chi tiết |
|---|---|---|---|
| **F1** | Xem danh sách HĐ — tìm kiếm động, phân trang, sắp xếp, xuất Excel | `UC_HDBanHang_DanhSach.md` · `SCR_HDBanHang_DanhSach.md` | [01](01-xem-danh-sach-hoa-don.md) |
| **F2** | Thêm mới HĐ (header + N dòng chi tiết), check trùng, tính tiền | `UC_HDBanHang_ThemMoi.md` · `SCR_HDBanHang_ThemMoi.md` | [02](02-them-moi-hoa-don.md) |
| **F3** | Xem chi tiết HĐ (readonly) | `UC_HDBanHang_ChiTiet.md` · `SCR_HDBanHang_ChiTiet.md` | [03](03-xem-chi-tiet-hoa-don.md) |
| **F4** | Cập nhật HĐ (chỉ khi "Chưa phát hành") + hệ quả BR02 | `UC_HDBanHang_CapNhat.md` · `SCR_HDBanHang_CapNhat.md` | [04](04-cap-nhat-hoa-don.md) |
| **F5** | Xóa mềm 1 HĐ + xóa hàng loạt (lỗi từng phần) | `UC_HDBanHang_Xoa.md` · `SCR_HDBanHang_Xoa.md` | [05](05-xoa-hoa-don.md) |
| **F6** | Nạp dữ liệu HĐ để lập Chứng từ bán hàng + đồng bộ `TrangThaiLapChungTu` | `UC_HDBanHang_DanhSach.md:41-46` · `SCR_HDBanHang_DanhSach.md:70-77` (BR04) | [06](06-lap-chung-tu-tu-hoa-don.md) |
| — | Migration `V3` + seed quyền `.Export` | §10, [07](07-thiet-ke-db.md) | [07](07-thiet-ke-db.md) |

### 1.2 NGOÀI phạm vi (không cài lần này)

| Việc bị loại | Nguồn | Endpoint có lộ ra không |
|---|---|---|
| **Phát hành hóa đơn điện tử** (chuyển `Chưa phát hành` → `Đã phát hành`, kết nối CQT) | `SCR_HDBanHang_ThemMoi.md:7` nói rõ "sẽ triển khai sau"; epic không có UC nào cho việc này | Không có endpoint. `trangThaiPhatHanh` luôn = `"Chưa phát hành"` với mọi HĐ tạo qua API này. |
| **Lập Chứng từ bán dịch vụ từ HĐ** (BR05 màn danh sách — `SCR_HDBanHang_DanhSach.md:79-86`) | Module Java `chung_tu_ban_dich_vu` **chưa tồn tại** (`ls cell/` chỉ có `chung_tu_ban_hang`, `chung_tu_mua_hang`) dù bảng `sal_chung_tu_ban_dich_vu` đã có ở baseline | BE **có** trả `coDongDichVu: boolean` trong DTO danh sách để FE ẩn/hiện nút, nhưng **không** có endpoint nạp dữ liệu. Bấm nút → FE tự mở màn CTBDV khi module đó ra đời. §12-Q6. |
| **Hóa đơn điều chỉnh / thay thế** (`BR06`, `BR07` màn danh sách — `SCR_HDBanHang_DanhSach.md:88-104`) | Là epic riêng **PMKT-E-06197** (`V1__baseline.sql:16760` — comment bảng `sal_dieu_chinh_hoa_don_ban_hang` ghi rõ "PMKT-E-06197"). Bảng "hóa đơn thay thế" **chưa tồn tại** trong DB. | Cột `trangThaiHoaDon` và `hoaDonLienQuan` **có** trong response danh sách nhưng lần này BE chỉ suy được **3/5** giá trị (`Hóa đơn gốc`, `Hóa đơn bị điều chỉnh`, `Hóa đơn điều chỉnh`); hai giá trị `thay thế` luôn không xuất hiện. §12-Q3. |
| **Nhập Excel** | Chưa có thiết kế mẫu file | `POST /import` **có** (kế thừa base) nhưng trả `400 IMPORT_NOT_SUPPORTED` — `BaseCrudController.java:113-116`. |
| **Popup phân bổ chiết khấu** (`SCR_CTBH_PBCK.md`, `SCR_CTBH_PBCK_MHHD.md`) | Tính toán phân bổ chạy **hoàn toàn ở FE**; BE chỉ nhận `tienChietKhau` từng dòng đã phân bổ xong và validate tổng | Không có endpoint. Validate `MSG_PMKT-E-06196_017`, `_018` vẫn chạy ở BE — [02 §5](02-them-moi-hoa-don.md). |
| **Nhân bản hóa đơn** | Epic không có UC nhân bản; `6.messages.md` không cấp mã nào | Không có endpoint (khác `BaseChungTuController` — xem D2). |

---

## 2. Hiện trạng đã khảo sát

### 2.1 Code hiện có — **GREENFIELD ở tầng Java**

```bash
cd cell-app/src/main/java && grep -rln "HoaDon" --include="*.java" . | grep -v master_data
```
Kết quả (đã bỏ `master_data/**` — vùng đóng băng):

| File | Liên quan gì |
|---|---|
| `chung_tu_ban_hang/internal/entity/ChiTietChungTuBanHang.java:213-215` | `@Column(name = "hoa_don_ban_hang_id")` kèm comment **"module Hoá đơn chưa có — hiện luôn null"** |
| `chung_tu_ban_hang/internal/model/TrangThaiHoaDon.java:12-14` | Enum 3 giá trị `Chưa lập` / `Đã lập một phần` / `Đã lập đủ` — **của CTBH**, không phải của HĐ (xem D11) |
| `common/constant/MaChucNang.java:220` | `public static final String LAP_HOA_DON_BAN = "LapHoaDonBan";` — hằng đã có sẵn |
| `quan_he_chung_tu/api/LoaiChungTu.java:25` | `SAL_HOA_DON_BAN_HANG(true, true)` — HĐ đã được khai là vừa nguồn vừa đích |

```bash
find cell-app/src/main/java/vn/vtt/pmkt/cell -maxdepth 1 -type d
```
→ `accounting_core, chung_tu_ban_hang, chung_tu_mua_hang, common, core, integration_ops, master_data, platform_iam, quan_he_chung_tu, reporting`

**Kết luận:** **không có** entity / repository / service / controller nào cho hóa đơn bán hàng. Toàn bộ tầng Java là greenfield. Tầng DB thì **brownfield** (§2.2).

### 2.2 Hiện trạng DB — **BROWNFIELD**

```bash
ls cell-app/src/main/resources/db/migration/
# V1__baseline.sql  V2__seed_toan_cuc.sql
```
**Số hiệu migration lớn nhất hiện tại: `V2` ⇒ file mới là `V3`.** (`db/rollback/` còn file `V340` nhưng đó là lịch sử trước đợt squash — xem cảnh báo ở §0.)

| Bảng | Vai trò | Vị trí | Trạng thái |
|---|---|---|---|
| `sal_hoa_don_ban_hang` | header HĐ, 57 cột, có RLS + audit trigger | `V1__baseline.sql:16795-16858` | **đã có** — thiếu 4 cột, sai 2 CHECK, sai 1 unique index |
| `sal_hoa_don_ban_hang_chi_tiet` | dòng HĐ, 47 cột | `V1__baseline.sql:16874-16923` | **đã có** — thiếu 7 cột |
| `sal_chung_tu_ban_hang` / `…_chi_tiet` | chứng từ bán hàng, counter `so_luong_da_xuat_hd` | `V1__baseline.sql:15965`, `:16113` | đã có, module Java đã có |
| `sal_dieu_chinh_hoa_don_ban_hang` | hóa đơn điều chỉnh (**PMKT-E-06197**) | `V1__baseline.sql:16706` | đã có bảng, **chưa có module Java** |
| `ctu_quan_he_chung_tu` | đồ thị liên kết nguồn↔đích | module `quan_he_chung_tu` | đã có, phải mở rộng CHECK (D7) |
| `mst_mau_so_hoa_don` | danh mục mẫu số hóa đơn | `V1__baseline.sql:11687` | đã có (thuộc `master_data` — chỉ tham chiếu `id`, không đọc code) |

Ràng buộc đã có trên `sal_hoa_don_ban_hang`:

| Loại | Định nghĩa | Vị trí | Đánh giá |
|---|---|---|---|
| unique | `(tenant_id, khach_hang_id, so_hoa_don, COALESCE(ky_hieu_hoa_don,''), COALESCE(mau_so_hoa_don_id,'000…'))  WHERE da_xoa=false AND so_hoa_don<>''` | `V1:23675` | ❌ **SAI so với BR03** — thừa `khach_hang_id`, xem §12-Q4 |
| index | `(tenant_id, ngay_hoa_don)` | `V1:21813` | ✅ dùng cho sort mặc định |
| index | `(tenant_id, hoa_don_ban_hang_id)` trên bảng chi tiết | `V1:21771` | ✅ |
| RLS | `tenant_id = fn_current_tenant()` + `FORCE ROW LEVEL SECURITY` | `V1:31708`, `:31715` | ✅ BR28 |
| trigger | `fn_audit()` AFTER INSERT/UPDATE/DELETE | `V1:25446`, `:25495` | ✅ |
| CHECK | `trang_thai_lap_chung_tu IN ('Chưa lập chứng từ','Đã lập chứng từ')` | `V1:16856` | ❌ thiếu giá trị thứ 3 (D8) |
| CHECK | `loai_nghiep_vu IN ('Bán hàng trong nước','Bán hàng xuất khẩu')` | `V1:16855` | ❌ thiếu `'Bán dịch vụ'` — xem §12-Q5 |

### 2.3 Hạ tầng base đã có sẵn những gì

| Cần | Đã có ở base | Vị trí |
|---|---|---|
| 8 endpoint chuẩn (`/search`, `/cot`, `GET /{id}`, `/them-moi`, `PUT /{id}`, `DELETE /{id}`, `/export`, `/import`) | `BaseCrudController<E,D,C,U>` | `core/controller/BaseCrudController.java:121,131,137,143,149,159,171,197` |
| Body tìm kiếm chuẩn `{page,pageSize,sort,keyword,filters,logic}` | `SearchRequest` record | `core/request/SearchRequest.java:33` |
| Envelope danh sách `{data,pagination,summary}` | `PageResponse<T>` | `core/response/PageResponse.java:21` |
| Envelope thành công `{data,message,messageId}` | `ApiResponse<T>` | `core/response/ApiResponse.java:22` |
| Envelope lỗi `{error:{code,message,messageId,details}}` | `ApiError` + `GlobalExceptionHandler` | `core/shared/error/ApiError.java:11` · `core/config/GlobalExceptionHandler.java:29` |
| Lọc/sắp xếp động theo whitelist, tự bơm `tenant_id` + `da_xoa=false` | `DynamicSpecification` (`MAX_FILTERS=20`) | `core/shared/search/DynamicSpecification.java:51,75,78` |
| Whitelist cột cho filter/sort/keyword | `@Searchable` | `core/shared/search/Searchable.java:36` |
| Tìm không dấu (BR11.1) | `bo_dau()` SQL function qua `unaccentLower` | `core/shared/search/DynamicSpecification.java:234-240` |
| Kiểm quyền `View/View.Detail/Create/Edit/Delete/Export` | `QuyenChecker` | gọi ở `core/controller/BaseCrudController.java:123,139,145,151,163,176` |
| Lock lạc quan `@Version` | `AggregateRootEntity.phienBan` | `core/entity/AggregateRootEntity.java:21-22` |
| Kiểm token lock từ client (`updatedAt` → 409 `STALE_DATA`) | mẫu `BanHangSupport.kiemTraLock` | `chung_tu_ban_hang/internal/service/business/BanHangSupport.java:120-130` |
| Xuất Excel toàn bộ bản ghi sau lọc | `ExcelExporter` + `cotMacDinh(LoaiMau.EXPORT)` | `core/controller/BaseCrudController.java:171-190` |
| Dòng tổng toàn cục (BR31) | `AbstractCrudService.summary(SearchRequest)` | mẫu `chung_tu_ban_hang/internal/service/ChungTuBanHangCrudService.java:191-195` |
| Đồ thị liên kết chứng từ + guard xóa + đếm số lượng đã tiêu thụ | `QuanHeChungTuApi` | `quan_he_chung_tu/api/QuanHeChungTuApi.java:36,46,54,57,60,69` |
| Kiểu số chuẩn BR7 | DOMAIN `money_vnd(18,2)`, `quantity(18,3)`, `percent_rate(5,2)`, `exchange_rate(18,6)` | `V1__baseline.sql:73,94,80,48` |
| Enum ⇄ chuỗi tiếng Việt trong DB | `GiaTriDb` + `GiaTriDb.Converter` | `chung_tu_ban_hang/internal/model/GiaTriDb.java` (**copy sang module mới** — D6) |

**Không viết lại:** phân trang, lọc động, sort đa cột, export Excel, envelope, RLS, audit trigger, đồ thị quan hệ chứng từ.

---

## 3. Kiến trúc

### 3.1 Phân tầng

```
HoaDonBanHangController                    extends core.controller.BaseCrudController
  │  + POST /xoa-hang-loat  (mới)
  │  + POST /lookup         (mới — bộ giá trị enum cho combo)
  │  + GET  /{id}/du-lieu-lap-chung-tu (mới — F6)
  ▼
HoaDonBanHangCrudService                   extends core.service.AbstractCrudService
  │  ├── kế thừa : search() · moTaCot() · duLieuExport()
  │  ├── override: get() (nạp kèm chi tiết) · create() · update() · delete() · summary() · defaultSortAlias()
  │  └── cài mới : xoaHangLoat() · duLieuLapChungTu()
  ▼
service/business/  LuuHoaDonBanTemplate · TaoHoaDonBan · SuaHoaDonBan · XoaHoaDonBan
                   KiemTraHoaDonBan · TinhToanHoaDonBan · TrangThaiHoaDonBan
                   HoaDonBanMapper · HoaDonBanSupport
  ▼
HoaDonBanHangRepository                    extends core.repository.BaseRepository<HoaDonBanHang, UUID>
  + HoaDonBanHangRepositoryCustom/Impl     (query tổng hợp §6.4 của file 01)
  ▼
HoaDonBanHang (@Table "sal_hoa_don_ban_hang")     extends core.entity.AggregateRootEntity
  └─ @OneToMany ChiTietHoaDonBanHang (@Table "sal_hoa_don_ban_hang_chi_tiet")
```

### 3.2 Lựa chọn kiến trúc + lý do

| Tiêu chí | Phương án A — nhét vào `chung_tu_ban_hang/` | Phương án B — kế thừa `BaseChungTuController` | **Phương án C (CHỌN) — module mới + `BaseCrudController`** |
|---|---|---|---|
| Ranh giới Modulith | Vỡ: 2 aggregate root khác nhau trong 1 module, HĐ phải import `internal/` của CTBH | Sạch | Sạch — module mới, ranh giới đủ điều kiện "sạch tuyệt đối" ngay từ ngày đầu |
| Khớp DB | — | ❌ `BaseChungTuEntity` đòi `so_chung_tu`, `ngay_hach_toan`, `status`, `loai_chung_tu_id`, `chi_nhanh_id` — bảng `sal_hoa_don_ban_hang` **không có cột nào** trong số đó (`V1:16795-16858`) | ✅ `AggregateRootEntity` chỉ đòi `id`, `tenant_id`, `phien_ban`, audit, `da_xoa` — bảng có đủ |
| Endpoint thừa | — | ❌ lộ `/ghi-so`, `/bo-ghi-so`, `/nhan-ban`, `/thong-tin-hach-toan` cho một chứng từ không hạch toán | ✅ đúng 8 endpoint + 3 endpoint riêng |
| Chi phí | Thấp nhất | Trung bình | **Cao nhất** — phải copy ~200 dòng tính toán từ `TinhToanBanHang` (D6) |
| Rủi ro | Sửa CTBH có thể làm vỡ HĐ và ngược lại | Endpoint chết gây hiểu nhầm cho FE | Trùng lặp code tính toán ⇒ **chốt an toàn:** test đối chiếu song song `TinhToanHoaDonBanTest` dùng chung bộ case với `TinhToanBanHangTest` (§16 của file 02) |

### 3.3 Cấu trúc thư mục (Modulith, đúng `cell-app/CLAUDE.md`)

```
cell/hoa_don_ban_hang/
├── package-info.java                    @ApplicationModule(displayName = "hoa_don_ban_hang")
└── internal/                            KHÔNG tạo api/ — chưa module nào cần gọi vào (§12-Q6)
    ├── controller/
    │   └── HoaDonBanHangController.java            (package-private)
    ├── dto/
    │   ├── HoaDonBanHangDto.java                    (chi tiết + danh sách)
    │   ├── ChiTietHoaDonBanHangDto.java
    │   ├── LuuHoaDonBanHangRequest.java             (dùng chung Thêm & Sửa — D4)
    │   ├── LuuChiTietHoaDonBanHangRequest.java
    │   ├── TongHopHoaDonBanDto.java                 (dòng tổng — BR31)
    │   ├── XoaHangLoatRequest.java
    │   ├── KetQuaXoaHangLoatDto.java
    │   └── DuLieuLapChungTuDto.java                 (F6)
    ├── entity/
    │   ├── HoaDonBanHang.java
    │   └── ChiTietHoaDonBanHang.java
    ├── model/
    │   ├── GiaTriDb.java                            (copy — D6)
    │   ├── LoaiNghiepVuHoaDon.java
    │   ├── LoaiChietKhauHoaDon.java
    │   ├── HinhThucThanhToanHoaDon.java
    │   ├── ThueSuatGtgtHoaDon.java
    │   ├── TrangThaiPhatHanh.java
    │   ├── TrangThaiLapChungTu.java
    │   ├── TrangThaiHoaDonKind.java                 (BR06 — Hóa đơn gốc/điều chỉnh/…)
    │   └── MaLoiHoaDonBan.java
    ├── port/
    │   └── DongHoaDonBanPort.java                   (cắm vào quan_he_chung_tu — D7)
    ├── repository/
    │   ├── HoaDonBanHangRepository.java
    │   ├── HoaDonBanHangRepositoryCustom.java
    │   └── HoaDonBanHangRepositoryImpl.java
    └── service/
        ├── HoaDonBanHangCrudService.java
        ├── HoaDonBanHangHangLoatService.java
        └── business/
            ├── HoaDonBanSupport.java
            ├── LuuHoaDonBanTemplate.java
            ├── TaoHoaDonBan.java · SuaHoaDonBan.java · XoaHoaDonBan.java
            ├── LenhHoaDonBan.java
            ├── KiemTraHoaDonBan.java
            ├── TinhToanHoaDonBan.java
            ├── TrangThaiHoaDonBan.java
            ├── HoaDonBanMapper.java
            └── SoTienHoaDon.java
```

Test đặt song ánh: `src/test/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/internal/service/business/…`

---

## 4. Danh mục API mục tiêu

Base path: **`/api/ban-hang/hoa-don-ban-hang`**. Mã chức năng: **`LapHoaDonBan`** (`common/constant/MaChucNang.java:220`).

| # | Nguồn | Method | Path | Quyền | Trả về | UC | File |
|---|---|---|---|---|---|---|---|
| **A1** | base | `POST` | `/search` | `.View` | `PageResponse<HoaDonBanHangDto>` | U-06456 | [01](01-xem-danh-sach-hoa-don.md) |
| **A2** | base | `GET` | `/cot` | `.View` | `ApiResponse<List<CotMoTa>>` | U-06456 | [01](01-xem-danh-sach-hoa-don.md) |
| **A3** | base | `POST` | `/export` | `.Export` ⚠ chưa seed | file `.xlsx` | U-06456 (BR39) | [01](01-xem-danh-sach-hoa-don.md) |
| **A4** | mới | `POST` | `/lookup` | `.View` | `ApiResponse<Map<String,List<String>>>` | U-06457 | [02](02-them-moi-hoa-don.md) |
| **A5** | base (override messageId) | `POST` | `/them-moi` | `.Create` | `201 ApiResponse<HoaDonBanHangDto>` | U-06457 | [02](02-them-moi-hoa-don.md) |
| **A6** | base (override nạp chi tiết) | `GET` | `/{id}` | `.View.Detail` | `ApiResponse<HoaDonBanHangDto>` | U-06466 | [03](03-xem-chi-tiet-hoa-don.md) |
| **A7** | base (override messageId) | `PUT` | `/{id}` | `.Edit` | `ApiResponse<HoaDonBanHangDto>` | U-06458 | [04](04-cap-nhat-hoa-don.md) |
| **A8** | base (override messageId) | `DELETE` | `/{id}` | `.Delete` | `ApiResponse<Void>` | U-06459 | [05](05-xoa-hoa-don.md) |
| **A9** | mới | `POST` | `/xoa-hang-loat` | `.Delete` | `ApiResponse<KetQuaXoaHangLoatDto>` | U-06459 | [05](05-xoa-hoa-don.md) |
| **A10** | mới | `GET` | `/{id}/du-lieu-lap-chung-tu` | `.View.Detail` | `ApiResponse<DuLieuLapChungTuDto>` | U-06456 (BR04) | [06](06-lap-chung-tu-tu-hoa-don.md) |
| — | base | `POST` | `/import` | `.Import` | `400 IMPORT_NOT_SUPPORTED` | — | ngoài phạm vi (D10) |

**Envelope thành công:** `{"data": …, "message": "…", "messageId": "MSG_PMKT-E-06196_00x"}` (`core/response/ApiResponse.java:22`).
**Envelope danh sách:** `{"data": [...], "pagination": {page,pageSize,totalItems,totalPages}, "summary": {...}}` (`core/response/PageResponse.java:21`).
**Envelope lỗi:** `{"error": {"code": "…", "message": "…", "messageId": "MSG_PMKT-E-06196_0xx", "details": [{field, message}]}}` (`core/shared/error/ApiError.java:11`).

**Quy ước enum trên wire:** dùng **chuỗi tiếng Việt đúng như lưu trong DB** (vd `"Bán hàng trong nước"`, `"Chưa phát hành"`), dùng chung cho cả `filters` lẫn `data`. Lý do: các chuỗi này nằm trong `CHECK` constraint của bảng (`V1:16853-16857`), lệch một dấu là không lưu được và lỗi chỉ lộ lúc COMMIT — hệt lý do đã ghi ở `ChungTuBanHangController.java:163-165`. `POST /lookup` (A4) trả bộ giá trị hợp lệ để FE không hardcode.

---

## 5. Ma trận UC → endpoint → tài liệu

| UC | Tên | Endpoint | Màn hình | File chi tiết |
|---|---|---|---|---|
| `PMKT-U-06456` | Xem danh sách HĐ | A1, A2, A3, A10 | `SCR_HDBanHang_DanhSach` | 01, 06 |
| `ThemMoi` (chưa có mã — §12-Q1) | Thêm mới HĐ | A4, A5 | `SCR_HDBanHang_ThemMoi` | 02 |
| `PMKT-U-06466` | Xem chi tiết HĐ | A6 | `SCR_HDBanHang_ChiTiet` | 03 |
| `PMKT-U-06458` | Cập nhật HĐ | A6 (nạp) + A7 (lưu) | `SCR_HDBanHang_CapNhat` | 04 |
| `PMKT-U-06459` | Xóa HĐ | A8, A9 | `SCR_HDBanHang_Xoa` | 05 |

Mọi UC trong `4.usecases/` xuất hiện đúng 1 lần. Không UC nào bị bỏ.

---

## 6. Luồng tổng thể — hai chiều liên kết (D11)

```mermaid
flowchart LR
  subgraph Chieu1["Chiều 1 — CTBH sinh ra HĐ (đã có ở PMKT-E-06194)"]
    CT1[Chứng từ bán hàng<br/>đã ghi sổ] -->|Lập hóa đơn| HD1[Hóa đơn bán hàng]
    HD1 -.->|cộng counter| C1["sal_chung_tu_ban_hang_chi_tiet<br/>so_luong_da_xuat_hd"]
    C1 -.->|suy ra| S1["ChungTuBan.TrangThaiLapHoaDon<br/>(TrangThaiHoaDon.java:12-14)"]
  end
  subgraph Chieu2["Chiều 2 — HĐ sinh ra CTBH (F6, lần này)"]
    HD2[Hóa đơn bán hàng] -->|Lập chứng từ bán hàng| CT2[Chứng từ bán hàng mới]
    CT2 -.->|cộng lượng đã tiêu thụ| C2["ctu_quan_he_chung_tu<br/>(dòng HĐ → dòng CTBH)"]
    C2 -.->|suy ra| S2["sal_hoa_don_ban_hang.TrangThaiLapChungTu<br/>Chưa lập / Đã lập 1 phần / Đã lập đủ"]
  end
```

Luồng lưu một hóa đơn (F2/F4):

```mermaid
sequenceDiagram
  participant FE
  participant C as HoaDonBanHangController
  participant S as HoaDonBanHangCrudService
  participant T as LuuHoaDonBanTemplate
  participant K as KiemTraHoaDonBan
  participant Q as QuanHeChungTuApi
  participant R as Repository
  FE->>C: POST /them-moi (header + N dòng)
  C->>C: quyen.require("LapHoaDonBan", CREATE)
  C->>S: create(command)
  S->>T: thucThi(Lenh.Luu)
  T->>K: kiểm bắt buộc + trùng HĐ (BR03) + CK + số lượng/đơn giá
  T->>T: TinhToanHoaDonBan — tính lại tiền dòng & tổng header (D5)
  alt HĐ lập từ CTBH nguồn
    T->>Q: lienKet(...) — kiểm SL ≤ SL còn lại, khoá dòng nguồn FOR UPDATE
    Q-->>T: VuotSoLuongNguonException → MSG_PMKT-E-06196_019
  end
  T->>R: save(aggregate) — cascade dòng chi tiết
  T-->>C: HoaDonBanHangDto
  C-->>FE: 201 {data, message, messageId: MSG_PMKT-E-06196_001}
```

---

## 7. Migration dự kiến

**`V3__sal_hoa_don_ban_hang_bo_sung_cot.sql`** (số hiệu = max hiện tại `V2` + 1). Nội dung đầy đủ + SQL chạy được: [07-thiet-ke-db.md §5](07-thiet-ke-db.md). Tóm tắt:

| # | Việc | Vì sao bắt buộc |
|---|---|---|
| 1 | Thêm 4 cột header: `tong_tien_thue_xk`, `tong_tien_thue_xk_quy_doi`, `trang_thai_hoa_don`, `chung_tu_ban_id` | `SCR_HDBanHang_ThemMoi.md:54` (Tổng thuế XK) · `SCR_HDBanHang_DanhSach.md:121` (`TrangThaiHoaDon`) · `:108` (`sal_hoa_don_ban_hang.ChungTuBanId`) |
| 2 | Thêm 7 cột chi tiết: `dien_giai`, `dien_giai_thue`, `khong_tong_hop_to_khai_gtgt`, `chiet_khau_hang_phan_tram`, `chiet_khau_hoa_don_phan_tram`, `gia_tri_tinh_thue_xk`, `gia_tri_tinh_thue_xk_quy_doi` | `SCR_HDBanHang_ThemMoi.md:44-45` · `SCR_CTBH_ThemMoi.md:234-235` (BR12d) · `:236-237` (BR14) |
| 3 | Sửa CHECK `trang_thai_lap_chung_tu` → 3 giá trị + backfill | D8, `SCR_HDBanHang_DanhSach.md:61-63` |
| 4 | Sửa CHECK `loai_nghiep_vu` → thêm `'Bán dịch vụ'` | `SCR_HDBanHang_ThemMoi.md:21` (HĐ lập kèm kế thừa `LoaiNghiepVu` của chứng từ nguồn) — chờ §12-Q5 |
| 5 | **Thay** `uq_sal_hdbh_so_hd` — bỏ `khach_hang_id` khỏi khóa unique | BR03 (`SCR_HDBanHang_ThemMoi.md:89`) — chờ §12-Q4, **có bước kiểm dữ liệu trùng trước** |
| 6 | Sửa CHECK `ck_ctu_qhct_loai_dich` — cho `SAL_CHUNG_TU_BAN_HANG` làm đích | D7, F6 |
| 7 | Seed quyền `LapHoaDonBan.Export` | Endpoint A3 kế thừa base gọi `quyen.require(…, EXPORT)`; chưa seed → 403 với **mọi** user kể cả Admin |
| 8 | Sửa `fn_bang_cua_loai_chung_tu`: `'SAL_HOA_DON_BAN_HANG'` đang trả tên bảng chi tiết **`sal_chi_tiet_hd_ban_hang`** nhưng bảng thật tên `sal_hoa_don_ban_hang_chi_tiet` | `V1__baseline.sql:313` vs `:16874` — bảng `sal_chi_tiet_hd_ban_hang` **không tồn tại** trong baseline. Xem §11-R3 |

---

## 8. Thứ tự thực hiện

1. **Đọc lại** `ls db/migration/` + chữ ký `AbstractCrudService`, `BaseCrudController` (cảnh báo §0).
2. **Migration `V3`** + seed quyền `.Export` → chạy Flyway trên DB dev (`SPRING_FLYWAY_ENABLED=true` một lượt) → chạy các query kiểm dữ liệu ở [07 §6](07-thiet-ke-db.md).
3. `model/` — 8 enum + `MaLoiHoaDonBan` + `GiaTriDb` → unit test pin giá trị chuỗi DB.
4. `entity/` + whitelist `@Searchable` → unit test pin whitelist (9 cột danh sách).
5. `repository/` — `BaseRepository` + `…RepositoryImpl.tongHop(spec)`.
6. `service/business/` — `TinhToanHoaDonBan` → `KiemTraHoaDonBan` → `TrangThaiHoaDonBan` → `HoaDonBanMapper` → 3 template. **Unit test song song từng lớp** (đây là phần dày nhất).
7. `service/` — `HoaDonBanHangCrudService`, `HoaDonBanHangHangLoatService`.
8. `controller/` + `port/DongHoaDonBanPort` + mở rộng `LoaiChungTu`.
9. F6 (`06-lap-chung-tu-tu-hoa-don.md`) — **làm sau cùng**, phụ thuộc bước 8 và migration mục 6.
10. `./gradlew unitTest` → smoke-test trên DB dev (RLS, unique index, cascade) → xuất Postman → PR.

**Phụ thuộc giữa các file con:** 02 là gốc (tính toán + validate) — 03, 04, 05 dùng lại. 01 độc lập. 06 phụ thuộc 02 (entity) và migration mục 6.

---

## 9. Rủi ro kỹ thuật

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| **R1** | **Nhầm hai chiều liên kết** (D11): lập trình viên cộng `so_luong_da_xuat_hd` của CTBH khi HĐ sinh ra CTBH, hoặc ngược lại. Hệ quả: số lượng còn lại sai, cho xuất trùng. | **Cao** | Đặt tên tường minh (`daXuatHoaDon` vs `daLapChungTu`); unit test riêng cho từng chiều; sơ đồ §6 dán vào javadoc của `TrangThaiHoaDonBan`. |
| **R2** | `LoaiChungTu.SAL_CHUNG_TU_BAN_HANG` đang là `(true, false)` — nguồn-only. Đổi thành `(true, true)` **có test đồng bộ đọc `pg_constraint`** (`LoaiChungTu.java:8-11`) → sửa enum mà quên sửa CHECK là **đỏ build**, sửa CHECK mà quên enum là lỗi runtime ở production. | **Cao** | Sửa cả hai trong cùng một PR; migration mục 6 và enum đi cùng commit; chạy đúng test đồng bộ đó qua IntelliJ trước khi push (test này cần DB → không nằm trong `unitTest`). |
| **R3** | `fn_bang_cua_loai_chung_tu('SAL_HOA_DON_BAN_HANG', true)` trả `'sal_chi_tiet_hd_ban_hang'` — **bảng không tồn tại** (`V1:313` vs `:16874`). Bất cứ chỗ nào (audit, ghi sổ, báo cáo) dùng hàm này với loại HĐ sẽ lỗi `relation does not exist` lúc chạy. | **Trung bình** | Sửa trong `V3` (mục 8 của §7). Trước khi sửa, `grep -rn "fn_bang_cua_loai_chung_tu" cell-app/src` để biết ai đang gọi. |
| **R4** | Trùng lặp ~200 dòng logic tính tiền giữa `TinhToanHoaDonBan` và `TinhToanBanHang` (D6) — sửa một bên quên bên kia. | Trung bình | Test đối chiếu dùng chung bộ case; javadoc hai lớp trỏ chéo nhau; ghi vào `docs/` mục nợ kỹ thuật. |
| **R5** | Sửa `uq_sal_hdbh_so_hd` (bỏ `khach_hang_id`) có thể **thất bại** nếu DB dev/prod đã có 2 HĐ cùng (số + ký hiệu + mẫu số) khác khách hàng. | Trung bình | Query kiểm trước ([07 §6](07-thiet-ke-db.md)); nếu có trùng → **báo BA**, không tự xóa. Chờ §12-Q4. |
| **R6** | Module `chung_tu_ban_dich_vu` chưa tồn tại → BR05 màn danh sách không nghiệm thu được đầy đủ. | Thấp | Đã tuyên bố ngoài phạm vi (§1.2); BE vẫn trả `coDongDichVu` để FE dựng nút. |
| **R7** | **Môi trường:** máy dev không có Docker → mọi test Testcontainers (~25 lớp) không chạy được; `./gradlew build` luôn đỏ. Cổng xanh thực tế là `./gradlew unitTest`. | Trung bình | Báo cáo hoàn thành phải **ghi rõ** phần tích hợp chưa chạy. Test cần DB thật chạy qua IntelliJ (`mcp__idea__execute_run_configuration`). |
| **R8** | Module mới phải **sạch tuyệt đối** về ranh giới Modulith (`cell-app/CLAUDE.md`), trong khi repo còn 96 vi phạm cũ. `ProxyModularityTest` chỉ soi vi phạm nhắc tới module mình → module mới bị soi 100%. | Thấp | Chỉ import `core.*`, `common.*`, `quan_he_chung_tu.api.*` (đã có `@NamedInterface`). **Tuyệt đối không** import `chung_tu_ban_hang.internal.*`. |

---

## 10. Quyền — BR25

Mã chức năng: `LapHoaDonBan` (`common/constant/MaChucNang.java:220`).

| Quyền | Endpoint | Đã seed chưa | Vị trí seed |
|---|---|---|---|
| `LapHoaDonBan.View` | A1, A2, A4 | ✅ | `V2__seed_toan_cuc.sql:577` · `db/seed/iam_quyen_full_639_ba.sql:375` |
| `LapHoaDonBan.View.Detail` | A6, A10 | ✅ | `V2__seed_toan_cuc.sql:578` · seed:376 |
| `LapHoaDonBan.Create` | A5 | ✅ | `V2__seed_toan_cuc.sql:579` · seed:372 |
| `LapHoaDonBan.Edit` | A7 | ✅ | seed:374 |
| `LapHoaDonBan.Delete` | A8, A9 | ✅ | seed:373 |
| `LapHoaDonBan.Export` | **A3** | ❌ **CHƯA SEED** | phải thêm ở `V3` — nếu không, `POST /export` trả **403 cho mọi user kể cả Admin** |
| `LapHoaDonBan.PhatHanh` | — | ✅ (seed:650) | **không dùng lần này** (D9) |

Hành vi khi thiếu quyền (BR25.2): `QuyenChecker` ném 403; FE hiển thị `MSG_PMKT-E-06196_011` "Không có quyền truy cập".

---

## 11. Mã thông báo (nguyên văn `6.messages.md`)

| Hằng `MaLoiHoaDonBan` | messageId | Nội dung (nguyên văn) | Dùng ở |
|---|---|---|---|
| `MSG_TAO_THANH_CONG` | `MSG_PMKT-E-06196_001` | Thêm mới Hóa đơn thành công | A5 |
| `MSG_CAP_NHAT_THANH_CONG` | `MSG_PMKT-E-06196_002` | Cập nhật Hóa đơn thành công | A7 |
| `MSG_XOA_THANH_CONG` | `MSG_PMKT-E-06196_003` | Xóa hóa đơn bán hàng thành công | A8 |
| `MSG_TRUNG_HOA_DON` | `MSG_PMKT-E-06196_006` | Hóa đơn đã tồn tại ({soHD}-{kyHieuHD}-{mauSoHD}) | A5, A7 |
| `MSG_THIEU_DONG_CHI_TIET` | `MSG_PMKT-E-06196_007` | Phải có ít nhất 1 dòng chi tiết hàng hóa | A5, A7 |
| `MSG_SO_LUONG_AM` | `MSG_PMKT-E-06196_009` | Số lượng không được âm | A5, A7 |
| `MSG_DA_PHAT_HANH_KHONG_XOA` | `MSG_PMKT-E-06196_010` | Hóa đơn đã phát hành, không được xóa | A8, A9 |
| `MSG_KHONG_CO_QUYEN` | `MSG_PMKT-E-06196_011` | Không có quyền truy cập | mọi endpoint (403) |
| `MSG_KHONG_TIM_THAY` | `MSG_PMKT-E-06196_012` | Hóa đơn không tồn tại | A6, A7, A8, A10 (404) |
| `MSG_LOI_HE_THONG` | `MSG_PMKT-E-06196_013` | Lỗi hệ thống | 500 |
| `MSG_PHAN_TRAM_CK_VUOT_100` | `MSG_PMKT-E-06196_015` | % Chiết khấu không được vượt quá 100% | A5, A7 |
| `MSG_TIEN_CK_VUOT_THANH_TIEN` | `MSG_PMKT-E-06196_016` | Tiền CK không được vượt quá thành tiền của dòng | A5, A7 |
| `MSG_TONG_CK_KHONG_KHOP` | `MSG_PMKT-E-06196_017` | Tổng tiền chiết khấu các dòng không khớp với tổng tiền chiết khấu của hóa đơn | A5, A7 |
| `MSG_TONG_TY_LE_PHAN_BO` | `MSG_PMKT-E-06196_018` | Tổng tỷ lệ phân bổ phải bằng 100% | A5, A7 |
| `MSG_VUOT_SL_XUAT_HD` | `MSG_PMKT-E-06196_019` | Số lượng xuất hóa đơn ({soLuong_nhap}) vượt quá số lượng còn lại được phép xuất ({soLuong_con_lai}) cho mặt hàng {maHang} | A5, A7 |
| `MSG_DON_GIA_AM` | `MSG_PMKT-E-06196_020` | Đơn giá không được âm | A5, A7 |
| `MSG_XOA_THAT_BAI` | `MSG_PMKT-E-06196_033` | Xóa hóa đơn thất bại | A8, A9 |
| `MSG_XAC_NHAN_XOA` | `MSG_PMKT-E-06196_027` | Bạn có chắc chắn muốn xóa hóa đơn bán hàng này không? | **FE only** |
| `MSG_KET_QUA_XOA_HANG_LOAT` | `MSG_PMKT-E-06196_054` | Xóa thành công {x}/{n} hóa đơn. {y} hóa đơn đã phát hành không được xóa. | A9 |
| `MSG_CANH_BAO_XOA_DA_LAP_CT` | `MSG_PMKT-E-06196_055` | Hóa đơn này đã được lập chứng từ bán hàng/dịch vụ. Việc thay đổi/xóa hóa đơn có thể ảnh hưởng đến số liệu chứng từ. Bạn có chắc chắn muốn tiếp tục? | **FE only** — BE cấp cờ `daLapChungTu` ở A6 |
| `MSG_CANH_BAO_SUA_DA_LAP_CT` | `MSG_PMKT-E-06196_056` | Hóa đơn này đã được lập chứng từ bán hàng/dịch vụ. Việc thay đổi mã khách hàng, mã hàng sẽ làm mất liên kết giữa hóa đơn và chứng từ, đồng thời thay đổi trạng thái của chứng từ. Nếu thêm mới mặt hàng, trạng thái lập chứng từ của hóa đơn sẽ bị thay đổi. Bạn có chắc chắn muốn tiếp tục? | **FE only** — BE cấp cờ `daLapChungTu` ở A6 |

⚠️ `6.messages.md` **không có mã** cho: "Hóa đơn đã lập chứng từ, không được xóa" (BR ở `UC_HDBanHang_Xoa.md:55` chỉ ghi "hiển thị thông báo lỗi") → §12-Q7. Tuyệt đối **không bịa mã mới**.

---

## 12. ⚠️ Điểm cần BA xác nhận

| # | Vấn đề | Bằng chứng mâu thuẫn (cả hai phía) | Xử lý tạm để code tiếp |
|---|---|---|---|
| **Q1** | UC Thêm mới **chưa có mã `PMKT-U-xxxxx`** — thư mục tên trần `ThemMoi/`, trong khi 4 UC còn lại đều có mã. | Có mã: `4.usecases/PMKT-U-06458_CapNhat/`, `PMKT-U-06459_Xoa/`, `PMKT-U-06466_ChiTiet/`, `PMKT-u-06456_DanhSach/`. Không mã: `4.usecases/ThemMoi/`. (Bonus: `PMKT-u-06456` viết thường chữ `u`.) | Dùng nhãn `ThemMoi` trong tài liệu; **không** bịa mã. BA cấp mã thì sửa §5. |
| **Q2** | `TrangThaiLapChungTu` có **2 hay 3** giá trị? | **3 giá trị:** `SCR_HDBanHang_DanhSach.md:61-63` — "Chưa lập" / "Đã lập 1 phần" / "Đã lập đủ"; `SCR_HDBanHang_CapNhat.md:40` — "thuộc 'Đã lập 1 phần' hoặc 'Đã lập đủ'"; `SCR_HDBanHang_DanhSach.md:47` — nút Lập CT hiện khi ∈ {"Chưa lập","Đã lập 1 phần"}. **2 giá trị:** `UC_HDBanHang_ThemMoi.md:39` — `TrangThaiLapChungTu = "Chưa lập chứng từ"`; `SCR_HDBanHang_ThemMoi.md:96` — 'chỉ chuyển "Đã lập chứng từ" khi HĐ được chọn vào một CTBH'; **DB CHECK** `V1__baseline.sql:16856` cũng chỉ có 2. | **Chọn 3 giá trị** (D8) vì màn Danh sách + Cập nhật là nơi dùng thật và nói rõ ngưỡng "1 phần". Migration `V3` mở CHECK. Nếu BA chốt 2 → bỏ mục 3 của §7 và đơn giản hóa `TrangThaiHoaDonBan`. |
| **Q3** | Cột **"Trạng thái hóa đơn"** (BR06) có 5 giá trị nhưng DB chỉ đỡ được 3. | BA: `SCR_HDBanHang_DanhSach.md:90-95` — 5 giá trị gồm `Hóa đơn thay thế` / `Hóa đơn bị thay thế`. DB: chỉ có `sal_dieu_chinh_hoa_don_ban_hang` (`V1:16706`, comment ghi **PMKT-E-06197**) + cột `da_bi_dieu_chinh boolean` (`V1:16836`) — **không có bảng/cột nào cho "thay thế"**. | Lần này BE suy được 3 giá trị (`Hóa đơn gốc` / `Hóa đơn bị điều chỉnh` / `Hóa đơn điều chỉnh`). Hai giá trị "thay thế" **luôn không xuất hiện** cho tới khi có epic tương ứng. Xác nhận có chấp nhận nghiệm thu một phần không. |
| **Q4** | **Khóa check trùng hóa đơn** có gồm khách hàng không? | BA: `SCR_HDBanHang_ThemMoi.md:89` — "Số hóa đơn + Ký hiệu hóa đơn + Mẫu số hóa đơn trong cùng 1 tenant"; `SCR_CTBH_ThemMoi.md:576` (BR06b) nói y hệt. DB: `uq_sal_hdbh_so_hd` (`V1:23675`) unique trên **`(tenant_id, khach_hang_id, so_hoa_don, ky_hieu, mau_so)`** — **có** `khach_hang_id`. | **Theo BA** — bỏ `khach_hang_id` (chặt hơn). Migration mục 5 của §7 kèm query kiểm dữ liệu trùng. Nếu DB đang có dữ liệu vi phạm → dừng, báo BA (R5). |
| **Q5** | `LoaiNghiepVu` của hóa đơn có nhận giá trị `"Bán dịch vụ"` không? | Có: `SCR_HDBanHang_ThemMoi.md:21` — "Hóa đơn **lập kèm** từ chứng từ nguồn thì **kế thừa** `LoaiNghiepVu` của chứng từ đó", mà `SCR_CTBH_ThemMoi.md:1422` khai `LoaiNghiepVu` có 3 giá trị gồm `Bán dịch vụ`. Không: cùng dòng `:21` nói HĐ lập trực tiếp "chỉ chọn giữa *Bán hàng trong nước* và *Bán hàng xuất khẩu*"; **DB CHECK** (`V1:16855`) chỉ có 2 giá trị. | Mở CHECK lên 3 giá trị (migration mục 4) nhưng `POST /lookup` chỉ trả 2 giá trị cho màn lập trực tiếp. Nếu BA chốt HĐ không bao giờ mang `Bán dịch vụ` → bỏ mục 4 của §7. |
| **Q6** | Nút **"Lập chứng từ bán dịch vụ"** (`SCR_HDBanHang_DanhSach.md:79-86`) — làm gì khi module CTBDV chưa tồn tại? | BA yêu cầu nút hiển thị khi HĐ có ≥1 dòng "Dịch vụ". Code: không có module `chung_tu_ban_dich_vu` trong `cell/`; bảng `sal_chung_tu_ban_dich_vu` đã có (`V1__baseline.sql`, FK ở `:28113`). | BE trả cờ `coDongDichVu` để FE dựng nút; bấm vào chưa có đích. Xác nhận: **ẩn nút** hay **hiện nhưng báo "chưa hỗ trợ"**? |
| **Q7** | Xóa HĐ **đã lập chứng từ** — chặn hay cảnh báo rồi cho xóa? Và dùng mã message nào? | Chặn: `UC_HDBanHang_Xoa.md:71` — "`TrangThaiLapChungTu = 'Đã lập chứng từ'` → **KHÔNG được xóa**"; `:55` — "Không cho phép xóa, hiển thị thông báo lỗi" (**không cấp mã**). Cho xóa: `SCR_HDBanHang_Xoa.md:81-82` (BR10) — "nội dung cảnh báo đổi thành **MSG_055**… Nếu người dùng vẫn tiếp tục chọn Yes: **Hệ thống thực hiện xóa hóa đơn**, mọi liên kết bị gỡ bỏ". | **Theo `SCR_HDBanHang_Xoa.md` BR10** (cụ thể hơn, là màn phụ trách xóa): cho xóa kèm gỡ liên kết. `UC` chặn thì cần một mã lỗi mới mà `6.messages.md` không có. Chi tiết: [05-xoa-hoa-don.md §5](05-xoa-hoa-don.md). |
| **Q8** | `MSG_PMKT-E-06196_054` viết "**{y} hóa đơn đã phát hành** không được xóa" — nhưng lý do bỏ qua còn có "đã lập chứng từ". | `6.messages.md:37` chỉ nhắc lý do "đã phát hành". `SCR_HDBanHang_Xoa.md:55` yêu cầu bảng kết quả có cột **"Lý do lỗi"** cho từng dòng. | BE trả `KetQuaXoaHangLoatDto` có `lyDo` từng dòng; FE dùng `_054` cho câu tóm tắt. Xác nhận có cần sửa nguyên văn `_054` không. |
| **Q9** | Trường **"Loại nghiệp vụ"** của hóa đơn có được sửa sau khi lưu không? | `SCR_HDBanHang_ThemMoi.md:21`: HĐ lập kèm "kế thừa… và **không cho sửa**". `SCR_HDBanHang_CapNhat.md:16-17`: màn Cập nhật "tham chiếu **đầy đủ** các trường của Thêm mới" — tức mặc định cho sửa. `SCR_CTBH_ThemMoi.md:1437`: chứng từ "đã lưu **không đổi được** `LoaiNghiepVu`". | Chặn sửa `loaiNghiepVu` ở `PUT /{id}` khi HĐ có `chungTuBanId ≠ null` (lập kèm). HĐ lập trực tiếp thì cho đổi giữa trong nước ↔ xuất khẩu. Xác nhận. |

---

## 13. Điều kiện nghiệm thu

### BA xác nhận
- [ ] Danh sách đủ 9 cột `SCR_HDBanHang_DanhSach.md:21-29`, sort mặc định ngày HĐ giảm dần (`UC_HDBanHang_DanhSach.md:11`).
- [ ] Nút Sửa/Xóa/Lập chứng từ ẩn/hiện đúng điều kiện — BE cấp đủ field cờ ([01 §5.3](01-xem-danh-sach-hoa-don.md)).
- [ ] 9 luật validate của `SCR_HDBanHang_ThemMoi.md:109-119` đều chặn được, đúng mã message.
- [ ] Xóa hàng loạt trả đủ dữ liệu dựng bảng "Danh sách không xóa được" (`SCR_HDBanHang_Xoa.md:49-55`).
- [ ] Đã chốt Q1…Q9.

### Dev BE xác nhận
- [ ] Controller không gọi repository; Entity không lọt ra ngoài Controller.
- [ ] Dùng lại `SearchRequest` / `DynamicSpecification` / `PageResponse` / `ApiResponse` / `QuyenChecker` / `ExcelExporter` / RLS thay vì tự viết.
- [ ] Mọi filter/sort whitelist bằng `@Searchable`; `tenant_id` và `da_xoa` không nhận từ client.
- [ ] Mọi handler gọi `quyen.require(...)`.
- [ ] Không hardcode magic value; enum ⇄ chuỗi DB qua converter.
- [ ] Không N+1: chi tiết nạp bằng `@EntityGraph`, dòng tổng là query aggregate riêng.
- [ ] Module mới **0 vi phạm** ranh giới Modulith.
- [ ] `./gradlew unitTest` xanh; **báo trung thực** phần Testcontainers chưa chạy (R7).

---

## 14. Quy chuẩn nghiệp vụ (BR) áp dụng

| BR | Áp ở đâu |
|---|---|
| **BR1** Phân trang | A1 — mặc định 20/trang, whitelist 10/20/50/100 (`SearchRequest.java:52`) — [01 §8](01-xem-danh-sach-hoa-don.md) |
| **BR2** Hiển thị & sắp xếp | A1 — sort mặc định `ngayHoaDon:desc`, STT do FE tính theo trang — [01 §8](01-xem-danh-sach-hoa-don.md) |
| **BR3** Popup | FE — BE chỉ cấp cờ cho popup xác nhận |
| **BR7** Precision & làm tròn | Toàn bộ cột số: `money_vnd(18,2)`, `quantity(18,3)`, `percent_rate(5,2)`, `exchange_rate(18,6)` — [07 §2](07-thiet-ke-db.md) |
| **BR8** Khoảng thời gian | A1 — filter `ngayHoaDon` toán tử `between` — [01 §5.2](01-xem-danh-sach-hoa-don.md) |
| **BR11** Tìm kiếm/lọc/sắp xếp | A1 — `keyword` không dấu, `filters` AND, sort server-side — [01 §5.2, §8](01-xem-danh-sach-hoa-don.md) |
| **BR13.1** Nút thao tác danh sách | A1 — field cờ ẩn/hiện — [01 §5.3](01-xem-danh-sach-hoa-don.md) |
| **BR14** Chế độ & hành vi form | A5/A7 — lỗi validate **không** rollback dữ liệu FE đang nhập (BE chỉ trả 400) |
| **BR15** Validation trường | A5/A7 — `details[]` của `ApiError` trỏ đúng `field` để FE focus — [02 §5](02-them-moi-hoa-don.md) |
| **BR16** Cảnh báo nghiệp vụ | A6 cấp cờ `daLapChungTu` cho popup `_055`/`_056` |
| **BR18** Ngoại tệ | Cột `…QuyDoi` = giá trị gốc × `tyGia`, trừ thuế GTGT/XK theo công thức riêng — [02 §4](02-them-moi-hoa-don.md) |
| **BR19** Kiểm tra trùng | A5/A7 — BR03 của epic, khóa (soHoaDon + kyHieu + mauSo) trong tenant — [02 §5](02-them-moi-hoa-don.md) |
| **BR20** Số chứng từ & mã | `so_hoa_don` nhập tay, ≤ 50 ký tự, không dấu tiếng Việt — [02 §3](02-them-moi-hoa-don.md) |
| **BR21** Grid chi tiết con | `thu_tu` do client gửi, BE đánh lại liên tục khi lưu — [02 §6](02-them-moi-hoa-don.md) |
| **BR25** Phân quyền | §10 |
| **BR26** Toast | `messageId` trong envelope |
| **BR28** Multi-tenant | RLS `tenant_isolation` (`V1:31708`, `:31715`) + `DynamicSpecification` tự bơm `tenant_id` |
| **BR29** Chính sách xóa | A8/A9 — xóa **mềm** (`UC_HDBanHang_Xoa.md:75`), cascade mềm xuống dòng chi tiết — [05 §6](05-xoa-hoa-don.md) |
| **BR30** Ẩn/hiện cột | `GET /cot` (A2) sinh từ whitelist `@Searchable` |
| **BR31** Dòng tổng | A1 — `summary` tính trên toàn bộ bản ghi sau lọc — [01 §8.4](01-xem-danh-sach-hoa-don.md) |
| **BR39** Xuất Excel | A3 — `cotMacDinh(EXPORT)` 9 cột của màn danh sách — [01 §9](01-xem-danh-sach-hoa-don.md) |
| **BR43** Trim | BE `trim()` mọi field text trước khi lưu và trước khi check trùng — [02 §5](02-them-moi-hoa-don.md) |
| **BR45** Thao tác hàng loạt | A9 — lỗi từng phần, transaction riêng mỗi HĐ — [05 §7](05-xoa-hoa-don.md) |
| **BR46** Trường hệ thống bắt buộc | `id`, `tenant_id`, `phien_ban`, audit 6 cột, `da_xoa` — kế thừa `AggregateRootEntity` |

**BR chưa xử lý được lần này:** BR4 (loại chứng từ — HĐ không đăng ký `mst_loai_chung_tu`), BR9 (mã chứng từ — HĐ dùng `so_hoa_don` nhập tay, không sinh theo quy tắc), BR12/BR17/BR33/BR36/BR37/BR41/BR42 (vòng đời ghi sổ, kỳ kế toán, ngày hạch toán — **HĐ không hạch toán**, D2), BR5/BR6/BR10 (combogrid & chọn nguồn — thuộc FE và module master data), BR22/BR23/BR40 (dữ liệu cây — không áp dụng), BR32/BR34/BR38/BR44 (thuần FE).

---

## 15. Tài liệu tham chiếu

- `pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/1.function-breakdown.md`, `3.crud-matrix.md`, `6.messages.md`
- `pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/4.usecases/**` (5 UC)
- `pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/5.screens/**` (5 SCR)
- `pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/Matrix/PMKT-E-06196_HoaDonBanHang/_scope.md`
- `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_ThemMoi.md` — BR06, BR07, BR08, BR09, BR10, BR11, BR12, BR13, BR14, BR15, BR23, BR24
- `pmkt-docs/ba/Common/business_rules.md` — BR1, BR2, BR3, BR7, BR8, BR11, BR13, BR14, BR15, BR16, BR18, BR19, BR20, BR21, BR25, BR26, BR28, BR29, BR30, BR31, BR39, BR43, BR45, BR46
- `CLAUDE.md`, `cell-app/CLAUDE.md`, `docs/conventions.md`, `docs/be-khung-kien-truc-chuan.md`
- Mẫu code tham khảo: `cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_ban_hang/`, `.../core/`, `.../quan_he_chung_tu/`
