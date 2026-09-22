# 08 · Hợp đồng API · i18n · hằng số · quyền

| | |
|---|---|
| Module | `client/src/base/domainKit/mauIn/` |
| Namespace i18n | **`mauIn`** — MỘT namespace cho cả module |
| Plan BE | `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-api/` — **CHƯA LẬP** |

---

## 1. Hợp đồng với BE

> ⚠ **Toàn bộ mục này là ĐỀ XUẤT chờ `/plan-be` chốt.** Endpoint hiện có
> (`cell-app/src/main/java/vn/vtt/pmkt/cell/mau_in/internal/controller/MauInController.java`,
> FE `client/src/base/domainKit/mauIn/api/mauInApi.ts:28` `MAU_IN_ENDPOINT='/api/mau-in'`)
> **không đúng hợp đồng này** — thiếu `maNghiepVu`, thiếu nhánh `chung`, thiếu kho trường.

### 1.1 Danh sách endpoint

| Mã | Method · Path | Dùng ở đâu | Query key | Trạng thái |
|---|---|---|---|---|
| **A1** | `GET /api/mau-in/hieu-luc?maLoaiChungTu&maNghiepVu` | mở modal Thiết lập | `mauInKeys.hieuLuc(ma, nv)` | ❌ **chưa có** (thiếu `maNghiepVu`) |
| **A2** | `PUT /api/mau-in?maLoaiChungTu&maNghiepVu` | bấm Lưu | mutation | ❌ **chưa có** |
| **A3** | `POST /api/mau-in/anh-nen` (multipart) | tải ảnh nền (chốt **C08**) | mutation | ❌ **chưa có** |
| **A4** | `DELETE /api/mau-in/anh-nen?maLoaiChungTu&maNghiepVu` | xoá ảnh nền | mutation | ❌ **chưa có** |
| **A5** | `GET /api/mau-in/du-lieu-in?chungTuId` | dữ liệu **thật** của chứng từ (`R-TLMI-217`) | `mauInKeys.duLieuIn(id)` | ⚠ có bản cũ, cần soát |
| **A6** | `GET /api/mau-in/menu?maLoaiChungTu&maNghiepVu&chungTuId` | dựng menu In (`R-TLMI-023`) + cờ cấm in (`R-TLMI-261`) | `mauInKeys.menu(…)` | ⚠ có bản cũ, cần soát |

⚠ **Q-16 — mọi API nhận CẶP `(maLoaiChungTu, maNghiepVu)`**, kể cả khi loại chứng từ hiện chỉ có một
nghiệp vụ. **Không rút gọn còn một tham số.**

⚠ **Bỏ** A7/A8/A9 của bản cũ (lịch sử phiên bản) — không có luật `R-TLMI-*` nào.

### 1.2 A1 — response mẫu

```jsonc
{
  "data": {
    "nguon": "TUY_CHINH",              // "CHUAN" | "TUY_CHINH"  — R-TLMI-007
    "phienBan": 3,                     // khoá lạc quan — chốt C06
    "mau": {                           // null khi nguon = "CHUAN"  — R-TLMI-007
      "schemaVersion": 2,
      "maLoaiChungTu": "BH",
      "maNghiepVu": "BAN_HANG_TRONG_NUOC",
      "trang": {
        // ⚠ CHỈ CÁC KHOÁ "RIÊNG". Khoá VẮNG MẶT = theo thiết lập chung (D5 · C28 · R-TLMI-037)
        "khoGiay": "A5",
        "mauChu": "#000000",           // luôn riêng — R-TLMI-064
        "nen": { "kieu": "KHUNG_VIEN", "doDam": 20 }
      },
      "dauTrang": {
        "inKhoi": true,                // riêng của mẫu — R-TLMI-076
        "dong": { "email": false }     // 7 khoá; khoá vắng = theo chung — R-TLMI-077
      },
      "truongDungChung": {             // CẤP MẪU — R-TLMI-156 · R-TLMI-164
        "diaChiGiaoHang": { "nhan": "Giao đến", "dam": true },
        "soChungTu":      { "nhan": "Số",       "dam": true }
      },
      "khoi": [                        // THỨ TỰ MẢNG = THỨ TỰ IN — R-TLMI-262
        { "id": "k1", "loai": "DAU_TRANG", "hien": true },
        { "id": "k2", "loai": "TIEU_DE", "hien": true,
          "tieuDe": { "noiDung": "Chứng từ bán hàng", "coChu": 18,
                      "can": "GIUA", "inHoa": true, "inDam": true, "dongNgayThang": true } },
        { "id": "k3", "loai": "BANG", "hien": true, "nguon": "luoiHangHoa",
          "bang": { "tenBang": "Danh sách hàng hoá", "inCotStt": true, "dongCong": true,
                    "lapTieuDe": true, "keO": "DAY_DU",
                    "cot": [
                      { "k": "maHang",    "in": true,  "nhan": "Mã hàng",   "rong": 12, "can": "TRAI",  "cong": false },
                      { "k": "tenHang",   "in": true,  "nhan": "Tên mặt hàng", "rong": 30, "can": "TRAI", "cong": false },
                      { "k": "chietKhau", "in": false, "nhan": "Chiết khấu", "rong": 10, "can": "PHAI", "cong": false }
                    ] } },
        { "id": "k4", "loai": "TU_DO", "hien": true, "ten": "Ghi chú giao hàng",
          "soDong": 2, "soCot": 2,
          "o": [                       // CHỈ Ô NEO — D7
            { "id": "o1", "dong": 0, "cot": 0, "rowSpan": 1, "colSpan": 1,
              "noiDung": { "loai": "TRUONG", "k": "diaChiGiaoHang" }, "can": "TRAI", "nghieng": false },
            { "id": "o2", "dong": 0, "cot": 1, "rowSpan": 1, "colSpan": 1,
              "noiDung": { "loai": "TRUONG", "k": "nguoiNhan" }, "can": "TRAI", "nghieng": false },
            { "id": "o3", "dong": 1, "cot": 0, "rowSpan": 1, "colSpan": 2,
              "noiDung": { "loai": "CHU_TU_DO", "chu": "Hàng dễ vỡ, xin nhẹ tay." },
              "can": "TRAI", "nghieng": true }
          ] },
        { "id": "k5", "loai": "CHU_KY", "hien": true,
          "chuKy": { "dongNgay": true, "choTrongKy": "VUA",
                     "o": [
                       { "vaiTro": "NGUOI_LAP_PHIEU", "hien": true, "tieuDe": "Người lập phiếu", "ghiChu": "(Ký, họ tên)" },
                       { "vaiTro": null, "hien": true, "tieuDe": "Thủ quỹ", "ghiChu": "(Ký, họ tên)", "tenTuDo": "Thủ quỹ" }
                     ] } }
      ]
    },
    "mauChuan": { /* … cùng hình dạng, để "Đặt lại mẫu chuẩn" — R-TLMI-016 */ },
    "chung": {                         // THIẾT LẬP CHUNG, CHỈ ĐỌC — Q3
      "khoGiay": "A4", "huongGiay": "TU_DONG", "soCotTuDongNgang": 8,
      "le": { "tren": 1, "trai": 1.5, "duoi": 1, "phai": 1 },
      "font": "TIMES_NEW_ROMAN", "coChu": 12,
      "dauTrang": { "dong": { "tenDonVi": true, "diaChi": true, "mst": true,
                              "dienThoai": true, "email": false, "taiKhoanNganHang": false, "logo": true },
                    "lapTrangSau": true },
      "hoSoDonVi": {                   // của CHI NHÁNH ghi trên chứng từ — R-TLMI-078 · Q-14
        "tenDonVi": "CÔNG TY CP CÔNG NGHỆ BIZ",
        "diaChi": "Tầng 6, Tòa nhà Tech, Số 1 Đường ABC, Phường X, Quận Y, TP Hà Nội",
        "mst": "0101234567", "dienThoai": "024 3333 6666",
        "email": "ketoan@biz.vn", "taiKhoanNganHang": "0011002233445 – Vietcombank CN Hà Nội",
        "logoUrl": null                // ⚠ Q5 — BE chưa có trường
      },
      "nguoiKy": {                     // R-TLMI-046 · R-TLMI-196
        "inTenNguoiKy": true,
        "NGUOI_LAP_PHIEU": { "tieuDe": "Người lập phiếu", "ten": "Nguyễn Văn An" },
        "KE_TOAN_TRUONG":  { "tieuDe": "Kế toán trưởng",  "ten": "Lưu Đức Huy" },
        "GIAM_DOC":        { "tieuDe": "Giám đốc",        "ten": "Lê Quang Dũng" },
        "THU_KHO":         { "tieuDe": "Thủ kho",         "ten": "Phạm Văn Kho" },
        "THU_QUY":         { "tieuDe": "Thủ quỹ",         "ten": "" }
      },
      "quyTacIn": { "choInChuaGhiSo": false, "choInDaKhoaSo": false, "congGopMatHang": true }
    },
    "khoTruong": [                     // R-TLMI-165 — danh sách PHẲNG, R-TLMI-166
      { "k": "khachHang",      "ten": "Khách hàng",      "conTrenForm": true },
      { "k": "diaChiGiaoHang", "ten": "Địa chỉ giao hàng","conTrenForm": true },
      { "k": "soTienBangChu",  "ten": "Số tiền bằng chữ", "conTrenForm": true },
      { "k": "truongCu",       "ten": "Trường cũ",        "conTrenForm": false }  // C10 — mờ + nhãn
    ],
    "luoi": [ { "nguon": "luoiHangHoa", "ten": "Bảng hàng hoá",
                "cot": [ { "k": "maHang", "ten": "Mã hàng", "kieu": "TEXT", "rongForm": 12 } ] } ]
  }
}
```

### 1.3 A2 — request

```jsonc
// PUT /api/mau-in?maLoaiChungTu=BH&maNghiepVu=BAN_HANG_TRONG_NUOC
{
  "phienBan": 3,        // khoá lạc quan — lệch ⇒ 409 + MSG_COMMON_001 (C06, L-4)
  "mau": { /* … như trên, ĐÃ qua chuanHoaMau(): xoá mọi khoá undefined (D5) */ }
}
```

| Mã HTTP | Ý nghĩa | FE làm gì |
|---|---|---|
| `200` | ghi xong | toast `MSG_101`, `danhDauDaLuu()`, invalidate `mauInKeys.hieuLuc` |
| `200` + `nguon: "CHUAN"` | mẫu **bằng** mẫu chuẩn ⇒ BE **xoá bản ghi** (chốt **C02**, `R-TLMI-021`) | như trên, badge `Đã lưu` |
| `400` | một trong `MSG_201…216` | hiện message tại chỗ |
| `403` | `MSG_PMKT-E-14549_21_002` | toast + đóng modal |
| `409` | xung đột phiên bản | `MSG_COMMON_001` + hỏi nạp lại (C06) |
| `5xx` | `MSG_PMKT-E-14549_21_003` | toast; BE đã rollback (`R-TLMI-249`) |

### 1.4 Zod — `api/model.ts`

```ts
// ⚠ LUẬT VÀNG: nhóm KẾ THỪA dùng .optional(), TUYỆT ĐỐI KHÔNG .default()  (D5 · R-TLMI-037)
const trangSchema = z.object({
  khoGiay:          z.enum(['A3','A4','A5']).optional(),
  huongGiay:        z.enum(['DOC','NGANG','TU_DONG']).optional(),
  soCotTuDongNgang: z.number().int().min(1).max(50).optional(),
  le: z.object({
    tren: z.number().min(0).max(5).optional(),
    trai: z.number().min(0).max(5).optional(),
    duoi: z.number().min(0).max(5).optional(),
    phai: z.number().min(0).max(5).optional(),
  }).optional(),
  font:   z.enum(['TIMES_NEW_ROMAN','ARIAL']).optional(),
  coChu:  z.number().int().min(8).max(20).optional(),
  // RIÊNG của mẫu — có default được
  mauChu: z.string().regex(/^#[0-9a-fA-F]{6}$/).default('#000000'),
  nen: z.object({
    kieu:   z.enum(['KHONG','KHUNG_VIEN','ANH']).default('KHONG'),
    doDam:  z.number().int().min(5).max(100).default(20),
    canAnh: z.enum(['GIUA_TRANG','TOAN_TRANG']).default('GIUA_TRANG'),
  }).default({}),
})

const noiDungOSchema = z.discriminatedUnion('loai', [
  z.object({ loai: z.literal('TRONG') }),
  z.object({ loai: z.literal('TRUONG'),     k:   z.string().min(1) }),
  z.object({ loai: z.literal('CHU_TU_DO'),  chu: z.string().max(255) }),   // R-TLMI-147
])

const oTuDoSchema = z.object({
  id: z.string(), dong: z.number().int().min(0), cot: z.number().int().min(0),
  rowSpan: z.number().int().min(1), colSpan: z.number().int().min(1),
  noiDung: noiDungOSchema,
  can: z.enum(['TRAI','GIUA','PHAI']).default('TRAI'),
  nghieng: z.boolean().default(false),
})

const khoiSchema = z.discriminatedUnion('loai', [
  khoiDauTrang, khoiTieuDe, khoiBang,
  khoiChung.extend({
    loai: z.literal('TU_DO'),
    ten:     z.string().min(1).max(60),        // R-TLMI-121
    soDong:  z.number().int().min(1).max(20),  // R-TLMI-129 · C20
    soCot:   z.number().int().min(1).max(6),   // R-TLMI-130 · C20
    o:       z.array(oTuDoSchema),
  }),
  khoiChuKy,
])

export const mauInSchema = z.object({
  schemaVersion: z.literal(2),
  maLoaiChungTu: z.string(), maNghiepVu: z.string(),
  trang: trangSchema,
  dauTrang: z.object({
    inKhoi: z.boolean().default(true),
    dong: z.object({                            // 7 khoá, VẮNG = theo chung — R-TLMI-077
      tenDonVi: z.boolean().optional(), diaChi: z.boolean().optional(),
      mst: z.boolean().optional(), dienThoai: z.boolean().optional(),
      email: z.boolean().optional(), taiKhoanNganHang: z.boolean().optional(),
      logo: z.boolean().optional(),             // R-TLMI-082 · C03
    }).default({}),
  }),
  truongDungChung: z.record(z.string(), z.object({
    nhan: z.string().max(255).optional(),       // R-TLMI-157
    dam:  z.boolean().optional(),
  })).default({}),                              // R-TLMI-156 · lọc theo R-TLMI-164
  khoi: z.array(khoiSchema).min(1),
})
```

**Không `any`, không `@ts-ignore`.** Mọi dữ liệu từ BE đi qua `mauInSchema.parse()`.

---

## 2. Trạng thái API — nợ kỹ thuật

| Endpoint | Có thật? | Nợ |
|---|---|---|
| A1 · A2 · A3 · A4 | ❌ | `api/mock.ts` đọc `test/fixtures/bh.*.json` |
| A5 · A6 | ⚠ có bản cũ, khoá thiếu `maNghiepVu` | phải sửa cùng `/plan-be` |

⚠ **Còn `api/mock.ts` = còn nợ.** Lô 6 gỡ file này. Cổng nghiệm thu cuối phải kiểm
`grep -rn "mock" client/src/base/domainKit/mauIn/api/` ⇒ rỗng.

⚠ 3 migration `V1148`-`V1150` **đã lên `origin/develop` + `origin/staging`** với khoá cũ
`(tenant, maLoaiChungTu)` (R7) ⇒ `/plan-be` phải viết **migration MỚI**, không sửa tại chỗ.

---

## 3. Bảng khoá i18n — namespace **`mauIn`**

> `vi` = **NGUYÊN VĂN tiếng Việt của BA** (từ `6.messages.md` và `02-rules.md`) — **cấm diễn đạt lại**.
> Chuỗi có `{…}` dùng interpolation, **không cộng chuỗi**.

### 3.1 `man.*` — khung màn

| Khoá | `vi` | `en` |
|---|---|---|
| `man.tieuDe` | `Thiết lập mẫu in: {{tenNghiepVu}}` | `Print template setup: {{tenNghiepVu}}` |
| `man.badge.daLuu` | `Đã lưu` | `Saved` |
| `man.badge.chuaLuu` | `Chưa lưu` | `Unsaved` |
| `man.badge.coLoi` | `Có lỗi` | `Has errors` |
| `man.nut.dong` | `Đóng` | `Close` |
| `man.nut.datLaiMauChuan` | `Đặt lại mẫu chuẩn` | `Reset to system template` |
| `man.nut.luu` | `Lưu` | `Save` |
| `man.nut.troGiup` | `Trợ giúp` | `Help` |
| `man.nut.dongModal` | `Đóng` | `Close` |

### 3.2 `boCuc.*` — cột trái

| Khoá | `vi` | `en` |
|---|---|---|
| `boCuc.tieuDe` | `BỐ CỤC MẪU` | `TEMPLATE LAYOUT` |
| `boCuc.thietLapMau` | `Thiết lập mẫu` | `Template settings` |
| `boCuc.khoi.dauTrang` | `Thông tin đầu trang` | `Page header` |
| `boCuc.khoi.tieuDe` | `Tiêu đề` | `Title` |
| `boCuc.khoi.chuKy` | `Chữ ký` | `Signatures` |
| `boCuc.badge.khoiTuDo` | `khối tự do` | `free block` |
| `boCuc.themKhoiTuDo` | `+ Thêm khối tự do` | `+ Add free block` |
| `boCuc.anHien` | `Ẩn/hiện khối` | `Show/hide block` |
| `boCuc.xoaKhoi` | `Xóa khối` | `Delete block` |
| `boCuc.chuThich1` | `Mẫu chuẩn gồm 4 loại: Thông tin đầu trang, Tiêu đề, các bảng dữ liệu và Chữ ký. Phần còn lại có thể tự thêm bằng các Khối tự do.` | *(dịch)* |
| `boCuc.chuThich2` | `Có thể thao tác ngay trên trang xem trước: kéo thả, sử dụng chuột phải thêm/xóa/gộp/tách dòng và cột tại các khối tự do` | *(dịch)* |

### 3.3 `thanhXemTruoc.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `thanhXemTruoc.hoanTac` | `Hoàn tác` | `Undo` |
| `thanhXemTruoc.lamLai` | `Làm lại` | `Redo` |
| `thanhXemTruoc.khoGiay` | `Khổ giấy` | `Paper size` |
| `thanhXemTruoc.huongGiay` | `Hướng giấy` | `Orientation` |
| `thanhXemTruoc.hienLuoiCanChinh` | `Hiện lưới căn chỉnh` | `Show alignment grid` |
| `thanhXemTruoc.thuNho` | `Thu nhỏ` | `Zoom out` |
| `thanhXemTruoc.phongTo` | `Phóng to` | `Zoom in` |
| `thanhXemTruoc.vuaKhung` | `Vừa khung` | `Fit to frame` |
| `thanhXemTruoc.goiYOTrong` | `Nháy đúp để chọn trường, hoặc kéo trường từ bảng bên phải thả vào ô` | *(dịch)* |

### 3.4 `thietLapMau.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `thietLapMau.tieuDe` | `Thiết lập mẫu` | `Template settings` |
| `thietLapMau.nhomGiayVaChu` | `Giấy và chữ` | `Paper and text` |
| `thietLapMau.theoThietLapChung` | `Theo thiết lập chung` | `Use general settings` |
| `thietLapMau.khoGiay` | `Khổ giấy` | `Paper size` |
| `thietLapMau.huongGiay` | `Hướng giấy` | `Orientation` |
| `thietLapMau.huong.doc` | `Dọc` | `Portrait` |
| `thietLapMau.huong.ngang` | `Ngang` | `Landscape` |
| `thietLapMau.huong.tuDong` | `Tự động` | `Auto` |
| `thietLapMau.soCotTuDongNgang` | `Số cột để tự động in ngang` | `Columns to auto-print landscape` |
| `thietLapMau.canLe` | `Căn lề (cm)` | `Margins (cm)` |
| `thietLapMau.le.tren` | `Trên` | `Top` |
| `thietLapMau.le.trai` | `Trái` | `Left` |
| `thietLapMau.le.duoi` | `Dưới` | `Bottom` |
| `thietLapMau.le.phai` | `Phải` | `Right` |
| `thietLapMau.font` | `Font chữ` | `Font` |
| `thietLapMau.coChuCoSo` | `Cỡ chữ cơ sở` | `Base font size` |
| `thietLapMau.moCauHinhBaoCao` | `Mở Cấu hình báo cáo chứng từ` | `Open document report settings` |
| `thietLapMau.nhomRiengCuaMau` | `Riêng của mẫu` | `Template-specific` |
| `thietLapMau.mauChu` | `Màu chữ` | `Text color` |
| `thietLapMau.hinhNen` | `Hình nền` | `Background` |
| `thietLapMau.nen.khong` | `Không` | `None` |
| `thietLapMau.nen.khungVien` | `Khung viền` | `Border frame` |
| `thietLapMau.nen.anhTaiLen` | `Ảnh tải lên` | `Uploaded image` |
| `thietLapMau.doDam` | `Độ đậm (5–100%)` | `Opacity (5–100%)` |
| `thietLapMau.canAnh` | `Căn ảnh` | `Image fit` |
| `thietLapMau.canAnh.giuaTrang` | `Giữa trang` | `Centered` |
| `thietLapMau.canAnh.toanTrang` | `Toàn trang` | `Full page` |
| `thietLapMau.anh` | `Ảnh (jpg/png ≤ 1MB)` | `Image (jpg/png ≤ 1MB)` |
| `thietLapMau.chonAnh` | `Chọn ảnh…` | `Choose image…` |
| `thietLapMau.xoaAnh` | `Xóa` | `Remove` |

### 3.5 `dauTrang.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `dauTrang.tieuDe` | `Thông tin đầu trang` | `Page header` |
| `dauTrang.inKhoi` | `In khối Thông tin đầu trang trên mẫu này` | `Print the page header block on this template` |
| `dauTrang.nhomDongInRa` | `Dòng in ra` | `Printed lines` |
| `dauTrang.dong.tenDonVi` | `Tên đơn vị` | `Organization name` |
| `dauTrang.dong.diaChi` | `Địa chỉ` | `Address` |
| `dauTrang.dong.mst` | `Mã số thuế` | `Tax code` |
| `dauTrang.dong.dienThoai` | `Số điện thoại` | `Phone number` |
| `dauTrang.dong.email` | `Email` | `Email` |
| `dauTrang.dong.taiKhoanNganHang` | `Tài khoản ngân hàng` | `Bank account` |
| `dauTrang.dong.logo` | `Logo` | `Logo` |
| `dauTrang.logoCoVua` | `[LOGO] cỡ vừa` | `[LOGO] medium size` |
| `dauTrang.moThongTinTrenBanIn` | `Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in` | `Open document report settings › Print information` |

### 3.6 `tieuDe.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `tieuDe.tieuDe` | `Tiêu đề bản in` | `Printout title` |
| `tieuDe.noiDung` | `Nội dung` | `Content` |
| `tieuDe.coChu` | `Cỡ chữ (pt, 10–36)` | `Font size (pt, 10–36)` |
| `tieuDe.can` | `Căn` | `Align` |
| `tieuDe.inHoa` | `IN HOA` | `UPPERCASE` |
| `tieuDe.inDam` | `In đậm` | `Bold` |
| `tieuDe.dongNgayThang` | `Dòng ngày tháng ngay dưới tiêu đề` | `Date line right below the title` |
| `tieuDe.ghiChuNgay` | `In nghiêng "Ngày 27 tháng 08 năm 2026" — lấy theo ngày chứng từ.` | *(dịch)* |

### 3.7 `bang.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `bang.tenBangInRa` | `Tên bảng in ra` | `Printed table name` |
| `bang.inCotStt` | `In cột STT` | `Print row-number column` |
| `bang.dongCong` | `Dòng Cộng` | `Total row` |
| `bang.lapTieuDeMoiTrang` | `Lặp tiêu đề mỗi trang` | `Repeat header on each page` |
| `bang.keO` | `Kẻ ô` | `Cell borders` |
| `bang.keO.dayDu` | `Đầy đủ` | `Full` |
| `bang.keO.keNgang` | `Kẻ ngang` | `Horizontal only` |
| `bang.nhomCotInRa` | `Cột in ra` | `Printed columns` |
| `bang.timCot` | `Tìm cột…` | `Find column…` |
| `bang.cot.tenDl` | `Tên cột DL` | `Data column` |
| `bang.cot.tenHienThi` | `Tên hiển thị` | `Display name` |
| `bang.cot.rong` | `Rộng %` | `Width %` |
| `bang.cot.can` | `Căn` | `Align` |
| `bang.cot.cong` | `Cộng` | `Sum` |
| `bang.tongDoRong` | `Tổng độ rộng cột đang {{tong}}% (nên = 100%)` | `Total column width is {{tong}}% (should be 100%)` |
| `bang.chiaDeuVe100` | `Chia đều về 100%` | `Rescale to 100%` |

### 3.8 `tuDo.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `tuDo.tenKhoi` | `Tên khối` | `Block name` |
| `tuDo.datTenKhoi` | `Đặt tên khối` | `Name the block` |
| `tuDo.timKiem` | `Tìm kiếm` | `Search` |
| `tuDo.timKiemPlaceholder` | `Tìm kiếm…` | `Search…` |
| `tuDo.truongDuLieu` | `Trường dữ liệu` | `Data field` |
| `tuDo.tenHienThi` | `Tên hiển thị` | `Display name` |
| `tuDo.inDam` | `In đậm` | `Bold` |
| `tuDo.tenHienThiPlaceholder` | `Trống = chỉ in giá trị` | `Empty = print value only` |
| `tuDo.xoaKhoiNay` | `Xóa khối này` | `Delete this block` |
| `tuDo.khongConTrenForm` | `không còn trên form` | `no longer on the form` |
| `tuDo.nhanNguCanh` | `{{tenKhoi}} · ô dòng {{dong}}, cột {{cot}}` | `{{tenKhoi}} · cell row {{dong}}, column {{cot}}` |
| `tuDo.nut.themDongTren` | `+ Dòng trên` | `+ Row above` |
| `tuDo.nut.themDongDuoi` | `+ Dòng dưới` | `+ Row below` |
| `tuDo.nut.themCotTrai` | `+ Cột trái` | `+ Column left` |
| `tuDo.nut.themCotPhai` | `+ Cột phải` | `+ Column right` |
| `tuDo.nut.xoaDong` | `− Dòng` | `− Row` |
| `tuDo.nut.xoaCot` | `− Cột` | `− Column` |
| `tuDo.nut.gopO` | `Gộp ô` | `Merge cells` |
| `tuDo.nut.tachO` | `Tách ô` | `Split cell` |
| `tuDo.nut.inDam` | `In đậm` | `Bold` |
| `tuDo.nut.nghieng` | `Nghiêng` | `Italic` |
| `tuDo.nut.canTrai` | `Trái` | `Left` |
| `tuDo.nut.canGiua` | `Giữa` | `Center` |
| `tuDo.nut.canPhai` | `Phải` | `Right` |
| `tuDo.nut.chonTruong` | `Chọn trường…` | `Choose field…` |
| `tuDo.nut.xoaNoiDung` | `Xóa nội dung` | `Clear content` |
| `tuDo.menu.chonTruongDuLieu` | `Chọn trường dữ liệu…` | `Choose data field…` |
| `tuDo.menu.suaChu` | `Sửa chữ` | `Edit text` |
| `tuDo.menu.xoaNoiDungO` | `Xóa nội dung ô` | `Clear cell content` |
| `tuDo.menu.themDongPhiaTren` | `Thêm dòng phía trên` | `Insert row above` |
| `tuDo.menu.themDongPhiaDuoi` | `Thêm dòng phía dưới` | `Insert row below` |
| `tuDo.menu.themCotBenTrai` | `Thêm cột bên trái` | `Insert column left` |
| `tuDo.menu.themCotBenPhai` | `Thêm cột bên phải` | `Insert column right` |
| `tuDo.menu.xoaDong` | `Xóa dòng` | `Delete row` |
| `tuDo.menu.xoaCot` | `Xóa cột` | `Delete column` |
| `tuDo.menu.gopO` | `Gộp ô` | `Merge cells` |
| `tuDo.menu.tachO` | `Tách ô` | `Split cell` |
| `tuDo.hopChon.oTrong` | `(Ô trống)` | `(Empty cell)` |
| `tuDo.hopChon.chuTuDo` | `Chữ tự do` | `Free text` |
| `tuDo.loiOChuTuDo` | `Ô: Chữ tự do chưa có nội dung — nháy đúp để gõ` | `Cell: free text is empty — double-click to type` |

### 3.9 `chuKy.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `chuKy.tieuDe` | `Chữ ký` | `Signatures` |
| `chuKy.chucDanh` | `Chức danh` | `Role` |
| `chuKy.tieuDeInRa` | `Tiêu đề in ra` | `Printed title` |
| `chuKy.dongGhiChu` | `Dòng ghi chú` | `Note line` |
| `chuKy.badgeTuDo` | `tự do` | `custom` |
| `chuKy.themOKyTuDo` | `+ Thêm ô ký tự do` | `+ Add custom signature` |
| `chuKy.goiYOKy` | `VD: "Người nhận hàng", "Bên thuê"` | `e.g. "Recipient", "Lessee"` |
| `chuKy.dongNgay` | `Dòng "Ngày … tháng … năm …" phía trên` | `"Date …" line above` |
| `chuKy.choTrongKy` | `Chỗ trống ký` | `Signing space` |
| `chuKy.choTrong.thap` | `Thấp` | `Small` |
| `chuKy.choTrong.vua` | `Vừa` | `Medium` |
| `chuKy.choTrong.cao` | `Cao` | `Large` |
| `chuKy.ghiChuNguoiKy` | `Tên người ký in ra hay không theo cờ "In tên người ký" ở Thiết lập người ký (đang: {{trangThai}}). Đổi chức danh, tên người ký tại đó.` | *(dịch)* |
| `chuKy.trangThai.co` | `Có` | `Yes` |
| `chuKy.trangThai.khong` | `Không` | `No` |
| `chuKy.thietLapNguoiKy` | `Thiết lập người ký` | `Signer settings` |
| `chuKy.vaiTro.nguoiLapPhieu` | `Người lập phiếu` | `Preparer` |
| `chuKy.vaiTro.keToanTruong` | `Kế toán trưởng` | `Chief accountant` |
| `chuKy.vaiTro.giamDoc` | `Giám đốc` | `Director` |
| `chuKy.vaiTro.thuKho` | `Thủ kho` | `Storekeeper` |
| `chuKy.vaiTro.thuQuy` | `Thủ quỹ` | `Cashier` |

### 3.10 `banIn.*` — màn xem trước + **chữ IN RA GIẤY** (⚠ Q13)

| Khoá | `vi` | `en` |
|---|---|---|
| `banIn.tieuDe` | `Xem trước bản in: {{tenNghiepVu}} {{soChungTu}}` | `Print preview: {{tenNghiepVu}} {{soChungTu}}` |
| `banIn.nut.in` | `In` | `Print` |
| `banIn.nut.xuatFile` | `Xuất file` | `Export file` |
| `banIn.nut.suaMau` | `Sửa mẫu` | `Edit template` |
| `banIn.trang` | `Trang {{hienTai}} / {{tong}}` | `Page {{hienTai}} / {{tong}}` |
| `banIn.giay.stt` | `STT` | `STT` |
| `banIn.giay.cong` | `Cộng` | `Cộng` |
| `banIn.giay.tong` | `Tổng:` | `Tổng:` |
| `banIn.giay.kyHoTen` | `(Ký, họ tên)` | `(Ký, họ tên)` |
| `banIn.giay.kyHoTenDongDau` | `(Ký, họ tên, đóng dấu)` | `(Ký, họ tên, đóng dấu)` |
| `banIn.giay.dongNgay` | `Ngày {{ngay}} tháng {{thang}} năm {{nam}}` | `Ngày {{ngay}} tháng {{thang}} năm {{nam}}` |

⚠ **Q13** — nhóm `banIn.giay.*` là chữ **in ra giấy** trên chứng từ kế toán Việt Nam. Đề xuất `en` giữ
nguyên tiếng Việt (chứng từ pháp lý), khác với nhãn giao diện. **Chờ BA xác nhận.**

### 3.11 `menuIn.*`

| Khoá | `vi` | `en` |
|---|---|---|
| `menuIn.in` | `In` | `Print` |
| `menuIn.mauTuyChinh` | `Mẫu tùy chỉnh` | `Custom template` |
| `menuIn.thietLapMauIn` | `Thiết lập mẫu in…` | `Print template setup…` |
| `menuIn.tooltipChuaGhiSo` | `Đơn vị không cho phép in chứng từ chưa ghi sổ` | `Your organization does not allow printing unposted documents` |
| `menuIn.tooltipDaKhoaSo` | `Đơn vị không cho phép in chứng từ đã khóa sổ` | `Your organization does not allow printing documents in a closed period` |

⚠ Hai tooltip là **nguyên văn `S20:155-156`**, **chưa có mã `MSG_`** (L-5) ⇒ `msg.sh` báo `THIEU`.

### 3.12 `msg.*` — **ĐỦ 26 mã** `MSG_PMKT-E-14549_21_*`

| Khoá | Mã BA | `vi` (**NGUYÊN VĂN**) | Loại |
|---|---|---|---|
| `msg.e002` | `_002` | `Bạn không có quyền thực hiện tác vụ này` | Error |
| `msg.e003` | `_003` | `Lỗi hệ thống, vui lòng thử lại sau` | Error |
| `msg.s101` | `_101` | `Lưu mẫu in thành công!` | Success |
| `msg.i102` | `_102` | `Đã đưa về mẫu chuẩn hệ thống. Bấm Lưu để có hiệu lực` | Info |
| `msg.i103` | `_103` | `Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in theo mẫu chuẩn hệ thống` | Info |
| `msg.i104` | `_104` | `Đã thêm khối tự do trước Chữ ký. Nháy đúp một ô để chọn trường, hoặc kéo trường từ bảng bên phải thả vào ô` | Info |
| `msg.e201` | `_201` | `Tiêu đề bản in không được để trống, tối đa 255 ký tự` | Error |
| `msg.e202` | `_202` | `Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36` | Error |
| `msg.e203` | `_203` | `Bảng "{{TenBang}}" phải giữ lại ít nhất 1 cột hiển thị` | Error |
| `msg.e204` | `_204` | `Tên hiển thị của cột không được để trống, tối đa 100 ký tự` | Error |
| `msg.e205` | `_205` | `Độ rộng cột phải là số nguyên từ 3 đến 90` | Error |
| `msg.e206` | `_206` | `Tên khối tự do không được để trống, tối đa 60 ký tự` | Error |
| `msg.e207` | `_207` | `Mỗi mẫu tối đa 10 khối tự do` | Error |
| `msg.e208` | `_208` | `Mỗi khối tự do tối đa 20 dòng` | Error |
| `msg.e209` | `_209` | `Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB` | Error |
| `msg.e210` | `_210` | `Mã màu phải có dạng #rrggbb` | Error |
| `msg.e211` | `_211` | `Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự` | Error |
| `msg.e212` | `_212` | `Tên hiển thị và chữ tự do tối đa 255 ký tự` | Error |
| `msg.e213` | `_213` | `Căn lề phải là số từ 0 đến 5 cm` | Error |
| `msg.e214` | `_214` | `Số cột để tự động in ngang phải là số nguyên từ 1 đến 50` | Error |
| `msg.e215` | `_215` | `Cỡ chữ phải là số nguyên từ 8 đến 20` | Error |
| `msg.e216` | `_216` | `Mỗi khối tự do tối đa 6 cột` | Error |
| `msg.c401` | `_401` | `Mẫu đã có thay đổi chưa lưu. Bạn muốn làm gì?` | Confirmation |
| `msg.c402` | `_402` | `Mọi tùy chỉnh (kể cả khối tự do, thứ tự khối, cột bảng, chữ ký) sẽ trở về mẫu chuẩn hệ thống. Thay đổi chỉ có hiệu lực khi bạn bấm Lưu. Tiếp tục?` | Confirmation |
| `msg.c403` | `_403` | `Xóa khối "{{TenKhoi}}" cùng các ô trong đó?` | Confirmation |
| `msg.c404` | `_404` | `Vùng chọn có {{SoO}} ô đang có nội dung. Gộp thì chỉ giữ nội dung của ô đầu tiên, các ô còn lại mất nội dung. Tiếp tục?` | Confirmation |

**Đếm: 2 + 4 + 16 + 4 = 26 mã.** ✔

### 3.13 Nút của các hộp xác nhận

| Khoá | `vi` | `en` | Luật |
|---|---|---|---|
| `msg.nut.luuVaDong` | `Lưu và đóng` | `Save and close` | `R-TLMI-252` |
| `msg.nut.khongLuu` | `Không lưu` | `Don't save` | `R-TLMI-253` |
| `msg.nut.oLai` | `Ở lại` | `Stay` | `R-TLMI-254` |
| `msg.nut.tiepTuc` | `Tiếp tục` | `Continue` | ⚠ **Q11** — tài liệu không nêu |
| `msg.nut.huy` | `Huỷ` | `Cancel` | ⚠ **Q11** |

### 3.14 Mã `MSG_COMMON_*` dùng lại (L-4)

| Khoá | Mã | Dùng khi | Luật |
|---|---|---|---|
| `msg.xungDotPhienBan` | `MSG_COMMON_001` + câu hướng dẫn riêng | hai người cùng Lưu, lệch phiên bản | chốt **C06** |
| — | `MSG_COMMON_003` | thiếu quyền **In** (BR25.2) | chốt **C15** |

⚠ Hai mã này là **giải pháp tạm** cho tới khi BA cấp mã riêng (**Q1**).

---

## 4. Bảng kiểm tra dữ liệu — **17 dòng** (`R-TLMI-239`)

| # | Trường | Điều kiện | Mã | Tầng | Thời điểm | Luật | File con |
|---|---|---|---|---|---|---|---|
| V01 | Tiêu đề: Nội dung | không trống, ≤ 255 | `_201` | Client/Server | rời ô, Lưu | `R-TLMI-085` | `03` |
| V02 | Tiêu đề: Cỡ chữ | int 10-36 | `_202` | Client/Server | rời ô, Lưu | `R-TLMI-086` | `03` |
| V03 | Bảng: cột in | bảng bật còn ≥ 1 cột tick | `_203` | Client/Server | bỏ tick cột, Lưu | `R-TLMI-104` | `04` |
| V04 | Bảng: Tên hiển thị cột | không trống, ≤ 100 | `_204` | Client/Server | rời ô, Lưu | `R-TLMI-102` | `04` |
| V05 | Bảng: Rộng % | int 3-90 | `_205` | Client/Server | rời ô, Lưu | `R-TLMI-108` | `04` |
| V06 | Khối tự do: tên | không trống, ≤ 60 | `_206` | Client/Server | hộp Đặt tên, rời ô, Lưu | `R-TLMI-121` | `05` |
| V07 | Số khối tự do | ≤ 10 | `_207` | Client/Server | bấm Thêm, Lưu | `R-TLMI-125` | `05` |
| V08 | Số dòng một khối | ≤ 20 | `_208` | Client/Server | bấm + Dòng, Lưu | `R-TLMI-129` | `05` |
| V09 | Số cột một khối | ≤ 6 | `_216` | Client/Server | bấm + Cột, Lưu | `R-TLMI-130` | `05` |
| V10 | Ảnh nền | jpg/png ≤ 1MB | `_209` | Client/Server | **khi chọn tệp** | `R-TLMI-069` | `02` |
| V11 | Màu chữ | `#rrggbb` | `_210` | Client/Server | rời ô, Lưu | `R-TLMI-066` | `02` |
| V12 | Chữ ký: ô ký tự do **đang bật** | tiêu đề không trống, ≤ 60 | `_211` | Client/Server | rời ô, Lưu | `R-TLMI-189` | `06` |
| V13 | Khối tự do: Tên hiển thị trường; ô Chữ tự do | ≤ 255 (**trống ⇒ về ô trống, KHÔNG lỗi**) | `_212` | Client/Server | rời ô, Lưu | `R-TLMI-147` · `157` | `05` |
| V14 | Căn lề 4 phía | 0-5, ≤ 1 chữ số lẻ | `_213` | Client/Server | rời ô, Lưu | `R-TLMI-061` | `02` |
| V15 | Số cột tự động in ngang | int 1-50, **chỉ khi Hướng = Tự động** | `_214` | Client/Server | rời ô, Lưu | `R-TLMI-057` | `02` |
| V16 | Cỡ chữ cơ sở | int 8-20 | `_215` | **Server** | Lưu | `R-TLMI-063` | `02` |
| V17 | Quyền | có quyền Thiết lập mẫu in | `_002` | **Server** | mở màn, Lưu | `R-TLMI-034` | `07` |

### **KHÔNG phải lỗi** — ba điều `BR10` nói thêm mà bảng không ghi

| Trường hợp | Luật |
|---|---|
| tổng độ rộng cột ≠ 100 ⇒ **tự chia lại khi Lưu** | `R-TLMI-111` |
| **ô trống** trong khối tự do | `R-TLMI-236` |
| ô lưới không hợp lệ ⇒ viền đỏ ngay trên trang xem trước (đã là lỗi, nhưng hiển thị tại chỗ) | `R-TLMI-235` |

⚠ **Bảng KHÔNG có dòng nào cho `Độ đậm` hình nền (5-100 %)** — ghi nhận ở `§Z` của `02-rules.md`.

---

## 5. Hằng số nghiệp vụ — `constants/constants.ts`

```ts
export const SCHEMA_VERSION_MAU_IN = 2

export const KHO_GIAY = ['A3', 'A4', 'A5'] as const                    // R-TLMI-054
export const HUONG_GIAY = ['DOC', 'NGANG', 'TU_DONG'] as const         // R-TLMI-055
export const FONT_CHU = ['TIMES_NEW_ROMAN', 'ARIAL'] as const          // R-TLMI-062

export const GIOI_HAN_LE          = { min: 0,  max: 5,  soLe: 1 }      // R-TLMI-061
export const GIOI_HAN_CO_CHU      = { min: 8,  max: 20 }               // R-TLMI-063
export const GIOI_HAN_CO_CHU_TIEU_DE = { min: 10, max: 36, macDinh: 18 } // R-TLMI-086
export const GIOI_HAN_TIEU_DE     = { max: 255 }                       // R-TLMI-085
export const GIOI_HAN_SO_COT_NGANG = { min: 1, max: 50 }               // R-TLMI-057
export const GIOI_HAN_DO_DAM      = { min: 5,  max: 100, macDinh: 20 } // R-TLMI-072
export const GIOI_HAN_RONG_COT    = { min: 3,  max: 90 }               // R-TLMI-108
export const GIOI_HAN_TEN_COT     = { max: 100 }                       // R-TLMI-102
export const GIOI_HAN_TEN_KHOI    = { max: 60 }                        // R-TLMI-121
export const GIOI_HAN_CHU_TU_DO   = { max: 255 }                       // R-TLMI-147
export const GIOI_HAN_TEN_HIEN_THI = { max: 255 }                      // R-TLMI-157
export const GIOI_HAN_TIEU_DE_O_KY = { max: 60 }                       // R-TLMI-189
export const GIOI_HAN_LUOI = { dongMin: 1, dongMax: 20,
                               cotMin: 1,  cotMax: 6 }                 // R-TLMI-129/130 · C20
export const GIOI_HAN_KHOI_TU_DO  = { max: 10 }                        // R-TLMI-125
export const LUOI_MOI             = { soDong: 1, soCot: 2 }            // R-TLMI-123
export const DO_SAU_HOAN_TAC      = 60                                 // R-TLMI-223 · C32
export const ANH_NEN = { kieuTep: ['image/jpeg', 'image/png'],
                         dungLuongToiDa: 1024 * 1024 }                 // R-TLMI-069
export const BE_RONG_O_KY_TOI_THIEU = '4cm'                            // R-TLMI-194
export const MAU_CHU_MAC_DINH = '#000000'                              // R-TLMI-064
export const MAU_PRESET = [ /* 10 mã màu — R-TLMI-066, lấy từ Figma frame 1 */ ] as const
export const ZOOM = { min: 40, max: 200, buoc: 10, macDinh: 'VUA_KHUNG' } // R-TLMI-221

export const VAI_TRO_KY = ['NGUOI_LAP_PHIEU', 'KE_TOAN_TRUONG',
                           'GIAM_DOC', 'THU_KHO', 'THU_QUY'] as const  // R-TLMI-182
export const VAI_TRO_KY_BAT_MAC_DINH = ['NGUOI_LAP_PHIEU',
                                        'KE_TOAN_TRUONG', 'GIAM_DOC'] as const // R-TLMI-184
export const THU_TU_DONG_DAU_TRANG = ['tenDonVi', 'diaChi', 'mst', 'dienThoai',
                                      'email', 'taiKhoanNganHang', 'logo'] as const // R-TLMI-083

export const MA_MSG = {
  E002: 'MSG_PMKT-E-14549_21_002', E003: 'MSG_PMKT-E-14549_21_003',
  S101: 'MSG_PMKT-E-14549_21_101', I102: 'MSG_PMKT-E-14549_21_102',
  I103: 'MSG_PMKT-E-14549_21_103', I104: 'MSG_PMKT-E-14549_21_104',
  E201: 'MSG_PMKT-E-14549_21_201', /* … tới E216 … */
  C401: 'MSG_PMKT-E-14549_21_401', C402: 'MSG_PMKT-E-14549_21_402',
  C403: 'MSG_PMKT-E-14549_21_403', C404: 'MSG_PMKT-E-14549_21_404',
} as const
```

**Luật 1 của `CLAUDE.md`:** không hardcode magic value — mọi số ở trên đều là constant có tên, đặt ở
đúng một chỗ, đặt gần nơi dùng nhất (trong module).

---

## 6. Mã quyền — `constants/permissions.ts` (BR25 · Q-15)

```ts
/** Q-15 — đặt MỘT chỗ; đổi sang mã theo nghiệp vụ chỉ sửa file này. */
export const MA_QUYEN_MAU_IN = {
  /** Mở màn Thiết lập mẫu in (đọc mẫu) — R-TLMI-031, seed ở V1149. */
  view: 'HTMauIn.View',
  /** Lưu mẫu + hiện mục menu và nút Sửa mẫu — R-TLMI-032/034. */
  edit: 'HTMauIn.Edit',
} as const
```

| Hành vi | Quyền cần | Luật |
|---|---|---|
| Hiện mục `Thiết lập mẫu in…` / nút `Sửa mẫu` | `MA_QUYEN_MAU_IN.edit` **VÀ** `props.quyenXemChiTiet` | `R-TLMI-032` · chốt **C13** |
| Mở modal | `MA_QUYEN_MAU_IN.view` | `R-TLMI-031` |
| Lưu | `MA_QUYEN_MAU_IN.edit` | `R-TLMI-034` |
| In `Mẫu tùy chỉnh` | chỉ `props.quyenXemChiTiet` | `R-TLMI-033` |

⚠ **L-3**: gate bằng `HTMauIn.*` + `<ChucNang>.View.Detail` là **giải pháp tạm** vì epic nghiệp vụ chưa
khai mã quyền `Thiết lập mẫu in` riêng (`R-TLMI-014`). Xem **Q1** và biên bản `§7.6`.

---

## 7. Đường dẫn — `constants/paths.ts`

```ts
/** CHỈ endpoint API. KHÔNG có route màn — màn là modal (D1). */
export const MAU_IN_ENDPOINT = '/api/mau-in' as const
export const MAU_IN_PATHS = {
  hieuLuc:   `${MAU_IN_ENDPOINT}/hieu-luc`,
  luu:        MAU_IN_ENDPOINT,
  anhNen:    `${MAU_IN_ENDPOINT}/anh-nen`,
  duLieuIn:  `${MAU_IN_ENDPOINT}/du-lieu-in`,
  menu:      `${MAU_IN_ENDPOINT}/menu`,
} as const
```

⚠ **Bỏ** `duongDanThietLapMauIn()` ở
`client/src/base/domainKit/mauIn/constants/gioiHan.ts:212` — không còn route (D1).

## 8. Query key — `api/queries.ts`

```ts
export const mauInKeys = {
  goc:      ['mauIn'] as const,
  hieuLuc:  (ma: string, nv: string) => [...mauInKeys.goc, 'hieuLuc', ma, nv] as const,
  duLieuIn: (id: string)             => [...mauInKeys.goc, 'duLieuIn', id]    as const,
  menu:     (ma: string, nv: string, id: string) =>
              [...mauInKeys.goc, 'menu', ma, nv, id] as const,
}
```

**Invalidate sau khi Lưu thành công** (`R-TLMI-022` · `R-TLMI-030`):
`mauInKeys.hieuLuc(ma, nv)` **và** `mauInKeys.duLieuIn(chungTuId)`.
