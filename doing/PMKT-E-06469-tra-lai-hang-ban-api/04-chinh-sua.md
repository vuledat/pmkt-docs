# F4 — Chỉnh sửa chứng từ trả lại hàng bán

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F4** |
| UC nguồn | `PMKT-U-06472` — `4.usecases/PMKT-U-06472_Sua/UC_SuaTraLaiHangBan.md` + `AD_Sua.puml` |
| Màn hình | `5.screens/SCR_SuaTraLaiHangBan.md` (49 dòng — dùng chung popup với Thêm mới) + `Matrix/…/SCR_SuaTraLaiHangBan_MaTranAnHien.md` |
| Endpoint phụ trách | **A8** `PUT /{id}` |
| Quyền | `TraLaiHangBan.Edit` |
| **Trạng thái** | ☐ chưa code — `update` đang chặn 400 `CHUA_HO_TRO` |

## 1. Quyết định riêng

| # | Quyết định | Trỏ về |
|---|---|---|
| 1.1 | `C` và `U` **cùng là** `LuuTraLaiHangBanRequest` — popup Sửa dùng chung toàn bộ trường/validate/BR với popup Thêm mới | `SCR_SuaTraLaiHangBan.md:3-5,26`; mẫu `ChungTuBanHangCrudService.java:36-39` |
| 1.2 | Chỉ sửa được chứng từ **CHƯA ghi sổ** ⇒ luồng SỬA **không có bước gỡ bút toán**, thay bằng đối soát sổ cái | `ChungTuTemplate.java:162-170`; `SuaChungTuBanHang.java:20-23` |
| 1.3 | "Lưu và ghi sổ" từ popup Sửa = `PUT` với `ghiSo = true` — vẫn MỘT transaction | `SCR_SuaTraLaiHangBan.md:33` |
| 1.4 | **Số chứng từ và Ngày chứng từ read-only ở FE**, nhưng BE **vẫn kiểm** giá trị gửi lên có khớp bản ghi hiện tại không | xem §4-V31 |

---

## 2. Hợp đồng API

### A8 — `PUT /api/ban-hang/tra-lai-hang-ban/{id}`

Quyền: `TraLaiHangBan.Edit`.

Request: **giống hoàn toàn** A7 ([03 §2](03-them-moi.md)), thêm **một** field:

| Field | Kiểu | Bắt buộc | Ràng buộc |
|---|---|---|---|
| `updatedAt` | `Instant` (ISO-8601) | N (khuyến nghị **luôn gửi**) | token optimistic-lock; lệch `ngay_cap_nhat` hiện tại → **409 `STALE_DATA`**. `null` ⇒ bỏ kiểm ở tầng này, `@Version phien_ban` vẫn là chốt cuối (`BanHangSupport.java:110-118`) |

```jsonc
// Response 200
{
  "data": { /* … DTO đầy đủ, updatedAt MỚI … */ },
  "message": "Cập nhật chứng từ trả lại hàng bán thành công",
  "messageId": "MSG_PMKT-E-06469_002"
}
```

Khi `ghiSo = true`: `"Ghi sổ chứng từ trả lại hàng bán thành công"` / `MSG_PMKT-E-06469_004`.

**Lỗi riêng của A8** (ngoài toàn bộ bảng lỗi của A7):

| code | HTTP | messageId | Khi nào |
|---|---|---|---|
| `FORBIDDEN` | 403 | `_007` | thiếu `TraLaiHangBan.Edit` |
| `NOT_FOUND` | 404 | `_008` | `id` không tồn tại / `da_xoa = true` |
| **`ALREADY_POSTED`** | **409** | **`_201`** | chứng từ đang `DA_GHI_SO` — *"Chứng từ đã ghi sổ, không được sửa"* |
| `STALE_DATA` | 409 | — | `updatedAt` lệch (`BanHangSupport.java:120-130`) hoặc `@Version` xung đột (`OptimisticLockException` → handler chung) |
| **`SO_CAI_LECH`** | **409** | `MSG_CORE_CT_SO_CAI_LECH` | cờ trạng thái nói "chưa ghi sổ" nhưng `acc_so_cai` **vẫn còn dòng** — `ChungTuTemplate.java:397-406` |
| `IMMUTABLE_FIELD` | 400 | — | `soChungTu`/`ngayChungTu` gửi lên khác bản ghi hiện tại (§4-V31) |

---

## 3. Ánh xạ cột — khác biệt so với Thêm mới

| Field | Thêm mới | **Chỉnh sửa** | Nguồn |
|---|---|---|---|
| `soChungTu` | tự sinh hoặc nhập tay | **read-only**, không đổi | `SCR_Sua:11`, `UC:157,176` |
| `ngayChungTu` | mặc định hôm nay | **read-only**, không đổi | `SCR_Sua:12`, `UC:157,176` |
| `ngayHachToan` | nhập | **cho sửa** (kéo theo kiểm kỳ mới) | `SCR:287,301` |
| `updatedAt` | không có | **token khoá** | `api/model.ts:187-188` |
| `status` | server đặt `CHUA_GHI_SO`/`DA_GHI_SO` | **giữ nguyên** nếu chỉ Lưu; `DA_GHI_SO` nếu Lưu và ghi sổ | `SCR_Sua:14` |
| `don_vi_id` | trigger gán | **BẤT BIẾN** — trigger `fn_pv_sal_chung_tu_tra_lai_hang_ban` ném `PV_BB_001` nếu đổi | `V1:2871-2879,26251` |
| dòng chi tiết | insert hết | **replace toàn bộ**: `cascade = ALL` + `orphanRemoval = true` ⇒ dòng không còn trong request bị xoá vật lý khỏi collection | `docs/rules/be-khung-kien-truc-chuan.md:201-202` |
| Mã hàng của dòng | cho sửa | **FE khoá** khi lập từ chứng từ nguồn (`SCR:204-205`: *"Không cho sửa Mã hàng nhưng vẫn cho xóa cả dòng"*); **BE không cưỡng chế** — xem §9 |

> **Lưu ý nguyên văn `UC_Sua:182`:** *"Người dùng có quyền sửa toàn bộ thông tin trên phiếu (kể cả loại điều chỉnh là tăng/giảm)"* ⇒ BE **không** khoá thêm field nào ngoài `soChungTu`/`ngayChungTu`.

---

## 4. Validation — bổ sung so với A7

Toàn bộ V1…V29 của [03 §4](03-them-moi.md) áp dụng, `V1` đổi quyền thành `.Edit`. Thêm:

| # | Luật | Điều kiện chặn | Thời điểm kiểm | Thông báo | BR nguồn |
|---|---|---|---|---|---|
| V30 | Chỉ sửa khi chưa ghi sổ | `ct.daGhiSo()` | `kiemTraNghiepVu` — **trước** mọi thứ khác trong hàm | 409 · `_201` | BR12 · `UC:154,198` |
| V31 | Số/ngày chứng từ bất biến | `request.soChungTu ≠ ct.soChungTu` hoặc `request.ngayChungTu ≠ ct.ngayChungTu` | `kiemTraNghiepVu` | 400 `IMMUTABLE_FIELD` | `UC:157,176` |
| V32 | Token khoá lạc quan | `updatedAt ≠ ct.ngayCapNhat` (so **epoch-milli**, không `equals`) | `chuanBiChungTu`, **trước** khi làm gì khác | 409 `STALE_DATA` | BR12 §"Chống sửa đổi đồng thời" |
| V33 | Đối soát sổ cái | `GhiSoApi.daGhiSo(id) == true` trong khi cờ nói chưa ghi sổ | **base, `private`** — `ChungTuTemplate.doiSoatVoiSoCai` chạy ngay sau `kiemTraNghiepVu` (`:171-185,397-406`) | 409 `SO_CAI_LECH` | — |
| V34 | Tồn tại | `id` không có / `da_xoa` | `chuanBiChungTu` → `TraLaiSupport.nap(id)` | 404 · `_008` | BR29.1 |

**V33 vì sao cần** (nguyên văn `ChungTuTemplate.java:386-395`): trước đây luồng SỬA gọi kernel bỏ ghi sổ vô điều kiện nên ca lệch được dọn hộ âm thầm. Nay luồng SỬA không chạm sổ cái nữa, mà `delete from acc_so_cai` là đường xoá **duy nhất** — để lệch trôi qua là bút toán mồ côi vĩnh viễn. Ca thường gặp không phải dữ liệu hỏng mà là **tranh chấp**: `kiemTraNghiepVu` đọc cờ từ entity nạp **trước khi có khoá**, nên nó không thấy người khác vừa ghi sổ xong; bước này hỏi thẳng sổ cái nên thấy. Cả hai ca xử lý bằng cùng một hành động: tải lại rồi Bỏ ghi sổ trước.

---

## 5. Luồng xử lý — `SuaTraLaiHangBan extends LuuTraLaiHangBanTemplate`

`hanhDong() = SUA` ⇒ template chạy `luongSua` (`ChungTuTemplate.java:171-185`). **Khác `luongTao` ở 3 bước đầu**:

```
doiHoiDinhDanh        ← base, ném IllegalState nếu chuanBiChungTu quên ghiNhanChungTu (:356-363)
khoaChungTu           ← base, private — khoá tới hết transaction (:376-378)
kiemTraNghiepVu       ← override (V30…V32 + V4…V29)
doiSoatVoiSoCai       ← base, private (V33)
luuChungTu            → truocKhiLuu → luuEntity → kiemTraDaGhiNhanChungTu
sauKhiLuu
coGhiSoNgay ? phanGhiSo : luuKhongGhiSo
ghiNhatKyTacDong → dangKyThongBaoSauCommit → taoKetQua
```

`chuanBiChungTu` (**override**) — thứ tự bên trong là bắt buộc, mẫu 1:1 `SuaChungTuBanHang.java:36-48`:

```java
ChungTuTraLaiHangBan ct = tl.nap(ctx.lenh().id());          // 1. nạp bản ghi CŨ (V34)
tl.kiemTraLock(ct, ctx.lenh().request().getUpdatedAt());     // 2. V32 — sớm nhất có thể
ctx.ghiNhanChungTu(ct);                                      // 3. công bố định danh BẢN GHI CŨ:
                                                             //    khoaChungTu + doiSoatVoiSoCai cần nó
tl.mapper().apDung(ctx.lenh().request(), ct);                 // 4. đắp dữ liệu mới lên entity đã quản lý
tl.tinhToan().apDung(ct);                                     // 5. tính lại toàn bộ tiền
ctx.put(CHUNG_TU, ct);
```

> Bước 3 **phải trước** bước 4: khoá chứng từ và đối soát sổ cái chạy ngay sau `chuanBiChungTu` và cả hai cần định danh bản ghi đang có (`ChungTuTemplate.java:298-306,352-363`).

`sauKhiLuu` (**override**) — khác `TaoTraLaiHangBan` một việc: **gỡ liên kết cũ trước khi tạo liên kết mới**.

```java
// 1. Gỡ sạch liên kết cũ của chứng từ này (dòng gốc có thể đã thay đổi hoàn toàn)
quanHe.goToanBoTheoDich(LoaiChungTu.SAL_CHUNG_TU_TRA_LAI_HANG_BAN, ct.getId());
// 2. Tạo lại theo dòng chi tiết hiện tại — lienKet tự kiểm Σ ≤ SL nguồn
quanHe.lienKet(lenhLienKet(ct));
// 3. Định khoản CHỈ khi ghiSo = true
if (coGhiSoNgay(ctx)) { … themDinhKhoan … }
```

**Vì sao phải gỡ trước:** `QuanHeChungTuApi` **không có** `capNhatLienKet` — và đó là chủ ý (`QuanHeChungTuApi.java:11-15`: *"Sửa số lượng là sửa dòng chứng từ đích; bảng quan hệ không đụng tới"*). Nhưng khi người dùng **xoá một dòng** hoặc **đổi dòng gốc**, liên kết cũ trở thành mồ côi và vẫn tính vào `daTieuThu` ⇒ dòng bán hàng gốc bị "khoá" số lượng vĩnh viễn. Gỡ-rồi-tạo-lại trong cùng transaction là cách duy nhất giữ đúng `Σ tiêu thụ`.
`goToanBoTheoDich` idempotent (`QuanHeChungTuApi.java:41-46`) ⇒ gọi khi chưa có liên kết nào cũng không sao.

---

## 6. Tương tranh & transaction

| Việc | Cơ chế | `file:dòng` |
|---|---|---|
| Ranh giới | một `@Transactional` cho toàn luồng | `ChungTuTemplate.java:102` |
| Khoá bi quan chứng từ | `khoaChungTu` ngay sau `doiHoiDinhDanh` — hai request cùng chứng từ: request sau **đợi** request trước commit | `:171-173,376-378` |
| Khoá lạc quan | `@Version phien_ban` trên aggregate root + token `updatedAt` | `BaseChungTuEntity.java:20-23`; `BanHangSupport.java:110-130` |
| Sửa chỉ chạm dòng con | phải gọi `ct.touch()` để `phien_ban` vẫn tăng | `BaseChungTuEntity.java:22-23` |
| Khoá dòng nguồn khi tạo lại liên kết | `FOR UPDATE` trong `DongChungTuPort` | `DongChungTuPort.java:32-44` |

**Hai lớp khoá không thay được nhau** (`ChungTuTemplate.java:373-375`): khoá bi quan chặn hai luồng chạy chồng; `@Version` chặn dữ liệu người dùng đang cầm trên màn hình đã cũ.

---

## 7. Kiểm thử

### 7.1 Unit

| Lớp test | Case | Input → kỳ vọng |
|---|---|---|
| `SuaTraLaiHangBanTest` | V30 | `trangThaiChungTu = DA_GHI_SO` → 409 `ALREADY_POSTED` + `messageId = _201` |
| | V31 | request đổi `soChungTu` → 400 `IMMUTABLE_FIELD`; đổi `ngayHachToan` → **hợp lệ** |
| | V32 | `updatedAt` lệch 1 ms → 409 `STALE_DATA`; `updatedAt = null` → đi tiếp |
| | thứ tự `chuanBiChungTu` | `ghiNhanChungTu` được gọi **trước** `mapper.apDung` (verify order bằng `InOrder`) |
| | gỡ-rồi-tạo liên kết | `goToanBoTheoDich` gọi **trước** `lienKet`, đúng 1 lần mỗi cái |
| | `ghiSo = true` | gọi `GhiSoApi.ghiSo` 1 lần; `ghiSo = false` → 0 lần |
| | `hanhDong()` | `== SUA` ⇒ quyền suy ra là `Edit` |
| `TraLaiMapperTest` | `apDung` replace dòng | 3 dòng cũ + request 2 dòng → collection còn 2 dòng (`orphanRemoval`) |
| | không ghi đè trường hệ thống | `apDung` **không** đổi `id`, `tenant_id`, `ngay_tao`, `nguoi_tao`, `don_vi_id` |

### 7.2 Tích hợp (cần Docker — chưa chạy được)

| Lớp | Kiểm gì |
|---|---|
| `SuaTraLaiHangBanIT` | V33: tay ghi 1 dòng `acc_so_cai` rồi set `trangThaiChungTu = CHUA_GHI_SO` → `PUT` trả 409 `SO_CAI_LECH` |
| | `orphanRemoval`: xoá 1 dòng chi tiết → bảng con còn đúng n−1 dòng |
| | trigger bất biến: đổi `don_vi_id` → `PV_BB_001` (`V1:2875`) |
| | liên kết: sửa từ 2 dòng gốc xuống 1 dòng → `ctu_quan_he_chung_tu` còn 1 bản ghi; `daTieuThu` của dòng bị bỏ về 0 |
| | hai `PUT` đồng thời cùng `id` → một 200, một 409 (`STALE_DATA` hoặc `OptimisticLock`) |
| | sửa `ngayHachToan` sang kỳ đã khoá → 409 `_203`, rollback sạch |

---

## 8. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR3 popup | 1.1 — dùng chung request/DTO với Thêm mới |
| BR12 trạng thái + chống sửa đồng thời | V30, V32, §6 |
| BR14.1 chế độ form | FE có 4 chế độ; BE chỉ phân biệt tạo/sửa qua endpoint |
| BR14.3 hành vi form | `SCR_Sua:11-14` — số/ngày chứng từ read-only ⇒ V31 |
| BR15 validation | toàn bộ V1…V34 |
| BR17 kỳ kế toán | V6 với `ngayHachToan` **mới** |
| BR19.1 kiểm trùng | V8 — loại chính bản ghi đang sửa ra khỏi phép kiểm (`id ≠ current`) |
| BR21 grid chi tiết con | replace toàn bộ + đánh lại `thu_tu` |
| BR25 phân quyền | V1 (`.Edit`) |
| BR29.1 xóa mềm | V34 — bản ghi `da_xoa` coi như không tồn tại, **không** hồi sinh |
| BR34 sửa từ màn Xem chi tiết | FE mở popup Sửa với DTO của A4; không có endpoint riêng |
| BR41 tham chiếu chéo | **không áp dụng** — quan hệ nguồn↔đích của epic này là ràng buộc nghiệp vụ, không phải tham chiếu mềm (`business_rules.md:1012-1014`) |
| BR46 trường hệ thống | `ngay_cap_nhat`/`nguoi_cap_nhat` do base gán; client chỉ **đọc** `updatedAt` làm token |
