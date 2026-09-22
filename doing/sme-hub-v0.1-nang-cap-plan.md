# Phương án nâng cấp — SME HUB v0.1 + ORDER callback

Ngày lập: 16/09/2026 · Phạm vi: `tenant-provisioning` (control-plane) + `integration-platform`

## Trạng thái (cập nhật 16/09/2026)

| Gói | Trạng thái | Ghi chú |
|---|---|---|
| **G1** — chốt hiệu lực đồng bộ | ✅ **XONG** | trừ khoá theo MST (§1.5) và payload-hash (§1.4, chặn bởi C1) |
| **G2** — tra cứu trả hiệu lực đã chốt | ✅ **XONG** | |
| **G3** — ORDER callback | ⛔ chưa làm | chờ C3–C5 |
| **G4** — dọn nợ | ⛔ chưa làm | |

C1 và C2 vẫn `OPEN`. C2 được hiện thực theo **hành vi đã có sẵn từ trước v0.1**
(`trangThai = HieuLuc` cho hợp đồng chỉ có addon) chứ không tự đặt luật mới — BA vẫn phải xác nhận.
C1 **không** hiện thực: hành vi re-claim bản ghi `FAILED` giữ nguyên như cũ.

## Nguồn

| # | Tài liệu | Vai trò |
|---|---|---|
| D1 | `API_nhanwebhook_SMEHub_v0.1_15.09.26.pdf` | **Bản mới** của contract webhook đăng ký |
| D2 | `Mô tả API ORDER gửi đối tác Tendoo kế toán.docx` | API **Tendoo gọi NGƯỢC ra** ORDER/SME HUB — chưa từng có |
| Đối chiếu | `pmkt-docs/ba/PMKT-E-13930_Authentication/10.api-integration/API_nhanwebhook_SMEHub.md` | Bản đang hiện thực |

⚠ D1/D2 nằm ở `Downloads`, **chưa vào `pmkt-docs/`**. Cần BA đưa vào repo và cho số phiên bản
trước khi code, nếu không sẽ không truy vết được.

---

## Phần 1 — Webhook v0.1: điểm lệch so với code hiện tại

### 1.1 `hieuLuc` trong response 202 — thay đổi NẶNG NHẤT

D1 Phần C: *"202 là cam kết"*. Response 202 phải mang:

```json
{
  "status": "ACCEPTED",
  "message": "Yêu cầu đã được tiếp nhận. Tendoo hoàn tất khởi tạo với hiệu lực dưới đây.",
  "warnings": [],
  "hieuLuc": { "packageCode": "...", "ngayBatDau": "...", "ngayKetThuc": "...", "trangThai": "HieuLuc|ChoHieuLuc" }
}
```

Hiện tại `WebhookAck.tiepNhan()` trả đúng 3 trường `httpStatus/status/message` — **không có
`warnings`, không có `hieuLuc`**.

Vấn đề thật không nằm ở DTO mà ở **thời điểm tính**:

| | Hiện tại | D1 đòi |
|---|---|---|
| Tính mốc hiệu lực | trong `DangKyDichVuService.capDangKy` — **sau** 202, trong transaction ghi | **trước** 202 |
| Lưu mốc | chỉ nằm ở `cp_goi_dich_vu_tenant` sau khi ghi xong | lưu cùng yêu cầu **trước** khi trả 202 |
| Khởi tạo ngầm | tự tính lại | phải ghi **đúng mốc đã trả** |

Tin tốt: `DangKyDichVuApi.kiemTra` đã chạy đồng bộ và đã tra catalog + đọc trạng thái gói hiện tại
của tenant — tức là **đã có đủ dữ liệu** để tính. Logic tính cũng đã tồn tại (`MocThoiHan`, hàm
`cong()`, nhánh stacking/cắt dùng thử trong `DangKyDichVuService`).

**Việc phải làm:** kéo phần tính mốc ra khỏi `capDangKy`, cho `kiemTra` trả về kèm `MocThoiHan`,
rồi `capDangKy` **nhận mốc đã chốt** làm tham số thay vì tự tính. Nếu để hai bên cùng tính, mốc
"kích hoạt ngay = now" ở hai thời điểm khác nhau sẽ lệch — và đó đúng là thứ D1 cấm.

### 1.2 `warnings` phải trả ngay ở 202

`KetQuaGd1.canhBao()` đã có sẵn ở nhánh đồng bộ (`ADDRESS_MAPPING_MISS`, `INVALID_LOAI_DANG_KY`),
nhưng hiện chỉ được nhét vào `warnings_json` để Polling đọc. Chỉ cần đưa vào `WebhookAck`. **Việc
nhỏ**, làm cùng 1.1.

### 1.3 Polling (Phần D) phải trả `warnings` + `hieuLuc` ở cả 3 trạng thái

`WebhookStatusResponse` hiện có `warnings` nhưng **thiếu `hieuLuc`**, và `dangXuLy()` /
`thatBai()` đang trả `warnings = null`. D1 nói rõ: *"warnings và hieuLuc ở cả ba trạng thái là
đúng giá trị đã trả trong response 202"*.

Thông báo trạng thái FAILED cũng đổi nghĩa:

| | Hiện tại | D1 |
|---|---|---|
| message | "Không thể khởi tạo hệ thống. Vui lòng thử lại hoặc liên hệ Tendoo." | "Khởi tạo đang được Ops Tendoo xử lý. SME HUB không cần gửi lại." |

404 `NOT_FOUND` đã đúng sẵn (`SmeHubWebhookController` + `ResourceNotFoundException`).

### 1.4 Replay khác payload → 202, KHÔNG xử lý lại (mâu thuẫn với code hiện tại)

D1 Phần A: *"replay cùng maHopDongHub nhưng nội dung payload KHÁC bản đã xử lý → vẫn trả 202 và
KHÔNG xử lý lại; Tendoo ghi log cảnh báo nội bộ (payload-hash mismatch)"*.

Code hiện tại đi **ngược lại** một cách có chủ đích. `SubscriptionWebhookService.tuChoi()` ghi rõ:

> *"400 thì không retry" trong contract nói với HUB rằng đừng gửi lại Y NGUYÊN, không phải rằng
> cửa đã đóng vĩnh viễn* — bản ghi rơi về `FAILED` để lần gửi lại (payload đã sửa) re-claim được.

Đây là **mâu thuẫn P1, phải BA chốt** — xem §Mâu thuẫn bên dưới.

### 1.5 Thứ tự xử lý theo doanh nghiệp

D1: *"Các webhook của cùng doanh nghiệp được xử lý lần lượt; mỗi webhook nhìn thấy kết quả của
những webhook đã xử lý xong trước nó"*.

Hiện tại `SubscriptionWebhookProcessor.xuLyNgam` chạy trên pool `webhookExecutor` — **song song,
không khoá theo MST**. Hai webhook cùng MST tới gần nhau có thể đọc cùng một trạng thái gói và
cùng "kích hoạt ngay", phá vỡ stacking.

D1 có nới: *"Với các webhook gửi gần như đồng thời, Tendoo không cam kết xử lý theo thứ tự gửi"* —
nhưng vẫn cam kết **không bao giờ trả `hieuLuc` sai**. Vì `hieuLuc` giờ chốt ở nhánh **đồng bộ**,
chỗ cần tuần tự hoá là `kiemTra` + ghi mốc, không phải toàn bộ khâu ngầm.

Có sẵn `BR-DKWEB-30` dùng partial unique index chống đua dùng thử. Cùng cách: khoá theo MST
(`SELECT ... FOR UPDATE` trên `cp_tenant_directory`, hoặc advisory lock theo hash MST) bọc quanh
đoạn tính-và-chốt mốc.

### 1.6 Không đổi

Chữ ký HMAC (`X-Hub-Signature`, `ts + "." + body`), cửa sổ ±5 phút, tách
`INVALID_TIMESTAMP`/`INVALID_SIGNATURE`, rate limit 100/min (webhook) và 300/min (status), danh mục
lỗi `errors[]`, BR-DKWEB-23→31 — **đã khớp**. `integration-platform` chuyển nguyên body nên mọi
trường mới tự động ra tới HUB, không phải sửa gì ở đó cho Phần 1.

---

## Phần 2 — ORDER callback (D2): hoàn toàn mới

Sau khi xử lý xong đăng ký, Tendoo phải **POST ngược** kết quả về ORDER.

```
POST http://10.207.252.26:8168/order/tendoo-accounting/api/receive-result
{
  "providerOrderId": "<= maHopDongHub>",
  "status": "OK" | "NOK",
  "metadata": { "tendooAccountingExpiredDate": "yyyy-MM-dd" }   // bắt buộc khi OK
}
→ { "message": "...", "errorCode": "0" }   // "0" = thành công
```

Hiện **không có một dòng code nào** cho đường này.

Chủ sở hữu rõ ràng theo kiến trúc: **`integration-platform`** giữ mọi biên ngoài (đúng như
`SmeHubWebhookForwarder` gọi vào control-plane theo chiều ngược lại). Control-plane phát sự kiện,
integration-platform gọi ra.

`tendooAccountingExpiredDate` = `hieuLuc.ngayKetThuc` rút về `yyyy-MM-dd` — **phụ thuộc Phần 1**,
nên phải làm 1.1 trước.

Đường dẫn đang là IP:port trần trong tài liệu → phải vào `application.yml` qua env, không hardcode
(luật 1).

---

## Phương án triển khai

Thứ tự bắt buộc: **G1 → G2 → G3**; G4 chạy song song được.

### G1 — Chốt hiệu lực ở nhánh đồng bộ (nền của mọi thứ còn lại)

1. `V18__cp_webhook_idempotency_hieu_luc.sql`: thêm `hieu_luc_json jsonb`, `payload_hash varchar(64)`.
   (Slot V18 đang trống — upstream dừng ở V17.)
2. `KetQuaKiemTra` mang thêm `MocThoiHan` (ngayBatDau/ngayKetThuc/trangThai/packageCode).
3. Tách phần tính mốc khỏi `DangKyDichVuService.capDangKy` → dùng chung cho `kiemTra`;
   `capDangKy(yeuCau, tenantId, mocDaChot)`.
4. Lưu `hieu_luc_json` **trước** khi trả 202.
5. `WebhookAck.tiepNhan(warnings, hieuLuc)`.
6. Khoá theo MST quanh đoạn tính-và-chốt (§1.5).

### G2 — Polling đọc lại giá trị đã chốt

`WebhookStatusResponse` thêm `hieuLuc`; cả 3 trạng thái đọc từ `hieu_luc_json` + `warnings_json`;
đổi message FAILED.

### G3 — ORDER callback

Module mới trong `integration-platform` (`service/OrderResultNotifier` + config endpoint/timeout/
retry theo mẫu `SmeHubWebhookForwarder`: resilience4j `retry`/`circuitbreaker`/`ratelimiter`).
Control-plane bắn sự kiện qua outbox (`cp_outbox_event` đã có) để callback **không** nằm trong
transaction ghi dữ liệu.

### G4 — Dọn nợ đang tồn (độc lập, nên làm cùng đợt)

- **`OnboardingReconciler` đọc sai kiểu payload** (đã báo ở phiên này): bản ghi webhook đăng ký
  lưu raw body của HUB nhưng reconciler parse thành `OwnerOnboardingRequest` → null toàn bộ →
  `cp_tenant_directory.ma` NOT NULL. 3 bản ghi `LOCAL-HUB-543973769/545033156/545196759` đang kẹt
  vì lỗi này.
- **Thiếu mã truy vết** ở BR-DKWEB-01/01b, 04, 08, 15, 16, 17, 22.
- **Thiếu test** cho `SubscriptionWebhookService`, `SubscriptionWebhookProcessor`,
  `SubscriptionWebhookTxOps`, `ReferralService`.

---

## Mâu thuẫn / câu hỏi phải BA chốt trước khi code

| # | Mức | Vấn đề |
|---|---|---|
| C1 | **P1** | §1.4 — replay khác payload: luật mới có áp cho bản ghi đang ở `FAILED` (đã bị 400) không? Code hiện cho phép HUB sửa payload rồi gửi lại cùng `maHopDongHub`. Nếu áp cứng thì mọi payload sai **vĩnh viễn** không sửa được trừ qua Ticket Ops. Chặn G1. |
| C2 | **P1** | Hợp đồng **chỉ có addon**: `hieuLuc.packageCode = null` và `ngayKetThuc` = ngày kết thúc gói chính đang chạy. Nhưng `trangThai` lấy gì? D1 không nói. |
| C3 | **P2** | D2 — gửi `NOK` khi nào? Chỉ khi khâu ngầm hỏng, hay cả khi webhook bị từ chối 400 ngay từ đầu (lúc đó chưa có `hieuLuc`)? |
| C4 | **P2** | D2 — xác thực chiều gọi ra ORDER? Tài liệu không có header auth nào. Gọi trần qua HTTP IP nội bộ? |
| C5 | **P2** | D2 — `errorCode != "0"` thì retry bao nhiêu lần, backoff bao lâu, hết cửa sổ thì sao? |
| C6 | **P2** | D1 §1.3 — `FAILED` giờ mang nghĩa "Ops đang xử lý, đừng gửi lại", trùng nghĩa `ABANDONED` hiện tại. Gộp hai trạng thái hay giữ hai? |

**Chưa chốt C1 và C2 thì chưa được bắt đầu G1** — theo §Cổng đặc tả, mục P1 còn `OPEN` là cấm code
các luật bị nó chặn.

---

## Bước kế tiếp đề nghị

1. BA đưa D1/D2 vào `pmkt-docs/ba/PMKT-E-13930_Authentication/10.api-integration/` kèm số phiên bản.
2. Chạy `/audit-spec` trên thư mục đó → sinh `01-conflict.md` (nạp sẵn C1–C6), `02-rules.md`.
3. BA chốt C1, C2 → `/plan-be` → `/gen-be`.

Tài liệu này **không thay thế** `/audit-spec`: nó là bản đối chiếu nhanh để thấy khối lượng và
chỗ vướng, chưa phải đặc tả nguyên tử có mã `R-…`/`INV-…`.
