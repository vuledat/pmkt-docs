# F3 — Xem chi tiết Hóa đơn bán hàng

| | |
|---|---|
| **Mã chức năng** | `F3` |
| **UC nguồn** | `PMKT-U-06466` — [`UC_HDBanHang_ChiTiet.md`](../../../pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/4.usecases/PMKT-U-06466_ChiTiet/UC_HDBanHang_ChiTiet.md) |
| **Màn hình nguồn** | `SCR_HDBanHang_ChiTiet.md` (readonly, tham chiếu trường của `SCR_HDBanHang_ThemMoi.md`) |
| **Endpoint phụ trách** | **A6** `GET /{id}` |
| **File gốc** | [`00-ke-hoach-tong.md`](00-ke-hoach-tong.md) |

---

## 1. Quyết định riêng của chức năng

| # | Quyết định | Trỏ về |
|---|---|---|
| F3-a | Override `AbstractCrudService.get(id)` để nạp **kèm dòng chi tiết** bằng `@EntityGraph`, không để lazy. | mẫu `ChungTuBanHangCrudService.java:106-117` — lazy sẽ ném `LazyInitializationException` khi mapper duyệt dòng ngoài transaction đọc |
| F3-b | Bản ghi **đã xóa mềm coi như không tồn tại** → 404 `_012`, không trả dữ liệu. | mẫu `BanHangSupport.java:83-91` |
| F3-c | `GET /{id}` là **endpoint duy nhất** cho cả màn Xem chi tiết (F3) và màn Cập nhật (F4 nạp dữ liệu). Không tách 2 endpoint. | `SCR_HDBanHang_CapNhat.md:12,16-17` — hai màn cùng bố cục, cùng bộ trường |
| F3-d | DTO chứa đủ **field cờ** để FE quyết định hiện nút "Cập nhật" và popup cảnh báo `_055`/`_056` — BE không tự phán quyết UI. | `SCR_HDBanHang_ChiTiet.md:25` · `SCR_HDBanHang_CapNhat.md:43` |

---

## 2. Hợp đồng API

### A6 — `GET /api/ban-hang/hoa-don-ban-hang/{id}`

**Quyền:** `LapHoaDonBan.View.Detail` (`BaseCrudController.java:139`) — đúng `UC_HDBanHang_ChiTiet.md:23`.

```jsonc
// Response 200 — ApiResponse<HoaDonBanHangDto>
{
  "data": {
    "id": "7f1c…",
    "loaiNghiepVu": "Bán hàng trong nước",

    // --- Thông tin hóa đơn ---
    "khachHangId": "9a03…", "tenKhachHang": "CÔNG TY TNHH ABC",
    "maSoThue": "0101234567", "nguoiMuaHang": "Nguyễn Văn A",
    "maSoDvqhns": "1234567", "cccd": "001199001234", "hoChieu": null,
    "soDienThoai": "0912345678", "diaChi": "Số 1 Trần Duy Hưng, Hà Nội",
    "nguoiLienHe": "Trần Thị B",
    "hinhThucThanhToan": "Chuyển khoản", "taiKhoanNganHangThuId": "c410…",
    "mauSoHoaDonId": "b21e…", "kyHieuHoaDon": "K26TAA",
    "ngayHoaDon": "2026-08-12", "soHoaDon": "0000123",
    "nhanVienBanHangId": "77aa…", "moTa": "Bán hàng theo hợp đồng 12/HĐKT",

    // --- Loại tiền / chiết khấu ---
    "loaiTienId": "0001…", "tyGia": 1.000000,
    "loaiChietKhau": "Theo mặt hàng", "giaTriChietKhau": 0,

    // --- Thông tin xuất khẩu (null khi bán trong nước) ---
    "soHopDong": null, "ngayHopDong": null, "diaDiemGiao": null,
    "diaDiemNhan": null, "soVanDon": null, "soContainer": null, "donViVanChuyen": null,

    // --- Trạng thái ---
    "trangThaiPhatHanh": "Chưa phát hành",
    "trangThaiLapChungTu": "Đã lập 1 phần",
    "trangThaiHoaDon": "Hóa đơn gốc",
    "chungTuBanId": null,

    // --- Tổng hợp tiền tệ ---
    "tongTienHangHoa": 8500000.00, "tongTienChietKhau": 425000.00,
    "tongTienChietKhauHang": 425000.00, "tongTienChietKhauHoaDon": 0.00,
    "tongTienThueGtgt": 807500.00, "tongTienThueXk": null,
    "tongTienSauThue": 8882500.00, "tongTienThanhToan": 8882500.00,
    "tongTienHangHoaQuyDoi": 8500000.00, "tongTienChietKhauQuyDoi": 425000.00,
    "tongTienThueGtgtQuyDoi": 807500.00, "tongTienThueXkQuyDoi": null,
    "tongTienSauThueQuyDoi": 8882500.00, "tongTienThanhToanQuyDoi": 8882500.00,

    // --- Field cờ điều khiển UI (§4) ---
    "choPhepSua": true,
    "choPhepXoa": true,
    "choPhepLapChungTuBanHang": true,
    "choPhepLapChungTuBanDichVu": false,
    "coDongDichVu": false,
    "daLapChungTu": true,
    "coHoaDonLienQuan": false,
    "hoaDonLienQuan": [],

    // --- Audit + lock ---
    "phienBan": 3,
    "ngayTao": "2026-08-12T02:10:00.000Z",
    "ngayCapNhat": "2026-08-13T04:11:02.451Z",

    "chiTiet": [
      {
        "id": "aa11…", "thuTu": 1, "loaiDongHang": true,
        "maHangId": "a1b2…", "tenHang": "Xi măng PC40", "dienGiai": "Xi măng PC40",
        "donViTinhId": "d001…",
        "soLuong": 100.000, "donGia": 85000.00, "donGiaQuyDoi": 85000.00,
        "thanhTien": 8500000.00, "thanhTienQuyDoi": 8500000.00,
        "hangKhuyenMai": false, "chietKhauThuongMai": false,
        "chietKhauPhanTram": 5.00, "chietKhau": 425000.00, "chietKhauQuyDoi": 425000.00,
        "chietKhauHangPhanTram": 5.00, "tienChietKhauHang": 425000.00,
        "tienChietKhauHangQuyDoi": 425000.00,
        "chietKhauHoaDonPhanTram": null, "tienChietKhauHoaDon": null,
        "tienChietKhauHoaDonQuyDoi": null,
        "thueSuatGtgtMacDinh": "10", "giaTriThueGtgt": null,
        "tienThueGtgt": 807500.00, "tienThueGtgtQuyDoi": 807500.00,
        "dienGiaiThue": "Thuế GTGT - Xi măng PC40", "khongTongHopToKhaiGtgt": false,
        "giaTriTinhThueXk": null, "giaTriTinhThueXkQuyDoi": null,
        "phanTramThueXk": null, "tienThueXk": null, "tienThueXkQuyDoi": null,
        "soLo": "L2608", "hanSuDung": "2027-08-12",
        "hopDongId": null, "donViId": null, "khoanMucChiPhiId": null, "vuViecId": null,
        "chungTuBanHangId": null, "chiTietChungTuBanHangId": null,
        "chungTuBanDichVuId": null, "chiTietChungTuBanDichVuId": null,
        "daLapChungTuTuDongNay": false,
        "soLuongDaLapChungTu": 0.000
      }
    ]
  },
  "message": null, "messageId": null
}
```

| Lỗi | HTTP | `code` | `messageId` | Nguồn |
|---|---|---|---|---|
| Thiếu quyền `.View.Detail` | 403 | `FORBIDDEN` | `MSG_PMKT-E-06196_011` | BR25.2 |
| HĐ không tồn tại **hoặc đã xóa mềm** | 404 | `NOT_FOUND` | `MSG_PMKT-E-06196_012` | `UC_HDBanHang_ChiTiet.md:38` |
| Lỗi tải dữ liệu | 500 | `INTERNAL_ERROR` | `MSG_PMKT-E-06196_013` | `UC_HDBanHang_ChiTiet.md:39` |

---

## 3. Ánh xạ cột BA ↔ DB ↔ DTO

Y hệt [02 §3](02-them-moi-hoa-don.md) — màn Chi tiết "tham chiếu **đầy đủ** tại SCR_HDBanHang_ThemMoi" (`SCR_HDBanHang_ChiTiet.md:15`). Khác biệt duy nhất theo `:18-19`:

| Điểm khác | Hệ quả lên BE |
|---|---|
| "Tất cả trường thông tin chỉ xem (readonly)" | **Không có** hệ quả BE — readonly là trạng thái UI. BE vẫn trả đủ mọi field. |
| "Không có các nút thao tác: Thêm dòng, Xóa dòng, Thêm ghi chú" | Không có hệ quả BE. |

**Ba field bổ sung chỉ có ở A6** (không có ở A1 để tránh phình query danh sách):

| Field | Nguồn | Dùng làm gì |
|---|---|---|
| `chiTiet[].daLapChungTuTuDongNay` | `QuanHeChungTuApi.theoNguon(SAL_HOA_DON_BAN_HANG, id)` (`QuanHeChungTuApi.java:57`) | FE tô màu / khóa dòng đã bị tiêu thụ |
| `chiTiet[].soLuongDaLapChungTu` | `QuanHeChungTuApi.daTieuThu(dongIds)` (`:54`) | hiển thị số lượng còn lại để lập tiếp |
| `hoaDonLienQuan` | query trên `sal_dieu_chinh_hoa_don_ban_hang` — xem [01 §8.5](01-xem-danh-sach-hoa-don.md) | BR07 màn danh sách, dùng lại ở màn chi tiết |

---

## 4. Field cờ điều khiển UI (F3-d)

| Nút / popup | Điều kiện BA | Field DTO | Công thức |
|---|---|---|---|
| Nút **Cập nhật** trên popup Chi tiết | "chỉ hiển thị khi Chưa phát hành" (`SCR_HDBanHang_ChiTiet.md:25`, `UC:41`) | `choPhepSua` | `trangThaiPhatHanh == CHUA_PHAT_HANH` |
| Nút **Xóa** | "Chưa phát hành" (BR01 danh sách) | `choPhepXoa` | `trangThaiPhatHanh == CHUA_PHAT_HANH` |
| Nút **Lập chứng từ bán hàng** | `trangThaiLapChungTu ∈ {Chưa lập, Đã lập 1 phần}` (BR04) | `choPhepLapChungTuBanHang` | `trangThaiLapChungTu != DA_LAP_DU` |
| Nút **Lập chứng từ bán dịch vụ** | như trên **và** có ≥1 dòng "Dịch vụ" (BR05) | `choPhepLapChungTuBanDichVu`, `coDongDichVu` | ⚠ ngoài phạm vi — [00 §12-Q6](00-ke-hoach-tong.md) |
| Popup cảnh báo **`_056`** khi mở form Sửa | HĐ có `trangThaiLapChungTu ∈ {Đã lập 1 phần, Đã lập đủ}` (`SCR_HDBanHang_CapNhat.md:40-45`) | `daLapChungTu` | `trangThaiLapChungTu != CHUA_LAP` |
| Popup cảnh báo **`_055`** khi bấm Xóa | như trên (`SCR_HDBanHang_Xoa.md:81`) | `daLapChungTu` | như trên |
| Nút **Đóng** | luôn (BR3) | — | FE |

**BE không tự chặn theo cờ này** — cờ chỉ để FE dựng UI. Việc **chặn thật** nằm ở A7/A8 (xem [04](04-cap-nhat-hoa-don.md), [05](05-xoa-hoa-don.md)): người dùng gọi thẳng API vẫn phải bị chặn.

---

## 5. Validation

Chỉ một luật: **id tồn tại, chưa xóa mềm, thuộc tenant hiện tại**.

| # | Luật | Cài ở | messageId |
|---|---|---|---|
| V01 | `id` là UUID hợp lệ | Spring `@PathVariable UUID` | 400 (base) |
| V02 | Bản ghi tồn tại, `da_xoa = false`, thuộc tenant (RLS) | `HoaDonBanSupport.nap(id)` | 404 `_012` |

RLS `tenant_isolation` (`V1__baseline.sql:31708`) đã chặn truy cập chéo tenant ở tầng DB — request tenant khác nhận **404**, không phải 403. Đây là hành vi đúng (không tiết lộ sự tồn tại của bản ghi).

---

## 6. Luồng xử lý

```
1. Controller.get(id)   ← BaseCrudController.java:137, quyen.require(…, VIEW_DETAIL)
2. HoaDonBanHangCrudService.get(id)   @Transactional(readOnly = true)   ← override, F3-a
   2.1 HoaDonBanSupport.nap(id)
         repository.findWithChiTietById(id)      @EntityGraph — 1 query, không N+1
           .filter(hd -> !hd.isDaXoa())
           .orElseThrow(() -> ApiException.notFound(KHONG_TIM_THAY, MSG_KHONG_TIM_THAY, …))
   2.2 quanHe.theoNguon(SAL_HOA_DON_BAN_HANG, id)    → daLapChungTuTuDongNay
   2.3 quanHe.daTieuThu(chiTietIds)                  → soLuongDaLapChungTu
   2.4 query phụ sal_dieu_chinh_hoa_don_ban_hang     → hoaDonLienQuan
   2.5 HoaDonBanMapper.toDto(entity, …)              + 7 field cờ
3. ApiResponse.ok(dto)   — message/messageId = null (đọc thành công không cần toast, BR26)
```

Tổng **4 query** cho một lần gọi: header+chi tiết (1), quan hệ theo nguồn (1), số lượng đã tiêu thụ (1), hóa đơn liên quan (1). Không có N+1.

---

## 7. Tương tranh & transaction

`@Transactional(readOnly = true)` bao trọn từ `nap()` tới `toDto()` — bắt buộc, nếu không `chiTiet` lazy sẽ nổ ngoài transaction (F3-a).

**`ngayCapNhat` trong response là token optimistic-lock** — FE giữ và gửi lại ở `PUT /{id}` và `DELETE /{id}` (`DeleteRequest.updatedAt`). Lệch → 409 `STALE_DATA` (mẫu `BanHangSupport.java:120-130`). `phienBan` cũng trả về nhưng chỉ để debug; chốt chặn thật là `@Version` ở tầng JPA.

---

## 8. Kiểm thử

### 8.1 Unit (`@Tag("unit")`)

| Lớp test | Case |
|---|---|
| `HoaDonBanMapperTest` | `choPhepSua`/`choPhepXoa` = `true` khi `Chưa phát hành`, `false` khi `Đã phát hành` |
| | `daLapChungTu` = `false` **chỉ** khi `trangThaiLapChungTu == CHUA_LAP` |
| | `choPhepLapChungTuBanHang` = `false` **chỉ** khi `DA_LAP_DU` |
| | Dòng ghi chú (`loaiDongHang=false`) map ra DTO giữ `tenHang`, các cột số `null` |
| | `chiTiet` trả **đúng thứ tự `thuTu` tăng dần** dù entity trả về theo thứ tự khác |
| `HoaDonBanSupportTest` | `nap()` với bản ghi `daXoa=true` → ném `ApiException` 404 mã `_012` (F3-b) |

### 8.2 Tích hợp (cần Docker — R7)

| Lớp | Kiểm |
|---|---|
| `ChiTietHoaDonBanIT` | Nạp HĐ 5 dòng → **1 query** cho header+chi tiết (đếm bằng Hibernate statistics), không N+1 |
| | HĐ của tenant khác → 404, không 200 và không 403 |
| | HĐ đã xóa mềm → 404 `_012` |
| | `soLuongDaLapChungTu` khớp tổng liên kết trong `ctu_quan_he_chung_tu` |

---

## 9. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR3 | Nút Đóng/"x" luôn có — FE; BE không can thiệp |
| BR13.2 | §4 — nút Sửa/Xóa hiện theo trạng thái, qua field cờ |
| BR14.1 | Chế độ form "Xem" — readonly, BE trả đủ field |
| BR25 | Quyền `.View.Detail` |
| BR26 | Đọc thành công không trả `messageId` (không toast) |
| BR28 | RLS + 404 thay vì 403 khi khác tenant |
| BR29.1 | F3-b — bản ghi xóa mềm coi như không tồn tại |
| BR46 | Trả `phienBan`, `ngayTao`, `ngayCapNhat` cho FE |

**Không áp dụng:** BR1, BR2, BR11, BR31, BR39 (thuộc màn danh sách); BR12/BR17/BR36/BR37 (HĐ không hạch toán).
