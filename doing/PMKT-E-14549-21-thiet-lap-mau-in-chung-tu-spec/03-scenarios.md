# PMKT-E-14549_21 Thiết lập mẫu in chứng từ — Kịch bản & expected state

| | |
|---|---|
| Phiếu yêu cầu | `pmkt-docs/ba/Phase_2/PMKT-E-14549_21_ThietLapMauInChungTu/` ⚠ vùng đóng băng |
| Mã viết tắt | **TLMI** → `S-TLMI-nnn` |
| Ngày lập | **2026-09-19** |
| Nguồn suy ra | `02-rules.md` (271 luật · 12 bất biến) + `01-conflict.md` (38 mục) + **`04-quyet-dinh-ban-giao.md`** |
| Trạng thái | **78 kịch bản** · **0 kịch bản bị chặn** |

> ✅ **Đã đồng bộ với [`04-quyet-dinh-ban-giao.md`](04-quyet-dinh-ban-giao.md) ngày 2026-09-19.**
> `01-conflict.md` còn **0 mục `OPEN`** — 32 mục chuyển `CLOSED-BA (Dat · 2026-09-19)`. Mọi dấu ⛔
> của bản trước đã gỡ; 7 kịch bản bị chặn được viết lại theo đúng kết cục đã chốt, và 18 kịch bản
> mới (`S-TLMI-061` … `S-TLMI-078`) phủ các mục §B nay đã hết bị chặn.
>
> ⚠ Ba quyết định gốc **thay đổi expected state của gần như mọi kịch bản** so với bản trước:
> **Q-01** mô hình lưu trữ = **JSON**, không dựng 5 bảng quan hệ · **Q-02** áp bộ BR **Phase 2** ·
> **Q-03** làm thêm tầng "thiết lập chung tối thiểu". Mục nào mang nhãn `[AI-ĐỀ-XUẤT]` trong file
> 04 thì **BA vẫn cần soát lại** — BA chốt khác thì sửa file 04 trước, rồi sửa kịch bản ở đây.

> **Đọc file này thế nào.** Mỗi kịch bản có `Nhóm` · `Tầng kiểm` · `Luật phủ` · `TIỀN ĐỀ` ·
> `THAO TÁC` · `EXPECTED`. Expected state là **giá trị cụ thể** — đường dẫn JSON, khóa vắng mặt, số bản ghi,
> **mã message nguyên văn**, nhãn badge (`Đã lưu` / `Chưa lưu` / `Có lỗi`).
>
> Kịch bản nào có dòng `Quyết định` thì kết cục của nó **không đến từ tài liệu BA** mà từ
> `04-quyet-dinh-ban-giao.md` — dòng đó ghi rõ mục `C<nn>` và nội dung đã chốt. **Không còn kịch
> bản nào bị chặn.**
>
> Chỗ vẫn không ghi được expected state (phát biểu không đo được · ngoài phạm vi epic) nằm ở
> **§B. Chưa viết được kịch bản**, **không đoán**.
>
> **Quy ước dữ liệu dùng chung** cho mọi kịch bản, trừ khi kịch bản nói khác:
> · tenant `T1`, đơn vị kế toán có 3 chi nhánh `CN-A` (trụ sở) · `CN-B` · `CN-C`
> · nghiệp vụ mẫu: `MaChucNang = CTMDV` (Chứng từ mua dịch vụ), `MaNghiepVu = MUA_DV_TRONG_NUOC`
> · form của nghiệp vụ này có **1 lưới** tên `Hàng hóa, dịch vụ` ⇒ mẫu chuẩn có **1 khối Bảng**
> · chứng từ đang mở: `CT-2026-000123`, ngày chứng từ `05/09/2026`, chi nhánh ghi trên chứng từ `CN-B`
> · người dùng `u1` có quyền Thiết lập mẫu in, đang làm việc ở `CN-A`
> · thiết lập chung (tầng "thiết lập chung tối thiểu" của **Q-03**, lưu JSON trên cấu hình tenant)
>   lúc đầu: Khổ `A4` · Hướng `Dọc` · lề `1 / 1,5 / 1 / 1` · font `Times New Roman` · cỡ chữ `12`
> · hồ sơ đơn vị đọc qua **một cổng duy nhất** `HoSoDonViPort.theoChiNhanh(chiNhanhId)` (**Q-14**);
>   bản hiện tại trả hồ sơ của tenant vì `cfg_chi_nhanh` chưa tồn tại (**L-7**) — kịch bản dưới đây
>   ghi expected theo **chi nhánh ghi trên chứng từ**, đúng hợp đồng của cổng
>
> **Mô hình lưu trữ — theo Q-01, KHÔNG dựng 5 bảng quan hệ.** Mọi expected state dưới đây ghi theo
> mô hình JSON; bản trước ghi theo `cfg_mau_in_*` đã bị thay:
>
> | | |
> |---|---|
> | Bảng | **`prn_mau_in_tuy_chinh`** — đúng **một bản ghi** cho mỗi mẫu |
> | Khóa nghiệp vụ | `(tenant_id, ma_loai_chung_tu, **ma_nghiep_vu**)` — cột `ma_nghiep_vu` là **cột mới** + unique index mới (migration mới, KHÔNG sửa `V1148`) |
> | Thân mẫu | cột `jsonb` gọi là **`noi_dung`** — 5 "entity" của `3.crud-matrix.md` trở thành **5 nhánh JSON** |
> | Khóa lạc quan | cột `phien_ban`; payload Lưu mang `phienBan` (**C06**) |
> | Ảnh nền | **cột riêng**, không nhét base64 vào JSON (**C08**): `anh_nen` (`bytea`) · `anh_nen_kieu_tep` · `anh_nen_ten_tep`; JSON chỉ giữ cờ `nen.kieu = 'ANH'` |
>
> Đường dẫn JSON dùng suốt file:
> `noi_dung.giayVaChu.*` · `noi_dung.rieng.*` · `noi_dung.khoi[]` ·
> `noi_dung.khoi[i].cot[]` · `noi_dung.khoi[i].oLuoi[]` · `noi_dung.khoi[chuKy].oKy[]`
>
> ⚠ **"Theo thiết lập chung" = khóa VẮNG MẶT trong JSON**, không phải giá trị `null` (**C28**).
> Chuẩn hóa JSON khi so sánh (**C02**) cũng **bỏ mọi khóa `null`** ⇒ ghi `null` và bỏ khóa là **cùng
> một trạng thái**; expected state dưới đây luôn ghi **"khóa vắng mặt"** cho ô theo chung.

---

## §A. Ma trận kịch bản

| ID | Nhóm | Điều kiện | Kết quả mong đợi (tóm tắt) | Luật phủ chính |
|---|---|---|---|---|
| S-TLMI-001 | happy | Mở màn lần đầu, chưa có bản ghi | Nạp mẫu chuẩn 4 loại khối, badge `Đã lưu`, nút Lưu mờ | R-006, R-007, R-008, R-009, INV-002, INV-008 |
| S-TLMI-002 | happy | Sửa tiêu đề rồi Lưu lần đầu | 1 bản ghi; `giayVaChu` = `{}` (mọi khóa vắng mặt); `MSG_…_101` | R-037, R-246, R-247, INV-003 |
| S-TLMI-003 | happy | Font riêng vs font theo chung, đổi thiết lập chung | Ô theo chung đổi theo, ô riêng đứng yên | R-036, R-038, R-039, R-264, INV-003 |
| S-TLMI-004 | happy | Thêm khối tự do, đặt trường + chữ tự do | `MSG_…_104`; in `Tên hiển thị: Giá trị` | R-120…R-124, R-144, R-152, R-156 |
| S-TLMI-005 | happy | In Mẫu tùy chỉnh sau khi đã lưu | Bản in đúng thứ tự khối, lưới căn chỉnh không in | R-022, R-259, R-262, R-178, R-013 |
| S-TLMI-006 | happy | In Mẫu tùy chỉnh khi chưa có bản ghi | In mẫu chuẩn + `MSG_…_103` một lần | R-007, R-260, INV-002 |
| S-TLMI-007 | happy | Vào bằng nút Sửa mẫu, Lưu, quay lại xem trước | Cùng một mẫu; bản in vẽ lại theo mẫu vừa lưu | R-027, R-028, R-029, R-030, R-269 |
| S-TLMI-008 | happy | Đổi Loại nghiệp vụ trên form rồi mở lại | Mở mẫu khác; 2 bản ghi độc lập | R-002, R-011, R-012, INV-001 |
| S-TLMI-009 | happy | Bỏ tick cột, kéo đổi thứ tự, Lưu | Tự chia lại tổng = 100, không báo lỗi | R-103, R-111, R-112, R-115, INV-005 |
| S-TLMI-010 | happy | Khối Chữ ký: thêm ô ký tự do, bật Thủ kho | 4 ô ký in, chia đều ≥ 4 cm | R-182…R-198, INV-010 |
| S-TLMI-011 | happy | Lưu ở `CN-A`, đọc ở `CN-B` | Cùng một mẫu, không lọc chi nhánh | R-005, R-035, INV-011 |
| S-TLMI-012 | happy | Tắt con mắt khối Bảng, kéo đổi thứ tự khối | Khối sau dồn lên, thiết lập bên trong giữ nguyên | R-204…R-209 |
| S-TLMI-013 | biên | Khối tự do đúng 20 dòng, bấm + Dòng dưới | Chặn, `MSG_…_208`, vẫn 20 dòng | R-129, R-133, INV-006 |
| S-TLMI-014 | biên | Khối tự do đúng 6 cột, bấm + Cột phải | Chặn, `MSG_…_216`, vẫn 6 cột | R-130, R-133, INV-006 |
| S-TLMI-015 | biên | Khối tự do còn 1 dòng × 1 cột | Nút − Dòng và − Cột `Disable` | R-135, INV-006 |
| S-TLMI-016 | biên | Mẫu đã có 10 khối tự do, bấm Thêm | Chặn, `MSG_…_207`, vẫn 10 khối | R-125, INV-006 |
| S-TLMI-017 | biên | Cỡ chữ chung 8 · 20 · 7 · 21 | 8 và 20 lưu được; 7 và 21 chặn ở **server**, `MSG_…_215` | R-063, R-239 (V16) |
| S-TLMI-018 | biên | Căn lề 0 · 5 · 5,1 · 1,25 | 0 và 5 hợp lệ; 5,1 và 1,25 ⇒ `MSG_…_213` | R-061, R-239 (V14) |
| S-TLMI-019 | biên | Rộng cột 3 · 90 · 2 · 91 | 3 và 90 hợp lệ; 2 và 91 ⇒ `MSG_…_205` | R-108, INV-005 |
| S-TLMI-020 | biên | Cỡ chữ tiêu đề 10 · 36 · 9 · 37 | 10 và 36 hợp lệ; 9 và 37 ⇒ `MSG_…_202` | R-086, R-239 (V02) |
| S-TLMI-021 | biên | Bảng còn đúng 1 cột, bỏ tick nốt | Chặn, `MSG_…_203` kèm `{TenBang}` | R-104, INV-004 |
| S-TLMI-022 | biên | Chia đều 100%: 40 / 40 / 40 | 33 / 33 / 34 | R-114, INV-005 |
| S-TLMI-023 | biên | Chia đều 100%: 50 / 30 | 62 / 38 | R-114, INV-005 |
| S-TLMI-024 | biên | Chia đều 100%: 90 / 70 / 2 (chạm sàn 3) | 54 / 43 / 3 | R-114, INV-005 |
| S-TLMI-025 | biên | Chia đều 100%: 10/10/10/10 + 1 cột bỏ tick | 25/25/25/25; cột bỏ tick giữ nguyên số cũ | R-112, R-113, R-114 |
| S-TLMI-026 | biên | Tên khối tự do 60 · 61 · trống | 60 OK; 61 và trống ⇒ `MSG_…_206` | R-121, R-239 (V06) |
| S-TLMI-027 | biên | Chữ tự do 255 · 256; Tên hiển thị trường 255 · 256 | 255 OK; 256 ⇒ `MSG_…_212`; tên hiển thị đồng bộ mọi khối | R-147, R-157, INV-009 |
| S-TLMI-028 | biên | Tên hiển thị cột 100 · 101 · trống | 100 OK; 101 và trống ⇒ `MSG_…_204` | R-102, R-239 (V04) |
| S-TLMI-029 | biên | Tiêu đề bản in 255 · 256 · trống | 255 OK; 256 và trống ⇒ `MSG_…_201` | R-085, R-239 (V01) |
| S-TLMI-030 | biên | Tiêu đề ô ký tự do 60 · 61 · trống (bật / tắt) | Bật + trống ⇒ `MSG_…_211`; tắt + trống ⇒ lưu được | R-189, R-191, INV-010 |
| S-TLMI-031 | biên | 61 thao tác rồi Hoàn tác liên tiếp | Lùi được đúng 60 bước, bước 61 ⇒ nút `Disable` | R-223, R-224, R-226, R-227 |
| S-TLMI-032 | biên | Số cột tự động in ngang 1 · 50 · 0 · 51 | 1 và 50 OK; 0 và 51 ⇒ `MSG_…_214`; Hướng ≠ Tự động ⇒ không kiểm | R-056, R-057, R-058, R-059 |
| S-TLMI-033 | biên | Bảy ô tick đầu trang: bỏ tick hết / hồ sơ trống | Khối không in gì, **không** lỗi, không cảnh báo mềm | R-076…R-081, R-238, R-267 |
| S-TLMI-034 | biên | Khối tự do bật mà mọi ô trống | Lưu được; bản in chừa khoảng trống bằng chiều cao dòng | R-143, R-176, R-236 |
| S-TLMI-035 | ngoại lệ | Người dùng không có quyền Thiết lập mẫu in | Mục menu + nút Sửa mẫu **Hide**; API ⇒ `MSG_…_002` | R-031, R-032, R-034, R-269 |
| S-TLMI-036 | ngoại lệ | Không quyền Thiết lập mẫu in, có quyền In | "Mẫu tùy chỉnh" vẫn `Show` và in được | R-033 |
| S-TLMI-037 | ngoại lệ | Badge `Có lỗi` mà bấm Lưu | Không ghi; chỉ báo **lỗi đầu tiên**; mở khối + focus ô | R-242, R-243, R-244, INV-012 |
| S-TLMI-038 | ngoại lệ | Gộp vùng 3 ô, trong đó 2 ô có nội dung | `MSG_…_404` với `{SoO} = 2`; đồng ý ⇒ giữ ô đầu tiên | R-136…R-139, R-174 |
| S-TLMI-039 | ngoại lệ | Ảnh nền `.gif` / `.png` 1,4 MB | Chặn khi chọn tệp, `MSG_…_209` | R-069, R-070, R-071, R-239 (V10) |
| S-TLMI-040 | ngoại lệ | Màu chữ `#GG0011` / `12ab34` | Chặn, `MSG_…_210`; màu cũ giữ nguyên | R-064, R-066, R-239 (V11) |
| S-TLMI-041 | ngoại lệ | Xóa khối tự do | `MSG_…_403` kèm `{TenKhoi}`; khối chuẩn không có nút xóa | R-175, R-210, R-211 |
| S-TLMI-042 | ngoại lệ | Lỗi hệ thống giữa vòng ghi bảng con | Rollback toàn bộ, `MSG_…_003`, màn giữ nguyên | R-247, R-249, INV-012 |
| S-TLMI-043 | ngoại lệ | Lỗi hệ thống khi dựng bản in | `MSG_…_003`, **không** mở màn xem trước | R-270 |
| S-TLMI-044 | ngoại lệ | Chứng từ chưa ghi sổ, đơn vị cấm in | Nút In `Disable`; tooltip nguyên văn qua key i18n cục bộ | R-261 · C14 chốt |
| S-TLMI-045 | ngoại lệ | API xóa khối chuẩn / Lưu mẫu thiếu khối chuẩn | Từ chối; 4 loại khối chuẩn luôn còn | R-210, INV-008 |
| S-TLMI-046 | ngoại lệ | Xóa ô ký chức danh | Không có nút xóa; chỉ bỏ tick được | R-185, R-186, R-192 |
| S-TLMI-047 | ngoại lệ | Đặt lại trường X vào ô thứ hai cùng khối | Ô cũ về Ô trống; khối khác vẫn dùng X được | R-152, R-153, INV-007 |
| S-TLMI-048 | ngoại lệ | Chưa chọn ô nào; Esc khi đang mở hộp thoại con | Thanh công cụ mờ; Esc không đóng màn chính | R-162, R-170, R-256 |
| S-TLMI-049 | ngoại lệ | Đổi Khổ giấy trên thanh Xem trước rồi muốn hoàn lại 1 ô | Đổi ở thanh Xem trước **là đổi mẫu**; chỉ hoàn lại được cả nhóm | R-042, R-044, R-045 · C16 C17 chốt |
| S-TLMI-050 | rollback | Đóng khi chưa lưu → *Lưu và đóng* | Chạy Lưu, hiện toast `_101`, **rồi** mới đóng | R-251, R-252 · C23 chốt |
| S-TLMI-051 | rollback | Đóng khi chưa lưu → *Không lưu* | Bỏ mọi thay đổi, DB không đổi, lịch sử Hoàn tác xóa | R-251, R-253, R-225, INV-012 |
| S-TLMI-052 | rollback | Đóng khi chưa lưu → *Ở lại* | Giữ màn, không đổi gì | R-254 |
| S-TLMI-053 | rollback | Không có thay đổi mà bấm Đóng | Đóng ngay, **không** hỏi | R-240, R-255, R-029 |
| S-TLMI-054 | rollback | Đặt lại mẫu chuẩn rồi Đóng › *Không lưu* | `MSG_…_402` → `MSG_…_102` → badge `Chưa lưu`; DB nguyên vẹn | R-015…R-020, INV-012 |
| S-TLMI-055 | rollback | Mẫu bằng mẫu chuẩn rồi Lưu — 3 ca | So sánh JSON chuẩn hóa ⇒ **cả ba ca đều 0 bản ghi** | R-021, INV-002 · C02 chốt |
| S-TLMI-056 | rollback | Hoàn tác / Làm lại chuỗi thao tác rồi đóng màn | Về đúng trạng thái từng bước; đóng ⇒ xóa lịch sử | R-041, R-223…R-227 |
| S-TLMI-057 | tương tranh | Hai người cùng mở một mẫu và cùng Lưu | Khóa lạc quan `phienBan`; người Lưu sau bị chặn, `MSG_COMMON_001` | R-258, R-247 · C06 chốt |
| S-TLMI-058 | tương tranh | Hai request Lưu song song cùng khóa duy nhất | Đúng 1 bản ghi, không sinh 2 | R-001, R-004, INV-001 |
| S-TLMI-059 | biên | Form đổi phiên bản: thêm cột **và** bỏ cột | Cột mới vào cuối; cột bị bỏ — in thì bỏ qua im lặng, mở màn thì mờ | R-093, R-167, INV-005 · C10 chốt |
| S-TLMI-060 | ngoại lệ | Thiết lập chung bật Cộng gộp mặt hàng khi in | Khóa gộp **có thuế suất** ⇒ 3 dòng; chỉ áp 3 loại chứng từ | R-119, R-266 · C01 C30 chốt |
| S-TLMI-061 | happy | Bỏ tick **Logo** trong 7 ô tick đầu trang | Logo không in; cột `inLogo` thành riêng | R-082 · C03 chốt |
| S-TLMI-062 | happy | Sửa *Tiêu đề in ra* của ô ký **chức danh** | Sửa được và lưu riêng; tên người ký vẫn theo chung | R-046, R-188, R-196 · C04 chốt |
| S-TLMI-063 | happy | In lại chứng từ cũ khi đang ở chi nhánh khác | Khối Chữ ký **và** đầu trang cùng đọc chi nhánh trên chứng từ | R-199, R-267 · C05 chốt |
| S-TLMI-064 | happy | Sửa tên khối tự do ở **cả hai chỗ** | Hộp Đặt tên khối và ô Tên khối cùng ghi một trường | R-127 · C07 chốt |
| S-TLMI-065 | ngoại lệ | Ẩn khối Tiêu đề rồi để trống Nội dung → Lưu | Bỏ qua validate khối ẩn; bật lại ⇒ báo `MSG_…_201` ngay | R-085, R-207 · C18 chốt |
| S-TLMI-066 | ngoại lệ | Bỏ tick cột cuối khi khối Bảng **đã tắt** con mắt | Không chặn; bật lại con mắt ⇒ `MSG_…_203` | R-104, R-208 · B-19 chốt |
| S-TLMI-067 | biên | Tách ô đang có nội dung | Nội dung về ô trên-trái, **không hỏi xác nhận** | R-140 · C19 chốt |
| S-TLMI-068 | biên | Lỗi đầu tiên khi một khối có cả ô bảng chỉnh lẫn ô lưới | Ô bảng chỉnh trước, rồi tới ô lưới | R-243, R-244 · C21 chốt |
| S-TLMI-069 | biên | Mở màn xem trước **lần thứ hai** khi chưa có mẫu | `MSG_…_103` hiện lại — một lần mỗi lần mở | R-260 · C22 chốt |
| S-TLMI-070 | biên | Chia đều 100% khi lưới cột **đang lọc** | Áp cho mọi cột đang tick in, kể cả cột bị lọc ẩn | R-114, R-116, R-117 · C31 chốt |
| S-TLMI-071 | ngoại lệ | Gọi API in khi thiếu **quyền In** | `MSG_COMMON_003`, KHÔNG dùng `MSG_…_002` | R-034, R-261 · C15 chốt |
| S-TLMI-072 | ngoại lệ | Thiếu `<ChucNang>.View.Detail` khi mở màn | Chặn mở màn — không lộ dữ liệu chứng từ qua xem trước | R-031, R-034 · C13 chốt |
| S-TLMI-073 | biên | Tải ảnh nền 980 KB rồi Lưu, rồi Hoàn tác | Ảnh vào cột `bytea`; JSON chỉ giữ `nen.kieu='ANH'` | R-069, R-223 · C08 chốt |
| S-TLMI-074 | ngoại lệ | Khối tự do còn 1 dòng × 1 cột, bấm Xóa dòng | Nút mờ, chặn; muốn bỏ hẳn thì Xóa khối | R-134, R-135 · C20 chốt |
| S-TLMI-075 | biên | Căn lề khối đầu trang = Giữa, có Logo | Logo vẫn bên trái cụm; căn lề áp cho **cả cụm** | R-049, R-082 · C29 chốt |
| S-TLMI-076 | biên | Lưu, đóng, mở lại rồi Hoàn tác | Lịch sử 60 bước **theo phiên mở màn**, không qua phiên | R-223, R-225 · C32 chốt |
| S-TLMI-077 | happy | Chuẩn hóa JSON: đổi thứ tự khóa, thêm khóa `null` | Hai payload khác chuỗi nhưng **bằng nhau** sau chuẩn hóa | R-021, R-037 · C02 C28 chốt |
| S-TLMI-078 | tương tranh | Lưu bằng `phienBan` cũ sau khi người khác đã Lưu | `MSG_COMMON_001`; màn hỏi nạp lại; DB giữ bản người trước | R-258, R-247 · C06 chốt |

Đủ 5 nhóm: **happy 17** · **biên 30** · **ngoại lệ 21** · **rollback 7** · **tương tranh 3** = **78**.

Kịch bản `S-TLMI-061` … `S-TLMI-078` là **đợt bổ sung 2026-09-19** sau khi `04-quyet-dinh-ban-giao.md`
đóng 32 mục mâu thuẫn; chúng phủ các mục §B của bản trước nay đã hết bị chặn.

---

## §1. Nhóm `happy`

### S-TLMI-001 · Mở màn lần đầu khi chưa có bản ghi mẫu

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-006, R-TLMI-007, R-TLMI-008, R-TLMI-009, R-TLMI-011, R-TLMI-023,
            R-TLMI-028, R-TLMI-053, R-TLMI-064, R-TLMI-067, R-TLMI-077, R-TLMI-085,
            R-TLMI-086, R-TLMI-183, R-TLMI-184, R-TLMI-190, R-TLMI-201, R-TLMI-202,
            R-TLMI-212, R-TLMI-217, R-TLMI-240, R-TLMI-245, INV-TLMI-002, INV-TLMI-008

TIỀN ĐỀ
  prn_mau_in_tuy_chinh WHERE tenant_id=T1 AND ma_loai_chung_tu=CTMDV
                         AND ma_nghiep_vu=MUA_DV_TRONG_NUOC       0 bản ghi
  thiết lập chung      A4 · Dọc · 1 / 1,5 / 1 / 1 · Times New Roman · 12
  người dùng           u1, CÓ quyền Thiết lập mẫu in, đang ở CN-A
  chứng từ đang mở     CT-2026-000123 (form sửa), chi nhánh CN-B, ngày 05/09/2026

THAO TÁC
  1. Trên form sửa chứng từ CT-2026-000123 → bấm nút In
  2. Chọn mục "Thiết lập mẫu in…"

EXPECTED — menu In (R-TLMI-023)
  thứ tự mục            các mẫu in cố định theo quy định (01-TT, 02-VT…)
                        → đường kẻ
                        → "Mẫu tùy chỉnh"
                        → "Thiết lập mẫu in…"

EXPECTED — màn vừa mở
  tiêu đề màn           "Thiết lập mẫu in: Chứng từ mua dịch vụ"
  nhãn trạng thái       "Đã lưu"   (badge xám, nằm cạnh tiêu đề màn)
  nút Lưu               Disable
  DB                    vẫn **0 bản ghi** trên `prn_mau_in_tuy_chinh`   ← INV-TLMI-002
                        (vắng bản ghi CHÍNH LÀ trạng thái "dùng mẫu chuẩn")

EXPECTED — cột Bố cục mẫu (đúng thứ tự, đúng 5 dòng)
  dòng 0                "Thiết lập mẫu"      (không phải khối, không kéo được)
  dòng 1                Thông tin đầu trang   con mắt = Có
  dòng 2                Tiêu đề               con mắt = Có
  dòng 3                "Bảng Hàng hóa, dịch vụ"  con mắt = Có   (1 lưới ⇒ 1 khối Bảng)
  dòng 4                Chữ ký                con mắt = Có
  không có khối nào khác; không dòng nào có nút ✕     ← INV-TLMI-008

EXPECTED — giá trị mặc định đọc được trên màn
  Giấy và chữ           Khổ A4 · Hướng Dọc · lề 1 / 1,5 / 1 / 1 · Times New Roman · cỡ 12
                        (cả sáu ô đều ở trạng thái "theo chung")
  Màu chữ               #000000        (riêng của mẫu, KHÔNG kế thừa)
  Kiểu hình nền         Không          (ô Độ đậm, Căn ảnh, Ảnh đều Hide)
  Tiêu đề: Nội dung     "Chứng từ mua dịch vụ"
  Tiêu đề: Cỡ chữ       18 · Căn Giữa · IN HOA Có · In đậm Có
  Chữ ký: thứ tự        Người lập phiếu, Kế toán trưởng, Giám đốc, Thủ kho, Thủ quỹ
  Chữ ký: tick          Có / Có / Có / Không / Không
  Chữ ký: dòng ghi chú  "(Ký, họ tên)" cho bốn ô; Giám đốc = "(Ký, họ tên, đóng dấu)"
  Trang xem trước       vẽ trang đầu bằng dữ liệu THẬT của CT-2026-000123
```

### S-TLMI-002 · Sửa tiêu đề rồi Lưu lần đầu — mọi khóa Giấy và chữ vắng mặt

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-037, R-TLMI-085, R-TLMI-088, R-TLMI-230, R-TLMI-241, R-TLMI-246,
            R-TLMI-247, R-TLMI-248, R-TLMI-250, INV-TLMI-003

TIỀN ĐỀ
  như S-TLMI-001 sau bước mở màn (0 bản ghi, badge "Đã lưu")

THAO TÁC
  1. Khối Tiêu đề → ô Nội dung: xóa, gõ "CHỨNG TỪ MUA DỊCH VỤ"
  2. Rời ô (Tab)
  3. Nhấn Ctrl+S

EXPECTED — ngay sau bước 2 (R-TLMI-230, R-TLMI-241)
  ô Nội dung            hợp lệ, không dấu lỗi
  nhãn trạng thái       "Chưa lưu"     (badge cam)
  nút Lưu               Enable

EXPECTED — sau Ctrl+S (R-TLMI-250 ⇒ chạy đúng nhánh Lưu)
  toast                 MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"
  nhãn trạng thái       "Đã lưu";  nút Lưu Disable;  màn KHÔNG đóng
  prn_mau_in_tuy_chinh  **1 bản ghi** (tenant_id=T1, ma_loai_chung_tu=CTMDV,
                                       ma_nghiep_vu=MUA_DV_TRONG_NUOC)
  → phien_ban           1
  → anh_nen             NULL (chưa tải ảnh)
  → noi_dung (jsonb), các khóa của nhóm Giấy và chữ **VẮNG MẶT HẾT**   ← C28
      noi_dung.giayVaChu      = {}   — không có khoGiay / huongGiay / leTren / leTrai
                                       / leDuoi / lePhai / fontChu / coChu
      noi_dung.rieng.mauChu   = '#000000'   (riêng của mẫu, LUÔN có mặt)
      noi_dung.rieng.nen.kieu = 'KHONG'
      noi_dung.khoi[]         4 phần tử: đầu trang · tiêu đề · 1 bảng · chữ ký
                              (0 khối tự do)
      noi_dung.khoi[tieuDe].noiDung  = 'CHỨNG TỪ MUA DỊCH VỤ'
      noi_dung.khoi[chuKy].oKy[]     5 phần tử, hienThi = Có/Có/Có/Không/Không
  ghi trong ĐÚNG MỘT transaction                               ← R-TLMI-247

  ⚠ Ở đây mẫu **đã khác** mẫu chuẩn (tiêu đề in hoa) nên bản ghi được tạo. Ca "mở ra Lưu ngay,
     không sửa gì" cho kết quả KHÁC — **0 bản ghi** theo C02; xem S-TLMI-055.
```

### S-TLMI-003 · Ô theo chung đổi theo thiết lập chung, ô riêng đứng yên

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-036, R-TLMI-038, R-TLMI-039, R-TLMI-054, R-TLMI-062, R-TLMI-220,
            R-TLMI-264, INV-TLMI-003

TIỀN ĐỀ
  mẫu CTMDV/MUA_DV_TRONG_NUOC đã lưu ở S-TLMI-002 (`giayVaChu` không có khóa nào)
  mẫu thứ hai: nghiệp vụ PHIEU_CHI của cùng tenant, `giayVaChu` cũng rỗng

THAO TÁC
  1. Mở mẫu CTMDV → Giấy và chữ → Font chữ: đổi sang "Arial" → Lưu
  2. Quản trị đổi thiết lập chung: Font chữ "Times New Roman" → "Arial",
                                   Khổ giấy "A4" → "A5"
  3. In Mẫu tùy chỉnh cho CT-2026-000123 (nghiệp vụ CTMDV)
  4. In Mẫu tùy chỉnh cho một phiếu chi bất kỳ (nghiệp vụ PHIEU_CHI)
  5. Quản trị đổi thiết lập chung lần nữa: Font chữ "Arial" → "Times New Roman"
  6. In lại cả hai

EXPECTED — sau bước 1
  noi_dung.giayVaChu.fontChu  = 'Arial'        ← khóa CÓ MẶT ⇒ ô RIÊNG
  noi_dung.giayVaChu.khoGiay  **vắng mặt**     ← vẫn theo chung

EXPECTED — bước 3 (bản in CTMDV)
  font bản in           Arial   (từ giá trị riêng của mẫu)
  khổ giấy bản in       A5      (đọc thiết lập chung TẠI LÚC IN — R-TLMI-264)

EXPECTED — bước 4 (bản in phiếu chi)
  font bản in           Arial   (theo chung, đổi theo)
  khổ giấy bản in       A5      (theo chung)

EXPECTED — bước 6 (sau khi thiết lập chung quay về Times New Roman)
  bản in CTMDV          font **Arial**            ← ô riêng KHÔNG đổi
  bản in phiếu chi      font **Times New Roman**  ← ô theo chung đổi theo
  cả hai bản ghi        `giayVaChu.khoGiay` vẫn vắng mặt, khổ in vẫn A5
```

### S-TLMI-004 · Thêm khối tự do, đặt trường và chữ tự do

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-010, R-TLMI-120, R-TLMI-121, R-TLMI-122, R-TLMI-123, R-TLMI-124,
            R-TLMI-126, R-TLMI-143, R-TLMI-144, R-TLMI-145, R-TLMI-146, R-TLMI-147,
            R-TLMI-149, R-TLMI-150, R-TLMI-156, R-TLMI-158, R-TLMI-161, R-TLMI-165,
            R-TLMI-229, INV-TLMI-006

TIỀN ĐỀ
  mẫu CTMDV đã lưu (0 khối tự do), badge "Đã lưu"
  kho trường có trường "Số chứng từ" (giá trị trên CT-2026-000123 = "CT-2026-000123")

THAO TÁC
  1. Bấm "+ Thêm khối tự do"
  2. Hộp Đặt tên khối hiện tên gợi ý "Khối tự do 1" → sửa thành "Thông tin chung" → Thêm
  3. Kéo dòng trường "Số chứng từ" ở bảng chỉnh thả vào ô (1,1)
  4. Nháy đúp ô (1,2) → chọn "Chữ tự do" → gõ "Liên 2: Giao khách hàng" → Enter
  5. Chọn ô (1,1) → bấm In đậm
  6. Chọn ô (1,2) → bấm Căn Phải
  7. Lưu

EXPECTED — sau bước 2
  toast          MSG_PMKT-E-14549_21_104 — "Đã thêm khối tự do trước Chữ ký. Nháy đúp một ô
                 để chọn trường, hoặc kéo trường từ bảng bên phải thả vào ô"
  Bố cục mẫu     … → "Bảng Hàng hóa, dịch vụ" → **"Thông tin chung"** → "Chữ ký"
  lưới khối mới  1 dòng × 2 cột, cả hai là Ô trống
  bảng chỉnh     mở sẵn khối "Thông tin chung"; ô (1,1) được chọn sẵn
  nhãn trạng thái "Chưa lưu"

EXPECTED — sau bước 6, trên trang xem trước
  ô (1,1)        "**Số chứng từ**: CT-2026-000123"   (chỉ Tên hiển thị đậm, giá trị in thường)
  ô (1,2)        "Liên 2: Giao khách hàng"  căn phải
  hai cột        rộng bằng nhau (mỗi cột nửa bề ngang)

EXPECTED — sau Lưu
  toast                    MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"
  noi_dung.khoi[]          5 phần tử; khối tự do có tenKhoi = 'Thông tin chung',
                           thuTu ngay trước khối Chữ ký
  noi_dung.khoi[tuDo].soDong = 1 · soCot = 2
  noi_dung.khoi[tuDo].oLuoi[]  2 phần tử:
      (1,1) loai='TRUONG'    maTruong='soChungTu'   inDam=Có
      (1,2) loai='CHU_TU_DO' noiDung='Liên 2: Giao khách hàng'  can='PHAI'
  (Tên hiển thị và In đậm là thuộc tính CỦA TRƯỜNG ⇒ lưu ở nhánh `noi_dung.truong[]`,
   một mục cho mỗi trường đang được dùng — xem S-TLMI-027)
  bản in                   **KHÔNG** in chuỗi "Thông tin chung" (tên khối không in ra)
```

### S-TLMI-005 · In Mẫu tùy chỉnh sau khi đã lưu — bản in đúng bố cục

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-013, R-TLMI-022, R-TLMI-023, R-TLMI-024, R-TLMI-025, R-TLMI-026,
            R-TLMI-177, R-TLMI-178, R-TLMI-179, R-TLMI-222, R-TLMI-259, R-TLMI-262,
            R-TLMI-263, R-TLMI-264, R-TLMI-265, R-TLMI-267, R-TLMI-268, R-TLMI-271

TIỀN ĐỀ
  mẫu CTMDV đã lưu ở S-TLMI-004 (6 khối, thứ tự: đầu trang → tiêu đề → bảng → tự do → chữ ký)
  ô tick "Hiện lưới căn chỉnh" trên màn thiết lập đang **bật** (mặc định Có)
  chứng từ CT-2026-000123 có 3 dòng hàng, ghi chi nhánh CN-B
  hồ sơ CN-B: tên "Chi nhánh Hà Nội", địa chỉ "12 Láng Hạ"

THAO TÁC
  1. Đóng màn thiết lập, về form sửa CT-2026-000123
  2. Bấm In → chọn "Mẫu tùy chỉnh"

EXPECTED — menu In ở form sửa và form xem chi tiết
  có menu In (R-TLMI-025);  form **Thêm mới** KHÔNG có nút In
  màn danh sách có In ⇒ menu In cũng xuất hiện ở đó (R-TLMI-026)
  các mẫu cố định 01-TT / 02-VT vẫn liệt kê và vẫn in như cũ (R-TLMI-013)

EXPECTED — bản in dựng ra
  thứ tự khối từ trên xuống
    1. Thông tin đầu trang   đọc hồ sơ **CN-B** ("Chi nhánh Hà Nội", "12 Láng Hạ")
    2. Tiêu đề               "CHỨNG TỪ MUA DỊCH VỤ", cỡ 18, căn giữa, đậm
                             + dòng ngày tháng "Ngày 05 tháng 09 năm 2026", nghiêng
    3. Bảng Hàng hóa, dịch vụ  3 dòng dữ liệu thật
    4. Thông tin chung       "Số chứng từ: CT-2026-000123" | "Liên 2: Giao khách hàng"
    5. Chữ ký                3 ô ký (Người lập phiếu, Kế toán trưởng, Giám đốc)
  hình nền                   vẽ dưới cùng (ở đây Kiểu = Không ⇒ không có)
  giấy và chữ                lấy theo mẫu; khóa **vắng mặt** lấy thiết lập chung tại lúc in
  đường phân ô khối tự do    **KHÔNG có** trên bản in và **KHÔNG có** trong PDF  ← R-TLMI-178
  dữ liệu chứng từ           không đổi một bit;  `prn_mau_in_tuy_chinh` không đổi ← R-TLMI-271
```

### S-TLMI-006 · In Mẫu tùy chỉnh khi chưa có bản ghi mẫu

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-007, R-TLMI-260, R-TLMI-268, INV-TLMI-002

TIỀN ĐỀ
  prn_mau_in_tuy_chinh WHERE (T1, CTMDV, MUA_DV_TRONG_NUOC)   0 bản ghi
  người dùng u1 có quyền In **và** `<ChucNang>.View.Detail` của nghiệp vụ

THAO TÁC
  1. Mở CT-2026-000123 → In → "Mẫu tùy chỉnh"

EXPECTED
  màn xem trước         MỞ bình thường — **không phải lỗi**
  bản in                dựng theo **mẫu chuẩn hệ thống** của nghiệp vụ
                        (4 loại khối theo thứ tự chuẩn, chữ ký 3 ô bật)
  thông báo             MSG_PMKT-E-14549_21_103 — "Đơn vị chưa thiết lập mẫu tùy chỉnh cho
                        nghiệp vụ này, đang in theo mẫu chuẩn hệ thống"
                        hiện **MỘT LẦN** trên màn xem trước
  DB                    vẫn 0 bản ghi — in KHÔNG sinh bản ghi

  **C22 chốt**: "một lần" = **một lần mỗi lần mở màn xem trước bản in**. Không nhớ qua phiên,
  không nhớ theo người dùng ⇒ **không** lưu cờ đã-hiện vào DB hay session. Xem S-TLMI-069.
```

### S-TLMI-007 · Lối vào bằng nút Sửa mẫu, Lưu, quay lại xem trước

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-027, R-TLMI-028, R-TLMI-029, R-TLMI-030, R-TLMI-218, R-TLMI-269

TIỀN ĐỀ
  đang ở màn xem trước bản in của CT-2026-000123, in bằng Mẫu tùy chỉnh
  u1 CÓ quyền Thiết lập mẫu in
  mẫu hiện tại: Tiêu đề cỡ chữ 18

THAO TÁC
  1. Trên màn xem trước, bấm nút "Sửa mẫu"
  2. Đổi Cỡ chữ của khối Tiêu đề: 18 → 24, rời ô
  3. Lưu
  4. Bấm Đóng

EXPECTED — bước 1
  nút "Sửa mẫu"      Show (vì có quyền)
  màn mở ra          ĐÚNG màn Thiết lập mẫu in, ĐÚNG mẫu của nghiệp vụ CT-2026-000123
                     (giống hệt lối vào qua menu In — R-TLMI-028)

EXPECTED — bước 2
  trang xem trước    vẽ lại NGAY, tiêu đề to lên, chưa cần Lưu
  nhãn trạng thái    "Chưa lưu"

EXPECTED — bước 3
  toast              MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"
  khối Tiêu đề.CoChu = 24

EXPECTED — bước 4
  quay về            ĐÚNG màn xem trước bản in (nơi vừa mở ra), KHÔNG về form chứng từ
  bản in             **vẽ lại** theo mẫu vừa lưu — tiêu đề cỡ 24
```

### S-TLMI-008 · Đổi Loại nghiệp vụ trên form rồi mở lại thì mở mẫu khác

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-001, R-TLMI-002, R-TLMI-003, R-TLMI-004, R-TLMI-011, R-TLMI-012,
            INV-TLMI-001

TIỀN ĐỀ
  mẫu (T1, CTMDV, MUA_DV_TRONG_NUOC) đã lưu, Tiêu đề = "CHỨNG TỪ MUA DỊCH VỤ"
  (T1, CTMDV, MUA_DV_NHAP_KHAU)        0 bản ghi

THAO TÁC
  1. Trên form CT-2026-000123, ô Loại nghiệp vụ đang là "Mua dịch vụ trong nước"
     → In → Thiết lập mẫu in…  → xem tiêu đề → Đóng
  2. Đổi ô Loại nghiệp vụ sang "Mua dịch vụ nhập khẩu"
  3. In → Thiết lập mẫu in… lần nữa
  4. Đổi Tiêu đề thành "CHỨNG TỪ MUA DỊCH VỤ NHẬP KHẨU" → Lưu

EXPECTED — bước 1
  mẫu mở ra     mẫu của MUA_DV_TRONG_NUOC; Tiêu đề = "CHỨNG TỪ MUA DỊCH VỤ";
                badge "Đã lưu"

EXPECTED — bước 3
  mẫu mở ra     mẫu KHÁC — của MUA_DV_NHAP_KHAU; chưa có bản ghi ⇒ mẫu chuẩn hệ thống;
                Tiêu đề = "Chứng từ mua dịch vụ" (tên loại chứng từ, mặc định)
                badge "Đã lưu" (bằng mẫu chuẩn)

EXPECTED — sau bước 4
  prn_mau_in_tuy_chinh  2 bản ghi:
    (T1, CTMDV, MUA_DV_TRONG_NUOC)  noi_dung.khoi[tieuDe].noiDung = "CHỨNG TỪ MUA DỊCH VỤ"
    (T1, CTMDV, MUA_DV_NHAP_KHAU)   noi_dung.khoi[tieuDe].noiDung
                                    = "CHỨNG TỪ MUA DỊCH VỤ NHẬP KHẨU"
  mỗi cặp (tenant_id, ma_loai_chung_tu, ma_nghiep_vu) vẫn ≤ 1 bản ghi   ← INV-TLMI-001

  Ghi chú: loại chứng từ KHÔNG chia nghiệp vụ (R-TLMI-003) ⇒ `ma_nghiep_vu` nhận đúng một
  giá trị quy ước cho cả loại chứng từ; khóa duy nhất vẫn **3 thành phần**, API luôn nhận
  **cặp** `(maLoaiChungTu, maNghiepVu)` kể cả khi chỉ có một nghiệp vụ   ← Q-16
```

### S-TLMI-009 · Bỏ tick cột, kéo đổi thứ tự, Lưu — tự chia lại về 100

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-092, R-TLMI-101, R-TLMI-103, R-TLMI-105, R-TLMI-106, R-TLMI-107,
            R-TLMI-110, R-TLMI-111, R-TLMI-112, R-TLMI-114, R-TLMI-115, INV-TLMI-005

TIỀN ĐỀ
  khối "Bảng Hàng hóa, dịch vụ" có 4 cột, đều tick in:
    C1 Tên hàng   (chữ)  Rộng 40  Căn Trái   ô Cộng: Hide
    C2 Số lượng   (số)   Rộng 20  Căn Phải   Cộng = Không
    C3 Đơn giá    (tiền) Rộng 20  Căn Phải   Cộng = Có
    C4 Thành tiền (tiền) Rộng 20  Căn Phải   Cộng = Có
  tổng = 100, badge "Đã lưu"

THAO TÁC
  1. Bỏ tick in cột C2 (Số lượng)
  2. Kéo ⠿ cột C4 lên trên cột C3
  3. Lưu

EXPECTED — sau bước 1
  dòng tổng dưới lưới cột   "Tổng độ rộng cột đang 80% (nên = 100%)" + link "Chia đều về 100%"
  cột C2                     giữ nguyên Rộng 20, không tính vào tổng   ← R-TLMI-112
  KHÔNG báo lỗi              (tổng ≠ 100 không nằm trong 17 dòng Validation)
  nhãn trạng thái            "Chưa lưu"

EXPECTED — sau bước 2
  thứ tự cột                 C1, C4, C3   (cột C2 bỏ tick vẫn nằm trong lưới cấu hình)

EXPECTED — sau Lưu (R-TLMI-111 → thuật toán R-TLMI-114)
  xét các cột đang tick in: C1=40, C4=20, C3=20 ⇒ tổng cũ = 80
    C1 = 40/80×100 = 50,0 → 50
    C4 = 20/80×100 = 25,0 → 25
    C3 = 20/80×100 = 25,0 → 25
    tổng = 100 ⇒ không phải cộng bù; không cột nào < 3
  noi_dung.khoi[bang].cot[]   C1 doRong=50 thuTu=1 hienThi=Có
                              C4 doRong=25 thuTu=2 hienThi=Có
                              C3 doRong=25 thuTu=3 hienThi=Có
                              C2 doRong=20 thuTu=4 hienThi=Không   ← giữ nguyên số cũ
  Σ doRong(cột tick in) = 100 và mọi cột tick in trong [3, 90]   ← INV-TLMI-005
  toast                 MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"
```

### S-TLMI-010 · Khối Chữ ký: thêm ô ký tự do, bật Thủ kho, đổi thứ tự

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-182, R-TLMI-183, R-TLMI-184, R-TLMI-185, R-TLMI-186, R-TLMI-187,
            R-TLMI-189, R-TLMI-190, R-TLMI-191, R-TLMI-193, R-TLMI-194, R-TLMI-195,
            R-TLMI-196, R-TLMI-197, R-TLMI-198, R-TLMI-200, INV-TLMI-010

TIỀN ĐỀ
  khối Chữ ký ở mẫu chuẩn: 5 ô ký, thứ tự Người lập phiếu · Kế toán trưởng · Giám đốc
                           · Thủ kho · Thủ quỹ; tick Có/Có/Có/Không/Không
  Thiết lập người ký: cờ "In tên người ký trên chứng từ, báo cáo" = **Bật**
                      tên người ký Giám đốc = "Nguyễn Văn A"
  Chỗ trống ký = Vừa (mặc định)

THAO TÁC
  1. Bật tick ô ký "Thủ kho"
  2. Bấm "Thêm ô ký tự do"
  3. Ô ký tự do mới: Tiêu đề in ra = "NGƯỜI NHẬN HÀNG"; Tên người ký = "Trần Thị B"; tick = Có
  4. Kéo ⠿ ô ký tự do lên vị trí thứ 2
  5. Lưu, rồi In Mẫu tùy chỉnh

EXPECTED — trên bảng chỉnh
  cột chức danh của 5 ô chuẩn    chỉ đọc (Disable, at)
  ô ký tự do                     cột chức danh ghi nhãn nguyên văn "tự do"
  Tên người ký của Giám đốc      chỉ đọc, không có nút xóa
  Tên người ký của ô ký tự do    gõ tay được, CÓ nút xóa
  số ô ký                        không giới hạn

EXPECTED — sau Lưu
  noi_dung.khoi[chuKy].oKy[]   6 phần tử
    thuTu 1  Người lập phiếu  hienThi=Có   dongGhiChu='(Ký, họ tên)'
    thuTu 2  (tự do)          hienThi=Có   tieuDe='NGƯỜI NHẬN HÀNG'
                              tenNguoiKy='Trần Thị B'  dongGhiChu='(Ký, họ tên)'
    thuTu 3  Kế toán trưởng   hienThi=Có   dongGhiChu='(Ký, họ tên)'
    thuTu 4  Giám đốc         hienThi=Có   dongGhiChu='(Ký, họ tên, đóng dấu)'
    thuTu 5  Thủ kho          hienThi=Có   dongGhiChu='(Ký, họ tên)'
    thuTu 6  Thủ quỹ          hienThi=Không
  mọi ô ký tự do đang bật có tieuDe ≠ trống và ≤ 60 ký tự       ← INV-TLMI-010

EXPECTED — bản in
  dòng trên các ô ký   "Ngày 05 tháng 09 năm 2026"  in nghiêng, căn phải
  số ô ký in ra        5 (Thủ quỹ tắt nên không in)
  bề ngang mỗi ô ký    chia đều, tối thiểu 4 cm; hết chỗ thì ô tiếp theo xuống hàng
                       và hàng mới lại chia đều
  tên người ký         CÓ in (theo cờ của Thiết lập người ký)
  cuối trang không đủ chỗ ⇒ **cả khối** Chữ ký sang trang mới, không bị cắt đôi

  **C04 chốt**: "Tiêu đề in ra" của ô ký **chức danh** **mẫu sửa riêng được** — xem S-TLMI-062.
  **C05 chốt**: khối Chữ ký đọc hồ sơ đơn vị của **chi nhánh ghi trên chứng từ** — xem S-TLMI-063.
```

### S-TLMI-011 · Mẫu dùng chung mọi chi nhánh

```
Nhóm        happy
Tầng kiểm   BE
Luật phủ    R-TLMI-005, R-TLMI-022, R-TLMI-031, R-TLMI-035, INV-TLMI-011

TIỀN ĐỀ
  u1 có quyền Thiết lập mẫu in của nghiệp vụ CTMDV **tại CN-A**
  u2 KHÔNG có quyền Thiết lập mẫu in, có quyền In, đang làm việc ở CN-C
  (T1, CTMDV, MUA_DV_TRONG_NUOC)  0 bản ghi

THAO TÁC
  1. u1 (đang ở CN-A) mở màn, đổi Màu chữ = #C00000, Lưu
  2. u1 đổi chi nhánh làm việc sang CN-B, mở lại màn
  3. u2 (ở CN-C) in một chứng từ CTMDV bằng Mẫu tùy chỉnh

EXPECTED — bước 1
  prn_mau_in_tuy_chinh  1 bản ghi, noi_dung.rieng.mauChu = '#C00000'
  bản ghi               **KHÔNG có** cột chi nhánh trong khóa duy nhất   ← INV-TLMI-011
                        (xếp **nhóm 1 — cấu hình hệ thống** của BR50.6   ← C26)
  KHÔNG có cảnh báo nào về việc mẫu áp cho cả CN-B, CN-C

EXPECTED — bước 2
  mẫu mở ra             ĐÚNG bản ghi vừa lưu (MauChu = '#C00000'), badge "Đã lưu"
  truy vấn đọc mẫu      KHÔNG có mệnh đề lọc chi nhánh

EXPECTED — bước 3
  bản in của u2         chữ và đường kẻ màu #C00000 (trừ logo)
  u2 in được dù không có quyền Thiết lập mẫu in                 ← R-TLMI-033
```

### S-TLMI-012 · Tắt con mắt khối Bảng và kéo đổi thứ tự khối

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-201, R-TLMI-202, R-TLMI-203, R-TLMI-204, R-TLMI-205, R-TLMI-206,
            R-TLMI-207, R-TLMI-208, R-TLMI-209, R-TLMI-212, R-TLMI-213, R-TLMI-214,
            R-TLMI-215, R-TLMI-216, R-TLMI-262

TIỀN ĐỀ
  mẫu 6 khối: Thông tin đầu trang · Tiêu đề · Bảng Hàng hóa, dịch vụ · Thông tin chung
              · Chữ ký   (5 dòng khối + dòng 0 "Thiết lập mẫu")
  cột bảng của khối Bảng: C1=50, C4=25, C3=25 (như S-TLMI-009)

THAO TÁC
  1. Tắt con mắt của khối "Bảng Hàng hóa, dịch vụ"
  2. Kéo ⠿ khối "Thông tin chung" lên **trên** khối Tiêu đề
  3. Bấm vào khối Chữ ký trên **trang xem trước**
  4. Rê chuột lên khối Tiêu đề trên trang xem trước
  5. Lưu, In

EXPECTED — bước 1
  trang xem trước    khối Bảng biến mất; khối "Thông tin chung" và "Chữ ký" **dồn lên**,
                     KHÔNG chừa khoảng trống
  thiết lập cột      C1=50 / C4=25 / C3=25 vẫn nguyên; bật lại con mắt ⇒ in như cũ

EXPECTED — bước 2
  Bố cục mẫu         Thiết lập mẫu → Thông tin đầu trang → **Thông tin chung** → Tiêu đề
                     → Bảng Hàng hóa, dịch vụ (đang tắt) → Chữ ký
  dòng 0 "Thiết lập mẫu"   KHÔNG kéo được, luôn ở đầu
  mọi khối khác            kéo được, kể cả Thông tin đầu trang và Chữ ký
  mỗi dòng khối            chỉ có ⠿, con mắt, tên khối (+ ✕ với khối tự do)

EXPECTED — bước 3
  bảng chỉnh bên phải   mở đúng khối **Chữ ký**
  cột trái, cột giữa, thanh tiêu đề   KHÔNG đổi

EXPECTED — bước 4
  hiện nhãn tên khối "Tiêu đề" trên trang

EXPECTED — bản in sau bước 5
  thứ tự in     Thông tin đầu trang → Thông tin chung → Tiêu đề → Chữ ký
  khối Bảng     KHÔNG in
```

---

## §2. Nhóm `biên`

### S-TLMI-013 · Lưới khối tự do đúng 20 dòng rồi thêm dòng thứ 21

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-129, R-TLMI-133, R-TLMI-239 (V08), INV-TLMI-006

TIỀN ĐỀ
  khối tự do "Thông tin chung": lưới **20 dòng × 2 cột**, ô (1,1) có Chữ tự do "Ghi chú"
  đang chọn ô (20,1)

THAO TÁC
  1. Bấm "+ Dòng dưới"
  2. Bấm "+ Dòng trên"
  3. (BE) POST lưu mẫu có khối tự do **21 dòng**

EXPECTED — bước 1 và bước 2
  thông báo       MSG_PMKT-E-14549_21_208 — "Mỗi khối tự do tối đa 20 dòng"
  lưới            vẫn **20 dòng × 2 cột**, không thêm dòng nào
  ô (1,1)         vẫn giữ Chữ tự do "Ghi chú"
  nhãn trạng thái KHÔNG đổi (không có thay đổi nào được ghi nhận)

EXPECTED — bước 3
  HTTP            400
  body            MSG_PMKT-E-14549_21_208
  DB              0 bản ghi bị đổi
  1 ≤ số dòng ≤ 20 luôn đúng                                    ← INV-TLMI-006

  Đối chứng dương: lưới 19 dòng, bấm "+ Dòng dưới" ⇒ thành 20 dòng, ô mới là **ô trống**,
  ô đang chọn giữ nguyên nội dung, KHÔNG có thông báo.
```

### S-TLMI-014 · Lưới khối tự do đúng 6 cột rồi thêm cột thứ 7

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-130, R-TLMI-131, R-TLMI-133, R-TLMI-239 (V09), INV-TLMI-006

TIỀN ĐỀ
  khối tự do "Thông tin chung": lưới **2 dòng × 6 cột**; đang chọn ô (1,6)

THAO TÁC
  1. Bấm "+ Cột phải"
  2. Bấm "+ Cột trái"
  3. (BE) POST lưu mẫu có khối tự do **7 cột**

EXPECTED — bước 1 và bước 2
  thông báo       MSG_PMKT-E-14549_21_216 — "Mỗi khối tự do tối đa 6 cột"
  lưới            vẫn **2 dòng × 6 cột**
  bề ngang        6 cột rộng bằng nhau (mỗi cột 1/6 bề ngang) — không đặt độ rộng riêng

EXPECTED — bước 3
  HTTP 400 + MSG_PMKT-E-14549_21_216;  DB không đổi
  1 ≤ số cột ≤ 6 luôn đúng                                      ← INV-TLMI-006
```

### S-TLMI-015 · Khối tự do còn 1 dòng × 1 cột — nút − Dòng / − Cột mờ

```
Nhóm        biên
Tầng kiểm   FE (sàn) · BE (chặn lưu)
Luật phủ    R-TLMI-134, R-TLMI-135, INV-TLMI-006

TIỀN ĐỀ
  khối tự do mới tạo: 1 dòng × 2 cột (R-TLMI-123)

THAO TÁC
  1. Chọn ô (1,2) → bấm "Xóa cột"
  2. Quan sát nút "− Dòng" và "− Cột"
  3. (BE) POST lưu mẫu có khối tự do **0 dòng**

EXPECTED — bước 1
  lưới            1 dòng × 1 cột

EXPECTED — bước 2
  nút "− Dòng"    Disable
  nút "− Cột"     Disable

EXPECTED — bước 3
  không lưu được; trạng thái 0 dòng / 0 cột không tồn tại được  ← INV-TLMI-006

  **C20 chốt**: sàn lưới = **1 dòng × 1 cột**; xóa dòng/cột cuối cùng bị chặn ở FE bằng nút
  mờ. Muốn bỏ hẳn khối thì dùng **Xóa khối này** (`MSG_…_403`). Xem S-TLMI-074.
  ⚠ Nhánh BE nhận payload 0 dòng / 0 cột: `04` không cấp mã `MSG_` riêng ⇒ ghi được **hành vi**
  (từ chối, DB không đổi) nhưng **không** ghi được mã trả về — xem §B.
```

### S-TLMI-016 · Mẫu đã có 10 khối tự do rồi thêm khối thứ 11

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-125, R-TLMI-239 (V07), INV-TLMI-006

TIỀN ĐỀ
  mẫu CTMDV có **10** khối tự do đang tồn tại (tên "Khối tự do 1"…"Khối tự do 10")

THAO TÁC
  1. Bấm "+ Thêm khối tự do"
  2. (BE) POST lưu mẫu có **11** khối tự do

EXPECTED — bước 1
  thông báo       MSG_PMKT-E-14549_21_207 — "Mỗi mẫu tối đa 10 khối tự do"
  hộp Đặt tên khối  **KHÔNG mở**
  Bố cục mẫu       vẫn 10 khối tự do; nhãn trạng thái KHÔNG đổi

EXPECTED — bước 2
  HTTP 400 + MSG_PMKT-E-14549_21_207;  DB không đổi
  COUNT(khối tự do) ≤ 10 luôn đúng                              ← INV-TLMI-006

  Đối chứng dương: mẫu có 9 khối ⇒ bấm Thêm mở được hộp Đặt tên khối, thêm thành khối 10.
```

### S-TLMI-017 · Cỡ chữ chung tại biên 8 · 20 và ngoài biên 7 · 21

```
Nhóm        biên
Tầng kiểm   BE
Luật phủ    R-TLMI-063, R-TLMI-239 (V16), R-TLMI-246

TIỀN ĐỀ
  ô Cỡ chữ của nhóm Giấy và chữ là **danh sách chọn** ⇒ FE không kiểm
  mẫu CTMDV đã có bản ghi

THAO TÁC
  1. Chọn Cỡ chữ = 8 → Lưu
  2. Chọn Cỡ chữ = 20 → Lưu
  3. (BE) POST lưu mẫu với CoChu = 7
  4. (BE) POST lưu mẫu với CoChu = 21

EXPECTED — bước 1, 2
  Lưu thành công; MSG_PMKT-E-14549_21_101; noi_dung.giayVaChu.coChu = 8, rồi = 20
  (ô đã sửa ⇒ **riêng**, khóa `coChu` từ vắng mặt chuyển thành **có mặt**)

EXPECTED — bước 3, 4
  HTTP            400
  body            MSG_PMKT-E-14549_21_215 — "Cỡ chữ phải là số nguyên từ 8 đến 20"
  chặn ở          **Server**, thời điểm "Khi nhấn Lưu"  (FE không có dấu lỗi tại chỗ)
  DB              `giayVaChu.coChu` giữ nguyên 20 (giá trị của bước 2)  ← INV-TLMI-012
```

### S-TLMI-018 · Căn lề tại biên 0 · 5 và ngoài biên 5,1 · 1,25

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-061, R-TLMI-239 (V14), R-TLMI-231, R-TLMI-234, R-TLMI-242

TIỀN ĐỀ
  Căn lề đang theo chung: trên 1 · trái 1,5 · dưới 1 · phải 1

THAO TÁC
  1. Lề trên = 0, rời ô
  2. Lề phải = 5, rời ô
  3. Lề dưới = 5,1, rời ô
  4. Sửa lề dưới = 1,25, rời ô
  5. Sửa lề dưới = 1,2, rời ô
  6. Lưu

EXPECTED — bước 1, 2
  hợp lệ, không dấu lỗi; nhãn trạng thái "Chưa lưu"

EXPECTED — bước 3 (5,1 > 5)
  ô Lề dưới        đánh dấu lỗi TẠI CHỖ kèm nội dung
                   MSG_PMKT-E-14549_21_213 — "Căn lề phải là số từ 0 đến 5 cm"
  dòng khối "Thiết lập mẫu" và khối trên trang xem trước đều mang dấu lỗi
  nhãn trạng thái  "Có lỗi"

EXPECTED — bước 4 (1,25 — quá một chữ số lẻ)
  vẫn lỗi, vẫn MSG_PMKT-E-14549_21_213; nhãn trạng thái "Có lỗi"

EXPECTED — bước 5
  dấu hiệu lỗi     TẮT NGAY ở cả hai nơi
  nhãn trạng thái  "Chưa lưu"

EXPECTED — bước 6
  Lưu được; MSG_PMKT-E-14549_21_101
  `giayVaChu.leTren`=0 · **`leTrai` vắng mặt** (chưa sửa ⇒ theo chung, in ra 1,5)
  · `leDuoi`=1,2 · `lePhai`=5
```

### S-TLMI-019 · Độ rộng cột tại biên 3 · 90 và ngoài biên 2 · 91

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-108, R-TLMI-239 (V05), INV-TLMI-005

TIỀN ĐỀ
  khối Bảng có 2 cột tick in: C1 Rộng 50, C4 Rộng 50

THAO TÁC
  1. C1 = 90, C4 = 10, rời ô
  2. C4 = 3, rời ô
  3. C4 = 2, rời ô
  4. C4 = 91, rời ô
  5. Sửa C4 = 10 → Lưu

EXPECTED — bước 1, 2
  hợp lệ; 90 và 3 là biên **trong**; dòng tổng báo "Tổng độ rộng cột đang 100%" (bước 1)
  và "Tổng độ rộng cột đang 93% (nên = 100%)" (bước 2) — không phải lỗi

EXPECTED — bước 3 (2 < 3) và bước 4 (91 > 90)
  ô Rộng %         dấu lỗi tại chỗ,
                   MSG_PMKT-E-14549_21_205 — "Độ rộng cột phải là số nguyên từ 3 đến 90"
  nhãn trạng thái  "Có lỗi"; bấm Lưu ⇒ không ghi (xem S-TLMI-037)

EXPECTED — bước 5
  Lưu được; sau commit đọc lại: Σ DoRong(cột tick in) = 100 và mọi cột trong [3, 90]
  (90 + 10 = 100 ⇒ thuật toán chia lại giữ nguyên)              ← INV-TLMI-005
```

### S-TLMI-020 · Cỡ chữ tiêu đề tại biên 10 · 36 và ngoài biên 9 · 37

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-086, R-TLMI-239 (V02)

TIỀN ĐỀ
  khối Tiêu đề: Cỡ chữ = 18 (mặc định), Nội dung = "CHỨNG TỪ MUA DỊCH VỤ"

THAO TÁC
  1. Cỡ chữ = 10, rời ô → 2. Cỡ chữ = 36, rời ô
  3. Cỡ chữ = 9, rời ô  → 4. Cỡ chữ = 37, rời ô
  5. Cỡ chữ = 20 → Lưu

EXPECTED — bước 1, 2
  hợp lệ; trang xem trước vẽ lại ngay với cỡ chữ tương ứng
  cỡ chữ tiêu đề ĐỘC LẬP với cỡ chữ chung (12) — không ảnh hưởng chữ thân bản in

EXPECTED — bước 3, 4
  ô Cỡ chữ         dấu lỗi tại chỗ,
                   MSG_PMKT-E-14549_21_202 — "Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36"
  nhãn trạng thái  "Có lỗi"

EXPECTED — bước 5
  Lưu được; khối Tiêu đề.CoChu = 20;  MSG_PMKT-E-14549_21_101
```

### S-TLMI-021 · Bảng còn đúng 1 cột rồi bỏ tick nốt

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-103, R-TLMI-104, R-TLMI-239 (V03), INV-TLMI-004

TIỀN ĐỀ
  khối "Bảng Hàng hóa, dịch vụ" **đang bật** (con mắt = Có)
  4 cột, chỉ còn C1 "Tên hàng" tick in (Rộng 100); C2, C3, C4 đã bỏ tick

THAO TÁC
  1. Bỏ tick in cột C1
  2. Tắt con mắt khối Bảng rồi bỏ tick C1 (đối chứng)
  3. (BE) POST lưu mẫu có khối Bảng **đang bật** với 0 cột tick

EXPECTED — bước 1
  chặn NGAY tại chỗ (thời điểm "Khi bỏ tick cột")
  thông báo        MSG_PMKT-E-14549_21_203 — `Bảng "Hàng hóa, dịch vụ" phải giữ lại ít nhất
                   1 cột hiển thị`   ({TenBang} = "Hàng hóa, dịch vụ")
  ô tick của C1    vẫn = Có

EXPECTED — bước 2
  **KHÔNG chặn** — khối đã tắt con mắt thì **bỏ qua validate của khối đó**   ← C18 / B-19
  bỏ tick được cột cuối cùng; badge vẫn "Chưa lưu", không có MSG_…_203
  Bật lại con mắt ⇒ validate chạy lại ngay và báo MSG_…_203 — xem S-TLMI-066.

EXPECTED — bước 3
  HTTP 400 + MSG_PMKT-E-14549_21_203 kèm {TenBang};  DB không đổi
  ∀ khối Bảng HienThi=Có: COUNT(cột HienThi=Có) ≥ 1               ← INV-TLMI-004
```

---

### S-TLMI-022 · Chia đều về 100% — ca 40 / 40 / 40 → 33 / 33 / 34

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-114, R-TLMI-111, INV-TLMI-005

TIỀN ĐỀ
  khối Bảng có 3 cột, cả 3 **đang tick in**:  C1 = 40 · C2 = 40 · C3 = 40  (tổng cũ = 120)

THAO TÁC
  1. Bấm link "Chia đều về 100%"   (hoặc: bấm Lưu — R-TLMI-111 gọi cùng thuật toán)

EXPECTED — từng bước của thuật toán
  bước 1   xét C1, C2, C3 (đều tick in)
  bước 2   C1 = 40 ÷ 120 × 100 = 33,33 → làm tròn XUỐNG → 33
           C2 = 33     · C3 = 33        ⇒ tổng = 99
  bước 3   thiếu 1 để đủ 100 ⇒ cộng vào **cột đang in cuối cùng** (C3): 33 → 34
  bước 4   không cột nào < 3 ⇒ không nâng, không trừ

EXPECTED — kết quả
  C1 = 33 · C2 = 33 · C3 = **34**;  Σ = 100
  TỶ LỆ giữa các cột được giữ — KHÔNG phải chia bằng nhau một cách máy móc
  dòng tổng dưới lưới cột: "Tổng độ rộng cột đang 100%"
```

### S-TLMI-023 · Chia đều về 100% — ca 50 / 30 → 62 / 38

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-114, INV-TLMI-005

TIỀN ĐỀ
  khối Bảng có 2 cột tick in:  C1 = 50 · C2 = 30   (tổng cũ = 80)

THAO TÁC
  1. Bấm "Chia đều về 100%"

EXPECTED
  bước 2   C1 = 50 ÷ 80 × 100 = 62,5 → 62
           C2 = 30 ÷ 80 × 100 = 37,5 → 37        ⇒ tổng = 99
  bước 3   thiếu 1 ⇒ cộng vào cột đang in cuối cùng (C2): 37 → **38**
  bước 4   62 ≥ 3 và 38 ≥ 3 ⇒ không nâng
  kết quả  C1 = 62 · C2 = 38;  Σ = 100;  cả hai trong [3, 90]
```

### S-TLMI-024 · Chia đều về 100% — ca chạm sàn 3: 90 / 70 / 2 → 54 / 43 / 3

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-114, R-TLMI-108, INV-TLMI-005

TIỀN ĐỀ
  khối Bảng có 3 cột tick in:  C1 = 90 · C2 = 70 · C3 = 2   (tổng cũ = 162)
  (C3 = 2 đến từ dữ liệu cũ / tỷ lệ cột trên lưới form, chưa qua bước kiểm 3–90)

THAO TÁC
  1. Bấm "Chia đều về 100%"

EXPECTED — từng bước
  bước 2   C1 = 90 ÷ 162 × 100 = 55,55… → 55
           C2 = 70 ÷ 162 × 100 = 43,20… → 43
           C3 =  2 ÷ 162 × 100 =  1,23… →  1        ⇒ tổng = 99
  bước 3   thiếu 1 ⇒ cộng vào cột đang in cuối cùng (C3): 1 → 2   ⇒ tổng = 100
  bước 4   C3 = 2 < 3 ⇒ **nâng lên 3** (phần nâng = 1)
           trừ 1 vào **cột rộng nhất** = C1 (55) → 54

EXPECTED — kết quả
  C1 = 54 · C2 = 43 · C3 = **3**;  Σ = 54 + 43 + 3 = 100
  mọi cột trong [3, 90]                                          ← INV-TLMI-005
  KHÔNG có MSG_…_205 — đây là hệ thống tự chia, không phải người dùng nhập sai
```

### S-TLMI-025 · Chia đều 100% với 4 cột đều nhau và một cột bỏ tick

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-112, R-TLMI-113, R-TLMI-114, INV-TLMI-005

TIỀN ĐỀ
  khối Bảng có 5 cột:
    C1 = 10 (tick) · C2 = 10 (tick) · C3 = 10 (tick) · C4 = 10 (tick)
    C5 = **bỏ tick**, Rộng % để **trống** (chưa từng đặt)

THAO TÁC
  1. Bấm "Chia đều về 100%"
  2. Tick lại C5, rồi bấm "Chia đều về 100%" lần nữa

EXPECTED — bước 1
  chỉ xét C1…C4 (tổng cũ = 40):  mỗi cột = 10 ÷ 40 × 100 = 25,0 → 25  ⇒ tổng = 100
  không cộng bù, không nâng sàn
  kết quả   C1 = C2 = C3 = C4 = 25;  **C5 giữ nguyên: bỏ tick, Rộng % trống**
  C5 KHÔNG tính vào tổng

EXPECTED — bước 2
  C5 được tick lại ⇒ nhận **phần chia** của nút Chia đều      ← R-TLMI-113
  xét C1…C5, C5 đang trống ⇒ sau chia mỗi cột nhận phần của mình; Σ = 100
  và mọi cột tick in ≥ 3

  **C31 chốt**: nút "Chia đều về 100%" áp cho **mọi cột đang tick in**, không phụ thuộc ô
  Tìm cột (ô tìm chỉ lọc hiển thị) — xem S-TLMI-070.
```

### S-TLMI-026 · Tên khối tự do 60 · 61 · trống

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-121, R-TLMI-239 (V06)

TIỀN ĐỀ
  mẫu có 0 khối tự do

THAO TÁC
  1. + Thêm khối tự do → gõ tên **60 ký tự** ("A"×60) → Thêm
  2. + Thêm khối tự do → gõ tên **61 ký tự** ("A"×61) → Thêm
  3. + Thêm khối tự do → xóa trắng tên → Thêm
  4. (BE) POST lưu mẫu có khối tự do TenKhoi = "" (rỗng)

EXPECTED — bước 1
  khối tạo thành công, TenKhoi dài 60 ký tự; MSG_PMKT-E-14549_21_104

EXPECTED — bước 2 và 3
  hộp Đặt tên khối **không đóng**
  thông báo   MSG_PMKT-E-14549_21_206 — "Tên khối tự do không được để trống, tối đa 60 ký tự"
  Bố cục mẫu  KHÔNG thêm khối nào

EXPECTED — bước 4
  HTTP 400 + MSG_PMKT-E-14549_21_206;  DB không đổi

  **C07 chốt**: tên khối sửa được ở **cả hai chỗ** — hộp Đặt tên khối lúc thêm **và** ô Tên khối
  trên bảng chỉnh; hai chỗ cùng ghi một trường. Xem S-TLMI-064.
  ⚠ Hai khối tự do có được **trùng tên** không: `Z-11` vẫn im lặng, `04` không chốt ⇒ ca "đặt
  tên trùng khối đã có" vẫn không ghi được — xem §B.
```

### S-TLMI-027 · Chữ tự do và Tên hiển thị của trường tại 255 · 256

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-147, R-TLMI-148, R-TLMI-156, R-TLMI-157, R-TLMI-158, R-TLMI-164,
            R-TLMI-237, R-TLMI-239 (V13), INV-TLMI-009

TIỀN ĐỀ
  hai khối tự do: "Khối A" và "Khối B"
  trường "Số chứng từ" đang đặt ở ô (1,1) của **cả hai** khối
  Tên hiển thị của "Số chứng từ" = "Số chứng từ" (mặc định = tên trường)
  trường "Người nộp tiền" **chưa được đặt vào ô nào**

THAO TÁC
  1. Ô (1,2) của Khối A: nháy đúp → Chữ tự do → gõ **255** ký tự → Enter
  2. Sửa ô đó thành **256** ký tự → rời ô
  3. Sửa lại còn 255 ký tự → rời ô
  4. Bảng chỉnh Khối A: đổi Tên hiển thị của "Số chứng từ" thành "Số CT" → rời ô
  5. Đổi Tên hiển thị của "Số chứng từ" thành chuỗi **256** ký tự → rời ô
  6. Ô (2,1) Khối A: nháy đúp → chọn Chữ tự do → **rời ô mà chưa gõ gì**
  7. Đổi Tên hiển thị của "Người nộp tiền" thành "Người nộp" (trường chưa đặt ở ô nào) → Lưu

EXPECTED — bước 1
  hợp lệ, in đúng 255 ký tự trên trang xem trước

EXPECTED — bước 2 và bước 5
  dấu lỗi tại chỗ (ô lưới ⇒ **viền đỏ ngay trên trang xem trước**),
  thông báo  MSG_PMKT-E-14549_21_212 — "Tên hiển thị và chữ tự do tối đa 255 ký tự"
  nhãn trạng thái "Có lỗi"

EXPECTED — bước 3
  dấu lỗi tắt ngay; nhãn trạng thái "Chưa lưu"

EXPECTED — bước 4
  ô (1,1) của **Khối A** in "Số CT: CT-2026-000123"
  ô (1,1) của **Khối B** đổi theo NGAY trên trang xem trước: "Số CT: CT-2026-000123"
  (Tên hiển thị là thuộc tính CỦA TRƯỜNG, dùng chung cả mẫu)     ← INV-TLMI-009

EXPECTED — bước 6
  ô (2,1) **tự trở về Ô trống**; **KHÔNG** báo lỗi              ← R-TLMI-148
  (ô trống không bao giờ là lỗi; chỉ xét lỗi ở ô CÓ nội dung)

EXPECTED — sau Lưu ở bước 7
  đọc lại mẫu   trường "Số chứng từ" có **đúng một** TenHienThi = 'Số CT'
                trường "Người nộp tiền" **KHÔNG được lưu** TenHienThi / InDam
                (chưa đặt vào ô nào)                             ← R-TLMI-164
```

### S-TLMI-028 · Tên hiển thị của cột 100 · 101 · trống

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-101, R-TLMI-102, R-TLMI-239 (V04)

TIỀN ĐỀ
  khối Bảng, cột C1: Tên cột dữ liệu = "Tên hàng" (chỉ đọc), Tên hiển thị = "Tên hàng"

THAO TÁC
  1. Tên hiển thị = chuỗi **100** ký tự → rời ô
  2. Tên hiển thị = chuỗi **101** ký tự → rời ô
  3. Tên hiển thị = "" (xóa trắng) → rời ô
  4. Thử sửa ô "Tên cột dữ liệu"
  5. Sửa Tên hiển thị = "Diễn giải hàng hóa" → Lưu

EXPECTED — bước 1
  hợp lệ; tiêu đề cột trên trang xem trước đổi theo ngay

EXPECTED — bước 2 và 3
  dấu lỗi tại chỗ,
  MSG_PMKT-E-14549_21_204 — "Tên hiển thị của cột không được để trống, tối đa 100 ký tự"
  nhãn trạng thái "Có lỗi"

EXPECTED — bước 4
  ô "Tên cột dữ liệu"  **chỉ đọc**, không sửa được (lấy theo đặc tả form)

EXPECTED — bước 5
  Lưu được; noi_dung.khoi[bang].cot[C1].tenHienThi = 'Diễn giải hàng hóa';
  MSG_PMKT-E-14549_21_101
```

### S-TLMI-029 · Tiêu đề bản in 255 · 256 · trống

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-085, R-TLMI-087, R-TLMI-088, R-TLMI-089, R-TLMI-090, R-TLMI-091,
            R-TLMI-239 (V01)

TIỀN ĐỀ
  khối Tiêu đề: Nội dung = "Chứng từ mua dịch vụ", IN HOA = Có, In đậm = Có, Căn = Giữa

THAO TÁC
  1. Nội dung = chuỗi **255** ký tự → rời ô
  2. Nội dung = chuỗi **256** ký tự → rời ô
  3. Nội dung = "" → rời ô
  4. Nội dung = "Chứng từ mua dịch vụ", IN HOA = Không → Lưu, In
  5. IN HOA = Có, Căn = Phải → Lưu, In

EXPECTED — bước 1
  hợp lệ

EXPECTED — bước 2 và 3
  dấu lỗi tại chỗ,
  MSG_PMKT-E-14549_21_201 — "Tiêu đề bản in không được để trống, tối đa 255 ký tự"
  nhãn trạng thái "Có lỗi"

EXPECTED — bước 4 (bản in)
  dòng tiêu đề     "Chứng từ mua dịch vụ"  — in ĐÚNG như gõ, đậm, căn giữa
  dòng ngay dưới   "Ngày 05 tháng 09 năm 2026"  — chữ nghiêng, căn giữa
  **Số chứng từ KHÔNG in trong khối Tiêu đề** — muốn in phải đưa vào khối tự do

EXPECTED — bước 5 (bản in)
  dòng tiêu đề     "CHỨNG TỪ MUA DỊCH VỤ"  — in hoa, căn **phải**
  dòng ngày tháng  căn **phải** (Căn của khối áp cho CẢ hai dòng)

  **C18 chốt**: khối Tiêu đề bị **ẩn** thì **bỏ qua validate** của khối đó — xem S-TLMI-065.
```

### S-TLMI-030 · Tiêu đề ô ký tự do 60 · 61 · trống, khi bật và khi tắt

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-187, R-TLMI-189, R-TLMI-191, R-TLMI-192, R-TLMI-239 (V12), INV-TLMI-010

TIỀN ĐỀ
  khối Chữ ký có 1 ô ký tự do vừa thêm: Tiêu đề in ra trống, tick = Có

THAO TÁC
  1. Tiêu đề in ra = chuỗi **60** ký tự → rời ô
  2. Tiêu đề in ra = chuỗi **61** ký tự → rời ô
  3. Tiêu đề in ra = "" → rời ô
  4. Bỏ tick ô ký tự do đó (tick = Không), giữ Tiêu đề = "" → Lưu
  5. (BE) POST lưu mẫu có ô ký tự do **đang bật** với TieuDe = "" và với TieuDe 61 ký tự

EXPECTED — bước 1
  hợp lệ

EXPECTED — bước 2 và 3
  dấu lỗi tại chỗ,
  MSG_PMKT-E-14549_21_211 — "Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự"
  nhãn trạng thái "Có lỗi"

EXPECTED — bước 4
  **Lưu được** — ô ký tự do TẮT thì tiêu đề trống không phải lỗi
  MSG_PMKT-E-14549_21_101;  noi_dung.khoi[chuKy].oKy[đó]: hienThi = Không, tieuDe = ''
  bản in                    KHÔNG in ô ký đó

EXPECTED — bước 5
  cả hai lần: HTTP 400 + MSG_PMKT-E-14549_21_211;  DB không đổi
  ∀ ô ký tự do HienThi=Có: TieuDe ≠ trống và ≤ 60 ký tự          ← INV-TLMI-010
```

### S-TLMI-031 · Hoàn tác đúng 60 bước, bước thứ 61 thì nút mờ

```
Nhóm        biên
Tầng kiểm   FE
Luật phủ    R-TLMI-041, R-TLMI-223, R-TLMI-224, R-TLMI-226, R-TLMI-227

TIỀN ĐỀ
  mẫu CTMDV vừa mở, badge "Đã lưu", lịch sử Hoàn tác rỗng
  nút Hoàn tác (↶) và Làm lại (↷) đều Disable

THAO TÁC
  1. Thực hiện **61** thao tác đổi mẫu, đếm theo R-TLMI-224, ví dụ:
       · đổi Cỡ chữ tiêu đề 18 → 19 → … (mỗi lần rời ô = 1 bước)
       · thêm 1 dòng vào khối tự do          = 1 bước
       · gộp 2 ô                              = 1 bước
       · bấm nút "Theo thiết lập chung"       = 1 bước  (R-TLMI-041)
  2. Bấm Hoàn tác (hoặc Ctrl+Z) liên tiếp 60 lần
  3. Bấm Hoàn tác lần thứ 61
  4. Bấm Làm lại (Ctrl+Y) 60 lần, rồi lần thứ 61

EXPECTED — sau bước 1
  nút ↶  Enable;  nút ↷  Disable
  lịch sử giữ **đúng 60 bước gần nhất** — bước thứ nhất đã rơi khỏi hàng đợi

EXPECTED — sau bước 2
  mẫu về đúng trạng thái NGAY SAU bước thứ 1 (không về được trạng thái ban đầu)
  nút ↶  **Disable**  (hết bước)
  nút ↷  Enable

EXPECTED — bước 3
  không xảy ra gì (nút đang Disable); mẫu KHÔNG đổi

EXPECTED — bước 4
  tiến lại đủ 60 bước, về đúng trạng thái sau thao tác thứ 61
  nút ↷  Disable;  nút ↶  Enable

  ⚠ **Đặt lại mẫu chuẩn** có phải một bước Hoàn tác được không: tài liệu im lặng (Z-17)
     ⇒ không đưa thao tác đó vào chuỗi 61 bước; xem §B.
```

### S-TLMI-032 · Số cột để tự động in ngang 1 · 50 · 0 · 51 và điều kiện hiện ô

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-055, R-TLMI-056, R-TLMI-057, R-TLMI-058, R-TLMI-059, R-TLMI-060,
            R-TLMI-220, R-TLMI-239 (V15)

TIỀN ĐỀ
  Hướng giấy đang = Dọc; khối Bảng đang bật có **9 cột in**

THAO TÁC
  1. Quan sát ô "Số cột để tự động in ngang" khi Hướng = Dọc
  2. Đổi Hướng giấy = Tự động
  3. Số cột = 1 → rời ô;  4. Số cột = 50 → rời ô
  5. Số cột = 0 → rời ô;  6. Số cột = 51 → rời ô
  7. Số cột = 8 → xem trang xem trước
  8. Số cột = 10 → xem trang xem trước
  9. Tắt con mắt khối Bảng (không còn khối Bảng nào bật) → xem trang xem trước
 10. Đổi Hướng giấy = Ngang, khối Bảng có 2 cột in → xem trang xem trước

EXPECTED — bước 1
  ô "Số cột để tự động in ngang"   **Hide** (chỉ hiện khi Hướng = Tự động)

EXPECTED — bước 3, 4
  hợp lệ (1 và 50 là biên trong)

EXPECTED — bước 5, 6
  dấu lỗi tại chỗ,
  MSG_PMKT-E-14549_21_214 — "Số cột để tự động in ngang phải là số nguyên từ 1 đến 50"
  nhãn trạng thái "Có lỗi"

EXPECTED — bước 7 (ngưỡng 8, bảng có 9 cột in ⇒ 9 ≥ 8)
  trang xem trước và bản in   **in NGANG**

EXPECTED — bước 8 (ngưỡng 10 > 9 cột in)
  in **DỌC**

EXPECTED — bước 9 (không có khối Bảng nào đang bật)
  in **DỌC**                                                     ← R-TLMI-059

EXPECTED — bước 10
  in **NGANG** bất kể chỉ có 2 cột                               ← R-TLMI-060
```

### S-TLMI-033 · Bảy ô tick Thông tin đầu trang — bỏ tick hết và hồ sơ trống

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-043, R-TLMI-076, R-TLMI-077, R-TLMI-078, R-TLMI-079, R-TLMI-080,
            R-TLMI-081, R-TLMI-083, R-TLMI-084, R-TLMI-238, R-TLMI-267

TIỀN ĐỀ
  chứng từ CT-2026-000123 ghi chi nhánh **CN-B**; người dùng đang làm việc ở **CN-A**
  hồ sơ CN-B: Tên "Chi nhánh Hà Nội" · Địa chỉ "12 Láng Hạ" · Mã số thuế **để trống**
  hồ sơ CN-A: Tên "Trụ sở chính" · Địa chỉ "1 Trần Duy Hưng"
  bảy ô tick đầu trang đang **theo chung**; thiết lập chung bật cả bảy
  thiết lập chung: "lặp đầu trang ở trang sau" = Bật

THAO TÁC
  1. Xem bảng chỉnh khối Thông tin đầu trang
  2. In thử (bảng dữ liệu dài 3 trang)
  3. Bỏ tick **cả bảy** dòng → Lưu → In
  4. Bấm nút "Theo thiết lập chung" của khối Thông tin đầu trang

EXPECTED — bước 1
  mỗi dòng tick hiển thị kèm **giá trị thật của CN-B**, không phải CN-A:
    "Tên đơn vị — Chi nhánh Hà Nội" · "Địa chỉ — 12 Láng Hạ" · "Mã số thuế — (trống)" …
  thứ tự các dòng   cố định, không kéo thả

EXPECTED — bước 2 (bản in)
  dòng "Mã số thuế"   **bỏ qua** — không in dòng trống          ← R-TLMI-079
  khối Thông tin đầu trang **lặp lại** ở trang 2 và trang 3     ← R-TLMI-084

EXPECTED — bước 3
  Lưu được; **KHÔNG** có lỗi, **KHÔNG** có cảnh báo mềm         ← R-TLMI-080, R-TLMI-238
  noi_dung.khoi[dauTrang]  bảy khóa tick **có mặt** và = Không (đã sửa ⇒ **riêng**):
    inTenDonVi · inDiaChi · inMaSoThue · inSoDienThoai · inEmail · inTaiKhoanNganHang
    · **inLogo**   (Logo là một trong bảy ô — C03)
  bản in   khối Thông tin đầu trang **không in gì**; khối Tiêu đề dồn lên

EXPECTED — bước 4
  cả **bảy** ô tick về **theo chung** ⇒ bảy khóa **bị xóa khỏi JSON** (vắng mặt)
  giá trị hiển thị lại lấy từ thiết lập chung (bật cả bảy)

  **C03 chốt**: Logo **CÓ** nằm trong bảy ô tick mà mẫu sửa riêng được — xem S-TLMI-061.
  **C29 chốt**: vị trí logo khi Căn lề ≠ Trái — xem S-TLMI-075.
```

### S-TLMI-034 · Khối tự do đang bật mà mọi ô đều trống

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-143, R-TLMI-176, R-TLMI-180, R-TLMI-181, R-TLMI-236, R-TLMI-237

TIỀN ĐỀ
  khối tự do "Chừa chỗ": lưới 3 dòng × 2 cột, **mọi ô đều là Ô trống**, con mắt = Có
  khối tự do "Thông tin chung": ô (1,1) gộp 1 dòng × 2 cột, chứa trường "Diễn giải"
    có giá trị dài 300 ký tự

THAO TÁC
  1. Lưu
  2. In

EXPECTED — bước 1
  **Lưu được**; MSG_PMKT-E-14549_21_101
  KHÔNG có dấu lỗi ở ô nào — ô trống không bao giờ là lỗi        ← R-TLMI-236
  noi_dung.khoi["Chừa chỗ"].oLuoi[]  6 phần tử loại `O_TRONG`  (soDong=3 · soCot=2)

EXPECTED — bước 2 (bản in)
  khối "Chừa chỗ"    in ra **một khoảng trống bằng chiều cao 3 dòng**, không chữ, không kẻ
  ô gộp ở "Thông tin chung"  chiếm **đúng 1 dòng × 2 cột** như đã gộp
  giá trị 300 ký tự  **tự xuống dòng** trong ô; các ô cùng hàng cao bằng nhau
```

### S-TLMI-059 · Form đổi phiên bản — thêm cột và **bỏ** cột

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-092, R-TLMI-093, R-TLMI-101, R-TLMI-107, R-TLMI-114, R-TLMI-165,
            R-TLMI-167, INV-TLMI-005
Quyết định  **C10 chốt** — phần tử không còn trong đặc tả form:
              · **khi IN**: bỏ qua **im lặng** — không in, không báo lỗi, bản in **không vỡ**
              · **khi MỞ màn Thiết lập mẫu in**: hiện **mờ + nhãn "không còn trên form"**,
                và **bị loại khỏi mẫu khi Lưu**
            Nguyên tắc: *bản in không bao giờ được vỡ vì cấu hình cũ.*

TIỀN ĐỀ
  mẫu CTMDV đã lưu, khối Bảng có 3 cột tick in: C1 = 50 · C3 = 25 · C4 = 25 (Σ = 100)
  khối tự do "Thông tin chung" có ô (1,1) = trường **"Người nộp tiền"**
  form của nghiệp vụ nâng phiên bản:
    · **THÊM** cột C6 "Tiền thuế" vào lưới (cột **tiền**)
    · **THÊM** ô "Người giao hàng" ngoài lưới
    · **BỎ** cột C3 "Đơn giá" khỏi lưới
    · **BỎ** trường "Người nộp tiền" khỏi form

THAO TÁC
  1. In Mẫu tùy chỉnh **trước khi** mở màn thiết lập
  2. Mở màn Thiết lập mẫu in, xem lưới cột và lưới khối tự do
  3. Không sửa gì thêm, bấm **Lưu**
  4. Đọc lại `noi_dung`

EXPECTED — bước 1 (bản in, chiều BỎ)
  cột C3 "Đơn giá"        **KHÔNG in**, không báo lỗi, không để lại ô trống lệch cột
  ô (1,1) "Người nộp tiền" **KHÔNG in**, ô chỉ **chiếm chỗ** như Ô trống (R-TLMI-143)
  bản in                  dựng trọn vẹn, **không vỡ bố cục**, không có dòng lỗi nào
  cột C6 "Tiền thuế"      **CÓ in** ở cuối bảng ngay lần in này (mặc định in)

EXPECTED — bước 2 (màn thiết lập, chiều THÊM)
  C6 "Tiền thuế"   xuất hiện ở **cuối bảng**, ô tick in = **Có**
  Căn              **Phải** (cột số) · ô Cộng Show và mặc định **Có** (cột tiền)
  "Người giao hàng"  **tự vào kho trường**, **KHÔNG tự chen** vào khối tự do nào
  độ rộng          các cột đang tick in chia lại theo thuật toán R-TLMI-114 ⇒ Σ = 100

EXPECTED — bước 2 (màn thiết lập, chiều BỎ)
  dòng cột C3 "Đơn giá"    hiện **mờ** + nhãn **"không còn trên form"**, không sửa được
  ô (1,1) khối tự do       hiện **mờ** + nhãn **"không còn trên form"**
  **KHÔNG** báo lỗi, badge **KHÔNG** chuyển "Có lỗi" — đây không phải lỗi validate

EXPECTED — bước 3 và 4 (Lưu ⇒ dọn)
  noi_dung.khoi[bang].cot[]   **KHÔNG còn** phần tử C3
  noi_dung.khoi[tuDo].oLuoi[] ô (1,1) trở thành `loai = 'O_TRONG'`
  noi_dung.truong[]           **KHÔNG còn** mục "Người nộp tiền"
  độ rộng các cột còn lại     chia lại về **Σ = 100**, mọi cột trong [3, 90] ← INV-TLMI-005
  `phien_ban` tăng 1;  toast MSG_PMKT-E-14549_21_101

  **Thời điểm chia lại độ rộng** (Z-13 cũ) nay xác định được: việc dọn + chia lại **ghi vào DB
  tại bước Lưu**; khi chỉ **in** thì bỏ qua im lặng và **không** ghi gì (R-TLMI-271).
```

---

## §3. Nhóm `ngoại lệ / bị chặn`

### S-TLMI-035 · Không có quyền — ẩn mục menu, ẩn nút Sửa mẫu, server chặn

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-014, R-TLMI-031, R-TLMI-032, R-TLMI-034, R-TLMI-239 (V17), R-TLMI-269

TIỀN ĐỀ
  người dùng u3: CÓ quyền In của nghiệp vụ CTMDV, **KHÔNG** có quyền Thiết lập mẫu in
  u3 đang làm việc ở CN-A;  mẫu (T1, CTMDV, MUA_DV_TRONG_NUOC) đã tồn tại

THAO TÁC
  1. u3 mở form sửa CT-2026-000123 → bấm In
  2. u3 in Mẫu tùy chỉnh → quan sát màn xem trước
  3. u3 gọi thẳng `GET` API mở màn thiết lập mẫu (bằng công cụ ngoài UI)
  4. u3 gọi thẳng `POST` API lưu mẫu

EXPECTED — bước 1
  menu In           các mẫu cố định → đường kẻ → "Mẫu tùy chỉnh"
  mục "Thiết lập mẫu in…"   **Hide — ẩn hẳn, KHÔNG render** (không phải disable)

EXPECTED — bước 2
  nút "Sửa mẫu" trên màn xem trước   **Hide**

EXPECTED — bước 3 và bước 4
  HTTP            403 (hoặc mã lỗi tương ứng của tầng ApiResponse)
  body            MSG_PMKT-E-14549_21_002 — "Bạn không có quyền thực hiện tác vụ này"
  tầng chặn       **Server**, thời điểm "Khi mở màn, khi Lưu"   ← R-TLMI-239 (V17)
  DB              không bản ghi nào bị đổi

  **C13 chốt**: mã quyền = **`HTMauIn.View` / `HTMauIn.Edit`** (đã seed ở `V1149`, đang trên
  develop — không seed thêm), **cộng thêm** `<ChucNang>.View.Detail` của chính nghiệp vụ đang
  mở để không lộ dữ liệu chứng từ qua màn xem trước. Đặt ở hằng số `MaQuyenMauIn` (**Q-15**) —
  sau này đổi sang mã theo nghiệp vụ chỉ sửa một file. Xem thêm S-TLMI-072.
  **C15 chốt**: thiếu **quyền In** dùng **`MSG_COMMON_003`**, **KHÔNG** dùng
  `MSG_PMKT-E-14549_21_002` — xem S-TLMI-071.
```

### S-TLMI-036 · Không có quyền Thiết lập mẫu in nhưng có quyền In

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-024, R-TLMI-033

TIỀN ĐỀ
  như S-TLMI-035;  mẫu tùy chỉnh đã lưu có Màu chữ = #C00000

THAO TÁC
  1. u3 → In → chọn "Mẫu tùy chỉnh"

EXPECTED
  mục "Mẫu tùy chỉnh"   **Show** (không mang điều kiện quyền Thiết lập mẫu in)
  bản in                dựng theo **mẫu tùy chỉnh đã lưu** — chữ màu #C00000
  KHÔNG có MSG_…_002, KHÔNG có MSG_…_103 (đã có bản ghi mẫu)
  tên hai mục menu đúng nguyên văn "Mẫu tùy chỉnh" và "Thiết lập mẫu in…" cho mọi nghiệp vụ
```

### S-TLMI-037 · Bấm Lưu khi đang "Có lỗi" — chỉ báo lỗi đầu tiên

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-232, R-TLMI-233, R-TLMI-235, R-TLMI-242, R-TLMI-243, R-TLMI-244,
            R-TLMI-246, INV-TLMI-012

TIỀN ĐỀ
  mẫu CTMDV đã lưu (bản đã lưu gọi là M0)
  Bố cục mẫu theo thứ tự: 1 Thông tin đầu trang · 2 Tiêu đề · 3 Bảng · 4 Khối tự do · 5 Chữ ký
  ba lỗi được tạo ra, theo đúng thứ tự khối:
    · khối **Tiêu đề**: Cỡ chữ = 9             ⇒ MSG_…_202
    · khối **Bảng**:    Rộng % của C3 = 91     ⇒ MSG_…_205
    · khối **tự do**:   ô (1,2) Chữ tự do 256 ký tự ⇒ MSG_…_212

THAO TÁC
  1. Quan sát nhãn trạng thái và các dấu hiệu lỗi
  2. Rê chuột lên dòng khối "Tiêu đề" ở Bố cục mẫu
  3. Bấm Lưu

EXPECTED — bước 1
  nhãn trạng thái   "Có lỗi"  (badge đỏ)
  nút Lưu           **vẫn Enable** (chỉ trạng thái "Đã lưu" mới Disable)
  mỗi khối lỗi được đánh dấu ở **hai nơi**: dòng khối ở Bố cục mẫu **và** khối trên trang
    xem trước
  ô lưới khối tự do sai   **viền đỏ ngay trên trang xem trước**

EXPECTED — bước 2
  hiện nội dung lỗi của khối Tiêu đề:
    MSG_PMKT-E-14549_21_202 — "Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36"

EXPECTED — bước 3
  **KHÔNG ghi** — 0 bản ghi bị đổi, DB vẫn đúng bằng M0          ← INV-TLMI-012
  hiện **đúng một** thông báo, của **lỗi ĐẦU TIÊN** theo thứ tự khối trong Bố cục mẫu:
    MSG_PMKT-E-14549_21_202
  (KHÔNG hiện MSG_…_205 và MSG_…_212 ở lần bấm này)
  bảng chỉnh        mở khối **Tiêu đề**
  con trỏ           đặt vào ô **Cỡ chữ**
  nhãn trạng thái   vẫn "Có lỗi"

EXPECTED — sửa lần lượt
  sửa Cỡ chữ = 18 → bấm Lưu ⇒ báo MSG_PMKT-E-14549_21_205, mở khối Bảng, focus ô Rộng %
  sửa Rộng % = 25 → bấm Lưu ⇒ báo MSG_PMKT-E-14549_21_212, **chọn ô (1,2) trên trang
                              xem trước** (lỗi ở ô lưới ⇒ không focus bảng chỉnh)
  sửa chữ tự do   → bấm Lưu ⇒ MSG_PMKT-E-14549_21_101, badge "Đã lưu"

  ⚠ Thứ tự "lỗi đầu tiên" **trong cùng một khối** khi khối có cả ô ở bảng chỉnh lẫn ô lưới:
     **C21 chốt**: ô ở bảng chỉnh trước (trên→dưới), rồi tới ô lưới trên trang xem trước
     (trái→phải, trên→dưới) — xem S-TLMI-068.
```

### S-TLMI-038 · Gộp ô khi vùng chọn có từ 2 ô có nội dung

```
Nhóm        ngoại lệ
Tầng kiểm   FE
Luật phủ    R-TLMI-132, R-TLMI-136, R-TLMI-137, R-TLMI-138, R-TLMI-139, R-TLMI-140,
            R-TLMI-141, R-TLMI-142, R-TLMI-174

TIỀN ĐỀ
  khối tự do "Thông tin chung": lưới 2 dòng × 3 cột
    (1,1) = trường "Số chứng từ"        (có nội dung)
    (1,2) = Ô trống
    (1,3) = Chữ tự do "Liên 2"          (có nội dung)
    (2,1) = Chữ tự do "Ghi chú"         (có nội dung)
    (2,2) = Ô trống · (2,3) = Ô trống

THAO TÁC
  1. Bấm ô (1,1), giữ Shift bấm ô (1,3) ⇒ chọn vùng 1 dòng × 3 cột
  2. Bấm "Gộp ô" → chọn **Hủy** ở hộp xác nhận
  3. Bấm "Gộp ô" lần nữa → chọn **Đồng ý**
  4. Chọn ô gộp → bấm "Tách ô"
  5. Gộp lại (1,1)…(1,3), rồi chọn ô (2,2) và bấm "Xóa dòng" — đối chứng ô gộp
  6. Gộp lại, rồi chọn ô trong vùng gộp và bấm "+ Cột trái"

EXPECTED — bước 1
  vùng chọn 3 ô; nút "Gộp ô" **Enable**, nút "Tách ô" **Disable**

EXPECTED — bước 2
  hộp xác nhận   MSG_PMKT-E-14549_21_404 — "Vùng chọn có 3 ô đang có nội dung. Gộp thì chỉ
                 giữ nội dung của ô đầu tiên, các ô còn lại mất nội dung. Tiếp tục?"
                 ⚠ {SoO} = **2** ở đây, vì chỉ (1,1) và (1,3) CÓ nội dung — (1,2) là ô trống.
                 ⇒ nguyên văn hiện ra: "Vùng chọn có 2 ô đang có nội dung. Gộp thì chỉ giữ
                    nội dung của ô đầu tiên, các ô còn lại mất nội dung. Tiếp tục?"
  chọn Hủy       lưới **không đổi**, 3 ô nguyên vẹn

EXPECTED — bước 3 (đồng ý)
  (1,1)…(1,3) thành **một ô** chiếm 1 dòng × 3 cột
  nội dung giữ lại   của **ô đầu tiên có nội dung** theo trái→phải, trên→xuống = (1,1)
                     ⇒ ô gộp mang trường "Số chứng từ"
  "Liên 2"           **mất nội dung**
  nút "Tách ô"       Enable;  nút "Gộp ô"  Disable

EXPECTED — bước 4
  trả về 3 ô đơn; nội dung ở **ô góc trên trái** (1,1); (1,2) và (1,3) là Ô trống

EXPECTED — bước 5
  vùng chọn chạm ô gộp ⇒ **tự nới ra** cho trọn ô gộp;
  xóa dòng đi qua ô gộp ⇒ ô gộp được **tách trước** rồi mới xóa

EXPECTED — bước 6
  ô gộp **rộng thêm một cột** (thành 1 dòng × 4 cột), nội dung giữ nguyên

  **C19 chốt**: Tách ô đưa nội dung về **ô trên-trái** của vùng vừa tách, các ô còn lại thành
  ô trống, **KHÔNG hỏi xác nhận** (không mất dữ liệu) — xem S-TLMI-067.
```

### S-TLMI-039 · Ảnh nền sai định dạng hoặc quá 1MB

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-067, R-TLMI-068, R-TLMI-069, R-TLMI-070, R-TLMI-071, R-TLMI-072,
            R-TLMI-073, R-TLMI-074, R-TLMI-075, R-TLMI-239 (V10)

TIỀN ĐỀ
  Kiểu hình nền = **Không** (mặc định);  Màu chữ = #C00000

THAO TÁC
  1. Quan sát ba ô Độ đậm / Căn ảnh / Ảnh khi Kiểu = Không
  2. Đổi Kiểu hình nền = **Khung viền**
  3. Đổi Kiểu hình nền = **Ảnh tải lên**
  4. Chọn tệp `nen.gif` (320 KB)
  5. Chọn tệp `nen.png` (1,4 MB)
  6. Chọn tệp `nen.png` (820 KB), Căn ảnh = Giữa trang, Độ đậm = 20 → Lưu, In

EXPECTED — bước 1
  Độ đậm · Căn ảnh · Ảnh   cả ba **Hide**;  bản in không có hình nền

EXPECTED — bước 2
  ô **Độ đậm** Show và bắt buộc; Căn ảnh và Ảnh vẫn Hide
  trang xem trước   kẻ **khung quanh mép trang** theo **màu chữ** (#C00000)
  Độ đậm mặc định   20

EXPECTED — bước 3
  cả ba ô Độ đậm · Căn ảnh · Ảnh đều **Show** và bắt buộc; Căn ảnh mặc định = Giữa trang

EXPECTED — bước 4 và bước 5
  chặn NGAY **khi chọn tệp** (Client và Server),
  thông báo   MSG_PMKT-E-14549_21_209 — "Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB"
  ô Ảnh       vẫn trống; hình nền không đổi

EXPECTED — bước 6
  Lưu được; bản in: ảnh vẽ **dưới mọi khối**, giữ tỷ lệ, nằm giữa trang,
  không làm dịch chuyển vị trí khối nào
  (Căn ảnh = Toàn trang ⇒ kéo giãn phủ kín phần giấy **trong lề**)

  **C08 chốt**: ảnh lưu ở **cột `anh_nen` (`bytea`)** của chính `prn_mau_in_tuy_chinh`, kèm
  `anh_nen_kieu_tep` và `anh_nen_ten_tep`; JSON **chỉ** giữ cờ `rieng.nen.kieu = 'ANH'`.
  Tải lên bằng **`multipart`, endpoint riêng** — xem S-TLMI-073.
  ⚠ Vi phạm miền **Độ đậm** (5–100 %) vẫn **không có mã message** — `Z-03` chưa được nâng
  thành mục `C` và `04` không chốt. Ca đó vẫn không ghi được, xem §B.
```

### S-TLMI-040 · Màu chữ sai dạng #rrggbb

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-064, R-TLMI-065, R-TLMI-066, R-TLMI-239 (V11)

TIỀN ĐỀ
  Màu chữ = #000000 (mặc định của mẫu, KHÔNG kế thừa thiết lập chung)

THAO TÁC
  1. Gõ mã màu `#GG0011` → rời ô
  2. Gõ `12ab34` (thiếu dấu #) → rời ô
  3. Gõ `#12ab34` → rời ô → Lưu → In

EXPECTED — bước 1 và 2
  dấu lỗi tại chỗ,
  MSG_PMKT-E-14549_21_210 — "Mã màu phải có dạng #rrggbb"
  nhãn trạng thái  "Có lỗi";  màu đang áp trên trang xem trước **không đổi** (vẫn #000000)

EXPECTED — bước 3
  hợp lệ; Lưu được; noi_dung.rieng.mauChu = '#12ab34'
  bản in   **toàn bộ chữ và đường kẻ** mang màu #12ab34, **TRỪ logo** (logo giữ màu gốc)

  ⚠ Tài liệu nói "10 ô màu" nhưng **không liệt kê 10 mã màu**; Figma đếm 9 ô preset + ô hex
     (Z-04) ⇒ ca "bấm ô màu thứ n" KHÔNG ghi được expected state — xem §B.
```

### S-TLMI-041 · Xóa khối tự do; khối chuẩn không có nút xóa

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-175, R-TLMI-203, R-TLMI-210, R-TLMI-211, R-TLMI-212, INV-TLMI-008

TIỀN ĐỀ
  Bố cục mẫu: Thông tin đầu trang · Tiêu đề · Bảng Hàng hóa, dịch vụ · **Thông tin chung**
              (khối tự do, 2 ô có nội dung) · Chữ ký

THAO TÁC
  1. Quan sát nút xóa trên các dòng khối
  2. Bấm ✕ trên dòng khối "Thông tin chung" → chọn **Hủy**
  3. Bấm nút "Xóa khối này" ở bảng chỉnh của khối đó → chọn **Đồng ý**

EXPECTED — bước 1
  dòng khối chuẩn (đầu trang · Tiêu đề · Bảng · Chữ ký)   **KHÔNG render nút ✕** (Hide)
  dòng khối tự do                                          có nút ✕
  nút xóa của khối tự do có ở **cả hai nơi**: dòng khối và bảng chỉnh
  tên khối chuẩn cố định, không sửa được; khối Bảng tên = "Bảng Hàng hóa, dịch vụ"

EXPECTED — bước 2
  hộp xác nhận  MSG_PMKT-E-14549_21_403 — `Xóa khối "Thông tin chung" cùng các ô trong đó?`
                ({TenKhoi} = "Thông tin chung")
  chọn Hủy      khối **còn nguyên**, 2 ô có nội dung không mất

EXPECTED — bước 3
  cùng hộp xác nhận MSG_PMKT-E-14549_21_403; đồng ý ⇒ khối bị xóa khỏi Bố cục mẫu
  4 loại khối chuẩn vẫn còn đủ                                  ← INV-TLMI-008
  nhãn trạng thái  "Chưa lưu"  (chưa ghi DB cho tới khi bấm Lưu)
```

### S-TLMI-042 · Lỗi hệ thống giữa vòng ghi bảng con — rollback

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-247, R-TLMI-249, INV-TLMI-012

TIỀN ĐỀ
  mẫu đã lưu M0: 5 khối, khối Bảng 3 cột (50/25/25), khối Chữ ký 5 ô ký
  người dùng đã sửa: thêm 1 khối tự do 2 ô, đổi Tiêu đề, đổi Rộng % ⇒ badge "Chưa lưu"
  ép lỗi hệ thống xảy ra **sau** khi đã `UPDATE` cột `noi_dung` và **trước** khi commit
  (ví dụ: lỗi khi ghi cột `anh_nen` hoặc khi tăng `phien_ban`)

THAO TÁC
  1. Bấm Lưu

EXPECTED
  transaction     **rollback** toàn bộ
  prn_mau_in_tuy_chinh  đọc lại ⇒ `noi_dung` **đúng bằng M0** từng byte sau chuẩn hóa,
                  `phien_ban` **không tăng**, `anh_nen` không đổi     ← INV-TLMI-012
  thông báo       MSG_PMKT-E-14549_21_003 — "Lỗi hệ thống, vui lòng thử lại sau"
  màn             **giữ nguyên** — không đóng, không mất thay đổi đang chỉnh
  nhãn trạng thái vẫn "Chưa lưu"
```

### S-TLMI-043 · Lỗi hệ thống khi dựng bản in

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-270, R-TLMI-271

TIỀN ĐỀ
  mẫu CTMDV đã lưu; ép lỗi hệ thống ở bước dựng bản in

THAO TÁC
  1. Mở CT-2026-000123 → In → "Mẫu tùy chỉnh"

EXPECTED
  thông báo       MSG_PMKT-E-14549_21_003 — "Lỗi hệ thống, vui lòng thử lại sau"
  màn xem trước   **KHÔNG mở**
  dữ liệu chứng từ và mẫu   không đổi
```

---

### S-TLMI-044 · Nút In bị disable theo hai quy tắc cấm in

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-261
Quyết định  **C14 chốt** — giữ NGUYÊN VĂN hai tooltip, đặt **key i18n cục bộ**, KHÔNG có mã `MSG_`

TIỀN ĐỀ
  thiết lập chung: "cho phép in chứng từ chưa ghi sổ" = **Không**
                   "cho phép in chứng từ đã khóa sổ"  = **Không**
  CT-A  trạng thái **chưa ghi sổ**
  CT-B  thuộc kỳ **đã khóa sổ**
  CT-C  đã ghi sổ, kỳ chưa khóa
  mẫu tùy chỉnh của nghiệp vụ đã lưu

THAO TÁC
  1. Mở CT-A → bấm nút In
  2. Mở CT-B → bấm nút In
  3. Mở CT-C → bấm nút In
  4. Trên CT-B: bấm Xuất Excel

EXPECTED — bước 1 và 2
  nút In        **Disable**
  menu In       **KHÔNG mở được** — kể cả mục "Mẫu tùy chỉnh"
  tooltip CT-A  nguyên văn **"Đơn vị không cho phép in chứng từ chưa ghi sổ"**
  tooltip CT-B  nguyên văn **"Đơn vị không cho phép in chứng từ đã khóa sổ"**
  cả hai chuỗi  có **key i18n ở cả `vi.ts` và `en.ts`** (luật 2), **KHÔNG mang mã `MSG_`**
  không có toast / hộp thoại nào (đây là tooltip, không phải thông báo)

EXPECTED — bước 3
  nút In Enable; menu In mở bình thường; "Mẫu tùy chỉnh" dựng bản in theo mẫu đã lưu

EXPECTED — bước 4
  quy tắc "đã khóa sổ" **chỉ** tác động nút In của chứng từ
  ⇒ **Xuất Excel vẫn chạy**, không bị chặn

EXPECTED — cổng `msg.sh`
  `msg.sh` **sẽ báo `THIEU`** cho hai chuỗi này cho tới khi BA cấp mã — đây là **kết quả đúng
  đã được chấp nhận** (`04` §5 L-5, §7 mục 1), KHÔNG phải lỗi cần sửa bằng cách tự đặt mã.
  Test hồi quy đối chiếu theo **key i18n**, không theo mã `MSG_`.
```

### S-TLMI-045 · Xóa khối chuẩn qua API; lưu mẫu thiếu khối chuẩn

```
Nhóm        ngoại lệ
Tầng kiểm   BE
Luật phủ    R-TLMI-008, R-TLMI-009, R-TLMI-092, R-TLMI-210, INV-TLMI-008

TIỀN ĐỀ
  mẫu CTMDV đã lưu, 5 khối (4 loại khối chuẩn + 1 khối tự do)

THAO TÁC
  1. Gọi API xóa khối với id của khối **Tiêu đề**
  2. Gọi API xóa khối với id của khối **Bảng Hàng hóa, dịch vụ**
  3. POST lưu mẫu mà payload **thiếu** khối Chữ ký
  4. POST lưu mẫu mà payload có **2** khối Bảng trong khi form chỉ có 1 lưới

EXPECTED — bước 1, 2
  **từ chối** — khối chuẩn không xóa được, chỉ ẩn được bằng con mắt
  DB không đổi

EXPECTED — bước 3, 4
  **từ chối**; DB không đổi
  ∀ mẫu: vẫn tồn tại khối Thông tin đầu trang, Tiêu đề, **n** khối Bảng (n = số lưới form),
  Chữ ký — chúng chỉ đổi ThuTu và HienThi                       ← INV-TLMI-008

  ⚠ Mã message cho hai nhánh từ chối này **không có** trong 26 mã của `6.messages.md`
     ⇒ expected "body trả mã nào" KHÔNG ghi được — xem §B.
```

### S-TLMI-046 · Ô ký chức danh không xóa được, chỉ tắt được

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-185, R-TLMI-186, R-TLMI-191, R-TLMI-192, R-TLMI-196

TIỀN ĐỀ
  khối Chữ ký: 5 chức danh + 1 ô ký tự do "NGƯỜI NHẬN HÀNG"
  Thiết lập người ký: tên người ký Giám đốc = "Nguyễn Văn A", cờ in tên = **Tắt**

THAO TÁC
  1. Tìm nút xóa trên dòng ô ký "Giám đốc"
  2. Thử sửa ô "Tên người ký" của dòng "Giám đốc"
  3. Bỏ tick dòng "Giám đốc" → Lưu → In
  4. Bấm nút xóa trên dòng ô ký tự do "NGƯỜI NHẬN HÀNG"

EXPECTED — bước 1
  dòng chức danh   **KHÔNG có nút xóa**
  cột chức danh    chỉ đọc (Disable, at)

EXPECTED — bước 2
  ô Tên người ký của chức danh   **chỉ đọc**, lấy từ Thiết lập người ký

EXPECTED — bước 3
  noi_dung.khoi[chuKy].oKy[Giám đốc].hienThi = **Không**, phần tử **vẫn tồn tại**
  bản in   không in ô ký Giám đốc
  các ô ký còn lại   **không in tên người ký** (cờ của Thiết lập người ký đang Tắt)

EXPECTED — bước 4
  ô ký tự do bị xóa khỏi danh sách; số ô ký giảm 1
```

### S-TLMI-047 · Một trường chỉ ở một ô trong một khối

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-149, R-TLMI-150, R-TLMI-151, R-TLMI-152, R-TLMI-153, R-TLMI-154,
            R-TLMI-155, R-TLMI-168, R-TLMI-169, INV-TLMI-007

TIỀN ĐỀ
  Khối A: lưới 2 dòng × 2 cột; ô (1,1) = trường "Số chứng từ"; các ô còn lại trống
  Khối B: lưới 1 dòng × 2 cột, cả hai ô trống
  kho trường có "Số chứng từ", "Ngày chứng từ", "Người nộp tiền"

THAO TÁC
  1. Trong Khối A: nháy đúp ô (1,2) → hộp chọn hiện; gõ "so chung tu" (không dấu)
  2. Chọn "Số chứng từ" cho ô (1,2)
  3. Trong Khối B: kéo dòng trường "Số chứng từ" thả vào ô (1,1)
  4. Kéo ô (1,2) của Khối A thả lên ô (2,1) của Khối A
  5. Chọn ô (2,1) → nhấn phím Delete
  6. Thử sửa cột "Trường dữ liệu" trong bảng chỉnh

EXPECTED — bước 1
  hộp chọn cạnh ô: hai mục đầu là **(Ô trống)** và **Chữ tự do**, rồi tới kho trường
  gõ "so chung tu" lọc ra "Số chứng từ" — **không phân biệt dấu**

EXPECTED — bước 2
  ô (1,2) mang trường "Số chứng từ"
  ô (1,1) **tự trở về Ô trống** — trường chuyển sang ô mới       ← INV-TLMI-007
  trong Khối A, COUNT(ô dùng "Số chứng từ") = 1

EXPECTED — bước 3
  **được phép** — Khối B cũng dùng "Số chứng từ"; Khối A giữ nguyên ô (1,2)
  hai khối cùng dùng một trường, ràng buộc "một ô" chỉ trong phạm vi MỘT khối

EXPECTED — bước 4
  hai ô **đổi nội dung** cho nhau: (2,1) mang trường, (1,2) thành Ô trống

EXPECTED — bước 5
  ô (2,1) về **Ô trống**; trường "Số chứng từ" không còn ô nào trong Khối A
  (Khối B vẫn giữ)

EXPECTED — bước 6
  cột "Trường dữ liệu"  **luôn chỉ đọc**
```

### S-TLMI-048 · Chưa chọn ô nào; Esc khi đang mở hộp thoại con

```
Nhóm        ngoại lệ
Tầng kiểm   FE
Luật phủ    R-TLMI-162, R-TLMI-163, R-TLMI-170, R-TLMI-171, R-TLMI-172, R-TLMI-173,
            R-TLMI-228, R-TLMI-256

TIỀN ĐỀ
  đang chọn khối **Tiêu đề** (không phải khối tự do); mẫu có thay đổi chưa lưu

THAO TÁC
  1. Quan sát thanh công cụ khối tự do và thanh Xem trước
  2. Chọn khối tự do "Thông tin chung", **chưa bấm vào ô nào**
  3. Bấm một ô là Chữ tự do → mở menu chuột phải
  4. Bấm "+ Thêm khối tự do" (hộp Đặt tên khối mở ra) → nhấn **Esc**
  5. Bấm Đóng màn (MSG_401 mở ra) → nhấn **Esc**

EXPECTED — bước 1
  thanh công cụ khối tự do   **KHÔNG hiện** (chỉ hiện khi đang chọn khối tự do)
  thanh **Xem trước**        **LUÔN hiện** ở mọi khối đang chọn

EXPECTED — bước 2
  thanh công cụ khối tự do hiện, nhưng **mọi nút đều mờ** (Disable)

EXPECTED — bước 3
  menu chuột phải có cùng tác dụng với thanh công cụ
  lệnh đầu menu = **"Sửa chữ"** (vì ô đang chọn là Chữ tự do)
  phím tắt trong lưới: mũi tên di chuyển ô · Delete xóa nội dung · Enter / F2 vào sửa

EXPECTED — bước 4 và 5
  Esc **không tác dụng với màn chính** — màn Thiết lập mẫu in KHÔNG đóng
  (hộp thoại con gồm: hộp Đặt tên khối, hộp chọn trường cạnh ô, bốn hộp xác nhận
   MSG_401…404)
```

### S-TLMI-049 · Đổi Khổ giấy trên thanh Xem trước rồi muốn hoàn lại riêng một ô

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-040, R-TLMI-042, R-TLMI-044, R-TLMI-045, R-TLMI-221, R-TLMI-228,
            INV-TLMI-003
Quyết định  **C17 chốt** — đổi Khổ/Hướng ở thanh Xem trước **LÀ đổi mẫu**, không phải đổi
            cách xem; hai ô là **một trường**, đồng bộ hai chiều tức thời (`SCR:79`)
            **C16 chốt** — giữ đúng tài liệu: nút *Theo thiết lập chung* chỉ ở **mức nhóm**,
            không nhãn từng ô, không hoàn lại riêng một ô. Ghi nhận là **rủi ro UX**, BA soát lại.

TIỀN ĐỀ
  sáu ô Giấy và chữ đều **theo chung** (`giayVaChu` = `{}`)
  người dùng đã đặt **riêng** hai ô: Lề trái = 2, Cỡ chữ = 14
  đang chọn khối **Chữ ký** (thanh Xem trước vẫn hiện — R-TLMI-228)

THAO TÁC
  1. Trên **thanh Xem trước**, đổi Khổ giấy A4 → A5
  2. Quay lại mục "Thiết lập mẫu", xem ô Khổ giấy
  3. Tìm cách đưa **riêng ô Khổ giấy** về theo chung
  4. Bấm nút "Theo thiết lập chung" của nhóm Giấy và chữ
  5. Bấm Thu / Phóng / Vừa khung trên thanh Xem trước → Lưu → In

EXPECTED — bước 1 và 2
  ô Khổ giấy ở mục Thiết lập mẫu **đổi theo NGAY** = A5 — **một trường, hai chỗ hiển thị**,
    đồng bộ **hai chiều**: sửa ở mục Thiết lập mẫu thì thanh Xem trước cũng đổi tức thời
  ô Khổ giấy trở thành **riêng** ⇒ khi Lưu, `giayVaChu.khoGiay = 'A5'` (khóa có mặt)
  **KHÔNG có nhãn** nào cho biết ô đang riêng hay theo chung; Show/Hide không đổi
  đây là **một bước Hoàn tác được** (mọi thao tác đổi mẫu đều là một bước — R-TLMI-224)

EXPECTED — bước 3
  **KHÔNG có cách nào** — phải bấm nút cho **cả nhóm** rồi gõ lại các ô còn lại

EXPECTED — bước 4
  **cả sáu ô** về theo chung ⇒ sáu khóa **bị xóa khỏi** `giayVaChu`, **mất luôn**
  Lề trái = 2, Cỡ chữ = 14 và Khổ giấy A5 vừa đặt ở bước 1
  thao tác này là **một bước Hoàn tác được** ⇒ bấm Ctrl+Z lấy lại cả ba   ← R-TLMI-041

EXPECTED — bước 5
  Thu / Phóng / Vừa khung chỉ đổi tỷ lệ nhìn, **không ảnh hưởng bản in**
  bản in vẫn theo Giấy và chữ đã lưu

EXPECTED — điều **cấm** làm (hệ quả của C16, C17)
  KHÔNG tự thêm nhãn "theo chung / riêng" cho từng ô
  KHÔNG tự thêm nút hoàn lại riêng một ô
  KHÔNG biến thanh Xem trước thành "chỉ để xem"
  Ba việc trên đều là **tự đặt luật ngoài đặc tả**. Hai rủi ro UX đã ghi vào `04` §7 mục 2
  để BA xác nhận là chủ ý hay sót đặc tả; **trước khi BA trả lời thì code đúng tài liệu**.
```

### S-TLMI-060 · Thiết lập chung bật Cộng gộp mặt hàng khi in

```
Nhóm        ngoại lệ
Tầng kiểm   BE
Luật phủ    R-TLMI-096, R-TLMI-097, R-TLMI-119, R-TLMI-262, R-TLMI-266
Quyết định  **C01 chốt** — khóa cộng gộp = **mã hàng + đơn vị tính + đơn giá + THUẾ SUẤT**
            (+ **số lô, hạn sử dụng** nếu vật tư theo dõi theo lô). Hai dòng khác thuế suất
            **KHÔNG gộp**. Theo `SCR_CauHinhBaoCaoChungTu.md:160-162` — nguồn chi tiết hơn,
            có ví dụ phủ định rõ; BR51.5 chỉ liệt kê thiếu, không phủ định.
            **C30 chốt** — phạm vi cộng gộp **giữ giới hạn BR51.5**: chỉ **Hóa đơn, phiếu
            xuất kho, phiếu nhập kho**.

TIỀN ĐỀ
  thiết lập chung: "Cộng gộp mặt hàng khi in" = **Bật**
  ca A — chứng từ là **Hóa đơn** (thuộc diện cộng gộp), lưới hàng hóa 4 dòng:
    D1  mã H01 · ĐVT "cái" · đơn giá 100.000 · **thuế suất 8%**  · SL 10
    D2  mã H01 · ĐVT "cái" · đơn giá 100.000 · **thuế suất 10%** · SL 5
    D3  mã H01 · ĐVT "cái" · đơn giá 100.000 · **thuế suất 8%**  · SL 3
    D4  mã H02 · ĐVT "hộp" · đơn giá  50.000 · thuế suất 8%      · SL 2
  ca B — chứng từ là **Phiếu chi** (KHÔNG thuộc diện cộng gộp), cùng 4 dòng như trên
  ca C — vật tư **theo dõi theo lô**: hai dòng giống hệt ca A/D1 nhưng **khác số lô**
  khối Bảng: In cột STT = Có · Dòng Cộng = Có; cột Thành tiền và Tiền thuế đều tick Cộng

THAO TÁC
  1. In Mẫu tùy chỉnh cho ca A
  2. In Mẫu tùy chỉnh cho ca B
  3. In Mẫu tùy chỉnh cho ca C
  4. Tắt "Cộng gộp mặt hàng khi in" ở thiết lập chung → in lại ca A

EXPECTED — bước 1 (ca A: Hóa đơn, có gộp)
  khóa gộp áp **TRƯỚC** khi dựng bảng                              ← R-TLMI-119
  D1 và D3 **GỘP** (cùng H01 · cái · 100.000 · **cùng 8%**)
  D2 **KHÔNG gộp** với D1/D3 — **khác thuế suất 10% vs 8%**
  bản in có **3 dòng**:
    STT 1  H01 · cái · 100.000 · 8%  · SL **13**  (= 10 + 3)
    STT 2  H01 · cái · 100.000 · 10% · SL 5
    STT 3  H02 · hộp ·  50.000 · 8%  · SL 2
  cột STT   đánh lại **1, 2, 3** trên các dòng **sau khi gộp**
  dòng cuối "Tổng:" cộng Thành tiền và Tiền thuế trên **3 dòng** đã gộp   ← R-TLMI-097

EXPECTED — bước 2 (ca B: Phiếu chi, KHÔNG gộp)
  bản in giữ nguyên **4 dòng** — cộng gộp **không áp** cho Phiếu chi     ← C30
  (điều kiện áp = thiết lập chung bật **VÀ** loại chứng từ ∈ {Hóa đơn, phiếu xuất kho,
   phiếu nhập kho})

EXPECTED — bước 3 (ca C: vật tư theo lô)
  hai dòng cùng mã / ĐVT / đơn giá / thuế suất nhưng **khác số lô** ⇒ **KHÔNG gộp**
  bản in giữ **2 dòng** riêng
  (khóa gộp cộng thêm **số lô** và **hạn sử dụng** khi vật tư theo dõi theo lô)

EXPECTED — bước 4 (tắt cộng gộp)
  bản in ca A quay lại **4 dòng**, đúng thứ tự dòng trên chứng từ

EXPECTED — hai quy tắc còn lại của R-TLMI-266
  (a) "cho phép in chứng từ chưa ghi sổ" và (b) "cho phép in chứng từ đã khóa sổ"
  áp ở bước 2 của UC02 — xem S-TLMI-044
```

---

## §4. Nhóm `rollback`

### S-TLMI-050 · Đóng khi chưa lưu → nhánh *Lưu và đóng*

```
Nhóm        rollback
Tầng kiểm   FE (+ BE ở bước Lưu)
Luật phủ    R-TLMI-029, R-TLMI-243, R-TLMI-248, R-TLMI-251, R-TLMI-252, INV-TLMI-012
Quyết định  **C23 chốt** — *Lưu và đóng* **CÓ** hiện toast `MSG_…_101` rồi mới đóng màn;
            toast sống độc lập với màn (BR26.1, góc phải trên)

TIỀN ĐỀ
  mẫu đã lưu M0; người dùng đổi Cỡ chữ tiêu đề 18 → 22 ⇒ badge "Chưa lưu"
  vào màn từ **form sửa chứng từ**

THAO TÁC — ca 1 (mẫu hợp lệ)
  1. Bấm Đóng
  2. Chọn nút **Lưu và đóng**

THAO TÁC — ca 2 (mẫu đang Có lỗi)
  3. Mở lại màn, đổi Cỡ chữ tiêu đề = 9 ⇒ badge "Có lỗi"
  4. Nhấn **Esc** → chọn **Lưu và đóng**

EXPECTED — bước 1
  hộp xác nhận  MSG_PMKT-E-14549_21_401 — "Mẫu đã có thay đổi chưa lưu. Bạn muốn làm gì?"
  ba nút        **Lưu và đóng** · **Không lưu** · **Ở lại**

EXPECTED — bước 2 (ca 1), theo đúng thứ tự
  1. chạy đủ bước Lưu: kiểm tra → transaction → commit
  2. `noi_dung.khoi[tieuDe].coChu` = 22 trong DB; `phien_ban` tăng 1
  3. hiện toast **MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"**   ← C23
  4. **rồi** mới đóng màn — **thành công MỚI đóng**
  toast vẫn hiển thị sau khi màn đã đóng (sống độc lập với màn, góc phải trên)
  đóng xong quay lại **đúng form sửa chứng từ** (nơi vừa mở ra)
  lịch sử Hoàn tác / Làm lại bị xóa

EXPECTED — bước 4 (ca 2)
  Lưu **thất bại** ở bước kiểm tra
  thông báo   MSG_PMKT-E-14549_21_202 — "Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36"
  màn         **Ở LẠI**, không đóng; badge vẫn "Có lỗi"
  DB          0 bản ghi bị đổi                                   ← INV-TLMI-012
  **KHÔNG** hiện toast `_101` (chưa commit thì chưa có gì để báo thành công)
  (gặp lỗi hệ thống thay vì lỗi validate ⇒ MSG_PMKT-E-14549_21_003 và cũng ở lại)
  (lệch `phienBan` ⇒ MSG_COMMON_001 và cũng ở lại — xem S-TLMI-078)
```

### S-TLMI-051 · Đóng khi chưa lưu → nhánh *Không lưu*

```
Nhóm        rollback
Tầng kiểm   FE
Luật phủ    R-TLMI-225, R-TLMI-251, R-TLMI-253, INV-TLMI-012

TIỀN ĐỀ
  mẫu đã lưu M0 (Tiêu đề cỡ 18, 1 khối tự do "Thông tin chung")
  người dùng đã làm: đổi cỡ chữ 18 → 22 · thêm khối tự do "Ghi chú" · bỏ tick cột C2
  ⇒ badge "Chưa lưu", lịch sử Hoàn tác có 3 bước

THAO TÁC
  1. Bấm Đóng
  2. Chọn nút **Không lưu**
  3. Mở lại màn

EXPECTED — bước 1
  MSG_PMKT-E-14549_21_401 với ba nút

EXPECTED — bước 2
  **bỏ mọi thay đổi** và đóng màn ngay, không gọi API lưu
  DB   `prn_mau_in_tuy_chinh` **đúng bằng M0**, `phien_ban` không tăng   ← INV-TLMI-012
  lịch sử Hoàn tác / Làm lại   **bị xóa**

EXPECTED — bước 3
  mẫu mở ra    Tiêu đề cỡ **18**, 1 khối tự do "Thông tin chung", cột C2 vẫn tick
  badge        "Đã lưu";  nút Lưu Disable
  nút Hoàn tác và Làm lại   đều Disable (lịch sử rỗng)
```

### S-TLMI-052 · Đóng khi chưa lưu → nhánh *Ở lại*

```
Nhóm        rollback
Tầng kiểm   FE
Luật phủ    R-TLMI-251, R-TLMI-254

TIỀN ĐỀ
  như S-TLMI-051 (3 thay đổi chưa lưu, badge "Chưa lưu", lịch sử 3 bước)

THAO TÁC
  1. Bấm Đóng → chọn nút **Ở lại**

EXPECTED
  màn                **giữ nguyên**, không đóng
  mọi thay đổi        còn nguyên: cỡ chữ 22 · khối "Ghi chú" · C2 bỏ tick
  badge               vẫn "Chưa lưu"
  lịch sử Hoàn tác    vẫn 3 bước, nút ↶ Enable
  DB                  vẫn bằng M0 (chưa gọi API nào)
```

### S-TLMI-053 · Không có thay đổi mà bấm Đóng — đóng ngay, không hỏi

```
Nhóm        rollback
Tầng kiểm   FE
Luật phủ    R-TLMI-029, R-TLMI-240, R-TLMI-255, R-TLMI-257

TIỀN ĐỀ
  ca 1: mẫu đã lưu, vừa mở màn, **chưa sửa gì**  ⇒ badge "Đã lưu"
  ca 2: chưa có bản ghi mẫu, vừa mở màn, chưa sửa gì ⇒ badge "Đã lưu" (bằng mẫu chuẩn)
  vào màn từ **màn xem trước bản in**

THAO TÁC
  1. Quan sát chân màn
  2. Bấm Đóng (ca 1)
  3. Nhấn Esc (ca 2)

EXPECTED — bước 1
  chân màn   **Đóng** ở góc trái · **Đặt lại mẫu chuẩn** và **Lưu** ở góc phải
  nút Lưu    **Disable** (badge "Đã lưu")
  nút Đặt lại mẫu chuẩn và Đóng   luôn Show ở mọi khối đang chọn

EXPECTED — bước 2 và 3
  **đóng ngay**, KHÔNG hiện MSG_PMKT-E-14549_21_401
  quay lại **đúng màn xem trước bản in** (nơi vừa mở ra)
  DB không đổi
```

### S-TLMI-054 · Đặt lại mẫu chuẩn rồi **không** Lưu, Đóng › *Không lưu*

```
Nhóm        rollback
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-015, R-TLMI-016, R-TLMI-017, R-TLMI-018, R-TLMI-019, R-TLMI-020,
            R-TLMI-064, R-TLMI-253, INV-TLMI-003, INV-TLMI-008, INV-TLMI-012

TIỀN ĐỀ — mẫu đã lưu M0, tùy chỉnh khá nhiều:
  KhoGiay='A5' · FontChu='Arial' · CoChu=14 · MauChu='#C00000' · KieuHinhNen='KHUNG_VIEN'
  3 khối tự do · khối Bảng bỏ tick 2 cột, cột đã đổi thứ tự
  khối Chữ ký: 6 ô ký (thêm 1 ô ký tự do), Thủ kho bật
  thứ tự khối: đầu trang → tự do 1 → Tiêu đề → Bảng → tự do 2 → tự do 3 → Chữ ký
  bảy ô tick đầu trang: 3 ô đã sửa riêng

THAO TÁC
  1. Bấm **Đặt lại mẫu chuẩn** → chọn **Hủy**
  2. Bấm **Đặt lại mẫu chuẩn** → chọn **Đồng ý**
  3. Kiểm tra DB (chưa bấm Lưu)
  4. Bấm Đóng → chọn **Không lưu**
  5. Mở lại màn

EXPECTED — bước 1
  hộp xác nhận  MSG_PMKT-E-14549_21_402 — "Mọi tùy chỉnh (kể cả khối tự do, thứ tự khối,
                cột bảng, chữ ký) sẽ trở về mẫu chuẩn hệ thống. Thay đổi chỉ có hiệu lực
                khi bạn bấm Lưu. Tiếp tục?"
  chọn Hủy      **giữ nguyên mẫu đang chỉnh trên màn**, không đổi gì, badge không đổi

EXPECTED — bước 2 (trên màn, chưa chạm DB)
  thông báo     MSG_PMKT-E-14549_21_102 — "Đã đưa về mẫu chuẩn hệ thống. Bấm Lưu để có hiệu lực"
  badge         **"Chưa lưu"**
  Bố cục mẫu    Thông tin đầu trang → Tiêu đề → Bảng Hàng hóa, dịch vụ → Chữ ký
                (**BỎ cả 3 khối tự do**, thứ tự về chuẩn)        ← INV-TLMI-008
  Giấy và chữ   **cả sáu ô về THEO CHUNG** ⇒ hiển thị A4 · Dọc · 1/1,5/1/1 · Times New Roman · 12
  bảy ô tick đầu trang   **về THEO CHUNG**
  Màu chữ       **#000000** (đen)
  Kiểu hình nền **Không**  (Độ đậm, Căn ảnh, Ảnh trở lại Hide)
  khối Bảng     đủ cột gốc, mọi cột tick in, thứ tự cột theo lưới form
  khối Chữ ký   5 ô ký chuẩn, thứ tự Người lập phiếu · Kế toán trưởng · Giám đốc · Thủ kho
                · Thủ quỹ; tick Có/Có/Có/Không/Không; **ô ký tự do bị bỏ**

EXPECTED — bước 3
  DB **KHÔNG ĐỔI** — `prn_mau_in_tuy_chinh.noi_dung` vẫn đúng bằng M0   ← R-TLMI-018

EXPECTED — bước 4
  đóng màn, không gọi API lưu

EXPECTED — bước 5
  mẫu mở ra   **đúng bằng M0** — A5 · Arial · 14 · #C00000 · khung viền · 3 khối tự do
              · 6 ô ký · thứ tự khối đã tùy chỉnh
  **không bản ghi nào bị xóa**                                   ← R-TLMI-019, INV-TLMI-012
  badge "Đã lưu"
```

### S-TLMI-055 · Mẫu bằng mẫu chuẩn rồi Lưu — ba ca, cùng một kết quả

```
Nhóm        rollback
Tầng kiểm   BE
Luật phủ    R-TLMI-006, R-TLMI-007, R-TLMI-021, R-TLMI-022, R-TLMI-247, INV-TLMI-002
Quyết định  **C02 chốt — SO SÁNH NỘI DUNG.** Khi Lưu, BE **chuẩn hóa** JSON mẫu trên payload
            rồi so với JSON **mẫu chuẩn hệ thống** sinh từ đặc tả form:
              · bằng nhau  ⇒ **XÓA bản ghi** (chưa có thì **KHÔNG tạo**)
              · khác nhau  ⇒ ghi/cập nhật bản ghi
            **Chuẩn hóa** = sắp khóa theo thứ tự cố định · bỏ mọi khóa có giá trị `null`
            · bỏ id kỹ thuật. Điều kiện KHÔNG phụ thuộc thao tác nào dẫn tới trạng thái đó.

TIỀN ĐỀ — ba ca phải cho CÙNG một kết quả:
  ca 1  mẫu M0 đã tùy chỉnh (như S-TLMI-054) → bấm **Đặt lại mẫu chuẩn** → **Lưu**
  ca 2  mẫu M0 đã tùy chỉnh → **chỉnh tay** từng thứ về đúng mẫu chuẩn
        (hoặc bấm Hoàn tác cho tới khi về mẫu chuẩn) → **Lưu**
  ca 3  **chưa có bản ghi**, vừa mở màn, **không sửa gì** → **Lưu**

THAO TÁC
  1. Thực hiện từng ca, rồi đọc lại `prn_mau_in_tuy_chinh`
  2. Ngay sau đó gọi API in "Mẫu tùy chỉnh"

EXPECTED — cả BA ca đều như nhau
  ca 1  prn_mau_in_tuy_chinh WHERE (T1, CTMDV, MUA_DV_TRONG_NUOC)   **0 bản ghi** (đã xóa)
  ca 2  **0 bản ghi** — chỉnh tay về đúng mẫu chuẩn cũng bị xóa, **bất kể** đến từ thao tác nào
  ca 3  **0 bản ghi** — KHÔNG tạo bản ghi rác khi mở ra Lưu ngay mà không sửa gì
  ảnh nền           cột `anh_nen` / `anh_nen_kieu_tep` / `anh_nen_ten_tep` cũng bị xóa cùng
                    bản ghi (mẫu chuẩn có `nen.kieu = 'KHONG'`)
  toast             MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"  (xóa cũng là Lưu thành công)
  nhãn trạng thái   "Đã lưu";  nút Lưu Disable
  transaction       một transaction cho cả so sánh + xóa                ← R-TLMI-247
  bất biến          nghiệp vụ dùng mẫu chuẩn ⟺ KHÔNG tồn tại bản ghi — **cả hai chiều**
                    nay đều kiểm được                                   ← INV-TLMI-002

EXPECTED — bước 2 (in ngay sau đó, cả ba ca)
  bản in    dựng theo **mẫu chuẩn hệ thống**
  thông báo MSG_PMKT-E-14549_21_103 — "Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này,
            đang in theo mẫu chuẩn hệ thống"
  có hiệu lực **ngay** cho MỌI chứng từ cùng nghiệp vụ của cả đơn vị    ← R-TLMI-022

EXPECTED — ca đối chứng (phải KHÁC ba ca trên)
  mẫu chỉ khác mẫu chuẩn **một chi tiết nhỏ nhất** — ví dụ Cỡ chữ tiêu đề 18 → 19 — rồi Lưu
  ⇒ **1 bản ghi** được tạo/giữ; `noi_dung.khoi[tieuDe].coChu = 19`
  ⇒ in ra **KHÔNG** có MSG_…_103

  Chi tiết phép so sánh xem S-TLMI-077 (chuẩn hóa JSON).
```

### S-TLMI-056 · Hoàn tác / Làm lại một chuỗi thao tác rồi đóng màn

```
Nhóm        rollback
Tầng kiểm   FE
Luật phủ    R-TLMI-041, R-TLMI-218, R-TLMI-222, R-TLMI-223, R-TLMI-224, R-TLMI-225,
            R-TLMI-226, R-TLMI-227, R-TLMI-229

TIỀN ĐỀ
  mẫu đã lưu M0: Cỡ chữ tiêu đề 18 · khối tự do "Thông tin chung" lưới 1×2, hai ô trống
  · Lề trái = 2 (riêng), Cỡ chữ chung = 14 (riêng)
  ô tick "Hiện lưới căn chỉnh" đang bật

THAO TÁC — 5 bước, mỗi bước là 1 bước Hoàn tác
  1. Đổi Cỡ chữ tiêu đề 18 → 22, rời ô
  2. Bấm "+ Dòng dưới" ở khối tự do (lưới thành 2×2)
  3. Nháy đúp ô (1,1) → Chữ tự do → gõ "Kính gửi" → rời ô  (gõ chữ = 1 bước khi rời ô)
  4. Chọn vùng (1,1)-(1,2) → Gộp ô
  5. Bấm nút "Theo thiết lập chung" của nhóm Giấy và chữ
  6. Bấm Hoàn tác 5 lần, quan sát từng lần
  7. Bấm Làm lại 2 lần
  8. Bỏ tick "Hiện lưới căn chỉnh" → Lưu → mở lại màn
  9. Bấm Đóng → *Không lưu* → mở lại màn

EXPECTED — bước 6 (lùi từng bước, trang xem trước vẽ lại ngay mỗi lần)
  lần 1  Lề trái về **2**, Cỡ chữ chung về **14** (hoàn tác nút Theo thiết lập chung)
  lần 2  ô (1,1) và (1,2) **tách trở lại**
  lần 3  ô (1,1) về **Ô trống** (mất chữ "Kính gửi")
  lần 4  lưới về **1 dòng × 2 cột**
  lần 5  Cỡ chữ tiêu đề về **18**
  sau lần 5   nút ↶ **Disable**; nút ↷ Enable; mẫu đúng bằng M0; badge "Đã lưu"

EXPECTED — bước 7
  tiến lại 2 bước: Cỡ chữ 22 và lưới 2×2; badge "Chưa lưu"

EXPECTED — bước 8
  "Hiện lưới căn chỉnh" **KHÔNG được lưu** — mở lại màn thì ô tick trở về **mặc định Có**
  các đường phân ô chỉ hiện trên màn, không có trên bản in / PDF

EXPECTED — bước 9
  mở lại màn: nút ↶ và ↷ **đều Disable** — lịch sử Hoàn tác / Làm lại đã bị xóa khi đóng màn

  ⚠ **Đặt lại mẫu chuẩn** có phải một bước Hoàn tác được không: tài liệu im lặng (Z-17)
     ⇒ không đưa vào chuỗi trên; xem §B.
```

---

## §5. Nhóm `tương tranh`

### S-TLMI-057 · Hai người cùng mở một mẫu và cùng bấm Lưu

```
Nhóm        tương tranh
Tầng kiểm   BE
Luật phủ    R-TLMI-005, R-TLMI-247, R-TLMI-258, INV-TLMI-012
Quyết định  **C06 chốt — KHÓA LẠC QUAN.** Payload Lưu mang `phienBan`; BE so với cột
            `phien_ban` của bản ghi. Lệch ⇒ **KHÔNG ghi**, trả **`MSG_COMMON_001`**, màn
            hỏi người dùng nạp lại. Mã `MSG_` riêng của epic **chưa có** ⇒ dùng mã chung
            (`04` §5 L-4); câu hướng dẫn "nạp lại" có **key i18n riêng**.

TIỀN ĐỀ
  mẫu (T1, CTMDV, MUA_DV_TRONG_NUOC) đã lưu, gọi là M0:
    Tiêu đề "CHỨNG TỪ MUA DỊCH VỤ" cỡ 18 · khối Bảng 3 cột · 1 khối tự do "Thông tin chung"
  u1 (ở CN-A) và u4 (ở CN-B) **cùng có quyền** Thiết lập mẫu in
  cả hai cùng mở màn Thiết lập mẫu in của **cùng một** mẫu, cùng đọc được M0
  cả hai cùng nhận `phienBan = 7` khi mở màn

THAO TÁC
  1. u1 đổi Cỡ chữ tiêu đề 18 → 22, thêm khối tự do "Ghi chú"
  2. u4 đổi Màu chữ → #C00000, bỏ tick cột C2 của khối Bảng
  3. u1 bấm **Lưu** (payload mang `phienBan = 7`)
  4. u4 bấm **Lưu** (payload **vẫn** mang `phienBan = 7` — u4 chưa nạp lại)
  5. u4 chọn nạp lại màn, sửa lại Màu chữ → #C00000, bấm Lưu

EXPECTED — bước 3 (u1 thắng, đến trước)
  `phien_ban` khớp ⇒ ghi thành công; `phien_ban` **tăng 7 → 8**
  toast MSG_PMKT-E-14549_21_101 — "Lưu mẫu in thành công!"
  DB: `noi_dung.khoi[tieuDe].coChu` = 22 · 2 khối tự do
  u1 badge "Đã lưu"

EXPECTED — bước 4 (u4 bị chặn)
  `phienBan` payload = 7  ≠  `phien_ban` DB = 8  ⇒ **KHÔNG ghi một bit nào**
  HTTP         409 (hoặc mã tương ứng của tầng `ApiResponse`)
  thông báo    **`MSG_COMMON_001`** — "Thao tác không hợp lệ với trạng thái hiện tại của
               chứng từ/phiếu."
  kèm hướng dẫn nạp lại (key i18n riêng của module, **không** phải mã `MSG_` của BA)
  DB           vẫn đúng bản của u1: Cỡ chữ 22 · 2 khối tự do · Màu chữ **KHÔNG** đổi
               · cột C2 **vẫn tick**;  `phien_ban` vẫn 8               ← INV-TLMI-012
  màn của u4   **giữ nguyên**, không đóng, không mất phần đang chỉnh; badge vẫn "Chưa lưu"
  **KHÔNG** có ghi đè âm thầm — công của u1 nguyên vẹn

EXPECTED — bước 5 (u4 nạp lại rồi Lưu)
  màn u4 nạp lại mẫu hiện tại: Cỡ chữ 22 · 2 khối tự do · `phienBan = 8`
  Lưu thành công; `phien_ban` **tăng 8 → 9**
  DB: Cỡ chữ 22 · 2 khối tự do · Màu chữ #C00000 · C2 bỏ tick — **giữ được cả hai người**
  toast MSG_PMKT-E-14549_21_101

  Ghi chú: mẫu dùng chung toàn tenant ⇒ u1 và u4 luôn thao tác trên **đúng một** bản ghi
  (R-TLMI-005), nên xung đột này là tình huống thật, không phải giả định.
  **Đã ghi vào `04` §7 mục 1**: đề nghị BA cấp mã `MSG_` riêng cho xung đột phiên bản.
```

### S-TLMI-058 · Hai request Lưu song song cùng khóa duy nhất

```
Nhóm        tương tranh
Tầng kiểm   BE
Luật phủ    R-TLMI-001, R-TLMI-004, R-TLMI-005, R-TLMI-247, INV-TLMI-001, INV-TLMI-011

TIỀN ĐỀ
  (T1, CTMDV, MUA_DV_TRONG_NUOC)   **0 bản ghi**
  hai request POST lưu mẫu **song song**, cùng tenant T1, cùng MaChucNang CTMDV,
  cùng MaNghiepVu MUA_DV_TRONG_NUOC; request R1 gửi Cỡ chữ tiêu đề 20, R2 gửi 24
  R1 đến từ người dùng ở CN-A, R2 từ người dùng ở CN-B

THAO TÁC
  1. Bắn R1 và R2 đồng thời
  2. Đọc lại `prn_mau_in_tuy_chinh` theo khóa (T1, CTMDV, MUA_DV_TRONG_NUOC)

EXPECTED
  COUNT(prn_mau_in_tuy_chinh WHERE tenant_id=T1 AND ma_loai_chung_tu=CTMDV
        AND ma_nghiep_vu=MUA_DV_TRONG_NUOC) = **1**              ← INV-TLMI-001
  **KHÔNG** sinh 2 bản ghi, kể cả ở khoảnh khắc giữa hai transaction
  chốt chặn cuối = **unique index mới** trên (tenant_id, ma_loai_chung_tu, ma_nghiep_vu)
    ⚠ index cũ của `V1148` chỉ có (tenant_id, ma_loai_chung_tu) ⇒ **migration mới bắt buộc**,
      không sửa `V1148` (đã lên origin/develop + origin/staging)      ← Q-01
  bản ghi duy nhất **không mang cột chi nhánh** trong khóa            ← INV-TLMI-011
  mỗi transaction all-or-nothing                                     ← R-TLMI-247

  Đối chứng: gọi Lưu **hai lần liên tiếp** (không song song) cùng khóa ⇒ vẫn đúng 1 bản ghi.

  Giá trị cuối cùng là 20 hay 24: cả hai request cùng gửi `phienBan` của bản **chưa tồn tại**
  ⇒ đúng một request thắng ở bước INSERT, request còn lại nhận `MSG_COMMON_001` — xem
  S-TLMI-057 và S-TLMI-078. Bất biến INV-TLMI-001 kiểm được **độc lập** với hướng khóa.
```

---

## §6. Đợt bổ sung sau khi `04-quyet-dinh-ban-giao.md` đóng 32 mục mâu thuẫn

> 18 kịch bản dưới đây phủ các mục §B của bản trước nay đã hết bị chặn. Mỗi kịch bản ghi rõ mục
> `C<nn>` là nguồn của kết cục — **không đến từ tài liệu BA**, nên BA soát lại thì sửa `04` trước.

### S-TLMI-061 · Bỏ tick **Logo** trong bảy ô tick đầu trang

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-043, R-TLMI-049, R-TLMI-077, R-TLMI-082, R-TLMI-083, INV-TLMI-003
Quyết định  **C03 chốt** — Logo **CÓ** nằm trong bảy ô tick mà mẫu sửa riêng được. Đủ bảy:
            Tên đơn vị · Địa chỉ · Mã số thuế · Số điện thoại · Email · Tài khoản ngân hàng
            · **Logo**. Ba nguồn đồng thuận (`SCR:125` · `MT:77` · Figma frame 4).

TIỀN ĐỀ
  bảy ô tick đầu trang đều **theo chung**; thiết lập chung bật cả bảy
  hồ sơ CN-B có logo (`Q-03` — trường Logo đơn vị do tầng "thiết lập chung tối thiểu" cấp)
  mẫu CTMDV đã lưu

THAO TÁC
  1. Bảng chỉnh khối Thông tin đầu trang → **bỏ tick riêng ô "Logo"**, giữ nguyên sáu ô kia
  2. Lưu → In
  3. Bấm nút "Theo thiết lập chung" của khối Thông tin đầu trang

EXPECTED — bước 1
  ô tick "Logo" hiện ra như **một trong bảy dòng**, sửa được (không phải chỉ đọc)
  sáu ô còn lại KHÔNG đổi trạng thái — vẫn theo chung

EXPECTED — bước 2
  noi_dung.khoi[dauTrang].inLogo = **Không**   ← khóa CÓ MẶT ⇒ ô riêng
  sáu khóa tick còn lại **vẫn vắng mặt** ⇒ vẫn theo chung        ← INV-TLMI-003
  bản in   **KHÔNG in logo**; sáu dòng chữ còn lại in đủ, đúng thứ tự cố định
  các dòng chữ **dồn lên**, không chừa khoảng trống chỗ logo

EXPECTED — bước 3
  cả bảy khóa (gồm `inLogo`) **bị xóa khỏi JSON** ⇒ về theo chung
  bản in có logo trở lại
```

### S-TLMI-062 · Sửa *Tiêu đề in ra* của ô ký **chức danh**

```
Nhóm        happy
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-046, R-TLMI-186, R-TLMI-188, R-TLMI-196, INV-TLMI-010
Quyết định  **C04 chốt** — *Tiêu đề in ra* của ô ký chức danh **mẫu sửa riêng được**
            (`SCR:295` + `MT:89` + Figma frame 6 thắng `SCR:257`). **Tên người ký** và cờ
            *In tên người ký trên chứng từ, báo cáo* thì **LUÔN** theo thiết lập chung.

TIỀN ĐỀ
  Thiết lập người ký: Giám đốc → tiêu đề "GIÁM ĐỐC", tên "Nguyễn Văn A", cờ in tên = **Bật**
  mẫu CTMDV chưa sửa gì ở khối Chữ ký

THAO TÁC
  1. Bảng chỉnh khối Chữ ký → dòng "Giám đốc" → ô *Tiêu đề in ra*: sửa "GIÁM ĐỐC"
     → "TỔNG GIÁM ĐỐC", rời ô
  2. Thử sửa ô *Tên người ký* và ô *In tên người ký* của dòng đó
  3. Lưu → In
  4. Quản trị đổi Thiết lập người ký: tiêu đề Giám đốc → "GIÁM ĐỐC ĐIỀU HÀNH",
     tên → "Lê Văn C", cờ in tên → **Tắt**
  5. In lại

EXPECTED — bước 1
  ô *Tiêu đề in ra* là **TextField sửa được** (Show, không Disable)
  ràng buộc: không trống, tối đa 60 ký tự; vi phạm ⇒ MSG_PMKT-E-14549_21_211

EXPECTED — bước 2
  ô *Tên người ký*        **chỉ đọc**, không có nút xóa    ← R-TLMI-186
  cờ *In tên người ký*    **chỉ đọc** ở màn này            ← R-TLMI-196

EXPECTED — bước 3
  noi_dung.khoi[chuKy].oKy[giamDoc].tieuDe = 'TỔNG GIÁM ĐỐC'   ← khóa CÓ MẶT ⇒ riêng
  **KHÔNG** lưu tenNguoiKy và cờ in tên vào mẫu (luôn theo chung ⇒ khóa vắng mặt)
  bản in   ô ký Giám đốc in tiêu đề "TỔNG GIÁM ĐỐC", tên "Nguyễn Văn A"

EXPECTED — bước 5 (sau khi thiết lập chung đổi)
  tiêu đề in ra   **vẫn "TỔNG GIÁM ĐỐC"** — ô riêng, không đổi theo
  tên người ký    **KHÔNG in** — cờ in tên đã Tắt ở thiết lập chung, mẫu không ghi đè được
  các ô ký **chưa sửa tiêu đề** (Kế toán trưởng…) thì tiêu đề **đổi theo** thiết lập chung
```

### S-TLMI-063 · In lại chứng từ cũ khi đang làm việc ở chi nhánh khác

```
Nhóm        happy
Tầng kiểm   BE
Luật phủ    R-TLMI-078, R-TLMI-081, R-TLMI-199, R-TLMI-267
Quyết định  **C05 chốt** — khối **Chữ ký** đọc hồ sơ đơn vị của **chi nhánh ghi trên chứng
            từ**, giống khối đầu trang (BR50.7). Lý do: in lại một chứng từ cũ ở chi nhánh
            khác phải ra **cùng một bản in**. Cả hai khối đi qua **một cổng duy nhất**
            `HoSoDonViPort.theoChiNhanh(chiNhanhId)` (**Q-14**).

TIỀN ĐỀ
  CT-2026-000123 ghi chi nhánh **CN-B**
  hồ sơ CN-B: tên "Chi nhánh Hà Nội" · địa chỉ "12 Láng Hạ" · Giám đốc "Nguyễn Văn A"
  hồ sơ CN-C: tên "Chi nhánh Đà Nẵng" · địa chỉ "5 Bạch Đằng" · Giám đốc "Phạm Thị D"
  người dùng u5 đang làm việc ở **CN-C**, có quyền In

THAO TÁC
  1. u5 mở CT-2026-000123 → In → "Mẫu tùy chỉnh"
  2. So bản in này với bản in cùng chứng từ do người ở CN-B in ra trước đó

EXPECTED — bước 1
  khối Thông tin đầu trang   "Chi nhánh Hà Nội" · "12 Láng Hạ"       ← hồ sơ **CN-B**
  khối Chữ ký                tên người ký Giám đốc = "Nguyễn Văn A"  ← hồ sơ **CN-B**
  **KHÔNG** lấy bất cứ thứ gì của CN-C (chi nhánh đang làm việc)
  cả hai khối gọi cùng một cổng `HoSoDonViPort.theoChiNhanh('CN-B')`

EXPECTED — bước 2
  hai bản in **giống hệt nhau** từng chi tiết — in lại ở chi nhánh khác không đổi nội dung

EXPECTED — trạng thái hiện tại của repo (L-7)
  `cfg_chi_nhanh` chưa tồn tại ⇒ bản hiện thực của cổng **bỏ qua tham số** và trả hồ sơ của
  **tenant**. Test hiện tại chốt **hợp đồng của cổng**: khối đầu trang và khối Chữ ký phải
  **cùng gọi cổng với `chiNhanhId` của chứng từ**, không được đọc thẳng cấu hình tenant.
  Khi `cfg_chi_nhanh` ra đời, **chỉ đổi phần hiện thực của cổng** — kịch bản này không sửa.
```

### S-TLMI-064 · Sửa tên khối tự do ở **cả hai chỗ**

```
Nhóm        happy
Tầng kiểm   FE
Luật phủ    R-TLMI-120, R-TLMI-121, R-TLMI-127, R-TLMI-212, R-TLMI-239 (V06)
Quyết định  **C07 chốt** — sửa tên khối tự do ở **cả hai chỗ**: hộp *Đặt tên khối* khi thêm
            mới (`SCR:284`) **và** ô *Tên khối* trên bảng chỉnh (Figma frame 3). Hai chỗ
            cùng ghi **một trường**.

TIỀN ĐỀ
  mẫu có 0 khối tự do

THAO TÁC
  1. + Thêm khối tự do → hộp Đặt tên khối → gõ "Thông tin chung" → Thêm
  2. Bảng chỉnh của khối vừa tạo → ô *Tên khối*: sửa thành "Thông tin người mua" → rời ô
  3. Ô *Tên khối*: xóa trắng → rời ô
  4. Ô *Tên khối*: gõ 61 ký tự → rời ô
  5. Sửa lại "Thông tin người mua" → Lưu → In

EXPECTED — bước 1
  khối tạo với tenKhoi = 'Thông tin chung'; MSG_PMKT-E-14549_21_104

EXPECTED — bước 2
  dòng khối ở **Bố cục mẫu** đổi tên **NGAY** thành "Thông tin người mua"
  nhãn tên khối khi rê chuột trên trang xem trước cũng đổi theo
  (một trường, hai chỗ hiển thị — không phải hai trường)
  nhãn trạng thái "Chưa lưu"

EXPECTED — bước 3 và 4
  dấu lỗi tại chỗ ở ô *Tên khối*,
  MSG_PMKT-E-14549_21_206 — "Tên khối tự do không được để trống, tối đa 60 ký tự"
  (cùng một mã với hộp Đặt tên khối — Validation V06 phủ **cả hai** thời điểm:
   "Trong hộp Đặt tên khối, khi rời ô, khi nhấn Lưu")
  nhãn trạng thái "Có lỗi"

EXPECTED — bước 5
  Lưu được; noi_dung.khoi[tuDo].tenKhoi = 'Thông tin người mua'
  bản in  **KHÔNG in** chuỗi "Thông tin người mua"                ← R-TLMI-126
  tên khối **chuẩn** vẫn cố định, không có ô Tên khối để sửa      ← R-TLMI-212
```

### S-TLMI-065 · Ẩn khối Tiêu đề rồi để trống Nội dung

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-085, R-TLMI-207, R-TLMI-208, R-TLMI-209, R-TLMI-234, R-TLMI-239 (V01),
            R-TLMI-241, R-TLMI-242
Quyết định  **C18 chốt** — **khối đang ẩn thì bỏ qua validate của khối đó**. Khối ẩn ⇒ không
            in ra ⇒ nội dung rỗng không gây hậu quả. **Bật lại khối thì validate lại ngay.**

TIỀN ĐỀ
  mẫu CTMDV đã lưu; khối Tiêu đề: con mắt = Có, Nội dung = "CHỨNG TỪ MUA DỊCH VỤ"

THAO TÁC
  1. Xóa trắng ô Nội dung của khối Tiêu đề → rời ô
  2. Tắt con mắt khối Tiêu đề
  3. Bấm Lưu
  4. In
  5. Bật lại con mắt khối Tiêu đề
  6. Bấm Lưu

EXPECTED — bước 1 (khối còn đang hiện)
  dấu lỗi tại chỗ; MSG_PMKT-E-14549_21_201 — "Tiêu đề bản in không được để trống, tối đa
  255 ký tự"; nhãn trạng thái **"Có lỗi"**

EXPECTED — bước 2 (vừa tắt con mắt)
  dấu hiệu lỗi **TẮT NGAY** ở cả hai nơi (dòng khối và khối trên trang xem trước)
  nhãn trạng thái chuyển **"Chưa lưu"**

EXPECTED — bước 3
  **Lưu được**; MSG_PMKT-E-14549_21_101
  noi_dung.khoi[tieuDe].hienThi = Không · noiDung = ''
  thiết lập bên trong khối **vẫn giữ** (cỡ chữ, căn, IN HOA…)     ← R-TLMI-209

EXPECTED — bước 4 (bản in)
  khối Tiêu đề **KHÔNG in**; các khối sau **dồn lên**, không chừa khoảng trống
  bản in **không vỡ**, không có dòng trống

EXPECTED — bước 5 (bật lại con mắt)
  validate chạy lại **NGAY**; dấu lỗi bật lại; MSG_PMKT-E-14549_21_201
  nhãn trạng thái **"Có lỗi"**

EXPECTED — bước 6
  **KHÔNG ghi**; báo MSG_PMKT-E-14549_21_201; mở bảng chỉnh khối Tiêu đề, focus ô Nội dung
  DB giữ nguyên bản của bước 3                                    ← INV-TLMI-012
```

### S-TLMI-066 · Bỏ tick cột cuối khi khối Bảng **đã tắt** con mắt

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-103, R-TLMI-104, R-TLMI-207, R-TLMI-208, R-TLMI-239 (V03), INV-TLMI-004
Quyết định  **B-19 chốt theo cùng họ với C18** — khối Bảng **đang ẩn** thì **không** bắt ràng
            buộc "phải giữ lại ít nhất 1 cột hiển thị". Bật lại con mắt thì bắt ngay.

TIỀN ĐỀ
  khối "Bảng Hàng hóa, dịch vụ": con mắt = **Không** (đã tắt)
  4 cột, chỉ còn C1 "Tên hàng" tick in (Rộng 100)

THAO TÁC
  1. Bỏ tick in cột C1
  2. Lưu
  3. Bật lại con mắt khối Bảng
  4. Lưu
  5. (BE) POST lưu mẫu có khối Bảng **đang ẩn** với 0 cột tick

EXPECTED — bước 1
  **KHÔNG chặn**, không có MSG_…_203
  nhãn trạng thái "Chưa lưu"

EXPECTED — bước 2
  **Lưu được**; MSG_PMKT-E-14549_21_101
  noi_dung.khoi[bang].hienThi = Không · mọi cot[].hienThi = Không
  bản in: khối Bảng không in, các khối sau dồn lên

EXPECTED — bước 3
  validate chạy lại NGAY ⇒ khối Bảng đang bật mà 0 cột tick
  dấu lỗi ở **hai nơi**; nhãn trạng thái **"Có lỗi"**

EXPECTED — bước 4
  **KHÔNG ghi**; thông báo MSG_PMKT-E-14549_21_203 —
  `Bảng "Hàng hóa, dịch vụ" phải giữ lại ít nhất 1 cột hiển thị`

EXPECTED — bước 5
  **chấp nhận** (HTTP 200) — INV-TLMI-004 phát biểu ràng buộc cho khối `HienThi = Có`;
  khối đang ẩn nằm ngoài phạm vi bất biến
  Đối chứng: cùng payload nhưng khối **đang bật** ⇒ 400 + MSG_…_203 (S-TLMI-021)
```

### S-TLMI-067 · Tách ô đang có nội dung

```
Nhóm        biên
Tầng kiểm   FE
Luật phủ    R-TLMI-137, R-TLMI-139, R-TLMI-140, R-TLMI-141, R-TLMI-174
Quyết định  **C19 chốt** — Tách ô đưa nội dung về **ô trên-trái** của vùng vừa tách, các ô
            còn lại thành **ô trống**, **KHÔNG hỏi xác nhận** (không mất dữ liệu). Đối xứng
            với luật Gộp (giữ nội dung ô đầu tiên theo trái→phải, trên→dưới).

TIỀN ĐỀ
  khối tự do "Thông tin chung": lưới 3 dòng × 3 cột
  ô gộp G phủ vùng (1,1)-(2,2) — 2 dòng × 2 cột — mang Chữ tự do "Kính gửi Quý khách"
  các ô còn lại đều trống

THAO TÁC
  1. Chọn ô gộp G → bấm **Tách ô**
  2. Gộp lại (1,1)-(2,2), rồi bấm chuột phải trên ô gộp → chọn **Tách ô** ở menu
  3. Gộp lại, rồi chọn vùng (2,1)-(3,3) — vùng **chạm** ô gộp → bấm Tách ô

EXPECTED — bước 1
  **KHÔNG có hộp xác nhận nào** (không có MSG_…_404 — mã đó chỉ dùng cho **Gộp**)
  vùng trả về **4 ô đơn**: (1,1) · (1,2) · (2,1) · (2,2)
  ô (1,1) — **ô trên-trái** — mang Chữ tự do "Kính gửi Quý khách"
  ba ô còn lại   **Ô trống**
  nút "Tách ô"   Disable;  nút "Gộp ô"  Enable (vùng chọn ≥ 2 ô)
  nhãn trạng thái "Chưa lưu";  đây là **một bước Hoàn tác được**  ← R-TLMI-224

EXPECTED — bước 2
  menu chuột phải cho **cùng kết quả** với thanh công cụ         ← R-TLMI-171

EXPECTED — bước 3
  vùng chọn **tự nới ra** cho trọn ô gộp ⇒ thành (1,1)-(3,3)     ← R-TLMI-137
  sau khi tách: nội dung về ô **(1,1)** — ô trên-trái của **vùng vừa tách**
```

### S-TLMI-068 · Lỗi đầu tiên khi một khối có cả ô bảng chỉnh lẫn ô lưới

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-235, R-TLMI-243, R-TLMI-244, R-TLMI-246, INV-TLMI-012
Quyết định  **C21 chốt** — thứ tự "lỗi đầu tiên":
              1. thứ tự **khối** trong Bố cục mẫu
              2. trong một khối: **ô ở bảng chỉnh trước** (từ trên xuống),
                 **rồi** tới **ô lưới trên trang xem trước** (trái→phải, trên→dưới)

TIỀN ĐỀ
  Bố cục mẫu: 1 đầu trang · 2 Tiêu đề · 3 Bảng · 4 khối tự do "Thông tin chung" · 5 Chữ ký
  khối tự do "Thông tin chung" có **hai lỗi cùng lúc**:
    · ô **Tên khối** ở bảng chỉnh: xóa trắng          ⇒ MSG_…_206
    · ô lưới (2,3): Chữ tự do **256 ký tự**           ⇒ MSG_…_212
  khối Chữ ký cũng có lỗi: ô ký tự do bật, tiêu đề trống ⇒ MSG_…_211

THAO TÁC
  1. Bấm Lưu
  2. Sửa Tên khối = "Thông tin chung" → bấm Lưu
  3. Sửa ô lưới (2,3) còn 200 ký tự → bấm Lưu

EXPECTED — bước 1
  **KHÔNG ghi**                                                  ← INV-TLMI-012
  báo **đúng một** thông báo: MSG_PMKT-E-14549_21_206 — "Tên khối tự do không được để trống,
  tối đa 60 ký tự"   ← ô **bảng chỉnh** đi trước ô lưới trong cùng khối
  mở **bảng chỉnh** của khối "Thông tin chung", con trỏ vào ô **Tên khối**
  KHÔNG báo MSG_…_212, KHÔNG báo MSG_…_211

EXPECTED — bước 2
  báo MSG_PMKT-E-14549_21_212 — "Tên hiển thị và chữ tự do tối đa 255 ký tự"
  **KHÔNG** focus bảng chỉnh — thay vào đó **chọn ô (2,3) trên trang xem trước**,
  ô đó **viền đỏ**                                               ← R-TLMI-244, R-TLMI-235

EXPECTED — bước 3
  báo MSG_PMKT-E-14549_21_211 — "Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự"
  (khối Chữ ký đứng **sau** khối tự do trong Bố cục mẫu nên tới lượt sau cùng)
  Sửa nốt ⇒ MSG_PMKT-E-14549_21_101, badge "Đã lưu"

EXPECTED — đối chứng thứ tự khối
  Kéo khối Chữ ký lên **trước** khối tự do rồi tạo lại cả ba lỗi ⇒ lần Lưu đầu báo
  MSG_PMKT-E-14549_21_211 (thứ tự khối quyết định trước thứ tự ô)
```

### S-TLMI-069 · Mở màn xem trước **lần thứ hai** khi chưa có mẫu

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-007, R-TLMI-260, R-TLMI-268, INV-TLMI-002
Quyết định  **C22 chốt** — `MSG_103` hiện **một lần mỗi lần mở màn xem trước bản in**.
            KHÔNG nhớ qua phiên, KHÔNG nhớ theo người dùng ⇒ **không** lưu cờ đã-hiện vào
            DB, session hay `localStorage`.

TIỀN ĐỀ
  (T1, CTMDV, MUA_DV_TRONG_NUOC)   0 bản ghi
  người dùng u1

THAO TÁC
  1. Mở CT-2026-000123 → In → "Mẫu tùy chỉnh"   (lần 1)
  2. Đóng màn xem trước
  3. In → "Mẫu tùy chỉnh" lần nữa                (lần 2, cùng phiên, cùng người dùng)
  4. Trong **cùng** màn xem trước lần 2, bấm nút In của trình duyệt / Xuất file
  5. Đăng xuất, đăng nhập lại, mở xem trước      (lần 3)
  6. Người dùng u3 mở xem trước cùng chứng từ    (lần 4)

EXPECTED — lần 1
  MSG_PMKT-E-14549_21_103 — "Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in
  theo mẫu chuẩn hệ thống"  — hiện **1 lần**

EXPECTED — lần 2
  MSG_PMKT-E-14549_21_103 **HIỆN LẠI** — mỗi lần mở màn là một lần

EXPECTED — bước 4
  **KHÔNG** hiện lại trong cùng một lần mở màn (vẫn đúng "một lần mỗi lần mở")

EXPECTED — lần 3 và lần 4
  MSG_PMKT-E-14549_21_103 **hiện lại** ở cả hai — không nhớ qua phiên, không nhớ theo người dùng

EXPECTED — sau khi đã có bản ghi
  Lưu một mẫu khác mẫu chuẩn rồi mở xem trước ⇒ **KHÔNG** có MSG_…_103   ← INV-TLMI-002
```

### S-TLMI-070 · Chia đều về 100% khi lưới cột **đang lọc**

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-112, R-TLMI-114, R-TLMI-116, R-TLMI-117, R-TLMI-118, INV-TLMI-005
Quyết định  **C31 chốt** — nút *Chia đều về 100%* áp cho **MỌI cột đang tick in**, không phụ
            thuộc ô *Tìm cột*. Ô tìm **chỉ lọc hiển thị**.

TIỀN ĐỀ
  khối Bảng có 4 cột, cả 4 tick in:
    C1 "Tên hàng"   Rộng 40
    C2 "Số lượng"   Rộng 40
    C3 "Đơn giá"    Rộng 40
    C4 "Thành tiền" Rộng 40     (tổng = 160)

THAO TÁC
  1. Gõ "don gia" (không dấu) vào ô *Tìm cột*
  2. Thử kéo ⠿ đổi thứ tự cột khi đang lọc
  3. Bấm "Chia đều về 100%" **trong khi vẫn đang lọc**
  4. Xóa ô *Tìm cột*, xem lại cả 4 cột
  5. Lưu, đóng màn, mở lại

EXPECTED — bước 1
  lưới cột chỉ hiện **C3 "Đơn giá"** — lọc theo Tên cột dữ liệu và Tên hiển thị,
  **không phân biệt dấu**
  thiết lập của ba cột bị ẩn khỏi lưới **KHÔNG đổi**             ← R-TLMI-118

EXPECTED — bước 2
  **KHÔNG cho kéo thả** khi đang lọc                             ← R-TLMI-117

EXPECTED — bước 3 (điểm chốt của C31)
  thuật toán xét **cả 4 cột đang tick in**, KHÔNG phải chỉ C3:
    mỗi cột = 40 ÷ 160 × 100 = 25,0 → 25   ⇒ tổng = 100
    không cộng bù, không nâng sàn
  lưới đang lọc chỉ **hiển thị** C3 = 25, nhưng C1, C2, C4 **cũng đã đổi** thành 25
  dòng tổng dưới lưới cột: "Tổng độ rộng cột đang 100%"
    ⚠ tổng tính trên **mọi cột tick in**, không phải trên các cột đang hiện

EXPECTED — bước 4
  C1 = 25 · C2 = 25 · C3 = 25 · C4 = 25;  Σ = 100

EXPECTED — bước 5
  ô *Tìm cột* **không được lưu** — mở lại màn thì ô tìm rỗng, lưới hiện đủ 4 cột
  Σ doRong(cột tick in) = 100 và mọi cột trong [3, 90]           ← INV-TLMI-005

  Đối chứng: một cột **bỏ tick in** thì **không** tham gia chia, dù đang hiện hay bị lọc ẩn
  (R-TLMI-112) — xem S-TLMI-025.
```

### S-TLMI-071 · Gọi API in khi thiếu **quyền In**

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-031, R-TLMI-033, R-TLMI-034, R-TLMI-259, R-TLMI-261
Quyết định  **C15 chốt** — thiếu **quyền In** dùng **`MSG_COMMON_003`** ("Bạn không có quyền
            thực hiện chức năng {tên chức năng}…", BR25.2). **KHÔNG** mở rộng
            `MSG_PMKT-E-14549_21_002` như `AD02:27` làm — `6.messages.md` khai mã đó **riêng**
            cho quyền *Thiết lập mẫu in*.

TIỀN ĐỀ
  người dùng u6: **KHÔNG** có quyền In của nghiệp vụ CTMDV
                 **CÓ** quyền Thiết lập mẫu in (`HTMauIn.View` / `HTMauIn.Edit`)
  mẫu CTMDV đã lưu

THAO TÁC
  1. u6 mở form sửa CT-2026-000123
  2. u6 gọi thẳng API dựng bản in "Mẫu tùy chỉnh"
  3. u6 mở màn Thiết lập mẫu in qua menu In
  4. (đối chứng) u3 — thiếu quyền **Thiết lập mẫu in** — gọi API lưu mẫu

EXPECTED — bước 1
  nút In / menu In của nghiệp vụ **không khả dụng** theo quy tắc phân quyền của epic nghiệp vụ

EXPECTED — bước 2
  HTTP      403
  body      **`MSG_COMMON_003`** — "Bạn không có quyền thực hiện chức năng {tên chức năng}…"
  **KHÔNG** trả `MSG_PMKT-E-14549_21_002`
  không dựng bản in, không mở màn xem trước, dữ liệu chứng từ không rò ra ngoài

EXPECTED — bước 3
  u6 **vẫn mở được** màn Thiết lập mẫu in (có quyền Thiết lập mẫu in)
  hai quyền **độc lập nhau** — đối xứng với R-TLMI-033 (có quyền In, không có quyền thiết lập)

EXPECTED — bước 4 (đối chứng, giữ nguyên S-TLMI-035)
  HTTP 403 + **`MSG_PMKT-E-14549_21_002`** — "Bạn không có quyền thực hiện tác vụ này"
  ⇒ hai nhánh thiếu quyền trả **hai mã khác nhau**, không được dùng lẫn

  **Đã ghi vào `04` §7 mục 1**: đề nghị BA cấp mã `MSG_` riêng cho nhánh thiếu quyền In.
```

### S-TLMI-072 · Thiếu `<ChucNang>.View.Detail` khi mở màn

```
Nhóm        ngoại lệ
Tầng kiểm   BE
Luật phủ    R-TLMI-014, R-TLMI-031, R-TLMI-034, R-TLMI-217, R-TLMI-239 (V17)
Quyết định  **C13 chốt** — gate quyền **hai tầng**:
              (a) `HTMauIn.View` (mở màn) / `HTMauIn.Edit` (lưu mẫu) — đã seed ở `V1149`
              (b) **cộng thêm** `<ChucNang>.View.Detail` của chính nghiệp vụ đang mở —
                  vì trang xem trước vẽ bằng **dữ liệu thật của chứng từ** (R-TLMI-217)
            Không tự seed `<ChucNang>.PrintConfig` — thêm mã vào ma trận phân quyền là quyết
            định của BA. Mã đặt ở hằng số **`MaQuyenMauIn`** (**Q-15**).

TIỀN ĐỀ
  người dùng u7: CÓ `HTMauIn.View` và `HTMauIn.Edit`
                 **KHÔNG** có `CTMDV.View.Detail`
  người dùng u8: CÓ `HTMauIn.View`, **KHÔNG** có `HTMauIn.Edit`, CÓ `CTMDV.View.Detail`

THAO TÁC
  1. u7 gọi API mở màn Thiết lập mẫu in cho CT-2026-000123
  2. u8 gọi API mở màn
  3. u8 gọi API lưu mẫu
  4. Kiểm tra mã quyền nằm ở đâu trong code

EXPECTED — bước 1
  HTTP      403
  body      MSG_PMKT-E-14549_21_002 — "Bạn không có quyền thực hiện tác vụ này"
  **KHÔNG** trả bất kỳ dữ liệu nào của CT-2026-000123 — trang xem trước vẽ bằng dữ liệu thật
  nên thiếu quyền xem chi tiết là **lỗ hổng lộ dữ liệu**, không phải bất tiện UI

EXPECTED — bước 2
  mở màn **thành công** (đủ `HTMauIn.View` + `CTMDV.View.Detail`)
  nút Lưu vẫn render (FE không biết `HTMauIn.Edit`), nhưng…

EXPECTED — bước 3
  HTTP 403 + MSG_PMKT-E-14549_21_002
  kiểm ở **Server**, thời điểm "Khi mở màn, **khi Lưu**"          ← R-TLMI-239 (V17)
  DB không đổi

EXPECTED — bước 4
  mọi chuỗi mã quyền nằm ở **một chỗ** (`MaQuyenMauIn`), không rải trong controller/service
  ⇒ đổi sang mã theo nghiệp vụ chỉ sửa một file                   ← Q-15

  ⚠ `04` §5 L-3 ghi rõ đây là chỗ **cố ý lệch tài liệu** (epic nghiệp vụ chưa khai mã quyền
  nào). BA khai mã thật thì sửa hằng số, kịch bản này không đổi.
```

### S-TLMI-073 · Tải ảnh nền hợp lệ, Lưu, rồi Hoàn tác

```
Nhóm        biên
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-069, R-TLMI-070, R-TLMI-071, R-TLMI-072, R-TLMI-075, R-TLMI-223,
            R-TLMI-224, R-TLMI-263, INV-TLMI-012
Quyết định  **C08 chốt** — ảnh nền lưu ở **cột `bytea` trên chính `prn_mau_in_tuy_chinh`**,
            KHÔNG nhét base64 vào JSON: `anh_nen` (`bytea`) · `anh_nen_kieu_tep` (`text`)
            · `anh_nen_ten_tep` (`text`). JSON **chỉ** giữ cờ `rieng.nen.kieu = 'ANH'`.
            Tải lên bằng **`multipart`, endpoint riêng**. Lý do: ảnh 1 MB thành ~1,37 MB
            base64 và bị đọc lại **mỗi lần** nạp mẫu, kể cả khi chỉ cần bố cục (`04` §5 L-2).

TIỀN ĐỀ
  mẫu CTMDV đã lưu; Kiểu hình nền = Không; `anh_nen` = NULL

THAO TÁC
  1. Đổi Kiểu hình nền = **Ảnh tải lên** → chọn `logo-nen.png` (980 KB), Căn ảnh = Giữa trang,
     Độ đậm = 20
  2. Lưu
  3. Nạp lại màn, quan sát số byte tải về của API mở màn
  4. Bấm Hoàn tác (Ctrl+Z)
  5. Đổi Kiểu hình nền = **Không** → Lưu

EXPECTED — bước 1
  tệp đi qua **endpoint `multipart` riêng**, không nằm trong payload JSON của API lưu mẫu
  trang xem trước vẽ ảnh ngay, độ đậm 20 %

EXPECTED — bước 2
  prn_mau_in_tuy_chinh:
    anh_nen           ≈ **980 KB nhị phân** (KHÔNG phải ~1,34 MB base64)
    anh_nen_kieu_tep  'image/png'
    anh_nen_ten_tep   'logo-nen.png'
    noi_dung.rieng.nen.kieu     'ANH'
    noi_dung.rieng.nen.canAnh   'GIUA_TRANG'
    noi_dung.rieng.nen.doDam    20
    noi_dung **KHÔNG chứa** một byte ảnh nào
  `phien_ban` tăng 1;  MSG_PMKT-E-14549_21_101

EXPECTED — bước 3
  API mở màn trả `noi_dung` **nhỏ gọn** (KB, không phải MB) — ảnh lấy qua **URL riêng**,
  chỉ tải khi cần vẽ nền

EXPECTED — bước 4
  Hoàn tác lùi **một bước chỉnh mẫu**: `nen.kieu` về 'KHONG' trên màn
  ⚠ cột `anh_nen` trong DB **KHÔNG bị Hoàn tác động tới** — Hoàn tác chỉ tác động trạng thái
  trên màn (R-TLMI-223); DB chỉ đổi khi bấm Lưu

EXPECTED — bước 5
  noi_dung.rieng.nen.kieu = 'KHONG'; ô Độ đậm / Căn ảnh / Ảnh trở lại **Hide**
  bản in **không có hình nền**
  ⚠ Tài liệu (và `04`) **không nói** có xóa `anh_nen` khỏi DB khi đổi Kiểu = Không hay giữ
  lại để bật lại nhanh ⇒ ca "đọc lại `anh_nen` sau bước 5" **không ghi được** — xem §B.
```

### S-TLMI-074 · Khối tự do còn 1 dòng × 1 cột, bấm Xóa dòng

```
Nhóm        ngoại lệ
Tầng kiểm   CẢ HAI
Luật phủ    R-TLMI-123, R-TLMI-133, R-TLMI-134, R-TLMI-135, R-TLMI-175, R-TLMI-211,
            INV-TLMI-006
Quyết định  **C20 chốt** — sàn lưới khối tự do = **1 dòng × 1 cột**. Xóa dòng cuối cùng /
            cột cuối cùng **bị chặn** (nút mờ). Muốn bỏ hẳn thì dùng *Xóa khối này*
            (`MSG_…_403`).

TIỀN ĐỀ
  khối tự do "Ghi chú" vừa tạo: lưới **1 dòng × 2 cột** (R-TLMI-123), cả hai ô trống

THAO TÁC
  1. Chọn ô (1,2) → bấm "Xóa cột"
  2. Quan sát nút "− Dòng" và "− Cột", rồi bấm cả hai
  3. Dùng menu chuột phải → lệnh Xóa dòng / Xóa cột
  4. Bấm "Xóa khối này" → chọn **Đồng ý**
  5. (BE) POST lưu mẫu có khối tự do `soDong = 0`

EXPECTED — bước 1
  lưới còn **1 dòng × 1 cột**; ô (1,1) giữ nội dung (ở đây là ô trống)

EXPECTED — bước 2
  nút "− Dòng"   **Disable**   ← điều kiện phụ `(đk-NG)`
  nút "− Cột"    **Disable**
  bấm vào không xảy ra gì; lưới **không đổi**; badge không đổi
  **KHÔNG** có thông báo lỗi nào — chặn bằng nút mờ, không bằng message

EXPECTED — bước 3
  hai lệnh tương ứng trong menu chuột phải cũng **mờ**            ← R-TLMI-171

EXPECTED — bước 4
  hộp xác nhận MSG_PMKT-E-14549_21_403 — `Xóa khối "Ghi chú" cùng các ô trong đó?`
  đồng ý ⇒ khối biến mất khỏi Bố cục mẫu — **đây là cách duy nhất** để bỏ hẳn khối
  (nút Xóa khối có ở **cả hai nơi**: dòng khối và bảng chỉnh)     ← R-TLMI-211

EXPECTED — bước 5
  **từ chối**, DB không đổi; 1 ≤ soDong ≤ 20 và 1 ≤ soCot ≤ 6 luôn đúng  ← INV-TLMI-006
  ⚠ Mã message trả về cho nhánh BE này **không có** trong 26 mã và `04` không cấp ⇒ ghi được
  **hành vi** nhưng không ghi được mã — xem §B.
```

### S-TLMI-075 · Căn lề khối đầu trang = Giữa, có Logo

```
Nhóm        biên
Tầng kiểm   BE
Luật phủ    R-TLMI-049, R-TLMI-078, R-TLMI-082, R-TLMI-083, R-TLMI-084
Quyết định  **C29 chốt** — Logo luôn nằm **bên trái khối thông tin đơn vị, cùng hàng với dòng
            đầu tiên**; **căn lề áp cho CẢ CỤM** (logo + các dòng chữ), không tách riêng.

TIỀN ĐỀ
  thiết lập chung — định dạng khối đầu trang (luôn theo chung, màn này không có ô chỉnh):
    Căn lề khối đầu trang = **Giữa** · cỡ logo = 2 cm · lặp trang sau = Bật
  bảy ô tick đầu trang: bật Logo · Tên đơn vị · Địa chỉ · Mã số thuế; tắt ba ô còn lại
  hồ sơ CN-B có logo

THAO TÁC
  1. In (bảng dữ liệu dài 2 trang)
  2. Đổi Căn lề khối đầu trang = **Phải** ở thiết lập chung → in lại
  3. Đổi Căn lề = **Trái** → in lại

EXPECTED — bước 1 (Căn = Giữa)
  cụm đầu trang = **[logo] + [3 dòng chữ]** được căn **GIỮA** trang như một khối
  logo   vẫn nằm **bên trái** các dòng chữ, **cùng hàng với dòng đầu tiên** ("Tên đơn vị")
  logo **KHÔNG** bị căn giữa riêng, chữ **KHÔNG** bị căn giữa riêng
  khối đầu trang **lặp lại** ở trang 2                             ← R-TLMI-084
  thứ tự ba dòng chữ cố định                                       ← R-TLMI-083

EXPECTED — bước 2 (Căn = Phải)
  cả cụm dồn sang **mép phải**; logo vẫn ở **bên trái cụm**, cùng hàng dòng đầu

EXPECTED — bước 3 (Căn = Trái)
  cả cụm sát **mép trái**; bố trí trong cụm không đổi

EXPECTED — luôn đúng
  định dạng khối đầu trang (kiểu chữ, in hoa, cỡ logo, căn lề, lặp trang sau) **luôn theo
  thiết lập chung** — màn Thiết lập mẫu in **không có ô chỉnh** cho chúng   ← R-TLMI-049
  mẫu chỉ điều khiển **bật/tắt bảy dòng** (gồm Logo — C03)
```

### S-TLMI-076 · Lịch sử Hoàn tác theo **phiên mở màn**

```
Nhóm        biên
Tầng kiểm   FE
Luật phủ    R-TLMI-223, R-TLMI-225, R-TLMI-226, R-TLMI-227, R-TLMI-240
Quyết định  **C32 chốt** — Hoàn tác nhớ **60 bước** trong **một phiên mở màn**; đóng màn thì
            **xóa lịch sử**. Không nhớ qua lần mở màn khác, không nhớ qua lần Lưu.

TIỀN ĐỀ
  mẫu CTMDV đã lưu M0; vừa mở màn, lịch sử rỗng, hai nút ↶ ↷ đều Disable

THAO TÁC
  1. Thực hiện 5 thao tác đổi mẫu
  2. Bấm **Lưu** (thành công)
  3. Bấm Hoàn tác 5 lần
  4. Bấm Đóng (badge đang "Chưa lưu" vì vừa hoàn tác) → *Không lưu*
  5. Mở lại màn, quan sát hai nút ↶ ↷
  6. Thực hiện 1 thao tác, bấm Hoàn tác

EXPECTED — bước 2 (Lưu KHÔNG xóa lịch sử)
  badge "Đã lưu"; nút Lưu Disable
  nút ↶ **vẫn Enable**, lịch sử **vẫn 5 bước** — Lưu không phải mốc cắt lịch sử
  (chỉ **đóng màn** mới xóa — R-TLMI-225)

EXPECTED — bước 3
  lùi đủ 5 bước về đúng M0; badge quay lại **"Đã lưu"** (mẫu trên màn bằng bản đã lưu…
  ⚠ ở đây bản đã lưu là bản của bước 2, khác M0) ⇒ badge = **"Chưa lưu"**
  nút ↶ Disable; nút ↷ Enable

EXPECTED — bước 4 và 5
  đóng màn ⇒ lịch sử **bị xóa**
  mở lại: nút ↶ **Disable**, nút ↷ **Disable** — không khôi phục lịch sử của phiên trước
  mẫu trên màn = bản đã lưu ở bước 2

EXPECTED — bước 6
  nút ↶ Enable ngay sau thao tác đầu tiên của **phiên mới**; hoàn tác được về đúng bản đã lưu
  trần vẫn là **60 bước** trong phiên mới (xem S-TLMI-031)
```

### S-TLMI-077 · Chuẩn hóa JSON trước khi so sánh với mẫu chuẩn

```
Nhóm        happy
Tầng kiểm   BE
Luật phủ    R-TLMI-006, R-TLMI-021, R-TLMI-036, R-TLMI-037, R-TLMI-247, INV-TLMI-002,
            INV-TLMI-003
Quyết định  **C02 chốt** — phép so "mẫu bằng mẫu chuẩn" chạy trên **JSON đã chuẩn hóa**:
              1. sắp khóa theo **thứ tự cố định**
              2. **bỏ mọi khóa có giá trị `null`**
              3. **bỏ id kỹ thuật**
            **C28 chốt** — `Bắt buộc = Y` nghĩa là *bắt buộc có **giá trị hiệu dụng*** sau
            fallback, **KHÔNG** phải cột `NOT NULL`. Với JSON: **khóa vắng mặt = theo thiết
            lập chung**.

TIỀN ĐỀ
  (T1, CTMDV, MUA_DV_TRONG_NUOC)  0 bản ghi (đang dùng mẫu chuẩn)
  mẫu chuẩn hệ thống sinh từ đặc tả form của nghiệp vụ

THAO TÁC — bốn payload, cùng nội dung nghiệp vụ, khác nhau về hình thức
  P1  JSON đúng mẫu chuẩn, khóa **đúng thứ tự** chuẩn
  P2  JSON đúng mẫu chuẩn nhưng **đảo thứ tự khóa** (`rieng` trước `giayVaChu`,
      `hienThi` trước `thuTu`…)
  P3  JSON đúng mẫu chuẩn, có thêm `"khoGiay": null`, `"fontChu": null`, `"leTren": null`
  P4  JSON đúng mẫu chuẩn, có thêm id kỹ thuật (`"id": "b3f1…"`, `"uid": 17`) ở mỗi khối
  P5  (đối chứng) như P1 nhưng `khoi[tieuDe].coChu = 19` thay vì 18

  Gửi lần lượt từng payload qua API Lưu, mỗi lần đọc lại DB.

EXPECTED — P1, P2, P3, P4 — **cùng một kết quả**
  sau chuẩn hóa, cả bốn cho **cùng một chuỗi JSON**, bằng chuỗi của mẫu chuẩn
  ⇒ **0 bản ghi** trên `prn_mau_in_tuy_chinh` (không tạo)         ← INV-TLMI-002
  ⇒ toast MSG_PMKT-E-14549_21_101; badge "Đã lưu"
  P3 chứng minh: ghi `null` và **bỏ khóa** là **cùng một trạng thái** — đều là *theo thiết
  lập chung*, không phải "đã nhập giá trị rỗng"                    ← C28, INV-TLMI-003
  P4 chứng minh: id kỹ thuật **không** làm mẫu "khác chuẩn"

EXPECTED — P5 (đối chứng)
  chuẩn hóa ra chuỗi **khác** mẫu chuẩn ⇒ **1 bản ghi** được tạo
  noi_dung.khoi[tieuDe].coChu = 19; `phien_ban` = 1
  in ra **KHÔNG** có MSG_…_103

EXPECTED — hệ quả với cột `NOT NULL`
  **KHÔNG** khai `NOT NULL` + default cho nhóm khóa Giấy và chữ; FE **không** đặt default
  trong Zod/TS cho nhóm này. Làm vậy sẽ phá kế thừa động: mọi mẫu sẽ "đã sửa" ngay khi lưu
  và không bao giờ bằng mẫu chuẩn nữa.                            ← R-TLMI-037 (bẫy triển khai)
```

### S-TLMI-078 · Lưu bằng `phienBan` cũ sau khi người khác đã Lưu

```
Nhóm        tương tranh
Tầng kiểm   BE
Luật phủ    R-TLMI-005, R-TLMI-022, R-TLMI-247, R-TLMI-249, R-TLMI-258, INV-TLMI-012
Quyết định  **C06 chốt** — khóa lạc quan bằng `phienBan`. Đây là kịch bản **BE thuần**, tách
            khỏi S-TLMI-057 (vốn mô tả trải nghiệm hai người dùng) để test API độc lập.

TIỀN ĐỀ
  prn_mau_in_tuy_chinh (T1, CTMDV, MUA_DV_TRONG_NUOC) tồn tại, `phien_ban` = 12

THAO TÁC — gọi API Lưu với các giá trị `phienBan` khác nhau
  1. POST với `phienBan = 12`   (khớp)
  2. POST với `phienBan = 12`   (lặp lại, nay đã lệch vì bước 1 đã tăng)
  3. POST với `phienBan = 99`   (lớn hơn thực tế)
  4. POST **thiếu** trường `phienBan`
  5. POST với `phienBan = 13` sau khi đọc lại   (khớp)
  6. Trường hợp mẫu **chưa tồn tại**: POST tạo mới hai lần liên tiếp

EXPECTED — bước 1
  ghi thành công; `phien_ban` **12 → 13**
  MSG_PMKT-E-14549_21_101

EXPECTED — bước 2 và 3
  HTTP      409
  body      **`MSG_COMMON_001`** — "Thao tác không hợp lệ với trạng thái hiện tại của
            chứng từ/phiếu."
  DB        `noi_dung` **không đổi một bit**, `phien_ban` **vẫn 13**   ← INV-TLMI-012
  **KHÔNG** rollback nhầm sang trạng thái cũ, **KHÔNG** ghi đè âm thầm

EXPECTED — bước 4
  từ chối như bước 2 — thiếu `phienBan` **không** được coi là "ghi đè vô điều kiện"
  (nếu không sẽ có đường vòng qua khóa lạc quan)

EXPECTED — bước 5
  ghi thành công; `phien_ban` **13 → 14**
  từ đó mọi lần in "Mẫu tùy chỉnh" dùng bản mới **ngay**            ← R-TLMI-022

EXPECTED — bước 6 (tạo mới, chưa có bản ghi)
  lần đầu   tạo bản ghi, `phien_ban` = 1
  lần hai   `phienBan` gửi lên vẫn là giá trị của "chưa có bản ghi" ⇒ lệch ⇒ `MSG_COMMON_001`
  ⇒ **đúng 1 bản ghi**, không sinh 2                                ← INV-TLMI-001

EXPECTED — phân biệt với lỗi hệ thống
  lệch phiên bản ⇒ `MSG_COMMON_001` (409) — **không** dùng MSG_PMKT-E-14549_21_003
  lỗi hệ thống thật ⇒ MSG_PMKT-E-14549_21_003 + rollback (S-TLMI-042)
```

---

## §A. Bảng phủ

### A.1 — Bất biến `INV-TLMI-…` → kịch bản (12/12 đã phủ)

| Bất biến | Kịch bản chứng minh | Ghi chú |
|---|---|---|
| INV-TLMI-001 | S-008 · **S-058** · S-078 | S-058 là ca tương tranh bắt buộc; S-078 phủ nhánh tạo mới hai lần |
| INV-TLMI-002 | S-001 · S-006 · **S-055** · S-069 · S-077 | **cả hai chiều** nay kiểm được sau khi C02 chốt "so sánh nội dung" |
| INV-TLMI-003 | S-002 · S-003 · S-049 · S-054 · S-061 · **S-077** | "theo chung" = **khóa vắng mặt** trong JSON (C28), không phải cột `NULL` |
| INV-TLMI-004 | S-021 · **S-066** | S-066 khoanh đúng phạm vi: bất biến chỉ áp cho khối `hienThi = Có` |
| INV-TLMI-005 | S-009 · S-019 · S-022 · S-023 · S-024 · S-025 · S-059 · S-070 | đủ 3 ví dụ của BA + ca chạm sàn 3 + ca đang lọc (C31) |
| INV-TLMI-006 | S-013 · S-014 · S-015 · S-016 · **S-074** | trần 10 khối · 20 dòng · 6 cột; sàn 1×1 chốt ở C20 |
| INV-TLMI-007 | S-047 | kèm ca "cùng trường ở khối khác thì được phép" |
| INV-TLMI-008 | S-001 · S-041 · S-045 · S-054 | S-045 là nhánh BE từ chối |
| INV-TLMI-009 | S-027 | đổi Tên hiển thị ở khối A ⇒ khối B đổi theo |
| INV-TLMI-010 | S-010 · S-030 · **S-062** | S-062 phủ nhánh ô ký **chức danh** sau khi C04 chốt |
| INV-TLMI-011 | S-011 · S-058 | không mệnh đề lọc chi nhánh; C26 xếp nhóm 1 — cấu hình hệ thống |
| INV-TLMI-012 | S-013 · S-017 · S-037 · S-042 · S-050 · S-051 · S-054 · S-065 · S-068 · **S-078** | rollback do validate · do lỗi hệ thống · do **lệch phiên bản** (C06) |

**Không bất biến nào trống.**

### A.2 — Luật P0 → kịch bản (47/47 đã phủ, **0 luật còn bị chặn**)

| Luật P0 | Kịch bản | Luật P0 | Kịch bản |
|---|---|---|---|
| R-TLMI-001 | S-008 · S-058 | R-TLMI-039 | S-003 |
| R-TLMI-002 | S-008 | R-TLMI-044 | S-049 |
| R-TLMI-003 | S-008 | R-TLMI-078 | S-033 · S-063 · S-075 |
| R-TLMI-004 | S-008 · S-058 | R-TLMI-093 | S-059 |
| R-TLMI-005 | S-011 · S-057 · S-058 · S-078 | R-TLMI-119 | S-060 |
| R-TLMI-006 | S-001 · S-055 · S-077 | R-TLMI-178 | S-005 · S-056 |
| R-TLMI-007 | S-001 · S-006 · S-069 | R-TLMI-192 | S-030 · S-046 |
| R-TLMI-008 | S-001 · S-045 · S-054 | R-TLMI-210 | S-041 · S-045 |
| R-TLMI-009 | S-001 · S-045 | R-TLMI-239 | S-013…S-021 · S-026…S-030 · S-032 · S-035 · S-037 · S-039 · S-040 · S-064 · S-065 · S-066 · S-072 |
| R-TLMI-011 | S-001 · S-008 | R-TLMI-243 | S-037 · **S-068** |
| R-TLMI-012 | S-008 | R-TLMI-246 | S-002 · S-017 · S-037 · S-072 |
| R-TLMI-013 | S-005 | R-TLMI-247 | S-002 · S-042 · S-055 · S-057 · S-058 · S-077 · S-078 |
| R-TLMI-018 | S-054 | R-TLMI-249 | S-042 · S-078 |
| R-TLMI-019 | S-054 | R-TLMI-251 | S-050 · S-051 · S-052 |
| R-TLMI-021 | **S-055** · S-077 | R-TLMI-252 | S-050 |
| R-TLMI-028 | S-001 · S-007 | R-TLMI-253 | S-051 · S-054 |
| R-TLMI-031 | S-011 · S-035 · S-072 | R-TLMI-259 | S-005 · S-071 |
| R-TLMI-032 | S-035 | R-TLMI-261 | S-044 · S-071 |
| R-TLMI-033 | S-011 · S-036 · S-071 | R-TLMI-264 | S-003 · S-005 |
| R-TLMI-034 | S-035 · S-071 · S-072 | R-TLMI-266 | S-060 |
| R-TLMI-035 | S-011 | R-TLMI-267 | S-005 · S-033 · **S-063** |
| R-TLMI-036 | S-003 · S-061 | R-TLMI-269 | S-007 · S-035 |
| R-TLMI-037 | S-002 · **S-077** | R-TLMI-270 | S-043 |
| R-TLMI-038 | S-003 | | |

**Không luật P0 nào trống, và không luật nào còn ở dạng "chưa chốt".** Sáu luật P0 từng bị chặn ở bản
trước nay đều có expected state dứt khoát: R-TLMI-021 (C02 → S-055, S-077) · R-TLMI-044 (C17 → S-049)
· R-TLMI-093 (C10 → S-059) · R-TLMI-119 và R-TLMI-266 (C01 → S-060) · R-TLMI-252 (C23 → S-050) ·
R-TLMI-261 (C14 → S-044).

### A.3 — Mã message → kịch bản (26/26 mã của BA + 2 mã chung)

| Mã message | Nội dung nguyên văn | Kịch bản |
|---|---|---|
| `MSG_PMKT-E-14549_21_002` | Bạn không có quyền thực hiện tác vụ này | S-035 · S-071 (đối chứng) · S-072 |
| `MSG_PMKT-E-14549_21_003` | Lỗi hệ thống, vui lòng thử lại sau | S-042 · S-043 · S-050 · S-078 (phân biệt) |
| `MSG_PMKT-E-14549_21_101` | Lưu mẫu in thành công! | S-002 · S-004 · S-007 · S-009 · S-017 · S-018 · S-020 · S-028 · S-030 · S-034 · S-036 · S-037 · **S-050** · S-055 · S-057 · S-059 · S-065 · S-066 · S-073 · S-077 · S-078 |
| `MSG_PMKT-E-14549_21_102` | Đã đưa về mẫu chuẩn hệ thống. Bấm Lưu để có hiệu lực | S-054 |
| `MSG_PMKT-E-14549_21_103` | Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in theo mẫu chuẩn hệ thống | S-006 · S-055 · **S-069** |
| `MSG_PMKT-E-14549_21_104` | Đã thêm khối tự do trước Chữ ký. Nháy đúp một ô để chọn trường, hoặc kéo trường từ bảng bên phải thả vào ô | S-004 · S-026 · S-064 |
| `MSG_PMKT-E-14549_21_201` | Tiêu đề bản in không được để trống, tối đa 255 ký tự | S-029 · **S-065** |
| `MSG_PMKT-E-14549_21_202` | Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36 | S-020 · S-037 · S-050 |
| `MSG_PMKT-E-14549_21_203` | Bảng "{TenBang}" phải giữ lại ít nhất 1 cột hiển thị | S-021 · **S-066** |
| `MSG_PMKT-E-14549_21_204` | Tên hiển thị của cột không được để trống, tối đa 100 ký tự | S-028 |
| `MSG_PMKT-E-14549_21_205` | Độ rộng cột phải là số nguyên từ 3 đến 90 | S-019 · S-037 |
| `MSG_PMKT-E-14549_21_206` | Tên khối tự do không được để trống, tối đa 60 ký tự | S-026 · **S-064** · S-068 |
| `MSG_PMKT-E-14549_21_207` | Mỗi mẫu tối đa 10 khối tự do | S-016 |
| `MSG_PMKT-E-14549_21_208` | Mỗi khối tự do tối đa 20 dòng | S-013 |
| `MSG_PMKT-E-14549_21_209` | Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB | S-039 |
| `MSG_PMKT-E-14549_21_210` | Mã màu phải có dạng #rrggbb | S-040 |
| `MSG_PMKT-E-14549_21_211` | Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự | S-030 · **S-062** · S-068 |
| `MSG_PMKT-E-14549_21_212` | Tên hiển thị và chữ tự do tối đa 255 ký tự | S-027 · S-037 · **S-068** |
| `MSG_PMKT-E-14549_21_213` | Căn lề phải là số từ 0 đến 5 cm | S-018 |
| `MSG_PMKT-E-14549_21_214` | Số cột để tự động in ngang phải là số nguyên từ 1 đến 50 | S-032 |
| `MSG_PMKT-E-14549_21_215` | Cỡ chữ phải là số nguyên từ 8 đến 20 | S-017 |
| `MSG_PMKT-E-14549_21_216` | Mỗi khối tự do tối đa 6 cột | S-014 |
| `MSG_PMKT-E-14549_21_401` | Mẫu đã có thay đổi chưa lưu. Bạn muốn làm gì? | S-048 · S-050 · S-051 · S-052 · S-053 |
| `MSG_PMKT-E-14549_21_402` | Mọi tùy chỉnh (kể cả khối tự do, thứ tự khối, cột bảng, chữ ký) sẽ trở về mẫu chuẩn hệ thống. Thay đổi chỉ có hiệu lực khi bạn bấm Lưu. Tiếp tục? | S-054 |
| `MSG_PMKT-E-14549_21_403` | Xóa khối "{TenKhoi}" cùng các ô trong đó? | S-041 · **S-074** |
| `MSG_PMKT-E-14549_21_404` | Vùng chọn có {SoO} ô đang có nội dung. Gộp thì chỉ giữ nội dung của ô đầu tiên, các ô còn lại mất nội dung. Tiếp tục? | S-038 · S-067 (đối chứng: Tách **không** dùng mã này) |

**Không mã nào trống.** Ba mã có **tham số** được kiểm cùng giá trị thật: `{TenBang}` = "Hàng hóa,
dịch vụ" (S-021, S-066) · `{TenKhoi}` = "Thông tin chung" / "Ghi chú" (S-041, S-074) · `{SoO}` = 2
(S-038 — đếm **ô CÓ nội dung**, không đếm ô trống trong vùng).

**Hai mã CHUNG dùng thay cho mã BA chưa cấp** (`04` §5 L-4 — cố ý lệch tài liệu):

| Mã chung | Nội dung nguyên văn | Dùng cho | Kịch bản |
|---|---|---|---|
| `MSG_COMMON_001` | Thao tác không hợp lệ với trạng thái hiện tại của chứng từ/phiếu. | lệch `phienBan` khi Lưu (C06) | **S-057** · **S-078** |
| `MSG_COMMON_003` | Bạn không có quyền thực hiện chức năng {tên chức năng}… | thiếu **quyền In** (C15) | **S-071** |

**Hai chuỗi CHỈ có key i18n, KHÔNG có mã `MSG_`** (`04` §5 L-5 — `msg.sh` báo `THIEU`, đã chấp nhận):

| Nguyên văn | Nơi dùng | Kịch bản |
|---|---|---|
| Đơn vị không cho phép in chứng từ chưa ghi sổ | tooltip nút In bị disable | **S-044** |
| Đơn vị không cho phép in chứng từ đã khóa sổ | tooltip nút In bị disable | **S-044** |

### A.4 — Mục mâu thuẫn đã chốt → kịch bản chứng minh (32/32)

| Mục | Mức | Quyết định (rút gọn) | Kịch bản |
|---|---|---|---|
| **C01** | P0 | khóa gộp **CÓ** thuế suất (+ số lô, HSD) | S-060 |
| **C02** | P0 | **so sánh nội dung** JSON chuẩn hóa ⇒ xóa bản ghi | S-055 · S-077 |
| **C08** | P0 | ảnh nền vào cột `bytea`, JSON chỉ giữ cờ | S-073 · S-039 |
| **C09** | P0 | không còn áp dụng sau Q-01 — thay bằng JSON schema | mọi kịch bản có expected DB |
| **C10** | P0 | bỏ qua im lặng khi in; mờ + nhãn khi mở màn | S-059 |
| **C11** | P0 | áp bộ BR **Phase 2** (Q-02) | nền của S-003 · S-033 · S-060 · S-063 · S-075 |
| **C12** | P0 | tầng "thiết lập chung tối thiểu" (Q-03) + cổng `HoSoDonViPort` (Q-14) | S-063 · S-075 |
| **C13** | P0 | `HTMauIn.*` + `<ChucNang>.View.Detail`, hằng số `MaQuyenMauIn` | S-072 · S-035 |
| **C37** | P0 | mô hình **JSON** trên `prn_mau_in_tuy_chinh` (Q-01) | S-002 · S-058 · S-077 |
| **C03** | P1 | Logo **CÓ** trong 7 ô tick sửa riêng được | S-061 · S-033 · S-075 |
| **C04** | P1 | tiêu đề in ra của chức danh **sửa riêng được** | S-062 |
| **C05** | P1 | Chữ ký đọc hồ sơ **chi nhánh trên chứng từ** | S-063 |
| **C06** | P1 | **khóa lạc quan** `phienBan` → `MSG_COMMON_001` | S-057 · S-078 |
| **C07** | P1 | sửa tên khối tự do ở **cả hai chỗ** | S-064 |
| **C14** | P1 | 2 tooltip giữ nguyên văn, **key i18n**, không mã `MSG_` | S-044 |
| **C15** | P1 | thiếu quyền In → **`MSG_COMMON_003`** | S-071 |
| **C16** | P1 | giữ đúng tài liệu — nút ở **mức nhóm**, không nhãn từng ô | S-049 |
| **C17** | P1 | đổi Khổ/Hướng ở thanh Xem trước **LÀ đổi mẫu** | S-049 |
| **C18** | P1 | khối **đang ẩn** thì bỏ qua validate của khối đó | S-065 · S-066 |
| **C19** | P1 | Tách ô → nội dung về ô trên-trái, **không hỏi** | S-067 |
| **C20** | P1 | sàn lưới **1 dòng × 1 cột**, nút mờ | S-074 · S-015 |
| **C21** | P1 | ô bảng chỉnh trước, rồi ô lưới | S-068 |
| **C22** | P1 | `MSG_103` một lần **mỗi lần mở màn xem trước** | S-069 |
| **C23** | P1 | *Lưu và đóng* **CÓ** toast `_101` rồi mới đóng | S-050 |
| **C24** | P1 | **không** thêm cảnh báo chi nhánh | S-011 |
| **C38** | P1 | `bieuMau` và mẫu in **độc lập**, không gộp dữ liệu | — quyết định kiến trúc, không sinh kịch bản nghiệp vụ |
| **C26** | P2 | xếp **nhóm 1 — cấu hình hệ thống** của BR50.6 | S-011 |
| **C28** | P2 | `Y` = bắt buộc **giá trị hiệu dụng**; khóa vắng mặt = theo chung | S-002 · S-077 |
| **C29** | P2 | logo luôn bên trái cụm; căn lề áp **cả cụm** | S-075 |
| **C30** | P2 | cộng gộp chỉ cho Hóa đơn / phiếu xuất kho / phiếu nhập kho | S-060 |
| **C31** | P2 | chia đều áp **mọi cột tick in**, không phụ thuộc ô Tìm cột | S-070 |
| **C32** | P2 | Hoàn tác **60 bước** theo phiên mở màn | S-076 · S-031 |

`C25` · `C27` · `C33` · `C34` đã `CLOSED-AUTO` từ vòng soát trước, không sinh kịch bản riêng.

---

## §B. Chưa viết được kịch bản

> Sau khi `04-quyet-dinh-ban-giao.md` đóng 32 mục, **26 mục `B-…` của bản trước đã thành kịch bản
> thật** (`S-TLMI-061` … `S-TLMI-078` cộng với 7 kịch bản viết lại). Phần còn lại dưới đây là chỗ
> **thật sự** không ghi được expected state.
>
> Ba nhóm: **(B.1)** phát biểu không đo được · **(B.2)** ngoài phạm vi epic · **(B.3)** khoảng trống
> `Z-…` chưa nâng thành mục `C` nên `04` không chốt · **(B.4)** hệ quả của mô hình JSON mà `04` chưa
> nói hết. Nhóm B.3 và B.4 **không chặn code** — mỗi mục ghi rõ phần nào ghi được, phần nào không.

### B.1 — Phát biểu **không đo được** (3 mục)

| # | Phát biểu | Vì sao không viết được expected state |
|---|---|---|
| B-01 | R-TLMI-073 · Căn ảnh = Giữa trang ⇒ ảnh "chiếm **khoảng nửa trang**" | "khoảng nửa trang" không có công thức ⇒ không có ngưỡng để so. S-TLMI-039 chỉ kiểm được *giữ tỷ lệ · nằm giữa · vẽ dưới mọi khối* |
| B-02 | R-TLMI-198 · Chỗ trống ký **Thấp / Vừa / Cao** | ba mức không có số đo (cm hay số dòng). S-TLMI-010 chỉ kiểm mặc định = Vừa |
| B-03 | R-TLMI-215 · Rê chuột hiện **nhãn tên khối** | có nội dung nhãn nhưng không có quy định thời gian trễ / vị trí. S-TLMI-012 chỉ kiểm nhãn hiện đúng tên |

### B.2 — Ngoài phạm vi epic (4 mục — **không phải lỗi tài liệu**)

| # | Hạng mục | Do ai quyết |
|---|---|---|
| B-04 | Hành vi chung của màn xem trước bản in (nút In, Xuất file, định dạng xuất) — S-TLMI-005 và S-TLMI-043 chỉ kiểm phần epic `_21` chịu trách nhiệm | ngoài epic (Z-39) |
| B-05 | Danh mục **mẫu in cố định theo quy định** (01-TT, 02-VT…) — S-TLMI-005 chỉ kiểm "vẫn liệt kê và vẫn in như cũ" | ngoài epic (Z-40) |
| B-06 | **Đặc tả form** (các ô, các lưới, cột của lưới) làm nguồn cho mẫu chuẩn và kho trường — mọi kịch bản giả định form mẫu ở phần "Quy ước dữ liệu" | epic nghiệp vụ (Z-35) |
| B-07 | Danh sách **5 chức danh** và các cột `TieuDeNguoiKy*` / `TenNguoiKy*` của màn Thiết lập người ký | epic `PMKT-E-14549_CauHinhBanDau` (Z-36) |

### B.3 — Khoảng trống `Z-…` mà `04` **không chốt** (6 mục — không chặn code)

| # | Chỗ thiếu | Ghi được gì | Không ghi được gì | Mã |
|---|---|---|---|---|
| B-08 | **Độ đậm hình nền** ngoài miền 5–100 % | miền hợp lệ 5–100, mặc định 20, áp cho cả Khung viền lẫn Ảnh (S-TLMI-039, S-TLMI-073) | **mã message** và **tầng chặn** khi vi phạm — bảng Validation 17 dòng không có dòng nào cho ô này | Z-03 |
| B-09 | **Danh sách 10 mã màu** preset | ô nhập hex và validate `#rrggbb` (S-TLMI-040) | ca "bấm ô màu preset thứ n" — tài liệu nói 10 ô, Figma đếm 9, không liệt kê mã nào | Z-04 |
| B-10 | Hai khối tự do **trùng tên** | ràng buộc không trống / ≤ 60 ký tự (S-TLMI-026, S-TLMI-064) | có unique check hay không ⇒ ca "đặt tên trùng khối đã có" | Z-11 |
| B-11 | **Đặt lại mẫu chuẩn** có phải một bước Hoàn tác được không | Đặt lại chỉ đổi trên màn, Lưu mới có hiệu lực (S-TLMI-054) | không đưa được thao tác này vào chuỗi đếm bước của S-TLMI-031 và S-TLMI-056 | Z-17 |
| B-12 | **In đậm / Nghiêng / Căn** trên vùng chọn có ô **khác loại nội dung** (vừa trường vừa Chữ tự do) | In đậm là thuộc tính CỦA TRƯỜNG dùng chung cả mẫu; Căn đặt theo ô (S-TLMI-027, S-TLMI-047) | kết quả khi hai mô hình dữ liệu đụng nhau trong một vùng chọn | Z-18 |
| B-13 | Kéo ô gộp thả lên ô thường khi **nội dung dài hơn chỗ chứa** | hai ô đổi nội dung, kích thước gộp giữ theo ô (S-TLMI-047) | hành vi hiển thị và in khi nội dung tràn | Z-19 |

### B.4 — Hệ quả của mô hình JSON mà `04` chưa nói hết (2 mục)

| # | Chỗ thiếu | Ghi được gì | Không ghi được gì |
|---|---|---|---|
| B-14 | Mã message cho các nhánh BE **từ chối vì cấu trúc sai** — xóa khối chuẩn · payload thiếu khối chuẩn · khối tự do 0 dòng / 0 cột | **hành vi**: từ chối, DB không đổi, bất biến vẫn đúng (S-TLMI-045, S-TLMI-074) | body trả **mã nào** — không nằm trong 26 mã của BA và `04` không cấp mã chung nào cho nhánh này |
| B-15 | Cột `anh_nen` khi người dùng đổi **Kiểu hình nền = Không** | JSON đổi `nen.kieu` về `KHONG`, bản in không có nền (S-TLMI-073 bước 5) | có **xóa** `anh_nen` khỏi DB hay **giữ lại** để bật lại nhanh — `04` §2 C08 không nói |

> Ba mục còn **nợ BA** ở `04` §7 (cấp mã `MSG_` cho xung đột phiên bản · thiếu quyền In · 2 tooltip)
> **không** nằm ở §B: chúng đã có kịch bản với mã chung hoặc key i18n (S-TLMI-078, S-TLMI-071,
> S-TLMI-044). Khi BA cấp mã thật thì **chỉ đổi mã trong ba kịch bản đó**, cấu trúc không đổi.
>
> Hai rủi ro UX ở `04` §7 mục 2 (**C16**, **C17**) cũng không nằm ở §B — S-TLMI-049 đã ghi expected
> state theo đúng tài liệu, kèm danh sách việc **cấm tự thêm** trước khi BA trả lời.

---

*Hết `03-scenarios.md`. File này suy ra từ `02-rules.md`, `01-conflict.md` và
`04-quyet-dinh-ban-giao.md`. Không sửa ba file đó từ đây; tài liệu BA gốc nằm trong vùng đóng băng
`Phase_2` — không mở.*
