# PMKT-E-06194 — Chứng từ bán hàng (FE) — Kế hoạch tổng

| | |
|---|---|
| **Trạng thái** | 🟡 Bản nháp chờ review — GHI ĐÈ bản 18/08 (chỉ có `00-doi-chieu-tai-lieu-code.md`) |
| **Ngày sinh** | 2026-08-20 |
| **Người review** | 1 BA · 1 Dev FE · 1 Design — *chưa gán, điền trước khi chuyển sang "Đã duyệt"* |
| **Vì sao chạy lại** | Tài liệu BA đổi ở 2 commit sau bản 18/08: `bb4c10eb9` (19/08 — chuẩn hoá quy tắc ghi sổ/bỏ ghi sổ chứng từ bán/mua/đối trừ, đổi tên trường `TrangThaiChungTu` → `TrangThaiGhiSo`, thêm BR21 mục 5, đổi luật nút Lập hóa đơn/Lập phiếu xuất) và `beaf3662a` (20/08 — sửa mapping `DonHangId` → `DonDatHangId` ở bảng field `ENT_acc_so_cai`, dòng 1188 `SCR_CTBH_ThemMoi.md`) |
| **Code FE hiện có** | `client/src/features/banHang/chungTuBanHang/` — đã merge PR #72, sửa tiếp 18/08 và 20/08 ("fix: ban hang dich vu"). **Module đã chạy** (`app/router/RootRoutes.tsx:219` → `banHangRoutes`) |
| **Tài liệu gốc** | `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/` (toàn bộ cây — usecases, screens, matrix, messages) |
| **Plan BE đi kèm** | [`../PMKT-E-06194-chung-tu-ban-hang-api/00-ke-hoach-tong.md`](../PMKT-E-06194-chung-tu-ban-hang-api/00-ke-hoach-tong.md) |
| **Figma** | [Danh sách](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/Ph%E1%BA%A7n-m%E1%BB%81m-K%E1%BA%BF-to%C3%A1n---Viettel?node-id=58263-112028) · [PBCK](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/...?node-id=21370-356363) · [PBCK theo mặt hàng/hóa đơn](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/...?node-id=46357-87788) — **không có link Figma riêng cho Thêm mới/Xem chi tiết/Xem dữ liệu ghi sổ trong tài liệu**; code hiện tại trỏ node `14770:332806` (xem `components/ChungTuBanHangThemMoiModal.tsx:3`), coi là nguồn UI đã duyệt trước đó |

| UC | Màn hình | Module FE | Domain | API phụ thuộc |
|---|---|---|---|---|
| UC_CTBH_DanhSach | SCR_CTBH_DanhSach | `banHang/chungTuBanHang` | `banHang` | `POST {base}/search`, `/cot`, `/lookup` |
| UC_CTBH_ThemMoi | SCR_CTBH_ThemMoi | `banHang/chungTuBanHang` | `banHang` | `POST {base}` |
| UC_CTBH_ChinhSua | SCR_CTBH_CapNhat | `banHang/chungTuBanHang` | `banHang` | `PUT {base}/{id}` — **chưa dựng ở BE** |
| UC_CTBH_XemChiTiet | SCR_CTBH_XemChiTiet | `banHang/chungTuBanHang` | `banHang` | `GET {base}/{id}` |
| UC_CTBH_GhiSo | (nút trên DanhSach/XemChiTiet) | `banHang/chungTuBanHang` | `banHang` | `{base}/{id}/ghi-so`, `{base}/ghi-so-hang-loat` |
| UC_CTBH_BoGhiSo | (nút trên DanhSach/XemChiTiet) | `banHang/chungTuBanHang` | `banHang` | `{base}/{id}/bo-ghi-so`, `{base}/bo-ghi-so-hang-loat` |
| UC_CTBH_Xoa | SCR_CTBH_PopupXacNhanXoa | `banHang/chungTuBanHang` | `banHang` | `DELETE {base}/{id}`, `{base}/xoa-hang-loat` |
| (con của ThemMoi) | SCR_CTBH_PBCK, SCR_CTBH_PBCK_MHHD | `banHang/chungTuBanHang` | `banHang` | không gọi API riêng — tính tại chỗ trên form |
| (con của ThemMoi/CapNhat/XemChiTiet) | SCR_CTBH_XemDuLieuGhiSo | `banHang/chungTuBanHang` | `banHang` | không có — **CHƯA BUILD**, xem F10 |

`CHUNG_TU_BAN_HANG_BASE` = `/api/ban-hang/chung-tu-ban-hang` (`api/chungTuBanHangApi.ts`).

---

## 0. Quyết định đã chốt

| # | Quyết định | Hệ quả lên code | Vì sao KHÔNG chọn phương án kia |
|---|---|---|---|
| **D1** | **Giữ nguyên field wire `trangThaiChungTu`** (KHÔNG đổi tên thành `trangThaiGhiSo`) cho tới khi BE thực sự đổi cột. | `api/model.ts:223`, `helpers/trangThai.ts`, `fields/columns.ts:100`, `api/chungTuModule.tsx:41-42,109-112` **giữ nguyên**, chỉ thêm 1 dòng comment trỏ về tên mới của BA (`TrangThaiGhiSo`) để người đọc sau không tưởng code sai. | Đã xác minh BE thật (`cell-app/src/main/java/vn/vtt/pmkt/cell/core/entity/TrangThaiChungTu.java`, `BaseChungTuEntity.java`) và plan BE (`docs/doing/PMKT-E-06194-chung-tu-ban-hang-api/00-ke-hoach-tong.md:47,100` — mục D6) **chưa đổi tên cột** `trang_thai_chung_tu`. Đổi tên phía FE theo tài liệu mới trước khi BE đổi ⇒ vỡ contract thật (bộ lọc/sort gửi sai field). Xem **Q1**. |
| **D2** | **Không sửa gì cho điều kiện hiện nút Ghi sổ/Bỏ ghi sổ** ở AC1 (BR21 mục 1–2). | 0 thay đổi — `chungTuModule.tsx:109-112` (`trangThai: { daGhiSo, chuaGhiSo }`) đã khớp đúng luật mới ("Ghi sổ hiện khi Chưa ghi sổ", "Bỏ ghi sổ hiện khi Đã ghi sổ"), do kernel `@domain-kit/chungTu` dựng nút theo đúng 2 giá trị này. | Không có phương án khác — logic hiện tại vốn đã generic theo 2 trạng thái, luật mới **không** đổi điều kiện *hiển thị* nút, chỉ đổi điều kiện *chặn khi bấm* (AC2), việc đó là BE-side (D3). |
| **D3** | **Điều kiện chặn AC2 của Bỏ ghi sổ (chứng từ thu lập riêng đang "Đã ghi sổ" · đang tham gia đối trừ công nợ) là validate phía BE, FE KHÔNG tự kiểm tra trước.** FE chỉ hiển thị message BE trả về (`MSG_PMKT-E-06194_049`, `_052`) qua kênh lỗi chung. | 0 thay đổi — `client/src/platform/http/apiError.ts` đã tước tiền tố `[MSG_*]` và hiển thị **nguyên văn message do BE localize**; không cần thêm khoá `_049`/`_052`/`_108` vào `i18n/vi.ts`/`en.ts` của module. | Nhân đôi validate ở FE (gọi thêm API kiểm tra chứng từ thu/đối trừ trước khi cho bấm nút) tốn 1 round-trip mà không giảm rủi ro — BE vẫn phải validate lại khi transaction thật chạy (race condition). Giữ đúng kiến trúc "server-localized error" đã có sẵn của repo. |
| **D4** | **Sửa nút "Lập hóa đơn" trên danh sách/chi tiết để lọc theo `trangThaiLapHoaDon` ("Chưa lập" · "Đã lập một phần")**, tách khỏi chỗ đang chỉ theo quyền. Thêm mới nút **"Lập phiếu xuất kho"** cùng cơ chế, lọc theo `trangThaiXuatHang` **và** `loaiNghiepVu ≠ Bán dịch vụ`. Cả hai vẫn giữ hành vi "đang phát triển" khi bấm (mở màn đích chưa dựng). | `components/ChungTuBanHangTab.tsx` — thêm điều kiện `visible` vào từng phần tử `rowActionsThem` dựa trên `row.trangThaiLapHoaDon` / `row.trangThaiXuatHang`; thêm hằng `lapPhieuXuat` vào `ROW_ACTION_THEM` + permission `lapPhieuXuat` vào `constants/permissions.ts`. | Không gộp vào kernel: hai nút này NẰM NGOÀI hợp đồng `ChungTuDescriptor` (comment `api/chungTuModule.tsx:20-21` đã nói rõ lý do — phụ thuộc quyền runtime khác + rời sang module khác), phải khai ở tầng feature. |
| **D5** | **Thêm cột "Đơn đặt hàng" (`donDatHangId`) vào lưới Chi tiết hàng hóa**, tái dùng đúng pattern `chon()` đang dùng cho `hopDongId` (`fields/chiTietFields.ts:602`). Vì danh mục Đơn đặt hàng (PMKT-E-14699, thêm 20/08 cùng commit `beaf3662a`) chưa chắc có endpoint lookup, cột này **để cùng trạng thái `CHUA_CO_DANH_MUC` placeholder như `hopDongId`** cho tới khi xác nhận. | `fields/chiTietFields.ts` (thêm 1 dòng `chon('donDatHangId', 'donDatHang', 96, options.donDatHang)`), `fields/types.ts` (`donDatHangId?: string`), `hooks/useDanhMucThemMoi.ts` (thêm khoá `donDatHang` vào object danh mục), `api/formDetail.ts` + `api/payload.ts` (map trường), `i18n/vi.ts`+`en.ts` (nhãn cột). | Không bỏ qua field vì "N — không bắt buộc": bảng field `SCR_CTBH_ThemMoi.md:261` liệt kê tường minh, và commit `beaf3662a` vừa sửa đúng tên field này ở mapping Sổ cái — bỏ qua sẽ lệch dữ liệu tra cứu Sổ cái theo Đơn đặt hàng. Xem **Q2**. |
| **D6** | **Không build lại "PopupXacNhanXoa" thành component riêng** — giữ nguyên cơ chế xác nhận xoá chung của kernel `@domain-kit/chungTu` (generic confirm + error hiển thị theo `apiError.ts`, giống D3). | 0 file mới — chỉ xác nhận bằng test rằng message `MSG_PMKT-E-06194_013`/`_111` hiển thị đúng qua kênh lỗi chung (file con `05-popup-xac-nhan-xoa.md` mô tả case test, không mô tả component mới). | BR03/BR3 của popup này (`docs/be-khung-kien-truc-chuan… §Popup`, business_rules `#br3-popup`) là khung popup xác nhận CHUẨN đã có ở kernel — dựng riêng là viết lại thứ khung đã cho. |
| **D7** | **Đưa popup "Xem dữ liệu ghi sổ" (SCR_CTBH_XemDuLieuGhiSo) vào phạm vi đợt kế hoạch này như một hạng mục MỚI**, dù không phải hệ quả trực tiếp của 2 commit vừa đổi — vì rà lại toàn bộ code phát hiện màn này **hoàn toàn chưa build** (không có nút, không có file). | File con mới `06-popup-xem-du-lieu-ghi-so.md` + hạng mục việc riêng ở §9. | Bỏ qua vì "không phải lý do chạy lại" sẽ để sót một UC đã có đặc tả đầy đủ (155 dòng, đủ Rule + luồng) nhưng 0% code — vi phạm mục đích của `/plan-fe` là bản đồ đầy đủ của epic, không chỉ của phần vừa đổi. |

---

## 1. Phạm vi

**Trong phạm vi đợt kế hoạch này** (review + có thể code theo `/gen-fe` sau khi duyệt):
- Đối chiếu + vá các điểm lệch D1–D7 nêu trên.
- 8 màn/popup: SCR_CTBH_DanhSach · SCR_CTBH_ThemMoi · SCR_CTBH_CapNhat · SCR_CTBH_XemChiTiet · SCR_CTBH_PBCK · SCR_CTBH_PBCK_MHHD · SCR_CTBH_PopupXacNhanXoa · SCR_CTBH_XemDuLieuGhiSo.

**NGOÀI phạm vi** (không code ở đợt này, không đề xuất mở rộng):
- `PUT /{id}` (Chỉnh sửa) — chặn bởi BE, xem plan BE `../PMKT-E-06194-chung-tu-ban-hang-api/`. FE giữ nguyên hành vi "đang phát triển" ở nút Lưu chế độ Sửa.
- 2/6 trường thuế XK quy đổi (`giaTriTinhThueXk`, `giaTriTinhThueXkQuyDoi`) — chặn bởi BE (F4/G13, xem `00-doi-chieu-tai-lieu-code.md` cũ, đã archive nội dung ở §"Cập nhật so với code hiện tại" bên dưới).
- BR16 định khoản ngầm định — hoãn theo quyết định BA (F5/Q2 cũ).
- SCR_CTBH_XemChiTiet, PBCK, PBCK_MHHD — không có thay đổi hành vi từ 2 commit mới, file con của chúng ở đợt này chỉ **xác nhận hiện trạng khớp**, không có việc code mới ngoài D5 (áp dụng chung cho lưới chi tiết dùng ở cả 3 màn).
- Chứng từ bán dịch vụ (PMKT-E-06195) — epic khác, xem `../PMKT-E-06195-chung-tu-ban-dich-vu-fe/`.
- Đơn đặt hàng (PMKT-E-14699) — chỉ thêm **cột liên kết** (D5) trên lưới chứng từ bán, không dựng màn Đơn đặt hàng.

---

## 2. Hiện trạng đã khảo sát

**4 câu hỏi bắt buộc (`docs/fe-khung-kien-truc-chuan.md §4`):**

| # | Câu hỏi | Trả lời | Bằng chứng |
|---|---|---|---|
| 0 | Code ở đâu? | `client/src/features/banHang/chungTuBanHang/` — đã tồn tại, đúng chuẩn §5 (có đủ `index.ts / api / components / constants / fields / helpers / hooks / i18n / pages / test`) | `find client/src/features/banHang/chungTuBanHang -type f` |
| 1 | Màn loại nào? | Chứng từ | dựng trên `@domain-kit/chungTu` (`api/chungTuModule.tsx:24-29`) |
| 2 | Đã có engine chưa? | Có — `defineChungTu` + `createChungTuModule` | `api/chungTuModule.tsx:94-161` |
| 3 | Component đã có ở `@base` chưa? | Đã dùng: `Card`, `CommonCheckbox`, `CommonEditableGrid`, `CommonListTable`, `CommonModalShell`, `CommonSelectBox`, `FieldLabel`, `HeaderControls`, `TabMenuChild`, `useToast` | `grep -n "@base" components/ChungTuBanHangThemMoiModal.tsx:36-51` |
| 4 | Domain đang chạy không? | Có — `banHangRoutes` đã nối vào `RootRoutes.tsx` | `client/src/app/router/RootRoutes.tsx:11,219` |

**API BE:**

| Endpoint | Trạng thái | Bằng chứng |
|---|---|---|
| `POST {base}` (Thêm mới, cả Lưu và Lưu-và-ghi-sổ) | ✅ Đã nối | `components/ChungTuBanHangThemMoiModal.tsx:19` |
| `GET {base}/{id}` (Xem) | ✅ Đã nối | `components/ChungTuBanHangThemMoiModal.tsx:20-21` |
| `PUT {base}/{id}` (Sửa) | ❌ **Chưa dựng ở BE** | `components/ChungTuBanHangThemMoiModal.tsx:24-26` |
| `POST {base}/search`, `/cot`, `/lookup` | ✅ Đã nối qua kernel | `api/chungTuModule.tsx` Nhóm A |
| `{base}/{id}/ghi-so`, `/bo-ghi-so` (+ hàng loạt) | ✅ Đã nối | `api/chungTuModule.tsx:121-134` |
| `DELETE {base}/{id}`, `/xoa-hang-loat` | ✅ Đã nối qua kernel | `api/chungTuModule.tsx` Nhóm A + `bulk.XOA` |
| Danh mục Vụ việc / Hợp đồng | ❌ Chưa có endpoint | `components/ChungTuBanHangThemMoiModal.tsx:30`, `hooks/useDanhMucThemMoi.ts:60,168` (`CHUA_CO_DANH_MUC`) |
| Danh mục Đơn đặt hàng (D5) | ❓ Chưa xác nhận — epic PMKT-E-14699 mới thêm 20/08 | không có mã trong `cell-app/` khảo sát qua grep |

Lệnh đã chạy:
```bash
find client/src/features/banHang/chungTuBanHang -type f | sort
grep -rn "trangThaiChungTu\|trangThaiGhiSo" client/src/features/banHang/chungTuBanHang
grep -rn "donHangId\|donDatHangId" client/src/features/banHang/chungTuBanHang pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang
find cell-app/src/main/java -iname "TrangThaiChungTu.java" -o -iname "BaseChungTuEntity.java"
grep -n "banHang" client/src/app/router/RootRoutes.tsx
```

---

## 3. Kế hoạch reuse

| Cần | Có sẵn ở đâu (`file:dòng`) | Dùng lại hay viết mới | Lý do |
|---|---|---|---|
| Khung danh sách chứng từ (phân trang, lọc, sort, 2 lựa chọn, panel xem nhanh) | `@domain-kit/chungTu` qua `chungTuBanHangModule.Page` | Dùng lại | Đã dựng, không viết lại kernel |
| Máy trạng thái nút Ghi sổ/Bỏ ghi sổ + confirm + toast + invalidate | `@domain-kit/chungTu` (đọc `trangThai` của descriptor) | Dùng lại | Idem D2 |
| Combogrid chọn danh mục theo dòng lưới (mẫu cho `donDatHangId` — D5) | `fields/chiTietFields.ts:602` hàm `chon()` | Dùng lại pattern | Đúng pattern `hopDongId` đã có, chỉ thêm 1 dòng khai báo cột |
| Popup xác nhận xoá chuẩn (BR3) | kernel `@domain-kit/chungTu` (generic confirm dialog) | Dùng lại | D6 |
| Hiển thị lỗi BE đã localize (MSG_*) | `client/src/platform/http/apiError.ts` | Dùng lại | D3 |
| Popup phân bổ chiết khấu (PBCK + PBCK theo mặt hàng/hóa đơn) | `components/PhanBoChietKhauModal.tsx` (231 dòng) + `helpers/chietKhau.ts` | Dùng lại, xác nhận còn khớp | Đã build, không có thay đổi từ 2 commit mới |
| Nút hàng động ngoài kernel (Thu tiền · Lập hóa đơn) | `components/ChungTuBanHangTab.tsx:38-93` (`ROW_ACTION_THEM`, `rowActionsThem`) | Sửa (D4), không viết mới khung | Khung đã có, chỉ thêm điều kiện `visible` + 1 mục "Lập phiếu xuất kho" |
| Popup "Xem dữ liệu ghi sổ" | **Không có** — kiểm `@base`/`@domain-kit` không có sẵn popup lưới bút toán read-only kèm 2 chế độ dữ liệu (xem trước / đã ghi sổ) | Viết mới | Đặc thù nghiệp vụ kế toán, không phải component trình bày thuần |
| Tên danh mục "Đơn đặt hàng" trong `hooks/useDanhMucThemMoi.ts` | `hooks/useDanhMucThemMoi.ts:60,168` (đã có pattern `CHUA_CO_DANH_MUC` cho Vụ việc/Hợp đồng) | Dùng lại pattern | Không viết lại cơ chế placeholder danh mục, chỉ thêm 1 khoá |

---

## 4. Kiến trúc module — cây thư mục

Module đã tồn tại đúng chuẩn §5; đợt này **không đổi cấu trúc**, chỉ thêm/sửa file bên trong (danh sách đủ ở §7 mỗi file con). Không tạo thư mục mới.

```
features/banHang/chungTuBanHang/
├── index.ts
├── api/            # + D5: formDetail.ts, payload.ts (map donDatHangId)
├── components/     # + D4: ChungTuBanHangTab.tsx (điều kiện nút) · modal/ (D7: popup mới)
├── constants/      # + D4: permissions.ts (mã quyền lapPhieuXuat, nếu BE cấp)
├── fields/         # + D5: chiTietFields.ts, types.ts
├── helpers/        # không đổi (D2/D3 không cần logic mới)
├── hooks/          # + D5: useDanhMucThemMoi.ts (khoá donDatHang)
├── i18n/           # + D4, D5, D7: khoá mới, KHÔNG thêm khoá MSG_* (D3)
├── pages/          # không đổi
└── test/           # + case cho D4, D5, D7 (xem từng file con §10)
```

Popup mới (D7) đặt ở `components/modal/` theo Luật cứng 4 (`client/CLAUDE.md §5`) — **đây là popup đầu tiên của module cần thư mục `modal/`**, vì `PhanBoChietKhauModal.tsx` và `ChungTuBanHangThemMoiModal.tsx` hiện đang phẳng ngay dưới `components/` (nợ cũ trước chuẩn hoá 2026-08-11, KHÔNG di dời trong đợt này vì ngoài phạm vi việc đang làm — xem "Khi gặp code cũ vi phạm quy tắc" ở `CLAUDE.md` gốc). Popup mới (`XemDuLieuGhiSoModal.tsx`) tạo trong `components/modal/` theo đúng chuẩn hiện hành; không kéo theo dọn 2 file cũ.

---

## 5. Checklist artefact

| Artefact | Trạng thái |
|---|---|
| `index.ts` (1 file duy nhất ở gốc) | ✅ Có |
| `api/` (Zod + I/O) | ✅ Có, cần thêm map `donDatHangId` (D5) |
| `components/` | ✅ Có, cần sửa `ChungTuBanHangTab.tsx` (D4) + thêm `modal/XemDuLieuGhiSoModal.tsx` (D7) |
| `constants/constants.ts · paths.ts · permissions.ts` | ✅ Có, cần thêm mã quyền (D4, chờ Q3) |
| `fields/` (+ `types.ts`) | ✅ Có, cần thêm cột `donDatHangId` (D5) |
| `helpers/` | ✅ Có, không đổi |
| `hooks/` | ✅ Có, cần thêm khoá danh mục (D5) |
| `i18n/vi.ts · en.ts · registerChungTuBanHangI18n.ts` | ✅ Có (1 namespace `banHang`), cần thêm khoá cho D4/D5/D7 |
| `pages/` | ✅ Có, không đổi |
| `test/` | ✅ Có 8 file, cần thêm case D4/D5/D7 |

---

## 6. Route & quyền

Không đổi route — `client/src/features/banHang/routes.tsx` + `RootRoutes.tsx:219` đã nối. Mã quyền hiện có ở `constants/permissions.ts:36-48` (`BAN_HANG_CHUNG_TU_PERM`).

**D4 cần thêm** (chờ xác nhận BE có cấp mã quyền riêng cho "Lập phiếu xuất kho" hay tái dùng mã có sẵn — **Q3**):
```ts
// constants/permissions.ts — dự kiến, CHƯA xác nhận với BE
lapPhieuXuat: 'PhieuXuatKho.Create', // hoặc mã khác — Q3
```

---

## 7. Bản đồ màn ↔ file con ↔ SCR ↔ UC ↔ Matrix

| File con | SCR | UC | Matrix |
|---|---|---|---|
| `01-danh-sach.md` | SCR_CTBH_DanhSach | UC_CTBH_DanhSach, UC_CTBH_GhiSo, UC_CTBH_BoGhiSo | — (không có file Matrix riêng cho DanhSach; BR04 của SCR đóng vai trò ma trận) |
| `02-them-moi-va-chinh-sua.md` | SCR_CTBH_ThemMoi, SCR_CTBH_CapNhat | UC_CTBH_ThemMoi, UC_CTBH_ChinhSua | SCR_CTBH_ThemMoi_MaTranAnHien.md, SCR_CTBH_CapNhat_MaTranAnHien.md |
| `03-xem-chi-tiet.md` | SCR_CTBH_XemChiTiet | UC_CTBH_XemChiTiet | SCR_CTBH_XemChiTiet_MaTranAnHien.md |
| `04-popup-phan-bo-chiet-khau.md` | SCR_CTBH_PBCK, SCR_CTBH_PBCK_MHHD | (con của UC_CTBH_ThemMoi/ChinhSua) | SCR_CTBH_PBCK_MaTranAnHien.md, SCR_CTBH_PBCK_MHHD_MaTranAnHien.md |
| `05-popup-xac-nhan-xoa.md` | SCR_CTBH_PopupXacNhanXoa | UC_CTBH_Xoa | — (không có file Matrix riêng, BR03/BR04 của SCR là ma trận) |
| `06-popup-xem-du-lieu-ghi-so.md` | SCR_CTBH_XemDuLieuGhiSo | (con của ThemMoi/CapNhat/XemChiTiet) | — (không có file Matrix riêng) |
| `07-hop-dong-api-va-i18n.md` | (cắt ngang tất cả) | — | — |

Mọi `SCR_*.md` của epic xuất hiện đúng 1 lần ở trên.

---

## 8. i18n

**Một namespace duy nhất**: `banHang` (`i18n/registerChungTuBanHangI18n.ts`). Nhánh khoá theo màn đã có: `list.*`, `themMoi.*`, `quickDetail.*`, `rowAction.*`. Đợt này thêm:

| Nhánh mới | Dùng cho |
|---|---|
| `list.rowAction.lapPhieuXuat` | D4 — nhãn nút "Lập phiếu xuất" |
| `themMoi.grid.donDatHang` | D5 — nhãn cột "Đơn đặt hàng" |
| `themMoi.footer.xemDuLieuGhiSo` | D7 — nhãn nút "Xem dữ liệu ghi sổ" |
| `xemDuLieuGhiSo.*` | D7 — toàn bộ nhãn của popup mới (tiêu đề, tên cột lưới, "Không có dữ liệu", nút Đóng) |

**Không thêm khoá cho `MSG_PMKT-E-06194_*`** — theo D3, message hiển thị nguyên văn từ BE qua `apiError.ts`.

---

## 9. Thứ tự thực hiện

1. **Q1 chốt trước** (naming `trangThaiChungTu`/`TrangThaiGhiSo`) — nếu BE quyết định đổi tên cột thật, D1 phải làm lại trước khi code các bước sau, tránh sửa 2 lần cùng chỗ.
2. D4 (nút Lập hóa đơn/Lập phiếu xuất) — độc lập, không phụ thuộc API mới, làm trước để có bằng chứng review.
3. D5 (cột Đơn đặt hàng) — cần **Q2** (danh mục Đơn đặt hàng có endpoint chưa) trả lời trước, nếu chưa có thì làm ở dạng placeholder giống Hợp đồng.
4. D7 (popup Xem dữ liệu ghi sổ) — độc lập, không phụ thuộc API mới (tính tại chỗ theo chế độ Xem trước — xem `06-popup-xem-du-lieu-ghi-so.md` §8); việc lớn nhất của đợt này, làm sau khi D4/D5 xong.
5. D6 (xác nhận PopupXacNhanXoa) — chỉ thêm test, làm cuối.

---

## 10. Rủi ro

| # | Rủi ro | Giảm thiểu |
|---|---|---|
| **R1** | BE đổi tên cột `trangThaiChungTu` → `trangThaiGhiSo` sau khi FE đã code xong D4/D5/D7 mà không báo | Hỏi thẳng BE ở Q1 trước khi bắt đầu; nếu BE xác nhận sẽ đổi, đợi commit BE trước khi bắt tay code (thứ tự ở §9 mục 1) |
| **R2** | Popup "Xem dữ liệu ghi sổ" (D7) tính bút toán tại chỗ theo cùng thuật toán BR20 (Ghi sổ) — nếu BE sửa BR20 mà FE không đồng bộ, chế độ "Xem trước" sẽ sai lệch với chế độ "Dữ liệu sổ" thật | Giữ logic tính bút toán Xem trước tối giản — CHỈ dùng cho các trường đã có sẵn giá trị trên form (không tính lại thuế/chiết khấu, tái dùng kết quả `helpers/hachToan.ts` đã tính cho `TongHopPanel`, không viết công thức riêng) |
| **R3** | Nút "Lập phiếu xuất kho" (D4) mở màn đích chưa dựng — vẫn phải hiện nút đúng điều kiện `trangThaiXuatHang`, dễ để sót test trạng thái "Đã xuất đủ" phải ẩn | Test `test/anHienVaDongBo.test.ts` thêm case cho `hienNutLapPhieuXuat` tương tự cách đã test `loaiNghiepVuHopLe` (đột biến: gỡ điều kiện → test đỏ) |
| **R4** | Đơn đặt hàng (D5) chưa có danh mục lookup — nếu để trống hoàn toàn, mapping Sổ cái (`DonDatHangId`) không có gì để kiểm tra hết-đến-cuối | Ghi rõ trong test D5 rằng payload gửi `donDatHangId: null` khi chưa chọn — không throw, không chặn Lưu |

---

## 11. Conflict Figma ↔ Matrix

Không phát hiện — tài liệu Matrix `SCR_CTBH_ThemMoi_MaTranAnHien.md` tự nhận là "derived view" từ SCR, không có Figma riêng cho từng ô ẩn/hiện để đối chiếu (xem "Điểm cần xác nhận" trong chính file Matrix — đã là câu hỏi treo tới BA, không phải conflict Figma↔Matrix). Không có việc mới của đợt này chạm vào vùng đó.

---

## 12. ⚠️ Điểm cần BA / Design xác nhận

| # | Câu hỏi | Bằng chứng hai phía |
|---|---|---|
| **Q1** | BA đã đổi tên trường `TrangThaiChungTu` → `TrangThaiGhiSo` trong tài liệu (`bb4c10eb9`, "Chuan hoa ten truong... theo LDM BanHang-Update"). BE có kế hoạch đổi tên cột thật (`trang_thai_chung_tu` → `trang_thai_ghi_so`) theo LDM mới không, và khi nào? | BA doc: `SCR_CTBH_ThemMoi.md:1375` `sal_chung_tu_ban.TrangThaiGhiSo`. Code thật: `cell-app/.../core/entity/TrangThaiChungTu.java`, `BaseChungTuEntity.java`, `client/.../api/model.ts:223` đều còn `trangThaiChungTu`/`trang_thai_chung_tu` |
| **Q2** | Danh mục "Đơn đặt hàng" (PMKT-E-14699) đã có endpoint lookup ở `cell-app` chưa? Nếu chưa, mốc dự kiến? | BA doc: `SCR_CTBH_ThemMoi.md:261` yêu cầu combogrid `DonDatHangId`. Code: không tìm thấy endpoint nào trong `cell-app/` khi grep `DonDatHang` |
| **Q3** | Nút "Lập phiếu xuất kho" trên `SCR_CTBH_DanhSach` cần mã quyền riêng hay tái dùng mã có sẵn của module Phiếu xuất kho (PMKT-E-03646)? Hiện `constants/permissions.ts` chưa có mã nào cho hành động này. | BA doc: `SCR_CTBH_DanhSach.md:67` chỉ ghi "có quyền lập phiếu xuất", không nêu mã cụ thể |
| **Q4** *(kế thừa từ bản 18/08, chưa đóng)* | Bảng "TK giá vốn / TK kho" và "Số lô / Hạn sử dụng" có nên gắn `(đk-PXK)` như 3 trường giá vốn liền trên không? | `SCR_CTBH_ThemMoi_MaTranAnHien.md` mục "Điểm cần xác nhận" #2 |
| **Q5** *(kế thừa)* | "Tỷ lệ/Tiền CK theo mặt hàng · theo hóa đơn" — read-only hay cho nhập tay? Mâu thuẫn bảng field (`Cho phép sửa = N`) và BR12.d (mô tả nhập tay). | `SCR_CTBH_ThemMoi_MaTranAnHien.md` mục "Điểm cần xác nhận" #3 |
| **Q6** *(kế thừa)* | Nút "Lập phiếu xuất kho" có thật sự hiển thị trên màn Xem chi tiết không? Bảng "Chức năng" của `SCR_CTBH_XemChiTiet.md` không liệt kê, nhưng BR23 của `SCR_CTBH_ThemMoi.md` nói có. | `SCR_CTBH_XemChiTiet_MaTranAnHien.md` mục "Điểm cần xác nhận" #2 |

---

## 13. Kiểm thử + cổng nghiệm thu

Cổng nhẹ (mặc định khi đang code, theo `client/CLAUDE.md §15`):
```bash
npx vitest run src/features/banHang/chungTuBanHang --reporter=dot
npx vite build
npm run check:committed   # chỉ khi có commit
```
Bốn lệnh nặng (`typecheck` / `lint` / `lint:boundaries` / full suite) **không chạy mặc định** — chỉ chạy khi đụng `src/base/index.ts`/barrel (thêm cột dùng component `@base` có sẵn thì không cần) hoặc khi user yêu cầu, theo bảng ở `client/CLAUDE.md §15.0`.

Từng file con liệt kê case cụ thể ở mục "Kiểm thử" riêng.

---

## 14. BR đã áp dụng

`BR21` (mục 1, 2, 4, 5 — Ghi sổ/Bỏ ghi sổ, đối tượng chặn) · `BR22` (4 trạng thái dẫn xuất, đặc biệt Lập hóa đơn/Xuất hàng theo counter) · `BR23` (điều kiện hiện nút Lập hóa đơn/Lập phiếu xuất) · `BR24` (phạm vi Loại nghiệp vụ — không đổi từ bản 18/08) · `BR6 chung` (combogrid Đơn đặt hàng) · `BR03/BR3 popup` (khung xác nhận xoá chuẩn) · `BR20` (nguồn dữ liệu Xem dữ liệu ghi sổ) · `BR45` (thao tác hàng loạt, không đổi).

**BR chưa đạt** (kế thừa từ bản 18/08, không đổi vì ngoài phạm vi 2 commit): `BR14` 2/6 trường thuế XK quy đổi (chặn BE) · `BR16` định khoản ngầm định (hoãn theo BA).

---

## 15. Tài liệu tham chiếu

- `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/` (toàn bộ)
- `docs/doing/PMKT-E-06194-chung-tu-ban-hang-api/00-ke-hoach-tong.md`
- `docs/fe-khung-kien-truc-chuan.md`, `client/CLAUDE.md`
- `pmkt-docs/ba/Common/business_rules.md`
- Commit BA: `bb4c10eb9`, `beaf3662a` (repo `pmkt-docs`)

---

## Cập nhật so với code hiện tại

Đối chiếu toàn bộ code FE (`client/src/features/banHang/chungTuBanHang/`) với tài liệu BA **mới nhất** (sau 2 commit `bb4c10eb9` + `beaf3662a`). Giữ nguyên đánh số **F1–F5** từ bản đối chiếu 18/08 (không đổi, vì không liên quan tới 2 commit này), thêm **F6–F13** phát hiện ở lượt rà này.

| # | Điểm lệch | Bằng chứng `file:dòng` | Trạng thái / hành động |
|---|---|---|---|
| **F1** | Combo `Loại nghiệp vụ` lọc đúng BR24 | `helpers/anHien.ts:169-171` (`loaiNghiepVuHopLe`) | ✅ Đã sửa 18/08 — không đổi bởi 2 commit mới |
| **F2** | Tab Thuế ẩn khi xuất khẩu | `helpers/anHien.ts` (deps `xuatKhau`) | ✅ Đã sửa 18/08 — không đổi |
| **F3** | Mặc định combo `Loại nghiệp vụ` = Trong nước | `helpers/anHien.ts:180-183` (`loaiNghiepVuMacDinh`) | ✅ Đã sửa 18/08 — không đổi |
| **F4** | Thiếu 2/6 trường BR14 quy đổi thuế XK | `fields/chiTietFields.ts` khối thuế XK | ❌ Chặn bởi BE (G13 bên plan BE) — không đổi |
| **F5** | BR16 định khoản ngầm định chưa có | `fields/chiTietFields.ts:218-221` | ⏸ Hoãn theo BA (Q2 cũ) — không đổi |
| **F6** | Field `TrangThaiGhiSo` (tên mới của BA từ `bb4c10eb9`) — FE vẫn dùng `trangThaiChungTu`, **khớp đúng BE hiện tại** (chưa đổi tên cột) nên KHÔNG phải bug, nhưng lệch thuật ngữ với BA doc mới nhất | `api/model.ts:223`, `helpers/trangThai.ts:9,28-30`, `fields/columns.ts:100`; BA: `SCR_CTBH_ThemMoi.md:1375` | ⏸ **Chờ Q1** — giữ nguyên (D1) cho tới khi BE xác nhận đổi cột |
| **F7** | Nút "Lập hóa đơn" hiện theo quyền, **không lọc theo `trangThaiLapHoaDon`** như BR04/BR1 mới yêu cầu ("chỉ hiện khi Chưa lập/Đã lập một phần") | `components/ChungTuBanHangTab.tsx:85-90` (`visible: canLapHoaDon`, không có điều kiện trạng thái) | ❌ **Gap thật — D4 sẽ sửa** |
| **F8** | Nút "Lập phiếu xuất kho" **hoàn toàn chưa có** trên danh sách/chi tiết | Không tìm thấy `lapPhieuXuat` trong `constants/permissions.ts` hay `ROW_ACTION_THEM` (`components/ChungTuBanHangTab.tsx:39-42`); BA: `SCR_CTBH_DanhSach.md:67`, `SCR_CTBH_XemChiTiet.md:28` | ❌ **Gap thật — D4 sẽ thêm mới** |
| **F9** | Cột "Số hóa đơn" **thiếu** trên danh sách (BE chưa join sang `sal_hoa_don_ban_hang`) | `fields/columns.ts:10-14` (comment tự nhận gap) | ❌ Chặn bởi BE — không đổi, ghi lại vào file con 01 để không lặp lại phát hiện |
| **F10** | Cột "Đơn đặt hàng" (`donDatHangId`) **hoàn toàn chưa có** trên lưới chi tiết | `fields/chiTietFields.ts` không có dòng nào chứa `donDatHang` (chỉ có `hopDongId` ở dòng 602); BA: `SCR_CTBH_ThemMoi.md:261`, mapping Sổ cái `SCR_CTBH_ThemMoi.md:1188` (vừa sửa bởi `beaf3662a`) | ❌ **Gap thật — D5 sẽ thêm mới** |
| **F11** | Popup "Xem dữ liệu ghi sổ" (SCR_CTBH_XemDuLieuGhiSo) **hoàn toàn chưa build** | Footer modal chỉ có "Hủy · Lưu · Lưu và ghi sổ" (`components/ChungTuBanHangThemMoiModal.tsx:17`); không có file nào chứa `XemDuLieuGhiSo` trong module | ❌ **Gap thật — D7 sẽ thêm mới** |
| **F12** | `PUT /{id}` (Sửa) chưa nối BE — nút Lưu ở chế độ Sửa báo "đang phát triển" | `components/ChungTuBanHangThemMoiModal.tsx:23-26` | ⏸ Chặn bởi BE (đã ghi nhận trong code, không phải phát hiện mới) — nêu lại vì liên quan trực tiếp BR21 mục 1 (nút "Lưu" ở Chỉnh sửa) |
| **F13** | Comment cũ ở `api/chungTuModule.tsx:105-112` mô tả "vòng đời 5 trạng thái... NHAP/CHO_DUYET/DA_DUYET/HUY" — mâu thuẫn với `helpers/trangThai.ts:28-30` ("đúng HAI giá trị") và với BE plan D6 (đã chốt 2 giá trị từ 16/08) | `api/chungTuModule.tsx:105-112` | ⚠️ Comment lỗi thời, không ảnh hưởng hành vi (code chỉ dùng `TRANG_THAI_CHUA_GHI_SO = [CHUA_GHI_SO]`) — dọn khi có việc khác chạm đúng file này (không mở diff riêng chỉ để sửa comment) |

**Đọc bảng này thế nào:** F1–F3 đã đóng, không việc gì thêm. F4–F5, F9, F12 bị chặn bởi bên khác (BE/BA), không phải việc FE có thể tự làm ở đợt này. F6 chờ quyết định BE (Q1). **F7, F8, F10, F11 là 4 việc code thật của đợt này**, tương ứng D4, D4, D5, D7. F13 là dọn rác nhỏ, làm tiện tay khi chạm `chungTuModule.tsx` cho D2 (dù D2 không cần sửa gì, nếu file được mở ra vì lý do khác thì tiện thể sửa comment).
