# F5 — Xóa Chứng từ điều chỉnh giá (đơn + hàng loạt)

> ### 🔄 CẬP NHẬT 2026-08-21
>
> 1. **Thêm một bước bắt buộc trong luồng xoá: THU HỒI SỐ CHỨNG TỪ.** Engine đánh số yêu cầu gọi `SoChungTuApi.thuHoi(chungTu, ngayHachToan)` **sau khi** entity đã xoá mềm, cùng transaction (BR10). Đủ điều kiện (số cuối dãy · Tự động cập nhật bật · kỳ chưa khoá) ⇒ bộ đếm lùi và số trả về pool; không đủ ⇒ số đã đốt, giữ nguyên. Bỏ bước này là mỗi lần xoá đốt vĩnh viễn một số.
> 2. **`status`** → `trangThaiChungTu`; X2 kiểm `trangThaiChungTu.choPhepSua()`.
> 3. §7 mục "soChungTu của chứng từ đã xoá dùng lại được" vẫn đúng (unique index có `WHERE da_xoa = false`) — nhưng nay còn phụ thuộc engine có thu hồi số hay không, test phải phủ cả hai nhánh.

| | |
|---|---|
| Mã chức năng | **F5** |
| UC nguồn | [PMKT-U-07668 — Xóa](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/4.usecases/PMKT-U-07668_Xoa/UC_Xoa.md) |
| Màn hình nguồn | [SCR_DanhSachDieuChinhGia.md](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/5.screens/SCR_DanhSachDieuChinhGia.md) |
| Endpoint phụ trách | **A6** `DELETE /{id}` · **A14** `POST /xoa-hang-loat` |

## 1. Quyết định riêng

- **Xóa mềm** (`da_xoa = true` + `nguoi_xoa` + `ngay_xoa`) theo BR29.1 — không xóa vật lý. Dòng chi tiết **cũng xóa mềm theo cha** (BR29.2), không dựa vào `ON DELETE CASCADE` của FK ([V1:27985](../../cell-app/src/main/resources/db/migration/V1__create_database.sql)): cascade đó chỉ chạy khi xóa vật lý, mà ta không xóa vật lý.
- **Gỡ toàn bộ liên kết nguồn** khi xóa: `QuanHeChungTuApi.goToanBoTheoDich(SAL_DIEU_CHINH_GIA_HANG_BAN, id)`. Không gỡ thì dòng bán hàng gốc vẫn "thấy" một chứng từ điều chỉnh đã bị xoá ở tab Chứng từ liên quan. **Không chọn** để liên kết lại rồi lọc `da_xoa` khi đọc: `ctu_quan_he_chung_tu` là bảng đa hình, lọc soft-delete xuyên loại là truy vấn phải biết mọi bảng đích.
- **Popup xác nhận (`MSG_300`) là của FE.** BE không có bước xác nhận; gọi DELETE là xoá thật (mềm).

## 2. Hợp đồng API

### A6 — `DELETE /api/ban-hang/dieu-chinh-gia-hang-ban/{id}` · quyền `DieuChinhGiaHangBan.Delete`

```jsonc
// Request body — DeleteRequest (core/request/DeleteRequest.java), token khoá lạc quan
{ "lockToken": "2026-08-10T03:12:44Z" }
```

```jsonc
// Response 200
{ "code": "SUCCESS", "message": "Xóa chứng từ điều chỉnh giá thành công",
  "messageId": "MSG_PMKT-E-07664_003", "data": null }
```

| Điều kiện | HTTP | Mã | messageId |
|---|---|---|---|
| Thiếu quyền `.Delete` | 403 | — | `_007` |
| `id` không tồn tại / đã xoá | 404 | — | — |
| Chứng từ **đã ghi sổ** | 400 | `DA_GHI_SO` | `_201` |
| Cờ trạng thái ≠ sổ cái | 409 | `SO_CAI_LECH` | — |
| `lockToken` lệch | 409 | `STALE_DATA` | — |

### A14 — `POST /xoa-hang-loat` · quyền `DieuChinhGiaHangBan.Delete`

```jsonc
// Request — XuLyHangLoatRequest
{ "ids": ["…", "…", "…"] }
```

```jsonc
// Response 200 — KỂ CẢ khi có dòng thất bại (đó là dữ liệu cho popup kết quả, không phải lỗi request)
{
  "code": "SUCCESS",
  "message": "Xử lý thành công 2 chứng từ, thất bại 1 chứng từ",
  "messageId": "MSG_PMKT-E-07664_003",
  "data": {
    "thanhCong": 2, "thatBai": 1,
    "chiTiet": [
      { "id": "…", "soChungTu": "BGG00001", "thanhCong": true,  "loi": null },
      { "id": "…", "soChungTu": "BGG00002", "thanhCong": true,  "loi": null },
      { "id": "…", "soChungTu": "BGG00003", "thanhCong": false, "loi": "Chứng từ đã ghi sổ" }
    ]
  }
}
```

Hình dạng chính xác của `KetQuaHangLoatDto` theo `accounting_core/chung_tu/dto/KetQuaHangLoatDto.java` — **đọc lại file đó trước khi code**, đừng bám mẫu JSON ở đây nếu lệch.

BR45: mỗi chứng từ là **một transaction riêng** (một dòng hỏng không kéo cả lô); chứng từ đã ghi sổ bị **bỏ qua có báo cáo**, không chặn cả lô.

## 3. Ánh xạ cột
Không có trường nghiệp vụ mới. Cột bị ghi: `da_xoa`, `ngay_xoa`, `nguoi_xoa` (base `SoftDeletableEntity` quản — BR46).

## 4. Validation

| # | Luật | Thời điểm | Thông báo | Mã | BR |
|---|---|---|---|---|---|
| X1 | Chứng từ tồn tại, chưa xoá, đúng tenant | `chuanBiChungTu` → `load(id)` | — | 404 | BR28 |
| X2 | `status.choPhepSua()` (chưa ghi sổ) | `kiemTraNghiepVu` | Chứng từ đã ghi sổ | `_201` | BR12, UC_Xoa luồng phụ |
| X3 | Sổ cái không còn dòng của chứng từ | `doiSoatVoiSoCai` (base) | — | 409 `SO_CAI_LECH` | — |
| X4 | `lockToken` khớp `updatedAt` hiện tại | `luuEntity` (`@Version`) | Dữ liệu đã được cập nhật bởi người dùng khác… | 409 `STALE_DATA` | BR12 |
| X5 | *(không có)* Chứng từ đang được chứng từ khác dùng làm nguồn | — | — | — | Điều chỉnh giá là loại **chỉ-là-đích** ([LoaiChungTu.java:31](../../cell-app/src/main/java/vn/vtt/pmkt/cell/quan_he_chung_tu/api/LoaiChungTu.java)), không chứng từ nào lấy nó làm nguồn ⇒ không cần guard `coLienKet` |

## 5. Luồng xử lý

`ChungTuTemplate` luồng XOA ([:194](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)):

```
doiHoiDinhDanh → khoaChungTu → kiemTraNghiepVu (X2) → doiSoatVoiSoCai (X3)
   → luuChungTu (truocKhiLuu: đánh dấu da_xoa cho header + mọi dòng chi tiết; luuEntity: save)
   → sauKhiLuu (goToanBoTheoDich — gỡ liên kết nguồn)
   → ghiNhatKyTacDong → dangKyThongBaoSauCommit
```

> Luồng XOA **không kiểm kỳ kế toán** — javadoc base nói rõ lý do: nó không tạo trạng thái sổ sách mới và cũng không gỡ dòng sổ cái nào. Đây là **lệch có chủ ý** so với BR17.1 (bảng BR17.1 chỉ liệt kê Lưu/Ghi sổ/Bỏ ghi sổ, không có Xóa — nên thực ra không lệch).

## 6. Tương tranh & transaction
`khoaChungTu` + `@Version` như [04 §5](04-chinh-sua.md). Xoá hàng loạt: mỗi id một transaction (`HangLoatChungTuService`), nên khoá giữ trong phạm vi từng chứng từ, không giữ khoá cả lô.

## 7. Kiểm thử

### Unit
| Lớp test | Kiểm gì |
|---|---|
| `XoaDieuChinhGiaTest` | X2 chặn `DA_GHI_SO` với mã `_201`; header và **mọi dòng chi tiết** đều được đánh `da_xoa`; `goToanBoTheoDich` được gọi đúng một lần với đúng loại + id |

### Tích hợp (cần Docker)
| Lớp test | Kiểm gì |
|---|---|
| `XoaDieuChinhGiaIT` | sau xoá: `GET /{id}` → 404, `POST /search` không trả bản ghi, dòng chi tiết `da_xoa = true`, `ctu_quan_he_chung_tu` không còn dòng đích · xoá chứng từ đã ghi sổ → 400 và **không** đụng dữ liệu · `lockToken` lệch → 409 · **`soChungTu` của chứng từ đã xoá dùng lại được** (unique index có `WHERE da_xoa = false`, [V1:23661](../../cell-app/src/main/resources/db/migration/V1__create_database.sql)) |
| `XoaHangLoatIT` | lô 3 chứng từ (2 chưa ghi sổ, 1 đã ghi sổ) → `thanhCong = 2`, `thatBai = 1`, HTTP 200; chứng từ đã ghi sổ **không** bị đụng |

## 8. BR đã áp dụng
BR12 (X2) · BR13.1 + BR42.2 (nút Xóa ẩn khi đã ghi sổ — FE, dựa `trangThaiChungTu`) · BR16 (`MSG_COMMON_001` cho thao tác sai trạng thái qua API) · BR25 (`.Delete`) · BR29.1 xoá mềm · BR29.2 xoá dòng con theo cha · BR41 (không áp dụng — quan hệ ở đây là ràng buộc nghiệp vụ, BR41 tự loại trừ) · BR45 (A14) · BR46 (`nguoi_xoa`/`ngay_xoa`).
