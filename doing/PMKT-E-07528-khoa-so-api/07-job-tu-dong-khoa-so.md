# F07 — Job khóa sổ tự động

> Quay lại [00-ke-hoach-tong.md](00-ke-hoach-tong.md)

| Mục | Nội dung |
|---|---|
| Nguồn BA | BR04–BR07 của `SCR_ThietLapNgayKhoaSo.md` · BR02, BR03, BR05 của `SCR_XemDanhSachThietLapKhoaSo.md` · `7.glossary.md` (Chu kỳ khóa sổ, Độ trễ thực thi) |
| Use case | Phần "tạo job scheduler" của `U-09193`, `U-09194`, `U-09195` |
| Endpoint | **Không có** — job chạy nền. Cấu hình vào hệ thống qua A4/A5 |
| Lớp chính | `internal/job/KhoaSoTuDongJob.java` + `internal/service/business/ChuKyKhoaSoCalculator.java` |

---

## 0. Các mục không áp dụng cho chức năng này

| Mục chuẩn | Trạng thái |
|---|---|
| **Hợp đồng API** | **Không áp dụng** — job chạy nền, không có endpoint. Cấu hình vào hệ thống qua **A4/A5** ([F02](02-tao-thiet-lap-khoa-so.md), [F03](03-chinh-sua-thiet-lap.md)); kết quả job đọc qua **A1** ([F01](01-xem-danh-sach-thiet-lap.md)) dưới dạng bản ghi `loaiKhoaSo = 3` |
| **Ánh xạ cột BA ↔ DB ↔ DTO** | **Không áp dụng cho request** (không có). Cột DB mà job **ghi**: `ngay_khoa_so`, `loai_khoa_so = 3`, `moc_chay_ke_tiep`, `lan_chay_gan_nhat`, `nguoi_cap_nhat`, `ngay_cap_nhat`, `phien_ban` — xem §3.2 và §4.3 |
| **Validation** | **Không áp dụng** — không có đầu vào người dùng. Cấu hình đã được validate ở A4/A5 (V3…V9, [F02 §3.1](02-tao-thiet-lap-khoa-so.md)) **trước khi** nằm trong DB. Job chỉ có hai điều kiện chạy: BR02 (§4.1) và "không còn chứng từ chưa ghi sổ" (§4.2) |
| **Phân trang · sắp xếp · lọc · dòng tổng** | **Không áp dụng** — không phải màn danh sách. Có một giới hạn lô: `pmkt.khoa-so.lo-moi-lan` (§7) |

---

## 1. Hai mốc thời gian khác nhau — đọc kỹ trước khi code

BA tách rất rõ (BR06 + BR07 của `SCR_ThietLapNgayKhoaSo.md:109-124`) hai khái niệm mà tên gọi rất dễ lẫn:

| Khái niệm | Là gì | Lưu ở đâu |
|---|---|---|
| **Mốc chốt dữ liệu** | Ngày mà chứng từ có `ngay_hach_toan <=` nó sẽ bị khóa | Ghi vào `ngay_khoa_so` của bản ghi **KẾT QUẢ** (loại 3) khi job chạy |
| **Thời điểm thực thi** | Lúc job thật sự chạy = mốc chốt + độ trễ + giờ | Lưu ở `moc_chay_ke_tiep` của bản ghi **THIẾT LẬP** (loại 2) |

Công thức BR07: **`Thời điểm chạy = [Ngày chốt dữ liệu] + [Số ngày độ trễ] + [Giờ]`**

Hai ví dụ nguyên văn của BA:
- *Hàng ngày*: "Khóa sổ đến hết 18:00 hàng ngày, thời gian thực hiện sau 1 ngày" → chốt dữ liệu đến 18:00 ngày T, job chạy 18:00 ngày **T+1**.
- *Hàng tháng*: "Khóa sổ đến hết ngày 31 hàng tháng, thực hiện sau **-3** ngày, lúc 02:00" → chốt dữ liệu đến 23:59:59 ngày 31, job chạy 02:00 sáng ngày **28**.

> ⚠️ Ví dụ hàng tháng cho thấy job có thể chạy **TRƯỚC** mốc chốt dữ liệu. Nghĩa là job khóa tới một ngày **trong tương lai**. Điều này hợp lệ theo BR01 (*"Nếu chọn ngày ở tương lai/hiện tại: hiểu là Khóa sổ tính đến thời điểm đó"* — `SCR_ThietLapNgayKhoaSo.md:90`) và **không được** thêm luật "ngày khóa sổ phải ≤ hôm nay" ở bất kỳ đâu.

---

## 2. Tính mốc chốt dữ liệu (`ChuKyKhoaSoCalculator`)

| `kyKhoaSo` | `giaTriKy` | Mốc chốt dữ liệu của chu kỳ chứa ngày `T` | Phần giờ |
|---|---|---|---|
| **1 — Hàng ngày** | không dùng | chính ngày `T` | `gioThucThi` (BR06: *"Khóa sổ đến hết đúng `[Giờ]` của ngày khóa sổ"*) |
| **2 — Hàng tuần** | 1..7 (T2..CN) | ngày trong tuần khớp `giaTriKy` của tuần đang xét | **23:59:59** (BR06) |
| **3 — Hàng tháng** | 1..31, **32 = ngày cuối tháng** (**Q2**) | ngày trong tháng khớp `giaTriKy`; `32` → ngày cuối tháng thật | **23:59:59** (BR06) |

Hai ca biên bắt buộc phải cài đúng:

| Ca | Xử lý | Vì sao |
|---|---|---|
| `giaTriKy = 31` nhưng tháng có 28/29/30 ngày | Dùng **ngày cuối tháng thật** | `LocalDate.of(2026, 2, 31)` ném `DateTimeException`. Người dùng chọn "ngày 31" nghĩa là "cuối tháng" trong tháng ngắn — hành vi này phải được **test pin**, không để mỗi lần refactor lại đổi |
| `giaTriKy = 32` (ngày cuối tháng) | `YearMonth.from(T).atEndOfMonth()` | Hằng `HangSoKhoaSo.NGAY_CUOI_THANG = 32`, **không** viết số 32 rải rác |

**Khoảng độ trễ hợp lệ** (BR06 — **Q1**, ba nguồn BA đang nói khác nhau):

| `kyKhoaSo` | Khoảng | Nguồn |
|---|---|---|
| Hàng ngày | `0 … 31` (**không âm**) | BR06 dòng 113: *"Là số nguyên **≥ 0** (không áp dụng số âm cho chu kỳ hàng ngày)"* |
| Hàng tuần | `-7 … 7` | BR06 dòng 116 |
| Hàng tháng | `-31 … 31` | BR06 dòng 119 |

Ghi chú xung đột (đã đưa vào **Q1**): phần "Ghi chú về giá trị độ trễ" ở `SCR_ThietLapNgayKhoaSo.md:52-54` nói `-31…31` cho mọi chu kỳ, còn `UC_ThietLapTuDongKhoaSoHeThong.md:11` nói `0-7 ngày`. Plan lấy **BR06** vì đó là mục duy nhất phân biệt theo chu kỳ và có ví dụ đi kèm.

---

## 3. Kiến trúc job

### 3.1 Vì sao poller thay vì trigger-per-setting (D7)

```yaml
# cell-app/src/main/resources/application.yml:52-54
# WORKER role uses Quartz (in-memory store). Jobs registered only under the 'worker' profile.
quartz:
  job-store-type: ${SPRING_QUARTZ_JOB_STORE_TYPE:memory}
```

Hiện trạng: Quartz starter **có** trong `build.gradle.kts:51`, nhưng **không lớp Java nào dùng** (`grep -rln "@Scheduled\|org.quartz" src/main/java` → rỗng) và **không có `@EnableScheduling`**. Đây là greenfield hoàn toàn.

| | A — mỗi thiết lập một Quartz trigger | **B (chọn) — MỘT poller quét bảng thiết lập** |
|---|---|---|
| JobStore `memory` + nhiều instance | **Mỗi instance có scheduler riêng ⇒ job chạy trùng N lần** | Poller cũng chạy N lần, nhưng `SELECT … FOR UPDATE SKIP LOCKED` bảo đảm mỗi thiết lập chỉ được **một** instance xử lý |
| Người dùng sửa/xoá thiết lập | Phải đồng bộ vòng đời trigger với vòng đời bản ghi (tạo/sửa/xoá/khôi phục) — 4 điểm dễ quên | Poller đọc DB mỗi lần chạy ⇒ **không có gì để đồng bộ** |
| Chuyển sang JobStore JDBC sau này | Có, nhưng thêm 11 bảng `qrtz_*` + migration | Không cần |
| Khởi động lại app | Trigger phải nạp lại từ DB thủ công | Không mất gì |
| Rủi ro | Chạy trùng ⇒ khóa sổ hai lần (may là idempotent, nhưng audit log nhân đôi và BR02 so sai) | Độ chính xác thời điểm chạy chỉ tới **chu kỳ poll**. Chốt an toàn: poll **mỗi 5 phút**, hằng `KHOANG_QUET_MS`; BA không yêu cầu chính xác tới giây |

Chọn **B**. Cụ thể: `@Scheduled(fixedDelayString = "${pmkt.khoa-so.khoang-quet-ms:300000}")` + `@EnableScheduling` bật **chỉ ở profile `worker`** (đúng ghi chú sẵn có trong `application.yml:52`), để instance phục vụ HTTP không chạy job.

### 3.2 Cột phục vụ job

| Cột (thêm mới — [09-thiet-ke-db.md §3](09-thiet-ke-db.md)) | Kiểu | Ai ghi | Vai trò |
|---|---|---|---|
| `moc_chay_ke_tiep` | `timestamptz` | server tính | Thời điểm job phải chạy lần tới. Là **khoá lọc** của truy vấn "tới hạn" ⇒ có index |
| `lan_chay_gan_nhat` | `timestamptz` | server tính | Truy vết + chống chạy lặp trong cùng một chu kỳ |

Cả hai **chỉ có giá trị trên bản ghi THIẾT LẬP** (`loai_khoa_so = 2`). Bản ghi kết quả để `NULL`.

Điều kiện tới hạn:
```sql
   da_xoa = false
   AND loai_khoa_so = 2          -- LoaiKhoaSo.THIET_LAP, bản ghi LỊCH
   AND is_tu_dong = true
   AND moc_chay_ke_tiep IS NOT NULL
   AND moc_chay_ke_tiep <= :bayGio
 ORDER BY moc_chay_ke_tiep
 LIMIT :loMotLan
```

> ⚠️ **Điều kiện này chạy CẮT NGANG tenant** — đó là điều RLS sinh ra để ngăn. Bản cài đặt vì vậy
> **không** phải một `SELECT` trần mà là `fn_khoa_so_thiet_lap_toi_han(:bayGio, :lo)` — xem §5.1.

`FOR UPDATE SKIP LOCKED` **không** nằm ở câu này mà ở vòng trong, trên đúng dòng sắp xử lý
(`KhoaSoTuDongXuLy`): đó mới là chỗ có transaction để giữ khoá. Nó là điểm serialize — instance thứ
hai bỏ qua dòng đang bị instance thứ nhất giữ, thay vì đợi rồi xử lý lại.

### 3.3 `moc_chay_ke_tiep` được tính lại ở đâu

Đúng ba nơi, không hơn:

1. **A4** khi tạo thiết lập với `isTuDong = true`.
2. **A5** khi sửa thiết lập (đổi chu kỳ / độ trễ / giờ).
3. **Cuối mỗi lần job xử lý xong** một thiết lập — kể cả khi lần đó bị bỏ qua theo BR02.

Điểm 3 là điểm dễ quên nhất: nếu bỏ qua mà không dời `moc_chay_ke_tiep`, poller sẽ **quét lại chính thiết lập đó mỗi 5 phút mãi mãi**.

---

## 4. Một lượt xử lý một thiết lập

```
① Nạp thiết lập (đã FOR UPDATE SKIP LOCKED)
② mocChotDuLieu = ChuKyKhoaSoCalculator.mocChot(kyKhoaSo, giaTriKy, gioThucThi, thoiDiemChay)
③ mocHienTai   = mốc khóa sổ ĐANG hiệu lực của ĐÚNG phạm vi này (bản ghi KẾT QUẢ cùng pham_vi_hash)
④ BR02: nếu mocChotDuLieu <= mocHienTai  ⇒ BỎ QUA (log INFO), sang ⑧
⑤ Quét chứng từ chưa ghi sổ trong phạm vi (ChungTuChoXuLyPort.dem)
     · soLuong > 0  ⇒ BỎ QUA lần chạy này + log WARN + (tương lai) notification BR05 — Q3
⑥ Ghi đè bản ghi KẾT QUẢ cùng phạm vi: loai_khoa_so = 3, ngay_khoa_so = mocChotDuLieu
     (chưa có bản ghi kết quả nào ⇒ INSERT mới)
⑦ lan_chay_gan_nhat = thoiDiemChay
⑧ moc_chay_ke_tiep = thời điểm chạy của chu kỳ KẾ TIẾP
```

### 4.1 Bước ④ — BR02 nguyên văn

`SCR_XemDanhSachThietLapKhoaSo.md:64-66`:
> *Khi đến lịch chạy, Job tự động chỉ thực hiện khóa sổ nếu ngày khóa sổ tính được **lớn hơn** ngày khóa sổ hiện tại đang áp dụng cho cùng đối tượng (cùng phạm vi). Nếu ngày khóa sổ mới ≤ ngày hiện tại, Job bị bỏ qua.*

Hai chi tiết quyết định tính đúng:

- **"cùng đối tượng (cùng phạm vi)"** ⇒ so với bản ghi kết quả có **cùng `pham_vi_hash`**, **không** phải với `MAX(ngay_khoa_so)` toàn tenant. Nếu so với MAX toàn tenant thì một thiết lập "Toàn hệ thống" khóa xa sẽ vô hiệu hoá vĩnh viễn mọi job theo loại chứng từ.
- **so `<=`, không phải `<`** ⇒ chạy lại đúng cùng mốc thì bỏ qua. Đây là chốt idempotent thứ hai (cùng với `SKIP LOCKED`): job chạy trùng do bất kỳ lý do gì cũng không sinh bản ghi thứ hai.

### 4.2 Bước ⑤ — chứng từ chưa ghi sổ, và giới hạn của phiên bản này

BR05 (`SCR_XemDanhSachThietLapKhoaSo.md:77-79`):
> *Khi Job tự động chạy và phát hiện có chứng từ chưa ghi sổ trong phạm vi khóa, hệ thống sẽ gửi notification đến Kế toán trưởng… **Lưu ý:** Chức năng notification này hệ thống chưa hỗ trợ ở phiên bản hiện tại, sẽ được phát triển sau.*

BA nói rõ notification chưa hỗ trợ, **nhưng không nói job phải làm gì** trong tình huống đó. Hai lựa chọn:

| | A — bỏ qua lần chạy, log WARN | B — khóa sổ luôn, kệ chứng từ chưa ghi sổ |
|---|---|---|
| Nhất quán với luồng thủ công | ✅ — thủ công cũng bị chặn (MSG_008) | ❌ — cùng một nghiệp vụ, hai kết quả khác nhau tuỳ ai kích hoạt |
| Hệ quả nếu sai | Kỳ không được khóa, người dùng phát hiện muộn (vì chưa có notification) | Chứng từ chưa ghi sổ bị kẹt vĩnh viễn trong kỳ đã khóa — **phải bỏ khóa mới sửa được**, và bỏ khóa cũng bị BR07 chặn |

Chọn **A**, và ghi vào **Q3** để BA xác nhận. Chốt an toàn tối thiểu cho tới khi có notification: ghi một dòng log `WARN` có cấu trúc (tenant, thiết lập id, số chứng từ, mốc bỏ qua) để vận hành dựng cảnh báo từ log.

Hạ tầng notification đã sẵn sàng (`common/notice/api/NoticeIssuerService.java`) — khi BA chốt nội dung thì chỉ là một lời gọi, không phải một epic.

### 4.3 Bước ⑥ — ghi đè bản ghi kết quả

Dùng **đúng** đường ghi đè của [F02 §3.3](02-tao-thiet-lap-khoa-so.md), khác đúng hai điểm: `loai_khoa_so = 3` và `nguoi_cap_nhat = null` (không có người dùng nào thao tác).

`BaseEntity.onUpdate()` lấy actor từ `TenantContext.userId()` (`BaseEntity.java:61`) — trong job thì `Optional` rỗng nên `nguoiCapNhat` giữ giá trị cũ. Điều đó **sai về mặt truy vết**: bản ghi sẽ mang tên người sửa lần trước dù lần này là hệ thống sửa. Hai cách:

| | A — chấp nhận, dựa vào `aud_audit_log` để truy vết | **B (chọn) — bind một "user hệ thống" vào `TenantContext` khi job chạy** |
|---|---|---|
| Truy vết trên chính bản ghi | Sai lệch | Đúng — `nguoi_cap_nhat` = id user hệ thống |
| Chi phí | 0 | Cần một UUID hằng cho "hệ thống" (hoặc `null` tường minh) |
| Rủi ro | Người đọc danh sách hiểu nhầm ai khóa sổ | User hệ thống phải **không** đăng nhập được. Chốt an toàn: dùng UUID cố định khai ở `HangSoKhoaSo.NGUOI_DUNG_HE_THONG`, không tạo tài khoản trong Keycloak |

Chọn **B**. Cột `loai_khoa_so = 3` (Tự động) trên màn danh sách đã nói rõ đây là job, nên đây chỉ là lớp truy vết thứ hai — nhưng nó rẻ và đúng.

---

## 5. Tenant và RLS trong job (R4)

Job chạy **ngoài request** ⇒ không có `TenantFilter` nào bơm `TenantContext`. Nếu chạy transaction mà không bind tenant:

- `TenantRlsAspect` bind GUC theo `TenantContext` ⇒ GUC rỗng ⇒ policy `tenant_isolation` (`V1__baseline.sql:7564`) khớp 0 dòng ⇒ **truy vấn trả rỗng, job im lặng không làm gì**;
- và nếu có ghi được thì `TenantedEntity.onTenantedCreate()` ném `IllegalStateException` (`TenantedEntity.java:25`) — may mà nó ném chứ không ghi bừa.

⇒ Cấu trúc bắt buộc:

```
Vòng NGOÀI  — không transaction, không RLS:
    lấy danh sách tenantId có thiết lập tới hạn
      · truy vấn này phải chạy bằng vai DB BỎ QUA RLS, hoặc bằng một bảng chỉ mục không RLS
Vòng TRONG  — mỗi tenant:
    TenantContext.set(tenantId)  →  @Transactional  →  ①..⑧  →  TenantContext.clear()
```

Vòng ngoài là điểm nhạy cảm nhất của toàn epic: nó **cố ý** đọc cắt ngang tenant. Ba ràng buộc bắt buộc:

1. Đúng **một** lời gọi được phép làm việc này, javadoc ghi rõ lý do.
2. Nó chỉ được lấy `tenant_id, id` — **không** đọc dữ liệu nghiệp vụ nào khác.
3. `TenantContext.clear()` đặt trong `finally` — rò tenant sang lượt sau là rò dữ liệu giữa các công ty.

### 5.1 ✅ Đã chốt và đã cài — `fn_khoa_so_thiet_lap_toi_han` (V361)

Chọn phương án **(b)** như đề xuất: một function `SECURITY DEFINER`, không cấp thêm vai DB.
`pmkt_app` bị `FORCE ROW LEVEL SECURITY` (`V1__baseline.sql:1174`) nên `SELECT` trần trả 0 dòng —
job im lặng không làm gì, đúng kiểu hỏng không ai phát hiện.

**Function LẶP qua từng tenant, không `SELECT` một phát.** Hai lý do, cả hai đều là chặn cứng chứ
không phải sở thích:

- `FORCE ROW LEVEL SECURITY` áp RLS cho **cả owner**, nên `SECURITY DEFINER` một mình không đủ.
  Chỉ superuser mới bypass, và không được phép giả định owner là superuser.
- Policy so bằng **một** giá trị (`tenant_id = fn_current_tenant()`) nên không có cách nào khớp
  nhiều tenant trong một lần đọc.

**Vì sao không thêm một policy permissive** kiểu `current_setting('app.khoa_so_job') = 'on'`: policy
đó do `pmkt_app` kích hoạt được, mà `pmkt_app` cũng là role phục vụ HTTP — bất kỳ đoạn code nào lỡ
set GUC đó là mở toang một lỗ đọc xuyên tenant. Vòng lặp không có cửa đó.

Ba chốt chặn trong function:

1. `WHERE c.tenant_id = v_tenant` **tường minh** — đúng kể cả khi owner LÀ superuser và RLS bị bỏ
   qua hoàn toàn; thiếu nó thì mỗi vòng lặp trả về toàn bộ bảng ⇒ nhân bản N lần.
2. Chỉ trả `(tenant_id, thiet_lap_id, moc_chay_ke_tiep)`.
3. `REVOKE ALL FROM PUBLIC` + `GRANT EXECUTE` riêng `pmkt_app`.

**Công bằng giữa các tenant:** gom tối đa `p_lo` dòng **mỗi** tenant rồi sắp xếp **toàn cục** theo
`moc_chay_ke_tiep` và mới cắt `p_lo`. Cắt ngay trong vòng lặp sẽ khiến tenant có `id` nhỏ ăn hết
hạn ngạch và các tenant còn lại không bao giờ tới lượt.

**`FOR UPDATE SKIP LOCKED` chuyển vào vòng TRONG**, trên đúng dòng đang xử lý — vòng ngoài không
giữ khoá nào (nó không có transaction dài để giữ).

**Đã kiểm trên DB dev:** dựng 2 thiết lập tới hạn ở 2 tenant, **không bind tenant** → function trả
2 dòng của 2 tenant khác nhau, `p_lo = 1` trả đúng 1 dòng, GUC `app.tenant_id` không bị rò sau lời
gọi (đã rollback, không để lại dữ liệu). **Chưa chứng minh được** phần vượt `FORCE RLS` dưới đúng
vai `pmkt_app`: trên DB dev, role `pmkt_dev` có `rolbypassrls = true` và không `SET ROLE pmkt_app`
được. Cần xác nhận lại ở môi trường CI/staging.

### 5.2 Bước xử lý phải là một bean RIÊNG

`KhoaSoTuDongXuLy.xuLyMotThietLap` tách khỏi `KhoaSoTuDongJob` vì lý do kỹ thuật, không phải thẩm mỹ:
để cùng lớp thì lời gọi là gọi thẳng trên `this`, **không qua proxy Spring**, và
`@Transactional(REQUIRES_NEW)` mất hiệu lực. Hệ quả dây chuyền: `FOR UPDATE SKIP LOCKED` không giữ
khoá quá một statement (hai instance cùng xử lý một thiết lập), GUC tenant không được bind nên RLS
trả tập rỗng, và ba lần `saveAndFlush` chạy ở ba transaction ngầm rời rạc — hỏng nửa chừng là để
lại bản ghi kết quả mà không dời được `moc_chay_ke_tiep`.

---

## 6. Kiểm thử

### 6.1 Unit test (`@Tag("unit")`) — `ChuKyKhoaSoCalculatorTest`

Toàn bộ lớp này thuần JVM (nhận `Clock` qua constructor — `core/config/ClockConfig.java` đã cấp bean sẵn, **không** gọi `Instant.now()` trong thân hàm).

| Ca | Đầu vào | Mốc chốt | Thời điểm chạy |
|---|---|---|---|
| Hàng ngày, độ trễ 0, 18:00 | T = 15/06/2026 | 15/06 18:00 | 15/06 18:00 |
| Hàng ngày, độ trễ 1, 18:00 *(ví dụ BR07)* | T = 15/06/2026 | 15/06 18:00 | **16/06 18:00** |
| Hàng tuần, thứ 6, độ trễ 0 | tuần chứa 15/06/2026 | 19/06 23:59:59 | 19/06 tại `gioThucThi` |
| Hàng tuần, thứ 2, độ trễ −2 | tuần chứa 15/06 | 15/06 23:59:59 | **13/06** |
| Hàng tháng, ngày 31, độ trễ −3, 02:00 *(ví dụ BR07)* | tháng 5/2026 | 31/05 23:59:59 | **28/05 02:00** |
| Hàng tháng, ngày 31, tháng 2 (28 ngày) | tháng 2/2026 | **28/02** 23:59:59 | theo độ trễ |
| Hàng tháng, ngày 31, tháng 2 nhuận | tháng 2/2028 | **29/02** 23:59:59 | theo độ trễ |
| Hàng tháng, `giaTriKy = 32` | tháng 4/2026 | **30/04** 23:59:59 | theo độ trễ |
| Độ trễ ngoài khoảng theo chu kỳ | — | ném lỗi V9 | — |

Thêm `MocChayKeTiepTest`: sau mỗi lượt xử lý (kể cả lượt bị bỏ qua theo BR02) `moc_chay_ke_tiep` **luôn** tiến về phía trước, không đứng yên.

Thêm `Br02BoQuaTest`: mốc mới `<` mốc hiện tại → bỏ qua · `=` → bỏ qua · `>` → thực hiện.

### 6.2 Test tích hợp (cần Docker)

`KhoaSoTuDongJobIT`:
- **Hai luồng chạy poller đồng thời** trên cùng một thiết lập tới hạn → đúng **một** bản ghi kết quả được ghi (chứng minh `FOR UPDATE SKIP LOCKED`).
- Job xử lý 2 tenant → mỗi tenant chỉ thấy dữ liệu của mình; sau khi job xong, `TenantContext` rỗng.
- Thiết lập bị xoá mềm giữa hai lần poll → lần poll sau không quét thấy nữa.
- Phạm vi có 3 chứng từ chưa ghi sổ → job bỏ qua, `ngay_khoa_so` **không đổi**, `moc_chay_ke_tiep` vẫn tiến (§4.2).
- Bản ghi kết quả do job sinh có `loai_khoa_so = 3` và hiển thị đúng ở A1.

---

## 7. Cấu hình

| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `pmkt.khoa-so.khoang-quet-ms` | `300000` (5 phút) | Chu kỳ poll — §3.1 |
| `pmkt.khoa-so.lo-moi-lan` | `50` | Số thiết lập xử lý tối đa mỗi lượt poll, chặn một lượt chạy quá dài |
| `pmkt.khoa-so.bat-job` | `true` | Cờ tắt job không cần đổi profile (dùng khi vận hành cần dừng khẩn) |

Đọc qua `@ConfigurationProperties`, **không** `@Value` rải rác; không hardcode `300000` trong annotation ngoài chuỗi placeholder có mặc định.

---

## 8. BR đã áp dụng

| BR | Áp thế nào |
|---|---|
| BR04 popup (hiển thị section tự động) | Không thuộc BE |
| BR05 popup (kế thừa đối tượng thiết lập) | Job dùng chính phạm vi lưu trên bản ghi thiết lập |
| BR06 popup (mốc chốt dữ liệu + khoảng độ trễ) | §2 — `ChuKyKhoaSoCalculator` |
| BR07 popup (thời điểm thực thi = chốt + trễ + giờ) | §2, §4, test §6.1 dùng đúng 2 ví dụ của BA |
| BR02 danh sách (điều kiện thực thi job) | §4.1 — so **theo cùng phạm vi**, toán tử `<=` |
| BR03 danh sách (ghi đè, loại đổi thành Tự động) | §4.3 |
| BR05 danh sách (notification job thất bại) | **Chưa đạt** — BA đã ghi chưa hỗ trợ; §4.2 tạm log WARN có cấu trúc, chờ **Q3** |
| BR28 Common (multi-tenant) | §5 — bind tenant từng lượt, `clear()` trong `finally` |
| BR46 Common (trường hệ thống) | §4.3 — `nguoi_cap_nhat` = user hệ thống |
