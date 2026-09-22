# 02 · Hợp đồng JSON của thiết lập chung + cổng hồ sơ đơn vị

| | |
|---|---|
| Mã | `F06` |
| Quyết định gốc | `D8` (lưu JSON trên `cfg_cau_hinh_he_thong`) · `D7` (logo là `bytea` trên `iam_tenant`) · `D9` (`HoSoDonViPort`) |
| Nguồn nghiệp vụ | `04-quyet-dinh-ban-giao.md` §1 **Q-03** `[USER]` — làm **tầng tối thiểu** của epic `PMKT-E-14549_20`, không làm cả epic |
| Luật phủ | `R-TLMI-036`…`052` · `054`…`063` (mặc định hệ thống) · `077` · `078` · `079` · `082` · `083` · `084` · `186` · `188` · `196` · `199` · `261` · `266` · `267` |

> **Vì sao phiếu `_21` phải làm phần của `_20`:** mọi ô của nhóm *Giấy và chữ* và 7 ô tick đầu trang đều **mặc định theo thiết lập chung** (`R-TLMI-036`), và bản in phải **đọc lại thiết lập chung tại lúc in** (`R-TLMI-038`). Không có tầng này thì `_21` không chạy được — `01-conflict.md` C12.

---

## §1. Nơi lưu

| Dữ liệu | Nơi | Migration |
|---|---|---|
| JSON thiết lập chung | `cfg_cau_hinh_he_thong` — một dòng/tenant: `ma_cau_hinh = 'IN_CHUNG_CHUNG_TU'`, `nhom = 'IN'`, `kieu_du_lieu = 'JSON'`, `ten_cau_hinh = 'Cấu hình in chứng từ'`, `gia_tri` = JSON §2 | **không cần** — bảng đã có `V1__create_database.sql:6134-6157`, ràng buộc `kieu_du_lieu` đã cho phép `'JSON'` (`:6154`) |
| Logo đơn vị | `iam_tenant.logo bytea` + `logo_kieu_tep` + `logo_ten_tep` | `V1160` |
| 5 người ký + cờ *In tên người ký* | **đã có** — `iam_tenant` (`V203`), DTO `platform_iam/tenant/internal/dto/CompanyInfoResponse.java:24-35` | — |
| Tên · địa chỉ · MST · điện thoại · email · tài khoản ngân hàng | **đã có** — `iam_tenant` (`V203`), `CompanyInfoResponse.java:13-23` | — |

**Không seed dòng `IN_CHUNG_CHUNG_TU`.** Thiếu dòng ⇒ đọc ra JSON rỗng `{}` ⇒ mọi khoá về **mặc định hệ thống** (§2). Tránh phải backfill cho mọi tenant hiện có, và đúng nguyên tắc D4 (*vắng = mặc định*).

---

## §2. JSON schema — `ThietLapChungJson`

```json
{
  "schemaVersion": 1,
  "giayVaChu": {
    "kho": "A4",
    "huong": "TU_DONG",
    "soCotTuDongNgang": 7,
    "leTren": 2.0, "leDuoi": 2.0, "leTrai": 2.0, "lePhai": 2.0,
    "font": "Times New Roman",
    "coChu": 12
  },
  "dauTrang": {
    "tenDonVi": true, "diaChi": true, "mst": true,
    "soDienThoai": false, "email": false, "taiKhoanNganHang": false, "logo": true,
    "lapLaiTrangSau": true
  },
  "quyTacIn": {
    "choInChuaGhiSo": true,
    "choInDaKhoaSo": false,
    "congGopMatHang": false
  }
}
```

### 2.1 `giayVaChu` — mặc định cho mọi mẫu (`R-TLMI-053`)

| Khoá | Kiểu | Miền | **Mặc định hệ thống** (khi khoá vắng) | Luật |
|---|---|---|---|---|
| `kho` | `String` | `A3` · `A4` · `A5` | **`A4`** | `R-TLMI-054` |
| `huong` | `String` | `DOC` · `NGANG` · `TU_DONG` | **`TU_DONG`** | `R-TLMI-055` |
| `soCotTuDongNgang` | `Integer` | `1…50` | **`7`** | `R-TLMI-057` |
| `leTren` · `leDuoi` · `leTrai` · `lePhai` | `Double` | `0…5` cm, ≤ 1 chữ số lẻ | **`2.0`** | `R-TLMI-061` |
| `font` | `String` | `Times New Roman` · `Arial` | **`Times New Roman`** | `R-TLMI-062` |
| `coChu` | `Integer` | `8…20` | **`12`** | `R-TLMI-063` |

Đây chính là tầng mà `HopNhatThietLapChung` lấy giá trị khi một khoá của `mauIn.trang` vắng mặt (`R-TLMI-038`).

### 2.2 `dauTrang` — 7 dòng in + cờ lặp trang (`R-TLMI-077` · `084`)

| Khoá | Kiểu | **Mặc định hệ thống** | Mẫu sửa riêng được? | Luật |
|---|---|---|---|---|
| `tenDonVi` | `Boolean` | `true` | ✔ | `R-TLMI-077` |
| `diaChi` | `Boolean` | `true` | ✔ | `R-TLMI-077` |
| `mst` | `Boolean` | `true` | ✔ | `R-TLMI-077` |
| `soDienThoai` | `Boolean` | `false` | ✔ | `R-TLMI-077` |
| `email` | `Boolean` | `false` | ✔ | `R-TLMI-077` |
| `taiKhoanNganHang` | `Boolean` | `false` | ✔ | `R-TLMI-077` |
| `logo` | `Boolean` | `true` | ✔ (quyết định **C03**) | `R-TLMI-082` |
| `lapLaiTrangSau` | `Boolean` | `true` | ❌ **luôn theo chung** | `R-TLMI-049` · `084` |

**Thứ tự in cố định** (`R-TLMI-083`), không có ô cấu hình thứ tự:

> Tên đơn vị → Địa chỉ → Mã số thuế → Số điện thoại → Email → Tài khoản ngân hàng → *(Logo nằm bên trái cụm, cùng hàng với dòng đầu tiên — quyết định C29)*

**Không đưa vào JSON này** (thuộc epic `_20` đầy đủ, ngoài phạm vi Q-03): kiểu chữ riêng của khối đầu trang · in hoa · cỡ logo · căn lề cụm. Khi epic `_20` ra đời thì **bổ sung khoá vào chính JSON này**, không đổi chỗ lưu.

### 2.3 `quyTacIn` — ba quy tắc in chứng từ (`R-TLMI-047` · `266`)

| Khoá | Kiểu | **Mặc định hệ thống** | Áp ở đâu | Luật |
|---|---|---|---|---|
| `choInChuaGhiSo` | `Boolean` | `true` | `A8` (menu In) · `A9` (dựng bản in) — `false` + chứng từ chưa ghi sổ ⇒ **cả menu In không mở được** | `R-TLMI-261` · `266`(a) |
| `choInDaKhoaSo` | `Boolean` | `false` | như trên; ⚠ **chỉ tác động nút In của chứng từ**, **không** tác động báo cáo và **không** tác động Xuất Excel | `R-TLMI-261` · `266`(b) |
| `congGopMatHang` | `Boolean` | `false` | `CongGopDong` — chỉ áp khi **bật** *và* loại chứng từ **thuộc diện cộng gộp** (D14) | `R-TLMI-119` · `266`(c) |

**Mẫu in KHÔNG có ô chỉnh ba quy tắc này và KHÔNG lưu riêng** (`R-TLMI-047`).

**Nguyên văn tooltip khi nút In bị disable** (`R-TLMI-261`; BA chưa cấp mã `MSG_`, quyết định C14 — chỉ có key i18n):

> *"Đơn vị không cho phép in chứng từ chưa ghi sổ"*
> *"Đơn vị không cho phép in chứng từ đã khóa sổ"*

### 2.4 Cái KHÔNG nằm trong JSON này

| Thứ | Vì sao | Ở đâu |
|---|---|---|
| 5 người ký (tiêu đề + tên) và cờ *In tên người ký trên chứng từ, báo cáo* | **đã có sẵn** trên `iam_tenant` từ `V203` | `CompanyInfoResponse.java:24-35`; đọc qua `HoSoDonViPort` |
| Logo (ảnh) | nhị phân — D7 | `iam_tenant.logo bytea` (`V1160`) |
| Mục *Bố cục mặc định của báo cáo* (lặp tiêu đề cột, cột STT, cộng chuyển trang) | **KHÔNG áp cho chứng từ** — mỗi khối Bảng tự có ba tuỳ chọn tương đương | `R-TLMI-048` · `096` · `097` · `099` |

---

## §3. `HoSoDonViPort` — cổng duy nhất (Q-14)

```java
package vn.vtt.pmkt.cell.mau_in.internal.port;

/**
 * Q-14 — CỔNG DUY NHẤT tới hồ sơ đơn vị dùng để in.
 * R-TLMI-078 · R-TLMI-199 · R-TLMI-267 — hồ sơ của CHI NHÁNH GHI TRÊN CHỨNG TỪ,
 * KHÔNG phải chi nhánh đang làm việc.
 */
public interface HoSoDonViPort {
    HoSoDonVi theoChiNhanh(UUID chiNhanhId);
}

public record HoSoDonVi(
        String tenDonVi,
        String diaChi,
        String mst,
        String soDienThoai,
        String email,
        String taiKhoanNganHang,          // đã dựng chuỗi "<số TK> - <ngân hàng>"
        boolean coLogo,                   // R-TLMI-078 Ghi chú — logo LUÔN của pháp nhân
        Map<VaiTroKy, NguoiKy> nguoiKy,   // R-TLMI-186 · 188
        boolean inTenNguoiKy) {           // R-TLMI-196 — cờ chung, chỉ đọc

    public record NguoiKy(String tieuDe, String ten) {}
}
```

### 3.1 Hiện thực bản này — `HoSoDonViTheoTenant`

```java
@Component
class HoSoDonViTheoTenant implements HoSoDonViPort {
    /** L-7 — `cfg_chi_nhanh` chưa tồn tại: BỎ QUA chiNhanhId, trả hồ sơ của tenant. */
    @Override public HoSoDonVi theoChiNhanh(UUID chiNhanhId) { … }
}
```

- Nguồn dữ liệu: `platform_iam.tenant.api.TenantConfigApi` (đã có; `TenantConfigApi.java` đang ở trạng thái ` M` chưa commit) → `CompanyInfoResponse`.
- Tên tỉnh/phường để dựng `diaChi` đầy đủ: native query đã có ở `cell/mau_in/internal/repository/TraCuuMauInRepository.java` (ngoại lệ `master_data` đã ghi ở `cell/mau_in/package-info.java`).
- Tài khoản ngân hàng: `CompanyInfoResponse.taiKhoanNganHangId` → tra qua cùng repository.

### 3.2 Luật bắt buộc cho tầng trên

| Luật | Nội dung |
|---|---|
| **Cấm** gọi thẳng `TenantConfigApi` từ `DungKhoiDauTrang`, `DungKhoiChuKy`, `DungBanInService`, `XemTruocService` | mọi hồ sơ đơn vị đi qua `HoSoDonViPort` |
| Tham số `chiNhanhId` **luôn** là `chungTu.chiNhanhId`, **không bao giờ** là chi nhánh phiên làm việc | `R-TLMI-078` · `267` · quyết định C05 |
| Dòng đã tick nhưng hồ sơ **trống** ⇒ **bỏ qua dòng**, không in dòng trống | `R-TLMI-079` |

Khi `cfg_chi_nhanh` ra đời: thêm `HoSoDonViTheoChiNhanh`, đánh dấu `@Primary` hoặc chọn bằng `@ConditionalOnProperty`, **không sửa** một dòng nào ở tầng trên. Đó là toàn bộ mục đích của cổng này.

---

## §4. Endpoint

Chi tiết hợp đồng: [03-api-thiet-lap-mau-in.md](03-api-thiet-lap-mau-in.md) §5 (`A10` · `A11`) và [04-api-anh-nen-va-logo.md](04-api-anh-nen-va-logo.md) §3 (`A12`).

| # | Method · Path | Quyền | Ghi chú |
|---|---|---|---|
| `A10` | `GET /api/mau-in/thiet-lap-chung` | `HTThongTinCongTy.View.Detail` | Trả JSON **đã điền mặc định hệ thống** cho mọi khoá vắng — client không phải biết bảng mặc định |
| `A11` | `PUT /api/mau-in/thiet-lap-chung` | `HTThongTinCongTy.Edit` | Ghi **nguyên JSON**; miền giá trị kiểm như §2; khoá lạc quan bằng `cfg_cau_hinh_he_thong.phien_ban` |
| `A12` | `POST` · `GET` · `DELETE /api/mau-in/thiet-lap-chung/logo` | `.Edit` / `.View.Detail` | `multipart`, jpg/png ≤ 1 MB |

> ⚠ **§12 `Q4`** — dùng `HTThongTinCongTy.*` là **đề xuất**, vì thiết lập chung nằm cùng nhóm với màn *Thông tin công ty* và epic `_20` chưa khai mã quyền nào. BA có thể muốn mã riêng.

---

## §5. Kiểm thử

| Test | Nội dung | Luật |
|---|---|---|
| `R_TLMI_038_thietLapChungDoiThiMauDoiTheo` | Mẫu có `trang.kho` vắng → hợp nhất với `giayVaChu.kho = "A5"` ⇒ ra `A5`; đổi thiết lập chung thành `A3` ⇒ cùng mẫu đó ra `A3` | `R-TLMI-038` |
| `R_TLMI_039_oRiengKhongDoiTheoThietLapChung` | Mẫu có `trang.kho = "A3"`; đổi `giayVaChu.kho` ⇒ vẫn `A3` | `R-TLMI-039` |
| `R_TLMI_077_bayOTickDauTrangKeThuaTungO` | `dong = {"soDienThoai": true}` + thiết lập chung tắt điện thoại ⇒ chỉ mẫu này in điện thoại, 6 dòng còn lại theo chung | `R-TLMI-077` |
| `R_TLMI_079_hoSoTrongThiBoQuaDong` | `dong.email = true` nhưng `HoSoDonVi.email` rỗng ⇒ không in dòng trống | `R-TLMI-079` |
| `R_TLMI_083_thuTuDongDauTrangCoDinh` | Dựng khối đầu trang ⇒ đúng thứ tự 7 dòng | `R-TLMI-083` |
| `R_TLMI_047_baQuyTacInLuonTheoThietLapChung` | JSON mẫu mang khoá `quyTacIn` ⇒ `MauInJsonCodec` **từ chối** (thuộc tính lạ) | `R-TLMI-047` |
| `R_TLMI_267_hoSoDonViDocTheoChiNhanhTrenChungTu` | `DungBanInService` gọi `HoSoDonViPort.theoChiNhanh(chungTu.chiNhanhId)`, **không** gọi với chi nhánh phiên | `R-TLMI-267` |
| `R_TLMI_196_coInTenNguoiKyLuonTheoThietLapChung` | JSON mẫu mang `khoi[CHU_KY].inTen` ⇒ từ chối | `R-TLMI-196` |
| `ThietLapChungServiceTest_khongCoDongThiTraMacDinhHeThong` | `cfg_cau_hinh_he_thong` không có dòng ⇒ `A10` trả đủ bộ mặc định §2 | D8 |
