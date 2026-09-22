# 01 · Hợp đồng JSON của mẫu in — thay cho ERD

| | |
|---|---|
| Mã | `F00` (nền của mọi chức năng) |
| Quyết định gốc | `D1` (một bản ghi một `jsonb`) · `D4` (khoá vắng mặt = theo chung) · `D11` (schema v2) |
| Nơi lưu | `prn_mau_in_tuy_chinh.cau_hinh jsonb` |
| Gương phía FE | `client/src/base/domainKit/mauIn/api/schemas.ts` (Zod) — mọi thay đổi phải sửa **cả hai** |
| Luật phủ | `R-TLMI-004` `006` `008` `009` `036`…`039` `053`…`075` `076`…`091` `092`…`118` `120`…`181` `182`…`198` `201`…`216` |

> **Đây là hợp đồng kỹ thuật thay cho ERD** (quyết định C09). 5 "entity" của `3.crud-matrix.md` ánh xạ thành 5 nhánh:
>
> | Entity trong `3.crud-matrix.md` | Nhánh JSON |
> |---|---|
> | `ENT_cfg_mau_in_chung_tu` | gốc + `trang` |
> | `ENT_cfg_mau_in_khoi` | `khoi[]` |
> | `ENT_cfg_mau_in_khoi_cot` | `khoi[loai=BANG].cot[]` |
> | `ENT_cfg_mau_in_khoi_o` | `khoi[loai=TU_DO].o[]` |
> | `ENT_cfg_mau_in_khoi_chu_ky` | `khoi[loai=CHU_KY].o[]` |

---

## §1. Ba quy ước đọc schema — đọc trước mọi thứ khác

### 1.1 **KHOÁ VẮNG MẶT = theo thiết lập chung** (`R-TLMI-037` · `INV-TLMI-003`)

Đánh dấu bằng ký hiệu **`⟨kế thừa⟩`** trong mọi bảng dưới đây.

- Ô *theo chung* ⇒ **khoá không xuất hiện trong JSON**. **KHÔNG** ghi `null`, **KHÔNG** ghi giá trị đang hiển thị trên màn.
- Ô *riêng* ⇒ khoá có mặt với giá trị thật.
- Đọc để in / để vẽ xem trước ⇒ `HopNhatThietLapChung` điền khoá vắng bằng thiết lập chung **tại thời điểm đó** (`R-TLMI-038`).
- `ChuanHoaMau` **xoá** mọi khoá `null` trước khi ghi — nên `null` không bao giờ nằm trong DB.

**Ngoại lệ duy nhất — chuỗi rỗng KHÁC vắng mặt:**

| Khoá | `""` (rỗng) nghĩa là | vắng mặt nghĩa là |
|---|---|---|
| `khoi[BANG].tenBang` | không in tên bảng (`R-TLMI-094`) | như `""` — chuẩn hoá quy về vắng mặt |
| `truong.<ma>.tenHienThi` | **chỉ in giá trị**, không in nhãn và dấu `:` (`R-TLMI-145`) | dùng tên trường mặc định của catalog (`R-TLMI-157`) |

### 1.2 Thứ tự mảng = thứ tự in

| Mảng | Thứ tự quyết định gì | Luật |
|---|---|---|
| `khoi[]` | thứ tự khối trên bản in | `R-TLMI-204` · `205` · `262` |
| `khoi[BANG].cot[]` | thứ tự cột trong bảng | `R-TLMI-115` |
| `khoi[CHU_KY].o[]` | thứ tự ô ký trái→phải, trên→xuống | `R-TLMI-183` |

Không có khoá `thuTu` / `viTri` nào — vị trí trong mảng **là** thứ tự. (`R-TLMI-128`: bảng chỉnh khối tự do **không có cột Vị trí**.)

### 1.3 Không có id kỹ thuật trong JSON đã lưu

`id` của khối là **id ổn định suy ra được** (`dau_trang`, `tieu_de`, `bang_<maLuoi>`, `chu_ky`, `tu_do_<n>`), không phải UUID sinh ngẫu nhiên. `ChuanHoaMau` đánh số lại `tu_do_1…tu_do_n` theo thứ tự mảng ⇒ so sánh với mẫu chuẩn không bao giờ lệch vì id.

---

## §2. Gốc — `MauInJson`

```json
{
  "schemaVersion": 2,
  "maLoaiChungTu": "BH",
  "maNghiepVu": "MAC_DINH",
  "trang": { },
  "truong": { },
  "khoi": [ ]
}
```

| Khoá | Kiểu | Bắt buộc | Ràng buộc | Luật |
|---|---|---|---|---|
| `schemaVersion` | `Integer` | ✔ | **luôn `2`**; khác ⇒ `MauInJsonCodec` từ chối | `D11` |
| `maLoaiChungTu` | `String` | ✔ | ≤ 20 ký tự, khớp `mst_loai_chung_tu.code` và khớp `provider.maLoaiChungTu()` | `R-TLMI-004` |
| `maNghiepVu` | `String` | ✔ | ≤ 50 ký tự; loại không chia nghiệp vụ ⇒ `"MAC_DINH"` | `R-TLMI-002` · `003` · `004` |
| `trang` | object | ✔ | §3 | `R-TLMI-053`…`075` |
| `truong` | map | ✔ (có thể `{}`) | thuộc tính **của trường**, dùng chung cả mẫu | `R-TLMI-156` · `157` · `164` · `INV-TLMI-009` |
| `khoi` | array | ✔ | §4 — đúng 1 `DAU_TRANG`, 1 `TIEU_DE`, n `BANG`, 1 `CHU_KY`, 0…10 `TU_DO` | `R-TLMI-008` · `009` · `125` · `INV-TLMI-008` |

**Java:**

```java
@JsonInclude(JsonInclude.Include.NON_NULL)
public record MauInJson(
        Integer schemaVersion,
        String maLoaiChungTu,
        String maNghiepVu,
        TrangJson trang,
        Map<String, ThuocTinhTruongJson> truong,
        List<KhoiJson> khoi) { … }
```

---

## §3. `trang` — Giấy và chữ + riêng của mẫu

```json
"trang": {
  "kho": "A4",
  "huong": "TU_DONG",
  "soCotTuDongNgang": 7,
  "leTren": 1.5, "leDuoi": 1.5, "leTrai": 2.0, "lePhai": 1.0,
  "font": "Times New Roman",
  "coChu": 12,

  "mauChu": "#000000",
  "nen": { "kieu": "ANH", "doDam": 20, "canAnh": "GIUA_TRANG" }
}
```

### 3.1 Nhóm **Giấy và chữ** — toàn bộ `⟨kế thừa⟩`

| Khoá | Kiểu | `⟨kế thừa⟩` | Miền giá trị | Mặc định hệ thống | Message khi sai | Luật |
|---|---|---|---|---|---|---|
| `kho` | `String` | ✔ | `A3` · `A4` · `A5` | `A4` | — (ô chọn) | `R-TLMI-054` |
| `huong` | `String` | ✔ | `DOC` · `NGANG` · `TU_DONG` | `TU_DONG` | — (ô chọn) | `R-TLMI-055` |
| `soCotTuDongNgang` | `Integer` | ✔ | `1…50`; **chỉ kiểm khi `huong = TU_DONG`** | `7` | `MSG_…_214` | `R-TLMI-056` · `057` |
| `leTren` · `leDuoi` · `leTrai` · `lePhai` | `Double` | ✔ (**từng cạnh riêng**) | `0…5` cm, **tối đa 1 chữ số lẻ** | `2.0` | `MSG_…_213` | `R-TLMI-061` |
| `font` | `String` | ✔ | **chỉ** `Times New Roman` · `Arial` | `Times New Roman` | — (ô chọn) | `R-TLMI-062` |
| `coChu` | `Integer` | ✔ | `8…20` | `12` | `MSG_…_215` — **chỉ chặn phía máy chủ** | `R-TLMI-063` |

> **Vì sao 4 lề phẳng chứ không lồng `le: {tren, duoi, trai, phai}`:** bảng kiểm tra `R-TLMI-239` V14 xét **từng cạnh** và `R-TLMI-036` cho mỗi ô một trạng thái *theo chung / riêng* độc lập. Lồng object thì "3 trong 4 cạnh kế thừa" phải biểu diễn bằng object có 1 khoá — hợp lệ nhưng dễ bị code sinh ra `le: {tren: 2, duoi: null, …}` và `null` lọt xuống DB. Phẳng thì `@JsonInclude(NON_NULL)` xử lý đúng ngay từ tầng Jackson. **Đây là chỗ khác `TrangJson.Le` của bản cũ** (`cell/mau_in/internal/model/json/TrangJson.java:65`).

### 3.2 Nhóm **riêng của mẫu** — LUÔN CÓ MẶT, không kế thừa

| Khoá | Kiểu | Bắt buộc | Miền | Mặc định | Message | Luật |
|---|---|---|---|---|---|---|
| `mauChu` | `String` | ✔ | `^#[0-9a-fA-F]{6}$` | `#000000` | `MSG_…_210` | `R-TLMI-064` · `065` · `066` |
| `nen.kieu` | `String` | ✔ | `KHONG` · `KHUNG_VIEN` · `ANH` | `KHONG` | — | `R-TLMI-067` · `068` · `069` |
| `nen.doDam` | `Integer` | ✔ **khi** `kieu != KHONG` | `5…100` | `20` | ⚠ **BA chưa cấp mã** — `02-rules.md` §Z | `R-TLMI-070` · `072` |
| `nen.canAnh` | `String` | ✔ **khi** `kieu = ANH` | `GIUA_TRANG` · `TOAN_TRANG` | `GIUA_TRANG` | — | `R-TLMI-071` · `073` · `074` |

- `mauChu` áp cho **toàn bộ chữ và đường kẻ**, **trừ logo** (`R-TLMI-065`); `KHUNG_VIEN` cũng kẻ theo `mauChu` (`R-TLMI-068`).
- **Ảnh không nằm trong JSON** — cột `prn_mau_in_tuy_chinh.anh_nen bytea` (quyết định C08 / D7). `kieu = "ANH"` mà cột `anh_nen` `NULL` ⇒ coi như `KHONG` khi dựng bản in, **không** báo lỗi.
- Hình nền vẽ **dưới mọi khối**, không ảnh hưởng vị trí khối (`R-TLMI-075` · `263`) — việc của FE (D3).

---

## §4. `khoi[]` — bốn loại chuẩn + khối tự do

### 4.0 Phần chung của mọi khối

```json
{ "id": "tieu_de", "loai": "TIEU_DE", "ten": "Tiêu đề", "hien": true }
```

| Khoá | Kiểu | Bắt buộc | Ý nghĩa | Luật |
|---|---|---|---|---|
| `id` | `String` | ✔ | id ổn định (§1.3) | — |
| `loai` | `String` | ✔ | `DAU_TRANG` · `TIEU_DE` · `BANG` · `CHU_KY` · `TU_DO` | `R-TLMI-008` |
| `ten` | `String` | ✔ | tên hiển thị ở **Bố cục mẫu**; cố định với khối chuẩn, sửa được với `TU_DO` | `R-TLMI-212` · `121` · `127` |
| `hien` | `boolean` | ✔ | con mắt — `false` ⇒ **không in**, các khối sau **dồn lên**; thiết lập bên trong **giữ nguyên** | `R-TLMI-207` · `208` · `209` |

**Không có** khoá `khoa` (xoá được / kéo được) như bản cũ (`KhoiJson.khoa()`): suy ra được từ `loai` — khối chuẩn không xoá được (`R-TLMI-210`), khối `TU_DO` xoá được (`R-TLMI-211`), **mọi khối** đều kéo được (`R-TLMI-206`). Lưu một thứ suy ra được là mở đường cho dữ liệu tự mâu thuẫn.

**Không có** khoá `coChu` dùng chung cho mọi khối như bản cũ (`KhoiJson.coChu()`): đặc tả mới chỉ cho **khối Tiêu đề** có cỡ chữ riêng (`R-TLMI-086`). Mọi khối khác dùng `trang.coChu`.

> ⚠ Sáu loại khối của bản cũ — `DON_VI`, `TIEU_DE`, `THONG_TIN`, `BANG`, `TONG_HOP`, `CHU_KY`, `TU_DO` — **giảm còn năm**. `THONG_TIN` (thông tin chung) và `TONG_HOP` (tổng tiền) **bị bỏ**: `R-TLMI-008` nói "**không có khối nào khác**", `R-TLMI-010` nói thẳng *"Thông tin chung / tổng tiền phải tự dựng bằng khối tự do"*. `DON_VI` đổi tên thành `DAU_TRANG` cho khớp nhãn BA ("Thông tin đầu trang").

### 4.1 `DAU_TRANG` — khối Thông tin đầu trang

```json
{
  "id": "dau_trang", "loai": "DAU_TRANG", "ten": "Thông tin đầu trang", "hien": true,
  "dong": { "soDienThoai": true }
}
```

| Khoá | Kiểu | `⟨kế thừa⟩` | Mặc định hệ thống | Luật |
|---|---|---|---|---|
| `hien` | `boolean` | ❌ (riêng của mẫu) | `true` — ô tick nguyên văn *"In khối Thông tin đầu trang trên mẫu này"* | `R-TLMI-076` |
| `dong.tenDonVi` | `Boolean` | ✔ | `true` | `R-TLMI-077` |
| `dong.diaChi` | `Boolean` | ✔ | `true` | `R-TLMI-077` |
| `dong.mst` | `Boolean` | ✔ | `true` | `R-TLMI-077` |
| `dong.soDienThoai` | `Boolean` | ✔ | `false` | `R-TLMI-077` |
| `dong.email` | `Boolean` | ✔ | `false` | `R-TLMI-077` |
| `dong.taiKhoanNganHang` | `Boolean` | ✔ | `false` | `R-TLMI-077` |
| `dong.logo` | `Boolean` | ✔ | `true` | `R-TLMI-082` (quyết định **C03: CÓ**, logo là ô tick thứ 7) |

Ví dụ trên đọc là: *sáu dòng theo thiết lập chung, riêng Số điện thoại thì mẫu này bật* — đúng ví dụ nguyên văn của BA (`R-TLMI-077` Ghi chú).

**Không lưu** (luôn theo thiết lập chung — `R-TLMI-049`): thứ tự dòng (cố định, `R-TLMI-083`) · kiểu chữ · in hoa · cỡ logo · căn lề của cụm · cờ *lặp đầu trang* (`R-TLMI-084`).
**Không lưu** nội dung các dòng: lấy từ `HoSoDonViPort.theoChiNhanh(chungTu.chiNhanhId)` lúc in (`R-TLMI-078`); hồ sơ trống ⇒ **bỏ qua dòng**, không in dòng trống (`R-TLMI-079`). Bỏ tick cả bảy dòng ⇒ khối không in gì, **không phải lỗi** (`R-TLMI-080`).

> ⚠ Bản cũ dùng `KhoiDonViJson.Dong(k, nhan, hien, dam)` — một mảng 5 dòng có nhãn và in đậm riêng (`cell/mau_in/internal/model/json/KhoiDonViJson.java:33`). Đặc tả mới: **7 dòng cố định thứ tự, chỉ bật/tắt**, không nhãn, không in đậm ⇒ đổi sang **map 7 khoá `Boolean`**.

### 4.2 `TIEU_DE` — khối Tiêu đề

```json
{
  "id": "tieu_de", "loai": "TIEU_DE", "ten": "Tiêu đề", "hien": true,
  "noiDung": "HÓA ĐƠN BÁN HÀNG",
  "coChu": 18, "can": "GIUA", "inHoa": true, "inDam": true, "dongNgayThang": true
}
```

| Khoá | Kiểu | Bắt buộc | Miền / mặc định | Message | Luật |
|---|---|---|---|---|---|
| `noiDung` | `String` | ✔ | không trống, ≤ **255**; mặc định = **tên loại chứng từ** | `MSG_…_201` | `R-TLMI-085` |
| `coChu` | `Integer` | ✔ | `10…36`, mặc định `18`, **độc lập** `trang.coChu` | `MSG_…_202` | `R-TLMI-086` |
| `can` | `String` | ✔ | `TRAI` · `GIUA` · `PHAI`, mặc định `GIUA` — áp cho **cả** dòng tiêu đề **và** dòng ngày tháng | — | `R-TLMI-087` |
| `inHoa` | `boolean` | ✔ | mặc định `true` | — | `R-TLMI-088` |
| `inDam` | `boolean` | ✔ | mặc định `true` | — | `R-TLMI-089` |
| `dongNgayThang` | `boolean` | ✔ | mặc định `true`; in **nghiêng** `Ngày <dd> tháng <mm> năm <yyyy>`, lấy **ngày chứng từ** | — | `R-TLMI-090` |

- Khối đang **ẩn** (`hien = false`) ⇒ **bỏ qua kiểm `noiDung`** (quyết định C18). Bật lại ⇒ kiểm lại ngay.
- **Số chứng từ KHÔNG thuộc khối này** (`R-TLMI-091`) — muốn in phải đưa trường `soChungTu` vào một khối tự do.
- ⚠ Bản cũ giới hạn tiêu đề **80 ký tự** (`GioiHanMauIn.TIEU_DE_MAX_LEN = 80`, `cell/mau_in/internal/model/GioiHanMauIn.java:28`) — đặc tả mới là **255**, phải sửa.

### 4.3 `BANG` — khối Bảng (một khối cho mỗi lưới trên form)

```json
{
  "id": "bang_chiTiet", "loai": "BANG", "ten": "Bảng Hàng hóa, dịch vụ", "hien": true,
  "maLuoi": "chiTiet",
  "tenBang": "",
  "inStt": true, "dongCong": true, "lapTieuDeMoiTrang": true, "keO": "DAY_DU",
  "cot": [
    { "maCot": "tenHang",   "tenHienThi": "Tên hàng hóa, dịch vụ", "in": true,  "rong": 34, "can": "TRAI" },
    { "maCot": "donViTinh", "tenHienThi": "ĐVT",                   "in": true,  "rong": 8,  "can": "TRAI" },
    { "maCot": "soLuong",   "tenHienThi": "Số lượng",              "in": true,  "rong": 10, "can": "PHAI", "cong": false },
    { "maCot": "donGia",    "tenHienThi": "Đơn giá",               "in": true,  "rong": 20, "can": "PHAI", "cong": false },
    { "maCot": "thanhTien", "tenHienThi": "Thành tiền",            "in": true,  "rong": 28, "can": "PHAI", "cong": true },
    { "maCot": "ghiChu",    "tenHienThi": "Ghi chú",               "in": false, "rong": 12, "can": "TRAI" }
  ]
}
```

| Khoá | Kiểu | Bắt buộc | Miền / mặc định | Luật |
|---|---|---|---|---|
| `maLuoi` | `String` | ✔ | khoá lưới trong catalog; **duy nhất trong một mẫu** | `R-TLMI-092` · `INV-TLMI-008` |
| `ten` | `String` | ✔ | cố định = `"Bảng <tên lưới>"` | `R-TLMI-009` · `212` |
| `tenBang` | `String` | — | **trống ⇒ không in tên bảng**; có nội dung ⇒ in một dòng **đậm** trên bảng. Mặc định: **trống** cho lưới đầu tiên, **= tên lưới** cho lưới khác | `R-TLMI-094` · `095` |
| `inStt` | `boolean` | ✔ | mặc định `true` — thêm cột đầu tiên đánh số 1, 2, 3… | `R-TLMI-096` |
| `dongCong` | `boolean` | ✔ | mặc định `true` — dòng cuối in chữ **"Tổng:"** + tổng các cột tick `cong`. `false` ⇒ cột tick `cong` **không có tác dụng** | `R-TLMI-097` · `098` |
| `lapTieuDeMoiTrang` | `boolean` | ✔ | mặc định `true` | `R-TLMI-099` |
| `keO` | `String` | ✔ | `DAY_DU` (mặc định) · `KE_NGANG` | `R-TLMI-100` |
| `cot[]` | array | ✔ | thứ tự mảng = thứ tự in | `R-TLMI-115` |

#### `cot[]`

| Khoá | Kiểu | Bắt buộc | Miền / mặc định | Message | Luật |
|---|---|---|---|---|---|
| `maCot` | `String` | ✔ | khoá cột trong catalog của lưới; **không** lưu *Tên cột dữ liệu* (chỉ đọc, lấy theo catalog) | — | `R-TLMI-101` |
| `tenHienThi` | `String` | ✔ | không trống, ≤ **100**; mặc định = tên cột dữ liệu | `MSG_…_204` | `R-TLMI-102` |
| `in` | `boolean` | ✔ | mặc định `true` | `MSG_…_203` khi bỏ tick cột cuối cùng của bảng đang bật | `R-TLMI-103` · `104` |
| `rong` | `Integer` | ✔ **khi `in = true`** | `3…90`; **cột `in = false` giữ nguyên số đang có, được phép vắng** | `MSG_…_205` | `R-TLMI-108` · `112` · `113` |
| `can` | `String` | ✔ | `TRAI` · `GIUA` · `PHAI` — áp cho **cả** tiêu đề cột **và** dữ liệu. Mặc định: cột **số** ⇒ `PHAI`, còn lại ⇒ `TRAI` | — | `R-TLMI-105` |
| `cong` | `Boolean` | — | **chỉ cột số mới có**; mặc định `true` với cột **tiền**, `false` với cột số khác. Cột chữ ⇒ khoá **không xuất hiện** | — | `R-TLMI-106` · `107` |

- Tổng `rong` của các cột `in = true` **nên** bằng 100 nhưng **tổng ≠ 100 KHÔNG phải lỗi** — hệ thống **tự chia lại** khi Lưu (`R-TLMI-111`, `INV-TLMI-005`). Thuật toán: [07](07-chuan-hoa-kiem-tra-va-thuat-toan.md) §3.
- Cột thêm vào lưới ở phiên bản sau **tự xuất hiện cuối bảng**, mặc định `in = true` và được chia lại độ rộng (`R-TLMI-093`).
- Cột **bị xoá** khỏi form: bỏ qua im lặng khi in, hiện mờ + nhãn *"không còn trên form"* khi mở màn, **loại khỏi mẫu khi Lưu** (quyết định C10).
- ⚠ Bản cũ có `KhoiBangJson.TieuDe(noiDung, hien, dam, can)` — object 4 khoá (`cell/mau_in/internal/model/json/KhoiBangJson.java:34`). Đặc tả mới chỉ có **một chuỗi `tenBang`**; `dam` luôn `true`, `can` không cấu hình được ⇒ rút gọn.

### 4.4 `CHU_KY` — khối Chữ ký

```json
{
  "id": "chu_ky", "loai": "CHU_KY", "ten": "Chữ ký", "hien": true,
  "dongNgayThang": true, "choTrongKy": "VUA",
  "o": [
    { "vaiTro": "NGUOI_LAP",       "in": true,  "ghiChu": "(Ký, họ tên)" },
    { "vaiTro": "KE_TOAN_TRUONG",  "in": true,  "ghiChu": "(Ký, họ tên)" },
    { "vaiTro": "GIAM_DOC",        "in": true,  "ghiChu": "(Ký, họ tên, đóng dấu)" },
    { "vaiTro": "THU_KHO",         "in": false, "ghiChu": "(Ký, họ tên)" },
    { "vaiTro": "THU_QUY",         "in": false, "ghiChu": "(Ký, họ tên)" },
    { "id": "ky_tu_do_1", "in": true, "tieuDe": "Người nhận hàng",
      "tenNguoiKy": "", "ghiChu": "(Ký, họ tên)" }
  ]
}
```

| Khoá (khối) | Kiểu | Bắt buộc | Miền / mặc định | Luật |
|---|---|---|---|---|
| `dongNgayThang` | `boolean` | ✔ | mặc định `true` — dòng *"Ngày … tháng … năm …"* in **nghiêng, căn phải, phía trên các ô ký**, lấy **ngày chứng từ** | `R-TLMI-197` |
| `choTrongKy` | `String` | ✔ | `THAP` · `VUA` (mặc định) · `CAO` ≈ 1 / 2 / 3 cm | `R-TLMI-198` |
| `o[]` | array | ✔ | **5 chức danh luôn có mặt** + n ô ký tự do; thứ tự mảng = thứ tự in | `R-TLMI-182` · `183` · `192` |

#### `o[]`

| Khoá | Kiểu | Ô chức danh | Ô tự do | Luật |
|---|---|---|---|---|
| `vaiTro` | `String` | ✔ `GIAM_DOC` · `KE_TOAN_TRUONG` · `THU_KHO` · `THU_QUY` · `NGUOI_LAP` | **vắng mặt** | `R-TLMI-182` · `185` |
| `id` | `String` | vắng mặt | ✔ `ky_tu_do_<n>` (chuẩn hoá đánh lại) | §1.3 |
| `in` | `boolean` | ✔ mặc định: `NGUOI_LAP` `KE_TOAN_TRUONG` `GIAM_DOC` = `true`; `THU_KHO` `THU_QUY` = `false` | ✔ | `R-TLMI-184` · `191` |
| `tieuDe` | `String` | `⟨kế thừa⟩` — **vắng = theo Tiêu đề người ký của Thiết lập người ký** (quyết định **C04: mẫu sửa riêng được**) | ✔ **bắt buộc khi `in = true`**, không trống, ≤ **60** → `MSG_…_211` | `R-TLMI-188` · `189` |
| `tenNguoiKy` | `String` | **không lưu** — chỉ đọc từ Thiết lập người ký | ✔ gõ tay được, có thể rỗng | `R-TLMI-186` · `187` |
| `ghiChu` | `String` | ✔ mặc định `"(Ký, họ tên)"`, riêng `GIAM_DOC` = `"(Ký, họ tên, đóng dấu)"` | ✔ như trên | `R-TLMI-190` |

- **Không giới hạn số ô ký** (`R-TLMI-193`). ⚠ Bản cũ chặn **4 ô** (`GioiHanMauIn.O_KY_TOI_DA = 4`, `cell/mau_in/internal/model/GioiHanMauIn.java:55`) — **phải bỏ**.
- Ô chức danh **chỉ tắt được, không xoá được**; ô tự do xoá được (`R-TLMI-192`).
- Cờ *In tên người ký trên chứng từ, báo cáo* **luôn theo thiết lập chung**, chỉ đọc ở màn này ⇒ **không lưu trong mẫu** (`R-TLMI-196`). ⚠ Bản cũ có `KhoiChuKyJson.inTen` ở cấp khối — **bỏ**.
- Tên người ký / tiêu đề mặc định đọc qua `HoSoDonViPort.theoChiNhanh(chungTu.chiNhanhId)` (quyết định **C05**: chi nhánh **ghi trên chứng từ**, không phải chi nhánh đang làm việc — `R-TLMI-199`).

### 4.5 `TU_DO` — khối tự do (lưới ô kiểu Excel)

```json
{
  "id": "tu_do_1", "loai": "TU_DO", "ten": "Thông tin chung", "hien": true,
  "soDong": 3, "soCot": 2,
  "o": [
    { "dong": 0, "cot": 0, "gopCot": 2, "loai": "TRUONG", "maTruong": "soChungTu", "can": "TRAI" },
    { "dong": 1, "cot": 0, "loai": "TRUONG", "maTruong": "tenKhachHang", "can": "TRAI" },
    { "dong": 1, "cot": 1, "loai": "CHU",    "noiDung": "Kèm theo:", "can": "PHAI", "dam": true },
    { "dong": 2, "cot": 0, "gopDong": 1, "gopCot": 2, "loai": "CHU",
      "noiDung": "Số tiền viết bằng chữ:", "can": "TRAI", "nghieng": true }
  ]
}
```

| Khoá (khối) | Kiểu | Bắt buộc | Miền | Message | Luật |
|---|---|---|---|---|---|
| `ten` | `String` | ✔ | không trống, ≤ **60** — **KHÔNG in ra bản in** | `MSG_…_206` | `R-TLMI-121` · `126` · `127` |
| `soDong` | `Integer` | ✔ | `1…20` | `MSG_…_208` | `R-TLMI-129` · C20 |
| `soCot` | `Integer` | ✔ | `1…6` | `MSG_…_216` | `R-TLMI-130` · C20 |
| `o[]` | array | ✔ (có thể `[]`) | các ô **có nội dung hoặc có định dạng**; ô không xuất hiện = **ô trống** | — | `R-TLMI-143` · `176` |

- Khối tự do mới: lưới **1 dòng × 2 cột toàn ô trống**, đặt **ngay trước khối Chữ ký** (`R-TLMI-122` · `123`).
- Tối đa **10 khối tự do** mỗi mẫu → `MSG_…_207` (`R-TLMI-125`).
- Các cột **rộng bằng nhau**, không có độ rộng riêng (`R-TLMI-131`) ⇒ **không có khoá `rong`** trong khối tự do.
- Khối tự do đang bật mà **mọi ô đều trống** thì **vẫn lưu được**, không phải lỗi (`R-TLMI-176` · `236`).

#### `o[]` — một ô của lưới

| Khoá | Kiểu | Bắt buộc | Miền / mặc định | Luật |
|---|---|---|---|---|
| `dong` | `Integer` | ✔ | `0 … soDong-1` | — |
| `cot` | `Integer` | ✔ | `0 … soCot-1` | — |
| `gopDong` | `Integer` | — | ≥ 1, **vắng = 1**; `dong + gopDong ≤ soDong` | `R-TLMI-136` · `180` |
| `gopCot` | `Integer` | — | ≥ 1, **vắng = 1**; `cot + gopCot ≤ soCot` | `R-TLMI-136` · `180` |
| `loai` | `String` | ✔ | `TRONG` · `TRUONG` · `CHU` | `R-TLMI-143` · `144` · `146` |
| `maTruong` | `String` | ✔ **khi** `loai = TRUONG` | khoá trường trong kho trường; **duy nhất trong một khối** (`INV-TLMI-007`), nhưng **được** dùng lại ở khối khác (`R-TLMI-153`) | `R-TLMI-152` · `153` |
| `noiDung` | `String` | ✔ **khi** `loai = CHU` | không trống (rỗng ⇒ ô tự về `TRONG`, **không** báo lỗi), ≤ **255** → `MSG_…_212` | `R-TLMI-147` · `148` |
| `can` | `String` | — | `TRAI` · `GIUA` · `PHAI` — đặt **THEO Ô**, không theo trường; vắng = `TRAI` | `R-TLMI-161` |
| `nghieng` | `Boolean` | — | áp cho **cả ô** (nhãn lẫn giá trị); vắng = `false` | `R-TLMI-160` |
| `dam` | `Boolean` | — | **chỉ dùng cho `loai = CHU`** (đậm cả chữ). Với `loai = TRUONG` thì in đậm là **thuộc tính của trường** (§5) và khoá này **không được xuất hiện** | `R-TLMI-158` · `159` |

**Cách in một ô:**

| `loai` | In ra |
|---|---|
| `TRONG` | không in gì, **chiếm chỗ** để các ô khác thẳng hàng (`R-TLMI-143`) |
| `TRUONG` | `Tên hiển thị: Giá trị` — `tenHienThi` rỗng ⇒ **chỉ in giá trị**, không in nhãn và dấu `:` (`R-TLMI-144` · `145`) |
| `CHU` | đúng chữ người dùng gõ, không có giá trị kèm theo (`R-TLMI-146`) |

> ⚠ **Đây là chỗ khác bản cũ nhiều nhất.** Bản cũ mô hình khối tự do bằng `KhoiTuDoJson{ boCuc: {soCot, keO, rongNhan}, truong: List<TruongInJson{k, nhan, hien, span, spanDoc, dam, nghieng, tuDo}> }` — một **danh sách trường** tự rải vào lưới (`cell/mau_in/internal/model/json/KhoiTuDoJson.java:8-17`, `TruongInJson.java:13-22`). Đặc tả mới cần **ma trận ô có toạ độ tường minh**: gộp/tách ô theo vùng (`R-TLMI-136`…`142`), thêm/xoá dòng-cột tại chỗ (`R-TLMI-133`…`135`), kéo ô đổi chỗ (`R-TLMI-154`). Danh sách tuần tự **không biểu diễn được** ô gộp 2×3 ở giữa lưới. ⇒ **viết lại**, không sửa vá.

---

## §5. `truong` — thuộc tính CỦA TRƯỜNG, dùng chung cả mẫu

```json
"truong": {
  "soChungTu":    { "tenHienThi": "Số phiếu", "dam": true },
  "ngayChungTu":  { "dam": true },
  "dienGiai":     { "tenHienThi": "" }
}
```

| Khoá | Kiểu | Bắt buộc | Miền / mặc định | Message | Luật |
|---|---|---|---|---|---|
| `<maTruong>` | key | — | chỉ ghi trường **đã được đặt vào ít nhất một ô**; trường chưa đặt vào ô nào ⇒ **không lưu** | — | `R-TLMI-164` |
| `.tenHienThi` | `String` | — | ≤ **255**. **Vắng** = dùng tên trường của catalog; **`""`** = chỉ in giá trị | `MSG_…_212` | `R-TLMI-145` · `157` |
| `.dam` | `Boolean` | — | vắng = `false`. In đậm ⇒ **chỉ đậm Tên hiển thị**, giá trị luôn in thường | — | `R-TLMI-156` · `158` |

- **Một trường có đúng một cặp (`tenHienThi`, `dam`) trong phạm vi một mẫu** — `INV-TLMI-009`. Sửa ở khối nào cũng đổi mọi khối (`R-TLMI-156`).
- `ChuanHoaMau` **xoá** mọi khoá `<maTruong>` không còn ô nào trỏ tới, và mọi entry rỗng `{}`.
- Ô mới thêm vào form ở phiên bản sau **tự vào kho trường** nhưng **không tự chen vào khối tự do** (`R-TLMI-167`) ⇒ không sinh entry ở đây.

---

## §6. Bất biến cưỡng chế trong `KiemTraMau`

| Bất biến | Cưỡng chế ở đâu | Luật |
|---|---|---|
| `INV-TLMI-001` — một tenant + một nghiệp vụ ⇒ tối đa một mẫu | unique index DB (`V1158`) | `R-TLMI-004` |
| `INV-TLMI-002` — mẫu bằng mẫu chuẩn ⇒ **không tồn tại** bản ghi | `MauInService.luu` bước 6 (D5) | `R-TLMI-021` |
| `INV-TLMI-003` — ô theo chung ⇒ **khoá vắng mặt** | `ChuanHoaMau` (xoá `null`) + cấm gọi `HopNhatThietLapChung` trước khi ghi | `R-TLMI-037` |
| `INV-TLMI-004` — khối `BANG` đang bật luôn ≥ 1 cột `in = true` | `KiemTraMau` V03 | `R-TLMI-104` |
| `INV-TLMI-005` — độ rộng cột đã lưu luôn hợp lệ và **tổng = 100** | `ChuanHoaMau` → `ChiaDeuDoRong` | `R-TLMI-108` · `111` · `114` |
| `INV-TLMI-006` — trần & sàn khối tự do: `1…20` dòng, `1…6` cột, ≤ 10 khối | `KiemTraMau` V06…V09 | `R-TLMI-125` · `129` · `130` |
| `INV-TLMI-007` — một trường ở tối đa một ô **trong một khối** | `KiemTraMau` | `R-TLMI-152` |
| `INV-TLMI-008` — bốn loại khối chuẩn luôn tồn tại | `KiemTraMau` (đếm theo `loai`) | `R-TLMI-008` · `009` |
| `INV-TLMI-009` — `tenHienThi` + `dam` của một trường là duy nhất trong mẫu | cấu trúc `truong` là **map** ⇒ đúng theo kiểu dữ liệu | `R-TLMI-156` |
| `INV-TLMI-010` — ô ký tự do đang bật luôn có tiêu đề hợp lệ | `KiemTraMau` V12 | `R-TLMI-189` |
| `INV-TLMI-011` — mẫu **không** mang phạm vi chi nhánh | không có khoá `chiNhanhId` ở bất kỳ đâu trong schema; repository không lọc chi nhánh | `R-TLMI-005` · `035` |
| `INV-TLMI-012` — Lưu là all-or-nothing | `@Transactional` trên `MauInService.luu` | `R-TLMI-247` |

---

## §7. Ví dụ đầy đủ — mẫu chuẩn hệ thống của một loại chứng từ đơn giản

Mẫu chuẩn **không có bản ghi trong DB** (`R-TLMI-006` · `007`); đây là cái `MauChuanBuilder` sinh ra từ catalog.

```json
{
  "schemaVersion": 2,
  "maLoaiChungTu": "PT",
  "maNghiepVu": "MAC_DINH",
  "trang": { "mauChu": "#000000", "nen": { "kieu": "KHONG" } },
  "truong": {},
  "khoi": [
    { "id": "dau_trang", "loai": "DAU_TRANG", "ten": "Thông tin đầu trang", "hien": true, "dong": {} },
    { "id": "tieu_de", "loai": "TIEU_DE", "ten": "Tiêu đề", "hien": true,
      "noiDung": "PHIẾU THU", "coChu": 18, "can": "GIUA",
      "inHoa": true, "inDam": true, "dongNgayThang": true },
    { "id": "bang_dinhKhoan", "loai": "BANG", "ten": "Bảng Hạch toán", "hien": true,
      "maLuoi": "dinhKhoan", "inStt": true, "dongCong": true,
      "lapTieuDeMoiTrang": true, "keO": "DAY_DU",
      "cot": [
        { "maCot": "dienGiai", "tenHienThi": "Diễn giải", "in": true, "rong": 40, "can": "TRAI" },
        { "maCot": "tkNo",     "tenHienThi": "TK Nợ",     "in": true, "rong": 15, "can": "TRAI" },
        { "maCot": "tkCo",     "tenHienThi": "TK Có",     "in": true, "rong": 15, "can": "TRAI" },
        { "maCot": "soTien",   "tenHienThi": "Số tiền",   "in": true, "rong": 30, "can": "PHAI", "cong": true }
      ] },
    { "id": "chu_ky", "loai": "CHU_KY", "ten": "Chữ ký", "hien": true,
      "dongNgayThang": true, "choTrongKy": "VUA",
      "o": [
        { "vaiTro": "NGUOI_LAP",      "in": true,  "ghiChu": "(Ký, họ tên)" },
        { "vaiTro": "KE_TOAN_TRUONG", "in": true,  "ghiChu": "(Ký, họ tên)" },
        { "vaiTro": "GIAM_DOC",       "in": true,  "ghiChu": "(Ký, họ tên, đóng dấu)" },
        { "vaiTro": "THU_KHO",        "in": false, "ghiChu": "(Ký, họ tên)" },
        { "vaiTro": "THU_QUY",        "in": false, "ghiChu": "(Ký, họ tên)" }
      ] }
  ]
}
```

Đọc bản này: **toàn bộ nhóm Giấy và chữ đều theo thiết lập chung** (`trang` chỉ còn 2 khoá riêng của mẫu), **cả 7 dòng đầu trang đều theo thiết lập chung** (`dong: {}`), **không có khối tự do**. Đúng `R-TLMI-008` (đúng bốn loại khối, thứ tự cố định) và `R-TLMI-010` (muốn in thông tin chung / tổng tiền thì tự thêm khối tự do).

---

## §8. Ánh xạ JSON ↔ record Java ↔ Zod

| Nhánh JSON | Record Java (`cell/mau_in/internal/model/json/`) | Zod (`client/src/base/domainKit/mauIn/api/schemas.ts`) |
|---|---|---|
| gốc | `MauInJson` | `mauInSchema` |
| `trang` | `TrangJson` | `trangSchema` |
| `truong` | `Map<String, ThuocTinhTruongJson>` | `z.record(thuocTinhTruongSchema)` |
| `khoi[]` | `KhoiJson` (sealed, `@JsonTypeInfo(EXISTING_PROPERTY, property="loai", visible=true)`) | `z.discriminatedUnion('loai', …)` |
| `khoi[DAU_TRANG]` | `KhoiDauTrangJson` | `khoiDauTrangSchema` |
| `khoi[TIEU_DE]` | `KhoiTieuDeJson` | `khoiTieuDeSchema` |
| `khoi[BANG]` | `KhoiBangJson` + `KhoiBangJson.Cot` | `khoiBangSchema` |
| `khoi[CHU_KY]` | `KhoiChuKyJson` + `KhoiChuKyJson.O` | `khoiChuKySchema` |
| `khoi[TU_DO]` | `KhoiTuDoJson` + `OLuoiJson` | `khoiTuDoSchema` |

**Ba luật bắt buộc cho mọi record:**

1. `@JsonInclude(JsonInclude.Include.NON_NULL)` — nếu không thì mọi khoá kế thừa bị ghi `null` xuống DB và `INV-TLMI-003` vỡ.
2. Kiểu **boxed** cho mọi khoá `⟨kế thừa⟩` (`Integer` · `Double` · `Boolean` · `String`), **không** `int`/`double`/`boolean`.
3. `MauInJsonCodec` cấu hình `FAIL_ON_UNKNOWN_PROPERTIES = true` — thuộc tính lạ ⇒ lỗi, không im lặng nuốt. Đây là cách bắt sớm lệch schema giữa FE và BE.

> ⚠ **Bẫy đã xảy ra thật ở bản cũ** (ghi trong `schemas.ts:117-120`): đặt `.default(1)` cho một khoá optional ở Zod thì FE gửi lên khoá đó, BE cũ chưa biết ⇒ từ chối **cả mẫu** với `Unrecognized field`. Với schema v2, nhóm `⟨kế thừa⟩` **cấm** `.default()` ở cả hai bên — đây vừa là lý do kỹ thuật vừa là yêu cầu nghiệp vụ `R-TLMI-037`.
