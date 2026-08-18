# F05 — Kế hoạch API Xem chi tiết Hóa đơn mua hàng

> **Trạng thái:** BẢN NHÁP CHỜ REVIEW · **Ngày:** 2026-08-07  
> **Use Case:** PMKT-U-01165  
> **Màn hình:** `SCR_HDMH_XemChiTiet.md`  
> **Tài liệu nguồn:** `4.usecases/PMKT-U-01165_XemChiTiet/UC_HDMH_XemChiTiet.md`, `5.screens/SCR_HDMH_XemChiTiet.md`, `6.messages.md`  

---

## 0. Các quyết định thiết kế

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Trả về cờ điều hướng và ID gốc đối với Hóa đơn kèm chứng từ (`laHDVeSau = false`) | FE nhận diện để tự động redirect sang màn hình xem chi tiết CTMH gốc. |
| **D2** | Đọc dữ liệu hạch toán thực tế từ Sổ cái qua `SoCaiApi` khi hóa đơn đã ghi sổ | Đảm bảo tính trung thực của dữ liệu kế toán thực tế, không tính toán dự phòng. |
| **D3** | Validate sự tồn tại của hóa đơn và cờ `da_xoa` tại Server | Đảm bảo trả lỗi `404` (hoặc `MSG_PMKT-E-00542_028`) khi ID không hợp lệ hoặc đã bị xóa mềm. |

---

## 1. Phạm vi

### 1.1 Trong phạm vi
- Endpoint `GET /nhan-hoa-don/{id}` trả về dữ liệu 4 phần (Section 1, 2, 3, 4) đầy đủ thông tin hóa đơn độc lập (Hóa đơn về sau).
- Trả về cờ điều hướng `laHDVeSau = false` và `chungTuMuaHangId` đối với Hóa đơn kèm chứng từ.
- Tải danh sách dòng chi tiết từ `pur_chi_tiet_hoa_don` (Tab Chi tiết hàng).
- Tổng hợp thuế GTGT theo nhóm (Tab Thuế).
- Đọc bút toán thực tế từ Sổ cái qua `SoCaiApi` (Tab Hạch toán).
- Tải danh sách chứng từ tham chiếu (Tab Tham chiếu).

### 1.2 Ngoài phạm vi
- Sửa đổi trực tiếp dữ liệu tại màn chi tiết (xử lý xem F03).

---

## 2. Hiện trạng đã khảo sát
- `SoCaiApi.theoChungTu(id)` hoạt động ổn định và lọc chính xác các bút toán thuộc `chung_tu_nhan_hoa_don_id`.
- Bảng tham chiếu `pur_chung_tu_tham_chieu` lưu liên kết các chứng từ.

---

## 3. Kiến trúc
```text
GET /nhan-hoa-don/{id} 
  → NhanHoaDonController.getOne
    → NhanHoaDonCrudService.getOne
      → load ChungTuNhanHoaDon (kiểm tra da_xoa, ném MSG_028 nếu fail)
      → load HoaDonMua & ChiTietHoaDon
      → IF laHDVeSau = true:
          ├─ call SoCaiApi.theoChungTu(id)
          └─ load ChungTuThamChieu
```

---

## 4. Hợp đồng API

### 4.1 `GET /{id}`
**Response 200 (Đối với Hóa đơn về sau - laHDVeSau = true)**:
```json
{
  "success": true,
  "data": {
    "id": "b3e8c9a1-7d8b-4c5a-a1b2-c3d4e5f67a8b",
    "soChungTu": "NHD-2026-0001",
    "ngayChungTu": "2026-08-07",
    "ngayHachToan": "2026-08-07",
    "dienGiai": "Nhận hóa đơn mua hàng đợt 1",
    "status": "DA_GHI_SO",
    "laHDVeSau": true,
    "nhaCungCapId": "c6a2b8e8-71e8-466d-8c10-fa2cde64848d",
    "tenNhaCungCap": "Công ty TNHH Cung ứng Vật tư Dopai",
    "maSoThue": "0102030405",
    "diaChi": "123 Đường Láng, Đống Đa, Hà Nội",
    "soHoaDon": "0001234",
    "ngayHoaDon": "2026-08-07",
    "kyHieuHoaDon": "1C26TAA",
    "mauSoHoaDon": "1/001",
    "loaiTienId": "d8a1b2c3-e4f5-6a7b-8c9d-0e1f2a3b4c5d",
    "tyGia": 1.0,
    "tongTruocThueVnd": 10000000.00,
    "tongThueGtgtVnd": 1000000.00,
    "tongSauThueVnd": 11000000.00,
    "chiTiet": [
      {
        "id": "d9f8e7b2-6c8f-4cf5-a1a1-9876543210ab",
        "maHang": "VT-0001",
        "tenHang": "Thép cuộn phi 6",
        "taiKhoanThueGtgtId": "3c2d1b0a-f9e8-8d7c-6b5a-4f3e2d1c0b9a",
        "taiKhoanCoId": "3c2d1b0a-f9e8-8d7c-6b5a-4f3e2d1c0b9b",
        "giaTriChuaThueVnd": 10000000.00,
        "thueSuatGtgt": 10.0,
        "tienThueGtgtVnd": 1000000.00,
        "nhomHhdvMuaVao": "Nhóm 1"
      }
    ],
    "hachToan": [
      {
        "taiKhoanNo": "1331",
        "taiKhoanCo": "331",
        "soTienVnd": 1000000.00,
        "dienGiai": "Thuế GTGT đầu vào"
      }
    ],
    "thamChieu": [
      {
        "soChungTu": "CTMH-2026-0089",
        "loaiChungTu": "Chứng từ mua hàng"
      }
    ]
  }
}
```

**Response 200 (Đối với Hóa đơn kèm chứng từ - laHDVeSau = false)**:
```json
{
  "success": true,
  "data": {
    "id": "c4f9e8a1-7d8b-4c5a-a1b2-c3d4e5f67a8b",
    "laHDVeSau": false,
    "chungTuMuaHangId": "e5b8d4f6-82c9-4cf5-99d9-482a9386d8cf"
  }
}
```

---

## 5. Xử lý lỗi không tìm thấy (MSG_028)
- Nếu hóa đơn không tồn tại hoặc đã bị xóa mềm (`da_xoa = true`), ném lỗi `MSG_PMKT-E-00542_028` ("Không tìm thấy thông tin hóa đơn") kèm mã HTTP Status `404`.

---

## 6. Kiểm thử (Verification Plan)
- **Unit test**: Test logic phân phối dữ liệu dựa trên cờ `laHDVeSau`.
- **Integration test**:
  - Gọi API `GET /nhan-hoa-don/{id}` với 1 hóa đơn về sau hợp lệ. Verify: Dữ liệu trả về đầy đủ 4 phần và Tab Hạch toán chứa đúng dòng bút toán từ sổ cái.
  - Gửi ID hóa đơn kèm chứng từ, verify trả về cờ `laHDVeSau = false` và ID chứng từ mua hàng gốc để FE điều hướng.
