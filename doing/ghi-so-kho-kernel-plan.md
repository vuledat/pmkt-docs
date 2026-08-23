# Kernel GHI SỔ KHO — kế hoạch xây dựng `accounting_core/ton_kho`

> **Trạng thái:** `BẢN NHÁP CHỜ REVIEW`
> **Ngày cập nhật:** 2026-08-06
> **Người review cần có:** 1 BA (chốt §11) + 1 Dev BE (chốt §5, §6, §10)

| Mục | Nội dung |
|---|---|
| Mục tiêu | Dựng kernel ghi sổ kho ĐỐI XỨNG với kernel ghi sổ cái đang có (`accounting_core/hach_toan`) |
| Module BE | `cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/ton_kho/` (tạo mới) |
| Bảng DB | `acc_so_xuat_nhap_tong_hop` (đã có, V245 — thiếu cột idempotency) · `inv_ton_kho` (đã có, V69) · `inv_cau_hinh_ton_kho` (đã có, V152) |
| Migration | `V353` (bổ sung idempotency + chốt chặn cho sổ kho) |
| Không đụng | `master_data/**` (vùng đóng băng), engine tính giá xuất kho V71 |

---

## 0. Các quyết định đã chốt

| # | Quyết định | Hệ quả lên code |
|---|---|---|
| **D1** | Kernel nằm trong `accounting_core/ton_kho`, cấu trúc `api/` + `internal/` **sao chép đúng** `accounting_core/hach_toan` | Chứng từ chỉ thấy `GhiSoKhoApi`/`SoKhoApi`; `TonKhoRepository`, `SoKhoEntity` nằm trong `internal`, Modulith chặn import chéo |
| **D2** | Ghi sổ kho tác động **HAI** bảng trong một lệnh: `acc_so_xuat_nhap_tong_hop` (sổ chi tiết, append/xoá vật lý) + `inv_ton_kho` (số dư luân chuyển, cộng/trừ tại chỗ) | Kernel không thể "chỉ INSERT" như sổ cái — xem §3 và thuật toán §5 |
| **D3** | **Bỏ ghi sổ kho suy delta từ CHÍNH DÒNG SỔ đang gỡ**, không lấy từ `ctx.bienDongTonKho()` | `boGhiSoKho(chungTuId)` chỉ cần id; idempotent, và đúng cả khi chứng từ trên màn hình đã bị sửa khác lúc ghi sổ |
| **D4** | Tái dùng nguyên `ChungTuKhoaApi` (advisory lock theo `chungTuId`) và `KyKeToanApi` — KHÔNG tạo khoá/kiểm kỳ riêng cho kho | `GhiSoKhoService` inject 2 API sẵn có; hai kernel xếp hàng trên cùng một khoá nên "ghi sổ cái + ghi sổ kho" của một chứng từ luôn nguyên tử với nhau |
| **D5** | Mọi method GHI của kernel là `Propagation.MANDATORY` | Gọi ngoài transaction ném lỗi ngay; tồn kho không bao giờ commit tách khỏi chứng từ |
| **D6** | Kernel ghi `so_lo = ''` thay vì `NULL` khi vật tư không quản lý lô | Khoá idempotency của sổ kho là UNIQUE trên **cột trần** (không dùng `COALESCE`) — bắt buộc, vì bảng partition không nhận unique index dạng biểu thức/partial |
| **D7** | `BienDongTonKho` hiện tại (4 trường) bị thay bằng `ton_kho/api/dto/BienDongKho` giàu trường hơn | Xoá `chung_tu/model/BienDongTonKho.java`; đổi kiểu `ChungTuContext.bienDongTonKho()`. **Chi phí = 0** vì hôm nay chưa có caller nào (§2.1) |
| **D8** | Kernel **KHÔNG tính giá xuất kho**. Nó nhận `giaTri` do chứng từ đưa xuống | Engine BQ/FIFO (`inv_luot_tinh_gia_xuat_kho`, V71) là epic riêng, nối vào sau bằng cách chạy lại `ghiSoKho` |
| **D9** | Giá bình quân (`inv_ton_kho.gia_binh_quan`) được kernel tính lại **dẫn xuất** sau mỗi lần áp delta: `gia_tri_ton / so_luong_ton` | Là giá trị phái sinh cho màn hình tra cứu, KHÔNG phải nguồn của engine tính giá — engine V71 có bảng kết quả riêng |
| **D10** | Chặn tồn âm đọc `inv_cau_hinh_ton_kho.cho_phep_ton_kho_am` qua `CauHinhTonKhoApi` | Cột `iam_tenant.cho_phep_ton_kho_am` **đã bị gỡ** ở `V181` — chỉ còn một nguồn cấu hình |

> ⚠️ **Cảnh báo môi trường:** `ChungTuTemplate` đang có 4 khối `TODO`/code comment-out (dòng 141, 452, 415-416) do một luồng sửa khác đang dở. Đọc lại file ngay trước khi code PR-4.

---

## 1. Mục tiêu

### 1.1 Trong phạm vi

| # | Chức năng | Ghi chú |
|---|---|---|
| F1 | `GhiSoKhoApi.ghiSoKho(request)` — ghi sổ chi tiết XNT + áp tồn, idempotent theo vân tay nội dung | Đối xứng `GhiSoApi.ghiSo` |
| F2 | `GhiSoKhoApi.boGhiSoKho(chungTuId)` — đảo tồn + xoá vật lý dòng sổ, idempotent | Đối xứng `GhiSoApi.boGhiSo` |
| F3 | `GhiSoKhoApi.daGhiSoKho(chungTuId)` | Dùng cho `doiSoatVoiSoKho` (lưới an toàn của template) |
| F4 | `SoKhoApi.theoChungTu(chungTuId)` — cổng ĐỌC sổ XNT | Đối xứng `SoCaiApi` |
| F5 | `TonKhoApi.tonHienTai(...)` — đọc tồn theo (kho, vật tư, lô) | Chứng từ cần để kiểm nghiệp vụ TRƯỚC khi ghi (báo lỗi sớm cho FE) |
| F6 | Chặn tồn âm theo cấu hình tenant | `MSG_INV_GS_004` |
| F7 | Nối kernel vào `ChungTuTemplate` — 2 hook `apDungTonKho`/`hoanTacTonKho` có cài đặt mặc định | Chứng từ chỉ còn việc `ctx.themBienDongKho(...)` |
| F8 | Migration `V353`: cột `request_hash`, khoá idempotency, trigger immutable + period-guard cho `acc_so_xuat_nhap_tong_hop` | §6 |

### 1.2 NGOÀI phạm vi

- **Engine tính giá xuất kho** (BQ cuối kỳ / BQ tức thời / FIFO / đích danh) — `V71` đã dựng schema `inv_luot_tinh_gia_xuat_kho`, `inv_ket_qua_tinh_gia_xuat_kho`; là epic riêng (D8).
- **Module chứng từ kho** (Phiếu nhập kho, Phiếu xuất kho, Điều chuyển, Kiểm kê) — schema có từ V69–V74, V232 nhưng **chưa có code Java**. Kernel này là điều kiện cần cho chúng, không phải chúng.
- **Bật `coAnhHuongTonKho()` cho chứng từ bán hàng / mua hàng** — làm ở PR sau, khi BA chốt giá vốn lấy từ đâu (§11-Q3).
- **Báo cáo NXT / `agg_ton_kho_ky`** — `acc_so_xuat_nhap_tong_hop` là nguồn cho báo cáo, việc dựng báo cáo là epic khác.
- **Kiểm kê, điều chỉnh tồn thủ công** — không đi qua chứng từ nên không đi qua kernel này ở MVP.

---

## 2. Hiện trạng đã khảo sát

### 2.1 Code hiện có — greenfield hoàn toàn

```bash
grep -rln "InvTonKho\|inv_ton_kho" --include="*.java" .
# → chỉ 2 file trong master_data/kho (dò tham chiếu khi xoá kho), KHÔNG có repository/service nào ghi

grep -rn "coAnhHuongTonKho\|apDungTonKho\|hoanTacTonKho" --include="*.java" . | grep -v ChungTuTemplate
# → 0 dòng cài đặt; chỉ 2 dòng javadoc nhắc tên
```

Kết luận: **không có chứng từ nào override `coAnhHuongTonKho()`** ⇒ bước `capNhatTonKho` tại
[ChungTuTemplate.java:510](../cell-app/src/main/java/vn/vtt/pmkt/cell/accounting_core/chung_tu/service/ChungTuTemplate.java) **chưa từng chạy một lần nào**. Chúng ta đang xây trên đất trống, không có hồi quy để lo.

Khung đã có sẵn (chỉ là chỗ cắm, chưa có ruột):

| File | Có gì | Thiếu gì |
|---|---|---|
| `chung_tu/model/BienDongTonKho.java` | record 4 trường `(khoId, vatTuId, soLuong, giaTri)` | không có `chiTietChungTuId` (⇒ không có khoá idempotency), không có `so_lo`, đơn giá, tài khoản, đơn vị tính, kiểu nhập/xuất |
| `chung_tu/model/ChungTuContext.java:39,77-83` | `List<BienDongTonKho>` + `themBienDongTonKho` | — |
| `chung_tu/service/ChungTuTemplate.java:442-453` | `phanGhiSo` gọi `capNhatTonKho` sau khi ghi sổ cái | `// TODO: thêm param để check xem có ghi sổ kho hay không` |
| `ChungTuTemplate.java:556-571` | 2 hook `apDungTonKho`/`hoanTacTonKho` | **mặc định NÉM `IllegalStateException`** |
| `ChungTuTemplate.java:240-242` | `luongBoGhiSo` đã gọi `hoanTacTonKho` sau `xoaButToanSoCai` | thứ tự đã đúng, chỉ thiếu cài đặt |
| `chung_tu_ban_hang/package-info.java:20-23` | Ghi rõ: *"tồn kho chưa có kernel nên chứng từ khai `coAnhHuongTonKho() = false`; giá vốn nhận theo giá trị người dùng nhập"* | — |

### 2.2 Hiện trạng DB — schema đi TRƯỚC code

| Bảng | Migration | Trạng thái |
|---|---|---|
| `inv_ton_kho` | `V69:118-154` | Đủ dùng: `(tenant, vật tư, kho, lô)` + `so_luong_ton numeric(18,4)`, `gia_tri_ton money_vnd`, `gia_binh_quan`, `phien_ban`, RLS + FORCE + `trg_audit_inv_ton_kho`, unique partial `uq_inv_ton_kho_key` trên `COALESCE(so_lo,'')` |
| `acc_so_xuat_nhap_tong_hop` | `V245` | Đủ cột nghiệp vụ (~90 cột), partition RANGE theo `ngay_hach_toan`, PK `(id, ngay_hach_toan)`, RLS + audit trigger. **THIẾU**: `request_hash`, khoá idempotency, trigger immutable, trigger period-guard |
| `inv_cau_hinh_ton_kho` | `V152` | 1 dòng/tenant, `cho_phep_ton_kho_am boolean DEFAULT false` |
| `iam_tenant.cho_phep_ton_kho_am` | `V148` thêm → `V181` **gỡ** | Đã chết. Chỉ đọc `inv_cau_hinh_ton_kho` (D10) |
| `inv_luot_tinh_gia_xuat_kho`, `inv_ket_qua_tinh_gia_xuat_kho` | `V71` | Ngoài phạm vi (D8) |

Migration mới nhất hiện tại: `V352__pur_ctmh_status_index_quyen_danh_sach.sql` ⇒ **số kế tiếp là `V353`**.

Ghi chú lịch sử đáng lưu: comment `V148` nhắc `InvTonKhoRepository.apThayDoiTonKho` — **class này chưa từng tồn tại trong repo**. Đây là dấu vết của một thiết kế đã lên kế hoạch rồi bỏ dở, không phải code bị xoá.

### 2.3 Hạ tầng dùng lại được, không phải viết lại

| Hạ tầng | File | Dùng vào việc gì |
|---|---|---|
| Advisory lock theo chứng từ | `hach_toan/internal/ghi_so/ChungTuKhoaRepository.java` (`pg_advisory_xact_lock`) | Serialize ghi/gỡ sổ kho cùng chứng từ. Reentrant trong cùng transaction ⇒ gọi lại ở kernel kho không tốn gì |
| Kiểm kỳ khoá sổ | `hach_toan/internal/ky_ke_toan/KyKeToanChecker.java` | Y nguyên: sổ kho cũng có `ngay_hach_toan` và cũng phải chịu khoá sổ |
| Tra id loại chứng từ | `hach_toan/internal/loai_chung_tu/LoaiChungTuLookup.java` (cache `ConcurrentHashMap`) | `acc_so_xuat_nhap_tong_hop.loai_chung_tu_id` |
| Vân tay nội dung | `hach_toan/internal/ghi_so/RequestHash.java` | **Không dùng lại được** — nó băm `DinhKhoan`. Viết `KhoRequestHash` cùng công thức, khác trường (§4.3) |
| Bọc lỗi API | `core/shared/error/ApiException`, `PeriodLockedException` | Y nguyên |
| Tenant + RLS | `TenantContext`, policy `tenant_isolation` trên cả 3 bảng | Không lọc tenant thủ công trong repository |

---

## 3. Vì sao KHÔNG copy-paste được kernel sổ cái — 5 điểm khác bản chất

Đây là phần quan trọng nhất của tài liệu. Ai bỏ qua mục này sẽ viết ra một kernel trông giống
`GhiSoService` mà sai tồn kho.

| # | Sổ cái (`hach_toan`) | Sổ kho (`ton_kho`) | Hệ quả thiết kế |
|---|---|---|---|
| **K1** | Chỉ ghi vào MỘT bảng append-only `acc_so_cai` | Ghi sổ chi tiết `acc_so_xuat_nhap_tong_hop` **và** cộng/trừ số dư `inv_ton_kho` | Kernel có 2 bước ghi; bước 2 là UPDATE tại chỗ, không phải INSERT |
| **K2** | Bỏ ghi sổ = `DELETE` là xong, số dư tự đúng vì nó luôn được tính lại từ tổng dòng | Xoá dòng sổ **không** tự trả `inv_ton_kho` về cũ — số dư là bản materialize | Bỏ ghi sổ phải **đảo delta** trước, rồi mới xoá dòng. Thứ tự ngược lại là mất luôn dữ liệu để đảo |
| **K3** | Cân đối Nợ/Có đúng **theo cấu trúc** (tách 1 định khoản → 2 dòng đối xứng) | Không có bất biến tự cân nào. Sai dấu = tồn sai, không ai phát hiện | Quy ước dấu phải cưỡng chế ở validator: `soLuong` và `giaTri` **bắt buộc cùng dấu**, `signum() != 0` |
| **K4** | Không có ràng buộc "số dư ≥ 0" | Tồn âm bị chặn theo cấu hình tenant, và chỉ biết được **SAU KHI** áp delta | Kiểm bằng `RETURNING so_luong_ton` của chính câu upsert, KHÔNG đọc trước rồi ghi sau (TOCTOU) |
| **K5** | Hai chứng từ khác nhau ghi hai tập dòng rời nhau ⇒ không tranh chấp hàng | Hai chứng từ khác nhau có thể cùng chạm một dòng `inv_ton_kho` ⇒ **khoá hàng chéo nhau ⇒ deadlock** | Sắp xếp delta theo `(kho_id, vat_tu_id, so_lo)` trước khi upsert — mọi transaction lấy khoá cùng thứ tự |

Riêng **K2** là chỗ dễ sai nhất. Cài đặt ngây thơ sẽ đảo tồn bằng `ctx.bienDongTonKho()` — tức bằng
*chứng từ đang cầm trên tay*. Nhưng luồng `BO_GHI_SO` chạy trên bản ghi vừa nạp từ DB, mà bản ghi đó
có thể đã được sửa (hoặc engine tính giá đã ghi đè đơn giá) sau lần ghi sổ. Đảo bằng số mới → tồn
lệch vĩnh viễn, không có gì báo. Vì vậy **D3**: đảo bằng đúng những con số đã ghi vào sổ.

---

## 4. Thiết kế

### 4.1 Cây thư mục

```
accounting_core/ton_kho/
├── package-info.java                    @ApplicationModule? KHÔNG — là sub-package của accounting_core
├── api/
│   ├── GhiSoKhoApi.java                 ghiSoKho / boGhiSoKho / daGhiSoKho
│   ├── SoKhoApi.java                    theoChungTu  (đọc sổ XNT)
│   ├── TonKhoApi.java                   tonHienTai   (đọc số dư)
│   ├── CauHinhTonKhoApi.java            choPhepTonKhoAm
│   ├── MaLoiTonKho.java                 mã lỗi + messageId — HỢP ĐỒNG với FE
│   └── dto/
│       ├── BienDongKho.java             đơn vị đầu vào (thay BienDongTonKho — D7)
│       ├── GhiSoKhoRequest.java         header + List<BienDongKho>
│       ├── KetQuaGhiSoKho.java          (soDong, laLapLai, requestHash)
│       ├── DongSoKhoDto.java            đọc sổ XNT
│       └── TonKhoDto.java               (khoId, vatTuId, soLo, soLuongTon, giaTriTon, giaBinhQuan)
└── internal/
    ├── ghi_so_kho/
    │   ├── GhiSoKhoService.java         cài GhiSoKhoApi — MANDATORY
    │   ├── BienDongKhoValidator.java    hàm thuần, không Spring
    │   └── KhoRequestHash.java          SHA-256, hàm thuần
    ├── so_kho/
    │   ├── SoKhoEntity.java             @Immutable, @Table("acc_so_xuat_nhap_tong_hop")
    │   ├── SoKhoRepository.java         timTatCa / xoaTheoChungTu / timMaLoaiChungTu
    │   └── SoKhoDocService.java         cài SoKhoApi — readOnly, KHÔNG mandatory
    ├── ton_kho/
    │   ├── TonKhoRepository.java        upsert delta (native) + đọc tồn
    │   └── TonKhoDocService.java        cài TonKhoApi — readOnly
    └── cau_hinh/
        ├── CauHinhTonKhoRepository.java
        └── CauHinhTonKhoService.java    cài CauHinhTonKhoApi
```

**Vì sao không tạo module Modulith riêng `inventory_core`?** Vì luồng ghi sổ kho và ghi sổ cái phải
chạy trong **cùng một transaction, dưới cùng một advisory lock, chịu cùng một cơ chế khoá kỳ**.
Tách module thì `ton_kho` phải import `hach_toan.api` (khoá + kỳ) và `chung_tu` phải import cả hai —
ba cạnh phụ thuộc thay vì một, đổi lấy đúng một lợi ích tưởng tượng là "gọn tên package". Người dùng
đã chốt đặt vào `accounting_core`; thiết kế này khớp với chốt đó.

### 4.2 `BienDongKho` — đơn vị đầu vào

```java
public record BienDongKho(
        UUID chiTietChungTuId,   // BẮT BUỘC — nằm trong khoá idempotency của sổ XNT
        UUID khoId,              // BẮT BUỘC
        UUID vatTuId,            // BẮT BUỘC
        String soLo,             // null → kernel chuẩn hoá thành "" (D6)
        LocalDate hanSuDung,     // null khi không quản lý HSD
        BigDecimal soLuong,      // DƯƠNG = nhập, ÂM = xuất — một chiều duy nhất
        BigDecimal giaTri,       // cùng dấu với soLuong
        BigDecimal donGia,       // null → kernel tự suy = |giaTri| / |soLuong|
        String donViTinh,
        BigDecimal heSoQuyDoi,
        UUID taiKhoanVatTuId,
        UUID taiKhoanDoiUngId,
        String dienGiai) {

    public boolean laNhap() { return soLuong.signum() > 0; }

    public static BienDongKho nhap(UUID khoId, UUID vatTuId, BigDecimal soLuong, BigDecimal giaTri);
    public static BienDongKho xuat(UUID khoId, UUID vatTuId, BigDecimal soLuong, BigDecimal giaTri);
    public BienDongKho voiChiTiet(UUID chiTietChungTuId);
    public BienDongKho voiLo(String soLo, LocalDate hanSuDung);
    public BienDongKho voiTaiKhoan(UUID vatTu, UUID doiUng);
}
```

**Giữ nguyên quy ước dấu một chiều** của `BienDongTonKho` cũ (dương = nhập, âm = xuất) — javadoc gốc
đã lý giải đúng: mang thêm cờ `kieuNhapXuat` là mở đường cho mỗi module tự diễn giải dấu một kiểu.
Hai factory `nhap()`/`xuat()` để chỗ gọi đọc được, `xuat()` tự đổi dấu về âm.

Cột `kieu_nhap_xuat` của bảng sổ vẫn được ghi — nhưng do **kernel suy ra từ dấu**, không do caller khai.

### 4.3 `GhiSoKhoRequest` + vân tay

```java
public record GhiSoKhoRequest(
        UUID chungTuId, String soChungTu,
        LocalDate ngayChungTu, LocalDate ngayHachToan,
        String maLoaiChungTu, String dienGiai,
        UUID doiTuongId, UUID loaiTienId, BigDecimal tyGia,
        List<BienDongKho> bienDong) { ... }
```

`KhoRequestHash` sao chép **công thức** của `RequestHash` (chuẩn hoá → sắp xếp → SHA-256 hex), khác
tập trường:
- vào vân tay: `chiTietChungTuId, khoId, vatTuId, soLo, soLuong, giaTri` + header `(chungTuId, soChungTu, ngayChungTu, ngayHachToan, maLoaiChungTu)`;
- **không** vào vân tay: `dienGiai`, `donViTinh`, `hanSuDung`, tài khoản — cùng lý do bản gốc loại `dienGiai`: sửa một dấu phẩy mà bắt người dùng bỏ ghi sổ rồi ghi lại là vô lý;
- số lượng/giá trị `stripTrailingZeros()` trước khi băm.

> Không gộp chung một `RequestHash` cho cả hai kernel: chúng băm hai loại record khác nhau, gộp thì
> phải generic hoá bằng `Function<T,String>` — thêm một lớp trừu tượng để tiết kiệm ~40 dòng hàm thuần
> đã có test riêng.

### 4.4 Hợp đồng `GhiSoKhoApi`

```java
public interface GhiSoKhoApi {
    /** Idempotent theo nội dung: replay → laLapLai=true; nội dung khác → 409 INVENTORY_PAYLOAD_MISMATCH. */
    KetQuaGhiSoKho ghiSoKho(GhiSoKhoRequest request);

    /** Đảo tồn theo ĐÚNG dòng sổ đang có rồi xoá vật lý chúng. Chưa ghi sổ → trả 0, không lỗi. */
    int boGhiSoKho(UUID chungTuId);

    boolean daGhiSoKho(UUID chungTuId);
}
```

Toàn bộ `Propagation.MANDATORY` (D5), lý do chép nguyên từ javadoc `GhiSoApi`: nếu để `REQUIRED`,
một lời gọi quên mở transaction vẫn chạy và commit biến động kho độc lập với chứng từ.

---

## 5. Thuật toán

### 5.1 `ghiSoKho`

```
1. BienDongKhoValidator.kiemTra(request)          // hàm thuần, chưa chạm DB
2. khoa.khoa(request.chungTuId())                 // pg_advisory_xact_lock — reentrant với kernel sổ cái
3. kyKeToan.kiemTraKyMo(ngayHachToan, maLoaiChungTu)
4. vanTay = KhoRequestHash.cua(request)
5. daGhi = soKho.timTatCa(chungTuId)
   nếu !daGhi.isEmpty():
        vanTay khớp  → return lapLai(daGhi.size(), vanTay)      // replay, không làm gì
        vanTay lệch  → throw 409 INVENTORY_PAYLOAD_MISMATCH     // KHÔNG ghi đè
6. loaiChungTuId = loaiChungTu.idTheoMa(maLoaiChungTu)
7. // (a) sổ chi tiết: 1 BienDongKho → 1 dòng acc_so_xuat_nhap_tong_hop
   soKho.saveAll(request.bienDong().map(b -> SoKhoEntity.dong(header, b, loaiChungTuId, vanTay)))
8. // (b) số dư: gộp delta theo khoá rồi áp, THEO THỨ TỰ ỔN ĐỊNH
   delta = bienDong.groupBy(kho, vatTu, so_lo).sum(soLuong, giaTri)
                   .sortedBy(khoId, vatTuId, soLo)              // chống deadlock — K5
   choPhepAm = cauHinh.choPhepTonKhoAm()
   với mỗi d trong delta:
        tonMoi = tonKho.apDelta(d)                              // upsert ... RETURNING so_luong_ton
        nếu tonMoi.signum() < 0 và !choPhepAm:
              throw 409 NEGATIVE_STOCK(kho, vật tư, lô, tonMoi) // rollback cả transaction
9. return daGhi(soDong, vanTay)
```

Bước 8 dùng **một câu SQL cho mỗi khoá**, không đọc-rồi-ghi:

```sql
INSERT INTO inv_ton_kho (tenant_id, vat_tu_id, kho_id, so_lo, so_luong_ton, gia_tri_ton, gia_binh_quan)
VALUES (fn_current_tenant(), :vatTuId, :khoId, :soLo, :dSoLuong, :dGiaTri,
        CASE WHEN :dSoLuong <> 0 THEN :dGiaTri / :dSoLuong END)
ON CONFLICT (tenant_id, vat_tu_id, kho_id, COALESCE(so_lo, ''))    -- uq_inv_ton_kho_key (V69)
WHERE da_xoa = false
DO UPDATE SET
    so_luong_ton  = inv_ton_kho.so_luong_ton + EXCLUDED.so_luong_ton,
    gia_tri_ton   = inv_ton_kho.gia_tri_ton  + EXCLUDED.gia_tri_ton,
    gia_binh_quan = CASE
        WHEN inv_ton_kho.so_luong_ton + EXCLUDED.so_luong_ton > 0
        THEN (inv_ton_kho.gia_tri_ton + EXCLUDED.gia_tri_ton)
             / (inv_ton_kho.so_luong_ton + EXCLUDED.so_luong_ton)
        ELSE inv_ton_kho.gia_binh_quan END,      -- tồn về 0 hoặc âm: GIỮ giá cũ, không chia cho 0
    phien_ban     = inv_ton_kho.phien_ban + 1,
    ngay_cap_nhat = now()
RETURNING so_luong_ton, gia_tri_ton;
```

Ba điểm phải giữ khi sửa câu này:
1. `so_luong_ton = <bảng>.so_luong_ton + <delta>` — cộng **trong SQL**, không cộng ở Java rồi SET.
   Cộng ở Java là lost-update kinh điển khi hai chứng từ khác nhau chạm cùng dòng.
2. `RETURNING` là nguồn DUY NHẤT để kiểm tồn âm (K4).
3. `ON CONFLICT` phải trỏ đúng index `uq_inv_ton_kho_key` **kèm** `WHERE da_xoa = false` — thiếu mệnh
   đề này Postgres không khớp được index partial và ném lỗi lúc chạy.

### 5.2 `boGhiSoKho`

```
1. nếu chungTuId == null → return 0
2. khoa.khoa(chungTuId)
3. dong = soKho.timTatCa(chungTuId);  nếu rỗng → return 0   // idempotent, KHÔNG lỗi
4. maLoai = soKho.timMaLoaiChungTu(chungTuId)
   với mỗi ngayHachToan RIÊNG BIỆT trong dong:  kyKeToan.kiemTraKyMo(ngay, maLoai)
5. // ĐẢO TỒN TRƯỚC KHI XOÁ — D3/K2
   delta = dong.map(d -> -(soLuongNhap - soLuongXuat), -(thanhTienNhap - thanhTienXuat))
              .groupBy(kho, vatTu, so_lo).sum()
              .sortedBy(khoId, vatTuId, soLo)
   với mỗi d: tonMoi = tonKho.apDelta(d)
              nếu tonMoi < 0 và !choPhepAm → throw 409 NEGATIVE_STOCK_ON_UNPOST   // §11-Q2
6. soKho.xoaTheoChungTu(chungTuId)      // native DELETE, không JPQL (@Immutable)
7. return dong.size()
```

Thứ tự 5 → 6 là bắt buộc: xoá trước thì bước 5 không còn dữ liệu để đảo.

### 5.3 Bảng đối chiếu hai kernel

| Việc | `hach_toan` | `ton_kho` |
|---|---|---|
| Cổng ghi | `GhiSoApi.ghiSo` | `GhiSoKhoApi.ghiSoKho` |
| Cổng đọc | `SoCaiApi.theoChungTu` | `SoKhoApi.theoChungTu` + `TonKhoApi.tonHienTai` |
| Validator thuần | `DinhKhoanValidator` | `BienDongKhoValidator` |
| Vân tay | `RequestHash` | `KhoRequestHash` |
| Bảng sổ | `acc_so_cai` | `acc_so_xuat_nhap_tong_hop` |
| Bảng số dư | *(không có)* | `inv_ton_kho` |
| Khoá idempotency | `uq_acc_so_cai_idempotency` (V1:4065) | `uq_acc_so_xnth_idempotency` (**V353**) |
| Nhân bản dòng | 1 định khoản → **2** dòng (Nợ/Có) | 1 biến động → **1** dòng |
| Bỏ ghi sổ | DELETE | đảo delta → DELETE |

---

## 6. Migration `V353__acc_so_xnth_idempotency_guard.sql`

```sql
-- 1) Vân tay nội dung — nền tảng idempotency cấp chứng từ (mirror acc_so_cai.request_hash, V1:419)
ALTER TABLE public.acc_so_xuat_nhap_tong_hop
    ADD COLUMN IF NOT EXISTS request_hash text;
COMMENT ON COLUMN public.acc_so_xuat_nhap_tong_hop.request_hash IS
    'SHA-256 hex nội dung chuẩn hoá GhiSoKhoRequest. Replay cùng hash → idempotent; lệch hash → INVENTORY_PAYLOAD_MISMATCH (409).';

-- 2) so_lo: NULL → '' và NOT NULL, để khoá idempotency là cột trần (D6).
--    Bảng partition KHÔNG nhận unique index dạng biểu thức/partial ⇒ không dùng được COALESCE.
UPDATE public.acc_so_xuat_nhap_tong_hop SET so_lo = '' WHERE so_lo IS NULL;
ALTER TABLE public.acc_so_xuat_nhap_tong_hop
    ALTER COLUMN so_lo SET DEFAULT '',
    ALTER COLUMN so_lo SET NOT NULL;

-- 3) Khoá chống ghi trùng. PHẢI chứa ngay_hach_toan (khoá phân vùng) — mirror uq_acc_so_cai_idempotency.
--    vat_tu_id/chi_tiet_chung_tu_id: hạ NOT NULL vì chúng nằm trong khoá.
ALTER TABLE public.acc_so_xuat_nhap_tong_hop
    ALTER COLUMN chi_tiet_chung_tu_id SET NOT NULL,
    ALTER COLUMN vat_tu_id            SET NOT NULL,
    ALTER COLUMN chung_tu_id          SET NOT NULL;
ALTER TABLE public.acc_so_xuat_nhap_tong_hop
    ADD CONSTRAINT uq_acc_so_xnth_idempotency
    UNIQUE (tenant_id, chung_tu_id, chi_tiet_chung_tu_id, vat_tu_id, so_lo, ngay_hach_toan);

-- 4) Bất biến sau khi ghi — mirror tg_acc_so_cai_immutable (V1:6471)
CREATE TRIGGER tg_acc_so_xnth_immutable
    BEFORE UPDATE ON public.acc_so_xuat_nhap_tong_hop
    FOR EACH ROW EXECUTE FUNCTION public.trg_acc_so_cai_immutable();

-- 5) Chốt chặn kỳ khoá ở DB — mirror acc_so_cai_period_guard (V1:121)
CREATE TRIGGER tg_acc_so_xnth_period_guard
    BEFORE INSERT OR DELETE ON public.acc_so_xuat_nhap_tong_hop
    FOR EACH ROW EXECUTE FUNCTION public.acc_so_cai_period_guard();
```

**Rủi ro của bước (3)**: `ALTER TABLE ... SET NOT NULL` trên bảng partition sẽ **nổ nếu đã có dữ liệu
NULL**. Bảng vừa được tạo ở V245 và **chưa có writer nào** (§2.1) ⇒ thực tế rỗng. Vẫn phải:
- chạy `SELECT count(*) FROM acc_so_xuat_nhap_tong_hop` trên staging trước khi merge;
- nếu có dòng, đổi (3) thành `NOT VALID` + backfill riêng, đừng ép `SET NOT NULL`.

**Rủi ro của bước (5)**: `acc_so_cai_period_guard()` đọc `NEW.loai_chung_tu_id` / `NEW.ngay_hach_toan`
— hai cột này có ở cả hai bảng nên hàm dùng chung được. **Phải đọc lại thân hàm ở `V1:121` trước khi
gắn**; nếu nó tham chiếu cột chỉ có ở `acc_so_cai`, tách thành hàm `acc_so_xnth_period_guard()` riêng.
Ghi rõ kết quả kiểm tra vào PR description.

---

## 7. Tích hợp `ChungTuTemplate`

### 7.1 Diff dự kiến

```java
// ChungTuSupport — thêm 1 phụ thuộc (constructor 7 → 8 tham số)
public ChungTuSupport(..., GhiSoKhoApi ghiSoKho) { ... }
public GhiSoKhoApi ghiSoKho() { return ghiSoKho; }

// ChungTuTemplate:556-571 — hai hook KHÔNG còn ném lỗi, đã có cài đặt mặc định
protected void apDungTonKho(ChungTuContext<C> ctx) {
    ghiSoKho.ghiSoKho(new GhiSoKhoRequest(
            ctx.chungTuId(), ctx.soChungTu(), ctx.ngayChungTu(), ctx.ngayHachToan(),
            maLoaiChungTu(), dienGiaiChung(ctx), doiTuongId(ctx), loaiTienId(ctx), tyGia(ctx),
            List.copyOf(ctx.bienDongKho())));
}

protected void hoanTacTonKho(ChungTuContext<C> ctx) {
    ghiSoKho.boGhiSoKho(ctx.chungTuId());
}

// ChungTuTemplate:510 — bỏ TODO ở :451, giữ nguyên điều kiện
private void capNhatTonKho(ChungTuContext<C> ctx) {
    if (!coAnhHuongTonKho() || ctx.bienDongKho().isEmpty()) return;
    apDungTonKho(ctx);
}

// ChungTuTemplate:402 — thêm lưới an toàn đối xứng doiSoatVoiSoCai
private void doiSoatVoiSoKho(ChungTuContext<C> ctx) {
    if (!coAnhHuongTonKho()) return;
    if (ghiSoKho.daGhiSoKho(ctx.chungTuId()))
        throw ApiException.conflict(MaLoiChungTu.SO_KHO_LECH, ...);
}
```

`doiSoatVoiSoKho` được gọi **ngay sau** `doiSoatVoiSoCai` trong `luongSua` (:176) và `luongXoa` (:200):
cùng lý do đã viết ở javadoc bản gốc — chỉ sửa/xoá được chứng từ chưa ghi sổ, nên còn dòng sổ kho là
dấu hiệu cờ trạng thái và sổ nói ngược nhau.

### 7.2 Thứ tự trong `luongBoGhiSo` — GIỮ NGUYÊN

`ChungTuTemplate.java:236-247` hiện gọi `xoaButToanSoCai` **rồi** `hoanTacTonKho`. Thứ tự này đúng và
không được đổi: cả hai chạy trong một transaction nên không có trạng thái trung gian nhìn thấy được;
đặt tồn kho trước sổ cái chỉ đổi thứ tự khoá hàng giữa hai bảng mà không được gì.

### 7.3 Hook mới cho lớp con

Chứng từ nghiệp vụ chỉ phải làm hai việc:

```java
@Override protected boolean coAnhHuongTonKho() { return true; }

@Override protected void sauKhiLuu(ChungTuContext<C> ctx) {
    for (ChiTiet d : ctx.get(CHI_TIET)) {
        ctx.themBienDongKho(BienDongKho.nhap(d.getKhoId(), d.getVatTuId(), d.getSoLuong(), d.getThanhTien())
                .voiChiTiet(d.getId())
                .voiLo(d.getSoLo(), d.getHanSuDung()));
    }
}
```

Không còn override `apDungTonKho`/`hoanTacTonKho` — hai hook đó thành `protected` có thân, chỉ override
khi chứng từ cần luật riêng (vd điều chuyển: một dòng sinh **hai** biến động, xuất kho A + nhập kho B).

---

## 8. Mã lỗi (`MaLoiTonKho`)

| Hằng số | HTTP | messageId | Khi nào |
|---|---|---|---|
| `INVALID_STOCK_MOVEMENT` | 400 | `MSG_INV_GS_001` | Thiếu kho/vật tư/chi tiết chứng từ; `soLuong = 0`; `soLuong` và `giaTri` **khác dấu**; trùng khoá `(chiTiet, kho, vậtTư, lô)` trong cùng lệnh |
| `INVENTORY_PAYLOAD_MISMATCH` | 409 | `MSG_INV_GS_002` | Chứng từ đã ghi sổ kho với nội dung khác |
| `UNKNOWN_VOUCHER_TYPE` | 400 | — | Tái dùng `MaLoiHachToan.UNKNOWN_VOUCHER_TYPE` (cùng `LoaiChungTuLookup`) |
| `NEGATIVE_STOCK` | 409 | `MSG_INV_GS_004` | Ghi sổ làm tồn < 0 và `cho_phep_ton_kho_am = false` |
| `NEGATIVE_STOCK_ON_UNPOST` | 409 | `MSG_INV_GS_005` | Bỏ ghi sổ làm tồn < 0 (hàng đã xuất đi rồi) — §11-Q2 |

Kỳ khoá dùng lại `PeriodLockedException` sẵn có, không thêm mã mới.

FE hiện **chưa có bảng tra `messageId` → chuỗi hiển thị** (`grep -rn "MSG_ACC_GS" client/src` → 0 kết
quả; `client/src/platform/http/apiError.ts:48` chỉ đọc field). Việc thêm key i18n vào `vi.ts`/`en.ts`
thuộc PR màn hình chứng từ kho, không thuộc plan này — nhưng **mã và messageId phải chốt ngay tại PR-1**
vì chúng là hợp đồng.

---

## 9. Tương tranh, deadlock, hiệu năng

| Tình huống | Cơ chế bảo vệ |
|---|---|
| Hai request "Lưu và ghi sổ" cùng chứng từ | `pg_advisory_xact_lock(chungTuId)` — request sau đợi, rồi thấy vân tay cũ → replay |
| Hai chứng từ khác nhau cùng chạm 1 dòng `inv_ton_kho` | Upsert delta trong SQL (không lost-update) + row lock của Postgres |
| Hai chứng từ chạm **cùng tập** dòng theo thứ tự ngược nhau | Sắp `(khoId, vatTuId, soLo)` trước khi áp — mọi transaction lấy khoá cùng thứ tự (K5) |
| Chứng từ có 500 dòng chi tiết | Gộp delta theo khoá trước ⇒ số câu upsert = số **khoá riêng biệt**, không phải số dòng |
| Người dùng cầm dữ liệu cũ trên màn hình | `@Version phien_ban` trên entity chứng từ (tầng khác, không thuộc kernel) |
| `inv_ton_kho.phien_ban` | Kernel tự `+ 1` trong upsert; **không** dùng làm optimistic lock — delta cộng trong SQL đã đủ |

**Điểm cần đo sau khi có chứng từ thật**: một transaction giữ khoá hàng `inv_ton_kho` từ lúc upsert
tới lúc COMMIT. Chứng từ nhiều dòng cùng vật tư ở giờ cao điểm sẽ xếp hàng trên hàng đó. Nếu thành
vấn đề, hướng xử lý là bảng delta append-only + job cộng dồn — **không** làm ở MVP (D2).

---

## 10. Rủi ro

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| **R1** | `acc_so_cai_period_guard()` không dùng lại được cho bảng sổ kho | Trung bình | Đọc thân hàm `V1:121` **trước** khi viết V353; tách hàm riêng nếu cần (§6) |
| **R2** | `SET NOT NULL` nổ vì bảng đã có dữ liệu | Thấp | Đếm dòng trên staging trước khi merge (§6) |
| **R3** | `ON CONFLICT` không khớp index partial `uq_inv_ton_kho_key` | Trung bình | Câu SQL phải kèm `WHERE da_xoa = false`; test tích hợp chạy đúng câu này, không mock |
| **R4** | Sai dấu ở chứng từ (khai xuất bằng số dương) | **Cao** | Validator chặn `soLuong`/`giaTri` khác dấu; factory `nhap()`/`xuat()`; test bảng đúng/sai dấu |
| **R5** | Bỏ ghi sổ đảo sai vì lấy số từ `ctx` | **Cao** | D3 — API `boGhiSoKho(chungTuId)` **không nhận** danh sách biến động, nên sai kiểu này không viết ra được |
| **R6** | Engine tính giá (V71) chạy sau, ghi đè đơn giá ⇒ `gia_tri_ton` lệch với sổ chi tiết | Trung bình | Ngoài phạm vi (D8). Ghi vào plan của epic tính giá: engine phải đi qua `boGhiSoKho` + `ghiSoKho` lại, không UPDATE thẳng |
| **R7** | Deadlock giữa kernel sổ cái và kernel sổ kho | Thấp | Cùng một advisory lock theo `chungTuId`, lấy trước mọi khoá hàng |
| **R8** | `ChungTuTemplate` đang bị sửa song song (4 TODO dở) | Trung bình | PR-4 tách riêng, rebase ngay trước khi code |

---

## 11. Điểm cần BA / user chốt trước khi code

| # | Câu hỏi | Ảnh hưởng |
|---|---|---|
| **Q1** | Tồn kho quản lý theo **lô** (`so_lo`) ở mức nào — mọi vật tư, hay chỉ vật tư bật cờ? | Quyết định `soLo` là bắt buộc hay optional trong validator |
| **Q2** | **Bỏ ghi sổ làm tồn âm** thì chặn hay cho qua? (VD: nhập 10, đã xuất 8, giờ bỏ ghi sổ phiếu nhập) | Có/không mã lỗi `NEGATIVE_STOCK_ON_UNPOST`. Đề xuất: **chặn**, cùng cấu hình `cho_phep_ton_kho_am` |
| **Q3** | Chứng từ bán hàng lấy **giá vốn** từ đâu khi bật `coAnhHuongTonKho()` — người dùng nhập (như hiện nay) hay engine tính giá? | Quyết định thời điểm bật cờ cho `chung_tu_ban_hang` (ngoài phạm vi plan này) |
| **Q4** | Kiểm tồn âm theo **kho** hay theo **toàn công ty**? | `V71` có khái niệm `THEO_KHO`/`KHONG_THEO_KHO` — đề xuất MVP: theo kho (đúng với khoá `inv_ton_kho`) |
| **Q5** | Vật tư **dịch vụ** (không quản lý tồn) đi vào kernel hay bị lọc từ chứng từ? | Đề xuất: chứng từ **không** sinh `BienDongKho` cho vật tư dịch vụ; kernel không tra danh mục (tránh phụ thuộc `master_data`) |

---

## 12. Kế hoạch triển khai — 5 PR, KHÔNG gộp

| PR | Nội dung | Điều kiện xanh |
|---|---|---|
| **PR-1** | `api/` thuần: `BienDongKho`, `GhiSoKhoRequest`, `KetQuaGhiSoKho`, `DongSoKhoDto`, `TonKhoDto`, `MaLoiTonKho`, 4 interface + javadoc "vì sao" | `./gradlew unitTest` xanh; chưa có cài đặt nên chưa có hành vi để hỏng |
| **PR-2** | `V353` + `SoKhoEntity` + `SoKhoRepository` + `TonKhoRepository` (câu upsert) + `CauHinhTonKhoService` | Test tích hợp: upsert cộng dồn đúng, `RETURNING` đúng, trigger immutable chặn UPDATE |
| **PR-3** | `BienDongKhoValidator` + `KhoRequestHash` + `GhiSoKhoService` + `SoKhoDocService` + `TonKhoDocService` | Unit test đủ luật (§13.1); tích hợp: ghi → replay → lệch hash → bỏ ghi → ghi lại |
| **PR-4** | Nối vào `ChungTuTemplate` + `ChungTuSupport`; xoá `BienDongTonKho` cũ; thêm `doiSoatVoiSoKho` | `ChungTuTemplateTest` mở rộng; **rebase ngay trước khi code** (R8) |
| **PR-5** | Chứng từ mẫu đầu tiên bật `coAnhHuongTonKho()` để nghiệm thu end-to-end | Chọn 1 chứng từ đơn giản; nếu chưa module kho nào tồn tại thì dùng test-fixture template trong `src/test` |

Không gộp PR-2 và PR-3: migration cần review DBA riêng, và R1/R2 phải được xác nhận trên staging
trước khi có code phụ thuộc vào nó.

---

## 13. Kiểm thử

### 13.1 Unit (`@Tag("unit")`, không cần Docker)

`BienDongKhoValidatorTest` — mỗi luật một test:
- thiếu `chungTuId` / `soChungTu` / `ngayHachToan` / `maLoaiChungTu` → 400
- danh sách biến động rỗng → 400
- thiếu `chiTietChungTuId` / `khoId` / `vatTuId` → 400
- `soLuong = 0` → 400 (không có "biến động rỗng")
- `soLuong > 0` mà `giaTri < 0` (và ngược lại) → 400 ← **R4**
- hai biến động trùng `(chiTiet, kho, vậtTư, lô)` trong cùng lệnh → 400 (sẽ đụng `uq_acc_so_xnth_idempotency`)
- `soLo = null` được chuẩn hoá thành `""`

`KhoRequestHashTest`:
- đổi thứ tự danh sách biến động → **cùng** vân tay
- `10` vs `10.00` → **cùng** vân tay
- đổi `dienGiai` → **cùng** vân tay
- đổi `soLuong` / `giaTri` / `soLo` → **khác** vân tay

`GhiSoKhoServiceTest` (mock repository, mirror `GhiSoServiceTest`):
- lệnh mới → gọi `saveAll` đúng số dòng, gọi `apDelta` đúng số **khoá gộp**
- replay cùng vân tay → không gọi `saveAll`, không gọi `apDelta`, `laLapLai = true`
- vân tay lệch → 409, không chạm repository nào
- gộp delta: 3 dòng cùng `(kho, vật tư, lô)` → **1** lần `apDelta` với tổng đúng
- thứ tự `apDelta` là thứ tự đã sắp `(khoId, vatTuId, soLo)` ← **K5**
- `RETURNING` trả tồn âm + `choPhepTonKhoAm = false` → 409; `= true` → đi tiếp
- `boGhiSoKho` khi chưa ghi sổ → trả 0, **không** ném lỗi
- `boGhiSoKho` đảo đúng dấu **từ dòng sổ**, không từ request ← **R5/D3**

### 13.2 Tích hợp (Testcontainers — cần Docker, chạy ở CI)

- Upsert đồng thời hai transaction trên cùng khoá → tổng cuối cùng đúng (không lost-update)
- `ON CONFLICT` khớp `uq_inv_ton_kho_key` (R3)
- `tg_acc_so_xnth_immutable` chặn UPDATE dòng sổ
- Kỳ khoá: ghi sổ kho vào kỳ đã khoá → `PeriodLockedException`; bỏ ghi sổ trong kỳ khoá → chặn
- RLS: tenant A không thấy dòng sổ / tồn của tenant B
- Vòng đời đủ: ghi → tồn tăng → bỏ ghi → tồn về đúng số ban đầu (**bất biến quan trọng nhất**)

### 13.3 Lệnh chạy trước khi báo hoàn thành

```bash
cd cell-app && ./gradlew unitTest
```

```bash
cd cell-app && ./gradlew build
```

> `cell-app/` là Gradle project độc lập — lệnh `./gradlew :cell-app:build` ghi trong `CLAUDE.md` không
> chạy được. Máy dev hiện **chưa có Docker**, nên `build` sẽ đỏ ở ~25 test Testcontainers có sẵn
> (`RedisCache*`, `FileStorage*`, `ToChucNhomCellMigrationTest`) — đó là giới hạn môi trường, không
> phải hồi quy. Cổng xanh thực tế ở máy dev là `unitTest`; phần tích hợp §13.2 phải xanh **ở CI**
> trước khi merge.

---

## 14. Điều kiện nghiệm thu

**Dev BE xác nhận**
- [ ] `grep -rn "inv_ton_kho\|acc_so_xuat_nhap_tong_hop" --include="*.java"` chỉ ra file trong `accounting_core/ton_kho/internal/**` (+ 2 file dò tham chiếu cũ ở `master_data/kho`)
- [ ] Mọi method ghi của kernel là `Propagation.MANDATORY`
- [ ] `boGhiSoKho` chỉ nhận `UUID` — không có overload nào nhận danh sách biến động (cưỡng chế D3)
- [ ] Vòng đời ghi → bỏ ghi trả tồn về **đúng** số ban đầu (test §13.2)
- [ ] Không import nào từ `master_data/**` trong package mới
- [ ] `ChungTuTemplate` không còn hook nào ném `IllegalStateException` vì "chưa có kernel"

**BA xác nhận**
- [ ] Q1–Q5 (§11) đã có câu trả lời ghi vào bảng D của tài liệu này
- [ ] Danh sách mã lỗi + messageId §8 được chấp nhận làm hợp đồng với FE

---

## Phụ lục — nguồn bằng chứng

| Khẳng định | Nguồn |
|---|---|
| Chưa chứng từ nào bật `coAnhHuongTonKho()` | `grep -rn "coAnhHuongTonKho" --include="*.java"` → chỉ javadoc |
| Hook tồn kho mặc định ném lỗi | `accounting_core/chung_tu/service/ChungTuTemplate.java:556-571, 605-611` |
| `capNhatTonKho` gọi sau ghi sổ cái | `ChungTuTemplate.java:442-453` |
| `luongBoGhiSo` gọi `hoanTacTonKho` sau `xoaButToanSoCai` | `ChungTuTemplate.java:236-247` |
| Bán hàng khai `coAnhHuongTonKho() = false` vì thiếu kernel | `chung_tu_ban_hang/package-info.java:20-23` |
| Kernel sổ cái `MANDATORY` + lý do | `hach_toan/internal/ghi_so/GhiSoService.java:28-36` |
| Idempotency bằng vân tay nội dung | `hach_toan/internal/ghi_so/RequestHash.java:17-32` |
| Bỏ ghi sổ = xoá vật lý | `hach_toan/internal/so_cai/SoCaiRepository.java` (`xoaTheoChungTu`) + `V56` |
| Advisory lock theo chứng từ | `hach_toan/internal/ghi_so/ChungTuKhoaRepository.java` |
| Kiểm kỳ khoá 2 phạm vi | `hach_toan/internal/ky_ke_toan/KhoaSoRepository.java` |
| `uq_acc_so_cai_idempotency` | `V1__baseline.sql:4061-4065` |
| `tg_acc_so_cai_immutable` | `V1__baseline.sql:6468-6471` |
| `acc_so_cai_period_guard()` | `V1__baseline.sql:118-121` |
| `inv_ton_kho` DDL + `uq_inv_ton_kho_key` | `V69__inv_phieu_nhap_kho_schema.sql:118-154` |
| `acc_so_xuat_nhap_tong_hop` DDL, partition, thiếu `request_hash` | `V245__acc_so_xuat_nhap_tong_hop.sql` |
| Cấu hình tồn âm — nguồn duy nhất | `V152__inv_cau_hinh_ton_kho.sql` + `V181__iam_tenant_drop_cho_phep_ton_kho_am.sql` |
| Engine tính giá là epic riêng | `V71__inv_tinh_gia_xuat_kho_schema.sql:1-8` |
| Migration mới nhất = V352 | `ls cell-app/src/main/resources/db/migration \| sort -V \| tail -1` |
