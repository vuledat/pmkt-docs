# Giải pháp: Module cấu hình động biểu mẫu (phụ lục thuế) — "PMKT Form Designer"

> Trạng thái: **ĐÃ TRIỂN KHAI v1 (2026-09-09) theo đề nghị mặc định** — xem [02-trang-thai-trien-khai.md](02-trang-thai-trien-khai.md); các câu hỏi §12 chưa được user chốt tường minh, đã đi theo cột "Đề nghị".
> Ngày: 2026-09-08. Phạm vi khảo sát: `pmkt-docs/ba/PMKT-E-07522_Thue`, `PMKT-E-10978_ToKhaiThueGTGT`,
> `PMKT-E-14792-ToKhaiThue04GTGT`, `report-service/`, `cell-app/` (module `thue`, `tien_mat_tien_gui`,
> `reporting`), `client/`.

---

## 0. Tóm tắt điều hành

Xây một module **độc lập, generic** (không biết gì về thuế) cho phép người dùng:

1. Thiết kế biểu mẫu trên **lưới ô kiểu Excel** có **kéo thả** (kéo trường vào ô, kéo rộng cột/cao dòng, gộp ô,
   ảnh/hộp chữ/đường kẻ nổi, số trang…), chỉnh font/cỡ/màu/căn lề/viền/định dạng số — năng lực tương đương
   Jaspersoft Studio nhưng trên web và theo tư duy bảng tính mà kế toán đã quen.
2. Gắn **nguồn dữ liệu** cho biểu mẫu (trường đơn) và cho từng bảng (danh sách nhiều dòng), có tham số.
3. Viết **công thức** cho ô, cho cột theo dòng, cho dòng tổng, tham chiếu chéo giữa các ô/bảng, có điều kiện.
4. **Lưu, quản lý danh sách** biểu mẫu (thêm/sửa/xóa/nhân bản/phiên bản/hiệu lực theo kỳ/xuất-nhập JSON).
5. **Kết xuất** PDF, Excel, Word; khổ A4/A3/A5 dọc hoặc ngang; gộp nhiều biểu mẫu thành một bộ in.

**Quyết định kiến trúc then chốt (đề nghị):**

| # | Quyết định | Lý do ngắn |
|---|---|---|
| D1 | Đặt BE là **module Spring Modulith `bieu_mau` bên trong `report-service`**, ranh giới cứng, schema DB riêng, để tách thành service riêng sau bằng cách "nhấc" module | `report-service` đã có Jasper 7.0.7, font Việt, POI, MinIO, RLS tenant, cổng S2S — tái dùng 100 %, không cài lại |
| D2 | **Nguồn sự thật là JSON** (`BieuMauDinhNghia` v1) do PMKT định nghĩa, **không** phải JRXML. Bố cục theo **lưới ô kiểu Excel** (cột/dòng/gộp ô/viền) — "grid-first" — với vùng dòng gắn ngữ nghĩa (tiêu đề, header lặp, dòng chi tiết nở theo dữ liệu, dòng tổng, chân trang) và phần tử nổi (ảnh, hộp chữ, đường kẻ) neo vào ô. BE dựng `JasperDesign` từ lưới để ra PDF; Excel/Word xuất **native** từ lưới | File mẫu tham chiếu (§2A) và toàn bộ mẫu Thông tư đều là lưới ô; Excel xuất 1:1; kế toán quen Excel; JRXML cho phép nhúng Java → RCE |
| D6 | **Nhập biểu mẫu từ file Excel** có placeholder `##Token##` (định dạng của sản phẩm tham chiếu) → sinh định nghĩa lưới + gợi ý binding; xuất ngược ra Excel mẫu | 11 sheet trong file mẫu chuyển thành 11 biểu mẫu trong vài phút thay vì vẽ lại |
| D3 | **Công thức do PMKT tự đánh giá** (engine riêng, ngôn ngữ kiểu Excel), Jasper chỉ nhận giá trị **đã tính, đã định dạng** | Không chạy mã người dùng; công thức không phụ thuộc Jasper; test thuần JVM |
| D4 | Nguồn dữ liệu là **catalog có đăng ký** (Java provider) là chính; SQL tự do chỉ cho quản trị hệ thống, có guard | An toàn RLS/tenant, không lộ schema |
| D5 | FE là **feature `features/bieuMau/`** với 2 module: danh sách + designer; thêm 4 thư viện nhỏ (`zustand`, `immer`, `zundo`, `@dnd-kit/core`) và CodeMirror 6 cho ô công thức | Không có thư viện kéo thả nào trong `client/` hiện nay |

Các điểm cần user chốt nằm ở **§12**.

---

## 1. Hiện trạng đo được (không suy diễn)

| Hạng mục | Hiện trạng | Nguồn |
|---|---|---|
| Engine báo cáo | `report-service` (port 8083/8092 local), Jasper **7.0.7** + `jasperreports-pdf` + `jasperreports-fonts`, POI 5.3.0, dựng `JasperDesign` **động bằng Java API**, cấm `JRLoader.loadObject` (CVE-2026-6009) | `report-service/build.gradle.kts`, `…/renders/jasper/GenericPdfDesignBuilder.java`, `JasperPdfRenderer.java` |
| Báo cáo hiện có | 7 `ReportDefinition` viết cứng bằng Java; manifest cây cột `ReportColumn`/`ReportRow`; 3 renderer pdf/xlsx/csv | `…/reporting/api/ReportDefinition.java`, `…/definitions/*` |
| Điểm cắm mẫu pháp định | `LegalPrintTemplateRegistry` **rỗng** | `…/renders/jasper/LegalPrintTemplateRegistry.java` |
| In chứng từ | `cell-app` in phiếu thu/chi/UNC bằng **19 file `.jrxml` tĩnh** (Jasper 6.21.3, font Liberation Serif), FE nhận `application/pdf` qua `http.get(responseType:'blob')` rồi mở tab | `cell-app/…/InPhieuThuChi.java`, `client/src/features/nganQuy/_shared/api/inPhieuApi.ts` |
| Xuất Word | **Không có** ở BE | khảo sát toàn repo |
| Engine công thức | **Không có** (chỉ `@Formula` SQL hằng) | khảo sát toàn repo |
| Lưu cấu hình dạng JSON | Tiền lệ `core_mau_excel` (cột `dinh_dang` JSON) và `CauHinhCot` | `cell-app/…/common/mau_excel`, `…/common/ui_config` |
| Lưu file | MinIO qua `common/storage` (`ObjectStorage`, Tika sniff MIME) | `cell-app/…/common/storage` |
| Multi-tenant | cột `tenant_id` + PostgreSQL RLS, role `pmkt_app`; GUC bind qua aspect **chỉ khi có transaction** | `…/core/config/TenantRls*.java` |
| Định tuyến | Gateway chỉ có 1 route catch-all `/api/** → cell-app`; `report-service` được gọi **S2S qua `cell-app/reporting/ReportProxyController`** với `X-Internal-Token` | `cell-gateway/…/application.yml`, `cell-app/…/reporting/**` |
| Migration | Quy ước timestamp `V<yyyyMMddHHmmss>__<prefix>_…`; `report-service` **Flyway tắt**, dùng chung DB `pmkt_cell` | `docs/rules/migration-danh-so-theo-timestamp.md`, `deploy/env/osp-report-service.env` |
| Dữ liệu thuế | Chỉ có `tax_thiet_lap_thong_tin_thue`, `tax_dang_ky_to_khai_thue` + 2 danh mục CQT. **Chưa có bảng tờ khai / phụ lục / bảng kê** | `cell-app/…/db/migration/V1075…V1078` |
| FE | React 19 + antd 6 + TanStack Query + Zod + i18next; **không** có dnd-kit/zustand/pdfjs/codemirror; có `exceljs`, `docx-preview` | `client/package.json` |
| FE báo cáo | Runner generic `app/pages/baoCao/ReportRunnerPage.tsx` + `base/domainKit/report/*` gọi `/api/reports/{id}/params|run` | `client/src/base/domainKit/report/reportApi.ts` |
| FE thuế | `features/thue/khaiBaoThue` (hub 2 thẻ), route nối tay trong `app/router/RootRoutes.tsx`, menu ở `app/layouts/shell/menuRegistry.tsx` | `client/src/features/thue/routes.tsx` |

---

## 2. Yêu cầu nghiệp vụ rút từ tài liệu thuế (engine phải phủ)

Bảng dưới liệt kê **năng lực** mà 8 biểu mẫu thuế đòi hỏi. Module là generic nhưng đây là bộ kiểm thử
nghiệm thu đầu tiên. (Trích từ `SCR_ToKhai01GTGT`, `SCR_PhuLuc_*`, `SCR_BangKe*`, `SCR_ToKhaiBoSung`,
`SCR_BanGiaiTrinhToKhaiBoSung`, `UC_InToKhai`, `BRD_ToKhai04GTGT`.)

| Năng lực | Ví dụ trong tài liệu | Ảnh hưởng thiết kế |
|---|---|---|
| Form chỉ tiêu đánh số `[21]…[43]` dạng nhãn + ô, có ô "Trong đó" thụt lề | 01/GTGT | Dòng tĩnh của lưới: ô nhãn gộp ngang + ô mã + ô giá trị, thụt lề bằng padding |
| Ô "chỉ để giữ layout, không dữ liệu" | `[11b]` Quận/Huyện (F1 BR3) | `field` không binding, hoặc `staticText` |
| Bảng chia **nhóm cố định** với dòng tổng nhóm in đậm + tổng cuối bảng loại trừ nhóm | BKBR 4 nhóm thuế suất (F4 BR01.2, BR04) | `table.groups[]` với `groupBy` + `footerRows` + tổng có điều kiện |
| Bảng ẩn/hiện **cả section** theo cấu hình | BKMV nhóm 4 (F5 BR01.1) | `visibleWhen` ở cấp group/section |
| Nhiều bảng trên một mẫu, mỗi bảng nguồn riêng | PL Giảm thuế Mục I/II/III | Mỗi `table` gắn một `dataset` riêng |
| Bảng 3 tầng: chi tiết → tổng theo tỉnh → tổng | PL 01-6 (F3) | Nhóm lồng + `SUM` theo nhóm |
| **Thứ tự cột khi in khác khi nhập** | PL 01-6 (F3 BR04, BR05) | Biểu mẫu in là định nghĩa riêng, không suy từ màn nhập |
| STT phân cấp `1`, `1.1`, `1.2` và đánh lại khi ẩn khối | 01-1/KHBS (F7 BR16, BR24) | Hàm `ROW_INDEX()`, `GROUP_INDEX()` |
| Control khác nhau theo dòng trong cùng cột (checkbox ở dòng 1.1) | 01-1/KHBS (F7 BR16) | `cell.renderWhen` + kiểu `checkbox` |
| Ô gộp chiếm nhiều dòng | 04/GTGT Mục A `[21]` | `rowSpan`/`colSpan` trong bảng |
| Công thức giữa chỉ tiêu, `MAX(0, …)`, làm tròn, `IF` | `[40a] = MAX(0,[36]-[22]+[37]-[38]-[39a])` | Engine công thức §5 |
| Công thức theo dòng, tổng cột, tổng có điều kiện (`SUMIF`) | `[7]=[6]×thuế suất`; `Σ[6] WHERE [8]=true` | Ngữ cảnh `row`, hàm tập hợp |
| Tham chiếu chéo mẫu ↔ mẫu | BKMV → `[23]…[25]` của 01/GTGT | Là việc của **nguồn dữ liệu** (dataset trả sẵn), không phải công thức xuyên biểu mẫu |
| Số âm `(1.000.000)` màu đỏ; `0` hiện `0`; tách nghìn `.`; số nguyên | F2 BR04, F8 BR_IN_03, F11 BR-16 | `format.number` (pattern, negativeStyle, zeroDisplay, precision) |
| Số trang `[trang]/[tổng]` liên tục toàn bộ **bộ in** nhiều mẫu | F8 BR_IN_03 | Kết xuất bộ (§7.4) hai lượt để đánh số liên tục |
| Khổ A4; hướng giấy **không nêu** | F8 | Thuộc tính trang của mẫu, mặc định A4 dọc, cho chọn ngang |
| Mẫu đổi theo văn bản hiệu lực (142/174/204, TT 40/2025) | F11 mục 9 | **Phiên bản có hiệu lực theo ngày** (`hieu_luc_tu/den`) |
| Chỉ PDF bắt buộc; Excel mức [C]; Word không có trong BA | F8, F11 FR-10 | Word làm ở mức "đủ dùng" (§7.3), nêu rõ giới hạn |

---

## 2A. Đối chiếu file mẫu Excel do user cung cấp (2026-09-08)

File gốc: `D:\Download\To khai thue GTGT khau tru 01GTGT.xlsx` — đã sao lưu vào
[mau/To_khai_thue_GTGT_khau_tru_01GTGT.xlsx](mau/To_khai_thue_GTGT_khau_tru_01GTGT.xlsx).
Đây là **bản xuất Excel của một sản phẩm khác** dùng engine "Excel template + placeholder": 6 sheet đầu
đã điền số liệu, 5 sheet cuối còn nguyên token dạng `##AdditionDetail_hkbs01_01_SortOrder##`,
`##TotalAdjustmentAmountTax40##`, `##attachment##`. Không có drawing/ảnh/checkbox control nào; ô tích
in bằng chữ `X`.

| # | Sheet | Khổ | Cột | Bề rộng in | Đặc điểm bố cục | Token |
|---|---|---|---|---|---|---|
| 0 | Tờ khai 01/GTGT | A4 dọc | 8 | 7,0 in | 56 vùng gộp; form chỉ tiêu `[21]…[43]` 2 cột giá trị/thuế; `[21]` in chữ "Không"; dòng "Trong đó" thụt lề; viền `lrtb` mọi ô | 0 |
| 1 | Bảng kê bán ra | A4 **ngang** | 14 | 17,0 in (tràn A4, 5 cột phụ HĐĐT/sàn TMĐT nằm ngoài vùng in) | Header 2 tầng gộp; 4 nhóm thuế suất, mỗi nhóm = dòng tiêu đề gộp full-width + dòng chi tiết + "Tổng nhóm n"; 2 dòng tổng ngoài bảng viền `t`; dòng chi tiết font 12 lệch header 9 | 0 |
| 2 | Bảng kê mua vào | A4 ngang | 16 | 12,4 in | 90 vùng gộp (cột nhỏ để căn nhiều tầng); cột "Là chứng từ nhập khẩu" = `X`; 5 dòng tổng ngoài bảng | 0 |
| 3 | PL 01-6 (VT cước trả sau) | A4 ngang | 12 | 10,2 in | 2 dòng chỉ tiêu `[06]`,`[07]` dạng nhãn + ô phải; header 3 tầng; "Cộng theo từng tỉnh", "Cộng các tỉnh", `[20]` | 0 |
| 4 | PL 01-6 (CSSX) | A4 ngang | 12 | 10,2 in | Như trên + **dòng mã chỉ tiêu** `[08]…[21]=([06]x([16]/[07])` ngay dưới header; nhóm tổng theo tỉnh sinh động | 0 |
| 5 | PL giảm thuế NQ 204 | Letter dọc | 18 | 11,3 in | **18 cột hẹp + gộp** để đặt 2 bảng khác cấu trúc cột trên cùng sheet; Mục III là dòng chữ + số + "đồng"; font tiêu đề Arial | 0 |
| 6 | Tờ khai bổ sung 01/KHBS | A4 dọc | 32 | 13,0 in | **32 cột hẹp (1–8 ký tự)** giả lập văn bản tự do có ô số chen giữa; 3 bảng + 2 khối form; có 3 công thức Excel `=AB10` | 30 |
| 7 | Bản giải trình 01-1/KHBS | A4 dọc | 9 | 7,0 in | Bảng 8 cột, dòng header phụ `(6) = (5) - (4)`; 3 dòng tổng `[07]…[09]` | 12 |
| 8 | Bảng kê thuế đã nộp ngoại tỉnh (01-5/GTGT) | Letter | 7 | 7,1 in | Bảng đơn + tổng; số `#,##0;\(#,##0\);;` (0 → trống) | 7 |
| 9 | Bảng phân bổ công trình liên tỉnh (01-7/GTGT) | Letter | 6 | 7,1 in | Bảng đơn + tổng, header phụ `(1)…(6)` nghiêng | 7 |
| 10 | PL giảm thuế NQ 406 | Letter | 6 | 7,1 in | Bảng đơn, header phụ có công thức `(5)=(4)x70%` | 7 |

**Kết luận rút ra cho thiết kế** (đây là lý do đổi D2 sang grid-first):

1. **100 % biểu mẫu là lưới ô**: mọi "form tự do" đều được dựng bằng cột hẹp + gộp ô (sheet 5, 6). Mô
   hình canvas tuyệt đối kiểu Jasper xuất Excel sẽ méo; mô hình lưới xuất Excel **1:1** và vẫn ra PDF
   chính xác (cột → x, dòng → y).
2. **Ba loại vùng dòng** đủ phủ mọi sheet: dòng tĩnh (tiêu đề, nhãn, header), **dòng chi tiết nở theo
   dataset** (token `##AdditionDetail_<bảng>_<trường>##`), dòng tổng (token `##Total…##` hoặc công thức).
   Nhóm = dòng tĩnh tiêu đề nhóm + dòng chi tiết lọc theo nhóm + dòng tổng nhóm.
3. **Định dạng số thống nhất** `#,##0;(#,##0)` (âm trong ngoặc), biến thể `;;` (0 → trống) và
   `#,##0.00` cho thuế suất → style số của engine phải hỗ trợ đúng cú pháp pattern Excel 3 phần.
4. **Cần thiết lập trang theo sheet**: khổ, hướng, lề, vùng in; nên bổ sung "lặp dòng header mỗi trang"
   (file mẫu không có `print_title_rows` — điểm ta làm tốt hơn).
5. **Lỗi trong file mẫu mà engine phải tránh lặp lại**: dòng chi tiết font 12 lệch header 9 (sheet 1);
   bảng kê bán ra tràn 17 in vượt A4 ngang; ngày lưu dạng chuỗi `20/12/2026` với pattern `m/d/yyyy`;
   khổ Letter ở 4 sheet. Engine phải ép style dòng chi tiết theo dòng mẫu, cảnh báo tràn trang, giữ
   kiểu ngày/số thật.
6. **Placeholder `##Token##` là hợp đồng nhập khẩu**: đọc file Excel → sinh lưới (rộng cột, cao dòng,
   gộp, viền, font, pattern số) + danh sách token → người dùng map token ↔ trường dataset (gợi ý tự động
   theo tên). Toàn bộ 11 sheet nhập được ngay, kể cả 6 sheet đã điền số (số liệu trở thành giá trị tĩnh
   để thay bằng binding).

---

## 3. Kiến trúc tổng thể

```
┌──────────────── client (React) ────────────────┐
│ features/bieuMau/danhSachBieuMau  (quản lý)     │
│ features/bieuMau/thietKeBieuMau   (designer)    │
│ base/domainKit/bieuMau (viewer PDF, nút in gộp) │
└───────────────┬────────────────────────────────┘
                │ /api/bieu-mau/**   (JWT qua gateway)
┌───────────────▼────────────────────────────────┐
│ cell-app · module bieu_mau_proxy (mỏng)         │  chuyển tiếp S2S + kiểm quyền BieuMau.*
│ cell-app · module thue → gọi S2S "ket-xuat"     │  (nút In tờ khai, in bộ phụ lục)
└───────────────┬────────────────────────────────┘
                │ X-Internal-Token
┌───────────────▼────────────────────────────────┐
│ report-service · module bieu_mau                │
│  api/        BieuMauKetXuatApi (cho reporting)  │
│  internal/                                      │
│   controller/  BieuMauController, NguonDuLieu…  │
│   dinh_nghia/  JSON schema v1 + validator       │
│   cong_thuc/   parser + evaluator + hàm         │
│   nguon/       DatasetProvider SPI + catalog    │
│   no_luoi/     nở dòng chi tiết/nhóm → RenderGrid │
│   ket_xuat/    pdf · xlsx · docx · bộ in        │
│   kho/         entity/repository (schema bm)    │
└────────────────────────────────────────────────┘
        DB pmkt_cell (schema `bieu_mau`, RLS)  ·  MinIO (ảnh/logo, artefact)
```

### 3.1 Vì sao đặt trong `report-service` (D1) mà không phải chỗ khác

| Phương án | Ưu | Nhược |
|---|---|---|
| **A. Module trong `report-service`** (đề nghị) | Jasper 7 + font + POI + MinIO + RLS + S2S đã sẵn; deploy riêng đã có; tách sau = nhấc package + `build.gradle` | Phải bật Flyway riêng cho schema `bieu_mau`; cần proxy mỏng ở `cell-app` |
| B. Service mới `form-designer-service` | Độc lập tuyệt đối ngay từ đầu | Lặp lại toàn bộ khung (security, tenant, MinIO, CI/CD, env, Sentry…) ~1–2 tuần thuần hạ tầng; thêm 1 tiến trình JVM |
| C. Module trong `cell-app` | Không cần proxy | Trái ý "độc lập"; `cell-app` chỉ có Jasper 6.21.3, nặng thêm monolith |

Ranh giới cưỡng chế bằng **ArchUnit** (đã có tiền lệ `ReportingEngineCoreArchTest`): `bieu_mau.**` không import `reporting.internal.**`; chỉ `bieu_mau.internal.ket_xuat.jasper.**` được import `net.sf.jasperreports.**`; chỉ `…ket_xuat.poi.**` được import `org.apache.poi.**`.

### 3.2 Luồng kết xuất (runtime)

```
POST /api/bieu-mau/{ma}/ket-xuat?format=pdf  {thamSo:{toKhaiId:…}, ngayHieuLuc:"2026-07-31"}
  1. Chọn phiên bản PUBLISHED có hiệu lực tại ngayHieuLuc (tenant override > hệ thống)
  2. Nạp datasets khai trong mẫu (provider catalog / SQL guard / tham số tay) — song song, có timeout
  3. Đánh giá công thức: dựng đồ thị phụ thuộc → topo sort → tính (BigDecimal), phát hiện vòng
  4. Nở lưới: dòng chi tiết × n, vùng nhóm × số nhóm, dòng tổng; resolve style/điều kiện → RenderGrid
     (mỗi ô giữ giá trị gốc + kiểu + pattern + chuỗi hiển thị)
  5. RenderGrid → PDF (Jasper, cache design theo hash) | XLSX (POI) | DOCX (POI XWPF) theo format
  6. Trả bytes (Content-Disposition) hoặc lưu MinIO + trả URL nếu bộ in lớn (job bất đồng bộ)
```

Bước 2–4 **không đụng Jasper/POI**: RenderGrid là hợp đồng duy nhất giữa tầng nghiệp vụ và 3 renderer.

---

## 4. Mô hình biểu mẫu — `BieuMauDinhNghia` v1 (JSON, grid-first)

Nguồn sự thật, lưu JSONB, có `schemaVersion` để migrate. Zod (FE) và Jackson + validator (BE) cùng
đọc một JSON Schema xuất từ BE (`GET /api/bieu-mau/schema/v1`).

**Ý tưởng cốt lõi**: một biểu mẫu = một **lưới ô** (như một sheet Excel) gồm danh sách cột (rộng) và
danh sách **dòng có ngữ nghĩa**. Ô có nội dung tĩnh hoặc công thức, style, gộp ô. Dòng "chi tiết" gắn
dataset sẽ **nở** thành n dòng khi kết xuất; dòng "tổng nhóm" lặp theo nhóm. Trên lưới có thể đặt
**phần tử nổi** (ảnh, hộp chữ, đường kẻ) neo vào một ô + độ lệch, cho logo/chữ ký/QR.

```jsonc
{
  "schemaVersion": 1,
  "ma": "BKBR_01_1_GTGT",
  "ten": "Bảng kê hóa đơn, chứng từ hàng hóa, dịch vụ bán ra",
  "trang": { "kho": "A4", "huong": "NGANG", "le": { "tren": 28, "duoi": 28, "trai": 28, "phai": 28 },
             "khoTuyChinh": null, "coGiuTrang": "VUA_CHIEU_RONG" },   // VUA_CHIEU_RONG | 100% | tỉ lệ
  "font": { "macDinh": "Times New Roman", "coMacDinh": 9 },
  "thamSo": [ { "ma": "toKhaiId", "kieu": "uuid", "batBuoc": true } ],
  "nguonDuLieu": [                                        // §6
    { "ma": "header", "loai": "CATALOG", "provider": "thue.toKhai01.header", "dangDong": "MOT_DONG",
      "thamSo": { "toKhaiId": "$P{toKhaiId}" } },
    { "ma": "bkbr", "loai": "CATALOG", "provider": "thue.bangKeBanRa.dong", "dangDong": "NHIEU_DONG",
      "thamSo": { "toKhaiId": "$P{toKhaiId}" } }
  ],
  "bien": [ { "ma": "tongDtChiuThue", "congThuc": "SUMIF(bkbr.doanhThu, bkbr.nhom <> 1)" } ],
  "kieuDang": [
    { "ma": "tieuDe", "co": 14, "dam": true, "canNgang": "GIUA" },
    { "ma": "header", "dam": true, "canNgang": "GIUA", "canDoc": "GIUA", "xuongDong": true, "vien": "LRTB" },
    { "ma": "oSo", "canNgang": "PHAI", "vien": "LRTB", "dinhDangSo": "#,##0;(#,##0)" },
    { "ma": "oChu", "canNgang": "TRAI", "vien": "LRTB", "xuongDong": true }
  ],
  "cot": [ { "ma": "A", "rong": 30 }, { "ma": "B", "rong": 90 }, { "ma": "C", "rong": 75 },
           { "ma": "D", "rong": 180 }, { "ma": "E", "rong": 90 }, { "ma": "F", "rong": 110 },
           { "ma": "G", "rong": 100 }, { "ma": "H", "rong": 120 } ],                 // đơn vị pt
  "dong": [
    { "id": "r1", "loai": "TINH", "cao": 24,
      "o": [ { "cot": "A", "gopDen": "H", "text": "BẢNG KÊ HOÁ ĐƠN, CHỨNG TỪ HÀNG HOÁ, DỊCH VỤ BÁN RA", "kieuDang": "tieuDe" } ] },
    { "id": "r2", "loai": "TINH", "cao": 14,
      "o": [ { "cot": "A", "gopDen": "H", "congThuc": "\"Kỳ tính thuế: \" & header.kyTinhThueChu", "canNgang": "GIUA" } ] },
    { "id": "h1", "loai": "HEADER", "lapMoiTrang": true, "cao": 16,
      "o": [ { "cot": "A", "gopDenDong": "h2", "text": "STT", "kieuDang": "header" },
             { "cot": "B", "gopDen": "C", "text": "Hóa đơn, chứng từ bán ra", "kieuDang": "header" },
             { "cot": "D", "gopDenDong": "h2", "text": "Tên người mua", "kieuDang": "header" },
             { "cot": "E", "gopDenDong": "h2", "text": "Mã số thuế người mua", "kieuDang": "header" },
             { "cot": "F", "gopDenDong": "h2", "text": "Doanh thu chưa có thuế GTGT", "kieuDang": "header" },
             { "cot": "G", "gopDenDong": "h2", "text": "Thuế GTGT", "kieuDang": "header" },
             { "cot": "H", "gopDenDong": "h2", "text": "Ghi chú", "kieuDang": "header" } ] },
    { "id": "h2", "loai": "HEADER", "lapMoiTrang": true, "cao": 26,
      "o": [ { "cot": "B", "text": "Số hóa đơn", "kieuDang": "header" },
             { "cot": "C", "text": "Ngày, tháng, năm lập hóa đơn", "kieuDang": "header" } ] },

    { "id": "g1", "loai": "NHOM", "nguon": "bkbr", "theo": "row.nhom", "sapXep": "ASC",
      "anKhiRong": false,                                   // BKBR: nhóm rỗng vẫn in tiêu đề + tổng = 0
      "dongDauNhom": [
        { "id": "g1h", "loai": "TINH", "cao": 16,
          "o": [ { "cot": "A", "gopDen": "H", "congThuc": "GROUP_INDEX() & \". \" & LOOKUP(\"tenNhomBkbr\", GROUP_KEY())", "dam": true, "vien": "LRTB" } ] } ],
      "dongChiTiet": { "id": "g1d", "loai": "CHI_TIET", "cao": 14, "tuDan": true,
          "o": [ { "cot": "A", "congThuc": "ROW_INDEX()", "canNgang": "GIUA", "vien": "LRTB" },
                 { "cot": "B", "congThuc": "row.soHoaDon", "kieuDang": "oChu", "canNgang": "GIUA" },
                 { "cot": "C", "congThuc": "row.ngayHoaDon", "dinhDangNgay": "dd/MM/yyyy", "canNgang": "GIUA", "vien": "LRTB" },
                 { "cot": "D", "congThuc": "row.tenNguoiMua", "kieuDang": "oChu" },
                 { "cot": "E", "congThuc": "row.mstNguoiMua", "kieuDang": "oChu" },
                 { "cot": "F", "congThuc": "row.doanhThu", "kieuDang": "oSo" },
                 { "cot": "G", "congThuc": "row.thueGtgt", "kieuDang": "oSo" },
                 { "cot": "H", "congThuc": "row.ghiChu", "kieuDang": "oChu" } ] },
      "dongCuoiNhom": [
        { "id": "g1f", "loai": "TONG_NHOM", "cao": 14, "giuCungTrangVoiDongTruoc": true,
          "o": [ { "cot": "A", "gopDen": "E", "congThuc": "\"Tổng nhóm \" & GROUP_INDEX()", "dam": true, "vien": "LRTB" },
                 { "cot": "F", "congThuc": "GROUP_SUM(bkbr.doanhThu)", "kieuDang": "oSo", "dam": true },
                 { "cot": "G", "congThuc": "GROUP_SUM(bkbr.thueGtgt)", "kieuDang": "oSo", "dam": true },
                 { "cot": "H", "vien": "LRTB" } ] } ]
    },

    { "id": "t1", "loai": "TINH", "cao": 14,
      "o": [ { "cot": "A", "gopDen": "D", "text": "Tổng doanh thu hàng hóa, dịch vụ bán ra chịu thuế GTGT (*):", "vien": "T" },
             { "cot": "E", "gopDen": "H", "congThuc": "tongDtChiuThue", "dinhDangSo": "#,##0;(#,##0)", "vien": "T" } ] },
    { "id": "ft", "loai": "CHAN_TRANG", "cao": 14,
      "o": [ { "cot": "F", "gopDen": "H", "congThuc": "\"Trang \" & PAGE() & \"/\" & PAGES()", "canNgang": "PHAI", "nghieng": true } ] }
  ],
  "phanTuNoi": [
    { "id": "logo", "loai": "ANH", "taiSanId": "…", "neo": { "dong": "r1", "cot": "A", "dx": 0, "dy": 0 }, "w": 60, "h": 40 }
  ]
}
```

### 4.1 Loại dòng

| `loai` | Hành vi khi kết xuất | Tương ứng Jasper (PDF) |
|---|---|---|
| `TINH` | In đúng một lần tại vị trí | phần tử trong band `title`/`detail` float |
| `HEADER` (`lapMoiTrang`) | In tại chỗ, và lặp lại đầu mỗi trang mới **nếu** phía dưới còn dòng chi tiết của bảng đó | `columnHeader` của table component |
| `CHI_TIET` (`nguon`) | Nở thành n dòng theo dataset (đã lọc theo nhóm cha nếu có); `tuDan` = cao theo nội dung; `caoToiThieu` | `detail` |
| `NHOM` | Vùng lặp theo khoá nhóm: `dongDauNhom[]` + `dongChiTiet` + `dongCuoiNhom[]`; lồng được; `anKhiRong`; `sapXep`; `danhSoLai` | `group` header/footer |
| `TONG_NHOM` / `TONG` | Dòng tính tập hợp trên nhóm/bảng; `giuCungTrangVoiDongTruoc` | `groupFooter` / `summary` |
| `CHAN_TRANG` / `DAU_TRANG` | Mỗi trang | `pageFooter` / `pageHeader` |
| `NGAT_TRANG` | Sang trang mới | `break` |
| `MAU_CON` | Nhúng biểu mẫu khác (khối NNT, khối ký tên) — lưới con có cột riêng, căn theo bề rộng trang | subreport |

Ô: `cot`, `gopDen` (gộp ngang), `gopDenDong` (gộp dọc, chỉ giữa các dòng tĩnh/header), `text` |
`congThuc`, `kieu` (`CHU`/`SO`/`NGAY`/`LOGIC`/`ANH`), `kieuDang` + ghi đè từng thuộc tính, `anKhi`,
`kieuDangKhi[]` (style có điều kiện), `renderKhi` (chọn kiểu hiển thị theo dòng: text/checkbox/ẩn —
phủ ca 01-1/KHBS dòng 1.1), `xoay`, `lienKet` (URL, phase 2).

Cột: `ma`, `rong` (pt), `anKhi` (ẩn cả cột theo điều kiện — BKMV nhóm 4, cột phụ HĐĐT), `coGian`
(cột hút phần dư khi vừa chiều rộng trang).

### 4.2 Mẫu con và bảng khác cấu trúc cột trên cùng trang

Hai cách, người dùng chọn: (a) cột hẹp + gộp như Excel (file mẫu sheet 5, 6 — nhập từ Excel giữ
nguyên); (b) `MAU_CON` hoặc **vùng lưới lồng** (`loai: "VUNG"`, có `cot[]` riêng, chiếm trọn bề
rộng dòng cha) — sạch hơn, designer khuyến nghị. Khi xuất Excel, vùng lồng được "chiếu" xuống lưới
cột chung bằng thuật toán cắt cột (union các mép cột) — cùng cách Jasper/POI làm.

### 4.3 Phần tử nổi

`ANH` (MinIO / công thức trả base64 hoặc URL; QR ở v2), `HOP_CHU` (text box tự do, viền/nền),
`DUONG_KE`, `KHUNG`. Neo `{dong, cot, dx, dy}` + `w,h` (pt), `anKhi`, `zIndex`, `theoTrang`
(`MOI_TRANG`/`TRANG_DAU`/`TRANG_CUOI`) cho watermark/logo. Excel: ảnh neo ô (POI `ClientAnchor`),
hộp chữ → text box hoặc ô gộp tuỳ chọn.

### 4.4 Style

Font (whitelist font nhúng — §12 Q4), cỡ, đậm/nghiêng/gạch chân, màu chữ, nền, căn ngang/dọc, xuống
dòng, viền 4 cạnh (độ dày/kiểu/màu), padding, xoay, thụt lề, `dinhDangSo` **theo cú pháp pattern Excel
3–4 phần** (`#,##0;(#,##0);;` = dương;âm;không;chữ — trùng file mẫu, xuất Excel giữ nguyên pattern,
PDF do engine format), `mauSoAm`, `dinhDangNgay` (`dd/MM/yyyy`…), `dinhDangLogic` (`X/`, `☑/☐`,
`Có/Không`). Style đặt tên kế thừa 1 cấp (`keThua`). Style dòng chi tiết là **của dòng mẫu**, mọi dòng
nở ra thừa kế — không có chuyện dòng chi tiết font 12 lệch header 9 như sheet 1 của file mẫu.

### 4.5 Thiết lập trang

Khổ (A4/A3/A5/Letter/tuỳ chỉnh), hướng, lề, `coGiuTrang` (`100%` | `VUA_CHIEU_RONG` — thu tỉ lệ toàn
lưới cho vừa bề rộng, có sàn cỡ chữ; cảnh báo trong designer khi lưới rộng hơn trang như sheet 1 tràn
17 in), lặp header, số trang liên tục trong bộ in, watermark, số liên.

---

## 5. Engine công thức (D3)

### 5.1 Ngôn ngữ

Cú pháp kiểu Excel/Google Sheets, **không** phải Java/JS. Mục tiêu: kế toán đọc được, không thể chạy mã.

```
row.giaTriChuaThue * 0.08                     // ngữ cảnh dòng bảng
SUM(mucII.thueDuocGiam)                       // tập hợp trên dataset
SUMIF(bkmv.thueGtgt, bkmv.laNhapKhau = true)  // tổng có điều kiện
IF(header.lanDau, "Lần đầu", "Bổ sung lần " & header.lanBoSung)
MAX(0, ct36 - ct22 + ct37 - ct38 - ct39a)     // biến cấp biểu mẫu
ROUND(row.a * 0.01 + row.b * 0.02, 0)
ROW_INDEX()  GROUP_INDEX()  GROUP_SUM(thueGtgt)  PREV(row.soDu)  // ngữ cảnh bảng/nhóm
FORMAT(x, "#,##0")  TEXT_UPPER(s)  DATE_FORMAT(d, "dd/MM/yyyy")  NUM_TO_WORDS(x)   // tiền bằng chữ đã có ở cell-app `SoTienBangChu`
```

- Kiểu: `số` (BigDecimal, không dùng double), `chuỗi`, `ngày`, `logic`, `null`. `null` trong phép số
  → coi là 0 khi cấu hình `nullLa0=true` (mặc định), chuỗi → rỗng.
- Toán tử: `+ - * / ^ & = <> < <= > >= AND OR NOT`, ngoặc, hằng chuỗi/số/ngày `DATE(2026,7,31)`.
- Định danh: `tenBien`, `nguon.truong`, `row.truong`, `$P{thamSo}`, `[21]` (alias chỉ tiêu — bí danh
  cho biến, cho phép kế toán gõ đúng mã chỉ tiêu trên mẫu).
- Hàm chuẩn (v1, ~35 hàm): `SUM AVG MIN MAX COUNT COUNTIF SUMIF ROUND ROUNDUP ROUNDDOWN ABS IF IFS
  COALESCE AND OR NOT LEN LEFT RIGHT MID UPPER LOWER TRIM CONCAT FORMAT TEXT DATE TODAY YEAR MONTH
  DAY DATE_ADD DATE_DIFF DATE_FORMAT ROW_INDEX GROUP_INDEX GROUP_SUM GROUP_COUNT PREV NEXT NUM_TO_WORDS`.
- **Không có** gán, vòng lặp, gọi hàm ngoài, truy cập object.

### 5.2 Thực thi

- Parser tự viết (Pratt/recursive descent, ~600 dòng Java) — không ANTLR để tránh thêm build step; FE có
  parser TS **cùng bộ test JSON** (`test/cong-thuc-cases.json` chạy ở cả 2 bên) để tô màu, gợi ý, báo lỗi
  cú pháp tức thì. FE **không** tính giá trị; xem trước luôn gọi BE.
- Đồ thị phụ thuộc giữa biến/ô/dòng tổng; topo sort; phát hiện vòng → lỗi `CONG_THUC_VONG` chỉ rõ chuỗi.
- Tập hợp trên dataset chạy 1 lượt/cột (O(n)), cache theo (dataset, cột, điều kiện).
- Giới hạn: độ sâu biểu thức, số dòng dataset (`pmkt.bieu-mau.max-rows`, mặc định 20 000), thời gian
  (`max-eval-ms`).
- Làm tròn: `ROUND` mặc định HALF_UP (Commercial rounding theo BR7), cấu hình được ở mẫu (`lamTron`).

### 5.3 Đối chiếu với BR7/BR18 (số liệu, tiền tệ)

Giá trị lưu/tính bằng BigDecimal đủ chữ số; **chỉ làm tròn khi hiển thị** trừ khi công thức gọi `ROUND`
tường minh (khớp BR7 "lưu DB giá trị đầy đủ, làm tròn khi hiển thị"). Mẫu thuế yêu cầu số nguyên → style
`dinhDangSo.mau = "#,##0"` và công thức `ROUND(…,0)` theo đúng chỗ BA quy định.

---

## 6. Nguồn dữ liệu (D4)

### 6.1 SPI provider (catalog)

```java
public interface NguonDuLieuProvider {
    String ma();                       // "thue.bangKeBanRa.dong", kebab/dot ổn định
    String nhom();                     // "Thuế GTGT", "Bán hàng"… để designer gom nhóm
    List<ThamSoMoTa> thamSo();         // tên, kiểu, bắt buộc, mặc định, nguồn lookup
    List<TruongMoTa> truong();         // tên, kiểu, nhãn, mô tả — designer hiện trong panel Dữ liệu
    DangDong dangDong();               // MOT_DONG | NHIEU_DONG
    KetQua nap(Map<String,Object> thamSo, NguCanh nc);   // nc: tenant, user, giới hạn dòng, timeout
    default KetQua duLieuMau(NguCanh nc) { ... }          // dữ liệu giả để xem trước trong designer
}
```

- Provider đăng ký là Spring bean, registry fail-fast trùng `ma()` (tiền lệ `ReportRegistry`).
- Provider thuế đặt ở `report-service/…/bieu_mau/internal/nguon/thue/` (đọc trực tiếp bảng `tax_*`,
  `sal_hoa_don_ban_hang`, `pur_hoa_don_mua`… như các `ReportDefinition` hiện làm). Khi bảng tờ khai chưa
  có, provider trả `duLieuMau()` và ném `NGUON_CHUA_SAN_SANG` khi chạy thật.
- Mọi truy vấn chạy trong `@Transactional(readOnly = true)` để RLS bind GUC (bẫy đã ghi ở `TenantRls`).

### 6.2 SQL tự do (chỉ quản trị hệ thống, tắt mặc định)

Bật bằng `pmkt.bieu-mau.sql-tu-do.enabled=true`. Guard: JSqlParser chỉ cho `SELECT` (cấm `;`, CTE ghi,
`INTO`, hàm nguy hiểm), bảng thuộc whitelist schema (`public.tax_*`, `sal_*`, `pur_*`, `mst_*`), tham số
bind `:ten` (không nối chuỗi), `statement_timeout`, `LIMIT` ép, role `pmkt_app` (RLS vẫn áp). Quyền riêng
`BieuMau.SqlTuDo`. → **cần user chốt có làm không (§12 Q2)**.

### 6.3 Tham số nhập tay & JSON tĩnh

`THAM_SO` (form hỏi người dùng lúc in, dựng từ `thamSo[]` — tái dùng `ReportParamsForm` của domain-kit)
và `TINH` (dữ liệu JSON gắn trong mẫu — dùng cho bảng mã cố định, dòng mẫu).

### 6.4 API JSON từ cell-app (giai đoạn 2)

`API_JSON`: gọi endpoint nội bộ cell-app bằng `X-Internal-Token`, map trường bằng JSONPath. Dùng khi dữ
liệu chỉ có qua service (đã tính bởi nghiệp vụ, ví dụ số liệu tờ khai bổ sung đã tổng hợp).

---

## 7. Kết xuất

Bước chung: **LuoiKetXuat** (RenderGrid) = lưới đã nở dòng chi tiết/nhóm, đã tính công thức, đã
resolve style, còn giữ **giá trị gốc + kiểu + pattern** cho từng ô. Ba renderer đọc cùng một
RenderGrid — không renderer nào đọc lại định nghĩa hay dataset.

### 7.1 PDF (chuẩn)

RenderGrid → `JasperDesign` bằng Java API (như `GenericPdfDesignBuilder`): cột → `x`, dòng → `y`, ô
gộp → một text field kích thước gộp, viền → `lineBox`, dòng HEADER lặp → `columnHeader`, dòng
`CHAN_TRANG` → `pageFooter`, phần tử nổi → `image`/`staticText`. Vì lưới đã nở sẵn, Jasper chỉ cần
một dataset phẳng "dòng lưới" và một detail band có chiều cao theo dòng — ngắt trang, lặp header,
`PAGE()/PAGES()` do Jasper đảm nhiệm. Font nhúng (`Identity-H`). Cache `JasperReport` theo
`sha256(cấu trúc lưới không dữ liệu) + kho + hướng`, LRU 200.

Đường thay thế đã dự phòng (nếu spike GĐ0 cho thấy Jasper tốn công): RenderGrid → HTML/CSS → PDF
bằng OpenHTMLtoPDF (thêm 1 dependency), giữ nguyên toàn bộ tầng trên.

### 7.2 Excel — native từ lưới (POI)

RenderGrid → `XSSFWorkbook`: rộng cột, cao dòng, gộp ô, viền, font, nền, **pattern số giữ nguyên**
(`#,##0;(#,##0);;`), ô số là số thật, ngày là ngày thật, ảnh neo ô, page setup (khổ/hướng/lề/vùng
in/`RepeatingRows` cho header lặp/fit-to-width). Kết quả **trùng 1:1 file mẫu §2A** và người dùng cộng
tiếp được. Tái dùng `core.shared.excel.ExcelStyles` của cell-app cho style; `SXSSF` khi > 20 000
dòng. (Bỏ `JRXlsxExporter` — không cần khi đã có lưới.)

### 7.3 Word — native từ lưới (POI XWPF)

RenderGrid → `XWPFDocument`: mỗi vùng dòng liên tục có viền → một `XWPFTable` (gộp ô = `gridSpan`/
`vMerge`), dòng không viền → đoạn văn, khổ/hướng/lề theo `sectPr`, header/footer trang với số trang
(field `PAGE`/`NUMPAGES`). Ảnh nổi → inline picture neo đoạn. Chất lượng: bảng biên tập được thật
(khác `JRDocxExporter` ra text-box). BA không yêu cầu Word nên xếp cuối GĐ3, ~1 tuần vì cùng RenderGrid.

### 7.4 Bộ in nhiều biểu mẫu (tờ khai + phụ lục)

`POST /api/bieu-mau/ket-xuat-bo` `{muc:[{ma, thamSo}], format, danhSoLienTuc:true}`: fill từng mẫu → đếm
trang → fill lại lần 2 với `$P{TRANG_BAT_DAU}`, `$P{TONG_TRANG}` → gộp `JasperPrint.pages` (tiền lệ
`InPhieuThuChi.xuatPdf` nhiều liên) → export một file. Thứ tự và bắt buộc/tuỳ chọn do caller (module
thuế) quyết theo BR_IN_01/02.

### 7.5 Giới hạn & bất đồng bộ

Đồng bộ nếu ước lượng ≤ `max-sync-rows` (5 000) và ≤ 10 s; vượt → tạo job (Quartz đã có trong
report-service), lưu MinIO, FE poll `GET /ket-xuat/jobs/{id}` (hợp đồng `/exports/{jobId}` đã có trong
`reportApi.ts`).

---

## 8. Lưu trữ & phiên bản

Schema `bieu_mau` (Flyway riêng của report-service: `spring.flyway.schemas=bieu_mau`,
`table=flyway_schema_history_bieu_mau`, locations `classpath:db/bieu_mau` — không đụng history của
cell-app; § 12 Q9).

| Bảng | Cột chính | Ghi chú |
|---|---|---|
| `bm_bieu_mau` | `id uuid`, `tenant_id uuid NULL`, `ma varchar(64)`, `ten`, `nhom` (`THUE_GTGT`, `CHUNG_TU`, `KHAC`), `mo_ta`, `trang_thai` (`NHAP`/`DA_PHAT_HANH`/`LUU_TRU`), `phien_ban_hien_hanh_id`, `ke_thua_tu_id` (mẫu hệ thống gốc), audit + soft delete | `tenant_id NULL` = mẫu hệ thống do vendor seed; RLS: `tenant_id IS NULL OR tenant_id = fn_current_tenant()`; ghi chỉ khi `= fn_current_tenant()` hoặc vai trò hệ thống. UNIQUE `(coalesce(tenant_id,'0'), ma) WHERE da_xoa=false` |
| `bm_phien_ban` | `id`, `bieu_mau_id`, `so_phien_ban int`, `dinh_nghia jsonb`, `schema_version int`, `hash char(64)`, `hieu_luc_tu date`, `hieu_luc_den date NULL`, `trang_thai` (`NHAP`/`DA_PHAT_HANH`), `ghi_chu`, audit | Bản NHÁP duy nhất/mẫu; PHÁT HÀNH là bất biến (sửa = tạo phiên bản mới). Chọn phiên bản: `hieu_luc_tu <= ngày < hieu_luc_den`, ưu tiên tenant |
| `bm_nguon_sql` | `id`, `tenant_id NULL`, `ma`, `ten`, `sql text`, `tham_so jsonb`, `truong jsonb`, audit | Chỉ khi bật SQL tự do |
| `bm_tai_san` | `id`, `tenant_id NULL`, `ten`, `loai` (`ANH`), `object_key` (MinIO), `mime`, `kich_thuoc`, `sha256` | Logo, ảnh chữ ký mẫu |
| `bm_nhat_ky_ket_xuat` | `id`, `tenant_id`, `bieu_mau_id`, `phien_ban_id`, `format`, `tham_so jsonb`, `so_trang`, `thoi_gian_ms`, `nguoi`, `luc` | Audit + đo hiệu năng; giữ 90 ngày |

Xuất/nhập mẫu: file `.pmkt-form.json` = `{bieuMau, phienBan.dinhNghia, taiSan[] (base64)}` để chuyển
giữa môi trường; import kiểm schema + kiểm ảnh bằng Tika.

---

## 9. API (prefix `/api/bieu-mau`, qua cell-app proxy → report-service)

| Method & path | Mục đích | Quyền |
|---|---|---|
| `POST /search` · `GET /{id}` · `POST /them-moi` · `PUT /{id}` · `DELETE /{id}` | CRUD danh sách (dùng khung `BaseCrudController` 8 endpoint của `core/` + `@Searchable`) | `BieuMau.View/Create/Edit/Delete` |
| `POST /{id}/nhan-ban` · `POST /{id}/ke-thua` | Nhân bản; tạo bản tenant từ mẫu hệ thống | `BieuMau.Create` |
| `GET /{id}/phien-ban` · `GET /{id}/phien-ban/{pv}` | Lịch sử, xem định nghĩa | `BieuMau.View` |
| `PUT /{id}/nhap` | Lưu bản nháp (autosave, `If-Match` hash chống ghi đè) | `BieuMau.Edit` |
| `POST /{id}/phat-hanh` `{hieuLucTu, hieuLucDen, ghiChu}` | Đóng băng phiên bản | `BieuMau.Publish` |
| `POST /{id}/khoi-phuc/{pv}` | Lấy phiên bản cũ làm nháp mới | `BieuMau.Edit` |
| `POST /kiem-tra` `{dinhNghia}` | Validate schema + công thức + binding, trả danh sách lỗi có `duongDan` JSON | `BieuMau.Edit` |
| `POST /xem-truoc?format=pdf` `{dinhNghia, thamSo, duLieuMau:true}` | Render bản nháp (không lưu) | `BieuMau.Edit` |
| `POST /{ma}/ket-xuat?format=pdf|xlsx|docx` `{thamSo, ngayHieuLuc}` | Kết xuất mẫu đã phát hành | `BieuMau.Export` hoặc quyền của module gọi (S2S) |
| `POST /ket-xuat-bo` | Bộ in nhiều mẫu, đánh số trang liên tục | như trên |
| `GET /ket-xuat/jobs/{id}` | Trạng thái job lớn | |
| `GET /nguon-du-lieu` · `GET /nguon-du-lieu/{ma}` · `POST /nguon-du-lieu/{ma}/du-lieu-mau` | Catalog cho designer, schema trường, dữ liệu mẫu | `BieuMau.Edit` |
| `GET /cong-thuc/ham` | Danh mục hàm + chữ ký + mô tả (autocomplete) | `BieuMau.Edit` |
| `GET /font` | Whitelist font nhúng | |
| `POST /tai-san` · `GET /tai-san/{id}/noi-dung` | Ảnh/logo | `BieuMau.Edit` |
| `POST /nhap-khau` · `GET /{id}/xuat-khau` | JSON mẫu | `BieuMau.Import/Export` |
| `POST /nhap-tu-excel` (multipart, chọn sheet) → `{dinhNghia, token[]}` · `POST /nhap-tu-excel/anh-xa` | Đọc sheet Excel (rộng cột, cao dòng, gộp, viền, font, pattern, page setup, token `##…##`) thành định nghĩa lưới + danh sách token cần map; gợi ý map theo tên trường dataset | `BieuMau.Import` |
| `GET /{id}/xuat-excel-mau` | Xuất ngược định nghĩa thành file Excel mẫu có token (để sửa ngoài rồi nhập lại) | `BieuMau.Export` |
| `GET /schema/v1` | JSON Schema định nghĩa (FE sinh Zod/kiểm) | |
| **S2S** `POST /internal/bieu-mau/ket-xuat[-bo]` | Cho `cell-app` (module thuế) gọi, `X-Internal-Token` | kiểm quyền ở cell-app |

Mọi response bọc `ApiResponse<T>`; file trả `ResponseEntity<InputStreamResource>` + `Content-Disposition`
(tiền lệ `ReportController`). Mã lỗi: `BM_SCHEMA_KHONG_HOP_LE`, `BM_CONG_THUC_LOI`, `BM_CONG_THUC_VONG`,
`BM_NGUON_KHONG_TON_TAI`, `BM_PHIEN_BAN_XUNG_DOT` (409), `BM_QUA_GIOI_HAN` (413), `BM_KET_XUAT_THAT_BAI`.

---

## 10. Frontend

### 10.1 Cấu trúc (theo `fe-khung-kien-truc-chuan.md`)

```
client/src/features/bieuMau/
├── routes.tsx
├── _shared/                     (tạo ngay vì có 2 module thật)
│   ├── api/bieuMauApi.ts        Zod schema định nghĩa v1 (sinh từ /schema/v1), CRUD, xem trước, kết xuất
│   ├── constants/{paths,permissions}.ts
│   └── i18n/
├── danhSachBieuMau/             MÀN QUẢN LÝ
│   ├── components/  BieuMauList.tsx · modal/ThemSuaBieuMauModal.tsx · modal/PhatHanhModal.tsx
│   │                modal/LichSuPhienBanDrawer.tsx · modal/NhapKhauModal.tsx
│   ├── fields/ hooks/ pages/BieuMauListPage.tsx test/
└── thietKeBieuMau/              DESIGNER (full-screen, ẩn menu trái)
    ├── components/
    │   ├── DesignerShell.tsx            bố cục 3 cột + toolbar + statusbar
    │   ├── canvas/  PageCanvas.tsx · BandView.tsx · ElementView.tsx · TableView.tsx · SelectionBox.tsx
    │   │            Rulers.tsx · Guides.tsx · ResizeHandles.tsx
    │   ├── palette/ ElementPalette.tsx (dnd-kit draggable)
    │   ├── panels/  OutlinePanel.tsx · DataPanel.tsx (tham số/nguồn/biến) · PropertiesPanel.tsx
    │   │            StylePanel.tsx · TableEditorPanel.tsx · PageSetupModal.tsx
    │   ├── formula/ FormulaEditor.tsx (CodeMirror 6 + ngôn ngữ riêng) · FunctionHelp.tsx
    │   └── preview/ PreviewDrawer.tsx (iframe PDF blob) · ExportMenu.tsx
    ├── helpers/  geometry.ts (snap, align, distribute) · formulaLang.ts (parser TS) · serialize.ts
    ├── hooks/    useDesignerStore.ts (zustand + immer + zundo) · useAutosave.ts · useKeyboard.ts
    │             usePreview.ts · useDataCatalog.ts
    ├── fields/ constants/ i18n/ pages/ThietKeBieuMauPage.tsx test/
```

Route: `/bieu-mau` (danh sách), `/bieu-mau/:id/thiet-ke` (designer). Menu "Hệ thống › Biểu mẫu động".
Nút "In" ở module thuế dùng `base/domainKit/bieuMau/` (`NutInBieuMau`, `ChonPhuLucInModal`) — hợp đồng
giống `inPhieuApi.ts` hiện có (blob → tab mới).

### 10.2 Designer — bố cục & trải nghiệm

```
┌ Toolbar: [Lưu] [Phát hành ▾] │ ↶ ↷ │ Zoom 50–200 % │ Lưới ▢ Snap ▢ Thước ▢ │ Khổ giấy ▾ │ [Xem trước ▾ PDF/Excel/Word] ┐
├──────────────┬──────────────────────────────────────────────────┬──────────────────────────────┤
│ Palette      │  thước ngang                                     │ Thuộc tính (theo chọn)       │
│  T Text      │ ┌──────────── trang A4 (bóng đổ, nền xám) ─────┐ │  ▸ Vị trí/kích thước x y w h │
│  ▤ Trường    │ │ [TIÊU ĐỀ]  ────────────────────────────────  │ │  ▸ Nội dung / Công thức  fx  │
│  ☐ Checkbox  │ │   GIẢM THUẾ GTGT THEO NQ 204/2025            │ │  ▸ Kiểu chữ  font cỡ B I U   │
│  ▦ Bảng      │ │   [04] Tên NNT: {header.tenNnt}              │ │  ▸ Căn lề · Viền · Nền       │
│  ▭ Hình chữ  │ │ [BẢNG mucI] ┌──┬────────┬──────┬──────┐      │ │  ▸ Định dạng số/ngày         │
│  ─ Đường     │ │             │ST│Tên HHDV│Giá trị│Thuế  │      │ │  ▸ Ẩn khi …  Style khi …     │
│  🖼 Ảnh       │ │             ├──┼────────┼──────┼──────┤      │ │                              │
│  # Số trang  │ │             │fx│row.ten │row.gt│ROUND │      │ ├──────────────────────────────┤
│ ─────────────│ │             ├──┴────────┼──────┼──────┤      │ │ Outline / Dữ liệu (tab)      │
│ Dữ liệu      │ │             │Tổng       │SUM() │SUM() │      │ │  ▾ Khối                      │
│  ▾ header    │ │ [KHỐI TỰ DO] [08] Chênh lệch: {ct08}         │ │    ▾ Bảng mucI …             │
│    tenNnt    │ │ [CHÂN TRANG]                Trang 1/{tổng}   │ │  ▾ Tham số · Nguồn · Biến    │
│  ▾ mucI …    │ └──────────────────────────────────────────────┘ │                              │
├──────────────┴──────────────────────────────────────────────────┴──────────────────────────────┤
│ Statusbar: 3 lỗi công thức ⚠ · đã lưu nháp 10:42 · A4 dọc · 595×842 pt                          │
```

**Canvas là một lưới ô kiểu Excel** (sơ đồ trên vẽ minh hoạ; thực tế mọi thứ nằm trong ô): đầu cột
`A B C…` kéo đổi rộng, đầu dòng kéo đổi cao, dải màu bên trái đánh dấu **loại dòng** (xám = tĩnh, xanh =
header lặp, vàng = chi tiết nở theo `bkbr`, cam = tổng nhóm, tím = chân trang), vùng nhóm được viền
khung có tên. Tương tác: chọn ô/vùng (Shift/kéo), gộp/bỏ gộp, chèn/xóa dòng/cột, kéo trường từ panel
Dữ liệu thả vào ô (tự sinh công thức `row.x` và tự đặt dòng thành CHI_TIẾT nếu trường thuộc dataset
nhiều dòng), gõ trực tiếp text vào ô, `=` mở formula editor, format painter, sao chép/dán style, undo/
redo 100 bước, zoom, phím tắt Excel quen thuộc (Ctrl+B/I, Ctrl+S, Ctrl+Z/Y, Del). Phần tử nổi: kéo từ
palette thả lên ô, kéo/resize bằng handles. Formula editor: tô màu, gợi ý trường/hàm/biến, kiểm cú
pháp tức thì (parser TS), kiểm ngữ nghĩa khi Lưu (BE `/kiem-tra`) hiện lỗi tại ô (viền đỏ + panel
lỗi). Xem trước: gọi BE với dữ liệu mẫu hoặc tham số tự nhập, PDF trong drawer (iframe blob), Excel/
Word tải xuống; đường ngắt trang ước lượng vẽ mờ trên lưới. Lưới render bằng DOM (`<div>` grid ảo
hoá theo dòng, không `<canvas>`) để chữ sắc nét, đo được bằng test — hoặc nhúng Univer nếu spike Q14
cho thấy lợi hơn.

Nhập từ Excel: modal chọn file → chọn sheet → xem trước lưới đã đọc → bảng map token `##…##` ↔ trường
dataset (gợi ý tự động theo tên, ô chưa map viền vàng) → tạo biểu mẫu nháp.

Giao diện: theo design token của app (antd 6), nền canvas tối nhẹ, trang trắng bóng đổ, panel bo góc,
icon Phosphor (đã có). Sẽ dựng mockup Figma/Stitch trước khi code nếu user muốn (§12 Q11).

### 10.3 Thư viện thêm vào `client/` (cần duyệt)

| Thư viện | Dùng cho | Cỡ |
|---|---|---|
| `zustand` + `immer` + `zundo` | store designer, undo/redo | nhỏ |
| `@dnd-kit/core` | kéo trường / phần tử nổi từ panel vào ô | nhỏ |
| `@codemirror/state`, `@codemirror/view`, `@codemirror/autocomplete`, `@codemirror/language` | ô công thức | vừa, chỉ nạp lazy trong designer |
| (tuỳ Q14) `@univerjs/*` | lõi lưới nếu không tự dựng | nặng ~2 MB, lazy |

Không thêm pdf.js (dùng viewer trình duyệt), không thêm react-moveable (handles phần tử nổi viết bằng
pointer events). `exceljs` đã có trong client chỉ dùng đọc nhanh sheet để xem trước khi nhập; phân tích
thật làm ở BE (POI) để FE/BE không lệch.

---

## 11. Bảo mật, hiệu năng, vận hành

- **Không chạy mã người dùng**: cấm nhận JRXML/`.jasper`, cấm scriptlet, biểu thức Jasper sinh ra chỉ là
  `$F{…}`/`$P{…}`; công thức chạy trong engine PMKT có giới hạn.
- SQL tự do: guard §6.2, quyền riêng, tắt mặc định, ghi audit mọi lần chạy.
- Ảnh: Tika sniff MIME, ≤ 2 MB, chỉ PNG/JPEG/SVG (SVG lọc script), lưu MinIO.
- Tenant: RLS trên mọi bảng `bm_*`; mẫu hệ thống `tenant_id NULL` chỉ vai trò vendor sửa.
- Giới hạn: dòng/dataset, thời gian đánh giá, thời gian render, kích thước file; vượt → 413/job.
- Cache compile Jasper theo hash; cache catalog nguồn; metrics `bieu_mau_ket_xuat_seconds{format}`.
- Ranh giới ArchUnit §3.1; test: parser (bảng ca JSON dùng chung FE/BE), evaluator, compiler (đọc ngược
  PDF bằng PDFBox test-scope như `SpikeJasperTiengVietTest`), golden-file PDF cho 8 mẫu thuế.
- Truy vết luật: luật của module này là luật kỹ thuật (`R-BM-…`) ghi trong `docs/doing/bieu-mau-dong/02-rules.md`
  khi bước sang giai đoạn plan; luật thuế (`R-…` của epic 10978) vẫn thuộc module thuế.

---

## 12. Điểm cần user CHỐT trước khi lập kế hoạch chi tiết

| # | Câu hỏi | Đề nghị của tôi |
|---|---|---|
| Q1 | Vị trí BE: **A** module trong `report-service` / B service mới / C trong `cell-app` | **A** |
| Q2 | Có làm nguồn **SQL tự do** cho quản trị không? | Có, nhưng giai đoạn 5, tắt mặc định |
| Q3 | Word: có cần trong v1 không? BA không yêu cầu; với grid-first xuất DOCX native (POI XWPF) chỉ ~1 tuần | Làm cuối GĐ3 |
| Q4 | Font: `report-service` đang copy **Times New Roman của Windows** (độc quyền MS). Whitelist font cho mẫu: Times New Roman + Liberation Serif + DejaVu Sans? Có cần Arial? | Liberation Serif (metric = TNR, giấy phép OFL) làm mặc định; giữ TNR nếu pháp chế đồng ý |
| Q5 | Ai được thiết kế mẫu: chỉ vendor/quản trị hệ thống, hay từng tenant (kế toán) cũng tự sửa? | Cả hai: vendor seed mẫu hệ thống; tenant kế thừa & sửa bản của mình; quyền `BieuMau.*` |
| Q6 | Khổ/hướng giấy từng mẫu thuế (BA không nêu): PL 01-6 ~13 cột, 01-1/KHBS 8 cột nên ngang? | Mặc định A4 dọc; PL 01-6, 01-1/KHBS, BKBR/BKMV A4 ngang — BA xác nhận |
| Q7 | Giai đoạn đầu có seed 8 mẫu thuế không khi **bảng tờ khai chưa có**? | Có, chạy bằng provider dữ liệu mẫu; nối dữ liệu thật khi epic 10978 có DB |
| Q8 | Duyệt thêm thư viện FE §10.3 | Duyệt |
| Q9 | Migration: bật Flyway riêng cho `report-service` (schema `bieu_mau`, history table riêng) hay đặt migration ở `cell-app`? | Flyway riêng (để tách service sau không kéo theo lịch sử cell-app) |
| Q10 | Đặt tên: module `bieu_mau`, bảng `bm_*`, API `/api/bieu-mau`, quyền `BieuMau.*`, feature FE `bieuMau` | Như trên |
| Q11 | Có cần mockup UI (Figma/Stitch) duyệt trước khi code designer không? | Nên, 1–2 ngày |
| Q12 | Thứ tự ưu tiên tính năng "và nhiều tính năng khác tương tự Jasper": barcode/QR, biểu đồ, mẫu con, ảnh động, chữ ký số, watermark, in nhiều bản/liên, đánh số trang lẻ/chẵn — cái nào vào v1? | v1: mẫu con + watermark + nhiều liên; QR/barcode v2; biểu đồ v3 |
| Q13 | **Mô hình bố cục**: grid-first (lưới ô kiểu Excel, §4) hay canvas tuyệt đối kiểu Jasper Studio? | **Grid-first** — khớp file mẫu §2A, Excel 1:1; phần tử nổi neo ô phủ nhu cầu logo/hộp chữ |
| Q14 | Lõi lưới ở FE: **tự dựng** (DOM, ~3 tuần, kiểm soát hoàn toàn) hay nhúng engine bảng tính mã nguồn mở (Univer, MIT, nặng ~2 MB, có sẵn merge/style/resize/undo)? | Spike GĐ0 đo cả hai trên sheet 6 (32 cột, 98 vùng gộp); nghiêng về **tự dựng** |
| Q15 | Nhập từ Excel: chỉ nhận file có token `##…##` hay nhận cả file đã điền số (số liệu → giá trị tĩnh) | Nhận cả hai |
| Q16 | Sản phẩm tham chiếu (nguồn file mẫu) là gì, có cần **tương thích tên token** của nó để tái dùng mẫu sẵn có không? | Hỗ trợ bảng ánh xạ token → trường, không ràng buộc tên |

---

## 13. Lộ trình & ước lượng (thô, 1 BE + 1 FE, chưa tính review/QA)

| GĐ | Nội dung | Thời gian | Đầu ra |
|---|---|---|---|
| 0 | **Spike**: (a) RenderGrid → Jasper PDF cho sheet 1 + sheet 6 của file mẫu (ngắt trang, lặp header, gộp ô, font Việt); (b) lõi lưới FE tự dựng vs Univer trên sheet 6 (32 cột, 98 gộp); (c) POI đọc sheet → lưới round-trip; (d) số trang liên tục 2 lượt | 1 tuần | Biên bản spike + chốt Q14 |
| 1 | **Nền tảng BE**: schema JSON v1 + validator, Flyway `bm_*`, CRUD + phiên bản + phát hành, engine công thức (parser/evaluator/hàm) + bộ test, SPI nguồn + 2 provider mẫu, nở lưới (nhóm/chi tiết/tổng) → RenderGrid → PDF (Jasper) + XLSX (POI), **nhập từ Excel**, xem trước, S2S, proxy cell-app, ArchUnit | 3–4 tuần | 11 sheet file mẫu nhập được và kết xuất lại PDF/XLSX giống bản gốc |
| 2 | **Màn quản lý + Designer MVP**: danh sách CRUD/nhân bản/phiên bản/nhập Excel; designer lưới: chọn ô/vùng, gộp, kéo rộng cột/cao dòng, style ô (font/viền/nền/căn/định dạng số), kéo trường từ panel Dữ liệu thả vào ô, gán loại dòng (tĩnh/header/chi tiết/tổng), page setup, undo/redo, autosave, xem trước PDF, kết xuất | 4 tuần | Thiết kế được 01/GTGT, bảng kê đơn giản |
| 3 | **Nhóm, công thức, phần tử nổi, Word**: vùng nhóm lồng + dòng tổng nhóm, formula editor (CodeMirror, autocomplete, kiểm lỗi), style có điều kiện, `renderKhi`, mẫu con/vùng lồng, ảnh/hộp chữ nổi, xuất DOCX | 3 tuần | Thiết kế được đủ 11 sheet + 01/KHBS, 01-1/KHBS |
| 4 | **Thuế**: provider `thue.*`, seed 8 mẫu hệ thống theo mẫu TT80/TT40 (đối chiếu PDF mẫu của TCT), bộ in gộp + đánh số liên tục, nút In tờ khai/phụ lục, golden test | 2–3 tuần | In được bộ tờ khai + phụ lục |
| 5 | **Hoàn thiện**: import/export JSON, hiệu lực theo kỳ, SQL tự do (nếu Q2 = có), job bất đồng bộ, watermark/nhiều liên, QR, e2e Playwright, tài liệu hướng dẫn | 2–3 tuần | Bàn giao |

Tổng: **15–18 tuần** lịch. Giai đoạn 1 và 2 chạy song song được (BE/FE), rút còn ~12–14 tuần.

---

## 14. Rủi ro chính

| Rủi ro | Giảm thiểu |
|---|---|
| Jasper khó tái tạo lưới gộp ô phức tạp (sheet 6: 98 vùng gộp) hoặc lặp header/ngắt trang không như ý | Spike GĐ0 trên chính sheet 1 và 6; fallback RenderGrid → HTML/CSS → PDF (OpenHTMLtoPDF), tầng trên không đổi |
| Lưới rộng hơn trang (sheet 1 tràn 17 in) hoặc quá nhiều cột hẹp (sheet 6: 32 cột) làm PDF chữ nhỏ | Cảnh báo tràn trong designer; `coGiuTrang` có sàn cỡ chữ; khuyến nghị vùng lồng thay cột hẹp |
| Bản quyền font Times New Roman | Q4 |
| Dữ liệu thuế chưa tồn tại → seed mẫu chỉ kiểm bằng dữ liệu giả | Provider `duLieuMau()`; nối thật khi epic 10978 xong |
| Phạm vi "tương tự Jasper" mở vô hạn | Q12 chốt v1/v2/v3 |
| Hai parser (Java/TS) lệch nhau | Bộ ca test JSON dùng chung, CI chạy cả hai |

---

## 15. Bước tiếp theo sau khi confirm

1. Chốt §12 → cập nhật tài liệu này thành bản "đã chốt" (ghi tên người + ngày).
2. Mockup designer (Q11) → duyệt.
3. Spike GĐ0 → biên bản.
4. `/plan-be` + `/plan-fe` cho module (kế hoạch file-by-file, luật `R-BM-…`, bảng truy vết), rồi `/gen-*`.
