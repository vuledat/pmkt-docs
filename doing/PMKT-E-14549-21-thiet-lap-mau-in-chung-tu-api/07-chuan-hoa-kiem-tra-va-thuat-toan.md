# 07 · `F05` — Chuẩn hoá · Kiểm tra 17 dòng · Ba thuật toán

| | |
|---|---|
| Mã chức năng | `F05` |
| Luật phủ | `R-TLMI-021` · `037` · `038` · `039` · `058` · `059` · `060` · `111`…`114` · `119` · `236`…`239` · `243` · `246` · `247` · `266` |
| Quyết định gốc | `D4` `D5` `D14` |
| Class | `ChuanHoaMau` · `KiemTraMau` · `ChiaDeuDoRong` · `GiaiHuongGiay` · `CongGopDong` · `HopNhatThietLapChung` |

> Đây là chỗ **dễ code sai nhất của epic** (`R-TLMI-038` Ghi chú nguyên văn). Mọi hàm trong file này là **hàm thuần**, không chạm DB, không chạm Spring context ⇒ unit-test được 100% mà không cần Docker.

---

## §1. `ChuanHoaMau` — điều kiện để phép so sánh ở `D5` chạy đúng

Chuẩn hoá chạy **hai lần mỗi lần Lưu**: một lần trên mẫu người dùng gửi lên, một lần trên mẫu chuẩn hệ thống. Hai kết quả đem so bằng `String.equals`.

| # | Việc | Vì sao | Luật |
|---|---|---|---|
| 1 | **Chia lại độ rộng cột về 100** với mọi khối `BANG` (§3) | `INV-TLMI-005` — độ rộng đã lưu luôn hợp lệ và tổng = 100 | `R-TLMI-111` |
| 2 | **Xoá mọi khoá `null`** | `null` ≠ vắng mặt ở tầng chuỗi JSON; giữ `null` là `INV-TLMI-003` vỡ | `R-TLMI-037` |
| 3 | **Xoá khoá có giá trị bằng đúng mặc định hệ thống?** → **KHÔNG** | ⚠ **BẪY.** Ô *riêng* mà tình cờ bằng mặc định vẫn phải giữ — người dùng đã chủ động đặt nó, thiết lập chung đổi thì nó **không** đổi theo (`R-TLMI-039`) | `R-TLMI-039` |
| 4 | **Sắp khoá theo thứ tự cố định** (không phải alphabet — dùng thứ tự khai báo của record qua `ObjectMapper` cấu hình `MapperFeature.SORT_PROPERTIES_ALPHABETICALLY = false` + `@JsonPropertyOrder`) | Hai JSON cùng nội dung khác thứ tự khoá ⇒ `String.equals` sai | `D5` |
| 5 | **Đánh số lại id kỹ thuật**: `tu_do_1…n` theo thứ tự mảng, `ky_tu_do_1…n` theo thứ tự mảng | id ngẫu nhiên làm phép so sánh không bao giờ bằng | [01 §1.3](01-hop-dong-json-mau-in.md) |
| 6 | **Xoá cờ `moi`** của cột / trường vừa hợp nhất | Cờ hiển thị của FE, không phải dữ liệu mẫu | `R-TLMI-093` |
| 7 | **Xoá ô `loai = TRONG` không có định dạng** khỏi `khoi[TU_DO].o[]` | Ô vắng mặt **là** ô trống; giữ lại là hai cách biểu diễn cùng một thứ | `R-TLMI-143` |
| 8 | **Xoá `gopDong` / `gopCot` bằng 1** | vắng = 1 | [01 §4.5](01-hop-dong-json-mau-in.md) |
| 9 | **Xoá entry `truong.<ma>`** không còn ô nào trỏ tới, và entry rỗng `{}` | `R-TLMI-164` — trường chưa đặt vào ô nào thì không lưu | `R-TLMI-164` |
| 10 | **Xoá khoá `cong`** của cột **không phải cột số** | `R-TLMI-106` — cột chữ không có ô Cộng | `R-TLMI-106` |
| 11 | **Xoá `nen.doDam`** khi `nen.kieu = KHONG`; **xoá `nen.canAnh`** khi `kieu != ANH` | `R-TLMI-070` · `071` — các ô này chỉ tồn tại theo điều kiện | `R-TLMI-070` · `071` |
| 12 | **Xoá `soCotTuDongNgang`** khi `huong != TU_DONG`? → **KHÔNG** | `R-TLMI-056` ELSE: *"giá trị đã nhập **vẫn giữ**"* khi ô bị ẩn | `R-TLMI-056` |
| 13 | **Quy `tenBang` rỗng/`null`/toàn khoảng trắng về vắng mặt** | Hai cách biểu diễn "không in tên bảng" | `R-TLMI-094` |
| 14 | **`trim()`** mọi chuỗi người dùng nhập (`noiDung` tiêu đề, `tenHienThi`, `ten` khối, `tieuDe` ô ký, `noiDung` ô chữ) | Khoảng trắng thừa làm hai mẫu giống hệt thành khác nhau | — |
| 15 | **Chuẩn hoá `mauChu` về chữ thường** (`#AABBCC` → `#aabbcc`) | Cùng màu, hai chuỗi | `R-TLMI-066` |

**Chuẩn hoá KHÔNG được làm:**

| Cấm | Vì sao |
|---|---|
| Gọi `HopNhatThietLapChung` | Điền giá trị vào ô kế thừa rồi ghi ⇒ **phá `R-TLMI-037`** trực tiếp. Đây là lỗi kinh điển của epic (`R4` ở [00 §9](00-ke-hoach-tong.md)) |
| Gọi `GiaiHuongGiay` | `huong = TU_DONG` là **giá trị hợp lệ để lưu**; giải nghĩa chỉ xảy ra lúc in / vẽ xem trước |
| Thêm khoá còn thiếu bằng mặc định | Cùng lý do trên |

---

## §2. `KiemTraMau` — 17 dòng của `R-TLMI-239`, chạy **cả ở server**

`R-TLMI-246` nguyên văn Ghi chú: *"Không được tin FE đã kiểm."*

| # | Trường | Điều kiện | Message | Tầng | Luật |
|---|---|---|---|---|---|
| V01 | Tiêu đề: Nội dung | Không trống, ≤ 255 ký tự | `MSG_PMKT-E-14549_21_201` | Client / **Server** | `R-TLMI-085` |
| V02 | Tiêu đề: Cỡ chữ | Số nguyên `10…36` | `MSG_…_202` | Client / **Server** | `R-TLMI-086` |
| V03 | Bảng: cột in | Bảng đang bật phải còn ≥ 1 cột tick | `MSG_…_203` | Client / **Server** | `R-TLMI-104` · `INV-TLMI-004` |
| V04 | Bảng: Tên hiển thị của cột | Không trống, ≤ 100 | `MSG_…_204` | Client / **Server** | `R-TLMI-102` |
| V05 | Bảng: Rộng % | Số nguyên `3…90` | `MSG_…_205` | Client / **Server** | `R-TLMI-108` |
| V06 | Khối tự do: tên | Không trống, ≤ 60 | `MSG_…_206` | Client / **Server** | `R-TLMI-121` |
| V07 | Số khối tự do | ≤ 10 | `MSG_…_207` | Client / **Server** | `R-TLMI-125` · `INV-TLMI-006` |
| V08 | Số dòng một khối tự do | ≤ 20 | `MSG_…_208` | Client / **Server** | `R-TLMI-129` · `INV-TLMI-006` |
| V09 | Số cột một khối tự do | ≤ 6 | `MSG_…_216` | Client / **Server** | `R-TLMI-130` · `INV-TLMI-006` |
| V10 | Ảnh nền | jpg/png, ≤ 1 MB | `MSG_…_209` | Client / **Server** | `R-TLMI-069` — kiểm ở `A5`, xem [04](04-api-anh-nen-va-logo.md) |
| V11 | Màu chữ | Dạng `#rrggbb` | `MSG_…_210` | Client / **Server** | `R-TLMI-066` |
| V12 | Chữ ký: ô ký tự do đang bật | Tiêu đề không trống, ≤ 60 | `MSG_…_211` | Client / **Server** | `R-TLMI-189` · `INV-TLMI-010` |
| V13 | Tên hiển thị của trường; nội dung ô Chữ tự do | ≤ 255 (ô Chữ tự do **trống ⇒ tự về ô trống, KHÔNG phải lỗi**) | `MSG_…_212` | Client / **Server** | `R-TLMI-147` · `157` · `148` |
| V14 | Căn lề trên/trái/dưới/phải | `0…5`, tối đa **một chữ số lẻ** | `MSG_…_213` | Client / **Server** | `R-TLMI-061` |
| V15 | Số cột để tự động in ngang | Số nguyên `1…50`, **chỉ kiểm khi `huong = TU_DONG`** | `MSG_…_214` | Client / **Server** | `R-TLMI-057` |
| V16 | Cỡ chữ | Số nguyên `8…20` | `MSG_…_215` | **CHỈ Server** | `R-TLMI-063` |
| V17 | Quyền | Có quyền Thiết lập mẫu in của nghiệp vụ | `MSG_…_002` | **CHỈ Server** | `R-TLMI-034` |

### 2.1 Kiểm thêm (cấu trúc — không có mã message riêng, trả `400` `MAU_IN_KHONG_HOP_LE`)

| Kiểm | Luật |
|---|---|
| `schemaVersion = 2`; `maLoaiChungTu`/`maNghiepVu` khớp path | `D11` · `R-TLMI-004` |
| Đúng 1 `DAU_TRANG`, 1 `TIEU_DE`, 1 `CHU_KY`; số `BANG` = số lưới trong catalog; ≤ 10 `TU_DO` | `INV-TLMI-008` · `R-TLMI-008` |
| `maLuoi` của mỗi khối `BANG` **duy nhất** và có trong catalog | `R-TLMI-092` · `INV-TLMI-003` |
| `maCot` có trong catalog của lưới đó | `R-TLMI-101` |
| Ô lưới: `dong ∈ [0, soDong)`, `cot ∈ [0, soCot)`, `dong+gopDong ≤ soDong`, `cot+gopCot ≤ soCot`, **không hai ô chồng nhau** | `R-TLMI-136` · `180` |
| `maTruong` **duy nhất trong một khối** tự do (được lặp giữa các khối) | `R-TLMI-152` · `153` · `INV-TLMI-007` |
| 5 ô ký chức danh **đủ mặt**, `vaiTro` không trùng | `R-TLMI-182` · `192` |
| Khối `TU_DO`: `soDong ≥ 1`, `soCot ≥ 1` | quyết định **C20** · `INV-TLMI-006` |

### 2.2 Ba điều **KHÔNG phải lỗi**

| Không phải lỗi | Xử lý | Luật |
|---|---|---|
| Tổng độ rộng cột ≠ 100 | tự chia lại về 100 khi Lưu | `R-TLMI-111` |
| Ô trống trong khối tự do | bỏ qua — *"ô trống **không bao giờ** là lỗi"* | `R-TLMI-236` |
| Ô lưới không hợp lệ hiện viền đỏ trên trang xem trước | chỉ là dấu hiệu FE | `R-TLMI-235` |

Thêm hai điều nữa:

| | |
|---|---|
| Khối `TU_DO` đang bật mà **mọi ô đều trống** | vẫn lưu được (`R-TLMI-176`) |
| Khối `TIEU_DE` đang **ẩn** mà `noiDung` trống | **bỏ qua V01** (quyết định **C18**) |

**Không có cảnh báo mềm** cho lựa chọn hợp lệ nhưng bất thường (`R-TLMI-238`) ⇒ ⚠ bỏ hằng `NEN_DO_DAM_CANH_BAO = 60` của bản cũ (`cell/mau_in/internal/model/GioiHanMauIn.java:58`).

### 2.3 Thứ tự "lỗi đầu tiên" (`R-TLMI-243` + quyết định **C21**)

```
1. Mục "Thiết lập mẫu"  (Giấy và chữ → màu chữ → hình nền)     ← đứng đầu Bố cục mẫu, R-TLMI-202
2. Theo thứ tự khối trong khoi[]
   2a. Ô ở BẢNG CHỈNH của khối, từ trên xuống
   2b. Rồi ô lưới trên trang xem trước, trái→phải, trên→dưới
```

`KiemTraMau` trả `KetQuaKiemTra` mang **danh sách đầy đủ** lỗi theo thứ tự này; `MauInService` chỉ lấy **phần tử đầu** để trả về (`R-TLMI-243`). Giữ danh sách đầy đủ có ích cho log và cho test.

Mỗi `LoiMau` mang: `ma` (mã message) · `duongDan` (JSON pointer, ví dụ `khoi[2].cot[4].rong`) · `thamSo` (ví dụ `{TenBang}` của `MSG_…_203`). FE dùng `duongDan` để mở đúng khối và đặt con trỏ vào ô lỗi (`R-TLMI-244`).

---

## §3. `ChiaDeuDoRong` — thuật toán chia đều về 100% (`R-TLMI-114`)

**Ba dịp chạy:** bấm nút *Chia đều về 100%* (FE) · **tự chạy khi Lưu** (`R-TLMI-111`) · khi có **cột mới** ở phiên bản sau (`R-TLMI-093`).

### 3.1 Bốn bước, đúng thứ tự

```
1. Chỉ xét các cột đang tick in (in = true).
   Cột bỏ tick GIỮ NGUYÊN số cũ và KHÔNG tính vào tổng (R-TLMI-112).

2. rong_moi = FLOOR( rong_cu / tong_rong_cu * 100 )        ← LÀM TRÒN XUỐNG

3. thieu = 100 - SUM(rong_moi)
   Cộng toàn bộ `thieu` vào CỘT ĐANG IN CUỐI CÙNG.

4. Cột nào < 3  ⇒ nâng lên 3, và TRỪ phần nâng vào CỘT RỘNG NHẤT.
   (lặp cho tới khi không còn cột < 3)
```

> **`ELSE` của luật, in đậm trong `02-rules.md`:** ***GIỮ NGUYÊN TỶ LỆ giữa các cột — KHÔNG chia bằng nhau.*** Tên nút là *"Chia đều về 100%"* nhưng việc nó làm là **quy tỷ lệ về tổng 100**. Đây là chỗ dễ đọc nhầm nhất của cả epic.

### 3.2 Ba ca chốt của BA — **test bắt buộc**

| Vào | Ra | Giải thích |
|---|---|---|
| `40 / 40 / 40` | **`33 / 33 / 34`** | mỗi cột `40/120*100 = 33.33` → floor `33`; tổng `99`, thiếu `1` → dồn vào cột **cuối** |
| `50 / 30` | **`62 / 38`** | `50/80*100 = 62.5` → `62`; `30/80*100 = 37.5` → `37`; tổng `99`, thiếu `1` → cột cuối `37+1 = 38` |
| `10 / 10 / 10 / 10` | **`25 / 25 / 25 / 25`** | `25` chẵn, không dư |

### 3.3 Ca biên phải có test

| Vào | Ra kỳ vọng | Bước áp dụng |
|---|---|---|
| `1 / 1 / 98` (2 cột sẽ `< 3`) | `3 / 3 / 94` | Bước 4 — nâng hai cột lên `3`, trừ `4` vào cột rộng nhất |
| `100` (một cột) | `100` | — |
| Cột `in = false` có `rong = 50`, hai cột `in = true` `40/40` | `50` **giữ nguyên**, hai cột in ⇒ `50/50` | Bước 1 (`R-TLMI-112`) |
| Cột `in = true` có `rong` **vắng** | nhận phần chia | `R-TLMI-113` |
| Không cột nào `in = true` | không đổi gì — đã bị V03 chặn trước đó | `R-TLMI-104` |

### 3.4 Phạm vi khi đang lọc ô *Tìm cột*

Áp cho **mọi cột đang tick in**, **không** phụ thuộc ô *Tìm cột* — ô tìm chỉ lọc hiển thị (quyết định **C31**). Server không biết ô tìm nên điều này tự đúng ở BE; ghi ra đây để FE không làm khác.

---

## §4. `GiaiHuongGiay` — giải `huong = TU_DONG` (`R-TLMI-058` · `059` · `060`)

```
giai(mauHieuLuc) -> "DOC" | "NGANG"

if  huong == "DOC"    -> "DOC"                                      R-TLMI-060
if  huong == "NGANG"  -> "NGANG"                                    R-TLMI-060
if  huong == "TU_DONG":
      cacBang = khoi.filter(loai == "BANG" && hien == true)
      if cacBang rỗng            -> "DOC"                           R-TLMI-059
      soCotNhieuNhat = max( bang.cot.filter(in == true).size() )    ← KHÔNG TÍNH CỘT STT
      return soCotNhieuNhat >= trang.soCotTuDongNgang ? "NGANG" : "DOC"   R-TLMI-058
```

**Ba cái bẫy, nêu rõ để không code sai:**

1. **KHÔNG tính cột STT.** `inStt = true` thêm một cột lên bản in nhưng **không** được đếm (`R-TLMI-058` nguyên văn).
2. Chỉ xét khối Bảng **đang bật** (`hien = true`), không xét khối đã tắt con mắt.
3. ⚠ **Khác quy tắc Tự động của BÁO CÁO** — báo cáo xét "số cột đang hiển thị" của báo cáo (`R-TLMI-058` Ghi chú: *"đừng dùng chung code"*). Nếu sau này epic `_20` làm phần báo cáo thì viết hàm riêng.
4. `trang.soCotTuDongNgang` có thể **vắng** ⇒ phải chạy **sau** `HopNhatThietLapChung` (mặc định hệ thống `7`).

**So sánh là `>=`**, không phải `>`: *"số cột đó **≥** Số cột đã đặt ⇒ in ngang"*.

---

## §5. `CongGopDong` — cộng gộp mặt hàng khi in (`R-TLMI-119` · `266`(c))

Quyết định **C01** (khoá có thuế suất) + **C30** (phạm vi 3 loại chứng từ).

### 5.1 Điều kiện áp

```
ap = thietLapChung.quyTacIn.congGopMatHang == true
     AND provider.thuocDienCongGop() == true
```

Thiếu **một trong hai** ⇒ không gộp. `SCR:281` không nhắc lại giới hạn phạm vi, nhưng BR51.5 và `S20:160` có ⇒ **giữ giới hạn** (`R-TLMI-119` Ghi chú nguyên văn: *"Code theo SCR:281 trần sẽ gộp cả Phiếu chi, Chứng từ mua dịch vụ… ⇒ phải giữ giới hạn"*).

### 5.2 Khoá gộp

```
khoa = (maHang, donViTinh, donGia, thueSuat)                       ← C01: CÓ thuế suất
     + (soLo, hanSuDung)   nếu vật tư theo dõi theo lô
```

| Cột | Xử lý khi gộp |
|---|---|
| `soLuong` và mọi cột **`KieuTruong.SO`** | **cộng dồn** |
| Mọi cột **`KieuTruong.TIEN`** | **cộng dồn** |
| Cột thuộc khoá gộp | giữ nguyên |
| Cột khác (diễn giải, ghi chú…) | giữ của **dòng đầu tiên** trong nhóm |

### 5.3 Vị trí trong luồng

Gộp chạy **TRƯỚC** khi dựng bảng (`R-TLMI-119`), trên **bản sao** `DuLieuChungTu` — **không** ghi ngược vào DB (`R-TLMI-271`). Sau khi gộp mới:

- dựng dòng theo các cột `in = true`;
- tính lại `BangDuLieu.tong` cho dòng Cộng (`R-TLMI-097`).

### 5.4 Ca chốt phải có test

| Ca | Kỳ vọng | Luật |
|---|---|---|
| 2 dòng cùng mã hàng, cùng ĐVT, cùng đơn giá, **cùng** thuế suất | **gộp thành 1**, số lượng cộng dồn | `R-TLMI-119` · C01 |
| 2 dòng như trên nhưng **khác thuế suất** | **KHÔNG gộp**, in thành hai dòng riêng | C01 (ví dụ phủ định nguyên văn của BA) |
| 2 dòng cùng mọi thứ, **khác số lô** (vật tư theo dõi lô) | **KHÔNG gộp** | `R-TLMI-119` |
| Phiếu chi (`thuocDienCongGop() = false`) + cờ chung **bật** | **KHÔNG gộp** | C30 |
| Hoá đơn + cờ chung **tắt** | **KHÔNG gộp** | `R-TLMI-266`(c) |

---

## §6. `HopNhatThietLapChung` — hàm CHỈ ĐỌC

```java
/** R-TLMI-038 · R-TLMI-264 — điền mọi khoá VẮNG bằng thiết lập chung TẠI THỜI ĐIỂM GỌI. */
MauInJson hopNhat(MauInJson mau, ThietLapChungJson chung);
```

| Nhóm khoá | Nguồn khi vắng |
|---|---|
| `trang.kho` · `huong` · `soCotTuDongNgang` · `leTren/leDuoi/leTrai/lePhai` · `font` · `coChu` | `chung.giayVaChu.*`, thiếu nữa ⇒ **mặc định hệ thống** ([02 §2.1](02-hop-dong-json-thiet-lap-chung.md)) |
| `khoi[DAU_TRANG].dong.<7 khoá>` | `chung.dauTrang.<khoá>` | 
| `khoi[CHU_KY].o[vaiTro].tieuDe` | `HoSoDonVi.nguoiKy[vaiTro].tieuDe` |

**Ba luật cứng:**

1. **Chỉ gọi khi ĐỌC** — `A1` **không** gọi (trả mẫu thô), `A3` và `A9` **có** gọi. Không có đường gọi nào từ `MauInService.luu`.
2. Kết quả **không bao giờ** được ghi xuống DB. Kiểu trả về nên là một record khác (`MauInHieuLuc`) để trình biên dịch chặn nhầm lẫn — nhưng nếu dùng chung `MauInJson` thì phải có test `R_TLMI_037_luuOTheoChungThiKhoaVangMat` canh.
3. Ô **riêng** (khoá có mặt) **không bị đụng** — thiết lập chung đổi cũng không ảnh hưởng (`R-TLMI-039`).

---

## §7. Danh sách unit test của `F05`

Mọi test `@Tag("unit")`, tên mang chính mã luật.

| Class test | Test | Luật |
|---|---|---|
| `ChiaDeuDoRongTest` | `R_TLMI_114_chia_40_40_40_thanh_33_33_34` | `R-TLMI-114` |
| | `R_TLMI_114_chia_50_30_thanh_62_38` | `R-TLMI-114` |
| | `R_TLMI_114_chia_10_10_10_10_thanh_25_moi_cot` | `R-TLMI-114` |
| | `R_TLMI_114_cotDuoi3ThiNangLen3VaTruCotRongNhat` | `R-TLMI-114` |
| | `R_TLMI_112_cotBoTickKhongTinhVaoTong` | `R-TLMI-112` |
| | `R_TLMI_113_tickLaiCotDoRongTrongThiNhanPhanChia` | `R-TLMI-113` |
| | `R_TLMI_111_tuChiaLaiKhiLuuKhongPhaiLoi` | `R-TLMI-111` · `INV-TLMI-005` |
| `GiaiHuongGiayTest` | `R_TLMI_058_tuDongXetBangDangBatNhieuCotNhat` | `R-TLMI-058` |
| | `R_TLMI_058_khongTinhCotStt` | `R-TLMI-058` |
| | `R_TLMI_058_soCotBangSoDaDatThiInNgang` (biên `>=`) | `R-TLMI-058` |
| | `R_TLMI_059_khongCoBangNaoBatThiInDoc` | `R-TLMI-059` |
| | `R_TLMI_060_docHoacNgangThiInDungHuongDo` | `R-TLMI-060` |
| `CongGopDongTest` | `R_TLMI_119_gopKhiTrungMaHangDvtDonGiaThueSuat` | `R-TLMI-119` |
| | `R_TLMI_119_khacThueSuatThiKhongGop` | `R-TLMI-119` · C01 |
| | `R_TLMI_119_khacSoLoThiKhongGop` | `R-TLMI-119` |
| | `R_TLMI_266_loaiNgoaiDienCongGopThiKhongGop` | `R-TLMI-266` · C30 |
| | `R_TLMI_119_gopChayTruocKhiDungBang` | `R-TLMI-119` |
| `ChuanHoaMauTest` | `R_TLMI_037_xoaMoiKhoaNull` | `R-TLMI-037` · `INV-TLMI-003` |
| | `R_TLMI_039_khongXoaKhoaCoGiaTriBangMacDinh` | `R-TLMI-039` |
| | `R_TLMI_143_xoaOTrongKhongDinhDang` | `R-TLMI-143` |
| | `R_TLMI_164_xoaTruongKhongConONaoTroToi` | `R-TLMI-164` |
| | `R_TLMI_106_xoaKhoaCongCuaCotKhongPhaiSo` | `R-TLMI-106` |
| | `R_TLMI_056_giuSoCotTuDongNgangKhiHuongKhacTuDong` | `R-TLMI-056` |
| | `ChuanHoaMau_haiMauGiongNhauThiRaCungMotChuoi` | D5 |
| `KiemTraMauTest` | `R_TLMI_239_du17Dong` (mỗi dòng một case) | `R-TLMI-239` |
| | `R_TLMI_243_traVeDungLoiDauTienTheoThuTu` | `R-TLMI-243` · C21 |
| | `R_TLMI_236_oTrongKhongBaoGioLaLoi` | `R-TLMI-236` |
| | `R_TLMI_176_khoiTuDoMoiOTrongVanLuuDuoc` | `R-TLMI-176` |
| | `R_TLMI_238_khongCoCanhBaoMem` | `R-TLMI-238` |
| | `C18_khoiTieuDeAnThiBoQuaKiemNoiDung` | quyết định C18 |
| | `INV_TLMI_007_motTruongToiDaMotOTrongMotKhoi` | `INV-TLMI-007` |
| | `R_TLMI_153_cungTruongDungONhieuKhoiThiDuoc` | `R-TLMI-153` |
| | `R_TLMI_136_haiOChongNhauThiKhongHopLe` | `R-TLMI-136` |
| `HopNhatThietLapChungTest` | `R_TLMI_038_khoaVangThiLayThietLapChungLucGoi` | `R-TLMI-038` |
| | `R_TLMI_039_khoaCoMatThiKhongDoiTheoThietLapChung` | `R-TLMI-039` |
| | `R_TLMI_037_hopNhatKhongDuocGoiTuLuongLuu` (kiểm bằng kiến trúc / ArchUnit) | `R-TLMI-037` |
