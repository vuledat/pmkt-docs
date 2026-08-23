# 04 — Popup Phân bổ chiết khấu (PBCK · PBCK theo mặt hàng/hóa đơn)

## 1. Header

- **Mã màn**: SCR_CTBH_PBCK (Phân bổ theo tổng giá trị hóa đơn), SCR_CTBH_PBCK_MHHD (Phân bổ theo hóa đơn — dành cho "Theo mặt hàng và hóa đơn")
- **SCR nguồn**: `5.screens/SCR_CTBH_PBCK.md` (122 dòng), `5.screens/SCR_CTBH_PBCK_MHHD.md` (126 dòng)
- **UC nguồn**: con của UC_CTBH_ThemMoi/ChinhSua — mở từ `GridHeaderActions`
- **Node Figma**: `node-id=21370-356363` (PBCK) · `node-id=46357-87788` (PBCK_MHHD)
- **File chính**: `client/src/features/banHang/chungTuBanHang/components/PhanBoChietKhauModal.tsx` (231 dòng — MỘT file cho cả 2 biến thể)

## 2. Bố cục

Header (Số tiền, Phương thức phân bổ) → lưới chi tiết phân bổ → dòng tổng → nút Phân bổ / Áp dụng / Hủy. Không đổi từ bản 18/08.

## 3. Đặc tả UI từ Figma

Không đo lại — không có thay đổi UI từ 2 commit BA mới (0 dòng đổi trong `bb4c10eb9`/`beaf3662a` cho 2 file SCR này, xem `git show <commit> --stat` ở `00-ke-hoach-tong.md` §2).

## 4. Ma trận ẩn/hiện · required · disabled

Từ `Matrix/SCR_CTBH_PBCK_MaTranAnHien.md` (54 dòng) và `Matrix/SCR_CTBH_PBCK_MHHD_MaTranAnHien.md` (55 dòng) — chưa đọc chi tiết ở lượt rà này vì **0 thay đổi từ 2 commit** và không có gap nào được `00-doi-chieu-tai-lieu-code.md` (bản 18/08) hay code comment tự nhận. Xác nhận nhanh qua cấu trúc file: `PhanBoChietKhauModal.tsx` có 231 dòng, đủ để chứa cả header + lưới + dòng tổng + 3 nút của cả 2 biến thể (thân bài chia nhánh theo `loaiChietKhau`).

**Việc của đợt này**: chỉ xác nhận còn khớp, không đọc lại toàn bộ 2 file Matrix — nếu muốn review sâu hơn BR1–BR8 của từng popup, cần một lượt riêng (ngoài phạm vi 2 commit đang đối chiếu).

## 5. Bảng cột / trường

Không liệt kê lại — không đổi.

## 6. Hành vi & sự kiện

Không đổi. `helpers/chietKhau.ts` xử lý BR1 (theo giá trị), BR2 (theo số lượng), BR3 (thủ công 2 chiều), BR7 (làm tròn dòng cuối) — có test `test/chietKhau.test.ts`.

## 7. Validation phía FE

Không đổi — BR6 (MSG_044, _047, _048) đã có sẵn qua `helpers/chietKhau.ts` + `helpers/kiemTra.ts` (giả định theo tên file, chưa đọc chi tiết ở lượt này).

## 8. Luồng xử lý

Không đổi — tính toán tại chỗ trên form, không gọi API. Nút "Áp dụng" cập nhật lại lưới chi tiết hàng hóa của form cha theo BR8 của từng file SCR.

## 9. Phân bổ file

Không đổi — `components/PhanBoChietKhauModal.tsx`, `helpers/chietKhau.ts`.

## 10. Kiểm thử

Không thêm case mới ở đợt này — `test/chietKhau.test.ts` đã tồn tại. Nếu lượt review Matrix sâu hơn (ngoài phạm vi) phát hiện gap, bổ sung case riêng.

## 11. BR đã áp dụng

`BR1–BR8` của cả 2 file SCR — không đổi, xác nhận qua sự tồn tại của `helpers/chietKhau.ts` + test đi kèm, không đọc lại chi tiết.

**Ghi chú phạm vi**: file con này KHÔNG đại diện một lượt audit đầy đủ cho PBCK/PBCK_MHHD — chỉ xác nhận "không có gì đổi từ 2 commit đang đối chiếu". Muốn plan chi tiết (bảng field đầy đủ, ma trận dịch nguyên vẹn) cần yêu cầu riêng.
