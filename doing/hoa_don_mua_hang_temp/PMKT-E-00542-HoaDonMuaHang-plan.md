> **Trạng thái:** BẢN NHÁP CHỜ REVIEW
> **Ngày cập nhật:** 2026-08-07
> **Người review cần có:** 1 BA + 1 Dev BE

| Mục | Nội dung |
|---|---|
| Use case | PMKT-E-00542 — Hóa đơn mua hàng |
| Màn hình | SCR_HDMH_DanhSach, SCR_HDMH_ThemMoi, SCR_HDMH_ChinhSua, SCR_HDMH_PopupChonChungTu, SCR_HDMH_XemChiTiet, vv. |
| Tài liệu nguồn | pmkt-docs/ba/PMKT-E-00542-HoaDonMuaHang/ |
| Module BE | cell-app/src/main/java/vn/vtt/pmkt/cell/mua_hang/hoa_don_mua/ |
| Bảng DB | ENT_HoaDonMua, ENT_ChiTietHoaDon, ENT_ChungTuNhanHoaDon, ENT_ChiTietChungTuMuaHang |

---

## 0. Các quyết định đã chốt

| # | Quyết định | Hệ quả |
|---|---|---|
| **D1** | Kế thừa `BaseChungTuController` | Các thao tác như Ghi sổ, Bỏ ghi sổ, Nhân bản, Thao tác hàng loạt sẽ được expose theo chuẩn `BaseChungTuController`. |
| **D2** | Hóa đơn mua hàng (ENT_HoaDonMua) thuộc loại chứng từ có Master-Detail | Kế thừa `AbstractChungTuCrudService` để tái sử dụng chuẩn hóa chung cho Chứng Từ. Tách các xử lý chuyên sâu vào `HoaDonMuaService`. |
| **D3** | Luồng lưu và ghi sổ (PMKT-U-01162) yêu cầu ghi sổ CT gốc (`ChungTuMuaHang`) và hóa đơn | Xử lý giao dịch tập trung (transaction) cẩn thận để rollback toàn bộ khi thất bại. |
| **D4** | Tách chi tiết file thiết kế | Thiết kế luồng xử lý riêng cho từng UC ra các file markdown con. |

---

## 1. Phạm vi

### 1.1 Trong phạm vi

| # | Chức năng | Nguồn |
|---|---|---|
| F1 | Xem danh sách hóa đơn mua hàng | PMKT-U-01161 |
| F2 | Thêm mới hóa đơn mua hàng | PMKT-U-01162 |
| F3 | Chỉnh sửa hóa đơn mua hàng | PMKT-U-01163 |
| F4 | Xóa hóa đơn mua hàng (Xóa mềm) | PMKT-U-01164 |
| F5 | Xem chi tiết hóa đơn mua hàng | PMKT-U-01165 |
| F6 | Ghi sổ / Bỏ ghi sổ hóa đơn mua hàng | PMKT-U-01166 |

### 1.2 NGOÀI phạm vi (không cài lần này)

Không có chức năng nào nằm ngoài phạm vi trong luồng hiện tại.

---

## 2. Hiện trạng đã khảo sát

### 2.1 Code hiện có

Dự án Greenfield cho Module Hóa đơn mua hàng. Base code đã có sẵn ở module `accounting_core` và `core`.

### 2.2 Hiện trạng DB

Các bảng cần có: `ENT_HoaDonMua`, `ENT_ChiTietHoaDon`, `ENT_ChungTuNhanHoaDon`.
File migration sẽ là `V...__init_hoa_don_mua.sql`

| Bảng phụ | Vai trò | Cột khoá nối |
|---|---|---|
| ENT_ChungTuNhanHoaDon | Bảng Master chứng từ kế toán đợt nhận HĐ | Id |
| ENT_ChiTietHoaDon | Chi tiết hàng & Thuế | HoaDonMuaId |
| ENT_ChiTietChungTuMuaHang | Dòng hàng gốc (Cần set cờ `DaNhanHoaDon = true`) | ChungTuMuaHangId |

### 2.3 Hạ tầng base đã có sẵn những gì

| Cần | Đã có ở base | Vị trí |
|---|---|---|
| API Chứng từ Base | BaseChungTuController | `../../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/controller/BaseChungTuController.java` |
| Service Chứng từ Base | AbstractChungTuCrudService | `../../../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/AbstractChungTuCrudService.java` |

---

## 3. Kiến trúc

### 3.1 Phân tầng

```
HoaDonMuaController  extends BaseChungTuController<...>
        ▼
HoaDonMuaService     extends AbstractChungTuCrudService<...>
        │
        ▼
HoaDonMuaRepository  extends BaseRepository<...>
        ▼
HoaDonMuaEntity      extends BaseChungTuEntity  →  @Table("ENT_HoaDonMua")
```

### 3.2 Lựa chọn kiến trúc + lý do

| | Phương án A (Viết lại API riêng cho HDMH) | **Phương án B (Kế thừa base chứng từ kế toán)** |
|---|---|---|
| Thiết kế | Custom hóa cao, không tái sử dụng | Chuẩn hóa, tự động xử lý chung CRUD, Ghi sổ, RLS |
| Rủi ro | Mất nhiều thời gian | Cần tuân thủ chặt chẽ chữ ký lớp base |

=> Chọn phương án B.

### 3.3 Cấu trúc thư mục

```
mua_hang/
└── hoa_don_mua/
    ├── package-info.java
    └── internal/
        ├── controller/HoaDonMuaController.java
        ├── dto/ HoaDonMuaDto.java, HoaDonMuaCommand.java, ...
        ├── entity/ HoaDonMua.java, ChiTietHoaDon.java, ...
        ├── repository/ HoaDonMuaRepository.java, ChiTietHoaDonRepository.java, ...
        └── service/ HoaDonMuaService.java, ...
```

---

## 4. Hợp đồng API

Base path: **`/api/mua-hang/hoa-don-mua`**. Mã chức năng: **`NhanHoaDon`**.

| # | Nguồn | Method | Path | Quyền | Trả về | Mục con |
|---|---|---|---|---|---|---|
| A1 | `base` | `POST` | `/search` | `.View` | `PageResponse<…>` | [XemDanhSach](PMKT-E-00542-HoaDonMuaHang-plan-danhsach.md) |
| A2 | `base` | `GET` | `/{id}` | `.View.Detail` | `HoaDonMuaDto` | [XemChiTiet](PMKT-E-00542-HoaDonMuaHang-plan-xemchitiet.md) |
| A3 | `base` | `POST` | `/` | `.Create` | `HoaDonMuaDto` | [ThemMoi](PMKT-E-00542-HoaDonMuaHang-plan-themmoi.md) |
| A4 | `base` | `PUT` | `/{id}` | `.Edit` | `HoaDonMuaDto` | [ChinhSua](PMKT-E-00542-HoaDonMuaHang-plan-chinhsua.md) |
| A5 | `base` | `DELETE` | `/{id}` | `.Delete` | `Void` | [Xoa](PMKT-E-00542-HoaDonMuaHang-plan-xoa.md) |
| A6 | `base` | `POST` | `/{id}/ghi-so` | `.Post` | `HoaDonMuaDto` | [GhiSo](PMKT-E-00542-HoaDonMuaHang-plan-ghiso.md) |
| A7 | `base` | `POST` | `/{id}/bo-ghi-so` | `.Unpost` | `HoaDonMuaDto` | [GhiSo](PMKT-E-00542-HoaDonMuaHang-plan-ghiso.md) |

---

## 5. Danh sách tài liệu con (Chi tiết xử lý từng Use Case)

1. [Danh Sách (PMKT-U-01161)](PMKT-E-00542-HoaDonMuaHang-plan-danhsach.md)
2. [Thêm Mới (PMKT-U-01162)](PMKT-E-00542-HoaDonMuaHang-plan-themmoi.md)
3. [Chỉnh Sửa (PMKT-U-01163)](PMKT-E-00542-HoaDonMuaHang-plan-chinhsua.md)
4. [Xóa (PMKT-U-01164)](PMKT-E-00542-HoaDonMuaHang-plan-xoa.md)
5. [Xem Chi Tiết (PMKT-U-01165)](PMKT-E-00542-HoaDonMuaHang-plan-xemchitiet.md)
6. [Ghi Sổ / Bỏ Ghi Sổ (PMKT-U-01166)](PMKT-E-00542-HoaDonMuaHang-plan-ghiso.md)
