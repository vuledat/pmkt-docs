# Mẫu in chứng từ theo khối — Kịch bản & trạng thái kỳ vọng

| | |
|---|---|
| Nguồn | [02-rules.md](02-rules.md) · hợp đồng [01-hop-dong-json-va-api-v1.md](../mau-in-chung-tu/01-hop-dong-json-va-api-v1.md) |
| Ngày soát | 2026-09-17 |
| Tổng | **55 kịch bản** (`S-001…108`, đánh số theo nhóm luật) |
| Phủ nhóm | happy 19 · biên 11 · ngoại lệ 12 · tương tranh 2 · hồi phục 2 |

> **File này là nguồn sự thật duy nhất để viết test.** Mỗi luật `P0` có ≥1 kịch bản. Tên test mang mã luật
> (`docs/rules/truy-vet-luat.md`). Fixture dùng chung: `docs/doing/mau-in-chung-tu/fixtures/`.

---

## Ma trận

| ID | Nhóm | Điều kiện | Kết quả mong đợi | Luật phủ |
|---|---|---|---|---|
| S-001 | ngoại lệ | user thiếu `HTMauIn.View` vào `/he-thong/thiet-lap-mau-in` | menu ẩn; route → 403 `MSG_COMMON_002`; `GET /api/mau-in/loai-chung-tu` → 403 | R-001 |
| S-002 | ngoại lệ | user có `HTMauIn.View`, thiếu `Edit`, gọi `PUT /api/mau-in/MDV` | 403 `MSG_COMMON_003`, `prn_mau_in_tuy_chinh` không đổi; editor không có nút Lưu | R-002 |
| S-003 | happy | user có `MuaDichVu.View.Detail` mở chi tiết MDV | nút `In \| ˅` hiện; `GET /api/mau-in/MDV/menu?chungTuId=` → `[TUY_CHINH]` | R-003 · R-071 |
| S-004 | ngoại lệ | user thiếu `MuaDichVu.View.Detail` gọi `…/du-lieu-in` | 403; FE không dựng nút In | R-003 |
| S-005 | happy | editor tenant gõ "MDV0000" vào "Chứng từ khác…" | A5 trả ≤20 dòng khớp số CT/diễn giải; thiếu `MuaDichVu.View` → 403 | R-004 · R-067 |
| S-006 | happy | user có `HTMauIn.Edit` mở menu In | có separator + "⚙ Thiết lập mẫu in…" → điều hướng kèm `?chungTuId=&troVe=` | R-005 |
| S-010 | biên | lề trái = 6 · cỡ chữ = 21 · mã màu `#zz0000` · tiêu đề cỡ 40 · rộng nhãn 70 · rộng cột 95 | mỗi giá trị một `loi` với đúng `MSG_MAUIN_001/002/014/017`; FE kẹp ô nhập về biên + toast | R-010 · R-011 · R-012 · R-025 |
| S-011 | ngoại lệ | tiêu đề `"   "` | `loi` `MSG_MAUIN_003`; nút Lưu disabled; Ctrl+S → toast lỗi này; `PUT` → 400 | R-013 · R-027 |
| S-012 | biên | bảng hạch toán 3 cột hiện rộng 30/30/30 | `canhBao` `MSG_MAUIN_004` (90 %); lưu được; sau `chuanHoa` = 33/33/34 (sai số dồn cột cuối) | R-014 · R-026 |
| S-013 | ngoại lệ | tắt hết cột của bảng đang hiện | `loi` `MSG_MAUIN_005` | R-015 |
| S-014 | biên | 4 ô ký đang hiện, tick ô thứ 5 / bấm "+ Thêm ô ký tự do" | FE từ chối + toast `MSG_MAUIN_012`; JSON có 5 ô hiện → BE 400 | R-016 |
| S-015 | happy | ẩn mọi bảng · CHU_KY bật không ô · TU_DO bật không dòng · nền 70 % · ẩn Số chứng từ | 5 `canhBao` `MSG_MAUIN_006/007/008/010/011`; vẫn lưu được | R-017 · R-018 · R-019 · R-021 · R-022 |
| S-016 | ngoại lệ | tên khối tự do rỗng | `loi` `MSG_MAUIN_009` | R-020 |
| S-017 | ngoại lệ | bỏ tick trường cuối cùng của Thông tin chung | FE từ chối + toast BR30 "Phải giữ lại ít nhất 1 trường hiển thị."; JSON như vậy → 400 `MSG_MAUIN_013` | R-023 |
| S-018 | ngoại lệ | PUT JSON có 2 khối TIEU_DE / DON_VI ở vị trí 1 / `nguon` bảng lạ | 400 `MSG_MAUIN_017` với `chiTiet` = JSON Pointer; DB không đổi | R-024 · R-027 · INV-001…005 · INV-008 |
| S-019 | happy | nhãn `"  Nhà cung cấp  "`, màu `#1E3A8A` | lưu xong: `"Nhà cung cấp"`, `#1e3a8a` | R-026 |
| S-020 | happy | tenant chưa tuỳ chỉnh, super admin chưa cấu hình, url super-admin trống | A2 `nguon = MAC_DINH_DONG_GOI`, `hieuLuc` = fixture `mdv.mau-chuan.json` | R-030 · R-094 |
| S-021 | happy | super admin đã lưu MDV v1, tenant chưa tuỳ chỉnh | A2 `nguon = MAC_DINH_HE_THONG`, `macDinh.phienBan = 1` | R-030 · R-090 |
| S-022 | happy | tenant đã tuỳ chỉnh | A2 `nguon = TUY_CHINH`, `phienBan` của bản tenant | R-030 |
| S-023 | happy | S-022 rồi super admin lưu v2 | bản in tenant không đổi; A1/A2 `coMacDinhMoi = true`; FE badge + `MSG_MAUIN_016` | R-031 · R-033 |
| S-024 | happy | PUT lần đầu khi hiệu lực là super admin v1 | bản ghi có `mac_dinh_nguon = MAC_DINH_HE_THONG`, `mac_dinh_phien_ban = 1` | R-032 |
| S-025 | hồi phục | super-admin-service trả 503: (a) cache còn hạn (b) cache stale (c) chưa có cache | (a) dùng cache, không log; (b) dùng stale + 1 WARN; (c) `MAC_DINH_DONG_GOI` + FE `MSG_MAUIN_020` | R-034 |
| S-026 | happy | DELETE bản tuỳ chỉnh | `da_xoa = true`; A2 ngay sau trả `nguon ≠ TUY_CHINH`; A1 `trangThai = MAU_CHUAN` | R-035 |
| S-027 | tương tranh | hai admin cùng mở, A lưu (v1→v2), B lưu với `phienBan = 1` | B nhận 409 `MSG_MAUIN_018`; editor B giữ nguyên | R-036 |
| S-028 | ngoại lệ | `GET /api/mau-in/KKK` (chưa có provider) | 404 `MSG_MAUIN_019`; A1 dòng KKK `hoTro = false`, FE khoá nút | R-037 |
| S-030 | happy | bản lưu có trường `k = 'truongCu'` không còn trong catalog + 1 dòng tự do | trường bị loại (`thayDoi.boTruong = ['truongCu']`), dòng tự do còn, thứ tự còn lại giữ nguyên | R-040 · R-045 |
| S-031 | happy | catalog thêm `k = 'soHopDong'` (a) mẫu đóng gói (b) bản tuỳ chỉnh | (a) thêm cuối THONG_TIN `hien = true`; (b) `hien = false, moi = true`; `thayDoi.themTruong = ['soHopDong']`; FE toast "Có 1 trường mới" | R-041 · R-046 · R-070 |
| S-032 | happy | catalog thêm cột `ghiChu` vào bảng `hachToan` đang có cột rộng 20/30/50 | cột mới cuối bảng, `rong = 33`, `hien` như S-031; sau chuẩn hoá Σ = 100 | R-042 |
| S-033 | happy | catalog thêm bảng `phuPhi` | khối BANG mới ngay trước CHU_KY, `hien = false` | R-043 |
| S-034 | biên | JSON DON_VI thiếu dòng `email`, CHU_KY có `vaiTro = 'THU_KHO'` nhưng catalog MDV không có | thêm dòng `email` `hien = false`; ô THU_KHO bị bỏ; ô tự do giữ | R-044 |
| S-050 | ngoại lệ | kéo BANG thả lên vị trí 0 / kéo DON_VI | `doiViTri` trả nguyên mảng; DON_VI/TIEU_DE không có tay cầm; JSON vi phạm → 400 | R-050 · INV-001 |
| S-051 | happy | bấm eye trên DON_VI / tìm eye trên TIEU_DE | DON_VI ẩn được; TIEU_DE không có eye; JSON `TIEU_DE.hien = false` → chuẩn hoá về true | R-051 |
| S-052 | happy | outline của mẫu chuẩn MDV | chỉ khối TU_DO có ✕; không có nút "thêm bảng"; JSON thiếu TONG_HOP → 400 | R-052 · R-054 · INV-002 |
| S-053 | happy | "+ Thêm khối tự do" ×2, rồi xoá khối 1 | chèn trước CHU_KY; tên "Khối tự do 1/2"; xoá có xác nhận "Xác nhận xóa"; chọn về trang | R-053 · R-065 |
| S-060 | happy | 61 lần đổi nhãn (blur mỗi lần) rồi Ctrl+Z 61 lần | hoàn tác được 60 bước; gõ liên tục 5 ký tự = 1 bước | R-060 · R-068 |
| S-061 | happy | đổi nhãn rồi đổi lại đúng giá trị cũ | tag về "Đã lưu" (dirty so JSON, không đếm thao tác) | R-061 |
| S-062 | happy | Ctrl+S khi hợp lệ · Esc khi không modal | lưu; Esc gọi luồng Đóng | R-062 |
| S-063 | happy | Đóng khi dirty | hộp "Xác nhận đóng" đúng chữ BR3; Xác nhận → về `troVe`; Hủy → ở lại; 2 nút | R-063 |
| S-064 | happy | "Đặt lại mẫu chuẩn" → xác nhận | editor = `macDinh.mau`, dirty = true, chưa có PUT nào | R-064 |
| S-066 | biên | zoom + 8 lần từ 100 % · "Vừa khung" ở canvas 700px với A4 | dừng ở 160 %; fit = min(1,4, 650/794) = 0,82 | R-066 |
| S-067 | happy | chọn "Chứng từ khác…" rồi đổi sang "Dữ liệu mẫu" | giấy đổi số liệu, JSON không đổi, không vào lịch sử undo | R-067 |
| S-071 | happy | menu In của PT (GĐ2) | `[PHIEU_THU_01, BIEN_LAI_06, TUY_CHINH]` + ⚙; PHIEU_THU_01 → `moBanIn` cũ | R-071 |
| S-072 | happy | bấm "Mẫu tùy chỉnh" | A6 → cùng `MauInPaper` → cửa sổ blob, `@page A4 portrait; margin 1cm 1cm 1cm 1.5cm`, `thead` lặp | R-072 · R-073 |
| S-074 | happy | MDV tổng thanh toán 154 000 | `tongHop.soTienBangChu = "Một trăm năm mươi bốn nghìn đồng"` (theo `SoTienBangChu`) | R-074 |
| S-075 | happy | tenant dùng dấu chấm nghìn | 140000 → "140.000"; ngày → `25/08/2026`; giá trị null → ô trống | R-075 |
| S-076 | ngoại lệ | id của chứng từ MUA HÀNG HOÁ gọi qua provider MDV | 404 (đi qua `getDichVu`); dòng có `tienThueGtgt = 0` không vào bảng `thue` | R-076 · C14 |
| S-080 | happy | Tenant có tenDonVi/mst/sđt; `mst_don_vi` GỐC khác tên | đầu trang lấy Tenant; xoá `tenDonVi` → lấy `mst_don_vi` GỐC | R-080 |
| S-081 | biên | diaChiChiTiet "12 Nguyễn Trãi", phường có tên, tỉnh id không tồn tại | "12 Nguyễn Trãi, Phường Thanh Xuân Trung" (không có "null") | R-081 |
| S-082 | happy | Tenant khai 5 người ký, `inTenNguoiKyTrenChungTu = false` | `nguoiKy` đủ 5 vai trò; renderer không in tên dù mẫu `inTen = true` | R-082 |
| S-083 | happy | cờ `layTenNguoiLapPhieuTuNguoiDungDangNhap = true`, user đăng nhập "Nguyễn Văn An" | `nguoiKy.NGUOI_LAP.ten = "Nguyễn Văn An"`; tra không ra → tên đã cấu hình | R-083 |
| S-090 | happy | cell gọi B5 lần 2 với `If-None-Match: "1"` | 304, cache giữ; super admin lưu v2 → lần sau 200 body v2 | R-090 |
| S-091 | ngoại lệ | super admin PUT JSON có cột `k` không trong snapshot | hợp nhất loại bỏ (không lỗi); JSON vi phạm INV → 400 | R-091 |
| S-092 | happy | super admin DELETE MDV | B5 → 404; cell sau TTL: `MAC_DINH_DONG_GOI` | R-092 |
| S-093 | happy | mở màn super admin | header hiện `catalogVersion` của snapshot | R-093 |
| S-094 | happy | boot cell không có `PMKT_SUPER_ADMIN_URL` | 1 dòng INFO; A2 luôn bỏ tầng 2 | R-094 |
| S-040 | ngoại lệ | tài khoản `kiemtra` (không quyền) gọi B1..B4 | 403 tất cả | R-006 |
| S-100 | happy | kéo mép cột `soLuong` (rong 20) sang phải 5 % trong bảng 4 cột 20/30/20/30 | `soLuong` = 25, cột hiện liền kề phải = 25, Σ vẫn 100; một bước Ctrl+Z trả về 20/30 | R-100 |
| S-101 | biên | kéo cột xuống dưới 3 % · kéo cột cuối · kéo khi docChi | dừng ở 3 %; cột cuối bù vào cột hiện bên TRÁI; docChi không có tay cầm | R-100 · INV-005 |
| S-102 | happy | lưu mẫu 3 lần rồi gọi A8 | 3 mục, `ngayTao` giảm dần, phiên bản 3/2/1, không mục nào kèm `cauHinh` | R-101 · R-102 |
| S-103 | happy | A4 xoá bản tuỳ chỉnh rồi mở mục lịch sử mới nhất | mục có `hanhDong = XOA`; A9 trả `mau` = JSON ngay TRƯỚC khi xoá, khôi phục được | R-101 · R-103 |
| S-104 | ngoại lệ | tenant B gọi A8 của loại tenant A vừa lưu · user thiếu `HTMauIn.View` | danh sách rỗng (RLS); thiếu quyền ⇒ 403 `MSG_COMMON_003` | R-102 |
| S-105 | happy | mở A9 của phiên bản lưu trước khi catalog thêm trường `soHopDong` | `mau` trả về có trường mới (`hien = false`) nhờ hợp nhất; bấm Khôi phục ⇒ editor dirty, chưa có PUT nào, toast `MSG_MAUIN_025` | R-103 · R-104 |
| S-106 | biên | lưu 55 lần một loại | bảng lịch sử còn đúng 50 bản mới nhất; bản cũ nhất biến mất | R-105 · INV-009 |
| S-107 | happy | console super admin mở loại có `duLieuMau` · loại không có | ô chọn 2 mục, mặc định "Dữ liệu mẫu"; loại không có ⇒ mục đó mờ, mặc định "Dữ liệu giữ chỗ" | R-106 |
| S-108 | happy | mẫu tắt hết đường kẻ ô, xem trên canvas rồi bấm In thử | canvas thấy kẻ mờ; HTML cửa sổ in không chứa lớp kẻ mờ | R-107 |

---

## Fixture (`docs/doing/mau-in-chung-tu/fixtures/`)

| File | Sinh bởi | Dùng ở |
|---|---|---|
| `mdv.catalog.json` | `XuatCatalogMauInTest` (cell-app) → chép tay | FE test hợp nhất/kiểm tra · super-admin snapshot |
| `mdv.mau-chuan.json` | `MauChuanBuilderTest` snapshot | S-020 · FE render snapshot |
| `mdv.du-lieu-mau.json` | `MdvMauInProviderTest` | FE `MauInPaper.render.test` · S-074/075 |
| `hop-nhat/{01-bo-khoa-la,02-them-truong,03-them-cot,04-them-bang,05-dong-bo-don-vi-chu-ky,06-giu-thu-tu}.{in,out}.json` | viết tay | S-030…034 (Java + TS) |
| `kiem-tra/{do,xanh}/R-MAUIN-0nn.json` | viết tay | S-010…018 (Java + TS) |
| `chuan-hoa/01-chia-lai-100.{in,out}.json` | viết tay | S-012 · S-019 |
