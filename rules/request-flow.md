# Luồng frontend gọi đến cell-app được xử lý như nào

Tài liệu này mô tả luồng request từ frontend đến `cell-app`, dùng ví dụ cụ thể là màn **Chức danh** với endpoint:

- `GET /api/master-data/chuc-danh`
- `GET /api/master-data/chuc-danh/{id}`
- `POST /api/master-data/chuc-danh`
- `PUT /api/master-data/chuc-danh/{id}`
- `DELETE /api/master-data/chuc-danh/{id}`

---

## 1. Tóm tắt ngắn

Luồng tổng thể:

```text
client-v2
  -> front-door
  -> cell-gateway
  -> cell-app / ChucDanhController
  -> ChucDanhServiceImpl
  -> Repository / DB
```

Frontend **không gọi trực tiếp** hostname của `cell-app`, mà chỉ gọi path `/api/**`. Sau đó hệ thống gateway sẽ:

1. Xác thực JWT
2. Xác định tenant/công ty đang active
3. Route request đến đúng cell
4. Kiểm tra tenant consistency
5. Forward vào `cell-app`
6. `cell-app` kiểm quyền nghiệp vụ và bind tenant vào DB session để RLS cô lập dữ liệu

---

## 2. Frontend gọi API như nào

File tham chiếu:

- `client-v2/src/features/danhMuc/doiTuong/chucDanh/api.ts`
- `client-v2/src/platform/http/httpClient.ts`

Trong `api.ts`, frontend định nghĩa:

```ts
export const CHUC_DANH_BASE = '/api/master-data/chuc-danh'
```

Và dùng axios client chung `http` để gọi:

- `list()` -> `http.get(CHUC_DANH_BASE, { params })`
- `detail(id)` -> `http.get(`${CHUC_DANH_BASE}/${id}`)`
- `create(body)` -> `http.post(CHUC_DANH_BASE, ...)`
- `update(id, body)` -> `http.put(`${CHUC_DANH_BASE}/${id}`, ...)`
- `remove(id)` -> `http.delete(`${CHUC_DANH_BASE}/${id}`, ...)`

=> FE chỉ làm việc với endpoint dạng `/api/...`.

---

## 3. Axios client gắn gì vào request

File: `client-v2/src/platform/http/httpClient.ts`

Axios interceptor tự gắn các header quan trọng:

- `Authorization: Bearer <accessToken>`
- `X-Tenant-Id: <congTyId đang active>`
- `Accept-Language: <locale hiện tại>`

Ý nghĩa:

- `Authorization` dùng để backend biết người gọi là ai
- `X-Tenant-Id` biểu diễn tenant/công ty hiện đang chọn trên UI
- `Accept-Language` để backend trả message theo ngôn ngữ phù hợp

---

## 4. Front Door nhận toàn bộ `/api/**`

File: `../../front-door/src/main/resources/application.yml`

Route chính:

```yml
- id: cell-api
  uri: ${DEFAULT_CELL_URI:http://cell-gateway:8090}
  predicates:
    - Path=/api/**
```

=> Mọi request business từ FE như `/api/master-data/chuc-danh` đều đi vào `front-door` trước.

---

## 5. Front Door resolve tenant và chọn cell

File: `../front-door/src/main/java/vn/vtt/pmkt/frontdoor/TenantRoutingFilter.java`

`TenantRoutingFilter` là nơi xử lý routing multi-tenant.

### 5.1. Gắn correlation id

Nếu request chưa có `X-Correlation-Id`, filter tự sinh ra một id mới.

### 5.2. Resolve tenant active

Ưu tiên resolve tenant theo thứ tự:

1. JWT claim `tenant_id`
2. Subdomain
3. Header `X-Tenant-Id` nếu request đi từ trusted proxy

Trong luồng FE bình thường:

- JWT chứa allowlist `tenant_id`
- FE gửi `X-Tenant-Id` là công ty đang active
- front-door chọn tenant active hợp lệ từ allowlist đó

### 5.3. Chọn đúng cell

Sau khi có tenant, front-door gọi:

- `TenantDirectoryClient.resolveCellUri(tenant)`

để tra tenant này đang nằm ở cell nào, rồi retarget request sang đúng `cell-gateway` của cell đó.

=> **Front-door là lớp quyết định request của tenant nào sẽ đi vào cell nào.**

---

## 6. Cell Gateway forward tiếp vào cell-app

File: `../../cell-gateway/src/main/resources/application.yml`

Route bên trong cell:

```yml
- id: cell-modules
  uri: ${CELL_APP_URI:http://cell-app:8081}
  predicates:
    - Path=/api/**
```

=> Sau khi `front-door` chọn đúng cell, `cell-gateway` sẽ forward tiếp toàn bộ `/api/**` sang `cell-app`.

---

## 7. Cell Gateway kiểm tra tenant một lần nữa

Các file chính:

- `../cell-gateway/src/main/java/vn/vtt/pmkt/cellgw/TenantClaimAuthorizationManager.java`
- `../cell-gateway/src/main/java/vn/vtt/pmkt/cellgw/TenantConsistencyFilter.java`

### 7.1. `TenantClaimAuthorizationManager`

Manager này áp vào `/api/**` để đảm bảo:

- JWT phải hợp lệ
- JWT phải có claim `tenant_id` hợp lệ

Nếu không có tenant hợp lệ trong JWT thì deny ngay từ gateway.

### 7.2. `TenantConsistencyFilter`

Filter này chống spoof `X-Tenant-Id`.

Nó làm các việc sau:

1. Đọc allowlist tenant từ JWT claim `tenant_id`
2. Đọc `X-Tenant-Id` từ request
3. Nếu header có mặt nhưng **không nằm trong allowlist** -> trả `403`
4. Nếu header hợp lệ hoặc vắng mặt -> stamp lại `X-Tenant-Id` đúng theo tenant active

=> `cell-gateway` không tin mù quáng header từ client, mà luôn đối chiếu với JWT.

---

## 8. Cell-app nhận request ở controller nào

File: `cell-app/src/main/java/vn/vtt/pmkt/cell/master_data/internal/ChucDanhController.java`

Controller map trực tiếp endpoint:

```java
@RequestMapping("/api/master-data/chuc-danh")
```

Các API tương ứng:

- `@GetMapping` -> list
- `@GetMapping("/{id}")` -> detail
- `@PostMapping` -> create
- `@PutMapping("/{id}")` -> update
- `@DeleteMapping("/{id}")` -> delete

Mỗi API đều có `@PreAuthorize(...)` để chặn theo quyền nghiệp vụ:

- `DMChucDanh.View`
- `DMChucDanh.View.Detail`
- `DMChucDanh.Create`
- `DMChucDanh.Edit`
- `DMChucDanh.Delete`

=> Request đến `cell-app` không chỉ vào đúng controller mà còn bị chặn bởi quyền business-level.

---

## 9. Cell-app nạp quyền nghiệp vụ như nào

File: `cell-app/src/main/java/vn/vtt/pmkt/cell/platform_iam/internal/PermissionAuthoritiesFilter.java`

Filter này chạy sau khi JWT đã được xác thực và làm các việc:

1. Lấy `userId` từ `sub`
2. Lấy `tenantId` active từ JWT + `X-Tenant-Id`
3. Set `TenantContext`
4. Load permission thực tế từ `PermissionQueryService`
5. Gắn các authority đó vào `SecurityContext`

=> Nhờ vậy `@PreAuthorize("hasAuthority('DMChucDanh.View')")` ở controller mới hoạt động đúng.

---

## 10. Từ controller xuống service xử lý nghiệp vụ

File: `cell-app/src/main/java/vn/vtt/pmkt/cell/master_data/internal/ChucDanhServiceImpl.java`

Controller gọi `ChucDanhService`, implementation là `ChucDanhServiceImpl`.

Ví dụ với `list()`:

1. `tenantRls.bind()`
2. Chuẩn hóa filter/search
3. Gọi `repository.search(...)`
4. Map entity sang DTO

Với `create/update/delete`, service còn xử lý thêm:

- validate dữ liệu
- duplicate check
- optimistic locking
- soft delete

=> Business logic thực sự nằm ở service layer.

---

## 11. Tenant isolation được áp ở DB bằng RLS

File: `cell-app/src/main/java/vn/vtt/pmkt/cell/config/TenantRls.java`

`tenantRls.bind()` set các session variable vào PostgreSQL:

- `app.tenant_id`
- `app.user_id`
- `app.is_owner`

Các giá trị này lấy từ `TenantContext`.

Sau đó các query/repository phía dưới sẽ bị Row-Level Security giới hạn theo tenant hiện tại.

=> Đây là tầng cô lập dữ liệu ở mức DB.

---

## 12. End-to-end flow đầy đủ

Với request ví dụ:

```text
GET /api/master-data/chuc-danh
```

Luồng xử lý là:

1. **Frontend** gọi `http.get('/api/master-data/chuc-danh')`
2. Axios gắn:
   - `Authorization`
   - `X-Tenant-Id`
3. **Front-door** nhận request `/api/**`
4. `TenantRoutingFilter`:
   - tạo/gắn correlation id
   - resolve tenant active
   - tra cell của tenant
   - route sang đúng `cell-gateway`
5. **Cell-gateway**:
   - verify JWT lại
   - kiểm tra claim `tenant_id`
   - kiểm tra `X-Tenant-Id` có hợp lệ với JWT không
   - stamp lại tenant header chuẩn
   - forward sang `cell-app`
6. **Cell-app**:
   - `PermissionAuthoritiesFilter` nạp quyền nghiệp vụ
   - request vào `ChucDanhController`
   - `@PreAuthorize` kiểm tra quyền `DMChucDanh.*`
7. **Service layer** (`ChucDanhServiceImpl`):
   - gọi `tenantRls.bind()`
   - bind tenant vào DB session
   - thao tác với repository
8. **DB/RLS**:
   - chỉ cho truy cập dữ liệu của tenant active
9. Response quay ngược lại:
   - `cell-app` -> `cell-gateway` -> `front-door` -> `frontend`

---

## 13. Sơ đồ ngắn dễ nhớ

```text
FE
 -> Axios httpClient
    -> Authorization + X-Tenant-Id
 -> Front Door
    -> resolve tenant
    -> chọn đúng cell
 -> Cell Gateway
    -> verify JWT
    -> check tenant consistency
 -> Cell App
    -> PermissionAuthoritiesFilter
    -> ChucDanhController
    -> ChucDanhServiceImpl
    -> TenantRls.bind()
    -> Repository / PostgreSQL RLS
```

---

## 14. Kết luận một câu

**Frontend gọi `/api/**` qua gateway, front-door chọn đúng cell theo tenant, cell-gateway kiểm tra lại tenant/JWT rồi mới forward vào cell-app; tại cell-app request tiếp tục bị kiểm quyền bằng `@PreAuthorize` và bị cô lập dữ liệu bằng `TenantRls.bind()` + PostgreSQL RLS.**
