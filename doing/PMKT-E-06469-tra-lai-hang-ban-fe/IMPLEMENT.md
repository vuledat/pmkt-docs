# IMPLEMENT — PMKT-E-06469 Trả lại hàng bán (FE)

> **Rà soát 2026-08-21** — đối chiếu lại tài liệu BA + code hiện tại. Ba thay đổi lớn kể từ bản
> 2026-08-12, chi tiết ở [§0](#0-rà-soát-2026-08-21--tài-liệu-và-code-đã-đổi-những-gì):
>
> 1. **Tài liệu BA đã đổi 13 commit** (2026-08-14 → 2026-08-17) — nặng nhất là `SCR_DanhSach`
>    (+162 dòng: đổi cột, thêm cột, thêm BR18 · BR21–BR28, **đặc tả vùng Thông tin chi tiết**).
> 2. **BE đã có thật** — `cell-app/.../cell/tra_lai_hang_ban/`, nhưng **chỉ phần ĐỌC**; FE đã bị một
>    phiên khác bật `DUNG_MOCK = false` nên **mọi luồng GHI hiện gọi vào endpoint chưa cài**.
> 3. **Màn danh sách đã chuyển sang engine `@domain-kit/chungTu`** (commit `4488c828`), FE thêm panel
>    "Chi tiết hàng hóa" dưới danh sách (2026-08-21).

## 0. Rà soát 2026-08-21 — tài liệu và code đã đổi những gì

### 0.1 Tài liệu BA (`pmkt-docs`, 13 commit từ `0705d142d`..`HEAD`)

| Tài liệu | Đổi gì | FE phải làm gì |
| --- | --- | --- |
| `SCR_DanhSachTraLaiHangBan.md` (+162 dòng) | Bảng chính đổi bộ cột: **Ngày hạch toán → Ngày chứng từ** (BR21) · **Tổng thanh toán → Tổng tiền** kèm công thức ∑(ThanhTien − ChietKhau + TienThueGTGT) (BR24) · thêm cột **Trạng thái thanh toán** (BR28) · thêm cột **Chọn** (checkbox) | **CHƯA làm** — xem L13, N8, N9 |
| ↑ | Thanh công cụ thêm **3 nút hàng loạt** Ghi sổ / Bỏ ghi sổ / Xóa (BR14 · BR15 · BR16); ô Tìm kiếm max length 100 → **255** | **CHƯA làm** — xem L14 |
| ↑ | **§Thông tin chi tiết** — đặc tả MỚI: chọn 1 dòng → hiện vùng chi tiết readonly ngay dưới danh sách, header "Số chứng từ: \<SoChungTu\>", chỉ hiện khi có `TraLaiHangBan.View.Detail`, tab hiện theo dữ liệu chứng từ | **ĐÃ làm 2026-08-21** — xem L12 |
| ↑ | Quyền đổi từ `PMKT.E06469.*` sang **`TraLaiHangBan.Create` · `.View` · `.View.Detail`** | **KHỚP SẴN** — L6 đóng lại |
| ↑ | BR18 (điều kiện lập chứng từ liên kết) tách thành mục riêng | Đã code đúng từ đầu (`rowActionsThem.visible`) |
| `SCR_ThemMoiTraLaiHangBan.md` (≈400 dòng đổi) | Phần lớn là chuẩn hoá trình bày: cột "Mô tả" → "Tham chiếu", tên control (`Combobox`→`Select`, `Textbox`→`TextField`), tên entity `ENT_*` → tên bảng LDM (`sal_*` · `cash_*` · `pur_*`), bổ sung Max length | Không ảnh hưởng code |
| ↑ | Bổ sung trường trên tab: Hóa đơn (Người mua hàng · Mã số ĐVQHNS · CCCD · Hộ chiếu · Điện thoại · Lý do điều chỉnh) · Phiếu chi/UNC/Séc (Kèm theo · Chứng từ gốc · Số giấy tờ · Nơi cấp) · PNK (Người giao hàng) | **CẦN ĐỐI CHIẾU** — xem L16 |
| ↑ | Thêm **BR99** — ràng buộc số ở tầng DB/LDM, *"không thay thế validation trên giao diện"* | Không ảnh hưởng code |
| `6.messages.md` | MSG_106 thêm ngoặc *"(Dịch vụ cho phép bằng 0 theo BR1)"* | **ĐÃ ĐÚNG SẴN** — `helpers/kiemTra.ts:84` đã miễn dòng dịch vụ |
| `README.md` | Đổi tên entity sang LDM (`ENT_sal_chung_tu_tra_lai_hang_ban`…) | Không ảnh hưởng code |
| **`Common/business_rules.md`** (17 commit · +286 dòng, tới 2026-08-20) | Phần lớn là dựng lại bảng; **ba BR MỚI**: **BR47** dữ liệu mặc định của danh mục · **BR48 Xem dữ liệu ghi sổ** · **BR49 Di chuyển chứng từ trước–sau ở màn chi tiết** | BR47 không chạm màn này. **BR48 · BR49 là việc MỚI cho mọi màn chứng từ** — xem §7 và §8-D |

### 0.2 Backend `cell-app` — đã có module, nhưng CHỈ phần ĐỌC

`cell-app/src/main/java/vn/vtt/pmkt/cell/tra_lai_hang_ban/` (14 file). Đọc thẳng code, không đoán:

| Endpoint | Trạng thái thật | Hệ quả cho FE |
| --- | --- | --- |
| `POST /api/ban-hang/tra-lai-hang-ban/search` · `/cot` · `GET /{id}` · export Excel | ✅ cài đủ (`TraLaiHangBanCrudService extends AbstractCrudService`) | Màn danh sách chạy thật |
| `POST /` · `PUT /{id}` · `DELETE /{id}` | ❌ **chặn tường minh** — `throw chuaCai(...)` → HTTP 400 `CHUA_HO_TRO` (`TraLaiHangBanController.java:98-116`) | Lưu · Sửa · Xóa từ FE **hiện luôn lỗi** |
| `POST /{id}/ghi-so` · `/{id}/bo-ghi-so` · `*-hang-loat` | ❌ **không tồn tại** — controller kế thừa `BaseCrudController`, không phải `BaseChungTuController` (nơi có 4 mapping đó) | Ghi sổ · Bỏ ghi sổ từ FE **404** |
| `chiTiet` trong `GET /{id}` | ❌ `TraLaiHangBanDto` **không có** trường `chiTiet`; service ghi rõ `layDongChiTiet` "chưa nằm trong phạm vi" | Panel chi tiết + lưới của popup Sửa/Xem **luôn rỗng** khi chạy thật |

`TraLaiHangBanDto` có javadoc *"khớp `traLaiHangBanRowSchema` của FE"* — BE đã lấy hợp đồng wire theo
đúng FE (quyết định D7 của [kế hoạch BE](../PMKT-E-06469-tra-lai-hang-ban-api/00-ke-hoach-tong.md)),
nên **L7 (enum wire chưa đối chiếu) coi như đã đóng cho phần header**; phần dòng chi tiết vẫn chờ F2.

### 0.3 Code FE đã đổi (không phải do phiên này)

| Thay đổi | Commit / ngày | Ảnh hưởng tới tài liệu này |
| --- | --- | --- |
| Màn danh sách chuyển sang engine `@domain-kit/chungTu` | `4488c828` | `api/chungTuModule.ts` thay cho state tự cầm; `components/TraLaiHangBanListTable.tsx` **thành code chết**; hai câu xác nhận đặc thù (BR19 bộ chứng từ · MSG_207) mất — đã ghi ở docblock của `TraLaiHangBanTab.tsx` |
| `DUNG_MOCK = false` | `66ce49f4` / 2026-08-14 | Màn danh sách chạy API thật; **luồng ghi vỡ** (§0.2) — `api/mock.ts` giờ là nhánh không bao giờ chạy |
| Popup bám lại Figma 15756:47126 + tách `ThanThemMoi` | 2026-08-13 (phiên này) | L10 |
| Panel "Chi tiết hàng hóa" dưới danh sách | 2026-08-21 (phiên này) | L12 |

## 1. Ngày · phạm vi đã code

**2026-08-12** — code THẲNG từ PYC `pmkt-docs/ba/PMKT-E-06469_TraLaiHangBan/` (user chọn bỏ bước
`/plan-fe`; vì vậy §1 + §2 của `/plan-fe` — đọc bắt buộc và khảo sát reuse có bằng chứng — được làm
đầy đủ và ghi ở §3 dưới đây).

Đã code:

| Màn / use case | Trạng thái |
| --- | --- |
| SCR_DanhSachTraLaiHangBan (U-06470 Xem danh sách) | ✅ đủ |
| SCR_ThemMoiTraLaiHangBan (U-06471 Thêm mới) | ✅ đủ khung + luật; phần chọn nguồn chờ API (§5) |
| SCR_SuaTraLaiHangBan (U-06472 Sửa) | ✅ đủ (dùng chung popup, khóa Số/Ngày chứng từ) |
| U-06473 Xóa | ✅ đủ (hộp xác nhận MSG_212 / BR19 bộ chứng từ) |
| U-06474 Nhân bản | ✅ đủ (`toFormValuesNhanBan`) |
| U-06475 Ghi sổ · U-06476 Bỏ ghi sổ (một chứng từ) | ✅ đủ (hộp xác nhận MSG_207) |
| SCR_XemChiTietTraLaiHangBan (U-06477) | ✅ đủ (chế độ `view`, khóa toàn bộ ô nhập) |
| BR14 · BR15 · BR16 — ghi sổ / bỏ ghi sổ / xóa **HÀNG LOẠT** | ⚠ mới lọc điều kiện, chưa chạy (§5) |

⚠ **Cột "Trạng thái" ở trên là trạng thái của FE, không phải của tính năng chạy được đầu-cuối.** Tính tới 2026-08-21, BE mới cài phần ĐỌC: Thêm mới · Sửa · Xóa trả 400 `CHUA_HO_TRO`, Ghi sổ · Bỏ ghi sổ không có endpoint, `GET /{id}` chưa trả dòng chi tiết — xem [§0.2](#02-backend-cell-app--đã-có-module-nhưng-chỉ-phần-đọc).

## 2. Danh sách file đã tạo / sửa

### Tạo mới — `client/src/features/banHang/traLaiHangBan/` (55 file · ~11.400 dòng, đo 2026-08-21)

| File | Vai trò |
| --- | --- |
| `index.ts` | Cửa ra duy nhất của module (file DUY NHẤT ở gốc) |
| `api/model.ts` | Hợp đồng wire Zod của `ChungTuTraLaiHangBan` + chi tiết + dòng tổng |
| `api/traLaiHangBanApi.ts` | Adapter BASE CRUD + `toSearchRequest` + ghi sổ/bỏ ghi sổ + tra nhanh chứng từ nguồn |
| `api/mock.ts` | **NỢ — nay là NHÁNH CHẾT**: `DUNG_MOCK = false` từ 2026-08-14 nên không lệnh nào chạy vào đây nữa (§0.3) |
| `api/chungTuModule.ts` | **Mới sau đợt chuyển engine** — descriptor `defineChungTu` + `createChungTuModule`: cột · phễu · trạng thái · endpoint · quyền |
| `api/queries.ts` | Hook react-query có phạm vi tenant |
| `api/lookups.ts` | Danh mục thật (`/api/master-data/*`) cho mọi select của popup |
| `api/payload.ts` | Form store → thân request (gộp tab về header phẳng, loại dòng trắng) |
| `api/formDetail.ts` | Chiều ngược: wire → form store; kèm biến thể **Nhân bản** |
| `constants/constants.ts` | Enum wire · nhãn cột · khóa tab · hình học · `MAX_LEN` |
| `constants/paths.ts` | Re-export path từ `banHang/_shared/constants/banHangTabs.ts` |
| `constants/permissions.ts` | Mã quyền `TraLaiHangBan.*` (BR25) |
| `fields/types.ts` | Hình dạng form store + `NguCanhAnHien` (bản dựng sẵn của ma trận) |
| `fields/columns.ts` | 8 cột màn danh sách |
| `fields/chiTietFields.ts` | ~30 cột lưới chi tiết + cascade tính lại |
| `fields/nguonColumns.ts` | Cột của hai popup chọn nguồn |
| `fields/tabColumns.ts` | Cột tab Thuế · tab Hạch toán |
| `fields/options.ts` · `fields/status.ts` · `fields/texts.ts` | Option enum · registry trạng thái · bundle chữ cho `@base` |
| `helpers/trangThai.ts` | Giá trị wire trạng thái + BR11/BR12/BR13 |
| `helpers/tinhToan.ts` | Số học một dòng (thành tiền · thuế · giá vốn · quy đổi) |
| `helpers/tongHop.ts` | Khối tổng + tab Thuế + **bút toán tự sinh** (3 bước của SCR) |
| `helpers/anHien.ts` | Bản CODE của ma trận ẩn/hiện (4 cột × 8 điều kiện + mức dòng) |
| `helpers/nguon.ts` | **BR1 · BR2 · BR5** — nạp/sắp/validate popup nguồn, đổ dòng sang lưới |
| `helpers/kiemTra.ts` | Kiểm tra trước khi lưu (MSG_104…MSG_112 + BR4) |
| `helpers/dongBo.ts` | Luật liên trường thuần (diễn giải · đồng bộ nhóm · kế thừa · hình thức TT) |
| `hooks/useDanhMucTraLai.ts` | Gom mọi danh mục + hệ số quy đổi + TK ngầm định theo tiền tố |
| `hooks/useDongBoTab.ts` | Nối luật liên trường vào form thật |
| `hooks/useNhanDongChiTiet.ts` | **Mới 2026-08-21** — 3 hàm tra nhãn (mã hàng · ĐVT · kho) cho panel chi tiết; chỉ 3 lookup, không phải 12 như popup |
| `fields/chiTietPanelColumns.ts` | **Mới 2026-08-21** — 11 cột bảng "Chi tiết hàng hóa" của panel dưới danh sách |
| `components/TraLaiHangBanTab.tsx` | State của màn danh sách + 3 luồng vòng đời |
| ~~`components/TraLaiHangBanListTable.tsx`~~ | **CODE CHẾT** — không file nào import từ khi màn dùng `traLaiHangBanModule.Page` (§0.3) |
| `components/TraLaiHangBanThemMoiModal.tsx` | KHUNG popup Thêm/Sửa/Xem/Nhân bản: form instance · nạp chứng từ · header/footer · lưu · 2 popup nguồn |
| `components/ThanThemMoi.tsx` | THÂN popup: hàng tùy chọn · thẻ "Nhập" · lưới · dải tổng. Tách ra vì mọi `Form.useWatch` phải chạy ở component CON của `<Form>` — xem §4 L10 |
| `components/GhiGiamCongNoTab.tsx` · `PhieuNhapKhoTab.tsx` · `ChiTienTab.tsx` · `HoaDonTab.tsx` | Thân 4 nhóm tab |
| `components/ChonChungTuNguonModal.tsx` · `ChonHoaDonDieuChinhModal.tsx` | Hai popup chọn nguồn |
| `components/GridHeaderActions.tsx` · `TongHopPanel.tsx` | Góc phải thanh tab lưới · khối Tổng cộng |
| `i18n/vi.ts` · `i18n/en.ts` · `i18n/registerTraLaiHangBanI18n.ts` | MỘT namespace `traLaiHangBan` |
| `test/i18n.test.ts` | **Chốt chặn khóa i18n dựng ĐỘNG** — xem §4 L8 |
| `pages/TraLaiHangBanPage.tsx` · `pages/traLaiHangBan.css` | Entry lazy + stylesheet của màn |
| `test/themMoiModal.render.test.tsx` | **Ghim cấu trúc popup theo Figma 15756:47126** — thứ tự tab · thứ tự cột lưới · cột ẩn (§4 L10) |
| `test/*` (**8 file · 112 case**, đo 2026-08-21) | api · nguồn · tính toán+ẩn hiện · payload · render danh sách · i18n · render popup · cột panel chi tiết |

### Sửa file có sẵn (3 file, diff nhỏ)

| File | Sửa gì |
| --- | --- |
| `features/banHang/_shared/constants/banHangTabs.ts` | Thêm `traLaiHangBan → /ban-hang/tra-lai-hang-ban` vào `BAN_HANG_TAB_PATHS` + cập nhật ghi chú |
| `features/banHang/routes.tsx` | Thêm route `traLaiHangBan` (lazy) |
| — | `app/router/RootRoutes.tsx` **không phải sửa**: `gateByHandle(banHangRoutes)` đã có sẵn |

## 3. Đã reuse gì (khảo sát có bằng chứng)

Mẫu tham chiếu đọc TRƯỚC khi code: `client/src/features/banHang/chungTuBanHang/` (toàn bộ 20 file
nguồn) + `hoaDonBanHang/pages/HoaDonBanHangPage.tsx` + `_shared/constants/banHangTabs.ts`.

**Component `@base` dùng lại — không tự viết cái nào:**

| Component | Dùng ở |
| --- | --- |
| `CommonListTable` | danh sách · tab Thuế · tab Hạch toán · 2 lưới popup nguồn |
| `CommonEditableGrid` | lưới chi tiết hàng hóa |
| `CommonModalShell` | popup Thêm/Sửa/Xem + 2 popup nguồn |
| `CommonConfirmModal` | xóa · ghi sổ · bỏ ghi sổ · xác nhận kế thừa |
| `HeaderControls` | cụm "Chọn chứng từ" trên thanh tiêu đề (3 nguồn của Figma) |
| `TabMenu2Level` · `TabMenuChild` | thanh 4 tab nhóm Bán hàng · tab trong popup |
| `useListFilter` · `CommonFilterPanel` | phễu ngày + lọc nâng cao + chip (BR11) |
| `RowActionButtons` · `CommonActionMenu` | con mắt + menu ⋮ |
| `TotalBreakdown` | khối Tổng cộng (chế độ 2 cột khi ngoại tệ) |
| `CommonSelectBox` · `CommonTextBox` · `CommonTextArea` · `CommonNumberInput` · `CommonDatePicker` · `CommonCheckbox` · `FieldLabel` · `CommonButton` · `Card` · `CommonEmpty` · `Tooltip` | mọi ô nhập/nhãn |
| `createSearchApi` · `createSearchQueries` (`@platform`) | toàn bộ vòng đời CRUD |
| `PERIOD_PRESET` · `formatNumber` (`@core`) | preset phễu ngày · định dạng số dòng tổng |

**Không có component nào phải tự viết mới ngoài component riêng của màn** (4 tab thân + 2 popup
nguồn + panel tổng + 2 bảng) — đó đều là UI mang nghiệp vụ của riêng màn này nên đúng chỗ ở
`<module>/components/`.

**Không thêm prop nào vào `@base`** trong lần này.

## 4. Lệch so với tài liệu / thiết kế

| # | Lệch gì | Vì sao | Ảnh hưởng |
| --- | --- | --- | --- |
| L1 | **Figma ↔ Ma trận — hai cột chiết khấu của lưới.** Figma (biến thể "Không chiết khấu") KHÔNG vẽ "Chiết khấu %" / "Tiền chiết khấu"; Ma trận ghi `Show` ở cả 4 cột tổ hợp. | Chọn theo **Ma trận** (nguồn sự thật cho behavior): cột luôn hiển thị, chỉ **khóa ô** khi Loại chiết khấu = "Không chiết khấu" — cùng quy ước với `chungTuBanHang`. | Cần BA/Design chốt: ẩn cột hay khóa ô. `helpers/anHien.khoaOChietKhauDong` là chỗ duy nhất phải sửa. |
| L2 | **Mã hàng trên lưới** — Ma trận ghi `Show`, BR5 ghi "Disable, không cho sửa" (Điểm cần xác nhận #2 của chính ma trận). | Code đọc HỢP NHẤT cả hai: lập TAY → sửa được; lập TỪ chứng từ nguồn → khóa (vẫn xóa được cả dòng, đúng ghi chú BR5). | Chờ BA chốt. `helpers/anHien.khoaMaHang`. |
| L3 | **"Tự động áp giá"** — Ma trận ghi `Disable` (bảng trường nói N), BR14 mô tả NSD tự tick (Điểm cần xác nhận #3). | Code theo **BR14** (cho tick), vì ô này là công tắc bật/tắt của chính BR14 — để `Disable` thì BR14 không còn nhánh nào chạy được. | Chờ BA chốt. `fields/chiTietFields.ts` cột `giaTrungBinh`. |
| L4 | **Cột "Chiết khấu thương mại"** — BR13 tham chiếu ô tick này nhưng bảng trường lưới KHÔNG có cột (Điểm cần xác nhận #4). | Đã dựng cột (BR13 cần nó mới diễn đạt được). | Nếu BA nói không có, xóa 1 cột + 2 predicate. |
| L5 | **Vị trí màn** — Figma vẽ "Trả lại hàng bán" là TAB của trang Chứng từ bán hàng. | Luật tầng cấm leaf import leaf anh em → mỗi tab là một route riêng. Đã dùng đúng cơ chế `_shared/constants/banHangTabs.ts` mà repo vừa dựng cho `hoaDonBanHang`: thanh tab vẫn đủ 4 mục, bấm tab khác là ĐIỀU HƯỚNG. | Không — người dùng thấy đúng như Figma. |
| L6 | ~~**Nhãn quyền**~~ — **ĐÃ ĐÓNG 2026-08-21**: SCR bản mới ghi thẳng `TraLaiHangBan.Create` · `.View` · `.View.Detail`, đúng bộ mã `constants/permissions.ts` đang dùng. | Tài liệu cũ ghi `PMKT.E06469.*`; code chọn theo `MaChucNang.TRA_LAI_HANG_BAN` của BE. | Không phải sửa gì. |
| L9 | **Đã sửa LÂY sang 2 module anh em** — `dieuChinhGiaHangBan` và `hoaDonBanHang` dính đúng lỗi preset (camelCase thay vì UPPER_SNAKE). | Cùng một builder `t(\`…filter.presets.${id}\`)`, cùng một cách đặt tên sai. | Đã sửa `vi.ts`/`en.ts` của cả hai + thêm `test/i18n.test.ts` cho mỗi module (đã kiểm ngược). Không đụng file nào khác của hai module đó. ⚠ Hai module này đang được phiên khác dựng dở — báo lại để tránh sửa chồng. |
| L8 | **Đã sửa: khóa i18n dựng ĐỘNG bị trượt** — dropdown "Kỳ" và viên thuốc kỳ in ra `filter.presets.MONTH_TO_DATE`; toast của hai lỗi chiết khấu in ra `msg.phanTramCkVuot100`. | Khóa preset phải trùng NGUYÊN VĂN id `PERIOD_PRESET` (UPPER_SNAKE), tôi đặt camelCase; hai mã của `MA_LOI` thì nằm nhầm nhánh `themMoi.tb.*` thay vì `msg.*`. Không lỗi biên dịch/lint nào bắt được. | Đã sửa cả `vi.ts`/`en.ts` **và** thêm `test/i18n.test.ts` chặn cứng: đối chiếu mọi khóa động với chính hằng số sinh ra nó + khớp khóa `vi` ⇄ `en` 1-1. Đã kiểm ngược (đổi lại camelCase → test đỏ đúng chỗ). |
| L7 | **Enum wire chưa đối chiếu được với BE** — **ĐÓNG MỘT NỬA 2026-08-21** | BE đã có `TraLaiHangBanDto` với javadoc *"khớp `traLaiHangBanRowSchema` của FE"* (quyết định D7 của kế hoạch BE) ⇒ phần **header** đã đối chiếu được: tên trường trùng khớp, `trangThaiChungTu` là TÊN HẰNG. | Phần **dòng chi tiết** và các enum của luồng ghi (`PHUONG_THUC_LAP_HOA_DON`, `LOAI_CHIET_KHAU`, `NGUON_CHUNG_TU`, `LOAI_DIEU_CHINH`) vẫn chưa có DTO nào để đối chiếu — phải soát lại khi BE lên F2 · F3. |
| L10 | **Đã sửa: popup Thêm mới bám lại Figma node 15756:47126** (user đối chiếu và báo lệch). | Bản dựng đầu bám node 15756:46675 — cùng màn nhưng khác biến thể. | Xem bảng "L10 — đã sửa gì" ngay dưới. |
| L11 | **"Loại tiền" ở góc phải thanh tab lưới — Figma KHÔNG vẽ**, chỉ có "Chiết khấu". | Cả hai node (46675 · 47126) đều là biến thể VND. Bỏ ô này thì `đk-QĐ`/BR18 mất công tắc: không còn cách chọn ngoại tệ nên tỷ giá + 4 cột quy đổi + 2 dòng tổng quy đổi thành code chết. | **Đang giữ ô Loại tiền**, chờ user/BA chốt. Bỏ = sửa `components/GridHeaderActions.tsx` + gỡ nhánh `ngoaiTe`. |
| L12 | **Đã bật panel "Chi tiết hàng hóa" dưới danh sách** (user báo thiếu so với ba màn chứng từ còn lại). | Descriptor từng khai `capabilities.listCon = false` với lý do "SCR không vẽ panel" — **lý do đó nay SAI**: bản SCR ngày 2026-08-14 đã có hẳn mục **§Thông tin chi tiết** đặc tả vùng này (chọn dòng → hiện readonly dưới danh sách, header "Số chứng từ: …", chỉ hiện khi có `TraLaiHangBan.View.Detail`). | Bỏ `capabilities`, khai `chiTietTabLabelKey`, thêm `fields/chiTietPanelColumns.ts` + `hooks/useNhanDongChiTiet.ts`, tiêm `lineColumns` từ `TraLaiHangBanTab`. **Còn lệch 2 điểm** so với SCR mới: (a) tab chưa "hiện theo dữ liệu" — luôn đúng 1 tab; (b) chạy API thật thì bảng rỗng vì `GET /{id}` chưa trả `chiTiet` (§0.2). |
| L13 | **Bảng chính lệch SCR mới** — SCR đổi cột đầu thành **Ngày chứng từ** (BR21) và **Tổng tiền** (BR24, công thức ∑ dòng), thêm cột **Trạng thái thanh toán** (BR28) và cột **Chọn**. | Code đang hiển thị *Ngày hạch toán* + *Tổng thanh toán* (`tongTienThanhToanQuyDoi`) theo bản SCR cũ; hai cột mới thì **wire chưa có** — `TraLaiHangBanDto` không trả `trangThaiThanhToan`, và cột Chọn chỉ có nghĩa khi có API hàng loạt. | **CHƯA sửa** — cần chốt với BA + BE, xem [§8](#8-backlog-fe-sau-rà-soát-2026-08-21). Đổi nhãn/cột là sửa `fields/columns.ts` + `i18n/*`; phễu ngày (`dateField: 'ngayHachToan'`) phải đổi cùng lúc với BE nếu BA chốt lọc theo Ngày chứng từ. |
| L14 | **Thao tác hàng loạt (BR14 · BR15 · BR16)** — SCR mới đưa hẳn 3 nút lên thanh công cụ + cột tick chọn. | Engine `chungTu` có sẵn Nhóm C, nhưng descriptor **không khai** vì BE chưa có endpoint `*-hang-loat` (§0.2). | **CHƯA làm** — mở được ngay khi BE lên F5/F7/F8; FE chỉ phải khai endpoint + `docKetQuaHangLoat`. |
| L15 | **FE đang gọi API cho những luồng BE chưa cài** — `DUNG_MOCK = false` bật cho toàn bộ adapter, trong khi BE mới có phần ĐỌC. | Phiên khác bật cờ khi F1 lên. Hệ quả: Lưu / Sửa / Xóa → 400 `CHUA_HO_TRO`, Ghi sổ / Bỏ ghi sổ → 404. | **CẦN QUYẾT ĐỊNH** (§8-A1): hoặc chấp nhận (thông báo lỗi của server đã đọc được), hoặc tạm ẩn nút cho tới khi F3–F8 lên. Không tự ý bật lại mock — mock che mất trạng thái thật. |
| L16 | **Trường mới trên các tab của popup** — SCR bổ sung: Hóa đơn (Người mua hàng · Mã số ĐVQHNS · CCCD · Hộ chiếu · Điện thoại · Lý do điều chỉnh) · Phiếu chi/UNC/Séc (Kèm theo · Chứng từ gốc · Số giấy tờ · Nơi cấp) · PNK (Người giao hàng). | Bản 2026-08-12 code theo SCR cũ. | **CHƯA đối chiếu từng ô** — việc này cần soát 4 file tab với bảng trường SCR mới, xem §8-B2. |

**L10 — đã sửa gì (theo Figma 15756:47126):**

| Chỗ | Trước | Sau |
| --- | --- | --- |
| Thứ tự tab thẻ "Nhập" | Ghi giảm công nợ · Phiếu nhập kho · chi tiền · Hóa đơn | Ghi giảm công nợ · **chi tiền** · Phiếu nhập kho · Hóa đơn |
| Hàng tùy chọn | có kẻ dọc ngăn nhóm | bốn ô tick/chọn chạy liền mạch, **không kẻ dọc** |
| Tab Ghi giảm công nợ · Phiếu nhập kho | "Mã số thuế" nằm cạnh Tên khách hàng | "Mã số thuế" xuống **cột trái** hàng 2; nhãn NV bán hàng đủ chữ |
| Tab Hóa đơn | bố cục riêng | dùng CHUNG `.pmkt-tlhb-tm-body` (lưới 2 cột · kẻ dọc · cột phải 300) + thanh chọn hóa đơn (ô chọn khóa + nút ≡🔍) + dải thông tin nền xanh |
| Mẫu số hóa đơn | ô nhập chữ | **select** (`useMauSoHoaDonLookup`) |
| Cột lưới | có "TK giá vốn" · "Chiết khấu thương mại" | ẩn hai cột Figma không vẽ; hai cột CK ẩn theo biến thể "Không chiết khấu" |

**Kèm theo L10 — một lớp lỗi của antd v6 đã ghim bằng test:** `Form.useWatch` bỏ qua lần đăng ký
đầu khi được gọi từ **chính component đang dựng `<Form>`** (`formInstance._init` còn false ở render
đó, cả hai effect của `useWatch` `return` sớm) — ma trận ẩn/hiện vì thế chỉ đúng từ lần re-render
sau. Đã tách toàn bộ khối watch xuống `components/ThanThemMoi.tsx` (con của `<Form>`) và cụm chọn
nguồn ở header xuống `ChonNguonHeader`. Ngoài ra `WatcherCenter` của antd v6 gom thông báo watch vào
**một macro task** (`MessageChannel`), nên test phải nhường một nhịp sau mỗi `fireEvent.click` —
`test/themMoiModal.render.test.tsx` có helper `tich()` làm đúng việc đó, kèm ghi chú.

## 5. Nợ kỹ thuật

| # | Nợ | Chi tiết |
| --- | --- | --- |
| N1 | **`api/mock.ts` — nay là code chết** | BE đã lên phần ĐỌC và `DUNG_MOCK = false` (2026-08-14), nên hai khối override trong `api/chungTuModule.ts` + `mockDoiTrangThai` không bao giờ chạy. Gỡ nợ = xoá `mock.ts`, xoá cờ `DUNG_MOCK` và hai khối override. Đã tạo việc riêng, **không gộp vào diff tính năng**. |
| N2 | **Hai popup chọn nguồn chưa có dữ liệu** | Lưới cần endpoint tra DÒNG HÀNG của chứng từ nguồn (kèm SL đã trả lại) và DANH SÁCH HÓA ĐƠN; `/chung-tu-ban-hang/search` chỉ trả header. **Kế hoạch BE đã chốt hai endpoint này** (D8 · F9: `POST {base}/nguon/chung-tu-ban-hang` · `POST {base}/nguon/hoa-don-dieu-chinh`) nhưng CHƯA cài. Hàm nạp được TIÊM qua props (`useNguonChuaCoApi`) nên nối API là sửa đúng một hook. |
| N3 | **Thao tác HÀNG LOẠT (BR14 · BR15 · BR16)** | SCR bản mới đưa 3 nút lên thanh công cụ + cột tick. Engine `chungTu` có sẵn Nhóm C + popup "thành công một phần", nhưng BE chưa có endpoint `*-hang-loat` nên descriptor cố ý không khai — thà không có nút còn hơn nút chỉ báo lỗi. Xem L14. |
| N4 | **Tab "Đính kèm" · "Tham chiếu"** | Dùng đặc tả chung (`Common/NguonDuLieu`), chưa dựng — hiện `CommonEmpty` có chữ giải thích. |
| N5 | **Ba danh mục chưa có endpoint** | Vụ việc · Hợp đồng · Số phiếu xuất (BR15) — cột vẫn dựng theo Figma, danh sách rỗng. |
| N6 | **"Hình thức TT" của tab Hóa đơn chưa cho nhập tay** | SCR cho phép nhập giá trị ngoài 3 mục; `CommonSelectBox` chưa có chế độ free-text một-giá-trị. Cần thêm prop vào `@base` hoặc chốt bỏ yêu cầu. |
| N7 | **"Lập HĐ điều chỉnh" · "Lập phiếu nhập kho"** | Hai mục ⋮ rời sang module khác (hóa đơn điều chỉnh / kho) — cả hai chưa dựng; hiện báo "đang phát triển". Mã quyền của chúng là GIẢ ĐỊNH. |
| N8 | **`GET /{id}` chưa trả `chiTiet`** | `TraLaiHangBanDto` không có trường dòng chi tiết (BE ghi rõ `layDongChiTiet` ngoài phạm vi đợt 1). Zod của FE khai `.nullish()` nên **không vỡ**, nhưng panel chi tiết dưới danh sách và lưới của popup Sửa/Xem/Nhân bản đều rỗng khi chạy thật. Không có việc gì để làm ở FE — chờ BE F2. |
| N9 | **Cột "Trạng thái thanh toán" (BR28) chưa có trên wire** | Nhãn *Chưa thanh toán / Đã thanh toán* suy từ chứng từ thanh toán liên kết (`ChungTuThanhToanId` → `cash_phieu_chi.TrangThai`); DTO hiện không trả. FE không tự suy được — dựng cột rỗng là bịa. Chờ BE. |

## 6. Kết quả cổng nghiệm thu

### Lần 3 — chạy 2026-08-21 (sau panel chi tiết + đợt rà soát này)

Theo cổng NHẸ của `client/CLAUDE.md` §15 (bản cập nhật 2026-08-13):

| Lệnh | Kết quả |
| --- | --- |
| `npx vitest run src/features/banHang/traLaiHangBan --reporter=dot` | **8 file · 112 case PASS** |
| `npx vite build` | ✓ built in 2,72s |
| `npx tsc -p tsconfig.app.json --noEmit` (chạy thêm vì có file mới) | 0 lỗi trong `features/banHang/**` |
| `npx eslint src/features/banHang/traLaiHangBan --max-warnings=0` | sạch |

⚠ **Chưa chạy** (§15.0 — chỉ chạy khi user yêu cầu hoặc đụng vùng chúng canh): `npm run lint`,
`npm run lint:boundaries`, full suite. Đợt này không đụng barrel · `@base` · `@domain-kit`.
⚠ **Chưa kiểm bằng mắt trên trình duyệt** ở cả ba lần: app chặn ở màn Đăng nhập, không dùng tài khoản
của user. Bằng chứng thay thế là test render thật (`traLaiHangBan.render.test.tsx` đi qua `GET /{id}`).

### Lần 2 — chạy 2026-08-13 (sau L8 · L9 · L10)

| Lệnh | Kết quả | Đối chiếu baseline |
| --- | --- | --- |
| `npx tsc -p tsconfig.app.json --noEmit` | **172 lỗi**, **0 lỗi** trong `src/features/banHang/**` | Baseline tài liệu 194 → không xấu hơn (phiên khác đã dọn bớt) |
| `npm run lint` | **11 vấn đề (9 lỗi + 2 cảnh báo)**, tất cả ở `src/legacy/` | Baseline 12 → không xấu hơn |
| `npx eslint src/features/banHang/traLaiHangBan` | **sạch (exit 0)**, `--max-warnings=0` | — |
| `npm run lint:boundaries` | **76 lỗi** = 74 "rule not found" + 2 `axios` trần trong `legacy` | Đúng baseline; `npx eslint src/features/banHang --config eslint.boundaries.config.js` → **exit 0** |
| `npx vitest run src/features/banHang/{traLaiHangBan,dieuChinhGiaHangBan,hoaDonBanHang}` | **19 file · 323 case PASS** (riêng `traLaiHangBan`: 7 file · 105 case) | — |
| `npx vite build` | ✓ built in 1.05s | — |

⚠ **Chưa kiểm được bằng mắt trên trình duyệt**: dev server chạy được nhưng app chặn ở màn Đăng nhập
và tôi không nhập tài khoản của user. Bằng chứng thay thế là `test/themMoiModal.render.test.tsx` —
render THẬT popup rồi đọc DOM (thứ tự tab · thứ tự cột · cột ẩn).

### Lần 1 — chạy 2026-08-12

| Lệnh | Kết quả | Đối chiếu baseline |
| --- | --- | --- |
| `npm run typecheck` | **192 lỗi** — 129 `features/danhMuc` · 39 `muaHang` · 16 `tienMat` · 6 `base/domainKit` · 2 khác. **0 lỗi trong `traLaiHangBan/`, `banHang/routes.tsx`, `banHang/_shared/`** | Baseline tài liệu 193–194 → **không xấu hơn** |
| `npm run lint` | **12 vấn đề (10 lỗi + 2 cảnh báo)**, TẤT CẢ ở `src/legacy/` | Đúng baseline tài liệu |
| `npx eslint src/features/banHang/traLaiHangBan src/features/banHang/routes.tsx src/features/banHang/_shared` | **sạch (exit 0)** — không dùng `eslint-disable` nào | — |
| `npm run lint:boundaries` | **76 lỗi** = 74 "rule not found" + 2 `axios` trần trong `legacy` | Đúng baseline; `npx eslint src/features/banHang --config eslint.boundaries.config.js` → **exit 0** (không sinh vi phạm tầng mới) |
| `npx vitest run src/features/banHang/traLaiHangBan` | **6 file · 99 case PASS** (chạy lại 3 lần, ổn định) | — |
| `npx vitest run` (toàn bộ) | 438 file · **4090 pass / 8 fail** — 8 ca đỏ nằm ở `app/layouts` (2), `app/router` — nhánh muaHang (1), `base/components` (2), `legacy` (3). **Không ca nào thuộc `banHang`** | Đỏ sẵn / việc dở của phiên khác |
| `npm run build` | `tsc -b` đỏ theo baseline repo (không phải file của module này); **`npx vite build` ✓ built in 1.19s** — app đóng gói được kèm module mới | — |

**Chưa chạy `npm run check:committed`**: chưa commit gì (client/CLAUDE.md §14 — không tự commit).
`git status` còn `?? src/features/banHang/traLaiHangBan/`. Trước khi commit phải `git add` TOÀN BỘ
thư mục module TRƯỚC, rồi mới commit `banHang/routes.tsx` + `_shared/constants/banHangTabs.ts` —
ngược lại là đúng công thức sinh lỗi `[UNRESOLVED_IMPORT]` ở CI (client/CLAUDE.md §15.1).

## 7. BR đã áp dụng

**Common BR (`pmkt-docs/ba/Common/business_rules.md`)**

| BR | Áp ở đâu |
| --- | --- |
| BR1 phân trang | `DANH_SACH_PAGE_SIZE = 20`, phân trang server |
| BR2 hiển thị & sắp xếp | `fields/columns.ts`, `DEFAULT_SORT` (BR17 của SCR) |
| BR3 popup | `CommonModalShell` + hộp xác nhận bỏ dở |
| BR5 combogrid | `HeaderControls` + `CommonSelectBox showSearch` |
| BR7 precision & làm tròn | `format: 'currency'`, `GIA_TRI_THUE_GTGT.precision` |
| BR8 khoảng thời gian | phễu ngày `useListFilter({ showTime })` |
| BR11 tìm kiếm/lọc/sắp xếp | `traLaiHangBanAdvFilterFields` + `persistKey` |
| BR12 trạng thái chứng từ | `helpers/trangThai.ts` (5 trạng thái, không phải 2) |
| BR13 nút thao tác | menu ⋮ theo trạng thái + quyền |
| BR14 chế độ & hành vi form | 4 chế độ `create/edit/view/clone` |
| BR15 validation | `helpers/kiemTra.ts` + rule của `CommonEditableGrid` |
| BR16 cảnh báo nghiệp vụ | BR4 số lượng vượt = cảnh báo, không chặn |
| BR17 kỳ kế toán | MSG_203/204 đã có chuỗi; **server quyết định** |
| BR18 ngoại tệ | `đk-QĐ` — tỷ giá + toàn bộ cột/tổng quy đổi |
| BR19 kiểm tra trùng | MSG_213 (số hóa đơn trùng) — chuỗi sẵn, server quyết |
| BR20 số chứng từ | ô Số chứng từ + khóa khi Sửa |
| BR21 grid chi tiết con | `CommonEditableGrid` |
| BR24 tooltip/help text | `FieldLabel tooltip` cho Mã số ĐVQHNS · CCCD |
| BR25 phân quyền | `constants/permissions.ts` + `gates` |
| BR26 toast/notification | `useToast` cho mọi luồng |
| BR28 multi-tenant | khóa react-query có phạm vi công ty/kỳ |
| BR29 chính sách xóa | soft delete + token khóa lạc quan `updatedAt` |
| BR30 ẩn/hiện cột | `showSettings` + `columnConfigKey` |
| BR31 dòng tổng | `summary` server-side, lùi về tổng trang |
| BR32 copy · BR38 group · BR39 xuất Excel | do `CommonListTable` cấp sẵn |
| BR33 màu trạng thái | `fields/status.ts` (green/gold/blue/default) |
| BR36 ghi sổ · BR42 bỏ ghi sổ | luồng xác nhận + `ghiSoChungTu`/`boGhiSoChungTu` |
| BR37 ngày hạch toán | đồng bộ sang mọi tab; SCR dòng 284 một chiều |
| BR43 trim · BR44 truncate | `chu()` ở payload · `textMode` ở cột |
| BR45 thao tác hàng loạt | ⚠ chưa đạt — xem N3 |
| BR46 trường hệ thống bắt buộc | `updatedAt` round-trip |

**BR riêng của epic**: BR1 · BR2 · BR3 · BR4 · BR5 · BR10–BR17 của SCR_DanhSach ·
BR_KhongTongHopToKhaiGTGT · BR-TLH-SAISOT · BR19 (bộ chứng từ, phần cảnh báo xóa).

**BR mới của SCR_DanhSach bản 2026-08-14** (rà 2026-08-21):

| BR | Trạng thái FE |
| --- | --- |
| BR18 điều kiện lập chứng từ liên kết | ✅ đã có sẵn — `rowActionsThem.visible` gác đúng "chưa ghi sổ + chưa có chứng từ liên kết" |
| BR21 định dạng ngày | ⚠ hiển thị DD/MM/YYYY đúng, nhưng cột đang là *Ngày hạch toán* — chờ A3 |
| BR22 chọn chứng từ (link mở chi tiết, gác `View.Detail`) | ✅ cột `soChungTu` là link → `moRow`; engine gác quyền |
| BR23 tên khách hàng đầy đủ | ✅ `textMode: 'long'` |
| BR24 định dạng tiền tệ | ✅ `format: 'currency'`; nhãn cột chờ B1 |
| BR25 · BR26 · BR27 nhãn Trả lại hàng / PT lập HĐ / Hình thức TT | ✅ `fields/status.ts` + `statusRegistry` |
| BR28 trạng thái thanh toán | ❌ chưa có — wire chưa trả (N9) |

**BR Common MỚI (bổ sung sau ngày code — rà 2026-08-21)**

| BR | Yêu cầu | Trạng thái FE |
| --- | --- | --- |
| BR47 dữ liệu mặc định của danh mục | Nguồn/quyền/ảnh hưởng khi Super Admin đổi dữ liệu mặc định | Không chạm màn này |
| **BR48 Xem dữ liệu ghi sổ** | Nút trên **Thêm mới · Sửa · Xem chi tiết**, mở form chỉ-xem các bút toán `SoCai`; **hai chế độ**: chưa ghi sổ → *Xem trước* (tính tại chỗ), đã ghi sổ → *Dữ liệu sổ* (**đọc thẳng `SoCai`, không tính lại**) | ❌ **Chưa đạt.** Module có tab "Hạch toán" tính tại chỗ (`helpers/tongHop.sinhButToan`) — đúng tinh thần chế độ *Xem trước*, nhưng: (a) không có nút/form riêng như BR48 mô tả; (b) chứng từ **đã ghi sổ** vẫn TÍNH LẠI thay vì đọc `SoCai` — sai đúng điểm BR48 nhấn mạnh. Engine `@domain-kit/chungTu` cũng chưa có gì cho việc này |
| **BR49 Di chuyển chứng từ trước–sau** | 2 mũi tên góc dưới-trái màn Xem chi tiết, duyệt theo đúng thứ tự đang sắp trên danh sách, disable ở đầu/cuối | ❌ **Chưa có.** Cần engine cấp (nó đang giữ danh sách + thứ tự), không nên dựng riêng trong module |

**BR chưa đạt**

| BR | Lý do |
| --- | --- |
| BR45 / BR14–BR16 hàng loạt | Chờ endpoint hàng loạt + popup "thành công một phần" (N3) |
| BR17 kỳ kế toán (chặn thật) | FE chỉ có chuỗi thông báo; kiểm kỳ là việc của server |
| BR19 kiểm tra trùng số hóa đơn | Như trên — MSG_213 sẵn sàng, server quyết định |
| BR-CORE-FREEZESIGN | Cần cờ `DaKeKhai` trên chi tiết hóa đơn — wire chưa có |

## 8. Backlog FE sau rà soát 2026-08-21

Sắp theo *ai đang chặn*, không theo độ khó. Mã trong ngoặc trỏ về mục giải thích ở trên.

### A. Chờ user / BA chốt — FE không tự quyết

| # | Câu hỏi | Vì sao không tự chọn được | Chạm vào đâu |
| --- | --- | --- | --- |
| A1 | Luồng GHI đang gọi vào endpoint BE chưa cài (Lưu/Sửa/Xóa → 400, Ghi sổ/Bỏ ghi sổ → 404). Để nguyên cho người dùng thấy lỗi server, hay **tạm ẩn/khoá** các nút đó tới khi BE lên F3–F8? (L15) | Ẩn nút là giấu chức năng đã đặc tả; để nguyên là để người dùng bấm vào lỗi. Cả hai đều có lý — người dùng quyết. | `api/chungTuModule.ts` (`anHanhDongTrenDong`) hoặc `components/TraLaiHangBanTab.tsx` |
| A2 | Ô **"Loại tiền"** ở góc phải thanh tab lưới: Figma không vẽ, nhưng bỏ nó là mất công tắc của BR18/`đk-QĐ` (L11 — hỏi từ 2026-08-13, chưa có trả lời) | Bỏ = 4 cột quy đổi + 2 dòng tổng quy đổi thành code chết | `components/GridHeaderActions.tsx` |
| A3 | Cột đầu bảng danh sách: SCR mới ghi **Ngày chứng từ**, code đang hiện **Ngày hạch toán** — và phễu ngày (cả FE lẫn BE) đang lọc theo `ngayHachToan` (L13) | Đổi cột hiển thị mà không đổi cột lọc thì người dùng lọc một đằng đọc một nẻo; đổi cả hai thì phải sửa cùng nhịp với BE | `fields/columns.ts` · `api/chungTuModule.ts` (`dateField`) · `i18n/*` |

### B. FE làm được ngay, không chờ ai

| # | Việc | Ghi chú |
| --- | --- | --- |
| B1 | Đổi nhãn cột **Tổng thanh toán → Tổng tiền** theo BR24 (giá trị `tongTienThanhToanQuyDoi` đã đúng công thức ∑) | 1 khoá i18n × 2 ngôn ngữ; làm cùng A3 để chỉ sửa `columns.ts` một lần |
| B2 | Soát 4 file tab của popup với bảng trường SCR bản 2026-08-14 (L16) — Hóa đơn · Phiếu chi/UNC/Séc · PNK | Việc SOÁT trước, có kết quả rồi mới ước lượng phần code |
| B3 | Ô tìm kiếm: SCR nâng max length 100 → 255 | Ô này do engine dựng — kiểm xem `chungTu` có prop độ dài không, thiếu thì thêm ở `@domain-kit` |
| B4 | Panel chi tiết: SCR nói *"tab hiện theo dữ liệu chứng từ"*, hiện luôn đúng 1 tab (L12) | Engine hỗ trợ `chiTietTabs`; chỉ làm được sau khi BE trả `chiTiet` (C1) — nếu không thì không biết chứng từ "có dữ liệu gì" |
| B5 | Dọn code chết: `api/mock.ts` + `components/TraLaiHangBanListTable.tsx` (N1 · §0.3) | Đã tách thành việc riêng, không gộp vào diff tính năng |

### C. Chờ BE — FE đã sẵn chỗ cắm

| # | Chờ gì | FE phải làm gì khi có |
| --- | --- | --- |
| C1 | **F2** — `chiTiet` trong `GET /{id}` (N8) | Không phải sửa gì: panel + popup đã đọc `chiTiet`; chỉ chạy lại test |
| C2 | **F3–F8** — Thêm/Sửa/Xóa/Ghi sổ/Bỏ ghi sổ (L15) | Bỏ phần xử lý tạm của A1 (nếu chọn ẩn nút) |
| C3 | **F9** — hai endpoint chọn chứng từ nguồn (N2) | Thay `useNguonChuaCoApi` bằng hàm gọi thật — đúng một hook |
| C4 | **BR28** — `trangThaiThanhToan` trên DTO (N9) | Thêm 1 cột + 1 nhánh `statusRegistry` |
| C5 | **BR14 · BR15 · BR16** — endpoint hàng loạt (L14 · N3) | Khai Nhóm C trong descriptor + `docKetQuaHangLoat`; engine lo phần còn lại |

### D. Việc MỚI phát sinh từ Common BR (nên làm ở `@domain-kit/chungTu`, không làm riêng trong module)

| # | Việc | Vì sao thuộc engine | Chặn bởi |
| --- | --- | --- | --- |
| D1 | **BR48 — "Xem dữ liệu ghi sổ"**: nút + form chỉ-xem, tự chọn chế độ *Xem trước* / *Dữ liệu sổ* theo trạng thái ghi sổ | Áp cho **mọi** loại chứng từ có ghi sổ; 4 màn chứng từ của nhóm Bán hàng đều cần. Riêng phần *Dữ liệu sổ* phải đọc `SoCai` lọc **đồng thời** `ChungTuId` + `LoaiChungTuId` — luật dễ làm sai, không nên nhân bản ở từng module | Cần endpoint đọc `SoCai` theo chứng từ (BE chưa có cho màn này) |
| D2 | **BR49 — mũi tên chứng từ trước / sau** ở màn Xem chi tiết, theo đúng thứ tự danh sách | Thứ tự và trang dữ liệu do controller của engine giữ; module không biết "chứng từ liền sau" là chứng từ nào | Không — FE làm được ngay khi engine mở điểm cắm |

> Hai việc D1 · D2 vượt phạm vi epic này (chạm `@domain-kit`, ảnh hưởng mọi màn chứng từ). Đề xuất
> **tách ticket riêng** thay vì nhét vào diff của E-06469 — ghi ở đây để không rơi mất.
