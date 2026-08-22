# F6 — Lập Chứng từ bán hàng từ Hóa đơn

| | |
|---|---|
| **Mã chức năng** | `F6` |
| **UC nguồn** | `PMKT-U-06456` — [`UC_HDBanHang_DanhSach.md:41-46`](../../../pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/4.usecases/PMKT-u-06456_DanhSach/UC_HDBanHang_DanhSach.md) (luồng phụ "Lập chứng từ bán hàng") |
| **Màn hình nguồn** | `SCR_HDBanHang_DanhSach.md:72-79` (BR04) · `:79-86` (BR05 — ngoài phạm vi) |
| **Endpoint phụ trách** | **A10** `GET /{id}/du-lieu-lap-chung-tu` |
| **File gốc** | [`00-ke-hoach-tong.md`](00-ke-hoach-tong.md) |
| **Trạng thái** | ⬜ **CHƯA CÀI** — `LoaiChungTu.java:19` vẫn `SAL_CHUNG_TU_BAN_HANG(true, false)`, CHECK `ck_ctu_qhct_loai_dich` (`V1:7339`) vẫn thiếu; xác nhận lại 2026-08-21 |

> **Làm sau cùng** — phụ thuộc entity của F2 và migration mục 3 của [00 §7](00-ke-hoach-tong.md). Đây là chức năng **rủi ro nhất** của epic (R1, R2).

---

## 0. 🆕 BA đã viết lại BR18 của Chứng từ bán hàng (2026-08-20)

BR18 đổi tên thành *"Chứng từ kiêm — phiếu xuất kho, phiếu thu **và hóa đơn**"* và đổi bản chất: chứng từ kiêm nay **sinh bản ghi riêng** thay vì "tự đóng vai". Bảng mới (`SCR_CTBH_ThemMoi.md:996-1008`) khai đích danh chiều 1:

| Phần | Điều kiện | Bản ghi sinh ra | Liên kết ngược |
|---|---|---|---|
| **Hóa đơn** | `LapKemHoaDon = True` | `ENT_sal_hoa_don_ban_hang` + `ENT_sal_hoa_don_ban_hang_chi_tiet` | **`sal_hoa_don_ban_hang.ChungTuBanId`**; dòng: `sal_hoa_don_ban_hang_chi_tiet.ChiTietChungTuBanId` |

Ba điều rút ra:

1. ✅ **Cột `chung_tu_ban_id` của kế hoạch là đúng** — BA nay khai đích danh nó là khóa liên kết ngược. Cột đã có ở baseline ([00 §2.2](00-ke-hoach-tong.md)).
2. ✅ BR18 mục 8 khẳng định *"Hóa đơn **vẫn là chứng từ độc lập** vì mang giá trị pháp lý riêng… có **màn Xem chi tiết riêng** (PMKT-E-06196) và **vòng đời riêng**"* — củng cố D2/D3.
3. ⚠️ **Luật mới, chưa có trong kế hoạch:** *"Bỏ tích checkbox rồi Lưu lại → hệ thống **xóa bản ghi phần tương ứng**, với điều kiện phiếu đó đang **Chưa ghi sổ**"* (`SCR_CTBH_ThemMoi.md:1010`). Nghĩa là **module `chung_tu_ban_hang` được phép XÓA một hóa đơn** khi người dùng bỏ tích "Lập kèm hóa đơn". Hóa đơn không có trạng thái ghi sổ ⇒ điều kiện "Chưa ghi sổ" phải dịch sang cái gì? Xem §9-Q7.

---

## 1. Vấn đề: hai chiều liên kết ngược nhau (D11, R1)

| | Chiều 1 — **đã có** (PMKT-E-06194) | Chiều 2 — **F6, lần này** |
|---|---|---|
| Nguồn → Đích | Chứng từ bán hàng → Hóa đơn | Hóa đơn → Chứng từ bán hàng |
| Ai bấm nút | Người dùng ở màn CTBH, nút "Lập hóa đơn" | Người dùng ở màn HĐ, nút "Lập chứng từ bán hàng" |
| Counter | `sal_chung_tu_ban_hang_chi_tiet.so_luong_da_xuat_hd` (`chung_tu_ban_hang/internal/entity/ChiTietChungTuBanHang.java` (`so_luong_da_xuat_hd`)) | `ctu_quan_he_chung_tu` (không cột counter riêng) |
| Trạng thái suy ra | `sal_chung_tu_ban_hang.trang_thai_hoa_don` — enum `TrangThaiHoaDon` 3 giá trị (`chung_tu_ban_hang/internal/model/TrangThaiHoaDon.java`) | `sal_hoa_don_ban_hang.trang_thai_lap_chung_tu` — 3 giá trị (D8) |
| Điều kiện hiển thị nút | CTBH `Đã ghi sổ` **và** `TrangThaiLapHoaDon ∈ {Chưa lập, Đã lập một phần}` (`SCR_CTBH_ThemMoi.md:1472`) | HĐ `TrangThaiLapChungTu ∈ {Chưa lập, Đã lập 1 phần}` (`SCR_HDBanHang_DanhSach.md:73`) |
| Ràng buộc số lượng | `SoLuong_nhap ≤ SoLuong − SoLuongDaXuatHoaDon` (BR23 §5.2) | ⚠️ BA **không nói** — xem §9-Q1 |

**Hai chiều tồn tại đồng thời và không loại trừ nhau.** Một HĐ lập từ CTBH (chiều 1) về lý thuyết vẫn có thể là nguồn của một CTBH khác (chiều 2) — điều đó vô lý nghiệp vụ nhưng **không có gì trong dữ liệu chặn**. Xem §9-Q2.

---

## 2. Chặn kỹ thuật hiện tại (R2)

```java
// quan_he_chung_tu/api/LoaiChungTu.java:19
SAL_CHUNG_TU_BAN_HANG(true, false),   // laNguon = true, laDich = FALSE
```

⇒ `LenhLienKet.kiemTra()` sẽ **ném `IllegalArgumentException`** khi cố tạo liên kết có `loaiDich = SAL_CHUNG_TU_BAN_HANG` (`LenhLienKet.java:38`).

Và giá trị enum này **phải khớp chính xác** CHECK constraint `ck_ctu_qhct_loai_dich` ở DB; javadoc `LoaiChungTu.java:8-11` ghi rõ: *"Có test đồng bộ đọc `pg_constraint` để lệch là đỏ build — không có nó, thêm một loại chứng từ mới sẽ chỉ lộ lỗi ở production, lúc người dùng lập chứng từ."*

**Việc phải làm — hai thay đổi đi cùng MỘT commit:**

| # | Thay đổi | File |
|---|---|---|
| 1 | `SAL_CHUNG_TU_BAN_HANG(true, false)` → `(true, true)` | `quan_he_chung_tu/api/LoaiChungTu.java:19` |
| 2 | `ALTER … DROP CONSTRAINT ck_ctu_qhct_loai_dich` + `ADD` lại kèm `'SAL_CHUNG_TU_BAN_HANG'` | migration `V1033` — [07 §5](07-thiet-ke-db.md) |

**Không sửa `laTieuThu()`.** `LoaiChungTu.java:58-71` phân loại theo *"quan hệ tới loại đích này có **lấy hàng đi khỏi** dòng nguồn không"*. Chứng từ bán hàng lập từ hóa đơn **có** lấy hàng đi (một hóa đơn 100 cái, lập chứng từ cho 60 thì còn 40) ⇒ phải nằm nhóm `true`. Nhưng đổi `SAL_CHUNG_TU_BAN_HANG` sang `laTieuThu = true` sẽ **ảnh hưởng chiều 1** (CTBH làm nguồn), nơi nó đang là `false`.

⚠️ **Đây là điểm cần đọc lại code trước khi sửa.** `laTieuThu()` đang được quyết định theo **loại đích**, không theo cặp (nguồn, đích) — nên một enum không diễn tả được cả hai vai trò của `SAL_CHUNG_TU_BAN_HANG`. Ba lựa chọn:

| | A — đổi `laTieuThu` sang `true` | B — thêm hằng enum riêng `SAL_CHUNG_TU_BAN_HANG_TU_HD` | **C (CHỌN) — không áp ràng buộc số lượng ở chiều 2** |
|---|---|---|---|
| Rủi ro | Đổi hành vi chiều 1 (CTBH làm nguồn của phiếu thu/điều chỉnh giá) — **có thể vỡ nghiệp vụ đang chạy** | Enum phình, CHECK constraint phình, hai hằng cùng trỏ một bảng | Không ràng buộc SL ⇒ về lý thuyết lập được chứng từ vượt số lượng hóa đơn |
| Bằng chứng BA | — | — | BA **không hề nêu** ràng buộc số lượng cho chiều 2 (`SCR_HDBanHang_DanhSach.md:72-79` chỉ nói auto-fill), khác hẳn chiều 1 vốn có BR23 rất chi tiết |
| Chốt an toàn | — | — | `TrangThaiLapChungTu` vẫn tính đúng (§5); nếu người dùng lập vượt thì trạng thái về `Đã lập đủ`, nút biến mất. Ghi vào §9-Q1 để BA quyết. |

---

## 3. Phạm vi thực tế của F6

BA (`SCR_HDBanHang_DanhSach.md:75-79`) chỉ nói:
> - Khi click vào nút, hệ thống mở màn hình Thêm mới Chứng từ bán hàng
> - **Tự động fill thông tin từ hóa đơn bán hàng sang chứng từ bán hàng:**
>   - Thông tin khách hàng: Mã khách hàng, Tên khách hàng, Địa chỉ, Điện thoại, Mã số thuế
>   - Thông tin mặt hàng: Fill tất cả các dòng hàng từ hóa đơn
>   - Các thông tin khác: Diễn giải, Ghi chú (nếu có)

⇒ **Việc lưu chứng từ vẫn do endpoint của module `chung_tu_ban_hang` làm** (`POST /api/ban-hang/chung-tu-ban-hang`). F6 chỉ gồm 2 phần:

| Phần | Ai làm | Trạng thái |
|---|---|---|
| **6a** — cấp dữ liệu HĐ cho FE nạp vào form CTBH | module `hoa_don_ban_hang` — endpoint **A10** | ✅ trong phạm vi |
| **6b** — khi lưu CTBH có nguồn là HĐ: tạo liên kết + tính lại `TrangThaiLapChungTu` của HĐ | module `chung_tu_ban_hang` phải gọi `quanHe.lienKet(...)` với `loaiNguon = SAL_HOA_DON_BAN_HANG` | ⚠️ **phải sửa module `chung_tu_ban_hang`** — xem §6 |

---

## 4. Hợp đồng API

### A10 — `GET /api/ban-hang/hoa-don-ban-hang/{id}/du-lieu-lap-chung-tu`

**Quyền:** `LapHoaDonBan.View.Detail`.
**Vì sao không dùng thẳng A6 (`GET /{id}`):** A6 trả DTO **theo hình dạng của hóa đơn**; FE sẽ phải tự dịch sang hình dạng request của CTBH và tự lọc dòng đã lập hết. Dịch ở FE là chỗ dễ sai và không test được ở BE. A10 trả **đúng hình dạng FE cần đổ vào form CTBH**, kèm số lượng còn lại từng dòng.

```jsonc
// Response 200
{
  "data": {
    "hoaDonBanHangId": "7f1c…",
    "soHoaDon": "0000123",
    "ngayHoaDon": "2026-08-12",
    "loaiNghiepVu": "TRONG_NUOC",
    "trangThaiLapChungTu": "DA_LAP_MOT_PHAN",

    // --- Thông tin khách hàng (BR04 gạch đầu dòng 1) ---
    "khachHangId": "9a03…",
    "tenKhachHang": "CÔNG TY TNHH ABC",
    "diaChi": "Số 1 Trần Duy Hưng, Hà Nội",
    "soDienThoai": "0912345678",
    "maSoThue": "0101234567",

    // --- Thông tin khác (BR04 gạch đầu dòng 3) ---
    "moTa": "Bán hàng theo hợp đồng 12/HĐKT",

    // --- Loại tiền (không có trong BR04 nhưng CTBH bắt buộc — §9-Q3) ---
    "loaiTienId": "0001…",
    "tyGia": 1.000000,

    // --- Thông tin mặt hàng (BR04 gạch đầu dòng 2) ---
    "dong": [
      {
        "chiTietHoaDonBanHangId": "aa11…",
        "thuTu": 1,
        "maHangId": "a1b2…",
        "tenHang": "Xi măng PC40",
        "donViTinhId": "d001…",
        "soLuong": 100.000,
        "soLuongDaLapChungTu": 40.000,
        "soLuongConLai": 60.000,
        "donGia": 85000.00,
        "thanhTien": 8500000.00,
        "chietKhauPhanTram": 5.00,
        "chietKhau": 425000.00,
        "thueSuatGtgtMacDinh": "MUC_10",
        "giaTriThueGtgt": null,
        "tienThueGtgt": 807500.00,
        "dienGiai": "Xi măng PC40",
        "dienGiaiThue": "Thuế GTGT - Xi măng PC40",
        "soLo": "L2608",
        "hanSuDung": "2027-08-12",
        "hopDongId": null, "donViId": null, "khoanMucChiPhiId": null, "vuViecId": null
      }
    ]
  },
  "message": null, "messageId": null
}
```

| Lỗi | HTTP | `code` | `messageId` |
|---|---|---|---|
| Thiếu quyền | 403 | `FORBIDDEN` | `MSG_PMKT-E-06196_011` |
| HĐ không tồn tại / đã xóa | 404 | `NOT_FOUND` | `MSG_PMKT-E-06196_012` |
| HĐ đã `Đã lập đủ` | 409 | `ALREADY_FULLY_USED` | ⚠️ chưa có mã — §9-Q4 |

**Dòng đã lập hết (`soLuongConLai = 0`) vẫn được trả về** kèm `soLuongConLai: 0`, không lọc bỏ. Lý do: FE hiển thị đủ dòng để người dùng thấy toàn cảnh hóa đơn, chỉ disable dòng hết số lượng. Nếu lọc ở BE, người dùng sẽ tưởng hóa đơn thiếu dòng.

**Không trả** các cột hạch toán (TK công nợ, TK doanh thu, Kho, giá vốn…) vì hóa đơn **không có** chúng ([02 §3.2](02-them-moi-hoa-don.md)). FE/CTBH tự auto-fill theo BR07 + BR16 của `SCR_CTBH_ThemMoi.md` khi người dùng chọn mã hàng. **Đây là điểm phải nói rõ với BA:** chứng từ lập từ hóa đơn **không kế thừa** được tài khoản/kho, người dùng vẫn phải nhập.

---

## 5. Tính `TrangThaiLapChungTu` của hóa đơn (D8)

Công thức (đã dùng ở [04 §4.3](04-cap-nhat-hoa-don.md)):

```
tongSoLuongDongHang = Σ soLuong của các dòng loaiDongHang = true
tongDaLapChungTu    = Σ quanHe.daTieuThu(chiTietHoaDonIds)     ← QuanHeChungTuApi.java:54

trangThaiLapChungTu =
    tongDaLapChungTu == 0                      → "Chưa lập"
    tongDaLapChungTu <  tongSoLuongDongHang    → "Đã lập 1 phần"
    tongDaLapChungTu >= tongSoLuongDongHang    → "Đã lập đủ"
```

Khớp nguyên văn BR02 (`SCR_HDBanHang_DanhSach.md:63-65`):
> - **"Chưa lập"**: Hóa đơn chưa được lập chứng từ (chưa được chọn vào bất kỳ CTBH/CTBDV nào)
> - **"Đã lập 1 phần"**: Tổng số lượng đã lập chứng từ < Tổng số lượng hàng hóa/dịch vụ trên hóa đơn
> - **"Đã lập đủ"**: Tổng số lượng đã lập chứng từ = Tổng số lượng hàng hóa/dịch vụ trên hóa đơn

**Ba thời điểm phải chạy lại:**

| Khi nào | Ai gọi | Trạng thái công việc |
|---|---|---|
| Lưu / sửa / xóa một CTBH có nguồn là HĐ | module `chung_tu_ban_hang` | ⚠️ §6 — **phải sửa module khác** |
| Sửa hóa đơn (thêm/xóa dòng, đổi số lượng) | `SuaHoaDonBan` | ✅ [04 §4.3](04-cap-nhat-hoa-don.md) |
| Xóa hóa đơn | `XoaHoaDonBan` — gỡ hết liên kết, trạng thái không còn ý nghĩa | ✅ [05 §5.1](05-xoa-hoa-don.md) |

**Cài ở đâu:** `TrangThaiHoaDonBan.tinhLaiTrangThaiLapChungTu(HoaDonBanHang)` — lớp thuần nghiệp vụ, nhận sẵn map `dongId → soLuongDaTieuThu` để test được không cần DB.

---

## 6. Phần phải sửa ở module `chung_tu_ban_hang` (6b)

Khi module CTBH lưu một chứng từ có nguồn là hóa đơn, nó phải:

```java
quanHe.lienKet(dongCtbh.stream().map(d -> new LenhLienKet(
        LoaiChungTu.SAL_HOA_DON_BAN_HANG, hoaDonId,          d.chiTietHoaDonBanHangId(),
        LoaiChungTu.SAL_CHUNG_TU_BAN_HANG, chungTuId,        d.id()))
    .toList());
```
rồi gọi ngược sang HĐ để tính lại trạng thái.

**Vấn đề ranh giới Modulith:** `chung_tu_ban_hang` không được import `hoa_don_ban_hang.internal.*`. Hai phương án:

| | A — HĐ mở `api/CapNhatTrangThaiApi`, CTBH gọi vào | **B (CHỌN) — HĐ tự suy trạng thái khi ĐỌC** |
|---|---|---|
| Cách làm | Module HĐ tạo `hoa_don_ban_hang/api/` + `@NamedInterface`; CTBH gọi sau khi lưu | `trang_thai_lap_chung_tu` là **cột vật lý** nhưng được **làm mới lúc HĐ tự đọc/ghi**; ngoài ra `HoaDonBanMapper` **luôn tính lại tại chỗ** từ `quanHe.daTieuThu(...)` khi trả DTO |
| Nhất quán | Cao — cột luôn đúng ngay sau khi CTBH lưu | Cột có thể **cũ**; DTO thì luôn đúng |
| Ranh giới | Phải tạo `api/` — đi ngược luật "không tạo `api/` cho chắc" (`cell-app/CLAUDE.md`), nhưng **lần này có người gọi thật** nên hợp lệ | Sạch tuyệt đối, không đụng module khác |
| Chi phí lọc/sắp xếp | Cột luôn đúng ⇒ `@Searchable` trên cột hoạt động chính xác | ⚠️ **Cột cũ ⇒ lọc/sắp xếp theo `trangThaiLapChungTu` ở [01](01-xem-danh-sach-hoa-don.md) có thể SAI** |
| Phạm vi sửa | 1 file mới ở HĐ + 1 chỗ gọi ở CTBH | 0 file ở module khác |

**Chốt:** phương án B **không đủ** vì nó phá vỡ chính cột mà BA yêu cầu lọc/sắp xếp được (`SCR_HDBanHang_DanhSach.md:25` — Tìm kiếm `Y`, Sắp xếp `Y`). ⇒ **Chọn phương án A**, nhưng đưa vào **cuối thứ tự thực hiện** ([00 §8](00-ke-hoach-tong.md) bước 9) và **báo user trước khi chạm `chung_tu_ban_hang`**, vì đó là module đang chạy production.

Hợp đồng tối thiểu:

```java
// hoa_don_ban_hang/api/package-info.java  →  @NamedInterface("hoa-don-ban-hang")
package vn.vtt.pmkt.cell.hoa_don_ban_hang.api;

public interface HoaDonBanHangApi {
    /** Tính lại TrangThaiLapChungTu của các hóa đơn nguồn sau khi chứng từ đích thay đổi. */
    void tinhLaiTrangThaiLapChungTu(Collection<UUID> hoaDonIds);
}
```
Gọi **trong cùng transaction** của luồng lưu CTBH.

---

## 7. Tương tranh & transaction

| Vấn đề | Xử lý |
|---|---|
| A10 | `@Transactional(readOnly = true)`, không khóa. Số lượng còn lại là **ảnh chụp tại thời điểm đọc**, có thể cũ khi người dùng bấm Lưu — chốt thật nằm ở `quanHe.lienKet` lúc CTBH lưu (`QuanHeChungTuApi.java:21-30`, khóa `ORDER BY id FOR UPDATE`). |
| Hai người cùng lập CTBH từ một HĐ | `lienKet` khóa dòng nguồn — người thứ hai thấy số lượng đã cập nhật. **Chỉ đúng nếu chọn phương án A của §2** (áp ràng buộc `laTieuThu`); với phương án C thì không có ràng buộc SL nào bị vi phạm, chỉ trạng thái nhảy sang `Đã lập đủ`. |
| Idempotency | `lienKet` dùng `INSERT … ON CONFLICT DO NOTHING` trên `(tenant_id, dong_dich_id)` (`QuanHeChungTuApi.java:27-29`) — lưu lại cùng chứng từ không nhân đôi liên kết. |

---

## 8. Kiểm thử

### 8.1 Unit (`@Tag("unit")`)

| Lớp test | Case |
|---|---|
| `TrangThaiHoaDonBanTest` | `daTieuThu` rỗng → `Chưa lập` |
| | `Σ daTieuThu = 40`, `Σ soLuong = 100` → `Đã lập 1 phần` |
| | `Σ daTieuThu = 100`, `Σ soLuong = 100` → `Đã lập đủ` |
| | `Σ daTieuThu = 120 > 100` (nếu chọn phương án C) → `Đã lập đủ`, không ném lỗi |
| | Dòng ghi chú **không** vào `Σ soLuong` |
| `DuLieuLapChungTuMapperTest` | Dòng có `soLuongConLai = 0` **vẫn** được trả về (không lọc bỏ) |
| | `soLuongConLai = soLuong − soLuongDaLapChungTu`, không âm |
| | Không lọt cột hạch toán nào vào DTO |
| `LoaiChungTuTest` | `SAL_CHUNG_TU_BAN_HANG.laDich() == true` sau khi sửa (R2) |

### 8.2 Tích hợp (cần Docker — R7)

| Lớp | Kiểm |
|---|---|
| `LoaiChungTuCheckConstraintIT` | ★ **Test đồng bộ enum ⇄ `pg_constraint`** đã có sẵn (`LoaiChungTu.java:8-11`) — chạy để chắc chắn migration `V1033` và enum khớp nhau. **Bắt buộc chạy qua IntelliJ trước khi push** (R2). |
| `LapChungTuTuHoaDonIT` | Lập CTBH từ HĐ 100 cái với 60 cái → `trangThaiLapChungTu` = `Đã lập 1 phần` |
| | Lập tiếp 40 cái → `Đã lập đủ`; nút biến mất (`choPhepLapChungTuBanHang = false`) |
| | Xóa CTBH đã lập → liên kết bị gỡ, HĐ về `Đã lập 1 phần` / `Chưa lập` |
| | Hai request song song lập CTBH từ cùng HĐ → liên kết không nhân đôi |
| `A10IT` | HĐ tenant khác → 404 |

---

## 9. Câu hỏi cần BA xác nhận

| # | Vấn đề | Bằng chứng | Xử lý tạm |
|---|---|---|---|
| **Q1** | Lập chứng từ từ hóa đơn có bị **ràng buộc số lượng** không (`SoLuong_nhap ≤ SoLuong − đã lập`)? | **Có (suy luận):** BR02 (`SCR_HDBanHang_DanhSach.md:63-65`) định nghĩa trạng thái theo tỷ lệ số lượng ⇒ ngụ ý có theo dõi số lượng. **Không (theo văn bản):** BR04 (`:70-77`) chỉ nói auto-fill, **không** nêu ràng buộc nào; đối chiếu chiều ngược lại thì BR23 của CTBH (`SCR_CTBH_ThemMoi.md:1429-1550`) mô tả ràng buộc rất chi tiết — sự vắng mặt ở đây có thể là cố ý hoặc là thiếu sót. | **Không** áp ràng buộc (phương án C của §2), tránh đụng `laTieuThu()` vốn ảnh hưởng nghiệp vụ đang chạy. Nếu BA chốt "có" → phải xử lý §2 phương án A hoặc B, **tăng đáng kể phạm vi và rủi ro**. |
| **Q2** | Một hóa đơn **được lập kèm từ CTBH** (chiều 1) có được phép làm nguồn để lập CTBH mới (chiều 2) không? | Không có tài liệu nào cấm. Về nghiệp vụ thì vô lý (hàng đã có chứng từ bán rồi). Dữ liệu: HĐ đó có `chungTuBanId ≠ null` (cột `chung_tu_ban_id` — ✅ đã có ở baseline). | Đề xuất **chặn**: nút "Lập chứng từ bán hàng" ẩn khi `chungTuBanId ≠ null`. Cần BA xác nhận trước khi cài. |
| **Q3** | Chứng từ lập từ hóa đơn có kế thừa `loaiTienId` / `tyGia` không? BR04 **không nhắc**. | `SCR_HDBanHang_DanhSach.md:74-77` liệt kê 3 nhóm fill: khách hàng, mặt hàng, diễn giải/ghi chú — **không có** loại tiền. Nhưng `ChungTuBan.LoaiTienId` là trường **bắt buộc** (`SCR_CTBH_ThemMoi.md:173`). | A10 **có trả** `loaiTienId` + `tyGia` để FE fill. Nếu BA không muốn → FE bỏ qua field. |
| **Q4** | Gọi A10 trên HĐ `Đã lập đủ` — trả lỗi gì? `6.messages.md` không có mã. | — | 409 `ALREADY_FULLY_USED`, `messageId = null`. **Cần BA cấp mã** hoặc xác nhận FE tự chặn bằng cờ `choPhepLapChungTuBanHang` (khi đó BE trả 409 chỉ là hàng rào phụ). |
| **Q5** | Chứng từ lập từ hóa đơn **không kế thừa** được TK công nợ / TK doanh thu / Kho / giá vốn (hóa đơn không có các cột này). Người dùng phải nhập lại — có chấp nhận không? | `SCR_HDBanHang_ThemMoi.md:40-41,69` liệt kê rõ các cột hóa đơn **không có** | FE auto-fill theo BR07/BR16 của CTBH khi chọn mã hàng. Xác nhận đây là hành vi mong muốn. |
| **Q6** | BR05 "Lập chứng từ bán dịch vụ" — module chưa tồn tại, xử lý thế nào? | `SCR_HDBanHang_DanhSach.md:81-88` | Xem [00 §12-Q6](00-ke-hoach-tong.md). |

---

## 10. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR2 (epic) — Trạng thái lập chứng từ 3 giá trị | §5 — công thức tính |
| BR4 (epic) — Nút Lập chứng từ bán hàng | §4 A10 + cờ `choPhepLapChungTuBanHang` ở [01 §5.3](01-xem-danh-sach-hoa-don.md) |
| BR13.1 (chung) | Nút hiện theo trạng thái |
| BR25 | Quyền `.View.Detail` |
| BR28 | RLS trên A10 |
| BR7 | `soLuongConLai` kiểu `quantity(18,3)` |

**BR chưa đạt:**
- **BR5 (epic) — Lập chứng từ bán dịch vụ:** ngoài phạm vi, module chưa tồn tại ([00 §1.2](00-ke-hoach-tong.md)).
- **BR23 của CTBH (ràng buộc số lượng)** — chiều 2 **không** áp ràng buộc, chờ Q1.
- **Phần 6b** (module `chung_tu_ban_hang` gọi ngược để tính lại trạng thái) — **phải xin phép user** trước khi sửa module đang chạy production; nếu không làm thì `trangThaiLapChungTu` không tự cập nhật khi CTBH được lưu, và cột lọc/sắp xếp ở màn danh sách sẽ sai.
