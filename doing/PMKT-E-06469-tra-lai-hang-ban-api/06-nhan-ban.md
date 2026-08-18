# F6 — Nhân bản chứng từ trả lại hàng bán

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F6** |
| UC nguồn | `PMKT-U-06474` — `4.usecases/PMKT-U-06474_NhanBan/UC_NhanBanTraLaiHangBan.md` + `AD_NhanBan.puml` |
| Màn hình | mở popup `SCR_SuaTraLaiHangBan` với dữ liệu đã fill (`UC:297`) |
| Endpoint phụ trách | **A11** `GET /{id}/nhan-ban` (+ **A7** `POST /` để lưu thật) |
| Quyền | `TraLaiHangBan.Clone` — đã seed (`db/seed/iam_quyen_full_639_ba.sql:657`) |

## 1. Quyết định riêng

| # | Quyết định | Trỏ về |
|---|---|---|
| 1.1 | **`GET`, không `POST`** — thao tác này KHÔNG ghi gì vào DB | `BaseChungTuController.java:112-125` |
| 1.2 | Không đi qua `ChungTuTemplate` — template cưỡng chế trình tự **ghi** chứng từ, nhân bản không ghi | `NhanBanChungTuBanHang.java:12-16` |
| 1.3 | Quyền là **`.Clone`** (không phải `.Create`) — base đã chốt | `BaseChungTuController.java:121`; `QuyenChecker.java:43` |
| 1.4 | Bản ghi nạp về **phải TÁCH khỏi persistence context** trước khi sửa | §5 — lỗi này xoá mất số chứng từ của bản gốc |
| 1.5 | UC nói *"Hệ thống tạo bản sao … sinh số chứng từ mới"* (`UC:295-296`) nhưng BE **để trống** số chứng từ; số cấp thật lúc bấm Lưu | §4 |

---

## 2. Hợp đồng API

### A11 — `GET /api/ban-hang/tra-lai-hang-ban/{id}/nhan-ban`

Quyền: `TraLaiHangBan.Clone`.

```jsonc
// Response 200 — ApiResponse<TraLaiHangBanDto>, KHÔNG ghi DB
{
  "data": {
    "id": null,                        // ← chưa tồn tại
    "soChungTu": null,                 // ← cấp lúc Lưu (1.5)
    "ngayChungTu": "2026-08-14",       // ← ngày hiện tại (UC:296)
    "ngayHachToan": "2026-08-14",
    "trangThaiChungTu": "NHAP",        // ← luôn "Chưa ghi sổ" kể cả bản gốc đã ghi sổ

    /* ── SAO CHÉP (UC:276) ─────────────────────────────── */
    "phuongThucLapHoaDon": "Người bán xuất hóa đơn điều chỉnh",
    "thanhToanNgay": false, "phuongThucThanhToan": null,
    "kiemPhieuNhapKho": true, "lapKemHoaDonDieuChinh": true,
    "khachHangId": "a1b2…", "tenKhachHang": "Công ty TNHH A",
    "maSoThue": "0101234567", "diaChi": "12 Trần Duy Hưng, Hà Nội",
    "nhanVienBanHangId": "b7c8…", "moTa": "Trả lại hàng bán cho Công ty TNHH A",
    "loaiTienId": "vnd0…", "tyGia": 1.000000,
    "loaiChietKhau": "Không chiết khấu", "phanTramChietKhau": 0.00,
    "loaiDieuChinh": "Trả lại hàng bán", "lyDoDieuChinh": "Hàng sai quy cách",
    "nguonChungTu": "Chứng từ bán hàng hóa, dịch vụ",
    "chungTuBanHangId": "aa11…",

    /* ── KHÔNG sao chép (UC:277) ───────────────────────── */
    "mauSoHoaDon": null, "kyHieuHoaDon": null, "soHoaDon": null, "ngayHoaDon": null,
    "hoaDonCanDieuChinhId": null, "hoaDonBanHangId": null,
    "soPhieuNhapKho": null, "soPhieuChi": null,

    /* ── Chi tiết: sao chép, id dòng = null ────────────── */
    "chiTiet": [
      { "id": null, "thuTu": 1, "maHangId": "vt01…", "tenHang": "Bàn gỗ A",
        "soLuong": 2.000, "donGia": 5000000.00, "thanhTien": 10000000.00,
        "taiKhoanTraLaiId": "tk5212…", "taiKhoanCongNoId": "tk131…",
        "chiTietChungTuBanHangId": "ct01…",     // ← xem §3 cảnh báo
        "soChungTuBanHang": "CTBH-000201", "soHoaDon": null }
    ],

    /* ── Trường hệ thống: rỗng hết ─────────────────────── */
    "phienBan": null, "createdBy": null, "createdAt": null,
    "updatedBy": null, "updatedAt": null
  },
  "message": "Nhân bản chứng từ trả lại hàng bán thành công",
  "messageId": null                    // ← epic KHÔNG cấp mã cho nhân bản, xem §7
}
```

| code | HTTP | messageId | Khi nào |
|---|---|---|---|
| `FORBIDDEN` | 403 | `_007` | thiếu `TraLaiHangBan.Clone` |
| `NOT_FOUND` | 404 | `_008` | `id` không có / `da_xoa = true` |

**Không có lỗi nghiệp vụ nào khác** — nhân bản được từ chứng từ **ở mọi trạng thái**, kể cả `DA_GHI_SO` (`AbstractChungTuCrudService.java:57-61`; `UC:288` chỉ đòi quyền "Thêm mới").

---

## 3. Ánh xạ trường: sao chép ⇄ không sao chép

Nguồn: `UC_NhanBanTraLaiHangBan.md:276-279`.

| Nhóm | Nguyên văn UC | Field | BE làm gì |
|---|---|---|---|
| **Sao chép** | *"Toàn bộ thông tin chứng từ (Phương thức lập hóa đơn, Hình thức thanh toán, Loại tiền, Tỷ giá, Chi tiết hàng hóa, Hạch toán, Tham chiếu)"* | tất cả field nghiệp vụ | copy nguyên |
| **KHÔNG sao chép** | *"Số chứng từ (sẽ tự động sinh mới), các thông tin liên quan đến hóa đơn (Mẫu số, Ký hiệu, Số hóa đơn, Ngày hóa đơn)"* | `soChungTu` · `mauSoHoaDon` · `kyHieuHoaDon` · `soHoaDon` · `ngayHoaDon` | về `null` |
| **Ngày chứng từ** | *"đặt ngày chứng từ là ngày hiện tại"* (`UC:296`) | `ngayChungTu` · `ngayHachToan` | `LocalDate.now(clock)` |
| **Trạng thái** | *"Trạng thái chứng từ mới: 'Chưa ghi sổ'"* (`UC:279`) | `status` | `NHAP`; `nguoiGhiSo`/`thoiGianGhiSo` về `null` |
| **Định danh + audit** | (base) | `id` · `phienBan` · 7 trường audit · `id` của từng dòng | `null` |
| **Chứng từ con** | suy từ "không sao chép thông tin hóa đơn" + D6 | `phieuNhapKhoId` · `phieuChiId` · `dieuChinhHoaDonBanHangId` · `hoaDonCanDieuChinhId` · `hoaDonBanHangId` | `null` — bản sao **chưa** có bộ chứng từ nào |

> ⚠️ **`chiTietChungTuBanHangId` — điểm cần BA xác nhận, không tự quyết.**
> UC nói sao chép *"Tham chiếu"*, tức giữ liên kết về dòng bán hàng gốc. Nhưng nếu giữ, bấm Lưu bản sao sẽ **cộng thêm** số lượng trả lại vào cùng dòng gốc và rất dễ vượt `Σ tiêu thụ ≤ SL nguồn` → 400 `_107` ngay ([03 §4](03-them-moi.md) V10). Đây chính là mục đích của ràng buộc, nhưng nghĩa là **nhân bản một chứng từ trả lại toàn phần sẽ luôn lỗi khi Lưu**.
> **Xử lý tạm:** GIỮ `chiTietChungTuBanHangId` (đúng nguyên văn "sao chép Tham chiếu") và để V10 chặn ở bước Lưu với thông báo `_107` đọc được — người dùng tự sửa số lượng hoặc bỏ liên kết. **Bổ sung câu hỏi vào §12 của file gốc** nếu BA muốn hành vi khác (vd bỏ liên kết khi nhân bản).

---

## 4. Về "sinh số chứng từ mới"

`UC:296` — *"Hệ thống sinh số chứng từ mới"*; `UC:278` — *"Số chứng từ mới được sinh theo quy tắc sinh số chứng từ"*.

BE **trả `soChungTu = null`**, không cấp số ở A11. Lý do (nguyên văn `AbstractChungTuCrudService.java:52-56` và `NhanBanChungTuBanHang.java:14-16`):

> *"Người dùng bấm 'Nhân bản' rồi đóng form là chuyện thường; tạo bản ghi ngay lúc bấm sẽ để lại chứng từ rác phải xoá tay, và chứng từ rác đó đã chiếm một số chứng từ trong quyển số"* — cấp số cũng vậy: bộ đếm `mst_quyen_chung_tu` tăng bằng `SELECT … FOR UPDATE` và **rollback theo transaction** (`ChungTuTemplate.java:316-321`). A11 là `GET` chỉ đọc, không có transaction ghi để rollback ⇒ mỗi lần bấm Nhân bản rồi đổi ý sẽ để lại một lỗ hổng số mà kế toán phải giải trình.

Số thật cấp ở **A7** khi người dùng bấm Lưu ([03 §1.4](03-them-moi.md)). FE hiển thị ô Số chứng từ trống — đúng như popup Thêm mới.

> Nếu BA yêu cầu **hiển thị trước** số dự kiến: phải thêm một API "xem số tiếp theo" **không tăng bộ đếm** (peek). Đó là thay đổi ở `SoChungTuApi`, ngoài phạm vi epic ⇒ ghi vào báo cáo, không tự làm.

---

## 5. Luồng xử lý — `NhanBanTraLaiHangBan` (`@Component`, KHÔNG extends template)

```java
@Transactional(readOnly = true)
public TraLaiHangBanDto thucThi(UUID id) {
    ChungTuTraLaiHangBan banNhap = tl.napTachRoi(id);   // 1
    banNhap.datLaiThanhBanNhap();                        // 2
    return tl.mapper().toDto(banNhap);                   // 3
}
```
Mẫu 1:1 `NhanBanChungTuBanHang.java:33-39`.

**Bước 1 — `napTachRoi(id)`: bước quan trọng nhất.** Bản ghi nạp về phải **TÁCH khỏi persistence context** trước khi sửa, nếu không Hibernate dirty-check và **ghi đè chính chứng từ gốc** — nghĩa là bấm "Nhân bản" sẽ **xoá mất số chứng từ của bản gốc** (nguyên văn `NhanBanChungTuBanHang.java:18-23`).
Việc tách nằm ở **repository** (`TraLaiHangBanRepository.napTachRoi` → `entityManager.detach(...)`), không ở lớp nghiệp vụ: nó là thao tác với persistence context, và để ở đó thì lớp nghiệp vụ không phải cầm `EntityManager` — cũng có nghĩa là không ai lỡ tay sửa thứ tự "tách rồi mới đổi field".
`napTachRoi` dùng **cùng một chính sách lỗi 404** với `nap` để hai đường nạp không trả hai mã lỗi khác nhau cho cùng một chứng từ (`BanHangSupport.java:93-103`).

**Bước 2 — `datLaiThanhBanNhap()`** trên entity: đặt về `null`/mặc định đúng danh sách §3. Đặt **trên entity** (không ở mapper) vì đó là hành vi vòng đời của chính chứng từ, và để có **một** chỗ duy nhất phải sửa khi thêm cột mới.

**Bước 3 — `toDto`** dùng chung mapper với A4 ⇒ FE nhận đúng shape đang đọc, chỉ khác là `id = null`.

> **Vì sao KHÔNG dùng `ChungTuTemplate`** (1.2): template cưỡng chế `kiemTraDauVao → kiemTraQuyen → chuanBiChungTu → luu…`, và mọi luồng đều `@Transactional` ghi. Nhân bản không ghi gì, không có `luuEntity` để cài, không có bút toán để sinh. Nhét vào template chỉ để "cho đồng bộ" là ép một thao tác đọc đi qua 12 bước ghi.

---

## 6. Tương tranh & transaction

| Việc | Cơ chế |
|---|---|
| Transaction | `@Transactional(readOnly = true)` — **bắt buộc** dù chỉ đọc: `TenantRlsAspect` bind GUC `app.tenant_id` theo transaction, thiếu nó RLS trả tập rỗng và chứng từ có thật cũng thành 404 (`AbstractChungTuCrudService.java:81-83`) |
| Khoá | **không** — chỉ đọc |
| Idempotency | tuyệt đối: gọi 100 lần không đổi gì trong DB |
| Ghi DB | **KHÔNG được có** — xem test §7 |

---

## 7. Về `messageId` của nhân bản

`6.messages.md` của epic có 35 mã, **không có mã nào cho nhân bản**. Base rơi về `ThaoTacChungTu.NHAN_BAN.messageIdMacDinh()` = mã chung `MSG_CORE_CT_*`.

Đúng cách xử lý, và đã có tiền lệ nguyên văn ở `ChungTuBanHangController.java:107-113`:

> *"Nhân bản KHÔNG có mã riêng: epic chưa có use case nhân bản nên `6.messages.md` không cấp mã nào. Rơi về mã chung của base là đúng — bịa một mã `MSG_PMKT-E-06194_xxx` ở đây sẽ là mã FE không bao giờ tra được trong tài liệu."*

⇒ `messageId(ThaoTacChungTu)` của controller này: `case NHAN_BAN -> super.messageId(thaoTac);`

---

## 8. Kiểm thử

### 8.1 Unit

| Lớp test | Case | Input → kỳ vọng |
|---|---|---|
| `NhanBanTraLaiHangBanTest` | **không ghi DB** | verify `repository.save*` **never**; chỉ `napTachRoi` được gọi |
| | tách khỏi context | verify gọi `napTachRoi`, **không** gọi `nap` (bản gốc không bị dirty-check) |
| | reset định danh | `id`, `phienBan`, 7 trường audit, `id` từng dòng == `null` |
| | reset số/ngày | `soChungTu == null`; `ngayChungTu == ngayHachToan == LocalDate.now(clock)` |
| | reset trạng thái | bản gốc `DA_GHI_SO` → bản sao `NHAP`, `nguoiGhiSo`/`thoiGianGhiSo` `null` |
| | reset hóa đơn | 4 field hóa đơn + `hoaDonCanDieuChinhId` + `hoaDonBanHangId` == `null` |
| | reset chứng từ con | `phieuNhapKhoId`, `phieuChiId`, `dieuChinhHoaDonBanHangId` == `null` |
| | giữ trường nghiệp vụ | `khachHangId`, `loaiTienId`, `tyGia`, `loaiChietKhau`, số dòng chi tiết, `soLuong`, `donGia` **giữ nguyên** |
| | giữ liên kết gốc | `chiTietChungTuBanHangId` **giữ** (§3 cảnh báo) |
| | 404 | `da_xoa = true` → 404 `_008`, **cùng mã** với `nap` |
| `TraLaiHangBanControllerTest` | quyền | thiếu `.Clone` → 403 (**không** phải `.Create`) |
| | messageId | `NHAN_BAN` → mã chung của base, **không** phải mã `MSG_PMKT-E-06469_*` |
| `ClockConfigTest` (đã có) | `LocalDate.now(clock)` | dùng `Clock` bean, **không** `LocalDate.now()` trần — lint P0-D13 cấm đọc đồng hồ tường trong mã nghiệp vụ (`BaseChungTuEntity.java:121-122`) |

### 8.2 Tích hợp (cần Docker — chưa chạy được)

| Lớp | Kiểm gì |
|---|---|
| `NhanBanTraLaiHangBanIT` | **bản gốc không đổi một cột nào** sau khi gọi A11 (so `ngay_cap_nhat`, `phien_ban`, `so_chung_tu` trước/sau) — chốt chặn của bẫy 1.4 |
| | bộ đếm `mst_quyen_chung_tu.so_hien_tai` **không tăng** (§4) |
| | `aud_audit_log` **không** có dòng mới |
| | A11 rồi A7 với payload trả về → chứng từ mới có số mới, bản gốc vẫn nguyên |
| | A11 trên chứng từ `DA_GHI_SO` → 200 (không chặn) |

---

## 9. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR12 trạng thái | §3 — bản sao luôn `NHAP` |
| BR13.1 nút thao tác | nút Nhân bản hiện ở **mọi** trạng thái (`SCR_XemChiTiet:19-21` cho cả Chưa và Đã ghi sổ) |
| BR14.1 chế độ form | FE mở popup ở chế độ `clone` (`IMPLEMENT.md:199`); BE chỉ cấp dữ liệu |
| BR20 số chứng từ | §4 — cấp lúc Lưu, không cấp ở A11 |
| BR25 phân quyền | quyền `.Clone` (1.3) |
| BR28 multi-tenant | §6 — `@Transactional(readOnly)` để RLS hoạt động |
| BR29.1 xóa mềm | 404 với bản ghi `da_xoa` |
| BR46 trường hệ thống | §3 — reset về `null`, để base gán lại lúc Lưu |

**BR chưa đạt:** không có. **Điểm chờ BA:** hành vi của `chiTietChungTuBanHangId` khi nhân bản (§3) và có cần hiển thị trước số chứng từ dự kiến (§4).
