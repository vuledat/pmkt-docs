# PMKT-E-06194 Chứng từ bán hàng — Bản đồ nguồn tài liệu

| | |
|---|---|
| Phiếu yêu cầu | `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/` |
| Commit tài liệu | `8cf9606ea` |
| Ngày soát | 2026-08-28 |
| Mã viết tắt | `CTBH` (lấy từ tiền tố `SCR_CTBH_*` / `UC_CTBH_*`) |
| Trạng thái | **ĐÃ SOÁT** — còn **7** mục `OPEN` (5 P0 · 2 P1) |
| Sinh bởi | `/audit-spec` |

---

## §1. Bảng file nguồn

| File | Loại | Bậc | Trạng thái | Dòng |
|---|---|---|---|---|
| `6.messages.md` | message | **5** | duyệt | 80 |
| `Common/business_rules.md` (BR1–BR49, tra qua `br.sh`) | BR chung | **5** | duyệt | — |
| `5.screens/SCR_CTBH_ThemMoi.md` | màn hình — **anchor** | 4 | duyệt | 1624 |
| `5.screens/SCR_CTBH_DanhSach.md` | màn hình | 4 | duyệt | 228 |
| `5.screens/SCR_CTBH_PopupXacNhanXoa.md` | màn hình | 4 | duyệt | 83 |
| `5.screens/SCR_CTBH_XemChiTiet.md` | màn hình | 4 | duyệt | 50 |
| `5.screens/SCR_CTBH_CapNhat.md` | màn hình | 4 | duyệt | 46 |
| `5.screens/SCR_CTBH_XemDuLieuGhiSo.md` | màn hình | 4 | duyệt | 155 |
| `5.screens/SCR_CTBH_PBCK.md` | màn hình | 4 | duyệt | 122 |
| `5.screens/SCR_CTBH_PBCK_MHHD.md` | màn hình | 4 | duyệt | 126 |
| `4.usecases/ThemMoi/UC_CTBH_ThemMoi.md` | use case | 3 | duyệt | 105 |
| `4.usecases/ChinhSua/UC_CTBH_ChinhSua.md` | use case | 3 | duyệt | 107 |
| `4.usecases/Xoa/UC_CTBH_Xoa.md` | use case | 3 | duyệt | 127 |
| `4.usecases/GhiSo/UC_CTBH_GhiSo.md` | use case | 3 | duyệt | 89 |
| `4.usecases/BoGhiSo/UC_CTBH_BoGhiSo.md` | use case | 3 | duyệt | 83 |
| `4.usecases/XemDanhSach/UC_CTBH_DanhSach.md` | use case | 3 | duyệt | 188 |
| `4.usecases/XemChiTiet/UC_CTBH_XemChiTiet.md` | use case | 3 | duyệt | 111 |
| `Matrix/…/SCR_CTBH_ThemMoi_MaTranAnHien.md` | ma trận | **0** | `[DRAFT — chờ duyệt]` | 133 |
| `Matrix/…/SCR_CTBH_CapNhat_MaTranAnHien.md` | ma trận | **0** | `[DRAFT — chờ duyệt]` | 55 |
| `Matrix/…/SCR_CTBH_XemChiTiet_MaTranAnHien.md` | ma trận | **0** | `[DRAFT — chờ duyệt]` | 100 |
| `Matrix/…/SCR_CTBH_PBCK_MaTranAnHien.md` | ma trận | **0** | `[DRAFT — chờ duyệt]` | 55 |
| `Matrix/…/SCR_CTBH_PBCK_MHHD_MaTranAnHien.md` | ma trận | **0** | `[DRAFT — chờ duyệt]` | 55 |
| `4.usecases/**/AD_*.puml` (6 file) | sơ đồ | 1 | — | 77–122 |
| `1.functions-breakdown.md` · `2.usecases.puml` · `3.crud-matrix.puml` | phạm vi | 1 | — | — |

> **Cả 5 file Matrix đều còn `[DRAFT — chờ duyệt]`** → bậc 0, **không được dùng làm luật**. Luật ẩn/hiện
> trong `02-rules.md` lấy từ `SCR_*` (bậc 4), không lấy từ Matrix.

---

## §2. Bảng chủ đề → nguồn

| Chủ đề | Nguồn | Bậc | Kết luận |
|---|---|---|---|
| Nội dung & mã thông báo | `6.messages.md` | 5 | chốt — trừ `MSG_…_109` (xem §4) |
| Thao tác hàng loạt (chính sách bỏ qua/chặn) | `business_rules.md` BR45 | 5 | partial success |
| | `SCR_CTBH_PopupXacNhanXoa.md:38-43` (BR02) | 4 | partial success — khớp BR45 |
| | `SCR_CTBH_DanhSach.md:81` | 4 | partial success — khớp BR45 |
| | `UC_CTBH_Xoa.md:11,86-89` (AC1) | 3 | **all-or-nothing, disable nút** → `C01` |
| | `AD_CTBH_Xoa.puml:48,55,62` | 1 | disable — củng cố UC |
| Mã lỗi "chứng từ đã sử dụng, không xóa được" | `SCR_CTBH_PopupXacNhanXoa.md:27,50` | 4 | `MSG_…_111` → `C02` |
| | `SCR_CTBH_DanhSach.md:64` | 4 | `MSG_…_111` |
| | `SCR_CTBH_ThemMoi.md:1552` (BR23 mục 9) | 4 | **`MSG_…_014`** → `C02` |
| | `UC_CTBH_Xoa.md:71` | 3 | `MSG_…_014` |
| Định nghĩa "đã sử dụng ở nghiệp vụ khác" | `SCR_CTBH_PopupXacNhanXoa.md:52-64` (BR04) | 4 | bảng chặn/không chặn chi tiết → `C03` |
| | `UC_CTBH_Xoa.md:96-103` | 3 | "đã tạo phiếu thu" (rộng hơn) → `C03` |
| Counter > 0 có chặn xóa không | `SCR_CTBH_PopupXacNhanXoa.md:62` (BR04) | 4 | counter > 0 → **chặn** → `C04` |
| | `SCR_CTBH_ThemMoi.md:1481-1485` (BR23 mục 4) | 4 | kiêm → counter = `SoLuong` ngay khi lưu → `C04` |
| | `SCR_CTBH_PopupXacNhanXoa.md:58` (BR04 cột phải) | 4 | phiếu kiêm **không chặn** → `C04` |
| Xóa CTBH có hóa đơn lập kèm | `SCR_CTBH_PopupXacNhanXoa.md:58` (BR04 cột trái) | 4 | có `sal_hoa_don_ban_hang.ChungTuBanId` → **chặn** → `C05` |
| | `SCR_CTBH_PopupXacNhanXoa.md:69` (BR05) | 4 | **xóa kèm** hóa đơn lập kèm → `C05` |
| | `SCR_CTBH_ThemMoi.md:1052` (BR18 mục 6) | 4 | chỉ nói xóa kèm "phiếu liên kết", không nói hóa đơn |
| | `UC_CTBH_Xoa.md:108` | 3 | xóa mềm kèm cả `HoaDonBanHang` |
| Sửa chứng từ đã có liên kết | `UC_CTBH_ChinhSua.md:9` (AC1) | 3 | đã sử dụng → **không cho sửa** → `C06` |
| | `SCR_CTBH_ThemMoi.md:1554` (BR23 mục 9) | 4 | cho sửa `SoLuong` với ràng buộc `≥ MAX(counter)` → `C06` |
| Nút "Lập phiếu xuất kho" trên Xem chi tiết | `SCR_CTBH_ThemMoi.md:1520` (BR23 mục 6.1) | 4 | **có** trên `SCR_CTBH_XemChiTiet` → `C07` |
| | `SCR_CTBH_XemChiTiet.md:23-41` | 4 | **không liệt kê** → `C07` |
| | `UC_CTBH_XemChiTiet.md:14,39-44` | 3 | không liệt kê |
| Cho phép sửa cột CK theo mặt hàng / hóa đơn | `SCR_CTBH_ThemMoi.md:219-224` (bảng trường) | 4 | Cho phép sửa = **N** → `C08` |
| | `SCR_CTBH_ThemMoi.md:747-758` (BR12.d TH1) | 4 | người dùng **nhập tay** → `C08` |
| Cho phép sửa "Tỷ lệ phân bổ" (popup PBCK) | `SCR_CTBH_PBCK.md:35` (bảng trường) | 4 | Cho phép sửa = **N** → `C09` |
| | `SCR_CTBH_PBCK.md:58-64` (BR3) | 4 | Thủ công → **enabled** → `C09` |
| Khởi tạo counter khi Lưu | `SCR_CTBH_ThemMoi.md:1481-1485` (BR23 mục 4) | 4 | **chốt** → `R-CTBH-060…063` |
| | `UC_CTBH_ThemMoi.md:26` (AC4) | 3 | **khớp** — đã dẫn chiếu BR23 mục 4, không mâu thuẫn |
| Bút toán & mapping sổ cái | `SCR_CTBH_ThemMoi.md:1133-1281` (BR20) | 4 | chốt — nguồn duy nhất |
| Ghi sổ / bỏ ghi sổ đồng bộ nhóm | `SCR_CTBH_ThemMoi.md:1288-1370` (BR21) | 4 | chốt |
| | `UC_CTBH_GhiSo.md` · `UC_CTBH_BoGhiSo.md` | 3 | khớp BR21 |
| Trạng thái dẫn xuất (4 trạng thái) | `SCR_CTBH_ThemMoi.md:1372-1426` (BR22) | 4 | chốt |
| Định khoản ngầm định | `SCR_CTBH_ThemMoi.md:896-956` (BR16) | 4 | chốt |
| Đánh số chứng từ | `SCR_CTBH_ThemMoi.md:1575-1579` (BR25) + BR20 chung | 4/5 | chốt |

---

## §3. UC → luật

| UC | Mã | Luật sinh ra | Ghi chú |
|---|---|---|---|
| `UC_CTBH_DanhSach` | PMKT-U-06396 | `R-CTBH-001…014` | lọc mặc định, cột, nút theo trạng thái, dòng tổng |
| `UC_CTBH_XemChiTiet` | PMKT-U-06400…06402, 06985 | `R-CTBH-015…020` | nút theo trạng thái, khu chi tiết dưới lưới |
| `UC_CTBH_ThemMoi` | PMKT-U-06397…06399, 06461, 06982 | `R-CTBH-021…075` | phần lớn luật nghiệp vụ nằm ở đây |
| `UC_CTBH_ChinhSua` | PMKT-U-06403…06405, 06983 | `R-CTBH-076…082` | |
| `UC_CTBH_Xoa` | PMKT-U-06406…06408, 06984 | `R-CTBH-083…090` | 5/8 luật đang `CHỜ` |
| `UC_CTBH_GhiSo` | PMKT-U-06430 | `R-CTBH-091…099` | |
| `UC_CTBH_BoGhiSo` | PMKT-U-06431 | `R-CTBH-100…106` | |
| — (màn Xem dữ liệu ghi sổ) | — | `R-CTBH-107…112` | không có UC riêng, chỉ có `SCR_CTBH_XemDuLieuGhiSo` |

**Không sót UC nào.** Chức năng "Chứng từ bán hàng có Chiết khấu (PMKT-U-06966)" trong
`1.functions-breakdown.md:37` **không có UC riêng** — `SCR_CTBH_ThemMoi.md:7` ghi rõ *"logic đã được
gộp vào BR12"*, luật nằm ở `R-CTBH-040…052`.

---

## §4. Message chưa có luật dùng

Mã tồn tại trong `6.messages.md` nhưng **không luật `R-…` nào tham chiếu** — hoặc BA thiếu luật, hoặc
mã thừa. Cần BA rà:

| Mã | Nội dung | Nhận xét |
|---|---|---|
| `MSG_…_012` | Bản ghi không tồn tại | trùng vai trò với `_011`; không BR nào dùng |
| `MSG_…_016` | Chỉ được chỉnh sửa chứng từ chưa ghi sổ | UC_ChinhSua không trích mã này (chỉ nói "không cho sửa") |
| `MSG_…_018` | Tiền chiết khấu không được vượt quá thành tiền | trùng vai trò `_044`; BR12 dùng `_044` |
| `MSG_…_019` | % Chiết khấu phải từ 0 đến 100 | trùng vai trò `_043` |
| `MSG_…_027` `_028` | Vui lòng chọn phiếu xuất kho / hóa đơn | thuộc luồng lập từ nguồn — không BR nào của epic này dùng |
| `MSG_…_029` `_030` `_031` `_032` `_033` `_034` | PXK/HĐ/chứng từ đã sử dụng · không tìm thấy | luồng "lập CTBH từ PXK/HĐ" (PMKT-U-06462/06463) **không có UC trong package** |
| `MSG_…_037` `_038` `_039` | Mã KH / hàng hóa / kho không tồn tại | không BR nào khai điều kiện phát sinh |
| `MSG_…_104` `_105` `_106` | cảnh báo xóa · đang sửa · số chứng từ đã ghi sổ | `_105` ngụ ý **khóa lạc quan khi sửa** nhưng không BR nào mô tả cơ chế |
| `MSG_…_110` | SL nhập > SL còn lại của Đơn đặt hàng nguồn | luồng lập từ Đơn đặt hàng — ngoài phạm vi package |
| `MSG_…_203` | Không có dữ liệu phân bổ chiết khấu | popup PBCK không nhắc mã này |

**Ngược lại — mã được dùng mà KHÔNG tồn tại:** `MSG_PMKT-E-06194_109` được tham chiếu tại
`SCR_CTBH_ThemMoi.md:1013` và `:1303` (chặn lưu khi toàn bộ dòng là Dịch vụ mà vẫn tích Kiêm phiếu
xuất kho) nhưng **không có trong `6.messages.md`** → mở `C10`.

---

## §5. Phát biểu không kiểm được

Không quy được về `WHEN … THEN …`, đã bỏ khỏi `02-rules.md`:

| Nguồn | Phát biểu | Vì sao |
|---|---|---|
| `SCR_CTBH_DanhSach.md:136` | "Chứng từ chưa ghi sổ được highlight lên" | không nói highlight bằng gì (màu / đậm / nền) |
| `SCR_CTBH_ThemMoi.md:351` | "Hiển thị thêm đuôi theo cách đọc tiền đã cấu hình của tenant" | không nói cấu hình nào, giá trị nào |
| `SCR_CTBH_ThemMoi.md:970` | "Không dùng Disable cho nhóm cột này" | là lý do thiết kế, luật thật đã có ở `R-CTBH-035` |
| `UC_CTBH_GhiSo.md:20` | "Quy tắc thao tác thực hiện theo quy tắc nghiệp vụ của màn hình thêm mới" | con trỏ, không phải luật |

---

## §6. AD đơn giản hoá — KHÔNG phải mâu thuẫn, nhưng không được code theo

| File | Thiếu gì so với BR/UC | Chốt theo |
|---|---|---|
| `AD_CTBH_ChinhSua.puml:53` | vẽ `Cập nhật trạng thái = "Đã ghi sổ"` thẳng, không đi qua `UC_CTBH_GhiSo` (không sinh bút toán, không ghi Sổ cái) | `UC_CTBH_ChinhSua.md:20` + BR21 |
| `AD_CTBH_ThemMoi.puml` | không vẽ ranh giới transaction / rollback toàn bộ khi một bước lỗi | `UC_CTBH_ThemMoi.md:34,95` (`R-CTBH-074`) |
| `AD_CTBH_ThemMoi.puml:83` | "Trạng thái thanh toán = Đã thanh toán" ngay ở nhánh Lưu-và-ghi-sổ | khớp BR22 mục 2 (ghi sổ phiếu thu) — không lệch |
| `AD_CTBH_Xoa.puml:71` | vòng lặp xóa mềm không mô tả xử lý chứng từ con | BR18 mục 6 + `C05` |

> `AD_CTBH_ThemMoi.puml:38,43` **đã** dẫn chiếu `BR23 mục 4` → sơ đồ đã được cập nhật khớp BR, không
> còn lệch như các bản trước.

---

## §7. BR chung đã đối chiếu

| BR | Áp ở luật | Epic có lệch không |
|---|---|---|
| BR2 (hiển thị & sắp xếp danh sách) | `R-CTBH-002`, `R-CTBH-005` | không |
| BR3 (popup) | `R-CTBH-084` | không |
| BR5 · BR6 (combogrid, trường tự do) | `R-CTBH-022`, `R-CTBH-039` | không |
| BR7 (làm tròn & precision) | `R-CTBH-046`, `R-CTBH-072` | không |
| BR8 (ngày tháng / kỳ) | `R-CTBH-029` | không |
| BR13.1 (màn danh sách) | `R-CTBH-008…014` | không |
| BR17 chung (kiểm tra kỳ kế toán) | `R-CTBH-092` | **epic im lặng** — BR chung áp đầy đủ; xem `C11` (thiếu quy định) |
| BR18 chung (chuyển đổi ngoại tệ) | `R-CTBH-047`, `R-CTBH-071` | không |
| BR20 chung (số chứng từ) | `R-CTBH-030`, `R-CTBH-067` | không |
| BR25 chung (quyền) | `R-CTBH-001`, `R-CTBH-015`, `R-CTBH-083` | không |
| BR28 chung (multi-tenant) | `R-CTBH-070` | không |
| BR29 chung (chính sách xóa) | `R-CTBH-089` | không |
| BR31 chung (dòng tổng) | `R-CTBH-013`, `R-CTBH-053` | không |
| BR41 chung (tham chiếu chéo) | `R-CTBH-088` | không |
| BR45 chung (thao tác hàng loạt) | `R-CTBH-086`, `R-CTBH-096` | **UC_CTBH_Xoa lệch** — xem `C01` |
