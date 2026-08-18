# F02 — Thiết lập điều kiện & Lấy dữ liệu chứng từ phải thu / phải trả

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F02** |
| Use case | **PMKT-U-14690** AC2 · Luồng chính bước 3–4 · `UC_BTCN_ThemMoi.md:16-17, 54-57` |
| Màn hình | `5.screens/SCR_BTCN_BuTru.md` — Header Filter + 2 bảng · BR01 |
| Ma trận ẩn/hiện | `Matrix/PMKT-E-14294_BuTruCongNo/SCR_BTCN_BuTru_MaTranAnHien.md` |
| Endpoint phụ trách | **A3** `POST /chung-tu-phai-thu` · **A4** `POST /chung-tu-phai-tra` · **A13** `GET /tai-khoan-cong-no` |
| Quyết định liên quan | **D4** (2 endpoint riêng), **D5** (SPI `ChungTuCongNoPort`) — [00 §0](00-ke-hoach-tong.md) |

---

## 1. Quyết định riêng của chức năng

| # | Quyết định | Lý do · vì sao không chọn cách kia |
|---|---|---|
| **F02-a** | **Hai endpoint riêng** cho hai bảng (D4) | Mỗi bảng có ô tìm kiếm riêng, dòng Tổng riêng, phân trang riêng (`SCR_BTCN_BuTru.md:40,45,71,76`). Một endpoint trả cả hai thì FE phải cắt trang phía client ⇒ vỡ BR1 |
| **F02-b** | Nguồn dữ liệu qua **SPI `ChungTuCongNoPort`**, mỗi module chứng từ tự cài (D5) | Số dư công nợ nằm trên bảng của module khác; chỉ chủ sở hữu bảng được ghi. **Không chọn** đọc thẳng `acc_so_cai`: sổ cái không có Số hóa đơn / Hạn thanh toán / Số chưa thu, và chỉ chứa dòng của chứng từ ĐÃ ghi sổ. **Không chọn** import entity của module khác: vi phạm ranh giới Modulith |
| **F02-c** | Gọi **song song** N port rồi **gộp + sắp xếp + cắt trang ở tầng service**, không đẩy phân trang xuống từng port | Sắp xếp là `NgayChungTu ASC, SoChungTu ASC` trên **hợp** của nhiều loại chứng từ (`SCR_BTCN_BuTru.md:44`). Phân trang từng port rồi ghép sẽ ra thứ tự sai. **Hệ quả phải nói thẳng:** mỗi port trả **toàn bộ** dòng thoả tiêu chí ⇒ có trần bảo vệ, xem §7 và **R-F02** |
| **F02-d** | A13 trả TK con của 131/331 bằng **native query** trên `mst_he_thong_tai_khoan` | Cùng khuôn `chung_tu_ban_hang/internal/repository/TraCuuDanhMucRepository.java:20-33` — "truy vấn theo TÊN BẢNG là hợp đồng ổn định hơn" so với import entity của `master_data` (vùng đóng băng) |
| **F02-e** | BE **không** giữ trạng thái phiên "đã bấm Lấy dữ liệu" | Stateless. `MSG_..._013` ("Vui lòng bấm Lấy dữ liệu") là luật FE; BE kiểm gián tiếp ở A6 bằng "danh sách chọn rỗng" — xem [03 §5](03-phan-bo-va-thuc-hien-bu-tru.md) |

---

## 2. Hợp đồng API

### 2.1 A13 — `GET /api/ke-toan-tong-hop/bu-tru-cong-no/tai-khoan-cong-no?chieu=PHAI_THU`

**Quyền:** `BuTruCongNo.Create`.

Phục vụ 2 dropdown "TK phải thu" / "TK phải trả" với giá trị mặc định theo BA:
> `SCR_BTCN_BuTru.md:29` — "131; nếu 131 có TK con thì TK con đầu tiên" · `:30` — "331; nếu 331 có TK con thì TK con đầu tiên"

```jsonc
// Response 200 — ApiResponse<List<TaiKhoanRefDto>> = { data, message, messageId }
// Shape đã kiểm: core/response/ApiResponse.java:21 (KHÔNG có code / timestamp)
{
  "data": [
    { "id": "…", "soTaiKhoan": "1311", "tenTaiKhoan": "Phải thu khách hàng trong nước",
      "laTkCongNo": true, "choPhepHachToan": true, "laMacDinh": true },
    { "id": "…", "soTaiKhoan": "1312", "tenTaiKhoan": "Phải thu khách hàng nước ngoài",
      "laTkCongNo": true, "choPhepHachToan": true, "laMacDinh": false }
  ],
  "message": null,
  "messageId": null
}
```

| Field | Kiểu | Ghi chú |
|---|---|---|
| `chieu` (query) | enum `PHAI_THU` \| `PHAI_TRA` | Bắt buộc. `PHAI_THU` → gốc `131`, `PHAI_TRA` → gốc `331` |
| `laMacDinh` | boolean | Server tính: TK con đầu tiên (theo `so_tai_khoan` ASC) nếu có con; nếu không có con thì chính TK gốc |
| `laTkCongNo` | boolean | Cột `mst_he_thong_tai_khoan.la_tk_cong_no` — trả ra để FE hiểu vì sao một TK bị loại |

**Điều kiện lọc (đã kiểm vòng 2 — §2.4-Đ5 ở [00](00-ke-hoach-tong.md)):**

| Điều kiện | Cột | Bằng chứng |
|---|---|---|
| Thuộc nhánh 131 / 331 | `so_tai_khoan LIKE '131%'` / `'331%'`, hoặc đệ quy theo `tk_cha_id` | `mst_he_thong_tai_khoan.tk_cha_id`, `.cap` (`V1__baseline.sql`, khối `CREATE TABLE public.mst_he_thong_tai_khoan`) |
| **Có theo dõi công nợ** | `la_tk_cong_no = true` | cột `la_tk_cong_no boolean NOT NULL DEFAULT false` — **đây chính là cờ BA nói tới** |
| Đang hoạt động | `trang_thai = 'ACTIVE'` | cùng hằng `TRANG_THAI_TAI_KHOAN_HOAT_DONG` ở `TraCuuDanhMucRepository.java:47` |
| Chưa xoá mềm | `da_xoa = false` | `TraCuuDanhMucRepository.java:65` dùng `da_xoa` cho chính bảng này (baseline khai `is_deleted`, đã được chuẩn hoá sau) |
| **Hạch toán được** (không phải TK cha) | `cho_phep_hach_toan = true` | cột `cho_phep_hach_toan boolean NOT NULL DEFAULT true`; `V1__baseline.sql:332` tự đặt `false` cho TK vừa có con |

> `SCR_BTCN_BuTru.md:29` nói TK phải thu chọn "từ danh sách tài khoản con **có theo dõi khách hàng**". Cột `la_tk_cong_no` là cờ chung "theo dõi công nợ", **không** phân biệt khách hàng với nhà cung cấp — việc phân biệt đến từ nhánh tài khoản (131 vs 331). Bảng còn có `doi_tuong_lien_quan varchar(20)` mô tả loại đối tượng gắn với tài khoản; nếu BA muốn lọc chặt hơn theo cột đó thì cần biết bộ giá trị hợp lệ của nó — nêu ở [00 §12](00-ke-hoach-tong.md).
>
> ⚠️ **Q16 (mới, vòng 2):** `mst_doi_tuong` có sẵn `tk_cong_no_phai_thu_id` / `tk_cong_no_phai_tra_id` — TK công nợ **riêng theo từng đối tượng**. Nếu đối tượng đã khai TK riêng mà màn bù trừ vẫn mặc định 131/331 thì rất dễ **không lấy được chứng từ nào**. Xem [00 §12-Q16](00-ke-hoach-tong.md).

### 2.2 A3 — `POST /api/ke-toan-tong-hop/bu-tru-cong-no/chung-tu-phai-thu`

**Quyền:** `BuTruCongNo.Create` (`UC_BTCN_ThemMoi.md:12`).

```jsonc
// Request
{
  "doiTuongId": "5f3a…",
  "taiKhoanCongNoId": "…",          // TK phải thu đã chọn
  "loaiTienId": "…",
  "ngayBuTru": "2026-08-11",
  "keyword": "HD-0012",             // "Tìm theo số chứng từ, số hóa đơn"
  "page": 1,
  "pageSize": 20
}
```

| Field | Kiểu | Bắt buộc | Ràng buộc | Nguồn BA |
|---|---|---|---|---|
| `doiTuongId` | UUID | **Y** | Tồn tại, đang hoạt động, **vừa là khách hàng vừa là NCC** | `SCR_BTCN_BuTru.md:28` |
| `taiKhoanCongNoId` | UUID | **Y** | Tồn tại, thuộc nhánh 131 | `SCR_BTCN_BuTru.md:29` |
| `loaiTienId` | UUID | **Y** | Tồn tại | `SCR_BTCN_BuTru.md:32` |
| `ngayBuTru` | date | **Y** | — (ràng buộc lọc theo ngày: **Q13**) | `SCR_BTCN_BuTru.md:31` |
| `keyword` | string | N | Tìm trên `soChungTu`, `soHoaDon` | `SCR_BTCN_BuTru.md:40` |
| `page` / `pageSize` | int | N | BR1 — mặc định 1 / 20 | BR1 |

Thiếu bất kỳ trường bắt buộc nào → **400** `MSG_PMKT-E-14294_006` kèm danh sách field vi phạm để FE highlight (`SCR_BTCN_BuTru.md:116`).

```jsonc
// Response 200 — PageResponse<DongCongNoDto>, KHÔNG bọc ApiResponse
// Shape đã kiểm: core/response/PageResponse.java:20-23
{
  "data": [
    {
      "chungTuId": "a1…",
      "loaiChungTu": "SAL_CHUNG_TU_BAN_HANG",
      "tenLoaiChungTu": "Chứng từ bán hàng",
      "ngayChungTu": "2026-07-02",
      "soChungTu": "PBH-000045",
      "soHoaDon": "HD-0012, HD-0013",     // dẫn xuất, có thể nhiều số — xem §4.3
      "hanThanhToan": "2026-08-02",
      "dienGiai": "Bán hàng hoá cho Công ty TNHH ABC",
      "tyGia": 25000.000000,
      "soTien": 400.0000,
      "soTienQuyDoi": 10000000.00,
      "soDuConLai": 320.0000,
      "soDuConLaiQuyDoi": 8000000.00,
      "phienBan": 4
    }
  ],
  "pagination": { "page": 1, "pageSize": 20, "totalItems": 12, "totalPages": 1 },
  "summary": {
    "soTien": 5200.0000, "soTienQuyDoi": 130000000.00,
    "soDuConLai": 3100.0000, "soDuConLaiQuyDoi": 77500000.00,
    "dongTienHachToan": false
  }
}
```

> `summary` là slot có sẵn của `PageResponse` (`core/response/PageResponse.java:20`) — dùng cho **dòng Tổng** của bảng (BR31) và cờ `dongTienHachToan`. Không phải field tự chế, không phải sửa `core` (§2.4-Đ2 ở [00](00-ke-hoach-tong.md)).

| Field response | Ý nghĩa BA | Ghi chú |
|---|---|---|
| `soDuConLai` | **"Số chưa thu"** ở bảng phải thu | Đặt tên trung tính vì cùng DTO dùng cho A4 ("Số còn nợ") — xem §4 |
| `soDuConLaiQuyDoi` | Số chưa thu quy đổi | = `soDuConLai × tyGia` (BR18.2), làm tròn BR7 |
| `soHoaDon` | Số hóa đơn | **Giá trị dẫn xuất**, có thể là nhiều số ngăn cách bởi `", "` — xem §4.3 |
| `phienBan` | `phien_ban` của chứng từ gốc | Dùng để phát hiện số dư đổi giữa Lưu và Ghi sổ (`MSG_..._018`) — xem [06 §7](06-ghi-so-bo-ghi-so.md) |
| `summary.dongTienHachToan` | `loaiTienId` có phải đồng tiền hạch toán không | Quyết định FE ẩn/hiện toàn bộ cột quy đổi (`SCR_BTCN_BuTru_MaTranAnHien.md:41-42, 48-49`) và BR18.4 |
| `summary.*` (4 cột tiền) | Dòng Tổng cuối bảng | BR31 — tính trên **toàn bộ** tập sau lọc, xem §8.4 |

**Lỗi** — body theo `ApiError` = `{ code, message, messageId, details }` (`core/shared/error/ApiError.java:11-15`); `details` mang danh sách `FieldIssue` để FE highlight:

| HTTP | `code` | `messageId` | Khi nào |
|---|---|---|---|
| 400 | `THIEU_TRUONG_BAT_BUOC` | `MSG_PMKT-E-14294_006` | Thiếu trường bắt buộc Header Filter |
| 403 | `FORBIDDEN` | `MSG_PMKT-E-14294_005` | Thiếu `BuTruCongNo.Create` |
| 404 | `KHONG_TIM_THAY` | — | `doiTuongId` / `taiKhoanCongNoId` / `loaiTienId` không tồn tại |

Không có chứng từ nào thoả → **200** với `noiDung: []`, `tongSo: 0`; FE hiển thị `MSG_PMKT-E-14294_201` "Không có dữ liệu" (`SCR_BTCN_BuTru.md:116`). **Không** trả 404.

### 2.3 A4 — `POST /api/ke-toan-tong-hop/bu-tru-cong-no/chung-tu-phai-tra`

Hợp đồng **giống hệt A3**, khác 3 điểm:
- `taiKhoanCongNoId` thuộc nhánh **331**;
- nguồn là chứng từ có dòng hạch toán bên **Có** TK phải trả (`SCR_BTCN_BuTru.md:73`);
- `soDuConLai` mang nghĩa **"Số còn nợ"** (`SCR_BTCN_BuTru.md:92`).

---

## 3. SPI `ChungTuCongNoPort` — hợp đồng với module chứng từ

Đặt ở `ke_toan_tong_hop/bu_tru_cong_no/api/` kèm `package-info.java` khai `@NamedInterface("bu-tru-cong-no")`; DTO ở `api/dto/` khai `@NamedInterface("bu-tru-cong-no-dto")` riêng — lộ `x.api` **không** tự động lộ `x.api.dto` (`cell-app/CLAUDE.md:38-40`).

```java
public interface ChungTuCongNoPort {

    /** Loại chứng từ mà bean này phục vụ — một bean một loại. */
    LoaiChungTuCongNo loai();

    /** Chiều công nợ: PHAI_THU (dòng Nợ TK 131) hay PHAI_TRA (dòng Có TK 331). */
    ChieuCongNo chieu();

    /**
     * Chứng từ còn số dư > 0 khớp tiêu chí. Trả TOÀN BỘ (không phân trang) —
     * service gộp nhiều port rồi mới sắp xếp + cắt trang (F02-c).
     */
    List<DongCongNoDto> timChungTuConNo(TieuChiCongNoDto tieuChi);

    /** Nạp lại theo id — dùng lúc phân bổ / lưu / ghi sổ để kiểm số dư tại thời điểm đó. */
    List<DongCongNoDto> theoIds(Collection<UUID> chungTuIds);

    /** Trừ số dư khi GHI SỔ chứng từ bù trừ. Chạy trong transaction của người gọi. */
    void giamSoDu(List<LenhCapNhatCongNo> lenh);

    /** Hoàn trả số dư khi BỎ GHI. Idempotent. */
    void hoanTraSoDu(List<LenhCapNhatCongNo> lenh);
}
```

Chi tiết hợp đồng, ràng buộc transaction và bên cài đặt: [08-chan-bo-ghi-chung-tu-goc.md §3](08-chan-bo-ghi-chung-tu-goc.md).

**Bean cài đợt này (2/4 loại BA yêu cầu — xem R4, Q2):**

| Loại | Chiều | Module cài | Bảng nguồn |
|---|---|---|---|
| `SAL_CHUNG_TU_BAN_HANG` | `PHAI_THU` | `chung_tu_ban_hang` | `sal_chung_tu_ban_hang` + `sal_chi_tiet_chung_tu_ban_hang` |
| `PUR_CHUNG_TU_MUA_HANG` | `PHAI_TRA` | `chung_tu_mua_hang` | `pur_chung_tu_mua_hang` |

---

## 4. Ánh xạ cột: BA ↔ DB ↔ DTO

### 4.1 Bảng "Chứng từ phải thu" (`SCR_BTCN_BuTru.md:50-67`)

| # | Cột BA | Nguồn DB (Chứng từ bán hàng) | Field DTO | Ghi chú |
|---|---|---|---|---|
| 1 | Checkbox | — | — | FE giữ trạng thái tick |
| 2 | Ngày chứng từ | `sal_chung_tu_ban_hang.ngay_chung_tu` | `ngayChungTu` | Khoá sắp xếp 1 |
| 3 | Số chứng từ | `.so_chung_tu` | `soChungTu` | Hyperlink mở chứng từ gốc; khoá sắp xếp 2 |
| 4 | Số hóa đơn | ⚠ **KHÔNG có cột** trên `sal_chung_tu_ban_hang` — phải gom từ `sal_hoa_don_ban_hang.so_hoa_don` (`V77:48`) | `soHoaDon` | **Giá trị dẫn xuất** — xem §4.3 |
| 5 | Hạn thanh toán | `.han_thanh_toan` (`ChungTuBanHang.java:125-126`) | `hanThanhToan` | |
| 6 | Diễn giải | `.mo_ta` (`ChungTuBanHang.java:110-111`) | `dienGiai` | **Tên DB lệch tên BA** |
| 7 | Tỷ giá | `.ty_gia` (`ChungTuBanHang.java:134`) | `tyGia` | Chỉ hiện khi ≠ đồng tiền hạch toán (BR18.4) |
| 8 | Số tiền | `.tong_tien_thanh_toan` (`ChungTuBanHang.java:184`) | `soTien` | "Tổng số tiền phải thu theo chứng từ" |
| 9 | Số tiền quy đổi | `.tong_tien_thanh_toan_quy_doi` (`ChungTuBanHang.java:211`) | `soTienQuyDoi` | |
| 10 | **Số chưa thu** | ⚠ **Q5** — hoặc `tong_tien_thanh_toan − so_tien_da_thanh_toan` (`ChungTuBanHang.java:184,214`), hoặc `Σ sal_chi_tiet_chung_tu_ban_hang.so_con_no_nt` (`V163:27`) | `soDuConLai` | **Chưa có code nào đọc/ghi cột per-line** — R2 |
| 11 | Số chưa thu quy đổi | như trên, cột `…_quy_doi` / `so_con_no_vnd` | `soDuConLaiQuyDoi` | |
| 12 | Số tiền bù trừ | — | *(FE/A5)* | Không thuộc endpoint này — xem [03](03-phan-bo-va-thuc-hien-bu-tru.md) |
| 13 | Loại chứng từ | — | `loaiChungTu` + `tenLoaiChungTu` | Theo BR09 (`business_rules.md` bảng mã) |

### 4.2 Bảng "Chứng từ phải trả" (`SCR_BTCN_BuTru.md:81-97`)

| # | Cột BA | Nguồn DB (Chứng từ mua hàng) | Field DTO | Ghi chú |
|---|---|---|---|---|
| 5 | Hạn thanh toán | `pur_chung_tu_mua_hang.han_thanh_toan` (`ChungTuMuaHang.java:113-114`) | `hanThanhToan` | |
| 6 | Diễn giải | `.dien_giai` (`ChungTuMuaHang.java:95-96`) | `dienGiai` | Bán hàng dùng `mo_ta`, mua hàng dùng `dien_giai` — **hai module lệch tên cột**, port che khác biệt này |
| 7 | Tỷ giá | `.ty_gia` (`ChungTuMuaHang.java:104`) | `tyGia` | |
| 8 | Số tiền | `.tong_no_phai_tra_vnd` (`ChungTuMuaHang.java:151`) | `soTien` | ⚠ tên cột có hậu tố `_vnd` nhưng là "Tổng nợ phải trả gốc lúc ghi sổ" |
| 10 | **Số còn nợ** | `.so_con_no_vnd` (`ChungTuMuaHang.java:155-156`) | `soDuConLaiQuyDoi` | |
| 11 | Số còn nợ (nguyên tệ) | `pur_chung_tu_mua_hang.so_con_no_nt` (`V154:18`) — **entity CHƯA map** | `soDuConLai` | **R3 — phải bù `@Column` trước khi làm F02** |
| 4 | Số hóa đơn | ⚠ **KHÔNG có cột** trên `pur_chung_tu_mua_hang` — đã có sẵn `@Formula` gom từ `pur_hoa_don_mua` (`ChungTuMuaHang.java:195-197`) | `soHoaDon` | **Dùng lại nguyên** `CongThucSql.SO_HOA_DON` — xem §4.3 |

### 4.3 "Số hóa đơn" là giá trị DẪN XUẤT, không phải cột (đính chính vòng 2 — §2.4-Đ4)

**Cả hai bảng chứng từ đều không có cột `so_hoa_don`.** Hóa đơn là một chứng từ **riêng**, lập sau và có thể gom nhiều chứng từ gốc:

| Chiều | Bảng hóa đơn | Đường nối tới chứng từ gốc |
|---|---|---|
| Phải trả (mua hàng) | `pur_hoa_don_mua.so_hoa_don` | `pur_hoa_don_mua.chung_tu_mua_hang_id` **hoặc** `pur_chi_tiet_hoa_don.chung_tu_mua_hang_id` |
| Phải thu (bán hàng) | `sal_hoa_don_ban_hang.so_hoa_don` (`V77:48`) | `sal_hoa_don_ban_hang.chung_tu_ban_hang_id` (`V77:130`) **hoặc** `sal_chi_tiet_hd_ban_hang.chi_tiet_chung_tu_ban_hang_id` (`V77:134`) |

**Mua hàng đã có lời giải sẵn — dùng lại, không viết mới.** `ChungTuMuaHang.soHoaDon` là `@Formula(CongThucSql.SO_HOA_DON)` (`ChungTuMuaHang.java:195-197`), và javadoc của hằng đó giải thích đúng cái bẫy:

> `CongThucSql.java:127-133` — *"Bảng `pur_chung_tu_mua_hang` **KHÔNG có cột `so_hoa_don`**. Phải gom từ `pur_hoa_don_mua` qua HAI đường, hợp bằng `or`: (1) `pur_hoa_don_mua.chung_tu_mua_hang_id` — liên kết trực tiếp, nhưng… CHỈ được điền khi hoá đơn gom đúng một chứng từ; (2) `pur_chi_tiet_hoa_don.chung_tu_mua_hang_id` — liên kết ở mức dòng, đúng cả khi một [hoá đơn gom nhiều chứng từ]"*

Công thức thật (`CongThucSql.java:145-156`) là `string_agg(distinct hd.so_hoa_don, ', ' order by hd.so_hoa_don)` ⇒ **một chứng từ có thể có NHIỀU số hóa đơn**, trả về dạng chuỗi ngăn cách `", "`.

**Hệ quả lên thiết kế:**

1. `DongCongNoDto.soHoaDon` là **`String` có thể chứa nhiều số**, không phải một số đơn — FE hiển thị nguyên chuỗi (BR44 truncate nếu dài).
2. Bảng cặp ghép lưu snapshot `so_hoa_don_phai_thu` / `so_hoa_don_phai_tra` cũng là **chuỗi gộp tại thời điểm bù trừ** ([09 §3.2](09-thiet-ke-db.md)).
3. `SCR_BTCN_ChungTu_ThemMoi.md:70,82` mô tả "Số hóa đơn" là **Hyperlink** "mở hóa đơn (nếu có)" — với nhiều hóa đơn thì **một link không đủ**. ⚠ **Cần BA xác nhận**: hiển thị link đầu tiên, hay danh sách link, hay bỏ link khi > 1 hóa đơn. Nêu ở [00 §12](00-ke-hoach-tong.md).
4. Port bán hàng phải viết một `@Formula` **tương đương** cho `sal_hoa_don_ban_hang`, hoặc gom bằng query riêng trong adapter. Đặt hằng SQL ở `chung_tu_ban_hang/internal/model/` theo đúng khuôn `CongThucSql`, **không** đặt ở module bù trừ (bảng `sal_*` thuộc module bán hàng).
5. Keyword "Tìm theo số chứng từ, số hóa đơn" (`SCR_BTCN_BuTru.md:40`) vì thế phải tìm **trên biểu thức dẫn xuất**, không trên cột — mua hàng đã khai `@Searchable(keyword = true)` ngay trên field `@Formula` (`ChungTuMuaHang.java:195`), làm y hệt cho bán hàng.

> ⚠️ **Bất đối xứng phải xử lý:** phía phải thu số dư (có thể) ở **cấp dòng**, phía phải trả ở **cấp header**. Bù trừ làm việc ở **cấp chứng từ** (`ldm-KTTH.puml:168,178` — `ChungTuPhaiThuId` / `ChungTuPhaiTraId` là id **chứng từ**). ⇒ Port phía bán hàng phải **cộng dồn số dư các dòng lên chứng từ** khi trả về, và khi trừ thì **phân bổ ngược xuống các dòng** theo thứ tự dòng. Ghi rõ ở [08 §3.2](08-chan-bo-ghi-chung-tu-goc.md). Nếu Q5 chốt dùng cặp header thì bất đối xứng biến mất.

---

## 5. Validation — ma trận đầy đủ

| # | Luật | Điều kiện | Thời điểm kiểm | Thông báo | BR nguồn |
|---|---|---|---|---|---|
| V1 | Có quyền | `BuTruCongNo.Create` | Đầu handler | 403 · `MSG_..._005` | BR25.2 · `UC_BTCN_ThemMoi.md:110` |
| V2 | Đủ trường bắt buộc | `doiTuongId`, `taiKhoanCongNoId`, `loaiTienId`, `ngayBuTru` ≠ null | `@Valid` trên request | 400 · `MSG_..._006` + danh sách field | BR15.1 · `SCR_BTCN_BuTru.md:116` |
| V3 | Đối tượng tồn tại & hoạt động | `mst_doi_tuong.da_xoa=false AND trang_thai=true` | Service, trước khi gọi port | 404 | `TraCuuDanhMucRepository.java:51-53` |
| V4 | Đối tượng **vừa là KH vừa là NCC** | `mst_doi_tuong.la_khach_hang = true AND la_nha_cung_cap = true` — **cột có thật, đã kiểm vòng 2** (§2.4-Đ6) | Service | 400 · **cần mã message riêng — chưa có trong `6.messages.md`** | `SCR_BTCN_BuTru.md:28` + `V1__baseline.sql` khối `CREATE TABLE public.mst_doi_tuong`. Nêu ở [00 §12](00-ke-hoach-tong.md) |
| V5 | TK công nợ hợp lệ | Đúng nhánh (`131*`/`331*`) **và** `la_tk_cong_no = true` **và** `cho_phep_hach_toan = true` **và** `trang_thai = 'ACTIVE'` — xem §2.1 | Service | 400 | `SCR_BTCN_BuTru.md:29-30` + cột thật trên `mst_he_thong_tai_khoan` |
| V6 | Loại tiền tồn tại | `mst_loai_tien` | Service | 404 | `SCR_BTCN_BuTru.md:32` |
| V7 | Trim keyword | Cắt khoảng trắng đầu/cuối trước khi tìm | Service | — | BR43 |
| V8 | `pageSize` whitelist | 10/20/50/100/200 | Service | Quy về 20 | BR1 |
| V9 | Chỉ chứng từ **đã ghi sổ** mới có công nợ | `status = DA_GHI_SO` ở port | Trong port | Lọc bỏ | Chứng từ chưa ghi sổ chưa phát sinh công nợ (BR12) |
| V10 | Số dư > 0 | `soDuConLai > 0` | Trong port | Lọc bỏ | `SCR_BTCN_BuTru.md:43,74` |
| V11 | Khớp loại tiền | `loai_tien_id` chứng từ = `loaiTienId` yêu cầu | Trong port | Lọc bỏ | `SCR_BTCN_BuTru.md:32` — "chỉ bù trừ các chứng từ cùng loại tiền" |
| V12 | Khớp tài khoản công nợ | Chứng từ hạch toán vào đúng TK đã chọn | Trong port | Lọc bỏ | `SCR_BTCN_BuTru.md:42,73` |
| V13 | Ngày hạch toán ≤ Ngày bù trừ | **Q13** — BA không nêu | Trong port | Lọc bỏ *(đề xuất)* | — |
| V14 | Loại trừ chứng từ đang tham gia bù trừ **đã ghi sổ** khác | Số dư đã bị trừ ⇒ V10 tự lọc | — | — | `SCR_BTCN_BuTru.md:43` — "Số tiền đã Bù trừ công nợ trước đó" nằm trong Số tiền đã thu |
| V15 | Loại trừ chứng từ đang nằm trong chứng từ bù trừ **CHƯA ghi sổ** | ⚠ Số dư **chưa** bị trừ ⇒ có thể bù trừ trùng | Service | **Chưa có luật BA** | **Xem §7 và [00 §12](00-ke-hoach-tong.md)** |
| V16 | Tenant | RLS ở DB | DB | — | BR28 |

> ⚠️ **V15 là lỗ hổng nghiệp vụ chưa được BA phủ.** BA nói khi Lưu thì "chưa cập nhật trạng thái thanh toán/số dư" (`SCR_BTCN_ChungTu_ThemMoi.md:142`), nhưng không nói chứng từ đang nằm trong một chứng từ bù trừ **chưa ghi sổ** có được lấy ra bù trừ lần nữa không. Hai chứng từ bù trừ chưa ghi sổ cùng dùng hết số dư của một chứng từ → chứng từ thứ hai ghi sổ sẽ bị `MSG_..._018`. Đó **có thể** là hành vi mong muốn (khớp đúng `MSG_..._018`), nhưng cần BA xác nhận thay vì để dev tự chọn.

---

## 6. Luồng xử lý

```
A3/A4  POST /chung-tu-phai-thu | /chung-tu-phai-tra
  1. quyen.require("BuTruCongNo", "Create")                       ← QuyenChecker.java:61
  2. @Valid request                                                → V2 → MSG_006
  3. KiemTraBuTru.kiemTraTieuChi(request)                          → V3…V6
  4. tieuChi = TieuChiCongNoDto(doiTuong, taiKhoan, loaiTien, ngayBuTru, keyword)
  5. ports.stream()
        .filter(p -> p.chieu() == chieu)                           ← chọn đúng nhóm port
        .map(p -> p.timChungTuConNo(tieuChi))                      → V9…V13 trong port
        .flatMap(...)                                              ← gộp nhiều loại chứng từ
  6. sort: ngayChungTu ASC, soChungTu ASC                          ← SCR_BTCN_BuTru.md:44,75
  7. tongCong = Σ toàn bộ tập (soTien, soTienQuyDoi, soDuConLai…)  ← BR31, TRƯỚC khi cắt trang
  8. cắt trang theo page/pageSize                                  ← BR1
  9. dongTienHachToan = (loaiTienId == đồng tiền hạch toán)        ← BR18.4
 10. trả PageResponse + tongCong + dongTienHachToan
```

**Bước gọi base / viết mới:**

| Bước | Base có sẵn? |
|---|---|
| 1 | ✅ `QuyenChecker.require` (`core/controller/QuyenChecker.java:61`) |
| 2 | ✅ Bean Validation + `GlobalExceptionHandler` |
| 3–9 | ❌ **viết mới** ở `bu_tru_cong_no/internal/service/` + `business/` |
| Đọc danh mục `mst_*` | ❌ viết mới `TraCuuDanhMucBuTruRepository` theo khuôn `TraCuuDanhMucRepository.java:42-60` |

---

## 7. Tương tranh & transaction

| Khía cạnh | Quyết định |
|---|---|
| Transaction | `@Transactional(readOnly = true, propagation = REQUIRED)`. Port khai `Propagation.MANDATORY` giống `TraCuuDanhMucRepository.java:37-41` — chạy ngoài transaction thì GUC tenant chưa bind và RLS trả tập rỗng "một cách khó hiểu" |
| Khoá | **Không khoá.** Đây là bước xem, số dư có thể đổi ngay sau đó — đúng lý do `MSG_..._018` tồn tại |
| Idempotency | Không áp dụng (chỉ đọc) |
| **Trần bảo vệ** | Vì port trả toàn bộ (F02-c), phải có hằng `private static final int GIOI_HAN_DONG_CONG_NO = 5_000;`. Vượt trần → trả 400 kèm gợi ý thu hẹp điều kiện, **không** cắt im lặng (`docs/_bieu-mau-plan-api.md` — "No silent caps"). **Cần BA/PO chốt con số** |

---

## 8. Phân trang · sắp xếp · lọc · dòng tổng

### 8.1 Bộ lọc
Toàn bộ đến từ Header Filter (đối tượng, TK công nợ, loại tiền, ngày bù trừ) — **bắt buộc**, không có mặc định BE bơm. Ô tìm kiếm phụ: `keyword` trên `soChungTu` + `soHoaDon` (`SCR_BTCN_BuTru.md:40,71`), không phân biệt hoa thường, có trim (BR11.1, BR43).

### 8.2 Sắp xếp
**Cố định** `NgayChungTu ASC`, cùng ngày → `SoChungTu ASC` (`SCR_BTCN_BuTru.md:44,75`). Người dùng **không** đổi được — BA không mô tả click header. Đây là **ghi đè BR2** (BR2 mặc định `NgayHachToan DESC`) trong phạm vi màn này; ghi rõ theo luật "epic thắng trong đúng phạm vi epic" của `CLAUDE.md`.

Thứ tự này còn là **đầu vào của thuật toán BR02** ("duyệt từ trên xuống" — `SCR_BTCN_BuTru.md:123`), nên nó là hợp đồng nghiệp vụ chứ không phải tuỳ chọn hiển thị. Xem [03 §6](03-phan-bo-va-thuc-hien-bu-tru.md).

### 8.3 Phân trang
BR1 — 1-based, mặc định 20, whitelist 10/20/50/100/200. Cắt trang **sau** khi gộp và sắp xếp (§6 bước 8).

> BA: "Trạng thái tick và Số tiền bù trừ của từng dòng được **giữ nguyên khi chuyển trang hoặc tìm kiếm**" (`SCR_BTCN_BuTru.md:46,77`). Đây là trách nhiệm **FE** (giữ map `chungTuId → soTienBuTru`); BE stateless. Nhưng nó là lý do A5/A6 nhận **danh sách id + số tiền đầy đủ** chứ không chỉ trang hiện tại — xem [03 §3](03-phan-bo-va-thuc-hien-bu-tru.md).

### 8.4 Dòng tổng (BR31)
Cộng các cột **Số tiền**, **Số chưa thu / Số còn nợ**, **Số tiền bù trừ** (`SCR_BTCN_BuTru.md:45,76`). Trong đó:
- `soTien`, `soDuConLai` (+ bản quy đổi) do BE trả trong **`PageResponse.summary`** — slot có sẵn của base (`core/response/PageResponse.java:20`, javadoc `:12-14` nói đúng mục đích "tổng footer TOÀN CỤC theo bộ lọc"), dựng bằng `PageResponse.of(page, pageNumber, summary)` (`:31-36`). **Không phải sửa `core`** (§2.4-Đ2 ở [00](00-ke-hoach-tong.md));
- Tính trên **toàn bộ tập sau lọc**, không phải trang hiện tại (BR31). Ở đây tập đã nằm sẵn trong bộ nhớ (F02-c gom toàn bộ trước khi cắt trang) nên cộng trực tiếp, **không** cần query `SUM` thứ hai;
- `Số tiền bù trừ` do **FE cộng** từ map lựa chọn của người dùng — BE không biết trạng thái tick ở endpoint này.

Kiểu `summary`: record riêng, vd `record TongCongNoDto(BigDecimal soTien, BigDecimal soTienQuyDoi, BigDecimal soDuConLai, BigDecimal soDuConLaiQuyDoi, boolean dongTienHachToan) {}` — base để `Object` chính là để mỗi màn gắn record riêng (`PageResponse.java:15-16`).

`SUM` trên tập rỗng trả `0`, không `null`. Ở đây **không có** vấn đề cộng lẫn nhiều loại tiền (khác [01 §8.4](01-danh-sach-chung-tu-bu-tru.md)) vì `loaiTienId` là **trường bắt buộc** của Header Filter — mọi dòng đã cùng một loại tiền.

---

## 9. Kiểm thử

### 9.1 Unit test (`@Tag("unit")`)

| Lớp test | Input → Kỳ vọng |
|---|---|
| `KiemTraBuTruTest` | Thiếu `doiTuongId` → `ApiException` 400 mã `MSG_..._006`, `chiTiet` chứa `"doiTuongId"` |
| `KiemTraBuTruTest` | TK phải thu là `3311` khi `chieu=PHAI_THU` → 400 |
| `GomDongCongNoTest` | 2 port trả (02/07 "B"), (02/07 "A"), (01/07 "C") → thứ tự C, A, B |
| `GomDongCongNoTest` | `summary` = Σ **toàn bộ 3 dòng**, kể cả khi `pageSize = 1` |
| `GomDongCongNoTest` | Tập rỗng → `summary` các cột = `0`, không `null` |
| `GomDongCongNoTest` | Vượt `GIOI_HAN_DONG_CONG_NO` → ném 400, **không** cắt im lặng |
| `QuyDoiTest` | `soDuConLai=320.0000`, `tyGia=25000.000000` → `soDuConLaiQuyDoi=8000000.00` (BR7, 2 chữ số) |
| `DongTienHachToanTest` | `loaiTienId` = đồng tiền hạch toán → `dongTienHachToan=true` |

### 9.2 Test tích hợp (cần Docker)

| Lớp test | Kiểm gì |
|---|---|
| `LayDuLieuCongNoIT` | Chứng từ bán hàng `status != DA_GHI_SO` **không** xuất hiện (V9) |
| `LayDuLieuCongNoIT` | Chứng từ đã thu hết (`soDuConLai = 0`) **không** xuất hiện (V10) |
| `LayDuLieuCongNoIT` | Chứng từ khác loại tiền **không** xuất hiện (V11) |
| `LayDuLieuCongNoIT` | Chứng từ của đối tượng khác **không** xuất hiện |
| `LayDuLieuCongNoIT` | `keyword` khớp `soHoaDon` **dẫn xuất** trả đúng dòng; có trim; không phân biệt hoa thường (§4.3) |
| `LayDuLieuCongNoIT` | RLS: tenant A không thấy chứng từ tenant B |
| `TaiKhoanCongNoIT` | `chieu=PHAI_THU` trả nhánh `131*`, `laMacDinh` đúng TK con đầu tiên |
| `TaiKhoanCongNoIT` | TK có `la_tk_cong_no = false` → **không** xuất hiện (§2.1) |
| `TaiKhoanCongNoIT` | TK cha (`cho_phep_hach_toan = false`) → **không** xuất hiện |
| `TaiKhoanCongNoIT` | TK `trang_thai <> 'ACTIVE'` → **không** xuất hiện |
| `LayDuLieuCongNoIT` | Đối tượng chỉ là khách hàng (`la_nha_cung_cap = false`) → 400 ở V4 |
| `ChungTuBanHangCongNoPortIT` | Port bán hàng cộng dồn số dư các dòng lên đúng cấp chứng từ (§4.2) |
| `ChungTuBanHangCongNoPortIT` | Chứng từ bán hàng có **2 hóa đơn** → `soHoaDon` = `"HD-0012, HD-0013"` (§4.3) |
| `ChungTuBanHangCongNoPortIT` | Chứng từ **chưa lập hóa đơn** → `soHoaDon = null`, dòng vẫn xuất hiện |
| `ChungTuMuaHangCongNoPortIT` | Port mua hàng trả **cả** `so_con_no_nt` và `so_con_no_vnd` (R3) |
| `ChungTuMuaHangCongNoPortIT` | `soHoaDon` khớp kết quả của `CongThucSql.SO_HOA_DON` qua **cả hai** đường nối (§4.3) |

---

## 10. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR1 | §8.3 phân trang 2 bảng |
| BR2 | **Bị epic ghi đè** ở §8.2 (sort `NgayChungTu ASC`) — ghi rõ đang lệch |
| BR7 | §4 quy đổi làm tròn 2 chữ số tiền / 6 chữ số tỷ giá |
| BR09 | `loaiChungTu` + `tenLoaiChungTu` theo bảng mã BR09 |
| BR11.1 | `keyword` trên `soChungTu`, `soHoaDon`; case-insensitive; trim |
| BR12 | V9 — chỉ chứng từ `DA_GHI_SO` mới có công nợ |
| BR15.1 | V2 — trường bắt buộc Header Filter |
| BR18.2 | Quy đổi = gốc × tỷ giá |
| BR18.4 | `dongTienHachToan` điều khiển ẩn/hiện cột quy đổi |
| BR25 | V1 `quyen.require` |
| BR28 | V16 RLS, port khai `MANDATORY` |
| BR31 | §8.4 dòng tổng trên toàn tập sau lọc |
| BR43 | V7 trim keyword |

**Chưa áp được:** BR5 (combogrid — FE), BR10 (chọn nguồn — không áp dụng), BR30 (ẩn/hiện cột — ngoài phạm vi), BR32/BR44 (FE).
