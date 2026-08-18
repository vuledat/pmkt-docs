# 01 — Danh sách Chứng từ bán dịch vụ (màn DÙNG CHUNG với Chứng từ bán hàng)

| | |
|---|---|
| **Phiên bản** | **v2 — 2026-08-15** (đồng bộ BA commit `1a928c53b`) |
| **SCR nguồn** | `5.screens/SCR_CTbanDichVu_DanhSach.md` → tham chiếu `PMKT-E-06194/5.screens/SCR_CTBH_DanhSach.md` |
| **UC nguồn** | `UC_CTbanDichVu_DanhSach` (PMKT-U-06196) |
| **Ma trận** | Không có — `Matrix/.../_scope.md` xếp **SKIP** |
| **Figma** | Danh sách: [node 58263-112028](https://www.figma.com/design/ymMyg329ejsgCWg28CNmGl/Ph%E1%BA%A7n-m%E1%BB%81m-K%E1%BA%BF-to%C3%A1n---Viettel?node-id=58263-112028) — frame của E-06194 (`SCR_CTBH_DanhSach.md:11`); CTBDV **không** có frame danh sách riêng. *(v1 ghi node `14770-338328` — đã cũ.)* |
| **Route** | `/ban-hang/chung-tu-ban-hang` — **không thêm route** |
| **Code** | `components/ChungTuBanHangTab.tsx` · `components/ChungTuBanHangListTable.tsx` · `fields/columns.ts` |

> **Phạm vi rất hẹp:** lưới danh sách **đã dựng xong** cho E-06194. Phiếu này chỉ làm phần **khác biệt
> của chứng từ bán dịch vụ trên chính lưới đó**.

---

## 1. Bố cục

Giữ nguyên (`pages/ChungTuBanHangPage.tsx:52-64`):

```
TabMenu2Level (4 tab: Chứng từ bán hàng | Trả lại hàng bán | Điều chỉnh hàng bán | Hóa đơn)
└── tab 1 (đã dựng) — ChungTuBanHangTab
    ├── Toolbar: [Thêm mới ▾] … [Tìm kiếm nhanh] [Lọc] [Tải lại] [Xuất Excel] [Cấu hình cột]
    ├── CommonListTable — 15 cột + cột "Chức năng" cố định phải (92px)
    ├── Dòng tổng cộng (server summary — BR31 / BR05 của BA)
    ├── Phân trang
    └── Panel Xem nhanh (quick detail) bên dưới
```

**Nguồn dữ liệu (BA v2 nói thẳng — `SCR_CTBH_DanhSach.md` BR01):**
lấy toàn bộ bản ghi **`ENT_ChungTuBan`** của tenant, phân biệt hai loại bằng
**`ChungTuBan.LoaiNghiepVu`**. `SCR_CTbanDichVu_DanhSach.md` **BR06** nhắc lại: *"Chứng từ bán dịch vụ
**không có màn danh sách riêng**"*.

⇒ **Một truy vấn, một resource** — [00 §0 D2](00-ke-hoach-tong.md). Câu hỏi Q2 của v1 đã được BA
trả lời.

---

## 2. Đặc tả UI

Không có đặc tả UI mới. Kích thước / spacing / typography giữ nguyên bản đã dựng cho E-06194;
Figma của E-06195 không vẽ lại màn danh sách.

---

## 3. Ma trận ẩn/hiện · required · disabled

Không áp dụng — `_scope.md` loại màn danh sách khỏi phạm vi ma trận form. Quy tắc hiển thị nút ở §5.

---

## 4. Bảng cột — mapping nguồn dữ liệu + khác biệt của dòng bán dịch vụ

Bộ cột giữ nguyên (`fields/columns.ts:56-99`). **Tên field đã đổi theo LDM v2** — bảng dưới lấy
nguyên từ `SCR_CTBH_DanhSach.md` BR01:

| # | Cột hiển thị | Khóa i18n | **Field v2** | ~~Field v1~~ | Ghi chú |
|---|---|---|---|---|---|
| 1 | Checkbox | — | — | — | chọn dòng, không lưu |
| 2 | STT | — | — | — | theo trang, không lưu |
| 3 | Ngày hạch toán | `list.col.ngayHachToan` | `ChungTuBan.NgayHachToan` | — | sort mặc định #1 |
| 4 | Ngày chứng từ | `list.col.ngayChungTu` | `ChungTuBan.NgayChungTu` | — | ngày của **phần ghi nợ**, không lấy ngày xuất kho / thu tiền |
| 5 | Số chứng từ | `list.col.soChungTu` | `ChungTuBan.SoChungTu` | — | Hyperlink → popup Xem |
| 6 | Số hóa đơn | `list.col.soHoaDon` | `HoaDonBan.SoHoaDon` (join `HoaDonBan.ChungTuBanId`) | ~~`SoHoaDon`~~ | nhiều hóa đơn ⇒ ngăn cách dấu phẩy; chưa có ⇒ trống |
| 7 | Khách hàng | `list.col.khachHang` | `ChungTuBan.TenKhachHang` | ~~`TenKhachHang`~~ | `textMode: 'long'` (BR44 nhóm 2) |
| 8 | Thành tiền | `list.col.thanhTien` | `ChungTuBan.TongTienHang` | ~~`TongTienHangHoaQuyDoi`~~ | ngoại tệ ⇒ `TongTienHangQuyDoi` |
| 9 | Tiền chiết khấu | `list.col.tienChietKhau` | `ChungTuBan.TongChietKhau` | ~~`TongTienChietKhauQuyDoi`~~ | ngoại tệ ⇒ `TongChietKhauQuyDoi` |
| 10 | Tiền thuế GTGT | `list.col.tienThueGTGT` | `ChungTuBan.TongThueGTGT` | ~~`TongTienThueGTGTQuyDoi`~~ | ngoại tệ ⇒ `TongThueGTGTQuyDoi` |
| 11 | Tổng tiền thanh toán | `list.col.tongTienThanhToan` | `ChungTuBan.TongThanhToan` | ~~`TongTienThanhToanQuyDoi`~~ | ngoại tệ ⇒ `TongThanhToanQuyDoi` |
| 12 | Trạng thái lập hóa đơn | `list.col.trangThaiHoaDon` | `ChungTuBan.TrangThaiLapHoaDon` | ~~`TrangThaiHoaDon`~~ | badge |
| 13 | Trạng thái thanh toán | `list.col.trangThaiThanhToan` | `ChungTuBan.TrangThaiThanhToan` | — | badge |
| 14 | **Trạng thái xuất hàng** | `list.col.trangThaiXuatHang` | `ChungTuBan.TrangThaiXuatHang` | — | ⚠ **để trống với dòng bán dịch vụ** |
| 15 | Trạng thái chứng từ | `list.col.trangThaiChungTu` | **`ChungTuBan.TrangThaiGhiSo`** | ~~`TrangThaiChungTu`~~ | badge, màu theo BR33 |
| 16 | Chức năng | — | — | — | cụm nút trên dòng (§5.2) |

**Hai khác biệt duy nhất của dòng bán dịch vụ:**

| Thành phần | Dòng bán hàng hóa | **Dòng bán dịch vụ** | Nguồn |
|---|---|---|---|
| Cột "Trạng thái xuất hàng" | badge Đã xuất đủ / Đã xuất 1 phần / Chưa xuất hàng | **ô trống**, không render badge | `SCR_CTBH_DanhSach.md` BR01 + `SCR_CTbanDichVu_DanhSach.md` BR06 |
| Nút "Lập phiếu xuất" | hiện theo điều kiện | **ẩn hẳn** | `SCR_CTBH_DanhSach.md` §Chức năng trên từng dòng |

**Cột tiền theo đồng tiền hạch toán** — chứng từ ngoại tệ lấy cột quy đổi (BR01 gạch đầu dòng 2).
Định dạng theo BR7; truncate theo BR44; ẩn/hiện cột theo BR30 (`ColumnConfigDrawer` đã có).

**Dòng tổng cộng (BR05):** cộng dồn `ChungTuBan.TongChietKhau` / `TongThueGTGT` / `TongThanhToan` của
các chứng từ trong bộ lọc. BA v2 nói rõ: **lấy theo số tổng đã lưu, không tính lại** ⇒ FE dùng
`summary` server trả về, **không** tự cộng client-side (fallback cộng trang hiện tại chỉ dùng khi
`summary` chưa về — hành vi hiện có ở `ChungTuBanHangListTable.tsx`).

---

## 5. Hành vi & sự kiện

### 5.1 Dropdown "Thêm mới"

Ba mục, đã khai ở `components/ChungTuBanHangListTable.tsx:67-74`. **BR24 của `SCR_CTBH_ThemMoi.md`
nói rõ dropdown này là chỗ duy nhất phân nhánh loại nghiệp vụ:**

| Mục | Gate hiện tại (`:184-188`) | **Gate đúng sau phiếu này** | Việc khi click |
|---|---|---|---|
| Chứng từ bán hàng | `gates.create` (`BanHangHoa.Create`) | giữ nguyên | popup, combo Loại nghiệp vụ = `Bán hàng trong nước` \| `Bán hàng xuất khẩu` (**ẩn** `Bán dịch vụ`) |
| **Chứng từ bán dịch vụ** | `gates.create` — **SAI**, đang dùng chung mã bán hàng hóa | **`BanDichVu.Create`** | popup với `loaiNghiepVu = 'Bán dịch vụ'` **cố định, ẩn ô** ([02](02-popup-them-moi.md)) |
| Thu tiền theo hóa đơn | `gates.thuTien` | giữ nguyên | giữ "coming soon" (ngoài phạm vi) |

> Đây chính là OPEN ITEM ở `ChungTuBanHangListTable.tsx:179-183` và `constants/permissions.ts:25-30`.
> Mã đã tồn tại: `MaChucNang.java:217`. **Gỡ được cả hai chỗ.**

Nút split chạy mục đầu tiên user có quyền (`:196-201`) — **giữ nguyên**, chỉ đổi tập `allowed`.

Phải sửa: `components/ChungTuBanHangTab.tsx:247-256` — mọi `variant` không phải `thuTienTheoHoaDon`
đều mở cùng một popup `mode: 'create'`; phải truyền `loaiNghiepVu` xuống modal.

### 5.2 Nút trên từng dòng (⋮ + icon)

Catalog ⋮ đã khai ở `ChungTuBanHangListTable.tsx:53-61`: `edit · thuTien · lapHoaDon · boGhiSo ·
ghiSo · ─ · delete`.

| Nút | Điều kiện hiện (`TrangThaiGhiSo`) | Quyền (dòng bán dịch vụ) | Việc |
|---|---|---|---|
| Xem chi tiết (👁 / link Số chứng từ) | luôn | `BanDichVu.View.Detail` | [04](04-popup-xem-chi-tiet.md) |
| Chỉnh sửa | `= "Chưa ghi sổ"` | `BanDichVu.Edit` | [03](03-popup-chinh-sua.md) |
| Xóa | `= "Chưa ghi sổ"` | `BanDichVu.Delete` | [05](05-popup-xac-nhan-xoa.md) |
| Ghi sổ | `= "Chưa ghi sổ"` | `BanDichVu.Post` | [06](06-ghi-so-bo-ghi-so.md) |
| Bỏ ghi | `= "Đã ghi sổ"` | `BanDichVu.Unpost` | [06](06-ghi-so-bo-ghi-so.md) |
| Thu tiền | `= "Đã ghi sổ"` AND `TrangThaiThanhToan ∈ {Chưa thanh toán, Đã thanh toán một phần}` | quyền chức năng *(BA v2 bỏ nhắc mã cụ thể)* | **coming soon** |
| Lập hóa đơn | `= "Đã ghi sổ"` AND `TrangThaiLapHoaDon ∈ {Chưa lập, Đã lập một phần}` | quyền lập hóa đơn | **coming soon** |
| **Lập phiếu xuất** | — | — | **KHÔNG hiện với dòng bán dịch vụ** |

Helper thuần đã có: `helpers/trangThai.ts:53 coTheGhiSo` · `:58 coTheBoGhiSo` — **dùng lại**, chỉ đổi
nguồn quyền và tên field.

**Không có quyền ⇒ ẩn nút, KHÔNG disable** (BR25.2). Double-click dòng ⇒ mở Xem chi tiết (BR13.1),
kiểm `.View.Detail` trước.

### 5.3 Thao tác hàng loạt

| Nút | Điều kiện hiện | Việc |
|---|---|---|
| Ghi sổ hàng loạt | ≥1 dòng tích chọn (BR13.1) | [06 §4](06-ghi-so-bo-ghi-so.md) |
| Bỏ ghi sổ hàng loạt | ≥1 dòng tích chọn | [06 §4](06-ghi-so-bo-ghi-so.md) |
| Xóa hàng loạt | ≥1 dòng tích chọn — **luôn enabled** | [05 §5.2](05-popup-xac-nhan-xoa.md) · `UC_CTbanDichVu_Xoa.md` |

Tất cả theo BR45: bỏ qua bản ghi không đủ điều kiện, popup kết quả chi tiết, đóng popup ⇒ reload giữ
nguyên lọc/sắp xếp/phân trang.

Chọn lẫn hai loại chứng từ trong một lần: xử lý theo quyền **của từng dòng**; dòng thiếu quyền bị bỏ
qua và liệt kê ở popup kết quả với nguyên nhân "Không có quyền" (MSG_PMKT-E-06195_011).
*Cách diễn đạt cần BA xác nhận.*

### 5.4 Bộ lọc, tìm kiếm, sắp xếp

Giữ nguyên: phễu ngày mặc định "Đầu tháng đến hiện tại" + nhớ theo phiên
(`ChungTuBanHangTab.tsx:88-100`), sắp xếp mặc định
`ngayHachToan:desc,ngayChungTu:desc,soChungTu:asc` (`api/chungTuBanHangApi.ts:39`), phân trang
server-side, dòng tổng server.

**Bổ sung:** thêm `loaiNghiepVu` vào `ADV_FILTER_WIRE` (`api/chungTuBanHangApi.ts:52-56`, op `eq`) để
lọc riêng từng loại khi cần. Đây là hệ quả trực tiếp của D2 (một endpoint).

---

## 6. Validation phía FE

Không có form ⇒ không có validation nhập liệu. Lỗi hiển thị:

| Tình huống | Message | Nguồn |
|---|---|---|
| Không có quyền xem danh sách | MSG_PMKT-E-06195_011 "Không có quyền truy cập" | **BE** (route guard 403 — BR25.2) |
| Lỗi tải dữ liệu | MSG_PMKT-E-06195_013 "Lỗi hệ thống" | **BE**; FE hiển thị qua `describeApiError` |
| Không có dữ liệu | "Không có dữ liệu" | đã có `CommonEmpty` |

---

## 7. Luồng xử lý

1. Vào route → `<RequirePermission>` kiểm `handle.perm` (⚠ **Q3** — [00 §6](00-ke-hoach-tong.md)).
2. `ChungTuBanHangTab` dựng `params` → `toSearchRequest` → `useSearch` (`api/queries.ts:14-18`).
   **Không đổi resource** — response thêm `loaiNghiepVu` mỗi dòng.
3. Mỗi dòng: `gatesChoDong(row, has)` chọn bộ quyền theo `row.loaiNghiepVu` → truyền vào
   `RowActionButtons` / `CommonActionMenu`.
4. Click Thêm mới → mục dịch vụ → `setModal({ open: true, mode: 'create', loaiNghiepVu: 'Bán dịch vụ' })`.
5. Click ⋮ → dispatcher `onRowMenuAction` (`ChungTuBanHangTab.tsx:288-301`) → popup / mutation tương
   ứng, kèm `loaiNghiepVu` suy từ dòng.
6. Mọi mutation xong → toast (BR26) + `invalidate: 'all'` (`api/queries.ts:17`) → lưới tự nạp lại.
7. Loading `isLoading`; Empty `CommonEmpty`; Error toast đỏ + giữ dữ liệu cũ.

---

## 8. Phân bổ file

| Việc | File |
|---|---|
| `LOAI_NGHIEP_VU` lên 3 giá trị | `constants/constants.ts` (đang ở `:20`, chỉ có 2) |
| `BAN_DICH_VU_PERM` | `constants/permissions.ts` |
| `loaiNghiepVu` trong row schema + đổi tên field theo LDM v2 | `api/model.ts` |
| `loaiNghiepVu` vào `ADV_FILTER_WIRE` | `api/chungTuBanHangApi.ts` |
| Chọn bộ quyền theo dòng — hàm thuần `gatesChoDong(row, has)` | `helpers/quyen.ts` 🆕 |
| Ẩn "Lập phiếu xuất" + để trống "Trạng thái xuất hàng" | `fields/columns.ts` |
| Gate mục dropdown Thêm mới | `components/ChungTuBanHangListTable.tsx` |
| Dispatcher `onAdd` / `onRowMenuAction` mang `loaiNghiepVu` | `components/ChungTuBanHangTab.tsx` |
| Nhãn mới | `i18n/vi.ts` · `i18n/en.ts` |

---

## 9. Kiểm thử

| # | Input | Kỳ vọng |
|---|---|---|
| T1 | `gatesChoDong` với `row.loaiNghiepVu = 'Bán dịch vụ'`, user có `BanDichVu.Edit` nhưng không có `BanHangHoa.Edit` | `edit = true` |
| T2 | như T1 đảo lại (chỉ có `BanHangHoa.Edit`) | `edit = false` |
| T3 | Dòng bán dịch vụ | cột "Trạng thái xuất hàng" render rỗng, **không** badge |
| T4 | Dòng bán dịch vụ | menu dòng **không** chứa "Lập phiếu xuất" |
| T5 | Dòng bán hàng hóa, "Đã ghi sổ", `TrangThaiXuatHang = "Chưa xuất hàng"` | menu dòng **có** "Lập phiếu xuất" (chống hồi quy E-06194) |
| T6 | User chỉ có `BanDichVu.Create` | dropdown Thêm mới chỉ có mục "Chứng từ bán dịch vụ"; nút split chạy đúng mục đó |
| T7 | User không có quyền create nào, có `thuTien` | dropdown chỉ có "Thu tiền theo hóa đơn" |
| T8 | Click mục "Chứng từ bán dịch vụ" | modal mở `mode='create'`, `loaiNghiepVu='Bán dịch vụ'` |
| T9 | `toSearchRequest` với `advFilters.loaiNghiepVu = 'Bán dịch vụ'` | sinh criterion `{ field: 'loaiNghiepVu', op: 'eq', value: 'Bán dịch vụ' }` |
| T10 | response thiếu `loaiNghiepVu` (BE cũ) | Zod `.nullish()` không vỡ trang; dòng rơi về bộ quyền mặc định `BanHangHoa` |

---

## 10. BR đã áp dụng

BR1 · BR2 · BR7 · BR8 · BR11 · BR12 · BR13.1 · BR25 · BR26 · BR30 · BR31 · BR32 · BR33 · BR42.2 ·
BR44 · BR45. Của CTBH: **BR01** (nguồn dữ liệu) · **BR02** (lọc/sắp xếp mặc định) · **BR05** (dòng
tổng) · **BR24** (phân nhánh loại nghiệp vụ ở dropdown Thêm mới).

**Chưa đạt:** BR38 (nhóm cột) · BR39 (xuất Excel) — chưa dựng trên lưới dùng chung, không thuộc yêu
cầu E-06195. Nợ của E-06194.
