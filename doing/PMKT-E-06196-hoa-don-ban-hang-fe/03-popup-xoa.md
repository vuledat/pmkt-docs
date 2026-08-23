# 03 — Popup Xác nhận xóa Hóa đơn bán hàng

## 1. Header

- **Mã màn:** `SCR_HDBanHang_Xoa`
- **`SCR_*` nguồn:** `5.screens/SCR_HDBanHang_Xoa.md`
- **UC nguồn:** `4.usecases/PMKT-U-06459_Xoa/UC_HDBanHang_Xoa.md`
- **Node Figma:** *(đang bổ sung, PYC chưa có link)*
- **Đường dẫn:** không có route riêng — mở từ `SCR_HDBanHang_DanhSach`
- **Trạng thái code:** ĐÃ CÓ. `_scope.md` xếp SKIP (popup xác nhận + list kết quả, không phải form
  ẩn/hiện theo trục input).

## 2. Bố cục

Hai popup con:

1. **Popup xác nhận xóa** (xóa 1 dòng hoặc xóa hàng loạt) — `CommonConfirmModal`, tone `danger`.
2. **Popup Kết quả xóa hàng loạt** — luôn hiện sau khi hoàn tất xóa hàng loạt (BR8) — `@base`
   `BulkDeleteResultModal`, đã thêm prop `tenDoiTuong` (cột "Tên khách hàng") vào component `@base`
   thay vì copy ra feature.

## 3. Đặc tả UI từ Figma

*(Chưa có Figma — đặc tả UI suy từ `SCR_HDBanHang_Xoa.md`, cần review lại khi có design — đúng luật
`SKILL.md §0.2`.)*

| Thành phần | Component `@base` | Ghi chú |
| :-- | :-- | :-- |
| Popup xác nhận (center, overlay mờ, nút Xác nhận đỏ) | `CommonConfirmModal` (`:269`) | BR3, BR4, BR5 của `SCR_HDBanHang_Xoa` |
| Popup kết quả (bảng "Danh sách không xóa được") | `BulkDeleteResultModal` (`:293`) + cột `tenDoiTuong` mới thêm | STT · Ngày HĐ · Số HĐ (link) · Tên KH · Lý do lỗi |

## 4. Ma trận ẩn/hiện · required · disabled

Không áp dụng — popup xác nhận không có trường nhập liệu theo trục input, chỉ có điều kiện hiện nút
(dịch từ `SCR_HDBanHang_Xoa.md §Rule`):

| Thành phần | Điều kiện |
| :-- | :-- |
| Nút "Xóa" (icon trên dòng) | chỉ hiện khi hóa đơn "Chưa phát hành" (BR2) |
| Nút "Xóa hàng loạt" | ≥1 dòng tick — xem mâu thuẫn nội bộ đã ghi ở `01-danh-sach-hoa-don.md §4` |
| Nội dung popup xác nhận (đơn lẻ) | MSG_027 mặc định; đổi sang MSG_055 nếu HĐ đang xóa có trạng thái lập chứng từ ∈ {"Đã lập 1 phần","Đã lập đủ"} (**BR10**) |
| Nội dung popup xác nhận (hàng loạt) | luôn dùng "cảnh báo chung của hệ thống" — BR10 nói rõ đổi câu **chỉ áp dụng khi xóa từng cái** |
| Popup Kết quả | luôn hiện sau xóa hàng loạt (BR8), không điều kiện |

## 5. Bảng cột / trường

Bảng "Danh sách không xóa được" (popup Kết quả):

| Tên hiển thị | Khoá i18n | Field API | Kiểu | Ghi chú |
| :-- | :-- | :-- | :-- | :-- |
| STT | `hoaDonBanHang:xoa.ketQua.col.stt` | `-` | số thứ tự hiển thị | không lưu |
| Ngày hóa đơn | `hoaDonBanHang:xoa.ketQua.col.ngayHoaDon` | `ngayHoaDon` | date | |
| Số hóa đơn | `hoaDonBanHang:xoa.ketQua.col.soHoaDon` | `soHoaDon` | string, hyperlink | |
| Tên khách hàng | `hoaDonBanHang:xoa.ketQua.col.tenKhachHang` | `tenKhachHang` | string | prop mới thêm ở `@base` |
| Lý do lỗi | `hoaDonBanHang:xoa.ketQua.col.lyDo` | `lyDo` | string | server sinh |

## 6. Hành vi & sự kiện

| Nút | Điều kiện hiện | Việc làm | Confirm | Toast | Invalidate |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Icon Xóa (1 dòng) | trạng thái Chưa phát hành + quyền `Delete` | mở popup xác nhận | MSG_027/MSG_055 | thành công MSG_003; lỗi MSG_033/MSG_010 | query list |
| Nút "Xóa hàng loạt" | ≥1 dòng tick | mở popup xác nhận hàng loạt | cảnh báo chung | — | — |
| Xác nhận (Yes) | — | gọi `DELETE /{id}` hoặc `POST /xoa-hang-loat` (⚠ BE 400 — nợ N1) | — | MSG_003 hoặc MSG_054 | query list |
| Đóng popup Kết quả | — | đóng + **luôn reload danh sách** (BR9) | — | — | query list |

## 7. Validation phía FE

Không có validate nhập liệu — popup chỉ xác nhận hành động. Điều kiện chặn duy nhất: nút Xóa ẩn khi
hóa đơn không ở trạng thái "Chưa phát hành" (BE vẫn tự kiểm lại — BR2 là ràng buộc 2 lớp).

## 8. Luồng xử lý

1. Xóa 1 dòng: bấm icon → build nội dung cảnh báo theo `trangThaiLapChungTu` của dòng (BR10) → Yes →
   `DELETE /{id}` (kèm `updatedAt` optimistic lock) → toast → invalidate.
2. Xóa hàng loạt: tick N dòng → bấm "Xóa hàng loạt" → cảnh báo chung → Yes →
   `xoaHoaDonHangLoat(rows)` (`api/hoaDonBanHangApi.ts:140-147`) → server bỏ qua hóa đơn "Đã phát
   hành" (BR7), xóa phần còn lại → luôn mở popup Kết quả (BR8) liệt kê phần thất bại → Đóng → reload
   (BR9).

## 9. Phân bổ file

| Việc | File |
| :-- | :-- |
| State 3 luồng xóa (đơn/hàng loạt/kết quả) | `components/HoaDonBanHangTab.tsx` |
| Gọi API xóa hàng loạt | `api/hoaDonBanHangApi.ts` (`xoaHoaDonHangLoat`) |
| Schema kết quả xóa hàng loạt | `api/model.ts:207-224` (`ketQuaXoaHangLoatSchema`) |
| Prop mới ở `@base` | `base/components/modal/BulkDeleteResultModal.tsx` (thêm `tenDoiTuong` optional, backward-compatible) |

## 10. Kiểm thử

| Case | Loại | File |
| :-- | :-- | :-- |
| Đổi nội dung cảnh báo theo `trangThaiLapChungTu` (BR10) | logic thuần (`node`) | `test/kiemTra.test.ts`* |
| `ketQuaXoaHangLoatSchema.parse` — hình dạng response | logic thuần (`node`) | `test/payload.test.ts`* |
| Render popup xác nhận + popup kết quả | DOM | `test/hoaDonBanHang.render.test.tsx` |

\* Case xóa hiện gộp trong 2 file test chung của module — tách riêng `xoa.test.ts` không bắt buộc
trong phạm vi PYC này (module đã xanh 118/118 với cách tổ chức hiện tại).

## 11. BR đã áp dụng

BR16 (cảnh báo nghiệp vụ) · BR45 §2/§3 (thao tác hàng loạt — **lệch có chủ ý** so với chuẩn chung ở
tiêu đề popup + bộ cột, theo epic, đã báo BA — xem `00-ke-hoach-tong.md §11 mục #8` bản 12/08) của
Common; BR1-BR10 riêng của `SCR_HDBanHang_Xoa`.
