# PMKT-E-14549_21 Thiết lập mẫu in chứng từ — Bản đồ nguồn tài liệu

| | |
|---|---|
| Phiếu yêu cầu | `pmkt-docs/ba/Phase_2/PMKT-E-14549_21_ThietLapMauInChungTu/` |
| Mã viết tắt | **TLMI** |
| Ngày soát | **2026-09-19** |
| Bản tài liệu | bản sao tải từ GitHub `ospgroupvn/pmkt-docs` ngày **2026-09-19** — **blob SHA từng file ghi ở §1** |
| Commit tài liệu | `c78e322a1` (2026-09-18, "update") · `pmkt-docs` main `8d387213e` — theo `01-conflict.md` |
| Commit `pmkt-docs` bản local | `7e7f44619` (2026-09-03) — ⚠ **cũ hơn bản đã soát, không dùng làm mốc**, xem §1.1 |
| Trạng thái | **ĐÃ SOÁT** · 271 luật `R-TLMI-…` · 12 bất biến `INV-TLMI-…` · sổ mâu thuẫn **38 mục `C01…C38`** (xem `01-conflict.md`) |

> ⚠ **Vùng đóng băng.** Toàn bộ tài liệu của phiếu yêu cầu này nằm trong `pmkt-docs/ba/Phase_2/**`.
> Đọc theo **yêu cầu trực tiếp của user (Dat, 2026-09-19)** qua **bản sao tải về thư mục tạm** —
> chi tiết ở **§4**. Không file nào trong `pmkt-docs/` bị đọc trực tiếp hay bị sửa.

## §1.1 — Vì sao phải ghi blob SHA thay vì chỉ một commit

`docs/rules/*` yêu cầu ghi `git -C pmkt-docs rev-parse --short HEAD`. Ở đợt soát này con số đó
**không dùng được một mình**: `pmkt-docs` bản local đang ở `7e7f44619` (2026-09-03), trong khi tài
liệu được soát là **bản tải mới từ GitHub ngày 2026-09-19** (commit tài liệu `c78e322a1`, repo main
`8d387213e`). Hai bản lệch nhau hơn hai tuần.

Bổ sung: ghi **blob SHA của từng file** (giá trị `git hash-object` của đúng nội dung đã đọc). Bất kỳ
lúc nào cần đối chiếu "BA đã sửa tài liệu sau khi audit chưa", chạy `git hash-object <file>` và so
với cột **Blob SHA** ở §1 — lệch một ký tự là file đã đổi, mọi luật trích từ file đó phải soát lại.

---

## §1. Bảng file nguồn

### 1a. Trong phiếu yêu cầu `PMKT-E-14549_21_ThietLapMauInChungTu/` — 11 file

| # | File | Loại | Bậc | Trạng thái | Dòng | Bytes | Blob SHA |
|---|---|---|---|---|---|---|---|
| 1 | `6.messages.md` | message | **5** | duyệt | 47 | 7 336 | `b0b29bfbaab6053ac189706f9710c9060a05f63f` |
| 2 | `5.screens/SCR_ThietLapMauIn.md` | màn hình | **4** | duyệt | 377 | 70 609 | `761106f60d3e678bcab032567d01d409c23fd74c` |
| 3 | `4.usecases/PMKT-U-14549_21-01_ThietLapMauIn/UC_ThietLapMauIn.md` | UC | **3** | duyệt | 100 | 12 804 | `cedb8abadbfb86db017ee8294070ff1c875a2a69` |
| 4 | `4.usecases/PMKT-U-14549_21-02_InMauTuyChinh/UC_InChungTuMauTuyChinh.md` | UC | **3** | duyệt | 72 | 5 480 | `360008e58c559c8544a621275aef23b6085f4edb` |
| 5 | `3.crud-matrix.md` | CRUD | **3** | duyệt | 17 | 1 740 | `49bb0f1e5ed115a5d8c279edad918ffba1f8ba1d` |
| 6 | `Matrix/PMKT-E-14549_21_ThietLapMauInChungTu/SCR_ThietLapMauIn_MaTranAnHien.md` | ma trận | **3** | `DONE` (không phải DRAFT) | 109 | 12 403 | `1d3efd31d3139ffd6f48b90606616da8ab5b651e` |
| 7 | `1.function-breakdown.md` | phạm vi | **2** | duyệt | 26 | 4 050 | `8790d662618f0dd07135fe0618121d5b32861307` |
| 8 | `Matrix/PMKT-E-14549_21_ThietLapMauInChungTu/_scope.md` | chỉ mục ma trận | **2** | duyệt | 7 | 1 737 | `15f32d720049cdd6aa6efc8d30f291f472830dc6` |
| 9 | `4.usecases/PMKT-U-14549_21-01_ThietLapMauIn/AD_ThietLapMauIn.puml` | sơ đồ | **1** | — | 57 | 2 546 | `7326f3d753388cb27c57afece0b24df13aa401bd` |
| 10 | `4.usecases/PMKT-U-14549_21-02_InMauTuyChinh/AD_InChungTuMauTuyChinh.puml` | sơ đồ | **1** | — | 31 | 1 237 | `94c5b08954c91477196daf025a4e7b1776474b8c` |
| 11 | `2.usecase.puml` | sơ đồ | **1** | — | 18 | 524 | `f1dea4016ed86c1e4b7bb8a5c7e3556d80587345` |

**Không có file nào mang `[DRAFT]` hay `[CXM]`.** Ký hiệu `[CXM]` chỉ xuất hiện trong **chú giải** của
ma trận (`MT:49`, định nghĩa "chưa có căn cứ") chứ không gắn vào ô nào trong thân ma trận `MT:57-93`;
`_scope.md` ghi ma trận là **`DONE`**. Vì vậy ma trận được giữ bậc 3, không hạ về bậc 0.

### 1b. Nguồn ngoài phiếu yêu cầu — đã đọc và có trích luật

| # | File | Loại | Bậc | Vì sao phải mở | Ghi chú |
|---|---|---|---|---|---|
| 12 | `pmkt-docs/ba/Phase_2/Common/business_rules.md` — mục **BR50 Chi nhánh** và **BR51 Tùy chỉnh và in báo cáo** | BR chung | **5** trong phạm vi bộ Phase 2 | `SCR:257/260/267/298/334/374` viện dẫn trực tiếp `BR50.7`, `BR51.5`, `BR51.6` | ⚠ **KHÔNG có trong bản Phase 1** (BR1…BR49) mà repo đang dùng — xem §4 |
| 13 | `pmkt-docs/ba/Phase_2/PMKT-E-14549_20_CauHinhBaoCaoChungTu/5.screens/SCR_CauHinhBaoCaoChungTu.md` | màn hình (epic khác) | **4** trong phạm vi epic `_20` | Nguồn của **mọi giá trị mặc định** mà mẫu in kế thừa; nguồn nguyên văn hai tooltip nút In | 229 dòng |
| 14 | `pmkt-docs/ba/Phase_2/PMKT-E-14549_20_CauHinhBaoCaoChungTu/6.messages.md` | message (epic khác) | **5** trong phạm vi epic `_20` | Đối chiếu để chứng minh epic `_21` **không** tái dùng mã của `_20` | 43 dòng |
| 15 | `pmkt-docs/ba/Phase_2/PMKT-E-14549_20_CauHinhBaoCaoChungTu/1.function-breakdown.md` | phạm vi (epic khác) | **2** | Xác định ranh giới `_20` ↔ `_21` | 27 dòng |
| 16 | `pmkt-docs/ba/Phase_2/PMKT-E-14549_CauHinhBanDau/5.screens/SCR_CauHinhChiTiet/SCR_CauHinhChiTiet_ThongTinCongTy.md` | màn hình (epic khác) | **4** trong phạm vi epic `CauHinhBanDau` | Nguồn của 5 chức danh người ký, cờ "In tên người ký", ảnh logo | 165 dòng |
| 17 | Figma — file `ymMyg329ejsgCWg28CNmGl`, section node `71956-288871` (8 frame) | thiết kế | **1** | Đối chiếu nhãn UI nguyên văn, control, ranh giới màn | Xem §1d |

### 1c. Bậc thẩm quyền — quy ước dùng trong đợt soát này

| Bậc | Loại nguồn | Ý nghĩa khi xử lý mâu thuẫn |
|---|---|---|
| **5** | `6.messages.md` | Nguồn duy nhất của **mã + nguyên văn** message. Nguồn khác ghi khác ⇒ ghi mâu thuẫn, không tự mở rộng. |
| **5** | BR chung (`business_rules.md`) | Luật nền. Epic im lặng ⇒ BR vẫn áp. Epic thắng trong **đúng phạm vi epic** và phải báo rõ đang lệch BR nào. |
| **4** | `SCR_*` | Luật nội bộ màn, trường, validation. Nguồn chi tiết nhất của epic. |
| **3** | `UC_*`, `3.crud-matrix.md`, `Matrix/*_MaTranAnHien.md` | Luồng, tiền/hậu điều kiện, AC, CRUD, trạng thái ẩn/hiện. |
| **2** | `1.function-breakdown.md`, `_scope.md` | Phạm vi và ranh giới, không phải luật chi tiết. |
| **1** | `*.puml`, Figma | **Đối chiếu**, KHÔNG tự bổ sung nghiệp vụ. AD thiếu bước = giản lược; AD nói ngược = ghi mâu thuẫn. |
| **0** | file `[DRAFT]` / `[CXM]` | Không có file nào ở bậc này trong phiếu yêu cầu này. |

Quy tắc áp dụng (theo `nguon-va-tham-quyen.md`): các nguồn SCR / UC / Matrix nói ngược nhau ⇒ `OPEN`,
**không mặc định một loại tài liệu thắng loại khác**.

### 1d. Figma — 8 frame đã đối chiếu

Ảnh đã tải về thư mục tạm (PNG 1440×1024), **không đưa vào repo**.

| # | Frame | node-id | Dùng để đối chiếu |
|---|---|---|---|
| 0 | SCR_XemTruocBanIn — Xem trước bản in | `71956:289768` | Lối vào thứ hai, nút Sửa mẫu (R-TLMI-027, R-TLMI-268) |
| 1 | SCR_ThietLapMauIn — Thiết lập toàn trang | `71956:288872` | Bảng chỉnh Thiết lập mẫu, link "Theo thiết lập chung" (R-TLMI-040, R-TLMI-053) |
| 1b | Thiết lập mẫu · Hình nền = Khung viền | `72218:690704` | Ẩn/hiện Căn ảnh + Ảnh (R-TLMI-068, R-TLMI-071) |
| 2 | Đang chọn Bảng hàng hoá | `71956:289243` | Lưới cột, "Chia đều về 100%", dòng tổng (R-TLMI-110, R-TLMI-114) |
| 3 | Đang chọn khối tự do + menu chuột phải | `71974:27549` | Thanh công cụ, menu chuột phải, ô lỗi (R-TLMI-170, R-TLMI-171, R-TLMI-235) |
| 4 | Đang chọn Thông tin đầu trang | `72163:26808` | Bảy ô tick kèm giá trị thật (R-TLMI-077, R-TLMI-081) |
| 5 | Đang chọn Tiêu đề | `72163:27460` | Ghi chú dòng ngày tháng (R-TLMI-090) |
| 6 | Đang chọn Chữ ký | `72163:28110` | Bảng ô ký, hộp ghi chú cờ in tên (R-TLMI-182, R-TLMI-196) |

⚠ Hai ghi chú bắt buộc về Figma:

1. Nghiệp vụ mẫu trong Figma là **Chứng từ bán hàng**, KHÔNG phải Chứng từ mua dịch vụ (pilot của
   bản code cũ ở §2). Đừng lấy tên nghiệp vụ trong ảnh làm phạm vi.
2. Figma đếm được **9** ô màu preset + ô nhập hex, trong khi `SCR:301` nói **"10 ô màu"**. Lệch số
   đếm ⇒ ghi ở `02-rules.md` §Z-04, **không tự chọn con số nào**.

---

## §1b. Độ phủ dòng

Dải cộng lại **phải phủ 1..N** từng file. Số dòng lấy bằng `wc -l` trên bản sao đã tải.

### Phủ đầy đủ — 11 file của phiếu yêu cầu

| File | Tổng dòng | Dải đã đọc | Cách đọc | Khoảng trống & lý do |
|---|---|---|---|---|
| `5.screens/SCR_ThietLapMauIn.md` | **377** | **1–212** + **209–377** | `sed -n` theo lô 45 dòng (1-45, 45-90, 90-135, 135-180, 180-212) cho nửa đầu; đọc theo **mục** cho nửa sau (`### Chức năng` 209-238 · chú thích `Y*` 240-243 · BR1…BR13 244-334 · Validation 336-356 · Thông báo 358-369 · Liên kết 371-377) | — (hai dải chồng nhau ở 209-212, không hở) |
| `6.messages.md` | **47** | 1–47 | `Read` cả file (7 KB) | — |
| `4.usecases/…21-01…/UC_ThietLapMauIn.md` | **100** | 1–100 | `Read` cả file (12 KB) | — |
| `4.usecases/…21-02…/UC_InChungTuMauTuyChinh.md` | **72** | 1–72 | `Read` cả file (5 KB) | — |
| `3.crud-matrix.md` | **17** | 1–17 | `Read` cả file | — |
| `Matrix/…/SCR_ThietLapMauIn_MaTranAnHien.md` | **109** | 1–109 | `Read` cả file (12 KB) | — |
| `1.function-breakdown.md` | **26** | 1–26 | `Read` cả file | — |
| `Matrix/…/_scope.md` | **7** | 1–7 | `Read` cả file | — |
| `4.usecases/…21-01…/AD_ThietLapMauIn.puml` | **57** | 1–57 | `Read` cả file | — |
| `4.usecases/…21-02…/AD_InChungTuMauTuyChinh.puml` | **31** | 1–31 | `Read` cả file | — |
| `2.usecase.puml` | **18** | 1–18 | `Read` cả file | — |

Biên giữa hai nửa của `SCR_ThietLapMauIn.md` đã xác nhận bằng số dòng thật: dòng **207** = `</div>`
đóng bảng khối Chữ ký · dòng **208** = dòng trống · dòng **209** = `### Chức năng`.

### Nửa sau `SCR_ThietLapMauIn.md` — chứng minh không hở mục nào

| Dải | Mục | Trạng thái |
|---|---|---|
| 209–238 | `### Chức năng` — bảng 24 dòng nút / thao tác | đã đọc, đã trích |
| 239 | dòng trống | — |
| 240–243 | `### Rule` + chú thích `Y*` (SCR:242) | đã đọc, đã trích |
| 244–248 | **BR1** Phạm vi mẫu | đã đọc, đã trích |
| 250–257 | **BR2** Giấy và chữ | đã đọc, đã trích |
| 259–264 | **BR3** Mẫu chuẩn hệ thống và Bố cục mẫu | đã đọc, đã trích |
| 266–269 | **BR4** Khối Thông tin đầu trang và khối Tiêu đề | đã đọc, đã trích |
| 271–281 | **BR5** Khối Bảng | đã đọc, đã trích |
| 283–292 | **BR6** Khối tự do | đã đọc, đã trích |
| 294–298 | **BR6b** Khối Chữ ký | đã đọc, đã trích |
| 300–302 | **BR7** Thiết lập riêng của mẫu | đã đọc, đã trích |
| 304–307 | **BR8** Xem trước | đã đọc, đã trích |
| 309–310 | **BR9** Đặt lại mẫu chuẩn | đã đọc, đã trích |
| 312–318 | **BR10** Kiểm tra, trạng thái, Hoàn tác, Lưu | đã đọc, đã trích |
| 320–322 | **BR11** Đóng và quyền | đã đọc, đã trích |
| 324–328 | **BR12** Hai lối vào | đã đọc, đã trích |
| 330–334 | **BR13** Dựng bản in theo mẫu | đã đọc, đã trích |
| 335 | dòng trống | — |
| 336–356 | `### Bảng kiểm tra dữ liệu (Validation)` — 17 dòng | đã đọc, chép nguyên văn vào `R-TLMI-239` |
| 358–369 | `### Thông báo` — 8 hành động | đã đọc, chép vào §Y của `02-rules.md` |
| 371–377 | `## Liên kết` | đã đọc, xem §1c bên dưới |

Các dòng không liệt kê là dòng trống hoặc thẻ `<div>` đóng / mở bảng. **Không bỏ sót dải nào.**

⚠ **`BR1…BR13` và `BR6b` là BR NỘI BỘ MÀN** (định nghĩa bằng heading ngay trong `SCR:244-334`) —
**không** phải BR chung của `business_rules.md`. BR chung được viện dẫn chỉ gồm **BR50.7 · BR51.5 · BR51.6**.

### Phủ nguồn ngoài phiếu yêu cầu

| File | Tổng dòng | Dải đã đọc | Khoảng trống & lý do |
|---|---|---|---|
| `Common/business_rules.md` — trích **BR50 + BR51** | 179 (bản trích) | 1–179 của bản trích | Chỉ trích **hai mục BR50, BR51**; các BR khác của bộ Phase 2 **cố ý không đọc** — ngoài phạm vi viện dẫn của `SCR` |
| `PMKT-E-14549_20…/SCR_CauHinhBaoCaoChungTu.md` | 229 | 1–229 | — |
| `PMKT-E-14549_20…/6.messages.md` | 43 | 1–43 | — |
| `PMKT-E-14549_20…/1.function-breakdown.md` | 27 | 1–27 | — |
| `PMKT-E-14549_CauHinhBanDau/…/SCR_CauHinhChiTiet_ThongTinCongTy.md` | 165 | 1–165 | — |

---

## §1c. Link chéo của `SCR_ThietLapMauIn.md`

Lấy bằng cách quét mọi liên kết markdown trong file. **9 đích link phân biệt**, mỗi đích một trạng
thái — không có "chưa xem".

| # | Link | Từ dòng | Trạng thái | Luật rút ra / Lý do bỏ qua |
|---|---|---|---|---|
| 1 | `../4.usecases/PMKT-U-14549_21-01_ThietLapMauIn/UC_ThietLapMauIn.md` | 373 | **ĐÃ MỞ** | Đọc đủ 100 dòng. Sinh ra phần lớn nhóm A, B, N — tiêu biểu: `R-TLMI-008` (4 loại khối), `R-TLMI-025` (form thêm mới không có nút In), `R-TLMI-247` (một transaction), `R-TLMI-251`…`254` (ba lựa chọn khi đóng) |
| 2 | `../4.usecases/PMKT-U-14549_21-02_InMauTuyChinh/UC_InChungTuMauTuyChinh.md` | 373 | **ĐÃ MỞ** | Đọc đủ 72 dòng. Sinh ra toàn bộ nhóm P — tiêu biểu: `R-TLMI-259`, `R-TLMI-260` (fallback mẫu chuẩn + `MSG_103`), `R-TLMI-261` (menu In không mở được), `R-TLMI-270` (không mở xem trước khi lỗi), `R-TLMI-271` |
| 3 | `../../PMKT-E-14549_20_CauHinhBaoCaoChungTu/5.screens/SCR_CauHinhBaoCaoChungTu.md` | 5 · 251 · 374 | **ĐÃ MỞ** | Đọc đủ 229 dòng. Nguồn của mọi **giá trị mặc định hệ thống** (A4 · Tự động · 7 cột · lề 1/1,5/1/1 · Times New Roman · 12) dùng ở `R-TLMI-054`…`063`; nguồn `R-TLMI-079` (bỏ dòng trống), `R-TLMI-083` (thứ tự dòng đầu trang), và **nguyên văn hai tooltip** ở `R-TLMI-261` |
| 4 | `../../PMKT-E-14549_CauHinhBanDau/5.screens/SCR_CauHinhChiTiet/SCR_CauHinhChiTiet_ThongTinCongTy.md` | 295 · 375 | **ĐÃ MỞ** | Đọc đủ 165 dòng. Nguồn của 5 chức danh người ký, các cột `TieuDeNguoiKy*` / `TenNguoiKy*` / `InTenNguoiKyTrenChungTu` (đều nằm trên `cfg_chi_nhanh`) ⇒ `R-TLMI-182`, `R-TLMI-186`, `R-TLMI-196`, và **là gốc của mâu thuẫn C05** (`R-TLMI-199`). Cũng là nguồn `cfg_tenant.Logo` — một logo dùng chung toàn đơn vị, chi nhánh không có logo riêng (`R-TLMI-078`) |
| 5 | `../../Common/business_rules.md#515-chứng-từ` (**BR51.5**) | 257 · 298 · 334 · 374 | **ĐÃ MỞ** | Đọc nguyên văn mục 51.5. Luật nền cho `R-TLMI-046` (người ký luôn theo chung), `R-TLMI-047` (ba quy tắc in), `R-TLMI-058` (hướng Tự động của chứng từ), `R-TLMI-090` / `R-TLMI-197` (ngày ký = ngày chứng từ), `R-TLMI-119` / `R-TLMI-266` (cộng gộp). **Là một bên của mâu thuẫn C01, C03, C04.** ⚠ BR bộ **Phase 2** |
| 6 | `../../Common/business_rules.md#507-hồ-sơ-đơn-vị` (**BR50.7**) | 267 | **ĐÃ MỞ** | Đọc nguyên văn mục 50.7. Luật nền cho `R-TLMI-078` và `R-TLMI-267`: thông tin in trên chứng từ lấy từ hồ sơ của **chi nhánh ghi trên chính bản ghi đó**; mọi nơi đi `ChiNhanhId` → `cfg_chi_nhanh`, không đi ngược lên đơn vị cha. ⚠ BR bộ **Phase 2** |
| 7 | `../../Common/business_rules.md#516-khóa-cột-và-khóa-tham-số-của-báo-cáo` (**BR51.6**) | 260 | **ĐÃ MỞ** | Đọc nguyên văn mục 51.6. Ghi ở `R-TLMI-092`: khóa kỹ thuật duy nhất trong phạm vi, không đổi suốt vòng đời, không dùng lại khóa của cột đã bỏ. ⚠ `SCR:260` chỉ nói "**như** BR51.6" — mượn *nguyên tắc*; nguyên văn BR51.6 chỉ nói về cột và tham số **báo cáo** (`cfg_bao_cao_tuy_chinh_cot.MaCot`…), không phải `cfg_mau_in_khoi_cot` / `cfg_mau_in_khoi_o`. ⚠ BR bộ **Phase 2** |
| 8 | `../../Common/LDM_update/ldm-HeThong.puml` | 376 | **BỎ QUA** | Là sơ đồ LDM (bậc 1). Năm entity mà nó chứa (`ENT_cfg_mau_in_chung_tu`, `…_khoi`, `…_khoi_cot`, `…_khoi_o`, `…_khoi_chu_ky`) **đã được `3.crud-matrix.md` liệt kê đủ và ở bậc cao hơn**. Mở thêm chỉ để lấy **cấu trúc cột**, mà đó là **quyết định kiến trúc thuộc `/plan-be`**, không thuộc `/audit-spec` (`nguon-va-tham-quyen.md` §5). Khoảng trống này đã ghi thành `Z-07` để `/plan-be` xử lý |
| 9 | `../../Z.ThietLapMauIn/khao-sat-misa-sua-mau-in.md` | 377 | **BỎ QUA** | **Link hỏng — đường dẫn không tồn tại trên nhánh `main`** của `pmkt-docs`. Ngay cả khi tồn tại, `SCR:377` tự gán nhãn "Khảo sát MISA và bản demo" ⇒ **tài liệu tham khảo, không phải nguồn luật** (khảo sát sản phẩm bên thứ ba). Đề nghị BA sửa hoặc bỏ link |

**Không link nào trỏ vào vùng cần `BỎ QUA` vì Phase_2** — vì **chính phiếu yêu cầu này đã nằm trong
`Phase_2`**; quy tắc "link trỏ vào `Phase_2/**` ⇒ BỎ QUA" của `mau-tai-lieu.md` không áp được ở đây.
Xem §4.

---

## §2. Mã nguồn tham chiếu — bộ đặc tả CŨ và kế hoạch CŨ

⚠ Repo **đã có sẵn** một bộ đặc tả và một bộ kế hoạch cho cùng chủ đề "mẫu in chứng từ", dựng trước
đợt này. **Bộ đặc tả hiện tại thay thế bộ cũ.**

| Đường dẫn trong repo | Là gì | Dựng từ nguồn nào | Trạng thái |
|---|---|---|---|
| `docs/doing/mau-in-chung-tu-spec/` (`00-source-map.md` · `01-conflict.md` · `02-rules.md` · `03-scenarios.md`) | Bộ đặc tả 4 file của **đợt trước** | **Mock HTML**, đợt 2026-09-17 — không dựng từ package BA `PMKT-E-14549_21` | **ĐÃ BỊ THAY THẾ** bởi `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/` |
| `docs/doing/mau-in-chung-tu/` (`00-plan-tong-the.md` · `01-hop-dong-json-va-api-v1.md` · `02-anh-xa-giao-dien-va-base-component.md` · `03-ban-giao.md` · `fixtures/` · `sync-catalog.sh`) | Kế hoạch BE + FE của **đợt trước** | cùng đợt 2026-09-17 | **KHÔNG dùng làm nguồn luật.** Có thể còn giá trị tham khảo về cấu trúc thư mục, nhưng mọi luật nghiệp vụ phải lấy từ `02-rules.md` của bộ này |

Bốn khác biệt **đáng kể** giữa bản mock 2026-09-17 và tài liệu BA lần này — đủ để kết luận bộ cũ
không còn dùng được làm nguồn:

1. Bản cũ dựng màn thành **route riêng ở phân hệ Hệ thống**; tài liệu BA lần này là **modal toàn màn
   mở từ form chứng từ**, hai lối vào (`R-TLMI-023`, `R-TLMI-027`).
2. Bản cũ **không có** khối tự do dạng **lưới ô kiểu Excel** (gộp / tách ô, menu chuột phải) —
   đây là nguyên cả nhóm I, 62 luật.
3. Bản cũ **tự khai 4 ô ký**; tài liệu BA lấy **5 chức danh từ Thiết lập người ký** cộng ô ký tự do
   (`R-TLMI-182`).
4. Bản cũ **không có cơ chế theo chung / riêng** (kế thừa động từ Cấu hình báo cáo chứng từ) — đây là
   nhóm C, 17 luật, và là chỗ dễ code sai nhất (`R-TLMI-037`, `R-TLMI-038`).

Thêm: pilot của bản cũ là **Chứng từ mua dịch vụ**, pilot của Figma lần này là **Chứng từ bán hàng**.

**`/audit-spec` không đối chiếu tài liệu với code hiện trạng** — việc đó thuộc `/plan-be` và
`/plan-fe` (`nguon-va-tham-quyen.md` §5). Mục này chỉ để cảnh báo hai thư mục cũ tồn tại, tránh
người sau nhặt nhầm nguồn.

---

## §3. Phát biểu KHÔNG kiểm được bằng máy

Câu tài liệu không quy được về `WHEN` / `THEN` đo được. Gộp từ ba lượt trích (`SCR:1-208` ·
`SCR:209-377` · UC + messages), đã khử trùng lặp. **Không mục nào trong đây là mâu thuẫn** — chúng chỉ
cần BA viết lại cho rõ nếu muốn test tự động phủ được.

| # | Phát biểu | Nguồn | Vì sao không kiểm được | Luật liên quan |
|---|---|---|---|---|
| K-01 | "trang in **vẽ sống** bằng dữ liệu của chứng từ đang mở" · "mọi thay đổi trên màn **vẽ lại ngay**" | `SCR:3` · `SCR:23` · `SCR:305` | "ngay" / "sống" không có ngưỡng thời gian; không nói có debounce khi gõ chữ | R-TLMI-217, R-TLMI-218 |
| K-02 | "chỉnh lưới ô của khối tự do **như bảng Excel**" | `SCR:23` | So sánh cảm tính, không liệt kê được tập hành vi | nhóm I |
| K-03 | "Màn **toàn trang**", bố cục ba cột | `SCR:18` | Trình bày, không có kích thước hay tỷ lệ cột | R-TLMI-201 |
| K-04 | "hộp chọn có tìm kiếm **hiện cạnh ô**" | `SCR:187` · `SCR:288` | "cạnh ô" không định vị được chính xác | R-TLMI-150 |
| K-05 | Nút "**mờ**" (Lưu, Hoàn tác / Làm lại, thanh công cụ khối tự do) | `SCR:40` · `SCR:77` · `SCR:79` | `SCR` không nói "mờ" = disable hay chỉ giảm opacity. **Đã được ma trận chốt**: `MT:49` định nghĩa `Disable` = "Hiện xám, read-only" ⇒ thực tế kiểm được, giữ ở đây chỉ để ghi nhận cách diễn đạt của `SCR` | R-TLMI-135, R-TLMI-162, R-TLMI-226, R-TLMI-240 |
| K-06 | "hai cách cho **cùng kết quả**" (kéo ở Bố cục mẫu và kéo trên trang xem trước) | `SCR:261` | Chỉ khẳng định tương đương; không nói kết quả chuẩn khi thả vào **giữa** hai khối hay thả ra ngoài vùng khối | R-TLMI-205 |
| K-07 | "mỗi ô rộng **tối thiểu 4 cm**; hết chỗ thì ô tiếp theo tự xuống hàng" | `SCR:297` | Ví dụ A4 dọc cho 4 ô/hàng, nhưng không nói xử lý khi bề ngang còn lại < 4 cm với **một** ô duy nhất, hay khi lề lớn khiến bề ngang < 4 cm | R-TLMI-194, R-TLMI-195 |
| K-08 | "Độ đậm **5–100 %**" áp cho cả Khung viền lẫn Ảnh | `SCR:302` | Không định nghĩa độ đậm là opacity hay độ xám ⇒ kết quả in không so sánh được | R-TLMI-072 |
| K-09 | "ảnh giữ tỷ lệ, chiếm **khoảng nửa trang**" | `SCR:302` | "khoảng nửa trang" không có công thức (nửa theo chiều rộng? theo diện tích?) | R-TLMI-073 |
| K-10 | "Chỗ trống ký Thấp / Vừa / Cao = khoảng trống **khoảng** 1 / 2 / 3 cm" | `SCR:298` | Có chữ "khoảng", không có dung sai | R-TLMI-198 |
| K-11 | "ô trống đang chọn có **chữ gợi ý** cách đưa nội dung vào" | `SCR:291` | Không cho nguyên văn chữ gợi ý ⇒ `msg.sh` không có gì để đối chiếu i18n | R-TLMI-177 · `Z-01` |
| K-12 | "chọn một trong **10 ô màu**" | `SCR:301` | Không liệt kê 10 mã màu cụ thể; Figma đếm được 9 | R-TLMI-066 · `Z-04` |
| K-13 | "**Số tiền bằng chữ** đọc từ ô tổng thanh toán **theo quy tắc đọc số chung**" | `SCR:290` | "quy tắc đọc số chung" không trích mã BR nào trong phạm vi tài liệu đã đọc | R-TLMI-165 · `Z-22` |
| K-14 | "mẫu trên màn **đúng bằng mẫu chuẩn** (sau Đặt lại) thì xóa bản ghi" | `SCR:318` | Không định nghĩa phép so sánh "đúng bằng" (so sâu toàn bộ cây? hay chỉ cần đã bấm Đặt lại và không sửa gì sau đó?) | R-TLMI-021 — **đã nâng thành mâu thuẫn C02** |
| K-15 | "tên khối gợi ý `Khối tự do <n>`" | `SCR:59` · `SCR:284` | `n` là số thứ tự gì — không quy định | R-TLMI-120 · `Z-23` |
| K-16 | "ghi lại toàn bộ khối, cột, ô lưới, chữ ký (**xóa hết bản cũ, ghi bản mới**)" | `SCR:318` | Không nói có giữ id cũ hay không ⇒ không kiểm được ảnh hưởng tới dữ liệu tham chiếu | R-TLMI-247 · `Z-10` |
| K-17 | "để người dùng **biết đang bật/tắt dòng nào**" | `SCR:131` | Là **mục đích**, không phải điều kiện | R-TLMI-081 |
| K-18 | "Người dùng nhìn thấy kết quả **ngay** bằng dữ liệu của chứng từ đang mở" | `SCR:3` | "ngay" không có ngưỡng thời gian (trùng ý K-01 nhưng ở phần mở đầu màn) | R-TLMI-217 |
| K-19 | "**Xuất file** theo hành vi chung của bản in chứng từ" | `UC02:25` | Hành vi chung (định dạng, PDF / Excel?) không khai ở đây. `AD02:21` nói "In / Xuất PDF" nhưng AD là bậc 1, không phải nguồn luật | R-TLMI-268 · `Z-39` |
| K-20 | "đồng bộ hai ô Khổ giấy / Hướng giấy là **cùng một trường**" | `SCR:79` · `SCR:256` | Không nói đồng bộ hai chiều **tức thời** hay có độ trễ. Đủ để code (một state chung), nhưng không đo được thời điểm | R-TLMI-044 |

### §3.1 — AD đơn giản hóa / AD nói ngược

`AD` là bậc 1, chỉ dùng để **đối chiếu**. Bốn điểm lệch so với UC, ghi lại để **không ai code theo AD**:

| # | Điểm lệch | AD nói | UC nói | Xử lý |
|---|---|---|---|---|
| D-1 | Điều kiện **xóa bản ghi khi Lưu** | `AD01:30` — `if (Mẫu đang **bằng** mẫu chuẩn?) then (Có) → Xóa bản ghi mẫu cùng bảng con` (phát biểu như **so sánh nội dung**) | `UC01:54` "nếu mẫu đang là mẫu chuẩn **(sau Đặt lại)**"; `CRUD:17` "Xóa (D) xảy ra khi người dùng bấm **Đặt lại mẫu chuẩn** rồi **Lưu**" (phát biểu như **đến từ hành động**) | **AD nói ngược, không phải giản lược** ⇒ đã nâng thành **mâu thuẫn C02**, chặn `R-TLMI-021` |
| D-2 | Nhánh **Đóng** thiếu lựa chọn "Ở lại" | `AD01:45-49` — hỏi `MSG_401` rồi **luôn** `:Đóng màn;`, không rẽ ba nhánh | `UC01:87` — *Ở lại* **giữ màn**; *Lưu và đóng* chạy bước 6–9 **rồi** đóng | **AD đơn giản hóa.** UC là chuẩn: `R-TLMI-251`…`254` |
| D-3 | `MSG_002` dùng cho nhánh **không được in** | `AD02:26-27` — "Nút In disable kèm tooltip … **hoặc từ chối MSG_PMKT-E-14549_21_002**" | `UC02` NL2 (`:53-56`) **không nhắc** `MSG_002`; `MSG:7` định nghĩa `_002` là "Không có quyền **Thiết lập mẫu in**" | **AD tự mở rộng.** Theo thẩm quyền bậc 5 của `6.messages.md`, **không** dùng `_002` cho nhánh thiếu quyền In. Khoảng trống ghi thành `Z-02` |
| D-4 | Thời điểm hiện `MSG_103` | `AD02:13-14` — hiện ngay ở nhánh chưa có mẫu, **trước** khi đọc thiết lập chung / dựng bản in | `UC02:22` — hiện "**một lần trên màn xem trước bản in**" | **AD giản lược.** Giữ theo UC: `R-TLMI-260` |

Các chỗ **AD khớp UC**, đã đối chiếu và không lệch: lối vào & kiểm quyền (`AD01:6-9` ↔ `UC01:47-48`) ·
nạp mẫu chuẩn 4 khối (`AD01:14-15` ↔ `UC01:23`) · đọc `cfg_tenant` / `cfg_chi_nhanh` (`AD01:17` ↔
`UC01:49`) · vòng chỉnh + vẽ lại + trạng thái (`AD01:19-25` ↔ `UC01:51`) · một transaction
(`AD01:33` ↔ `UC01:54`) · lỗi đầu tiên 201…216 (`AD01:37` ↔ `UC01:67`) · Hoàn tác / Làm lại
(`AD01:43-44` ↔ `UC01:76-77`) · fallback mẫu chuẩn khi in (`AD02:12-14` ↔ `UC02:48-51`) · cộng gộp
mặt hàng (`AD02:17` ↔ `UC02:41`) · lỗi dựng bản in (`AD02:23` ↔ `UC02:60`).

### §3.2 — Ranh giới: thứ tài liệu **cố ý** không quy định (không phải thiếu sót)

Ghi để không ai đi tìm trong epic này. Chi tiết ở `02-rules.md` §Z.6.

| Hạng mục | Do ai quyết | Nguồn nguyên văn |
|---|---|---|
| **Chứng từ nào, nghiệp vụ nào** có mẫu tùy chỉnh | epic của từng nghiệp vụ | `FB:9` — "Epic này **không** liệt kê chứng từ nào, nghiệp vụ nào có mẫu tùy chỉnh" |
| **Mã quyền** Thiết lập mẫu in và quyền In | epic của từng nghiệp vụ | `FB:9` · `UC01:11` — "(mã do epic nghiệp vụ khai báo)" |
| **Đặc tả form** (các ô, các lưới, cột của lưới) — nguồn của mẫu chuẩn và kho trường | epic nghiệp vụ | `UC01:16` · `CRUD:15` |
| **Giá trị mặc định** của Giấy và chữ + bảy dòng thông tin đơn vị | epic `PMKT-E-14549_20` | `FB:9` · `UC01:17` · `UC01:28` |
| **Người ký / in tên người ký** | Thiết lập người ký (Thông tin công ty) + thiết lập chung | `FB:9` · `UC01:18` · `UC01:28` · `UC02:23` |
| **Ba quy tắc in** chứng từ chưa ghi sổ / đã khóa sổ / cộng gộp mặt hàng | thiết lập chung + **BR51.5** | `FB:9` · `FB:26` · `UC01:28` · `UC02:23` · `UC02:39` |
| **Tooltip khi nút In bị disable** | BR7 của màn Cấu hình báo cáo chứng từ (epic `_20`) | `UC02:55` |
| **Mẫu in cố định theo quy định** (01-TT, 02-VT…) | ngoài epic — "không sửa được và vẫn in như cũ" | `FB:7` |
| **Hành vi chung của bản in chứng từ** (nút In, Xuất file) và màn xem trước bản in | ngoài epic | `UC02:25` · `SCR:326` |

Đối xứng đáng nhớ của epic này: **mẫu** dùng chung toàn đơn vị kế toán, mọi người dùng, mọi chi nhánh
(`FB:7`) — nhưng **quyền** thì "Tenant-scoped, **xét theo chi nhánh đang làm việc**" (`UC01:11`).
Đây là nguồn của `R-TLMI-035` và của khoảng trống `Z-28`.

---

## §4. Ghi chú vùng đóng băng — BẮT BUỘC đọc trước khi dùng bộ đặc tả này

### 4.1 — Tài liệu của phiếu yêu cầu này nằm trong `pmkt-docs/ba/Phase_2/**`

`CLAUDE.md` liệt kê `pmkt-docs/ba/Phase_2/**` là **vùng đóng băng**: chặn cứng ở
`.claude/settings.json` (`permissions.deny` cho `Read`) và ở hook `.claude/hooks/pmkt-gate.py` cho
`Grep` · `Glob` · `Edit` · `Write` · `Bash` và nhóm `mcp__idea__*`.

**Toàn bộ 11 file của `PMKT-E-14549_21_ThietLapMauInChungTu/` nằm trong vùng này** — không có bản
Phase 1 tương ứng. Đây **không phải** trường hợp "hai bản khác nội dung của cùng một epic" mà
`CLAUDE.md` mô tả; epic này **chỉ tồn tại ở bộ Phase 2**.

### 4.2 — Căn cứ đọc: yêu cầu trực tiếp của user

| | |
|---|---|
| Người yêu cầu | **Dat** (`aitool8@osp.vn`) |
| Ngày | **2026-09-19** |
| Hình thức | Yêu cầu trực tiếp trong phiên làm việc |
| Cách đọc | **Bản sao tải từ GitHub** (`ospgroupvn/pmkt-docs`) về **thư mục tạm của phiên**, ngoài repo |
| Đã chạm `pmkt-docs/` chưa | **KHÔNG.** Không file nào trong `pmkt-docs/` bị `Read`, `Grep`, `Edit` hay `Write` trong đợt soát này |
| Đã gỡ rule `deny` chưa | **KHÔNG.** `.claude/settings.json` và `.claude/settings.local.json` giữ nguyên; hook `pmkt-gate.py` giữ nguyên; biến `PMKT_ALLOW_PHASE2` **không** được đặt |

Đây là đúng **ngoại lệ duy nhất** mà `CLAUDE.md` cho phép: *"Chỉ đọc bản Phase 2 khi user yêu cầu
trực tiếp, và phải báo rõ đang chạm vùng đóng băng"*. Việc **báo rõ** chính là mục này.

### 4.3 — BR50 / BR51 là BR chung của bộ **Phase 2**, KHÔNG có trong Phase 1

Đây là điểm quan trọng nhất của §4.

| | Bản **Phase 1** (repo đang làm) | Bản **Phase 2** (nguồn của phiếu yêu cầu này) |
|---|---|---|
| Đường dẫn | `pmkt-docs/ba/Common/business_rules.md` | `pmkt-docs/ba/Phase_2/Common/business_rules.md` |
| Phạm vi BR | **BR1 … BR49** | **BR1 … BR51** |
| `./docs/rules/br.sh` đọc bản nào | **chỉ bản Phase 1** (cố ý) | không đọc |
| Có `BR50. Chi nhánh` không | **KHÔNG** | **CÓ** |
| Có `BR51. Tùy chỉnh và in báo cáo` không | **KHÔNG** | **CÓ** |

Ba mục BR chung mà `SCR_ThietLapMauIn.md` viện dẫn — **BR50.7 Hồ sơ đơn vị** (`SCR:267`),
**BR51.5 Chứng từ** (`SCR:257`, `:298`, `:334`, `:374`), **BR51.6 Khóa cột và khóa tham số của báo
cáo** (`SCR:260`) — **đều nằm ngoài BR1…BR49**.

Hệ quả bắt buộc nhớ:

1. **`./docs/rules/br.sh 50` và `br.sh 51` sẽ KHÔNG trả về gì** — `br.sh` cố ý chỉ đọc bản Phase 1.
   Đừng kết luận "BR không tồn tại"; nó tồn tại ở bộ Phase 2.
2. Mọi luật trong `02-rules.md` ghi `BR2P BR50.7` / `BR2P BR51.5` / `BR2P BR51.6` ở dòng **Nguồn** hoặc
   **Ghi chú** đều đang dựa trên **BR chung của bộ Phase 2**. Danh sách các luật đó:
   `R-TLMI-001` · `R-TLMI-004` · `R-TLMI-005` · `R-TLMI-014` · `R-TLMI-023` · `R-TLMI-035` ·
   `R-TLMI-036` · `R-TLMI-039` · `R-TLMI-046` (⛔ C04) · `R-TLMI-047` · `R-TLMI-058` · `R-TLMI-078` ·
   `R-TLMI-082` (⛔ C03) · `R-TLMI-090` · `R-TLMI-092` · `R-TLMI-119` (⛔ C01) · `R-TLMI-165` ·
   `R-TLMI-182` · `R-TLMI-197` · `R-TLMI-199` (⛔ C05) · `R-TLMI-261` · `R-TLMI-266` (⛔ C01) ·
   `R-TLMI-267`, cộng ba bất biến `INV-TLMI-001` · `INV-TLMI-005` · `INV-TLMI-011`.
3. **Ba trong bảy mâu thuẫn OPEN (C01, C03, C04) có một bên là BR chung Phase 2.** Quy tắc "epic thắng
   trong đúng phạm vi epic, và phải báo rõ đang lệch BR nào" (`CLAUDE.md` §BR mục 3) **không tự áp
   được ở đây**, vì bản thân việc bộ BR Phase 2 có hiệu lực hay chưa cũng là câu hỏi cho BA. Cả ba
   để `OPEN`.
4. Nếu sau này repo chuyển sang Phase 1 cho chính chức năng này, **phải soát lại toàn bộ** — bản
   Phase 1 không có BR50/BR51 thì các luật ở mục 2 mất nền.

### 4.4 — Khi cần đọc lại tài liệu nguồn

Thư mục tạm của phiên **không tồn tại ở phiên sau**. Muốn đọc lại:

1. Xin user xác nhận lại (vẫn là vùng đóng băng, vẫn cần yêu cầu trực tiếp).
2. Tải lại từ GitHub về thư mục tạm, **không** đọc thẳng `pmkt-docs/`.
3. Chạy `git hash-object` trên bản mới, so với cột **Blob SHA** ở §1. Lệch ⇒ tài liệu đã đổi ⇒
   mọi luật trích từ file đó phải soát lại.
4. Nếu buộc phải đọc thẳng trong repo: đặt `PMKT_ALLOW_PHASE2=1` (hook chuyển từ chặn sang cảnh báo)
   **và** gỡ thủ công dòng `deny` cho `Read` — cả hai đều **phải xin phép user trước**, và **phải
   khôi phục sau khi xong**.

---

## §5. Bảng chủ đề → nguồn

Mỗi **chủ đề nghiệp vụ** một nhóm dòng, liệt kê mọi nơi nói về nó — để thấy ngay chỗ nào có nhiều
nguồn và chỗ nào chỉ có một.

| Chủ đề | Nguồn | Bậc | Kết luận |
|---|---|---|---|
| **Phạm vi mẫu** — một mẫu / cặp (loại chứng từ, nghiệp vụ) | `SCR:3` · `SCR:244-247` | 4 | **chốt** → `R-TLMI-001`…`005` |
| | `FB:7` · `CRUD:17` | 2 / 3 | khớp |
| | `BR2P` BR51.5 | 5 | khớp — "một mẫu cho cả đơn vị" |
| **Chưa có bản ghi = dùng mẫu chuẩn** | `SCR:247` · `SCR:328` | 4 | **chốt** → `R-TLMI-007`, `INV-TLMI-002` |
| | `CRUD:15` | 3 | khớp — "không có entity riêng" |
| | `UC02:48-51` · `MSG:16` | 3 / 5 | khớp |
| **Điều kiện xóa bản ghi khi Lưu** | `SCR:318` "đúng bằng mẫu chuẩn" | 4 | lệch → **C02** |
| | `UC01:54` "(sau Đặt lại)" · `UC01:33` · `CRUD:17` | 3 | lệch → **C02** |
| | `AD01:30` "bằng mẫu chuẩn?" | 1 | AD **nói ngược**, không phải giản lược → **C02** |
| **Kế thừa theo chung / riêng** | `SCR:252` · `SCR:253` · `SCR:256` · `SCR:318` · `SCR:331` | 4 | **chốt** → `R-TLMI-036`…`045`, `INV-TLMI-003` |
| | `UC01:28` · `UC02:23` · `FB:18` · `FB:26` | 2 / 3 | khớp |
| | `BR2P` BR51.5 "đổi theo khi thiết lập chung đổi" | 5 | khớp |
| | `MT:103` "không có nhãn riêng cho từng ô" | 3 | bổ sung → `R-TLMI-045`, `Z-25` |
| **Người ký — tiêu đề in ra** | `SCR:257` "luôn theo thiết lập chung (tiêu đề, tên, cờ in tên)" | 4 | lệch → **C04** |
| | `SCR:295` "tiêu đề in ra **sửa được riêng cho mẫu**" | 4 | lệch → **C04** (mâu thuẫn **trong cùng file**) |
| | `SCR:199` khai `TieuDe` Cho phép sửa = Y · `MT:89` = Show | 4 / 3 | đứng về phía `SCR:295` |
| | `BR2P` BR51.5 "người ký … luôn lấy từ thiết lập chung" | 5 | đứng về phía `SCR:257` |
| **Người ký — đọc hồ sơ chi nhánh nào** | `SCR:295-298` | 4 | **IM LẶNG** → **C05** |
| | `TTC:46-50` · `TTC:60` (cột nằm trên `cfg_chi_nhanh`) | 4 | cho thấy giá trị **đổi theo chi nhánh** |
| | `BR2P` BR50.7 · `UC01:49` · `UC02:41` | 5 / 3 | gợi ý "chi nhánh ghi trên chứng từ", nhưng **không nói cho khối Chữ ký** |
| **Logo — mẫu sửa riêng được không** | `SCR:125` khai `InLogo` · `SCR:267` · `MT:77` | 4 / 3 | lệch → **C03** |
| | `BR2P` BR51.5 "dòng thông tin đơn vị" (logo không phải "dòng") | 5 | lệch → **C03** |
| **Cộng gộp mặt hàng — khóa gộp** | `BR2P` BR51.5 — mã hàng, đơn vị tính, đơn giá (+ lô, HSD) | 5 | lệch → **C01** |
| | `S20:160-162` — thêm **cùng thuế suất**, có ví dụ phủ định | 4 | lệch → **C01** |
| | `SCR:281` · `SCR:334` — chỉ nói "áp trước khi dựng bảng", **không nhắc phạm vi 3 loại chứng từ** | 4 | bổ sung cảnh báo `Z-29` |
| **Thông tin đầu trang — nguồn nội dung** | `SCR:267` "chi nhánh ghi trên chứng từ" · `SCR:131` | 4 | **chốt** → `R-TLMI-078`, `R-TLMI-081` |
| | `BR2P` BR50.7 | 5 | khớp, là luật nền |
| | `S20:126-128` (nội dung từng dòng, thứ tự, bỏ dòng trống) | 4 | bổ sung → `R-TLMI-079`, `R-TLMI-083` |
| **Hướng giấy Tự động — chứng từ** | `SCR:255` (không tính cột STT; không có bảng ⇒ dọc) | 4 | **chốt** → `R-TLMI-058`, `R-TLMI-059` |
| | `BR2P` BR51.5 (im lặng hai chi tiết trên) | 5 | epic **chi tiết hóa**, không trái BR |
| | `S20:180` — **báo cáo** xét "số cột đang hiển thị" | 4 | **gốc so sánh khác** — đừng dùng chung code |
| **Thuật toán chia đều 100 %** | `SCR:279` (công thức + 3 ví dụ) · `SCR:233` · `SCR:167` | 4 | **chốt** → `R-TLMI-114`, `INV-TLMI-005` |
| | `UC01:26` "nút chia lại về 100 % theo tỷ lệ" | 3 | khớp |
| **Khối tự do — lưới, gộp/tách ô** | `SCR:283-292` · `SCR:79` · `SCR:81` · `SCR:187` · `SCR:222-231` | 4 | **chốt** → nhóm I (62 luật) |
| | `UC01:25` · `FB:15` | 2 / 3 | khớp |
| | `MT:68-70` · `MT:102` | 3 | bổ sung trạng thái Show/Hide/Disable |
| | `FIGMA` frame 3 | 1 | khớp nhãn nút và menu |
| **Tên hiển thị + In đậm là thuộc tính của trường** | `SCR:289` | 4 | **chốt** → `R-TLMI-156`, `INV-TLMI-009` |
| | `UC01:25` · `FB:15` | 2 / 3 | khớp |
| | `SCR:227` (nút trên thanh công cụ áp theo **vùng ô**) | 4 | va nhau ở vùng chọn hỗn hợp → `Z-18` |
| **Sửa tên khối tự do ở đâu** | `SCR:53` · `SCR:59` · `SCR:177` · `SCR:345` · `MT:86` | 4 / 3 | lệch → **C07** (bốn nguồn nói có ô Tên khối) |
| | `SCR:284` · `UC01:24` | 4 / 3 | lệch → **C07** (chỉ mô tả hộp Đặt tên lúc thêm) |
| **Ghi đè đồng thời** | `SCR:247` · `SCR:318` · `UC01:54` · `CRUD:17` · `MSG` | — | **IM LẶNG hoàn toàn** → **C06** |
| **Validation** | `SCR:338-356` (17 dòng) | 4 | **chốt** → `R-TLMI-239` |
| | `SCR:314-315` (BR10 — ba điều "không phải lỗi") | 4 | bổ sung → `R-TLMI-111`, `R-TLMI-235`, `R-TLMI-236` |
| | `UC01:53` · `UC01:65-68` | 3 | khớp |
| | `MT:109` "không đổi Show/Hide/Disable" | 3 | khớp |
| **Quyền** | `SCR:9-10` · `SCR:322` · `SCR:356` | 4 | **chốt** → `R-TLMI-031`…`035` |
| | `UC01:11-12` · `UC01:43` · `UC01:60-63` · `UC02:11` | 3 | khớp |
| | `MT:29` · `MT:57-59` | 3 | khớp — `Hide`, không phải disable |
| | `AD02:26-27` dùng `MSG_002` cho nhánh thiếu quyền **In** | 1 | **AD tự mở rộng** → `Z-02` |
| **Lối vào & menu In** | `SCR:324-328` | 4 | **chốt** → `R-TLMI-023`…`030` |
| | `UC02:21-25` · `UC01:22` · `UC01:42` | 3 | khớp |
| | `BR2P` BR51.5 (menu In có Mẫu tùy chỉnh + Thiết lập mẫu in…) | 5 | khớp |
| | `FIGMA` frame 0 | 1 | khớp |

---

## §6. UC → luật

Mọi UC trong `4.usecases/` phải sinh ra ít nhất một luật; UC không sinh luật nào = đã bỏ sót.

| UC | Nội dung | Luật sinh ra | Nhận xét |
|---|---|---|---|
| **UC01** `PMKT-U-14549_21-01` Thiết lập mẫu in | Dựng mẫu in cho một nghiệp vụ ngay trên form chứng từ | `R-TLMI-008`…`010` · `014` · `022` · `025` · `028`…`029` · `031`…`034` · `036`…`040` · `046`…`047` · `053` · `055` · `069` · `076`…`077` · `085` · `092`…`093` · `102`…`104` · `108` · `114` · `120`…`125` · `129`…`130` · `136` · `143` · `149`…`150` · `152` · `156`…`158` · `165`…`166` · `170` · `175`…`176` · `178` · `182`…`184` · `189` · `193`…`195` · `197` · `201` · `205`…`206` · `210` · `213`…`214` · `217`…`223` · `225` · `227` · `229`…`232` · `236` · `240`…`244` · `246`…`255` | 7 AC (`:22`-`:34`) + 6 luồng phụ (NL1-NL6) đều đã sinh luật |
| **UC02** `PMKT-U-14549_21-02` In chứng từ bằng mẫu tùy chỉnh | Chọn Mẫu tùy chỉnh trong menu In; fallback mẫu chuẩn | `R-TLMI-007` · `013` · `023` · `026`…`027` · `033` · `039` · `046`…`047` · `143` · `178` · `259`…`271` | 5 AC (`:21`-`:25`) + 3 luồng phụ (NL1-NL3) đều đã sinh luật |

`2.usecase.puml` (18 dòng) là sơ đồ tổng quan hai UC, bậc 1 — **không sinh luật riêng**, chỉ xác nhận
epic có đúng hai UC.

---

## §7. BR chung đã đối chiếu

| BR | Bộ | Nội dung dùng đến | Áp ở luật nào | Epic có lệch không |
|---|---|---|---|---|
| **BR50.7** Hồ sơ đơn vị | **Phase 2** | Thông tin in trên chứng từ lấy từ hồ sơ của **chi nhánh ghi trên chính bản ghi đó**; mọi nơi đi `ChiNhanhId` → `cfg_chi_nhanh`, không đi ngược lên đơn vị cha; mỗi chi nhánh có MST riêng | `R-TLMI-078` · `R-TLMI-165` · `R-TLMI-267` | **Không lệch.** Ngoại lệ có chủ ý: **ảnh logo** ở `cfg_tenant.Logo`, chi nhánh không có logo riêng (`TTC:129`) ⇒ bản in của chi nhánh B mang logo pháp nhân. Tài liệu ghi rõ, không phải bug |
| **BR51.5** Chứng từ | **Phase 2** | Mẫu áp Đầu trang / Chữ ký / Giấy và chữ của thiết lập chung làm mặc định; hướng Tự động của chứng từ; ba quy tắc in chứng từ; menu In có Mẫu tùy chỉnh + Thiết lập mẫu in…; nút Sửa mẫu; một mẫu cho cả đơn vị; ô chưa sửa đổi theo thiết lập chung; **ngày ký trên chứng từ luôn là ngày chứng từ** | `R-TLMI-001` · `005` · `023` · `036` · `039` · `046` · `047` · `058` · `090` · `119` · `197` · `261` · `266` | **LỆCH / CHI TIẾT HÓA — 3 chỗ:** ① khóa cộng gộp (có "thuế suất" hay không) → **C01 OPEN**; ② Logo có thuộc "dòng thông tin đơn vị" không → **C03 OPEN**; ③ "tiêu đề in ra" của người ký → **C04 OPEN**. Một chỗ **chi tiết hóa, không trái**: `SCR:255` bổ sung "không tính cột STT" và "không có bảng nào bật ⇒ in dọc" cho hướng Tự động |
| **BR51.6** Khóa cột và khóa tham số của báo cáo | **Phase 2** | Khóa kỹ thuật duy nhất trong phạm vi, không đổi suốt vòng đời, không dùng lại khóa của cột đã bỏ | `R-TLMI-092` | **Mượn nguyên tắc, không áp nguyên văn.** `SCR:260` viết "**như** BR51.6"; nguyên văn BR51.6 chỉ nói về cột và tham số **báo cáo** (`cfg_bao_cao_tuy_chinh_cot.MaCot`, `cfg_bao_cao_tuy_chinh_tham_so.MaThamSo`), trong khi bảng của màn này là `cfg_mau_in_khoi_cot` / `cfg_mau_in_khoi_o`. Ghi nhận, không nâng thành mâu thuẫn |
| **BR50.6** Phạm vi dữ liệu theo chi nhánh | **Phase 2** | Bảng phân nhóm entity: nhóm nào lọc `ChiNhanhId`, nhóm nào không | `R-TLMI-004` · `INV-TLMI-011` (đối chiếu) | **Khoảng trống của BR chung:** bảng BR50.6 **không liệt kê `cfg_mau_in_chung_tu`** ở nhóm nào. `SCR:247` nói rõ khóa không có `ChiNhanhId` ⇒ theo tinh thần thuộc nhóm "Cấu hình hệ thống". Ghi nhận để BA bổ sung vào bảng BR50.6; **không chặn code** vì `SCR:247` đã đủ dứt khoát |
| **BR50.2** Phạm vi quyền theo chi nhánh | **Phase 2** | Quyền xét theo chi nhánh đang làm việc | `R-TLMI-031` · `R-TLMI-035` | **Không lệch**, nhưng tạo bất đối xứng mẫu-chung / quyền-theo-chi-nhánh ⇒ khoảng trống `Z-28` |
| **BR1 … BR49** | **Phase 1** | — | — | **KHÔNG áp dụng.** Tài liệu của phiếu yêu cầu này **không viện dẫn BR nào trong BR1…BR49**. `br.sh` (chỉ đọc bản Phase 1) không dùng được cho epic này |

⚠ Nhắc lại từ §4.3: **BR50 và BR51 chỉ tồn tại ở bộ Phase 2.** Mọi dòng "BR chung" trong bảng này
phụ thuộc vào việc bộ Phase 2 có hiệu lực hay không — chính câu hỏi đó cũng cần BA xác nhận.

---

*Hết `00-source-map.md`. Hai file `01-conflict.md` và `03-scenarios.md` của bộ đặc tả này do người
khác lập — không sửa hai file đó từ đây.*
