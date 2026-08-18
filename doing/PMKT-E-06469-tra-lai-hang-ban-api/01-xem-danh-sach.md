# F1 — Xem danh sách chứng từ trả lại hàng bán

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F1** |
| UC nguồn | `PMKT-U-06470` — `4.usecases/PMKT-U-06470_XemDanhSach/UC_XemDanhSachTraLaiHangBan.md` + `AD_XemDanhSach.puml` |
| Màn hình | `5.screens/SCR_DanhSachTraLaiHangBan.md` (137 dòng) |
| Endpoint phụ trách | **A1** `POST /search` · **A2** `GET /cot` · **A3** `POST /export` |
| Quyền | `TraLaiHangBan.View` (A1, A2) · `TraLaiHangBan.Export` (A3) |

## 1. Quyết định riêng

| # | Quyết định | Trỏ về |
|---|---|---|
| 1.1 | Toàn bộ 3 endpoint **kế thừa nguyên** `BaseCrudController` — chỉ override `cotMacDinh(EXPORT)` và `defaultSortAlias()` | §0-D2 |
| 1.2 | Hai cột nhãn `traLaiHang` và `hinhThucThanhToan` là **trường dẫn xuất trong DTO**, không phải cột DB | xem §4 |
| 1.3 | Cột trạng thái trả **TÊN HẰNG** (`DA_GHI_SO`) chứ không phải chuỗi tiếng Việt | §0-D3, §0-D7 |

---

## 2. Hợp đồng API

### A1 — `POST /api/ban-hang/tra-lai-hang-ban/search`

Quyền: `TraLaiHangBan.View` (`BaseCrudController.java:121-125`).

```jsonc
// Request — core/request/SearchRequest.java:32-38
{
  "page": 1,
  "pageSize": 20,
  "sort": "ngayHachToan:desc,ngayChungTu:desc,soChungTu:asc",
  "keyword": "TLHB",
  "logic": "AND",
  "filters": [
    { "field": "ngayHachToan",        "op": "between", "value": ["2026-08-01", "2026-08-31"] },
    { "field": "soChungTu",           "op": "like",    "value": "CTTL-000" },
    { "field": "tenKhachHang",        "op": "like",    "value": "Công ty A" },
    { "field": "trangThaiChungTu",    "op": "eq",      "value": "DA_GHI_SO" },
    { "field": "phuongThucLapHoaDon", "op": "eq",      "value": "Người bán xuất hóa đơn điều chỉnh" }
  ]
}
```

| Field request | Kiểu | Bắt buộc | Ràng buộc | Nguồn BA |
|---|---|---|---|---|
| `page` | int, 1-based | N | `null`/`<1` → 1 | BR1 |
| `pageSize` | int | N | whitelist `10/20/50/100/200`, khác → 20 | BR1 · `SCR:BR10` (20/trang) |
| `sort` | string `alias:asc\|desc[,…]` | N | alias phải `@Searchable(sortable=true)`; alias lạ bị **bỏ qua + log warn** (`Searchable.java:11-13`) | `SCR:BR17`, `UC:16` |
| `keyword` | string ≤ 100 | N | quét các field `keyword = true` — xem §3 | `SCR` §Thanh công cụ (`keyword`, max 100) |
| `filters[].field` | string | N | 4 alias ở §3; **alias lạ bị bỏ qua, không 400** | `api/traLaiHangBanApi.ts:68-73` |
| `logic` | `AND`\|`OR` | N | mặc định `AND`; `keyword` **luôn** AND với cả nhóm | `SearchRequest.java:29-30` |

```jsonc
// Response 200 — core/response/PageResponse.java:20-23
{
  "data": [
    {
      "id": "0f5c…",
      "soChungTu": "CTTL-000012",
      "ngayChungTu": "2026-08-10",
      "ngayHachToan": "2026-08-10",
      "khachHangId": "a1b2…",
      "tenKhachHang": "Công ty TNHH A",
      "maSoThue": "0101234567",
      "tongTienHangQuyDoi": 10000000.00,
      "tongChietKhauQuyDoi": 500000.00,
      "tongTienThueGtgtQuyDoi": 950000.00,
      "tongTienThanhToanQuyDoi": 10450000.00,
      "trangThaiChungTu": "DA_GHI_SO",
      "traLaiHang": "Qua kho",
      "phuongThucLapHoaDon": "Người bán xuất hóa đơn điều chỉnh",
      "hinhThucThanhToan": "Điều chỉnh công nợ",
      "kiemPhieuNhapKho": true,
      "thanhToanNgay": false,
      "lapKemHoaDonDieuChinh": true,
      "soChungTuLienQuan": 0,
      "chiTiet": null,
      "updatedAt": "2026-08-10T03:12:44.512Z"
    }
  ],
  "pagination": { "page": 1, "pageSize": 20, "totalItems": 137, "totalPages": 7 },
  "summary": {
    "tongTienHang": 850000000.00,
    "tongChietKhau": 12000000.00,
    "tongTienThueGtgt": 78500000.00,
    "tongTienThanhToan": 916500000.00
  }
}
```

> `data[]` dùng **cùng một DTO** với `GET /{id}`; danh sách chỉ để `chiTiet = null` (mẫu `ChungTuBanHangDto.java:10-14`). Không tách List/Detail DTO: dòng chi tiết vẫn nạp cùng aggregate ở luồng detail, tách ra chỉ nhân đôi mapper.

| Lỗi | HTTP | messageId |
|---|---|---|
| Không có quyền `TraLaiHangBan.View` | 403 | `MSG_PMKT-E-06469_007` |
| `sort`/`filters[].field` không hợp lệ | **không lỗi** — bỏ qua + log warn (`Searchable.java:11-13`) | — |
| Không có kết quả | 200, `data: []` | FE hiển thị `MSG_PMKT-E-06469_008` |
| `filters` khoảng ngày đảo (`from > to`) | 400 `INVALID_DATE_RANGE` | `MSG_PMKT-E-06469_103` |

### A2 — `GET /api/ban-hang/tra-lai-hang-ban/cot`

Quyền `.View`. Trả `ApiResponse<List<CotMoTa>>` sinh **tự động** từ whitelist `@Searchable` của entity (`BaseCrudController.java:128-135`) — FE dựng bộ lọc động + màn cấu hình cột từ đây, **không hardcode** (BR30).

### A3 — `POST /api/ban-hang/tra-lai-hang-ban/export`

Quyền `.Export`. Xuất **toàn bộ** bản ghi khớp bộ lọc hiện tại (không chỉ trang đang xem) — `BaseCrudController.java:167-190`. Body = cùng `SearchRequest` của A1; query param `mauId` tuỳ chọn (mẫu cột người dùng đã lưu).

Bộ cột mặc định (override `cotMacDinh(LoaiMau.EXPORT)`, mẫu `ChungTuBanHangController.java:188-206`) — đúng thứ tự cột của `SCR_DanhSachTraLaiHangBan.md` §Bảng chính:

| # | alias | Nhãn | Kiểu | Rộng |
|---|---|---|---|---|
| 1 | `ngayHachToan` | Ngày hạch toán | NGAY | 16 |
| 2 | `soChungTu` | Số chứng từ | — | 18 |
| 3 | `tenKhachHang` | Khách hàng | — | 32 |
| 4 | `tongTienThanhToanQuyDoi` | Tổng thanh toán | SO | 20 |
| 5 | `traLaiHang` | Trả lại hàng | — | 18 |
| 6 | `phuongThucLapHoaDon` | Phương thức lập HĐ | — | 28 |
| 7 | `hinhThucThanhToan` | Hình thức thanh toán | — | 20 |
| 8 | `trangThaiChungTu` | Trạng thái | — | 16 |

Tên file: `Chung-tu-tra-lai-hang-ban.xlsx` (`tenFileExport()`).

`cotMacDinh(LoaiMau.IMPORT)` trả **rỗng** ⇒ `POST /import` = 400 `IMPORT_NOT_SUPPORTED` (§1.2 file gốc).

---

## 3. Whitelist `@Searchable` — bắt buộc khai đủ

| alias | path | `sortable` | `keyword` | Nhãn | Vì sao bắt buộc |
|---|---|---|---|---|---|
| `soChungTu` | (base) | ✅ | ✅ | Số chứng từ | đã có ở `BaseChungTuEntity.java:56-58` — **không khai lại** |
| `ngayChungTu` | (base) | ✅ | — | Ngày chứng từ | `BaseChungTuEntity.java:60-62` |
| `ngayHachToan` | (base) | ✅ | — | Ngày hạch toán | `BaseChungTuEntity.java:64-66` — sort mặc định + phễu ngày |
| `trangThaiChungTu` | `status` | ✅ | — | Trạng thái chứng từ | base khai alias `status` (`:70-73`) ⇒ **phải khai lại ở entity con với `alias = "trangThaiChungTu"`** vì FE lọc theo tên đó (`api/traLaiHangBanApi.ts:71`) — xem §7 |
| `chiNhanhId` | (base) | ✅ | — | Chi nhánh | `BaseChungTuEntity.java:44-46` |
| `khachHangId` | `khachHangId` | ✅ | — | Khách hàng | cột `khach_hang_id` |
| `tenKhachHang` | `tenKhachHang` | ✅ | ✅ | Tên khách hàng | lọc `like` + tìm nhanh (`UC:32`) |
| `maSoThue` | `maSoThue` | — | ✅ | Mã số thuế | tìm nhanh |
| `moTa` | `moTa` | — | ✅ | Diễn giải | tìm nhanh |
| `phuongThucLapHoaDon` | `phuongThucLapHoaDon` | ✅ | — | Phương thức lập HĐ | lọc `eq` (`api/traLaiHangBanApi.ts:72`) |
| `kiemPhieuNhapKho` | `kiemPhieuNhapKho` | ✅ | — | Trả lại hàng | FE lọc cột "Trả lại hàng" — xem §4 |
| `thanhToanNgay` | `thanhToanNgay` | ✅ | — | Hình thức thanh toán | xem §4 |
| `tongTienHangQuyDoi` | | ✅ | — | Tổng tiền hàng | sort cột tiền |
| `tongChietKhauQuyDoi` | | ✅ | — | Tổng chiết khấu | |
| `tongTienThueGtgtQuyDoi` | | ✅ | — | Tiền thuế GTGT | |
| `tongTienThanhToanQuyDoi` | | ✅ | — | Tổng thanh toán | cột tiền của SCR |
| `ngayTao` | `ngayTao` | ✅ | — | Ngày tạo | `UC:16` — *"Mặc định sắp xếp theo thời gian tạo chứng từ từ mới tới cũ nhất"*; khai ở **mức class** vì field ở `BaseEntity` (`Searchable.java:25-31`) |

> **Cột không khai `@Searchable` = không lọc/sort được.** Đó là hàng rào có chủ ý (`Searchable.java:11-13`), không phải thiếu sót.

---

## 4. Ánh xạ cột BA ↔ DB ↔ DTO

| # | Cột BA (`SCR` §Bảng chính) | Field BA | Cột DB thật | Field DTO | Lọc | Sort |
|---|---|---|---|---|---|---|
| 1 | STT | — | — | — (FE tính theo phân trang) | N | N |
| 2 | Ngày hạch toán | `NgayHachToan` | `ngay_hach_toan` | `ngayHachToan` | Y (`between`) | Y |
| 3 | Số chứng từ | `SoChungTu` | `so_chung_tu` | `soChungTu` | Y (`like`) | Y |
| 4 | Khách hàng | `KhachHangTen` | `ten_khach_hang` | **`tenKhachHang`** | Y (`like`) | Y |
| 5 | Tổng thanh toán | `TongTienThanhToan` | `tong_tien_thanh_toan_quy_doi` **(MỚI, V3)** | **`tongTienThanhToanQuyDoi`** | N | Y |
| 6 | Trả lại hàng | `TraLaiHang` | — **dẫn xuất** | `traLaiHang` | Y (qua `kiemPhieuNhapKho`) | Y |
| 7 | Phương thức lập HĐ | `PhuongThucLapHoaDon` | `phuong_thuc_lap_hoa_don` **(MỚI, V3)** | `phuongThucLapHoaDon` | Y (`eq`) | Y |
| 8 | Hình thức thanh toán | `HinhThucThanhToan` | — **dẫn xuất** | `hinhThucThanhToan` | Y (qua `thanhToanNgay`) | Y |
| 9 | Trạng thái | `TrangThaiChungTu` | `status` | **`trangThaiChungTu`** | Y (`eq`, tên hằng) | Y |
| 10 | Chức năng | — | — | `trangThaiChungTu` + `soChungTuLienQuan` (FE tự suy nút) | N | N |

> ⚠️ **Bốn cột tên DB lệch tên BA** (in đậm): `KhachHangTen` → `ten_khach_hang`, `TongTienThanhToan` → `tong_tien_thanh_toan_quy_doi`, `TrangThaiChungTu` → `status`, và hai cột nhãn không có cột DB. **Không tạo migration đổi tên**: `ten_khach_hang` / `status` là tên chuẩn của baseline và của `BaseChungTuEntity`; đổi tên = đụng RLS policy + trigger + FE đã code.

### 4.1 Hai cột dẫn xuất

**Cột "Trả lại hàng"** — `SCR` §Bảng chính: *"Label: Qua kho / Không qua kho"*.

```
traLaiHang = kiemPhieuNhapKho == TRUE ? "Qua kho" : "Không qua kho"
```
Nguồn: cột `kiem_phieu_nhap_kho boolean` (đã có, `V1:16482`). Tính ở **mapper** (`TraLaiMapper`), không lưu cột thứ hai.
Lọc: FE gửi `{field: "kiemPhieuNhapKho", op: "eq", value: true}`. **Vì sao không lưu cột nhãn:** hai nguồn sự thật cho cùng một sự kiện, và nhãn là chuỗi hiển thị — đổi chữ là phải backfill cả bảng.
Hằng chuỗi khai ở `model/NhanTraLaiHang.java` (`TRA_LAI_QUA_KHO = "Qua kho"`, `TRA_LAI_KHONG_QUA_KHO = "Không qua kho"`) — khớp `constants/constants.ts:129-132`.

**Cột "Hình thức thanh toán"** — `SCR` §Bảng chính: *"Label: Điều chỉnh công nợ / Hoàn tiền ngay"*.

```
hinhThucThanhToan = thanhToanNgay == TRUE ? "Hoàn tiền ngay" : "Điều chỉnh công nợ"
```
Nguồn: cột `thanh_toan_ngay boolean` (đã có, `V1:16505`). Khớp `constants/constants.ts:135-138`.
⚠ **Đừng nhầm** với cột DB `hinh_thuc_thanh_toan` đang tồn tại (CHECK `'Tiền mặt'/'Chuyển khoản'`, `V1:16543`) — hai thứ khác nhau, xem §12-Q5 của file gốc.

---

## 5. Validation

| # | Luật | Điều kiện | Thời điểm | Thông báo | BR nguồn |
|---|---|---|---|---|---|
| V1 | Quyền xem | thiếu `TraLaiHangBan.View` | đầu handler | `MSG_PMKT-E-06469_007` → 403 | BR25 · `UC:39` |
| V2 | Khoảng ngày | `dateTo < dateFrom` | trước khi dựng spec | `MSG_PMKT-E-06469_103` → 400 | `SCR` §Validate · BR8 |
| V3 | Cỡ trang | `pageSize` ngoài whitelist | `SearchRequest.pageSizeOrDefault()` | không lỗi, về 20 | BR1 |
| V4 | Alias lạ | `field`/`sort` không trong whitelist | `DynamicSpecification` | không lỗi, bỏ qua + log warn | `Searchable.java:11-13` |
| V5 | Tenant | — | `TenantRlsAspect` bind GUC theo transaction | RLS trả tập rỗng nếu thiếu | BR28 |

**V2 là luật duy nhất phải tự cài** — 4 luật còn lại base đã lo.

---

## 6. Lọc · sắp xếp · phân trang · dòng tổng

### 6.1 Bộ lọc mặc định
BE **không** bơm bộ lọc mặc định nào; FE gửi phễu ngày rỗng nghĩa là "Tất cả thời gian" (`api/traLaiHangBanApi.ts:83`). Bộ lọc trạng thái mặc định "Tất cả" (`SCR` §Thanh công cụ) ⇒ **không** thêm `filters` nào. Lối thoát lấy toàn bộ: `POST /search` với body rỗng → `SearchRequest.empty()`.

### 6.2 Sắp xếp mặc định
`UC:16` — *"Mặc định sắp xếp theo thời gian tạo chứng từ từ mới tới cũ nhất"*; `SCR:BR17` — *"Mặc định sắp xếp theo thời gian tạo từ mới đến cũ"*.

FE đã chốt `ngayHachToan:desc,ngayChungTu:desc,soChungTu:asc` (`api/traLaiHangBanApi.ts:57`) và gửi tường minh ở **mọi** request. BE khai `defaultSortAlias()` trả **cùng chuỗi đó** (mẫu `ChungTuBanHangCrudService.java:90-93`) để request không có `sort` cũng ra đúng thứ tự.

> ⚠ **Lệch nhẹ so với BA**: BA nói "thời gian **tạo**" (`ngayTao`), FE+BE dùng "ngày **hạch toán**". Lý do FE chọn vậy: mũi tên sort về trạng thái "đã bỏ sắp xếp" phải rơi đúng thứ tự lúc mở màn. `ngayTao` vẫn khai `@Searchable(sortable)` để đổi được bằng một dòng. **Ghi vào §12 để BA biết** (không tạo Q riêng vì FE đã quyết và không ai phản đối).
> `SortResolver` của core tự nối `id asc` làm khoá cuối ⇒ phân trang ổn định, không cần khai.

### 6.3 Phân trang
Mặc định 20 (`SearchRequest.java:51-53` và `SCR:BR10`), **1-based** ở cả request và response (`PageResponse.PageInfo`). `SCR:BR10` nói *"Khi người dùng scroll thì load thêm 20 bản ghi"* — infinite scroll là việc FE, wire vẫn là phân trang.

### 6.4 Dòng tổng cộng (BR31)
4 cột: `tongTienHang` · `tongChietKhau` · `tongTienThueGtgt` · `tongTienThanhToan` (`api/model.ts:194-199`), **theo đồng tiền hạch toán** (cột `*_quy_doi`).

Phạm vi: **toàn bộ** tập đã lọc, không phải trang hiện tại (BR31 *"tính động theo tập dữ liệu thực tế của toàn bộ bản ghi (bao gồm dữ liệu sau khi filter, tìm kiếm)"*).

Cài: override `summary(SearchRequest)` → một truy vấn aggregate trên **chính** `specCuaRequest(req)` của request đang xem, y hệt `ChungTuBanHangCrudService.java:191-195`. Dựng lại điều kiện lọc bằng tay là cách chắc chắn nhất để tổng lệch với danh sách.

Tập rỗng: `SUM` trả `NULL` ⇒ `TongHopTraLaiHangBanDto` phải `COALESCE(..., 0)` ở SQL (không để `null` lên FE, `TotalBreakdown` sẽ hiện ô trống).

---

## 7. Điểm cài đặt cần cẩn thận: alias `trangThaiChungTu`

`BaseChungTuEntity.java:70-73` khai `@Searchable(sortable = true, label = "Trạng thái chứng từ")` trên field `status` ⇒ alias mặc định là **`status`** (`Searchable.java:45-46`: *"Rỗng → dùng tên field Java"*).

Nhưng FE lọc/sort bằng **`trangThaiChungTu`** (`api/traLaiHangBanApi.ts:71`, `api/model.ts:171`). Hai cách:

| | A — FE đổi sang `status` | **B (chọn) — entity con khai thêm alias ở mức class** |
|---|---|---|
| Cách làm | sửa `api/traLaiHangBanApi.ts` + `model.ts` + test | `@Searchable(alias = "trangThaiChungTu", path = "status", sortable = true, label = "Trạng thái chứng từ")` trên `@Entity class TraLaiHangBan` |
| Chi phí | sửa FE đã test xanh, và lệch với `ChungTuBanHangDto.java:84` (cũng phơi `trangThaiChungTu`) | 1 dòng annotation; `Searchable` là `@Repeatable` và khai ở mức class được (`Searchable.java:25-35`) |
| Rủi ro | — | có **hai** alias cùng trỏ `status` (`status` từ base + `trangThaiChungTu`) ⇒ `GET /cot` trả trùng một cột hai lần. **Chốt an toàn:** unit test ghim danh sách `CotMoTa` — nếu trùng thì lọc bớt ở `moTaCot()` |

DTO phơi field tên `trangThaiChungTu` (kiểu `String`, giá trị = `status.name()`) — giống `ChungTuBanHangDto.java:84`.

---

## 8. Tương tranh & transaction

Chỉ đọc. `search`/`cot`/`export` đều `@Transactional(readOnly = true)` do base quản. **Bắt buộc có transaction** dù chỉ đọc: `TenantRlsAspect` bind GUC `app.tenant_id` theo transaction, thiếu nó thì RLS trả tập rỗng (`AbstractChungTuCrudService.java:81-83`).

`summary` là **truy vấn thứ hai** trong cùng transaction readOnly — chấp nhận, và là cách duy nhất để tổng khớp bộ lọc mà không kéo hết bản ghi về JVM.

---

## 9. Kiểm thử

### 9.1 Unit (`@Tag("unit")`, không cần Docker)

| Lớp test | Case | Input → kỳ vọng |
|---|---|---|
| `TraLaiMapperTest` | `traLaiHang` dẫn xuất | `kiemPhieuNhapKho = true` → `"Qua kho"`; `false`/`null` → `"Không qua kho"` |
| | `hinhThucThanhToan` dẫn xuất | `thanhToanNgay = true` → `"Hoàn tiền ngay"`; `false`/`null` → `"Điều chỉnh công nợ"` |
| | `trangThaiChungTu` | `status = DA_GHI_SO` → `"DA_GHI_SO"` (**không** phải "Đã ghi sổ") |
| | list DTO bỏ `chiTiet` | mapper danh sách → `chiTiet == null` |
| `TraLaiHangBanSearchableTest` | whitelist **ghim** | tập alias sinh từ `SearchableRegistry` **chứa đủ** 4 alias lọc + 3 alias sort của FE; `GET /cot` không trả trùng alias (§7) |
| `TraLaiHangBanCrudServiceTest` | sort mặc định | `defaultSortAlias()` == `"ngayHachToan:desc,ngayChungTu:desc,soChungTu:asc"` |
| | khoảng ngày đảo | `filters` `between ["2026-08-31","2026-08-01"]` → `ApiException` 400 `MSG_..._103` |
| `TongHopTraLaiHangBanDtoTest` | tập rỗng | 4 tổng == `BigDecimal.ZERO`, không `null` |
| `CotMacDinhExportTest` | bộ cột export | 8 cột đúng thứ tự §2-A3; `cotMacDinh(IMPORT)` rỗng |

### 9.2 Tích hợp (cần Docker — **chưa chạy được**, R8)

| Lớp | Kiểm gì chỉ DB thật làm được |
|---|---|
| `TraLaiHangBanSearchIT` | RLS: user tenant A không thấy chứng từ tenant B; policy `pv_select` theo `don_vi_id` |
| | `summary` khớp `SUM` thực tế của tập đã lọc (137 bản ghi seed) |
| | index sort mặc định được dùng (`EXPLAIN` có `Index Scan`) |
| `TraLaiHangBanExportIT` | file `.xlsx` mở được, đủ số dòng = `totalItems` |

---

## 10. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR1 phân trang | §6.3 |
| BR2 hiển thị & sắp xếp | §4, §6.2 |
| BR8 khoảng thời gian | §5-V2, §6.1 |
| BR11 tìm kiếm/lọc/sắp xếp | §3, §6.1 |
| BR12 trạng thái chứng từ | §4 dòng 9, §7 |
| BR13.1 nút thao tác | §4 dòng 10 — DTO trả `trangThaiChungTu` + `soChungTuLienQuan` để FE tự ẩn/hiện; **BE không quyết định UI** |
| BR25 phân quyền | §5-V1 |
| BR28 multi-tenant | §5-V5, §8 |
| BR30 ẩn/hiện cột | A2 `GET /cot` — FE dựng từ whitelist, không hardcode |
| BR31 dòng tổng | §6.4 |
| BR32 copy · BR38 group · BR44 truncate | **FE thuần** — không có phần BE |
| BR39 xuất Excel | A3 |
| BR45 thao tác hàng loạt | không thuộc file này — xem [05](05-xoa.md), [07](07-ghi-so.md), [08](08-bo-ghi-so.md) |
