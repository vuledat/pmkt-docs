# Review PR #19 — report-service: Báo cáo sổ nhật ký thu/chi tiền

**Chế độ: NHANH** (chỉ đọc + kiểm tĩnh bằng git/grep). KHÔNG chạy test, KHÔNG build, KHÔNG worktree,
KHÔNG sửa code, KHÔNG đăng comment lên PR (user yêu cầu rõ).

| Mục | Giá trị |
|---|---|
| PR | ospgroupvn-pmkt/report-service#19 — "Feat: Báo cáo sổ nhật ký thu/chi tiền" (datnt5920, OPEN) |
| Head | 1a2fe8adb38dcca756edb303760ff27d5fd4d203 (feature/sonhatkythutien) |
| Base | origin/develop = caec7c306deb41b2e060f3d8b344a2e7a6dec29c |
| Merge-base | caec7c30… — trùng base, nhánh KHÔNG tụt |
| Diff | 18 file · +2275 / −899 · 2 commit |
| Working tree | git status --porcelain rỗng — không có file lạc |
| Epic | PMKT-E-10784 (thu tiền) + PMKT-E-10786 (chi tiền) |

## Kết luận

**Không thấy lỗi chặn merge trong phạm vi đã đọc, nhưng có 1 Major cần BA/dev trả lời trước khi merge (M1).**

⚠ **Cổng test/build CHƯA CHẠY** (./gradlew :report-service:build, ./gradlew unitTest). Kết luận này
chỉ dựa trên đọc code + kiểm tĩnh; không phải APPROVE.

| Mức | Số lượng | Mã |
|---|---|---|
| Blocker | 0 | — |
| Major | 1 | M1 |
| Minor | 6 | m1 · m2 · m3 · m4 · m5 · m6 |
| Nit | 5 | n1 · n2 · n3 · n4 · n5 |

---

## Findings

### M1 — Major · Control 3 tham số lệch SCR, và javadoc viện dẫn SCR sai

- **File**: src/main/java/vn/vtt/pmkt/cell/reporting/internal/service/definitions/sonhatkytien/SoNhatKyTienReportDefinition.java:165-203 (khoá P_TAI_KHOAN_ID = "taiKhoanTienId", dòng 73)
- **Nguồn**: pmkt-docs/ba/PMKT-E-10786_SoNhatKyChiTien/5.screens/SCR_SoNhatKyChiTien_ChonThamSo.md
  §"Form thông tin tham số" — Tài khoản = **CombogridSearchTreeGrid**, Loại tiền = **Select**,
  Tài khoản ngân hàng = **CombogridSearchFlatGrid**.
- **Actual**: cả ba khai ReportParamField.Kind.LOOKUP; riêng Tài khoản còn **đổi tên khoá** sang
  taiKhoanTienId (thay vì taiKhoanId như SoCaiReportDefinition.java:61) với javadoc dòng 166-169:
  "hub vẽ khoá taiKhoanId thành bảng chọn một dòng, còn Figma và SCR của báo cáo này là ô Select thường".
- **Expected**: SCR **không** nói "Select thường" cho Tài khoản — nó nói CombogridSearchTreeGrid.
  Javadoc đang trích dẫn sai chính tài liệu nó viện dẫn.
- **Hậu quả**: FE render ô chọn phẳng thay vì cây tài khoản → mất khả năng duyệt cây 111/112 mà BR02
  (màn Chọn tham số) mô tả; và nếu Figma thật sự là Select thì đây là **mâu thuẫn tài liệu chưa chốt**,
  phải mở mục OPEN trong 01-conflict.md để BA quyết, không tự chọn một cách hiểu (CLAUDE.md luật 9 +
  Cổng đặc tả luật 2).
- **Đề xuất**: xin BA chốt bằng văn bản; nếu giữ LOOKUP thì sửa javadoc cho khớp sự thật.

### m1 — Minor · Validate tài khoản ngân hàng bỏ điều kiện "Đang hoạt động"

- **File**: .../internal/repository/SoNhatKyTienRepository.java:111-115 vs :97-108
- **Nguồn**: SCR ChonThamSo BR04 — "Chỉ hiển thị các TK ngân hàng ở trạng thái **Đang hoạt động**".
- **Actual**: taiKhoanNganHangOptions() lọc da_xoa = false AND trang_thai = true, nhưng
  taiKhoanNganHangTonTai(id) chỉ kiểm da_xoa = false.
- **Trigger**: BR05 cho phép pre-fill tham số từ session cũ; TK ngân hàng bị ngừng hoạt động giữa session
  vẫn được gửi lên và **được chấp nhận**, báo cáo lọc theo một TK không còn hợp lệ.
- **Fix**: thêm AND trang_thai = true vào câu đếm.

### m2 — Minor · dataVersion chạy lại toàn bộ phanGiaiBoLoc, lặp ~5 truy vấn danh mục mỗi lần chạy

- **File**: SoNhatKyTienReportDefinition.java:271 (phanGiaiBoLoc(p)) — đã chạy trước đó ở :214.
- Mỗi lần gọi phanGiaiBoLoc kéo: caySoTaiKhoanTien() (CTE đệ quy toàn cây 111/112),
  cayTaiKhoanChiTiet(), loaiTienTonTai(), loaiTienHachToan().
- **Actual**: một lần xem báo cáo chạy bộ này 2 lần (resolveColumns + dataVersion), cộng maxNgayTao.
  Kế hoạch đã chốt nằm sẵn trong NhatKyTienPlan nhưng dataVersion không nhận được ResolvedColumns.
- Kèm theo: phanGiaiBoLoc dùng caySoTaiKhoanTien().stream().filter(...) — load cả cây rồi lọc trong
  Java (checklist-be §E). Cây nhỏ nên tác động thấp; ghi Minor, không phải N+1 theo dòng.

### m3 — Minor · NPE tiềm ẩn khi chungTuId null ở nhánh cộng gộp

- **File**: .../definitions/sonhatkytien/DungDongNhatKyTien.java:144 và :149
- **Actual**: dau.chungTuId().toString() và dau.chungTuId() + "#" + (i+1) không guard null, trong khi
  truongChung (:158) lại guard rõ: d.chungTuId() == null ? null : d.chungTuId().toString().
- **Hậu quả**: hoặc guard ở :158 là code chết (chung_tu_id NOT NULL), hoặc :144 ném NPE khi
  congGop = true. Hai chỗ phải thống nhất.

### m4 — Minor · Text UI tiếng Việt hardcode trong enum thay vì messages.properties

- **File**: .../definitions/sonhatkytien/ChieuTien.java:9,11 — "Ghi nợ TK " / "Ghi có TK ",
  dùng ở SoNhatKyTienReportDefinition.java:242.
- **Nguồn**: CLAUDE.md luật 2. Mọi nhãn khác của báo cáo này đều đi qua khoá i18n trong
  src/main/resources/messages.properties.
- **Hậu quả**: tiêu đề cột tiền không dịch được, không nằm cùng chỗ với 30 khoá còn lại.

### m5 — Minor · Javadoc chết trỏ tới class vừa bị xoá

- **File**: .../internal/repository/PhanBoTheoThangRepository.java:21 — {@link SoNhatKyThuTienRepository}.
- PR xoá SoNhatKyThuTienRepository.java (đổi thành SoNhatKyTienRepository) nhưng không sửa tham chiếu.
  Tên đơn (cùng package) nay không resolve được → javadoc hỏng. Không chặn compileJava.

### m6 — Minor · Chuỗi "----" tồn tại hai nơi, dễ lệch nhau

- **File**: DungDongNhatKyTien.java:37 (NHAN_KHE_TRONG = "----", giá trị trong Ô) và
  messages.properties (soNhatKyThu.ghiCoTrong=----, soNhatKyChi.ghiNoTrong=----, giá trị TIÊU ĐỀ cột).
- **Nguồn**: SCR KetQua BR02 bước 3 — cùng một ký tự "----" cho cả tiêu đề lẫn ô.
- **Hậu quả**: sửa một nơi thì tiêu đề và ô lệch nhau, không test nào bắt.

### n1 — Nit · "111" literal trong khi "112" đã có hằng
SoNhatKyTienReportDefinition.java:176 dùng "111".equals(...) để chọn mặc định, còn GOC_112 là hằng ở :69.

### n2 — Nit · Tham số/hợp đồng overflow của PivotColumns không còn dùng
KHE_OVERFLOW_SUFFIX (:71) vẫn truyền vào PivotColumns.capped(...) (:217), nhưng capped.overflowKey() và
capped.overflowItems() **không được đọc ở đâu** — thiết kế mới thay cột thùng tràn bằng nhóm "các TK khác"
+ tách dòng (đúng BR02 bước 4-5). Javadoc của Capped vẫn yêu cầu caller cộng dồn overflowItems → dễ hiểu nhầm.

### n3 — Nit · Khối khoá i18n của E-10786 nằm dưới header comment của E-10784
messages.properties: 15 khoá soNhatKyChi.* nối ngay sau khối "so-nhat-ky-thu-tien (Story 1.9, E-10784)"
mà không có header riêng cho so-nhat-ky-chi-tien.

### n4 — Nit · So sánh ngayHachToan không null-safe
DungDongNhatKyTien.java:47 — Comparator.comparing(DongNhatKyTien::ngayHachToan) không bọc nullsLast,
trong khi 3 khoá còn lại của TRONG_NGAY đều bọc.

### n5 — Nit · Tên nhánh và phạm vi PR
Nhánh feature/sonhatkythutien nhưng PR mang cả PMKT-E-10786 (chi tiền) + refactor gom lõi chung.
Hai commit đều đúng dạng feat(<scope>): <mô tả>; PR body trống.

---

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả | Ghi chú |
|---|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ | Sub-package service/definitions/sonhatkytien/ theo đúng tiền lệ bangtonghopphatsinh/, sochitiettaikhoan/; class @Component để package-private; base package vn.vtt.pmkt.cell.reporting.* đúng service |
| 2 | Không đánh lại version migration | ✅ N/A | 0 file trong src/main/resources/db/** thay đổi; migration biểu mẫu sẵn có không bị M/D/R |
| 3 | Chưa test lại sau khi merge | ✅ N/A | git rev-list --count caec7c30..origin/develop = **0**; comm -12 giao nhau = **0 file** |
| 4 | N+1 / chưa tối ưu | ⚠ | m2 — lặp truy vấn danh mục hằng số, KHÔNG phải N+1 theo dòng. Ba câu SQL chính đều 1 lượt, dùng chung dieuKienLoc |
| 5 | Chưa tận dụng base BE | ✅ | Dùng ReportDefinition / ResolvedColumns / PivotColumns.capped / ReportDefinitionSupport.periodParams / PeriodLockFingerprint; không tự chế logic sinh khoá cột |
| 6 | Chưa tận dụng base FE | ✅ N/A | Diff không chạm client/ |
| 7 | Constant đặt sai chỗ | ⚠ | m4, m6, n1. Repo này không có internal/constant/; quy ước hiện hành là private static final đầu file — PR theo đúng quy ước đó |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ✅ trừ m4. Không Controller/Entity mới; không secret; không try/catch nuốt lỗi; lỗi nghiệp vụ ném ApiException.badRequest cho handler chung; DI qua constructor; không chạm vùng đóng băng (master_data/**, Phase_2/** không đọc) |
| B — Kiến trúc & 7 lỗi | xem bảng trên |
| C — Nghiệp vụ & truy vết | Xem 2 mục dưới. Hành vi lõi khớp SCR; 1 điểm lệch = M1 |
| D — Vệ sinh diff & Git | ✅ git status sạch, không file ?? trong src/; commit đúng chuẩn; xoá/đổi tên bằng git. n3, n5 |

## Đối chiếu nghiệp vụ (SCR chi tiền — đã đọc trọn 2 file, 272 dòng)

| Luật | Kết quả |
|---|---|
| BR01.a nguồn acc_so_cai, lọc kỳ + TK tiền + vế Nợ/Có | ✅ SoNhatKyTienRepository.dieuKienLoc |
| BR01.a "chứng từ Đã ghi sổ" | ✅ theo quy ước repo — không repository báo cáo nào lọc trạng thái trên acc_so_cai (bảng chỉ chứa bút toán đã ghi sổ) |
| BR01.b Diễn giải: không gộp → DienGiaiDong, gộp → DienGiai | ✅ DungDongNhatKyTien:97 / :133 (có thêm fallback DienGiaiDong → DienGiai, mở rộng nhẹ, vô hại) |
| BR01.c gộp TK cấp con vào 1 cột tiền | ✅ cayTaiKhoanChiTiet nở id, tất cả dồn vào chieu.khoaTien() |
| BR02.a sắp xếp ngày → số CT → thứ tự dòng | ✅ THU_TU_DONG + TRONG_NGAY; giảm dần chỉ đảo ngày (:75-77) |
| BR02.b bước 1-2 gom TK đối ứng, sort chuỗi tăng dần | ✅ ORDER BY tkdu.so_tai_khoan COLLATE "C" |
| BR02.b bước 3 lấy 4 TK đầu, thiếu thì "----" | ✅ PivotColumns.capped(..., CAP=4) luôn trả đủ 4 khe |
| BR02.b bước 4 TH1 (không gộp) mỗi bút toán 1 dòng | ✅ cumRoi |
| BR02.b bước 4 TH2 (gộp) gộp cùng TK Nợ/Có trong 1 chứng từ, TK ngoài 4 cột tách dòng từ cái thứ 2 | ✅ cumGop:113-150 |
| BR02 bước 5 dòng đầu = tổng cột trên dòng; dòng tách = số tiền TK khác | ✅ :134-148, có test batBienGhiNoBangTongCacCotCoTrenTungDongVaTongPhatSinh |
| BR02 bước 6 dòng tách lặp ngày/số hiệu/diễn giải, 4 cột động trống | ✅ truongChung gọi lại cho dòng tách |
| BR03 click Số hiệu mở chứng từ | ✅ ReportColumnLink.Kind.DOC + chungTuId + maLoaiChungTu (2 cột ẩn) |
| BR04 (KetQua) không dữ liệu → không có tổng cuối bảng | ✅ if (!rows.isEmpty()) bao quanh totals |
| BR04 (ChonThamSo) TK ngân hàng chỉ áp dụng khi TK thuộc cây 112 | ✅ :299; ⚠ m1 về trạng thái hoạt động |
| Tổng cuối bảng cộng 3 nhóm cột tiền | ✅ :81-90 |
| Control tham số | ⚠ **M1** |

## Truy vết & cổng

| Cổng | Kết quả |
|---|---|
| trace.sh | **NOT-RUN** — không có docs/doing/*-spec/ cho PMKT-E-10784 / 10786 (chưa chạy /audit-spec). Không đoán bừa spec khác |
| msg.sh … be | **Không áp dụng** — script hardcode phạm vi quét cell-app/src và client/src (docs/rules/msg.sh:30-32), không quét report-service/. Kết quả "THIEU 4" là dương tính giả |
| Message của 2 epic | 4+7 mã đều là thông báo chung của hub (quyền, Từ/Đến ngày, không có dữ liệu, xuất Excel). Definition đã khai permission() và ReportParamRule.dateOrder(...); hợp đồng ReportDefinition chỉ có MỘT permission(), không có hook quyền Export ở bất kỳ definition nào → không phải thiếu sót riêng của PR này |
| br.sh (BR chung) | **Không chạy** — BR01…BR05 trong hai file SCR_* là BR nội bộ màn, không phải business_rules.md. BR chung duy nhất được trích chéo là BR8 (khoảng thời gian) → do ReportDefinitionSupport.periodParams xử lý dùng chung, không đổi trong PR |
| ./gradlew :report-service:build | **NOT-RUN — chế độ nhanh** |
| ./gradlew unitTest | **NOT-RUN — chế độ nhanh**. 3 test class mới đều gắn @Tag("unit"): DungDongNhatKyTienTest (18 case), SoNhatKyThuTienReportDefinitionTest (17), SoNhatKyChiTienReportDefinitionTest |
| E2E | SoNhatKyThuTienE2eTest / SoNhatKyChiTienE2eTest extend AbstractReportE2eTest → **Testcontainers, KHÔNG chạy được trên máy này (không Docker)** |

**Coverage test không thụt lùi**: 14 case của SoNhatKyThuTienReportDefinitionTest cũ (bị xoá) đều có case
tương đương ở 2 file mới, trừ overflowTotalEqualsGrandTotalMinusTheFourNamedColumns — case này mất theo
thiết kế cũ (cột thùng tràn) mà BR02 bước 4-5 đã thay bằng nhóm "các TK khác" + tách dòng; đã có
gopPT0001TachHaiDongVaGhiNoDongDauGomTkKhacDauTien và tkKhacXepTheoMaChuoiDuDauVaoDao phủ.

## Lệnh đã chạy

- gh pr view 19 --json number,title,headRefName,baseRefName,headRefOid,state,author,body
- git merge-base origin/develop 1a2fe8ad  → caec7c30 (= origin/develop)
- git diff --stat / --name-status caec7c30 1a2fe8ad
- git rev-list --count caec7c30..origin/develop  → 0
- comm -12 (diff base..develop) (diff base..head)  → rỗng
- git status --porcelain  → rỗng
- git show 1a2fe8ad:<path>  → đọc 6 file main + 3 file test ở head
- git grep -n <ký hiệu> 1a2fe8ad -- src/main  → tìm caller / tiền lệ / tham chiếu chết
- ./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-10784_SoNhatKyThuTien be
- ./docs/rules/scr.sh <SCR> --stat

## Phần chưa đọc

- src/test/java/.../e2e/SoNhatKyThuTienE2eTest.java (diff sửa), SoNhatKyChiTienE2eTest.java — mới đọc
  danh sách case và tag, chưa soi assert từng case.
- SoNhatKyChiTienReportDefinitionTest.java — chỉ đọc danh sách case (bản gương của test thu tiền).
- SCR của PMKT-E-10784 (thu tiền) — đối chiếu qua SCR chi tiền vì hai BA là ảnh gương.
- 4.usecases/** và Matrix/** của cả hai epic.
- Figma (không truy cập được) — liên quan trực tiếp tới M1.

**Chưa đăng lên PR — user yêu cầu chỉ ghi file, không comment.**
