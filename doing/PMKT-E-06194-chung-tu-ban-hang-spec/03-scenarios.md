# PMKT-E-06194 Chứng từ bán hàng — Kịch bản & trạng thái kỳ vọng

| | |
|---|---|
| Commit tài liệu | `8cf9606ea` |
| Ngày soát | 2026-08-28 |
| Tổng | **81 kịch bản** (`S-001…081`) |
| Phủ nhóm | happy 34 · biên 14 · ngoại lệ 21 · rollback 6 · tương tranh 6 |

> **File này là nguồn sự thật duy nhất để viết test.** Mỗi luật `P0` trong
> [`02-rules.md`](02-rules.md) có ít nhất một kịch bản ở đây. Kịch bản của luật đang `CHỜ` được
> đánh dấu 🚫 — **không viết test** cho tới khi mục conflict tương ứng `CLOSED-BA`.

---

## Ma trận

| ID | Nhóm | Điều kiện | Kết quả mong đợi | Luật phủ |
|---|---|---|---|---|
| S-001 | happy | Vào danh sách lần đầu | lọc `NgayHachToan ∈ [đầu tháng, hôm nay]`, sort 3 khóa | R-002, R-005 |
| S-002 | happy | Vào lại danh sách sau khi đã lọc | khôi phục đúng bộ lọc + sort lần trước | R-003 |
| S-003 | happy | Tenant có 3 loại nghiệp vụ | danh sách trả cả 3, không lọc `LoaiNghiepVu` | R-004 |
| S-004 | biên | Chứng từ USD, tỷ giá 25.000 | 4 cột tiền lấy `…QuyDoi` | R-006, INV-013 |
| S-005 | happy | 1 CTBH có 2 hóa đơn liên kết | cột Số hóa đơn = `"HD001, HD002"` | R-007 |
| S-006 | happy | 1 dòng Chưa ghi sổ + 1 dòng Đã ghi sổ | dòng 1 hiện Sửa/Ghi sổ/Xóa; dòng 2 hiện Bỏ ghi | R-008, R-009 |
| S-007 | happy | Đã ghi sổ + Chưa thanh toán | hiện nút Thu tiền | R-010 |
| S-008 | happy | `TrangThaiLapHoaDon` = Đã lập một phần, Đã ghi sổ | vẫn hiện nút Lập hóa đơn | R-011 |
| S-009 | happy | `TrangThaiXuatHang` = Chưa xuất, bán dịch vụ | **ẩn** nút Lập phiếu xuất | R-012 |
| S-010 | biên | Bộ lọc trả 0 chứng từ | ẩn dòng tổng cộng | R-013 |
| S-011 | biên | Chứng từ chỉ có dòng dịch vụ | `TrangThaiXuatHang = NULL`, cột trống | R-014, INV-009 |
| S-012 | happy | Mở Xem chi tiết | mọi trường readonly, 6 nút đúng danh sách | R-016, R-017 |
| S-013 | happy | Đổi tiêu điểm dòng, không đổi checkbox | khu chi tiết nạp theo tiêu điểm, checkbox giữ nguyên | R-018 |
| S-014 | happy | Chọn khách hàng KH001 (tổ chức) | auto-fill 8 trường tab ghi nợ + TK công nợ dòng 1 | R-021, R-022, R-023 |
| S-015 | happy | Chọn KH "Cty A", nhập số HĐ "001" | diễn giải = `"bán hàng Cty A theo hóa đơn số 001"` | R-024 |
| S-016 | ngoại lệ | MST tổ chức nhập `"12345"` | chặn lưu, `MSG_…_050` | R-025 |
| S-017 | happy | Sửa Tên KH ở tab PXK | tab ghi nợ + phiếu thu cập nhật theo, tab HĐ theo R-028 | R-027, R-028 |
| S-018 | happy | Đổi Ngày hạch toán ở tab Phiếu thu | 4 tab cùng ngày; Ngày chứng từ **không** đổi | R-029, R-068, INV-010 |
| S-019 | happy | Mở màn Thêm mới từ nút "Chứng từ bán hàng" | `SoChungTu` sinh theo quy tắc, tiền tố `BH` | R-030 |
| S-020 | biên | Sửa tay Hạn thanh toán rồi đổi Ngày chứng từ | Hạn thanh toán **giữ nguyên** | R-031 |
| S-021 | happy | `ThuTienNgay = false` | Hình thức TT tab HĐ = `"TM/CK"` | R-032 |
| S-022 | happy | Tích "Đã lập hóa đơn" | "Lập kèm hóa đơn" bị uncheck + disable | R-033 |
| S-023 | happy | Lưu hóa đơn đầu tiên từ CTBH có 2 cờ = false | `DaLapHoaDon := true`, counter **không** đổi | R-034, R-064 |
| S-024 | happy | `KiemPhieuXuatKho = false` | ẩn hẳn 8 cột nhóm kho | R-035 |
| S-025 | ngoại lệ | Toàn dòng dịch vụ + tích kiêm PXK | chặn lưu 🚫 message chờ C10 | R-036 |
| S-026 | happy | Chọn mã hàng VT001 (hàng hóa) | auto-fill 10 trường từ `mst_vat_tu` | R-038, R-039 |
| S-027 | happy | 3 dòng: hàng hóa · KM · CKTM, kiêm PXK | PXK có 2 dòng (hàng hóa + KM) | R-037, INV-008 |
| S-028 | happy | Thêm dòng sau dòng thường / sau dòng KM | chép đủ 7 trường / chỉ chép 7 cột TK | R-040, R-041 |
| S-029 | biên | Thêm dòng ghi chú vào chứng từ đã tính | mọi tổng không đổi, không sinh bút toán | R-042, INV-011 |
| S-030 | ngoại lệ | Thiếu quyền (View / Detail / Delete / Post / Unpost) | ẩn nút; gọi API trực tiếp → `MSG_…_007` | R-001, R-015, R-020, R-083, R-091, R-100 |
| S-031 | happy | Tích Hàng khuyến mại | CKTM disable; 3 cột CK disable; đơn giá mở khóa | R-043, R-044 |
| S-032 | biên | Dòng KM: Thành tiền 0, Tiền thuế nhập tay 100.000 | sinh bút toán #4, **không** sinh #1 | R-044 |
| S-033 | happy | Dòng CKTM Thành tiền 500.000 | lưu `−500.000`, hiển thị `500.000`, bút toán #3 `ABS` | R-045, INV-008 |
| S-034 | happy | Nhập SL 10, ĐG 1.000 | ThanhTien = 10.000; sửa ThanhTien 20.000 → ĐG = 2.000 | R-046 |
| S-035 | biên | Nhập SL = 0 khi ThanhTien = 20.000 | ĐG := 0, ThanhTien **giữ 20.000**, vẫn vào Σ | R-047 |
| S-036 | biên | ĐVT = Thùng (hệ số 24), SL 2, ĐG 240.000 | SL quy đổi 48, ĐG quy đổi 10.000 | R-048 |
| S-037 | happy | CK theo mặt hàng, nhập 10% | Tiền CK = 10% Thành tiền; giá trị tính thuế trừ CK | R-049 |
| S-038 | happy | CK theo mặt hàng và hóa đơn | CK HĐ tính trên "sau CK mặt hàng"; Tiền CK = tổng 2 phần | R-050, R-051, INV-006 |
| S-039 | happy | CK theo % hóa đơn 5%, có dòng KM | mọi dòng thường nhận 5%, dòng KM bỏ qua | R-052 |
| S-040 | happy | Lưới có dòng ghi chú + chứng từ VND | Σ bỏ dòng ghi chú; ẩn dòng tổng cột quy đổi | R-053 |
| S-041 | ngoại lệ | Dòng thường: Tiền CK 200.000 > Thành tiền 100.000 | **chặn lưu**, `MSG_…_044` | R-054, INV-006 |
| S-042 | ngoại lệ | Dòng KM: Tiền CK 200.000 > Thành tiền 0 | **cảnh báo Yes/No**, không chặn | R-054 |
| S-043 | happy | PBCK 3 phương thức | giá trị/số lượng → 2 cột disable; thủ công → enable | R-055, R-056, R-058 |
| S-044 | biên | PBCK 100.000 cho 3 dòng bằng nhau | 33.333 + 33.333 + **33.334**; Σ = 100.000 | R-057, INV-007 |
| S-045 | ngoại lệ | PBCK thủ công Σ tỷ lệ = 99% | chặn Áp dụng, `MSG_…_048` | R-059 |
| S-046 | happy | Lưu lần đầu, cả 3 cờ = true, 1 dòng SL 10 | counter HĐ = 10, counter kho = 10; sinh 3 bản ghi con có số riêng | R-060, R-062, R-065, R-067 |
| S-047 | happy | Lưu lần đầu, `DaLapHoaDon` do người dùng tích | counter HĐ = SoLuong | R-061 |
| S-048 | biên | Lưu lần đầu, cả 3 cờ = false | cả 2 counter = 0; không sinh bản ghi con | R-063 |
| S-049 | biên | Lưu sửa lần 2 chứng từ có counter HĐ = 5/10 | counter **giữ 5**, không bị ép về 10 | R-064, INV-005 |
| S-050 | happy | `ThuTienNgay` + Tiền mặt | sinh `cash_phieu_thu` liên kết `ChungTuBanId` | R-065 |
| S-051 | happy | Bỏ tích `ThuTienNgay` rồi lưu lại (phiếu chưa ghi sổ) | xóa bản ghi phiếu thu | R-066 |
| S-052 | happy | Đổi `ThuTienNgay` false → true, tiền mặt | tra lại định khoản, áp lại TK dòng chưa sửa tay | R-069 |
| S-053 | ngoại lệ | TK trên dòng bị đổi thành TK cha | chặn lưu, `MSG_…_107` | R-070, INV-012 |
| S-054 | biên | Sửa tay `ThanhTienQuyDoi` | **không** tính ngược ThanhTien / TyGia | R-071, INV-013 |
| S-055 | biên | Chiết khấu vượt thành tiền → tổng âm | `TongThanhToan` âm, hiển thị đỏ trong ngoặc | R-072, INV-003 |
| S-056 | happy | Bán hàng xuất khẩu | ẩn cột thuế GTGT + Tab Thuế; hiện khối thuế XK | R-073 |
| S-057 | **rollback** | Lỗi ở bước sinh phiếu thu | không bản ghi nào tồn tại; form giữ nguyên dữ liệu | R-074, R-075, INV-002 |
| S-058 | happy | Chứng từ Đã ghi sổ | ẩn nút Sửa | R-076 |
| S-059 | happy | Mở màn Sửa | hiện 4 trường theo dõi số lượng readonly | R-077 |
| S-060 | happy | `DaLapHoaDon` do hệ thống tự tích | disable cả 2 checkbox | R-079 |
| S-061 | happy | Sửa Tên KH của CTBH có PXK kiêm | PXK cập nhật theo, `SoChungTu` PXK giữ nguyên | R-080, INV-002 |
| S-062 | ngoại lệ | Sửa SoLuong khi Đã ghi sổ | chặn | R-082 |
| S-063 | happy | Bấm Xóa | popup xác nhận đúng cấu trúc BR3 | R-084 |
| S-064 | ngoại lệ | Xóa chứng từ Đã ghi sổ | chặn, `MSG_…_013`, kiểm **trước** kiểm "đã sử dụng" | R-085, INV-001 |
| S-065 | ngoại lệ | Có Create, thiếu Post | chỉ hiện nút "Lưu", ẩn "Lưu và ghi sổ" | R-091 |
| S-066 | ngoại lệ | Ghi sổ vào kỳ đã khóa | chặn theo BR17 chung | R-092, INV-014 |
| S-067 | happy | Ghi sổ 1 dòng bán trong nước có CK + thuế | 3 bút toán × 2 = 6 bản ghi `acc_so_cai` | R-093, R-094, R-095, INV-001 |
| S-068 | happy | Ghi sổ chứng từ xuất khẩu | có bút toán #5, không có #4 | R-093 |
| S-069 | happy | Ghi sổ hàng loạt 5 chứng từ, 2 lỗi | 3 thành công, popup `MSG_…_108` "3/2" | R-096 |
| S-070 | happy | Ghi sổ CTBH có PXK + phiếu thu kiêm + HĐ | cả 3 chứng từ → Đã ghi sổ; **hóa đơn không đổi** | R-097, R-099 |
| S-071 | **rollback** | Ghi sổ nhóm, phiếu xuất kho không đủ tồn | chặn cả nhóm, không chứng từ nào đổi trạng thái | R-098, INV-002 |
| S-072 | ngoại lệ | Bỏ ghi sổ khi phiếu thu lập riêng Đã ghi sổ | chặn, `MSG_…_049` | R-101 |
| S-073 | ngoại lệ | Bỏ ghi sổ khi đang tham gia đối trừ | chặn, `MSG_…_052` | R-102 |
| S-074 | happy | Bỏ ghi sổ CTBH có PXK **lập riêng** đã xuất đủ | cho phép; `TrangThaiXuatHang` **giữ** "Đã xuất đủ" | R-103, R-105 |
| S-075 | **rollback** | Bỏ ghi sổ CTBH kiêm | xóa hết `acc_so_cai` + sổ công nợ + sổ kho của cả nhóm | R-104, INV-002 |
| S-076 | happy | Bỏ ghi sổ CTBH có thu tiền ngay | `SoTienDaThanhToan := 0`, trạng thái → Chưa thanh toán | R-106, INV-003 |
| S-077 | happy | Mở Xem dữ liệu ghi sổ, chứng từ chưa Lưu | chế độ Xem trước, không tạo bản ghi nào | R-107, R-108, R-109 |
| S-078 | happy | Mở Xem dữ liệu ghi sổ, chứng từ đã ghi sổ, kiêm PXK | đọc `acc_so_cai` của cả nhóm, sắp xếp đúng thứ tự | R-108, R-110, R-112 |
| S-079 | biên | Xem trước khi dòng chưa chọn TK doanh thu | bỏ bút toán #1, các bút toán khác vẫn hiện, không báo lỗi | R-111 |
| S-080 | **tương tranh** | 2 request cùng lập PXK 6/10 từ 1 dòng | 1 thành công, 1 lỗi `MSG_…_103`, counter cuối = 6 | INV-004 |
| S-081 | **tương tranh** | 2 request cùng lập HĐ 6/10 từ 1 dòng | 1 thành công, 1 lỗi `MSG_…_102`, counter cuối = 6 | INV-005 |

**Kịch bản 🚫 bị chặn (chưa viết):** xóa hàng loạt (`C01`), điều kiện "đã sử dụng" (`C02` `C03` `C04`),
cascade hóa đơn (`C05`), sửa chứng từ có liên kết (`C06`), nút lập PXK trên Xem chi tiết (`C07`),
nội dung `MSG_…_109` (`C10`). Sau khi BA chốt sẽ bổ sung `S-082…`.

---

## Chi tiết — kịch bản P0

### S-004 · Chứng từ ngoại tệ trên danh sách
```
Nhóm      biên            Luật phủ  R-CTBH-006 · INV-013

INPUT
  LoaiTien              = USD
  TyGia                 = 25.000
  TongTienHang          = 1.000        TongTienHangQuyDoi    = 25.000.000
  TongThanhToan         = 1.100        TongThanhToanQuyDoi   = 27.500.000

EXPECTED — lưới danh sách
  cột Thành tiền              = 25.000.000
  cột Tổng tiền thanh toán    = 27.500.000
  (KHÔNG hiển thị 1.000 / 1.100 — cột danh sách luôn theo đồng tiền hạch toán)
```

### S-018 · Đồng bộ ngày hạch toán, không đồng bộ ngày chứng từ
```
Nhóm      happy           Luật phủ  R-CTBH-029 · R-CTBH-068 · INV-010

INPUT
  KiemPhieuXuatKho = true · ThuTienNgay = true (tiền mặt)
  Tab ghi nợ:    NgayHachToan = 2026-08-01   NgayChungTu = 2026-08-01
  Tab PXK:       NgayChungTu  = 2026-08-02
  Tab Phiếu thu: NgayChungTu  = 2026-08-03
  → người dùng đổi NgayHachToan ở TAB PHIẾU THU thành 2026-08-05

EXPECTED — trên form
  NgayHachToan  4 tab đều = 2026-08-05
  NgayChungTu   ghi nợ 2026-08-01 · PXK 2026-08-02 · phiếu thu 2026-08-03 (KHÔNG đổi)

EXPECTED — sau Lưu
  sal_chung_tu_ban.NgayHachToan     = 2026-08-05
  inv_phieu_xuat_kho.NgayHachToan   = 2026-08-05
  cash_phieu_thu.NgayHachToan       = 2026-08-05
  inv_phieu_xuat_kho.NgayChungTu    = 2026-08-02
  cash_phieu_thu.NgayChungTu        = 2026-08-03
```

### S-027 · Xác định dòng vào phiếu xuất kho
```
Nhóm      happy           Luật phủ  R-CTBH-037 · INV-008

INPUT   KiemPhieuXuatKho = true, lưới 4 dòng:
  D1  VT001 (hàng hóa)     SL 10
  D2  VT002 (hàng hóa)     SL 5    LaHangKhuyenMai = true
  D3  VT003 (hàng hóa)     SL 2    LaChietKhauThuongMai = true
  D4  DV001 (dịch vụ)      SL 1
  D5  dòng ghi chú         LoaiDongHang = false

EXPECTED — sau Lưu
  inv_phieu_xuat_kho_chi_tiet   đúng 2 dòng: VT001 (10) và VT002 (5)
  SoLuongDaXuatKho              D1 = 10 · D2 = 5 · D3 = 0 · D4 = 0 · D5 = 0
  bút toán giá vốn              chỉ sinh cho D1 và D2 (do phiếu xuất kho sinh)
```

### S-035 · Số lượng = 0 giữ nguyên thành tiền
```
Nhóm      biên            Luật phủ  R-CTBH-047

INPUT
  Dòng đang có: SoLuong = 10 · DonGia = 2.000 · ThanhTien = 20.000
  → người dùng nhập SoLuong = 0

EXPECTED — ngay sau khi nhập (không cần rời ô)
  SoLuong    = 0
  DonGia     = 0          ← bị ép về 0
  ThanhTien  = 20.000     ← GIỮ NGUYÊN, không ghi đè về 0

EXPECTED — Section Tổng hợp
  TongTienHang bao gồm 20.000 của dòng này
```

### S-038 · Chiết khấu theo mặt hàng và hóa đơn
```
Nhóm      happy           Luật phủ  R-CTBH-050 · R-CTBH-051 · INV-006

INPUT
  LoaiChietKhau               = "Theo mặt hàng và hóa đơn"
  Dòng D1: ThanhTien = 1.000.000 · TyLeChietKhauTheoHang = 10%
  TyLeChietKhauTheoHoaDon     = 5%

EXPECTED — trên dòng D1
  TienChietKhauTheoHang       = 100.000
  Thành tiền sau CK mặt hàng  = 900.000        (tính tại chỗ, không lưu)
  TienChietKhauTheoHoaDon     = 45.000         = 900.000 × 5%
  TienChietKhau               = 145.000        = 100.000 + 45.000
  TyLeChietKhau               = 14,5%          = 145.000 / 1.000.000 × 100
  Giá trị tính thuế           = 855.000        = 1.000.000 − 145.000

EXPECTED — bút toán khi ghi sổ
  đúng MỘT bút toán #2 trên số tổng 145.000, dùng TaiKhoanChietKhauId của dòng
  (KHÔNG tách thành 2 bút toán 100.000 + 45.000)
```

### S-044 · Phân bổ chiết khấu — dòng cuối bù làm tròn
```
Nhóm      biên            Luật phủ  R-CTBH-057 · INV-007

INPUT
  Số tiền CK  = 100.000
  Phương thức = "Theo giá trị"
  3 dòng, ThanhTien bằng nhau = 1.000.000 mỗi dòng

EXPECTED
  D1 TienChietKhau = 33.333      TyLePhanBo = 33,33
  D2 TienChietKhau = 33.333      TyLePhanBo = 33,33
  D3 TienChietKhau = 33.334      TyLePhanBo = 33,34    ← bù chênh lệch
  Σ TienChietKhau  = 100.000     (khớp TUYỆT ĐỐI số tiền nhập)
  Σ TyLePhanBo     = 100,00
```

### S-046 · Lưu lần đầu với cả ba checkbox
```
Nhóm      happy           Luật phủ  R-CTBH-060 · R-CTBH-062 · R-CTBH-065 · R-CTBH-067

INPUT
  LoaiNghiepVu      = Bán hàng trong nước
  KiemPhieuXuatKho  = true · LapKemHoaDon = true · ThuTienNgay = true (Tiền mặt)
  1 dòng hàng: VT001 (hàng hóa) · SoLuong = 10 · DonGia = 100.000

EXPECTED — sal_chung_tu_ban
  TrangThaiGhiSo        = "Chưa ghi sổ"
  TrangThaiLapHoaDon    = "Đã lập đủ"          (counter = SoLuong)
  TrangThaiXuatHang     = "Đã xuất đủ"         (counter = SoLuong)
  TrangThaiThanhToan    = "Chưa thanh toán"    ← chỉ đổi khi phiếu thu GHI SỔ
  SoChungTu             khớp quy tắc "Chứng từ bán hàng", tiền tố BH

EXPECTED — sal_chung_tu_ban_chi_tiet (dòng D1)
  SoLuongDaXuatHoaDon   = 10
  SoLuongDaXuatKho      = 10

EXPECTED — bản ghi con
  inv_phieu_xuat_kho     1 bản ghi · NguonId = sal_chung_tu_ban.Id
                         · LoaiChungTuNguon = ChungTuBan · SoChungTu tiền tố PXK
                         · TrangThaiGhiSo = "Chưa ghi sổ"
  cash_phieu_thu         1 bản ghi · cash_phieu_thu_chi_tiet.ChungTuBanId = Id
                         · SoChungTu tiền tố PT · TrangThaiGhiSo = "Chưa ghi sổ"
  sal_hoa_don_ban_hang   1 bản ghi · ChungTuBanId = Id
                         · …_chi_tiet.ChiTietChungTuBanId = D1.Id

EXPECTED — sổ sách
  acc_so_cai             0 bản ghi
  acc_so_kho             0 bản ghi
  sổ công nợ             0 bản ghi
```

### S-049 · Lưu sửa không khởi tạo lại counter
```
Nhóm      biên            Luật phủ  R-CTBH-064 · INV-005

INPUT
  Chứng từ đã tồn tại: D1 SoLuong = 10 · SoLuongDaXuatHoaDon = 5 (đã lập HĐ 5 cái)
  DaLapHoaDon = true (do HỆ THỐNG tự tích theo R-CTBH-034)
  → người dùng sửa Diễn giải rồi Lưu

EXPECTED
  SoLuongDaXuatHoaDon   = 5           ← GIỮ NGUYÊN, KHÔNG bị ép lên 10
  TrangThaiLapHoaDon    = "Đã lập một phần"
```

### S-057 · Rollback toàn bộ khi lỗi giữa chừng
```
Nhóm      rollback        Luật phủ  R-CTBH-074 · R-CTBH-075 · INV-002

INPUT
  Cả 3 checkbox = true; ép lỗi ở bước sinh phiếu thu (vd TaiKhoanTienId không hợp lệ)
  → bấm "Lưu và ghi sổ"

EXPECTED — cơ sở dữ liệu
  sal_chung_tu_ban           0 bản ghi mới
  sal_chung_tu_ban_chi_tiet  0 bản ghi mới
  inv_phieu_xuat_kho         0 bản ghi mới      ← đã sinh trước đó nhưng phải rollback
  sal_hoa_don_ban_hang       0 bản ghi mới
  cash_phieu_thu             0 bản ghi mới
  acc_so_cai                 0 bản ghi mới
  bộ đếm số chứng từ         KHÔNG tăng

EXPECTED — giao diện
  form KHÔNG đóng, KHÔNG reset; giữ nguyên mọi giá trị đã nhập; highlight trường lỗi
```

### S-067 · Bút toán một dòng bán trong nước
```
Nhóm      happy           Luật phủ  R-CTBH-093 · R-CTBH-094 · R-CTBH-095 · INV-001

INPUT   ghi sổ chứng từ VND, 1 dòng hàng D1 (ThuTu = 1):
  ThanhTien       = 10.000.000    TaiKhoanCongNoId    = 131
  TienChietKhau   =    500.000    TaiKhoanDoanhThuId  = 5111
  TienThueGTGT    =    950.000    TaiKhoanChietKhauId = 5211
                                  TaiKhoanThueGTGTId  = 33311

EXPECTED — acc_so_cai: đúng 6 bản ghi (3 bút toán × 2 vế)
  STT=1 vế Nợ   TKId 131   TKDoiUngId 5111   PSNo 10.000.000  PSCo 0
  STT=1 vế Có   TKId 5111  TKDoiUngId 131    PSNo 0           PSCo 10.000.000
  STT=2 vế Nợ   TKId 5211  TKDoiUngId 131    PSNo 500.000     PSCo 0
  STT=2 vế Có   TKId 131   TKDoiUngId 5211   PSNo 0           PSCo 500.000
  STT=4 vế Nợ   TKId 131   TKDoiUngId 33311  PSNo 950.000     PSCo 0
  STT=4 vế Có   TKId 33311 TKDoiUngId 131    PSNo 0           PSCo 950.000

EXPECTED — mọi bản ghi
  ChungTuId          = sal_chung_tu_ban.Id
  ChiTietChungTuId   = D1.Id            STTDongChiTiet = 1
  TienTeHachToanId   = đồng tiền hạch toán của TENANT (không phải LoaiTienId)
  TyGia              = 1                PSNoQuyDoi = PSNo · PSCoQuyDoi = PSCo
  IsAuto             = false
  Σ PSNo = Σ PSCo    = 11.450.000       ← INV-001
```

### S-071 · Chặn cả nhóm khi một chứng từ lỗi
```
Nhóm      rollback        Luật phủ  R-CTBH-098 · INV-002

INPUT
  CTBH kiêm PXK + phiếu thu, tồn kho không đủ để xuất → bấm Ghi sổ trên CHỨNG TỪ BÁN

EXPECTED
  sal_chung_tu_ban.TrangThaiGhiSo      = "Chưa ghi sổ"   (không đổi)
  inv_phieu_xuat_kho.TrangThaiGhiSo    = "Chưa ghi sổ"
  cash_phieu_thu.TrangThaiGhiSo        = "Chưa ghi sổ"
  acc_so_cai                            0 bản ghi mới cho cả 3 chứng từ
  acc_so_kho                            0 bản ghi mới
  thông báo                             MSG_PMKT-E-06194_042
```

### S-074 · Bỏ ghi sổ không đổi trạng thái xuất hàng
```
Nhóm      happy           Luật phủ  R-CTBH-103 · R-CTBH-105

INPUT
  CTBH SoLuong 10, KHÔNG kiêm PXK; đã lập PXK LẬP RIÊNG 10 cái (SoLuongDaXuatKho = 10)
  CTBH đang "Đã ghi sổ"; PXK lập riêng cũng "Đã ghi sổ"
  → bỏ ghi sổ CHỨNG TỪ BÁN

EXPECTED
  thao tác                         THÀNH CÔNG (PXK lập riêng không phải điều kiện chặn)
  sal_chung_tu_ban.TrangThaiGhiSo  = "Chưa ghi sổ"
  TrangThaiXuatHang                = "Đã xuất đủ"    ← KHÔNG đổi
  SoLuongDaXuatKho                 = 10              ← KHÔNG đổi
  inv_phieu_xuat_kho (lập riêng)   vẫn "Đã ghi sổ", không bị đụng
```

### S-075 · Bỏ ghi sổ nhóm chứng từ kiêm
```
Nhóm      rollback        Luật phủ  R-CTBH-104 · INV-002

INPUT
  CTBH kiêm PXK + phiếu thu, cả nhóm đang "Đã ghi sổ"
  acc_so_cai: 6 bản ghi của CTBH + 2 của PXK + 2 của phiếu thu
  → bỏ ghi sổ ở PHIẾU XUẤT KHO

EXPECTED
  cả 3 chứng từ                TrangThaiGhiSo = "Chưa ghi sổ"
  acc_so_cai (cả 3 ChungTuId)  0 bản ghi còn lại
  acc_so_kho                   0 bản ghi còn lại
  sổ công nợ (ChungTuId=CTBH)  0 bản ghi còn lại
  SoTienDaThanhToan            = 0 · TrangThaiThanhToan = "Chưa thanh toán"
  hóa đơn lập kèm              KHÔNG bị đụng (R-CTBH-099)
  SoLuongDaXuatKho             = 10   ← KHÔNG đổi (R-CTBH-105)
```

### S-080 · Tương tranh lập phiếu xuất kho
```
Nhóm      tương tranh     Luật phủ  INV-004

INPUT
  Dòng D1: SoLuong = 10 · SoLuongDaXuatKho = 0
  Hai request ĐỒNG THỜI, mỗi request lập PXK xuất 6 cái từ D1

EXPECTED
  đúng 1 request THÀNH CÔNG
  request còn lại THẤT BẠI với MSG_PMKT-E-06194_103
  SoLuongDaXuatKho cuối cùng = 6        ← KHÔNG phải 12
  inv_phieu_xuat_kho           đúng 1 bản ghi mới

Ghi chú   BR23 mục 3.3 yêu cầu kiểm tra + cập nhật counter phải NGUYÊN TỬ (khóa dòng hoặc
          optimistic lock). Test phải chạy 2 luồng thật, không mô phỏng tuần tự.
```

### S-081 · Tương tranh lập hóa đơn
```
Nhóm      tương tranh     Luật phủ  INV-005

INPUT
  Dòng D1: SoLuong = 10 · SoLuongDaXuatHoaDon = 0
  Hai request ĐỒNG THỜI, mỗi request lập hóa đơn 6 cái từ D1

EXPECTED
  đúng 1 request THÀNH CÔNG
  request còn lại THẤT BẠI với MSG_PMKT-E-06194_102
  SoLuongDaXuatHoaDon cuối cùng = 6
  sal_hoa_don_ban_hang            đúng 1 bản ghi mới
```

---

## Ghi chú về phủ nhóm

| Nhóm | Số kịch bản | Đủ chưa |
|---|---|---|
| happy path | 34 | đủ — phủ 7 UC |
| biên | 14 | đủ — SL 0 · tổng âm · làm tròn · ĐVT quy đổi · counter một phần |
| ngoại lệ / bị chặn | 21 | đủ — quyền · trạng thái · validate · kỳ khóa · liên kết |
| rollback | 6 | đủ — lỗi giữa chừng khi lưu · ghi sổ nhóm · bỏ ghi sổ nhóm |
| tương tranh | 6 | **mỏng** — mới phủ counter (S-080, S-081). Chưa có kịch bản tương tranh cho: cấp số chứng từ đồng thời (BR25 chung) và sửa đồng thời một chứng từ (`MSG_…_105` có mã nhưng không BR nào mô tả cơ chế — xem `00-source-map.md` §4) |
