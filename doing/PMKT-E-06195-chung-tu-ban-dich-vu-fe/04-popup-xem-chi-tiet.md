# 04 — Popup Xem chi tiết Chứng từ bán dịch vụ (readonly)

| | |
|---|---|
| **Phiên bản** | **v2 — 2026-08-15** (đồng bộ BA commit `1a928c53b`) |
| **SCR nguồn** | `5.screens/SCR_CTbanDichVu_ChiTiet.md` |
| **UC nguồn** | `UC_CTbanDichVu_ChiTiet` (AC1–AC3) |
| **Ma trận** | `Matrix/.../SCR_CTbanDichVu_ChiTiet_MaTranAnHien.md` — **[DRAFT]** |
| **Figma** | **Không có** — SCR ghi mục "Nguyên mẫu" là `[]` (rỗng). Layout suy ra từ màn Thêm mới ở chế độ readonly |
| **Quyền** | `BanDichVu.View.Detail` |

> ⚠ **Chưa có Figma cho màn này** — bộ nút footer và cách trình bày ô read-only là **suy luận**, phải
> Design review lại.

---

## 1. Bố cục

Cùng vỏ popup và bố cục 3 khối như [02 §1](02-popup-them-moi.md), khác:

- Tiêu đề `"Xem chi tiết chứng từ bán dịch vụ"`.
- **Không** có cụm "Chọn chứng từ" ở header (thao tác của Thêm mới).
- **Không** có 3 nút lưới (Thêm dòng · Thêm ghi chú · Xóa hết dòng) và cột 🗑 (Matrix: `Hide`).
- **Không** có tab Hạch toán 🆕 — BA v2 xoá khỏi `UC_CTbanDichVu_ChiTiet.md` AC2 và bước 4, và khỏi
  ma trận ([00 D7](00-ke-hoach-tong.md)). Bộ tab thẻ lưới còn: `Chi tiết dịch vụ · Thuế · Tham chiếu`
  (+ ⚠`Đính kèm` nếu BA duyệt — **Q9**).
- Footer đổi thành bộ nút theo trạng thái (§5).

## 2. Đặc tả UI

Chưa có Figma. Ô read-only theo quy ước `Disable` của ma trận (**hiện xám, read-only**) — dùng đúng
control cũ ở trạng thái `disabled`, **không** đổi sang label thuần để bố cục không nhảy so với màn
Thêm mới. Ma trận tự ghi điểm này ở "Điểm cần xác nhận" #3 ⇒ [00 §12 Q8](00-ke-hoach-tong.md).

Ô hệ thống tính (Σ, bảng Thuế) dùng `displayOnly` — render chữ, không viền, không nằm trong tab order
(`helpers/anHien.ts:12`).

## 3. Ma trận Ẩn/Hiện · Disabled (dịch nguyên từ nguồn v2)

**Trục cột:** I = `ChungTuBan.TrangThaiGhiSo` — C1 "Chưa ghi sổ" · C2 "Đã ghi sổ".
**Điều kiện phụ:** `(đk-cfg)` trường/tab chỉ hiển thị khi thuộc **cấu hình đã lưu** của chứng từ ·
`(đk-HĐ)` trạng thái hóa đơn (`ChungTuBan.TrangThaiLapHoaDon`).

| Tab/Section | Thành phần | C1 Chưa ghi sổ | C2 Đã ghi sổ |
|---|---|:--:|:--:|
| Header Options | **Loại nghiệp vụ · Kiêm phiếu xuất kho** | Hide(at) | Hide(at) |
| Header Options | Lập kèm hóa đơn · Thu tiền ngay | Disable | Disable |
| Header Options | Hình thức thanh toán *(đk-cfg: Thu tiền ngay=True)* | Disable(đk-cfg) | Disable(đk-cfg) |
| Ghi nợ | Mã KH · Tên KH · MST/CCCD · Người liên hệ · Địa chỉ · NV bán hàng · Diễn giải · Ngày HT · Ngày CT · Số CT · Đã lập hóa đơn | Disable | Disable |
| Ghi nợ | Điều khoản TT · Số ngày được nợ · Hạn thanh toán *(đk-cfg: Không thu ngay)* | Disable(đk-cfg) | Disable(đk-cfg) |
| Tab Phiếu thu *(đk-cfg: Thu ngay-Tiền mặt)* | toàn bộ trường | Disable(đk-cfg) | Disable(đk-cfg) |
| Tab Giấy báo có *(đk-cfg: Thu ngay-Chuyển khoản)* | toàn bộ trường | Disable(đk-cfg) | Disable(đk-cfg) |
| Tab Hóa đơn *(đk-cfg: Lập kèm hóa đơn=True)* | toàn bộ trường | Disable(đk-cfg) | Disable(đk-cfg) |
| Loại tiền / CK | Loại tiền · Loại chiết khấu | Disable | Disable |
| Loại tiền / CK | Tỷ giá quy đổi *(đk-cfg)* · Ô nhập % *(đk-cfg)* | Disable(đk-cfg) | Disable(đk-cfg) |
| Chi tiết DV | Loại dòng dịch vụ · Diễn giải (ẩn) | Hide(at) | Hide(at) |
| Chi tiết DV | Cột chung (STT · Mã DV · Tên DV · CKTM · Hàng KM · TK công nợ · TK doanh thu · ĐVT · Số lượng · **Số lượng đã xuất HĐ** · Đơn giá · Thành tiền · Tài khoản CK · % thuế GTGT · Giá trị thuế GTGT · Tiền thuế GTGT · TK Thuế GTGT · Diễn giải thuế · HH không TH tờ khai GTGT) | Disable | Disable |
| Chi tiết DV | Cột quy đổi / chiết khấu theo cấu hình *(đk-cfg)* | Disable(đk-cfg) | Disable(đk-cfg) |
| Chi tiết DV (nút lưới) | Thêm dòng · Xóa dòng · Thêm ghi chú · Áp dụng · Phân bổ | **Hide** | **Hide** |
| Chi tiết DV | Dòng tổng (Σ) | Disable | Disable |
| Tab Thuế | bảng tổng hợp thuế GTGT | Disable | Disable |
| ~~Tab Hạch toán~~ | ~~bảng định khoản~~ | **BỎ — BA v2 xoá khỏi ma trận (D7)** | |
| Tab Tham chiếu | danh sách CT tham chiếu | Disable(at) | Disable(at) |
| **Nút** | Chỉnh sửa | Show | Hide |
| **Nút** | Ghi sổ | Show | Hide |
| **Nút** | Bỏ ghi sổ | Hide | Show |
| **Nút** | Lập hóa đơn *(đk-HĐ)* | Hide | Hide/Show(đk-HĐ) |
| **Nút** | Xóa | Show | Hide |
| **Nút** | Đóng | Show | Show |
| **Nút** 🆕 | **Xem dữ liệu ghi sổ** | Show *(đề xuất — thay tab Hạch toán vừa bị xoá, **C14/Q11**)* | Show |

**Lưu ý `Số lượng đã xuất HĐ`:** ở màn Xem, ma trận đưa cột này vào nhóm "Cột chung" (**hiện**,
`Disable`) — khác màn Thêm mới (`Hide(at)`). Xử lý: **ẩn ở Thêm mới, hiện ở Sửa/Xem**.

**Nút lưới = `Hide`, không phải `Disable`** — nguồn ghi rõ *"Không có các nút thao tác: Thêm dòng,
Xóa dòng, Thêm ghi chú, Áp dụng, Phân bổ"* (`SCR_CTbanDichVu_ChiTiet.md:19`). **Lệch** BR14.1 ("tất cả
control disabled") và lệch chốt của epic CTMH 00485 — ma trận tự ghi ở "Điểm cần xác nhận" #3.
**Theo nguồn của epic** (`Hide`), ghi rõ là lệch.

## 4. Trường & cột

Y hệt [02 §4](02-popup-them-moi.md) (tên field theo LDM v2), toàn bộ ở trạng thái read-only. Không có
trường mới.

## 5. Hành vi & sự kiện

| Nút | Điều kiện hiện | Quyền | Việc |
|---|---|---|---|
| **Chỉnh sửa** | `TrangThaiGhiSo = "Chưa ghi sổ"` | `BanDichVu.Edit` | mở popup Sửa ([03](03-popup-chinh-sua.md)). Lưu/Hủy ⇒ **quay lại popup này** (BR34) |
| **Ghi sổ** | `= "Chưa ghi sổ"` | `BanDichVu.Post` | [06](06-ghi-so-bo-ghi-so.md) |
| **Bỏ ghi sổ** | `= "Đã ghi sổ"` | `BanDichVu.Unpost` | [06](06-ghi-so-bo-ghi-so.md) |
| **Lập hóa đơn** | `= "Đã ghi sổ"` **AND** `TrangThaiLapHoaDon ∈ {Chưa lập, Đã lập một phần}` | quyền lập hóa đơn | **coming soon** — module hóa đơn chưa dựng |
| **Xóa** | `= "Chưa ghi sổ"` | `BanDichVu.Delete` | [05](05-popup-xac-nhan-xoa.md) |
| **Xem dữ liệu ghi sổ** 🆕 | luôn *(đề xuất)* | — | popup bút toán ([02 §5.4](02-popup-them-moi.md)) |
| **Đóng** / **×** / ESC | luôn | — | đóng popup, về danh sách. **Không** hỏi xác nhận |

**Quyền:** SCR ghi *"Quyền của người dùng được kiểm tra khi bấm nút chức năng"* — nhưng **BR25.2 nói
ẩn nút khi không có quyền, không disable**. Áp dụng BR25.2 (ẩn). Ghi rõ đây là **diễn giải BR25 chèn
lên câu của SCR** — cần BA xác nhận.

## 6. Validation phía FE

Không có nhập liệu ⇒ không có validation. Lỗi hiển thị:

| Tình huống | Message | Mã |
|---|---|---|
| Chứng từ không tồn tại | "Chứng từ không tồn tại" | _012 |
| Lỗi tải dữ liệu | "Lỗi hệ thống" | _013 |
| Không có quyền xem chi tiết | "Không có quyền truy cập" | _011 — **BE** trả 403 |

## 7. Luồng xử lý

1. Mở popup `mode='view'` + `rowId` → `useDetail(rowId)` (**cùng query key** với panel Xem nhanh ⇒ dữ
   liệu đã có trong cache, không tốn request thứ hai — `ChungTuBanHangTab.tsx:9-13`).
2. Map response → form values readonly; đọc `loaiNghiepVu` từ bản ghi.
3. Dựng `nguCanhAnHien` từ **cấu hình đã lưu** để quyết `(đk-cfg)`.
4. Bộ nút dựng từ `TrangThaiGhiSo` + `TrangThaiLapHoaDon` + quyền.
5. Loading: `UiSpin` phủ thân popup. Error: `CommonEmpty` + toast.

## 8. Phân bổ file

| Việc | File |
|---|---|
| Bộ nút theo trạng thái + quyền — hàm thuần | `helpers/trangThai.ts` (`coTheGhiSo:53`, `coTheBoGhiSo:58` đã có) + `helpers/quyen.ts` |
| Ẩn nút lưới ở mode `view` | `helpers/anHien.ts` (`nc.readOnly` đã có — `anHien.ts:48`) |
| Ráp UI + footer | `components/ChungTuBanHangThemMoiModal.tsx` (`mode='view'`) |
| Popup bút toán | `components/XemDuLieuGhiSoModal.tsx` 🆕 |
| Quay lại popup Xem sau khi Sửa (BR34) | `components/ChungTuBanHangTab.tsx` |
| Chữ | `i18n/vi.ts` · `en.ts` |

## 9. Kiểm thử

| # | Input | Kỳ vọng |
|---|---|---|
| T1 | `mode='view'` | mọi ô nhập `disabled`; 3 nút lưới và cột 🗑 **không render** |
| T2 | `TrangThaiGhiSo = "Chưa ghi sổ"` | footer có Chỉnh sửa · Ghi sổ · Xóa · Đóng; **không** có Bỏ ghi sổ / Lập hóa đơn |
| T3 | "Đã ghi sổ", `TrangThaiLapHoaDon = "Chưa lập"` | footer có Bỏ ghi sổ · Lập hóa đơn · Đóng |
| T4 | "Đã ghi sổ", `TrangThaiLapHoaDon = "Đã lập đủ"` | **không** có Lập hóa đơn |
| T5 | "Chưa ghi sổ", user không có `.Edit` | **ẩn** nút Chỉnh sửa (không disable) |
| T6 | chứng từ Không thu ngay | **không** render tab Phiếu thu / Giấy báo có; **có** khối Điều khoản thanh toán (read-only) |
| T7 | chứng từ Loại tiền = VND | **không** render cột quy đổi |
| T8 | lưới chi tiết | cột `Số lượng đã xuất HĐ` **hiện**, read-only |
| T9 | bấm Chỉnh sửa → Lưu | quay lại popup Xem, dữ liệu đã cập nhật (BR34) |
| T10 🆕 | `mode='view'` | **không** render tab Hạch toán |

## 10. BR đã áp dụng

**Chung:** BR3 · BR7 · BR12 · BR13.2 · BR14.1 (chế độ Xem) · BR18 · BR25 · BR26 · BR33 · BR34 · BR42.2.
**Của CTBH:** BR05 (trạng thái lập hóa đơn) · BR21 · BR24.

**Chưa đạt / lệch:**
- **BR13.2** — thiếu nút **"In"** và **"Nhân bản"** (BA không liệt kê) ⇒ [00 §12 Q6](00-ke-hoach-tong.md).
- **BR14.1** — nút lưới ở chế độ Xem theo BA là `Hide`, BR nói "disabled". Theo BA, ghi rõ là lệch.
- **BR41** — Tab Tham chiếu chưa dựng ⇒ [00 §12 Q5](00-ke-hoach-tong.md).
- **Nút "Xem dữ liệu ghi sổ"** ở màn Xem là **đề xuất của FE** (BA chưa khai ở `SCR_CTbanDichVu_ChiTiet.md`)
  ⇒ [00 §12 Q11](00-ke-hoach-tong.md).
