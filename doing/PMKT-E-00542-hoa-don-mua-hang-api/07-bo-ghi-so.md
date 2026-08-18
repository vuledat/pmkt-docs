# F07 — Kế hoạch API Bỏ ghi sổ Hóa đơn mua hàng

> **Trạng thái:** BẢN NHÁP CHỜ REVIEW · **Ngày:** 2026-08-07  
> **Use Case:** PMKT-U-01167 (Bỏ ghi sổ đơn lẻ & hàng loạt)  
> **Màn hình:** `SCR_HDMH_DanhSach.md` & `SCR_HDMH_XemChiTiet.md`  
> **Tài liệu nguồn:** `4.usecases/PMKT-U-01166_GhiSo/UC_HDMH_GhiSo.md`, `5.screens/SCR_HDMH_DanhSach.md`, `6.messages.md`  

---

## 0. Các quyết định thiết kế

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Sử dụng `BoGhiSoNhanHoaDonTemplate` kế thừa từ `ChungTuTemplate` cho nghiệp vụ BO_GHI_SO | Đảm bảo tính nhất quán của quy trình bỏ ghi sổ kế toán dự án. |
| **D2** | **Xóa vật lý bút toán thuế khỏi sổ cái**, không sinh bút toán đảo | Đảm bảo đúng chuẩn mực kế toán dự án đã chốt tại migration `V56`. |
| **D3** | **Không bỏ ghi sổ chứng từ mua hàng gốc**: Việc bỏ ghi sổ hóa đơn về sau độc lập với chứng từ gốc | Tránh gây nhiễu loạn sổ sách tồn kho và công nợ tạm tính của CTMH gốc. |
| **D4** | Chặn bỏ ghi sổ tại BE nếu đã thanh toán hoặc kỳ kế toán đã khóa | Trả lỗi và disable nút; bảo vệ tính an toàn dữ liệu tài chính. |

---

## 1. Phạm vi

### 1.1 Trong phạm vi
- Bỏ ghi sổ hóa đơn đơn lẻ: `POST /nhan-hoa-don/{id}/bo-ghi-so`.
- Bỏ ghi sổ hóa đơn hàng loạt: `POST /nhan-hoa-don/bo-ghi-so-hang-loat`.
- Kiểm tra điều kiện bỏ ghi sổ: `trangThaiThanhToan == "ChuaThanhToan"` và kỳ kế toán thuộc ngày hạch toán chưa khóa.
- Xóa vật lý dòng hạch toán `Nợ 133 / Có 331` của hóa đơn khỏi Sổ cái, Sổ công nợ NCC và Sổ thuế.
- Cập nhật trạng thái `status` của `ChungTuNhanHoaDon` sang `NHAP` và `pur_hoa_don_mua.trang_thai` = `'Chưa ghi sổ'`.

### 1.2 Ngoài phạm vi
- Bỏ ghi sổ chứng từ mua hàng gốc (muốn làm phải vào màn hình CTMH gốc thực hiện).

---

## 2. Hiện trạng đã khảo sát
- Kernel `GhiSoApi.boGhiSo` tự động thực hiện xóa vật lý các dòng bút toán khỏi `acc_so_cai` và các bảng sổ phụ liên quan.
- Cờ `trang_thai_thanh_toan` trên `pur_hoa_don_mua` phản ánh chính xác tình trạng thanh toán của hóa đơn.

---

## 3. Kiến trúc
```text
POST /nhan-hoa-don/{id}/bo-ghi-so 
  → NhanHoaDonController.boGhiSo
    → NhanHoaDonCrudService.boGhiSo
      → BoGhiSoNhanHoaDonTemplate extends ChungTuTemplate (hanhDong = BO_GHI_SO)
        → lock chung tu
        → validate constraints (payment, closed period)
        → call GhiSoApi.boGhiSo (physical delete entries)
        → update status to NHAP
```

---

## 4. Hợp đồng API

### 4.1 `POST /{id}/bo-ghi-so` (Bỏ ghi sổ đơn lẻ)
**Response 200**:
```json
{
  "success": true,
  "messageId": "MSG_PMKT-E-00542_024",
  "message": "Bỏ ghi sổ hóa đơn thành công",
  "data": {
    "id": "b3e8c9a1-7d8b-4c5a-a1b2-c3d4e5f67a8b",
    "status": "NHAP"
  }
}
```

### 4.2 `POST /bo-ghi-so-hang-loat` (Bỏ ghi sổ hàng loạt)
**Request Body**:
```json
{
  "ids": [
    "b3e8c9a1-7d8b-4c5a-a1b2-c3d4e5f67a8b",
    "c4f9e8a1-7d8b-4c5a-a1b2-c3d4e5f67a8b"
  ]
}
```

**Response 200**:
```json
{
  "success": true,
  "data": {
    "thanhCong": 2,
    "thatBai": 0,
    "errors": []
  }
}
```

---

## 5. Ràng buộc chặn Bỏ ghi sổ
- **Đã thanh toán**: Nếu `trangThaiThanhToan != "ChuaThanhToan"` (ví dụ: `DaThanhToan` hoặc `ThanhToanMotPhan`) → Disable nút trên UI và chặn ở BE (ném lỗi).
- **Kỳ kế toán đã khóa**: Nếu kỳ kế toán của ngày hạch toán đã đóng → Disable nút trên UI và chặn ở BE (ném lỗi).

---

## 6. Kiểm thử (Verification Plan)
- **Unit test**: Test logic kiểm tra điều kiện bỏ ghi sổ.
- **Integration test**:
  - Thực hiện bỏ ghi sổ hóa đơn đã ghi sổ. Verify: Hóa đơn quay về trạng thái `NHAP`, các bút toán thuế GTGT biến mất khỏi sổ cái, sổ thuế, sổ công nợ NCC. Chứng từ gốc liên quan vẫn giữ nguyên trạng thái `DA_GHI_SO` và giữ nguyên hạch toán.
  - Gửi request bỏ ghi sổ hóa đơn đã có thanh toán liên kết, verify trả lỗi chặn đứng.
