# PLAN CẬP NHẬT — PMKT-E-06196 Hóa đơn bán hàng (FE)

> Bản kế hoạch **DELTA**, lập lại sau khi (a) BA cập nhật tài liệu và (b) module bị việc song song
> refactor sang engine `@domain-kit/chungTu`. Bản thi công lần đầu ghi ở [IMPLEMENT.md](IMPLEMENT.md).
>
> **Mốc so sánh:** code lần đầu bám tài liệu ở commit trước `051266623`; tài liệu hiện ở
> `d23d1e20d "đồng bộ tên entity ldm - scr field"`.

---

## 0. Trạng thái hiện tại (đo trước khi sửa)

| Cổng | Kết quả |
| :-- | :-- |
| `typecheck` | **0 lỗi** trong `hoaDonBanHang/**` và `banHang/_shared/**` |
| `vitest` module | **6 file · 123/123 PASS** |

Nghĩa là: code đang XANH, nhưng đang bám **tài liệu cũ**. Toàn bộ việc dưới đây là *đồng bộ lại với
tài liệu mới*, không phải sửa lỗi.

---

## 1. Tài liệu đã đổi gì

### 1.1. `SCR_HDBanHang_DanhSach.md` (104 → 172 dòng) — đổi NHIỀU NHẤT

| # | Thay đổi | Tác động |
| :-- | :-- | :-- |
| D1 | Bảng chính thêm **2 cột**: `Mẫu số hóa đơn`, `Ký hiệu hóa đơn` (giữa *Ngày hóa đơn* và *Số hóa đơn*), đều `Tìm kiếm = Y`, `Sắp xếp = Y` | Code đang có 8 cột → phải thành 10 |
| D2 | Cột **STT** được khai tường minh (`Control = Text`, `N/N`) | Cần chốt: Figma vẽ ô tích ở ô đầu, BA khai STT → mục 4 |
| D3 | **BR08 (MỚI) — Nguồn dữ liệu**: bảng ánh xạ cột → field, đổi hẳn tên entity/field | Đổi tên trường trên toàn bộ `api/` |
| D4 | **BR09 (MỚI) — Khu vực chi tiết dưới lưới**: đặc tả đầy đủ panel con | Đối chiếu lại panel |
| D5 | Link Figma đổi sang `node-id=58263-162967` | Khớp node code đang dùng — không phải sửa |

**D3 — bảng đổi tên (từ BR08):**

| Cột | Tên CŨ (code đang dùng) | Tên MỚI (BR08) |
| :-- | :-- | :-- |
| Entity | `HoaDonBan` | `sal_hoa_don_ban_hang` |
| Entity dòng | `ChiTietHoaDonBan` | `sal_hoa_don_ban_hang_chi_tiet` |
| Trạng thái phát hành | `trangThaiPhatHanhHoaDon` | **`trangThaiPhatHanh`** |
| Tiền thuế GTGT | `tongTienThueGtgtQuyDoi` | **`tongThueGTGT`** (ngoại tệ lấy `tongThueGTGTQuyDoi`) |
| Mẫu số | *(chưa có)* | `mauSoHoaDonId` → `mst_mau_so_hoa_don.MauSo` |
| Diễn giải ẩn của dòng | `moTa` | **`dienGiai`** |
| Liên kết chứng từ nguồn | *(chưa có ở header)* | **`chungTuBanId`** |

**D4 — BR09 nói gì (đối chiếu với code hiện tại):**

| Yêu cầu BR09 | Code hiện tại | Việc |
| :-- | :-- | :-- |
| Chỉ hiện khi có `LapHoaDonBan.View.Detail`; **kiểm quyền trước khi trả dữ liệu** | ✅ query tắt khi thiếu quyền | — |
| Tiêu điểm dòng TÁCH khỏi checkbox | ✅ | — |
| Đổi trang / lọc / sắp xếp → tiêu điểm về dòng đầu | ✅ | — |
| Đang tải thì hiện **trạng thái đang tải**, không hiện bản ghi trước | ✅ `loading` | — |
| Nội dung: **CHỈ** Bảng chi tiết hàng hóa, *"chỉ một section nên hiển thị **thẳng, không chia tab**"* | ⚠ panel có **2 tab** (Chi tiết hàng hóa · Đính kèm) | **W6** |
| Nhãn Số chứng từ là **liên kết** mở Xem chi tiết | ⚠ đang là text thường | **W7** |
| Phân trang riêng · chỉ đọc · dòng Tổng theo BR31 | ✅ | — |

### 1.2. `SCR_HDBanHang_ThemMoi.md`

| # | Thay đổi | Tác động |
| :-- | :-- | :-- |
| T1 | **`LoaiNghiepVu` có 3 giá trị**: thêm `Bán dịch vụ` | `constants` đang khai 2 |
| T2 | Màn này **chỉ cho chọn 2** (`Bán hàng trong nước` · `Bán hàng xuất khẩu`), **ẩn** `Bán dịch vụ` khỏi combo — CTBH **BR24** | `options.ts` đang đổ hết `Object.values` |
| T3 | Hóa đơn **lập kèm** từ chứng từ nguồn thì **kế thừa `LoaiNghiepVu` và KHÔNG cho sửa** | Ô đang luôn sửa được |
| T4 | Toàn bộ tham chiếu BR của CTBH **đổi số** (BA đã sửa đúng lệch mà `IMPLEMENT.md §4.3` báo) | Comment trong code trỏ số cũ |
| T5 | Field dòng: `MoTa` → `DienGiai` | `types.ts`, `payload.ts`, `formDetail.ts` |

**T4 — bảng đối chiếu số BR của CTBH (code đang ghi số CŨ):**

| Nội dung | Code đang ghi | Tài liệu MỚI |
| :-- | :-- | :-- |
| Auto-fill Khách hàng | BR07 | **BR01** |
| Kiểm trùng hóa đơn | BR06 | BR06 *(giữ)* |
| Auto-fill từ danh mục Vật tư | *(gộp BR07)* | **BR07** |
| Thêm dòng | BR05 | **BR08** |
| Hàng khuyến mại · CK thương mại | BR02 · BR03 | **BR09** |
| Đơn vị tính quy đổi | BR16 | **BR10** |
| Số lượng · Đơn giá · Thành tiền | BR18 | **BR11** |
| Trường quy đổi theo tỷ giá | BR09 | **BR11 mục 5** |
| Chiết khấu | BR11 | **BR12** |
| Thuế GTGT | BR10 | **BR13** |
| Thuế xuất khẩu | *(§Tab chi tiết)* | **BR14** |
| Diễn giải · Diễn giải thuế | BR20 | **BR15** |
| Theo dõi SL đã xuất | BR17 | **BR23** |
| Phạm vi Loại nghiệp vụ | *(chưa có)* | **BR24 (mới)** |

### 1.3. `3.crud-matrix.md` · `_scope.md` · `SCR_HDBanHang_Xoa.md`

- crud-matrix: đổi tên entity (`ENT_mst_doi_tuong`, `ENT_mst_vat_tu`…) — **không đổi hành vi**.
- `_scope.md`: bỏ "Tab Hạch toán" khỏi danh mục lược bỏ — **không đổi hành vi**.
- `SCR_HDBanHang_Xoa.md`: chuẩn hóa cột `Control`/`Tham chiếu`; **cấu trúc popup kết quả giữ nguyên**
  (STT · Ngày hóa đơn · Số hóa đơn · Tên khách hàng · Lý do lỗi) → code vẫn khớp.
- Ma trận Ẩn/Hiện: vẫn **2 cột** theo Loại nghiệp vụ → `Bán dịch vụ` không mở thêm cột (mục 4).

---

## 2. Code đã bị đổi gì (việc song song)

| # | Thay đổi | Đánh giá |
| :-- | :-- | :-- |
| C1 | **Màn danh sách chuyển sang engine `@domain-kit/chungTu`** — thêm `api/chungTuModule.ts`, `Tab` dùng `ChungTuListPage`, `queries.ts` lấy từ `hoaDonBanHangModule` | ✅ Đúng hướng `client/CLAUDE.md §4` ("có engine thì dùng descriptor, đừng viết lại khung") |
| C2 | Ba nhóm trạng thái đổi từ chuỗi tiếng Việt sang **TÊN HẰNG** (`CHUA_LAP`, `DA_PHAT_HANH`, `GOC`…) | ✅ Khớp cách `trangThaiChungTu` của CTBH; nhãn vẫn qua i18n |
| C3 | `routes.tsx`: `crumbKeys` → **`crumbs`** (`{key, path}`) — sửa lỗi breadcrumb rỗng | ✅ Sửa lỗi thật |
| C4 | Thêm `test/i18n.test.ts` | ✅ |
| C5 | **`HoaDonBanHangListTable.tsx` và `HoaDonBanHangQuickDetail.tsx` thành MỒ CÔI** — engine đã thay, không file nào import | ❌ Code chết → **W8** |

---

## 3. Danh sách việc (theo thứ tự thi công)

| # | Việc | File | Nguồn |
| :-- | :-- | :-- | :-- |
| **W1** | `LOAI_NGHIEP_VU` thêm `banDichVu`; thêm hằng `LOAI_NGHIEP_VU_CHON_DUOC` (2 giá trị của màn này) | `constants/constants.ts` | T1 · T2 · BR24 |
| **W2** | `loaiNghiepVuOptions()` chỉ đổ 2 giá trị chọn được | `fields/options.ts` | T2 · BR24 |
| **W3** | Ô "Loại nghiệp vụ" **disable khi hóa đơn kế thừa từ chứng từ nguồn** (`chungTuBanId` ≠ null) | `types.ts` · `HoaDonBanHangThemMoiModal.tsx` · `ThongTinHoaDon.tsx` | T3 · BR24 |
| **W4** | Đổi tên field theo BR08: `trangThaiPhatHanhHoaDon`→`trangThaiPhatHanh`, `tongTienThueGtgtQuyDoi`→`tongThueGTGT(QuyDoi)`, dòng `moTa`→`dienGiai`; thêm `chungTuBanId`, `mauSoHoaDon` | `api/model.ts` · `payload.ts` · `formDetail.ts` · `mock.ts` · `hoaDonBanHangApi.ts` · `fields/*` · `helpers/*` · `test/*` | D3 · T5 |
| **W5** | Danh sách thêm **2 cột** Mẫu số hóa đơn · Ký hiệu hóa đơn (có tìm kiếm + sắp xếp) | `fields/columns.ts` · `fields/texts.ts` · `i18n/*` | D1 |
| **W6** | Panel con **bỏ tab "Đính kèm"** — BR09 đòi hiển thị thẳng một section | `constants.ts` · `chungTuModule.ts` | D4 |
| **W7** | Nhãn "Số chứng từ" ở panel con thành **liên kết** mở Xem chi tiết | `chungTuModule.ts` / engine | D4 |
| **W8** | **Xóa 2 file mồ côi** + sửa comment trỏ tới chúng | `components/HoaDonBanHangListTable.tsx` · `HoaDonBanHangQuickDetail.tsx` · `helpers/trangThai.ts` | C5 |
| **W9** | Cập nhật **số hiệu BR của CTBH** trong mọi doc-comment; đổi tên entity trong comment | `helpers/*` · `fields/*` · `api/*` | T4 |
| **W10** | Bổ sung test khóa hành vi mới (3 giá trị nghiệp vụ · 2 cột mới · disable khi kế thừa) | `test/anHien.test.ts` · `payload.test.ts` | W1–W5 |

---

## 4. Điểm cần BA / Design xác nhận (KHÔNG code phần phụ thuộc)

| Q | Câu hỏi | Vì sao treo |
| :-- | :-- | :-- |
| **Q1** | Bảng chính có cột **STT** không? BA khai (`D2`), Figma `58263:162967` vẽ **ô tích** ở ô đầu và không có STT. | Hai nguồn nói khác nhau; đang theo Figma (`showIndex = false`). Không tự đổi. |
| **Q2** | `Bán dịch vụ` có mở thêm **cột ma trận** thứ ba không? Ma trận Ẩn/Hiện vẫn 2 cột, nhưng BR24 khai 3 giá trị. | Đang xử lý `Bán dịch vụ` **như trong nước** (BR24: *"thuế GTGT xử lý giống Bán hàng trong nước, khối cột thuế XK ẩn"*) — suy luận có căn cứ, cần BA chốt. |
| **Q3** | `TrangThaiPhatHanh` hay `TrangThaiPhatHanhHoaDon`? BR08 (mới) viết **`TrangThaiPhatHanh`**, BR04 của ThemMoi vẫn viết `TrangThaiPhatHanhHoaDon`. | Mâu thuẫn nội bộ tài liệu. Theo **BR08** vì đó là bảng nguồn dữ liệu mới nhất. |
| **Q4** | Panel con: engine luôn dựng **thanh tab** (tab đầu do engine tạo). BR09 đòi *"không chia tab"*. | Bỏ tab thứ hai là làm được; bỏ HẲN thanh tab phải sửa `@domain-kit` — ngoài phạm vi PYC. |

---

## 5. Cổng nghiệm thu cho lượt này

```bash
cd client && npx tsc -p tsconfig.app.json --noEmit    # 0 lỗi trong hoaDonBanHang/**
cd client && npx vitest run src/features/banHang/hoaDonBanHang/test
cd client && npx eslint src/features/banHang/hoaDonBanHang src/features/banHang/_shared
```

Cộng: soát tay `any` / `@ts-ignore` / `eslint-disable` / `../../` / file lạc ở gốc module, và cân bằng
khóa i18n vi ⇄ en — đúng bộ kiểm đã dùng ở `IMPLEMENT.md §6.3`.

---

## 6. KẾT QUẢ THI CÔNG (cùng lượt)

### 6.1. ⚠ Phát hiện chặn — **W4 bị HỦY sau khi đối chiếu BE**

Khi bắt tay làm W4 (đổi tên field theo BR08) thì phát hiện **BE đã lên**: `HDBH_DUNG_MOCK = false` từ
2026-08-14, cell-app đã có `cell/hoa_don_ban_hang` với `POST /tim-kiem` · `GET /cot` · `GET /{id}`.

Đối chiếu tận nơi thì **BR08 KHÔNG phải hợp đồng JSON** — nó là bảng ánh xạ **cột DB / LDM**:

| Nguồn | `Trạng thái phát hành` | `Tiền thuế GTGT` |
| :-- | :-- | :-- |
| BR08 (tên **cột DB**) | `sal_hoa_don_ban_hang.TrangThaiPhatHanh` | `TongThueGTGT` / `TongThueGTGTQuyDoi` |
| `HoaDonBanHangDto` (tên **khóa JSON**) | **`trangThaiPhatHanhHoaDon`** | **`tongTienThueGtgtQuyDoi`** |
| `@Searchable` (alias cho `sort` / `filters[].field`) | **`trangThaiPhatHanhHoaDon`** *(alias khai tường minh)* | — |

→ Đổi tên theo BR08 là **đổi khóa thành thứ server không bao giờ gửi**, và `sort`/`filters` trỏ vào
alias không tồn tại. **Đã hoàn tác toàn bộ**; `api/model.ts` giữ tên DTO và header file được viết lại
để cảnh báo đúng cái bẫy này cho người sau.

**Việc thật sự làm của W4:** bổ sung hai trường DTO đang thiếu — `chungTuBanId` (BR24) và `phienBan`.

### 6.2. Bảng kết quả từng việc

| # | Việc | Kết quả |
| :-- | :-- | :-- |
| W1 | `LOAI_NGHIEP_VU` + `banDichVu`; thêm `LOAI_NGHIEP_VU_CHON_DUOC` | ✅ |
| W2 | Combo chỉ đổ 2 giá trị chọn được | ✅ |
| W3 | Khóa ô Loại nghiệp vụ khi kế thừa (`chungTuBanId` ≠ null) — thêm `keThuaLoaiNghiepVu` + `khoaLoaiNghiepVu()` | ✅ |
| W4 | ~~Đổi tên field theo BR08~~ → **HỦY** (xem 6.1); thay bằng `+ chungTuBanId`, `+ phienBan` | ✅ (đổi hướng) |
| W5 | Thêm cột **Ký hiệu hóa đơn** (+ i18n vi/en) | ✅ một phần — xem 6.3 |
| W6 | Panel con bỏ tab "Đính kèm" | ✅ đạt sẵn nhờ engine; đã gỡ hằng số + khóa i18n chết |
| W7 | Nhãn Số chứng từ thành liên kết | ⛔ Không làm — engine sở hữu panel, sửa phải vào `@domain-kit` |
| W8 | Xóa 2 file mồ côi + sửa comment trỏ tới chúng | ✅ |
| W9 | Cập nhật số hiệu BR của CTBH (23 file) + tên entity | ✅ |
| W10 | Test cho hành vi mới | ✅ +12 test (123 → **135**) |

### 6.3. Việc KHÔNG làm, kèm lý do

| Việc | Lý do |
| :-- | :-- |
| Cột **"Mẫu số hóa đơn"** | `HoaDonBanHangDto` chỉ trả `mauSoHoaDonId` (UUID), **không** trả `MauSo`; entity cũng không khai `@Searchable` cho nó. In UUID thì không đọc được, in trắng thì đọc thành thiếu dữ liệu. Cột danh sách dựng ở **module scope** nên không tra được danh mục (engine chỉ cho ghi đè `lineColumns`, không cho ghi đè `columns`). → **Chờ BE thêm tên mẫu số vào DTO.** Cùng tiền lệ `chungTuBanHang/fields/chiTietColumns.ts` bỏ cột tên danh mục. |
| **Sắp xếp** cột "Ký hiệu hóa đơn" | BA khai `Sắp xếp = Y` nhưng entity khai `@Searchable(keyword = true)` **không có `sortable`** → `sort=kyHieuHoaDon:asc` không chạy. Cột có mặt và tìm nhanh vẫn quét nó; chỉ bỏ mũi tên. **Cần BE thêm `sortable = true`.** |
| Cột **STT** (Q1) | Figma `58263:162967` vẽ ô tích ở ô đầu, không có STT. Giữ `showIndex = false`, chờ BA chốt. |
| W7 — nhãn liên kết ở panel | Phải sửa `@domain-kit/chungTu`, ngoài phạm vi PYC. |

### 6.4. Cổng nghiệm thu

| Cổng | Kết quả |
| :-- | :-- |
| `typecheck` (module) | **0 lỗi** ✅ |
| `eslint` (module) | **0 lỗi** ✅ |
| `vitest` module | **7 file · 135/135 PASS** ✅ |
| `vitest` toàn domain `banHang` | 513/517 — **4 lỗi thuộc `chungTuBanHang`**, do việc song song đang chuyển module đó sang engine (17 file `M`, +349 dòng, sửa cả test của chính nó). Phiên này KHÔNG đụng `chungTuBanHang`. |
| `any` · `@ts-ignore` · `eslint-disable` · `../../` · file lạc ở gốc | **0** ✅ |
| Cân bằng i18n vi ⇄ en | **312 = 312** ✅ |

### 6.5. Câu hỏi mới cho BA / BE (bổ sung §4)

| Q | Nội dung |
| :-- | :-- |
| **Q5** | **BE bổ sung `mauSoHoaDon` (chuỗi `MauSo`) vào `HoaDonBanHangDto`** để dựng được cột "Mẫu số hóa đơn" BA vừa thêm. |
| **Q6** | **BE thêm `sortable = true` cho `kyHieuHoaDon`** nếu BA thật sự cần sắp xếp theo cột này (BA đang khai `Sắp xếp = Y`). |
| **Q7** | BR08 dùng tên **cột DB**, còn FE phải bám tên **DTO** — đề nghị BA ghi rõ trong tài liệu đó là ánh xạ LDM, để lần sau không ai đổi nhầm khóa JSON theo nó (đã suýt xảy ra, xem 6.1). |
| **Q8** | `TrangThaiPhatHanh` (BR08) vs `TrangThaiPhatHanhHoaDon` (BR04 · DTO · alias `@Searchable`) — tài liệu tự mâu thuẫn, code theo DTO. |
