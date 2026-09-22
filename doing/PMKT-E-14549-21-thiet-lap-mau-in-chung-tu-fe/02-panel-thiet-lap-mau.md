# 02 · Bảng chỉnh *Thiết lập mẫu* — Giấy và chữ + Riêng của mẫu

| | |
|---|---|
| Mã màn | `SCR_ThietLapMauIn` — mục `Thiết lập mẫu` của cột phải |
| Nguồn SCR | `SCR:88-160` · `SCR:254-279` |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` |
| Figma | frame **1** `71956:288872` (Hình nền = Ảnh tải lên) · frame **1b** `72218:690704` (Hình nền = Khung viền) |
| File chính | `@domain-kit/mauIn/components/inspector/ThietLapMauInspector.tsx` |
| Luật phủ | `R-TLMI-036…075` (nhóm C · D · E) |

---

## 1. Bố cục (Figma frame 1)

```
Thiết lập mẫu                                          ← tiêu đề bảng chỉnh
─────────────────────────────────────────────────────
Giấy và chữ                        Theo thiết lập chung ← link ĐỎ, mức NHÓM
Khổ giấy                 Hướng giấy
[ A4            ▾ ]      [ Tự động       ▾ ]
Căn lề (cm)
Trên [1]  Trái [1,5]  Dưới [1]  Phải [1]
Font chữ                 Cỡ chữ cơ sở
[ Times New Roman ▾ ]    [ 12           ▾ ]
Mở Cấu hình báo cáo chứng từ                          ← link ĐỎ
─────────────────────────────────────────────────────
Riêng của mẫu
Màu chữ
[■][■][■][■][■][■][■][■][■][■]  [ #000000 ]          ← 10 ô màu + ô hex
Hình nền                 Độ đậm (5–100%)
[ Ảnh tải lên   ▾ ]      [ 20 ]
Căn ảnh                                               ← CHỈ khi Hình nền = Ảnh tải lên
(•) Giữa trang   ( ) Toàn trang
Ảnh (jpg/png ≤ 1MB)                                   ← CHỈ khi Hình nền = Ảnh tải lên
[⇧ Chọn ảnh…]  logo.png   Xóa
```

⚠ **X1** — đếm trên Figma frame 1 và 1b: **10 ô màu** preset, khớp `R-TLMI-066`. Ghi chú khảo sát
`A0-figma.md §4.1` chép nhầm "9 ô màu" — sửa ghi chú, không sửa luật.

---

## 2. Đặc tả UI từ Figma

| Thành phần | Component | Kiểu | Biến thể / trạng thái | Luật |
|---|---|---|---|---|
| Nhóm `Giấy và chữ` | `PropSection` (`base/index.ts:226`) | — | slot phải = link `Theo thiết lập chung` | `R-TLMI-040` |
| `Khổ giấy` | `CommonSelect` (`base/index.ts:691`) | select | `A3` · `A4` · `A5` | `R-TLMI-054` |
| `Hướng giấy` | `CommonSelect` | select | `Dọc` · `Ngang` · `Tự động` | `R-TLMI-055` |
| `Số cột để tự động in ngang` | `CommonNumberInput` (`base/index.ts:235`) | số nguyên 1-50 | **Show CHỈ KHI** `Hướng giấy = Tự động` | `R-TLMI-056` · `R-TLMI-057` |
| `Căn lề (cm)` — `Trên` `Trái` `Dưới` `Phải` | 4 × `CommonNumberInput` | số 0-5, **tối đa 1 chữ số lẻ** | 4 ô nằm cùng hàng | `R-TLMI-061` |
| `Font chữ` | `CommonSelect` | select | `Times New Roman` · `Arial` — **chỉ hai** | `R-TLMI-062` |
| `Cỡ chữ cơ sở` | `CommonSelect` | select số nguyên 8-20 | ô **chọn từ danh sách** ⇒ FE không nhập sai được | `R-TLMI-063` |
| link `Mở Cấu hình báo cáo chứng từ` | `CommonButton` variant link | chữ đỏ | ⚠ **Q4** — chưa có đích | `R-TLMI-050` |
| Nhóm `Riêng của mẫu` | `PropSection` | — | **không** có link `Theo thiết lập chung` | `R-TLMI-064` |
| `Màu chữ` | `CommonColorPicker` (`base/index.ts:269`) | 10 ô preset + ô hex | mặc định `#000000` | `R-TLMI-064` · `R-TLMI-066` |
| `Hình nền` | `CommonSelect` | select | `Không` · `Khung viền` · `Ảnh tải lên` | `R-TLMI-067/068/069` |
| `Độ đậm (5–100%)` | `CommonNumberInput` | số 5-100 | **Show CHỈ KHI** `Hình nền ≠ Không`; mặc định **20** | `R-TLMI-070` · `R-TLMI-072` |
| `Căn ảnh` | `CommonRadio.Group` (`base/index.ts:257`) | radio | `Giữa trang` · `Toàn trang`; **Show CHỈ KHI** `Hình nền = Ảnh tải lên` | `R-TLMI-071` · `R-TLMI-073/074` |
| `Ảnh (jpg/png ≤ 1MB)` | nút `⇧ Chọn ảnh…` + tên tệp + link `Xóa` | file | **Show CHỈ KHI** `Hình nền = Ảnh tải lên` | `R-TLMI-069` · `R-TLMI-071` |

---

## 3. Kế thừa — **chỗ dễ code sai nhất** (D5)

### 3.1 Hai trạng thái

| Trạng thái | Nghĩa | Trong JSON |
|---|---|---|
| **theo chung** | giá trị đọc lại từ *Cấu hình báo cáo chứng từ* **tại thời điểm in / vẽ xem trước** | khoá **VẮNG MẶT** |
| **riêng** | giá trị của mẫu; thiết lập chung đổi **không ảnh hưởng** | khoá **có mặt** |

`R-TLMI-036` (hai trạng thái) · `R-TLMI-037` (**tuyệt đối không copy giá trị đang hiển thị**) ·
`R-TLMI-038` (theo chung đọc lại **tại thời điểm in**) · `R-TLMI-039` (riêng thì đứng yên) ·
chốt **C28** (khoá vắng mặt = theo chung).

### 3.2 Sáu ô thuộc nhóm kế thừa

`Khổ giấy` · `Hướng giấy` · `Căn lề (4 số)` · `Font chữ` · `Cỡ chữ cơ sở` (+ `Số cột để tự động in ngang`
khi hiện). `R-TLMI-053`: nhóm **luôn hiện đủ sáu ô kèm giá trị đang dùng** — dù đang theo chung.

### 3.3 Cách hiển thị và ghi

```ts
// ĐÚNG
const khoGiay = mau.trang.khoGiay ?? chung.khoGiay          // hiển thị
onChange: (v) => capNhatTrang({ khoGiay: v })               // ghi ⇒ hoá RIÊNG
veTheoChung(['khoGiay','huongGiay','le','font','coChu'])    // xoá khoá ⇒ về THEO CHUNG

// SAI — cấm tuyệt đối
const khoGiay = mau.trang.khoGiay                           // mất giá trị hiển thị
z.object({ khoGiay: z.enum([...]).default('A4') })          // .default() biến ô thành RIÊNG âm thầm
capNhatTrang({ ...chung })                                  // copy thiết lập chung vào mẫu
```

### 3.4 Nút `Theo thiết lập chung`

| Luật | Nội dung |
|---|---|
| `R-TLMI-040` | nút ở **mức nhóm** `Giấy và chữ` — đưa **cả nhóm** về theo chung |
| `R-TLMI-041` | bấm nút là **một bước Hoàn tác được** |
| `R-TLMI-042` | **không có cách** đưa **riêng một ô** về theo chung — ⚠ rủi ro UX, chốt **C16**, xem Q2 |
| `R-TLMI-045` | trạng thái theo chung / riêng **không có nhãn riêng từng ô**, không đổi Show/Hide — **không tự thêm UI** |

### 3.5 Những thứ **LUÔN** theo thiết lập chung (mẫu không sửa được)

| Hạng mục | Luật |
|---|---|
| Người ký: tiêu đề mặc định, tên người ký, cờ *In tên người ký* | `R-TLMI-046` (chốt **C04**: riêng *Tiêu đề in ra* thì mẫu **sửa được**) |
| Ba quy tắc in chứng từ (cho in chưa ghi sổ · cho in đã khoá sổ · cộng gộp mặt hàng) | `R-TLMI-047` |
| Định dạng khối đầu trang (căn lề khối, lặp trang sau) | `R-TLMI-049` |

Mục **"Bố cục mặc định của báo cáo"** của thiết lập chung **KHÔNG áp cho chứng từ** (`R-TLMI-048`) —
không đọc, không hiển thị.

### 3.6 Ba liên kết

| Link | Mở gì | Luật | Ghi chú |
|---|---|---|---|
| `Mở Cấu hình báo cáo chứng từ` | màn cấu hình chung | `R-TLMI-050` | ⚠ **Q4** — epic `_20` chưa có màn |
| `Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in` | đúng mục *Thông tin trên bản in* | `R-TLMI-051` | ở panel *Thông tin đầu trang* — xem file `03` |
| `Thiết lập người ký` | màn thiết lập người ký | `R-TLMI-052` | ở panel *Chữ ký* — xem file `06`. **Có thật**: `client/src/features/heThong/thongTinCongTy/components/NguoiKyTable.tsx` |

---

## 4. Bảng trường

| Trường | Khoá i18n | Field API | Kiểu | Định dạng | Mặc định | Kế thừa? | Luật |
|---|---|---|---|---|---|---|---|
| Khổ giấy | `thietLapMau.khoGiay` | `trang.khoGiay` | `'A3'\|'A4'\|'A5'` | select | theo chung | ✔ | `R-TLMI-054` |
| Hướng giấy | `thietLapMau.huongGiay` | `trang.huongGiay` | `'DOC'\|'NGANG'\|'TU_DONG'` | select | theo chung | ✔ | `R-TLMI-055` |
| Số cột để tự động in ngang | `thietLapMau.soCotTuDongNgang` | `trang.soCotTuDongNgang` | int | 1-50 | theo chung | ✔ | `R-TLMI-057` |
| Lề trên | `thietLapMau.leTren` | `trang.le.tren` | number | 0-5, 1 chữ số lẻ | theo chung | ✔ | `R-TLMI-061` |
| Lề trái | `thietLapMau.leTrai` | `trang.le.trai` | number | như trên | theo chung | ✔ | `R-TLMI-061` |
| Lề dưới | `thietLapMau.leDuoi` | `trang.le.duoi` | number | như trên | theo chung | ✔ | `R-TLMI-061` |
| Lề phải | `thietLapMau.lePhai` | `trang.le.phai` | number | như trên | theo chung | ✔ | `R-TLMI-061` |
| Font chữ | `thietLapMau.font` | `trang.font` | `'TIMES_NEW_ROMAN'\|'ARIAL'` | select | theo chung | ✔ | `R-TLMI-062` |
| Cỡ chữ cơ sở | `thietLapMau.coChu` | `trang.coChu` | int | 8-20 | theo chung | ✔ | `R-TLMI-063` |
| Màu chữ | `thietLapMau.mauChu` | `trang.mauChu` | `#rrggbb` | 10 preset + hex | **`#000000`** | ❌ **riêng** | `R-TLMI-064` · `R-TLMI-066` |
| Hình nền | `thietLapMau.hinhNen` | `trang.nen.kieu` | `'KHONG'\|'KHUNG_VIEN'\|'ANH'` | select | `KHONG` | ❌ riêng | `R-TLMI-067/068/069` |
| Độ đậm | `thietLapMau.doDam` | `trang.nen.doDam` | int | 5-100 | **20** | ❌ riêng | `R-TLMI-072` |
| Căn ảnh | `thietLapMau.canAnh` | `trang.nen.canAnh` | `'GIUA_TRANG'\|'TOAN_TRANG'` | radio | `GIUA_TRANG` | ❌ riêng | `R-TLMI-073/074` |
| Ảnh | `thietLapMau.anh` | `anhNen` (multipart riêng) | file | jpg/png ≤ 1MB | — | ❌ riêng | `R-TLMI-069` · chốt **C08** |

⚠ **Ảnh nền KHÔNG nằm trong JSON** — chốt **C08**: lưu cột `bytea` trên bảng, tải lên bằng **multipart,
endpoint riêng**. JSON chỉ giữ cờ `nen.kieu = 'ANH'`.

---

## 5. Hành vi & sự kiện

| Thao tác | Điều kiện hiện | Việc làm | Luật |
|---|---|---|---|
| Đổi `Hướng giấy` → `Tự động` | luôn | **hiện** ô `Số cột để tự động in ngang` | `R-TLMI-056` |
| Đổi `Hướng giấy` → `Dọc`/`Ngang` | luôn | **ẩn** ô đó; giá trị vẫn giữ trong mẫu | `R-TLMI-056` |
| Đổi `Hình nền` → `Không` | luôn | **ẩn** `Độ đậm`, `Căn ảnh`, `Ảnh`; trang **không in hình nền** | `R-TLMI-067` · `R-TLMI-070` |
| Đổi `Hình nền` → `Khung viền` | luôn | **hiện** `Độ đậm`; **ẩn** `Căn ảnh` + `Ảnh`; trang kẻ khung quanh mép **theo màu chữ** | `R-TLMI-068` · Figma 1b |
| Đổi `Hình nền` → `Ảnh tải lên` | luôn | **hiện** cả `Độ đậm`, `Căn ảnh`, `Ảnh` | `R-TLMI-071` |
| Bấm `⇧ Chọn ảnh…` | `Hình nền = Ảnh tải lên` | mở file picker `accept=".jpg,.jpeg,.png"`; sai định dạng / > 1MB ⇒ `MSG_209` **ngay khi chọn tệp** | `R-TLMI-069` |
| Bấm `Xóa` cạnh tên tệp | có ảnh | gỡ ảnh; `Hình nền` **giữ nguyên** `Ảnh tải lên` (trở thành chưa có ảnh) | — |
| Gõ mã màu sai dạng | luôn | `MSG_210` khi **rời ô** | `R-TLMI-066` |
| Bấm `Theo thiết lập chung` | luôn | xoá 5-6 khoá của nhóm; **một bước undo** | `R-TLMI-040/041` |
| Bấm link `Mở Cấu hình báo cáo chứng từ` | ⚠ Q4 | chưa có đích — đề xuất **ẩn link** | `R-TLMI-050` |

**Hình nền vẽ DƯỚI mọi khối** (`R-TLMI-075` · `R-TLMI-263`) ⇒ `z-index` thấp nhất trong `BanInPaper`.
**Màu chữ áp cho toàn bộ chữ VÀ đường kẻ, trừ logo** (`R-TLMI-065`) ⇒ đặt thành CSS custom property
`--mauIn-mau-chu` ở gốc trang giấy, mọi `border` của bảng dùng `currentColor`.

**Hướng `Tự động`** (`R-TLMI-058/059/060`) là việc **BE** khi dựng bản in: xét khối Bảng **đang bật** có
nhiều cột in nhất; không có khối Bảng nào bật ⇒ **in dọc**. FE chỉ hiển thị trang xem trước theo kết quả
BE trả về hoặc tính lại cùng công thức trong `helpers/trangGiay.ts`.

---

## 6. Validation phía FE

| # | Trường | Điều kiện | Message (nguyên văn) | Thời điểm | Tầng | Luật |
|---|---|---|---|---|---|---|
| V10 | Ảnh nền | jpg/png, ≤ 1MB | `Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB` | **khi chọn tệp** | Client/Server | `R-TLMI-069` |
| V11 | Màu chữ | dạng `#rrggbb` | `Mã màu phải có dạng #rrggbb` | rời ô, khi Lưu | Client/Server | `R-TLMI-066` |
| V14 | Căn lề trên/trái/dưới/phải | số 0-5, **tối đa 1 chữ số lẻ** | `Căn lề phải là số từ 0 đến 5 cm` | rời ô, khi Lưu | Client/Server | `R-TLMI-061` |
| V15 | Số cột để tự động in ngang | int 1-50, **chỉ kiểm khi** `Hướng giấy = Tự động` | `Số cột để tự động in ngang phải là số nguyên từ 1 đến 50` | rời ô, khi Lưu | Client/Server | `R-TLMI-057` |
| V16 | Cỡ chữ cơ sở | int 8-20 | `Cỡ chữ phải là số nguyên từ 8 đến 20` | khi Lưu | **Server** (ô chọn từ danh sách) | `R-TLMI-063` |

⚠ **Bảng kiểm `R-TLMI-239` KHÔNG có dòng nào cho `Độ đậm` (5-100 %)** — ghi nhận ở `§Z` của
`02-rules.md`. Đề xuất: FE vẫn ràng `min=5 max=100` trên `CommonNumberInput` nhưng **không** đưa vào
trạng thái `Có lỗi` (vì không có mã message), và **không** tự đặt luật mới.

---

## 7. Phân bổ file

| Việc | File |
|---|---|
| Ráp 2 nhóm | `components/inspector/ThietLapMauInspector.tsx` |
| Nhóm kế thừa + link `Theo thiết lập chung` | `components/inspector/GiayVaChuGroup.tsx` |
| Nhóm riêng (màu · nền · độ đậm · căn ảnh · ảnh) | `components/inspector/RiengCuaMauGroup.tsx` |
| `giaTriHieuDung` · `laTheoChung` · `veTheoChung` | `helpers/keThua.ts` |
| Ràng V10/V11/V14/V15 | `helpers/kiemTraMau.ts` |
| Hằng `KHO_GIAY` · `HUONG_GIAY` · `FONT` · `CO_CHU` · `MAU_PRESET` (10) · `GIOI_HAN_LE` · `GIOI_HAN_DO_DAM` | `constants/constants.ts` |
| Tính hướng `Tự động` cho xem trước | `helpers/trangGiay.ts` |

---

## 8. Kiểm thử

### `test/keThua.test.ts` (`node`)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-036 · hai trạng thái theo chung / riêng` | `laTheoChung(mau,'khoGiay')` = `true` khi khoá vắng, `false` khi có |
| `R-TLMI-037 · ô theo chung ghi trống khi Lưu` | mẫu chưa đụng `khoGiay` → payload **không có** khoá `khoGiay` |
| `R-TLMI-039 · ô riêng giữ giá trị của mẫu` | `khoGiay='A5'`, `chung.khoGiay='A4'` → `giaTriHieuDung()` = `'A5'` |
| `R-TLMI-053 · nhóm luôn hiện đủ giá trị đang dùng` | mẫu rỗng, `chung` đủ → `giaTriHieuDung()` trả giá trị của `chung` cho cả 6 ô |
| `R-TLMI-040 · nút đưa CẢ NHÓM về theo chung` | mẫu có 5 khoá riêng → `veTheoChung(nhomGiayVaChu)` → cả 5 khoá **vắng** |
| `R-TLMI-042 · không có API đưa riêng một ô về chung` | `helpers/keThua.ts` **không** export hàm nào nhận đúng một khoá đơn lẻ (kiểm bằng signature) |
| `R-TLMI-049 · định dạng khối đầu trang luôn theo chung` | mẫu **không** có khoá căn lề khối đầu trang |

### `test/riengCuaMau.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-056 · Số cột tự động in ngang chỉ hiện khi Hướng = Tự động` | `Dọc` → ô **không** render; đổi sang `Tự động` → ô render |
| `R-TLMI-054 · Khổ giấy chỉ nhận A3/A4/A5` | select có đúng 3 option |
| `R-TLMI-055 · Hướng giấy chỉ nhận Dọc/Ngang/Tự động` | select có đúng 3 option |
| `R-TLMI-062 · Font chỉ Times New Roman hoặc Arial` | select có đúng 2 option |
| `R-TLMI-063 · Cỡ chữ là ô chọn 8-20` | select có 13 option (8…20) |
| `R-TLMI-066 · 10 ô màu preset + ô hex` | render → **10** nút màu + 1 ô nhập |
| `R-TLMI-066 · gõ mã sai dạng thì báo MSG_210` | gõ `#12`, blur → hiện `Mã màu phải có dạng #rrggbb` |
| `R-TLMI-067 · Hình nền = Không thì không in hình nền` | chọn `Không` → `BanInPaper` không render lớp nền |
| `R-TLMI-068 · Khung viền kẻ khung theo màu chữ` | chọn `Khung viền`, màu `#FF0000` → khung có `border-color` = màu chữ |
| `R-TLMI-070 · Độ đậm chỉ hiện khi Hình nền ≠ Không` | `Không` → ô ẩn; `Khung viền` → ô hiện |
| `R-TLMI-071 · Căn ảnh + Ảnh chỉ hiện khi Ảnh tải lên` | `Khung viền` → cả hai ẩn; `Ảnh tải lên` → cả hai hiện |
| `R-TLMI-072 · Độ đậm mặc định 20` | mẫu mới → ô hiện `20` |
| `R-TLMI-069 · chọn tệp sai định dạng thì báo MSG_209` | chọn `.gif` → hiện `Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB` |
| `R-TLMI-069 · tệp > 1MB thì báo MSG_209` | chọn png 1,2 MB → như trên |
| `R-TLMI-075 · hình nền vẽ dưới mọi khối` | → lớp nền có `z-index` nhỏ hơn mọi khối |
| `R-TLMI-065 · màu chữ áp cả đường kẻ, trừ logo` | đổi màu → bảng có `border-color` đổi theo; `img` logo **không** đổi |
| `R-TLMI-050/051/052 · ba liên kết` | render → có đúng 3 link với nguyên văn nhãn |

### `test/kiemTraMau.test.ts` (`node`) — phần thuộc file này

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-061 · căn lề biên 0 và 5 hợp lệ` | `0`, `5` → không lỗi |
| `R-TLMI-061 · căn lề 5,1 và 1,25 không hợp lệ` | → `MSG_213` (5,1 quá biên; 1,25 quá 1 chữ số lẻ) |
| `R-TLMI-057 · số cột 1 và 50 hợp lệ, 0 và 51 không` | → `MSG_214` cho 0 và 51 |
| `R-TLMI-057 · Hướng ≠ Tự động thì KHÔNG kiểm số cột` | `Dọc` + `soCot=0` → **không** lỗi |
| `R-TLMI-063 · cỡ chữ 8 và 20 hợp lệ, 7 và 21 không` | → `MSG_215` (tầng Server) |

---

## 9. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR13 | mọi ô của bảng chỉnh; kiểm khi rời ô |
| BR26 | message lỗi tại chỗ, không cảnh báo mềm (`R-TLMI-238`) |
| BR51.5 (Phase 2) | mẫu dùng chung cả đơn vị |
| BR50.6 (Phase 2) | mẫu không khai `ChiNhanhId` |
