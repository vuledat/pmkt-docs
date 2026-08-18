# F03 — Kế hoạch API Chỉnh sửa Hóa đơn mua hàng

> **Trạng thái:** BẢN NHÁP CHỜ REVIEW · **Ngày:** 2026-08-07  
> **Use Case:** PMKT-U-01163  
> **Màn hình:** `SCR_HDMH_ChinhSua.md`  
> **Tài liệu nguồn:** `4.usecases/PMKT-U-01163_ChinhSua/UC_HDMH_ChinhSua.md`, `5.screens/SCR_HDMH_ChinhSua.md`, `6.messages.md`  

---

## 0. Các quyết định thiết kế

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Sử dụng `ChungTuTemplate` cho nghiệp vụ SUA, kết hợp cơ chế khóa chứng từ `ChungTuKhoaApi` | Tránh tranh chấp đồng thời (concurrency conflict); hai người dùng không thể sửa cùng một hóa đơn tại một thời điểm |
| **D2** | Cho phép thay đổi danh sách chứng từ gốc đã chọn trong đợt nhận hóa đơn | Cho phép chọn thêm hoặc bỏ bớt chứng từ gốc, tự động đồng bộ hóa cờ `DaNhanHoaDon` trên dòng chi tiết gốc. |
| **D3** | Validate Loại tiền & Tỷ giá đồng nhất kể cả khi chọn thêm chứng từ gốc mới | Đảm bảo tính nhất quán dữ liệu, chống lỗi lệch tiền tệ. |
| **D4** | Chặn chỉnh sửa phía BE nếu trạng thái khác `NHAP` | Phòng tránh bypass UI; trả lỗi `MSG_PMKT-E-00542_009`. |

---

## 1. Phạm vi

### 1.1 Trong phạm vi
- Cập nhật thông tin Header của chứng từ và hóa đơn: số chứng từ, ngày chứng từ, ngày hạch toán, diễn giải, số hóa đơn, ngày hóa đơn, mẫu số, ký hiệu, ghi chú.
- Cập nhật thông tin dòng chi tiết hóa đơn (chỉ các trường thuế GTGT: mã thuế, tiền thuế, tiền thuế quy đổi, nhóm HHDV mua vào).
- Chọn thêm chứng từ gốc mới (nạp dòng chi tiết mới, set `DaNhanHoaDon = true`).
- Bỏ chọn chứng từ gốc đang liên kết (xóa dòng chi tiết tương ứng, reset `DaNhanHoaDon = false`, clear `hoaDonMuaId` trên dòng gốc).
- Tính toán lại tổng tiền trên Header và cập nhật lại trạng thái nhận hóa đơn trên các chứng từ gốc.

### 1.2 Ngoài phạm vi
- Sửa đổi trực tiếp hóa đơn kèm chứng từ (LaHDVeSau = false) -> Bị ẩn nút trên UI; BE chặn cứng.

---

## 2. Hiện trạng đã khảo sát
- DB bảng `pur_chi_tiet_hoa_don` lưu `chung_tu_mua_hang_id` và `chi_tiet_chung_tu_mua_hang_id` để đối chiếu dòng chi tiết gốc.
- Base class `AbstractChungTuCrudService` cung cấp API update tổng thể.

---

## 3. Kiến trúc
```text
PUT /nhan-hoa-don/{id} 
  → NhanHoaDonController.update
    → NhanHoaDonCrudService.update
      → LuuNhanHoaDonTemplate extends ChungTuTemplate (hanhDong = SUA)
        → lock chung tu (ChungTuKhoaApi)
        → validate status == NHAP (MSG_009)
        → execute business logic (add/remove docs, update tax values)
        → save entities & reset/set DaNhanHoaDon on source lines
```

---

## 4. Hợp đồng API

### 4.1 `PUT /{id}` (Chỉnh sửa hóa đơn)
**Request Body**:
```json
{
  "soChungTu": "NHD-2026-0001",
  "ngayChungTu": "2026-08-07",
  "ngayHachToan": "2026-08-07",
  "dienGiai": "Nhận hóa đơn mua hàng đợt 1 - Cập nhật số HĐ",
  "soHoaDon": "0001234-A",
  "ngayHoaDon": "2026-08-07",
  "kyHieuHoaDon": "1C26TAA",
  "mauSoHoaDon": "1/001",
  "chungTuMuaHangIds": [
    "e5b8d4f6-82c9-4cf5-99d9-482a9386d8cf",
    "b8c9d4f6-82c9-4cf5-99d9-482a9386d8cf"
  ],
  "chiTiet": [
    {
      "id": "d9f8e7b2-6c8f-4cf5-a1a1-9876543210ab",
      "chiTietChungTuMuaHangId": "f7d9e8b2-6c8f-4cf5-a1a1-9876543210ab",
      "chungTuMuaHangId": "e5b8d4f6-82c9-4cf5-99d9-482a9386d8cf",
      "taiKhoanThueGtgtId": "3c2d1b0a-f9e8-8d7c-6b5a-4f3e2d1c0b9a",
      "thueSuatGtgt": 10.0,
      "tienThueGtgtVnd": 550000.00,
      "tienThueGtgtQuyDoi": 550000.00,
      "nhomHhdvMuaVao": "Nhóm 1"
    },
    {
      "chiTietChungTuMuaHangId": "a2b3c4d5-6c8f-4cf5-a1a1-9876543210ab",
      "chungTuMuaHangId": "b8c9d4f6-82c9-4cf5-99d9-482a9386d8cf",
      "taiKhoanThueGtgtId": "3c2d1b0a-f9e8-8d7c-6b5a-4f3e2d1c0b9a",
      "thueSuatGtgt": 10.0,
      "tienThueGtgtVnd": 200000.00,
      "tienThueGtgtQuyDoi": 200000.00,
      "nhomHhdvMuaVao": "Nhóm 1"
    }
  ]
}
```

**Response 200**:
```json
{
  "success": true,
  "messageId": "MSG_PMKT-E-00542_010",
  "message": "Cập nhật hóa đơn thành công",
  "data": {
    "id": "b3e8c9a1-7d8b-4c5a-a1b2-c3d4e5f67a8b",
    "soChungTu": "NHD-2026-0001",
    "status": "NHAP"
  }
}
```

---

## 5. Logic nghiệp vụ khi thêm/bớt chứng từ gốc
- **Bớt chứng từ gốc**:
  - So sánh `chungTuMuaHangIds` trong request với dữ liệu cũ trong DB.
  - Tìm ra ID chứng từ bị loại bỏ.
  - Reset cờ `da_nhan_hoa_don = false` và clear `hoaDonMuaId` trên các dòng chi tiết của chứng từ bị loại bỏ tại bảng `pur_chi_tiet_chung_tu_mua_hang`.
  - Cập nhật lại `trang_thai_nhan_hoa_don` của chứng từ gốc bị loại bỏ thành `"CHUA_NHAN"` hoặc `"NHAN_MOT_PHAN"`.
- **Thêm chứng từ gốc**:
  - Tìm các chứng từ gốc mới được thêm vào.
  - Validate cùng loại tiền và tỷ giá.
  - Set cờ `da_nhan_hoa_don = true` và lưu liên kết `hoaDonMuaId` trên các dòng chi tiết gốc.
  - Cập nhật `trang_thai_nhan_hoa_don` của chứng từ gốc mới thành `"DA_CO_HOA_DON"`.

---

## 6. Kiểm tra trùng hóa đơn (BR1)
- Hệ thống kiểm tra trùng bộ 4 trường: `nhaCungCapId + soHoaDon + kyHieuHoaDon + mauSoHoaDon` (loại trừ chính ID hóa đơn hiện tại).
- Nếu phát hiện trùng, trả về cảnh báo `MSG_PMKT-E-00542_002` dạng popup. Người dùng chọn tiếp tục lưu ghi đè hoặc hủy để điều chỉnh.

---

## 7. Kiểm thử (Verification Plan)
- **Unit test**: Test logic bớt chứng từ gốc và khôi phục trạng thái nhận hóa đơn trên các dòng gốc.
- **Integration test**:
  - Gửi request `PUT /nhan-hoa-don/{id}` loại bỏ 1 chứng từ gốc ra khỏi hóa đơn.
  - Verify: Dòng chi tiết hóa đơn bị xóa khỏi DB, cờ `DaNhanHoaDon` trên dòng chứng từ mua hàng gốc quay lại thành `false`, và trạng thái nhận hóa đơn của CTMH gốc quay lại thành `CHUA_NHAN`.
  - Gửi request sửa đổi hóa đơn đã ghi sổ, verify ném lỗi `MSG_PMKT-E-00542_009`.
