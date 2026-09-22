# Mẫu in chứng từ theo khối — Bản đồ nguồn tài liệu

| | |
|---|---|
| Phiếu yêu cầu | **Chưa có PYC trong `pmkt-docs/ba/`** — yêu cầu đến trực tiếp từ user (chat 2026-09-17) kèm mock HTML |
| Nguồn gốc | `C:\Users\DatVL\Downloads\ThietLapMauIn.html` (540 dòng, demo cho *Chứng từ mua dịch vụ*) |
| Ngày soát | 2026-09-17 |
| Mã viết tắt | `MAUIN` → luật `R-MAUIN-nnn`, bất biến `INV-MAUIN-nnn`, message `MSG_MAUIN_nnn` (tạm — Q11) |
| Trạng thái | **ĐÃ SOÁT** — 15 mục conflict: 8 `CLOSED-BA` (user chốt Q1–Q21) · 6 `CLOSED-AUTO` · **1 `OPEN` P2** (không chặn luật nào) |
| Sinh bởi | viết tay (không chạy được `/audit-spec` vì không có thư mục PYC) — cùng khuôn 4 file để `/plan-*` · `/gen-*` · `trace.sh` · `/verify-spec` dùng được |

---

## §1. Bảng file nguồn

| File | Loại | Bậc | Trạng thái | Ghi chú |
|---|---|---|---|---|
| `ThietLapMauIn.html` — `defaultState()` (:158-190) | mock — **anchor** | 4 | user duyệt | cấu trúc khối, trường, cột, mặc định bật/tắt của MDV |
| `ThietLapMauIn.html` — `checks()` (:256-268) | mock | 4 | user duyệt | 11 phép kiểm + nguyên văn message |
| `ThietLapMauIn.html` — `renderIns()` / `bindIns()` (:317-474) | mock | 4 | user duyệt | control của từng khối, giới hạn số (lề 0–5, cỡ 8–20, tiêu đề 10–36, rộng 3–90, 4 ô ký) |
| `ThietLapMauIn.html` — `renderPaper()` (:272-306) | mock | 4 | user duyệt | bố cục giấy, `two`/`flow`, bảng, chữ ký, chân trang |
| `ThietLapMauIn.html` — `#top` · `#menuDemo` (:129-145, :506-510) | mock | 4 | user duyệt | thanh trên, menu In (cố định 🔒 · tuỳ chỉnh · ⚙) |
| Chat 2026-09-17 — 5 bổ sung của user | yêu cầu | **5** | chốt | tiêu đề bảng cấu hình được · thông tin dạng bảng · khoá DON_VI/TIEU_DE · kéo thả trên giấy · bảng chi tiết theo loại · JSON · style hệ thống |
| Chat 2026-09-17 — "Đồng ý hết Q1–Q21 theo đề nghị" | quyết định | **5** | chốt | xem [01-conflict.md](01-conflict.md) |
| `docs/doing/mau-in-chung-tu/00-plan-tong-the.md` | kế hoạch | 3 | chốt | D1–D14, WBS |
| `docs/doing/mau-in-chung-tu/01-hop-dong-json-va-api-v1.md` | hợp đồng kỹ thuật | 3 | chốt | schema · catalog · API · DB · luật kiểm tra |
| `docs/doing/mau-in-chung-tu/02-anh-xa-giao-dien-va-base-component.md` | hợp đồng giao diện | 3 | chốt | token · control → `@base` · CSS cục bộ |
| `Common/business_rules.md` — BR3 · BR4/BR9 · BR16 · BR25 · BR26 · BR30 · BR43 · BR46 | BR chung | **5** | duyệt | tra qua `br.sh` |
| `pmkt-docs/ba/PMKT-E-00093_DanhMucDungChung/5.screens/SCR_LoaiChungTu/DuLieuKhoiTao_LoaiChungTu.md` | BA | 5 | duyệt | 47 loại chứng từ, cột **Mã** |

Bậc thẩm quyền khi mâu thuẫn: 5 (BR/BA/quyết định user) > 4 (mock) > 3 (plan/hợp đồng) > code hiện có.

---

## §2. Mã nguồn tham chiếu (đọc để không lệch pattern hiện hành)

| Vùng | File | Dùng làm gì |
|---|---|---|
| In hiện có | `cell-app/…/tien_mat_tien_gui/internal/service/InPhieuThuChiService.java` · `model/MauInPhieuThuChi.java` · `controller/BaseChungTuThuChiController.java:89-113` | menu mẫu cố định → `mauCoDinh()` của provider PT (GĐ2) |
| In hiện có (FE) | `client/src/features/nganQuy/_shared/components/NutInPhieu.tsx` · `api/inPhieuApi.ts` | khuôn split button, blob URL (không `window.open` API trần) |
| JSON theo màn | `cell-app/…/common/ui_config/**` (`CauHinhCot`, `CauHinhCotServiceImpl`) | `@JdbcTypeCode(SqlTypes.JSON) String`, `ObjectMapper` |
| SPI precedent | `cell-app/…/core/controller/spi/MauCotPort.java` | port hẹp, đảo chiều phụ thuộc |
| Modulith | `cell-app/src/test/java/…/arch/ProxyModularityTest.java` | mẫu test ranh giới cho module mới |
| Thông tin công ty | `cell-app/…/platform_iam/tenant/api/TenantConfigApi.java` · `internal/adapter/TenantConfigAdapter.java` · `internal/dto/CompanyInfoResponse.java` | mở thêm `thongTinDonViIn()` |
| Người dùng | `cell-app/…/platform_iam/nguoi_dung/api/NguoiDungLookupApi.java` (`hoTenTheoId`) | tên người đăng nhập cho ô Người lập phiếu |
| MDV | `cell-app/…/chung_tu_mua_hang/internal/controller/ChungTuMuaDichVuController.java` · `service/ChungTuMuaHangCrudService.java` (`getDichVu`, `layDongChiTietDichVu`, `searchDichVu`) · `dto/ChungTuMuaHangDto.java` · `dto/ChiTietChungTuMuaHangDto.java` | provider pilot |
| Tra cứu tên/mã | `cell-app/…/tien_mat_tien_gui/internal/repository/TraCuuDanhMucThuChiRepository.java:95-160` (`mst_he_thong_tai_khoan` · `mst_doi_tuong` · `mst_nhan_vien` · `mst_dieu_khoan_thanh_toan` · `mst_don_vi`) | SQL tra cứu tương đương trong module MDV |
| Số tiền bằng chữ | `cell-app/…/tien_mat_tien_gui/internal/service/business/SoTienBangChu.java` | chuyển lên `core/shared/text/` để ≥2 module dùng |
| Quyền | `cell-app/…/common/constant/MaChucNang.java` · `V3__gop_thay_doi_sau_baseline.sql:1400-1436` (`iam_quyen` nhóm "Tiện ích, thiết lập") · `V1111__iam_quyen_bieu_mau.sql` | seed `HTMauIn.*` |
| Migration | `V1145__tax_bang_ke_ban_ra_mua_vao.sql` (RLS · FORCE · GRANT `pmkt_app`) | DDL `prn_mau_in_tuy_chinh` |
| FE khuôn module | `client/src/features/heThong/dinhDangSo/**` · `features/banHang/chungTuBanHang/**` | shape module, register i18n, test provider stack |
| FE designer có sẵn | `client/src/features/bieuMau/thietKeBieuMau/hooks/useDesignerStore.ts` · `helpers/keoTha.ts` · `components/PropField.tsx` | zustand + immer + zundo, id dnd, PropField/PropSection |
| FE điểm nối | `client/src/features/heThong/routes.tsx` · `paths.ts` · `app/layouts/shell/menuRegistry.tsx:473-497` · `app/i18n/{vi,en}.ts` · `app/layouts/AppLayout.tsx:155-170` · `features/muaHang/chungTuMuaHang/components/modal/MuaDichVuModal.tsx:584-604` | route, menu, full-bleed, nút In |
| Super admin | `super-admin-service/…/quan_tri/cau_hinh/**` · `security/internal/controller/MaQuyenAdmin.java` · `security/internal/config/AdminSecurityConfig.java` · `tenant-provisioning/…/core/security/InternalTokenSupport.java` | GĐ2 |

---

## §3. Danh mục nguồn dữ liệu loại chứng từ (BR4/BR9)

Mã dùng trong hệ = `mst_loai_chung_tu.code` **sau `V1032`** (`PT PC GBC PCTG CTNB`…), **không** phải seed
`db/seed/20_loai_chung_tu.sql`. Bảng 47 mã theo BA (`DuLieuKhoiTao_LoaiChungTu.md`). Migration còn thêm
`CTNHD` (V1001), `PTT` (V1011) — hai mã ngoài bảng BA; provider của chúng (nếu có) vẫn khai theo mã DB.

Pilot GĐ1: **`MDV`** (module `chung_tu_mua_hang`, `MaChucNang.MUA_DICH_VU`, base path `/api/mua-hang/chung-tu-mua-dich-vu`).
