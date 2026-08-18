# PMKT-E-00542 — Kế hoạch tổng thể API Hóa đơn mua hàng (Nhận hóa đơn)

> **Trạng thái:** BẢN NHÁP CHỜ BA/DEV BE REVIEW  
> **Ngày khảo sát:** 2026-08-07  
> **Phạm vi:** toàn bộ `PMKT-E-00542-HoaDonMuaHang`  
> **Module đích:** `cell-app/src/main/java/vn/dopai/pmkt/cell/nhan_hoa_don` (greenfield - tạo package mới độc lập)

---

## 1. Mục tiêu và bộ tài liệu con

Kế hoạch triển khai hoàn chỉnh các API cho phân hệ "Nhận hóa đơn mua hàng" theo đúng kiến trúc tiêu chuẩn `Controller → Service → Repository → Entity` của Dự án, kế thừa luồng đọc/tìm kiếm động từ `core` và luồng vòng đời chứng từ kế toán từ `accounting_core`.

Chi tiết thiết kế và luồng xử lý cụ thể cho từng chức năng được tách thành các tài liệu con sau:

| Mã | Chức năng | Tài liệu |
|---|---|---|
| F01 | Xem danh sách hóa đơn mua hàng (PMKT-U-01161) | [01-xem-danh-sach.md](01-xem-danh-sach.md) |
| F02 | Thêm mới hóa đơn mua hàng (PMKT-U-01162) | [02-them-moi.md](02-them-moi.md) |
| F03 | Chỉnh sửa hóa đơn mua hàng (PMKT-U-01163) | [03-chinh-sua.md](03-chinh-sua.md) |
| F04 | Xóa hóa đơn mua hàng (PMKT-U-01164) | [04-xoa.md](04-xoa.md) |
| F05 | Xem chi tiết hóa đơn mua hàng (PMKT-U-01165) | [05-xem-chi-tiet.md](05-xem-chi-tiet.md) |
| F06 | Ghi sổ hóa đơn mua hàng (PMKT-U-01166) | [06-ghi-so.md](06-ghi-so.md) |
| F07 | Bỏ ghi sổ hóa đơn mua hàng (PMKT-U-01167) | [07-bo-ghi-so.md](07-bo-ghi-so.md) |

---

## 2. Kết luận khảo sát hiện trạng

### 2.1 Hiện trạng Code và DB
- **Hiện trạng Code:** Greenfield đối với nghiệp vụ Nhận hóa đơn mua hàng độc lập (chưa có code java tương ứng cho Controller, Service, Repository, Mapper). Tuy nhiên, code base `accounting_core` đã hỗ trợ sẵn khung `ChungTuTemplate` và `BaseChungTuController` để kế thừa trực tiếp.
- **Hiện trạng DB:**
  - Bảng DB đã được định nghĩa tại migration `V61__pur_hoa_don_mua_hang_schema.sql` gồm:
    1. `pur_chung_tu_nhan_hoa_don` (Master - chứng từ nhận hóa đơn)
    2. `pur_hoa_don_mua` (Thông tin hóa đơn nhà cung cấp)
    3. `pur_chi_tiet_hoa_don` (Detail - chi tiết dòng hàng hóa/dịch vụ của hóa đơn)
  - Cấu trúc cột header đã được chuẩn hóa tại `V345__chung_tu_chuan_cot_sal_pur.sql` (thêm `status`, `da_xoa`, `chi_nhanh_id`, `phien_ban`...) và `V351__chung_tu_tra_ten_cot_thoi_gian_ve_ngay.sql`.

### 2.2 Các mối ràng buộc chính giữa các bảng

| Bảng nguồn | Bảng đích | Khóa ngoại / Liên kết | Vai trò |
|---|---|---|---|
| `pur_hoa_don_mua` | `pur_chung_tu_nhan_hoa_don` | `chung_tu_nhan_hoa_don_id` | Liên kết 1-1 giữa thông tin HĐ và chứng từ kế toán |
| `pur_chi_tiet_hoa_don` | `pur_hoa_don_mua` | `hoa_don_mua_id` | Liên kết 1-N dòng chi tiết với HĐ |
| `pur_chi_tiet_hoa_don` | `pur_chung_tu_mua_hang` | `chung_tu_mua_hang_id` | XFK để liên kết ngược về chứng từ mua hàng gốc |
| `pur_chi_tiet_hoa_don` | `pur_chi_tiet_chung_tu_mua_hang` | `chi_tiet_chung_tu_mua_hang_id` | XFK dòng chi tiết gốc để cập nhật trạng thái nhận HĐ |

---

## 3. Kiến trúc bắt buộc của BE

Kiến trúc thực hiện tuân thủ tuyệt đối khung kiến trúc phân tầng của BE:

```text
NhanHoaDonController (kế thừa BaseChungTuController)
  ▼
NhanHoaDonCrudService (kế thừa AbstractChungTuCrudService)
  ├─ Phần Đọc: Kế thừa BaseCrudController → AbstractCrudService / SearchExecutor
  └─ Phần Ghi (Vòng đời chứng từ): Tự xây dựng thông qua ChungTuTemplate
         ├─ LuuNhanHoaDonTemplate (cho TAO / SUA / XOA)
         ├─ GhiSoNhanHoaDonTemplate (cho GHI_SO)
         └─ BoGhiSoNhanHoaDonTemplate (cho BO_GHI_SO)
```

### Nguyên tắc triển khai:
1. **Tái sử dụng hạ tầng `core` và `accounting_core`**: Không tự viết lại các cơ chế search động (`DynamicSpecification`), phân trang, kiểm tra quyền (`QuyenChecker`), multi-tenant RLS, audit log (`NhatKyKiemToan`), khóa chứng từ (`ChungTuKhoaApi`), và sinh số chứng từ (`SoChungTuApi`).
2. **Controller không gọi Repository**: Mọi thao tác đi qua Service, Service giao tiếp với Repository.
3. **Quản lý Transaction**: Thao tác thêm/sửa/xóa và ghi/bỏ ghi sổ phải đảm bảo tính nguyên tử (atomic). Ví dụ: việc cập nhật trạng thái nhận hóa đơn của chứng từ mua hàng gốc (`ChiTietChungTuMuaHang.DaNhanHoaDon`) và việc lưu Hóa đơn phải nằm chung một transaction, lỗi bất kỳ bước nào sẽ rollback toàn bộ.
4. **Cách ly Module**: Không import các package `internal` của module khác (như `chung_tu_mua_hang.internal`). Giao tiếp chéo qua các API/Service/Port công khai.

---

## 4. Danh mục API mục tiêu

Base path: `/api/mua-hang/nhan-hoa-don`; mã quyền: `NhanHoaDon`.

| API | Method | Quyền | Mô tả | Nguồn |
|---|---|---|---|---|
| `POST /search` | `POST` | `NhanHoaDon.View` | Lấy danh sách hóa đơn kèm bộ lọc động, phân trang, và dòng tổng cộng | Kế thừa core base |
| `GET /cot` | `GET` | `NhanHoaDon.View` | Lấy danh sách cột định nghĩa cho FE hiển thị | Kế thừa core base |
| `POST /export` | `POST` | `NhanHoaDon.Export` | Xuất dữ liệu excel theo bộ lọc | Kế thừa core base |
| `GET /{id}` | `GET` | `NhanHoaDon.View.Detail` | Xem chi tiết thông tin hóa đơn (header + dòng hàng) | Kế thừa core base |
| `GET /{id}/dong-chi-tiet` | `GET` | `NhanHoaDon.View.Detail` | Lấy danh sách dòng chi tiết theo thứ tự hiển thị | Kế thừa accounting base |
| `GET /{id}/thong-tin-hach-toan` | `GET` | `NhanHoaDon.View.Detail` | Lấy danh sách bút toán sổ cái thực tế đã ghi | Kế thừa accounting base |
| `POST /` | `POST` | `NhanHoaDon.Create` | Thêm mới hóa đơn (nháp hoặc ghi sổ ngay) | Tự cài đặt |
| `PUT /{id}` | `PUT` | `NhanHoaDon.Edit` | Chỉnh sửa hóa đơn chưa ghi sổ | Tự cài đặt |
| `DELETE /{id}` | `DELETE` | `NhanHoaDon.Delete` | Xóa mềm hóa đơn chưa ghi sổ | Tự cài đặt |
| `POST /{id}/ghi-so` | `POST` | `NhanHoaDon.Post` | Ghi sổ hóa đơn đơn lẻ | Kế thừa accounting base |
| `POST /{id}/bo-ghi-so` | `POST` | `NhanHoaDon.Unpost` | Bỏ ghi sổ hóa đơn đơn lẻ | Kế thừa accounting base |
| `POST /ghi-so-hang-loat` | `POST` | `NhanHoaDon.Post` | Ghi sổ hàng loạt (hỗ trợ trả kết quả từng phần) | Kế thừa accounting base |
| `POST /bo-ghi-so-hang-loat` | `POST` | `NhanHoaDon.Unpost` | Bỏ ghi sổ hàng loạt | Kế thừa accounting base |
| `POST /xoa-hang-loat` | `POST` | `NhanHoaDon.Delete` | Xóa mềm hàng loạt | Kế thừa accounting base |
| `GET /{id}/nhan-ban` | `GET` | `NhanHoaDon.Clone` | Trả về bản nháp nhân bản của hóa đơn, không lưu DB | Kế thừa accounting base |
| `POST /lay-chung-tu-goc` | `POST` | `NhanHoaDon.Create` | Popup lấy danh sách chứng từ mua hàng chưa có hóa đơn | Tự cài đặt |

---

## 5. Kế hoạch và Thứ tự triển khai

Số hiệu migration tiếp theo dự kiến là **`V355`** (với giả định V353 và V354 đã được các epic khác giữ chỗ trước).

| PR | Nội dung | Phụ thuộc | Điều kiện nghiệm thu (DoD) |
|---|---|---|---|
| **PR-1** | **Database Migration & Seed quyền**: Tạo file `V355__seed_quyen_nhan_hoa_don.sql` để seed đầy đủ các quyền `NhanHoaDon.View`, `NhanHoaDon.Create`, `NhanHoaDon.Edit`, `NhanHoaDon.Delete`, `NhanHoaDon.Post`, `NhanHoaDon.Unpost`, `NhanHoaDon.Export`, `NhanHoaDon.Clone`. | Không | Chạy `flyway` thành công, kiểm tra bảng `iam_quyen` có đủ quyền mới. |
| **PR-2** | **Entities & Repositories**: Định nghĩa các Entity Java `ChungTuNhanHoaDon`, `HoaDonMua`, `ChiTietHoaDon` kế thừa từ base classes; viết Repositories tương ứng. | PR-1 | Khởi động Spring Boot thành công, các truy vấn Hibernate không lỗi map cột. |
| **PR-3** | **DTOs, Mappers & API Xem danh sách/Chi tiết**: Tạo các class DTO (List, Detail), Mapper. Cài đặt các API `POST /search`, `GET /{id}`, `GET /{id}/dong-chi-tiet`. | PR-2 | Query test xanh, phân trang, default sort (`ngayHachToan DESC, ngayChungTu DESC, soChungTu ASC`) và tính summary đúng. |
| **PR-4** | **API Thêm mới & Chỉnh sửa**: Thực hiện `ChungTuTemplate` cho nghiệp vụ TAO, SUA. Tích hợp popup chọn chứng từ mua hàng gốc. | PR-3 | Test logic validate Loại tiền/Tỷ giá, logic set cờ `DaNhanHoaDon` trên dòng chứng từ mua hàng gốc. |
| **PR-5** | **API Xóa mềm**: Cài đặt nghiệp vụ XOA trong template, reset cờ `DaNhanHoaDon = false` khi xóa. | PR-4 | Xóa mềm đặt `da_xoa = true` trên DB, dữ liệu gốc được khôi phục trạng thái. |
| **PR-6** | **Ghi sổ & Bỏ ghi sổ**: Cài đặt GHI_SO (sinh bút toán `Nợ 133 / Có 331`, tự động chuyển chứng từ gốc sang "Đã ghi sổ" nếu "Lưu và ghi sổ") và BO_GHI_SO (xóa bút toán, không ghi đảo). | PR-5 | Kiểm thử tích hợp với kernel sổ cái, sổ công nợ NCC và sổ thuế. Rollback toàn bộ transaction khi có lỗi. |
| **PR-7** | **Thao tác hàng loạt & Kiểm thử tích hợp**: Tích hợp các API hàng loạt (ghi sổ, bỏ ghi sổ, xóa) và Postman tests. | PR-6 | Toàn bộ unit tests và integration tests xanh. Postman chạy không lỗi. |

---

## 6. Các điểm BA/Kiến trúc cần xác nhận trước khi code

| # | Câu hỏi | Đề xuất xử lý tạm thời để code tiếp |
|---|---|---|
| **Q1** | Khi chọn "Lưu và ghi sổ" (hoặc Ghi sổ sau đó), hệ thống tự động ghi sổ chứng từ mua hàng gốc qua `UC_CTMH_GhiSo`. Nếu chứng từ gốc bị lỗi khóa sổ hoặc lỗi dữ liệu con, việc nhận hóa đơn có bị rollback toàn bộ? | **Bắt buộc rollback trọn gói.** Để đảm bảo tính nhất quán dữ liệu, nếu một chứng từ gốc không thể ghi sổ, toàn bộ giao dịch nhận hóa đơn sẽ bị rollback và báo lỗi chi tiết của chứng từ gốc đó. |
| **Q2** | Với Hóa đơn kèm chứng từ (`LaHDVeSau = false`), nút Xem chi tiết trên danh sách điều hướng sang Chứng từ mua hàng gốc. API `GET /nhan-hoa-don/{id}` có cần trả về thông tin của CTMH gốc không? | **Có.** Endpoint detail sẽ trả về DTO có cờ `laHDVeSau` và `chungTuMuaHangId` để FE chủ động điều hướng sang màn hình xem chi tiết của Chứng từ mua hàng tương ứng. |
| **Q3** | Bỏ ghi sổ Hóa đơn về sau (`LaHDVeSau = true`) có tự động bỏ ghi sổ chứng từ mua hàng gốc không? | **Không.** Theo BR5/BR6 và usecase `UC_HDMH_GhiSo`, việc bỏ ghi sổ hóa đơn về sau chỉ xóa bút toán thuế Nợ 133 / Có 331 và đưa hóa đơn về "Chưa ghi sổ", chứng từ mua hàng gốc vẫn giữ nguyên trạng thái "Đã ghi sổ" và bút toán tạm tính. |
