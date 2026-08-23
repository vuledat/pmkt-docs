# Kế hoạch FE — PMKT-E-06195 Chứng từ bán dịch vụ

| | |
|---|---|
| **Trạng thái** | 🟡 BẢN NHÁP — chờ review, **chưa code một dòng nào** |
| **Phiên bản** | **v2 — 2026-08-15**, đồng bộ với tài liệu BA sau 2 commit `289d5079d` (12/08) + `1a928c53b` (13/08). Đổi lớn so với v1: xem [§16 Nhật ký](#16-nhật-ký-thay-đổi-so-với-v1) |
| **Người review bắt buộc** | 1 BA · 1 Dev FE · 1 Design |
| **Phiếu yêu cầu** | `pmkt-docs/ba/PMKT-E-06195_ChungTuBanDichVu/` |
| **Figma** | [Nguyên tệ — node 61661-103452](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/Ph%E1%BA%A7n-m%E1%BB%81m-K%E1%BA%BF-to%C3%A1n---Viettel?node-id=61661-103452) · [Ngoại tệ — node 61685-126981](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/Ph%E1%BA%A7n-m%E1%BB%81m-K%E1%BA%BF-to%C3%A1n---Viettel?node-id=61685-126981) |
| **Module FE đích** | `client/src/features/banHang/chungTuBanHang/` (KHÔNG mở module mới — xem **D1**) |
| **Domain** | `banHang` — đang chạy: `app/router/RootRoutes.tsx:11`, `:161` |
| **Route** | `/ban-hang/chung-tu-ban-hang` (dùng chung, `constants/paths.ts:9-11`) |
| **API phụ thuộc** | 🟡 **ĐÃ CÓ MỘT PHẦN (cập nhật 2026-08-18)** — `LoaiNghiepVuBanHang` nay có đủ 3 giá trị kể cả `DICH_VU`, dùng chung bảng `sal_chung_tu_ban_hang`. NHƯNG API tạo/sửa của màn bán hàng **cố tình từ chối** `DICH_VU` (`hopLeChoManBanHang()`), nên màn này vẫn cần **endpoint riêng hoặc cờ riêng** để ghi được giá trị đó. Dòng "chưa có `LoaiNghiepVu`" của v2 đã lỗi thời. Xem **R1**, §2 |
| **⚠ Khiếm khuyết đang chạy** | Mục **"Chứng từ bán dịch vụ"** trên dropdown Thêm mới của màn danh sách hiện mở **đúng popup bán hàng hóa** ([`ChungTuBanHangTab.tsx:126`](../../../client/src/features/banHang/chungTuBanHang/components/ChungTuBanHangTab.tsx)), tạo ra chứng từ `Bán hàng trong nước`. Người dùng bấm đúng mục mà ra sai loại nghiệp vụ, không có cảnh báo nào. Đây là **lý do màn này cần được ưu tiên**, hoặc tạm thời cho mục đó báo "đang phát triển" như mục "Thu tiền theo hóa đơn" bên cạnh. |

| UC | Màn hình / SCR | File con |
|---|---|---|
| UC_CTbanDichVu_DanhSach (PMKT-U-06196) | SCR_CTbanDichVu_DanhSach (dùng chung CTBH) | [01](01-danh-sach-dung-chung.md) |
| UC_CTbanDichVu_ThemMoi | SCR_CTbanDichVu_ThemMoi | [02](02-popup-them-moi.md) |
| UC_CTbanDichVu_CapNhat | SCR_CTbanDichVu_CapNhat | [03](03-popup-chinh-sua.md) |
| UC_CTbanDichVu_ChiTiet | SCR_CTbanDichVu_ChiTiet | [04](04-popup-xem-chi-tiet.md) |
| UC_CTbanDichVu_Xoa | SCR_CTbanDichVu_Xoa | [05](05-popup-xac-nhan-xoa.md) |
| UC_CTbanDichVu_GhiSo (PMKT-U-06449) · UC_CTbanDichVu_BoGhiSo (PMKT-U-06451) | *(không có SCR riêng)* | [06](06-ghi-so-bo-ghi-so.md) |
| — | Hợp đồng API + i18n | [07](07-hop-dong-api-va-i18n.md) |

---

## 0. Quyết định đã chốt

### D1 — Chứng từ bán dịch vụ dựng **trong** module `chungTuBanHang`, KHÔNG mở module/route mới

**Quyết định:** thêm trục **biến thể** `bienThe: 'hangHoa' | 'dichVu'` vào module
`features/banHang/chungTuBanHang/` hiện có. CTBDV **không** có module riêng, **không** có path riêng,
**không** có entry `routes.tsx` riêng.

**Căn cứ (v2 — BA nay nói thẳng, không còn phải suy):**

1. `SCR_CTBH_ThemMoi.md` **BR24**: *"Hai màn Thêm mới dùng **chung entity** `ChungTuBan` /
   `ChiTietChungTuBan`; `LoaiNghiepVu` là trường phân biệt luồng nghiệp vụ, **không tách entity
   riêng**"*.
2. `SCR_CTbanDichVu_DanhSach.md` **BR06 (mới)**: *"Chứng từ bán dịch vụ **không có màn danh sách
   riêng** — hiển thị chung màn danh sách với Chứng từ bán hàng, lọc theo `ChungTuBan.LoaiNghiepVu` =
   Bán dịch vụ"*.
3. Một màn hình ⇒ một module (`client/CLAUDE.md §5` luật cứng 2); popup Thêm/Sửa/Xem là component
   của cùng module (`client/CLAUDE.md:226-229`).
4. **Luật tầng chặn cứng phương án tách module:** `client/CLAUDE.md:106-112` — `leaf` **không** với
   được `leaf` anh em. Dựng `chungTuBanDichVu/` thành leaf riêng thì `ChungTuBanHangTab.tsx` (chủ lưới
   dùng chung) **không được phép** import popup của nó.
5. Điểm nối đã có sẵn: `components/ChungTuBanHangListTable.tsx:70` đã khai
   `ADD_MENU.chungTuBanDichVu`; i18n đã có nhãn `i18n/vi.ts:85`.

**Hệ quả cụ thể lên code:**

| Việc | File | Thay đổi |
|---|---|---|
| Khai biến thể | `constants/constants.ts` | `LOAI_NGHIEP_VU` mở rộng lên **3 giá trị** (thêm `banDichVu`) |
| Kiểu | `fields/types.ts` | `NguCanhAnHien` dùng `loaiNghiepVu` sẵn có, thêm cờ dẫn xuất `banDichVu` |
| Ẩn/hiện | `helpers/anHien.ts` | `laBanDichVu(nc)`; `hienTabPhieuXuatKho` / `hienLoaiNghiepVu` / `hienKiemPhieuXuatKho` = `false` khi bán dịch vụ; nhóm cột kho/giá vốn/ĐVT quy đổi/thuế XK ẩn |
| Cột lưới | `fields/chiTietFields.ts` | `visible` của nhóm cột trên `&& !laBanDichVu(nc)` |
| Chữ | `i18n/vi.ts` · `en.ts` | nhánh con `banDichVu.*` **trong cùng namespace `banHang`** |
| Quyền | `constants/permissions.ts` | thêm `BAN_DICH_VU_PERM` (mã thật, xem D3) |
| API | `api/model.ts` · `payload.ts` | thêm `loaiNghiepVu` vào row + body; **không** thêm resource mới (xem D2) |
| Popup | `components/ChungTuBanHangThemMoiModal.tsx` | thêm prop `loaiNghiepVu` khởi tạo; ẩn ô Loại nghiệp vụ khi bán dịch vụ |

**Vì sao KHÔNG chọn phương án kia:** module riêng ⇒ vi phạm luật tầng + nhân bản 386 dòng
`ChungTuBanHangListTable.tsx` + 354 dòng `ChungTuBanHangTab.tsx`, trong khi BA nói rõ là **một**
danh sách trên **một** entity.

### D2 — MỘT resource, MỘT endpoint, phân biệt bằng `LoaiNghiepVu` ⚠️ ĐỔI HOÀN TOÀN SO VỚI v1

v1 giả định "hai entity, hai endpoint" và treo câu hỏi chặn Q2. **BA đã trả lời dứt điểm:**

- `SCR_CTBH_DanhSach.md` **BR01 "Nguồn dữ liệu"**: *"Màn danh sách **dùng chung** … lấy toàn bộ bản
  ghi **ENT_ChungTuBan** của tenant, phân biệt hai loại bằng `ChungTuBan.LoaiNghiepVu`"*, kèm bảng
  mapping đủ 16 cột → field.
- `3.crud-matrix.md` đã đổi `ENT_ChungTuBanDichVu` → **`ENT_ChungTuBan`**.

**Chốt:** FE dùng **đúng một** resource `/api/ban-hang/chung-tu-ban-hang` (base path hiện có,
`api/chungTuBanHangApi.ts:32`) cho cả hai loại. Không tạo `chungTuBanDichVuApi.ts`, không tạo query
family thứ hai. Việc còn lại:

1. `loaiNghiepVu` vào row schema + body ghi.
2. `loaiNghiepVu` vào `ADV_FILTER_WIRE` (op `eq`) để lọc riêng từng loại khi cần.
3. FE dựa vào `row.loaiNghiepVu` để chọn bộ quyền, ẩn "Lập phiếu xuất", để trống "Trạng thái xuất
   hàng".

> **Câu hỏi còn lại (Q2 v2):** một entity nhưng **hai mã chức năng** quyền (`BanHangHoa` /
> `BanDichVu`) ⇒ BE phải phân quyền **theo dòng** trên cùng một endpoint `/search`. Cần BE xác nhận
> `/search` lọc theo quyền của người dùng chứ không chặn cả request.

### D3 — Mã quyền là mã THẬT

`cell-app/src/main/java/vn/vtt/pmkt/cell/common/constant/MaChucNang.java:217` khai
`BAN_DICH_VU = "BanDichVu"` với chú thích *"hành động: View, View.Detail, Create, Edit, Delete, Post,
Unpost"* — khớp **1:1** với các UC.

**Hệ quả:** gỡ OPEN ITEM ở `constants/permissions.ts:25-30` và ghi chú ở
`components/ChungTuBanHangListTable.tsx:179-186`. Mục "Chứng từ bán dịch vụ" trong dropdown Thêm mới
gate bằng `BanDichVu.Create`, **không** dùng chung `BanHangHoa.Create`.

### D4 — Một namespace i18n

Chữ của CTBDV là nhánh con `banDichVu.*` trong namespace `banHang` đã có
(`client/CLAUDE.md:362-370`). Chữ dùng chung tái sử dụng khóa cũ.

### D5 — Thứ tự làm: nối lưới trước, popup sau

Bước 1 (nối lưới + quyền + gate nút) độc lập với API mới, giao được ngay. Bước 2 (popup) bị chặn bởi
BE (**R1**). Chi tiết §9.

### D6 — `LoaiNghiepVu` cố định "Bán dịch vụ", ẩn khỏi UI, bất biến sau khi lưu 🆕

`SCR_CTbanDichVu_ThemMoi.md` §Thông tin chung + `SCR_CTBH_ThemMoi.md` **BR24**:

| | Chứng từ bán hàng | **Chứng từ bán dịch vụ** |
|---|---|---|
| Giá trị cho chọn | `Bán hàng trong nước` · `Bán hàng xuất khẩu` (**ẩn** `Bán dịch vụ` khỏi combo) | Cố định `Bán dịch vụ` |
| Trường trên UI | Hiển thị, cho sửa | **Ẩn khỏi giao diện** |

**Hệ quả code:** `LOAI_NGHIEP_VU` (`constants/constants.ts:20`) hiện chỉ có 2 giá trị → phải thêm
`banDichVu`. Ô select Loại nghiệp vụ giữ nguyên component nhưng `visible: false` ở biến thể dịch vụ,
và **giá trị vẫn phải nằm trong form + payload** (BE dựa vào nó để định tuyến nghiệp vụ).

**Bất biến:** *"Chứng từ **đã lưu không đổi được** `LoaiNghiepVu` giữa nhóm bán hàng và nhóm bán dịch
vụ"* ⇒ ở chế độ Sửa, ô này **không** được đưa vào body `PUT`, hoặc gửi nguyên giá trị cũ.

### D7 — Bỏ Tab Hạch toán, thay bằng nút "Xem dữ liệu ghi sổ" 🆕

Tài liệu v2 **xoá hẳn Tab Hạch toán** khỏi `SCR_CTbanDichVu_ThemMoi.md`, khỏi
`UC_CTbanDichVu_ThemMoi.md` AC2/bước 5, khỏi `UC_CTbanDichVu_ChiTiet.md` AC2/bước 4 và khỏi **cả ba**
ma trận Ẩn/Hiện.

Figma thay bằng **nút footer "Xem dữ liệu ghi sổ"** → mở popup read-only liệt kê bút toán
(Figma node **61661:104532**). Bộ tab thẻ lưới còn: `Chi tiết dịch vụ · Thuế · Đính kèm · Tham chiếu`.

**Hệ quả:** bỏ `hachToanColumns` khỏi tab list; `helpers/hachToan.ts:49 sinhButToan` **vẫn giữ** —
nó nuôi popup mới thay vì nuôi tab.

---

## 1. Phạm vi

### Trong phạm vi

- Nối mục **"Chứng từ bán dịch vụ"** của dropdown Thêm mới trên lưới dùng chung → mở popup Thêm mới
  với `loaiNghiepVu = 'Bán dịch vụ'` (hiện mọi mục đều mở cùng một popup —
  `components/ChungTuBanHangTab.tsx:247-256`).
- Gate quyền theo `BanDichVu.*` cho dòng bán dịch vụ (D3).
- Popup **Thêm mới / Chỉnh sửa / Xem chi tiết** biến thể dịch vụ, 2 chế độ tiền (nguyên tệ / ngoại tệ)
  × 4 biến thể tab thanh toán (mặc định · Hóa đơn · Phiếu thu · Giấy báo có).
- Popup **"Xem dữ liệu ghi sổ"** (D7).
- Popup **xác nhận xóa** đơn + **kết quả hàng loạt**.
- **Ghi sổ / Bỏ ghi sổ** đơn + hàng loạt.
- Ẩn "Lập phiếu xuất" và để trống "Trạng thái xuất hàng" ở dòng bán dịch vụ.

### NGOÀI phạm vi (nêu đích danh)

| Bị loại | Lý do |
|---|---|
| Màn **Thu tiền** (BR04) → `SCR_PhieuThuTM_TimKiemChungTu` / `SCR_PhieuThuTG_TimKiemChungTu` | Epic PMKT-E-06219 / PMKT-E-06222. Giữ "coming soon" (`ChungTuBanHangTab.tsx:249-251`) |
| Màn **Lập hóa đơn** (`SCR_HDBanHang_ThemMoi`) | Module hóa đơn bán hàng chưa dựng |
| Sửa hành vi của **chứng từ bán hàng hóa** (E-06194) | Chỉ chạm khi bắt buộc để tách biến thể |
| Ba tab còn lại của màn (`Trả lại hàng bán` · `Điều chỉnh hàng bán` · `Hóa đơn`) | Design-only, `pages/ChungTuBanHangPage.tsx:16-19` |
| **Tab "Đính kèm"** | Figma **có**, BA epic này **không nhắc ở đâu** ⇒ **C13**, chờ BA (**Q9**) |
| Tab **Tham chiếu** dựng đầy đủ | BA trỏ sang `Common/NguonDuLieu/SCR_ThamChieuCT.md`; CTBH cũng chưa dựng (`ChungTuBanHangThemMoiModal.tsx:30`) ⇒ **Q5** |
| Nhân bản / In trên popup Xem (BR13.2) | BA không liệt kê ⇒ **Q6** |
| Xuất Excel (BR39), Nhóm cột (BR38) | Không thuộc phiếu này; nợ của E-06194 |

---

## 2. Hiện trạng đã khảo sát

### 4 câu hỏi bắt buộc (`docs/fe-khung-kien-truc-chuan.md §4`)

| # | Câu hỏi | Trả lời | Bằng chứng |
|---|---|---|---|
| 0 | Code ở đâu? | `client/src/features/banHang/chungTuBanHang/` | luật cứng §4 Bước 0 |
| 1 | Màn loại nào? | **Chứng từ** ⇒ đáng lẽ `@domain-kit/chungTu` | `client/CLAUDE.md:130` |
| 2 | Đã có engine chưa? | **CÓ engine nhưng module tham chiếu KHÔNG dùng** — `chungTuBanHang` tự dựng popup bằng `@base` + `helpers/` riêng | `ls src/base/domainKit/chungTu/` có `createChungTuModule.tsx`; `grep -rn "domain-kit" src/features/banHang/` → **0 kết quả** |
| 3 | Component đã có ở `@base`? | Có đủ. `CommonEditableGrid` `src/base/index.ts:535` · `HeaderControls` `:277` · `TabMenuChild` `:144` · `CommonListTable` `:310` · `CommonConfirmModal` `:269` · `useListFilter` `:501` · `CommonComboGrid` `:562` · `CommonSelectBox` `:572` · `CommonNumberInput` `:160` · `CommonDateInput` `:164` · `CommonCheckbox` `:176` · `FieldLabel` `:188` · `RowActionButtons` `:340` · `CommonStatusTag` `:587` · `CommonEmpty` `:601` | |
| 4 | Domain đang chạy? | **CÓ** — `app/router/RootRoutes.tsx:11`, `:161` | |

> **Ghi chú câu 2:** phiếu này **không** đổi `chungTuBanHang` sang `@domain-kit/chungTu`. Đó là nợ
> kiến trúc của E-06194.

### Lệnh đã chạy + kết quả thật

```
$ grep -rn "banHang" client/src/app/router/RootRoutes.tsx
11:import { banHangRoutes } from '@features/banHang/routes'
161:                  ...gateByHandle(banHangRoutes),

$ grep -rn "DichVu\|dichVu" client/src/features/banHang/chungTuBanHang | grep -v /test/
components/ChungTuBanHangListTable.tsx:70:  chungTuBanDichVu: 'chungTuBanDichVu',
components/ChungTuBanHangListTable.tsx:186:  { key: ADD_MENU.chungTuBanDichVu, allowed: gates.create },
i18n/vi.ts:85:      chungTuBanDichVu: 'Chứng từ bán dịch vụ',
i18n/en.ts:67:      chungTuBanDichVu: 'Service sales voucher',
helpers/anHien.ts:94:export function laDichVu(line …)   ← ⚠ "DÒNG hàng loại Dịch vụ", KHÔNG PHẢI loại nghiệp vụ

$ grep -n "LOAI_NGHIEP_VU" -A6 client/src/features/banHang/chungTuBanHang/constants/constants.ts
20:export const LOAI_NGHIEP_VU = { … }      ← hiện chỉ 2 giá trị, thiếu 'Bán dịch vụ' (D6)

$ ls cell-app/src/main/java/vn/vtt/pmkt/cell/
accounting_core  chung_tu_ban_hang  chung_tu_mua_hang  common  core
integration_ops  master_data  platform_iam  quan_he_chung_tu  reporting

$ grep -n "BAN_DICH_VU" cell-app/…/common/constant/MaChucNang.java
217:    public static final String BAN_DICH_VU = "BanDichVu";
```

> ⚠ **Bẫy đặt tên:** `helpers/anHien.ts:94 laDichVu(line)` đã tồn tại với nghĩa **khác** — "dòng hàng
> có `loaiVatTu === 'Dịch vụ'`" (BR17 của CTBH). Hàm mới cho loại nghiệp vụ **phải** tên khác:
> `laBanDichVu(nc)`.

### Tình trạng API BE

| Cần | Trạng thái |
|---|---|
| `loaiNghiepVu` trên row + body của `/api/ban-hang/chung-tu-ban-hang` | ❌ chưa có (entity BE chưa có trường) |
| `/search` phân quyền theo dòng (`BanHangHoa` vs `BanDichVu`) | ❌ chưa xác nhận — **Q2 v2** |
| `PUT /{id}` | ❌ chưa có **kể cả cho bán hàng hóa** (`ChungTuBanHangThemMoiModal.tsx:25-27`) |
| Ghi sổ / bỏ ghi sổ / hàng loạt | ❌ chưa nối **kể cả cho bán hàng hóa** (`ChungTuBanHangTab.tsx:288-301`) |
| Endpoint dữ liệu ghi sổ (D7) | ❌ chưa có |
| Catalog quyền `BanDichVu.*` | ✅ có — `MaChucNang.java:217` |

⇒ **Phải có `/plan-be` cho PMKT-E-06195 trước khi code bước 2.** Xem **R1**.

---

## 3. Kế hoạch reuse

| Cần | Có sẵn ở đâu (`file:dòng`) | Dùng lại hay viết mới | Lý do |
|---|---|---|---|
| Lưới danh sách + phân trang + lọc + dòng tổng | `components/ChungTuBanHangListTable.tsx:1-386` | **Dùng lại nguyên** | Danh sách dùng chung, chỉ thêm gate theo `loaiNghiepVu` |
| State lưới | `components/ChungTuBanHangTab.tsx:1-354` | **Dùng lại**, sửa `onAdd:247-256` + `onRowMenuAction:288-301` | Điểm nối duy nhất |
| **Adapter + query family** | `api/chungTuBanHangApi.ts:110-114` · `api/queries.ts:14-18` | **Dùng lại NGUYÊN** | **D2 — một resource.** v1 định tạo file mới, nay bỏ |
| Dropdown Thêm mới | `ChungTuBanHangListTable.tsx:67-74`, `:179-190` | **Dùng lại**, đổi gate mục 2 sang `BanDichVu.Create` | D3 |
| Shell popup + header chọn chứng từ nguồn | `ChungTuBanHangThemMoiModal.tsx:38-52` | **Dùng lại** | Figma CTBDV có đúng header đó |
| Tab Chứng từ ghi nợ | `components/ChungTuGhiNoTab.tsx` (238 dòng) | **Dùng lại** | Figma v2: bộ 14 trường trùng khít |
| Tab Hóa đơn | `components/HoaDonTab.tsx` (230 dòng) | **Dùng lại** | BA tham chiếu nguyên |
| Tab Phiếu thu / Giấy báo có | `components/ThuTienTab.tsx` (195 dòng) | **Dùng lại** | như trên |
| Tab Phiếu xuất kho | `components/PhieuXuatKhoTab.tsx` | **KHÔNG dùng** | dịch vụ không xuất kho (BR24) |
| Khối Thông tin bổ sung | `components/ThongTinBoSung.tsx` | **KHÔNG dùng** | Figma v2 vẫn không vẽ; Matrix loại (giả định #3) |
| Lưới chi tiết | `fields/chiTietFields.ts:164` + `@base CommonEditableGrid` (`src/base/index.ts:535`) | **Dùng lại + tham số hoá `visible`** | ẩn nhóm cột kho/giá vốn/ĐVT quy đổi/thuế XK |
| Tab Thuế | `fields/tabColumns.ts` (`thueColumns`) + `helpers/hachToan.ts:184 tongHopThue` | **Dùng lại** | BA v2: *"gộp theo từng mức % thuế GTGT; mọi ô readonly"* |
| ~~Tab Hạch toán~~ | `fields/tabColumns.ts` (`hachToanColumns`) | **Chuyển chỗ dùng** | D7 — nuôi popup "Xem dữ liệu ghi sổ" thay vì tab |
| Số học dòng | `helpers/tinhToan.ts:18-179` | **Dùng lại** | trừ `soLuongQuyDoi:58`, `donGiaTheoDonViCoBan:63`, `dungDonViQuyDoi:69`, `tienVon:147` |
| Chiết khấu 2 tầng + phân bổ | `helpers/chietKhau.ts:23-253` + `components/PhanBoChietKhauModal.tsx` | **Dùng lại nguyên** | BR03 → BR12 của CTBH |
| Tổng hợp tiền | `helpers/tongHop.ts:19-118` + `components/TongHopPanel.tsx` | **Dùng lại** | Figma v2 cùng khối tổng |
| Đồng bộ liên trường | `helpers/dongBo.ts:27-211` + `hooks/useDongBoTab.ts` | **Dùng lại**, thêm template diễn giải riêng | BR01 CTBDV |
| Validate trước lưu | `helpers/kiemTra.ts:18-136` | **Dùng lại**, bỏ `kiemTraKiemPhieuXuatKho:96`, đổi `MA_LOI` sang `MSG_PMKT-E-06195_*` | |
| Danh mục / lookup | `api/lookups.ts:1-304` + `hooks/useDanhMucThemMoi.ts` | **Dùng lại**, thêm lọc `Loại = Dịch vụ` (BR02) | |
| Trạng thái + màu | `helpers/trangThai.ts:32-77` + `fields/status.ts` | **Dùng lại**, đổi tên field `TrangThaiChungTu` → `TrangThaiGhiSo` | BR12 · BR33 |
| Popup xác nhận | `@base CommonConfirmModal` (`src/base/index.ts:269`) | **Dùng lại** | BR3 |
| Toast | `@base useToast` | **Dùng lại** | BR26 |

**Viết mới (mỗi cái kèm lý do đã kiểm `@base`/`@domain-kit`):**

| Viết mới | Lý do |
|---|---|
| `helpers/anHien.ts` → `laBanDichVu` + predicate biến thể | logic nghiệp vụ riêng của màn, không thuộc `@base` |
| `components/XemDuLieuGhiSoModal.tsx` 🆕 | D7. Đã kiểm `src/base/index.ts` — có `CommonListTable` nhưng không có shell "xem sổ" dựng sẵn |
| `components/KetQuaHangLoatModal.tsx` 🆕 | BR45.3. Đã kiểm `@base` — không có shell "kết quả hàng loạt" |
| `components/GhiSoConfirmModal.tsx` 🆕 | bọc `CommonConfirmModal` + cảnh báo MSG_106 |

> ⚠ **Bỏ so với v1:** `api/chungTuBanDichVuApi.ts` — không còn cần (D2).

---

## 4. Kiến trúc module — cây thư mục sau khi làm

🆕 = file mới, ✏️ = file sửa.

```
features/banHang/
├── routes.tsx                            (giữ nguyên — không thêm route)
└── chungTuBanHang/
    ├── index.ts                          (giữ nguyên — cửa ra duy nhất ở gốc)
    ├── api/
    │   ├── chungTuBanHangApi.ts          ✏️ `loaiNghiepVu` vào ADV_FILTER_WIRE
    │   ├── model.ts                      ✏️ `loaiNghiepVu` + đổi tên field theo LDM v2
    │   ├── payload.ts                    ✏️ gửi `loaiNghiepVu`; bỏ trường kho/giá vốn ở biến thể DV
    │   ├── formDetail.ts                 ✏️ map detail → form values theo biến thể
    │   ├── lookups.ts                    ✏️ lookup dịch vụ (lọc Loại = Dịch vụ)
    │   ├── queries.ts                    ✏️ thêm mutation ghi sổ / bỏ ghi sổ / hàng loạt
    │   └── ghiSo.ts                      🆕 đọc dữ liệu ghi sổ cho popup D7
    ├── components/
    │   ├── ChungTuBanHangTab.tsx         ✏️ onAdd · onRowMenuAction · gates theo loaiNghiepVu
    │   ├── ChungTuBanHangListTable.tsx   ✏️ gate mục Thêm mới · ẩn "Lập phiếu xuất" dòng DV
    │   ├── ChungTuBanHangThemMoiModal.tsx ✏️ loaiNghiepVu · bỏ tab Hạch toán · thêm nút Xem dữ liệu ghi sổ
    │   ├── ChungTuGhiNoTab.tsx           ✏️ nhãn theo biến thể
    │   ├── HoaDonTab.tsx · ThuTienTab.tsx (giữ nguyên)
    │   ├── PhieuXuatKhoTab.tsx · ThongTinBoSung.tsx (giữ nguyên — không render ở biến thể DV)
    │   ├── XemDuLieuGhiSoModal.tsx       🆕 D7
    │   ├── KetQuaHangLoatModal.tsx       🆕 BR45.3
    │   └── GhiSoConfirmModal.tsx         🆕
    ├── constants/
    │   ├── constants.ts                  ✏️ `LOAI_NGHIEP_VU` lên 3 giá trị (D6)
    │   ├── paths.ts                      (giữ nguyên)
    │   └── permissions.ts                ✏️ `BAN_DICH_VU_PERM`, gỡ OPEN ITEM dòng 25-30
    ├── fields/
    │   ├── chiTietFields.ts              ✏️ visible/nhãn theo biến thể
    │   ├── chiTietColumns.ts · columns.ts · options.ts · status.ts · tabColumns.ts ✏️
    │   ├── ghiSoColumns.ts               🆕 cột popup D7
    │   ├── hangLoatColumns.ts            🆕 cột bảng lỗi BR45.3
    │   ├── texts.ts                      ✏️
    │   └── types.ts                      ✏️ `loaiNghiepVu`, dòng chi tiết DV
    ├── helpers/
    │   ├── anHien.ts                     ✏️ `laBanDichVu` + gate biến thể
    │   ├── hachToan.ts                   ✏️ bỏ bút toán giá vốn / thuế XK ở biến thể DV
    │   ├── kiemTra.ts                    ✏️ mã lỗi `MSG_PMKT-E-06195_*` + bỏ kiểm PXK
    │   ├── dongBo.ts                     ✏️ template diễn giải "bán dịch vụ" (BR01)
    │   ├── quyen.ts                      🆕 `gatesChoDong(row, has)`
    │   ├── hangLoat.ts                   🆕 đếm dòng theo trạng thái
    │   └── chietKhau.ts · tinhToan.ts · tongHop.ts · trangThai.ts (giữ nguyên)
    ├── hooks/
    │   ├── useDanhMucThemMoi.ts          ✏️ lookup dịch vụ
    │   ├── useDongBoTab.ts               ✏️ nhận biến thể
    │   └── useHangLoat.ts                🆕
    ├── i18n/
    │   ├── vi.ts · en.ts                 ✏️ nhánh `banDichVu.*` (CÙNG namespace)
    │   └── registerChungTuBanHangI18n.ts (giữ nguyên)
    ├── pages/
    │   ├── ChungTuBanHangPage.tsx        (giữ nguyên)
    │   └── chungTuBanHang.css            ✏️ nếu cần, tiền tố `.pmkt-ctbdv-*`
    └── test/
        ├── banDichVu.anHien.test.ts      🆕
        ├── banDichVu.hachToan.test.ts    🆕
        ├── banDichVu.payload.test.ts     🆕
        └── banDichVu.render.test.tsx     🆕
```

**Kiểm luật cứng:** gốc module vẫn đúng **một** file `index.ts` ✅ · không thư mục theo hành vi ✅ ·
không `_shared/` ✅ · không `../../` ✅ · một namespace i18n ✅ · một stylesheet ✅.

---

## 5. Checklist artefact (`docs/fe-khung-kien-truc-chuan.md §5`)

| # | Artefact | Đường dẫn | Phiếu này |
|---|---|---|---|
| 1 | Hợp đồng BE (Zod + hàm gọi) | `api/` | ✅ sửa `model.ts`/`payload.ts`/`queries.ts` + `ghiSo.ts` |
| 2 | Kiểu dùng chung | `fields/types.ts` | ✅ sửa |
| 3 | Hằng số nghiệp vụ | `constants/constants.ts` | ✅ sửa |
| 4 | Cột / ô lưới / option / badge | `fields/` | ✅ sửa + 2 file mới |
| 5 | Logic nghiệp vụ thuần | `helpers/` | ✅ sửa + 2 file mới |
| 6 | State & request | `hooks/` | ✅ sửa + `useHangLoat.ts` |
| 7 | Component riêng của màn | `components/` | ✅ sửa + 3 file mới |
| 8 | Entry màn hình + CSS | `pages/` | ⚪ giữ nguyên |
| 9 | i18n vi + en + register | `i18n/` | ✅ sửa `vi.ts`/`en.ts` |
| 10 | Cửa ra | `index.ts` | ⚪ giữ nguyên |
| 11 | Test | `test/` | ✅ 4 file mới |
| 12 | Mã quyền | `constants/permissions.ts` | ✅ sửa |
| 13 | Đường dẫn | `constants/paths.ts` | ⚪ giữ nguyên |
| 14 | Route + `handle` | `features/banHang/routes.tsx` | ⚪ giữ nguyên |
| 15 | Nối tay vào cây route | `app/router/RootRoutes.tsx` | ⚪ giữ nguyên (đã nối) |

`mock.ts`: **sẽ phải tạo tạm** nếu code bước 2 trước khi BE xong — **còn `mock.ts` = còn nợ**.

---

## 6. Route & quyền

**Route:** không thêm. `/ban-hang/chung-tu-ban-hang` giữ `handle.perm = BAN_HANG_CHUNG_TU_PERM.view`
(`routes.tsx:32-33`).

> ⚠ **Q3 (chưa được trả lời trong v2):** người chỉ có `BanDichVu.View` mà không có `BanHangHoa.View`
> sẽ bị `<RequirePermission>` chặn ở cổng route. Ba hướng: (a) `handle.perm` nhận mảng "có một trong
> hai" (hiện là `PermissionKey` đơn, `routes.tsx:19-20`); (b) chấp nhận `BanHangHoa.View` là quyền
> vào màn; (c) BE gộp một mã quyền cho màn dùng chung. **Không tự chọn** — hỏi BA.
> Câu này **nặng hơn ở v2**: BA nay khẳng định một entity, nhưng vẫn giữ hai mã chức năng.

**Mã quyền (BR25), theo `MaChucNang.java:217`:**

```ts
export const BAN_DICH_VU_PERM = {
  view:       'BanDichVu.View',
  viewDetail: 'BanDichVu.View.Detail',
  create:     'BanDichVu.Create',
  edit:       'BanDichVu.Edit',
  delete:     'BanDichVu.Delete',
  ghiSo:      'BanDichVu.Post',
  boGhiSo:    'BanDichVu.Unpost',
} as const
```

Hành vi khi thiếu quyền: **ẩn nút, không disable** (BR25.2). Nút "Lưu và ghi sổ" cần **đồng thời**
`.Create`(hoặc `.Edit`) **và** `.Post` (UC_ThemMoi AC5, UC_CapNhat AC4).

---

## 7. Bản đồ màn ↔ file con ↔ SCR ↔ UC ↔ Matrix

| File con | SCR nguồn | UC nguồn | Ma trận |
|---|---|---|---|
| [01](01-danh-sach-dung-chung.md) | `SCR_CTbanDichVu_DanhSach.md` (+ `SCR_CTBH_DanhSach.md`) | UC_CTbanDichVu_DanhSach | *(SKIP theo `_scope.md`)* |
| [02](02-popup-them-moi.md) | `SCR_CTbanDichVu_ThemMoi.md` | UC_CTbanDichVu_ThemMoi | `SCR_CTbanDichVu_ThemMoi_MaTranAnHien.md` |
| [03](03-popup-chinh-sua.md) | `SCR_CTbanDichVu_CapNhat.md` | UC_CTbanDichVu_CapNhat | `SCR_CTbanDichVu_CapNhat_MaTranAnHien.md` |
| [04](04-popup-xem-chi-tiet.md) | `SCR_CTbanDichVu_ChiTiet.md` | UC_CTbanDichVu_ChiTiet | `SCR_CTbanDichVu_ChiTiet_MaTranAnHien.md` |
| [05](05-popup-xac-nhan-xoa.md) | `SCR_CTbanDichVu_Xoa.md` | UC_CTbanDichVu_Xoa | *(SKIP theo `_scope.md`)* |
| [06](06-ghi-so-bo-ghi-so.md) | *(không có SCR riêng)* | UC_CTbanDichVu_GhiSo · UC_CTbanDichVu_BoGhiSo | — |
| [07](07-hop-dong-api-va-i18n.md) | — | — | — |

**Đối chiếu:** 5/5 file `5.screens/*.md` xuất hiện **đúng một lần**. 7/7 UC đã có chỗ.

---

## 8. i18n — một namespace `banHang`

```
banHang:
├── list.addMenu.chungTuBanDichVu        (đã có — vi.ts:85)
├── banDichVu:                           ← 🆕 nhánh con
│   ├── title.themMoi / chinhSua / xemChiTiet
│   ├── tabs.chiTietDichVu
│   ├── grid.<cột>
│   ├── ghiSo.<…>                        (popup "Xem dữ liệu ghi sổ" — D7)
│   ├── validate.<mã>                    (MSG_PMKT-E-06195_006 … _055)
│   ├── toast.<mã>                       (MSG_PMKT-E-06195_001/004/009/020/021/030)
│   ├── confirm.xoa / xoaHangLoat / ghiSo / boGhiSo
│   └── hangLoat.<…>                     (BR45.3)
└── (mọi khóa còn lại — DÙNG LẠI khóa cũ)
```

Bảng khóa đầy đủ vi/en: [07 §3](07-hop-dong-api-va-i18n.md). Chuỗi động dùng interpolation, **không
cộng chuỗi** (`client/CLAUDE.md:374-379`).

---

## 9. Thứ tự thực hiện

| Bước | Việc | Phụ thuộc | Chặn bởi API? |
|---|---|---|---|
| **B1** | `constants/permissions.ts` + `constants/constants.ts` (`LOAI_NGHIEP_VU` 3 giá trị) + `fields/types.ts` | — | Không |
| **B2** | `helpers/anHien.ts`: `laBanDichVu` + predicate biến thể (+ test) | B1 | Không |
| **B3** | Lưới dùng chung: gate mục Thêm mới, ẩn "Lập phiếu xuất", để trống "Trạng thái xuất hàng", gate ⋮ theo `loaiNghiepVu` — [01](01-danh-sach-dung-chung.md) | B1, B2 | **Có** (cần `loaiNghiepVu` trong response) |
| **B4** | `api/`: `loaiNghiepVu` vào schema + payload + filter | B1 | **Có** — R1 |
| **B5** | Popup Thêm mới biến thể DV (bỏ tab Hạch toán) — [02](02-popup-them-moi.md) | B2, B4 | **Có** |
| **B6** | Popup "Xem dữ liệu ghi sổ" — [02 §5](02-popup-them-moi.md) | B5 | **Có** |
| **B7** | Popup Xem chi tiết — [04](04-popup-xem-chi-tiet.md) | B5 | **Có** |
| **B8** | Popup Chỉnh sửa (+ BR02 khóa checkbox hóa đơn) — [03](03-popup-chinh-sua.md) | B5, B7 | **Có** (`PUT` chưa có) |
| **B9** | Xóa đơn + hàng loạt + popup kết quả — [05](05-popup-xac-nhan-xoa.md) | B3 | **Có** |
| **B10** | Ghi sổ / Bỏ ghi sổ đơn + hàng loạt — [06](06-ghi-so-bo-ghi-so.md) | B3 | **Có** |
| **B11** | Test + cổng nghiệm thu §13 | tất cả | — |

B1→B2 giao được ngay. B3 trở đi đứng sau plan BE.

---

## 10. Rủi ro

| Mã | Rủi ro | Giảm thiểu |
|---|---|---|
| **R1** | **API BE chưa có** `loaiNghiepVu`; chưa có ghi sổ/bỏ ghi sổ/hàng loạt/`PUT`/dữ liệu ghi sổ | Chạy `/plan-be pmkt-docs/ba/PMKT-E-06195_ChungTuBanDichVu` trước. Buộc làm UI trước ⇒ `api/mock.ts` tạm, ghi rõ là **nợ** |
| **R2** | Module `chungTuBanHang` phình to — `ChungTuBanHangThemMoiModal.tsx` đã 961 dòng | Đẩy quyết định biến thể xuống `helpers/anHien.ts` + `fields/`; popup chỉ **ráp**. Vượt ~1.100 dòng thì tách theo **khối UI** (không theo hành vi) |
| **R3** | Sửa file dùng chung làm **hồi quy E-06194** (đang chạy) | Mọi predicate mới mặc định loại nghiệp vụ cũ; giữ nguyên chữ ký. Chạy lại đủ 8 test hiện có trước khi báo xong |
| **R4** | Người chỉ có `BanDichVu.View` không vào được màn (§6) | Q3 — chốt với BA trước B3 |
| **R5** | Figma lệch BA ở bộ cột lưới (§11) | Chốt §11 với BA + Design **trước** B5 |
| **R6** | `laDichVu` (dòng hàng) vs `laBanDichVu` (loại nghiệp vụ) dễ trộn | Tên khác nhau + comment tại chỗ + test riêng |
| **R7** | Ma trận Ẩn/Hiện vẫn ở trạng thái **`[DRAFT — chờ duyệt]`** (cả 3 file) | Không code theo ô `(sl)`/`[CXM]`; các điểm đó nằm ở §12 |
| **R8** 🆕 | **Tài liệu BA đang biến động mạnh** — 2 commit trong 2 ngày đổi entity, đổi số hiệu BR, đổi link Figma, bỏ cả một tab | Trước mỗi bước code, `git log -1 -- pmkt-docs/ba/PMKT-E-06195_ChungTuBanDichVu` để soát; ghi commit hash BA đã đối chiếu vào PR |
| **R9** 🆕 | **Mâu thuẫn nội tại của BA về `ENT_PhieuThu`** (§12 Q10) — ảnh hưởng payload và luồng Bỏ ghi sổ | Chốt trước B5 |

---

## 11. Conflict Figma ↔ Matrix / BA (đo lại trên Figma v2)

> Xử lý chung: **UI theo Figma, behavior theo Matrix/BA**. Các dòng ⚠ dưới đây là conflict về **sự
> tồn tại của trường** — phải BA + Design chốt trước khi code (R5).

| # | Điểm | Figma v2 | Matrix / BA v2 | Xử lý |
|---|---|---|---|---|
| ~~C1~~ | Cột `Số lượng đã xuất HĐ` ở Thêm mới | ✅ **Đã hết ở bản Nguyên tệ** — Figma bỏ cột, khớp Matrix `Hide(at)` | | ⚠ **nhưng bản Ngoại tệ (61685:127083) VẪN vẽ cột này** ⇒ mâu thuẫn **trong chính Figma** → **C16** |
| **C2** | Cột `Tài khoản CK` | **KHÔNG** có | Matrix `Show`; BR02 nói auto-fill "Tài khoản CK" | Giữ cột (BR thắng), mặc định **ẩn qua cấu hình cột** (BR30) — Design xác nhận |
| ~~C3~~ | Cột `Diễn giải thuế` | ✅ **Đã có** trong Figma v2 | | hết conflict |
| ~~C4~~ | Cột `HH không TH trên tờ khai thuế GTGT` | ✅ **Đã có** trong Figma v2 | | hết conflict |
| **C5** | Cột Figma có, BA không nhắc | `Đối tượng THCP · Vụ việc · Đơn vị · Khoản mục chi phí · Hợp đồng bán · Đơn đặt hàng` | BA không nhắc | **Không code** — hỏi BA (**Q4**). CTBH cũng đang treo Vụ việc/Hợp đồng vì thiếu endpoint danh mục (`ChungTuBanHangThemMoiModal.tsx:31`) |
| **C6** | Dòng "Chi phí" ở khối tổng | **Nguyên tệ CÓ**, **Ngoại tệ KHÔNG** | BA không nhắc | Mâu thuẫn trong Figma. Đề xuất: **không render** cho tới khi BA định nghĩa |
| **C7** | Nút lưới | `Thêm dòng · Thêm ghi chú · Xóa hết dòng` | BA: `Thêm dòng · Xóa dòng · Thêm ghi chú` | Theo Figma về nhãn/thứ tự; "xóa dòng đang chọn" ở icon 🗑 cột Chức năng (BR21.1) |
| **C8** | Nút lưới ở màn Xem | *(Figma không vẽ màn Xem)* | Matrix: `Hide`; BR14.1: "tất cả control disabled" | Theo Matrix (`Hide`) — Matrix trích `SCR_CTbanDichVu_ChiTiet.md:19` |
| ~~C9~~ | Placeholder "Điều khoản thanh toán" | ✅ **Đã sửa** — "Chọn điều khoản thanh toán" | | hết conflict |
| **C10** | Section "Thông tin bổ sung" | **Không vẽ** | Matrix giả định #3 "không đưa vào" | ✅ Figma **xác nhận** giả định — không làm |
| **C11** | Header Options | chỉ `Lập kèm hóa đơn` · `Thu tiền ngay` (+ `Hình thức thanh toán`) | BR24: ẩn Loại nghiệp vụ + Kiêm phiếu xuất kho | ✅ **Khớp** |
| **C12** 🆕 | Nhãn cột lưới | **"Mã hàng hóa" / "Tên hàng hóa"** | BA: *"Đổi tên các trường từ Hàng hóa sang Dịch vụ (Mã dịch vụ, Tên dịch vụ, Tổng tiền dịch vụ)"* | **Theo BA** (behavior/chữ nghiệp vụ) — Figma dùng lại component của CTBH nên chưa đổi nhãn. Báo Design |
| **C13** 🆕 | **Tab "Đính kèm"** | **CÓ** (tab thứ 3 của thẻ lưới) | BA epic này **không nhắc ở đâu** | **Không code** — **Q9** |
| **C14** 🆕 | Nút footer **"Xem dữ liệu ghi sổ"** | **CÓ** | BA bảng Chức năng chỉ khai 3 nút (Lưu · Lưu và ghi sổ · Hủy) | **Code theo Figma** — nó thay thế Tab Hạch toán vừa bị BA xoá (D7); nếu không có thì không còn chỗ nào xem bút toán. Cần BA bổ sung vào bảng Chức năng |
| **C15** 🆕 | Tiêu đề popup | **"Thêm chứng từ bán dịch vụ"** | SCR: "Thêm mới Chứng từ bán dịch vụ" | Theo Figma (chữ hiển thị) |
| **C16** 🆕 | Nguyên tệ ↔ Ngoại tệ lệch nhau | Ngoại tệ có `Số lượng đã xuất HĐ` + **không** có dòng "Chi phí"; Nguyên tệ ngược lại | — | Mâu thuẫn **nội bộ Figma** — Design phải chốt một bản |
| **C17** 🆕 | Ô **Tỷ giá** ở biến thể ngoại tệ | Figma ngoại tệ **không vẽ** ô Tỷ giá ở hàng header lưới (chỉ `Loại tiền [USD]` + `Chiết khấu`) | Matrix: `Tỷ giá quy đổi` `Show(đk-LT)` | Theo Matrix (**có** ô Tỷ giá) — không có nó thì không nhập được tỷ giá. Báo Design bổ sung |

---

## 12. ⚠️ Điểm cần BA / Design xác nhận

**Q1 — Tên module.** D1 để CTBDV sống trong `features/banHang/chungTuBanHang/`, nên tên module không
còn tả đúng nội dung. Có đổi thành `chungTuBan` không? *(`client/CLAUDE.md:202-204` gọi
`chungTuBanHang` là **mẫu tham chiếu duy nhất** của repo — đổi tên là `git mv` + sửa mọi alias.)*
**Đề xuất: KHÔNG đổi trong phiếu này**, mở ticket riêng. Ghi chú: BA v2 đã đổi entity thành
`ChungTuBan`, nên tên `chungTuBan` giờ **khớp LDM hơn** — cân nhắc lại khi có ticket.

**Q2 v2 — Phân quyền theo dòng trên một endpoint.** ~~(v1: một hay hai endpoint — BA đã trả lời)~~
Một entity `ChungTuBan` nhưng **hai mã chức năng** (`BanHangHoa` / `BanDichVu`). `POST /search` phải
**lọc theo quyền của người dùng** (trả về dòng nào họ được xem) chứ không chặn cả request. Cần BE
xác nhận cơ chế.

**Q3 — Quyền vào màn danh sách dùng chung.** Xem §6. Chưa được trả lời trong v2.

**Q4 — Bộ cột lưới chi tiết.** Chốt C2 · C5 · C12 · C16 ở §11. Đầu vào trực tiếp của
`fields/chiTietFields.ts`.

**Q5 — Tab Tham chiếu.** BA trỏ sang `Common/NguonDuLieu/SCR_ThamChieuCT.md`; Figma v2 vẫn có tab.
CTBH chưa dựng (`ChungTuBanHangThemMoiModal.tsx:30`). Có nằm trong phiếu E-06195 không?

**Q6 — Nút "Nhân bản" và "In" trên popup Xem.** BR13.2 quy định popup chi tiết **luôn** có "In" và
(chế độ Xem) có "Nhân bản". `SCR_CTbanDichVu_ChiTiet.md` chỉ liệt kê 6 nút. **Đang lệch BR13.2.**

**Q7 — Bỏ ghi sổ chứng từ "Thu tiền sau".** `UC_CTbanDichVu_BoGhiSo.md` AC2 cấm khi có phiếu thu
riêng tham chiếu (MSG_..._010). FE tự kiểm hay chỉ hiển thị lỗi BE? Đề xuất: **BE kiểm, FE hiển thị**.
*(Liên quan Q10 — nếu bán dịch vụ không sinh `ENT_PhieuThu` thì tình huống này có xảy ra không?)*

**Q8 — Ma trận đang DRAFT.** Cả 3 file mang tiêu đề `[DRAFT — chờ duyệt]`, còn 2–3 "Điểm cần xác
nhận" chưa trả lời (Section "Thông tin bổ sung"; quy ước `Disable` xám hay label thuần; trạng thái
trường trong Tab Hóa đơn khi BR02 khóa checkbox).

**Q9 🆕 — Tab "Đính kèm".** Figma v2 vẽ tab này ở cả 2 biến thể tiền; BA epic 06195 không nhắc ở đâu.
Có thuộc phiếu này không? Nếu có thì cần đặc tả (loại file, dung lượng, nơi lưu).

**Q10 🆕 — Mâu thuẫn `ENT_PhieuThu` trong chính tài liệu v2.** Ba chỗ nói ba kiểu:

| Nguồn | Nói gì |
|---|---|
| `SCR_CTbanDichVu_ThemMoi.md:35` (**mới thêm**) | *"tích Thu tiền ngay **tự nó đóng vai phiếu thu — không sinh bản ghi `ENT_PhieuThu`**; dữ liệu lưu trên `ChungTuBan`"* |
| `UC_CTbanDichVu_ThemMoi.md:15` AC3 | *"Cả hai **sinh ENT_PhieuThu** phân biệt theo Hình thức thanh toán"* |
| `3.crud-matrix.md:22` | `ENT_PhieuThu` = **C** ở UC_GhiSo, **D** ở UC_BoGhiSo |

Ảnh hưởng: payload (có/không khối phiếu thu riêng), luồng Bỏ ghi sổ (MSG_..._010), và mapping cột
"Trạng thái thanh toán". **Chốt trước B5.**

**Q11 🆕 — Nút "Xem dữ liệu ghi sổ" chưa có trong bảng Chức năng của SCR.** BA vừa xoá Tab Hạch toán;
Figma bù bằng nút này. Nếu BA không bổ sung, người dùng **không còn chỗ nào** xem bút toán trước/sau
ghi sổ. Đề nghị BA bổ sung nút vào `SCR_CTbanDichVu_ThemMoi.md` §Chức năng + `SCR_CTbanDichVu_ChiTiet.md`.

---

## 13. Kiểm thử + cổng nghiệm thu

```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test && npm run build
```

Repo **đỏ sẵn** (baseline `docs/fe-khung-kien-truc-chuan.md:303-306`): `typecheck` 193 lỗi ·
`lint` 10 lỗi + 2 warning · `lint:boundaries` 76 (74 "rule not found" + 2 vi phạm thật trong `legacy`).

Luật: (1) không tăng số lỗi · (2) file mình chạm **0 lỗi** · (3) không sinh vi phạm tầng mới ·
(4) không `eslint-disable` để dập lint · (5) fail thì dán output thật.

Riêng phiếu này:

6. **Không hồi quy E-06194** — chạy lại đủ 8 test hiện có của module (`test/anHienVaDongBo.test.ts` ·
   `api.test.ts` · `chietKhau.test.ts` · `chungTuBanHang.render.test.tsx` · `payload.test.ts` ·
   `tinhToan.test.ts` · `tongHopPanel.render.test.tsx` · `tongHopVaHachToan.test.ts`), xanh **trước và
   sau**. ⚠ Việc mở `LOAI_NGHIEP_VU` lên 3 giá trị (D6) **chạm trực tiếp** vào
   `test/anHienVaDongBo.test.ts`.
7. **Cổng cây commit** — `npm run check:committed` sau khi commit; `git add` file mới **trước** khi
   sửa barrel/import trỏ tới nó.
8. **Ghi commit hash của `pmkt-docs`** đã đối chiếu vào PR (R8).

---

## 14. BR áp dụng

| BR chung | Áp ở đâu |
|---|---|
| BR1 · BR2 · BR11 · BR30 · BR31 · BR32 · BR44 | [01](01-danh-sach-dung-chung.md) — lưới dùng chung |
| BR13.1 · BR45 | [01](01-danh-sach-dung-chung.md), [05](05-popup-xac-nhan-xoa.md), [06](06-ghi-so-bo-ghi-so.md) |
| BR3 · BR13.2 · BR14 · BR15 · BR24 · BR34 · BR43 | [02](02-popup-them-moi.md), [03](03-popup-chinh-sua.md), [04](04-popup-xem-chi-tiet.md) |
| BR5 · BR6 · BR10 | [02](02-popup-them-moi.md) |
| BR4 · BR9 · BR12 · BR17 · BR33 · BR36 · BR37 · BR41 · BR42 | [02](02-popup-them-moi.md), [06](06-ghi-so-bo-ghi-so.md) |
| BR7 · BR18 | [02](02-popup-them-moi.md) |
| BR8 | [01](01-danh-sach-dung-chung.md) |
| BR16 · BR26 · BR27 | mọi file |
| BR19 · BR20 · BR28 · BR29 · BR46 | [05](05-popup-xac-nhan-xoa.md), [07](07-hop-dong-api-va-i18n.md) |
| BR21 | [02](02-popup-them-moi.md) |
| BR25 | §6 + mọi file |

**BR của epic CTBH (số hiệu v2 — ĐÃ ĐÁNH SỐ LẠI, đừng dùng số cũ):**

| Việc | BR v2 của `SCR_CTBH_ThemMoi.md` | ~~BR v1~~ |
|---|---|---|
| Auto-fill khách hàng | **BR01** | ~~BR07~~ |
| Ngày hạch toán / ngày chứng từ | **BR02** | — |
| Hạn thanh toán | **BR03** | — |
| Thu tiền ngay / hình thức TT | **BR04** | — |
| Lập kèm hóa đơn / Đã lập hóa đơn | **BR05** | ~~BR15~~ |
| Auto-fill từ danh mục vật tư | **BR07** | ~~BR07 mục b~~ |
| Hàng khuyến mại / CKTM | **BR09** | ~~BR02, BR03~~ |
| Số lượng · Đơn giá · Thành tiền | **BR11** | ~~BR18~~ |
| Chiết khấu (phân bổ) | **BR12** | ~~BR11~~ |
| Thuế GTGT (gồm "HH không TH tờ khai") | **BR13** (mục 6 = tổng hợp tab Thuế, mục 7 = checkbox) | ~~BR10~~ |
| Thuế XK | **BR14** | — |
| Diễn giải / Diễn giải thuế trên lưới | **BR15** | ~~BR20~~ |
| Tài khoản ngầm định | **BR16** | — |
| Ẩn cột kho theo dòng Dịch vụ | **BR17** | — |
| Kiêm phiếu xuất kho / phiếu thu | **BR18** | — |
| Không xuất kho / giá vốn | **BR19** | — |
| Sinh bút toán hạch toán | **BR20** | ~~BR12~~ |
| Ghi sổ / Bỏ ghi sổ | **BR21** | ~~BR13~~ |
| Theo dõi số lượng đã xuất | **BR23** | ~~BR17~~ |
| Phạm vi `LoaiNghiepVu` theo màn khởi tạo | **BR24** 🆕 | — |

**BR chưa xử lý được (kèm lý do):**

- **BR38 · BR39** — lưới dùng chung chưa có; nợ của E-06194.
- **BR35** — "Thu tiền"/"Lập hóa đơn" điều hướng sang module chưa dựng.
- **BR17 (chung) kỳ kế toán** — FE không có API kỳ; chỉ hiển thị lỗi BE.

---

## 15. Tài liệu tham chiếu

- Phiếu yêu cầu: `pmkt-docs/ba/PMKT-E-06195_ChungTuBanDichVu/` — **đối chiếu tại commit `1a928c53b`**
- Epic tham chiếu xuyên suốt: `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/5.screens/SCR_CTBH_ThemMoi.md`,
  `SCR_CTBH_DanhSach.md`, `SCR_CTBH_PopupXacNhanXoa.md`
- BR chung: `pmkt-docs/ba/Common/business_rules.md`
- Khung FE: `docs/fe-khung-kien-truc-chuan.md` · `client/CLAUDE.md` · `docs/conventions.md` · `CLAUDE.md`
- Module tham chiếu: `client/src/features/banHang/chungTuBanHang/`
- Plan BE của epic anh em: `docs/doing/PMKT-E-06194-chung-tu-ban-hang-api/`

---

## 16. Nhật ký thay đổi so với v1

| # | v1 (đối chiếu tài liệu trước 12/08) | **v2 (hiện tại)** |
|---|---|---|
| 1 | D2: hai entity `ENT_ChungTuBanDichVu` + `ENT_ChiTietChungTuBanDV`, hai endpoint, 12 endpoint mới ở [07](07-hop-dong-api-va-i18n.md) | **MỘT** entity `ENT_ChungTuBan`, **một** endpoint, thêm `loaiNghiepVu`. Bỏ hẳn `api/chungTuBanDichVuApi.ts` |
| 2 | Q2 "một hay hai endpoint?" là câu hỏi **chặn** | **BA đã trả lời** (`SCR_CTBH_DanhSach` BR01). Q2 v2 đổi thành "phân quyền theo dòng thế nào" |
| 3 | "Bán dịch vụ không có Loại nghiệp vụ" | **D6** — có, cố định `Bán dịch vụ`, ẩn UI, bất biến sau khi lưu (BR24) |
| 4 | Có **Tab Hạch toán** trong ma trận và tab list | **D7** — BA xoá tab; Figma thay bằng nút **"Xem dữ liệu ghi sổ"** + popup |
| 5 | Field `ChungTuBanDichVu.*`, `ChiTietChungTuBanDV.*`, `TrangThaiChungTu`, `MoTa` | `ChungTuBan.*`, `ChiTietChungTuBan.*`, **`TrangThaiGhiSo`**, **`DienGiai`**, `MaSoThueCCCD` … |
| 6 | Figma node `14770-340432` | **2 node**: Nguyên tệ `61661-103452` · Ngoại tệ `61685-126981` |
| 7 | Trích BR của CTBH theo số cũ (BR07/BR10/BR11/BR12/BR13/BR15/BR17/BR18) | **Đánh số lại toàn bộ** — bảng ánh xạ ở §14 |
| 8 | Conflict C1 · C3 · C4 · C9 | **Đã hết** (Figma v2 sửa) |
| 9 | — | **Conflict mới** C12 (nhãn "Mã hàng hóa") · C13 (tab Đính kèm) · C14 (nút Xem dữ liệu ghi sổ) · C15 (tiêu đề) · C16 (nguyên tệ ↔ ngoại tệ lệch) · C17 (thiếu ô Tỷ giá) |
| 10 | — | **Q9 · Q10 · Q11** mới; **R8 · R9** mới |
