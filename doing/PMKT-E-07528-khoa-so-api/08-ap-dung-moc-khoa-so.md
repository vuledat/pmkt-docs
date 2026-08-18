# F08 — Áp dụng mốc khóa sổ và chặn thao tác

> Quay lại [00-ke-hoach-tong.md](00-ke-hoach-tong.md)
> **Đây là phần rủi ro cao nhất của epic** — nó sửa kernel hạch toán đang chạy. PR riêng (PR-5).

| Mục | Nội dung |
|---|---|
| Nguồn BA | BR01 + BR07 của `SCR_XemDanhSachThietLapKhoaSo.md` · BR17 Common · `MSG_PMKT-E-07528_026` |
| Endpoint | **Không có** — đây là hành vi ngang, áp cho mọi API chứng từ của mọi module |
| File sửa | `KyKeToanApi.java` · `KhoaSoRepository.java` · `KyKeToanChecker.java` · migration sửa function `acc_so_cai_period_guard` |

---

## 0. Các mục không áp dụng cho chức năng này

| Mục chuẩn | Trạng thái |
|---|---|
| **Hợp đồng API** | **Không áp dụng** — F08 không thêm endpoint nào. Nó đổi **hành vi** của mọi API chứng từ đang có (thêm/sửa/xoá/ghi sổ/bỏ ghi sổ ở `chung_tu_ban_hang`, `chung_tu_mua_hang`, và mọi module chứng từ sau này). Hợp đồng thay đổi duy nhất nhìn thấy từ ngoài: envelope lỗi `409 PERIOD_LOCKED` nay mang thêm `messageId = MSG_PMKT-E-07528_026` và tham số ngày khóa — §3.4 |
| **Ánh xạ cột BA ↔ DB ↔ DTO** | **Không áp dụng cho request**. Cột DB mà F08 **đọc**: `cfg_thiet_lap_khoa_so.{loai_doi_tuong, loai_chon_nguoi_dung, ngay_khoa_so, da_xoa}` + `…_chung_tu.ma_loai_chung_tu` + `…_nguoi_dung.user_id` — truy vấn đầy đủ ở §3.3 |
| **Validation** | **Không áp dụng** — không có đầu vào người dùng. Bản thân F08 **là** cổng validation của các luồng khác |
| **Phân trang · sắp xếp · lọc · dòng tổng** | **Không áp dụng** — không phải màn danh sách |
| **Tương tranh & transaction** | Có, nhưng không có gì mới: `kiemTraKyMo` khai `@Transactional(propagation = MANDATORY, readOnly = true)` (`KyKeToanChecker.java:31`) — nó **bắt buộc** chạy trong transaction của caller. Gọi ngoài transaction là ném lỗi chứ không phải im lặng fail-open, và đó là hành vi đã có, giữ nguyên |

---

> **Cập nhật 2026-08-11 — đã cài xong.** Tài liệu này viết ở thì tương lai khi lập kế hoạch; các
> mục §3 và §4 nay mô tả **code đang có**. Hai chốt của user làm thay đổi thiết kế so với bản đầu:
> **A1** — "người dùng" của thiết lập khoá sổ là **người đang thao tác** (người ghi sổ), nên
> `acc_so_cai.nguoi_tao` mang đúng giá trị đó và DB cưỡng chế được (V359); **Q15** — dùng cả
> `cfg_thiet_lap_khoa_so.chi_nhanh_id` và `acc_so_cai.ma_don_vi_id`, nên chiều chi nhánh cũng được
> cưỡng chế (V362). Kết luận cũ *"DB lỏng hơn Java một chiều"* **không còn đúng** — hai tầng nay
> đối xứng trên cả ba chiều.

## 1. Hiện trạng: đã có, nhưng thiếu một phạm vi

Hệ thống **đã** chặn thao tác vào kỳ đã khóa ở hai tầng. Bảng dưới là hiện trạng **trước** epic:

| Tầng | Ở đâu | Xét phạm vi nào | Thiếu gì |
|---|---|---|---|
| Java | `KhoaSoRepository.SQL_MOC_KHOA` (`KhoaSoRepository.java:25-38`) | `loai_doi_tuong = 1` (toàn hệ thống) · `= 2` khớp `ma_loai_chung_tu` | **Người dùng · chi nhánh** |
| DB | function `acc_so_cai_period_guard` (`V1__baseline.sql:121-161`), trigger trên `acc_so_cai` | y hệt | **Người dùng · chi nhánh** |

Sau epic, cả hai tầng xét đủ **ba chiều**: loại chứng từ · người thao tác · chi nhánh.

Javadoc `KhoaSoRepository.java:14-19` ràng buộc rõ:
> *Truy vấn ở đây là bản sao có chủ đích của trigger `acc_so_cai_period_guard`: cùng nguồn dữ liệu, cùng hai phạm vi khoá… Lệch một chi tiết là hệ thống cho nhập rồi mới chặn ở COMMIT (hoặc tệ hơn: chặn thứ DB cho phép), nên khi sửa trigger phải sửa cả đây.*

⇒ **Không được sửa một bên.** Mọi thay đổi ở §3 phải đi kèm thay đổi tương ứng ở §4, trong cùng một PR, kèm test đối chiếu (§6.2).

**Hệ quả nếu bỏ qua F08 và vẫn cho tạo thiết lập theo người dùng:** một thiết lập khóa cho user A sẽ chặn **tất cả mọi người** — vì truy vấn hiện tại chỉ nhìn `loai_doi_tuong` và `ma_loai_chung_tu`, không hề đọc bảng `cfg_thiet_lap_khoa_so_nguoi_dung`. Đây là lý do D9 xếp F08 là bắt buộc, không phải tuỳ chọn.

---

## 2. BR01 — nguyên tắc mốc muộn nhất

`SCR_XemDanhSachThietLapKhoaSo.md:59-62`:
> *Khi một chứng từ chịu chi phối của nhiều thiết lập ở các phạm vi khác nhau, hệ thống áp dụng mốc thời gian khóa sổ **lớn nhất**. Thiết lập "Toàn hệ thống" là mốc cơ sở. Các thiết lập chi tiết chỉ có tác dụng khi ngày khóa sổ lớn hơn mốc cơ sở.*
> *Ví dụ: Toàn hệ thống khóa đến 31/05, loại "Bán hàng" khóa đến 10/06. Chứng từ Bán hàng ngày 05/06 bị chặn (lấy mốc 10/06), nhưng chứng từ Mua hàng ngày 05/06 được phép sửa (chỉ chịu mốc 31/05).*

`MAX(...)` hiện tại **đã cài đúng BR01** cho hai phạm vi có sẵn. Việc cần làm là mở rộng tập bản ghi được đưa vào `MAX`, không phải đổi phép toán.

Ba phạm vi và điều kiện áp dụng cho một chứng từ `(ngayHachToan, maLoaiChungTu, nguoiTaoId)`:

| Bản ghi thiết lập | Áp dụng khi |
|---|---|
| `loai_doi_tuong = 1` | **luôn** — mốc cơ sở |
| `loai_doi_tuong = 2`, `loai_chon_nguoi_dung = 1` | `maLoaiChungTu` ∈ tập loại CT của thiết lập |
| `loai_doi_tuong = 2`, `loai_chon_nguoi_dung = 2` | `maLoaiChungTu` ∈ tập loại CT **và** `nguoiTaoId` ∈ tập user |

Chỉ tính các bản ghi `da_xoa = false`, `ngay_khoa_so IS NOT NULL` (loại trừ bản ghi THIẾT LẬP, vốn luôn có `ngay_khoa_so = NULL` — xem [F02 §1](02-tao-thiet-lap-khoa-so.md)).

---

## 3. Java — mở rộng `KyKeToanApi`

### 3.1 Chữ ký

```java
public interface KyKeToanApi {

    void kiemTraKyMo(LocalDate ngayHachToan, String maLoaiChungTu, UUID chiNhanhId);

    boolean kyDangMo(LocalDate ngayHachToan, String maLoaiChungTu, UUID chiNhanhId);
}
```

**Chỉ thêm MỘT tham số, không phải hai.** Chiều người dùng KHÔNG đi qua tham số: theo chốt A1,
"người dùng" của thiết lập khoá sổ là **người đang thao tác** — thứ đã nằm sẵn trong
`TenantContext` y như `tenantId`, và `KyKeToanChecker` tự đọc. Bắt mọi call-site truyền tay id
người dùng chỉ tạo thêm một chỗ để quên, mà quên thì mất chốt chặn **im lặng**.

Đối xứng ở tầng DB: `acc_so_cai.nguoi_tao` do `BaseEntity.onCreate()` gán từ
`TenantContext.userId()` lúc INSERT, nên trigger và Java đọc **cùng một giá trị**.

**Không giữ overload 2 tham số.** Bản kế hoạch đầu đề xuất một `default` `@Deprecated` để khỏi
sửa mọi call-site; thực tế chỉ có **ba** call-site (`ChungTuTemplate.kiemTraKyKeToan`,
`GhiSoService.ghiSo`, `GhiSoService.boGhiSo`) nên chi phí bằng không, còn cái giá của overload thì
không: một overload "chạy được nhưng thiếu một chiều phạm vi" là bẫy mà module mới sẽ sập vào, và
sập im lặng.

### 3.2 `chiNhanhId = null` nghĩa là gì

Không phải "bỏ qua kiểm tra" mà là **"chứng từ này không gắn chi nhánh"**:

| Thiết lập | Chứng từ không gắn chi nhánh | Chứng từ chi nhánh X |
|---|---|---|
| `chi_nhanh_id IS NULL` (khoá cấp pháp nhân) | **áp** | **áp** |
| `chi_nhanh_id = X` | không áp | **áp** |
| `chi_nhanh_id = Y` | không áp | không áp |

Toàn bộ dữ liệu hiện có rơi vào dòng đầu (chưa có thiết lập nào gắn chi nhánh), nên bật chiều này
**không gây hồi quy**. Không suy đoán chứng từ thuộc chi nhánh nào khi cột để trống — suy đoán ở
đây là chặn nhầm hoặc thả nhầm, cả hai đều im lặng.

**Giới hạn phải biết:** dòng `acc_so_cai` ghi **trước** V362 có `ma_don_vi_id = NULL` kể cả khi
chứng từ gốc có chi nhánh, nên chúng chỉ chịu khoá cấp pháp nhân. Không backfill trong epic này —
`acc_so_cai` là bảng phân vùng lớn nhất hệ thống, `@Immutable`, và có trigger
`tg_acc_so_cai_immutable` chặn UPDATE; backfill phải là một migration riêng có kế hoạch vận hành.

### 3.3 Truy vấn mới

```sql
SELECT MAX(t.ngay_khoa_so::date)
  FROM cfg_thiet_lap_khoa_so t
 WHERE t.tenant_id = :tenantId
   AND t.da_xoa = false
   AND t.ngay_khoa_so IS NOT NULL
   AND (t.chi_nhanh_id IS NULL
        OR t.chi_nhanh_id = cast(:chiNhanhId as uuid))
   AND (
        t.loai_doi_tuong = 1
     OR (t.loai_doi_tuong = 2
         AND EXISTS (SELECT 1 FROM cfg_thiet_lap_khoa_so_chung_tu c
                      WHERE c.thiet_lap_id = t.id
                        AND c.da_xoa = false
                        AND c.ma_loai_chung_tu = cast(:maLoaiChungTu as text))
         AND (t.loai_chon_nguoi_dung = 1
              OR (cast(:nguoiThaoTac as uuid) IS NOT NULL
                  AND EXISTS (SELECT 1 FROM cfg_thiet_lap_khoa_so_nguoi_dung n
                               WHERE n.thiet_lap_id = t.id
                                 AND n.da_xoa = false
                                 AND n.user_id = cast(:nguoiThaoTac as uuid)))))
       )
```

`:nguoiThaoTac` = `TenantContext.userId()`, không phải tham số của API (§3.1). Mệnh đề chi nhánh
đứng **ngoài** khối `loai_doi_tuong` vì nó áp cho cả hai loại phạm vi; mệnh đề người dùng đứng
**trong** nhánh `= 2` vì BA chỉ cho chọn người dùng khi khoá theo loại chứng từ.

Ba điểm cài đặt bắt buộc giữ nguyên từ bản cũ:
- Ép kiểu tường minh `cast(:x as text/uuid)` — bind `null` vào tham số native khiến PostgreSQL không suy được kiểu (ghi chú `KhoaSoRepository.java:40-41`).
- Mã rỗng thay cho `null` ở `maLoaiChungTu` (hằng `KHONG_XAC_DINH_LOAI`).
- So `ngay_khoa_so::date` — phần giờ **không** tham gia phép chặn (**Q10**).

`loai_chon_nguoi_dung` đọc từ **bảng cha** — đây là cột được chuyển vị trí trong migration ([09-thiet-ke-db.md §3](09-thiet-ke-db.md)). Nếu để nguyên ở bảng con thì mệnh đề trên phải `EXISTS` hai lần và giá trị "Tất cả" phải biểu diễn bằng một dòng con có `user_id IS NULL` — một dòng "không đại diện cho người dùng nào" là đúng loại dữ liệu gây lỗi off-by-one khi đếm.

### 3.4 Message lỗi phải đổi

Hôm nay `KyKeToanChecker.java:35-38` tự viết message và **không có `messageId`**:

```java
throw new PeriodLockedException(String.format(
        "Kỳ kế toán đã khoá đến %s — không thể hạch toán chứng từ %s ngày %s", …));
```

BA yêu cầu `MSG_PMKT-E-07528_026` với **hai tham số**: `{0}` ngày khóa sổ `DD/MM/YYYY`, `{1}` **tên thao tác** (`SCR_XemDanhSachThietLapKhoaSo.md:92`):
> *"Chứng từ thuộc kỳ đã khóa sổ (ngày khóa sổ: 31/05/2026). Không thể sửa."*

⇒ `kiemTraKyMo` cần biết **thao tác đang thực hiện**. Nguồn có sẵn: `HanhDongChungTu` (`accounting_core/chung_tu/model/HanhDongChungTu.java`) mà `ChungTuTemplate` đã cầm trong `ChungTuContext` (`ChungTuTemplate.java:104`).

| | A — thêm tham số `HanhDongChungTu` vào `kiemTraKyMo` | **B (chọn) — `PeriodLockedException` mang `mocKhoa`; tên thao tác gắn ở nơi bắt** |
|---|---|---|
| Kernel biết ngữ cảnh UI | Có — nhưng `GhiSoApi` cũng gọi `kiemTraKyMo` và nó **không** biết người dùng đang bấm nút gì | Không cần biết |
| Số call-site phải sửa | Mọi call-site | Chỉ nơi dựng message |
| Rủi ro | Tham số thứ tư trên một API kernel, dễ truyền sai | Message ghép ở `GlobalExceptionHandler` hoặc ở `ChungTuTemplate` — phải **không quên** một nhánh. Chốt an toàn: `PeriodLockedException` mang sẵn `messageId` + `{0}`; `{1}` mặc định là `"thực hiện thao tác"` nếu không nơi nào cung cấp |

Chọn **B**: mở rộng `PeriodLockedException` (`core/shared/error/PeriodLockedException.java:7`) để mang `LocalDate mocKhoa` + `messageId`. `GlobalExceptionHandler.java:302` đã map nó sang **409**; chỉ cần thêm `messageId` và `details` vào envelope, không đổi HTTP status.

---

## 4. DB — sửa function `acc_so_cai_period_guard`

Hai migration, mỗi cái thêm đúng một chiều: **V359** người dùng, **V362** chi nhánh. Kết quả là
trigger và `KhoaSoRepository.SQL_MOC_KHOA` (§3.3) xét **cùng ba chiều, cùng ngữ nghĩa**.

### 4.1 Chiều người dùng — chốt A1 gỡ được thế bí (Q4)

Bản kế hoạch đầu bế tắc ở chỗ: `acc_so_cai` không có cột nào trỏ về **người lập chứng từ**, và
cũng không biết bảng nguồn của `chung_tu_id`. Ba lối ra khi đó là (A) dùng `acc_so_cai.nguoi_tao`
— *người ghi sổ*, (B) thêm cột `nguoi_tao_chung_tu` + backfill, (C) DB chỉ giữ 2 chiều và chấp
nhận *"DB lỏng hơn Java"*. Bản đầu chọn C.

**Chốt A1 của user (2026-08-11) làm A trở thành đúng, không phải xấp xỉ:** "người dùng" của thiết
lập khoá sổ là **người đang thao tác** — chính là người bấm nút ghi sổ. Mà đó đúng là giá trị
`acc_so_cai.nguoi_tao` mang: `BaseEntity.onCreate()` gán nó từ `TenantContext.userId()` tại thời
điểm INSERT (`core/entity/BaseEntity.java:53-55`).

Cách đọc còn lại — cột `nguoi_ghi_so` **của chứng từ** — không dùng được: chứng từ chưa ghi sổ có
`nguoi_ghi_so = NULL`, nên không thiết lập theo người dùng nào khớp được và BR07 mất 3/5 thao tác
(Thêm mới · Sửa · Xoá).

⇒ Chọn **A**. Không cần cột mới, không cần backfill, và Java ↔ DB đối xứng.

Hai giới hạn có ý thức, ghi ngay trong V359:

1. `TG_OP = 'DELETE'` (bỏ ghi sổ) đọc `OLD.nguoi_tao` = người **đã** ghi sổ, không phải người đang
   bỏ ghi sổ. Chấp nhận được: thao tác đang gỡ chính bút toán của người đó.
2. `nguoi_tao IS NULL` (job/migration không có `TenantContext`) ⇒ thiết lập theo người dùng **không
   áp**. Fail-open có chủ đích — chặn một tiến trình nền bằng mốc dành cho một người cụ thể là chặn
   nhầm, mà tiến trình nền không có cách nào tự gỡ.

### 4.2 Chiều chi nhánh — chốt Q15

Bản đầu **cố ý bỏ qua** chi nhánh, và V359 ghi lý do ngay trong file: `acc_so_cai` không mang chi
nhánh (`ma_don_vi_id` có trong schema nhưng `SoCaiEntity` không map, javadoc ghi thẳng *"Thiếu
chiNhanhId"*). Thêm mệnh đề so với một cột **luôn NULL** sẽ khiến mọi thiết lập theo chi nhánh
**im lặng không chặn ai** — tệ hơn hẳn việc chưa hỗ trợ.

**Chốt Q15 của user: "Sử dụng cả `chi_nhanh_id` và `ma_don_vi_id`"** — hai tên cột cho cùng một
khái niệm. Ba điều kiện đủ đã làm trong cùng PR, trước khi V362 bật mệnh đề:

| # | Đã làm | Ở đâu |
|---|---|---|
| 1 | `SoCaiEntity` map `ma_don_vi_id` + `voiChiNhanh(...)` | `so_cai/SoCaiEntity.java` |
| 2 | `GhiSoRequest` mang `chiNhanhId`; `ChungTuTemplate.ghiSoCai` truyền `ctx.chiNhanhId()`; `ChungTuContext.ghiNhanChungTu(BaseChungTuEntity)` lấy thẳng từ header | `hach_toan/api/dto/`, `chung_tu/service/`, `chung_tu/model/` |
| 3 | `KyKeToanApi` nhận `chiNhanhId`; `KhoaSoRepository` kiểm cùng ba chiều với trigger | §3 |

Điểm 2 là chỗ dễ hỏng nhất nên có overload nhận thẳng entity: một module mới sao chép overload 4
tham số cũ sẽ mất chiều chi nhánh mà không có gì báo. `ChungTuContextChiNhanhTest` khoá điều này lại.

**`RequestHash` KHÔNG lấy `chiNhanhId`**, có chủ đích: thêm vào sẽ đổi vân tay của mọi chứng từ đã
ghi sổ trước đây, biến mọi lần ghi lại hợp lệ thành `POSTING_PAYLOAD_MISMATCH` (409). Đổi lấy một
thứ không cần: chi nhánh chỉ đổi được qua luồng SỬA, luồng SỬA đòi bỏ ghi sổ trước, và bỏ ghi sổ
xoá vật lý dòng sổ cái (V56) — không tồn tại đường nào tới được nhánh ghi lại với chi nhánh khác.

---

## 5. BR07 — chặn những thao tác nào

`SCR_XemDanhSachThietLapKhoaSo.md:85-94` liệt kê 5 thao tác bị chặn với chứng từ có `NgayHachToan <= NgayKhoaSo`:

| Thao tác | Cổng kiểm | Đã có chưa |
|---|---|---|
| **Thêm mới** chứng từ | `ChungTuTemplate` luồng TẠO — tự kiểm ở ca lưu nháp, hoặc `GhiSoApi.ghiSo` kiểm ở ca lưu-và-ghi-sổ | ✅ có |
| **Sửa** chứng từ | `ChungTuTemplate` luồng SỬA | ✅ có |
| **Xóa** chứng từ | `ChungTuTemplate` luồng XOÁ | ✅ có |
| **Ghi sổ** | `GhiSoApi.ghiSo` — tự gọi `kiemTraKyMo` với đúng cặp tham số sắp INSERT | ✅ có |
| **Bỏ ghi sổ** | `GhiSoApi.boGhiSo` — kiểm theo **từng ngày hạch toán** của các dòng đang gỡ | ✅ có |

⇒ **Không thêm cổng kiểm mới.** Nguyên tắc đã ghi ở `ChungTuTemplate.java:56-61`: *"Đúng MỘT cổng cho mỗi thao tác… Thêm một cổng kiểm thứ hai ở tầng trên là thừa một truy vấn, yếu hơn (chỉ biết một ngày của header) và có thể chặn nhầm chính thao tác gỡ hợp lệ."*

Việc của F08 chỉ là làm cho **các cổng sẵn có** biết thêm phạm vi người dùng, và trả đúng messageId.

**Một lưu ý dễ bỏ sót:** BR07 chặn cả **bỏ ghi sổ** trong kỳ đã khóa, mà bỏ ghi sổ là **XOÁ VẬT LÝ** dòng sổ cái (quyết định chốt ở `V56__acc_so_cai_unpost_physical_delete.sql`, ghi lại ở `ChungTuTemplate.java:52-53`). Trigger `acc_so_cai_period_guard` đã bắt cả `TG_OP = 'DELETE'` (`V1__baseline.sql:130-131`) nên tầng DB đã phủ. Không cần làm gì thêm — ghi ở đây để người review không đi tìm.

---

## 6. Kiểm thử

### 6.1 Unit test (`@Tag("unit")`)

| Lớp test | Kiểm gì |
|---|---|
| `KyKeToanCheckerTest` | Ba phạm vi §2: hệ thống · loại CT + "Tất cả" · loại CT + user cụ thể |
| `KyKeToanCheckerTest` | BR01 mốc muộn nhất: hệ thống 31/05 + Bán hàng 10/06 → CT Bán hàng 05/06 **bị chặn**, CT Mua hàng 05/06 **được phép** (đúng ví dụ BA) |
| `KyKeToanCheckerTest` | `TenantContext` không có user → bỏ qua nhóm thiết lập theo người dùng (§4.1 giới hạn 2) |
| `KyKeToanCheckerTest` | Ba ca chi nhánh của bảng §3.2 |
| `KyKeToanCheckerTest` | `ngayHachToan` đúng bằng mốc → **bị chặn** (BA: `<=`) |
| `PeriodLockedExceptionTest` | Message ghép đúng `MSG_PMKT-E-07528_026` với `{0}` định dạng `DD/MM/YYYY`; `{1}` mặc định khi không có ngữ cảnh |
| ~~`CallSiteDeprecatedTest`~~ | **Bỏ** — không còn overload 2 tham số để đếm (§3.1) |
| `ChungTuContextChiNhanhTest` ✅ | Chi nhánh đi được từ header vào context; overload 4 tham số không xoá mất nó |

### 6.2 Test tích hợp (cần Docker) — **bắt buộc**

`KyKhoaSoDoiChieuIT` — chạy CÙNG bộ dữ liệu qua hai đường và so kết luận:

| Bộ dữ liệu | Java `kyDangMo(...)` | INSERT thẳng `acc_so_cai` | Khẳng định |
|---|---|---|---|
| Không thiết lập nào | mở | thành công | bằng nhau |
| Toàn hệ thống 31/05, CT ngày 31/05 | đóng | trigger chặn | bằng nhau |
| Toàn hệ thống 31/05, CT ngày 01/06 | mở | thành công | bằng nhau |
| Loại BAN_HANG 10/06 + "Tất cả", CT BAN_HANG 05/06 | đóng | trigger chặn | bằng nhau |
| Loại BAN_HANG 10/06 + "Tất cả", CT MUA_HANG 05/06 | mở | thành công | bằng nhau |
| Loại BAN_HANG 10/06 + user A, dòng sổ cái `nguoi_tao = A` | đóng | **trigger chặn** | bằng nhau — §4.1 phương án A |
| Loại BAN_HANG 10/06 + user A, dòng sổ cái `nguoi_tao = B` | mở | thành công | bằng nhau |
| Loại BAN_HANG 10/06 + user A, dòng sổ cái `nguoi_tao IS NULL` | mở | thành công | bằng nhau — fail-open §4.1 giới hạn 2 |
| Chi nhánh X 31/05, dòng sổ cái `ma_don_vi_id = X` | đóng | trigger chặn | bằng nhau — §4.2 |
| Chi nhánh X 31/05, dòng sổ cái `ma_don_vi_id = Y` | mở | thành công | bằng nhau |
| Chi nhánh X 31/05, dòng sổ cái `ma_don_vi_id IS NULL` | mở | thành công | bằng nhau — không suy đoán chi nhánh |
| `chi_nhanh_id IS NULL` 31/05, dòng sổ cái `ma_don_vi_id = X` | đóng | trigger chặn | khoá cấp pháp nhân áp cho mọi chi nhánh |
| Bản ghi THIẾT LẬP (loại 2, `ngay_khoa_so = NULL`) | mở | thành công | bản ghi lịch **không** khóa gì |
| Bản ghi đã xoá mềm | mở | thành công | `da_xoa` được tôn trọng ở cả hai |

Khẳng định tổng: **hai tầng cho cùng một kết luận trên mọi dòng.** Bản kế hoạch đầu chỉ đòi một
chiều ("DB không bao giờ chặn thứ Java cho qua") vì khi đó DB thiếu hai phạm vi; sau A1 + Q15 thì
ràng buộc chặt hơn này mới là thứ phải giữ, và nới nó ra là để hai bên trôi xa nhau.

`HoiQuyChungTuIT`: chạy lại toàn bộ test hiện có của `chung_tu_ban_hang` và `chung_tu_mua_hang` sau khi đổi chữ ký — không được đỏ thêm dòng nào.

---

## 7. BR đã áp dụng

| BR | Áp thế nào |
|---|---|
| BR01 danh sách (mốc muộn nhất) | §2 — `MAX` trên tập bản ghi áp dụng được |
| BR07 danh sách (chặn 5 thao tác) | §5 — dùng nguyên các cổng sẵn có của kernel |
| BR17 Common (kiểm tra kỳ kế toán) | Lưu / Ghi sổ / Bỏ ghi sổ đều đi qua `kiemTraKyMo`; message theo `MSG_PMKT-E-07528_026` thay cho câu chung của BR17 |
| BR42 Common (bỏ ghi sổ) | §5 — trigger phủ cả `TG_OP = 'DELETE'` |
| BR28 Common (multi-tenant) | Truy vấn luôn có `tenant_id`; `TenantContext` rỗng ⇒ trả `null` (không có thiết lập nào để đối chiếu) và RLS vẫn là chốt chặn — hành vi này giữ nguyên từ `KyKeToanChecker.java:53-58` |
| BR12 Common (trạng thái chứng từ) | Không đụng |
