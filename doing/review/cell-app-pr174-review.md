# Review — cell-app PR #174 "Feat/bang ke mua vao"

**Chế độ:** NHANH (đọc + kiểm tĩnh bằng git; **không** chạy test/build, không worktree, không baseline, không merge thử)
**PR:** https://github.com/ospgroupvn-pmkt/cell-app/pull/174 · tác giả `hotuanhai` · state OPEN · `mergeable: MERGEABLE`
**head** `fe2991c29ad7f5c7257ac575265c9181f6ef09e2` (`feat/bang-ke-mua-vao`)
**base** `origin/develop` = `14b838425ed043ad693035772b037dff77d44e9c` · **merge-base** `f36241558c5dd509c7b8cea7d2dc5f3c58801cb6`
**Phạm vi:** 215 file · +14.051 −3 · 9 commit · epic **PMKT-E-10978** (Tờ khai thuế GTGT 01/GTGT)
**Working tree local:** có 1 file untracked `V1133__ccdc_ghi_giam_chi_tiet_bo_sung_chi_nhanh_id.sql` — thuộc cây làm việc của user trên `develop`, **không** thuộc PR này.

---

## Kết luận

🔴 **REJECT** — 1 Blocker (B1: trùng số 4 migration với `develop`, Flyway vỡ ngay khi merge).

| Mức | Số | Mã |
|---|---|---|
| 🚫 Blocker | 1 | B1 |
| ⚠️ Major | 3 | M1, M2, M3 |
| 🔸 Minor | 2 | m1, m2 |
| 💬 Nit | 3 | n1, n2, n3 |

Chế độ nhanh: cổng `unitTest` / `build` **chưa chạy**. Không dùng báo cáo này để APPROVE.

---

## Findings

### 🚫 B1 — Bốn migration V1129–V1132 trùng số với migration đã merge vào `develop`

**File:** `src/main/resources/db/migration/V1129__tax_khoi_tao_to_khai.sql` · `V1130__tax_to_khai_thue_01_gtgt.sql` · `V1131__tax_bang_ke_ban_ra_mua_vao.sql` · `V1132__tax_dinh_kem_phu_luc.sql`
**Nguồn:** CLAUDE.md §Trước khi báo hoàn thành · bảy lỗi #2 "Không đánh lại version migration"

**Trigger**

```
$ git ls-tree -r --name-only origin/develop src/main/resources/db/migration | sort -V | tail -6
V1129__ref_ctct_them_loai_chu_kho.sql
V1130__acc_so_kho_bo_sung_cot_chung_tu_kho.sql
V1131__pur_doi_namespace_quyen_dieu_chinh_gia_hang_mua.sql
V1132__sal_hdbh_tai_khoan_ngan_hang_thu_chu_tu_do.sql
V1133__ccdc_ghi_giam_chi_tiet_bo_sung_chi_nhanh_id.sql
V1134__cap_nhat_mo_ta_thong_tu.sql
```

**Actual / Expected:** PR mang V1129, V1130, V1131, V1132 — **cả bốn số đều đã bị `develop` chiếm**, và max của `develop` đã là **V1134** / mỗi migration một số lớn hơn max nhánh đích, tức bắt đầu từ **V1135**.

**Cơ chế:** tại merge-base max chỉ là **V1119**, nên commit `c443c3bd feat(db): update migrations numbers` đánh lại số là đúng **tại thời điểm đó**; `develop` sau đó đi thêm **20 commit** và chiếm V1129–V1134. Merge xong, thư mục `db/migration` có hai file cùng version → Flyway ném `FlywayException: Found more than one migration with version 1129` ngay lúc khởi động, **service không lên được**. Không phải checksum mismatch — là lỗi chặn boot.

**Hậu quả:** deploy đỏ 100%. Cần đánh lại thành V1135–V1138 (và kiểm lại ngay trước khi merge, vì `develop` vẫn đang chạy).

**Lưu ý kèm:** hai nhánh khác cũng đang giành V1133/V1134 với `develop` (`feat/cn-720-lap-bao-cao-tai-chinh`, `feat/tai-khoan-theo-vai-tro`, `bugfix/httk-gop-tang-dung-chung`) — ngoài phạm vi PR này nhưng nên báo để nhóm xử lý chung.

---

### ⚠️ M1 — Mã tính chất thuế lạ được **cộng vào chỉ tiêu [25]** (thuế GTGT được khấu trừ) thay vì bị loại

**File:** `src/main/java/vn/vtt/pmkt/cell/thue/to_khai_gtgt/internal/service/business/TongHopChiTieuMuaVao.java:51-55`
**Nguồn:** BR04 SCR_BangKeMuaVao (javadoc chính file này: "[25] = Σ [7] tính chất 1, 2, 3 — KHÔNG cộng tính chất 4")

```java
private static boolean vaoChiTieu25(String maTinhChat) {
    return TinhChatThueMuaVao.theoMa(maTinhChat)
            .map(TinhChatThueMuaVao::vaoChiTieu25)
            .orElse(true);          // <- mã không nhận ra ⇒ VẪN cộng vào [25]
}
```

**Trigger:** `POST /api/thue/to-khai-gtgt/mua-vao/tong-hop` với một phần tử `dongDangGiu[]` mang `tinhChatThue` ngoài `"1".."4"` (ví dụ `null`, `"04"`, `"9"`).

**Chuỗi không có chốt chặn nào:**

1. `internal/dto/BangKeMuaVaoDongLuuRequest.java:8` khai `String tinhChatThue` — record **không có bean validation nào**, không `@NotNull`, không `@Pattern`. `@Valid` ở controller vì thế không kiểm gì.
2. `business/MapBangKeMuaVaoLuu.java:33` gán thẳng: `b.setTinhChatThue(d.tinhChatThue());`
3. `business/ValidateThanBangKeMuaVao.java:26-51` kiểm số hóa đơn, ngày, tên người bán, MST, ngày vượt kỳ — **không hề kiểm `tinhChatThue`**.
4. `TongHopChiTieuMuaVao.tinh` cộng tiền thuế của dòng đó vào `[25]`.

**Actual / Expected:** mã lạ ⇒ thuế của dòng **được** tính là khấu trừ được / mã lạ phải bị từ chối, hoặc chí ít **không** cộng vào [25].

**Hậu quả:** đường compute (`tongHopThu`, `tongHopThuLamMoi`, `seedThuPhuLuc`) đều `@Transactional(readOnly = true)` — **không chạm DB**, nên CHECK constraint `tinh_chat_thue IN ('1','2','3','4')` của `V1131` không đỡ được: API trả về chỉ tiêu [25] **cao hơn thực tế, im lặng, không lỗi**. [25] là số thuế GTGT được khấu trừ kỳ này — sai theo hướng có lợi cho người nộp thuế, loại sai chỉ lộ ra khi quyết toán. Ở đường Lưu (`ghiThanTuPayload`) CHECK constraint có bắt, nhưng bắt lúc flush ⇒ vỡ transaction thành lỗi hạ tầng chứ không phải lỗi nghiệp vụ có mã.

**Bằng chứng đây là lệch chuẩn nội bộ, không phải chủ ý:** lớp anh em ngay cạnh fail **closed** cho đúng tình huống này —

```java
// PhanNhomTinhChatThueMuaVao.java:10-16
if (maNhomHhdvMuaVao == null || !TinhChatThueMuaVao.NHOM_HHDV_TONG_HOP.contains(maNhomHhdvMuaVao)) {
    return Optional.empty();
}
```

`orElse(true)` là chỗ **duy nhất** trong cả module `to_khai_gtgt` (`git grep -n "orElse(true)"` → 1 kết quả).

**Test:** `TongHopChiTieuMuaVaoTest` có `nhom3_vaoChiTieu25`, `nhom4_khongVaoChiTieu25_nhungVao23_24`, `nhapKhau_vao23a_24a` — **không có** case mã lạ/null. Nhánh `.orElse(true)` chưa từng được chạy trong test.

---

### ⚠️ M2 — 40 chỗ ném `ApiException` dùng **mã lỗi literal**, module thiếu lớp hằng số `MaLoi*`

**File:** toàn module `internal/service/**` — ví dụ `ChonHoaDonMuaVaoService.java:116,304,312,320,482` · `LuuToKhaiService.java:148,154,194,198,203,206,231,236,249` · `ChonHoaDonBanRaService.java:99,199,223,229,237` · `PhuLucService.java:158`
**Nguồn:** CLAUDE.md §9 luật — luật 1 "Không hardcode magic value — mọi số/chuỗi nghiệp vụ phải là constant có tên" · bảy lỗi #7 "Constant đặt sai chỗ"

**Trigger**

```
$ git grep -ohE 'ApiException(\.(badRequest|notFound|conflict))?\("[A-Z_0-9]+"' <head> -- .../thue/to_khai_gtgt \
    | grep -oE '"[A-Z_0-9]+"' | sort | uniq -c | sort -rn
  16 "NOT_FOUND"       3 "VALIDATION_ERROR"    2 "TU_NGAY_KHONG_HOP_LE"   2 "TINH_CHAT_3_KHONG_SUA"
   2 "THIEU_KHOI_TAO"  2 "STALE_DATA"          2 "PHU_LUC_KHONG_DINH_KEM" 2 "PHU_LUC_KHONG_AP_DUNG"
   2 "KHONG_TIM_THAY_SO_SANH"  ...            (16 mã distinct / 40 lượt ném)
```

**Actual / Expected:** mã lỗi rải rác dạng chuỗi trần trong thân service / chuẩn repo là một lớp hằng số cạnh module — `git ls-tree origin/develop` cho thấy **10+ module** đã có: `MaLoiChungTu`, `MaLoiHachToan`, `MaLoiDanhSo`, `MaLoiKhoaSo`, `MaLoiBanHang`, `MaLoiDieuChinhGia`, `MaLoiHoaDonBanHang`, `MaLoiTraLaiHangBan`, `MaLoiKhaiBaoCptt`…

**Cụ thể hơn:** module **đã** làm đúng việc này cho mã thông báo (`internal/model/MaThongBaoToKhai.java`, 58 hằng số, rất tốt) nhưng **không** làm cho mã lỗi; `internal/` cũng không có thư mục `constant(s)/`. Ba mã `"TU_NGAY_KHONG_HOP_LE"`, `"THIEU_KHOI_TAO"`, `"PHU_LUC_KHONG_DINH_KEM"` bị gõ lặp ở hai file khác nhau — đúng kiểu lỗi mà hằng số sinh ra để chặn.

**Hậu quả:** FE bắt lỗi theo chuỗi gõ tay ở hai phía; đổi hoặc gõ sai một mã không có gì phát hiện (không compile-break, không test đỏ).

---

### ⚠️ M3 — Nhánh tụt 20 commit so với `develop`, chưa test lại sau merge

**Nguồn:** bảy lỗi #3

**Trigger (đo bằng git, không chạy test)**

```
$ git rev-list --count <merge-base>..origin/develop
20
$ comm -12 <(git diff --name-only <mb> origin/develop|sort) <(git diff --name-only <mb> <head>|sort)
src/test/java/vn/vtt/pmkt/cell/arch/ProxyModularityTest.java
```

**Actual / Expected:** 1 file giao nhau / 0.

**Đánh giá đúng mức:** bản thân file giao nhau này **lành** — hai bên sửa hai hunk rời nhau (`develop` đổi tên `giaThanhKhongCoViPhamRanhGioiNao` → `cauHinhGiaThanh…` rồi thêm method mới ở dòng ~98; PR thêm `seamBangKeMuaVaoPha2KhongCoViPhamRanhGioiNao` ở dòng ~138), merge văn bản sạch, GitHub báo `MERGEABLE`.

**Hậu quả thật nằm chỗ khác:** `comm -12` **không** bắt được B1, vì migration của hai bên khác **tên file** dù trùng **số version**. Đây chính là cái bẫy của phép đo #3 — nhánh tụt 20 commit là tín hiệu, và hệ quả cụ thể là B1. Sau khi rebase/merge `develop` và đánh lại số migration, phải chạy lại `./gradlew unitTest` trên cây đã merge (lượt review này chế độ nhanh nên chưa chạy).

---

### 🔸 m1 — ~20 thông báo người dùng thấy được truyền `messageId = null`, nội dung không có trong catalog BA

**File:** `ChonHoaDonMuaVaoService.java:116-118,304-305,312-313,320-321` · `LuuToKhaiService.java:194-249` · `ChonHoaDonBanRaService.java:99,223,229` · `DanhSachToKhaiController.java:72-74`

```java
throw ApiException.badRequest("TU_NGAY_KHONG_HOP_LE", null,
        "Từ ngày phải lớn hơn ngày cuối cùng của kỳ kê khai. Vui lòng lựa chọn lại.");
```

**Trigger:** `grep -n "Từ ngày" pmkt-docs/ba/PMKT-E-10978_ToKhaiThueGTGT/6.messages.md` → **không có kết quả**.

**Actual / Expected:** chuỗi tiếng Việt hiển thị cho user, `messageId = null`, không có mã `MSG_PMKT-E-10978_nnn` / mọi text người dùng thấy phải mang mã để FE i18n và để `msg.sh` truy vết được.

**Hạ mức xuống Minor vì:** đây là nếp có sẵn của repo, không phải cái PR này đẻ ra — trên `develop` 71/441 lượt `ApiException.badRequest` cũng truyền `null`. Nêu ở đây vì module này **có** catalog message BA đầy đủ và đã dùng rất tốt ở chỗ khác, nên khoảng trống này lệch với chính nó.

---

### 🔸 m2 — Hai mã thông báo `_222` / `_223` do dev tự cấp, chưa có trong `6.messages.md`

**File:** `internal/model/MaThongBaoToKhai.java:85-90`

```java
// ---- ĐỀ XUẤT (chưa có trong 6.messages.md — chờ BA) --------------------------------
public static final String CHUA_THIET_LAP_THONG_TIN_THUE = "MSG_PMKT-E-10978_222";   // Q_F01-3
public static final String TRANG_THAI_CHUYEN_KHONG_HOP_LE = "MSG_PMKT-E-10978_223";  // Q_F03-2
```

**Nguồn:** CLAUDE.md §Cổng đặc tả luật 2 "Không tự đặt luật mới… mở mục OPEN và hỏi"

**Actual / Expected:** dev tự cấp số tiếp theo sau `_221` (mã cuối BA cấp) / BA cấp mã.
**Hậu quả:** nếu BA cấp `_222` cho việc khác, hai bên đụng mã và FE map nhầm thông báo.
**Ghi nhận công bằng:** tác giả **đã** đánh dấu rõ `// ĐỀ XUẤT`, trỏ đúng câu hỏi treo `Q_F01-3` / `Q_F03-2`. Đây là khai báo minh bạch, không phải giấu — chỉ cần BA chốt trước khi merge.

---

### 💬 n1 — Javadoc gắn nhầm vào hằng số thay vì method

**File:** `so_du_ban_dau/so_du_tai_khoan/internal/repository/TongHopSoDuTaiKhoanRepository.java:320-345`

Khối javadoc mô tả `tongDuNoTheoSoTaiKhoan(...)` (BA chốt 2026-09-03, "khớp chính xác, KHÔNG `LIKE '133%'`") nhưng đặt trên `private static final String TONG_DU_NO_THEO_SO_TAI_KHOAN`. Nội dung rất giá trị mà không xuất hiện ở javadoc của method public. Chuyển khối javadoc xuống ngay trên `public BigDecimal tongDuNoTheoSoTaiKhoan`.

### 💬 n2 — Commit message lệch chuẩn

`fe2991c2 Fix: resolve comments` — chuẩn là `<type>(<scope>): <mô tả>`, type viết thường + có scope (vd `fix(to-khai-gtgt): …`). `9e343ff7 fix: resolve merge conflicts` thiếu scope. Nhánh `feat/bang-ke-mua-vao` đúng chuẩn.

### 💬 n3 — PR 215 file / +14.051 dòng

Tiêu đề "bang ke mua vao" nhưng nội dung là **cả module** `thue/to_khai_gtgt` (5 controller, 6 entity, 4 migration, 47 DTO, 40 business class, 40 test) + 7 seam `api/` mở sang 7 module khác. Không phải trộn `feat` + `refactor` (diff gần như thuần thêm mới: −3 dòng), nhưng quá khổ cho một lượt review người. Lần sau nên tách theo feature (F01 khung tờ khai → F04b bán ra → F05 mua vào → F11 phụ lục).

---

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| **A — Cổng cứng** | ⚠️ Vi phạm luật 1 (hardcode mã lỗi → **M2**). Không secret, không debug code, không `TODO` mới, không chạm vùng đóng băng. BE: controller package-private, mọi response bọc `ApiResponse<T>`, không controller nào gọi Repository, không Entity lộ ra controller, không nuốt exception (4 `catch` đều có xử lý và có javadoc lý do). "Nghiệp vụ tự bịa": 2 mã message tự cấp (**m2**) — đã khai báo minh bạch. |
| **B — Kiến trúc & 7 lỗi** | 1 Blocker (#2), 2 Major (#3, #7) — bảng dưới. |
| **C — Nghiệp vụ & truy vết** | Không có `docs/doing/*-spec/` cho PMKT-E-10978 ⇒ `trace.sh` `NOT-RUN`. `msg.sh` xem bảng cổng. Không có `01-conflict.md` nên không có mục P0/P1 `OPEN` chặn — nhưng cũng nghĩa là **cổng đặc tả chưa từng chạy cho epic này** (`/audit-spec` chưa chạy), nên không chấm được độ phủ luật `R-…`. |
| **D — Vệ sinh diff & Git** | Cổng cây commit ✅ (PR đã push, không file `??` trong `src/` của PR; file untracked duy nhất ở máy local thuộc `develop`). Commit message lệch nhẹ (**n2**), PR quá khổ (**n3**). Không rename bằng `mv` trần. |

## Bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục (BE) | ✅ Đạt. `thue/to_khai_gtgt/` có `package-info.java`, mọi thứ nằm dưới `internal/{controller,dto,entity,model,repository,service}`, business tách `service/business/` + `service/nguon/`, không file phẳng ra gốc module. 7 `api/` mới **đều** có `@NamedInterface` và **đều có consumer thật** (kiểm từng cái: 2–3 consumer ngoài `api/`) — không có `api/` "cho chắc". |
| 2 | Không đánh lại version migration | 🚫 **Blocker — B1** |
| 3 | Chưa test lại sau merge | ⚠️ **Major — M3** (tụt 20 commit, 1 file giao nhau) |
| 4 | N+1 / chưa tối ưu | ✅ Đạt. Không query trong vòng lặp; anti-join chia lô `CO_LO_ANTI_JOIN = 1_000` có hằng số + lý do (giới hạn 65.535 bind param của PostgreSQL); danh sách dùng `findByKhoiTaoToKhaiIdIn(...)` gom một lượt; không `FetchType.EAGER`, không `@OneToMany`/`@ManyToOne` (tham chiếu đa hình cố ý, có javadoc); repository nguồn dùng native SQL có `JOIN`, không lazy access ngoài transaction. Index `ix_tax_bang_ke_mua_vao_anti_join` phủ đúng cột anti-join. |
| 5 | Chưa tận dụng Base BE | ✅ Đạt trong phạm vi hợp lý. Entity extend `AggregateRootEntity`; dùng `ApiResponse<T>`, `QuyenChecker`, `ApiException` của `core`; có `@Searchable` trên `KhoiTaoToKhai`. Không dùng `BaseCrudController` — chấp nhận được: đây không phải CRUD 8-endpoint mà là màn tờ khai có `lam-moi` / `tong-hop` / `trang-thai` / `phu-luc`, và bộ lọc `loc.ky`/`loc.nam`/`loc.trangThai`/`loc.nganhNghe` + Σ `[40]` theo loại kỳ (BR31) nằm ngoài khuôn base. |
| 6 | Chưa tận dụng base FE | ✅ N/A — PR không chạm `client/`. |
| 7 | Constant đặt sai chỗ | ⚠️ **Major — M2** (mã lỗi literal, thiếu `MaLoi*`). Mã message thì **đạt** — `MaThongBaoToKhai` gom đủ 58 hằng số. |

## Cổng đã chạy

| Cổng | Kết quả |
|---|---|
| `trace.sh` | `NOT-RUN` — không có `docs/doing/<slug>-spec/` cho PMKT-E-10978 (chưa chạy `/audit-spec`). Không đoán bừa thư mục PYC khác. |
| `msg.sh` | **Đạt 55/55.** Lần chạy đầu `msg.sh pmkt-docs/ba/PMKT-E-10978_ToKhaiThueGTGT be` báo `THIEU 55` — **kết quả sai**, vì script đọc working tree (đang ở `develop`, chưa có code PR). Đo lại thẳng trên head: `comm -23 <BA> <code>` → **rỗng**, tức **mọi mã BA cấp đều có trong code**. Dư 2 mã `_222`/`_223` (m2) + 1 false positive `_2` (chuỗi `MSG_PMKT-E-10978_2xx` trong javadoc `CanhBaoVang.java:10`). |
| Trùng số migration | ❌ **Đỏ** — quét toàn bộ remote branch, xem B1. |
| Đo tụt nhánh #3 | ⚠️ 20 commit · 1 file giao nhau — xem M3. |
| Cây commit / `git status` | ✅ Sạch trong phạm vi PR. |
| Compile-break do đổi chữ ký | ✅ Không — file prod bị **sửa** chỉ có `TongHopSoDuTaiKhoanRepository` (thêm method mới, thuần cộng thêm) và 2 `package-info.java` (javadoc). 212 file còn lại là thêm mới. |
| `@Tag("unit")` trên test mới | ✅ 40/40 file test mới đều có → sẽ chạy trong cổng `./gradlew unitTest`. |
| `./gradlew unitTest` | `NOT-RUN` — chế độ nhanh |
| Build / Testcontainers | `NOT-RUN` — chế độ nhanh (và Testcontainers cần Docker, đã bị cấm) |

## BR đã đọc / chưa đọc

**Đã đọc:** BR7 (làm tròn & precision), BR18 (ngoại tệ), BR19 (kiểm trùng), BR20.

**Chưa đọc (nêu rõ để lượt sau bù):** BR8 (ngày tháng / kỳ báo cáo — liên quan `KhoangKyTinhThue`, `HanNopToKhai`), BR28/BR29/BR46 (entity/DB/API), BR16/BR26/BR27 (thông báo & cảnh báo), BR25 (quyền), BR1/2/11/13.1/30/31/32/38/39/44/45 (màn danh sách tờ khai).

**Ghi chú BR7:** DDL khai `numeric` không precision cho `gia_tri_hang_mua_vao` / `thue_gtgt_hang_mua_vao`, còn code làm tròn `setScale(0, HALF_UP)` (VND nguyên) — lệch bảng BR7.1 (`decimal(18,2)`). Tờ khai thuế dùng VND nguyên là đúng nghiệp vụ nên **không** lập thành finding, nhưng chưa đối chiếu được với mục BR/quyết định nào cho phép lệch; nên để BA xác nhận.

## Phần chưa đọc

Đọc ~25/212 file nguồn, chọn theo thứ tự: seam `api/` → controller → service điều phối luồng Mua vào → business tính chỉ tiêu → repository nguồn → entity/DDL tương ứng. **Chưa đọc:**

- Service: `ChonHoaDonBanRaService`, `LuuToKhaiService`, `PhuLucService`, `LapToKhaiService`, `TongHopBoSungService`, `ToKhaiGtgtQueryService`, `XoaTrangThaiToKhaiService`, `ToKhaiChiTietMapper`, `ToKhaiGtgtSupport`.
- ~36/40 lớp `service/business/` (đã đọc: `TongHopChiTieuMuaVao`, `MapBangKeMuaVaoLuu`, `ValidateThanBangKeMuaVao`, `PhanNhomTinhChatThueMuaVao`). **Chưa đọc gồm cả** `TinhChiTieuToKhai`, `TinhChenhLechBoSung`, `TrangThaiToKhaiStateMachine`, `ChiTieuCodec`, `DoiChieuChiTieuBangKe`, `KhoangKyTinhThue`, `HanNopToKhai` — đây là nơi tính chỉ tiêu tờ khai, **rủi ro nghiệp vụ cao nhất còn lại**.
- 5/6 repository nguồn + 5/6 adapter `nguon/` (đã đọc `TraLaiHangMuaMuaVaoBangKeRepository`).
- DDL `V1129`, `V1130`, `V1132` (mới chỉ đọc phần `tax_bang_ke_mua_vao` của `V1131`).
- 40 file test (chỉ đọc tên method của `TongHopChiTieuMuaVaoTest` + kiểm `@Tag`), ~40 DTO, 2/5 controller (`PhuLucController`, `ToKhaiBoSungController`).

Không phần nào bị loại vì vùng đóng băng.

## Lệnh thực sự đã chạy

```bash
gh pr view 174 --repo ospgroupvn-pmkt/cell-app --json ...
git fetch origin pull/174/head:refs/pmkt-review/pr174 --force ; git fetch origin develop
git merge-base origin/develop refs/pmkt-review/pr174
git log --oneline <mb>..<head> ; git diff --stat/--name-status <mb> <head>
git ls-tree -r --name-only origin/develop src/main/resources/db/migration | sort -V | tail
for b in $(git branch -r | grep -v HEAD); do git ls-tree -r --name-only $b <migration> | grep -E "V(112[5-9]|113[0-9])__"; done
git rev-list --count <mb>..origin/develop
comm -12 <(git diff --name-only <mb> origin/develop|sort) <(git diff --name-only <mb> <head>|sort)
git diff <mb> <head> -- <file> ; git show <head>:<file>
git grep -n / -l / -c <head> -- <path>        # NamedInterface, MSG_, mã lỗi, N+1, secret, @Tag
./docs/rules/br.sh 7 18 19 20
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10978_ToKhaiThueGTGT be   # (chạy trên develop — xem ghi chú)
```

**Tài nguyên lượt này tạo:** ref tạm `refs/pmkt-review/pr174` (chưa xóa — xóa bằng `git update-ref -d refs/pmkt-review/pr174` nếu không cần tra lại). Không tạo worktree, không sửa file nào của repo `cell-app`.

---

## Nhận xét chung

Chất lượng kỹ thuật của module này cao hơn mặt bằng: javadoc dẫn thẳng tới quyết định BA kèm ngày chốt, RLS bật đủ `ENABLE` + `FORCE` + policy trên mọi bảng mới, repository nguồn dựa vào GUC tenant với `Propagation.MANDATORY` thay vì tự lọc `tenant_id`, anti-join chia lô có hằng số giải thích lý do, 40 file test đều gắn `@Tag("unit")`, mọi `api/` mở ra đều có người dùng thật và có test ranh giới Modulith riêng cho seam mới.

Ba việc phải làm trước khi merge: **(1)** đánh lại migration thành V1135–V1138 và kiểm lại sát giờ merge — B1; **(2)** đóng nhánh fail-open `[25]` và thêm validation cho `tinhChatThue` — M1; **(3)** gom mã lỗi vào một lớp `MaLoiToKhaiGtgt` — M2. Song song, nên chạy `/audit-spec pmkt-docs/ba/PMKT-E-10978_ToKhaiThueGTGT` để có `02-rules.md` — hiện chưa có cách nào chấm định lượng được độ phủ nghiệp vụ của 14 nghìn dòng này.
