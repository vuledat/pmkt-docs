# F1 — Xem danh sách Chứng từ điều chỉnh giá

| | |
|---|---|
| Mã chức năng | **F1** |
| UC nguồn | [PMKT-U-07665 — Xem danh sách](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/4.usecases/PMKT-U-07665_XemDanhSach/UC_XemDanhSach.md) |
| Màn hình nguồn | [SCR_DanhSachDieuChinhGia.md](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/5.screens/SCR_DanhSachDieuChinhGia.md) |
| Endpoint phụ trách | **A1** `POST /search` · **A2** `GET /cot` |

## 1. Quyết định riêng

- Theo **D1** (§0 file gốc): cả hai endpoint **kế thừa nguyên** từ `BaseCrudController` ([:121](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/controller/BaseCrudController.java), [:131](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/controller/BaseCrudController.java)) — không viết lại handler nào. Việc của module là (a) khai `@Searchable` đúng whitelist, (b) cài `tongHop(...)` cho dòng tổng.
- Dòng tổng (`summary`) đi theo mẫu `ChungTuBanHangRepositoryImpl.tongHop` ([:49](../../cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/internal/repository/ChungTuBanHangRepositoryImpl.java)) — **không chọn** tính tổng trong Java trên trang hiện tại: BR31 yêu cầu tổng trên toàn tập sau lọc.

## 2. Hợp đồng API

### A1 — `POST /api/ban-hang/dieu-chinh-gia-hang-ban/search` · quyền `DieuChinhGiaHangBan.View`

```jsonc
// Request — body chuẩn SearchRequest (core/request/SearchRequest.java:33)
{
  "page": 1,
  "pageSize": 10,
  "sort": "ngayHachToan:desc,soChungTu:desc",
  "keyword": "BGG00001",
  "logic": "AND",
  "filters": [
    { "field": "huongDieuChinhGia", "op": "eq", "value": "GiamGia" },
    { "field": "status",            "op": "in", "value": ["NHAP", "DA_GHI_SO"] },
    { "field": "khachHangId",       "op": "eq", "value": "6f1e…-uuid" },
    { "field": "ngayHachToan",      "op": "between", "value": ["2026-08-01", "2026-08-31"] }
  ]
}
```

| Field request | Kiểu | Bắt buộc | Ràng buộc | Nguồn BA |
|---|---|---|---|---|
| `page` | int | N | ≥ 1, mặc định 1 | BR1 |
| `pageSize` | int | N | whitelist `10/20/50/100/200`, **FE gửi 10** | SCR_DanhSach BR1 |
| `sort` | string | N | `col:dir[,col:dir]`, `col` phải là alias `@Searchable(sortable)` | BR11.3 |
| `keyword` | string | N | tìm trên `soChungTu`, `tenKhachHang` | SCR_DanhSach dòng 15 |
| `filters[]` | list | N | `field` phải nằm trong whitelist, giá trị lạ ⇒ 400 | BR11.2 |
| `logic` | string | N | `AND` (mặc định) / `OR` | — |

```jsonc
// Response 200 — PageResponse (core/response/PageResponse.java:20)
{
  "data": [
    {
      "id": "…",
      "soChungTu": "BGG00001",
      "ngayChungTu": "2026-08-10",
      "ngayHachToan": "2026-08-10",
      "huongDieuChinhGia": "GiamGia",
      "thanhToanNgay": false,
      "hinhThucThanhToan": "DieuChinhCongNo",
      "lapKemHoaDonDieuChinh": true,
      "khachHangId": "…", "tenKhachHang": "Công ty TNHH ABC",
      "maSoThue": "0101234567", "diaChi": "…",
      "nhanVienBanHangId": null, "dienGiai": "Giảm giá hàng bán tháng 8",
      "nguonChungTu": "CHUNG_TU_BAN_HANG",
      "soHoaDonDieuChinh": "00001234",
      "loaiTienId": "…", "tyGia": 1,
      "tongTienHang": 1000000, "tongChietKhau": 0,
      "tongTienThueGtgt": 100000, "tongTienThanhToan": 1100000,
      "tongThanhTienQuyDoi": 1000000, "tongChietKhauQuyDoi": 0,
      "tongTienThueGtgtQuyDoi": 100000, "tongTienThanhToanQuyDoi": 1100000,
      "trangThaiChungTu": "NHAP",
      "chungTuThanhToan": null,
      "updatedAt": "2026-08-10T03:12:44Z"
    }
  ],
  "pagination": { "page": 1, "pageSize": 10, "totalItems": 37, "totalPages": 4 },
  "summary": { "tongTienThanhToanQuyDoi": 41250000 }
}
```

> `chiTiet` **không** có trong projection danh sách — chỉ `GET /{id}` trả (xem [02](02-xem-chi-tiet.md)). Khớp `model.ts` dòng 240-241.

| Lỗi | HTTP | messageId |
|---|---|---|
| Thiếu quyền `.View` | 403 | `MSG_PMKT-E-07664_007` |
| `filters[].field` không có trong whitelist | 400 | — (lỗi kỹ thuật, `GlobalExceptionHandler`) |
| Không có kết quả | **200** + `data: []` | FE hiển thị `MSG_PMKT-E-07664_008` |

### A2 — `GET /cot` · quyền `DieuChinhGiaHangBan.View`

Trả `List<CotMoTa>` sinh từ `@Searchable(label = …)` của entity — FE dùng để dựng bộ lọc nâng cao và bảng cấu hình cột (BR30). Không có tham số.

## 3. Ánh xạ cột BA ↔ DB ↔ DTO

### 3.1 Cột hiển thị của lưới (SCR_DanhSach dòng 22-33)

| # | Cột BA | Field BA | Cột DB thật | Field DTO | Lọc | Sort |
|---|---|---|---|---|---|---|
| 1 | Ngày hạch toán | `NgayHachToan` | `ngay_hach_toan` | `ngayHachToan` | ✅ `between` | ✅ |
| 2 | Số chứng từ | `SoChungTu` | `so_chung_tu` | `soChungTu` | ✅ keyword | ✅ |
| 3 | Số hóa đơn điều chỉnh | `SoHoaDonDieuChinh` | `so_hoa_don_dieu_chinh` | `soHoaDonDieuChinh` | ❌ | ✅ |
| 4 | Phương thức điều chỉnh | `HuongDieuChinhGia` | **`loai_dieu_chinh`** ⚠ | `huongDieuChinhGia` | ✅ `eq/in` | ✅ |
| 5 | Khách hàng | `KhachHangTen` | `ten_khach_hang` | `tenKhachHang` | ✅ keyword | ✅ |
| 6 | Tổng tiền thanh toán | `TongTienThanhToan` | **`tong_thanh_toan_chenh_lech`** ⚠ (+ cột quy đổi mới, §9.2 của [09](09-thiet-ke-db.md)) | `tongTienThanhToan` / `tongTienThanhToanQuyDoi` | ❌ | ✅ |
| 7 | Hình thức thanh toán | `HinhThucThanhToan` | `hinh_thuc_thanh_toan` + `thanh_toan_ngay` (mới) | `hinhThucThanhToan`, `thanhToanNgay` | ✅ `eq/in` | ❌ |
| 8 | Trạng thái | `TrangThaiGhiSo` | **`status`** ⚠ (cột `trang_thai_chung_tu` bị DROP — D7) | `trangThaiChungTu` | ✅ `eq/in` | ✅ |
| 9 | Thao tác | — | — | suy từ `trangThaiChungTu` (§3.3) | — | — |

> ⚠ **Ba cột tên DB lệch tên BA** (#4, #6, #8). **Không** tạo migration đổi tên: `loai_dieu_chinh` đã có CHECK constraint và comment mô tả đúng nghĩa Tăng/Giảm ([V1__baseline.sql:16322](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)); `tong_thanh_toan_chenh_lech` mô tả đúng bản chất "chênh lệch". Ánh xạ ở tầng entity là đủ, và mọi tên DB xuất hiện trong index/policy/comment đã có sẵn.

**Cột "Số chứng từ" — lưu ý nghiệp vụ (SCR_DanhSach dòng 34):** *"Số chứng từ ở đây được lấy số chứng từ tại tab đầu tiên (VD người dùng chọn thanh toán ngay = Tiền mặt > Phiếu thu/Phiếu chi. Số chứng từ lấy Phiếu thu/Phiếu chi)"*. Nhưng cùng SCR (dòng 34, câu đầu) lại ghi thứ tự tab là **Công nợ > Hóa đơn**, tức tab đầu tiên luôn là Công nợ.
→ **Cài:** cột `so_chung_tu` (tab Công nợ) là số định danh của chứng từ và là cột hiển thị; số của phiếu thu/chi lưu riêng ở `so_chung_tu_phieu_thu_chi` (cột đã có sẵn, comment tại [V1__baseline.sql:16369](../../cell-app/src/main/resources/db/migration/V1__baseline.sql) nói rõ *"KHÔNG mượn so_chung_tu của chứng từ điều chỉnh"*). Nếu BA muốn lưới hiển thị số phiếu thu/chi khi Thanh toán ngay thì đó là **hiển thị**, FE chọn giữa hai field — không đổi cột định danh. Đưa vào §12-Q5 mở rộng nếu BA phản hồi khác.

### 3.2 Bộ tiêu chí tìm kiếm (SCR_DanhSach dòng 12-19)

| Field BA | Control | Alias BE | Toán tử |
|---|---|---|---|
| Từ khóa tìm kiếm | text | `keyword` | `like` trên `soChungTu`, `tenKhachHang` (khai `@Searchable(keyword = true)`) |
| Phương thức điều chỉnh | select | `huongDieuChinhGia` | `eq` / `in`; "Tất cả" ⇒ FE **không gửi** filter |
| Trạng thái ghi sổ | select | `status` | `in` — "Chưa ghi sổ" ⇒ `["NHAP","CHO_DUYET","DA_DUYET"]`, "Đã ghi sổ" ⇒ `["DA_GHI_SO"]` |
| Khách hàng | select | `khachHangId` | `eq` |
| Ngày từ / Ngày đến | date | `ngayHachToan` | `between` — SCR ghi rõ lọc theo **Ngày hạch toán** |

Ghép điều kiện: `AND`; `keyword` luôn `AND` với cả nhóm ([SearchRequest.java:30](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/request/SearchRequest.java)).

⚠ **Ánh xạ trạng thái 2 giá trị (BA) ↔ 5 giá trị (`TrangThaiChungTu`)**: BA chỉ biết "Chưa ghi sổ"/"Đã ghi sổ" (BR12), enum có 5. Cách trên đặt **ở FE** (FE đã làm — `helpers/trangThai.ts`, `IMPLEMENT.md` dòng 281). BE không dựng alias ảo `trangThaiGhiSo`: một alias suy diễn là một chỗ nữa để lệch, và `status` đã `@Searchable(sortable = true)` sẵn ở base ([BaseChungTuEntity.java:70](../../cell-app/src/main/java/vn/dopai/pmkt/cell/core/entity/BaseChungTuEntity.java)).

### 3.3 Field phụ trong DTO để FE ẩn/hiện nút (BR13.1, BR42.2)

| Nút | Điều kiện | Field DTO cần có |
|---|---|---|
| Xem chi tiết | luôn (có quyền `.View.Detail`) | `id` |
| Sửa · Xóa · Ghi sổ | `trangThaiChungTu != "DA_GHI_SO"` | `trangThaiChungTu` |
| Bỏ ghi sổ | `trangThaiChungTu == "DA_GHI_SO"` | `trangThaiChungTu` |
| Nhân bản | luôn (có quyền `.Clone`) | `id` |
| PUT/DELETE/ghi sổ (khoá lạc quan) | — | `updatedAt` — FE gửi lại làm lock token |

**Không** thêm field kiểu `coTheSua`/`coTheXoa` do BE tính: điều kiện là hàm thuần của trạng thái + quyền, mà quyền FE đã có từ token; thêm cờ là nhân đôi nguồn sự thật và FE vẫn phải kiểm quyền.

## 4. Lọc · sắp xếp · phân trang · dòng tổng

### 4.1 Bộ lọc mặc định
BE **không bơm** bộ lọc mặc định nào ngoài `da_xoa = false` (do `SoftDeletableEntity`) và RLS tenant/đơn vị (policy DB, [V1__baseline.sql:29662](../../cell-app/src/main/resources/db/migration/V1__baseline.sql)). Phễu ngày mặc định "đầu tháng → hiện tại" là **của FE** (BR8) — FE gửi tường minh. Lối thoát lấy toàn bộ: gửi `filters: []`.

### 4.2 Sắp xếp mặc định
`SCR_DanhSach` dòng 37: *"sắp xếp theo Ngày chứng từ (Mới nhất → Cũ nhất), Nếu cùng ngày chứng từ thì sắp xếp theo Số chứng từ giảm dần"*. UC_XemDanhSach lại ghi *"Sắp xếp theo: Ngày chứng từ (mới nhất lên đầu)"*, còn bộ lọc ngày thì theo **Ngày hạch toán** (dòng 18-19), và BR2 chung quy định ưu tiên **Ngày hạch toán giảm dần**.

→ **Chọn** `ngayHachToan desc, soChungTu desc` — theo BR2 (quy chuẩn chung) và khớp FE (`DEFAULT_SORT` ở `IMPLEMENT.md` dòng 276). Lệch chữ "Ngày chứng từ" của SCR: hai ngày này bằng nhau ở phần lớn chứng từ, và lọc/hiển thị đều dùng ngày hạch toán nên sắp theo cùng cột là nhất quán. **Cần BA xác nhận** — bổ sung vào §12 file gốc nếu BA phản đối.

Cài: `sort` do FE gửi; khi FE không gửi, `SortResolver` lấy mặc định của entity (`@Searchable` + `ListSort` mặc định khai trên entity).

### 4.3 Phân trang
1-based (`SearchRequest.pageOrDefault`), whitelist size `10/20/50/100/200`, giá trị lạ → 20. FE gửi `pageSize = 10` theo SCR BR1.

### 4.4 Dòng tổng cộng
- Cột: **`tongTienThanhToanQuyDoi`** — Figma chỉ vẽ một ô tổng dưới cột "Tổng tiền thanh toán (VNĐ)" (`model.ts` dòng 250-255).
- Phạm vi: **toàn bộ bản ghi sau lọc** (BR31), không phải trang hiện tại.
- Cài: `DieuChinhGiaHangBanRepositoryCustom.tongHop(Specification)` dùng Criteria `cb.sum(...)`, đúng mẫu [ChungTuBanHangRepositoryImpl.java:49](../../cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/internal/repository/ChungTuBanHangRepositoryImpl.java).
- Tập rỗng: `SUM` trả `NULL` ⇒ map về `BigDecimal.ZERO`, **không** trả `null` (FE sẽ hiện ô trống thay vì 0).

## 5. Luồng xử lý

1. `BaseCrudController.search` gọi `quyen.require("DieuChinhGiaHangBan", VIEW)`.
2. `AbstractCrudService.search` dựng `Specification` qua `DynamicSpecification` từ `SearchRequest` (whitelist `@Searchable`).
3. Repository trả `Page<DieuChinhGiaHangBan>`; RLS lọc tenant + phạm vi đơn vị ở tầng DB.
4. `DieuChinhGiaMapper` map sang DTO **không kèm** `chiTiet`.
5. Service gọi `tongHop(spec)` với **cùng** `Specification` → `TongHopDieuChinhGiaDto`.
6. Trả `PageResponse.of(page, pageNumber, summary)`.

Không có bước nào viết mới ở tầng controller/service ngoài (5).

## 6. Tương tranh & transaction
`@Transactional(readOnly = true)` — bắt buộc dù chỉ đọc: `TenantRlsAspect` bind GUC `app.tenant_id` theo transaction, thiếu nó RLS trả tập rỗng (javadoc [AbstractChungTuCrudService.java:82](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/AbstractChungTuCrudService.java)).

## 7. Kiểm thử

### Unit (`@Tag("unit")`)
| Lớp test | Kiểm gì |
|---|---|
| `DieuChinhGiaSearchableTest` | pin whitelist `@Searchable`: đúng 9 alias sort + 5 alias filter + 2 field keyword; thêm/bớt cột phải sửa test (hàng rào, không phải phiền hà) |
| `DieuChinhGiaMapperTest` | list-projection **không** kèm `chiTiet`; `huongDieuChinhGia` map từ `loai_dieu_chinh`; `trangThaiChungTu` trả tên hằng |
| `TongHopDieuChinhGiaTest` | `SUM` trên tập rỗng → `ZERO`, không `null` |

### Tích hợp (cần Docker — chạy ở CI)
| Lớp test | Kiểm gì |
|---|---|
| `DieuChinhGiaSearchIT` | phân trang 1-based; sort mặc định; `between` trên `ngayHachToan`; `keyword` trúng cả 2 cột; `summary` bằng tổng toàn tập chứ không phải tổng trang; RLS chặn tenant khác |

## 8. BR đã áp dụng
BR1 (§4.3) · BR2 (§4.2) · BR8 (§3.2) · BR11 (§3.2, §4) · BR12 (§3.3) · BR13.1 (§3.3) · BR25 (§2) · BR28 (§5 bước 3) · BR29 (§4.1) · BR31 (§4.4) · BR46 (`updatedAt` ở §3.3).
