# Hướng dẫn tạo công ty (tenant) · tài khoản owner · nhân viên · phân quyền

Dùng cho môi trường **DEV local** (các service chạy bằng IntelliJ, không Docker). Mục tiêu: có ngay
một bộ dữ liệu đăng nhập được để test — 1 công ty, 1 chủ sở hữu, N nhân viên với các mức quyền khác nhau.

- Script tái sử dụng: [`../../deploy/seed-tenant.py`](../../deploy/seed-tenant.py)
- Profile mẫu: [`../../deploy/seed-profiles/mau-co-ban.json`](../../deploy/seed-profiles/mau-co-ban.json)
- Lần seed cũ (2 tenant OSP-DEMO, hardcode, chỉ để tham khảo): [`../../deploy/seed-osp-demo.README.md`](../../deploy/seed-osp-demo.README.md)

> ⚠ File này chứa mật khẩu tài khoản DEV. Không dùng lại mật khẩu đó ở staging/production.

---

## 1. Bức tranh: ai tạo cái gì

Không service nào tự làm hết. Bốn chặng, mỗi chặng một chủ sở hữu dữ liệu:

| # | Chặng | Service | Sinh ra cái gì |
|---|---|---|---|
| 1 | Tạo tenant + định danh chủ sở hữu | `tenant-provisioning` :8082 → `identity` :8084 → Keycloak | dòng `cp_tenant_directory`, user Keycloak của owner |
| 2 | Dựng tenant phía cell | `cell-app` :8081 `/internal/tenants/{id}/init` | `iam_tenant` + master-data mặc định + catalog `iam_quyen` |
| 3 | Dựng bản ghi owner phía cell | `cell-app` `/internal/tenants/{id}/owner` | `iam_tai_khoan` + `iam_tai_khoan_tenant.la_chu_so_huu=true` |
| 4 | Vai trò + nhân viên | `cell-app` `/api/iam/vai-tro`, `/api/iam/nguoi-dung` (token của owner) | `iam_vai_tro`, `iam_tai_khoan(+quyền)` — cell-app tự gọi ngược control-plane → identity để tạo user Keycloak |

**Luật sống còn**: `iam_tai_khoan.id` của một người dùng **phải bằng** `sub` (subject) của họ trong
Keycloak — `PermissionAuthoritiesFilter` map quyền theo `jwt.getSubject()`. Vì thế không bao giờ được
`INSERT` thẳng người dùng vào DB: luôn đi qua API để id được lấy từ Keycloak.

Owner **bypass RBAC** (claim `is_owner=true`); nhân viên phải có vai trò mới làm được gì.

---

## 2. Chuẩn bị

Phải chạy đủ 5 service trong IntelliJ (kiểm bằng `lsof -nP -iTCP:<port> -sTCP:LISTEN`):

| Service | Port | Vai trò trong luồng này |
|---|---|---|
| `front-door` | 8080 | đường thật của client — dùng để ĐỌC/verify |
| `cell-app` | 8081 | IAM + dữ liệu nghiệp vụ — dùng để GHI |
| `tenant-provisioning` | 8082 | tạo tenant |
| `identity` | 8084 | Keycloak + email |
| `cell-gateway` | 8090 | front-door → cell |

Hạ tầng dùng chung (không cần Docker trên máy này): Keycloak `http://192.168.1.76:8088` realm `pmkt`,
Postgres cell `192.168.1.76:15433`. Secret lấy tự động từ `deploy/env/osp-*.env`
(`PMKT_INTERNAL_TOKEN`, `KC_ADMIN_PASSWORD`).

Kiểm nhanh cell-app đang đọc DB nào:

```bash
grep "FlywayExecutor - Database" logs/cell-app.log | tail -1
```

---

## 3. Cách nhanh — chạy script với một profile

### 3.1 Xem trước, không ghi gì

```bash
python3 deploy/seed-tenant.py deploy/seed-profiles/mau-co-ban.json --report
```

### 3.2 Seed thật (idempotent — chạy lại bao nhiêu lần cũng được)

```bash
python3 deploy/seed-tenant.py deploy/seed-profiles/mau-co-ban.json
```

Script chạy đúng 7 bước B1…B7 và in kết quả từng bước; cuối cùng ghi ra
`<profile>.result.json` (máy đọc) + `<profile>.commands.txt` (toàn bộ curl tương đương, secret đã che).

### 3.3 Chỉ kiểm tra lại đăng nhập của bộ đã seed

```bash
python3 deploy/seed-tenant.py deploy/seed-profiles/mau-co-ban.json --verify
```

### 3.4 Tạo bộ dữ liệu MỚI

Copy profile, đổi `mst` + toàn bộ email + mã vai trò rồi chạy lại:

```bash
cp deploy/seed-profiles/mau-co-ban.json deploy/seed-profiles/mau-kho-hang.json
```

Cấu trúc profile:

```jsonc
{
  "password": "OspDemo@2026",          // mật khẩu chung cho MỌI tài khoản trong profile
  "tenants": [{
    "mst": "0100008801",               // = mã tenant, PHẢI duy nhất
    "ten": "Cong ty Mau Test 01",
    "hubContractId": "SEED-MAU-01",    // khoá idempotency của onboarding
    "owner": { "email": "...", "hoTen": "...", "soDienThoai": "..." },
    "vaiTro": [
      { "ma": "MAU_KT_TRUONG", "ten": "...", "moTa": "...", "quyen": "FULL" }
      // "quyen": "FULL" | "EDITOR" | "VIEWER"  (preset tính từ catalog quyền THẬT của tenant)
      //        | ["HTNguoiDung.View", "SalChungTuBanHang.Create", ...]  (liệt kê tường minh)
    ],
    "nhanVien": [
      { "email": "...", "hoTen": "...", "soDienThoai": "...", "vaiTro": ["MAU_KT_TRUONG"] }
    ]
  }]
}
```

Ba preset quyền suy từ đuôi mã quyền trong catalog của chính tenant đó:

| Preset | Gồm | Số quyền (tenant mẫu) |
|---|---|---|
| `FULL` | tất cả | 721 |
| `EDITOR` | `.View*` + `.Create/.Add/.Edit/.Clone/.Copy/.NhanBan/.Import` | 424 |
| `VIEWER` | chỉ `.View`, `.View.Detail`, `.ViewList`, `.Search`, `.ViewPII` | 233 |

---

## 4. Bộ dữ liệu mẫu đã tạo sẵn (chạy ngày 2026-08-18, DB `pmkt_cell`)

Công ty **Cong ty Mau Test 01** — MST `0100008801`,
tenantId `a92bc78e-c680-41db-a53d-001254d6f650`. **Mật khẩu chung: `OspDemo@2026`**

| Email | Loại | Vai trò | Kiểm chứng |
|---|---|---|---|
| `mau01.owner@pmkt.vn` | chủ sở hữu | *(bypass RBAC, `is_owner=true`)* | login OK |
| `mau01.kttruong@pmkt.vn` | nhân viên | `MAU_KT_TRUONG` (FULL, 721 quyền) | login OK · `GET /api/iam/nguoi-dung` 200 · `POST /api/iam/vai-tro` không bị 403 |
| `mau01.ktvien@pmkt.vn` | nhân viên | `MAU_KT_VIEN` (EDITOR, 424 quyền) | login OK · 200 · không bị 403 |
| `mau01.xem@pmkt.vn` | nhân viên | `MAU_XEM` (VIEWER, 233 quyền) | login OK · 200 · **403 khi POST** — đúng như mong đợi |

Đăng nhập web client: <http://localhost:5173>.

Lấy token bằng CLI:

```bash
curl -s -X POST http://192.168.1.76:8088/realms/pmkt/protocol/openid-connect/token -d grant_type=password -d client_id=pmkt-web -d username=mau01.owner@pmkt.vn --data-urlencode 'password=OspDemo@2026' | jq -r .access_token
```

---

## 5. Cách thủ công — từng lệnh curl

Biến dùng chung:

```bash
cd /Users/macbook/Documents/VTT/Code/osp/vtt-osp
TOK=$(grep '^PMKT_INTERNAL_TOKEN=' deploy/env/osp-tenant-provisioning.env | cut -d= -f2-)
KCPW=$(grep '^KC_ADMIN_PASSWORD=' deploy/env/osp-tenant-provisioning.env | cut -d= -f2-)
KC=http://192.168.1.76:8088
ADM=$(curl -s -X POST $KC/realms/master/protocol/openid-connect/token -d grant_type=password -d client_id=admin-cli -d username=admin --data-urlencode "password=$KCPW" | jq -r .access_token)
```

**B1 — tạo tenant + owner** (trả 422 trên máy local: xem §6.1, tenant vẫn được tạo)

```bash
curl -s -X POST http://localhost:8082/api/control-plane/onboarding/owner -H "X-Internal-Token: $TOK" -H 'Content-Type: application/json' -d '{"mst":"0100008801","tenDoanhNghiep":"Cong ty Mau Test 01","ownerEmail":"mau01.owner@pmkt.vn","ownerName":"Chu So Huu Mau 01","ownerPhone":"0910008801","hubContractId":"SEED-MAU-01"}'
```

Lấy `tenantId` (kể cả khi B1 lỗi):

```bash
curl -s http://localhost:8082/api/control-plane/directory/by-ma/0100008801 -H "X-Internal-Token: $TOK" | jq -r .tenantId
```

**B2 — dựng định danh owner trên Keycloak** (bù cho B1 dừng sớm)

```bash
curl -s -X POST http://localhost:8084/internal/identity/owners -H "X-Internal-Token: $TOK" -H 'Content-Type: application/json' -d '{"email":"mau01.owner@pmkt.vn","name":"Chu So Huu Mau 01","phone":"0910008801","tenantId":"<TENANT_ID>"}'
```

**B3 — đặt mật khẩu + bỏ bước xác thực email**

```bash
SUB=$(curl -s "$KC/admin/realms/pmkt/users?email=mau01.owner@pmkt.vn&exact=true" -H "Authorization: Bearer $ADM" | jq -r '.[0].id')
curl -s -X PUT "$KC/admin/realms/pmkt/users/$SUB" -H "Authorization: Bearer $ADM" -H 'Content-Type: application/json' -d '{"enabled":true,"emailVerified":true,"requiredActions":[]}'
curl -s -X PUT "$KC/admin/realms/pmkt/users/$SUB/reset-password" -H "Authorization: Bearer $ADM" -H 'Content-Type: application/json' -d '{"type":"password","value":"OspDemo@2026","temporary":false}'
```

**B4 — dựng tenant + owner phía cell** (idempotent, tự lành tenant dở dang)

```bash
curl -s -X POST http://localhost:8081/internal/tenants/<TENANT_ID>/init  -H "X-Internal-Token: $TOK" -H 'Content-Type: application/json' -d '{"ma":"0100008801","ten":"Cong ty Mau Test 01"}'
curl -s -X POST http://localhost:8081/internal/tenants/<TENANT_ID>/owner -H "X-Internal-Token: $TOK" -H 'Content-Type: application/json' -d "{\"userId\":\"$SUB\",\"email\":\"mau01.owner@pmkt.vn\",\"hoTen\":\"Chu So Huu Mau 01\",\"soDienThoai\":\"0910008801\"}"
```

**B5 — token owner + catalog quyền**

```bash
OT=$(curl -s -X POST $KC/realms/pmkt/protocol/openid-connect/token -d grant_type=password -d client_id=pmkt-web -d username=mau01.owner@pmkt.vn --data-urlencode 'password=OspDemo@2026' | jq -r .access_token)
curl -s http://localhost:8080/api/iam/quyen -H "Authorization: Bearer $OT" | jq -r '[.[].ma]' > /tmp/quyen.json
```

**B6 — tạo vai trò** (POST **thẳng** :8081, xem §6.3)

```bash
curl -s -X POST http://localhost:8081/api/iam/vai-tro -H "Authorization: Bearer $OT" -H 'Content-Type: application/json' -d "{\"ma\":\"MAU_KT_TRUONG\",\"ten\":\"Ke toan truong (mau)\",\"moTa\":\"\",\"quyen\":$(cat /tmp/quyen.json),\"nguoiDungIds\":[]}"
```

**B7 — tạo nhân viên** (`vaiTroIds` **bắt buộc có ít nhất 1**, xem §6.4)

```bash
curl -s -X POST http://localhost:8081/api/iam/nguoi-dung -H "Authorization: Bearer $OT" -H 'Content-Type: application/json' -d '{"hoTen":"Nhan Vien Ke Toan Truong","email":"mau01.kttruong@pmkt.vn","soDienThoai":"0910008811","vaiTroIds":["<ROLE_ID>"],"guiKichHoat":false}'
```

Rồi lặp lại **B3** cho email nhân viên để đặt mật khẩu (thay vì chờ email kích hoạt).

**Xoá một người dùng** — cần `updatedAt`, thiếu sẽ 409 `STALE_DATA`:

```bash
curl -s -X DELETE http://localhost:8081/api/iam/nguoi-dung/<ID> -H "Authorization: Bearer $OT" -H 'Content-Type: application/json' -d '{"updatedAt":"<updatedAt lấy từ GET>"}'
```

---

## 6. Bẫy đã gặp — đọc trước khi debug

### 6.1 `POST /onboarding/owner` trả 422 `PROVISIONING_FAILED` trên máy local

`TenantProvisioningService.cellBaseUri()` suy URI cell theo convention Docker
`http://{cellId}-cell-app:8081`. Hostname đó **không phân giải được** khi stack chạy bằng IntelliJ, nên
`ensureProvisioned()` ném lỗi **trước** khi kịp gọi `identity.provisionOwner()`:

- dòng `cp_tenant_directory` **đã** được tạo (lấy `tenantId` qua `/directory/by-ma/{mst}`),
- Keycloak **chưa** có owner nào ⇒ phải tự gọi `identity /internal/identity/owners` (B2),
- phía cell chưa có gì ⇒ phải tự gọi `/internal/tenants/{id}/init` + `/owner` (B4).

Script đã làm sẵn cả ba việc bù này. Muốn chữa tận gốc thì map `cell-1-cell-app` → `127.0.0.1` trong
`/etc/hosts` (cần quyền sudo) hoặc chạy tất cả bằng Docker (đã bị cấm trong repo này).

### 6.2 User tạo ra nhưng không đăng nhập được

`KeycloakUserSyncRest` có `@ConditionalOnProperty("pmkt.control-plane.url")`. Thiếu
`PMKT_CONTROL_PLANE_URL` trong `../../deploy/env/osp-cell-app.env` → rơi về bean **no-op**:
`POST /api/iam/nguoi-dung` vẫn trả **201**, nhưng id là UUID ngẫu nhiên và Keycloak không có user nào
⇒ tài khoản chết, **không vá tay được** (Keycloak Admin API bỏ qua trường `id` khi tạo user).

Script có guard: tạo 1 user thăm dò `seed.probe@pmkt.vn`, đối chiếu Keycloak, rollback rồi **dừng hẳn**
nếu phát hiện no-op. Cách chữa: thêm `PMKT_CONTROL_PLANE_URL=http://localhost:8082` vào env rồi
**restart cell-app** (đã có sẵn trong repo, chỉ cần restart nếu env vừa đổi).

### 6.3 Tạo vai trò qua front-door bị 405

`CELL_CB_TIMEOUT=8s` (`../../deploy/env/osp-cell-gateway.env`). `POST /api/iam/vai-tro` với ~700 mã quyền
chạy quá 8s ⇒ circuit-breaker cắt và fallback trả **405 Method Not Allowed**, trong khi cell-app **vẫn
commit** vai trò. Vì thế: **GHI IAM đi thẳng :8081**, ĐỌC/verify đi qua front-door :8080.

### 6.4 `400 VAITRO_REQUIRED` khi tạo người dùng

Mỗi người dùng phải có **ít nhất một vai trò** (`MSG_PMKT-E-14552_211`). Không còn tạo được user
"noaccess" trắng quyền như đợt seed cũ; muốn user gần như không có quyền thì tạo một vai trò rỗng/tối
thiểu rồi gán.

### 6.5 `403 FORBIDDEN_GRANT` (`ITKQ_001/002/003`) khi gán vai trò

Trigger `fn_itkq_kiem_soat_nguoi_cap` — "không cấp được thứ mình không có". Nguyên nhân thường gặp:
**gán vai trò `ADMIN` có sẵn của hệ thống** cho user mới. Hãy tạo vai trò riêng (`MAU_*`) và gán vai trò
đó, đừng đụng `ADMIN`.

### 6.6 Kiểm tra thẳng dưới DB

```bash
export PATH=/usr/local/opt/libpq/bin:$PATH
export PGPASSWORD=$(grep -o 'password=[^&"]*' .idea/dataSources.xml | head -1 | cut -d= -f2)
psql -h 192.168.1.76 -p 15433 -U pmkt -d pmkt_cell -Atc \
  "select tk.email, t.la_chu_so_huu, t.trang_thai from iam_tai_khoan tk join iam_tai_khoan_tenant t on t.tai_khoan_id=tk.id where tk.email like 'mau01%';"
```

`psql` nằm ở `/usr/local/opt/libpq/bin` (keg-only, không có trong PATH). Mọi lệnh phải chạy ngoài
sandbox mạng.

---

## 7. Checklist nghiệm thu một bộ dữ liệu mới

1. `--report` khớp ý định.
2. Chạy seed: mọi dòng B6 báo `tạo mới`/`đã có`, không có `LỖI`.
3. B7: owner `is_owner=[True]`, mọi nhân viên `login=OK` và `GET /api/iam/nguoi-dung=200`.
4. Phân quyền có khác nhau thật: user VIEWER phải bị **403** khi `POST /api/iam/vai-tro`, user
   EDITOR/FULL thì không.
5. Đăng nhập thử trên <http://localhost:5173> bằng ít nhất owner + 1 nhân viên.
