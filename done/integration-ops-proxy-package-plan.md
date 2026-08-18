# Kế hoạch triển khai package `integration_ops.proxy` — gọi API sang hệ thống ngoài

> Vị trí: `../../cell-app/src/main/java/vn/dopai/pmkt/cell/integration_ops/proxy`
> Thay thế bản nháp cũ đặt ở `common/proxy` (đã xoá).

## Trạng thái triển khai

**Phase 0–3 ĐÃ XONG** (đồng bộ + circuit breaker + retry ≤ 3 lượt + bất đồng bộ không bền).
Phase 4 (hàng đợi bền) và Phase 5 (migrate 2 adapter cũ) chưa làm — theo đúng đề xuất §18 mục 1 và 4.

### Code mẫu

`cell-app/src/test/.../integration_ops/proxy/vidu/` — adapter hoàn chỉnh cho một đối tác hoá đơn điện
tử giả định (`HoaDonDienTuApi` cổng + `HoaDonDienTuRest` adapter + test). **Chép file `HoaDonDienTuRest`
làm khuôn khi viết adapter mới.** Đặt ở `src/test` vì đối tác đó không có thật, nhưng nó được biên
dịch và chạy nên không mục theo thời gian như code dán trong tài liệu.

**Chưa có caller ở production**: không module nghiệp vụ nào đang import `ProxyClient`. Caller thật
đầu tiên sẽ là Phase 5 (migrate `ControlPlaneToChucRest`).

| Kiểm chứng | Kết quả |
|---|---|
| `cd cell-app && ./gradlew unitTest` | **377 test xanh**, 0 đỏ — trong đó 67 test của proxy + code mẫu |
| `cd cell-app && ./gradlew build` | Đỏ ở đúng 7 lớp Testcontainers (`RedisCache*`, `FileStorage*`, `ToChucNhomCellMigrationTest`) vì **máy dev chưa có Docker**; đã đối chiếu: **không lỗi nào không phải Docker** |
| `cd client && npm run typecheck` | Đỏ sẵn từ trước với **193 lỗi** ở các feature không liên quan; **0 lỗi** ở file i18n vừa sửa |

### Lệch so với kế hoạch — và vì sao

1. **Thêm `ProxyTransportException`** (5 lớp lỗi thay vì 4). Kế hoạch gộp "không tới được đích" vào
   timeout, nhưng hai chuyện dẫn tới hai kết luận khác nhau khi thử lại: timeout nghĩa là đích CÓ
   THỂ đã xử lý xong request, còn connection refused thì gần như chắc chắn chưa.
2. **Chưa có `OAUTH2_CLIENT_CREDENTIALS`**, nên `ProxyTargetId.KEYCLOAK_ADMIN` cũng chưa khai. Nó cần
   lấy token rồi cache và làm mới — đúng phạm vi Phase 5 khi migrate `KeycloakUserSyncRest`. Khai
   sẵn một hằng trỏ tới đích chưa dùng được chỉ mời gọi người khác gọi vào rồi nhận 401 khó hiểu.
3. **Không dùng `Decorators` của resilience4j** — lớp đó nằm ở artifact `resilience4j-all`, không có
   trong `resilience4j-spring-boot3`. Ghép decorator thủ công, thứ tự còn đọc rõ hơn.
4. **Không có `TimeLimiter` ở đường async.** Timeout thật đã nằm ở read-timeout, chuỗi thử lại đã bị
   `total-budget` chặn; lớp thứ ba chỉ tạo thêm một con số phải giữ cho khớp, mà lại là lớp KHÔNG
   cắt được kết nối đang mở. Caller cần hạn chót riêng thì dùng `future.orTimeout(...)`.
5. **`ApplicationModules.verify()` không bật được toàn cục.** Xem [§2.2](#22-tình-trạng-ranh-giới-modulith-của-repo).



---

## 1. Mục tiêu & phạm vi

Xây một **cổng ra duy nhất** cho mọi lời gọi HTTP từ `cell-app` sang hệ thống khác (control plane,
Keycloak, Logs, Export, Notification…), với ba năng lực bắt buộc:

1. **Đồng bộ** — gọi và chờ kết quả, dùng trong luồng request của người dùng.
2. **Bất đồng bộ** — hai mức:
   - *Không bền* (`CompletableFuture`): gọi song song / giấu độ trễ, mất khi JVM chết.
   - *Bền* (store-and-forward qua bảng + worker): việc **phải xảy ra bằng được**, sống sót restart.
3. **Circuit breaker** — cùng timeout, bulkhead, rate limiter; một hệ thống đích chết **không được**
   kéo sập `cell-app`.
4. **Retry — tối đa 3 lần chạm đích cho một lời gọi** (1 lần gọi đầu + tối đa 2 lần thử lại), có
   backoff luỹ thừa, có ngân sách thời gian tổng, và chỉ thử lại khi an toàn. Trần 3 là **trần cứng
   trong code**, cấu hình vượt quá thì app không khởi động — xem [§9.6](#96-cơ-chế-retry--tối-đa-3-lần).

Kèm theo: **hướng dẫn sử dụng viết thẳng vào code** dưới dạng javadoc/comment ([§13](#13-hướng-dẫn-sử-dụng--viết-thẳng-vào-code)),
để người dùng package không phải mở tài liệu này ra mới biết cách gọi.

### Ngoài phạm vi

- Gọi ra ngoài bằng gRPC / SOAP / message queue — chỉ HTTP(S)/JSON.
- Nhận webhook **vào** — đã có `integration_ops.webhook_log` và `integration_ops.inbox`.
- Thay thế `integration_ops.outbox`. Xem ranh giới ở [§10.3](#103-ranh-giới-với-outbox-hàng-xóm-cùng-module).

---

## 2. Vì sao đặt trong `integration_ops` (không phải `common`)

Bản nháp đầu đặt ở `common.proxy`. Đưa sang `integration_ops.proxy` **tốt hơn ở bốn điểm cụ thể**,
không chỉ là đổi chỗ:

| | `common.proxy` (bản cũ) | `integration_ops.proxy` (bản này) |
|---|---|---|
| **Ranh giới `internal/`** | `common` khai `ApplicationModule.Type.OPEN` → Modulith **không** giấu được `internal`; ranh giới chỉ là *quy ước do review giữ* (đúng như javadoc `common/storage/package-info.java` tự thừa nhận) | `integration_ops` là module **CLOSED** (mặc định) → Modulith **thật sự chặn** import vào `internal`. Từ quy ước thành ràng buộc công cụ. |
| **Tiền tố bảng** | Bảng `ops_proxy_call` nằm trong module `common` — lệch, vì `80-ops.sql` định nghĩa `ops_` là *integration/ops* (outbox/inbox/webhook/job) | `ops_` khớp đúng module. Không cần ADR miễn trừ như `str_` đã phải làm (ADR-10). |
| **Ranh giới với outbox** | Phải lập luận vòng ("`common` không được phụ thuộc module nghiệp vụ nên hàng đợi bền phải ở lại `common`") | Hàng đợi bền nằm cạnh `outbox`/`inbox` — cùng một họ khái niệm, so sánh trực tiếp được. |
| **Ngữ nghĩa module** | `common` = tiện ích kỹ thuật dùng chung (storage, cấu hình, mẫu Excel) | `integration_ops` = *mọi thứ đi ra/đi vào hệ thống ngoài*. Proxy là định nghĩa của module này. |

### 2.1 Hệ quả phải xử lý — hai việc bắt buộc

Vì `integration_ops` là module CLOSED, **sub-package không tự động công khai**:

1. **`integration_ops/proxy/api/package-info.java` PHẢI khai `@NamedInterface`**, theo đúng tiền lệ
   `accounting_core/hach_toan/api/package-info.java` (`@NamedInterface("hach_toan_api")`).
   Không khai → module khác không import được `ProxyClient`, và lỗi chỉ lộ ra khi có test kiểm tra
   Modulith.

2. **`integration_ops/package-info.java` hiện đang RỖNG (0 byte)** — không có `@ApplicationModule`,
   không có javadoc, khác hẳn `platform_iam`, `accounting_core`, `chung_tu_ban_hang`. Thêm khai báo
   + javadoc mô tả module là dọn dẹp nhỏ, nằm đúng phạm vi đang sửa (§"Khi gặp code cũ" của CLAUDE.md).

### 2.2 Tình trạng ranh giới Modulith của repo

Chạy `ApplicationModules.of(PmktCellApplication.class).verify()` lần đầu cho ra **96 vi phạm có sẵn
từ trước**, không liên quan gì tới proxy:

| Vi phạm | Số lượng |
|---|---|
| `platform_iam → master_data.co_cau_to_chuc.dto` | 38 |
| `platform_iam → master_data.co_cau_to_chuc.service` | 30 |
| `core → platform_iam.quyen.api` | 10 |
| `chung_tu_* → accounting_core.hach_toan.api.dto` | 10 |
| `core → platform_iam.nguoi_dung.api` | 8 |

Vì vậy **không bật được `verify()` toàn cục** — dọn 96 vi phạm là một đợt refactor riêng, và biến
chúng thành một test đỏ thường trực thì chỉ dạy mọi người bỏ qua test. Thay vào đó `ProxyModularityTest`
chạy đúng bộ luật ấy nhưng chỉ soi vi phạm **có nhắc tới proxy** (và inbox), nên module mới bị giữ ở
chuẩn đầy đủ ngay từ đầu còn nợ cũ vẫn nhìn thấy được mà không chặn ai.

Hai thứ đã sửa trong đợt này nhờ phát hiện đó:

1. **`inbox/api` thiếu `@NamedInterface`** trong khi `platform_iam...InternalTenantController:15` đang
   import `InboxService` — một vi phạm tiềm ẩn chỉ chờ ai bật kiểm tra Modulith. Đã thêm
   `@NamedInterface("inbox_api")`.
2. **`proxy/api/error` cần `@NamedInterface` RIÊNG.** Modulith không suy ra tính công khai theo cây
   package: lộ `proxy.api` **không** tự động lộ `proxy.api.error`, nên `GlobalExceptionHandler` bắt
   `ProxyException` là vi phạm cho tới khi package con khai `@NamedInterface("proxy_api")` của chính
   nó. Cùng cách `accounting_core.chung_tu` làm với bốn package con.

---

## 3. Hiện trạng — vì sao cần package này

| File | Vấn đề |
|---|---|
| `platform_iam/to_chuc_nhom/internal/adapter/ControlPlaneToChucRest.java` | Tự dựng `RestClient` + `SimpleClientHttpRequestFactory`, tự viết hàm `goi()` dịch lỗi. **Không** circuit breaker, **không** retry. |
| `platform_iam/nguoi_dung/internal/adapter/KeycloakUserSyncRest.java` | Lặp lại đúng khuôn đó lần thứ hai. |
| `../../identity`, `../../front-door`, `../../integration-platform` (5 file khác) | Cùng bài toán, giải lại từ đầu ở từng service. |

Hệ quả cụ thể:

- **Không có bất kỳ circuit breaker nào trong toàn bộ `cell-app`** — `resilience4j` đã có trong
  `../../cell-app/gradle/libs.versions.toml` (2.2.0) nhưng **chưa được khai báo** trong
  `../../cell-app/build.gradle.kts`. Dependency nằm đó mà không ai dùng.
- **Không có bulkhead**: một control plane treo 10 giây × N request đồng thời sẽ giữ hết thread của
  Tomcat. Timeout đọc chỉ giới hạn *thời lượng* một lời gọi, không giới hạn *số* lời gọi.
- Không có metrics/log chuẩn cho lời gọi ra ngoài → khi đối tác chậm, không có số liệu để chứng minh.
- Không có cơ chế bất đồng bộ nào: `@Async`, `@EnableAsync`, `CompletableFuture`, `@Scheduled`
  **không xuất hiện lần nào** trong `../../cell-app/src/main/java` (ngoài vùng đóng băng).

---

## 4. Nguyên tắc thiết kế

Bám [CLAUDE.md](../../CLAUDE.md) và [docs/conventions.md](../conventions.md):

1. **Không hardcode** — base URL, timeout, ngưỡng circuit breaker, số lần retry đều ở
   `application.yml` dưới `pmkt.proxy.*`, đọc qua `@ConfigurationProperties`. Hằng kỹ thuật đặt
   `private static final` ngay trong lớp dùng (§1.2 conventions).
2. **Không commit secret** — API key / client secret chỉ qua placeholder env (`${...}`).
3. **Phân tầng** — `proxy` là tầng *adapter hạ tầng*, nằm **dưới** Service. Controller **không** được
   gọi thẳng `ProxyClient`.
4. **`proxy` không phụ thuộc module nghiệp vụ nào** — kể cả hai feature hàng xóm `outbox`/`inbox`.
   Hướng phụ thuộc luôn là `<module nghiệp vụ> → integration_ops.proxy.api`. `proxy` chỉ được dùng
   `core` (OPEN) và `common` (OPEN).
5. **`api/` vs `internal/`** — module khác **chỉ** được import `integration_ops.proxy.api`, và lần này
   Modulith giữ hộ (xem [§2](#2-vì-sao-đặt-trong-integration_ops-không-phải-common)).
6. **Không nuốt exception** — mọi nhánh lỗi đều ném tiếp hoặc trả trạng thái tường minh (§3.3 conventions).
7. **Không I/O trong transaction** — lời gọi mạng **không** được nằm trong `@Transactional`.
   Quy tắc đã ghi ở `V331__str_file.sql`; kế hoạch này tuân thủ bằng cách tách "ghi DB" và "gọi mạng"
   thành hai nhịp riêng (Phase 4).
8. **Không dùng Lombok** — `cell-app` **không** có Lombok trong classpath (dù conventions §3.5 nhắc
   tới `@RequiredArgsConstructor`). Dùng constructor tường minh + `private final`, giống toàn bộ code
   hiện có.

---

## 5. Cấu trúc package

Theo đúng khuôn *feature* của `integration_ops` (`outbox/`, `inbox/`, `webhook_log/` — mỗi cái
`api/` + `internal/`):

```text
cell-app/src/main/java/vn/dopai/pmkt/cell/integration_ops/
├── package-info.java                         # ⚠ đang RỖNG — bổ sung @ApplicationModule + javadoc
├── outbox/            (đã có)
├── inbox/             (đã có)
├── webhook_log/       (đã có)
└── proxy/                                    # ── MỚI ──
    ├── package-info.java                     # javadoc kiến trúc + bất biến + bảng "cấm"
    ├── api/                                  # ── BỀ MẶT DUY NHẤT cho module khác ──
    │   ├── package-info.java                 # @NamedInterface("proxy_api") + cookbook ngắn
    │   ├── ProxyClient.java                  # interface: exchange / call / exchangeAsync / enqueue
    │   ├── ProxyRequest.java                 # record + builder
    │   ├── ProxyResponse.java                # record (status, headers, body, durationMs, attempts)
    │   ├── ProxyTargetId.java                # hằng targetId đã đăng ký (tránh gõ chuỗi tự do)
    │   ├── ProxyCallHandle.java              # id + trạng thái của lời gọi bền (Phase 4)
    │   └── error/
    │       ├── ProxyException.java           # gốc, RuntimeException
    │       ├── ProxyRemoteException.java     # đích trả non-2xx (mang status + body)
    │       ├── ProxyTimeoutException.java    # connect/read/time-limiter timeout
    │       └── ProxyUnavailableException.java# circuit OPEN / bulkhead đầy / rate limit
    └── internal/                             # ── Modulith CHẶN import từ ngoài ──
        ├── config/
        │   ├── ProxyProperties.java          # @ConfigurationProperties("pmkt.proxy")
        │   ├── ProxyTargetProperties.java
        │   ├── ProxyResilienceProperties.java
        │   ├── ProxyRestClientFactory.java   # RestClient theo từng đích (timeout, no-redirect)
        │   ├── ProxyResilienceConfig.java    # các Registry của resilience4j
        │   └── ProxyAsyncConfig.java         # executor có chặn + truyền TenantContext
        ├── resilience/
        │   ├── ProxyResilienceGuard.java     # bọc supplier theo đúng thứ tự decorator
        │   └── CircuitBreakerScope.java      # enum GLOBAL | PER_TENANT
        ├── security/
        │   ├── ProxyUrlGuard.java            # chặn URL tuyệt đối, path traversal, IP nội bộ
        │   └── ProxyAuthApplier.java         # NONE | API_KEY | BEARER | OAUTH2_CC | INTERNAL_TOKEN
        ├── observability/
        │   ├── ProxyCallMetrics.java
        │   └── ProxyCallLogger.java          # log có che (mask) trường nhạy cảm
        ├── async/
        │   ├── ProxyAsyncExecutor.java       # CompletableFuture + TimeLimiter (Phase 3)
        │   ├── entity/ProxyCallTask.java     # hàng đợi bền (Phase 4)
        │   ├── repository/ProxyCallTaskRepository.java
        │   ├── service/ProxyCallEnqueuer.java
        │   └── service/ProxyCallWorker.java  # poller SKIP LOCKED + backoff + DLQ
        └── service/
            ├── ProxyClientImpl.java          # điều phối: guard → auth → gửi → map → log
            └── ProxyExchange.java            # một lượt gửi thật, không biết gì về resilience
```

**Ghi chú kiến trúc**: `ProxyExchange` (gửi thật) tách khỏi `ProxyResilienceGuard` (chính sách) là cố
ý — test circuit breaker không cần dựng HTTP, và test HTTP không cần chờ circuit breaker.

---

## 6. Public API

### 6.1 `ProxyClient`

```java
public interface ProxyClient {

    /** Gọi đồng bộ. KHÔNG ném khi đích trả non-2xx — caller tự quyết định 404/409 có ý nghĩa gì. */
    <T> ProxyResponse<T> exchange(ProxyRequest<T> request);

    /** Như trên nhưng ném {@link ProxyRemoteException} khi non-2xx. Dùng khi mọi lỗi đều là sự cố. */
    <T> T call(ProxyRequest<T> request);

    /** Bất đồng bộ KHÔNG BỀN. Mất khi JVM chết — chỉ dùng cho đọc / fan-out. */
    <T> CompletableFuture<ProxyResponse<T>> exchangeAsync(ProxyRequest<T> request);

    /** Bất đồng bộ BỀN (Phase 4): ghi hàng đợi trong transaction nghiệp vụ, worker gửi sau. */
    ProxyCallHandle enqueue(ProxyRequest<Void> request);
}
```

Vì sao tách `exchange` và `call`: `ControlPlaneToChucRest` hiện phải tự viết `goi()` để phân biệt
"409 = MST đã có chủ, là câu trả lời đúng cho người dùng" với "502 = control plane đang chết".
Sự phân biệt đó là **của module nghiệp vụ**, proxy không đoán thay được.

### 6.2 `ProxyRequest`

```java
public record ProxyRequest<T>(
        String targetId,                       // khoá trong pmkt.proxy.targets
        HttpMethod method,
        String path,                           // TƯƠNG ĐỐI, có thể chứa {ph} — cấm URL tuyệt đối
        List<Object> uriVariables,             // thay cho nối chuỗi (chặn injection)
        MultiValueMap<String, String> query,
        Map<String, String> headers,
        Object body,
        ParameterizedTypeReference<T> responseType,
        String idempotencyKey,                 // bắt buộc nếu muốn retry POST
        Duration timeoutOverride,              // null = theo cấu hình đích
        Supplier<T> fallback                   // null = ném exception
) { public static <T> Builder<T> builder(String targetId, HttpMethod method, String path) { ... } }
```

### 6.3 `ProxyResponse`

```java
public record ProxyResponse<T>(
        int status,
        HttpHeaders headers,
        T body,
        String rawBody,          // giữ nguyên để module nghiệp vụ tự parse lỗi của đối tác
        long durationMs,
        int attempts,
        boolean fromFallback
) {
    public boolean isSuccess()     { return status >= 200 && status < 300; }
    public boolean isClientError() { return status >= 400 && status < 500; }
    public boolean isServerError() { return status >= 500; }
}
```

---

## 7. Cấu hình

Thêm khối `pmkt.proxy` vào `../../cell-app/src/main/resources/application.yml`, cạnh `pmkt.storage`:

```yaml
pmkt:
  proxy:
    # Executor dùng chung cho exchangeAsync + JDK HttpClient. CÓ CHẶN (bounded) là cố ý:
    # hàng đợi vô hạn chỉ đổi "từ chối ngay" thành "hết RAM sau 10 phút".
    async:
      core-size: ${PROXY_ASYNC_CORE_SIZE:8}
      max-size: ${PROXY_ASYNC_MAX_SIZE:32}
      queue-capacity: ${PROXY_ASYNC_QUEUE_CAPACITY:200}
      thread-name-prefix: pmkt-proxy-
    # Giá trị mặc định, mỗi đích chỉ khai phần khác biệt.
    defaults:
      connect-timeout: 5s
      read-timeout: 10s
      log-body: false                 # bật = có nguy cơ ghi PII/secret vào log
      mask-headers: authorization,x-api-key,x-internal-token,cookie
      circuit-breaker:
        enabled: true
        scope: GLOBAL                 # GLOBAL | PER_TENANT
        sliding-window-type: TIME_BASED
        sliding-window-size: 60       # giây (TIME_BASED) hoặc số lời gọi (COUNT_BASED)
        minimum-number-of-calls: 10
        failure-rate-threshold: 50    # %
        slow-call-duration-threshold: 3s
        slow-call-rate-threshold: 100 # %
        wait-duration-in-open-state: 30s
        permitted-calls-in-half-open-state: 3
        max-instances: 1000           # trần registry khi scope = PER_TENANT
      retry:
        enabled: true
        # TRẦN CỨNG = 3. Đây là TỔNG số lần chạm đích (1 lần gọi đầu + tối đa 2 lần thử lại),
        # KHÔNG phải "3 lần thử lại". Khai > 3 → app KHÔNG khởi động (ProxyProperties validation):
        # retry khuếch đại tải lên đúng lúc đích đang hấp hối, 3 đã đủ cho lỗi chớp nhoáng.
        max-attempts: 3
        initial-interval: 200ms
        multiplier: 2.0
        randomization-factor: 0.5     # chống retry storm đồng pha
        # Trần thời gian cho CẢ chuỗi thử lại, tính từ lúc exchange() được gọi. Hết ngân sách là
        # dừng dù còn lượt — nếu không, 3 lượt × read-timeout 10s = 30s cho một request người dùng.
        total-budget: 15s
        retry-on-status: 502,503,504,429
        respect-retry-after: true     # 429/503 có Retry-After → nghe đối tác, không dùng backoff của ta
        idempotent-methods-only: true # POST/PATCH chỉ retry khi có Idempotency-Key
        # Retry của WORKER hàng đợi bền (Phase 4) — KHÁC với 3 lượt in-call ở trên và không nhân với
        # nó (worker chạy với in-call retry tắt). Xem §9.6.7.
        durable-max-attempts: 10
        durable-initial-interval: 1m
        durable-max-interval: 6h
      bulkhead:
        max-concurrent-calls: 16
        max-wait-duration: 0s         # 0 = từ chối ngay, không xếp hàng
      rate-limiter:
        enabled: false
    targets:
      control-plane:
        base-url: ${PMKT_CONTROL_PLANE_URL:http://front-door:8080}
        auth:
          type: INTERNAL_TOKEN
          token: ${PMKT_INTERNAL_TOKEN}
        read-timeout: 10s
      keycloak-admin:
        base-url: ${KEYCLOAK_URL:http://keycloak:8080}
        auth:
          type: OAUTH2_CLIENT_CREDENTIALS
          token-uri: ${KEYCLOAK_URL:http://keycloak:8080}/realms/master/protocol/openid-connect/token
          client-id: ${KEYCLOAK_ADMIN_CLIENT_ID:admin-cli}
          client-secret: ${KEYCLOAK_ADMIN_CLIENT_SECRET:}
        circuit-breaker:
          wait-duration-in-open-state: 60s
      hoa-don-dien-tu:
        base-url: ${HDDT_URL:}
        auth:
          type: API_KEY
          header-name: X-Api-Key
          value: ${HDDT_API_KEY:}
        # Nhà cung cấp HĐĐT cấp quota theo từng tenant → circuit breaker phải tách theo tenant,
        # nếu không một tenant bị khoá tài khoản sẽ ngắt luôn đường của mọi tenant khác.
        circuit-breaker:
          scope: PER_TENANT
        rate-limiter:
          enabled: true
          limit-for-period: 10
          limit-refresh-period: 1s
```

**Không đích nào được hardcode trong Java.** `ProxyTargetId` chỉ chứa hằng `String` là *khoá*
(`"control-plane"`), không chứa URL. Khởi động mà `targetId` không có trong `targets` → **fail fast**
ở `ProxyProperties` validation, không đợi tới lúc chạy.

---

## 8. Luồng xử lý một lời gọi đồng bộ

```text
Service nghiệp vụ
  └─ ProxyClient.exchange(request)
       ├─ 1. tra ProxyTargetProperties theo targetId          (không có → lỗi ngay lúc khởi động)
       ├─ 2. ProxyUrlGuard: path tương đối? có "../"? có scheme?   → từ chối trước khi mở socket
       ├─ 3. ProxyResilienceGuard.decorate(target, tenantId)
       │     Retry( CircuitBreaker( RateLimiter( Bulkhead( gửi ) ) ) )
       │     └─ 4. ProxyExchange.send()
       │           ├─ ProxyAuthApplier: gắn header xác thực
       │           ├─ gắn X-Correlation-Id (TenantContext.correlationId), traceparent
       │           ├─ gắn Idempotency-Key nếu có
       │           └─ RestClient gửi, đo thời gian
       ├─ 5. map sang ProxyResponse (không ném khi non-2xx)
       ├─ 6. ProxyCallMetrics.record(...) + ProxyCallLogger.log(...)
       └─ 7. trả về Service
```

Bước 2 và bước 6 nằm **ngoài** guard là cố ý: lỗi cấu hình của chính ta không được tính vào tỉ lệ
hỏng của đối tác, và metrics phải ghi được cả lời gọi bị circuit breaker chặn.

---

## 9. Resilience — chi tiết

### 9.1 Thứ tự bọc decorator

Dùng `io.github.resilience4j.decorators.Decorators`, gọi theo thứ tự **trong → ngoài**:

```java
Decorators.ofSupplier(send)
        .withBulkhead(bulkhead)          // trong cùng: chặn số lời gọi đồng thời
        .withRateLimiter(rateLimiter)    // giữ đúng QPS hợp đồng
        .withCircuitBreaker(circuitBreaker)
        .withRetry(retry)                // ngoài cùng
        .get();
```

Retry ở ngoài cùng nghĩa là **mỗi lần thử đều được circuit breaker ghi nhận** — đúng ý: 3 lần thử
đều hỏng là bằng chứng mạnh hơn 1 lần hỏng.

**Bẫy phải xử lý**: khi circuit OPEN, `CircuitBreaker` ném `CallNotPermittedException`; Retry ở ngoài
sẽ thử lại — vô nghĩa và làm nghẽn thread. Bắt buộc cấu hình:

```java
RetryConfig.custom()
        .ignoreExceptions(CallNotPermittedException.class,
                          BulkheadFullException.class,
                          RequestNotPermitted.class)
        ...
```

### 9.2 Cái gì được tính là "hỏng"

Đây là quyết định thiết kế quan trọng nhất của circuit breaker:

| Kết quả | Tính vào failure rate? | Lý do |
|---|---|---|
| 2xx | Không | — |
| **4xx** (trừ 429) | **Không** | 400/404/409 là *ta gửi sai* hoặc *câu trả lời nghiệp vụ*, không phải đối tác chết. Tính vào đây sẽ khiến một vòng lặp nhập liệu sai của người dùng ngắt luôn đường đi của cả hệ thống. |
| 429 | Có | Đối tác đang từ chối vì quá tải — lùi lại là đúng. Đọc `Retry-After` nếu có. |
| 5xx | Có | — |
| Timeout / IOException | Có | — |
| Lời gọi chậm > `slow-call-duration-threshold` | Có (qua `slowCallRateThreshold`) | Đối tác "còn sống nhưng bò" nguy hiểm hơn đối tác chết hẳn: nó ăn hết thread mà không bao giờ kích hoạt failure rate. |

Vì `ProxyExchange` **trả về** `ProxyResponse` thay vì ném với non-2xx, phân loại làm bằng
`recordResultPredicate`:

```java
CircuitBreakerConfig.custom()
        .recordResultPredicate(r -> {
            ProxyResponse<?> res = (ProxyResponse<?>) r;
            return res.isServerError() || res.status() == HttpStatus.TOO_MANY_REQUESTS.value();
        })
        .recordExceptions(IOException.class, ProxyTimeoutException.class)
        .ignoreExceptions(ProxyRemoteException.class)   // 4xx
        ...
```

### 9.3 Sliding window: chọn TIME_BASED

`COUNT_BASED` + `minimumNumberOfCalls: 10` trên một đích chỉ được gọi 3 lần/giờ nghĩa là circuit
breaker **không bao giờ mở**, và tệ hơn: nó đánh giá dựa trên các lời gọi từ hôm qua. Phần lớn đích
tích hợp của `cell-app` là loại lưu lượng thấp → mặc định `TIME_BASED`, cho phép override sang
`COUNT_BASED` cho đích lưu lượng cao.

### 9.4 Phạm vi circuit breaker: `GLOBAL` vs `PER_TENANT`

- `GLOBAL` (mặc định) — một breaker cho mỗi đích. Đúng khi đích là hạ tầng dùng chung (control plane,
  Keycloak): nó chết thì chết với mọi tenant.
- `PER_TENANT` — khoá breaker là `targetId + ":" + tenantId`. Đúng khi mỗi tenant có tài khoản /
  endpoint riêng ở đích (HĐĐT, ngân hàng): tenant A bị khoá tài khoản không được làm gián đoạn tenant B.

**Rủi ro của `PER_TENANT`**: `CircuitBreakerRegistry` giữ instance vĩnh viễn → với hàng nghìn tenant
là rò rỉ bộ nhớ chậm. Xử lý: `ProxyResilienceGuard` giữ registry riêng dạng LRU có trần
(`max-instances`, mặc định 1000) và log cảnh báo khi phải trục xuất. Bị trục xuất = breaker reset về
CLOSED, chấp nhận được với tenant đã lâu không gọi.

### 9.5 Bulkhead — lớp bảo vệ bị bỏ quên

`SemaphoreBulkhead` với `max-wait-duration: 0` là thứ ngăn "một đích treo 10 giây" biến thành "cạn
thread pool của Tomcat". Timeout đọc **không** làm được việc này. `max-concurrent-calls` nên đặt
≈ 10–20% số thread của Tomcat cho mỗi đích.

### 9.6 Cơ chế retry — tối đa 3 lần

#### 9.6.1 "3 lần" nghĩa là gì

**3 = tổng số lần chạm đích cho MỘT lời gọi**, không phải 3 lần thử lại (tức không phải 4 lượt):

| Lượt | Là gì | Thời điểm (backoff mặc định) |
|---|---|---|
| 1 | Lần gọi đầu | t = 0 |
| 2 | Thử lại #1 | sau `initial-interval` × jitter ≈ 100–300ms |
| 3 | Thử lại #2 | sau `initial-interval × multiplier` × jitter ≈ 200–600ms |
| — | Hết lượt → ném lỗi / trả `ProxyResponse` của lượt cuối | |

Đây đúng ngữ nghĩa `maxAttempts` của resilience4j, nên không cần chuyển đổi con số ở tầng cấu hình
— nhưng **phải ghi rõ trong javadoc và trong yaml**, vì "max attempts = 3" và "max retries = 3" lệch
nhau một lượt và đây là chỗ hiểu nhầm kinh điển.

Trần 3 là **trần cứng trong code**, không chỉ là giá trị mặc định:

```java
public final class ProxyRetryProperties {

    /** Trần cứng số lượt chạm đích. Retry khuếch đại tải lên đích đang hỏng — 3 lượt đã là 3× lưu
     *  lượng gửi tới một hệ thống vốn đang không chịu nổi lưu lượng bình thường. Muốn bền hơn thì
     *  dùng hàng đợi bền ({@code enqueue}) với backoff tính bằng phút, không phải nâng số này. */
    public static final int MAX_ATTEMPTS_CEILING = 3;

    @Min(1)
    @Max(MAX_ATTEMPTS_CEILING)
    private int maxAttempts = MAX_ATTEMPTS_CEILING;
    ...
}
```

`@ConfigurationProperties` + `@Validated` → khai `max-attempts: 5` trong yaml thì **app không khởi
động**, kèm thông báo chỉ đúng khoá sai. Fail fast, không phải phát hiện lúc sự cố production.

#### 9.6.2 Cái gì được thử lại, cái gì không

| Kết quả lượt trước | Thử lại? | Lý do |
|---|---|---|
| 5xx (502, 503, 504…) | **Có** | Lỗi phía đích, thường thoáng qua |
| 429 | **Có**, theo `Retry-After` nếu có | Đối tác bảo "chậm lại", nghe lời đối tác chứ đừng dùng backoff của ta |
| Timeout đọc / kết nối, `IOException` | **Có** | Sự cố mạng chớp nhoáng |
| **4xx** (trừ 429) | **Không** | Request của ta sai — gửi lại y hệt thì vẫn sai. Thử lại chỉ tốn thời gian của người dùng. |
| 2xx, 3xx | Không | — |
| `CallNotPermittedException` (circuit OPEN) | **Không** | Circuit vừa nói "đích đang chết"; thử lại là phủ định chính quyết định đó. **Đây là bẫy phải cấu hình tường minh**, xem [§9.1](#91-thứ-tự-bọc-decorator). |
| `BulkheadFullException`, `RequestNotPermitted` | **Không** | Ta đang tự bảo vệ mình; thử lại phá luôn cơ chế bảo vệ |
| `POST`/`PATCH` không có `Idempotency-Key` | **Không** | Xem §9.6.5 |

#### 9.6.3 Backoff

```java
IntervalFunction.ofExponentialRandomBackoff(
        props.getInitialInterval(),      // 200ms
        props.getMultiplier(),           // 2.0
        props.getRandomizationFactor());  // 0.5
```

Nhiễu ngẫu nhiên (`randomizationFactor`) là **bắt buộc, không phải tuỳ chọn**: không có nó thì 50
request cùng hỏng ở giây thứ 0 sẽ cùng thử lại ở giây thứ 0,2 — đúng một đợt sóng nữa giáng vào hệ
thống đang hỏng, rồi lại cùng nhau ở 0,6. Nhiễu ±50% trải chúng ra.

Độ trễ cộng thêm khi cả 3 lượt hỏng **nhanh** (connection refused): ~0,3–0,9 giây. Chấp nhận được
trong một request người dùng. Khi các lượt hỏng **chậm** thì khác hẳn — mục kế tiếp.

#### 9.6.4 Ngân sách tổng — cái bẫy nhân ba

Retry nhân độ trễ xấu nhất lên: `read-timeout: 10s` × 3 lượt + backoff ≈ **30,6 giây** cho một lời
gọi. Hai hệ quả:

- Vượt xa ngưỡng chịu đựng của người dùng, và vượt cả timeout của gateway phía trước → người dùng
  nhận lỗi gateway trong khi `cell-app` vẫn còn đang thử lại, giữ nguyên một thread và một suất
  bulkhead cho một kết quả không ai còn chờ.
- Đây là lỗi ta tự gây ra khi bật retry, không phải lỗi của đối tác.

Xử lý: **deadline cho cả chuỗi**, ghi ở `total-budget` (mặc định 15s). `ProxyResilienceGuard` chốt
mốc thời gian lúc vào và dừng thử lại khi hết ngân sách, dù còn lượt:

```java
long deadlineNanos = System.nanoTime() + props.getTotalBudget().toNanos();
RetryConfig.custom()
        .maxAttempts(props.getMaxAttempts())
        // resilience4j KHÔNG có sẵn "ngân sách tổng" cho lời gọi đồng bộ — chỉ có số lượt và
        // khoảng chờ. Chốt deadline ở predicate là cách rẻ nhất: hết giờ thì coi như không còn
        // đáng thử lại, trả nguyên kết quả lượt cuối cho caller.
        .retryOnResult(r -> System.nanoTime() < deadlineNanos && dangThuLaiDuoc(r))
        .retryOnException(e -> System.nanoTime() < deadlineNanos && dangThuLaiDuoc(e))
        .ignoreExceptions(CallNotPermittedException.class,
                          BulkheadFullException.class,
                          RequestNotPermitted.class)
        .intervalFunction(...)
        .build();
```

Quy tắc đặt số: `total-budget` nên **nhỏ hơn** timeout của tầng gọi vào (gateway / trình duyệt), và
`read-timeout × max-attempts` nên **xấp xỉ** `total-budget` — lệch quá thì một trong hai con số là
trang trí.

#### 9.6.5 Retry và tính bất biến (idempotency)

Retry một `POST` đã tới được server nhưng mất response trên đường về = **tạo trùng bản ghi ở đối tác**.
Với hoá đơn hay lệnh chuyển tiền thì đây không phải phiền toái, mà là sự cố dữ liệu.

- `GET`, `HEAD`, `PUT`, `DELETE`, `OPTIONS` → retry tự do (bản thân phương thức đã bất biến).
- `POST`, `PATCH` → **chỉ** retry khi `ProxyRequest.idempotencyKey != null`. Proxy gửi header
  `Idempotency-Key` **giữ nguyên qua cả 3 lượt** — đó là thứ cho phép đối tác nhận ra "lần 2 và lần 3
  là cùng một việc với lần 1".
- Khoá phải **ổn định theo nghiệp vụ** (`"hddt:" + chungTuId`), **không** phải `UUID.randomUUID()`:
  khoá ngẫu nhiên trông thì đúng cú pháp nhưng vô hiệu hoá đúng cái nó sinh ra để làm.
- `POST` + không khoá + retry đang bật → ném `IllegalArgumentException` **lúc build request**, không
  phải lúc chạy. Lỗi lập trình phải lộ ở lần chạy test đầu tiên, không phải ở production lúc 2 giờ sáng.

#### 9.6.6 Retry và circuit breaker ảnh hưởng lẫn nhau

Retry nằm **ngoài** circuit breaker ([§9.1](#91-thứ-tự-bọc-decorator)) → **mỗi lượt thử đều được
circuit breaker ghi nhận**. Hệ quả phải biết trước:

- Một lời gọi hỏng hoàn toàn đóng góp **3 mẫu hỏng**, không phải 1. Với
  `minimum-number-of-calls: 10`, cửa sổ đủ mẫu sau ~4 lời gọi hỏng chứ không phải 10.
- Đây là **ý muốn** (phát hiện sự cố nhanh hơn), nhưng phải là lựa chọn có ý thức khi chỉnh ngưỡng —
  không phải phát hiện ra sau khi circuit mở sớm hơn dự kiến. Ghi rõ ở comment của
  `ProxyResilienceConfig`.
- Khi circuit đã OPEN, retry **không** được thử lại (§9.6.2) → lời gọi bị chặn trả về ngay, không tốn
  thêm 0,6 giây backoff vô ích.

#### 9.6.7 Ba chế độ gọi — retry không được nhân lên

| Chế độ | Retry trong lời gọi | Retry bên ngoài | Tổng số lần chạm đích |
|---|---|---|---|
| `exchange()` / `call()` | tối đa **3** | không | **3** |
| `exchangeAsync()` | tối đa **3** (trong thread worker) | không | **3** |
| `enqueue()` (bền, Phase 4) | **TẮT** (`max-attempts = 1`) | worker: `so_lan_thu` + `next_attempt_at`, trần `durable-max-attempts: 10`, backoff 1 phút → 6 giờ | **10** |

Điều bắt buộc ở dòng cuối: **worker chạy với in-call retry tắt**. Nếu để cả hai, một việc sẽ chạm
đích 3 × 10 = **30 lần thật** — vừa spam đối tác, vừa khiến `so_lan_thu` trong DB không còn phản ánh
thực tế.

Hai loại retry giải hai bài toán khác nhau và không thay thế nhau:

- **In-call (≤ 3 lượt, backoff mili giây)** — cho lỗi *chớp nhoáng*: một gói tin rớt, một pod của
  đối tác vừa bị thay. Người dùng vẫn đang chờ, nên toàn bộ chuỗi phải xong trong `total-budget`.
- **Durable (≤ 10 lượt, backoff phút → giờ)** — cho *sự cố kéo dài*: đối tác bảo trì 2 tiếng. Không
  ai đang chờ, nên thử lại thưa và lâu mới đúng. Hết 10 lượt → `DEAD`, vào dead-letter cho người vận
  hành xử lý, **không** thử lại vô hạn trong im lặng.

#### 9.6.8 Quan sát được số lần thử

Retry mà không đo được thì không biết nó đang cứu mình hay đang che một sự cố kéo dài:

- `ProxyResponse.attempts` — số lượt đã dùng, trả về cho caller.
- Counter `pmkt.proxy.retry` tag `target`, `outcome` (`RECOVERED` = lượt sau thành công /
  `EXHAUSTED` = hết 3 lượt vẫn hỏng / `BUDGET_EXCEEDED` = dừng vì hết ngân sách).
- Log WARN **mỗi lần thử lại**, kèm lượt thứ mấy và lý do; log ERROR khi cạn lượt.
- `attempts > 1` mà thường xuyên `RECOVERED` = đích đang chập chờn — tín hiệu cần nói chuyện với đối
  tác, không phải cứ để retry giấu đi mãi.

### 9.7 Timeout

| Mức | Cơ chế | Ghi chú |
|---|---|---|
| Kết nối | `HttpClient.connectTimeout` | |
| Đọc | `JdkClientHttpRequestFactory.setReadTimeout` | Đây là timeout thật của chế độ **đồng bộ**. |
| Tổng thể | `TimeLimiter` của resilience4j | **Chỉ dùng được cho bất đồng bộ** — `TimeLimiter` cần một `Future` để huỷ. Ở chế độ đồng bộ nó không cắt được thread đang chờ socket, nên **không** dùng, tránh ảo giác an toàn. |

### 9.8 `RestClient` factory

Không dựa vào mặc định của Spring — khai báo tường minh:

```java
HttpClient jdk = HttpClient.newBuilder()
        .followRedirects(HttpClient.Redirect.NEVER)   // chặn SSRF qua 3xx (đích bị chiếm → 302 sang host khác)
        .connectTimeout(target.getConnectTimeout())
        .executor(proxyIoExecutor)                    // executor có tên + có chặn, không để JDK tự tạo
        .build();
JdkClientHttpRequestFactory factory = new JdkClientHttpRequestFactory(jdk);
factory.setReadTimeout(target.getReadTimeout());
```

Chọn `JdkClientHttpRequestFactory` thay vì `SimpleClientHttpRequestFactory` (mà `ControlPlaneToChucRest`
đang dùng) vì `Simple` mở **một `HttpURLConnection` mới cho mỗi lời gọi** — không có connection pool,
mỗi lời gọi tốn một lần bắt tay TLS. JDK `HttpClient` có pool sẵn và `Redirect.NEVER` là mặc định của nó.

*Nếu sau này cần metrics pool theo route hoặc tinh chỉnh keep-alive*: thêm
`org.apache.httpcomponents.client5:httpclient5` và đổi sang `HttpComponentsClientHttpRequestFactory`
— chỉ đổi trong `ProxyRestClientFactory`, không lan ra ngoài.

---

## 10. Bất đồng bộ

### 10.1 Mức 1 — không bền (`CompletableFuture`), Phase 3

Dùng cho: gọi song song nhiều đích để dựng một màn hình; làm giàu dữ liệu không bắt buộc; việc mất đi
thì chấp nhận được.

Ba điểm phải làm đúng:

1. **Executor có chặn** — `ThreadPoolTaskExecutor` với `queueCapacity` hữu hạn và `AbortPolicy`; đầy →
   ném `ProxyUnavailableException` ngay. Hàng đợi vô hạn chỉ dời thời điểm sập.
2. **Truyền `TenantContext`** — `TenantContext` là `ThreadLocal`; sang thread khác là **mất sạch**, và
   hệ quả không phải là exception mà là **RLS trả về 0 dòng trong im lặng** (xem javadoc
   `TenantContext.SYSTEM_PRINCIPAL`). Bắt buộc dùng `TaskDecorator`:

   ```java
   executor.setTaskDecorator(task -> {
       TenantContext.Snapshot snapshot = TenantContext.capture();
       Map<String, String> mdc = MDC.getCopyOfContextMap();
       return () -> {
           TenantContext.Snapshot previous = TenantContext.capture();
           TenantContext.restore(snapshot);
           if (mdc != null) { MDC.setContextMap(mdc); }
           try { task.run(); }
           finally { TenantContext.restore(previous); MDC.clear(); }
       };
   });
   ```

   `TenantContext` đã có sẵn `capture()`/`restore(Snapshot)` đúng cho việc này — dùng chúng, **không**
   dùng `set(tenantId, null, null)` (javadoc của lớp đã ghi rõ vì sao cách đó xoá mất principal).
3. **`TimeLimiter`** bọc future để có timeout tổng thể thật sự.

### 10.2 Mức 2 — bền (store-and-forward), Phase 4

Dùng cho: việc có tác dụng phụ **phải xảy ra bằng được** (đẩy hoá đơn sang cơ quan thuế, báo đối tác),
chấp nhận trễ nhưng không chấp nhận mất.

```text
Transaction nghiệp vụ                      Ngoài transaction
──────────────────────                     ─────────────────────────────────
ghi dữ liệu nghiệp vụ  ┐                   ProxyCallWorker (@Scheduled)
INSERT ops_proxy_call  ┘ cùng commit  ──▶   SELECT ... FOR UPDATE SKIP LOCKED
   (PENDING)                                gọi qua ProxyClient.exchange()  ← có đủ CB/retry
                                            cập nhật SUCCEEDED | PENDING(backoff) | DEAD
```

- `enqueue()` chạy `@Transactional(propagation = MANDATORY)` — **cùng khuôn** `OutboxPublisherImpl`
  (hàng xóm cùng module): không có transaction nghiệp vụ thì lỗi, không tự mở riêng. Đây là điều làm
  nó *bền*: hoặc cả nghiệp vụ và lời gọi cùng được ghi, hoặc không cái nào.
- Worker gọi lại chính `ProxyClient.exchange()` → thừa hưởng nguyên circuit breaker, không có đường
  code song song. **Nhưng in-call retry phải TẮT** ở đường này (`max-attempts = 1`), nếu không một
  việc sẽ chạm đích 3 × 10 = 30 lần — xem [§9.6.7](#967-ba-chế-độ-gọi--retry-không-được-nhân-lên).
- Retry của worker là loại *thưa và lâu*: `so_lan_thu` + `next_attempt_at`, backoff 1 phút → 6 giờ,
  trần `durable-max-attempts: 10`. Cạn lượt → `DEAD` (dead-letter), có API quản trị để xem và gửi lại
  thủ công — **không** thử lại vô hạn trong im lặng.
- Chống trùng bằng `UNIQUE (tenant_id, target_id, idempotency_key)`.

### 10.3 Ranh giới với `outbox` (hàng xóm cùng module)

| | `integration_ops.outbox` | `integration_ops.proxy` (async bền) |
|---|---|---|
| Ghi cái gì | **Sự kiện nghiệp vụ** đã xảy ra (`ChungTuBanHangDaGhiSo`) | **Lời gọi HTTP** cần thực hiện |
| Ai tiêu thụ | Nhiều consumer, chưa biết trước | Đúng một đích đã biết |
| Bảng | `ops_outbox_event` | `ops_proxy_call` |

Chúng **không** thay thế nhau. Cần "bắn sự kiện cho ai quan tâm" → `outbox`. Cần "gọi đúng endpoint
này của đối tác này cho bằng được" → `proxy.enqueue()`. Hai feature nằm cạnh nhau trong cùng module
nên khi ai đó phân vân, họ nhìn thấy cả hai lựa chọn ở cùng một chỗ — đây là lợi ích trực tiếp của
việc đặt `proxy` trong `integration_ops`.

---

## 11. Bảo mật

### 11.1 SSRF — `ProxyUrlGuard`

Đây là bề mặt tấn công chính của bất kỳ package tên "proxy" nào. Ba lớp chặn:

1. **Caller không bao giờ truyền URL** — chỉ truyền `targetId` + `path` tương đối. Base URL chỉ đến từ
   cấu hình. `path` bắt đầu bằng `http://`, `https://`, `//` → từ chối.
2. **Chuẩn hoá path** — chứa `..`, `%2e%2e`, ký tự điều khiển, hoặc thoát khỏi base path sau khi
   `URI.normalize()` → từ chối.
3. **Không đi theo redirect** — `Redirect.NEVER`. Đích bị chiếm quyền trả 302 sang `169.254.169.254`
   (metadata endpoint của cloud) là kịch bản thật.

Tuỳ chọn (`pmkt.proxy.defaults.block-private-networks: true`): phân giải host của base URL lúc khởi
động và từ chối nếu rơi vào dải riêng — chỉ hợp lý ở PROD, vì DEV gọi `http://minio:9000`.

### 11.2 Secret

Toàn bộ trường `auth.*` chỉ nhận placeholder env. Bổ sung `ProxyProperties` validation: giá trị secret
**không rỗng** ở profile `prod`, log **không bao giờ** in giá trị (chỉ in `type` và độ dài).

### 11.3 Che dữ liệu trong log

`ProxyCallLogger` mặc định: **không** log body. Khi `log-body: true`:
- che header trong `mask-headers`;
- che các khoá JSON trong `mask-json-fields` (mặc định `password,token,secret,soTaiKhoan,cccd`);
- cắt body ở `max-log-body-bytes` (mặc định 2048).

Ràng buộc pháp lý ở [audit-logs-service-plan.md §4](audit-logs-service-plan.md) ("không lưu password,
token, private key; CCCD/tài khoản ngân hàng phải mask") áp dụng nguyên vẹn cho log của proxy.

---

## 12. Quan sát & xử lý lỗi

| Hạng mục | Chi tiết |
|---|---|
| Metrics | Timer `pmkt.proxy.call` tag `target`, `method`, `outcome` (SUCCESS/CLIENT_ERROR/SERVER_ERROR/TIMEOUT/CIRCUIT_OPEN/BULKHEAD_FULL), `status`. `micrometer-registry-prometheus` đã có. |
| Metrics resilience4j | `resilience4j-spring-boot3` tự phát `resilience4j_circuitbreaker_state`, `..._calls`, `..._buffered_calls` khi có actuator. |
| Actuator | Thêm `circuitbreakers`, `circuitbreakerevents` vào `management.endpoints.web.exposure.include` (hiện là `health, info, prometheus, modulith`). |
| Log | Một dòng/lời gọi: INFO (thành công) / WARN (4xx) / ERROR (5xx, timeout, CB open) — `target`, `method`, `path`, `status`, `durationMs`, `attempts`, `correlation_id`. `correlation_id` đã có sẵn trong MDC nhờ `TenantFilter`. |
| Cảnh báo | Circuit chuyển OPEN → log ERROR + (tuỳ chọn) `Sentry.captureMessage`. `sentry-spring-boot` đã có. |

Bảng ánh xạ lỗi:

| Tình huống | Exception | HTTP trả client | `code` | `messageId` |
|---|---|---|---|---|
| Đích trả 4xx | `ProxyRemoteException` | *module nghiệp vụ tự quyết* | — | — |
| Đích trả 5xx | `ProxyRemoteException` | 502 | `PROXY_UPSTREAM_LOI` | `MSG_PROXY_UPSTREAM_LOI` |
| Timeout | `ProxyTimeoutException` | 504 | `PROXY_TIMEOUT` | `MSG_PROXY_TIMEOUT` |
| Circuit OPEN / bulkhead đầy | `ProxyUnavailableException` | 503 | `PROXY_TAM_NGUNG` | `MSG_PROXY_TAM_NGUNG` |

- Bổ sung `@ExceptionHandler` cho `ProxyException` vào `core/config/GlobalExceptionHandler.java` —
  **không** try/catch trong Controller (§3.3 conventions).
- Message trả client **không** được chứa base URL, tên host nội bộ hay body của đối tác.
- Thêm key i18n vào **cả** `../../client/src/app/i18n/vi.ts` và `../../client/src/app/i18n/en.ts` (luật 2 CLAUDE.md).

---

## 13. Hướng dẫn sử dụng — viết thẳng vào code

Đây là phần **bắt buộc của Phase 1**, không phải việc làm thêm nếu còn thời gian. Mục tiêu: một dev
gõ `ProxyClient` rồi bấm Ctrl+Q (Quick Doc) trong IDE là đủ biết phải làm gì, **không cần mở tài liệu
này**. Dưới đây là nội dung javadoc để chép vào từng file.

### 13.1 `integration_ops/package-info.java` (đang rỗng — bổ sung)

```java
/**
 * integration_ops ({@code ops_}) — <b>mọi thứ đi RA và đi VÀO hệ thống ngoài</b>.
 *
 * <p>Bốn feature, mỗi cái một hướng và một đảm bảo khác nhau — chọn nhầm là gánh sai độ bền:
 *
 * <table border="1">
 *   <caption>Chọn feature nào</caption>
 *   <tr><th>Việc cần làm</th><th>Feature</th><th>Đảm bảo</th></tr>
 *   <tr><td>Gọi API đối tác, cần kết quả ngay</td><td>{@code proxy} — {@code ProxyClient.exchange()}</td>
 *       <td>Đồng bộ, có circuit breaker</td></tr>
 *   <tr><td>Gọi API đối tác, PHẢI tới nơi bằng được</td><td>{@code proxy} — {@code ProxyClient.enqueue()}</td>
 *       <td>Bền, sống sót restart</td></tr>
 *   <tr><td>Bắn sự kiện nghiệp vụ cho ai quan tâm</td><td>{@code outbox}</td>
 *       <td>Bền, nhiều consumer</td></tr>
 *   <tr><td>Nhận lệnh/sự kiện từ ngoài vào</td><td>{@code inbox}</td><td>Chống xử lý trùng</td></tr>
 *   <tr><td>Ghi nhật ký webhook đã nhận</td><td>{@code webhook_log}</td><td>Truy vết</td></tr>
 * </table>
 *
 * <p><b>Module CLOSED</b>: package {@code *.internal} của mỗi feature bị Spring Modulith chặn từ
 * ngoài. Module khác chỉ import được package có {@code @NamedInterface} — hiện là
 * {@code proxy.api} ({@code "proxy_api"}).
 */
@org.springframework.modulith.ApplicationModule(displayName = "integration_ops")
package vn.dopai.pmkt.cell.integration_ops;
```

### 13.2 `integration_ops/proxy/package-info.java`

```java
/**
 * proxy — <b>cổng ra DUY NHẤT</b> cho mọi lời gọi HTTP từ {@code cell-app} sang hệ thống khác.
 *
 * <h2>Vì sao bắt buộc đi qua đây</h2>
 * Trước khi có package này, mỗi adapter tự dựng {@code RestClient}: tự đặt timeout, tự chặn redirect,
 * tự viết hàm dịch lỗi — và KHÔNG cái nào có circuit breaker. Hệ quả: một đích treo 10 giây × N
 * request đồng thời là cạn thread pool của Tomcat, cả hệ thống đứng vì một đối tác chậm. Timeout đọc
 * giới hạn THỜI LƯỢNG một lời gọi, không giới hạn SỐ lời gọi — chỉ bulkhead làm được việc đó, và
 * bulkhead nằm ở đây.
 *
 * <h2>Bất biến kiến trúc</h2>
 * <ul>
 *   <li>Package này KHÔNG được phụ thuộc module nghiệp vụ nào, kể cả hai feature hàng xóm
 *       {@code outbox} / {@code inbox}. Hướng phụ thuộc luôn là
 *       {@code <module nghiệp vụ> → integration_ops.proxy.api}.</li>
 *   <li>Caller KHÔNG bao giờ truyền URL tuyệt đối — chỉ {@code targetId} + path tương đối.
 *       Base URL chỉ đến từ {@code pmkt.proxy.targets.*} (chống SSRF, xem
 *       {@code internal.security.ProxyUrlGuard}).</li>
 *   <li>Lời gọi mạng KHÔNG được nằm trong {@code @Transactional} (quy tắc "không I/O trong
 *       transaction"). Cần gọi sau khi lưu → dùng {@code enqueue()}, đừng gọi thẳng trong service
 *       đang mở transaction.</li>
 * </ul>
 *
 * <h2>CẤM</h2>
 * <ul>
 *   <li>KHÔNG {@code new RestClient/RestTemplate/HttpClient} ở bất kỳ đâu ngoài package này —
 *       {@code ProxyArchTest} sẽ đánh trượt build.</li>
 *   <li>KHÔNG import {@code integration_ops.proxy.internal} từ ngoài — Modulith chặn.</li>
 *   <li>KHÔNG đặt base URL / API key vào hằng Java — chúng thuộc {@code application.yml} + env.</li>
 *   <li>KHÔNG bọc {@code try/catch} rồi nuốt {@code ProxyException} — để nó lên
 *       {@code GlobalExceptionHandler}.</li>
 * </ul>
 *
 * @see vn.dopai.pmkt.cell.integration_ops.proxy.api.ProxyClient hướng dẫn sử dụng kèm ví dụ
 */
package vn.dopai.pmkt.cell.integration_ops.proxy;
```

### 13.3 `integration_ops/proxy/api/package-info.java`

```java
/**
 * Public contract của cổng gọi API ngoài, cho các module khác dùng trong modulith.
 *
 * <p>Điểm vào duy nhất: {@link vn.dopai.pmkt.cell.integration_ops.proxy.api.ProxyClient} — javadoc của
 * nó có sẵn 5 công thức dùng thường gặp.
 */
@org.springframework.modulith.NamedInterface("proxy_api")
package vn.dopai.pmkt.cell.integration_ops.proxy.api;
```

### 13.4 `ProxyClient` — javadoc lớp (phần quan trọng nhất)

Đây là chỗ dev sẽ đọc. Viết theo khuôn `FileStorageApi` (prose + `<pre>{@code …}</pre>`):

```java
/**
 * Cổng gọi API sang hệ thống ngoài — mọi lời gọi HTTP ra khỏi {@code cell-app} phải đi qua đây.
 * KHÔNG tự dựng {@code RestClient}, KHÔNG chạm package {@code internal}.
 *
 * <p>Mỗi lời gọi tự động có: timeout, circuit breaker, retry (khi an toàn), bulkhead, log có che
 * secret, metrics, và header {@code X-Correlation-Id} lấy từ {@code TenantContext}. Bạn không phải
 * làm gì thêm cho những thứ đó.
 *
 * <h2>Retry: tự động, tối đa 3 lần — đừng tự viết vòng lặp</h2>
 * "3 lần" là TỔNG số lần chạm đích: 1 lần gọi đầu + tối đa 2 lần thử lại, cách nhau ~200ms rồi
 * ~400ms (có nhiễu ngẫu nhiên). Cả chuỗi bị chặn bởi một ngân sách thời gian
 * ({@code pmkt.proxy.defaults.retry.total-budget}, mặc định 15s) nên không bao giờ kéo dài
 * 3 × read-timeout.
 * <ul>
 *   <li>Thử lại khi: 5xx, 429, timeout, lỗi mạng.</li>
 *   <li>KHÔNG thử lại khi: 4xx (request của bạn sai — gửi lại vẫn sai), circuit đang OPEN,
 *       bulkhead đầy.</li>
 *   <li>{@code POST}/{@code PATCH} chỉ được thử lại khi có {@code idempotencyKey} — không có khoá
 *       mà lượt 1 đã tới nơi thì lượt 2 tạo bản ghi trùng ở đối tác. Thiếu khoá là lỗi ném NGAY lúc
 *       build request, không đợi tới production.</li>
 * </ul>
 * Cần bền hơn 3 lượt (đối tác bảo trì 2 tiếng) thì KHÔNG nâng số này — nâng cũng không được, 3 là
 * trần cứng và app sẽ không khởi động. Dùng {@link #enqueue} (công thức 5): worker thử lại tới 10
 * lượt với backoff tính bằng phút và giờ.
 *
 * <p>{@link ProxyResponse#attempts()} cho biết lời gọi vừa rồi đã dùng mấy lượt — {@code > 1} lặp
 * lại đều đặn nghĩa là đích đang chập chờn, đáng báo cho đối tác thay vì để retry che mãi.
 *
 * <h2>Bước 0 — đăng ký đích trước khi gọi</h2>
 * Thêm một mục vào {@code pmkt.proxy.targets} trong {@code application.yml}, và thêm hằng tương ứng
 * vào {@link ProxyTargetId}. Gọi tới {@code targetId} chưa đăng ký sẽ hỏng NGAY LÚC KHỞI ĐỘNG, không
 * phải lúc chạy production.
 *
 * <h2>Công thức 1 — GET đơn giản</h2>
 * <pre>{@code
 * ProxyResponse<NodeToChuc> res = proxy.exchange(
 *         ProxyRequest.builder(ProxyTargetId.CONTROL_PLANE, HttpMethod.GET, "/api/to-chuc/{id}")
 *                 .uriVariables(nodeId)              // KHÔNG nối chuỗi vào path
 *                 .responseType(NODE_TO_CHUC)        // ParameterizedTypeReference, hằng static final
 *                 .build());
 * if (res.isSuccess()) {
 *     return res.body();
 * }
 * }</pre>
 *
 * <h2>Công thức 2 — phân biệt "lỗi nghiệp vụ" với "đối tác chết"</h2>
 * Đây là lý do {@link #exchange} KHÔNG ném khi đích trả non-2xx: chỉ module nghiệp vụ mới biết một
 * 409 nghĩa là gì. Với sổ đăng ký tổ chức, 409 = "mã số thuế đã có chủ" — đó là CÂU TRẢ LỜI ĐÚNG cho
 * người dùng, phải ra 409 kèm thông điệp, chứ không phải sự cố hạ tầng:
 * <pre>{@code
 * ProxyResponse<NodeToChuc> res = proxy.exchange(request);
 * if (res.isSuccess()) {
 *     return res.body();
 * }
 * if (res.status() == HttpStatus.CONFLICT.value()) {
 *     throw ApiException.conflict("TO_CHUC_TU_CHOI", "MSG_TO_CHUC_TU_CHOI",
 *             "Mã số thuế này đã được đăng ký.");
 * }
 * throw new ApiException(HttpStatus.BAD_GATEWAY.value(), "CONTROL_PLANE_LOI",
 *         "MSG_CONTROL_PLANE_LOI", "Không kết nối được sổ đăng ký tổ chức. Vui lòng thử lại sau.");
 * }</pre>
 * Nếu MỌI mã lỗi đều là sự cố (không có mã nào mang nghĩa nghiệp vụ), dùng {@link #call} cho gọn —
 * nó tự ném {@link ProxyRemoteException}.
 *
 * <h2>Công thức 3 — POST có tác dụng phụ</h2>
 * Retry một POST đã tới nơi nhưng mất response trên đường về = TẠO TRÙNG bản ghi ở đối tác. Vì vậy
 * POST/PATCH chỉ được retry khi có khoá bất biến, và khoá phải ỔN ĐỊNH theo nghiệp vụ (đừng dùng
 * {@code UUID.randomUUID()} — mỗi lần người dùng bấm lại sẽ ra khoá mới, vô nghĩa):
 * <pre>{@code
 * proxy.call(ProxyRequest.builder(ProxyTargetId.HOA_DON_DIEN_TU, HttpMethod.POST, "/invoices")
 *         .body(payload)
 *         .idempotencyKey("hddt:" + chungTuId)      // ổn định theo chứng từ
 *         .responseType(KET_QUA_PHAT_HANH)
 *         .build());
 * }</pre>
 *
 * <h2>Công thức 4 — gọi song song nhiều đích (không bền)</h2>
 * Dùng khi dựng một màn hình cần dữ liệu từ 2–3 đích và việc mất đi thì chấp nhận được. Context
 * tenant/correlation được truyền sang thread worker tự động.
 * <pre>{@code
 * var f1 = proxy.exchangeAsync(requestA);
 * var f2 = proxy.exchangeAsync(requestB);
 * CompletableFuture.allOf(f1, f2).join();
 * }</pre>
 * <b>Không</b> dùng cách này cho việc có tác dụng phụ: JVM chết là mất, không ai biết.
 *
 * <h2>Công thức 5 — việc PHẢI xảy ra bằng được (bền)</h2>
 * Ghi lời gọi vào hàng đợi CÙNG transaction nghiệp vụ; worker gửi sau, tự retry, quá hạn thì vào
 * dead-letter. Đây là cách duy nhất đúng để "lưu chứng từ xong thì đẩy sang cơ quan thuế":
 * <pre>{@code
 * @Transactional
 * public void ghiSoVaPhatHanh(ChungTu ct) {
 *     repository.save(ct);
 *     proxy.enqueue(ProxyRequest.builder(ProxyTargetId.HOA_DON_DIEN_TU, HttpMethod.POST, "/invoices")
 *             .body(payloadTu(ct))
 *             .idempotencyKey("hddt:" + ct.getId())
 *             .build());                            // CHƯA gửi — chỉ ghi hàng đợi
 * }
 * }</pre>
 * {@code enqueue} là {@code @Transactional(propagation = MANDATORY)}: gọi ngoài transaction sẽ lỗi.
 * Cố ý — hoặc cả chứng từ và lời gọi cùng được ghi, hoặc không cái nào.
 *
 * <h2>Ba lỗi hay gặp</h2>
 * <ol>
 *   <li><b>Gọi HTTP bên trong {@code @Transactional}</b> — giữ connection của Hikari suốt thời gian
 *       chờ mạng, đủ nhiều là cạn pool. Cần gọi sau khi lưu → {@code enqueue()}.</li>
 *   <li><b>Bọc {@code try/catch (Exception e)} rồi trả {@code null}</b> — nuốt cả tín hiệu circuit
 *       breaker cần để biết đối tác đang chết. Để exception lên
 *       {@code GlobalExceptionHandler}.</li>
 *   <li><b>Nối tham số vào {@code path} bằng {@code +}</b> — dùng {@code {ph}} +
 *       {@code uriVariables(...)}, vừa được encode đúng vừa giữ tag metrics gộp được theo endpoint
 *       thay vì nổ thành hàng nghìn tag riêng lẻ.</li>
 * </ol>
 *
 * @see ProxyRequest cách dựng request
 * @see ProxyTargetId danh sách đích đã đăng ký
 */
public interface ProxyClient { ... }
```

### 13.5 Javadoc từng phương thức

```java
/**
 * Gọi ĐỒNG BỘ và trả về nguyên trạng thái, KHÔNG ném khi đích trả non-2xx.
 *
 * <p>Dùng khi một vài mã lỗi của đích mang nghĩa nghiệp vụ (409 = trùng, 404 = chưa có) và bạn cần
 * xử lý khác nhau — xem công thức 2 ở javadoc của lớp.
 *
 * @throws ProxyUnavailableException circuit đang OPEN, bulkhead đầy, hoặc vượt rate limit —
 *         request KHÔNG hề được gửi đi
 * @throws ProxyTimeoutException hết thời gian kết nối hoặc đọc
 * @throws IllegalArgumentException {@code targetId} chưa đăng ký, hoặc {@code path} không hợp lệ
 *         (URL tuyệt đối / có {@code ..}) — lỗi lập trình, không phải lỗi runtime của đối tác
 */
<T> ProxyResponse<T> exchange(ProxyRequest<T> request);

/**
 * Như {@link #exchange} nhưng NÉM {@link ProxyRemoteException} khi đích trả non-2xx, và trả thẳng
 * body khi thành công.
 *
 * <p>Dùng khi mọi mã lỗi đều là sự cố — không mã nào mang nghĩa nghiệp vụ. Ngắn hơn {@code exchange}
 * đúng một nhánh {@code if}; nếu bạn thấy mình đang {@code catch (ProxyRemoteException e)} rồi đọc
 * {@code e.status()}, nghĩa là bạn cần {@link #exchange}.
 */
<T> T call(ProxyRequest<T> request);

/**
 * Gọi BẤT ĐỒNG BỘ, KHÔNG BỀN — công việc nằm trong bộ nhớ, JVM chết là mất.
 *
 * <p>Chỉ dùng cho ĐỌC hoặc việc mất đi thì chấp nhận được (gọi song song để dựng màn hình, làm giàu
 * dữ liệu không bắt buộc). Việc có TÁC DỤNG PHỤ phải dùng {@link #enqueue}.
 *
 * <p>{@code TenantContext} và MDC được truyền sang thread worker tự động. Đây không phải chi tiết
 * trang trí: mất {@code TenantContext} thì RLS trả về 0 dòng TRONG IM LẶNG, không có exception nào
 * báo cho bạn biết.
 *
 * <p>Executor có hàng đợi HỮU HẠN. Đầy → future hoàn thành với {@link ProxyUnavailableException}
 * ngay lập tức, không xếp hàng vô hạn.
 */
<T> CompletableFuture<ProxyResponse<T>> exchangeAsync(ProxyRequest<T> request);

/**
 * Ghi lời gọi vào hàng đợi BỀN để worker gửi sau — dùng cho việc PHẢI xảy ra bằng được.
 *
 * <p>{@code @Transactional(propagation = MANDATORY)}: phải nằm trong transaction nghiệp vụ đang
 * chạy, không có thì LỖI (không tự mở transaction riêng). Đây chính là điều làm nó bền — hoặc cả
 * thay đổi nghiệp vụ và lời gọi cùng được ghi, hoặc không cái nào.
 *
 * <p>{@code idempotencyKey} là BẮT BUỘC và phải ổn định theo nghiệp vụ: nó vừa là khoá chống trùng
 * ở DB ({@code UNIQUE (tenant_id, target_id, idempotency_key)}), vừa là header gửi cho đối tác. Gọi
 * {@code enqueue} hai lần với cùng khoá = một lần gửi.
 *
 * @return handle để tra trạng thái sau; KHÔNG phải kết quả của lời gọi (lời gọi chưa xảy ra)
 */
ProxyCallHandle enqueue(ProxyRequest<Void> request);
```

### 13.6 `ProxyTargetId`

```java
/**
 * Khoá của các đích đã đăng ký trong {@code pmkt.proxy.targets}.
 *
 * <p>Chỉ chứa KHOÁ, không chứa URL — URL thuộc {@code application.yml} theo môi trường. Thêm đích
 * mới = thêm một hằng ở đây VÀ một mục trong yaml; thiếu một trong hai thì app không khởi động được
 * (fail fast, cố ý).
 */
public final class ProxyTargetId {
    public static final String CONTROL_PLANE = "control-plane";
    public static final String KEYCLOAK_ADMIN = "keycloak-admin";
    public static final String HOA_DON_DIEN_TU = "hoa-don-dien-tu";

    private ProxyTargetId() {}
}
```

### 13.7 Comment giữ tri thức tại chỗ trong `internal/`

Năm chỗ **bắt buộc** có comment giải thích *vì sao*, vì đây là những quyết định mà người sửa sau rất
dễ "dọn dẹp" nhầm:

- `ProxyResilienceGuard` — vì sao Retry ở NGOÀI CÙNG, và vì sao phải
  `ignoreExceptions(CallNotPermittedException.class)` (nếu không, circuit OPEN sẽ bị retry vô nghĩa).
- `ProxyResilienceGuard` (chỗ tính deadline) — vì sao phải tự cài `total-budget` bằng predicate:
  resilience4j **không có sẵn** ngân sách tổng cho lời gọi đồng bộ, chỉ có số lượt và khoảng chờ; bỏ
  đoạn này đi thì độ trễ xấu nhất nhảy lên `read-timeout × 3`.
- `ProxyRetryProperties.MAX_ATTEMPTS_CEILING` — vì sao trần là 3 và vì sao **không** nới: retry
  khuếch đại tải lên đúng lúc đích đang hỏng; cần bền hơn thì dùng `enqueue()`, không phải nâng số.
- `ProxyResilienceConfig` — vì sao **4xx không tính vào failure rate** (một vòng lặp nhập sai của
  người dùng không được ngắt đường của cả hệ thống); vì sao `slowCallRateThreshold` cần thiết (đối
  tác "còn sống nhưng bò" nguy hiểm hơn đối tác chết hẳn); và **mỗi lời gọi hỏng đóng góp 3 mẫu**
  cho circuit breaker vì retry nằm ngoài — đã tính đến khi đặt `minimum-number-of-calls`.
- `ProxyAsyncConfig` — vì sao `TaskDecorator` dùng `TenantContext.capture()/restore()` chứ không
  `set(tenantId, null, null)`, dẫn chiếu javadoc `TenantContext.SYSTEM_PRINCIPAL`.
- `ProxyCallWorker` — vì sao worker chạy với in-call retry **tắt** (3 × 10 = 30 lần chạm đích thật
  cho một việc, và `so_lan_thu` trong DB sẽ không còn khớp thực tế).

---

## 14. Schema DB (chỉ Phase 4)

Migration `V345__ops_proxy_call.sql` (số hiện tại lớn nhất là `V344`):

```sql
CREATE TABLE IF NOT EXISTS public.ops_proxy_call (
    id               uuid          PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id        uuid          NOT NULL,
    target_id        varchar(64)   NOT NULL,
    http_method      varchar(10)   NOT NULL,
    path             varchar(1024) NOT NULL,
    headers          jsonb,                                  -- ĐÃ che secret trước khi ghi
    body             text,
    idempotency_key  varchar(128)  NOT NULL,
    trang_thai       varchar(20)   NOT NULL DEFAULT 'PENDING',
    so_lan_thu       integer       NOT NULL DEFAULT 0,
    next_attempt_at  timestamptz   NOT NULL DEFAULT now(),
    response_status  integer,
    last_error       text,
    correlation_id   varchar(64),
    phien_ban        integer       NOT NULL DEFAULT 1,       -- BR12
    ngay_tao         timestamptz   NOT NULL DEFAULT now(),   -- BR30
    nguoi_tao        uuid,
    ngay_cap_nhat    timestamptz,
    nguoi_cap_nhat   uuid,
    CONSTRAINT ck_ops_proxy_call_trang_thai
        CHECK (trang_thai IN ('PENDING','IN_PROGRESS','SUCCEEDED','FAILED','DEAD'))
);

CREATE UNIQUE INDEX ux_ops_proxy_call_idem
    ON public.ops_proxy_call (tenant_id, target_id, idempotency_key);
CREATE INDEX idx_ops_proxy_call_claim
    ON public.ops_proxy_call (next_attempt_at)
    WHERE trang_thai = 'PENDING';

ALTER TABLE public.ops_proxy_call ENABLE ROW LEVEL SECURITY;
ALTER TABLE ONLY public.ops_proxy_call FORCE ROW LEVEL SECURITY;
-- policy tenant_isolation: theo đúng khuôn V331__str_file.sql
```

Tiền tố `ops_` khớp đúng module (`80-ops.sql` định nghĩa `ops_` = integration/ops) — không cần ADR
miễn trừ như `str_` đã phải làm ở ADR-10.

**Vấn đề đã biết cần chốt**: worker quét **xuyên tenant**, nhưng RLS lọc theo `app.tenant_id` → worker
sẽ thấy 0 dòng. `ops_outbox_event` hiện cũng vướng đúng chuyện này (chưa có relay nên chưa lộ). Ba
hướng, xem [§18](#18-quyết-định-cần-chốt-trước-khi-code).

---

## 15. Kiểm thử

Tất cả test đơn vị gắn `@Tag("unit")` để chạy được ở làn `./gradlew unitTest` (không cần Docker).

| Lớp test | Kiểm cái gì | Cách |
|---|---|---|
| `ProxyUrlGuardTest` | URL tuyệt đối, `..`, `%2e%2e`, scheme lạ đều bị từ chối | thuần JVM |
| `ProxyClientSyncTest` | map status/body/header, gắn auth, gắn `X-Correlation-Id` | `MockRestServiceServer.bindTo(RestClient.builder())` — có sẵn từ Spring 6.1, **không cần thêm dependency** |
| `ProxyCircuitBreakerTest` | N lần 5xx → OPEN; lời gọi kế tiếp **không** chạm socket; sau `wait-duration` → HALF_OPEN → CLOSED | `waitDurationInOpenState` rút còn ms |
| `ProxyCircuitBreakerIgnoresClientErrorTest` | 100 lần 400 → circuit **vẫn CLOSED** | chống hồi quy cho quyết định §9.2 |
| `ProxyRetryTest` | 503 → chạm đích **đúng 3 lần** rồi dừng (không phải 4); 400 → **1 lần**; `CallNotPermittedException` / `BulkheadFullException` → **1 lần**; POST không `idempotencyKey` → **1 lần**; POST có khoá → 3 lần và **cùng một giá trị** `Idempotency-Key` ở cả 3 | đếm số request tới `MockRestServiceServer` |
| `ProxyRetryCeilingTest` | `max-attempts: 5` trong yaml → context **không khởi động được** | `ApplicationContextRunner` + assert `failure()` |
| `ProxyRetryBudgetTest` | `total-budget` ngắn hơn `read-timeout × 3` → dừng khi hết ngân sách dù còn lượt; `outcome = BUDGET_EXCEEDED` | |
| `ProxyRetryAfterTest` | 429 kèm `Retry-After: 2` → chờ theo header thay vì backoff mặc định | |
| `ProxyRetryMetricsTest` | `ProxyResponse.attempts` đúng số lượt; counter `pmkt.proxy.retry` lên đúng nhãn `RECOVERED` / `EXHAUSTED` | |
| `ProxyBulkheadTest` | vượt `max-concurrent-calls` → `ProxyUnavailableException` ngay, không xếp hàng | |
| `ProxyAsyncTenantPropagationTest` | `TenantContext` + MDC còn nguyên trong thread worker; thread gọi **không** bị đổi context sau khi xong | quan trọng nhất nhóm async |
| `ProxyAsyncRejectionTest` | hàng đợi đầy → từ chối ngay, không phình RAM | |
| `ProxyCallLoggerMaskingTest` | `Authorization`, `password`, `cccd` không xuất hiện trong log | |
| `ProxyCallWorkerTest` (Phase 4) | `SKIP LOCKED` không xử lý trùng; backoff tăng; quá `durable-max-attempts` → `DEAD`; **worker chạm đích đúng 1 lần mỗi lượt** (in-call retry đã tắt, không nhân 3×10) | Testcontainers → làn `build` |
| `ProxyArchTest` | không nơi nào ngoài `integration_ops.proxy` `new` `RestClient`/`RestTemplate`/`HttpClient` | ArchUnit (`archunit-junit5` đã có) |
| `CellModularityTest` | `ApplicationModules.of(PmktCellApplication.class).verify()` | **sẽ đỏ vì `inbox` thiếu `@NamedInterface`** — xem [§2.2](#22-một-vi-phạm-ranh-giới-đã-có-sẵn--chỉ-báo-không-sửa-ở-đây) |

---

## 16. Chống trôi (anti-drift)

1. **`CellModularityTest`** — `ApplicationModules.verify()`. Đây là thứ `common.proxy` **không thể**
   có (module OPEN không giấu được `internal`), và là lợi ích lớn nhất của việc chuyển sang
   `integration_ops`. Ràng buộc `api/` – `internal/` từ "quy ước do review giữ" thành "build đỏ".
2. **ArchUnit `ProxyArchTest`** — cấm `new RestClient/RestTemplate/HttpClient` ngoài package proxy.
   Đây là thứ ngăn package bị bỏ quên: người tiếp theo cần gọi API ngoài sẽ bị build chặn nếu tự dựng
   client. Cho phép ngoại lệ tường minh (danh sách lớp) với adapter chưa kịp migrate.
3. **Javadoc `package-info.java`** — nội dung ở [§13](#13-hướng-dẫn-sử-dụng--viết-thẳng-vào-code),
   độ chi tiết ngang `common/storage/package-info.java`.
4. **Checkstyle** đang ở chế độ báo cáo (`isIgnoreFailures = true`) — không thêm rule mới ở đây.

---

## 17. Lộ trình

| Phase | Nội dung | Kết quả kiểm chứng được | Ước lượng |
|---|---|---|---|
| **0** | `libs.resilience4j.spring.boot3` vào `build.gradle.kts`; `ProxyProperties` + khối yaml; `integration_ops/package-info.java` (đang rỗng) + `proxy/package-info.java` + `api/package-info.java` có `@NamedInterface`; skeleton `api/` | `cd cell-app && ./gradlew compileJava` xanh; app khởi động, `/actuator/health` OK | 0,5 ngày |
| **1** | `ProxyUrlGuard`, `ProxyAuthApplier`, `ProxyRestClientFactory`, `ProxyExchange`, `ProxyClientImpl.exchange/call`, error → `GlobalExceptionHandler`, log + metrics, **toàn bộ javadoc §13** | 4 lớp test đầu §15 xanh; Ctrl+Q trên `ProxyClient` ra đủ 5 công thức | 2,5 ngày |
| **2** | Circuit breaker + **retry (trần cứng 3 lượt + `total-budget` + `Retry-After` + luật idempotency)** + bulkhead + rate limiter, `CircuitBreakerScope`, registry LRU, actuator endpoints; `CellModularityTest` + `ProxyArchTest` (kèm 1 dòng `@NamedInterface` cho `inbox`) | 8 lớp test resilience/retry xanh; `/actuator/circuitbreakers` thấy đủ đích | 2,5 ngày |
| **3** | `exchangeAsync` + executor có chặn + `TaskDecorator` truyền `TenantContext`/MDC + `TimeLimiter` | 2 lớp test async xanh | 1 ngày |
| **4** | Async **bền**: migration `V345`, entity/repository, `ProxyCallEnqueuer`, `ProxyCallWorker`, DLQ + API quản trị | test worker xanh (cần Docker) | 3 ngày |
| **5** *(tuỳ chọn, tách ticket riêng)* | Migrate `ControlPlaneToChucRest` + `KeycloakUserSyncRest` sang `ProxyClient`; siết `ProxyArchTest` (bỏ danh sách ngoại lệ) | test hiện có của `platform_iam` vẫn xanh | 1,5 ngày |

Phase 0–3 là một lô giao được (proxy đồng bộ + circuit breaker + async không bền). Phase 4 chỉ nên làm
khi đã có nghiệp vụ thật cần "gửi cho bằng được".

Phase 5 **đổi hành vi code đang chạy** (`ControlPlaneToChucRest` hiện *không* có retry; sau khi migrate
sẽ có) → tách ticket, review riêng, không gộp vào diff Phase 1–4.

---

## 18. Quyết định cần chốt trước khi code

| # | Câu hỏi | Các lựa chọn | Đề xuất |
|---|---|---|---|
| 1 | Có làm Phase 4 (async **bền**) ngay không? | (a) làm luôn · (b) hoãn tới khi có nghiệp vụ thật | **(b)** — Phase 0–3 đã giải quyết trọn "đồng bộ + bất đồng bộ + circuit breaker" như yêu cầu. |
| 2 | Xử lý `inbox` thiếu `@NamedInterface` thế nào? | (a) thêm 1 dòng trong cùng PR Phase 2 · (b) ticket riêng, tạm chưa bật `CellModularityTest` | **(a)** — sửa 1 dòng, cùng loại việc; nếu không thì lợi ích lớn nhất của lần chuyển này chưa dùng được. |
| 3 | Worker Phase 4 vượt RLS thế nào? | (a) role DB riêng có `BYPASSRLS` · (b) policy phụ đọc `current_setting('app.worker')` · (c) worker lặp theo từng `tenant_id` | **(b)** — hiển thị được trong `pg_policies`, không cấp quyền rộng như `BYPASSRLS`. |
| 4 | Có migrate 2 adapter hiện có sang proxy không? | (a) có, Phase 5 · (b) để nguyên, chỉ code mới dùng proxy | **(a) nhưng tách ticket** — nếu để nguyên thì `ProxyArchTest` phải giữ danh sách ngoại lệ vĩnh viễn và package sẽ trôi. |
| 5 | Chỉ `cell-app` hay đưa lên `shared-kernel` cho `identity`/`front-door` dùng chung? | (a) `cell-app` trước · (b) `shared-kernel` ngay | **(a)** — 5 file client ở service khác dùng stack khác nhau; đưa lên `shared-kernel` sau khi ổn định qua một release. |
| 6 | Bật `block-private-networks` ở PROD? | có/không | **Có ở `prod`, tắt ở `local`/`dev`** (DEV gọi `http://minio:9000`, `http://keycloak:8080`). |

---

## 19. Definition of Done

Trước khi báo hoàn thành từng phase — chạy và **báo trung thực** kết quả:

```bash
cd cell-app && ./gradlew unitTest
```

```bash
cd cell-app && ./gradlew build
```

> Lưu ý môi trường: máy dev hiện **chưa có Docker**, nên `build` sẽ đỏ ở ~25 test Testcontainers
> (`RedisCache*`, `FileStorage*`, `ToChucNhomCellMigrationTest`) — đó là giới hạn môi trường, không
> phải hồi quy. `unitTest` là cổng xanh thực tế; đối chiếu danh sách lớp lỗi trước khi kết luận.

Nếu có chạm `../../client` (thêm key i18n ở §12):

```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test
```

Checklist bổ sung:

- [ ] Không còn magic value: mọi timeout/ngưỡng ở `pmkt.proxy.*` hoặc `private static final` có tên.
- [ ] Không có secret trong code, test, comment, dữ liệu mẫu.
- [ ] Ba `messageId` mới có key ở **cả** `vi.ts` và `en.ts`.
- [ ] `MAX_ATTEMPTS_CEILING = 3` là trần **cứng**: khai `max-attempts: 4` trong yaml thì app không
      khởi động (có test chứng minh), không chỉ là giá trị mặc định.
- [ ] `total-budget` có hiệu lực thật: có test cho trường hợp dừng vì hết ngân sách khi vẫn còn lượt.
- [ ] Worker hàng đợi bền chạy với in-call retry **tắt** — có test đếm số lần chạm đích.
- [ ] `POST`/`PATCH` thiếu `idempotencyKey` mà bật retry → ném lúc **build request**, không phải lúc gửi.
- [ ] `integration_ops/package-info.java` không còn rỗng — có `@ApplicationModule` + javadoc bảng chọn feature.
- [ ] `proxy/api/package-info.java` có `@NamedInterface("proxy_api")`.
- [ ] Javadoc `ProxyClient` đủ 5 công thức + mục "ba lỗi hay gặp"; javadoc từng phương thức ghi rõ exception nào ném khi nào.
- [ ] Ba chỗ trong `internal/` ở §13.7 có comment giải thích *vì sao*.
- [ ] `ProxyArchTest` xanh; `CellModularityTest` xanh (sau khi xử lý `inbox`).
- [ ] Không có `catch (Exception ignored)`; không có `System.out.println`.
- [ ] Commit chuẩn `feat(cell-app): …`, nhánh `tinh-nang/proxy-goi-api-ngoai`, không commit thẳng `master`/`develop`.
- [ ] Soát [Checklist §5 của conventions](../conventions.md#5-checklist-trước-khi-commit).

---

## Phụ lục A — Thay đổi build

`../../cell-app/build.gradle.kts`, khối `dependencies`:

```kotlin
// Resilience: circuit breaker / retry / bulkhead / rate limiter cho integration_ops.proxy.
// Alias đã có sẵn trong gradle/libs.versions.toml (resilience4j 2.2.0) nhưng chưa từng được khai báo.
// resilience4j-spring-boot3 cần spring-boot-starter-aop — đã có ở dòng trên.
implementation(libs.resilience4j.spring.boot3)
```

Nếu bật `CellModularityTest` (Phase 2), thêm:

```kotlin
testImplementation(libs.spring.modulith.test)
```

Không cần dependency nào khác: `MockRestServiceServer` cho `RestClient.Builder` nằm trong
`spring-boot-starter-test` (Spring 6.1+), `archunit-junit5` và `micrometer-registry-prometheus` đã có.

## Phụ lục B — Tài liệu liên quan

- [docs/conventions.md](../conventions.md) — §1 (không hardcode/secret), §3 (Java).
- [docs/request-flow.md](../request-flow.md) — luồng request vào `cell-app`.
- [docs/audit-logs-service-plan.md](audit-logs-service-plan.md) — §4 quy định che dữ liệu nhạy cảm.
- `cell-app/.../accounting_core/hach_toan/api/package-info.java` — tiền lệ `@NamedInterface` trong module CLOSED.
- `cell-app/.../common/storage/api/FileStorageApi.java` — khuôn javadoc "hướng dẫn dùng" (prose + `<pre>{@code …}</pre>`).
- `cell-app/.../integration_ops/outbox/internal/service/OutboxPublisherImpl.java` — khuôn
  `@Transactional(propagation = MANDATORY)` cho ghi hàng đợi cùng transaction nghiệp vụ.
