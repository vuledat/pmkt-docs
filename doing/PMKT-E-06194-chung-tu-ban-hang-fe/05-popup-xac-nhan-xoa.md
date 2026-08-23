# 05 — Popup Xác nhận xóa Chứng từ bán hàng

## 1. Header

- **Mã màn**: SCR_CTBH_PopupXacNhanXoa
- **SCR nguồn**: `5.screens/SCR_CTBH_PopupXacNhanXoa.md` (83 dòng)
- **UC nguồn**: UC_CTBH_Xoa
- **Route**: mở từ nút "Xóa" / "Xóa hàng loạt" trên `SCR_CTBH_DanhSach`
- **File chính**: **không có component riêng** — dùng cơ chế confirm chuẩn của kernel `@domain-kit/chungTu` (D6, `00-ke-hoach-tong.md`)

## 2. Bố cục

Popup chuẩn theo BR3 chung (business_rules `#br3-popup`): tiêu đề "Xác nhận xóa", icon cảnh báo, nội dung, nút Đồng ý/Hủy — do kernel dựng, không có bố cục riêng của module.

## 3. Đặc tả UI từ Figma

Không có Figma (SCR ghi `[]` ở mục Nguyên mẫu) — dùng khung chuẩn của kernel.

## 4. Ma trận ẩn/hiện · required · disabled

Không có file Matrix riêng. Áp BR03/BR04/BR06 của chính SCR:

| Quy tắc | Trạng thái code |
|---|---|
| Nút "Xóa" trên dòng: hiện khi `Chưa ghi sổ` AND quyền xóa (BR03) | ✅ qua kernel (`trangThai.chuaGhiSo`) |
| Chứng từ đã dùng nghiệp vụ khác vẫn hiện nút Xóa, click báo lỗi MSG_111 (BR03/BR04) | ✅ qua D3 — BE trả lỗi, `apiError.ts` hiển thị nguyên văn |
| Nút "Xóa hàng loạt" KHÔNG disable theo trạng thái dòng đã chọn (BR02) | ✅ qua kernel `bulk.XOA` |
| Thứ tự kiểm: BR01 (đã ghi sổ) → BR04 (đã dùng nơi khác) (BR06) | ✅ — thứ tự do BE quyết định, FE không tự sắp xếp lại thông báo |

## 5. Bảng cột / trường

Không áp dụng — popup xác nhận không có trường nhập liệu.

## 6. Hành vi & sự kiện

Không đổi từ bản 18/08 — không có thay đổi trong 2 commit BA mới cho file này.

## 7. Validation phía FE

Không có — mọi điều kiện chặn xóa (BR01, BR04) là BE-side, FE chỉ hiển thị message (`MSG_PMKT-E-06194_013`, `_111`, `_015`) qua kênh lỗi chung (D3).

## 8. Luồng xử lý

1. User bấm Xóa (đơn/hàng loạt).
2. Kernel hiện popup xác nhận chuẩn.
3. User xác nhận → gọi `DELETE {base}/{id}` hoặc `{base}/xoa-hang-loat`.
4. Thành công: toast MSG_003, invalidate danh sách. Lỗi: toast/hiển thị message BE trả về nguyên văn.

## 9. Phân bổ file

Không có file mới — nếu kernel hiện tại chưa đủ (ví dụ chưa hỗ trợ hiển thị danh sách chứng từ không xóa được ở xóa hàng loạt theo BR45), việc đó thuộc phạm vi `@domain-kit/chungTu`, không phải module này — báo lại nếu phát hiện thiếu, không tự vá bằng code feature-level.

## 10. Kiểm thử

| Case | Input → kỳ vọng | Loại |
|---|---|---|
| Xóa chứng từ đã dùng nơi khác | BE trả lỗi kèm `MSG_PMKT-E-06194_111` → toast hiển thị đúng message BE (không hiển thị fallback key) | test tích hợp nhẹ hoặc xác nhận bằng đọc code `apiError.ts`, không cần viết test mới nếu đã có test chung cho `apiError.ts` |
| Xóa hàng loạt không disable theo trạng thái | chọn 1 dòng "Đã ghi sổ" + 1 dòng "Chưa ghi sổ" → nút Xóa hàng loạt vẫn enable | test đã có ở tầng kernel (`base/domainKit/chungTu/test/`), không lặp lại ở module |

## 11. BR đã áp dụng

`BR01, BR02, BR03, BR04, BR05, BR06` của SCR_CTBH_PopupXacNhanXoa — toàn bộ đã đúng qua D6 (dùng lại kernel), không có việc code mới.
