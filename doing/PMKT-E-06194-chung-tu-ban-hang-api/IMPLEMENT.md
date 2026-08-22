# IMPLEMENT — PMKT-E-06194 Chứng từ bán hàng (BE)

> Nhật ký thi công của `/gen-be`. Nguồn: [`00-ke-hoach-tong.md`](00-ke-hoach-tong.md) (đã chốt đủ 6/6
> câu hỏi BA ngày 2026-08-16) + PYC `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/` @ `1a928c53b`.

## 1. Ngày · phạm vi

**2026-08-16.** Code trên `cell-app` nhánh `feat/chung-tu-ban-hang-2`, base package `vn.vtt.pmkt`.

**Đây là sửa BROWNFIELD, không phải sinh mới.** Module `chung_tu_ban_hang/` đã có sẵn 46 file Java
với đầy đủ template lưu/ghi sổ/bỏ ghi sổ, bộ định khoản 7 bút toán, và bộ tính tiền. Việc của đợt này
là **kéo module về khớp PYC bản 2026-08-13** (bản mà plan cũ 07–10/08 chưa có).

10 file con của plan (`01-…10-`) là bản 07–10/08 mô tả kiến trúc đã bị thay thế → đã chuyển vào
[`_cu-2026-08-10-KHONG-DUNG/`](_cu-2026-08-10-KHONG-DUNG/) kèm README. Nguồn sự thật khi code là
`00-ke-hoach-tong.md` + PYC.

## 2. File đã tạo / sửa

### Migration

| File | Nội dung |
|---|---|
| `db/migration/V1012__sal_ctbh_gop_ban_dich_vu_va_kiem_chung_tu.sql` (mới) | A. nới `CHECK loai_nghiep_vu` nhận `'Bán dịch vụ'` · B1–B2. 4 cột BR18 mới · B3. 2 cột BR14 · B4. nới `NOT NULL` của `trang_thai_xuat_hang` · C. di trú 30 header + 30 dòng từ 2 bảng bán dịch vụ · D. index BR02 |

⚠ **DROP hai bảng nguồn CHƯA làm** — cố ý để ở migration riêng (`V1003`) chạy sau, theo R7 của plan:
nếu bước di trú sai ánh xạ thì còn bảng gốc để đối chiếu.

### Java — `cell/chung_tu_ban_hang/internal/`

| File | Sửa gì |
|---|---|
| `model/LoaiNghiepVuBanHang.java` | thêm `DICH_VU("Bán dịch vụ")` + `laDichVu()` + `hopLeChoManBanHang()` |
| `entity/ChungTuBanHang.java` | +6 field BR18 (`soChungTuXuatKho`, `ngayChungTuXuatKho`, `soChungTuThuTien`, `ngayChungTuThuTien`, `taiKhoanNhanId`, `tenNganHangNhan`) · `trangThaiXuatHang` bỏ `nullable = false` |
| `entity/ChiTietChungTuBanHang.java` | +2 field BR14 (`giaTriTinhThueXk`, `giaTriTinhThueXkQuyDoi`) |
| `dto/ChungTuBanHangDto.java` · `dto/LuuChungTuBanHangRequest.java` | +6 trường BR18 |
| `service/business/ChungTuBanHangMapper.java` | nối 6 trường BR18 cả hai chiều |
| `service/business/TinhToanBanHang.java` | BR14 tách **hai luồng tiền tệ độc lập**; BR11 mục 2 (SL = 0 ép đơn giá 0, giữ thành tiền) |
| `service/business/TrangThaiBanHang.java` | BR22 — trạng thái xuất hàng trả `null` khi không có dòng hàng hóa |
| `service/business/KiemTraBanHang.java` | +`kiemTraLoaiNghiepVuThuocManBanHang()` (plan R8) · **gỡ chặn** `kiemPhieuXuatKho` / `thuTienNgay` |
| `service/business/SoTien.java` | +`bang0()` |
| `service/business/DinhKhoanBanHang.java` | +javadoc `TODO-C6` |
| `service/business/GhiSoChungTuBanHang.java` | +javadoc `TODO-C7` |

### Test

| File | Nội dung |
|---|---|
| `test/…/service/business/QuyTacMoiBanHang2026Test.java` (mới) | 6 ca `@Tag("unit")`: BR11 mục 2 · BR14 hai luồng · BR14 giữ giá trị người dùng sửa · xuất khẩu không phát sinh GTGT · R8 chặn `DICH_VU` · 3 chuỗi enum khớp `CHECK` constraint |

### Frontend

| File | Sửa gì |
|---|---|
| `client/src/features/banHang/chungTuBanHang/api/model.ts` | `trangThaiXuatHang` → `z.string().nullish()` — BE giờ trả `null` cho chứng từ không có dòng hàng hóa (BR22); giữ `z.string()` thì `safeParse` vỡ cả trang |

## 3. Quyết định khi code (ngoài plan)

**3.1 — Không thêm cột trùng nghĩa.** Bản nháp migration đầu tiên của tôi thêm `nguoi_nhan_hang`,
`nguoi_nop_tien`, `ly_do_thu`. Bảng **đã có** `nguoi_nhan`, `nguoi_nop`, `mieu_ta_phieu_thu` mang đúng
ba khái niệm đó (`ChungTuBanHang.java:104,107,153`). Đã bỏ, dùng lại cột cũ và thêm `COMMENT` nối tên
BA ↔ tên cột.

**3.2 — Gỡ chặn `kiemPhieuXuatKho` / `thuTienNgay`.** `KiemTraBanHang` đang chặn cứng cả ba cờ với lý
do "cờ bật nhưng không có chứng từ con nào được tạo". BR18 bãi bỏ tiền đề đó: chứng từ bán **tự đóng
vai** phiếu xuất kho / phiếu thu, BA nói thẳng *"hệ thống KHÔNG sinh bản ghi `ENT_PhieuXuatKho` hay
`ENT_PhieuThu`"*. Giữ chặn thì hai chức năng chính của epic không bật được.
**`lapKemHoaDon` giữ nguyên chặn** — BR18 mục 6 tách bạch: hóa đơn vẫn là chứng từ độc lập phải sinh
bản ghi thật, mà module hóa đơn chưa nối.

**3.3 — `donGiaThueXk` giữ đồng bộ.** Cột cũ từng đóng vai "giá trị tính thuế XK" khi chỉ có một
luồng. Code mới đọc `giaTriTinhThueXkQuyDoi`, nhưng vẫn ghi `donGiaThueXk` = giá trị đó để dữ liệu cũ
và báo cáo đang đọc cột này không gãy.

## 4. Cổng kiểm tra

| Cổng | Kết quả |
|---|---|
| `cd cell-app && ./gradlew unitTest` | ✅ **BUILD SUCCESSFUL** (chạy lại sau mỗi bước) |
| Migration V1002 trên schema thật | ✅ chạy trong transaction + ROLLBACK trên `pmkt_cell_datvl_2`: 148 + 30 = **178** chứng từ, 30 dòng `Bán dịch vụ`, chi tiết 305 + 30 = **335**. DB không đổi |
| `client`: `npx vitest run …/chungTuBanHang --reporter=dot` | ⚠ 145 pass / **4 fail** — **nền sẵn có**, đã xác minh bằng `git stash` (đỏ y hệt khi chưa có thay đổi của tôi) |
| `client`: `npx vite build` | ✅ built in 1.41s |

**CHƯA chạy:**

- **Test tích hợp Testcontainers** — cấm Docker theo luật repo.
- **`npm run typecheck` / `lint` / `lint:boundaries`** — bốn lệnh nặng, `client/CLAUDE.md §15.0` chốt
  không chạy mặc định. Đã đếm typecheck: **159 lỗi trước và sau** thay đổi của tôi (không làm xấu hơn).
- **Postman collection** — `docs/json/PMKT-E-06194-*.postman_collection.json` **chưa xuất được**:
  skill yêu cầu lấy từ `/v3/api-docs` của app đang chạy, mà `curl localhost:8081/v3/api-docs` trả
  `000` (app không chạy). Bịa collection bằng tay sẽ lệch chữ ký thật. **Cần chạy app rồi xuất lại.**

## 5. ⚠️ Việc CHƯA làm — phải đọc trước khi test

Chi tiết + lý do ở [§15 Cảnh báo bàn giao](00-ke-hoach-tong.md) của plan. Tóm tắt:

| # | Chưa làm | Hệ quả khi test |
|---|---|---|
| **C7** 🔍 | **Sổ kho không được ghi.** `acc_so_kho` có trong DB nhưng toàn bộ Java không có entity/API/writer nào. Nơi đúng là `accounting_core` = core, **không được sửa** theo yêu cầu 2026-08-16. Đánh dấu `TODO-C7` ở `GhiSoChungTuBanHang.java` | Ghi sổ chứng từ kiêm phiếu xuất kho **không làm giảm tồn kho** |
| **C6** 🔍 | **6 trường BR20 không lên sổ cái** (`VuViecId`, `DonViId`, `DoiTuongTapHopChiPhiId`, `DonHangId`, `HopDongId`, `STTButToan`) — record `DinhKhoan` của kernel không có tham số tương ứng. Đánh dấu `TODO-C6` ở `DinhKhoanBanHang.java` | Báo cáo lọc theo Vụ việc / Đơn vị / Đối tượng THCP / Hợp đồng **không thấy** bút toán bán hàng |
| **C1** | Giá vốn đứng ở 0 cho tới khi PMKT-E-03629 được sửa (người khác làm) | Bút toán giá vốn = 0 |
| **C4** | BR16 định khoản ngầm định chưa cài — bảng danh mục chưa tồn tại | Người dùng phải tự chọn tài khoản trên từng dòng |
| **C5** | Auto-fill khách hàng thiếu 3 trường so với BR01 (mô hình `mst_khach_hang_*` không có) | Điều khoản TT / số ngày nợ / loại tiền phải nhập tay |
| **C2** | Sắp xếp mặc định 3 cột — **lệch BR11** bản 12/08 (epic thắng, BA đã đồng ý) | — |
| **C3** | Tên cột hệ thống không theo hậu tố `Id` — **lệch BR46** | — |
| — | `lapKemHoaDon` vẫn bị chặn (§3.2) | Không tích được ô "Lập kèm hóa đơn" |
| — | Migration `V1003` DROP 2 bảng bán dịch vụ chưa viết (cố ý — R7) | Hai bảng cũ còn nằm đó, không ai đọc |

## 6. Bước tiếp theo

1. Chạy app → xuất Postman collection từ `/v3/api-docs` vào `docs/json/`.
2. Test tay luồng thêm mới / sửa / ghi sổ / bỏ ghi sổ với `kiemPhieuXuatKho = true` và
   `thuTienNgay = true` (hai cờ vừa được mở).
3. Đối chiếu 30 chứng từ bán dịch vụ sau khi migration chạy thật, rồi mới viết `V1003` DROP.
4. Mở ticket `accounting_core` cho C6 + C7 nếu nghiệp vụ cần sổ kho và các chiều phân tích.

---

## 7. Đối chiếu lại 2026-08-18 — bảng §5 đã lỗi thời một phần

Tài liệu BA có bản mới (3 commit ngày 08-17) và code đã merge thêm 2 module (`tinh_gia_xuat_kho/`,
`kho/`). Kết quả rà soát đầy đủ nằm ở **[plan §17](00-ke-hoach-tong.md#17-đối-chiếu-tài-liệu--code-2026-08-18)**.
Ba dòng của §5 phải đọc lại theo đó:

| Dòng §5 | Sửa lại |
|---|---|
| **C7** | **Sai khung.** Tài liệu nói chứng từ bán **KHÔNG** ghi `acc_so_kho` — phiếu xuất kho ghi (BR18 mục 4 · BR20 mục 4). Không cần `GhiSoKhoApi` ở `accounting_core`. Lỗi thật: chưa sinh `inv_phieu_xuat_kho` (§17 G6). |
| **C6** | **Thu hẹp.** `STTButToan` / `STTDongChiTiet` / `KhoanMucChiPhiId` **truyền được** qua `DinhKhoan.voiThuTu(...)` / `voiKhoanMucChiPhi(...)` — code chỉ quên gọi (§17 G2, G3). Còn thiếu thật 4–6 trường, vẫn cần ticket kernel (§17 G4). |
| **C1** | **Nút thắt đổi.** PMKT-E-03629 **đã được cài** và không cần sửa; `TinhGiaXuatKhoRealtimeApi` nhận id phiếu xuất kho. Chờ §17 G6, không chờ 03629 (§17 G7 cũ). |

Phát sinh mới chưa có trong §5: **G8** (lọc tài khoản còn ràng `TrangThai = ACTIVE`, trái BR16 bản
08-17 → chặn lưu oan), **G11** (`V1003` đã bị chiếm, dùng `V1011`), **G12** (`client/…/model.ts` chưa
commit).

---

## 8. Đợt code 2026-08-20 — nhóm "không chạm core"

Chi tiết + lý do từng mục: **[plan §17.2b](00-ke-hoach-tong.md#172b-đã-code--2026-08-20)**.

| File | Thay đổi |
|---|---|
| `DinhKhoanBanHang.java` | `STT_BUT_TOAN` cố định theo bảng BR20 mục 1; nạp `khoanMucChiPhiId`; `sttDongChiTiet` = `ThuTu` của dòng, có đường lùi khi `thuTu` trùng |
| `ChungTuBanHangMapper.java` | `thuTu` client gửi lên phải phân biệt được từng dòng, trùng thì server đánh lại |
| `TraCuuDanhMucRepository.java` | Bỏ `trang_thai` khỏi truy vấn tài khoản cấp cuối **và** khách hàng (BR16 mục 4 · BR01 mục 1, bản 08-17) |
| `KiemTraBanHang.java` | Javadoc theo BR16 mục 4 mới — không còn kiểm "đang hoạt động" |
| `GhiSoChungTuBanHang.java` | Viết lại `TODO-C7` (bản cũ mô tả sai nghĩa vụ) |
| `QuyTacMoiBanHang2026Test.java` | +3 test: STT theo BR20, `STTDongChiTiet` + khoản mục chi phí, đường lùi khi `thuTu` trùng |

**Cổng:** `cd cell-app && ./gradlew unitTest` → **BUILD SUCCESSFUL** (2m21s). Testcontainers không chạy (cấm Docker).

### Không đụng core — đúng yêu cầu

Không sửa file nào dưới `accounting_core/` hay `core/`. Ba chỗ từng nghĩ phải sửa kernel thì hoá ra
kernel đã có sẵn hàm — `DinhKhoan.voiThuTu(...)` và `voiKhoanMucChiPhi(...)` — chỉ là module bán hàng
chưa gọi.

### Còn nợ — nguyên nhân nằm ngoài module

| # | Việc | Vướng ở đâu |
|---|---|---|
| **G1 + G6** | Sinh `inv_phieu_xuat_kho` / `cash_phieu_thu` / `sal_hoa_don_ban_hang` khi Lưu, rồi thôi ghi hộ bút toán giá vốn + thu tiền | `kho/` có entity nhưng `create`/`ghiSo` đều `throw chuaHoTro`; `kho/` và `hoa_don_ban_hang/` chưa có `api/`; chưa có module `cash_phieu_thu` |
| **G4** | 4 trường phân tích còn lại lên sổ cái | `DinhKhoan` thiếu tham số (core) **và** bảng chi tiết thiếu `doi_tuong_tap_hop_chi_phi_id` · `don_dat_hang_id` |
| **G7 · G10** | Cột back-link của `inv_phieu_xuat_kho_chi_tiet`; ~10 cột `acc_so_cai` mà BR20 khai | Bảng của module khác |
| **G9** | Hai cột nguyên tệ/quy đổi khi `TyGia = 1` | Câu hỏi cho BA |
| **C4 / BR16** | Định khoản ngầm định | **Vừa mở khoá** — xem [plan §17.2d](00-ke-hoach-tong.md#172d-việc-vừa-được-mở-khoá--chưa-làm) |

### Thay đổi trong cây làm việc KHÔNG phải của đợt này

Phát hiện lúc sửa, ghi lại để khỏi lẫn vào diff của epic:

- `ChungTuBanHangController.java` — gỡ ba override CRUD (kèm `thongBaoLuu` / `messageIdLuu`). Hệ quả:
  thông báo lưu/sửa/xoá về mã chung `MSG_CORE_*`, mất mã riêng của epic và mất cả câu
  "Ghi sổ chứng từ bán hàng thành công" khi bấm *Lưu và ghi sổ*. **Cần xác nhận là có chủ ý.**
- `core/config/FlywayConfig.java` — bỏ comment dòng `ALTER ROLE pmkt_app WITH PASSWORD`.
- `db/migration/V1032__tknd_va_cau_hinh_danh_so.sql` — sửa một migration **đã commit**. Vô hại lúc này
  vì DB dev mới ở `V1031` (chưa chạy V1032), nhưng trái luật "không sửa migration đã merge" — nếu có
  máy nào đã chạy rồi thì sẽ lệch checksum.
