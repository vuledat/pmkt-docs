# Mẫu in chứng từ theo khối — Luật nghiệp vụ nguyên tử

| | |
|---|---|
| Nguồn | mock `ThietLapMauIn.html` · chốt user 2026-09-17 (Q1–Q21) · hợp đồng [01-hop-dong-json-va-api-v1.md](../mau-in-chung-tu/01-hop-dong-json-va-api-v1.md) |
| Ngày soát | 2026-09-17 |
| Tổng | **75 luật** (`R-MAUIN-001…107`, đánh số theo nhóm, có khoảng trống) · **9 bất biến** (`INV-MAUIN-001…009`) |
| Trạng thái | 75 `CHỐT` · 0 `CHỜ` (mọi mục conflict đã đóng) |

> **File này là nguồn sự thật duy nhất để code.** `/plan-be` · `/gen-be` lọc `Tầng = BE|CẢ HAI`; `/plan-fe` ·
> `/gen-fe` lọc `Tầng = FE|CẢ HAI`. Tầng `SA` = chỉ `super-admin-service`/`client-admin` — `trace.sh` **không quét**
> hai codebase đó (chỉ quét `cell-app/src` + `client/src`), nên luật `SA` được ghim bằng test trong chính service
> đó và liệt kê tay ở báo cáo hoàn thành.
>
> Mọi luật `CLOSED-AUTO` (C08 C09 C10 C12 C13 C14) là quyết định ngoài tài liệu → **bắt buộc có test mang mã luật**.

---

## Bảng tổng

| ID | Tên luật | Tầng | Sev | TT | Nguồn |
|---|---|---|---|---|---|
| R-MAUIN-001 | Menu & route Thiết lập mẫu in theo `HTMauIn.View` | CẢ HAI | P1 | CHỐT | BR25 · Q4 |
| R-MAUIN-002 | Lưu / đặt lại mẫu của đơn vị theo `HTMauIn.Edit` | CẢ HAI | P0 | CHỐT | BR25 · Q4 |
| R-MAUIN-003 | Menu in & dữ liệu in theo quyền in của loại chứng từ | CẢ HAI | P0 | CHỐT | BR25 · mock #menuDemo · C08 |
| R-MAUIN-004 | Chọn chứng từ thật để xem thử cần `<ChucNang>.View` | BE | P1 | CHỐT | BR25 · Q9 |
| R-MAUIN-005 | Mục "⚙ Thiết lập mẫu in…" chỉ hiện khi có `HTMauIn.Edit` | FE | P1 | CHỐT | BR25.2 (ẩn nút) · mock |
| R-MAUIN-006 | Super admin: `MauInMacDinh.View · View.Detail · Edit · Delete` | SA | P1 | CHỐT | Q4 · `MaQuyenAdmin` |
| R-MAUIN-010 | Lề 0–5 cm | CẢ HAI | P1 | CHỐT | mock checks() :257 |
| R-MAUIN-011 | Cỡ chữ cơ sở 8–20 pt | CẢ HAI | P1 | CHỐT | mock :258 |
| R-MAUIN-012 | Mã màu chữ `#rrggbb` | CẢ HAI | P1 | CHỐT | mock bindIns colorhex :427 |
| R-MAUIN-013 | Tiêu đề bản in không được trống | CẢ HAI | P0 | CHỐT | mock :259 |
| R-MAUIN-014 | Σ độ rộng cột ≠ 100 % → cảnh báo | CẢ HAI | P2 | CHỐT | mock :261 |
| R-MAUIN-015 | Bảng đang bật phải có ≥1 cột | CẢ HAI | P0 | CHỐT | mock :262 · BR30 |
| R-MAUIN-016 | Tối đa 4 ô ký hiện | CẢ HAI | P1 | CHỐT | mock :462,467 |
| R-MAUIN-017 | Không có bảng chi tiết nào → cảnh báo | CẢ HAI | P2 | CHỐT | mock :263 |
| R-MAUIN-018 | Khối chữ ký bật mà không ô nào → cảnh báo | CẢ HAI | P2 | CHỐT | mock :264 |
| R-MAUIN-019 | Khối tự do bật mà không dòng nào → cảnh báo | CẢ HAI | P2 | CHỐT | mock :265 |
| R-MAUIN-020 | Khối tự do phải có tên | CẢ HAI | P1 | CHỐT | mock :265 |
| R-MAUIN-021 | Nền đậm > 60 % → cảnh báo | CẢ HAI | P2 | CHỐT | mock :266 |
| R-MAUIN-022 | Không hiện Số chứng từ → cảnh báo | CẢ HAI | P2 | CHỐT | mock :267 |
| R-MAUIN-023 | Thông tin chung bật phải còn ≥1 trường hiển thị | CẢ HAI | P0 | CHỐT | BR30 |
| R-MAUIN-024 | JSON vi phạm bất biến cấu trúc → 400 | BE | P0 | CHỐT | hợp đồng §1 |
| R-MAUIN-025 | Giới hạn số: tiêu đề 10–36 pt · rộng nhãn 15–60 % · rộng cột 3–90 % | CẢ HAI | P1 | CHỐT | mock :390,:417 · Q17 |
| R-MAUIN-026 | Chuẩn hoá trước khi lưu: trim, chia lại 100 %, màu chữ thường | CẢ HAI | P1 | CHỐT | mock doSave :488 · BR43 |
| R-MAUIN-027 | Còn lỗi thì không lưu (FE khoá nút, BE 400) | CẢ HAI | P0 | CHỐT | mock :296,:487 |
| R-MAUIN-030 | Giải mẫu hiệu lực theo chuỗi 3 tầng | BE | P0 | CHỐT | D2 |
| R-MAUIN-031 | Bản tuỳ chỉnh thắng tuyệt đối, không merge thay đổi super admin | BE | P0 | CHỐT | D2 |
| R-MAUIN-032 | Lưu bản tuỳ chỉnh ghi `mac_dinh_nguon` + `mac_dinh_phien_ban` | BE | P1 | CHỐT | D2 · hợp đồng §8.1 |
| R-MAUIN-033 | `coMacDinhMoi` khi mẫu super admin mới hơn bản gốc của tenant | CẢ HAI | P1 | CHỐT | D2 · L4 |
| R-MAUIN-034 | Không nối được super-admin: cache còn hạn → dùng; stale → dùng + WARN; chưa có → đóng gói | BE | P1 | CHỐT | D4 · L6 |
| R-MAUIN-035 | Xoá bản tuỳ chỉnh = xoá mềm, đọc lại ra mặc định | BE | P1 | CHỐT | BR29 · A4 |
| R-MAUIN-036 | Khoá lạc quan `phienBan` → 409 `MSG_MAUIN_018` | CẢ HAI | P1 | CHỐT | hợp đồng A3 |
| R-MAUIN-037 | Loại chưa có provider → 404 `MSG_MAUIN_019`; danh sách 47 loại đánh dấu `hoTro=false` | CẢ HAI | P1 | CHỐT | BR4/BR9 · A1 |
| R-MAUIN-040 | Hợp nhất: bỏ khoá không còn trong catalog, giữ dòng tự do | CẢ HAI | P0 | CHỐT | hợp đồng §4.1 |
| R-MAUIN-041 | Hợp nhất: thêm trường mới vào cuối THONG_TIN; `hien` theo nguồn mẫu | CẢ HAI | P0 | CHỐT | mock :400 · Q6 |
| R-MAUIN-042 | Hợp nhất: thêm cột mới vào cuối bảng, rộng = trung bình cột đang hiện | CẢ HAI | P1 | CHỐT | mock :425 · Q6 |
| R-MAUIN-043 | Hợp nhất: bảng catalog chưa có khối → thêm trước CHU_KY, ẩn | CẢ HAI | P1 | CHỐT | Q16 |
| R-MAUIN-044 | Hợp nhất: DON_VI đúng 5 dòng; CHU_KY bỏ vai trò không thuộc catalog | CẢ HAI | P1 | CHỐT | hợp đồng §4.5 |
| R-MAUIN-045 | Hợp nhất không đổi thứ tự phần tử đang có | CẢ HAI | P0 | CHỐT | hợp đồng §4.6 |
| R-MAUIN-046 | Hợp nhất trả `thayDoi` (thêm/bỏ) để FE báo | CẢ HAI | P2 | CHỐT | hợp đồng §4 |
| R-MAUIN-050 | DON_VI ở vị trí 0, TIEU_DE ở vị trí 1 — không kéo, không thả lên trên | CẢ HAI | P0 | CHỐT | bổ sung #3 · C12 |
| R-MAUIN-051 | DON_VI/TIEU_DE không xoá; TIEU_DE luôn hiện; DON_VI ẩn được | CẢ HAI | P1 | CHỐT | bổ sung #3 · Q5 |
| R-MAUIN-052 | Khối chuẩn (THONG_TIN · TONG_HOP · CHU_KY) và mọi khối BANG không xoá, chỉ ẩn | CẢ HAI | P1 | CHỐT | mock hint :150 · Q16 |
| R-MAUIN-053 | Chỉ TU_DO thêm/xoá; thêm vào ngay trước CHU_KY | FE | P2 | CHỐT | mock addFree :300 |
| R-MAUIN-054 | Mỗi bảng của catalog đúng một khối BANG | CẢ HAI | P1 | CHỐT | Q16 |
| R-MAUIN-060 | Undo/redo 60 bước, chỉ `mau` vào lịch sử | FE | P1 | CHỐT | mock push() :243 |
| R-MAUIN-061 | Dirty = JSON khác bản đã lưu → tag "Chưa lưu" | FE | P1 | CHỐT | mock isDirty :245 |
| R-MAUIN-062 | Phím tắt Ctrl+S · Ctrl+Z · Ctrl+Y · Esc | FE | P2 | CHỐT | mock :511 |
| R-MAUIN-063 | Đóng khi dirty → xác nhận BR3 (2 nút, chữ nguyên văn) | FE | P1 | CHỐT | BR3 · Q18 |
| R-MAUIN-064 | "Đặt lại mẫu chuẩn" nạp `macDinh.mau` vào editor sau xác nhận, chưa lưu | FE | P1 | CHỐT | mock resetBtn :492 |
| R-MAUIN-065 | Xoá khối tự do → xác nhận "Xác nhận xóa" (BR3) | FE | P2 | CHỐT | BR3 · mock :296 |
| R-MAUIN-066 | Zoom 40–160 % bước 10; "Vừa khung" theo bề ngang canvas, trần 140 % | FE | P2 | CHỐT | mock :500-503 |
| R-MAUIN-067 | Nguồn xem thử: chứng từ đang mở / dữ liệu mẫu / chứng từ khác; super admin chỉ dữ liệu mẫu | FE | P1 | CHỐT | mock #dataSeg · Q9 |
| R-MAUIN-068 | Gõ nhãn cập nhật canvas ngay; lịch sử ghi lúc blur | FE | P2 | CHỐT | mock input/change :447 |
| R-MAUIN-070 | Có `thayDoi` → thông báo "Có N trường mới" | FE | P2 | CHỐT | mock hint :400 · Q6 |
| R-MAUIN-071 | Menu In = mẫu cố định của provider + "Mẫu tùy chỉnh" + "⚙ Thiết lập mẫu in…" | CẢ HAI | P1 | CHỐT | mock #menuDemo :506 |
| R-MAUIN-072 | In tuỳ chỉnh dùng CÙNG renderer với canvas, không bản dựng thứ hai | FE | P0 | CHỐT | D5 · Q1 |
| R-MAUIN-073 | In qua blob URL cửa sổ mới; `@page` theo khổ/lề; `thead` lặp khi `lapTieuDeCot` | FE | P1 | CHỐT | inPhieuApi.ts (401 khi mở API trần) · mock repeatHead |
| R-MAUIN-074 | Số tiền bằng chữ do BE cấp | BE | P1 | CHỐT | SoTienBangChu · hợp đồng §0.6 |
| R-MAUIN-075 | Số/ngày trên bản in định dạng theo runtime tenant | FE | P1 | CHỐT | BR7 · BR8 · D10 |
| R-MAUIN-076 | Dữ liệu in đi qua `layChiTiet` của module chủ (kẹp tenant/quyền) | BE | P0 | CHỐT | InPhieuThuChiService · C14 |
| R-MAUIN-080 | Đầu trang đơn vị từ Thông tin công ty; fallback `mst_don_vi` GỐC | BE | P1 | CHỐT | mock company :372 · C09 |
| R-MAUIN-081 | Địa chỉ = chi tiết + phường/xã + tỉnh (bỏ phần thiếu) | BE | P2 | CHỐT | C13 |
| R-MAUIN-082 | Người ký theo vai trò từ Thông tin công ty; `inTen` mặc định = cờ tenant | CẢ HAI | P1 | CHỐT | mock sign :383 · CompanyInfoResponse |
| R-MAUIN-083 | Người lập phiếu = người đang đăng nhập khi cờ tenant bật | BE | P2 | CHỐT | C10 |
| R-MAUIN-090 | Cell kéo mẫu mặc định qua `/internal/mau-in/mac-dinh/{ma}` với X-Internal-Token, ETag/304 | BE | P1 | CHỐT | D4 · Q2 |
| R-MAUIN-091 | Super admin lưu qua cùng bộ kiểm §5 với catalog snapshot | SA | P0 | CHỐT | D3 · D8 |
| R-MAUIN-092 | Super admin xoá bản mặc định → cell rơi về mẫu đóng gói | SA | P1 | CHỐT | D2 |
| R-MAUIN-093 | Snapshot catalog mang `catalogVersion`, hiển thị ở màn super admin | SA | P2 | CHỐT | D3 · R2 |
| R-MAUIN-094 | TTL cache mặc định 10 phút (cấu hình); `PMKT_SUPER_ADMIN_URL` trống → bỏ tầng 2, log một lần | BE | P1 | CHỐT | D4 |
| R-MAUIN-100 | Kéo mép cột trên giấy để đổi độ rộng, bù trừ cột liền kề | FE | P1 | CHỐT | user 2026-09-17 |
| R-MAUIN-101 | Mỗi lần lưu hoặc bỏ mẫu ghi một bản ghi lịch sử | BE · SA | P1 | CHỐT | user 2026-09-17 |
| R-MAUIN-102 | Danh sách lịch sử phiên bản, mới nhất trước | CẢ HAI · SA | P1 | CHỐT | user 2026-09-17 |
| R-MAUIN-103 | Xem trước một phiên bản cũ bằng chính renderer của canvas | CẢ HAI · SA | P1 | CHỐT | user 2026-09-17 |
| R-MAUIN-104 | Khôi phục phiên bản cũ chỉ nạp vào editor, chưa ghi DB | FE | P1 | CHỐT | user 2026-09-17 |
| R-MAUIN-105 | Giữ tối đa 50 bản ghi lịch sử mỗi loại, dọn bản cũ nhất | BE · SA | P2 | CHỐT | user 2026-09-17 |
| R-MAUIN-106 | Console super admin chọn nguồn xem thử: dữ liệu mẫu hoặc giữ chỗ | SA | P2 | CHỐT | user 2026-09-17 |
| R-MAUIN-107 | Ô bảng kẻ mờ trên canvas, không có khi in | FE | P2 | CHỐT | user 2026-09-17 |
| INV-MAUIN-001 | `khoi[0]` = DON_VI, `khoi[1]` = TIEU_DE, mỗi loại đúng 1, cả hai `khoa={viTri,xoa}` | CẢ HAI | P0 | CHỐT | bổ sung #3 |
| INV-MAUIN-002 | Đúng một THONG_TIN, một TONG_HOP, một CHU_KY | CẢ HAI | P0 | CHỐT | mock defaultState |
| INV-MAUIN-003 | `id` khối duy nhất; `nguon` BANG duy nhất và có trong catalog | CẢ HAI | P0 | CHỐT | Q16 |
| INV-MAUIN-004 | Mọi `k` tồn tại trong catalog (khoá lạ bị loại ở hợp nhất, không lỗi) | CẢ HAI | P0 | CHỐT | hợp đồng §4 |
| INV-MAUIN-005 | `span ∈ [1, soCot]`; `rong ∈ [3, 90]`; sau chuẩn hoá Σ rong cột hiện = 100 ± 0,5 | CẢ HAI | P0 | CHỐT | mock tnorm |
| INV-MAUIN-006 | `UNIQUE (tenant_id, ma_loai_chung_tu) WHERE da_xoa = false` | BE | P0 | CHỐT | hợp đồng §8.1 |
| INV-MAUIN-007 | `schema_version` cột = `cauHinh.schemaVersion` | BE | P1 | CHỐT | hợp đồng §8.1 |
| INV-MAUIN-008 | JSON chỉ được ghi xuống DB sau khi qua `KiemTraMau` không còn lỗi | BE | P0 | CHỐT | R-027 |
| INV-MAUIN-009 | Bản ghi lịch sử chỉ được THÊM; không sửa, không xoá trừ khi dọn theo giới hạn 50 | BE · SA | P1 | CHỐT | R-101 · R-105 |

---

## Nhóm 0 — Quyền (`R-MAUIN-001…006`)

### R-MAUIN-001 · Menu & route Thiết lập mẫu in theo `HTMauIn.View`
```
Tầng      CẢ HAI          Sev  P1
Nguồn     BR25.1 (Menu · Trang) · Q4
WHEN      người dùng không có HTMauIn.View
THEN      ẩn mục menu; vào thẳng URL → trang 403 MSG_COMMON_002; A1/A2/A5 trả 403 MSG_COMMON_003
Kịch bản  S-001
```

### R-MAUIN-002 · Lưu / đặt lại mẫu của đơn vị theo `HTMauIn.Edit`
```
Tầng      CẢ HAI          Sev  P0
Nguồn     BR25 · Q4
WHEN      PUT /api/mau-in/{ma} hoặc DELETE /api/mau-in/{ma} bởi người thiếu HTMauIn.Edit
THEN      403 MSG_COMMON_003, không ghi gì; FE ẩn nút Lưu/Đặt lại (editor chỉ đọc) khi thiếu quyền
Kịch bản  S-002
```

### R-MAUIN-003 · Menu in & dữ liệu in theo quyền in của loại chứng từ
```
Tầng      CẢ HAI          Sev  P0
Nguồn     BR25 · mock #menuDemo · C08
WHEN      GET /api/mau-in/{ma}/menu · GET /api/mau-in/{ma}/chung-tu/{id}/du-lieu-in
THEN      BE kiểm <maChucNang>.<hanhDongIn()> — mặc định "Print"; provider MDV khai "View.Detail" (C08)
          FE chỉ dựng NutInChungTu khi có mã quyền đó (ẩn, không xám)
Lỗi       MSG_COMMON_003
Kịch bản  S-003 · S-004
```

### R-MAUIN-004 · Chọn chứng từ thật để xem thử cần `<ChucNang>.View`
```
Tầng      BE              Sev  P1
Nguồn     BR25 · Q9
WHEN      GET /api/mau-in/{ma}/chung-tu-gan-day
THEN      require HTMauIn.View VÀ <maChucNang>.View; tối đa 20 dòng, tìm theo số chứng từ/diễn giải
Kịch bản  S-005
```

### R-MAUIN-005 · Mục "⚙ Thiết lập mẫu in…" chỉ hiện khi có `HTMauIn.Edit`
```
Tầng      FE              Sev  P1
Nguồn     BR25.2 · mock menu
WHEN      dựng menu In
THEN      mục ⚙ có mặt khi useHasPermission()('HTMauIn.Edit'); thiếu quyền ⇒ không có mục (không disabled)
Kịch bản  S-006
```

### R-MAUIN-006 · Super admin: `MauInMacDinh.*`
```
Tầng      SA              Sev  P1
Nguồn     Q4 · MaQuyenAdmin
WHEN      B1..B4
THEN      View (B1) · View.Detail (B2) · Edit (B3) · Delete (B4); khai đủ ở MaQuyenAdmin để FE nhận mã
Kịch bản  S-040
```

---

## Nhóm 1 — Kiểm tra & chuẩn hoá (`R-MAUIN-010…027`)

Chung: `kiemTraMau(mau, catalog) → { loi[], canhBao[] }` chạy ở FE (panel "Kiểm tra trước khi lưu") và BE
(A3/B3 trả 400 `MSG_MAUIN_017` kèm danh sách `loi`). Message nguyên văn ở hợp đồng §5.1.

### R-MAUIN-010 · Lề 0–5 cm
```
WHEN  le.tren|duoi|trai|phai ∉ [0, 5]      THEN  LỖI MSG_MAUIN_001 "Lề {viTri} phải từ 0 đến 5 cm."
FE    ô nhập kẹp về 0/5 kèm toast cảnh báo (mock :424)            Kịch bản S-010
```
### R-MAUIN-011 · Cỡ chữ cơ sở 8–20 pt
```
WHEN  coChu ∉ [8, 20]                      THEN  LỖI MSG_MAUIN_002                       Kịch bản S-010
```
### R-MAUIN-012 · Mã màu chữ `#rrggbb`
```
WHEN  mauChu !~ ^#[0-9a-f]{6}$ (so không phân biệt hoa/thường)   THEN  LỖI MSG_MAUIN_014
FE    ô hex sai → toast + trả về giá trị cũ (mock :427)           Kịch bản S-010
```
### R-MAUIN-013 · Tiêu đề bản in không được trống
```
WHEN  khối TIEU_DE (luôn hien) có noiDung.trim() = ''            THEN  LỖI MSG_MAUIN_003     Kịch bản S-011
```
### R-MAUIN-014 · Σ độ rộng cột ≠ 100 % → cảnh báo
```
WHEN  bảng hien có |Σ rong(cột hien) − 100| > 0,5   THEN  CẢNH BÁO MSG_MAUIN_004 (lưu vẫn được; R-026 chia lại)
Kịch bản S-012
```
### R-MAUIN-015 · Bảng đang bật phải có ≥1 cột
```
WHEN  bảng hien không có cột hien           THEN  LỖI MSG_MAUIN_005                        Kịch bản S-013
```
### R-MAUIN-016 · Tối đa 4 ô ký hiện
```
WHEN  CHU_KY có > 4 ô hien                  THEN  LỖI MSG_MAUIN_012
FE    tick ô thứ 5 bị từ chối + toast; "+ Thêm ô ký tự do" bị chặn khi đã 4 (mock :462,:467)   Kịch bản S-014
```
### R-MAUIN-017 · Không có bảng chi tiết nào → cảnh báo
```
WHEN  không khối BANG nào hien              THEN  CẢNH BÁO MSG_MAUIN_006                   Kịch bản S-015
```
### R-MAUIN-018 · Khối chữ ký bật mà không ô nào → cảnh báo
```
WHEN  CHU_KY.hien && không ô hien           THEN  CẢNH BÁO MSG_MAUIN_007                   Kịch bản S-015
```
### R-MAUIN-019 · Khối tự do bật mà không dòng nào → cảnh báo
```
WHEN  TU_DO.hien && không truong hien       THEN  CẢNH BÁO MSG_MAUIN_008                   Kịch bản S-015
```
### R-MAUIN-020 · Khối tự do phải có tên
```
WHEN  TU_DO.ten.trim() = ''                 THEN  LỖI MSG_MAUIN_009                        Kịch bản S-016
```
### R-MAUIN-021 · Nền đậm > 60 % → cảnh báo
```
WHEN  nen.kieu ≠ KHONG && nen.doDam > 60    THEN  CẢNH BÁO MSG_MAUIN_010                   Kịch bản S-015
```
### R-MAUIN-022 · Không hiện Số chứng từ → cảnh báo
```
WHEN  không trường nào k='soChungTu' đang hien (ở THONG_TIN hoặc TU_DO) và TIEU_DE.dongSoNgay = false
THEN  CẢNH BÁO MSG_MAUIN_011                                                               Kịch bản S-015
```
### R-MAUIN-023 · Thông tin chung bật phải còn ≥1 trường hiển thị
```
Nguồn BR30 (nguyên văn) · Sev P0
WHEN  THONG_TIN.hien && mọi truong.hien = false     THEN  LỖI MSG_MAUIN_013 "Phải giữ lại ít nhất 1 trường hiển thị."
FE    bỏ tick trường cuối cùng bị từ chối + toast                                          Kịch bản S-017
```
### R-MAUIN-024 · JSON vi phạm bất biến cấu trúc → 400
```
Tầng BE · Sev P0
WHEN  vi phạm INV-MAUIN-001…005 (chỉ khi JSON bị sửa tay / client lỗi)
THEN  400 MSG_MAUIN_017 "Mẫu in không hợp lệ: {chiTiet}" với chiTiet = JSON Pointer; KHÔNG ghi DB (INV-008)
Kịch bản S-018
```
### R-MAUIN-025 · Giới hạn số khác
```
WHEN  TIEU_DE.coChu ∉ [10,36] · boCuc.rongNhan ∉ [15,60] · CotIn.rong ∉ [3,90] · boCuc.soCot ∉ {1,2,3,4}
THEN  LỖI MSG_MAUIN_017 (chiTiet trỏ đúng trường); FE kẹp giá trị ở ô nhập như mock (:428,:449)   Kịch bản S-010
```
### R-MAUIN-026 · Chuẩn hoá trước khi lưu
```
Tầng CẢ HAI · Sev P1 · Nguồn mock doSave :488 · BR43
WHEN  lưu (FE trước khi gửi, BE luôn chạy lại)
THEN  trim mọi chuỗi; mỗi bảng: cột hien chia lại về Σ=100 theo tỷ lệ, sai số dồn cột cuối; mauChu về chữ thường;
      truong có k thì bỏ tuDo, không k thì bỏ dam/nghieng? (giữ) — chỉ bỏ tuDo/k mâu thuẫn
Kịch bản S-012 · S-019
```
### R-MAUIN-027 · Còn lỗi thì không lưu
```
Tầng CẢ HAI · Sev P0
WHEN  kiemTraMau còn ≥1 loi
THEN  FE: nút Lưu disabled, Ctrl+S → toast lỗi đầu tiên; BE: 400 MSG_MAUIN_017 kèm toàn bộ loi
Kịch bản S-011 · S-018
```

---

## Nhóm 2 — Giải mẫu & lưu trữ (`R-MAUIN-030…037`)

### R-MAUIN-030 · Giải mẫu hiệu lực theo chuỗi 3 tầng
```
Tầng BE · Sev P0 · Nguồn D2
WHEN  A2 / A6 / A7 cần mẫu hiệu lực của (tenant, ma)
THEN  1) prn_mau_in_tuy_chinh(tenant, ma, da_xoa=false) → nguon=TUY_CHINH
      2) else cache super-admin(ma) → nguon=MAC_DINH_HE_THONG
      3) else MauChuanBuilder(provider.moTa()) → nguon=MAC_DINH_DONG_GOI
      kết quả LUÔN qua hopNhat(catalog) + chuanHoa()
Kịch bản S-020 · S-021 · S-022
```
### R-MAUIN-031 · Bản tuỳ chỉnh thắng tuyệt đối
```
Tầng BE · Sev P0
WHEN  super admin đổi mẫu mặc định sau khi tenant đã có bản tuỳ chỉnh
THEN  bản in của tenant KHÔNG đổi; không merge tự động       Kịch bản S-023
```
### R-MAUIN-032 · Lưu ghi `mac_dinh_nguon` + `mac_dinh_phien_ban`
```
Tầng BE · Sev P1
WHEN  PUT lần đầu (tạo bản tuỳ chỉnh)
THEN  ghi nguồn mẫu đang hiệu lực lúc đó (MAC_DINH_HE_THONG + phienBan, hoặc MAC_DINH_DONG_GOI + null)
Kịch bản S-024
```
### R-MAUIN-033 · `coMacDinhMoi`
```
Tầng CẢ HAI · Sev P1
WHEN  tenant có bản tuỳ chỉnh với mac_dinh_nguon=MAC_DINH_HE_THONG và phienBan super admin hiện tại > mac_dinh_phien_ban
THEN  A1/A2 trả coMacDinhMoi=true; FE hiện badge + toast MSG_MAUIN_016 và nút "Đặt lại theo mẫu chuẩn"
Kịch bản S-023
```
### R-MAUIN-034 · Không nối được super-admin
```
Tầng BE · Sev P1 · Nguồn D4 · L6
WHEN  MacDinhHeThongRest ném lỗi mạng/5xx
THEN  cache còn hạn → dùng; hết hạn → dùng bản stale + log WARN (≤1 lần/ma/5 phút); chưa từng có → tầng 3 (đóng gói),
      nguon=MAC_DINH_DONG_GOI, FE hiện MSG_MAUIN_020 cho admin
Kịch bản S-025
```
### R-MAUIN-035 · Xoá bản tuỳ chỉnh = xoá mềm
```
Tầng BE · Sev P1 · Nguồn BR29
WHEN  DELETE /api/mau-in/{ma}
THEN  da_xoa=true (audit), A2 ngay sau đó trả nguon ≠ TUY_CHINH        Kịch bản S-026
```
### R-MAUIN-036 · Khoá lạc quan
```
Tầng CẢ HAI · Sev P1
WHEN  PUT với phienBan ≠ phienBan hiện tại (hoặc null khi đã có bản ghi)
THEN  409 MSG_MAUIN_018 "Mẫu đã được người khác thay đổi. Tải lại trước khi lưu."; FE toast + giữ nguyên editor
Kịch bản S-027
```
### R-MAUIN-037 · Loại chưa có provider
```
Tầng CẢ HAI · Sev P1 · Nguồn BR4/BR9
WHEN  A2..A7 với ma không có provider          THEN 404 MSG_MAUIN_019
WHEN  A1                                       THEN 47 dòng từ mst_loai_chung_tu; dòng không provider: hoTro=false, FE khoá nút Thiết lập kèm nhãn "Chưa hỗ trợ"
Kịch bản S-028
```

---

## Nhóm 3 — Hợp nhất catalog (`R-MAUIN-040…046`) — cùng fixture `fixtures/hop-nhat/*`

### R-MAUIN-040 · Bỏ khoá lạ, giữ dòng tự do
```
WHEN  truong/cot/tongHop có k ∉ catalog        THEN  loại khỏi mẫu, ghi vào thayDoi.boTruong; dòng tuDo (không k) giữ nguyên
Kịch bản S-030
```
### R-MAUIN-041 · Thêm trường mới
```
WHEN  catalog.truong có k chưa xuất hiện ở bất kỳ THONG_TIN/TU_DO nào
THEN  thêm vào cuối THONG_TIN với span=1, nhan=catalog.nhan; hien=true nếu nguon mẫu ∈ {MAC_DINH_*}, hien=false + moi=true nếu TUY_CHINH (Q6)
Kịch bản S-031
```
### R-MAUIN-042 · Thêm cột mới
```
WHEN  catalog.bang[x].cot có k chưa có trong khối BANG(nguon=x)
THEN  thêm cuối bảng, rong = trung bình rong cột đang hien (làm tròn), hien như R-041   Kịch bản S-032
```
### R-MAUIN-043 · Thêm bảng mới
```
WHEN  catalog.bang có k chưa có khối BANG        THEN  khối BANG mới ngay trước CHU_KY, hien=false, cột theo macDinh
Kịch bản S-033
```
### R-MAUIN-044 · Đồng bộ DON_VI / CHU_KY
```
WHEN  DON_VI thiếu/thừa dòng so với 5 khoá cố định · CHU_KY có vaiTro ∉ catalog.vaiTroKy
THEN  bổ sung dòng thiếu (hien=false), bỏ dòng thừa; bỏ ô ký vai trò lạ (ô tuDo giữ)   Kịch bản S-034
```
### R-MAUIN-045 · Không đổi thứ tự
```
WHEN  hợp nhất                                    THEN  thứ tự khối/trường/cột hiện có giữ nguyên tuyệt đối   Kịch bản S-030…034
```
### R-MAUIN-046 · Trả `thayDoi`
```
THEN  { themTruong[], themCot{nguon:[k]}, themBang[], boTruong[] } đi kèm A2/B2; rỗng khi không đổi   Kịch bản S-031
```

---

## Nhóm 4 — Khoá khối & cấu trúc (`R-MAUIN-050…054`)

### R-MAUIN-050 · DON_VI ở 0, TIEU_DE ở 1
```
Tầng CẢ HAI · Sev P0 · Nguồn bổ sung #3 · C12
WHEN  kéo thả khối (outline hoặc trên giấy) · PUT JSON
THEN  FE: hai khối không draggable, thả vào vị trí < 2 bị từ chối (doiViTri trả nguyên mảng); BE: INV-001 → 400
Kịch bản S-050
```
### R-MAUIN-051 · Không xoá; TIEU_DE luôn hiện; DON_VI ẩn được
```
Tầng CẢ HAI · Sev P1 · Nguồn Q5
THEN  outline không có nút ✕ và không có eye cho TIEU_DE; DON_VI có eye; BE: TIEU_DE.hien=false → chuanHoa ép true
Kịch bản S-051
```
### R-MAUIN-052 · Khối chuẩn & BANG không xoá, chỉ ẩn
```
Tầng CẢ HAI · Sev P1
THEN  FE không có ✕ cho THONG_TIN/TONG_HOP/CHU_KY/BANG; BE: INV-002/003 → 400   Kịch bản S-052
```
### R-MAUIN-053 · Chỉ TU_DO thêm/xoá
```
Tầng FE · Sev P2 · Nguồn mock addFree :300
WHEN  "+ Thêm khối tự do"   THEN  chèn ngay trước CHU_KY, tên "Khối tự do N", 2 dòng mẫu như mock, chọn khối mới
Kịch bản S-053
```
### R-MAUIN-054 · Mỗi bảng catalog đúng một khối BANG
```
Tầng CẢ HAI · Sev P1 · Nguồn Q16
THEN  không có nút "thêm bảng"; chọn bảng = eye trên khối BANG; BE INV-003   Kịch bản S-052
```

---

## Nhóm 5 — Editor (`R-MAUIN-060…070`, FE)

### R-MAUIN-060 · Undo/redo 60 bước
```
THEN  zundo temporal store, limit UNDO_TOI_DA=60; chỉ `mau` vào lịch sử (selection/zoom/nguồn xem thử không)
Kịch bản S-060
```
### R-MAUIN-061 · Dirty
```
THEN  dirty = JSON.stringify(mau) !== daLuu; tag "Chưa lưu" (gold) / "Đã lưu" (default); lưu xong → daLuu = mau
Kịch bản S-061
```
### R-MAUIN-062 · Phím tắt
```
THEN  Ctrl+S = Lưu · Ctrl+Z = Undo · Ctrl+Y = Redo · Esc = Đóng (chỉ khi không có modal mở)   Kịch bản S-062
```
### R-MAUIN-063 · Đóng khi dirty → BR3
```
Nguồn BR3 · Q18 · Sev P1
THEN  CommonConfirmModal tiêu đề "Xác nhận đóng", nội dung "Dữ liệu đã có thay đổi. Bạn có chắc chắn muốn đóng? Thay đổi sẽ không được lưu."
      Xác nhận → về troVe/danh sách, bỏ thay đổi; Hủy/Esc/click ngoài → ở lại      Kịch bản S-063
```
### R-MAUIN-064 · Đặt lại mẫu chuẩn
```
THEN  xác nhận (BR16 kiểu popup) → nạp macDinh.mau vào editor (đẩy vào lịch sử, dirty=true), toast MSG_MAUIN_021 "Đã đưa về mẫu chuẩn (chưa lưu)"
Kịch bản S-064
```
### R-MAUIN-065 · Xoá khối tự do
```
THEN  CommonConfirmModal "Xác nhận xóa" — "Bạn có chắc chắn muốn xóa khối tự do '{ten}'? Thao tác này không thể hoàn tác." → xoá, chọn về trang
Kịch bản S-053
```
### R-MAUIN-066 · Zoom
```
THEN  ZOOM 0,4–1,6 bước 0,1; "Vừa khung" = min(1,4, (rộng canvas − 50)/rộng giấy); đổi khổ/hướng gọi lại fit
Kịch bản S-066
```
### R-MAUIN-067 · Nguồn xem thử
```
THEN  tenant: segment "Chứng từ đang mở" (khi có chungTuId) · "Dữ liệu mẫu" · combo "Chứng từ khác…" (A5); super admin: chỉ dữ liệu mẫu
      đổi nguồn KHÔNG đổi mẫu, không vào lịch sử                                            Kịch bản S-067
```
### R-MAUIN-068 · Gõ nhãn
```
THEN  onChange input cập nhật mau (canvas vẽ lại) nhưng lịch sử chỉ ghi ở blur/Enter (một bước cho một lần sửa nhãn)
Kịch bản S-060
```
### R-MAUIN-070 · Thông báo trường mới
```
THEN  khi tải A2 có thayDoi.themTruong/themCot không rỗng → toast info "Có {n} trường/cột mới được thêm vào mẫu" + đánh dấu `moi` trong bảng
Kịch bản S-031
```

---

## Nhóm 6 — In (`R-MAUIN-071…076`)

### R-MAUIN-071 · Menu In
```
Tầng CẢ HAI · Sev P1 · Nguồn mock #menuDemo
THEN  A7 trả [CO_DINH…(provider.mauCoDinh(id)), TUY_CHINH]; FE thêm separator + "⚙ Thiết lập mẫu in…" (R-005)
      nửa trái split button = mục đầu tiên; đang tải/ rỗng → mục disabled như NutInPhieu                Kịch bản S-071
```
### R-MAUIN-072 · Một renderer
```
Tầng FE · Sev P0 · Nguồn D5 · Q1
THEN  MauInPaper render cả canvas (cheDo SUA) lẫn HTML in (cheDo XEM, renderToStaticMarkup); không component in riêng
Kịch bản S-072
```
### R-MAUIN-073 · Cửa sổ in
```
Tầng FE · Sev P1
THEN  dựng HTML tự chứa (CSS giấy + @page {size: <khổ> <hướng>; margin: <lề>cm}), thead {display: table-header-group} khi lapTieuDeCot,
      mở blob URL bằng window.open (noopener), gọi print() sau load, thu hồi URL sau khi đóng   Kịch bản S-072
```
### R-MAUIN-074 · Số tiền bằng chữ do BE cấp
```
Tầng BE · Sev P1
THEN  DuLieuIn.tongHop.soTienBangChu = SoTienBangChu.doc(tổng thanh toán, "đồng" | mã tiền); FE không tự đọc số   Kịch bản S-074
```
### R-MAUIN-075 · Định dạng số/ngày theo tenant
```
Tầng FE · Sev P1 · Nguồn BR7 · BR8
THEN  kieu TIEN/SO → useNumberFormatRuntime().formatForDisplay(v, 'tien'|'soLuong'…, 'baoCao'); NGAY → dd/MM/yyyy theo locale; null → ''
Kịch bản S-075
```
### R-MAUIN-076 · Dữ liệu in đi qua module chủ
```
Tầng BE · Sev P0 · Nguồn InPhieuThuChiService · C14
THEN  provider.duLieuIn(id) gọi đúng service của module (MDV: getDichVu + layDongChiTietDichVu — 404 khi id không phải dịch vụ);
      bảng `thue` của MDV suy từ dòng có tienThueGtgt ≠ 0; mọi giá trị null → '' / null, không "null"   Kịch bản S-076
```

---

## Nhóm 7 — Đơn vị & người ký (`R-MAUIN-080…083`)

### R-MAUIN-080 · Đầu trang đơn vị
```
Tầng BE · Sev P1 · Nguồn C09
THEN  donVi.ten = Tenant.tenDonVi (trống → mst_don_vi GỐC.ten); mst = Tenant.mst; dienThoai = soDienThoai; email = email
Kịch bản S-080
```
### R-MAUIN-081 · Địa chỉ ghép
```
Tầng BE · Sev P2 · Nguồn C13
THEN  join(", ", [diaChiChiTiet, tên phường xã, tên tỉnh].filter(non-blank)); tất cả trống → mst_don_vi GỐC.dia_chi → ''   Kịch bản S-080
```
### R-MAUIN-082 · Người ký theo vai trò
```
Tầng CẢ HAI · Sev P1
THEN  nguoiKy[vaiTro] = {tieuDe: Tenant.tieuDeNguoiKy*, ten: Tenant.tenNguoiKy*}; MauChuanBuilder đặt CHU_KY.inTen = Tenant.inTenNguoiKyTrenChungTu?
      — KHÔNG: mẫu chuẩn là tĩnh (không phụ thuộc tenant) → inTen mặc định true trong mẫu; renderer chỉ in tên khi inTen && duLieu.inTenNguoiKy
Kịch bản S-082
```
### R-MAUIN-083 · Người lập phiếu = người đăng nhập
```
Tầng BE · Sev P2 · Nguồn C10
THEN  cờ bật → nguoiKy.NGUOI_LAP.ten = NguoiDungLookupApi.hoTenTheoId(TenantContext.userId()); tra không ra → tên đã cấu hình
Kịch bản S-083
```

---

## Nhóm 8 — Super admin & lan mẫu (`R-MAUIN-090…094`)

### R-MAUIN-090 · Cell kéo mẫu mặc định
```
Tầng BE (client ở cell) + SA (server) · Sev P1 · Nguồn D4 · Q2
THEN  GET {PMKT_SUPER_ADMIN_URL}/internal/mau-in/mac-dinh/{ma} với X-Internal-Token; If-None-Match: "<phienBan>" → 304 giữ cache;
      200 → cập nhật cache + ETag; 404 → ghi "không có" (negative cache) để rơi tầng 3
Kịch bản S-090
```
### R-MAUIN-091 · Super admin lưu qua cùng bộ kiểm
```
Tầng SA · Sev P0 · Nguồn D3 · D8
THEN  B3: KiemTraMau + ChuanHoa (bản Java sao từ cell) với catalog từ snapshot; lỗi → 400 MSG_MAUIN_017   Kịch bản S-091
```
### R-MAUIN-092 · Super admin xoá
```
Tầng SA · Sev P1
THEN  B4 xoá mềm; B5 trả 404 cho ma đó; cell rơi về đóng gói sau TTL   Kịch bản S-092
```
### R-MAUIN-093 · `catalogVersion`
```
Tầng SA · Sev P2
THEN  snapshot mang catalogVersion (git sha + ngày sinh); B1 trả về; màn super admin hiển thị ở header   Kịch bản S-093
```
### R-MAUIN-094 · TTL & tắt tầng 2
```
Tầng BE · Sev P1 · Nguồn D4
THEN  pmkt.mau-in.super-admin.ttl mặc định 10m; url trống → bean client vắng, GiaiMauHieuLuc bỏ tầng 2 và log INFO một lần lúc boot
Kịch bản S-094
```

---

---

## Nhóm 9 — Lịch sử phiên bản & thao tác trên giấy (`R-MAUIN-100…107`)

Chốt của user 2026-09-17 (đợt bổ sung sau khi xem bản chạy thật). Bốn quyết định gốc: kéo cột bù trừ với cột
liền kề · lịch sử áp cho **cả hai tầng** · popup lịch sử cho xem trước **và** khôi phục · nguồn xem thử ở console
super admin đổi được giữa dữ liệu mẫu và dữ liệu giữ chỗ.

### R-MAUIN-100 · Kéo mép cột trên giấy để đổi độ rộng
```
Tầng      FE              Sev  P1
WHEN      trỏ vào mép phải một ô tiêu đề cột của khối BANG trên canvas (chế độ 'canvas', không docChi)
THEN      con trỏ đổi thành col-resize; kéo đổi `rong` của cột đang kéo và BÙ TRỪ ngược lại vào cột HIỆN
          liền kề bên phải (cột cuối thì bù vào cột hiện liền kề bên trái) ⇒ Σ rong không đổi, luôn = 100
          mỗi cột kẹp trong [3, 90] (INV-MAUIN-005); chạm biên thì dừng, không đẩy tiếp sang cột thứ ba
          một lần kéo (nhấn → thả) = MỘT bước hoàn tác (R-MAUIN-060)
KHÔNG     chế độ 'in' và docChi không gắn tay cầm; khối BANG đang ẩn không kéo được
Kịch bản  S-100 · S-101
```

### R-MAUIN-101 · Ghi lịch sử mỗi lần lưu hoặc bỏ mẫu
```
Tầng      BE (cell) · SA (super-admin)        Sev  P1
WHEN      A3 PUT /api/mau-in/{ma} thành công · A4 DELETE thành công · B3 PUT · B4 DELETE
THEN      chèn một bản ghi lịch sử: { maLoaiChungTu, phienBan (sau khi lưu), cauHinh (JSON đã chuẩn hoá),
          schemaVersion, hanhDong ∈ {LUU, XOA}, ghiChu, nguoiTao, ngayTao }
          cell: kèm tenantId + RLS như bảng chính. Ghi trong CÙNG giao dịch với bản ghi mẫu
          hanhDong = XOA thì `cauHinh` là JSON NGAY TRƯỚC khi xoá (để khôi phục được)
Kịch bản  S-102 · S-103
```

### R-MAUIN-102 · Danh sách lịch sử
```
Tầng      CẢ HAI · SA     Sev  P1
WHEN      A8 GET /api/mau-in/{ma}/lich-su  ·  B7 GET /api/admin/mau-in/{ma}/lich-su
THEN      trả tối đa 50 mục, `ngayTao` GIẢM DẦN, mỗi mục
          { id, phienBan, hanhDong, ghiChu, nguoiTao, ngayTao } — KHÔNG kèm `cauHinh` (nhẹ danh sách)
Quyền     cell: HTMauIn.View  ·  super-admin: MauInMacDinh.View.Detail
Kịch bản  S-102 · S-104
```

### R-MAUIN-103 · Xem trước một phiên bản cũ
```
Tầng      CẢ HAI · SA     Sev  P1
WHEN      A9 GET /api/mau-in/{ma}/lich-su/{id}  ·  B8 GET /api/admin/mau-in/{ma}/lich-su/{id}
THEN      trả { id, phienBan, hanhDong, ngayTao, nguoiTao, mau } với `mau` đã đi qua hopNhat(catalog hiện tại)
          + chuanHoa — phiên bản cũ thiếu trường mới vẫn mở được, không vỡ
          id không thuộc {ma} (hoặc khác tenant) ⇒ 404 MSG_MAUIN_024
FE        popup vẽ bản xem trước bằng CHÍNH MauInPaper chế độ 'canvas' (R-MAUIN-072: một renderer)
Kịch bản  S-103 · S-105
```

### R-MAUIN-104 · Khôi phục phiên bản cũ
```
Tầng      FE              Sev  P1
WHEN      bấm "Khôi phục" trong popup lịch sử
THEN      nạp `mau` của phiên bản đó vào editor bằng thayMau (VÀO lịch sử hoàn tác), đóng popup,
          toast MSG_MAUIN_025 "Đã nạp phiên bản {phienBan} vào trình soạn (chưa lưu)."
          KHÔNG gọi PUT — người dùng phải tự bấm Lưu / Xuất bản; huỷ bằng Ctrl+Z
          thiếu quyền sửa (docChi) ⇒ không có nút Khôi phục, vẫn xem trước được
Kịch bản  S-105
```

### R-MAUIN-105 · Giới hạn số bản ghi lịch sử
```
Tầng      BE · SA         Sev  P2
THEN      sau khi chèn, xoá các bản ghi ngoài 50 bản mới nhất của cùng (tenant, maLoaiChungTu)
          hằng GIOI_HAN_LICH_SU = 50 đặt cạnh GioiHanMauIn
Kịch bản  S-106
```

### R-MAUIN-106 · Nguồn xem thử ở console super admin
```
Tầng      SA (FE)         Sev  P2
WHEN      màn sửa mẫu mặc định hệ thống
THEN      thanh công cụ canvas có ô chọn 2 mục: "Dữ liệu mẫu" (duLieuMau của snapshot) và "Dữ liệu giữ chỗ"
          (duLieuXemThuTuCatalog); snapshot loại đó không có duLieuMau ⇒ mục "Dữ liệu mẫu" bị mờ, mặc định
          rơi về giữ chỗ. Đổi nguồn KHÔNG đổi mẫu, KHÔNG vào lịch sử hoàn tác (như R-MAUIN-067)
Kịch bản  S-107
```

### R-MAUIN-107 · Kẻ mờ ô bảng trên canvas
```
Tầng      FE              Sev  P2
THEN      chế độ 'canvas': mọi ô của khối BANG và của THONG_TIN dạng bảng có đường kẻ mờ 1px (màu rất nhạt,
          không phải màu viền thật của mẫu) để thấy ranh giới ô khi mẫu tắt đường kẻ
          chế độ 'in' và HTML sinh cho cửa sổ in KHÔNG có đường này (CSS đặt dưới lớp .pmkt-mau-in--canvas)
Kịch bản  S-108
```

## Bất biến

| ID | Cưỡng chế ở |
|---|---|
| INV-MAUIN-001 | `KiemTraMau.kiemCauTruc` (BE) · `kiemTraMau.ts` (FE) · `doiViTri` từ chối |
| INV-MAUIN-002 | như trên |
| INV-MAUIN-003 | như trên + `MauChuanBuilder` sinh đúng một khối/bảng |
| INV-MAUIN-004 | `HopNhatCatalog` (loại khoá lạ) — không phải lỗi |
| INV-MAUIN-005 | `KiemTraMau` (R-025) + `ChuanHoaMau` (R-026) |
| INV-MAUIN-006 | migration `prn_mau_in_tuy_chinh` unique index một phần + `MauInService.luu` (find-or-create) |
| INV-MAUIN-007 | `MauInTuyChinh` setter ghi `schemaVersion` từ JSON đã parse |
| INV-MAUIN-008 | `MauInService.luu` chỉ gọi `repository.save` sau `KiemTraMau` rỗng lỗi |
| INV-MAUIN-009 | `MauInLichSuService.ghi` chỉ `insert`; dọn bằng truy vấn giữ N bản mới nhất |

## Ghi chú hiện thực (chốt khi code, 2026-09-17)

| Chủ đề | Quyết định khi code | Ảnh hưởng luật |
|---|---|---|
| Kênh cell ↔ super-admin | `ProxyArchTest` cấm `RestClient` trần ⇒ `MacDinhHeThongRest` đi qua `ProxyClient`, đích `pmkt.proxy.targets.super-admin` (INTERNAL_TOKEN, `read-timeout 3s`, không retry); bật bằng `pmkt.mau-in.super-admin.enabled` | R-MAUIN-034 · R-MAUIN-090 · R-MAUIN-094 |
| Message mới | `MSG_MAUIN_021` "Đã đưa về mẫu chuẩn (chưa lưu)" (FE, R-MAUIN-064); `MSG_MAUIN_023` B5 trả 404 "chưa có mẫu mặc định hệ thống" (super-admin) | R-MAUIN-064 · R-MAUIN-090 |
| Đặt lại ≠ Bỏ tuỳ chỉnh | Editor tenant có HAI nút: "Đặt lại mẫu chuẩn" (R-MAUIN-064, cục bộ, chưa lưu) và "Bỏ bản tuỳ chỉnh" (A4 · R-MAUIN-035, xoá mềm trên server, chỉ khi đang `TUY_CHINH`) | R-MAUIN-035 · R-MAUIN-064 |
| Nguồn xem thử | Route editor đứng riêng (không mở từ chứng từ) ⇒ chỉ có "Dữ liệu mẫu" + combo 20 chứng từ gần đây (A5); segment "Chứng từ đang mở" không áp dụng | R-MAUIN-067 |
| Lịch sử khi gõ | Canvas nhận từng phím; lịch sử gộp các thay đổi cách nhau < 400 ms thành một bước (thay cho "ghi lúc blur") — kết quả undo tương đương | R-MAUIN-068 |
| Cửa sổ in | **Sửa 2026-09-17 sau báo cáo bản in 2 trang:** lề khai ở `@page` để MỌI trang đều có; `padding` của giấy chỉ còn cho lúc XEM cửa sổ in trên màn hình và bị gỡ trong `@media print` (mốc khung viền đổi theo). Trước đó `@page { margin: 0 }` + padding ⇒ trang 2 mất lề trên. Cùng khối đó hạ `tfoot` xuống `table-row-group` để dòng "Cộng" không lặp ở cuối mỗi trang | R-MAUIN-073 · R-MAUIN-010 |
| Snapshot catalog | `catalog.json` = `{catalogVersion, sinhLuc, loai[{moTa, mauChuan, duLieuMau?}]}`; đồng bộ bằng `docs/doing/mau-in-chung-tu/sync-catalog.sh` | R-MAUIN-093 |
| Dữ liệu mẫu trong snapshot | `XuatCatalogMauInTest` xuất `loai[].duLieuMau` = `DuLieuInDto.ghep(<Loai>MoTaMauIn.duLieuMau(), DonViInService.mau())` cho **cả 4 loại đã có provider** (MDV · BH · PT · PC) ⇒ console super admin xem thử bằng số liệu thật của loại đó; nhánh giữ chỗ `duLieuXemThuTuCatalog` ở client-admin chỉ còn dùng cho loại chưa xuất. Mapper bật `ORDER_MAP_ENTRIES_BY_KEYS` để hai lần chạy cho cùng một byte (fixture vàng không trôi) | R-MAUIN-093 · R-MAUIN-067 |
