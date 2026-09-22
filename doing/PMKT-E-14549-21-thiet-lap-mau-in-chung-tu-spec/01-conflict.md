# PMKT-E-14549_21 Thiết lập mẫu in chứng từ — Sổ mâu thuẫn tài liệu

| | |
|---|---|
| Phiếu yêu cầu | `pmkt-docs/ba/Phase_2/PMKT-E-14549_21_ThietLapMauInChungTu/` ⚠ **vùng đóng băng** |
| Commit tài liệu | `c78e322a1` (2026-09-18, "update") · repo `pmkt-docs` main `8d387213e` |
| Figma | `ymMyg329ejsgCWg28CNmGl` node `71956:288871` — 8 frame, đọc 2026-09-19 |
| Ngày soát | 2026-09-19 |
| Mã viết tắt | `TLMI` → `R-TLMI-nnn` · `INV-TLMI-nnn` · message giữ nguyên `MSG_PMKT-E-14549_21_nnn` |
| Trạng thái | **ĐÃ CHỐT** — 36 mục · **0 OPEN** · 32 `CLOSED-BA` (Dat · 2026-09-19, uỷ quyền) · 4 `CLOSED-AUTO` |

> ⚠ **Đọc vùng đóng băng theo yêu cầu trực tiếp của user.** Tài liệu PYC này nằm trong
> `pmkt-docs/ba/Phase_2/**` — CLAUDE.md §Vùng đóng băng cấm đọc, repo đang làm Phase 1. User (Dat)
> yêu cầu trực tiếp ngày 2026-09-19 và chọn cách "chỉ kéo đúng một thư mục ra thư mục tạm". Bản đã
> đọc là bản sao tải từ GitHub, **không** khôi phục `Phase_2/` vào cây `pmkt-docs`.

---

## Bảng tổng

### P0 — chặn code

| ID | Chủ đề | Sev | Trạng thái | Luật bị chặn | Chốt |
|---|---|---|---|---|---|
| **C01** | Khóa cộng gộp dòng khi in — có tính *thuế suất* hay không | P0 | `CLOSED-BA` | `R-TLMI-119` · `R-TLMI-266` | Dat · 2026-09-19 |
| **C02** | Điều kiện xóa bản ghi khi Lưu: *so sánh nội dung bằng mẫu chuẩn* hay *đến từ hành động Đặt lại* | P0 | `CLOSED-BA` | `R-TLMI-021` (nhóm A `001`–`022`) | Dat · 2026-09-19 |
| **C08** | Ảnh nền ≤1MB lưu ở đâu — không bảng/cột nào trong 5 entity chứa được ảnh | P0 | `CLOSED-BA` | `R-TLMI-064`…`075` | Dat · 2026-09-19 |
| **C09** | Cấu trúc cột thật của 5 bảng `cfg_mau_in_*` — package **không có file entity/ERD** | P0 | `CLOSED-BA` | toàn bộ thiết kế DB — chặn `/plan-be` | Dat · 2026-09-19 |
| **C10** | Cột / lưới **bị xóa** khỏi form ở phiên bản sau thì mẫu đã lưu xử lý sao | P0 | `CLOSED-BA` | `R-TLMI-092`…`119` · `R-TLMI-120`…`181` | Dat · 2026-09-19 |
| **C11** | **Nền luật là BR50 / BR51 của bộ Phase 2** — bản Phase 1 mà repo đang dùng chỉ có BR1…BR49 | P0 | `CLOSED-BA` | 23 luật nền BR Phase 2 (xem C11) + `INV-TLMI-001` · `005` · `011` | Dat · 2026-09-19 |
| **C12** | **Epic nền `PMKT-E-14549_20` và bảng `cfg_chi_nhanh` chưa tồn tại trong repo** — không có nguồn để kế thừa | P0 | `CLOSED-BA` | 23 luật nền BR Phase 2 (xem C11) + `INV-TLMI-001` · `005` · `011` | Dat · 2026-09-19 |
| **C37** | **Mô hình dữ liệu**: repo đã có `prn_mau_in_tuy_chinh` (jsonb, V1148–V1150 **đã lên develop/staging**) vs tài liệu yêu cầu **5 bảng quan hệ** | P0 | `CLOSED-BA` | toàn bộ BE | Dat · 2026-09-19 |
| **C13** | **Mã quyền** của từng nghiệp vụ chưa nơi nào khai (epic giao cho epic nghiệp vụ) | P0 | `CLOSED-BA` | `R-TLMI-023`…`035` | Dat · 2026-09-19 |

### P1

| ID | Chủ đề | Sev | Trạng thái | Luật bị chặn | Chốt |
|---|---|---|---|---|---|
| **C03** | Logo có thuộc nhóm "dòng thông tin đơn vị mẫu sửa riêng được" không | P1 | `CLOSED-BA` | `R-TLMI-082` | Dat · 2026-09-19 |
| **C04** | Người ký: *Tiêu đề in ra* mẫu sửa riêng được hay luôn theo thiết lập chung (SCR tự mâu thuẫn **trong cùng một file**) | P1 | `CLOSED-BA` | `R-TLMI-046` · `R-TLMI-188` | Dat · 2026-09-19 |
| **C05** | Khối Chữ ký đọc hồ sơ đơn vị của **chi nhánh nào** | P1 | `CLOSED-BA` | `R-TLMI-199` | Dat · 2026-09-19 |
| **C06** | Hai người cùng sửa một mẫu — không có quy định chống ghi đè | P1 | `CLOSED-BA` | `R-TLMI-258` | Dat · 2026-09-19 |
| **C07** | Sửa **tên khối tự do** ở đâu: hộp Đặt tên lúc thêm, hay ô Tên khối ở bảng chỉnh | P1 | `CLOSED-BA` | `R-TLMI-127` | Dat · 2026-09-19 |
| **C14** | Thiếu mã message cho **2 tooltip** nút In bị disable | P1 | `CLOSED-BA` | `R-TLMI-259`…`271` | Dat · 2026-09-19 |
| **C15** | Thiếu message cho nhánh **thiếu quyền In** (AD tự mở rộng `MSG_002` ngoài phạm vi `6.messages.md`) | P1 | `CLOSED-BA` | `R-TLMI-023`…`035` · `R-TLMI-259`…`271` | Dat · 2026-09-19 |
| **C16** | Không có nhãn phân biệt ô *theo chung* / *riêng*, và **không có cách đưa riêng từng ô về theo chung** | P1 | `CLOSED-BA` | `R-TLMI-036`…`052` | Dat · 2026-09-19 |
| **C17** | Đổi Khổ/Hướng giấy **trên thanh Xem trước** biến ô thành *riêng* vĩnh viễn | P1 | `CLOSED-BA` | `R-TLMI-036`…`052` · `R-TLMI-053`…`063` | Dat · 2026-09-19 |
| **C18** | Ẩn khối **Tiêu đề** rồi thì `MSG_201` (Nội dung không được trống) còn bắt buộc không | P1 | `CLOSED-BA` | `R-TLMI-085`…`091` · `R-TLMI-230`…`258` | Dat · 2026-09-19 |
| **C19** | **Tách ô** đang có nội dung: nội dung về ô nào (Gộp có `MSG_404`, Tách không có quy định) | P1 | `CLOSED-BA` | `R-TLMI-120`…`181` | Dat · 2026-09-19 |
| **C20** | **Số dòng / số cột tối thiểu** của khối tự do (chỉ có trần 20 × 6) | P1 | `CLOSED-BA` | `R-TLMI-120`…`181` | Dat · 2026-09-19 |
| **C21** | Thứ tự **"lỗi đầu tiên"** khi khối có cả ô ở bảng chỉnh lẫn ô lưới trên trang xem trước | P1 | `CLOSED-BA` | `R-TLMI-230`…`258` | Dat · 2026-09-19 |
| **C22** | `MSG_103` hiện **"một lần"** — một lần mỗi lần mở xem trước, mỗi phiên, hay mỗi người dùng | P1 | `CLOSED-BA` | `R-TLMI-259`…`271` | Dat · 2026-09-19 |
| **C23** | *Lưu và đóng* (`MSG_401`) có hiện `MSG_101` trước khi đóng không | P1 | `CLOSED-BA` | `R-TLMI-230`…`258` | Dat · 2026-09-19 |
| **C24** | Quyền xét theo **chi nhánh đang làm việc** nhưng mẫu áp **mọi chi nhánh** — có cảnh báo không | P1 | `CLOSED-BA` | `R-TLMI-001`…`022` · `R-TLMI-023`…`035` | Dat · 2026-09-19 |
| **C38** | Hệ **`bieuMau` (biểu mẫu động)** đang tồn tại song song trong repo, cũng thiết kế trang in — chồng lấn mục đích | P1 | `CLOSED-BA` | quyết định kiến trúc FE | Dat · 2026-09-19 |

### P2

| ID | Chủ đề | Sev | Trạng thái | Luật bị chặn | Chốt |
|---|---|---|---|---|---|
| **C25** | AD lệch UC 4 điểm (D1–D4) | P2 | `CLOSED-AUTO` | — | 2026-09-19 |
| **C26** | `cfg_mau_in_chung_tu` không được xếp vào nhóm nào trong bảng phạm vi BR50.6 | P2 | `CLOSED-BA` | `R-TLMI-001`…`022` | Dat · 2026-09-19 |
| **C27** | Nguồn dữ liệu khối Xem trước: `_20` = hồ sơ tổng công ty · `_21` = chứng từ đang mở | P2 | `CLOSED-AUTO` | — | 2026-09-19 |
| **C28** | Cột `Bắt buộc = Y` cho ô Giấy và chữ trong khi giá trị lưu có thể **NULL** (theo chung) | P2 | `CLOSED-BA` | `R-TLMI-036`…`052` · `R-TLMI-053`…`063` | Dat · 2026-09-19 |
| **C29** | Vị trí **logo** khi Căn lề đầu trang ≠ Trái | P2 | `CLOSED-BA` | `R-TLMI-076`…`084` | Dat · 2026-09-19 |
| **C30** | Phạm vi cộng gộp: BR51.5 + `_20` giới hạn **Hóa đơn / phiếu xuất / phiếu nhập kho**, `_21` không nhắc lại | P2 | `CLOSED-BA` | `R-TLMI-259`…`271` | Dat · 2026-09-19 |
| **C31** | **Chia đều về 100%** khi lưới cột đang lọc bằng ô Tìm cột: áp cho mọi cột hay chỉ cột đang hiện | P2 | `CLOSED-BA` | `R-TLMI-092`…`119` | Dat · 2026-09-19 |
| **C32** | **Độ sâu Hoàn tác / Làm lại** — bao nhiêu bước | P2 | `CLOSED-BA` | `R-TLMI-217`…`229` | Dat · 2026-09-19 |
| **C33** | Ma trận ẩn/hiện **không phủ hộp thoại con** (Đặt tên khối, chọn trường, 4 hộp xác nhận) | P2 | `CLOSED-AUTO` | — | 2026-09-19 |
| **C34** | Lỗi đánh dấu trong chính file ma trận: `MT:108` mở đầu bằng marker `\1` hỏng; `MT:3` nhắc `Y*` mà thân ma trận không có ô nào mang `Y*` | P2 | `CLOSED-AUTO` | — | 2026-09-19 |

> Bốn trạng thái: `OPEN` · `CLOSED-AUTO` · `CLOSED-BA` (bắt buộc có **tên người + ngày**) · `HUỶ`.
> `CLOSED-BA` thiếu tên hoặc thiếu ngày thì `/gen-be` · `/gen-fe` **coi như `OPEN`**.

---

## Chi tiết các mục P0

### C01 · Khóa cộng gộp dòng khi in — có "thuế suất" hay không

| Bên | Nguyên văn | Nguồn | Bậc |
|---|---|---|---|
| A | "cộng gộp các dòng cùng mã hàng, đơn vị tính, đơn giá (và cùng số lô, hạn sử dụng nếu vật tư theo dõi theo lô)" | `Common/business_rules.md` BR51.5 (Phase 2) | 5 |
| B | "cùng mã hàng, cùng đơn vị tính, cùng đơn giá **và cùng thuế suất**" … "Hai dòng … **khác thuế suất** thì **không gộp**, in thành hai dòng riêng" | `PMKT-E-14549_20/5.screens/SCR_CauHinhBaoCaoChungTu.md:160-162` | 4 |

**Hệ quả:** hai bộ khóa cho **số dòng trên bản in khác nhau** — đây là số liệu người dùng đối chiếu
với hóa đơn. Không tự chọn.

**Câu hỏi cho BA:** Khóa cộng gộp có gồm **thuế suất** không?
· **A** — theo BR51.5, không tính thuế suất → hai dòng khác thuế suất bị gộp làm một, tiền thuế phải cộng dồn.
· **B** — theo SCR của epic `_20`, có tính thuế suất → giữ hai dòng.
**Hệ quả lên code:** khác nhau ở khóa gom nhóm và ở cách tính tiền thuế của dòng gộp.

---

### C02 · Điều kiện xóa bản ghi khi Lưu

| Bên | Nguyên văn | Nguồn | Bậc |
|---|---|---|---|
| A | `if (Mẫu đang **bằng** mẫu chuẩn?) then (Có) → Xóa bản ghi mẫu cùng bảng con` — phát biểu như **so sánh nội dung** | `4.usecases/…-01_ThietLapMauIn/AD_ThietLapMauIn.puml:30` | 1 |
| B | "nếu mẫu đang là mẫu chuẩn **(sau Đặt lại)** thì xóa bản ghi cùng bảng con" · "Xóa (D) xảy ra khi người dùng bấm **Đặt lại mẫu chuẩn** rồi **Lưu**" | `UC_ThietLapMauIn.md:54` · `3.crud-matrix.md:17` | 3 |

Thêm một mâu thuẫn **trong cùng một câu** `UC_ThietLapMauIn.md:54`: vừa "tạo mới nếu chưa có" vừa
"nếu mẫu đang là mẫu chuẩn thì xóa bản ghi".

**Hệ quả:** người dùng chỉnh tay rồi Hoàn tác hết về đúng mẫu chuẩn — theo A thì xóa bản ghi, theo B
thì vẫn ghi một bản ghi trùng y mẫu chuẩn. Và **Lưu ngay lần đầu mở, không sửa gì** thì có sinh bản
ghi rác hay không cũng chưa rõ.

**Câu hỏi cho BA:** Điều kiện xóa bản ghi là gì?
· **A** — **so sánh nội dung**: mẫu sau khi chỉnh đúng bằng mẫu chuẩn thì xóa bản ghi, bất kể đến từ thao tác nào.
· **B** — **theo hành động**: chỉ xóa khi người dùng bấm *Đặt lại mẫu chuẩn* rồi Lưu.
**Hệ quả lên code:** A cần hàm so sánh sâu mẫu ↔ mẫu chuẩn (và phải định nghĩa "bằng" gồm những gì);
B chỉ cần một cờ trên payload.

---

### C08 · Ảnh nền ≤1MB lưu ở đâu

CRUD matrix liệt kê đúng 5 entity (`cfg_mau_in_chung_tu` · `_khoi` · `_khoi_cot` · `_khoi_o` ·
`_khoi_chu_ky`), **không entity nào có chỗ chứa ảnh**. Tài liệu chỉ nói ảnh ≤ 1MB, jpg/png
(`MSG_PMKT-E-14549_21_209`).

**Câu hỏi cho BA:** ảnh nền lưu **binary trong DB** (cột `bytea`), lưu **đường dẫn tới object
storage**, hay dùng chung kho ảnh của Thông tin công ty? Có giới hạn kích thước điểm ảnh không? Ảnh
có bị **Hoàn tác** khôi phục không?

---

### C09 · Không có đặc tả cột của 5 bảng `cfg_mau_in_*`

Package tài liệu **không có file entity/ERD**. Tên 5 bảng có trong `3.crud-matrix.md`, tên các
thuộc tính rải rác trong bảng trường của `SCR_ThietLapMauIn.md`, nhưng **không có** khóa chính, khóa
ngoại, cột phân biệt loại khối, kiểu dữ liệu, ràng buộc.

Đặc biệt: **cấu trúc lưới của khối tự do** (số dòng, số cột, ô gộp `rowspan`/`colspan`, nội dung ô,
căn lề ô, nghiêng) là thứ người dùng thao tác được nhưng `cfg_mau_in_khoi_o` theo tài liệu chỉ có
`TenHienThi` và `InDam` — **không có chỗ lưu**.

**Câu hỏi cho BA:** xin file LDM/ERD của 5 bảng, hoặc xác nhận để dev đề xuất rồi BA duyệt.

---

### C10 · Cột / lưới bị xóa khỏi form ở phiên bản sau

Tài liệu chỉ quy định chiều **thêm** (`UC_ThietLapMauIn.md:26`: ô/cột mới tự vào kho trường, không
tự chen vào khối; bản tùy chỉnh thì ẩn + cờ *mới*). **Không có** chiều xóa.

**Câu hỏi cho BA:** cột đã cấu hình mà form bỏ đi, và trường đã đặt vào ô khối tự do mà form bỏ đi,
thì bản in xử lý sao — bỏ qua im lặng, in ô trống, hay báo lỗi dựng bản in?

---

### C11 · Nền luật là BR50 / BR51 của bộ Phase 2

`SCR_ThietLapMauIn.md` và cả hai UC viện dẫn **BR51.5 (Chứng từ)**, **BR51.6**, **BR50.7 (Hồ sơ đơn
vị)**. Ba mục này chỉ có trong `pmkt-docs/ba/Phase_2/Common/business_rules.md`. Bản
**Phase 1** mà repo đang dùng (`./docs/rules/br.sh --list`) chỉ có **BR1…BR49** — không có BR50,
không có BR51.

CLAUDE.md nói thẳng: *"Không có BR50 trong phạm vi Phase 1 — thấy tài liệu nhắc BR50 thì đó là tài
liệu Phase 2, bỏ qua."*

**Câu hỏi cho BA / quản lý dự án:** epic này có được chuyển vào phạm vi thi công của Phase 1 không?
· **A** — Có → phải bổ sung BR50/BR51 vào bản Phase 1 (hoặc tuyên bố epic này chạy theo bộ BR Phase 2), và sửa CLAUDE.md cho khớp.
· **B** — Không → epic dừng ở mức đặc tả, **không code lúc này**.
Đây là mục chặn nặng nhất: **mọi luật kế thừa thiết lập chung đều đứng trên BR51.5.**

---

### C12 · Epic nền `_20` và bảng `cfg_chi_nhanh` chưa tồn tại trong repo

Kiểm kê code 2026-09-19 (`extract/A5-hien-trang-code.md`):

| Thứ tài liệu coi là nền | Trong repo |
|---|---|
| Thông tin công ty (tên, MST, địa chỉ, ĐT, email, TK ngân hàng) | ✅ `platform_iam/tenant` + `client/src/features/heThong/thongTinCongTy/` |
| Người ký / 5 chức danh | ✅ trong màn Thông tin công ty |
| **Logo đơn vị** | ❌ chưa có trường |
| **Cấu hình chung giấy + chữ khi in** | ❌ chưa có — hiện chỉ nằm bên trong từng mẫu |
| **`cfg_chi_nhanh`** | ❌ bảng không tồn tại ở bất kỳ repo nào |
| **Cấu hình báo cáo chứng từ (epic `_20`)** | ❌ chưa có |

Toàn bộ cơ chế **kế thừa động** (ô để trống ⇒ lấy theo thiết lập chung ⇒ đổi theo khi thiết lập
chung đổi) **không có nguồn để kế thừa**.

**Câu hỏi cho BA / quản lý dự án:** làm epic `_21` trước khi có `_20` thì xử lý ra sao?
· **A** — Làm `_20` trước (hoặc làm phần "thiết lập chung" tối thiểu: giấy-chữ, 7 dòng đầu trang, 3 quy tắc in) rồi mới `_21`.
· **B** — `_21` tạm đọc mặc định hệ thống hardcode, để trống cơ chế kế thừa, nợ lại — **sẽ phải sửa lại toàn bộ tầng đọc cấu hình khi `_20` ra**.
· **C** — Gộp hai epic thành một đợt.

---

### C13 · Mã quyền của từng nghiệp vụ chưa nơi nào khai

Epic tuyên bố rõ: *"epic này **không** liệt kê chứng từ nào, nghiệp vụ nào có mẫu tùy chỉnh và không
khai mã quyền: **epic của từng nghiệp vụ** sẽ ghi 'có chức năng Thiết lập mẫu in' và tham chiếu về
đây, kèm mã quyền của nghiệp vụ đó"* (`1.function-breakdown.md`).

Không có epic nghiệp vụ nào đã khai. Bản code cũ đang gate bằng `HTMauIn.View` / `HTMauIn.Edit`
(seed ở `V1149`, **đã lên develop/staging**) — mã này **không** khớp mô hình "quyền theo nghiệp vụ"
mà tài liệu mô tả.

**Câu hỏi cho BA:** nghiệp vụ nào vào đợt đầu, và mã quyền là gì — `<ChucNang>.PrintConfig` theo
nghiệp vụ, hay giữ một mã dùng chung `HTMauIn.*`?

---

### C37 · Mô hình dữ liệu: jsonb đã phát hành vs 5 bảng quan hệ theo tài liệu

| | Đang có trong repo | Tài liệu yêu cầu |
|---|---|---|
| Bảng | `prn_mau_in_tuy_chinh` (một cột `jsonb` giữ cả mẫu) + `prn_mau_in_lich_su` | 5 bảng quan hệ `cfg_mau_in_chung_tu` · `_khoi` · `_khoi_cot` · `_khoi_o` · `_khoi_chu_ky` |
| Khóa | `(tenant_id, ma_loai_chung_tu)` | `(TenantId, loại chứng từ, **nghiệp vụ**)` |
| Migration | `V1148` · `V1149` · `V1150` — **đã merge vào `origin/develop` và `origin/staging`** (PR #223, commit `018d444f`, 2026-09-18) | — |

Migration đã phát hành thì **không sửa tại chỗ được**, phải viết migration mới.

**Câu hỏi cho BA / tech lead:**
· **A** — Đổi sang 5 bảng quan hệ theo tài liệu: viết migration mới `DROP` hai bảng cũ (chưa có dữ liệu thật vì API chưa lên) + tạo 5 bảng mới. Sạch, nhưng bỏ toàn bộ tầng BE đã viết.
· **B** — Giữ jsonb, coi 5 "entity" của CRUD matrix là **mô hình logic** chứ không phải bảng vật lý. Nhanh, nhưng lệch tài liệu và `/verify-spec` sẽ chấm trượt.
· **C** — Quan hệ cho phần cấu hình, jsonb cho riêng lưới khối tự do.

---

## Chi tiết các mục P1 đáng chú ý nhất

### C04 · SCR tự mâu thuẫn trong cùng một file

| Bên | Nguyên văn | Nguồn |
|---|---|---|
| A | "người ký (**tiêu đề**, tên, cờ in tên …) luôn theo thiết lập chung" | `SCR_ThietLapMauIn.md:257` |
| B | "tiêu đề và tên người ký lấy từ đó, **tiêu đề in ra sửa được riêng cho mẫu**" | `SCR_ThietLapMauIn.md:295` (BR6b) |

Ma trận ẩn/hiện (`SCR_ThietLapMauIn_MaTranAnHien.md:89`) cho *Tiêu đề in ra* = **Show** → đứng về
phía B. Figma frame 6 cũng vẽ ô **Tiêu đề in ra** sửa được.
**Không tự chốt bằng chênh bậc nguồn vì hai phát biểu cùng một file, cùng một bậc.**

**Câu hỏi cho BA:** *Tiêu đề in ra* của ô ký chức danh có phải cột lưu trên bảng chữ ký của mẫu
không, và có theo cơ chế theo-chung/riêng như Giấy và chữ không?

### C05 · Khối Chữ ký đọc hồ sơ đơn vị của chi nhánh nào

`TenNguoiKy*` và cờ `InTenNguoiKyTrenChungTu` nằm trên `cfg_chi_nhanh` nên **khác nhau giữa các chi
nhánh**, nhưng `SCR_ThietLapMauIn.md:295-298` không nói lấy theo chi nhánh nào. Suy theo BR50.7 thì
phải là **chi nhánh ghi trên chứng từ** (nhất quán với khối đầu trang) — nhưng tài liệu không viết
ra, và luật 9 cấm suy diễn.

### C16 · Không đưa riêng từng ô về theo chung được

Ma trận ghi thẳng: *"không có nhãn riêng cho từng ô và không đổi Show/Hide"*; SCR ghi *"Không có cách
đưa riêng từng ô về theo chung"*. Người dùng đổi một ô rồi muốn hoàn lại **chỉ ô đó** thì buộc reset
cả nhóm và gõ lại các ô khác, mà không có chỉ báo nào cho biết ô nào đang riêng.
**Câu hỏi cho BA:** đây là chủ ý hay sót đặc tả?

### C17 · Thao tác "xem" làm mẫu ngừng kế thừa

Đổi Khổ/Hướng giấy **trên thanh Xem trước** biến ô thành *riêng* (`SCR:256`), mà thanh Xem trước
**luôn hiện ở cả 6 khối** (`MT:67`). Một thao tác người dùng tưởng chỉ để xem thử làm mẫu **ngừng kế
thừa thiết lập chung vĩnh viễn**.
**Câu hỏi cho BA:** có xác nhận hành vi này là chủ ý không? Nếu không, thanh Xem trước nên chỉ đổi
cách xem, còn muốn đổi mẫu thì vào panel *Thiết lập mẫu*.

---

## Các mục `CLOSED-AUTO` (tự chốt theo thang thẩm quyền — có lý do, có chỗ đối chiếu)

### C25 · AD lệch UC 4 điểm
`AD_*.puml` **không bao giờ là nguồn luật** (audit-spec §1 bảng thứ tự đọc). Bốn điểm lệch:
D1 AD02:27 tự mở rộng `MSG_002` sang nhánh thiếu quyền **In** → tách thành **C15**;
D2 AD01:30 điều kiện xóa → nâng thành **C02** (P0);
D3 AD01:45-49 bỏ nhánh *Ở lại* của `MSG_401` → **lấy theo UC**;
D4 AD02:13-14 đặt sai chỗ hiện `MSG_103` → **lấy theo UC**.
Chốt: D3, D4 lấy theo UC; D1, D2 chuyển thành mục OPEN riêng.

### C27 · Nguồn dữ liệu khối Xem trước
Hai màn khác nhau nên không mâu thuẫn: màn `_20` xem trước bằng hồ sơ **tổng công ty**
(`S20:148`), màn `_21` xem trước bằng **chứng từ đang mở** và thông tin đơn vị theo **chi nhánh ghi
trên chứng từ** (`S21:306`, `S21:132`). Ghi nhận để dev không copy nhầm.

### C33 · Ma trận không phủ hộp thoại con
Trục cột của ma trận chỉ có 6 giá trị = 6 loại khối. Hộp **Đặt tên khối**, hộp **chọn trường** cạnh
ô, và 4 hộp xác nhận `MSG_…_401/402/403/404` **không** lên ma trận. Ghi nhận để `/plan-fe` không
tưởng ma trận đã phủ hết màn.

### C34 · Lỗi đánh dấu trong chính file ma trận
`MT:108` mở đầu bằng marker `\1` hỏng — không có neo `\1` ở bất kỳ ô nào trong thân ma trận; nội
dung ("Cột bỏ tick in giữ nguyên số Rộng % đang có, có thể để trống") đúng với `S21:276` nên vẫn
dùng được. `MT:3` nói ma trận có chú thích `Y*` nhưng thân ma trận không có ô nào mang `Y*` (đã
chuyển hết thành điều kiện `(đk-HG)` / `(đk-HN)`). **Đề nghị BA sửa file ma trận** — không ảnh hưởng
nghiệp vụ.

---

## Danh sách câu hỏi gửi BA (gom từ mọi mục `OPEN`)

| # | Mục | Câu hỏi đóng | Phương án |
|---|---|---|---|
| 1 | C11 | Epic này chạy theo bộ BR nào? | A. Bổ sung BR50/BR51 vào bản Phase 1 · B. Epic hoãn, chỉ dừng ở đặc tả |
| 2 | C12 | Làm `_21` trước khi có `_20` thì sao? | A. Làm `_20` trước · B. `_21` hardcode mặc định, nợ lại · C. Gộp hai epic |
| 3 | C37 | Mô hình dữ liệu | A. 5 bảng quan hệ, viết migration mới · B. Giữ jsonb · C. Lai |
| 4 | C09 | Xin LDM/ERD 5 bảng `cfg_mau_in_*` | A. BA cấp · B. Dev đề xuất, BA duyệt |
| 5 | C08 | Ảnh nền lưu ở đâu | A. bytea trong DB · B. object storage · C. dùng chung kho ảnh Thông tin công ty |
| 6 | C01 | Khóa cộng gộp có **thuế suất** không | A. Không (BR51.5) · B. Có (SCR `_20`) |
| 7 | C02 | Điều kiện xóa bản ghi khi Lưu | A. So sánh nội dung · B. Theo hành động *Đặt lại* |
| 8 | C10 | Cột/trường **bị xóa** khỏi form thì bản in xử lý sao | A. Bỏ qua im lặng · B. In ô trống · C. Báo lỗi |
| 9 | C13 | Mã quyền | A. `<ChucNang>.PrintConfig` theo nghiệp vụ · B. một mã chung `HTMauIn.*` |
| 10 | C03 | Logo có nằm trong 7 ô tick mẫu sửa riêng được không | A. Có (theo SCR + ma trận + Figma) · B. Không (theo BR51.5) |
| 11 | C04 | *Tiêu đề in ra* của ô ký chức danh | A. Mẫu sửa riêng được · B. Luôn theo thiết lập chung |
| 12 | C05 | Khối Chữ ký đọc `cfg_chi_nhanh` nào | A. Chi nhánh ghi trên chứng từ · B. Chi nhánh đang làm việc |
| 13 | C06 | Hai người cùng Lưu một mẫu | A. Khóa lạc quan + báo lỗi · B. Ghi đè, người sau thắng |
| 14 | C14 · C15 | Cấp mã `MSG_` cho 2 tooltip nút In disable và cho nhánh thiếu quyền In | A. BA cấp mã mới · B. Dùng `MSG_COMMON_003` |
| 15 | C16 · C17 | Kế thừa: không hoàn lại từng ô được, và thanh Xem trước phá kế thừa | A. Chủ ý, giữ nguyên · B. Sót đặc tả, cần bổ sung |
| 16 | C18 | Ẩn khối Tiêu đề thì Nội dung còn bắt buộc không | A. Vẫn bắt buộc · B. Bỏ qua validate khi khối ẩn |
| 17 | C19 · C20 | Tách ô có nội dung · số dòng/cột tối thiểu khối tự do | cần BA viết bổ sung |
| 18 | C38 | Hệ `bieuMau` (biểu mẫu động) và mẫu in chứng từ | A. Hai chức năng độc lập · B. Gộp · C. Bỏ một |

---

## Phần tài liệu thiếu hẳn

1. **File entity / ERD của 5 bảng `cfg_mau_in_*`** — không có trong package (C09).
2. **Chỗ lưu cấu trúc lưới khối tự do** (số dòng, số cột, gộp ô, nội dung ô, căn lề ô) — thao tác
   được nhưng không có trường nào (C09).
3. **Chỗ lưu ảnh nền** (C08).
4. **Danh sách nghiệp vụ vào đợt đầu + mã quyền** — epic cố ý giao cho epic nghiệp vụ, nhưng chưa
   epic nghiệp vụ nào khai (C13).
5. **Mã message cho 2 tooltip nút In disable và cho nhánh thiếu quyền In** (C14, C15).
6. **Quy định chống ghi đè đồng thời** (C06).
7. **Link chéo hỏng**: `../../Z.ThietLapMauIn/khao-sat-misa-sua-mau-in.md` — không tồn tại trên
   nhánh `main` của `pmkt-docs`.

---

## BR chung đã đối chiếu

| BR (Phase 1) | Áp ở đâu | Epic có lệch không |
|---|---|---|
| BR3 Popup | Đóng khi chưa lưu, 4 hộp xác nhận | **LỆCH** — `MSG_401` có **3 nút** (Lưu và đóng · Không lưu · Ở lại), BR3 chỉ có 2 nút. Epic thắng trong phạm vi epic, ghi nhận lệch |
| BR14 Form nhập liệu | nút Lưu / Đóng, hành vi form | khớp |
| BR15 Validation trường | 17 dòng bảng Validation, viền đỏ + scroll tới ô lỗi | khớp; epic chi tiết hơn (mở khối chứa lỗi) |
| BR16 Cảnh báo nghiệp vụ | format mã `MSG_[MODULE]_[ID]` | khớp — epic dùng `MSG_PMKT-E-14549_21_nnn` |
| BR24 Tooltip / help text | tooltip nút In disable | **thiếu mã message** → C14 |
| BR25 Phân quyền | quyền ⇒ **ẩn** nút và mục menu, server kiểm lại | khớp |
| BR26 Thông báo | toast `MSG_101`, `MSG_103` | khớp |
| BR29 Chính sách xóa dữ liệu | "xóa bản ghi mẫu cùng bảng con" khi Đặt lại + Lưu | **cần làm rõ** — BR29.1 bắt **chỉ xóa mềm**; tài liệu epic nói "xóa bản ghi". Xem C02 |
| BR30 Tùy biến giao diện | ẩn/hiện khối, ẩn/hiện cột, "phải giữ lại ít nhất 1 cột" | khớp — `MSG_203` là bản epic hóa của BR30 |
| BR43 Trim khi nhập liệu | mọi ô text của màn | khớp |
| BR46 Trường hệ thống trên mọi Entity | 5 bảng `cfg_mau_in_*` | khớp — nhưng C28: cột `Bắt buộc = Y` vs lưu NULL |
| **BR50 Chi nhánh** | hồ sơ đơn vị theo chi nhánh | ⛔ **không có trong bản Phase 1** → C11 |
| **BR51 Tùy chỉnh và in báo cáo** | nền của toàn bộ epic (51.5 Chứng từ) | ⛔ **không có trong bản Phase 1** → C11 |

---

## Nhắc cổng đặc tả

**Không còn mục `OPEN`.** 32 mục được đóng ngày **2026-09-19** theo uỷ quyền trực tiếp của user
(Dat): *"Làm hết các yêu cầu, tự làm theo đề xuất rồi note lại nội dung vào file .md khi bàn giao"*.
Căn cứ và nội dung từng quyết định ghi ở **[04-quyet-dinh-ban-giao.md](04-quyet-dinh-ban-giao.md)**.

⚠ Đây là `CLOSED-BA` **theo uỷ quyền của user**, không phải BA đã trả lời. Hai mục
`§5. Những thứ CỐ Ý lệch tài liệu` và `§7. Việc còn nợ BA` của file quyết định là danh sách BA phải
soát lại. BA chốt khác thì **sửa ở file quyết định trước, rồi mới sửa code**.

Ba quyết định gốc chi phối mọi thứ còn lại:

| | Quyết định |
|---|---|
| **Q-01** | Toàn bộ lưu **JSON**, không dựng 5 bảng quan hệ của `3.crud-matrix.md` |
| **Q-02** | Chức năng này áp bộ **BR Phase 2** (BR50.7 · BR51.5 · BR51.6) |
| **Q-03** | Làm thêm **tầng thiết lập chung tối thiểu** mà epic `_20` lẽ ra phải cấp |

Cổng đặc tả **đã mở** — `/plan-be` · `/plan-fe` · `/gen-be` · `/gen-fe` chạy được trên toàn bộ 271 luật.
