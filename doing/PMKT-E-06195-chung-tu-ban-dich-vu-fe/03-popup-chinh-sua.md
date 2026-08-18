# 03 — Popup Chỉnh sửa Chứng từ bán dịch vụ

| | |
|---|---|
| **Phiên bản** | **v2 — 2026-08-15** (đồng bộ BA commit `1a928c53b`) |
| **SCR nguồn** | `5.screens/SCR_CTbanDichVu_CapNhat.md` |
| **UC nguồn** | `UC_CTbanDichVu_CapNhat` (AC1–AC4) |
| **Ma trận** | `Matrix/.../SCR_CTbanDichVu_CapNhat_MaTranAnHien.md` — **[DRAFT]** |
| **Figma** | **Không có frame riêng.** SCR: *"Giao diện và layout giống SCR_CTbanDichVu_ThemMoi"* → dùng [Nguyên tệ 61661:104737](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/?node-id=61661-103452) / [Ngoại tệ 61685:127083](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/?node-id=61685-126981) |
| **Quyền** | `BanDichVu.Edit` (Lưu) · `BanDichVu.Edit` **AND** `BanDichVu.Post` (Lưu và ghi sổ) |
| **Tiền điều kiện** | Chứng từ ở trạng thái **"Chưa ghi sổ"** (`ChungTuBan.TrangThaiGhiSo`) |

> **Đây KHÔNG phải popup thứ hai.** Cùng component `ChungTuBanHangThemMoiModal` với `mode = 'edit'`
> (`ChungTuBanHangThemMoiModal.tsx:108`). File này chỉ ghi **cái khác** so với
> [02](02-popup-them-moi.md).

---

## 1. Bố cục

Giống hệt [02 §1](02-popup-them-moi.md), **gồm cả** việc bỏ tab Hạch toán và có nút footer
"Xem dữ liệu ghi sổ" ([00 D7](00-ke-hoach-tong.md)). Khác hai chỗ:

- Tiêu đề: `"Chỉnh sửa chứng từ bán dịch vụ"` (khóa `banHang:banDichVu.title.chinhSua`).
- Cụm "Chọn chứng từ" ở header (`HeaderControls`) — **cần BA xác nhận** có giữ ở chế độ Sửa không;
  "lập chứng từ từ chứng từ nguồn" là thao tác của Thêm mới. Đề xuất: **ẩn ở mode `edit`**.

## 2. Đặc tả UI

Kế thừa nguyên [02 §2](02-popup-them-moi.md). Không có số đo mới.

## 3. Ma trận Ẩn/Hiện · Disabled

**Ma trận trường y hệt màn Thêm mới** ([02 §3](02-popup-them-moi.md)) — nguồn tự khai như vậy.
Khác duy nhất là điều kiện `(đk-HĐ)`:

| Tab/Section | Thành phần | C1…C6 |
|---|---|---|
| Header Options | **Loại nghiệp vụ** | `Hide(at)` — cố định `Bán dịch vụ`, **bất biến** (D6) |
| Header Options | **Kiêm phiếu xuất kho** | `Hide(at)` |
| Header Options | Lập kèm hóa đơn *(đk-HĐ)* | `Show/Disable(đk-HĐ)` |
| Tab Chứng từ ghi nợ | Đã lập hóa đơn (checkbox) *(đk-HĐ)* | `Show/Disable(đk-HĐ)` |
| *(mọi trường còn lại)* | | **= Thêm mới** |
| Nút hoạt động | Lưu · Lưu và ghi sổ · Hủy (+ **Xem dữ liệu ghi sổ**) | `Show` |

**`(đk-HĐ)` — BR02 của `SCR_CTbanDichVu_CapNhat.md`:**

| Nguồn tích "Đã lập hóa đơn" | "Đã lập hóa đơn" | "Lập kèm hóa đơn" |
|---|---|---|
| **NSD tự tích** | `Show` (cho sửa lại) | `Show` |
| **Hệ thống tích** (đã tồn tại hóa đơn sinh từ chứng từ này) | **`Disable`** | **`Disable`** |

⇒ FE cần trường phân biệt **nguồn tích**. **Chưa có trong hợp đồng BE** — xem
[07 §1.3](07-hop-dong-api-va-i18n.md) (**Q-BR02**).

> **Gợi ý v2:** LDM v2 có `HoaDonBan.ChungTuBanId` (dùng ở `SCR_CTBH_DanhSach` BR01 để join cột "Số
> hóa đơn"). Nếu response chi tiết trả kèm danh sách hóa đơn liên kết thì FE suy được
> `daLapHoaDonDoHeThong = (danhSachHoaDon.length > 0)` — **không cần trường mới**. Cần BE xác nhận.

**⚠ Chưa rõ** (nguồn tự ghi ở "Điểm cần xác nhận" #2): khi hệ thống đã tích, các **trường bên trong
Tab Hóa đơn** là read-only hay vẫn nhập được? Nguồn chỉ nói khóa 2 checkbox ⇒
[00 §12 Q8](00-ke-hoach-tong.md).

## 4. Trường & cột

Y hệt [02 §4](02-popup-them-moi.md) (đã đổi tên field theo LDM v2). Khác về **dữ liệu**, không về cấu
trúc:

- Load giá trị hiện tại của `ChungTuBan` + `ChiTietChungTuBan` (`GET /{id}`).
- Cho **thêm / sửa / xóa** dòng chi tiết (`SCR_CTbanDichVu_CapNhat.md` §Điểm khác biệt).
- Cột `SoLuongDaXuatHD` **hiện** ở chế độ Sửa (khác Thêm mới); ô read-only.
- `LoaiNghiepVu` **không** đưa vào body `PUT`, hoặc gửi nguyên giá trị cũ — BR24: *"Chứng từ **đã lưu
  không đổi được** `LoaiNghiepVu` giữa nhóm bán hàng và nhóm bán dịch vụ"*.

## 5. Hành vi & sự kiện

| Nút | Điều kiện hiện | Việc | Message |
|---|---|---|---|
| **Lưu** | có `BanDichVu.Edit` | validate → `PUT /{id}` kèm `updatedAt` (optimistic lock, BR12) → đóng popup | **MSG_PMKT-E-06195_020** "Lưu thành công" |
| **Lưu và ghi sổ** | có `.Edit` **AND** `.Post` | validate → `PUT /{id}` với `ghiSo: true` — một request, một transaction (**BR21**) | **MSG_PMKT-E-06195_021** "Cập nhật và ghi sổ chứng từ thành công" |
| **Xem dữ liệu ghi sổ** | luôn | popup bút toán ([02 §5.4](02-popup-them-moi.md)) | — |
| **Hủy** / **×** / ESC | luôn | có thay đổi ⇒ popup xác nhận đóng (BR3) | — |

**Vào từ đâu:**
- Lưới → ⋮ "Chỉnh sửa" (chỉ khi "Chưa ghi sổ" + có quyền) → đóng popup ⇒ **về lưới**.
- Popup Xem chi tiết → nút "Chỉnh sửa" → **BR34**: Lưu hoặc Hủy ⇒ đóng popup Sửa và **quay lại popup
  Xem chi tiết** (đã cập nhật dữ liệu), **không** nhảy về danh sách.

**Trạng thái form sau lỗi:** giữ nguyên dữ liệu đã sửa, highlight trường vi phạm, không reset/đóng
(`UC_CTbanDichVu_CapNhat.md` ghi chú cuối).

**Lỗi BE cần hiển thị nguyên văn:**

| Tình huống | Message | Mã |
|---|---|---|
| Chứng từ không tồn tại | "Chứng từ không tồn tại" | _012 |
| Người khác đang sửa / dữ liệu đã đổi | "Chứng từ đang được người khác chỉnh sửa. Vui lòng thử lại sau" | _105 |
| Lỗi hệ thống | "Lỗi hệ thống" | _013 |
| Cố ghi sổ chứng từ đã ghi sổ | "Không thể ghi sổ chứng từ đã ghi sổ" | _016 |

## 6. Validation phía FE

Toàn bộ V1–V20 của [02 §6](02-popup-them-moi.md), **không trừ gì** (`SCR_CTbanDichVu_CapNhat.md`
**BR01**: *"Áp dụng tất cả các quy tắc validate tại SCR_CTbanDichVu_ThemMoi"*).

Bổ sung: validate thất bại ⇒ **focus vào trường đầu tiên có lỗi** (BR01 của SCR CapNhat, khớp BR15.4).

## 7. Luồng xử lý

1. Mở popup `mode='edit'`, `rowId` → `useDetail(rowId)` (**cùng resource** — [00 D2](00-ke-hoach-tong.md)).
2. `toFormValuesChiTiet` (`api/formDetail.ts`) map response → form values; đọc `loaiNghiepVu` từ bản
   ghi (không đoán từ chỗ mở popup).
3. Tính lại `nguCanhAnHien` từ dữ liệu đã lưu (Loại nghiệp vụ / Thu tiền ngay / Hình thức TT / Lập kèm
   hóa đơn / Loại tiền / Loại chiết khấu) ⇒ ra đúng cột C1…C6.
4. Áp `(đk-HĐ)`: hóa đơn do hệ thống sinh ⇒ disable 2 checkbox.
5. User sửa → mọi công thức tính lại như Thêm mới.
6. Lưu → `PUT` → toast → đóng → invalidate.
7. Loading: `UiSpin` phủ thân popup trong lúc `useDetail` chạy; **không** render form rỗng rồi đổ dữ
   liệu.

> ⚠ **Nợ đã biết:** `PUT /{id}` **chưa dựng ở BE kể cả cho chứng từ bán hàng hóa** —
> `ChungTuBanHangThemMoiModal.tsx:25-27` ghi rõ nút Lưu ở chế độ Sửa đang báo "đang phát triển" và
> popup Sửa **cố tình không nạp sẵn chi tiết**. Với CTBDV giữ nguyên quy tắc: **không** đổ dữ liệu ra
> cho user sửa khi chưa lưu được. Xem [00 §10 R1](00-ke-hoach-tong.md).

## 8. Phân bổ file

| Việc | File |
|---|---|
| `(đk-HĐ)` — khóa cặp checkbox hóa đơn | `helpers/anHien.ts` → `khoaCheckboxHoaDon(values)` |
| Cờ / danh sách hóa đơn liên kết trong schema | `api/model.ts` |
| Map detail → form values | `api/formDetail.ts` |
| Body `PUT` + `updatedAt`, giữ nguyên `loaiNghiepVu` | `api/payload.ts` |
| Mutation | `api/queries.ts` (`useUpdate`) |
| Bộ nút theo mode | `components/ChungTuBanHangThemMoiModal.tsx` |
| Quay lại popup Xem sau khi Lưu/Hủy (BR34) | `components/ChungTuBanHangTab.tsx` (state `modal`) |
| Chữ | `i18n/vi.ts` · `en.ts` |

## 9. Kiểm thử

| # | Input | Kỳ vọng |
|---|---|---|
| T1 | chứng từ đã có hóa đơn hệ thống sinh | cả "Đã lập hóa đơn" và "Lập kèm hóa đơn" **disabled** |
| T2 | NSD tự tích, chưa có hóa đơn | cả hai **enabled** |
| T3 | `TrangThaiGhiSo = "Đã ghi sổ"` | popup Sửa **không mở được** (nút bị ẩn từ lưới/màn xem) |
| T4 | mode `edit`, user có `.Edit` không `.Post` | chỉ hiện "Lưu" |
| T5 | Lưu thành công | toast MSG_..._020, popup đóng, list invalidate |
| T6 | Lưu và ghi sổ thành công | toast MSG_..._021 |
| T7 | BE trả 409 stale | toast MSG_..._105, **form giữ nguyên** dữ liệu đã sửa |
| T8 | mở từ popup Xem → Lưu | quay lại popup Xem với dữ liệu mới (BR34), **không** về danh sách |
| T9 | ma trận trường | mọi ô ở mode `edit` giống mode `create` (trừ cặp checkbox hóa đơn) |
| T10 🆕 | body `PUT` | **không** chứa `loaiNghiepVu` đã đổi giá trị — luôn bằng giá trị của bản ghi gốc (BR24) |
| T11 🆕 | mode `edit` | **không** render tab Hạch toán; **có** nút "Xem dữ liệu ghi sổ" |

## 10. BR đã áp dụng

**Chung:** BR3 · BR12 (optimistic lock) · BR13.2 · BR14.1 (chế độ Chỉnh sửa) · BR15 · BR16 · BR25 ·
BR26 · BR34 · BR37 · BR43 + toàn bộ BR của [02](02-popup-them-moi.md).
**Của CTBH:** BR05 (checkbox hóa đơn) · BR21 (ghi sổ) · **BR24** (LoaiNghiepVu bất biến).

**Chưa đạt:** như [02 §10](02-popup-them-moi.md), cộng thêm — cờ "nguồn tích hóa đơn" chưa có trong
hợp đồng BE (**Q-BR02**, [07 §1.3](07-hop-dong-api-va-i18n.md)).
