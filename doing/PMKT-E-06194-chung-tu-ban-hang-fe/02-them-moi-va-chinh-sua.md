# 02 — Thêm mới / Chỉnh sửa Chứng từ bán hàng

## 1. Header

- **Mã màn**: SCR_CTBH_ThemMoi (khung chính), SCR_CTBH_CapNhat (chỉ nêu khác biệt — cùng component theo Luật cứng 2 `client/CLAUDE.md §5`)
- **SCR nguồn**: `5.screens/SCR_CTBH_ThemMoi.md` (1613 dòng), `5.screens/SCR_CTBH_CapNhat.md` (46 dòng)
- **UC nguồn**: UC_CTBH_ThemMoi, UC_CTBH_ChinhSua
- **Node Figma**: `node-id=14770-332806` (biến thể mặc định `14770-331827`) — trỏ từ code, không có trong tài liệu BA
- **Route**: mở qua popup từ `SCR_CTBH_DanhSach` (dropdown "Thêm mới" / nút "Sửa")
- **File chính**: `client/src/features/banHang/chungTuBanHang/components/ChungTuBanHangThemMoiModal.tsx` (~870+ dòng, đã build đầy đủ)

## 2. Bố cục

Không đổi so với hiện trạng — xem comment đầu file `ChungTuBanHangThemMoiModal.tsx:9-17`: Modal Header → hàng tùy chọn (Loại nghiệp vụ | Kiêm phiếu xuất kho · Lập kèm hóa đơn · Thu tiền ngay [· HTTT]) → thẻ "Nhập" (5 tab điều kiện) → thẻ lưới (4 tab: Chi tiết hàng hóa · Thuế · Hạch toán · Tham chiếu) → khối tổng → footer.

**D7 đổi footer**: `Hủy · Xem dữ liệu ghi sổ · Lưu · Lưu và ghi sổ` (thêm 1 nút — xem `06-popup-xem-du-lieu-ghi-so.md` §1 "Điểm gọi"). Nút "Xem dữ liệu ghi sổ" **luôn hiển thị**, không phụ thuộc trạng thái ghi sổ (BR01 của SCR_CTBH_XemDuLieuGhiSo).

## 3. Đặc tả UI từ Figma

Không đo lại — không có thay đổi layout từ 2 commit BA mới, chỉ đổi luật hiển thị/luật ghi sổ. D5 thêm 1 cột lưới ("Đơn đặt hàng") vào khối "Chiều phân tích" hiện có (STT/Đơn vị/Vụ việc/Khoản mục CP/Hợp đồng), giữ đúng style combogrid 96px đã dùng cho `hopDongId`.

## 4. Ma trận ẩn/hiện · required · disabled

Dịch từ `Matrix/SCR_CTBH_ThemMoi_MaTranAnHien.md` + `Matrix/SCR_CTBH_CapNhat_MaTranAnHien.md` — **không đổi từ bản 18/08** (2 commit BA mới không chạm ma trận này, chỉ chạm BR21/BR22 văn bản + mapping Sổ cái). Đối chiếu với code hiện có:

| Trục / điều kiện | Trạng thái code |
|---|---|
| I1 Loại nghiệp vụ (Trong nước / Xuất khẩu) — ẩn khối thuế XK ⇄ GTGT | ✅ `helpers/anHien.ts` (`nc.xuatKhau`) |
| I2 Thu tiền ngay + HTTT — tab Phiếu thu/Giấy báo có | ✅ `helpers/anHien.ts:67-88` |
| `(đk-PXK)` Kiêm phiếu xuất kho — tab + cột giá vốn | ✅ `helpers/anHien.ts:58-60`, `fields/chiTietFields.ts:573-596` |
| `(đk-HD)` Lập kèm hóa đơn — tab Hóa đơn + checkbox Đã lập hóa đơn | ✅ `helpers/anHien.ts:63-65` |
| `(đk-LT)` Loại tiền ≠ đồng tiền hạch toán — cột quy đổi | ✅ (không grep sâu lại — không đổi từ bản 18/08) |
| `(đk-CK)` Loại chiết khấu — ô %/nút Áp dụng/nút Phân bổ | ✅ `components/GridHeaderActions.tsx` |
| Điều kiện mức dòng (Dịch vụ, CKTM, KM, ĐVT≠chính, %GTGT=KHAC) | ✅ `helpers/anHien.ts:94-158` |

Cột mới D5 "Đơn đặt hàng": theo bảng field `SCR_CTBH_ThemMoi.md:261`, **không có điều kiện ẩn/hiện riêng** (luôn hiện, N required, Y editable) — cùng loại với `hopDongId` đã có, không cần thêm nhánh vào `NguCanhAnHien`.

## 5. Bảng cột / trường (chỉ phần thay đổi — D5)

| Tên hiển thị | Khoá i18n | Field API | Kiểu | Required | Editable | Trạng thái |
|---|---|---|---|---|---|---|
| Đơn đặt hàng | `themMoi.grid.donDatHang` | `sal_chung_tu_ban_chi_tiet.donDatHangId` | combogrid | N | Y | ❌ **F10 — thiếu, D5 thêm mới** |

Toàn bộ bảng field còn lại của lưới Chi tiết hàng hóa — **không đổi**, đã build đủ theo `fields/chiTietFields.ts` (không liệt kê lại, xem file cũ `00-doi-chieu-tai-lieu-code.md` §1 cho F4/F5 còn tồn).

## 6. Hành vi & sự kiện

### 6.1 — BR21/BR22 (không cần sửa code, chỉ xác nhận)

| Hành vi | Luật mới (BR21/BR22) | Code hiện tại | Kết luận |
|---|---|---|---|
| Nút "Lưu" | Lưu ở "Chưa ghi sổ", chạy đủ validate xuất kho | `toLuuChungTuBanHangBody(values, { ghiSo: false, ... })` — `ChungTuBanHangThemMoiModal.tsx:572` | ✅ khớp |
| Nút "Lưu và ghi sổ" | 1 request, cờ `ghiSo` | cùng dòng, `ghiSo: true` | ✅ khớp — `luuGhiSoField: 'ghiSo'` (`api/chungTuModule.tsx:147`) |
| Khóa sửa sau ghi sổ | Chứng từ "Đã ghi sổ" không sửa được, phải Bỏ ghi sổ trước | Nút "Sửa" trên danh sách ẩn khi `DA_GHI_SO` (kernel) | ✅ khớp (dù `PUT` chưa nối — F12, không phải lỗi luật) |
| Đồng bộ ghi sổ nhóm liên kết (BR21 mục 3) | Ghi sổ/Bỏ ghi sổ 1 chứng từ trong nhóm kiêm → cả nhóm | Xử lý hoàn toàn ở BE (transaction), FE chỉ gọi 1 endpoint | ✅ khớp — không có việc FE |

**Kết luận: mục 6.1 không có việc code nào cho FE** — toàn bộ BR21/BR22 mới đã đúng kiến trúc hiện tại (nhờ tách rạch ròi FE chỉ gọi API + hiển thị lỗi, không tự đoán luật chặn).

### 6.2 — D7 (nút "Xem dữ liệu ghi sổ")

- Thêm nút vào footer, `onClick` mở `XemDuLieuGhiSoModal` (component mới — xem `06-popup-xem-du-lieu-ghi-so.md`), truyền `values` hiện tại của form (chế độ Thêm mới/Sửa) hoặc dữ liệu đã load (chế độ Xem).
- Luôn enable, không phụ thuộc trạng thái ghi sổ hay `readOnly`.

### 6.3 — D5 (cột Đơn đặt hàng)

- Thêm dòng `chon('donDatHangId', 'donDatHang', 96, options.donDatHang)` vào `fields/chiTietFields.ts` (cạnh dòng 602 `hopDongId`).
- `hooks/useDanhMucThemMoi.ts`: thêm khoá `donDatHang: CommonSelectBoxOption[]`, khởi tạo `CHUA_CO_DANH_MUC` (giống `hopDong`) cho tới khi Q2 trả lời có endpoint.
- `api/formDetail.ts`: thêm `donDatHangId: chu(line.donDatHangId)` (đối xứng dòng 101 `hopDongId`).
- `api/payload.ts`: thêm `donDatHangId: line.donDatHangId ?? null` (đối xứng dòng 137 `hopDongId`).
- `fields/types.ts`: thêm `donDatHangId?: string` vào `ChungTuBanHangLine` (đối xứng dòng 98 `hopDongId`).

## 7. Validation phía FE

Không đổi cho D5/D7 — cả hai đều N required (D5) hoặc không phải input (D7 là popup chỉ xem). Validate còn lại (chiết khấu, trùng số chứng từ…) không đổi từ 2 commit BA mới.

## 8. Luồng xử lý

**D7 — mở popup Xem dữ liệu ghi sổ:**
1. User bấm nút "Xem dữ liệu ghi sổ".
2. Component đọc `values` (Form.useWatch toàn bộ hoặc `form.getFieldsValue()`), truyền vào `XemDuLieuGhiSoModal`.
3. Modal tính bút toán "Xem trước" theo BR20 (tái dùng `helpers/hachToan.ts` đã có — không viết công thức mới, xem R2 ở `00-ke-hoach-tong.md`).
4. Hiển thị lưới read-only, không gọi API.
5. Đóng modal — không tác động dữ liệu form đang mở.

## 9. Phân bổ file

| Việc | File |
|---|---|
| D5 — cột lưới | `fields/chiTietFields.ts`, `fields/types.ts` |
| D5 — danh mục | `hooks/useDanhMucThemMoi.ts` |
| D5 — map request/response | `api/formDetail.ts`, `api/payload.ts` |
| D5 — nhãn | `i18n/vi.ts`, `i18n/en.ts` (`themMoi.grid.donDatHang`) |
| D7 — nút footer | `components/ChungTuBanHangThemMoiModal.tsx` |
| D7 — popup mới | `components/modal/XemDuLieuGhiSoModal.tsx` (xem `06-popup-xem-du-lieu-ghi-so.md`) |

## 10. Kiểm thử

| Case | Input → kỳ vọng | Loại |
|---|---|---|
| D5 — payload gửi `donDatHangId` khi đã chọn | dòng có `donDatHangId = 'x'` → `toLuuChungTuBanHangBody(...).chiTiet[0].donDatHangId === 'x'` | `test/payload.test.ts`, `node` |
| D5 — payload gửi `null` khi chưa chọn | dòng không có `donDatHangId` → `.donDatHangId === null` | `test/payload.test.ts`, `node` |
| D5 — form nạp đúng khi Sửa/Xem | response có `donDatHangId` → `toFormValuesChiTiet(...).donDatHangId` khớp | `test/*.test.ts`, `node` |
| D7 — nút luôn hiện | `readOnly = true/false`, `trangThaiChungTu` bất kỳ → nút "Xem dữ liệu ghi sổ" luôn render | `test/chungTuBanHang.render.test.tsx`, jsdom |

## 11. BR đã áp dụng

`BR21` (mục 1, 2, 4 — xác nhận không cần sửa) · `BR22` (xác nhận không cần sửa) · `BR6 chung` (combogrid, D5) · `BR20` (nguồn tính Xem dữ liệu ghi sổ, D7) · SCR_CTBH_XemDuLieuGhiSo BR01 (điều kiện hiện nút, D7).

**BR chưa đạt**: `BR14` (F4, chặn BE) · `BR16` (F5, hoãn BA) — không đổi.
