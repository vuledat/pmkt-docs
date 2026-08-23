# F01 — Danh sách chứng từ bù trừ công nợ

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F01** |
| Use case | **PMKT-U-14688** — `4.usecases/PMKT-U-14688_BTCN_DanhSach/UC_BTCN_DanhSach.md` |
| Màn hình | `5.screens/SCR_BTCN_DanhSach.md` (mô tả **khác biệt**; nền là `PMKT-E-09980_PhieuKTTH/5.screens/SCR_PhieuKTTH/SCR_PhieuKTTH_DanhSach.md`) |
| Endpoint phụ trách | **A1** `POST /api/ke-toan-tong-hop/phieu-ke-toan/search` · **A2** `GET /api/ke-toan-tong-hop/phieu-ke-toan/cot` |
| Quyết định liên quan | **D1** (module), **D2** (chỉ cài phần đọc của Phiếu KTTH), **D12** (loại phiếu hệ thống tạo) — xem [00 §0](00-ke-hoach-tong.md) |

---

## 1. Bối cảnh

Chứng từ bù trừ **không có màn danh sách riêng**: nó hiển thị chung trên danh sách Phiếu kế toán tổng hợp với Loại nghiệp vụ = "Bù trừ công nợ".

> `SCR_BTCN_DanhSach.md:5` — "Chứng từ bù trừ công nợ hiển thị chung trên **danh sách Phiếu kế toán tổng hợp** với Loại nghiệp vụ 'Bù trừ công nợ'; **không xây màn hình danh sách độc lập**."

Epic PMKT-E-09980 (chủ sở hữu màn danh sách đó) **chưa có một dòng Java nào** — xem [00 §2.1](00-ke-hoach-tong.md). Theo **D2**, đợt này cài phần **chỉ đọc** của Phiếu KTTH; luồng ghi (thêm/sửa phiếu loại 1–4) để lại cho E-09980. Nếu BA/PO chốt ngược (**Q1**) thì bỏ toàn bộ file này.

---

## 2. Quyết định riêng của chức năng

| # | Quyết định | Lý do · vì sao không chọn cách kia |
|---|---|---|
| **F01-a** | Controller riêng `PhieuKeToanTongHopController` ở `ke_toan_tong_hop/phieu/internal/controller/`, **không** gộp vào `BuTruCongNoController` | Base path khác nhau (`/phieu-ke-toan` vs `/bu-tru-cong-no`), mã chức năng khác nhau (`PhieuKeToan` vs `BuTruCongNo`), và danh sách phục vụ **mọi** loại phiếu KTTH chứ không riêng bù trừ. Gộp thì E-09980 phải sửa lại controller của module bù trừ |
| **F01-b** | Kế thừa `BaseCrudController`, **không** kế thừa `BaseChungTuController` cho controller danh sách | `BaseChungTuController` làm lộ `/ghi-so`, `/bo-ghi-so`, `/nhan-ban`, 3 endpoint hàng loạt (`BaseChungTuController.java:93-184`) — với phiếu KTTH chung thì các thao tác đó thuộc E-09980, còn với chứng từ bù trừ thì chúng đã nằm ở `BuTruCongNoController` (A10–A12). Lộ hai bản trùng nhau là mời gọi FE gọi nhầm bản không có logic hoàn trả công nợ |
| **F01-c** | Không tạo endpoint `/danh-sach-bu-tru` riêng | BA cấm ("không xây màn hình danh sách độc lập"). FE lọc bằng `filters: [{field:"loaiPhieu", op:"in", value:["BU_TRU_CONG_NO"]}]` |

---

## 3. Hợp đồng API

### 3.1 A1 — `POST /api/ke-toan-tong-hop/phieu-ke-toan/search`

**Quyền:** `PhieuKeToan.View` (`QuyenChecker.VIEW` — `core/controller/QuyenChecker.java:27`).

Body theo `SearchRequest` chuẩn (`core/request/SearchRequest.java:33-40`) — **không định nghĩa body riêng**.

```jsonc
// Request
{
  "page": 1,
  "pageSize": 20,
  "sort": "ngayHachToan:desc,soChungTu:asc",
  "keyword": "PBT-000012",
  "logic": "AND",
  "filters": [
    { "field": "loaiPhieu",     "op": "in",      "value": ["BU_TRU_CONG_NO"] },
    { "field": "ngayHachToan",  "op": "between", "value": ["2026-08-01", "2026-08-31"] },
    { "field": "status",        "op": "in",      "value": ["NHAP", "DA_GHI_SO"] }
  ]
}
```

| Field | Kiểu | Bắt buộc | Ràng buộc | Nguồn BA |
|---|---|---|---|---|
| `page` | int | N | ≥ 1, mặc định 1 | BR1 |
| `pageSize` | int | N | whitelist 10/20/50/100/200, khác → 20 (`SearchRequest.java:51-53`) | BR1 |
| `sort` | string | N | `col:dir[,col:dir]`, chỉ field khai `@Searchable(sortable = true)` | BR11.3 |
| `keyword` | string | N | tìm trên field khai `@Searchable(keyword = true)` | BR11.1 |
| `filters[].field` | string | N | alias whitelist; field không khai bị **bỏ qua** kèm log warn (`core/shared/search/Searchable.java:11-13`) | BR11.2 |
| `logic` | string | N | `AND` (mặc định) / `OR`; `keyword` luôn ghép AND | `SearchRequest.java:29-30` |

```jsonc
// Response 200 — PageResponse<PhieuKeToanTongHopDto>, KHÔNG bọc ApiResponse
// Shape đã kiểm: core/response/PageResponse.java:20-23
{
  "data": [
    {
      "id": "8f1c…",
      "loaiPhieu": "BU_TRU_CONG_NO",
      "tenLoaiPhieu": "Bù trừ công nợ",
      "soChungTu": "PBT-000012",
      "ngayChungTu": "2026-08-11",
      "ngayHachToan": "2026-08-11",
      "moTa": "Bù trừ công nợ phải thu, phải trả với Công ty TNHH ABC",
      "loaiTienId": "…", "maLoaiTien": "VND", "tyGia": 1,
      "tongTien": 5000000.00,
      "status": "DA_GHI_SO",
      "ngayCapNhat": "2026-08-11T09:12:33Z",
      "phienBan": 3,
      "choPhepXemChiTiet": true,
      "choPhepSua": false,
      "choPhepXoa": false,
      "choPhepGhiSo": false,
      "choPhepBoGhi": true,
      "duongDanChiTiet": "BU_TRU_CONG_NO"
    }
  ],
  "pagination": { "page": 1, "pageSize": 20, "totalItems": 137, "totalPages": 7 },
  "summary": { "tongTien": 812345678.00 }
}
```

> `ngayCapNhat` trả ra vì `DELETE /{id}` dùng nó làm token optimistic-lock (`core/request/DeleteRequest.java:17`) — xem [07 §2](07-xoa-chung-tu-bu-tru.md).
>
> `summary` là slot có sẵn của `PageResponse` cho **dòng tổng toàn cục** (§8.4) — không phải field tự chế.

**Lỗi** — body theo `ApiError` = `{ code, message, messageId, details }` (`core/shared/error/ApiError.java:11-15`):

| HTTP | `code` | `messageId` | Khi nào |
|---|---|---|---|
| 403 | `FORBIDDEN` | `MSG_PMKT-E-14294_005` | Thiếu `PhieuKeToan.View` |
| 500 | `INTERNAL_ERROR` | `MSG_PMKT-E-14294_022` | Lỗi hệ thống khi tải danh sách (`UC_BTCN_DanhSach.md:51`) |

### 3.2 A2 — `GET /api/ke-toan-tong-hop/phieu-ke-toan/cot`

**Quyền:** `PhieuKeToan.View`. Trả `ApiResponse<List<CotMoTa>>` — metadata cột cho FE dựng grid, do `BaseCrudController.java:131-135` cấp sẵn, **không viết lại**.

---

## 4. Ánh xạ cột: BA ↔ DB ↔ DTO

`SCR_BTCN_DanhSach.md` chỉ mô tả điểm khác biệt; bộ cột lấy từ `UC_BTCN_DanhSach.md:13`.

| # | Cột BA | Cột DB (`ktth_phieu_ke_toan_tong_hop`) | Field DTO / alias lọc | Lọc | Sort |
|---|---|---|---|---|---|
| 1 | STT | — | *(FE tính theo BR2: `(trang−1)×coTrang + vị trí`)* | — | — |
| 2 | Số chứng từ | `so_chung_tu` | `soChungTu` | ✅ contains | ✅ |
| 3 | Loại nghiệp vụ | `loai_phieu` | `loaiPhieu` (enum) + `tenLoaiPhieu` (nhãn hiển thị) | ✅ in | ✅ |
| 4 | Ngày chứng từ | `ngay_chung_tu` | `ngayChungTu` | ✅ between | ✅ |
| 5 | Ngày hạch toán | **`ngay_hach_toan`** ⚠ đang là `timestamptz` (`V202:47`), phải đổi `date` — xem [09 §2](09-thiet-ke-db.md) | `ngayHachToan` | ✅ between | ✅ (sort mặc định) |
| 6 | Diễn giải | `mo_ta` | `moTa` | ✅ contains, keyword | — |
| 7 | Tổng tiền | `tong_tien` | `tongTien` | ✅ between | ✅ |
| 8 | Trạng thái | **`status`** (`V348:75`) — **không** dùng `trang_thai` (`V202:52`), xem R7 | `status` (`TrangThaiChungTu`) | ✅ in | ✅ |
| 9 | Chức năng | — | 5 field boolean ở §4.1 | — | — |

> ⚠️ **Cột lệch tên BA ↔ DB:** BA gọi "Diễn giải" nhưng cột DB là **`mo_ta`** (`V202:44`) và LDM cũng là `MoTa` (`ldm-KTTH.puml:17`). Giữ nguyên tên DB, đặt alias `@Searchable(alias = "moTa", label = "Diễn giải")`. **Không** tạo migration đổi tên cột.
>
> ⚠️ **`tongTien` với chứng từ bù trừ** = Tổng(Số tiền tab Hạch toán) — theo `SCR_BTCN_DanhSach.md:20`: "dòng xử lý chênh lệch tỷ giá có số tiền nguyên tệ = 0 nên không ảnh hưởng". Giá trị này do luồng Lưu tính và ghi vào `tong_tien`, **không** tính lại lúc đọc danh sách (tránh N+1). Xem [04 §6](04-luu-chung-tu-bu-tru.md).

### 4.1 Field phụ trong DTO để FE ẩn/hiện nút (BR13.1)

| Nút | Điều kiện (nguồn BA) | Field DTO |
|---|---|---|
| Xem chi tiết | Luôn (BR13.1) | `choPhepXemChiTiet` = `true` |
| **Sửa** | **Không bao giờ** với `loaiPhieu = BU_TRU_CONG_NO` (`SCR_BTCN_DanhSach.md:33`) | `choPhepSua` = `loaiPhieu != BU_TRU_CONG_NO && status.choPhepSua()` |
| Xóa | `status != DA_GHI_SO` (`SCR_BTCN_DanhSach.md:34`, BR13.1) | `choPhepXoa` |
| Ghi sổ | `status != DA_GHI_SO` | `choPhepGhiSo` |
| Bỏ ghi | `status == DA_GHI_SO` (BR42.2) | `choPhepBoGhi` |
| Điều hướng màn chi tiết | `loaiPhieu = BU_TRU_CONG_NO` → mở `SCR_BTCN_ChungTu_XemChiTiet`, loại khác → màn chi tiết Phiếu KTTH (`SCR_BTCN_DanhSach.md:29`) | `duongDanChiTiet` = giá trị `loaiPhieu` |

`choPhepSua/Xoa/GhiSo/BoGhi` tính **ở service** từ `status` + `loaiPhieu`, không tính ở FE — BR25 nói ẩn nút là quyết định của server, và FE không được tự suy luật nghiệp vụ.

> **Lưu ý:** các field trên **không** tính quyền người dùng. FE giao cắt thêm với danh sách quyền của phiên. Nếu BA muốn server trả luôn kết quả đã giao cắt thì đó là thay đổi hợp đồng — nêu ở [00 §12](00-ke-hoach-tong.md).

---

## 5. Validation

| # | Luật | Thời điểm | Xử lý | BR nguồn |
|---|---|---|---|---|
| V1 | Có quyền `PhieuKeToan.View` | Đầu handler | 403 + `MSG_..._005` | BR25.2, `UC_BTCN_DanhSach.md:50` |
| V2 | `field` trong `filters` phải thuộc whitelist `@Searchable` | `DynamicSpecification` | **Bỏ qua** field lạ + log warn (không 500) | `core/shared/search/Searchable.java:11-13` |
| V3 | `pageSize` ngoài whitelist | `SearchRequest.pageSizeOrDefault()` | Quy về 20 | BR1 |
| V4 | `sort` trỏ field không `sortable` | `SortResolver` | Bỏ qua, dùng sort mặc định | BR11.3 |
| V5 | Dữ liệu chỉ trong tenant hiện hành | RLS ở DB (`V202:75-79`) | Không nhận `tenantId` từ client | BR28 |
| V6 | Bỏ bản ghi `da_xoa = true` | Spec mặc định của `BaseRepository` | — | BR29.1 |

**Không** có validation nghiệp vụ nào khác — đây là endpoint chỉ đọc.

---

## 6. Luồng xử lý

1. `PhieuKeToanTongHopController.search(request)` — `quyen.require(MaChucNang.PHIEU_KE_TOAN, QuyenChecker.VIEW)`.
2. Gọi `service().search(request)` — **kế thừa nguyên** từ `BaseCrudController.java:121-129`, không override.
3. `AbstractCrudService` dựng `DynamicSpecification` từ `filters` + `keyword` theo whitelist `@Searchable` của `PhieuKeToanTongHop`.
4. `SortResolver` áp `sort`; rỗng → sort mặc định (§8.2).
5. Repository trả `Page<PhieuKeToanTongHop>`; mapper → `PhieuKeToanTongHopDto` (`business/PhieuKtthMapper`), tính 5 field boolean §4.1.
6. Trả `PageResponse<PhieuKeToanTongHopDto>`.

Không có bước nào chạm sổ cái, không transaction ghi. **Không viết mới bước nào** ngoài mapper.

---

## 7. Tương tranh & transaction

`@Transactional(readOnly = true)` ở service. Không khoá, không idempotency — endpoint chỉ đọc.

---

## 8. Phân trang · sắp xếp · lọc · dòng tổng

### 8.1 Bộ lọc mặc định
FE gửi, BE **không bơm ngầm**. Bộ lọc thời gian mặc định "Đầu tháng tới hiện tại" (BR11.2.1) do FE tính rồi gửi `ngayHachToan between`. Lý do không bơm ở BE: cùng một endpoint phục vụ cả danh sách Phiếu KTTH chung lẫn màn lọc riêng bù trừ; bơm ngầm sẽ khiến FE không có lối thoát để lấy toàn bộ.

### 8.2 Sắp xếp mặc định
BR2: **Ngày hạch toán giảm dần**, cùng ngày thì **Số chứng từ tăng dần** — trùng với `UC_BTCN_DanhSach.md:13` ("sắp xếp mặc định Ngày hạch toán mới nhất lên trước").

Cài bằng `Sort` mặc định trong repository/service khi `request.sort()` rỗng: `ngayHachToan DESC, soChungTu ASC`. Cần index hỗ trợ — xem [09 §4](09-thiet-ke-db.md) (`V202:66-68` chỉ có index `(tenant_id, ngay_chung_tu)`, **không phủ** sort mặc định).

BR2 còn có luật "bản ghi không hoạt động xuống cuối" — **không áp dụng**: phiếu KTTH không có trường trạng thái hoạt động/ngừng hoạt động.

### 8.3 Phân trang
`SearchRequest`: **1-based**, mặc định `pageSize = 20`, whitelist `10/20/50/100/200` (`core/request/SearchRequest.java:47-53`). Không viết lại.

### 8.4 Dòng tổng cộng (BR31)
`SCR_BTCN_DanhSach.md` **không** mô tả dòng tổng cho danh sách phiếu KTTH; BR31 lại nói "nếu tồn tại cột số tiền thì tự động hiển thị dòng tổng". Cột `Tổng tiền` là cột tiền ⇒ theo BR31 phải có.

**Cách cài — không phải sửa `core`** (§2.4-Đ2 ở [00](00-ke-hoach-tong.md)): `PageResponse<T>(List<T> data, PageInfo pagination, Object summary)` đã có sẵn slot `summary`, và javadoc của nó nói đúng mục đích này — *"bổ sung `summary` (nullable) cho các màn cần tổng footer TOÀN CỤC theo bộ lọc… tổng tính trên toàn bộ bản ghi sau lọc, không chỉ trang hiện tại"* (`core/response/PageResponse.java:12-14`). Dựng bằng `PageResponse.of(page, pageNumber, summary)` (`:31-36`).

- Kiểu `summary`: record riêng của màn, vd `record TongPhieuKtthDto(BigDecimal tongTien) {}` — base để `Object` chính là để mỗi màn gắn record riêng mà không ràng buộc `core` (`PageResponse.java:15-16`).
- Tính bằng **query riêng** `SUM(tong_tien)` áp đúng `Specification` của bộ lọc hiện hành, chạy song song với query trang — **không** cộng từ `data` (chỉ có 20 dòng).
- `SUM` trên tập rỗng trả `0`, không `null`.

> ⚠️ `tong_tien` với chứng từ bù trừ là **nguyên tệ** (§4 ghi chú). Cộng tổng qua nhiều loại tiền khác nhau là số vô nghĩa. Đề xuất: `summary` chỉ trả `tongTien` khi bộ lọc đã ràng một `loaiTienId` duy nhất, ngược lại trả `null` kèm cờ `daLocMotLoaiTien = false`. **Cần BA xác nhận** — nêu ở [00 §12](00-ke-hoach-tong.md).

---

## 9. Kiểm thử

### 9.1 Unit test (`@Tag("unit")`)

| Lớp test | Kiểm gì |
|---|---|
| `PhieuKtthMapperTest` | `status = DA_GHI_SO` → `choPhepXoa=false`, `choPhepGhiSo=false`, `choPhepBoGhi=true` |
| `PhieuKtthMapperTest` | `loaiPhieu = BU_TRU_CONG_NO` + `status = NHAP` → `choPhepSua = false` (dù trạng thái cho sửa) |
| `PhieuKtthMapperTest` | `loaiPhieu = KHAC` + `status = NHAP` → `choPhepSua = true` |
| `PhieuKtthMapperTest` | `duongDanChiTiet` = `BU_TRU_CONG_NO` với phiếu bù trừ |
| `LoaiPhieuKTTHTest` | Converter enum ⇄ chuỗi tiếng Việt khớp **đúng** whitelist CHECK `V202:38-42` + `V258:8-13` (6 giá trị) |
| `LoaiPhieuKTTHTest` | `BU_TRU_CONG_NO.nguoiDungChonDuoc() == false` (D12) |

### 9.2 Test tích hợp (cần Docker)

| Lớp test | Kiểm gì |
|---|---|
| `PhieuKeToanTongHopSearchIT` | Sort mặc định `ngayHachToan desc, soChungTu asc` với 3 bản ghi cùng ngày |
| `PhieuKeToanTongHopSearchIT` | Lọc `loaiPhieu in [BU_TRU_CONG_NO]` trả đúng tập |
| `PhieuKeToanTongHopSearchIT` | Field lọc ngoài whitelist bị bỏ qua, **không** 500 |
| `PhieuKeToanTongHopSearchIT` | Bản ghi `da_xoa = true` không xuất hiện |
| `PhieuKeToanTongHopSearchIT` | RLS: tenant A không thấy bản ghi tenant B |
| `PhieuKeToanTongHopSearchIT` | `summary.tongTien` = `SUM` toàn tập sau lọc, không phải trang hiện tại; tập rỗng → `0` |
| `PhieuKtthSchemaIT` | **R9** — đọc/ghi thật một bản ghi qua entity, bắt lỗi lệch **tên cột** với schema (thứ `JpaMetamodelArchTest` không kiểm được) |

> `JpaMetamodelArchTest` (`src/test/java/vn/vtt/pmkt/cell/arch/JpaMetamodelArchTest.java:25-48`) **đã có sẵn** và tự động phủ 4 entity mới ngay khi chúng mang `@Entity` — không phải viết thêm gì, nhưng cũng không thay được `PhieuKtthSchemaIT`.

---

## 10. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR1 | §8.3 — `SearchRequest`, 1-based, mặc định 20 |
| BR2 | §8.2 sort mặc định · §4 cột STT do FE tính |
| BR11.1 | `keyword` trên field `@Searchable(keyword = true)`: `soChungTu`, `moTa` |
| BR11.2 | `filters` + `logic` AND · toán tử theo kiểu cột |
| BR11.3 | Sắp xếp server-side trên toàn bộ tập sau lọc |
| BR12 | `status` quyết định nút hiển thị (§4.1) |
| BR13.1 | 5 field boolean §4.1 |
| BR25 | `quyen.require(PhieuKeToan, View)` |
| BR28 | RLS `tenant_isolation` (`V202:75-79`) |
| BR29.1 | Bỏ `da_xoa = true` |
| BR31 | §8.4 dòng tổng (cần Dev BE chốt cách trả) |
| BR33 | DTO trả `status` để FE tô màu |
| BR42.2 | Nút Bỏ ghi ẩn với dòng chưa ghi sổ |
| BR46 | Trường hệ thống do base entity quản, là cột ẩn trên danh sách |

**Chưa áp được:** BR30 (ẩn/hiện cột — `common/ui_config`, ngoài phạm vi) · BR32 (copy grid — FE) · BR38 (nhóm cột — tiện ích báo cáo) · BR39 (xuất Excel — **Q12**) · BR44 (truncate — FE) · BR45 (thao tác hàng loạt — **Q11**).
