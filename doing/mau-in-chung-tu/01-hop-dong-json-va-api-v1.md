# Hợp đồng kỹ thuật v1 — Mẫu in chứng từ theo khối (`MauInChungTu`)

> **Trạng thái:** BẢN NHÁP CHỜ CHỐT — đi kèm [00-plan-tong-the.md](00-plan-tong-the.md) §14 (câu hỏi Q1…Q17).
> **Ngày:** 2026-09-17. **Nguồn yêu cầu:** `ThietLapMauIn.html` (mock 540 dòng) + 5 bổ sung của user.
> **Dùng chung cho 4 codebase:** `cell-app` · `client` · `super-admin-service` · `client-admin`. Đây là
> nguồn sự thật DUY NHẤT cho schema JSON, catalog, API, luật kiểm tra — không tầng nào tự diễn giải lại.

---

## 0. Quy ước chung

| # | Quy ước | Ghi chú |
|---|---|---|
| 1 | Khoá JSON camelCase tiếng Việt không dấu, giống DTO hiện có (`soChungTu`, `ngayChungTu`) | khớp `ColumnDef.key` / alias `@Searchable` |
| 2 | **Nhãn in là DỮ LIỆU tiếng Việt**, không phải chuỗi i18n | ngoại lệ đã ghi ở `client/CLAUDE.md §8`: bản in tiếng Anh vẫn in tiếng Việt đúng luật |
| 3 | Đơn vị đo: lề **cm** (0–5, bước 0,25) · cỡ chữ **pt** · độ rộng cột **%** (tổng 100 sau chuẩn hoá) | giữ nguyên mock |
| 4 | `schemaVersion` nguyên dương; đổi shape không tương thích ⇒ tăng số và cả BE lẫn FE phải có `nangCap(v → v+1)` | lưu JSON là lưu hợp đồng — không có bước nâng cấp thì bản ghi cũ chết lặng |
| 5 | **Mã loại chứng từ = `mst_loai_chung_tu.code`** (`PT · PC · GBC · PCTG · CTNB · BH · MDV · TLHM…`) | nguồn đối chiếu là migration (`V1032` cho thu/chi), **không** phải `db/seed/20_loai_chung_tu.sql` (lạc hậu) và **không** phải enum `quan_he_chung_tu.api.LoaiChungTu` (bộ mã khác mục đích) |
| 6 | Mọi giá trị BE trả trong `DuLieuIn` là **giá trị thô có kiểu** (`string` · `number` · `null`); FE định dạng theo runtime của tenant (`@domain-kit/dinhDangSo`, BR7/BR8). Riêng **số tiền bằng chữ** BE tính sẵn (`SoTienBangChu.java`) | tránh hai bộ luật làm tròn; chữ số→chữ chỉ có một chỗ đúng |
| 7 | Mã luật `R-MAUIN-nnn`, bất biến `INV-MAUIN-nnn`, message `MSG_MAUIN_nnn` (**tạm** — đổi sang `MSG_PMKT-E-xxxxx_nnn` khi BA cấp mã epic, xem Q11) | để `trace.sh` đếm được |

---

## 1. Schema `MauInChungTu` v1

Zod ở FE (`@domain-kit/mauIn/api/mauInSchema.ts`), record Jackson ở BE (`mau_in.internal.model.json.*` và bản
sao ở `super-admin-service`). Hai bên cùng chạy một bộ fixture (§10).

```ts
type MauInChungTu = {
  schemaVersion: 1
  maLoaiChungTu: string                       // 'MDV' — phải khớp catalog
  trang: Trang
  khoi: Khoi[]                                // THỨ TỰ MẢNG = THỨ TỰ IN, trên xuống dưới
}

type Trang = {
  kho: 'A4' | 'A5'
  huong: 'DOC' | 'NGANG'
  le: { tren: number; duoi: number; trai: number; phai: number }   // cm, 0–5   (R-MAUIN-010)
  font: string                                // ∈ FONT_CHO_PHEP (§5.3)
  coChu: number                               // pt, 8–20                        (R-MAUIN-011)
  mauChu: string                              // '#rrggbb'                       (R-MAUIN-012)
  logo: { hien: boolean; viTri: 'TRAI' | 'GIUA' | 'PHAI'; co: 'S' | 'M' | 'L' }   // Q7: v1 chỉ lưu, chưa render ảnh
  nen: { kieu: 'KHONG' | 'KHUNG_VIEN' | 'ANH'; doDam: number; phu: 'GIUA' | 'TOAN_TRANG'; anhId?: string }
  chanTrang: { soTrang: boolean; ghiChu: string }
}

/* ---- Khối ------------------------------------------------------------------------------- */
type KhoiChung = {
  id: string                                  // ổn định, duy nhất trong mẫu; khối chuẩn dùng id cố định
  loai: LoaiKhoi
  ten: string                                 // tên trong outline / tag chọn
  hien: boolean
  khoa?: { viTri: boolean; xoa: boolean }     // DON_VI & TIEU_DE: {viTri:true, xoa:true}  (R-MAUIN-020/021)
}
type LoaiKhoi = 'DON_VI' | 'TIEU_DE' | 'THONG_TIN' | 'BANG' | 'TONG_HOP' | 'CHU_KY' | 'TU_DO'

type KhoiDonVi = KhoiChung & {
  loai: 'DON_VI'
  can: 'TRAI' | 'GIUA'
  dong: { k: 'ten' | 'diaChi' | 'mst' | 'dienThoai' | 'email'; nhan: string; hien: boolean; dam?: boolean }[]
}
type KhoiTieuDe = KhoiChung & {
  loai: 'TIEU_DE'
  noiDung: string                             // 1–80 ký tự, không rỗng khi hien   (R-MAUIN-013)
  coChu: number                               // 10–36 pt
  inHoa: boolean; dam: boolean
  can: 'TRAI' | 'GIUA' | 'PHAI'
  dongSoNgay: boolean                         // "Số: … — Ngày …" ngay dưới tiêu đề
}

/** Bố cục dạng BẢNG cho khối trường (yêu cầu bổ sung #2). */
type BoCucBang = {
  soCot: 1 | 2 | 3 | 4                        // số cặp nhãn:giá trị trên một hàng
  keO: 'KHONG' | 'DAY_DU' | 'NGANG'
  rongNhan: number                            // % bề ngang một ô dành cho nhãn, 15–60
}
type TruongIn = {
  k?: string                                  // khoá catalog; vắng ⇒ dòng tự do
  nhan: string
  hien: boolean
  span: number                                // 1..soCot — số ô chiếm trên hàng (thay 'half'/'full' của mock)
  dam?: boolean; nghieng?: boolean
  tuDo?: { noiDung: string }                  // chỉ khi !k: nội dung cố định / "………" ghi tay
}
type KhoiThongTin = KhoiChung & { loai: 'THONG_TIN'; boCuc: BoCucBang; truong: TruongIn[] }

type KhoiBang = KhoiChung & {
  loai: 'BANG'
  nguon: string                               // khoá bảng trong catalog ('hachToan', 'thue'…) — mỗi nguồn ĐÚNG MỘT khối (Q16)
  tieuDe: { noiDung: string; hien: boolean; dam: boolean; can: 'TRAI' | 'GIUA' | 'PHAI' }   // yêu cầu bổ sung #1
  stt: boolean
  dongCong: boolean
  lapTieuDeCot: boolean                       // <thead> lặp khi sang trang
  keO: 'DAY_DU' | 'NGANG' | 'KHONG'
  cot: CotIn[]
}
type CotIn = { k: string; nhan: string; hien: boolean; rong: number; can: 'TRAI' | 'GIUA' | 'PHAI'; cong?: boolean }

type KhoiTongHop = KhoiChung & {
  loai: 'TONG_HOP'
  can: 'TRAI' | 'PHAI'
  truong: { k: string; nhan: string; hien: boolean; dam?: boolean; nghieng?: boolean }[]
}

type VaiTroKy = 'GIAM_DOC' | 'KE_TOAN_TRUONG' | 'THU_KHO' | 'THU_QUY' | 'NGUOI_LAP'   // = 5 người ký ở Thông tin công ty
type OKy = {
  vaiTro?: VaiTroKy                           // vắng ⇒ ô ký tự do
  tieuDe?: string                             // ghi đè tiêu đề lấy từ Thông tin công ty
  ghiChu: string                              // "(Ký, họ tên)" / "(Ký, họ tên, đóng dấu)"
  hien: boolean
  tuDo?: { tieuDe: string; ten: string }
}
type KhoiChuKy = KhoiChung & {
  loai: 'CHU_KY'
  dongNgay: boolean                           // "Ngày … tháng … năm …"
  inTen: boolean                              // mặc định = Tenant.inTenNguoiKyTrenChungTu
  chieuCao: 'S' | 'M' | 'L'
  o: OKy[]                                    // tối đa 4 ô hien = true   (R-MAUIN-016)
}

type KhoiTuDo = KhoiChung & { loai: 'TU_DO'; inTen: boolean; boCuc: BoCucBang; truong: TruongIn[] }

type Khoi = KhoiDonVi | KhoiTieuDe | KhoiThongTin | KhoiBang | KhoiTongHop | KhoiChuKy | KhoiTuDo
```

**Bất biến cấu trúc** (validator hai bên cùng ném cùng mã):

| ID | Bất biến |
|---|---|
| INV-MAUIN-001 | `khoi[0].loai === 'DON_VI'` và `khoi[1].loai === 'TIEU_DE'`; mỗi loại đúng một khối; cả hai `khoa = {viTri:true, xoa:true}` |
| INV-MAUIN-002 | Đúng một `THONG_TIN`, một `TONG_HOP`, một `CHU_KY` (khối chuẩn — ẩn được, không xoá được) |
| INV-MAUIN-003 | `id` khối duy nhất; `nguon` của `BANG` duy nhất và tồn tại trong catalog |
| INV-MAUIN-004 | Mọi `k` (trường, cột, tổng hợp) tồn tại trong catalog của `maLoaiChungTu`; `k` lạ bị loại ở bước hợp nhất, không lỗi |
| INV-MAUIN-005 | `span ∈ [1, boCuc.soCot]`; `rong ∈ [3, 90]`; sau chuẩn hoá Σ`rong` cột `hien` = 100 (±0,5) |

---

## 2. Catalog `MoTaMauIn` — do `MauInProvider` của từng loại chứng từ khai (cell-app)

```ts
type MoTaMauIn = {
  maLoaiChungTu: string; ten: string; nhom: string            // nhom: 'Mua hàng' | 'Bán hàng' | 'Ngân quỹ' | 'Kho' …
  maChucNang: string                                          // 'MuaDichVu' → kiểm <maChucNang>.Print / .View
  basePath: string                                            // '/api/mua-hang/chung-tu-mua-dich-vu' — FE gọi mẫu cố định
  truong: TruongCatalog[]                                     // ô phần đầu form (không gồm cột bảng)
  bang: BangCatalog[]                                         // "danh sách các bảng chi tiết để chọn theo từng loại"
  tongHop: TruongCatalog[]                                    // ô tổng cuối form + soTienBangChu
  vaiTroKy: VaiTroKy[]                                        // vai trò ký hợp lệ của loại này
  macDinh: {                                                  // gợi ý dựng MẪU CHUẨN ĐÓNG GÓI
    tieuDe: string                                            // 'Chứng từ mua dịch vụ'
    thongTin: { k: string; span?: number }[]                  // thứ tự + trường hiện mặc định
    bang: { nguon: string; hien: boolean; cot: { k: string; rong: number; cong?: boolean }[] }[]
    tongHop: string[]; chuKy: { vaiTro: VaiTroKy; hien: boolean; ghiChu: string }[]
  }
}
type TruongCatalog = { k: string; nhan: string; kieu: 'CHUOI' | 'SO' | 'TIEN' | 'NGAY' | 'LOGIC'; nhom?: string }
type BangCatalog   = { k: string; ten: string; cot: (TruongCatalog & { can?: 'TRAI' | 'GIUA' | 'PHAI'; congDuoc?: boolean })[] }
```

`mau_in.internal.service.business.MauChuanBuilder` dựng `MauInChungTu` chuẩn từ `MoTaMauIn.macDinh` — **một chỗ
dựng** cho cả 47 loại; provider chỉ mô tả, không tự viết JSON tay.

**Snapshot cho super-admin-service:** `cell-app` xuất `build/mau-in/catalog.json` =
`{ catalogVersion, sinhLuc, loai: [{ moTa, mauChuan, duLieuMau }] }` (Gradle task `xuatCatalogMauIn` chạy test
`@Tag("unit")` `XuatCatalogMauInTest`); script `tools/sync-catalog.sh` chép sang
`super-admin-service/src/main/resources/mau-in/catalog.json`. Xem Q3.

---

## 3. Dữ liệu in `DuLieuIn`

```ts
type DuLieuIn = {
  donVi: { ten: string; diaChi: string; mst: string; dienThoai: string; email: string }   // mst_don_vi cấp GỐC (như ToChucInDto)
  truong: Record<string, string | number | null>                                          // theo TruongCatalog.k
  bang: Record<string, { dong: Record<string, string | number | null>[]; tong: Record<string, number> }>
  tongHop: Record<string, string | number | null>                                         // gồm soTienBangChu (string)
  nguoiKy: Record<VaiTroKy, { tieuDe: string; ten: string }>                              // đã áp layTenNguoiLapPhieuTuNguoiDungDangNhap
  kieu: Record<string, TruongCatalog['kieu']>                                             // gộp kiểu của mọi khoá để FE định dạng
}
```

Provider **tự kẹp phạm vi** khi nạp chứng từ thật (đi qua đúng `service().layChiTiet(id)` của module đó — cùng
nguyên tắc `InPhieuThuChiService`: không có đường thứ hai nạp chứng từ để có thể quên kẹp tenant/quyền).

---

## 4. Hợp nhất `hopNhat(mau, catalog) → mau'` — thuần, tất định, cùng fixture hai bên

1. **Loại** trường/cột/tổng hợp có `k` không còn trong catalog (giữ dòng `tuDo`).
2. **Thêm** trường catalog chưa xuất hiện ở bất kỳ `THONG_TIN`/`TU_DO` nào → cuối khối `THONG_TIN`, `span = 1`,
   `hien` theo Q6 (mock: **hiện**; đề nghị: hiện với mẫu hệ thống, **ẩn + cờ `moi: true`** với mẫu tuỳ chỉnh của
   đơn vị).
3. **Thêm** cột catalog chưa có trong khối `BANG` tương ứng → cuối bảng, `rong` = trung bình cột đang hiện, `hien` như bước 2.
4. **Thêm** bảng catalog chưa có khối → khối `BANG` mới ngay trước `CHU_KY`, `hien: false`, cột theo `macDinh`.
5. **Đồng bộ** `DON_VI.dong` về đúng 5 khoá cố định; `CHU_KY.o` bỏ vai trò không thuộc `vaiTroKy`.
6. Không đổi thứ tự bất kỳ phần tử nào đang có. Kết quả đi qua `chuanHoa()` (§5.2) trước khi trả.

Đầu ra kèm `thayDoi: { themTruong: string[]; themCot: Record<string,string[]>; boTruong: string[] }` để FE hiện
thông báo "Có N trường mới".

---

## 5. Luật kiểm tra & chuẩn hoá

### 5.1 Kiểm tra (`kiemTraMau(mau, catalog) → { loi[], canhBao[] }`) — chạy ở FE (panel "Kiểm tra trước khi lưu") và BE (400 nếu còn `loi`)

| ID | Mức | Điều kiện | Message (nguyên văn mock / BR) | Mã |
|---|---|---|---|---|
| R-MAUIN-010 | LỖI | lề ∉ [0, 5] | `Lề {viTri} phải từ 0 đến 5 cm.` | MSG_MAUIN_001 |
| R-MAUIN-011 | LỖI | `coChu` ∉ [8, 20] | `Cỡ chữ cơ sở phải từ 8 đến 20.` | MSG_MAUIN_002 |
| R-MAUIN-012 | LỖI | `mauChu` không khớp `^#[0-9a-f]{6}$` | `Mã màu phải dạng #rrggbb.` | MSG_MAUIN_014 |
| R-MAUIN-013 | LỖI | `TIEU_DE.hien && noiDung.trim() === ''` | `Tiêu đề bản in đang trống.` | MSG_MAUIN_003 |
| R-MAUIN-014 | CẢNH BÁO | bảng `hien` có Σ`rong` cột hiện ≠ 100 (±0,5) | `{tenBang}: tổng độ rộng cột đang {tong}% (nên = 100%). Khi lưu sẽ tự chia lại theo tỷ lệ.` | MSG_MAUIN_004 |
| R-MAUIN-015 | LỖI | bảng `hien` không có cột nào `hien` | `{tenBang} chưa có cột nào.` | MSG_MAUIN_005 |
| R-MAUIN-016 | LỖI | `CHU_KY` có > 4 ô `hien` | `Tối đa 4 ô ký trên một hàng.` | MSG_MAUIN_012 |
| R-MAUIN-017 | CẢNH BÁO | không có khối `BANG` nào `hien` | `Bản in không có bảng chi tiết nào.` | MSG_MAUIN_006 |
| R-MAUIN-018 | CẢNH BÁO | `CHU_KY.hien` và không ô nào `hien` | `Khối chữ ký đang bật nhưng không có ô ký nào.` | MSG_MAUIN_007 |
| R-MAUIN-019 | CẢNH BÁO | khối `TU_DO` `hien` không có dòng `hien` | `"{tenKhoi}" đang bật nhưng chưa có dòng nào.` | MSG_MAUIN_008 |
| R-MAUIN-020 | LỖI | khối `TU_DO` có `ten.trim() === ''` | `Khối tự do chưa có tên.` | MSG_MAUIN_009 |
| R-MAUIN-021 | CẢNH BÁO | `nen.kieu !== 'KHONG' && doDam > 60` | `Hình nền đậm quá 60% có thể che chữ khi in.` | MSG_MAUIN_010 |
| R-MAUIN-022 | CẢNH BÁO | không trường nào `k === 'soChungTu'` đang `hien` | `Bản in không hiện Số chứng từ.` | MSG_MAUIN_011 |
| R-MAUIN-023 | LỖI | `THONG_TIN.hien` mà mọi trường đều ẩn (BR30) | `Phải giữ lại ít nhất 1 trường hiển thị.` | MSG_MAUIN_013 |
| R-MAUIN-024 | LỖI | vi phạm INV-MAUIN-001…005 (chỉ xảy ra khi JSON bị sửa tay / lỗi client) | `Mẫu in không hợp lệ: {chiTiet}` | MSG_MAUIN_017 |
| R-MAUIN-025 | LỖI | `TIEU_DE.coChu` ∉ [10, 36] · `rongNhan` ∉ [15, 60] · `rong` ∉ [3, 90] | như MSG_MAUIN_017, `chiTiet` = đường dẫn JSON Pointer | MSG_MAUIN_017 |

### 5.2 Chuẩn hoá trước khi lưu (`chuanHoa(mau)`) — BE luôn chạy, FE chạy để hiển thị trước

- Trim mọi chuỗi (BR43); cột `hien` của mỗi bảng chia lại về Σ = 100 theo tỷ lệ, dồn sai số vào cột cuối
  (đúng thuật toán `data-tnorm` của mock); `mauChu` về chữ thường; bỏ `tuDo` khi có `k` và ngược lại.

### 5.3 Hằng số dùng chung (`constants.ts` ↔ `GioiHanMauIn.java`)

`FONT_CHO_PHEP = ['Times New Roman','Arial','Tahoma','Cambria','Open Sans','Arial Narrow']` ·
`MAU_CHU_GOI_Y` (10 mã như mock) · `LE = {min:0,max:5,buoc:0.25}` · `CO_CHU = {min:8,max:20}` ·
`CO_TIEU_DE = {min:10,max:36}` · `RONG_COT = {min:3,max:90}` · `O_KY_TOI_DA = 4` · `UNDO_TOI_DA = 60` ·
`ZOOM = {min:0.4,max:1.6,buoc:0.1}` · `KHO = {A4:[794,1123], A5:[559,794]}` px @96dpi · `CM_PX = 37.8`.

---

## 6. API `cell-app` — module `mau_in`, prefix `/api/mau-in`

| # | Method · Path | Quyền | Vào | Ra (`ApiResponse<T>`) |
|---|---|---|---|---|
| A1 | `GET /api/mau-in/loai-chung-tu` | `HTMauIn.View` | — | `LoaiChungTuMauInDto[]` — 47 dòng từ `mst_loai_chung_tu` ⟕ registry provider: `{ ma, ten, nhom, hoTro, trangThai: 'MAU_CHUAN'\|'TUY_CHINH', phienBan, nguonMacDinh, macDinhPhienBan, coMacDinhMoi, ngayCapNhat, nguoiCapNhat }` |
| A2 | `GET /api/mau-in/{ma}` | `HTMauIn.View` | — | `{ hieuLuc: MauInChungTu, nguon: 'TUY_CHINH'\|'MAC_DINH_HE_THONG'\|'MAC_DINH_DONG_GOI', phienBan, macDinh: { mau: MauInChungTu, nguon, phienBan }, catalog: MoTaMauIn, duLieuMau: DuLieuIn, thayDoi }` |
| A3 | `PUT /api/mau-in/{ma}` | `HTMauIn.Edit` | `{ mau: MauInChungTu, phienBan: number\|null }` | `{ phienBan }` · 400 `MSG_MAUIN_017` · 409 `MSG_MAUIN_018` (khoá lạc quan) · 404 `MSG_MAUIN_019` (loại chưa có provider) |
| A4 | `DELETE /api/mau-in/{ma}` | `HTMauIn.Edit` | — | xoá mềm bản tuỳ chỉnh → quay về mặc định; trả như A2 |
| A5 | `GET /api/mau-in/{ma}/chung-tu-gan-day?q=&gioiHan=20` | `HTMauIn.View` **và** `<maChucNang>.View` | — | `ChungTuTomTat[]` `{ id, soChungTu, ngayChungTu, dienGiai, tongTien }` — để "Chứng từ khác…" trong editor (Q9) |
| A6 | `GET /api/mau-in/{ma}/chung-tu/{id}/du-lieu-in` | `<maChucNang>.Print` | — | `{ mau: MauInChungTu (hiệu lực), duLieu: DuLieuIn, catalog }` — dùng cho cả xem trước bằng chứng từ thật lẫn **in mẫu tuỳ chỉnh** |
| A7 | `GET /api/mau-in/{ma}/menu?chungTuId=` | `<maChucNang>.Print` | — | `MucMenuIn[]` `{ ma, ten, loai: 'CO_DINH'\|'TUY_CHINH' }` — `CO_DINH` lấy từ `provider.mauCoDinh(id)` (thu/chi ⇒ `MauInPhieuThuChi.choPhieu`), `TUY_CHINH` luôn có; FE in `CO_DINH` qua endpoint `/in` sẵn có của module đó |
| A8 | `GET /api/mau-in/{ma}/lich-su` | `HTMauIn.View` | — | `MauInLichSuDto[]` `{ id, phienBan, hanhDong: 'LUU'|'XOA', ghiChu, nguoiTao, ngayTao }` — tối đa 50, `ngayTao` giảm dần, KHÔNG kèm mẫu (R-MAUIN-102) |
| A9 | `GET /api/mau-in/{ma}/lich-su/{id}` | `HTMauIn.View` | — | `MauInLichSuChiTietDto` = A8 + `mau` đã `hopNhat(catalog hiện tại)` + `chuanHoa` (R-MAUIN-103); id lạ ⇒ 404 `MSG_MAUIN_024` |

Giai đoạn 2 (Q1): `GET /api/mau-in/{ma}/chung-tu/{id}/in.pdf` — BE kết xuất PDF từ cùng JSON + `DuLieuIn`.

Không đụng `BaseChungTuController` — tránh trùng mapping với `BaseChungTuThuChiController#/{id}/mau-in` và tránh
`accounting_core` (kernel) phụ thuộc module ngoại vi.

---

## 7. API `super-admin-service` — module `quan_tri/mau_in`, prefix `/api/admin/mau-in`

| # | Method · Path | Quyền | Ghi chú |
|---|---|---|---|
| B1 | `GET /api/admin/mau-in` | `MauInMacDinh.View` | 47 dòng từ `catalog.json` ⟕ `sa_mau_in_mac_dinh`: `{ ma, ten, nhom, trangThai: 'DONG_GOI'\|'SUPER_ADMIN', phienBan, ngayCapNhat, nguoiCapNhat, catalogVersion }` |
| B2 | `GET /api/admin/mau-in/{ma}` | `MauInMacDinh.View.Detail` | `{ hieuLuc, nguon, phienBan, macDinh: { mau (đóng gói) }, catalog, duLieuMau, thayDoi }` |
| B3 | `PUT /api/admin/mau-in/{ma}` | `MauInMacDinh.Edit` | `{ mau, phienBan }` → kiểm §5 với catalog snapshot, `phienBan++`; 400/409 như A3 |
| B4 | `DELETE /api/admin/mau-in/{ma}` | `MauInMacDinh.Delete` | xoá mềm → cell rơi về mẫu đóng gói |
| B5 | `GET /internal/mau-in/mac-dinh/{ma}` | header `X-Internal-Token` (ROLE_INTERNAL) | `ETag: "<phienBan>"`, hỗ trợ `If-None-Match` → 304; 404 khi không có bản super admin (cell dùng đóng gói) |
| B6 | `GET /internal/mau-in/mac-dinh` | như B5 | `{ catalogVersion, items: [{ ma, phienBan, ngayCapNhat }] }` — cell làm mới hàng loạt / kiểm "có bản mới" |
| B7 | `GET /api/admin/mau-in/{ma}/lich-su` | `MauInMacDinh.View.Detail` | như A8, không có chiều tenant |
| B8 | `GET /api/admin/mau-in/{ma}/lich-su/{id}` | `MauInMacDinh.View.Detail` | như A9, hợp nhất với catalog snapshot |

Không dùng `BaseCrudController` cho B1–B4: đây không phải CRUD trên một entity tìm kiếm được (47 dòng ghép từ
snapshot + override, khoá tự nhiên là `ma`). Ghi rõ lý do trong javadoc controller để review không hỏi lại.

---

## 8. DB

### 8.1 `cell-app` — `prn_mau_in_tuy_chinh` (migration `V<max+1>__prn_mau_in_tuy_chinh.sql`, lấy `max` ngay trước khi tạo; hôm nay max = 1146)

| Cột | Kiểu | Ghi chú |
|---|---|---|
| `id` | uuid PK | |
| `tenant_id` | uuid NOT NULL | RLS `tenant_isolation_prn_mau_in_tuy_chinh` giống `core_cau_hinh_cot` (`V1__create_database.sql:31895`) |
| `ma_loai_chung_tu` | varchar(20) NOT NULL | = `mst_loai_chung_tu.code` |
| `cau_hinh` | jsonb NOT NULL | `@JdbcTypeCode(SqlTypes.JSON) String` như `CauHinhCot.cauHinh` |
| `schema_version` | int NOT NULL | trùng `cau_hinh.schemaVersion` — lọc nâng cấp bằng SQL |
| `mac_dinh_nguon` | varchar(30) | `MAC_DINH_HE_THONG` \| `MAC_DINH_DONG_GOI` — bản tuỳ chỉnh xuất phát từ đâu |
| `mac_dinh_phien_ban` | int | phiên bản mẫu super admin lúc tách bản → tính `coMacDinhMoi` |
| `phien_ban` | int NOT NULL | `@Version` |
| audit BR46 | | `ngay_tao · nguoi_tao · ngay_cap_nhat · nguoi_cap_nhat · da_xoa · ngay_xoa · nguoi_xoa` — kế thừa `AggregateRootEntity` |
| ràng buộc | | `UNIQUE (tenant_id, ma_loai_chung_tu) WHERE da_xoa = false` |

Seed quyền: `V<max+2>__iam_quyen_ht_mau_in.sql` theo khuôn `V1111` — `HTMauIn.View`, `HTMauIn.Edit`
(`nhom = 'Hệ thống'`, `ten_chuc_nang = 'Thiết lập mẫu in'`), kèm khối `DO $$` đếm đủ 2 mã.

### 8.2 `super-admin-service` — `sa_mau_in_mac_dinh` (`common/V4__sa_mau_in_mac_dinh.sql`; H2 đã có V3 nên lấy V4)

| Cột | Kiểu | Ghi chú |
|---|---|---|
| `id` uuid PK · `ma_loai_chung_tu` varchar(20) UNIQUE (kèm `da_xoa`, làm ở vendor `postgresql/V5` index một phần; H2 kiểm ở service) | | |
| `cau_hinh` | **TEXT** | không `jsonb` ở `common/` (H2); `postgresql/V5` có thể `ALTER … TYPE jsonb USING cau_hinh::jsonb` — tuỳ chọn |
| `schema_version` int · `catalog_version` varchar(64) · `ghi_chu` varchar(1000) · `dang_ap_dung` boolean · `phien_ban` int (`@Version`) | | |
| audit | | kế thừa `core.entity.BaseEntity` (bảng `sa_*` của mình) |

Dữ liệu mẫu (nếu cần cho demo) **chỉ ở `h2/`** theo luật thư mục migration của service này.

---

### 8.3 Lịch sử phiên bản (bổ sung 2026-09-17 — R-MAUIN-101 · INV-MAUIN-009)

Hai bảng cùng hình dạng, chỉ khác chiều tenant:

| | `cell-app` | `super-admin-service` |
|---|---|---|
| Bảng | `prn_mau_in_lich_su` | `sa_mau_in_mac_dinh_lich_su` |
| Cột riêng | `tenant_id` + RLS/FORCE/GRANT như bảng chính | — |
| Cột chung | `id` · `ma_loai_chung_tu` · `phien_ban` · `cau_hinh` (JSON) · `schema_version` · `hanh_dong` `varchar(10)` ∈ {`LUU`,`XOA`} · `ghi_chu` · cột audit |
| Chỉ số | `(tenant_id, ma_loai_chung_tu, ngay_tao DESC)` | `(ma_loai_chung_tu, ngay_tao DESC)` |

Đọc và dọn theo **`ngay_tao DESC, phien_ban DESC`** — hai lần lưu liên tiếp có thể trùng mốc thời gian, khi đó
thứ tự chỉ theo `ngay_tao` là ngẫu nhiên của storage. Bản ghi chỉ được THÊM; dọn giữ 50 bản mới nhất mỗi loại
(`GIOI_HAN_LICH_SU`, đặt ở file riêng cạnh `GioiHanMauIn` để không làm lệch ba bản `GioiHanMauIn` ↔ `gioiHan.ts`).
`hanh_dong = XOA` lưu JSON **ngay trước** khi xoá, nhờ vậy khôi phục được bản vừa bỏ.

## 9. Quyền

| Nơi | Mã | Ai | Dùng cho |
|---|---|---|---|
| cell-app | `HTMauIn.View` | admin đơn vị | menu Hệ thống › Thiết lập mẫu in, A1, A2, A5 |
| cell-app | `HTMauIn.Edit` | admin đơn vị | A3, A4, mục "⚙ Thiết lập mẫu in…" trong menu In |
| cell-app | `<maChucNang>.Print` (đã có) | người in | A6, A7 và in thật |
| cell-app | `<maChucNang>.View` (đã có) | | A5 — chọn chứng từ thật để xem trước |
| super-admin | `MauInMacDinh.View · View.Detail · Edit · Delete` | super admin | B1–B4; khai ở `MaQuyenAdmin` |

Q4 là chỗ đổi sang quyền theo loại (`<maChucNang>.PrintConfig`) nếu user muốn — khi đó A2/A3 kiểm theo loại.

---

## 10. Fixture vàng (`docs/doing/mau-in-chung-tu/fixtures/`, chép vào test của cả 4 codebase)

| File | Kiểm |
|---|---|
| `mdv.mau-chuan.json` | mẫu chuẩn đóng gói của MDV (đúng bố cục mock) — snapshot của `MauChuanBuilder` |
| `mdv.catalog.json` · `mdv.du-lieu-mau.json` | catalog + dữ liệu mẫu (số liệu lấy từ `VOUCHERS.sample` của mock) |
| `hop-nhat/*.in.json` + `*.out.json` | 6 ca: thêm trường · thêm cột · thêm bảng · bỏ trường lạ · giữ dòng tự do · không đổi thứ tự |
| `kiem-tra/*.json` | mỗi luật R-MAUIN-010…025 một ca đỏ + một ca xanh |
| `chuan-hoa/*.json` | chia lại 100 %, dồn sai số cột cuối |

Bộ fixture là **hợp đồng chạy được** giữa TS và Java: đổi thuật toán ở một bên mà quên bên kia thì test bên kia đỏ.
