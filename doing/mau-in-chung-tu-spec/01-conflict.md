# Mẫu in chứng từ theo khối — Sổ mâu thuẫn tài liệu

| | |
|---|---|
| Nguồn | mock `ThietLapMauIn.html` + yêu cầu/chốt của user 2026-09-17 + code hiện có |
| Ngày soát | 2026-09-17 |
| Tổng | **15** mục — 9 `CLOSED-BA` · 6 `CLOSED-AUTO` · **0 `OPEN`** |

---

## Bảng tổng

| ID | Chủ đề | Sev | Trạng thái | Luật bị chặn | Chốt |
|---|---|---|---|---|---|
| C16 | Kênh cell → super-admin không được dựng `RestClient` trần (`ProxyArchTest` của `integration_ops.proxy`) — plan gốc ghi `pmkt.mau-in.super-admin.url` | P1 | CLOSED-AUTO 2026-09-17 | — | Đi qua `ProxyClient`, đích `pmkt.proxy.targets.super-admin`, cờ `pmkt.mau-in.super-admin.enabled`; xem ghi chú hiện thực ở `02-rules.md` |
| **C01** | Render bản in ở FE (khác chốt A9 2026-08-20 "render thuộc BE" cho mẫu pháp định) | P0 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q1): GĐ1 FE render; BE PDF là GĐ5 |
| **C02** | Mở kênh `/internal/mau-in/**` trên super-admin-service (service tuyên bố "không có kênh internal") | P1 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q2) |
| **C03** | Quyền màn thiết lập: một mã `HTMauIn` hay theo loại `<ChucNang>.PrintConfig` | P1 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q4): `HTMauIn.View/Edit` |
| **C04** | `DON_VI` / `TIEU_DE` có được ẩn không (mock cho ẩn mọi khối) | P1 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q5): `DON_VI` ẩn được, `TIEU_DE` luôn hiện |
| **C05** | Trường/cột mới sau này mặc định HIỆN (mock) hay ẨN ở bản tuỳ chỉnh | P1 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q6): mẫu hệ thống → hiện; bản tuỳ chỉnh → ẩn + cờ `moi` |
| **C06** | Logo / ảnh nền trong v1 (tenant chưa có trường logo) | P2 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q7): v1 chỉ "Khung viền"; `logo`/`nen.kieu='ANH'` lưu nhưng không render |
| **C07** | Hộp "Đóng khi chưa lưu": mock 3 nút vs BR3 2 nút | P1 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q18): theo BR3 |
| **C08** | `MuaDichVu.Print` **không tồn tại** trong `iam_quyen` / `MaChucNang` (MDV chỉ có View·View.Detail·Create·Edit·Delete·Post·Unpost) — in MDV gate bằng gì? | P1 | `CLOSED-AUTO` | — | 2026-09-17: gate bằng **`MuaDichVu.View.Detail`** — quyền hẹp sẵn có, bản in không lộ gì ngoài màn chi tiết; provider khai `hanhDongIn()`; BA cấp `.Print` sau thì đổi một hằng. **Báo user.** |
| **C09** | Nguồn "Đầu trang đơn vị": mock nói *Thông tin công ty*; thu/chi hiện dùng `mst_don_vi` cấp GỐC | P2 | `CLOSED-AUTO` | — | 2026-09-17: theo mock (bậc 4) — `Tenant` (Thông tin công ty) ưu tiên; `tenDonVi` trống thì fallback `mst_don_vi` GỐC |
| **C10** | Cờ `layTenNguoiLapPhieuTuNguoiDungDangNhap`: người tạo chứng từ hay người đang in? | P2 | `CLOSED-AUTO` | — | 2026-09-17: đúng nghĩa đen — **người đang đăng nhập** lúc in (`NguoiDungLookupApi.hoTenTheoId`) |
| **C11** | Mã message/luật tạm khi chưa có mã epic | P2 | `CLOSED-BA` | — | Dat · 2026-09-17 (Q11): `MSG_MAUIN_nnn`, `R-MAUIN-nnn` |
| **C12** | Q10 duyệt thêm `@dnd-kit/sortable`, nhưng máy dev **không có npm** (Node chỉ chạy qua Electron) → không cập nhật được `package-lock.json` | P2 | `CLOSED-AUTO` | — | 2026-09-17: **tự dựng sortable trên `@dnd-kit/core`** (đã cài, `bieuMau` cũng chỉ dùng core); không đổi `package.json`. **Báo user** — cài sortable sau nếu muốn |
| **C13** | Địa chỉ đơn vị: `Tenant` chỉ có `diaChiChiTiet` + `phuongXaId` + `tinhThanhPhoId` | P2 | `CLOSED-AUTO` | — | 2026-09-17: ghép `diaChiChiTiet, <tên phường xã>, <tên tỉnh>` khi tra được (`mst_phuong_xa`, `mst_tinh_thanh_pho`); phần thiếu bỏ qua, không in "null" |
| **C14** | MDV không có bảng thuế riêng (thuế nằm trên từng dòng dịch vụ) nhưng mock có "Bảng Thuế" | P2 | `CLOSED-AUTO` | — | 2026-09-17: bảng `thue` = các dòng dịch vụ có `tienThueGtgt ≠ 0`, cột theo mock (`tenDV · thueSuat · giaTriChiuThue · tienThue · tkThue · nhomHhdv`) |
| **C15** | `super-admin-service/`, `client-admin/` chưa là git repo — remote/nhánh chưa có | P2 | `CLOSED-BA` | — | Dat · 2026-09-17: đã `git init` cả hai, remote `ospgroupvn-pmkt/{super-admin-service,client-admin}`, nhánh mặc định `develop`, đã đẩy bản nhập đầu |

> Bốn trạng thái: `OPEN` · `CLOSED-AUTO` (tự chốt theo thang thẩm quyền, có ghi lý do) · `CLOSED-BA` (có tên
> người + ngày) · `HUỶ`. Mục `CLOSED-AUTO` là quyết định thiết kế **ngoài tài liệu** — mỗi mục phải có test ghim
> (truy vết ở [02-rules.md](02-rules.md)) để người kiểm thử có chỗ đối chiếu.

---

## Chi tiết các mục `CLOSED-AUTO`

### C08 · In MDV gate bằng `MuaDichVu.View.Detail`
- Bằng chứng thiếu: `MaChucNang.java:207-208` javadoc MDV không có `Print`; `rg "MuaDichVu.Print" db/migration` = 0.
- Không tự seed `.Print` cho MDV: thêm mã quyền vào ma trận phân quyền là quyết định BA (DanhSachQuyen.md).
- Hệ quả code: `MauInProvider.hanhDongIn()` mặc định `Print`; `MdvMauInProvider` trả `View.Detail` kèm chú thích
  trỏ về mục này. FE `NutInChungTu` nhận `quyenIn` từ module chủ (`MuaDichVu.View.Detail`).
- Luật liên quan: `R-MAUIN-003`.

### C09 · Đầu trang đơn vị lấy từ Thông tin công ty
- Mock (bậc 4) ghi rõ *"Nội dung lấy từ Thông tin công ty"* và có MST/ĐT — `mst_don_vi` không có hai cột này.
- Fallback `mst_don_vi` GỐC giữ tương thích với tenant chưa khai Thông tin công ty.
- Luật liên quan: `R-MAUIN-080`, `R-MAUIN-081`.

### C10 · Người lập phiếu = người đang đăng nhập
- Tên cờ nói "từ người dùng đăng nhập"; BE đã có `NguoiDungLookupApi.hoTenTheoId` để tra tên. Người TẠO chứng từ
  (`nguoiTao`) không phải nghĩa của cờ. Khi tra không ra tên → dùng `tenNguoiKyNguoiLapPhieu` đã cấu hình.
- Luật liên quan: `R-MAUIN-083`.

### C12 · Sortable tự dựng trên `@dnd-kit/core`
- `which npm` = không có; Node chỉ chạy qua `ELECTRON_RUN_AS_NODE=1 Code.exe`. Thêm package mà không cập nhật
  lockfile là gieo lỗi `npm ci` ở CI.
- Cài đặt: `useDraggable` + `useDroppable` theo chỉ số, `doiViTri(tu, den)` từ chối `den < 2` (R-MAUIN-050).
- Luật liên quan: `R-MAUIN-050`, `R-MAUIN-053`.

### C13 · Ghép địa chỉ
- Luật liên quan: `R-MAUIN-081`.

### C14 · Bảng thuế MDV suy từ dòng
- Luật liên quan: `R-MAUIN-076` (provider MDV), fixture `mdv.du-lieu-mau.json`.
