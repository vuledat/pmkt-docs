# BE — Khung kiến trúc chuẩn cho một phiếu yêu cầu

Bản trích từ `cell-app/src/main/java/vn/vtt/pmkt/cell/` (đo ngày 2026-08-11). Đây là **khung bắt
buộc**: mọi phiếu yêu cầu (module / API / bảng mới) làm ở backend phải sinh ra đúng bộ artefact dưới
đây, đúng vị trí, đúng tên. Không có ngoại lệ cho "API nhỏ".

**Module tham chiếu:**

| Loại việc | Đọc module này |
|---|---|
| Chứng từ kế toán (thêm/sửa/xoá/ghi sổ) | `cell/chung_tu_ban_hang/` |
| Kernel / engine dùng chung nhiều module | `cell/accounting_core/` |
| CRUD + phân quyền | `cell/platform_iam/quyen/`, `cell/platform_iam/nguoi_dung/` |
| Outbox / inbox / gọi hệ thống ngoài | `cell/integration_ops/` |

SSOT chi tiết: [cell-app/CLAUDE.md](../../cell-app/CLAUDE.md) · [docs/conventions.md §3](conventions.md) ·
song song với bản FE: [docs/fe-khung-kien-truc-chuan.md](fe-khung-kien-truc-chuan.md).

---

## 1. Bản đồ dịch vụ — biết mình được viết ở đâu

| Dịch vụ | Vai trò | Kiến trúc |
|---|---|---|
| **`../../cell-app`** | nghiệp vụ kế toán (nơi ~90% phiếu yêu cầu đáp xuống) | **Spring Modulith** — §2 |
| `../../cell-gateway` · `../../front-door` | định tuyến, cửa vào | phẳng `controller/ service/ …`, xem CLAUDE.md của module |
| `../../identity` | xác thực | như trên |
| `../../integration-platform` | tích hợp ngoài, có migration riêng | như trên |
| `../../tenant-provisioning` | control-plane, cấp phát tenant | chia theo bounded context (`controlplane/<ctx>/`) |
| `../../shared-kernel` | thư viện dùng chung | như trên |

Base package chung: `vn.vtt.pmkt`. Stack: Java 21 · Spring Boot · Gradle Kotlin DSL.

**Tài liệu này mô tả chuẩn của `cell-app`.** Dịch vụ khác giữ shape riêng đã có; trước khi sửa phải
đọc `../../CLAUDE.md` trong đúng thư mục đó (luật cộng dồn — xem CLAUDE.md gốc).

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

**Test đặt song ánh cây `main`** — `…/<module>/internal/service/` ở `main` thì test ở
`src/test/java/…/<module>/internal/service/`. Test thuần JVM gắn `@Tag("unit")`.

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

Controller không chứa business logic, không gọi Repository, không trả Entity ra ngoài. Mọi response
bọc `ApiResponse<T>`; lỗi xử lý tập trung bằng `@RestControllerAdvice`. DI bằng constructor injection
(`private final` + `@RequiredArgsConstructor`).

📄 Chi tiết từng tầng, chuẩn API, DI, JPA: [`conventions-be.md` §3.2–3.6](conventions-be.md).

---

## 5. Bộ artefact tối thiểu của một phiếu — checklist sinh file

| # | Artefact | Đường dẫn | Bắt buộc |
|---|---|---|---|
| 1 | Khai báo module | `cell/<module>/package-info.java` (`@ApplicationModule`) | ✅ |
| 2 | Migration schema | `cell-app/src/main/resources/db/migration/V<yyyyMMddHHmmss>__<prefix>_<mô_tả>.sql` | ✅ nếu có bảng |
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

**Migration:** `V<yyyyMMddHHmmss>__<prefix>_<mô_tả_snake_case>.sql` — version là **timestamp lúc tạo
file**, lấy bằng `date +V%Y%m%d%H%M%S`, KHÔNG đếm `max + 1`. Hai nhánh song song vì thế không bao giờ
đẻ ra hai file trùng version. File đã merge giữ nguyên tên cũ — không đổi, không sửa; sửa schema thì
thêm file mới. Chi tiết: [migration-danh-so-theo-timestamp.md](migration-danh-so-theo-timestamp.md).

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

## 7. Cổng nghiệm thu (DoD)

```bash
cd cell-app && ./gradlew unitTest     # CỔNG CHÍNH — chỉ @Tag("unit"), ~1 phút, KHÔNG cần Docker
```

🚫 **KHÔNG `./gradlew build`.** Nó kéo ~25 test Testcontainers và bắt buộc có Docker — thứ đã bị cấm
ở [`CLAUDE.md` §CHẠY CODE](../../CLAUDE.md). Mục này trước đây ghi `./gradlew build` là cổng DoD;
**đó là bản cũ đã sai**, giữ lại ghi chú này để không ai chép lại.

⚠ `cell-app/` là Gradle project ĐỘC LẬP; `./gradlew :cell-app:build` ở gốc repo luôn báo "no such file
or directory".

📄 Cách kiểm ranh giới Modulith (vì sao `ApplicationModules.verify()` không chạy trần được, mẫu
`ProxyModularityTest`), và cổng đầy đủ: [`cell-app/CLAUDE.md`](../../cell-app/CLAUDE.md).

Luật nghiệm thu: (1) không làm xấu hơn baseline; (2) **module mới phải sạch tuyệt đối** về ranh giới
Modulith — không mang nợ ngay từ ngày đầu; (3) lệnh fail thì **dán output thật**; (4) báo cáo phải
**liệt kê BR đã áp dụng** và BR chưa đạt.

---

## 8. Vùng cấm & shape đóng băng

| Vùng | Luật |
|---|---|
| **`cell/master_data/**` — VÙNG ĐÓNG BĂNG** | ✗ **Không đọc** để tham khảo (grep rơi vào đây thì bỏ qua, không trích làm bằng chứng cho quy ước hiện hành) · ✗ **Không sao chép** kiến trúc / cách chia package / cách đặt tên / pattern · ✗ **Không dùng làm mẫu** cho module mới, kể cả module danh mục. Chặn cứng ở `../../.claude/settings.json` (`permissions.deny` cho tool `Read`) |
| `master_data` khi ĐÃ được cho phép | Chỉ đọc **đúng** chữ ký cần dùng (`master_data.*.dto`, `master_data.*.service`, `TenantProvisioner`), không mang kiến trúc sang, **báo rõ cho user** là đang chạm vùng đóng băng, và **xin phép** gỡ tạm rule deny |
| **Shape phẳng không có `internal/`** | `controller/ dto/ entity/ repository/ service/` nằm thẳng ở gốc module. Nợ còn lại: `platform_iam/rbac_console/`, `common/mau_excel/`, `common/ui_config/`. **Không mở module mới theo shape này** |
| `../../client/src/legacy` | Vùng khoá của FE — xem [fe-khung-kien-truc-chuan.md §10](fe-khung-kien-truc-chuan.md) |

**Nợ hiện tại (đo 2026-08-11):** 96 vi phạm ranh giới Modulith · 3 sub-module còn shape phẳng ·
`master_data` chưa chuyển.

Luật áp **từ nay về sau**: module mới đủ chuẩn; module cũ chuyển dần khi có việc chạm vào. Không mở
đợt refactor toàn bộ nếu không được giao.

---

## 9. BR và luật cứng — KHÔNG lặp lại ở đây

Hai mục này từng được chép lại trong file này và đã bắt đầu lệch (bảng BR ở đây còn thiếu BR35 và
BR47–49). Đọc thẳng bản gốc:

| Cần gì | Bản gốc (SSOT) |
|---|---|
| Bảng tra BR + cách trích | [`CLAUDE.md` §BR](../../CLAUDE.md) → `./docs/rules/br.sh <số BR>` |
| Luật cứng toàn repo (gồm phân trang — [phan-trang.md](phan-trang.md)) | [`CLAUDE.md`](../../CLAUDE.md) |
| Quy ước Java (đặt tên, API, DI, JPA) | [`conventions-be.md`](conventions-be.md) |
| Quy tắc chung + Git + checklist commit | [`conventions-chung.md`](conventions-chung.md) |
| Cổng chạy, tiền tố bảng, Modulith | [`cell-app/CLAUDE.md`](../../cell-app/CLAUDE.md) |

Riêng của phiếu BE: báo cáo hoàn thành phải **liệt kê BR đã áp dụng** và BR chưa đạt (kèm lý do).
