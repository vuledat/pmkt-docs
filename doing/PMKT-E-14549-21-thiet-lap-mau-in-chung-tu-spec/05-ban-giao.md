# PMKT-E-14549_21 Thiết lập mẫu in chứng từ — BÀN GIAO

| | |
|---|---|
| Ngày | 2026-09-19 |
| Nhánh | `cell-app` → `feat/mau-in` · `client` → `feat/mau-in` — **chưa push** |
| Tài liệu nguồn | `pmkt-docs/ba/Phase_2/PMKT-E-14549_21_ThietLapMauInChungTu/` commit `c78e322a1` ⚠ vùng đóng băng |
| Figma | `ymMyg329ejsgCWg28CNmGl` node `71956:288871` — 8 frame, đã đối chiếu hết |
| Trạng thái | **Code xong, mọi cổng đo được đều ĐẠT.** Còn nợ tường minh ở §6 |

---

## §1. Đọc gì trước

| Thứ tự | File | Vì sao |
|---|---|---|
| 1 | [04-quyet-dinh-ban-giao.md](04-quyet-dinh-ban-giao.md) | **32 quyết định không có trong tài liệu BA.** Không đọc thì sẽ code theo đúng chữ tài liệu rồi ra kết quả khác |
| 2 | [02-rules.md](02-rules.md) | 271 luật `R-TLMI-…` — nguồn sự thật để code |
| 3 | [03-scenarios.md](03-scenarios.md) | 78 kịch bản `S-TLMI-…` — nguồn sự thật để test |
| 4 | `…-api/IMPLEMENT.md` · `…-fe/IMPLEMENT.md` | cái gì đã làm, làm ở đâu, lệch kế hoạch chỗ nào |

`00-source-map.md` và `01-conflict.md` để tra ngược khi nghi ngờ một luật.

---

## §2. Kết quả đo được — không phải tự đánh giá

```
trace.sh be   → Tong 156 luat: OK 156 · NO-TEST 0 · MISSING 0 · BLOCKED 0 · VI-PHAM 0 → DAT
trace.sh fe   → Tong 244 luat: OK 244 · NO-TEST 0 · MISSING 0 · BLOCKED 0 · VI-PHAM 0 → DAT
trace.sh all  → Tong 271 luat: OK 271 · NO-TEST 0 · MISSING 0 · BLOCKED 0 · VI-PHAM 0 → DAT

msg.sh fe     → Tong 26 message: OK 26 · LECH 0 · THIEU 0
msg.sh be     → Tong 26 message: OK 20 · LECH 0 · THIEU 6   (6 mã là toast/hộp thoại của FE)
```

| Cổng | Kết quả | Ghi chú |
|---|---|---|
| `cell-app` · `./gradlew unitTest` | `5770 tests completed, 3 failed` | **+52 test**. Ba test đỏ là `ChiPhiTraTruocModularityTest` · `HandlerAuthorizationArchTest` · `PhieuChiMuaHangRulesTest` — **đỏ sẵn trên `develop`**, ba file byte-identical với `37303112` |
| `client` · typecheck | `239 lỗi` = **đúng baseline**, `diff` rỗng | **0 lỗi mới**. 239 lỗi cũ có sẵn trên develop (`features/danhMuc` 129 · `muaHang` 26 …), không sửa vì ngoài phạm vi |
| `client` · vitest (module `mauIn`) | `19 tệp · 368 test · 0 fail` | |
| `client` · ESLint | 0 lỗi, 0 cảnh báo | 18 lỗi phát sinh đã **sửa thật**, không tắt rule |
| Cây commit | `??` = **0** ở cả hai repo | `cell-app` 138 thay đổi · `client` 166 thay đổi. **Chưa commit bản cuối** |

**Chưa chạy được, không phải đã chạy và bỏ qua:**
`lint:boundaries` và `vite build` (không có `npm` trên PATH — đã kiểm tay: 0 `../../` xuyên tầng, engine không import `@features/*`/`@app/*`) · toàn bộ test **Testcontainers** (máy cấm Docker) · `/qa-flow` trên trình duyệt thật.

---

## §3. Đã làm gì

### Backend `cell-app` — module `cell/mau_in`
- **12 endpoint**: `A1` GET · `A2` PUT `/{maLoai}/{maNghiepVu}` · `A3` xem-truoc · `A4` chung-tu-gan-day · `A5/A6/A7` ảnh nền · `A8` menu-in · `A9` ban-in · `A10/A11` thiet-lap-chung · `A12` logo.
  Bỏ 4 endpoint của bản cũ: danh sách 47 loại chứng từ, `DELETE` mẫu (xoá nằm trong `PUT`), 2 endpoint lịch sử phiên bản.
- **3 migration mới**: `V1158` khoá nghiệp vụ · `V1159` ảnh nền · `V1160` logo `iam_tenant`.
- **4 provider** nghiệp vụ; tầng **thiết lập chung tối thiểu** + `HoSoDonViPort`.
- Postman: `docs/json/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu.postman_collection.json` (7 nhóm, 26 request).

### Frontend `client` — engine `base/domainKit/mauIn/` (88 tệp)
Màn là **modal toàn màn mở từ form chứng từ**, **không** phải route riêng — bản cũ làm route `/he-thong/thiet-lap-mau-in`, đã gỡ trọn (20 tệp).
Đủ 3 cột, thanh xem trước (hoàn tác/làm lại 60 bước, zoom, vừa khung, lưới căn chỉnh), 4 bảng chỉnh khối chuẩn, **khối tự do dạng lưới ô kiểu Excel** (gộp/tách ô, 15 nút thanh công cụ, 10 mục menu chuột phải), màn Xem trước bản in, nút `In ▾`.
Gắn vào pilot **Chứng từ bán hàng**.

---

## §4. Những thứ CỐ Ý lệch tài liệu — BA phải soát

Chi tiết ở [04-quyet-dinh-ban-giao.md §5](04-quyet-dinh-ban-giao.md). Tóm tắt:

| # | Lệch gì | Ai quyết |
|---|---|---|
| L-1 | **Không dựng 5 bảng quan hệ** `cfg_mau_in_*`, toàn bộ lưu **JSON** | user |
| L-2 | Ảnh nền + logo lưu cột `bytea`, không base64 vào JSON | AI đề xuất |
| L-3 | Quyền = `HTMauIn.*` + `<ChucNang>.View.Detail`, không phải quyền *Thiết lập mẫu in* theo nghiệp vụ | AI đề xuất |
| L-4 | `MSG_COMMON_001` cho xung đột phiên bản · `MSG_COMMON_003` cho thiếu quyền In | AI đề xuất |
| L-5 | 2 tooltip nút In disable chỉ có key i18n, chưa có mã `MSG_` | AI đề xuất |
| L-6 | Làm thêm **tầng thiết lập chung tối thiểu** vốn thuộc epic `_20` | user |
| L-7 | Hồ sơ đơn vị tạm đọc từ Thông tin công ty vì `cfg_chi_nhanh` chưa tồn tại | AI đề xuất |
| L-8 | Áp bộ **BR Phase 2** (BR50.7 · BR51.5 · BR51.6) cho riêng chức năng này | user |

Cộng thêm ba điểm **Figma lệch tài liệu chữ** đã chốt ở [§8 của file quyết định](04-quyet-dinh-ban-giao.md):
mẫu chuẩn **đúng 4 loại khối** (Figma vẽ mẫu đã tuỳ chỉnh) · mẫu chuẩn **bật mọi lưới** · số chứng từ **không** thuộc khối Tiêu đề.

⚠ **Hệ quả nghiệp vụ lớn nhất, BA phải xác nhận:** mẫu chuẩn của một nghiệp vụ mới **không in** Khách hàng, Địa chỉ, Diễn giải, Tổng tiền hàng, Tiền thuế, Số tiền bằng chữ — người dùng phải tự thêm khối tự do. Đây là hệ quả trực tiếp của `1.function-breakdown.md`, không phải suy diễn.

---

## §5. Việc cho người vận hành — đọc trước khi deploy

1. ⛔ **`V1158` xoá dữ liệu mẫu in v1** (đổi khoá sang cặp *loại chứng từ – nghiệp vụ*).
   Trước khi chạy: `SELECT count(*) FROM prn_mau_in_tuy_chinh;` — **khác 0 thì DỪNG và hỏi**.
   Bảng này lên develop/staging ngày 2026-09-18 và chưa có API nào ghi vào, nhiều khả năng rỗng — nhưng đừng đoán.
2. `V1148` `V1149` `V1150` **đã nằm trên `origin/develop` và `origin/staging`** — không sửa tại chỗ được, mọi thay đổi DB phải là migration mới.
3. Ba migration mới **chưa chạy ở môi trường nào**.
4. **Sự cố bảo mật đã xử lý**: `application.yml` từng chứa token nội bộ thật làm giá trị mặc định (phần chưa commit). Đã đưa về `${PMKT_INTERNAL_TOKEN:}`. Kiểm chứng: **chưa bao giờ lên git** (`git log -S` trên mọi nhánh = rỗng) ⇒ không cần thu hồi. Vẫn nên xác nhận với người từng đặt giá trị đó vào máy.

---

## §6. Còn nợ

| # | Nợ | Chặn gì |
|---|---|---|
| N1 | **Lô 6 FE**: nối Chứng từ mua dịch vụ, gỡ `api/mock.ts` (còn cờ `DUNG_MOCK_KHI_BE_LOI`) | cần BE chạy thật |
| N2 | `/qa-flow` trên trình duyệt thật | chưa chạy lần nào |
| N3 | Test **Testcontainers**: RLS, GRANT sau `ADD COLUMN`, unique index thật, rollback `@Transactional` thật | máy cấm Docker |
| N4 | `lint:boundaries` + `vite build` | không có `npm` trên PATH |
| N5 | BA cấp mã `MSG_` cho: xung đột phiên bản · thiếu quyền In · 2 tooltip nút In disable | |
| N6 | BA khai **danh sách nghiệp vụ** có mẫu tuỳ chỉnh đợt đầu + **mã quyền** từng nghiệp vụ | |
| N7 | `cfg_chi_nhanh` ra đời thì đổi hiện thực `HoSoDonViPort.theoChiNhanh()` — **không** phải sửa tầng trên | |
| N8 | `XuatCatalogMauInTest` bị xoá (phụ thuộc `duLieuMau()` đã bỏ khỏi SPI) ⇒ `sync-catalog.sh` mất nguồn | |
| N9 | Postman dựng từ hợp đồng API, **chưa đối chiếu app đang chạy** | |

### Hai chỗ cần dev xác nhận
> ✅ **Đã đóng 2026-09-21** — nút `In ▾` nay nằm ở **chân popup**, cùng hàng với Lưu / Chỉnh sửa
> (Dat chốt). Kết luận ban đầu "footer không chứa được split button" là **sai**:
> `CommonModalFooter` đã có sẵn slot `rightExtraNode` (thêm 2026-08-24 cho nút in phiếu thu/chi của
> `nganQuy`), chỉ thiếu ở `mode: 'edit'` — đã mở, kèm 2 test ghim vị trí và ghim "không khoá khi
> đang lưu".

- `TenantConfigApi` mở thêm **2 method ghi** cho logo, dù API đó tự khai "chỉ mở phần đọc" (cửa hẹp 1 trường, vẫn gate `HTThongTinCongTy.Edit`).
- `mau_in` đọc/ghi `cfg_cau_hinh_he_thong` bằng **native query** vì `CauHinhHeThongApi` không lộ `phien_ban` mà `A11` cần khoá lạc quan.

---

## §7. Việc ngoài phạm vi đã xử lý luôn

| Việc | Vì sao |
|---|---|
| Vá `docs/rules/msg.sh` | Báo `THIEU-VI` **oan** cho mọi message dài hơn `printWidth` của Prettier (khoá một dòng, giá trị dòng sau). Sau khi vá epic này ra **26/26 OK**; chạy thử trên epic Phase 1 khác vẫn bình thường |
| Gỡ token thật khỏi `application.yml` | Luật 7 |
| Gỡ `CommonColorPicker` | Figma vẽ 10 ô màu + ô hex, không có picker ⇒ component thành code chết trong `@base` |
| Đánh dấu **đã thay thế** cho `docs/doing/mau-in-chung-tu{,-spec}/` | Bản dựng từ mock HTML 2026-09-17, giữ để tra lịch sử quyết định Q1–Q21 |
| `client` chuyển từ **đứng thẳng trên `develop`** sang nhánh `feat/mau-in` | Luật 8 |
| Hai repo kéo `origin/develop` về (fast-forward) | Theo yêu cầu trực tiếp, tránh conflict về sau |
