# Review PR #170 — client · CN-433 Bù trừ công nợ trên Phiếu KTTH (PMKT-E-14294)

- **Ngày review:** 2026-09-05 · **Nhánh đích:** `develop` · **Merge-base:** `f2372f71` · **HEAD PR:** `4f8a75cc`
- **Phạm vi:** 61 file · +4.006/−966 · 18 commit · độ tụt so `develop`: **0** (không cần merge thử)
- **Cách chấm:** 4 lát cắt độc lập (kiến trúc/base · nghiệp vụ BR · hiệu năng · constant/i18n/git) + vòng phản biện
  trực tiếp trên các finding nặng (mở đúng `file:dòng` + trích SCR nguyên văn). Không đọc plan/`IMPLEMENT.md`.

## KẾT LUẬN: ❌ REJECT (REQUEST CHANGES sau khi gỡ Blocker)

| Mức | Số finding |
|---|---|
| **Blocker** | 1 |
| **Major** | 8 |
| Minor | 9 |
| Nit | 4 |

Điểm sáng cần ghi nhận trước: kiến trúc module rất sạch (tab Tham chiếu dựng bằng `CommonListTable` của `@base`,
mở chứng từ gốc qua registry `@domain-kit/chungTuGoc` thay vì import ngang domain, `_shared/` hợp lệ, `mock.ts`
đã xóa), cặp i18n vi/en cưỡng chế bằng `typeof`, 26/26 message đối chiếu **nguyên văn** tài liệu, nhiều BR làm
đúng (BR02 công thức MIN + chiều lãi/lỗ, BR7/BR18 làm tròn một điểm, BR3 dirty-confirm, BR43 trim, BR25.2 quyền),
và PR còn **giảm 1 lỗi** typecheck nền.

---

## 1. BLOCKER

### BL-1 · Lối vào tạo mới Bù trừ công nợ từ danh sách Phiếu KTTH — SCR cấm nguyên văn

- **Code:** `src/features/tongHop/phieuKeToanTongHop/hooks/usePhieuKttHPage.ts:137-144` (nhánh `moTaoMoi` điều
  hướng `TONG_HOP_ROUTES.buTruCongNo`), mục dropdown khai ở `:20,133-135`; quyền ở `_shared/constants/quyen.ts:5-7`.
- **Rule nguồn:** `SCR_BTCN_DanhSach.md:22-25` — *"Nút **Thêm mới** trên màn hình danh sách này **KHÔNG tạo được
  Chứng từ bù trừ công nợ**… Chứng từ bù trừ công nợ chỉ được tạo… menu **Bán hàng → Bù trừ công nợ** hoặc
  **Mua hàng → Bù trừ công nợ**"* + CLAUDE.md gốc luật 9 & §Cổng đặc tả (quyết định thiếu tên/ngày trong tài
  liệu = OPEN → cấm code phần bị chặn).
- **Vấn đề:** comment code viện "quyết định sản phẩm chốt 2026-08-27" nhưng quyết định này **không tồn tại trong
  tài liệu BA nào** (SCR/UC/messages không đổi). Lập luận kỹ thuật trong code (quyền `BuTruCongNo.Create` độc lập
  không có lối vào khác) là có thật — nhưng lối thoát đúng là mở mục menu Bán hàng/Mua hàng theo SCR, hoặc mở
  conflict hỏi BA, không phải tự chế lối vào bị cấm.
- **Hậu quả:** người dùng có lối vào nghiệp vụ mà BA cấm; nếu BA giữ BR2 phải gỡ dropdown + quyen.ts + nhánh điều hướng.
- **Gỡ chặn:** BA xác nhận bằng văn bản (ghi vào tài liệu epic / conflict log có tên + ngày) → hạ về hợp lệ.

## 2. MAJOR

| # | Finding | Bằng chứng | Rule nguồn |
|---|---|---|---|
| M1 | **Số chứng từ hạ từ bắt buộc→tùy chọn, không tự sinh khi mở màn; MSG_014 thành message chết.** Xung đột với quy tắc nền tảng (PMKT-U-16693, `BaseChungTuRequest` không `@NotBlank`) là CÓ THẬT và được ghi trong code — nhưng FE tự chọn phương án thay vì hỏi BA; SCR đòi hiển thị số tự sinh trước khi lưu và cho sửa theo `ChoPhepSuaSo` | `helpers/kiemTra.ts:116-135` · `i18n/vi.ts:142` (placeholder tự chế) | `SCR_BTCN_ChungTu_ThemMoi.md:26` (Bắt buộc=Y, "Tự sinh theo cấu hình đánh số", BR05, MSG_014/015) + luật 9 |
| M2 | **"Tick đi theo tiền"** — dòng phải trả đã tick nhưng không được cấp tiền bị tự bỏ tick (kể cả tick người dùng vừa bấm); nguồn viện dẫn là màn Đối trừ CN-430 (epic KHÁC). Test `phanBo.test.ts:36-43` dán nhãn "ví dụ nguyên văn của BA" trong khi ví dụ BA không nói C hết tick | `helpers/phanBo.ts:79-86,104-120` · `hooks/useBuTruSetup.ts:227-239` | `SCR_BTCN_BuTru.md` BR02 (dòng 122-138) + luật 9 (nghiệp vụ không nguồn) |
| M3 | **Tab Tham chiếu chế độ XEM luôn rỗng** (`thamChieu: []`), BR41.3 (thêm/xóa dòng thủ công) chưa có; FE không gọi API tham chiếu nào, giấu khoảng trống bằng bảng trống | `components/ThamChieuTab.tsx:24-26` · `ChungTuBuTruModal.tsx:102-107` | BR41.2/BR41.3 + `SCR_BTCN_ChungTu_ThemMoi.md` BR03 (dòng 144) |
| M4 | **Nợ quy trình Cổng đặc tả:** chưa có `docs/doing/PMKT-E-14294-*-spec` (chưa `/audit-spec`), không mã luật `R-…` trong code/test → `trace.sh` không chạy được; `msg.sh`: **THIEU 22 · CHUA-DAT 4** (mã `MSG_…` không thành key/hằng — key i18n dùng tên ngữ nghĩa; nội dung đã đối chiếu tay: nguyên văn 26/26) | toàn module | CLAUDE.md gốc §Cổng đặc tả + `truy-vet-luat.md` §6 |
| M5 | **Phân trang máy chủ "giả" + tải lại trọn tập mỗi tương tác:** `layDuLieu` tải toàn phạm vi hai bên rồi `catTrang`/`locTheoTuKhoa` cắt ở client; `queryKey` chứa `request` + `timKiem` → mỗi lần lật trang/đổi cỡ trang/gõ từ khóa = một POST full-scope mới có nội dung y hệt. 5.000 khoản nợ/bên → mỗi nhịp tương tác tải lại 10.000 dòng để hiển thị 10 | `api/buTruCongNoApi.ts:104-119,151-163` (docblock tự nhận "cái giá") · `api/queries.ts:89-104` | checklist-fe §E; phần tải-một-lần là nợ BE (đã ghi FOUNDATION_FOLLOW_UP), phần tải-LẠI mỗi tương tác là của FE — key bỏ `timKiem`, cắt trang bằng `select`/`useMemo` là đủ |
| M6 | **4 endpoint master-data tin bằng generic axios, không Zod** — `laTkCongNo`/`doiTuongLienQuan`/`trangThai`/`capToChuc` được filter TRƯỚC mọi parse; BE đổi tên trường → combo TK rỗng im lặng. Comment "Toàn bộ dữ liệu vào đều đi qua Zod parse" (`buTruCongNoApi.ts:14`) không đúng cho lớp wire | `api/danhMucApi.ts:80-99,165-171,174-185` | `client/CLAUDE.md §11.2` (BẮT BUỘC parse dữ liệu ngoài) |
| M7 | **Hằng gốc REST chép đôi:** `PHIEU_KTTH_BASE` (`_shared/api/phieuKtthChiTiet.ts:30`) trùng giá trị `BASE_PATH` (`phieuKeToanTongHop/constants/constants.ts:17`), docblock tự thú "đổi cả hai". Hướng đúng: dời lên `_shared/constants` — đúng mẫu PR này đã làm với `QUYEN_TAO_BU_TRU_CONG_NO` | hai file trên (đã kiểm trực tiếp, trùng từng ký tự) | checklist-fe §D + conventions-chung §1.2 — lỗi hay gặp **#7** |
| M8 | **MSG_010/_011/_012 không bao giờ hiển thị:** ô Số tiền bù trừ bị kẹp im lặng vào [0, số dư]; `kiemTraSoTienBuTru` — hàm duy nhất phát 3 message — không được component nào gọi (chỉ test gọi) | `helpers/kiemTra.ts:97-107` · `hooks/useBuTruSetup.ts:295-311` | `SCR_BTCN_BuTru.md` bảng "Số tiền bù trừ" (dòng 63, 94) + 6.messages.md |

## 3. MINOR

1. **TK 515/635 hardcode suy từ số hiệu** thay vì "theo cấu hình" — `api/danhMucApi.ts:25-27,91-94,112-113` (SCR BR04; đã ghi chú tạm vì BE chưa lộ cấu hình).
2. **PAGE_SIZE_MAC_DINH = 10 lệch BR1 (20)** — `constants/constants.ts:40-46`; căn cứ chỉ là Figma, chưa có xác nhận BA.
3. **Tham chiếu thành TAB riêng** (SCR khai Hyperlink trong Thông tin chung) theo "quyết định coordinator 2026-09-05" không có trong tài liệu; link mở chứng từ gốc mới hỗ trợ 3 loại BH/MH/TLHB — `ThamChieuTab.tsx:15-17` · `useMoChungTuGocBuTru.ts:28-32` (BR35).
4. **Test "phân trang máy chủ" mock ngay trên lớp đang tự cắt trang** → xanh mà không ghim được điều nó đặt tên; comment `ChungTuBuTruTable.tsx:10` ghi "phân trang PHÍA MÁY CHỦ ← BR1" không đúng hiện thực — `test/phanTrangMayChu.render.test.tsx:107-113`.
5. **`layLookupThat`/`timDoiTuongThat` ghim vỏ response trần** (`res.data.data`) không dùng lưới an toàn `danhSach()` chính file này dựng — `danhMucApi.ts:81-89,175-184`; đổi vỏ → query treo pending vĩnh viễn.
6. **3 popup nằm phẳng ở `components/`** thay vì `components/modal/` (nợ cũ nhưng PR sửa sâu đúng các file này mà không `git mv`) — `client/CLAUDE.md §5` luật cứng 4; lỗi hay gặp **#1** (mức nhẹ).
7. **`staleTime: 5*60*1000` lặp 2 chỗ không tên** — `api/queries.ts:50,63` (luật 1).
8. **Drive-by fix casing kho (`0466d41e`) trộn vào PR nghiệp vụ tongHop** — 4 file `kho/phieuNhapDieuChuyen`; fix đúng nhưng nên tách PR (conventions-chung §4.1). FieldLabel (`203bcdff`) và MuaHangHoaModal phục vụ trực tiếp CN-433 — hợp lệ.
9. **Commit `cb1c4d92` thiếu `(scope)` và gộp 2 fix** — conventions-chung §4.1.

## 4. NIT

1. Test mới `themMoiBuTruCongNo.render.test.tsx:35` mock bằng `../../../../platform/...` thay vì alias (tiền lệ tại chỗ nên chỉ Nit).
2. Lớp `_shared/styles/` là lớp mới chưa có trong rule/tiền lệ (banHang/_shared chỉ có api/ + constants/) — nên chốt thành lệ trước khi domain khác bắt chước.
3. Import casing `ChiTietNdcColumns.tsx` được khắc sâu thay vì `git mv` về camelCase theo ngoại lệ §10 (file trả descriptor).
4. Docblock mồ côi giữa `LOAI_TIEN_WIDTH` và `COT_CHUNG_TU_WIDTH` — `buTruCongNo/constants/constants.ts:99-101`. · Tiêu đề popup theo Figma khi conflict C1/Q3 tự ghi là chưa chốt — `i18n/vi.ts:125-127`.

## 5. Bảng 7 lỗi hay gặp

| # | Mục | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ⚠ gần đạt — cấu trúc mới đều đúng ngăn; sót 3 popup ở `components/` gốc (Minor 6), `_shared/styles/` chưa có lệ (Nit 2) |
| 2 | Không đánh lại version migration | ✅ không áp dụng (PR thuần FE, không migration) |
| 3 | Chưa test lại sau merge | ✅ độ tụt = 0, test chạy trên chính HEAD PR |
| 4 | N+1 / chưa tối ưu | ❌ M5 — tải lại trọn tập mỗi lượt lật trang/gõ tìm kiếm |
| 5 | Chưa tận dụng BaseController/BaseEntity (BE) | ✅ không áp dụng (PR thuần FE) |
| 6 | Chưa tận dụng base FE | ✅ tốt — `CommonListTable`, registry `@domain-kit/chungTuGoc`, sửa `FieldLabel` tại base thay vì copy ra feature |
| 7 | Constant đặt sai chỗ | ❌ M7 (hằng REST chép đôi) + Minor 7 (staleTime); phần còn lại đặt đúng `constants/`/`_shared/constants/` |

## 6. Nghiệp vụ không có nguồn (tự thêm, cần BA xác nhận hoặc gỡ)

1. Tự bỏ tick dòng không được cấp tiền — `phanBo.ts:79-86,104` (nguồn viện dẫn là epic CN-430 khác) → M2.
2. Fallback chi nhánh = đơn vị GỐC (`capToChuc === 'GOC'`, `chaId == null`) — `danhMucApi.ts:146-171` (Phase 1 không có BR chi nhánh).
3. Placeholder "Để trống để hệ thống tự cấp số" — `i18n/vi.ts:142` (text UI không có trong 6.messages.md/SCR).
4. `MAX_LEN_LY_DO = 500` — `constants.ts:51` (SCR khai "-", 500 mượn từ Diễn giải).
5. `tyGia` gửi `null` trong body lưu — `payload.ts:83-87,112` (hợp đồng BE, không có trong BA).
6. Toast kép "Lưu thành công" + "Ghi sổ thành công" cho một lần Lưu-và-ghi-sổ — `ChungTuBuTruModal.tsx:161-162`.

## 7. Kết quả cổng lệnh (chạy thật trên worktree HEAD PR, so baseline đo tại merge-base)

| Cổng | PR | Baseline (merge-base) | Kết luận |
|---|---|---|---|
| `npx vitest run src/features/tongHop src/features/kho/phieuNhapDieuChuyen` | 422 pass / **1 fail** | test fail (`khoaSo/duongVaoManKhoaSo`) **cũng đỏ tại merge-base** | ✅ nợ nền, không do PR |
| `npx vite build` | ✅ 12,14s | — | ✅ |
| `npm run typecheck` | **179 lỗi** | 180 lỗi | ✅ PR giảm 1 |
| `npm run lint` | 67 error | 67 error | ✅ không xấu hơn |
| `npm run lint:boundaries` | 92 error | 92 error | ✅ không xấu hơn |
| Full vitest (`--exclude src/legacy/**`) | (điền khi suite chạy xong) | nền 16 đỏ (doc 2026-08-13) | — |

Ghi chú trung thực: `npm run check:committed` **không chạy** (máy Windows này cho ~5133 báo động giả);
các số lỗi nền lint/boundaries đã trôi so với tài liệu 2026-08-13 (9+2→67, 76→92) — trôi ở **cả hai phía**
merge-base/PR, không do PR này.

## 8. Truy vết & BR đã đối chiếu

- `trace.sh`: **không chạy được** — chưa có thư mục spec (xem M4).
- `msg.sh` (shim quét đúng worktree PR): `Tong 26 message (tang=fe): OK 0 · LECH 0 · THIEU-VI 0 · CHUA-DAT 4 · THIEU 22`
  — toàn bộ do mã `MSG_…` không thành key/hằng; nội dung 26/26 đối chiếu tay **nguyên văn** khớp tài liệu.
- BR chung đã chạy `br.sh`: **3 · 7 · 14 · 15 · 16 · 18 · 21 · 26 · 34 · 35 · 41 · 43**. BR nội bộ màn đọc qua
  `scr.sh` trên 5 file SCR của `pmkt-docs/ba/PMKT-E-14294_BuTruCongNo/5.screens/`.

## 9. Việc đề nghị theo thứ tự

1. Đưa BL-1 + M1 + M2 (+ Minor 2, 3 và mục §6) ra BA chốt — đúng một buổi, tất cả cùng một cụm "quyết định
  miệng chưa vào tài liệu". Chạy `/audit-spec pmkt-docs/ba/PMKT-E-14294_BuTruCongNo` để có sổ conflict chính thức (M4).
2. FE tự sửa không cần BA: M5 (bỏ `timKiem` khỏi queryKey + cắt trang bằng select), M6/Minor 5 (Zod cho master-data),
  M7 (dời hằng lên `_shared/constants`), M8 (nối `kiemTraSoTienBuTru` vào UI hoặc xin BA bỏ message), Minor 7.
3. Tách commit `0466d41e` (fix kho) sang PR riêng nếu quy trình cho phép.
