# 03 — Popup Chứng từ bù trừ công nợ (Thêm mới)

| | |
|---|---|
| **Mã màn** | `SCR_BTCN_ChungTu_ThemMoi` |
| **UC nguồn** | PMKT-U-14690 — `UC_BTCN_ThemMoi.md` (AC4, AC5 · LP3, LP4) |
| **SCR nguồn** | `5.screens/SCR_BTCN_ChungTu_ThemMoi.md` |
| **Matrix** | `Matrix/PMKT-E-14294_BuTruCongNo/SCR_BTCN_ChungTu_ThemMoi_MaTranAnHien.md` |
| **Figma** | `41383:666955` (VND) · `41667:46774` (ngoại tệ) · `41383:672221` + `41697:102387` (tab Chứng từ công nợ) |
| **Đường vào** | Bấm **Bù trừ** ở [popup 02](02-popup-bu-tru-cong-no.md) — popup này **đè lên** popup 02 |
| **Component gốc** | `components/ChungTuBuTruModal.tsx` với `mode='create'` |

> ⚠ **Tiêu đề popup trong Figma là "Phiếu kế toán tổng hợp"**, không phải "Chứng từ bù trừ công nợ"
> như SCR. Conflict **C1 / Q3** — chưa chốt thì code lấy khoá i18n `chungTu.title`, đổi giá trị chuỗi
> là đủ, không phải sửa cấu trúc.

---

## 1. Bố cục (Figma node `41383:668454`)

```
Overlay 1440×1024  (popup 02 vẫn nằm dưới, bị làm mờ)
└ Dialog Box  1392×538  @ (24,243)                    ← căn giữa dọc, KHÔNG full-height
  ├ Modal Header             1392×56    "Phiếu kế toán tổng hợp"  [?] [×]
  ├ Modal Body               1392×426
  │ ├ Hàng Loại nghiệp vụ    1344×32  @ (16,8)
  │ │   "Loại nghiệp vụ *" [Bù trừ công nợ ▾]  (read-only, w≈350)
  │ ├ Thẻ Thông tin chung    1360×214 @ (16,48)
  │ │ └ body                 1328×190 @ (+16,+12)
  │ │   ├ Cột TRÁI  w=1004 — 3 hàng cao 58, cách nhau 8
  │ │   │   ① Đối tượng                                       (full 1004, disabled)
  │ │   │   ② TK phải thu │ TK phải trả │ Ngày bù trừ           (3 ô, disabled)
  │ │   │   ③ Lý do                                            (full 1004, ENABLE)
  │ │   ├ Đường kẻ dọc @ x=1016, cao 190
  │ │   └ Cột PHẢI  w=300 @ x=1028 — 3 hàng cao 58
  │ │       ① Số chứng từ *      (ENABLE, để trống)
  │ │       ② Ngày hạch toán *   (ENABLE)
  │ │       ③ Ngày chứng từ *    (ENABLE)
  │ └ Thẻ Tab                1360×148 @ (16,270)
  │   ├ Tab Navigation       1328×56  @ (+16,0)
  │   │   [Hạch toán w=64] [Chứng từ công nợ w=112] [Đính kèm w=59] [Tham chiếu w=74]
  │   │                                        … "Loại tiền [VND]" 160×32 @ x≈1168
  │   ├ Bảng                 1328×72  @ (+16,+64)      (header 36 + dòng 36)
  │   └ Scrollbar dọc        8px      @ x=1350
  └ ModelFooter              1392×56  @ y=482
      [Hủy] ································· [Lưu] [Lưu và ghi sổ]
```

Chiều cao 538 là của biến thể **VND, 1 dòng hạch toán**. Biến thể ngoại tệ (`41667:46774`) có 2 dòng
+ dòng Tổng ⇒ thẻ tab cao hơn. ⇒ **chiều cao popup co giãn theo nội dung**, chỉ bề rộng 1392 là cố định.

Footer: **Hủy** trái · **Lưu** (secondary, viền) · **Lưu và ghi sổ** (primary đỏ) phải — BR3 + BR13.2.

---

## 2. Đặc tả UI từ Figma

| Thành phần | Component `@base` dùng lại | Số đo Figma | Ghi chú |
|---|---|---|---|
| Khung popup | `CommonModalShell` `mode='custom'`, `zIndex` **cao hơn popup 02** — `base/index.ts:264`, `CommonModalShell.tsx:65` | w=1392, cao theo nội dung | `busy` bật khi đang gọi Lưu (khoá toàn popup — `CommonModalShell.tsx:57-63`) |
| Loại nghiệp vụ | `CommonSelectBox` `disabled` — `base/index.ts:578` | hàng 1344×32, ô ≈350 | ⚠ **C2** — SCR không có trường này |
| Thẻ Thông tin chung | `Card` — `base/index.ts:158` | 1360×214, padding 16/12 | |
| Bố cục 2 cột + kẻ dọc | CSS grid trong `components/ThongTinChungBuTru.tsx` | trái 1004 · kẻ @1016 · phải 300 @1028 | class `.pmkt-btcn-ct-cols` |
| Ô chữ | `CommonTextBox` + `maxLen` — `base/index.ts:178,205` | h=32 | |
| Ô ngày | `CommonDateInput` — `base/index.ts:170` | h=32 | |
| Thanh tab | `TabMenuChild` (tab gạch chân) — `base/index.ts:150` | 1328×56; tab active gạch đỏ dưới | **Không** dùng `TabMenu2Level` (tab thư mục của thanh cấp 2) |
| Cụm "Loại tiền" góc phải thanh tab | `FieldLabel` + `CommonSelectBox` `disabled` | 160×32 @ x≈1168 | `SCR_BTCN_ChungTu_ThemMoi.md:29` — *"Hiển thị góc phải khu vực tab"* ✅ khớp Figma |
| Bảng 2 tab | `CommonListTable` (`wrapInCard={false}`, `showSearch/Filter/Settings/Add = false`) | vùng 1328 | |
| Nhóm cột cha–con tab Chứng từ công nợ | `ListField.children` — `listTableFormat.ts:47-56` (cha 34px + con 32px) | | Đúng thứ Figma vẽ ở `41383:672221` |
| Dòng Tổng | `showSummary` + `ListField.summary` | h=36 | ⚠ Figma **VND** không vẽ dòng Tổng ở tab Hạch toán, Figma **ngoại tệ** có → theo **BR31** (bắt buộc khi có cột tiền) ⇒ **luôn hiện** |
| Footer 3 nút | `CommonModalFooter` / `ModelFooter` — `base/index.ts:271,295` | h=56 | |

---

## 3. Ma trận ẩn/hiện · required · disabled

Dịch nguyên vẹn từ `SCR_BTCN_ChungTu_ThemMoi_MaTranAnHien.md:32-47`. Trục cột = **Loại tiền**
(read-only, kế thừa từ popup 02).

| Vùng | Trường / Thành phần | C1 (= ĐTHT) | C2 (≠ ĐTHT) |
|---|---|:--:|:--:|
| Thông tin chung | **Lý do** | Show | Show |
| Thông tin chung | **Ngày hạch toán · Ngày chứng từ · Số chứng từ** | Show | Show |
| Thông tin chung | Đối tượng · TK phải thu · TK phải trả · Ngày bù trừ · Tham chiếu · Số tiền bù trừ · Loại tiền | Disable | Disable |
| Tab Hạch toán | **Diễn giải** | Show | Show |
| Tab Hạch toán | `#` · TK Nợ · TK Có · Số tiền | Disable | Disable |
| Tab Hạch toán | **Số tiền quy đổi** | **Hide** | Disable |
| Tab Chứng từ công nợ | `#` | Disable | Disable |
| Tab Chứng từ công nợ · **Nhóm phải thu** | Loại chứng từ · Ngày chứng từ · Số chứng từ · Số hóa đơn · Hạn thanh toán · Số tiền · Số chưa thu · Số bù trừ | Disable | Disable |
| Tab Chứng từ công nợ · **Nhóm phải thu** | Số tiền quy đổi · Số chưa thu quy đổi · Số bù trừ quy đổi | **Hide** | Disable |
| Tab Chứng từ công nợ · **Nhóm phải trả** | Loại chứng từ · Ngày chứng từ · Số chứng từ · Số hóa đơn · Hạn thanh toán · Số tiền · Số còn nợ · Số bù trừ | Disable | Disable |
| Tab Chứng từ công nợ · **Nhóm phải trả** | Số tiền quy đổi · Số còn nợ quy đổi · Số bù trừ quy đổi | **Hide** | Disable |
| Tab Chứng từ công nợ · Cột cuối | **Chênh lệch tỷ giá** | **Hide** | Disable |
| Nút hoạt động | Hủy · Lưu · Lưu và ghi sổ | Show | Show |

**Đúng 5 trường cho nhập** (`SCR_BTCN_ChungTu_ThemMoi_MaTranAnHien.md:53`):
Lý do · Ngày hạch toán · Ngày chứng từ · Số chứng từ · Diễn giải (tab Hạch toán).
Mọi thứ còn lại **dựng sẵn từ popup 02** và read-only.

**Điều kiện mức DÒNG (không lên trục cột)** — `SCR_BTCN_ChungTu_ThemMoi.md:35`:
*"Dòng 1 luôn có; dòng 2 chỉ có khi bù trừ ngoại tệ phát sinh chênh lệch tỷ giá quy đổi."*
Đây là **số dòng phát sinh**, không phải ẩn/hiện trường ⇒ xử lý ở `helpers/hachToan.ts`, không ở
`helpers/anHien.ts`.

---

## 4. Bảng trường — Thông tin chung

| Trường | Control | Field | Max | Bắt buộc | Mặc định | Sửa được | Ghi chú |
|---|---|---|---|:--:|---|:--:|---|
| **Loại nghiệp vụ** ⚠C2 | Dropdown (disabled) | — | — | Y (Figma) | **"Bù trừ công nợ"** | **N** | Hằng số `LOAI_NGHIEP_VU.BU_TRU_CONG_NO` → `constants/constants.ts` |
| Đối tượng | Text (disabled) | `BuTruCongNo.DoiTuongId` | — | Y | Đối tượng đã chọn ở popup 02 | N | |
| **Lý do** | `CommonTextBox` | `PhieuKeToanTongHop.MoTa` | **500** | Y | `"Bù trừ công nợ phải thu, phải trả với " + [Tên đối tượng]` | **Y** | Chuỗi mặc định dùng **interpolation** `t('chungTu.lyDoMacDinh', { tenDoiTuong })`, **không** cộng chuỗi (luật 2) |
| TK phải thu | Text (disabled) | `BuTruCongNo.TaiKhoanPhaiThuId` | — | Y | TK đã chọn | N | |
| TK phải trả | Text (disabled) | `BuTruCongNo.TaiKhoanPhaiTraId` | — | Y | TK đã chọn | N | |
| Ngày bù trừ | Date (disabled) | `BuTruCongNo.NgayBuTru` | — | Y | Ngày đã chọn | N | |
| **Ngày hạch toán** | `CommonDateInput` | `PhieuKeToanTongHop.NgayHachToan` | — | Y | `= Ngày bù trừ` | **Y** | **BR37** — xem §6.1 |
| **Ngày chứng từ** | `CommonDateInput` | `PhieuKeToanTongHop.NgayChungTu` | — | Y | `= Ngày bù trừ` | **Y** | |
| **Số chứng từ** | `CommonTextBox` | `PhieuKeToanTongHop.SoChungTu` | **50** | Y | **để trống** ⚠C4 | **Y** | BR20: ≤50 ký tự, **không** cho ký tự tiếng Việt có dấu; BR19.1 kiểm trùng khi Lưu |
| Tham chiếu | Link list (disabled) | — | — | — | Số chứng từ các chứng từ công nợ tham gia | N | ⚠ **C3** — Figma đặt thành **tab**, SCR đặt trong Thông tin chung |
| Số tiền bù trừ | nhãn chỉ đọc | `BuTruCongNo.SoTienBuTru` | — | — | Tổng số tiền bù trừ | N | |
| Loại tiền | Dropdown (disabled) | `PhieuKeToanTongHop.LoaiTienId` | — | — | Loại tiền đã chọn | N | Hiển thị **góc phải khu vực tab** |

---

## 5. Bảng cột — Tab **Hạch toán**

`fields/hachToanColumns.ts` → `hachToanColumns({ coQuyDoi, t, locale })`

| # | Tên hiển thị | Khoá i18n | Field | Kiểu | Sửa? | Ẩn/hiện |
|---|---|---|---|---|:--:|---|
| 1 | `#` | `chungTu.cotHachToan.stt` | — | index | N | Hiện |
| 2 | **Diễn giải** | `chungTu.cotHachToan.dienGiai` | `ChiTietPhieuKTTH_HachToan.MoTa` | `CommonTextBox` maxLength **500** | **Y** | Hiện |
| 3 | TK Nợ ⚠C8 | `chungTu.cotHachToan.tkNo` | `…TaiKhoanNoId` | text | N | Hiện |
| 4 | TK Có ⚠C8 | `chungTu.cotHachToan.tkCo` | `…TaiKhoanCoId` | text | N | Hiện |
| 5 | Số tiền | `chungTu.cotHachToan.soTien` | `…SoTien` | currency, `summary:'sum'` | N | Hiện |
| 6 | Số tiền quy đổi | `chungTu.cotHachToan.soTienQuyDoi` | `…SoTienQuyDoi` | currency, `summary:'sum'` | N | **Chỉ khi `coQuyDoi`** |

Figma ghi "TN Nợ"/"TN Có" — theo SCR là **"TK Nợ"/"TK Có"** (conflict C8, viết tắt sai trong Figma).

### 5.1. Nội dung 2 dòng — `helpers/hachToan.ts` (BR02 của SCR)

**Dòng 1 — luôn có:**

| | |
|---|---|
| Diễn giải | *"Bù trừ công nợ phải thu, phải trả"* |
| TK Nợ | **TK phải trả** |
| TK Có | **TK phải thu** |
| Số tiền | Tổng số tiền bù trừ (nguyên tệ) |
| Số tiền quy đổi | `MIN(Tổng bù trừ quy đổi phải thu, Tổng bù trừ quy đổi phải trả)` — **lấy bên NHỎ hơn** |

**Dòng 2 — chỉ khi** `Loại tiền ≠ ĐTHT` **và** tổng quy đổi 2 bên **lệch nhau**:

| Trường hợp | Điều kiện | TK Nợ | TK Có |
|---|---|---|---|
| **Lỗ tỷ giá** | quy đổi phải thu **>** phải trả | TK chênh lệch **lỗ** (635 — theo cấu hình) | **TK phải thu** |
| **Lãi tỷ giá** | quy đổi phải thu **<** phải trả | **TK phải trả** | TK chênh lệch **lãi** (515 — theo cấu hình) |

Diễn giải: *"Xử lý chênh lệch tỷ giá"* · Số tiền (nguyên tệ) = **0** ·
Số tiền quy đổi = `|Tổng quy đổi phải thu − Tổng quy đổi phải trả|`.

⚠ `515` / `635` là **giá trị theo cấu hình hệ thống**, không phải hằng số cứng
(`SCR_BTCN_ChungTu_ThemMoi.md:123-124`) ⇒ đọc từ endpoint cấu hình, đặt tên hằng chỉ cho **khoá cấu hình**.

**Kiểm chứng số học** (ví dụ `SCR_BTCN_ChungTu_ThemMoi.md:129-137`, bù trừ 100 USD):

| Ca | Quy đổi phải thu | Quy đổi phải trả | Dòng 1 quy đổi | Dòng 2 | Kết quả phát sinh |
|---|---|---|---|---|---|
| Lỗ | 2.500.000 (TG 25.000) | 2.450.000 (TG 24.500) | **2.450.000** | Nợ 635 / Có TK phải thu = **50.000** | Nợ TK phải trả 2.450.000 ✓ · Có TK phải thu 2.500.000 ✓ |
| Lãi | 2.450.000 | 2.500.000 | **2.450.000** | Nợ TK phải trả / Có 515 = **50.000** | Nợ TK phải trả 2.500.000 ✓ · Có TK phải thu 2.450.000 ✓ |

⚠ Dữ liệu mẫu trong Figma ngoại tệ (`41667:46774`) vẽ dòng 2 là `635 / 132` và dòng Tổng
`1.362 / 659 / 310.050 / 650.000` — **là số giả**, không khớp BR02 (TK Có phải là TK phải thu = 131).
Lấy **theo BR02**, không lấy theo mẫu.

---

## 6. Bảng cột — Tab **Chứng từ công nợ**

`fields/chungTuCongNoColumns.ts` → `chungTuCongNoColumns({ coQuyDoi, t, locale })`.
Dùng `ListField.children` để dựng **2 nhóm cột cha–con** (`listTableFormat.ts:47-56`).

```
│ # │——— Chứng từ phải thu ———————│——— Chứng từ phải trả ———————│ Chênh lệch tỷ giá │
```

| Nhóm | Cột | Khoá i18n (`chungTu.cotCongNo.`) | Field | Kiểu | Ẩn/hiện |
|---|---|---|---|---|---|
| — | `#` | `stt` | — | index | Hiện |
| **Phải thu** | Loại chứng từ | `loaiChungTu` | `ChiTietBuTruCongNo_ChungTu.LoaiChungTuPhaiThu` | text | Hiện |
| | Ngày chứng từ | `ngayChungTu` | *(theo chứng từ gốc)* | date | Hiện |
| | Số chứng từ | `soChungTu` | `…ChungTuPhaiThuId` | `format:'link'` · `identity` | Hiện |
| | Số hóa đơn | `soHoaDon` | `…SoHoaDonPhaiThu` | `format:'link'` · `identity` | Hiện |
| | Hạn thanh toán | `hanThanhToan` | *(theo chứng từ gốc)* | date | Hiện |
| | Số tiền | `soTien` | *(theo chứng từ gốc)* | currency, `summary:'sum'` | Hiện |
| | Số tiền quy đổi | `soTienQuyDoi` | *(FE tính)* | currency, `summary:'sum'` | **`coQuyDoi`** |
| | Số chưa thu | `soChuaThu` | `…SoChuaThu` | currency, `summary:'sum'` | Hiện |
| | Số chưa thu quy đổi | `soChuaThuQuyDoi` | *(FE tính)* | currency, `summary:'sum'` | **`coQuyDoi`** |
| | **Số bù trừ** | `soBuTru` | `…SoTienBuTruPhaiThu` | currency, `summary:'sum'` | Hiện |
| | Số bù trừ quy đổi | `soBuTruQuyDoi` | `…SoTienBuTruPhaiThuQuyDoi` | currency, `summary:'sum'` | **`coQuyDoi`** |
| **Phải trả** | *(9 cột đối xứng)* | … | `…LoaiChungTuPhaiTra`, `…ChungTuPhaiTraId`, `…SoHoaDonPhaiTra`, `…SoConNo`, `…SoTienBuTruPhaiTra`, `…SoTienBuTruPhaiTraQuyDoi` | như trên, `Số chưa thu` → **`Số còn nợ`** | như trên |
| — | **Chênh lệch tỷ giá** | `chenhLechTyGia` | `…ChenhLechTyGia` | currency **có dấu**, `summary:'sum'` | **`coQuyDoi`** |

"Số bù trừ" là **tên hiển thị rút gọn** của "Số tiền bù trừ" (`SCR_BTCN_ChungTu_ThemMoi.md:52`) ⇒
khoá i18n riêng, **không** dùng lại khoá của popup 02.

**Toàn bộ tab chỉ xem, không sửa** (`SCR_BTCN_ChungTu_ThemMoi.md:52`).

### 6.1. Quy tắc dựng dòng — `helpers/ghepCap.ts`

Lấy **danh sách chứng từ phải thu làm gốc** (`SCR_BTCN_ChungTu_ThemMoi.md:54-57`):

```ts
export interface CapGhep {
  phaiThu: DongBuTru
  phaiTra: DongBuTru
  soBuTru: number            // nguyên tệ — BẰNG NHAU ở hai nhóm cột trên cùng dòng
  chenhLechTyGia: number     // = soBuTru×tyGiaPhaiThu − soBuTru×tyGiaPhaiTra (mang dấu)
}
export function ghepCap(phaiThu: readonly DongBuTru[], phaiTra: readonly DongBuTru[]): CapGhep[]
```

1. Duyệt các chứng từ **phải thu đã chọn** theo thứ tự hiển thị ở popup 02.
2. Với mỗi chứng từ phải thu, ghép `Số tiền bù trừ` của nó với các chứng từ **phải trả** (theo thứ tự
   hiển thị) còn phần bù trừ **chưa được ghép** — mỗi phần ghép tạo **một dòng**.
3. Một chứng từ phải thu đối ứng nhiều chứng từ phải trả → xuất hiện ở nhiều dòng, và ngược lại.

**Ví dụ** (`:59`): phải thu A có Số tiền bù trừ 5.000.000; phân bổ cho X 3.000.000 và Y 2.000.000
→ 2 dòng: `(A — X: 3.000.000)` và `(A — Y: 2.000.000)`.

**Dấu của Chênh lệch tỷ giá** (`:91`): `= Số bù trừ quy đổi nhóm phải thu − Số bù trừ quy đổi nhóm
phải trả`; **dương = lỗ tỷ giá**, **âm = lãi tỷ giá**.

**Bất biến phải test** (`:95`): `|Σ Chênh lệch tỷ giá của mọi dòng|` **=** Số tiền quy đổi của dòng
hạch toán 2. Đây là R7 — điểm làm tròn phải duy nhất, xem §10/T-CL.

---

## 7. Hành vi & sự kiện

### 7.1. BR37 — đồng bộ Ngày hạch toán ↔ Ngày chứng từ

| Trạng thái trước khi sửa | Người dùng sửa | Kết quả |
|---|---|---|
| Ngày hạch toán **=** Ngày chứng từ | Ngày hạch toán | Ngày chứng từ **tự cập nhật** theo giá trị mới |
| Ngày hạch toán **≠** Ngày chứng từ | Ngày hạch toán | Ngày chứng từ **không đổi** |
| bất kỳ | Ngày chứng từ | Ngày hạch toán **luôn không đổi** |

Ban đầu cả hai `= Ngày bù trừ` ⇒ **bằng nhau** ⇒ sửa Ngày hạch toán lần đầu sẽ kéo theo Ngày chứng từ.

### 7.2. Nút

| Nút | Điều kiện hiện | Disable khi | Việc làm | Confirm | Toast | Invalidate |
|---|---|---|---|---|---|---|
| **Hủy** | Luôn | `busy` | Đóng popup này, **quay về popup 02 giữ nguyên dữ liệu đã thiết lập** (`UC_BTCN_ThemMoi.md:99-100`) | Chỉ khi 5 trường nhập đã đổi (BR3 dirty) | — | — |
| **Lưu** | quyền `BuTruCongNo.Create` | `busy` | `POST /api/tong-hop/bu-tru-cong-no` với `ghiSo: false` | Không (BR13.2) | ✅ `MSG_..._001` · ❌ `MSG_..._017` | danh sách Phiếu KTTH |
| **Lưu và ghi sổ** | quyền `BuTruCongNo.Create` **và** `PhieuKeToan.Post` | `busy` | **MỘT** request, `ghiSo: true` | Không (BR13.2: *"không hiển thị popup xác nhận"*) | ✅ `MSG_..._001` **và** `MSG_..._002` · ❌ `MSG_..._017` | danh sách + các chứng từ công nợ tham gia |

#### ⚠ Điểm mâu thuẫn phải chốt: "Lưu và ghi sổ" có nguyên tử không? (**Q11**)

| Nguồn | Nói gì |
|---|---|
| **Code — kernel** | *"Bất biến kernel: đó là MỘT request, MỘT transaction — **không phải save rồi post** (`ChungTuTemplate.java:43-44`)"* — `base/domainKit/chungTu/api/ChungTuDescriptor.ts:174-181` |
| **BA — Activity Diagram** | `AD_BTCN_ThemMoi.puml`: Lưu → **hiện `MSG_..._001`** → *rồi mới* kiểm số dư → nếu không đủ: **`MSG_..._018`; "chứng từ giữ trạng thái Chưa ghi sổ"** ⇒ bản ghi **đã commit** trước khi ghi sổ thất bại |
| **BA — Use Case** | `UC_BTCN_ThemMoi.md:122`: *"Chặn Ghi sổ, yêu cầu lấy lại dữ liệu; **chứng từ vẫn được lưu ở trạng thái Chưa ghi sổ**"*; `:135`: *"Thất bại: Hệ thống không lưu chứng từ (**hoặc giữ trạng thái Chưa ghi sổ nếu lỗi ở bước ghi sổ**)"* |

Hai bên nói ngược nhau về **hậu quả khi bước ghi sổ hỏng**: kernel nói rollback cả lượt, BA nói giữ
lại bản ghi Chưa ghi sổ.

**Hệ quả lên FE (khác nhau thật, không phải chi tiết BE):**

| Nếu chốt **nguyên tử** (theo kernel) | Nếu chốt **2 pha** (theo BA) |
|---|---|
| Ghi sổ hỏng ⇒ **chưa có chứng từ nào** ⇒ giữ popup mở, người dùng sửa rồi bấm lại | Ghi sổ hỏng ⇒ **chứng từ đã tồn tại** ⇒ **phải đóng popup** và về danh sách, nếu không người dùng bấm Lưu lần hai sẽ tạo **chứng từ trùng** |
| Toast: chỉ 1 thông báo (thành công hoặc lỗi) | Toast: `MSG_..._001` (đã lưu) **rồi** `MSG_..._018` (không ghi sổ được) — hai toast liên tiếp, BR26.1 cho phép tối đa 3 |
| `invalidate` chỉ chạy khi thành công | `invalidate` **phải chạy cả khi ghi sổ hỏng** (danh sách đã có bản ghi mới) |

**Kế hoạch tạm theo BA (2 pha)** vì đó là đặc tả nghiệp vụ của epic, và ghi rõ **đang lệch bất biến
kernel** — nhưng đây là thứ **phải chốt trước khi code** `hooks/useChungTuBuTruForm.ts`, vì hai
phương án cho hai hành vi đóng/mở popup khác hẳn nhau. Xem **Q11** ở
[00 §12](00-ke-hoach-tong.md).

Về **giao thức**: dù chốt cách nào, FE vẫn gửi **một** request `POST {BASE}` kèm cờ `ghiSo`
(`ChungTuDescriptor.luuGhiSoField` — `ChungTuDescriptor.ts:174-181`), **không** gọi Lưu rồi gọi Ghi sổ
thành 2 request. Khác biệt nằm ở **response** khi ghi sổ hỏng: BE trả lỗi kèm `id` của chứng từ đã
lưu (2 pha) hay trả lỗi trơn (nguyên tử) — chốt ở [06 §1.4](06-hop-dong-api-va-i18n.md).

Sau khi Lưu thành công: **đóng cả hai popup**, quay về danh sách và làm mới
(`SCR_BTCN_ChungTu_ThemMoi.md:104`).

Khi lưu **thất bại**: giữ nguyên toàn bộ dữ liệu người dùng đã nhập, **không reset, không đóng form**,
highlight vùng vi phạm (`UC_BTCN_ThemMoi.md:127`).

### 7.3. Tabs

| Tab | Trong phạm vi? | Nội dung |
|---|:--:|---|
| **Hạch toán** | ✅ | §5 — mặc định active |
| **Chứng từ công nợ** | ✅ | §6 |
| Đính kèm | ❌ ⚠C3 | Giữ chỗ trên thanh tab (Figma vẽ), nội dung "đang phát triển" — chờ Q3 |
| Tham chiếu | ❌ ⚠C3 | Như trên. SCR đặt "Tham chiếu" là **trường Link list** trong Thông tin chung, không phải tab |

BR15.4 — khi Lưu mà lỗi nằm ở tab khác, **tự chuyển sang tab chứa lỗi**. Hiện chỉ ô "Diễn giải" (tab
Hạch toán) là trường nhập trong tab ⇒ áp dụng cho nó.

---

## 8. Validation phía FE

| # | Luật | Điều kiện | Thông báo (nguyên văn) | BR nguồn | Ai kiểm |
|---|---|---|---|---|---|
| V1 | Số chứng từ bắt buộc | trống khi bấm Lưu / Lưu và ghi sổ | *"Vui lòng nhập Số chứng từ"* (`MSG_..._014`) | BR15.1 | **FE** |
| V2 | Số chứng từ ≤ 50 ký tự | nhập | — (chặn cứng tại ô, **không** báo lỗi) | BR14.4 · BR20.2 | **FE** |
| V3 | Số chứng từ không có ký tự tiếng Việt có dấu | nhập | — | BR20.2 | **FE** |
| V4 | Lý do bắt buộc, ≤ 500 | trống / vượt | *"[Tên trường] không được để trống"* | BR15.1 · BR14.4 | **FE** |
| V5 | Diễn giải dòng hạch toán ≤ 500 | nhập | — (chặn cứng) | BR14.4 | **FE** |
| V6 | Trim đầu/cuối Lý do · Số chứng từ · Diễn giải | blur + trước submit | — | BR43 | **FE** |
| V7 | Ngày hạch toán / Ngày chứng từ bắt buộc | trống | *"[Tên trường] không được để trống"* | BR15.1 | **FE** |
| V8 | **Trùng Số chứng từ** | khi Lưu | *"Số chứng từ đã tồn tại. Vui lòng nhập số khác"* (`MSG_..._015`) | BR19.1 | **BE** — FE hiển thị lỗi trả về |
| V9 | **Kỳ kế toán đã khóa** | khi Lưu / Ghi sổ | *"Chứng từ thuộc kỳ đã khóa sổ {ngày khóa sổ}. Không thể thực hiện"* (`MSG_..._019`) | BR17 | **BE** |
| V10 | **Số dư đã thay đổi** | khi Ghi sổ | *"Số dư công nợ của chứng từ đã thay đổi. Vui lòng lấy lại dữ liệu và thực hiện lại"* (`MSG_..._018`) | — | **BE** |
| V11 | **Chưa cấu hình TK chênh lệch tỷ giá** | ngoại tệ + lệch quy đổi | *"Chưa cấu hình tài khoản xử lý chênh lệch tỷ giá lãi/lỗ. Vui lòng kiểm tra cấu hình"* (`MSG_..._016`) | — | **BE** (FE đã chặn sớm ở popup 02 nếu có endpoint cấu hình) |
| V12 | Lỗi hệ thống khi lưu | — | *"Lỗi khi xử lý chứng từ bù trừ công nợ"* (`MSG_..._017`) | — | **BE** |

BR15.3 — cặp *Ngày hạch toán ≥ Ngày chứng từ*: **không áp dụng** ở màn này. BR37 (§7.1) mới là quy tắc
đúng cho cặp ngày này, và SCR không đặt ràng buộc so sánh. → nếu BA muốn áp cả BR15.3, cần nói rõ
(đưa vào Q của file 00).

---

## 9. Luồng xử lý

1. Popup 02 bấm **Bù trừ** hợp lệ → gọi `helpers/ghepCap.ts` (danh sách cặp) và `helpers/hachToan.ts`
   (1–2 dòng bút toán), truyền xuống popup này qua **prop**, không qua API.
2. `useChungTuBuTruForm({ duLieuDungSan })` khởi tạo form:
   `Lý do` = chuỗi mặc định · `Ngày hạch toán` = `Ngày chứng từ` = `Ngày bù trừ` · `Số chứng từ` = `''`.
3. Người dùng nhập **Số chứng từ**, sửa Lý do / ngày / Diễn giải dòng hạch toán.
4. Bấm **Lưu** hoặc **Lưu và ghi sổ**:
   - Validate FE (V1, V4, V7) → lỗi thì border đỏ + scroll tới ô đầu tiên + switch tab (BR15.4).
   - `api/payload.ts` dựng body từ state (§ [06 §1](06-hop-dong-api-va-i18n.md)).
   - `queries.useLuu()` → `busy = true` khoá popup (`CommonModalShell.busy`).
5. Thành công: toast (7.2) → `invalidateQueries` → đóng **cả hai** popup → về danh sách.
6. Thất bại: toast lỗi từ `describeApiError`, giữ nguyên form, mở khoá.

---

## 10. Phân bổ file

| Việc | File |
|---|---|
| Khung popup, tabs, footer 3 nút, `busy`/`dirty` | `components/ChungTuBuTruModal.tsx` |
| Khối 2 cột Thông tin chung + đường kẻ dọc | `components/ThongTinChungBuTru.tsx` |
| Tab Hạch toán | `components/HachToanTab.tsx` |
| Tab Chứng từ công nợ (nhóm cột cha–con) | `components/ChungTuCongNoTab.tsx` |
| Mô tả cột 2 tab | `fields/hachToanColumns.ts` · `fields/chungTuCongNoColumns.ts` |
| **Dựng 1–2 dòng hạch toán + chênh lệch tỷ giá** | `helpers/hachToan.ts` |
| **Dựng các cặp ghép** | `helpers/ghepCap.ts` |
| Quy đổi + làm tròn BR7 | `helpers/quyDoi.ts` |
| Cờ ẩn/hiện theo Loại tiền | `helpers/anHien.ts` |
| **BR37** đồng bộ 2 ngày | `hooks/useChungTuBuTruForm.ts` |
| State form + gọi Lưu / Lưu và ghi sổ | `hooks/useChungTuBuTruForm.ts` |
| `POST /bu-tru-cong-no` + Zod | `api/buTruCongNoApi.ts` · `api/model.ts` · `api/payload.ts` · `api/queries.ts` |
| `LOAI_NGHIEP_VU`, `MAX_LEN_LY_DO=500`, `MAX_LEN_SO_CHUNG_TU=50`, `MAX_LEN_DIEN_GIAI=500`, `TAB_KEY.*` | `constants/constants.ts` |
| Chữ (title, 12 nhãn, 6+21 tên cột, 3 nút, `msg.*`) | `i18n/vi.ts` · `i18n/en.ts` |
| Class `.pmkt-btcn-ct-*` (2 cột + kẻ dọc) | `pages/buTruCongNo.css` |

---

## 11. Kiểm thử (`test/`)

### `hachToan.test.ts`

| # | Input | Kỳ vọng |
|---|---|---|
| H1 | VND, tổng bù trừ 10.000.000 | **1 dòng**: Nợ = TK phải trả, Có = TK phải thu, Số tiền 10.000.000, **không** có Số tiền quy đổi |
| H2 | USD, quy đổi phải thu 2.500.000 > phải trả 2.450.000 | **2 dòng**. D1 quy đổi = **2.450.000** (MIN). D2: Nợ **635**, Có **TK phải thu**, nguyên tệ **0**, quy đổi **50.000** |
| H3 | USD, quy đổi phải thu 2.450.000 < phải trả 2.500.000 | D1 quy đổi = **2.450.000**. D2: Nợ **TK phải trả**, Có **515**, quy đổi **50.000** |
| H4 | USD, quy đổi 2 bên **bằng nhau** | **1 dòng** — không sinh dòng chênh lệch |
| H5 | H2 + kiểm phát sinh | Nợ TK phải trả = 2.450.000 · Có TK phải thu = 2.450.000 + 50.000 = **2.500.000** |

### `ghepCap.test.ts`

| # | Input | Kỳ vọng |
|---|---|---|
| G1 | Phải thu A=5.000.000; phải trả X=3.000.000, Y=2.000.000 | **2 dòng**: (A—X, 3.000.000) · (A—Y, 2.000.000) |
| G2 | Phải thu A=2.000.000, B=1.000.000; phải trả X=3.000.000 | **2 dòng**: (A—X, 2.000.000) · (B—X, 1.000.000) — X xuất hiện 2 lần |
| G3 | Mọi dòng | `soBuTru` nhóm phải thu **=** `soBuTru` nhóm phải trả (nguyên tệ) |
| **T-CL** | Ngoại tệ, tỷ giá 2 bên khác nhau | `\|Σ chenhLechTyGia\|` **=** Số tiền quy đổi dòng hạch toán 2 (bất biến `SCR:95`, rủi ro R7) |

### `useChungTuBuTruForm` (BR37)

| # | Input | Kỳ vọng |
|---|---|---|
| N1 | HT = CT = 31/01, sửa HT → 05/02 | CT **tự đổi** thành 05/02 |
| N2 | HT = 05/02, CT = 31/01, sửa HT → 10/02 | CT **giữ** 31/01 |
| N3 | Sửa CT → 20/02 | HT **không đổi** |

### `anHien.test.ts` (bổ sung cho popup này)

| # | Input | Kỳ vọng |
|---|---|---|
| A3 | `coQuyDoi = false` | Tab Hạch toán **không có** cột "Số tiền quy đổi"; tab Chứng từ công nợ **không có** 6 cột quy đổi lẫn cột "Chênh lệch tỷ giá" |
| A4 | `mode='create'` | Đúng **5** trường enable: Lý do · Ngày hạch toán · Ngày chứng từ · Số chứng từ · Diễn giải |

### `chungTuBuTru.render.test.tsx`

| # | Input | Kỳ vọng |
|---|---|---|
| R5 | Mở popup ở `mode='create'` | Số chứng từ **rỗng** (không phải "BTCN-2026-…" như mẫu Figma — C4) |
| R6 | Bấm Lưu khi Số chứng từ rỗng | Không gọi API; hiện `MSG_..._014`; ô Số chứng từ border đỏ |
| R7 | Bấm Hủy sau khi sửa Lý do | Hiện xác nhận đóng (BR3); xác nhận → popup 02 vẫn **giữ nguyên** tick và số tiền |
| R8 | Người dùng không có quyền `PhieuKeToan.Post` | Nút "Lưu và ghi sổ" **bị ẩn** (BR25.2 — ẩn, không disable), nút "Lưu" vẫn còn |
| R9 | "Lưu và ghi sổ", BE trả lỗi `SO_DU_DA_THAY_DOI` **kèm `id`** (phương án **2 pha** — Q11) | Toast `MSG_..._001` **rồi** `MSG_..._018`; **popup đóng**; `invalidate` danh sách đã chạy ⇒ bấm Lưu lần hai không thể tạo chứng từ trùng |
| R10 | "Lưu và ghi sổ", BE trả lỗi **không** kèm `id` (phương án **nguyên tử** — Q11) | Chỉ toast `MSG_..._018`; **popup giữ nguyên**, dữ liệu người dùng nhập còn đủ; **không** invalidate danh sách |

> R9/R10 là **hai ca loại trừ nhau** — viết cả hai ngay từ đầu, bật ca nào theo kết luận của **Q11**.
> Đây chính là lý do Q11 chặn bước B9 ([00 §9](00-ke-hoach-tong.md)).

---

## 12. BR đã áp dụng

BR2 (STT) · BR3 (popup, ×/Esc, xác nhận đóng khi dirty, nút hủy trái–action phải) ·
BR4 · BR09 (cột Loại chứng từ, trường Tham chiếu) · BR7 (precision & làm tròn quy đổi, chênh lệch) ·
BR13.2 (Lưu / Lưu và Ghi sổ không hỏi xác nhận; Đóng hỏi khi dirty) · BR14.1 (chế độ Thêm mới) ·
BR14.3 (focus ô đầu) · BR14.4 (chặn cứng maxLength 500/50/500) · BR15.1/15.4 (bắt buộc, border đỏ,
scroll tới lỗi, switch tab) · BR17 (kỳ kế toán — BE kiểm, FE hiển thị) · BR18.2/18.4 (công thức quy đổi,
ẩn cột quy đổi khi = ĐTHT) · BR19.1 (trùng số chứng từ) · BR20 (≤50 ký tự, không dấu, nhập tay) ·
BR21 (lưới chi tiết con — **chỉ đọc**, không nút Thêm/Xóa dòng theo quy định riêng của SCR) ·
BR25 ("Lưu và ghi sổ" cần cả `.Create` lẫn `.Post`; thiếu quyền → ẩn) · BR26 (toast) ·
BR31 (dòng Tổng 2 tab) · BR36 (không gộp bút toán — FE gửi đúng số dòng đã dựng) ·
BR37 (đồng bộ Ngày hạch toán ↔ Ngày chứng từ) · BR43 (trim) · BR44 (truncate).

**Chưa xử lý:**
- **BR15.3** cặp *Ngày hạch toán ≥ Ngày chứng từ* — SCR không đặt ràng buộc này, BR37 mới là luật của
  cặp ngày ở đây. Cần BA xác nhận có áp thêm không.
- **BR6** (Đối tượng tập hợp chi phí · Vụ việc · Đơn vị · Khoản mục chi phí trên dòng hạch toán) —
  SCR không cho nhập các trường này; 2 dòng hạch toán do hệ thống dựng sẵn.
- **Tab Đính kèm · Tab Tham chiếu** — ngoài phạm vi, chờ **Q3**.
