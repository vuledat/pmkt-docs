# Coding Convention — Java (các module Spring Boot)

> Tách từ `conventions.md` (2026-08-23) để tác vụ FE và tác vụ Java không phải nạp phần của nhau.
> Nội dung giữ **nguyên văn**. Phần dùng chung cho cả hai: [`conventions-chung.md`](conventions-chung.md).

## 3. Coding Convention — Java (các module Spring Boot)

Stack: Java 21 · Spring Boot · Gradle Kotlin DSL · base package `vn.vtt.pmkt`.

### 3.1 Quy ước đặt tên

| Đối tượng | Quy tắc | Ví dụ |
|---|---|---|
| Class, Interface, Enum, Record | PascalCase | `UserService`, `OrderController`, `UserStatus` |
| Package | chữ thường toàn bộ, `snake_case` khi cần tách từ | `vn.vtt.pmkt.identity.service.impl`, `…​.ban_hang` |
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
INTELLIJ, TUYỆT ĐỐI KHÔNG DOCKER" ở `../../CLAUDE.md` gốc.

Service Java chưa có làn `unitTest` riêng, hoặc cần chạy sâu hơn → chạy test class / run
configuration **qua IntelliJ** (`mcp__idea__get_run_configurations` +
`mcp__idea__execute_run_configuration`, truyền `projectPath`), rồi nói rõ trong báo cáo là phần
tích hợp Testcontainers chưa chạy.

---
