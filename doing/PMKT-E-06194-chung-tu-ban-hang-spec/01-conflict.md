# PMKT-E-06194 Chứng từ bán hàng — Sổ mâu thuẫn tài liệu

| | |
|---|---|
| Commit tài liệu | `8cf9606ea` |
| Ngày soát | 2026-08-28 |
| Tổng | **11** mục — 7 `OPEN` (5 P0 · 2 P1) · 3 `CLOSED-AUTO` · 1 `OPEN` (P0, thiếu quy định) |

---

## Bảng tổng

| ID | Chủ đề | Sev | Trạng thái | Luật bị chặn | Chốt ngày |
|---|---|---|---|---|---|
| **C01** | Xóa hàng loạt: chặn cả lô hay bỏ qua bản ghi lỗi | **P0** | **OPEN** | `R-CTBH-086` `R-CTBH-087` | — |
| **C02** | Mã message khi chặn xóa: `_014` hay `_111` | **P1** | **OPEN** | `R-CTBH-088` | — |
| **C03** | Định nghĩa "đã sử dụng ở nghiệp vụ khác" | **P0** | **OPEN** | `R-CTBH-088` | — |
| **C04** | Counter > 0 chặn xóa ⇒ mọi chứng từ kiêm không xóa được | **P0** | **OPEN** | `R-CTBH-088` `R-CTBH-090` | — |
| **C05** | Xóa CTBH có hóa đơn lập kèm: chặn hay xóa kèm | **P0** | **OPEN** | `R-CTBH-089` | — |
| **C06** | Sửa chứng từ đã phát sinh liên kết | **P0** | **OPEN** | `R-CTBH-078` `R-CTBH-081` | — |
| **C07** | Nút "Lập phiếu xuất kho" trên màn Xem chi tiết | **P1** | **OPEN** | `R-CTBH-019` | — |
| **C08** | Cột CK theo mặt hàng / hóa đơn: readonly hay nhập tay | **P1** | `CLOSED-AUTO` | — | 2026-08-28 |
| **C09** | "Tỷ lệ phân bổ" ở phương thức Thủ công: có nhập được không | **P1** | `CLOSED-AUTO` | — | 2026-08-28 |
| **C10** | `MSG_PMKT-E-06194_109` được dùng nhưng không tồn tại | **P1** | **OPEN** | `R-CTBH-036` | — |
| **C11** | Kỳ kế toán đã khóa — epic không quy định | **P0** | `CLOSED-AUTO` | — | 2026-08-28 |

> Bốn trạng thái: `OPEN` · `CLOSED-AUTO` (tự chốt theo thang thẩm quyền) · `CLOSED-BA` (bắt buộc có
> tên người + ngày) · `HUỶ`. **`CLOSED-BA` thiếu tên hoặc ngày thì `/gen-be` · `/gen-fe` coi như `OPEN`.**

---

## C01 · Xóa hàng loạt khi có chứng từ không đủ điều kiện — **P0 · OPEN**

**Nguồn A** — `business_rules.md` BR45 mục 2 (bậc 5) + `SCR_CTBH_PopupXacNhanXoa.md:38-43` (BR02, bậc 4)
+ `SCR_CTBH_DanhSach.md:81` (bậc 4):

> BR45: *"Hệ thống **bỏ qua** các bản ghi lỗi và vẫn thực hiện cho các bản ghi hợp lệ. Sau khi xử lý
> xong, hệ thống hiển thị một **Popup thông báo chi tiết kết quả**"*
> SCR popup BR02: *"Nút **Xóa hàng loạt** **không disable** theo trạng thái của các dòng đang chọn."*

**Nguồn B** — `UC_CTBH_Xoa.md:11` (AC1) + `:86-89` (bậc 3), củng cố bởi `AD_CTBH_Xoa.puml:48,55,62` (bậc 1):

> *"Nút "Xóa hàng loạt" bị disable nếu có ít nhất 1 chứng từ đã ghi sổ hoặc đã sử dụng ở nghiệp vụ khác"*
> *"Nút chỉ enable khi TẤT CẢ các chứng từ được chọn đều thỏa mãn … Nếu có ít nhất 1 chứng từ không
> thỏa mãn → disable nút"*

**Vì sao không tự chốt:** chủ đề thuộc **P0** (vòng đời chứng từ + chính sách transaction). Cán cân
nghiêng rõ về A (BR chung bậc 5 + 2 nguồn bậc 4 so với 1 nguồn bậc 3), nhưng luật cấm tự chốt P0.

**CÂU HỎI:** Người dùng chọn 5 chứng từ, trong đó 2 chứng từ đã ghi sổ. Hệ thống làm gì?

| | Phương án | Hệ quả lên code |
|---|---|---|
| **A** *(khuyến nghị — khớp BR45)* | Xóa 3 chứng từ hợp lệ, hiện popup "Xóa thành công 3 / Không xóa được 2" kèm bảng lý do | API `POST /xoa-hang-loat` trả `200` + danh sách kết quả từng dòng; transaction **theo từng chứng từ**; FE **không** disable nút, render popup kết quả theo BR45 mục 3 |
| **B** | Chặn cả 5, không xóa gì | API trả `400`; transaction **một lần cho cả lô**; FE disable nút khi có ≥1 dòng không hợp lệ |

**Luật bị chặn:** `R-CTBH-086`, `R-CTBH-087`.

---

## C02 · Mã message khi chặn xóa chứng từ đã sử dụng — **P1 · OPEN**

**Nguồn A** — `SCR_CTBH_PopupXacNhanXoa.md:27,50` + `SCR_CTBH_DanhSach.md:64` (cùng bậc 4):
`MSG_PMKT-E-06194_111` — *"Chứng từ đã được sử dụng trong nghiệp vụ khác, không thể xóa"*

**Nguồn B** — `SCR_CTBH_ThemMoi.md:1552` (BR23 mục 9, **cũng bậc 4**) + `UC_CTBH_Xoa.md:71` (bậc 3):
`MSG_PMKT-E-06194_014` — *"Chứng từ đã được sử dụng, không thể xóa"*

**Vì sao không tự chốt:** hai nguồn **cùng bậc 4**. `6.messages.md` (bậc 5) có **cả hai mã** và cả hai
đều mô tả đúng tình huống — mô tả của `_111` ghi *"BR04 màn Xác nhận xóa"*, của `_014` ghi *"Chứng từ
đã liên kết"*. Thẩm quyền bậc 5 không phân giải được.

**CÂU HỎI:** Khi chặn xóa vì chứng từ đã phát sinh liên kết, hệ thống trả mã nào?

| | Phương án | Hệ quả lên code |
|---|---|---|
| **A** | Dùng `_111` cho mọi trường hợp; `_014` thành mã chết | BE trả `messageId = MSG_PMKT-E-06194_111`; FE khai 1 key i18n; BA xóa `_014` khỏi `6.messages.md` |
| **B** | `_014` cho liên kết cứng (hóa đơn/PXK/phiếu thu), `_111` cho counter > 0 | BE phân nhánh 2 mã theo nguyên nhân; FE khai 2 key; phải định nghĩa rõ ranh giới hai nhóm |

**Luật bị chặn:** `R-CTBH-088`.

---

## C03 · Định nghĩa "đã sử dụng ở nghiệp vụ khác" — **P0 · OPEN**

**Nguồn A** — `SCR_CTBH_PopupXacNhanXoa.md:52-64` (BR04, bậc 4) — bảng hai cột **rất cụ thể**:

| Chặn xóa | KHÔNG chặn xóa |
|---|---|
| Đã lập hóa đơn (`sal_hoa_don_ban_hang.ChungTuBanId`) | **Phiếu xuất kho / phiếu thu kiêm** (`cash_phieu_thu_chi_tiet.ChungTuBanId` ≠ NULL) |
| Phiếu xuất kho **thủ công** (`inv_phieu_xuat_kho.NguonId`) | Tham chiếu **mềm** ở tab Tham chiếu (BR41) |
| Phiếu thu / giấy báo có **Thu tiền theo hóa đơn** (`cash_chung_tu_cong_no_phieu_thu.ChungTuBanId`) | |
| Trả lại hàng bán · điều chỉnh giá hàng bán | |
| Counter `SoLuongDaXuatHoaDon` hoặc `SoLuongDaXuatKho` > 0 | |

**Nguồn B** — `UC_CTBH_Xoa.md:96-103` (bậc 3):

> *"Chứng từ đã được sử dụng khi: **Đã tạo phiếu thu từ chứng từ này**; Đã được tham chiếu bởi chứng
> từ khác"*

**Vì sao không tự chốt:** chênh 1 bậc **và** chủ đề P0. UC nói "đã tạo phiếu thu" **không phân biệt
kiêm với lập riêng**, trong khi SCR nói phiếu thu **kiêm không chặn** — hai cách hiểu cho ra kết quả
ngược nhau trên chính chứng từ có `ThuTienNgay = True`, tức phần lớn chứng từ thu tiền mặt.

**CÂU HỎI:** Chứng từ bán có `ThuTienNgay = True` (đã sinh phiếu thu kiêm), chưa ghi sổ. Xóa được không?

| | Phương án | Hệ quả lên code |
|---|---|---|
| **A** *(khuyến nghị — theo bậc cao hơn)* | Xóa được; phiếu thu kiêm bị xóa mềm theo | `DeletePolicy` chỉ chặn theo đúng 5 dòng cột trái của BR04; phiếu kiêm nằm trong nhánh cascade |
| **B** | Không xóa được | mọi chứng từ thu tiền ngay trở thành không xóa được — mâu thuẫn tiếp với BR18 mục 6 (*"Xóa chứng từ bán → xóa cùng các phiếu liên kết"*) |

**Luật bị chặn:** `R-CTBH-088`.

---

## C04 · Counter > 0 chặn xóa ⇒ chứng từ kiêm không bao giờ xóa được — **P0 · OPEN**

Đây là mâu thuẫn **nội bộ giữa hai BR cùng bậc 4**, và là mâu thuẫn nguy hiểm nhất của package: nó
làm **vô hiệu hóa chức năng Xóa** cho phần lớn chứng từ.

**Nguồn A** — `SCR_CTBH_PopupXacNhanXoa.md:62` (BR04):

> *"Counter `SoLuongDaXuatHoaDon` hoặc `SoLuongDaXuatKho` > 0 (**BR23**)"* → **chặn xóa**

**Nguồn B** — `SCR_CTBH_ThemMoi.md:1481-1485` (BR23 mục 4):

> *"Khi **lưu** CTBH lần đầu, với **mỗi dòng hàng**: `LapKemHoaDon = True` → `SoLuongDaXuatHoaDon =
> SoLuong` … `KiemPhieuXuatKho = True` → `SoLuongDaXuatKho = SoLuong`"*

**Hệ quả logic:** checkbox `Kiêm phiếu xuất kho` và `Lập kèm hóa đơn` đều **mặc định Checked**
(`SCR_CTBH_ThemMoi.md:28,29`) → mọi chứng từ lập theo mặc định đều có counter > 0 ngay khi Lưu →
theo A thì **không chứng từ nào xóa được**, kể cả khi chưa ghi sổ và chưa phát sinh chứng từ lập riêng.
Điều này mâu thuẫn trực tiếp với chính BR04 cột phải (*"phiếu kiêm — không chặn xóa"*) và với
`SCR_CTBH_ThemMoi.md:1552` (BR23 mục 9: *"Chỉ cho xóa khi CTBH chưa phát sinh hóa đơn / phiếu xuất kho
**lập riêng** liên kết"* — tức chỉ xét **lập riêng**).

**Vì sao không tự chốt:** ba nguồn cùng bậc 4; chủ đề P0.

**CÂU HỎI:** Điều kiện chặn xóa theo counter phải hiểu thế nào?

| | Phương án | Hệ quả lên code |
|---|---|---|
| **A** *(khuyến nghị — khớp BR23 mục 9)* | Chỉ chặn khi counter **được cộng bởi chứng từ lập riêng**, tức tồn tại dòng hóa đơn / PXK có `ChiTietChungTuBanId` trỏ tới. Counter do khởi tạo lúc lưu (BR23 mục 4) **không** chặn | `DeletePolicy` kiểm **sự tồn tại bản ghi liên kết lập riêng**, không kiểm giá trị counter |
| **B** | Chặn theo đúng chữ: counter > 0 là chặn | Cần đổi mặc định 2 checkbox thành Unchecked, nếu không chức năng Xóa vô dụng |
| **C** | Tách counter thành 2 phần: khởi tạo và lũy kế từ chứng từ lập riêng | thêm 2 cột DB `SoLuongDaXuatHoaDonLapRieng` / `…KhoLapRieng`; ảnh hưởng BR22, BR23 mục 5–7 |

**Luật bị chặn:** `R-CTBH-088`, `R-CTBH-090`.

---

## C05 · Xóa CTBH có hóa đơn lập kèm — **P0 · OPEN**

Mâu thuẫn **trong cùng một file**, giữa hai BR liền nhau.

**Nguồn A** — `SCR_CTBH_PopupXacNhanXoa.md:58` (BR04, cột "Chặn xóa"):

> *"Đã lập **hóa đơn** từ chứng từ này (`sal_hoa_don_ban_hang.ChungTuBanId`)"* → **chặn xóa**

**Nguồn B** — `SCR_CTBH_PopupXacNhanXoa.md:69` (BR05, cùng file):

> *"Xóa chứng từ bán thì **xóa cùng** các phiếu kiêm sinh tự động là phiếu xuất kho, phiếu thu **và
> hóa đơn lập kèm nếu có**"*

Hóa đơn lập kèm (`LapKemHoaDon = True`) **cũng** mang `sal_hoa_don_ban_hang.ChungTuBanId`
(`SCR_CTBH_ThemMoi.md:1003`) → thỏa điều kiện chặn của BR04, nhưng BR05 lại bảo xóa kèm.

Nguồn thứ ba làm phức tạp thêm: `SCR_CTBH_ThemMoi.md:1069` (BR18 mục 8) — *"Hóa đơn **vẫn là chứng từ
độc lập** vì mang giá trị pháp lý riêng … có vòng đời riêng"*; và `:1052` (BR18 mục 6) chỉ nói xóa kèm
*"các phiếu liên kết sinh tự động"*, không nhắc hóa đơn. `UC_CTBH_Xoa.md:108` (bậc 3) thì liệt kê cả
`HoaDonBanHang` vào nhánh xóa mềm theo.

**Vì sao không tự chốt:** cùng bậc 4, cùng file, chủ đề P0 (vòng đời chứng từ có giá trị pháp lý).

**CÂU HỎI:** Chứng từ bán chưa ghi sổ, `LapKemHoaDon = True` đã sinh hóa đơn số HĐ001. Bấm Xóa thì sao?

| | Phương án | Hệ quả lên code |
|---|---|---|
| **A** | Chặn xóa, yêu cầu xóa hóa đơn trước | `DeletePolicy` chặn theo `sal_hoa_don_ban_hang.ChungTuBanId`; hóa đơn phải xóa được độc lập |
| **B** | Xóa CTBH và xóa mềm hóa đơn theo | cascade sang module hóa đơn (PMKT-E-06196); **rủi ro pháp lý** nếu hóa đơn đã phát hành |
| **C** *(khuyến nghị — dung hòa BR18 mục 8)* | Xóa kèm **nếu hóa đơn chưa phát hành**; chặn nếu đã phát hành | cần trường trạng thái phát hành của hóa đơn — **BA phải xác nhận trường này tồn tại** ở PMKT-E-06196 |

**Luật bị chặn:** `R-CTBH-089`.

---

## C06 · Sửa chứng từ đã phát sinh liên kết — **P0 · OPEN**

**Nguồn A** — `UC_CTBH_ChinhSua.md:9` (AC1, bậc 3):

> *"Chứng từ **đã được sử dụng ở nghiệp vụ khác** hoặc đã ghi sổ: **không cho phép sửa**."*

**Nguồn B** — `SCR_CTBH_ThemMoi.md:1554` (BR23 mục 9, bậc 4):

> *"**CTBH bị bỏ ghi sổ:** Cho phép sửa lại `SoLuong`, nhưng phải đảm bảo cho **từng dòng**:
> `SoLuong_moi ≥ MAX(SoLuongDaXuatHoaDon, SoLuongDaXuatKho)`"*

B mặc nhiên cho sửa chứng từ **đã có counter > 0**, tức đã phát sinh hóa đơn / PXK — đúng thứ A cấm.

**Vì sao không tự chốt:** chênh 1 bậc, chủ đề P0.

**CÂU HỎI:** Chứng từ đã lập hóa đơn một phần (5/10), sau đó bỏ ghi sổ. Có sửa được không?

| | Phương án | Hệ quả lên code |
|---|---|---|
| **A** *(khuyến nghị — theo bậc cao hơn)* | Sửa được, chặn ở mức trường: `SoLuong_moi ≥ MAX(counter)` từng dòng, báo `MSG_…_102`/`_103` | validator mức dòng khi Lưu bản sửa; nút Sửa hiện bình thường |
| **B** | Không sửa được, ẩn nút Sửa | `EditPolicy` chặn ở mức chứng từ; BR23 mục 9 thành luật chết |

**Luật bị chặn:** `R-CTBH-078`, `R-CTBH-081`.

---

## C07 · Nút "Lập phiếu xuất kho" trên màn Xem chi tiết — **P1 · OPEN**

**Nguồn A** — `SCR_CTBH_ThemMoi.md:1520` (BR23 mục 6.1, bậc 4):

> *"Khi người dùng bấm "Lập phiếu xuất kho" từ **SCR_CTBH_DanhSach** hoặc **SCR_CTBH_XemChiTiet**"*

**Nguồn B** — `SCR_CTBH_XemChiTiet.md:23-41` (bảng Chức năng + BR1, **cùng bậc 4**): chỉ liệt kê
**Chỉnh sửa · Ghi sổ · Bỏ ghi sổ · Lập hóa đơn · Xem dữ liệu ghi sổ · Đóng** — **không có** "Lập phiếu
xuất kho". `UC_CTBH_XemChiTiet.md:14,39-44` (bậc 3) cũng không có.

Chính BA đã ghi nhận mâu thuẫn này trong `Matrix/…/SCR_CTBH_XemChiTiet_MaTranAnHien.md:98` (bậc 0)
và để marker `(sl)`.

**Vì sao không tự chốt:** hai nguồn cùng bậc 4.

**CÂU HỎI:** Màn Xem chi tiết có nút "Lập phiếu xuất kho" không?

| | Phương án | Hệ quả lên code |
|---|---|---|
| **A** | Có — điều kiện giống màn Danh sách | FE thêm nút + điều kiện `TrangThaiXuatHang ∈ {Chưa xuất, Đã xuất một phần}` và loại chứng từ ≠ Bán dịch vụ |
| **B** | Không — chỉ lập từ màn Danh sách | FE giữ nguyên 6 nút; BA sửa BR23 mục 6.1 bỏ `SCR_CTBH_XemChiTiet` |

**Luật bị chặn:** `R-CTBH-019`.

---

## C08 · Cột CK theo mặt hàng / hóa đơn: readonly hay nhập tay — **P1 · `CLOSED-AUTO`**

**Nguồn A** — `SCR_CTBH_ThemMoi.md:219-224` (bảng trường): `Tỷ lệ CK theo mặt hàng (%)` ·
`Tiền CK theo mặt hàng` · `Tỷ lệ CK theo hóa đơn (%)` · `Tiền CK theo hóa đơn` đều ghi
**Cho phép sửa = N**.

**Nguồn B** — `SCR_CTBH_ThemMoi.md:747-758` (BR12.d Trường hợp 1): *"Người dùng nhập thủ công các
trường Tỷ lệ CK theo mặt hàng và Tỷ lệ CK theo hóa đơn"*, kèm công thức tính 2 chiều khi người dùng nhập.

**Tự chốt theo B.** Căn cứ: quy tắc miền — *công thức · điều kiện* thuộc thẩm quyền của mục `BRxx`,
còn bảng trường ở đầu màn là bảng liệt kê control. BR12.d mô tả **toàn bộ cơ chế tính 2 chiều phụ
thuộc thao tác nhập của người dùng**; nếu 4 cột này readonly thì Trường hợp 1 của BR12.d không có
đường kích hoạt và trở thành luật chết. Ngoài ra `SCR_CTBH_ThemMoi.md:762` khai riêng rằng **chỉ**
`Tiền CK` và `Tỷ lệ CK (%)` (cột tổng hợp) là disabled — tức 4 cột thành phần thì không.

**Chốt:** `Tỷ lệ CK theo mặt hàng (%)` và `Tỷ lệ CK theo hóa đơn (%)` **cho nhập tay**;
`Tiền CK theo mặt hàng` **cho nhập tay** (tính ngược ra tỷ lệ); `Tiền CK theo hóa đơn` cho nhập tay
hoặc nhận từ popup PBCK_MHHD. Ghi vào `R-CTBH-050`, `R-CTBH-051`.

> Đây là chốt kỹ thuật để không chặn code. BA nên xác nhận lại khi duyệt Matrix — điểm này đã được
> `Matrix/…/SCR_CTBH_ThemMoi_MaTranAnHien.md:130` nêu là "Điểm cần xác nhận #3".

---

## C09 · "Tỷ lệ phân bổ" ở phương thức Thủ công — **P1 · `CLOSED-AUTO`**

**Nguồn A** — `SCR_CTBH_PBCK.md:35` (bảng trường): `Tỷ lệ phân bổ` — Cho phép sửa = **N**.
**Nguồn B** — `SCR_CTBH_PBCK.md:58-64` (BR3 Phân bổ thủ công): *"Cột "Tiền CK phân bổ" và "Tỷ lệ phân
bổ" đều ở trạng thái **enabled**"*, kèm công thức tính 2 chiều.

**Tự chốt theo B** — cùng lý do C08: BR mô tả cơ chế, bảng trường mô tả mặc định. Ngoài ra BR3 nói rõ
"đều ở trạng thái enabled" — câu khẳng định trực tiếp về enable, mạnh hơn ô "N" của bảng.

**Chốt:** phương thức `Theo giá trị` / `Theo số lượng` → cả 2 cột **Disable**; phương thức `Thủ công`
→ cả 2 cột **enable**, tính 2 chiều. Ghi vào `R-CTBH-055`, `R-CTBH-056`. Áp cho cả `SCR_CTBH_PBCK_MHHD`.

---

## C10 · `MSG_PMKT-E-06194_109` không tồn tại — **P1 · OPEN**

`SCR_CTBH_ThemMoi.md:1013` và `:1303` đều chặn lưu với **`MSG_PMKT-E-06194_109`** cho tình huống
*"Toàn bộ dòng hàng là Dịch vụ mà vẫn tích Kiêm phiếu xuất kho"*. Mã này **không có** trong
`6.messages.md` (đã kiểm: file có `_108`, `_110`, `_111`, nhảy qua `_109`).

**Vì sao không tự chốt:** `6.messages.md` là **bậc 5 tuyệt đối** về nội dung thông báo — không được
tự đặt nội dung message. Đây là **thiếu quy định**, không phải mâu thuẫn.

**CÂU HỎI:** Nội dung nguyên văn của `MSG_PMKT-E-06194_109` là gì? (BA bổ sung vào `6.messages.md`.)
Gợi ý theo ngữ cảnh — *"Chứng từ chỉ gồm dòng hàng dịch vụ, không thể kiêm phiếu xuất kho"* — **cần BA
duyệt nguyên văn**, không code theo gợi ý này.

**Luật bị chặn:** `R-CTBH-036` (phần message; phần điều kiện chặn thì đã rõ, vẫn code được).

---

## C11 · Kỳ kế toán đã khóa — **P0 · `CLOSED-AUTO`**

Không tài liệu nào của epic nhắc tới kỳ kế toán đã khóa trong luồng Lưu / Ghi sổ / Bỏ ghi sổ / Xóa
của chứng từ bán hàng.

**Tự chốt theo BR chung.** Căn cứ: `business_rules.md` BR17 (kiểm tra kỳ kế toán) là **bậc 5** và áp
chung cho mọi chứng từ hạch toán; BR45 mục 2 còn nêu đích danh *"kỳ kế toán đã khóa — BR17"* là một
nguyên nhân bỏ qua bản ghi trong thao tác hàng loạt. Epic **im lặng** ⇒ theo quy tắc "epic không nhắc
BR không có nghĩa được bỏ qua BR", BR17 áp dụng đầy đủ.

**Chốt:** ghi sổ / bỏ ghi sổ / xóa chứng từ thuộc kỳ đã khóa đều bị chặn theo BR17 chung. Ghi vào
`R-CTBH-092`. Message dùng mã của BR17 chung (`MSG_PMKT-E-07528_026` — module Khóa sổ), **không** tự
đặt mã mới trong namespace `PMKT-E-06194`.
