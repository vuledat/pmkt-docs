# Mẫu in chứng từ theo khối — Báo cáo bàn giao

| | |
|---|---|
| Ngày | 2026-09-17 |
| Phạm vi | GĐ1 (cell-app + client) **và** GĐ2 (super-admin-service + client-admin) — làm trọn cả hai tầng |
| Spec | [`docs/doing/mau-in-chung-tu-spec/`](../mau-in-chung-tu-spec/) — 75 luật `R-MAUIN-nnn` · 9 bất biến `INV-MAUIN-nnn` · 55 kịch bản `S-nnn` |
| Trạng thái | **Hoàn thành phần code + test tự động.** GĐ2 đã đẩy lên GitHub; `cell-app` và `client` chưa commit; chưa kiểm trên trình duyệt thật |

---

## 1. Đã giao gì

| Vùng | Số file | Nội dung |
|---|---|---|
| `cell-app/…/cell/mau_in/` | 51 main · 15 test | Module Spring Modulith mới: JSON model, `MauChuanBuilder`, `HopNhatCatalog`, `KiemTraMau`, `ChuanHoaMau`, `GiaiMauHieuLuc`, cache + client super-admin, controller A1–A7, entity `prn_mau_in_tuy_chinh`, SPI `MauInProvider` |
| `cell-app` — provider | 4 loại | `MDV` (mua dịch vụ) · `BH` (bán hàng) · `PT` / `PC` (phiếu thu / chi tiền mặt), mỗi loại một `…MoTaMauIn` + `…MauInProvider` + test ghim trường |
| `cell-app` — migration | 3 | `V1148__prn_mau_in_tuy_chinh.sql` (bảng + RLS + GRANT) · `V1149__iam_quyen_ht_mau_in.sql` (seed `HTMauIn.View/Edit`) · `V1150__prn_mau_in_lich_su.sql` (bảng lịch sử + RLS) |
| `client/src/base/domainKit/mauIn/` | 48 | Engine dùng chung: Zod schema, helper (hợp nhất · kiểm tra · chuẩn hoá · định dạng · thao tác khối), store zustand + zundo, `MauInPaper` (một renderer cho canvas lẫn bản in), `MauInEditor` 3 cột, `NutInChungTu`, i18n `mauIn` |
| `client/src/features/heThong/thietLapMauIn/` | 16 | Màn danh sách 47 loại + màn editor của đơn vị, query/mutation, route, menu |
| `client/src/base/**` | 5 | Bổ sung `@base`: `CommonSegmented`, `CommonColorPicker`, `PropSection`, `PropField`, `propField.css` |
| `super-admin-service/…/quan_tri/mau_in/` | 41 | Bản sao bộ kiểm/hợp nhất, `CatalogSnapshot`, entity `sa_mau_in_mac_dinh`, B1–B4 (`/api/admin/mau-in`), B5–B6 (`/internal/mau-in`), `InternalTokenFilter`, migration common V4 + postgresql/h2 V5 |
| `client-admin/…/quanTri/mauInMacDinh/` | 25 | Console super admin: danh sách loại + editor mẫu mặc định (Xuất bản · Về mẫu đóng gói · Đặt lại · In thử). Engine `@domain-kit/mauIn` sao **nguyên** từ `client` |

## 2. Kết quả cổng (đo lần cuối 2026-09-17)

| Repo | Lệnh | Kết quả |
|---|---|---|
| `cell-app` | `./gradlew unitTest --tests 'vn.vtt.pmkt.cell.mau_in.*' --tests arch.{MauInModularityTest,ProxyArchTest} --tests '*MoTaMauInTest' --tests '*MauInProviderTest'` | **85 test · 0 lỗi** (làn hẹp); `./gradlew unitTest` đầy đủ: 5574 test, 3 đỏ đều có sẵn trên `develop` |
| `super-admin-service` | `./gradlew unitTest --tests '*MauIn*' --tests '*CatalogSnapshot*'` | **105 test · 0 lỗi** |
| `client` | `vitest run src/base/domainKit/mauIn src/features/heThong/thietLapMauIn` | **87 test · 0 lỗi** (12 file) |
| `client-admin` | `vitest run src/base/domainKit/mauIn src/features/quanTri/mauInMacDinh --maxWorkers=2` | **98 test · 0 lỗi** (15 file) |
| `client` | `tsc -b --noEmit` · `eslint` · `lint:boundaries` · `vite build` | 0 lỗi mới (nền sẵn có 237 lỗi typecheck, không dòng nào trong file mới); build OK |
| Truy vết | `trace.sh docs/doing/mau-in-chung-tu-spec be` · `… fe` | **BE 63/63 OK · FE 61/61 OK** — 0 MISSING, 0 VI-PHAM, kết luận **DAT** |
| Engine song sinh | `diff -rq client/src/base/domainKit/mauIn client-admin/src/base/domainKit/mauIn` | giống hệt, 0 khác biệt |

Luật tầng `SA` (`R-MAUIN-006 · 091 · 092 · 093`) không nằm trong `trace.sh` (script chỉ quét `cell-app/src` và
`client/src`) — được ghim bằng test trong chính `super-admin-service` (`MauInMacDinhServiceTest`,
`CatalogSnapshotTest`, `MauInMacDinhApiTest`).

## 3. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR3 (form · xác nhận đóng) | Hộp "Xác nhận đóng" 2 nút, nguyên văn BR, ở cả editor tenant và editor super admin; hộp "Xác nhận xóa" khi bỏ khối tự do |
| BR7 · BR8 (số · ngày) | Bản in định dạng theo runtime của đơn vị (`taoDinhDangIn`); BE chỉ trả giá trị thô + kiểu |
| BR16 · BR26 (thông báo) | Toast/banner cho cảnh báo kiểm mẫu, "có mẫu chuẩn mới", lỗi tải dữ liệu in |
| BR25 (quyền) | `HTMauIn.View/Edit` cho màn thiết lập; quyền in theo từng loại; `MauInMacDinh.*` phía super admin; thiếu quyền thì **ẩn** chứ không làm mờ |
| BR29 | Bỏ bản tuỳ chỉnh = xoá mềm, đọc lại rơi về mẫu mặc định |
| BR30 (grid · tối thiểu 1 cột) | Bảng đang hiện phải còn ≥1 cột; Thông tin chung phải còn ≥1 trường |
| BR43 (chuẩn hoá trước lưu) | Trim nhãn, chia lại tổng rộng cột về 100 %, mã màu về chữ thường |
| BR4 · BR9 (loại chứng từ) | Danh sách 47 mã theo BA; loại chưa có provider đánh dấu "Chưa hỗ trợ" |

## 4. Quyết định tự chốt cần BA xác nhận lại

Sáu mục `CLOSED-AUTO` trong [`01-conflict.md`](../mau-in-chung-tu-spec/01-conflict.md), mỗi mục đều có test ghim.
Ba mục đáng để BA soi lại:

1. **C08 · quyền in.** Seed quyền không có `MuaDichVu.Print` nên in MDV gác bằng `MuaDichVu.View.Detail`; bán hàng
   cũng vậy (`BanHangHoa.View.Detail`). Phiếu thu/chi dùng `ThuTienTM.Print` / `ChiTienTM.Print` vì đã có sẵn.
   BA cấp mã `.Print` cho MDV/BH thì chỉ phải đổi một hằng trong provider.
2. **Mã loại bán hàng là `BH`** (theo `mst_loai_chung_tu.code` sau V1032), không phải `BHH`/`CTBH`.
3. **C14 · bảng thuế** của MDV và BH suy từ các dòng có tiền thuế khác 0 (hai loại này không có bảng thuế riêng).

Mục `OPEN` cuối cùng (C15) đã đóng ngày 2026-09-17: hai thư mục GĐ2 nay là git repo thật, remote `ospgroupvn-pmkt`, nhánh mặc định `develop`.

## 4a. Đợt bổ sung 2026-09-17 (sau khi user xem bản chạy thật)

| Yêu cầu | Luật | Làm ở đâu |
|---|---|---|
| Kéo mép cột trên giấy để đổi độ rộng, bù trừ cột liền kề | R-MAUIN-100 | `helpers/thaoTacKhoi.ts` (hàm thuần) · store · `MauInPaper` · CSS |
| Lịch sử phiên bản, xem trước và khôi phục | R-MAUIN-101…105 · INV-MAUIN-009 | bảng lịch sử + 2 endpoint ở CẢ hai tầng; popup dùng chung `HopLichSuMauIn` |
| Dựng lại đầu trang cho đỡ chật | — | In thử thành nút icon · menu "Khác" gom 2 thao tác hiếm · bỏ nút "Đóng" trùng với mũi tên quay lại |
| Nút "Dữ liệu mẫu" ở console super admin không chạy | R-MAUIN-106 | đổi từ chữ tĩnh thành ô chọn: dữ liệu mẫu ↔ dữ liệu giữ chỗ |
| Bảng kẻ mờ trên canvas, không có khi in | R-MAUIN-107 | lớp CSS chỉ gắn ở chế độ canvas, quy tắc nằm dưới lớp bọc canvas |

## 4b. Đã đẩy lên GitHub (2026-09-17)

| Repo | Remote | Nhánh | Commit | Số file |
|---|---|---|---|---|
| `super-admin-service` | `ospgroupvn-pmkt/super-admin-service` | `develop` (mặc định) | `80794ef` | 185 |
| `client-admin` | `ospgroupvn-pmkt/client-admin` | `develop` (mặc định) | `a64e4a3` | 889 |

Hai repo trước đó chưa được khởi tạo git; đây là bản nhập đầu nên commit thẳng vào `develop` theo chỉ định
của user (ngoại lệ của luật 8). Không có `build/`, `node_modules/`, `dist/` lọt vào cây commit; số file trên đĩa
dưới `src/` bằng đúng số file trong cây commit ở cả hai repo.

⚠ `super-admin-service/src/main/resources/application-local.yml` chứa hai tài khoản dựng sẵn cho hồ sơ `local`
(`superadmin/SuperAdmin@123`, `kiemtra/KiemTra@123`, H2 trong bộ nhớ, tên miền `@pmkt.local`). Đây là dữ liệu
thử của máy dev chứ không phải bí mật sản phẩm, nhưng đã nằm trên remote — nếu muốn sạch tuyệt đối thì chuyển
sang biến môi trường và xoá khỏi lịch sử.

## 5. Chưa làm (nói rõ để không bị hiểu là quên)

- **`cell-app` và `client` chưa commit.** Toàn bộ nằm trong working tree và còn file mới chưa
  `git add` — phải add trước khi commit, nếu không CI sẽ đỏ vì thiếu file (xem `client/CLAUDE.md §15.1`).
- **Chưa kiểm trên trình duyệt thật** (chưa chạy dev server để soi editor, kéo thả, cửa sổ in).
- **Chưa chạy test Testcontainers** — máy cấm Docker. Controller/repository của module mới chỉ được phủ bằng test
  đơn vị và test H2 phía super-admin.
- **Chưa có provider** cho 43 loại còn lại (phiếu tiền gửi, chứng từ nội bộ, kho…). Thêm một loại = một bean
  `MauInProvider` + một dòng trong `XuatCatalogMauInTest.CATALOG` + chạy lại `sync-catalog.sh`.
- **Ô ghi chú khi lưu / xuất bản chưa có ở giao diện.** Cột `ghi_chu` và trường DTO đã sẵn ở cả hai tầng, nhưng A3/B3 chưa có ô nhập nên mọi bản ghi lịch sử hiện có `ghiChu = null`. Cần BA chốt có cho nhập lý do hay không.
- Logo và ảnh nền: lưu được trong JSON nhưng **không render** (chốt C06 cho v1).

## 6. Chạy lại thế nào

```bash
# BE cell-app — nhớ gỡ tạm 5 test cũ không biên dịch được của develop, xong khôi phục ngay
cd cell-app && export JAVA_HOME="/c/Users/DatVL/.jdks/ms-21.0.12.1" && ./gradlew unitTest --tests 'vn.vtt.pmkt.cell.mau_in.*'
```

```bash
# Sinh lại snapshot catalog rồi chép đi (docs · super-admin · fixture test của client và client-admin)
bash docs/doing/mau-in-chung-tu/sync-catalog.sh
```

```bash
# Truy vết luật — cổng bắt buộc trước khi báo xong
bash docs/rules/trace.sh docs/doing/mau-in-chung-tu-spec be && bash docs/rules/trace.sh docs/doing/mau-in-chung-tu-spec fe
```

Biến môi trường mới: `PMKT_MAU_IN_SUPER_ADMIN_ENABLED` (mặc định `false` — tắt thì cell bỏ tầng mẫu super admin),
`PMKT_SUPER_ADMIN_URL`, `PMKT_MAU_IN_MAC_DINH_TTL` (mặc định 10 phút). Chạy `super-admin-service` ở máy local
**bắt buộc** có `PMKT_INTERNAL_TOKEN` — service fail-fast khi thiếu, kể cả profile `local`.
