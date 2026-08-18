# BE — Khung kiến trúc chuẩn cho một phiếu yêu cầu

Bản trích từ `cell-app/src/main/java/vn/dopai/pmkt/cell/` (đo ngày 2026-08-11). Đây là **khung bắt
buộc**: mọi phiếu yêu cầu (module / API / bảng mới) làm ở backend phải sinh ra đúng bộ artefact dưới
đây, đúng vị trí, đúng tên. Không có ngoại lệ cho "API nhỏ".

**Module tham chiếu:**

| Loại việc | Đọc module này |
|---|---|
| Chứng từ kế toán (thêm/sửa/xoá/ghi sổ) | `cell/chung_tu_ban_hang/` |
| Kernel / engine dùng chung nhiều module | `cell/accounting_core/` |
| CRUD + phân quyền | `cell/platform_iam/quyen/`, `cell/platform_iam/nguoi_dung/` |
| Outbox / inbox / gọi hệ thống ngoài | `cell/integration_ops/` |

SSOT chi tiết: [cell-app/CLAUDE.md](../cell-app/CLAUDE.md) · [docs/conventions.md §3](conventions.md) ·
song song với bản FE: [docs/fe-khung-kien-truc-chuan.md](fe-khung-kien-truc-chuan.md).

---

## 1. Bản đồ dịch vụ — biết mình được viết ở đâu

| Dịch vụ | Vai trò | Kiến trúc |
|---|---|---|
| **`cell-app/`** | nghiệp vụ kế toán (nơi ~90% phiếu yêu cầu đáp xuống) | **Spring Modulith** — §2 |
| `cell-gateway/` · `front-door/` | định tuyến, cửa vào | phẳng `controller/ service/ …`, xem CLAUDE.md của module |
| `identity/` | xác thực | như trên |
| `integration-platform/` | tích hợp ngoài, có migration riêng | như trên |
| `tenant-provisioning/` | control-plane, cấp phát tenant | chia theo bounded context (`controlplane/<ctx>/`) |
| `shared-kernel/` | thư viện dùng chung | như trên |

Base package chung: `vn.dopai.pmkt`. Stack: Java 21 · Spring Boot · Gradle Kotlin DSL.

**Tài liệu này mô tả chuẩn của `cell-app`.** Dịch vụ khác giữ shape riêng đã có; trước khi sửa phải
đọc `CLAUDE.md` trong đúng thư mục đó (luật cộng dồn — xem CLAUDE.md gốc).

---

## 2. Cấu trúc chuẩn của một module `cell-app` — BẮT BUỘC

`cell-app` là **Spring Modulith**: mỗi thư mục cấp 1 dưới `cell/` là một application module, ranh
giới do `package-info.java` khai và Modulith kiểm.

```
cell/<module>/                      ← một module nghiệp vụ (snake_case)
├── package-info.java               ← BẮT BUỘC: @ApplicationModule(displayName = "<module>")
├── api/                            ← CHỈ tạo khi module khác thật sự cần gọi vào
│   ├── package-info.java             @NamedInterface("<tên>") — không khai thì Modulith chặn
│   └── dto/                          record công khai đi kèm hợp đồng
└── internal/                       ← mặc định MỌI thứ nằm ở đây; module khác không import được
    ├── controller/                 REST adapter — @RestController
    ├── dto/                        Request / Response / Dto của riêng module
    ├── entity/                     @Entity + @Table
    ├── model/                      enum, mã lỗi, hằng số nghiệp vụ
    ├── port/                       interface module khác cắm vào (outbound port)
    ├── repository/                 Spring Data + …RepositoryCustom/…RepositoryImpl khi cần query động
    └── service/
        ├── <Tên>CrudService.java   điều phối
        └── business/               logic nghiệp vụ tách nhỏ: template · mapper · validator · tính toán
```

**Luật cứng 1 — mặc định là `internal/`.** Không tạo `api/` "cho chắc". Một thư mục `api/` không ai
gọi tới là một hợp đồng công khai không có người dùng, và nó khoá tay refactor về sau.
`chung_tu_ban_hang/` — module chứng từ đầy đủ nhất repo — **không có `api/` nào**.

**Luật cứng 2 — `api/` phải có `package-info.java` khai `@NamedInterface`.** Lộ `x.api` **không** tự
động lộ `x.api.dto` hay `x.api.error`: mỗi package con cần `@NamedInterface` riêng, nếu không module
khác import vào là vi phạm ranh giới (đã có đúng một lỗi như vậy bị `ProxyModularityTest` bắt).

**Luật cứng 3 — không đổ file phẳng ra gốc module.** Gốc module chỉ có `package-info.java` và các
thư mục con. Shape `controller/ dto/ entity/ repository/ service/` nằm thẳng ở gốc (không có
`internal/`) là **shape cũ đã đóng băng** — xem §8.

**Module lớn thì chia sub-module trước, rồi mới `api/ internal/`:**

```
cell/<module>/<sub>/api|internal/…       vd platform_iam/quyen/{api,internal}
                                            integration_ops/outbox/{api,internal}
                                            accounting_core/hach_toan/{api,internal}
```

### 2.1 File mới đặt đâu — cây quyết định (dừng ở dòng đầu tiên đúng)

```
Là @RestController?                        → internal/controller/
Là @Entity?                                → internal/entity/
Là interface Spring Data?                  → internal/repository/
Là enum / mã lỗi / hằng số nghiệp vụ?      → internal/model/
Là record Request/Response/Dto?            → internal/dto/   (api/dto/ nếu là hợp đồng công khai)
Là interface cho module khác cài đặt?      → internal/port/
Là công thức / quy tắc / mapper?           → internal/service/business/
Điều phối + @Transactional?                → internal/service/
Module KHÁC phải gọi được?                 → api/  + @NamedInterface
```

### 2.2 Visibility — Modulith chỉ chặn được cái bạn không mở

| Thành phần | Visibility | Vì sao |
|---|---|---|
| `@RestController` + constructor của nó | **package-private** (`class XxxController`) | không ai ngoài Spring cần tham chiếu; `public` là mời gọi lách ranh giới |
| `…RepositoryImpl` | package-private | chi tiết cài đặt của `…RepositoryCustom` |
| Service, entity, dto, enum trong `internal/` | `public` là chấp nhận được | Modulith đã chặn ở mức package; `public` ở đây chỉ để trong-module dùng nhau |
| Mọi thứ trong `api/` | `public` | đó là hợp đồng |

Mẫu: `ChungTuBanHangController` khai `class …` (không `public`), `ChungTuBanHangRepositoryImpl` cũng vậy.

---

## 3. Đừng viết lại khung — `core/` đã cấp sẵn

Trước khi viết controller/service, kiểm `cell/core/`:

| Cần gì | Dùng cái có sẵn |
|---|---|
| Bộ endpoint CRUD + tìm kiếm động | `core.controller.BaseCrudController` |
| Chứng từ kế toán (ghi sổ, bỏ ghi sổ, nhân bản, hàng loạt) | `accounting_core.chung_tu.controller.BaseChungTuController` |
| Luồng thêm/sửa/xoá chứng từ (12 bước, bất biến kế toán) | `accounting_core.chung_tu.service.ChungTuTemplate` |
| CRUD service | `core.service.BaseCrudService` / `AbstractCrudService` |
| Wrapper response | `core.response.ApiResponse<T>` · `PageResponse` · `ListItemResponse` |
| Kiểm quyền | `core.controller.QuyenChecker` |
| Lọc / sắp xếp động theo whitelist | `core.shared.search.*` + `@Searchable` trên entity |
| Ghi sổ cái | `accounting_core.hach_toan.api.GhiSoApi` — **nơi DUY NHẤT** được insert `acc_so_cai` |

`BaseCrudController` cấp sẵn 8 endpoint, **không viết lại cái nào**:

```
POST /search      GET /cot        GET /{id}       POST /them-moi
PUT  /{id}        DELETE /{id}    POST /export    POST /import
```

`QuyenChecker` cấp sẵn action: `View` · `View.Detail` · `Create` · `Edit` · `Delete` · `Export` ·
`Import` · `Post` · `Unpost` · `Clone`. Mã quyền = `<MaChucNang>.<Action>`, ví dụ `BanHangHoa.Post`.

Chứng từ kế toán **không** dùng `BaseCrudService` cho thêm/sửa/xoá: thứ tự "gỡ bút toán cũ → lưu →
sinh bút toán mới → kiểm kỳ khoá" là bất biến, không phải lựa chọn của từng màn. Phần ĐỌC (tìm kiếm,
phân trang, chi tiết, export) vẫn dùng `core` như mọi màn danh sách.

---

## 4. Phân tầng — BẮT BUỘC

```
Controller  →  Service  →  Repository  →  Entity
```

- **Controller**: nhận request, `@Valid`, gọi Service, trả DTO. KHÔNG business logic, KHÔNG gọi
  Repository trực tiếp.
- **Service**: toàn bộ business logic, quản lý `@Transactional`.
- **Repository**: chỉ truy cập dữ liệu.
- **Entity KHÔNG ĐƯỢC** trả ra Controller — luôn map sang DTO.
- **Response**: mọi API bọc `ApiResponse<T>` (`code`, `message`, `data`, `timestamp`).
- **Lỗi**: xử lý tập trung bằng `@RestControllerAdvice` + `@ExceptionHandler`. KHÔNG `try/catch` trả
  lỗi thủ công trong Controller, KHÔNG nuốt exception, KHÔNG trả stacktrace ra client.
- **DI**: constructor injection — `private final` + `@RequiredArgsConstructor`. Hạn chế `@Autowired`
  trên field.

---

## 5. Bộ artefact tối thiểu của một phiếu — checklist sinh file

| # | Artefact | Đường dẫn | Bắt buộc |
|---|---|---|---|
| 1 | Khai báo module | `cell/<module>/package-info.java` (`@ApplicationModule`) | ✅ |
| 2 | Migration schema | `cell-app/src/main/resources/db/migration/V<N>__<prefix>_<mô_tả>.sql` | ✅ nếu có bảng |
| 3 | Entity | `internal/entity/` | ✅ |
| 4 | Repository | `internal/repository/` | ✅ |
| 5 | Enum / mã lỗi nghiệp vụ | `internal/model/` | ✅ nếu có enum/mã lỗi |
| 6 | DTO Request / Response | `internal/dto/` | ✅ |
| 7 | Logic nghiệp vụ | `internal/service/business/` | ✅ nếu có công thức/quy tắc |
| 8 | Service điều phối | `internal/service/` | ✅ |
| 9 | Controller | `internal/controller/` | ✅ |
| 10 | Seed mã quyền | migration (`iam_quyen`) | ✅ |
| 11 | Test | `src/test/java/…/<module>/` **song ánh** cây `main` | ✅ |
| 12 | Hợp đồng công khai + `@NamedInterface` | `api/` | ⬜ chỉ khi module khác cần gọi |

**Test đặt song ánh với `main`** — `chung_tu_ban_hang/internal/service/` ở `main` thì test nằm ở
`src/test/java/…/chung_tu_ban_hang/internal/service/`. Test thuần JVM gắn `@Tag("unit")` để vào được
làn `unitTest`.

---

## 6. Quy ước dữ liệu

**Tiền tố bảng — mỗi module một tiền tố, khai ngay ở `package-info.java`:**

| Module | Tiền tố | | Module | Tiền tố |
|---|---|---|---|---|
| `accounting_core` | `acc_` | | `platform_iam` | `iam_` |
| `chung_tu_ban_hang` | `sal_` | | `integration_ops` | `ops_` |
| `chung_tu_mua_hang` | `pur_` | | `quan_he_chung_tu` | `ctu_` |
| `master_data` (đóng băng) | `mst_` | | audit | `aud_` |

Module mới → chọn tiền tố mới, **ghi vào `package-info.java`** dòng đầu: `<module> ({@code xxx_}) — …`.

**Migration:** `V<N>__<prefix>_<mô_tả_snake_case>.sql`, N tăng dần toàn repo (hiện đã tới V83+ trong
tổng 311 file). Không sửa file migration đã merge — thêm file mới.

**JPA:**
- `@Column` khai rõ `nullable`, `length` (chuỗi), kiểu khi không mặc định.
- Quan hệ mặc định `FetchType.LAZY`; nạp bằng `JOIN FETCH` / `@EntityGraph` **trong** transaction.
- Aggregate root: dòng con `cascade = ALL` + `orphanRemoval`, khoá lạc quan qua trường `phien_ban`.
  Sửa chỉ chạm dòng con thì gọi `touch()` — không thì hai người sửa hai dòng sẽ ghi đè nhau im lặng.
- Cột nào FE được phép lọc/sắp xếp thì khai `@Searchable` (whitelist). **Không khai = không lọc được** —
  đó là hàng rào, không phải thiếu sót.
- Ràng buộc kế toán đã có ở tầng DB (trigger cân đối Nợ/Có, chặn kỳ khoá, chống sửa in-place,
  idempotency, audit log). Java kiểm lại **trước** khi ghi không phải vì không tin DB, mà để lỗi có
  ngữ cảnh đọc được thay vì nổ ở COMMIT.

---

## 7. Cổng nghiệm thu (DoD) — chạy trước khi báo hoàn thành

```bash
cd cell-app && ./gradlew build
```

⚠ **`cell-app/` là Gradle project ĐỘC LẬP** (có wrapper riêng, `rootProject.name = "cell-app"`); repo
gốc **không** có `gradlew`. Lệnh `./gradlew :cell-app:build` ở gốc repo sẽ báo "no such file or
directory".

Hai làn test:

| Lệnh | Chạy gì | Khi nào dùng |
|---|---|---|
| `./gradlew unitTest` | chỉ `@Tag("unit")`, thuần JVM, ~1 phút | cổng xanh thực tế, luôn chạy được |
| `./gradlew build` | cả bộ tích hợp qua Testcontainers | cần **Docker đang chạy** |

Không có Docker thì `build` đỏ ở ~25 test Testcontainers (`Could not find a valid Docker
environment`) — đó là giới hạn môi trường, **không phải hồi quy**. Đối chiếu danh sách lớp lỗi trước
khi kết luận, và nói rõ cho user là đã dùng `unitTest` làm cổng thay thế.

**Ranh giới Modulith:** `ApplicationModules.verify()` hiện **không** chạy trần được — `cell-app` còn
**96 vi phạm ranh giới có sẵn từ trước** (`core → platform_iam`, `platform_iam → master_data`,
`chung_tu_* → accounting_core.hach_toan.api.dto`). Mẫu xử lý đúng: viết test chỉ soi vi phạm **có
nhắc tới module mình** (xem `cell/arch/ProxyModularityTest.java`) — module mới bị giữ ở chuẩn đầy đủ
ngay từ đầu, nợ cũ vẫn nhìn thấy mà không chặn ai.

Luật nghiệm thu:

1. **Không làm xấu hơn baseline** — không lệnh nào được tăng số lỗi, số vi phạm ranh giới không tăng.
2. **Module mới phải sạch tuyệt đối** về ranh giới Modulith — không mang nợ ngay từ ngày đầu.
3. Lệnh nào fail thì **dán output thật**, không báo "đã xong".
4. Báo cáo hoàn thành phải **liệt kê BR đã áp dụng** và BR chưa đạt (kèm lý do) — §9.

---

## 8. Vùng cấm & shape đóng băng

| Vùng | Luật |
|---|---|
| **`cell/master_data/**` — VÙNG ĐÓNG BĂNG** | ✗ **Không đọc** để tham khảo (grep rơi vào đây thì bỏ qua, không trích làm bằng chứng cho quy ước hiện hành) · ✗ **Không sao chép** kiến trúc / cách chia package / cách đặt tên / pattern · ✗ **Không dùng làm mẫu** cho module mới, kể cả module danh mục. Chặn cứng ở `.claude/settings.json` (`permissions.deny` cho tool `Read`) |
| `master_data` khi ĐÃ được cho phép | Chỉ đọc **đúng** chữ ký cần dùng (`master_data.*.dto`, `master_data.*.service`, `TenantProvisioner`), không mang kiến trúc sang, **báo rõ cho user** là đang chạm vùng đóng băng, và **xin phép** gỡ tạm rule deny |
| **Shape phẳng không có `internal/`** | `controller/ dto/ entity/ repository/ service/` nằm thẳng ở gốc module. Nợ còn lại: `platform_iam/rbac_console/`, `common/mau_excel/`, `common/ui_config/`. **Không mở module mới theo shape này** |
| `client/src/legacy/` | Vùng khoá của FE — xem [fe-khung-kien-truc-chuan.md §10](fe-khung-kien-truc-chuan.md) |

**Nợ hiện tại (đo 2026-08-11):** 96 vi phạm ranh giới Modulith · 3 sub-module còn shape phẳng ·
`master_data` chưa chuyển.

Luật áp **từ nay về sau**: module mới đủ chuẩn; module cũ chuyển dần khi có việc chạm vào. Không mở
đợt refactor toàn bộ nếu không được giao.

---

## 9. Quy chuẩn nghiệp vụ (BR) phải đối chiếu

Mọi phiếu phải code theo [pmkt-docs/ba/Common/business_rules.md](../pmkt-docs/ba/Common/business_rules.md).
Epic chỉ mô tả phần đặc thù; phần chung **mặc định lấy theo BR**. Epic không nhắc BR ≠ được bỏ BR.

BR hay dùng ở BE:

| Phạm vi | BR phải đọc |
|---|---|
| Entity / DB / API | BR7 precision · BR19 kiểm tra trùng · BR20 số chứng từ & mã danh mục · BR28 multi-tenant · BR29 chính sách xóa · BR46 trường hệ thống bắt buộc |
| Chứng từ & hạch toán | BR4 loại chứng từ · BR9 mã chứng từ · BR12 trạng thái · BR17 kỳ kế toán · BR36 ghi sổ · BR37 ngày hạch toán · BR41 tham chiếu chéo · BR42 bỏ ghi sổ |
| Số liệu / tiền tệ | BR7 precision & làm tròn · BR18 ngoại tệ |
| Quyền | BR25 phân quyền |
| Thông báo | BR16 cảnh báo nghiệp vụ |

**Quy ước tiền tệ (BR9/BR18):** trường gốc (`thanh_tien`, `chiet_khau`, `tien_thue_gtgt`…) lưu theo
LOẠI TIỀN đã chọn; trường `*_quy_doi` lưu theo ĐỒNG TIỀN HẠCH TOÁN (`= gốc × tỷ giá`). Sổ cái luôn ghi
bằng đồng tiền hạch toán, phần nguyên tệ đi kèm qua `DinhKhoan.voiNgoaiTe(...)`.

**Xung đột / thiếu quy định:** epic khác BR → epic thắng trong đúng phạm vi epic, và phải **báo rõ**
đang lệch BR nào. BR chưa phủ → **hỏi user**, không tự đặt luật mới rồi code luôn.

---

## 10. Luật cứng áp cho mọi phiếu

1. **Không hardcode magic value** — `private static final` có tên, đặt gần nơi dùng nhất.
2. **Không commit secret** — dùng env / `application.yml` / `@ConfigurationProperties`.
3. **Phân tầng** `Controller → Service → Repository → Entity`; Controller không chứa business logic,
   không gọi Repository, không trả Entity.
4. **API chuẩn**: mọi response bọc `ApiResponse<T>`; lỗi tập trung ở `@RestControllerAdvice`.
5. **Đặt tên**: Class/Interface/Enum/Record PascalCase · package chữ thường (`snake_case` khi cần) ·
   method/variable camelCase · constant SCREAMING_SNAKE_CASE + `static final` · bảng/cột DB
   snake_case · DTO có hậu tố `…Request` / `…Response` / `…Dto`.
6. **Commit & branch đúng chuẩn**: `<type>(<scope>): <mô tả>` và `loại-nhánh/tên-mo-ta`. Không commit
   trực tiếp vào `master`/`develop`. Không tự commit/push khi user không yêu cầu rõ ràng.
7. **Code cũ vi phạm quy tắc**: code mới tuân thủ 100%; code cũ chỉ dọn trong phạm vi đang sửa —
   không refactor hàng loạt, không mở rộng diff. Vi phạm diện rộng thì báo để mở ticket riêng.
