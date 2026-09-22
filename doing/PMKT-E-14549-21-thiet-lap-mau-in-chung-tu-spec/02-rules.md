# PMKT-E-14549_21 Thiết lập mẫu in chứng từ — Luật & bất biến

| | |
|---|---|
| Phiếu yêu cầu | `pmkt-docs/ba/Phase_2/PMKT-E-14549_21_ThietLapMauInChungTu/` |
| Mã viết tắt | **TLMI** |
| Ngày soát | **2026-09-19** |
| Bản tài liệu | blob SHA từng file — xem `00-source-map.md` §1 (bản sao tải từ GitHub `ospgroupvn/pmkt-docs`, 2026-09-19) |
| Trạng thái | **ĐÃ CHỐT** · 271 luật · 12 bất biến · **0 luật bị chặn** — mọi luật code được |
| Cổng mâu thuẫn | `01-conflict.md` còn **0 mục `OPEN`**: 32 mục chuyển `CLOSED-BA (Dat · 2026-09-19)`, 4 mục `CLOSED-AUTO` |
| Căn cứ chốt | [`04-quyet-dinh-ban-giao.md`](04-quyet-dinh-ban-giao.md) — uỷ quyền trực tiếp của user (Dat) ngày 2026-09-19 |

> ✅ **Cổng đặc tả đã mở.** `01-conflict.md` không còn mục `OPEN` nào ⇒ **không luật nào trong file
> này bị cấm code**, `trace.sh` không còn lý do in `VI-PHAM` vì trạng thái *CHỜ*.
>
> Chín luật từng bị chặn — `R-TLMI-021` · `046` · `082` · `119` · `127` · `188` · `199` · `258` ·
> `266` — nay đã có `WHEN`/`THEN` dứt khoát, mang dòng `Chốt` trỏ về mục `C` tương ứng, và **vẫn
> giữ nguyên phần giải thích hai cách hiểu** kèm lý do chọn. Đọc phần đó trước khi code: nó nói rõ
> hành vi nào **khác đi** so với cách hiểu bị loại.
>
> ⚠ **Đây là quyết định của phía triển khai, không phải của BA.** Mọi mục dưới đây đều là chỗ tài
> liệu im lặng hoặc tự mâu thuẫn. **BA vẫn cần soát lại** — chỗ nào BA chốt khác thì sửa
> `04-quyet-dinh-ban-giao.md` trước, rồi mới sửa file này, rồi mới sửa code.

> ⚠ **Vùng đóng băng.** Tài liệu nguồn nằm trong `pmkt-docs/ba/Phase_2/**`. Đọc theo **yêu cầu trực
> tiếp của user (Dat, 2026-09-19)** qua bản sao tải về thư mục tạm — xem `00-source-map.md` §4.
> **BR50 / BR51 là BR chung của bộ Phase 2, KHÔNG có trong bản Phase 1 (BR1…BR49)** mà repo đang dùng.

> ⚠ **`BR1…BR13` và `BR6b` nhắc trong file này là BR NỘI BỘ MÀN**, định nghĩa ngay trong
> `SCR_ThietLapMauIn.md:244–334` — **không** phải BR chung của `business_rules.md`.

## Quy ước nguồn (viết tắt dùng suốt file)

| Mã | File thật (đường dẫn đầy đủ trong repo tài liệu) |
|---|---|
| `SCR` | `pmkt-docs/ba/Phase_2/PMKT-E-14549_21_ThietLapMauInChungTu/5.screens/SCR_ThietLapMauIn.md` |
| `MSG` | `…/PMKT-E-14549_21_ThietLapMauInChungTu/6.messages.md` |
| `UC01` | `…/4.usecases/PMKT-U-14549_21-01_ThietLapMauIn/UC_ThietLapMauIn.md` |
| `AD01` | `…/4.usecases/PMKT-U-14549_21-01_ThietLapMauIn/AD_ThietLapMauIn.puml` |
| `UC02` | `…/4.usecases/PMKT-U-14549_21-02_InMauTuyChinh/UC_InChungTuMauTuyChinh.md` |
| `AD02` | `…/4.usecases/PMKT-U-14549_21-02_InMauTuyChinh/AD_InChungTuMauTuyChinh.puml` |
| `FB` | `…/PMKT-E-14549_21_ThietLapMauInChungTu/1.function-breakdown.md` |
| `CRUD` | `…/PMKT-E-14549_21_ThietLapMauInChungTu/3.crud-matrix.md` |
| `MT` | `…/Matrix/PMKT-E-14549_21_ThietLapMauInChungTu/SCR_ThietLapMauIn_MaTranAnHien.md` |
| `SC` | `…/Matrix/PMKT-E-14549_21_ThietLapMauInChungTu/_scope.md` |
| `S20` | `pmkt-docs/ba/Phase_2/PMKT-E-14549_20_CauHinhBaoCaoChungTu/5.screens/SCR_CauHinhBaoCaoChungTu.md` |
| `M20` | `pmkt-docs/ba/Phase_2/PMKT-E-14549_20_CauHinhBaoCaoChungTu/6.messages.md` |
| `TTC` | `pmkt-docs/ba/Phase_2/PMKT-E-14549_CauHinhBanDau/5.screens/SCR_CauHinhChiTiet/SCR_CauHinhChiTiet_ThongTinCongTy.md` |
| `BR2P` | `pmkt-docs/ba/Phase_2/Common/business_rules.md` — **BR50**, **BR51** (bộ Phase 2) |
| `FIGMA` | Figma file `ymMyg329ejsgCWg28CNmGl`, section node `71956-288871` (8 frame) |

Ký hiệu `SCR:267` = file `SCR`, đúng dòng 267.

## Đọc file này thế nào

- Trạng thái luật chỉ có ba: `CHỐT` · `CHỜ C<nn>` · `HUỶ`. **Hiện cả 271 luật đều `CHỐT`** — không
  còn luật nào ở trạng thái `CHỜ`, không luật nào bị cấm code.
- Luật mang dòng `Chốt   C<nn> · 04-quyet-dinh-ban-giao.md … · Dat · 2026-09-19` là luật từng bị
  tranh chấp. Phần `Ghi chú` của nó **giữ lại cả hai cách hiểu** cùng lý do chọn — đọc kỹ, vì nó nêu
  chính xác hành vi nào khác đi so với cách hiểu bị loại. Sáu luật ghi `(A) ĐÃ CHỌN` / `(B) KHÔNG
  CHỌN`; `R-TLMI-127` chọn **cả hai nhánh**.
- Dòng `Tầng — vì sao FE` chỉ có ở bảy luật bố cục pixel (`R-TLMI-180` · `181` · `194` · `195` ·
  `200` · `263` · `265`). Chúng là **FE** vì giai đoạn 1 FE dựng bản in; khi BE sinh PDF thì phải
  xem lại cả bảy một lượt.
- Mọi text hiển thị trong file này là **nguyên văn tiếng Việt của BA** — chép thẳng vào `vi.ts`,
  cấm diễn đạt lại (luật 2 của `CLAUDE.md`).
- Bố cục nhóm: **A** phạm vi & vòng đời · **B** lối vào & quyền · **C** kế thừa thiết lập chung ·
  **D** giấy và chữ · **E** riêng của mẫu · **F** khối Thông tin đầu trang · **G** khối Tiêu đề ·
  **H** khối Bảng · **I** khối tự do · **K** khối Chữ ký · **L** bố cục mẫu · **M** xem trước ·
  **N** kiểm tra & trạng thái · **P** dựng bản in.

---

## Bảng tổng

### Nhóm A — Phạm vi & vòng đời mẫu (R-TLMI-001…022)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-001 | Một mẫu tùy chỉnh cho mỗi cặp (loại chứng từ, nghiệp vụ) của một đơn vị kế toán | BE | P0 | CHỐT |
| R-TLMI-002 | "Nghiệp vụ" = giá trị ô Loại nghiệp vụ trên form, do epic nghiệp vụ định nghĩa | CẢ HAI | P0 | CHỐT |
| R-TLMI-003 | Loại chứng từ không chia nghiệp vụ thì cả loại chứng từ là một mẫu | CẢ HAI | P0 | CHỐT |
| R-TLMI-004 | Khóa duy nhất của mẫu = (TenantId, MaChucNang, MaNghiepVu) | BE | P0 | CHỐT |
| R-TLMI-005 | Mẫu dùng chung mọi người dùng và mọi chi nhánh | BE | P0 | CHỐT |
| R-TLMI-006 | Mỗi cặp có đúng một mẫu chuẩn hệ thống, sinh từ đặc tả form, không có entity riêng | BE | P0 | CHỐT |
| R-TLMI-007 | Chưa có bản ghi mẫu = nghiệp vụ đang dùng mẫu chuẩn hệ thống | CẢ HAI | P0 | CHỐT |
| R-TLMI-008 | Mẫu chuẩn có đúng bốn loại khối theo thứ tự cố định, không khối nào khác | CẢ HAI | P0 | CHỐT |
| R-TLMI-009 | Form có n lưới thì mẫu chuẩn có n khối Bảng, đủ cột gốc, mọi lưới bật | CẢ HAI | P0 | CHỐT |
| R-TLMI-010 | Thông tin chung / tổng tiền phải tự dựng bằng khối tự do | CẢ HAI | P1 | CHỐT |
| R-TLMI-011 | Mở màn từ một chứng từ thì mở đúng mẫu của nghiệp vụ chứng từ đó | CẢ HAI | P0 | CHỐT |
| R-TLMI-012 | Đổi Loại nghiệp vụ trên form rồi mở lại thì mở một mẫu khác | CẢ HAI | P0 | CHỐT |
| R-TLMI-013 | Mẫu in cố định theo quy định (01-TT, 02-VT…) không sửa được, vẫn in như cũ | CẢ HAI | P0 | CHỐT |
| R-TLMI-014 | Nghiệp vụ nào có chức năng này và mã quyền là gì do epic nghiệp vụ khai báo | CẢ HAI | P1 | CHỐT |
| R-TLMI-015 | Bấm Đặt lại mẫu chuẩn thì hỏi trước | FE | P1 | CHỐT |
| R-TLMI-016 | Xác nhận Đặt lại thì nạp lại toàn bộ mẫu chuẩn hệ thống | FE | P1 | CHỐT |
| R-TLMI-017 | Đặt lại xong thì báo và chuyển nhãn trạng thái Chưa lưu | FE | P1 | CHỐT |
| R-TLMI-018 | Đặt lại chỉ đổi trên màn, bấm Lưu mới có hiệu lực | CẢ HAI | P0 | CHỐT |
| R-TLMI-019 | Đặt lại mà chưa Lưu rồi Đóng › Không lưu thì mẫu cũ còn nguyên | CẢ HAI | P0 | CHỐT |
| R-TLMI-020 | Không đồng ý hộp xác nhận Đặt lại thì giữ nguyên mẫu đang chỉnh | FE | P1 | CHỐT |
| R-TLMI-021 | Lưu khi mẫu **bằng nội dung** mẫu chuẩn thì xóa bản ghi cùng các nhánh con | BE | P0 | CHỐT (C02) |
| R-TLMI-022 | Lưu thành công thì mọi lần in Mẫu tùy chỉnh sau đó dùng mẫu mới ngay | BE | P1 | CHỐT |

### Nhóm B — Lối vào & quyền (R-TLMI-023…035)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-023 | Menu In: mẫu cố định → đường kẻ → Mẫu tùy chỉnh → Thiết lập mẫu in… | FE | P1 | CHỐT |
| R-TLMI-024 | Hai mục menu dùng đúng tên "Mẫu tùy chỉnh" và "Thiết lập mẫu in…" cho mọi nghiệp vụ | FE | P1 | CHỐT |
| R-TLMI-025 | Form thêm mới không có nút In; menu In chỉ có ở form sửa và form xem chi tiết | CẢ HAI | P1 | CHỐT |
| R-TLMI-026 | Nghiệp vụ có In từ danh sách thì menu In cũng xuất hiện trên màn danh sách | FE | P1 | CHỐT |
| R-TLMI-027 | Màn xem trước bản in có thêm nút Sửa mẫu | FE | P1 | CHỐT |
| R-TLMI-028 | Hai lối vào cho cùng một màn và cùng một mẫu | CẢ HAI | P0 | CHỐT |
| R-TLMI-029 | Đóng màn thì quay lại đúng nơi vừa mở ra | FE | P1 | CHỐT |
| R-TLMI-030 | Quay lại màn xem trước sau khi lưu thì bản in vẽ lại theo mẫu vừa lưu | FE | P1 | CHỐT |
| R-TLMI-031 | Quyền Thiết lập mẫu in xét theo nghiệp vụ tại chi nhánh đang làm việc | CẢ HAI | P0 | CHỐT |
| R-TLMI-032 | Không có quyền thì mục menu và nút Sửa mẫu **ẩn hẳn**, không phải disable | FE | P0 | CHỐT |
| R-TLMI-033 | Không có quyền Thiết lập mẫu in nhưng có quyền In thì vẫn in được Mẫu tùy chỉnh | CẢ HAI | P0 | CHỐT |
| R-TLMI-034 | Gọi thẳng API mà không có quyền thì server chặn | BE | P0 | CHỐT |
| R-TLMI-035 | Có quyền ở một chi nhánh là sửa được mẫu dùng chung cho mọi chi nhánh | BE | P0 | CHỐT |

### Nhóm C — Kế thừa thiết lập chung (R-TLMI-036…052)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-036 | Mỗi ô Giấy và chữ và mỗi ô trong bảy ô tick đầu trang có hai trạng thái theo chung / riêng | CẢ HAI | P0 | CHỐT |
| R-TLMI-037 | Ô theo chung ghi **trống (NULL)** khi Lưu, tuyệt đối không copy giá trị đang hiển thị | BE | P0 | CHỐT |
| R-TLMI-038 | Ô theo chung đọc lại thiết lập chung tại thời điểm in và thời điểm vẽ xem trước | BE | P0 | CHỐT |
| R-TLMI-039 | Ô riêng giữ giá trị của mẫu, thiết lập chung đổi không ảnh hưởng | BE | P0 | CHỐT |
| R-TLMI-040 | Nút Theo thiết lập chung của nhóm Giấy và chữ đưa cả nhóm về theo chung | FE | P1 | CHỐT |
| R-TLMI-041 | Bấm nút Theo thiết lập chung là một bước Hoàn tác được | FE | P2 | CHỐT |
| R-TLMI-042 | Không có cách đưa riêng một ô về theo chung | FE | P1 | CHỐT |
| R-TLMI-043 | Nút Theo thiết lập chung của khối Thông tin đầu trang đưa cả bảy ô tick về theo chung | FE | P1 | CHỐT |
| R-TLMI-044 | Đổi Khổ giấy / Hướng giấy trên thanh Xem trước làm ô đó trở thành **riêng** | CẢ HAI | P0 | CHỐT |
| R-TLMI-045 | Trạng thái theo chung / riêng không có nhãn riêng từng ô, không đổi Show/Hide | FE | P1 | CHỐT |
| R-TLMI-046 | Người ký luôn theo thiết lập chung, TRỪ **tiêu đề in ra** (mẫu sửa riêng được) | CẢ HAI | P1 | CHỐT (C04) |
| R-TLMI-047 | Ba quy tắc in chứng từ luôn theo thiết lập chung, màn này không có ô chỉnh | CẢ HAI | P1 | CHỐT |
| R-TLMI-048 | Mục "Bố cục mặc định của báo cáo" của thiết lập chung KHÔNG áp cho chứng từ | CẢ HAI | P1 | CHỐT |
| R-TLMI-049 | Định dạng khối đầu trang (kiểu chữ, in hoa, cỡ logo, căn lề, lặp trang sau) luôn theo thiết lập chung | CẢ HAI | P1 | CHỐT |
| R-TLMI-050 | Liên kết Mở Cấu hình báo cáo chứng từ (tab Quy tắc in chung) | FE | P2 | CHỐT |
| R-TLMI-051 | Liên kết Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in | FE | P2 | CHỐT |
| R-TLMI-052 | Liên kết Mở Thiết lập người ký | FE | P2 | CHỐT |

### Nhóm D — Giấy và chữ (R-TLMI-053…063)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-053 | Nhóm Giấy và chữ luôn hiện đủ sáu ô kèm giá trị đang dùng | FE | P1 | CHỐT |
| R-TLMI-054 | Khổ giấy chỉ nhận A3 / A4 / A5 | CẢ HAI | P1 | CHỐT |
| R-TLMI-055 | Hướng giấy chỉ nhận Dọc / Ngang / Tự động | CẢ HAI | P1 | CHỐT |
| R-TLMI-056 | Hướng giấy = Tự động thì ô Số cột để tự động in ngang mới hiện và mới bắt buộc | CẢ HAI | P1 | CHỐT |
| R-TLMI-057 | Số cột để tự động in ngang là số nguyên 1–50 | CẢ HAI | P1 | CHỐT |
| R-TLMI-058 | Hướng Tự động với chứng từ: xét khối Bảng đang bật có nhiều cột in nhất | CẢ HAI | P1 | CHỐT |
| R-TLMI-059 | Hướng Tự động mà không có khối Bảng nào đang bật thì in dọc | CẢ HAI | P1 | CHỐT |
| R-TLMI-060 | Hướng Dọc hoặc Ngang thì in đúng hướng đó bất kể số cột | CẢ HAI | P1 | CHỐT |
| R-TLMI-061 | Căn lề bốn phía là số 0–5 cm, tối đa một chữ số lẻ | CẢ HAI | P1 | CHỐT |
| R-TLMI-062 | Font chữ chỉ nhận Times New Roman hoặc Arial | CẢ HAI | P1 | CHỐT |
| R-TLMI-063 | Cỡ chữ là số nguyên 8–20, chỉ chặn phía máy chủ | BE | P1 | CHỐT |

### Nhóm E — Riêng của mẫu (R-TLMI-064…075)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-064 | Màu chữ là giá trị riêng của mẫu, mặc định `#000000`, không kế thừa thiết lập chung | CẢ HAI | P1 | CHỐT |
| R-TLMI-065 | Màu chữ áp cho toàn bộ chữ và đường kẻ của bản in, trừ logo | CẢ HAI | P1 | CHỐT |
| R-TLMI-066 | Chọn màu bằng 10 ô màu hoặc gõ mã dạng `#rrggbb` | CẢ HAI | P1 | CHỐT |
| R-TLMI-067 | Kiểu hình nền = Không (mặc định) thì không in hình nền | CẢ HAI | P2 | CHỐT |
| R-TLMI-068 | Kiểu hình nền = Khung viền thì kẻ khung quanh mép trang theo màu chữ | CẢ HAI | P2 | CHỐT |
| R-TLMI-069 | Kiểu hình nền = Ảnh tải lên thì chọn tệp jpg/png ≤ 1MB | CẢ HAI | P1 | CHỐT |
| R-TLMI-070 | Kiểu hình nền ≠ Không thì ô Độ đậm mới hiện và mới bắt buộc | FE | P1 | CHỐT |
| R-TLMI-071 | Kiểu hình nền = Ảnh tải lên thì ô Căn ảnh và ô Ảnh mới hiện và mới bắt buộc | FE | P1 | CHỐT |
| R-TLMI-072 | Độ đậm 5–100 %, mặc định 20, áp cho cả Khung viền lẫn Ảnh tải lên | CẢ HAI | P1 | CHỐT |
| R-TLMI-073 | Căn ảnh = Giữa trang thì ảnh giữ tỷ lệ, chiếm khoảng nửa trang, nằm giữa | CẢ HAI | P2 | CHỐT |
| R-TLMI-074 | Căn ảnh = Toàn trang thì kéo giãn ảnh phủ kín phần giấy trong lề | CẢ HAI | P2 | CHỐT |
| R-TLMI-075 | Hình nền in dưới mọi khối và không ảnh hưởng vị trí khối | CẢ HAI | P1 | CHỐT |

### Nhóm F — Khối Thông tin đầu trang (R-TLMI-076…084)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-076 | Ô tick "In khối Thông tin đầu trang trên mẫu này" bật/tắt cả khối, mặc định Có | CẢ HAI | P1 | CHỐT |
| R-TLMI-077 | Bảy ô tick dòng in, mặc định theo thiết lập chung với mặc định hệ thống cho sẵn | CẢ HAI | P1 | CHỐT |
| R-TLMI-078 | Nội dung các dòng lấy từ hồ sơ đơn vị của **chi nhánh ghi trên chứng từ** | BE | P0 | CHỐT |
| R-TLMI-079 | Dòng đã tick nhưng hồ sơ để trống thì bỏ qua dòng, không in dòng trống | BE | P1 | CHỐT |
| R-TLMI-080 | Bỏ tick cả bảy dòng thì khối không in gì và đây không phải lỗi | CẢ HAI | P1 | CHỐT |
| R-TLMI-081 | Mỗi dòng tick hiển thị kèm giá trị thật của chi nhánh ghi trên chứng từ | FE | P1 | CHỐT |
| R-TLMI-082 | Logo **CÓ** là một trong bảy ô tick mà mẫu sửa riêng được | CẢ HAI | P1 | CHỐT (C03) |
| R-TLMI-083 | Thứ tự các dòng đầu trang cố định | BE | P2 | CHỐT |
| R-TLMI-084 | Thiết lập chung bật lặp đầu trang thì khối Thông tin đầu trang lặp lại ở trang sau | BE | P1 | CHỐT |

### Nhóm G — Khối Tiêu đề (R-TLMI-085…091)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-085 | Nội dung tiêu đề mặc định là tên loại chứng từ, không trống, tối đa 255 ký tự | CẢ HAI | P1 | CHỐT |
| R-TLMI-086 | Cỡ chữ tiêu đề là số nguyên 10–36, mặc định 18, độc lập với cỡ chữ chung | CẢ HAI | P1 | CHỐT |
| R-TLMI-087 | Căn của khối Tiêu đề áp cho cả dòng tiêu đề và dòng ngày tháng | CẢ HAI | P1 | CHỐT |
| R-TLMI-088 | IN HOA = Có thì in toàn chữ hoa, = Không thì in đúng như gõ | CẢ HAI | P1 | CHỐT |
| R-TLMI-089 | In đậm của khối Tiêu đề, mặc định Có | CẢ HAI | P2 | CHỐT |
| R-TLMI-090 | Dòng ngày tháng in ngay dưới tiêu đề, chữ nghiêng, lấy ngày chứng từ | CẢ HAI | P1 | CHỐT |
| R-TLMI-091 | Số chứng từ **không** thuộc khối Tiêu đề, muốn in phải đưa vào khối tự do | CẢ HAI | P1 | CHỐT |

### Nhóm H — Khối Bảng (R-TLMI-092…119)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-092 | Mỗi khối Bảng ứng đúng một lưới trên form, đúng và đủ cột của lưới đó | CẢ HAI | P1 | CHỐT |
| R-TLMI-093 | Cột thêm vào lưới ở phiên bản sau tự xuất hiện cuối bảng và mặc định in | CẢ HAI | P0 | CHỐT |
| R-TLMI-094 | Tên bảng trống thì không in tên bảng, có nội dung thì in một dòng đậm trên bảng | CẢ HAI | P2 | CHỐT |
| R-TLMI-095 | Tên bảng mặc định trống cho lưới đầu tiên, bằng tên lưới cho lưới khác | CẢ HAI | P2 | CHỐT |
| R-TLMI-096 | In cột STT = Có thì thêm cột đầu tiên đánh số 1, 2, 3… | CẢ HAI | P1 | CHỐT |
| R-TLMI-097 | Dòng Cộng = Có thì dòng cuối bảng in "Tổng:" và tổng các cột được tick Cộng | CẢ HAI | P1 | CHỐT |
| R-TLMI-098 | Dòng Cộng = Không thì không có dòng này và các cột tick Cộng không có tác dụng | CẢ HAI | P1 | CHỐT |
| R-TLMI-099 | Lặp tiêu đề mỗi trang khi bảng tràn trang | CẢ HAI | P1 | CHỐT |
| R-TLMI-100 | Kẻ ô Đầy đủ / Kẻ ngang | CẢ HAI | P2 | CHỐT |
| R-TLMI-101 | Tên cột dữ liệu lấy theo đặc tả form và chỉ đọc | CẢ HAI | P1 | CHỐT |
| R-TLMI-102 | Tên hiển thị của cột không trống, tối đa 100 ký tự, mặc định bằng Tên cột dữ liệu | CẢ HAI | P1 | CHỐT |
| R-TLMI-103 | Ô tick in của cột, mặc định Có; bỏ tick thì bỏ cột và các cột sau dịch sang trái | CẢ HAI | P1 | CHỐT |
| R-TLMI-104 | Khối Bảng đang bật phải giữ lại ít nhất một cột hiển thị | CẢ HAI | P1 | CHỐT |
| R-TLMI-105 | Căn của cột áp cho cả tiêu đề cột và dữ liệu; mặc định cột số Phải, còn lại Trái | CẢ HAI | P2 | CHỐT |
| R-TLMI-106 | Chỉ cột số mới có ô Cộng; cột chữ thì ô Cộng ẩn tĩnh | CẢ HAI | P1 | CHỐT |
| R-TLMI-107 | Cộng mặc định Có với cột tiền, Không với cột khác | CẢ HAI | P1 | CHỐT |
| R-TLMI-108 | Độ rộng cột là số nguyên 3–90, bắt buộc với cột đang tick in | CẢ HAI | P1 | CHỐT |
| R-TLMI-109 | Độ rộng mặc định lấy theo tỷ lệ độ rộng cột trên lưới form, quy về 100 | CẢ HAI | P1 | CHỐT |
| R-TLMI-110 | Tổng độ rộng khác 100 thì dòng tổng dưới lưới cột báo số hiện tại | FE | P2 | CHỐT |
| R-TLMI-111 | Lưu mà tổng độ rộng khác 100 thì hệ thống tự chia lại về 100, không phải lỗi | CẢ HAI | P1 | CHỐT |
| R-TLMI-112 | Cột bỏ tick in không tính vào tổng và giữ nguyên số đang có | CẢ HAI | P1 | CHỐT |
| R-TLMI-113 | Tick lại một cột đang có độ rộng trống thì cột nhận phần chia của nút Chia đều | CẢ HAI | P1 | CHỐT |
| R-TLMI-114 | **Thuật toán chia đều về 100%** — công thức, làm tròn, số dư, sàn 3 % | CẢ HAI | P1 | CHỐT |
| R-TLMI-115 | Kéo thả đổi thứ tự cột; mặc định theo thứ tự cột trên lưới của form | FE | P1 | CHỐT |
| R-TLMI-116 | Ô Tìm cột lọc theo Tên cột dữ liệu và Tên hiển thị, không phân biệt dấu, không lưu | FE | P2 | CHỐT |
| R-TLMI-117 | Đang lọc ở ô Tìm cột thì không cho kéo thả cột | FE | P2 | CHỐT |
| R-TLMI-118 | Lọc ở ô Tìm cột không đổi thiết lập của cột bị ẩn khỏi lưới | FE | P1 | CHỐT |
| R-TLMI-119 | Cộng gộp mặt hàng — khóa gộp **có thuế suất**, gộp trước khi dựng bảng | BE | P0 | CHỐT (C01·C30) |

### Nhóm I — Khối tự do (R-TLMI-120…181)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-120 | Bấm Thêm khối tự do mở hộp Đặt tên khối với tên gợi ý | FE | P1 | CHỐT |
| R-TLMI-121 | Tên khối tự do không trống, tối đa 60 ký tự | CẢ HAI | P1 | CHỐT |
| R-TLMI-122 | Khối tự do mới đặt ngay trước khối Chữ ký | CẢ HAI | P1 | CHỐT |
| R-TLMI-123 | Khối tự do mới là lưới 1 dòng × 2 cột toàn ô trống | CẢ HAI | P1 | CHỐT |
| R-TLMI-124 | Thêm khối tự do thành công thì báo, mở bảng chỉnh và chọn sẵn ô đầu tiên | FE | P2 | CHỐT |
| R-TLMI-125 | Mỗi mẫu tối đa 10 khối tự do | CẢ HAI | P1 | CHỐT |
| R-TLMI-126 | Tên khối tự do không in ra bản in | CẢ HAI | P1 | CHỐT |
| R-TLMI-127 | Sửa tên khối tự do ở **cả hai chỗ** (hộp Đặt tên + ô Tên khối) | FE | P1 | CHỐT (C07) |
| R-TLMI-128 | Bảng chỉnh khối tự do không có ô Kích thước lưới và không có cột Vị trí | FE | P2 | CHỐT |
| R-TLMI-129 | Mỗi khối tự do tối đa 20 dòng | CẢ HAI | P1 | CHỐT |
| R-TLMI-130 | Mỗi khối tự do tối đa 6 cột | CẢ HAI | P1 | CHỐT |
| R-TLMI-131 | Các cột của khối tự do rộng bằng nhau, không đặt độ rộng riêng | CẢ HAI | P1 | CHỐT |
| R-TLMI-132 | Bấm ô để chọn ô; giữ Shift và bấm ô khác để chọn một vùng chữ nhật | FE | P2 | CHỐT |
| R-TLMI-133 | Thêm dòng trên/dưới, cột trái/phải ngay cạnh ô đang chọn, ô mới là ô trống | FE | P1 | CHỐT |
| R-TLMI-134 | Xóa dòng / Xóa cột xóa các dòng, cột mà vùng chọn phủ | FE | P1 | CHỐT |
| R-TLMI-135 | Khối tự do còn 1 dòng hoặc 1 cột thì nút − Dòng / − Cột mờ | FE | P1 | CHỐT |
| R-TLMI-136 | Chọn từ 2 ô rồi bấm Gộp ô thì vùng đó thành một ô nhiều dòng nhiều cột | FE | P1 | CHỐT |
| R-TLMI-137 | Vùng chọn chạm vào ô đã gộp thì tự nới ra cho trọn ô gộp đó | FE | P1 | CHỐT |
| R-TLMI-138 | Vùng gộp có từ 2 ô có nội dung thì hỏi trước khi gộp | FE | P1 | CHỐT |
| R-TLMI-139 | Gộp ô giữ nội dung của ô đầu tiên có nội dung, các ô còn lại mất nội dung | FE | P1 | CHỐT |
| R-TLMI-140 | Tách ô trả về các ô đơn, nội dung ở ô góc trên trái | FE | P1 | CHỐT |
| R-TLMI-141 | Xóa dòng / cột đi qua một ô gộp thì ô gộp được tách trước rồi mới xóa | FE | P1 | CHỐT |
| R-TLMI-142 | Thêm dòng / cột vào giữa một ô gộp thì ô gộp rộng thêm một dòng / cột | FE | P1 | CHỐT |
| R-TLMI-143 | Ô trống không in gì, chỉ chiếm chỗ để các ô khác thẳng hàng | CẢ HAI | P1 | CHỐT |
| R-TLMI-144 | Ô là một trường của form thì in dạng `Tên hiển thị: Giá trị` | CẢ HAI | P1 | CHỐT |
| R-TLMI-145 | Tên hiển thị của trường bị xóa trống thì chỉ in giá trị, không in nhãn và dấu ":" | CẢ HAI | P1 | CHỐT |
| R-TLMI-146 | Ô Chữ tự do in đúng chữ người dùng gõ, không có giá trị kèm theo | CẢ HAI | P1 | CHỐT |
| R-TLMI-147 | Gõ Chữ tự do ngay trong ô trên trang xem trước, tối đa 255 ký tự | CẢ HAI | P1 | CHỐT |
| R-TLMI-148 | Chọn Chữ tự do mà rời ô khi chưa gõ thì ô tự về Ô trống, không báo lỗi | FE | P1 | CHỐT |
| R-TLMI-149 | Kéo một dòng trường ở bảng chỉnh thả vào một ô để đặt trường vào ô | FE | P1 | CHỐT |
| R-TLMI-150 | Nháy đúp ô mở hộp chọn cạnh ô, hai mục đầu là (Ô trống) và Chữ tự do | FE | P1 | CHỐT |
| R-TLMI-151 | Gõ chữ trong hộp chọn trường thì lọc kho trường không phân biệt dấu | FE | P2 | CHỐT |
| R-TLMI-152 | Một trường chỉ ở một ô trong một khối; đặt lại vào ô khác thì chuyển sang ô mới | FE | P1 | CHỐT |
| R-TLMI-153 | Cùng một trường được dùng ở nhiều khối tự do khác nhau thì được phép | CẢ HAI | P1 | CHỐT |
| R-TLMI-154 | Kéo một ô có nội dung thả lên ô khác thì hai ô đổi nội dung cho nhau | FE | P1 | CHỐT |
| R-TLMI-155 | Xóa nội dung (phím Delete) đưa các ô đang chọn về ô trống | FE | P1 | CHỐT |
| R-TLMI-156 | **Tên hiển thị và In đậm là thuộc tính CỦA TRƯỜNG, dùng chung cả mẫu** | CẢ HAI | P1 | CHỐT |
| R-TLMI-157 | Tên hiển thị của trường tối đa 255 ký tự, mặc định bằng tên trường | CẢ HAI | P1 | CHỐT |
| R-TLMI-158 | Ô trường + In đậm = Có thì chỉ đậm Tên hiển thị, giá trị luôn in thường | CẢ HAI | P1 | CHỐT |
| R-TLMI-159 | Ô Chữ tự do + In đậm = Có thì đậm cả chữ | CẢ HAI | P1 | CHỐT |
| R-TLMI-160 | Nghiêng áp cho cả ô (nhãn và giá trị) | CẢ HAI | P2 | CHỐT |
| R-TLMI-161 | Căn Trái / Giữa / Phải trong khối tự do đặt **theo ô**, không theo trường | CẢ HAI | P1 | CHỐT |
| R-TLMI-162 | Chưa chọn ô nào thì mọi nút trên thanh công cụ khối tự do đều mờ | FE | P1 | CHỐT |
| R-TLMI-163 | Bấm In đậm / Nghiêng / Căn áp cho ô hoặc vùng đang chọn | FE | P1 | CHỐT |
| R-TLMI-164 | Trường chưa được đặt vào ô nào thì Tên hiển thị và In đậm của trường không lưu | CẢ HAI | P1 | CHỐT |
| R-TLMI-165 | Kho trường = mọi ô trên form trừ cột trong các lưới | CẢ HAI | P1 | CHỐT |
| R-TLMI-166 | Kho trường là một danh sách phẳng, không chia nhóm, theo thứ tự các ô trên form | FE | P2 | CHỐT |
| R-TLMI-167 | Ô mới ở phiên bản sau tự vào kho trường nhưng không tự chen vào khối tự do | CẢ HAI | P1 | CHỐT |
| R-TLMI-168 | Ô Tìm kiếm của khối tự do lọc theo tên trường và Tên hiển thị, không phân biệt dấu | FE | P1 | CHỐT |
| R-TLMI-169 | Cột Trường dữ liệu trong bảng chỉnh khối tự do luôn chỉ đọc | FE | P1 | CHỐT |
| R-TLMI-170 | Thanh công cụ khối tự do chỉ hiện khi đang chọn một khối tự do | FE | P1 | CHỐT |
| R-TLMI-171 | Menu chuột phải trên ô khối tự do có cùng tác dụng với thanh công cụ | FE | P1 | CHỐT |
| R-TLMI-172 | Ô đang chọn là Chữ tự do thì lệnh đầu menu là "Sửa chữ" | FE | P1 | CHỐT |
| R-TLMI-173 | Phím tắt trong lưới: mũi tên, Delete, Enter / F2 | FE | P2 | CHỐT |
| R-TLMI-174 | Gộp ô và Tách ô bật/tắt theo vùng chọn | FE | P1 | CHỐT |
| R-TLMI-175 | Xóa khối tự do thì hỏi trước | FE | P1 | CHỐT |
| R-TLMI-176 | Khối tự do đang bật mà mọi ô đều trống thì vẫn lưu được | CẢ HAI | P1 | CHỐT |
| R-TLMI-177 | Bật Hiện lưới căn chỉnh thì kẻ đường phân ô và gợi ý ở ô trống đang chọn | FE | P2 | CHỐT |
| R-TLMI-178 | Dấu hiệu của lưới căn chỉnh không in và không xuất PDF | CẢ HAI | P0 | CHỐT |
| R-TLMI-179 | Bỏ tick Hiện lưới căn chỉnh thì trang xem trước hiển thị đúng như bản in | FE | P2 | CHỐT |
| R-TLMI-180 | In ô gộp thì ô chiếm đúng số dòng, số cột đã gộp | FE | P1 | CHỐT |
| R-TLMI-181 | Giá trị dài trong ô tự xuống dòng, các ô cùng hàng cao bằng nhau | FE | P1 | CHỐT |

### Nhóm K — Khối Chữ ký (R-TLMI-182…200)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-182 | Danh sách ô ký gồm 5 chức danh của Thiết lập người ký và các ô ký tự do | CẢ HAI | P1 | CHỐT |
| R-TLMI-183 | Thứ tự ô ký mặc định và kéo thả đổi được | CẢ HAI | P1 | CHỐT |
| R-TLMI-184 | Mặc định bật Người lập phiếu, Kế toán trưởng, Giám đốc; tắt Thủ kho, Thủ quỹ | CẢ HAI | P1 | CHỐT |
| R-TLMI-185 | Cột chức danh chỉ đọc; ô ký tự do mang nhãn "tự do" | CẢ HAI | P1 | CHỐT |
| R-TLMI-186 | Chức danh có sẵn: Tên người ký lấy từ Thiết lập người ký, chỉ đọc, không có nút xóa | CẢ HAI | P1 | CHỐT |
| R-TLMI-187 | Ô ký tự do: Tên người ký trống, gõ tay được, có nút xóa | CẢ HAI | P1 | CHỐT |
| R-TLMI-188 | Tiêu đề in ra bắt buộc, **mẫu sửa riêng được**, mặc định theo Thiết lập người ký | CẢ HAI | P1 | CHỐT (C04) |
| R-TLMI-189 | Ô ký tự do đang bật phải có tiêu đề in ra không trống, tối đa 60 ký tự | CẢ HAI | P1 | CHỐT |
| R-TLMI-190 | Dòng ghi chú mặc định "(Ký, họ tên)", riêng Giám đốc "(Ký, họ tên, đóng dấu)" | CẢ HAI | P1 | CHỐT |
| R-TLMI-191 | Ô tick của ô ký quyết định in hay không in ô ký đó | CẢ HAI | P1 | CHỐT |
| R-TLMI-192 | Ô ký tự do xóa được; chức danh của Thiết lập người ký chỉ tắt được | CẢ HAI | P0 | CHỐT |
| R-TLMI-193 | Thêm ô ký tự do — không giới hạn số ô ký | CẢ HAI | P1 | CHỐT |
| R-TLMI-194 | In khối Chữ ký chia đều các ô đang bật, mỗi ô rộng tối thiểu 4 cm | FE | P1 | CHỐT |
| R-TLMI-195 | Một hàng ô ký hết chỗ thì ô tiếp theo tự xuống hàng và hàng mới lại chia đều | FE | P1 | CHỐT |
| R-TLMI-196 | In tên người ký theo cờ "In tên người ký trên chứng từ, báo cáo" (chỉ đọc ở màn này) | CẢ HAI | P1 | CHỐT |
| R-TLMI-197 | Dòng "Ngày … tháng … năm …" in nghiêng căn phải phía trên các ô ký, lấy ngày chứng từ | CẢ HAI | P1 | CHỐT |
| R-TLMI-198 | Chỗ trống ký Thấp / Vừa / Cao, mặc định Vừa | CẢ HAI | P2 | CHỐT |
| R-TLMI-199 | Khối Chữ ký đọc hồ sơ đơn vị của **chi nhánh ghi trên chứng từ** | BE | P1 | CHỐT (C05) |
| R-TLMI-200 | Cuối trang không đủ chỗ thì cả khối Chữ ký sang trang mới, không bị cắt đôi | FE | P1 | CHỐT |

### Nhóm L — Bố cục mẫu (R-TLMI-201…216)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-201 | Cột trái là Bố cục mẫu: danh sách khối theo thứ tự in, kéo thả được | FE | P1 | CHỐT |
| R-TLMI-202 | Mục đầu danh sách là "Thiết lập mẫu", không phải khối, không kéo được | FE | P1 | CHỐT |
| R-TLMI-203 | Dòng khối chỉ có biểu tượng kéo, con mắt, tên khối (và nút xóa với khối tự do) | FE | P2 | CHỐT |
| R-TLMI-204 | Kéo biểu tượng ⠿ của dòng khối để đổi thứ tự khối (= thứ tự in) | FE | P1 | CHỐT |
| R-TLMI-205 | Kéo khối ngay trên trang xem trước cho cùng kết quả với kéo ở Bố cục mẫu | FE | P1 | CHỐT |
| R-TLMI-206 | Mọi khối, kể cả Thông tin đầu trang và Chữ ký, đều kéo được | FE | P1 | CHỐT |
| R-TLMI-207 | Con mắt của khối = Có thì khối được in ra; mặc định Có | CẢ HAI | P1 | CHỐT |
| R-TLMI-208 | Con mắt = Không thì khối không in và các khối sau dồn lên | CẢ HAI | P1 | CHỐT |
| R-TLMI-209 | Tắt con mắt không mất thiết lập bên trong khối | CẢ HAI | P1 | CHỐT |
| R-TLMI-210 | Khối chuẩn không xóa được, chỉ ẩn được; nút xóa ẩn hẳn | CẢ HAI | P0 | CHỐT |
| R-TLMI-211 | Khối tự do có nút xóa ở cả Bố cục mẫu lẫn bảng chỉnh | FE | P1 | CHỐT |
| R-TLMI-212 | Tên khối chuẩn cố định; khối Bảng đặt tên "Bảng \<tên lưới\>" | CẢ HAI | P1 | CHỐT |
| R-TLMI-213 | Bấm một dòng khối thì bảng chỉnh mở đúng khối đó và khối được đánh dấu trên trang | FE | P2 | CHỐT |
| R-TLMI-214 | Bấm một khối trên trang xem trước thì bảng chỉnh mở đúng khối đó | FE | P2 | CHỐT |
| R-TLMI-215 | Rê chuột lên một khối trên trang xem trước thì hiện nhãn tên khối | FE | P2 | CHỐT |
| R-TLMI-216 | Chỉ bảng chỉnh bên phải đổi theo khối đang chọn; cột trái, cột giữa, thanh tiêu đề luôn hiện | FE | P1 | CHỐT |

### Nhóm M — Xem trước & thao tác trên trang (R-TLMI-217…229)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-217 | Trang xem trước vẽ trang đầu bằng dữ liệu thật của chứng từ đang mở | FE | P1 | CHỐT |
| R-TLMI-218 | Bất kỳ thay đổi nào trên màn thì trang xem trước vẽ lại ngay | FE | P1 | CHỐT |
| R-TLMI-219 | Không có chế độ dữ liệu mẫu và không chọn được chứng từ khác | FE | P1 | CHỐT |
| R-TLMI-220 | Trang xem trước vẽ theo nhóm Giấy và chữ của mẫu, kể cả hướng Tự động | FE | P1 | CHỐT |
| R-TLMI-221 | Thu / Phóng / Vừa khung chỉ đổi tỷ lệ nhìn, không ảnh hưởng bản in | FE | P2 | CHỐT |
| R-TLMI-222 | Hiện lưới căn chỉnh chỉ trên màn, **không lưu**, mặc định Có | FE | P1 | CHỐT |
| R-TLMI-223 | Hoàn tác / Làm lại nằm trên thanh Xem trước, nhớ tối đa **60 bước** trong phiên | FE | P1 | CHỐT |
| R-TLMI-224 | Mỗi thao tác đổi mẫu là một bước; gõ chữ trong một ô tính một bước khi rời ô | FE | P1 | CHỐT |
| R-TLMI-225 | Đóng màn thì lịch sử Hoàn tác / Làm lại bị xóa | FE | P1 | CHỐT |
| R-TLMI-226 | Hết bước Hoàn tác (hoặc Làm lại) thì nút tương ứng mờ | FE | P2 | CHỐT |
| R-TLMI-227 | Ctrl+Z / Ctrl+Y tương đương Hoàn tác / Làm lại | FE | P2 | CHỐT |
| R-TLMI-228 | Thanh Xem trước luôn hiện ở mọi khối đang chọn | FE | P1 | CHỐT |
| R-TLMI-229 | Trang xem trước là nơi thao tác với lưới khối tự do | FE | P1 | CHỐT |

### Nhóm N — Kiểm tra & trạng thái (R-TLMI-230…258)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-230 | Rời một ô thì kiểm tra ngay ô đó, không có mục kiểm tra riêng | FE | P1 | CHỐT |
| R-TLMI-231 | Ô không hợp lệ được đánh dấu tại chỗ kèm nội dung thông báo tương ứng | FE | P1 | CHỐT |
| R-TLMI-232 | Khối chứa ô lỗi được đánh dấu ở **hai nơi**: dòng khối và khối trên trang xem trước | FE | P1 | CHỐT |
| R-TLMI-233 | Rê chuột lên dòng khối hoặc khối đang lỗi thì hiện nội dung lỗi | FE | P2 | CHỐT |
| R-TLMI-234 | Sửa đúng thì các dấu hiệu lỗi tắt ngay | FE | P1 | CHỐT |
| R-TLMI-235 | Ô lưới khối tự do không hợp lệ thì viền đỏ ngay trên trang xem trước | FE | P1 | CHỐT |
| R-TLMI-236 | Ô trống trong khối tự do **không bao giờ** là lỗi | CẢ HAI | P1 | CHỐT |
| R-TLMI-237 | Xét lỗi trong khối tự do chỉ xét ô có nội dung | CẢ HAI | P1 | CHỐT |
| R-TLMI-238 | Không có cảnh báo mềm cho lựa chọn hợp lệ nhưng bất thường | CẢ HAI | P1 | CHỐT |
| R-TLMI-239 | **Bảng kiểm tra dữ liệu 17 dòng** — tầng và thời điểm kiểm tra | CẢ HAI | P0 | CHỐT |
| R-TLMI-240 | Nhãn trạng thái "Đã lưu" và nút Lưu mờ | FE | P1 | CHỐT |
| R-TLMI-241 | Nhãn trạng thái "Chưa lưu" | FE | P1 | CHỐT |
| R-TLMI-242 | Nhãn trạng thái "Có lỗi" | FE | P1 | CHỐT |
| R-TLMI-243 | Có lỗi mà bấm Lưu thì không ghi, chỉ báo **lỗi đầu tiên** theo thứ tự đã định | CẢ HAI | P0 | CHỐT |
| R-TLMI-244 | Báo lỗi đầu tiên thì mở bảng chỉnh của khối đó và đưa con trỏ vào ô lỗi | FE | P1 | CHỐT |
| R-TLMI-245 | Tiêu đề màn và vị trí nhãn trạng thái, nút Lưu | FE | P2 | CHỐT |
| R-TLMI-246 | Bấm Lưu thì kiểm tra lại toàn bộ theo bảng Validation, **cả ở server** | BE | P0 | CHỐT |
| R-TLMI-247 | Lưu hợp lệ thì ghi toàn bộ mẫu trong **một transaction** | BE | P0 | CHỐT |
| R-TLMI-248 | Lưu thành công thì báo, màn giữ nguyên, nhãn trạng thái về "Đã lưu" | CẢ HAI | P1 | CHỐT |
| R-TLMI-249 | Lưu gặp lỗi hệ thống thì rollback, giữ nguyên màn và báo lỗi | CẢ HAI | P0 | CHỐT |
| R-TLMI-250 | Ctrl+S tương đương bấm Lưu | FE | P2 | CHỐT |
| R-TLMI-251 | Đóng hoặc Esc khi mẫu khác bản đã lưu thì hỏi với ba lựa chọn | FE | P0 | CHỐT |
| R-TLMI-252 | Chọn "Lưu và đóng" thì chạy Lưu, thành công mới đóng | FE | P0 | CHỐT |
| R-TLMI-253 | Chọn "Không lưu" thì bỏ mọi thay đổi và đóng | FE | P0 | CHỐT |
| R-TLMI-254 | Chọn "Ở lại" thì giữ màn | FE | P1 | CHỐT |
| R-TLMI-255 | Không có thay đổi mà bấm Đóng / Esc thì đóng ngay, không hỏi | FE | P1 | CHỐT |
| R-TLMI-256 | Đang mở một hộp thoại con thì phím Esc không tác dụng với màn chính | FE | P1 | CHỐT |
| R-TLMI-257 | Chân màn: Đóng ở góc trái; Đặt lại mẫu chuẩn · Lưu ở góc phải | FE | P2 | CHỐT |
| R-TLMI-258 | Hai người cùng sửa một mẫu — **khóa lạc quan** bằng `phienBan` | BE | P1 | CHỐT (C06) |

### Nhóm P — Dựng bản in (UC02) (R-TLMI-259…271)

| ID | Tên luật | Tầng | Sev | Trạng thái |
|---|---|---|---|---|
| R-TLMI-259 | Chọn Mẫu tùy chỉnh thì dựng bản in theo mẫu của nghiệp vụ chứng từ đang mở | BE | P0 | CHỐT |
| R-TLMI-260 | Chưa có bản ghi mẫu thì in theo mẫu chuẩn hệ thống và báo một lần | CẢ HAI | P1 | CHỐT |
| R-TLMI-261 | Nút In bị disable theo hai quy tắc cấm in thì cả menu In không mở được | CẢ HAI | P0 | CHỐT |
| R-TLMI-262 | Dựng bản in từ trên xuống theo thứ tự Bố cục mẫu, chỉ các khối đang bật | BE | P1 | CHỐT |
| R-TLMI-263 | Hình nền vẽ dưới cùng | FE | P1 | CHỐT |
| R-TLMI-264 | Chữ, đường kẻ và giấy-chữ của bản in theo mẫu; ô theo chung lấy giá trị lúc in | BE | P0 | CHỐT |
| R-TLMI-265 | Bảng dài tràn trang; khối đứng sau in tiếp ngay dưới dòng cuối của bảng | FE | P1 | CHỐT |
| R-TLMI-266 | Áp ba quy tắc in chứng từ của thiết lập chung khi dựng bản in | BE | P0 | CHỐT (C01·C30) |
| R-TLMI-267 | Đọc hồ sơ đơn vị để in theo chi nhánh ghi trên chứng từ | BE | P0 | CHỐT |
| R-TLMI-268 | Mở màn xem trước bản in như các mẫu cố định | FE | P1 | CHỐT |
| R-TLMI-269 | Màn xem trước có nút Sửa mẫu khi người dùng có quyền | FE | P0 | CHỐT |
| R-TLMI-270 | Lỗi hệ thống khi dựng bản in thì báo và **không** mở màn xem trước | CẢ HAI | P0 | CHỐT |
| R-TLMI-271 | In bằng mẫu tùy chỉnh không thay đổi dữ liệu chứng từ hay mẫu | BE | P1 | CHỐT |

---

## A. Phạm vi & vòng đời mẫu

### R-TLMI-001 · Một mẫu tùy chỉnh cho mỗi cặp (loại chứng từ, nghiệp vụ) của một đơn vị kế toán

```
Tầng      BE
Sev       P0
Nguồn     SCR:3 · SCR:244 · SCR:245 · SCR:247 · FB:7 · CRUD:17 · BR2P BR51.5
WHEN      đơn vị kế toán chỉnh mẫu chuẩn của một cặp (loại chứng từ, nghiệp vụ)
THEN      kết quả là ĐÚNG MỘT bản ghi cfg_mau_in_chung_tu cho cặp đó, không có nhiều bản
Lỗi       —
Bất biến  INV-TLMI-001
Ghi chú   BR nội bộ màn BR1 (SCR:244). BR chung nền: BR51.5 "một mẫu cho cả đơn vị" (Phase 2).
```

### R-TLMI-002 · "Nghiệp vụ" = giá trị ô Loại nghiệp vụ trên form

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:245
WHEN      xác định phạm vi một mẫu
THEN      "nghiệp vụ" là giá trị ô **Loại nghiệp vụ** trên form, do epic nghiệp vụ định nghĩa
Lỗi       —
Bất biến  INV-TLMI-001
Ghi chú   BR1.
```

### R-TLMI-003 · Loại chứng từ không chia nghiệp vụ thì cả loại chứng từ là một mẫu

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:245
WHEN      loại chứng từ KHÔNG chia nghiệp vụ
THEN      cả loại chứng từ đó là một mẫu (một bản ghi)
Lỗi       —
Bất biến  INV-TLMI-001
Ghi chú   BR1.
```

### R-TLMI-004 · Khóa duy nhất của mẫu = (TenantId, MaChucNang, MaNghiepVu)

```
Tầng      BE
Sev       P0
Nguồn     SCR:247 · BR2P BR50.6 (đối chiếu, xem C-nhóm §Ghi chú)
WHEN      lưu mẫu
THEN      cfg_mau_in_chung_tu duy nhất theo (TenantId, MaChucNang, MaNghiepVu)
ELSE      KHÔNG có ChiNhanhId trong khóa duy nhất; truy vấn KHÔNG lọc theo chi nhánh đang làm việc
Lỗi       —
Bất biến  INV-TLMI-001, INV-TLMI-011
Ghi chú   BR1. Bảng phạm vi BR50.6 (BR2P) không liệt kê cfg_mau_in_chung_tu ở nhóm nào —
          ghi nhận là khoảng trống của BR chung Phase 2, không chặn luật này.
```

### R-TLMI-005 · Mẫu dùng chung mọi người dùng và mọi chi nhánh

```
Tầng      BE
Sev       P0
Nguồn     SCR:3 · SCR:247 · FB:7 · BR2P BR51.5
WHEN      một mẫu đã lưu
THEN      mẫu áp cho MỌI người dùng và MỌI chi nhánh; sửa ở chi nhánh nào cũng áp cho chi nhánh còn lại
ELSE      không có mẫu theo người dùng, không có mẫu theo chi nhánh
Lỗi       —
Bất biến  INV-TLMI-011
Ghi chú   BR1. Đối xứng ngược với quyền — xem R-TLMI-031, R-TLMI-035.
```

### R-TLMI-006 · Mỗi cặp có đúng một mẫu chuẩn hệ thống, sinh từ đặc tả form

```
Tầng      BE
Sev       P0
Nguồn     SCR:3 · CRUD:15 · UC01:16
WHEN      xét một cặp (loại chứng từ, nghiệp vụ)
THEN      tồn tại ĐÚNG MỘT mẫu chuẩn hệ thống cố định, là **dữ liệu cố định sinh từ đặc tả form
          của epic nghiệp vụ**, KHÔNG có entity riêng trong DB
Lỗi       —
Bất biến  INV-TLMI-002
Ghi chú   CRUD:15 nguyên văn: "Mẫu chuẩn hệ thống … là dữ liệu cố định sinh từ đặc tả form của
          epic nghiệp vụ, không có entity riêng."
```

### R-TLMI-007 · Chưa có bản ghi mẫu = nghiệp vụ đang dùng mẫu chuẩn hệ thống

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:247 · SCR:328 · CRUD:15 · UC01:23 · UC02:17 · MSG:16
WHEN      không tồn tại bản ghi cfg_mau_in_chung_tu của cặp (loại chứng từ, nghiệp vụ)
THEN      nghiệp vụ đó đang dùng mẫu chuẩn hệ thống
Lỗi       MSG_PMKT-E-14549_21_103 (chỉ khi in — xem R-TLMI-260)
Bất biến  INV-TLMI-002
Ghi chú   BR1, BR12. Vắng bản ghi CHÍNH LÀ trạng thái "đang dùng mẫu chuẩn" — không có cờ riêng.
```

### R-TLMI-008 · Mẫu chuẩn có đúng bốn loại khối theo thứ tự cố định

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:51 · SCR:260 · UC01:23 · AD01:14-15 · FIGMA (cột BỐ CỤC MẪU)
WHEN      dựng mẫu chuẩn hệ thống của bất kỳ loại chứng từ nào
THEN      có đúng bốn loại khối theo thứ tự: Thông tin đầu trang → Tiêu đề → các Bảng → Chữ ký
ELSE      không có khối nào khác
Lỗi       —
Bất biến  INV-TLMI-008
Ghi chú   BR3. UC01:23 nguyên văn "không có khối nào khác".
```

### R-TLMI-009 · Form có n lưới thì mẫu chuẩn có n khối Bảng

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:148 · SCR:260 · UC01:23 · FB:13
WHEN      form gốc của nghiệp vụ có n lưới
THEN      mẫu chuẩn có n khối Bảng, tên khối = "Bảng <tên lưới>", mọi lưới đều bật, mỗi bảng đủ cột gốc
Lỗi       —
Bất biến  INV-TLMI-008
Ghi chú   BR3. Xem R-TLMI-092 (cột của khối Bảng).
```

### R-TLMI-010 · Thông tin chung / tổng tiền phải tự dựng bằng khối tự do

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:260
WHEN      cần in phần thông tin chung, tổng tiền… trên bản in
THEN      người dùng tự dựng bằng **khối tự do** (mẫu chuẩn KHÔNG có sẵn khối đó)
Lỗi       —
Bất biến  INV-TLMI-008
Ghi chú   BR3, BR6.
```

### R-TLMI-011 · Mở màn từ một chứng từ thì mở đúng mẫu của nghiệp vụ chứng từ đó

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:246 · SCR:327 · UC01:22 · UC01:49 · UC02:22
WHEN      mở màn Thiết lập mẫu in từ một chứng từ (bằng bất kỳ lối vào nào)
THEN      mở đúng mẫu của **nghiệp vụ mà chứng từ đó đang chọn**
Lỗi       —
Bất biến  —
Ghi chú   BR1, BR12.
```

### R-TLMI-012 · Đổi Loại nghiệp vụ trên form rồi mở lại thì mở một mẫu khác

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:246
WHEN      người dùng đổi ô Loại nghiệp vụ trên form rồi mở lại màn
THEN      mở một mẫu KHÁC — mẫu của nghiệp vụ mới
Lỗi       —
Bất biến  INV-TLMI-001
Ghi chú   BR1.
```

### R-TLMI-013 · Mẫu in cố định theo quy định không sửa được

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:248 · FB:7 · UC02:21
WHEN      nghiệp vụ có mẫu in cố định theo quy định (01-TT, 02-VT…)
THEN      các mẫu đó KHÔNG sửa được và vẫn in như cũ; chúng vẫn liệt kê trong menu In
Lỗi       —
Bất biến  —
Ghi chú   BR1. Nằm ngoài phạm vi epic _21.
```

### R-TLMI-014 · Nghiệp vụ nào có chức năng này và mã quyền là gì do epic nghiệp vụ khai báo

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:10 · SCR:248 · FB:9 · UC01:11 · UC01:16 · BR2P BR51.5
WHEN      cần biết chứng từ / nghiệp vụ nào có chức năng Thiết lập mẫu in và mã quyền là gì
THEN      lấy theo khai báo của **epic nghiệp vụ**, tham chiếu về màn này
ELSE      epic _21 KHÔNG liệt kê nghiệp vụ nào và KHÔNG khai mã quyền nào
Lỗi       —
Bất biến  —
Ghi chú   BR1. FB:9 nguyên văn: "Epic này không liệt kê chứng từ nào, nghiệp vụ nào có mẫu tùy chỉnh."
          ⇒ hằng số quyền CHƯA code được ở epic này — xem §Z mục thiếu quy định.
```

### R-TLMI-015 · Bấm Đặt lại mẫu chuẩn thì hỏi trước

```
Tầng      FE
Sev       P1
Nguồn     SCR:234 · SCR:310 · SCR:363 · UC01:33 · UC01:71 · MSG:45
WHEN      người dùng bấm nút **Đặt lại mẫu chuẩn**
THEN      hỏi MSG_PMKT-E-14549_21_402 trước khi làm gì
Lỗi       MSG_PMKT-E-14549_21_402 — "Mọi tùy chỉnh (kể cả khối tự do, thứ tự khối, cột bảng, chữ ký)
          sẽ trở về mẫu chuẩn hệ thống. Thay đổi chỉ có hiệu lực khi bạn bấm Lưu. Tiếp tục?"
Bất biến  —
Ghi chú   BR9. Tài liệu KHÔNG nêu tên hai nút của hộp xác nhận này — xem §Z.
```

### R-TLMI-016 · Xác nhận Đặt lại thì nạp lại toàn bộ mẫu chuẩn hệ thống

```
Tầng      FE
Sev       P1
Nguồn     SCR:38 · SCR:310 · UC01:33 · UC01:72
WHEN      người dùng xác nhận MSG_402
THEN      màn nạp lại mẫu chuẩn hệ thống của nghiệp vụ:
            · bốn loại khối theo thứ tự chuẩn, đủ cột gốc, chữ ký mặc định
            · mọi ô nhóm Giấy và chữ VỀ THEO CHUNG
            · bảy ô tick Thông tin đầu trang VỀ THEO CHUNG
            · Màu chữ = đen
            · Kiểu hình nền = Không
            · BỎ mọi khối tự do
Lỗi       —
Bất biến  INV-TLMI-003, INV-TLMI-008
Ghi chú   BR9. Nút này KHÔNG ghi DB ngay — xem R-TLMI-018.
```

### R-TLMI-017 · Đặt lại xong thì báo và chuyển nhãn trạng thái Chưa lưu

```
Tầng      FE
Sev       P1
Nguồn     SCR:310 · SCR:363 · UC01:72 · MSG:15
WHEN      Đặt lại mẫu chuẩn hoàn tất trên màn
THEN      hiển thị MSG_PMKT-E-14549_21_102 và nhãn trạng thái chuyển **Chưa lưu**
Lỗi       MSG_PMKT-E-14549_21_102 — "Đã đưa về mẫu chuẩn hệ thống. Bấm Lưu để có hiệu lực"
Bất biến  —
Ghi chú   BR9, BR10.
```

### R-TLMI-018 · Đặt lại chỉ đổi trên màn, bấm Lưu mới có hiệu lực

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:38 · SCR:310 · SCR:318 · UC01:33
WHEN      người dùng Đặt lại mẫu chuẩn nhưng CHƯA bấm Lưu
THEN      DB không đổi; bản ghi mẫu cũ còn nguyên
Lỗi       —
Bất biến  —
Ghi chú   BR9, BR10. Hiệu lực thật xảy ra ở R-TLMI-021 (đang bị C02 chặn).
```

### R-TLMI-019 · Đặt lại mà chưa Lưu rồi Đóng › Không lưu thì mẫu cũ còn nguyên

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:310 · SCR:321
WHEN      Đặt lại mẫu chuẩn AND chưa Lưu AND người dùng chọn Đóng › *Không lưu*
THEN      mẫu cũ trong DB còn nguyên, không bản ghi nào bị xóa
Lỗi       —
Bất biến  INV-TLMI-012
Ghi chú   BR9, BR11.
```

### R-TLMI-020 · Không đồng ý hộp xác nhận Đặt lại thì giữ nguyên mẫu đang chỉnh

```
Tầng      FE
Sev       P1
Nguồn     UC01:72
WHEN      người dùng KHÔNG đồng ý MSG_402
THEN      giữ nguyên mẫu đang chỉnh trên màn, không đổi gì
Lỗi       —
Bất biến  —
Ghi chú   BR9 · UC01 NL3.
```

### R-TLMI-021 · Lưu khi mẫu bằng mẫu chuẩn thì xóa bản ghi cùng các bảng con

```
Tầng      BE
Sev       P0
Nguồn     SCR:318 · SCR:310 · UC01:33 · UC01:54 · CRUD:17 · AD01:30-31
Chốt      C02 · 04-quyet-dinh-ban-giao.md §2 · Dat · 2026-09-19

WHEN      bấm Lưu AND chuanHoa(JSON mẫu trên màn) == chuanHoa(JSON mẫu chuẩn hệ thống)
            chuanHoa() = sắp khóa theo thứ tự cố định
                       + bỏ MỌI khóa có giá trị null hoặc vắng mặt
                       + bỏ id kỹ thuật
THEN      xóa bản ghi mẫu cùng toàn bộ nhánh con (khối, cột, ô lưới, chữ ký), trong CÙNG transaction
          với thao tác Lưu ⇒ nghiệp vụ trở về dùng mẫu chuẩn hệ thống
ELSE      chưa có bản ghi AND mẫu trên màn bằng mẫu chuẩn ⇒ **KHÔNG tạo** bản ghi
Lỗi       —
Bất biến  INV-TLMI-002
Ghi chú   Tài liệu có HAI cách hiểu, đã chốt **cách (A) — so sánh nội dung**:
          (A) ĐÃ CHỌN · SO SÁNH NỘI DUNG — SCR:318 "mẫu trên màn **đúng bằng mẫu chuẩn**";
              AD01:30 "if (Mẫu đang **bằng** mẫu chuẩn?) then (Có) → Xóa bản ghi mẫu cùng bảng con".
          (B) KHÔNG CHỌN · ĐẾN TỪ HÀNH ĐỘNG ĐẶT LẠI — UC01:54 "nếu mẫu đang là mẫu chuẩn
              **(sau Đặt lại)**"; UC01:33; CRUD:17 "Xóa (D) xảy ra khi người dùng bấm **Đặt lại
              mẫu chuẩn** rồi **Lưu**" ⇒ chỉ cần một cờ "phiên này đã Đặt lại và chưa sửa gì sau đó".
          Vì sao chọn (A):
            1. Hai nguồn phát biểu theo **nội dung** (SCR:318 bậc 4, AD01:30) nói thẳng điều kiện;
               (B) chỉ suy ra từ ngữ cảnh "(sau Đặt lại)".
            2. Với mô hình lưu **JSON** (quyết định Q-01), so sâu chỉ là **so hai chuỗi đã chuẩn hóa**
               — rẻ, không cần duyệt cây quan hệ.
            3. Cho bất biến sạch: *mẫu bằng chuẩn ⇔ không tồn tại bản ghi* (INV-TLMI-002 đúng cả
               hai chiều). Với (B) bất biến chỉ đúng một chiều.
            4. Không sinh bản ghi rác khi người dùng mở màn rồi Lưu mà không sửa gì.
          Hệ quả đo được so với (B): chỉnh tay rồi Hoàn tác hết về đúng mẫu chuẩn ⇒ **xóa bản ghi**
          (với (B) thì giữ). Lưu lần đầu khi chưa có bản ghi và không sửa gì ⇒ **không tạo**
          (với (B) thì tạo mới theo "tạo mới nếu chưa có" của UC01:54).
```

### R-TLMI-022 · Lưu thành công thì mọi lần in Mẫu tùy chỉnh sau đó dùng mẫu mới ngay

```
Tầng      BE
Sev       P1
Nguồn     SCR:318 · UC01:32 · UC01:92
WHEN      Lưu mẫu thành công
THEN      từ đó menu In › Mẫu tùy chỉnh của MỌI chứng từ cùng nghiệp vụ dùng mẫu này, áp cho cả đơn vị kế toán
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

---

## B. Lối vào & quyền

### R-TLMI-023 · Menu In: mẫu cố định → đường kẻ → Mẫu tùy chỉnh → Thiết lập mẫu in…

```
Tầng      FE
Sev       P1
Nguồn     SCR:325 · UC02:21 · MT:57-58 · BR2P BR51.5
WHEN      mở menu In của chứng từ
THEN      menu gồm các mẫu in cố định của nghiệp vụ như hiện nay → một đường kẻ ngăn cách →
          **Mẫu tùy chỉnh** → **Thiết lập mẫu in…**
Lỗi       —
Bất biến  —
Ghi chú   BR12. Mục "Thiết lập mẫu in…" còn phụ thuộc quyền — R-TLMI-032.
```

### R-TLMI-024 · Hai mục menu dùng đúng tên cho mọi nghiệp vụ

```
Tầng      FE
Sev       P1
Nguồn     SCR:325
WHEN      đặt tên hai mục trong menu In
THEN      dùng đúng nguyên văn "Mẫu tùy chỉnh" và "Thiết lập mẫu in…" cho MỌI nghiệp vụ
Lỗi       —
Bất biến  —
Ghi chú   BR12. Hai chuỗi này phải có key i18n ở cả vi.ts và en.ts (luật 2), giữ nguyên văn tiếng Việt.
```

### R-TLMI-025 · Form thêm mới không có nút In

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:9 · SCR:325 · UC01:42
WHEN      form chứng từ đang ở chế độ **thêm mới**
THEN      không có nút In ⇒ không có lối vào màn Thiết lập mẫu in
ELSE      menu In chỉ có trên **form sửa** và **form xem chi tiết** của chứng từ ĐÃ LƯU
Lỗi       —
Bất biến  —
Ghi chú   BR12 · UC01 Tiền điều kiện.
```

### R-TLMI-026 · Nghiệp vụ có In từ danh sách thì menu In cũng ở màn danh sách

```
Tầng      FE
Sev       P1
Nguồn     SCR:325 · UC02:33
WHEN      nghiệp vụ có chức năng In từ danh sách
THEN      menu In cũng xuất hiện trên màn danh sách
Lỗi       —
Bất biến  —
Ghi chú   BR12.
```

### R-TLMI-027 · Màn xem trước bản in có thêm nút Sửa mẫu

```
Tầng      FE
Sev       P1
Nguồn     SCR:326 · UC02:25 · UC01:22 · FIGMA (frame 0 — header: In · Xuất file · Sửa mẫu)
WHEN      người dùng ở màn xem trước bản in của chứng từ
THEN      có thêm nút **Sửa mẫu** cạnh các nút In / Xuất file; bấm thì mở màn Thiết lập mẫu in
Lỗi       —
Bất biến  —
Ghi chú   BR12. Còn phụ thuộc quyền — R-TLMI-032, R-TLMI-269.
```

### R-TLMI-028 · Hai lối vào cho cùng một màn và cùng một mẫu

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:327 · UC01:22
WHEN      vào màn bằng một trong hai lối (menu In hoặc nút Sửa mẫu)
THEN      cùng một màn và cùng một mẫu: mẫu của nghiệp vụ của chứng từ đang mở
Lỗi       —
Bất biến  —
Ghi chú   BR12, BR1.
```

### R-TLMI-029 · Đóng màn thì quay lại đúng nơi vừa mở ra

```
Tầng      FE
Sev       P1
Nguồn     SCR:327 · UC01:22
WHEN      đóng màn Thiết lập mẫu in
THEN      quay lại ĐÚNG nơi vừa mở ra (form chứng từ hoặc màn xem trước bản in)
Lỗi       —
Bất biến  —
Ghi chú   BR12, BR11.
```

### R-TLMI-030 · Quay lại màn xem trước sau khi lưu thì bản in vẽ lại theo mẫu vừa lưu

```
Tầng      FE
Sev       P1
Nguồn     SCR:327
WHEN      quay lại màn xem trước bản in sau khi đã Lưu mẫu
THEN      bản in được vẽ lại theo mẫu vừa lưu
Lỗi       —
Bất biến  —
Ghi chú   BR12.
```

### R-TLMI-031 · Quyền Thiết lập mẫu in xét theo nghiệp vụ tại chi nhánh đang làm việc

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:10 · SCR:322 · UC01:11 · UC01:43 · MT:29
WHEN      kiểm tra quyền mở màn / lưu mẫu
THEN      quyền cần có là **Thiết lập mẫu in** của CHÍNH nghiệp vụ đó, **tenant-scoped, xét theo
          chi nhánh đang làm việc**; mã quyền do epic nghiệp vụ khai báo (R-TLMI-014)
Lỗi       MSG_PMKT-E-14549_21_002 (khi gọi thẳng API — R-TLMI-034)
Bất biến  —
Ghi chú   BR11.
```

### R-TLMI-032 · Không có quyền thì mục menu và nút Sửa mẫu ẩn hẳn

```
Tầng      FE
Sev       P0
Nguồn     SCR:10 · SCR:322 · SCR:325 · SCR:326 · UC01:62 · MT:29 · MT:58 · MT:59
WHEN      người dùng KHÔNG có quyền Thiết lập mẫu in của nghiệp vụ
THEN      mục "Thiết lập mẫu in…" trong menu In **Hide** (ẩn hẳn, không render)
          AND nút "Sửa mẫu" trên màn xem trước bản in **Hide**
ELSE      KHÔNG phải disable
Lỗi       —
Bất biến  —
Ghi chú   BR11 · MT:49 định nghĩa `Hide` = "Ẩn hẳn, không render".
```

### R-TLMI-033 · Không có quyền Thiết lập mẫu in nhưng có quyền In thì vẫn in được Mẫu tùy chỉnh

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:322 · UC01:12 · UC01:62 · UC02:11 · MT:57
WHEN      người dùng KHÔNG có quyền Thiết lập mẫu in nhưng CÓ quyền In của nghiệp vụ
THEN      mục "Mẫu tùy chỉnh" vẫn **Show** và vẫn in được bằng mẫu tùy chỉnh đã lưu
Lỗi       —
Bất biến  —
Ghi chú   BR11, BR12. MT:57 (dòng "Mẫu tùy chỉnh") KHÔNG mang điều kiện (đk-Q).
```

### R-TLMI-034 · Gọi thẳng API mà không có quyền thì server chặn

```
Tầng      BE
Sev       P0
Nguồn     SCR:322 · SCR:356 · UC01:62 · MSG:7 · MT:29
WHEN      gọi thẳng API mở màn hoặc API lưu mẫu mà không có quyền Thiết lập mẫu in
THEN      server chặn và trả MSG_PMKT-E-14549_21_002
Lỗi       MSG_PMKT-E-14549_21_002 — "Bạn không có quyền thực hiện tác vụ này"
Bất biến  —
Ghi chú   BR11 · bảng Validation dòng V17 (SCR:356): kiểm ở **Server**, thời điểm "Khi mở màn, khi Lưu".
          ⚠ AD02:26-27 tự mở rộng MSG_002 sang nhánh thiếu **quyền In** — UC02 NL2 và MSG:7 KHÔNG
          nói vậy. Không dùng MSG_002 cho nhánh thiếu quyền In; xem §Z mục thiếu quy định.
```

### R-TLMI-035 · Có quyền ở một chi nhánh là sửa được mẫu dùng chung cho mọi chi nhánh

```
Tầng      BE
Sev       P0
Nguồn     SCR:9 · SCR:247 · SCR:322 · UC01:11 · FB:7 · BR2P BR50.2
WHEN      người dùng có quyền Thiết lập mẫu in tại chi nhánh A và lưu mẫu
THEN      mẫu có hiệu lực ở MỌI chi nhánh còn lại (B, C…) — không có cảnh báo nào
Lỗi       —
Bất biến  INV-TLMI-011
Ghi chú   Bất đối xứng có chủ ý của tài liệu: **mẫu** dùng chung toàn tenant (FB:7) nhưng **quyền**
          xét theo chi nhánh đang làm việc (UC01:11). Tài liệu KHÔNG cấp message cảnh báo cho
          tình huống này — xem §Z.
```

---

## C. Kế thừa thiết lập chung

### R-TLMI-036 · Hai trạng thái theo chung / riêng

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:252 · SCR:267 · BR2P BR51.5
WHEN      xét một ô của nhóm Giấy và chữ, hoặc một trong bảy ô tick của khối Thông tin đầu trang
THEN      ô có ĐÚNG HAI trạng thái: **theo chung** (chưa sửa trong mẫu) / **riêng** (đã sửa)
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR2, BR4. Nguyên văn ví dụ của BA (SCR:252): "đơn vị đổi font chung từ Times New Roman
          sang Arial: mẫu Phiếu chi chưa sửa font sẽ in Arial; mẫu Chứng từ mua dịch vụ đã đặt
          font riêng Times New Roman vẫn in Times New Roman."
```

### R-TLMI-037 · Ô theo chung ghi trống (NULL) khi Lưu

```
Tầng      BE
Sev       P0
Nguồn     SCR:318
WHEN      Lưu AND một ô là **theo chung**
THEN      ghi **TRỐNG** vào cột tương ứng — KHÔNG ghi giá trị đang hiển thị
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR10, BR2. **Bẫy triển khai:** cột NULL ở đây là **sentinel "theo chung"**, không phải
          "chưa nhập". FE không đặt default trong Zod/TS cho nhóm cột này; BE không khai
          `nullable = false` kèm default. Cột "Bắt buộc = Y" ở SCR:93-101 là bắt buộc **giá trị
          hiệu dụng** sau fallback, không phải bắt buộc giá trị lưu.
```

### R-TLMI-038 · Ô theo chung đọc lại thiết lập chung tại thời điểm in / vẽ xem trước

```
Tầng      BE
Sev       P0
Nguồn     SCR:252 · SCR:306 · SCR:331
WHEN      in bản in, hoặc vẽ trang xem trước
THEN      ô theo chung lấy giá trị thiết lập chung **tại thời điểm đó** (COALESCE(mẫu, thiết lập chung));
          thiết lập chung đổi thì mẫu đổi theo
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR2, BR13. Đây là chỗ dễ code sai nhất của epic.
```

### R-TLMI-039 · Ô riêng giữ giá trị của mẫu

```
Tầng      BE
Sev       P0
Nguồn     SCR:252 · BR2P BR51.5
WHEN      người dùng ĐÃ sửa một ô của nhóm Giấy và chữ (hoặc một ô tick đầu trang)
THEN      ô là **riêng**: giữ giá trị của mẫu; thiết lập chung đổi cũng KHÔNG ảnh hưởng
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR2.
```

### R-TLMI-040 · Nút Theo thiết lập chung của nhóm Giấy và chữ

```
Tầng      FE
Sev       P1
Nguồn     SCR:102 · SCR:232 · SCR:253 · MT:71 · FIGMA (link đỏ "Theo thiết lập chung")
WHEN      người dùng bấm nút **Theo thiết lập chung** ở nhóm Giấy và chữ
THEN      CẢ NHÓM về theo chung — mọi ô của nhóm mất giá trị riêng
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR2.
```

### R-TLMI-041 · Bấm nút Theo thiết lập chung là một bước Hoàn tác được

```
Tầng      FE
Sev       P2
Nguồn     SCR:253
WHEN      người dùng bấm nút Theo thiết lập chung
THEN      thao tác đó là MỘT bước Hoàn tác được
Lỗi       —
Bất biến  —
Ghi chú   BR2, BR10. ⚠ Tài liệu KHÔNG nói **Đặt lại mẫu chuẩn** có phải bước Hoàn tác được không — xem §Z.
```

### R-TLMI-042 · Không có cách đưa riêng một ô về theo chung

```
Tầng      FE
Sev       P1
Nguồn     SCR:253
WHEN      người dùng muốn đưa RIÊNG MỘT ô về theo chung
THEN      không có cách nào — phải bấm nút cho cả nhóm rồi sửa lại các ô còn lại
Lỗi       —
Bất biến  —
Ghi chú   BR2. Hệ quả tiện dụng nặng, cộng với R-TLMI-045 (không có nhãn phân biệt) — xem §Z.
```

### R-TLMI-043 · Nút Theo thiết lập chung của khối Thông tin đầu trang

```
Tầng      FE
Sev       P1
Nguồn     SCR:126 · SCR:232 · SCR:267 · MT:77
WHEN      người dùng bấm nút **Theo thiết lập chung** ở khối Thông tin đầu trang
THEN      CẢ BẢY ô tick về theo chung
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR4, BR2.
```

### R-TLMI-044 · Đổi Khổ giấy / Hướng giấy trên thanh Xem trước làm ô đó trở thành riêng

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:68-69 · SCR:79 · SCR:256 · MT:67
WHEN      người dùng đổi Khổ giấy hoặc Hướng giấy **trên thanh Xem trước**
THEN      ô tương ứng ở mục Thiết lập mẫu đổi theo (CÙNG MỘT giá trị, cùng một trường)
          AND ô đó trở thành **riêng** — mẫu ngừng kế thừa thiết lập chung ở ô đó
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR2, BR8. ⚠ Thanh Xem trước luôn hiện ở cả 6 khối đang chọn (MT:67), nên một thao tác
          tưởng chỉ "để xem" có hậu quả vĩnh viễn. Tài liệu khẳng định rõ, không phải suy diễn;
          nhưng cần BA xác nhận là chủ ý — xem §Z.
```

### R-TLMI-045 · Trạng thái theo chung / riêng không có nhãn riêng từng ô

```
Tầng      FE
Sev       P1
Nguồn     MT:103 · SCR:253
WHEN      một ô đang ở trạng thái theo chung hay riêng
THEN      **không có nhãn riêng cho từng ô và không đổi Show/Hide** — người dùng không phân biệt
          được bằng mắt
Lỗi       —
Bất biến  —
Ghi chú   MT:103 nguyên văn: "BR2, BR4 — không có nhãn riêng cho từng ô và không đổi Show/Hide;
          nút Theo thiết lập chung áp cho cả nhóm."
```

### R-TLMI-046 · Người ký luôn theo thiết lập chung, TRỪ tiêu đề in ra

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:5 · SCR:257 · SCR:295 · SCR:298 · MT:89 · UC01:28 · UC02:23 · BR2P BR51.5 · FIGMA frame 6
Chốt      C04 · 04-quyet-dinh-ban-giao.md §3 · Dat · 2026-09-19

WHEN      cần người ký để dựng bản in
THEN      **Tên người ký** và cờ **"In tên người ký trên chứng từ, báo cáo"** LUÔN theo thiết lập
          chung — màn Thiết lập mẫu in chỉ đọc, không có ô sửa
ELSE      **Tiêu đề in ra** của ô ký (kể cả ô ký chức danh) **mẫu sửa riêng được**, theo đúng cơ chế
          theo-chung / riêng của nhóm Giấy và chữ (R-TLMI-036…039): chưa sửa ⇒ lấy Tiêu đề người ký
          của Thiết lập người ký tại lúc in; đã sửa ⇒ giữ giá trị của mẫu
Lỗi       —
Bất biến  INV-TLMI-003, INV-TLMI-010
Ghi chú   Tài liệu MÂU THUẪN TRONG CÙNG MỘT FILE `SCR`; đã chốt **cách (B)** cho riêng ô Tiêu đề in ra:
          (A) KHÔNG CHỌN · LUÔN THEO CHUNG, KHÔNG CÓ Ô SỬA — SCR:257 nguyên văn: "Không có ô ở màn
              này, luôn theo thiết lập chung: **người ký** (tiêu đề, tên, cờ in tên — Thiết lập
              người ký)…"; BR2P BR51.5: "người ký và ba quy tắc trên **luôn lấy từ thiết lập chung**"
              ⇒ mẫu KHÔNG lưu TieuDe; FE hiển thị read-only.
          (B) ĐÃ CHỌN · TIÊU ĐỀ IN RA SỬA ĐƯỢC RIÊNG CHO MẪU — SCR:295 nguyên văn: "(… tiêu đề và tên
              người ký lấy từ đó, **tiêu đề in ra sửa được riêng cho mẫu**)"; SCR:199 khai `TieuDe`
              bắt buộc, Cho phép sửa = **Y**; MT:89 cho "Tiêu đề in ra" = **Show** ở cột C6;
              Figma frame 6 vẽ đúng một **ô nhập** ở cột đó.
          Vì sao chọn (B):
            1. Ba nguồn độc lập đồng thuận (SCR:295 + SCR:199 bậc 4, MT:89 bậc 3, Figma bậc 1) —
               SCR:257 chỉ có một câu.
            2. SCR:257 là câu **liệt kê gộp** ("người ký (tiêu đề, tên, cờ in tên)"), còn SCR:295 là
               câu **đặc tả riêng** cho chính ô đó ⇒ câu đặc tả riêng thắng câu liệt kê gộp.
            3. BR51.5 nói "người ký … luôn lấy từ thiết lập chung" nhưng KHÔNG nói tiêu đề in ra
               trên bản in là bất biến ⇒ không phủ định (B).
          Phần KHÔNG đổi: tên người ký và cờ in tên vẫn luôn theo thiết lập chung — đúng cả (A) lẫn (B).
          Khác nhau đo được đã chọn: mẫu **CÓ** lưu TieuDe cho cả 5 chức danh; UI là TextField.
          Xem thêm R-TLMI-188.
```

### R-TLMI-047 · Ba quy tắc in chứng từ luôn theo thiết lập chung

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:5 · SCR:257 · SCR:334 · UC01:28 · UC02:23 · FB:9 · BR2P BR51.5
WHEN      áp ba quy tắc in chứng từ (cho phép in chứng từ **chưa ghi sổ** · cho phép in chứng từ
          **đã khóa sổ** · **cộng gộp mặt hàng** khi in)
THEN      LUÔN lấy theo thiết lập chung; màn Thiết lập mẫu in KHÔNG có ô chỉnh, mẫu KHÔNG lưu riêng
Lỗi       —
Bất biến  —
Ghi chú   BR2, BR13. Nội dung của chính ba quy tắc thuộc epic PMKT-E-14549_20 + BR51.5.
          Điều kiện cộng gộp đang bị C01 chặn — xem R-TLMI-119, R-TLMI-266.
```

### R-TLMI-048 · Mục "Bố cục mặc định của báo cáo" KHÔNG áp cho chứng từ

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:257 · SCR:274
WHEN      dựng bản in chứng từ
THEN      mục *Bố cục mặc định của báo cáo* của thiết lập chung (lặp tiêu đề cột, cột STT,
          cộng chuyển trang) **KHÔNG** áp
ELSE      mỗi khối Bảng tự có ba tùy chọn tương đương của nó — R-TLMI-096, R-TLMI-097, R-TLMI-099
Lỗi       —
Bất biến  —
Ghi chú   BR2, BR5.
```

### R-TLMI-049 · Định dạng khối đầu trang luôn theo thiết lập chung

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:267 · SCR:332
WHEN      in khối Thông tin đầu trang
THEN      kiểu chữ tên đơn vị · in hoa · kích thước logo · căn lề khối · lặp lại ở trang sau
          LUÔN theo thiết lập chung — màn này KHÔNG có ô chỉnh
Lỗi       —
Bất biến  —
Ghi chú   BR4, BR13. Phân biệt rõ với bảy ô tick *dòng nào in* (R-TLMI-077) — bảy ô đó sửa riêng được.
```

### R-TLMI-050 · Liên kết Mở Cấu hình báo cáo chứng từ

```
Tầng      FE
Sev       P2
Nguồn     SCR:103 · SCR:253 · MT:71 · FIGMA (link đỏ "Mở Cấu hình báo cáo chứng từ")
WHEN      người dùng bấm liên kết **Mở Cấu hình báo cáo chứng từ** ở mục Thiết lập mẫu
THEN      mở màn thiết lập chung ở **tab Quy tắc in chung**
Lỗi       —
Bất biến  —
Ghi chú   BR2. Màn đích thuộc epic PMKT-E-14549_20.
```

### R-TLMI-051 · Liên kết Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in

```
Tầng      FE
Sev       P2
Nguồn     SCR:127 · SCR:267 · MT:77
WHEN      người dùng bấm liên kết **Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in**
THEN      mở thẳng sang đúng mục đó để xem hoặc sửa
Lỗi       —
Bất biến  —
Ghi chú   BR4.
```

### R-TLMI-052 · Liên kết Mở Thiết lập người ký

```
Tầng      FE
Sev       P2
Nguồn     SCR:205 · SCR:298 · MT:92
WHEN      người dùng bấm liên kết **Mở Thiết lập người ký** ở khối Chữ ký
THEN      mở thẳng sang đó để đổi chức danh, tên người ký hoặc cờ "In tên người ký"
Lỗi       —
Bất biến  —
Ghi chú   BR6b. Màn đích: `TTC` (epic PMKT-E-14549_CauHinhBanDau).
```

---

## D. Giấy và chữ

### R-TLMI-053 · Nhóm Giấy và chữ luôn hiện đủ sáu ô kèm giá trị đang dùng

```
Tầng      FE
Sev       P1
Nguồn     SCR:87 · SCR:251 · SCR:93-101 · MT:71 · FIGMA (bảng chỉnh "Thiết lập mẫu")
WHEN      bảng chỉnh đang ở mục **Thiết lập mẫu**
THEN      nhóm **Giấy và chữ** hiện đủ: khổ giấy · hướng giấy (kèm số cột để tự động in ngang) ·
          lề bốn phía · font chữ · cỡ chữ; MỌI ô luôn hiện đủ kèm giá trị đang dùng
ELSE      ở năm mục còn lại (Thông tin đầu trang, Tiêu đề, Bảng, Khối tự do, Chữ ký) nhóm này **Hide**
Lỗi       —
Bất biến  —
Ghi chú   BR2 · MT:71.
```

### R-TLMI-054 · Khổ giấy chỉ nhận A3 / A4 / A5

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:93 · SCR:254
WHEN      chọn khổ giấy
THEN      chỉ nhận **A3 / A4 / A5**
ELSE      mặc định theo thiết lập chung; mặc định hệ thống = **A4**
Lỗi       —
Bất biến  —
Ghi chú   BR2. Ô này còn xuất hiện trên thanh Xem trước — cùng một trường (R-TLMI-044).
```

### R-TLMI-055 · Hướng giấy chỉ nhận Dọc / Ngang / Tự động

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:94 · SCR:254 · UC01:28
WHEN      chọn hướng giấy
THEN      chỉ nhận **Dọc / Ngang / Tự động**
ELSE      mặc định theo thiết lập chung; mặc định hệ thống = **Tự động**
Lỗi       —
Bất biến  —
Ghi chú   BR2.
```

### R-TLMI-056 · Hướng giấy = Tự động thì ô Số cột để tự động in ngang mới hiện

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:242 · MT:32 · MT:72 · MT:107
WHEN      Hướng giấy = **Tự động**
THEN      ô **Số cột để tự động in ngang** hiện (Show) và mới **bắt buộc** (`Y*`)
ELSE      Hướng giấy = Dọc hoặc Ngang ⇒ ô này **Hide**; giá trị đã nhập vẫn giữ
Lỗi       —
Bất biến  —
Ghi chú   BR2 · SCR:242 định nghĩa `Y*` = "Bắt buộc có điều kiện".
```

### R-TLMI-057 · Số cột để tự động in ngang là số nguyên 1–50

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:95 · SCR:254 · SCR:354 · MSG:36
WHEN      nhập Số cột để tự động in ngang (chỉ kiểm tra khi Hướng giấy = Tự động)
THEN      phải là số nguyên **1–50**; mặc định hệ thống = **7**
ELSE      báo MSG_PMKT-E-14549_21_214
Lỗi       MSG_PMKT-E-14549_21_214 — "Số cột để tự động in ngang phải là số nguyên từ 1 đến 50"
Bất biến  —
Ghi chú   BR2 · Validation V15 (SCR:354): Client / Server, khi rời ô và khi nhấn Lưu.
```

### R-TLMI-058 · Hướng Tự động với chứng từ: xét khối Bảng đang bật có nhiều cột in nhất

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:255 · BR2P BR51.5
WHEN      Hướng giấy = Tự động AND in chứng từ
THEN      xét khối Bảng **đang bật** có **nhiều cột in nhất** (KHÔNG tính cột STT):
            · số cột đó ≥ Số cột đã đặt  ⇒ in **ngang**
            · số cột đó <  Số cột đã đặt ⇒ in **dọc**
Lỗi       —
Bất biến  —
Ghi chú   BR2. BR chung nền BR51.5: "in ngang khi bảng đang in có nhiều cột nhất đạt số cột đã đặt".
          SCR:255 **chi tiết hóa** BR51.5 hai chỗ mà BR51.5 im lặng: không tính cột STT, và
          trường hợp không có bảng nào bật (R-TLMI-059). Chi tiết hóa, không trái BR.
          ⚠ KHÁC quy tắc Tự động của **báo cáo** (S20:180 xét "số cột đang hiển thị" của báo cáo) —
          đừng dùng chung code.
```

### R-TLMI-059 · Hướng Tự động mà không có khối Bảng nào đang bật thì in dọc

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:255
WHEN      Hướng giấy = Tự động AND KHÔNG có khối Bảng nào đang bật
THEN      in **dọc**
Lỗi       —
Bất biến  —
Ghi chú   BR2. BR51.5 im lặng về trường hợp này.
```

### R-TLMI-060 · Hướng Dọc hoặc Ngang thì in đúng hướng đó

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:255
WHEN      Hướng giấy = Dọc hoặc Ngang
THEN      in đúng hướng đó **bất kể số cột**
Lỗi       —
Bất biến  —
Ghi chú   BR2.
```

### R-TLMI-061 · Căn lề bốn phía là số 0–5 cm, tối đa một chữ số lẻ

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:96-99 · SCR:254 · SCR:353 · MSG:35
WHEN      nhập Căn lề trên / trái / dưới / phải
THEN      giá trị phải trong **0 – 5 cm** và **tối đa một chữ số lẻ**
ELSE      báo MSG_PMKT-E-14549_21_213
          Mặc định hệ thống: trên = **1** · trái = **1,5** · dưới = **1** · phải = **1**
Lỗi       MSG_PMKT-E-14549_21_213 — "Căn lề phải là số từ 0 đến 5 cm"
Bất biến  —
Ghi chú   BR2 · Validation V14 (SCR:353): Client / Server, khi rời ô và khi nhấn Lưu.
```

### R-TLMI-062 · Font chữ chỉ nhận Times New Roman hoặc Arial

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:100 · SCR:254
WHEN      chọn font chữ
THEN      chỉ nhận **Times New Roman** hoặc **Arial**
ELSE      mặc định theo thiết lập chung; mặc định hệ thống = **Times New Roman**
Lỗi       —
Bất biến  —
Ghi chú   BR2.
```

### R-TLMI-063 · Cỡ chữ là số nguyên 8–20, chỉ chặn phía máy chủ

```
Tầng      BE
Sev       P1
Nguồn     SCR:101 · SCR:254 · SCR:355 · MSG:37
WHEN      máy chủ nhận cỡ chữ
THEN      phải là số nguyên **8 – 20**; mặc định hệ thống = **12**
ELSE      báo MSG_PMKT-E-14549_21_215
Lỗi       MSG_PMKT-E-14549_21_215 — "Cỡ chữ phải là số nguyên từ 8 đến 20"
Bất biến  —
Ghi chú   BR2 · Validation V16 (SCR:355): tầng **Server**, thời điểm "Khi nhấn Lưu". Ô trên màn là
          danh sách chọn nên FE không cần kiểm — đây chỉ là chốt chặn server.
```

---

## E. Riêng của mẫu

### R-TLMI-064 · Màu chữ là giá trị riêng của mẫu, mặc định #000000

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:87 · SCR:104 · SCR:301 · SCR:310
WHEN      khởi tạo mẫu (kể cả sau Đặt lại mẫu chuẩn)
THEN      Màu chữ = **#000000** (đen) — là giá trị **riêng của mẫu**, KHÔNG kế thừa thiết lập chung
Lỗi       —
Bất biến  —
Ghi chú   BR7, BR9. Nhóm "Riêng của mẫu" (màu chữ, hình nền) nằm ngoài cơ chế theo chung / riêng.
```

### R-TLMI-065 · Màu chữ áp cho toàn bộ chữ và đường kẻ, trừ logo

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:301 · SCR:331
WHEN      dựng bản in theo mẫu
THEN      Màu chữ áp cho **toàn bộ chữ và đường kẻ** của bản in, **TRỪ logo**
Lỗi       —
Bất biến  —
Ghi chú   BR7, BR13.
```

### R-TLMI-066 · Chọn màu bằng 10 ô màu hoặc gõ mã #rrggbb

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:104 · SCR:301 · SCR:350 · MSG:32 · FIGMA (9 ô màu + ô nhập hex)
WHEN      chọn màu chữ
THEN      chọn một trong **10 ô màu** hoặc gõ mã dạng **`#rrggbb`**
ELSE      sai dạng ⇒ báo MSG_PMKT-E-14549_21_210
Lỗi       MSG_PMKT-E-14549_21_210 — "Mã màu phải có dạng #rrggbb"
Bất biến  —
Ghi chú   BR7 · Validation V11 (SCR:350): Client / Server, khi rời ô và khi Lưu.
          ⚠ Tài liệu KHÔNG liệt kê 10 mã màu cụ thể; Figma đếm được **9** ô màu preset + ô hex.
          Lệch số đếm 10 vs 9 — xem §Z.
```

### R-TLMI-067 · Kiểu hình nền = Không thì không in hình nền

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:105 · SCR:302
WHEN      Kiểu hình nền = **Không** (mặc định)
THEN      không in hình nền
Lỗi       —
Bất biến  —
Ghi chú   BR7.
```

### R-TLMI-068 · Kiểu hình nền = Khung viền thì kẻ khung quanh mép trang theo màu chữ

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:302 · FIGMA (frame 1b)
WHEN      Kiểu hình nền = **Khung viền**
THEN      kẻ khung quanh mép trang **theo màu chữ**
Lỗi       —
Bất biến  —
Ghi chú   BR7.
```

### R-TLMI-069 · Kiểu hình nền = Ảnh tải lên thì chọn tệp jpg/png ≤ 1MB

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:108 · SCR:302 · SCR:349 · MSG:31 · UC01:29
WHEN      Kiểu hình nền = **Ảnh tải lên** và người dùng chọn tệp
THEN      tệp phải là **jpg** hoặc **png**, dung lượng **≤ 1MB**
ELSE      báo MSG_PMKT-E-14549_21_209
Lỗi       MSG_PMKT-E-14549_21_209 — "Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB"
Bất biến  —
Ghi chú   BR7 · Validation V10 (SCR:349): Client / Server, thời điểm "Khi chọn tệp".
          ⚠ Tài liệu KHÔNG nói ảnh lưu ở cột / bảng nào trong 5 entity — xem §Z.
```

### R-TLMI-070 · Kiểu hình nền ≠ Không thì ô Độ đậm mới hiện và mới bắt buộc

```
Tầng      FE
Sev       P1
Nguồn     SCR:242 · SCR:106 · MT:26 · MT:75 · MT:101
WHEN      Kiểu hình nền ≠ Không (Khung viền hoặc Ảnh tải lên)
THEN      ô **Độ đậm** hiện (Show) và mới **bắt buộc** (`Y*`)
ELSE      Kiểu = Không ⇒ Độ đậm **Hide**
Lỗi       —
Bất biến  —
Ghi chú   BR7.
```

### R-TLMI-071 · Kiểu hình nền = Ảnh tải lên thì ô Căn ảnh và ô Ảnh mới hiện

```
Tầng      FE
Sev       P1
Nguồn     SCR:242 · SCR:107-108 · SCR:302 · MT:26 · MT:76 · MT:101 · FIGMA (frame 1 vs 1b)
WHEN      Kiểu hình nền = **Ảnh tải lên**
THEN      ô **Căn ảnh** và ô **Ảnh** hiện (Show) và mới **bắt buộc** (`Y*`)
ELSE      Kiểu = Không hoặc Khung viền ⇒ cả hai **Hide**
Lỗi       —
Bất biến  —
Ghi chú   BR7 · MT:101 nguyên văn: "Kiểu = Không thì cả ba ẩn; Khung viền chỉ hiện Độ đậm;
          Ảnh tải lên hiện đủ ba."
```

### R-TLMI-072 · Độ đậm 5–100 %, mặc định 20

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:106 · SCR:302
WHEN      nhập Độ đậm
THEN      giá trị **5 – 100 %**, mặc định **20**, áp cho **cả Khung viền lẫn Ảnh tải lên**
Lỗi       — (tài liệu KHÔNG cấp mã message cho vi phạm miền này — xem §Z)
Bất biến  —
Ghi chú   BR7. Bảng Validation 17 dòng KHÔNG có dòng nào cho Độ đậm.
```

### R-TLMI-073 · Căn ảnh = Giữa trang

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:107 · SCR:302
WHEN      Căn ảnh = **Giữa trang** (mặc định)
THEN      ảnh giữ tỷ lệ, chiếm khoảng nửa trang, nằm giữa
Lỗi       —
Bất biến  —
Ghi chú   BR7. "khoảng nửa trang" không có công thức — phát biểu không kiểm được (xem `00-source-map.md` §3).
```

### R-TLMI-074 · Căn ảnh = Toàn trang

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:302
WHEN      Căn ảnh = **Toàn trang**
THEN      kéo giãn ảnh phủ kín phần giấy **trong lề**
Lỗi       —
Bất biến  —
Ghi chú   BR7.
```

### R-TLMI-075 · Hình nền in dưới mọi khối

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:302 · SCR:331
WHEN      in hình nền
THEN      in **dưới mọi khối** và **không ảnh hưởng vị trí khối**
Lỗi       —
Bất biến  —
Ghi chú   BR7, BR13. Xem R-TLMI-263 (thứ tự dựng bản in).
```

---

## F. Khối Thông tin đầu trang

### R-TLMI-076 · Ô tick "In khối Thông tin đầu trang trên mẫu này"

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:118 · MT:77 · FIGMA (frame 4)
WHEN      dựng bảng chỉnh khối Thông tin đầu trang
THEN      có ô tick nguyên văn **"In khối Thông tin đầu trang trên mẫu này"**, ghi vào
          `cfg_mau_in_khoi.HienThi`, mặc định **Có**
Lỗi       —
Bất biến  —
Ghi chú   BR4. Cùng ý nghĩa với con mắt trên dòng khối (R-TLMI-207).
```

### R-TLMI-077 · Bảy ô tick dòng in, mặc định theo thiết lập chung

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:119-125 · SCR:267 · MT:77 · UC01:28
WHEN      quyết định dòng nào của Thông tin đầu trang được in
THEN      theo **bảy ô tick** của khối, mỗi ô theo cơ chế theo chung / riêng của BR2:
            · Tên đơn vị          `InTenDonVi`          mặc định hệ thống **Có**
            · Địa chỉ             `InDiaChi`            mặc định hệ thống **Có**
            · Mã số thuế          `InMST`               mặc định hệ thống **Có**
            · Số điện thoại       `InSoDienThoai`       mặc định hệ thống **Không**
            · Email               `InEmail`             mặc định hệ thống **Không**
            · Tài khoản ngân hàng `InTaiKhoanNganHang`  mặc định hệ thống **Không**
            · Logo                `InLogo`              mặc định hệ thống **Có** (đã chốt C03 — R-TLMI-082)
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR4, BR2. Ví dụ nguyên văn của BA (SCR:267): "thiết lập chung không in Số điện thoại
          nhưng mẫu Phiếu thu tick in → chỉ Phiếu thu có số điện thoại".
```

### R-TLMI-078 · Nội dung các dòng lấy từ hồ sơ đơn vị của chi nhánh ghi trên chứng từ

```
Tầng      BE
Sev       P0
Nguồn     SCR:267 · UC01:49 · UC02:41 · BR2P BR50.7
WHEN      in khối Thông tin đầu trang
THEN      nội dung các dòng (tên, địa chỉ, mã số thuế, điện thoại, email, tài khoản ngân hàng, logo)
          lấy từ hồ sơ đơn vị của **CHI NHÁNH GHI TRÊN CHỨNG TỪ** — tra `cfg_chi_nhanh` bằng
          `ChungTu.ChiNhanhId`
ELSE      KHÔNG dùng chi nhánh đang làm việc, KHÔNG đi ngược lên đơn vị cha
Lỗi       —
Bất biến  —
Ghi chú   BR4. BR chung nền **BR50.7** (Phase 2): "Thông tin in trên chứng từ, báo cáo, tờ khai lấy
          từ hồ sơ của chi nhánh ghi trên chính bản ghi đó. Xem hay in một chứng từ của chi nhánh
          khác thì vẫn ra đúng thông tin của chi nhánh đó."
          ⚠ Ngoại lệ tài liệu ghi rõ: **ảnh logo** nằm ở `cfg_tenant.Logo`, một logo dùng chung toàn
          đơn vị kế toán, **chi nhánh không có logo riêng** (TTC:129) ⇒ bản in của chi nhánh B mang
          logo của pháp nhân trong khi tên/địa chỉ/MST là của chi nhánh B. Đúng tài liệu, không phải bug.
```

### R-TLMI-079 · Dòng đã tick nhưng hồ sơ để trống thì bỏ qua dòng

```
Tầng      BE
Sev       P1
Nguồn     S20:127
WHEN      một dòng của khối Thông tin đầu trang được tick in nhưng hồ sơ đơn vị để trống
THEN      **bỏ qua dòng**, KHÔNG in một dòng trống
Lỗi       —
Bất biến  —
Ghi chú   Nguồn là màn thiết lập chung (epic _20) — khối đầu trang của chứng từ dùng lại quy tắc này.
```

### R-TLMI-080 · Bỏ tick cả bảy dòng thì khối không in gì

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:267 · SCR:315
WHEN      người dùng bỏ tick cả bảy dòng của Thông tin đầu trang
THEN      khối không in gì (giống như tắt con mắt) và đây **KHÔNG phải lỗi**
ELSE      không có cảnh báo mềm
Lỗi       —
Bất biến  —
Ghi chú   BR4, BR10.
```

### R-TLMI-081 · Mỗi dòng tick hiển thị kèm giá trị thật của chi nhánh ghi trên chứng từ

```
Tầng      FE
Sev       P1
Nguồn     SCR:131 · FIGMA (frame 4 — giá trị mờ dưới mỗi checkbox)
WHEN      hiển thị mỗi dòng tick của khối Thông tin đầu trang
THEN      kèm **giá trị thật của chi nhánh ghi trên chứng từ** (nguyên văn ví dụ của BA:
          "Địa chỉ: 12 Nguyễn Huệ, Q1, TP.HCM")
Lỗi       —
Bất biến  —
Ghi chú   BR4. Khác màn thiết lập chung (epic _20) vốn xem trước bằng hồ sơ **tổng công ty** (S20:148) —
          đừng dùng lại code xem trước của màn kia.
```

### R-TLMI-082 · Logo là một trong bảy ô tick mà mẫu sửa riêng được

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:125 · SCR:267 · MT:77 · BR2P BR51.5 · FIGMA frame 4
Chốt      C03 · 04-quyet-dinh-ban-giao.md §3 · Dat · 2026-09-19

WHEN      xét ô tick **Logo** ở khối Thông tin đầu trang
THEN      Logo **CÓ** nằm trong bảy ô tick mà mẫu sửa riêng được — mẫu lưu `InLogo` theo cơ chế
          theo-chung / riêng như sáu dòng còn lại (R-TLMI-036…039, R-TLMI-043)
ELSE      **kích thước logo** thì KHÔNG — luôn theo thiết lập chung (R-TLMI-049)
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   Tài liệu có HAI cách hiểu, đã chốt **cách (A) — Logo thuộc bảy ô tick**:
          (A) ĐÃ CHỌN · LOGO THUỘC BẢY Ô TICK — SCR:125 khai `InLogo`, Bắt buộc = Y,
              Cho phép sửa = **Y**, mặc định "Theo thiết lập chung (hệ thống: Có)";
              MT:77 gộp Logo vào dòng "7 ô tick dòng in (Tên đơn vị … Logo)" = **Show** ở cột C2;
              Figma frame 4 vẽ đúng **bảy** checkbox, ô cuối là Logo kèm giá trị mờ „[LOGO] cỡ vừa".
          (B) KHÔNG CHỌN · LOGO KHÔNG THUỘC — BR2P BR51.5 nguyên văn cho phép mẫu sửa riêng "dòng
              thông tin đơn vị nào in ở đầu trang"; **logo không phải một "dòng thông tin"**
              ⇒ không lưu `InLogo` trên mẫu; in logo hay không luôn theo thiết lập chung.
          Vì sao chọn (A):
            1. **Ba nguồn độc lập đồng thuận** — SCR:125 (bậc 4), MT:77 (bậc 3), Figma frame 4
               (bậc 1). BR51.5 chỉ có một cách diễn đạt gộp.
            2. BR51.5 **không phủ định** Logo; nó liệt kê thiếu chứ không viết "trừ logo".
               Liệt kê thiếu không đủ để loại một ô mà ba nguồn khác khai rõ.
            3. Epic thắng BR chung trong đúng phạm vi epic — và đây đúng là phạm vi epic _21.
          Khác nhau đo được đã chọn: mẫu **CÓ** trường `InLogo`; UI có **bảy** checkbox, không phải sáu.
```

### R-TLMI-083 · Thứ tự các dòng đầu trang cố định

```
Tầng      BE
Sev       P2
Nguồn     S20:128
WHEN      in khối Thông tin đầu trang
THEN      thứ tự các dòng **cố định**: Tên đơn vị, Địa chỉ, Mã số thuế, Số điện thoại, Email,
          Tài khoản ngân hàng
ELSE      không có ô cấu hình thứ tự
Lỗi       —
Bất biến  —
Ghi chú   Nguồn thuộc epic _20.
```

### R-TLMI-084 · Thiết lập chung bật lặp đầu trang thì khối lặp lại ở trang sau

```
Tầng      BE
Sev       P1
Nguồn     SCR:332 · SCR:267
WHEN      thiết lập chung bật "Lặp lại thông tin đơn vị ở các trang sau"
THEN      khối Thông tin đầu trang lặp lại ở trang sau
ELSE      mẫu KHÔNG có ô chỉnh cờ này (R-TLMI-049)
Lỗi       —
Bất biến  —
Ghi chú   BR13, BR4.
```

---

## G. Khối Tiêu đề

### R-TLMI-085 · Nội dung tiêu đề mặc định là tên loại chứng từ, không trống, tối đa 255 ký tự

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:139 · SCR:268 · SCR:340 · MSG:23 · FIGMA (frame 5)
WHEN      nhập ô **Nội dung** của khối Tiêu đề
THEN      không trống và tối đa **255 ký tự**; mặc định khi tạo mẫu chuẩn = **tên loại chứng từ**
          (ví dụ nguyên văn của BA: "Chứng từ mua dịch vụ")
ELSE      báo MSG_PMKT-E-14549_21_201
Lỗi       MSG_PMKT-E-14549_21_201 — "Tiêu đề bản in không được để trống, tối đa 255 ký tự"
Bất biến  —
Ghi chú   BR4 · Validation V01 (SCR:340): Client / Server, khi rời ô và khi nhấn Lưu.
          ⚠ Tài liệu KHÔNG nói ràng buộc này còn áp khi khối Tiêu đề bị **ẩn** (con mắt = Không) — xem §Z.
```

### R-TLMI-086 · Cỡ chữ tiêu đề là số nguyên 10–36, mặc định 18

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:140 · SCR:268 · SCR:341 · MSG:24
WHEN      nhập Cỡ chữ của khối Tiêu đề
THEN      phải là số nguyên **10 – 36**, mặc định **18**, **độc lập với cỡ chữ chung**
ELSE      báo MSG_PMKT-E-14549_21_202
Lỗi       MSG_PMKT-E-14549_21_202 — "Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36"
Bất biến  —
Ghi chú   BR4 · Validation V02 (SCR:341).
```

### R-TLMI-087 · Căn của khối Tiêu đề áp cho cả dòng tiêu đề và dòng ngày tháng

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:141 · SCR:268
WHEN      đặt Căn **Trái / Giữa / Phải** ở khối Tiêu đề (mặc định **Giữa**)
THEN      áp cho **CẢ** dòng tiêu đề và dòng ngày tháng
Lỗi       —
Bất biến  —
Ghi chú   BR4.
```

### R-TLMI-088 · IN HOA của khối Tiêu đề

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:142 · SCR:268
WHEN      IN HOA = **Có** (mặc định)
THEN      in toàn chữ hoa
ELSE      IN HOA = Không ⇒ in đúng như gõ
Lỗi       —
Bất biến  —
Ghi chú   BR4.
```

### R-TLMI-089 · In đậm của khối Tiêu đề

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:143 · SCR:268
WHEN      In đậm = **Có** (mặc định)
THEN      in đậm
ELSE      In đậm = Không ⇒ in thường
Lỗi       —
Bất biến  —
Ghi chú   BR4.
```

### R-TLMI-090 · Dòng ngày tháng in ngay dưới tiêu đề, lấy ngày chứng từ

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:144 · SCR:269 · FIGMA (frame 5 ghi chú) · BR2P BR51.5
WHEN      "Dòng ngày tháng ngay dưới tiêu đề" = **Có** (mặc định)
THEN      in ngay dưới tiêu đề một dòng **nghiêng** `Ngày <dd> tháng <mm> năm <yyyy>`, lấy
          **ngày chứng từ**
ELSE      = Không ⇒ không in dòng này
Lỗi       —
Bất biến  —
Ghi chú   BR4. BR chung nền BR51.5: "Ngày ký trên chứng từ luôn là ngày chứng từ" — chứng từ
          **không** theo cờ `NgayKyBaoCaoTheoCuoiKy` (cờ đó chỉ cho báo cáo, S20:169).
          Nguyên văn ghi chú Figma: „In nghiêng "Ngày 27 tháng 08 năm 2026" — lấy theo ngày chứng từ."
```

### R-TLMI-091 · Số chứng từ không thuộc khối Tiêu đề

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:269
WHEN      người dùng muốn in **Số chứng từ**
THEN      phải đưa trường Số chứng từ vào một **khối tự do**
ELSE      Số chứng từ KHÔNG thuộc khối Tiêu đề
Lỗi       —
Bất biến  —
Ghi chú   BR4, BR6. Số chứng từ và Ngày chứng từ đều nằm trong kho trường (R-TLMI-165).
```

---

## H. Khối Bảng

### R-TLMI-092 · Mỗi khối Bảng ứng đúng một lưới trên form

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:148 · SCR:272 · UC01:26
WHEN      dựng khối Bảng
THEN      mỗi khối Bảng ứng với ĐÚNG MỘT lưới trên form; cột của khối = **đúng và đủ** các cột của
          lưới đó; thứ tự gốc theo form
Lỗi       —
Bất biến  INV-TLMI-008
Ghi chú   BR5. Khóa kỹ thuật của lưới / cột / ô do đặc tả kỹ thuật quy định, tài liệu nghiệp vụ
          không liệt kê — SCR:260 mượn nguyên tắc của **BR51.6** (khóa duy nhất trong phạm vi,
          không đổi suốt vòng đời, không dùng lại khóa của cột đã bỏ).
```

### R-TLMI-093 · Cột thêm vào lưới ở phiên bản sau tự xuất hiện cuối bảng

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:272 · UC01:26
WHEN      một cột được thêm vào lưới ở phiên bản sau
THEN      cột tự xuất hiện ở **cuối bảng** và **mặc định in**; độ rộng các cột đang bật chia lại
          theo thuật toán của R-TLMI-114
Lỗi       —
Bất biến  INV-TLMI-005
Ghi chú   BR5. ⚠ Tài liệu KHÔNG nói việc chia lại này xảy ra **lúc nào** (mở màn / Lưu / in), và
          KHÔNG quy định nhánh ngược lại (cột bị **bỏ** khỏi lưới) — xem §Z.
```

### R-TLMI-094 · Tên bảng trống thì không in tên bảng

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:154 · SCR:273
WHEN      ô **Tên bảng in ra** để trống
THEN      không in tên bảng
ELSE      có nội dung ⇒ in một dòng **đậm** ngay trên bảng
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-095 · Tên bảng mặc định trống cho lưới đầu tiên

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:154 · SCR:273
WHEN      tạo mẫu chuẩn
THEN      Tên bảng in ra mặc định **trống** cho lưới **đầu tiên**, bằng **tên lưới** cho các lưới khác
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-096 · In cột STT

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:155 · SCR:274
WHEN      In cột STT = **Có** (mặc định)
THEN      thêm cột đầu tiên đánh số 1, 2, 3… theo dòng
ELSE      = Không ⇒ không có cột này
Lỗi       —
Bất biến  —
Ghi chú   BR5. Cột STT KHÔNG tính vào quy tắc Hướng giấy Tự động (R-TLMI-058).
```

### R-TLMI-097 · Dòng Cộng

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:156 · SCR:274
WHEN      Dòng Cộng = **Có** (mặc định)
THEN      dòng cuối bảng in chữ **"Tổng:"** và tổng của các cột được tick Cộng
Lỗi       —
Bất biến  —
Ghi chú   BR5. Chuỗi "Tổng:" là text hiển thị ⇒ phải có key i18n (luật 2).
```

### R-TLMI-098 · Dòng Cộng = Không

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:274
WHEN      Dòng Cộng = **Không**
THEN      không có dòng này AND các cột tick Cộng **không có tác dụng**
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-099 · Lặp tiêu đề mỗi trang

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:157 · SCR:274
WHEN      Lặp tiêu đề mỗi trang = **Có** (mặc định) AND bảng tràn trang
THEN      trang sau in lại dòng tiêu đề cột
ELSE      = Không ⇒ trang sau in tiếp dữ liệu, không có tiêu đề
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-100 · Kẻ ô Đầy đủ / Kẻ ngang

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:158 · SCR:275
WHEN      Kẻ ô = **Đầy đủ** (mặc định)
THEN      kẻ mọi đường ngang và dọc
ELSE      Kẻ ô = **Kẻ ngang** ⇒ chỉ kẻ đường ngang giữa các dòng, không kẻ đường dọc
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-101 · Tên cột dữ liệu chỉ đọc

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:162 · SCR:276 · MT:82
WHEN      hiển thị cột **Tên cột dữ liệu** trên lưới cột của khối Bảng
THEN      lấy theo **đặc tả form** và **chỉ đọc** (MT:82 — `Disable (at)`)
ELSE      KHÔNG phải cột lưu của mẫu
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-102 · Tên hiển thị của cột không trống, tối đa 100 ký tự

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:163 · SCR:276 · SCR:343 · MSG:26
WHEN      nhập **Tên hiển thị** của cột
THEN      không trống, tối đa **100 ký tự**; mặc định = Tên cột dữ liệu
ELSE      báo MSG_PMKT-E-14549_21_204
Lỗi       MSG_PMKT-E-14549_21_204 — "Tên hiển thị của cột không được để trống, tối đa 100 ký tự"
Bất biến  —
Ghi chú   BR5 · Validation V04 (SCR:343).
```

### R-TLMI-103 · Ô tick in của cột

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:161 · SCR:277
WHEN      ô tick in của cột = **Có** (mặc định)
THEN      cột in ra
ELSE      = Không ⇒ bỏ cột và các cột sau **dịch sang trái**
Lỗi       —
Bất biến  INV-TLMI-004
Ghi chú   BR5.
```

### R-TLMI-104 · Khối Bảng đang bật phải giữ lại ít nhất một cột hiển thị

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:277 · SCR:342 · MSG:25 · UC01:26
WHEN      khối Bảng đang bật AND người dùng bỏ tick cột **cuối cùng** còn lại
THEN      chặn — phải giữ ít nhất 1 cột hiển thị
Lỗi       MSG_PMKT-E-14549_21_203 — `Bảng "{TenBang}" phải giữ lại ít nhất 1 cột hiển thị`
          (tham số `{TenBang}`)
Bất biến  INV-TLMI-004
Ghi chú   BR5, BR10 · Validation V03 (SCR:342): Client / Server, "Khi bỏ tick cột, khi nhấn Lưu".
```

### R-TLMI-105 · Căn của cột

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:165 · SCR:277
WHEN      đặt Căn **Trái / Giữa / Phải** cho một cột
THEN      áp cho **CẢ** tiêu đề cột và dữ liệu
ELSE      mặc định: cột **số** ⇒ **Phải**; cột còn lại ⇒ **Trái**
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-106 · Chỉ cột số mới có ô Cộng

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:166 · SCR:277 · MT:83 · MT:84
WHEN      cột là **cột số**
THEN      cột mới có ô **Cộng** (Show); tick thì dòng Cộng ghi tổng của cột đó
ELSE      cột **chữ** ⇒ ô Cộng **Hide (at)** — ẩn tĩnh, không render
Lỗi       —
Bất biến  —
Ghi chú   BR5. MT:84 chốt hành vi cột chữ là **Hide**, không phải disable — dứt điểm khoảng trống
          mà SCR:166 để lại.
```

### R-TLMI-107 · Cộng mặc định Có với cột tiền

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:166
WHEN      khởi tạo cột
THEN      `CongODongCong` mặc định = **Có** với cột **tiền**, **Không** với cột khác
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-108 · Độ rộng cột là số nguyên 3–90

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:164 · SCR:242 · SCR:278 · SCR:344 · MSG:27
WHEN      nhập Độ rộng cột (Rộng %)
THEN      là **phần trăm bề ngang bảng**, số nguyên **3 – 90**; **bắt buộc** (`Y*`) với cột đang tick in
ELSE      báo MSG_PMKT-E-14549_21_205
Lỗi       MSG_PMKT-E-14549_21_205 — "Độ rộng cột phải là số nguyên từ 3 đến 90"
Bất biến  INV-TLMI-005
Ghi chú   BR5 · Validation V05 (SCR:344) · `Y*` định nghĩa ở SCR:242.
```

### R-TLMI-109 · Độ rộng mặc định lấy theo tỷ lệ độ rộng cột trên lưới form

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:164 · SCR:278
WHEN      tạo mẫu chuẩn
THEN      Độ rộng mặc định lấy theo **tỷ lệ độ rộng các cột trên lưới form**, quy về 100 theo
          thuật toán của R-TLMI-114
Lỗi       —
Bất biến  INV-TLMI-005
Ghi chú   BR5.
```

### R-TLMI-110 · Tổng độ rộng khác 100 thì dòng tổng dưới lưới cột báo số hiện tại

```
Tầng      FE
Sev       P2
Nguồn     SCR:278 · FIGMA (frame 2 — chân bảng cột)
WHEN      tổng độ rộng các cột **đang tick in** khác 100
THEN      dòng tổng dưới lưới cột báo số hiện tại kèm chú thích **"nên = 100%"**
Lỗi       —
Bất biến  —
Ghi chú   BR5. Nguyên văn Figma: „Tổng độ rộng cột đang **98%** (nên = 100%)" + link "Chia đều về 100%".
```

### R-TLMI-111 · Lưu mà tổng độ rộng khác 100 thì tự chia lại về 100

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:278 · SCR:314 · SCR:318
WHEN      bấm Lưu AND tổng độ rộng các cột đang tick in khác 100
THEN      hệ thống **tự chia lại về 100** theo R-TLMI-114
ELSE      **KHÔNG phải lỗi, KHÔNG chặn lưu**
Lỗi       —
Bất biến  INV-TLMI-005
Ghi chú   BR5, BR10. SCR:314 nói rõ tổng ≠ 100 không nằm trong danh sách chặn lưu.
```

### R-TLMI-112 · Cột bỏ tick in không tính vào tổng

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:278 · MT:108
WHEN      cột bị **bỏ tick in**
THEN      không tính vào tổng AND giữ nguyên số đang có (để trống nếu chưa từng đặt)
Lỗi       —
Bất biến  INV-TLMI-005
Ghi chú   BR5. MT:108 nguyên văn: "Cột bỏ tick in giữ nguyên số Rộng % đang có, có thể để trống."
          ⚠ Dòng chú thích MT:108 mở đầu bằng marker hỏng `\1`, không có neo trong thân ma trận — xem §Z.
```

### R-TLMI-113 · Tick lại một cột đang có độ rộng trống

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:278
WHEN      tick lại một cột đang có độ rộng **trống**
THEN      cột nhận phần chia của nút **Chia đều về 100%**
Lỗi       —
Bất biến  INV-TLMI-005
Ghi chú   BR5.
```

### R-TLMI-114 · Thuật toán chia đều về 100%

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:167 · SCR:233 · SCR:279
WHEN      chia lại độ rộng — ba dịp: bấm nút **Chia đều về 100%** · tự chia khi **Lưu** (R-TLMI-111) ·
          khi có **cột mới** ở phiên bản sau (R-TLMI-093)
THEN      thực hiện đúng bốn bước, theo thứ tự:
            1. Chỉ xét các cột **đang tick in**; cột bỏ tick giữ nguyên số cũ.
            2. rộng_mới = rộng_cũ ÷ tổng_rộng_cũ × 100, **làm tròn XUỐNG** về số nguyên.
            3. Còn thiếu để đủ 100 ⇒ cộng phần thiếu vào **cột đang in cuối cùng**.
            4. Sau khi chia, cột nào **nhỏ hơn 3** ⇒ nâng lên **3** và trừ phần nâng vào
               **cột rộng nhất**.
ELSE      **GIỮ NGUYÊN TỶ LỆ giữa các cột — KHÔNG chia bằng nhau.**
Lỗi       —
Bất biến  INV-TLMI-005
Ghi chú   BR5. Ba ví dụ nguyên văn của BA (SCR:279) dùng làm test:
            40/40/40      → 33/33/34
            50/30         → 62/38
            10/10/10/10   → 25/25/25/25
          ⚠ Tài liệu KHÔNG nói nút này áp cho mọi cột hay chỉ cột đang hiện khi lưới cột **đang lọc**
          bằng ô Tìm cột — xem §Z.
```

### R-TLMI-115 · Kéo thả đổi thứ tự cột

```
Tầng      FE
Sev       P1
Nguồn     SCR:160 · SCR:280 · MT:80
WHEN      người dùng kéo biểu tượng ⠿ ở lưới cột
THEN      đổi thứ tự cột (`cfg_mau_in_khoi_cot.ThuTu`)
ELSE      mặc định = thứ tự cột trên lưới của form
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-116 · Ô Tìm cột lọc không phân biệt dấu, không lưu

```
Tầng      FE
Sev       P2
Nguồn     SCR:159 · SCR:280
WHEN      người dùng gõ vào ô **Tìm cột**
THEN      lọc dòng trên lưới cột theo **Tên cột dữ liệu** và **Tên hiển thị**, **không phân biệt dấu**
ELSE      từ khóa **không lưu**
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-117 · Đang lọc ở ô Tìm cột thì không cho kéo thả cột

```
Tầng      FE
Sev       P2
Nguồn     SCR:280 · MT:30 · MT:80 · MT:105
WHEN      ô Tìm cột **có từ khóa**
THEN      biểu tượng kéo thả cột **Disable**
ELSE      xóa từ khóa thì dùng lại được
Lỗi       —
Bất biến  —
Ghi chú   BR5 · điều kiện phụ `(đk-LOC)` của ma trận.
```

### R-TLMI-118 · Lọc ở ô Tìm cột không đổi thiết lập của cột bị ẩn khỏi lưới

```
Tầng      FE
Sev       P1
Nguồn     SCR:280
WHEN      lọc ở ô Tìm cột
THEN      thiết lập của cột bị ẩn khỏi lưới **KHÔNG đổi**
Lỗi       —
Bất biến  —
Ghi chú   BR5.
```

### R-TLMI-119 · Cộng gộp mặt hàng áp trước khi dựng bảng

```
Tầng      BE
Sev       P0
Nguồn     SCR:281 · SCR:334 · UC02:41 · BR2P BR51.5 · S20:160-164
Chốt      C01 + C30 · 04-quyet-dinh-ban-giao.md §2, §4 · Dat · 2026-09-19

WHEN      thiết lập chung bật **Cộng gộp mặt hàng khi in**
          AND loại chứng từ ∈ { Hóa đơn, phiếu xuất kho, phiếu nhập kho }
THEN      gộp dòng **TRƯỚC** khi dựng bảng, rồi mới in theo các cột đã chọn.
          **Khóa gộp** = mã hàng + đơn vị tính + đơn giá + **thuế suất**
                       (+ số lô + hạn sử dụng, nếu vật tư theo dõi theo lô)
ELSE      loại chứng từ ngoài ba loại trên (Phiếu chi, Chứng từ mua dịch vụ…) ⇒ **KHÔNG gộp**
Lỗi       —
Bất biến  —
Ghi chú   Tài liệu có HAI cách hiểu về khóa gộp, đã chốt **cách (B) — CÓ tính thuế suất**:
          (A) KHÔNG CHỌN · KHÔNG TÍNH THUẾ SUẤT — BR2P BR51.5 nguyên văn: gộp các dòng "cùng
              **mã hàng, đơn vị tính, đơn giá** (và cùng **số lô, hạn sử dụng** nếu vật tư theo dõi
              theo lô)" — không nhắc thuế suất.
          (B) ĐÃ CHỌN · CÓ TÍNH THUẾ SUẤT — S20:160-162 (BR8 của epic _20): "cùng mã hàng, cùng đơn
              vị tính, cùng đơn giá **và cùng thuế suất**", kèm ví dụ phủ định rõ ràng: "Hai dòng …
              **khác thuế suất** thì **không gộp**, in thành hai dòng riêng."
          Vì sao chọn (B):
            1. S20 **chi tiết hơn** và có **ví dụ phủ định** — tức BA đã nghĩ tới đúng ca biên này.
            2. BR51.5 chỉ **liệt kê thiếu**, không viết "không xét thuế suất" ⇒ không phủ định (B).
            3. Gộp hai dòng khác thuế suất làm một buộc phải cộng dồn tiền thuế — sai số liệu kế toán
               trên chính bản in mà người dùng đối chiếu với hóa đơn.
          **Phạm vi cộng gộp — chốt riêng ở C30:** giữ giới hạn của BR51.5 + S20:160, chỉ áp cho
          **Hóa đơn, phiếu xuất kho, phiếu nhập kho**. SCR:281 không nhắc lại giới hạn này **không**
          có nghĩa mở rộng ra mọi chứng từ.
          Khác nhau đo được đã chọn: chứng từ có hai dòng cùng mã hàng, cùng đơn giá, **khác thuế
          suất** ⇒ in **hai dòng**.
```

---

## I. Khối tự do

### R-TLMI-120 · Bấm Thêm khối tự do mở hộp Đặt tên khối

```
Tầng      FE
Sev       P1
Nguồn     SCR:55 · SCR:59 · SCR:219 · SCR:284 · MT:65 · FIGMA (nút "+ Thêm khối tự do")
WHEN      người dùng bấm **Thêm khối tự do**
THEN      mở **hộp Đặt tên khối** với tên gợi ý sẵn `"Khối tự do <n>"`
Lỗi       —
Bất biến  INV-TLMI-006
Ghi chú   BR6. ⚠ Tài liệu KHÔNG định nghĩa `n` là gì (số khối hiện có + 1? số lớn nhất từng dùng + 1?) — xem §Z.
          Nút Thêm khối tự do luôn Show ở mọi khối đang chọn (MT:65).
```

### R-TLMI-121 · Tên khối tự do không trống, tối đa 60 ký tự

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:59 · SCR:177 · SCR:284 · SCR:345 · MSG:28
WHEN      nhập tên khối (trong hộp Đặt tên khối hoặc ở ô Tên khối)
THEN      không trống, tối đa **60 ký tự**
ELSE      báo MSG_PMKT-E-14549_21_206
Lỗi       MSG_PMKT-E-14549_21_206 — "Tên khối tự do không được để trống, tối đa 60 ký tự"
Bất biến  —
Ghi chú   BR6 · Validation V06 (SCR:345): Client / Server, "Trong hộp Đặt tên khối, khi rời ô, khi nhấn Lưu".
          ⚠ Tài liệu KHÔNG nói hai khối tự do có được **trùng tên** không — xem §Z.
```

### R-TLMI-122 · Khối tự do mới đặt ngay trước khối Chữ ký

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:51 · SCR:219 · SCR:284 · MSG:17
WHEN      bấm **Thêm** trong hộp Đặt tên khối
THEN      khối mới được chèn vào vị trí **ngay trước khối Chữ ký**
Lỗi       —
Bất biến  INV-TLMI-008
Ghi chú   BR6, BR3.
```

### R-TLMI-123 · Khối tự do mới là lưới 1 dòng × 2 cột toàn ô trống

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:59 · SCR:284
WHEN      khối tự do vừa được tạo
THEN      khối là lưới **1 dòng × 2 cột** toàn **ô trống**
Lỗi       —
Bất biến  INV-TLMI-006
Ghi chú   BR6.
```

### R-TLMI-124 · Thêm khối tự do thành công thì báo, mở bảng chỉnh và chọn sẵn ô đầu tiên

```
Tầng      FE
Sev       P2
Nguồn     SCR:59 · SCR:284 · SCR:364 · MSG:17
WHEN      thêm khối tự do thành công
THEN      hiển thị MSG_PMKT-E-14549_21_104
          AND mở ngay bảng chỉnh của khối đó
          AND chọn sẵn ô đầu tiên của khối trên trang xem trước
Lỗi       MSG_PMKT-E-14549_21_104 — "Đã thêm khối tự do trước Chữ ký. Nháy đúp một ô để chọn trường,
          hoặc kéo trường từ bảng bên phải thả vào ô"
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-125 · Mỗi mẫu tối đa 10 khối tự do

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:284 · SCR:346 · MSG:29 · UC01:24
WHEN      mẫu đã có **10** khối tự do AND người dùng bấm Thêm khối tự do
THEN      chặn
Lỗi       MSG_PMKT-E-14549_21_207 — "Mỗi mẫu tối đa 10 khối tự do"
Bất biến  INV-TLMI-006
Ghi chú   BR6 · Validation V07 (SCR:346): Client / Server, "Khi bấm Thêm khối tự do, khi Lưu".
```

### R-TLMI-126 · Tên khối tự do không in ra bản in

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:284
WHEN      in bản in
THEN      tên khối tự do **KHÔNG in ra** — chỉ dùng trong Bố cục mẫu và bảng chỉnh
Lỗi       —
Bất biến  —
Ghi chú   BR6. Figma vẽ nhãn tên khối nổi màu đỏ ở góc khối trên trang xem trước — đó là dấu hiệu
          trên màn, không in.
```

### R-TLMI-127 · Sửa tên khối tự do sau khi tạo

```
Tầng      FE
Sev       P1
Nguồn     SCR:53 · SCR:59 · SCR:177 · SCR:284 · SCR:345 · MT:86 · FIGMA frame 3
Chốt      C07 · 04-quyet-dinh-ban-giao.md §3 · Dat · 2026-09-19

WHEN      người dùng đặt hoặc đổi tên một khối tự do
THEN      sửa được ở **CẢ HAI chỗ**, cùng ghi vào **một trường** `TenKhoi`:
            1. hộp **Đặt tên khối** lúc bấm Thêm khối tự do (SCR:284, R-TLMI-120)
            2. ô **Tên khối** trên bảng chỉnh của khối (SCR:59, SCR:177, MT:86, Figma frame 3)
ELSE      không có chỗ thứ ba — KHÔNG sửa trực tiếp trên dòng khối ở Bố cục mẫu (SCR:53)
Lỗi       MSG_PMKT-E-14549_21_206 — ràng buộc ≤ 60 ký tự áp ở cả hai chỗ (R-TLMI-121)
Bất biến  —
Ghi chú   Tài liệu có HAI cách hiểu, đã chốt **cả hai chỗ đều sửa được (hợp (A) và (B))**:
          (A) ĐÃ CHỌN · CÓ Ô TÊN KHỐI Ở BẢNG CHỈNH — SCR:177 khai `TenKhoi`, TextField,
              Cho phép sửa = **Y**; SCR:59 "tên khối vẫn sửa được sau đó ở ô Tên khối trong bảng
              chỉnh"; SCR:53 "khối tự do: … chỉ sửa được ở ô Tên khối của bảng chỉnh";
              SCR:345 (Validation V06) ghi thời điểm kiểm tra gồm **"khi rời ô"** ⇒ có ô nhập;
              MT:86 cho "Tên khối" = **Show** ở cột C5; Figma frame 3 vẽ ô nhập đó.
          (B) ĐÃ CHỌN · ĐẶT TÊN LÚC THÊM — SCR:284 mô tả **hộp Đặt tên khối** khi bấm Thêm khối
              tự do; UC01:24 "thêm tối đa 10 khối tự do (**đặt tên ngay khi thêm**)".
          Vì sao chọn cả hai, không chọn một:
            1. Hai nhánh **không loại trừ nhau**. (B) nói về *lúc tạo*, (A) nói về *sau khi tạo* —
               SCR:59 ghép rõ hai thời điểm trong cùng một câu.
            2. Sáu nguồn ở (A) cộng Figma đều khai ô nhập; bỏ ô đó là bỏ đặc tả có sẵn.
            3. Bỏ hộp Đặt tên lúc thêm thì khối mới sinh ra không tên — mâu thuẫn R-TLMI-121
               (tên bắt buộc) và MSG_206.
          Khác nhau đo được đã chọn: bảng chỉnh khối tự do **CÓ** TextField "Tên khối"; API lưu mẫu
          nhận `TenKhoi` từ cả hai luồng, **không** cần endpoint đổi tên riêng.
```

### R-TLMI-128 · Bảng chỉnh khối tự do không có ô Kích thước lưới và không có cột Vị trí

```
Tầng      FE
Sev       P2
Nguồn     SCR:187 · SCR:284 · MT:102
WHEN      xem bảng chỉnh của khối tự do
THEN      **KHÔNG có** ô nhập số dòng / số cột, **KHÔNG có** ô Kích thước lưới, **KHÔNG có** cột Vị trí
ELSE      số dòng, số cột và vị trí của trường nhìn thẳng trên trang xem trước; đổi bằng các nút
          thêm / xóa dòng cột trên trang
Lỗi       —
Bất biến  —
Ghi chú   BR6 · MT:102 nguyên văn.
```

### R-TLMI-129 · Mỗi khối tự do tối đa 20 dòng

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:285 · SCR:347 · SCR:366 · MSG:30 · UC01:25
WHEN      người dùng bấm **+ Dòng trên** / **+ Dòng dưới** mà khối tự do đã đủ **20** dòng
THEN      chặn
Lỗi       MSG_PMKT-E-14549_21_208 — "Mỗi khối tự do tối đa 20 dòng"
Bất biến  INV-TLMI-006
Ghi chú   BR6 · Validation V08 (SCR:347): Client / Server, "Khi bấm + Dòng trên / + Dòng dưới, khi Lưu".
```

### R-TLMI-130 · Mỗi khối tự do tối đa 6 cột

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:285 · SCR:348 · SCR:366 · MSG:38 · UC01:25
WHEN      người dùng bấm **+ Cột trái** / **+ Cột phải** mà khối tự do đã đủ **6** cột
THEN      chặn
Lỗi       MSG_PMKT-E-14549_21_216 — "Mỗi khối tự do tối đa 6 cột"
Bất biến  INV-TLMI-006
Ghi chú   BR6 · Validation V09 (SCR:348).
```

### R-TLMI-131 · Các cột của khối tự do rộng bằng nhau

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:285 · SCR:332 · UC01:25
WHEN      in khối tự do
THEN      các cột rộng **bằng nhau** (2 cột = mỗi cột nửa bề ngang, 3 cột = một phần ba…)
ELSE      KHÔNG đặt độ rộng riêng cho từng cột của khối tự do
Lỗi       —
Bất biến  —
Ghi chú   BR6, BR13.
```

### R-TLMI-132 · Chọn ô và chọn vùng

```
Tầng      FE
Sev       P2
Nguồn     SCR:222 · SCR:285 · SCR:307
WHEN      người dùng bấm một ô trên trang xem trước
THEN      chọn ô đó
ELSE      giữ **Shift** và bấm một ô khác ⇒ chọn một **vùng chữ nhật**
Lỗi       —
Bất biến  —
Ghi chú   BR6, BR8.
```

### R-TLMI-133 · Thêm dòng / cột ngay cạnh ô đang chọn

```
Tầng      FE
Sev       P1
Nguồn     SCR:223 · SCR:224 · SCR:285
WHEN      bấm **+ Dòng trên** / **+ Dòng dưới** / **+ Cột trái** / **+ Cột phải**
THEN      thêm ngay cạnh ô đang chọn; ô mới là **ô trống**; ô đang chọn **giữ nguyên nội dung**
Lỗi       MSG_…_208 / MSG_…_216 khi chạm trần (R-TLMI-129, R-TLMI-130)
Bất biến  INV-TLMI-006
Ghi chú   BR6.
```

### R-TLMI-134 · Xóa dòng / Xóa cột

```
Tầng      FE
Sev       P1
Nguồn     SCR:225 · SCR:285
WHEN      bấm **Xóa dòng** / **Xóa cột**
THEN      xóa các dòng / cột mà **vùng chọn phủ**
Lỗi       —
Bất biến  INV-TLMI-006
Ghi chú   BR6. Đi qua ô gộp thì tách trước — R-TLMI-141.
```

### R-TLMI-135 · Khối tự do còn 1 dòng hoặc 1 cột thì nút − Dòng / − Cột mờ

```
Tầng      FE
Sev       P1
Nguồn     SCR:285 · MT:27 · MT:69 · MT:102
WHEN      khối tự do chỉ còn **1 dòng** (hoặc **1 cột**)
THEN      không xóa được nữa — nút **− Dòng** (hoặc **− Cột**) **Disable**
Lỗi       —
Bất biến  INV-TLMI-006
Ghi chú   BR6 · điều kiện phụ `(đk-NG)`. Đây là **sàn** của lưới: ≥1 dòng và ≥1 cột.
```

### R-TLMI-136 · Gộp ô

```
Tầng      FE
Sev       P1
Nguồn     SCR:226 · SCR:286 · UC01:25
WHEN      chọn vùng từ **2 ô trở lên** rồi bấm **Gộp ô**
THEN      vùng đó thành **một ô** chiếm nhiều dòng, nhiều cột
Lỗi       MSG_PMKT-E-14549_21_404 nếu vùng có ≥2 ô có nội dung (R-TLMI-138)
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-137 · Vùng chọn chạm ô đã gộp thì tự nới ra

```
Tầng      FE
Sev       P1
Nguồn     SCR:286
WHEN      vùng chọn chạm vào một ô **đã gộp**
THEN      vùng chọn **tự nới ra** cho trọn ô đã gộp đó
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-138 · Vùng gộp có từ 2 ô có nội dung thì hỏi trước

```
Tầng      FE
Sev       P1
Nguồn     SCR:286 · SCR:367 · MSG:47
WHEN      vùng gộp có từ **2 ô CÓ NỘI DUNG** trở lên
THEN      hỏi MSG_PMKT-E-14549_21_404; đồng ý mới gộp
Lỗi       MSG_PMKT-E-14549_21_404 — "Vùng chọn có {SoO} ô đang có nội dung. Gộp thì chỉ giữ nội dung
          của ô đầu tiên, các ô còn lại mất nội dung. Tiếp tục?" (tham số `{SoO}`)
Bất biến  —
Ghi chú   BR6. Tài liệu KHÔNG nêu tên hai nút của hộp xác nhận — xem §Z.
```

### R-TLMI-139 · Gộp ô giữ nội dung của ô đầu tiên có nội dung

```
Tầng      FE
Sev       P1
Nguồn     SCR:226 · SCR:286
WHEN      gộp ô
THEN      ô gộp giữ nội dung của **ô đầu tiên có nội dung** theo thứ tự **trái → phải, trên → xuống**;
          các ô còn lại **mất nội dung**
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-140 · Tách ô

```
Tầng      FE
Sev       P1
Nguồn     SCR:286
WHEN      bấm **Tách ô**
THEN      ô đã gộp trả về các ô đơn: nội dung ở **ô góc trên trái**, các ô còn lại trống
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-141 · Xóa dòng / cột đi qua ô gộp thì tách trước rồi mới xóa

```
Tầng      FE
Sev       P1
Nguồn     SCR:225 · SCR:286
WHEN      xóa dòng / cột đi qua một ô gộp
THEN      ô gộp được **tách trước** rồi mới xóa
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-142 · Thêm dòng / cột vào giữa ô gộp thì ô gộp rộng thêm

```
Tầng      FE
Sev       P1
Nguồn     SCR:286
WHEN      thêm dòng / cột vào **giữa** một ô gộp
THEN      ô gộp **rộng thêm** một dòng / cột
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-143 · Ô trống không in gì nhưng chiếm chỗ

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:287 · SCR:332 · UC02:24
WHEN      ô trong lưới khối tự do là **Ô trống**
THEN      không in gì, chỉ **chiếm chỗ** để các ô khác thẳng hàng
Lỗi       —
Bất biến  —
Ghi chú   BR6, BR13. Ô trống KHÔNG BAO GIỜ là lỗi — R-TLMI-236.
```

### R-TLMI-144 · Ô là một trường của form thì in dạng `Tên hiển thị: Giá trị`

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:287
WHEN      ô là **một trường của form**
THEN      giá trị lấy tự động từ chứng từ khi in, in dạng `Tên hiển thị: Giá trị`
          — **dấu ":" hệ thống tự thêm**, không nằm trong Tên hiển thị
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-145 · Tên hiển thị của trường bị xóa trống thì chỉ in giá trị

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:287 · FIGMA (placeholder „Trống = chỉ in giá…")
WHEN      Tên hiển thị của trường bị xóa **trống**
THEN      chỉ in giá trị — **không in nhãn, không in dấu ":"**
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-146 · Ô Chữ tự do in đúng chữ người dùng gõ

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:287
WHEN      ô là **Chữ tự do**
THEN      in **đúng chữ người dùng gõ**, không có giá trị kèm theo
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-147 · Gõ Chữ tự do ngay trong ô, tối đa 255 ký tự

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:287 · SCR:352 · MSG:34
WHEN      gõ Chữ tự do
THEN      gõ ngay trong ô trên trang xem trước (nháy đúp ô, **Enter** để xong), tối đa **255 ký tự**
ELSE      quá 255 ⇒ báo MSG_PMKT-E-14549_21_212
Lỗi       MSG_PMKT-E-14549_21_212 — "Tên hiển thị và chữ tự do tối đa 255 ký tự"
Bất biến  —
Ghi chú   BR6 · Validation V13 (SCR:352): Client / Server, khi rời ô và khi nhấn Lưu.
```

### R-TLMI-148 · Chọn Chữ tự do mà rời ô khi chưa gõ thì ô tự về Ô trống

```
Tầng      FE
Sev       P1
Nguồn     SCR:287 · SCR:314 · SCR:352
WHEN      ô đã chọn Chữ tự do mà người dùng rời ô khi **chưa gõ chữ**
THEN      ô **tự trở về Ô trống**
ELSE      **KHÔNG báo lỗi**
Lỗi       —
Bất biến  —
Ghi chú   BR6, BR10. Figma vẽ trạng thái lỗi „Ô: Chữ tự do chưa có nội dung — nháy đúp để gõ" — đó là
          trạng thái **trong lúc đang chỉnh**, không phải lỗi chặn lưu; SCR:314 chốt là không lỗi.
```

### R-TLMI-149 · Kéo dòng trường thả vào ô

```
Tầng      FE
Sev       P1
Nguồn     SCR:187 · SCR:230 · SCR:288 · UC01:25
WHEN      người dùng kéo một dòng trường ở bảng chỉnh thả vào một ô trên trang xem trước
THEN      trường được đặt vào ô đó
Lỗi       —
Bất biến  INV-TLMI-007
Ghi chú   BR6.
```

### R-TLMI-150 · Nháy đúp ô mở hộp chọn cạnh ô

```
Tầng      FE
Sev       P1
Nguồn     SCR:187 · SCR:228 · SCR:288
WHEN      người dùng nháy đúp ô (hoặc bấm nút **Chọn trường…**, hoặc nhấn **Enter**)
THEN      mở hộp chọn **cạnh ô**; hai mục đầu là *(Ô trống)* và *Chữ tự do*, tiếp theo là kho trường
Lỗi       —
Bất biến  —
Ghi chú   BR6. "cạnh ô" không định vị được chính xác — phát biểu không kiểm được.
```

### R-TLMI-151 · Gõ chữ trong hộp chọn trường thì lọc không phân biệt dấu

```
Tầng      FE
Sev       P2
Nguồn     SCR:288
WHEN      gõ chữ trong hộp chọn trường
THEN      lọc kho trường **không phân biệt dấu**
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-152 · Một trường chỉ ở một ô trong một khối

```
Tầng      FE
Sev       P1
Nguồn     SCR:288 · UC01:25
WHEN      một trường đã đặt ở một ô AND được đặt lại vào ô khác **trong cùng khối**
THEN      trường **chuyển** sang ô mới; ô cũ thành **ô trống**
ELSE      một trường chỉ ở một ô trong một khối
Lỗi       —
Bất biến  INV-TLMI-007
Ghi chú   BR6.
```

### R-TLMI-153 · Cùng một trường dùng ở nhiều khối tự do khác nhau được phép

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:288
WHEN      cùng một trường được dùng ở **nhiều khối tự do khác nhau**
THEN      được phép
Lỗi       —
Bất biến  INV-TLMI-007
Ghi chú   BR6. Ràng buộc "một ô" chỉ trong phạm vi MỘT khối.
```

### R-TLMI-154 · Kéo ô có nội dung thả lên ô khác thì hai ô đổi nội dung

```
Tầng      FE
Sev       P1
Nguồn     SCR:231 · SCR:288 · UC01:25
WHEN      kéo một ô có nội dung thả lên ô khác (kể cả sang **khối tự do khác**)
THEN      hai ô **đổi nội dung** cho nhau; kích thước gộp **giữ theo ô**
Lỗi       —
Bất biến  INV-TLMI-007
Ghi chú   BR6. ⚠ Tài liệu KHÔNG nói xử lý khi nội dung dài hơn chỗ chứa của ô đích — xem §Z.
```

### R-TLMI-155 · Xóa nội dung đưa các ô đang chọn về ô trống

```
Tầng      FE
Sev       P1
Nguồn     SCR:229 · SCR:288 · SCR:81
WHEN      bấm **Xóa nội dung** (hoặc phím **Delete**)
THEN      các ô đang chọn về **ô trống**
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-156 · Tên hiển thị và In đậm là thuộc tính CỦA TRƯỜNG, dùng chung cả mẫu

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:289 · UC01:25 · FB:15
WHEN      đặt **Tên hiển thị** hoặc **In đậm** cho một trường
THEN      áp cho **MỌI ô đang dùng trường đó, KỂ CẢ ở khối tự do khác**
ELSE      đây là thuộc tính **CỦA TRƯỜNG**, dùng chung cho cả mẫu — KHÔNG phải thuộc tính của ô
Lỗi       —
Bất biến  INV-TLMI-009
Ghi chú   BR6. Đối lập trực tiếp với **Căn** vốn đặt theo ô (R-TLMI-161).
          ⚠ Tài liệu KHÔNG nói kết quả khi bấm In đậm trên thanh công cụ với một vùng chọn có ô
          **khác loại nội dung** (vừa trường vừa Chữ tự do) — xem §Z.
```

### R-TLMI-157 · Tên hiển thị của trường tối đa 255 ký tự

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:181 · SCR:289 · SCR:352 · MSG:34
WHEN      nhập Tên hiển thị của trường trong kho trường
THEN      tối đa **255 ký tự**; mặc định = tên trường; không bắt buộc
ELSE      quá 255 ⇒ báo MSG_PMKT-E-14549_21_212
Lỗi       MSG_PMKT-E-14549_21_212 — "Tên hiển thị và chữ tự do tối đa 255 ký tự"
Bất biến  INV-TLMI-009
Ghi chú   BR6 · Validation V13 (SCR:352).
```

### R-TLMI-158 · Ô trường + In đậm thì chỉ đậm Tên hiển thị

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:182 · SCR:227 · SCR:289 · SCR:332 · UC01:25
WHEN      ô là trường dữ liệu AND In đậm = **Có**
THEN      **chỉ đậm Tên hiển thị**; **giá trị LUÔN in thường**
ELSE      In đậm mặc định = **Không**
Lỗi       —
Bất biến  INV-TLMI-009
Ghi chú   BR6, BR13.
```

### R-TLMI-159 · Ô Chữ tự do + In đậm thì đậm cả chữ

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:289
WHEN      ô là **Chữ tự do** AND In đậm = Có
THEN      đậm **cả chữ**
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-160 · Nghiêng áp cho cả ô

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:289 · SCR:79
WHEN      đặt **Nghiêng**
THEN      áp cho **cả ô** (nhãn và giá trị)
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-161 · Căn trong khối tự do đặt theo ô

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:289
WHEN      đặt Căn **Trái / Giữa / Phải** trong khối tự do
THEN      đặt **THEO Ô** — **KHÔNG theo trường**
Lỗi       —
Bất biến  —
Ghi chú   BR6. Khác Tên hiển thị và In đậm (R-TLMI-156) vốn theo trường.
```

### R-TLMI-162 · Chưa chọn ô nào thì mọi nút thanh công cụ đều mờ

```
Tầng      FE
Sev       P1
Nguồn     SCR:79 · SCR:227 · SCR:289 · MT:27 · MT:9 · MT:102
WHEN      đang chọn khối tự do nhưng **chưa chọn ô nào**
THEN      **MỌI nút** trên thanh công cụ khối tự do **Disable**, gồm cả In đậm · Nghiêng · Căn
Lỗi       —
Bất biến  —
Ghi chú   BR6 · điều kiện phụ `(đk-NG)`.
```

### R-TLMI-163 · Bấm In đậm / Nghiêng / Căn áp cho ô hoặc vùng đang chọn

```
Tầng      FE
Sev       P1
Nguồn     SCR:227 · SCR:289
WHEN      bấm **In đậm** · **Nghiêng** · **Căn** trên thanh công cụ
THEN      áp cho **ô hoặc vùng đang chọn**
Lỗi       —
Bất biến  —
Ghi chú   BR6. ⚠ Với In đậm, hành vi này va với R-TLMI-156 (thuộc tính của trường) — xem §Z.
```

### R-TLMI-164 · Trường chưa được đặt vào ô nào thì Tên hiển thị và In đậm không lưu

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:289
WHEN      một trường **chưa được đặt vào ô nào**
THEN      Tên hiển thị và In đậm của trường đó **KHÔNG lưu**; mở lại màn thì về mặc định
Lỗi       —
Bất biến  INV-TLMI-009
Ghi chú   BR6.
```

### R-TLMI-165 · Kho trường = mọi ô trên form trừ cột trong các lưới

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:187 · SCR:290 · UC01:25 · FB:15 · BR2P BR50.7
WHEN      dựng kho trường dữ liệu cho khối tự do
THEN      kho = **mọi ô trên form của nghiệp vụ TRỪ cột trong các lưới**, gồm:
            · ô nhập đầu form (gồm **Số chứng từ**, **Ngày chứng từ**)
            · ô tổng cuối form, kèm **Số tiền bằng chữ** đọc từ ô tổng thanh toán theo quy tắc
              đọc số chung
            · thông tin đơn vị (tên, địa chỉ, mã số thuế, điện thoại) của **chi nhánh ghi trên chứng từ**
Lỗi       —
Bất biến  —
Ghi chú   BR6. Nguồn khai báo kho trường là **đặc tả form của epic nghiệp vụ** (UC01:16) — epic _21
          không liệt kê. "quy tắc đọc số chung" không trích mã BR nào — xem §Z.
```

### R-TLMI-166 · Kho trường là danh sách phẳng, không chia nhóm

```
Tầng      FE
Sev       P2
Nguồn     SCR:187 · SCR:290 · UC01:25
WHEN      hiển thị kho trường
THEN      là **một danh sách phẳng, KHÔNG chia nhóm**, xếp theo **thứ tự các ô trên form**;
          mỗi dòng gồm tên trường + ô Tên hiển thị + ô In đậm
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-167 · Ô mới ở phiên bản sau tự vào kho trường nhưng không tự chen vào khối tự do

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:290
WHEN      form có ô mới ở phiên bản sau
THEN      ô đó **tự xuất hiện trong kho trường**
ELSE      **KHÔNG tự chen vào khối tự do**
Lỗi       —
Bất biến  —
Ghi chú   BR6. ⚠ Nhánh ngược lại (trường đã đặt trong ô nhưng bị **bỏ khỏi form**) KHÔNG được quy định — xem §Z.
```

### R-TLMI-168 · Ô Tìm kiếm của khối tự do lọc không phân biệt dấu

```
Tầng      FE
Sev       P1
Nguồn     SCR:178 · SCR:187
WHEN      người dùng gõ vào ô **Tìm kiếm** của khối tự do
THEN      lọc theo **tên trường** và **Tên hiển thị**, **không phân biệt dấu**
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-169 · Cột Trường dữ liệu luôn chỉ đọc

```
Tầng      FE
Sev       P1
Nguồn     SCR:180 · MT:88
WHEN      hiển thị cột **Trường dữ liệu** trong bảng chỉnh khối tự do
THEN      lấy theo đặc tả form và **chỉ đọc** (MT:88 — `Disable (at)`)
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-170 · Thanh công cụ khối tự do chỉ hiện khi đang chọn khối tự do

```
Tầng      FE
Sev       P1
Nguồn     SCR:23 · SCR:72 · SCR:79 · MT:68 · MT:69 · MT:70 · FIGMA (frame 3)
WHEN      đang chọn một **khối tự do**
THEN      thanh công cụ khối tự do hiện **ngay trên trang xem trước**, gồm nguyên văn các nút:
          `+ Dòng trên` · `+ Dòng dưới` · `+ Cột trái` · `+ Cột phải` · `− Dòng` · `− Cột` ·
          `Gộp ô` · `Tách ô` · `In đậm` · `Nghiêng` · `Trái / Giữa / Phải` · `Chọn trường…` ·
          `Xóa nội dung`
ELSE      không đang chọn khối tự do ⇒ **toàn bộ** thanh công cụ và menu chuột phải **Hide**
Lỗi       —
Bất biến  —
Ghi chú   BR6, BR8 · MT:68-70 (Hide ở C1–C4 và C6, Show (đk-NG) ở C5).
          Figma hiển thị thêm nhãn ngữ cảnh `{Tên khối} · ô dòng {r}, cột {c}` ở đầu thanh.
```

### R-TLMI-171 · Menu chuột phải có cùng tác dụng với thanh công cụ

```
Tầng      FE
Sev       P1
Nguồn     SCR:81 · SCR:285 · MT:70 · FIGMA (frame 3)
WHEN      người dùng dùng **menu chuột phải trên ô khối tự do**
THEN      các lệnh trong menu có **cùng tác dụng** với thanh công cụ; danh sách nguyên văn:
          `Chọn trường dữ liệu…` · `Xóa nội dung ô` · `Thêm dòng phía trên` · `Thêm dòng phía dưới` ·
          `Thêm cột bên trái` · `Thêm cột bên phải` · `Xóa dòng` · `Xóa cột` · `Gộp ô` · `Tách ô`
Lỗi       —
Bất biến  —
Ghi chú   BR6. Figma cho thấy menu chia **ba nhóm** ngăn cách: (chọn trường / xóa nội dung) —
          (thêm–xóa dòng cột) — (gộp / tách).
```

### R-TLMI-172 · Ô đang chọn là Chữ tự do thì lệnh đầu menu là "Sửa chữ"

```
Tầng      FE
Sev       P1
Nguồn     SCR:81
WHEN      ô đang chọn là ô **Chữ tự do**
THEN      lệnh đầu menu chuột phải hiển thị là **"Sửa chữ"** thay cho **"Chọn trường dữ liệu…"**
Lỗi       —
Bất biến  —
Ghi chú   BR6. Hai chuỗi này phải có key i18n riêng (luật 2).
```

### R-TLMI-173 · Phím tắt trong lưới

```
Tầng      FE
Sev       P2
Nguồn     SCR:81
WHEN      đang chọn ô trong lưới khối tự do
THEN      **mũi tên** ⇒ di chuyển ô đang chọn
          **Delete** ⇒ xóa nội dung ô
          **Enter** hoặc **F2** ⇒ mở chọn trường / sửa chữ
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-174 · Gộp ô và Tách ô bật/tắt theo vùng chọn

```
Tầng      FE
Sev       P1
Nguồn     SCR:285 · SCR:286 · MT:27 · MT:69 · MT:102
WHEN      vùng chọn có **≥ 2 ô**
THEN      nút **Gộp ô** Show; ngược lại Disable
ELSE      ô đang chọn là **ô đã gộp** ⇒ nút **Tách ô** Show; ngược lại Disable
Lỗi       —
Bất biến  —
Ghi chú   BR6 · điều kiện phụ `(đk-NG)`.
```

### R-TLMI-175 · Xóa khối tự do thì hỏi trước

```
Tầng      FE
Sev       P1
Nguồn     SCR:54 · SCR:183 · SCR:220 · SCR:292 · SCR:365 · MSG:46 · MT:64 · MT:86
WHEN      người dùng bấm **✕** ở dòng khối (Bố cục mẫu) hoặc nút **Xóa khối này** ở bảng chỉnh
THEN      hỏi MSG_PMKT-E-14549_21_403 trước khi xóa
Lỗi       MSG_PMKT-E-14549_21_403 — `Xóa khối "{TenKhoi}" cùng các ô trong đó?` (tham số `{TenKhoi}`)
Bất biến  —
Ghi chú   BR6, BR3. Chỉ khối tự do mới có nút xóa — R-TLMI-210, R-TLMI-211.
```

### R-TLMI-176 · Khối tự do đang bật mà mọi ô đều trống thì vẫn lưu được

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:292 · SCR:314
WHEN      khối tự do đang bật mà **mọi ô đều trống**
THEN      vẫn lưu được; bản in chừa một **khoảng trống bằng chiều cao các dòng**
Lỗi       —
Bất biến  —
Ghi chú   BR6, BR10.
```

### R-TLMI-177 · Bật Hiện lưới căn chỉnh

```
Tầng      FE
Sev       P2
Nguồn     SCR:291 · FIGMA (frame 3)
WHEN      bật ô tick **Hiện lưới căn chỉnh**
THEN      trên trang xem trước các ô của khối tự do được **kẻ đường phân ô**, và **ô trống đang chọn
          có chữ gợi ý** cách đưa nội dung vào
Lỗi       —
Bất biến  —
Ghi chú   BR6. ⚠ Tài liệu KHÔNG cho **nguyên văn** chữ gợi ý ⇒ `msg.sh` không có gì để đối chiếu — xem §Z.
```

### R-TLMI-178 · Dấu hiệu lưới căn chỉnh không in và không xuất PDF

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:291 · SCR:332 · UC01:25 · UC02:24 · FB:15
WHEN      in hoặc xuất PDF
THEN      các dấu hiệu của lưới căn chỉnh **KHÔNG in** và **KHÔNG xuất**
Lỗi       —
Bất biến  —
Ghi chú   BR6, BR13.
```

### R-TLMI-179 · Bỏ tick Hiện lưới căn chỉnh

```
Tầng      FE
Sev       P2
Nguồn     SCR:291
WHEN      bỏ tick **Hiện lưới căn chỉnh**
THEN      trang xem trước hiển thị **đúng như bản in**
Lỗi       —
Bất biến  —
Ghi chú   BR6.
```

### R-TLMI-180 · In ô gộp chiếm đúng số dòng, số cột đã gộp

```
Tầng      FE
Sev       P1
Nguồn     SCR:332
WHEN      in ô gộp trong khối tự do
THEN      ô chiếm **đúng số dòng, số cột đã gộp**
Lỗi       —
Bất biến  —
Ghi chú   BR13, BR6.
Tầng — vì sao FE
          Đây là luật **bố cục pixel**, không phải luật số liệu. Giai đoạn 1 **FE dựng bản in**
          (quyết định D3 · `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-api/00-ke-hoach-tong.md`),
          BE chỉ cấp mẫu + dữ liệu chứng từ.
          **Xem lại khi:** BE bắt đầu sinh PDF phía máy chủ ⇒ luật này chuyển về **BE** (hoặc CẢ HAI
          nếu giữ song song hai bộ dựng). Bảy luật cùng diện: R-TLMI-180 · 181 · 194 · 195 · 200 ·
          263 · 265 — đổi thì đổi cả bảy một lượt.
```

### R-TLMI-181 · Giá trị dài trong ô tự xuống dòng

```
Tầng      FE
Sev       P1
Nguồn     SCR:332
WHEN      giá trị trong một ô khối tự do dài
THEN      tự xuống dòng trong ô AND các ô **cùng hàng cao bằng nhau**
Lỗi       —
Bất biến  —
Ghi chú   BR13, BR6.
Tầng — vì sao FE
          Luật **bố cục pixel** (ngắt dòng, chiều cao hàng). Giai đoạn 1 **FE dựng bản in**
          (quyết định D3 của kế hoạch BE). **Xem lại khi** BE sinh PDF — xem ghi chú ở R-TLMI-180.
```

---

## K. Khối Chữ ký

### R-TLMI-182 · Danh sách ô ký gồm 5 chức danh và các ô ký tự do

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:195 · SCR:197 · SCR:295 · UC01:27 · FB:17 · FIGMA (frame 6)
WHEN      dựng khối Chữ ký
THEN      danh sách ô ký gồm **5 chức danh** của Thiết lập người ký (Giám đốc, Kế toán trưởng,
          Thủ kho, Thủ quỹ, Người lập phiếu) và các **ô ký tự do** do người dùng thêm
Lỗi       —
Bất biến  INV-TLMI-008
Ghi chú   BR6b. Danh sách 5 chức danh do màn **Thiết lập người ký** (`TTC`) khai, không phải epic _21.
```

### R-TLMI-183 · Thứ tự ô ký mặc định và kéo thả đổi được

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:195 · SCR:296 · SCR:297 · MT:89 · UC01:27
WHEN      khởi tạo khối Chữ ký
THEN      thứ tự ô ký mặc định = **Người lập phiếu, Kế toán trưởng, Giám đốc, Thủ kho, Thủ quỹ**
ELSE      kéo biểu tượng ⠿ để đổi thứ tự **trái → phải, trên → xuống**
Lỗi       —
Bất biến  —
Ghi chú   BR6b.
```

### R-TLMI-184 · Mặc định bật ba, tắt hai

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:196 · SCR:296
WHEN      tạo mẫu chuẩn
THEN      `HienThi` = **Có** cho Người lập phiếu, Kế toán trưởng, Giám đốc
          AND `HienThi` = **Không** cho Thủ kho, Thủ quỹ
Lỗi       —
Bất biến  —
Ghi chú   BR6b.
```

### R-TLMI-185 · Cột chức danh chỉ đọc; ô ký tự do mang nhãn "tự do"

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:197 · SCR:295 · MT:90 · MT:104
WHEN      hiển thị cột **chức danh** của ô ký
THEN      lấy 5 chức danh của Thiết lập người ký và **chỉ đọc** (MT:90 — `Disable (at)`)
ELSE      ô ký tự do ghi nhãn nguyên văn **"tự do"** thay cho chức danh
Lỗi       —
Bất biến  —
Ghi chú   BR6b.
```

### R-TLMI-186 · Chức danh có sẵn: Tên người ký chỉ đọc, không có nút xóa

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:198 · SCR:201 · SCR:295 · MT:91 · MT:104 · TTC:46-50
WHEN      ô ký là **chức danh có sẵn**
THEN      `TenNguoiKy` = tên của Thiết lập người ký và **chỉ đọc**
          AND **không có nút xóa** ô ký đó
Lỗi       —
Bất biến  —
Ghi chú   BR6b · điều kiện phụ `(đk-TD)`.
```

### R-TLMI-187 · Ô ký tự do: Tên người ký gõ tay được, có nút xóa

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:198 · SCR:201 · SCR:295 · MT:91 · MT:104
WHEN      ô ký là **ô ký tự do**
THEN      `TenNguoiKy` mặc định **trống** và **gõ tay được** (tùy chọn)
          AND có **nút xóa**
Lỗi       —
Bất biến  —
Ghi chú   BR6b · điều kiện phụ `(đk-TD)`. ⚠ Tài liệu KHÔNG cho giới hạn ký tự / tính bắt buộc của
          **Tên người ký** gõ tay và của **Dòng ghi chú** — xem §Z.
          Figma ghi gợi ý nguyên văn cho ô ký tự do: „VD: "Người nhận hàng", "Bên thuê"".
```

### R-TLMI-188 · Tiêu đề in ra bắt buộc, mặc định là Tiêu đề người ký của Thiết lập người ký

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:199 · SCR:257 · SCR:295 · MT:89 · BR2P BR51.5 · FIGMA frame 6
Chốt      C04 · 04-quyet-dinh-ban-giao.md §3 · Dat · 2026-09-19

WHEN      khởi tạo ô ký (cả 5 chức danh lẫn ô ký tự do)
THEN      `TieuDe` (Tiêu đề in ra) **bắt buộc** và **mẫu sửa riêng được** — ô nhập trên bảng chỉnh
ELSE      chưa sửa trong mẫu ⇒ theo chung: lấy **Tiêu đề người ký của Thiết lập người ký** tại lúc in
          (cơ chế theo-chung / riêng, R-TLMI-036…039); đã sửa ⇒ giữ giá trị của mẫu
Lỗi       MSG_PMKT-E-14549_21_211 — áp cho **ô ký tự do đang bật** (R-TLMI-189)
Bất biến  INV-TLMI-003, INV-TLMI-010
Ghi chú   Tài liệu MÂU THUẪN TRONG CÙNG MỘT FILE `SCR`; đã chốt **cách (B)**. Lý lẽ đầy đủ ở
          **R-TLMI-046**. Tóm tắt khác biệt đo được:
          (A) KHÔNG CHỌN — mẫu **không** lưu `TieuDe` cho 5 chức danh; UI read-only (theo SCR:257).
          (B) ĐÃ CHỌN — mẫu **CÓ** lưu `TieuDe`, sửa được; UI là TextField (SCR:199 Cho phép sửa = Y,
              SCR:295 "tiêu đề in ra sửa được riêng cho mẫu", MT:89 = Show, Figma frame 6 vẽ ô nhập).
          Với **ô ký tự do** thì cả hai bên vốn đã thống nhất: tiêu đề in ra do người dùng gõ, bắt buộc.
          Phần KHÔNG đổi sau khi chốt: **tên người ký** và cờ **"In tên người ký"** vẫn luôn theo
          thiết lập chung, chỉ đọc ở màn này (R-TLMI-186, R-TLMI-196).
```

### R-TLMI-189 · Ô ký tự do đang bật phải có tiêu đề in ra không trống, tối đa 60 ký tự

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:295 · SCR:351 · MSG:33
WHEN      ô ký là **ô ký tự do** AND đang bật (tick = Có)
THEN      Tiêu đề in ra không trống, tối đa **60 ký tự**
ELSE      báo MSG_PMKT-E-14549_21_211
Lỗi       MSG_PMKT-E-14549_21_211 — "Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự"
Bất biến  INV-TLMI-010
Ghi chú   BR6b, BR10 · Validation V12 (SCR:351): Client / Server, khi rời ô và khi nhấn Lưu.
```

### R-TLMI-190 · Dòng ghi chú mặc định

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:200 · SCR:296
WHEN      tạo mẫu chuẩn
THEN      `DongGhiChu` mặc định = **"(Ký, họ tên)"**; riêng **Giám đốc** = **"(Ký, họ tên, đóng dấu)"**
Lỗi       —
Bất biến  —
Ghi chú   BR6b. Hai chuỗi này là text in ra ⇒ phải có key i18n, giữ nguyên văn tiếng Việt (luật 2).
          ⚠ Tài liệu KHÔNG nói dòng ghi chú của **5 chức danh chuẩn** có sửa được trong mẫu không
          (SCR:200 khai Cho phép sửa = Y, nhưng SCR:295 chỉ nói "tiêu đề in ra sửa được") — xem §Z.
```

### R-TLMI-191 · Ô tick của ô ký quyết định in hay không in

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:196 · SCR:295 · MT:89
WHEN      ô tick của một ô ký = **Có**
THEN      ô ký in ra
ELSE      = Không ⇒ không in
Lỗi       —
Bất biến  INV-TLMI-010
Ghi chú   BR6b.
```

### R-TLMI-192 · Ô ký tự do xóa được; chức danh chỉ tắt được

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:201 · SCR:295 · MT:91 · MT:104
WHEN      ô ký là **ô ký tự do**
THEN      xóa được
ELSE      là **chức danh của Thiết lập người ký** ⇒ **chỉ tắt được, KHÔNG xóa được**
Lỗi       —
Bất biến  —
Ghi chú   BR6b.
```

### R-TLMI-193 · Thêm ô ký tự do — không giới hạn số ô ký

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:202 · SCR:297 · MT:93 · UC01:27
WHEN      người dùng bấm **Thêm ô ký tự do**
THEN      thêm một ô ký loại tự do vào khối Chữ ký
ELSE      **KHÔNG giới hạn số ô ký**
Lỗi       —
Bất biến  —
Ghi chú   BR6b. Đối lập với khối tự do (trần 10 khối, 20 dòng, 6 cột).
```

### R-TLMI-194 · In khối Chữ ký chia đều, mỗi ô rộng tối thiểu 4 cm

```
Tầng      FE
Sev       P1
Nguồn     SCR:297 · UC01:27
WHEN      in khối Chữ ký
THEN      chia đều các ô **đang bật** theo bề ngang; mỗi ô rộng **tối thiểu 4 cm**
Lỗi       —
Bất biến  —
Ghi chú   BR6b. ⚠ Tài liệu KHÔNG nói xử lý khi bề ngang còn lại < 4 cm với **một** ô duy nhất, hay
          khi lề lớn khiến bề ngang < 4 cm — xem §Z.
Tầng — vì sao FE
          Luật **bố cục pixel** (chia bề ngang theo cm). Giai đoạn 1 **FE dựng bản in**
          (quyết định D3 của kế hoạch BE). **Xem lại khi** BE sinh PDF — xem ghi chú ở R-TLMI-180.
```

### R-TLMI-195 · Hàng ô ký hết chỗ thì ô tiếp theo tự xuống hàng

```
Tầng      FE
Sev       P1
Nguồn     SCR:297 · UC01:27
WHEN      một hàng ô ký hết chỗ
THEN      ô tiếp theo **tự xuống hàng** và hàng mới lại chia đều
Lỗi       —
Bất biến  —
Ghi chú   BR6b. Ví dụ nguyên văn của BA: A4 dọc lề 1,5 + 1 cm còn 17,5 cm ⇒ 4 ô một hàng, ô thứ 5 xuống hàng.
Tầng — vì sao FE
          Luật **bố cục pixel** (xuống hàng theo bề ngang còn lại). Giai đoạn 1 **FE dựng bản in**
          (quyết định D3 của kế hoạch BE). **Xem lại khi** BE sinh PDF — xem ghi chú ở R-TLMI-180.
```

### R-TLMI-196 · In tên người ký theo cờ của Thiết lập người ký

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:298 · UC02:23 · TTC:60 · FIGMA (hộp ghi chú frame 6)
WHEN      in tên người ký
THEN      theo cờ **"In tên người ký trên chứng từ, báo cáo"** của Thiết lập người ký
ELSE      cờ này **chỉ đọc** ở màn Thiết lập mẫu in
Lỗi       —
Bất biến  —
Ghi chú   BR6b. Nguyên văn hộp ghi chú Figma: „Tên người ký in ra hay không theo cờ "In tên người ký"
          ở Thiết lập người ký (đang: Có). Đổi chức danh, tên người ký tại đó."
          Cờ này nằm trên `cfg_chi_nhanh` ⇒ khác nhau giữa các chi nhánh; đọc theo **chi nhánh ghi
          trên chứng từ** — đã chốt C05, xem R-TLMI-199.
```

### R-TLMI-197 · Dòng "Ngày … tháng … năm …" của khối Chữ ký

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:203 · SCR:298 · UC01:27 · BR2P BR51.5
WHEN      Dòng "Ngày … tháng … năm …" = **Có** (bắt buộc, mặc định Có)
THEN      in một dòng **nghiêng, căn phải, phía trên các ô ký**, lấy **ngày chứng từ**
ELSE      = Không ⇒ không in dòng này
Lỗi       —
Bất biến  —
Ghi chú   BR6b. BR chung nền BR51.5: "Ngày ký trên chứng từ luôn là ngày chứng từ" — không theo cờ
          `NgayKyBaoCaoTheoCuoiKy` của báo cáo (S20:169).
```

### R-TLMI-198 · Chỗ trống ký Thấp / Vừa / Cao

```
Tầng      CẢ HAI
Sev       P2
Nguồn     SCR:204 · SCR:298
WHEN      Chỗ trống ký = **Thấp / Vừa / Cao** (bắt buộc, mặc định **Vừa**)
THEN      khoảng trống để ký khoảng **1 / 2 / 3 cm** tương ứng
Lỗi       —
Bất biến  —
Ghi chú   BR6b. Có chữ "khoảng", không có dung sai — phát biểu không kiểm được chính xác.
```

### R-TLMI-199 · Khối Chữ ký đọc hồ sơ đơn vị của chi nhánh nào

```
Tầng      BE
Sev       P1
Nguồn     SCR:295 · SCR:296 · SCR:297 · SCR:298 · TTC:46-50 · TTC:60 · BR2P BR50.7 · UC01:49 · UC02:41
Chốt      C05 · 04-quyet-dinh-ban-giao.md §3 · Dat · 2026-09-19

WHEN      dựng khối Chữ ký (tên người ký của 5 chức danh, cờ "In tên người ký", tiêu đề người ký)
THEN      đọc hồ sơ đơn vị của **CHI NHÁNH GHI TRÊN CHỨNG TỪ** — giống khối Thông tin đầu trang
          (R-TLMI-078), qua cổng duy nhất `HoSoDonViPort.theoChiNhanh(chiNhanhId)`
ELSE      **KHÔNG** dùng chi nhánh đang làm việc
Lỗi       —
Bất biến  —
Ghi chú   Gốc của tranh chấp: các cột `TieuDeNguoiKy*`, `TenNguoiKy*`, `InTenNguoiKyTrenChungTu`,
          `LayTenNguoiLapPhieuTuNguoiDungDangNhap` nằm trên **`cfg_chi_nhanh`** (TTC:46-50, TTC:60-61)
          ⇒ **khác nhau giữa các chi nhánh** — trong khi mẫu in dùng chung toàn tenant (R-TLMI-005).
          SCR:295-298 nói lấy "từ Thiết lập người ký" nhưng **KHÔNG nói theo chi nhánh nào**.
          Hai cách hiểu, đã chốt **cách (A)**:
          (A) ĐÃ CHỌN · CHI NHÁNH GHI TRÊN CHỨNG TỪ — nhất quán với khối Thông tin đầu trang
              (R-TLMI-078) và với BR50.7: "Thông tin in trên chứng từ … lấy từ hồ sơ của chi nhánh
              ghi trên chính bản ghi đó"; UC01:49 / UC02:41 đọc hồ sơ đơn vị và người ký "của
              **chi nhánh ghi trên chứng từ**".
          (B) KHÔNG CHỌN · CHI NHÁNH ĐANG LÀM VIỆC — không nguồn nào nói thẳng; chỉ là cách hiểu
              mặc định của nhiều màn khác.
          Vì sao chọn (A):
            1. UC01:49 và UC02:41 **đã nói thẳng** "chi nhánh ghi trên chứng từ" cho bước đọc
               `cfg_chi_nhanh` — mà người ký nằm chính trên bảng đó.
            2. BR50.7 là luật nền và nói phổ quát cho "chứng từ, báo cáo, tờ khai", không loại trừ
               khối Chữ ký.
            3. Tiêu chí quyết định: **in lại một chứng từ cũ ở chi nhánh khác phải ra CÙNG MỘT bản
               in**. Với (B), cùng một chứng từ in ở hai nơi ra hai bản khác nhau — không chấp nhận
               được với chứng từ kế toán.
            4. Giữ đúng một quy tắc cho cả hai khối đọc hồ sơ đơn vị (đầu trang + chữ ký), không
               có ngoại lệ phải nhớ.
          Khác nhau đo được đã chọn: truy vấn hồ sơ đơn vị nhận `ChungTu.ChiNhanhId`, không nhận
          chi nhánh phiên làm việc.
          ⚠ Bản hiện tại: `cfg_chi_nhanh` chưa tồn tại trong repo ⇒ cổng
          `HoSoDonViPort.theoChiNhanh()` tạm trả hồ sơ của tenant (điểm nối Q-14 ở
          `04-quyet-dinh-ban-giao.md §6`). Khi `cfg_chi_nhanh` ra đời thì **chỉ đổi phần hiện thực
          của cổng**, không đụng khối Chữ ký, khối đầu trang hay tầng dựng bản in.
```

### R-TLMI-200 · Cuối trang không đủ chỗ thì cả khối Chữ ký sang trang mới

```
Tầng      FE
Sev       P1
Nguồn     SCR:333
WHEN      cuối trang không đủ chỗ cho **cả** khối Chữ ký
THEN      cả khối sang trang mới — khối Chữ ký **KHÔNG bị cắt đôi** giữa hai trang
Lỗi       —
Bất biến  —
Ghi chú   BR13, BR6b.
Tầng — vì sao FE
          Luật **ngắt trang**, thuộc tầng dựng bản in. Giai đoạn 1 **FE dựng bản in**
          (quyết định D3 của kế hoạch BE). **Xem lại khi** BE sinh PDF — xem ghi chú ở R-TLMI-180.
```

---

## L. Bố cục mẫu

### R-TLMI-201 · Cột trái là Bố cục mẫu

```
Tầng      FE
Sev       P1
Nguồn     SCR:18 · SCR:20-24 · SCR:22 · MT:63 · MT:65 · FIGMA (cột "BỐ CỤC MẪU")
WHEN      dựng màn Thiết lập mẫu in
THEN      màn là **toàn trang**, ba cột Trái / Giữa / Phải; cột trái là **Bố cục mẫu**: danh sách khối
          theo **thứ tự in**, **kéo thả được**, kèm nút **Thêm khối tự do**
Lỗi       —
Bất biến  —
Ghi chú   BR3. Tiêu đề màn: `"Thiết lập mẫu in: <Tên loại chứng từ>"` (SCR:36) — xem R-TLMI-245.
          Figma còn vẽ khối chú thích cuối cột (hai gạch đầu dòng) — text hiển thị, phải có key i18n.
```

### R-TLMI-202 · Mục đầu danh sách là "Thiết lập mẫu", không kéo được

```
Tầng      FE
Sev       P1
Nguồn     SCR:50 · SCR:215 · SCR:261 · MT:71 · FIGMA (dòng bánh răng "Thiết lập mẫu")
WHEN      dựng danh sách khối
THEN      **mục đầu danh sách** là mục chọn **"Thiết lập mẫu"** — KHÔNG phải một khối
          AND bấm vào nó ⇒ mở bảng chỉnh "Thiết lập mẫu"
ELSE      mục này **không kéo được**
Lỗi       —
Bất biến  —
Ghi chú   BR2, BR3.
```

### R-TLMI-203 · Dòng khối chỉ có ba thành phần

```
Tầng      FE
Sev       P2
Nguồn     SCR:51-54 · SCR:261 · MT:63 · MT:64
WHEN      hiển thị một dòng khối trong Bố cục mẫu
THEN      dòng chỉ có **biểu tượng kéo**, **con mắt**, **tên khối** (và **nút xóa** với khối tự do),
          cộng dấu hiệu lỗi khi khối có ô không hợp lệ
ELSE      **KHÔNG ghi** số dòng / số cột / số ô
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-204 · Kéo ⠿ của dòng khối để đổi thứ tự khối

```
Tầng      FE
Sev       P1
Nguồn     SCR:51 · SCR:217 · SCR:261
WHEN      người dùng kéo biểu tượng ⠿ của một dòng khối thả vào vị trí mới
THEN      `cfg_mau_in_khoi.ThuTu` đổi theo vị trí thả — thứ tự khối = **thứ tự in**
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-205 · Kéo khối trên trang xem trước cho cùng kết quả

```
Tầng      FE
Sev       P1
Nguồn     SCR:217 · SCR:261 · SCR:307 · UC01:24 · UC01:30
WHEN      người dùng nắm một khối trên trang xem trước kéo thả lên khối khác
THEN      khối đang kéo chuyển vào vị trí của khối đó — **cùng kết quả** với kéo ở Bố cục mẫu
Lỗi       —
Bất biến  —
Ghi chú   BR3, BR8. ⚠ Tài liệu chỉ khẳng định "hai cách cho cùng kết quả", KHÔNG nói kết quả chuẩn khi
          thả vào **giữa** hai khối hay thả ra ngoài vùng khối — phát biểu không kiểm được, xem §Z.
```

### R-TLMI-206 · Mọi khối đều kéo được

```
Tầng      FE
Sev       P1
Nguồn     SCR:261 · UC01:24
WHEN      kéo **bất kỳ** khối nào, **kể cả Thông tin đầu trang và Chữ ký**
THEN      đều kéo được để đổi thứ tự
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-207 · Con mắt của khối = Có thì khối được in ra

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:52 · SCR:262 · MT:63
WHEN      con mắt của khối = **Có** (mặc định)
THEN      khối được in ra
Lỗi       —
Bất biến  —
Ghi chú   BR3. Với khối Thông tin đầu trang, cùng một trường với ô tick ở bảng chỉnh (R-TLMI-076).
```

### R-TLMI-208 · Con mắt = Không thì khối không in và các khối sau dồn lên

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:262
WHEN      con mắt của khối = **Không**
THEN      khối không in AND các khối sau **dồn lên**, KHÔNG chừa khoảng trống
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-209 · Tắt con mắt không mất thiết lập bên trong khối

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:262
WHEN      khối bị tắt con mắt
THEN      thiết lập bên trong khối **vẫn giữ nguyên**; bật lại là in như cũ
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-210 · Khối chuẩn không xóa được

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:263 · UC01:24 · MT:34 · MT:64 · MT:100
WHEN      khối là **khối chuẩn** (Thông tin đầu trang, Tiêu đề, Bảng, Chữ ký)
THEN      **KHÔNG xóa được**, chỉ ẩn được bằng con mắt
ELSE      nút xóa khối **Hide** (ẩn hẳn)
Lỗi       —
Bất biến  INV-TLMI-008
Ghi chú   BR3 · điều kiện phụ `(đk-KT)`.
```

### R-TLMI-211 · Khối tự do có nút xóa ở cả hai nơi

```
Tầng      FE
Sev       P1
Nguồn     SCR:54 · SCR:183 · MT:64 · MT:86 · MT:100
WHEN      khối là **khối tự do**
THEN      nút xóa **Show** ở **cả** Bố cục mẫu (✕ trên dòng khối) **lẫn** bảng chỉnh (nút "Xóa khối này")
Lỗi       MSG_PMKT-E-14549_21_403 (R-TLMI-175)
Bất biến  —
Ghi chú   BR3, BR6 · MT:100 nguyên văn.
```

### R-TLMI-212 · Tên khối chuẩn cố định

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:53 · SCR:260
WHEN      khối là **khối chuẩn**
THEN      tên khối **cố định**, không sửa được trên dòng khối
ELSE      khối **Bảng** ⇒ tên khối = `"Bảng <tên lưới>"`
Lỗi       —
Bất biến  —
Ghi chú   BR3, BR6.
```

### R-TLMI-213 · Bấm một dòng khối thì bảng chỉnh mở đúng khối đó

```
Tầng      FE
Sev       P2
Nguồn     SCR:264
WHEN      người dùng bấm một dòng khối trong Bố cục mẫu
THEN      bảng chỉnh mở đúng khối đó AND khối được **đánh dấu trên trang xem trước**
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-214 · Bấm một khối trên trang xem trước thì bảng chỉnh mở đúng khối đó

```
Tầng      FE
Sev       P2
Nguồn     SCR:216 · SCR:264 · UC01:30
WHEN      người dùng bấm một khối trên trang xem trước
THEN      bảng chỉnh bên phải mở đúng khối đó AND khối được đánh dấu kèm **nhãn tên khối**
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-215 · Rê chuột lên một khối trên trang thì hiện nhãn tên khối

```
Tầng      FE
Sev       P2
Nguồn     SCR:261
WHEN      người dùng rê chuột lên một khối trên trang xem trước
THEN      hiện **nhãn tên khối**
Lỗi       —
Bất biến  —
Ghi chú   BR3.
```

### R-TLMI-216 · Chỉ bảng chỉnh bên phải đổi theo khối đang chọn

```
Tầng      FE
Sev       P1
Nguồn     SCR:24 · MT:7 · MT:99 · SC:6
WHEN      đổi khối đang chọn (một trong sáu: Thiết lập mẫu / Thông tin đầu trang / Tiêu đề / Bảng /
          Khối tự do / Chữ ký)
THEN      **chỉ bảng chỉnh bên phải** đổi nội dung
ELSE      cột trái (Bố cục mẫu), cột giữa (Xem trước) và thanh tiêu đề **luôn hiện ở mọi trường hợp**
Lỗi       —
Bất biến  —
Ghi chú   BR3 · Trục cột I1 của ma trận ẩn/hiện.
          ⚠ Ma trận **không phủ hộp thoại con**: hộp Đặt tên khối, hộp chọn trường cạnh ô, và bốn hộp
          xác nhận MSG_401…404 — đừng tưởng ma trận đã phủ hết màn.
```

---

## M. Xem trước & thao tác trên trang

### R-TLMI-217 · Trang xem trước vẽ bằng dữ liệu thật của chứng từ đang mở

```
Tầng      FE
Sev       P1
Nguồn     SCR:3 · SCR:23 · SCR:305 · UC01:30 · UC01:50
WHEN      mở trang xem trước
THEN      vẽ **trang đầu** của bản in theo mẫu đang chỉnh (**kể cả khi chưa lưu**) bằng
          **dữ liệu thật của chứng từ đang mở**
Lỗi       —
Bất biến  —
Ghi chú   BR8.
```

### R-TLMI-218 · Bất kỳ thay đổi nào thì trang xem trước vẽ lại ngay

```
Tầng      FE
Sev       P1
Nguồn     SCR:305 · UC01:30 · UC01:51
WHEN      có bất kỳ thay đổi nào trên màn
THEN      trang xem trước **vẽ lại ngay**
Lỗi       —
Bất biến  —
Ghi chú   BR8. "ngay" không có ngưỡng thời gian, không nói có debounce khi gõ chữ — phát biểu không kiểm được.
```

### R-TLMI-219 · Không có chế độ dữ liệu mẫu

```
Tầng      FE
Sev       P1
Nguồn     SCR:305
WHEN      người dùng muốn thử mẫu với chứng từ khác
THEN      phải mở màn **từ chứng từ đó**
ELSE      **không có chế độ dữ liệu mẫu**, **không chọn được chứng từ khác** trên màn
Lỗi       —
Bất biến  —
Ghi chú   BR8.
```

### R-TLMI-220 · Trang xem trước vẽ theo nhóm Giấy và chữ của mẫu

```
Tầng      FE
Sev       P1
Nguồn     SCR:306 · UC01:30
WHEN      vẽ trang xem trước
THEN      khổ giấy, hướng giấy, lề, font, cỡ chữ theo **nhóm Giấy và chữ của mẫu**
          (ô theo chung lấy thiết lập chung tại lúc vẽ — R-TLMI-038);
          hướng **Tự động** vẽ đúng hướng sẽ in ra với chứng từ đang mở
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR8, BR2.
```

### R-TLMI-221 · Thu / Phóng / Vừa khung không ảnh hưởng bản in

```
Tầng      FE
Sev       P2
Nguồn     SCR:71 · SCR:221 · SCR:306
WHEN      bấm Thu / Phóng / Vừa khung
THEN      chỉ đổi **tỷ lệ nhìn trên màn** — **KHÔNG** ảnh hưởng bản in
ELSE      mức thu phóng mặc định khi mở màn = **Vừa khung**
Lỗi       —
Bất biến  —
Ghi chú   BR8.
```

### R-TLMI-222 · Hiện lưới căn chỉnh chỉ trên màn, không lưu

```
Tầng      FE
Sev       P1
Nguồn     SCR:70
WHEN      dựng ô tick **Hiện lưới căn chỉnh**
THEN      trường này **chỉ trên màn, KHÔNG lưu**, mặc định = **Có**
Lỗi       —
Bất biến  —
Ghi chú   BR6. Xem R-TLMI-177…179 cho hành vi.
```

### R-TLMI-223 · Hoàn tác / Làm lại nhớ tối đa 60 bước trong phiên

```
Tầng      FE
Sev       P1
Nguồn     SCR:67 · SCR:77 · SCR:317 · UC01:34 · UC01:76-77 · FIGMA (↶ ↷ trên thanh xem trước)
WHEN      dùng Hoàn tác / Làm lại
THEN      hai nút nằm trên **thanh Xem trước** và ghi nhớ tối đa **60 bước** trong phiên đang mở;
          lùi hoặc tiến **một bước chỉnh**, áp cho **toàn mẫu** chứ không riêng phần xem trước
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-224 · Cách đếm một bước Hoàn tác

```
Tầng      FE
Sev       P1
Nguồn     SCR:253 · SCR:317
WHEN      đếm bước Hoàn tác
THEN      **mỗi thao tác đổi mẫu là một bước**, kể cả thêm / xóa dòng cột và gộp / tách ô;
          **gõ chữ trong một ô tính một bước khi rời ô**;
          bấm nút **Theo thiết lập chung** cũng là một bước (R-TLMI-041)
Lỗi       —
Bất biến  —
Ghi chú   BR10, BR2. ⚠ Tài liệu KHÔNG nói **Đặt lại mẫu chuẩn** có phải một bước Hoàn tác được không — xem §Z.
```

### R-TLMI-225 · Đóng màn thì lịch sử Hoàn tác / Làm lại bị xóa

```
Tầng      FE
Sev       P1
Nguồn     SCR:317 · UC01:77
WHEN      đóng màn
THEN      lịch sử Hoàn tác / Làm lại **bị xóa**
Lỗi       —
Bất biến  —
Ghi chú   BR10, BR11.
```

### R-TLMI-226 · Hết bước thì nút tương ứng mờ

```
Tầng      FE
Sev       P2
Nguồn     SCR:77 · MT:33 · MT:66
WHEN      không còn bước Hoàn tác (hoặc Làm lại)
THEN      nút tương ứng **Disable**
Lỗi       —
Bất biến  —
Ghi chú   BR10 · điều kiện phụ `(đk-UNDO)`.
```

### R-TLMI-227 · Ctrl+Z / Ctrl+Y

```
Tầng      FE
Sev       P2
Nguồn     SCR:77 · UC01:76-77
WHEN      người dùng nhấn **Ctrl+Z** / **Ctrl+Y**
THEN      tương đương Hoàn tác / Làm lại
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-228 · Thanh Xem trước luôn hiện ở mọi khối đang chọn

```
Tầng      FE
Sev       P1
Nguồn     MT:67 · MT:99
WHEN      bảng chỉnh đang ở bất kỳ mục nào trong sáu mục
THEN      thanh Xem trước (Khổ giấy · Hướng giấy · Hiện lưới căn chỉnh · Thu / Phóng / Vừa khung ·
          Trang xem trước) **luôn Show**
Lỗi       —
Bất biến  —
Ghi chú   Hệ quả đáng lưu ý: ô Khổ / Hướng giấy trên thanh này luôn bấm được, và bấm là biến ô thành
          **riêng** (R-TLMI-044).
```

### R-TLMI-229 · Trang xem trước là nơi thao tác với lưới khối tự do

```
Tầng      FE
Sev       P1
Nguồn     SCR:23 · SCR:187 · SCR:307 · UC01:25 · UC01:30
WHEN      thao tác trên trang xem trước với khối tự do
THEN      hỗ trợ: bấm ô · Shift + bấm chọn vùng · nháy đúp ô · chuột phải · kéo ô thả lên ô khác ·
          nhận trường kéo từ bảng chỉnh thả vào ô
ELSE      bảng chỉnh **không có** ô chỉnh từng ô lưới (R-TLMI-128)
Lỗi       —
Bất biến  —
Ghi chú   BR8, BR6.
```

---

## N. Kiểm tra & trạng thái

### R-TLMI-230 · Rời một ô thì kiểm tra ngay ô đó

```
Tầng      FE
Sev       P1
Nguồn     SCR:313 · UC01:31
WHEN      người dùng rời một ô nhập liệu
THEN      hệ thống **kiểm tra ngay ô đó**
ELSE      **không có mục kiểm tra riêng** trên màn
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-231 · Ô không hợp lệ được đánh dấu tại chỗ

```
Tầng      FE
Sev       P1
Nguồn     SCR:313
WHEN      một ô không hợp lệ
THEN      ô được **đánh dấu tại chỗ** kèm nội dung thông báo tương ứng của bảng Validation
Lỗi       MSG_PMKT-E-14549_21_201…216 theo bảng Validation (R-TLMI-239)
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-232 · Khối chứa ô lỗi được đánh dấu ở hai nơi

```
Tầng      FE
Sev       P1
Nguồn     SCR:313 · SCR:261 · UC01:31 · MT:63
WHEN      một ô không hợp lệ
THEN      khối chứa ô đó được đánh dấu là có lỗi ở **HAI nơi**:
            1. dòng khối trong **Bố cục mẫu**
            2. chính khối trên **trang xem trước**
Lỗi       —
Bất biến  —
Ghi chú   BR10, BR3.
```

### R-TLMI-233 · Rê chuột lên dòng khối hoặc khối đang lỗi thì hiện nội dung lỗi

```
Tầng      FE
Sev       P2
Nguồn     SCR:313
WHEN      rê chuột lên dòng khối hoặc lên khối đang lỗi
THEN      hiện **nội dung lỗi**
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-234 · Sửa đúng thì các dấu hiệu lỗi tắt ngay

```
Tầng      FE
Sev       P1
Nguồn     SCR:313
WHEN      người dùng sửa đúng
THEN      các dấu hiệu lỗi **tắt ngay**
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-235 · Ô lưới khối tự do không hợp lệ thì viền đỏ ngay trên trang xem trước

```
Tầng      FE
Sev       P1
Nguồn     SCR:315 · FIGMA (frame 3 — ô lỗi viền đỏ, chữ đỏ nghiêng)
WHEN      một ô lưới của khối tự do không hợp lệ
THEN      ô đó **viền đỏ ngay trên trang xem trước**
Lỗi       —
Bất biến  —
Ghi chú   BR10. BR10 nói thêm điều này mà bảng Validation 17 dòng không ghi.
```

### R-TLMI-236 · Ô trống trong khối tự do không bao giờ là lỗi

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:314 · UC01:31
WHEN      ô trong khối tự do là **ô trống**
THEN      **KHÔNG BAO GIỜ** là lỗi; khối toàn ô trống vẫn lưu được
Lỗi       —
Bất biến  —
Ghi chú   BR10, BR6.
```

### R-TLMI-237 · Xét lỗi trong khối tự do chỉ xét ô có nội dung

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:314
WHEN      xét lỗi trong khối tự do
THEN      **chỉ xét ô CÓ NỘI DUNG** (ví dụ ô Chữ tự do quá 255 ký tự)
Lỗi       MSG_PMKT-E-14549_21_212
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-238 · Không có cảnh báo mềm

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:315
WHEN      người dùng chọn ẩn hết bảng, không có ô ký, khối tự do toàn ô trống…
THEN      **KHÔNG** có cảnh báo mềm — đó là quyền của người dùng
Lỗi       —
Bất biến  —
Ghi chú   BR10. Cấm tự thêm cảnh báo "cho chắc".
```

### R-TLMI-239 · Bảng kiểm tra dữ liệu 17 dòng

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:338-356
WHEN      kiểm tra dữ liệu của mẫu
THEN      áp đúng 17 dòng dưới đây, đúng tầng và đúng thời điểm:
```

| # | Trường thông tin | Điều kiện kiểm tra | Mã thông báo | Tầng kiểm tra | Thời điểm kiểm tra | Luật |
|---|---|---|---|---|---|---|
| V01 | Tiêu đề: Nội dung | Không trống, tối đa 255 ký tự | `MSG_PMKT-E-14549_21_201` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-085 |
| V02 | Tiêu đề: Cỡ chữ | Số nguyên 10–36 | `MSG_PMKT-E-14549_21_202` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-086 |
| V03 | Bảng: cột in | Bảng đang bật phải còn ít nhất 1 cột tick | `MSG_PMKT-E-14549_21_203` | Client / Server | Khi bỏ tick cột, khi nhấn Lưu | R-TLMI-104 |
| V04 | Bảng: Tên hiển thị của cột | Không trống, tối đa 100 ký tự | `MSG_PMKT-E-14549_21_204` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-102 |
| V05 | Bảng: Rộng % | Số nguyên 3–90 | `MSG_PMKT-E-14549_21_205` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-108 |
| V06 | Khối tự do: tên | Không trống, tối đa 60 ký tự | `MSG_PMKT-E-14549_21_206` | Client / Server | Trong hộp Đặt tên khối, khi rời ô, khi nhấn Lưu | R-TLMI-121 |
| V07 | Số khối tự do | Tối đa 10 | `MSG_PMKT-E-14549_21_207` | Client / Server | Khi bấm Thêm khối tự do, khi Lưu | R-TLMI-125 |
| V08 | Số dòng một khối tự do | Tối đa 20 | `MSG_PMKT-E-14549_21_208` | Client / Server | Khi bấm + Dòng trên / + Dòng dưới, khi Lưu | R-TLMI-129 |
| V09 | Số cột một khối tự do | Tối đa 6 | `MSG_PMKT-E-14549_21_216` | Client / Server | Khi bấm + Cột trái / + Cột phải, khi Lưu | R-TLMI-130 |
| V10 | Ảnh nền | jpg/png, ≤ 1MB | `MSG_PMKT-E-14549_21_209` | Client / Server | Khi chọn tệp | R-TLMI-069 |
| V11 | Màu chữ | Dạng `#rrggbb` | `MSG_PMKT-E-14549_21_210` | Client / Server | Khi rời ô, khi Lưu | R-TLMI-066 |
| V12 | Chữ ký: ô ký tự do đang bật | Tiêu đề không trống, tối đa 60 ký tự | `MSG_PMKT-E-14549_21_211` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-189 |
| V13 | Khối tự do: Tên hiển thị của trường; nội dung ô Chữ tự do | Tối đa 255 ký tự (ô Chữ tự do trống thì tự về ô trống, không phải lỗi) | `MSG_PMKT-E-14549_21_212` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-147, R-TLMI-157 |
| V14 | Giấy và chữ: Căn lề trên, trái, dưới, phải | Số từ 0 đến 5, tối đa một chữ số lẻ | `MSG_PMKT-E-14549_21_213` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-061 |
| V15 | Giấy và chữ: Số cột để tự động in ngang | Số nguyên 1–50, chỉ kiểm tra khi Hướng giấy = Tự động | `MSG_PMKT-E-14549_21_214` | Client / Server | Khi rời ô, khi nhấn Lưu | R-TLMI-057 |
| V16 | Giấy và chữ: Cỡ chữ | Số nguyên 8–20 (ô chọn từ danh sách nên chỉ chặn phía máy chủ) | `MSG_PMKT-E-14549_21_215` | Server | Khi nhấn Lưu | R-TLMI-063 |
| V17 | Quyền | Có quyền Thiết lập mẫu in của nghiệp vụ | `MSG_PMKT-E-14549_21_002` | Server | Khi mở màn, khi Lưu | R-TLMI-034 |

```
Lỗi       17 mã ở cột "Mã thông báo"
Bất biến  INV-TLMI-004, INV-TLMI-005, INV-TLMI-006, INV-TLMI-010
Ghi chú   BR10 · Ba điều BR10 (SCR:314-315) nói thêm mà bảng này KHÔNG ghi, và đều là "KHÔNG phải lỗi":
            · tổng độ rộng cột khác 100 ⇒ tự chia lại khi Lưu (R-TLMI-111)
            · ô trống trong khối tự do (R-TLMI-236)
            · ô lưới không hợp lệ viền đỏ ngay trên trang xem trước (R-TLMI-235)
          ⚠ Bảng KHÔNG có dòng nào cho **Độ đậm hình nền** (5–100 %) — xem §Z.
```

### R-TLMI-240 · Nhãn trạng thái "Đã lưu" và nút Lưu mờ

```
Tầng      FE
Sev       P1
Nguồn     SCR:37 · SCR:40 · SCR:316 · MT:31 · MT:62 · MT:106 · FIGMA (badge xám "Đã lưu")
WHEN      mẫu trên màn **bằng bản đã lưu** (hoặc bằng mẫu chuẩn khi chưa có bản ghi)
THEN      nhãn trạng thái = **"Đã lưu"** AND nút **Lưu** **Disable**
Lỗi       —
Bất biến  —
Ghi chú   BR10 · điều kiện phụ `(đk-DL)`.
```

### R-TLMI-241 · Nhãn trạng thái "Chưa lưu"

```
Tầng      FE
Sev       P1
Nguồn     SCR:37 · SCR:316 · FIGMA (badge cam "Chưa lưu")
WHEN      có thay đổi AND **mọi ô hợp lệ**
THEN      nhãn trạng thái = **"Chưa lưu"** AND bấm Lưu thì ghi
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-242 · Nhãn trạng thái "Có lỗi"

```
Tầng      FE
Sev       P1
Nguồn     SCR:37 · SCR:316 · FIGMA (badge đỏ "Có lỗi")
WHEN      còn **ít nhất một ô không hợp lệ**
THEN      nhãn trạng thái = **"Có lỗi"**
Lỗi       —
Bất biến  —
Ghi chú   BR10. Ba nhãn "Đã lưu / Chưa lưu / Có lỗi" là text hiển thị ⇒ phải có key i18n (luật 2).
```

### R-TLMI-243 · Có lỗi mà bấm Lưu thì chỉ báo lỗi đầu tiên

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:40 · SCR:235 · SCR:316 · UC01:31 · UC01:67 · AD01:37 · MT:106
WHEN      trạng thái = **Có lỗi** AND người dùng bấm Lưu
THEN      **KHÔNG ghi**; hiện thông báo của **lỗi ĐẦU TIÊN** theo thứ tự:
            1. thứ tự **khối** trong Bố cục mẫu
            2. rồi thứ tự **ô** trong khối
Lỗi       một trong MSG_PMKT-E-14549_21_201…216
Bất biến  INV-TLMI-012
Ghi chú   BR10. Nút Lưu vẫn **bấm được** khi Có lỗi (MT:106) — chỉ Đã lưu mới Disable.
          ⚠ Tài liệu KHÔNG quy định thứ tự ô lỗi **trong một khối** khi khối có cả ô ở bảng chỉnh
          lẫn ô lưới trên trang xem trước — xem §Z.
```

### R-TLMI-244 · Báo lỗi đầu tiên thì mở khối và đưa con trỏ vào ô lỗi

```
Tầng      FE
Sev       P1
Nguồn     SCR:40 · SCR:316 · UC01:31 · UC01:67
WHEN      báo lỗi đầu tiên lúc Lưu
THEN      mở **bảng chỉnh của khối đó** và đưa **con trỏ vào ô lỗi**
ELSE      lỗi ở **ô lưới khối tự do** ⇒ **chọn ô đó trên trang xem trước**
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-245 · Tiêu đề màn và vị trí nhãn trạng thái, nút Lưu

```
Tầng      FE
Sev       P2
Nguồn     SCR:18 · SCR:36 · SCR:316 · MT:60 · FIGMA (modal header)
WHEN      bố trí màn
THEN      tiêu đề màn = `"Thiết lập mẫu in: <Tên loại chứng từ>"`;
          **nhãn trạng thái nằm cạnh tiêu đề màn**; **nút Lưu ở chân màn**
Lỗi       —
Bất biến  —
Ghi chú   BR1, BR10. Figma vẽ header modal cao 52 px với nhãn trạng thái là badge cạnh tiêu đề,
          bên phải là icon `?` (trợ giúp) và `✕`.
```

### R-TLMI-246 · Bấm Lưu thì kiểm tra lại toàn bộ, cả ở server

```
Tầng      BE
Sev       P0
Nguồn     SCR:318 · SCR:338-356 · UC01:53
WHEN      bấm Lưu
THEN      kiểm tra lại **toàn bộ** theo bảng Validation (R-TLMI-239), **CẢ Ở SERVER**
Lỗi       MSG_PMKT-E-14549_21_201…216
Bất biến  —
Ghi chú   BR10. Không được tin FE đã kiểm.
```

### R-TLMI-247 · Lưu hợp lệ thì ghi toàn bộ mẫu trong một transaction

```
Tầng      BE
Sev       P0
Nguồn     SCR:318 · UC01:32 · UC01:54 · AD01:33 · CRUD:5-9
WHEN      Lưu hợp lệ
THEN      trong **MỘT transaction**:
            · ghi bản ghi `cfg_mau_in_chung_tu` (tạo mới nếu chưa có)
            · ghi lại toàn bộ **khối, cột, ô lưới, chữ ký** — **xóa hết bản cũ, ghi bản mới**
            · ô **theo chung** ghi **trống** (R-TLMI-037)
Lỗi       —
Bất biến  INV-TLMI-003, INV-TLMI-012
Ghi chú   BR10. ⚠ Tài liệu KHÔNG nói có giữ id cũ hay không ⇒ không kiểm được ảnh hưởng tới dữ liệu
          tham chiếu (nếu có) — xem §Z. Nhánh **xóa bản ghi** đang bị C02 chặn (R-TLMI-021).
```

### R-TLMI-248 · Lưu thành công thì báo, màn giữ nguyên

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:318 · SCR:362 · UC01:32 · UC01:55 · MSG:14
WHEN      Lưu thành công (commit)
THEN      hiển thị MSG_PMKT-E-14549_21_101; màn **giữ nguyên**; nhãn trạng thái về **"Đã lưu"**
Lỗi       MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"
Bất biến  —
Ghi chú   BR10. ⚠ Tài liệu KHÔNG nói nhánh *Lưu và đóng* (R-TLMI-252) có hiện MSG_101 trước khi đóng
          không — xem §Z.
```

### R-TLMI-249 · Lưu gặp lỗi hệ thống thì rollback

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:318 · SCR:362 · UC01:80-83 · UC01:93 · MSG:8
WHEN      Lưu gặp lỗi hệ thống
THEN      **rollback**; **giữ nguyên màn**; hiển thị MSG_PMKT-E-14549_21_003
ELSE      **không thay đổi mẫu** — hậu điều kiện thất bại của UC01
Lỗi       MSG_PMKT-E-14549_21_003 — "Lỗi hệ thống, vui lòng thử lại sau"
Bất biến  INV-TLMI-012
Ghi chú   BR10 · UC01 NL5.
```

### R-TLMI-250 · Ctrl+S tương đương bấm Lưu

```
Tầng      FE
Sev       P2
Nguồn     SCR:40
WHEN      người dùng nhấn **Ctrl+S**
THEN      tương đương bấm **Lưu**
Lỗi       —
Bất biến  —
Ghi chú   BR10.
```

### R-TLMI-251 · Đóng hoặc Esc khi có thay đổi chưa lưu thì hỏi

```
Tầng      FE
Sev       P0
Nguồn     SCR:39 · SCR:236 · SCR:321 · SCR:368 · UC01:34 · UC01:86-87 · MSG:44
WHEN      bấm **Đóng** hoặc phím **Esc** AND mẫu trên màn **khác** bản đã lưu
THEN      hỏi MSG_PMKT-E-14549_21_401 với **ba nút**: *Lưu và đóng* / *Không lưu* / *Ở lại*
Lỗi       MSG_PMKT-E-14549_21_401 — "Mẫu đã có thay đổi chưa lưu. Bạn muốn làm gì?"
          Nút: **Lưu và đóng** · **Không lưu** · **Ở lại**
Bất biến  —
Ghi chú   BR11. ⚠ AD01:45-49 đơn giản hóa: hỏi MSG_401 rồi **luôn** đóng màn, không rẽ ba nhánh.
          UC01:87 là chuẩn — đừng code theo AD.
```

### R-TLMI-252 · Chọn "Lưu và đóng"

```
Tầng      FE
Sev       P0
Nguồn     SCR:321 · UC01:87
WHEN      người dùng chọn *Lưu và đóng*
THEN      chạy Lưu (bước kiểm tra → transaction → commit), **thành công mới đóng**
ELSE      mẫu **Có lỗi** ⇒ báo lỗi đầu tiên và **ở lại** màn
Lỗi       MSG_PMKT-E-14549_21_201…216 hoặc `_003`
Bất biến  INV-TLMI-012
Ghi chú   BR11, BR10.
```

### R-TLMI-253 · Chọn "Không lưu"

```
Tầng      FE
Sev       P0
Nguồn     SCR:321 · UC01:87
WHEN      người dùng chọn *Không lưu*
THEN      **bỏ mọi thay đổi** và đóng màn
Lỗi       —
Bất biến  INV-TLMI-012
Ghi chú   BR11.
```

### R-TLMI-254 · Chọn "Ở lại"

```
Tầng      FE
Sev       P1
Nguồn     UC01:87
WHEN      người dùng chọn *Ở lại*
THEN      **giữ màn**, không đóng, không đổi gì
Lỗi       —
Bất biến  —
Ghi chú   BR11 · UC01 NL6.
```

### R-TLMI-255 · Không có thay đổi thì đóng ngay

```
Tầng      FE
Sev       P1
Nguồn     SCR:321 · UC01:87
WHEN      **không có thay đổi** AND bấm Đóng / Esc
THEN      **đóng ngay**, KHÔNG hỏi
Lỗi       —
Bất biến  —
Ghi chú   BR11.
```

### R-TLMI-256 · Đang mở hộp thoại con thì Esc không tác dụng với màn chính

```
Tầng      FE
Sev       P1
Nguồn     SCR:321
WHEN      đang mở một **hộp thoại con** AND bấm Esc
THEN      phím Esc **không tác dụng** với màn chính
Lỗi       —
Bất biến  —
Ghi chú   BR11. Hộp thoại con gồm: hộp Đặt tên khối, hộp chọn trường cạnh ô, bốn hộp xác nhận MSG_401…404.
```

### R-TLMI-257 · Chân màn

```
Tầng      FE
Sev       P2
Nguồn     SCR:26 · MT:61 · MT:62 · FIGMA (chân màn cao ~56)
WHEN      dựng chân màn
THEN      **Đóng** ở **góc trái**; **Đặt lại mẫu chuẩn** · **Lưu** ở **góc phải**
ELSE      Đặt lại mẫu chuẩn và Đóng **luôn Show** ở mọi khối đang chọn; Lưu theo `(đk-DL)` (R-TLMI-240)
Lỗi       —
Bất biến  —
Ghi chú   Figma: nút Lưu là nút chính (đỏ).
```

### R-TLMI-258 · Hai người cùng sửa một mẫu — khóa lạc quan bằng `phienBan`

```
Tầng      BE
Sev       P1
Nguồn     SCR:247 · SCR:318 · UC01:54 · CRUD:17 — (tất cả đều IM LẶNG về tình huống này)
Chốt      C06 · 04-quyet-dinh-ban-giao.md §3 · Dat · 2026-09-19

WHEN      bấm Lưu AND `phienBan` trong payload KHÁC `phienBan` của bản ghi mẫu hiện tại trong DB
THEN      **KHÔNG ghi** — hủy transaction, trả lỗi MSG_COMMON_001; màn giữ nguyên thay đổi của người
          dùng và hỏi nạp lại mẫu mới nhất
ELSE      `phienBan` khớp ⇒ ghi bình thường (R-TLMI-247) và tăng `phienBan` lên 1
Lỗi       MSG_COMMON_001 — thao tác không hợp lệ với trạng thái hiện tại (mã dùng chung, BR25/BR26)
          + một key i18n riêng cho câu hướng dẫn nạp lại
Bất biến  INV-TLMI-012
Ghi chú   Đây vốn là khoảng trống **có rủi ro thật**, không phải mâu thuẫn tài liệu: mẫu dùng chung
          cho cả đơn vị (R-TLMI-005) và Lưu là "xóa hết bản cũ, ghi bản mới" (R-TLMI-247) ⇒ nếu code
          trần theo tài liệu thì người Lưu sau **ghi đè âm thầm** toàn bộ công của người Lưu trước.
          Ba hướng đã cân nhắc, đã chốt **hướng (2)**:
            (1) KHÔNG CHỌN · ghi đè theo thứ tự đến — không thêm gì. Đúng chữ tài liệu nhưng **mất
                dữ liệu âm thầm**, không có cách phát hiện.
            (2) ĐÃ CHỌN · **khóa lạc quan** bằng `phienBan` trong payload. Trường này **đã có sẵn**
                ở `LuuMauInRequest` bản cũ ⇒ không đổi hợp đồng API, không thêm cột mới.
            (3) KHÔNG CHỌN · khóa bi quan / cảnh báo khi mở — cần thêm API giữ khóa, thêm luồng
                nhả khóa khi mất kết nối, và vẫn cần một mã message mới. Đắt hơn hẳn (2) mà không
                chặn được nhiều hơn.
          Vì sao chọn (2): rẻ nhất (đã có trường), không mất dữ liệu, và giữ nguyên hành vi Lưu
          all-or-nothing của INV-TLMI-012.
          ⚠ **Nợ BA (L-4 ở `04-quyet-dinh-ban-giao.md §5`):** `6.messages.md` chưa cấp mã riêng cho
          tình huống này ⇒ tạm dùng `MSG_COMMON_001`. Khi BA cấp mã `MSG_PMKT-E-14549_21_…` thì đổi
          ở đây trước, rồi mới đổi code.
```

---

## P. Dựng bản in (UC02)

### R-TLMI-259 · Chọn Mẫu tùy chỉnh thì dựng bản in theo mẫu của nghiệp vụ chứng từ đang mở

```
Tầng      BE
Sev       P0
Nguồn     SCR:328 · UC02:22 · UC02:40 · FB:24-26
WHEN      người dùng chọn **Mẫu tùy chỉnh** trong menu In
THEN      xác định nghiệp vụ của chứng từ, đọc `cfg_mau_in_chung_tu` cùng bảng con và dựng bản in
          theo mẫu tùy chỉnh của **nghiệp vụ của chứng từ đang mở**
Lỗi       —
Bất biến  —
Ghi chú   BR12.
```

### R-TLMI-260 · Chưa có bản ghi mẫu thì in theo mẫu chuẩn và báo một lần

```
Tầng      CẢ HAI
Sev       P1
Nguồn     SCR:328 · SCR:369 · UC02:22 · UC02:48-51 · FB:25 · MSG:16
WHEN      chọn Mẫu tùy chỉnh AND **chưa có** bản ghi mẫu của nghiệp vụ
THEN      in theo **mẫu chuẩn hệ thống của nghiệp vụ** và hiện MSG_PMKT-E-14549_21_103
          **MỘT LẦN** trên màn xem trước bản in
ELSE      **KHÔNG phải lỗi** — vẫn mở màn xem trước bình thường
Lỗi       MSG_PMKT-E-14549_21_103 — "Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in
          theo mẫu chuẩn hệ thống"
Bất biến  INV-TLMI-002
Ghi chú   BR12 · UC02 NL1. ⚠ "một lần" là một lần **mỗi lần mở xem trước**, mỗi phiên, hay mỗi người
          dùng — tài liệu không nói, xem §Z.
          ⚠ AD02:13-14 đặt MSG_103 ngay ở nhánh chưa có mẫu, trước khi dựng bản in; UC02:22 nói
          "một lần trên màn xem trước bản in" — giữ theo UC02.
```

### R-TLMI-261 · Nút In bị disable thì cả menu In không mở được

```
Tầng      CẢ HAI
Sev       P0
Nguồn     SCR:328 · UC02:23 · UC02:39 · UC02:53-56 · S20:155-156 · BR2P BR51.5
WHEN      nút In bị disable theo **hai quy tắc cấm in** của thiết lập chung
          (không cho phép in chứng từ **chưa ghi sổ** · không cho phép in chứng từ **đã khóa sổ**,
          và chứng từ đang ở trạng thái đó)
THEN      **cả menu In không mở được**, kể cả mục **Mẫu tùy chỉnh**
ELSE      nút In disable kèm **tooltip** theo BR7 của màn Cấu hình báo cáo chứng từ
Lỗi       — (tooltip, không có mã message: xem §Z)
Bất biến  —
Ghi chú   BR12. Nguyên văn hai tooltip (S20:155-156), là **chuỗi người dùng thấy** ⇒ phải có key i18n:
            · "Đơn vị không cho phép in chứng từ chưa ghi sổ"
            · "Đơn vị không cho phép in chứng từ đã khóa sổ"
          Quy tắc "đã khóa sổ" **chỉ tác động nút In của chứng từ**, không tác động báo cáo và
          **không tác động Xuất Excel** (S20:157).
```

### R-TLMI-262 · Dựng bản in theo thứ tự Bố cục mẫu, chỉ khối đang bật

```
Tầng      BE
Sev       P1
Nguồn     SCR:331 · UC02:24 · UC02:42
WHEN      dựng bản in
THEN      dựng **từ trên xuống** theo thứ tự Bố cục mẫu, **chỉ các khối đang bật**, theo đúng nội dung
          ô, cột bảng, chữ ký của mẫu, bằng dữ liệu của chứng từ đang in
Lỗi       —
Bất biến  —
Ghi chú   BR13.
```

### R-TLMI-263 · Hình nền vẽ dưới cùng

```
Tầng      FE
Sev       P1
Nguồn     SCR:331 · SCR:302
WHEN      mẫu có hình nền
THEN      vẽ hình nền **dưới cùng**
Lỗi       —
Bất biến  —
Ghi chú   BR13, BR7.
Tầng — vì sao FE
          Luật **thứ tự lớp vẽ**, thuộc tầng dựng bản in. Giai đoạn 1 **FE dựng bản in**
          (quyết định D3 của kế hoạch BE); BE chỉ trả cờ `nen.kieu` và ảnh nền.
          **Xem lại khi** BE sinh PDF — xem ghi chú ở R-TLMI-180.
```

### R-TLMI-264 · Chữ, đường kẻ và giấy-chữ của bản in

```
Tầng      BE
Sev       P0
Nguồn     SCR:331
WHEN      dựng bản in
THEN      chữ và đường kẻ theo **màu chữ của mẫu**; khổ giấy, hướng giấy, lề, font, cỡ chữ theo
          **nhóm Giấy và chữ của mẫu**; ô **theo chung** lấy giá trị thiết lập chung **TẠI LÚC IN**
Lỗi       —
Bất biến  INV-TLMI-003
Ghi chú   BR13, BR2. Đây là điểm đo được của R-TLMI-038.
```

### R-TLMI-265 · Bảng dài tràn trang; khối sau in tiếp ngay dưới

```
Tầng      FE
Sev       P1
Nguồn     SCR:332 · SCR:333
WHEN      bảng dài
THEN      tràn sang trang sau; các khối đứng **sau** bảng (khối tự do, Chữ ký) in tiếp **ngay dưới
          dòng cuối** của bảng ở trang cuối
ELSE      trừ khối Chữ ký khi không đủ chỗ — R-TLMI-200
Lỗi       —
Bất biến  —
Ghi chú   BR13, BR5.
Tầng — vì sao FE
          Luật **ngắt trang và dòng chảy khối**, thuộc tầng dựng bản in. Giai đoạn 1 **FE dựng bản
          in** (quyết định D3 của kế hoạch BE). **Xem lại khi** BE sinh PDF — xem ghi chú ở R-TLMI-180.
```

### R-TLMI-266 · Áp ba quy tắc in chứng từ của thiết lập chung

```
Tầng      BE
Sev       P0
Nguồn     SCR:334 · UC02:23 · UC02:39 · UC02:41 · FB:26 · BR2P BR51.5 · S20:160-164
Chốt      C01 + C30 · 04-quyet-dinh-ban-giao.md §2, §4 · Dat · 2026-09-19

WHEN      dựng bản in chứng từ
THEN      áp **ba quy tắc** của thiết lập chung:
            (a) cho phép in chứng từ **chưa ghi sổ**  — kiểm ở bước 2 của UC02, xem R-TLMI-261
            (b) cho phép in chứng từ **đã khóa sổ**   — kiểm ở bước 2 của UC02, xem R-TLMI-261
            (c) **cộng gộp mặt hàng** khi in — khóa gộp = mã hàng + đơn vị tính + đơn giá +
                **thuế suất** (+ số lô + hạn sử dụng nếu vật tư theo dõi theo lô), áp **trước** khi
                dựng bảng (R-TLMI-119)
ELSE      (c) chỉ áp khi thiết lập chung bật **VÀ** loại chứng từ ∈ { Hóa đơn, phiếu xuất kho,
          phiếu nhập kho }
Lỗi       —
Bất biến  —
Ghi chú   Lý lẽ đầy đủ ở **R-TLMI-119**. Tóm tắt: chọn khóa gộp **CÓ thuế suất** theo S20:160-162 vì
          nguồn này chi tiết hơn và có ví dụ phủ định ("khác thuế suất thì **không gộp**"); BR51.5
          chỉ liệt kê thiếu, không phủ định. Giữ **phạm vi** của BR51.5 + S20:160 — SCR:281 không
          nhắc lại giới hạn ba loại chứng từ, không được vì thế mà mở rộng ra mọi chứng từ.
```

### R-TLMI-267 · Đọc hồ sơ đơn vị để in theo chi nhánh ghi trên chứng từ

```
Tầng      BE
Sev       P0
Nguồn     UC01:49 · UC02:41 · SCR:267 · BR2P BR50.7
WHEN      đọc hồ sơ đơn vị để dựng bản in (và để vẽ trang xem trước)
THEN      đọc `ENT_cfg_chi_nhanh` theo **chi nhánh ghi trên chứng từ** — KHÔNG phải chi nhánh đang
          làm việc; đọc thiết lập chung từ `ENT_cfg_tenant`
Lỗi       —
Bất biến  —
Ghi chú   BR50.7. Áp cho **khối Thông tin đầu trang** (R-TLMI-078), **kho trường** (R-TLMI-165)
          và **khối Chữ ký** — tài liệu im lặng ở khối Chữ ký nhưng đã chốt C05 theo cùng quy tắc,
          xem R-TLMI-199. Mọi chỗ đi qua một cổng duy nhất `HoSoDonViPort.theoChiNhanh(chiNhanhId)`.
```

### R-TLMI-268 · Mở màn xem trước bản in như các mẫu cố định

```
Tầng      FE
Sev       P1
Nguồn     UC02:25 · UC02:43 · FIGMA (frame 0)
WHEN      dựng bản in xong
THEN      mở **màn xem trước bản in như các mẫu cố định**, có nút **In** và **Xuất file** theo
          **hành vi chung của bản in chứng từ**
Lỗi       —
Bất biến  —
Ghi chú   Hành vi chung của bản in chứng từ nằm **ngoài** epic này — xem `00-source-map.md` §3.
```

### R-TLMI-269 · Màn xem trước có nút Sửa mẫu khi người dùng có quyền

```
Tầng      FE
Sev       P0
Nguồn     UC02:25 · UC02:43 · UC01:22 · SCR:326 · MT:59
WHEN      người dùng **có quyền Thiết lập mẫu in**
THEN      màn xem trước bản in có thêm nút **Sửa mẫu** mở màn Thiết lập mẫu in
ELSE      không có quyền ⇒ nút **Hide** (R-TLMI-032)
Lỗi       —
Bất biến  —
Ghi chú   BR12.
```

### R-TLMI-270 · Lỗi hệ thống khi dựng bản in thì không mở màn xem trước

```
Tầng      CẢ HAI
Sev       P0
Nguồn     UC02:58-61 · AD02:23 · MSG:8
WHEN      dựng bản in gặp lỗi hệ thống
THEN      hiển thị MSG_PMKT-E-14549_21_003 AND **KHÔNG mở màn xem trước**
Lỗi       MSG_PMKT-E-14549_21_003 — "Lỗi hệ thống, vui lòng thử lại sau"
Bất biến  —
Ghi chú   UC02 NL3.
```

### R-TLMI-271 · In bằng mẫu tùy chỉnh không thay đổi dữ liệu

```
Tầng      BE
Sev       P1
Nguồn     UC02:65
WHEN      in bằng mẫu tùy chỉnh
THEN      **KHÔNG thay đổi** dữ liệu chứng từ hay mẫu
Lỗi       —
Bất biến  —
Ghi chú   UC02 Hậu điều kiện.
```

---

## §X. Bất biến `INV-TLMI-nnn`

Điều **luôn đúng bất kể luồng**. Mỗi bất biến **bắt buộc có ít nhất một test** — `/verify-spec` chấm
FAIL nếu không tìm thấy test mang chính mã `INV-TLMI-nnn` trong tên.

### INV-TLMI-001 · Một tenant + một nghiệp vụ ⇒ tối đa một mẫu

```
Phát biểu       COUNT(cfg_mau_in_chung_tu WHERE TenantId=? AND MaChucNang=? AND MaNghiepVu=?) ≤ 1
                (mọi thời điểm, kể cả giữa hai transaction)
Nguồn           SCR:247 · CRUD:17 · FB:7
Luật liên quan  R-TLMI-001, R-TLMI-002, R-TLMI-003, R-TLMI-004, R-TLMI-012
Cách kiểm       BE: test ràng buộc unique index — hai lần Lưu liên tiếp cùng (tenant, chức năng,
                nghiệp vụ) ⇒ vẫn đúng 1 bản ghi. Cộng một test tương tranh: 2 request Lưu song song
                ⇒ không sinh 2 bản ghi.
```

### INV-TLMI-002 · Mẫu bằng mẫu chuẩn ⇒ không tồn tại bản ghi

```
Phát biểu       nghiệp vụ đang dùng mẫu chuẩn hệ thống  ⟺  KHÔNG tồn tại bản ghi cfg_mau_in_chung_tu
                (vắng bản ghi CHÍNH LÀ trạng thái "dùng mẫu chuẩn" — không có cờ riêng)
Nguồn           SCR:247 · SCR:318 · SCR:328 · CRUD:15 · CRUD:17
Luật liên quan  R-TLMI-006, R-TLMI-007, R-TLMI-021, R-TLMI-260
Cách kiểm       BE: sau Đặt lại mẫu chuẩn + Lưu ⇒ không còn bản ghi mẫu (kể cả mọi nhánh con);
                ngay sau đó gọi API in Mẫu tùy chỉnh ⇒ trả mẫu chuẩn + MSG_…_103.
                Chiều "⟸" (C02 đã chốt **so sánh nội dung** — R-TLMI-021) có thêm hai ca bắt buộc:
                  · chỉnh tay rồi Hoàn tác hết về đúng mẫu chuẩn, bấm Lưu ⇒ **cũng** xóa bản ghi;
                  · mở màn lần đầu khi chưa có bản ghi, bấm Lưu mà không sửa gì ⇒ **không tạo**.
```

### INV-TLMI-003 · Ô theo chung ⇒ cột NULL

```
Phát biểu       ô ở trạng thái "theo chung"  ⟺  cột tương ứng trong cfg_mau_in_chung_tu /
                cfg_mau_in_khoi = NULL (trống). Không bao giờ lưu giá trị đang hiển thị.
Nguồn           SCR:252 · SCR:318 · SCR:331
Luật liên quan  R-TLMI-036 … R-TLMI-044, R-TLMI-220, R-TLMI-264
Cách kiểm       BE: mở mẫu mới, không sửa gì, Lưu ⇒ mọi cột nhóm Giấy và chữ = NULL.
                Rồi đổi thiết lập chung (font TNR → Arial) ⇒ bản in của mẫu đó đổi sang Arial.
                Sau đó sửa font riêng trong mẫu ⇒ cột có giá trị; đổi thiết lập chung lần nữa ⇒
                bản in KHÔNG đổi.
```

### INV-TLMI-004 · Khối Bảng đang bật luôn có ít nhất một cột hiển thị

```
Phát biểu       ∀ khối Bảng có HienThi = Có:  COUNT(cột có HienThi = Có) ≥ 1
Nguồn           SCR:277 · SCR:342
Luật liên quan  R-TLMI-103, R-TLMI-104
Cách kiểm       BE: POST lưu mẫu có một khối Bảng đang bật với 0 cột tick ⇒ 400 + MSG_…_203 kèm
                {TenBang}. FE: bỏ tick cột cuối ⇒ chặn ngay tại chỗ.
```

### INV-TLMI-005 · Độ rộng cột đã lưu luôn hợp lệ và tổng bằng 100

```
Phát biểu       ∀ khối Bảng đã lưu:  Σ DoRong(cột đang tick in) = 100
                AND ∀ cột đang tick in:  3 ≤ DoRong ≤ 90
Nguồn           SCR:278 · SCR:279 · SCR:318 · SCR:344
Luật liên quan  R-TLMI-108 … R-TLMI-114
Cách kiểm       BE: lưu mẫu với tổng 98 ⇒ commit xong đọc lại thấy tổng đúng 100.
                Ba bộ dữ liệu của BA làm test bảng: 40/40/40 → 33/33/34 · 50/30 → 62/38 ·
                10/10/10/10 → 25/25/25/25. Cộng một ca chạm sàn: cột sau khi chia < 3 ⇒ nâng lên 3,
                trừ vào cột rộng nhất, tổng vẫn 100.
```

### INV-TLMI-006 · Trần và sàn của khối tự do

```
Phát biểu       COUNT(khối tự do trong một mẫu) ≤ 10
                AND ∀ khối tự do:  1 ≤ số dòng ≤ 20  AND  1 ≤ số cột ≤ 6
Nguồn           SCR:284 · SCR:285 · SCR:346 · SCR:347 · SCR:348
Luật liên quan  R-TLMI-123, R-TLMI-125, R-TLMI-129, R-TLMI-130, R-TLMI-133, R-TLMI-134, R-TLMI-135
Cách kiểm       BE: POST lưu mẫu có 11 khối tự do ⇒ 400 + MSG_…_207; 21 dòng ⇒ MSG_…_208;
                7 cột ⇒ MSG_…_216; 0 dòng hoặc 0 cột ⇒ không lưu được.
                FE: khối còn 1 dòng ⇒ nút − Dòng Disable.
```

### INV-TLMI-007 · Một trường ở tối đa một ô trong một khối

```
Phát biểu       ∀ khối tự do, ∀ trường:  COUNT(ô trong khối đó đang dùng trường) ≤ 1
                (nhưng cùng một trường ĐƯỢC dùng ở nhiều khối tự do khác nhau)
Nguồn           SCR:288 · UC01:25
Luật liên quan  R-TLMI-149, R-TLMI-152, R-TLMI-153, R-TLMI-154
Cách kiểm       FE: đặt trường X vào ô (1,1), rồi đặt lại X vào ô (1,2) ⇒ ô (1,1) thành ô trống,
                ô (1,2) mang X. BE: lưu mẫu có hai ô cùng khối cùng trường ⇒ không tồn tại trạng thái đó.
```

### INV-TLMI-008 · Bốn loại khối chuẩn luôn tồn tại trong mẫu

```
Phát biểu       ∀ mẫu (kể cả mẫu tùy chỉnh đã sửa nhiều): vẫn tồn tại khối Thông tin đầu trang,
                khối Tiêu đề, n khối Bảng (n = số lưới trên form) và khối Chữ ký.
                Chúng chỉ đổi ThuTu và HienThi; KHÔNG bao giờ bị xóa.
Nguồn           SCR:260 · SCR:263 · UC01:23 · UC01:24 · MT:64 · MT:100
Luật liên quan  R-TLMI-008, R-TLMI-009, R-TLMI-092, R-TLMI-182, R-TLMI-210
Cách kiểm       BE: gọi API xóa khối với id của một khối chuẩn ⇒ từ chối. Lưu mẫu thiếu một khối
                chuẩn ⇒ từ chối. FE: dòng khối chuẩn không render nút ✕.
```

### INV-TLMI-009 · Tên hiển thị và In đậm của một trường là duy nhất trong phạm vi một mẫu

```
Phát biểu       ∀ mẫu, ∀ trường F đang được dùng ở ≥1 ô:  mọi ô dùng F có CÙNG TenHienThi và
                CÙNG InDam. Trường không được dùng ở ô nào thì không lưu hai thuộc tính này.
Nguồn           SCR:289
Luật liên quan  R-TLMI-156, R-TLMI-157, R-TLMI-158, R-TLMI-164
Cách kiểm       FE: đặt trường X ở khối A và khối B; đổi Tên hiển thị của X ở bảng chỉnh khối A ⇒
                ô ở khối B đổi theo ngay trên trang xem trước. BE: đọc lại mẫu ⇒ đúng một giá trị
                TenHienThi cho X.
```

### INV-TLMI-010 · Ô ký tự do đang bật luôn có tiêu đề hợp lệ

```
Phát biểu       ∀ ô ký tự do có HienThi = Có:  TieuDe ≠ trống AND length(TieuDe) ≤ 60
Nguồn           SCR:295 · SCR:351
Luật liên quan  R-TLMI-187, R-TLMI-189, R-TLMI-191
Cách kiểm       BE: POST lưu mẫu có ô ký tự do bật mà tiêu đề trống ⇒ 400 + MSG_…_211;
                tiêu đề 61 ký tự ⇒ 400 + MSG_…_211. Ô ký tự do **tắt** mà tiêu đề trống ⇒ lưu được.
```

### INV-TLMI-011 · Mẫu không mang phạm vi chi nhánh

```
Phát biểu       cfg_mau_in_chung_tu KHÔNG có ChiNhanhId trong khóa duy nhất, và mọi truy vấn đọc /
                ghi mẫu KHÔNG lọc theo chi nhánh đang làm việc.
Nguồn           SCR:247 · FB:7 · BR2P BR50.6
Luật liên quan  R-TLMI-004, R-TLMI-005, R-TLMI-035
Cách kiểm       BE: lưu mẫu khi đang làm việc ở chi nhánh A, rồi đổi sang chi nhánh B và đọc mẫu ⇒
                ra đúng mẫu vừa lưu. Kiểm thêm: không có mệnh đề lọc chi nhánh trong repository.
```

### INV-TLMI-012 · Lưu là all-or-nothing

```
Phát biểu       sau một lần Lưu THẤT BẠI (validation hoặc lỗi hệ thống), trạng thái DB của mẫu
                KHÔNG đổi một bit nào — 5 bảng cfg_mau_in_* giữ nguyên như trước khi gọi.
Nguồn           SCR:318 · UC01:54 · UC01:82 · UC01:93 · AD01:33
Luật liên quan  R-TLMI-019, R-TLMI-243, R-TLMI-247, R-TLMI-249, R-TLMI-252, R-TLMI-253
Cách kiểm       BE: test rollback — ép lỗi ở giữa vòng ghi bảng con ⇒ đọc lại thấy đúng mẫu cũ,
                MSG_…_003. Test thứ hai: Lưu mẫu có lỗi validation ở khối cuối ⇒ 0 bản ghi bị đổi.
```

---

## §Y. Bảng tra message → luật

26 mã của `6.messages.md` (2 chung · 4 nghiệp vụ · 16 validate · 4 xác nhận), **cộng 2 mã dùng chung**
phải thêm theo quyết định bàn giao (§Y.1). Nội dung là **nguyên văn tiếng Việt của BA** — chép thẳng
vào `vi.ts`, cấm diễn đạt lại (luật 2). Tham số `{TenBang}` · `{TenKhoi}` · `{SoO}` giữ nguyên tên,
FE dùng `t('key', { TenBang })`.

| Mã message | Loại | Nội dung nguyên văn | Nút / hành vi | Luật dùng |
|---|---|---|---|---|
| `MSG_PMKT-E-14549_21_002` | Error | Bạn không có quyền thực hiện tác vụ này | Thông báo lỗi, chặn tác vụ | R-TLMI-034 · R-TLMI-239 (V17) |
| `MSG_PMKT-E-14549_21_003` | Error | Lỗi hệ thống, vui lòng thử lại sau | Rollback / không mở xem trước | R-TLMI-249 · R-TLMI-252 · R-TLMI-270 |
| `MSG_PMKT-E-14549_21_101` | Success | Lưu mẫu in thành công! | Toast; màn giữ nguyên, trạng thái "Đã lưu" | R-TLMI-248 |
| `MSG_PMKT-E-14549_21_102` | Info | Đã đưa về mẫu chuẩn hệ thống. Bấm Lưu để có hiệu lực | Thông báo sau khi xác nhận | R-TLMI-017 |
| `MSG_PMKT-E-14549_21_103` | Info | Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in theo mẫu chuẩn hệ thống | Hiện **một lần** trên màn xem trước, không phải lỗi | R-TLMI-260 |
| `MSG_PMKT-E-14549_21_104` | Info | Đã thêm khối tự do trước Chữ ký. Nháy đúp một ô để chọn trường, hoặc kéo trường từ bảng bên phải thả vào ô | Thông báo hướng dẫn sau khi thêm khối | R-TLMI-124 |
| `MSG_PMKT-E-14549_21_201` | Error | Tiêu đề bản in không được để trống, tối đa 255 ký tự | Chặn Lưu, mở khối chứa lỗi | R-TLMI-085 · R-TLMI-239 (V01) |
| `MSG_PMKT-E-14549_21_202` | Error | Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36 | Chặn Lưu, báo tại ô | R-TLMI-086 · R-TLMI-239 (V02) |
| `MSG_PMKT-E-14549_21_203` | Error | Bảng "{TenBang}" phải giữ lại ít nhất 1 cột hiển thị | Chặn, báo tại khối; tham số `{TenBang}` | R-TLMI-104 · R-TLMI-239 (V03) |
| `MSG_PMKT-E-14549_21_204` | Error | Tên hiển thị của cột không được để trống, tối đa 100 ký tự | Chặn Lưu, báo tại ô | R-TLMI-102 · R-TLMI-239 (V04) |
| `MSG_PMKT-E-14549_21_205` | Error | Độ rộng cột phải là số nguyên từ 3 đến 90 | Chặn Lưu, báo tại ô | R-TLMI-108 · R-TLMI-239 (V05) |
| `MSG_PMKT-E-14549_21_206` | Error | Tên khối tự do không được để trống, tối đa 60 ký tự | Chặn, báo tại ô — áp ở **cả hai chỗ** nhập tên khối | R-TLMI-121 · R-TLMI-127 · R-TLMI-239 (V06) |
| `MSG_PMKT-E-14549_21_207` | Error | Mỗi mẫu tối đa 10 khối tự do | Chặn hành động thêm | R-TLMI-125 · R-TLMI-239 (V07) |
| `MSG_PMKT-E-14549_21_208` | Error | Mỗi khối tự do tối đa 20 dòng | Chặn hành động thêm dòng | R-TLMI-129 · R-TLMI-133 · R-TLMI-239 (V08) |
| `MSG_PMKT-E-14549_21_209` | Error | Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB | Chặn chọn tệp | R-TLMI-069 · R-TLMI-239 (V10) |
| `MSG_PMKT-E-14549_21_210` | Error | Mã màu phải có dạng #rrggbb | Chặn, báo tại ô | R-TLMI-066 · R-TLMI-239 (V11) |
| `MSG_PMKT-E-14549_21_211` | Error | Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự | Chặn Lưu, báo tại ô | R-TLMI-189 · R-TLMI-188 · R-TLMI-239 (V12) |
| `MSG_PMKT-E-14549_21_212` | Error | Tên hiển thị và chữ tự do tối đa 255 ký tự | Chặn, báo tại ô | R-TLMI-147 · R-TLMI-157 · R-TLMI-237 · R-TLMI-239 (V13) |
| `MSG_PMKT-E-14549_21_213` | Error | Căn lề phải là số từ 0 đến 5 cm | Chặn, báo tại ô | R-TLMI-061 · R-TLMI-239 (V14) |
| `MSG_PMKT-E-14549_21_214` | Error | Số cột để tự động in ngang phải là số nguyên từ 1 đến 50 | Chặn, báo tại ô | R-TLMI-057 · R-TLMI-239 (V15) |
| `MSG_PMKT-E-14549_21_215` | Error | Cỡ chữ phải là số nguyên từ 8 đến 20 | **Chỉ chặn phía máy chủ** | R-TLMI-063 · R-TLMI-239 (V16) |
| `MSG_PMKT-E-14549_21_216` | Error | Mỗi khối tự do tối đa 6 cột | Chặn hành động thêm cột | R-TLMI-130 · R-TLMI-133 · R-TLMI-239 (V09) |
| `MSG_PMKT-E-14549_21_401` | Confirmation | Mẫu đã có thay đổi chưa lưu. Bạn muốn làm gì? | **3 nút**: Lưu và đóng / Không lưu / Ở lại | R-TLMI-251 · R-TLMI-252 · R-TLMI-253 · R-TLMI-254 |
| `MSG_PMKT-E-14549_21_402` | Confirmation | Mọi tùy chỉnh (kể cả khối tự do, thứ tự khối, cột bảng, chữ ký) sẽ trở về mẫu chuẩn hệ thống. Thay đổi chỉ có hiệu lực khi bạn bấm Lưu. Tiếp tục? | 2 nút xác nhận / hủy (**tên nút không có trong tài liệu**) | R-TLMI-015 · R-TLMI-016 · R-TLMI-020 |
| `MSG_PMKT-E-14549_21_403` | Confirmation | Xóa khối "{TenKhoi}" cùng các ô trong đó? | 2 nút xác nhận / hủy (**tên nút không có trong tài liệu**); tham số `{TenKhoi}` | R-TLMI-175 · R-TLMI-211 |
| `MSG_PMKT-E-14549_21_404` | Confirmation | Vùng chọn có {SoO} ô đang có nội dung. Gộp thì chỉ giữ nội dung của ô đầu tiên, các ô còn lại mất nội dung. Tiếp tục? | 2 nút xác nhận / hủy (**tên nút không có trong tài liệu**); tham số `{SoO}` | R-TLMI-136 · R-TLMI-138 · R-TLMI-139 |

### Y.1 — Mã dùng chung phải thêm (BA chưa cấp mã riêng)

Hai tình huống dưới đây là **quyết định triển khai** (`04-quyet-dinh-ban-giao.md §3`, nợ **L-4**),
không có trong `6.messages.md`. Dùng **mã dùng chung** cho tới khi BA cấp mã riêng.

| Mã | Loại | Dùng cho | Quyết định | Luật dùng |
|---|---|---|---|---|
| `MSG_COMMON_001` | Error | **Xung đột phiên bản khi Lưu** — `phienBan` trong payload lệch bản ghi hiện tại | **C06** · `04` §3 · khóa lạc quan; kèm một key i18n riêng cho câu hướng dẫn nạp lại | R-TLMI-258 |
| `MSG_COMMON_003` | Error | **Thiếu quyền In** khi gọi API in mẫu tùy chỉnh | **C15** · `04` §3 · theo BR25.2. **KHÔNG** mở rộng `MSG_PMKT-E-14549_21_002` như `AD02:27` làm — `6.messages.md` khai mã đó riêng cho quyền *Thiết lập mẫu in* | R-TLMI-033 · R-TLMI-261 |

⚠ Khi BA cấp mã `MSG_PMKT-E-14549_21_…` cho hai tình huống này: sửa
`04-quyet-dinh-ban-giao.md` trước, rồi sửa bảng này và hai luật trên, rồi mới sửa code.

### Y.2 — Mã message chưa luật nào dùng

**KHÔNG CÓ.** Cả 26 mã của `6.messages.md` đều được ít nhất một luật `R-TLMI-…` tham chiếu.

Kiểm ngược: `6.messages.md` không có mã `001`, `105+`, `217+`, `2xx` ngoài 201–216, `3xx`, `405+`.
Epic `_21` **KHÔNG tái dùng** mã nào của epic `_20` — đừng import `MSG_PMKT-E-14549_20_*` vào i18n
của module này. Ba cặp trùng nội dung khác mã (`_20_201`↔`_21_215`, `_20_202`↔`_21_213`,
`_20_203`↔`_21_214`) và hai mã chung (`_002`, `_003`) là **nhân đôi có chủ ý**.

### Y.3 — Chuỗi người dùng thấy nhưng **CHƯA có mã message** (⚠ `msg.sh` sẽ báo `THIEU`)

| Nguyên văn tiếng Việt | Nơi dùng | Nguồn | Luật |
|---|---|---|---|
| "Đơn vị không cho phép in chứng từ chưa ghi sổ" | tooltip nút In bị disable | `S20:155` | R-TLMI-261 |
| "Đơn vị không cho phép in chứng từ đã khóa sổ" | tooltip nút In bị disable | `S20:156` | R-TLMI-261 |
| chữ gợi ý ở ô trống đang chọn khi bật Hiện lưới căn chỉnh | trang xem trước | `SCR:291` — **không cho nguyên văn** | R-TLMI-177 |
| tên hai nút của các hộp xác nhận `_402` / `_403` / `_404` | hộp thoại | `SCR:363` · `SCR:365` · `SCR:367` — **không nêu tên nút** | R-TLMI-015, R-TLMI-138, R-TLMI-175 |
| câu hướng dẫn nạp lại khi xung đột phiên bản | hộp lỗi sau khi Lưu thất bại | — (quyết định `04` §3) | R-TLMI-258 |

Các dòng này là chuỗi người dùng thấy ⇒ theo **luật 2** phải có key i18n ở cả `vi.ts` và `en.ts`,
giữ **nguyên văn tiếng Việt**. Tài liệu **chưa cấp mã** ⇒ `msg.sh` báo `THIEU` — **đã chấp nhận** ở
`04-quyet-dinh-ban-giao.md` (nợ **L-5**), xem thêm §Z mục `Z-01`.

---

## §Z. Chỗ tài liệu còn THIẾU QUY ĐỊNH (sau khi khử chéo bốn báo cáo trích)

> Đây là phần **tài liệu im lặng** — khác hẳn `01-conflict.md` vốn ghi chỗ tài liệu **tự mâu thuẫn**.
>
> ✅ **Phần lớn đã được trả lời** ở `04-quyet-dinh-ban-giao.md` (uỷ quyền của user, 2026-09-19).
> **§Z.0 là bảng tra chính** — nó nói mục nào đã chốt và chốt ra sao. Các mục §Z.1…§Z.6 bên dưới
> **giữ nguyên văn mô tả khoảng trống** để thấy tài liệu BA gốc im lặng ở đâu; đọc chúng cùng §Z.0,
> đừng đọc một mình. **Không mục nào trong §Z còn chặn code.**
>
> Mục nào §Z.0b liệt kê là **CÒN HỞ** thì vẫn phải hỏi BA trước khi nghiệm thu.
>
> Đã **loại bỏ** các mục "thiếu quy định" mà báo cáo A1 (đọc `SCR:1-208`) nêu nhưng nửa sau file
> `SCR` **đã trả lời**: chú giải `Y*` (SCR:242) · miền giá trị mọi ô số (bảng Validation SCR:338-356
> và SCR:302) · toàn bộ enum (SCR:254, 275, 277, 287, 298, 302) · thuật toán Chia đều về 100%
> (SCR:279) · ràng buộc tổng = 100 và xử lý khi lệch (SCR:278, 314, 318) · xóa khối chuẩn và hỏi xác
> nhận (SCR:263, 292) · trần lưới khối tự do 20×6 và trần 10 khối (SCR:284-285) · sàn 1 dòng / 1 cột
> (SCR:285) · giới hạn số ô ký (SCR:297 — không giới hạn) · nội dung 26 message (`6.messages.md`) ·
> Đặt lại có hỏi xác nhận và có bỏ khối tự do không (SCR:310) · số bước Hoàn tác = 60 (SCR:317) ·
> ô Cộng với cột chữ (MT:83-84 — Hide) · nội dung khi Tách ô (SCR:286) · thứ tự ưu tiên báo lỗi ở mức
> khối (SCR:316) · mẫu chuẩn lưu ở đâu (CRUD:15 — không có entity riêng).

### Z.0 — Trạng thái từng mục `Z-nn` sau khi chốt — ĐỌC TRƯỚC

`01-conflict.md` ghi **38 mục `C01…C38`**, nay **0 mục `OPEN`** (32 `CLOSED-BA (Dat · 2026-09-19)`,
4 `CLOSED-AUTO`). Vì vậy **§Z không còn chặn gì**. Bảng dưới chia §Z làm hai loại:

- **ĐÃ CHỐT** — `04-quyet-dinh-ban-giao.md` đã trả lời; cột cuối ghi **quyết định** và chỗ đọc chi tiết.
  Với các mục này, phần mô tả ở §Z.1…§Z.6 bên dưới giữ nguyên để **thấy tài liệu gốc im lặng chỗ nào**,
  nhưng **câu trả lời nằm ở đây và ở `04-quyet-dinh-ban-giao.md`**.
- **CÒN HỞ** — `04` không chốt; vẫn là khoảng trống tài liệu, **không chặn code** nhưng phải hỏi BA
  trước khi nghiệm thu.

#### Z.0a — Mục đã chốt

| `Z-nn` | Mục `C` | Quyết định (rút gọn) | Đọc chi tiết |
|---|---|---|---|
| `Z-01` (tooltip nút In chưa có mã) | **C14** | Giữ **nguyên văn** `S20:155-156`, đặt key i18n cục bộ; `msg.sh` báo `THIEU` cho tới khi BA cấp mã — **chấp nhận** (nợ L-5) | `04` §3 · §5 |
| `Z-02` (thiếu message nhánh thiếu quyền In) | **C15** | Dùng **`MSG_COMMON_003`** theo BR25.2. **Không** mở rộng `MSG_PMKT-E-14549_21_002` như `AD02:27` | `04` §3 |
| `Z-05` (`MSG_103` "một lần" là gì) | **C22** | **Một lần mỗi lần mở màn xem trước bản in.** Không nhớ qua phiên, không nhớ theo người dùng | `04` §3 |
| `Z-06` (*Lưu và đóng* có hiện `MSG_101` không) | **C23** | **Có** — hiện toast `MSG_101` rồi mới đóng màn; toast sống độc lập với màn (BR26.1) | `04` §3 |
| `Z-07` (cấu trúc cột 5 bảng `cfg_mau_in_*`) | **C09** + **C37** | **Không còn áp dụng** — mô hình đổi sang **JSON** (Q-01). 5 "entity" thành 5 nhánh JSON; hợp đồng kỹ thuật là **JSON schema** viết ở `/plan-be` | `04` §1 Q-01 · §2 |
| `Z-08` (cấu trúc lưới khối tự do không có chỗ lưu) | **C09** | JSON schema **phải phủ** số dòng, số cột, `rowSpan`/`colSpan`, loại ô, nội dung ô, căn ô | `04` §2 |
| `Z-09` (ảnh nền lưu ở đâu) | **C08** | Cột **`bytea`** trên chính bảng đã có: `anh_nen` + `anh_nen_kieu_tep` + `anh_nen_ten_tep`; JSON chỉ giữ cờ `nen.kieu='ANH'`; upload `multipart`, endpoint riêng (nợ L-2) | `04` §2 · §5 |
| `Z-12` (Chia đều 100% khi đang lọc) | **C31** | Áp cho **mọi cột đang tick in**, không phụ thuộc ô *Tìm cột* — ô tìm chỉ lọc hiển thị | `04` §4 |
| `Z-14` (cột / lưới / trường **bị xóa** khỏi form) | **C10** | **Bỏ qua im lặng khi in** (không in, không lỗi, bản in không vỡ); **báo nhẹ khi mở màn**: hiện mờ + nhãn "không còn trên form", loại khỏi mẫu khi Lưu | `04` §2 |
| `Z-20` (thứ tự "lỗi đầu tiên" trong một khối) | **C21** | Theo thứ tự khối trong Bố cục mẫu; trong một khối: **ô ở bảng chỉnh trước** (trên → xuống), **rồi ô lưới** trên trang xem trước (trái → phải, trên → xuống) | `04` §3 |
| `Z-21` (ẩn khối Tiêu đề rồi còn bắt buộc `MSG_201` không) | **C18** | **Khối đang ẩn thì bỏ qua validate của khối đó**; bật lại khối thì validate lại ngay | `04` §3 |
| `Z-24` (vị trí logo khi Căn lề ≠ Trái) | **C29** | Logo luôn **bên trái khối thông tin đơn vị, cùng hàng với dòng đầu tiên**; căn lề áp cho **cả cụm** (logo + các dòng chữ) | `04` §4 |
| `Z-25` (không phân biệt theo chung / riêng) | **C16** | **Giữ đúng tài liệu và Figma** — nút *Theo thiết lập chung* ở mức nhóm, không nhãn từng ô. Không tự thêm UI ngoài đặc tả. Ghi nhận **rủi ro UX**, BA soát lại | `04` §3 · §7 |
| `Z-26` (đổi Khổ/Hướng trên thanh Xem trước) | **C17** | **Giữ đúng tài liệu** — `SCR:79` nói thẳng "đổi ở đây là đổi mẫu". Hai ô là **một trường**, đồng bộ hai chiều tức thời. Ghi nhận **rủi ro UX**, BA soát lại | `04` §3 · §7 |
| `Z-27` (`Bắt buộc = Y` vs lưu NULL) | **C28** | `Y` đọc là **"bắt buộc có giá trị hiệu dụng"**, không phải `NOT NULL`. Với JSON: **khóa vắng mặt = theo chung** | `04` §4 |
| `Z-28` (quyền chi nhánh A sửa mẫu cho B, C) | **C24** | **Không thêm cảnh báo** — tài liệu không yêu cầu, thêm hộp thoại ngoài đặc tả là tự đặt luật. Ghi nhận để BA cân nhắc | `04` §3 |
| `Z-29` (phạm vi cộng gộp 3 loại chứng từ) | **C30** | **Giữ giới hạn của BR51.5**: chỉ Hoá đơn, phiếu xuất kho, phiếu nhập kho — đã viết vào `R-TLMI-119` và `R-TLMI-266` | `04` §2 |
| `Z-30`, `Z-31` (lỗi hình thức ma trận) | **C34** | `CLOSED-AUTO` — đề nghị BA sửa file ma trận (nợ §7 mục 4) | `04` §7 |
| `Z-32` (ma trận không phủ hộp thoại con) | **C33** | `CLOSED-AUTO` — ghi nhận để plan FE không tưởng ma trận đã phủ hết màn | — |
| `Z-33` (mã quyền) | **C13** | **Hai tầng**: `HTMauIn.View` / `HTMauIn.Edit` (đã seed `V1149`) **cộng** quyền xem chi tiết của nghiệp vụ (`<ChucNang>.View.Detail`). Đặt hằng số ở `MaQuyenMauIn` để sau đổi một chỗ (nợ L-3, điểm nối Q-15) | `04` §2 · §5 · §6 |
| `Z-34` (nghiệp vụ nào có mẫu tùy chỉnh) | **C13** liên đới | Vẫn do epic nghiệp vụ khai; bản này gate bằng `HTMauIn.*` nên **không chặn** — xem `Z-33` | `04` §2 |
| `Z-37` (giá trị mặc định của epic `_20`) | **C12** | Làm **"thiết lập chung tối thiểu"** — đúng phần `_21` cần, lưu JSON trên cấu hình tenant hiện có, **không** dựng `cfg_tenant` / `cfg_chi_nhanh` mới (nợ L-6) | `04` §1 Q-03 |
| `Z-36` (5 chức danh, cột người ký) | **C12** + **C05** | Tạm đọc hồ sơ đơn vị từ **Thông tin công ty (tenant)** vì `cfg_chi_nhanh` chưa có; mọi chỗ đi qua cổng `HoSoDonViPort.theoChiNhanh(chiNhanhId)` để sau đổi nguồn không sửa tầng trên (nợ L-7, điểm nối Q-14) | `04` §1 Q-03 · §6 |
| — | **C11** | Epic chạy theo **bộ BR Phase 2** cho riêng chức năng này (nợ L-8). 23 luật + 3 bất biến đứng trên nền này — danh sách ở `00-source-map.md §4.3` | `04` §1 Q-02 |
| — | **C26** | `cfg_mau_in_chung_tu` xếp **nhóm 1 (cấu hình hệ thống)** của BR50.6 — không khai `ChiNhanhId`. Đề nghị BA bổ sung vào bảng BR50.6 | `04` §4 · §7 |
| — | **C32** | Độ sâu Hoàn tác = **60 bước** trong một phiên (đã là `R-TLMI-223`) | `04` §4 |
| — | **C38** | `bieuMau` và mẫu in chứng từ là **hai chức năng độc lập, không gộp**; chỉ dùng lại kỹ thuật (`useDesignerStore`, `keoTha`, `PropField`) | `04` §3 |
| — | **C25**, **C27** | `CLOSED-AUTO` — AD lệch UC (đã ghi ở `00-source-map.md §3.1`) · nguồn dữ liệu khối Xem trước | — |

#### Z.0b — Mục còn hở (không chặn code, phải hỏi BA trước nghiệm thu)

`Z-03` (Độ đậm thiếu dòng Validation + mã message) · `Z-04` (10 ô màu chưa liệt kê, Figma đếm 9) ·
`Z-10` (Lưu có giữ id cũ không) · `Z-11` (trùng tên khối tự do) · `Z-13` (thời điểm tự chia lại độ
rộng khi có cột mới) · `Z-15` (giới hạn ký tự của Tên người ký gõ tay và Dòng ghi chú) · `Z-16`
(dòng ghi chú của 5 chức danh có sửa được không) · `Z-17` (Đặt lại có phải bước Hoàn tác không) ·
`Z-18` (In đậm áp cho vùng chọn hỗn hợp trường + Chữ tự do) · `Z-19` (nội dung dài hơn chỗ chứa khi
đổi ô) · `Z-22` (quy tắc đọc số cho Số tiền bằng chữ) · `Z-23` (`n` trong "Khối tự do \<n\>") ·
`Z-35` (đặc tả form của epic nghiệp vụ) · `Z-38`…`Z-40` (tooltip BR7 của `_20` · hành vi chung bản in
chứng từ · danh mục mẫu cố định).

Hai mục trong đó — **`Z-19`** và **`Z-18`** — chạm hành vi người dùng thấy được; nếu gặp lúc code thì
chọn cách **an toàn nhất** (không mất dữ liệu) và ghi lại vào `04-quyet-dinh-ban-giao.md`, không
lặng lẽ tự quyết.

### Z.1 — Thiếu mã message / thiếu nguyên văn

| # | Chỗ thiếu | Vì sao chặn | Nguồn | Luật liên quan |
|---|---|---|---|---|
| **Z-01** | Các chuỗi ở §Y.3 là text người dùng thấy nhưng **không có mã `MSG_…`** | Luật 2 buộc có key i18n; `msg.sh` không có mã để đối chiếu ⇒ báo `THIEU` | `S20:155-156` · `SCR:291` · `SCR:363/365/367` | R-TLMI-177, R-TLMI-261 |
| **Z-02** | Người dùng **không có quyền In** gọi API in mẫu tùy chỉnh thì trả message nào? `MSG_002` được `MSG:7` mô tả là "Không có quyền **Thiết lập mẫu in**"; UC02 NL2 chỉ nói disable nút | Thiếu message cho một nhánh từ chối thật. AD02:26-27 tự mở rộng `MSG_002` sang nhánh này — **không được lấy AD làm nguồn luật** | `MSG:7` · `UC02:53-56` · `AD02:26-27` | R-TLMI-034, R-TLMI-261 |
| **Z-03** | **Độ đậm hình nền** có miền 5–100 % nhưng **không có dòng nào trong bảng Validation** và không có mã message | Vi phạm miền thì báo gì, chặn ở đâu | `SCR:302` vs `SCR:338-356` | R-TLMI-072 |
| **Z-04** | Tài liệu nói **"10 ô màu"** nhưng **không liệt kê 10 mã màu**; Figma đếm được **9** ô preset + ô hex | Không code được hằng số bảng màu, và số đếm lệch | `SCR:301` · `SCR:104` · `FIGMA` frame 1 | R-TLMI-066 |
| **Z-05** | `MSG_103` hiện **"một lần"** — một lần **mỗi lần mở xem trước**, **mỗi phiên**, hay **mỗi người dùng**? | Khác nhau ở chỗ lưu cờ đã-hiện (state màn / session / DB) | `UC02:22` · `SCR:328` | R-TLMI-260 |
| **Z-06** | Nhánh *Lưu và đóng* (`MSG_401`) có hiện `MSG_101` trước khi đóng không? | UC01:87 chỉ nói "chạy bước 6–9 rồi đóng"; bước 9 có MSG_101 nhưng màn đã đóng | `UC01:87` · `UC01:55` | R-TLMI-248, R-TLMI-252 |

### Z.2 — Thiếu cấu trúc dữ liệu

| # | Chỗ thiếu | Vì sao chặn | Nguồn | Luật liên quan |
|---|---|---|---|---|
| **Z-07** | **Không file nào khai cột của 5 bảng `cfg_mau_in_*`** (khóa chính, khóa ngoại, cột thứ tự, cột phân biệt loại khối). Package BA không có ERD | Chặn `/plan-be` — không thiết kế được entity | `CRUD:5-9` · `SCR:376` (chỉ liệt kê tên entity) | toàn nhóm A, H, I, K |
| **Z-08** | **Cấu trúc lưới của khối tự do** (số dòng, số cột, gộp / tách ô, vị trí ô, căn lề, nghiêng) thao tác được nhưng **không có tên trường nào** để lưu. `cfg_mau_in_khoi_o` chỉ khai `TenHienThi` và `InDam` | Chặn thiết kế bảng ô lưới | `SCR:181-182` · `SCR:187` · `SCR:79` · `SCR:81` | R-TLMI-132 … R-TLMI-161 |
| **Z-09** | **Ảnh nền** (≤1MB) lưu ở đâu — cột nào, bảng nào, binary hay đường dẫn; có giới hạn kích thước điểm ảnh; có bị Hoàn tác khôi phục không | Chặn thiết kế DB và luồng upload | `SCR:302` · `SCR:317` · `SCR:376` | R-TLMI-069 |
| **Z-10** | Lưu là "xóa hết bản cũ, ghi bản mới" — **có giữ id cũ không?** | Không kiểm được ảnh hưởng tới dữ liệu tham chiếu (nếu có) | `SCR:318` | R-TLMI-247 |

### Z.3 — Thiếu quy tắc nghiệp vụ

| # | Chỗ thiếu | Vì sao chặn | Nguồn | Luật liên quan |
|---|---|---|---|---|
| **Z-11** | Hai khối tự do có được **trùng tên** không? | Quyết định có unique check khi tạo / sửa tên | `SCR:59` · `SCR:177` · `SCR:284` | R-TLMI-121 |
| **Z-12** | Nút **Chia đều về 100%** khi lưới cột **đang lọc** bằng ô Tìm cột: áp cho mọi cột hay chỉ cột đang hiện? SCR:280 chỉ cấm kéo thả khi lọc | Kết quả độ rộng khác nhau | `SCR:279` · `SCR:280` | R-TLMI-114, R-TLMI-117 |
| **Z-13** | Việc **tự chia lại độ rộng khi có cột mới ở phiên bản sau** xảy ra ở thời điểm nào — khi mở màn, khi Lưu, hay khi in? | Ba chỗ đặt code khác nhau, hành vi khác nhau | `SCR:272` · `SCR:279` | R-TLMI-093 |
| **Z-14** | **Cột / lưới / trường bị BỎ khỏi form** ở phiên bản sau thì mẫu đã lưu xử lý sao (bỏ trống? thành ô trống? báo lỗi?). Tài liệu chỉ quy định chiều **thêm** | Bản in có thể vỡ hoặc lỗi dựng | `SCR:272` · `SCR:290` · `UC01:26` | R-TLMI-093, R-TLMI-167 |
| **Z-15** | **Tên người ký** gõ tay ở ô ký tự do và **Dòng ghi chú**: có giới hạn ký tự không, có bắt buộc không? Chỉ "tiêu đề in ra" có ràng buộc ≤60 | Không viết được validator | `SCR:295` · `SCR:198` · `SCR:200` | R-TLMI-187, R-TLMI-190 |
| **Z-16** | **Dòng ghi chú của 5 chức danh chuẩn** có sửa được trong mẫu không? `SCR:200` khai Cho phép sửa = Y nhưng `SCR:295` chỉ nói "tiêu đề in ra sửa được" | Có hay không cột lưu + ô nhập | `SCR:200` · `SCR:295` · `SCR:296` | R-TLMI-190 |
| **Z-17** | **Đặt lại mẫu chuẩn** có phải một bước **Hoàn tác được** không? BR2 nói rõ nút Theo thiết lập chung là một bước; BR9 / BR10 im lặng với Đặt lại | Quyết định có push snapshot vào undo stack | `SCR:253` · `SCR:310` · `SCR:317` | R-TLMI-016, R-TLMI-224 |
| **Z-18** | Nút **In đậm / Nghiêng / Căn** áp cho vùng chọn có ô **khác loại nội dung** (vừa trường vừa Chữ tự do) thì kết quả ra sao? In đậm là thuộc tính *của trường* (dùng chung cả mẫu) nhưng nút lại áp *theo vùng ô* | Hai mô hình dữ liệu đụng nhau | `SCR:227` · `SCR:289` | R-TLMI-156, R-TLMI-163 |
| **Z-19** | Kéo ô gộp thả lên ô thường: "kích thước gộp giữ theo ô" — nội dung **dài hơn chỗ chứa** thì sao? | Hành vi hiển thị và in không xác định | `SCR:288` | R-TLMI-154 |
| **Z-20** | Thứ tự **ô lỗi trong một khối** khi khối có cả ô ở bảng chỉnh lẫn ô lưới trên trang xem trước. BR10 chỉ nói "thứ tự ô trong khối" | Quyết định thứ tự validate ở BE và ô nào được focus | `SCR:316` | R-TLMI-243, R-TLMI-244 |
| **Z-21** | Khối **Tiêu đề** bị **ẩn** (con mắt = Không) thì ràng buộc "Nội dung không trống" còn áp không? | Ẩn khối rồi mà vẫn chặn lưu vì ô trong khối ẩn ⇒ người dùng bế tắc | `UC01:24` · `MSG:23` · `SCR:340` | R-TLMI-085, R-TLMI-239 (V01) |
| **Z-22** | "**Số tiền bằng chữ** đọc từ ô tổng thanh toán **theo quy tắc đọc số chung**" — quy tắc đọc số chung không được trích mã BR nào trong phạm vi tài liệu này | Không biết dùng quy tắc nào | `SCR:290` | R-TLMI-165 |
| **Z-23** | `n` trong tên gợi ý `"Khối tự do <n>"` là số gì — số khối hiện có + 1, hay số lớn nhất từng dùng + 1? | Kết quả khác nhau sau khi xóa khối giữa | `SCR:59` · `SCR:284` | R-TLMI-120 |
| **Z-24** | **Vị trí logo khi Căn lề khối đầu trang ≠ Trái**. `S20:140` chỉ mô tả "Logo đặt bên trái khối thông tin đơn vị, cùng hàng với dòng đầu tiên" | Bản in chứng từ có thể lệch so với báo cáo | `S20:140` · `S20:143` · `SCR:267` | R-TLMI-049, R-TLMI-078 |

### Z.4 — Cần BA xác nhận "là chủ ý, không phải sót đặc tả"

| # | Chỗ cần xác nhận | Rủi ro nếu code thẳng | Nguồn | Luật liên quan |
|---|---|---|---|---|
| **Z-25** | Người dùng **không phân biệt được** ô *theo chung* và ô *riêng* (không nhãn, không đổi Show/Hide), **và** không có cách đưa riêng một ô về theo chung | Đổi 1 ô rồi muốn hoàn lại chỉ ô đó ⇒ buộc reset cả nhóm và gõ lại các ô khác, không có chỉ báo nào | `MT:103` · `SCR:253` | R-TLMI-042, R-TLMI-045 |
| **Z-26** | Đổi Khổ / Hướng giấy **trên thanh Xem trước** biến ô thành *riêng* vĩnh viễn, trong khi thanh Xem trước **luôn hiện ở cả 6 khối** | Một thao tác tưởng chỉ "để xem" làm mẫu ngừng kế thừa thiết lập chung | `SCR:256` · `MT:67` · `MT:71` | R-TLMI-044, R-TLMI-228 |
| **Z-27** | Cột **Bắt buộc = Y** cho các ô Giấy và chữ (`SCR:93-101`) trong khi giá trị lưu **có thể trống** (theo chung, `SCR:318`) | Đọc thẳng bảng sẽ sinh `NOT NULL` ⇒ **phá vỡ kế thừa động**. Đề nghị BA ghi rõ `Y` = bắt buộc **giá trị hiệu dụng** | `SCR:93-101` · `SCR:318` | R-TLMI-037 |
| **Z-28** | Người có quyền ở **chi nhánh A** sửa mẫu áp cho **chi nhánh B, C** — có cảnh báo gì không? | Rủi ro nghiệp vụ thật, tài liệu không cấp message nào | `FB:7` · `UC01:11` · `SCR:247` | R-TLMI-035 |
| **Z-29** | `SCR:281` nói cộng gộp mặt hàng **không nhắc lại** giới hạn phạm vi "Hóa đơn, phiếu xuất/nhập kho" của `BR51.5` và `S20:160` | Code theo `SCR:281` trần sẽ gộp cả Phiếu chi, Chứng từ mua dịch vụ… | `SCR:281` vs `BR2P BR51.5` · `S20:160` | R-TLMI-119, R-TLMI-266 |

### Z.5 — Lỗi hình thức của chính tài liệu (đề nghị BA sửa file)

| # | Lỗi | Nguồn |
|---|---|---|
| **Z-30** | `MT:108` mở đầu bằng marker hỏng `\1`, **không có neo `\1`** ở bất kỳ ô nào trong thân ma trận `MT:57-93`. Nội dung ("Cột bỏ tick in giữ nguyên số Rộng % đang có, có thể để trống") đúng với `SCR:278`, nhưng không biết gắn vào dòng nào | `MT:108` |
| **Z-31** | `MT:3` nói ma trận có chú thích `Y*`, nhưng thân ma trận `MT:57-93` **không có ô nào mang marker `Y*`** — các điều kiện `Y*` đã chuyển hết thành `(đk-HG)` / `(đk-HN)` | `MT:3` · `SCR:242` |
| **Z-32** | Ma trận **không phủ hộp thoại con**: hộp Đặt tên khối (`SCR:284`), hộp chọn trường cạnh ô (`SCR:288`), bốn hộp xác nhận `MSG_401…404`. Trục I1 chỉ có 6 giá trị = 6 khối | `MT:38-45` · `SCR:284-293` · `MSG:44-47` |

### Z.6 — Ngoài phạm vi epic (do nơi khác quyết — **không phải lỗi tài liệu**, nhưng chưa code được ở đây)

| # | Hạng mục | Do ai quyết | Nguồn |
|---|---|---|---|
| **Z-33** | **Mã quyền** Thiết lập mẫu in và quyền In | epic của từng nghiệp vụ | `FB:9` · `UC01:11` · `SCR:248` |
| **Z-34** | **Chứng từ nào, nghiệp vụ nào** có mẫu tùy chỉnh | epic của từng nghiệp vụ | `FB:9` |
| **Z-35** | **Đặc tả form** (các ô, các lưới, cột của lưới) làm nguồn cho mẫu chuẩn và kho trường | epic nghiệp vụ | `UC01:16` · `CRUD:15` · `SCR:290` |
| **Z-36** | Danh sách **5 chức danh** và các cột `TieuDeNguoiKy*` / `TenNguoiKy*` | màn Thiết lập người ký (`TTC`, epic PMKT-E-14549_CauHinhBanDau) | `SCR:295` · `TTC:46-50` |
| **Z-37** | Nội dung **bảy dòng thông tin đơn vị** và toàn bộ giá trị mặc định của Giấy và chữ | epic PMKT-E-14549_20 Cấu hình báo cáo chứng từ | `FB:9` · `UC01:17` · `S20` |
| **Z-38** | **Tooltip khi nút In bị disable** | BR7 của màn Cấu hình báo cáo chứng từ (epic _20) | `UC02:55` |
| **Z-39** | **Hành vi chung của bản in chứng từ** (nút In, Xuất file, định dạng xuất) và hành vi màn xem trước bản in | ngoài epic | `UC02:25` · `SCR:326` |
| **Z-40** | Danh mục **mẫu in cố định theo quy định** (01-TT, 02-VT…) | ngoài epic | `FB:7` |

---

*Hết `02-rules.md`. File này là **nguồn sự thật duy nhất để code** — 271 luật `CHỐT`, 0 luật bị chặn.
Chỗ nào file này lệch tài liệu BA thì lý do nằm ở [`04-quyet-dinh-ban-giao.md`](04-quyet-dinh-ban-giao.md);
BA chốt khác thì sửa file `04` trước, rồi sửa file này, rồi mới sửa code.
`00-source-map.md` · `01-conflict.md` · `03-scenarios.md` · `04-quyet-dinh-ban-giao.md` do người khác
lập — không sửa bốn file đó từ đây.*
