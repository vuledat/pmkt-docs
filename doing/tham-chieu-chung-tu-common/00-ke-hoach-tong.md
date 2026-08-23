# Kế hoạch: Common "Tham chiếu chứng từ" (tab Tham chiếu dùng chung cho mọi màn chứng từ)

> Trạng thái: **BẢN KẾ HOẠCH — CHƯA CODE**. Cần chốt các câu hỏi ở §8 trước khi vào pha 1.
> Ngày lập: 2026-08-22.

## 1. Mục tiêu

Một cơ chế **dùng chung duy nhất** cho tab "Tham chiếu" của mọi màn chứng từ (danh sách · thêm mới ·
chỉnh sửa · xem chi tiết · panel xem nhanh): lưu quan hệ **tham chiếu mềm** từ chứng từ hiện tại tới
các chứng từ khác trong hệ thống, theo đúng màn dùng chung
[`SCR_ThamChieuCT.md`](../../../pmkt-docs/ba/Common/NguonDuLieu/SCR_ThamChieuCT.md) và
[BR41](../../../pmkt-docs/ba/Common/business_rules.md).

Kết quả mong muốn: màn chứng từ mới **khai báo 1 lần** là có đủ tab Tham chiếu (lưới + nút Chọn chứng
từ / Xóa dòng / Xóa tất cả + panel chọn chứng từ + lưu + đọc + BR41), không viết lại UI, không tạo
bảng riêng, không tự nghĩ hợp đồng API.

## 2. Tài liệu đã đọc (cơ sở của kế hoạch)

| Tài liệu | Nội dung dùng |
|---|---|
| `Common/NguonDuLieu/SCR_ThamChieuCT.md` | Phần 1 popup chọn chứng từ (3 ô lọc + nút Tìm kiếm + bảng kết quả), Phần 2 tab (4 cột + 3 nút), BR1–BR3 của màn |
| `Common/business_rules.md` — **BR41** | Tham chiếu mềm: xóa/bỏ ghi sổ chứng từ nguồn ⇒ **không chặn, không cảnh báo**, tự gỡ liên kết ngầm, không đụng dữ liệu chứng từ đích |
| **BR4 / BR09** | Danh mục 47 loại chứng từ (`ENT_mst_loai_chung_tu`) — nguồn của ô lọc "Loại chứng từ" |
| **BR8** | Logic Khoảng thời gian ⇄ Từ ngày/Đến ngày (chọn preset thì fill ngày; sửa ngày thì preset về "Tùy chỉnh") |
| `Common/NguonDuLieu/SCR_NguonCT_TongHop.md` | Template bảng kết quả theo từng loại chứng từ (cách hiển thị "Chọn theo chứng từ"); loại không có template ⇒ bảng mặc định 7 cột |
| **BR1/BR2/BR11/BR13.1/BR30/BR39/BR44/BR45** | Quy tắc lưới (phân trang, sắp xếp, nút thao tác, ẩn/hiện cột, xuất Excel, truncate) |
| **BR12/BR25/BR28/BR29.2/BR46** | Trạng thái chứng từ, phân quyền, multi-tenant, chính sách xóa, trường hệ thống |
| 16 màn BA trỏ tới `SCR_ThamChieuCT.md` | CTBH · CT bán dịch vụ · CTMH · CT mua DV · HĐ mua hàng · HĐBH điều chỉnh · Điều chỉnh CCDC · Ghi tăng/Ghi giảm TSCĐ · Phiếu thu/chi TM · Phiếu thu/chi TG · Chuyển tiền nội bộ · Đánh giá lại TK ngoại tệ |

## 3. Hiện trạng — vì sao phải làm common

### 3.1 Backend: 7 bảng, 5 hợp đồng, 0 tìm kiếm chung

| Bảng | Chủ sở hữu | Hình dạng |
|---|---|---|
| `pur_chung_tu_tham_chieu` | chứng từ mua hàng | `loai_chung_tu_nguon` (text) + `chung_tu_nguon_id` + snapshot số CT + 8 cột trạng thái thừa |
| `pur_hoa_don_mua_tham_chieu` | hóa đơn mua | mirror bảng trên, thêm `ngay_chung_tu_nguon` |
| `cb_phieu_thu_tham_chieu` | phiếu thu | mirror `pur_chung_tu_tham_chieu` (COMMENT tự khai là mirror) |
| `cash_phieu_thu_chi_chung_tu_lien_quan` | phiếu thu/chi ngân quỹ | 5 UUID đa hình + `stt` + snapshot |
| `ktth_phieu_ke_toan_tong_hop_chung_tu_lien_quan` | phiếu KTTH | "đối xứng với bảng cash" (chính comment migration ghi vậy) |
| `ccdc_phieu_dieu_chinh_chung_tu_lien_quan` | phiếu điều chỉnh CCDC | copy bảng cash, **lệch khuôn 2 điểm** (đã ghi trong migration V1033) |
| `ccdc_tham_chieu_thu_cong` | **CCDC** (không phải phiếu) | mô hình khác hẳn: tham chiếu gắn vào tài sản, phiếu đọc gián tiếp |

Endpoint hiện có, mỗi module một kiểu: `GET /{id}/tham-chieu` (ngân quỹ),
`GET /{id}/chung-tu-lien-quan` (KTTH, mua hàng, mua dịch vụ), `POST /{id}/chung-tu-lien-quan/export`.
**Không có endpoint tìm kiếm chứng từ ứng viên** (Phần 1 của SCR) — đây là lỗ hổng lớn nhất.

Ranh giới đã rõ và **không được gộp**: module `quan_he_chung_tu` (`ctu_quan_he_chung_tu`) là quan hệ
**cứng** nguồn↔đích ở mức dòng, xóa nguồn thì **CHẶN**. Tham chiếu mềm thì **tự gỡ**. Chính
`quan_he_chung_tu/package-info.java` đã viết rõ hai chính sách xóa trái ngược nhau.

### 3.2 Frontend: 9 tab, 3 kiểu popup, 3 nguồn mock

| Màn | Component lưới | Popup chọn | Nguồn dữ liệu |
|---|---|---|---|
| `banHang/chungTuBanHang` | tự dựng footer + `CommonListTable` | Drawer riêng (bảng **hóa đơn** 6 cột, bấm dòng là chọn, không có nút Đồng ý) | `THAM_CHIEU_MOCK` |
| `nganQuy/_shared` (phiếu chi, chuyển tiền NB) | `CommonListTable` + hàng nút riêng | `ReferencePickerModal` của `@base` (modal giữa màn) | `MOCK_UNG_VIEN_THAM_CHIEU` |
| `nganQuy/chungTuTienMat`, `chungTuTienGui` | `CommonListTable` (chỉ đọc) | — | `GET /{id}/tham-chieu` (thật) |
| `congCuDungCu/dieuChinh` | `CommonEditableGrid` (footer = Action Bar) | Drawer trượt phải (Figma 60070:439281 + BR10) | API thật |
| `congCuDungCu/ghiTang` | `CommonEditableGrid` | copy 1:1 từ dieuChinh | — |
| `chiPhiTraTruoc/khaiBao` | `CommonEditableGrid` | popup riêng | `adapterChuaCoBE.ts` |
| `tongHop/phieuKeToanTongHop` | `CommonListTable` (chỉ đọc) | — | `GET /{id}/chung-tu-lien-quan` |
| `kho/phieuXuatKho` | `CommonEmpty` + suy từ lưới chi tiết | — | không có spec |

Ba kiểu popup khác nhau cho **cùng một màn dùng chung của BA** là bằng chứng đủ để làm common.

## 4. Thiết kế Backend

### 4.1 Module mới `cell/tham_chieu_chung_tu` (Spring Modulith, prefix bảng `ref_`)

```
cell/tham_chieu_chung_tu/
├── package-info.java                     @ApplicationModule(displayName = "tham_chieu_chung_tu")
├── api/                                  @NamedInterface("api")
│   ├── ThamChieuChungTuApi.java          cổng duy nhất module khác gọi
│   ├── NguonThamChieuPort.java           SPI: từng module chứng từ tự khai cách tra ứng viên
│   ├── LoaiChungTuChu.java               enum chủ sở hữu (khớp CHECK ở DB)
│   └── dto/                              @NamedInterface("api-dto"): DongThamChieuDto · UngVienDto · TieuChiTimKiem
└── internal/
    ├── controller/  ThamChieuChungTuController (package-private)
    ├── entity/      ThamChieuChungTu
    ├── repository/  ThamChieuChungTuRepository · UngVienQuery
    └── service/     ThamChieuChungTuService · business/{DongBoThamChieu, GoTheoNguon}
```

Vì sao module riêng, không nhét vào `accounting_core`: `accounting_core` tự khai phạm vi hẹp "nơi
DUY NHẤT ghi sổ cái", tham chiếu mềm không chạm sổ cái — đúng lập luận đã dùng cho
`quan_he_chung_tu`. Không nhét vào `common` vì đây là nghiệp vụ, không phải tiện ích.

### 4.2 Bảng chung `ref_chung_tu_tham_chieu`

```
id, tenant_id                              -- RLS FORCE, khớp BR28
loai_chung_tu_chu   text NOT NULL          -- CHECK whitelist, test đồng bộ enum ↔ pg_constraint
chung_tu_chu_id     uuid NOT NULL          -- chứng từ ĐANG lập (chứng từ B của BR41)
stt                 integer                -- cột STT lưới, LƯU THẬT (không row_number lúc đọc)
-- chứng từ ĐƯỢC tham chiếu (FK đa hình, KHÔNG enforce)
chung_tu_nguon_id   uuid NOT NULL
loai_chung_tu_id    uuid                   -- mst_loai_chung_tu (BR4)
-- KHÔNG có chi_tiet_nguon_id: đã chốt tham chiếu ở MỨC CHỨNG TỪ (Q3), đúng SCR_ThamChieuCT
-- SNAPSHOT (bắt buộc: FK đa hình không JOIN ra được, ADR-05 cấm join xuyên module)
so_chung_tu, ngay_chung_tu, ngay_hach_toan, ten_loai_chung_tu, tong_tien, dien_giai
tu_dong             boolean NOT NULL DEFAULT false   -- dòng do hệ thống sinh vs người dùng chọn
+ phien_ban, da_xoa, ngay_tao/nguoi_tao/ngay_cap_nhat/nguoi_cap_nhat/ngay_xoa/nguoi_xoa  (BR46)
```

Ràng buộc & index:
- `UNIQUE (tenant_id, loai_chung_tu_chu, chung_tu_chu_id, chung_tu_nguon_id) WHERE da_xoa = false` — chống thêm trùng (BR19). Một chứng từ chỉ nằm MỘT dòng trong tab.
- `INDEX (tenant_id, loai_chung_tu_chu, chung_tu_chu_id) WHERE da_xoa = false` — chiều đọc tab.
- `INDEX (tenant_id, chung_tu_nguon_id) WHERE da_xoa = false` — **chiều BR41**, bắt buộc, không có thì gỡ liên kết phải quét toàn bảng.
- RLS + FORCE + trigger kiểm tenant (theo đúng khuôn `ctu_quan_he_chung_tu`).
- Job quét mồ côi hàng đêm (FK đa hình không enforce được) — bắt buộc, như module `quan_he_chung_tu` đã ghi.

### 4.3 `ThamChieuChungTuApi`

```java
/** Ghi đè toàn bộ danh sách tham chiếu của một chứng từ (diff thêm/sửa/xóa). Gọi trong tx của module gọi. */
void dongBo(LoaiChungTuChu loaiChu, UUID chungTuChuId, List<DongThamChieuDto> dong);

/** Đọc cho tab Tham chiếu + panel Xem nhanh. */
List<DongThamChieuDto> theoChungTu(LoaiChungTuChu loaiChu, UUID chungTuChuId);

/** Xóa chứng từ chủ ⇒ dọn danh sách tham chiếu của chính nó. */
int xoaTheoChungTuChu(LoaiChungTuChu loaiChu, UUID chungTuChuId);

/** BR41: chứng từ NGUỒN bị xóa / bỏ ghi sổ ⇒ gỡ ngầm khỏi mọi chứng từ đang tham chiếu nó. */
int goTheoNguon(UUID chungTuNguonId);
```

Không có `capNhatMotDong` — sửa tab là sửa cả danh sách, `dongBo` là điểm ghi duy nhất. Cùng lý do
`quan_he_chung_tu` cố ý không có `capNhatLienKet`.

### 4.4 Tìm kiếm ứng viên (Phần 1 của SCR) — SPI `NguonThamChieuPort`

Đây là phần chưa từng có. Không thể viết một câu SQL: 47 loại chứng từ nằm ở ~10 module khác nhau,
ADR-05 cấm join xuyên module.

```java
public interface NguonThamChieuPort {
    String maLoaiChungTu();                       // mst_loai_chung_tu.code — "PBH", "PNK", "PKT"…
    List<UngVienDto> tim(TieuChiTimKiem tc);      // tuNgay, denNgay, tuKhoa, gioiHan
}
```

- Mỗi module chứng từ đăng ký **một bean** `NguonThamChieuPort`; service của common gom theo các mã
  loại người dùng chọn, sắp `ngay_chung_tu DESC, so_chung_tu`, phân trang tại tầng service.
- `UngVienDto` = đúng **bảng mặc định 7 cột** của SCR: `ngayHachToan · ngayChungTu · soChungTu ·
  loaiChungTu · tongTien · moTa` (+ `id`). Loại đã có template ở `SCR_NguonCT_TongHop` thì FE dựng cột
  theo registry `@domain-kit/chungTuNguon` sẵn có, BE vẫn trả 7 cột chuẩn + `duLieuThem` (map) nếu cần.
- Module chưa có port ⇒ **không hiện trong ô lọc Loại chứng từ** (danh sách loại lọc lấy từ tập port
  đã đăng ký, không lấy trọn 47 mã) — nhìn thấy loại nhưng tìm luôn ra 0 dòng là lỗi UX tệ hơn.
- Đợt 1 nên có port cho các loại đã có module thật: bán hàng, bán dịch vụ, hóa đơn bán hàng, mua hàng,
  mua dịch vụ, hóa đơn mua, phiếu nhập kho, phiếu xuất kho, phiếu thu/chi, phiếu KTTH (**xem Q5**).

### 4.5 BR41 — gỡ liên kết ngầm, qua sự kiện

`ChungTuTemplate` (accounting_core) là nơi mọi chứng từ đi qua khi Xóa / Bỏ ghi sổ
(`HanhDongChungTu.XOA` · `BO_GHI_SO`). Cho template **phát sự kiện**
`ChungTuDaXoa(loai, id)` / `ChungTuDaBoGhiSo(loai, id)`; module `tham_chieu_chung_tu` nghe bằng
`@ApplicationModuleListener` và gọi `goTheoNguon`.

Vì sao sự kiện chứ không gọi thẳng: `accounting_core` không được biết tới module tham chiếu (sai
chiều phụ thuộc). Hạ tầng đã sẵn — `spring-modulith-starter-jpa` + bảng `event_publication` đã có
trong migration, nên sự kiện được lưu bền, mất listener thì replay được chứ không mất liên kết.

**Đúng BR41**: không chặn, không cảnh báo, không đụng tới trạng thái/tiền/hạch toán của chứng từ đích.

### 4.6 Hợp đồng REST

| Method | Path | Dùng cho |
|---|---|---|
| `GET` | `/api/chung-tu/tham-chieu?loaiChu=&chungTuChuId=` | tab Tham chiếu (form + panel Xem nhanh) |
| `POST` | `/api/chung-tu/tham-chieu/ung-vien` | Phần 1 — tìm kiếm chứng từ ứng viên (body: `loaiChungTu[]`, `tuNgay`, `denNgay`, `tuKhoa`, `page`, `size`) |
| `GET` | `/api/chung-tu/tham-chieu/loai-chung-tu` | danh sách loại cho ô lọc (chỉ loại có port) |

Ghi tham chiếu **đi kèm payload lưu chứng từ** (`thamChieu: [...]` trong request của từng màn), template
gọi `dongBo` trong cùng transaction — tham chiếu và chứng từ phải cùng sống cùng chết. Không làm
endpoint POST/PUT riêng cho tab (sẽ đẻ ra trạng thái nửa vời khi lưu chứng từ hỏng).
Mọi response bọc `ApiResponse<T>`. Quyền: theo mã chức năng **của màn chủ** (`QuyenChecker`, BR25).

### 4.7 Di trú 7 bảng cũ — ĐÃ CHỐT: làm màn mới trước, thay thế sau

Quyết định (2026-08-22): **không backfill ở đợt này**. Trình tự:

1. Dựng bảng + module chung, **đấu vào chứng từ bán hàng (CTBH) làm màn thí điểm**.
2. CTBH là ca sạch: cụm `sal_` **chưa có bảng tham chiếu nào**, nên pilot là greenfield — không di trú
   dữ liệu, không đụng module đang chạy.
3. Chạy thật, nghiệm thu trên CTBH xong mới mở ticket riêng thay thế lần lượt 6 bảng + 8 màn còn lại.

Hệ quả phải chấp nhận trong giai đoạn quá độ: hai cơ chế song song. Chặn rủi ro "người sau copy nhầm
khuôn cũ" bằng cách ghi thẳng vào `package-info.java` của module chung và COMMENT của 6 bảng cũ:
*"bảng đóng băng — màn mới dùng `ref_chung_tu_tham_chieu`"*.

## 5. Thiết kế Frontend

### 5.1 Vị trí: `@domain-kit/thamChieu` (TIER 2)

Không đặt ở `@base` (base phải business-agnostic, mà tab này biết loại chứng từ, BR8, BR41), không đặt
ở `features/*/_shared` (phải dùng chung xuyên domain). Đúng chỗ là `src/base/domainKit/thamChieu/`,
cạnh engine `chungTuNguon` và `chungTu` đang có.

```
src/base/domainKit/thamChieu/
├── index.ts                        barrel (side-effect: đăng ký i18n namespace 'thamChieu')
├── api/        thamChieuApi.ts · thamChieuSchema.ts (Zod)
├── components/ ThamChieuTab.tsx · ChonChungTuPanel.tsx
├── constants/  constants.ts (THAM_CHIEU_NAME, page size, cỡ panel)
├── fields/     cotThamChieu.ts (Phần 2) · cotUngVien.ts (Phần 1 mặc định) · types.ts
├── helpers/    gopKhongTrung.ts · danhSachLoaiChungTu.ts · tieuChiTimKiem.ts
├── hooks/      useThamChieu.ts · useUngVienThamChieu.ts
├── i18n/       vi.ts · en.ts · registerThamChieuI18n.ts
└── test/
```

### 5.2 Hợp đồng component

```tsx
<ThamChieuTab
  loaiChu="CHUNG_TU_BAN_HANG"      // enum khớp BE
  chungTuChuId={id}                 // undefined khi Thêm mới ⇒ tab chạy thuần trên Form
  name={THAM_CHIEU_NAME}            // khóa trong Form của màn — lưu cùng payload chứng từ
  cheDo="SUA" | "XEM" | "PANEL"     // XEM: ẩn 3 nút; PANEL: chỉ đọc, tự gọi GET
  loaiChungTuChoPhep={[...]}        // tùy chọn: giới hạn loại ứng viên theo nghiệp vụ của màn
  t={t} locale={locale}
/>
```

Chuẩn dựng lưới: **`CommonEditableGrid`** — footer của nó chính là Action Bar của Figma (nút trái +
phân trang phải, cùng một hàng). 3/9 màn đã làm đúng thế; `CommonListTable` không mở slot dưới bảng
nên các màn dùng nó đều phải chế thêm một hàng và lệch thiết kế.

Popup Phần 1 — **ĐÃ CHỐT (Q2): panel trượt phải** (`Drawer`) theo **BR10** + Figma `60070:439281`.
Có **nút Tìm kiếm** (SCR: chỉ hiện kết quả sau khi bấm tìm), 3 ô lọc theo BR8, chọn nhiều dòng rồi
bấm **Đồng ý**. `ReferencePickerModal` của `@base` **giữ nguyên**, không sửa, không dùng cho tab này:
nó là modal giữa màn + danh sách live không có nút Tìm kiếm ⇒ lệch SCR ở 2 điểm. Panel mới dựng trong
`@domain-kit/thamChieu/components/ChonChungTuPanel.tsx`, cùng khuôn `Drawer` mà
`congCuDungCu/dieuChinh` và `ghiTang` đang dùng (đã đúng Figma).

### 5.3 Quy tắc bắt buộc kèm theo

- i18n: **một namespace `thamChieu`**, `vi.ts` giữ **nguyên văn tiếng Việt của BR/SCR**, `en.ts` đủ key (luật 2).
- Không `any`, dữ liệu BE parse bằng Zod (luật 3); import bằng alias, module phẳng một bậc (luật 4).
- Cột theo SCR Phần 2: `STT · Số chứng từ (link) · Ngày chứng từ · Loại chứng từ · Chức năng`.
- BR30 ẩn/hiện cột · BR39 xuất Excel · BR44 truncate · BR1 phân trang: dùng móc sẵn có của grid, không tự chế.
- Link "Số chứng từ" mở chứng từ nguồn: cần seam điều hướng theo loại + kiểm quyền xem (BR25) —
  hiện `nganQuy` đã có `useMoChungTuNguon`, nâng lên common.

### 5.4 Di trú 9 màn FE

**Màn thí điểm: `banHang/chungTuBanHang`** (đã chốt). Sau khi CTBH nghiệm thu xong mới mở ticket di
trú, thứ tự đề xuất theo rủi ro tăng dần: `congCuDungCu/ghiTang` → `congCuDungCu/dieuChinh` →
`chiPhiTraTruoc/khaiBao` → `nganQuy/_shared` + `chungTuTienMat` + `chungTuTienGui` →
`tongHop/phieuKeToanTongHop` → `kho/phieuXuatKho` (chưa có spec, chờ BA).

⚠ **CTBH có một lệch phải chốt trước khi code (Q8)**: popup "Chọn chứng từ" hiện tại của CTBH là
Drawer liệt kê **hóa đơn** (6 cột: ngày · số · mẫu số · ký hiệu · giá trị · khách hàng), bấm dòng là
chọn ngay, **không có nút Đồng ý** — khác hẳn popup chứng từ chung của SCR (bảng 7 cột, tick nhiều
dòng, bấm Đồng ý). Đấu common vào CTBH đồng nghĩa **thay popup hiện tại**. Cần BA xác nhận popup hóa
đơn là sai spec (bỏ) hay là ngoại lệ có chủ đích (giữ song song).

## 6. Phân pha & cổng nghiệm thu

| Pha | Nội dung | Artefact | Cổng |
|---|---|---|---|
| **P0** | Chốt Q1–Q7 với BA/người giao việc | biên bản chốt trong thư mục này | user duyệt |
| **P1 — BE nền** | migration bảng chung + module + `ThamChieuChungTuApi` + unit test | `V####__ref_chung_tu_tham_chieu.sql`, module Java, test Modulith `ApplicationModules.verify()` | `cd cell-app && ./gradlew unitTest` xanh |
| **P2 — BE tìm kiếm** | SPI `NguonThamChieuPort` + port cho các loại đợt 1 + 3 endpoint + Postman collection | `docs/json/tham-chieu-chung-tu.postman.json` | unitTest xanh + gọi thử qua IntelliJ run config |
| **P3 — BR41** | sự kiện Xóa/Bỏ ghi sổ ở `ChungTuTemplate` + listener gỡ liên kết + test | test: xóa CT nguồn ⇒ dòng tham chiếu biến mất, CT đích không đổi | unitTest xanh |
| **P4 — FE common** | `@domain-kit/thamChieu` đầy đủ (tab + Drawer chọn + hook + api + i18n) + test | | `npm run typecheck && lint && lint:boundaries && test && build` |
| **P5 — Pilot CTBH** | đấu common vào `banHang/chungTuBanHang` (BE port + payload lưu + FE tab), xóa `THAM_CHIEU_MOCK` và Drawer hóa đơn cũ | port `NguonThamChieuPort` cho CTBH | cổng FE + `npm run check:committed` + user nghiệm thu trên màn thật |
| **P6 — Di trú (TICKET RIÊNG, sau khi CTBH chạy)** | 8 màn còn lại + backfill 6 bảng cũ → bảng chung → drop | migration backfill + script đối soát | unitTest xanh + đối soát số dòng trước/sau |

Chạy code: **qua IntelliJ MCP**, không Docker. Test tích hợp Testcontainers **không chạy được** trên
máy này — phải ghi rõ trong báo cáo hoàn thành.

## 7. Rủi ro

1. **Tìm kiếm xuyên module chậm** khi người dùng tick nhiều loại chứng từ — chặn bằng `gioiHan` mỗi
   port + bắt buộc có khoảng ngày (SCR đã yêu cầu điền tiêu chí trước khi tìm).
2. **Snapshot lệch thực tế**: chứng từ nguồn đổi số/ngày sau khi được tham chiếu ⇒ snapshot cũ. Cần chốt
   có đồng bộ lại không (Q6).
3. **Backfill 6 bảng** khác hình dạng, nhất là `cash`/`ktth` có 5 UUID đa hình còn `pur`/`cb` chỉ có
   text + 1 UUID — phải viết map từng bảng, không có đường tự động.
4. **`ccdc_tham_chieu_thu_cong`** mô hình khác bản chất (gắn vào tài sản) — ép vào common có thể sai
   nghiệp vụ (Q4).
5. FE `banHang/chungTuBanHang` đang dùng popup **hóa đơn** thay vì popup chứng từ chung — hoặc BA sai
   hoặc màn này là ngoại lệ có chủ đích; phải chốt trước khi di trú.

## 8. Câu hỏi

### Đã chốt (2026-08-22)

- **Q1 — Phạm vi**: ✅ Làm common cho **màn mới trước**, tích hợp vào **chứng từ bán hàng** làm thí
  điểm; thay thế các màn/bảng cũ ở ticket sau.
- **Q2 — Popup Phần 1**: ✅ **Panel trượt phải (Drawer)** theo BR10 + Figma `60070:439281`.
  `ReferencePickerModal` giữ nguyên, không dùng cho tab này.
- **Q3 — Mức tham chiếu**: ✅ Chỉ **mức chứng từ**, đúng `SCR_ThamChieuCT` — bảng chung **không có**
  `chi_tiet_nguon_id`.

### Còn chặn
- **Q4 — CCDC**: `ccdc_tham_chieu_thu_cong` (tham chiếu gắn vào tài sản) có nằm trong common không?
- **Q5 — Loại chứng từ đợt 1**: danh sách loại phải tìm kiếm được ngay ở pha 2 gồm những gì?
- **Q6 — Snapshot**: khi chứng từ nguồn đổi số/ngày, tab tham chiếu hiển thị số cũ (snapshot) hay
  đồng bộ lại?
- **Q7 — Ghi Excel/ẩn cột**: tab Tham chiếu có cần BR30 (ẩn/hiện cột) + BR39 (xuất Excel) không, hay
  chỉ lưới đọc đơn giản?
- **Q8 — CTBH (chặn P5)**: popup chọn hiện tại của CTBH liệt kê **hóa đơn** (6 cột, bấm dòng là chọn,
  không nút Đồng ý) — sai spec nên thay bằng popup chứng từ chung, hay là ngoại lệ có chủ đích phải
  giữ song song? Xem §5.4.

## 9. BR sẽ áp dụng

BR1 · BR2 · BR3 · BR4/BR09 · BR8 · BR11 · BR12 · BR13.1 · BR19 · BR25 · BR26 · BR28 · BR29.2 · BR30 ·
BR32 · BR39 · BR41 (trọng tâm) · BR43 · BR44 · BR45 · BR46.
