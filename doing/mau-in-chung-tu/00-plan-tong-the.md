# Mẫu in chứng từ cấu hình theo khối — Kế hoạch tổng thể (phân tích · thiết kế · triển khai)

| | |
|---|---|
| **Trạng thái** | BẢN NHÁP CHỜ CHỐT — 17 câu hỏi ở §14 phải có câu trả lời của user trước khi `/gen-*` |
| **Ngày** | 2026-09-17 |
| **Nguồn yêu cầu** | `C:\Users\DatVL\Downloads\ThietLapMauIn.html` (mock 540 dòng, demo cho *Chứng từ mua dịch vụ*) + 5 bổ sung của user (§1) — **không có tài liệu BA** cho tính năng này |
| **Codebase chạm tới** | `super-admin-service` + `client-admin` (mẫu mặc định hệ thống) · `cell-app` + `client` (mẫu tuỳ chỉnh của đơn vị + in) |
| **Tài liệu đi kèm** | [01-hop-dong-json-va-api-v1.md](01-hop-dong-json-va-api-v1.md) — schema JSON, catalog, API, DB, luật kiểm tra (nguồn sự thật kỹ thuật) · [02-anh-xa-giao-dien-va-base-component.md](02-anh-xa-giao-dien-va-base-component.md) — token mock → hệ thống, ánh xạ từng control → `@base`, CSS cục bộ "chế độ dày", khoảng trống phải thêm vào `@base`, checklist nghiệm thu giao diện |
| **Người chốt cần có** | user/BA (§14) · 1 dev BE · 1 dev FE |

---

## 0. Tóm tắt điều hành

1. **Hai tầng mẫu, một JSON:** super admin sửa *mẫu mặc định hệ thống* cho từng loại chứng từ (áp cho mọi tenant);
   admin đơn vị sửa tiếp thành *mẫu tuỳ chỉnh của đơn vị*. Cell giải mẫu hiệu lực theo chuỗi
   `tuỳ chỉnh đơn vị → mặc định super admin → mẫu chuẩn đóng gói trong code`.
2. **Mô hình "khối"** (đầu trang đơn vị · tiêu đề · thông tin chung dạng bảng · N bảng chi tiết · tổng hợp · chữ ký ·
   khối tự do) đúng như mock — **không** dùng engine lưới `bieu_mau` đã có (khác bài toán, §3-D1), nhưng tái dùng
   toàn bộ hạ tầng của nó ở FE (`@dnd-kit/core`, `zustand`, `zundo`, `immer`, pattern store/dnd).
3. **Catalog trường/bảng theo loại chứng từ là code Java trong `cell-app`** (một `MauInProvider` mỗi loại, cắm qua
   SPI); mẫu chuẩn đóng gói sinh từ catalog; super-admin-service dùng **snapshot** của catalog.
4. **Render:** một renderer HTML ở FE (`@domain-kit/mauIn`) dùng cho cả canvas cấu hình lẫn in (khuyến nghị giai
   đoạn 1 — Q1); BE cấp *dữ liệu in chuẩn hoá*. PDF phía BE là giai đoạn 2 nếu cần lưu trữ/gửi mail.
5. **Lan mẫu mặc định xuống cell** bằng **pull + cache** qua kênh `/internal/**` mới trên super-admin-service
   (Q2) — không fan-out, không copy lúc provisioning.
6. Lộ trình 4 giai đoạn ≈ **40–45 ngày công** cho khung + 3 loại chứng từ pilot (MDV · BH · PT); 25 loại còn lại
   ≈ 0,5–1 ngày/loại, làm song song theo chủ module (§12).

---

## 1. Yêu cầu — rút từ mock + bổ sung của user

| # | Yêu cầu | Nguồn | Ghi chú thiết kế |
|---|---|---|---|
| F1 | Màn 3 cột: **Bố cục mẫu** (outline kéo thả, ẩn/hiện, xoá khối tự do) · **Xem trước** (giấy A4/A5, dọc/ngang, zoom, vừa khung, chọn dữ liệu xem thử) · **Bảng chỉnh** theo khối đang chọn | mock `#left/#center/#right` | `MauInEditor` trong `@domain-kit/mauIn` |
| F2 | Thiết lập toàn trang: khổ/hướng, lề 0–5 cm, font (6 font), cỡ chữ 8–20, màu chữ, logo, hình nền/dấu chìm, chân trang (số trang + ghi chú) | mock `sel==='page'` | `Trang` §1 hợp đồng |
| F3 | 7 loại khối: `company` · `title` · `fields` · `table` (×N) · `summary` · `sign` · `free` | mock `defaultState()` | đổi tên `DON_VI · TIEU_DE · THONG_TIN · BANG · TONG_HOP · CHU_KY · TU_DO` |
| F4 | Mỗi trường/cột: tick in, đổi nhãn, đậm/nghiêng, độ rộng, kiểu; kéo ⠿ đổi thứ tự; tìm nhanh | mock `renderIns` | inspector theo loại khối |
| F5 | Bảng: tên bảng, cột STT, dòng Cộng, lặp tiêu đề cột, kẻ ô (đầy đủ/ngang/không), độ rộng % + "Chia đều về 100 %" | mock `type==='table'` | |
| F6 | Chữ ký: 5 vai trò lấy từ Thông tin công ty + ô ký tự do, tối đa 4 ô/hàng, dòng "Ngày … tháng … năm …", in tên, chiều cao chỗ ký | mock `type==='sign'` | vai trò = 5 người ký của `CompanyInfoResponse` |
| F7 | Khối tự do: dòng dữ liệu (chọn từ kho trường) hoặc dòng chữ tự do; thêm/xoá/kéo | mock `type==='free'`, `pickDataFields` | |
| F8 | Kiểm tra trước khi lưu (lỗi chặn lưu / cảnh báo), Undo/Redo (60 bước), Ctrl+S/Z/Y/Esc, cờ "Chưa lưu", xác nhận đóng khi dirty, "Đặt lại mẫu chuẩn" | mock `checks()`, `push()`, `doSave()` | luật R-MAUIN-010…025 |
| F9 | Xem thử bằng **chứng từ đang mở / dữ liệu mẫu / chứng từ khác cùng loại** | mock `#dataSeg`, `#pickVoucher` | tenant: A5/A6; super admin: chỉ dữ liệu mẫu |
| F10 | Menu **In** của chứng từ: mẫu cố định 🔒 + "Mẫu tuỳ chỉnh" + "⚙ Thiết lập mẫu in…" | mock `#menuDemo` | `NutInChungTu`, A7 |
| **F11** | **Tiêu đề của bảng chi tiết cấu hình được** (nội dung · hiện/ẩn · đậm · căn) — ngoài nhãn từng cột | bổ sung #1 | `KhoiBang.tieuDe` |
| **F12** | **Thông tin chung chia layout dạng bảng**: 1–4 cột, trường chiếm 1..n ô, kẻ ô, độ rộng nhãn | bổ sung #2 | `BoCucBang`, `TruongIn.span` |
| **F13** | **"Đầu trang đơn vị" và "Tiêu đề" không đổi vị trí, không xoá** (luôn là khối 1 và 2) | bổ sung #3 | `khoa`, INV-MAUIN-001; ẩn/hiện xem Q5 |
| **F14** | **Kéo thả trực tiếp các vùng trên giấy** (không chỉ ở outline) | bổ sung #4 | dnd-kit trên canvas, đồng bộ outline |
| **F15** | Mỗi loại chứng từ có **danh sách bảng chi tiết riêng để chọn** | user | `MoTaMauIn.bang[]`; mỗi bảng = một khối `BANG` bật/tắt (Q16) |
| F16 | Cấu hình lưu **JSON** | user | `jsonb` (cell) · `TEXT` (control plane, H2) |
| F17 | Super admin cấu hình ban đầu, áp cho mọi tenant; admin công ty sửa tiếp từ mặc định | user | §3-D2, §9 |
| F18 | Giao diện **giống style/màu hệ thống** (antd v6, brand red `#EE0033`, `@base` components) — không dùng xanh `#2b5f9e` của mock | user | §7.6 |
| F19 | Áp cho **tất cả 47 loại chứng từ** (BR4/BR9) | user | rollout theo provider, §12 GĐ4 |
| F20 | Phân quyền (BR25), i18n chrome UI (luật 2), không hardcode (luật 1), truy vết luật (`trace.sh`) | CLAUDE.md | §9, §10 |

---

## 2. Hiện trạng đo được (không suy diễn)

| Hạng mục | Hiện trạng | Bằng chứng |
|---|---|---|
| In chứng từ thu/chi | 10 mẫu **Jasper `.jrxml` tĩnh** (Jasper 6.21.3), registry enum, PDF do BE render; `InPhieuJasperArchTest` ghim "lớp duy nhất import Jasper" | `cell-app/…/tien_mat_tien_gui/internal/model/MauInPhieuThuChi.java`, `…/service/business/InPhieuThuChi.java`, `BaseChungTuThuChiController.java:89-113` (`/{id}/mau-in`, `/{id}/in`) |
| FE in thu/chi | split button `In \| ˅`, menu = danh sách mẫu do BE suy; **chốt Dat 2026-08-20: render thuộc BE** | `client/src/features/nganQuy/_shared/components/NutInPhieu.tsx`, `api/inPhieuApi.ts` |
| FE in kho | dựng HTML ở FE (`MauInChungTuKho`), tải `.doc` (HTML + `@page`), chờ endpoint BE | `client/src/features/kho/_shared/components/MauInChungTuKho.tsx`, `helpers/taiFileIn.ts` |
| Engine "Biểu mẫu động" | designer **lưới kiểu Excel** cho phụ lục thuế, JSON `BieuMauDinhNghia` v1 + công thức + PDF/XLSX/DOCX ở `report-service`; đã merge `develop` (`client` #192, `cell-app` #152) | `docs/doing/bieu-mau-dong/00-giai-phap.md`, `01-hop-dong-v1.md §1`, `client/src/features/bieuMau/**`, `cell-app/…/bieu_mau_proxy/**` |
| Thư viện FE sẵn có | `@dnd-kit/core 6.3` · `zustand 5` · `zundo 2` · `immer 11`; pattern store undo/redo và id kéo/thả | `client/package.json:18,30,38,39`, `bieuMau/thietKeBieuMau/hooks/useDesignerStore.ts`, `helpers/keoTha.ts` |
| Lưu cấu hình JSON | `core_cau_hinh_cot`, `core_mau_excel`: `@JdbcTypeCode(SqlTypes.JSON) String`, RLS theo `tenant_id` | `cell-app/…/common/ui_config/entity/CauHinhCot.java`, `V1__create_database.sql:31895` |
| Điểm cắm chung cho chứng từ | **28 controller** kế thừa `BaseChungTuController` (kernel `accounting_core`); SPI precedent `MauCotPort` | `cell-app/…/accounting_core/chung_tu/controller/BaseChungTuController.java`, `core/controller/spi/MauCotPort.java` |
| Thông tin đơn vị & người ký | 5 người ký (`GIAM_DOC · KE_TOAN_TRUONG · THU_KHO · THU_QUY · NGUOI_LAP`) + 2 cờ `inTenNguoiKyTrenChungTu`, `layTenNguoiLapPhieuTuNguoiDungDangNhap`; tên/địa chỉ in lấy `mst_don_vi` cấp GỐC; **chưa có trường logo** | `platform_iam/tenant/internal/dto/CompanyInfoResponse.java`, `tien_mat_tien_gui/internal/dto/ToChucInDto.java` |
| Số tiền bằng chữ | đã có ở BE | `tien_mat_tien_gui/internal/service/business/SoTienBangChu.java` |
| Danh mục loại chứng từ | 47 loại theo BA, `mst_loai_chung_tu.code` (bộ mã chuẩn sau `V1032`: `PT PC GBC PCTG CTNB`…; migration còn thêm `CTNHD`, `PTT`) | `pmkt-docs/ba/PMKT-E-00093_DanhMucDungChung/5.screens/SCR_LoaiChungTu/DuLieuKhoiTao_LoaiChungTu.md`, `V1001`, `V1008`, `V1011`, `V1032` |
| super-admin-service | Modulith `core · security · quan_tri/{tenant,cau_hinh}`, H2 profile `local`, Flyway `sa_flyway_schema_history`, **không có kênh `/internal/**`**, `MaQuyenAdmin` viết tay | `super-admin-service/CLAUDE.md`, `security/internal/config/AdminSecurityConfig.java:58`, `MaQuyenAdmin.java` |
| Kênh S2S sẵn có | cell-app → control-plane & report-service bằng `X-Internal-Token` (`PMKT_INTERNAL_TOKEN`), URL trực tiếp; `tenant-provisioning` có `InternalTokenSupport/Filter` làm mẫu; front-door **chỉ** route `/auth/**` và `/api/**` → cell | `cell-app/src/main/resources/application.yml:112,359-364`, `tenant-provisioning/…/core/security/InternalTokenSupport.java`, `front-door/src/main/resources/application.yml:22-32` |
| client-admin | module mẫu `features/quanTri/cauHinh`, menu `app/layouts/shell/menuRegistry.tsx`, breadcrumb dùng ns `app:` | `client-admin/CLAUDE.md` |
| Vị trí màn "Quản trị" ở client | nhóm QUẢN TRỊ: Thông tin công ty · Cấu hình chi tiết · Định dạng số; route `heThong/routes.tsx`, paths ở `heThong/paths.ts` (shape cũ ở cấp domain) | `client/src/app/layouts/shell/menuRegistry.tsx:473-497`, `features/heThong/paths.ts` |
| Theme | `colorPrimary = BRAND_RED`, antd v6 token, `@base` 219 component | `client/src/base/theme/antdTheme.ts:19`, `base/index.ts` |
| Git | `client` & `cell-app` ở `develop`, sạch; **`super-admin-service/` và `client-admin/` KHÔNG phải git repo** (`fatal: not a git repository`) | `git -C … status` 2026-09-17 |
| Migration cell-app | đánh số `V<max+1>`; **max hiện tại = 1146** | `cell-app/CLAUDE.md`, `ls db/migration` |

---

## 3. Quyết định kiến trúc (đề nghị — chốt qua §14)

| # | Quyết định | Vì sao | Vì sao KHÔNG phương án kia | Hệ quả lên code |
|---|---|---|---|---|
| **D1** | Schema JSON **theo khối** riêng (`MauInChungTu` v1) — không tái dùng `BieuMauDinhNghia` (lưới) | Yêu cầu là *bật/tắt · đổi nhãn · đổi thứ tự · kéo khối* trên mẫu chuẩn có sẵn; người dùng là admin công ty, không phải người thiết kế lưới | Dịch khối → lưới ô mất tính "khối" (kéo thả theo vùng, ẩn/hiện theo trường), lưới hợp nhất cột cho bảng 2 cột và bảng 13 cột rất xấu; engine lưới nằm ở `report-service` (thêm một nhịp S2S cho mỗi lần xem trước) | Schema + validator + renderer riêng; để ngỏ converter khối→lưới nếu sau cần xuất XLSX/DOCX |
| **D2** | Hai tầng mẫu, giải theo chuỗi `TUY_CHINH (cell) → MAC_DINH_HE_THONG (control plane) → MAC_DINH_DONG_GOI (code)`; **bản tuỳ chỉnh thắng tuyệt đối**; ghi `mac_dinh_phien_ban` để báo "mẫu chuẩn có bản mới" | Dự đoán được; không có "merge ba chiều" lặng lẽ lên bản in kế toán đã duyệt | Merge tự động thay đổi của super admin vào bản tenant ⇒ bản in đổi mà không ai bấm gì | `GiaiMauHieuLuc` (cell), badge + nút "Đặt lại theo mẫu chuẩn" (FE) |
| **D3** | **Catalog = code Java trong cell-app** (`MauInProvider` mỗi loại); mẫu chuẩn đóng gói **sinh** từ catalog (`MauChuanBuilder`); super-admin-service dùng **snapshot `catalog.json`** | Chỉ module chứng từ biết DTO/dòng chi tiết của nó; snapshot tránh mở thêm kênh cell→super-admin và tránh super-admin phụ thuộc một "cell tham chiếu" | Catalog viết tay ở FE/super-admin = bản sao thứ hai của luật; gọi live một cell buộc super-admin biết cell nào, `X-Cell-Id`, tenant… | Gradle task `xuatCatalogMauIn` + `tools/sync-catalog.sh`; test super-admin xác nhận snapshot parse được |
| **D4** | Lan mẫu mặc định: **cell pull + cache** (`GET /internal/mau-in/mac-dinh/{ma}`, ETag, TTL 10 phút, stale-while-error, fallback đóng gói) | Tự lành khi cell/super-admin tạm mất kết nối; không cần sổ đăng ký cell ở super-admin; không cần outbox | Push fan-out cần biết mọi cell + retry + trạng thái từng cell; copy lúc provisioning thì tenant cũ không bao giờ nhận mẫu mới; đọc `sa_*` qua tenant-provisioning là vượt quyền sở hữu bảng | super-admin-service thêm `InternalTokenSupport/Filter` (mirror tenant-provisioning) + `hasRole("INTERNAL")` cho `/internal/**`; cell-app thêm `PMKT_SUPER_ADMIN_URL` (bean `@ConditionalOnProperty`, thiếu ⇒ bỏ qua tầng 2, log một lần) |
| **D5** | **Render giai đoạn 1 = FE** (một renderer `MauInPaper` cho canvas + in qua cửa sổ in của trình duyệt, `@page` theo khổ); BE cấp `DuLieuIn` (A6). **Giai đoạn 2 (tuỳ chọn) = BE PDF** từ cùng JSON | WYSIWYG: thứ người dùng kéo thả chính là thứ được in; một renderer ⇒ không trôi; đỡ ~10–12 ngày Jasper động | BE-render-ngay đi ngược nhu cầu canvas tương tác (không click/kéo trên PDF), buộc hai renderer phải khớp từng pixel | ⚠ Đi ngược chốt A9 (2026-08-20) cho mẫu **pháp định cố định** — mẫu tuỳ chỉnh là ca khác; **Q1** |
| **D6** | Module `cell/mau_in/` (prefix `prn_`) sở hữu `api/` (`MauInApi`, SPI `MauInProvider`, DTO) và `internal/`; **không sửa `BaseChungTuController`**; endpoint in theo loại nằm ở `/api/mau-in/{ma}/chung-tu/{id}/…` | Tránh trùng mapping với `/{id}/mau-in` của thu/chi; kernel `accounting_core` không phụ thuộc module ngoại vi; provider của thu/chi chỉ cần **uỷ quyền** sang `MauInPhieuThuChi.choPhieu` để menu hợp nhất | Thêm endpoint vào base ⇒ 28 controller đổi hành vi cùng lúc, và `BaseChungTuThuChiController` phải `@Override` để không nổ `Ambiguous mapping` lúc boot | 28 module → `mau_in.api` (một chiều); `mau_in` → `core` (+ `platform_iam`? **không** — lấy thông tin đơn vị/người ký qua port `DonViInPort` do `platform_iam` cài) |
| **D7** | Quyền: một mã chức năng hệ thống **`HTMauIn.View/Edit`** cho màn thiết lập; in dùng `<ChucNang>.Print` sẵn có; super admin `MauInMacDinh.*` | "Admin của công ty" là vai trò cấp đơn vị; 1 mã seed thay vì 28 mã `PrintConfig` | Quyền theo loại chi tiết hơn nhưng nhân 28 dòng seed + 28 dòng ma trận phân quyền | `MaChucNang.HT_MAU_IN`, seed `iam_quyen`, `MaQuyenAdmin`; **Q4** |
| **D8** | Hợp nhất catalog khi tải (`hopNhat`) chạy **ở BE** cho mẫu hiệu lực (A2/A6/B2) **và** có bản TS trong engine để editor xử lý offline (client-admin) — cùng fixture vàng | Trường mới của form "tự xuất hiện" mà không cần migration dữ liệu; hai bản được ghim bằng test chung | Chỉ FE làm ⇒ bản in server-side (GĐ2) không thấy trường mới; chỉ BE làm ⇒ client-admin cần BE của cell | `HopNhatCatalog.java` ×2 (cell, super-admin) + `hopNhatVoiCatalog.ts`; **Q6** về `hien` mặc định |
| **D9** | Engine FE ở **`@domain-kit/mauIn`** (schema · helpers · renderer · editor · `NutInChungTu`), feature chỉ là adapter; **client-admin sao NGUYÊN thư mục** như luật sao `base/` | Cùng một editor cho hai console; `client-admin` không có cơ chế package chung ngoài sao chép | Đặt editor trong feature `heThong` thì client-admin phải import chéo domain (luật tầng cấm) | Thêm `export * from './mauIn'` ở `domainKit/index.ts`; script/ghi chú đồng bộ `client-admin/src/base/domainKit/mauIn` |
| **D10** | Định dạng số/ngày ở FE theo runtime tenant (`@domain-kit/dinhDangSo`); BE trả giá trị thô + kiểu; chỉ `soTienBangChu` BE tính | Nhất quán với mọi màn FE hiện có; một chỗ đọc chữ | BE định dạng sẵn ⇒ client-admin (không tenant) và FE phải hiểu chuỗi đã định dạng | `DuLieuIn.kieu`, prop `dinhDang` của renderer |
| **D11** | Khối chuẩn (`DON_VI · TIEU_DE · THONG_TIN · TONG_HOP · CHU_KY`) và mọi khối `BANG` của catalog **không xoá được, chỉ ẩn**; `DON_VI`/`TIEU_DE` còn **khoá vị trí**; chỉ `TU_DO` xoá/thêm được | Đúng mock ("khối của mẫu chuẩn thì không") + bổ sung #3; giữ cấu hình cột khi tạm ẩn bảng | Cho xoá bảng rồi "thêm lại" phải dựng lại cột từ đầu | INV-MAUIN-001/002/003, UI ẩn nút ✕ và tắt drag handle |
| **D12** | Nhãn in là dữ liệu tiếng Việt; chữ giao diện editor qua i18n **một namespace `mauIn`** trong engine; feature không mở namespace thứ hai cho editor | luật 2 + ngoại lệ §8 của `client/CLAUDE.md` | | `domainKit/mauIn/i18n/{vi,en,registerMauInI18n}.ts` |
| **D13** | Không ghi BA docs; đặc tả viết tay vào `docs/doing/mau-in-chung-tu-spec/` (4 file chuẩn) để `/plan-be` · `/gen-be` · `/gen-fe` · `trace.sh` · `/verify-spec` chạy được | `/audit-spec` cần thư mục PYC trong `pmkt-docs/ba/` — chưa có; skill cấm sửa BA gốc | | GĐ0 |
| **D14** | **Giao diện: bố cục/hành vi 1:1 theo mock, phong cách theo hệ thống, control 100 % từ `@base`; ba khoảng trống (`CommonSegmented` · `CommonColorPicker` · `PropField/PropSection`) bổ sung vào `@base`; CSS cục bộ "chế độ dày" theo 4 bậc (prop → CSS phần tử mình → thêm prop base → ghi đè antd có phạm vi)** — chốt của user 2026-09-17 | màn dày thông tin (bảng 7 cột trong panel 370px) mà body app 14px/field 32px quá thưa; bieuMau đã phải import antd `Segmented`/`ColorPicker` trần — lặp lần 2 là đủ điều kiện "≥2 màn ⇒ base" | copy component ra engine = bản sao thứ hai; giữ palette xanh của mock là lệch design system | chi tiết: [02-anh-xa-giao-dien-va-base-component.md](02-anh-xa-giao-dien-va-base-component.md); +2 ngày FE ở GĐ1 |

---

## 4. Kiến trúc tổng thể

```
 client-admin (5174)                                 client (5173)
 features/quanTri/mauInMacDinh  ──┐            ┌──  features/heThong/thietLapMauIn   (list 47 + editor host)
 @domain-kit/mauIn (bản sao)      │            │    @domain-kit/mauIn (gốc): schema · hopNhat · kiemTra
                                  │            │        MauInPaper (render) · MauInEditor · NutInChungTu
        /api/admin/mau-in/**      │            │    /api/mau-in/**  +  {base}/{id}/in (mẫu cố định sẵn có)
                                  ▼            ▼
 super-admin-service (8099)                 cell-app (8081)
 quan_tri/mau_in                            mau_in
   sa_mau_in_mac_dinh (TEXT JSON)             prn_mau_in_tuy_chinh (jsonb, RLS)
   catalog.json (snapshot từ cell-app)        api/: MauInApi · MauInProvider (SPI) · dto
   /internal/mau-in/mac-dinh/{ma} ◄────────── internal/client/MacDinhHeThongRest (X-Internal-Token, cache TTL)
              (X-Internal-Token)              internal/service: GiaiMauHieuLuc · HopNhatCatalog · KiemTraMau · ChuanHoaMau · MauChuanBuilder
                                              ▲ implements MauInProvider
                                    ban_hang · chung_tu_mua_hang · tien_mat_tien_gui · kho · … (28 module, mỗi loại một bean)

 Chuỗi giải mẫu hiệu lực (cell):  prn_mau_in_tuy_chinh(tenant, ma)  →  cache super-admin(ma)  →  MauChuanBuilder(provider.moTa())
                                  ─────── luôn đi qua hopNhat(catalog) + chuanHoa() trước khi trả ───────
```

---

## 5. Thiết kế BE — `cell-app` (module mới `cell/mau_in/`, tiền tố bảng `prn_`)

### 5.1 Cây module

```
cell/mau_in/
├── package-info.java                      @ApplicationModule(displayName = "mau_in")  — "mau_in ({@code prn_}) — mẫu in chứng từ theo khối"
├── api/
│   ├── package-info.java                  @NamedInterface("api")
│   ├── MauInApi.java                      mauHieuLuc(ma) · duLieuIn(ma, id) · menuIn(ma, id) — cho module khác (GĐ2: hach_toan? thue?) — CHỈ tạo nếu có người gọi; GĐ1 có thể chưa cần
│   ├── MauInProvider.java                 SPI (dưới)
│   └── dto/  package-info.java · MoTaMauIn · TruongCatalog · BangCatalog · DuLieuIn · ChungTuTomTat · MucMenuIn · VaiTroKy
└── internal/
    ├── controller/MauInController.java    /api/mau-in/** (A1–A7), package-private
    ├── dto/  LuuMauInRequest · MauInHieuLucDto · LoaiChungTuMauInDto · ThayDoiHopNhatDto
    ├── entity/MauInTuyChinh.java          prn_mau_in_tuy_chinh, extends AggregateRootEntity, @JdbcTypeCode(SqlTypes.JSON) String cauHinh, @Version
    ├── model/  MaLoiMauIn (MSG_MAUIN_*) · NguonMau · GioiHanMauIn (hằng §5.3 hợp đồng) · json/ (record Jackson của schema §1)
    ├── port/DonViInPort.java              tên/địa chỉ/MST đơn vị gốc + 5 người ký + 2 cờ — platform_iam cài (tránh mau_in → platform_iam.internal)
    ├── repository/MauInTuyChinhRepository.java
    ├── client/  MacDinhHeThongClient (interface) · MacDinhHeThongRest (RestClient + X-Internal-Token, timeout 2s/5s) · MacDinhHeThongCache (ConcurrentHashMap<ma, {json, phienBan, etag, hetHan}>)
    └── service/
        ├── MauInService.java              điều phối @Transactional; A1–A7
        └── business/  DangKyProvider (Map<ma, MauInProvider> từ List<MauInProvider>, kiểm trùng mã lúc boot)
                       · MauChuanBuilder · HopNhatCatalog · KiemTraMau · ChuanHoaMau · GiaiMauHieuLuc · MauInJson (Jackson strict, FAIL_ON_UNKNOWN_PROPERTIES=true)
```

Cấu hình (chốt khi code, 2026-09-17 — `ProxyArchTest` cấm dựng `RestClient` ngoài `integration_ops.proxy`):
`pmkt.mau-in.super-admin.enabled: ${PMKT_MAU_IN_SUPER_ADMIN_ENABLED:false}` (tắt = bỏ tầng 2, dùng mẫu đóng gói),
`pmkt.mau-in.super-admin.ttl: ${PMKT_MAU_IN_MAC_DINH_TTL:10m}`; URL / token / timeout nằm ở đích proxy
`pmkt.proxy.targets.super-admin` (`base-url: ${PMKT_SUPER_ADMIN_URL:http://super-admin-service:8080}`, `read-timeout: 3s`,
`auth.type: INTERNAL_TOKEN` dùng lại `PMKT_INTERNAL_TOKEN`, `resilience.retry.enabled: false` — không thử lại trên đường xem chứng từ);
hằng `ProxyTargetId.SUPER_ADMIN`; client `MacDinhHeThongRest` gọi `ProxyClient.exchange` kèm `If-None-Match` (304 / 404 / 200).

### 5.2 SPI `MauInProvider` (mỗi loại chứng từ một bean trong module của nó)

```java
public interface MauInProvider {
    String maLoaiChungTu();                          // "MDV" — phải tồn tại trong mst_loai_chung_tu (test đồng bộ)
    MoTaMauIn moTa();                                // catalog + gợi ý mẫu chuẩn (bất biến, có thể static final)
    DuLieuIn duLieuMau();                            // dữ liệu mẫu tĩnh — dùng ở cả super admin
    DuLieuIn duLieuIn(UUID chungTuId);               // đi qua service().layChiTiet(id) của module — tự kẹp tenant/quyền
    List<ChungTuTomTat> chungTuGanDay(String tuKhoa, int gioiHan);
    default List<MucMenuIn> mauCoDinh(UUID chungTuId) { return List.of(); }   // thu/chi: MauInPhieuThuChi.choPhieu(...)
}
```

`DonViInPort` cấp phần chung (đơn vị, người ký) — provider **không** tự truy `Tenant`. Với
`layTenNguoiLapPhieuTuNguoiDungDangNhap = true`, `nguoiKy.NGUOI_LAP.ten` lấy từ người tạo chứng từ (đã có trên
`BaseChungTuEntity.nguoiTao`), không phải người đang in — ghi rõ ở javadoc, kiểm bằng test (BA không nói, **Q**
trong `01-conflict.md`).

### 5.3 Ba provider pilot

| Loại | Module | Lý do chọn | Bảng chi tiết (catalog `bang[]`) |
|---|---|---|---|
| `MDV` Chứng từ mua dịch vụ | `chung_tu_mua_hang` (`ChungTuMuaDichVuController`) | đúng loại của mock — đối chiếu 1:1 bố cục | `hachToan` (dòng dịch vụ) · `thue` |
| `BH` Chứng từ bán hàng | `ban_hang/chung_tu_ban_hang` | module tham chiếu duy nhất đạt chuẩn; nhiều bảng (hàng hoá · thuế · chi phí/hoá đơn kèm) — thử `BANG` ×N | theo `ChiTietChungTuBanHangDto` + `HoaDonKemDto` |
| `PT` Phiếu thu tiền mặt | `tien_mat_tien_gui` | đã có mẫu cố định Jasper ⇒ kiểm **hợp nhất menu** `CO_DINH + TUY_CHINH` và uỷ quyền `mauCoDinh()` | `hachToan` (`DongHachToanDto`) |

Rollout 25 loại còn lại: mỗi module chủ tự cài provider theo **hướng dẫn 1 trang** `02-huong-dan-viet-provider.md`
(viết ở GĐ1 sau khi MDV chạy) + test pin khoá trường (`MdvMauInProviderTest` làm khuôn).

### 5.4 Điểm chạm ngoài module

| File | Sửa gì |
|---|---|
| `common/constant/MaChucNang.java` | `HT_MAU_IN = "HTMauIn"` (nhóm HT*, javadoc: View, Edit) |
| `db/migration/V<max+1>__prn_mau_in_tuy_chinh.sql` · `V<max+2>__iam_quyen_ht_mau_in.sql` | bảng + RLS + seed quyền (khuôn `V1111`) |
| `platform_iam/tenant/**` | bean cài `mau_in.internal.port.DonViInPort`? — **không được** (port nằm trong `internal`). Đặt port ở `mau_in/api/DonViInPort.java` (`@NamedInterface`), `platform_iam` cài; `mau_in` không import `platform_iam` |
| `tien_mat_tien_gui/internal/service/…PtMauInProvider.java` | provider + uỷ quyền `mauCoDinh` |
| `src/test/java/…/mau_in/MauInModularityTest.java` | mẫu `ProxyModularityTest` — chỉ soi vi phạm nhắc `mau_in`; **module mới sạch tuyệt đối** |
| `src/test/java/…/mau_in/XuatCatalogMauInTest.java` + task Gradle `xuatCatalogMauIn` | sinh `build/mau-in/catalog.json` (D3) |

### 5.5 Test (`@Tag("unit")`, song ánh cây `main`)

`MauChuanBuilderTest` (snapshot = fixture `mdv.mau-chuan.json`) · `HopNhatCatalogTest` (6 fixture) · `KiemTraMauTest`
(mỗi R-MAUIN một ca đỏ/xanh, tên test mang mã luật) · `ChuanHoaMauTest` · `GiaiMauHieuLucTest` (3 tầng + fallback khi
client ném) · `MacDinhHeThongCacheTest` (TTL, ETag 304, stale-while-error) · `DangKyProviderTest` (trùng mã ⇒ fail boot;
mọi `maLoaiChungTu` ∈ danh sách 47 mã) · `MdvMauInProviderTest` (pin từng khoá trường/cột) · `MauInModularityTest`.
Controller/repository: không viết test Testcontainers (Docker cấm) — kiểm qua IntelliJ run configuration, báo rõ.

---

## 6. Thiết kế BE — `super-admin-service` (module `quan_tri/mau_in/`)

```
quan_tri/mau_in/
├── package-info.java                      (sub-module của quan_tri, giống cau_hinh)
└── internal/
    ├── controller/  MauInMacDinhController (/api/admin/mau-in, B1–B4)  ·  MauInNoiBoController (/internal/mau-in, B5–B6)
    ├── dto/  …
    ├── entity/MauInMacDinh.java           sa_mau_in_mac_dinh, extends BaseEntity, @Version phienBan
    ├── repository/MauInMacDinhRepository.java
    └── service/  MauInMacDinhService · business/{CatalogSnapshot (đọc resources/mau-in/catalog.json một lần, kiểm catalogVersion),
                  HopNhatCatalog, KiemTraMau, ChuanHoaMau, MauInJson}   ← BẢN SAO của cell-app, cùng fixture (D8)
security/internal/  + InternalTokenSupport · InternalTokenFilter (mirror tenant-provisioning) ; AdminSecurityConfig: `/internal/**` → hasRole("INTERNAL")
security/internal/controller/MaQuyenAdmin.java  + MAU_IN_MAC_DINH = View · View.Detail · Edit · Delete
resources/  mau-in/catalog.json · db/migration/common/V4__sa_mau_in_mac_dinh.sql (+ postgresql/V5 tuỳ chọn) · application.yml: pmkt.internal-token
```

Ghi chú bắt buộc trong javadoc `AdminSecurityConfig`: cập nhật đoạn "Không có kênh `/internal/**`" (dòng 58) thành
mô tả kênh mới, chỉ đọc, chỉ `/internal/mau-in/**`. Profile `local` (H2) cần `PMKT_INTERNAL_TOKEN` trong run
configuration — không đặt default trong yml (luật 7; `InternalTokenSupport` fail-fast như tenant-provisioning).

Test: `KienTrucModuleTest` (có sẵn, tự phủ module mới) · `MauInMacDinhServiceTest` (lưu/kiểm/409/xoá mềm) ·
`CatalogSnapshotTest` (snapshot parse được, đủ 47 mã hoặc log rõ mã thiếu) · `MauInNoiBoControllerTest` (403 thiếu
token, 304 ETag) trên H2.

---

## 7. Thiết kế FE — `client`

### 7.1 Engine `src/base/domainKit/mauIn/` (D9) — cấu trúc theo §3 `fe-khung-kien-truc-chuan.md`

```
mauIn/
├── index.ts                    cửa ra duy nhất: MauInEditor · MauInPaper · NutInChungTu · mauInSchema · types · hopNhatVoiCatalog · kiemTraMau · chuanHoaMau · moCuaSoIn · registerMauInI18n
├── api/         mauInSchema.ts (Zod v1 + nangCap) · catalogSchema.ts · duLieuInSchema.ts · menuInSchema.ts
├── components/  MauInEditor.tsx (khung 3 cột, adapter) · EditorToolbar.tsx · BoCucPanel.tsx (outline + dnd + kiểm tra) · XemTruocPanel.tsx (zoom · khổ · nguồn dữ liệu)
│                · MauInPaper.tsx (RENDERER thuần — dùng cho canvas VÀ in; prop `cheDo: 'XEM' | 'SUA'`)
│                · khối: KhoiDonVi.tsx · KhoiTieuDe.tsx · KhoiThongTin.tsx (bảng n cột) · KhoiBang.tsx · KhoiTongHop.tsx · KhoiChuKy.tsx · KhoiTuDo.tsx
│                · inspector: ThietLapTrangForm.tsx · DonViForm.tsx · TieuDeForm.tsx · ThongTinForm.tsx · BangForm.tsx · TongHopForm.tsx · ChuKyForm.tsx · TuDoForm.tsx · BangDongKeoTha.tsx (bảng dòng có ⠿, dùng chung 5 form)
│                · NutInChungTu.tsx (split button `In | ˅`, menu A7, mục "⚙ Thiết lập mẫu in…")
│                · mauIn.css (một stylesheet, tiền tố `.pmkt-mau-in-*`; phần giấy `.pmkt-mau-in-giay` + `@media print` + `@page`)
│                └── modal/  ChonTruongDuLieuModal.tsx · ChonChungTuModal.tsx · XacNhanModal.tsx (dùng UiModal, BR3)
├── constants/   constants.ts (§5.3 hợp đồng · ID khối chuẩn · DND prefix)
├── fields/      types.ts (suy từ Zod) · options.ts (font, màu, khổ, căn, kẻ ô — nhãn qua t())
├── helpers/     hopNhatVoiCatalog.ts · kiemTraMau.ts (R-MAUIN-…) · chuanHoaMau.ts · mauChuanTuCatalog.ts (chỉ cho test/so sánh) · doiViTri.ts · keoThaKhoi.ts (id dnd) · dungHtmlIn.ts (renderToStaticMarkup + CSS + @page) · moCuaSoIn.ts
├── hooks/       useMauInEditorStore.ts (zustand + immer + zundo, 60 bước; selection/zoom ngoài lịch sử) · useMauInHotkeys.ts · useKeoThaKhoi.ts · useDuLieuXemTruoc.ts
├── i18n/        vi.ts · en.ts · registerMauInI18n.ts   (ns `mauIn`; chữ của inspector là nhánh con: `mauIn:khoi.bang.*`)
└── test/        schema · hopNhat (fixture vàng) · kiemTra (mỗi luật) · chuanHoa · store (undo/redo, dirty) · MauInPaper.render.test.tsx (snapshot MDV) · NutInChungTu.test.tsx · keoTha
```

Ghi chú: engine không có `pages/`; stylesheet đặt ở `components/mauIn.css` (một file, tiền tố lớp) — nêu rõ trong
`index.ts` để review khỏi bắt "CSS phải ở pages/".

**Adapter** (feature cấp cho editor, không có React/mạng bên trong engine ngoài adapter):

```ts
interface MauInEditorAdapter {
  phamVi: 'DON_VI' | 'HE_THONG'                       // đổi tag + câu thông báo lưu
  tenLoaiChungTu: string
  tai(): Promise<{ mau; catalog; nguon; phienBan; macDinh: { mau; nguon; phienBan }; duLieuMau; thayDoi }>
  luu(mau, phienBan): Promise<{ phienBan }>
  duLieuXemTruoc?: { timChungTu(q): Promise<ChungTuTomTat[]>; layChungTu(id): Promise<DuLieuIn> }   // tenant only
  dinhDang: { so(v, kieu): string; ngay(v): string }
  lienKet?: { thongTinCongTy?: string; troVe?: string }  // BR35
}
```

"Đặt lại mẫu chuẩn" = nạp `macDinh.mau` vào editor (chưa lưu, đúng mock); "Dùng lại mẫu chuẩn" ở màn danh sách =
`DELETE` (A4/B4) sau xác nhận.

### 7.2 Kéo thả (F14) — `@dnd-kit/core` (có sẵn) + đề nghị thêm `@dnd-kit/sortable` + `@dnd-kit/utilities` (Q10)

- Một `DndContext` bao cả outline và canvas; mỗi khối là `useSortable({ id, disabled: khoa?.viTri })`; hai vùng
  dùng chung một mảng `khoi` ⇒ kéo ở đâu cũng đổi cùng state, không có "hai nguồn thứ tự".
- `DON_VI`/`TIEU_DE`: không draggable, không phải đích thả; thuật toán `doiViTri(tu, den)` từ chối `den < 2`
  (R-MAUIN-020) — ghim bằng test.
- Dòng trong bảng inspector (`BangDongKeoTha`) là sortable riêng theo khối (giữ hành vi mock).
- Bàn phím: Alt+↑/↓ đổi vị trí khối đang chọn (dnd-kit sortable đã có keyboard sensor).

### 7.3 In mẫu tuỳ chỉnh (`NutInChungTu`)

1. Mount ⇒ `GET /api/mau-in/{ma}/menu?chungTuId=` (giống `NutInPhieu`: nạp ngay, không lười).
2. Mục `CO_DINH` ⇒ gọi `onInMauCoDinh(ma)` do module truyền (nganQuy dùng `moBanIn` sẵn có); các loại khác chưa có mẫu cố định.
3. Mục `TUY_CHINH` ⇒ `GET …/chung-tu/{id}/du-lieu-in` → `dungHtmlIn(MauInPaper, mau, duLieu)` → `moCuaSoIn(html)`:
   mở cửa sổ mới bằng blob URL (không điều hướng `/api/...` trần — bài học 401 trong `inPhieuApi.ts`), CSS tự chứa,
   `@page { size: A4 portrait; margin: <lề> }`, `thead { display: table-header-group }` cho `lapTieuDeCot`,
   gọi `print()` sau `load`.
4. Mục "⚙ Thiết lập mẫu in…" chỉ hiện khi có `HTMauIn.Edit` (BR25 — ẩn, không disable); điều hướng
   `/he-thong/thiet-lap-mau-in/{ma}?chungTuId=&troVe=` (BR35 giữ ngữ cảnh).

Tích hợp pilot: `muaHang/chungTuMuaDichVu` (kiểm module đang chạy qua `RootRoutes.tsx` trước), `banHang/chungTuBanHang`,
và mở rộng `nganQuy/_shared/components/NutInPhieu.tsx` → dùng `NutInChungTu` với `onInMauCoDinh = moBanIn`.

### 7.4 Feature tenant `src/features/heThong/thietLapMauIn/`

```
thietLapMauIn/
├── index.ts
├── api/        thietLapMauInApi.ts (A1–A6, Zod) · queries.ts (TanStack, key theo tenant)
├── components/ LoaiChungTuTable.tsx (CommonListTable: Mã · Tên · Nhóm · Trạng thái mẫu · Dựa trên mẫu chuẩn v · Cập nhật · Người cập nhật · Thao tác) · ThietLapMauInHost.tsx (dựng adapter → MauInEditor) · modal/DungLaiMauChuanModal.tsx
├── constants/  constants.ts (BASE_PATH `/api/mau-in`) · paths.ts (`thietLapMauIn`, `thietLapMauInChiTiet(ma)`) · permissions.ts (`HTMauIn.View/Edit`)
├── fields/     columns.tsx · types.ts · trangThaiBadge.ts
├── helpers/    tenTrangThaiMau.ts
├── hooks/      useLoaiChungTuMauIn.ts · useMauInAdapter.ts
├── i18n/       vi.ts · en.ts · registerThietLapMauInI18n.ts (ns `thietLapMauIn`: `menu.title`, `list.*`, `host.*`)
├── pages/      ThietLapMauInPage.tsx (danh sách) · ThietLapMauInChiTietPage.tsx (route `/:ma`, chỉ ráp Host) · thietLapMauIn.css
└── test/
```

Nối app: `heThong/paths.ts` thêm 2 path (giữ lệ của domain); `heThong/routes.tsx` thêm 2 route (`perm: HTMauIn.View`,
crumb `app:shell.menu.groupAdmin` + `thietLapMauIn:menu.title`); `menuRegistry.tsx` nhóm QUẢN TRỊ thêm mục
`thiet-lap-mau-in` (icon `PrinterIcon`, `anyOf: [HT_MAU_IN_PERM.view]`); `app/i18n/{vi,en}.ts` thêm `shell.menu.thietLapMauIn`.
Route chi tiết dùng layout **toàn khung** (ẩn padding trang) — kiểm `AppLayout` có hỗ trợ handle `fullBleed` chưa;
nếu chưa thì thêm cờ vào handle thay vì CSS hack.

### 7.5 Trạng thái editor & cổng UX

- Store: `mau` (trong lịch sử undo) · `daLuu` (JSON snapshot) · `dirty = JSON(mau) !== daLuu` · `chon` · `zoom` ·
  `nguonXemTruoc` (ngoài lịch sử). Gõ liên tục vào ô nhãn: cập nhật `mau` trực tiếp, `push` lịch sử ở `blur/change`
  (đúng mock `input` vs `change`).
- Toast `useToast` (BR26). Xác nhận đóng khi dirty dùng đúng chữ BR3: *"Dữ liệu đã có thay đổi. Bạn có chắc chắn muốn
  đóng? Thay đổi sẽ không được lưu."* Xoá khối tự do dùng khuôn "Xác nhận xóa" BR3. Esc = Đóng, click ngoài = huỷ.
- Nút Lưu `disabled` khi còn lỗi; cảnh báo không chặn. Ctrl+S khi còn lỗi ⇒ toast lỗi đầu tiên (mock).
- BR25: route 403 khi thiếu `HTMauIn.View`; BE kiểm lại mọi yêu cầu.

### 7.6 Style theo hệ thống (F18) — chi tiết ở [02-anh-xa-giao-dien-va-base-component.md](02-anh-xa-giao-dien-va-base-component.md)

- **Bố cục & hành vi 1:1 mock** (3 cột 250 / 1fr / 370, thứ tự panel-mục-control, undo/redo, kiểm tra, kéo thả).
- **Token hệ thống thay palette mock**: `#2b5f9e` → `BRAND_RED`; `#e8f0fa` → `PRIMARY.bg`; `#f59e0b` (khối chọn) →
  viền `BRAND_RED` + `--ui-brand-soft`; `#eef1f5` → `colorBgLayout`; `#dfe3e8` → `colorBorderSecondary`; Segoe UI →
  Roboto; toast dời lên góc phải trên (BR26). **Giấy** giữ Times New Roman/đen (bản in, không phải UI).
- **Control 100 % `@base`** (đã đối chiếu barrel `client/src/base/index.ts` 2026-09-17): `PageHeader` · `Toolbar` ·
  `CommonButton` (variant/size small) · `CommonTextBox` · `CommonNumberInput` · `CommonSelectBox` · `CommonCheckbox` ·
  `CommonSlider` · `ListTag` · `CommonTitle/CommonText` · `UiModal` · `CommonConfirmModal` + `useDiscardGuard` ·
  `CommonComboGrid` (chọn chứng từ khác) · `CommonDropdownButtonTwofold` (nút In) · `useToast` · icon barrel `base/icons`.
- **Bổ sung vào `@base`** (2 ngày, làm ở client rồi sao sang client-admin): `CommonSegmented`, `CommonColorPicker`,
  `PropField`/`PropSection` (nâng từ bieuMau), 3 icon thiếu, tuỳ chọn `handle.fullBleed` cho `AppLayout`.
- **CSS cục bộ "chế độ dày"** (chốt user 2026-09-17) trong `mauIn.css` tiền tố `.pmkt-mau-in-*`: field 24px, hàng 28px,
  chữ 12px, gap 4/8 — theo 4 bậc, không hex trần ngoài khối giấy, không selector antd v5.
- Checklist nghiệm thu giao diện: file 02 §5 (grep không còn mã màu mock; engine không import control antd trần…).

---

## 8. Thiết kế FE — `client-admin`

- Sao **nguyên** `client/src/base/domainKit/mauIn/` → `client-admin/src/base/domainKit/mauIn/` + `export` ở
  `domainKit/index.ts` (luật sao khung vỏ). Thêm script `client-admin/tools/sync-domain-kit-mau-in.ps1` (copy + diff) và
  test `domainKit/mauIn/test/dongBoVoiClient.test.ts` so hash để không lệch lặng.
- Feature `src/features/quanTri/mauInMacDinh/` (sao khuôn `quanTri/cauHinh`): `api/` (B1–B4), `components/`
  (`LoaiChungTuTable`, `MauInMacDinhHost` — adapter `phamVi: 'HE_THONG'`, không `duLieuXemTruoc`), `constants/`
  (`/quan-tri/mau-in`, `/quan-tri/mau-in/:ma`; `MauInMacDinh.*`), `i18n/`, `pages/`, `test/`.
- Nối: `quanTri/routes.tsx` (+2 route, `crumbs` ns `app:`), `menuRegistry.tsx` (+1 leaf), `app/i18n` (+`shell.menu.mauInMacDinh`).
- Định dạng số/ngày trong preview: `Intl` vi-VN mặc định (không có runtime tenant).

---

## 9. Luồng nghiệp vụ chính

| # | Luồng | Các bước |
|---|---|---|
| L1 | Super admin sửa mẫu mặc định MDV | client-admin `GET /api/admin/mau-in/MDV` (đóng gói + catalog + dữ liệu mẫu) → sửa → kiểm → `PUT` (phienBan 0→1) → `sa_mau_in_mac_dinh` |
| L2 | Tenant chưa tuỳ chỉnh in MDV | client `GET /api/mau-in/MDV/chung-tu/{id}/du-lieu-in` → cell `GiaiMauHieuLuc`: không có override → cache miss → `GET super-admin /internal/mau-in/mac-dinh/MDV` (ETag) → hợp nhất catalog → trả `{mau, duLieu}` → FE in |
| L3 | Admin đơn vị tuỳ chỉnh | từ menu In "⚙ Thiết lập mẫu in…" (mang `chungTuId`) → `GET /api/mau-in/MDV` (hiệu lực = bản super admin v1, `macDinh.phienBan=1`) → sửa → `PUT` → `prn_mau_in_tuy_chinh(mac_dinh_phien_ban=1)` → quay về chứng từ (BR35) |
| L4 | Super admin đổi mẫu (v2) sau L3 | tenant có override: bản in **không đổi**; màn danh sách hiện `coMacDinhMoi` + gợi ý "Đặt lại theo mẫu chuẩn" (D2). Tenant không override: nhận v2 sau tối đa TTL |
| L5 | Form MDV thêm ô mới | provider thêm `TruongCatalog` → `hopNhat` thêm trường vào `THONG_TIN` mọi bản (theo Q6) → editor báo "Có 1 trường mới" |
| L6 | super-admin-service không kết nối được | cache còn hạn ⇒ dùng; hết hạn ⇒ dùng bản stale + log WARN (một lần/ma/5 phút); chưa từng có ⇒ mẫu đóng gói, `nguon = MAC_DINH_DONG_GOI` hiển thị cho admin biết (MSG_MAUIN_020) |

---

## 10. Bộ luật cho `docs/doing/mau-in-chung-tu-spec/02-rules.md` (seed — hoàn thiện ở GĐ0)

Ngoài R-MAUIN-010…025 (kiểm tra, xem hợp đồng §5.1), các nhóm luật cần có mã để `trace.sh` đếm:

| Nhóm | Mã | Nội dung | Tầng |
|---|---|---|---|
| Quyền | R-MAUIN-001…004 | menu/route/API theo `HTMauIn.View/Edit`; in theo `.Print`; chọn chứng từ thật theo `.View`; super admin `MauInMacDinh.*` | CẢ HAI |
| Giải mẫu | R-MAUIN-030…034 | chuỗi 3 tầng; override thắng; ghi `mac_dinh_phien_ban`; `coMacDinhMoi`; fallback khi lỗi mạng | BE |
| Hợp nhất | R-MAUIN-040…046 | 6 bước §4 hợp đồng + `thayDoi` | CẢ HAI |
| Khoá khối | R-MAUIN-050…053 | `DON_VI`/`TIEU_DE` cố định vị trí 0/1, không xoá; khối chuẩn & `BANG` không xoá; chỉ `TU_DO` thêm/xoá; tối đa 4 ô ký | CẢ HAI |
| Editor | R-MAUIN-060…068 | undo 60 bước; dirty; Ctrl+S/Z/Y/Esc; xác nhận đóng (chữ BR3); đặt lại mẫu chuẩn không lưu; zoom 40–160 %; nguồn xem thử; lưu chuẩn hoá cột về 100 % | FE |
| In | R-MAUIN-070…074 | menu `CO_DINH + TUY_CHINH + ⚙`; in qua blob URL; `@page` theo khổ/lề; lặp `thead`; số tiền bằng chữ từ BE | CẢ HAI |
| Lưu trữ | INV-MAUIN-006…008 | unique (tenant, ma) sống; `schema_version` = `cauHinh.schemaVersion`; JSON qua `KiemTraMau` mới được ghi | BE |

Mỗi luật để lại mã ở nơi hiện thực + tên test (`docs/rules/truy-vet-luat.md`). Message theo mã `MSG_MAUIN_nnn`
(bảng ở hợp đồng §5.1 + `_015` lưu thành công, `_016` mẫu chuẩn có bản mới, `_018` 409, `_019` loại chưa hỗ trợ, `_020` fallback).

---

## 11. BR — đã đọc khi lập kế hoạch và phải đọc lại trước khi gen

| Phạm vi | BR | Áp vào đâu |
|---|---|---|
| **Đã đọc** (br.sh) | 3 · 4 · 9 · 16 · 25 · 26 · 30 | popup/xác nhận · danh mục 47 loại · message chung · phân quyền 5 cấp · toast · "≥1 trường hiển thị" |
| Màn danh sách 47 loại | 1 2 11 13.1 30 31 32 38 39 44 45 | `LoaiChungTuTable` (CommonListTable đã phủ phần lớn; 47 dòng — phân trang mặc định) |
| Form/inspector | 3 13.2 14 15 24 34 43 | validation, tooltip/help text (`.hint` của mock), trim |
| Thông báo | 16 26 27 | toast + trang 403 (`MSG_COMMON_002`) |
| Entity/DB/API | 7 19 20 28 29 46 | audit, xoá mềm, multi-tenant/RLS, làm tròn số ở renderer |
| Danh mục mặc định | 23 47 | mẫu chuẩn đóng gói là "dữ liệu mặc định" của danh mục — cách seed/khôi phục |
| Điều hướng | 35 | quay về chứng từ sau khi thiết lập |
| Ngày/Số | 7 8 18 | định dạng trong `MauInPaper` qua runtime tenant |

Tài liệu im lặng ở các điểm §14 → **không tự đặt luật**, ghi `OPEN` trong `01-conflict.md`.

---

## 12. Kế hoạch triển khai

### 12.1 Giai đoạn & ước lượng (ngày công, 1 BE + 1 FE làm song song; chưa gồm review/QA)

| GĐ | Nội dung | BE | FE | Đầu ra / cổng |
|---|---|---|---|---|
| **0 · Chốt & khung** (tuần 0, 2–3 ngày) | Trả lời §14 · viết `docs/doing/mau-in-chung-tu-spec/{00-source-map,01-conflict,02-rules,03-scenarios}.md` từ mock + §10 · fixture vàng §10 hợp đồng · `git init`/gắn remote cho `super-admin-service`, `client-admin` (Q15) · nhánh `feat/mau-in-chung-tu` ở 4 repo · (tuỳ chọn) mock Figma theo theme | 1 | 1 | spec xanh `01-conflict` không còn P0/P1 OPEN chặn GĐ1 |
| **1 · Lõi tenant + MDV** (tuần 1–2) | module `mau_in` (entity · migration · repo · service · business · controller A1–A7) · SPI · `DonViInPort` · provider **MDV** · seed quyền · test | 7 | **bổ sung `@base`** (`CommonSegmented` · `CommonColorPicker` · `PropField/PropSection` · icon · showcase — file 02 §4) · engine `@domain-kit/mauIn` (schema · helpers · store · renderer · editor 7 inspector · dnd · checks · i18n · `mauIn.css` chế độ dày) · feature `thietLapMauIn` · `NutInChungTu` + tích hợp MDV · in qua cửa sổ in | 13 | demo end-to-end trong tenant: sửa mẫu MDV → in; checklist giao diện file 02 §5; `./gradlew unitTest`; `npx vitest run src/base/domainKit/mauIn src/features/heThong/thietLapMauIn`; `npx vite build` |
| **2 · Super admin + lan mẫu** (tuần 3) | super-admin-service module `quan_tri/mau_in` · kênh `/internal` · snapshot catalog + task xuất + script sync · cell `MacDinhHeThongRest` + cache · provider **BH**, **PT** (hợp nhất menu) | 6 | client-admin: sao engine + feature `mauInMacDinh` + route/menu · client: tích hợp NutIn vào BH, nganQuy | 4 | L1→L2→L4 chạy thật (2 service local, H2); `./gradlew unitTest` cả 2 BE; `npx vitest`/`vite build` cả 2 FE |
| **3 · Hoàn thiện** (tuần 4) | hardening: 409, ETag, fallback, log; `XuatCatalogMauIn` ổn định; hướng dẫn provider 1 trang; `/verify-spec` | 3 | undo/redo hoàn chỉnh, kéo thả canvas + bàn phím, khối tự do, hộp thoại chọn chứng từ, zoom/fit, a11y, `check:committed`; `/verify-spec` | 4 | bảng truy vết `Rule → Code → Test` không còn ❌; `trace.sh … be|fe` không `MISSING` |
| **4 · Rollout 25 loại** (song song, theo chủ module) | mỗi loại: provider + test pin khoá + tích hợp `NutInChungTu` | 0,5–1/loại | 0,25/loại | danh sách 47 loại không còn "Chưa hỗ trợ" |
| **5 · Tuỳ chọn** | BE PDF từ JSON (Jasper động trong `mau_in`, cập nhật `InPhieuJasperArchTest`), logo/ảnh nền qua `common/storage`, tenant-specific default ở super admin | 10–12 | 2 | theo Q1/Q7/Q14 |

Tổng GĐ0–3 ≈ **17 BE + 22 FE ≈ 39–47 ngày công** (biên ±20 %). Ước lượng, không phải cam kết.

### 12.2 Thứ tự làm & phụ thuộc

`spec + fixture` → (BE) `schema records → MauChuanBuilder → HopNhat/KiemTra/ChuanHoa → provider MDV → service/controller`
song song (FE) `Zod → helpers (chạy fixture) → renderer → store → editor → feature` → ghép qua A2/A6 → super admin →
kênh internal → cache. FE có thể chạy sớm bằng fixture `mdv.*.json` làm mock của A2 trước khi BE xong (mock chỉ trong
`test/`, không có `mock.ts` trong module — nợ đã ghi ở `fe-no-ky-thuat-va-su-co.md`).

### 12.3 Quy ước Git & cổng nghiệm thu (theo `conventions-chung.md §4`, `client/CLAUDE.md §15`, `cell-app/CLAUDE.md`)

- Nhánh mỗi repo: `feat/mau-in-chung-tu`; commit `feat(mauIn): …` / `feat(mau_in): …`; không commit thẳng `develop`.
- `git add` file mới **trước** khi sửa barrel; `git status` sạch trước khi báo; FE chạy `npm run check:committed` sau commit.
- Cổng: `cd cell-app && ./gradlew unitTest` · `cd super-admin-service && ./gradlew unitTest` ·
  `cd client && npx vitest run <module> --reporter=dot && npx vite build` (cùng lệnh cho `client-admin`) ·
  `./docs/rules/trace.sh docs/doing/mau-in-chung-tu-spec be|fe` · 4 lệnh nặng FE chỉ khi user yêu cầu.
- Không Docker: test Testcontainers **không chạy**, báo rõ; chạy service qua IntelliJ (`mcp__idea__*`) — phiên này
  server `idea` không kết nối được, cần user mở lại trước GĐ1.

---

## 13. Rủi ro & giảm thiểu

| # | Rủi ro | Giảm thiểu |
|---|---|---|
| R1 | **Hai bản thuật toán** (`hopNhat`/`kiemTra`/`chuanHoa`) ở TS và Java trôi nhau | fixture vàng chạy ở cả 4 codebase; đổi fixture = đổi hợp đồng, PR phải chạm cả hai |
| R2 | Snapshot `catalog.json` ở super-admin cũ hơn cell (module mới thêm trường) | `catalogVersion` hiển thị ở màn super admin; `hopNhat` ở cell dung nạp trường lạ; CI/hook nhắc chạy `sync-catalog.sh` khi provider đổi |
| R3 | Mã `mst_loai_chung_tu.code` lệch giữa BA / seed / migration (`CTNHD`, `PTT`, `BCTG`) | test `DangKyProvider` đối chiếu mã provider với bảng thật lúc boot (log lỗi rõ); danh sách 47 lấy từ DB, không hardcode ở FE |
| R4 | In từ trình duyệt khác nhau về ngắt trang/lề | `@page` + `break-inside: avoid` cho khối ký; `thead` lặp; kiểm Chrome/Edge (đối tượng chính); PDF BE ở GĐ5 nếu cần |
| R5 | Đi ngược chốt A9 "render thuộc BE" | nêu tường minh ở Q1; mẫu pháp định cố định vẫn BE render; thiết kế A6 để GĐ5 thêm PDF không đổi hợp đồng |
| R6 | `super-admin-service`, `client-admin` chưa có git ⇒ không commit/review được | GĐ0 khởi tạo repo/remote (Q15) trước khi viết code |
| R7 | Kéo thả trên canvas làm chậm khi bảng nhiều dòng | canvas render tối đa 20 dòng/bảng khi `cheDo='SUA'` + ghi "…và N dòng nữa"; in dùng đủ dữ liệu |
| R8 | Font chọn trong mẫu không có trên máy người dùng | whitelist 6 font + fallback CSS (`Liberation Serif`, `serif`); ghi chú ở inspector |
| R9 | Provider của module khác quên kẹp phạm vi/quyền khi `duLieuIn(id)` | hướng dẫn 1 trang bắt buộc đi qua `service().layChiTiet(id)`; test mẫu; review checklist |
| R10 | `heThong` là domain shape cũ (`paths.ts` cấp domain) | module mới đạt chuẩn §5, chỉ chạm `paths.ts`/`routes.tsx` của domain đúng 2 dòng — không refactor domain |

---

## 14. Câu hỏi cần user chốt (không tự quyết — luật 9)

| # | Câu hỏi | Đề nghị |
|---|---|---|
| **Q1** | **Render:** GĐ1 in bằng renderer HTML ở FE (cửa sổ in/PDF của trình duyệt), BE chỉ cấp dữ liệu; PDF phía BE để GĐ5 — chấp nhận dù khác chốt A9 (2026-08-20)? Hay bắt buộc BE PDF ngay (+10–12 ngày, hai renderer)? | **FE trước**, BE PDF khi có nhu cầu lưu trữ/gửi mail/in hàng loạt |
| **Q2** | **Kênh lan mẫu mặc định:** mở `/internal/mau-in/**` (X-Internal-Token) trên super-admin-service cho cell pull + cache? (thay đổi tuyên bố "không có kênh internal" của service này) | **Có** — mirror `tenant-provisioning` |
| **Q3** | **Catalog cho super admin:** snapshot `catalog.json` chép từ build cell-app, hay super-admin gọi live một cell tham chiếu? | **Snapshot** |
| **Q4** | **Quyền:** một mã `HTMauIn.View/Edit` cho toàn màn, hay theo loại `<ChucNang>.PrintConfig` (28 mã)? | **`HTMauIn`** |
| **Q5** | `DON_VI`/`TIEU_DE`: khoá vị trí + không xoá đã rõ; **có cho ẩn** không? | Cho ẩn `DON_VI` (giấy tiêu đề in sẵn); `TIEU_DE` luôn hiện |
| **Q6** | Trường/cột **mới thêm vào form sau này** mặc định HIỆN (mock) trên mọi bản, hay chỉ hiện ở mẫu hệ thống và **ẩn + đánh dấu mới** ở bản tuỳ chỉnh của đơn vị? | Hiện ở mẫu hệ thống; ẩn + cờ ở bản tuỳ chỉnh |
| **Q7** | **Logo & ảnh nền** trong v1? Tenant chưa có trường logo; cần upload qua `common/storage` + màn Thông tin công ty | v1: chỉ "Khung viền"; logo/ảnh ở GĐ5 |
| **Q8** | **Khổ giấy:** A4/A5 × dọc/ngang (mock). Có cần "A5 in cuộn" như kho/thu-chi? | v1: A4/A5; cuộn để sau |
| **Q9** | Xem thử bằng **chứng từ thật** trong editor tenant (A5/A6, cần `.View`/`.Print` của loại) — đồng ý? Giới hạn 20 chứng từ gần nhất? | Đồng ý, 20 |
| **Q10** | Thêm 2 package `@dnd-kit/sortable`, `@dnd-kit/utilities` (cùng họ, nhỏ) cho `client` và `client-admin`? Hay tự viết sortable trên `@dnd-kit/core`? | **Thêm** |
| **Q11** | Mã tạm `R-MAUIN-nnn` / `MSG_MAUIN_nnn` cho tới khi BA cấp mã epic — chấp nhận? Ai tạo PYC trong `pmkt-docs/ba`? | Chấp nhận; BA tạo PYC sau, đổi mã bằng `msg.sh` |
| **Q12** | Giữ nguyên các hằng của mock: lề 0–5 cm, cỡ chữ 8–20, tiêu đề 10–36 pt, 4 ô ký/hàng, undo 60, 6 font, 10 màu? | Giữ |
| **Q13** | Thứ tự pilot **MDV → BH → PT**, rồi 25 loại còn lại theo chủ module? | Đồng ý |
| **Q14** | Super admin có cần **mặc định riêng cho một tenant** (như `sa_cau_hinh.tenant_id`) không? | Không trong v1 |
| **Q15** | `super-admin-service/`, `client-admin/` chưa là git repo — remote ở đâu, ai tạo? Có nhánh `develop` chưa? | Tạo trước GĐ1 |
| **Q16** | Mỗi bảng chi tiết của catalog = **một** khối `BANG`, chọn bằng bật/tắt, không nhân đôi, không xoá — đúng ý "danh sách bảng để chọn"? | Đúng |
| **Q17** | "Thông tin chung dạng bảng": mặc định **2 cột**, kẻ ô **Không**, nhãn 30 % — ok? Có cần kẻ ô cho khối tự do không? | 2 cột / Không / 30 %; khối tự do cùng tuỳ chọn |
| **Q18** | Hộp "Đóng khi chưa lưu": mock có **3 nút** (Lưu và đóng / Không lưu / Ở lại); BR3 + `CommonConfirmModal` là **2 nút** ("Xác nhận đóng" — *Dữ liệu đã có thay đổi…*). Theo BR3 hay theo mock (phải mở rộng `CommonConfirmModal`)? | **BR3 (2 nút)** — thống nhất toàn app |
| **Q19** | Bổ sung vào `@base` 3 control (`CommonSegmented`, `CommonColorPicker`, `PropField/PropSection`) + 3 icon, sao sang `client-admin` — duyệt? (bieuMau đang import antd trần, chuyển sau, ngoài phạm vi) | **Duyệt** |
| **Q20** | Full-bleed cho trang editor: thêm `handle.fullBleed` vào `AppLayout` (client & client-admin) hay dùng `margin:-16px` như `thietKeBieuMau.css`? | thêm `handle.fullBleed` |
| **Q21** | Kích thước hai panel 250 / 370 như mock (rộng hơn bieuMau 280 / 320) và chế độ dày (field 24px · hàng 28px · chữ 12px) — chấp nhận lệch mật độ so với màn nhập liệu thường? | **Chấp nhận** (đúng yêu cầu "màn dày thông tin") |

---

## 15. Ngoài phạm vi (nói rõ để không bị hiểu là quên)

- Không đụng 10 mẫu Jasper cố định của thu/chi và bản in HTML của kho (chúng vẫn chạy; chỉ thêm mục vào menu In).
- Không đổi engine `bieu_mau` / `report-service`.
- Không viết tài liệu vào `pmkt-docs/ba` (BA làm); không sửa `src/legacy/**`, `master_data/**`, `Phase_2/**`.
- Chưa có: xuất XLSX/DOCX từ mẫu khối, in nhiều liên, chữ ký số, QR — ghi nhận là ứng viên GĐ5+.
