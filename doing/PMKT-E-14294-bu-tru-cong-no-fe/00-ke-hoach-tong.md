# Kế hoạch FE — PMKT-E-14294 Bù trừ công nợ

| | |
|---|---|
| **Trạng thái** | 🟡 BẢN NHÁP — chờ review, **chưa code một dòng nào** |
| **Ngày lập** | 2026-08-11 |
| **Người review** | 1 BA (chủ epic PMKT-E-14294) · 1 Dev FE · 1 Design (chủ file Figma) |
| **Nguồn BA** | `pmkt-docs/ba/PMKT-E-14294_BuTruCongNo/` |
| **Figma** | [Section "Bù trừ công nợ" — node 41322:649030](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/Ph%E1%BA%A7n-m%E1%BB%81m-K%E1%BA%BF-to%C3%A1n---Viettel?node-id=41322-649030) |
| **Module FE** | `client/src/features/tongHop/buTruCongNo/` |
| **Domain** | `tongHop` (đã có route contribution — `client/src/features/tongHop/routes.tsx`) |
| **i18n namespace** | `buTruCongNo` (MỘT namespace cho cả module) |
| **API phụ thuộc** | ❌ **chưa có gì ở BE** — `cell-app/src/main/java/vn/dopai/pmkt/cell/` không có module `bu_tru_cong_no` lẫn `phieu_ke_toan_tong_hop` (xem §2) |

## Bản đồ UC · màn hình · file con

| UC | Màn (SCR) | Figma node | File kế hoạch | Ghi chú phạm vi |
|---|---|---|---|---|
| PMKT-U-14688 — Xem danh sách | `SCR_BTCN_DanhSach` | `41322:651294` "Danh sách" | [01-danh-sach-chung-tu-bu-tru.md](01-danh-sach-chung-tu-bu-tru.md) | **NGOÀI phạm vi build** — màn nền thuộc epic PMKT-E-09980; file này chỉ chốt hợp đồng tích hợp |
| PMKT-U-14690 — Thêm mới (bước 1) | `SCR_BTCN_BuTru` | `41323:656771` (VND) · `41383:670216` (ngoại tệ) | [02-popup-bu-tru-cong-no.md](02-popup-bu-tru-cong-no.md) | Trong phạm vi |
| PMKT-U-14690 — Thêm mới (bước 2) | `SCR_BTCN_ChungTu_ThemMoi` | `41383:666955` (VND) · `41667:46774` (ngoại tệ) · `41383:672221` / `41697:102387` (tab Chứng từ công nợ) | [03-popup-chung-tu-bu-tru-them-moi.md](03-popup-chung-tu-bu-tru-them-moi.md) | Trong phạm vi |
| PMKT-U-14691 — Xem chi tiết<br>PMKT-U-14693 — Ghi sổ / Bỏ ghi | `SCR_BTCN_ChungTu_XemChiTiet` | **KHÔNG có frame riêng** (xem Q6) | [04-popup-chung-tu-bu-tru-xem-chi-tiet.md](04-popup-chung-tu-bu-tru-xem-chi-tiet.md) | Trong phạm vi (chế độ `view` của cùng popup) |
| PMKT-U-14692 — Xóa | `SCR_BTCN_PopupXacNhanXoa` | Không có Figma (BA ghi rõ) | [05-popup-xac-nhan-xoa.md](05-popup-xac-nhan-xoa.md) | Trong phạm vi |
| — | — | — | [06-hop-dong-api-va-i18n.md](06-hop-dong-api-va-i18n.md) | Hợp đồng Zod với BE + bảng khoá i18n vi/en |

---

## 0. Quyết định đã chốt

### D1 — Một module phẳng `features/tongHop/buTruCongNo/`, mọi popup là component

Toàn bộ nghiệp vụ (popup thiết lập bù trừ → popup chứng từ → popup xác nhận xóa) là **MỘT module**;
ba popup nằm ở `components/`, dùng chung `fields/types.ts`, `constants/`, `api/`, `helpers/`, i18n.

**Hệ quả lên code:** không tạo `themMoi/` · `xemChiTiet/` · `danhSach/`; không tạo `_shared/`
(domain `tongHop` hiện mới có 1 module thật là `khoaSo`, luật `_shared` cần **≥2 module thật cùng cần
dùng chung** — `client/CLAUDE.md:250-252`). Gốc module chỉ có `index.ts`.

**Không chọn phương án tách 3 module** (`buTruThietLap/`, `buTruChungTu/`, …) vì đó đúng là shape
"tách theo hành vi" đã bị gỡ ngày 2026-08-11 và bị cấm mở mới (`client/CLAUDE.md:187-195`;
`docs/fe-khung-kien-truc-chuan.md:326`).

### D2 — Đặt module ở domain `tongHop`, KHÔNG ở `banHang`/`muaHang`

Chứng từ kết quả là **Phiếu kế toán tổng hợp** (`LoaiPhieu = 5. Bù trừ công nợ` —
`3.crud-matrix.md:24`), Figma dựng nó trong nhánh `Tổng hợp → Phiếu kế toán tổng hợp`
(breadcrumb + tab bar của frame `41322:651294`), và danh sách của nó là danh sách Phiếu KTTH.

**Hệ quả lên code:** route đóng góp qua `client/src/features/tongHop/routes.tsx` (file đã tồn tại,
hiện chỉ có 1 route `khoaSo`); hằng số đường dẫn của module này đặt tên `BU_TRU_CONG_NO_PATHS`
(**không** tái dùng `TONG_HOP_PATHS` đang nằm trong `khoaSo/constants/paths.ts:9-11` — một module
không được với sang leaf anh em, `client/CLAUDE.md:108-109`).

**Không chọn `features/banHang/`** dù menu truy cập nằm ở Bán hàng/Mua hàng: menu chỉ là **đường vào**,
còn dữ liệu, quyền (`PhieuKeToan.*`) và màn danh sách đều thuộc Tổng hợp. Đặt ở `banHang` sẽ buộc
`muaHang` import ngang sang leaf anh em — lint tầng chặn.

### D3 — KHÔNG dựng danh sách Chứng từ bù trừ trong epic này

`SCR_BTCN_DanhSach.md:5` nói rõ: *"không xây màn hình danh sách độc lập"*, mọi bố cục lấy theo
`SCR_PhieuKTTH_DanhSach.md` của epic PMKT-E-09980. Repo **chưa có** module Phiếu KTTH
(grep `phieuKeToan|phieuKTTH|keToanTongHop` trong `client/src` — 0 kết quả ngoài legacy, xem §2).

**Hệ quả lên code:** module này export ra `index.ts` **popup chứng từ + hook hành động** để module
Phiếu KTTH (khi dựng) cắm vào; bản thân nó chỉ tự chủ **luồng tạo mới** qua route riêng. Nợ tích hợp
được ghi thành R1 + Q1.

### D4 — Dùng `@base` trực tiếp, chỉ mượn **kernel** của `@domain-kit/chungTu`

Engine `@domain-kit/chungTu` là engine **màn danh sách** (`ChungTuListPage`, `useChungTuList`,
`ChungTuDescriptor` — `client/src/base/domainKit/chungTu/index.ts:75-92`). Epic này không dựng danh
sách (D3) nên **không** khai descriptor.

Nhưng phần **kernel** thì dùng lại nguyên vẹn, không viết lại:

| Mượn gì | Ở đâu |
|---|---|
| `TRANG_THAI_GHI_SO`, `docTrangThai`, `BanDoTrangThai` | `base/domainKit/chungTu/index.ts:12-31` |
| `tinhTrangThaiHanhDong`, `LY_DO_DISABLE`, `LuatModule` (máy trạng thái nút Ghi sổ/Bỏ ghi/Xóa) | `base/domainKit/chungTu/index.ts:37-49` |
| `MA_LOI_KERNEL`, `moTaLoiChungTu` (7 mã lỗi kernel) | `base/domainKit/chungTu/index.ts:52-54` |

**Không chọn "viết máy trạng thái nút riêng"**: BR12/BR13/BR42 đúng là thứ kernel đã mã hoá, tự viết
lại là nhân bản luật.

### D5 — Hai bảng chứng từ dùng CHUNG một component, phân biệt bằng prop `ben`

Bảng "Chứng từ phải thu" và "Chứng từ phải trả" khác nhau đúng **hai** điểm: tên cột
(`Số chưa thu` ↔ `Số còn nợ`) và luật auto-fill khi tick (`= Số chưa thu` ↔ `= MIN(...)` theo BR02).
Mọi thứ còn lại (15 cột, dòng Tổng, ô tìm kiếm, nút Reload, phân trang, giữ tick qua trang) trùng nhau.

**Hệ quả lên code:** `components/ChungTuBuTruTable.tsx` nhận `ben: 'phaiThu' | 'phaiTra'`;
`fields/buTruColumns.ts` xuất một hàm `buTruColumns(ben, ctx)`.

### D6 — Hai bảng nạp **toàn bộ** tập kết quả một lần, phân trang phía client

BR02 bắt duyệt phân bổ *"trên toàn bộ danh sách đã nạp (từ trên xuống, **không giới hạn trong trang
hiện tại**)"* (`SCR_BTCN_BuTru.md:123`), và `SCR_BTCN_BuTru.md:46,77` bắt *"trạng thái tick và Số tiền
bù trừ … giữ nguyên khi chuyển trang hoặc tìm kiếm"*. Hai yêu cầu này **không** thoả được với phân
trang server-side nếu BE không cấp endpoint phân bổ.

**Hệ quả lên code:** `POST …/lay-du-lieu` trả **đủ** 2 danh sách; `CommonListTable` chạy
`pagination` client-side + `summaryScope: 'all'` (`CommonListTable.tsx:538-543` — tổng tính trên
**toàn bộ** tập, không phải trang hiện tại) + `preserveSelectedRowKeys` (`CommonListTable.tsx:523`).
Ô tìm kiếm dùng quick-search sẵn có của bảng (`showSearch` + `onSearch`, `CommonListTable.tsx:389,399`).

**Rủi ro khối lượng** → R3. **Cần BA chốt trần số dòng** → Q4.

### D7 — Cột "Số tiền bù trừ" là ô nhập trong `CommonListTable`, KHÔNG dùng `CommonEditableGrid`

`CommonEditableGrid` (`base/index.ts:541`) là lưới **thêm/xóa dòng** trên `Form.List` — hai bảng ở
đây không thêm/xóa dòng, chỉ có 1 cột số nhập được + 1 cột checkbox.

**Hệ quả lên code:** cột `soTienBuTru` khai `format: (value, record) => <CommonNumberInput …/>`
(`ListField.format` nhận hàm render — `base/components/table/listTableFormat.ts:56`), checkbox dùng
cột chọn dòng sẵn có của bảng (`selectable` — `CommonListTable.tsx:515-519`), **không** tự vẽ checkbox.

### D8 — Popup 2 (chứng từ) là MỘT component, ba chế độ `create | view`

`SCR_BTCN_ChungTu_XemChiTiet.md:5` nói bố cục **giống hệt** màn Thêm mới, chỉ khác là toàn bộ
control disabled + bộ nút theo trạng thái. Không có nút Sửa ở bất kỳ trạng thái nào
(`SCR_BTCN_ChungTu_XemChiTiet.md:56`) nên **không có chế độ `edit`**.

**Hệ quả lên code:** `components/ChungTuBuTruModal.tsx` nhận `mode: 'create' | 'view'`;
`helpers/anHien.ts` là hàm thuần dịch thẳng 3 ma trận Ẩn/Hiện sang cờ; footer dựng từ máy trạng thái
kernel (D4).

### D9 — i18n: MỘT namespace `buTruCongNo`, popup là nhánh con

`buTru.*` (popup thiết lập) · `chungTu.*` (popup chứng từ) · `xoa.*` (popup xác nhận) · `danhSach.*`
(chữ bổ sung cho màn danh sách) · `msg.*` (nguyên văn `6.messages.md`).

**Hệ quả lên code:** một cặp `vi.ts`/`en.ts` duy nhất, khớp khoá 1-1; `registerBuTruCongNoI18n.ts`
được `pages/BuTruCongNoPage.tsx` side-effect import để đi cùng chunk lazy (`client/CLAUDE.md:355-370`;
mẫu `features/banHang/chungTuBanHang/pages/ChungTuBanHangPage.tsx:27`).

### D10 — Chiều rộng popup lấy số thật của Figma, không ép về token

Figma: Dialog Box **1392×988** (node `41323:660608`), popup 2 rộng **1392** (đo trên frame
`41383:666955`). Token hiện có: `MODAL_WIDTH_SIMPLE = 800`, `MODAL_WIDTH_COMPLEX = 1200`
(`client/src/base/theme/tokens.ts:37-38`) — **không cái nào khớp**.

**Hệ quả lên code:** thêm token `MODAL_WIDTH_WIDE = 1392` vào `base/theme/tokens.ts` và export qua
`@base` (thêm vào base, **không** hardcode 1392 trong feature — `client/CLAUDE.md:321-323`).
Cần Design xác nhận đây là bề rộng chuẩn thứ ba hay chỉ là số riêng của màn này → Q7.

---

## 1. Phạm vi

### Trong phạm vi

- **F1** — Popup **Bù trừ công nợ** (thiết lập): header filter, nút Lấy dữ liệu, 2 bảng chứng từ,
  tick/untick + phân bổ tự động BR02, sửa tay số tiền bù trừ, ô "Số tiền bù trừ", nút Bù trừ · Hủy.
- **F2** — Popup **Chứng từ bù trừ công nợ (Thêm mới)**: thông tin chung, tab Hạch toán (kể cả dòng
  chênh lệch tỷ giá), tab Chứng từ công nợ (cặp ghép), nút Hủy · Lưu · Lưu và ghi sổ.
- **F3** — Popup **Chứng từ bù trừ công nợ (Xem chi tiết)**: cùng bố cục, chế độ chỉ xem, bộ nút theo
  trạng thái (Ghi sổ · Xóa khi Chưa ghi sổ; Bỏ ghi khi Đã ghi sổ).
- **F4** — Popup **xác nhận Xóa** + popup **xác nhận Bỏ ghi**.
- **F5** — Route `/tong-hop/bu-tru-cong-no` + nối tay vào `RootRoutes.tsx` + mã quyền.
- **F6** — i18n `vi` + `en`, hằng số, hợp đồng Zod với BE, test.

### NGOÀI phạm vi (nêu đích danh)

| Bị loại | Lý do |
|---|---|
| **`SCR_BTCN_DanhSach` — dựng màn danh sách** | Thuộc epic **PMKT-E-09980** (`SCR_BTCN_DanhSach.md:5`). File `01-*.md` chỉ chốt hợp đồng tích hợp, không sinh code màn danh sách. |
| Nút **In**, **Tiện ích**, **Điều hướng trước/sau** trên màn Xem chi tiết | `SCR_BTCN_ChungTu_XemChiTiet.md:38` ghi rõ *"Nghiệp vụ in sẽ được mô tả ở tài liệu riêng (chưa xử lý trong phạm vi này)"*; "Tiện ích" và "Điều hướng" không có đặc tả lẫn Figma. → Q6. |
| **Tab "Đính kèm"** và **tab "Tham chiếu"** (2/4 tab Figma vẽ) | Không có trong bất kỳ bảng trường nào của `SCR_BTCN_ChungTu_ThemMoi.md`. → C3 / Q3. |
| **MSG_PMKT-E-14294_101** — chặn Bỏ ghi sổ chứng từ công nợ đang tham gia bù trừ | Popup này bật ở **màn chứng từ bán hàng / mua hàng**, không ở module này (`SCR_BTCN_ChungTu_ThemMoi.md:152`). Ghi lại ở §12/Q8 để mở ticket cho các module đó. |
| Menu **Bán hàng → Bù trừ công nợ** / **Mua hàng → Bù trừ công nợ** dạng submenu | Sidebar hiện chỉ có **2 cấp** (nhóm → leaf), `MenuGroup.children` là leaf phẳng (`app/layouts/shell/menuModel.ts:25-29`, `menuRegistry.tsx:120-172`). Cần quyết định của Design → Q2. |

---

## 2. Hiện trạng đã khảo sát

Bốn câu hỏi bắt buộc của `docs/fe-khung-kien-truc-chuan.md:131-139`:

| # | Câu hỏi | Trả lời | Bằng chứng |
|---|---|---|---|
| 0 | Code ở đâu? | `client/src/features/tongHop/buTruCongNo/` | luật cứng `client/CLAUDE.md:121-123` |
| 1 | Màn loại nào? | **Chứng từ** — nhưng là **form/popup**, không phải màn danh sách | `3.crud-matrix.md:7` (ENT_PhieuKeToanTongHop) |
| 2 | Đã có engine chưa? | Có engine `@domain-kit/chungTu` nhưng **là engine danh sách** → chỉ mượn kernel (D4) | `base/domainKit/chungTu/index.ts:75-92` (`ChungTuListPage`, `useChungTuList`) vs `:17-53` (kernel) |
| 3 | Component đã có ở `@base`? | **Có gần như đủ** — xem §3 | `base/index.ts` (638 dòng export) |
| 4 | Domain đang chạy không? | **Có** — `tongHopRoutes` đã nằm trong cây route | `app/router/RootRoutes.tsx:16` (import) + `:166` (`...gateByHandle(tongHopRoutes)`) |

### Lệnh đã chạy + kết quả thật

```bash
# 1) Domain nào đang chạy
grep -n "Routes" client/src/app/router/RootRoutes.tsx
#   → banHang · heThong · muaHang · tienGui · tienMat · tongHop   (dòng 11-16, 161-166)
#   → `features/danhMuc` KHÔNG có trong cây route (nhánh chết, client/CLAUDE.md:164)

# 2) Đã có code Phiếu KTTH / Bù trừ công nợ ở FE chưa
grep -rniE "phieuKeToan|phieuKTTH|keToanTongHop" client/src --include="*.ts" --include="*.tsx" -l
#   → 0 kết quả
grep -rniE "butru" client/src --include="*.ts" --include="*.tsx" -l
#   → 0 kết quả   (chỉ có `doiTru` — nghiệp vụ KHÁC, xem ghi chú dưới)

# 3) BE đã có chưa
ls cell-app/src/main/java/vn/dopai/pmkt/cell/
#   → accounting_core · chung_tu_ban_hang · chung_tu_mua_hang · common · core
#     integration_ops · master_data · platform_iam · quan_he_chung_tu · reporting
#   → KHÔNG có bu_tru_cong_no, KHÔNG có phieu_ke_toan_tong_hop
grep -niE "butru|phieuketoan" cell-app/.../common/constant/MaChucNang.java
#   → :354  PHIEU_KE_TOAN   = "PhieuKeToan"
#   → :366  BU_TRU_CONG_NO  = "BuTruCongNo"
#   ⇒ hai MÃ CHỨC NĂNG đã được seed, nhưng CHƯA có controller/endpoint nào
```

**Ghi chú quan trọng** — `features/muaHang/chungTuMuaHang/doiTruChungTu/` là **Đối trừ chứng từ**
(nghiệp vụ khác: bù một chứng từ với chính chuỗi thanh toán của nó), **không phải** Bù trừ công nợ
(bù công nợ phải thu ↔ phải trả của cùng đối tượng). Module đó còn `mock.ts`
(`features/muaHang/chungTuMuaHang/doiTruChungTu/mock.ts`) và theo **shape phẳng đã đóng băng**
(`client/CLAUDE.md:176-184`) ⇒ **không lấy làm mẫu**, chỉ ghi nhận để không trùng tên.

### Tình trạng API BE

**Chưa có endpoint nào.** ⇒ `api/mock.ts` sẽ tồn tại tạm và **là nợ phải gỡ** khi BE lên
(`docs/fe-khung-kien-truc-chuan.md:163`). Hợp đồng đề xuất ở
[06-hop-dong-api-va-i18n.md](06-hop-dong-api-va-i18n.md) — cần chốt với BE **trước** khi code
`api/model.ts`, vì Zod schema là điểm gãy đắt nhất nếu đoán sai.

Chưa có plan BE tương ứng trong `docs/doing/` (hiện chỉ có `PMKT-E-00542-*`, `PMKT-E-06194-*`,
`PMKT-E-07528-*`) ⇒ **đề nghị chạy `/plan-be` cho epic này trước hoặc song song**.

---

## 3. Kế hoạch reuse

Luật: thiếu prop nhỏ → **thêm prop vào `@base`**, không copy ra feature (`client/CLAUDE.md:321-323`).

| Cần | Có sẵn ở đâu | Dùng lại / viết mới | Lý do |
|---|---|---|---|
| Khung popup (header + body + footer, ×, Esc, guard "bỏ dở", khoá khi đang gọi API) | `CommonModalShell` — `base/index.ts:264`; props `zIndex`, `busy`, `dirty`+`discardConfirm`, `width` — `base/components/modal/CommonModalShell.tsx:33-67` | **Dùng lại** | `zIndex` giải quyết được đúng bài toán 2 popup chồng nhau của Figma |
| Footer 3 nút (Hủy trái · Lưu · Lưu và ghi sổ phải) | `CommonModalFooter` — `base/index.ts:271` · `ModelFooter` — `:295` | **Dùng lại** | BR3 (nút hủy trái / action phải) đã nằm trong component |
| Bảng 2 danh sách chứng từ: 15 cột · checkbox chọn dòng · dòng Tổng · tìm nhanh · Reload · phân trang · giữ tick qua trang | `CommonListTable` — `base/index.ts:316`. `selectable`/`selectedRowKeys`/`onSelectionChange`/`rowSelectable` (`CommonListTable.tsx:515-519`), `preserveSelectedRowKeys` (`:523`), `showSummary`+`summaryScope:'all'` (`:538-543`), `showSearch`/`onSearch` (`:389,399`), `showReload`/`onReload` (`:392,447`), `pagination` (`:546`), `title` (`:559`), `wrapInCard` (`:585`) | **Dùng lại 100%** | Không thiếu prop nào cho yêu cầu của SCR |
| Nhóm cột cha–con "Chứng từ phải thu" / "Chứng từ phải trả" (tab Chứng từ công nợ) | `ListField.children` — `base/components/table/listTableFormat.ts:47-56` (header GROUP 34px + con 32px) | **Dùng lại** | Đúng thứ Figma vẽ ở node `41383:672221` |
| Dòng Tổng của bảng con (tab Hạch toán, tab Chứng từ công nợ) | `ListField.summary: 'sum' \| fn \| node` — `listTableFormat.ts:80-86`; `CommonTableSummaryRow` — `base/index.ts:340` | **Dùng lại** | |
| Ô nhập số "Số tiền bù trừ" trong lưới | `CommonNumberInput` — `base/index.ts:166` | **Dùng lại** | |
| Combogrid chọn **Đối tượng** | `CommonComboGrid` — `base/index.ts:568` (có `extraColumns`, `pagination`, `searchable`, `isInactive`) | **Dùng lại** | BR5 dòng "Mã đối tượng" (`business_rules.md:95`) |
| Dropdown **TK phải thu / TK phải trả / Loại tiền / Loại nghiệp vụ** | `CommonSelectBox` — `base/index.ts:578` | **Dùng lại** | SCR ghi control = Dropdown (`SCR_BTCN_BuTru.md:29-32`) → Q5 |
| Ô ngày **Ngày bù trừ / Ngày hạch toán / Ngày chứng từ** | `CommonDateInput` — `base/index.ts:170` | **Dùng lại** | |
| Ô chữ **Lý do / Số chứng từ / Diễn giải** | `CommonTextBox` — `base/index.ts:178` (kèm `maxLen` — `:205`) | **Dùng lại** | BR14.4 chặn cứng maxLength đã nằm trong component |
| Nhãn có dấu `*` | `FieldLabel` — `base/index.ts:194` | **Dùng lại** | |
| Tab gạch chân (Hạch toán · Chứng từ công nợ · …) | `TabMenuChild` — `base/index.ts:150` | **Dùng lại** | `TabMenu2Level` (`:148`) là tab **thư mục** của thanh cấp 2, không phải cái Figma vẽ trong popup |
| Popup xác nhận Xóa / Bỏ ghi | `CommonConfirmModal` (`tone='danger'`) — `base/index.ts:276`; mẫu dùng: `features/banHang/chungTuBanHang/components/ChungTuBanHangTab.tsx:339-348` | **Dùng lại** | BR3 |
| Toast thành công/lỗi | `useToast` — `base/index.ts:49`; map lỗi API bằng `describeApiError` từ `@platform` (mẫu `ChungTuBanHangTab.tsx:274-276`) | **Dùng lại** | BR26 |
| Badge trạng thái Chưa/Đã ghi sổ | `CommonStatusTag` / `ListTag` — `base/index.ts:593` | **Dùng lại** | BR33 |
| Máy trạng thái nút Ghi sổ/Bỏ ghi/Xóa theo trạng thái + quyền | `tinhTrangThaiHanhDong`, `LY_DO_DISABLE`, `LuatModule` — `base/domainKit/chungTu/index.ts:37-49` | **Dùng lại** | BR12/BR13/BR42 đã mã hoá trong kernel |
| Chuỗi trạng thái ghi sổ ↔ 2 khái niệm kernel | `TRANG_THAI_GHI_SO`, `docTrangThai`, `BanDoTrangThai` — `base/domainKit/chungTu/index.ts:12-31` | **Dùng lại** | Engine **cấm hardcode** chuỗi trạng thái (`ChungTuDescriptor.ts:151`) |
| 7 mã lỗi kernel | `MA_LOI_KERNEL`, `moTaLoiChungTu` — `base/domainKit/chungTu/index.ts:52-54` | **Dùng lại** | |
| **Bề rộng popup 1392px** | `MODAL_WIDTH_SIMPLE=800` / `MODAL_WIDTH_COMPLEX=1200` — `base/theme/tokens.ts:37-38` | ⚠ **Thêm token vào `@base`** (`MODAL_WIDTH_WIDE = 1392`) | Không có token khớp; thêm ở base thay vì hardcode ở feature (D10, Q7) |
| Component riêng của màn | — | **Viết mới 8 component** (§4) | Đã kiểm `@base` (638 dòng barrel) và `@domain-kit`: không có sẵn "popup 2 bảng bù trừ", "tab cặp ghép", "khối 2 cột thông tin chứng từ" — chúng mang **logic nghiệp vụ riêng của màn**, không phải component thuần trình bày dùng được ≥2 màn |

---

## 4. Kiến trúc module — cây thư mục sẽ sinh

```
client/src/features/tongHop/
├── routes.tsx                              ← SỬA: thêm 1 route (file đã có)
└── buTruCongNo/                            ← MODULE MỚI
    ├── index.ts                            ← FILE DUY NHẤT ở gốc
    ├── api/
    │   ├── model.ts                        Zod schema + type suy ra (wire với BE)
    │   ├── buTruCongNoApi.ts               hàm gọi http, parse Zod
    │   ├── queries.ts                      TanStack Query hooks (useLayDuLieu · useLuu · useChiTiet · useGhiSo · useBoGhi · useXoa)
    │   ├── payload.ts                      state form → request body
    │   └── mock.ts                         ⚠ NỢ — chỉ tồn tại tới khi BE lên
    ├── components/
    │   ├── BuTruCongNoModal.tsx            popup 1 — thiết lập bù trừ
    │   ├── BuTruHeaderFilter.tsx           hàng lọc trên cùng popup 1
    │   ├── ChungTuBuTruTable.tsx           1 bảng dùng cho cả phải thu / phải trả (prop `ben`)
    │   ├── ChungTuBuTruModal.tsx           popup 2 — Phiếu KTTH loại Bù trừ (mode create | view)
    │   ├── ThongTinChungBuTru.tsx          khối 2 cột thông tin chung của popup 2
    │   ├── HachToanTab.tsx                 tab Hạch toán
    │   ├── ChungTuCongNoTab.tsx            tab Chứng từ công nợ (2 nhóm cột cha–con)
    │   └── XacNhanBuTruModal.tsx           popup xác nhận Xóa / Bỏ ghi (bọc CommonConfirmModal)
    ├── constants/
    │   ├── constants.ts                    TK mặc định 131/331 · page size · maxLength · khoá tab …
    │   ├── paths.ts                        BU_TRU_CONG_NO_PATHS
    │   └── permissions.ts                  BU_TRU_CONG_NO_PERM · PHIEU_KE_TOAN_PERM
    ├── fields/
    │   ├── types.ts                        kiểu dùng chung của module
    │   ├── buTruColumns.ts                 cột 2 bảng chứng từ (hàm theo `ben` + `coQuyDoi`)
    │   ├── hachToanColumns.ts              cột tab Hạch toán
    │   ├── chungTuCongNoColumns.ts         cột tab Chứng từ công nợ (nhóm cha–con)
    │   ├── options.ts                      option Loại nghiệp vụ / Loại tiền / TK
    │   └── texts.ts                        gom `texts` của CommonListTable / ComboGrid / ConfirmModal
    ├── helpers/
    │   ├── phanBo.ts                       BR02 — thuật toán phân bổ tự động
    │   ├── ghepCap.ts                      dựng các cặp ghép cho tab Chứng từ công nợ
    │   ├── hachToan.ts                     dựng 2 dòng hạch toán + chênh lệch tỷ giá (BR02 popup 2)
    │   ├── quyDoi.ts                       nhân tỷ giá + làm tròn BR7
    │   ├── anHien.ts                       dịch 3 ma trận Ẩn/Hiện thành cờ
    │   └── kiemTra.ts                      BR01/BR03/BR04 — điều kiện Lấy dữ liệu / Bù trừ
    ├── hooks/
    │   ├── useBuTruSetup.ts                state popup 1 (filter · 2 bảng · tick · phân bổ · tổng)
    │   ├── useChungTuBuTruForm.ts          state popup 2 (form · dựng sẵn · lưu / lưu và ghi sổ)
    │   └── useBuTruActions.ts              ghi sổ · bỏ ghi · xóa (+ confirm + toast + invalidate)
    ├── i18n/
    │   ├── vi.ts
    │   ├── en.ts
    │   └── registerBuTruCongNoI18n.ts
    ├── pages/
    │   ├── BuTruCongNoPage.tsx             CHỈ ráp: side-effect import i18n + mở popup 1
    │   └── buTruCongNo.css                 tiền tố `.pmkt-btcn-*`
    └── test/
        ├── phanBo.test.ts
        ├── ghepCap.test.ts
        ├── hachToan.test.ts
        ├── anHien.test.ts
        ├── kiemTra.test.ts
        ├── api.test.ts
        └── buTruCongNo.render.test.tsx
```

Không tạo thư mục rỗng; không file thứ hai ở gốc module; không `../../` (cây phẳng một bậc).

---

## 5. Checklist artefact (bám `docs/fe-khung-kien-truc-chuan.md:143-163`)

| # | Artefact | Đường dẫn | Sẽ tạo? |
|---|---|---|---|
| 1 | Hợp đồng BE (Zod + hàm gọi) | `buTruCongNo/api/` | ✅ |
| 2 | Kiểu dùng chung | `buTruCongNo/fields/types.ts` | ✅ |
| 3 | Hằng số nghiệp vụ | `buTruCongNo/constants/constants.ts` | ✅ |
| 4 | Cột / ô lưới / option / badge | `buTruCongNo/fields/` | ✅ (5 file) |
| 5 | Logic nghiệp vụ thuần | `buTruCongNo/helpers/` | ✅ (6 file — BR02 phân bổ, ghép cặp, hạch toán, quy đổi, ẩn/hiện, kiểm tra) |
| 6 | State & request | `buTruCongNo/hooks/` | ✅ (3 hook) |
| 7 | Component riêng của màn (kể cả popup) | `buTruCongNo/components/` | ✅ (8 component) |
| 8 | Entry màn hình + CSS | `buTruCongNo/pages/` | ✅ |
| 9 | i18n `vi` + `en` + register (MỘT namespace) | `buTruCongNo/i18n/` | ✅ |
| 10 | Cửa ra | `buTruCongNo/index.ts` | ✅ (file DUY NHẤT ở gốc) |
| 11 | Test | `buTruCongNo/test/` | ✅ (7 file) |
| 12 | Mã quyền | `buTruCongNo/constants/permissions.ts` | ✅ |
| 13 | Đường dẫn | `buTruCongNo/constants/paths.ts` | ✅ |
| 14 | Route + `handle` (perm, crumbKeys) | `features/tongHop/routes.tsx` | ✅ (**sửa file có sẵn**) |
| 15 | Nối tay vào cây route | `app/router/RootRoutes.tsx` | ➖ **không cần sửa** — `tongHopRoutes` đã được nối ở `:166`; route mới ăn theo |

Ngoài module: `base/theme/tokens.ts` + `base/index.ts` — thêm `MODAL_WIDTH_WIDE` (D10).

---

## 6. Route & quyền

### 6.1. `constants/paths.ts`

```ts
export const BU_TRU_CONG_NO_PATHS = {
  buTruCongNo: '/tong-hop/bu-tru-cong-no',
} as const
```

Slug giữ chính tả tiếng Việt không dấu, đồng bộ `TONG_HOP_PATHS.khoaSo = '/tong-hop/khoa-so-ky-ke-toan'`
(`features/tongHop/khoaSo/constants/paths.ts:9-11`).

### 6.2. `features/tongHop/routes.tsx` — thêm route thứ hai

```ts
import { BU_TRU_CONG_NO_PATHS } from './buTruCongNo/constants/paths.ts'
import { BU_TRU_CONG_NO_PERM } from './buTruCongNo/constants/permissions.ts'

// … route khoaSo giữ nguyên …
{
  path: BU_TRU_CONG_NO_PATHS.buTruCongNo,
  handle: {
    perm: BU_TRU_CONG_NO_PERM.create,
    crumbKeys: ['app:shell.menu.tongHop', 'buTruCongNo:menu.buTruCongNo'],
  } satisfies TongHopRouteHandle,
  lazy: async () => ({ Component: (await import('./buTruCongNo')).BuTruCongNoPage }),
}
```

⚠ **`perm` là `.Create`, không phải `.View`** — đây là ngoại lệ có chủ đích so với quy ước:
`UC_BTCN_ThemMoi.md:12` ghi *"mở màn hình SCR_BTCN_BuTru khi người dùng có quyền `BuTruCongNo.Create`;
không có quyền → ẩn menu"*, và `MSG_PMKT-E-14294_005` áp cho trường hợp vào thẳng bằng URL.
Mã chức năng `BuTruCongNo` không có động từ `.View` trong tài liệu BA.

### 6.3. Mã quyền — `constants/permissions.ts` (BR25)

```ts
/** Mã chức năng `BuTruCongNo` — MaChucNang.java:366 (đã seed ở BE). */
export const BU_TRU_CONG_NO_PERM = {
  create: 'BuTruCongNo.Create',
} as const

/** Chứng từ kết quả là Phiếu KTTH ⇒ vòng đời đi theo mã chức năng `PhieuKeToan` — MaChucNang.java:354. */
export const PHIEU_KE_TOAN_PERM = {
  view: 'PhieuKeToan.View',
  viewDetail: 'PhieuKeToan.View.Detail',
  delete: 'PhieuKeToan.Delete',
  ghiSo: 'PhieuKeToan.Post',
  boGhiSo: 'PhieuKeToan.Unpost',
} as const
```

Cả hai mã chức năng **đã có trong catalog BE**
(`cell-app/src/main/java/vn/dopai/pmkt/cell/common/constant/MaChucNang.java:354,366`), nhưng **chưa có
controller nào tiêu thụ** ⇒ tên động từ (`.Create`, `.Post`, …) vẫn là **giả định theo tài liệu BA**,
phải đối chiếu lại khi BE lên.

BR25.2: thiếu quyền → **ẩn nút**, không disable.

### 6.4. Menu

Sidebar hiện: leaf `tong-hop` đang **`disabled: true`** (`app/layouts/shell/menuRegistry.tsx:177`) —
tức màn Khóa sổ đang chạy nhưng **không vào được từ menu**. Màn này cũng vậy nếu không sửa.
Cách đưa vào menu (submenu Bán hàng/Mua hàng như BA yêu cầu) **chưa có cơ chế** — xem Q2.

---

## 7. Bản đồ màn ↔ file con ↔ SCR ↔ UC ↔ Matrix

| File con | SCR | UC | Matrix |
|---|---|---|---|
| [01-danh-sach-chung-tu-bu-tru.md](01-danh-sach-chung-tu-bu-tru.md) | `SCR_BTCN_DanhSach.md` | PMKT-U-14688 | **SKIP** — `_scope.md:10` (màn danh sách, ngoài phạm vi ma trận) |
| [02-popup-bu-tru-cong-no.md](02-popup-bu-tru-cong-no.md) | `SCR_BTCN_BuTru.md` | PMKT-U-14690 | `SCR_BTCN_BuTru_MaTranAnHien.md` |
| [03-popup-chung-tu-bu-tru-them-moi.md](03-popup-chung-tu-bu-tru-them-moi.md) | `SCR_BTCN_ChungTu_ThemMoi.md` | PMKT-U-14690 | `SCR_BTCN_ChungTu_ThemMoi_MaTranAnHien.md` |
| [04-popup-chung-tu-bu-tru-xem-chi-tiet.md](04-popup-chung-tu-bu-tru-xem-chi-tiet.md) | `SCR_BTCN_ChungTu_XemChiTiet.md` | PMKT-U-14691 · PMKT-U-14693 | `SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md` |
| [05-popup-xac-nhan-xoa.md](05-popup-xac-nhan-xoa.md) | `SCR_BTCN_PopupXacNhanXoa.md` | PMKT-U-14692 | **SKIP** — `_scope.md:11` |

Đủ 5/5 `SCR_*.md` của epic, mỗi file xuất hiện đúng 1 lần.

---

## 8. i18n — một namespace `buTruCongNo`

```
buTruCongNo
├── menu.buTruCongNo                      "Bù trừ công nợ"
├── buTru.*            popup 1  — title · filter.* · bangPhaiThu.* · bangPhaiTra.* · cot.* · nut.*
├── chungTu.*          popup 2  — title · thongTinChung.* · tab.* · cotHachToan.* · cotCongNo.* · nut.*
├── xoa.*              popup xác nhận xóa  — title · message · nut.*
├── boGhi.*            popup xác nhận bỏ ghi
├── danhSach.*         chữ bổ sung của màn danh sách (loại nghiệp vụ "Bù trừ công nợ", nút hàng)
├── trangThai.*        "Chưa ghi sổ" · "Đã ghi sổ"        (BR12/BR33)
└── msg.*              NGUYÊN VĂN 6.messages.md (MSG_001 … MSG_201)
```

Nguồn chữ: **nguyên văn tiếng Việt** của `6.messages.md` và của các bảng trường trong `5.screens/**`.
Chuỗi động dùng interpolation (`msg.xacNhanXoa` có `{{soChungTu}}`, `msg.kyDaKhoa` có `{{ngayKhoaSo}}`),
**không** cộng chuỗi. Bảng khoá đầy đủ vi/en: [06-hop-dong-api-va-i18n.md §3](06-hop-dong-api-va-i18n.md).

---

## 9. Thứ tự thực hiện

| Bước | Việc | Phụ thuộc |
|---|---|---|
| B0 | **Chốt hợp đồng API với BE** (file 06) + chốt Q1…Q11 với BA/Design | — |
| B1 | `constants/` + `fields/types.ts` + `i18n/` + `api/model.ts` (Zod) | B0 |
| B2 | `helpers/quyDoi.ts` · `helpers/phanBo.ts` · `helpers/ghepCap.ts` · `helpers/hachToan.ts` + test | B1 — **thuần, làm được ngay dù chưa có API** |
| B3 | `helpers/anHien.ts` · `helpers/kiemTra.ts` + test | B1 |
| B4 | `api/buTruCongNoApi.ts` · `api/queries.ts` · `api/payload.ts` (+ `mock.ts` nếu BE chưa lên) | B1 |
| B5 | `fields/buTruColumns.ts` · `fields/texts.ts` + `components/ChungTuBuTruTable.tsx` | B2, B4 |
| B6 | `components/BuTruHeaderFilter.tsx` + `hooks/useBuTruSetup.ts` + `components/BuTruCongNoModal.tsx` | B5 |
| B7 | `base/theme/tokens.ts` — thêm `MODAL_WIDTH_WIDE` (D10) | B0 (Q7) |
| B8 | `fields/hachToanColumns.ts` · `fields/chungTuCongNoColumns.ts` + `HachToanTab` · `ChungTuCongNoTab` · `ThongTinChungBuTru` | B2, B3 |
| B9 | `hooks/useChungTuBuTruForm.ts` + `components/ChungTuBuTruModal.tsx` (mode `create`) | B6, B8 · **chặn bởi Q11** (nguyên tử hay 2 pha ⇒ hành vi đóng popup khác hẳn) |
| B10 | `hooks/useBuTruActions.ts` + `XacNhanBuTruModal` + mode `view` của popup 2 | B9 |
| B11 | `pages/` + `index.ts` + `routes.tsx` + CSS | B10 |
| B12 | Test render + chạy cổng nghiệm thu §13 | B11 |

**Chặn cứng:** B4 trở đi phụ thuộc BE. B2/B3 (toàn bộ nghiệp vụ tính toán — phần khó nhất và
đáng test nhất của epic) **không** phụ thuộc BE ⇒ nên làm trước để không nằm chờ.

---

## 10. Rủi ro

| # | Rủi ro | Giảm thiểu |
|---|---|---|
| **R1** | **Không có màn danh sách để đặt chân.** Xem chi tiết / Ghi sổ / Bỏ ghi / Xóa (3/5 UC) đều khởi phát từ danh sách Phiếu KTTH — module đó chưa tồn tại. | Module export popup + hook hành động qua `index.ts`; luồng tạo mới tự chủ qua route riêng. Khi module Phiếu KTTH lên, phần dùng chung chuyển xuống `features/tongHop/_shared/` (leaf **không** với được leaf anh em — `client/CLAUDE.md:108-109`). → Q1 |
| **R2** | **BE trắng.** Không có endpoint, không có DTO, không có plan BE. Đoán sai shape ⇒ đập lại `api/` + `helpers/`. | B0 chốt hợp đồng trước; `mock.ts` khoanh gọn trong `api/`; mọi dữ liệu ngoài đi qua Zod `parse` nên đổi shape là lỗi biên dịch, không phải lỗi giữa màn |
| **R3** | **Nạp toàn bộ 2 danh sách (D6).** Đối tượng nhiều giao dịch ⇒ vài nghìn dòng × 15 cột trong RAM + 2 bảng cùng lúc. | Đo thật trước khi phát hành; nếu vượt trần → yêu cầu BE cấp endpoint phân bổ server-side. Trần cần BA chốt → Q4 |
| **R4** | **Hai popup chồng nhau** (Figma vẽ popup 2 đè lên popup 1). Focus trap của antd, Esc đóng nhầm lớp, guard "bỏ dở" của lớp dưới bị kích hoạt sai. | `CommonModalShell` có `zIndex` + `escClosable` + `dirty`/`discardConfirm` riêng cho từng lớp (`CommonModalShell.tsx:48-65`); test render phải phủ đúng ca "Esc khi popup 2 đang mở" |
| **R5** | **Tràn ngang khi ngoại tệ.** 15 cột trong vùng rộng 1328px — chính mock Figma (`41383:670216`) cũng vẽ tràn ra ngoài hộp thoại. | Bảng cuộn ngang trong khung riêng; cân nhắc ghim cột `Số chứng từ`; Design chốt bộ độ rộng cột → Q9 |
| **R6** | **Không vào được từ menu.** Leaf `tong-hop` đang `disabled: true` (`menuRegistry.tsx:177`), và submenu 3 cấp mà BA mô tả thì shell chưa hỗ trợ. | → Q2. Trong lúc chờ, màn vẫn deep-link được bằng URL và test được |
| **R7** | **Sai số làm tròn quy đổi.** Tổng đại số cột "Chênh lệch tỷ giá" **phải** đúng bằng Số tiền quy đổi dòng hạch toán 2 (`SCR_BTCN_ChungTu_ThemMoi.md:95`). Cộng từng dòng đã làm tròn ≠ làm tròn của tổng. | `helpers/quyDoi.ts` là điểm làm tròn **duy nhất**; dòng 2 tính từ **tổng chưa làm tròn** rồi mới làm tròn một lần (BR7.3: lưu đủ, chỉ tròn khi hiển thị). Có test riêng cho ca lệch |
| **R8** | **Số dư đổi giữa chừng** (`MSG_PMKT-E-14294_018`). FE không kiểm được, chỉ hiển thị lỗi BE trả. | `api/` map mã lỗi BE → khoá i18n; FE **không** tự sinh câu chữ cho ca này |
| **R9** | **"Lưu và ghi sổ" không rõ có nguyên tử không.** BA (`AD_BTCN_ThemMoi.puml`, `UC_BTCN_ThemMoi.md:122,135`) mô tả **2 pha** — lưu xong rồi ghi sổ hỏng thì **giữ lại** chứng từ Chưa ghi sổ; kernel FE lại khai *"MỘT request, MỘT transaction"* (`ChungTuDescriptor.ts:174-181`). Chọn sai ⇒ người dùng bấm Lưu lần hai và **tạo chứng từ trùng**. | Chốt **Q11** trước bước B9; response lỗi phải mang `id` nếu là 2 pha. Hệ quả chi tiết: [03 §7.2](03-popup-chung-tu-bu-tru-them-moi.md) · [06 §1.4](06-hop-dong-api-va-i18n.md) |

---

## 11. Conflict Figma ↔ Matrix/SCR

> Luật xử lý: **UI theo Figma, behavior theo Matrix/SCR**. Mọi điểm dưới đây đều cần BA/Design xác nhận.

| # | Điểm | Figma nói gì | Matrix / SCR nói gì | Xử lý |
|---|---|---|---|---|
| **C1** | Tiêu đề popup 2 | "**Phiếu kế toán tổng hợp**" (node `41383:666955`) | "Chứng từ bù trừ công nợ" + [Số chứng từ] (`SCR_BTCN_ChungTu_XemChiTiet.md:5`) | Tiêu đề là **chữ hiển thị** ⇒ theo Figma; nhưng hai tài liệu mâu thuẫn trực tiếp → **Q3** |
| **C2** | Trường "**Loại nghiệp vụ**" | Có, bắt buộc `*`, read-only, giá trị "Bù trừ công nợ" | **Không có** trong bảng Thông tin chung (`SCR_BTCN_ChungTu_ThemMoi.md:17-31`) | Render read-only theo Figma; giá trị là **hằng số** `LOAI_NGHIEP_VU.BU_TRU_CONG_NO`, không cho đổi |
| **C3** | Số tab của popup 2 | **4 tab**: Hạch toán · Chứng từ công nợ · **Đính kèm** · **Tham chiếu** | **2 tab**; "Tham chiếu" là **trường Link list trong Thông tin chung** (`SCR_BTCN_ChungTu_ThemMoi.md:27`); không có "Đính kèm" | Dựng **2 tab trong phạm vi**; 2 tab còn lại giữ chỗ trên thanh tab (Figma vẽ) + nội dung "đang phát triển" → **Q3** |
| **C4** | Giá trị mặc định "Số chứng từ" | Điền sẵn `BTCN-2026-7251` | **"Để trống"**, người dùng tự nhập (`SCR_BTCN_ChungTu_ThemMoi.md:26`) | **Behavior theo SCR: để trống.** Chuỗi trong Figma là dữ liệu mẫu |
| **C5** | Cột "**Ngày hạch toán**" ở 2 bảng chứng từ | Có, là cột đầu sau checkbox | **Không có** trong 2 bảng (`SCR_BTCN_BuTru.md:50-66`, `:81-97`) | Hiển thị theo Figma (read-only) → **Q4** |
| **C6** | Nhãn cột hạn | Frame VND: "Hạn thanh toán" · Frame ngoại tệ (`41383:670216`): "**Hạn hạch toán**" | "Hạn thanh toán" | **Theo SCR** — hai frame Figma tự mâu thuẫn ⇒ frame ngoại tệ là lỗi chính tả |
| **C7** | Nhãn cột bảng phải trả | Frame VND: "**Số chưa nợ**" · Frame ngoại tệ: "Số còn nợ" | "Số còn nợ" | **Theo SCR** (frame ngoại tệ đồng ý) |
| **C8** | Nhãn cột tab Hạch toán | "**TN Nợ**" / "**TN Có**" | "TK Nợ" / "TK Có" (`SCR_BTCN_ChungTu_ThemMoi.md:43-44`) | **Theo SCR** — "TN" là viết tắt sai trong Figma |
| **C9** | Dấu `*` của "Ngày bù trừ" | **Không có** dấu `*` (đo trên node `41383:661314`) | Bắt buộc = **Y** (`SCR_BTCN_BuTru.md:31`); BR01 chặn Lấy dữ liệu nếu thiếu | **Behavior theo SCR: bắt buộc**, UI **phải** có `*` ⇒ Figma cần sửa → **Q5** |
| **C10** | Vị trí ô "Số tiền bù trừ" | Frame `41323:656771`: **dải riêng đáy popup** (node `41383:669973`, 1360×40, chữ phải, số màu xanh lá) · Frame `41383:666955`: **trong hàng header filter**, góc phải | Thuộc **Header Filter** (`SCR_BTCN_BuTru.md:34`) | Hai frame Figma tự mâu thuẫn → **Q5**. Tạm chọn **dải đáy** (frame chuyên cho màn này) |
| **C11** | Icon **thùng rác** trên từng dòng 2 bảng | Có (frame `41383:666955`) | Ma trận **không có** hành động xóa dòng; 2 bảng chỉ tick + nhập số tiền | **Behavior theo Matrix: không render cột xóa** → **Q4** |
| **C12** | Dòng **Tổng** trong tab Hạch toán và tab Chứng từ công nợ | Có ở cả hai | SCR **không nhắc** | Dựng theo Figma — BR31 vốn bắt buộc dòng tổng cho cột số tiền |
| **C13** | Tên cột tiền trên danh sách | "**Số tiền**" | "**Tổng tiền**" (`SCR_BTCN_DanhSach.md:20`, `SCR_PhieuKTTH_DanhSach.md`) | **Theo SCR** — nhưng là màn của epic 09980, chỉ ghi nhận |
| **C14** | Màn **Xem chi tiết** | **Không có frame riêng**; Figma chỉ có panel xem nhanh dưới danh sách với 4 tab + menu ⋮ (Xem chi tiết · Ghi sổ · Bỏ ghi sổ · Xóa) | Màn chỉ-xem đầy đủ, có Điều hướng trước/sau · In · Tiện ích | Dùng lại popup 2 ở `mode='view'` (D8); 3 nút không có Figma ⇒ **ngoài phạm vi** → **Q6** |
| **C15** | Đường vào menu | Không có frame menu điều hướng (frame `41322:650973` "Dropdown Menu bù trừ" thực chất là **menu ⋮ trên dòng**: Xem chi tiết · Ghi sổ · Bỏ ghi sổ · Xóa) | Menu **Bán hàng → Bù trừ công nợ** và **Mua hàng → Bù trừ công nợ** (`SCR_BTCN_BuTru.md:7-8`) | Shell chưa có submenu 3 cấp → **Q2** |

---

## 12. ⚠️ Điểm cần BA / Design xác nhận

**Q1 — Ai dựng màn danh sách Phiếu kế toán tổng hợp, và bao giờ?**
`SCR_BTCN_DanhSach.md:5` đẩy toàn bộ danh sách sang epic PMKT-E-09980; FE **chưa có** module đó
(grep `phieuKeToan|phieuKTTH|keToanTongHop` trong `client/src` = 0 kết quả). Không có nó thì
UC-14688 / 14691 / 14692 / 14693 **không có đường vào**.
→ Cần chốt: (a) epic 14294 dựng luôn danh sách (mở rộng phạm vi), hay (b) chờ 09980 và epic này chỉ
giao popup + hook?

**Q2 — Đường vào menu đặt ở đâu?**
BA: *"Menu Bán hàng → Bù trừ công nợ"* và *"Mua hàng → Bù trừ công nợ"* (`SCR_BTCN_BuTru.md:7-8`).
Thực tế shell: sidebar **2 cấp**, mỗi module đúng **một leaf** trỏ thẳng vào màn chính
(`app/layouts/shell/menuRegistry.tsx:141-161`), `MenuGroup.children` không có cấp con
(`menuModel.ts:25-29`); riêng leaf `tong-hop` còn đang `disabled: true` (`menuRegistry.tsx:177`).
→ Chọn: (a) mở submenu cấp 3 cho shell (việc của app, ngoài epic); (b) đặt nút "Bù trừ công nợ" trên
**toolbar** màn Chứng từ bán hàng / Chứng từ mua hàng; hay (c) mở leaf `tong-hop` và đặt ở đó?

**Q3 — Popup 2 tên là gì và có mấy tab?**
Figma: tiêu đề "Phiếu kế toán tổng hợp", **4 tab** (thêm *Đính kèm*, *Tham chiếu*), có trường
*Loại nghiệp vụ*. SCR: tiêu đề "Chứng từ bù trừ công nợ", **2 tab**, *Tham chiếu* là trường Link list
trong Thông tin chung, không có *Đính kèm*, không có *Loại nghiệp vụ*.
→ Cần bản chốt duy nhất, vì nó quyết định số component và cây khoá i18n.

**Q4 — Ba điểm dữ liệu của 2 bảng chứng từ:**
1. Cột **"Ngày hạch toán"** (C5) — có thật không? SCR không liệt kê.
2. Icon **thùng rác trên dòng** (C11) — có hay không? Ma trận không có hành động này.
3. **Trần số dòng** một lần Lấy dữ liệu (R3) — hệ thống chấp nhận tối đa bao nhiêu chứng từ/bên?
   Trả lời cái này quyết định giữ D6 (nạp hết, phân trang client) hay phải yêu cầu BE cấp
   endpoint phân bổ server-side.

**Q5 — Hai điểm UI của popup 1:**
1. **"Ngày bù trừ"**: SCR bắt buộc (Y) nhưng Figma **không** vẽ dấu `*` (C9) — Figma sửa lại đúng chứ?
2. **Ô "Số tiền bù trừ"** nằm ở **dải đáy popup** hay **trong hàng header filter**? Hai frame Figma
   vẽ hai kiểu (C10).

**Q6 — Màn Xem chi tiết trình bày thế nào?**
Không có frame Figma riêng (C14). → (a) Dùng lại popup "Phiếu kế toán tổng hợp" ở chế độ chỉ xem
(đề xuất của kế hoạch này), hay (b) một màn/popup khác? Và ba nút **Điều hướng trước/sau · In ·
Tiện ích** (`SCR_BTCN_ChungTu_XemChiTiet.md:37-39`) — có thiết kế chưa, hay đúng là để lại kỳ sau
như nút In đã ghi?
Ma trận cũng tự hỏi điều này ở *"Điểm cần xác nhận"* mục 3 (`SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md:66`):
màn có nút **Đóng** riêng không?

**Q7 — Bề rộng popup 1392px (D10).** Design chốt: đây là **bề rộng chuẩn thứ ba** của hệ (nên thêm
token `MODAL_WIDTH_WIDE` vào design system), hay chỉ là số riêng của màn này? Hai token hiện có là
800 và 1200 (`base/theme/tokens.ts:37-38`).

**Q8 — MSG_PMKT-E-14294_101 do module nào dựng?**
Popup chặn *"Chứng từ đã tham gia bù trừ công nợ…"* bật khi người dùng Bỏ ghi sổ một **chứng từ bán
hàng / mua hàng** (`SCR_BTCN_ChungTu_ThemMoi.md:152`) ⇒ nằm ở `features/banHang/chungTuBanHang` và
`features/muaHang/chungTuMuaHang`, không ở module này. Xác nhận để mở ticket riêng.

**Q9 — Bộ độ rộng cột của 2 bảng chứng từ (chế độ ngoại tệ).**
15 cột trong vùng 1328px; chính mock Figma vẽ tràn ra ngoài hộp thoại (R5). Cần Design chốt độ rộng
từng cột + cột nào được ghim.

**Q10 — Control của "TK phải thu" / "TK phải trả".**
SCR ghi **Dropdown** (`SCR_BTCN_BuTru.md:29-30`), Figma vẽ ô hẹp 86px hiện "131"/"331". Nhưng BR5
xếp *"Tài khoản kế toán (nợ/có/thuế)"* vào nhóm **combogrid** (`business_rules.md:82`).
→ Dropdown thường hay combogrid? Kế hoạch tạm theo SCR (dropdown).

**Q11 — ⭐ "Lưu và ghi sổ" có nguyên tử không? (chặn bước B9)**
Đây là mâu thuẫn **giữa tài liệu BA và code có sẵn**, không phải Figma ↔ Matrix:

| Nguồn | Khi bước ghi sổ hỏng (`MSG_..._018`) |
|---|---|
| **Code — kernel FE** | *"Bất biến kernel: đó là MỘT request, MỘT transaction — **không phải save rồi post** (`ChungTuTemplate.java:43-44`)"* — `base/domainKit/chungTu/api/ChungTuDescriptor.ts:174-181` ⇒ **rollback cả lượt** |
| **BA — Activity Diagram** | `AD_BTCN_ThemMoi.puml`: Lưu → hiện `MSG_..._001` → *rồi mới* kiểm số dư → không đủ thì `MSG_..._018` và **"chứng từ giữ trạng thái Chưa ghi sổ"** |
| **BA — Use Case** | `UC_BTCN_ThemMoi.md:122`: *"chứng từ **vẫn được lưu** ở trạng thái Chưa ghi sổ"*; `:135`: *"Thất bại: Hệ thống không lưu chứng từ (**hoặc giữ trạng thái Chưa ghi sổ nếu lỗi ở bước ghi sổ**)"* |

**Vì sao FE phải biết:** nếu là **2 pha** mà popup không đóng, người dùng bấm Lưu lần hai sẽ tạo
**chứng từ trùng** — và số chứng từ do người dùng tự nhập nên BE có thể chặn bằng `MSG_..._015`,
nhưng người dùng thì không hiểu vì sao. Ngoài ra đổi cả cách toast (1 hay 2 thông báo liên tiếp) và
cách `invalidate` (có phải làm mới danh sách khi ghi sổ hỏng không).

Kế hoạch **tạm theo BA (2 pha)** và đã ghi rõ đang lệch bất biến kernel. Nếu chốt 2 pha thì response
lỗi **bắt buộc** mang `id` chứng từ đã lưu — xem [06 §1.4](06-hop-dong-api-va-i18n.md).

---

## 13. Kiểm thử + cổng nghiệm thu

```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test
```

Rồi `npm run build`.

**Baseline repo đang ĐỎ SẴN** (`docs/fe-khung-kien-truc-chuan.md:303-305`, đo 2026-08-11):
`typecheck` **193 lỗi** · `lint` **10 lỗi + 2 warning** · `lint:boundaries` **76**
(74 "rule not found" + **2 vi phạm thật** trong `legacy`).

Luật nghiệm thu áp cho việc này:

1. Không lệnh nào được **tăng** số lỗi so với baseline.
2. **File mình chạm phải sạch** — 0 lỗi typecheck, 0 lỗi lint.
3. Không sinh vi phạm tầng mới — `boundaries/*` giữ nguyên mức nợ cũ (2).
4. Không dùng `eslint-disable` để dập lint.
5. Lệnh nào fail thì **dán output thật**.
6. `no-explicit-any` chỉ ở mức `warn` ⇒ lint xanh **không** chứng minh sạch `any`; phải tự soát
   (`client/CLAUDE.md:477-482`).

Danh sách ca test cụ thể nằm ở mục **§10 Kiểm thử** của từng file con.

---

## 14. BR áp dụng

| BR | Áp ở đâu |
|---|---|
| **BR1** phân trang | 2 bảng chứng từ popup 1 (10/20/50/100, "1-10 trên 40") — file 02 |
| **BR2** hiển thị & sắp xếp | Thứ tự Ngày chứng từ ↑ rồi Số chứng từ; cột STT `#`; checkbox sau STT — file 02, 03 |
| **BR3** popup | Cả 4 popup: nút Đóng/×, Esc, hủy trái–action phải, popup xác nhận xóa, popup xác nhận đóng khi dirty — file 02, 03, 04, 05 |
| **BR4 · BR09** loại chứng từ | Cột "Loại chứng từ" ở 2 bảng và ở tab Chứng từ công nợ; trường Tham chiếu — file 02, 03 |
| **BR5** combogrid | Combogrid **Đối tượng** (dòng "Mã đối tượng", `business_rules.md:95`) — file 02 |
| **BR7** precision & làm tròn | `helpers/quyDoi.ts`: VND `18,2` · ngoại tệ `18,4` · tỷ giá `18,6`; làm tròn ở **kết quả cuối** — file 02, 03 |
| **BR11** tìm kiếm | Ô "Tìm theo số chứng từ, số hóa đơn" của 2 bảng — file 02 |
| **BR12** trạng thái chứng từ | Chưa ghi sổ / Đã ghi sổ; quy tắc bất biến (đã ghi sổ: không sửa, không xóa) — file 04 |
| **BR13.1 / BR13.2** nút thao tác | Bộ nút theo trạng thái trên danh sách và trên popup xem chi tiết — file 01, 04 |
| **BR14.1** chế độ form | `create` = enabled theo ma trận · `view` = disabled toàn bộ — file 03, 04 |
| **BR14.4** maxLength | Lý do 500 · Số chứng từ 50 · Diễn giải 500 — chặn cứng, không báo lỗi — file 03 |
| **BR15** validation | Bắt buộc, ≥ 0, so sánh; border đỏ + text đỏ + scroll tới lỗi + switch tab — file 02, 03 |
| **BR16** cảnh báo nghiệp vụ | Popup xác nhận Bỏ ghi (`MSG_..._102`), popup chặn (`MSG_..._101`, ngoài phạm vi) — file 04 |
| **BR17** kỳ kế toán | `MSG_..._019` khi Lưu / Ghi sổ / Bỏ ghi — FE hiển thị lỗi BE trả — file 03, 04 |
| **BR18** ngoại tệ | Ẩn hẳn cột Tỷ giá + mọi cột quy đổi khi Loại tiền = đồng tiền hạch toán (BR18.4) — file 02, 03, 04 |
| **BR19 · BR20** trùng & số chứng từ | Số chứng từ ≤ 50 ký tự, không dấu tiếng Việt, kiểm trùng khi Lưu (`MSG_..._015`) — file 03 |
| **BR21** grid chi tiết con | Tab Hạch toán / Chứng từ công nợ — **chỉ đọc**, không có nút Thêm/Xóa dòng (khác mặc định BR21.1, do SCR quy định) — file 03 |
| **BR25** phân quyền | `BuTruCongNo.Create` gác route; `PhieuKeToan.*` gác từng nút; thiếu quyền → **ẩn** — §6 |
| **BR26** toast | Toast thành công/lỗi cho Lưu · Ghi sổ · Bỏ ghi · Xóa — file 03, 04, 05 |
| **BR29** xóa mềm | Xóa là xóa mềm ở BE; FE chỉ gọi + làm mới danh sách — file 05 |
| **BR30** ẩn/hiện cột | Gear cấu hình cột cho 2 bảng chứng từ (`columnConfigKey` + `columnConfigTexts` — `CommonListTable.tsx:571-573`) — file 02 |
| **BR31** dòng tổng | Dòng Tổng ở 2 bảng chứng từ, tab Hạch toán, tab Chứng từ công nợ — file 02, 03 |
| **BR32** copy từ grid | Sẵn có ở `CommonListTable` — không viết thêm |
| **BR33** màu trạng thái | `CommonStatusTag` — file 01, 04 |
| **BR36** ghi sổ không gộp bút toán | Ràng buộc **BE**; FE chỉ gửi đúng số dòng hạch toán đã dựng — file 03 |
| **BR37** đồng bộ Ngày hạch toán ↔ Ngày chứng từ | `hooks/useChungTuBuTruForm.ts` — file 03 |
| **BR42** bỏ ghi sổ | Nút Bỏ ghi chỉ hiện khi Đã ghi sổ; popup xác nhận — file 04 |
| **BR43** trim | Lý do · Số chứng từ · Diễn giải — trim khi blur và trước submit — file 03 |
| **BR44** truncate | `textMode: 'identity'` cho Số chứng từ/Số hóa đơn; `'long'` cho Diễn giải — file 02, 03 |
| **BR46** trường hệ thống | Ràng buộc **BE** (entity) — FE chỉ mang `updatedAt` làm token khoá lạc quan khi Xóa/Ghi sổ — file 06 |

**BR chưa xử lý được trong kế hoạch này:**

| BR | Lý do |
|---|---|
| **BR38** nhóm theo cột · **BR39** xuất Excel | SCR của epic không yêu cầu cho 2 bảng chứng từ; Figma cũng ẩn nút excel/print (node `41383:666551`, `41383:666552` đều `hidden="true"`) |
| **BR45** thao tác hàng loạt | Ghi sổ/Bỏ ghi/Xóa hàng loạt thuộc màn danh sách Phiếu KTTH (ngoài phạm vi, D3) |
| **BR22 · BR23 · BR40** | Không áp dụng — không có dữ liệu dạng cây, không có danh mục trong epic |
| **BR34** sửa từ màn Xem | Không áp dụng — chứng từ bù trừ **không cho sửa** ở mọi trạng thái (`SCR_BTCN_ChungTu_XemChiTiet.md:56`) |
| **BR6** trường tự do dòng hạch toán | Không áp dụng — 2 dòng hạch toán do hệ thống dựng sẵn, SCR không cho nhập Vụ việc/Đơn vị/Khoản mục |

---

## 15. Tài liệu tham chiếu

**Luật & khung**
- [CLAUDE.md](../../../CLAUDE.md) · [client/CLAUDE.md](../../../client/CLAUDE.md) ·
  [docs/fe-khung-kien-truc-chuan.md](../../fe-khung-kien-truc-chuan.md) ·
  [docs/conventions.md](../../conventions.md)
- [pmkt-docs/ba/Common/business_rules.md](../../../pmkt-docs/ba/Common/business_rules.md)

**Tài liệu BA của epic** — `pmkt-docs/ba/PMKT-E-14294_BuTruCongNo/`, đã đọc **toàn bộ**:

| File | Đã dùng vào |
|---|---|
| `1.function-breakdown.md` | Danh sách file con của kế hoạch (§7) |
| `2.usecase.puml` | Đối chiếu 5 UC — không có UC nào ngoài 5 cái đã liệt kê, không có `include`/`extend` |
| `3.crud-matrix.md` | D2 (chứng từ là Phiếu KTTH `LoaiPhieu = 5`), phạm vi entity BE |
| `4.usecases/**/UC_*.md` (5 file) | Luồng chính, luồng phụ, bảng ngoại lệ ⇒ §6/§7 mỗi file con |
| `4.usecases/**/AD_*.puml` (5 file) | Thứ tự kiểm tra khi Ghi sổ (kỳ kế toán **trước**, số dư **sau**) · vị trí popup xác nhận Bỏ ghi (trước khi kiểm kỳ) · **phát hiện mâu thuẫn Q11 / R9** |
| `5.screens/**` (5 file) | Bảng trường, bảng cột, BR của từng màn |
| `6.messages.md` | Nguyên văn 26 message ⇒ nhánh `msg.*` của `vi.ts` ([06 §3.5](06-hop-dong-api-va-i18n.md)) |
| `Matrix/**` (3 ma trận + `_scope.md`) | Mục §3 của mỗi file con |
| *(không có `7.glossary.md`)* | — epic này không có file thuật ngữ |

- Epic nền: `pmkt-docs/ba/PMKT-E-09980_PhieuKTTH/5.screens/SCR_PhieuKTTH/SCR_PhieuKTTH_DanhSach.md`

**Code tham chiếu**
- Module chuẩn **duy nhất**: `client/src/features/banHang/chungTuBanHang/`
- Module cùng domain: `client/src/features/tongHop/khoaSo/` + `client/src/features/tongHop/routes.tsx`
- Barrel: `client/src/base/index.ts` · `client/src/base/domainKit/chungTu/index.ts`
- Router: `client/src/app/router/RootRoutes.tsx` · Menu: `client/src/app/layouts/shell/menuRegistry.tsx`

**Figma** — file `ymMyg329ejsgCWg28CNmGl`, section `41322:649030`:
`41322:651294` Danh sách · `41323:656771` Bù trừ (VND) · `41383:670216` Bù trừ (ngoại tệ) ·
`41383:666955` Thêm mới (VND) · `41667:46774` Thêm mới (ngoại tệ) ·
`41383:672221` + `41697:102387` Tab chứng từ công nợ · `41322:650973` menu ⋮ trên dòng
