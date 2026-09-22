# PMKT-E-14549_21 — Biên bản quyết định & bàn giao

| | |
|---|---|
| Ngày | 2026-09-19 |
| Người quyết | **Dat** (user) — uỷ quyền cho AI tự chốt phần còn lại theo đề xuất |
| Căn cứ | chat 2026-09-19: *"tất cả lưu json, không tạo bảng để lưu, không làm theo thiết kế DB dạng bảng của BA"* · *"Làm tất cả các tính năng"* · *"Làm hết các yêu cầu, tự làm theo đề xuất rồi note lại nội dung vào file .md khi bàn giao"* |
| Phạm vi | đóng **32 mục `OPEN`** của [01-conflict.md](01-conflict.md) để mở cổng đặc tả |

> ⚠ **Đọc trước khi dùng.** File này ghi các quyết định **không có trong tài liệu BA**. Mọi mục
> dưới đây đều là chỗ tài liệu im lặng hoặc tự mâu thuẫn. **BA vẫn cần soát lại** — chỗ nào BA chốt
> khác thì sửa ở đây trước, rồi mới sửa code.
>
> Ký hiệu: **`[BA-THEO-TL]`** = chọn theo một bên có sẵn trong tài liệu · **`[AI-ĐỀ-XUẤT]`** = tài
> liệu không nói, AI đề xuất theo uỷ quyền của user · **`[USER]`** = user quyết trực tiếp.

---

## §1. Ba quyết định gốc (chi phối mọi quyết định còn lại)

### Q-01 · Mô hình lưu trữ = JSON, không dựng bảng quan hệ **`[USER]`**

Bỏ mô hình 5 bảng `cfg_mau_in_chung_tu` / `_khoi` / `_khoi_cot` / `_khoi_o` / `_khoi_chu_ky` mà
`3.crud-matrix.md` mô tả. Giữ **một bản ghi một cột `jsonb`** trên bảng đã có
`prn_mau_in_tuy_chinh`.

**Hệ quả bắt buộc ghi nhận:**
- `3.crud-matrix.md` từ nay đọc là **mô hình logic**, không phải bảng vật lý. 5 "entity" trở thành 5
  **nhánh trong JSON schema**.
- `/verify-spec` sẽ chấm trượt phần entity nếu chấm theo đúng chữ tài liệu → đã ghi ngoại lệ ở đây.
- Khoá nghiệp vụ phải đổi: bảng hiện có khoá `(tenant_id, ma_loai_chung_tu)`, tài liệu yêu cầu khoá
  theo **cặp (loại chứng từ, nghiệp vụ)** → **phải thêm cột `ma_nghiep_vu`** và đổi unique index.
  Đây là **migration mới**, không sửa `V1148` (đã lên `origin/develop` + `origin/staging`).
- BR46 (trường hệ thống bắt buộc) vẫn áp cho **bản ghi**, không áp cho từng nhánh JSON.

### Q-02 · Epic chạy theo bộ BR **Phase 2** cho riêng chức năng này **`[USER]`**

BR50.7 · BR51.5 · BR51.6 **không có** trong bản Phase 1 (BR1…BR49) mà `br.sh` đọc. User quyết làm
tất cả tính năng ⇒ chức năng này **áp bộ BR Phase 2**.

23 luật + 3 bất biến đứng trên nền này (danh sách ở
[00-source-map.md §4.3](00-source-map.md)). Nếu sau này dự án quyết chức năng này thuộc Phase 1 thì
**phải soát lại toàn bộ 26 mục đó**.

### Q-03 · Làm thêm tầng "thiết lập chung tối thiểu" **`[USER]` + `[AI-ĐỀ-XUẤT]`**

Epic `_21` kế thừa động từ epic `_20` (chưa tồn tại trong repo). Làm **đúng phần `_21` cần**, không
làm cả epic `_20`:

| Làm | Không làm (thuộc `_20`, ngoài phạm vi) |
|---|---|
| Giấy và chữ mặc định: khổ · hướng · số cột tự động in ngang · 4 lề · font · cỡ chữ | Màn *Danh sách báo cáo* |
| 7 dòng thông tin đơn vị đầu trang (gồm Logo) + căn lề + lặp trang sau | Màn *Tùy chỉnh báo cáo* |
| 3 quy tắc in chứng từ: cho in chưa ghi sổ · cho in đã khoá sổ · cộng gộp mặt hàng | Báo cáo yêu thích |
| **Logo đơn vị** (repo chưa có trường) | Mở rộng/thu gọn nhóm báo cáo |

Lưu cùng kiểu: **JSON**, trên cấu hình tenant hiện có — **không** dựng `cfg_tenant` / `cfg_chi_nhanh`
mới. `cfg_chi_nhanh` chưa tồn tại ⇒ tạm đọc hồ sơ đơn vị từ **Thông tin công ty (tenant)** đang có,
và **để sẵn điểm nối** để khi có chi nhánh thì đổi nguồn mà không sửa tầng trên (xem Q-14).

---

## §2. Đóng các mục P0

| Mục | Quyết định | Loại |
|---|---|---|
| **C01** — khoá cộng gộp dòng | **CÓ tính thuế suất.** Khoá gộp = *mã hàng + đơn vị tính + đơn giá + thuế suất* (+ *số lô, hạn sử dụng* nếu vật tư theo dõi theo lô). Lấy theo `SCR_CauHinhBaoCaoChungTu.md:160-162` vì nguồn này chi tiết hơn và có ví dụ phủ định rõ ("khác thuế suất thì **không gộp**"). BR51.5 chỉ liệt kê thiếu, không phủ định. | `[BA-THEO-TL]` |
| **C30** — phạm vi cộng gộp | **Giữ giới hạn của BR51.5**: chỉ áp cho **Hoá đơn, phiếu xuất kho, phiếu nhập kho**. `SCR:281` không nhắc lại không có nghĩa là mở rộng ra mọi chứng từ. | `[BA-THEO-TL]` |
| **C02** — điều kiện xoá bản ghi khi Lưu | **So sánh nội dung.** Khi Lưu, chuẩn hoá JSON mẫu rồi so với JSON mẫu chuẩn hệ thống; **bằng ⇒ xoá bản ghi** (không tạo nếu chưa có). Chọn phương án này vì: (a) `SCR:318` và `AD01:30` đều phát biểu theo nội dung; (b) với mô hình JSON (Q-01) so sánh sâu là một phép so chuỗi đã chuẩn hoá, rẻ; (c) cho bất biến sạch — *mẫu bằng chuẩn ⇔ không tồn tại bản ghi*, không sinh bản ghi rác khi người dùng mở rồi Lưu mà không sửa gì. **Chuẩn hoá** = sắp khoá theo thứ tự cố định, bỏ mọi khoá có giá trị `null`, bỏ id kỹ thuật. | `[BA-THEO-TL]` |
| **C08** — ảnh nền lưu ở đâu | **Cột `bytea` trên chính bảng đã có**, không nhét base64 vào JSON. Thêm `anh_nen` (`bytea`) + `anh_nen_kieu_tep` (`text`) + `anh_nen_ten_tep` (`text`) vào `prn_mau_in_tuy_chinh`; JSON chỉ giữ cờ `nen.kieu='ANH'`. Lý do lệch nguyên tắc "tất cả lưu JSON": ảnh 1 MB thành ~1,37 MB base64 và sẽ bị đọc lại **mỗi lần** nạp mẫu, kể cả khi chỉ cần bố cục. Đây là dữ liệu nhị phân, không phải cấu hình. **Không tạo bảng mới** — đúng tinh thần quyết định của user. Ảnh tải lên bằng `multipart`, endpoint riêng. | `[AI-ĐỀ-XUẤT]` |
| **C09** — không có ERD 5 bảng | **Không còn áp dụng** sau Q-01. Thay bằng **JSON schema** là hợp đồng kỹ thuật duy nhất, viết ở `docs/doing/<slug>-api/` khi `/plan-be`. Schema phải phủ đủ 5 nhánh logic + **cấu trúc lưới khối tự do** (số dòng, số cột, `rowSpan`/`colSpan`, loại ô, nội dung ô, căn ô) — thứ mà tài liệu không có chỗ lưu. | `[AI-ĐỀ-XUẤT]` |
| **C10** — cột/lưới/trường **bị xoá** khỏi form | **Bỏ qua im lặng khi in, báo nhẹ khi mở màn thiết lập.** Dựng bản in: phần tử không còn trong đặc tả form thì **không in**, không báo lỗi, không làm hỏng bản in. Mở màn Thiết lập mẫu in: các phần tử đó hiện **mờ + nhãn "không còn trên form"** và bị loại khỏi mẫu khi Lưu. Nguyên tắc: **bản in không bao giờ được vỡ vì cấu hình cũ**. | `[AI-ĐỀ-XUẤT]` |
| **C11** — nền BR Phase 2 | Xem **Q-02**. | `[USER]` |
| **C12** — epic `_20` + `cfg_chi_nhanh` chưa có | Xem **Q-03** và **Q-14**. | `[USER]` |
| **C13** — mã quyền | **Hai tầng**: (a) mở màn / lưu mẫu cần `HTMauIn.View` / `HTMauIn.Edit` — đã seed ở `V1149`, đang trên develop, không phải seed thêm; (b) **cộng thêm** quyền xem chi tiết của chính nghiệp vụ đang mở (`<ChucNang>.View.Detail`) để không lộ dữ liệu chứng từ qua màn xem trước. Không tự seed `<ChucNang>.PrintConfig` vì thêm mã vào ma trận phân quyền là quyết định BA. **Đổi sang mã theo nghiệp vụ sau này chỉ phải đổi một hằng số.** | `[AI-ĐỀ-XUẤT]` |
| **C37** — mô hình dữ liệu | Xem **Q-01**. | `[USER]` |

---

## §3. Đóng các mục P1

| Mục | Quyết định | Loại |
|---|---|---|
| **C03** — Logo có nằm trong 7 ô tick mẫu sửa riêng được | **CÓ.** Đủ 7 ô: Tên đơn vị · Địa chỉ · Mã số thuế · Số điện thoại · Email · Tài khoản ngân hàng · **Logo**. Ba nguồn đồng thuận (`SCR:125`, ma trận `MT:77`, Figma frame 4); BR51.5 chỉ nói "dòng thông tin" nên không phủ định Logo. | `[BA-THEO-TL]` |
| **C04** — *Tiêu đề in ra* của ô ký | **Mẫu sửa riêng được.** `SCR:295` + ma trận `MT:89` + Figma frame 6 (ô nhập được) thắng `SCR:257`. Tên người ký và cờ *In tên người ký* thì **luôn** theo thiết lập chung. | `[BA-THEO-TL]` |
| **C05** — Chữ ký đọc hồ sơ đơn vị của chi nhánh nào | **Chi nhánh ghi trên chứng từ**, giống khối đầu trang (BR50.7). Không dùng chi nhánh đang làm việc — in lại một chứng từ cũ ở chi nhánh khác phải ra **cùng một bản in**. | `[AI-ĐỀ-XUẤT]` |
| **C06** — hai người cùng Lưu | **Khoá lạc quan.** Payload mang `phienBan` (đã có sẵn ở `LuuMauInRequest` bản cũ); lệch phiên bản ⇒ **không ghi**, trả lỗi, màn hỏi nạp lại. Chưa có mã `MSG_` của BA ⇒ dùng **`MSG_COMMON_001`** (thao tác không hợp lệ với trạng thái hiện tại) + key i18n riêng cho câu hướng dẫn. **Đề nghị BA cấp mã riêng.** | `[AI-ĐỀ-XUẤT]` |
| **C07** — sửa tên khối tự do ở đâu | **Cả hai chỗ.** Hộp *Đặt tên khối* khi thêm mới (`SCR:284`) **và** ô *Tên khối* trên bảng chỉnh (Figma frame 3 vẽ rõ, `SCR:345` ngụ ý qua "khi rời ô"). Hai chỗ cùng ghi một trường. | `[BA-THEO-TL]` |
| **C11.b / C14** — 2 tooltip nút In bị disable | Giữ **nguyên văn** của `SCR_CauHinhBaoCaoChungTu.md:155-156`, đặt key i18n cục bộ. `msg.sh` sẽ báo `THIEU` cho tới khi BA cấp mã — **chấp nhận, đã ghi ở đây**. | `[AI-ĐỀ-XUẤT]` |
| **C15** — thiếu quyền **In** | Dùng **`MSG_COMMON_003`** ("Bạn không có quyền thực hiện chức năng {tên chức năng}…") theo BR25.2. **Không** mở rộng `MSG_PMKT-E-14549_21_002` như `AD02:27` làm — `6.messages.md` khai mã đó riêng cho quyền *Thiết lập mẫu in*. | `[BA-THEO-TL]` |
| **C16** — không phân biệt / không hoàn lại được từng ô | **Giữ đúng tài liệu và Figma**: nút *Theo thiết lập chung* ở **mức nhóm**, không có nhãn từng ô. Không tự thêm UI ngoài đặc tả. **Ghi nhận là rủi ro UX, đề nghị BA xem lại.** | `[BA-THEO-TL]` |
| **C17** — đổi Khổ/Hướng trên thanh Xem trước = đổi mẫu | **Giữ đúng tài liệu.** `SCR:79` nói thẳng *"đổi ở đây là đổi mẫu, không phải chỉ đổi cách xem"*. Hai ô ở thanh Xem trước và ở panel *Thiết lập mẫu* là **một trường**, đồng bộ hai chiều tức thời. **Ghi nhận là rủi ro UX, đề nghị BA xem lại.** | `[BA-THEO-TL]` |
| **C18** — ẩn khối Tiêu đề rồi còn bắt buộc `MSG_201`? | **Khối đang ẩn thì bỏ qua validate của khối đó.** Theo tinh thần BR30 ("ẩn trường không đổi rule nghiệp vụ") nhưng ở đây khối ẩn ⇒ **không in ra** ⇒ nội dung rỗng không gây hậu quả. Bật lại khối thì validate lại ngay. | `[AI-ĐỀ-XUẤT]` |
| **C19** — Tách ô đang có nội dung | Nội dung về **ô trên-trái** của vùng vừa tách; các ô còn lại thành ô trống. Đối xứng với luật Gộp (giữ nội dung ô đầu tiên theo trái→phải, trên→dưới). **Không hỏi xác nhận** — không mất dữ liệu. | `[AI-ĐỀ-XUẤT]` |
| **C20** — sàn lưới khối tự do | **Tối thiểu 1 dòng × 1 cột.** Xoá dòng cuối cùng / cột cuối cùng bị chặn (nút mờ). Muốn bỏ hẳn thì dùng *Xoá khối này* (`MSG_403`). | `[AI-ĐỀ-XUẤT]` |
| **C21** — thứ tự "lỗi đầu tiên" | Theo **thứ tự khối trong Bố cục mẫu**; trong một khối: **ô ở bảng chỉnh trước** (theo thứ tự từ trên xuống), **rồi ô lưới trên trang xem trước** (trái→phải, trên→dưới). | `[AI-ĐỀ-XUẤT]` |
| **C22** — `MSG_103` hiện "một lần" | **Một lần mỗi lần mở màn xem trước bản in.** Không nhớ qua phiên, không nhớ theo người dùng. | `[AI-ĐỀ-XUẤT]` |
| **C23** — *Lưu và đóng* có hiện `MSG_101` không | **Có** — hiện toast `MSG_101` ("Lưu mẫu in thành công!") rồi mới đóng màn. Toast sống độc lập với màn (BR26.1, góc phải trên). | `[AI-ĐỀ-XUẤT]` |
| **C24** — quyền theo chi nhánh nhưng mẫu áp mọi chi nhánh | **Không thêm cảnh báo.** Tài liệu không yêu cầu; thêm hộp thoại ngoài đặc tả là tự đặt luật. Ghi nhận để BA cân nhắc. | `[BA-THEO-TL]` |
| **C38** — chồng lấn với hệ `bieuMau` | **Hai chức năng độc lập, không gộp.** `bieuMau` là biểu mẫu động do người dùng tự dựng từ đầu; mẫu in chứng từ gắn cứng với đặc tả form của một nghiệp vụ và có mẫu chuẩn hệ thống. Chỉ **dùng lại kỹ thuật** (`useDesignerStore`, `keoTha`, `PropField`) chứ không dùng chung dữ liệu. | `[AI-ĐỀ-XUẤT]` |

---

## §4. Đóng các mục P2

| Mục | Quyết định |
|---|---|
| **C26** — `cfg_mau_in_chung_tu` thuộc nhóm nào của BR50.6 | Xếp **nhóm 1 (cấu hình hệ thống)** — không khai `ChiNhanhId`, dùng chung mọi chi nhánh. Đề nghị BA bổ sung dòng này vào bảng BR50.6. |
| **C28** — `Bắt buộc = Y` vs lưu `NULL` | `Y` đọc là **"bắt buộc có giá trị hiệu dụng"**, không phải "cột NOT NULL". `NULL` trong mẫu là **cờ *theo thiết lập chung***, không phải "chưa nhập". Với JSON: khoá **vắng mặt** = theo chung. |
| **C29** — vị trí logo khi căn lề ≠ Trái | Logo luôn nằm **bên trái khối thông tin đơn vị, cùng hàng với dòng đầu tiên**; căn lề áp cho **cả cụm** (logo + các dòng chữ) chứ không tách riêng. |
| **C31** — *Chia đều về 100%* khi đang lọc cột | Áp cho **mọi cột đang tick in**, không phụ thuộc ô *Tìm cột*. Ô tìm chỉ lọc hiển thị. |
| **C32** — độ sâu Hoàn tác | **60 bước** trong một phiên mở màn (số đã có ở nửa sau `SCR`). Đóng màn thì xoá lịch sử. |

---

## §5. Những thứ CỐ Ý lệch tài liệu — danh sách để BA soát

| # | Lệch gì | Vì sao | Ai quyết |
|---|---|---|---|
| L-1 | Không dựng 5 bảng quan hệ, lưu JSON | quyết định kỹ thuật của user | `[USER]` |
| L-2 | Thêm cột `bytea` cho ảnh nền thay vì nhét base64 vào JSON | tránh đọc 1,4 MB mỗi lần nạp mẫu | `[AI-ĐỀ-XUẤT]` |
| L-3 | Gate quyền bằng `HTMauIn.*` + `<ChucNang>.View.Detail` thay vì quyền *Thiết lập mẫu in* theo nghiệp vụ | epic nghiệp vụ chưa khai mã quyền nào | `[AI-ĐỀ-XUẤT]` |
| L-4 | Dùng `MSG_COMMON_001` cho xung đột phiên bản, `MSG_COMMON_003` cho thiếu quyền In | BA chưa cấp mã | `[AI-ĐỀ-XUẤT]` |
| L-5 | 2 tooltip nút In disable chỉ có key i18n, không có mã `MSG_` | BA chưa cấp mã — `msg.sh` sẽ báo `THIEU` | `[AI-ĐỀ-XUẤT]` |
| L-6 | Làm thêm tầng "thiết lập chung tối thiểu" vốn thuộc epic `_20` | `_21` không chạy được nếu thiếu | `[USER]` |
| L-7 | Hồ sơ đơn vị tạm đọc từ Thông tin công ty (tenant) vì `cfg_chi_nhanh` chưa tồn tại | xem Q-14 | `[AI-ĐỀ-XUẤT]` |
| L-8 | Áp bộ BR **Phase 2** cho riêng chức năng này | xem Q-02 | `[USER]` |

## §6. Điểm nối để sau này không phải viết lại

**Q-14 · Hồ sơ đơn vị theo chi nhánh.** Mọi chỗ cần hồ sơ đơn vị (khối đầu trang, khối chữ ký) phải
đi qua **một cổng duy nhất** nhận vào `chiNhanhId` của chứng từ:

```
HoSoDonViPort.theoChiNhanh(chiNhanhId) -> HoSoDonVi
```

Bản hiện tại bỏ qua tham số và trả hồ sơ của tenant. Khi `cfg_chi_nhanh` ra đời thì **chỉ đổi phần
hiện thực của cổng**, không đụng khối đầu trang, khối chữ ký hay tầng dựng bản in.

**Q-15 · Mã quyền.** Đặt thành hằng số ở một chỗ (`MaQuyenMauIn`), không rải chuỗi trong code — đổi
sang mã theo nghiệp vụ chỉ sửa một file.

**Q-16 · Khoá nghiệp vụ.** Mọi API nhận **cặp** `(maLoaiChungTu, maNghiepVu)`, kể cả khi hiện tại một
loại chứng từ chỉ có một nghiệp vụ. Không rút gọn còn một tham số.

---

## §7. Việc còn nợ BA (không chặn code, nhưng phải trả lời trước khi nghiệm thu)

1. Cấp mã `MSG_` cho: xung đột phiên bản khi Lưu · thiếu quyền In · 2 tooltip nút In disable.
2. Xác nhận **C16** và **C17** (hai rủi ro UX) là chủ ý hay sót đặc tả.
3. Bổ sung `cfg_mau_in_chung_tu` vào bảng phạm vi dữ liệu BR50.6.
4. Sửa lỗi hình thức trong `SCR_ThietLapMauIn_MaTranAnHien.md`: marker `\1` hỏng ở dòng 108; dòng 3
   nhắc ký hiệu `Y*` mà thân ma trận không có ô nào mang `Y*`.
5. Link chéo hỏng trong `SCR_ThietLapMauIn.md:377` → `../../Z.ThietLapMauIn/khao-sat-misa-sua-mau-in.md`
   không tồn tại trên nhánh `main`.
6. Khai **danh sách nghiệp vụ** có mẫu tuỳ chỉnh ở đợt đầu và **mã quyền** của từng nghiệp vụ.

---

## §8. Bổ sung 2026-09-19 — ba điểm Figma lệch tài liệu chữ (phát hiện lúc `/plan-fe`)

Ba điểm này do agent lập kế hoạch FE tìm ra khi đọc 8 frame Figma, không có trong sổ mâu thuẫn ban
đầu vì chỉ lộ ra khi đối chiếu ảnh với luật.

### X5 · Figma vẽ `Thông tin chứng từ` và `Tổng hợp` có nút `✕` **`[BA-THEO-TL]`**

| Bên | Nội dung | Nguồn |
|---|---|---|
| A | Mẫu chuẩn hệ thống gồm **đúng bốn loại khối**: Thông tin đầu trang · Tiêu đề · các Bảng · Chữ ký | `1.function-breakdown.md` (bậc 5) · `R-TLMI-008` |
| B | Figma frame 1–6 vẽ thêm hai dòng khối `Thông tin chứng từ` và `Tổng hợp` **có nút `✕`** — tức là khối xoá được, tức là khối tự do | Figma `71956:288872` |

**Chốt: theo A.** Mẫu chuẩn hệ thống = **đúng 4 loại khối**, không có ngoại lệ.

Căn cứ mạnh nhất nằm ngay trong chính Figma: khối chú thích ở chân cột trái viết nguyên văn
*"Mẫu chuẩn gồm 4 loại: **Thông tin đầu trang**, **Tiêu đề**, các **bảng dữ liệu** và **Chữ ký**.
Phần còn lại có thể tự thêm bằng các **Khối tự do**."* — Figma **tự nói** nó chỉ có 4 loại. Kết luận:
**8 frame Figma vẽ một mẫu ĐÃ TUỲ CHỈNH**, không phải mẫu chuẩn. Ba dấu hiệu cùng hướng: có khối tự do
tên `Ghi chú giao hàng`, badge trạng thái là `Đã lưu` / `Chưa lưu` / `Có lỗi` (mẫu chuẩn chưa lưu bao
giờ), và `Bảng thuế` đang bị tắt mắt (xem X6).

⚠ **Hệ quả nghiệp vụ phải báo BA.** Mẫu chuẩn của một nghiệp vụ mới vì thế **không in** Khách hàng,
Địa chỉ, Diễn giải, Tổng tiền hàng, Tiền thuế, Tổng thanh toán, Số tiền bằng chữ — người dùng phải
tự thêm khối tự do thì mới có. Bản in mặc định sẽ khá trống. Đây là hệ quả **trực tiếp** của
`1.function-breakdown.md`, không phải suy diễn. **Đề nghị BA xác nhận đây là chủ ý**; nếu không thì
BA phải khai *mẫu chuẩn có sẵn N khối tự do dựng sẵn* — đó là dữ liệu khởi tạo, phải BA viết ra, dev
không được tự chế.

### X6 · Figma vẽ `Bảng thuế` bị tắt mắt sẵn **`[BA-THEO-TL]`**

**Chốt: theo `R-TLMI-009`** — mẫu chuẩn bật **mọi** lưới có trên form. Figma vẽ `Bảng thuế` mắt gạch
chéo là vì đó là mẫu đã tuỳ chỉnh (cùng lời giải với X5), không phải mặc định.

### X2 · Frame 0 in `Số: SO000123 · Ngày 27 tháng 08 năm 2026` dưới tiêu đề **`[BA-THEO-TL]`**

**Chốt: theo `R-TLMI-091`** — dòng dưới tiêu đề **chỉ có ngày chứng từ**, số chứng từ **không thuộc**
khối Tiêu đề. Bốn frame 1–5 cũng chỉ vẽ dòng ngày; chỉ frame 0 (xem trước bản in) có thêm số. Muốn
in số chứng từ thì đưa trường `Số chứng từ` vào một **khối tự do** — đúng như frame 3 vẽ trong kho
trường (`Số chứng từ → Tên hiển thị "Số"`).

### Tám điểm còn lại — tự giải được, không cần BA

| # | Lệch gì | Xử lý |
|---|---|---|
| X1 | Ghi chú khảo sát chép nhầm "9 ô màu" | Đếm lại Figma ra **10** ô — khớp `R-TLMI-066`, lấy 10 |
| X7 | `Gộp ô` / `Tách ô` luôn hiện và **mờ**, không ẩn | Lấy theo `R-TLMI-162` (Disable), không theo `R-TLMI-174` (viết lẫn Show/Disable) |
| X8 | Figma có nhãn ngữ cảnh `{Tên khối} · ô dòng {r}, cột {c}` mà luật không nhắc | Lấy theo Figma — UI thắng ở chỗ tài liệu chữ im lặng về trình bày |
| X14 | `Hiện lưới căn chỉnh` mặc định Có theo luật, frame 1/1b vẽ chưa tick | Lấy theo luật |
| X3 | Ngày 25 vs 27 tháng 08 trên cùng một chứng từ giữa các frame | Lỗi hình thức Figma — báo Design |
| X4 | `Tiêu hiển thị` thiếu chữ "u" (đúng: `Tiêu đề hiển thị`) | Lỗi hình thức Figma — báo Design |

## §9. Bổ sung — sự cố bảo mật đã xử lý 2026-09-19

`cell-app/src/main/resources/application.yml` trong phần **chưa commit** có
`${PMKT_INTERNAL_TOKEN:<token thật 64 ký tự hex>}` làm giá trị mặc định ở **2 chỗ**
(`targets.control-plane` và `targets.super-admin`) — vi phạm **luật 7** (không commit secret).

Đã kiểm chứng: `git show HEAD:…/application.yml` cho thấy bản **đã commit** là
`${PMKT_INTERNAL_TOKEN:}` (rỗng, fail-fast), và `git log -S "<token>" --all` **không ra commit nào**
⇒ **token chưa bao giờ lên git, không cần thu hồi**.

Đã sửa: cả hai chỗ về `${PMKT_INTERNAL_TOKEN:}`. Quét lại toàn bộ 29 file chưa commit của `cell-app`:
không còn chuỗi nào khớp mẫu secret.

**Việc cho người vận hành:** xác nhận với người từng đặt giá trị đó vào máy xem token này còn hiệu
lực ở môi trường nào không.
