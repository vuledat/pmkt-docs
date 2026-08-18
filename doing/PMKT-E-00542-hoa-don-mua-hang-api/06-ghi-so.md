# F06 — Kế hoạch API Ghi sổ Hóa đơn mua hàng

> **Trạng thái:** BẢN NHÁP CHỜ REVIEW · **Ngày:** 2026-08-07  
> **Use Case:** PMKT-U-01166 (Ghi sổ đơn lẻ & hàng loạt)  
> **Màn hình:** `SCR_HDMH_DanhSach.md` & `SCR_HDMH_XemChiTiet.md`  
> **Tài liệu nguồn:** `4.usecases/PMKT-U-01166_GhiSo/UC_HDMH_GhiSo.md`, `5.screens/SCR_HDMH_DanhSach.md`, `6.messages.md`  

---

## 0. Các quyết định thiết kế

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Sử dụng `GhiSoNhanHoaDonTemplate` kế thừa từ `ChungTuTemplate` cho nghiệp vụ GHI_SO | Đảm bảo tính nhất quán của quy trình ghi sổ kế toán dự án; tự động gọi đúng API/Kernel. |
| **D2** | **Tự động ghi sổ CTMH gốc trước** (nếu chưa ghi sổ): Giao dịch đồng thời cùng ghi sổ gốc và ghi sổ hóa đơn trong 1 transaction | Tránh tình trạng lệch sổ; hóa đơn ghi sổ thuế nhưng gốc chưa ghi sổ hàng/nợ tạm tính. |
| **D3** | Ghi đồng thời 3 sổ: Sổ cái, Sổ thuế, Sổ công nợ | Đảm bảo tính nguyên tử của nghiệp vụ thuế GTGT; không ghi sổ kho. |
| **D4** | Hỗ trợ ghi sổ hàng loạt trả lỗi từng phần | API không chết đứng khi có 1 chứng từ lỗi; trả về bảng kết quả chi tiết cho FE vẽ popup. |

---

## 1. Phạm vi

### 1.1 Trong phạm vi
- Ghi sổ hóa đơn đơn lẻ: `POST /nhan-hoa-don/{id}/ghi-so`.
- Ghi sổ hóa đơn hàng loạt: `POST /nhan-hoa-don/ghi-so-hang-loat`.
- Kiểm tra đầy đủ thông tin bắt buộc và kỳ kế toán mở.
- Tự động gọi `UC_CTMH_GhiSo` cho các chứng từ mua hàng gốc chưa ghi sổ.
- Đẩy dòng định khoản **`Nợ TK 133 / Có TK 331`** sang kernel `GhiSoApi` để ghi vào Sổ cái, Sổ thuế (thuế GTGT đầu vào), và Sổ công nợ NCC.
- Chuyển trạng thái `status` của `ChungTuNhanHoaDon` sang `DA_GHI_SO` và `pur_hoa_don_mua.trang_thai` = `'Đã ghi sổ'`.

### 1.2 Ngoài phạm vi
- Ghi sổ hóa đơn kèm chứng từ (`laHDVeSau = false`) -> Bị ẩn nút, hạch toán nằm chung trong CTMH gốc.

---

## 2. Hiện trạng đã khảo sát
- Kernel `GhiSoApi.ghiSo` chịu trách nhiệm validate kỳ và thực hiện ghi vào 3 sổ đồng thời.
- `SoChungTuApi` tự động chống ghi sổ trùng.

---

## 3. Kiến trúc
```text
POST /nhan-hoa-don/{id}/ghi-so 
  → NhanHoaDonController.ghiSo
    → NhanHoaDonCrudService.ghiSo
      → GhiSoNhanHoaDonTemplate extends ChungTuTemplate (hanhDong = GHI_SO)
        → lock chung tu
        → validate business rules
        → call UC_CTMH_GhiSo for unposted source documents
        → build journal entry (Nợ 133 / Có 331)
        → call GhiSoApi.ghiSo
        → update status to DA_GHI_SO
```

---

## 4. Hợp đồng API

### 4.1 `POST /{id}/ghi-so` (Ghi sổ đơn lẻ)
**Response 200**:
```json
{
  "success": true,
  "messageId": "MSG_PMKT-E-00542_023",
  "message": "Ghi sổ hóa đơn thành công",
  "data": {
    "id": "b3e8c9a1-7d8b-4c5a-a1b2-c3d4e5f67a8b",
    "status": "DA_GHI_SO"
  }
}
```

### 4.2 `POST /ghi-so-hang-loat` (Ghi sổ hàng loạt)
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
  "messageId": "MSG_PMKT-E-00542_025",
  "message": "Ghi sổ thành công 2 hóa đơn, thất bại 0 hóa đơn",
  "data": {
    "thanhCong": 2,
    "thatBai": 0,
    "errors": []
  }
}
```

---

## 5. Quy tắc hạch toán & Ghi sổ

| Sổ ghi | Cột cập nhật | Tài khoản / Chi tiết |
|---|---|---|
| **Sổ cái** | `acc_so_cai` | Nợ `TK 133` / Có `TK 331` |
| **Sổ thuế** | Thuế GTGT đầu vào khấu trừ | Nợ `TK 133` + MST + Số HĐ + Doanh thu chưa thuế |
| **Sổ công nợ** | Phải trả NCC | Có `TK 331` + `nhaCungCapId` |

---

## 6. Kiểm thử (Verification Plan)
- **Unit test**: Test logic dựng bút toán thuế GTGT từ dòng chi tiết hóa đơn.
- **Integration test**:
  - Tạo mới hóa đơn nháp (status = NHAP) liên kết 1 CTMH nháp. Gọi API ghi sổ hóa đơn.
  - Verify: CTMH gốc tự động chuyển sang `DA_GHI_SO`, hóa đơn chuyển sang `DA_GHI_SO`, Sổ cái ghi nhận đầy đủ bút toán tạm tính của CTMH gốc và bút toán thuế của hóa đơn mua.
  - Gọi API ghi sổ hàng loạt với 1 hóa đơn hợp lệ và 1 hóa đơn thuộc kỳ đã khóa. Verify: Hóa đơn 1 ghi sổ thành công, hóa đơn 2 thất bại và được liệt kê lỗi trong `errors` response.
