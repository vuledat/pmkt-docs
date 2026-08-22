# 01 — Danh sách Chứng từ bù trừ công nợ

| | |
|---|---|
| **Mã màn** | `SCR_BTCN_DanhSach` |
| **UC nguồn** | PMKT-U-14688 — `4.usecases/PMKT-U-14688_BTCN_DanhSach/UC_BTCN_DanhSach.md` |
| **SCR nguồn** | `5.screens/SCR_BTCN_DanhSach.md` — chỉ mô tả **điểm khác biệt** so với `SCR_PhieuKTTH_DanhSach.md` (epic PMKT-E-09980) |
| **Matrix** | **SKIP** — `Matrix/.../_scope.md:10` (màn danh sách, ngoài phạm vi ma trận Ẩn/Hiện) |
| **Figma** | node `41322:651294` "Danh sách" (1440×1024) |
| **Route** | ✅ **ĐÃ CÓ** — `/tong-hop/phieu-ke-toan-tong-hop` (`features/tongHop/phieuKeToanTongHop/constants/paths.ts`) |
| **Phạm vi epic này** | ⛔ **KHÔNG dựng màn này** (quyết định D1/D3 ở [00-ke-hoach-tong.md](00-ke-hoach-tong.md)). File này chốt **hợp đồng tích hợp** để module Phiếu KTTH cắm chứng từ bù trừ vào. |

> **Lý do không dựng:** `SCR_BTCN_DanhSach.md:5` — *"Chứng từ bù trừ công nợ hiển thị chung trên danh
> sách Phiếu kế toán tổng hợp … **không xây màn hình danh sách độc lập**. Toàn bộ bố cục, thành phần
> … theo tài liệu SCR_PhieuKTTH_DanhSach.md — **không mô tả lại**."*
>
> **CẬP NHẬT 2026-08-21 — chặn cứng R1/Q1 đã được gỡ.** Module `features/tongHop/phieuKeToanTongHop/`
> đã được dựng (commit `32b8a6ca`, 28 file): route `/tong-hop/phieu-ke-toan-tong-hop`, dựng trên
> engine `@domain-kit/chungTu` (`defineChungTu` + `ChungTuListPage`), quyền `PhieuKeToan.*`, và **đã
> biết `loaiPhieu = 'BU_TRU_CONG_NO'`** với nhãn "Bù trừ công nợ" (`fields/options.ts:76`).
>
> Quyết định **không dựng lại** màn này vẫn giữ nguyên. Cái đổi là **phần tích hợp ở §8 nay làm được
> ngay** — xem D11/D12 ở [00 §−1](00-ke-hoach-tong.md).

---

## 1. Bố cục (đọc từ Figma `41322:651294`)

```
┌ Sidebar OSP ─┬ Banner ──────────────────────────────────────────────────────┐
│              │ ← ⌂ │ Tổng hợp / Phiếu kế toán tổng hợp                      │
│              ├──────────────────────────────────────────────────────────────┤
│              │ Kết chuyển lãi lỗ │ Báo cáo tài chính │ Khoá sổ kỳ kế toán   │
│              │ │ Bỏ khoá sổ kỳ kế toán │ ▚ Phiếu kế toán tổng hợp ▚         │  ← tab cấp 2
│              ├──────────────────────────────────────────────────────────────┤
│              │ ┌ Card ─────────────────────────────────────────────────────┐│
│              │ │ [+ Thêm mới]      [Tìm kiếm…🔍][⟳][▽][⚙]  1-10 trên 40    ││
│              │ │                                          ‹ [1] › [10/trang]││
│              │ │ ┌──────────────────────────────────────────────────────┐  ││
│              │ │ │ # │Ngày hạch toán│Ngày chứng từ│Số chứng từ│Số tiền│…│  ││
│              │ │ │ 3 │ 12/12/2025   │ 12:00 Thứ 2 │BTCN-…    │5.000.000│ ││
│              │ │ ├─ Tổng:                              30.000.000 ──────┤  ││
│              │ └───────────────────────────────────────────────────────┘  ││
│              │                          ⌄  ← tay nắm mở/đóng panel xem nhanh│
│              │ ┌ Panel xem nhanh ──────────────────────────────────────────┐│
│              │ │ Hạch toán │ Chứng từ công nợ │ Đính kèm │ Tham chiếu      ││
│              │ │                            Số chứng từ: DB-2023-114      ││
│              │ │ # │ Diễn giải │ TN Nợ │ TN Có │ Số tiền                  ││
│              │ │ ─ Tổng: ────────────────────────────────── 15 ───────────││
│              │ │                    1-2 trên 2 ‹ [1] › [20 / trang]       ││
│              │ └───────────────────────────────────────────────────────────┘│
└──────────────┴──────────────────────────────────────────────────────────────┘
```

Điểm đáng chú ý của bố cục: **panel xem nhanh dùng đúng 4 tab của popup chứng từ** (Hạch toán ·
Chứng từ công nợ · Đính kèm · Tham chiếu) — cùng bộ tab với popup ở [file 03](03-popup-chung-tu-bu-tru-them-moi.md),
nên tab `Chứng từ công nợ` phải dùng lại được ở cả hai chỗ (xem §9).

---

## 2. Đặc tả UI từ Figma (tham khảo cho epic 09980)

| Thành phần | Component `@base` dùng lại | Số đo Figma |
|---|---|---|
| Thanh tab cấp 2 (5 tab) | `TabMenu2Level` — `base/index.ts:148` | full-bleed dưới banner, y=100 (theo mẫu `ChungTuBanHangPage.tsx:33-36`) |
| Card danh sách + toolbar | `CommonListTable` (`wrapInCard` mặc định true) — `base/index.ts:316` | card inset 16px |
| Nút Thêm mới | `CommonListTable.onAdd` + `addIcon` — `CommonListTable.tsx:455-457` | primary đỏ |
| Ô tìm kiếm · Reload · Phễu lọc · Bánh răng cấu hình cột | `showSearch` · `showReload` · `showFilter` · `showSettings` — `CommonListTable.tsx:389-393` | 4 nút 32×32, khoảng cách 8 |
| Phân trang | `pagination` — `CommonListTable.tsx:546` | "1-10 trên 40" · `10 / trang` |
| Badge trạng thái | `CommonStatusTag` / `ListTag` — `base/index.ts:593` | "Đã ghi sổ" nền xanh lá nhạt · "Chưa ghi sổ" nền vàng nhạt (BR33) |
| Cột Chức năng: 👁 + ⋮ | `onView` + `rowActions` — `CommonListTable.tsx:485-487` | ghim phải |
| Dòng Tổng | `showSummary` + `ListField.summary:'sum'` — `CommonListTable.tsx:538`, `listTableFormat.ts:80-86` | "Tổng: 30.000.000" |
| Panel xem nhanh | `ChungTuChiTietPanel` — `base/domainKit/chungTu/index.ts:91` | có tay nắm ⌄, phân trang riêng "20 / trang" |

Menu ⋮ trên dòng (node `41322:650973`, 150×144 — 4 mục 142×32):

| Thứ tự | Nhãn | Icon | Điều kiện hiển thị (BR13.1 + `SCR_BTCN_DanhSach.md:34`) | Quyền |
|---|---|---|---|---|
| 1 | Xem chi tiết | 👁 | Luôn | `PhieuKeToan.View.Detail` |
| 2 | Ghi sổ | 🖊 | Trạng thái = **Chưa ghi sổ** | `PhieuKeToan.Post` |
| 3 | Bỏ ghi sổ | ⃠ | Trạng thái = **Đã ghi sổ** | `PhieuKeToan.Unpost` |
| 4 | **Xóa** (đỏ, có gạch phân cách phía trên) | 🗑 | Trạng thái = **Chưa ghi sổ** | `PhieuKeToan.Delete` |

**KHÔNG có mục "Chỉnh sửa"** — `SCR_BTCN_DanhSach.md:33`: *"Không có nút Chỉnh sửa với chứng từ bù trừ
công nợ (không cho sửa; thay đổi bằng cách Bỏ ghi → Xóa → bù trừ lại)"*. Figma cũng không vẽ mục đó.

---

## 3. Ma trận ẩn/hiện · required · disabled

**Không áp dụng** — `_scope.md:10` loại màn này khỏi phạm vi ma trận (màn danh sách, không có trường
nhập liệu). Điều kiện hiển thị nút đã nằm ở §2 (bảng menu ⋮) và tuân BR13.1 · BR42.2.

---

## 4. Bảng cột

Cột do epic 09980 định nghĩa (`SCR_PhieuKTTH_DanhSach.md`). Ghi lại để đối chiếu, kèm **conflict C13**:

| Cột (SCR 09980) | Figma vẽ | Field | Kiểu / định dạng | Sort? | Lọc? | Ghi chú cho chứng từ bù trừ |
|---|---|---|---|---|---|---|
| STT | `#` | — | index | ✗ | ✗ | `showIndex` + `indexOffset = (page-1)*pageSize` (BR2 — STT liên tục qua trang) |
| Số chứng từ | Số chứng từ | `PhieuKeToanTongHop.SoChungTu` | `format:'link'` · `textMode:'identity'` (BR44 nhóm 1) | ✓ | ✓ | Click → mở [04 — Xem chi tiết](04-popup-chung-tu-bu-tru-xem-chi-tiet.md) khi Loại nghiệp vụ = Bù trừ công nợ (`SCR_BTCN_DanhSach.md:29`) |
| Loại nghiệp vụ | Loại nghiệp vụ | `PhieuKeToanTongHop.LoaiPhieu` | badge | ✓ | ✓ | **Phải có giá trị "Bù trừ công nợ"** trong danh sách lọc (`SCR_BTCN_DanhSach.md:19`) |
| Ngày chứng từ | Ngày chứng từ | `.NgayChungTu` | date `DD/MM/YYYY` | ✓ | ✓ | |
| Ngày hạch toán | Ngày hạch toán | `.NgayHachToan` | datetime | ✓ | ✓ | Sắp xếp mặc định: **giảm dần** (BR2) |
| Diễn giải | Diễn giải | `.MoTa` | text · `textMode:'long'` (BR44 nhóm 2) | ✗ | ✓ | |
| **Tổng tiền** | **"Số tiền"** ⚠ C13 | `.TongTien` | currency, `summary:'sum'` | ✓ | ✗ | Với loại "Bù trừ công nợ" = Tổng(Số tiền tab Hạch toán) = Số tiền bù trừ (dòng chênh lệch tỷ giá có nguyên tệ = 0 nên không cộng vào) — `SCR_BTCN_DanhSach.md:20` |
| Trạng thái | Trạng thái | `.TrangThai` | `format:'status'` + `statusRegistry` | ✓ | ✓ | BR33 |
| Chức năng | Chức năng | — | 👁 + ⋮ | ✗ | ✗ | ghim phải |

**Ẩn/hiện cột (BR30)**: `columnConfigKey` riêng cho màn Phiếu KTTH.

---

## 5. Hành vi & sự kiện — phần thuộc epic 14294

| Thao tác | Điều kiện hiện | Việc làm | Confirm | Toast | Invalidate |
|---|---|---|---|---|---|
| **Thêm mới** (nút toolbar) | quyền `PhieuKeToan.Create` | Mở popup Thêm mới Phiếu KTTH **thường** | — | — | — |
| | | ⚠ **KHÔNG tạo được chứng từ bù trừ** — `SCR_BTCN_DanhSach.md:24`, `UC_BTCN_DanhSach.md:16`. Danh sách loại nghiệp vụ của popup đó **không có** "Bù trừ công nợ" | | | |
| **Xem chi tiết** / double-click dòng | quyền `.View.Detail` | Loại nghiệp vụ = Bù trừ công nợ → mở [popup 04](04-popup-chung-tu-bu-tru-xem-chi-tiet.md); loại khác → popup xem chi tiết Phiếu KTTH chung | — | — | — |
| **Ghi sổ** | Chưa ghi sổ + `.Post` | `POST …/{id}/ghi-so` | Không (BR13.2: ghi sổ không hỏi xác nhận) | ✅ `MSG_..._002` · ❌ `MSG_..._017` | danh sách + chi tiết |
| **Bỏ ghi** | Đã ghi sổ + `.Unpost` | Popup xác nhận `MSG_..._102` → `POST …/{id}/bo-ghi-so` | ✅ có | ✅ `MSG_..._003` · ❌ `MSG_..._017` | danh sách + chi tiết + **các chứng từ công nợ liên quan** |
| **Xóa** | Chưa ghi sổ + `.Delete` | Mở [popup 05](05-popup-xac-nhan-xoa.md) | ✅ có | ✅ `MSG_..._004` · ❌ `MSG_..._020` | danh sách |
| **Tải danh sách lỗi** | — | — | — | ❌ `MSG_..._022` | — |
| **Không có dữ liệu** | — | Bảng rỗng | — | ℹ `MSG_..._201` "Không có dữ liệu" | — |
| **Không có quyền `PhieuKeToan.View`** | — | Ẩn menu; vào thẳng URL → trang 403 (BR25.2 · BR27) | — | `MSG_..._005` | — |

**BR29.4** — sau khi Xóa / Ghi sổ / Bỏ ghi, **giữ nguyên trang hiện tại**, không nhảy về trang 1.

---

## 6. Validation phía FE

Không có form ⇒ không có validation nhập liệu. Toàn bộ kiểm tra nghiệp vụ (kỳ kế toán BR17, số dư
`MSG_..._018`, trạng thái `MSG_COMMON_001`) **chỉ BE kiểm**; FE hiển thị lại thông báo BE trả về qua
`describeApiError` (`@platform`) — mẫu dùng: `features/banHang/chungTuBanHang/components/ChungTuBanHangTab.tsx:274-276`.

---

## 7. Luồng xử lý

1. Người dùng mở `Tổng hợp → Phiếu kế toán tổng hợp`.
2. (Tùy chọn) Lọc **Loại nghiệp vụ = "Bù trừ công nợ"** để xem riêng chứng từ bù trừ.
3. Bảng hiển thị theo BR1 (phân trang) · BR2 (sắp xếp) · BR31 (dòng tổng) · BR28 (lọc theo tenant).
4. Chọn một dòng → panel xem nhanh nạp `GET …/{id}`, hiển thị tab Hạch toán / Chứng từ công nợ.
5. Thao tác trên dòng theo §5.
6. Loading: skeleton của `CommonListTable`; Empty: `MSG_..._201`; Error: toast `MSG_..._022`.

---

## 8. Phân bổ file

⛔ **Epic này không sinh file cho màn danh sách.** Bảng dưới là **hợp đồng bàn giao** cho module
Phiếu KTTH (epic 09980):

| Việc | Ai sở hữu | File |
|---|---|---|
| Khung danh sách, toolbar, phân trang, panel xem nhanh, máy trạng thái nút | **epic 09980** | `features/tongHop/phieuKeToanTongHop/` (đề xuất) — nên dựng trên engine `@domain-kit/chungTu` (`ChungTuListPage` + `defineChungTu`), engine đã lo đúng bộ này |
| Hằng số `LOAI_NGHIEP_VU.BU_TRU_CONG_NO` | **epic 14294** | `buTruCongNo/constants/constants.ts` |
| Popup Xem chi tiết chứng từ bù trừ (mode `view`) | **epic 14294** | `buTruCongNo/components/ChungTuBuTruModal.tsx`, export qua `buTruCongNo/index.ts` |
| Tab "Chứng từ công nợ" (cặp ghép) dùng cho **cả** panel xem nhanh lẫn popup | **epic 14294** | `buTruCongNo/components/ChungTuCongNoTab.tsx` + `fields/chungTuCongNoColumns.ts` |
| Hook Ghi sổ / Bỏ ghi / Xóa chứng từ bù trừ | **epic 14294** | `buTruCongNo/hooks/useBuTruActions.ts` |
| Popup xác nhận Xóa / Bỏ ghi | **epic 14294** | `buTruCongNo/components/XacNhanBuTruModal.tsx` |
| Chữ i18n riêng của chứng từ bù trừ trên danh sách | **epic 14294** | `buTruCongNo/i18n/vi.ts` — nhánh `danhSach.*` |

### Cách nối — ĐÃ CHỐT (D11/D12, cập nhật 2026-08-21)

Ràng buộc tầng là thật và SSOT nói rõ: *"sibling leaves stay sealed"*
(`eslint.boundaries.js:89-100`) — `leaf` chỉ với được tầng dưới, `_shared` của **chính domain mình**,
và `_shared` của chính mình. Nên `phieuKeToanTongHop` **không được** import popup của `buTruCongNo`.

**Không** chuyển popup xuống `_shared/` (sẽ moi rỗng cả leaf). Thay vào đó nối bằng **URL**:

| Bên | Làm gì |
|---|---|
| `buTruCongNo` | Mở thêm route `/tong-hop/bu-tru-cong-no/:id` → `BuTruCongNoPage` chế độ `view` |
| `tongHop/_shared/constants/paths.ts` | Hằng đường dẫn cấp domain, để hai leaf dùng **cùng một** chuỗi (`leaf → domain _shared` là đường luật tầng cho phép) |
| `phieuKeToanTongHop` | `usePhieuKttHPage.moForm(row)`: `row?.loaiPhieu === 'BU_TRU_CONG_NO'` ⇒ `navigate(...)`; các loại phiếu khác giữ nguyên toast "chưa hỗ trợ". **Diff đúng một hàm** |

Chỗ nối này vốn đã được chừa sẵn trong module bạn — chú thích của `moForm` ghi *"Popup thuộc ĐỢT SAU"*.

---

## 9. Kiểm thử

Epic này không sinh test cho màn danh sách. Ba ca dưới đây là **điều kiện nghiệm thu tích hợp**, chạy
khi module Phiếu KTTH lên:

| # | Input | Kỳ vọng |
|---|---|---|
| T1 | Dòng có `LoaiPhieu = 'Bù trừ công nợ'`, trạng thái `Chưa ghi sổ`, user đủ 4 quyền | Menu ⋮ có đúng **Xem chi tiết · Ghi sổ · Xóa**; **không** có "Chỉnh sửa", **không** có "Bỏ ghi sổ" |
| T2 | Cùng dòng, trạng thái `Đã ghi sổ` | Menu ⋮ có đúng **Xem chi tiết · Bỏ ghi sổ**; **không** có Ghi sổ / Xóa / Chỉnh sửa |
| T3 | Double-click dòng bù trừ | Mở popup của module `buTruCongNo` ở `mode='view'`, **không** mở popup xem chi tiết Phiếu KTTH chung |

---

## 10. BR đã áp dụng

BR1 (phân trang) · BR2 (sắp xếp mặc định, STT liên tục, checkbox sau STT, sticky header, ghim cột
Chức năng) · BR11 (tìm kiếm & lọc) · BR12 (vòng đời trạng thái) · BR13.1 (điều kiện hiện nút + Reload
+ double-click mở chi tiết) · BR25 (ẩn nút khi thiếu quyền) · BR26 (toast) · BR27 (trang 403) ·
BR28 (multi-tenant) · BR29.4 (giữ nguyên trang sau sửa/xóa) · BR30 (ẩn/hiện cột) · BR31 (dòng tổng) ·
BR32 (copy từ grid) · BR33 (màu trạng thái) · BR42.2 (ẩn nút Bỏ ghi với dòng Chưa ghi sổ) ·
BR44 (truncate: `identity` cho Số chứng từ, `long` cho Diễn giải).

**Chưa xử lý:** BR38 (nhóm cột) · BR39 (xuất Excel) · BR45 (thao tác hàng loạt) — không có trong SCR
của epic 14294 và thuộc quyết định của epic 09980.
