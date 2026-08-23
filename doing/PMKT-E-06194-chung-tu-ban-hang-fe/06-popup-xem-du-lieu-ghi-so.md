# 06 — Popup Xem dữ liệu ghi sổ (MỚI — F11 / D7)

> **Khác các file con trước**: màn này **0% code**, đây là plan xây MỚI, không phải đối chiếu.

## 1. Header

- **Mã màn**: SCR_CTBH_XemDuLieuGhiSo
- **SCR nguồn**: `5.screens/SCR_CTBH_XemDuLieuGhiSo.md` (155 dòng)
- **UC nguồn**: không có UC riêng — con của UC_CTBH_ThemMoi, UC_CTBH_ChinhSua, UC_CTBH_XemChiTiet
- **Node Figma**: không có (SCR ghi `[]` ở mục Nguyên mẫu) — **đặc tả UI suy ra từ SCR, phải review lại khi có design**
- **Điểm gọi**: nút "Xem dữ liệu ghi sổ" ở footer của `ChungTuBanHangThemMoiModal.tsx` (cả 3 mode: create/edit/view) — luôn hiển thị, không có mã quyền riêng (kế thừa quyền màn gọi)
- **File dự kiến**: `client/src/features/banHang/chungTuBanHang/components/modal/XemDuLieuGhiSoModal.tsx` (mới — đặt ở `components/modal/` theo Luật cứng 4, xem `00-ke-hoach-tong.md` §4)

## 2. Bố cục

Modal chỉ xem, 1 lưới bút toán (2 dòng đối ứng liền nhau mỗi bút toán, không gộp) + dòng tổng (Tổng PS Nợ, Tổng PS Có, luôn bằng nhau) + phân trang riêng (50/100/200) + nút Đóng duy nhất.

## 3. Đặc tả UI từ Figma

Không có Figma — suy ra hoàn toàn từ SCR. Cấu trúc lưới: 13 cột theo bảng §5. Không đoán kích thước/màu sắc — để dev tự áp style chuẩn `CommonListTable`/`CommonEditableGrid` (`@base`) khi code, không tự bịa số đo ở đây.

## 4. Ma trận ẩn/hiện · required · disabled

Không có file Matrix. BR01/BR02 của SCR đóng vai trò ma trận:

| Thành phần | Điều kiện |
|---|---|
| Nút "Xem dữ liệu ghi sổ" (điểm gọi) | Luôn hiện ở ThemMoi/CapNhat/XemChiTiet — KHÔNG hiện ở Hóa đơn bán hàng (PMKT-E-06196, ngoài phạm vi module này) |
| Chế độ dữ liệu | `Chưa ghi sổ` (kể cả chưa Lưu lần nào) → "Xem trước" (tính tại chỗ); `Đã ghi sổ` → "Dữ liệu sổ" (đọc `acc_so_cai`, **không tính lại**) |
| Nút "Đóng" | Luôn hiện — nút duy nhất |

## 5. Bảng cột / trường

| Cột | Chế độ Dữ liệu sổ (field) | Chế độ Xem trước (nguồn) | Kiểu |
|---|---|---|---|
| STT | — | tự tăng | number |
| Ngày hạch toán | `acc_so_cai.NgayHachToan` | `NgayHachToan` chứng từ sinh bút toán | date |
| Ngày chứng từ | `acc_so_cai.NgayChungTu` | idem | date |
| Số chứng từ | `acc_so_cai.SoChungTu` | idem (trống nếu chưa Lưu — BR04) | text |
| Mã đối tượng | `acc_so_cai.DoiTuongId → mst_doi_tuong.Code` | `sal_chung_tu_ban.KhachHangId → Code` | text |
| Tên đối tượng | `acc_so_cai.TenDoiTuong` | `sal_chung_tu_ban.TenKhachHang` | text |
| Diễn giải | `DienGiaiDong`; trống → `DienGiai` | tương ứng dòng chi tiết/chứng từ | text |
| Tài khoản | `acc_so_cai.TK` | TK người dùng chọn trên dòng | text |
| Tài khoản đối ứng | `acc_so_cai.TKDoiUng` | idem | text |
| Phát sinh nợ | `acc_so_cai.PSNoQuyDoi` | theo bảng bút toán BR20; vế Có = 0 | currency |
| Phát sinh có | `acc_so_cai.PSCoQuyDoi` | theo bảng bút toán BR20; vế Nợ = 0 | currency |
| Vụ việc | `acc_so_cai.VuViecId → Code` | `sal_chung_tu_ban_chi_tiet.VuViecId → Code` | text |
| Khoản mục chi phí | `acc_so_cai.KhoanMucChiPhiId → Code` | idem | text |
| Đối tượng THCP | `acc_so_cai.DoiTuongTapHopChiPhiId → Code` | idem | text |
| Đơn vị | `acc_so_cai.DonViId → Code` | idem | text |

Với phiếu xuất kho/phiếu thu kiêm trong nhóm: nguồn "Xem trước" đổi theo bảng bổ sung ở SCR dòng 60-67 (không lặp lại ở đây — trỏ nguyên văn).

## 6. Hành vi & sự kiện

- **Mở popup**: đọc `values` hiện tại của form cha (mode create/edit) hoặc dữ liệu đã load (mode view). Không gọi API — mọi tính toán ở FE.
- **Chọn chế độ**: `trangThaiChungTu === TRANG_THAI_CHUNG_TU.daGhiSo ? 'du-lieu-so' : 'xem-truoc'`.
  - Chế độ "Dữ liệu sổ": **NGOÀI PHẠM VI FE build tại đây** nếu chưa có endpoint đọc `acc_so_cai` theo nhóm chứng từ — cần xác nhận với BE (xem Q ở dưới). Nếu BE đã có endpoint (thường đi kèm plan BE của epic Sổ cái/Hạch toán), map thẳng response.
  - Chế độ "Xem trước": tính tại chỗ, tái dùng **nguyên** kết quả `helpers/hachToan.ts` đã tính cho `TongHopPanel` (không viết công thức bút toán thứ hai — R2 ở `00-ke-hoach-tong.md`).
- **Đóng**: không tác động dữ liệu form cha.
- **Không có dữ liệu**: hiển thị `CommonEmpty` (`@base`) kèm text "Không có dữ liệu".

## 7. Validation phía FE

Không có — form chỉ xem, không chặn, không hiển thị lỗi validate (BR04: "Form không chặn, mọi validate thực hiện tại nút Lưu/Lưu và ghi sổ của màn gọi").

## 8. Luồng xử lý

1. User bấm "Xem dữ liệu ghi sổ" ở form cha.
2. Component xác định chế độ theo `trangThaiChungTu` của chứng từ.
3. **Xem trước**: gọi hàm thuần (helpers) build danh sách dòng bút toán từ `values` hiện tại — KHÔNG gọi API, KHÔNG sinh `Id`/`ChungTuId`.
4. **Dữ liệu sổ**: gọi API đọc `acc_so_cai` theo nhóm chứng từ (endpoint cần Q bên dưới) — nếu chưa có endpoint, hiển thị trạng thái "đang phát triển" cho nhánh này, KHÔNG giả lập dữ liệu.
5. Hiển thị lưới + dòng tổng (Σ PS Nợ = Σ PS Có, kiểm tra bằng test).
6. Đóng.

## 9. Phân bổ file (dự kiến — mới hoàn toàn)

| Việc | File |
|---|---|
| Component popup | `components/modal/XemDuLieuGhiSoModal.tsx` |
| Hàm build dòng "Xem trước" (thuần) | `helpers/xemDuLieuGhiSo.ts` (mới) — tái dùng `helpers/hachToan.ts`, không viết công thức mới |
| Kiểu dữ liệu | `fields/types.ts` (thêm `DongButToanGhiSo`) |
| Cột lưới | `fields/xemDuLieuGhiSoColumns.ts` (mới, theo pattern `chiTietColumns.ts`) |
| API đọc `acc_so_cai` (nếu BE đã có) | `api/xemDuLieuGhiSoApi.ts` (mới) |
| Nhãn | `i18n/vi.ts`, `i18n/en.ts` (nhánh `xemDuLieuGhiSo.*`) |

## 10. Kiểm thử

| Case | Input → kỳ vọng | Loại |
|---|---|---|
| Xem trước — tổng PS Nợ = tổng PS Có | `values` hợp lệ với thuế + chiết khấu → 2 tổng bằng nhau | `helpers/xemDuLieuGhiSo.test.ts`, `node` |
| Xem trước — dòng chưa chọn đủ TK không sinh bút toán | dòng thiếu `taiKhoanDoanhThuId` → bút toán tương ứng không xuất hiện trong kết quả, các bút toán khác vẫn có | idem, `node` |
| Xem trước — chưa nhập số chứng từ | `values.soChungTu` rỗng → cột "Số chứng từ" trả `undefined`/rỗng, không throw | idem, `node` |
| Chế độ chọn đúng theo trạng thái | `trangThaiChungTu = 'DA_GHI_SO'` → chế độ "Dữ liệu sổ"; `'CHUA_GHI_SO'` → "Xem trước" | idem, `node` |
| Render — nút Đóng luôn có, không có nút khác | render modal → chỉ 1 nút | `components/modal/*.render.test.tsx`, jsdom |

## 11. BR đã áp dụng

`BR01` (điều kiện hiện nút) · `BR02` (2 chế độ dữ liệu) · `BR03` (phạm vi nhóm chứng từ liên kết) · `BR04` (dữ liệu chưa đủ ở Xem trước) · `BR05` (thứ tự sắp xếp) · `BR20` của SCR_CTBH_ThemMoi (nguồn công thức bút toán, tái dùng `helpers/hachToan.ts`).

## 12. Điểm cần BA/BE xác nhận (bổ sung — chỉ riêng file con này)

| # | Câu hỏi |
|---|---|
| Q7 | Đã có endpoint BE đọc `acc_so_cai` theo nhóm chứng từ (chế độ "Dữ liệu sổ") chưa? Nếu chưa, chế độ này của popup chỉ dựng UI + trạng thái "đang phát triển" ở đợt này, giống cách `ChungTuBanHangTab.tsx` đang xử lý "Thu tiền"/"Lập hóa đơn". |
| Q8 | `helpers/hachToan.ts` hiện tính cho `TongHopPanel` (tổng hợp số tiền) — có đủ chi tiết theo TỪNG DÒNG bút toán (STTButToan 1→5 theo BR20) để tái dùng cho lưới "Xem trước", hay cần một hàm tổng hợp mới đọc cùng input nhưng xuất khác hình dạng? Cần dev đọc `helpers/hachToan.ts` trước khi ước lượng lại effort D7 — **chưa đọc file này ở lượt research của plan-fe, vì ngoài 2 commit đang đối chiếu**; đây là việc đầu tiên khi bắt tay code D7.
