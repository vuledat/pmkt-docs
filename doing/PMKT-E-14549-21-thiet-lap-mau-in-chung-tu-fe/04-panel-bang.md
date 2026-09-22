# 04 · Bảng chỉnh *{Tên bảng}* — khối Bảng

| | |
|---|---|
| Mã màn | `SCR_ThietLapMauIn` — mục `{Tên bảng}` của cột phải (một mục cho **mỗi lưới** trên form) |
| Nguồn SCR | `SCR:141-175` · `SCR:277-279` |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` |
| Figma | frame **2** `71956:289243` |
| File chính | `components/inspector/BangInspector.tsx` · `BangCotRow.tsx` · `helpers/doRongCot.ts` |
| Luật phủ | `R-TLMI-092…119` (nhóm H) |

---

## 1. Bố cục (Figma frame 2)

```
Bảng hàng hoá
─────────────────────────────────────────────────────
Tên bảng in ra
[ Danh sách hàng hoá                                 ]
☑ In cột STT
☑ Dòng Cộng
☑ Lặp tiêu đề mỗi trang
Kẻ ô
(•) Đầy đủ    ( ) Kẻ ngang
Cột in ra
[🔍 Tìm cột…                                        ]
┌──┬─┬─────────────┬───────────────┬───────┬─────┬─────┐
│⠿ │☑│ Tên cột DL  │ Tên hiển thị  │Rộng % │ Căn │Cộng │
├──┼─┼─────────────┼───────────────┼───────┼─────┼─────┤
│⠿ │☑│ Mã hàng     │[Mã hàng     ] │[ 12 ] │≡≡≡  │ ☐   │
│⠿ │☑│ Tên hàng    │[Tên mặt h…  ] │[ 30 ] │≡≡≡  │ ☐   │
│⠿ │☑│ ĐVT         │[ĐVT         ] │[  8 ] │≡≡≡  │ ☐   │
│⠿ │☑│ Số lượng    │[Số lượng    ] │[ 10 ] │≡≡≡  │ ☑   │
│⠿ │☑│ Đơn giá     │[Đơn giá     ] │[ 14 ] │≡≡≡  │ ☐   │
│⠿ │☑│ Thành tiền  │[Thành tiền  ] │[ 16 ] │≡≡≡  │ ☑   │
│⠿ │☑│ Kho         │[Kho         ] │[  8 ] │≡≡≡  │ ☐   │
│⠿ │☐│ Chiết khấu  │[Chiết khấu  ] │  —    │≡≡≡  │ ☐   │  ← dòng MỜ
│⠿ │☐│ Thuế suất   │[Thuế suất   ] │  —    │≡≡≡  │ ☐   │  ← dòng MỜ
└──┴─┴─────────────┴───────────────┴───────┴─────┴─────┘
Tổng độ rộng cột đang 98% (nên = 100%)      Chia đều về 100%   ← link ĐỎ
```

⚠ **X4** — Figma frame 2 ghi nhãn cột là **`Tiêu hiển thị`** (thiếu chữ "u"); frame 3 ghi đúng
`Tên hiển thị`; `R-TLMI-102` và `MSG_204` đều gọi **"Tên hiển thị của cột"**. ⇒ dùng **`Tên hiển thị`**.

---

## 2. Đặc tả UI

| Thành phần | Component | Ghi chú | Luật |
|---|---|---|---|
| `Tên bảng in ra` | `CommonInput` (`base/index.ts:251`) | **được phép trống** ⇒ không in tên bảng | `R-TLMI-094` · `R-TLMI-095` |
| `In cột STT` | `CommonCheckbox` | | `R-TLMI-096` |
| `Dòng Cộng` | `CommonCheckbox` | | `R-TLMI-097` · `R-TLMI-098` |
| `Lặp tiêu đề mỗi trang` | `CommonCheckbox` | | `R-TLMI-099` |
| `Kẻ ô` | `CommonRadio.Group` (`base/index.ts:257`) | `Đầy đủ` · `Kẻ ngang` | `R-TLMI-100` |
| `Tìm cột…` | `CommonSearchGroup` (`base/index.ts:423`) hoặc `CommonInput` + icon | lọc **không phân biệt dấu**, **không lưu** | `R-TLMI-116` |
| Lưới cột | **mới** `BangCotRow.tsx` trong `SortableList` (`components/SortableList.tsx`) | 7 cột: `⠿` · ☑ · `Tên cột DL` · `Tên hiển thị` · `Rộng %` · `Căn` · `Cộng` | `R-TLMI-101…108` |
| Cột `Căn` | `CommonSegmented` (`base/index.ts:267`) | 3 nút Trái · Giữa · Phải | `R-TLMI-105` |
| Dòng tổng | text | nguyên văn `Tổng độ rộng cột đang {n}% (nên = 100%)` | `R-TLMI-110` |
| link `Chia đều về 100%` | `CommonButton` variant link | chữ **đỏ** | `R-TLMI-114` |

**Cột bỏ tick** ⇒ cả dòng **mờ**, ô `Rộng %` hiện **`—`** (Figma frame 2, hai dòng cuối).

---

## 3. Bảng trường của khối Bảng

| Trường | Khoá i18n | Field API | Kiểu | Ràng buộc | Mặc định | Luật |
|---|---|---|---|---|---|---|
| Tên bảng in ra | `bang.tenBang` | `khoi.bang.tenBang` | string | được phép trống | **trống** cho lưới đầu tiên | `R-TLMI-094/095` |
| In cột STT | `bang.inCotStt` | `khoi.bang.inCotStt` | bool | — | `true` | `R-TLMI-096` |
| Dòng Cộng | `bang.dongCong` | `khoi.bang.dongCong` | bool | — | `true` | `R-TLMI-097` |
| Lặp tiêu đề mỗi trang | `bang.lapTieuDe` | `khoi.bang.lapTieuDe` | bool | — | `true` | `R-TLMI-099` |
| Kẻ ô | `bang.keO` | `khoi.bang.keO` | `'DAY_DU'\|'KE_NGANG'` | radio | `DAY_DU` | `R-TLMI-100` |

## 4. Bảng cột (mỗi dòng của lưới `Cột in ra`)

| Cột | Khoá i18n | Field API | Kiểu | Sửa được | Ràng buộc | Luật |
|---|---|---|---|---|---|---|
| `⠿` | — | thứ tự mảng | — | kéo thả | **disable khi đang lọc** | `R-TLMI-115` · `R-TLMI-117` |
| ☑ in | `bang.cot.in` | `cot.in` | bool | ✔ | khối bật phải còn **≥ 1** cột tick | `R-TLMI-103` · `R-TLMI-104` |
| `Tên cột DL` | `bang.cot.tenDl` | `cot.k` | string | ❌ **chỉ đọc** | — | `R-TLMI-101` |
| `Tên hiển thị` | `bang.cot.tenHienThi` | `cot.nhan` | string | ✔ | **không trống, ≤ 100 ký tự** | `R-TLMI-102` |
| `Rộng %` | `bang.cot.rong` | `cot.rong` | int | ✔ | **3-90**; `—` khi bỏ tick | `R-TLMI-108` · `R-TLMI-112` |
| `Căn` | `bang.cot.can` | `cot.can` | `'TRAI'\|'GIUA'\|'PHAI'` | ✔ | — | `R-TLMI-105` |
| `Cộng` | `bang.cot.cong` | `cot.cong` | bool | ✔ **chỉ cột SỐ** | mặc định **Có** với cột tiền | `R-TLMI-106` · `R-TLMI-107` |

**Độ rộng mặc định** lấy theo **tỷ lệ độ rộng cột trên lưới form** (`R-TLMI-109`) — do BE tính khi dựng
mẫu chuẩn, FE chỉ nhận.

---

## 5. Thuật toán `Chia đều về 100%` — `helpers/doRongCot.ts` (D9)

```
chiaDeuVe100(cot):
  1. tapIn   = cot.filter(c => c.in)                 // R-TLMI-112: cột bỏ tick GIỮ NGUYÊN số cũ
     tongCu  = sum(tapIn.rong)
  2. tapIn.forEach(c => c.rong = Math.floor(c.rong / tongCu * 100))   // LÀM TRÒN XUỐNG
  3. thieu = 100 - sum(tapIn.rong)
     tapIn[tapIn.length - 1].rong += thieu           // dồn vào CỘT IN CUỐI CÙNG
  4. tapIn.forEach(c => {
       if (c.rong < 3) {
         const bu = 3 - c.rong
         c.rong = 3
         cotRongNhat(tapIn).rong -= bu               // trừ vào CỘT RỘNG NHẤT
       }
     })
```

⚠ **`ELSE` viết hoa trong `R-TLMI-114`: "GIỮ NGUYÊN TỶ LỆ giữa các cột — KHÔNG chia bằng nhau."**
Tên nút gây hiểu nhầm.

### Ba ca chốt của BA + ca chạm sàn — **bắt buộc thành test**

| Input | Output | Nguồn |
|---|---|---|
| `40 / 40 / 40` | `33 / 33 / 34` | `R-TLMI-114` (`SCR:279`) |
| `50 / 30` | `62 / 38` | `R-TLMI-114` |
| `10 / 10 / 10 / 10` | `25 / 25 / 25 / 25` | `R-TLMI-114` |
| `90 / 70 / 2` | `54 / 43 / 3` | `S-TLMI-024` (ca chạm sàn 3) |

Kiểm tay ca 1: `40/120×100 = 33,33 → 33` mỗi cột ⇒ tổng 99 ⇒ thiếu 1 ⇒ cột cuối `34`. ✔
Kiểm tay ca 2: `50/80×100 = 62,5 → 62`; `30/80×100 = 37,5 → 37` ⇒ tổng 99 ⇒ cột cuối `38`. ✔
Kiểm tay ca 4: tổng 162. `90/162×100 = 55,5 → 55`; `70/162×100 = 43,2 → 43`; `2/162×100 = 1,23 → 1`
⇒ tổng 99 ⇒ cột cuối `1+1 = 2`. Bước 4: `2 < 3` ⇒ nâng lên `3`, trừ 1 vào cột rộng nhất (`55 → 54`)
⇒ **`54 / 43 / 3`**. ✔

### Ba dịp gọi

| Dịp | Luật |
|---|---|
| bấm nút `Chia đều về 100%` | `R-TLMI-114` |
| **tự chạy khi Lưu** nếu tổng ≠ 100 | `R-TLMI-111` |
| khi có **cột mới** ở phiên bản sau | `R-TLMI-093` |

Chốt **C31**: áp cho **mọi cột đang tick in**, **không** phụ thuộc ô `Tìm cột`.

---

## 6. Hành vi & sự kiện

| Thao tác | Điều kiện | Việc làm | Luật |
|---|---|---|---|
| Xoá trống `Tên bảng in ra` | luôn | **không in tên bảng** — không phải lỗi | `R-TLMI-094` |
| Bỏ tick cột | còn > 1 cột tick | cột không in; dòng mờ; `Rộng %` hiện `—`; **không** tính vào tổng | `R-TLMI-103` · `R-TLMI-112` |
| Bỏ tick cột **cuối cùng** | khối đang **bật** | **chặn**, báo `MSG_203` với `{TenBang}` | `R-TLMI-104` |
| Tick lại cột đang có `Rộng %` trống | luôn | gán lại độ rộng (theo `R-TLMI-113`) | `R-TLMI-113` |
| Đổi `Rộng %` | luôn | cập nhật dòng tổng ngay; **tổng ≠ 100 KHÔNG phải lỗi** | `R-TLMI-110` |
| Bật `Cộng` | **chỉ cột số** | cột không phải số ⇒ ô `Cộng` **không có** | `R-TLMI-106` |
| Kéo `⠿` | **không đang lọc** | đổi thứ tự cột | `R-TLMI-115` |
| Kéo `⠿` khi **đang lọc** ở `Tìm cột` | — | **chặn** kéo thả | `R-TLMI-117` |
| Gõ vào `Tìm cột` | luôn | lọc **không phân biệt dấu** (`foldAccent` ở `client/src/utils/text/quickSearch.ts:8`); **không lưu**; **không đổi** thiết lập của cột bị ẩn khỏi lưới | `R-TLMI-116` · `R-TLMI-118` |
| Bấm `Chia đều về 100%` | luôn | chạy thuật toán §5; **một bước undo** | `R-TLMI-114` |
| Tắt `👁` khối Bảng | luôn | khối không in; **bỏ qua validate** khối đó (C18) | `R-TLMI-207` · `R-TLMI-208` |

**Trên bản in:**
- `R-TLMI-092`: mỗi khối Bảng ứng **đúng một lưới** trên form.
- `R-TLMI-093`: cột thêm vào lưới ở phiên bản sau **tự xuất hiện CUỐI bảng**.
- `R-TLMI-097/098`: `Dòng Cộng = Có` ⇒ in dòng `Cộng` cuối bảng cho các cột có tick `Cộng`;
  `= Không` ⇒ không in dòng nào.
- `R-TLMI-099`: `Lặp tiêu đề mỗi trang = Có` ⇒ hàng tiêu đề cột lặp ở mỗi trang (`thead` + `@media print`).
- `R-TLMI-100`: `Đầy đủ` = kẻ cả dọc lẫn ngang; `Kẻ ngang` = chỉ kẻ ngang.
- `R-TLMI-265`: bảng dài **tràn trang**; khối đứng sau in **tiếp ngay dưới** dòng cuối của bảng (BE).
- `R-TLMI-119`: cộng gộp mặt hàng áp **trước** khi dựng bảng — **BE**, ngoài phạm vi FE (chốt **C01**:
  khoá gộp = *mã hàng + đơn vị tính + đơn giá + thuế suất* (+ *số lô, hạn sử dụng*); chốt **C30**: chỉ áp
  cho **Hoá đơn, phiếu xuất kho, phiếu nhập kho**).

---

## 7. Validation phía FE

| # | Trường | Điều kiện | Message (nguyên văn) | Thời điểm | Tầng | Luật |
|---|---|---|---|---|---|---|
| V03 | Cột in | khối **đang bật** phải còn **≥ 1** cột tick | `Bảng "{TenBang}" phải giữ lại ít nhất 1 cột hiển thị` | **khi bỏ tick cột**, khi Lưu | Client/Server | `R-TLMI-104` |
| V04 | `Tên hiển thị` của cột | không trống, ≤ 100 ký tự | `Tên hiển thị của cột không được để trống, tối đa 100 ký tự` | rời ô, khi Lưu | Client/Server | `R-TLMI-102` |
| V05 | `Rộng %` | số nguyên 3-90 | `Độ rộng cột phải là số nguyên từ 3 đến 90` | rời ô, khi Lưu | Client/Server | `R-TLMI-108` |

**KHÔNG phải lỗi:** tổng độ rộng ≠ 100 (`R-TLMI-110/111`), tên bảng trống (`R-TLMI-094`).

`MSG_203` dùng interpolation `{TenBang}`: `t('mauIn:msg.e203', { TenBang })` — **không cộng chuỗi**.

---

## 8. Phân bổ file

| Việc | File |
|---|---|
| Panel khối Bảng | `components/inspector/BangInspector.tsx` |
| Một dòng của lưới cột | `components/inspector/BangCotRow.tsx` |
| `chiaDeuVe100` · `tongDoRong` | `helpers/doRongCot.ts` |
| Kéo thả cột | `components/SortableList.tsx` (dùng lại) |
| Lọc không dấu | `@core` `matchesQuickSearch` (`client/src/utils/text/quickSearch.ts:20`) |
| Render bảng trên giấy (kẻ ô, dòng Cộng, lặp tiêu đề) | `components/BanInPaper.tsx` |
| Ràng V03/V04/V05 | `helpers/kiemTraMau.ts` |
| Hằng `GIOI_HAN_RONG_COT = { min: 3, max: 90 }` · `GIOI_HAN_TEN_COT = { max: 100 }` | `constants/constants.ts` |

---

## 9. Kiểm thử

### `test/doRongCot.test.ts` (`node`) — **file quan trọng nhất của khối Bảng**

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-114 · ca BA 40/40/40 thành 33/33/34` | `[40,40,40]` → `[33,33,34]` |
| `R-TLMI-114 · ca BA 50/30 thành 62/38` | `[50,30]` → `[62,38]` |
| `R-TLMI-114 · ca BA 10/10/10/10 thành 25/25/25/25` | `[10,10,10,10]` → `[25,25,25,25]` |
| `R-TLMI-114 · ca chạm sàn 90/70/2 thành 54/43/3` | `[90,70,2]` → `[54,43,3]` |
| `R-TLMI-114 · GIỮ NGUYÊN TỶ LỆ, không chia bằng nhau` | `[80,20]` → `[80,20]` (không thành `[50,50]`) |
| `R-TLMI-114 · làm tròn XUỐNG rồi dồn vào cột in cuối` | `[1,1,1]` → `[33,33,34]` |
| `R-TLMI-112 · cột bỏ tick giữ nguyên số cũ và không tính vào tổng` | `[{40,in},{40,in},{99,off}]` → hai cột in thành `[50,50]`, cột off vẫn `99` |
| `C31 · áp cho mọi cột tick in, không phụ thuộc ô Tìm cột` | gọi với `loc='Mã'` → vẫn chia cho cả 7 cột tick |
| `R-TLMI-110 · tongDoRong chỉ cộng cột đang tick` | → `98` với ví dụ Figma |
| `R-TLMI-111 · tổng ≠ 100 KHÔNG phải lỗi` | `kiemTraMau` với tổng 98 → **không** sinh lỗi |

### `test/inspectors.test.tsx` (DOM) — phần khối Bảng

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-094 · tên bảng trống thì không in tên bảng` | `tenBang=''` → `BanInPaper` không render caption |
| `R-TLMI-095 · tên bảng mặc định trống cho lưới đầu tiên` | mẫu chuẩn → lưới 1 có `tenBang === ''` |
| `R-TLMI-096 · In cột STT` | tick → bảng có cột `STT`; bỏ tick → không |
| `R-TLMI-097/098 · Dòng Cộng` | `Có` → có dòng `Cộng`; `Không` → không có dòng nào |
| `R-TLMI-099 · Lặp tiêu đề mỗi trang` | `Có` → hàng tiêu đề nằm trong `<thead>` |
| `R-TLMI-100 · Kẻ ô Đầy đủ / Kẻ ngang` | `DAY_DU` → ô có border 4 phía; `KE_NGANG` → chỉ border-bottom |
| `R-TLMI-101 · Tên cột DL chỉ đọc` | → ô `Tên cột DL` **không** phải input |
| `R-TLMI-102 · Tên hiển thị trống hoặc > 100 thì MSG_204` | `''` và 101 ký tự → hiện `Tên hiển thị của cột không được để trống, tối đa 100 ký tự` |
| `R-TLMI-103 · bỏ tick cột thì dòng mờ và Rộng % hiện —` | bỏ tick → dòng có class mờ, ô rộng hiện `—` |
| `R-TLMI-104 · bỏ tick cột cuối cùng thì MSG_203` | còn 1 cột tick, bỏ nốt → `Bảng "Danh sách hàng hoá" phải giữ lại ít nhất 1 cột hiển thị` |
| `R-TLMI-104 · khối đang TẮT thì không chặn` | tắt `👁`, bỏ tick hết → **không** báo lỗi (C18) |
| `R-TLMI-105 · Căn của cột` | bấm `Phải` → ô bảng trên giấy `text-align: right` |
| `R-TLMI-106 · chỉ cột số mới có ô Cộng` | cột `Tên hàng` (text) → **không** có checkbox `Cộng` |
| `R-TLMI-107 · Cộng mặc định Có với cột tiền` | mẫu chuẩn → `Thành tiền` có `cong === true` |
| `R-TLMI-108 · Rộng % biên 3 và 90 hợp lệ, 2 và 91 không` | → `MSG_205` cho 2 và 91 |
| `R-TLMI-113 · tick lại cột đang có Rộng % trống` | bỏ tick rồi tick lại → `Rộng %` có số, không trống |
| `R-TLMI-115 · kéo thả đổi thứ tự cột` | kéo dòng 1 xuống dòng 3 → thứ tự mảng đổi |
| `R-TLMI-116 · Tìm cột lọc không phân biệt dấu, không lưu` | gõ `ma hang` → hiện dòng `Mã hàng`; `mau` **không** đổi |
| `R-TLMI-117 · đang lọc thì không cho kéo thả cột` | gõ vào `Tìm cột` → handle `⠿` `disabled` |
| `R-TLMI-118 · lọc không đổi thiết lập của cột bị ẩn` | lọc rồi bỏ lọc → thiết lập mọi cột nguyên vẹn |
| `R-TLMI-110 · dòng tổng hiện số hiện tại` | tổng 98 → text `Tổng độ rộng cột đang 98% (nên = 100%)` |
| `R-TLMI-111 · Lưu khi tổng ≠ 100 thì tự chia lại` | tổng 98, bấm Lưu → payload có tổng **= 100** |
| `R-TLMI-092 · mỗi khối Bảng ứng đúng một lưới` | form 2 lưới → mẫu chuẩn có 2 khối Bảng |
| `R-TLMI-093 · cột mới ở phiên bản sau vào CUỐI bảng` | catalog thêm cột → cột mới ở cuối mảng |

---

## 10. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR7 | định dạng số ở dòng `Cộng` và giá trị tiền trên bản in |
| BR13 | ô `Tên hiển thị`, `Rộng %` — kiểm khi rời ô |
| BR30 | chốt **C18** — khối Bảng đang ẩn thì bỏ qua validate |
| BR51.6 (Phase 2) | `R-TLMI-119` cộng gộp mặt hàng — **BE**, chốt **C01** + **C30** |
