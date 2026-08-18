# F03 — Chỉnh sửa thiết lập khóa sổ

> Quay lại [00-ke-hoach-tong.md](00-ke-hoach-tong.md) · liên quan chặt với [02-tao-thiet-lap-khoa-so.md](02-tao-thiet-lap-khoa-so.md)

| Mục | Nội dung |
|---|---|
| Use case | `PMKT-U-11303_ChinHSuaThietLapKhoaSo` |
| Màn hình | `SCR_ThietLapNgayKhoaSo.md` (chế độ Sửa) + `SCR_XemDanhSachThietLapKhoaSo.md` (icon Bút) |
| Endpoint | **A5** `PUT /api/he-thong/khoa-so/{id}` |
| Quyền | `HTKhoaSo.Edit` — **cộng thêm** `HTKhoaSo.Execute` khi `isTuDong = false` |
| Nguồn | **Override** `BaseCrudController.update` |

---

## 1. Sửa khác Tạo ở đúng ba điểm

`UC_ChinHSuaThietLapKhoaSo.md:8-10`: *"Cho phép sửa tất cả các trường: Phạm vi, Loại chứng từ, Người dùng, Ngày khóa sổ… Khi lưu: hệ thống validate đầy đủ, ghi đè bản ghi cũ"*.

⇒ Body **giống hệt** A4 (`LuuThietLapKhoaSoRequest`), toàn bộ validation V1…V10 và kiểm giao thoa của [F02 §3](02-tao-thiet-lap-khoa-so.md) **áp nguyên**. Ba khác biệt:

| # | Khác biệt | Vì sao |
|---|---|---|
| **E1** | Đích của thao tác là **bản ghi `{id}`**, không phải bản ghi khớp hash | Người dùng bấm sửa trên một dòng cụ thể |
| **E2** | **Phạm vi có thể ĐỔI** ⇒ `pham_vi_hash` phải tính lại; bản ghi sau khi sửa có thể **đụng** một bản ghi khác đang tồn tại | §2 |
| **E3** | Có **optimistic lock** — dữ liệu người dùng cầm trên popup có thể đã cũ | §3 |

**Vì sao KHÔNG gộp A4 và A5 thành một endpoint upsert:** hai thao tác cần **hai mã quyền khác nhau** (`Create` vs `Edit`, BR25) và **hai messageId khác nhau** (`_019` vs `_020`). Gộp lại thì phải suy quyền và message từ việc `id` có null hay không — một nhánh ngầm mà không test nào nhìn thấy trực tiếp.

---

## 2. Sửa làm đổi phạm vi — ba nhánh

Sau khi sửa, phạm vi mới (`hashMoi`) có thể:

| Nhánh | Tình huống | Xử lý |
|---|---|---|
| **N1** | `hashMoi == hashCũ` (phạm vi không đổi, chỉ đổi ngày / chu kỳ) | Cập nhật thẳng bản ghi `{id}` |
| **N2** | `hashMoi` **chưa** thuộc bản ghi nào khác trong cùng `nhom_ban_ghi` | Cập nhật bản ghi `{id}` + tính lại `pham_vi_hash` + đồng bộ 2 bảng con |
| **N3** | `hashMoi` **đã** thuộc một bản ghi khác `{idKhac}` cùng `nhom_ban_ghi` | **409 `TRUNG_PHAM_VI`** — xem bên dưới |

Với **N3**, có hai cách xử lý và cần chốt:

| | Phương án A — ghi đè `{idKhac}` rồi xoá mềm `{id}` | **Phương án B (chọn) — chặn 409, yêu cầu người dùng xoá/sửa bản ghi kia trước** |
|---|---|---|
| Người dùng thấy gì | Sửa một dòng, hai dòng biến mất, một dòng lạ thay đổi | Thông báo rõ: phạm vi này đã có bản ghi khác |
| Truy vết | Khó — một thao tác Sửa lại sinh ra một lần xoá không ai yêu cầu | Rõ ràng |
| Đúng BA? | BA **không mô tả** ca này | BA cũng không mô tả — nhưng chặn là lựa chọn không phá dữ liệu |
| Rủi ro | Xoá dữ liệu ngoài ý muốn | Người dùng phải thao tác 2 lần. **Chốt an toàn**: message chỉ đích danh bản ghi đang chiếm phạm vi để họ biết sửa cái nào |

Chọn **B**. `messageId` dùng lại `MSG_PMKT-E-07528_027` (giao thoa/trùng phạm vi) vì đó là mã BA đã cấp cho đúng ngữ nghĩa "phạm vi này đã có bản ghi khóa sổ" — không bịa mã mới. Ghi vào **Q9** để BA xác nhận cách dùng lại mã này.

Ba nhánh N1/N2/N3 vẫn chạy **trong advisory lock theo phạm vi** như [F02 §5](02-tao-thiet-lap-khoa-so.md), nhưng phải khoá **cả hai** hash (cũ và mới) theo thứ tự tăng dần để tránh deadlock khi hai request sửa chéo nhau.

---

## 3. Optimistic lock

Bản ghi kế thừa `AggregateRootEntity` ⇒ có `@Version phien_ban` (`AggregateRootEntity.java:18-22`). Hibernate tự nối `WHERE phien_ban = ?` vào UPDATE và ném `OptimisticLockingFailureException` → `GlobalExceptionHandler.java:91` trả **409 `STALE_DATA`**.

Ngoài ra, request **được phép** gửi thêm token `ngayCapNhat` (đúng khuôn `DeleteRequest.updatedAt` mà base đang dùng cho DELETE — `BaseCrudController.java:159-165`) để chặn sớm hơn, trước cả khi chạy validation. `AbstractCrudService.kiemTraLock` (`AbstractCrudService.java:145-155`) đã cài sẵn logic so bằng epoch-milli; tái dùng, không viết lại.

**Cảnh báo cài đặt**: sửa chỉ chạm **dòng con** (đổi danh sách loại CT mà không đổi gì trên header) sẽ **không** làm Hibernate tăng `phien_ban`. Phải gọi `entity.touch()` (`BaseEntity.java:74-76`) — nếu quên, hai người cùng sửa danh sách loại CT sẽ ghi đè nhau im lặng. Đây đúng là ca mà javadoc `AggregateRootEntity.java:12-15` cảnh báo.

---

## 4. Hợp đồng API

### 4.1 A5 — `PUT /api/he-thong/khoa-so/{id}`

Request: **y hệt A4** (`LuuThietLapKhoaSoRequest`) + trường tuỳ chọn:

```jsonc
{
  "…": "… các trường như A4 …",
  "ngayCapNhat": "2026-05-30T08:12:44Z"    // tuỳ chọn — token optimistic-lock; không gửi = bỏ qua kiểm
}
```

```jsonc
// Response 200
{
  "data": { /* ThietLapKhoaSoDto sau khi sửa */ },
  "message": "Thiết lập khóa sổ đã được cập nhật thành công",
  "messageId": "MSG_PMKT-E-07528_020"
}
```

| HTTP | Mã lỗi | messageId | Khi nào |
|---|---|---|---|
| 400 | `THIEU_*` | `MSG_..._005/_006/_007/_015/_017/_018/_022` | V1…V10 — [F02 §3.1](02-tao-thiet-lap-khoa-so.md) |
| 404 | `NOT_FOUND` | `MSG_CORE_CRUD_001` | id không tồn tại hoặc đã xoá mềm |
| 409 | `GIAO_THOA_PHAM_VI` | `MSG_PMKT-E-07528_027` | giao thoa một phần, hoặc N3 trùng phạm vi với bản ghi khác |
| 409 | `CO_CHUNG_TU_CHUA_GHI_SO` | `MSG_PMKT-E-07528_008` | `isTuDong = false` và còn chứng từ chưa ghi sổ |
| 409 | `STALE_DATA` | — | §3 |
| 403 | — | — | thiếu `HTKhoaSo.Edit` (hoặc `.Execute` khi khóa ngay) |
| 500 | — | `MSG_PMKT-E-07528_025` | lỗi hệ thống (`UC_ChinHSuaThietLapKhoaSo.md:40`) |

### 4.2 Bảng field — chỉ phần KHÁC A4

11 field của `LuuThietLapKhoaSoRequest` giữ nguyên ràng buộc, xem [F02 §2.2](02-tao-thiet-lap-khoa-so.md). Ba khác biệt:

| # | Field | Kiểu | Bắt buộc | Ràng buộc | Nguồn |
|---|---|---|---|---|---|
| 1 | `{id}` (path) | `UUID` | **Y** | Bản ghi phải tồn tại và chưa xoá mềm, nếu không → 404 | `SCR_XemDanhSachThietLapKhoaSo.md:52` — icon Bút trên dòng |
| 2 | `ngayCapNhat` | `Instant` | N | Token optimistic-lock. Lệch `ngay_cap_nhat` hiện tại → 409 `STALE_DATA`. **Null ⇒ bỏ qua kiểm** (`AbstractCrudService.java:145-148`) | Không có trong BA — theo khuôn `DeleteRequest.updatedAt` base đang dùng cho DELETE |
| 3 | *(mọi field còn lại)* | — | — | **Y hệt A4** — BA nói *"Cho phép sửa tất cả các trường: Phạm vi, Loại chứng từ, Người dùng, Ngày khóa sổ"* (`UC_ChinHSuaThietLapKhoaSo.md:8`) nên không field nào bị khoá ở chế độ Sửa | — |

**Vì sao PUT toàn phần chứ không PATCH bán phần:** BA mô tả popup Sửa nạp **đầy đủ** dữ liệu hiện tại rồi lưu lại toàn bộ (`UC_ChinHSuaThietLapKhoaSo.md:23`). Nhận PATCH thì phải phân biệt "field không gửi" với "field gửi null" — mà `ngayKhoaSo = null` là trạng thái **hợp lệ** (bản ghi Thiết lập), nên hai thứ đó không phân biệt được bằng JSON thường. Base cũng chỉ cấp `PUT /{id}` (`BaseCrudController.java:149-153`).

---

## 4bis. Ánh xạ cột: BA ↔ DB ↔ DTO

Giống hệt [F02 §2bis](02-tao-thiet-lap-khoa-so.md) — cùng một request, cùng một bảng. Năm cột có giá trị **khác** ở luồng Sửa:

| Cột DB | Ở A4 (tạo) | Ở A5 (sửa) |
|---|---|---|
| `pham_vi_hash` | tính từ request | **tính lại** — phạm vi có thể đổi (E2, §2) |
| `loai_khoa_so` | 1 hoặc 2 theo `isTuDong` | 1 hoặc 2 theo `isTuDong`; bản ghi đang là **3** sửa xong thành **1** (§5, BR03) |
| `nhom_ban_ghi` | cột sinh | cột sinh — **đổi nhóm** khi bật/tắt `isTuDong`, kéo theo việc tách bản ghi (§5) |
| `ngay_tao`, `nguoi_tao` | gán mới | **giữ nguyên** — `BaseEntity.java:24,36` khai `updatable = false` |
| `la_mac_dinh` | luôn `false` | **giữ nguyên** — sửa bản ghi mặc định không làm mất cờ, nó chỉ chi phối quyền xoá |

---

## 4ter. Phân trang · sắp xếp · lọc · dòng tổng

**Không áp dụng** — endpoint ghi một bản ghi. Xem [F01 §5](01-xem-danh-sach-thiet-lap.md).

BR29.4 Common (*"giữ nguyên trang hiện tại sau khi sửa"*) là việc của FE: BE không đổi thứ tự sắp xếp sau khi sửa, nhưng bản ghi vừa sửa **sẽ nhảy lên đầu nhóm** vì sort mặc định có `ngayCapNhat:desc`. Nếu BA coi đó là vi phạm BR29.4 thì phải đổi sort mặc định của F01 — nêu ở **Q12** khi rà soát.

---

## 4quater. Quét chứng từ chưa ghi sổ — chỉ quét PHẦN MỚI BỊ KHOÁ THÊM

> ⚠️ Đây là điểm **khác** F02 và là điểm dễ cài sai nhất của luồng Sửa. Đọc hết trước khi code.

### 4quater.1 Vì sao không dùng nguyên điều kiện của A4

A4 quét mọi chứng từ có `ngay_hach_toan <= ngayKhoaSo` vì lúc tạo mới, **toàn bộ** khoảng đó là phần mới bị khoá. Ở A5 thì không: bản ghi đã có một mốc cũ đang hiệu lực, nên chỉ phần **vượt quá mốc cũ** mới là phần bị khoá thêm.

Dùng nguyên điều kiện của A4 sẽ tạo **bẫy kẹt cứng** không có đường ra:

| Bước | Việc | Kết quả |
|---|---|---|
| 1 | Chứng từ chưa ghi sổ nằm trong kỳ đã khoá | Xảy ra được — **R3**: loại chứng từ chưa có `ChungTuChoXuLyPort` không được đếm lúc khoá, nên lọt vào kỳ khoá hợp lệ. Cũng xảy ra qua job (**Q3**) và qua nhập liệu di trú |
| 2 | Người dùng lùi `ngayKhoaSo` 31/05 → 10/04 để **mở sổ** cho chúng | BR01 `SCR_ThietLapNgayKhoaSo.md:91` nói đây **chính là** cách mở sổ |
| 3 | Luồng Sửa quét, thấy chứng từ chưa ghi sổ có `ngay_hach_toan <= 10/04` | **409 `MSG_..._008`** — không cho lùi |
| 4 | Người dùng quay sang ghi sổ chúng | **BR07 chặn** — mốc cũ 31/05 vẫn hiệu lực (`SCR_XemDanhSachThietLapKhoaSo.md:85-92` liệt kê "Ghi sổ chứng từ") |

⇒ Không mở sổ được, cũng không ghi sổ được. Thoát ra chỉ còn cách sửa thẳng DB.

### 4quater.2 Điều kiện đúng

```
mocCu  = mốc khoá sổ ĐANG hiệu lực cho PHẠM VI MỚI, tính theo BR01 (MAX qua mọi thiết lập
         áp dụng được cho phạm vi đó) — KHÔNG phải ngay_khoa_so của chính bản ghi đang sửa
mocMoi = ngayKhoaSo trong request

quét khi  mocMoi > mocCu
quét gì   chứng từ chưa ghi sổ, trong phạm vi MỚI, có   mocCu < ngay_hach_toan <= mocMoi
```

Ba hệ quả:

| Ca | `mocCu` vs `mocMoi` | Quét? | Vì sao |
|---|---|---|---|
| **Lùi ngày (Mở sổ)** | `mocMoi <= mocCu` | **Không** | Không khoá thêm gì. Quét ở đây tạo đúng cái bẫy §4quater.1 |
| **Tiến ngày** | `mocMoi > mocCu` | **Có**, chỉ khoảng `(mocCu, mocMoi]` | Chứng từ ≤ `mocCu` đã bị khoá từ trước — chặn vì chúng là chặn một việc người dùng không gây ra |
| **Đổi phạm vi, giữ nguyên ngày** | tính lại `mocCu` cho phạm vi MỚI | **Có thể** | Phạm vi mới có thể chưa từng bị khoá ⇒ `mocCu` nhỏ hơn nhiều ⇒ khoảng quét rộng ra. Đây là lý do `mocCu` phải tính theo **phạm vi mới**, không lấy `ngay_khoa_so` cũ của bản ghi |

> ⚠️ **`mocCu` phải tính theo BR01, không đọc từ chính bản ghi đang sửa.** Nếu bản ghi đang sửa có phạm vi "Bán hàng" khoá tới 10/04, mà thiết lập "Toàn hệ thống" đang khoá tới 31/05, thì chứng từ bán hàng ngày 20/05 **đã bị khoá rồi** (BR01 lấy mốc lớn nhất). Đọc `ngay_khoa_so` của bản ghi ⇒ tưởng 20/05 là phần mới ⇒ chặn nhầm. Dùng lại đúng truy vấn của [08 §3.3](08-ap-dung-moc-khoa-so.md), **loại trừ chính bản ghi đang sửa** khỏi phép `MAX`.

### 4quater.3 Áp ngược lại cho A4

Cùng lập luận, [F02](02-tao-thiet-lap-khoa-so.md) cũng phải dùng công thức này: tạo mới một thiết lập "Bán hàng khoá tới 30/06" khi hệ thống đã khoá tới 31/05 thì phần mới bị khoá chỉ là `(31/05, 30/06]`. Chứng từ chưa ghi sổ ngày 20/05 nằm ngoài phần đó và **không được phép** chặn lần lưu này — vì người dùng không thể ghi sổ chúng, và cũng không phải họ làm chúng bị khoá.

Với A4 tạo mới trên phạm vi **chưa từng có thiết lập nào**, `mocCu` = mốc nền do BR01 cấp (thường là bản ghi "Toàn hệ thống"), hoặc `null` nếu chưa có gì — khi đó khoảng quét là toàn bộ `ngay_hach_toan <= mocMoi`, **đúng bằng** điều kiện gốc của BA. Nói cách khác công thức mới **tổng quát hoá** điều kiện BA chứ không mâu thuẫn với nó.

### 4quater.4 Lệch BA — cần xác nhận

BR01 `SCR_PopupCanhBaoChungTu.md:41` viết điều kiện là *"(1) Ngày hạch toán <= ngày khóa sổ"*, không có vế `> mocCu`. Plan **lệch có chủ đích** ở đúng vế đó, vì đọc nguyên văn sẽ tạo bẫy §4quater.1. Đưa vào **Q14** để BA phán quyết — nếu BA khẳng định phải quét toàn bộ thì phải kèm một lối thoát khác cho ca "mở sổ khi còn chứng từ chưa ghi sổ", nếu không hệ thống có trạng thái không tự thoát được.

---

## 5. Sửa bản ghi loại nào thì hợp lệ?

`SCR_XemDanhSachThietLapKhoaSo.md:40` cho icon Sửa hiện trên **mọi** dòng (chỉ Xóa mới bị giới hạn theo `loaiKhoaSo = 2`). Diễn giải theo từng loại:

| `loaiKhoaSo` của bản ghi | Sửa nghĩa là gì | Hợp lệ? |
|---|---|---|
| **1 — Thủ công** | Đổi ngày khóa sổ (kể cả lùi ngày = Mở sổ, BR01) hoặc đổi phạm vi | ✅ |
| **2 — Thiết lập** | Đổi chu kỳ / độ trễ / giờ / phạm vi của lịch tự động | ✅ — kèm tính lại `moc_chay_ke_tiep` ([F07](07-job-tu-dong-khoa-so.md)) |
| **3 — Tự động** | Đây là **kết quả** một lần job chạy. Người dùng sửa nó = ghi đè kết quả bằng một mốc thủ công | ✅ nhưng `loai_khoa_so` **chuyển thành 1** — đúng BR03: *"nếu đang có bản ghi 'Tự động', người dùng tạo khóa sổ thủ công mới đè lên thì loại sẽ đổi thành 'Thủ công'"* |

Trường hợp đặc biệt: **bật `isTuDong` trên một bản ghi đang là kết quả (loại 1 hoặc 3)**. Bản ghi đó chuyển sang `nhom_ban_ghi = 2` (THIẾT LẬP) ⇒ nó **rời khỏi** nhóm kết quả và mốc khóa sổ hiện hành của phạm vi đó **biến mất**. Hệ quả: kỳ đang khóa bị **mở ra** mà người dùng không chủ ý.

| | Phương án A — cho phép, chấp nhận mốc biến mất | **Phương án B (chọn) — tách bản ghi** |
|---|---|---|
| Hành vi | Bản ghi đổi `nhom_ban_ghi`, mốc khóa mất | Giữ nguyên bản ghi kết quả (loại 1/3) với `ngay_khoa_so` cũ; **tạo thêm** một bản ghi THIẾT LẬP (loại 2) cùng phạm vi |
| Đúng BR03? | Không — BR03 nói rõ hai nhóm *"tồn tại độc lập"* | Có |
| Người dùng thấy | Một dòng đổi loại, kỳ tự mở | Hai dòng: kết quả cũ giữ nguyên + lịch mới |
| Rủi ro | **Mở sổ ngoài ý muốn** — hỏng dữ liệu kế toán | Danh sách có thêm dòng. **Chốt an toàn**: nếu phạm vi đó đã có bản ghi THIẾT LẬP thì ghi đè bản ghi đó thay vì tạo mới (nhánh N3 không xảy ra) |

Chọn **B**. Ghi vào **Q12** để BA xác nhận: đây là ca BA không mô tả, và phương án B là cách duy nhất không làm mất mốc khóa đang có hiệu lực.

Chiều ngược lại (tắt `isTuDong` trên bản ghi loại 2): bản ghi chuyển sang `nhom_ban_ghi = 1`, cần `ngayKhoaSo` (V7) và **phải quét chứng từ chưa ghi sổ** như A4 — nó trở thành một lần khóa sổ thật.

---

## 6. Luồng xử lý

```mermaid
flowchart TD
  A[PUT /{id}] --> Q1[quyen: Edit + Execute nếu isTuDong = false]
  Q1 --> L[load id — 404 nếu không có / đã xoá mềm]
  L --> LK[kiemTraLock ngayCapNhat — 409 STALE_DATA]
  LK --> V[V1..V10 — KhoaSoValidator]
  V --> H[Tính hashMoi; khoá advisory hashCũ + hashMoi theo thứ tự tăng dần]
  H --> SW{Đổi nhóm bản ghi?}
  SW -->|bật isTuDong trên bản ghi kết quả| SPLIT[Tách: giữ bản ghi kết quả + upsert bản ghi THIẾT LẬP]
  SW -->|không| N{hashMoi thuộc về ai?}
  N -->|chính nó| U1[Cập nhật]
  N -->|chưa ai| U2[Cập nhật + đổi pham_vi_hash + đồng bộ 2 bảng con]
  N -->|bản ghi khác| E409[409 MSG_027]
  U1 --> SCAN{isTuDong = false?}
  U2 --> SCAN
  SPLIT --> SCAN
  SCAN -->|không| J[Tính lại moc_chay_ke_tiep]
  SCAN -->|có| MOC[Tính mocCu theo BR01 cho PHẠM VI MỚI, trừ chính bản ghi này]
  MOC --> CMP{mocMoi > mocCu?}
  CMP -->|Không — lùi ngày = Mở sổ| SAVE[save + touch nếu chỉ đổi dòng con]
  CMP -->|Có| P["Quét khoảng mocCu < ngay_hach_toan <= mocMoi<br/>409 MSG_008 nếu > 0"]
  P --> SAVE
  J --> SAVE
  SAVE --> OK[200 MSG_020]
```

---

## 7. Kiểm thử

### 7.1 Unit test (`@Tag("unit")`)

| Lớp test | Kiểm gì |
|---|---|
| `SuaThietLapPhamViTest` | Ba nhánh N1/N2/N3 §2 |
| `SuaThietLapDoiNhomTest` | Bật `isTuDong` trên bản ghi loại 1/3 → **tách** thành 2 bản ghi, mốc khóa cũ giữ nguyên (§5) |
| `SuaThietLapDoiNhomTest` | Tắt `isTuDong` trên bản ghi loại 2 → yêu cầu `ngayKhoaSo` (V7) và bật đường quét chứng từ |
| `SuaThietLapLoaiKhoaSoTest` | Sửa bản ghi loại 3 → `loaiKhoaSo` thành 1 (BR03) |
| `TouchKhiChiDoiDongConTest` | Chỉ đổi `maLoaiChungTu` → `phienBan` vẫn tăng (chứng minh `touch()` được gọi) |
| `QuetPhanMoiBiKhoaTest` | Ba ca §4quater.2: lùi ngày → **không** gọi `dem()` lần nào · tiến ngày → gọi với đúng khoảng `(mocCu, mocMoi]` · đổi phạm vi → `mocCu` tính lại theo **phạm vi mới** |
| `QuetPhanMoiBiKhoaTest` | `mocCu` tính theo BR01 và **loại trừ chính bản ghi đang sửa**: bản ghi "Bán hàng 10/04" + thiết lập "Toàn hệ thống 31/05" → sửa Bán hàng lên 30/06 thì `mocCu = 31/05`, **không phải** 10/04 |

### 7.2 Test tích hợp (cần Docker)

`SuaThietLapKhoaSoIT`:
- Hai request sửa cùng bản ghi với `ngayCapNhat` cũ → một thành công, một 409 `STALE_DATA`.
- Hai request sửa **chéo** phạm vi của nhau (A→hash2, B→hash1) → không deadlock (nhờ khoá theo thứ tự tăng dần).
- Sửa phạm vi từ 5 loại CT xuống 2 → còn đúng 2 dòng con, 3 dòng cũ bị `orphanRemoval`, không dòng mồ côi trong DB.
- **`MoSoKhiConChungTuChuaGhiSoIT`** — tái hiện đúng 4 bước của bẫy R10, khẳng định bước 2 đi qua được:
  1. Khoá "Toàn hệ thống" tới 31/05 (bỏ qua kiểm để mô phỏng đường R3: chứng từ của loại chưa có port).
  2. Tạo một chứng từ **chưa ghi sổ** ngày 20/05 trực tiếp qua repository.
  3. Sửa thiết lập lùi mốc về 10/04 → **phải 200**, không phải 409.
  4. Sau đó ghi sổ chứng từ 20/05 → **phải thành công** (kỳ đã mở).

  Đây là test chống hồi quy cho R10. Nếu ai đó "sửa cho đúng BA" bằng cách bỏ cận dưới `mocCu`, test này đỏ ngay.

---

## 8. BR đã áp dụng

| BR | Áp thế nào |
|---|---|
| BR03 danh sách (ghi đè) | §2 N1/N2, §5 (loại 3 → loại 1) |
| BR01 popup (không ràng buộc tương lai/quá khứ) | Cho phép lùi `ngayKhoaSo` |
| Toàn bộ BR02–BR07 của popup | Kế thừa nguyên từ [F02](02-tao-thiet-lap-khoa-so.md) |
| BR14.1 Common (chế độ form) | A3 nạp dữ liệu vào popup ở chế độ Sửa; BR34 (sửa từ màn Xem) dùng cùng cặp A3 → A5 |
| BR15 Common (validation) | V1…V10 |
| BR25 Common (phân quyền) | `Edit` + `Execute` |
| BR29.4 Common (giữ nguyên trang sau khi sửa) | FE — BE không đổi thứ tự sắp xếp sau khi sửa |
| BR46 Common (trường hệ thống) | `nguoi_cap_nhat`/`ngay_cap_nhat` do `BaseEntity.onUpdate()` tự đóng dấu |
