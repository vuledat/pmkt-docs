# 03 · `F01` — API Thiết lập mẫu in (UC01)

| | |
|---|---|
| Mã chức năng | `F01` + `F06` (phần đọc/ghi thiết lập chung) |
| UC nguồn | `PMKT-U-14549_21-01` Thiết lập mẫu in |
| Màn nguồn | `SCR_ThietLapMauIn.md` (qua `02-rules.md`) · Figma `ymMyg329ejsgCWg28CNmGl` node `71956:288871` |
| Endpoint phụ trách | `A1` `A2` `A3` `A4` `A10` `A11` |
| Quyết định liên quan | `D4` `D5` `D6` `D10` `D12` |

---

## §1. `A1` — Mở màn Thiết lập mẫu in

```
GET /api/mau-in/{maLoai}/{maNghiepVu}
```

**Quyền:** `HTMauIn.View` **+** `<MaChucNang của nghiệp vụ>.View.Detail` (quyết định C13 — tầng (b) để không lộ dữ liệu chứng từ qua màn xem trước).

### Response — `ApiResponse<MauInManHinhResponse>`

```json
{
  "success": true,
  "data": {
    "maLoaiChungTu": "PT",
    "maNghiepVu": "MAC_DINH",
    "tenLoaiChungTu": "Phiếu thu",
    "nguon": "TUY_CHINH",
    "phienBan": 3,
    "mau":       { "schemaVersion": 2, "...": "JSON mẫu ĐÃ LƯU — khoá kế thừa VẪN VẮNG" },
    "mauChuan":  { "schemaVersion": 2, "...": "mẫu chuẩn hệ thống sinh từ catalog" },
    "thietLapChung": { "giayVaChu": { }, "dauTrang": { }, "quyTacIn": { } },
    "catalog":   { "...": "MoTaMauIn — kho trường, các lưới, các cột" },
    "coAnhNen": true,
    "canhBao": [
      { "loai": "PHAN_TU_KHONG_CON_TREN_FORM", "duongDan": "khoi[2].cot[5]", "nhan": "Ghi chú" }
    ]
  }
}
```

| Trường | Kiểu | Ý nghĩa | Luật |
|---|---|---|---|
| `nguon` | `MAU_CHUAN` · `TUY_CHINH` | **Không có bản ghi = đang dùng mẫu chuẩn**, không có cờ riêng | `R-TLMI-007` · `INV-TLMI-002` |
| `phienBan` | `Integer` | `null` khi `nguon = MAU_CHUAN`; client gửi lại nguyên si ở `A2` (D6) | `R-TLMI-258` |
| `mau` | `JsonNode` | JSON **đã lưu**, **khoá kế thừa vẫn vắng**. ⚠ **TUYỆT ĐỐI KHÔNG hợp nhất ở đây** — nếu hợp nhất, FE lưu lại sẽ ghi giá trị đang hiển thị và `R-TLMI-037` vỡ | `R-TLMI-036` · `037` |
| `mauChuan` | `JsonNode` | Để nút *Đặt lại mẫu chuẩn* hoạt động **hoàn toàn trên màn**, không gọi lại server | `R-TLMI-016` · `018` |
| `thietLapChung` | object | Gửi kèm để FE hiển thị "giá trị đang dùng" của các ô kế thừa (`R-TLMI-053`) mà không phải gọi `A10` | `R-TLMI-036` · `053` |
| `catalog` | `MoTaMauIn` | Kho trường + các lưới + cột gốc; xem [06](06-provider-nghiep-vu-va-kho-truong.md) | `R-TLMI-009` · `165` |
| `coAnhNen` | `boolean` | Có ảnh nền trong cột `bytea` không (tải bằng `A6`) | `R-TLMI-069` |
| `canhBao[]` | array | Phần tử còn trong mẫu nhưng **không còn trên form** ⇒ FE hiện **mờ + nhãn "không còn trên form"**, loại khỏi mẫu khi Lưu | quyết định **C10** |

### Luồng

1. `quyen.require(HT_MAU_IN, VIEW)` → thiếu ⇒ `403` `MSG_PMKT-E-14549_21_002` (`R-TLMI-034`).
2. `provider = DangKyProvider.can(maLoai, maNghiepVu)` → không có ⇒ `404` `MAU_IN_NGHIEP_VU_CHUA_HO_TRO`.
3. `quyen.require(provider.moTa().maChucNang(), VIEW_DETAIL)`.
4. Đọc bản ghi theo `(tenant, maLoai, maNghiepVu)` — **không lọc chi nhánh** (`R-TLMI-005` · `035` · `INV-TLMI-011`).
5. Có bản ghi ⇒ `HopNhatCatalog.hopNhat(mauDaLuu, catalog)`: bỏ cột/trường không còn trên form (đưa vào `canhBao`), thêm cột mới vào **cuối bảng** với `in = true` (`R-TLMI-093`), thêm trường mới vào **kho trường** nhưng **không** chen vào khối tự do (`R-TLMI-167`).
6. Không có bản ghi ⇒ `mau = mauChuan`, `nguon = MAU_CHUAN`.

> **Lối vào:** cả hai lối (menu In › *Thiết lập mẫu in…* và nút *Sửa mẫu* trên màn xem trước) gọi **cùng endpoint này với cùng cặp khoá** ⇒ cùng một mẫu (`R-TLMI-028`). Đổi *Loại nghiệp vụ* trên form rồi mở lại ⇒ `maNghiepVu` khác ⇒ **mẫu khác** (`R-TLMI-012`).

---

## §2. `A2` — Lưu mẫu

```
PUT /api/mau-in/{maLoai}/{maNghiepVu}
Content-Type: application/json
```

**Quyền:** `HTMauIn.Edit` **+** `<MaChucNang>.View.Detail`.

### Request — `LuuMauInRequest`

```json
{
  "mau": { "schemaVersion": 2, "maLoaiChungTu": "PT", "maNghiepVu": "MAC_DINH", "...": "..." },
  "phienBan": 3
}
```

| Trường | Kiểu | Bắt buộc | Ràng buộc |
|---|---|---|---|
| `mau` | `JsonNode` | ✔ `@NotNull` | Theo [01-hop-dong-json-mau-in.md](01-hop-dong-json-mau-in.md); `maLoaiChungTu`/`maNghiepVu` bên trong **phải khớp** path, lệch ⇒ `400` |
| `phienBan` | `Integer` | — | `null` = "tôi tin là chưa có bản ghi". Lệch bản đang có ⇒ `409` (D6) |

### Response — `ApiResponse<KetQuaLuuDto>`

```json
{
  "success": true,
  "message": "Lưu mẫu in thành công!",
  "messageCode": "MSG_PMKT-E-14549_21_101",
  "data": { "nguon": "TUY_CHINH", "phienBan": 4, "mauDaChuanHoa": { "...": "..." } }
}
```

`mauDaChuanHoa` trả về để FE **thay thẳng** state của mình — vì server có thể đã **chia lại độ rộng cột về 100** (`R-TLMI-111`) và bỏ các khoá thừa. Không trả thì màn và DB lệch nhau ngay sau khi Lưu.

Khi mẫu **bằng mẫu chuẩn** ⇒ `nguon = "MAU_CHUAN"`, `phienBan = null`, `mauDaChuanHoa` = mẫu chuẩn.

### Luồng — xem [00 §6.1](00-ke-hoach-tong.md); chi tiết thuật toán ở [07](07-chuan-hoa-kiem-tra-va-thuat-toan.md)

### Tương tranh & transaction

| Hạng mục | Quyết định |
|---|---|
| Ranh giới `@Transactional` | Bao trọn bước 6 + ghi lịch sử. `R-TLMI-247` · `INV-TLMI-012` — all-or-nothing |
| Khoá | **Lạc quan** bằng `phien_ban` (D6). `@Version` của JPA trên `MauInTuyChinh.phienBan` ⇒ `OptimisticLockingFailureException` đã được `GlobalExceptionHandler` map sang `409 STALE_DATA` (mẫu ở `platform_iam/tenant/internal/entity/Tenant.java:20-24`) |
| Idempotency | Không cần token riêng: `phienBan` **chính là** khoá idempotency — gửi lại cùng `phienBan` lần hai ⇒ `409`, không ghi đè |
| Lỗi hệ thống | Rollback, giữ nguyên màn, `500` + `MSG_PMKT-E-14549_21_003` (`R-TLMI-249`) |

### Ma trận validation (server)

Đầy đủ 17 dòng ở [07 §2](07-chuan-hoa-kiem-tra-va-thuat-toan.md). Ba điều **KHÔNG phải lỗi** và **không chặn Lưu**:

| Không phải lỗi | Xử lý | Luật |
|---|---|---|
| Tổng độ rộng cột ≠ 100 | **tự chia lại về 100** khi Lưu | `R-TLMI-111` |
| Ô trống trong khối tự do | bỏ qua | `R-TLMI-236` · `237` |
| Khối tự do đang bật mà mọi ô đều trống | vẫn lưu được | `R-TLMI-176` |
| Khối Tiêu đề đang **ẩn** mà `noiDung` trống | bỏ qua kiểm của khối đó | quyết định **C18** |

### Bảng mã lỗi

| Tình huống | HTTP | Mã lỗi nội bộ | Mã message |
|---|---|---|---|
| Thiếu quyền | `403` | `ACCESS_DENIED` | `MSG_PMKT-E-14549_21_002` |
| Nghiệp vụ chưa có provider | `404` | `MAU_IN_NGHIEP_VU_CHUA_HO_TRO` | — |
| JSON sai cấu trúc / thuộc tính lạ / `schemaVersion ≠ 2` | `400` | `MAU_IN_KHONG_HOP_LE` | — |
| Vi phạm một trong 17 dòng kiểm tra | `422` | `MAU_IN_KHONG_HOP_LE` | `MSG_…_201`…`216` — **chỉ lỗi ĐẦU TIÊN** (`R-TLMI-243`) |
| Lệch phiên bản | `409` | `MAU_IN_PHIEN_BAN_CU` | `MSG_COMMON_001` (tạm — §12 `Q7`) |
| Lỗi hệ thống | `500` | — | `MSG_PMKT-E-14549_21_003` |

**Thứ tự "lỗi đầu tiên"** (`R-TLMI-243` + quyết định C21) — server phải trả đúng thứ tự này để FE mở đúng khối và đặt con trỏ vào đúng ô (`R-TLMI-244`):

1. Theo **thứ tự khối trong `khoi[]`** (= thứ tự Bố cục mẫu).
2. Trong một khối: **ô ở bảng chỉnh trước** (theo thứ tự từ trên xuống), **rồi** ô lưới khối tự do (trái→phải, trên→dưới).
3. Lỗi ở mục *Thiết lập mẫu* (nhóm Giấy và chữ, màu chữ, hình nền) xếp **trước mọi khối** — vì mục này đứng đầu danh sách Bố cục mẫu (`R-TLMI-202`).

Response lỗi mang thêm `duongDan` (JSON pointer, ví dụ `khoi[2].cot[4].rong`) để FE nhảy tới đúng ô.

---

## §3. `A3` — Xem trước bằng dữ liệu chứng từ thật

```
GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu/{chungTuId}/xem-truoc
```

**Quyền:** `HTMauIn.View` **+** `<MaChucNang>.View.Detail`.

### Response — `ApiResponse<XemTruocResponse>`

```json
{
  "data": {
    "mauHieuLuc": { "...": "mẫu ĐÃ HỢP NHẤT thiết lập chung, hướng giấy đã giải" },
    "duLieu":     { "donVi": { }, "truong": { }, "bang": { }, "nguoiKy": { } },
    "huongGiayThucTe": "NGANG"
  }
}
```

| Trường | Ý nghĩa | Luật |
|---|---|---|
| `mauHieuLuc` | JSON mẫu **đã hợp nhất** — mọi khoá vắng đã điền từ thiết lập chung **tại thời điểm gọi** | `R-TLMI-038` · `220` |
| `duLieu` | Dữ liệu **thật** của chứng từ đang mở — **không có chế độ dữ liệu mẫu** | `R-TLMI-217` · `219` |
| `huongGiayThucTe` | `DOC` · `NGANG` — kết quả của `GiaiHuongGiay` khi `huong = TU_DONG` | `R-TLMI-058` · `059` · `060` |

- **Không** cộng gộp dòng ở đây: cộng gộp là quy tắc của **bản in** (`R-TLMI-119` · `266`), trang xem trước của màn thiết lập vẽ **mẫu**, không phải bản in cuối. ⚠ Tài liệu không nói rõ; ghi nhận là **suy luận có chủ ý**, cần BA soát — nếu BA muốn xem trước giống hệt bản in thì gọi `A9` thay vì `A3`.
- FE gọi lại `A3` khi đổi chứng từ nguồn; **mọi thay đổi trên màn thì FE tự vẽ lại bằng state của mình**, không gọi server mỗi lần gõ (`R-TLMI-218`).
- Nhập/xuất ảnh: `mauHieuLuc.trang.nen.kieu = "ANH"` ⇒ FE tải ảnh bằng `A6`.

---

## §4. `A4` — Chứng từ gần đây (chọn nguồn xem thử)

```
GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu-gan-day?q=&gioiHan=
```

**Quyền:** `HTMauIn.View` **+** `<MaChucNang>.View` (chỉ cần quyền danh sách, không cần chi tiết).

| Query | Kiểu | Mặc định | Ghi chú |
|---|---|---|---|
| `q` | `String` | — | Lọc theo số chứng từ / đối tượng, **không phân biệt dấu** |
| `gioiHan` | `Integer` | `20` | Trần `50` |

Response: `ApiResponse<List<ChungTuTomTat>>` — `{ id, soChungTu, ngayChungTu, doiTuong, soTien }`.

Ủy quyền hoàn toàn cho `provider.chungTuGanDay(q, gioiHan)` — `mau_in` **không biết** bảng chứng từ nào.

---

## §5. `A10` · `A11` — Thiết lập chung tối thiểu

```
GET /api/mau-in/thiet-lap-chung           quyền HTThongTinCongTy.View.Detail
PUT /api/mau-in/thiet-lap-chung           quyền HTThongTinCongTy.Edit
```

Schema: [02-hop-dong-json-thiet-lap-chung.md §2](02-hop-dong-json-thiet-lap-chung.md).

### `A10` Response

```json
{ "data": {
    "thietLap": { "giayVaChu": { }, "dauTrang": { }, "quyTacIn": { } },
    "coLogo": true,
    "phienBan": 2
} }
```

`thietLap` trả về **đã điền đủ mặc định hệ thống** cho mọi khoá vắng — client không phải mang bảng mặc định.

### `A11` Request

```json
{ "thietLap": { "giayVaChu": { }, "dauTrang": { }, "quyTacIn": { } }, "phienBan": 2 }
```

| Kiểm | Message |
|---|---|
| `kho ∈ {A3,A4,A5}` · `huong ∈ {DOC,NGANG,TU_DONG}` · `font ∈ {Times New Roman, Arial}` | `400` |
| `soCotTuDongNgang ∈ 1…50` | `MSG_PMKT-E-14549_21_214` |
| `le* ∈ 0…5`, ≤ 1 chữ số lẻ | `MSG_PMKT-E-14549_21_213` |
| `coChu ∈ 8…20` | `MSG_PMKT-E-14549_21_215` |
| `phienBan` lệch | `409` + `MSG_COMMON_001` |

Ghi vào `cfg_cau_hinh_he_thong` dòng `IN_CHUNG_CHUNG_TU`; **chưa có dòng ⇒ tạo mới** với `nhom='IN'`, `kieu_du_lieu='JSON'`, `ten_cau_hinh='Cấu hình in chứng từ'`, `la_he_thong=false`.

> **Ảnh hưởng dây chuyền:** đổi thiết lập chung ⇒ **mọi mẫu có ô kế thừa đổi theo ngay**, không cần đụng tới `prn_mau_in_tuy_chinh` (`R-TLMI-038`). Đây chính là lý do D4 chọn "khoá vắng mặt".

---

## §6. Ánh xạ cột BA ↔ DB ↔ DTO

> Tài liệu BA mô tả 5 bảng `cfg_mau_in_*`. Theo `D1` chúng là **nhánh JSON**, không phải cột DB. Bảng dưới ánh xạ **tên trường của BA** sang chỗ thật.

| Trường BA (`3.crud-matrix.md` / `SCR`) | Chỗ thật | Kiểu | Ghi chú |
|---|---|---|---|
| `cfg_mau_in_chung_tu.TenantId` | `prn_mau_in_tuy_chinh.tenant_id` | `uuid` | RLS `tenant_isolation` |
| `cfg_mau_in_chung_tu.MaChucNang` | `prn_mau_in_tuy_chinh.ma_loai_chung_tu` | `varchar(20)` | = `mst_loai_chung_tu.code` |
| `cfg_mau_in_chung_tu.MaNghiepVu` | `prn_mau_in_tuy_chinh.ma_nghiep_vu` | `varchar(50)` | **cột MỚI** — `V1158` |
| `cfg_mau_in_chung_tu.KhoGiay` / `HuongGiay` / `Le*` / `Font` / `CoChu` | `cau_hinh -> trang -> *` | jsonb | `⟨kế thừa⟩` — vắng = theo chung |
| `cfg_mau_in_chung_tu.MauChu` | `cau_hinh -> trang -> mauChu` | jsonb | riêng của mẫu |
| `cfg_mau_in_chung_tu.KieuNen` / `DoDam` / `CanAnh` | `cau_hinh -> trang -> nen -> *` | jsonb | |
| *(ảnh nền)* | `prn_mau_in_tuy_chinh.anh_nen` | `bytea` | **cột MỚI** — `V1159`, quyết định C08 |
| `cfg_mau_in_khoi.*` | `cau_hinh -> khoi[]` | jsonb | thứ tự mảng = `ThuTu` |
| `cfg_mau_in_khoi.Hien` (con mắt) | `cau_hinh -> khoi[i] -> hien` | jsonb | `R-TLMI-207` |
| `cfg_mau_in_khoi_cot.*` | `cau_hinh -> khoi[i] -> cot[]` | jsonb | thứ tự mảng = `ThuTu` |
| `cfg_mau_in_khoi_o.*` | `cau_hinh -> khoi[i] -> o[]` | jsonb | **có `dong`/`cot`/`gopDong`/`gopCot`** — chỗ tài liệu không có nơi lưu (C09) |
| `cfg_mau_in_khoi_chu_ky.*` | `cau_hinh -> khoi[CHU_KY] -> o[]` | jsonb | |
| `cfg_tenant.*` (thiết lập chung) | `cfg_cau_hinh_he_thong` dòng `IN_CHUNG_CHUNG_TU` | `text` (JSON) | D8 |
| `cfg_tenant.Logo` | `iam_tenant.logo` | `bytea` | **cột MỚI** — `V1160` |
| `cfg_chi_nhanh.*` | **chưa có** → `HoSoDonViPort.theoChiNhanh()` trả hồ sơ tenant | — | L-7 · Q-14 |

---

## §7. Kiểm thử

Mọi test `@Tag("unit")`, tên mang **chính mã luật** (`docs/rules/truy-vet-luat.md §3`).

| Test | Input → kỳ vọng | Luật |
|---|---|---|
| `R_TLMI_007_chuaCoBanGhiThiNguonLaMauChuan` | Không có bản ghi → `A1` trả `nguon=MAU_CHUAN`, `mau == mauChuan`, `phienBan=null` | `R-TLMI-007` |
| `R_TLMI_004_khoaDuyNhatTheoCapLoaiVaNghiepVu` | Hai bản ghi cùng `maLoai` khác `maNghiepVu` → cùng tồn tại; trùng cả cặp → vi phạm unique | `R-TLMI-004` · `INV-TLMI-001` |
| `R_TLMI_012_doiNghiepVuThiMoMauKhac` | `A1` với `maNghiepVu` khác → trả mẫu khác | `R-TLMI-012` |
| `R_TLMI_037_luuOTheoChungThiKhoaVangMat` | Lưu mẫu có `trang.kho` vắng → chuỗi `cau_hinh` **không chứa** khoá `kho` | `R-TLMI-037` · `INV-TLMI-003` |
| `R_TLMI_021_mauBangMauChuanThiXoaBanGhi` | Có bản ghi; Lưu mẫu đúng bằng mẫu chuẩn → bản ghi bị xoá, `nguon=MAU_CHUAN` | `R-TLMI-021` · `INV-TLMI-002` |
| `R_TLMI_021_luuLanDauKhongSuaGiThiKhongTaoBanGhi` | Chưa có bản ghi; Lưu nguyên mẫu chuẩn → **không** tạo bản ghi | `R-TLMI-021` |
| `R_TLMI_022_luuXongThiInDungMauMoiNgay` | Lưu → `A9` ngay sau đó dùng mẫu mới | `R-TLMI-022` |
| `R_TLMI_246_serverKiemLaiToanBo` | Payload hợp lệ với FE nhưng `coChu = 30` → `422` `MSG_…_215` | `R-TLMI-246` · `063` |
| `R_TLMI_243_chiBaoLoiDauTien` | Payload có 3 lỗi ở 3 khối → response chỉ mang **một** lỗi, đúng khối đầu theo thứ tự | `R-TLMI-243` |
| `R_TLMI_247_luuLaAllOrNothing` | Lỗi khi ghi lịch sử → bản ghi mẫu **không** đổi | `R-TLMI-247` · `INV-TLMI-012` |
| `R_TLMI_258_lechPhienBanThiKhongGhi` | `phienBan=2` trong khi DB là `3` → `409`, `cau_hinh` không đổi | `R-TLMI-258` |
| `R_TLMI_034_goiThangApiKhongQuyenThiChan` | Không có `HTMauIn.Edit` → `A2` trả `403` `MSG_…_002` | `R-TLMI-034` |
| `R_TLMI_035_suaMauOMotChiNhanhApChoMoiChiNhanh` | Repository không sinh điều kiện `chi_nhanh_id` | `R-TLMI-035` · `INV-TLMI-011` |
| `R_TLMI_093_cotMoiTuXuatHienCuoiBang` | Catalog thêm cột → `A1` trả cột mới ở cuối, `in=true` | `R-TLMI-093` |
| `R_TLMI_167_truongMoiVaoKhoNhungKhongChenVaoKhoiTuDo` | Catalog thêm trường → có trong `catalog`, **không** có ô mới trong `khoi[TU_DO]` | `R-TLMI-167` |
| `R_TLMI_111_tongRongKhac100ThiTuChiaLaiKhiLuu` | Lưu với `40/40/40` → `mauDaChuanHoa` có `33/33/34`, **không** báo lỗi | `R-TLMI-111` |
| `R_TLMI_218_xemTruocTraMauDaHopNhat` | `A3` với mẫu có khoá kế thừa vắng → `mauHieuLuc` đã điền | `R-TLMI-038` · `218` |
| `R_TLMI_219_khongCoCheDoDuLieuMau` | `A3` không có tham số nào bật dữ liệu mẫu | `R-TLMI-219` |

## §8. BR đã áp dụng

| BR | Bước |
|---|---|
| BR25 (quyền) | Gate hai tầng ở mọi endpoint (§1, §2) |
| BR26 (thông báo) | `MSG_…_101` toast thành công; `MSG_…_201`…`216` lỗi tại chỗ |
| BR28 (multi-tenant) | RLS + khoá `(tenant_id, …)`; repository không nhận `tenantId` từ client |
| BR29 (xoá) | ⚠ **lệch có chủ ý** — hard delete, xem [08 §6](08-thiet-ke-db.md) |
| BR50.6 · BR50.7 (Phase 2) | Không lọc chi nhánh khi đọc mẫu; đọc hồ sơ theo chi nhánh trên chứng từ |
