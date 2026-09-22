# Hợp đồng kỹ thuật v1 — module `bieu_mau` (BE `report-service`) · `features/bieuMau` (FE)

> Nguồn sự thật DUY NHẤT cho mọi agent BE/FE. Lệch hợp đồng = lỗi, không "tự hiểu" thêm. Bản thiết kế
> tổng: [00-giai-phap.md](00-giai-phap.md). Ngày 2026-09-08.

## 0. Quy ước chung

- BE: Java 21, Spring Boot, package **`vn.vtt.pmkt.cell.bieu_mau`** trong `report-service/`. Modulith
  module riêng (`package-info.java` + `@ApplicationModule(displayName = "bieu_mau")`). Mặc định
  `internal/`; không tạo `api/` (chưa module nào cần gọi vào).
- Cấm: `net.sf.jasperreports.**` ngoài `internal.ket_xuat.jasper`; `org.apache.poi.**` ngoài
  `internal.ket_xuat.poi` và `internal.nhap_excel`; cấm nạp `.jasper`/JRXML từ ngoài; cấm biểu thức
  Jasper động — mọi text field Jasper chỉ là `$F{...}` của lưới đã tính.
- JSON: Jackson, **tên trường tiếng Việt camelCase đúng như dưới**, không đổi. `null` = vắng.
- FE: TS strict, Zod 4 parse mọi dữ liệu ngoài, alias `@platform`/`@base`/`@core`, antd 6, i18n cả
  `vi.ts` và `en.ts`, không `any`.
- Đơn vị kích thước: **point** (pt, 1/72 inch). Excel: rộng cột (ký tự) × 7 = px, px × 0,75 = pt; cao
  dòng Excel đã là pt.

## 1. Schema `BieuMauDinhNghia` v1

```ts
type BieuMauDinhNghia = {
  schemaVersion: 1
  ma: string                      // ^[A-Z0-9_]{2,64}$
  ten: string
  trang: {
    kho: 'A4' | 'A3' | 'A5' | 'LETTER' | 'TUY_CHINH'
    huong: 'DOC' | 'NGANG'
    rongTuyChinh?: number; caoTuyChinh?: number   // pt, chỉ khi TUY_CHINH (khổ ĐỨNG)
    le: { tren: number; duoi: number; trai: number; phai: number }
    coGiuTrang: 'KHONG' | 'VUA_CHIEU_RONG'          // VUA_CHIEU_RONG: thu tỉ lệ toàn lưới cho vừa bề rộng, sàn 0,6
  }
  font: { macDinh: string; coMacDinh: number }       // font ∈ whitelist GET /font
  thamSo: ThamSo[]
  nguonDuLieu: NguonDuLieu[]
  bien: { ma: string; congThuc: string }[]           // ma ^[a-zA-Z_][a-zA-Z0-9_]*$, không trùng nguồn
  kieuDang: (KieuDang & { ma: string; keThua?: string })[]
  cot: Cot[]
  dong: Dong[]
  phanTuNoi: PhanTuNoi[]
}
type ThamSo = { ma: string; ten?: string; kieu: 'text'|'number'|'date'|'uuid'|'boolean'; batBuoc?: boolean; macDinh?: string }
type NguonDuLieu = {
  ma: string                                      // ^[a-zA-Z_][a-zA-Z0-9_]*$ — dùng trong công thức
  loai: 'CATALOG' | 'TINH'
  provider?: string                               // CATALOG: mã provider, vd "thue.bangKeBanRa.dong"
  dangDong: 'MOT_DONG' | 'NHIEU_DONG'
  thamSo?: Record<string, string>                 // giá trị = công thức (thường "param.toKhaiId")
  duLieuTinh?: Record<string, unknown>[]          // TINH
}
type Cot = { ma: string; rong: number; anKhi?: string; coGian?: boolean }   // ma: "A".."ZZ" duy nhất
type KieuDang = {
  font?: string; co?: number; dam?: boolean; nghieng?: boolean; gachChan?: boolean
  mauChu?: string; mauNen?: string                // "#RRGGBB"
  canNgang?: 'TRAI'|'GIUA'|'PHAI'; canDoc?: 'TREN'|'GIUA'|'DUOI'
  xuongDong?: boolean
  vien?: string                                   // tập con các chữ L R T B, vd "LRTB", "T", ""
  doDayVien?: number; mauVien?: string            // mặc định 0.5 pt, "#000000"
  dinhDangSo?: string                             // pattern Excel 1–4 phần: "#,##0;(#,##0);;"
  dinhDangNgay?: string                           // "dd/MM/yyyy"
  dinhDangLogic?: string                          // "X|" (đúng|sai, tách bằng |), "☑|☐", "Có|Không"
  thutLe?: number; padding?: number               // pt
}
type O = {
  cot: string; gopDen?: string; gopDenDong?: string   // gộp ngang tới cột; gộp dọc tới id dòng (chỉ TINH/HEADER liền kề)
  text?: string                                   // tĩnh — hoặc
  congThuc?: string                               // §2 — chỉ một trong text/congThuc
  kieu?: 'CHU'|'SO'|'NGAY'|'LOGIC'                // gợi ý kiểu khi công thức không suy được; mặc định theo giá trị
  kieuDang?: string; ghiDe?: KieuDang
  anKhi?: string                                  // công thức logic → ô rỗng (vẫn giữ viền)
  kieuDangKhi?: { khi: string; kieuDang: string }[]   // style có điều kiện, áp lần lượt
  renderKhi?: { khi: string; kieu: 'CHU'|'LOGIC'|'AN' }[]
}
type DongThuong = {
  id: string; loai: 'TINH'|'HEADER'|'CHI_TIET'|'TONG'|'DAU_TRANG'|'CHAN_TRANG'|'NGAT_TRANG'
  cao: number; tuDan?: boolean; caoToiThieu?: number
  lapMoiTrang?: boolean                           // HEADER
  nguon?: string; loc?: string                    // CHI_TIET: nguồn NHIEU_DONG; loc = công thức logic trên row (và nhom.*)
  sapXep?: string                                 // CHI_TIET: "row.ngayHoaDon ASC, row.soHoaDon ASC"
  danhSoLai?: boolean                             // CHI_TIET trong NHOM: ROW_INDEX() đếm lại từ 1
  anKhi?: string
  giuCungTrangVoiDongTruoc?: boolean
  o: O[]
}
type DongNhom = {
  id: string; loai: 'NHOM'
  nguonNhom?: string                              // cách 2: lặp theo từng dòng của nguồn NHIEU_DONG (nhóm cố định, kể cả rỗng)
  nguon?: string; theo?: string                   // cách 1: suy nhóm từ dữ liệu — distinct giá trị của `theo` (công thức trên row)
  sapXep?: 'ASC'|'DESC'; anKhiRong?: boolean
  dau: DongThuong[]; than: Dong[]; cuoi: DongThuong[]
}
type Dong = DongThuong | DongNhom
type PhanTuNoi = {
  id: string; loai: 'ANH'|'HOP_CHU'|'DUONG_KE'
  neo: { dong: string; cot: string; dx: number; dy: number }; w: number; h: number
  taiSanId?: string; base64?: string             // ANH
  text?: string; congThuc?: string; kieuDang?: string; ghiDe?: KieuDang   // HOP_CHU
  anKhi?: string; theoTrang?: 'MOT_LAN'|'MOI_TRANG'
}
```

Ràng buộc validator (mã lỗi → `duongDan` JSON Pointer):
`BM_MA_TRUNG` (id dòng/mã cột/mã nguồn/mã biến trùng) · `BM_COT_KHONG_TON_TAI` · `BM_NGUON_KHONG_TON_TAI`
· `BM_PROVIDER_KHONG_TON_TAI` · `BM_CONG_THUC_LOI` (kèm vị trí ký tự) · `BM_CONG_THUC_VONG` ·
`BM_GOP_O_CHONG` · `BM_CHI_TIET_THIEU_NGUON` · `BM_NHOM_THIEU_NGUON` · `BM_FONT_KHONG_HOP_LE` ·
`BM_PAGE_NGOAI_CHAN_TRANG` (PAGE/PAGES ngoài DAU_TRANG/CHAN_TRANG) · `BM_ROW_NGOAI_CHI_TIET`
(row.* ngoài CHI_TIET/loc/sapXep) · `BM_NHOM_NGOAI_NHOM`.

## 2. Ngôn ngữ công thức

```
expr    := or
or      := and ("OR" and)*
and     := not ("AND" not)*
not     := "NOT" not | cmp
cmp     := cat (("=" | "<>" | "<" | "<=" | ">" | ">=") cat)?
cat     := add ("&" add)*
add     := mul (("+" | "-") mul)*
mul     := unary (("*" | "/") unary)*
unary   := "-" unary | pow
pow     := atom ("^" unary)?
atom    := NUMBER | STRING | "TRUE" | "FALSE" | "NULL" | ident | call | "(" expr ")"
ident   := NAME ("." NAME)?          // header.tenNnt · row.x · nhom.x · param.x · bien
call    := NAME "(" (expr ("," expr)*)? ")"
```
Từ khoá không phân biệt hoa/thường; tên hàm viết HOA. STRING trong `"..."` (escape `\"`), NUMBER thập
phân dấu chấm. Kiểu: `SO` (BigDecimal), `CHU`, `NGAY` (LocalDate), `LOGIC`, `NULL`. `null` trong phép số
= 0, trong `&` = "", trong so sánh: `NULL = NULL` là TRUE. So sánh chuỗi không phân biệt hoa/thường,
có dấu. Chia cho 0 → NULL. Kết quả số làm tròn theo pattern lúc hiển thị (HALF_UP).

Phạm vi định danh:

| Dạng | Ở đâu | Nghĩa |
|---|---|---|
| `nguon.truong` (nguồn MOT_DONG) | mọi nơi | trường của dòng duy nhất |
| `nguon.truong` (nguồn NHIEU_DONG) | chỉ làm **đối số hàm tập hợp** hoặc trong **điều kiện của SUMIF/COUNTIF** | cột |
| `row.truong` | ô của CHI_TIET, `loc`, `sapXep`, `kieuDangKhi/anKhi` trong CHI_TIET | dòng hiện tại |
| `nhom.truong` | trong NHOM (dau/than/cuoi) | cách 2: dòng nguồn nhóm; cách 1: `nhom.khoa` + các trường của dòng đầu nhóm |
| `param.x` | mọi nơi | tham số |
| `tenBien` | mọi nơi | biến cấp biểu mẫu (tính một lần, không được dùng row/nhom) |

Hàm v1 (bắt buộc đủ): `SUM(col)` `SUMIF(col, cond)` `COUNT(nguon|col)` `COUNTIF(col, cond)` `MIN` `MAX`
`AVG` · `GROUP_SUM(col)` `GROUP_COUNT()` `GROUP_MIN` `GROUP_MAX` (trên dòng thuộc nhóm hiện tại) ·
`GROUP_INDEX()` (1-based) `GROUP_KEY()` · `ROW_INDEX()` · `ROUND(x, n=0)` `ROUNDUP` `ROUNDDOWN` `ABS`
`MOD` · `IF(c,a,b)` `IFS(c1,v1,...,vElse)` `AND` `OR` `NOT` `COALESCE(...)` `ISNULL(x)` · `LEN` `LEFT`
`RIGHT` `MID` `UPPER` `LOWER` `TRIM` `CONCAT` `REPLACE` · `FORMAT(so, pattern)` `TEXT(x)` `VALUE(chu)` ·
`TODAY()` `DATE(y,m,d)` `YEAR` `MONTH` `DAY` `DATE_FORMAT(d, pattern)` `DATE_ADD(d, n, "DAY|MONTH|YEAR")`
`DATE_DIFF(d1,d2)` · `NUM_TO_WORDS(x)` (tiền bằng chữ tiếng Việt) · `PAGE()` `PAGES()` (chỉ DAU_TRANG/
CHAN_TRANG; renderer thay bằng số trang thật) · `LOOKUP(nguon, truongKhoa, giaTri, truongLay)`.

Trong `SUMIF(col, cond)`: `cond` được đánh giá trên **từng dòng của nguồn của `col`**, trong đó tham chiếu
`nguon.truong` cùng nguồn = trường của dòng đó (vd `SUMIF(bkbr.doanhThu, bkbr.nhom <> 1)`).

## 3. Nở lưới → `LuoiKetXuat` (RenderGrid)

1. Nạp nguồn (`CATALOG` qua `NguonDuLieuProvider`; `duLieuMau=true` → `duLieuMau()`).
2. Tính `bien` (topo sort, phát hiện vòng).
3. Duyệt `dong[]`: TINH/HEADER/TONG/DAU_TRANG/CHAN_TRANG → 1 dòng; CHI_TIET → n dòng (lọc `loc`, sắp
   `sapXep`); NHOM → với mỗi nhóm: `dau` + `than` (đệ quy; CHI_TIET bên trong lọc thêm theo nhóm) +
   `cuoi`; `anKhiRong` bỏ nhóm không có dòng con. `anKhi` dòng đúng → bỏ dòng.
4. Mỗi ô: tính công thức → `GiaTriO { kieu, giaTri, chuoi }` + style resolve (kế thừa: font mặc định →
   kieuDang → ghiDe → kieuDangKhi). Ô gộp giữ `gopNgang`, `gopDoc` (số ô).
5. `LuoiKetXuat { trang, cot[], dong[] (moi dong: id goc, loai, cao, o[]), phanTuNoi[], headerLap: id[] }`.
   Dòng `HEADER lapMoiTrang` kề nhau thành một khối lặp cho bảng kế tiếp; dòng `DAU_TRANG/CHAN_TRANG`
   tách ra khỏi thân.

## 4. Port Java (BE-B gọi, BE-A hiện thực) — package `vn.vtt.pmkt.cell.bieu_mau.internal.port`

Đã tạo sẵn các file trong package này (xem code). Không đổi chữ ký; cần thêm thì thêm method `default`.

## 5. Nguồn dữ liệu — SPI + catalog mẫu

```java
public interface NguonDuLieuProvider {
    String ma(); String ten(); String nhom(); DangDong dangDong();
    List<TruongMoTa> truong(); List<ThamSoMoTa> thamSo();
    List<Map<String, Object>> nap(Map<String, Object> thamSo);      // thật — v1 thuế: ném NGUON_CHUA_SAN_SANG
    List<Map<String, Object>> duLieuMau();                           // cho designer/xem trước
}
```
Provider mẫu thuế nạp từ JSON `src/main/resources/bieu_mau/nguon/*.json` (một class
`JsonNguonDuLieuProvider` đọc thư mục, đăng ký mỗi file một provider). Cấu trúc file:
`{ "ma","ten","nhom","dangDong","truong":[{ma,ten,kieu}], "thamSo":[...], "duLieuMau":[{...}] }`.
Kiểu trường: `CHU|SO|NGAY|LOGIC`. Ngày trong JSON: `yyyy-MM-dd`.

## 6. API HTTP (BE `report-service`, prefix `/api/bieu-mau`; FE gọi qua cell-app proxy cùng path)

Bọc `ApiResponse<T>`; file trả `ResponseEntity<byte[]>` với `Content-Disposition`. Lỗi qua
`GlobalExceptionHandler` (`ApiException`).

| Method path | Body → Data |
|---|---|
| `POST /tim-kiem` `{tuKhoa?, nhom?, trangThai?, page=1, pageSize=20}` | `PageResponse<BieuMauDong>` (`{data:[], pagination:{page,pageSize,totalItems,totalPages}}`) |
| `GET /{id}` | `BieuMauChiTiet` = `BieuMauDong` + `dinhNghiaNhap` (bản nháp) + `phienBanHienHanh?` |
| `POST /` `{ma, ten, nhom, moTa, dinhNghia?}` | `BieuMauDong` (tạo nháp; `dinhNghia` mặc định = lưới trống 8 cột) |
| `PUT /{id}` `{ten, nhom, moTa}` | `BieuMauDong` |
| `DELETE /{id}` | mềm |
| `POST /{id}/nhan-ban` `{ma, ten}` | `BieuMauDong` |
| `PUT /{id}/nhap` `{dinhNghia, hashTruoc?}` | `{hash}` — 409 `BM_PHIEN_BAN_XUNG_DOT` nếu hashTruoc lệch |
| `POST /{id}/phat-hanh` `{hieuLucTu?, hieuLucDen?, ghiChu?}` | `PhienBanDong` |
| `GET /{id}/phien-ban` | `PhienBanDong[]` |
| `GET /{id}/phien-ban/{pv}` | `PhienBanChiTiet` (kèm `dinhNghia`) |
| `POST /{id}/khoi-phuc/{pv}` | chép định nghĩa phiên bản vào nháp |
| `POST /kiem-tra` `{dinhNghia}` | `KiemTraKetQua` |
| `POST /xem-truoc?format=pdf|xlsx|docx` `{dinhNghia, thamSo?, duLieuMau=true}` | file |
| `POST /{ma}/ket-xuat?format=` `{thamSo, ngayHieuLuc?, duLieuMau?}` | file — chọn phiên bản PHÁT HÀNH hiệu lực; tenant override > hệ thống |
| `POST /ket-xuat-bo?format=pdf` `{muc:[{ma, thamSo}], danhSoLienTuc}` | file PDF gộp |
| `GET /nguon-du-lieu` | `NguonMoTa[]` |
| `POST /nguon-du-lieu/{ma}/du-lieu-mau` | `Map[]` (≤ 50 dòng) |
| `GET /cong-thuc/ham` | `HamMoTa[]` |
| `GET /font` | `string[]` |
| `POST /nhap-tu-excel` multipart `file`, `sheet?` | `NhapExcelKetQua {dinhNghia, token[], sheets[]}` |
| `GET /schema/v1` | JSON Schema |

`BieuMauDong = {id, ma, ten, nhom, moTa, trangThai:'NHAP'|'DA_PHAT_HANH'|'LUU_TRU', heThong:boolean,
soPhienBanHienHanh?:number, hieuLucTu?, hieuLucDen?, ngayCapNhat, nguoiCapNhat}`.
`PhienBanDong = {id, soPhienBan, trangThai, hieuLucTu?, hieuLucDen?, ghiChu?, hash, ngayTao, nguoiTao}`.

Quyền (mã đã chọn, kiểm ở cell-app proxy bằng `QuyenChecker`; report-service chỉ kiểm đã đăng nhập):
`BieuMau.View` · `BieuMau.Create` · `BieuMau.Edit` · `BieuMau.Delete` · `BieuMau.Export` ·
`BieuMau.Import` · `BieuMau.Publish`.

S2S cho module khác trong cell-app: `POST /internal/bieu-mau/ket-xuat` và `/ket-xuat-bo` (cùng body,
header `X-Internal-Token`, `X-Tenant-Id`).

## 7. DB — schema `bieu_mau` (Flyway riêng của report-service)

`spring.flyway.schemas=bieu_mau`, `table=flyway_schema_history_bieu_mau`, `locations=classpath:db/bieu_mau`.
File: `V20260908210000__bm_bieu_mau.sql`, seed hệ thống: `R__bm_seed_he_thong.sql` (repeatable, chạy lại khi
checksum đổi; INSERT … ON CONFLICT DO UPDATE theo `(ma) WHERE tenant_id IS NULL`).

```sql
CREATE TABLE bieu_mau.bm_bieu_mau (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NULL,                      -- NULL = mẫu hệ thống
  ma varchar(64) NOT NULL, ten varchar(255) NOT NULL,
  nhom varchar(32) NOT NULL DEFAULT 'KHAC', mo_ta text,
  trang_thai varchar(16) NOT NULL DEFAULT 'NHAP',
  he_thong boolean NOT NULL DEFAULT false,
  ke_thua_tu_id uuid NULL, phien_ban_hien_hanh_id uuid NULL,
  dinh_nghia_nhap jsonb NOT NULL, hash_nhap char(64) NOT NULL,
  phien_ban int NOT NULL DEFAULT 0,          -- optimistic lock
  ngay_tao timestamptz NOT NULL DEFAULT now(), nguoi_tao uuid, ngay_cap_nhat timestamptz, nguoi_cap_nhat uuid,
  da_xoa boolean NOT NULL DEFAULT false, ngay_xoa timestamptz, nguoi_xoa uuid
);
CREATE UNIQUE INDEX ux_bm_bieu_mau_ma ON bieu_mau.bm_bieu_mau (COALESCE(tenant_id,'00000000-0000-0000-0000-000000000000'), ma) WHERE da_xoa = false;
CREATE TABLE bieu_mau.bm_phien_ban (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NULL, bieu_mau_id uuid NOT NULL REFERENCES bieu_mau.bm_bieu_mau(id),
  so_phien_ban int NOT NULL, dinh_nghia jsonb NOT NULL, schema_version int NOT NULL DEFAULT 1,
  hash char(64) NOT NULL, hieu_luc_tu date, hieu_luc_den date,
  trang_thai varchar(16) NOT NULL DEFAULT 'DA_PHAT_HANH', ghi_chu text,
  ngay_tao timestamptz NOT NULL DEFAULT now(), nguoi_tao uuid,
  UNIQUE (bieu_mau_id, so_phien_ban)
);
-- RLS cả hai bảng: ENABLE + FORCE; policy USING (tenant_id IS NULL OR tenant_id = public.fn_current_tenant())
--   WITH CHECK (tenant_id = public.fn_current_tenant()); GRANT SELECT/INSERT/UPDATE/DELETE TO pmkt_app; GRANT USAGE ON SCHEMA.
```

## 8. FE — cấu trúc & hợp đồng nội bộ

```
client/src/features/bieuMau/
├── routes.tsx                              (FE-A)
├── _shared/                                (FE-A) api/bieuMauApi.ts · api/dinhNghiaSchema.ts (Zod của §1, export type)
│                                           constants/{paths,permissions}.ts · i18n/{vi,en,registerBieuMauSharedI18n}.ts
├── danhSachBieuMau/                        (FE-A) màn quản lý
└── thietKeBieuMau/                         (FE-B) designer — import `@features/bieuMau/_shared/...` cho api/schema/paths
```
Route: `/bieu-mau` (danh sách) · `/bieu-mau/:id/thiet-ke` (designer, layout full-screen). Menu: nhóm
`other` → mục `bieu-mau`, `titleKey: 'shell.menu.bieuMau'`, icon `LayoutIcon`, `anyOf: [BIEU_MAU_PERM.view]`.
Namespace i18n: `bieuMauShared`, `bieuMauDanhSach`, `bieuMauThietKe`.
Tải file: `http.post(url, body, { responseType: 'blob' })` rồi mở blob URL (tiền lệ
`features/nganQuy/_shared/api/inPhieuApi.ts`), không `window.open(url)` trần.

## 9. Bổ sung 2026-09-09 — nguồn dữ liệu kiểu `API` (API bất kỳ, có chế độ sample)

```ts
type NguonDuLieu = {
  ma: string; dangDong: 'MOT_DONG' | 'NHIEU_DONG'
  loai: 'CATALOG' | 'TINH' | 'API'
  // …CATALOG/TINH như §1…
  api?: {
    url: string                              // http(s)://… ; được chứa {{param.x}} thay thế trước khi gọi
    method?: 'GET' | 'POST'                  // mặc định GET
    headers?: Record<string, string>         // giá trị được chứa {{param.x}}
    body?: string                            // POST: JSON/text, được chứa {{param.x}}
    thamSoQuery?: Record<string, string>     // GET/POST: thêm query ?k=v (v là công thức, thường "param.toKhaiId")
    duongDanDuLieu?: string                  // đường dẫn tới dữ liệu trong JSON trả về, dạng "a.b[0].c" hoặc "data.items"; rỗng = gốc
    sample?: {                               // cách bật CHẾ ĐỘ SAMPLE khi duLieuMau=true
      kieu: 'QUERY' | 'HEADER'               // mặc định QUERY
      ten: string                            // mặc định "mode"
      giaTri: string                         // mặc định "sample"
    }
    timeoutMs?: number                       // mặc định 10000, tối đa 60000
  }
}
```
- Kết quả API: MOT_DONG → object (hoặc mảng lấy phần tử đầu); NHIEU_DONG → mảng object. Kiểu trường suy từ
  JSON: number → SO, boolean → LOGIC, chuỗi `yyyy-MM-dd`/ISO → NGAY, còn lại CHU; object/array lồng → chuỗi JSON.
- Cùng một lần kết xuất, các nguồn API có cùng (url, method, headers, body, query đã thay thế) chỉ gọi **một
  lần** (cache theo lần chạy) — một API trả nhiều mảng (`header`, `phaiNop`, …) khai thành nhiều nguồn chỉ
  khác `duongDanDuLieu`.
- `duLieuMau=true` → gọi API kèm sample (query `?mode=sample` hoặc header) thay vì trả lỗi; `false` → gọi thật.
- Bảo mật: chỉ `http/https`; chặn `file:`, `jar:`; host cho phép theo `pmkt.bieu-mau.api.allow-hosts`
  (mặc định `*` ở dev, prod nên liệt kê); giới hạn phản hồi 5 MB; timeout; không theo redirect sang host khác.
- Endpoint khám phá cho designer: `POST /api/bieu-mau/nguon-du-lieu/api/kham-pha` `{api, thamSo?, dangDong}`
  → `{ truong: TruongMoTa[], duLieuMau: object[] (≤ 20 dòng), canhBao: string[] }` (luôn gọi ở chế độ sample).
- API giả để thử (report-service, permitAll, chỉ dữ liệu fake, bật bằng `pmkt.bieu-mau.mau-api.enabled`
  mặc định true): `GET /mau-api/to-khai-bo-sung?mode=sample&toKhaiId=…` trả
  `{ header:{…}, phaiNop:[…], phanBo:[…], khauTru:[…], deNghiHoan:[…] }` cùng trường như các nguồn
  `thue.toKhaiBoSung.*`; không có `mode=sample` → 404 `MAU_API_CHI_CO_SAMPLE` (mô phỏng API thật chưa có).
  Seed thêm biểu mẫu `TO_KHAI_BO_SUNG_01_KHBS_API` = bản 01/KHBS dùng 5 nguồn API trỏ vào endpoint này.
