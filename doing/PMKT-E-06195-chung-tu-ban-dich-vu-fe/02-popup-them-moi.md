# 02 — Popup Thêm mới Chứng từ bán dịch vụ

| | |
|---|---|
| **Phiên bản** | **v2 — 2026-08-15** (đồng bộ BA commit `1a928c53b`) |
| **SCR nguồn** | `5.screens/SCR_CTbanDichVu_ThemMoi.md` (màn anchor của epic) |
| **UC nguồn** | `UC_CTbanDichVu_ThemMoi` (AC1–AC5) |
| **Ma trận** | `Matrix/.../SCR_CTbanDichVu_ThemMoi_MaTranAnHien.md` — **[DRAFT — chờ duyệt]** |
| **Figma** | **Nguyên tệ** [section 61661:103452](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/?node-id=61661-103452) → modal **61661:104737** · Hóa đơn **61661:105191** · Phiếu thu **61661:105660** · Chuyển khoản **61661:106254** · Thêm ghi chú **61661:103453** · Tab Thuế **61661:103826** · Tab Tham chiếu **61661:103899** · **Xem dữ liệu ghi sổ 61661:104532** · Phân bổ CK **61661:108086** / **61661:109133**<br>**Ngoại tệ** [section 61685:126981](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/?node-id=61685-126981) → modal **61685:127083** |
| **Route** | không có — popup mở từ lưới `/ban-hang/chung-tu-ban-hang` |
| **Quyền** | `BanDichVu.Create` (Lưu) · `BanDichVu.Create` **AND** `BanDichVu.Post` (Lưu và ghi sổ) |

---

## 1. Bố cục (đọc từ Figma v2 — modal 61661:104737)

```
┌ Modal Header ─────────────────────────────────────────────────────────────────┐
│ "Thêm chứng từ bán dịch vụ"   [⚙|Chọn chứng từ ▾|≡🔍]        [⌨] [?] [×]      │
├───────────────────────────────────────────────────────────────────────────────┤
│ ☐ Lập kèm hóa đơn   ☐ Thu tiền ngay   [· Hình thức thanh toán ▾ khi tick]      │  ← Header Options
│   (KHÔNG có "Loại nghiệp vụ", KHÔNG có "Kiêm phiếu xuất kho" — BR24)           │
├─ Thẻ "Nhập" ──────────────────────────────────────────────────────────────────┤
│ ┌ tab: Chứng từ ghi nợ | (Phiếu thu | Giấy báo có) | Hóa đơn ────────────────┐ │
│ │ lưới 4 cột × 4 hàng field                                                  │ │
│ └────────────────────────────────────────────────────────────────────────────┘ │
├─ Thẻ lưới ────────────────────────────────────────────────────────────────────┤
│ tab: Chi tiết dịch vụ | Thuế | ⚠Đính kèm | Tham chiếu                          │
│               phải: Loại tiền [VND ▾]  Chiết khấu [Không chiết khấu ▾]         │
│                     (+ Tỷ giá khi ngoại tệ — C17) (+ ô % · [Áp dụng] · [Phân bổ])│
│ ┌ CommonEditableGrid ────────────────────────────────────────────────────────┐ │
│ │ …cột chi tiết dịch vụ…                                          [🗑]        │ │
│ │ Tổng:                                                                      │ │
│ └────────────────────────────────────────────────────────────────────────────┘ │
│ [+ Thêm dòng] [🗒 Thêm ghi chú] [🗑 Xóa hết dòng]   1-20 trên 20  ‹ 1 ›  20/trang│
├───────────────────────────────────────────────────────────────────────────────┤
│                                       Tổng tiền hàng          1.960.000.000    │
│                                       Tiền chiết khấu         (392.000.000)    │
│                                       ⚠Chi phí                          0      │
│                                       Tiền thuế GTGT            156.800.000    │
│                                       ────────────────────────────────────     │
│                                       Tổng tiền thanh toán    1.724.800.000    │
├───────────────────────────────────────────────────────────────────────────────┤
│ [Hủy]                    [Xem dữ liệu ghi sổ]           [Lưu] [Lưu và ghi sổ]  │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Khác popup Chứng từ bán hàng (`ChungTuBanHangThemMoiModal.tsx`):**

1. Header Options **ẩn** `Loại nghiệp vụ` (cố định `Bán dịch vụ`) và `Kiêm phiếu xuất kho` — BR24.
2. **Không** có tab `Phiếu xuất kho`.
3. **Không** có khối `Thông tin bổ sung` (Figma v2 vẫn không vẽ → xác nhận giả định của Matrix).
4. **Không** có tab `Hạch toán` 🆕 — BA v2 xoá; thay bằng nút footer **"Xem dữ liệu ghi sổ"** (§5.3).
5. Lưới chi tiết bỏ nhóm cột kho / giá vốn / ĐVT quy đổi / thuế XK.
6. Footer có **4** nút (thêm "Xem dữ liệu ghi sổ") thay vì 3.

**Biến thể ngoại tệ (61685:127083):** cùng bố cục, khác 3 chỗ — lưới thêm `Thành tiền quy đổi` ·
`Tiền thuế GTGT quy đổi`; khối tổng thành **2 cột `(USD) | (VND)`**; khối tổng **không** có dòng
"Chi phí" (⇒ **C16**).

## 2. Đặc tả UI từ Figma

| Thành phần | Component `@base` dùng lại | Kích thước / ghi chú |
|---|---|---|
| Vỏ popup | `CommonModalShell` + `MODAL_WIDTH_COMPLEX` (`ChungTuBanHangThemMoiModal.tsx:44,47`) | thân 1.126px trong khung 1.158px |
| Cụm "Chọn chứng từ" ở header | `HeaderControls` (`src/base/index.ts:277`) | ⚙ + select 263px + ≡🔍 |
| Hàng Header Options | `CommonCheckbox` (`:176`) + `CommonSelectBox` (`:572`) | select Hình thức TT rộng `HINH_THUC_TT_WIDTH = 160` (`constants.ts:134`) |
| Tab thẻ "Nhập" · thẻ lưới | `TabMenuChild` (`:144`) | tab active gạch chân đỏ |
| Lưới chi tiết | `CommonEditableGrid` (`:535`) | hàng 56px · header 44px · `CHI_TIET_PAGE_SIZE = 20` (`constants.ts:116`) |
| Cột "Chức năng" | icon 🗑 | `CHUC_NANG_COL_WIDTH = 96` (`constants.ts:146`) |
| Bảng Thuế · Tham chiếu · popup ghi sổ | `CommonListTable` (`:310`) | read-only |
| Khối tổng | `TongHopPanel.tsx` | `TOTALS_WIDTH = 364` (`constants.ts:149`); ngoại tệ ⇒ 2 cột |
| Footer | `CommonButton` | Hủy trái · **Xem dữ liệu ghi sổ** · Lưu · Lưu và ghi sổ phải (BR3) |
| Ngày | `CommonDateInput` (`:164`), `DATE_FORMAT = 'DD/MM/YYYY'` (`constants.ts:122`) | |
| Số | `CommonNumberInput` (`:160`) | BR7 |

**Chưa xác định (đo lại node con khi code):** spacing giữa các hàng field, cỡ chữ label. Figma dùng
đúng bộ component của CTBH ⇒ các trị này **kế thừa** từ bản đã dựng, không phát minh trị mới.

## 3. Ma trận Ẩn/Hiện · Disabled (dịch nguyên từ `SCR_CTbanDichVu_ThemMoi_MaTranAnHien.md`)

**Trục cột:** I1 = trạng thái thanh toán (a Không thu ngay · b Thu ngay+Tiền mặt · c Thu ngay+Chuyển
khoản) × I2 = Lập kèm hóa đơn (0 Không · 1 Có) ⇒ **6 cột**.
**Điều kiện phụ không lên cột:** `(đk-LT)` Loại tiền ≠ đồng tiền hạch toán · `(đk-CK)` Loại chiết
khấu · `(đk-TT)` Hình thức TT trong Tab Hóa đơn = Chuyển khoản.

| Tab/Section | Thành phần | C1 KhôngTN·KhôngHĐ | C2 KhôngTN·CóHĐ | C3 TM·KhôngHĐ | C4 TM·CóHĐ | C5 CK·KhôngHĐ | C6 CK·CóHĐ |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Header | **Loại nghiệp vụ** 🆕 | Hide(at) | Hide(at) | Hide(at) | Hide(at) | Hide(at) | Hide(at) |
| Header | **Kiêm phiếu xuất kho** 🆕 | Hide(at) | Hide(at) | Hide(at) | Hide(at) | Hide(at) | Hide(at) |
| Header | Lập kèm hóa đơn · Thu tiền ngay | Show | Show | Show | Show | Show | Show |
| Header | Hình thức thanh toán | Hide | Hide | Show | Show | Show | Show |
| Ghi nợ | Mã KH · Tên KH · MST/CCCD · Người liên hệ · Địa chỉ · NV bán hàng · Diễn giải | Show | Show | Show | Show | Show | Show |
| Ghi nợ | Điều khoản TT · Số ngày được nợ · Hạn thanh toán | Show | Show | Hide | Hide | Hide | Hide |
| Ghi nợ | Ngày hạch toán · Ngày chứng từ · Số chứng từ | Show | Show | Show | Show | Show | Show |
| Ghi nợ | Đã lập hóa đơn (checkbox) | Show | Show | Show | Show | Show | Show |
| Phiếu thu | toàn bộ trường | Hide | Hide | Show | Show | Hide | Hide |
| Giấy báo có | trường nhập | Hide | Hide | Hide | Hide | Show | Show |
| Giấy báo có | Tên ngân hàng nhận (auto-fill) | Hide | Hide | Hide | Hide | Disable | Disable |
| Hóa đơn | trường HĐ (14 trường) | Hide | Show | Hide | Show | Hide | Show |
| Hóa đơn | Tài khoản NH *(đk-TT)* | Hide | Show(đk-TT) | Hide | Show(đk-TT) | Hide | Show(đk-TT) |
| Lưới-header | Loại tiền · Loại chiết khấu | Show ×6 | | | | | |
| Lưới-header | Tỷ giá quy đổi *(đk-LT)* | Show(đk-LT) ×6 — ⚠ **C17** | | | | | |
| Lưới-header | Ô nhập % · nút Áp dụng · nút Phân bổ CK *(đk-CK)* | Show(đk-CK) ×6 | | | | | |
| Chi tiết DV | STT | Disable ×6 | | | | | |
| Chi tiết DV | Loại dòng dịch vụ · Diễn giải (ẩn) · Số lượng đã xuất HĐ | Hide(at) ×6 — ⚠ **C16** ở bản ngoại tệ | | | | | |
| Chi tiết DV | Mã DV · Tên DV · CKTM · Hàng KM · TK công nợ · TK doanh thu · ĐVT · Số lượng · Đơn giá · Thành tiền · Tài khoản CK · % thuế GTGT · Giá trị thuế GTGT · Tiền thuế GTGT · TK thuế GTGT · Diễn giải thuế · HH không TH tờ khai GTGT | Show ×6 | | | | | |
| Chi tiết DV | Thành tiền quy đổi · Tiền CK quy đổi *(đk-LT)* | Show(đk-LT) ×6 | | | | | |
| Chi tiết DV | Tiền thuế GTGT quy đổi *(đk-LT, auto)* | Disable(đk-LT) ×6 | | | | | |
| Chi tiết DV | Tỷ lệ CK (%) · Tiền CK *(đk-CK)* | Show(đk-CK) ×6 | | | | | |
| Chi tiết DV | Cột CK auto-calc (theo mặt hàng · theo hóa đơn + quy đổi) *(đk-CK)* | Disable(đk-CK) ×6 | | | | | |
| Nút lưới | Thêm dòng · Thêm ghi chú · Xóa hết dòng | Show ×6 | | | | | |
| Chi tiết DV | Dòng tổng theo tiền hạch toán (Σ) | Disable ×6 | | | | | |
| Chi tiết DV | Dòng tổng theo loại tiền (Σ) *(đk-LT)* | Disable(đk-LT) ×6 | | | | | |
| Thuế | bảng tổng hợp thuế GTGT | Disable ×6 | | | | | |
| ~~Hạch toán~~ | ~~bảng định khoản tự động~~ | **BỎ — BA v2 xoá tab (D7)** | | | | | |
| Tham chiếu | danh sách CT tham chiếu | Disable(at) ×6 | | | | | |
| Nút | Lưu · Lưu và ghi sổ · Hủy | Show ×6 | | | | | |
| Nút 🆕 | **Xem dữ liệu ghi sổ** | Show ×6 *(theo Figma — **C14**, BA chưa khai)* | | | | | |

**Điều kiện mức DÒNG (không lên cột):**

| Điều kiện | Hệ quả | Helper đã có |
|---|---|---|
| Dòng ghi chú (`Loại dòng dịch vụ = False`) | khóa **mọi** ô trừ "Tên dịch vụ" | `helpers/anHien.ts:102 khoaVìDongGhiChu` |
| Dòng Hàng khuyến mại hoặc CKTM | khóa 3 ô chiết khấu của dòng | `:115 khoaCotChietKhauDong` |
| Tick "Hàng KM" ⇔ tick "CKTM" | loại trừ nhau | `:120`, `:124` |
| `% thuế GTGT = KHAC` | hiện ô "Giá trị thuế GTGT" | `:134 hienGiaTriThueGtgt` |
| `% thuế GTGT ∈ {KHAC, KKKNT}` | ép tick + disable "HH không TH tờ khai GTGT" | `:147 epKhongTongHopToKhai` |

**Ánh xạ ký hiệu → code** (`helpers/anHien.ts:10-13`): `Hide` → `visible: false` · `Disable` (ô nhập)
→ `disabled: true` · `Disable` (ô hệ thống tính) → `displayOnly` · `Show` → hiện + nhập được.

**⚠ Ma trận đang `[DRAFT]`.** Xem [00 §12 Q8](00-ke-hoach-tong.md).

## 4. Trường & cột

> **Tên field đã đổi theo LDM v2** — mọi tiền tố `ChungTuBanDichVu.*` / `ChiTietChungTuBanDV.*` của
> bản v1 **không còn đúng**.

### 4.1 Header Options

| Trường | Control | **Field v2** | Bắt buộc | Mặc định | Ghi chú |
|---|---|---|---|---|---|
| **Loại nghiệp vụ** | Select | `ChungTuBan.LoaiNghiepVu` | Y | **`Bán dịch vụ`** | **Ẩn khỏi UI**, cố định, **bất biến sau khi lưu** (BR24 · [00 D6](00-ke-hoach-tong.md)). Vẫn nằm trong form store + payload |
| **Kiêm phiếu xuất kho** | CheckBox | `ChungTuBan.KiemPhieuXuatKho` | N | — | **Ẩn** — dịch vụ không xuất kho (BR24) |
| Lập kèm hóa đơn | CheckBox | `ChungTuBan.LapKemHoaDon` | N | CTBH khai `Checked`; **Figma CTBDV vẽ bỏ tick** | ⚠ lệch nguồn — đề xuất theo Figma (Unchecked), chốt khi review. Tham chiếu **BR05** |
| Thu tiền ngay | CheckBox | `ChungTuBan.ThuTienNgay` | N | Unchecked | **BR04** · **BR18** |
| Hình thức thanh toán | Select | `ChungTuBan.HinhThucThanhToan` | Y (khi hiện) | Tiền mặt | Tiền mặt ⇒ Tab Phiếu thu · Chuyển khoản ⇒ Tab Giấy báo có. **BR04** |

### 4.2 Tab Chứng từ ghi nợ (14 trường)

Bộ trường **y hệt** CTBH (`SCR_CTBH_ThemMoi.md` § Tab Chứng từ ghi nợ) — Figma v2 xác nhận từng ô:

| Trường | Control | **Field v2** | Max | Bắt buộc | Mặc định | Tham chiếu |
|---|---|---|---|---|---|---|
| Mã Khách hàng | CombogridSearchFlatGrid | `ChungTuBan.KhachHangId` | — | **Y** | — | BR01 |
| Tên khách hàng | TextField | `ChungTuBan.TenKhachHang` | 255 | N | Auto-fill | BR01 |
| Mã số thuế/CCCD chủ hộ | InputNumber | **`ChungTuBan.MaSoThueCCCD`** | 14 | N | Auto-fill | BR01 |
| Người liên hệ | TextField | `ChungTuBan.NguoiLienHe` | 50 | N | Auto-fill | BR01 |
| Địa chỉ | TextField | `ChungTuBan.DiaChi` | 400 | N | Auto-fill | BR01 |
| Nhân viên bán hàng | CombogridSearchFlatGrid | `ChungTuBan.NhanVienBanHangId` | — | N | Auto-fill | BR01 |
| Diễn giải | TextArea | **`ChungTuBan.DienGiai`** | 500 | N | template §7.1 | BR01 · BR15 |
| Điều khoản thanh toán | CombogridSearchFlatGrid | `ChungTuBan.DieuKhoanThanhToanId` | — | N | Auto-fill | BR01 |
| Số ngày được nợ | InputNumber | `ChungTuBan.SoNgayDuocNo` | 50 | N | Auto-fill | BR01 |
| Hạn thanh toán | DatePicker | `ChungTuBan.HanThanhToan` | — | N | auto-calc | BR03 |
| Ngày hạch toán | DateTimePicker | `ChungTuBan.NgayHachToan` | — | **Y** | Ngày hiện tại | BR02 |
| Ngày chứng từ | DatePicker | `ChungTuBan.NgayChungTu` | — | **Y** | Ngày hiện tại | BR02 |
| Số chứng từ | TextField | `ChungTuBan.SoChungTu` | 50 | **Y** | — | — |
| Đã lập hóa đơn | CheckBox | `ChungTuBan.DaLapHoaDon` | — | N | Unchecked | BR05 |

Placeholder "Điều khoản thanh toán": Figma v2 **đã sửa** thành "Chọn điều khoản thanh toán" (C9 hết).

### 4.3 Tab Phiếu thu / Giấy báo có / Hóa đơn

Tham chiếu nguyên `SCR_CTBH_ThemMoi.md`. Component **dùng lại nguyên**: `components/ThuTienTab.tsx`,
`components/HoaDonTab.tsx`.

**Tab Phiếu thu — field v2:** `ChungTuBan.KhachHangId · TenKhachHang · NguoiNopTien(100) ·
DiaChi(400) · NhanVienBanHangId · LyDoThu(500) · TaiKhoanTienId* · NgayHachToan* ·
NgayChungTuThuTien* · SoChungTuThuTien*(50)`. Mặc định `TaiKhoanTienId` = TK `111x` đầu tiên trên DM
Hệ thống tài khoản (**BR16**).

> ⚠ **Q10 — mâu thuẫn nguồn:** `SCR_CTbanDichVu_ThemMoi.md:35` (mới thêm) nói *"tích Thu tiền ngay
> **tự nó đóng vai phiếu thu — không sinh bản ghi `ENT_PhieuThu`**; dữ liệu lưu trên `ChungTuBan`"*,
> nhưng `UC_CTbanDichVu_ThemMoi.md:15` AC3 vẫn ghi *"Cả hai **sinh ENT_PhieuThu**"* và
> `3.crud-matrix.md:22` vẫn để `ENT_PhieuThu` = C/D. **Chốt trước khi code payload.**
> Field name (`ChungTuBan.*`) ủng hộ phương án "không sinh bản ghi riêng".

### 4.4 Lưới "Chi tiết dịch vụ"

| # | Cột | **Field v2** (`ChiTietChungTuBan.*`) | Kiểu | Định dạng (BR7) | Sửa được | Nguồn |
|---|---|---|---|---|---|---|
| 1 | STT | — | number | — | N (Disable) | Matrix |
| — | *Loại dòng dịch vụ* | `LoaiDongHang` | bool | — | — | **cột ẩn** (at) |
| — | *Diễn giải (ẩn)* | **`DienGiai`** | text | — | — | **cột ẩn** (at); auto-fill theo Tên dịch vụ — **BR15** |
| 2 | Mã dịch vụ | `VatTuId` | Combogrid | — | Y | BR02 — chỉ vật tư `Loại = Dịch vụ` |
| 3 | Tên dịch vụ | `TenHang` | text | — | Y | auto-fill |
| 4 | Chiết khấu thương mại | `ChietKhauThuongMai` | checkbox | — | Y | **BR09** |
| 5 | Hàng khuyến mại | `HangKhuyenMai` | checkbox | — | Y | **BR09** — dòng KM của dịch vụ không phát sinh giá vốn/xuất kho; ghi nhận doanh thu theo giá trị người dùng nhập |
| 6 | TK Công nợ | `TaiKhoanCongNoId` | Combogrid TK | — | Y | auto-fill BR07 · TK ngầm định **BR16** |
| 7 | TK doanh thu | `TaiKhoanDoanhThuId` | Combogrid TK | — | Y | như trên |
| 8 | ĐVT | `DonViTinhId` | select | — | Y | auto-fill BR07 |
| 9 | Số lượng | `SoLuong` | number | `18,3` | Y | ≥ 0 · **BR11** |
| 10 | *Số lượng đã xuất HĐ* | `SoLuongDaXuatHD` | number | `18,3` | N | `Hide(at)` ở Thêm mới. ⚠ **C16** — Figma ngoại tệ vẫn vẽ |
| 11 | Đơn giá | `DonGia` | number | `18,2` / ngoại tệ `18,4` | Y | ≥ 0 · **BR11** |
| 12 | Thành tiền | `ThanhTien` | number | `18,2` | Y (2 chiều) | = SL × ĐG · **BR11** · BR18.3 |
| 13 | Thành tiền quy đổi *(đk-LT)* | `ThanhTienQuyDoi` | number | `18,2` | Y | BR18 |
| 14 | Tỷ lệ CK (%) *(đk-CK)* | `ChietKhauPhanTram` | number | `5,2` | Y | ≤ 100 · **BR12** |
| 15 | Tiền chiết khấu *(đk-CK)* | `ChietKhau` | number | `18,2` | Y | ≤ Thành tiền dòng · **BR12** |
| 16 | Tiền CK quy đổi *(đk-LT,đk-CK)* | `ChietKhauQuyDoi` | number | `18,2` | N | auto |
| 17 | Tỷ lệ/Tiền CK theo mặt hàng · theo hóa đơn *(đk-CK)* | `PhanTram/TienChietKhauHang`, `…HoaDon` (+ quy đổi) | number | `18,2` | N (Disable) | **BR12** |
| 18 | Tài khoản CK | `TaiKhoanChietKhauId` | Combogrid TK | — | Y | **BR16**. ⚠ **C2** — Figma không vẽ |
| 19 | % thuế GTGT | `ThueSuatGtgt` | select | `0·5·8·10·KCT·KKKNT·KHAC` | Y | `constants.ts:51`. **Không** lọc theo xuất khẩu — dịch vụ xử lý **giống Bán hàng trong nước** (BR24 · **BR13**) |
| 20 | Giá trị thuế GTGT | `GiaTriThueGtgt` | number | `5,2`, 0 ≤ x < 100 | Y | chỉ hiện khi `% = KHAC` (`constants.ts:160`) |
| 21 | Tiền thuế GTGT | `TienThueGtgt` | number | `18,2` | Y | auto, cho ghi đè · **BR13** |
| 22 | Tiền thuế GTGT quy đổi *(đk-LT)* | `TienThueGtgtQuyDoi` | number | `18,2` | N | auto |
| 23 | TK thuế GTGT | `TaiKhoanThueGtgtId` | Combogrid TK | — | Y | **BR16** |
| 24 | Diễn giải thuế | `DienGiaiThue` | text | — | Y | mặc định `Thuế GTGT - [Tên dịch vụ]` · **BR15**. ✅ Figma v2 đã có |
| 25 | HH không TH trên tờ khai thuế GTGT | `KhongTongHopToKhaiGTGT` | checkbox | mặc định `False` | Y/ép | **sau** cột Diễn giải thuế; ép tick + disable khi `% ∈ {KHÁC, KKKNT}` · **BR13 mục 7**. ✅ Figma v2 đã có |
| 26 | Chức năng | — | icon 🗑 | — | — | xóa dòng |

**KHÔNG có** (dịch vụ — BR17 · BR19 · BR24): Kho · Giá vốn · Tiền vốn · Lô · Hạn sử dụng · Mã quy
cách · TK kho · TK giá vốn · Đơn giá vốn · Tự nhập đơn giá vốn · Hệ số quy đổi · Số lượng quy đổi ·
Đơn giá quy đổi · mọi cột Thuế XK (**BR14**).

**Có trong Figma v2 nhưng BA không nêu** (không code — **C5**): `Đối tượng THCP · Vụ việc · Đơn vị ·
Khoản mục chi phí · Hợp đồng bán · Đơn đặt hàng`.

**Nhãn cột — theo BA, không theo Figma (C12):** Figma v2 vẫn ghi "Mã hàng hóa"/"Tên hàng hóa" (dùng
lại component CTBH); BA yêu cầu **"Mã dịch vụ"/"Tên dịch vụ"/"Tổng tiền dịch vụ"**.

### 4.5 Khối tổng

| Dòng | Nguồn | Ghi chú |
|---|---|---|
| Tổng tiền hàng | Σ `ThanhTien` → `ChungTuBan.TongTienHang` | |
| Tiền chiết khấu | Σ `ChietKhau` → `ChungTuBan.TongChietKhau` | trong ngoặc, màu đỏ — `helpers/tongHop.ts:105` |
| **Chi phí** | — | ⚠ **C6** — Nguyên tệ có, Ngoại tệ không, BA không nhắc ⇒ **không render** đến khi BA định nghĩa |
| Tiền thuế GTGT | Σ `TienThueGtgt` → `ChungTuBan.TongThueGTGT` | |
| **Tổng tiền thanh toán** | `ChungTuBan.TongThanhToan` = Tổng tiền hàng − CK + Thuế | màu xanh, đậm |

Ngoại tệ ⇒ hai cột `(USD)` và `(VND)`.

## 5. Hành vi & sự kiện

### 5.1 Điều khiển chính

| Thành phần | Điều kiện hiện | Việc |
|---|---|---|
| Tick "Thu tiền ngay" | luôn | hiện ô Hình thức TT; **ẩn** khối Điều khoản TT/Số ngày nợ/Hạn TT; mở Tab Phiếu thu hoặc Giấy báo có (**BR04** · **BR18**) |
| Select Hình thức TT | `thuTienNgay = true` | Tiền mặt ⇒ Tab Phiếu thu · Chuyển khoản ⇒ Tab Giấy báo có |
| Tick "Lập kèm hóa đơn" | luôn | hiện Tab Hóa đơn; đồng bộ với ô "Đã lập hóa đơn" theo **BR05** (`helpers/dongBo.ts:181 trangThaiOTickHoaDon`) |
| Select Loại tiền | luôn | ≠ đồng tiền hạch toán ⇒ hiện Tỷ giá + 4 cột quy đổi + khối tổng nguyên tệ (**BR18**) |
| Select Loại chiết khấu | luôn | đổi bộ cột CK; đổi nút Áp dụng/Phân bổ (`helpers/chietKhau.ts:100-132`) · **BR12** |
| Nút **Áp dụng** | Loại CK = "Theo % hóa đơn" | `apDungPhanTramHoaDon` (`chietKhau.ts:53`) |
| Nút **Phân bổ chiết khấu** | Loại CK ∈ {theo số tiền trên tổng HĐ, theo mặt hàng và hóa đơn} | mở `PhanBoChietKhauModal.tsx` (Figma **61661:108086** / **61661:109133**) |

### 5.2 Nút lưới

| Nút | Việc |
|---|---|
| **Thêm dòng** | chèn **ngay dưới dòng đang focus**; không focus ⇒ cuối bảng; đánh lại STT; focus ô đầu tiên của dòng mới (**BR21.2**) |
| **Thêm ghi chú** | thêm dòng `LoaiDongHang = False` — **không** có ô Kho, **không** auto-fill theo Mã dịch vụ (`SCR_CTbanDichVu_ThemMoi.md` §Dòng ghi chú). Figma có frame riêng **61661:103453** |
| **Xóa hết dòng** | xóa toàn bộ dòng. **Không** hỏi xác nhận (BR21.1 "Xác nhận trước xóa: mặc định tắt") |
| 🗑 cột Chức năng | xóa dòng đó |

### 5.3 Nút footer

| Nút | Điều kiện hiện | Việc | Message |
|---|---|---|---|
| **Hủy** / **×** / ESC / click ngoài | luôn | có thay đổi ⇒ popup xác nhận đóng (BR3: *"Dữ liệu đã có thay đổi. Bạn có chắc chắn muốn đóng? Thay đổi sẽ không được lưu."*) | — |
| **Xem dữ liệu ghi sổ** 🆕 | luôn *(theo Figma — **C14**)* | mở popup read-only bút toán (§5.4) | — |
| **Lưu** | có `BanDichVu.Create` | validate → `POST` với `ghiSo: false` | **MSG_PMKT-E-06195_001** "Thêm mới chứng từ thành công" |
| **Lưu và ghi sổ** | có `.Create` **AND** `.Post` | validate → `POST` với `ghiSo: true` (**một** request, **một** transaction — **BR21**) | **MSG_PMKT-E-06195_004** "Lưu và ghi sổ chứng từ thành công" |

**Trạng thái form sau lỗi:** giữ nguyên dữ liệu đã nhập, highlight ô vi phạm, **không** reset/đóng.
Form chỉ đóng khi lưu thành công hoặc user chủ động Hủy/×.
**BR15.4:** lỗi ⇒ border đỏ + text đỏ dưới ô + scroll tới ô lỗi đầu tiên + **tự chuyển sang tab chứa
lỗi**.

### 5.4 Popup "Xem dữ liệu ghi sổ" 🆕 (Figma 61661:104532)

Thay thế Tab Hạch toán vừa bị BA xoá ([00 D7](00-ke-hoach-tong.md)).

```
┌ Xem dữ liệu ghi sổ                                                   [?] [×] ┐
│ ┌ CommonListTable (read-only) ───────────────────────────────────────────┐   │
│ │ # │Ngày hạch toán│Ngày chứng từ│Số chứng từ│Mã đối tượng│Tên đối tượng│  │   │
│ │   │Diễn giải│Tài khoản│Tài khoản đối ứng│Phát sinh nợ│Phát sinh có│     │   │
│ │   │Vụ việc│Khoản mục chi phí│Đối tượng tập hợp chi phí│Đơn vị          │   │
│ │ Tổng:                                    92.500.000    92.500.000      │   │
│ └────────────────────────────────────────────────────────────────────────┘   │
│                                     1-10 trên 10  ‹ 1 ›  20 / trang           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                    [Đóng]     │
└───────────────────────────────────────────────────────────────────────────────┘
```

- "Số chứng từ" là **link** (màu xanh trong Figma).
- Dòng **Tổng** cộng `Phát sinh nợ` / `Phát sinh có` — hai số phải **bằng nhau**.
- Bút toán sinh theo §7.4; **không gộp** dòng cùng tài khoản (**BR36** · **BR20** của CTBH).
- Với bán dịch vụ **không có** dòng "Giá vốn hàng bán" (ảnh Figma là ví dụ chung của CTBH).
- Nguồn dữ liệu: **chưa có endpoint** ⇒ dựng tại chỗ từ `helpers/hachToan.ts:49 sinhButToan` trên dữ
  liệu form. Khi BE có API bút toán thật thì chuyển sang đọc server (ghi nhận là **nợ**).

## 6. Validation phía FE

| # | Điều kiện | Message (nguyên văn `6.messages.md`) | Mã | Ai kiểm |
|---|---|---|---|---|
| V1 | Trường `*` để trống | "[Tên trường] không được để trống" | BR15.1 | FE |
| V2 | Phải có ít nhất 1 dòng chi tiết | "Phải có ít nhất 1 dòng chi tiết" | _007 | FE |
| V3 | Ngày hạch toán ≥ Ngày chứng từ | "Ngày hạch toán phải lớn hơn hoặc bằng ngày chứng từ" | _008 | FE |
| V4 | Ngày chứng từ ≤ ngày hiện tại | "Ngày chứng từ không được lớn hơn ngày hiện tại" | _036 | FE |
| V5 | Số lượng ≥ 0 | "Số lượng không được âm" | _040 | FE |
| V6 | Đơn giá ≥ 0 | "Đơn giá không được âm" | _041 | FE |
| V7 | % Chiết khấu ≤ 100 | "% Chiết khấu không được vượt quá 100%" | _043 | FE |
| V8 | Tiền CK ≤ Thành tiền dòng | "Tiền CK không được vượt quá thành tiền của dòng" | _044 | FE — `helpers/kiemTra.ts:54` |
| V9 | Σ tiền CK các dòng = tổng CK chứng từ | "Tổng tiền chiết khấu các dòng không khớp với tổng tiền chiết khấu của chứng từ" | _046 | FE — `kiemTra.ts:80` |
| V10 | Σ tỷ lệ phân bổ = 100% | "Tổng tỷ lệ phân bổ phải bằng 100%" | _048 | FE — `kiemTra.ts:70`, sai số `SAI_SO_PHAN_BO` (`constants.ts:167`) |
| V11 | MaxLength mọi ô | *(không báo lỗi — chặn nhập im lặng, BR14.4)* | — | FE — `constants.ts:170 MAX_LEN` |
| V12 | Trim đầu/cuối khi blur + trước submit | — | BR43 | FE |
| **V13** | Số chứng từ không trùng | "Số chứng từ đã tồn tại" | _006 | **BE** (BR19.1) |
| **V14** | Mã khách hàng tồn tại | "Mã khách hàng không tồn tại" | _037 | **BE** |
| **V15** | Mã dịch vụ tồn tại | "Mã dịch vụ [{maDichVu}] không tồn tại" | _038 | **BE** |
| **V16** | Tài khoản là cấp cuối | "Tài khoản {tenTK} không phải là tài khoản cấp cuối. Vui lòng chọn tài khoản chi tiết." | _055 | **BE** |
| **V17** | SL lập HĐ ≤ SL còn lại được xuất | "Số lượng lập hóa đơn [{soLuongMoi}] vượt quá số lượng còn lại được phép xuất [{soLuongConLai}] trên Chứng từ bán dịch vụ gốc." | _102 | **BE** (**BR04** → **BR23** của CTBH) |
| **V18** | SL ≤ SL còn lại của Đơn đặt hàng nguồn | "Số lượng nhập vào lớn hơn số lượng còn lại của Đơn đặt hàng nguồn" | _104 | **BE** (**BR05**) — chặn ngay khi Lưu |
| **V19** | Kỳ kế toán chưa khóa | *(message của BE)* | BR17 | **BE** |
| **V20** | Chứng từ đang được người khác sửa | "Chứng từ đang được người khác chỉnh sửa. Vui lòng thử lại sau" | _105 | **BE** (BR12) |

> ⚠ `SCR_CTbanDichVu_ThemMoi.md` §Validate ghi chữ khác `6.messages.md` ở 4 dòng (_007 "…dịch vụ",
> _043 "Tỷ lệ chiết khấu…", _044 "Tiền chiết khấu không được lớn hơn thành tiền", _046 "…phải bằng
> số tổng"). **Lấy `6.messages.md` làm chuẩn**; ghi vào biên bản review.

## 7. Luồng xử lý

### 7.1 Auto-fill Diễn giải (BR01 riêng của CTBDV)

Trường **`ChungTuBan.DienGiai`** — **diễn giải đầu chứng từ**, khác `ChiTietChungTuBan.DienGiai` của
từng dòng (**BR15**). Template:
`[Prefix] + "bán dịch vụ" + [{TenKhachHang}] + [theo hóa đơn số {SoHoaDon}]`
- Prefix `"Thu tiền "` ở Tab Phiếu thu / Giấy báo có; **rỗng** ở Tab Chứng từ ghi nợ.
- `{TenKhachHang}` chỉ thêm khi đã chọn KH; `theo hóa đơn số {SoHoaDon}` chỉ khi đã nhập số HĐ.

| Điều kiện | Tab Ghi nợ | Tab Phiếu thu / Giấy báo có |
|---|---|---|
| Không KH, không số HĐ | `bán dịch vụ` | `Thu tiền bán dịch vụ` |
| Có KH, không số HĐ | `bán dịch vụ {TenKhachHang}` | `Thu tiền bán dịch vụ {TenKhachHang}` |
| Có KH và số HĐ | `bán dịch vụ {TenKhachHang} theo hóa đơn số {SoHoaDon}` | `Thu tiền bán dịch vụ {TenKhachHang} theo hóa đơn số {SoHoaDon}` |

Chỉ auto-fill khi user **chưa** tự sửa ô (`helpers/dongBo.ts:73 coTheGhiDeDienGiai`). Đây là **hằng số
nghiệp vụ tiếng Việt**, không phải chuỗi i18n — đặt cạnh `PREFIX_DIEN_GIAI` (`dongBo.ts:41`).

### 7.2 Auto-fill khi chọn Mã dịch vụ (BR02 → BR07 của CTBH)

Chọn dịch vụ ⇒ điền `Tên dịch vụ · Đơn giá · ĐVT · TK công nợ · TK doanh thu · Tài khoản CK · % thuế
GTGT` (từ cấu hình vật tư, TK ngầm định theo **BR16** nhóm *Bán dịch vụ*); rồi tính lại `Tiền thuế
GTGT` = Thành tiền × % thuế.
Combogrid **chỉ liệt kê vật tư `Loại = Dịch vụ`** — thêm tham số lọc ở `api/lookups.ts`.

### 7.3 Đồng bộ ngày (BR37 chung · BR02 của CTBH)

Ngày hạch toán = Ngày chứng từ **trước khi sửa**, user sửa Ngày hạch toán ⇒ Ngày chứng từ chạy theo.
Khác nhau ⇒ không đồng bộ. Sửa Ngày chứng từ ⇒ **không bao giờ** đổi Ngày hạch toán.
`helpers/dongBo.ts:118 dongBoNgayHachToan` — dùng lại.

### 7.4 Bút toán tự sinh (BR03 → **BR20** của CTBH)

| # | Bút toán | Nợ | Có | Số tiền | Điều kiện |
|---|---|---|---|---|---|
| 1 | Ghi nhận doanh thu & công nợ | `TK Công nợ` | `TK Doanh thu` | `Thành tiền` | dòng có Thành tiền > 0, không CKTM (gồm dòng KM kèm điều kiện) |
| 2 | Chiết khấu | `TK Chiết khấu` | `TK Công nợ` | `Tiền CK` | Tiền CK > 0 |
| 3 | Chiết khấu thương mại | `TK Doanh thu` | `TK Công nợ` | trị tuyệt đối `Thành tiền` (dòng mang dấu âm) | dòng CKTM = True |
| 4 | Thuế GTGT đầu ra | `TK Công nợ` | `TK Thuế GTGT` | `Tiền thuế GTGT` | > 0 |
| 5 | Thu tiền ngay | `TK Tiền` | `TK Công nợ` | Tổng phải thu (Giá bán − CK + VAT) | Thu tiền ngay = True |

**Không** có bút toán giá vốn (**BR19**), **không** có thuế XK (**BR14**). **Không gộp** bút toán
cùng tài khoản (BR36 chung · **BR20**). `helpers/hachToan.ts:49 sinhButToan` — thêm nhánh biến thể.
Kết quả nuôi popup §5.4.

### 7.5 Luồng lưu

1. Trim (BR43) → validate FE (V1–V12) → có lỗi ⇒ scroll + switch tab, **dừng**.
2. `toLuuChungTuBanBody(values)` (`api/payload.ts`) — gửi `loaiNghiepVu = 'Bán dịch vụ'`, **bỏ** mọi
   trường kho/giá vốn/quy đổi ĐVT/thuế XK.
3. `POST /api/ban-hang/chung-tu-ban-hang` với `ghiSo: false|true`.
4. Thành công ⇒ toast (BR26) → đóng popup → `invalidate: 'all'`.
5. Lỗi ⇒ `describeApiError` → toast đỏ / gắn lỗi vào ô → **giữ form**.
6. Loading: nút Lưu `loading`, khóa cả hai nút để không double-submit.

## 8. Phân bổ file

| Việc | File |
|---|---|
| Ẩn/hiện theo loại nghiệp vụ + theo I1/I2/(đk) | `helpers/anHien.ts` |
| Bộ cột lưới chi tiết (visible · disabled · displayOnly · nhãn) | `fields/chiTietFields.ts` |
| Nhãn cột/trường theo biến thể | `fields/texts.ts` |
| Option `% thuế GTGT`, Loại tiền, Loại chiết khấu, **Loại nghiệp vụ (3 giá trị)** | `fields/options.ts` · `constants/constants.ts` |
| Bảng Thuế | `fields/tabColumns.ts` (`thueColumns`) |
| **Cột popup Xem dữ liệu ghi sổ** | `fields/ghiSoColumns.ts` 🆕 |
| Số học dòng | `helpers/tinhToan.ts` |
| Chiết khấu 2 tầng + phân bổ | `helpers/chietKhau.ts` |
| Bút toán + tổng hợp thuế | `helpers/hachToan.ts` |
| Khối tổng | `helpers/tongHop.ts` + `components/TongHopPanel.tsx` |
| Đồng bộ liên trường + template diễn giải BR01 | `helpers/dongBo.ts` |
| Validate trước lưu | `helpers/kiemTra.ts` |
| State liên tab | `hooks/useDongBoTab.ts` |
| Danh mục / lookup (lọc `Loại = Dịch vụ`) | `api/lookups.ts` + `hooks/useDanhMucThemMoi.ts` |
| Zod + gọi API | `api/model.ts` · `api/payload.ts` · `api/formDetail.ts` · `api/ghiSo.ts` 🆕 |
| Ráp UI | `components/ChungTuBanHangThemMoiModal.tsx` · `components/XemDuLieuGhiSoModal.tsx` 🆕 |
| Kiểu | `fields/types.ts` |
| Chữ | `i18n/vi.ts` · `i18n/en.ts` |

## 9. Kiểm thử

| # | Input | Kỳ vọng |
|---|---|---|
| T1 | `loaiNghiepVu='Bán dịch vụ'` | Header Options **ẩn** Loại nghiệp vụ và Kiêm phiếu xuất kho; **giá trị vẫn có trong form store** |
| T2 | như T1 | **không** có tab Phiếu xuất kho, **không** có khối Thông tin bổ sung, **không** có tab Hạch toán |
| T3 | `loaiNghiepVu='Bán hàng trong nước'` | vẫn có đủ (chống hồi quy E-06194) |
| T4 | như T1 | lưới **không** có cột Kho/Giá vốn/Tiền vốn/Lô/HSD/Hệ số quy đổi/SL quy đổi/ĐG quy đổi/Thuế XK |
| T5 | tick Thu tiền ngay + Tiền mặt | hiện tab Phiếu thu, ẩn khối Điều khoản TT |
| T6 | tick Thu tiền ngay + Chuyển khoản | hiện tab Giấy báo có; "Tên ngân hàng nhận" read-only |
| T7 | tick Lập kèm hóa đơn | hiện tab Hóa đơn; "Tài khoản NH" chỉ khi Hình thức TT = Chuyển khoản |
| T8 | Loại tiền ≠ VND | hiện Tỷ giá + `Thành tiền quy đổi`/`Tiền CK quy đổi`/`Tiền thuế GTGT quy đổi` + khối tổng 2 cột |
| T9 | dòng `% thuế = KHAC` | hiện `Giá trị thuế GTGT`; `HH không TH tờ khai GTGT` **ép tick + disable** |
| T10 | dòng `% thuế = 10` | `HH không TH…` tự bỏ tick, **cho** user tự tích |
| T11 | dòng ghi chú | mọi ô khóa trừ `Tên dịch vụ`; **không** có ô Kho; không auto-fill theo Mã dịch vụ |
| T12 | Diễn giải, KH "Cty A", số HĐ "HĐ13332", tab Ghi nợ | `"bán dịch vụ Cty A theo hóa đơn số HĐ13332"` |
| T13 | như T12 nhưng tab Phiếu thu | `"Thu tiền bán dịch vụ Cty A theo hóa đơn số HĐ13332"` |
| T14 | Ngày HT = Ngày CT, sửa Ngày HT | Ngày CT chạy theo (BR02 của CTBH) |
| T15 | Ngày HT ≠ Ngày CT, sửa Ngày HT | Ngày CT **không** đổi |
| T16 | lưới rỗng, bấm Lưu | chặn, MSG_..._007 |
| T17 | Tiền CK dòng > Thành tiền dòng | chặn, MSG_..._044 |
| T18 | 1 dòng Thành tiền 1.000.000, thuế 10%, thu tiền ngay | `sinhButToan` sinh đúng **3 cặp** bút toán (doanh thu · thuế · thu tiền), **không** có bút toán giá vốn; Σ Nợ = Σ Có |
| T19 | `toLuuChungTuBanBody` | payload có `loaiNghiepVu='Bán dịch vụ'`; **không** chứa `khoId`/`donGiaVon`/`heSoQuyDoi`/`tienThueXk` |
| T20 | user có `.Create` nhưng không `.Post` | **không** hiện nút "Lưu và ghi sổ" |
| T21 | Thêm dòng khi đang focus dòng 1 (bảng 5 dòng) | dòng mới là dòng 2, STT đánh lại 1..6 (BR21.2) |
| T22 🆕 | bấm "Xem dữ liệu ghi sổ" | popup mở, bảng bút toán khớp §7.4, dòng Tổng Nợ = Tổng Có |
| T23 🆕 | `LOAI_NGHIEP_VU` | có đủ **3** giá trị; combo ở popup bán hàng hóa **ẩn** `Bán dịch vụ` (BR24) |

## 10. BR đã áp dụng

**BR chung:** BR3 · BR5 · BR6 · BR7 · BR9 · BR10 · BR12 · BR13.2 · BR14 · BR15 · BR16 · BR18 · BR19 ·
BR20 · BR21 · BR24 · BR25 · BR26 · BR36 · BR37 · BR41 · BR43 · BR46.

**BR của `SCR_CTBH_ThemMoi.md` (số hiệu v2):** BR01 (auto-fill KH) · BR02 (ngày) · BR03 (hạn TT) ·
BR04 (thu tiền ngay) · BR05 (lập kèm/đã lập hóa đơn) · BR07 (auto-fill vật tư) · BR09 (KM/CKTM) ·
BR11 (SL·ĐG·TT) · BR12 (chiết khấu) · BR13 (thuế GTGT, mục 6 tab Thuế + mục 7 checkbox) · BR14
(thuế XK — **không áp dụng**) · BR15 (diễn giải) · BR16 (TK ngầm định) · BR17 (ẩn cột kho) · BR18
(kiêm phiếu thu) · BR19 (không giá vốn) · BR20 (bút toán) · BR21 (ghi sổ) · BR23 (theo dõi SL xuất) ·
**BR24 (phạm vi LoaiNghiepVu)**.

**Chưa đạt:**
- **BR13.2 chung** — thiếu nút "In" và "Lưu và Thêm mới"; BA chỉ khai 3 nút ⇒ [00 §12 Q6](00-ke-hoach-tong.md).
- **BR17 chung (kỳ kế toán)** — BE kiểm, FE hiển thị lỗi.
- **BR41 chung** — Tab Tham chiếu treo ⇒ [00 §12 Q5](00-ke-hoach-tong.md).
- **Tab "Đính kèm"** — Figma có, BA không ⇒ [00 §12 Q9](00-ke-hoach-tong.md), không code.
