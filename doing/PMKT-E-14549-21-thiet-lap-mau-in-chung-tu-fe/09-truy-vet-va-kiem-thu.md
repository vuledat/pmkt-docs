# 09 · Bảng truy vết luật → file → test · Danh sách kiểm thử

| | |
|---|---|
| Nguồn luật | [`02-rules.md`](../PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/02-rules.md) — 271 luật |
| Tổng luật | **271** |
| Luật tầng `FE` | **108** |
| Luật tầng `CẢ HAI` | **129** |
| **FE phải phủ** | **237 / 271** (108 + 129) |
| Luật thuần `BE` (ngoài phạm vi file này) | **34** |
| Trạng thái chặn | **0 mục `OPEN`** — 9 luật từng mang `CHỜ C01…C07` đã được [`04-quyet-dinh-ban-giao.md`](../PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/04-quyet-dinh-ban-giao.md) đóng |

> **Bảng §1 sinh bằng máy** từ các bảng tổng của `02-rules.md` (lọc `Tầng ∈ {FE, CẢ HAI}`) rồi ánh xạ
> sang file/test theo nhóm luật. Đường dẫn rút gọn, gốc là `client/src/base/domainKit/mauIn/`.
> **Không sửa tay** — sinh lại bằng đoạn PowerShell ở §4.

> ⚠ Đây là **file DỰ KIẾN**, chưa có dòng code nào. Sau `/gen-fe`, chạy
> `./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec fe` để đối chiếu
> bảng này với code thật; `MISSING` nghĩa là **luật chưa được hiện thực**, bất kể code trông có vẻ đúng.

---

## 1. Bảng truy vết — 237 luật tầng FE

| Luật | Tầng | Sev | Tên luật (rút gọn) | File dự kiến (`@domain-kit/mauIn/…`) | Test dự kiến |
|---|---|---|---|---|---|
| `R-TLMI-002` | CẢ HAI | P0 | "Nghiệp vụ" = giá trị ô Loại nghiệp vụ trên form, do epic n… | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-003` | CẢ HAI | P0 | Loại chứng từ không chia nghiệp vụ thì cả loại chứng từ là … | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-007` | CẢ HAI | P0 | Chưa có bản ghi mẫu = nghiệp vụ đang dùng mẫu chuẩn hệ thống | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-008` | CẢ HAI | P0 | Mẫu chuẩn có đúng bốn loại khối theo thứ tự cố định, không … | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-009` | CẢ HAI | P0 | Form có n lưới thì mẫu chuẩn có n khối Bảng, đủ cột gốc, mọ… | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-010` | CẢ HAI | P1 | Thông tin chung / tổng tiền phải tự dựng bằng khối tự do | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-011` | CẢ HAI | P0 | Mở màn từ một chứng từ thì mở đúng mẫu của nghiệp vụ chứng … | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-012` | CẢ HAI | P0 | Đổi Loại nghiệp vụ trên form rồi mở lại thì mở một mẫu khác | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-013` | CẢ HAI | P0 | Mẫu in cố định theo quy định (01-TT, 02-VT…) không sửa được… | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-014` | CẢ HAI | P1 | Nghiệp vụ nào có chức năng này và mã quyền là gì do epic ng… | `helpers/mauChuan.ts · api/schemas.ts` | `test/mauChuan.test.ts` |
| `R-TLMI-015` | FE | P1 | Bấm Đặt lại mẫu chuẩn thì hỏi trước | `hooks/useDatLaiMauChuan.ts · components/modal/XacNhanDatLaiModal.tsx` | `test/datLaiMauChuan.test.tsx` |
| `R-TLMI-016` | FE | P1 | Xác nhận Đặt lại thì nạp lại toàn bộ mẫu chuẩn hệ thống | `hooks/useDatLaiMauChuan.ts · components/modal/XacNhanDatLaiModal.tsx` | `test/datLaiMauChuan.test.tsx` |
| `R-TLMI-017` | FE | P1 | Đặt lại xong thì báo và chuyển nhãn trạng thái Chưa lưu | `hooks/useDatLaiMauChuan.ts · components/modal/XacNhanDatLaiModal.tsx` | `test/datLaiMauChuan.test.tsx` |
| `R-TLMI-018` | CẢ HAI | P0 | Đặt lại chỉ đổi trên màn, bấm Lưu mới có hiệu lực | `hooks/useDatLaiMauChuan.ts · components/modal/XacNhanDatLaiModal.tsx` | `test/datLaiMauChuan.test.tsx` |
| `R-TLMI-019` | CẢ HAI | P0 | Đặt lại mà chưa Lưu rồi Đóng › Không lưu thì mẫu cũ còn nguyên | `hooks/useDatLaiMauChuan.ts · components/modal/XacNhanDatLaiModal.tsx` | `test/datLaiMauChuan.test.tsx` |
| `R-TLMI-020` | FE | P1 | Không đồng ý hộp xác nhận Đặt lại thì giữ nguyên mẫu đang c… | `hooks/useDatLaiMauChuan.ts · components/modal/XacNhanDatLaiModal.tsx` | `test/datLaiMauChuan.test.tsx` |
| `R-TLMI-023` | FE | P1 | Menu In: mẫu cố định → đường kẻ → Mẫu tùy chỉnh → Thiết lập… | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-024` | FE | P1 | Hai mục menu dùng đúng tên "Mẫu tùy chỉnh" và "Thiết lập mẫ… | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-025` | CẢ HAI | P1 | Form thêm mới không có nút In; menu In chỉ có ở form sửa và… | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-026` | FE | P1 | Nghiệp vụ có In từ danh sách thì menu In cũng xuất hiện trê… | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-027` | FE | P1 | Màn xem trước bản in có thêm nút Sửa mẫu | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-028` | CẢ HAI | P0 | Hai lối vào cho cùng một màn và cùng một mẫu | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-029` | FE | P1 | Đóng màn thì quay lại đúng nơi vừa mở ra | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-030` | FE | P1 | Quay lại màn xem trước sau khi lưu thì bản in vẽ lại theo m… | `components/NutInChungTu.tsx · components/modal/XemTruocBanInModal.tsx` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-031` | CẢ HAI | P0 | Quyền Thiết lập mẫu in xét theo nghiệp vụ tại chi nhánh đan… | `components/NutInChungTu.tsx · constants/permissions.ts` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-032` | FE | P0 | Không có quyền thì mục menu và nút Sửa mẫu ẩn hẳn, không ph… | `components/NutInChungTu.tsx · constants/permissions.ts` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-033` | CẢ HAI | P0 | Không có quyền Thiết lập mẫu in nhưng có quyền In thì vẫn i… | `components/NutInChungTu.tsx · constants/permissions.ts` | `test/NutInChungTu.test.tsx` |
| `R-TLMI-036` | CẢ HAI | P0 | Mỗi ô Giấy và chữ và mỗi ô trong bảy ô tick đầu trang có ha… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-040` | FE | P1 | Nút Theo thiết lập chung của nhóm Giấy và chữ đưa cả nhóm v… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-041` | FE | P2 | Bấm nút Theo thiết lập chung là một bước Hoàn tác được | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-042` | FE | P1 | Không có cách đưa riêng một ô về theo chung | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-043` | FE | P1 | Nút Theo thiết lập chung của khối Thông tin đầu trang đưa c… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-044` | CẢ HAI | P0 | Đổi Khổ giấy / Hướng giấy trên thanh Xem trước làm ô đó trở… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-045` | FE | P1 | Trạng thái theo chung / riêng không có nhãn riêng từng ô, k… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-046` | CẢ HAI | P1 | Người ký (tiêu đề, tên, cờ in tên) luôn theo thiết lập chung | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-047` | CẢ HAI | P1 | Ba quy tắc in chứng từ luôn theo thiết lập chung, màn này k… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-048` | CẢ HAI | P1 | Mục "Bố cục mặc định của báo cáo" của thiết lập chung KHÔNG… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-049` | CẢ HAI | P1 | Định dạng khối đầu trang (kiểu chữ, in hoa, cỡ logo, căn lề… | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-050` | FE | P2 | Liên kết Mở Cấu hình báo cáo chứng từ (tab Quy tắc in chung) | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-051` | FE | P2 | Liên kết Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-052` | FE | P2 | Liên kết Mở Thiết lập người ký | `helpers/keThua.ts · components/inspector/ThietLapMauInspector.tsx` | `test/keThua.test.ts` |
| `R-TLMI-053` | FE | P1 | Nhóm Giấy và chữ luôn hiện đủ sáu ô kèm giá trị đang dùng | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-054` | CẢ HAI | P1 | Khổ giấy chỉ nhận A3 / A4 / A5 | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-055` | CẢ HAI | P1 | Hướng giấy chỉ nhận Dọc / Ngang / Tự động | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-056` | CẢ HAI | P1 | Hướng giấy = Tự động thì ô Số cột để tự động in ngang mới h… | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-057` | CẢ HAI | P1 | Số cột để tự động in ngang là số nguyên 1–50 | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-058` | CẢ HAI | P1 | Hướng Tự động với chứng từ: xét khối Bảng đang bật có nhiều… | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-059` | CẢ HAI | P1 | Hướng Tự động mà không có khối Bảng nào đang bật thì in dọc | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-060` | CẢ HAI | P1 | Hướng Dọc hoặc Ngang thì in đúng hướng đó bất kể số cột | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-061` | CẢ HAI | P1 | Căn lề bốn phía là số 0–5 cm, tối đa một chữ số lẻ | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-062` | CẢ HAI | P1 | Font chữ chỉ nhận Times New Roman hoặc Arial | `components/inspector/GiayVaChuGroup.tsx · helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-064` | CẢ HAI | P1 | Màu chữ là giá trị riêng của mẫu, mặc định `#000000`, không… | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-065` | CẢ HAI | P1 | Màu chữ áp cho toàn bộ chữ và đường kẻ của bản in, trừ logo | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-066` | CẢ HAI | P1 | Chọn màu bằng 10 ô màu hoặc gõ mã dạng `#rrggbb` | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-067` | CẢ HAI | P2 | Kiểu hình nền = Không (mặc định) thì không in hình nền | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-068` | CẢ HAI | P2 | Kiểu hình nền = Khung viền thì kẻ khung quanh mép trang the… | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-069` | CẢ HAI | P1 | Kiểu hình nền = Ảnh tải lên thì chọn tệp jpg/png ≤ 1MB | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-070` | FE | P1 | Kiểu hình nền ≠ Không thì ô Độ đậm mới hiện và mới bắt buộc | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-071` | FE | P1 | Kiểu hình nền = Ảnh tải lên thì ô Căn ảnh và ô Ảnh mới hiện… | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-072` | CẢ HAI | P1 | Độ đậm 5–100 %, mặc định 20, áp cho cả Khung viền lẫn Ảnh t… | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-073` | CẢ HAI | P2 | Căn ảnh = Giữa trang thì ảnh giữ tỷ lệ, chiếm khoảng nửa tr… | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-074` | CẢ HAI | P2 | Căn ảnh = Toàn trang thì kéo giãn ảnh phủ kín phần giấy tro… | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-075` | CẢ HAI | P1 | Hình nền in dưới mọi khối và không ảnh hưởng vị trí khối | `components/inspector/RiengCuaMauGroup.tsx · helpers/kiemTraMau.ts` | `test/riengCuaMau.test.tsx` |
| `R-TLMI-076` | CẢ HAI | P1 | Ô tick "In khối Thông tin đầu trang trên mẫu này" bật/tắt c… | `components/inspector/DauTrangInspector.tsx · helpers/keThua.ts` | `test/DauTrangInspector.test.tsx` |
| `R-TLMI-077` | CẢ HAI | P1 | Bảy ô tick dòng in, mặc định theo thiết lập chung với mặc đ… | `components/inspector/DauTrangInspector.tsx · helpers/keThua.ts` | `test/DauTrangInspector.test.tsx` |
| `R-TLMI-080` | CẢ HAI | P1 | Bỏ tick cả bảy dòng thì khối không in gì và đây không phải lỗi | `components/inspector/DauTrangInspector.tsx · helpers/keThua.ts` | `test/DauTrangInspector.test.tsx` |
| `R-TLMI-081` | FE | P1 | Mỗi dòng tick hiển thị kèm giá trị thật của chi nhánh ghi t… | `components/inspector/DauTrangInspector.tsx · helpers/keThua.ts` | `test/DauTrangInspector.test.tsx` |
| `R-TLMI-082` | CẢ HAI | P1 | Logo là một trong bảy ô tick mà mẫu sửa riêng được | `components/inspector/DauTrangInspector.tsx · helpers/keThua.ts` | `test/DauTrangInspector.test.tsx` |
| `R-TLMI-085` | CẢ HAI | P1 | Nội dung tiêu đề mặc định là tên loại chứng từ, không trống… | `components/inspector/TieuDeInspector.tsx` | `test/TieuDeInspector.test.tsx` |
| `R-TLMI-086` | CẢ HAI | P1 | Cỡ chữ tiêu đề là số nguyên 10–36, mặc định 18, độc lập với… | `components/inspector/TieuDeInspector.tsx` | `test/TieuDeInspector.test.tsx` |
| `R-TLMI-087` | CẢ HAI | P1 | Căn của khối Tiêu đề áp cho cả dòng tiêu đề và dòng ngày tháng | `components/inspector/TieuDeInspector.tsx` | `test/TieuDeInspector.test.tsx` |
| `R-TLMI-088` | CẢ HAI | P1 | IN HOA = Có thì in toàn chữ hoa, = Không thì in đúng như gõ | `components/inspector/TieuDeInspector.tsx` | `test/TieuDeInspector.test.tsx` |
| `R-TLMI-089` | CẢ HAI | P2 | In đậm của khối Tiêu đề, mặc định Có | `components/inspector/TieuDeInspector.tsx` | `test/TieuDeInspector.test.tsx` |
| `R-TLMI-090` | CẢ HAI | P1 | Dòng ngày tháng in ngay dưới tiêu đề, chữ nghiêng, lấy ngày… | `components/inspector/TieuDeInspector.tsx` | `test/TieuDeInspector.test.tsx` |
| `R-TLMI-091` | CẢ HAI | P1 | Số chứng từ không thuộc khối Tiêu đề, muốn in phải đưa vào … | `components/inspector/TieuDeInspector.tsx` | `test/TieuDeInspector.test.tsx` |
| `R-TLMI-092` | CẢ HAI | P1 | Mỗi khối Bảng ứng đúng một lưới trên form, đúng và đủ cột c… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-093` | CẢ HAI | P0 | Cột thêm vào lưới ở phiên bản sau tự xuất hiện cuối bảng và… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-094` | CẢ HAI | P2 | Tên bảng trống thì không in tên bảng, có nội dung thì in mộ… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-095` | CẢ HAI | P2 | Tên bảng mặc định trống cho lưới đầu tiên, bằng tên lưới ch… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-096` | CẢ HAI | P1 | In cột STT = Có thì thêm cột đầu tiên đánh số 1, 2, 3… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-097` | CẢ HAI | P1 | Dòng Cộng = Có thì dòng cuối bảng in "Tổng:" và tổng các cộ… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-098` | CẢ HAI | P1 | Dòng Cộng = Không thì không có dòng này và các cột tick Cộn… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-099` | CẢ HAI | P1 | Lặp tiêu đề mỗi trang khi bảng tràn trang | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-100` | CẢ HAI | P2 | Kẻ ô Đầy đủ / Kẻ ngang | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-101` | CẢ HAI | P1 | Tên cột dữ liệu lấy theo đặc tả form và chỉ đọc | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-102` | CẢ HAI | P1 | Tên hiển thị của cột không trống, tối đa 100 ký tự, mặc địn… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-103` | CẢ HAI | P1 | Ô tick in của cột, mặc định Có; bỏ tick thì bỏ cột và các c… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-104` | CẢ HAI | P1 | Khối Bảng đang bật phải giữ lại ít nhất một cột hiển thị | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-105` | CẢ HAI | P2 | Căn của cột áp cho cả tiêu đề cột và dữ liệu; mặc định cột … | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-106` | CẢ HAI | P1 | Chỉ cột số mới có ô Cộng; cột chữ thì ô Cộng ẩn tĩnh | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-107` | CẢ HAI | P1 | Cộng mặc định Có với cột tiền, Không với cột khác | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-108` | CẢ HAI | P1 | Độ rộng cột là số nguyên 3–90, bắt buộc với cột đang tick in | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-109` | CẢ HAI | P1 | Độ rộng mặc định lấy theo tỷ lệ độ rộng cột trên lưới form,… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-110` | FE | P2 | Tổng độ rộng khác 100 thì dòng tổng dưới lưới cột báo số hi… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-111` | CẢ HAI | P1 | Lưu mà tổng độ rộng khác 100 thì hệ thống tự chia lại về 10… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-112` | CẢ HAI | P1 | Cột bỏ tick in không tính vào tổng và giữ nguyên số đang có | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-113` | CẢ HAI | P1 | Tick lại một cột đang có độ rộng trống thì cột nhận phần ch… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-114` | CẢ HAI | P1 | Thuật toán chia đều về 100% — công thức, làm tròn, số dư, s… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-115` | FE | P1 | Kéo thả đổi thứ tự cột; mặc định theo thứ tự cột trên lưới … | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-116` | FE | P2 | Ô Tìm cột lọc theo Tên cột dữ liệu và Tên hiển thị, không p… | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-117` | FE | P2 | Đang lọc ở ô Tìm cột thì không cho kéo thả cột | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-118` | FE | P1 | Lọc ở ô Tìm cột không đổi thiết lập của cột bị ẩn khỏi lưới | `components/inspector/BangInspector.tsx · helpers/doRongCot.ts` | `test/doRongCot.test.ts` |
| `R-TLMI-120` | FE | P1 | Bấm Thêm khối tự do mở hộp Đặt tên khối với tên gợi ý | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-121` | CẢ HAI | P1 | Tên khối tự do không trống, tối đa 60 ký tự | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-122` | CẢ HAI | P1 | Khối tự do mới đặt ngay trước khối Chữ ký | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-123` | CẢ HAI | P1 | Khối tự do mới là lưới 1 dòng × 2 cột toàn ô trống | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-124` | FE | P2 | Thêm khối tự do thành công thì báo, mở bảng chỉnh và chọn s… | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-125` | CẢ HAI | P1 | Mỗi mẫu tối đa 10 khối tự do | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-126` | CẢ HAI | P1 | Tên khối tự do không in ra bản in | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-127` | FE | P1 | Sửa tên khối tự do sau khi tạo | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-128` | FE | P2 | Bảng chỉnh khối tự do không có ô Kích thước lưới và không c… | `components/inspector/KhoiTuDoInspector.tsx · components/modal/HopDatTenKhoiModal.tsx` | `test/KhoiTuDoInspector.test.tsx` |
| `R-TLMI-129` | CẢ HAI | P1 | Mỗi khối tự do tối đa 20 dòng | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-130` | CẢ HAI | P1 | Mỗi khối tự do tối đa 6 cột | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-131` | CẢ HAI | P1 | Các cột của khối tự do rộng bằng nhau, không đặt độ rộng riêng | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-132` | FE | P2 | Bấm ô để chọn ô; giữ Shift và bấm ô khác để chọn một vùng c… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-133` | FE | P1 | Thêm dòng trên/dưới, cột trái/phải ngay cạnh ô đang chọn, ô… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-134` | FE | P1 | Xóa dòng / Xóa cột xóa các dòng, cột mà vùng chọn phủ | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-135` | FE | P1 | Khối tự do còn 1 dòng hoặc 1 cột thì nút − Dòng / − Cột mờ | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-136` | FE | P1 | Chọn từ 2 ô rồi bấm Gộp ô thì vùng đó thành một ô nhiều dòn… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-137` | FE | P1 | Vùng chọn chạm vào ô đã gộp thì tự nới ra cho trọn ô gộp đó | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-138` | FE | P1 | Vùng gộp có từ 2 ô có nội dung thì hỏi trước khi gộp | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-139` | FE | P1 | Gộp ô giữ nội dung của ô đầu tiên có nội dung, các ô còn lạ… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-140` | FE | P1 | Tách ô trả về các ô đơn, nội dung ở ô góc trên trái | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-141` | FE | P1 | Xóa dòng / cột đi qua một ô gộp thì ô gộp được tách trước r… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-142` | FE | P1 | Thêm dòng / cột vào giữa một ô gộp thì ô gộp rộng thêm một … | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-143` | CẢ HAI | P1 | Ô trống không in gì, chỉ chiếm chỗ để các ô khác thẳng hàng | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-144` | CẢ HAI | P1 | Ô là một trường của form thì in dạng `Tên hiển thị: Giá trị` | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-145` | CẢ HAI | P1 | Tên hiển thị của trường bị xóa trống thì chỉ in giá trị, kh… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-146` | CẢ HAI | P1 | Ô Chữ tự do in đúng chữ người dùng gõ, không có giá trị kèm… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-147` | CẢ HAI | P1 | Gõ Chữ tự do ngay trong ô trên trang xem trước, tối đa 255 … | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-148` | FE | P1 | Chọn Chữ tự do mà rời ô khi chưa gõ thì ô tự về Ô trống, kh… | `helpers/luoiTuDo.ts · components/LuoiTuDo.tsx` | `test/luoiTuDo.test.ts` |
| `R-TLMI-149` | FE | P1 | Kéo một dòng trường ở bảng chỉnh thả vào một ô để đặt trườn… | `components/LuoiTuDo.tsx · components/modal/HopChonTruongO.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-150` | FE | P1 | Nháy đúp ô mở hộp chọn cạnh ô, hai mục đầu là (Ô trống) và … | `components/LuoiTuDo.tsx · components/modal/HopChonTruongO.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-151` | FE | P2 | Gõ chữ trong hộp chọn trường thì lọc kho trường không phân … | `components/LuoiTuDo.tsx · components/modal/HopChonTruongO.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-152` | FE | P1 | Một trường chỉ ở một ô trong một khối; đặt lại vào ô khác t… | `components/LuoiTuDo.tsx · components/modal/HopChonTruongO.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-153` | CẢ HAI | P1 | Cùng một trường được dùng ở nhiều khối tự do khác nhau thì … | `components/LuoiTuDo.tsx · components/modal/HopChonTruongO.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-154` | FE | P1 | Kéo một ô có nội dung thả lên ô khác thì hai ô đổi nội dung… | `components/LuoiTuDo.tsx · components/modal/HopChonTruongO.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-155` | FE | P1 | Xóa nội dung (phím Delete) đưa các ô đang chọn về ô trống | `components/LuoiTuDo.tsx · components/modal/HopChonTruongO.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-156` | CẢ HAI | P1 | Tên hiển thị và In đậm là thuộc tính CỦA TRƯỜNG, dùng chung… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-157` | CẢ HAI | P1 | Tên hiển thị của trường tối đa 255 ký tự, mặc định bằng tên… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-158` | CẢ HAI | P1 | Ô trường + In đậm = Có thì chỉ đậm Tên hiển thị, giá trị lu… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-159` | CẢ HAI | P1 | Ô Chữ tự do + In đậm = Có thì đậm cả chữ | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-160` | CẢ HAI | P2 | Nghiêng áp cho cả ô (nhãn và giá trị) | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-161` | CẢ HAI | P1 | Căn Trái / Giữa / Phải trong khối tự do đặt theo ô, không t… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-162` | FE | P1 | Chưa chọn ô nào thì mọi nút trên thanh công cụ khối tự do đ… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-163` | FE | P1 | Bấm In đậm / Nghiêng / Căn áp cho ô hoặc vùng đang chọn | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-164` | CẢ HAI | P1 | Trường chưa được đặt vào ô nào thì Tên hiển thị và In đậm c… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-165` | CẢ HAI | P1 | Kho trường = mọi ô trên form trừ cột trong các lưới | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-166` | FE | P2 | Kho trường là một danh sách phẳng, không chia nhóm, theo th… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-167` | CẢ HAI | P1 | Ô mới ở phiên bản sau tự vào kho trường nhưng không tự chen… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-168` | FE | P1 | Ô Tìm kiếm của khối tự do lọc theo tên trường và Tên hiển t… | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-169` | FE | P1 | Cột Trường dữ liệu trong bảng chỉnh khối tự do luôn chỉ đọc | `components/inspector/KhoiTuDoInspector.tsx · helpers/truongDungChung.ts` | `test/truongDungChung.test.ts` |
| `R-TLMI-170` | FE | P1 | Thanh công cụ khối tự do chỉ hiện khi đang chọn một khối tự do | `components/ThanhCongCuTuDo.tsx · components/MenuChuotPhaiO.tsx` | `test/ThanhCongCuTuDo.test.tsx` |
| `R-TLMI-171` | FE | P1 | Menu chuột phải trên ô khối tự do có cùng tác dụng với than… | `components/ThanhCongCuTuDo.tsx · components/MenuChuotPhaiO.tsx` | `test/ThanhCongCuTuDo.test.tsx` |
| `R-TLMI-172` | FE | P1 | Ô đang chọn là Chữ tự do thì lệnh đầu menu là "Sửa chữ" | `components/ThanhCongCuTuDo.tsx · components/MenuChuotPhaiO.tsx` | `test/ThanhCongCuTuDo.test.tsx` |
| `R-TLMI-173` | FE | P2 | Phím tắt trong lưới: mũi tên, Delete, Enter / F2 | `components/ThanhCongCuTuDo.tsx · components/MenuChuotPhaiO.tsx` | `test/ThanhCongCuTuDo.test.tsx` |
| `R-TLMI-174` | FE | P1 | Gộp ô và Tách ô bật/tắt theo vùng chọn | `components/ThanhCongCuTuDo.tsx · components/MenuChuotPhaiO.tsx` | `test/ThanhCongCuTuDo.test.tsx` |
| `R-TLMI-175` | FE | P1 | Xóa khối tự do thì hỏi trước | `components/ThanhCongCuTuDo.tsx · components/MenuChuotPhaiO.tsx` | `test/ThanhCongCuTuDo.test.tsx` |
| `R-TLMI-176` | CẢ HAI | P1 | Khối tự do đang bật mà mọi ô đều trống thì vẫn lưu được | `components/ThanhCongCuTuDo.tsx · components/MenuChuotPhaiO.tsx` | `test/ThanhCongCuTuDo.test.tsx` |
| `R-TLMI-177` | FE | P2 | Bật Hiện lưới căn chỉnh thì kẻ đường phân ô và gợi ý ở ô tr… | `components/LuoiTuDo.tsx · components/BanInPaper.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-178` | CẢ HAI | P0 | Dấu hiệu của lưới căn chỉnh không in và không xuất PDF | `components/LuoiTuDo.tsx · components/BanInPaper.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-179` | FE | P2 | Bỏ tick Hiện lưới căn chỉnh thì trang xem trước hiển thị đú… | `components/LuoiTuDo.tsx · components/BanInPaper.tsx` | `test/LuoiTuDo.test.tsx` |
| `R-TLMI-182` | CẢ HAI | P1 | Danh sách ô ký gồm 5 chức danh của Thiết lập người ký và cá… | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-183` | CẢ HAI | P1 | Thứ tự ô ký mặc định và kéo thả đổi được | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-184` | CẢ HAI | P1 | Mặc định bật Người lập phiếu, Kế toán trưởng, Giám đốc; tắt… | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-185` | CẢ HAI | P1 | Cột chức danh chỉ đọc; ô ký tự do mang nhãn "tự do" | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-186` | CẢ HAI | P1 | Chức danh có sẵn: Tên người ký lấy từ Thiết lập người ký, c… | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-187` | CẢ HAI | P1 | Ô ký tự do: Tên người ký trống, gõ tay được, có nút xóa | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-188` | CẢ HAI | P1 | Tiêu đề in ra bắt buộc, mặc định là Tiêu đề người ký của Th… | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-189` | CẢ HAI | P1 | Ô ký tự do đang bật phải có tiêu đề in ra không trống, tối … | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-190` | CẢ HAI | P1 | Dòng ghi chú mặc định "(Ký, họ tên)", riêng Giám đốc "(Ký, … | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-191` | CẢ HAI | P1 | Ô tick của ô ký quyết định in hay không in ô ký đó | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-192` | CẢ HAI | P0 | Ô ký tự do xóa được; chức danh của Thiết lập người ký chỉ t… | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-193` | CẢ HAI | P1 | Thêm ô ký tự do — không giới hạn số ô ký | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-196` | CẢ HAI | P1 | In tên người ký theo cờ "In tên người ký trên chứng từ, báo… | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-197` | CẢ HAI | P1 | Dòng "Ngày … tháng … năm …" in nghiêng căn phải phía trên c… | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-198` | CẢ HAI | P2 | Chỗ trống ký Thấp / Vừa / Cao, mặc định Vừa | `components/inspector/ChuKyInspector.tsx` | `test/ChuKyInspector.test.tsx` |
| `R-TLMI-201` | FE | P1 | Cột trái là Bố cục mẫu: danh sách khối theo thứ tự in, kéo … | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-202` | FE | P1 | Mục đầu danh sách là "Thiết lập mẫu", không phải khối, khôn… | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-203` | FE | P2 | Dòng khối chỉ có biểu tượng kéo, con mắt, tên khối (và nút … | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-204` | FE | P1 | Kéo biểu tượng ⠿ của dòng khối để đổi thứ tự khối (= thứ tự… | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-205` | FE | P1 | Kéo khối ngay trên trang xem trước cho cùng kết quả với kéo… | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-206` | FE | P1 | Mọi khối, kể cả Thông tin đầu trang và Chữ ký, đều kéo được | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-207` | CẢ HAI | P1 | Con mắt của khối = Có thì khối được in ra; mặc định Có | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-208` | CẢ HAI | P1 | Con mắt = Không thì khối không in và các khối sau dồn lên | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-209` | CẢ HAI | P1 | Tắt con mắt không mất thiết lập bên trong khối | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-210` | CẢ HAI | P0 | Khối chuẩn không xóa được, chỉ ẩn được; nút xóa ẩn hẳn | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-211` | FE | P1 | Khối tự do có nút xóa ở cả Bố cục mẫu lẫn bảng chỉnh | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-212` | CẢ HAI | P1 | Tên khối chuẩn cố định; khối Bảng đặt tên "Bảng \<tên lưới\>" | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-213` | FE | P2 | Bấm một dòng khối thì bảng chỉnh mở đúng khối đó và khối đư… | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-214` | FE | P2 | Bấm một khối trên trang xem trước thì bảng chỉnh mở đúng kh… | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-215` | FE | P2 | Rê chuột lên một khối trên trang xem trước thì hiện nhãn tê… | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-216` | FE | P1 | Chỉ bảng chỉnh bên phải đổi theo khối đang chọn; cột trái, … | `components/BoCucMauPane.tsx` | `test/BoCucMauPane.test.tsx` |
| `R-TLMI-217` | FE | P1 | Trang xem trước vẽ trang đầu bằng dữ liệu thật của chứng từ… | `components/ThanhXemTruoc.tsx · components/XemTruocPane.tsx` | `test/ThanhXemTruoc.test.tsx` |
| `R-TLMI-218` | FE | P1 | Bất kỳ thay đổi nào trên màn thì trang xem trước vẽ lại ngay | `components/ThanhXemTruoc.tsx · components/XemTruocPane.tsx` | `test/ThanhXemTruoc.test.tsx` |
| `R-TLMI-219` | FE | P1 | Không có chế độ dữ liệu mẫu và không chọn được chứng từ khác | `components/ThanhXemTruoc.tsx · components/XemTruocPane.tsx` | `test/ThanhXemTruoc.test.tsx` |
| `R-TLMI-220` | FE | P1 | Trang xem trước vẽ theo nhóm Giấy và chữ của mẫu, kể cả hướ… | `components/ThanhXemTruoc.tsx · components/XemTruocPane.tsx` | `test/ThanhXemTruoc.test.tsx` |
| `R-TLMI-221` | FE | P2 | Thu / Phóng / Vừa khung chỉ đổi tỷ lệ nhìn, không ảnh hưởng… | `components/ThanhXemTruoc.tsx · components/XemTruocPane.tsx` | `test/ThanhXemTruoc.test.tsx` |
| `R-TLMI-222` | FE | P1 | Hiện lưới căn chỉnh chỉ trên màn, không lưu, mặc định Có | `components/ThanhXemTruoc.tsx · components/XemTruocPane.tsx` | `test/ThanhXemTruoc.test.tsx` |
| `R-TLMI-223` | FE | P1 | Hoàn tác / Làm lại nằm trên thanh Xem trước, nhớ tối đa 60 … | `hooks/mauInStore.ts · components/ThanhXemTruoc.tsx` | `test/mauInStore.test.ts` |
| `R-TLMI-224` | FE | P1 | Mỗi thao tác đổi mẫu là một bước; gõ chữ trong một ô tính m… | `hooks/mauInStore.ts · components/ThanhXemTruoc.tsx` | `test/mauInStore.test.ts` |
| `R-TLMI-225` | FE | P1 | Đóng màn thì lịch sử Hoàn tác / Làm lại bị xóa | `hooks/mauInStore.ts · components/ThanhXemTruoc.tsx` | `test/mauInStore.test.ts` |
| `R-TLMI-226` | FE | P2 | Hết bước Hoàn tác (hoặc Làm lại) thì nút tương ứng mờ | `hooks/mauInStore.ts · components/ThanhXemTruoc.tsx` | `test/mauInStore.test.ts` |
| `R-TLMI-227` | FE | P2 | Ctrl+Z / Ctrl+Y tương đương Hoàn tác / Làm lại | `hooks/mauInStore.ts · components/ThanhXemTruoc.tsx` | `test/mauInStore.test.ts` |
| `R-TLMI-228` | FE | P1 | Thanh Xem trước luôn hiện ở mọi khối đang chọn | `hooks/mauInStore.ts · components/ThanhXemTruoc.tsx` | `test/mauInStore.test.ts` |
| `R-TLMI-229` | FE | P1 | Trang xem trước là nơi thao tác với lưới khối tự do | `hooks/mauInStore.ts · components/ThanhXemTruoc.tsx` | `test/mauInStore.test.ts` |
| `R-TLMI-230` | FE | P1 | Rời một ô thì kiểm tra ngay ô đó, không có mục kiểm tra riêng | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-231` | FE | P1 | Ô không hợp lệ được đánh dấu tại chỗ kèm nội dung thông báo… | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-232` | FE | P1 | Khối chứa ô lỗi được đánh dấu ở hai nơi: dòng khối và khối … | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-233` | FE | P2 | Rê chuột lên dòng khối hoặc khối đang lỗi thì hiện nội dung… | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-234` | FE | P1 | Sửa đúng thì các dấu hiệu lỗi tắt ngay | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-235` | FE | P1 | Ô lưới khối tự do không hợp lệ thì viền đỏ ngay trên trang … | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-236` | CẢ HAI | P1 | Ô trống trong khối tự do không bao giờ là lỗi | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-237` | CẢ HAI | P1 | Xét lỗi trong khối tự do chỉ xét ô có nội dung | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-238` | CẢ HAI | P1 | Không có cảnh báo mềm cho lựa chọn hợp lệ nhưng bất thường | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-239` | CẢ HAI | P0 | Bảng kiểm tra dữ liệu 17 dòng — tầng và thời điểm kiểm tra | `helpers/kiemTraMau.ts` | `test/kiemTraMau.test.ts` |
| `R-TLMI-240` | FE | P1 | Nhãn trạng thái "Đã lưu" và nút Lưu mờ | `components/BadgeTrangThai.tsx · pages/ThietLapMauInScreen.tsx` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-241` | FE | P1 | Nhãn trạng thái "Chưa lưu" | `components/BadgeTrangThai.tsx · pages/ThietLapMauInScreen.tsx` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-242` | FE | P1 | Nhãn trạng thái "Có lỗi" | `components/BadgeTrangThai.tsx · pages/ThietLapMauInScreen.tsx` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-243` | CẢ HAI | P0 | Có lỗi mà bấm Lưu thì không ghi, chỉ báo lỗi đầu tiên theo … | `components/BadgeTrangThai.tsx · pages/ThietLapMauInScreen.tsx` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-244` | FE | P1 | Báo lỗi đầu tiên thì mở bảng chỉnh của khối đó và đưa con t… | `components/BadgeTrangThai.tsx · pages/ThietLapMauInScreen.tsx` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-245` | FE | P2 | Tiêu đề màn và vị trí nhãn trạng thái, nút Lưu | `components/BadgeTrangThai.tsx · pages/ThietLapMauInScreen.tsx` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-248` | CẢ HAI | P1 | Lưu thành công thì báo, màn giữ nguyên, nhãn trạng thái về … | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-249` | CẢ HAI | P0 | Lưu gặp lỗi hệ thống thì rollback, giữ nguyên màn và báo lỗi | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-250` | FE | P2 | Ctrl+S tương đương bấm Lưu | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-251` | FE | P0 | Đóng hoặc Esc khi mẫu khác bản đã lưu thì hỏi với ba lựa chọn | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-252` | FE | P0 | Chọn "Lưu và đóng" thì chạy Lưu, thành công mới đóng | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-253` | FE | P0 | Chọn "Không lưu" thì bỏ mọi thay đổi và đóng | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-254` | FE | P1 | Chọn "Ở lại" thì giữ màn | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-255` | FE | P1 | Không có thay đổi mà bấm Đóng / Esc thì đóng ngay, không hỏi | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-256` | FE | P1 | Đang mở một hộp thoại con thì phím Esc không tác dụng với m… | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-257` | FE | P2 | Chân màn: Đóng ở góc trái; Đặt lại mẫu chuẩn · Lưu ở góc phải | `pages/ThietLapMauInScreen.tsx · hooks/useLuuMau.ts` | `test/ThietLapMauInScreen.test.tsx` |
| `R-TLMI-260` | CẢ HAI | P1 | Chưa có bản ghi mẫu thì in theo mẫu chuẩn hệ thống và báo m… | `components/BanInPaper.tsx · components/modal/XemTruocBanInModal.tsx` | `test/BanInPaper.test.tsx` |
| `R-TLMI-261` | CẢ HAI | P0 | Nút In bị disable theo hai quy tắc cấm in thì cả menu In kh… | `components/BanInPaper.tsx · components/modal/XemTruocBanInModal.tsx` | `test/BanInPaper.test.tsx` |
| `R-TLMI-268` | FE | P1 | Mở màn xem trước bản in như các mẫu cố định | `components/BanInPaper.tsx · components/modal/XemTruocBanInModal.tsx` | `test/BanInPaper.test.tsx` |
| `R-TLMI-269` | FE | P0 | Màn xem trước có nút Sửa mẫu khi người dùng có quyền | `components/BanInPaper.tsx · components/modal/XemTruocBanInModal.tsx` | `test/BanInPaper.test.tsx` |
| `R-TLMI-270` | CẢ HAI | P0 | Lỗi hệ thống khi dựng bản in thì báo và không mở màn xem trước | `components/BanInPaper.tsx · components/modal/XemTruocBanInModal.tsx` | `test/BanInPaper.test.tsx` |

---

## 2. 34 luật thuần `BE` — **ngoài phạm vi kế hoạch FE này**

| Luật | Tên | Thuộc plan |
|---|---|---|
| `R-TLMI-001` | Một mẫu tùy chỉnh cho mỗi cặp (loại chứng từ, nghiệp vụ) | `/plan-be` |
| `R-TLMI-004` | Khóa duy nhất `(TenantId, MaChucNang, MaNghiepVu)` | `/plan-be` |
| `R-TLMI-005` | Mẫu dùng chung mọi người dùng và mọi chi nhánh | `/plan-be` |
| `R-TLMI-006` | Mỗi cặp có đúng một mẫu chuẩn hệ thống, sinh từ đặc tả form | `/plan-be` |
| `R-TLMI-021` | Lưu khi mẫu bằng mẫu chuẩn thì **xóa bản ghi** (chốt **C02**) | `/plan-be` |
| `R-TLMI-022` | Lưu thành công thì mọi lần in sau dùng mẫu mới ngay | `/plan-be` |
| `R-TLMI-034` | Gọi thẳng API mà không có quyền thì server chặn | `/plan-be` |
| `R-TLMI-035` | Có quyền ở một chi nhánh là sửa được mẫu dùng chung | `/plan-be` |
| `R-TLMI-037` | Ô theo chung ghi **trống (NULL)** khi Lưu | `/plan-be` ⚠ FE **phải** gửi payload vắng khoá (D5) |
| `R-TLMI-038` | Ô theo chung đọc lại thiết lập chung **tại thời điểm in** | `/plan-be` |
| `R-TLMI-039` | Ô riêng giữ giá trị của mẫu | `/plan-be` |
| `R-TLMI-047` | Ba quy tắc in chứng từ luôn theo thiết lập chung | `/plan-be` |
| `R-TLMI-048` | Mục "Bố cục mặc định của báo cáo" KHÔNG áp cho chứng từ | `/plan-be` |
| `R-TLMI-049` | Định dạng khối đầu trang luôn theo thiết lập chung | `/plan-be` |
| `R-TLMI-058` · `059` · `060` | Hướng `Tự động` / `Dọc` / `Ngang` khi dựng bản in | `/plan-be` |
| `R-TLMI-064` · `065` | Màu chữ là giá trị riêng; áp cho chữ và đường kẻ, trừ logo | `/plan-be` (FE vẽ theo) |
| `R-TLMI-075` | Hình nền in dưới mọi khối | `/plan-be` (FE vẽ theo) |
| `R-TLMI-078` · `083` · `084` | Nội dung / thứ tự / lặp trang của khối đầu trang | `/plan-be` |
| `R-TLMI-119` | Cộng gộp mặt hàng áp **trước** khi dựng bảng (chốt **C01** · **C30**) | `/plan-be` |
| `R-TLMI-199` | Khối Chữ ký đọc hồ sơ đơn vị của chi nhánh nào (chốt **C05**) | `/plan-be` |
| `R-TLMI-246` · `247` · `248` · `249` | Kiểm lại ở server · transaction · báo · rollback | `/plan-be` |
| `R-TLMI-258` | Hai người cùng sửa một mẫu (chốt **C06**) | `/plan-be` |
| `R-TLMI-259` · `262` · `263` · `264` · `265` · `266` · `267` · `271` | Dựng bản in | `/plan-be` |

⚠ **Luật `CẢ HAI` là ranh giới FE-BE**, không phải chỗ để chia việc. FE kiểm để người dùng biết sớm,
BE kiểm để dữ liệu không vào sai. **Bỏ ở FE vì "BE đã chặn rồi" là sai; bỏ ở BE vì "FE đã chặn rồi"
còn sai hơn.**

---

## 3. Danh sách kiểm thử — 13 file

### 3.1 Quy ước bắt buộc (để `trace.sh` đếm được)

```ts
// @vitest-environment node        ← chỉ cho *.test.ts (helpers / store)
it('R-TLMI-114 · chia đều 40/40/40 thành 33/33/34', () => { … })
```

- Mỗi `it()` mở đầu bằng **chính mã luật** `R-TLMI-nnn`, rồi dấu `·`, rồi mô tả tiếng Việt.
- Một `it()` phủ **một** luật. Luật cần nhiều ca ⇒ nhiều `it()` cùng mã, khác mô tả.
- Test **không** import barrel `@base` (luật `client/CLAUDE.md §13`) — import thẳng file.
- Test logic thuần ⇒ `*.test.ts` + docblock `// @vitest-environment node`.
- Test cần DOM ⇒ `*.test.tsx`, **chỉ** cho `components/` và `pages/`.

### 3.2 Bảng file test

| # | File | Môi trường | Luật phủ | Chi tiết ca |
|---|---|---|---|---|
| 1 | `test/luoiTuDo.test.ts` | `node` | `123, 129…143, 148, 152…155, 180, 181` | [`05` §14](05-khoi-tu-do-luoi-o.md) |
| 2 | `test/doRongCot.test.ts` | `node` | `108…114, 118` | [`04` §9](04-panel-bang.md) |
| 3 | `test/keThua.test.ts` | `node` | `036, 039, 040, 042, 049, 053` | [`02` §8](02-panel-thiet-lap-mau.md) |
| 4 | `test/kiemTraMau.test.ts` | `node` | `057, 061, 063, 230…239, 243` | [`02` §8](02-panel-thiet-lap-mau.md) |
| 5 | `test/chuanHoaMau.test.ts` | `node` | `018, 019, 037, 164` | [`01` §10](01-modal-thiet-lap-mau-in.md) |
| 6 | `test/mauChuan.test.ts` | `node` | `002, 003, 007…010, 013, 093, 167` | §3.3 dưới |
| 7 | `test/truongDungChung.test.ts` | `node` | `156…161, 164` | [`05` §14](05-khoi-tu-do-luoi-o.md) |
| 8 | `test/mauInStore.test.ts` | `node` | `041, 223…227` | [`01` §10](01-modal-thiet-lap-mau-in.md) |
| 9 | `test/ThietLapMauInScreen.test.tsx` | DOM | `015…020, 240…245, 250…257` | [`01` §10](01-modal-thiet-lap-mau-in.md) |
| 10 | `test/BoCucMauPane.test.tsx` | DOM | `120, 125, 201…216, 232` | [`01` §10](01-modal-thiet-lap-mau-in.md) |
| 11 | `test/ThanhXemTruoc.test.tsx` | DOM | `044, 179, 221, 222, 226, 228` | [`01` §10](01-modal-thiet-lap-mau-in.md) |
| 12 | `test/LuoiTuDo.test.tsx` | DOM | `131, 132, 144…151, 161, 173, 177…179, 235, 236` | [`05` §14](05-khoi-tu-do-luoi-o.md) |
| 13 | `test/ThanhCongCuTuDo.test.tsx` | DOM | `138, 162, 163, 170…176` | [`05` §14](05-khoi-tu-do-luoi-o.md) |
| 14 | `test/KhoiTuDoInspector.test.tsx` | DOM | `120…128, 166…169, 175, 211` | [`05` §14](05-khoi-tu-do-luoi-o.md) |
| 15 | `test/riengCuaMau.test.tsx` | DOM | `050…052, 054…056, 062, 066…075` | [`02` §8](02-panel-thiet-lap-mau.md) |
| 16 | `test/DauTrangInspector.test.tsx` | DOM | `043, 076, 077, 079…083` | [`03` §6](03-panel-dau-trang-va-tieu-de.md) |
| 17 | `test/TieuDeInspector.test.tsx` | DOM | `085…091` | [`03` §6](03-panel-dau-trang-va-tieu-de.md) |
| 18 | `test/inspectors.test.tsx` | DOM | `092…107, 116, 117` (khối Bảng) | [`04` §9](04-panel-bang.md) |
| 19 | `test/ChuKyInspector.test.tsx` | DOM | `046, 052, 182…198` | [`06` §9](06-panel-chu-ky.md) |
| 20 | `test/NutInChungTu.test.tsx` | DOM | `012, 013, 023…033, 260, 261, 268…270` | [`07` §G](07-loi-vao-va-xem-truoc-ban-in.md) |
| 21 | `test/BanInPaper.test.tsx` | DOM | `143, 178, 180, 181, 262…264` | [`07` §H](07-loi-vao-va-xem-truoc-ban-in.md) |

> Bảng §1 ánh xạ theo **nhóm luật** nên tên file test ở đó gộp hơn bảng này (ví dụ nhóm `092…119` đều
> trỏ `test/doRongCot.test.ts`). Bảng §3.2 là **phân bổ thật** khi code; §1 là bản đồ thô để `trace.sh`
> đối chiếu nhanh. Hai bảng **không mâu thuẫn** — §3.2 chi tiết hơn.

### 3.3 `test/mauChuan.test.ts` — ca chi tiết

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-007 · chưa có bản ghi thì dùng mẫu chuẩn hệ thống` | A1 trả `nguon='CHUAN'`, `mau=null` → store nạp `mauChuan`, badge `Đã lưu` |
| `R-TLMI-008 · mẫu chuẩn có đúng bốn loại khối theo thứ tự cố định` | mẫu chuẩn → `loai` theo đúng thứ tự `DAU_TRANG · TIEU_DE · BANG* · CHU_KY` ⚠ **Q7** |
| `R-TLMI-009 · form n lưới thì mẫu chuẩn có n khối Bảng, mọi lưới bật` | catalog 2 lưới → 2 khối `BANG`, cả hai `hien=true` ⚠ **Q8** |
| `R-TLMI-010 · thông tin chung / tổng tiền phải tự dựng bằng khối tự do` | mẫu chuẩn → **không** có khối `THONG_TIN` hay `TONG_HOP` |
| `R-TLMI-002 · nghiệp vụ = giá trị ô Loại nghiệp vụ trên form` | đổi `maNghiepVu` → `queryKey` đổi |
| `R-TLMI-003 · loại không chia nghiệp vụ thì cả loại là một mẫu` | `maNghiepVu` mặc định của loại → vẫn gửi cặp (Q-16) |
| `R-TLMI-013 · mẫu cố định theo quy định không sửa được` | menu A6 trả mẫu cố định → mục đó không mở được modal thiết lập |
| `R-TLMI-093 · cột thêm ở phiên bản sau tự xuất hiện cuối bảng` | catalog thêm cột → `hopNhatVoiCatalog` đặt cột mới ở **cuối** mảng |
| `R-TLMI-167 · ô mới vào kho trường nhưng không tự chen vào khối tự do` | catalog thêm trường → có trong `khoTruong`, **không** ô nào đổi |
| `C10 · phần tử bị xoá khỏi form: mờ + nhãn, loại khi Lưu` | catalog bỏ cột đang dùng → cột mờ + nhãn `không còn trên form`; payload Lưu **không** có cột đó |

### 3.4 Cổng nghiệm thu

```bash
# Cổng nhẹ — mỗi lô
cd client && npx vitest run src/base/domainKit/mauIn --reporter=dot
cd client && npx vite build

# Cổng đầy đủ — trước khi báo hoàn thành
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test && npm run build
git -C client status --porcelain        # thay cho check:committed (lỗi giả trên Windows)

# Cổng truy vết — BẮT BUỘC
./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec fe
./docs/rules/msg.sh   pmkt-docs/ba/<PYC> fe
```

**Ngưỡng chấp nhận:**

| Kết quả `trace.sh` | Ngưỡng |
|---|---|
| `OK` | ≥ **95 %** của 237 luật |
| `NO-TEST` | ≤ 5 % — chỉ cho luật P2 thuần hiển thị |
| `MISSING` | **0** |
| `VI-PHAM` | **0** |

**Ngưỡng chấp nhận `msg.sh`:** `THIEU` ≤ **5** — đúng 5 chuỗi đã ghi nhận ở L-4 / L-5 (2 tooltip nút In
disable · xung đột phiên bản · thiếu quyền In · câu hướng dẫn nạp lại). Nhiều hơn 5 ⇒ **trượt cổng**.

---

## 4. Sinh lại bảng §1

Máy dev **không có `node` và không có `python` thật** trên `PATH` (`where.exe node` ⇒ không tìm thấy;
`python.exe` là alias của Windows Store). Dùng PowerShell:

```powershell
# Đọc mọi dòng "| R-TLMI-nnn | … | Tầng | Sev | Trạng thái |" trong 02-rules.md,
# lọc Tầng ∈ {FE, CẢ HAI}, ánh xạ số luật -> (file, test) theo nhóm, ghi thẳng vào §1 của chính file này.
# Script đầy đủ: xem lịch sử phiên lập plan (2026-09-19).
```

Kiểm nhanh số liệu:
```bash
grep -c "^| R-TLMI-" docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/02-rules.md   # 271
grep "^| R-TLMI-" docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/02-rules.md \
  | awk -F'|' '{print $4}' | sort | uniq -c                                                  # 34 BE · 129 CẢ HAI · 108 FE
```
