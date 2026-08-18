# Chi tiết triển khai - PMKT-U-01166_GhiSo

## 1. Hợp đồng API

**Endpoint (Ghi sổ):** `POST /api/mua-hang/hoa-don-mua/{id}/ghi-so`
**Quyền:** `NhanHoaDon.Post`

**Endpoint (Bỏ ghi sổ):** `POST /api/mua-hang/hoa-don-mua/{id}/bo-ghi-so`
**Quyền:** `NhanHoaDon.Unpost`

**Ghi sổ hàng loạt:** `POST /api/mua-hang/hoa-don-mua/ghi-so-hang-loat`
**Bỏ ghi sổ hàng loạt:** `POST /api/mua-hang/hoa-don-mua/bo-ghi-so-hang-loat`

## 2. Luồng xử lý

**Ghi sổ:**
1. Check quyền.
2. Lấy `HoaDonMua` (đảm bảo `LaHDVeSau = true` và `TrangThaiChungTu = CHUA_GHI_SO`).
3. Sinh bút toán Nợ 133 / Có 331.
4. Lưu bút toán vào module `SoCaiApi`.
5. Cập nhật `TrangThaiChungTu = DA_GHI_SO`.
6. Thông báo thành công (`MSG_PMKT-E-00542_023`).

**Bỏ ghi sổ:**
1. Check quyền.
2. Kiểm tra điều kiện bỏ ghi sổ (`TrangThaiThanhToan == CHUA_THANH_TOAN` và kỳ kế toán chưa khóa).
3. Xóa sổ cái liên quan đến `ChungTuNhanHoaDon`.
4. Cập nhật `TrangThaiChungTu = CHUA_GHI_SO`.
5. Thông báo thành công (`MSG_PMKT-E-00542_024`).

## 3. Đặc thù nghiệp vụ

- Chú ý: Việc Ghi Sổ / Bỏ Ghi Sổ của Hóa Đơn Về Sau **KHÔNG** làm thay đổi trạng thái của Chứng từ gốc (`ChungTuMuaHang`). Cập nhật sổ cái chỉ tác động đến thuế GTGT (Nợ 133 / Có 331). Không ghi/xóa sổ kho.
- Các API hàng loạt sẽ nhận vào `XuLyHangLoatRequest` và thực hiện lần lượt các ID, tổng hợp kết quả (thành công/thất bại) để trả về frontend như định nghĩa trong `BaseChungTuController`.
