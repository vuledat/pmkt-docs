# F4 — Chỉnh sửa Chứng từ điều chỉnh giá

> ### 🔄 CẬP NHẬT 2026-08-21
>
> 1. **`soChungTu` không cho sửa** — nay đi qua engine: template vẫn gọi `SoChungTuApi.sinhSo(chungTu, soNguoiDungGo)`, và "sửa chứng từ mà số không đổi ⇒ không làm gì" là hành vi sẵn có của engine. §1 (bỏ qua giá trị client gửi) vẫn đúng về kết quả.
> 2. **Cột phẳng (huỷ D6)** — §3 và §4 đọc theo [09 §9.2.1](09-thiet-ke-db.md).
> 3. **`status.choPhepSua()`** nay là `trangThaiChungTu.choPhepSua()`, chỉ đúng khi `CHUA_GHI_SO`.
> 4. Mẫu code: `dieu_chinh_gia_hang_mua/internal/service/business/SuaDieuChinhGiaMua.java`.

| | |
|---|---|
| Mã chức năng | **F4** |
| UC nguồn | [PMKT-U-07671 — Sửa](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/4.usecases/PMKT-U-07671_Sua/UC_Sua.md) |
| Màn hình nguồn | [SCR_SuaDieuChinhGia.md](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/5.screens/SCR_SuaDieuChinhGia.md) (form giống hệt Thêm mới) |
| Endpoint phụ trách | **A5** `PUT /api/ban-hang/dieu-chinh-gia-hang-ban/{id}` |
| Phụ thuộc | [03-them-moi.md](03-them-moi.md) — dùng chung request DTO, công thức, ma trận validate |

## 1. Quyết định riêng

- **Dùng lại nguyên `LuuDieuChinhGiaHangBanRequest`** (kiểu `U` = kiểu `C` trong generic của controller, đúng mẫu `ChungTuBanHangController` khai `<…, LuuChungTuBanHangRequest, LuuChungTuBanHangRequest>`). Form Sửa của BA là *"form giống nhau"* với Thêm mới (SCR_Sua dòng 20) — hai DTO khác nhau sẽ phải đồng bộ tay mỗi lần thêm trường.
- **Thay toàn bộ dòng chi tiết** (`orphanRemoval`) thay vì diff từng dòng: BA cho phép thêm/xoá dòng tự do (UC_Sua bước 6), và diff theo `id` dòng chỉ có ý nghĩa nếu dòng mang trạng thái riêng — ở đây không có. Đổi lại phải **giữ `thu_tu`** theo mảng client gửi (BR21.2 "Lưu thứ tự dòng").
- **`soChungTu` không cho sửa** (SCR_Sua dòng 23, BR2 của màn). Cài ở **server**: bỏ qua giá trị client gửi, giữ nguyên số cũ. Không ném lỗi khi client gửi khác — FE đã khoá ô, và ném lỗi ở đây chỉ tạo ca đỏ vô nghĩa khi client gửi lại nguyên payload đọc được từ `GET /{id}`.

## 2. Hợp đồng API

### A5 — `PUT /{id}` · quyền `DieuChinhGiaHangBan.Edit`

Request: **giống hệt [03 §2](03-them-moi.md)**, thêm hai điểm:

| Field | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `updatedAt` | string (ISO instant) | **Y** | token khoá lạc quan lấy từ `GET /{id}`; lệch ⇒ 409 |
| `soChungTu` | string | — | **bị bỏ qua** (§1) |
| `ghiSo` | bool | N | `true` = nút "Lưu và ghi sổ" của màn Sửa (SCR_Sua dòng 30) |

```jsonc
// Response 200
{
  "code": "SUCCESS",
  "message": "Cập nhật chứng từ điều chỉnh giá thành công",
  "messageId": "MSG_PMKT-E-07664_002",     // hoặc _004 khi ghiSo=true
  "data": { /* giống A3 */ }
}
```

| Điều kiện | HTTP | Mã | messageId |
|---|---|---|---|
| Thiếu quyền `.Edit` | 403 | — | `_007` |
| `id` không tồn tại / đã xoá | 404 | — | — |
| Chứng từ **đã ghi sổ** | 400 | `DA_GHI_SO` | `_201` |
| Cờ trạng thái nói chưa ghi sổ nhưng sổ cái còn dòng | 409 | `SO_CAI_LECH` | — (base ném, xem §4) |
| `updatedAt` lệch | 409 | `STALE_DATA` | — (BR12: *"Dữ liệu đã được cập nhật bởi người dùng khác. Vui lòng tải lại dữ liệu trước khi thao tác."*) |
| Các lỗi validate còn lại | 400 | — | như [03 §2.4](03-them-moi.md) |

## 3. Ánh xạ cột · công thức · validation

Không lặp lại: xem [03 §3](03-them-moi.md) (ánh xạ), [03 §4](03-them-moi.md) (công thức), [03 §5](03-them-moi.md) (ma trận V1…V20).

Khác biệt duy nhất trong ma trận:

| # | Luật | Khác gì với Thêm mới |
|---|---|---|
| V3 | trùng `soChungTu` | loại trừ chính bản ghi đang sửa (`id <> :id`) — nếu không, mọi lần sửa đều báo trùng với chính nó |
| V20 | khoá lạc quan | **chỉ có ở luồng này và luồng Xoá**; cột `phien_ban` (`@Version`) là thứ chặn lost-update thật, `updatedAt` là token FE cầm |
| **V21** | Chứng từ phải **chưa ghi sổ** | luật riêng của luồng sửa — `status.choPhepSua()` ([TrangThaiChungTu.java](../../cell-app/src/main/java/vn/vtt/pmkt/cell/core/entity/TrangThaiChungTu.java)); vi phạm ⇒ 400 `_201` |

## 4. Luồng xử lý

`ChungTuTemplate` luồng SUA ([:171](../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)) — **có hai bước mà luồng TAO không có**:

| Bước base | Ý nghĩa ở màn này |
|---|---|
| `doiHoiDinhDanh` | `chuanBiChungTu` phải gọi `ctx.ghiNhanChungTu(...)` với bản ghi đang có, nếu không base ném `IllegalStateException` |
| **`khoaChungTu`** | `ChungTuKhoaApi.khoa(id)` — hai người cùng sửa thì người sau đợi người trước commit. Khoá này **không thay** optimistic lock: dữ liệu người dùng cầm trên màn hình đã cũ vẫn phải bị `@Version` chặn (409 `STALE_DATA`) |
| `kiemTraNghiepVu` | V21 (chưa ghi sổ) chạy ở đây → mã `_201` đọc được cho FE |
| **`doiSoatVoiSoCai`** | hỏi thẳng `GhiSoApi.daGhiSo(id)`. Chỉ nổ ở ca **lệch**: cờ nói chưa ghi sổ mà `acc_so_cai` còn dòng (ai đó vừa ghi sổ xong giữa lúc ta đọc entity). Trả **409** vì đây là tranh chấp, không phải dữ liệu hỏng |
| `truocKhiLuu` | tính lại toàn bộ số tiền (§4 của [03](03-them-moi.md)); **giữ nguyên** `so_chung_tu` cũ |
| `luuEntity` | thay toàn bộ `chiTiet` (orphanRemoval), đánh lại `thu_tu` theo mảng client gửi |
| `sauKhiLuu` | **gỡ liên kết cũ rồi tạo lại**: `QuanHeChungTuApi.goToanBoTheoDich(SAL_DIEU_CHINH_GIA_HANG_BAN, id)` → `lienKet(...)` với bộ dòng mới. Bắt buộc — dòng chi tiết cũ đã bị xoá, liên kết trỏ vào chúng thành mồ côi |
| `coGhiSoNgay` | `request.ghiSo()` |

> **Vì sao luồng SUA không có bước gỡ bút toán:** chỉ sửa được chứng từ **chưa ghi sổ**, nên không tồn tại dòng sổ cái nào để gỡ (javadoc `luongSua`). `doiSoatVoiSoCai` là lưới an toàn cho đúng ca lệch.

## 5. Tương tranh & transaction

| Cơ chế | Chống gì | Ở đâu |
|---|---|---|
| `@Transactional` bao cả luồng | nửa vời giữa xoá dòng cũ và ghi dòng mới | `ChungTuTemplate.thucThi` |
| `ChungTuKhoaApi.khoa(id)` (pessimistic, reentrant) | hai request sửa/ghi sổ cùng chứng từ chạy chồng | `khoaChungTu` |
| `@Version phien_ban` | lost-update từ màn hình đã cũ | entity → 409 `STALE_DATA` |
| `doiSoatVoiSoCai` | sửa chứng từ vừa bị người khác ghi sổ | base → 409 `SO_CAI_LECH` |
| `ORDER BY id FOR UPDATE` trên dòng nguồn | hai chứng từ cùng lấy một dòng nguồn | `QuanHeChungTuApi.lienKet` |

**Idempotency:** PUT là thay-thế-toàn-bộ nên tự nhiên idempotent với cùng `updatedAt`; gọi lần hai với `updatedAt` cũ ⇒ 409, đúng ý.

## 6. Kiểm thử

### Unit
| Lớp test | Kiểm gì |
|---|---|
| `SuaDieuChinhGiaTest` | `soChungTu` client gửi khác bị **bỏ qua**; V3 loại trừ chính mình; V21 chặn chứng từ `DA_GHI_SO` với mã `_201`; `thu_tu` đánh lại theo thứ tự mảng |
| `LienKetNguonDieuChinhGiaTest` | sửa ⇒ gỡ hết liên kết cũ rồi tạo lại; bỏ một dòng chi tiết ⇒ liên kết của dòng đó biến mất |

### Tích hợp (cần Docker)
| Lớp test | Kiểm gì |
|---|---|
| `SuaDieuChinhGiaIT` | sửa chứng từ đã ghi sổ ⇒ 400 `_201`, dữ liệu không đổi · `updatedAt` cũ ⇒ 409, dữ liệu không đổi · xoá 1 dòng + thêm 2 dòng ⇒ đúng số dòng và đúng số liên kết trong `ctu_quan_he_chung_tu` · sửa + `ghiSo=true` ⇒ đủ dòng `acc_so_cai` trong cùng transaction · kỳ khoá ⇒ 400 `_203` và rollback sạch |

## 7. BR đã áp dụng
BR12 (V21 + chống sửa đồng thời + ghi sổ duy nhất) · BR15 (ma trận [03 §5](03-them-moi.md)) · BR17 (kỳ kế toán) · BR19 (V3 loại trừ chính mình) · BR21 (giữ thứ tự dòng) · BR25 (`.Edit`) · BR29 (dòng con xoá theo cha) · BR34 (mở từ màn Xem chi tiết — FE) · BR37 (ngày hạch toán ≥ ngày chứng từ) · BR46 (`nguoi_cap_nhat`/`ngay_cap_nhat` do base ghi).
