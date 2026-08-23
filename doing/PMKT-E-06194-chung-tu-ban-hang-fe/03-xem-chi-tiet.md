# 03 — Xem chi tiết Chứng từ bán hàng

## 1. Header

- **Mã màn**: SCR_CTBH_XemChiTiet
- **SCR nguồn**: `5.screens/SCR_CTBH_XemChiTiet.md` (50 dòng — layout giống ThemMoi, chỉ khai điểm khác biệt)
- **UC nguồn**: UC_CTBH_XemChiTiet
- **Route**: mở qua popup từ danh sách (link Số chứng từ / nút Xem)
- **File chính**: cùng `ChungTuBanHangThemMoiModal.tsx`, `mode = 'view'` (Luật cứng 2, `client/CLAUDE.md §5`)

## 2. Bố cục

Giống hệt `02-them-moi-va-chinh-sua.md` §2, đổi `readOnly = true` toàn bộ + đổi bộ nút footer.

## 3. Đặc tả UI từ Figma

Không đổi — không có link Figma riêng, dùng chung node của ThemMoi.

## 4. Ma trận ẩn/hiện · required · disabled

Dịch từ `Matrix/SCR_CTBH_XemChiTiet_MaTranAnHien.md` — **không đổi từ bản 18/08** ngoại trừ 1 điểm đã đối chiếu bởi commit `bb4c10eb9` (diff `SCR_CTBH_XemChiTiet.md | 10 +---`, 8 dòng đổi cho BR1):

| Nút | Điều kiện (BR1, đã cập nhật theo `bb4c10eb9`) | Trạng thái code |
|---|---|---|
| Chỉnh sửa | `TrangThaiGhiSo = "Chưa ghi sổ"` AND quyền sửa | ✅ khớp (dùng `trangThaiChungTu`, xem F6) |
| Ghi sổ | `TrangThaiGhiSo = "Chưa ghi sổ"` AND quyền ghi sổ | ✅ khớp |
| Bỏ ghi sổ | `TrangThaiGhiSo = "Đã ghi sổ"` AND quyền bỏ ghi sổ | ✅ khớp |
| Lập hóa đơn | `TrangThaiLapHoaDon ∈ {Chưa lập, Đã lập một phần}` AND quyền — **không phụ thuộc ghi sổ** | ❌ cùng gap F7 với màn Danh sách — sửa 1 lần dùng chung nếu tách hàm điều kiện vào `helpers/` (xem `01-danh-sach.md` §10 khuyến nghị) |
| **Xem dữ liệu ghi sổ** | Luôn hiển thị (BR mới) | ❌ **F11 — chưa có, D7 thêm mới** |
| Đóng | Luôn hiển thị | ✅ khớp |

Ma trận field vẫn `(đk-cfg)` theo cấu hình đã lưu — không đổi, mọi trường `Disable` (view-only). D5 thêm cột "Đơn đặt hàng" cũng theo cùng quy tắc — hiện dạng `Disable`.

## 5. Bảng cột / trường

Không đổi so với `02-them-moi-va-chinh-sua.md` §5, cộng thêm: 2 cột "Số lượng đã xuất HĐ/kho" + "Số lượng còn lại xuất HĐ/kho" hiện read-only ở màn này (ẩn ở Thêm mới) — **đã build**, không có gap mới ghi nhận ở lượt rà này (kế thừa nguyên trạng từ bản 18/08).

## 6. Hành vi & sự kiện

- **D4 (áp dụng chung với Danh sách)**: nút "Lập hóa đơn" trong popup Xem chi tiết dùng lại đúng hàm điều kiện sẽ tách ở `01-danh-sach.md` §10 — không viết logic riêng cho popup này.
- **D7**: thêm nút "Xem dữ liệu ghi sổ" vào bộ nút của popup Xem (giống `02-them-moi-va-chinh-sua.md` §6.2), luôn hiện.

## 7. Validation phía FE

Không áp dụng — màn chỉ đọc.

## 8. Luồng xử lý

Không đổi — `GET {base}/{id}` nạp dữ liệu, hiển thị read-only. D7 thêm 1 nhánh mở popup con, không gọi API mới (xem `02-them-moi-va-chinh-sua.md` §8).

## 9. Phân bổ file

Dùng chung toàn bộ với `02-them-moi-va-chinh-sua.md` §9 — không có file riêng cho Xem chi tiết (cùng component `ChungTuBanHangThemMoiModal.tsx`, khác `mode`).

## 10. Kiểm thử

| Case | Input → kỳ vọng | Loại |
|---|---|---|
| D7 nút hiện ở mode view | `mode = 'view'` → nút "Xem dữ liệu ghi sổ" render | `test/chungTuBanHang.render.test.tsx`, jsdom |
| Nút Lập hóa đơn dùng chung điều kiện với Danh sách | cùng case đã liệt kê ở `01-danh-sach.md` §10, chạy lại ở context popup Xem | jsdom hoặc `node` nếu tách hàm |

## 11. BR đã áp dụng

BR1 của SCR_CTBH_XemChiTiet (đã cập nhật bởi `bb4c10eb9`) · `BR21` mục 5 (Lập hóa đơn/Xuất hàng không phụ thuộc ghi sổ) · SCR_CTBH_XemDuLieuGhiSo BR01 (D7).

**Điểm cần xác nhận** — kế thừa **Q6** ở `00-ke-hoach-tong.md` §12: nút "Lập phiếu xuất kho" có thật sự nằm trên màn này không (mâu thuẫn giữa bảng "Chức năng" và BR23 của ThemMoi). Chưa code cho tới khi có câu trả lời — nếu BA xác nhận CÓ, bổ sung vào cùng đợt D4 (không mở đợt riêng).
