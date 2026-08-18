# Chi tiết triển khai - PMKT-U-01165_XemChiTiet

## 1. Hợp đồng API

**Endpoint:** `GET /api/mua-hang/hoa-don-mua/{id}`
**Quyền:** `NhanHoaDon.View.Detail`

```jsonc
// Response 200 OK
{
  "code": 200,
  "data": {
     // Dữ liệu HoaDonMuaDto chứa cả ChungTuNhanHoaDonDto, ChiTietHoaDonDto, TongHopThueDto...
  }
}
```

## 2. Luồng xử lý

- Lấy `HoaDonMua` theo `id`.
- Fetch `ChungTuNhanHoaDon`.
- Fetch list `ChiTietHoaDon`.
- Tính toán Section 4 (Tổng hợp tiền thuế).
- Ánh xạ sang DTO trả về.

## 3. Đặc thù nghiệp vụ

- Tương tự như sửa, nhưng không giới hạn trạng thái. Tuy nhiên, nếu Hóa Đơn Kèm CT (`LaHDVeSau = false`), mặc dù UC có nhắc đến điều hướng ở frontend sang Chứng từ mua hàng, API GET của Hóa đơn mua hàng vẫn trả về bình thường nếu FE lỡ gọi, hoặc có thể BE ném một Response báo chuyển hướng, nhưng chuẩn nhất là trả đúng data read-only.
- Nếu không tìm thấy, BE trả về 404 (Hoặc tùy biến trả lỗi `MSG_PMKT-E-00542_028`).
