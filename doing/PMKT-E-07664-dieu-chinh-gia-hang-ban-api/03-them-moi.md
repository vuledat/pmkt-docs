# F3 — Thêm mới Chứng từ điều chỉnh giá

| | |
|---|---|
| Mã chức năng | **F3** |
| UC nguồn | [PMKT-U-07666 — Thêm mới](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/4.usecases/PMKT-U-07666_ThemMoi/UC_ThemMoi.md) |
| Màn hình nguồn | [SCR_ThemMoiDieuChinhGia.md](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/5.screens/SCR_ThemMoiDieuChinhGia.md) |
| Endpoint phụ trách | **A4** `POST /api/ban-hang/dieu-chinh-gia-hang-ban` |
| Phụ thuộc | Bước 1 chọn nguồn → [08](08-chon-nguon-chung-tu.md) · schema → [09](09-thiet-ke-db.md) |

## 1. Quyết định riêng

- **Một endpoint cho cả "Lưu" và "Lưu và ghi sổ"**, phân biệt bằng cờ `ghiSo` trong body — đúng mẫu `LuuChungTuBanHangRequest.ghiSo` ([:95](../../cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/internal/dto/LuuChungTuBanHangRequest.java)) và đúng hook `coGhiSoNgay` của template ([ChungTuTemplate.java:341](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)). **Không chọn** hai endpoint riêng: "Lưu và ghi sổ" phải là **một** transaction, hai request rời sẽ để lại chứng từ đã lưu mà chưa ghi sổ khi request thứ hai hỏng.
- **Path là `POST /` (rỗng)**, không phải `/them-moi` của base — override như `ChungTuBanHangController.create` ([:126](../../cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/internal/controller/ChungTuBanHangController.java)), và khớp đúng đường dẫn FE đã khai (`IMPLEMENT.md` dòng 181).
- **BE tính lại toàn bộ số tiền**, không tin số FE gửi. FE vẫn gửi (để hiển thị tức thì và để đối chiếu), BE ghi đè bằng kết quả `TinhToanDieuChinhGia`. Lý do: số tiền là đầu vào của bút toán — một sai lệch làm bảng cân đối sai, và client không phải nơi giữ bất biến kế toán.
- **Không sinh số chứng từ** (D12): người dùng nhập. Chống trùng: kiểm sớm ở service (trả `MSG_109` đọc được) + unique index `uq_sal_dcg_so_ct` làm chốt chặn cuối.

## 2. Hợp đồng API

### A4 — `POST /api/ban-hang/dieu-chinh-gia-hang-ban` · quyền `DieuChinhGiaHangBan.Create`

```jsonc
// Request — LuuDieuChinhGiaHangBanRequest
{
  // ── Khối tùy chọn nghiệp vụ (SCR dòng 262-274) ────────────────────────────
  "huongDieuChinhGia": "GiamGia",          // TangGia | GiamGia — BẮT BUỘC
  "thanhToanNgay": true,
  "hinhThucThanhToan": "ChiTienMat",       // xem bảng field §2.1
  "lapKemHoaDonDieuChinh": true,

  // ── Xuất xứ (Bước 1) ──────────────────────────────────────────────────────
  "nguonChungTu": "CHUNG_TU_BAN_HANG",     // CHUNG_TU_BAN_HANG | HOA_DON_DIEU_CHINH | null
  "lyDoDieuChinhNguon": null,              // chỉ khi nguồn = HOA_DON_DIEU_CHINH
  "chungTuBanHangId": "…",
  "chungTuBanDichVuId": null,
  "hoaDonDieuChinhId": null,

  // ── Tab Chứng từ điều chỉnh công nợ (luôn có) ─────────────────────────────
  "khachHangId": "…",                      // BẮT BUỘC
  "tenKhachHang": "Công ty TNHH ABC",      // BẮT BUỘC
  "soChungTu": "BGG00001",                 // BẮT BUỘC, ≤ 50
  "maSoThue": "0101234567",
  "diaChi": "12 Nguyễn Trãi, Hà Nội",
  "ngayChungTu": "2026-08-10",             // BẮT BUỘC
  "ngayHachToan": "2026-08-10",            // BẮT BUỘC
  "nhanVienBanHangId": "…",
  "dienGiai": "Giảm giá hàng bán theo thỏa thuận",

  // ── Tiền tệ ───────────────────────────────────────────────────────────────
  "loaiTienId": "…",                       // BẮT BUỘC
  "tyGia": 1,                              // > 0

  // ── Tab thanh toán (chỉ khi thanhToanNgay = true) ─────────────────────────
  "chungTuThanhToan": {
    "soChungTu": "PC00042",                // BẮT BUỘC khi thanhToanNgay
    "taiKhoanTienId": "…",                 // BẮT BUỘC khi thanhToanNgay
    "taiKhoanNganHangId": null,
    "tenNganHang": null,
    "nguoiGiaoDich": "Nguyễn Văn A",
    "lyDo": "Chi trả giảm giá hàng bán",
    "soGiayTo": null, "ngayCap": null, "noiCap": null,
    "kemTheo": null, "chungTuGoc": null
  },

  // ── Tab Hóa đơn ───────────────────────────────────────────────────────────
  "hoaDon": {
    "tenKhachHang": "…", "maSoThue": "…", "diaChi": "…",
    "nguoiMuaHang": "…", "maSoDvqhns": null, "cccd": null, "hoChieu": null,
    "soDienThoai": "0912345678",
    "hinhThucThanhToan": "Tiền mặt",
    "taiKhoanNganHangThuId": null,
    "loaiDieuChinh": "DieuChinhGia",       // BẮT BUỘC khi lapKemHoaDonDieuChinh
    "lyDoDieuChinh": "Điều chỉnh giảm giá theo hợp đồng",  // BẮT BUỘC khi lapKem…
    "mauSoHoaDon": "1", "kyHieuHoaDon": "C26TAA",
    "soHoaDonDieuChinh": "00001234", "ngayHoaDonDieuChinh": "2026-08-10",
    "hoaDonGocId": "…"                     // BẮT BUỘC khi lapKemHoaDonDieuChinh
  },

  // ── Lưới chi tiết (≥ 1 dòng) ──────────────────────────────────────────────
  "chiTiet": [
    {
      "thuTu": 1,
      "maHangId": "…",                     // BẮT BUỘC
      "tenHang": "Bánh gạo hộp 200g",
      "donViTinhId": "…",
      "taiKhoanCongNoId": "…",             // BẮT BUỘC
      "taiKhoanDoanhThuId": null,          // BẮT BUỘC khi huong = TangGia
      "taiKhoanGiamGiaId": "…",            // BẮT BUỘC khi huong = GiamGia
      "soLuong": 10, "donGia": 5000, "thanhTien": 50000,
      "chietKhauPhanTram": 0, "chietKhauTien": 0, "taiKhoanChietKhauId": null,
      "thueSuatGtgt": "10", "giaTriThueGtgt": null,
      "tienThueGtgt": 5000, "taiKhoanThueGtgtId": "…",   // TK thuế BẮT BUỘC
      "khongTongHopToKhaiGtgt": false,
      "chungTuNguonId": "…", "chiTietNguonId": "…",
      "soChungTuBanHang": "PBH00120", "soHoaDonGoc": "00001200",
      "ngayChungTuGoc": "2026-07-15",
      "donViId": null, "vuViecId": null, "khoanMucChiPhiId": null, "doiTuongThcpId": null
    }
  ],

  "ghiSo": false                            // false = "Lưu"; true = "Lưu và ghi sổ"
}
```

### 2.1 Bảng field header

| Field | Kiểu | Bắt buộc | Ràng buộc | Nguồn BA |
|---|---|---|---|---|
| `huongDieuChinhGia` | enum | **Y** | `TangGia` \| `GiamGia` — khớp CHECK `loai_dieu_chinh` ([V1:16322](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)) | SCR dòng 264 |
| `thanhToanNgay` | bool | N | mặc định `false` | SCR dòng 265 |
| `hinhThucThanhToan` | enum | **Y khi** `thanhToanNgay` | `thanhToanNgay=false` ⇒ server ghi `DieuChinhCongNo`. `TangGia` ⇒ `ThuTienMat`\|`GiayBaoCo`; `GiamGia` ⇒ `ChiTienMat`\|`UyNhiemChi`\|`SecChuyenKhoan`\|`SecTienMat` | SCR BR6 dòng 269-274 |
| `lapKemHoaDonDieuChinh` | bool | N | mặc định `true` khi nguồn là CTBH; **`false` và khóa** khi nguồn là HĐ điều chỉnh (SCR dòng 217) | SCR dòng 267 |
| `nguonChungTu` | enum | N | `CHUNG_TU_BAN_HANG` \| `HOA_DON_DIEU_CHINH` \| `null` (lập tay) | SCR dòng 22-27 |
| `lyDoDieuChinhNguon` | enum | **Y khi** nguồn = HĐ ĐC | `DieuChinhTang` \| `DieuChinhGiam` | SCR dòng 38 |
| `khachHangId` | uuid | **Y** | tồn tại trong `mst_khach_hang` | SCR dòng 288 |
| `tenKhachHang` | string(255) | **Y** | trim (BR43) | SCR dòng 289 |
| `soChungTu` | string(50) | **Y** | ≤ 50, không dấu tiếng Việt (BR20.2), duy nhất trong tenant (BR19.1) | SCR dòng 290 |
| `maSoThue` | string(255) | N | | SCR dòng 291 |
| `diaChi` | string(500) | N | | SCR dòng 292 |
| `ngayChungTu` | date | **Y** | ≤ ngày hiện tại (`MSG_103`) | SCR dòng 293 |
| `ngayHachToan` | date | **Y** | ≥ `ngayChungTu` (`MSG_205`); thuộc kỳ mở (`MSG_203`) | SCR dòng 296 |
| `nhanVienBanHangId` | uuid | N | | SCR dòng 294 |
| `dienGiai` | string(500) | N | → cột `mo_ta` | SCR dòng 295 |
| `loaiTienId` | uuid | **Y** | | SCR dòng 184 (lấy từ CTBH nguồn) |
| `tyGia` | decimal(18,6) | **Y** | > 0; = 1 khi loại tiền = tiền hạch toán (BR18.1) | BR18 |
| `chiTiet[]` | list | **Y** | ≥ 1 dòng (`MSG_104`) | SCR dòng 600 |
| `ghiSo` | bool | N | mặc định `false` | SCR dòng 520-524 |

### 2.2 Bảng field dòng chi tiết (SCR dòng 444-465)

| # | Field | Kiểu | Bắt buộc | Ràng buộc / công thức | BR |
|---|---|---|---|---|---|
| 1 | `maHangId` | uuid | **Y** | tồn tại trong danh mục VTHH | — |
| 2 | `tenHang` | string(255) | N | autofill | — |
| 3 | `taiKhoanCongNoId` | uuid | **Y** | nguồn CTBH ⇒ autofill từ CTBH; khác ⇒ TK công nợ trên DM KH | BR7 (SCR) |
| 4 | `taiKhoanDoanhThuId` | uuid | **Y khi** `TangGia` | nguồn CTBH ⇒ autofill; khác ⇒ TK doanh thu của vật tư | BR8 (SCR) |
| 5 | `taiKhoanGiamGiaId` | uuid | **Y khi** `GiamGia` | TK giảm giá của VTHH (5213) | BR8 (SCR) |
| 6 | `donViTinhId` | uuid | N | | — |
| 7 | `soLuong` | decimal(18,3) | **Y** | > 0, **trừ dòng dịch vụ** (§12-Q4 file gốc) | BR7 |
| 8 | `donGia` | decimal(18,2) | **Y** | > 0, **trừ dòng dịch vụ** | BR9 (SCR) |
| 9 | `thanhTien` | decimal(18,2) | **Y** | server tính `= soLuong × donGia`; dòng dịch vụ nhập tay | BR15 (SCR) |
| 10 | `thanhTienQuyDoi` | decimal(18,2) | — | **server tính** `= thanhTien × tyGia` | BR18.2 |
| 11 | `chietKhauPhanTram` | decimal(5,2) | N | 0–100 | — |
| 12 | `chietKhauTien` | decimal(18,2) | N | server tính `= chietKhauPhanTram × thanhTien / 100`; nếu client gửi `chietKhauTien` mà không gửi `%` thì server tính ngược `%` | BR10 (SCR) |
| 13 | `chietKhauTienQuyDoi` | decimal(18,2) | — | **server tính** | BR18.2 |
| 14 | `taiKhoanChietKhauId` | uuid | N | ngầm định TK CK trên DM VTHH | — |
| 15 | `thueSuatGtgt` | enum | **Y** | `0`\|`5`\|`8`\|`10`\|`KCT`\|`KKKNT`\|`KHAC`; không chọn nguồn ⇒ mặc định `0` | BR11 CTBH |
| — | `giaTriThueGtgt` | decimal(18,2) | **Y khi** `thueSuatGtgt = KHAC` | phần trăm tường minh | — |
| 16 | `tienThueGtgt` | decimal(18,2) | — | **server tính** `= (thanhTien − chietKhauTien) × thuếsuất` | SCR dòng 461 |
| 17 | `tienThueGtgtQuyDoi` | decimal(18,2) | — | **server tính** | BR18.2 |
| 18 | `khongTongHopToKhaiGtgt` | bool | N | `thueSuatGtgt ∈ {KHAC, KKKNT}` ⇒ **server ép `true`**; các mức khác ⇒ giữ giá trị client gửi (mặc định `false`) | BR_KhongTongHopToKhaiGTGT (SCR dòng 498-501) |
| 19 | `taiKhoanThueGtgtId` | uuid | **Y** | mặc định 33311x đầu tiên | SCR dòng 464 |
| — | `chungTuNguonId` / `chiTietNguonId` | uuid | N | có khi lập từ nguồn; dùng dựng liên kết (D4) | SCR "Lưu ý quan trọng" §1 |
| — | `soChungTuBanHang`, `soHoaDonGoc`, `ngayChungTuGoc` | string/date | N | snapshot hiển thị, **không cho sửa** ở FE | SCR dòng 202 |
| — | `thuTu` | int | N | thứ tự dòng; thiếu ⇒ server đánh lại theo thứ tự mảng | BR21.2 |

### 2.3 Response

```jsonc
// 201 Created
{
  "code": "SUCCESS",
  "message": "Thêm mới chứng từ điều chỉnh giá thành công",   // hoặc "Ghi sổ … thành công" khi ghiSo=true
  "messageId": "MSG_PMKT-E-07664_001",                        // hoặc _004 khi ghiSo=true
  "data": { /* giống A3 của 02-xem-chi-tiet.md */ }
}
```

### 2.4 Bảng lỗi

| Điều kiện | HTTP | Mã lỗi (hằng) | messageId |
|---|---|---|---|
| Thiếu quyền `.Create` | 403 | — | `MSG_PMKT-E-07664_007` |
| `soChungTu` rỗng | 400 | `THIEU_SO_CHUNG_TU` | `_101` |
| `soChungTu` trùng | 400 | `TRUNG_SO_CHUNG_TU` | `_109` |
| `huongDieuChinhGia` rỗng | 400 | `THIEU_PHUONG_THUC` | `_102` |
| `hoaDon.loaiDieuChinh` rỗng khi lập kèm HĐ | 400 | `THIEU_LOAI_DIEU_CHINH` | `_207` |
| `hoaDon.lyDoDieuChinh` rỗng khi lập kèm HĐ | 400 | `THIEU_LY_DO` | `_110` |
| `ngayChungTu` rỗng | 400 | `THIEU_NGAY_CHUNG_TU` | `_107` |
| `ngayChungTu` > hôm nay | 400 | `NGAY_CT_KHONG_HOP_LE` | `_103` |
| `chiTiet` rỗng | 400 | `THIEU_DONG_CHI_TIET` | `_104` |
| `soLuong ≤ 0` (dòng không phải dịch vụ) | 400 | `SO_LUONG_KHONG_HOP_LE` | `_105` |
| `donGia ≤ 0` (dòng không phải dịch vụ) | 400 | `DON_GIA_KHONG_HOP_LE` | `_106` |
| `ngayHachToan < ngayChungTu` | 400 | `NGAY_HT_NHO_HON_NGAY_CT` | `_205` |
| `ngayHachToan` thuộc kỳ đã khoá | 400 | `KY_KE_TOAN_DONG` | `_203` (kernel ném `PeriodLockedException`) |
| Tick lập kèm HĐ nhưng thiếu `hoaDon.hoaDonGocId` | 400 | `THIEU_HOA_DON_GOC` | `_206` |
| `chungTuNguonId`/`chiTietNguonId` trỏ dòng không tồn tại / đã xoá | 400 | `CHUNG_TU_GOC_KHONG_TON_TAI` | `_204` |
| Lỗi không lường trước | 500 | — | `_006` |

## 3. Ánh xạ cột BA ↔ DB ↔ DTO

Xem đầy đủ ở [02 §3](02-xem-chi-tiet.md) (header + hai object con) và [09 §9.2](09-thiet-ke-db.md) (danh sách cột thêm mới). Bốn điểm cần nhắc lại vì hay map sai:

| Field DTO | Cột DB | Bẫy |
|---|---|---|
| `huongDieuChinhGia` | `loai_dieu_chinh` | tên lệch — §12-Q9 file gốc |
| `dienGiai` | `mo_ta` | tên lệch |
| `hoaDon.mauSoHoaDon` (chuỗi mã) | `mau_so_hoa_don_id` (uuid FK) | **mapper phải tra ngược** `mst_mau_so_hoa_don` theo mã; mã không tồn tại ⇒ 400 chứ không lưu `null` im lặng |
| `chiTiet[].soLuong/donGia/thanhTien` | cặp `*_tang` / `*_giam` | ghi vào khối theo `huongDieuChinhGia`; **khối còn lại để `NULL`**, không ghi 0 — `COALESCE(so_luong_tang, so_luong_giam)` của [DongChungTuPort.java:54](../../cell-app/src/main/java/vn/dopai/pmkt/cell/quan_he_chung_tu/api/DongChungTuPort.java) sẽ đọc nhầm khối 0 |

## 4. Công thức tính (server là nguồn sự thật)

Cài trong `TinhToanDieuChinhGia`, chạy ở hook `truocKhiLuu` của template.

**Từng dòng** (SCR dòng 444-465, BR7 làm tròn 2 chữ số ở kết quả cuối):
```
thanhTien            = soLuong × donGia                       (dòng dịch vụ: nhập tay, giữ nguyên)
chietKhauTien        = chietKhauPhanTram × thanhTien / 100    (nếu client gửi tiền CK → tính ngược %)
tienThueGtgt         = (thanhTien − chietKhauTien) × thueSuat  ; KCT/KKKNT/KHAC-0% ⇒ 0
thanhTienQuyDoi      = thanhTien      × tyGia                  (BR18.2)
chietKhauTienQuyDoi  = chietKhauTien  × tyGia
tienThueGtgtQuyDoi   = tienThueGtgt   × tyGia
```

**Tổng header** (SCR dòng 506-514) → ghi vào 6 cột tổng đã có + 4 cột quy đổi mới:
```
tongTienHang            = Σ thanhTien            → tong_tien_hang_chenh_lech
tongChietKhau           = Σ chietKhauTien        → tong_tien_chiet_khau_chenh_lech
tongTienTruocThue       = tongTienHang − tongChietKhau         → tong_tien_truoc_thue_chenh_lech
tongTienThueGtgt        = Σ tienThueGtgt         → tong_tien_thue_gtgt_chenh_lech
tongTienSauThue         = tongTienTruocThue + tongTienThueGtgt → tong_tien_sau_thue_chenh_lech
tongTienThanhToan       = tongTienSauThue                      → tong_thanh_toan_chenh_lech
tong*QuyDoi             = tong* × tyGia                        → 4 cột mới (§9.2)
```

**Làm tròn (BR7.2):** làm tròn thương mại (HALF_UP) đến 2 chữ số **ở kết quả cuối của mỗi phép**, không làm tròn trung gian; lưu giá trị đã làm tròn theo đúng scale của domain DB (`money_vnd numeric(18,2)`).

**Dấu:** mọi số lưu **dương** ở cả hai hướng — hướng Tăng/Giảm quyết định vế Nợ/Có của bút toán, không quyết định dấu. Hiển thị số âm cho hóa đơn điều chỉnh giảm là việc của màn Hóa đơn điều chỉnh (SCR dòng 622-626), không phải cột lưu trữ.

## 5. Validation — ma trận đầy đủ

| # | Luật | Thời điểm kiểm | Thông báo (nguyên văn) | Mã | BR nguồn |
|---|---|---|---|---|---|
| V1 | `@NotNull`/`@NotBlank` trên request | `kiemTraDauVao` (bean validation, template gọi trước mọi thứ) | theo từng field | `_101`/`_102`/`_107`/`_110` | BR15.1 |
| V2 | `soChungTu` ≤ 50 ký tự, không dấu tiếng Việt | `kiemTraDauVao` | Số chứng từ không được để trống | `_101` | BR20.2 |
| V3 | `soChungTu` chưa tồn tại trong tenant (trừ chính nó khi sửa) | `kiemTraNghiepVu` | Số chứng từ đã tồn tại, vui lòng nhập số khác | `_109` | BR19.1 |
| V4 | `ngayChungTu ≤` hôm nay | `kiemTraNghiepVu` | Ngày chứng từ không hợp lệ | `_103` | SCR dòng 574 |
| V5 | `ngayHachToan ≥ ngayChungTu` | `kiemTraNghiepVu` | Ngày hạch toán không được nhỏ hơn ngày chứng từ | `_205` | BR15.3, BR37 |
| V6 | `ngayHachToan` thuộc kỳ mở | **kernel** — `GhiSoApi.ghiSo` khi ghi sổ; `kiemTraKyMo` khi lưu nháp ([ChungTuTemplate.java:512](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)) | Ngày hạch toán không thuộc kỳ kế toán đang mở | `_203` | BR17.1 |
| V7 | `chiTiet` ≥ 1 dòng | `kiemTraNghiepVu` | Vui lòng nhập ít nhất một dòng chi tiết điều chỉnh | `_104` | SCR dòng 600 |
| V8 | `soLuong > 0` **trừ** dòng dịch vụ (`soLuong == 0 && donGia == 0 && thanhTien != 0`) | `kiemTraNghiepVu` | Số lượng phải lớn hơn 0 | `_105` | SCR dòng 582 **vs** BR2/BR3 — §12-Q4 |
| V9 | `donGia > 0`, cùng miễn trừ V8 | `kiemTraNghiepVu` | Đơn giá phải lớn hơn 0 | `_106` | SCR dòng 583 |
| V10 | `TangGia` ⇒ mọi dòng có `taiKhoanDoanhThuId`; `GiamGia` ⇒ mọi dòng có `taiKhoanGiamGiaId` | `kiemTraNghiepVu` | *(chưa có mã)* dùng `MSG_COMMON_001` | — | BR8 (SCR dòng 472-477) |
| V11 | Mọi dòng có `taiKhoanCongNoId` và `taiKhoanThueGtgtId` | `kiemTraNghiepVu` | *(chưa có mã)* `MSG_COMMON_001` | — | SCR dòng 448, 464 |
| V12 | `lapKemHoaDonDieuChinh = true` ⇒ `hoaDon.hoaDonGocId != null` | `kiemTraNghiepVu` | Bạn cần chọn hóa đơn gốc trên tab Hóa đơn | `_206` | SCR dòng 406, 586 |
| V13 | `lapKemHoaDonDieuChinh = true` ⇒ `hoaDon.loaiDieuChinh != null` | `kiemTraNghiepVu` | Vui lòng chọn loại điều chỉnh trên tab Hóa đơn | `_207` | SCR dòng 579 |
| V14 | `lapKemHoaDonDieuChinh = true` ⇒ `hoaDon.lyDoDieuChinh` không rỗng | `kiemTraNghiepVu` | Vui lòng nhập lý do điều chỉnh | `_110` | SCR dòng 580 |
| V15 | `thanhToanNgay = true` ⇒ `hinhThucThanhToan` thuộc đúng nhóm của hướng điều chỉnh (BR6) và `chungTuThanhToan.soChungTu`, `.taiKhoanTienId` không rỗng | `kiemTraNghiepVu` | *(chưa có mã)* `MSG_COMMON_001` | — | SCR BR6 dòng 269-274 |
| V16 | `chungTuNguonId`/`chiTietNguonId` (nếu có) trỏ tới dòng **tồn tại, chưa xoá, đã ghi sổ** | `kiemTraNghiepVu` | Chứng từ gốc không tồn tại | `_204` | UC_ThemMoi luồng phụ |
| V17 | `nguonChungTu = HOA_DON_DIEU_CHINH` ⇒ `lapKemHoaDonDieuChinh = false` | `kiemTraNghiepVu` (server ép về false, không ném lỗi) | — | — | SCR dòng 217 |
| V18 | `thueSuatGtgt = KHAC` ⇒ `giaTriThueGtgt != null` | `kiemTraNghiepVu` | *(chưa có mã)* `MSG_COMMON_001` | — | BR11 CTBH |
| V19 | `tyGia > 0`; loại tiền = tiền hạch toán ⇒ `tyGia = 1` | `kiemTraNghiepVu` | *(chưa có mã)* `MSG_COMMON_001` | — | BR18.1 |
| V20 | Khoá lạc quan (`updatedAt`) — **chỉ ở luồng sửa**, xem [04](04-chinh-sua.md) | — | Dữ liệu đã được cập nhật bởi người dùng khác… | 409 `STALE_DATA` | BR12 |

⚠ **Bảy luật (V10, V11, V15, V18, V19 và hai luật phụ) không có mã message riêng trong `6.messages.md`.** Dùng `MSG_COMMON_001` ("Thao tác không hợp lệ với trạng thái hiện tại của chứng từ/phiếu" — BR16.1) là **giải pháp tạm và không đúng nghĩa**; đề nghị BA cấp mã. Bổ sung vào §12 file gốc khi có phản hồi.

## 6. Luồng xử lý

```
POST /  →  DieuChinhGiaHangBanController.create
        →  quyen.require(DieuChinhGiaHangBan, Create)
        →  DieuChinhGiaHangBanCrudService.create(request)
        →  TaoDieuChinhGia (extends LuuDieuChinhGiaTemplate extends ChungTuTemplate).thucThi
```

Bên trong `ChungTuTemplate.thucThi` — luồng TAO ([:149](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)), **thứ tự do base cưỡng chế, module chỉ cài hook**:

| Bước base | Module cài gì |
|---|---|
| `kiemTraDauVao` | (mặc định) bean validation → V1, V2 |
| `kiemTraQuyen` | (mặc định) `DieuChinhGiaHangBan.Create` |
| `chuanBiChungTu` | nạp danh mục cần tra (mẫu số hóa đơn, tài khoản), nạp dòng nguồn theo `chiTietNguonId` |
| `kiemTraNghiepVu` | **`KiemTraDieuChinhGia`** → V3…V19 |
| `truocKhiLuu` | **`TinhToanDieuChinhGia`** (§4) + chốt `status = NHAP`, `hinh_thuc_thanh_toan` khi không thanh toán ngay |
| `luuEntity` | ghi header + chi tiết (cascade), gọi `ctx.ghiNhanChungTu(id, soChungTu, ngayChungTu, ngayHachToan)` — **bắt buộc**, thiếu là `IllegalStateException` |
| `sauKhiLuu` | **`LienKetNguonDieuChinhGia`** → `QuanHeChungTuApi.lienKet(...)` (D4) · và khi `ghiSo=true`: **`DinhKhoanDieuChinhGia`** dựng `List<DinhKhoan>` gắn `voiChiTiet(chiTietId)` — id dòng chỉ có sau bước lưu |
| `coGhiSoNgay` | `return request.ghiSo() == Boolean.TRUE` |
| `phanGhiSo` / `luuKhongGhiSo` | (base) — `ghiSo=true` ⇒ `GhiSoApi.ghiSo`; `false` ⇒ `kiemTraKyMo` (V6) và **cấm** để lại định khoản nào |
| `ghiNhatKyTacDong` | (mặc định) một dòng `aud_audit_log`, trong transaction |
| `bangGoc()` | `"sal_chung_tu_dieu_chinh_gia_hang_ban"` |
| `maLoaiChungTu()` | `"CTDG"` (D11 — §12-Q1) |
| `coSinhButToan()` | `true` |
| `coAnhHuongTonKho()` | **`false`** — comment của bảng ghi rõ *"CÓ hạch toán, KHÔNG di chuyển tồn kho"* ([V1:16334](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)) |

Bút toán khi `ghiSo = true`: xem [06-ghi-so.md §4](06-ghi-so.md) — **cùng một lớp `DinhKhoanDieuChinhGia`**, không viết hai bản.

## 7. Tương tranh & transaction

- Toàn bộ là **một** `@Transactional` do `ChungTuTemplate.thucThi` mở ([:102](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)) — thoả "Ràng buộc nguyên tử" của UC_GhiSo trong phạm vi đã chốt ở D3.
- Luồng TAO **không khoá chứng từ**: bản ghi chưa tồn tại, kernel tự khoá theo id mới lúc ghi sổ.
- Dòng nguồn **được khoá** qua `DongChungTuPort.khoaVaLaySoLuong` bên trong `QuanHeChungTuApi.lienKet` (`ORDER BY id FOR UPDATE`) — chống hai người cùng lập chứng từ trên cùng dòng nguồn.
- **Idempotency:** trùng số chứng từ bị chặn bởi unique `uq_sal_dcg_so_ct`; bấm Lưu hai lần nhanh ⇒ lần sau 400 `_109` chứ không sinh hai chứng từ. Ghi sổ idempotent theo nội dung ở kernel ([GhiSoApi.java:31](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/hach_toan/api/GhiSoApi.java)).

## 8. Kiểm thử

### Unit (`@Tag("unit")`)
| Lớp test | Kiểm gì |
|---|---|
| `TinhToanDieuChinhGiaTest` | 6 công thức dòng + 6 tổng header; làm tròn HALF_UP 2 chữ số ở kết quả cuối; `tyGia = 1` ⇒ quy đổi = gốc; số FE gửi sai bị **ghi đè** |
| `KiemTraDieuChinhGiaTest` | 20 ca của ma trận §5, mỗi ca một mã lỗi + messageId; đặc biệt **V8/V9 miễn trừ dòng dịch vụ** (`SL=0, ĐG=0, TT≠0` ⇒ pass) |
| `DinhKhoanDieuChinhGiaTest` | xem [06](06-ghi-so.md) |
| `LuuDieuChinhGiaMapperTest` | ghi đúng khối `*_tang` / `*_giam`, khối kia `NULL`; `mauSoHoaDon` tra ngược ra id; `khongTongHopToKhaiGtgt` bị ép `true` với `KHAC`/`KKKNT` |
| `TaoDieuChinhGiaHookTest` | `coGhiSoNgay` đọc từ **lệnh** chứ không từ entity; `maLoaiChungTu = "CTDG"`; `coAnhHuongTonKho = false` |

### Tích hợp (cần Docker)
| Lớp test | Kiểm gì |
|---|---|
| `TaoDieuChinhGiaIT` | `ghiSo=false` ⇒ 0 dòng `acc_so_cai`, `status = NHAP` · `ghiSo=true` ⇒ đủ dòng sổ cái, `status = DA_GHI_SO`, `nguoi_ghi_so`/`thoi_gian_ghi_so` có giá trị · trùng `soChungTu` ⇒ 400 `_109` · kỳ khoá ⇒ 400 `_203` và **không** còn dòng nào (rollback) · liên kết `ctu_quan_he_chung_tu` sinh đúng số dòng nguồn |

## 9. BR đã áp dụng
BR7 (§4 làm tròn + precision) · BR10 chọn nguồn (§2 các field `nguon*`) · BR15 (§5) · BR16 (`MSG_COMMON_001`) · BR17 (V6) · BR18 (§4 quy đổi) · BR19 (V3) · BR20 (V2) · BR21 (`thuTu`) · BR25 (quyền `.Create`) · BR28 (RLS) · BR36 (không gộp bút toán — [06](06-ghi-so.md)) · BR37 (V5) · BR43 (trim ở bean validation) · BR46 (audit do base ghi).
