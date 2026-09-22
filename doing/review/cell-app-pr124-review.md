# Review cell-app PR #124 — ngân quỹ thu/chi: phiếu kiêm theo dòng hàng (V1099)

- **Chế độ**: **SÂU**. Lý do: diff chạm migration (`V1099`) — điều kiện bắt buộc chế độ sâu.
- **Phạm vi nghiệp vụ**: user yêu cầu **không check nghiệp vụ** ⇒ bỏ đối chiếu BR / `trace.sh` / `msg.sh`.
  Không có thư mục `docs/doing/*-spec` cho epic ngân quỹ thu/chi nên hai cổng đó cũng không có đầu vào.

## 1. Phạm vi đã khoanh

| Mục | Giá trị |
|---|---|
| PR | `https://github.com/ospgroupvn-pmkt/cell-app/pull/124` |
| Head SHA | `01c01505175826a0c943f7513a38f717cfae50c0` |
| Nhánh head | `origin/feature/thuchimodulemua` |
| Base (xác minh) | `origin/develop` = `cfc18545cd29f47f34bba835a29faa8efb7e0c7f` |
| Merge-base | `cfc18545…` — **bằng đúng tip develop**, nhánh KHÔNG tụt, không cần merge thử |
| Commit | 1 · `feat(thu-chi): ngân quỹ thu/chi — phiếu kiêm theo dòng hàng (vat_tu_id V1099), sửa phiếu kiêm từ màn tiền, TTTHD, trạng thái thanh toán theo nguyên tệ` |
| Quy mô | 64 file · +673 / −210 |
| Vùng đóng băng | 0 file rơi vào `master_data/**` — không phải loại trừ gì |
| Working tree khi review | worktree detached riêng, sạch |

`gh` không có trên máy ⇒ head lấy bằng `git fetch origin refs/pull/124/head` vào ref tạm
`refs/pmkt-review/cellapp-pr124`; base suy từ merge-base trùng đúng tip `develop` (đã xác minh
`master` cho merge-base cũ hơn 163 commit nên không phải hotfix).

## 2. Findings

### 🟠 Major 1 — Đổi **phương thức thanh toán** trong cùng tiền gửi vẫn giữ số của dãy cũ

- **File**: `src/main/java/vn/vtt/pmkt/cell/tien_mat_tien_gui/internal/service/PhieuKiemService.java:212-222`
  (`capNhatPhieuChi`) và `:161` (`doiHinhThucTien`).
- **Hợp đồng bị phá**: `LuuPhieuChiTienGuiTemplate.java:20-32` — *"Loại DUY NHẤT lấy PTTT từ BODY
  (PCTG-a) — **ba giá trị, ba dãy đánh số**"*. PTTT là thứ chọn dãy số bên trong loại PCTG.
- **Trigger**: chứng từ mua hàng đã tick "Trả tiền ngay", phiếu chi tiền gửi hiện có
  `PTTT = UY_NHIEM_CHI`, số `UNC0007`. Người dùng Sửa chứng từ mua, đổi Hình thức thanh toán sang
  **Séc chuyển khoản** (hoặc Séc tiền mặt) rồi Lưu.
- **Actual**: `doiHinhThucTien(phieuId, tienMat=false)` so `getHinhThucTien() == TIEN_MAT` (false)
  với `tienMat` (false) ⇒ `false != false` ⇒ **không** rẽ nhánh xoá-và-cấp-lại. Đi tiếp
  `lenhChi(phieuId, yc, yc.soChungTu())` ⇒ phiếu giữ nguyên `UNC0007` trong khi PTTT đã sang
  `SEC_CHUYEN_KHOAN`.
- **Expected**: cùng luật với đổi hình thức tiền — số cũ thuộc dãy khác thì phải để trống cho hệ
  thống cấp lại (chính lý do PR viết ở `PhieuKiemService.java:120`).
- **Hậu quả**: phiếu chi mang số của dãy không phải của nó; hai dãy dính số trùng/nhảy cóc. Đây
  đúng lớp lỗi PR đang sửa, chỉ khác trục — sửa được ở cùng một chỗ.
- **Đã phản biện**: `phuongThucCuaChi()` vẫn map đúng PTTT mới, và `hinhThucChiCua` xác nhận
  `SEC_TIEN_MAT` thuộc `hinh_thuc_tien = TIEN_GUI` (nên không rơi vào nhánh đổi hình thức tiền).
  Test `PhieuKiemServiceNapPhieuTest.doi_hinh_thuc_thanh_toan_thi_xoa_phieu_cu_va_cap_phieu_moi_dung_loai`
  chỉ phủ trục hình thức tiền, không phủ trục PTTT.

### 🟠 Major 2 — Đổi hình thức thanh toán nay đòi thêm quyền **Delete** trên phiếu thu/chi

- **File**: `PhieuKiemService.java:136-140` · `:207-215` (nhánh `xoa(phieuId); tao…`) →
  `PhieuKiemService.java:315-321` (`xoa`) → `DieuHuongGhiTheoLoai.java:89-90`
  (`kiemTraVaLayLoai(hinhThucTien, id, QuyenChecker.DELETE)`).
- **Trigger**: người dùng có quyền sửa chứng từ bán hàng và có `ThuTien.Create` + `ThuTien.Update`
  nhưng **không** có `ThuTien.Delete`; họ Sửa chứng từ bán, đổi Hình thức thanh toán Tiền mặt →
  Chuyển khoản, bấm Lưu.
- **Actual**: `dieuHuong.xoa` ném 403. `PhieuKiemService` là `@Transactional`, lời gọi nằm trong
  transaction của luồng lưu chứng từ bán ⇒ **rollback cả lượt lưu chứng từ nguồn**; người dùng
  không sửa được chứng từ bán chỉ vì thiếu một quyền của màn khác.
- **Expected**: một thao tác Sửa ở màn nguồn không nên đòi quyền Delete ở màn ngân quỹ. Yêu cầu
  quyền này là **hệ quả phụ** của việc tái dùng `dieuHuong.xoa` để không nhân bản cascade năm bảng
  con (lý do chính đáng), không phải quyết định phân quyền có chủ ý — nó không được ghi ở
  `package-info.java` mục "Quyền: hai tầng theo NAMESPACE" và không có test.
- **Đã phản biện**: đường tạo (`taoPhieuThu` → template) cũng gác quyền
  (`LuuPhieuThuChiTemplate.kiemTraQuyen` → `super`), nên `Create` vốn đã cần từ trước — chỉ
  `Delete` là mới. Trước PR đường này ném 404 nên chưa ai chạm tới, tức đây là **hành vi mới**,
  không phải hồi quy có sẵn.
- **Hướng**: hoặc tách một lối xoá nội bộ không gác `DELETE` (chứng từ nguồn mới là chủ vòng đời —
  đúng lập luận D5 mà chính javadoc `xoa` đã viết), hoặc ghi rõ ràng buộc quyền mới vào
  `package-info.java` + một test phân quyền.

### 🔵 Minor 3 — `ghiSo(UUID)` / `boGhiSo(UUID)` không `final`, cờ `tuNguon` mất âm thầm

`ChungTuThuChiCrudService.java:329-347`: bản 1 tham số uỷ nhiệm sang bản 2 tham số với
`tuNguon = false`. Lớp con nào lỡ override bản **1 tham số** sẽ vô hiệu hoá đường lan trạng thái từ
chứng từ nguồn mà **không cổng nào đỏ** — phiếu kiêm chỉ đơn giản không ghi sổ được nữa. Đã kiểm:
cả 5 lớp con (`PhieuThu/ChiTienMat`, `PhieuThu/ChiTienGui`, `ChuyenTienNoiBo`) hiện đều override
đúng bản 2 tham số. Đặt `final` cho hai bản 1 tham số là chặn được vĩnh viễn.

### 🔵 Minor 4 — Test Jackson không dùng ObjectMapper của ứng dụng

`DongRequestVatTuJacksonTest.java:18` dựng `new ObjectMapper().findAndRegisterModules()`. Rủi ro nó
canh (record hai constructor làm Jackson mơ hồ) phụ thuộc cấu hình creator của mapper; mapper của
Spring Boot có cấu hình khác. Test đúng ý tưởng nhưng chưa phủ đúng runtime.

### 🔵 Minor 5 — Commit gộp hai việc, scope không phủ hết diff

Commit `feat(thu-chi): …` sửa cả `ban_hang/chung_tu_ban_hang` và `chung_tu_mua_hang`
(`TrangThaiThanhToan` so theo nguyên tệ — một thay đổi độc lập với phiếu kiêm theo dòng hàng).
Scope `thu-chi` không phủ hai module đó. Hai việc nên là hai commit.

### 🔵 Minor 6 — Tên nhánh lệch quy ước

`feature/thuchimodulemua`. `conventions-chung.md §4.2` khai tiền tố là `feat/*` (không `feature/`),
`§4.3` yêu cầu tên mô tả **chữ thường, phân cách bằng `-`**. Đúng phải là
`feat/thu-chi-module-mua`.

### ⚪ Nit 7 — Tham số chết trên `ChuyenTienNoiBoCrudService`

`ChuyenTienNoiBoCrudService.java:112,117` nhận `tuNguon` nhưng chuyển tiền nội bộ không bao giờ là
phiếu kiêm. Vô hại, chỉ là bề mặt API rộng hơn cần thiết.

### ⚪ Nit 8 — Import lộn xộn

`PhieuKiemService.java:5-14`: `vn.vtt.pmkt…DongPhieuChi` / `DongPhieuThu` chèn giữa nhóm
`java.util`, `java.util.Map` nằm sau `org.springframework`. Checkstyle của repo chạy
`isIgnoreFailures = true` và không bật rule import-order nên không đỏ.

### ⚪ Nit 9 — Sửa javadoc V1092 → V1094/V1095 diện rộng

~20 file chỉ đổi số hiệu migration trong javadoc. Đúng và có ích, nhưng làm diff phình ngoài phạm
vi tính năng — khó soi phần logic thật.

## 3. Bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục Modulith | ✅ Không vi phạm. 2 file mới: `V1099__…sql` + `DongRequestVatTuJacksonTest` (đúng `internal/dto` bên test). Không file phẳng ra gốc module, không tạo `api/` thừa, `package-info.java` chỉ sửa javadoc. Base package `vn.vtt.pmkt` đúng cho `cell-app`. |
| 2 | Không đánh lại version migration | ✅ Không vi phạm — xem §4. |
| 3 | Chưa test lại sau khi merge | ✅ N/A — merge-base **bằng đúng** tip `develop`, nhánh không tụt một commit nào, không có file giao nhau cần merge thử. |
| 4 | N+1 / chưa tối ưu | ✅ Không vi phạm. `NoDanhMucService.java:649` nạp hàng hoá **theo lô** (`traCuu.vatTu(gop(dong, …))` → `WHERE id IN (:ids)`), đúng khuôn với `doiTuong`/`dieuKhoanThanhToan` liền kề. Không có query trong vòng lặp mới, không thêm quan hệ JPA nào (cột `vat_tu_id` là khoá mềm `UUID`, không FK, không `@ManyToOne`). |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ Không vi phạm. Không có controller/entity/repository **mới**. Ba entity sửa vẫn extend `BaseChiTietChungTuEntity` / `SoftDeletableEntity`; luồng lưu vẫn đi `ChungTuTemplate`; ghi sổ vẫn qua template, không insert thẳng bảng sổ. |
| 6 | Chưa tận dụng base FE | N/A — PR backend. |
| 7 | Constant đặt sai chỗ | ✅ Không vi phạm. Mã lỗi `PHIEU_KIEM` là hằng ở `internal/constant/MaLoiChung.java:22`, dùng lại ở `DoiTrangThaiPhieuThuChi` chứ không viết lại literal. |

## 4. Migration (cổng cứng)

```
max trên origin/develop        : 1098   (V1098__sal_hdbh_uq_bo_khach_hang_id.sql)
migration mới trong diff       : A  V1099__cash_map_vat_tu_id.sql
dòng M/D/R trên migration cũ   : không có
nhánh remote khác giành V1099  : chỉ chính origin/feature/thuchimodulemua
```

✅ Số `1099 > 1098`, không trùng, không sửa/rename/xoá migration đã merge, tên dạng số thứ tự 4 chữ
số (không phải timestamp 14 chữ số). SQL dùng `ADD COLUMN IF NOT EXISTS` nên chạy lại được. Ba bảng
đích (`cash_phieu_thu_chi_chi_tiet`, `map_phieu_thu_chung_tu_ban`, `map_phieu_chi_chung_tu_mua`) đều
là bảng **đã có**, không phát sinh tiền tố bảng mới. Schema ↔ entity khớp cả hai chiều: mỗi cột mới
có đúng một `@Column(name = "vat_tu_id")` tương ứng, không entity nào khai cột thiếu migration.

## 5. Cổng đã chạy

Lệnh thực tế (worktree detached `.review-cellapp-pr124` tại `01c01505`):

```bash
cd .review-cellapp-pr124 && ./gradlew unitTest --console=plain > /tmp/gate-cellapp-unittest.log 2>&1
```

| Cổng | Kết quả head | Baseline | Kết luận |
|---|---|---|---|
| `./gradlew unitTest` | 3852 test · **2 failed** · 2 skipped | 3841 test · **2 failed** — *cùng hai bài* | **Lỗi nền**, không do PR. PR thêm 11 test, tất cả xanh. |
| Testcontainers (~25 bài) | **NOT-RUN** | — | Máy không có Docker (luật repo). |

Hai bài đỏ giống hệt hai bên:
- `HoaDonMuaControllerPermissionTest.luuVaGhiSoYeuCauThemQuyenPost()` — Mockito `WantedButNotInvoked`.
- `LoaiChungTuChuDongBoCheckTest.enum_va_check_constraint_khop_nhau()` — bài này đọc **file**
  `V1086__…sql` để so whitelist CHECK với enum; `V1093__ref_ctct_khai_lai_tron_bo_loai_chu.sql`
  (đã ở trên develop) sửa lại CHECK mà hằng `MIGRATION` chưa được cập nhật — đúng cái bẫy javadoc
  của chính bài đó cảnh báo. Cả hai nằm ngoài diff PR.

### ⚠ Ghi nhận về baseline: `develop` hiện **không biên dịch nổi test**

Chạy `unitTest` thẳng trên `cfc18545` (tip develop) thì **`compileTestJava` FAILED**:
`DoiTruChungTuServiceTest.java:163` và `:758` gọi `new KhoanNo(…)` thiếu một tham số `UUID` so với
record hiện tại. **PR #124 sửa đúng hai dòng này** (`+ UUID.randomUUID()`), tức nó vá luôn một lỗi
đỏ đang nằm trên develop. Baseline ở bảng trên vì thế được đo trên
`merge-base + đúng file `DoiTruChungTuServiceTest.java` lấy từ head` — cách duy nhất có số so được;
đã ghi rõ để không nhầm là baseline nguyên bản.

## 6. Điểm làm tốt

- `DongRequestVatTuJacksonTest` canh đúng rủi ro nguy hiểm nhất của thay đổi này: hai record
  (`DongCongNoRequest`, `DongHachToanRequest`) nhận thêm constructor "chữ ký cũ", thứ có thể làm
  Jackson mơ hồ và nổ ở request thật thay vì ở test.
- `DinhKhoanPhieuThuChi.coNguyenTe` (`:66-68`) dùng `signum() > 0` **khớp chính xác** ràng buộc
  kernel `DinhKhoanValidator.java:109` (`soTienNguyenTe().signum() <= 0` → ném lỗi). Đã kiểm thêm:
  `DongHachToanRequest` javadoc ràng `soTien >= 0`, nên không có nhánh âm để lọt.
- `PhanBoCongNoService.gopDong` (`:502-511`) thêm `chiTietId` vào khoá gộp có ghi rõ vì sao dòng
  TTTHD (`chiTietId == null`) vẫn gộp như cũ — không phá hành vi cũ.
- Vá lỗi biên dịch test đang đỏ trên develop (xem §5).

## 7. Chưa đọc / chưa kiểm

- ~25 test Testcontainers (`*IT.java` trong diff: `ChungTuThuChiPanelIT`, `NganQuyKtthSchemaIT`,
  `ChungTuThuChiQuyenIT`) — không chạy được, máy không có Docker.
- Không đối chiếu BR / spec / `trace.sh` / `msg.sh` — user yêu cầu bỏ phần nghiệp vụ.
- Không kiểm hành vi thật trên UI/API (`qa-flow`) — ngoài phạm vi lượt này.

## 8. Kết luận

**REQUEST CHANGES** — 2 Major (không Blocker).

Cổng cứng đều sạch: migration đúng số, kiến trúc Modulith đúng, không N+1 mới, không hardcode,
không lộ Entity, `unitTest` không đỏ thêm một bài nào so với nền. Hai Major đều nằm ở đúng một chỗ
(`PhieuKiemService` nhánh đổi hình thức thanh toán): một là **thiếu phủ trục PTTT** của chính luật
"đổi loại thì cấp số mới" mà PR vừa dựng, một là **yêu cầu quyền `Delete` phát sinh ngoài ý định**
làm hỏng cả lượt lưu chứng từ nguồn. Cả hai sửa gọn trong cùng một method.
