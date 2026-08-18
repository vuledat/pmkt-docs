# F04 — Lưu / Lưu và Ghi sổ chứng từ bù trừ công nợ

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F04** |
| Use case | **PMKT-U-14690** AC5 · Luồng chính bước 9–14 — `UC_BTCN_ThemMoi.md:28-31, 62-67` |
| Màn hình | `SCR_BTCN_ChungTu_ThemMoi.md` — Chức năng (Lưu / Lưu và Ghi sổ) · BR01, BR03, BR04 |
| Ma trận ẩn/hiện | `Matrix/…/SCR_BTCN_ChungTu_ThemMoi_MaTranAnHien.md` — 5 trường cho nhập, còn lại read-only |
| Endpoint phụ trách | **A7** `POST /api/ke-toan-tong-hop/bu-tru-cong-no/them-moi` |
| Quyết định liên quan | **D3** (ChungTuTemplate), **D8** (số chứng từ tự nhập), **D9** (snapshot), **D10** (định khoản) |

---

## 1. Quyết định riêng của chức năng

| # | Quyết định | Lý do · vì sao không chọn cách kia |
|---|---|---|
| **F04-a** | **Một endpoint** cho cả "Lưu" và "Lưu và Ghi sổ", phân biệt bằng cờ `ghiSoNgay` trong body | `ChungTuTemplate.coGhiSoNgay(ctx)` (`ChungTuTemplate.java:341-343`) đã là cơ chế chuẩn để phân biệt hai nút; base ghi rõ "'Lưu và ghi sổ' trên màn hình là MỘT lần `thucThi` trong MỘT transaction, không phải hai request rời" (`ChungTuTemplate.java:99-100`). **Không chọn** 2 endpoint: "lưu xong rồi ghi sổ" thành 2 transaction, có khoảnh khắc chứng từ tồn tại mà chưa ghi sổ dù người dùng bấm nút gộp |
| **F04-b** | Request mang lại **toàn bộ** lựa chọn (2 danh sách chứng từ + số tiền), **không** mang bản nháp A6 trả về | Server **dựng lại** cặp ghép, dòng hạch toán, chênh lệch tỷ giá từ đầu bằng chính các lớp `business/` đã dùng ở A6. Tin bản nháp client gửi lên là mở đường cho số liệu hạch toán bị chỉnh tay |
| **F04-c** | Kiểm quyền: `BuTruCongNo.Create` **luôn**, cộng `PhieuKeToan.Post` **khi** `ghiSoNgay = true` | `ChungTuTemplate.kiemTraQuyen` mặc định chỉ kiểm `maChucNang().Create` (`ChungTuTemplate.java:294-296`). Bù trừ có **hai** mã chức năng (tạo thuộc `BuTruCongNo`, ghi sổ thuộc `PhieuKeToan` — `SCR_BTCN_ChungTu_XemChiTiet.md:50`) ⇒ `TaoChungTuBuTru` **override** `kiemTraQuyen` để kiểm cả hai |
| **F04-d** | `tong_tien` của phiếu = **Σ `so_tien` (nguyên tệ) các dòng hạch toán**, tính lúc lưu và ghi vào cột | `SCR_BTCN_DanhSach.md:20` — "Tổng tiền với chứng từ loại 'Bù trừ công nợ' = Tổng(Số tiền tab Hạch toán) — bằng Số tiền bù trừ (dòng xử lý chênh lệch tỷ giá có số tiền nguyên tệ = 0 nên không ảnh hưởng)". Ghi sẵn để danh sách (F01) không phải join + SUM mỗi lần đọc |
| **F04-e** | Aggregate root là **`PhieuKeToanTongHop`**; `BuTruCongNo` + cặp ghép + dòng hạch toán + tham chiếu là con, `cascade = ALL` + `orphanRemoval = true` | `docs/be-khung-kien-truc-chuan.md:201-202`. Chỉ `PhieuKeToanTongHopRepository` là repository của aggregate; các repository con dùng cho truy vấn đọc chuyên biệt |

---

## 2. Hợp đồng API

### A7 — `POST /api/ke-toan-tong-hop/bu-tru-cong-no/them-moi`

**Quyền:** `BuTruCongNo.Create` (+ `PhieuKeToan.Post` khi `ghiSoNgay = true`).

```jsonc
// Request — LuuBuTruRequest
{
  "soChungTu": "PBT-000012",
  "lyDo": "Bù trừ công nợ phải thu, phải trả với Công ty TNHH ABC",
  "ngayChungTu": "2026-08-11",
  "ngayHachToan": "2026-08-11",
  "ghiSoNgay": false,

  "doiTuongId": "5f3a…",
  "taiKhoanPhaiThuId": "…",
  "taiKhoanPhaiTraId": "…",
  "loaiTienId": "…",
  "ngayBuTru": "2026-08-11",

  "phaiThu": [ { "chungTuId": "a1…", "loaiChungTu": "SAL_CHUNG_TU_BAN_HANG", "soTienBuTru": 5000000.0000 } ],
  "phaiTra": [ { "chungTuId": "b1…", "loaiChungTu": "PUR_CHUNG_TU_MUA_HANG", "soTienBuTru": 3000000.0000 },
               { "chungTuId": "b2…", "loaiChungTu": "PUR_CHUNG_TU_MUA_HANG", "soTienBuTru": 2000000.0000 } ],

  "dienGiaiHachToan": [
    { "thuTu": 1, "moTa": "Bù trừ công nợ phải thu, phải trả" },
    { "thuTu": 2, "moTa": "Xử lý chênh lệch tỷ giá" }
  ]
}
```

| Field | Kiểu | Bắt buộc | Ràng buộc | Nguồn BA |
|---|---|---|---|---|
| `soChungTu` | string | **Y** | Trim (BR43); ≤ 50 ký tự; không dấu tiếng Việt (BR20.2); duy nhất theo tenant (BR19.1) | `SCR_BTCN_ChungTu_ThemMoi.md:26` |
| `lyDo` | string | **Y** | Trim; ≤ **500** ký tự | `:20` |
| `ngayChungTu` | date | **Y** | — | `:25` |
| `ngayHachToan` | date | **Y** | Kỳ kế toán phải mở (BR17.1) | `:24` |
| `ghiSoNgay` | boolean | N | Mặc định `false` = nút **Lưu**; `true` = **Lưu và Ghi sổ** | `:104-105` |
| 5 trường Header Filter | — | **Y** | Như [03 §3](03-phan-bo-va-thuc-hien-bu-tru.md) | `SCR_BTCN_BuTru.md:28-32` |
| `phaiThu[]` / `phaiTra[]` | list | **Y** | Như A6 — validate lại đầy đủ | BR03 |
| `dienGiaiHachToan[]` | list | N | Chỉ 2 field cho sửa trên tab Hạch toán là **Diễn giải** (`:42`, ma trận `…ThemMoi_MaTranAnHien.md:37`); mọi trường khác server tự dựng | `:42` |

> **Không nhận từ client:** `taiKhoanNoId`/`taiKhoanCoId`/`soTien`/`soTienQuyDoi` của dòng hạch toán, `capGhep[]`, `thamChieu[]`, `tongTien`, `status`, `tenantId`, `daXoa`, mọi trường hệ thống BR46. Ma trận ẩn/hiện xác nhận **chỉ 5 trường cho nhập**: Lý do, Ngày hạch toán, Ngày chứng từ, Số chứng từ, Diễn giải tab Hạch toán (`SCR_BTCN_ChungTu_ThemMoi_MaTranAnHien.md:53`). Nhận thêm trường nào ngoài đó là lỗi thiết kế.

```jsonc
// Response 201 — ApiResponse<ChungTuBuTruDto> = { data, message, messageId }
// Shape đã kiểm: core/response/ApiResponse.java:21 (KHÔNG có code / timestamp)
{
  "data": { /* cấu trúc như A8 — xem 05-xem-chi-tiet-chung-tu-bu-tru.md §3 */ },
  "message": "Lưu chứng từ bù trừ công nợ thành công",
  "messageId": "MSG_PMKT-E-14294_001"
}
```

Dựng bằng `ApiResponse.ok(dto, message, messageId)` (`core/response/ApiResponse.java:33`).

Khi `ghiSoNgay = true`: `message` = "Ghi sổ chứng từ bù trừ công nợ thành công", `messageId` = `MSG_PMKT-E-14294_002`.

> ⚠️ BA yêu cầu hiển thị **cả hai** thông báo khi Lưu và Ghi sổ: "`MSG_..._001` **và** `MSG_..._002`" (`SCR_BTCN_ChungTu_ThemMoi.md:105`). Envelope `ApiResponse` chỉ mang **một** `messageId`. Đề xuất: trả `messageId = MSG_..._002` (thông báo cuối cùng, mang nhiều thông tin hơn) và thêm `data.daGhiSo = true` để FE tự bắn thêm toast `MSG_..._001`. Nêu ở [00 §12](00-ke-hoach-tong.md) nếu BA muốn envelope đa message.

**Lỗi:**

| HTTP | Mã lỗi | messageId | Khi nào |
|---|---|---|---|
| 400 | `THIEU_SO_CHUNG_TU` | `MSG_..._014` | `soChungTu` rỗng sau trim |
| 400 | `MSG_..._006/007/008/009/010/011/012/013/016` | như [03 §3.2](03-phan-bo-va-thuc-hien-bu-tru.md) | Validate BR03/BR04 lặp lại |
| 403 | `FORBIDDEN` | `MSG_..._005` | Thiếu `BuTruCongNo.Create` hoặc `PhieuKeToan.Post` |
| 409 | `TRUNG_SO_CHUNG_TU` | `MSG_..._015` | Số chứng từ đã tồn tại trong tenant |
| 409 | `KY_DA_KHOA` | `MSG_..._019` | `PeriodLockedException` — kỳ đã khoá (BR17.1) |
| 409 | `SO_DU_DA_THAY_DOI` | `MSG_..._018` | `ghiSoNgay=true` và số dư chứng từ gốc không còn đủ |
| 500 | `INTERNAL_ERROR` | `MSG_..._017` | Lỗi hệ thống — **không lưu gì** (rollback toàn bộ) |

---

## 3. Ánh xạ cột: BA ↔ DB ↔ DTO

### 3.1 `ktth_phieu_ke_toan_tong_hop` (master)

| Cột BA | Cột DB | Ai ghi | Giá trị |
|---|---|---|---|
| — | `loai_phieu` | **server** | Hằng `'Bù trừ công nợ'` (khớp CHECK `V202:38-42`) — client **không** gửi |
| Số chứng từ | `so_chung_tu` | client | Đã trim |
| Ngày chứng từ | `ngay_chung_tu` | client | |
| Ngày hạch toán | `ngay_hach_toan` | client | ⚠ cột đang `timestamptz`, phải đổi `date` — [09 §2](09-thiet-ke-db.md) |
| Lý do | `mo_ta` | client | Đã trim, ≤ 500 |
| Loại tiền | `loai_tien_id` | client | |
| — | `ty_gia` | **server** | `1` khi đồng tiền hạch toán; ngoại tệ → **Q8** (đề xuất `so_tien_quy_doi_dong1 / so_tien_dong1`, 6 chữ số) |
| Tổng tiền | `tong_tien` | **server tính** | F04-d — Σ `so_tien` các dòng hạch toán |
| Trạng thái | `status` | **server** | `NHAP` (Lưu) hoặc `DA_GHI_SO` (Lưu và Ghi sổ) — `core/entity/TrangThaiChungTu.java:20,29` |
| — | `loai_chung_tu_id` | **server** | `LoaiChungTuLookup.idTheoMa("PBT")` (`LoaiChungTuLookup.java:38`) |
| — | `nam` | **server** | `V202:43` `NOT NULL`; với bù trừ không có ý nghĩa ⇒ ghi `year(ngay_hach_toan)`. `V202:87` ghi chú "0/năm hiện tại với loại khác" |
| — | `nguoi_ghi_so`, `thoi_gian_ghi_so` | **base** | `BaseChungTuEntity.ghiSo()` (`core/entity/BaseChungTuEntity.java:166-180`) — BR46 |
| — | `tenant_id`, `phien_ban`, `ngay_tao`, `nguoi_tao`, `da_xoa`… | **base** | BR28, BR46 |

### 3.2 `ktth_bu_tru_cong_no` (mở rộng 1-1) — bảng **mới**

| Cột BA | Cột DB | Ai ghi | Nguồn |
|---|---|---|---|
| — | `phieu_ktth_id` | server | FK 1-1 (`ldm-KTTH.puml:149`) |
| Đối tượng | `doi_tuong_id` | client | `ldm-KTTH.puml:150` |
| TK phải thu | `tai_khoan_phai_thu_id` | client | `:151` |
| TK phải trả | `tai_khoan_phai_tra_id` | client | `:152` |
| Ngày bù trừ | `ngay_bu_tru` | client | `:153` |
| Số tiền bù trừ | `so_tien_bu_tru` | **server tính** | Σ `soTienBuTru` phía phải thu (= phía phải trả sau V9) · `:154` |
| Số tiền bù trừ quy đổi | `so_tien_bu_tru_quy_doi` | **server tính** | `MIN(Σ quy đổi phải thu, Σ quy đổi phải trả)` · `:155` |

### 3.3 `ktth_chi_tiet_phieu_ktth_hach_toan` — 1 hoặc 2 dòng

Xem [03 §4.2](03-phan-bo-va-thuc-hien-bu-tru.md). Client chỉ ghi được `mo_ta`.

### 3.4 `ktth_chi_tiet_bu_tru_cong_no_chung_tu` — cặp ghép, bảng **mới**

Toàn bộ **server tính** (snapshot D9) — xem [03 §4.3](03-phan-bo-va-thuc-hien-bu-tru.md) và [09 §3](09-thiet-ke-db.md).

### 3.5 `ktth_chung_tu_lien_quan` — tham chiếu đối ứng

`SCR_BTCN_ChungTu_ThemMoi.md:142` — "cập nhật tham chiếu đối ứng **2 chiều**: chứng từ bù trừ ↔ từng chứng từ công nợ tham gia".

| Cột DB | Giá trị | Ghi chú |
|---|---|---|
| `phieu_ktth_id` | id phiếu bù trừ | FK nội-module (`V202:241`) |
| `chung_tu_id` | id phiếu bù trừ | `V202:242` polymorphic |
| `loai_chung_tu_id` | id của `PBT` | |
| `chung_tu_lien_quan_id` | id chứng từ công nợ | `V202:244` |
| `loai_chung_tu_lien_quan_id` | id loại chứng từ gốc | |

Mỗi chứng từ công nợ tham gia → **một** dòng (dedupe theo `chungTuId`, vì một chứng từ có thể xuất hiện ở nhiều cặp ghép).

> ⚠️ "2 chiều" ở đây là **một dòng** mô tả quan hệ hai đầu, không phải hai dòng. Bảng có sẵn cả `chung_tu_id` lẫn `chung_tu_lien_quan_id` nên một dòng đủ diễn tả. Nếu BA muốn chứng từ gốc cũng có dòng riêng trỏ ngược (để tab Tham chiếu của chứng từ bán hàng thấy được), cần thêm dòng thứ hai — **cần BA xác nhận**, và liên quan **Q6** (dùng `ktth_chung_tu_lien_quan` hay `ctu_quan_he_chung_tu`).

---

## 4. Validation — ma trận đầy đủ

| # | Luật | Điều kiện | Thời điểm | Thông báo | BR nguồn |
|---|---|---|---|---|---|
| V1 | Quyền tạo | `BuTruCongNo.Create` | `kiemTraQuyen` (`ChungTuTemplate.java:294`) | 403 · `MSG_..._005` | BR25 |
| V2 | Quyền ghi sổ | `PhieuKeToan.Post` khi `ghiSoNgay` | `kiemTraQuyen` override | 403 · `MSG_..._005` | `SCR_BTCN_ChungTu_XemChiTiet.md:50` |
| V3 | Trim trước mọi kiểm | `soChungTu`, `lyDo`, `moTa` dòng hạch toán | `kiemTraDauVao` | — | BR43 |
| V4 | Số chứng từ bắt buộc | `soChungTu` ≠ rỗng sau trim | `@NotBlank` → `kiemTraDauVao` | 400 · `MSG_..._014` | BR01 màn Thêm mới · `:113` |
| V5 | Số chứng từ ≤ 50 ký tự, không dấu tiếng Việt | Regex | `kiemTraDauVao` | 400 | BR20.2 |
| V6 | Số chứng từ **không trùng** | Kiểm trước ở service + unique index `uq_ktth_phieu_tenant_so_ct` (`V202:70-74`) | `kiemTraNghiepVu` | 409 · `MSG_..._015` | BR19.1 · `:113` |
| V7 | Lý do bắt buộc, ≤ 500 | `@NotBlank @Size(max=500)` | `kiemTraDauVao` | 400 | `:20` |
| V8 | Đủ trường Header Filter | 5 trường | `kiemTraDauVao` | 400 · `MSG_..._006` | BR01 màn Bù trừ |
| V9…V17 | **Toàn bộ luật BR03/BR04** của A6 lặp lại | Xem [03 §5](03-phan-bo-va-thuc-hien-bu-tru.md) V4–V12 | `kiemTraNghiepVu` | `MSG_..._007/008/009/010/011/012/013/016` | BR03, BR04 |
| V18 | Kỳ kế toán mở | `ngayHachToan` không thuộc kỳ khoá | **Lưu thuần:** `ChungTuTemplate.luuKhongGhiSo → kiemTraKyKeToan` (`ChungTuTemplate.java:469-477`) · **Lưu và Ghi sổ:** kernel tự kiểm (`ChungTuTemplate.java:56-61`) | 409 · `MSG_..._019` | BR17.1 |
| V19 | Số dư còn đủ khi ghi sổ | Chỉ khi `ghiSoNgay` — nạp lại dưới khoá | `sauKhiLuu` trước khi gọi port | 409 · `MSG_..._018` | `:149` |
| V20 | Cấu hình TK lãi/lỗ | Chỉ khi ngoại tệ lệch quy đổi | `kiemTraNghiepVu` | 400 · `MSG_..._016` | BR04 · `:127` |
| V21 | Giữ nguyên dữ liệu khi lỗi | Mọi lỗi ⇒ rollback, **không** lưu bản ghi nào | Transaction | — | `UC_BTCN_ThemMoi.md:127`, `:115` |

> **BR37 (đồng bộ Ngày hạch toán ⇄ Ngày chứng từ) là luật FE.** BE nhận cả hai giá trị và **không tự suy** — BR37 mô tả hành vi *khi người dùng sửa trên form*, server không biết giá trị trước khi sửa. Ghi rõ để FE không kỳ vọng server đồng bộ hộ.

---

## 5. Luồng xử lý

`TaoChungTuBuTru extends ChungTuTemplate<LuuBuTruRequest, ChungTuBuTruDto>`, `hanhDong()` = `TAO` (mặc định — `ChungTuTemplate.java:275-277`).

Trình tự do `ChungTuTemplate.luongTao` cưỡng chế (`ChungTuTemplate.java:149-160`):

```
thucThi(lenh)                                        @Transactional  ← ChungTuTemplate.java:102
 1. kiemTraDauVao(ctx)          [base]  Bean Validation             → V3…V8
 2. kiemTraQuyen(ctx)           [OVERRIDE] BuTruCongNo.Create
                                          + PhieuKeToan.Post nếu ghiSoNgay   → V1, V2
 3. chuanBiChungTu(ctx)         [OVERRIDE] nạp đối tượng, TK, loại tiền,
                                          nạp lại 2 danh sách qua port.theoIds()
 ── luongTao ──────────────────────────────────────────────────────────
 4. kiemTraNghiepVu(ctx)        [BẮT BUỘC CÀI] KiemTraBuTru: V6, V9…V17, V20
 5. truocKhiLuu(ctx)            [OVERRIDE]  ← gọi từ luuChungTu (ChungTuTemplate.java:417-421)
        · GhepCapBuTru  → capGhep[]
        · ChenhLechTyGiaBuTru → dòng hạch toán 1 (+2)
        · tính tong_tien (F04-d), so_tien_bu_tru, so_tien_bu_tru_quy_doi
        · loai_chung_tu_id = LoaiChungTuLookup.idTheoMa("PBT")
        · status = NHAP           (ghi sổ hay không do bước 7 quyết định)
    luuEntity(ctx)              [BẮT BUỘC CÀI]
        · save PhieuKeToanTongHop (cascade: BuTruCongNo, dòng hạch toán,
          cặp ghép, ChungTuLienQuan)
        · ctx.ghiNhanChungTu(id, soChungTu, ngayChungTu, ngayHachToan)   ← BẮT BUỘC
                                          (ChungTuTemplate.java:428-435)
 6. sauKhiLuu(ctx)              [OVERRIDE]
        · dựng DinhKhoan cho từng dòng hạch toán, gắn voiChiTiet(id dòng)
          — id chỉ có SAU khi INSERT (ChungTuTemplate.java:326-331)
        · CHỈ khi ghiSoNgay: port.giamSoDu(...) + kiểm V19
 7. coGhiSoNgay(ctx)            [OVERRIDE] = lenh.ghiSoNgay()
    ├─ true  → phanGhiSo → ghiSoCai → GhiSoApi.ghiSo(...)   (kernel tự kiểm kỳ khoá)
    │          → entity.ghiSo()  ⇒ status = DA_GHI_SO, nguoi_ghi_so, thoi_gian_ghi_so
    └─ false → luuKhongGhiSo → kiemTraKyKeToan(ctx)          → V18
               (base ném IllegalStateException nếu đã dựng định khoản mà không ghi sổ
                — ChungTuTemplate.java:469-476 ⇒ bước 6 chỉ dựng DinhKhoan khi ghiSoNgay)
 8. ghiNhatKyTacDong(ctx)       [base]  aud_audit_log, TRONG transaction
 9. dangKyThongBaoSauCommit(ctx)[base]  không dùng (không gửi thông báo)
10. taoKetQua(ctx)              [BẮT BUỘC CÀI] → ChungTuBuTruDto
```

> ⚠️ **Bẫy ở bước 6/7:** `luuKhongGhiSo` ném `IllegalStateException` nếu context có định khoản mà `coGhiSoNgay = false` (`ChungTuTemplate.java:469-476`). ⇒ `sauKhiLuu` **chỉ** dựng `DinhKhoan` khi `lenh.ghiSoNgay()`. Nút "Lưu" thuần không sinh bút toán, không đụng công nợ — đúng `SCR_BTCN_ChungTu_ThemMoi.md:142`.

**Bảng gọi base / override / viết mới:**

| Bước | Trạng thái |
|---|---|
| 1, 8, 9, khoá, kiểm kỳ, ghi/gỡ sổ cái | ✅ **kế thừa nguyên** từ `ChungTuTemplate` |
| 2 `kiemTraQuyen` | 🔁 **override** (2 mã chức năng) |
| 3 `chuanBiChungTu`, 5 `truocKhiLuu`, 6 `sauKhiLuu`, 7 `coGhiSoNgay` | 🔁 **override** |
| 4 `kiemTraNghiepVu`, `luuEntity`, `taoKetQua`, `bangGoc`, `maChucNang`, `maLoaiChungTu` | 🆕 **bắt buộc cài** (`ChungTuTemplate.java:248-272`) |
| `PhanBoBuTru`, `GhepCapBuTru`, `ChenhLechTyGiaBuTru`, `KiemTraBuTru`, `DinhKhoanBuTru`, `BuTruCongNoMapper` | 🆕 **viết mới** ở `service/business/` |

Giá trị hằng của template:

| Hook | Giá trị | Bằng chứng |
|---|---|---|
| `bangGoc()` | `"ktth_phieu_ke_toan_tong_hop"` | `V202:35` |
| `maChucNang()` | `MaChucNang.BU_TRU_CONG_NO` = `"BuTruCongNo"` | `common/constant/MaChucNang.java:366` |
| `maLoaiChungTu()` | `"PBT"` | BR09 bảng mã · `TaiLieuMappingSoCai.md:1869` — **chưa seed**, xem [09 §5](09-thiet-ke-db.md) |
| `coSinhButToan()` | `true` (mặc định) | `ChungTuTemplate.java:597-599` |
| `coAnhHuongTonKho()` | `false` (mặc định) | `ChungTuTemplate.java:602-604` |
| `dienGiaiChung(ctx)` | `lyDo` của phiếu | `ChungTuTemplate.java:346-348` |

---

## 6. Định khoản gửi kernel (BR36, D10)

Với ví dụ lỗ tỷ giá của BA (`SCR_BTCN_ChungTu_ThemMoi.md:130-133`):

```java
// Dòng 1 — luôn có
DinhKhoan.cua(taiKhoanPhaiTraId, taiKhoanPhaiThuId, new BigDecimal("2450000.00"), "Bù trừ công nợ phải thu, phải trả")
    .voiChiTiet(idDongHachToan1)                    // BẮT BUỘC — DinhKhoan.java:17-21
    .voiDoiTuong(doiTuongBuTruId)                   // gắn CẢ 2 vế — TaiLieuMappingSoCai.md:1873
    .voiNgoaiTe(loaiTienId, tyGiaSuyRa, new BigDecimal("100.0000"));

// Dòng 2 — chỉ khi ngoại tệ lệch quy đổi
DinhKhoan.cua(taiKhoanLoCLTGId, taiKhoanPhaiThuId, new BigDecimal("50000.00"), "Xử lý chênh lệch tỷ giá")
    .voiChiTiet(idDongHachToan2)
    .voiDoiTuong(doiTuongBuTruId);                  // ⚠ R1 — xem dưới
    // KHÔNG voiNgoaiTe: soTienNguyenTe = 0, mà ButToanSoCai.java:41-43 / DinhKhoanValidator.java:90-93
    // yêu cầu số tiền nguyên tệ > 0 ⇒ dòng 2 là bút toán VND thuần
```

**Bốn điểm phải nhớ:**

1. `soTien` của `DinhKhoan` là **số đã quy đổi** (`DinhKhoan.java:71-74`), phần nguyên tệ đi kèm qua `voiNgoaiTe` — trùng quy ước ở `docs/be-khung-kien-truc-chuan.md:279-281`.
2. `soTien` phải **> 0** (`DinhKhoanValidator.java:73-76`) ⇒ dòng 2 chỉ dựng khi `chenhLech > 0`.
3. Hai định khoản khác `chiTietChungTuId` nên **không** đụng khoá idempotency. Khoá thật (đã kiểm): `uq_acc_so_cai_idempotency UNIQUE (tenant_id, chung_tu_id, chi_tiet_chung_tu_id, tai_khoan_id, tai_khoan_doi_ung_id, ngay_hach_toan)` — `V1__baseline.sql:4065`; `DinhKhoanValidator.kiemTraTrungKhoa` chặn sớm ca đụng khoá này (`DinhKhoanValidator.java:98-110`).
   > ⚠️ `acc_so_cai` **phân vùng theo năm**: `acc_so_cai_2024 … acc_so_cai_2028` (`V1__baseline.sql:2838-2860`) **cộng một partition `_default`** (`:2873`). Chứng từ có `ngay_hach_toan` ngoài 2024–2028 vẫn ghi được, rơi vào `_default` — không phải lỗi, nhưng nên biết khi đọc kế hoạch dung lượng.
4. **R1 — đối tượng ở dòng 2:** kernel gán **cùng** `doiTuongId` cho cả vế Nợ lẫn vế Có (`accounting_core/hach_toan/internal/ghi_so/GhiSoService.java:152,158`), trong khi mapping yêu cầu dòng chênh lệch **chỉ** gắn đối tượng ở phía tài khoản công nợ, phía 635/515 **không** gắn (`TaiLieuMappingSoCai.md:1875`). Không có đường nào phân biệt bằng API hiện tại ⇒ **Q9**. Ba lựa chọn ở [00 §9 R1](00-ke-hoach-tong.md).

**Mapping sang `acc_so_cai`** (`TaiLieuMappingSoCai.md:1862-1876`): giống mục "Phiếu kế toán tổng hợp (hạch toán)", khác 2 điểm — `LoaiChungTu = PBT`, `MaDoiTuongId = BuTruCongNo.DoiTuongId` (thay cho `ChiTietPhieuKTTH_HachToan.DoiTuongNoId`). Kernel tách mỗi `DinhKhoan` thành đúng 2 dòng sổ cái, **không gộp** (BR36 · `DinhKhoan.java:9-13`).

---

## 7. Tương tranh & transaction

| Khía cạnh | Quyết định | Bằng chứng |
|---|---|---|
| Ranh giới transaction | Đúng **một** `@Transactional` ở `ChungTuTemplate.thucThi` — bao cả lưu, giảm công nợ và ghi sổ cái | `ChungTuTemplate.java:102`, `GhiSoApi.java:9-14` (`Propagation.MANDATORY`) |
| Khoá chứng từ bù trừ | **Không** ở luồng TAO — "bản ghi chưa tồn tại nên không ai tranh chấp được id vừa sinh" | `ChungTuTemplate.java:141-143` |
| Khoá chứng từ **gốc** | **Có** — `port.giamSoDu` phải `SELECT … FOR UPDATE` theo `ORDER BY id` trước khi trừ | Cùng khuôn `QuanHeChungTuApi.java:25-27`; thứ tự cố định để tránh deadlock |
| Optimistic lock | `phien_ban` trên `PhieuKeToanTongHop` và trên chứng từ gốc; lệch → 409 `STALE_DATA` | `ChungTuTemplate.java:370-374` |
| Chống trùng số chứng từ | Unique partial index; bắt `DataIntegrityViolationException` → `MSG_..._015` | `V202:70-74` |
| Idempotency ghi sổ | Kernel idempotent theo nội dung: gọi lại cùng nội dung không sinh dòng mới; nội dung khác → 409 `POSTING_PAYLOAD_MISMATCH` | `GhiSoApi.java:20-28` |
| Nhật ký kiểm toán | Ghi **trong** transaction (nguyên tử với dữ liệu) | `ChungTuTemplate.java:521-530` |

**Cửa sổ đua thực tế:** A6 (xem trước) → người dùng nhập số chứng từ → A7. Trong khoảng đó số dư chứng từ gốc có thể bị giao dịch khác dùng. ⇒ A7 nạp lại số dư dưới khoá và trả `MSG_..._018` nếu không đủ. Với **Lưu thuần** thì **không** kiểm số dư (chưa trừ công nợ) — đúng BA: "chứng từ vẫn được lưu ở trạng thái Chưa ghi sổ" (`UC_BTCN_ThemMoi.md:122`).

---

## 8. Phân trang · sắp xếp · lọc · dòng tổng

Không áp dụng — endpoint ghi.

---

## 9. Kiểm thử

### 9.1 Unit test (`@Tag("unit")`)

| Lớp test | Input → Kỳ vọng |
|---|---|
| `TaoChungTuBuTruTest` | `soChungTu = "   "` → 400 `MSG_..._014` (trim chạy trước — BR43) |
| `TaoChungTuBuTruTest` | `soChungTu` 51 ký tự → 400 (BR20.2) |
| `TaoChungTuBuTruTest` | `soChungTu` chứa "à" → 400 (BR20.2) |
| `TaoChungTuBuTruTest` | `lyDo` 501 ký tự → 400 |
| `TaoChungTuBuTruTest` | `ghiSoNgay=false` → **không** dựng `DinhKhoan` nào; `luuKhongGhiSo` không ném |
| `TaoChungTuBuTruTest` | `ghiSoNgay=true` nhưng thiếu `PhieuKeToan.Post` → 403 |
| `TaoChungTuBuTruTest` | `loai_phieu` luôn = `'Bù trừ công nợ'` dù client gửi giá trị khác |
| `TinhTongTienTest` | 2 dòng hạch toán (5.000.000 nguyên tệ + 0) → `tong_tien = 5.000.000` (F04-d) |
| `DinhKhoanBuTruTest` | Dòng 1 VND: `soTien` = tổng bù trừ, không `voiNgoaiTe` |
| `DinhKhoanBuTruTest` | Dòng 1 ngoại tệ: `soTien` = MIN quy đổi, `soTienNguyenTe` = tổng bù trừ, `tyGia` suy ra |
| `DinhKhoanBuTruTest` | Dòng 2: `soTien` = \|chênh lệch\|, **không** `voiNgoaiTe` |
| `DinhKhoanBuTruTest` | `chenhLech = 0` → **không** sinh dòng 2 |
| `DinhKhoanBuTruTest` | Mọi `DinhKhoan` đều có `chiTietChungTuId` ≠ null (`DinhKhoanValidator.java:63-65`) |
| `ThamChieuBuTruTest` | Một chứng từ xuất hiện ở 3 cặp ghép → chỉ **1** dòng `ktth_chung_tu_lien_quan` |

### 9.2 Test tích hợp (cần Docker)

| Lớp test | Kiểm gì |
|---|---|
| `LuuBuTruIT` | Lưu thuần → `status = NHAP`, `acc_so_cai` **rỗng**, số dư chứng từ gốc **không đổi** |
| `LuuBuTruIT` | Lưu và Ghi sổ → `status = DA_GHI_SO`, `acc_so_cai` có **2 dòng** (VND) hoặc **4 dòng** (ngoại tệ có chênh lệch), số dư gốc đã giảm, `trang_thai_thanh_toan` cập nhật |
| `LuuBuTruIT` | Số chứng từ trùng → 409 `MSG_..._015`, **không** bản ghi nào được lưu |
| `LuuBuTruIT` | Kỳ đã khoá + Lưu thuần → 409 `MSG_..._019` (BR17.1 chặn cả lưu nháp) |
| `LuuBuTruIT` | Kỳ đã khoá + Lưu và Ghi sổ → 409 `MSG_..._019` từ kernel |
| `LuuBuTruIT` | Số dư gốc bị giao dịch khác dùng hết giữa A6 và A7, `ghiSoNgay=true` → 409 `MSG_..._018`, **rollback sạch** |
| `LuuBuTruIT` | Lỗi ở bước ghi sổ → rollback: `ktth_phieu_ke_toan_tong_hop` không có dòng nào (V21) |
| `LuuBuTruIT` | `acc_so_cai.ma_doi_tuong_id` = đối tượng bù trừ ở **cả** dòng Nợ 331 và Có 131 (`TaiLieuMappingSoCai.md:1873`) |
| `LuuBuTruIT` | `acc_so_cai.loai_chung_tu_id` = id của `PBT` |
| `LuuBuTruIT` | Cascade: xoá cứng phiếu trong test → con bị xoá theo (kiểm `orphanRemoval`) |
| `LuuBuTruSchemaIT` | **R9** — đọc/ghi thật cả 5 entity, bắt lỗi lệch tên cột |

---

## 10. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR7 | §3.1 `ty_gia` 6 chữ số, tiền 2/4 chữ số; §6 làm tròn quy đổi |
| BR09 | `maLoaiChungTu() = "PBT"` |
| BR12 | `status` `NHAP` → `DA_GHI_SO`; ghi sổ duy nhất một lần (idempotency kernel) |
| BR13.2 | Nút Lưu / Lưu và Ghi sổ → cờ `ghiSoNgay` |
| BR15.1/15.2 | §4 V4–V8 |
| BR16 | `MSG_..._018` cảnh báo số dư đổi |
| BR17.1 | §4 V18 — chặn cả **lưu nháp** vào kỳ khoá (`ChungTuTemplate.java:145-147`) |
| BR18 | §6 quy đổi + `voiNgoaiTe` |
| BR19.1 | §4 V6 chống trùng số chứng từ theo tenant |
| BR20.2 | §4 V5 độ dài 50, không dấu tiếng Việt |
| BR25 | §4 V1, V2 |
| BR28 | `tenant_id` do base, RLS ở DB |
| BR36 | §6 không gộp bút toán — mỗi dòng hạch toán một `DinhKhoan` |
| BR37 | **Luật FE** — ghi rõ ở §4 |
| BR41 | Tham chiếu §3.5 (ngoại lệ theo **Q7**) |
| BR43 | §4 V3 trim trước mọi kiểm |
| BR46 | Trường hệ thống do `BaseChungTuEntity` + `SoftDeletableEntity`; `nguoi_ghi_so`/`thoi_gian_ghi_so` do `entity.ghiSo()` |

**Chưa áp được:** BR21 (tab Chứng từ công nợ chỉ xem — không có thêm/xóa dòng), BR34 (không có luồng sửa từ màn xem — BA cấm), BR14.2 (không có nút "Lưu và Thêm mới" trong BA).
