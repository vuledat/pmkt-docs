# 04 · `F02` — API ảnh nền của mẫu và logo đơn vị

| | |
|---|---|
| Mã chức năng | `F02` |
| UC nguồn | `PMKT-U-14549_21-01` (nhóm *Riêng của mẫu* và ô tick *Logo* của khối đầu trang) |
| Endpoint phụ trách | `A5` `A6` `A7` (ảnh nền) · `A12` (logo) |
| Quyết định gốc | `D7` (nhị phân là cột `bytea`, không base64 trong JSON) — quyết định **C08** |
| Luật phủ | `R-TLMI-069` · `071` · `073` · `074` · `075` · `082` |

> **Vì sao tách riêng khỏi `A2`:** nếu ảnh đi chung payload Lưu thì mỗi lần bấm Lưu phải đẩy lại ~1,4 MB base64 kể cả khi chỉ đổi một ô căn lề. Tách endpoint `multipart` ⇒ ảnh tải một lần, độc lập vòng đời với JSON mẫu.

---

## §1. Hằng số dùng chung

```java
/** R-TLMI-069 — ảnh nền và logo: jpg/png, ≤ 1MB. */
public static final long ANH_MAX_BYTE = 1L * 1024 * 1024;
public static final Set<String> ANH_KIEU_TEP = Set.of("image/jpeg", "image/png");
public static final Set<String> ANH_DUOI_TEP = Set.of("jpg", "jpeg", "png");
```

Đặt ở `cell/mau_in/internal/model/GioiHanMauIn.java` (gương của `gioiHan.ts` phía FE).

**Kiểm ở server, không tin phần mở rộng tên tệp:** đọc **magic bytes** đầu tệp (`FF D8 FF` = JPEG, `89 50 4E 47` = PNG) rồi mới so với `Content-Type`. Lệch ⇒ từ chối. Lý do: `R-TLMI-246` (*không được tin FE đã kiểm*), và một tệp `.exe` đổi tên thành `.png` mà lọt xuống `bytea` thì sẽ được trả lại nguyên si ở `A6`.

---

## §2. Ảnh nền của một mẫu

### 2.1 `A5` — Tải lên

```
POST /api/mau-in/{maLoai}/{maNghiepVu}/anh-nen
Content-Type: multipart/form-data
```

**Quyền:** `HTMauIn.Edit`.

| Part | Kiểu | Bắt buộc | Ràng buộc |
|---|---|---|---|
| `tep` | file | ✔ | jpg/png, ≤ 1 MB (kiểm cả `Content-Type` lẫn magic bytes) |

**Response** `ApiResponse<AnhNenDto>`:

```json
{ "data": { "coAnh": true, "kieuTep": "image/png", "tenTep": "nen-cong-ty.png", "kichThuoc": 284133 } }
```

**Luồng:**

1. `quyen.require(HT_MAU_IN, EDIT)`.
2. Kiểm tệp → sai ⇒ `422` + `MSG_PMKT-E-14549_21_209` *"Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB"*.
3. **Bản ghi mẫu chưa tồn tại** ⇒ tạo một bản ghi tối thiểu mang mẫu chuẩn đã chuẩn hoá, rồi mới ghi ảnh.
   > ⚠ **Ngoại lệ có chủ ý của `INV-TLMI-002`.** Bất biến nói *mẫu bằng chuẩn ⇒ không tồn tại bản ghi*, nhưng ảnh nền phải có chỗ bám. Xử lý: bản ghi này **luôn** đi kèm `trang.nen.kieu = "ANH"` do FE đặt cùng lúc ⇒ mẫu **khác** mẫu chuẩn ⇒ bất biến không vỡ. `KiemTraMau` bổ sung một luật chốt điều đó: *có `anh_nen` mà `trang.nen.kieu != "ANH"` ⇒ xoá ảnh khi Lưu*.
4. `UPDATE … SET anh_nen = ?, anh_nen_kieu_tep = ?, anh_nen_ten_tep = ?` — **không** đụng `cau_hinh`, **không** tăng `phien_ban` (tránh làm hỏng khoá lạc quan của màn đang mở).

### 2.2 `A6` — Tải về

```
GET /api/mau-in/{maLoai}/{maNghiepVu}/anh-nen
```

**Quyền:** `HTMauIn.View`.

- Trả **bytes thô**, `Content-Type` = `anh_nen_kieu_tep`, `Content-Disposition: inline; filename="<anh_nen_ten_tep>"`.
- **Không** bọc `ApiResponse` — đây là tài nguyên nhị phân, FE dùng thẳng làm `src`.
- Không có ảnh ⇒ `404`.
- `Cache-Control: private, max-age=0, must-revalidate` + `ETag` theo `md5(anh_nen)` ⇒ đổi ảnh thì trình duyệt nạp lại ngay.

### 2.3 `A7` — Bỏ ảnh

```
DELETE /api/mau-in/{maLoai}/{maNghiepVu}/anh-nen
```

**Quyền:** `HTMauIn.Edit`. `UPDATE … SET anh_nen = NULL, anh_nen_kieu_tep = NULL, anh_nen_ten_tep = NULL`.

### 2.4 Quan hệ với JSON mẫu

| `trang.nen.kieu` | Cột `anh_nen` | Bản in |
|---|---|---|
| `KHONG` | bất kỳ | không in hình nền (`R-TLMI-067`) |
| `KHUNG_VIEN` | bất kỳ | kẻ khung quanh mép trang theo `trang.mauChu`, độ đậm `nen.doDam` (`R-TLMI-068` · `072`) |
| `ANH` | có | in ảnh theo `nen.canAnh` và `nen.doDam` (`R-TLMI-073` · `074`) |
| `ANH` | **NULL** | **coi như `KHONG`**, không báo lỗi — bản in không bao giờ được vỡ vì cấu hình cũ (tinh thần quyết định **C10**) |

Hình nền luôn vẽ **dưới mọi khối** và **không ảnh hưởng vị trí khối** (`R-TLMI-075` · `263`) — việc của FE (`D3`).

---

## §3. `A12` — Logo đơn vị

```
POST   /api/mau-in/thiet-lap-chung/logo      quyền HTThongTinCongTy.Edit
GET    /api/mau-in/thiet-lap-chung/logo      quyền HTThongTinCongTy.View.Detail
DELETE /api/mau-in/thiet-lap-chung/logo      quyền HTThongTinCongTy.Edit
```

Cùng ràng buộc tệp như §1. Ghi vào `iam_tenant.logo` / `logo_kieu_tep` / `logo_ten_tep` (`V1160`).

| Điểm | Nội dung | Luật |
|---|---|---|
| **Một logo cho cả đơn vị kế toán** | Chi nhánh **không** có logo riêng — bản in của chi nhánh B mang logo pháp nhân trong khi tên/địa chỉ/MST là của chi nhánh B. **Đúng tài liệu, không phải bug** | `R-TLMI-078` Ghi chú |
| **Logo là ô tick thứ 7** của khối đầu trang, mẫu sửa riêng được | `khoi[DAU_TRANG].dong.logo` | `R-TLMI-082` · quyết định **C03** |
| **Màu chữ KHÔNG áp cho logo** | `trang.mauChu` áp cho toàn bộ chữ và đường kẻ, **trừ logo** | `R-TLMI-065` |
| **Vị trí logo** | Luôn bên **trái** khối thông tin đơn vị, **cùng hàng với dòng đầu tiên**; căn lề áp cho **cả cụm** (logo + các dòng chữ), không tách riêng | quyết định **C29** |
| `dong.logo = true` mà **chưa tải logo** | Bỏ qua, không in chỗ trống | `R-TLMI-079` |

---

## §4. Mã lỗi

| Tình huống | HTTP | Mã message |
|---|---|---|
| Thiếu quyền | `403` | `MSG_PMKT-E-14549_21_002` |
| Sai định dạng hoặc quá 1 MB | `422` | `MSG_PMKT-E-14549_21_209` |
| Magic bytes không khớp `Content-Type` | `422` | `MSG_PMKT-E-14549_21_209` |
| `GET` mà chưa có ảnh | `404` | — |
| Lỗi hệ thống | `500` | `MSG_PMKT-E-14549_21_003` |

Cấu hình Spring cần đặt (`application.yml`):

```yaml
spring:
  servlet:
    multipart:
      max-file-size: 2MB        # > 1MB để lỗi được xử lý bằng MSG_209 thay vì 413 trần
      max-request-size: 2MB
```

---

## §5. Kiểm thử

| Test | Input → kỳ vọng | Luật |
|---|---|---|
| `R_TLMI_069_anhNenChiNhanJpgPngDuoi1MB` | `.gif` → `422` `MSG_…_209`; `.png` 2 MB → `422`; `.png` 300 KB → `200` | `R-TLMI-069` |
| `R_TLMI_069_kiemMagicBytesKhongTinPhanMoRong` | Tệp `.png` nhưng nội dung là ZIP → `422` | `R-TLMI-069` · `246` |
| `R_TLMI_071_canAnhChiCoNghiaKhiKieuLaAnh` | `nen.kieu = "KHUNG_VIEN"` mà có `canAnh` → `ChuanHoaMau` xoá khoá `canAnh` | `R-TLMI-071` |
| `R_TLMI_067_kieuAnhMaThieuAnhThiCoiNhuKhong` | `kieu = "ANH"`, `anh_nen = NULL` → `A9` trả bản in **không** có hình nền, **không** lỗi | `R-TLMI-067` · C10 |
| `R_TLMI_082_logoLaOTickThu7` | `dong.logo = false` → khối đầu trang không có logo dù tenant đã tải logo | `R-TLMI-082` |
| `R_TLMI_065_mauChuKhongApChoLogo` | `mauChu = "#FF0000"` → dữ liệu trả về đánh dấu logo **không** nhận màu | `R-TLMI-065` |
| `AnhServiceTest_taiAnhKhongTangPhienBan` | `A5` → `phien_ban` của bản ghi **không đổi** | D6 |
| `AnhServiceTest_xoaAnhThiBaCotVeNull` | `A7` → cả 3 cột `NULL` | — |
