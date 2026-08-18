# PMKT-E-06194 — Chứng từ bán hàng (FE) — Đối chiếu tài liệu ↔ code

| | |
|---|---|
| **Trạng thái** | 🟡 Màn đã chạy, còn 5 khoảng cách so với BA |
| **Ngày rà** | 2026-08-18 |
| **Câu hỏi khởi nguồn** | *"3 loại nghiệp vụ Bán hàng trong nước / xuất khẩu / Bán dịch vụ khác gì nhau, code đáp ứng chưa?"* |
| **Tài liệu gốc** | `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_ThemMoi.md` (1583 dòng) |
| **Module FE** | `client/src/features/banHang/chungTuBanHang/` |
| **Plan BE đi kèm** | [`../PMKT-E-06194-chung-tu-ban-hang-api/00-ke-hoach-tong.md`](../PMKT-E-06194-chung-tu-ban-hang-api/00-ke-hoach-tong.md) — bảng G |

> **Tài liệu 06194 KHÔNG đổi dòng nào** trong 39 commit mới của `pmkt-docs` (fetch 2026-08-18 23:32).
> Năm khoảng cách dưới đây là **nợ có sẵn**, không phải hệ quả của tài liệu đổi. `Công trình → Vụ việc`
> (commit `9f391dce0`) chỉ chạm `PMKT-E-14700_HopDongBanHang` — epic chưa có module FE.

---

## 1. Ba loại nghiệp vụ khác nhau ở đâu

`sal_chung_tu_ban.LoaiNghiepVu` có 3 giá trị nhưng **hai cửa vào**: `Bán dịch vụ` thuộc màn riêng
`SCR_CTbanDichVu_ThemMoi` (PMKT-E-06195), không nằm trong combo của màn này (**BR24**).

| Trục | Trong nước | Xuất khẩu | Bán dịch vụ |
|---|---|---|---|
| % thuế GTGT | 0·5·8·10·KCT·KKKNT·KHAC | **chỉ 0 · KCT** | như trong nước |
| Cột `Tiền thuế GTGT`, `TK Thuế GTGT` | hiện | **ẩn cả cột** | hiện |
| Tab Thuế | hiện | **ẩn cả tab** | hiện |
| Khối cột thuế XK (6 trường) | ẩn | **hiện** | ẩn |
| Section Tổng hợp | `Tiền thuế GTGT` | `Tổng thuế XK` | `Tiền thuế GTGT` |
| Tổng thanh toán | cộng thuế GTGT | **không** cộng thuế XK¹ | cộng thuế GTGT |
| `Kiêm phiếu xuất kho` + nhóm cột kho | có | có | **ẩn hết** |
| Xuất kho · giá vốn | có | có | không |
| Bút toán thuế | #4 Nợ CN / Có TK thuế GTGT | #5 **Nợ DT** / Có TK thuế XK | #4 |
| Định khoản ngầm định | 3 tổ hợp theo Thu tiền ngay × HTTT | 1 (không phụ thuộc) | 3 tổ hợp |

¹ Thuế XK là khoản nộp NSNN **giảm trừ doanh thu**, không thu của khách (BR20 §3).

## 2. Năm khoảng cách — bảng F

| # | Khoảng cách | Bằng chứng | Trạng thái |
|---|---|---|---|
| **F1** | Combo `Loại nghiệp vụ` cho chọn **Bán dịch vụ**, trái BR24. `POST /lookup` trả cả 3 giá trị, FE đổ thẳng vào combo; API tạo/sửa lại từ chối → chọn xong ăn lỗi ở bước Lưu. | `lookups.ts:296` → `ChungTuBanHangThemMoiModal.tsx` combo | ✅ **ĐÃ SỬA 2026-08-18** — `loaiNghiepVuHopLe()` + `LOAI_NGHIEP_VU_MAN_BAN_HANG`. Gốc BE vẫn còn: xem **G14**. |
| **F2** | Tab **Thuế** không ẩn khi xuất khẩu (BR13 §5 + mục "Tab Thuế"). Tab luôn rỗng, đọc ra là "chưa nhập" chứ không phải "không áp dụng". | `gridTabs` — mảng phẳng, deps không có `xuatKhau` | ✅ **ĐÃ SỬA 2026-08-18** — lọc theo `nguCanh.xuatKhau`. |
| **F3** | Mặc định combo lấy `enums.loaiNghiepVu[0]`, tức phụ thuộc **thứ tự enum trong file Java**. Đảo một dòng bên BE là màn mặc định sang xuất khẩu, không test nào đỏ. | seed `useEffect` của modal | ✅ **ĐÃ SỬA 2026-08-18** — `loaiNghiepVuMacDinh()` neo vào `Bán hàng trong nước` theo BR24. |
| **F4** | Lưới thiếu **2/6 trường BR14**: `Giá trị tính thuế XK quy đổi` · `Tiền thuế XK quy đổi`. Tệ hơn: cột đang gắn nhãn "Giá trị tính thuế XK" ghi vào `donGiaThueXk`, mà BE **ghi đè** trường đó → số người dùng nhập theo Tờ khai Hải quan mất trắng. | `chiTietFields.ts` khối thuế XK (4 cột) · `tongHop.ts` tự nhận *"thuế XK không có cột quy đổi riêng"* | ❌ **CHẶN BỞI BE** — DTO chưa lộ `giaTriTinhThueXk` / `giaTriTinhThueXkQuyDoi`. Xem **G13**. |
| **F5** | **BR16 định khoản ngầm định chưa có.** TK hiện tự điền từ **danh mục vật tư**, không phải từ định khoản của loại chứng từ; `TK công nợ` · `TK thuế GTGT` · `TK thuế XK` không tự điền gì. Luật *"đổi Loại nghiệp vụ → tra lại và áp lại TK cho dòng chưa sửa tay"* cũng chưa có. | `chiTietFields.ts:218-221` | ⏸ **LỆCH CÓ CHỦ Ý** — BA đã chốt hoãn ở [Q2](../PMKT-E-06194-chung-tu-ban-hang-api/00-ke-hoach-tong.md) (bảng định khoản chưa tồn tại trong DB). Không phải bug FE. |

## 3. Đọc bảng F thế nào

- **F1 · F2 · F3 đã đóng** — mỗi cái là một hàm thuần trong `helpers/anHien.ts`, có test `node` phủ
  (`test/anHienVaDongBo.test.ts`, khối "BR24"), đã kiểm bằng đột biến: gỡ bộ lọc thì 2 test đỏ.
- **F4 là mất dữ liệu im lặng, không phải thiếu tính năng** — ưu tiên cao nhất, nhưng phải chờ
  **G13** bên BE. Thứ tự đúng: BE lộ 2 trường → FE bổ sung 2 cột quy đổi + trỏ lại cột nguyên tệ.
- **F5 không làm ở đợt này** theo quyết định BA; chỉ cần bảo đảm chỗ nào sẽ tra thì có comment trỏ về Q2.
- Loại nghiệp vụ thứ ba (**Bán dịch vụ**) chưa có màn — xem
  [`../PMKT-E-06195-chung-tu-ban-dich-vu-fe/00-ke-hoach-tong.md`](../PMKT-E-06195-chung-tu-ban-dich-vu-fe/00-ke-hoach-tong.md),
  mục "⚠ Khiếm khuyết đang chạy".

## 4. BR đã áp dụng ở lượt sửa này

`BR13` §1 §5 (thuế suất theo loại nghiệp vụ · ẩn tab Thuế) · `BR24` (phạm vi + mặc định `LoaiNghiepVu`).

**BR chưa đạt:** `BR14` (2/6 trường — chặn bởi G13) · `BR16` (hoãn theo Q2).
