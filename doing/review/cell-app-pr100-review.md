# Review PR #100 — cell-app → develop

| | |
|---|---|
| Repo | `cell-app` |
| Nguồn | PR #100, ref review `review/pr-100` (đỉnh `5faab0fb`) |
| Nhánh đích | `develop` — merge-base `04d04b840f25f97122bafd6f50e4a40abda360d8` (= đỉnh `origin/develop`, độ tụt **0 commit**, file giao nhau: **không có**) |
| Ngày review | 2026-09-06 |
| Phạm vi | ~230 file thay đổi: cụm `tien_mat_tien_gui` (phiếu thu/chi TM·TG, chuyển tiền nội bộ, in Jasper, hàng loạt), `so_cong_no` (đường đọc + đối trừ), `ban_hang/chung_tu_ban_hang` (phiếu thu kiêm — Thu tiền ngay), `hoa_don_mua` (export), migration V1092–V1093, 19 mẫu in `.jrxml` + font |
| Chế độ | CHỈ ĐỌC — không sửa code, không commit, không comment GitHub |

## KẾT LUẬN: ❌ REJECT

Căn cứ: **2 BLOCKER** (code vào luật đang bị mục OPEN P0 chặn + tự đặt luật nghiệp vụ không nguồn),
kèm **7 MAJOR**. Cổng `unitTest` đỏ nhưng **cả 2 test fail đều là lỗi nền có sẵn trên develop**
(tái hiện nguyên văn tại merge-base) — không tính cho diff; REJECT đến từ findings, không từ cổng test.

---

## 1. Cổng kiểm chứng (số liệu dán từ agent test — không suy diễn thêm)

### 1.1 unitTest

- `./gradlew unitTest` trên worktree `review/pr-100`: **3556 tests, 2 failed, 2 skipped — BUILD FAILED in 3m 40s**.
- Baseline merge-base `04d04b84` (chạy đúng 2 test class fail): **cả 2 fail y hệt** — lỗi NỀN, không quy cho diff:
  1. `LoaiChungTuChuDongBoCheckTest.enum_va_check_constraint_khop_nhau` — whitelist SQL thiếu `CASH_CHUYEN_TIEN_NOI_BO` so với enum; enum baseline ĐÃ có giá trị này từ trước, diff chỉ đổi tên hằng `MaChucNang`, chênh lệch expected/actual trùng tuyệt đối giữa hai ref.
  2. `HoaDonMuaControllerPermissionTest.luuVaGhiSoYeuCauThemQuyenPost` — Mockito WantedButNotInvoked, message fail giống từng chữ trên baseline.
- `loi_do_diff`: **rỗng**. 2 skipped là trạng thái bình thường của bộ unitTest.
- Testcontainers / `./gradlew build`: **KHÔNG chạy** (cấm Docker theo CLAUDE.md).

### 1.2 Test sau merge

**KHÔNG ÁP DỤNG** — `git rev-list --left-right --count review/pr-100...origin/develop` = `135 0`
(nhánh đi trước 135 commit, `origin/develop` là tổ tiên), file giao nhau `[]`. Migration không đụng
số: develop max V1091, nhánh thêm V1092–V1093.

### 1.3 trace.sh / msg.sh

- `trace.sh docs/doing/PMKT-E-06194-chung-tu-ban-hang-spec be`: **0 OK · 86 MISSING · 7 BLOCKED → CHƯA ĐẠT**.
  Hạn chế đo: trace.sh quét working tree đang ở nhánh khác (`feat/chung-tu-ban-hang-2`); kết luận
  then chốt được kiểm lại trực tiếp trên ref: `git grep "R-CTBH" review/pr-100` = **0 kết quả**
  (merge-base cũng 0 → phần lớn MISSING là baseline; finding chỉ tính phần luật mà code MỚI của PR hiện thực).
- 4 epic thu/chi (PMKT-E-06219/06220/06222/06223): **không có thư mục spec** trong `docs/doing` →
  trace.sh/msg.sh **không chạy được** cho phần chiếm đa số diff (xem finding MAJOR-3). Bù bằng soát
  tay: bộ hằng `MaLoiTienMat`/`MaLoiTheoLoai` mang mã `MSG_PMKT-E-06219/06220` đúng khuôn.

---

## 2. Findings

### BLOCKER (2)

**B-1 · Code vào luật đang bị OPEN P0 chặn — cascade xóa phiếu thu kiêm**
`src/main/java/vn/vtt/pmkt/cell/ban_hang/chung_tu_ban_hang/internal/service/business/XoaChungTuBanHang.java:109`
Diff thêm `bh.chungTuCon().xoaPhieuThu(ct)` — cascade xóa mềm phiếu thu kiêm khi xóa CTBH. Đây là
hiện thực R-CTBH-089 (trạng thái CHỜ C05) và ngầm chốt C03/C04 (R-CTBH-088) theo phương án A trong
khi **C03, C04, C05 đều đang OPEN P0** trong `01-conflict.md` (chưa có tên người + ngày chốt của BA).
*Hậu quả*: BA chốt phương án khác (chặn xóa khi có phiếu thu / chặn theo counter) → mọi chứng từ
ThuTienNgay=True đã xóa kèm phiếu thu trong lúc chờ chốt là dữ liệu xóa sai, không khôi phục được
về nghiệp vụ.
*Nguồn*: CLAUDE.md §Cổng đặc tả luật 1 + `docs/doing/PMKT-E-06194-chung-tu-ban-hang-spec/01-conflict.md`
C03·C04·C05 (OPEN P0) + `02-rules.md` R-CTBH-088/089 (CHỜ).

**B-2 · Tự đặt luật nghiệp vụ không nguồn — định khoản Mục đích thu phiếu kiêm**
`src/main/java/vn/vtt/pmkt/cell/ban_hang/chung_tu_ban_hang/internal/service/business/ChungTuConBanHang.java:253`
`dinhKhoanThuTienNgay` javadoc tự nhận "BA không khai ô Mục đích thu cho phiếu kiêm" rồi tự quyết:
(a) tra bộ seed tài khoản ngầm định theo tình huống `thuTienNgay·loaiNghiepVu·hinhThucThanhToan`,
(b) bán dịch vụ tra theo mã cứng `"BDV"`, (c) không tìm thấy thì để null và không chặn lưu. Không
mở mục OPEN trong `01-conflict.md` để hỏi BA.
*Hậu quả*: ô Mục đích thu của mọi phiếu thu kiêm điền theo quy tắc dev tự nghĩ; BA chốt khác thì
dữ liệu phiếu đã lập mang định khoản sai hàng loạt, không luật nào truy vết được.
*Nguồn*: CLAUDE.md luật 9 + §Cổng đặc tả luật 2.

### MAJOR (7)

**M-1 · Thuật toán phân bổ dòng âm tự đặt, phần âm khác TK bị nuốt im lặng**
`.../ban_hang/chung_tu_ban_hang/internal/service/business/ChungTuConBanHang.java:293`
`dongPhaiThu`: dòng phải thu âm (CKTM/KM) "trừ vào các dòng dương cùng TK công nợ theo thứ tự dòng" —
quy tắc khớp-theo-TK-và-FIFO không BR/spec nào quy định; phần âm thuộc TK không có dòng dương cùng
TK bị bỏ qua im lặng (map `giamTru` không bao giờ được áp).
*Hậu quả*: ca CKTM/KM mang TK công nợ khác các dòng hàng → phiếu thu kiêm VƯỢT số khách thực phải
trả đúng bằng phần giảm trừ, TK 131 dư Có sau ghi sổ; cách chia theo dòng quyết định số liệu đối trừ
trên `map_phieu_thu_chung_tu_ban`.
*Nguồn*: CLAUDE.md luật 9 + §Cổng đặc tả luật 2.

**M-2 · Không để lại mã R-CTBH trong code lẫn test — truy vết không đếm được**
`.../ChungTuConBanHang.java:119` (đại diện cụm)
Code mới hiện thực các luật ĐÃ CHỐT (R-CTBH-065/066/067, 080, 097, 104/106) nhưng
`git grep "R-CTBH" review/pr-100` = 0; chỉ ghi "BR18 §1 + §6", "BR21 §3" kiểu cũ.
trace.sh be = 0 OK · 86 MISSING · 7 BLOCKED → CHƯA ĐẠT.
*Hậu quả*: MISSING = luật tính là chưa hiện thực bất kể code trông đúng; bảng truy vết
Rule→Code→Test không lập được bằng lệnh, /verify-spec chấm rớt toàn bộ phần phiếu thu kiêm.
*Nguồn*: `docs/rules/truy-vet-luat.md` §1–§3 + CLAUDE.md §Cổng đặc tả luật 3 + §Truy vết phải đếm được.

**M-3 · 4 epic thu/chi không có spec — cổng /audit-spec bị bỏ qua cho phần đa số diff**
`.../tien_mat_tien_gui/internal/service/business/LuuPhieuThuChiTemplate.java:1` (đại diện cụm)
PMKT-E-06219/06220/06222/06223 không có thư mục `*-spec` trong `docs/doing` (chỉ 06194 có).
Không chạy được trace.sh; truy vết chỉ tồn tại dạng comment trích BA, không đếm được. Không có
`01-conflict.md` nên ≥5 chỗ code tự nhận "BA không khai / BA chưa khai" không có sổ mâu thuẫn để BA chốt.
*Nguồn*: CLAUDE.md §Cổng đặc tả ("Thư mục spec chưa tồn tại → chạy /audit-spec trước") + luật cổng 3.

**M-4 · Mã lỗi tự bịa + text tiếng Việt hardcode không mang mã MSG**
`.../ban_hang/chung_tu_ban_hang/internal/service/CongNoBanHangService.java:88`
`ApiException` với mã tự bịa `"THIEU_KHACH_HANG"` + nguyên văn "Chế độ thu từ MỘT đối tượng phải
chọn đúng một khách hàng (BR01)." — không mang mã `MSG_PMKT-E-xxxxx_nnn` từ 6.messages.md. Chính
javadoc `MaLoiTienMat.java` trong PR gọi khuôn tương tự là "tiền lệ" tạo mã FE không tra được.
*Hậu quả*: msg.sh chấm THIEU/LECH; FE không có key i18n đối chiếu.
*Nguồn*: `docs/rules/truy-vet-luat.md` + CLAUDE.md §Truy vết + luật 2.

**M-5 · Export Excel lệch BR39 ở 4 điểm, không ghi lý do**
`.../hoa_don_mua/internal/controller/HoaDonMuaExportController.java:63`
(1) `tieuDe=null` → thiếu dòng Tên báo cáo + tham số lọc (BR39.3); (2) tên file cố định
`hoa-don-mua.xlsx` thiếu `[Ngày xuất]_[Giờ xuất]` (BR39.4, dòng 64); (3) 12 cột cố định server,
không theo cột đang hiển thị/thứ tự grid (BR39.1); (4) không có dòng Tổng cộng (BR39.5).
*Nguồn*: business_rules.md BR39.1/39.3/39.4/39.5 (`./docs/rules/br.sh 39`).

**M-6 · kiemTraLock gắn cứng messageId của epic 06223 cho MỌI loại phiếu** *(lỗi hay gặp #7)*
`.../tien_mat_tien_gui/internal/service/business/PhieuThuChiSupport.java:210`
`kiemTraLock()` dùng `MaLoiTienGui.MSG_CHI_TG_LOI_HE_THONG` (MSG_PMKT-E-06223_305) cho cả 5 loại
(gọi từ `SuaPhieuThuTienMat.java:41`, `SuaPhieuChiTienMat.java:35`, `SuaGiayBaoCo.java:35`,
`XoaPhieuThuChi.java:83`…). Bảng `MaLoiTheoLoai` đã khai `loiHeThong` đúng theo epic cho ca
STALE_DATA (javadoc `MaLoiTheoLoai.java:34-36`); chính class này đã sửa cùng lỗi cho `khongTonTai`
nhưng bỏ sót `kiemTraLock`.
*Hậu quả*: 409 STALE_DATA khi sửa/xoá phiếu thu tiền mặt (epic 06219) mang messageId epic 06223 —
FE tra 6.messages.md epic mình không ra, msg.sh chấm LECH.
*Nguồn*: checklist-be.md §F + CLAUDE.md §Truy vết.

**M-7 · Literal `"CHUA_HO_TRO"` thay vì hằng đã có** *(lỗi hay gặp #7)*
`.../tien_mat_tien_gui/internal/service/business/HachToanPhieuKiem.java:96`
`ApiException.badRequest("CHUA_HO_TRO", …)` bằng string literal trong khi mã đã là hằng
(`MaLoiTienMat.CHUA_HO_TRO` / `MaLoiTienGui.CHUA_HO_TRO`) và cùng giá trị đã dùng ở
`ChungTuThuChiCrudService#chuaHoTro`. Mã máy đọc dùng từ ≥2 file phải tham chiếu hằng.
*Nguồn*: checklist-be.md §F.

### MINOR (8)

**m-1** · `.../tien_mat_tien_gui/api/PhieuThuChiApi.java:34` — javadoc tự nhận "BA chưa khai người
lập chứng từ bán/mua có cần quyền lập phiếu thu/chi không" và tự chốt phương án bảo thủ (vẫn kiểm
`ThuTienTM.Create`…); có ghi "finding bàn giao" nhưng không có mục OPEN trong sổ mâu thuẫn.
Người có `BanHangHoa.Create` thiếu `ThuTienTM.Create` sẽ không lưu được chứng từ tick Thu tiền ngay.
*Nguồn*: CLAUDE.md luật 9 + §Cổng đặc tả luật 2; BR25.

**m-2** · `.../tien_mat_tien_gui/internal/model/LoaiPhieuThuChi.java:172` — PTTT mặc định do server
tự điền cho cột NOT NULL (phiếu chi TG thật ra có 4 PTTT hợp lệ); tương tự diễn giải mặc định
"Thu tiền"/"Chi tiền" hardcode ở `HachToanPhieuKiem.java:54`. Đã ghi chú rõ, user sửa được → MINOR.
*Nguồn*: CLAUDE.md luật 9 + §Cổng đặc tả luật 2.

**m-3** · `.../tien_mat_tien_gui/internal/service/business/GhiSoCongNoThuChi.java:411` *(lỗi hay gặp #4 — N+1)* —
`ghiNhanDoiTruDichDanh()` gọi trong vòng `while` của `ganTuan()` (404–419); mỗi lời gọi chạy 3 SQL
(SELECT FOR UPDATE + SUM + INSERT) ⇒ ~3×(số dòng đối trừ) truy vấn/transaction, dù dòng 116–120 đã
tra sẵn toàn bộ dòng gốc theo lô và `SoCongNoService.taoPhanBo` (249–296) có sẵn khuôn theo lô.
Lý do lệch ĐÃ ghi trong code (dòng 115) → hạ MAJOR→MINOR theo quy tắc ánh xạ mức.
*Nguồn*: checklist-be.md §E.

**m-4** · `.../tien_mat_tien_gui/internal/constant/MaLoiTienMat.java:27` *(lỗi hay gặp #7)* —
`CHUA_HO_TRO` và `KHONG_TIM_THAY = "NOT_FOUND"` (dòng 29) trùng giá trị với `MaLoiTienGui.java:26,28`
— copy sang file thứ hai thay vì đặt ở `MaLoiChung` cùng thư mục. Hệ quả đã lộ: service phục vụ cả
tiền mặt import `MaLoiTienGui.KHONG_TIM_THAY` (`PhieuThuChiSupport.java:224`,
`DieuHuongGhiTheoLoai.java:182`, `PhieuKiemService.java:389`) còn `ChungTuTienMatCrudService.java:65`
dùng `MaLoiTienMat.KHONG_TIM_THAY` — hai nguồn sự thật một mã.
*Nguồn*: checklist-be.md §F.

**m-5** · `.../tien_mat_tien_gui/internal/service/HangLoatTronThuChiService.java:43` *(lỗi hay gặp #7)* —
chép `"MSG_002"` (+ nguyên văn câu 403 dòng 111, `"SYSTEM_ERROR"`/`"FORBIDDEN"` dòng 41–42) từ
`GlobalExceptionHandler` của core sang hằng private module. Javadoc có ghi lý do → MINOR; gốc là
core chưa phơi hằng MSG_002 — nên phơi rồi tham chiếu.
*Nguồn*: checklist-be.md §F + ánh xạ mức "NÊN mà lệch CÓ ghi lý do".

**m-6** · `.../tien_mat_tien_gui/internal/constant/MaLoiChung.java:17` *(lỗi hay gặp #7)* —
`MSG_TRANG_THAI_KHONG_HOP_LE = "MSG_COMMON_001"` trùng `MaLoiDieuChinhGia.MSG_COMMON_001` của module
`ban_hang/dieu_chinh_gia_hang_ban` — mã BR16.1 dùng ≥2 module thuộc core/shared-kernel. Javadoc có
lý do ("core chưa có nơi khai MSG_COMMON_*") → MINOR; đề nghị mở chỗ khai chung ở core.
*Nguồn*: checklist-be.md §F.

**m-7** · `src/main/resources/db/migration/V1092__ngan_quy_thu_chi_va_so_cong_no.sql:62` *(lỗi hay gặp #2)* —
sau 5 đợt đánh lại số, nội dung vẫn giữ số hiệu cũ: `RAISE EXCEPTION 'V1058 ①: tenant…'` (62),
comment "V1058 chỉ thêm cặp…" (351), "đã DROP ở V1062" (415 — DROP thực nằm ngay trong file này),
"Xem ① của V1089" (434). Trên develop các số này thuộc migration khác hẳn (V1058=ccdc_phan_bo,
V1062=iam_tenant_number_format, V1089=sal_hdbh). Migration fail sẽ báo mã "V1058" trong khi Flyway
chạy V1092 — ops tra nhầm.
*Nguồn*: checklist-be.md §C lỗi hay gặp #2.

**m-8** · `src/main/resources/db/migration/V1093__quyen_ngan_quy.sql:68` *(lỗi hay gặp #2)* —
heading "V1059 — Quyền ngân quỹ" (7), "V1060 — Gỡ mã quyền CẤP MÀN" (264); nghiêm trọng hơn, chuỗi
`[TẠM — ngoài BA, V1059]` và "V1059: suy từ …" được **ghi vào dữ liệu** cột `iam_quyen.mo_ta`
(68, 204) rồi dùng làm khoá DELETE (319). Trên develop V1059/V1060 là migration khác hẳn nội dung.
*Nguồn*: checklist-be.md §C lỗi hay gặp #2.

### NIT (6)

**n-1** · `.../tien_mat_tien_gui/package-info.java:38-45` — javadoc module (thêm trong chính PR) mô
tả mô hình quyền ĐÃ GỠ (mã gộp TienMat.*/TienGui.* cấp màn), trong khi `MaChucNang.java` cùng PR
ghi "BA chốt 2026-08-24: bỏ hẳn mã GỘP" và hai controller màn gác AND đủ bộ mã theo loại. Người sau
đọc dễ "hồi sinh" mã đã gỡ — đúng bẫy 403 mà comment `MaChucNang` cảnh báo. Không có luật repo về
độ chính xác javadoc → NIT.

**n-2** · `.../ban_hang/chung_tu_ban_hang/internal/controller/ChungTuBanHangController.java:89` —
`@org.springframework.web.bind.annotation.RequestBody` inline thay vì import như toàn bộ file/cụm.
Không trích được rule nguồn cho style import → NIT.

**n-3** · `.../tien_mat_tien_gui/internal/service/business/SuaChuyenTienNoiBo.java:50` *(lỗi hay gặp #7, gián tiếp)* —
guard "đã ghi sổ không sửa" gọi thẳng `MaLoiTienGui.MSG_CTNB_DA_GHI_SO_KHONG_XOA` thay vì tra bảng
`loai().maLoi().daGhiSoKhongSua()` như 4 lớp `Sua*` anh em; `GhiSoChuyenTienNoiBo.java:50` tương tự.
Ngày BA cấp mã _sửa riêng cho CTNB, cập nhật enum là không đủ.

**n-4** · `src/main/resources/db/migration/V1093__quyen_ngan_quy.sql:1` *(lỗi hay gặp #2, nhẹ)* —
tên file không mang `<prefix>` bảng theo chuẩn `V<max+1>__<prefix>_<mo_ta>.sql`: V1093 thao tác toàn
bảng `iam_*` nhưng tên "quyen_ngan_quy"; V1092 chạm `cash_`/`map_` nhưng tên
"ngan_quy_thu_chi_va_so_cong_no". Develop có tiền lệ lệch (V1049) → NIT.

**n-5** · `src/main/resources/db/seed/20_loai_chung_tu.sql:13` — thêm dòng `CTNB` nhưng file vẫn giữ
mã `BCTG`/`BNTG` (11–12) đã lạc hậu so với bộ chuẩn BA `GBC`/`PCTG` — chính PR khai điều này trong
javadoc `LoaiPhieuThuChi.java:26-28`. Môi trường dựng mới không chạy đủ V1032 → mã code tra không
khớp, module thu/chi TG hỏng im lặng.
*Nguồn*: checklist-be.md §C (đồng bộ dữ liệu nền với code).

**n-6** · Vệ sinh commit — `842c6a90 merge: develop (5 commit)` dùng type `merge` tự chế; scope
không thống nhất cho cùng vùng code qua 60 commit (thu-chi / tien_mat_tien_gui / tien-mat-tien-gui /
ngan_quy; banHang / ban_hang / ban-hang; cong-no / so-cong-no / so_cong_no). Các commit còn lại đạt
định dạng, không commit thẳng develop/master.
*Nguồn*: CLAUDE.md luật 8 (luật không quy định từ vựng scope → không nâng mức).

---

## 3. Bảng 7 lỗi hay gặp (rà từng mục — bắt buộc)

| # | Lỗi hay gặp | Kết quả | Bằng chứng / finding |
|---|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ không vi phạm | 0 import xuyên module vào `.internal.` khác; `api/` + `api/dto/` của `tien_mat_tien_gui` đều có `package-info` `@NamedInterface`; không file phẳng ra gốc module; `internal/chi_nhanh/` theo pattern có sẵn |
| 2 | Không đánh lại version migration | ⚠ cổng cứng ĐẠT, nội văn ❌ | Số version đúng: V1092/V1093 > max develop (V1091), không trùng, không sửa migration đã merge, squash 9→2 trước merge đúng quy trình. NHƯNG tham chiếu nội văn giữ số 2 đời trước, kể cả ghi vào dữ liệu `iam_quyen.mo_ta` → **m-7, m-8, n-4** |
| 3 | Chưa test lại sau merge | ✅ N/A | Độ tụt = 0 (merge-base = đỉnh origin/develop), file giao nhau `[]` → không cần merge thử; max migration cây kết quả 1093, không đụng độ |
| 4 | Code chưa tối ưu / N+1 | ❌ 1 MINOR | **m-3** (`GhiSoCongNoThuChi:411` — 3 SQL/lệnh đối trừ trong vòng lặp; hạ mức vì lý do ghi trong code). Còn lại sạch: không `FetchType.EAGER` mới, tab chi tiết/lưu/export tra theo lô, entity mới không khai quan hệ JPA |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ không vi phạm | Mọi controller/entity/repo mới extend đúng base (`BaseChungTuThuChiController`→`BaseChungTuController`; `SoftDeletableEntity`/`BaseChungTuEntity`/`BaseChiTietChungTuEntity`; `BaseRepository`); chứng từ qua `ChungTuTemplate`, ghi sổ chỉ qua `hach_toan.api.GhiSoApi`. `HoaDonMuaExportController` không extend base export nhưng base không phủ được lưới lọc bằng `TimKiemRequest` riêng — chấp nhận |
| 6 | Chưa tận dụng base FE | — N/A | Diff thuần BE, không chạm `client/` |
| 7 | Constant đặt sai chỗ | ❌ 2 MAJOR + 3 MINOR + 1 NIT | **M-6** (messageId sai epic), **M-7** (literal `CHUA_HO_TRO`), **m-4** (trùng giá trị 2 file), **m-5** (copy MSG_002 từ core), **m-6** (MSG_COMMON_001 nhân bản liên module), **n-3** (gọi thẳng hằng vòng qua bảng loại). Điểm cộng: 4 file `MaLoi*` đặt đúng `internal/constant/`, mọi mã `MSG_PMKT-E-*` là hằng public, bộ mã theo loại có test pin |

---

## 4. BR đã đối chiếu (qua `br.sh`, bản Phase 1)

1, 2, 4, 7, 9, 11, 12, 13, 16, 17, 18, 19, 20, 21, 25, 26, 27, 28, 29, 30, 31, 32, 33, 36, 37, 38,
39, 41, 42, 44, 45, 46, 48, 49. Kết quả: lệch BR39 (→ M-5); seed `CTNB` ĐÃ có trong danh mục 47 loại
Phase 1 (`DuLieuKhoiTao_LoaiChungTu.md` dòng 42 — không phải finding).

## 5. Lệnh thực sự đã chạy

```
git diff 04d04b84..review/pr-100 -- <lát cắt>          (5 lát cắt song song)
./docs/rules/br.sh <34 BR>                              → OK
./docs/rules/trace.sh docs/doing/PMKT-E-06194-...-spec be → 0 OK · 86 MISSING · 7 BLOCKED
git grep "R-CTBH" review/pr-100                         → 0 (merge-base cũng 0)
git worktree add ../review-test-pr100 review/pr-100
git rev-list --left-right --count review/pr-100...origin/develop → 135  0
./gradlew unitTest (worktree PR)                        → 3556 tests, 2 failed, 2 skipped, FAILED 3m40s
git worktree add ../review-test-pr100-base 04d04b84
./gradlew unitTest --tests <2 class fail> (baseline)    → cả 2 fail y hệt
git worktree remove ×2 --force
```

## 6. Phần chưa đọc / chưa kiểm — khai trung thực

- **msg.sh chưa chạy** cho 4 epic thu/chi (không có spec/PYC được giao + working tree ở nhánh khác) — bù soát tay bộ hằng MSG.
- **Testcontainers / `./gradlew build` không chạy** (cấm Docker) — phần integration test phụ thuộc DB thật chưa kiểm.
- **Không chạy app/DB để đo SQL thật** — kết luận N+1 dựa đọc code + checklist §E.
- Không đọc plan (`docs/doing/*-api`, `*-fe`), IMPLEMENT.md, `Phase_2/**`, vùng đóng băng.
- Không kiểm được "?? chưa git add" của working tree tác giả — review trên ref đã commit, mọi file diff nằm trong cây commit.
- Nội dung `.jrxml`/font: đã có test pin (`MauInJrxmlTest`, `MauInKhopFileBaTest`, `SpikeJasperTiengVietTest` + 19 file `.txt` đối chiếu) — không review pixel mẫu in.

## 7. Ghi chú riêng cho user (ngoài findings)

- PR **chạm vùng đóng băng `master_data`**: thêm `master_data/tai_khoan_ngam_dinh/api/dto/package-info.java`
  (khai `@NamedInterface` hợp thức ranh giới, có arch test `TaiKhoanNgamDinhApiRanhGioiTest` ghim).
  Thuộc đúng ngoại lệ "API công khai của module đóng băng", nhưng CLAUDE.md yêu cầu **báo rõ với user**
  khi chạm vùng này — không xác minh được việc báo từ diff, ghi nhận để user đối chiếu.
- Phụ thuộc vòng `ban_hang ↔ tien_mat_tien_gui` được khai kèm lý do trong `api/package-info`;
  `ProxyModularityTest` lọc mọi thông báo Cycle nên không đỏ — nên có quyết định kiến trúc chính thức.
- 2 test nền đỏ trên develop (`LoaiChungTuChuDongBoCheckTest`, `HoaDonMuaControllerPermissionTest`)
  cần ticket riêng — không thuộc PR này.

## 8. Việc phải làm để mở lại PR (tối thiểu)

1. **B-1**: gỡ hoặc gác cascade xóa phiếu thu kiêm sau khi BA chốt C03/C04/C05 (có tên + ngày trong `01-conflict.md`).
2. **B-2, M-1**: mở mục OPEN trong `01-conflict.md` cho quy tắc định khoản Mục đích thu + phân bổ dòng âm; chờ BA chốt.
3. **M-2**: gắn mã `R-CTBH-xxx` vào code + tên test cho các luật đã chốt; chạy lại trace.sh đến khi phần luật của PR hết MISSING.
4. **M-3**: chạy `/audit-spec` cho 4 epic thu/chi (hoặc user xác nhận miễn cổng — ghi rõ).
5. **M-4→M-7**: thay mã tự bịa bằng mã MSG chuẩn, sửa messageId theo bảng loại, tham chiếu hằng thay literal, bổ sung BR39 cho export.
6. m-7/m-8: sửa tham chiếu nội văn V1058/V1059/V1060/V1062/V1089 → số hiện hành (V1093 cần cả chiến lược cho chuỗi đã thiết kế ghi vào `iam_quyen.mo_ta`).

---
*Review bởi Claude Code (review-code-fanout, 5 lát cắt + cổng test + vòng phản biện). CHỈ ĐỌC — không sửa code, không comment GitHub.*
