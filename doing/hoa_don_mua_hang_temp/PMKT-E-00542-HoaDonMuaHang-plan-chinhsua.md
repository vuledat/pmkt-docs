# Chi tiết triển khai - PMKT-U-01163_ChinhSua

## 1. Hợp đồng API (Base Update)

**Endpoint:** `PUT /api/mua-hang/hoa-don-mua/{id}`
**Quyền:** `NhanHoaDon.Edit`

```jsonc
// Request Body
{
  "chungTuNhanHoaDon": {
    "soChungTu": "CT-1234",
    "ngayChungTu": "2023-10-01",
    "ngayHachToan": "2023-10-05",
    "dienGiai": "Sửa diễn giải"
  },
  "hoaDonMua": {
    "nhaCungCapId": "uuid",
    "mauSoHoaDon": "01GTKT",
    "kyHieuHoaDon": "AA/20E",
    "soHoaDon": "1234567",
    "ngayHoaDon": "2023-10-01"
  },
  "chiTietHoaDon": [
    // Chi tiết cập nhật (chỉ được update thuế GTGT)
  ],
  "chungTuThamChieuIds": ["uuid", "uuid"]
}

// Response 200 OK
{
  "code": 200,
  "data": { ... HoaDonMuaDto ... },
  "message": "Cập nhật hóa đơn thành công" // MSG_PMKT-E-00542_010
}
```

## 2. Luồng xử lý

- BE phải kiểm tra ID Hóa đơn có tồn tại và thuộc trạng thái **Chưa ghi sổ** và **LaHDVeSau = true**. Nếu không thỏa ném lỗi `MSG_PMKT-E-00542_009`.
- Nếu chứng từ gốc bị gỡ/bỏ chọn (FE gửi lên không có chi tiết của chứng từ đó): 
  - Delete `ChiTietHoaDon` liên đới.
  - Reset `ChiTietChungTuMuaHang.DaNhanHoaDon = false`.
  - Tổng hợp lại `TrangThaiNhanHoaDon` cho chứng từ gốc.
- Tính toán và lưu thông tin cập nhật vào Database.
- Cập nhật chứng từ tham chiếu.

## 3. Đặc thù nghiệp vụ

- **Check trùng**: Giống như Thêm mới nhưng **loại trừ HĐ hiện tại** đang sửa. Nếu trùng, ném warning `MSG_PMKT-E-00542_002` để FE hiển thị.
- Không thể sửa hóa đơn đã ghi sổ. Cần chặn cứng ở BE.
