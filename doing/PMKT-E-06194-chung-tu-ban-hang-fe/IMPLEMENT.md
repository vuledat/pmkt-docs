# IMPLEMENT — PMKT-E-06194 Chứng từ bán hàng FE

## 2026-09-05 — Lập phiếu xuất từ danh sách Chứng từ bán hàng

- Phạm vi: nối thao tác `Lập phiếu xuất` sang popup Thêm mới Phiếu xuất kho và tự nạp đúng phần
  hàng hóa còn phải xuất của chứng từ nguồn; giữ số chứng từ bán hàng trên dòng nguồn.
- FE sửa `phieuXuatKho/api/themMoiApi.ts` để gửi `chungTuBanHangId`; popup truyền ID nhận từ URL.
- BE bổ sung query param tùy chọn `chungTuBanHangId` cho `GET /api/kho/nguon-xuat-ban` và chuyển
  thẳng vào `BoLocDongConLai`, tránh quét toàn bộ nguồn rồi lọc lại tại client.
- Reuse: giữ nguyên `layNguonBanHang`, `themDongTuNguon`, `dienThongTinTuNguon` và popup hiện có;
  không tạo component mới.
- Lệch plan: hợp đồng API thêm bộ lọc tùy chọn, tương thích ngược với popup chọn nguồn thông thường.
- Nợ kỹ thuật: không phát sinh mock/TODO mới. Hóa đơn điều chỉnh nằm ngoài phạm vi.
- BR áp dụng: `SCR_CTBH_DanhSach` BR04/R-CTBH-012; `SCR_PhieuXuatKho_ThemMoi` BR8, BR20, BR21,
  BR34 và VAL-004.
- Kiểm tra: TypeScript typecheck đạt; ESLint các file sửa đạt; 3 file test liên quan đạt; Vite build
  đạt; unit test backend `NguonBanHangCapChoKhoTest` đạt (`BUILD SUCCESSFUL`). Không chạy full suite,
  lint toàn repo hay lint boundaries.
