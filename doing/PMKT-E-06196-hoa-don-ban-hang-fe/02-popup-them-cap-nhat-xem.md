# 02 — Popup Thêm mới / Cập nhật / Xem chi tiết Hóa đơn bán hàng

> Một component `components/HoaDonBanHangThemMoiModal.tsx` phục vụ **3 SCR** vì cả 3 file Matrix tự
> khai ma trận trường **y hệt nhau**, chỉ khác `mode` (`create`/`edit`/`view`) và bộ nút footer. Gộp 1
> file kế hoạch là theo đúng cấu trúc code thật (§7 của `00-ke-hoach-tong.md`).

## 1. Header

- **Mã màn:** `SCR_HDBanHang_ThemMoi` (anchor) · `SCR_HDBanHang_CapNhat` · `SCR_HDBanHang_ChiTiet`
- **`SCR_*` nguồn:** `5.screens/SCR_HDBanHang_ThemMoi.md`, `SCR_HDBanHang_CapNhat.md`,
  `SCR_HDBanHang_ChiTiet.md` — cả ba tham chiếu trực tiếp cấu trúc trường của
  `PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_ThemMoi.md#tab-hóa-đơn` (+ Thông tin bổ sung, Lựa
  chọn Loại tiền/Chiết khấu, Tab Chi tiết hàng hóa, Dòng tổng tiền)
- **UC nguồn:** `4.usecases/ThemMoi/UC_HDBanHang_ThemMoi.md`,
  `PMKT-U-06458_CapNhat/UC_HDBanHang_CapNhat.md`, `PMKT-U-06466_ChiTiet/UC_HDBanHang_ChiTiet.md`
- **Node Figma:** `14770-349117` (bộ popup) · `14770:349569` (Dialog Box) — `SCR_HDBanHang_ChiTiet`
  chưa có node riêng trong PYC
- **Route:** không có route riêng — popup mở từ `SCR_HDBanHang_DanhSach` (`/ban-hang/hoa-don-ban-hang`)

## 2. Bố cục

```
CommonModalShell
├── HeaderControls           "Chọn chứng từ" (nguồn) — chỉ ở mode create/edit
├── ThongTinHoaDon.tsx        Section "Thông tin hóa đơn" (16 trường)
├── ThongTinXuatKhau.tsx      Section "Thông tin xuất khẩu" — Show(đk: xuất khẩu)
├── GridHeaderActions.tsx     Loại tiền · Tỷ giá · Loại chiết khấu · Ô % · nút Áp dụng/Phân bổ
├── CommonEditableGrid        Bảng chi tiết hàng hóa (chiTietFields.ts — lưới lớn nhất module)
├── TongHopPanel.tsx          Khối "Tổng hợp tiền tệ"
└── footer: Hủy · Lưu (create/edit) · Cập nhật · Đóng (view)

PhanBoChietKhauModal.tsx      popup con — mở từ nút "Phân bổ chiết khấu" trong GridHeaderActions
```

## 3. Đặc tả UI từ Figma

| Thành phần | Component `@base` | Ghi chú |
| :-- | :-- | :-- |
| Khung popup + guard "bỏ thay đổi" + footer 2 chế độ | `CommonModalShell` (`:258`) | mode create/edit dùng footer "Hủy·Lưu"; mode view dùng "Cập nhật·Đóng" (BR34) |
| Cụm "Chọn chứng từ" | `HeaderControls` (`:277`) | node 14770:349569 |
| Lưới nhập liệu | `CommonEditableGrid` (`:535`) | cascade, dòng ghi chú, phân trang, dòng Σ |
| Khối tổng | `TotalBreakdown` (`:205`) | không đuôi "(Tiền hạch toán)" — hóa đơn không hạch toán |
| Ô nhập | `CommonTextBox`/`CommonNumberInput`/`CommonSelectBox`/`CommonDatePicker`/`FieldLabel` (`:172,160,572,166,188`) | |
| `ThongTinHoaDon.tsx`, `ThongTinXuatKhau.tsx` | **viết mới** | bố cục trường riêng màn (node 14770:349584); không component `@base` nào vẽ 1 section form nghiệp vụ |
| `PhanBoChietKhauModal.tsx` | **viết mới** | 2 biến thể trong 1 component — theo `SCR_CTBH_PBCK.md` (theo tổng) và `SCR_CTBH_PBCK_MHHD.md` (theo mặt hàng+hóa đơn) |

## 4. Ma trận ẩn/hiện · required · disabled

Dịch nguyên vẹn từ `Matrix/SCR_HDBanHang_ThemMoi_MaTranAnHien.md` (biến thể A) +
`_CapNhat_MaTranAnHien.md` (giống hệt, chỉ khác bộ nút) + `_ChiTiet_MaTranAnHien.md` (biến thể B —
mọi trường `Disable`, trục cột đổi sang Trạng thái phát hành). Trục cột **I = Loại nghiệp vụ**
(2 giá trị: C1 Trong nước · C2 Xuất khẩu) cho ThemMoi/CapNhat.

| Tab/Section | Trường/Thành phần | C1 (Trong nước) | C2 (Xuất khẩu) | Xem (mọi C) |
| :-- | :-- | :--: | :--: | :--: |
| Thông tin hóa đơn | Loại nghiệp vụ | Show | Show | Disable |
| Thông tin hóa đơn | Mã KH · Tên KH · MST/CCCD · Người mua · Mã DVQHNS · CCCD · Hộ chiếu · SĐT · Địa chỉ · HT TT · Mẫu số · Ký hiệu · Ngày HĐ · Số HĐ | Show | Show | Disable |
| Thông tin hóa đơn | Tài khoản NH `(đk-TT: HTTT=Chuyển khoản)` | Show(đk-TT) | Show(đk-TT) | Disable(đk-cfg) |
| Thông tin xuất khẩu | 7 trường (Số hợp đồng…Đơn vị vận chuyển) | Hide | Show | Disable(đk-cfg) |
| Loại tiền/Chiết khấu | Loại tiền · Loại chiết khấu | Show | Show | Disable |
| Loại tiền/Chiết khấu | Tỷ giá quy đổi `(đk-LT)` | Show(đk-LT) | Show(đk-LT) | Disable(đk-cfg) |
| Loại tiền/Chiết khấu | Ô % · nút Áp dụng · nút Phân bổ `(đk-CK)` | Show(đk-CK) | Show(đk-CK) | Disable(đk-cfg) |
| Bảng chi tiết | STT | Disable | Disable | Disable |
| Bảng chi tiết | Loại dòng hàng · Diễn giải (ẩn) `(at)` | Hide | Hide | Hide |
| Bảng chi tiết | Mã hàng · Tên hàng · CK thương mại · Hàng KM · ĐVT · SL · Đơn giá · Thành tiền · Diễn giải thuế · HH không TH GTGT | Show | Show | Disable |
| Bảng chi tiết | Hệ số/SL/Đơn giá quy đổi (tính toán) | Disable | Disable | Disable |
| Bảng chi tiết | % thuế GTGT · Giá trị thuế GTGT · Tiền thuế GTGT | Show | Hide | Disable(đk-cfg: trong nước) |
| Bảng chi tiết | Giá trị tính thuế XK · % Thuế XK · Tiền thuế XK | Hide | Show | Disable(đk-cfg: xuất khẩu) |
| Bảng chi tiết | Thành tiền quy đổi · Tiền CK quy đổi `(đk-LT)` | Show(đk-LT) | Show(đk-LT) | Disable(đk-cfg) |
| Bảng chi tiết | Tiền thuế GTGT quy đổi `(đk-LT, auto)` | Disable(đk-LT) | Hide | Disable(đk-cfg) |
| Bảng chi tiết | Tỷ lệ/Tiền CK `(đk-CK)` | Show(đk-CK) | Show(đk-CK) | Disable(đk-cfg) |
| Bảng chi tiết | Cột CK auto-calc theo mặt hàng/hóa đơn + quy đổi `(đk-CK)` | Disable(đk-CK) | Disable(đk-CK) | Disable(đk-cfg) |
| Nút lưới | Thêm dòng · Xóa dòng · Thêm ghi chú | Show | Show | **Hide** |
| Tổng hợp | Tổng tiền hàng · Tổng CK · Tổng thanh toán (Σ) | Disable | Disable | Disable |
| Tổng hợp | Tổng thuế GTGT | Disable | Hide | Disable(đk-cfg) |
| Tổng hợp | Tổng thuế XK | Hide | Disable | Disable(đk-cfg) |
| Tổng hợp | Tổng theo loại tiền `(đk-LT)` | Disable(đk-LT) | Disable(đk-LT) | Disable(đk-cfg) |
| Nút hoạt động | Lưu · Hủy | Show | Show | *(xem §6 — Cập nhật/Đóng)* |

**Ghi chú áp dụng nguyên trạng từ Matrix gốc** (không diễn giải lại):

- **Cột hạch toán bị loại khỏi lưới hóa đơn** (không xuất hiện trong ma trận trên): Kho, Giá vốn, Tiền
  vốn, TK công nợ, TK doanh thu, TK giá vốn, TK kho, TK chiết khấu, TK Thuế GTGT. Lưới **vẫn có** "%
  thuế GTGT"/"Tiền thuế GTGT" để thể hiện số tiền thuế, chỉ không có TK.
  Điểm cần xác nhận (**Q5** — `00-ke-hoach-tong.md §12`): "TK Thuế XK" có bị loại theo cùng nguyên tắc
  không — chưa có căn cứ tường minh.
- **(đk-LT)**: hiện khi Loại tiền ≠ đồng tiền hạch toán.
- **(đk-CK)**: theo Loại chiết khấu — Ô % + nút Áp dụng khi "Theo % hóa đơn"; nút Phân bổ khi "Theo
  số tiền trên tổng hóa đơn" HOẶC "Theo mặt hàng và hóa đơn".
- **Dòng ghi chú** (`Loại dòng hàng = False`): disable toàn bộ cột, chỉ nhập Tên hàng, không auto-fill,
  không bắt buộc.
- Ma trận `_ChiTiet` (Xem): mọi trường `Disable`, nút lưới `Hide` (khác `Disable` — tài liệu ghi rõ
  "không có nút", không phải "hiện xám"). Nút "Cập nhật" chỉ hiện khi Trạng thái phát hành = "Chưa
  phát hành"; "Đóng" luôn hiện.

## 5. Bảng cột / trường

Header (`HoaDonBanHangFormValues`, `fields/types.ts:109-151`) — field API là tên wire, khớp thẳng
`HoaDonBanHangDto.java` (đã đối chiếu, `00-ke-hoach-tong.md §2.1`):

| Trường | Field API | Kiểu form | Bắt buộc | Ghi chú |
| :-- | :-- | :-- | :-- | :-- |
| Loại nghiệp vụ | `loaiNghiepVu` | string (enum) | Y | mặc định "Bán hàng trong nước"; kế thừa + khoá sửa khi lập kèm từ chứng từ nguồn |
| Mã/Tên KH, MST, Người mua, Mã DVQHNS, CCCD, Hộ chiếu, SĐT, Địa chỉ | `khachHangId…diaChi` | string | Y (Mã KH, Tên KH, Địa chỉ) | auto-fill theo BR01 CTBH |
| Nhân viên bán hàng | `nhanVienBanHangId` | string | N | auto-fill |
| Hình thức TT | `hinhThucThanhToan` | string (enum 3 giá trị) | Y | |
| Tài khoản NH | `taiKhoanNganHangThuId` | string | N, hiện theo `(đk-TT)` | |
| Mẫu số/Ký hiệu/Ngày/Số hóa đơn | `mauSoHoaDonId…soHoaDon` | string/Dayjs | Y | BR06, khoá trùng BR03 |
| 7 trường Thông tin xuất khẩu | `soHopDong…donViVanChuyen` | string/Dayjs | N | chỉ hiện khi xuất khẩu |
| Loại tiền, Tỷ giá | `loaiTienId`, `tyGia` | string/number | Y | mặc định đồng tiền hạch toán, tỷ giá = 1 |
| Loại chiết khấu, % chiết khấu | `loaiChietKhau`, `giaTriChietKhau` | string/number | Y/N | 5 loại (CTBH BR12) |

Chi tiết dòng (`HoaDonBanHangLine`, `fields/types.ts:30-106`) — **34 trường trên wire** + **6 trường
chỉ sống trong form store** (không gửi lên: `heSoQuyDoi`, `soLuongQuyDoi`, `loaiVatTu`,
`dienGiaiThueTuSua`, `soLuongConLaiChoPhep`, `chiPhi` — lý do từng trường ghi tại chỗ khai báo). Bảng
đầy đủ không lặp lại ở đây — xem `fields/chiTietFields.ts` (625 dòng, "bản CODE của ma trận ẩn/hiện")
và bảng Field của `SCR_CTBH_ThemMoi.md#tab-chi-tiết-hàng-hóa` (dòng 190-247, phần không thuộc nhóm
hạch toán).

## 6. Hành vi & sự kiện

| Nút | Điều kiện hiện | Điều kiện disable | Việc làm | Confirm | Toast | Invalidate |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Hủy | create/edit | — | đóng popup, hỏi nếu có thay đổi chưa lưu (`CommonModalShell` guard) | Yes/No nếu dirty | — | — |
| Lưu | create/edit | validate fail | `POST /` hoặc `PUT /{id}` (⚠ BE 400 — nợ N1, xem §2 file gốc) | — | MSG_001 (thêm) / MSG_002 (sửa) | query list |
| Cập nhật (từ Xem) | view, trạng thái Chưa phát hành | — | mở lại popup mode `edit` (BR34) | — | — | — |
| Đóng | mọi mode xem | — | đóng popup, không lưu | — | — | — |
| Mở form Sửa khi HĐ đã lập chứng từ | mode edit | — | popup cảnh báo Yes/No trước khi mở form thật (BR02 của `SCR_HDBanHang_CapNhat`) | MSG_056 | — | — |
| Thêm dòng / Xóa dòng / Thêm ghi chú | create/edit | — | thao tác `CommonEditableGrid` (BR08) | — | — | — |
| Nút "Áp dụng" (chiết khấu %) | `(đk-CK)` = "Theo % hóa đơn" | — | phân bổ % đều theo Thành tiền dòng | — | — | — |
| Nút "Phân bổ chiết khấu" | `(đk-CK)` = 2 loại còn lại | — | mở `PhanBoChietKhauModal` | — | — | ghi lại vào `chiTiet[].tienChietKhauHoaDon…` |

## 7. Validation phía FE

| Điều kiện | Thông báo (nguyên văn `6.messages.md`) | Nguồn BR | FE hay BE kiểm |
| :-- | :-- | :-- | :-- |
| Trùng hóa đơn (Số HĐ + Ký hiệu + Mẫu số) | MSG_PMKT-E-06196_006: "Hóa đơn đã tồn tại ({{soHD}}-{{kyHieuHD}}-{{mauSoHD}})" | BR03 | **BE** — FE chỉ hiển thị lỗi trả về (không có endpoint kiểm trùng riêng) |
| Không có dòng chi tiết hàng hóa | MSG_007: "Phải có ít nhất 1 dòng chi tiết hàng hóa" | Validate lưới | FE (`helpers/kiemTra.ts`) |
| Số lượng âm | MSG_009: "Số lượng không được âm" | | FE |
| % Chiết khấu > 100% | MSG_015 | BR02 popup | FE |
| Tiền CK > Thành tiền dòng | MSG_016 | BR02 popup | FE |
| Tổng CK dòng ≠ tổng CK hóa đơn (phân bổ thủ công) | MSG_017 | BR02 popup | FE |
| Tổng tỷ lệ phân bổ ≠ 100% | MSG_018 | BR02 popup | FE |
| SL xuất HĐ vượt quá còn lại (lập từ CTBH) | MSG_019 | BR05 ThemMoi / BR23 CTBH | FE — nhưng **nguồn `soLuongConLaiChoPhep` chưa có** (nợ N7, phụ thuộc N6) |
| Đơn giá âm | MSG_020 | | FE |

## 8. Luồng xử lý

1. Mở popup (create) → form trắng, `loaiNghiepVu` mặc định "Bán hàng trong nước", `tyGia = 1`.
2. Mở popup (edit) → `GET /{id}` (đã thật) → `formDetail.toFormValues(...)` map wire→form; nếu
   `trangThaiLapChungTu` ∈ {"Đã lập 1 phần","Đã lập đủ"} → hiện MSG_056 trước khi render form.
3. Mở popup (view) → như edit nhưng mọi input `readOnly`, không tải để sửa.
4. Đổi `loaiNghiepVu` → `helpers/anHien.ts` tính lại `NguCanhAnHien` → toàn bộ section/cột đọc lại
   theo object đó (không tự suy diễn rời rạc — xem chú thích `fields/types.ts:154-159`).
5. Đổi dòng lưới (mã hàng, số lượng, đơn giá, % thuế…) → `helpers/tinhToan.ts` tính lại Thành tiền,
   quy đổi, thuế; `helpers/tongHop.ts` cộng dòng tổng.
6. Bấm Lưu → `helpers/kiemTra.ts` chạy toàn bộ validate §7 → nếu pass, `api/payload.ts` cắt/trim →
   gọi API → thành công: toast + đóng popup + invalidate; thất bại: hiện lỗi tại field hoặc toast.

## 9. Phân bổ file

| Việc | File |
| :-- | :-- |
| Component chính, 3 mode | `components/HoaDonBanHangThemMoiModal.tsx` (676 dòng) |
| Section Thông tin hóa đơn / Xuất khẩu | `components/ThongTinHoaDon.tsx`, `ThongTinXuatKhau.tsx` |
| Cụm Loại tiền/Chiết khấu | `components/GridHeaderActions.tsx` |
| Khối tổng | `components/TongHopPanel.tsx` |
| Popup phân bổ | `components/PhanBoChietKhauModal.tsx` (⚠ nợ N11 — nên chuyển vào `components/modal/`) |
| Mô tả cột lưới | `fields/chiTietFields.ts`, `fields/phanBoFields.ts` |
| Ngữ cảnh ẩn/hiện | `helpers/anHien.ts` |
| Tính toán | `helpers/tinhToan.ts`, `helpers/tongHop.ts`, `helpers/chietKhau.ts` |
| Validate | `helpers/kiemTra.ts` |
| Auto-fill KH/mã hàng | `helpers/dongBo.ts` |
| Danh mục dùng chung | `hooks/useDanhMucHoaDon.ts`, `api/lookups.ts` |
| Wire ↔ form | `api/payload.ts` (form→wire), `api/formDetail.ts` (wire→form) |

## 10. Kiểm thử

| Case | Loại | File |
| :-- | :-- | :-- |
| `helpers/tinhToan` — BR09/BR10/BR16/BR18 + thuế XK | logic thuần (`node`) | `test/tinhToan.test.ts` |
| `helpers/anHien` — 3 ma trận | logic thuần (`node`) | `test/anHien.test.ts` |
| `helpers/kiemTra` — 9 case validate §7 | logic thuần (`node`) | `test/kiemTra.test.ts` |
| `api/payload` — form→wire, trim, cắt trường theo mode | logic thuần (`node`) | `test/payload.test.ts` |
| Render popup, đổi mode, submit | DOM | `test/hoaDonBanHang.render.test.tsx` |

## 11. BR đã áp dụng

BR13.2 (nút form) · BR14 (chế độ form) · BR15 (validation) · BR16 (cảnh báo — MSG_055/056) · BR18
(ngoại tệ) · BR24 (tooltip) · BR34 (sửa từ Xem) · BR43 (trim) · BR46 (`updatedAt` optimistic lock) của
Common; BR01-BR05 riêng của `SCR_HDBanHang_ThemMoi`, BR01-BR02 riêng của `SCR_HDBanHang_CapNhat`.
Toàn bộ logic tính toán/chiết khấu/thuế **tham chiếu trực tiếp** BR01, BR06-BR15, BR23, BR24 của
`SCR_CTBH_ThemMoi.md` (đã đối chiếu số hiệu khớp HEAD 20/08 — `00-ke-hoach-tong.md §2.3`).
