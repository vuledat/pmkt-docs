# F2 — Xem chi tiết chứng từ trả lại hàng bán

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F2** |
| UC nguồn | `PMKT-U-06477` — ⚠ **không có thư mục `4.usecases/`**, chỉ có ở `README.md:64`; xem §12-Q4 file gốc |
| Màn hình | `5.screens/SCR_XemChiTietTraLaiHangBan.md` (36 dòng) + `Matrix/…/SCR_XemChiTietTraLaiHangBan_MaTranAnHien.md` |
| Endpoint phụ trách | **A4** `GET /{id}` · **A5** `GET /{id}/dong-chi-tiet` · **A6** `GET /{id}/thong-tin-hach-toan` |
| Quyền | `TraLaiHangBan.View.Detail` — cả ba (`BaseCrudController.java:137-141`, `BaseChungTuController.java:139-151`) |

## 1. Quyết định riêng

| # | Quyết định | Trỏ về |
|---|---|---|
| 1.1 | `GET /{id}` trả **một DTO duy nhất** dùng chung với danh sách, khác biệt là có `chiTiet[]` | §0-D7; mẫu `ChungTuBanHangDto.java:10-14` |
| 1.2 | Override `get(id)` để nạp `@EntityGraph` **kèm** dòng chi tiết, không để lazy | mẫu `ChungTuBanHangCrudService.java:106-117` |
| 1.3 | Tab Hạch toán trên popup Xem = bút toán **DỰ KIẾN** (tính lại từ dữ liệu chứng từ), khác A6 = `acc_so_cai` **thật** | `BaseChungTuController.java:129-137` |
| 1.4 | Popup Xem không có endpoint riêng — dùng chung A4 với popup Sửa; chế độ read-only là việc FE | `SCR_XemChiTietTraLaiHangBan.md:5-7` |

---

## 2. Hợp đồng API

### A4 — `GET /api/ban-hang/tra-lai-hang-ban/{id}`

```jsonc
// Response 200 — ApiResponse<TraLaiHangBanDto>
{
  "data": {
    "id": "0f5c…",

    /* ── Định danh chứng từ ─────────────────────────────── */
    "soChungTu": "CTTL-000012",
    "ngayChungTu": "2026-08-10",
    "ngayHachToan": "2026-08-10",
    "trangThaiChungTu": "CHUA_GHI_SO_PLACEHOLDER → thực tế: NHAP | CHO_DUYET | DA_DUYET | DA_GHI_SO | HUY",

    /* ── Nguồn (BR1 · BR5) ──────────────────────────────── */
    "nguonChungTu": "Chứng từ bán hàng hóa, dịch vụ",
    "chungTuBanHangId": "aa11…",
    "hoaDonBanHangId": null,

    /* ── Hàng tùy chọn nghiệp vụ ────────────────────────── */
    "phuongThucLapHoaDon": "Người bán xuất hóa đơn điều chỉnh",
    "thanhToanNgay": false,
    "phuongThucThanhToan": null,
    "kiemPhieuNhapKho": true,
    "lapKemHoaDonDieuChinh": true,

    /* ── Tab Ghi giảm công nợ (= header chứng từ) ────────── */
    "khachHangId": "a1b2…",
    "tenKhachHang": "Công ty TNHH A",
    "maSoThue": "0101234567",
    "diaChi": "12 Trần Duy Hưng, Hà Nội",
    "nhanVienBanHangId": "b7c8…",
    "moTa": "Trả lại hàng bán cho Công ty TNHH A",

    /* ── Loại tiền & chiết khấu ─────────────────────────── */
    "loaiTienId": "vnd0…",
    "tyGia": 1.000000,
    "loaiChietKhau": "Không chiết khấu",
    "phanTramChietKhau": 0.00,

    /* ── Header phẳng của các tab chứng từ liên kết ──────── */
    "soPhieuNhapKho": "PNK-000045",
    "nguoiGiaoHang": "Nguyễn Văn A",
    "soPhieuChi": null,
    "nguoiNhan": null, "lyDoChi": null,
    "taiKhoanTienId": null, "taiKhoanChiTienId": null,
    "nguoiLinhTien": null, "soGiayTo": null, "ngayCap": null, "noiCap": null,
    "kemTheo": null, "chungTuGoc": null,

    /* ── Tab Hóa đơn ────────────────────────────────────── */
    "nguoiMuaHang": "Nguyễn Văn A", "maSoDvqhns": null,
    "cccd": null, "hoChieu": null, "soDienThoai": "0912345678",
    "hinhThucThanhToanHoaDon": "TM/CK",
    "taiKhoanNganHangThuId": null,
    "loaiDieuChinh": "Trả lại hàng bán",
    "lyDoDieuChinh": "Hàng sai quy cách",
    "laHoaDonDieuChinhSaiSot": false,
    "mauSoHoaDon": "1", "kyHieuHoaDon": "K26TAA", "soHoaDon": "00000123",
    "ngayHoaDon": "2026-08-10",
    "hoaDonCanDieuChinhId": "hd99…",

    /* ── Tổng tiền (đồng tiền hạch toán) ────────────────── */
    "tongTienHangQuyDoi": 10000000.00,
    "tongChietKhauQuyDoi": 500000.00,
    "tongTienThueGtgtQuyDoi": 950000.00,
    "tongTienThanhToanQuyDoi": 10450000.00,

    /* ── Nhãn dẫn xuất (xem 01 §4.1) ────────────────────── */
    "traLaiHang": "Qua kho",
    "hinhThucThanhToan": "Điều chỉnh công nợ",
    "soChungTuLienQuan": 0,

    /* ── Dòng chi tiết — CHỈ có ở endpoint này ──────────── */
    "chiTiet": [ /* … xem A5 … */ ],

    /* ── Tab Hạch toán: bút toán DỰ KIẾN (§4) ───────────── */
    "dinhKhoan": [
      { "nghiepVu": "Giảm trừ doanh thu",  "taiKhoanNoId": "tk5212…", "taiKhoanCoId": "tk131…", "soTien": 9500000.00, "dienGiai": "Trả lại hàng bán cho Công ty TNHH A" },
      { "nghiepVu": "Thuế GTGT đầu ra",     "taiKhoanNoId": "tk33311…","taiKhoanCoId": "tk131…", "soTien":  950000.00, "dienGiai": null },
      { "nghiepVu": "Nhập lại kho, giảm giá vốn", "taiKhoanNoId": "tk156…", "taiKhoanCoId": "tk632…", "soTien": 7000000.00, "dienGiai": null }
    ],

    /* ── Trường hệ thống (BR46) ─────────────────────────── */
    "phienBan": 3,
    "createdBy": "u1…", "createdAt": "2026-08-10T02:10:00Z",
    "updatedBy": "u1…", "updatedAt": "2026-08-10T03:12:44.512Z"
  },
  "message": null,
  "messageId": null
}
```

| Lỗi | HTTP | code | messageId |
|---|---|---|---|
| Không có quyền `.View.Detail` | 403 | `FORBIDDEN` | `MSG_PMKT-E-06469_007` |
| `id` không tồn tại / đã xoá mềm | 404 | `NOT_FOUND` | `MSG_PMKT-E-06469_008` |
| `id` không phải UUID | 400 | `BAD_REQUEST` | — (handler chung) |

> Bản ghi `da_xoa = true` **bị coi như không tồn tại** (mẫu `BanHangSupport.java:84-91`): nếu không, `GET` rò rỉ dữ liệu đã xoá và `PUT` sẽ hồi sinh nó âm thầm.

### A5 — `GET /{id}/dong-chi-tiet`

Trả `ApiResponse<List<ChiTietTraLaiHangBanDto>>` theo **đúng thứ tự hiển thị** (`thu_tu` tăng dần) — `BaseChungTuController.java:147-151`.

```jsonc
{
  "data": [
    {
      "id": "d001…",
      "thuTu": 1,
      "loaiDongHang": true,            // false = dòng ghi chú: chỉ tenHang có nghĩa, không tính toán, không sinh bút toán

      "maHangId": "vt01…",
      "tenHang": "Bàn gỗ A",
      "donViTinhId": "dvt01…",
      "soLo": "LOT-2608", "hanSuDung": "2027-08-01",
      "hangKhuyenMai": false,
      "chietKhauThuongMai": false,

      "khoId": "kho01…",              // chỉ có giá trị khi kiemPhieuNhapKho = true

      "soLuong": 2.000,
      "donGia": 5000000.00,
      "thanhTien": 10000000.00,
      "thanhTienQuyDoi": 10000000.00,

      "chietKhauPhanTram": 5.00,
      "chietKhau": 500000.00,
      "chietKhauQuyDoi": 500000.00,

      "taiKhoanKhoId": "tk156…",
      "taiKhoanGiaVonId": "tk632…",
      "taiKhoanTraLaiId": "tk5212…",
      "taiKhoanCongNoId": "tk131…",

      "thueSuatGtgt": "10",
      "giaTriThueGtgt": null,          // chỉ dùng khi thueSuatGtgt = "KHAC"
      "taiKhoanThueGtgtId": "tk33311…",
      "tienThueGtgt": 950000.00,
      "tienThueGtgtQuyDoi": 950000.00,
      "tinhChatThueGtgtId": "tc01…",
      "khongTongHopToKhaiGtgt": false,

      "giaTrungBinh": true,           // "Tự động áp giá" — DB lưu cột NGHỊCH ĐẢO tu_nhap_don_gia_von, xem §3
      "donGiaVon": 3500000.00,
      "giaVon": 7000000.00,
      "soPhieuXuatId": null,

      "hopDongId": null, "donViId": null, "khoanMucChiPhiId": null, "vuViecId": null,

      "chiTietChungTuBanHangId": "ct01…",
      "soChungTuBanHang": "CTBH-000201",
      "soHoaDon": "00000098"
    }
  ]
}
```

### A6 — `GET /{id}/thong-tin-hach-toan`

Trả `ApiResponse<List<DongSoCaiDto>>` = các dòng **`acc_so_cai` ĐÃ GHI** của chứng từ (`BaseChungTuController.java:139-144`).

- Chứng từ **chưa ghi sổ** → `data: []`. Đó là **trạng thái hợp lệ**, không phải lỗi.
- Base gọi `service().kiemTraTonTai(id)` **trước** khi đọc sổ cái ⇒ một `id` bịa ra trả **404**, phân biệt được với chứng từ có thật mà chưa ghi sổ.

**Khác biệt A6 ⇄ `dinhKhoan[]` của A4** — hai thứ không được lẫn:

| | `A4.dinhKhoan[]` | `A6` |
|---|---|---|
| Là gì | Bút toán **DỰ KIẾN**, tính lại từ dữ liệu chứng từ mỗi lần đọc | Bản ghi kế toán **CHÍNH THỨC** trong `acc_so_cai` |
| Có khi chưa ghi sổ | ✅ (tab Hạch toán của popup Thêm/Sửa cần) | ❌ rỗng |
| Nguồn | `DinhKhoanTraLai.dung(ct)` — bỏ qua nghiệp vụ thiếu tài khoản (`DinhKhoanBanHang.java:63-69`) | `SoCaiApi.theoChungTu(id)` |
| Đơn vị tiền | đồng tiền hạch toán | đồng tiền hạch toán + phần nguyên tệ |

---

## 3. Ánh xạ cột BA ↔ DB ↔ DTO — những chỗ LỆCH

Bảng đầy đủ ở [11-thiet-ke-db.md §7](11-thiet-ke-db.md). Sáu chỗ tên lệch, đây là nguồn lỗi map số 1:

| # | Nhãn BA | Field FE / DTO | Cột DB thật | Ghi chú |
|---|---|---|---|---|
| 1 | Diễn giải (header) | `moTa` | `mo_ta` | BA gọi "Diễn giải" (`SCR:300`), DB/FE gọi `moTa`. **Giữ `moTa`** — FE đã code (`api/model.ts:111-112`) |
| 2 | Mã hàng | `maHangId` | `hang_hoa_id` | DB đặt `hang_hoa_id` (`V1:16638`), FE gửi `maHangId`. Mapper dịch; **không** đổi tên cột |
| 3 | Tên hàng | `tenHang` | `ten_hang` | khớp |
| 4 | Tự động áp giá | `giaTrungBinh` (boolean) | `tu_nhap_don_gia_von` (boolean) | **NGHỊCH ĐẢO nhau**: `giaTrungBinh = !tu_nhap_don_gia_von`. BA: *"Khi Tự động áp giá = UnChecked, cho phép người dùng sửa đơn giá nhập"* (`SCR:643`) ⇒ "tự nhập giá vốn" = "không tự động áp giá". Mapper phải đảo, **có unit test riêng** |
| 5 | Giá vốn | `giaVon` | `gia_von` | = `soLuong × donGiaVon` |
| 6 | Tỷ lệ CK (%) header | `phanTramChietKhau` | `gia_tri_chiet_khau` | DB đặt tên chung `gia_tri_chiet_khau` (dùng cho cả % và số tiền tuỳ `loai_chiet_khau`), FE gửi `phanTramChietKhau`. **Xem [11 §2](11-thiet-ke-db.md)** — đề xuất thêm cột `ty_le_chiet_khau` riêng để hai nghĩa không dùng chung một cột |

Cột **dẫn xuất/tính toán** (không đọc thẳng từ DB):

| Field DTO | Công thức | Nguồn |
|---|---|---|
| `traLaiHang` | `kiemPhieuNhapKho ? "Qua kho" : "Không qua kho"` | [01 §4.1](01-xem-danh-sach.md) |
| `hinhThucThanhToan` | `thanhToanNgay ? "Hoàn tiền ngay" : "Điều chỉnh công nợ"` | [01 §4.1](01-xem-danh-sach.md) |
| `soChungTuLienQuan` | `COUNT` chứng từ con đang liên kết = `(phieu_nhap_kho_id ≠ null) + (phieu_chi_id ≠ null) + (dieu_chinh_hoa_don_ban_hang_id ≠ null)` | `api/model.ts:181-182`; BR19 bộ chứng từ (`README.md` §BR19). Đợt 1 **luôn = 0** (D6) |
| `chiTiet[].thanhTien` | `soLuong × donGia` | `SCR:470` |
| `chiTiet[].tienThueGtgt` | `(thanhTien − chietKhau) × thueSuat%` | `SCR:473` |
| `chiTiet[].giaVon` | `soLuong × donGiaVon` | `SCR:462` |
| `chiTiet[].*QuyDoi` | `<gốc> × tyGia` | `SCR:469,471,474`; BR18 |
| `dinhKhoan[]` | xem [10](10-hach-toan-va-chung-tu-kem.md) | `UC_GhiSo:541-558` |

---

## 4. Validation

Chỉ đọc — không có validate nghiệp vụ. Ba chốt chặn:

| # | Luật | Điều kiện | Thời điểm | Kết quả | BR |
|---|---|---|---|---|---|
| V1 | Quyền | thiếu `.View.Detail` | đầu handler, `quyen.require(...)` | 403 · `_007` | BR25 |
| V2 | Tồn tại | không thấy / `da_xoa = true` | `TraLaiSupport.nap(id)` | 404 · `_008` | BR29.1 |
| V3 | Tenant | — | `@Transactional` + `TenantRlsAspect` | RLS lọc | BR28 |

---

## 5. Luồng xử lý

1. `quyen.require("TraLaiHangBan", QuyenChecker.VIEW_DETAIL)` — base làm (`BaseCrudController.java:139`).
2. `TraLaiHangBanCrudService.get(id)` (**override**) → `TraLaiSupport.nap(id)`:
   - `repository.findWithChiTietById(id)` — `@EntityGraph` nạp `chiTiet` **trong** transaction;
   - `.filter(ct -> !ct.isDaXoa())`;
   - `.orElseThrow(() -> ApiException.notFound(MaLoiTraLaiHangBan.KHONG_TIM_THAY, MSG_..._008, "Không tìm thấy chứng từ trả lại hàng bán"))`.
3. `TraLaiMapper.toDto(ct)`:
   - map header + `chiTietTheoThuTu()` (sắp theo `thu_tu`);
   - tính 3 nhãn dẫn xuất (§3);
   - `dinhKhoan = DinhKhoanTraLai.sangDto(DinhKhoanTraLai.dung(ct))` — **không** ném lỗi khi thiếu tài khoản (`DinhKhoanBanHang.java:63-69`), vì tab Hạch toán còn phục vụ chứng từ đang nhập dở.
4. Trả `ApiResponse.ok(dto)` — không `message`/`messageId` (đọc thành công không cần thông báo).

**Vì sao override `get` mà không dùng của base**: `AbstractCrudService.get` nạp header rồi để `chiTiet` lazy; lúc mapper duyệt dòng thì đã ra ngoài transaction đọc ở một số luồng gọi → `LazyInitializationException`. Nạp thẳng bằng `@EntityGraph` vừa an toàn vừa bỏ được một truy vấn phụ (lý do nguyên văn: `ChungTuBanHangCrudService.java:106-111`).

---

## 6. Tương tranh & transaction

| Endpoint | Transaction | Ghi chú |
|---|---|---|
| A4 | `@Transactional(readOnly = true)` | bắt buộc — GUC tenant bind theo transaction |
| A5 | `@Transactional(readOnly = true)` | như trên |
| A6 | base gọi `kiemTraTonTai(id)` (đã `@Transactional(readOnly = true)`, `AbstractChungTuCrudService.java:85-88`) rồi `soCai.theoChungTu(id)` | hai truy vấn, không cần khoá |

Không khoá gì. `updatedAt` trong DTO là **token** cho A8/A9 dùng sau (`api/model.ts:187-188`) — trả về ở đây chính là cách FE lấy token.

---

## 7. Kiểm thử

### 7.1 Unit

| Lớp test | Case | Input → kỳ vọng |
|---|---|---|
| `TraLaiMapperTest` | `giaTrungBinh` nghịch đảo | `tu_nhap_don_gia_von = true` → `giaTrungBinh = false`; `null` → `giaTrungBinh = true` |
| | thứ tự dòng | chi tiết `thu_tu = 3,1,2` → DTO trả 1,2,3 |
| | dòng ghi chú | `loaiDongHang = false` → không tham gia `dinhKhoan[]`, `soLuong`/`donGia` giữ nguyên giá trị đã lưu |
| | `soChungTuLienQuan` | 3 id con `null` → 0; có `phieu_nhap_kho_id` → 1 |
| | quy đổi | `tyGia = 24000`, `thanhTien = 100` → `thanhTienQuyDoi = 2400000` |
| `TraLaiSupportTest` | soft-delete | `da_xoa = true` → ném 404 `_008`, **không** trả DTO |
| `DinhKhoanTraLaiTest` | thiếu tài khoản | dòng thiếu `taiKhoanTraLaiId` → nghiệp vụ đó **bị bỏ qua**, không ném lỗi |

### 7.2 Tích hợp (cần Docker — chưa chạy được)

| Lớp | Kiểm gì |
|---|---|
| `TraLaiHangBanDetailIT` | `GET /{id}` nạp `chiTiet` **không** `LazyInitializationException`; đếm số truy vấn = 1 (không N+1) |
| | A6 chứng từ chưa ghi sổ → `data: []`; id bịa → 404 |
| | A6 chứng từ đã ghi sổ → số dòng `acc_so_cai` = 2 × số định khoản (kernel tách mỗi định khoản thành 2 dòng, `DinhKhoan.java:9-12`) |

---

## 8. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR3 popup | Popup Xem dùng chung trường với popup Thêm mới (`SCR_XemChiTiet:5-6`) ⇒ **một** DTO, không tạo endpoint riêng |
| BR7 precision | `tyGia` `decimal(18,6)`, tiền `(18,2)`, ngoại tệ `(18,4)`, SL `(18,3)` — [11 §4](11-thiet-ke-db.md) |
| BR12 trạng thái | `trangThaiChungTu` = tên hằng; FE dùng nó để chọn bộ nút (`SCR_XemChiTiet:19-21`) |
| BR13.2 nút trên form chi tiết | BE chỉ trả trạng thái + `soChungTuLienQuan`; **ẩn/hiện nút là việc FE** |
| BR18 ngoại tệ | các cột `*QuyDoi` (§3) |
| BR21 grid chi tiết con | `thu_tu` liên tục, A5 trả theo thứ tự đã lưu |
| BR24 tooltip | text tooltip (Mã số ĐVQHNS, CCCD) nằm ở FE i18n, **không** qua API |
| BR25 phân quyền | §4-V1 |
| BR28 multi-tenant | §4-V3 |
| BR29.1 xóa mềm | §4-V2 |
| BR34 sửa từ màn Xem | FE mở popup Sửa với chính DTO này; BE không có endpoint riêng |
| BR46 trường hệ thống | `phienBan`, `createdBy/At`, `updatedBy/At` trong DTO; `nguoiGhiSo`/`thoiGianGhiSo` **không** phơi ra wire (FE chưa cần — `api/model.ts` không khai) |
