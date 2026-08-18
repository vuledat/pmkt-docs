# 02 — Popup Bù trừ công nợ (thiết lập)

| | |
|---|---|
| **Mã màn** | `SCR_BTCN_BuTru` |
| **UC nguồn** | PMKT-U-14690 — `UC_BTCN_ThemMoi.md` (AC2, AC3, AC4 · LP1, LP2) |
| **SCR nguồn** | `5.screens/SCR_BTCN_BuTru.md` |
| **Matrix** | `Matrix/PMKT-E-14294_BuTruCongNo/SCR_BTCN_BuTru_MaTranAnHien.md` |
| **Figma** | `41323:656771` (Loại tiền = đồng tiền hạch toán) · `41383:670216` (Loại tiền ≠ ĐTHT) |
| **Route** | `/tong-hop/bu-tru-cong-no` — quyền `BuTruCongNo.Create` |
| **Component gốc** | `components/BuTruCongNoModal.tsx` |

> **Đây là POPUP, không phải trang.** Figma dựng nó là `Dialog Box` (node `41323:660608`) nằm trong
> `Overlay` phủ toàn màn hình (node `41323:657388`) — SCR không nói rõ điều này, Figma nói.

---

## 1. Bố cục

```
Overlay 1440×1024
└ Dialog Box  1392×988  @ (24,24)              ← lề 24px mọi phía
  ├ Modal Header            1392×56            "Bù trừ công nợ"   [?] [×]
  ├ Modal Body              1392×876
  │ ├ Thẻ Header Filter     1360×82  @ (16,8)
  │ │ └ Form                1328×58  @ (+16,+12)
  │ │   Đối tượng 816 · TK phải thu 86 · TK phải trả 86 · Ngày bù trừ 121
  │ │   · Loại tiền 86 · [Lấy dữ liệu] 92          (gap 8 giữa các ô)
  │ ├ Thẻ "Chứng từ phải thu"  1360×357 @ (16,98)
  │ │ ├ Section Title       1328×32  @ (+16,+12)
  │ │ │   tiêu đề 132×24 (trái)  ·  [Tìm kiếm 219×32][⟳ 32×32] @ x=1069 (phải)
  │ │ ├ Bảng                1328×216 @ (+16,+52)
  │ │ ├ Summary Row         1328×36  @ y=+217 (trong khối bảng)
  │ │ ├ Action Bar          1328×32  @ y=+261 → phân trang ghim phải (336px)
  │ │ └ Scrollbar dọc       8px      @ x=1350
  │ ├ Thẻ "Chứng từ phải trả"  1360×357 @ (16,463)      ← gap 8 giữa 2 thẻ
  │ │   (cấu trúc y hệt thẻ trên)
  │ └ Dải "Số tiền bù trừ"  1360×40  @ (16,828)   ← nhãn + số, canh PHẢI, số màu xanh lá
  └ ModelFooter             1392×56  @ y=932      [Hủy] ················ [Bù trừ]
```

Nút **Hủy** trái (mặc định), **Bù trừ** phải (primary đỏ) — đúng BR3 (*"nút xác nhận luôn ở bên phải,
nút hủy/đóng luôn ở bên trái"*).

---

## 2. Đặc tả UI từ Figma

| Thành phần | Component `@base` dùng lại | Kích thước / spacing (Figma) | Ghi chú |
|---|---|---|---|
| Khung popup | `CommonModalShell` `mode='custom'` — `base/index.ts:264` | `width = 1392` → token mới `MODAL_WIDTH_WIDE` (D10, Q7) | `maskClosable=false` (mặc định — bảo vệ nhập liệu), `dirty`+`discardConfirm` bật khi đã tick/nhập |
| Header popup | `CommonModalHeader` — `base/index.ts:277` | h=56; tiêu đề trái, `[?]` + `[×]` phải | `[?]` = trợ giúp — chưa có đặc tả nội dung → xem Q ở file 00 |
| Thẻ Header Filter | `Card` — `base/index.ts:158` | 1360×82, padding 16/12 | |
| Nhãn có `*` | `FieldLabel` — `base/index.ts:194` | | |
| Đối tượng | `CommonComboGrid` — `base/index.ts:568` | w=**816**, h=32 | BR5 dòng "Mã đối tượng" (`business_rules.md:95`) |
| TK phải thu / TK phải trả | `CommonSelectBox` — `base/index.ts:578` | w=**86** mỗi ô | SCR ghi Dropdown; BR5 xếp TK vào combogrid → **Q10** |
| Ngày bù trừ | `CommonDateInput` — `base/index.ts:170` | w=**121** | định dạng `DD/MM/YYYY` (mẫu Figma `31/01/2026`) |
| Loại tiền | `CommonSelectBox` | w=**86** | |
| Nút Lấy dữ liệu | `CommonButton` — `base/index.ts:53` | w=**92**, h=32, nền **đen/tối** (không phải đỏ primary) | Design xác nhận biến thể nút này |
| Tiêu đề thẻ bảng | `CommonListTable` prop `title` — `CommonListTable.tsx:559` | text 24px cao, w≈132 ("Chứng từ phải thu") / 129 ("Chứng từ phải trả") | |
| Ô tìm kiếm | `showSearch` + `onSearch` — `CommonListTable.tsx:389,399` | 219×32, placeholder "Tìm kiếm…" | SCR ghi placeholder *"Tìm theo số chứng từ, số hóa đơn"* → lấy **theo SCR** |
| Nút Reload | `showReload` + `onReload` — `CommonListTable.tsx:392,447` | 32×32, cách ô tìm kiếm 8px | |
| Nút Excel / Print / Import | — | **`hidden="true"`** trong Figma (node `41383:666551`, `666552`, `666553`) | ⇒ **không dựng** (BR39 không áp cho màn này) |
| Bảng | `CommonListTable` | vùng 1328×216 (≈5 dòng + header) | |
| Dòng Tổng | `showSummary` + `summaryScope='all'` — `CommonListTable.tsx:538-543` | 1328×36, nền xám nhạt, nhãn "Tổng:" | BR31; `'all'` = tính trên **toàn bộ** tập, không phải trang hiện tại |
| Phân trang | `pagination` — `CommonListTable.tsx:546` | thanh 1328×32, cụm phải rộng 336: "1-10 trên 40" ‹ [1] › `10 / trang` | BR1 |
| Dải "Số tiền bù trừ" | Khối riêng (`components/BuTruCongNoModal.tsx`) | 1360×40, nhãn + số canh **phải**, số màu **xanh lá** | Vị trí conflict → **C10 / Q5** |
| Footer | `CommonModalFooter` / `ModelFooter` — `base/index.ts:271,295` | h=56 | |

**Chưa xác định từ Figma** (cần Design chốt — Q9): độ rộng từng cột của 2 bảng. Metadata chỉ cho tổng
vùng bảng 1328px; ở biến thể ngoại tệ 15 cột **tràn ra ngoài** hộp thoại trong chính mock
(`41383:670216`).

---

## 3. Ma trận ẩn/hiện · required · disabled

Dịch **nguyên vẹn** từ `SCR_BTCN_BuTru_MaTranAnHien.md:32-52`. Trục cột duy nhất = **Loại tiền**.

`Show` = hiện & nhập được · `Hide` = **không render** · `Disable` = hiện, read-only.

| Vùng | Thành phần | C1 (Loại tiền = ĐTHT) | C2 (Loại tiền ≠ ĐTHT) |
|---|---|:--:|:--:|
| Header Filter | Đối tượng · TK phải thu · TK phải trả · Ngày bù trừ · Loại tiền | Show | Show |
| Header Filter | Nút **Lấy dữ liệu** | Show | Show |
| Header Filter | **Số tiền bù trừ** (nhãn = MIN 2 bảng) | Disable | Disable |
| Bảng phải thu | Ô tìm kiếm · Checkbox chọn tất cả (header) | Show | Show |
| Bảng phải thu | Checkbox chọn dòng | Show | Show |
| Bảng phải thu | **Số tiền bù trừ** (ô nhập trong lưới) | Show | Show |
| Bảng phải thu | Ngày chứng từ · Số chứng từ · Số hóa đơn · Hạn thanh toán · Diễn giải · Số tiền · **Số chưa thu** · Loại chứng từ | Disable | Disable |
| Bảng phải thu | **Tỷ giá** | **Hide** | Disable |
| Bảng phải thu | Số tiền quy đổi · Số chưa thu quy đổi · Số tiền bù trừ quy đổi | **Hide** | Disable |
| Bảng phải thu | Dòng Tổng (Số tiền · Số chưa thu · Số tiền bù trừ) | Disable | Disable |
| Bảng phải trả | Ô tìm kiếm · Checkbox chọn tất cả (header) | Show | Show |
| Bảng phải trả | Checkbox chọn dòng | Show | Show |
| Bảng phải trả | **Số tiền bù trừ** (ô nhập trong lưới) | Show | Show |
| Bảng phải trả | Ngày chứng từ · Số chứng từ · Số hóa đơn · Hạn thanh toán · Diễn giải · Số tiền · **Số còn nợ** · Loại chứng từ | Disable | Disable |
| Bảng phải trả | **Tỷ giá** | **Hide** | Disable |
| Bảng phải trả | Số tiền quy đổi · Số còn nợ quy đổi · Số tiền bù trừ quy đổi | **Hide** | Disable |
| Bảng phải trả | Dòng Tổng (Số tiền · Số còn nợ · Số tiền bù trừ) | Disable | Disable |
| Nút hoạt động | **Bù trừ** · **Hủy** | Show | Show |

**Đọc ma trận thành code** — `helpers/anHien.ts`:

```ts
export interface CoBuTru {
  /** Loại tiền ≠ đồng tiền hạch toán ⇒ render khối cột quy đổi. */
  coQuyDoi: boolean
}
export function tinhCoBuTru(loaiTienId: string, dongTienHachToanId: string): CoBuTru
```

`coQuyDoi = false` ⇒ **lọc bỏ hẳn** 4 cột (`Tỷ giá`, `… quy đổi` ×3) ra khỏi mảng `ListField[]`,
**không** render rồi ẩn bằng CSS — ma trận ghi `Hide` = *"Ẩn hẳn, không render"*
(`SCR_BTCN_BuTru_MaTranAnHien.md:26`), và BR18.4 cũng bắt "Ẩn".

**Không lên trục cột** (theo Ghi chú của ma trận, `:60-63`):
- Tick checkbox chỉ **đổi giá trị** ô Số tiền bù trừ (BR02), không đổi Ẩn/Hiện/Disable.
- Ràng buộc `≥ 0` và `≤ Số chưa thu / Số còn nợ` là **ràng buộc giá trị**, không đổi trạng thái hiển thị.

---

## 4. Bảng cột — Chứng từ phải thu / phải trả

Một mảng cột duy nhất, sinh bởi `fields/buTruColumns.ts` → `buTruColumns(ben, { coQuyDoi, t, locale })`.
Cột `#` (STT) do `CommonListTable` tự thêm (`showIndex`), cột checkbox do `selectable` tự thêm.

| # | Tên hiển thị | Khoá i18n (`buTruCongNo:`) | Field API (đề xuất) | Kiểu / định dạng | Sort | Lọc | Ẩn/hiện mặc định | Ghi chú |
|---|---|---|---|---|:--:|:--:|---|---|
| 0 | (checkbox) | — | — | `selectable` của bảng | ✗ | ✗ | Hiện | `preserveSelectedRowKeys` — giữ tick qua trang/tìm kiếm |
| 1 | **Ngày hạch toán** ⚠C5 | `buTru.cot.ngayHachToan` | `ngayHachToan` | date `DD/MM/YYYY` | ✓ | ✗ | Hiện | **Chỉ Figma có**, SCR không liệt kê → **Q4.1** |
| 2 | Ngày chứng từ | `buTru.cot.ngayChungTu` | `ngayChungTu` | date | ✓ | ✗ | Hiện | Sắp xếp mặc định ↑ (BR2 + `SCR_BTCN_BuTru.md:44`) |
| 3 | Số chứng từ | `buTru.cot.soChungTu` | `soChungTu` | `format:'link'` · `textMode:'identity'` | ✓ | ✗ | Hiện | Link mở chứng từ gốc (tab/popup mới) |
| 4 | Số hóa đơn | `buTru.cot.soHoaDon` | `soHoaDon` | text · `identity` | ✗ | ✗ | Hiện | |
| 5 | Hạn thanh toán ⚠C6 | `buTru.cot.hanThanhToan` | `hanThanhToan` | date | ✓ | ✗ | Hiện | Figma biến thể ngoại tệ ghi nhầm "Hạn hạch toán" → **theo SCR** |
| 6 | Diễn giải | `buTru.cot.dienGiai` | `dienGiai` | text · `textMode:'long'` | ✗ | ✗ | Hiện | BR44 nhóm 2 — clamp 2 dòng + tooltip |
| 7 | Tỷ giá | `buTru.cot.tyGia` | `tyGia` | number, **6 chữ số thập phân** (BR7.1) | ✗ | ✗ | **Chỉ khi `coQuyDoi`** | |
| 8 | Số tiền | `buTru.cot.soTien` | `soTien` | currency, `summary:'sum'` | ✓ | ✗ | Hiện | |
| 9 | Số tiền quy đổi | `buTru.cot.soTienQuyDoi` | *(FE tính)* | currency | ✗ | ✗ | **Chỉ khi `coQuyDoi`** | `= soTien × tyGia`, BR7 |
| 10 | **Số chưa thu** (phải thu)<br>**Số còn nợ** (phải trả) ⚠C7 | `buTru.cot.soChuaThu` / `buTru.cot.soConNo` | `soChuaThu` / `soConNo` | currency, `summary:'sum'` | ✓ | ✗ | Hiện | BE tính (`SCR_BTCN_BuTru.md:43,74`); FE **không** tự tính |
| 11 | Số chưa thu quy đổi / Số còn nợ quy đổi | `buTru.cot.soChuaThuQuyDoi` / `…soConNoQuyDoi` | *(FE tính)* | currency | ✗ | ✗ | **Chỉ khi `coQuyDoi`** | |
| 12 | **Số tiền bù trừ** | `buTru.cot.soTienBuTru` | `ChiTietBuTruCongNo_ChungTu.SoTienBuTruPhaiThu` / `…PhaiTra` | **ô nhập** `CommonNumberInput`, `summary:'sum'` | ✗ | ✗ | Hiện | Cột **duy nhất** nhập được — xem §6 |
| 13 | Số tiền bù trừ quy đổi | `buTru.cot.soTienBuTruQuyDoi` | *(FE tính)* | currency | ✗ | ✗ | **Chỉ khi `coQuyDoi`** | |
| 14 | Loại chứng từ | `buTru.cot.loaiChungTu` | `loaiChungTu` | text | ✗ | ✗ | Hiện | Tên theo BR09 (`business_rules.md:222+`) — BE trả tên, FE **không** map mã |

**Precision (BR7.1)** — `helpers/quyDoi.ts` là điểm định dạng duy nhất:
tiền VND `decimal(18,2)` · ngoại tệ `decimal(18,4)` · tỷ giá `decimal(18,6)`.
Làm tròn ở **kết quả cuối cùng** của phép tính (BR7.2), giữ giá trị đầy đủ trong state (BR7.3).

**Ẩn/hiện cột (BR30):** bật gear cấu hình cột cho cả 2 bảng —
`columnConfigKey: 'buTruCongNo.phaiThu' | 'buTruCongNo.phaiTra'` + `columnConfigTexts`
(`CommonListTable.tsx:571-573`). Cột `Số tiền bù trừ` đặt `lockColumn: true`
(`listTableFormat.ts:36-41`) để không ẩn được — ẩn nó thì màn mất chức năng.

---

## 5. Header Filter — bảng trường

| Trường | Control | Field | Max | Bắt buộc | Mặc định | Sửa được | Ghi chú |
|---|---|---|---|:--:|---|:--:|---|
| Đối tượng | `CommonComboGrid` | `BuTruCongNo.DoiTuongId` | — | **Y** | — | Y | Chỉ đối tượng **vừa là khách hàng vừa là nhà cung cấp** (`SCR_BTCN_BuTru.md:28`) ⇒ BE lọc, FE gửi cờ |
| TK phải thu | `CommonSelectBox` | `BuTruCongNo.TaiKhoanPhaiThuId` | — | **Y** | `131`; nếu 131 có TK con → **TK con đầu tiên** | Y | Danh sách TK con có theo dõi khách hàng |
| TK phải trả | `CommonSelectBox` | `BuTruCongNo.TaiKhoanPhaiTraId` | — | **Y** | `331`; nếu 331 có TK con → **TK con đầu tiên** | Y | Danh sách TK con có theo dõi nhà cung cấp |
| Ngày bù trừ | `CommonDateInput` | `BuTruCongNo.NgayBuTru` | — | **Y** ⚠C9 | **Ngày hiện tại** | Y | Figma thiếu dấu `*` → **Q5.1** |
| Loại tiền | `CommonSelectBox` | `PhieuKeToanTongHop.LoaiTienId` | — | **Y** | **Đồng tiền hạch toán** | Y | Đổi giá trị ⇒ đổi khối cột quy đổi (§3) |
| **Số tiền bù trừ** | nhãn chỉ đọc | — | — | — | `0` | N | `= MIN(Tổng bù trừ phải thu, Tổng bù trừ phải trả)`, cập nhật **tức thời** |

Hằng số `TK_PHAI_THU_MAC_DINH = '131'`, `TK_PHAI_TRA_MAC_DINH = '331'` → `constants/constants.ts`
(luật 1: không hardcode magic value).

---

## 6. Hành vi & sự kiện

### 6.1. Nút **Lấy dữ liệu** (BR01 của SCR)

| | |
|---|---|
| Điều kiện hiện | Luôn |
| Điều kiện disable | Đang có request nạp dữ liệu |
| Việc làm | Validate 5 trường bắt buộc → `POST /api/tong-hop/bu-tru-cong-no/lay-du-lieu` → nạp **cả 2 bảng** |
| Thiếu trường bắt buộc | Chặn, **highlight trường thiếu**, toast lỗi **MSG_PMKT-E-14294_006** |
| Bảng rỗng | Hiển thị empty state với **MSG_PMKT-E-14294_201** ("Không có dữ liệu") |
| Nạp lại | **Reset toàn bộ** tick + Số tiền bù trừ đã nhập (dữ liệu nguồn đổi ⇒ phân bổ cũ vô nghĩa) |

### 6.2. Tick / untick checkbox — phân bổ tự động (BR02)

Thuật toán ở `helpers/phanBo.ts`, **thuần**, không React, không mạng, không `t()`:

```ts
export interface DongBuTru { id: string; soDu: number; soTienBuTru: number }

/** BR02 — chứng từ phải thu là NGUỒN, chứng từ phải trả là ĐÍCH phân bổ. */
export function phanBoTuDong(
  phaiThuDaTick: readonly DongBuTru[],
  phaiTraDaTick: readonly DongBuTru[],   // theo ĐÚNG thứ tự hiển thị, TOÀN BỘ danh sách đã nạp
): Map<string, number>                    // id dòng phải trả → số tiền phân bổ
```

Các bước (dịch từ `SCR_BTCN_BuTru.md:120-127`):

1. `nguonConLai = Σ soTienBuTru` của các dòng **phải thu đã tick**.
2. Duyệt các dòng **phải trả đã tick** theo thứ tự hiển thị **trên toàn bộ danh sách đã nạp**
   (không giới hạn trang hiện tại — đây là lý do của D6):
   `phanBo = MIN(nguonConLai, soDu)`; ghi vào `Số tiền bù trừ`; `nguonConLai -= phanBo`.
3. Dừng khi `nguonConLai = 0` hoặc hết dòng đã tick.
4. Sau mỗi lần phân bổ, **Tổng 2 bảng luôn bằng nhau**.

Ba quy tắc kèm theo:

| Tình huống | Xử lý |
|---|---|
| Tick 1 dòng **phải thu** | `Số tiền bù trừ` của dòng đó tự điền `= Số chưa thu` (`SCR_BTCN_BuTru.md:63`) |
| Untick 1 dòng | `Số tiền bù trừ` của dòng đó về `0` |
| Tick 1 dòng **phải trả** | Chạy lại toàn bộ `phanBoTuDong` (dòng đó nhận `MIN(Số còn nợ, nguồn còn lại)`) |
| Người dùng **sửa tay** rồi tick/untick dòng khác | Chạy lại `phanBoTuDong` — **ghi đè** giá trị sửa tay (`SCR_BTCN_BuTru.md:126`: *"sau khi sửa tay, hệ thống không tự phân bổ lại **cho đến lần tick/untick tiếp theo**"*) |
| Checkbox "chọn tất cả" ở header | Chọn/bỏ chọn **các dòng trong trang hiện tại** (`SCR_BTCN_BuTru.md:46`), rồi chạy lại phân bổ |

### 6.3. Sửa tay ô **Số tiền bù trừ** (LP2)

| | |
|---|---|
| Điều kiện | Luôn nhập được (kể cả dòng chưa tick — SCR không cấm; nhập > 0 ở dòng chưa tick → **Q**: có tự tick không? kế hoạch tạm **không** tự tick) |
| Ràng buộc | `≥ 0` (**MSG_..._012**) · `≤ Số chưa thu` (**MSG_..._010**) / `≤ Số còn nợ` (**MSG_..._011**) |
| Cách chặn | Chặn **ngay tại ô** (`CommonNumberInput` với `min=0`, `max=soDu`) — UC ghi *"Chặn nhập"* (`UC_BTCN_ThemMoi.md:115-116`), không phải chặn khi bấm nút |
| Sau khi sửa | Cập nhật lại dòng Tổng 2 bảng + ô "Số tiền bù trừ"; **không** tự phân bổ lại |

### 6.4. Ô tìm kiếm mỗi bảng

Lọc theo **số chứng từ, số hóa đơn** (`SCR_BTCN_BuTru.md:40`). Lọc client-side trên tập đã nạp (D6).
**Tick và Số tiền bù trừ được giữ nguyên** khi lọc — `preserveSelectedRowKeys`
(`CommonListTable.tsx:523`) lo phần tick; phần số tiền nằm trong state của hook nên vốn không mất.

### 6.5. Nút **Reload** mỗi bảng

BR13.1 (Reload giữ nguyên lọc/tìm kiếm/phân trang/sắp xếp). Ở đây = gọi lại `lay-du-lieu`.
⚠ **Cảnh báo UX:** reload sẽ **mất phân bổ đang làm dở** → phải có popup xác nhận nếu đã tick
(BR3 "Xác nhận đóng form có thay đổi") → **Q**: BA xác nhận hành vi này.

### 6.6. Nút **Bù trừ** (BR03 + BR04)

Kiểm tra theo thứ tự, dừng ở lỗi đầu tiên (`helpers/kiemTra.ts`):

| Thứ tự | Điều kiện | Message khi vi phạm |
|---|---|---|
| 1 | Đã bấm **Lấy dữ liệu** | **MSG_PMKT-E-14294_013** |
| 2 | Đã tick ≥ 1 chứng từ **phải thu** | **MSG_PMKT-E-14294_008** |
| 3 | Đã tick ≥ 1 chứng từ **phải trả** | **MSG_PMKT-E-14294_009** |
| 4 | Tổng Số tiền bù trừ 2 bảng **bằng nhau** | **MSG_PMKT-E-14294_007** |
| 5 | Nếu `coQuyDoi` **và** tổng quy đổi 2 bảng lệch → đã cấu hình TK chênh lệch lãi (515) / lỗ (635) | **MSG_PMKT-E-14294_016** |

Hợp lệ → **không gọi API**, chỉ dựng dữ liệu trong bộ nhớ (`helpers/ghepCap.ts` + `helpers/hachToan.ts`)
rồi mở [popup 03](03-popup-chung-tu-bu-tru-them-moi.md) đè lên (`zIndex` cao hơn).

⚠ Điều kiện 5 cần **dữ liệu cấu hình TK chênh lệch tỷ giá** — FE phải có endpoint đọc cấu hình đó
(xem [06 §1](06-hop-dong-api-va-i18n.md)); nếu BE không cấp, việc kiểm này lùi về BE ở bước Lưu.

### 6.7. Nút **Hủy** / `×` / `Esc`

Chưa thao tác gì → đóng ngay. Đã tick/nhập → popup xác nhận đóng theo BR3
(*"Dữ liệu đã có thay đổi. Bạn có chắc chắn muốn đóng? Thay đổi sẽ không được lưu."*).
Dùng `dirty` + `discardConfirm` của `CommonModalShell` (`CommonModalShell.tsx:51-52`), **không** tự viết.

---

## 7. Validation phía FE

| # | Luật | Điều kiện | Thông báo (nguyên văn) | BR nguồn | Ai kiểm |
|---|---|---|---|---|---|
| V1 | 5 trường Header Filter bắt buộc | trống khi bấm Lấy dữ liệu | *"Vui lòng nhập đầy đủ các trường bắt buộc"* (`MSG_..._006`) | BR15.1 | **FE** |
| V2 | Chưa Lấy dữ liệu | bấm Bù trừ | *"Vui lòng bấm "Lấy dữ liệu" để nạp chứng từ"* (`MSG_..._013`) | — | **FE** |
| V3 | ≥ 1 chứng từ phải thu | bấm Bù trừ | *"Vui lòng chọn ít nhất 1 chứng từ phải thu"* (`MSG_..._008`) | — | **FE** |
| V4 | ≥ 1 chứng từ phải trả | bấm Bù trừ | *"Vui lòng chọn ít nhất 1 chứng từ phải trả"* (`MSG_..._009`) | — | **FE** |
| V5 | Tổng 2 bảng bằng nhau | bấm Bù trừ | *"Tổng số tiền bù trừ ở 2 bảng (Chứng từ phải thu và Chứng từ phải trả) phải bằng nhau"* (`MSG_..._007`) | — | **FE** |
| V6 | Số tiền bù trừ ≥ 0 | nhập tay | *"Số tiền bù trừ không được âm"* (`MSG_..._012`) | BR15.2 (Số ≥ 0) | **FE** — chặn tại ô |
| V7 | ≤ Số chưa thu | nhập tay, bảng phải thu | *"Số tiền bù trừ không được vượt quá Số chưa thu"* (`MSG_..._010`) | — | **FE** — chặn tại ô |
| V8 | ≤ Số còn nợ | nhập tay, bảng phải trả | *"Số tiền bù trừ không được vượt quá Số còn nợ"* (`MSG_..._011`) | — | **FE** — chặn tại ô |
| V9 | Cấu hình TK chênh lệch tỷ giá | ngoại tệ + lệch quy đổi | *"Chưa cấu hình tài khoản xử lý chênh lệch tỷ giá lãi/lỗ. Vui lòng kiểm tra cấu hình"* (`MSG_..._016`) | — | **FE nếu có endpoint cấu hình, ngược lại BE** |

**Chỉ BE kiểm, FE chỉ hiển thị lỗi trả về:**
`Số chưa thu` / `Số còn nợ` (công thức nhiều nguồn — `SCR_BTCN_BuTru.md:43,74`) ·
số dư đổi giữa chừng (`MSG_..._018`) · kỳ kế toán (`MSG_..._019`, BR17) · quyền (`MSG_..._005`).

Hiển thị lỗi theo BR15.4: border đỏ + text đỏ dưới ô + scroll tới ô lỗi đầu tiên.

---

## 8. Luồng xử lý

1. Route `/tong-hop/bu-tru-cong-no` → `BuTruCongNoPage` side-effect import `registerBuTruCongNoI18n`,
   render `<BuTruCongNoModal open />`.
2. `useBuTruSetup()` khởi tạo header filter: `TK phải thu = 131` (hoặc TK con đầu tiên),
   `TK phải trả = 331`, `Ngày bù trừ = hôm nay`, `Loại tiền = đồng tiền hạch toán`.
   Nguồn dữ liệu: `queries.useLookups()` (đối tượng · TK · loại tiền · đồng tiền hạch toán).
3. Người dùng chọn Đối tượng (combogrid, tìm kiếm server-side theo BR5) → bấm **Lấy dữ liệu**.
4. `queries.useLayDuLieu()` → 2 mảng dòng. Loading: `loading` của `CommonListTable`.
   Rỗng: empty state `MSG_..._201`. Lỗi: toast + giữ nguyên trạng thái cũ.
5. Tick / untick / sửa tay → `helpers/phanBo.ts` chạy đồng bộ trong hook, cập nhật state.
6. Ô "Số tiền bù trừ" = `MIN(tổng phải thu, tổng phải trả)`, tính lại mỗi lần state đổi.
7. Bấm **Bù trừ** → `helpers/kiemTra.ts` (§6.6) → hợp lệ thì `helpers/ghepCap.ts` +
   `helpers/hachToan.ts` dựng dữ liệu → `setChungTuMoOpen(true)` mở popup 03.
8. Popup 03 bấm **Hủy** → quay lại popup này, **giữ nguyên toàn bộ dữ liệu đã thiết lập**
   (`UC_BTCN_ThemMoi.md:99-100`) ⇒ state nằm ở `useBuTruSetup` của popup này, **không** ở popup 03.
9. Popup 03 **Lưu** thành công → đóng **cả hai** popup, điều hướng về danh sách và làm mới
   (`SCR_BTCN_ChungTu_ThemMoi.md:104`).

---

## 9. Phân bổ file

| Việc | File |
|---|---|
| Khung popup, ghép 3 khối, footer, `dirty` guard | `components/BuTruCongNoModal.tsx` |
| Hàng lọc trên cùng (6 ô) | `components/BuTruHeaderFilter.tsx` |
| Bảng chứng từ (dùng chung 2 bên, prop `ben`) | `components/ChungTuBuTruTable.tsx` |
| Mô tả cột 2 bảng (hàm theo `ben` + `coQuyDoi`) | `fields/buTruColumns.ts` |
| `texts` cho `CommonListTable` / `CommonComboGrid` | `fields/texts.ts` |
| Option Loại tiền / TK | `fields/options.ts` |
| Kiểu `DongBuTru`, `BenBuTru`, `BuTruSetupState` | `fields/types.ts` |
| **BR02 — phân bổ tự động** | `helpers/phanBo.ts` |
| Quy đổi + làm tròn BR7 | `helpers/quyDoi.ts` |
| Cờ ẩn/hiện theo Loại tiền (§3) | `helpers/anHien.ts` |
| BR01/BR03/BR04 — điều kiện Lấy dữ liệu & Bù trừ | `helpers/kiemTra.ts` |
| State filter + 2 bảng + tick + phân bổ + tổng | `hooks/useBuTruSetup.ts` |
| `POST …/lay-du-lieu`, lookup, Zod parse | `api/buTruCongNoApi.ts` · `api/model.ts` · `api/queries.ts` |
| `TK_PHAI_THU_MAC_DINH`, `TK_PHAI_TRA_MAC_DINH`, `PAGE_SIZE_MAC_DINH`, `PAGE_SIZE_OPTIONS` | `constants/constants.ts` |
| Chữ: title, nhãn 6 ô, tên 15 cột, nhãn nút, `msg.*` | `i18n/vi.ts` · `i18n/en.ts` |
| Class `.pmkt-btcn-*` (dải Số tiền bù trừ, khoảng cách 2 thẻ) | `pages/buTruCongNo.css` |

Theo cây quyết định `docs/fe-khung-kien-truc-chuan.md:98-108`: có JSX → `components/` · có state →
`hooks/` · gọi http → `api/` · trả mô tả cột → `fields/` · công thức/luật → `helpers/`.

---

## 10. Kiểm thử (`test/`)

### `phanBo.test.ts` — BR02

| # | Input | Kỳ vọng |
|---|---|---|
| P1 | Nguồn 5.000.000; phải trả tick A(3.000.000) · B(2.500.000) · C(1.000.000) | A=3.000.000 · B=2.000.000 · **C=0** (đúng ví dụ `SCR_BTCN_BuTru.md:129-132`) |
| P2 | Nguồn 0 (chưa tick phải thu nào), tick 3 dòng phải trả | Cả 3 = 0 |
| P3 | Nguồn 10.000.000; tick 1 dòng phải trả còn nợ 3.000.000 | Dòng = 3.000.000; **Tổng 2 bảng KHÔNG bằng nhau** ⇒ V5 phải chặn nút Bù trừ |
| P4 | Untick dòng phải thu duy nhất | Mọi dòng phải trả về 0; ô "Số tiền bù trừ" = 0 |
| P5 | Nguồn 5.000.000, các dòng phải trả **nằm ở trang 2 và 3** | Vẫn phân bổ đúng — chứng minh duyệt trên **toàn bộ** tập, không phải trang hiện tại |
| P6 | Sửa tay dòng phải trả rồi tick thêm dòng khác | Giá trị sửa tay **bị ghi đè** bởi phân bổ mới (`SCR_BTCN_BuTru.md:126`) |

### `quyDoi.test.ts` — BR7

| # | Input | Kỳ vọng |
|---|---|---|
| Q1 | `soTien=1.900,00`, `tyGia=1,2` | `2.280,00` — làm tròn 2 chữ số ở kết quả cuối |
| Q2 | Tỷ giá 6 chữ số thập phân `24.512,345678` | Không mất chữ số khi tính; chỉ tròn khi hiển thị |
| Q3 | Tổng quy đổi = tổng của các dòng **chưa làm tròn**, rồi tròn 1 lần | ≠ tổng của các dòng **đã làm tròn** khi có lệch → khẳng định điểm làm tròn duy nhất (R7) |

### `kiemTra.test.ts` — BR01/BR03/BR04

| # | Input | Kỳ vọng |
|---|---|---|
| K1 | Thiếu Đối tượng | `MSG_..._006`, chặn Lấy dữ liệu |
| K2 | Chưa Lấy dữ liệu, bấm Bù trừ | `MSG_..._013` |
| K3 | Có tick phải thu, không tick phải trả | `MSG_..._009` |
| K4 | Tổng lệch 1 đồng | `MSG_..._007` |
| K5 | Ngoại tệ, quy đổi lệch, chưa cấu hình TK 515/635 | `MSG_..._016` |
| K6 | Đủ điều kiện | Trả về `{ hopLe: true }`, không có message |

### `anHien.test.ts`

| # | Input | Kỳ vọng |
|---|---|---|
| A1 | `loaiTienId === dongTienHachToanId` | `coQuyDoi = false`; mảng cột **không chứa** `tyGia` và 3 cột `…QuyDoi` |
| A2 | Loại tiền USD, ĐTHT VND | `coQuyDoi = true`; mảng cột đủ 15 cột (14 + checkbox) |

### `buTruCongNo.render.test.tsx`

| # | Input | Kỳ vọng |
|---|---|---|
| R1 | Mở popup | Có tiêu đề, 6 ô filter, 2 thẻ bảng, dải Số tiền bù trừ, 2 nút footer |
| R2 | Chưa tick gì, bấm Hủy | Đóng ngay, **không** hỏi xác nhận |
| R3 | Tick 1 dòng rồi bấm `×` | Hiện popup xác nhận đóng (BR3) |
| R4 | `coQuyDoi = false` | Không tìm thấy header cột "Tỷ giá" trong DOM (Hide = không render) |

---

## 11. BR đã áp dụng

BR1 (phân trang 2 bảng) · BR2 (STT, checkbox, sắp xếp Ngày chứng từ ↑, sticky header) ·
BR3 (popup: ×/Esc, hủy trái–action phải, xác nhận đóng khi dirty) · BR4 · BR09 (cột Loại chứng từ) ·
BR5 (combogrid Đối tượng) · BR7 (precision & làm tròn quy đổi) · BR11.1 (tìm kiếm nhanh 2 bảng) ·
BR13.1 (nút Reload) · BR14.3 (focus ô đầu khi mở) · BR15.1/15.2/15.4 (bắt buộc, ≥0, hiển thị lỗi) ·
BR18.4 (ẩn cột tỷ giá & quy đổi khi Loại tiền = ĐTHT) · BR25 (route gác bằng `BuTruCongNo.Create`) ·
BR26 (toast lỗi/thông tin) · BR30 (ẩn/hiện cột) · BR31 (dòng Tổng 2 bảng) · BR32 (copy từ grid — sẵn có) ·
BR43 (trim — không có trường chữ ở màn này, áp ở [file 03](03-popup-chung-tu-bu-tru-them-moi.md)) ·
BR44 (truncate `identity` cho Số chứng từ/Số hóa đơn, `long` cho Diễn giải).

**Chưa xử lý:** BR21 (không phải lưới nhập liệu chi tiết con — 2 bảng không thêm/xóa dòng) ·
BR38/BR39 (Figma ẩn nút excel/print) · BR45 (không có thao tác hàng loạt ở màn này).
