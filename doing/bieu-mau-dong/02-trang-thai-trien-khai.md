# Trạng thái triển khai — module biểu mẫu động (cập nhật 2026-09-09)

Nguồn sự thật thiết kế: [00-giai-phap.md](00-giai-phap.md) · hợp đồng kỹ thuật:
[01-hop-dong-v1.md](01-hop-dong-v1.md) · công cụ sinh seed: `tools/sinh_seed_tu_excel.py`.

## 1. Đã làm (working tree, CHƯA commit ở cả 3 repo)

| Repo | Thành phần | Ghi chú |
|---|---|---|
| `report-service` (nhánh `develop`) | Module Modulith `vn.vtt.pmkt.cell.bieu_mau` — 157 file: `internal/{port,dinh_nghia,cong_thuc,luoi,no_luoi,ket_xuat/{jasper,poi},nhap_excel,nguon,engine,kho,dto,service,controller,config,seed}` | Engine JSON → lưới → PDF (Jasper) / XLSX (POI) / DOCX (XWPF); công thức 47 hàm; nhập Excel; catalog nguồn; CRUD + phiên bản + phát hành; seed hệ thống |
| | Flyway riêng `db/bieu_mau/V20260908210000__bm_bieu_mau.sql` (schema `bieu_mau`, history `flyway_schema_history_bieu_mau`) | **Đã áp lên DB dev chung** `100.100.1.5:15433/pmkt_cell` ngày 2026-09-09 |
| | `bieu_mau/seed/*.json` (11 mẫu) + `bieu_mau/nguon/*.json` (20 nguồn mẫu + 2 nguồn test) | Sinh từ file Excel mẫu; runner `SeedBieuMauHeThong` đã upsert 11/11 lúc khởi động |
| | Sửa `InternalCallerFilter` (bảo vệ thêm `/api/bieu-mau/`), `application.yml` (flyway + `pmkt.bieu-mau`) | |
| `cell-app` (nhánh `feat/chung-tu-ban-hang-2`) | Module `bieu_mau_proxy` (`/api/bieu-mau/**` → S2S report-service, kiểm quyền `BieuMau.*` theo method/path), `api/BieuMauExportApi` cho module khác | `V1111__iam_quyen_bieu_mau.sql` seed 7 mã quyền — **đã áp lên DB dev** |
| `client` (nhánh `feat/chung-tu-ban-hang-2`) | `src/features/bieuMau/` — 93 file: `_shared` (Zod schema v1, api, i18n), `danhSachBieuMau` (màn quản lý), `thietKeBieuMau` (designer lưới) | Nối route `/bieu-mau`, `/bieu-mau/:id/thiet-ke`, menu "Biểu mẫu động" nhóm Khác; thêm dep `zustand`, `immer`, `zundo`, `@dnd-kit/core` |
| `deploy` | `env/osp-cell-app.env` thêm `PMKT_REPORT_SERVICE_URL=http://localhost:8092` | Cần cho proxy (bean `@ConditionalOnProperty`) |

## 2. Cổng đã chạy (nguyên văn)

```
report-service: ./gradlew compileJava compileTestJava -q  → exit 0
report-service: ./gradlew unitTest                          → BUILD SUCCESSFUL · tests=180 skipped=0 fail=0
cell-app:       ./gradlew compileJava compileTestJava -q  → exit 0
cell-app:       ./gradlew unitTest --tests 'vn.vtt.pmkt.cell.bieu_mau_proxy.*' --tests 'vn.vtt.pmkt.cell.arch.*' → BUILD SUCCESSFUL · tests=69 fail=0
client:         npx vitest run src/features/bieuMau --reporter=dot → Test Files 9 passed · Tests 108 passed
client:         npx vite build → ✓ built in 1.79s
client:         npx tsc -p tsconfig.app.json --noEmit | grep bieuMau|app/router|app/layouts|app/i18n → 0 dòng
client:         npx eslint src/features/bieuMau src/app/router/RootRoutes.tsx src/app/layouts/shell/menuRegistry.tsx → sạch
```

KHÔNG chạy: `./gradlew build`/`test` đầy đủ (Testcontainers cần Docker), `npm run typecheck`/`lint`/
`lint:boundaries`/full suite toàn repo (nền đỏ sẵn, theo `client/CLAUDE.md §15`), `check:committed`
(chưa commit).

## 3. Chạy thật end-to-end (đã làm ngày 2026-09-09)

1. `report-service` chạy nền `./gradlew bootRun` với env `deploy/env/osp-report-service.env` +
   `SPRING_FLYWAY_ENABLED=true` (lần đầu để tạo schema) — log: schema `bieu_mau` tạo, seed 11/11.
2. `cell-app` khởi động lại qua IntelliJ `PmktCellApplication` — Flyway áp `V1111`, lên sau 37 s.
3. S2S `POST http://localhost:8092/internal/bieu-mau/ket-xuat?format=pdf|xlsx|docx` với
   `X-Internal-Token` + `X-Tenant-Id`, `{"ma":"<MA>","duLieuMau":true}` → **33/33 HTTP 200**
   (11 mẫu × 3 định dạng), file ở `tmp/out/`. Đã soi PDF Bảng kê bán ra, Tờ khai 01/GTGT, Tờ khai bổ
   sung: đúng bố cục file mẫu; XLSX: số là số thật + pattern `#,##0;(#,##0)`, ngày thật, gộp ô, lặp
   header `$4:$5`, khổ/hướng đúng.
4. Bảo mật: `POST http://localhost:8081/api/bieu-mau/tim-kiem` không JWT → 401;
   `POST http://localhost:8092/api/bieu-mau/tim-kiem` không token nội bộ → 403.
5. Lỗi phát hiện & đã vá lúc chạy thật: `NguCanh.goc` dùng `Map.copyOf` → NPE khi tham số
   `toKhaiId` chưa truyền (null). Đã thay bằng bản sao cho phép null.

**Chưa kiểm được trên trình duyệt**: màn `/bieu-mau` và designer cần đăng nhập; tôi không tự nhập
mật khẩu. Bước còn lại cho người dùng: đăng nhập `http://localhost:5173` (tài khoản dev theo
`docs/rules/huong-dan-tao-tenant-user-phan-quyen.md`), vào menu **Khác › Biểu mẫu động** → thấy 11
mẫu hệ thống → "Nhân bản" một mẫu → "Thiết kế" → sửa ô/kéo trường → "Xem trước PDF" → "Phát hành".

## 4. Lệch so với hợp đồng/đề xuất (có chủ ý)

- `nhan-ban` yêu cầu `BieuMau.Edit` (00-giai-phap ghi Create); `POST /tim-kiem` → View.
- `BieuMauChiTiet` có thêm `hashNhap`; `KieuDang` có thêm `mauSoAm`, `xoay`; mã lỗi bổ sung
  `BM_SCHEMA_LOI`, `BM_KIEU_DANG_KHONG_TON_TAI`, `BM_DONG_KHONG_TON_TAI`, `BM_DINH_DANH_KHONG_TON_TAI`,
  `BM_THAM_SO_THIEU`, `BM_DINH_NGHIA_KHONG_HOP_LE`, `BM_KET_XUAT_LOI`, `BM_NHAP_EXCEL_LOI`.
- Seed hệ thống bằng Java runner (`SeedBieuMauHeThong`, cửa RLS `app.bm_seed`) thay vì
  `R__bm_seed_he_thong.sql`.
- Migration cell-app đánh số `V1111` (theo `cell-app/CLAUDE.md`, không timestamp).
- `BieuMauProxyRest` nằm trong `ProxyArchTest.NGOAI_LE` cùng lý do `ReportServiceRest`
  (`integration_ops.proxy.ProxyClient` không truyền byte/multipart) — nợ chung, chưa xử lý.
- Font ngoài whitelist trong file mẫu (Microsoft Sans Serif, Arial) map về Times New Roman.
- Test render FE tự dựng provider (lint cấm `features/**` import `src/test/**`).

## 5. Chưa làm / giới hạn v1

- Nguồn dữ liệu thuế mới có `duLieuMau()`; `nap()` thật ném `BM_NGUON_CHUA_SAN_SANG` (bảng tờ khai
  chưa tồn tại — chờ epic PMKT-E-10978).
- Ảnh nổi từ MinIO (`taiSanId`) chưa nạp — chỉ `base64`; DOCX chưa có ảnh nổi; bộ in nhiều khổ giấy
  dùng khổ mục đầu.
- Designer: chưa format painter, chưa kéo sắp xếp dòng, chưa UI `renderKhi`, lưới chưa ảo hoá.
- SQL tự do (Q2), QR/barcode, watermark, nhiều liên, job bất đồng bộ: chưa.
- Chưa có `docs/doing/<slug>-spec/` theo cổng đặc tả (module kỹ thuật, không có PYC BA); truy vết
  luật `R-…` chưa lập.
- Quyền hạt mịn ở report-service vẫn chỉ "đã đăng nhập" (tiền lệ `ReportAccessGuard`); kiểm mã quyền
  thật nằm ở cell-app proxy.

## 6. BR đã đối chiếu

Màn quản lý danh sách: BR1/2/11/13.1/30/31/32/38/39/44/45 — áp dụng phần chung (tìm kiếm, phân
trang server, trạng thái tag, confirm xóa, ẩn/hiện theo quyền); chưa đối chiếu từng dòng vì màn
không thuộc PYC BA. Định dạng số/tiền trên bản in theo BR7 (lưu đủ, làm tròn khi hiển thị HALF_UP)
và BR_IN_03 của epic 10978 (A4, số âm trong ngoặc, số trang `trang/tổng`).

## 7. Đợt bổ sung 2026-09-09 (sau khi user test)

- **Tắt tạm phân quyền toàn luồng** (đều đánh dấu `[TẠM 2026-09-09]`, bật lại bằng cách bỏ comment/đổi cờ):
  `cell-app BieuMauProxyController` (`@PreAuthorize`), `report-service BieuMauService.yeuCauSuaDuoc`
  (guard `BM_MAU_HE_THONG`), FE `useBieuMauGates` (`TAM_BO_QUA_QUYEN`), `helpers/hanhDongDong`
  (`TAM_MO_MAU_HE_THONG`); 2 test FE `.skip` + 1 test BE `@Disabled` tương ứng. Vẫn cần đăng nhập (JWT).
- **Giao diện danh sách theo chuẩn chứng từ**: bỏ tiêu đề trang; bảng `fillHeight` (header dính, thân
  cuộn); phễu lọc + sắp xếp từng cột (controlled, server-side; `POST /tim-kiem` nhận thêm `ma/ten` +
  toán tử, `nhom[]`, `trangThai[]`, `heThong`, `soPhienBan`, `hieuLucTu/Den`, `ngayCapNhatTu/Den`, `sapXep`);
  popup Thêm/Sửa/Nhân bản/Phát hành/Nhập Excel sang `CommonModalShell` kiểu chứng từ; drawer Lịch sử
  phiên bản theo kiểu drawer kho.
- **Nguồn dữ liệu kiểu API** (hợp đồng §9): `loai: "API"` với url/method/headers/body/thamSoQuery/
  duongDanDuLieu/sample/timeoutMs; cache theo lần kết xuất; allow-hosts `pmkt.bieu-mau.api.allow-hosts`
  (mặc định `*`, prod phải liệt kê); `POST /api/bieu-mau/nguon-du-lieu/api/kham-pha`; designer có modal
  Thêm/Sửa nguồn API + nút Khám phá + cache trường.
- **API giả có chế độ sample**: `GET http://localhost:8092/mau-api/to-khai-bo-sung?mode=sample&toKhaiId=…`
  (permitAll, tắt bằng `pmkt.bieu-mau.mau-api.enabled=false`); seed thêm mẫu
  `TO_KHAI_BO_SUNG_01_KHBS_API` dùng 5 nguồn API → đã kết xuất PDF/XLSX thành công qua S2S.
- Cổng sau đợt này: report-service `unitTest` 218 test (1 disabled) xanh; client 145 test (2 skip) xanh,
  build/tsc/eslint sạch vùng bieuMau. Sửa nhỏ: `BieuMauProperties` cần `@ConstructorBinding` (record có
  2 constructor làm Spring không bind được — phát hiện lúc khởi động thật).
