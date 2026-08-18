# Quy định & Quy tắc phát triển — VTT / OSP

> Tài liệu gốc (single source of truth). Mọi `CLAUDE.md` trong repo đều trỏ về đây.
> Áp dụng cho **tất cả project** trong `vtt-osp`: `client` (FE) và các module Java
> (`cell-app`, `cell-gateway`, `front-door`, `identity`, `integration-platform`,
> `shared-kernel`, `tenant-provisioning`).

---

## 0. Cách đọc tài liệu này

| Từ khóa | Nghĩa | Hệ quả khi vi phạm |
|---|---|---|
| **BẮT BUỘC** | Không có ngoại lệ | Reviewer **reject PR** |
| **KHÔNG ĐƯỢC** | Cấm tuyệt đối | Reviewer **reject PR** |
| **NÊN** | Mặc định đúng | Được phép khác, nhưng phải ghi lý do trong mô tả PR |

**Dành cho AI agent (Claude Code, Cursor, Copilot…):** đây là ràng buộc cứng khi sinh code.
Trước khi kết thúc một task, tự chạy [Checklist §5](#5-checklist-trước-khi-commit) và báo cáo trung thực
mục nào chưa đạt. Nếu quy định này mâu thuẫn với code hiện có, **hỏi người dùng**, không tự ý sửa hàng loạt.

---

## 1. Quy tắc chung (áp dụng cho mọi ngôn ngữ)

### 1.1 Không hardcode — BẮT BUỘC

Mọi giá trị có ý nghĩa nghiệp vụ (số, chuỗi, timeout, mã trạng thái, URL, kích thước trang…)
phải đặt tên qua constant hoặc file cấu hình. Không để "magic value" nằm giữa logic.

```ts
// ❌ SAI — 10 là gì? 3 lần retry hay 3 giây?
const res = await api.get('/users', { params: { size: 10 } })
if (retry < 3) ...

// ✅ ĐÚNG
const PAGE_SIZE = 10
const MAX_RETRY_COUNT = 3
const res = await api.get('/users', { params: { size: PAGE_SIZE } })
if (retry < MAX_RETRY_COUNT) ...
```

**Ngoại lệ hợp lệ (không cần đặt tên):** `0`, `1`, `-1` dùng làm chỉ số/bước nhảy; chuỗi rỗng `''`.

### 1.2 Phạm vi constant — BẮT BUỘC

Constant đặt **gần nơi dùng nhất có thể**:

- Dùng trong 1 file → khai báo đầu file đó.
- Dùng trong 1 module/feature → `constants` của chính module đó.
- Dùng ≥ 2 module → mới đưa lên tầng dùng chung (`@core`/`@base` ở FE, `shared-kernel` ở BE).

Không dồn hết vào một file `constants` khổng lồ toàn cục.

### 1.3 Secret & cấu hình môi trường — BẮT BUỘC

**KHÔNG ĐƯỢC** commit secret (mật khẩu, API key, token, connection string thật) vào Git —
kể cả trong file test, comment, hay dữ liệu mẫu. Secret nằm ở biến môi trường / `application.yml`
theo profile / secret manager. Phát hiện secret đã lỡ commit → báo ngay, **rotate key**, không chỉ xóa commit.

### 1.4 Không để lại rác — BẮT BUỘC

Không commit: code bị comment lại "để dành", `console.log` / `System.out.println` debug,
`TODO` không có ngữ cảnh, file thử nghiệm tạm. `TODO` hợp lệ phải có dạng
`// TODO(<mã ticket>): <việc cần làm>`.

---

## 2. Coding Convention — Frontend (`client`)

Stack: React 19 · TypeScript (strict) · Vite · Ant Design · TanStack Query · i18next · Zod.

### 2.1 Quy ước đặt tên

| Đối tượng | Quy tắc | Ví dụ |
|---|---|---|
| File `.tsx` (component) | PascalCase | `UserProfile.tsx`, `ButtonPrimary.tsx` |
| File `.ts` (logic, hook, util) | camelCase | `formatDate.ts`, `useAuth.ts` |
| Thư mục | camelCase | `src/features/tienGui/`, `src/base/domainKit/` |
| Function, variable | camelCase | `const userData = …`, `function calculateTotal() {}` |
| Constant | SCREAMING_SNAKE_CASE | `const MAX_RETRY_COUNT = 3` |
| Component, Interface, Type, Enum | PascalCase | `interface UserProfileProps {}`, `enum UserRole {}` |
| Custom hook | camelCase, tiền tố `use` | `useFetchList.ts`, `useWindowSize.ts` |
| Prop sự kiện | `onXxx` | `<Button onClick={…} />`, `onSubmitForm` |
| Hàm xử lý sự kiện | `handleXxx` | `const handleClickSubmit = () => {}` |

```tsx
// ✅ Cặp prop/handler chuẩn
<Button onClick={handleClickSubmit} />
```

### 2.2 TypeScript — Type safety

- **KHÔNG ĐƯỢC dùng `any`** (kể cả `as any`, `any[]`, `Promise<any>`).
- Chưa biết kiểu → dùng `unknown` rồi thu hẹp (narrow) bằng type guard hoặc Zod.
- Dữ liệu từ API/`localStorage`/query param là **dữ liệu không tin cậy**: parse bằng Zod schema, không ép kiểu mù.
- **KHÔNG ĐƯỢC** dùng `@ts-ignore`. Trường hợp bất khả kháng dùng `@ts-expect-error` kèm comment lý do.

```ts
// ❌ SAI
const user = (await res.json()) as any

// ✅ ĐÚNG
const user = UserSchema.parse(await res.json())   // UserSchema: z.object({...})
```

### 2.3 i18n — Không hardcode text

Mọi chuỗi người dùng nhìn thấy (label, title, nút, thông báo lỗi, placeholder, tooltip, cột bảng)
**BẮT BUỘC** khai báo song ngữ trong `src/app/i18n/vi.ts` và `en.ts`.

**Key phân tầng theo module/feature:** `<module>.<màn hình>.<thành phần>`

```
auth.login.submitButton
common.label.cancel
tienGui.list.columnAmount
```

Chuỗi động **BẮT BUỘC** dùng interpolation, **KHÔNG ĐƯỢC** cộng chuỗi (cộng chuỗi sai trật tự từ ở ngôn ngữ khác):

```ts
// ❌ SAI
t('welcome') + ' ' + name

// ✅ ĐÚNG
t('welcome_user', { name })
```

Không cần i18n: log kỹ thuật, key nội bộ, mã lỗi backend.

### 2.4 Import & cấu trúc

**BẮT BUỘC dùng path alias**, KHÔNG ĐƯỢC dùng relative path vượt cấp (`../../`).
Alias theo tầng của repo này:

| Alias | Tầng |
|---|---|
| `@core` / `@core/*` | tiện ích thuần, không phụ thuộc UI |
| `@base` / `@base/*` | thành phần dùng chung |
| `@domain-kit` / `@domain-kit/*` | khối nghiệp vụ dùng chung |
| `@platform` / `@platform/*` | hạ tầng: auth, http, query, tenant, rbac |
| `@features/*` | từng nghiệp vụ |
| `@app/*` | router, layout, provider, i18n |
| `@test/*` | tiện ích test |

```ts
// ❌ SAI
import { Button } from '../../../base/components/Button'

// ✅ ĐÚNG
import { Button } from '@base/components/Button'
```

**Luật tầng (tier boundary):** import chỉ được đi **xuống dưới**
(`app → features → platform → domain-kit → base → core`), không đi ngược, không đi ngang giữa hai `features`.
Luật này được ép bằng lint: `npm run lint:boundaries`.

**Export:** NÊN dùng **named export**; chỉ dùng `default` khi framework bắt buộc.

```ts
// ✅ export const UserCard = () => {}
// ❌ export default function UserCard() {}
```

### 2.5 Lệnh kiểm tra bắt buộc trước khi commit (`client/`)

```bash
npm run typecheck        # không được có lỗi
npm run lint             # không được có error
npm run lint:boundaries  # luật tầng
npm run test             # test phải xanh
```

---

## 3. Coding Convention — Java (các module Spring Boot)

Stack: Java 21 · Spring Boot · Gradle Kotlin DSL · base package `vn.dopai.pmkt`.

### 3.1 Quy ước đặt tên

| Đối tượng | Quy tắc | Ví dụ |
|---|---|---|
| Class, Interface, Enum, Record | PascalCase | `UserService`, `OrderController`, `UserStatus` |
| Package | chữ thường toàn bộ, `snake_case` khi cần tách từ | `vn.dopai.pmkt.identity.service.impl`, `…​.ban_hang` |
| Method, variable, parameter | camelCase | `getUserById()`, `totalAmount`, `orderId` |
| Constant, giá trị Enum | SCREAMING_SNAKE_CASE + `static final` | `public static final int MAX_PAGE_SIZE = 50;` |
| Bảng & cột DB (JPA) | snake_case | `@Table(name = "user_account")`, `@Column(name = "created_at")` |
| DTO / Request / Response | hậu tố rõ mục đích | `CreateUserRequest`, `UserResponse`, `UserDto` |

### 3.2 Kiến trúc phân tầng — BẮT BUỘC

```
Controller  →  Service  →  Repository  →  Entity
```

- **Controller**: nhận request, validate đầu vào (`@Valid`), gọi Service, trả DTO. **Không** chứa business logic, **không** gọi Repository trực tiếp.
- **Service**: toàn bộ business logic, quản lý `@Transactional`.
- **Repository**: chỉ truy cập dữ liệu.
- **Entity KHÔNG ĐƯỢC** lộ ra ngoài Controller — luôn map sang DTO.

### 3.3 Chuẩn API

- **Response**: tất cả API dùng **một wrapper thống nhất** `ApiResponse<T>` gồm `code`, `message`, `data`, `timestamp`.
- **Exception**: xử lý tập trung bằng `@RestControllerAdvice` + `@ExceptionHandler`.
  **KHÔNG ĐƯỢC** `try/catch` rồi trả lỗi thủ công trong Controller; ném exception nghiệp vụ để handler chung xử lý.
  **KHÔNG ĐƯỢC** nuốt exception (`catch (Exception e) {}`) hoặc trả message lộ stacktrace/thông tin nội bộ ra client.

### 3.4 Cấu hình & hardcode

- Giá trị cố định → `private static final`; giá trị theo môi trường → `application.yml` / `application.properties`.
- Đọc cấu hình qua `@ConfigurationProperties` (ưu tiên) hoặc `@Value("${app.jwt.secret}")`.
- Secret: xem [§1.3](#13-secret--cấu-hình-môi-trường--bắt-buộc).

### 3.5 Dependency Injection & code sạch

- **NÊN dùng Constructor Injection** với Lombok `@RequiredArgsConstructor` + field `private final`.
- Hạn chế `@Autowired` trực tiếp trên field (khó test, che giấu phụ thuộc bắt buộc).

```java
// ✅ ĐÚNG
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
}
```

### 3.6 Database & JPA

- `@Column` **BẮT BUỘC** khai báo rõ `nullable`, `length` (với chuỗi), kiểu dữ liệu khi không mặc định.
- Quan hệ mặc định `FetchType.LAZY`; nạp dữ liệu cần thiết bằng `JOIN FETCH` / `@EntityGraph` **trong** transaction
  để tránh `LazyInitializationException` và N+1 query.
- Thay đổi schema đi qua migration script, không sửa tay trên môi trường chung.

### 3.7 Lệnh kiểm tra trước khi commit (module Java)

Mỗi service Java là một **Gradle project ĐỘC LẬP** (wrapper riêng, `settings.gradle.kts` riêng);
repo gốc KHÔNG có `gradlew`. Phải `cd` vào service rồi mới chạy — `./gradlew :<module>:build` từ gốc
repo sẽ báo "no such file or directory".

```bash
cd cell-app && ./gradlew unitTest   # CỔNG CHÍNH — chỉ @Tag("unit"), thuần JVM, ~1 phút
```

🚫 **KHÔNG `./gradlew build`, KHÔNG `./gradlew test`, KHÔNG Docker.** Cả hai task đó kéo test
Testcontainers và **bắt buộc có Docker** — thứ bị cấm tuyệt đối, xem luật cứng "CHẠY CODE — QUA
INTELLIJ, TUYỆT ĐỐI KHÔNG DOCKER" ở `CLAUDE.md` gốc.

Service Java chưa có làn `unitTest` riêng, hoặc cần chạy sâu hơn → chạy test class / run
configuration **qua IntelliJ** (`mcp__idea__get_run_configurations` +
`mcp__idea__execute_run_configuration`, truyền `projectPath`), rồi nói rõ trong báo cáo là phần
tích hợp Testcontainers chưa chạy.

---

## 4. Git

### 4.1 Commit message

Định dạng: `<type>(<scope>): <mô tả ngắn, thể mệnh lệnh>`

| Type | Dùng khi |
|---|---|
| `feat` | Thêm tính năng mới |
| `fix` | Sửa lỗi / sự cố kỹ thuật |
| `docs` | Tài liệu, comment, README |
| `style` | Định dạng code (khoảng trắng, layout) — **không đổi logic** |
| `refactor` | Tái cấu trúc bên trong, **giữ nguyên hành vi bên ngoài** |
| `perf` | Cải thiện hiệu năng |
| `test` | Thêm/sửa test |
| `chore` | Build tool, cấu hình, cập nhật dependency |

```
✅ feat(auth): add login with Google OAuth
✅ fix(tienGui): sửa sai số làm tròn khi tính lãi
❌ update code
❌ fix bug
```

Quy tắc: 1 commit = 1 ý nghĩa. Không trộn `feat` + `refactor` + format lại toàn file trong cùng commit.

### 4.2 Nhánh

| Nhánh | Mục đích | Tách từ | Merge về |
|---|---|---|---|
| `master` | Code production-ready. **Không bao giờ commit trực tiếp.** | — | — |
| `develop` | Tích hợp tính năng, integration testing | `master` | `master` (qua `release/*`) |
| `feat/*` | Phát triển tính năng mới | `develop` | `develop` |
| `bugfix/*` | Sửa lỗi phát hiện khi test (chưa lên production) | `develop` | `develop` |
| `release/*` | Đóng gói phiên bản, kiểm thử cuối, sửa lỗi nhỏ | `develop` | `master` + `develop` |
| `hotfix/*` | Sửa lỗi **khẩn cấp trên production** | `master` | `master` + `develop` |

> Dùng tiền tố `bugfix/` (không dùng `fix/`) để phân biệt rõ với nhánh tính năng.

### 4.3 Quy tắc đặt tên nhánh

Cấu trúc: **`loại-nhánh/tên-mô-tả-ngắn-gọn`** — chữ thường, phân cách bằng dấu `-`.

```
feat/login
feat/customer-api
feat/order-import
feat/report-sale
bugfix/login
hotfix/payment
release/v1.2
chore/update-dependency
refactor/auth
docs/api
```

### 4.4 Git flow

```
master
│
├── develop
│    ├── feat/login
│    │       └── bugfix/login
│    ├── feat/customer
│    │       └── bugfix/customer
│    ├── feat/product
│    ├── feat/order
│    └── feat/report
│
├── release/*
│
└── hotfix/*
```

---

## 5. Checklist trước khi commit

Tự soát (DEV **và** AI agent) — mọi mục phải ✅ mới được tạo PR:

**Chung**
- [ ] Không còn magic value / text hardcode
- [ ] Không có secret trong diff
- [ ] Không còn code debug, code comment "để dành"
- [ ] Commit message đúng `<type>(<scope>): <mô tả>`
- [ ] Đang ở đúng nhánh (không phải `master`/`develop`)

**Nếu chạm `client/`**
- [ ] Không có `any` / `@ts-ignore` mới
- [ ] Text mới đã có key i18n ở **cả** `vi.ts` và `en.ts`
- [ ] Import dùng alias, không có `../../`
- [ ] `npm run typecheck && npm run lint && npm run lint:boundaries && npm run test` — xanh

**Nếu chạm module Java**
- [ ] Business logic nằm ở Service, Controller không gọi Repository
- [ ] Không trả Entity ra Controller
- [ ] API trả `ApiResponse<T>`; lỗi qua Global Exception Handler
- [ ] Dùng constructor injection
- [ ] `cd cell-app && ./gradlew unitTest` — xanh (repo gốc không có `gradlew`; **không** chạy
      `./gradlew build` vì nó cần Docker — §3.7)

---

## 6. Khi quy định mâu thuẫn với code hiện tại

Không tự ý refactor hàng loạt. Thứ tự xử lý:

1. **Code mới** → tuân thủ 100% tài liệu này.
2. **Code cũ đang sửa** → dọn theo quy tắc trong phạm vi thay đổi (boy-scout rule), không mở rộng diff.
3. **Vi phạm diện rộng** → ghi nhận thành ticket riêng, báo team lead, không gộp vào PR tính năng.

---

## 7. Vùng đóng băng (legacy) — KHÔNG ĐƯỢC đọc & tham khảo

Một số vùng code đã lỗi thời về kiến trúc và **ngừng phát triển**. Chúng vẫn nằm trong repo vì còn
chạy production, nhưng **KHÔNG ĐƯỢC** dùng làm chuẩn tham chiếu — mọi pattern trong đó đều đi trước
tài liệu này và đọc chúng chỉ làm code mới bị nhân bản lỗi cũ.

### 7.1 Danh sách vùng đóng băng

| Đường dẫn | Lý do |
|---|---|
| `cell-app/src/main/java/vn/dopai/pmkt/cell/master_data/**` | Kiến trúc cũ (`controller/ dto/ entity/ repository/ service/` phẳng, không có ranh giới `internal/` của Modulith); không phát triển tiếp |

### 7.2 Quy tắc — BẮT BUỘC (áp dụng cho cả người và AI agent)

- **KHÔNG ĐƯỢC đọc** file trong vùng đóng băng để tìm hiểu "dự án đang làm thế nào".
- **KHÔNG ĐƯỢC sao chép** kiến trúc, cách chia package, cách đặt tên, pattern hay đoạn code từ đó.
- **KHÔNG ĐƯỢC dùng làm mẫu** cho module / màn hình / API mới — kể cả khi việc mới cùng loại nghiệp vụ.
- Kết quả `grep` / `glob` rơi vào vùng đóng băng → **bỏ qua**, không trích làm bằng chứng cho quy ước
  hiện hành của dự án.
- Mẫu tham khảo đúng cho `cell-app`: `chung_tu_ban_hang/`, `accounting_core/`, `platform_iam/`,
  `integration_ops/`, `common/` (Modulith, có `internal/` + `package-info.java`).

### 7.3 Ngoại lệ

Chỉ được chạm vào vùng đóng băng khi:

1. Người dùng / ticket **yêu cầu trực tiếp** sửa, vá lỗi trong vùng đó; hoặc
2. Module khác **lỗi biên dịch** vì API công khai của nó (`master_data.co_cau_to_chuc.dto`,
   `master_data.co_cau_to_chuc.service`, `master_data.TenantProvisioner`).

Khi đó: đọc **đúng phần chữ ký cần dùng**, không mang kiến trúc từ đó sang code mới, giữ diff tối
thiểu, và **nói rõ trong PR / phản hồi** rằng đang phải chạm vào vùng đóng băng.

### 7.4 Code mới thuộc nghiệp vụ danh mục

Không thêm file mới vào `master_data/`. Danh mục mới đặt ở module tương ứng theo kiến trúc Modulith
hiện hành; nếu chưa rõ đặt ở đâu, **hỏi team lead** trước khi tạo package.
