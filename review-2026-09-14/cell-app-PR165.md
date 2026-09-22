# Review PR #165 — cell-app · "create api for dieu chinh gia hang mua"

| Mục | Giá trị |
|---|---|
| Repo | `ospgroupvn-pmkt/cell-app` |
| PR | [#165](https://github.com/ospgroupvn-pmkt/cell-app/pull/165) · OPEN |
| Nhánh | `feat/pmkt-e-06768-be` → `develop` |
| head SHA | `0e931fe4f867815955bbed5bfe755df405426938` |
| base SHA (develop lúc review) | `aab533e76732342535e01fae0613067f3c745377` |
| merge-base | `c6cb948ecb67faf13c3c9e59edc321664522c7c1` |
| Diff | 46 file · +3120 / −249 · 1 commit |
| Working tree | sạch (`git status --porcelain` rỗng) |
| **Chế độ review** | **NHANH** — chỉ đọc + kiểm tĩnh bằng git/grep. **KHÔNG** chạy `unitTest`/build, không worktree, không merge thử, không đo baseline. |
| Epic | PMKT-E-06768 — Điều chỉnh giá hàng mua |

**Kết luận: REJECT** — 2 Blocker, 7 Major.

---

## 1. Bảng đếm finding

| Mức | Số lượng | Mã |
|---|---|---|
| **Blocker** | 2 | B1, B2 |
| **Major** | 7 | M1 … M7 |
| **Minor** | 6 | m1 … m6 |
| **Nit** | 3 | n1 … n3 |

---

## 2. Blocker

### B1 — Toàn bộ migration của epic THIẾU khỏi PR, trong khi entity/quyền/CHECK đều đã đổi theo nó

- **Bằng chứng:** `git diff --name-status c6cb948e 0e931fe4 -- src/main/resources/db/migration` → **rỗng**. Không một file `.sql` nào trong PR.
- Nhưng code đã đi trước lược đồ:
  - `internal/entity/ChiTietDieuChinhGiaMua.java` thêm **11 cột mới** (`chung_tu_mua_hang_id`, `loai_dong_hang NOT NULL`, `loai_vat_tu_id`, `don_vi_tinh_chinh_id`, `he_so_quy_doi NOT NULL`, `thanh_tien`, `nhom_hhdv_mua_vao`, `khong_tong_hop_to_khai_gtgt NOT NULL`, `dien_giai_thue`, `thanh_tien_quy_doi`, `chiet_khau_quy_doi`, `tien_thue_gtgt_quy_doi`).
  - `internal/entity/ChungTuDieuChinhGiaMua.java` thêm **7 cột** (`tong_tien_thue_gtgt`, `tong_thanh_toan`, 4 cột `*_quy_doi`, `so_chung_tu_phieu_thu_chi`) và **gỡ `nullable = false`** khỏi `chung_tu_mua_hang_id`.
  - `common/constant/MaChucNang.java:216` đổi mã quyền `GiamGiaHangMua` → `DieuChinhGiaHangMua`; javadoc khai catalog quyền đổi ở `V1111__iam_doi_namespace_quyen_dieu_chinh_gia_hang_mua.sql`, mã `.Clone` seed ở `V1112`.
  - `tham_chieu_chung_tu/api/LoaiChungTuChu.java:42` thêm `PUR_DIEU_CHINH_GIA_HANG_MUA`, javadoc khai "whitelist DB mở ở V1113".
  - `NguonDieuChinhGiaQuery.java` đọc `d.loai_dong_hang`, `d.thanh_tien`; `DieuChinhGiaMuaSupport.java:38` khai CHECK `ck_pur_ct_dcgm_ly_do (V1112)`.
- **Kiểm chứng:** `git ls-tree -r --name-only 0e931fe4 -- src/main/resources/db/migration` → max trên head là **V1110**; **V1112 và V1113 không tồn tại**, còn **V1111 ĐÃ BỊ CHIẾM** bởi `V1111__iam_quyen_bieu_mau.sql` (có sẵn từ trước PR).
- **Hậu quả:** Hibernate validate / mọi native query nổ trên DB thật; `QuyenChecker` so `DieuChinhGiaHangMua` không khớp `iam_quyen` ⇒ **toàn bộ màn 403 với mọi user kể cả admin** (chính javadoc controller cảnh báo điều này); `pur_chung_tu_dieu_chinh_gia_hang_mua.chung_tu_mua_hang_id` vẫn `NOT NULL` ⇒ lập chứng từ đa nguồn/nhập tay chết ở tầng DB.
- **Fix:** bổ sung migration. **Đánh lại số ≥ V1123** — `max` trên `origin/develop` hiện là **V1122**, và V1111 đã bị dùng; mọi javadoc trỏ V1111/V1112/V1113 phải sửa theo.

### B2 — Cổng `unitTest` chắc chắn ĐỎ: test mới tự yêu cầu một migration không tồn tại

- `src/test/java/vn/vtt/pmkt/cell/dieu_chinh_gia_hang_mua/NguonVaHoaDonSchemaTest.java` khai danh sách file phải đọc, có `"V1112__pur_dcgm_bo_sung_cot_theo_ldm.sql"`, và `gopMigration()` assert:

```java
assertThat(Files.exists(file)).as("Thiếu migration %s", ten).isTrue();
```

- File đó không tồn tại (xem B1) ⇒ **cả hai test `bangVaCotCuaA17ConTonTaiDungTen` và `bangVaCotCuaA19ConTonTaiDungTen` đỏ** ngay khi `./gradlew unitTest` chạy. Đây là kết luận tĩnh, không cần chạy cổng.
- Test đỏ này quy được cho diff (cả file test lẫn migration đều thuộc phạm vi PR).

---

## 3. Major

### M1 — N+1 ở `DieuChinhGiaMuaSupport.napNguon` (lỗi hay gặp #4)

`internal/DieuChinhGiaMuaSupport.java` (khối `napNguon`):

```java
for (UUID id : nguonIds) {
    NguonDieuChinhGia nguon = nguonApi.layNguonDieuChinhGia(id);   // 1 lượt đọc / 1 chứng từ nguồn
    ...
}
```

- **Trigger:** đúng tính năng chủ đạo của PR — D6 cho phép một chứng từ điều chỉnh lấy dòng từ **nhiều** chứng từ mua. Vòng lặp chạy trên tập id gom từ dòng.
- **Actual:** N lượt gọi cổng module khác cho mỗi lượt Lưu / Ghi sổ (và `kiemTraNghiepVu` được gọi ở cả 4 luồng Tạo · Sửa · Ghi sổ · Lưu-và-ghi).
- **Expected:** cổng nhận cả lô (`layNguonDieuChinhGia(Set<UUID>)`) như `soCongNoApi.dinhTuyenTaiKhoan(Set)` ngay bên dưới trong cùng file đã làm đúng.
- Thêm một lượt đọc nữa: `nguonQuery.laDichVuTheoDong(chiTietIds)` — cái này đã gom lô, đúng.

### M2 — `thanhTienQuyDoi` tính từ số NET, lệch nghĩa với `thanhTien` cùng dòng

`internal/service/TinhToanDieuChinhGiaMua.java` (thân `apDung`):

```java
d.setThanhTien(tien(thanhTien));                                  // GROSS: soLuong × donGia
...
d.setThanhTienQuyDoi(quyDoi(d.getThanhTienQuyDoi(), net, tyGia));  // ← net = thanhTien − chiết khấu
```

- **Nguồn:** javadoc của chính entity `ChiTietDieuChinhGiaMua`: *"LDM `ThanhTien` = `soLuong × donGia`, **TRƯỚC** chiết khấu"*.
- **Actual:** `thanh_tien_quy_doi = (thanhTien − ck) × tyGia`. **Expected:** `thanhTien × tyGia`.
- **Hậu quả:** ô "Thành tiền quy đổi" trên lưới FE không bằng "Thành tiền × tỷ giá" — người dùng đối chiếu tay sẽ thấy lệch đúng bằng chiết khấu. Tổng header vô tình vẫn đúng vì `tongHangQd = thanhTienQuyDoi + chietKhauQuyDoi`, nên lỗi này **không** lộ ra ở bất kỳ tổng nào — chỉ lộ ở mức dòng.

### M3 — Làm tròn / lưu trữ trái BR7.1 và BR7.2.3

`TinhToanDieuChinhGiaMua.java` `SCALE_TIEN = 2`, áp cho **mọi** ô tiền kể cả nguyên tệ (`tien(...)` gọi ở 14 chỗ trong `apDung`).

- **BR7.1:** Tiền tệ VND `decimal(18,2)` nhưng **Ngoại tệ `decimal(18,4)`**. Chứng từ này có `loaiTienId` + `tyGia`, tức nguyên tệ có thể là ngoại tệ ⇒ cắt về 2 chữ số là mất 2 chữ số BR bắt giữ.
- **BR7.2.3:** *"Lưu giá trị đầy đủ (không làm tròn) vào DB… Chỉ làm tròn khi hiển thị"*. Code làm tròn **trước khi lưu**.
- Thêm: thuế làm tròn **theo từng dòng** rồi mới cộng (`d.setTienThueGtgtVnd(tien(thue))` → `tongThue.add(thue)`), trong khi javadoc lớp tự khai *"làm tròn ở KẾT QUẢ CUỐI"* — hai câu trong cùng một file không khớp nhau.

### M4 — Mã message không thành hằng số (lỗi hay gặp #7)

Module `dieu_chinh_gia_hang_mua` **không có thư mục `internal/constant(s)/`** (`git ls-tree` toàn module: 38 file, không có ngăn constant), trong khi 8 module anh em đều có `MaLoi*.java` (`ban_hang/chung_tu_ban_hang/internal/constant/MaLoiBanHang.java`, `kho/nhap_kho/…/MaLoiNhapKho.java`, …).

Mã rải dạng string literal:

- `internal/controller/DieuChinhGiaMuaController.java:98,99,118,119,158` — `MSG_PMKT-E-06768_001/_002/_003/_004/_604`
- `internal/congno/CongNoDieuChinhGiaMuaService.java:171` — `_203`
- `internal/service/KiemTraDieuChinhGiaMua.java:252` — `_104`
- `MSG_COMMON_001` lặp ở 4 file (`GhiSo`, `BoGhiSo`, `Sua`, `Xoa`).

`checklist-be §F`: mã dùng ≥2 file phải là `public static final` trong `internal/constant/MaLoi<Module>.java`.

### M5 — Phần lớn lỗi nghiệp vụ trả `messageId = null` ⇒ không truy vết được message nào

- `KiemTraDieuChinhGiaMua.loi(code, message)` — **toàn bộ** luật kiểm dòng ném qua đây với `messageId` cứng là `null`.
- `NguonDieuChinhGiaService` — `SUPPLIER_REQUIRED`, `DATE_RANGE_REQUIRED`, `INVALID_DATE_RANGE`, `INVALID_SOURCE_DOCUMENT_TYPE`: đủ 4 lỗi, `messageId = null`.
- `DieuChinhGiaMuaCrudService.notFound`, `DieuChinhGiaMuaSupport.nap`, `CongNoDieuChinhGiaMuaService.loaiTienId/taiKhoanDoiUng`: PR **gỡ** mã `_002` (đúng — `_002` là câu thành công) nhưng thay bằng `null` chứ không xin mã mới.
- **Đo được:** `./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-06768_DieuChinhGiaHangMua be` → `Tong 0 message (tang=be): OK 0 · LECH 0 · THIEU-VI 0 · CHUA-DAT 0 · THIEU 0`. Không có một message nào của epic được đối chiếu.
- **Hậu quả:** FE không i18n được, và mọi câu tiếng Việt trong PR là chuỗi Java cứng không có khoá.

### M6 — Đổi luật kế toán mà nguồn viện dẫn là một câu chat, không phải tài liệu BA

`internal/congno/CongNoDieuChinhGiaMuaService.java` (javadoc lớp + thân `ghi`): nhánh "phần điều chỉnh GIẢM vượt số còn nợ" trước đây ghi thành **khoản chờ**, nay **bỏ hẳn** ⇒ rơi vào `VUOT_SO_DU` của `ghiNhanDoiTruDichDanh` ⇒ **cả lượt ghi sổ 409**.

Javadoc tự khai nguồn: *"Chốt của user: 'không thuộc epic này nhắc tới thì bỏ đi nhé'"*.

- Đây là thay đổi **hành vi tiền** (chứng từ trước đây lưu được nay bị chặn), viện dẫn một câu hội thoại chứ không phải mục nào của `TaiLieuMappingSoCongNo` §5.7.
- `CLAUDE.md` luật 9 + lớp A "Nghiệp vụ tự bịa / không nguồn": phải mở mục `OPEN` và hỏi BA, không tự chọn. Cần BA xác nhận bằng văn bản trước khi merge.

### M7 — Chưa test lại sau khi merge nhánh đích (lỗi hay gặp #3)

```
git rev-list --count c6cb948e..origin/develop        → 26
comm -12 <(git diff --name-only c6cb948e origin/develop) <(git diff --name-only c6cb948e 0e931fe4)
  → src/main/java/vn/vtt/pmkt/cell/common/storage/api/FileGroup.java
    src/main/java/vn/vtt/pmkt/cell/tham_chieu_chung_tu/api/LoaiChungTuChu.java
```

- Nhánh tụt **26 commit** và có **2 file giao nhau**. Cả hai đều là **enum đăng ký dùng chung toàn repo** (`FileGroup`, `LoaiChungTuChu`), PR này thêm hằng vào **cuối** cả hai — đúng chỗ nhánh khác cũng thêm ⇒ xung đột văn bản gần như chắc chắn, và xung đột kiểu "cả hai cùng thêm một dòng trước dấu `;`" rất dễ giải sai.
- `LoaiChungTuChu` còn được `LoaiChungTuChuDongBoCheckTest` soi đồng bộ với DB — merge sai là test đó đỏ.
- **Yêu cầu:** rebase/merge `develop` rồi chạy lại cổng trước khi merge.

---

## 4. Minor

| Mã | Vị trí | Nội dung |
|---|---|---|
| m1 | `internal/repository/NguonDieuChinhGiaQuery.java` (`CTE`, `DIEU_KIEN`, `KIEM_PHIEU_NHAP_KHO`) · `KiemTraTrungHoaDonDcgmQuery.java` (`SQL`) | Magic value nghiệp vụ nhúng thẳng SQL: `'TangGiaHangMua'`, `'TrongNuoc'`, `'DA_GHI_SO'`, `'NhapKho','MuaHangNhapKho'`, `'PhieuChi'`, `'NguoiBanXuatDieuChinh'`. Riêng `'TangGiaHangMua'` đã có hằng `DieuChinhGiaMuaSupport.TANG_GIA` ngay trong module — chép giá trị sang file thứ hai là vi phạm luật 1. |
| m2 | `DieuChinhGiaMuaCrudService.xemTruocHachToan` | `@Transactional(readOnly = true)` nhưng gọi `dcg.tinhToan().apDung(ct)` — ghi đè hàng loạt field của entity đang **managed**. Hiện an toàn nhờ `FlushMode.MANUAL` của readOnly, nhưng đây là ghi lén trong phép đọc; nên tính trên bản sao. |
| m3 | `NguonDieuChinhGiaService.trang(...)` | Tự dựng `PageResponse` + `PageInfo` và tự tính `offset`/`soTrang` thay vì dùng `PageResponse.ofList` / helper của `core` (controller ngay bên cạnh dùng `PageResponse.ofList(..., PhanTrang.cua(...))`). Hai cách tính phân trang song song trong cùng một màn. |
| m4 | `NguonDieuChinhGiaQuery.java` javadoc lớp · `KiemTraTrungHoaDonDcgmQuery.java` javadoc lớp | Trỏ tới `NguonDieuChinhGiaSchemaTest` và `KiemTraTrungHoaDonSchemaTest` — **không tồn tại**; test thật là `NguonVaHoaDonSchemaTest`. Javadoc là bằng chứng "cổng đã có", trỏ sai tên làm mất chính bằng chứng đó. |
| m5 | Toàn bộ javadoc mới | Trộn BR nội bộ epic với BR chung mà không phân biệt: `XoaDieuChinhGiaMua` viết *"vế thu hồi của BR10"* (BR10 chung là **"Trường Chọn nguồn"**, không liên quan số chứng từ); tương tự `BR12`, `BR16.1`, `BR29.1`. Nên viết `BR_DCGM_xx` hoặc ghi rõ "BR chung". |
| m6 | `DieuChinhGiaMuaCrudService.java:16-17` · `MapperDieuChinhGiaMua.java` | Import `vn.vtt.pmkt...` chèn **trước** `org.springframework...` (sai thứ tự nhóm); còn dùng tên đầy đủ inline `java.math.BigDecimal.ZERO`, `vn.vtt.pmkt.cell.core.entity.TrangThaiChungTu.CHUA_GHI_SO` giữa biểu thức. |

---

## 5. Nit

| Mã | Vị trí | Nội dung |
|---|---|---|
| n1 | `KiemTraTrungHoaDonDcgmQuery.java` javadoc `SQL` | Khai *"mỗi nhánh trả đúng **13** cột"* — đếm thật mỗi nhánh **14** cột (có `mau_so_hoa_don_id` mà lớp ngoài không chiếu ra DTO). |
| n2 | Commit `0e931fe4` | Message `create api for dieu chinh gia hang mua` không theo chuẩn `<type>(<scope>): <mô tả>` (luật 8). 46 file trong một commit. |
| n3 | `ChungTuDieuChinhGiaMua.soChungTuPhieuThuChi` + 3 field `null` cứng ở `MapperDieuChinhGiaMua.kemTen` | Cột + trường DTO ship ra API nhưng **luôn `null`** (F12 chưa nối `PhieuThuChiApi`). Hợp đồng API mang trường chết. |

---

## 6. Bốn lớp review

| Lớp | Kết quả |
|---|---|
| **A — Cổng cứng** | Secret: ✅ không có. Controller: ✅ không chứa business logic, không gọi Repository, không trả Entity. Response: ✅ `ApiResponse<T>` / `PageResponse<T>` theo đúng convention base. Lỗi: ✅ ném `ApiException` cho `@RestControllerAdvice`, không try/catch thủ công, không nuốt exception. Vùng đóng băng: ✅ không chạm `master_data/**`. Base package: ✅ `vn.vtt.pmkt`. **Vi phạm: hardcode magic value (m1), nghiệp vụ không nguồn (M6).** |
| **B — Kiến trúc & 7 lỗi** | xem bảng §7 |
| **C — Nghiệp vụ & truy vết** | `trace.sh`: **NOT-RUN** — không có `docs/doing/*06768*-spec/`, epic chưa qua `/audit-spec`. `msg.sh`: **đã chạy**, trả **0 message** ⇒ không có độ phủ message nào để chấm. Không có mã luật `R-…` nào trong diff (`grep -c "R-[0-9]"` → 0), nên không truy vết được luật → code → test. |
| **D — Vệ sinh diff & Git** | Cổng cây commit: ✅ `git status --porcelain` sạch, không file `??` trong `src/`. Không rename bằng `mv` trần. Diff thuần `feat`, không trộn refactor toàn file. ⚠ commit message sai chuẩn (n2). |

---

## 7. Bảng 7 lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục (BE) | ✅ Đạt — 9 file mới đều nằm dưới `internal/` đúng ngăn (`dto/`, `dto/nguon/`, `dto/hoadon/`, `repository/`, `service/`); không tạo `api/` "cho chắc"; `package-info.java` gốc module đã có; controller để package-private; không đổ file phẳng ra gốc module. |
| 2 | Không đánh lại version migration | ⛔ **Blocker B1** — migration thiếu hoàn toàn; số dự kiến V1111 đã bị `V1111__iam_quyen_bieu_mau.sql` chiếm, `max(origin/develop)` = **1122** ⇒ phải bắt đầu từ **V1123**. |
| 3 | Chưa test lại sau merge | ⚠ **M7** — tụt 26 commit, 2 file giao nhau (`FileGroup.java`, `LoaiChungTuChu.java`). |
| 4 | N+1 / chưa tối ưu | ⚠ **M1** — `napNguon` gọi `layNguonDieuChinhGia` trong vòng lặp. Phần còn lại tốt: phân trang ở SQL (`LIMIT/OFFSET`), `laDichVuTheoDong` gom lô, `dinhTuyenTaiKhoan` gom lô, lưới danh sách cố ý **không** nạp tab Hóa đơn để tránh N+1. |
| 5 | Chưa tận dụng base BE | ✅ Đạt — `BaseChungTuController` (bỏ hết 3 override thừa), `AbstractChungTuCrudService`, `ChungTuTemplate` cho Tạo/Sửa/Xóa/GhiSổ/BỏGhiSổ, `BaseChungTuEntity` + `BaseChiTietChungTuEntity`, `QuyenChecker`, `@Searchable`, `SoChungTuApi` qua hook `chungTuDangLuu`, ghi sổ công nợ chỉ qua `SoCongNoApi`. |
| 6 | Chưa tận dụng base FE | N/A — diff không chạm `client/`. |
| 7 | Constant đặt sai chỗ | ⚠ **M4** (mã message không thành hằng, module thiếu `internal/constant/`) + **m1** (magic value trong SQL). |

---

## 8. Lệnh đã chạy

```bash
gh pr view 165 --json ...
git merge-base aab533e7 0e931fe4                        # → c6cb948e
git diff --stat / --name-status c6cb948e 0e931fe4
git log --oneline c6cb948e..0e931fe4
git rev-list --count c6cb948e..origin/develop            # → 26
comm -12 <(git diff --name-only c6cb948e origin/develop|sort) \
         <(git diff --name-only c6cb948e 0e931fe4|sort)   # → 2 file
git ls-tree -r --name-only origin/develop -- src/main/resources/db/migration | ... | tail -1   # → 1122
git ls-tree -r --name-only 0e931fe4      -- src/main/resources/db/migration | grep V111x       # → max V1110
git grep -n "GIAM_GIA_HANG_MUA\|MSG_PMKT-E-06768" 0e931fe4 -- src
git grep -n "sauKhiLuu\|chungTuDangLuu\|soChungTuNguoiDungGo" 0e931fe4 -- .../accounting_core/chung_tu
git status --porcelain                                    # → sạch
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-06768_DieuChinhGiaHangMua be
./docs/rules/br.sh --list ; ./docs/rules/br.sh 7 10
```

**KHÔNG chạy:** `./gradlew unitTest`, `build`, worktree, merge thử, baseline — chế độ nhanh.

## 9. BR đã đọc / chưa đọc

- **Đã đọc:** `--list` (mục lục), **BR7** (làm tròn — dùng cho M3), **BR10** (Trường Chọn nguồn — dùng cho m5).
- **Chưa đọc** (diff có nhắc, chưa đối chiếu nguồn): BR8, BR12, BR16, BR18, BR20, BR29, BR45.
- **BR nội bộ epic** (`BR_Popup_*`, `BR_LuoiCT_*`, `BR_ChietKhau_*`, `BR_QuyDoi_1`, `BR_TongHop_1`, `BR_HoaDon_*`, `BR_Thue_4`, `BR_DanhSach_*`, `BR_Sua_*`): **chưa đối chiếu** — cần mở `pmkt-docs/ba/PMKT-E-06768_DieuChinhGiaHangMua` bằng `scr.sh` ở một lượt riêng.

## 10. Phần chưa đọc kỹ

Đã đọc đầy đủ: controller, 2 lớp native query mới, `DieuChinhGiaMuaSupport`, `CongNoDieuChinhGiaMuaService`, `TinhToanDieuChinhGiaMua`, `MapperDieuChinhGiaMua`, `DieuChinhGiaMuaCrudService`, 5 template business, 2 entity, `LuuDieuChinhGiaMuaRequest`, `TimNguonRequest`, `NguonVaHoaDonSchemaTest`, storage API/adapter/TxOps, `MaChucNang`, `FileGroup`, `LoaiChungTuChu`.

**Chưa đọc chi tiết (chỉ lướt chữ ký):**

- `internal/service/KiemTraDieuChinhGiaMua.java` (+292 dòng) — mới quét danh sách method/`throw`, chưa soi từng luật V01…V30.
- `internal/service/DinhKhoanDieuChinhGiaMua.java` (+82)
- `internal/repository/HoaDonDieuChinhQuery.java` (+68)
- DTO records: `HoaDonDieuChinhDto/Request`, `HoaDonTrungDto`, `KiemTraTrungHoaDonRequest`, `NguonHoaDonTrung`, `ChungTuNguonDto`, `DongNguonDto`, `ChiTietDieuChinhGiaMuaDto`, `DieuChinhGiaMuaDto`
- Thân các file test: `DieuChinhGiaMuaControllerEndpointTest`, `KiemTraDieuChinhGiaMuaTest`, `TinhToanDieuChinhGiaMuaTest`, `DinhKhoanDieuChinhGiaMuaTest`, `CongNoDieuChinhGiaMuaServiceTest`, `MuaHangVongDoiIT`, `LoaiChungTuChuDongBoCheckTest` (đã xác nhận 3 file test mới đều gắn `@Tag("unit")`).

## 11. Kết luận

**REJECT** — B1, B2.
Sau khi xử lý Blocker, vẫn còn **REQUEST CHANGES** vì M1–M7.
M6 cần **BA chốt bằng văn bản** trước khi merge, không phải việc dev tự quyết.

> ⚠ Review chạy ở **chế độ nhanh**: chưa chạy `./gradlew unitTest`, chưa build, chưa merge thử với `develop`. Kết luận đỏ ở B2 rút ra bằng đối chiếu tĩnh (file migration mà test assert `Files.exists` không tồn tại trong cây), không phải từ một lượt chạy test.
>
> **Chưa đăng lên PR** — user yêu cầu rõ không đăng comment.
