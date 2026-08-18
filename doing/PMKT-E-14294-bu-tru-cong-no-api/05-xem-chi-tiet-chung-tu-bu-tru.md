# F05 — Xem chi tiết chứng từ bù trừ công nợ

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F05** |
| Use case | **PMKT-U-14691** — `4.usecases/PMKT-U-14691_BTCN_XemChiTiet/UC_BTCN_XemChiTiet.md` |
| Màn hình | `5.screens/SCR_BTCN_ChungTu_XemChiTiet.md` |
| Ma trận ẩn/hiện | `Matrix/…/SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md` |
| Endpoint phụ trách | **A8** `GET /api/ke-toan-tong-hop/bu-tru-cong-no/{id}` · **A9** `GET /{id}/thong-tin-hach-toan` |
| Quyết định liên quan | **D9** (snapshot cặp ghép) |

---

## 1. Quyết định riêng của chức năng

| # | Quyết định | Lý do · vì sao không chọn cách kia |
|---|---|---|
| **F05-a** | **Một** endpoint A8 trả **toàn bộ** màn hình (thông tin chung + tab Hạch toán + tab Chứng từ công nợ + tham chiếu) | BA: cả hai tab hiển thị ngay khi mở màn, chế độ chỉ xem (`SCR_BTCN_ChungTu_XemChiTiet.md:23-27`). Tách 3 endpoint = 3 round-trip cho một màn không có tab lazy |
| **F05-b** | Endpoint nằm ở `/bu-tru-cong-no/{id}`, **không** ở `/phieu-ke-toan/{id}` | BA: xem chi tiết chứng từ bù trừ mở `SCR_BTCN_ChungTu_XemChiTiet`, "**không** mở màn xem chi tiết Phiếu kế toán tổng hợp chung" (`UC_BTCN_XemChiTiet.md:12`). Hai màn khác nhau ⇒ hai hợp đồng khác nhau |
| **F05-c** | Trả 404 `MSG_..._021` nếu `id` tồn tại nhưng `loai_phieu ≠ 'Bù trừ công nợ'` | Endpoint này là hợp đồng của **chứng từ bù trừ**. Trả về một phiếu KTTH loại khác qua đây sẽ khiến FE dựng màn sai (thiếu tab Chứng từ công nợ) |
| **F05-d** | Cột **Ngày chứng từ / Hạn thanh toán / Số tiền** của chứng từ gốc trong tab Chứng từ công nợ đọc **join qua port**, không lưu snapshot | BA ghi "Lấy theo chứng từ gốc" cho đúng 3 cột này (`SCR_BTCN_ChungTu_ThemMoi.md:68,71,72`), khác với `Số chưa thu`/`Số còn nợ`/`Số bù trừ` là snapshot (`:74,86`). Lưu snapshot thứ BA nói lấy từ gốc sẽ hiển thị sai khi chứng từ gốc được sửa |
| **F05-e** | Tab Hạch toán của màn xem chi tiết đọc từ **`ktth_chi_tiet_phieu_ktth_hach_toan`**, không phải `acc_so_cai` | BA mô tả tab Hạch toán là "các dòng bút toán bù trừ và chênh lệch tỷ giá (nếu có)" ở **chế độ chỉ xem** — đó là dữ liệu chứng từ, hiển thị được cả khi chưa ghi sổ. `acc_so_cai` trả về qua A9 riêng, đúng phân biệt đã ghi ở `BaseChungTuController.java:130-134` |

---

## 2. Hợp đồng API

### 2.1 A8 — `GET /api/ke-toan-tong-hop/bu-tru-cong-no/{id}`

**Quyền:** `PhieuKeToan.View.Detail` (`SCR_BTCN_ChungTu_XemChiTiet.md:19`, `QuyenChecker.java:28`).

```jsonc
// Response 200 — ApiResponse<ChungTuBuTruDto>
{
  // ApiResponse<T> = { data, message, messageId } — core/response/ApiResponse.java:21
  "message": null, "messageId": null,
  "data": {
    "id": "8f1c…",
    "soChungTu": "PBT-000012",
    "status": "DA_GHI_SO",
    "phienBan": 3,

    "thongTinChung": {
      "doiTuongId": "5f3a…", "maDoiTuong": "KH001", "tenDoiTuong": "Công ty TNHH ABC",
      "lyDo": "Bù trừ công nợ phải thu, phải trả với Công ty TNHH ABC",
      "taiKhoanPhaiThuId": "…", "soTaiKhoanPhaiThu": "1311", "tenTaiKhoanPhaiThu": "…",
      "taiKhoanPhaiTraId": "…", "soTaiKhoanPhaiTra": "3311", "tenTaiKhoanPhaiTra": "…",
      "ngayBuTru": "2026-08-11",
      "ngayHachToan": "2026-08-11",
      "ngayChungTu": "2026-08-11",
      "soTienBuTru": 5000000.0000,
      "soTienBuTruQuyDoi": 5000000.00,
      "loaiTienId": "…", "maLoaiTien": "VND",
      "dongTienHachToan": true
    },

    "dongHachToan": [
      { "thuTu": 1, "moTa": "Bù trừ công nợ phải thu, phải trả",
        "taiKhoanNoId": "…", "soTaiKhoanNo": "3311",
        "taiKhoanCoId": "…", "soTaiKhoanCo": "1311",
        "soTien": 5000000.0000, "soTienQuyDoi": 5000000.00, "tyGia": 1 }
    ],

    "capGhep": [
      { "thuTu": 1,
        "phaiThu": { "chungTuId": "a1…", "loaiChungTu": "SAL_CHUNG_TU_BAN_HANG",
                     "tenLoaiChungTu": "Chứng từ bán hàng",
                     "ngayChungTu": "2026-07-02", "soChungTu": "PBH-000045",
                     "soHoaDon": "HD-0012", "hanThanhToan": "2026-08-02",
                     "soTien": 10000000.0000, "soTienQuyDoi": 10000000.00,
                     "soChuaThu": 8000000.0000, "soChuaThuQuyDoi": 8000000.00,
                     "tyGia": 1,
                     "soTienBuTru": 3000000.0000, "soTienBuTruQuyDoi": 3000000.00,
                     "chungTuTonTai": true },
        "phaiTra": { "chungTuId": "b1…", "loaiChungTu": "PUR_CHUNG_TU_MUA_HANG",
                     "tenLoaiChungTu": "Chứng từ mua hàng",
                     "ngayChungTu": "2026-06-20", "soChungTu": "PMH-000031",
                     "soHoaDon": "HD-9911", "hanThanhToan": "2026-07-20",
                     "soTien": 4000000.0000, "soTienQuyDoi": 4000000.00,
                     "soConNo": 3000000.0000, "soConNoQuyDoi": 3000000.00,
                     "tyGia": 1,
                     "soTienBuTru": 3000000.0000, "soTienBuTruQuyDoi": 3000000.00,
                     "chungTuTonTai": true },
        "chenhLechTyGia": 0 }
    ],
    "tongChenhLechTyGiaQuyDoi": 0,

    "thamChieu": [
      { "chungTuId": "a1…", "loaiChungTu": "SAL_CHUNG_TU_BAN_HANG", "soChungTu": "PBH-000045" },
      { "chungTuId": "b1…", "loaiChungTu": "PUR_CHUNG_TU_MUA_HANG", "soChungTu": "PMH-000031" }
    ],

    "choPhepSua":   false,
    "choPhepXoa":   false,
    "choPhepGhiSo": false,
    "choPhepBoGhi": true,
    "daGhiSo":      true
  }
}
```

**Lỗi:**

| HTTP | Mã lỗi | messageId | Khi nào |
|---|---|---|---|
| 403 | `FORBIDDEN` | `MSG_..._005` | Thiếu `PhieuKeToan.View.Detail` (`UC_BTCN_XemChiTiet.md:63`) |
| 404 | `KHONG_TIM_THAY` | `MSG_..._021` | `id` không tồn tại, đã xóa mềm, **hoặc** `loai_phieu ≠ 'Bù trừ công nợ'` (F05-c) — `UC_BTCN_XemChiTiet.md:64` |

### 2.2 A9 — `GET /api/ke-toan-tong-hop/bu-tru-cong-no/{id}/thong-tin-hach-toan`

**Kế thừa nguyên** từ `BaseChungTuController.java:139-144`, **không viết lại**. Trả các dòng `acc_so_cai` **đã ghi** của chứng từ, qua `SoCaiApi.theoChungTu` (`accounting_core/hach_toan/api/SoCaiApi.java:31`).

Quyền `PhieuKeToan.View.Detail`. Chứng từ chưa ghi sổ trả **danh sách rỗng** — trạng thái hợp lệ, không phải lỗi (`SoCaiApi.java:24-27`). Base đã gọi `service().kiemTraTonTai(id)` trước để một id bịa không trả 200 rỗng (`BaseChungTuController.java:135-137`).

> A9 dùng để **đối chiếu** tab Hạch toán (bút toán của chứng từ) với sổ cái thật. Nếu BA không cần chức năng đối chiếu này trên UI thì endpoint vẫn nên giữ — nó là công cụ hỗ trợ vận hành, chi phí bằng 0 vì base đã cấp.

---

## 3. Ánh xạ cột: BA ↔ DB ↔ DTO

### 3.1 Thông tin chung (`SCR_BTCN_ChungTu_XemChiTiet.md:25`)

| Cột BA | Field DTO | Nguồn |
|---|---|---|
| Đối tượng | `tenDoiTuong` (+ `maDoiTuong`) | `ktth_bu_tru_cong_no.doi_tuong_id` → join `mst_doi_tuong` (native query) |
| Lý do | `lyDo` | `ktth_phieu_ke_toan_tong_hop.mo_ta` |
| TK phải thu / TK phải trả | `soTaiKhoanPhaiThu` / `…PhaiTra` | `ktth_bu_tru_cong_no.tai_khoan_phai_thu_id` / `…_phai_tra_id` → join `mst_he_thong_tai_khoan` |
| Ngày bù trừ | `ngayBuTru` | `ktth_bu_tru_cong_no.ngay_bu_tru` |
| Ngày hạch toán / Ngày chứng từ | `ngayHachToan` / `ngayChungTu` | `ktth_phieu_ke_toan_tong_hop.*` |
| Số chứng từ | `soChungTu` | `.so_chung_tu` |
| Tham chiếu | `thamChieu[]` | `ktth_chung_tu_lien_quan` → join lấy `soChungTu` chứng từ gốc |
| Số tiền bù trừ | `soTienBuTru` (+ `…QuyDoi`) | `ktth_bu_tru_cong_no.so_tien_bu_tru` / `…_quy_doi` |
| Loại tiền | `maLoaiTien` | `.loai_tien_id` → join `mst_loai_tien` |

### 3.2 Tab Chứng từ công nợ — snapshot vs. đọc gốc

| Cột BA | Nguồn | Lý do |
|---|---|---|
| Loại chứng từ | **snapshot** `loai_chung_tu_phai_thu` / `…_phai_tra` | `ldm-KTTH.puml:169,179` |
| Số chứng từ (link) | **snapshot id** + `soChungTu` đọc gốc qua port | Id là snapshot (`:168,178`); số hiển thị lấy gốc để phản ánh chỉnh sửa |
| Số hóa đơn | **snapshot** `so_hoa_don_phai_thu` / `…_phai_tra` | `:170,180` |
| Ngày chứng từ · Hạn thanh toán · Số tiền | **đọc gốc** qua `port.theoIds` | BA: "Lấy theo chứng từ gốc" (`SCR_BTCN_ChungTu_ThemMoi.md:68,71,72`) — F05-d |
| Số chưa thu / Số còn nợ | **snapshot** `so_chua_thu` / `so_con_no` | BA: "tại thời điểm bù trừ" (`:74,86`); LDM: "Lưu số liệu snapshot… để hiển thị và hoàn trả khi Bỏ ghi/Xóa" (`ldm-KTTH.puml:160-161`) |
| Số bù trừ (+ quy đổi) | **snapshot** `so_tien_bu_tru_phai_thu(_quy_doi)` / `…_phai_tra(_quy_doi)` | `:175-176,184-185` |
| Chênh lệch tỷ giá | **snapshot** `chenh_lech_ty_gia` | `:187` |
| Tỷ giá (dùng quy đổi) | **snapshot** `ty_gia_phai_thu` / `ty_gia_phai_tra` | `:172,182` |

> **`chungTuTonTai`** trong DTO: chứng từ gốc có thể đã bị xóa mềm sau khi bù trừ **bị bỏ ghi** (chứng từ bù trừ đã ghi sổ thì chặn — [08](08-chan-bo-ghi-chung-tu-goc.md)). Khi đó `port.theoIds` không trả dòng ⇒ 3 cột "đọc gốc" là `null` và `chungTuTonTai = false`; FE tắt hyperlink. **Không** ném lỗi: màn xem chi tiết phải mở được kể cả khi chứng từ gốc biến mất.

### 3.3 Field phụ để FE ẩn/hiện nút (BR13.2)

Theo `Matrix/…/SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md:43-46`:

| Nút | Điều kiện | Field DTO |
|---|---|---|
| Ghi sổ | `status != DA_GHI_SO` | `choPhepGhiSo` |
| Xóa | `status != DA_GHI_SO` | `choPhepXoa` |
| Bỏ ghi | `status == DA_GHI_SO` | `choPhepBoGhi` |
| **Sửa** | **Không bao giờ** (`SCR_BTCN_ChungTu_XemChiTiet.md:56`) | `choPhepSua` = **hằng `false`** |
| In · Tiện ích · Điều hướng | Luôn hiển thị | Không cần field (FE tự biết) |

`dongTienHachToan` điều khiển ẩn/hiện toàn bộ cột quy đổi + cột Chênh lệch tỷ giá (marker `(đk-LT)` ở ma trận dòng 39, 42) theo BR18.4.

---

## 4. Validation

| # | Luật | Thời điểm | Thông báo | BR nguồn |
|---|---|---|---|---|
| V1 | Quyền `PhieuKeToan.View.Detail` | Đầu handler | 403 · `MSG_..._005` | BR25 · `UC_BTCN_XemChiTiet.md:63` |
| V2 | Chứng từ tồn tại, `da_xoa = false` | Service | 404 · `MSG_..._021` | BR29.1 · `:64` |
| V3 | `loai_phieu = 'Bù trừ công nợ'` | Service | 404 · `MSG_..._021` | F05-c |
| V4 | Tenant | RLS ở DB | — | BR28 |
| V5 | Chứng từ gốc không tồn tại | Service | **Không lỗi** — `chungTuTonTai = false` | §3.2 |

Không có validation nghiệp vụ nào khác — endpoint chỉ đọc.

---

## 5. Luồng xử lý

```
A8  GET /bu-tru-cong-no/{id}
 1. quyen.require("PhieuKeToan", "View.Detail")
 2. Nạp aggregate bằng MỘT query có JOIN FETCH:
        PhieuKeToanTongHop
          ├── BuTruCongNo                       (1-1)
          ├── ChiTietPhieuKtthHachToan          (1-n, ORDER BY thu_tu)
          ├── ChiTietBuTruCongNoChungTu         (1-n, ORDER BY thu_tu)
          └── ChungTuLienQuan                   (1-n)
    → V2, V3
 3. Gom (chungTuId, loaiChungTu) của 2 bên trong capGhep + thamChieu
 4. GỌI MỘT LẦN cho mỗi port: port.theoIds(ids)      ← chống N+1
 5. Nạp danh mục (đối tượng, 2 tài khoản, loại tiền) bằng native query gộp
 6. BuTruCongNoMapper → ChungTuBuTruDto, tính choPhep* + dongTienHachToan
 7. ApiResponse.ok(dto)
```

**Bước gọi base / viết mới:**

| Bước | Trạng thái |
|---|---|
| 1 | ✅ `QuyenChecker.require` |
| 2 | 🆕 `PhieuKeToanTongHopRepository` — `@EntityGraph` / `JOIN FETCH` **trong** transaction (`cell-app/CLAUDE.md:145-146`) |
| 4 | ✅ SPI `ChungTuCongNoPort.theoIds` — [08 §3](08-chan-bo-ghi-chung-tu-goc.md) |
| 5 | 🆕 `TraCuuDanhMucBuTruRepository` theo khuôn `TraCuuDanhMucRepository.java:42-60` |
| 6 | 🆕 `BuTruCongNoMapper` |
| A9 | ✅ **kế thừa nguyên** `BaseChungTuController.java:139-144` |

> ⚠️ **Bẫy N+1:** nạp 4 collection bằng một `JOIN FETCH` duy nhất sẽ nhân bản dòng (Cartesian). Dùng `@EntityGraph` cho quan hệ 1-1 (`BuTruCongNo`) + **query riêng theo `phieu_ktth_id`** cho từng collection còn lại, rồi ghép ở mapper. Bốn query cố định, không phụ thuộc số dòng — đúng yêu cầu "Không N+1; aggregate là query riêng" của `docs/_bieu-mau-plan-api.md:484`.

---

## 6. Tương tranh & transaction

`@Transactional(readOnly = true)`. Không khoá, không idempotency. `phienBan` trả về DTO để FE gửi kèm ở các thao tác ghi sau đó (ghi sổ / bỏ ghi / xóa) — chống lost-update theo `ChungTuTemplate.java:370-374`.

**LP1 của UC** ("Mở từ link tham chiếu trên chứng từ công nợ" — `UC_BTCN_XemChiTiet.md:50-53`) dùng **chính** A8; chỉ khác điểm vào ở FE. Không cần endpoint riêng.

---

## 7. Phân trang · sắp xếp · lọc · dòng tổng

**Không áp dụng** — màn xem chi tiết một chứng từ.

Hai bảng trong màn có thứ tự cố định:
- Tab Hạch toán: `ORDER BY thu_tu` (dòng 1 bù trừ, dòng 2 chênh lệch tỷ giá — `SCR_BTCN_ChungTu_ThemMoi.md:35`);
- Tab Chứng từ công nợ: `ORDER BY thu_tu` — đúng thứ tự ghép cặp đã lưu (`ldm-KTTH.puml:167`), là thứ tự người dùng đã thấy lúc bù trừ.

Không phân trang: số cặp ghép bị chặn bởi số chứng từ người dùng tick, thực tế nhỏ. Nếu sau này cần trần thì đặt ở bước tạo ([03 §7](03-phan-bo-va-thuc-hien-bu-tru.md)), không ở bước đọc.

**Dòng tổng (BR31):** tab Chứng từ công nợ có cột số tiền ⇒ theo BR31 nên có dòng tổng. BA **không** mô tả dòng tổng cho tab này (khác với 2 bảng ở màn Bù trừ, `SCR_BTCN_BuTru.md:45,76` có nói rõ). Đề xuất: FE cộng từ `capGhep[]` (dữ liệu đã trả đủ, không phân trang) — BE không thêm field. `tongChenhLechTyGiaQuyDoi` **có** trả vì BA yêu cầu đối chiếu với dòng hạch toán 2 (`SCR_BTCN_ChungTu_ThemMoi.md:95`).

---

## 8. Kiểm thử

### 8.1 Unit test (`@Tag("unit")`)

| Lớp test | Input → Kỳ vọng |
|---|---|
| `BuTruCongNoMapperTest` | `status = DA_GHI_SO` → `choPhepBoGhi=true`, `choPhepGhiSo=false`, `choPhepXoa=false` |
| `BuTruCongNoMapperTest` | `status = NHAP` → `choPhepGhiSo=true`, `choPhepXoa=true`, `choPhepBoGhi=false` |
| `BuTruCongNoMapperTest` | `choPhepSua` = `false` ở **mọi** trạng thái (`SCR_BTCN_ChungTu_XemChiTiet.md:56`) |
| `BuTruCongNoMapperTest` | Chứng từ gốc thiếu trong map port → `chungTuTonTai=false`, 3 cột đọc-gốc = `null`, **không** ném |
| `BuTruCongNoMapperTest` | `loaiTienId` = đồng tiền hạch toán → `dongTienHachToan=true`, `tongChenhLechTyGiaQuyDoi=0` |
| `BuTruCongNoMapperTest` | Σ `capGhep[].chenhLechTyGia` == `tongChenhLechTyGiaQuyDoi` |
| `BuTruCongNoMapperTest` | `capGhep` sắp theo `thuTu` tăng dần |
| `BuTruCongNoMapperTest` | `thamChieu` dedupe theo `chungTuId` |

### 8.2 Test tích hợp (cần Docker)

| Lớp test | Kiểm gì |
|---|---|
| `XemChiTietBuTruIT` | Trả đủ thông tin chung + 2 dòng hạch toán (ngoại tệ) + N cặp ghép + tham chiếu |
| `XemChiTietBuTruIT` | `id` của phiếu KTTH loại `'Khác'` → 404 `MSG_..._021` (F05-c) |
| `XemChiTietBuTruIT` | `id` đã xóa mềm → 404 `MSG_..._021` |
| `XemChiTietBuTruIT` | RLS: tenant khác → 404 |
| `XemChiTietBuTruIT` | **Đếm số query** khi có 20 cặp ghép: cố định, không tăng theo số dòng (chống N+1) |
| `XemChiTietBuTruIT` | Chứng từ chưa ghi sổ: A8 trả `dongHachToan` **có dữ liệu**, A9 trả **rỗng** (F05-e) |
| `XemChiTietBuTruIT` | Chứng từ đã ghi sổ: A9 trả đúng số dòng `acc_so_cai` (2 hoặc 4) |

---

## 9. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR7 | Hiển thị số quy đổi theo precision đã lưu |
| BR12 | `status` quyết định bộ nút (§3.3) |
| BR13.2 | 4 field `choPhep*` |
| BR14.1 | Chế độ **Xem** — mọi control disabled; BE không cấp endpoint sửa |
| BR18.4 | `dongTienHachToan` ẩn/hiện cột quy đổi |
| BR25 | V1 `quyen.require(PhieuKeToan, View.Detail)` |
| BR28 | RLS |
| BR29.1 | V2 bỏ bản ghi `da_xoa = true` |
| BR33 | Trả `status` để FE tô màu |
| BR35 | Link tham chiếu mở chứng từ gốc — FE điều hướng, BE cấp `chungTuId` + `loaiChungTu` |
| BR42.2 | Nút Bỏ ghi ẩn khi chưa ghi sổ |
| BR46 | Trường hệ thống không hiển thị trên form |

**Chưa áp được:** BR31 (dòng tổng tab Chứng từ công nợ — BA không mô tả, đề xuất FE tự cộng, §7) · BR34 (không có luồng sửa) · BR44 (truncate — FE) · In/Tiện ích/Điều hướng (ngoài phạm vi, **Q10**).
