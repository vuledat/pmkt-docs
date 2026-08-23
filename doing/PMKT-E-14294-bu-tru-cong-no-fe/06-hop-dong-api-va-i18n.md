# 06 — Hợp đồng API với BE · Bảng khoá i18n · Hằng số · Quyền · Đường dẫn

> ⚠ **Toàn bộ mục §1 là ĐỀ XUẤT, chưa chốt với BE.** `cell-app` hiện **không có** module
> `bu_tru_cong_no` lẫn `phieu_ke_toan_tong_hop` (xem [00 §2](00-ke-hoach-tong.md)). Phải chốt §1 với
> BE **trước** khi code `api/model.ts` — Zod schema là điểm gãy đắt nhất nếu đoán sai.
>
> Đề nghị chạy `/plan-be` cho epic này để có `docs/doing/PMKT-E-14294-bu-tru-cong-no-api/` đối chiếu.

---

## 1. Hợp đồng với BE

### 1.0. Quy ước nền

Mọi response bọc `ApiResponse<T>` (luật 6 của `CLAUDE.md`) ⇒ FE đọc `res.data.data`.
Nếu BE dựng trên `BaseCrudController` như `chung_tu_ban_hang`, phần lớn endpoint lấy sẵn từ
`createSearchApi` + `createSearchQueries` của `@platform`
(mẫu: `features/banHang/chungTuBanHang/api/chungTuBanHangApi.ts:21-31` và `api/queries.ts:11-19`),
FE **không** viết tay.

`BASE = '/api/tong-hop/bu-tru-cong-no'` → `constants/constants.ts`.

### 1.1. Bảng endpoint đề xuất

| # | Mục đích | Method · Path | Query key | Trạng thái |
|---|---|---|---|---|
| E1 | Lookup mở màn: đối tượng vừa là KH vừa là NCC · TK con của 131 · TK con của 331 · loại tiền · **đồng tiền hạch toán** · **cấu hình TK chênh lệch tỷ giá lãi/lỗ** | `POST {BASE}/lookup` | `['buTruCongNo','lookup']` | ❌ chưa có |
| E2 | **Lấy dữ liệu** — nạp 2 bảng chứng từ | `POST {BASE}/lay-du-lieu` | `['buTruCongNo','layDuLieu', req]` | ❌ chưa có |
| E3 | **Lưu** / **Lưu và ghi sổ** (MỘT request, MỘT transaction) | `POST {BASE}` | mutation | ❌ chưa có |
| E4 | **Xem chi tiết** | `GET {BASE}/{id}` | `['buTruCongNo','detail', id]` | ❌ chưa có |
| E5 | **Ghi sổ** | `POST {BASE}/{id}/ghi-so` | mutation | ❌ chưa có |
| E6 | **Bỏ ghi sổ** | `POST {BASE}/{id}/bo-ghi-so` | mutation | ❌ chưa có |
| E7 | **Xóa** (xóa mềm) | `DELETE {BASE}/{id}` | mutation | ❌ chưa có |
| E8 | Danh sách Phiếu KTTH (chứa chứng từ bù trừ) | `POST /api/tong-hop/phieu-ke-toan-tong-hop/search` | thuộc module Phiếu KTTH | ❌ chưa có · **ngoài phạm vi** (D3) |

E5/E6 khai qua `ChungTuEndpoints` (`base/domainKit/chungTu/api/ChungTuDescriptor.ts:37`) chứ không
nhúng cứng trong engine — đổi quy ước URL của BE = sửa một dòng.

### 1.2. E1 — Lookup

```jsonc
// Response .data
{
  "dongTienHachToanId": "VND",                       // quyết định coQuyDoi của toàn bộ màn
  "loaiTien":    [{ "id": "VND", "ma": "VND", "ten": "Việt Nam Đồng" }],
  "taiKhoanPhaiThu": [{ "id": "…", "so": "1311", "ten": "Phải thu KH trong nước" }],
  "taiKhoanPhaiTra": [{ "id": "…", "so": "3311", "ten": "Phải trả NCC trong nước" }],
  "cauHinhChenhLechTyGia": { "taiKhoanLaiId": "515", "taiKhoanLoId": "635" }  // null nếu chưa cấu hình
}
```

`cauHinhChenhLechTyGia = null` ⇒ FE chặn sớm ở [popup 02](02-popup-bu-tru-cong-no.md) với
`MSG_..._016`. **Nếu BE không cấp trường này**, việc kiểm lùi hết về bước Lưu (E3) — phải nói rõ với
BA vì UC yêu cầu chặn **ngay khi bấm Bù trừ** (`UC_BTCN_ThemMoi.md:25`).

⚠ Đối tượng **không** nằm trong lookup này — combogrid Đối tượng tìm kiếm **server-side** theo BR5,
cần endpoint riêng của danh mục đối tượng có cờ *"vừa là khách hàng vừa là nhà cung cấp"*.
→ **cần BE xác nhận** endpoint và tên cờ.

### 1.3. E2 — Lấy dữ liệu (⭐ quan trọng nhất)

```jsonc
// Request
{
  "doiTuongId":        "…",
  "taiKhoanPhaiThuId": "…",
  "taiKhoanPhaiTraId": "…",
  "ngayBuTru":         "2026-01-31",
  "loaiTienId":        "USD"
}
// Response .data
{
  "phaiThu": [ /* DongBuTru[] */ ],
  "phaiTra": [ /* DongBuTru[] */ ]
}
```

Một `DongBuTru`:

```jsonc
{
  "id":             "…",              // id dòng công nợ (khoá của bảng)
  "chungTuId":      "…",              // để mở chứng từ gốc
  "loaiChungTu":    "CTBH",           // mã BR09 — BE trả kèm tên hiển thị
  "tenLoaiChungTu": "Bán hàng dịch vụ - chưa thanh toán",
  "ngayHachToan":   "2026-03-07",     // ⚠ C5 — chỉ Figma có, xác nhận ở Q4.1
  "ngayChungTu":    "2026-03-07",
  "soChungTu":      "BH47.00421",
  "soHoaDon":       "132",
  "hoaDonId":       "…",              // null nếu chưa có hóa đơn
  "hanThanhToan":   "2026-04-07",
  "dienGiai":       "Bán hàng VIETTEL - Chi nhánh Hà Nội",
  "tyGia":          1.2,              // decimal(18,6) — 1 khi Loại tiền = ĐTHT
  "soTien":         9900000,          // decimal(18,2) VND · (18,4) ngoại tệ
  "soDu":           8697248           // Số chưa thu (phải thu) / Số còn nợ (phải trả)
}
```

**Ba điểm phải chốt với BE:**

| # | Vấn đề | Vì sao quan trọng |
|---|---|---|
| A1 | **Trả toàn bộ hay phân trang?** Kế hoạch giả định **trả toàn bộ** (D6) | BR02 bắt phân bổ trên toàn bộ danh sách đã nạp; tick phải sống qua trang. Nếu BE bắt phân trang server-side thì **phải** có endpoint phân bổ server-side thay thế |
| A2 | **Tên trường số dư**: một tên chung `soDu` cho cả 2 bên, hay `soChuaThu` / `soConNo` riêng? | Quyết định `fields/buTruColumns.ts` có `name` động hay không. Đề xuất: **`soDu` chung** — hai bảng dùng chung một component (D5), chỉ khác **tiêu đề cột** |
| A3 | `soChuaThu` / `soConNo` **do BE tính** (công thức nhiều nguồn — `SCR_BTCN_BuTru.md:43,74`) | FE **không** tự tính. Khẳng định lại để không ai cài lại công thức ở FE |

**FE tự tính** (không có trên wire): mọi cột `…QuyDoi` = `giá trị × tyGia`, làm tròn theo BR7 —
`helpers/quyDoi.ts`.

### 1.4. E3 — Lưu / Lưu và ghi sổ

```jsonc
// Request body
{
  "ghiSo": false,                        // ⭐ cờ "Lưu và ghi sổ" — TÊN CẦN BE CHỐT
  "loaiPhieu": "BU_TRU_CONG_NO",         // LoaiPhieu = 5 theo ldm-KTTH
  "doiTuongId": "…",
  "taiKhoanPhaiThuId": "…",
  "taiKhoanPhaiTraId": "…",
  "ngayBuTru":     "2026-01-31",
  "ngayHachToan":  "2026-01-31",
  "ngayChungTu":   "2026-01-31",
  "soChungTu":     "BTCN-2026-7251",
  "moTa":          "Bù trừ công nợ phải thu, phải trả với VIETTEL …",
  "loaiTienId":    "USD",
  "soTienBuTru":   100,

  "hachToan": [                          // 1 hoặc 2 dòng — helpers/hachToan.ts dựng
    { "stt": 1, "moTa": "Bù trừ công nợ phải thu, phải trả",
      "taiKhoanNoId": "331", "taiKhoanCoId": "131",
      "soTien": 100, "soTienQuyDoi": 2450000 },
    { "stt": 2, "moTa": "Xử lý chênh lệch tỷ giá",
      "taiKhoanNoId": "635", "taiKhoanCoId": "131",
      "soTien": 0,   "soTienQuyDoi": 50000 }
  ],

  "capGhep": [                           // helpers/ghepCap.ts dựng
    { "stt": 1,
      "chungTuPhaiThuId": "…", "soChuaThu": 8697248,
      "soTienBuTruPhaiThu": 3000000, "soTienBuTruPhaiThuQuyDoi": 75000000,
      "chungTuPhaiTraId": "…", "soConNo":  9900000,
      "soTienBuTruPhaiTra": 3000000, "soTienBuTruPhaiTraQuyDoi": 73500000,
      "chenhLechTyGia": 1500000 }
  ]
}
```

**⭐ MỘT request** — không gọi Lưu rồi gọi Ghi sổ thành 2 request. Chỗ khai tên cờ đã có sẵn trong
engine: `ChungTuDescriptor.luuGhiSoField` (`base/domainKit/chungTu/api/ChungTuDescriptor.ts:174-181`).

⚠ **Nhưng "một request" ≠ "một transaction" — điểm này BA và code nói ngược nhau (Q11):**

| Nguồn | Khi bước ghi sổ hỏng (`MSG_..._018`) |
|---|---|
| Kernel (`ChungTuDescriptor.ts:174-181` dẫn `ChungTuTemplate.java:43-44`) | **Rollback cả lượt** — không có chứng từ nào được lưu |
| `AD_BTCN_ThemMoi.puml` + `UC_BTCN_ThemMoi.md:122,135` | **Giữ lại** chứng từ ở trạng thái *Chưa ghi sổ* |

**Phải chốt với BE, vì nó đổi hình dạng response lỗi:**

| Phương án | Response khi ghi sổ hỏng | FE làm gì |
|---|---|---|
| **Nguyên tử** | `4xx` + mã lỗi, **không** có `id` | Giữ popup mở, người dùng sửa rồi bấm lại |
| **2 pha** (BA đang mô tả) | `2xx`/`4xx` + **`id` của chứng từ đã lưu** + mã lỗi `SO_DU_DA_THAY_DOI` | **Đóng popup** (nếu không sẽ tạo chứng từ trùng khi bấm Lưu lần hai), toast `MSG_..._001` rồi `MSG_..._018`, invalidate danh sách |

Nếu chốt **2 pha**, response **bắt buộc** phải mang `id` — thiếu nó thì FE không có cách nào phân biệt
"chưa lưu gì" với "đã lưu nhưng chưa ghi sổ", và người dùng sẽ tạo trùng. Chi tiết hệ quả lên UI:
[03 §7.2](03-popup-chung-tu-bu-tru-them-moi.md).

**Cần BE chốt:** tên cờ (`ghiSo` / `luuVaGhiSo` / …) · có gửi `capGhep` từ FE hay BE tự dựng lại từ
danh sách chứng từ + số tiền · có gửi `hachToan` từ FE hay BE tự sinh bút toán.
**Khuyến nghị:** BE tự dựng lại và **đối chiếu** với dữ liệu FE gửi — FE tính để hiển thị, BE tính để
ghi sổ; lệch nhau thì BE từ chối. Tránh cảnh FE là nguồn sự thật của bút toán.

Response `.data`: chứng từ vừa lưu (shape của E4), tối thiểu có `id`, `soChungTu`, `trangThai`, `updatedAt`.

### 1.5. E4 — Xem chi tiết

```jsonc
{
  "id": "…", "soChungTu": "BTCN-20895048",
  "trangThai": "Chưa ghi sổ",            // ⭐ chuỗi wire — KHÔNG hardcode ở FE, đi qua BanDoTrangThai
  "updatedAt": "2026-01-31T08:00:00Z",   // token khoá lạc quan (BR12) — mang theo khi Xóa/Ghi sổ

  "doiTuongId": "…", "tenDoiTuong": "VIETTEL - Chi nhánh Hà Nội",
  "taiKhoanPhaiThuId": "131", "taiKhoanPhaiTraId": "331",
  "ngayBuTru": "…", "ngayHachToan": "…", "ngayChungTu": "…",
  "moTa": "…", "loaiTienId": "USD", "soTienBuTru": 100,

  "thamChieu": [ { "chungTuId": "…", "soChungTu": "BH47.00421", "loaiChungTu": "CTBH" } ],
  "hachToan":  [ /* như E3, thêm tenTaiKhoanNo / tenTaiKhoanCo để hiển thị */ ],
  "capGhep":   [ /* như E3, thêm đủ trường hiển thị của 2 nhóm cột (xem file 03 §6) */ ]
}
```

**`capGhep` trong E4 phải đủ trường để render tab Chứng từ công nợ** — mỗi phần tử cần cả nhóm phải
thu lẫn nhóm phải trả: `loaiChungTu`, `ngayChungTu`, `soChungTu`, `soHoaDon`, `hanThanhToan`,
`soTien`, `soChuaThu`/`soConNo`, `soTienBuTru…`, `tyGia` (để FE tính cột quy đổi). Đây là **số liệu
tại thời điểm bù trừ** (`SCR_BTCN_ChungTu_ThemMoi.md:74,86`), **không** phải số dư hiện tại ⇒ BE
snapshot khi lưu.

**Chuỗi trạng thái**: BE trả tiếng Việt của `CHECK` constraint. FE **cấm hardcode** — khai
`BanDoTrangThai` (`base/domainKit/chungTu/index.ts:12-31`,
`base/domainKit/chungTu/api/ChungTuDescriptor.ts:151`), và giải mã nhãn hiển thị bằng `statusRegistry`.

### 1.6. E5 · E6 · E7

| | Body | Response |
|---|---|---|
| E5 Ghi sổ | `{ "updatedAt": "…" }` | chứng từ sau khi ghi sổ (shape E4) |
| E6 Bỏ ghi | `{ "updatedAt": "…" }` | chứng từ sau khi bỏ ghi (shape E4) |
| E7 Xóa | `{ "updatedAt": "…" }` (token trong body — như `chungTuBanHangQueries.useDelete`) | `{ "id": "…" }` |

Mọi lỗi nghiệp vụ đi qua mã lỗi để FE map i18n, **không** dựa vào chuỗi tiếng Việt:

| Mã lỗi đề xuất | Message hiển thị |
|---|---|
| `KY_DA_KHOA` | `MSG_..._019` (có tham số `{ngayKhoaSo}`) |
| `SO_CHUNG_TU_TRUNG` | `MSG_..._015` |
| `SO_DU_DA_THAY_DOI` | `MSG_..._018` |
| `CHUA_CAU_HINH_TK_CHENH_LECH` | `MSG_..._016` |
| `KHONG_TIM_THAY` | `MSG_..._021` |
| *(7 mã kernel)* | `moTaLoiChungTu` (`base/domainKit/chungTu/index.ts:52-54`) |

### 1.7. Zod schema dự kiến — `api/model.ts`

```ts
import { z } from 'zod'

export const dongBuTruSchema = z.object({
  id: z.string(),
  chungTuId: z.string(),
  loaiChungTu: z.string(),
  tenLoaiChungTu: z.string(),
  ngayHachToan: z.string(),              // ISO date — FE format bằng @core
  ngayChungTu: z.string(),
  soChungTu: z.string(),
  soHoaDon: z.string().nullable(),
  hoaDonId: z.string().nullable(),
  hanThanhToan: z.string().nullable(),
  dienGiai: z.string().nullable(),
  tyGia: z.number(),
  soTien: z.number(),
  soDu: z.number(),                      // Số chưa thu (phải thu) / Số còn nợ (phải trả) — A2
})
export type DongBuTru = z.infer<typeof dongBuTruSchema>

export const layDuLieuResponseSchema = z.object({
  phaiThu: z.array(dongBuTruSchema),
  phaiTra: z.array(dongBuTruSchema),
})

export const dongHachToanSchema = z.object({
  stt: z.number(),
  moTa: z.string().nullable(),
  taiKhoanNoId: z.string(),
  tenTaiKhoanNo: z.string().nullable(),
  taiKhoanCoId: z.string(),
  tenTaiKhoanCo: z.string().nullable(),
  soTien: z.number(),
  soTienQuyDoi: z.number().nullable(),
})

export const capGhepSchema = z.object({ /* … xem §1.5 … */ })

export const chungTuBuTruSchema = z.object({
  id: z.string(),
  soChungTu: z.string(),
  trangThai: z.string(),                 // chuỗi wire — giải mã qua BanDoTrangThai
  updatedAt: z.string(),
  // … phần còn lại của §1.5 …
  hachToan: z.array(dongHachToanSchema),
  capGhep: z.array(capGhepSchema),
})
export type ChungTuBuTru = z.infer<typeof chungTuBuTruSchema>
```

Luật type safety (`client/CLAUDE.md:443-482`): **không `any`, không `@ts-ignore`**; mọi dữ liệu từ
ngoài vào **phải Zod `parse`**, không ép kiểu.

### 1.8. Trạng thái API — tóm tắt nợ

| Endpoint | Có thật? | Hệ quả |
|---|:--:|---|
| E1 … E7 | ❌ **không có endpoint nào** | ⇒ `api/mock.ts` tồn tại tạm. **Còn `mock.ts` = còn nợ** (`docs/fe-khung-kien-truc-chuan.md:163`) — phải gỡ khi BE lên |
| E8 (danh sách Phiếu KTTH) | ❌ | Ngoài phạm vi (D3), thuộc epic PMKT-E-09980 |
| Endpoint danh mục **Đối tượng** cho combogrid | ❓ chưa xác định | Cần BE cho biết endpoint + cờ lọc "vừa KH vừa NCC" |
| Endpoint **cấu hình TK chênh lệch tỷ giá** | ❓ chưa xác định | Không có thì `MSG_..._016` lùi về bước Lưu (mất yêu cầu chặn sớm của UC) |

**Mã chức năng thì đã có** ở BE: `PHIEU_KE_TOAN = "PhieuKeToan"` và `BU_TRU_CONG_NO = "BuTruCongNo"`
(`cell-app/src/main/java/vn/vtt/pmkt/cell/common/constant/MaChucNang.java:354,366`) — nhưng chưa có
controller nào tiêu thụ chúng, nên **tên động từ** (`.Create`, `.Post`, `.Unpost`, `.Delete`,
`.View.Detail`) vẫn là **giả định theo tài liệu BA**.

---

## 2. Hằng số nghiệp vụ — `constants/constants.ts`

Mọi số/chuỗi nghiệp vụ là constant có tên (luật 1). SCREAMING_SNAKE_CASE.

| Hằng | Giá trị | Nguồn |
|---|---|---|
| `BU_TRU_CONG_NO_BASE` | `'/api/tong-hop/bu-tru-cong-no'` | §1.0 |
| `TK_PHAI_THU_MAC_DINH` | `'131'` | `SCR_BTCN_BuTru.md:29` |
| `TK_PHAI_TRA_MAC_DINH` | `'331'` | `SCR_BTCN_BuTru.md:30` |
| `LOAI_NGHIEP_VU` | `{ BU_TRU_CONG_NO: 'BU_TRU_CONG_NO' }` | `3.crud-matrix.md:24` (LoaiPhieu = 5) |
| `PAGE_SIZE_MAC_DINH` | `10` | Figma vẽ `10 / trang` ở 2 bảng (BR1 mặc định là 20 — **lệch có chủ đích theo Figma**, ghi rõ ở đây) |
| `PAGE_SIZE_OPTIONS` | `[10, 20, 50, 100]` | BR1 |
| `MAX_LEN_LY_DO` | `500` | `SCR_BTCN_ChungTu_ThemMoi.md:20` |
| `MAX_LEN_SO_CHUNG_TU` | `50` | `SCR_BTCN_ChungTu_ThemMoi.md:26`; BR20.2 |
| `MAX_LEN_DIEN_GIAI` | `500` | `SCR_BTCN_ChungTu_ThemMoi.md:42` |
| `TAB_KEY` | `{ HACH_TOAN: 'hachToan', CHUNG_TU_CONG_NO: 'chungTuCongNo', DINH_KEM: 'dinhKem', THAM_CHIEU: 'thamChieu' }` | Figma `41383:670167` |
| `COLUMN_CONFIG_KEY` | `{ PHAI_THU: 'buTruCongNo.phaiThu', PHAI_TRA: 'buTruCongNo.phaiTra' }` | BR30 |
| `DATE_FORMAT` | `'DD/MM/YYYY'` | Figma `31/01/2026` |
| `SCALE` | `{ TIEN_VND: 2, TIEN_NGOAI_TE: 4, TY_GIA: 6 }` | **BR7.1** |

⚠ `PAGE_SIZE_MAC_DINH = 10` **lệch BR1** (mặc định 20 bản ghi/trang). Figma vẽ `10 / trang` ở cả 2
bảng của popup 02. Epic thắng trong phạm vi epic, nhưng **phải nói rõ đang lệch BR1** → thêm vào
danh mục hỏi BA.

---

## 3. Bảng khoá i18n — namespace `buTruCongNo`

MỘT namespace cho cả module; hai từ điển khớp khoá **1-1**. Giá trị `vi` giữ **nguyên văn** BA/BR.
Chuỗi động dùng interpolation, **không** cộng chuỗi.

### 3.1. Khung & menu

| Khoá | `vi` | `en` |
|---|---|---|
| `menu.buTruCongNo` | Bù trừ công nợ | Debt offsetting |
| `trangThai.chuaGhiSo` | Chưa ghi sổ | Unposted |
| `trangThai.daGhiSo` | Đã ghi sổ | Posted |
| `comingSoon` | Tính năng đang được phát triển | This feature is under development |

### 3.2. Popup 1 — thiết lập bù trừ (`buTru.*`)

| Khoá | `vi` | `en` |
|---|---|---|
| `buTru.title` | Bù trừ công nợ | Debt offsetting |
| `buTru.filter.doiTuong` | Đối tượng | Partner |
| `buTru.filter.tkPhaiThu` | TK phải thu | Receivable account |
| `buTru.filter.tkPhaiTra` | TK phải trả | Payable account |
| `buTru.filter.ngayBuTru` | Ngày bù trừ | Offset date |
| `buTru.filter.loaiTien` | Loại tiền | Currency |
| `buTru.filter.layDuLieu` | Lấy dữ liệu | Load data |
| `buTru.soTienBuTru` | Số tiền bù trừ | Offset amount |
| `buTru.bangPhaiThu.title` | Chứng từ phải thu | Receivable documents |
| `buTru.bangPhaiTra.title` | Chứng từ phải trả | Payable documents |
| `buTru.timKiem` | Tìm theo số chứng từ, số hóa đơn | Search by document no., invoice no. |
| `buTru.cot.ngayHachToan` | Ngày hạch toán | Posting date |
| `buTru.cot.ngayChungTu` | Ngày chứng từ | Document date |
| `buTru.cot.soChungTu` | Số chứng từ | Document no. |
| `buTru.cot.soHoaDon` | Số hóa đơn | Invoice no. |
| `buTru.cot.hanThanhToan` | Hạn thanh toán | Due date |
| `buTru.cot.dienGiai` | Diễn giải | Description |
| `buTru.cot.tyGia` | Tỷ giá | Exchange rate |
| `buTru.cot.soTien` | Số tiền | Amount |
| `buTru.cot.soTienQuyDoi` | Số tiền quy đổi | Converted amount |
| `buTru.cot.soChuaThu` | Số chưa thu | Uncollected amount |
| `buTru.cot.soChuaThuQuyDoi` | Số chưa thu quy đổi | Converted uncollected amount |
| `buTru.cot.soConNo` | Số còn nợ | Outstanding amount |
| `buTru.cot.soConNoQuyDoi` | Số còn nợ quy đổi | Converted outstanding amount |
| `buTru.cot.soTienBuTru` | Số tiền bù trừ | Offset amount |
| `buTru.cot.soTienBuTruQuyDoi` | Số tiền bù trừ quy đổi | Converted offset amount |
| `buTru.cot.loaiChungTu` | Loại chứng từ | Document type |
| `buTru.tong` | Tổng: | Total: |
| `buTru.nut.buTru` | Bù trừ | Offset |
| `buTru.nut.huy` | Hủy | Cancel |

### 3.3. Popup 2 — chứng từ (`chungTu.*`)

| Khoá | `vi` | `en` |
|---|---|---|
| `chungTu.title` | Phiếu kế toán tổng hợp ⚠**C1/Q3** | General accounting voucher |
| `chungTu.titleXem` | Chứng từ bù trừ công nợ {{soChungTu}} | Debt offsetting document {{soChungTu}} |
| `chungTu.loaiNghiepVu` | Loại nghiệp vụ | Transaction type |
| `chungTu.loaiNghiepVuBuTru` | Bù trừ công nợ | Debt offsetting |
| `chungTu.doiTuong` | Đối tượng | Partner |
| `chungTu.lyDo` | Lý do | Reason |
| `chungTu.lyDoMacDinh` | Bù trừ công nợ phải thu, phải trả với {{tenDoiTuong}} | Offsetting receivables and payables with {{tenDoiTuong}} |
| `chungTu.tkPhaiThu` | TK phải thu | Receivable account |
| `chungTu.tkPhaiTra` | TK phải trả | Payable account |
| `chungTu.ngayBuTru` | Ngày bù trừ | Offset date |
| `chungTu.ngayHachToan` | Ngày hạch toán | Posting date |
| `chungTu.ngayChungTu` | Ngày chứng từ | Document date |
| `chungTu.soChungTu` | Số chứng từ | Document no. |
| `chungTu.thamChieu` | Tham chiếu | References |
| `chungTu.soTienBuTru` | Số tiền bù trừ | Offset amount |
| `chungTu.loaiTien` | Loại tiền | Currency |
| `chungTu.tab.hachToan` | Hạch toán | Journal entries |
| `chungTu.tab.chungTuCongNo` | Chứng từ công nợ | Debt documents |
| `chungTu.tab.dinhKem` | Đính kèm | Attachments |
| `chungTu.tab.thamChieu` | Tham chiếu | References |
| `chungTu.cotHachToan.stt` | # | # |
| `chungTu.cotHachToan.dienGiai` | Diễn giải | Description |
| `chungTu.cotHachToan.tkNo` | TK Nợ | Debit account |
| `chungTu.cotHachToan.tkCo` | TK Có | Credit account |
| `chungTu.cotHachToan.soTien` | Số tiền | Amount |
| `chungTu.cotHachToan.soTienQuyDoi` | Số tiền quy đổi | Converted amount |
| `chungTu.dongHachToan1` | Bù trừ công nợ phải thu, phải trả | Offsetting receivables and payables |
| `chungTu.dongHachToan2` | Xử lý chênh lệch tỷ giá | Exchange rate difference handling |
| `chungTu.nhomPhaiThu` | Chứng từ phải thu | Receivable documents |
| `chungTu.nhomPhaiTra` | Chứng từ phải trả | Payable documents |
| `chungTu.cotCongNo.soBuTru` | Số bù trừ | Offset |
| `chungTu.cotCongNo.soBuTruQuyDoi` | Số bù trừ quy đổi | Converted offset |
| `chungTu.cotCongNo.chenhLechTyGia` | Chênh lệch tỷ giá | Exchange rate difference |
| *(các cột còn lại dùng lại nhãn giống `buTru.cot.*` nhưng khai riêng để đổi độc lập)* | | |
| `chungTu.nut.huy` | Hủy | Cancel |
| `chungTu.nut.luu` | Lưu | Save |
| `chungTu.nut.luuVaGhiSo` | Lưu và ghi sổ | Save and post |
| `chungTu.nut.ghiSo` | Ghi sổ | Post |
| `chungTu.nut.boGhi` | Bỏ ghi | Unpost |
| `chungTu.nut.xoa` | Xóa | Delete |
| `chungTu.nut.dong` | Đóng | Close |

### 3.4. Popup xác nhận (`xoa.*`, `boGhi.*`)

| Khoá | `vi` | `en` |
|---|---|---|
| `xoa.title` | Xác nhận xóa | Confirm deletion |
| `xoa.dong` | Đóng | Close |
| `xoa.xacNhan` | Xác nhận | Confirm |
| `boGhi.title` | Xác nhận bỏ ghi sổ | Confirm unposting |

### 3.5. Message — `msg.*` (**nguyên văn** `6.messages.md`)

| Khoá | Mã BA | `vi` (nguyên văn) | `en` |
|---|---|---|---|
| `msg.luuThanhCong` | `_001` | Lưu chứng từ bù trừ công nợ thành công | Debt offsetting document saved successfully |
| `msg.ghiSoThanhCong` | `_002` | Ghi sổ chứng từ bù trừ công nợ thành công | Debt offsetting document posted successfully |
| `msg.boGhiThanhCong` | `_003` | Bỏ ghi chứng từ bù trừ công nợ thành công | Debt offsetting document unposted successfully |
| `msg.xoaThanhCong` | `_004` | Xóa chứng từ bù trừ công nợ thành công | Debt offsetting document deleted successfully |
| `msg.khongCoQuyen` | `_005` | Bạn không có quyền truy cập chức năng này | You do not have permission to access this function |
| `msg.thieuTruongBatBuoc` | `_006` | Vui lòng nhập đầy đủ các trường bắt buộc | Please fill in all required fields |
| `msg.tongKhongBang` | `_007` | Tổng số tiền bù trừ ở 2 bảng (Chứng từ phải thu và Chứng từ phải trả) phải bằng nhau | The total offset amounts in both tables (Receivable and Payable documents) must be equal |
| `msg.chuaChonPhaiThu` | `_008` | Vui lòng chọn ít nhất 1 chứng từ phải thu | Please select at least 1 receivable document |
| `msg.chuaChonPhaiTra` | `_009` | Vui lòng chọn ít nhất 1 chứng từ phải trả | Please select at least 1 payable document |
| `msg.vuotSoChuaThu` | `_010` | Số tiền bù trừ không được vượt quá Số chưa thu | The offset amount must not exceed the uncollected amount |
| `msg.vuotSoConNo` | `_011` | Số tiền bù trừ không được vượt quá Số còn nợ | The offset amount must not exceed the outstanding amount |
| `msg.soTienAm` | `_012` | Số tiền bù trừ không được âm | The offset amount must not be negative |
| `msg.chuaLayDuLieu` | `_013` | Vui lòng bấm "Lấy dữ liệu" để nạp chứng từ | Please click "Load data" to load documents |
| `msg.thieuSoChungTu` | `_014` | Vui lòng nhập Số chứng từ | Please enter the document number |
| `msg.trungSoChungTu` | `_015` | Số chứng từ đã tồn tại. Vui lòng nhập số khác | The document number already exists. Please enter another one |
| `msg.chuaCauHinhTkChenhLech` | `_016` | Chưa cấu hình tài khoản xử lý chênh lệch tỷ giá lãi/lỗ. Vui lòng kiểm tra cấu hình | The exchange-rate gain/loss accounts are not configured. Please check the configuration |
| `msg.loiXuLy` | `_017` | Lỗi khi xử lý chứng từ bù trừ công nợ | An error occurred while processing the debt offsetting document |
| `msg.soDuDaThayDoi` | `_018` | Số dư công nợ của chứng từ đã thay đổi. Vui lòng lấy lại dữ liệu và thực hiện lại | The document's debt balance has changed. Please reload the data and try again |
| `msg.kyDaKhoa` | `_019` | Chứng từ thuộc kỳ đã khóa sổ {{ngayKhoaSo}}. Không thể thực hiện | The document belongs to a closed period {{ngayKhoaSo}}. The action cannot be performed |
| `msg.loiXoa` | `_020` | Lỗi khi xóa chứng từ bù trừ công nợ | An error occurred while deleting the debt offsetting document |
| `msg.khongTimThay` | `_021` | Không tìm thấy chứng từ bù trừ công nợ | Debt offsetting document not found |
| `msg.loiTaiDanhSach` | `_022` | Lỗi khi tải danh sách chứng từ bù trừ công nợ | An error occurred while loading the debt offsetting document list |
| `msg.chanBoGhiChungTuCongNo` | `_101` | Chứng từ đã tham gia bù trừ công nợ. Vui lòng xử lý chứng từ bù trừ công nợ trước khi bỏ ghi sổ | This document is part of a debt offset. Please handle the debt offsetting document before unposting |
| `msg.xacNhanBoGhi` | `_102` | Bạn có chắc chắn muốn bỏ ghi sổ chứng từ bù trừ công nợ? Hệ thống sẽ hoàn trả số dư công nợ của các chứng từ liên quan | Are you sure you want to unpost this debt offsetting document? The system will restore the debt balances of the related documents |
| `msg.xacNhanXoa` | `_103` | Bạn có chắc chắn muốn xóa chứng từ bù trừ công nợ '{{soChungTu}}'? Thao tác này không thể hoàn tác | Are you sure you want to delete debt offsetting document '{{soChungTu}}'? This action cannot be undone |
| `msg.khongCoDuLieu` | `_201` | Không có dữ liệu | No data |

⚠ `msg.chanBoGhiChungTuCongNo` (`_101`) khai ở đây **cho đủ bộ**, nhưng nơi **hiển thị** nó là màn
chứng từ bán hàng / mua hàng — ngoài module này (**Q8**). Khi ticket đó làm, chữ nên chuyển sang
namespace của module tương ứng, hoặc module đó `t('buTruCongNo:msg.chanBoGhiChungTuCongNo')`
(hợp lệ — i18n không bị luật tầng chặn).

### 3.6. Chữ khung của component `@base`

`CommonListTable`, `CommonComboGrid`, `CommonConfirmModal` đều nhận `texts` — gom ở `fields/texts.ts`
(`chungTuBanHang` làm y hệt: `features/banHang/chungTuBanHang/fields/texts.ts`), lấy chữ từ cùng
namespace này. Không mở namespace thứ hai (luật `client/CLAUDE.md:362-370`).

---

## 4. Mã quyền — `constants/permissions.ts` (BR25)

```ts
/**
 * Mã chức năng `BuTruCongNo` — đã seed ở BE (MaChucNang.java:366) nhưng CHƯA có controller nào
 * tiêu thụ ⇒ động từ dưới đây là GIẢ ĐỊNH theo tài liệu BA, đối chiếu lại khi BE lên.
 */
export const BU_TRU_CONG_NO_PERM = {
  /** Gác route + gác menu — UC_BTCN_ThemMoi.md:12. */
  create: 'BuTruCongNo.Create',
} as const

/**
 * Chứng từ kết quả là Phiếu kế toán tổng hợp ⇒ vòng đời đi theo mã chức năng `PhieuKeToan`
 * (MaChucNang.java:354). Khớp tài liệu BA của cả epic 14294 lẫn epic 09980.
 */
export const PHIEU_KE_TOAN_PERM = {
  view:       'PhieuKeToan.View',
  viewDetail: 'PhieuKeToan.View.Detail',
  delete:     'PhieuKeToan.Delete',
  ghiSo:      'PhieuKeToan.Post',
  boGhiSo:    'PhieuKeToan.Unpost',
} as const
```

| Hành động | Quyền cần | Nguồn |
|---|---|---|
| Mở màn Bù trừ công nợ (menu + URL) | `BuTruCongNo.Create` | `UC_BTCN_ThemMoi.md:12`, `SCR_BTCN_BuTru.md:17` |
| Lưu chứng từ | `BuTruCongNo.Create` | `SCR_BTCN_ChungTu_ThemMoi.md:11` |
| **Lưu và ghi sổ** | `BuTruCongNo.Create` **VÀ** `PhieuKeToan.Post` | một request vừa lưu vừa ghi sổ (§1.4) |
| Xem danh sách | `PhieuKeToan.View` | `SCR_BTCN_DanhSach.md:13` |
| Xem chi tiết | `PhieuKeToan.View.Detail` | `SCR_BTCN_ChungTu_XemChiTiet.md:19` |
| Ghi sổ | `PhieuKeToan.Post` | `SCR_BTCN_ChungTu_XemChiTiet.md:50` |
| Bỏ ghi | `PhieuKeToan.Unpost` | `SCR_BTCN_ChungTu_XemChiTiet.md:40` |
| Xóa | `PhieuKeToan.Delete` | `SCR_BTCN_PopupXacNhanXoa.md:11` |

**BR25.2** — thiếu quyền thì **ẩn** nút, **không** disable. URL không có quyền → trang 403 (BR27).

---

## 5. Đường dẫn — `constants/paths.ts`

```ts
/**
 * TIER 3 features/tongHop/buTruCongNo · route slug. Nằm ở `constants/`, KHÔNG sau `index.ts`, để
 * `features/tongHop/routes.tsx` deep-import được mà không kéo page graph vào chunk eager (§7).
 * Slug giữ chính tả tiếng Việt không dấu bất kể ngôn ngữ UI (URL là hợp đồng sản phẩm).
 */
export const BU_TRU_CONG_NO_PATHS = {
  buTruCongNo: '/tong-hop/bu-tru-cong-no',
} as const
```

**Deep-import CỐ Ý** hai file `constants/paths.ts` và `constants/permissions.ts` từ ngoài module —
đây là ngoại lệ duy nhất được phép, giữ chunk eager của `routes.tsx` và menu shell không kéo theo page
graph (`client/CLAUDE.md:336-344`):

```ts
import { BU_TRU_CONG_NO_PATHS } from '@features/tongHop/buTruCongNo/constants/paths.ts'
import { BU_TRU_CONG_NO_PERM }  from '@features/tongHop/buTruCongNo/constants/permissions.ts'
```

⚠ **Không** đặt tên `TONG_HOP_PATHS` — tên đó đã bị `khoaSo` dùng
(`features/tongHop/khoaSo/constants/paths.ts:9-11`), và leaf **không** với được leaf anh em
(`client/CLAUDE.md:108-109`). Mỗi module một bộ hằng riêng; khi domain có ≥2 module cần gộp thì mới
tính chuyện đẩy xuống `features/tongHop/_shared/`.

---

## 6. `index.ts` — cửa ra duy nhất

```ts
/**
 * TIER 3 features/tongHop/buTruCongNo · cửa ra DUY NHẤT (§5) và là FILE DUY NHẤT ở gốc module.
 * `paths.ts` / `permissions.ts` KHÔNG đi qua barrel này (deep-import cố ý — §5 của file 06).
 */
export { BuTruCongNoPage } from './pages/BuTruCongNoPage.tsx'

/* Bàn giao cho module Phiếu KTTH (epic 09980) — xem 01 §8.
   Khi module đó lên, ba thứ dưới đây chuyển xuống features/tongHop/_shared/. */
export { ChungTuBuTruModal } from './components/ChungTuBuTruModal.tsx'
export { useBuTruActions } from './hooks/useBuTruActions.ts'
export type { ChungTuBuTru } from './fields/types.ts'
```
