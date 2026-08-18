# 07 — Hợp đồng API · i18n · hằng số · quyền · đường dẫn

**Phiên bản: v2 — 2026-08-15** (đồng bộ BA commit `1a928c53b`).
⚠ **Đổi lớn so với v1:** BA đã chốt **MỘT entity `ENT_ChungTuBan`** ⇒ mục §1 của v1 (12 endpoint
`/chung-tu-ban-dich-vu`) **đã bị bỏ hoàn toàn**. Xem [00 §0 D2](00-ke-hoach-tong.md).

---

## 1. Hợp đồng với BE

### 1.1 Nguyên tắc: KHÔNG thêm resource mới

`SCR_CTBH_ThemMoi.md` **BR24**: *"Hai màn Thêm mới dùng **chung entity** `ChungTuBan` /
`ChiTietChungTuBan`; `LoaiNghiepVu` là trường phân biệt luồng nghiệp vụ, **không tách entity riêng**"*.
`SCR_CTBH_DanhSach.md` **BR01**: danh sách lấy toàn bộ `ENT_ChungTuBan`, phân biệt bằng `LoaiNghiepVu`.

⇒ FE dùng **đúng resource sẵn có**: base `/api/ban-hang/chung-tu-ban-hang`
(`api/chungTuBanHangApi.ts:32`), adapter `chungTuBanHangApi` (`:110-114`), query family
`chungTuBanHangQueries` (`api/queries.ts:14-18`). **Không** tạo `chungTuBanDichVuApi.ts`, **không**
tạo query family thứ hai.

> Base path hiện mang chữ "chung-tu-ban-hang" trong khi resource nay phục vụ cả hai loại. Đổi thành
> `/api/ban-hang/chung-tu-ban` sẽ khớp LDM hơn — **nhưng đó là quyết định của BE**, FE không tự đổi.
> Nêu khi review plan BE.

### 1.2 Endpoint cần (bám BASE CRUD wire contract v1 — `api/chungTuBanHangApi.ts:5-19`)

| # | Method · Path | Quyền BE | Trạng thái | Việc |
|---|---|---|---|---|
| E1 | `POST {base}/search` | `BanHangHoa.View` **và/hoặc** `BanDichVu.View` | ✅ có, ⚠ thiếu `loaiNghiepVu` | danh sách + `pagination` + `summary` (BR31 / BR05) |
| E2 | `GET {base}/cot` | như trên | ✅ có | whitelist `@Searchable` |
| E3 | `GET {base}/{id}` | `.View.Detail` | ✅ có | chứng từ **kèm** `chiTiet` |
| E4 | `POST {base}` | `.Create` (+ `.Post` nếu `ghiSo=true`) | ✅ có, ⚠ thiếu `loaiNghiepVu` | tạo mới / tạo + ghi sổ |
| E5 | `PUT {base}/{id}` | `.Edit` (+ `.Post`) | ❌ **chưa dựng** | cập nhật; body mang `updatedAt` |
| E6 | `DELETE {base}/{id}` | `.Delete` | ✅ có | xóa mềm; body mang `updatedAt` |
| E7 | `POST {base}/xoa-hang-loat` | `.Delete` | ❌ chưa nối FE | trả `KetQuaHangLoatDto` |
| E8 | `POST {base}/{id}/ghi-so` | `.Post` | ❌ chưa nối FE | — |
| E9 | `POST {base}/ghi-so-hang-loat` | `.Post` | ❌ chưa nối FE | trả `KetQuaHangLoatDto` |
| E10 | `POST {base}/{id}/bo-ghi-so` | `.Unpost` | ❌ chưa nối FE | — |
| E11 | `POST {base}/bo-ghi-so-hang-loat` | `.Unpost` | ❌ chưa nối FE | trả `KetQuaHangLoatDto` |
| E12 | `POST {base}/lookup` | `.View` | ✅ có | danh mục (KH · **dịch vụ** · TK · ĐVT · NV · loại tiền · điều khoản TT · TK ngân hàng) |
| **E13** 🆕 | `GET {base}/{id}/but-toan` | `.View.Detail` | ❌ **chưa có** | dữ liệu popup "Xem dữ liệu ghi sổ" ([00 D7](00-ke-hoach-tong.md)) |

Mọi response bọc `ApiResponse<T>` — FE đọc `res.data.data` (`docs/fe-khung-kien-truc-chuan.md:204`).

### 1.3 ❗ Việc BE phải làm cho epic này

| # | Việc | Vì sao |
|---|---|---|
| **A1** | Thêm `ChungTuBan.LoaiNghiepVu` (3 giá trị: `Bán hàng trong nước` · `Bán hàng xuất khẩu` · `Bán dịch vụ`) vào entity, DTO, `@Searchable` whitelist, và body ghi | BR24 — trục phân biệt duy nhất |
| **A2** | `POST /search` **lọc theo quyền của người dùng** (trả dòng nào họ được xem) thay vì chặn cả request | Một entity, **hai** mã chức năng (`BanHangHoa` / `BanDichVu`) ⇒ **Q2 v2** |
| **A3** | Gate `POST` / `PUT` / `DELETE` / ghi sổ / bỏ ghi sổ theo `LoaiNghiepVu` của bản ghi | như A2 |
| **A4** | Chặn đổi `LoaiNghiepVu` giữa nhóm bán hàng ↔ bán dịch vụ ở `PUT` | BR24: *"Chứng từ đã lưu không đổi được"* |
| **A5** | Trả cờ hoặc danh sách hóa đơn liên kết để FE suy "Đã lập hóa đơn do hệ thống tích" | **Q-BR02** — xem §1.5 |
| **A6** | `E13` — endpoint bút toán | D7 thay Tab Hạch toán |
| **A7** | Xác nhận chứng từ bán dịch vụ **có / không** sinh `ENT_PhieuThu` | **Q10** — xem §1.6 |

### 1.4 Row schema (`api/model.ts`) — đổi tên field theo LDM v2

```ts
/** Loại nghiệp vụ — trục phân biệt bán hàng hóa / bán dịch vụ trên resource dùng chung (BR24).
 *  z.string() chứ không z.enum: BE có thể thêm giá trị, một giá trị lạ phải degrade về mặc định
 *  chứ không được reject cả trang (cùng lý do với 4 cột trạng thái, xem api/model.ts:14-18). */
export const loaiNghiepVuSchema = z.string()
```

| Field v1 (plan cũ) | **Field v2 (LDM)** | Nguồn |
|---|---|---|
| `ChungTuBanDichVu.*` | **`ChungTuBan.*`** | BR24 · `3.crud-matrix.md` |
| `ChiTietChungTuBanDV.*` | **`ChiTietChungTuBan.*`** | `SCR_CTbanDichVu_ThemMoi.md` §Tab Chi tiết dịch vụ |
| `TrangThaiChungTu` | **`TrangThaiGhiSo`** | `SCR_CTBH_DanhSach.md` BR01 · `SCR_CTbanDichVu_ThemMoi.md` §Chức năng |
| `TrangThaiHoaDon` | **`TrangThaiLapHoaDon`** | `SCR_CTBH_DanhSach.md` BR01 |
| `MoTa` (đầu chứng từ) | **`DienGiai`** | BR01 của CTBDV |
| `MoTa` (dòng chi tiết) | **`ChiTietChungTuBan.DienGiai`** | **BR15** của CTBH |
| `MaSoThue` | **`MaSoThueCCCD`** | §Tab Chứng từ ghi nợ |
| `TongTienHangHoaQuyDoi` | **`TongTienHang`** (+ `TongTienHangQuyDoi`) | `SCR_CTBH_DanhSach.md` BR01 |
| `TongTienChietKhauQuyDoi` | **`TongChietKhau`** (+ `TongChietKhauQuyDoi`) | như trên |
| `TongTienThueGTGTQuyDoi` | **`TongThueGTGT`** (+ `TongThueGTGTQuyDoi`) | như trên |
| `TongTienThanhToanQuyDoi` | **`TongThanhToan`** (+ `TongThanhToanQuyDoi`) | như trên |
| `ENT_KhachHang` | **`ENT_DoiTuong`** | `3.crud-matrix.md` |
| `ENT_HoaDonBanHang` | **`ENT_HoaDonBan`** (khóa `HoaDonBan.ChungTuBanId`) | `3.crud-matrix.md` · BR01 |

**Dòng chi tiết dịch vụ** = `chungTuBanHangChiTietSchema` (`api/model.ts:47+`) **trừ** các khóa
kho / giá vốn / quy đổi ĐVT / thuế XK: `khoId · soLo · hanSuDung · taiKhoanKhoId · taiKhoanGiaVonId ·
tuNhapDonGiaVon · donGiaVon · donGiaVonQuyDoi · soLuongDaXuatKho · soLuongDaXuatKhoQuyDoi ·
soLuongConLaiXuatKho · donGiaThueXk · phanTramThueXk · tienThueXk · tienThueXkQuyDoi ·
taiKhoanThueXkId` + hệ số / số lượng / đơn giá quy đổi ĐVT (**BR14** · **BR17** · **BR19**).

**Vẫn giữ** (dịch vụ có): `soLuongDaXuatHd` · `soLuongConLaiXuatHd` (**BR23**).

> **Cách làm ở FE:** giữ **một** schema chi tiết dùng chung (các khóa kho `.nullish()`), phân biệt
> hiển thị bằng `visible` ở `fields/chiTietFields.ts`. Tách hai schema chỉ đẻ thêm một nhánh
> `formDetail.ts` phải đồng bộ tay.

### 1.5 ❗ `Q-BR02` — nguồn tích checkbox "Đã lập hóa đơn"

BR02 của `SCR_CTbanDichVu_CapNhat.md` phân biệt: NSD tự tích ⇒ cho sửa; **hệ thống** tích ⇒ disable
cả 2 checkbox. FE không suy được từ hợp đồng hiện tại.

Hai phương án, **đề xuất phương án 2** (nói lên *vì sao*, không chỉ *rằng*):

1. `daLapHoaDonDoHeThong: boolean`
2. **`hoaDonLienKet: { id, soHoaDon }[]`** — FE suy `daLapHoaDonDoHeThong = hoaDonLienKet.length > 0`.
   LDM v2 đã có quan hệ `HoaDonBan.ChungTuBanId` (dùng ở BR01 để dựng cột "Số hóa đơn"), nên trường
   này **có thể đã sẵn** ở tầng dữ liệu — chỉ cần lộ ra `GET /{id}`.

### 1.6 ❗ `Q10` — chứng từ bán dịch vụ có sinh `ENT_PhieuThu` không?

| Nguồn | Nói gì |
|---|---|
| `SCR_CTbanDichVu_ThemMoi.md:35` (**mới thêm v2**) | *"tích Thu tiền ngay **tự nó đóng vai phiếu thu — không sinh bản ghi `ENT_PhieuThu`**; dữ liệu lưu trên `ChungTuBan`"* (dẫn **BR18** của CTBH) |
| `UC_CTbanDichVu_ThemMoi.md:15` AC3 | *"Cả hai **sinh ENT_PhieuThu** phân biệt theo Hình thức thanh toán"* |
| `3.crud-matrix.md:22` | `ENT_PhieuThu` = **C** ở UC_GhiSo, **D** ở UC_BoGhiSo |

**Ảnh hưởng FE:** hình dạng payload (khối phiếu thu là field trên `ChungTuBan` hay object con), luồng
Bỏ ghi sổ (MSG_..._010 có xảy ra không — [06 §3](06-ghi-so-bo-ghi-so.md)), và cách hiển thị "Trạng
thái thanh toán".

**Bằng chứng nghiêng về phương án "không sinh":** bảng trường Tab Phiếu thu của CTBH v2 dùng field
`ChungTuBan.NguoiNopTien` · `ChungTuBan.LyDoThu` · `ChungTuBan.TaiKhoanTienId` ·
`ChungTuBan.NgayChungTuThuTien` · `ChungTuBan.SoChungTuThuTien` — **tất cả đều trên `ChungTuBan`**,
không phải trên một entity phiếu thu riêng.

### 1.7 Body ghi (`api/payload.ts`)

```ts
/** Create và update dùng chung một shape; PUT thêm `updatedAt` (optimistic lock, BR12).
 *  `ghiSo: true` là nút "Lưu và ghi sổ" — MỘT request, MỘT transaction (BR21).
 *  `loaiNghiepVu` BẮT BUỘC: BE dựa vào nó để định tuyến nghiệp vụ (BR24). Ở PUT thì gửi nguyên giá
 *  trị của bản ghi gốc — đổi giữa nhóm bán hàng ↔ bán dịch vụ bị cấm. */
export interface LuuChungTuBanBody extends Record<string, unknown> {
  loaiNghiepVu: string
  ghiSo?: boolean
  updatedAt?: string | null
}
```

Giữ shape mở như `LuuChungTuBanHangBody` (`api/chungTuBanHangApi.ts:105-108`) cho tới khi BE chốt
DTO — khai đủ ~45 trường lúc này chỉ là đoán.

**Biến thể dịch vụ bỏ khỏi payload:** mọi trường kho / giá vốn / quy đổi ĐVT / thuế XK / phiếu xuất
kho (**BR14** · **BR17** · **BR19** · **BR24**).

### 1.8 `KetQuaHangLoatDto` (E7 · E9 · E11)

```ts
export const ketQuaHangLoatSchema = z.object({
  tongSo: z.number(),
  thanhCong: z.number(),
  thatBai: z.number(),
  chiTietLoi: z.array(z.object({
    id: z.string(),
    soChungTu: z.string().nullish(),
    ngayChungTu: z.string().nullish(),
    nguyenNhan: z.string(),      // message nguyên văn của BE, FE KHÔNG diễn đạt lại
  })).default([]),
})
```

Đủ để dựng popup BR45.3 (tổng kết + bảng `Số chứng từ · Ngày chứng từ · Nguyên nhân`).

### 1.9 Bút toán cho popup "Xem dữ liệu ghi sổ" (E13) 🆕

```ts
export const butToanSchema = z.object({
  ngayHachToan: z.string(),
  ngayChungTu: z.string(),
  soChungTu: z.string(),
  maDoiTuong: z.string().nullish(),
  tenDoiTuong: z.string().nullish(),
  dienGiai: z.string().nullish(),
  taiKhoan: z.string(),
  taiKhoanDoiUng: z.string(),
  phatSinhNo: z.number().nullish(),
  phatSinhCo: z.number().nullish(),
  vuViec: z.string().nullish(),
  khoanMucChiPhi: z.string().nullish(),
  doiTuongTapHopChiPhi: z.string().nullish(),
  donVi: z.string().nullish(),
})
```

Cột lấy đúng theo Figma node **61661:104532**. Σ `phatSinhNo` phải **bằng** Σ `phatSinhCo`.
**Chưa có endpoint** ⇒ tạm dựng client-side từ `helpers/hachToan.ts:49 sinhButToan` trên dữ liệu
form; ghi nhận là **nợ**, chuyển sang đọc server khi E13 có.

### 1.10 Sắp xếp & lọc

Giữ nguyên hợp đồng hiện tại (`api/chungTuBanHangApi.ts:39-94`):
`DEFAULT_SORT = 'ngayHachToan:desc,ngayChungTu:desc,soChungTu:asc'` (**BR02** của CTBH); phễu ngày =
một criterion `between` trên `ngayHachToan`; bộ lọc nâng cao qua `ADV_FILTER_WIRE` (key lạ bị **bỏ
qua**, không truyền thẳng).

**Bổ sung:** `loaiNghiepVu: { field: 'loaiNghiepVu', op: 'eq' }` vào `ADV_FILTER_WIRE`
(`:52-56`) — hệ quả trực tiếp của D2.

---

## 2. Trạng thái API — tổng hợp

| Hạng mục | Trạng thái | Hệ quả |
|---|---|---|
| `loaiNghiepVu` trên row + body | ❌ chưa có (A1) | chặn B3 → B10 |
| `/search` phân quyền theo dòng | ❌ chưa xác nhận (A2 · **Q2 v2**) | chặn B3 |
| `PUT /{id}` | ❌ chưa có **kể cả cho bán hàng hóa** (`ChungTuBanHangThemMoiModal.tsx:25-27`) | popup Sửa không nạp dữ liệu tới khi có |
| Ghi sổ / bỏ ghi sổ / hàng loạt | ❌ chưa nối **kể cả cho bán hàng hóa** (`ChungTuBanHangTab.tsx:288-301`) | [06](06-ghi-so-bo-ghi-so.md) |
| E13 bút toán | ❌ chưa có (A6) | popup D7 dựng client-side tạm |
| Cờ / danh sách hóa đơn liên kết | ❌ chưa có (A5 · **Q-BR02**) | BR02 màn Sửa không làm được |
| 4 ô định danh hóa đơn (Mẫu số · Ký hiệu · Ngày · Số HĐ) | ❌ chưa có trường trên request (nợ cũ CTBH, `ChungTuBanHangThemMoiModal.tsx:28-29`) | Tab Hóa đơn lưu thiếu |
| Danh mục Vụ việc · Hợp đồng · Đối tượng THCP · Khoản mục CP · Đơn vị · Đơn đặt hàng | ❌ chưa có endpoint (`ChungTuBanHangThemMoiModal.tsx:31`) | liên quan **C5** |
| Catalog quyền `BanDichVu.*` | ✅ **có** — `MaChucNang.java:217` | dùng ngay được |

> **Luật `mock.ts`:** chỉ tồn tại khi API chưa sẵn sàng; **còn `mock.ts` = còn nợ**
> (`docs/fe-khung-kien-truc-chuan.md:163`). Repo đang có **9** `mock.ts` — đừng thêm cái thứ 10 nếu
> chờ được BE.

---

## 3. Bảng khóa i18n

Namespace **`banHang`** (một module một namespace). Nhánh mới `banDichVu.*`. `vi` = **nguyên văn**
BA / BR.

### 3.1 Tiêu đề & tab

| Khóa | vi | en |
|---|---|---|
| `banDichVu.title.themMoi` | Thêm chứng từ bán dịch vụ | Add service sales voucher |
| `banDichVu.title.chinhSua` | Chỉnh sửa chứng từ bán dịch vụ | Edit service sales voucher |
| `banDichVu.title.xemChiTiet` | Xem chi tiết chứng từ bán dịch vụ | Service sales voucher details |
| `banDichVu.tabs.chiTietDichVu` | Chi tiết dịch vụ | Service details |

> Tiêu đề Thêm mới lấy theo **Figma v2** ("Thêm chứng từ…", không có chữ "mới") — **C15**.
> Các tab còn lại (Chứng từ ghi nợ · Phiếu thu · Giấy báo có · Hóa đơn · Thuế · Tham chiếu) **dùng lại
> khóa `banHang:themMoi.tabs.*`** đã có (`i18n/vi.ts:224`). ~~Tab Hạch toán~~ — bỏ (D7).

### 3.2 Cột lưới chi tiết (chỉ khóa THẬT SỰ khác bán hàng hóa)

| Khóa | vi | en |
|---|---|---|
| `banDichVu.grid.maDichVu` | Mã dịch vụ | Service code |
| `banDichVu.grid.tenDichVu` | Tên dịch vụ | Service name |
| `banDichVu.grid.loaiDongDichVu` | Loại dòng dịch vụ | Service line type |
| `banDichVu.grid.tongTienDichVu` | Tổng tiền dịch vụ | Total service amount |

*(Mọi cột còn lại dùng lại khóa cũ. Lưu ý **C12**: Figma vẫn ghi "Mã hàng hóa"/"Tên hàng hóa" — theo
BA, không theo Figma.)*

### 3.3 Popup "Xem dữ liệu ghi sổ" 🆕 (D7 — Figma 61661:104532)

| Khóa | vi | en |
|---|---|---|
| `banDichVu.ghiSo.title` | Xem dữ liệu ghi sổ | Ledger entries |
| `banDichVu.ghiSo.col.ngayHachToan` | Ngày hạch toán | Posting date |
| `banDichVu.ghiSo.col.ngayChungTu` | Ngày chứng từ | Voucher date |
| `banDichVu.ghiSo.col.soChungTu` | Số chứng từ | Voucher number |
| `banDichVu.ghiSo.col.maDoiTuong` | Mã đối tượng | Party code |
| `banDichVu.ghiSo.col.tenDoiTuong` | Tên đối tượng | Party name |
| `banDichVu.ghiSo.col.dienGiai` | Diễn giải | Description |
| `banDichVu.ghiSo.col.taiKhoan` | Tài khoản | Account |
| `banDichVu.ghiSo.col.taiKhoanDoiUng` | Tài khoản đối ứng | Contra account |
| `banDichVu.ghiSo.col.phatSinhNo` | Phát sinh nợ | Debit |
| `banDichVu.ghiSo.col.phatSinhCo` | Phát sinh có | Credit |
| `banDichVu.ghiSo.col.vuViec` | Vụ việc | Case |
| `banDichVu.ghiSo.col.khoanMucChiPhi` | Khoản mục chi phí | Cost item |
| `banDichVu.ghiSo.col.doiTuongTapHopChiPhi` | Đối tượng tập hợp chi phí | Cost object |
| `banDichVu.ghiSo.col.donVi` | Đơn vị | Unit |
| `banDichVu.ghiSo.tong` | Tổng: | Total: |
| `banDichVu.ghiSo.moButton` | Xem dữ liệu ghi sổ | View ledger entries |

### 3.4 Toast (Success)

| Khóa | Mã | vi | en |
|---|---|---|---|
| `banDichVu.toast.themMoi` | _001 | Thêm mới chứng từ thành công | Voucher created successfully |
| `banDichVu.toast.luuVaGhiSo` | _004 | Lưu và ghi sổ chứng từ thành công | Voucher saved and posted successfully |
| `banDichVu.toast.boGhiSo` | _009 | Bỏ ghi sổ chứng từ bán dịch vụ thành công | Service sales voucher unposted successfully |
| `banDichVu.toast.luu` | _020 | Lưu thành công | Saved successfully |
| `banDichVu.toast.capNhatVaGhiSo` | _021 | Cập nhật và ghi sổ chứng từ thành công | Voucher updated and posted successfully |
| `banDichVu.toast.xoa` | _030 | Xóa chứng từ thành công | Voucher deleted successfully |

### 3.5 Validate (Error)

| Khóa | Mã | vi | en |
|---|---|---|---|
| `banDichVu.validate.soChungTuTrung` | _006 | Số chứng từ đã tồn tại | Voucher number already exists |
| `banDichVu.validate.thieuDongChiTiet` | _007 | Phải có ít nhất 1 dòng chi tiết | At least one detail line is required |
| `banDichVu.validate.ngayHachToan` | _008 | Ngày hạch toán phải lớn hơn hoặc bằng ngày chứng từ | Posting date must be on or after the voucher date |
| `banDichVu.validate.ngayChungTuTuongLai` | _036 | Ngày chứng từ không được lớn hơn ngày hiện tại | Voucher date cannot be later than today |
| `banDichVu.validate.khachHangKhongTonTai` | _037 | Mã khách hàng không tồn tại | Customer code does not exist |
| `banDichVu.validate.dichVuKhongTonTai` | _038 | Mã dịch vụ [{{maDichVu}}] không tồn tại | Service code [{{maDichVu}}] does not exist |
| `banDichVu.validate.soLuongAm` | _040 | Số lượng không được âm | Quantity cannot be negative |
| `banDichVu.validate.donGiaAm` | _041 | Đơn giá không được âm | Unit price cannot be negative |
| `banDichVu.validate.ckVuot100` | _043 | % Chiết khấu không được vượt quá 100% | Discount percentage cannot exceed 100% |
| `banDichVu.validate.tienCkVuotThanhTien` | _044 | Tiền CK không được vượt quá thành tiền của dòng | Discount amount cannot exceed the line amount |
| `banDichVu.validate.tongCkKhongKhop` | _046 | Tổng tiền chiết khấu các dòng không khớp với tổng tiền chiết khấu của chứng từ | Sum of line discounts does not match the voucher discount |
| `banDichVu.validate.phanBoKhac100` | _048 | Tổng tỷ lệ phân bổ phải bằng 100% | Total allocation ratio must equal 100% |
| `banDichVu.validate.taiKhoanKhongCapCuoi` | _055 | Tài khoản {{tenTK}} không phải là tài khoản cấp cuối. Vui lòng chọn tài khoản chi tiết. | Account {{tenTK}} is not a leaf account. Please select a detail account. |
| `banDichVu.validate.vuotSoLuongHoaDon` | _102 | Số lượng lập hóa đơn [{{soLuongMoi}}] vượt quá số lượng còn lại được phép xuất [{{soLuongConLai}}] trên Chứng từ bán dịch vụ gốc. | Invoiced quantity [{{soLuongMoi}}] exceeds the remaining issuable quantity [{{soLuongConLai}}] on the original service sales voucher. |
| `banDichVu.validate.vuotSoLuongDonHang` | _104 | Số lượng nhập vào lớn hơn số lượng còn lại của Đơn đặt hàng nguồn | Entered quantity exceeds the remaining quantity of the source sales order |

### 3.6 Ghi sổ / Bỏ ghi sổ / Xóa (Error · Warning · Confirm)

| Khóa | Mã | vi | en |
|---|---|---|---|
| `banDichVu.error.ghiSo` | _015 | Lỗi khi ghi sổ chứng từ | Failed to post the voucher |
| `banDichVu.error.daGhiSo` | _016 | Không thể ghi sổ chứng từ đã ghi sổ | Cannot post an already posted voucher |
| `banDichVu.error.boGhiSo` | _017 | Lỗi khi bỏ ghi sổ chứng từ | Failed to unpost the voucher |
| `banDichVu.error.chuaGhiSo` | _023 | Không thể bỏ ghi sổ chứng từ chưa ghi sổ | Cannot unpost a voucher that has not been posted |
| `banDichVu.error.thuTienSauCoPhieuThu` | _010 | Chứng từ "Thu tiền sau" đã có phiếu thu riêng tham chiếu, không được bỏ ghi sổ | A deferred-payment voucher referenced by a separate receipt cannot be unposted |
| `banDichVu.error.daSuDung` | _014 | Chứng từ đã được sử dụng, không thể xóa | The voucher is already in use and cannot be deleted |
| `banDichVu.error.daGhiSoKhongXoa` | _031 | Chứng từ đã ghi sổ, không thể xóa | A posted voucher cannot be deleted |
| `banDichVu.error.daPhatHanhHoaDon` | _032 | Chứng từ đã phát hành hóa đơn, không thể xóa | A voucher with an issued invoice cannot be deleted |
| `banDichVu.error.xoaThatBai` | _033 | Xóa chứng từ thất bại | Failed to delete the voucher |
| `banDichVu.error.khongCoQuyen` | _011 | Không có quyền truy cập | You do not have access permission |
| `banDichVu.error.khongTonTai` | _012 | Chứng từ không tồn tại | The voucher does not exist |
| `banDichVu.error.heThong` | _013 | Lỗi hệ thống | System error |
| `banDichVu.warning.dangDuocSua` | _105 | Chứng từ đang được người khác chỉnh sửa. Vui lòng thử lại sau | The voucher is being edited by another user. Please try again later |
| `banDichVu.warning.coChungTuDaGhiSo` | _106 | Có {{n}} chứng từ đã ghi sổ trong số chứng từ được chọn | {{n}} of the selected vouchers have already been posted |
| `banDichVu.confirm.xoa.content` | _027 | Bạn có chắc chắn muốn xóa chứng từ bán dịch vụ này không? | Are you sure you want to delete this service sales voucher? |
| `banDichVu.confirm.xoa.title` | — | Xác nhận xóa chứng từ bán dịch vụ | Confirm voucher deletion |
| `banDichVu.hangLoat.ketQuaXoa` | _054 | Xóa thành công {{x}}/{{n}} chứng từ. {{y}} chứng từ đã ghi sổ không được xóa. | Deleted {{x}} of {{n}} vouchers. {{y}} posted vouchers were skipped. |

### 3.7 Popup kết quả hàng loạt (BR45.3)

| Khóa | vi | en |
|---|---|---|
| `banDichVu.hangLoat.title.ghiSo` | Thông báo kết quả Ghi sổ | Posting result |
| `banDichVu.hangLoat.title.boGhiSo` | Thông báo kết quả Bỏ ghi sổ | Unposting result |
| `banDichVu.hangLoat.title.xoa` | Thông báo kết quả Xóa | Deletion result |
| `banDichVu.hangLoat.tongKet` | Thực hiện thành công {{x}}/{{n}} chứng từ. Thất bại {{y}} chứng từ. | Completed {{x}} of {{n}} vouchers. {{y}} failed. |
| `banDichVu.hangLoat.thanhCong.ghiSo` | Đã ghi sổ thành công {{x}} chứng từ. | Successfully posted {{x}} vouchers. |
| `banDichVu.hangLoat.thanhCong.boGhiSo` | Đã bỏ ghi sổ thành công {{x}} chứng từ. | Successfully unposted {{x}} vouchers. |
| `banDichVu.hangLoat.thanhCong.xoa` | Đã xóa thành công {{x}} chứng từ. | Successfully deleted {{x}} vouchers. |
| `banDichVu.hangLoat.col.soChungTu` | Số chứng từ | Voucher number |
| `banDichVu.hangLoat.col.ngayChungTu` | Ngày chứng từ | Voucher date |
| `banDichVu.hangLoat.col.nguyenNhan` | Nguyên nhân | Reason |

> **Đổi so với v1:** v1 dùng một khóa với nội suy `{{thaoTac}}` — bản tiếng Anh ghép động từ đọc
> gượng. v2 **tách thành 3 khóa riêng** cho 3 thao tác, đúng luật "không cộng chuỗi" mà vẫn tự nhiên
> ở cả hai ngôn ngữ.

### 3.8 Confirm ghi sổ / bỏ ghi sổ

| Khóa | vi | en |
|---|---|---|
| `banDichVu.confirm.ghiSo.title` | Xác nhận ghi sổ | Confirm posting |
| `banDichVu.confirm.ghiSo.content` | Bạn có chắc chắn muốn ghi sổ chứng từ này không? | Are you sure you want to post this voucher? |
| `banDichVu.confirm.boGhiSo.title` | Xác nhận bỏ ghi sổ | Confirm unposting |
| `banDichVu.confirm.boGhiSo.content` | Bạn có chắc chắn muốn bỏ ghi sổ chứng từ này không? | Are you sure you want to unpost this voucher? |

*(4 khóa này **không** có trong `6.messages.md` — chữ do FE đặt theo BR3. Cần BA duyệt.)*

**Ngoại lệ i18n có chủ đích:** template Diễn giải theo BR01 (`"bán dịch vụ {TenKhachHang} theo hóa
đơn số {SoHoaDon}"`) là **dữ liệu chứng từ pháp định tiếng Việt**, không phải chuỗi UI ⇒ **hằng số**
ở `helpers/dongBo.ts`, không vào `vi.ts`/`en.ts` (`client/CLAUDE.md:381-383`).

---

## 4. Hằng số nghiệp vụ (`constants/constants.ts`)

```ts
/**
 * BR24 — `ChungTuBan.LoaiNghiepVu` có ĐÚNG 3 giá trị. Hằng hiện tại (constants.ts:20) mới có 2;
 * phiếu này bổ sung `banDichVu`. Đây là trục phân biệt duy nhất giữa hai luồng nghiệp vụ trên cùng
 * một entity — KHÔNG tách entity, KHÔNG tách endpoint.
 */
export const LOAI_NGHIEP_VU = {
  trongNuoc: 'Bán hàng trong nước',
  xuatKhau:  'Bán hàng xuất khẩu',
  banDichVu: 'Bán dịch vụ',          // 🆕
} as const

/** Giá trị được phép chọn trên combo, theo màn khởi tạo (BR24). Màn bán hàng ẨN `Bán dịch vụ`;
 *  màn bán dịch vụ cố định `Bán dịch vụ` và ẩn hẳn ô chọn. */
export const LOAI_NGHIEP_VU_THEO_MAN = {
  chungTuBanHang:   [LOAI_NGHIEP_VU.trongNuoc, LOAI_NGHIEP_VU.xuatKhau],
  chungTuBanDichVu: [LOAI_NGHIEP_VU.banDichVu],
} as const

/** Loại vật tư được phép chọn ở lưới chi tiết dịch vụ (BR02). */
export const LOAI_VAT_TU_CHO_BAN_DICH_VU = LOAI_VAT_TU_DICH_VU   // 'Dịch vụ' — constants.ts:80
```

⚠ **Cảnh báo hồi quy:** mở `LOAI_NGHIEP_VU` chạm trực tiếp `test/anHienVaDongBo.test.ts` —
xem [00 §13](00-ke-hoach-tong.md) điều kiện 6.

Dùng lại **nguyên** các hằng đã có, **không** khai trùng: `HINH_THUC_THANH_TOAN:29` ·
`HINH_THUC_TT_HOA_DON:35` · `LOAI_CHIET_KHAU:42` · `THUE_SUAT:51` · `MA_TIEN_HACH_TOAN_MAC_DINH:83` ·
`TAB_CHUNG_TU:96` · `TAB_CHI_TIET:105` · `CHI_TIET_NAME:113` · `CHI_TIET_PAGE_SIZE:116` ·
`DATE_FORMAT:122` · `WIRE_DATE_FORMAT:125` · `MAX_LEN:170` · `SAI_SO_PHAN_BO:167` ·
`GIA_TRI_THUE_GTGT:160` · `PHAN_TRAM_MAX:155` · `TOTALS_WIDTH:149`.

**Không** dùng cho biến thể dịch vụ: `THUE_SUAT_XUAT_KHAU:68` — dịch vụ xử lý thuế **giống Bán hàng
trong nước** (BR24 · **BR13**), không có nghiệp vụ xuất khẩu.
`TAB_CHI_TIET:105` phải **bỏ mục Hạch toán** cho biến thể dịch vụ (D7).

---

## 5. Mã quyền (`constants/permissions.ts` — BR25)

```ts
/**
 * Mã THẬT của backend — `MaChucNang.BAN_DICH_VU = "BanDichVu"`
 * (cell-app/.../common/constant/MaChucNang.java:217; chú thích liệt kê đúng 7 hành động dưới đây).
 * Gỡ OPEN ITEM ở đầu file này về `CTBanDichVu.Create` — mã đã tồn tại, không còn phải đoán.
 *
 * LƯU Ý: một entity `ChungTuBan` nhưng HAI mã chức năng. Quyền chọn theo `row.loaiNghiepVu`
 * (helpers/quyen.ts), và BE phải gate tương ứng trên cùng một endpoint — xem §1.3 A2/A3.
 */
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

Hai mã **không** thuộc bộ này (thao tác rời khỏi module): lập hóa đơn (`LapHoaDonBan.*` —
`MaChucNang.java` khai `LAP_HOA_DON_BAN`) và thu tiền (`ThuTien.Create` / `ThuTienTG.Create`).
⚠ BA v2 đã **bỏ nhắc mã cụ thể** ở `SCR_CTBH_DanhSach.md` (chỉ ghi "có quyền chức năng") — giữ
nguyên hiện trạng `BAN_HANG_CHUNG_TU_PERM.lapHoaDon` / `.thuTien` cho tới khi module đích dựng.

---

## 6. Đường dẫn (`constants/paths.ts`)

**Không thêm path.** CTBDV dùng chung `BAN_HANG_PATHS.chungTuBanHang = '/ban-hang/chung-tu-ban-hang'`
(`constants/paths.ts:9-11`). BA v2 xác nhận: *"Chứng từ bán dịch vụ **không có màn danh sách riêng**"*
(`SCR_CTbanDichVu_DanhSach.md` BR06).

Quy ước deep-import **cố ý** giữ nguyên — `routes.tsx` và `app/layouts/shell/*` import thẳng
`constants/paths.ts` + `constants/permissions.ts`, **không** qua `index.ts`
(`client/CLAUDE.md:336-344`).

> ⚠ **Q3** ([00 §6](00-ke-hoach-tong.md)) vẫn treo: `handle.perm` là `PermissionKey` **đơn**
> (`routes.tsx:19-20`), nên người chỉ có `BanDichVu.View` không vào được màn. Đây là câu hỏi **về
> route**, không phải về resource — D2 không giải quyết được nó.
