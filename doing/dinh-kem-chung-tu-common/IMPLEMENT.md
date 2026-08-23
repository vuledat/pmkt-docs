# IMPLEMENT — `@domain-kit/dinhKem` + đấu vào Chứng từ bán hàng

> Ngày: 2026-08-22 · Nguồn: `pmkt-docs/ba/Common/NguonDuLieu/SCR_FileDinhKem.md` ·
> Figma `63458-609649` (3 frame) · hợp đồng API `dinh_kem_chung_tu` do user cấp trong phiên — **hợp đồng đó nay đã bỏ, xem §1**.
> Kế hoạch nền: [`00-ke-hoach-tong.md`](00-ke-hoach-tong.md) — bản kế hoạch là **FE + BE**, lần này
> **chỉ làm FE (P4 + phần FE của P5)**.

## 1. Phạm vi đã code / chưa code

> **Cập nhật 2026-08-22 (lượt 2): FE đã di trú xong sang hợp đồng
> [`02-plan-tich-hop-qua-storage-api.md`](02-plan-tich-hop-qua-storage-api.md).** Không còn lời gọi
> nào tới `/api/chung-tu/dinh-kem`; toàn bộ tab chạy trên `/api/storage/files` với `group` = type
> nghiệp vụ (`chung-tu-ban-hang`) + `doiTuongId` = id chứng từ.

| Pha (theo plan 02) | Trạng thái |
|---|---|
| **P1 BE — `FileGroup.BAN_HANG_HOA` + config group + `Map.ofEntries` + kiểm phần mở rộng** | ✅ **xong 2026-08-22** — `./gradlew unitTest` xanh (1925 test) |
| **P2 BE — `V1036` 3 cột vào `str_file` · `FileDto` +4 trường · filter `doiTuongId`** | ✅ **xong 2026-08-23** — `./gradlew unitTest` xanh (1936 test) |
| **P3 BE — `POST /api/storage/files/gan-doi-tuong`** | ✅ **xong 2026-08-23** — kèm khử trùng tên BR02 phía server |
| **P4 FE base — `@domain-kit/dinhKem`** | ✅ **xong** (UI · BR01–BR04 · i18n · tầng api mới · 31 test xanh) |
| **P5 FE CTBH** | ✅ **xong** — popup Thêm/Sửa/Xem · panel Xem nhanh · gọi `gan-doi-tuong` sau khi Lưu |
| P6 Nghiệm thu end-to-end | ❌ chưa — chờ BE |
| P7 Job dọn tệp chưa gắn | ❌ chưa |
| P8 Các màn còn lại + backfill bảng ngân quỹ | ❌ chưa — ticket riêng |

**P1–P3 BE đã xong (2026-08-23).** Còn lại: P6 nghiệm thu end-to-end (cần MinIO + đăng nhập) và
P7 job dọn tệp chưa gắn (`doi_tuong_id IS NULL` quá 24h) — xem `02-plan…` §5.

## 2. File đã tạo / sửa

### Mới — `client/src/base/domainKit/dinhKem/` (TIER 2)

| File | Vai trò |
|---|---|
| `index.ts` | barrel + side-effect đăng ký i18n namespace `dinhKem` |
| `api/dinhKemSchema.ts` | Zod `TepDinhKem` = `FileDto` của `common/storage` (+ `tenHienThi`/`thuTu`/`doiTuongId`/`nguoiTaoTen`) · `trangTepSchema` cho `PageResponse` |
| `api/dinhKemApi.ts` | `docDinhKem(group, doiTuongId)` · `xoaDinhKem(fileId)` · `taiTepLen(tep, group, doiTuongId, onTienDo)` · **`ganDinhKem`** · `docNoiDungTep` · `dinhKemQueryKey` — tất cả trỏ `/api/storage/files` |
| `constants/constants.ts` | 5MB · 16 phần mở rộng BR02 · Nhóm 1 BR01 · cỡ trang · bề rộng cột · `STORAGE_FILE_PATH` + `STORAGE_GAN_PATH`. **Không** còn hằng số group — group do màn chủ truyền vào |
| `fields/types.ts` | `GiaTriDinhKem` (giá trị Form) · `DongDinhKem` (dòng bảng) · `GanDinhKemLenh` (phần tử payload) · `CheDoDinhKem` |
| `fields/cotDinhKem.tsx` | 6 cột theo Figma, gồm thanh tiến trình % và cụm nút Tải xuống/Xóa |
| `helpers/nhomXem.ts` | BR01 — nhóm suy từ phần mở rộng; `xemTrucTiepDuoc` · `laAnh` |
| `helpers/kiemTraTep.ts` | BR02 — chặn theo định dạng rồi mới theo dung lượng |
| `helpers/datTenKhongTrung.ts` | BR02 — hậu tố ` (1)` đặt TRƯỚC phần mở rộng |
| `helpers/doDungLuong.ts` | BR02 — KB/MB, 1 chữ số thập phân, bậc 1024 |
| `helpers/dongDinhKem.ts` | hợp nhất `daLuu` + `moi` → dòng bảng; `dinhKemGuiLen` → thân `gan-doi-tuong`; `coTepChuaGan` → có cần gọi không |
| `hooks/useDinhKem.ts` | nạp tệp đã gắn vào Form store · tải lên có % (kèm `doiTuongId` khi Sửa) · xoá theo BR03 — **`DELETE` cho cả tệp mới lẫn tệp đã gắn** |
| `hooks/useXemTep.tsx` | BR01 — mở trình xem (Modal trong trang) hoặc tải về |
| `components/DinhKemTab.tsx` | tab đầy đủ (bảng + kéo–thả + confirm xóa + trình xem) |
| `components/DinhKemPanelTab.tsx` | bản CHỈ ĐỌC cho panel Xem nhanh (không cột Chức năng) |
| `components/VungKeoTha.tsx` | khối kéo–thả, bọc `DragDropUpload` của `@base` |
| `i18n/{vi,en,registerDinhKemI18n}.ts` | MỘT namespace `dinhKem`; câu ở `msg.*` là **nguyên văn** SCR |
| `test/dinhKemHelpers.test.ts` | 23 ca logic thuần (`// @vitest-environment node`) |
| `test/dinhKemTab.render.test.tsx` | 8 ca render: BR04 · bộ cột Figma · 3 luật ẩn thao tác |

### Sửa

| File | Sửa gì |
|---|---|
| `base/components/upload/DragDropUpload.tsx` | **thêm prop `showFileList`** (mặc định `true`, không đổi hành vi cũ) — tab này vẽ danh sách tệp bằng bảng riêng nên phải tắt chip trong ô |
| `base/domainKit/index.ts` | export `./dinhKem` |
| `banHang/chungTuBanHang/components/DinhKemTab.tsx` | từ `CommonEmpty` → lớp nối: bọc `Form.Item name="dinhKem"` quanh common |
| `banHang/chungTuBanHang/components/XemNhanhTabs.tsx` | `DinhKemTabXemNhanh` dùng `DinhKemPanelTab`, đọc `row.id` |
| `banHang/chungTuBanHang/api/chungTuModule.tsx` | tab panel truyền `{locale, row}` thay vì render rỗng |
| `banHang/chungTuBanHang/api/payload.ts` | **KHÔNG** mang `dinhKem` — tệp gắn bằng lời gọi riêng sau khi Lưu |
| `banHang/chungTuBanHang/fields/types.ts` | `ChungTuBanHangFormValues.dinhKem?: GiaTriDinhKem` |
| `banHang/chungTuBanHang/constants/constants.ts` | `STORAGE_GROUP_CTBH = 'chung-tu-ban-hang'` — phải khớp `FileGroup` phía BE |
| `banHang/chungTuBanHang/components/ChungTuBanHangThemMoiModal.tsx` | cờ `daGhiSo` + truyền `rowId`/`readOnly`/`daGhiSo`/`locale` vào tab; **`handleSave` gọi `ganDinhKem` sau khi Lưu**, hỏng thì báo lỗi và KHÔNG đóng popup |
| `banHang/chungTuBanHang/i18n/{vi,en}.ts` | gỡ khoá chết `themMoi.dinhKemTab.empty`; thêm `themMoi.msg.ganDinhKemThatBai` |
| `banHang/chungTuBanHang/test/xemNhanhTabs.render.test.tsx` | đổi kỳ vọng: panel dựng bảng 5 cột, KHÔNG có cột Chức năng |
| `banHang/chungTuBanHang/test/payload.test.ts` | thêm 2 ca cho mảng `dinhKem` |

## 3. Đã reuse gì

| Dùng lại | Ở đâu |
|---|---|
| `DragDropUpload` (`@base`) | `components/VungKeoTha.tsx` — khung nét đứt + icon mây + validate `accept`/`maxSizeMB` + seam `uploadRequest` |
| `CommonListTable` + `ListField` (`@base`) | `components/DinhKemTab.tsx`, `DinhKemPanelTab.tsx` |
| `CommonConfirmModal` · `CommonButton` · `TrashIcon` · `DownloadSimpleIcon` · `GLYPH_COLOR` (`@base`) | confirm xóa + cụm nút cột Chức năng |
| `useToast` (`@base`) | 6 thông báo của SCR |
| `http` (`@platform`) | mọi request — token/tenant đã tự gắn |
| Khuôn `DinhKemPanelTab` của `nganQuy/_shared` | `fillHeight` cho panel 280px, `textMode:'long'` cho BR44, quy ước bậc 1024 |

**Viết mới (không có sẵn):** `useXemTep` — `@domain-kit/storage#useStoragePreview` suy "ảnh hay không"
từ `contentType`, còn BR01 phân nhóm theo **phần mở rộng** và còn phải phân biệt "mở được" với "phải
tải về"; cùng cơ chế (fetch blob kèm token → Modal), khác luật chọn nhánh.

## 4. Lệch so với plan / SCR / Figma — nêu hết

| # | Lệch gì | Vì sao | Ảnh hưởng |
|---|---|---|---|
| 1 | **Bảng có 6 cột**, SCR chỉ khai 2 (Tên tệp · Dung lượng) | Figma 63458:606661 vẽ thêm `#` · Người tải lên · Thời gian tải lên · Chức năng. Luật `/gen-fe`: UI theo Figma | **BE phải trả `nguoiTaiLen` + `thoiGianTaiLen`** trong `DinhKemDto`, nếu không hai cột luôn trống. Đã khai `nullish` nên không vỡ |
| 2 | **Nút Tải xuống chỉ ở Nhóm 1**, Figma vẽ nó ở CẢ dòng `.jpg` | BR01 nói rõ "Nhóm 2 không có" — đây là hành vi ⇒ theo BR | Dòng ảnh không có nút; bấm tên tệp là tải về |
| 3 | **Xem trực tiếp chỉ `.pdf` + ảnh**; `.doc/.docx/.xls/.xlsx` báo lỗi `msg.khongMoDuoc` | Phương án **C** của §5.4 plan. Không có bộ chuyển đổi phía server; Gotenberg là container ⇒ vi phạm luật cấm Docker | **Lệch BR01** — chờ BA duyệt. SCR đã lường nhánh "mở thất bại → báo lỗi, vẫn tải xuống được" nên tab không bịa gì |
| 4 | Câu trạng thái rỗng là **"Chưa có tệp đính kèm — kéo thả tệp vào đây hoặc bấm để chọn tệp"** | BR04 viết "…kéo thả tệp vào đây"; Figma nối thêm "hoặc bấm để chọn tệp" (không có nút "Chọn tệp" rời như SCR mô tả — chính khối kéo–thả là nút) | Chữ dài hơn BR04 đúng một mệnh đề |
| 5 | Dòng gợi ý dưới khối kéo–thả liệt kê **16 phần mở rộng BR02**, Figma chỉ vẽ 5 (`.doc .docx .xls .xlsx .pdf`) | Q2 của phiên: user chốt **FE theo BR02** | Chữ gợi ý dài hơn bản vẽ |
| 6 | Plan ghi "14 phần mở rộng" | Đếm lại đúng bảng BR02: 5 tài liệu + 5 ảnh + 3 nén + 3 dữ liệu = **16** | Hằng số và test đều lấy 16 |
| 7 | Tải lên bằng `POST /api/storage/files` (1 tệp/request), plan đề xuất `upload-multiple` | BR02 đòi **% tiến trình từng tệp** và "tệp hợp lệ vẫn lên, tệp lỗi báo riêng"; `upload-multiple` gộp cả lô vào một request nên mất cả hai | Nhiều request hơn khi thả 10 tệp; đổi lại đúng BR02 |
| 8 | `nhomXem` do **FE tính**, plan để BE tính sẵn trong DTO | BE chưa có; luật BR01 là "suy từ phần mở rộng", đặt ở một hàm thuần `helpers/nhomXem.ts` | Khi BE trả `nhomXem`, bỏ hàm này và đọc thẳng DTO |

## 5. Nợ kỹ thuật (phải đọc trước khi nghiệm thu)

1. **BE chưa có gì cho luồng gắn tệp.** FE đã đúng hợp đồng plan 02, nhưng phía BE `str_file` chưa
   có 3 cột (`doi_tuong_id` · `ten_hien_thi` · `thu_tu`), `GET` chưa nhận `doiTuongId`, và
   `POST /api/storage/files/gan-doi-tuong` **chưa tồn tại**. Hiện trạng hôm nay:
   - **tải lên · xem · tải xuống · xoá** chạy thật (đi thẳng `common/storage`);
   - `GET ?doiTuongId=` bị BE **bỏ qua tham số** ⇒ tab Sửa/Xem và panel Xem nhanh sẽ liệt kê mọi tệp
     của group, không lọc theo chứng từ;
   - `gan-doi-tuong` → 404 ⇒ bấm Lưu xong hiện lỗi "Đã lưu chứng từ nhưng chưa gắn được tệp đính
     kèm" và popup **không đóng** (đúng thiết kế: chứng từ đã lưu, chỉ bước gắn hỏng).
2. **Tiến trình `cell-app` đang chạy phải khởi động lại** để nạp `FileGroup.BAN_HANG_HOA` — bản
   đang chạy vẫn trả `MSG_FILE_GROUP_INVALID` với danh sách 5 group cũ.
3. ~~`STORAGE_GROUP_CTBH` chưa đối chiếu được~~ — đã chốt: `'BanHangHoa'`, khớp
   `FileGroup.BAN_HANG_HOA.code()` = `MaChucNang.BAN_HANG_HOA`. Có test canh
   (`DinhKemBanHangBr02Test#maGroup_layTuMaChucNang_khongPhaiChuoiTuDat`).
4. **Quyền `File.Create` / `File.View.Detail`** của `common/storage` phải được cấp cho vai trò kế toán,
   nếu không tab 403 với mọi người dùng thường (Q6 của plan, chưa chốt).
5. **Cột "Người tải lên" / "Thời gian tải lên" trống với tệp vừa tải trong phiên** — hai giá trị đó do
   BE điền khi chứng từ được lưu; FE không bịa.
6. Không còn `mock.ts` nào trong phạm vi lần này.
7. **Bốn bản `DinhKemTab` trùng chưa dọn** (`nganQuy/_shared`, `nganQuy/chungTuTienMat|Gui`,
   `congCuDungCu/dieuChuyen`, `kho/_shared`) — §5.5 của plan, thuộc P7, ngoài phạm vi lần này.

## 6. Kết quả cổng — lượt 2 (sau khi di trú sang `/api/storage/files`)

| Lệnh | Kết quả |
|---|---|
| `npx vitest run src/base/domainKit/dinhKem` | ✅ **31/31 xanh** (2 file) |
| `npx vitest run src/features/banHang/chungTuBanHang` | ✅ **232/232 xanh** (14 file) |
| `npx vite build` | ✅ built in 1,44s |
| `npm run typecheck` | **181 lỗi** (baseline 192; lượt trước 182). **0 lỗi trong file lần này tạo/sửa** — 3 lỗi thuộc `banHang/chungTuBanHang` đều ở file của việc dở khác (`test/payload.test.ts` dòng 220/228 là ca `chiTiet` cũ, `test/soChungTuGoiY.render.test.tsx`) |
| `npx vitest run --exclude 'src/legacy/**'` | `14 file đỏ / 30 test đỏ` trên 680 file. **Không file nào thuộc `dinhKem` hay `chungTuBanHang`** — 9/30 là `Test timed out in 5000ms` khi chạy song song cả suite; phần còn lại là engine `chungTu` (việc dở khác — cờ `dungApiDongChiTiet` không có trong HEAD), `boundaries.test.ts` thăm dò `src/features/tienGui/**` đã đổi tên, và app shell/muaHang |
| `npm run lint` · `npm run lint:boundaries` | **CHƯA CHẠY** |
| `npm run check:committed` | **CHƯA CHẠY** — chưa commit gì |

## 7. BR đã áp dụng / chưa đạt

**Đã áp dụng:** BR01 (nhóm tệp, mở/tải — trừ phần Office, xem lệch #3) · BR02 (5MB · 16 định dạng ·
kiểm từng tệp độc lập · tệp bị chặn không vào danh sách · % tiến trình · khử trùng tên · màn Xem không
tải thêm) · BR03 (nút Xóa chỉ ở Thêm/Sửa, ẩn khi đã ghi sổ, có confirm) · BR04 (hai trạng thái của
khối, thả ở bất kỳ đâu trong khối) · BR12/BR33 (đọc `trangThaiChungTu` để suy `daGhiSo`) ·
BR14 (ba chế độ SUA/XEM/PANEL) · BR15 (validation trước khi đẩy lên) · BR25 (prop `coQuyenSua`) ·
BR26 (toast 3s qua `useToast`) · BR44 (`textMode:'long'` cho tên tệp dài) · BR1/BR2 (phân trang 20,
cỡ trang 10/20/50/100).

**Chưa đạt:**

| BR | Vì sao |
|---|---|
| **BR01 — Nhóm 1 xem trực tiếp** | `.doc/.docx/.xls/.xlsx` chưa xem được (lệch #3, chờ BA chốt A/B/C) |
| **BR29.1 — xóa mềm** | Là hành vi của BE; FE chỉ gọi `DELETE`, BE chưa có |
| **BR16.1 — `MSG_COMMON_001`** khi xóa tệp của chứng từ đã ghi sổ | FE đã ẩn nút; **chặn ở API** là việc BE |
| **BR19 — không gắn một tệp hai lần vào cùng chứng từ** | Ràng buộc là unique index ở BE |
| **BR28 — multi-tenant** | RLS ở BE |
| **BR46 — trường hệ thống** | Entity ở BE |

## 8. Việc còn lại

Không liệt kê ở đây nữa để tránh hai nguồn sự thật — toàn bộ việc BE **và** danh sách file FE phải
sửa nằm ở [`02-plan-tich-hop-qua-storage-api.md`](02-plan-tich-hop-qua-storage-api.md):
§2 (thay đổi BE) · §3 (hợp đồng REST) · §4 (FE, từng file) · §6 (phân pha) · §8 (câu hỏi cần chốt).

Ba việc phải làm **trước tiên**, vì chúng chặn mọi thứ khác:

1. **Kiểm 4 quyền `File.Create` · `File.View` · `File.View.Detail` · `File.Delete`** đã cấp cho vai
   trò kế toán chưa — chưa cấp thì tab 403 với mọi người dùng thường dù code xong hết.
2. **`FileGroup.Mime.EXTENSION_BY_MIME`** đang là `Map.of` 8 cặp và `extensionFor()` **ném** —
   upload `.zip/.txt/.gif` trả **500** ngay lần đầu.
3. **Chốt Q1–Q5** của plan 02.
