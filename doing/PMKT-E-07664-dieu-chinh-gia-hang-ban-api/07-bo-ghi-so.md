# F7 — Bỏ ghi sổ Chứng từ điều chỉnh giá (đơn + hàng loạt)

| | |
|---|---|
| Mã chức năng | **F7** |
| UC nguồn | [PMKT-U-07670 — Bỏ ghi sổ](../../pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan/4.usecases/PMKT-U-07670_BoGhiSo/UC_BoGhiSo.md) |
| Màn hình nguồn | `SCR_DanhSachDieuChinhGia` (nút Bỏ ghi sổ) · `SCR_XemChiTietDieuChinhGia` BR1 |
| Endpoint phụ trách | **A8** `POST /{id}/bo-ghi-so` · **A13** `POST /bo-ghi-so-hang-loat` |

## 1. Quyết định riêng

- **Bỏ ghi sổ = XOÁ VẬT LÝ dòng sổ cái**, không sinh bút toán đảo — quyết định nghiệp vụ đã chốt của hệ thống (migration V56, ghi trong javadoc [GhiSoApi.boGhiSo](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/hach_toan/api/GhiSoApi.java)). Hệ quả bắt buộc phải nói với BA: **chứng từ thuộc kỳ đã khoá KHÔNG bỏ ghi sổ được** — muốn gỡ phải mở kỳ trước (đúng BR17.1 dòng "Bỏ ghi sổ · kỳ đóng ⇒ chặn").
- **`MSG_202` "Hóa đơn đã ký phát hành, không thể bỏ ghi sổ" chưa kiểm được** — §12-Q3 file gốc. Cài **cấu trúc** để module hóa đơn sau này cắm vào mà không phải sửa luồng: interface `HoaDonDieuChinhPort` trong `internal/port/`, cài đặt mặc định `KhongCoHoaDonAdapter` trả "chứng từ không gắn hóa đơn đã phát hành". **Không chọn** bỏ hẳn luật: khi module hóa đơn lên, chỗ cắm đã có sẵn và có test chờ.
- **Popup xác nhận của UC bước 5** (*"Nếu bỏ ghi sổ … thì Hóa đơn điều chỉnh được sinh ra cũng bị xóa…"*) là **của FE**; BE không trả câu này (không có mã trong `6.messages.md` — §12-Q5). FE đã dựng (`IMPLEMENT.md` dòng 300).

## 2. Hợp đồng API

### A8 — `POST /{id}/bo-ghi-so` · quyền `DieuChinhGiaHangBan.Unpost`

Không có body ([BaseChungTuController.java:102](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/controller/BaseChungTuController.java)).

```jsonc
// Response 200
{ "code": "SUCCESS", "message": "Bỏ ghi sổ chứng từ điều chỉnh giá thành công",
  "messageId": "MSG_PMKT-E-07664_005", "data": { /* DTO, trangThaiChungTu = "NHAP" */ } }
```

| Điều kiện | HTTP | Mã | messageId |
|---|---|---|---|
| Thiếu quyền `.Unpost` | 403 | — | `_007` |
| `id` không tồn tại | 404 | — | — |
| Chứng từ **chưa ghi sổ** | 400 | `CHUA_GHI_SO` | `MSG_COMMON_001` (BR42.1 quy định đúng mã này) |
| Dòng sổ cái thuộc **kỳ đã khoá** | 400 | `KY_KE_TOAN_DONG` | `_203` (kernel ném `PeriodLockedException`) |
| Hóa đơn điều chỉnh **đã ký phát hành** | 400 | `HOA_DON_DA_KY_PHAT_HANH` | `_202` — **hiện không bao giờ xảy ra**, xem §1 |
| Gọi lại khi đã bỏ ghi sổ | 400 `CHUA_GHI_SO` (chặn ở G2') hoặc kernel trả 0 dòng | — | idempotent |

### A13 — `POST /bo-ghi-so-hang-loat` · quyền `.Unpost`

Body/response như [05 §2 A14](05-xoa.md), messageId `MSG_PMKT-E-07664_005`.
BR42.3: chứng từ "Chưa ghi sổ" trong lô bị **tự động bỏ qua** (skip), không làm hỏng cả lô; thông báo kết quả dạng *"Bỏ ghi sổ thành công X/Y chứng từ. Đã bỏ qua Z chứng từ chưa ghi sổ."* — câu này do FE dựng từ `KetQuaHangLoatDto`.

## 3. Validation

| # | Luật | Thời điểm | Thông báo | Mã |
|---|---|---|---|---|
| B1 | Chứng từ tồn tại, đúng tenant | `chuanBiChungTu` | — | 404 |
| B2 | `status == DA_GHI_SO` | `kiemTraNghiepVu` | Thao tác không hợp lệ với trạng thái hiện tại của chứng từ/phiếu | `MSG_COMMON_001` (BR42.1) |
| B3 | Hóa đơn điều chỉnh gắn kèm chưa ký phát hành | `kiemTraNghiepVu` qua `HoaDonDieuChinhPort` | Hóa đơn đã ký phát hành | `_202` |
| B4 | Mọi dòng sổ cái đang gỡ thuộc kỳ mở | **kernel** `GhiSoApi.boGhiSo` — kiểm theo **từng ngày hạch toán riêng** của các dòng | Ngày hạch toán không thuộc kỳ kế toán đang mở | `_203` |

## 4. Luồng xử lý

`ChungTuTemplate` luồng BO_GHI_SO ([:231](../../cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java)) — **gỡ tác động cũ TRƯỚC, đổi trạng thái SAU**:

```
doiHoiDinhDanh → khoaChungTu → kiemTraNghiepVu (B2, B3)
  → xoaButToanSoCai   → GhiSoApi.boGhiSo(id)     ← xoá vật lý acc_so_cai
  → (hoanTacTonKho bị bỏ qua: coAnhHuongTonKho = false)
  → luuChungTu (truocKhiLuu: status = NHAP, nguoiGhiSo = null, thoiGianGhiSo = null)
  → sauKhiLuu (KHÔNG gỡ liên kết nguồn — xem dưới)
  → ghiNhatKyTacDong → dangKyThongBaoSauCommit
```

**Không có khoảnh khắc nào cờ nói "chưa ghi sổ" mà sổ cái còn dòng** — cả hai bước trong một transaction, theo đúng thứ tự base đã cưỡng chế.

### Liên kết nguồn: giữ hay gỡ?

**Chọn: GIỮ.** Bỏ ghi sổ đưa chứng từ về trạng thái sửa được, chứ không huỷ nó — dòng chi tiết vẫn còn, nên liên kết nguồn vẫn đúng. Gỡ liên kết ở đây rồi phải tạo lại khi ghi sổ lại là thêm một cặp thao tác không cần thiết, và cửa sổ giữa hai lần đó khiến tab "Chứng từ liên quan" của CTBH gốc mất dòng một cách khó hiểu.
Liên kết **chỉ bị gỡ** ở luồng Xoá ([05 §1](05-xoa.md)) và khi Sửa (gỡ rồi tạo lại — [04 §4](04-chinh-sua.md)).
⚠ Điều này lệch với `QuanHeChungTuApi.goToanBoTheoDich` javadoc ("dùng khi xóa **hoặc bỏ ghi sổ** chứng từ đó"). Lý do lệch đã nêu; **cần Dev BE review chốt** (đưa vào §13 file gốc).

### Cái UC đòi mà ta không làm được

| UC_BoGhiSo đòi | Trạng thái |
|---|---|
| Xóa bút toán hạch toán | ✅ làm |
| Cập nhật trạng thái về "Chưa ghi sổ" | ✅ làm |
| Rollback công nợ khách hàng | ✅ **hệ quả tự nhiên** của việc xoá dòng sổ cái — công nợ là số dư tính từ sổ cái, không phải bảng riêng |
| Rollback sổ thuế đầu ra | ❌ không có module sổ thuế (D3) |
| Xóa HĐĐT điều chỉnh | ❌ không có module hóa đơn (D3) |
| Hủy Phiếu thu/chi, Giấy báo | ❌ không có module phiếu thu/chi (D3) |

## 5. Tương tranh & idempotency

| Cơ chế | Chống gì |
|---|---|
| `khoaChungTu` | hai người cùng bấm Bỏ ghi sổ, hoặc một người ghi sổ trong lúc người kia đang bỏ ghi sổ |
| B2 (`status`) | bỏ ghi sổ chứng từ chưa ghi sổ (BR42.1) |
| Kernel `boGhiSo` idempotent | chưa ghi sổ ⇒ trả 0, **không ném lỗi** — nên retry mạng an toàn |
| `period_guard` ở DB | DELETE vào kỳ khoá lọt qua tầng Java |

## 6. Kiểm thử

### Unit (`@Tag("unit")`)
| Lớp test | Kiểm gì |
|---|---|
| `BoGhiSoDieuChinhGiaTest` | B2 chặn chứng từ `NHAP` với `MSG_COMMON_001`; `truocKhiLuu` đặt `status = NHAP` và **null hoá** `nguoiGhiSo`/`thoiGianGhiSo` (BR46.3); B3 gọi `HoaDonDieuChinhPort` đúng một lần |
| `KhongCoHoaDonAdapterTest` | cài đặt mặc định luôn trả "không có hóa đơn đã phát hành" ⇒ B3 không chặn ai (ghim hành vi tạm để khi module hóa đơn lên là test đỏ, buộc sửa) |

### Tích hợp (cần Docker)
| Lớp test | Kiểm gì |
|---|---|
| `BoGhiSoDieuChinhGiaIT` | sau bỏ ghi sổ: 0 dòng `acc_so_cai`, `status = NHAP`, `nguoi_ghi_so IS NULL` · **liên kết `ctu_quan_he_chung_tu` vẫn còn** (§4) · chứng từ trong kỳ đã khoá ⇒ 400 `_203` và dòng sổ cái **vẫn nguyên** · bỏ ghi sổ → sửa → ghi sổ lại ⇒ bút toán mới đúng, không trùng |
| `BoGhiSoHangLoatIT` | lô hỗn hợp: chứng từ chưa ghi sổ bị skip, đếm đúng, HTTP 200 |

## 7. BR đã áp dụng
BR12 (B2, quy tắc bất biến) · BR13.1 (nút chỉ hiện khi đã ghi sổ — FE) · BR16.1 (`MSG_COMMON_001`) · BR17.1 (B4 — kỳ khoá chặn cả bỏ ghi sổ) · BR25 (`.Unpost`) · BR41 (không áp dụng — quan hệ nguồn của epic này là ràng buộc nghiệp vụ, BR41 tự loại trừ) · BR42 (toàn bộ) · BR45 (A13) · BR46 (null hoá vết ghi sổ).

**BR chưa đạt:** phần rollback sổ thuế / HĐĐT / phiếu thu-chi của UC_BoGhiSo — D3, §12-Q2 file gốc.
