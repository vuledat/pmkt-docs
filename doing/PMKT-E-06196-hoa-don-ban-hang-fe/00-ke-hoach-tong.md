# Kế hoạch FE — PMKT-E-06196 Hóa đơn bán hàng

> **Trạng thái:** DRAFT — chờ review (1 BA + 1 Dev FE + 1 Design) · **Ngày sinh:** 2026-08-20 (lần 2,
> ghi đè bản 12/08) · **Người review:** _(điền khi review)_
>
> **Vì sao chạy lại `/plan-fe`:** tài liệu BA của epic đổi ở 2 commit ngày 17/08
> (`d23d1e20d`, `25f9a7ca6`) sau khi màn đã được **CODE THẲNG** ngày 12/08 (không qua `/plan-fe`).
> File cũ `IMPLEMENT.md` trong thư mục này **không phải** đầu ra của `/plan-fe` — nó là nhật ký thi
> công của `/gen-fe` (tự ghi rõ ở dòng 4: *"Không có plan FE cho epic này — user chọn code thẳng từ
> PYC"*). Bộ file `00…NN` dưới đây là bản `/plan-fe` **đầu tiên** của epic này, sinh SAU khi code đã
> tồn tại — vai trò của nó đổi từ "kế hoạch trước khi code" sang **"đối chiếu as-built ↔ BA hiện hành
> + chốt kế hoạch cho phần còn nợ"**. `IMPLEMENT.md` **giữ nguyên, không xoá** — code
> (`api/model.ts:15`, `api/hoaDonBanHangApi.ts`) đang trỏ thẳng vào nó làm nhật ký gỡ nợ; xoá sẽ để
> lại tham chiếu treo. Đọc mục 2 và mục 11 dưới đây để biết đã đối chiếu những gì.

| UC | Màn hình (`SCR_*`) | Figma | Module FE | Domain | API phụ thuộc |
| :-- | :-- | :-- | :-- | :-- | :-- |
| PMKT-u-06456_DanhSach | `SCR_HDBanHang_DanhSach` | node `58263:162967` | `hoaDonBanHang` | `banHang` | `POST /api/ban-hang/hoa-don-ban-hang/tim-kiem`, `GET .../cot`, `GET .../{id}` |
| ThemMoi | `SCR_HDBanHang_ThemMoi` | node `14770-349117` | `hoaDonBanHang` | `banHang` | `POST /api/ban-hang/hoa-don-ban-hang` (⚠ BE chưa cài — xem §2) |
| PMKT-U-06458_CapNhat | `SCR_HDBanHang_CapNhat` | = ThemMoi | `hoaDonBanHang` | `banHang` | `PUT .../{id}` (⚠ BE chưa cài) |
| PMKT-U-06466_ChiTiet | `SCR_HDBanHang_ChiTiet` | *(chưa có link riêng)* | `hoaDonBanHang` | `banHang` | `GET .../{id}` (header đã thật, `chiTiet` luôn `null` — xem §2) |
| PMKT-U-06459_Xoa | `SCR_HDBanHang_Xoa` | *(đang bổ sung)* | `hoaDonBanHang` | `banHang` | `DELETE .../{id}`, `POST .../xoa-hang-loat` (⚠ BE chưa cài) |

---

## 0. Quyết định đã chốt

Toàn bộ 2 quyết định lớn của epic đã chốt **trước khi code** (12/08, ghi ở `IMPLEMENT.md §1`) và vẫn
đúng sau khi rà lại BA doc 20/08 — không quyết định nào cần đổi.

| # | Quyết định | Hệ quả lên code | Vì sao KHÔNG chọn phương án kia |
| :-- | :-- | :-- | :-- |
| **D1** | Hóa đơn **không hạch toán** (BR04) → dựng UI ghi sổ theo Figma nhưng khoá sau cờ biên dịch `HDBH_CO_GHI_SO = false` (`constants/constants.ts:147`) thay vì bỏ hẳn nút | Nút "Xem dữ liệu ghi sổ" / "Lưu và ghi sổ" không lên DOM khi cờ tắt; bật cờ = mở lại UI đã có sẵn, không phải viết lại từ đầu | Bỏ hẳn markup thì khi BA lật quyết định (hiện chưa, nhưng BR20 của CTBH vẫn đang được BA tinh chỉnh tích cực — xem §11) phải code lại từ đầu; Figma đã vẽ sẵn layout nên giữ rẻ hơn xoá |
| **D2** | Hóa đơn là **module riêng + route riêng** (`/ban-hang/hoa-don-ban-hang`), không nhét vào trong `chungTuBanHang`; 4 tab của nhóm Bán hàng dùng chung từ vựng ở `banHang/_shared/constants/banHangTabs.ts` | `features/banHang/hoaDonBanHang/` là `leaf` riêng theo §5; `_shared` chỉ giữ path + khoá tab, **không** giữ logic nghiệp vụ | Nhét vào trong `chungTuBanHang` vi phạm luật cứng 2 (không tách màn theo hành vi) ngược chiều — đây là 2 màn thật, không phải 2 chế độ của 1 màn; Figma vẽ 1 thanh tab dùng chung nhưng đó là bố cục UI, không phải cấu trúc module |
| **D3** *(mới, chốt khi rà lại lần này)* | Bộ file `/plan-fe` **KHÔNG thay thế** `IMPLEMENT.md` — cả hai cùng tồn tại trong thư mục, mỗi file một vai trò (kế hoạch/đối chiếu vs. nhật ký thi công) | Không xoá `IMPLEMENT.md`; `git status` sau khi ghi đè vẫn thấy đủ 2 loại tài liệu | Code đang `import`-tham-chiếu `IMPLEMENT.md` bằng docblock (`api/model.ts:15`, `api/hoaDonBanHangApi.ts` docblock) — xoá tạo tham chiếu treo mà `/plan-fe` không có quyền sửa code để vá lại |

---

## 1. Phạm vi

**Trong phạm vi** (không đổi so với 12/08): 5 màn `SCR_HDBanHang_DanhSach` · `_ThemMoi` · `_CapNhat` ·
`_ChiTiet` · `_Xoa`, dựng trên module `features/banHang/hoaDonBanHang/` đã tồn tại — bản `/plan-fe`
này ghi lại đúng phạm vi đã build, không mở rộng.

**NGOÀI phạm vi:**

- **Ghi sổ / Bỏ ghi sổ hóa đơn** — BR04 của epic nói rõ "không phát sinh bút toán"; UI có nhưng khoá
  cờ (D1). Chưa có hợp đồng API ghi sổ trong PYC.
- **Phát hành hóa đơn điện tử (kết nối CQT)** — `SCR_HDBanHang_ThemMoi.md` dòng 7: *"chưa kết nối API
  CQT để phát hành (sẽ triển khai sau)"*.
- **Hành động "Lập chứng từ bán hàng / bán dịch vụ" từ danh sách** (BR04 · BR05 của
  `SCR_HDBanHang_DanhSach`) — nút có, gác đúng điều kiện, nhưng **hành động thật** (mở màn Thêm mới
  CTBH/CTBDV có auto-fill) nằm ngoài phạm vi kỹ thuật của module này: `chungTuBanHang` là `leaf` anh
  em, luật tầng cấm `leaf` import `leaf` (xem §3 kế hoạch reuse). PYC-U-06459 (Chứng từ bán dịch vụ)
  còn chưa có module FE nào cả.
- **BE ghi (Thêm/Sửa/Xóa/Xóa hàng loạt) và dòng chi tiết hàng hóa của `GET /{id}`** — xem §2, đây là
  nợ kỹ thuật đang chờ BE, không phải việc của lần chạy `/plan-fe` này.

---

## 2. Hiện trạng đã khảo sát

### 2.1 Bốn câu hỏi bắt buộc (`fe-khung-kien-truc-chuan.md §4`)

| # | Câu hỏi | Trả lời | Bằng chứng |
| :-- | :-- | :-- | :-- |
| 0 | Code ở đâu? | `client/src/features/banHang/hoaDonBanHang/` | đã tồn tại — 47 file, ~9.167 dòng (`find … \| wc -l`, chạy 20/08) |
| 1 | Màn loại nào? | Chứng từ (nhưng KHÔNG hạch toán — biến thể "chứng từ thương mại") | `package-info.java:7` BE: *"Hóa đơn KHÔNG phải chứng từ kế toán"* |
| 2 | Đã có engine chưa? | Không dùng `@domain-kit/chungTu` (engine đó giả định có ghi sổ); dựng thủ công trên `@base` giống `chungTuBanHang` | `helpers/*`, `api/chungTuModule.ts:8` (`capabilities: { ghiSo: false, boGhiSo: false }`) |
| 3 | Component đã có ở `@base` chưa? | Có — 12+ component tái dùng, xem bảng §3 | `client/src/base/index.ts` |
| 4 | Domain đang chạy không? | Có — route đã nối tay | `client/src/features/banHang/routes.tsx:66-72` |

**API BE đã có chưa? (khảo sát MỚI, quan trọng nhất của lần chạy này):**

- `cell-app/src/main/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/` **ĐÃ TỒN TẠI** (không có ở lần khảo sát
  12/08) — module Modulith đầy đủ `internal/{controller,dto,entity,model,repository,service}`.
- Phạm vi thật (package-info.java:19-24): **chỉ màn DANH SÁCH** — `POST /tim-kiem`, `GET /cot`,
  `GET /{id}` **ở mức HEADER**. `GET /{id}` trả `chiTiet = null` (dòng chi tiết hàng hóa CHƯA cài).
  Ba endpoint ghi (Create/Update/Delete) bị **chặn tường minh 400** ngay ở controller
  (`HoaDonBanHangController.java:72-93`, hàm `chuaCai(...)`) — không phải quên implement, là chốt có
  chủ ý theo "kế hoạch F2-F5" (nhắc tới trong Javadoc nhưng chưa có file kế hoạch BE tương ứng trong
  `docs/doing/`).
- FE đã đối chiếu và **khớp gần như 1:1**: `HoaDonBanHangDto.java:24-75` ↔
  `client/…/hoaDonBanHang/api/model.ts:104-175` (`hoaDonBanHangRowSchema`) — cùng tên trường
  (`soHoaDon`, `kyHieuHoaDon`, `mauSoHoaDonId`, `loaiNghiepVu`, `maSoThue`, `cccd`,
  `trangThaiPhatHanhHoaDon`, `hoaDonLienQuan`…), cùng quy ước enum **TÊN HẰNG** thay vì chuỗi tiếng
  Việt (`package-info.java:26-30` ↔ `constants.ts:94-95` dùng `'CHUA_PHAT_HANH'`/`'DA_PHAT_HANH'`).
  DTO có thêm 2 trường FE chưa đọc: `chungTuBanId`, `phienBan` — không phải lỗi (Zod bỏ qua khoá lạ),
  nhưng là việc nên làm khi BE mở thêm luồng ghi (§10).
- `client/…/hoaDonBanHang/api/hoaDonBanHangApi.ts:44`: `HDBH_DUNG_MOCK = false` — **đã tắt mock cho
  luồng đọc** từ 2026-08-14 (ghi rõ ở dòng 38 file đó), sớm hơn cả đợt code 12/08 tưởng. `api/mock.ts`
  vẫn còn trong cây nguồn (355 dòng) vì `xoaHoaDonHangLoat()` (dòng 140-147) vẫn gọi nhánh mock khi cờ
  bật — hiện cờ tắt nên nhánh đó chết nhưng file chưa xoá được vì BE chưa có `/xoa-hang-loat` thật.
  ⚠ **Docblock đầu `hoaDonBanHangApi.ts` (dòng 12-15) và đầu `model.ts` (dòng 5) vẫn viết "BE CHƯA
  CÓ"** — câu này đã LỖI THỜI so với thực tế (BE có rồi, chỉ thiếu phần ghi + chi tiết). Không sửa ở
  đây (`/plan-fe` không code) — ghi vào Q1 (§12) để dev sửa comment khi chạm lại file.

### 2.2 Đối chiếu 2 commit BA đổi tài liệu (17/08) — không có drift code

| Commit | Nội dung | Ảnh hưởng lên code hiện có |
| :-- | :-- | :-- |
| `d23d1e20d` "đồng bộ tên entity ldm - scr field" | Đổi bí danh entity trong **văn bản tài liệu** từ PascalCase (`HoaDonBan.X`, `ChungTuBan.X`, `PhieuThu.X`, `PhieuXuatKho.X`, `MauSoHoaDon.X`) sang tên bảng thật snake_case (`sal_hoa_don_ban_hang.X`, `sal_chung_tu_ban.X`, `cash_phieu_thu.X`, `inv_phieu_xuat_kho.X`, `mst_mau_so_hoa_don.X`) trên **cả 06196** (`5.screens/SCR_HDBanHang_DanhSach.md`, `SCR_HDBanHang_ThemMoi.md`, `Matrix/…_MaTranAnHien.md`) **và 06194** (`SCR_CTBH_ThemMoi.md`, toàn bộ 5 tab) | **KHÔNG có trường nào đổi tên thật** — đối chiếu từng dòng diff (`git show d23d1e20d`) xác nhận chỉ tiền tố đổi, cột `Field` (`NgayHoaDon`, `SoHoaDon`, `TenKhachHang`…) giữ nguyên. FE dùng camelCase JSON (`ngayHoaDon`, `soHoaDon`…) vốn đã khớp; DTO thật của BE (`HoaDonBanHangDto.java`) cũng camelCase — **không có gì để sửa trong Zod schema hay `fields/types.ts`.** |
| `25f9a7ca6` "gom mo ta sinh but toan…" | Bỏ "Tab Hạch toán" khỏi danh sách tab bị lược trong `Matrix/_scope.md` — vì CTBH (nguồn tham chiếu) **chưa từng có** tab này, ghi thêm vào danh sách loại trừ là sai, không phải do phạm vi HĐBH đổi | `grep -rn "hạch toán" hoaDonBanHang --include="*.ts*"` (đã chạy) xác nhận **0 chỗ** trong code cài markup/route/component tên "Tab Hạch toán" hay bất kỳ UI ghi sổ nào ngoài cờ `HDBH_CO_GHI_SO` đã có sẵn (D1). **Zero drift.** |

### 2.3 Phát hiện THÊM — churn của `SCR_CTBH_ThemMoi.md` vượt ngoài 2 commit trên

`SCR_CTBH_ThemMoi.md` (file 06194 mà HĐBH tham chiếu trực tiếp cho toàn bộ Tab Hóa đơn / Thông tin bổ
sung / Lựa chọn Loại tiền-Chiết khấu / Tab Chi tiết hàng hóa / Dòng tổng) đổi **7 lần khác** từ
13/08 → 20/08 (hôm nay), không chỉ 2 commit được nêu trong yêu cầu chạy lại:

```
7215f4a41  20/08  Merge … RefactorV5           602 dòng đổi trên SCR_CTBH_ThemMoi.md
beaf3662a  20/08  update                          2 dòng
bb4c10eb9  19/08  chuan hoa quy tac ghi so…      50 dòng
8b7fac043  17/08  bo mo ta loc trang thai…        6 dòng
715907142  16/08  cập nhật entity                58 dòng + 3.crud-matrix.md của 06196 (18 dòng)
b15f479bc  15/08  chuẩn hóa Control/Max length   50 dòng
06b72a7b4  15/08  chuẩn hóa liên kết công nợ…    15 dòng
920baf04e  13/08  tach entity riêng…            431 dòng
```

**Đã đối chiếu:** đọc trực tiếp bản HEAD của `SCR_CTBH_ThemMoi.md` (1.613 dòng) ở 5 section HĐBH
tham chiếu — `#tab-hóa-đơn` (dòng 82-107), `#thông-tin-bổ-sung` (155-171),
`#lựa-chọn---loại-tiền-chiết-khấu` (174-189), `#tab-chi-tiết-hàng-hóa` (190-247, phần cột KHÔNG
thuộc nhóm hạch toán), `#dòng-tổng-tiền` (266-302) — và số hiệu BR (BR01, BR06-BR15, BR23, BR24) mà
`SCR_HDBanHang_ThemMoi.md` trích dẫn. Kết quả: **cấu trúc trường và số hiệu BR ổn định**, các anchor
Markdown không đổi tên, danh sách trường không thêm/bớt so với những gì `fields/chiTietFields.ts` và
`fields/types.ts` đã code. Điểm đáng chú ý:

- **Lệch số BR đã nêu ở `IMPLEMENT.md §4.3` (12/08) nay đã TỰ HẾT** — khi đó `SCR_HDBanHang_ThemMoi.md`
  trỏ `#BR08/#BR10/#BR11…` lệch 1 so với CTBH. Bản HEAD hiện tại của `SCR_HDBanHang_ThemMoi.md`
  (đọc lại 20/08) đã dùng đúng số hiệu hiện hành (BR01, BR06, BR07…BR14, BR23, BR24) — khớp 100% với
  `SCR_CTBH_ThemMoi.md` HEAD. Ai đó (không rõ commit nào trong danh sách trên) đã sửa; ghi nhận đây
  **không phải việc cần làm nữa**, chỉ để `IMPLEMENT.md §4.3` không còn đúng hiện trạng.
- Riêng BR20 "Sinh bút toán hạch toán" (dòng 1130-1283 của CTBH, bị viết lại lớn ở `bb4c10eb9`) và
  BR21 "Ghi sổ và Bỏ ghi sổ" — **không áp dụng cho HĐBH** (BR04 loại trừ toàn bộ khối hạch toán), nên
  churn ở 2 BR này không kéo theo việc gì phải sửa ở module `hoaDonBanHang`.
- **Chưa** đối chiếu dòng-theo-dòng toàn bộ 1.613 dòng của CTBH — phạm vi `/plan-fe` này giới hạn ở
  các section HĐBH trích dẫn trực tiếp. Nếu BA có ý định đổi tiếp CTBH theo hướng ảnh hưởng field
  KHÔNG thuộc 5 section trên, đưa vào Q2 (§12).

---

## 3. Kế hoạch reuse

Module đã build đúng luật "reuse trước, viết mới sau" — bảng dưới là bằng chứng, không phải đề xuất.

| Cần | Có sẵn ở đâu (`file:dòng`) | Dùng lại hay viết mới | Lý do |
| :-- | :-- | :-- | :-- |
| Bảng danh sách + toolbar + chip lọc + dòng tổng + chọn hàng loạt | `CommonListTable` — `src/base/index.ts:310` | Dùng lại | Đúng shape BR1·BR2·BR31·BR45 |
| Lưới nhập liệu (ô, cascade, dòng ghi chú, Σ) | `CommonEditableGrid` — `src/base/index.ts:535` | Dùng lại | BR21 |
| Khung popup + guard "bỏ thay đổi" + footer 2 chế độ | `CommonModalShell` — `src/base/index.ts:258` | Dùng lại | BR3, BR13.2 |
| Popup kết quả xóa hàng loạt (đã thêm cột `tenDoiTuong`) | `BulkDeleteResultModal` — `src/base/index.ts:293`; prop mới ở `base/components/modal/BulkDeleteResultModal.tsx` | Dùng lại + **đã thêm prop optional** | SCR_HDBanHang_Xoa cần cột "Tên khách hàng" — reuse đúng luật "thiếu prop nhỏ thì thêm vào `@base`" thay vì copy ra feature |
| Popup xác nhận (Xóa · cảnh báo BR02/BR10) | `CommonConfirmModal` — `src/base/index.ts:269` | Dùng lại | BR16 |
| Khối tổng 1-2 cột | `TotalBreakdown` — `src/base/index.ts:205` | Dùng lại | Tổng hợp tiền tệ |
| Thanh 4 tab dạng thẻ | `TabMenu2Level` — `src/base/index.ts:142` | Dùng lại | D2 |
| Phễu ngày + lọc nâng cao + chip | `useListFilter` · `CommonFilterPanel` — `:501` · `:476` | Dùng lại | BR8, BR11 |
| Adapter CRUD + query theo tenant | `createSearchApi` · `createSearchQueries` — `@platform` `:141`, `:143` | Dùng lại | Đúng hợp đồng BASE-CRUD của `BaseCrudController` |
| **Toàn bộ kiến trúc module** (9 lớp, 1 namespace i18n) | `features/banHang/chungTuBanHang/` | Dùng lại làm khung | Mẫu tham chiếu duy nhất, `client/CLAUDE.md §5` |
| `helpers/*` (tinhToan · tongHop · chietKhau · anHien · kiemTra · trangThai · dongBo) | — | **Viết mới**, có lý do | Luật tầng cấm `leaf` import `leaf` anh em; bản HĐBH cũng là tập con thật sự (bỏ giá vốn + mọi TK hạch toán) chứ không phải bản sao nguyên. Trùng lặp ~500 dòng với `chungTuBanHang` là **nợ đã biết** (N9, §10), ticket gom lên `@domain-kit/chungTu` để ngoài phạm vi PYC này. |
| `api/lookups.ts` (7 danh mục) | — | Viết mới, lý do như trên | |
| `components/ThongTinHoaDon.tsx` · `ThongTinXuatKhau.tsx` | — | Viết mới | Bố cục trường riêng màn, không component `@base` nào vẽ section form nghiệp vụ |
| `components/*Tab · *ListTable · *QuickDetail · *ThemMoiModal · TongHopPanel · GridHeaderActions · PhanBoChietKhauModal` | — | Viết mới | Mang logic nghiệp vụ riêng màn; phần trình bày thuần đã đẩy xuống `@base` |

---

## 4. Kiến trúc module — cây thư mục đã sinh

Đúng chuẩn §5 `client/CLAUDE.md` — gốc module chỉ có `index.ts`, popup ở `components/modal/`… **có
một sai khác với luật cứng 4 cần ghi nhận:**

```
features/banHang/hoaDonBanHang/
├── index.ts
├── api/            model.ts · hoaDonBanHangApi.ts · queries.ts · mock.ts(nợ) · lookups.ts
│                   · payload.ts · formDetail.ts · chungTuModule.ts
├── components/     HoaDonBanHangTab · …ListTable · …QuickDetail · …ThemMoiModal ·
│                   ThongTinHoaDon · ThongTinXuatKhau · GridHeaderActions · TongHopPanel ·
│                   PhanBoChietKhauModal        ⚠ xem ghi chú dưới
├── constants/      constants.ts · paths.ts · permissions.ts
├── fields/         types.ts · columns.ts · chiTietColumns.ts · chiTietFields.ts ·
│                   phanBoFields.ts · options.ts · status.ts · texts.ts
├── helpers/        tinhToan · tongHop · chietKhau · anHien · kiemTra · trangThai · dongBo
├── hooks/          useDanhMucHoaDon.ts
├── i18n/           vi.ts · en.ts · registerHoaDonBanHangI18n.ts   (namespace `hoaDonBanHang`)
├── pages/          HoaDonBanHangPage.tsx · hoaDonBanHang.css
└── test/           anHien · kiemTra · payload · tinhToan · i18n · hoaDonBanHang.render (6 file)
```

⚠ **`PhanBoChietKhauModal.tsx` nằm phẳng trong `components/`, không phải `components/modal/`.**
Luật cứng 4 (`client/CLAUDE.md §5`) nói *"popup nằm ở `components/modal/`, thư mục con DUY NHẤT được
phép trong `components/`"*. Đây là **sai lệch có thật** so với chuẩn hiện hành (chuẩn hoá 2026-08-11,
sau khi `hoaDonBanHang` đã code hôm 12/08 — có thể module code trước, luật cứng 4 chốt sau, hoặc đơn
giản là bỏ sót). Việc sửa (`git mv` file vào `components/modal/`) là code thật, **ngoài phạm vi
`/plan-fe`** — ghi vào nợ kỹ thuật N11 (§10) để dev dọn khi chạm lại module.

---

## 5. Checklist artefact

Đối chiếu bảng 15 dòng của `docs/fe-khung-kien-truc-chuan.md §5` — tất cả **đã có**, trừ 1 dòng lệch
đã nêu ở §4:

| Artefact | Trạng thái |
| :-- | :-- |
| `index.ts` (1 file gốc) | ✅ `index.ts:1-9` |
| `routes.tsx` đóng góp route domain | ✅ `banHang/routes.tsx:66-72` |
| `constants/paths.ts` · `permissions.ts` | ✅ |
| `fields/types.ts` | ✅ |
| `api/` + Zod | ✅ (list/detail thật; create/update/delete còn hợp đồng đề xuất — §2) |
| `helpers/` thuần, không React/mạng/`t()` | ✅ 7 file |
| `i18n/` 1 namespace, vi+en cân bằng | ✅ 313=313 khoá (đo 12/08, `IMPLEMENT.md §6.3`) |
| `pages/<Tên>Page.tsx` chỉ ráp | ✅ 100 dòng |
| `test/` | ✅ 6 file, xem §13 |
| Popup ở `components/modal/` | ⚠ **1 popup lệch** (`PhanBoChietKhauModal.tsx`) — xem §4 |
| Không `../../` trong module | ✅ đã soát tay, 0 chỗ (`IMPLEMENT.md §6.3`) |
| Không `any`/`@ts-ignore` | ✅ đã soát tay, 0 chỗ |

---

## 6. Route & quyền

```ts
// features/banHang/routes.tsx:66-72
{
  path: HOA_DON_BAN_HANG_PATHS.hoaDonBanHang,        // '/ban-hang/hoa-don-ban-hang'
  handle: handleFor(HOA_DON_BAN_HANG_PERM.view, 'hoaDonBanHang:menu.hoaDonBanHang'),
  lazy: async () => ({ Component: (await import('./hoaDonBanHang')).HoaDonBanHangPage }),
}
```

- `handle.crumbs` (không phải `crumbKeys` — xem chú thích ở `routes.tsx:24-30`: tên trường cũ
  `crumbKeys` từng làm breadcrumb rỗng âm thầm suốt tới 2026-08-18, đã sửa).
- Mã quyền (BR25): `LapHoaDonBan.{View,View.Detail,Create,Edit,Delete}` —
  `constants/permissions.ts:32-39`, khớp đúng cột "Mã" B4.3 của
  `pmkt-docs/ba/PMKT-E-14559_VaiTro/DanhSachQuyen.md` và khớp `MA_CHUC_NANG` phía BE
  (`HoaDonBanHangController.java:39`). ⚠ Quyền chưa được `iam_quyen` seed (nợ N1 một phần — BE mới
  cài phần đọc).
- Nút "Lập chứng từ bán hàng/dịch vụ" dùng quyền của màn đích (`LAP_CHUNG_TU_PERM` —
  `permissions.ts:50-53`), không phải quyền riêng của hóa đơn.

---

## 7. Bản đồ màn ↔ file con ↔ SCR ↔ UC ↔ Matrix

| SCR | UC | Matrix | File con `/plan-fe` | Component code |
| :-- | :-- | :-- | :-- | :-- |
| `SCR_HDBanHang_DanhSach` | `PMKT-u-06456_DanhSach/UC_HDBanHang_DanhSach.md` | *(SKIP theo `_scope.md` — không phải form)* | `01-danh-sach-hoa-don.md` | `HoaDonBanHangTab.tsx` + `HoaDonBanHangListTable.tsx` + `HoaDonBanHangQuickDetail.tsx` |
| `SCR_HDBanHang_ThemMoi` | `4.usecases/ThemMoi/UC_HDBanHang_ThemMoi.md` | `SCR_HDBanHang_ThemMoi_MaTranAnHien.md` | `02-popup-them-cap-nhat-xem.md` | `HoaDonBanHangThemMoiModal.tsx` (mode `create`) |
| `SCR_HDBanHang_CapNhat` | `PMKT-U-06458_CapNhat/UC_HDBanHang_CapNhat.md` | `SCR_HDBanHang_CapNhat_MaTranAnHien.md` | `02-popup-them-cap-nhat-xem.md` | cùng component, mode `edit` |
| `SCR_HDBanHang_ChiTiet` | `PMKT-U-06466_ChiTiet/UC_HDBanHang_ChiTiet.md` | `SCR_HDBanHang_ChiTiet_MaTranAnHien.md` | `02-popup-them-cap-nhat-xem.md` | cùng component, mode `view` |
| `SCR_HDBanHang_Xoa` | `PMKT-U-06459_Xoa/UC_HDBanHang_Xoa.md` | *(SKIP — popup xác nhận, không phải form)* | `03-popup-xoa.md` | `CommonConfirmModal` + `BulkDeleteResultModal` qua `HoaDonBanHangTab.tsx` |

Một component `HoaDonBanHangThemMoiModal.tsx` phục vụ 3 SCR (ThemMoi/CapNhat/ChiTiet) vì cả 3 Matrix
tự khai *"ma trận trường y hệt Thêm mới"* — gộp 1 file kế hoạch cho 3 SCR là theo đúng cấu trúc code
thật, không phải rút gọn tài liệu.

---

## 8. i18n

Namespace **`hoaDonBanHang`** — 1 namespace duy nhất cho cả module (§5 quy chuẩn), đăng ký ở
`i18n/registerHoaDonBanHangI18n.ts:1-18`. Cây khoá chính (đọc từ `i18n/vi.ts`, 518 dòng):

```
hoaDonBanHang.menu.hoaDonBanHang        # nhãn tab + breadcrumb
hoaDonBanHang.list.*                    # bảng danh sách, cột, nút, chip lọc
hoaDonBanHang.themMoi.*                 # popup — nhánh con, DÙNG CHUNG cho ThemMoi/CapNhat/ChiTiet
hoaDonBanHang.themMoi.tabs.*            # section trong popup (Thông tin HĐ, Xuất khẩu, Chi tiết…)
hoaDonBanHang.xoa.*                     # popup xác nhận xóa + kết quả xóa hàng loạt
hoaDonBanHang.msg.'MSG_PMKT-E-06196_xxx'  # NGUYÊN VĂN 6.messages.md, khoá = chính mã message
```

313 = 313 khoá vi/en cân bằng (đo 12/08). Nguồn chữ = nguyên văn `6.messages.md` +
`SCR_HDBanHang_*.md` — không diễn đạt lại. Chuỗi động dùng interpolation
(`'MSG_PMKT-E-06196_006': 'Hóa đơn đã tồn tại ({{soHD}}-{{kyHieuHD}}-{{mauSoHD}})'` —
`i18n/vi.ts:477`, đổi `{x}` của BA thành `{{x}}` của i18next).

---

## 9. Thứ tự thực hiện (đã hoàn tất — ghi lại cho hồ sơ)

1. `constants/` + `fields/types.ts` — khung dữ liệu trước.
2. `api/model.ts` (đề xuất, dựng từ CTBH) → `api/mock.ts` → `api/hoaDonBanHangApi.ts`.
3. `helpers/*` — thuần, test được ngay không cần UI.
4. `fields/columns.ts` · `chiTietFields.ts` · `status.ts` · `options.ts`.
5. `components/` — list trước, popup Thêm mới sau (Cập nhật/Xem chỉ đổi `mode`).
6. `pages/` + `routes.tsx` nối tay + `i18n/register…`.
7. `test/`.
8. **(20/08, ngoài phạm vi module này)** BE mở `POST /tim-kiem` thật → gỡ `HDBH_DUNG_MOCK` cho luồng
   đọc — đã xong, không cần việc gì thêm ở FE.
9. **(còn treo)** BE mở luồng ghi + dòng chi tiết → đối chiếu `api/model.ts` với DTO thật lần 2, gỡ
   `api/mock.ts` hẳn, siết `LuuHoaDonBanHangBody` từ `Record<string, unknown>` sang kiểu chặt.

---

## 10. Rủi ro

| # | Rủi ro | Giảm thiểu |
| :-- | :-- | :-- |
| **R1** | BE chỉ mới cài phần đọc — Thêm/Sửa/Xóa của FE gọi vào 400 tường minh nếu ai bật thử trên môi trường có BE thật (local vẫn OK vì `HDBH_DUNG_MOCK` chỉ tắt cho phần list, các hàm ghi vẫn còn `mock.ts` chờ) | Giữ nguyên `mock.ts` cho tới khi BE công bố xong luồng ghi; không tự ý tắt mock cho các hàm ghi |
| **R2** | Comment "BE CHƯA CÓ" ở đầu `model.ts`/`hoaDonBanHangApi.ts` đã lỗi thời, dễ khiến dev sau đọc nhầm | Q1 (§12) — sửa comment khi có việc chạm lại 2 file này |
| **R3** | `PhanBoChietKhauModal.tsx` lệch luật cứng 4 (không nằm trong `components/modal/`) | N11 (§ nợ), dọn khi có việc chạm lại module |
| **R4** | `SCR_CTBH_ThemMoi.md` (nguồn tham chiếu) còn đang được BA chỉnh tích cực (7 commit trong 7 ngày, mới nhất là HÔM NAY) — rủi ro field/BR đổi tiếp sau khi `/plan-fe` này chốt | Q2 (§12) — hỏi BA có đợt sửa CTBH nào sắp tới ảnh hưởng 5 section HĐBH tham chiếu không, trước khi FE code thêm |
| **R5** | Quyền `LapHoaDonBan.*` chưa seed ở `iam_quyen` (theo ghi chú `permissions.ts:28-30`, chưa xác minh lại lần này vì ngoài phạm vi DB) | Xác minh khi BE mở luồng ghi — nếu chưa seed thì mọi nút Thêm/Sửa/Xóa vẫn ẩn dù BE đã có endpoint |

---

## 11. Conflict Figma ↔ Matrix

Không phát sinh conflict MỚI trong lần rà soát 20/08. Giữ nguyên bảng đã chốt 12/08
(`IMPLEMENT.md §4.1`, đã verify vẫn đúng — đọc lại `SCR_HDBanHang_ThemMoi.md` HEAD xác nhận mục
"Chức năng" (dòng 56-65) vẫn chỉ có Hủy/Lưu, khớp cách code đã khoá nút ghi sổ sau cờ D1):

| # | Figma nói | Matrix/BA nói | Đã chọn |
| :-- | :-- | :-- | :-- |
| 1 | Footer có `Xem dữ liệu ghi sổ` · `Lưu và ghi sổ` (node 61146:217365) | `SCR_HDBanHang_ThemMoi.md` §Chức năng chỉ Hủy/Lưu; BR04 "không phát sinh bút toán" | D1 — dựng theo Figma, khoá sau `HDBH_CO_GHI_SO=false` |
| 2 | Cột trạng thái in "HĐ mới"/"HĐ thay thế"/"HĐ điều chỉnh" | BR06 gọi "Hóa đơn gốc"/"…thay thế"/"…điều chỉnh" | Theo **BR06** — Figma là nguồn bố cục, không phải thuật ngữ |
| 3 | Ô "Nhân viên bán hàng" trong Thông tin hóa đơn | Bảng trường CTBH hiện tại **CÓ** liệt kê ô này (`SCR_CTBH_ThemMoi.md:98`) | ✅ **Đã hết conflict** — bản CTBH đọc lại 20/08 đã có trường này ở đúng vị trí. Ghi chú: khi code hôm 12/08, CTBH bản khi đó CHƯA có trường này rõ ràng (theo `IMPLEMENT.md` #3); nay đã khớp Figma tự nhiên |
| 4 | Khối tổng có dòng "Chi phí" | `SCR_HDBanHang_ThemMoi.md` §Tổng hợp tiền tệ không có dòng này | Giữ nguyên theo Figma, luôn = 0 — Q3 (§12) hỏi BA nguồn dữ liệu |
| 5 | Cột "Số lô"/"Hạn sử dụng" trên lưới | CTBH hiện tại (`SCR_CTBH_ThemMoi.md:238-239`) **CÓ** 2 cột này ở Tab Chi tiết hàng hóa, nhưng thuộc nhóm field `Y (khi Kiêm phiếu xuất kho)` — HĐBH không có khái niệm "kiêm phiếu xuất kho" | Giữ theo Figma (đã code) — Q4 hỏi BA điều kiện bắt buộc của 2 cột này trên HĐBH là gì khi CTBH gắn nó với điều kiện không áp dụng cho hóa đơn |
| 6 | Cột "Số chứng từ" (`CT00291`) trên lưới | Bảng trường CTBH không nêu cột này ở Tab Chi tiết hàng hóa | Giữ theo Figma, cột chỉ-đọc `soChungTuNguon` (`api/model.ts:94`) — dấu vết hóa đơn lập từ chứng từ nguồn |

---

## 12. ⚠️ Điểm cần BA / Design xác nhận

| # | Câu hỏi | Bằng chứng hai phía |
| :-- | :-- | :-- |
| **Q1** | Comment "BE CHƯA CÓ" ở `api/model.ts:5` và `api/hoaDonBanHangApi.ts:12` đã lỗi thời (BE có module `hoa_don_ban_hang` từ 14/08, chỉ thiếu phần ghi). Xác nhận để dev sửa comment lần chạm kế tiếp — không phải câu hỏi nghiệp vụ, nhưng cần BA/Dev BE xác nhận **mốc thời gian dự kiến** BE mở luồng ghi + dòng chi tiết, để FE biết khi nào gỡ `mock.ts` | `HoaDonBanHangController.java:26-32` (Javadoc nói "kế hoạch F2-F5" nhưng chưa thấy file kế hoạch BE trong `docs/doing/`) |
| **Q2** | `SCR_CTBH_ThemMoi.md` đổi 7 lần trong 7 ngày qua (13-20/08), mới nhất là HÔM NAY (`7215f4a41`, 602 dòng). 5 section HĐBH tham chiếu trực tiếp đã được đối chiếu và **ổn định** (§2.3), nhưng có đợt sửa CTBH nào **sắp tới** dự kiến đụng vào Tab Hóa đơn / Thông tin bổ sung / Lựa chọn Loại tiền-Chiết khấu / Tab Chi tiết hàng hóa (phần không-hạch-toán) / Dòng tổng không? | `git log` 8 commit trên `SCR_CTBH_ThemMoi.md` từ 13/08 |
| **Q3** | Dòng "Chi phí" trong khối tổng (Figma node 14770:349117) hiện luôn = 0 vì chưa có cột nào trên lưới ghi vào `chiPhi` và DTO thật (`HoaDonBanHangDto.java`) cũng không có trường này. Nguồn dữ liệu dòng này là gì? | Figma vs `SCR_HDBanHang_ThemMoi.md` §Tổng hợp tiền tệ (không nêu dòng Chi phí) vs `HoaDonBanHangDto.java:24-75` (không có trường `chiPhi`/`tongChiPhi`) |
| **Q4** | Cột "Số lô"/"Hạn sử dụng" — CTBH gắn 2 cột này với điều kiện `Y (khi Kiêm phiếu xuất kho)` (`SCR_CTBH_ThemMoi.md:238-239`), nhưng HĐBH không có trường "Kiêm phiếu xuất kho". Với hóa đơn, 2 cột này bắt buộc nhập khi nào, hay luôn optional? | `SCR_CTBH_ThemMoi.md:238-239` vs `SCR_HDBanHang_ThemMoi_MaTranAnHien.md` (chưa liệt kê rõ 2 cột này trong ma trận Show/Hide) |
| **Q5** *(kế thừa từ `IMPLEMENT.md`, chưa có trả lời)* | "TK Thuế XK" trên lưới xuất khẩu — CTBH liệt kê cột này (`TaiKhoanThueXKId`, dòng 245) nhưng danh mục cột bị loại của HĐBH không nêu tường minh. Suy luận theo nguyên tắc chung (hóa đơn không có TK hạch toán) là loại luôn — cần BA xác nhận | `SCR_HDBanHang_ThemMoi_MaTranAnHien.md` §Điểm cần xác nhận #1 |
| **Q6** *(kế thừa)* | BR02 của `SCR_HDBanHang_CapNhat` (cảnh báo khi HĐ đã lập chứng từ) — sau khi người dùng chọn "Yes" ở popup cảnh báo, có trường nào bị khoá nhập (Mã KH/Mã hàng) hay vẫn cho sửa tự do? | `SCR_HDBanHang_CapNhat_MaTranAnHien.md` §Điểm cần xác nhận #2 |

---

## 13. Kiểm thử + cổng nghiệm thu

Module đã có `test/` với 5 file logic + 1 file render — không cần viết mới trong lần `/plan-fe` này,
chỉ ghi lại làm chuẩn tham chiếu:

```bash
npx vitest run src/features/banHang/hoaDonBanHang/test --reporter=dot   # 118/118 PASS (đo 12/08)
npx vite build                                                            # xanh, chunk lazy tách đúng
npm run check:committed                                                   # chỉ khi có commit mới
```

Bốn lệnh nặng (`typecheck`/`lint`/`lint:boundaries`/full suite) — **không** chạy mặc định theo
`client/CLAUDE.md §15.0`; lần đo gần nhất (12/08, `IMPLEMENT.md §6`) cho baseline sạch trong phạm vi
module (0 lỗi typecheck/lint riêng của `hoaDonBanHang`). Chưa chạy lại lần này vì `/plan-fe` không
sửa code — không có gì mới để baseline lệch.

---

## 14. BR đã áp dụng

Không đổi so với bảng đầy đủ ở `IMPLEMENT.md §7` (BR1, BR2, BR7, BR8, BR11, BR13.1, BR13.2, BR14,
BR15, BR16, BR18, BR24, BR25, BR26, BR30, BR31, BR34, BR43, BR44, BR45, BR46 của Common + toàn bộ
BR01-BR10 riêng của epic 06196) — **không lặp lại ở đây**, tránh hai bản có thể lệch nhau theo thời
gian. Điểm đổi duy nhất sau khi rà lại 20/08: **không có BR nào cần áp dụng lại** — 2 commit BA
17/08 không đổi nghĩa BR nào (chỉ đổi bí danh entity trong văn bản, §2.2).

BR chưa đạt — giữ nguyên danh sách `IMPLEMENT.md §7`: **BR39 xuất Excel** (ngoài phạm vi PYC),
**BR32/BR38** (ngoài phạm vi), **BR17/BR36/BR37/BR42** (không áp dụng — hóa đơn không hạch toán),
**BR19/BR20** (luật server, FE chỉ hiển thị lỗi trả về — nay đã CÓ endpoint đọc thật nhưng vẫn CHƯA
có endpoint kiểm trùng ghi), **BR45 §3** (lệch có chủ ý theo epic, đã báo), **BR21** (đã dùng
`CommonEditableGrid`, chưa đối chiếu từng dòng con của BR21 chung).

---

## 15. Tài liệu tham chiếu

- `pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang/**` (toàn bộ, đọc 20/08)
- `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_ThemMoi.md` (HEAD 20/08, 1.613 dòng)
- `docs/doing/PMKT-E-06196-hoa-don-ban-hang-fe/IMPLEMENT.md` (nhật ký thi công 12/08 — vẫn giữ)
- `client/CLAUDE.md`, `docs/fe-khung-kien-truc-chuan.md`, `pmkt-docs/ba/Common/business_rules.md`
- Code: `client/src/features/banHang/hoaDonBanHang/**`,
  `cell-app/src/main/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/**`

---

## 16. Cập nhật so với code hiện tại *(mục bắt buộc riêng — theo yêu cầu chạy lại lần này)*

**Tình trạng code FE: ĐÃ TRIỂN KHAI ĐẦY ĐỦ**, không phải "chưa có" — 47 file, ~9.167 dòng tại
`client/src/features/banHang/hoaDonBanHang/`, build ngày 12/08 qua `/gen-fe` (không qua `/plan-fe`
trước đó — xem lời giải thích ở đầu file). Dưới đây là toàn bộ điểm lệch/đồng bộ đã kiểm, gộp lại từ
§0, §2, §4, §11 để dễ tra một chỗ.

### 16.1 Hai commit BA nêu trong yêu cầu chạy lại — **KHÔNG có drift code nào**

| Commit | Kết luận |
| :-- | :-- |
| `d23d1e20d` (đổi bí danh entity → tên bảng thật) | Đối chiếu từng dòng diff: chỉ đổi tiền tố hiển thị trong văn bản (`HoaDonBan.X` → `sal_hoa_don_ban_hang.X` …), **field name giữ nguyên**. Zod schema (`api/model.ts`) và `fields/types.ts` dùng camelCase JSON vốn đã đúng, không cần sửa gì. |
| `25f9a7ca6` (bỏ "Tab Hạch toán" khỏi `_scope.md`) | Xác nhận bằng `grep` toàn module: code chưa từng cài Tab/route/component "Hạch toán" nào ngoài cờ `HDBH_CO_GHI_SO` đã có sẵn từ 12/08 (quyết định D1). Ghi chú sửa chỉ làm ĐÚNG lại _mô tả_ phạm vi vốn đã đúng ở code. |

**Không có việc code nào phải làm từ 2 commit này.**

### 16.2 Việc thật đã đổi kể từ 12/08 mà nằm NGOÀI 2 commit được nêu

| Gì đã đổi | Bằng chứng | Ảnh hưởng |
| :-- | :-- | :-- |
| **BE `cell/hoa_don_ban_hang` được tạo mới** (14/08), cài `POST /tim-kiem`, `GET /cot`, `GET /{id}` (header) | `cell-app/src/main/java/vn/vtt/pmkt/cell/hoa_don_ban_hang/**` | FE đã tự cập nhật theo kịp: `HDBH_DUNG_MOCK = false` từ 14/08 (`api/hoaDonBanHangApi.ts:44`), field Zod khớp DTO thật gần 1:1. **Không cần việc FE nào thêm cho phần đọc.** |
| **BE vẫn CHƯA cài** Create/Update/Delete/xóa-hàng-loạt (400 tường minh) và dòng chi tiết hàng hóa (`GET /{id}` trả `chiTiet=null`) | `HoaDonBanHangController.java:72-93`, `package-info.java:19-24` | `api/mock.ts` (355 dòng) còn sống đúng cho các luồng này — **giữ nguyên, không xoá**, ngược lại `IMPLEMENT.md` N1 tưởng "mock toàn bộ" nay chỉ còn đúng cho phần ghi |
| Docblock đầu `api/model.ts:5` và `api/hoaDonBanHangApi.ts:12` vẫn viết "BE CHƯA CÓ" | đọc trực tiếp file | **Lỗi thời** — Q1 (§12), sửa khi có việc chạm lại 2 file |
| `dieuChinhGiaHangBan` — N10 của `IMPLEMENT.md` (route 404) | `dieuChinhGiaHangBan/pages/DieuChinhGiaHangBanPage.tsx` tồn tại + `banHang/routes.tsx:52-58` đã có route | **N10 ĐÃ GIẢI QUYẾT** — không còn là nợ |
| `routes.tsx` field `crumbKeys` → `crumbs` (bug thật, không liên quan 06196 nhưng nằm trong file `hoaDonBanHang` phụ thuộc) | `banHang/routes.tsx:24-30` (chú thích sửa 2026-08-18) | Không có action — đã sửa, chỉ ghi nhận cho hồ sơ |
| `client/CLAUDE.md §5` chốt luật cứng 4 (popup phải ở `components/modal/`) — không rõ chốt trước hay sau khi `hoaDonBanHang` code | so `components/PhanBoChietKhauModal.tsx` (phẳng) với luật hiện hành | **Lệch thật**, N11 mới — xem §10 |

### 16.3 So với `IMPLEMENT.md` cũ (12/08) — việc BA cần phản ánh vào plan mới

Vì code đã tồn tại, "plan mới" ở đây đóng vai trò **cập nhật + chốt nợ**, không phải "thiết kế từ đầu".
Ba điểm khác nhau thật sự so với những gì `IMPLEMENT.md` ghi nhận hồi 12/08:

1. **BR-offset đã tự hết** — `IMPLEMENT.md §4.3` từng nêu `SCR_HDBanHang_ThemMoi.md` trỏ sai số BR
   của CTBH (lệch 1). Đọc lại HEAD 20/08: số đã khớp đúng. Không cần đổi gì, chỉ xoá kỳ vọng "phải sửa
   số BR" khỏi backlog.
2. **N1 (mock toàn bộ vì BE chưa có) đã tách làm hai** — phần ĐỌC hết nợ (BE có thật, FE đã nối), phần
   GHI + dòng chi tiết vẫn nợ y nguyên. Backlog cần cập nhật lại đúng phạm vi còn thiếu thay vì nói
   chung chung "BE chưa có".
3. **N10 (route `dieuChinhGiaHangBan`) đã đóng** — việc song song đã hoàn tất, không còn là rủi ro của
   module này.

Không có mục nào trong `IMPLEMENT.md` bị BA đảo ngược quyết định (D1/D2 vẫn đúng nguyên).
