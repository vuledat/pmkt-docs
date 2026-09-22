# 05 · Khối tự do — lưới ô kiểu Excel, thanh công cụ, menu chuột phải, kho trường

| | |
|---|---|
| Mã màn | `SCR_ThietLapMauIn` — khối tự do (lưới trên trang xem trước + bảng chỉnh bên phải) |
| Nguồn SCR | `SCR:176-200` · `SCR:284-292` |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` |
| Figma | frame **3** `71974:27549` |
| File chính | `helpers/luoiTuDo.ts` · `components/LuoiTuDo.tsx` · `OLuoi.tsx` · `ThanhCongCuTuDo.tsx` · `MenuChuotPhaiO.tsx` · `inspector/KhoiTuDoInspector.tsx` |
| Luật phủ | `R-TLMI-120…181` (nhóm I — **62 luật, lô nặng nhất**) |

> **Lô thi công riêng (Lô 4).** Phụ thuộc duy nhất vào Lô 1 (type + store). Sở hữu trọn bộ file ở §8.

---

## 1. Bố cục (Figma frame 3)

```
─── Thanh công cụ khối tự do (CHỈ hiện khi đang chọn khối tự do) ───────────────────
Ghi chú giao hàng · ô dòng 2, cột 3 │+ Dòng trên│+ Dòng dưới│+ Cột trái│+ Cột phải│− Dòng│− Cột│Gộp ô│
Tách ô │ B │ I │ Trái │ Giữa │ Phải │ Chọn trường… │ Xóa nội dung
────────────────────────────────────────────────────────────────────────────────────

Trên TRANG XEM TRƯỚC — lưới ô của khối:
┌───────────────────────────────────┬───────────────────────────────────┐
│ Giao đến: 12 Trần Hưng Đạo, …     │ Người nhận: Nguyễn Văn An          │
├───────────────────────────────────┼───────────────────────────────────┤
│ Ghi chú: hàng dễ vỡ, xin nhẹ tay  │ ⌐Ô: Chữ tự do chưa có nội dung —  │ ← viền ĐỎ
│                                   │  nháy đúp để gõ                 ⌐ │
└───────────────────────────────────┴───────────────────────────────────┘
                                          [Ghi chú giao hàng]  ← nhãn tên khối nổi (đỏ)

Bảng chỉnh bên phải:
Ghi chú giao hàng   [khối tự do]
─────────────────────────────────────────────────────
Tên khối
[ Ghi chú giao hàng                                  ]
Tìm kiếm
[🔍 Tìm kiếm…                                        ]
┌───────────────────┬──────────────────┬────────┐
│ Trường dữ liệu    │ Tên hiển thị     │ In đậm │
├───────────────────┼──────────────────┼────────┤
│ Khách hàng        │[Khách hàng     ] │   ☐    │
│ Địa chỉ giao hàng │[Giao đến       ] │   ☑    │
│ Người nhận        │[Người nhận     ] │   ☑    │
│ Điện thoại        │[Điện thoại     ] │   ☐    │
│ Diễn giải         │[Diễn giải      ] │   ☐    │
│ Số chứng từ       │[Số            ] │   ☑    │
│ Ngày chứng từ     │[Ngày          ] │   ☑    │
│ Tổng tiền hàng    │[Tổng tiền hàng ] │   ☐    │
│ Thuế GTGT         │[Thuế GTGT     ] │   ☐    │
│ Tổng tiền thanh…  │[Tổng tiền thanh…]│   ☑    │
│ Số tiền bằng chữ  │[Trống = chỉ in…] │   ☐    │  ← placeholder
│ Tên đơn vị        │[Tên đơn vị    ] │   ☐    │
└───────────────────┴──────────────────┴────────┘
                                        Xóa khối này   ← link ĐỎ
```

⚠ **Bảng chỉnh KHÔNG có ô `Kích thước lưới` và KHÔNG có cột `Vị trí`** (`R-TLMI-128`) — mọi thao tác với
lưới làm **trên trang xem trước** (`R-TLMI-229`).

---

## 2. Mô hình dữ liệu ô (D7)

```ts
type NoiDungO =
  | { loai: 'TRONG' }
  | { loai: 'TRUONG'; k: string }          // k = mã trường trong kho trường
  | { loai: 'CHU_TU_DO'; chu: string }     // <= 255 ký tự

interface OTuDo {
  id: string                               // ổn định qua gộp/tách
  dong: number; cot: number                // 0-based, góc TRÊN-TRÁI
  rowSpan: number; colSpan: number         // >= 1
  noiDung: NoiDungO
  can: 'TRAI' | 'GIUA' | 'PHAI'            // THEO Ô   — R-TLMI-161
  nghieng: boolean                         // THEO Ô   — R-TLMI-160
}

interface KhoiTuDo {
  id: string; loai: 'TU_DO'
  ten: string                              // <= 60 ký tự, KHÔNG in ra — R-TLMI-121/126
  hien: boolean
  soDong: number                           // 1…20     — R-TLMI-129, sàn 1 theo C20
  soCot: number                            // 1…6      — R-TLMI-130, sàn 1 theo C20
  o: OTuDo[]                               // CHỈ ô neo
}

// CẤP MẪU, không nằm trong khối — R-TLMI-156
type TruongDungChung = Record<string, { nhan?: string; dam?: boolean }>
```

**Bảng phủ dẫn xuất** (`helpers/luoiTuDo.ts`):
```ts
function bangPhu(k: KhoiTuDo): (string | null)[][]   // [dong][cot] -> oId | null
```
Mọi thuật toán chạy trên bảng phủ rồi ghi ngược ra `o[]`.

**Bất biến của lưới** (kiểm bằng test, không cần luật mới):
- mọi ô của `[0..soDong-1] × [0..soCot-1]` được phủ **đúng một lần**;
- không ô neo nào tràn ra ngoài `soDong × soCot`;
- `1 <= soDong <= 20`, `1 <= soCot <= 6`.

---

## 3. Thuật toán — `helpers/luoiTuDo.ts`

| Hàm | Luật | Mô tả |
|---|---|---|
| `bangPhu(khoi)` | — | dựng ma trận phủ |
| `chonVung(neo1, neo2, khoi)` | `R-TLMI-132` | vùng chữ nhật từ hai ô; **Shift + bấm** |
| `noiVungTheoOGop(vung, khoi)` | `R-TLMI-137` | vùng chạm ô đã gộp ⇒ **tự nới ra** cho trọn ô đó; lặp tới khi ổn định |
| `demOCoNoiDung(vung, khoi)` | `R-TLMI-138` | đếm ô **có nội dung** trong vùng ⇒ tham số `{SoO}` của `MSG_404` |
| `gopO(vung, khoi)` | `R-TLMI-136` · `R-TLMI-139` | vùng → **một** ô; giữ nội dung của **ô đầu tiên CÓ nội dung** theo **trái→phải, trên→xuống**; các ô còn lại mất nội dung |
| `tachO(oId, khoi)` | `R-TLMI-140` · chốt **C19** | ô gộp → các ô đơn; nội dung về **ô góc trên-trái**, các ô khác trống; **không hỏi xác nhận** |
| `themDong(khoi, tai, phia)` | `R-TLMI-133` · `R-TLMI-142` | chèn dòng cạnh ô đang chọn; ô mới **trống**; ô đang chọn **giữ nguyên nội dung**; chèn vào **giữa** ô gộp ⇒ ô gộp **rộng thêm** một dòng |
| `themCot(khoi, tai, phia)` | như trên | tương tự theo cột |
| `xoaDong(khoi, vung)` | `R-TLMI-134` · `R-TLMI-141` | xoá các dòng **vùng chọn phủ**; đi qua ô gộp ⇒ **tách trước rồi mới xoá** |
| `xoaCot(khoi, vung)` | như trên | |
| `doiNoiDungHaiO(a, b, khoi)` | `R-TLMI-154` | kéo ô có nội dung thả lên ô khác ⇒ **hai ô đổi nội dung** |
| `xoaNoiDung(vung, khoi)` | `R-TLMI-155` | đưa mọi ô đang chọn về **ô trống** |
| `datTruongVaoO(oId, k, khoi)` | `R-TLMI-152` · `R-TLMI-153` | **một trường chỉ ở một ô TRONG MỘT KHỐI** — đặt lại ⇒ gỡ khỏi ô cũ cùng khối; **cùng trường ở nhiều khối khác nhau thì ĐƯỢC PHÉP** |
| `coTheGop(vung)` · `coTheTach(oId, khoi)` | `R-TLMI-174` | bật/tắt nút `Gộp ô` / `Tách ô` |
| `coTheXoaDong(khoi)` · `coTheXoaCot(khoi)` | `R-TLMI-135` · chốt **C20** | `false` khi còn **1 dòng** / **1 cột** |

### 3.1 Sàn và trần

| | Sàn | Trần | Luật |
|---|---|---|---|
| Dòng | **1** (nút `− Dòng` mờ) | **20** (`MSG_208`) | `R-TLMI-135` · `R-TLMI-129` · chốt **C20** |
| Cột | **1** (nút `− Cột` mờ) | **6** (`MSG_216`) | `R-TLMI-135` · `R-TLMI-130` · chốt **C20** |
| Khối tự do / mẫu | 0 | **10** (`MSG_207`) | `R-TLMI-125` |

Muốn bỏ hẳn khối thì dùng **`Xóa khối này`** (`MSG_403`), không phải xoá hết dòng/cột (chốt **C20**).

### 3.2 `Các cột rộng bằng nhau` (`R-TLMI-131`)

Khối tự do **KHÔNG** có độ rộng riêng cho từng cột — 2 cột = mỗi cột nửa bề ngang, 3 cột = một phần ba…
⇒ CSS `grid-template-columns: repeat(var(--soCot), 1fr)`. Không có ô nhập `Rộng %` nào ở khối tự do.

---

## 4. Thanh công cụ (Figma frame 3 — 2 hàng, 15 nút)

| Hàng | Nút (nguyên văn) | Điều kiện Disable | Luật |
|---|---|---|---|
| 0 | nhãn ngữ cảnh `{Tên khối} · ô dòng {r}, cột {c}` | — | **X8** (Figma, không có trong `R-TLMI-170`) |
| 1 | `+ Dòng trên` | chưa chọn ô · đủ 20 dòng | `R-TLMI-133` · `R-TLMI-129` |
| 1 | `+ Dòng dưới` | như trên | |
| 1 | `+ Cột trái` | chưa chọn ô · đủ 6 cột | `R-TLMI-133` · `R-TLMI-130` |
| 1 | `+ Cột phải` | như trên | |
| 1 | `− Dòng` | chưa chọn ô · **còn 1 dòng** | `R-TLMI-134` · `R-TLMI-135` |
| 1 | `− Cột` | chưa chọn ô · **còn 1 cột** | như trên |
| 1 | `Gộp ô` | vùng chọn **< 2 ô** | `R-TLMI-174` · **X7** |
| 2 | `Tách ô` | ô đang chọn **không phải ô gộp** | `R-TLMI-174` · **X7** |
| 2 | `B` (In đậm) | chưa chọn ô | `R-TLMI-163` |
| 2 | `I` (Nghiêng) | chưa chọn ô | `R-TLMI-163` |
| 2 | `Trái` `Giữa` `Phải` | chưa chọn ô | `R-TLMI-161` · `R-TLMI-163` |
| 2 | `Chọn trường…` | chưa chọn ô | `R-TLMI-150` |
| 2 | `Xóa nội dung` | chưa chọn ô | `R-TLMI-155` |

- `R-TLMI-162`: **chưa chọn ô nào ⇒ MỌI nút đều mờ**.
- `R-TLMI-170`: thanh công cụ **Hide** hoàn toàn khi khối đang chọn **không phải** khối tự do.
- **X7**: `Gộp ô` / `Tách ô` **luôn hiện, mờ khi không áp dụng được** (Figma) — không ẩn.

### 4.1 Nút `B` / `I` / căn — áp **theo vùng chọn** (`R-TLMI-163`), nhưng ghi **hai nơi khác nhau** (D6)

| Nút | Ghi vào | Phạm vi ảnh hưởng | Luật |
|---|---|---|---|
| `B` | `truongDungChung[k].dam` cho mọi ô-**trường** trong vùng | **MỌI ô dùng trường đó, KỂ CẢ ở khối tự do khác** | `R-TLMI-156` · `R-TLMI-158` |
| `B` trên ô **Chữ tự do** | ⚠ tài liệu không nói lưu ở đâu — đề xuất `OTuDo` có thêm `dam?: boolean` cho riêng ô Chữ tự do | chỉ ô đó | `R-TLMI-159` · **Q9** |
| `I` | `OTuDo.nghieng` | **chỉ ô đó** | `R-TLMI-160` |
| `Trái` / `Giữa` / `Phải` | `OTuDo.can` | **chỉ ô đó** | `R-TLMI-161` |

⚠ **Q9** — vùng chọn **trộn** ô-trường và ô-Chữ tự do thì `B` ra gì? `R-TLMI-156 §Ghi chú` ghi rõ tài
liệu **không quy định**. Đề xuất: áp cho **mọi ô trong vùng**, theo đúng bản chất từng ô.

### 4.2 In đậm trên bản in

| Loại ô | Đậm cái gì | Luật |
|---|---|---|
| Ô **trường** + `In đậm` | **CHỈ `Tên hiển thị`**; giá trị luôn in **thường** | `R-TLMI-158` |
| Ô **Chữ tự do** + `In đậm` | **cả chữ** | `R-TLMI-159` |

⇒ `BanInPaper` render ô-trường thành `<b>{nhan}: </b><span>{giaTri}</span>`, **không** bọc cả ô trong `<b>`.

---

## 5. Menu chuột phải (Figma frame 3 — 10 mục, 3 nhóm)

```
┌──────────────────────────────┐
│ Chọn trường dữ liệu…         │  ← "Sửa chữ" khi ô đang chọn là Chữ tự do (R-TLMI-172)
│ Xóa nội dung ô               │
├──────────────────────────────┤
│ Thêm dòng phía trên          │
│ Thêm dòng phía dưới          │
│ Thêm cột bên trái            │
│ Thêm cột bên phải            │
│ Xóa dòng                     │
│ Xóa cột                      │
├──────────────────────────────┤
│ Gộp ô                   (mờ) │
│ Tách ô                  (mờ) │
└──────────────────────────────┘
```

`R-TLMI-171`: các lệnh có **cùng tác dụng** với thanh công cụ ⇒ dùng chung một lớp hành động
(`hooks/useVungChon.ts` export các `lenh` chung cho cả hai UI).
`R-TLMI-170`: menu **Hide** khi khối đang chọn không phải khối tự do.

---

## 6. Phím tắt (`R-TLMI-173`)

| Phím | Việc làm |
|---|---|
| `↑` `↓` `←` `→` | di chuyển ô đang chọn |
| `Delete` | xoá nội dung ô |
| `Enter` hoặc `F2` | mở chọn trường / sửa chữ |
| `Shift` + bấm ô | chọn **vùng chữ nhật** (`R-TLMI-132`) |

Phím tắt **tắt** khi đang mở hộp thoại con (`R-TLMI-256`) và khi focus đang ở một ô nhập của bảng chỉnh.

---

## 7. Nội dung ô — bốn cách đưa vào

| # | Cách | Luật |
|---|---|---|
| 1 | **Nháy đúp ô** ⇒ mở hộp chọn **cạnh ô**; hai mục đầu là *(Ô trống)* và *Chữ tự do*, tiếp theo là kho trường | `R-TLMI-150` |
| 2 | Nút `Chọn trường…` trên thanh công cụ, hoặc `Enter` | `R-TLMI-150` |
| 3 | **Kéo dòng trường** ở bảng chỉnh **thả vào ô** trên trang xem trước (K2) | `R-TLMI-149` |
| 4 | Menu chuột phải › `Chọn trường dữ liệu…` | `R-TLMI-171` |

Trong hộp chọn: gõ chữ ⇒ lọc kho trường **không phân biệt dấu** (`R-TLMI-151`, dùng
`matchesQuickSearch` ở `client/src/utils/text/quickSearch.ts:20`).

### 7.1 Ba loại nội dung

| Loại | In ra gì | Luật |
|---|---|---|
| **Ô trống** | **không in gì nhưng CHIẾM CHỖ** | `R-TLMI-143` |
| **Trường** | `Tên hiển thị: Giá trị`; `Tên hiển thị` bị xoá trống ⇒ **chỉ in giá trị** | `R-TLMI-144` · `R-TLMI-145` |
| **Chữ tự do** | **đúng chữ người dùng gõ**; gõ **ngay trong ô**, tối đa **255 ký tự** | `R-TLMI-146` · `R-TLMI-147` |

⚠ `R-TLMI-148`: chọn `Chữ tự do` mà **rời ô khi chưa gõ** ⇒ ô **tự về Ô trống**. **Không phải lỗi.**
Nhưng Figma frame 3 cho thấy ô Chữ tự do đang ở **trạng thái đang sửa** thì báo lỗi tại chỗ, nguyên văn:
`Ô: Chữ tự do chưa có nội dung — nháy đúp để gõ` (`R-TLMI-235`).

### 7.2 Ràng buộc trùng trường

| Luật | Nội dung |
|---|---|
| `R-TLMI-152` | một trường **chỉ ở một ô TRONG MỘT KHỐI** |
| `R-TLMI-153` | **cùng một trường dùng ở NHIỀU khối tự do khác nhau** — **được phép** |

---

## 8. Kho trường (bảng chỉnh bên phải)

| Cột | Sửa được | Ràng buộc | Luật |
|---|---|---|---|
| `Trường dữ liệu` | ❌ **luôn chỉ đọc** | — | `R-TLMI-169` |
| `Tên hiển thị` | ✔ | ≤ 255 ký tự; **mặc định = tên trường**; **không bắt buộc** | `R-TLMI-157` |
| `In đậm` | ✔ | — | `R-TLMI-156` |

**Nguồn kho trường** (`R-TLMI-165`, BR50.7): **mọi ô trên form của nghiệp vụ TRỪ cột trong các lưới**:
- ô nhập đầu form (gồm **Số chứng từ**, **Ngày chứng từ**);
- ô tổng cuối form, kèm **Số tiền bằng chữ** đọc từ ô tổng thanh toán theo quy tắc đọc số chung;
- thông tin đơn vị (tên, địa chỉ, mã số thuế, điện thoại) của **chi nhánh ghi trên chứng từ**.

⚠ `R-TLMI-165 §Ghi chú`: nguồn khai báo là **đặc tả form của epic nghiệp vụ**, epic `_21` **không liệt
kê** ⇒ FE nhận qua API (`catalog.khoTruong`), **không** tự suy.

| Luật | Nội dung |
|---|---|
| `R-TLMI-166` | kho trường là **danh sách phẳng, KHÔNG chia nhóm** |
| `R-TLMI-167` | ô mới ở phiên bản sau **tự vào kho trường** nhưng **KHÔNG tự chen vào khối tự do** |
| `R-TLMI-168` | ô `Tìm kiếm` lọc **không phân biệt dấu** |
| `R-TLMI-164` | trường **chưa đặt vào ô nào** ⇒ `Tên hiển thị` và `In đậm` **KHÔNG lưu**; mở lại màn thì về mặc định |
| chốt **C10** | trường bị **xoá khỏi form**: hiện **mờ + nhãn "không còn trên form"**, loại khỏi mẫu khi Lưu; bản in **bỏ qua im lặng** |

---

## 9. Kéo thả (D8 — `@dnd-kit/core`, không thêm package)

| # | Nguồn | Đích | `data.current` | Hành vi |
|---|---|---|---|---|
| K2 | dòng kho trường | ô neo | `{ loai: 'truong', k }` → `{ loai: 'oLuoi', khoiId, oId }` | `datTruongVaoO` (`R-TLMI-149`) |
| K3 | ô neo **có nội dung** | ô neo khác | `{ loai: 'oLuoi', … }` → `{ loai: 'oLuoi', … }` | `doiNoiDungHaiO` (`R-TLMI-154`) |

Cả hai nằm trong **cùng** `DndContext` ở `pages/ThietLapMauInScreen.tsx` (chung với K1 và K4) ⇒ **bắt
buộc** phân biệt bằng `data.current.loai`, xem **R1**.

**Hiệu năng (R12):** `OLuoi` bọc `memo`; vùng chọn giữ ở `useVungChon` (**ngoài** store undo) nên đổi
vùng chọn không tạo bước Hoàn tác (`R-TLMI-223` `partialize`).

---

## 10. Lưới căn chỉnh

| Luật | Nội dung |
|---|---|
| `R-TLMI-177` | bật ⇒ các ô của khối tự do được **kẻ đường phân ô**, và **ô trống đang chọn có chữ gợi ý** cách đưa nội dung vào |
| `R-TLMI-178` | mọi dấu hiệu **KHÔNG in, KHÔNG xuất PDF** ⇒ `@media print { display: none }` (D13) |
| `R-TLMI-179` | bỏ tick ⇒ trang xem trước hiển thị **đúng như bản in**; thao tác vẫn dùng được |

⚠ `R-TLMI-177 §Ghi chú`: tài liệu **không cho nguyên văn** chữ gợi ý ⇒ `msg.sh` không có gì đối chiếu.
Đề xuất dùng nguyên văn Figma frame 3 cho ô Chữ tự do chưa gõ:
`Ô: Chữ tự do chưa có nội dung — nháy đúp để gõ`; ô trống đang chọn:
`Nháy đúp để chọn trường, hoặc kéo trường từ bảng bên phải thả vào ô` (mượn nguyên văn `MSG_104`).

---

## 11. Validation phía FE

| # | Trường | Điều kiện | Message (nguyên văn) | Thời điểm | Luật |
|---|---|---|---|---|---|
| V06 | Tên khối tự do | không trống, ≤ 60 ký tự | `Tên khối tự do không được để trống, tối đa 60 ký tự` | trong hộp `Đặt tên khối`, rời ô, khi Lưu | `R-TLMI-121` |
| V07 | Số khối tự do | ≤ 10 | `Mỗi mẫu tối đa 10 khối tự do` | khi bấm `+ Thêm khối tự do`, khi Lưu | `R-TLMI-125` |
| V08 | Số dòng | ≤ 20 | `Mỗi khối tự do tối đa 20 dòng` | khi bấm `+ Dòng trên` / `+ Dòng dưới`, khi Lưu | `R-TLMI-129` |
| V09 | Số cột | ≤ 6 | `Mỗi khối tự do tối đa 6 cột` | khi bấm `+ Cột trái` / `+ Cột phải`, khi Lưu | `R-TLMI-130` |
| V13 | `Tên hiển thị` của trường; nội dung ô `Chữ tự do` | ≤ 255 ký tự | `Tên hiển thị và chữ tự do tối đa 255 ký tự` | rời ô, khi Lưu | `R-TLMI-147` · `R-TLMI-157` |

### **KHÔNG BAO GIỜ là lỗi** (D12)

| Trường hợp | Luật |
|---|---|
| **Ô trống** trong khối tự do | `R-TLMI-236` |
| Khối tự do **đang bật mà MỌI ô đều trống** — vẫn **lưu được** | `R-TLMI-176` |
| Chọn `Chữ tự do` rồi rời ô khi chưa gõ ⇒ **tự về Ô trống** | `R-TLMI-148` |

⇒ `helpers/kiemTraMau.ts` duyệt khối tự do phải `if (o.noiDung.loai === 'TRONG') continue` **trước mọi
phép kiểm khác** (`R-TLMI-237`: xét lỗi **chỉ xét ô có nội dung**).

### Hộp xác nhận

| Mã | Nguyên văn | Khi nào | Luật |
|---|---|---|---|
| `MSG_403` | `Xóa khối "{TenKhoi}" cùng các ô trong đó?` | bấm `✕` ở dòng khối hoặc link `Xóa khối này` | `R-TLMI-175` |
| `MSG_404` | `Vùng chọn có {SoO} ô đang có nội dung. Gộp thì chỉ giữ nội dung của ô đầu tiên, các ô còn lại mất nội dung. Tiếp tục?` | bấm `Gộp ô` khi vùng có **≥ 2 ô CÓ nội dung** | `R-TLMI-138` |

⚠ **Q11** — tài liệu **không nêu tên hai nút** của `MSG_404`. Đề xuất `Tiếp tục` / `Huỷ`.
**Tách ô KHÔNG hỏi xác nhận** (chốt **C19**) — không mất dữ liệu.

---

## 12. Vòng đời khối tự do

```
Bấm "+ Thêm khối tự do" (cột trái)
 ├─ đã có 10 khối         → chặn, MSG_207                          (R-TLMI-125)
 └─ mở hộp "Đặt tên khối"                                          (R-TLMI-120)
      ├─ tên trống / > 60 → MSG_206                                (R-TLMI-121)
      └─ hợp lệ
           • tạo lưới 1 dòng × 2 cột, TOÀN Ô TRỐNG                 (R-TLMI-123)
           • đặt NGAY TRƯỚC khối Chữ ký                            (R-TLMI-122)
           • toast MSG_104                                         (R-TLMI-124)
           • mở bảng chỉnh của khối                                (R-TLMI-124)
           • CHỌN SẴN ô đầu tiên                                   (R-TLMI-124)

Sửa tên sau khi tạo: ô "Tên khối" trên bảng chỉnh (chốt C07)        (R-TLMI-127)
Tên khối KHÔNG in ra bản in                                        (R-TLMI-126)
Xoá khối: ✕ ở dòng khối HOẶC link "Xóa khối này" — cả hai hỏi MSG_403  (R-TLMI-175/211)
```

---

## 13. Phân bổ file

| Việc | File |
|---|---|
| ⭐ Toàn bộ thuật toán lưới | `helpers/luoiTuDo.ts` |
| Gom / lọc `truongDungChung` | `helpers/truongDungChung.ts` |
| Lưới ô trên trang xem trước | `components/LuoiTuDo.tsx` |
| Một ô neo (draggable + droppable + inline edit) | `components/OLuoi.tsx` |
| Thanh công cụ 2 hàng | `components/ThanhCongCuTuDo.tsx` |
| Menu chuột phải 10 mục | `components/MenuChuotPhaiO.tsx` |
| Hộp chọn cạnh ô | `components/modal/HopChonTruongO.tsx` |
| Hộp `Đặt tên khối` | `components/modal/HopDatTenKhoiModal.tsx` |
| Hộp `MSG_404` | `components/modal/XacNhanGopOModal.tsx` |
| Hộp `MSG_403` | `components/modal/XacNhanXoaKhoiModal.tsx` |
| Bảng chỉnh kho trường | `components/inspector/KhoiTuDoInspector.tsx` · `KhoTruongRow.tsx` |
| Vùng chọn + phím tắt + lệnh chung | `hooks/useVungChon.ts` |
| DnD cho K2/K3 | `hooks/useKeoThaO.ts` |
| Render khối tự do trên giấy | `components/BanInPaper.tsx` |
| Ràng V06/V07/V08/V09/V13 | `helpers/kiemTraMau.ts` |
| Hằng `GIOI_HAN_LUOI = { dongMin:1, dongMax:20, cotMin:1, cotMax:6 }` · `GIOI_HAN_KHOI_TU_DO = { max: 10 }` · `GIOI_HAN_TEN_KHOI = { max: 60 }` · `GIOI_HAN_CHU_TU_DO = { max: 255 }` · `LUOI_MOI = { soDong: 1, soCot: 2 }` | `constants/constants.ts` |

---

## 14. Kiểm thử

### `test/luoiTuDo.test.ts` (`node`) — **file quan trọng nhất của lô 4**

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-123 · khối mới là lưới 1×2 toàn ô trống` | `taoKhoiTuDo('X')` → `soDong=1`, `soCot=2`, 2 ô `TRONG` |
| `R-TLMI-132 · Shift chọn vùng chữ nhật` | chọn (0,0) rồi Shift (1,2) → vùng 2×3 = 6 ô |
| `R-TLMI-137 · vùng chạm ô gộp thì tự nới ra` | ô gộp phủ (0,0)-(1,1); chọn (0,0)-(0,0) rồi mở rộng tới (0,2) → vùng thành (0,0)-(1,2) |
| `R-TLMI-136 · gộp vùng 2 ô thành một ô` | vùng 1×2 → 1 ô neo `colSpan=2`, `o.length` giảm 1 |
| `R-TLMI-139 · gộp giữ nội dung ô đầu tiên CÓ nội dung (trái→phải, trên→xuống)` | ô(0,0) trống, ô(0,1) = `Chữ A`, ô(0,2) = `Chữ B` → ô gộp giữ `Chữ A` |
| `R-TLMI-138 · vùng có 2 ô có nội dung thì demOCoNoiDung = 2` | → `2`, dùng làm `{SoO}` |
| `R-TLMI-138 · vùng có 1 ô có nội dung thì KHÔNG hỏi` | → `demOCoNoiDung() === 1` ⇒ gộp thẳng |
| `R-TLMI-140 · tách ô đưa nội dung về góc trên-trái` | ô gộp 2×2 chứa `Chữ A` → tách → ô(0,0) = `Chữ A`, 3 ô còn lại `TRONG` |
| `C19 · tách ô KHÔNG hỏi xác nhận` | `tachO()` là hàm thuần, không trả cờ cần hỏi |
| `R-TLMI-133 · thêm dòng trên: ô mới trống, ô đang chọn giữ nội dung` | ô(1,0)=`A`; `themDong(tai:1, phia:'tren')` → dòng 1 trống, `A` xuống dòng 2 |
| `R-TLMI-142 · thêm dòng vào GIỮA ô gộp thì ô gộp rộng thêm` | ô gộp (0,0)-(2,0); thêm dòng tại 1 → `rowSpan` từ 3 thành 4 |
| `R-TLMI-134 · xoá dòng mà vùng chọn phủ` | vùng phủ dòng 1-2 → `soDong` giảm 2 |
| `R-TLMI-141 · xoá dòng đi qua ô gộp thì tách trước` | ô gộp (0,0)-(1,1); xoá dòng 0 → còn ô đơn ở dòng cũ 1, không còn ô gộp |
| `R-TLMI-135 · còn 1 dòng thì coTheXoaDong = false` | `soDong=1` → `false` |
| `R-TLMI-135 · còn 1 cột thì coTheXoaCot = false` | `soCot=1` → `false` |
| `R-TLMI-129 · đủ 20 dòng thì themDong bị chặn` | `soDong=20` → ném/`trả lỗi MSG_208` |
| `R-TLMI-130 · đủ 6 cột thì themCot bị chặn` | `soCot=6` → `MSG_216` |
| `R-TLMI-143 · ô trống chiếm chỗ` | lưới 1×2 với 1 ô trống → bảng phủ có **2** ô, không phải 1 |
| `R-TLMI-148 · Chữ tự do rỗng khi rời ô thì về Ô trống` | `{loai:'CHU_TU_DO', chu:''}` + `roiO()` → `{loai:'TRONG'}` |
| `R-TLMI-152 · một trường chỉ ở một ô trong một khối` | đặt `k='soCt'` vào ô A rồi ô B (cùng khối) → ô A về `TRONG` |
| `R-TLMI-153 · cùng trường ở hai khối khác nhau thì được phép` | đặt `k='soCt'` ở khối 1 và khối 2 → cả hai giữ |
| `R-TLMI-154 · kéo ô có nội dung thả lên ô khác thì ĐỔI nội dung` | ô A=`X`, ô B=`Y` → sau đổi: A=`Y`, B=`X` |
| `R-TLMI-155 · Xóa nội dung đưa mọi ô đang chọn về ô trống` | vùng 2×2 có nội dung → cả 4 ô `TRONG` |
| `R-TLMI-174 · coTheGop / coTheTach` | vùng 1 ô → `coTheGop=false`; ô gộp → `coTheTach=true` |
| `bất biến · bảng phủ luôn phủ đúng một lần` | 200 thao tác ngẫu nhiên → mọi ô `[dong][cot]` có đúng một `oId` |
| `bất biến · không ô neo nào tràn ra ngoài lưới` | như trên |

### `test/truongDungChung.test.ts` (`node`)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-156 · Tên hiển thị và In đậm dùng chung cả mẫu` | đặt `nhan='Giao đến'` cho `k='diaChiGiao'` ở khối 1 → ô dùng cùng `k` ở khối 2 đọc ra `Giao đến` |
| `R-TLMI-157 · Tên hiển thị mặc định = tên trường` | chưa đặt → `nhan` = tên trường trong catalog |
| `R-TLMI-157 · 255 hợp lệ, 256 không` | → `MSG_212` cho 256 |
| `R-TLMI-164 · trường chưa đặt vào ô nào thì không lưu` | `truongDungChung` có `k` không ô nào dùng → `locTruongDungChung()` bỏ `k` đó |
| `R-TLMI-161 · Căn theo Ô, KHÔNG dùng chung` | đặt `can='PHAI'` cho ô A dùng `k` → ô B dùng cùng `k` vẫn `TRAI` |
| `R-TLMI-160 · Nghiêng theo Ô` | tương tự |

### `test/LuoiTuDo.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-144 · ô trường in dạng Tên hiển thị: Giá trị` | `k='nguoiNhan'`, `nhan='Người nhận'`, giá trị `Nguyễn Văn An` → text `Người nhận: Nguyễn Văn An` |
| `R-TLMI-145 · Tên hiển thị trống thì chỉ in giá trị` | `nhan=''` → text `Nguyễn Văn An`, **không** có dấu `:` |
| `R-TLMI-146 · ô Chữ tự do in đúng chữ đã gõ` | `chu='Hàng dễ vỡ'` → text đúng như vậy |
| `R-TLMI-147 · gõ Chữ tự do ngay trong ô, > 255 thì MSG_212` | gõ 256 ký tự → `Tên hiển thị và chữ tự do tối đa 255 ký tự` |
| `R-TLMI-158 · ô trường + In đậm chỉ đậm Tên hiển thị` | → phần tử chứa `Người nhận:` có `font-weight: bold`, phần giá trị **không** |
| `R-TLMI-159 · ô Chữ tự do + In đậm thì đậm cả chữ` | → cả ô `font-weight: bold` |
| `R-TLMI-149 · kéo dòng trường thả vào ô` | mô phỏng `dragEnd` với `data.current.loai='truong'` → ô nhận trường |
| `R-TLMI-150 · nháy đúp mở hộp chọn, hai mục đầu là (Ô trống) và Chữ tự do` | dblclick → hộp hiện, mục 1 = `(Ô trống)`, mục 2 = `Chữ tự do` |
| `R-TLMI-151 · gõ trong hộp chọn lọc không phân biệt dấu` | gõ `nguoi nhan` → hiện `Người nhận` |
| `R-TLMI-173 · mũi tên di chuyển ô đang chọn` | `keyDown ArrowRight` → ô chọn dịch sang phải |
| `R-TLMI-173 · Delete xoá nội dung ô` | `keyDown Delete` → ô về `TRONG` |
| `R-TLMI-173 · Enter mở chọn trường` | `keyDown Enter` → hộp chọn hiện |
| `R-TLMI-161 · Căn đặt theo ô` | bấm `Phải` → chỉ ô đang chọn `text-align: right` |
| `R-TLMI-177 · bật lưới căn chỉnh thì kẻ đường phân ô` | tick → ô có class đường kẻ |
| `R-TLMI-178 · dấu hiệu lưới không in` | → CSS `@media print` chứa `display: none` cho class đó |
| `R-TLMI-179 · bỏ tick thì hiển thị như bản in` | bỏ tick → không còn class đường kẻ; vẫn click chọn ô được |
| `R-TLMI-235 · ô lưới không hợp lệ viền đỏ NGAY trên trang xem trước` | Chữ tự do đang sửa mà rỗng → ô có viền đỏ + chữ `Ô: Chữ tự do chưa có nội dung — nháy đúp để gõ` |
| `R-TLMI-236 · ô trống KHÔNG BAO GIỜ là lỗi` | khối toàn ô trống → badge **không** thành `Có lỗi` |
| `R-TLMI-176 · khối tự do đang bật mà mọi ô trống thì vẫn lưu được` | bấm Lưu → API **được** gọi |
| `R-TLMI-131 · các cột rộng bằng nhau` | `soCot=3` → `grid-template-columns` = `repeat(3, 1fr)` |

### `test/ThanhCongCuTuDo.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-162 · chưa chọn ô thì MỌI nút đều mờ` | → tất cả 14 nút `disabled` |
| `R-TLMI-163 · bấm B áp cho vùng đang chọn` | vùng 2 ô-trường, bấm `B` → cả hai `k` có `dam=true` trong `truongDungChung` |
| `R-TLMI-170 · thanh Hide khi khối đang chọn không phải khối tự do` | chọn khối `Tiêu đề` → thanh **không** render |
| `R-TLMI-170 · thanh có đủ 15 nút nguyên văn` | → khớp danh sách `R-TLMI-170` |
| `X8 · nhãn ngữ cảnh {Tên khối} · ô dòng {r}, cột {c}` | chọn ô (1,2) → text `Ghi chú giao hàng · ô dòng 2, cột 3` |
| `R-TLMI-171 · menu chuột phải có đủ 10 mục, 3 nhóm` | contextmenu → 10 mục theo đúng thứ tự, 2 đường ngăn |
| `R-TLMI-172 · ô Chữ tự do thì lệnh đầu menu là "Sửa chữ"` | ô Chữ tự do → mục 1 = `Sửa chữ`; ô khác → `Chọn trường dữ liệu…` |
| `R-TLMI-174 · Gộp ô mờ khi vùng < 2 ô` | 1 ô → nút `Gộp ô` `disabled` nhưng **vẫn render** (X7) |
| `R-TLMI-174 · Tách ô mờ khi ô không phải ô gộp` | như trên |
| `R-TLMI-135 · − Dòng mờ khi còn 1 dòng` | `soDong=1` → `disabled` |
| `R-TLMI-138 · Gộp ô khi vùng có 2 ô có nội dung thì hỏi MSG_404` | → hộp hiện với `Vùng chọn có 2 ô đang có nội dung…` |

### `test/KhoiTuDoInspector.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-120 · bấm Thêm khối tự do mở hộp Đặt tên khối` | → hộp hiện |
| `R-TLMI-121 · tên trống / 61 ký tự thì MSG_206` | → `Tên khối tự do không được để trống, tối đa 60 ký tự` |
| `R-TLMI-122 · khối mới đặt ngay trước khối Chữ ký` | → index khối mới = index khối Chữ ký − 1 |
| `R-TLMI-124 · thêm thành công thì toast, mở bảng chỉnh, chọn sẵn ô đầu` | → toast `MSG_104`, bảng chỉnh = khối mới, ô (0,0) đang chọn |
| `R-TLMI-125 · đủ 10 khối thì MSG_207` | → `Mỗi mẫu tối đa 10 khối tự do` |
| `R-TLMI-126 · tên khối KHÔNG in ra bản in` | → `BanInPaper` không chứa chuỗi tên khối |
| `R-TLMI-127 · sửa tên khối ở ô Tên khối trên bảng chỉnh` | gõ tên mới, blur → tên đổi ở cả dòng khối cột trái (C07) |
| `R-TLMI-128 · bảng chỉnh KHÔNG có ô Kích thước lưới và cột Vị trí` | → không tìm thấy hai thứ đó |
| `R-TLMI-166 · kho trường là danh sách phẳng` | → không có header nhóm nào |
| `R-TLMI-168 · Tìm kiếm lọc không phân biệt dấu` | gõ `so tien` → hiện `Số tiền bằng chữ` |
| `R-TLMI-169 · cột Trường dữ liệu chỉ đọc` | → không phải input |
| `R-TLMI-167 · ô mới ở phiên bản sau vào kho nhưng không chen vào khối` | catalog thêm trường → có trong kho, **không** xuất hiện trong ô nào |
| `R-TLMI-175 · Xóa khối tự do thì hỏi MSG_403` | bấm `Xóa khối này` → `Xóa khối "Ghi chú giao hàng" cùng các ô trong đó?` |
| `R-TLMI-211 · khối tự do có nút xoá ở cả hai nơi` | → `✕` ở dòng khối **và** link `Xóa khối này` |
| `C10 · trường bị xoá khỏi form thì mờ + nhãn "không còn trên form"` | catalog bỏ trường đang dùng → dòng mờ, có nhãn |

---

## 15. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR3 | `MSG_403`, `MSG_404` dùng `CommonConfirmModal` 2 nút |
| BR13 | ô `Tên khối`, `Tên hiển thị`, `Chữ tự do` — kiểm khi rời ô; `R-TLMI-181` giá trị dài tự xuống dòng |
| BR14 | phím tắt `↑↓←→` · `Delete` · `Enter` · `F2` · `Shift` + bấm |
| BR26 | toast `MSG_104`; lỗi đánh dấu tại chỗ, **không** cảnh báo mềm |
| BR50.7 (Phase 2) | `R-TLMI-165` — kho trường = mọi ô form trừ cột lưới |
