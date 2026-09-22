# Review — cell-app PR #149 «Feature/hoa don mua hang dich vu 1.0»

**Chế độ:** NHANH (chỉ đọc + kiểm tĩnh bằng git — KHÔNG chạy test/build, KHÔNG worktree, KHÔNG baseline)
**head** `1519cc4b` · **base** `origin/develop` = `ce79f419` · **merge-base** `ce79f419`
**Phạm vi:** 7 file · +520 −3 · không có migration · không có file test
**PYC đối chiếu:** `pmkt-docs/ba/PMKT-E-06758_ChungTuTraLaiHangMua/5.screens/SCR_TLHM_PopupChonChungTu.md` (BR1, BR2 — BR **nội bộ màn**)
**BR chung đã đọc:** BR1 (phân trang). **Chưa đọc:** BR7, BR8, BR18 (không có finding nào cần trích).

| Mức | Số | Mã |
|---|---|---|
| 🚫 Blocker | 2 | B1, B2 |
| ⚠️ Major | 5 | M1–M5 |
| 🔸 Minor | 3 | m1–m3 |
| 💬 Nit | 1 | n1 |

---

## 🚫 B1 — Phân trang 0-based, lệch giao ước `PageResponse` (1-based) → mất nguyên một trang

**File:** `src/main/java/vn/vtt/pmkt/cell/chung_tu_mua_hang/internal/adapter/ChungTuMuaHangNguonAdapter.java:403, 266, 290, 397`
**Nguồn:** `core/response/PageResponse.java:26` — *"Thông tin phân trang trả về FE (page **1-based** để hiển thị trực tiếp)"*; `PageResponse.ofList` dùng `(page - 1) * pageSize`; cùng repo `HoaDonMuaService:200` dùng `(pageOrDefault() - 1) * pageSize`.
**Trigger:** FE gửi `page = 1` (giá trị đầu tiên theo BR1/PageResponse).
**Actual / Expected:**

```java
private static int page(Integer value)  { return value == null || value < 0 ? 0 : value; }
...
query.setFirstResult(page * pageSize)          // page=1 → OFFSET 20
return pageResponse(..., page, pageSize, total) // trả pagination.page = 1
```

`OFFSET page * pageSize` (bỏ qua 20 bản ghi đầu) / phải là `(page - 1) * pageSize`.
**Hậu quả:** trang 1 của combobox và của lưới popup **mất 20 dòng đầu**; nếu FE gửi `page = 0` cho khớp thì `pagination.page = 0` lại sai giao ước hiển thị. Không có test nào bắt được vì bộ test rỗng (M3).

---

## 🚫 B2 — "Số lượng đã trả lại" không quy đổi ĐVT → số lượng còn trả được sai

**File:** `ChungTuMuaHangNguonAdapter.java:49–59` (`RETURNED_QUANTITY`)
**Nguồn:** `SCR_TLHM_PopupChonChungTu.md` BR2.1 — *"Trường hợp chứng từ trả lại có ĐVT khác với chứng từ mua hàng hóa, dịch vụ ⇒ **Quy đổi** SL trả lại theo ĐVT chính trên chứng từ trả lại theo ĐVT trên chứng từ mua hàng để xác định Số lượng trả lại cho đúng"* (kèm ví dụ Thùng/Hộp/Cái).
**Trigger:** mua 1 Thùng, lập TLHM trả 2 Cái (`pur_chung_tu_tra_lai_hang_mua_chi_tiet.don_vi_tinh_id` khác, `he_so_quy_doi` khác — hai cột này **có tồn tại**, xem `ChiTietTraLaiHangMua.java:30-31`).
**Actual / Expected:**

```sql
coalesce((select sum(r.so_luong) ...), 0)     -- cộng thô, bỏ qua r.he_so_quy_doi và d.he_so_quy_doi
```

phải quy đổi theo hệ số như BR2.1 trước khi cộng.
**Hậu quả:** `so_luong_con_lai` sai → người dùng trả lại vượt số đã mua (hoặc bị chặn oan), `don_gia`/`thanh_tien` theo BR2.3 (`thành tiền / số lượng`) sai theo. Sai lệch chỉ lộ ra lúc quyết toán.
*(Ghi chú: bản hiện hành `TraLaiHangMuaRepositoryImpl:80,131` cũng thiếu quy đổi — nhưng code MỚI phải tuân thủ 100%, và bản mới đang được viết để thay chỗ đó.)*

---

## ⚠️ M1 — 520 dòng API không có caller nào; đồng thời tồn tại bản hiện thực thứ hai đang chạy, hành vi lệch nhau

**File:** `api/ChungTuMuaHangNguonApi.java:20,23,26` · `internal/adapter/ChungTuMuaHangNguonAdapter.java:253,273,297`
**Nguồn:** CLAUDE.md §Cấu trúc module BE — *"CHỈ tạo `api/` khi module KHÁC thật sự cần gọi vào"*; luật 9 (một nguồn sự thật cho nghiệp vụ).
**Trigger:** `git grep -n "timChungTuConLaiTraLai\|timDongConLaiTraLai" <head> -- src` → chỉ khai báo + hiện thực, **0 caller**. Endpoint đang phục vụ FE vẫn là `TraLaiHangMuaController:122 GET /nguon` và `:133 GET /nguon/{id}` → `TraLaiHangMuaRepositoryImpl.timNguon/layNguon`.
**Actual / Expected:** hai hiện thực song song của cùng BR1/BR2, **đã lệch nhau**:

| | bản cũ (đang chạy) | bản mới (PR này) |
|---|---|---|
| sắp xếp | `ngay_hach_toan **desc**` | `asc` (đúng BR1) |
| keyword | số CT **hoặc** tên NCC | chỉ số CT |
| điều chỉnh giá | không đọc | có (`ADJUSTMENT_AMOUNT`) |
| lọc hình thức / loại nghiệp vụ | không | có |

**Hậu quả:** FE vẫn nhận dữ liệu của bản cũ (sai BR1 về sắp xếp), còn bản mới là code chết chờ phân rã; sửa BR2 sau này phải nhớ sửa hai chỗ. Cần hoặc đấu bản mới vào controller và **xóa** đường cũ trong cùng PR, hoặc tách PR.

## ⚠️ M2 — Chứng từ trả lại **chưa ghi sổ** vẫn bị trừ, trong khi điều chỉnh giá thì chỉ tính khi đã ghi sổ

**File:** `ChungTuMuaHangNguonAdapter.java:49` (`RETURNED_QUANTITY`), `:61` (`RETURNED_AMOUNT`) vs `:73` (`ADJUSTMENT_AMOUNT`)
**Nguồn:** BR2 không quy định trạng thái của phiếu trả lại/điều chỉnh dùng để trừ → **tài liệu im lặng**, luật 9 + Cổng đặc tả §2: mở mục `OPEN` và hỏi BA, không tự chọn.
**Trigger:** một chứng từ TLHM nháp (`CHUA_GHI_SO`) trên cùng dòng hàng.
**Actual / Expected:**

```sql
-- trả lại: KHÔNG lọc trạng thái
and h.da_xoa = false and (cast(:traLaiHangMuaId as uuid) is null or h.id <> :traLaiHangMuaId)
-- điều chỉnh giá: CÓ lọc
and dc.trang_thai_chung_tu = 'DA_GHI_SO'
```

**Hậu quả:** hai công thức trong cùng một biểu thức áp hai chuẩn khác nhau; một phiếu nháp của người khác làm giảm số lượng có thể trả, không nhất quán với cách xử lý điều chỉnh giá. Phải để BA chốt rồi mới code.

## ⚠️ M3 — Không một test nào cho ~500 dòng công thức nghiệp vụ

**File:** diff không chạm `src/test/**` (`git diff --name-only … | grep -c src/test` → `0`)
**Nguồn:** CLAUDE.md §Truy vết — luật hiện thực xong phải để lại mã luật trong tên test; `bon-lop.md` Lớp C.
**Trigger:** BR2 có 4 nhánh công thức (checkbox false / true / dòng dịch vụ SL=ĐG=0 override / quy đổi ĐVT) + BR1 có 5 điều kiện load.
**Hậu quả:** B1, B2 và mọi lệch công thức sau này không có gì bắt; `./gradlew unitTest` xanh không nói gì về đúng/sai nghiệp vụ.

## ⚠️ M4 — Hardcode chuỗi enum và số phân trang, trong khi enum đã có sẵn

**File:** `ChungTuMuaHangNguonAdapter.java:89–92` (`PURCHASE_SOURCE_TYPES`), và lặp lại nguyên chuỗi `('DichVu','MuaDichVu','DichVuChiPhi','MuaDichVuChiPhi')` **8 lần** inline ở `:97, 110, 140, 151, 172, 181, 190, 379`; `:407` (`20`, `200`); `:307, 333, 351` (`'TrongNuoc','MuaHangTrongNuoc'`).
**Nguồn:** 9 luật §1 (không hardcode magic value, constant có tên đặt gần nơi dùng); lỗi hay gặp #7. Enum chính tắc đã có: `internal/model/LoaiNghiepVuMuaHang.java` (`maDb()` + `biDanh()`), `internal/model/HinhThucMuaHang.java`.
**Actual / Expected:** chuỗi DB rải rác trong SQL / phải sinh từ enum (hoặc ít nhất một constant duy nhất trong `internal/constant`). `20` là mặc định của **BR1** ("mặc định 20 bản ghi/trang") nên càng phải là hằng số có tên, không phải số trần trong `pageSize()`.
**Hậu quả:** thêm một biến thể `loai_nghiep_vu` là phải sửa 9 chỗ; `'MuaHangTrongNuoc'` **không tồn tại** trong `HinhThucMuaHang` (enum chỉ có `TrongNuoc`/`NhapKhau`) — chuỗi tự nghĩ ra, không ai bắt được vì SQL native không kiểm kiểu.

## ⚠️ M5 — 11 truy vấn tương quan trên mỗi dòng kết quả; combobox không bắt buộc lọc

**File:** `ChungTuMuaHangNguonAdapter.java:136–199` (`LINE_SELECT` nội suy `RETURNED_QUANTITY` ×3, `AFTER_RETURN_AMOUNT` ×5 — mỗi cái là một subquery `sum()` có `join`), cộng `SO_HOA_DON` (`string_agg` + `exists`) và `RETURNABLE_LINE` trong `WHERE`.
**Nguồn:** lỗi hay gặp #4 (code chưa tối ưu).
**Trigger:** `timChungTuConLaiTraLai` **không** bắt buộc `nhaCungCapId`/khoảng ngày (khác `timDongConLaiTraLai:278` có chặn) → combobox quét toàn bộ chứng từ đã ghi sổ của tenant, mỗi dòng chạy lại toàn bộ khối subquery, và chạy **hai lần** (count + data).
**Actual / Expected:** nội suy lặp / tính một lần trong `LATERAL` (hoặc CTE) rồi tham chiếu lại.
**Hậu quả:** tenant nhiều chứng từ → combobox "Chọn chứng từ gốc" chậm tuyến tính theo tổng số chứng từ, không theo 20 dòng cần trả. *(BR1 mục 2 chỉ yêu cầu combobox load toàn bộ NCC — không yêu cầu bỏ mọi bộ lọc thời gian.)*

---

## 🔸 m1 — `@PersistenceContext` chồng lên constructor injection, field mất `final`

`ChungTuMuaHangNguonAdapter.java:221–222` thêm `@PersistenceContext private EntityManager em;` nhưng constructor `:246–249` vẫn nhận và gán `em`. Spring gán constructor trước, rồi field injection **ghi đè**. Hệ quả: một trong hai đường là thừa, field không còn bất biến, và `@RequiredArgsConstructor`/constructor injection theo §Quy ước đặt tên bị phá lệ. Bỏ một trong hai.

## 🔸 m2 — `thu_tu` NULL làm `mapLine` ném NPE

`ChungTuMuaHangNguonAdapter.java:426` `row.get("thu_tu", Integer.class)` đổ vào `DongMuaConLai.thuTu` kiểu **`int`** (`api/dto/DongMuaConLai.java:11`). Cột khai `@Column(name = "thu_tu")` **không** `nullable = false` (`core/entity/BaseChiTietChungTuEntity.java:33-34`, `Integer`). Dòng chi tiết cũ có `thu_tu` NULL ⇒ NPE lúc unboxing, 500 trên toàn popup. Dùng `Integer` hoặc `coalesce(d.thu_tu, 0)`.

## 🔸 m3 — Tham số chết

`headerWhere(filter, onlyReturnable)` (`:328`) và `bindFilter(query, filter, withReturnId)` (`:385`) chỉ từng được gọi với `true` (`:258, 260, 265, 283, 288, 319`). Cờ không bao giờ `false` ⇒ nhánh `if` không có đường chạy — bỏ tham số hoặc bỏ nhánh.

---

## 💬 n1 — Commit message không theo chuẩn

`git log` trên nhánh: `update api tim kiem hoa don` (×2), `update api tich hop cho tra lai hang mua` (×2), `fix api nguon chi phi` (×2), `hoa don mua hang dich vu va tich hop cho truong`. Chuẩn (9 luật §8): `<type>(<scope>): <mô tả>`, ví dụ `feat(tra-lai-hang-mua): api tìm chứng từ gốc còn trả được`. Sáu commit trùng nội dung + 5 merge develop ⇒ nên squash trước khi merge.

---

## Ngoài phạm vi trên — thay đổi `HoaDonMuaService` cần nói riêng

**⚠️ (tính vào M-list là M6 nếu BA không xác nhận)** `hoa_don_mua/internal/service/HoaDonMuaService.java:182-183`

```sql
coalesce(hd.chung_tu_nhan_hoa_don_id, hd.chung_tu_mua_hang_id) as chung_tu_nhan_hoa_don_id
```

Giá trị này chảy thẳng vào `HoaDonMuaRow.chungTuNhanHoaDonId` (`HoaDonMuaModels.java:52`) rồi vào
`ChungTuNhanHoaDonDto.chungTuNhanHoaDonId` (`HoaDonMuaCrudService.java:181`). Sau thay đổi, trường
mang tên "id chứng từ nhận hóa đơn" có thể chứa **id của chứng từ mua hàng** — hai bảng khác nhau
(`pur_chung_tu_nhan_hoa_don` vs `pur_chung_tu_mua_hang`). Mọi consumer điều hướng/tra cứu theo id
này (ví dụ `CongNoHoaDonMuaService.kiemTraTruocKhiGo(chungTuNhanHoaDonId, …)`) sẽ tra nhầm bảng.
Cùng file, `:309` và `:1304` vẫn trả `hd.chung_tu_nhan_hoa_don_id` **thô** ⇒ ba đường đọc cùng một
trường cho hai giá trị khác nhau. Nếu ý đồ là "chứng từ gốc để mở từ lưới" thì phải là **trường
mới** có tên đúng, không mượn tên cũ. Không có test và không thấy nguồn spec cho thay đổi này.

---

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ⚠ Hardcode magic value (M4). Không secret, không `any`, response chưa lộ Entity (chưa có controller), phân tầng OK (adapter chỉ-đọc). Nghiệp vụ tự bịa: `'MuaHangTrongNuoc'` không có trong enum (M4); trạng thái phiếu trả lại tự quyết (M2). |
| B — Kiến trúc & 7 lỗi | xem bảng dưới |
| C — Nghiệp vụ & truy vết | ⚠ BR2.1 MISSING (B2); BR2.2/2.3/2.4, BR1 (điều kiện load, sắp xếp) đối chiếu **đạt**. `trace.sh`/`msg.sh` `NOT-RUN` — chưa có `docs/doing/*-tra-lai-hang-mua-spec/`, không đoán bừa PYC. |
| D — Vệ sinh diff & Git | ⚠ n1 (commit message); cây commit sạch (`git status --porcelain` rỗng); không có TODO/code debug; không rename. |

## Bảy lỗi hay gặp

| # | Mục | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ⚠ `api/` mở rộng nhưng **không module nào gọi** (M1). `package-info.java` + `@NamedInterface("dto")` đã có ✅. |
| 2 | Version migration | ✅ N/A — diff không có file `db/migration`. |
| 3 | Chưa test lại sau merge | ✅ N/A — `git rev-list --count ce79f419..origin/develop` = **0** (nhánh đích không đi trước), 0 file giao nhau. |
| 4 | N+1 / chưa tối ưu | ⚠ M5. |
| 5 | Chưa tận dụng BaseController/BaseEntity | ⚠ tự viết phân trang + count native thay vì `@Searchable`/`SearchExecutor`/`PageResponse.of` (dẫn tới B1). Không phải CRUD nên không cần `BaseCrudController`. |
| 6 | Chưa tận dụng base FE | ✅ N/A — PR không chạm `client/`. |
| 7 | Constant đặt sai chỗ | ⚠ M4 — chuỗi DB và số phân trang nằm trong SQL của adapter, không ở `internal/constant`, dù enum chính tắc đã có ở `internal/model`. |

## Cổng đã chạy

| Cổng | Kết quả |
|---|---|
| `git status --porcelain` | sạch |
| `git rev-list --count <merge-base>..origin/develop` | 0 |
| `comm -12` file giao nhau với develop | 0 file |
| quét trùng số migration mọi remote branch | N/A — diff không có migration |
| `git grep` caller của API mới | 0 caller → M1 |
| `trace.sh` / `msg.sh` | `NOT-RUN` — chưa có thư mục spec cho PMKT-E-06758 |
| `./gradlew unitTest` | `NOT-RUN` — chế độ nhanh |

**Chưa đọc / chưa kiểm:** BR chung 7, 8, 18; các file `4.usecases/**` và `6.messages.md` của PYC;
`ChungTuMuaHangNguonAdapter` phần cũ (`layNguonDieuChinhGia`, `dongNguonKhaDung`) ngoài diff.

---

## Kết luận: 🔴 **REJECT** — B1, B2 (Blocker); M1–M5 (+ mục `HoaDonMuaService`) cần xử lý trước khi merge

Cổng test/build **chưa chạy** (chế độ nhanh). Kết luận này dựa trên đọc mã + kiểm tĩnh bằng git,
không thay cho `./gradlew unitTest`.
