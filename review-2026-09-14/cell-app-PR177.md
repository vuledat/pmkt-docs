# Review PR #177 — `ospgroupvn-pmkt/cell-app`

> `fix(sdbd): fix business rules and validation across opening balance modules`
> **Chế độ: NHANH** — chỉ đọc + kiểm tĩnh bằng `git`/`grep`. **KHÔNG** chạy `unitTest`,
> **KHÔNG** build, **KHÔNG** worktree, **KHÔNG** sửa code, **KHÔNG** đăng comment lên PR.

| | |
|---|---|
| Head | `d2b19700` (`fix/so-du-ban-dau`) |
| Base | `aab533e7` (`develop`) — merge-base = base, develop **0 commit** ahead |
| Diff | 56 file · +1210 / −728 (41 file `src/main`, 15 file `src/test`) |
| Commit | 3 commit, message đúng chuẩn `fix(<scope>): …` |

## Bảng đếm finding

| Mức | Số lượng |
|---|---|
| **Blocker** | **1** |
| **Major** | **5** |
| Minor | 8 |
| Nit | 7 |

**Kết luận: REJECT** — có 1 Blocker (nghiệp vụ không có nguồn) và 5 Major.
Cổng `./gradlew unitTest` và cổng Testcontainers **chưa chạy** (chế độ nhanh + máy không có Docker).

---

## Blocker

### B1 — Luật "số tiền không được âm" (BR13 / `_250`) là nghiệp vụ tự bịa, mã message không tồn tại

| | |
|---|---|
| Code | `internal/domain/KiemTraSoDu.java:184-194` · `internal/constants/MaLoiCongNoNv.java:62` · `internal/constants/MaLoiSoDuBanDau.java:59` · `cong_no_nv/internal/service/SoDuBanDauNhanVienCrudService.java:521` · `cong_no_nv/internal/nhap_excel/SoDuBanDauNhanVienNhapExcel.java:279-292` · `cong_no_nv/internal/dto/CreateSoDuBanDauNhanVienRequest.java:14` |
| Nguồn | `pmkt-docs/ba/PMKT-E-10964_SoDuBanDauNV/6.messages.md` · `5.screens/SCR_SoDuBanDauNV/SCR_SoDuBanDauNV_ThemMoi.md:78` · `…_NhapExcel.md:143` · `./docs/rules/br.sh 13` |

Ba bằng chứng độc lập nói ngược lại luật vừa thêm:

1. **BA cho phép số âm.** `SCR_SoDuBanDauNV_ThemMoi.md:78` và `…_NhapExcel.md:143` viết nguyên văn:
   *"số dư quy đổi tương ứng … bắt buộc phải khác 0 và phải cùng dấu (**cùng dương hoặc cùng âm**)"*.
   Chính javadoc cũ của DTO cũng ghi *"Giá trị âm là hợp lệ — BA nói rõ như vậy cho cả bốn cột"*;
   PR **xoá câu đó** và thay bằng *"Không nhận số âm (BR13)"*, không dẫn nguồn nào.
2. **`BR13` không phải luật này.** `./docs/rules/br.sh 13` → **"BR13. Hiển thị nút thao tác"**
   (điều kiện hiện nút Thêm/Sửa/Xoá/Ghi sổ). Epic `PMKT-E-10964` cũng **không** có `### BR13:`
   nội bộ màn (`grep -rn "BR13" pmkt-docs/ba/PMKT-E-10964_SoDuBanDauNV/` → 0 kết quả).
3. **Mã `MSG_PMKT-E-10964_250` không tồn tại** trong catalogue `6.messages.md` (26 mã, error cao nhất
   là `_231`, confirm `_401`/`_402`). Câu "Vui lòng nhập giá trị ≥ 0" cũng do dev tự đặt.

**Trigger** — nhập tay hoặc import Excel số dư nhân viên có bất kỳ ô nào < 0.
**Actual** — 400 `SO_TIEN_KHONG_HOP_LE` / lỗi dòng Excel.
**Expected (theo BA hiện hành)** — chấp nhận, chỉ kiểm "cùng dấu và khác 0".
**Hậu quả** — chặn dữ liệu hợp lệ ở phân hệ công nợ NV; FE nhận mã message không có trong
catalogue nên không i18n được (hiện chuỗi thô/rỗng).

Vi phạm **luật 9** (không tự quyết nghiệp vụ) + **Cổng đặc tả luật 2** (tài liệu không quy định →
mở mục `OPEN`, hỏi BA, không suy diễn) + Lớp A *"Nghiệp vụ tự bịa"*.

> Nếu có quyết định BA riêng cho bug 12–41 yêu cầu đổi luật này, **đính kèm nguồn vào PR** và bổ
> sung `_250` vào `6.messages.md` trước; khi đó B1 hạ xuống Minor (chỉ còn thiếu cập nhật catalogue).

---

## Major

### M1 — Đổi nguyên văn message `_228`, lệch BA ở cả 5 epic

`internal/nhap_excel/service/business/kiem_tra/KiemTraChungExcel.java:136`

```
- "Số dư quy đổi phải cùng dấu và khác 0 khi số dư nguyên tệ có phát sinh."
+ "Số dư quy đổi phải lớn hơn 0 khi số dư nguyên tệ có phát sinh."
```

`KiemTraChungExcel` dùng chung cho **cả 5 phân hệ**. Cả 5 catalogue
(`PMKT-E-10931/10958/10964/10970/10976` `6.messages.md`, mã `_228`) đều ghi **nguyên văn** bản cũ.
Đây là `LECH` theo `msg.sh` — và câu mới còn **nói sai luật**: BA cho phép "cùng âm", câu mới nói
"phải lớn hơn 0". Sửa: trả lại đúng chuỗi BA, hoặc xin BA đổi catalogue trước.

### M2 — Nhân bản `@Formula` SQL thuần ra 4 entity và xoá luôn cảnh báo "chỉ Testcontainers mới chứng minh được"

`internal/entity/CongThucSoDuSql.java` (mới, 69 dòng) · entity KH/NV/TKNH · `cong_no_ncc/internal/entity/CongThucNcc.java` (xoá)

`CongThucNcc` bị xoá mang đúng cảnh báo này trong javadoc:

> *"Không unit test nào bắt được; chỗ duy nhất chứng minh được bảy biểu thức dưới đây là gate
> `./gradlew build` với Postgres thật (Testcontainers). **Bắt buộc chạy gate trước khi merge.**"*

PR gỡ cảnh báo đó và nhân số biểu thức từ 7 (một entity) lên 13 (bốn entity), trong đó **6 biểu thức
hoàn toàn mới chưa từng chạy**: `MA_KHACH_HANG`, `TEN_KHACH_HANG`, `MA_NHAN_VIEN`, `TEN_NHAN_VIEN`,
`SO_TK_NGAN_HANG`, `TEN_NGAN_HANG`. `ddl-auto: none` nên sai tên bảng/cột chỉ lộ ở **truy vấn đầu
tiên chạm entity** — tức là 500 trên màn danh sách ở môi trường thật.

Tôi đã đối chiếu tay tên cột với `V1__create_database.sql`, **tất cả đều đúng**
(`mst_nhan_vien.ma/ten`, `mst_tai_khoan_ngan_hang.so_tai_khoan/ngan_hang_id`, `mst_ngan_hang.ten/da_xoa`,
`mst_doi_tuong.ma/ten`, và `khach_hang_id`/`nhan_vien_id`/`tk_ngan_hang_id`/`loai_tien_id` trên 3 bảng
`sdbd_*`). Bốn `*TongHopIntegrationTest` mới **có** phủ lọc/sắp xếp/tìm nhanh trên các cột này —
nhưng cả bốn **không** gắn `@Tag("unit")`, cần Docker, nên **không chạy được trên máy này**.
→ **Bắt buộc chạy các test này trên CI có Docker trước khi merge**; đừng merge dựa trên `unitTest` xanh.

### M3 — Lọc/sắp xếp/tìm nhanh chuyển từ `IN (ids)` có index sang correlated subquery + `LIKE` không index được

`internal/domain/LocCotDanhMuc.java` (120 → 46 dòng) · `internal/repository/LocDanhMucSoDuRepository.java` (xoá, 265 dòng) ·
`SoDuBanDauKhachHangCrudService.java:122` · `SoDuBanDauNhanVienCrudService.java:119` · `SoDuTkNganHangCrudService.java:116`

Trước: điều kiện trên `maKhachHang`/`tenKhachHang`/`soHieuTaiKhoan`/`soTaiKhoanNganHang`/`tenNganHang`
được hỏi danh mục **một lần** rồi viết lại thành `<fieldId> IN (ids)` — chạy trên khoá UUID có index.
Sau: điều kiện chạy thẳng trên property `@Formula`, Hibernate sinh
`lower((select dt.ten from mst_doi_tuong dt where dt.id = khach_hang_id)) like '%…%'`
— **subquery tương quan cho TỪNG dòng** của `sdbd_*`, không dùng được index, không short-circuit,
và `WHERE` không thu hẹp được trước khi subquery chạy. Cùng đường đó áp cho `sort` và cho
`keyword = true` (7 cột × N dòng). Trên tenant có vài chục nghìn dòng số dư, mỗi lần bấm Lọc/Tìm là
một seq scan kèm N subquery.

Nếu chấp nhận đánh đổi này để có server-side sort (lý do chính đáng, đã ghi ở javadoc `CongThucNcc` cũ)
thì **ghi rõ trong PR** và đo trên dữ liệu thật; đừng để mất im lặng đường `IN (ids)`.

### M4 — Đọc danh mục hai lần trên mọi dòng lưới

`SoDuBanDauKhachHangMapper.java:104-118` · `SoDuTkNganHangMapper.java:48-62` ·
`SoDuBanDauNhanVienMapper.java:41` · `…CrudService.dongGop()` · `…CrudService.bomDanhMuc()/lamGiau()`

Mapper và `dongGop` **giờ** lấy mã/tên tài khoản, khách hàng, nhân viên, ngân hàng, loại tiền từ
`@Formula` (mỗi dòng 5–7 subquery). Ngay sau đó `search()` vẫn gọi `lamGiau()` → `bomDanhMuc()` và
**ghi đè toàn bộ** bằng đúng các giá trị đó lấy từ tra cứu theo lô có sẵn:

```java
tk != null ? tk.soTaiKhoan() : dto.soHieuTaiKhoan()   // SoDuTkNganHangCrudService.java:503
```

Đường happy-path trả tiền hai lần cho cùng một dữ liệu. Nhánh `@Formula` chỉ còn tác dụng khi tra cứu
danh mục **trượt** — và khi đó nó sinh ra M5. Chọn một: hoặc bỏ `bomDanhMuc` cho các cột đã có
`@Formula`, hoặc bỏ `@Formula` khỏi projection DTO và chỉ giữ để lọc/sắp xếp.

### M5 — `tinhChatTaiKhoan` rò giá trị DB thô, vượt hợp đồng đã đóng băng

`SoDuBanDauNhanVienCrudService.java:604` · `SoDuTkNganHangCrudService.java:505` · `SoDuBanDauNhanVienMapper.java:41-43`

`TinhChatTaiKhoan.tenTheoHopDong()` có javadoc: *"`contract.md` (FROZEN) khai trường này đúng ba giá
trị — `"DU_NO" | "DU_CO" | "LUONG_TINH"`"*, và `KHONG_CO_SO_DU` **phải ra `null`**.

`@Formula CongThucSoDuSql.TINH_CHAT_TAI_KHOAN` trả **mã DB thô**: `DuNo` / `DuCo` / `LuongTinh` /
`KhongCoSoDu`. Trong `bomDanhMuc`, nhánh fallback mới là:

```java
tk != null ? TinhChatTaiKhoan.tenTheoHopDong(tk.tinhChat()) : dto.tinhChatTaiKhoan()
```

**Trigger** — tài khoản kế toán bị xoá/không tra được trong danh mục (`tk == null`).
**Actual** — DTO trả `"DuNo"` (hoặc giá trị thứ tư `"KhongCoSoDu"`).
**Expected** — `null` (hành vi TRƯỚC PR) hoặc `"DU_NO"`.
**Hậu quả** — FE so chuỗi enum sẽ không khớp → render sai ô Tính chất; hợp đồng FROZEN bị mở rộng âm thầm.
Sửa: bọc fallback bằng `TinhChatTaiKhoan.tenTheoHopDong(dto.tinhChatTaiKhoan())`.

---

## Minor

| # | Vị trí | Nội dung |
|---|---|---|
| m1 | `internal/constants/BoMaThongBao.java:41-48` | Constructor 8 tham số "tương thích ngược" nhét `null` cho `soTienKhongAm`. 5/6 instance (`MaLoiCongNoKh.MASTER/CHI_TIET`, `MaLoiCongNoNcc.BO_MA`, `MaLoiSoDuTaiKhoan.MASTER/CHI_TIET`, `MaLoiSoDuTkNganHang.BO_MA`) đang mang `null`. Hôm nay chỉ `cong_no_nv` gọi `khongDuocAm` nên chưa nổ; lần đầu một module khác gọi, lỗi bắn ra **không có mã message**. Bỏ overload, bắt mọi nơi khai tường minh. |
| m2 | `KiemTraSoDu.java:193` + `SoDuBanDauNhanVienNhapExcel.java:291` | Chuỗi `"Vui lòng nhập giá trị ≥ 0"` hardcode ở **2 file** → phải thành hằng số trong `internal/constants/` (luật 1 + lỗi #7). |
| m3 | `KiemTraSoDuKhachHang.java:189-193` · `KiemTraSoDuTaiKhoan.java:179-181` · `KiemTraChungExcel.java:44-46` | Ba overload cũ giờ **chỉ còn test gọi** (`git grep` xác nhận 0 caller ở `src/main`). Tệ hơn: `KiemTraSoDuKhachHangTest` và `KiemTraSoDuTaiKhoanTest` **không nằm trong PR**, vẫn assert ngữ nghĩa BR8/BR18 **đã bị thay** → xanh giả. Xoá overload và cập nhật hai test class đó. |
| m4 | `CayTaiKhoanSoDu.java:188-190` | `nutKhopTuKhoa` và `truyenChoCon` tính bằng **biểu thức y hệt nhau** → gọi `viTuTuKhoa.test(nut)` hai lần cho mỗi nút. Gộp thành một biến. |
| m5 | `CongThucSoDuSql.java:60-64` | Chỉ `TEN_NGAN_HANG` lọc `nh.da_xoa = false`; 12 biểu thức còn lại không lọc `da_xoa`. Hoặc thống nhất lọc, hoặc ghi rõ vì sao ngân hàng khác phần còn lại. |
| m6 | `SoDuBanDauVatTuCrudService.java:116-120` | `ApiException.notFound("NOT_FOUND", null, "Bản ghi không tồn tại hoặc đã bị xóa")` — message người dùng thấy **không có mã `MSG_…`** (tham số thứ 2 là `null`) → FE không i18n được. |
| m7 | `internal/entity/CongThucSoDuSql.java` | Lớp hằng số thuần (không `@Entity`) đặt trong `internal/entity/`. Module đã có `internal/constants/` — theo lỗi #7 nó phải nằm ở đó. (Bản cũ `CongThucNcc` cũng sai chỗ này, PR nhân bản cái sai ra phạm vi toàn phân hệ.) |
| m8 | `SoDuBanDauKhachHangNhapExcel.java:173,205` · `SoDuBanDauNccNhapExcel.java:177,213` | `boiCanh.loaiTien(DocO.chuoi(d, CotSoDu.LOAI_TIEN))` tra **2 lần cho mỗi dòng** (khối `soDuCanDoi` và khối `tyGia`). Tra một lần, truyền xuống. |

## Nit

| # | Vị trí | Nội dung |
|---|---|---|
| n1 | `SoDuBanDauKhachHang.java:92-113` · `SoDuTkNganHang.java:76-100` · `DanhSachSoDuTaiKhoanService.java:98-101` · `SoDuBanDauNhanVienNhapExcel.java:286-288` | Dùng tên đầy đủ inline (`@Formula(vn.vtt.pmkt.cell…CongThucSoDuSql.X)`, `java.util.function.Predicate`, `java.math.BigDecimal`, `vn.vtt.pmkt…SoTien`) thay vì `import`. `SoDuBanDauNhanVien.java` trong cùng PR đã làm đúng — không đồng nhất. |
| n2 | `SoDuBanDauNccEntity.java:24` · `cong_no_ncc/package-info.java:25` | `{@link CongThucNcc}` / `{@code CongThucNcc}` trỏ tới class **đã xoá**. Không gãy build (không bật doclint) nhưng javadoc hỏng. |
| n3 | `DoiTruSoDuKhachHang.java:58-60` | `rong()` đổi `duNoQuyDoi` → `duNoQuyDoi()` (no-op trên record), lệch kiểu với `duNo`/`duCo` ngay cạnh. Diff thừa. |
| n4 | Nhánh `fix/so-du-ban-dau` | Chuẩn nhánh là `bugfix/<mo-ta>`, không `fix/` (`conventions-chung.md`, Lớp D). |
| n5 | `SoDuBanDauNccNhapExcel.java:233-238` | Hai khối javadoc liên tiếp trên cùng một method — khối đầu (`/** Trùng khoá BR19 … */`) bị javac bỏ qua. Gộp lại. |
| n6 | `LocCotDanhMuc.java` cuối file | Thêm một dòng trắng thừa ở EOF. |
| n7 | `SoDuBanDauKhachHang.java:50,92` (và NV, NCC, TKNH) | `@Searchable(alias="soHieuTaiKhoan", path="soTaiKhoan", keyword=true)` ở class + `@Searchable(keyword=true)` ở field `soTaiKhoan` → cùng một cột vào mệnh đề keyword `OR` **hai lần**. Vô hại, nhưng nên bỏ `keyword` ở một trong hai. |

---

## Bảng 7 lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ⚠ **m7** — `CongThucSoDuSql` (hằng số thuần) nằm ở `internal/entity/`. Còn lại ✅: mọi file mới đều trong `internal/`, không thêm `api/`, base package `vn.vtt.pmkt` đúng, không đụng `master_data/**` (chỉ tham chiếu bảng `mst_*` bằng SQL — đã có tiền lệ ở `CongThucNcc`, và javadoc entity khai rõ) |
| 2 | Không đánh lại version migration | ✅ **N/A** — `git diff --name-status` không có file nào dưới `src/main/resources/db/migration` |
| 3 | Chưa test lại sau khi merge | ✅ **N/A** — `git rev-list --count $MB..origin/develop` = **0**; `comm -12` file giao nhau = **0 file** |
| 4 | Chưa tối ưu / N+1 | ⚠ **M3, M4, m8** |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ — service vẫn extend `AbstractCrudService`, entity extend `SoDuCanDoiEntity`, tìm kiếm qua `@Searchable`/`SearchExecutor`; không có controller/entity/repository mới |
| 6 | Chưa tận dụng base FE | ✅ **N/A** — PR thuần BE |
| 7 | Constant đặt sai chỗ | ⚠ **m2** (chuỗi lặp 2 file), **m6** (message không có mã), **m7** |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| **A — Cổng cứng** | ⚠ **B1** (nghiệp vụ tự bịa). Không secret; không đụng Controller / `ApiResponse` / `@RestControllerAdvice`; không nuốt exception; không commit thẳng `develop`; không copy pattern từ vùng đóng băng |
| **B — Kiến trúc & 7 lỗi** | xem bảng trên |
| **C — Nghiệp vụ & truy vết** | `trace.sh` **NOT-RUN** — không có `docs/doing/*-spec` cho sdbd. `msg.sh` **NOT-RUN** — diff trải trên **6 epic** (`PMKT-E-10931/10958/10964/10970/10976/10984`), không có một thư mục PYC đơn để truyền vào. **Thay thế**: đối chiếu tay 8 chuỗi message đổi trong diff với `6.messages.md` của từng epic → 6 đúng nguyên văn (✅ `_219` KH, `_219` NCC, `_212` NV, `_212` TKNH, `_213` VT, `_211` tỷ giá KH), **2 sai** (❌ `_228` = **M1**, ❌ `_250` không tồn tại = **B1**) |
| **D — Vệ sinh diff & Git** | ⚠ **n2, n3, n4, n5, n6**. Commit message đúng chuẩn `fix(sdbd): …`, 3 commit tách theo nhóm bug. Không thấy code debug/TODO không mã. Cổng cây commit: không tìm thấy tham chiếu treo — `git grep` trên head xác nhận `LocDanhMucSoDuRepository`, `LocCotDanhMuc.vietLai`, `LocCotDanhMuc.AnhXa`, `CongThucNcc` không còn caller nào ở `src` (chỉ còn 3 chỗ nhắc trong **javadoc/comment** → n2) |

## BR đã đọc / chưa đọc

- **Đã đọc**: `BR13` (qua `./docs/rules/br.sh 13`) — để kiểm chứng B1.
- **Chưa đọc**: BR1, 2, 7, 11, 16, 18, 19, 30, 38, 39 và bộ BR chứng từ/tiền tệ. Lý do: diff là
  **sửa lỗi trong phạm vi đã có**, các luật đó đã hiện thực từ trước và diff không thay đổi ý nghĩa
  của chúng — trừ BR8/BR16/BR18 (xác nhận ghi đè), đã kiểm bằng cách đọc thẳng code + test thay vì
  kéo thêm ~45 KB BR.

## Phần đã đọc / chưa đọc

**Đã đọc đầy đủ diff `src/main` (41/41 file).**

**Chưa đọc / chưa kiểm sâu** (`src/test`, 15 file — chỉ đọc 6):

- `SoDuBanDauKhachHangTongHopIntegrationTest`, `SoDuBanDauNccTongHopIntegrationTest`,
  `SoDuBanDauNhanVienTongHopIntegrationTest`, `SoDuTkNganHangTongHopIntegrationTest` —
  chỉ xem danh sách `@Test` (xác nhận có phủ lọc/sort/tìm nhanh trên cột `@Formula`), **không đọc thân test**.
- `SoDuBanDauNhanVienSearchableTest`, `LocCotDanhMucTest` (−141 dòng), `CayTaiKhoanSoDuTest` (+55),
  `DanhSachSoDuTaiKhoanServiceTest` (+43), `SoDuBanDauVatTuNhapExcelTest`, `SoDuBanDauVatTuCrudServiceTest`,
  `SoDuTkNganHangCrudServiceTest`, `SoDuBanDauNhanVienCrudServiceTest` (chỉ đọc phần assert `_250`) —
  **không đọc chi tiết**.
- `KiemTraSoDuKhachHangTest` / `KiemTraSoDuTaiKhoanTest`: **không nằm trong PR** nhưng liên quan trực tiếp
  (xem m3) — chỉ `git grep` xác nhận chúng còn gọi overload cũ.

## Cổng chưa chạy

| Cổng | Trạng thái |
|---|---|
| `cd cell-app && ./gradlew unitTest` | **NOT-RUN** — chế độ nhanh |
| Testcontainers (4 `*TongHopIntegrationTest` mới) | **NOT-RUN** — máy không có Docker (luật cứng CLAUDE.md). **Đây là cổng duy nhất chứng minh 13 biểu thức `@Formula` (M2) — bắt buộc chạy trên CI trước khi merge** |
| `trace.sh` / `msg.sh` | **NOT-RUN** — lý do ở Lớp C |
| Merge thử | **NOT-RUN** — không cần, 0 file giao nhau với `develop` |

## Lệnh đã chạy

```bash
gh pr view 177 --json …
git fetch origin fix/so-du-ban-dau develop
git merge-base aab533e7 d2b19700                       # = aab533e7
git rev-list --count $MB..origin/develop               # = 0
comm -12 <(git diff --name-only $MB origin/develop|sort) \
         <(git diff --name-only $MB origin/fix/so-du-ban-dau|sort)   # rỗng
git diff --name-status aab533e7..d2b19700
git diff aab533e7..d2b19700 -- <từng nhóm file>
git show d2b19700:<file>                               # đọc file ở head
git grep -n "<symbol>" d2b19700 -- src                 # tìm caller / tham chiếu treo
./docs/rules/br.sh 13
grep -rn … pmkt-docs/ba/PMKT-E-109*/6.messages.md      # đối chiếu message
```

> Lượt review này **không** sửa file nào trong repo. Có một lần `git checkout --detach` tạm trên
> `cell-app` để grep migration, **đã khôi phục lại đúng nhánh `feat/chung-tu-ban-hang-2`**; working
> tree sạch sau khi xong.

## Chưa đăng lên PR

Theo yêu cầu của người gọi: **tuyệt đối không** `gh pr comment` / `gh pr review`. Báo cáo chỉ nằm ở
file này.
