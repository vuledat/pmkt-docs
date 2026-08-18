# IMPLEMENT — PMKT-E-07664 Điều chỉnh giá hàng bán (FE)

Nhật ký sinh code của `/gen-fe`. Nguồn: `pmkt-docs/ba/PMKT-E-07664_DieuChinhGiaHangBan` +
Figma section “Điều chỉnh giá hàng bán” (`ymMyg329ejsgCWg28CNmGl`, node `15810-60793`).

---

## 1. Ngày · phạm vi đã code

**2026-08-12.** Chạy `/gen-fe` **không có plan FE** — user chọn “code thẳng từ PYC” (§0.2 của skill),
nên §1 + §2 của `/plan-fe` (đọc bắt buộc + khảo sát reuse có bằng chứng) được làm trước dòng code đầu
tiên và ghi lại ở mục 3 dưới đây.

Phạm vi user chốt: **toàn bộ 4 màn của PYC**.

| Màn (SCR) | Trạng thái |
|---|---|
| `SCR_DanhSachDieuChinhGia` | ✅ đủ — lưới 8 cột, phễu ngày + lọc nâng cao + tìm nhanh, dòng tổng, phân trang/sắp xếp server, panel Xem nhanh 5 tab, nút thao tác theo trạng thái, xóa · ghi sổ · bỏ ghi sổ (đơn + hàng loạt) |
| `SCR_ThemMoiDieuChinhGia` (Bước 1 — chọn nguồn) | ⚠ đủ khung, **chưa có dữ liệu** — endpoint nguồn chưa tồn tại (mục 5) |
| `SCR_ThemMoiDieuChinhGia` (Bước 2 — form) | ✅ đủ — hàng tùy chọn, 2-3 tab động theo ma trận, lưới chi tiết 22 cột, tab Thuế/Hạch toán tính thật, khối tổng |
| `SCR_SuaDieuChinhGia` | ✅ đủ — cùng component, khóa “Số chứng từ” |
| `SCR_XemChiTietDieuChinhGia` | ✅ đủ — cùng component, khóa mọi ô, bộ nút theo trạng thái |

48 file · 9.969 dòng trong `client/src/features/banHang/dieuChinhGiaHangBan/`.

---

## 2. File đã tạo / sửa

### Tạo mới — `client/src/features/banHang/dieuChinhGiaHangBan/`

| File | Vai trò |
|---|---|
| `index.ts` | cửa ra duy nhất của module (file DUY NHẤT ở gốc) |
| `api/model.ts` | hợp đồng Zod của `ENT_DieuChinhGiaHangBan` + chi tiết + hai chứng từ con |
| `api/dieuChinhGiaApi.ts` | base path · `toSearchRequest` · adapter BASE CRUD · ghi sổ / bỏ ghi sổ · cờ `DUNG_MOCK` |
| `api/mock.ts` | **NỢ** — adapter giả, kho rỗng, gỡ khi BE lên |
| `api/queries.ts` | hook react-query theo tenant + hai mutation chuyển trạng thái |
| `api/lookups.ts` | 10 nguồn danh mục cho popup (khách hàng · tài khoản · vật tư · …) |
| `api/nguonApi.ts` | I/O của Bước 1 — lưới nguồn, combo chọn nhanh, nạp dòng của một chứng từ |
| `api/formDetail.ts` | wire → form store; **BR5** nguồn → form |
| `api/payload.ts` | form store → thân request `POST` / `PUT` |
| `constants/constants.ts` | enum wire · khóa tab · giới hạn nhập · số đo Figma |
| `constants/paths.ts` | re-export path từ `_shared` (xem mục 4) |
| `constants/permissions.ts` | 7 mã quyền `DieuChinhGiaHangBan.*` theo `DanhSachQuyen.md` §B4.6 |
| `fields/types.ts` | form store · `NguCanhAnHien` · dòng nguồn |
| `fields/columns.ts` | 8 cột màn danh sách (bề rộng đọc từ Figma) |
| `fields/chiTietColumns.ts` | cột bảng panel Xem nhanh |
| `fields/chiTietFields.ts` | 22 cột lưới chi tiết + cascade BR10/BR15 |
| `fields/nguonFields.ts` | 16 cột lưới popup Bước 1 + cascade BR3 |
| `fields/tabColumns.ts` | cột tab Thuế và tab Hạch toán |
| `fields/status.ts` | registry nhãn + tông màu cho hai cột enum |
| `fields/options.ts` | option enum · thuế suất · nguồn chứng từ |
| `fields/texts.ts` | gói chữ cho component `@base` + bộ lọc nâng cao |
| `helpers/trangThai.ts` | giá trị wire trạng thái + 4 vị từ BR2/BR3 |
| `helpers/tinhToan.ts` | BR2 · BR3 · BR10 · BR15 · thuế · khối tổng |
| `helpers/anHien.ts` | bản code của ma trận ẩn/hiện (chính + phụ) |
| `helpers/hachToan.ts` | bút toán dự kiến 2 nhánh + bảng thuế |
| `helpers/kiemTra.ts` | validate liên trường (bảng Validate dòng 572-586) |
| `helpers/nguon.ts` | BR1 validate chọn nguồn + áp bộ ba BR3 |
| `hooks/useDanhMucDieuChinhGia.ts` | gom danh mục + TK tiền/thuế mặc định |
| `hooks/useDongBoTab.ts` | luật “Đồng bộ nhóm” (dòng 235-250) |
| `i18n/vi.ts` · `en.ts` · `registerDieuChinhGiaI18n.ts` | namespace DUY NHẤT `dieuChinhGia`; `en` khóa theo `vi` bằng kiểu, lệch khóa là lỗi biên dịch |
| `components/DieuChinhGiaTab.tsx` | thân màn danh sách — state, truy vấn, 4 luồng hành động |
| `components/DieuChinhGiaListTable.tsx` | lưới danh sách (trình bày) |
| `components/DieuChinhGiaQuickDetail.tsx` | panel Xem nhanh 5 tab |
| `components/DieuChinhGiaThemMoiModal.tsx` | popup Thêm/Sửa/Xem/Nhân bản (4 chế độ, 1 component) |
| `components/ChonNguonModal.tsx` | popup Bước 1 |
| `components/CongNoTab.tsx` · `ThanhToanTab.tsx` · `HoaDonTab.tsx` | thân ba nhóm tab |
| `components/TongHopPanel.tsx` | khối Tổng cộng |
| `pages/DieuChinhGiaHangBanPage.tsx` + `dieuChinhGiaHangBan.css` | entry lazy + stylesheet của màn |
| `test/*` (5 file, 90 ca) | số học · ma trận · wire · bút toán/validate · render |

### Sửa file có sẵn (2 file, đều là sửa CỘNG THÊM, không đổi hành vi cũ)

| File | Sửa gì |
|---|---|
| `features/banHang/routes.tsx` | thêm 1 route `/ban-hang/dieu-chinh-gia-hang-ban` |
| `features/banHang/_shared/constants/banHangTabs.ts` | thêm 1 mục `dieuChinhHangBan` vào `BAN_HANG_TAB_PATHS` |

`app/router/RootRoutes.tsx` **không phải sửa**: `banHangRoutes` đã được nối tay từ trước.

---

## 3. Khảo sát reuse (thay cho §2 của `/plan-fe`) — đã reuse gì

### Dùng lại nguyên vẹn từ `@base` / `@platform` / `@core`

| Thứ | Dùng ở |
|---|---|
| `CommonListTable` | lưới danh sách · panel Xem nhanh · tab Thuế · tab Hạch toán |
| `CommonEditableGrid` | lưới chi tiết hàng hóa · lưới popup Bước 1 |
| `CommonModalShell` | popup Thêm/Sửa/Xem · popup Chọn nguồn |
| `CommonFilterPanel` · `useListFilter` · `PERIOD_PRESET` | phễu ngày + lọc nâng cao + chip |
| `TabMenu2Level` · `TabMenuChild` | thanh 4 tab nhóm · thanh tab trong popup và panel |
| `CommonActionMenu` · `RowActionButtons` · `Tooltip` | cột Chức năng |
| `CommonConfirmModal` · `useToast` | 3 luồng xác nhận + toast |
| `TotalBreakdown` | khối Tổng cộng (chế độ 2 cột khi ngoại tệ) |
| `CommonSelectBox` · `CommonTextBox` · `CommonTextArea` · `CommonDatePicker` · `CommonCheckbox` · `CommonButton` · `CommonAlert` · `CommonEmpty` · `Card` · `FieldLabel` | toàn bộ ô nhập |
| `createSearchApi` · `createSearchQueries` · `pageResponseSchema` · `http` · `useT` · `useHasPermission` · `useTenant` · `describeApiError` | tầng dữ liệu |
| `formatNumber` (`@core`) | ô tiền của dòng tổng |

**Không component nào phải viết mới ở `@base`, và `@base` không bị sửa.** Mọi `.tsx` trong
`components/` đều mang logic nghiệp vụ riêng của màn (ma trận ẩn/hiện, BR5, BR6, BR8), không phải
component trình bày dùng lại được — nên chúng đúng chỗ ở feature.

### Cố ý KHÔNG dùng

| Thứ | Lý do |
|---|---|
| `@domain-kit/chungTu` (engine chứng từ) | **module tham chiếu `chungTuBanHang` cũng không dùng** — nó tự dựng list bằng `useListFilter` + `createSearchQueries`. Engine đòi một `ChungTuDescriptor` với `basePath`/`maChucNang`/`endpoints` trỏ vào BE **chưa tồn tại**; đi theo mẫu tham chiếu duy nhất của repo là đường ít rủi ro hơn. Chuyển sang engine là việc nên làm CÙNG LÚC với `chungTuBanHang`, không phải riêng màn này |
| `@domain-kit/chungTuNguon` | engine đó phục vụ ô “Chọn chứng từ” trên **thanh tiêu đề** (`HeaderControls` + `defineSource`), còn Bước 1 của epic này là một **popup toàn màn** có tham số lọc riêng, ô tick từng dòng và ba cột nhập BR3 — khác hình dạng, không phải khác cấu hình |
| `@test/renderWithProviders` | luật tầng bịt `features/` khỏi `src/test`; harness dựng tay như `chungTuBanHang.render.test.tsx` |
| `features/muaHang/chungTuMuaHang/dieuChinhGia/` | tên gần giống nhưng là **điều chỉnh giá hàng MUA**, và module đó theo shape phẳng cũ đã đóng băng (`client/CLAUDE.md` §4.2) |

### Viết mới vì không có sẵn

Mọi file trong `helpers/` — đó là nghiệp vụ của riêng epic (BR2 · BR3 · BR5 · BR6 · BR8 · BR10 ·
BR15 · bút toán). `api/lookups.ts` và `hooks/useDongBoTab.ts` dựng lại bộ tối thiểu **local trong
leaf** vì luật tầng cấm hai `leaf` import chéo (cùng cách `chungTuBanHang` và `traLaiHangBan` làm).

---

## 4. Lệch so với tài liệu · quyết định đã chốt

### 4.1 Vị trí màn hình — **user đã chốt**

Figma vẽ màn này là **tab thứ ba** của thanh 4 tab nhóm Bán hàng (breadcrumb “Bán hàng › Điều chỉnh
hàng bán”), tức cùng một màn với `chungTuBanHang`. BA thì tách thành màn riêng có bộ quyền riêng
`DieuChinhGiaHangBan.*`.

→ **Module riêng + route riêng** (user chọn). Page tự vẽ lại thanh 4 tab; bấm tab khác là ĐIỀU HƯỚNG.
Cách này về sau trùng khớp với hai module `traLaiHangBan` / `hoaDonBanHang` đang được dựng song song.

### 4.2 Xung đột nhãn Figma ↔ BA (3 chỗ) — đã xử lý, **cần BA/Design xác nhận lại**

| Chỗ | Figma | BA | Đã chọn | Vì sao |
|---|---|---|---|---|
| Tiêu đề cột | “Loại điều chỉnh” | “Phương thức điều chỉnh” | **BA** | màn này CÒN một trường tên “Loại điều chỉnh” khác hẳn (tab Hóa đơn: Điều chỉnh giá / Sai sót / Khác) — và `6.messages.md` tách hẳn hai thông báo `MSG_102` (“phương thức”) vs `MSG_207` (“loại điều chỉnh trên tab Hóa đơn”). Dùng chung một nhãn là bẫy đọc |
| Giá trị cột | “Điều chỉnh tăng/giảm” | “Tăng/Giảm giá hàng bán” | **cả hai** | chuỗi BA là giá trị WIRE, nhãn Figma là chữ hiển thị (qua registry) |
| Cột “Hình thức thanh toán” | 3 nhãn: Điều chỉnh công nợ · Thu tiền ngay · Chi tiền ngay | 2 giá trị | **cả hai** | nhãn suy từ `thanhToanNgay` + `huongDieuChinhGia` ngay tại cột, không bịa thêm enum ba giá trị |
| Tiêu đề cột tiền | “Tổng tiền thanh toán **(VNĐ)**” | “Tổng tiền thanh toán” | **BA** | đồng tiền hạch toán là cấu hình của từng tenant; in cứng “VNĐ” là nói sai với công ty hạch toán bằng đồng tiền khác. Cột vẫn là số đã quy đổi |
| Cột thứ 3 panel Xem nhanh | “TK tiền” (mẫu: 111) | “TK công nợ” (BR7 → nhóm 131) | **BA** | 111 là tài khoản tiền mặt, không phải tài khoản công nợ — nhãn khung hình mâu thuẫn với chính nghiệp vụ nó minh họa |

### 4.3 Số đo Figma còn thiếu

Lưới popup Bước 1: khung hình chỉ vẽ **12 trong 16 cột** (bảng có thanh cuộn ngang). Sáu cột khớp
chắc chắn lấy số đo thật (44 · 53 · 118 · 127 · 99 · 99); các cột còn lại lấy bề rộng theo loại dữ
liệu. **Cần Design xác nhận.**

---

## 5. Nợ kỹ thuật

### 5.1 `api/mock.ts` — **nợ chính**

cell-app **chưa có module `dieu_chinh_gia_hang_ban`** (`cell/` chỉ có `chung_tu_ban_hang` và
`chung_tu_mua_hang`). Toàn bộ màn chạy trên adapter giả.

Gỡ nợ khi BE lên, đúng 3 bước ghi ở đầu `api/mock.ts`:
1. đối chiếu `api/model.ts` với DTO thật (và `formDetail.ts` · `payload.ts` — ba file này là TOÀN BỘ
   mặt tiếp xúc hợp đồng);
2. đổi `DUNG_MOCK` ở `api/dieuChinhGiaApi.ts` thành `false`;
3. xóa `api/mock.ts` và mọi import tới nó.

Kho của mock **bắt đầu rỗng** (giống `traLaiHangBan/api/mock.ts`): nó cấp LUỒNG (phân trang, lọc,
ghi sổ, xóa) chứ không cấp SỐ LIỆU — một bảng số kế toán bịa trông y hệt số thật nguy hiểm hơn hẳn
một màn trống.

**Hệ quả nhìn thấy được:** popup Bước 1 luôn trả lưới rỗng, và combo “Chọn nhanh chứng từ” luôn rỗng.
BR1/BR2 là phép tính trên lịch sử chứng từ bán hàng + hóa đơn điều chỉnh + chứng từ trả lại của khách
hàng (có quy đổi ĐVT giữa các chứng từ) — không mô phỏng được ở FE mà không bịa ra một “số lượng chưa
trả lại” không dựa trên gì.

### 5.2 Endpoint đã khai sẵn, chờ BE dựng đúng tên

```
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/search
GET    /api/ban-hang/dieu-chinh-gia-hang-ban/cot
GET    /api/ban-hang/dieu-chinh-gia-hang-ban/{id}
POST   /api/ban-hang/dieu-chinh-gia-hang-ban
PUT    /api/ban-hang/dieu-chinh-gia-hang-ban/{id}
DELETE /api/ban-hang/dieu-chinh-gia-hang-ban/{id}
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/{id}/ghi-so
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/{id}/bo-ghi-so
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/nguon/search
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/nguon/chung-tu
POST   /api/ban-hang/dieu-chinh-gia-hang-ban/nguon/chung-tu/{id}/dong
```

7 mã quyền `DieuChinhGiaHangBan.{View, View.Detail, Create, Edit, Delete, Post, Unpost}` cũng chưa
được seed trong `iam_quyen` → hiện mọi `has(...)` trả false với người dùng không phải chủ sở hữu.

### 5.3 Phần chưa dựng (ngoài phạm vi hoặc chờ module khác)

| Phần | Lý do |
|---|---|
| Nút **“Chọn hóa đơn cần điều chỉnh”** trên tab Hóa đơn (dòng 400-407) | tham chiếu chức năng cùng tên của màn **Hóa đơn điều chỉnh** (`PMKT-E-06197`) — một popup tra cứu của module khác. Ô hiện chỉ hiển thị hóa đơn gốc đã chọn + dải mô tả “Điều chỉnh cho hóa đơn Mẫu số… ngày…” |
| Tab **Tham chiếu** trong khối lưới | dùng chung đặc tả `Common/NguonDuLieu/SCR_ThamChieuCT.md`, chưa dựng |
| Tab **Thuế · Hạch toán · Đính kèm · Tham chiếu** của panel Xem nhanh | Figma chỉ vẽ tab đầu; bốn tab kia hiện “đang phát triển” thay vì một bố cục tự nghĩ ra |
| Khối **III. Tính toán & Phân bổ chiết khấu** (dòng 436-438) | tài liệu chỉ ghi “Tham khảo phần chiết khấu của chứng từ bán hàng” — không có đặc tả riêng. Lưới vẫn có đủ cột `Chiết khấu %` · `Tiền chiết khấu` · `Tài khoản CK` và tính đúng BR10; **chưa có** popup Phân bổ chiết khấu và nút “Áp dụng” |
| **BR13** ĐVT khác chuẩn (dòng 487) — hiện thêm trường ĐVT quy đổi | một dòng duy nhất trong tài liệu, không có bảng trường; cần BA đặc tả |
| **BR14** Chiết khấu thương mại (dòng 488-493) | bảng trường của lưới KHÔNG có ô tick “Chiết khấu thương mại”; BR mô tả hành vi cho một ô không tồn tại — cần BA làm rõ |

---

## 6. Điểm chờ BA / Design

Sáu “Điểm cần xác nhận” của ma trận **chưa có trả lời**; dưới đây là cách đã chọn để code chạy được,
kèm chỗ phải sửa nếu BA quyết khác.

| # | Điểm | Đã chọn | Sửa ở đâu nếu khác |
|---|---|---|---|
| 1 | Trục cột ma trận (I1 × I2 = 4 cột, HTTT đưa xuống `(đk-HTTT)`) | theo ma trận | — |
| 2 | `(sl)` Ẩn cột TK doanh thu / TK giảm giá theo loại điều chỉnh | **ẩn cột không dùng** (BR8) — để cả hai thì màn Tăng bắt nhập một TK giảm giá không bao giờ được hạch toán | `helpers/anHien.hienCotTkDoanhThu` / `hienCotTkGiamGia` |
| 3 | Mâu thuẫn “Mã hàng”: Cho phép sửa = Y (dòng 446) vs BR5 “Disable” | **khóa khi có nguồn**, mở khi lập tay | `helpers/anHien.khoaMaHang` |
| 4 | `[CXM]` Tab **Ủy nhiệm chi** không có bảng trường | dùng chung bộ ô của các tab ngân hàng khác | `components/ThanhToanTab.tsx` |
| 5 | Loại tiền là input hay readonly | autofill từ nguồn, **không** cho sửa tay (BR5 dòng 184) | `components/DieuChinhGiaThemMoiModal.tsx` |
| 6 | Quy ước `Disable` = xám read-only | hiện xám read-only | — |

**Ba mâu thuẫn NỘI TẠI của tài liệu phát hiện thêm trong lúc code:**

1. **MSG_105/106 vs BR2/BR3 — mâu thuẫn thật.** Bảng Validate bắt “Số lượng phải lớn hơn 0” và “Đơn
   giá phải lớn hơn 0”, trong khi BR2 (dòng 112-115) và BR3 (dòng 137-139) mô tả dòng **Dịch vụ** có
   `SL = Đơn giá = 0`, `Thành tiền ≠ 0` và khóa hai ô đó ở 0. Áp thẳng bảng Validate thì **không bao
   giờ lưu được chứng từ điều chỉnh giá dịch vụ**. → đã **miễn hai luật cho dòng dịch vụ**
   (`helpers/kiemTra.ts`, có test). Cần BA chốt.
2. **BR5 nhánh Hóa đơn điều chỉnh, mục “Thanh toán ngay”** (dòng 212-216) suy từ *hình thức thanh
   toán trên hóa đơn nguồn*, mà dòng nguồn không mang trường đó. → đặt `thanhToanNgay = false` (mặc
   định của form) thay vì đoán; đoán một giá trị thanh toán là thay người dùng quyết định một bút
   toán tiền (`api/formDetail.toFormValuesTuNguon`).
3. **Số chứng từ ở màn Sửa** — tài liệu ghi “không cho phép sửa” nhưng số chứng từ có mặt trên nhiều
   tab. → khóa ô Số chứng từ của **cả tab Công nợ lẫn tab thanh toán**; ma trận cũng nêu đúng câu hỏi
   này ở “Điểm cần xác nhận” #1 của `SCR_SuaDieuChinhGia_MaTranAnHien.md`.

---

## 7. Cổng nghiệm thu — output thật

Chạy `2026-08-12` tại `client/`. ⚠ Repo có **việc song song đang diễn ra** trong cùng domain
(`traLaiHangBan`, `hoaDonBanHang`, `_shared` — file chưa commit của phiên khác), nên số nền dao động
giữa các lần chạy.

| Lệnh | Kết quả | Của module này |
|---|---|---|
| `npm run typecheck` | **192 lỗi** — 129 `features/danhMuc` · 39 `features/muaHang` · 16 `features/tienMat` · 6 `base/domainKit` · 2 `base/components` | **0** |
| `npm run lint` | **9 lỗi + 2 warning** — toàn bộ ở `base/components/fields/CommonSlider.tsx` và `legacy/**` | **0** |
| `npm run lint:boundaries` | **76 lỗi** — 74 “rule … was not found” + 2 vi phạm thật (`axios` trần trong `legacy`) | **0**, không sinh vi phạm tầng mới |
| `npx vitest run src/features/banHang/dieuChinhGiaHangBan` | **5 file · 90/90 PASS** | ✅ |
| `npm run build` | **ĐỎ** — `tsc -b` dừng ở đúng 192 lỗi trên | **0** |

Đối chiếu baseline `client/CLAUDE.md` §15 (typecheck 194 · lint 10+2 · boundaries 76): **không lệnh
nào tăng số lỗi.**

`npm run build` đỏ là **trạng thái nền của repo**, không phải hồi quy của việc này: `build` chạy
`tsc -b` trên toàn bộ `src/`, mà `features/danhMuc` (nhánh chết) một mình đã 129 lỗi.

**Test của các module khác:** `src/app/layouts/test/AppLayout.test.tsx` (2 ca) và
`src/features/banHang/chungTuBanHang/test/chungTuBanHang.render.test.tsx` (3 ca) đang đỏ. Đã kiểm
CHỦ ĐỘNG bằng cách gỡ route của module này khỏi `routes.tsx` rồi chạy lại: **vẫn đỏ đúng 2 ca ở
Router/AppLayout** → không phải do việc này gây ra (chúng đến từ `menuRegistry.tsx` và
`chungTuBanHang/**` đang được sửa ở phiên song song).

**Cổng cây commit:** chưa commit gì. Khi commit phải `git add` **toàn bộ 48 file mới TRƯỚC**, rồi mới
commit hai file sửa (`routes.tsx`, `_shared/constants/banHangTabs.ts`) — cả hai đều trỏ tới file mới,
và đó đúng là kịch bản “xanh ở local, đỏ ở deploy” mà `client/CLAUDE.md` §15.1 mô tả. Sau đó chạy
`npm run check:committed`.

---

## 8. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| **BR1** Phân trang | `DANH_SACH_PAGE_SIZE = 10` (SCR_DanhSach BR1) · `CHI_TIET_PAGE_SIZE = 20` |
| **BR2** Hiển thị & sắp xếp | `DEFAULT_SORT` = Ngày hạch toán ↓ · Ngày chứng từ ↓ · Số chứng từ ↓ |
| **BR3** Popup | `CommonModalShell` + hộp xác nhận “bỏ thay đổi” khi form bẩn |
| **BR7** Precision & làm tròn | `TIEN_QUY_DOI_PRECISION` cho ô tiền quy đổi (cột Max length `21,6`) |
| **BR8** Khoảng thời gian | phễu ngày `useListFilter({ showTime })`, mặc định “Đầu tháng đến hiện tại” |
| **BR11** Tìm kiếm / lọc / sắp xếp | tìm nhanh + 3 tiêu chí nâng cao + phễu ngày, tất cả server-side; nhớ bộ lọc theo phiên |
| **BR12** Trạng thái chứng từ | `helpers/trangThai.ts` — 5 giá trị của `core.entity.TrangThaiChungTu` |
| **BR13.1** Nút thao tác | con mắt + menu ⋮, lọc theo quyền **và** theo trạng thái dòng |
| **BR13.2** Nút trên form | Hủy · Lưu · Lưu và ghi sổ (Xem: Đóng) |
| **BR14** Chế độ & hành vi form | 4 chế độ `create/clone/edit/view` trên một component |
| **BR15** Validation | `helpers/kiemTra.ts` + `rules` của từng `Form.Item`; BR15.3 so sánh ngày |
| **BR16** Cảnh báo nghiệp vụ | cảnh báo khác tỷ giá (cho đi tiếp) vs chặn khác loại tiền |
| **BR17** Kỳ kế toán | `MSG_203` — **server quyết định**, FE hiển thị nguyên văn lỗi |
| **BR18** Ngoại tệ | `(đk-LT)` — khối cột + khối tổng quy đổi, `quyDoiTien` |
| **BR20** Số chứng từ | ô bắt buộc, khóa ở màn Sửa; kiểm trùng ở server (`MSG_109`) |
| **BR21** Grid chi tiết con | `CommonEditableGrid` — thêm/xóa dòng, dòng tổng, phân trang |
| **BR24** Tooltip / help text | 4 tooltip nguyên văn tài liệu ở tab Hóa đơn |
| **BR25** Phân quyền | 7 mã `DieuChinhGiaHangBan.*`; nút thiếu quyền **ẩn hẳn**, không để bấm rồi 403 |
| **BR26** Toast / notification | `useToast` cho cả 6 thông báo kết quả |
| **BR29** Chính sách xóa | chỉ xóa chứng từ chưa ghi sổ; xác nhận trước; token khóa lạc quan |
| **BR30** Ẩn/hiện cột | `showSettings` + `columnConfigKey` |
| **BR31** Dòng tổng | `summary` server-side trên toàn tập lọc, lùi về tổng trang khi chưa có |
| **BR32** Copy | mặc định của `CommonListTable` |
| **BR33** Màu trạng thái | `fields/status.ts` — xanh “đã xong”, vàng “chưa xong”, xám “huỷ” |
| **BR34** Sửa từ màn xem | popup Xem có nút Chỉnh sửa khi chưa ghi sổ (BR1 của SCR_XemChiTiet) |
| **BR36** Ghi sổ · **BR42** Bỏ ghi sổ | `useGhiSo` / `useBoGhiSo` + xác nhận (bỏ ghi sổ cảnh báo nguyên văn về hóa đơn điều chỉnh bị xóa) |
| **BR37** Ngày hạch toán | validate `Ngày hạch toán ≥ Ngày chứng từ` (`MSG_205`) |
| **BR43** Trim | `laDongCoDuLieu` + `toSearchRequest` coi chuỗi trắng là rỗng |
| **BR44** Truncate text | `textMode` theo từng cột |
| **BR45** Thao tác hàng loạt | Ghi sổ · Bỏ ghi sổ · Xóa, lọc trước theo trạng thái, chạy tuần tự |
| **BR46** Trường hệ thống | `updatedAt` làm token khóa lạc quan trên PUT / DELETE / ghi sổ |

### BR chưa đạt

| BR | Lý do |
|---|---|
| **BR38** Group dữ liệu trên lưới | Figma không vẽ; `CommonListTable` chưa bật nhóm cho màn này |
| **BR39** Xuất Excel | `DanhSachQuyen.md` §B4.6 **không bật** quyền Xuất Excel cho chức năng này |
| **BR19** Kiểm trùng · **BR17** kỳ kế toán | thuộc server (`MSG_109` · `MSG_301` · `MSG_203`); FE hiển thị nguyên văn lỗi trả về |
| **BR5 / BR6 / BR10** Combogrid | các ô chọn dùng `CommonSelectBox` (danh mục nạp sẵn), chưa dùng `CommonComboGrid` nhiều cột — tài liệu ghi “combogrid search” cho một số ô; **cần chốt với BA/Design** có bắt buộc dạng combogrid không |
| **BR22 / BR23 / BR40** Danh mục cây | không thuộc phạm vi màn chứng từ |
| **BR27** Trang hệ thống | thuộc `app/` |
| **BR28** Multi-tenant | do `@platform` lo (mọi query khóa theo `congTyId`/`kyKeToanId`) |
