# F6 — Ghi sổ Chứng từ điều chỉnh giá (đơn + hàng loạt)

| | |
|---|---|
| Mã chức năng | **F6** |
| UC nguồn | [PMKT-U-07669 — Ghi sổ](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/4.usecases/PMKT-U-07669_GhiSo/UC_GhiSo.md) |
| Màn hình nguồn | `SCR_DanhSachDieuChinhGia` (nút Ghi sổ) · `SCR_ThemMoiDieuChinhGia` mục "Hạch toán khi Lưu và ghi sổ" (dòng 528-559) |
| Endpoint phụ trách | **A7** `POST /{id}/ghi-so` · **A12** `POST /ghi-so-hang-loat` |
| Dùng chung | `DinhKhoanDieuChinhGia` — cũng là lớp dựng bút toán cho "Lưu và ghi sổ" ở [03](03-them-moi.md) |

## 1. Quyết định riêng

- **Phạm vi ghi sổ = bút toán sổ cái + trạng thái** (quyết định **D3** ở file gốc). Năm tác động còn lại mà UC liệt kê (phiếu thu/chi, HĐĐT, sổ thuế, tồn quỹ) không có module BE để gọi — §1.2 và §12-Q2 file gốc. **Sổ cái vẫn đúng** vì bút toán 2 (vế tiền) sinh đủ từ `tai_khoan_tien_id`.
- **Bút toán 2 (vế tiền) phân bổ theo từng dòng chi tiết**, không dồn thành một định khoản header. Lý do kỹ thuật: `DinhKhoan.chiTietChungTuId` là cột **NOT NULL** của `acc_so_cai` và nằm trong khoá chống ghi trùng ([DinhKhoan.java javadoc](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/hach_toan/api/dto/DinhKhoan.java)) — một định khoản header không có dòng để gắn. Lý do nghiệp vụ: BR36 cấm gộp dòng bút toán. **Không chọn** gắn tất cả vào dòng đầu tiên: sổ chi tiết công nợ theo mặt hàng sẽ lệch.
- **Kiểm kỳ kế toán KHÔNG gọi ở module** — `GhiSoApi.ghiSo` tự kiểm với đúng cặp `(ngayHachToan, maLoaiChungTu)` nó sắp INSERT ([ChungTuTemplate javadoc](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)). Gọi thêm là thừa một truy vấn và tạo an toàn giả.

## 2. Hợp đồng API

### A7 — `POST /{id}/ghi-so` · quyền `DieuChinhGiaHangBan.Post`

Không có body (base khai `@PostMapping("/{id}/ghi-so")`, [BaseChungTuController.java:93](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/controller/BaseChungTuController.java)).

```jsonc
// Response 200
{ "code": "SUCCESS", "message": "Ghi sổ chứng từ điều chỉnh giá thành công",
  "messageId": "MSG_PMKT-E-07664_004", "data": { /* DTO đã cập nhật trạng thái */ } }
```

| Điều kiện | HTTP | Mã | messageId |
|---|---|---|---|
| Thiếu quyền `.Post` | 403 | — | `_007` |
| `id` không tồn tại | 404 | — | — |
| Chứng từ **đã ghi sổ** | 400 | `DA_GHI_SO` | `_201` |
| Trùng số chứng từ với chứng từ khác | 400 | `TRUNG_SO_CHUNG_TU` | `_109` |
| Kỳ kế toán đã khoá | 400 | `KY_KE_TOAN_DONG` | `_203` (kernel ném `PeriodLockedException`) |
| Ghi sổ lại đúng nội dung cũ | **200** | — | idempotent, `KetQuaGhiSo.laLapLai() = true` |
| Ghi sổ lại với nội dung KHÁC | 409 | `POSTING_PAYLOAD_MISMATCH` | — (kernel) |
| Chứng từ không sinh dòng bút toán nào (tổng = 0) | 200 | — | base chỉ `log.info`, vẫn kiểm kỳ |

### A12 — `POST /ghi-so-hang-loat` · quyền `.Post`

Body/response giống [05 §2 A14](05-xoa.md) (`XuLyHangLoatRequest` → `KetQuaHangLoatDto`), messageId `MSG_PMKT-E-07664_004`. BR45: mỗi chứng từ một transaction; chứng từ đã ghi sổ bị bỏ qua có báo cáo.

## 3. Validation

| # | Luật | Thời điểm | Thông báo | Mã | Nguồn |
|---|---|---|---|---|---|
| G1 | Chứng từ tồn tại, đúng tenant | `chuanBiChungTu` | — | 404 | BR28 |
| G2 | Chứng từ **chưa ghi sổ** | `kiemTraNghiepVu` | Chứng từ đã ghi sổ | `_201` | BR12 "Ghi sổ duy nhất" |
| G3 | **Số chứng từ không trùng** chứng từ khác (kiểm lại trước khi ghi sổ) | `kiemTraNghiepVu` | Số chứng từ đã tồn tại, vui lòng nhập số khác | `_109` | UC_GhiSo bước 4 + mục "Kiểm tra trùng số chứng từ" |
| G4 | Kỳ kế toán đang mở | **kernel** `GhiSoApi.ghiSo` | Ngày hạch toán không thuộc kỳ kế toán đang mở | `_203` | BR17.1 |
| G5 | Mỗi dòng đủ tài khoản để dựng bút toán (công nợ + doanh thu/giảm giá + thuế; chiết khấu nếu có tiền CK) | `sauKhiLuu` khi dựng định khoản | *(chưa có mã)* `MSG_COMMON_001` | — | BR7/BR8 của SCR |
| G6 | Tổng Nợ = Tổng Có | **kernel** + trigger DB cân đối | — | 400 | BR36 |

⚠ G3 dùng lại `MSG_109`. UC_GhiSo viết câu khác — *"Số chứng từ {SoChungTu} đã tồn tại. Vui lòng kiểm tra lại trước khi ghi sổ."* — nhưng `6.messages.md` không cấp mã cho câu đó (§12-Q5 file gốc).

## 4. Bút toán — bốn kịch bản

Nguồn: UC_GhiSo mục "Bút toán hạch toán" + SCR dòng 528-559. Dựng ở `DinhKhoanDieuChinhGia`, gọi trong hook `sauKhiLuu` (id dòng chi tiết chỉ có sau bước lưu).

Ký hiệu theo dòng chi tiết `d`: `TT` = `thanhTien`, `CK` = `chietKhauTien`, `T` = `tienThueGtgt`, `TTT` = `TT − CK + T` (tổng thanh toán của dòng).

### TH1 — Tăng giá + Điều chỉnh công nợ

| # | Nợ | Có | Số tiền | Điều kiện |
|---|---|---|---|---|
| 1 | `taiKhoanCongNoId` | `taiKhoanDoanhThuId` | `TT` | luôn |
| 2 | `taiKhoanCongNoId` | `taiKhoanThueGtgtId` | `T` | `T > 0` |
| 3 | `taiKhoanChietKhauId` | `taiKhoanCongNoId` | `CK` | `CK > 0` |

Net vế 131 = `TT + T − CK` = `TTT` ✔

### TH2 — Tăng giá + Thanh toán ngay

Bút toán 1: **giống TH1** (3 định khoản trên).
Bút toán 2 — kết chuyển thu tiền, **sinh trên từng dòng**:

| # | Nợ | Có | Số tiền |
|---|---|---|---|
| 4 | `header.taiKhoanTienId` (tab Phiếu thu ⇒ 111x; tab Giấy báo Có ⇒ 112x) | `taiKhoanCongNoId` | `TTT` |

### TH3 — Giảm giá + Điều chỉnh công nợ

| # | Nợ | Có | Số tiền | Điều kiện |
|---|---|---|---|---|
| 1 | `taiKhoanGiamGiaId` (5213 hoặc 511) | `taiKhoanCongNoId` | `TT` | luôn |
| 2 | `taiKhoanThueGtgtId` (3331) | `taiKhoanCongNoId` | `T` | `T > 0` |
| 3 | `taiKhoanCongNoId` | `taiKhoanChietKhauId` | `CK` | `CK > 0` |

### TH4 — Giảm giá + Thanh toán ngay

Bút toán 1: **giống TH3**.
Bút toán 2 — kết chuyển chi tiền, trên từng dòng:

| # | Nợ | Có | Số tiền |
|---|---|---|---|
| 4 | `taiKhoanCongNoId` | `header.taiKhoanTienId` (Phiếu chi/Séc TM ⇒ 111x; Séc CK/UNC ⇒ 112x) | `TTT` |

### Quy tắc chung cho mọi định khoản

- **Không gộp** (BR36): mỗi cặp tài khoản là một `DinhKhoan` riêng; kernel tự tách thành 2 dòng `acc_so_cai` (vế Nợ + vế Có).
- `\.voiChiTiet(chiTietId)` — **bắt buộc**, cột NOT NULL.
- `\.voiDoiTuong(khachHangId)` cho mọi định khoản có chạm tài khoản công nợ — sổ chi tiết công nợ theo khách hàng cần nó.
- Ngoại tệ (BR18): `soTien` = **số đã quy đổi** sang tiền hạch toán, kèm `\.voiNgoaiTe(loaiTienId, tyGia, soTienNguyenTe)`. Sổ cái luôn ghi bằng tiền hạch toán, phần nguyên tệ đi kèm.
- `dienGiai` từng dòng: `"<Tăng|Giảm> giá hàng bán — <tenHang>"`; `dienGiaiChung(ctx)` = `mo_ta` của header.
- Định khoản có `soTien = 0` **bị bỏ**, không đẩy xuống kernel (kernel đòi `soTien > 0`).

> ⚠ **Mâu thuẫn tài liệu — cần BA xác nhận (bổ sung §12 file gốc):** SCR dòng 534 ghi *"Nợ [TK Công nợ] / Có [TK Doanh thu]: **Tổng tiền thanh toán tăng thêm**"*, trong khi UC_GhiSo cùng bút toán ghi *"Nợ [TK Công nợ] (131): Tổng tiền thanh toán tăng thêm — Có [TK Doanh thu] (511): **Giá trị hàng hóa tăng thêm** — Có [TK Thuế GTGT] (3331): Tiền thuế tăng thêm"*. Nếu lấy theo SCR thì vế Có 511 nhận cả phần thuế và tổng Nợ/Có lệch. **Chọn theo UC** (511 nhận `thanhTien`, 3331 nhận `tienThueGtgt`) vì đó là bút toán cân đối; SCR dòng 534 là lỗi diễn đạt.

## 5. Luồng xử lý

`ChungTuTemplate` luồng GHI_SO ([:212](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)):

```
doiHoiDinhDanh → khoaChungTu → kiemTraNghiepVu (G2, G3)
  → luuChungTu (truocKhiLuu: status = DA_GHI_SO, nguoiGhiSo, thoiGianGhiSo)
  → sauKhiLuu (DinhKhoanDieuChinhGia → ctx.dinhKhoan)
  → phanGhiSo → GhiSoApi.ghiSo(GhiSoRequest{chungTuId, soChungTu, ngayChungTu,
                               ngayHachToan, "CTDG", dienGiai, chiNhanhId, dinhKhoan})
  → ghiNhatKyTacDong → dangKyThongBaoSauCommit
```

```mermaid
flowchart LR
  A[POST /{id}/ghi-so] --> B[khoá chứng từ<br/>ChungTuKhoaApi]
  B --> C{chưa ghi sổ?}
  C -- không --> E1[400 _201]
  C -- có --> D{số chứng từ trùng?}
  D -- có --> E2[400 _109]
  D -- không --> F[status = DA_GHI_SO<br/>nguoiGhiSo · thoiGianGhiSo]
  F --> G[dựng định khoản theo 4 kịch bản]
  G --> H[GhiSoApi.ghiSo]
  H -- kỳ khoá --> E3[400 _203 · rollback toàn bộ]
  H -- ok --> I[acc_so_cai: 2 dòng / định khoản]
  I --> J[aud_audit_log · trong transaction]
```

**Nguyên tử:** cả luồng nằm trong một `@Transactional`; `GhiSoApi` chạy `Propagation.MANDATORY` (không tự mở transaction riêng) nên bút toán và chứng từ cùng sống cùng chết — đúng "Ràng buộc nguyên tử" của UC trong phạm vi D3.

## 6. Tương tranh & idempotency

| Cơ chế | Chống gì |
|---|---|
| `khoaChungTu` ngay đầu luồng | hai người cùng bấm Ghi sổ — người sau đợi người trước commit |
| G2 (`status`) | ghi sổ hai lần (BR12 "Ghi sổ duy nhất") |
| Kernel idempotent theo nội dung | retry mạng / redelivery: gọi lại đúng nội dung ⇒ không sinh dòng mới, `laLapLai() = true` |
| Kernel `POSTING_PAYLOAD_MISMATCH` (409) | gọi lại với nội dung khác ⇒ chặn, buộc bỏ ghi sổ trước |
| Trigger cân đối Nợ/Có ở DB | bút toán lệch lọt qua tầng Java |

## 7. Kiểm thử

### Unit (`@Tag("unit")`)
| Lớp test | Kiểm gì |
|---|---|
| `DinhKhoanDieuChinhGiaTest` | **4 kịch bản × (có/không chiết khấu) × (có/không thuế)** = 16 ca: đúng cặp TK, đúng số tiền, đúng số lượng định khoản · Σ Nợ = Σ Có ở mọi ca · định khoản `soTien = 0` bị loại · mọi định khoản có `chiTietChungTuId` · định khoản chạm 131 có `doiTuongId = khachHangId` · ngoại tệ: `soTien` là số quy đổi, `soTienNguyenTe` là số gốc |
| `GhiSoDieuChinhGiaTest` | G2 chặn `DA_GHI_SO` (`_201`); G3 chặn trùng số (`_109`); `truocKhiLuu` set `nguoiGhiSo`/`thoiGianGhiSo`; `maLoaiChungTu = "CTDG"` |
| `PhanBoButToanTienTest` | bút toán 2 sinh trên **từng dòng**, Σ = tổng thanh toán của chứng từ; hướng Nợ/Có đảo đúng giữa TH2 và TH4 |

### Tích hợp (cần Docker)
| Lớp test | Kiểm gì |
|---|---|
| `GhiSoDieuChinhGiaIT` | đủ dòng `acc_so_cai` (= 2 × số định khoản) · ghi sổ lần 2 cùng nội dung ⇒ không sinh thêm dòng · kỳ khoá ⇒ 400 `_203` và **không** dòng nào được ghi, `status` giữ `NHAP` · trigger cân đối không nổ |
| `GhiSoHangLoatIT` | lô hỗn hợp: thành công/thất bại đếm đúng, chứng từ lỗi không để lại dòng sổ cái |

## 8. BR đã áp dụng
BR12 (G2, ghi sổ duy nhất) · BR13.1/BR42.2 (nút Ghi sổ chỉ hiện khi chưa ghi sổ — FE) · BR16 (`MSG_COMMON_001` cho G5) · BR17.1 (G4, kernel) · BR18 (§4 ngoại tệ) · BR19 (G3) · BR25 (`.Post`) · BR36 (không gộp bút toán) · BR45 (A12) · BR46 (`nguoi_ghi_so`, `thoi_gian_ghi_so`).

**BR chưa đạt ở chức năng này:** phần "cập nhật sổ thuế đầu ra", "cập nhật tồn quỹ", "tạo HĐĐT" của UC_GhiSo — D3/§12-Q2.
