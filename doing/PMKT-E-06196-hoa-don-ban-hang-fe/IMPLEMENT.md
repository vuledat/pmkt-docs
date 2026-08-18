# IMPLEMENT — PMKT-E-06196 Hóa đơn bán hàng (FE)

> Nhật ký thi công của `/gen-fe`. **Không có plan FE** cho epic này — user chọn **code thẳng từ PYC**
> (`pmkt-docs/ba/PMKT-E-06196_HoaDonBanHang`), nên §1 (đọc bắt buộc) và §2 (khảo sát có bằng chứng)
> của `/plan-fe` được làm đầy đủ và ghi lại ở mục 3 bên dưới.

---

## 1. Ngày · phạm vi đã code

**Ngày:** 2026-08-12
**Figma:** node `14770-349117` (bộ popup) · `58263:162967` (danh sách + xem nhanh) ·
`14770:349569` (Dialog Box) · `61146:217365` (Xem dữ liệu ghi sổ — KHÔNG dựng, xem mục 5)

| Màn (SCR) | Trạng thái | Ghi chú |
| :-- | :-- | :-- |
| `SCR_HDBanHang_DanhSach` | ✅ Xong | Bảng 8 cột · dòng tổng BR31 · phễu ngày · lọc nâng cao · cấu hình cột · chọn hàng loạt · panel Xem nhanh |
| `SCR_HDBanHang_ThemMoi` | ✅ Xong | Trừ hai nút ghi sổ — xem mục 5 |
| `SCR_HDBanHang_CapNhat` | ✅ Xong | Dùng chung popup, thêm cảnh báo BR02 (MSG_056) lúc mở form |
| `SCR_HDBanHang_ChiTiet` | ✅ Xong | Dùng chung popup ở `mode='view'`, footer Cập nhật · Đóng |
| `SCR_HDBanHang_Xoa` | ✅ Xong | Xóa một dòng (BR10 đổi câu cảnh báo) + xóa hàng loạt + popup kết quả |

**Quyết định đã chốt với user trước khi code (2 câu hỏi chặn):**

1. **Ghi sổ** — Figma vẽ `Hủy · Xem dữ liệu ghi sổ · Lưu · Lưu và ghi sổ`, BA nói hóa đơn KHÔNG hạch
   toán. Chốt: **dựng UI theo Figma nhưng khóa sau cờ** `HDBH_CO_GHI_SO = false`.
2. **Vị trí màn** — Figma vẽ danh sách là **tab thứ 4** của thanh tab Bán hàng. Chốt: **module riêng
   + route riêng**, thanh tab điều hướng giữa các route, từ vựng tab đặt ở `banHang/_shared/`.

---

## 2. Danh sách file đã tạo / sửa

### Tạo mới — `client/src/features/banHang/hoaDonBanHang/` (28 file)

```
index.ts                                 cửa ra duy nhất của module (§5)
api/
  model.ts                               hợp đồng WIRE (Zod) — HoaDonBanHang + ChiTietHDBanHang
  hoaDonBanHangApi.ts                    adapter BASE-CRUD + toSearchRequest + xoaHoaDonHangLoat
  queries.ts                             hook react-query theo tenant
  mock.ts                                ⚠ NỢ — kho dữ liệu giả, gỡ khi BE lên
  lookups.ts                             7 danh mục master-data màn này cần
  payload.ts                             form → wire (cắt trường theo ngữ cảnh, trim, đổi kiểu)
  formDetail.ts                          wire → form (mở lại · lập từ chứng từ nguồn)
components/
  HoaDonBanHangTab.tsx                   giữ MỌI state: query · lọc · chọn · 3 luồng xóa/sửa
  HoaDonBanHangListTable.tsx             bảng danh sách (thuần trình bày)
  HoaDonBanHangQuickDetail.tsx           panel "Xem nhanh" + tay nắm thu/mở
  HoaDonBanHangThemMoiModal.tsx          popup Thêm / Sửa / Xem (một component, ba chế độ)
  ThongTinHoaDon.tsx                     section "Thông tin hóa đơn"
  ThongTinXuatKhau.tsx                   section "Thông tin xuất khẩu" (BR02)
  GridHeaderActions.tsx                  Loại tiền · Tỷ giá · Chiết khấu · Áp dụng · Phân bổ
  TongHopPanel.tsx                       khối "Tổng hợp tiền tệ"
  PhanBoChietKhauModal.tsx               popup phân bổ (2 biến thể trong 1 component)
constants/
  constants.ts                           enum wire · cờ HDBH_CO_GHI_SO · hình học · MAX_LEN
  paths.ts                               re-export path từ _shared
  permissions.ts                         mã quyền `LapHoaDonBan.*` (B4.3)
fields/
  types.ts                               hình dạng FORM-STORE + NguCanhAnHien
  columns.ts                             8 cột danh sách
  chiTietColumns.ts                      11 cột panel Xem nhanh
  chiTietFields.ts                       lưới nhập liệu — bản CODE của ma trận ẩn/hiện
  phanBoFields.ts                        lưới popup phân bổ
  options.ts                             option enum + nhãn thuế suất
  status.ts                              registry màu/nhãn 2 cột trạng thái
  texts.ts                               bó chữ cho component @base
helpers/
  tinhToan.ts                            BR09 · BR10 · BR16 · BR18 + thuế XK
  tongHop.ts                             khối tổng + định dạng ngoặc đơn
  chietKhau.ts                           BR11 + BR1–BR8 popup phân bổ
  anHien.ts                              bản CODE của 3 ma trận ẩn/hiện
  kiemTra.ts                             validate trước khi Lưu (mã MSG_*)
  trangThai.ts                           máy trạng thái nút của danh sách
  dongBo.ts                              BR20 diễn giải + auto-fill khách hàng
hooks/
  useDanhMucHoaDon.ts                    gom 7 danh mục + 4 hàm suy ra
i18n/
  vi.ts · en.ts · registerHoaDonBanHangI18n.ts   một namespace `hoaDonBanHang`
pages/
  HoaDonBanHangPage.tsx                  chỉ ráp: thanh 4 tab + thân tab
  hoaDonBanHang.css                      CSS phạm vi màn
test/
  tinhToan.test.ts · anHien.test.ts · kiemTra.test.ts · payload.test.ts
  hoaDonBanHang.render.test.tsx
```

### Tạo mới — `client/src/features/banHang/_shared/` (1 file)

- `constants/banHangTabs.ts` — từ vựng thanh 4 tab + **nguồn DUY NHẤT** của mọi path nhóm Bán hàng.

### Sửa file có sẵn (4 file, diff nhỏ)

| File | Sửa gì | Vì sao |
| :-- | :-- | :-- |
| `banHang/routes.tsx` | thêm route `hoaDonBanHang`; `handleFor` nhận `crumbKey` đầy đủ thay vì lá cố định | mỗi module một namespace i18n nên crumb không dùng chung tiền tố `banHang:` được nữa |
| `banHang/chungTuBanHang/constants/paths.ts` | re-export path từ `_shared` | gom một bản duy nhất; hợp đồng export `BAN_HANG_PATHS` giữ nguyên nên `routes.tsx` và `menuRegistry.tsx` không phải sửa |
| `banHang/chungTuBanHang/pages/ChungTuBanHangPage.tsx` | thanh tab đọc `_shared`, bấm tab có module thì `navigate` | trước đây tab "Hóa đơn" hiện "đang phát triển" — nay đã có màn |
| `banHang/chungTuBanHang/test/chungTuBanHang.render.test.tsx` | bọc `MemoryRouter` + đổi 1 test sang khẳng định hành vi ĐIỀU HƯỚNG | **hồi quy do PYC này gây ra và đã sửa** — xem mục 6.1 |
| `base/components/modal/BulkDeleteResultModal.tsx` | thêm cột TÙY CHỌN `tenDoiTuong` | SCR_HDBanHang_Xoa đòi cột "Tên khách hàng"; theo luật reuse thì **thêm prop vào @base**, không copy component ra feature. Backward-compatible: không truyền heading thì bảng giữ nguyên 3 cột cũ |

---

## 3. Khảo sát reuse (§2 của `/plan-fe`) — có bằng chứng

### Đã reuse

| Thứ | Nguồn | Bằng chứng |
| :-- | :-- | :-- |
| Bảng danh sách + thanh công cụ + chip lọc + dòng tổng + chọn hàng loạt | `CommonListTable` | `@base` — `src/base/index.ts:310` |
| Lưới nhập liệu (ô, cascade, dòng ghi chú, phân trang, dòng Σ) | `CommonEditableGrid` | `src/base/index.ts:535` |
| Khung popup + guard "bỏ thay đổi" + footer 2 chế độ | `CommonModalShell` | `src/base/index.ts:258` |
| Popup kết quả xóa hàng loạt | `BulkDeleteResultModal` | `src/base/index.ts:293` |
| Popup xác nhận (xóa · cảnh báo BR02) | `CommonConfirmModal` | `src/base/index.ts:269` |
| Khối tổng 1–2 cột | `TotalBreakdown` | `src/base/index.ts:205` |
| Thanh 4 tab dạng thẻ | `TabMenu2Level` | `src/base/index.ts:142` |
| Tab con của panel/lưới | `TabMenuChild` | `src/base/index.ts:144` |
| Phễu ngày + lọc nâng cao + chip | `useListFilter` · `CommonFilterPanel` | `src/base/index.ts:501` · `:476` |
| Cụm "Chọn chứng từ" ở header popup | `HeaderControls` | `src/base/index.ts:277` |
| Menu ⋮ + nút hàng trên dòng | `CommonActionMenu` · `RowActionButtons` | `src/base/index.ts:342` · `:340` |
| Ô nhập | `CommonTextBox` · `CommonNumberInput` · `CommonSelectBox` · `CommonDatePicker` · `FieldLabel` | `src/base/index.ts:172`, `:160`, `:572`, `:166`, `:188` |
| Adapter CRUD + query theo tenant | `createSearchApi` · `createSearchQueries` | `@platform` — `src/platform/index.ts:141`, `:143` |
| Preset kỳ | `PERIOD_PRESET` (`@core`) | dùng ở `fields/texts.ts` |
| Toàn bộ **kiến trúc module** (9 lớp, một namespace i18n, cách chú thích) | `features/banHang/chungTuBanHang/` | mẫu tham chiếu duy nhất — `client/CLAUDE.md §5` |

### Phải viết mới — kèm lý do không reuse được

| Viết mới | Lý do |
| :-- | :-- |
| `helpers/*` (tinhToan · tongHop · chietKhau · anHien · kiemTra · trangThai · dongBo) | Luật nghiệp vụ CÙNG NGUỒN với `chungTuBanHang` nhưng luật tầng **cấm leaf import leaf anh em** (`eslint.boundaries.js`, chính sách `leaf`). Bản của hóa đơn cũng là TẬP CON thật sự: bỏ hẳn nhóm giá vốn (CTBH BR21) và mọi bút toán. Xem mục 6 — đã đề xuất ticket gom lên `@domain-kit`. |
| `api/lookups.ts` | Cùng lý do; đây đúng là cách `chungTuBanHang/api/lookups.ts` và `danhMuc/kho/kho/lookups.ts` đang làm. Bản này chỉ có 7 danh mục thay vì 13. |
| `components/ThongTinHoaDon.tsx` · `ThongTinXuatKhau.tsx` | Bố cục trường của riêng màn này (Figma node 14770:349584) — không component `@base` nào vẽ một section form nghiệp vụ. |
| `components/*Tab · *ListTable · *QuickDetail · *ThemMoiModal · TongHopPanel · GridHeaderActions · PhanBoChietKhauModal` | Mang logic nghiệp vụ của riêng màn; phần trình bày thuần đã đẩy hết xuống `@base`. |
| Tay nắm thu/mở của panel Xem nhanh (markup cục bộ trong `HoaDonBanHangQuickDetail`) | Không có component `@base` nào vẽ viên thuốc 76×20 vắt qua mép thẻ; `IconButton` là ô vuông 32×32 có viền, hình dạng khác hẳn. Nhãn vẫn đi qua `Tooltip` của design system. |

---

## 4. Lệch so với tài liệu — **phải đọc**

### 4.1. Figma ↔ BA (đã hỏi user, đã chốt)

| # | Figma nói | BA nói | Đã làm |
| :-- | :-- | :-- | :-- |
| 1 | Footer popup có **Xem dữ liệu ghi sổ · Lưu và ghi sổ**, kèm popup bút toán (node 61146:217365) | `SCR_HDBanHang_ThemMoi` §Chức năng chỉ có **Hủy · Lưu**; BR04 "không phát sinh bút toán"; `DanhSachQuyen.md` B4.3 bỏ trống cả Ghi sổ lẫn Bỏ ghi | Dựng layout theo Figma, **khóa sau cờ `HDBH_CO_GHI_SO = false`**. Bật `true` là hiện lại — nhưng khi đó **phải bổ sung hợp đồng API ghi sổ vào PYC** (hiện chưa có) và mã quyền `LapHoaDonBan.Post/.Unpost` (danh mục chưa cấp). |
| 2 | Cột trạng thái in **"HĐ mới"**, "HĐ thay thế", "HĐ điều chỉnh" | BR06 gọi là **"Hóa đơn gốc"**, "Hóa đơn thay thế", "Hóa đơn điều chỉnh" | Lấy theo **BR06** — Figma là nguồn của bố cục, không phải của thuật ngữ nghiệp vụ. Có test khóa lại (`hoaDonBanHang.render.test.tsx`). |
| 3 | Section Thông tin hóa đơn có ô **"Nhân viên bán hàng"** | Bảng trường của `SCR_CTBH_ThemMoi` §Tab Hóa đơn **không liệt kê** ô này | Giữ theo **Figma** (nguồn của UI). Cần BA xác nhận trường này có lưu không. |
| 4 | Khối tổng có dòng **"Chi phí"** | `SCR_HDBanHang_ThemMoi` §Tổng hợp tiền tệ không có dòng này | Dựng dòng đó nhưng **luôn = 0**: chưa có cột nào trên lưới ghi vào `chiPhi` và wire chưa có trường. Cần BA chốt nguồn dữ liệu. |
| 5 | Lưới có cột **Số lô · Hạn sử dụng** | Ma trận Thêm mới dòng 49 **không liệt kê** hai cột này (nhưng cũng không nằm trong danh mục cột bị loại ở dòng 40) | Giữ theo **Figma**. |
| 6 | Lưới có cột **Số chứng từ** (`CT00291`) | Bảng trường không nêu | Giữ theo **Figma**, dựng là ô chỉ-đọc (`soChungTuNguon`) — nó là dấu vết hóa đơn được lập TỪ một chứng từ. |

### 4.2. Mâu thuẫn NỘI BỘ tài liệu BA

| # | Chỗ A | Chỗ B | Đã chọn |
| :-- | :-- | :-- | :-- |
| 7 | `SCR_HDBanHang_DanhSach` §Chức năng: nút "Xóa hàng loạt" **disable** nếu có ≥1 hóa đơn đã phát hành | `SCR_HDBanHang_Xoa` BR7: hệ thống **chỉ xóa** hóa đơn "Chưa phát hành", các hóa đơn đã phát hành **được liệt kê trong popup kết quả** | Chọn **BR7 + BR45 §2** (cho chạy rồi báo cáo). Disable nút từ đầu thì popup "Kết quả xóa hàng loạt" (BR8 bắt buộc luôn hiện) không bao giờ có đường xuất hiện. |
| 8 | `SCR_HDBanHang_Xoa` §Popup kết quả: tiêu đề "Kết quả xóa hàng loạt", cột STT · Ngày HĐ · Số HĐ · Tên KH · Lý do lỗi | Quy chuẩn chung **BR45 §3**: tiêu đề "Thông báo kết quả \[Tên thao tác\]", cột Số chứng từ · Ngày chứng từ · Nguyên nhân | Chọn **epic** (thắng trong đúng phạm vi epic — `CLAUDE.md` luật 3). **Đang lệch BR45 §3** ở tiêu đề và bộ cột. |

### 4.3. Lệch mã tham chiếu trong tài liệu (không chặn, nhưng nên sửa doc)

- `SCR_HDBanHang_ThemMoi.md` trỏ tới `SCR_CTBH_ThemMoi.md#BR08 / #BR10 / #BR11 / #BR12 / #BR17 /
  #BR18 / #BR19`. File CTBH hiện tại đánh số **lệch 1** cho mọi BR ≥ 07: auto-fill KH là **BR07**
  (không phải BR08), thuế GTGT là **BR10** (không phải BR11), chiết khấu là **BR11** (không phải
  BR12), ĐVT quy đổi là **BR16** (không phải BR17), theo dõi SL đã xuất là **BR17** (không phải
  BR18), SL–ĐG–TT là **BR18** (không phải BR19), quy đổi tỷ giá là **BR09** (không phải BR10).
  Các tham chiếu BR02 · BR03 · BR05 · BR06 thì **khớp**.
  → Code bám theo **NỘI DUNG** của CTBH hiện hành. Đề nghị BA cập nhật lại số hiệu trong
  `SCR_HDBanHang_ThemMoi.md`.
- `chungTuBanHang/constants/permissions.ts` khai `HOA_DON_BAN_PERM = { view: 'HoaDonBan.View', … }`
  và tự ghi chú là ASSUMED. Danh mục quyền B4.3 nói mã thật là **`LapHoaDonBan`**. Module này dùng
  `LapHoaDonBan`; bộ `HoaDonBan.*` bên kia là **mã sai cần dọn** — ngoài phạm vi PYC nên không sửa.

---

## 5. Nợ kỹ thuật

| # | Nợ | Gỡ thế nào |
| :-- | :-- | :-- |
| N1 | **`api/mock.ts` — BE chưa có.** `cell-app/cell/` không có module `hoa_don_ban_hang`, nên toàn bộ lời gọi bị chặn trong trình duyệt. | 1) `HDBH_DUNG_MOCK = false` ở `api/hoaDonBanHangApi.ts`; 2) đối chiếu từng khóa `api/model.ts` với DTO thật; 3) **xóa `mock.ts`** + dòng import. `hoaDonBanHang.render.test.tsx` khi đó phải đổi sang stub `http.get/post`. |
| N2 | **Hợp đồng API là ĐỀ XUẤT của FE**, dựng từ bảng trường CTBH + danh mục cột bị loại. Chưa có BE xác nhận. | Rà `api/model.ts` khi module BE lên. |
| N3 | **Enum lấy từ hằng số, không từ `/lookup`.** CTBH gọi `POST /lookup` để BE khai danh sách hợp lệ; hóa đơn chưa có endpoint đó. | Đổi `fields/options.ts` sang đọc `/lookup` khi BE lên. |
| N4 | **Hai nút ghi sổ khóa sau cờ** `HDBH_CO_GHI_SO` (mục 4.1 #1). | Chờ BA chốt. |
| N5 | **Cột "Hóa đơn liên quan" in TEXT, chưa bấm được.** BR07 nói mỗi số hóa đơn phải là link tới chi tiết; giá trị là một MẢNG quan hệ mà `ListField` của `@base` chưa có renderer nhiều-liên-kết. | Thêm renderer vào `@base`, hoặc BA chấp nhận text. |
| N6 | **Nguồn "Chọn chứng từ" ở header popup đang trỏ vào chính danh sách hóa đơn**, chưa phải Chứng từ bán hàng. Module CTBH là leaf anh em nên không import adapter của nó được. | Đẩy adapter CTBH xuống `@domain-kit/chungTuNguon`, hoặc BE mở một endpoint nguồn dùng chung. |
| N7 | **`soLuongConLaiChoPhep` (trần MSG_019) chưa có nguồn cấp.** `formDetail.toFormValuesTuChungTuNguon` đã nhận hàm tiêm và `kiemTra` đã bắt lỗi — chỉ thiếu số liệu từ CTBH. | Nối khi có N6. |
| N8 | **"Địa điểm giao" dựng là ô TEXT**, CTBH đặc tả là Combobox từ `ENT_DiaChiGiaoHang`. | Danh mục chưa có endpoint trong cell-app. |
| N9 | **Trùng lặp helper với `chungTuBanHang`** (~500 dòng số học BR chung). | Ticket riêng: gom `tinhToan/tongHop/chietKhau` + bộ adapter master-data lên `@domain-kit/chungTu`. **Không làm trong PYC này** (`CLAUDE.md`: không refactor ngoài phạm vi). |
| N10 | **Tab "Điều chỉnh hàng bán" trỏ tới route chưa đăng ký.** `_shared/banHangTabs.ts` khai `/ban-hang/dieu-chinh-gia-hang-ban` nhưng `routes.tsx` chưa có route đó (module `dieuChinhGiaHangBan` đang dựng song song, chưa có `pages/`). Bấm tab đó hiện rơi vào 404. | Việc song song hoàn tất là hết. |

---

## 6. Kết quả cổng nghiệm thu

Chạy tại `client/` bằng đường dẫn tuyệt đối.

| Lệnh | Kết quả | Đánh giá |
| :-- | :-- | :-- |
| `npm run typecheck` | **192 lỗi toàn repo · 0 lỗi trong file của PYC này** | ✅ Baseline `client/CLAUDE.md §15` ghi 194 (đo 2026-08-08); hiện 192. Lỗi nằm ở `danhMuc/**`, `muaHang/**`, `tienMat/**`, `base/domainKit`, và hai module `banHang` đang dựng song song. |
| `npm run lint` | **11 lỗi + 2 warning, TẤT CẢ trong `src/legacy/`** · 0 trong file của PYC này | ✅ Đúng baseline |
| `npm run lint:boundaries` | **78 lỗi**, trong đó **76 là "Definition for rule … was not found"** (không phải vi phạm tầng) và **2 vi phạm thật** — cả hai là `axios` trần trong `src/legacy/` | ✅ Đúng baseline (nợ cũ = 2). **0 lỗi `boundaries/*`** → thiết kế `_shared` hợp luật tầng |
| `npx vitest run src/features/banHang/hoaDonBanHang/test` | **5 file · 118/118 test PASS** | ✅ |
| `npx vitest run` trên **mọi file PYC này chạm** (`hoaDonBanHang` + `chungTuBanHang` + `base/components/modal` + `test/boundaries`) | **23 file · 369/369 test PASS** | ✅ |
| `npm run test` (toàn repo) | **19 file đỏ / 438** — sau khi sửa hồi quy 6.1 còn **18 file, KHÔNG file nào thuộc PYC này** | ⚠ Đỏ sẵn + việc song song, xem 6.2 |
| `npm run build` | **Đỏ** vì `tsc -b` gặp baseline 192 lỗi — **0 lỗi trong file của PYC này** | ⚠ Đỏ sẵn từ trước |
| `npx vite build` (bỏ qua tsc baseline) | **✓ built in 2.18s**; sinh đúng chunk lazy `hoaDonBanHang-HN7DeTIj.js` + `hoaDonBanHang--tcKcjyk.css` | ✅ Module code-split đúng, không kéo vào chunk eager |

> **Về `npm run build`:** repo đã đỏ sẵn ở bước `tsc -b` trước khi có PYC này (`client/CLAUDE.md
> §15` ghi rõ baseline 194 lỗi typecheck). Đã kiểm riêng: không lỗi nào thuộc file của PYC này, và
> `vite build` đứng một mình thì xanh. Đây là **giới hạn baseline của repo, không phải hồi quy**.

### 6.1. Một hồi quy DO PYC NÀY GÂY RA — đã tìm ra và đã sửa

Đổi `ChungTuBanHangPage` sang điều hướng bằng `useNavigate` làm **29 test** của
`chungTuBanHang.render.test.tsx` đỏ:

```
Error: useNavigate() may be used only in the context of a <Router> component.
```

Harness của file đó render page KHÔNG có Router. Đã sửa hai chỗ, đều trong chính file test:

1. bọc `MemoryRouter initialEntries={['/ban-hang/chung-tu-ban-hang']}` + một `LocationProbe` nhỏ để
   đọc được `location.pathname`;
2. test *"keeps the built tab mounted (hidden) when another tab is selected"* mô tả hành vi CŨ (tab
   đổi tại chỗ, hiện "đang phát triển") — hành vi đó chỉ tồn tại khi màn Hóa đơn chưa có. Đổi thành
   *"navigates to the sibling screen when a tab with its own module is clicked"*, khẳng định
   `pathname === '/ban-hang/hoa-don-ban-hang'`.

Sau khi sửa: `chungTuBanHang` **29/29 PASS**.

### 6.2. 18 file còn đỏ ở suite toàn repo — quy trách nhiệm

Đã chạy lại từng file và truy nguyên; **không file nào thuộc PYC này**:

| File đỏ | Nguyên nhân |
| :-- | :-- |
| `app/layouts/test/AppLayout.test.tsx` (2 test) | **Việc song song**: `menuRegistry.tsx` (đang sửa dở, không phải diff của tôi) đổi mục "Tổng hợp" từ `disabled: true` thành mục gác quyền `KHOA_SO_PERM.view`; user của test không có quyền đó nên mục biến mất. |
| `app/router/test/Router.test.tsx` (2 test) | `danhMuc` — nhánh chết (`client/CLAUDE.md §4.1`), 129/192 lỗi typecheck của repo nằm ở đó. |
| `features/banHang/traLaiHangBan/test/…` | Test của **module đang dựng song song**, không phải của PYC này. |
| `base/components/dropdown/CommonDropdownBasic.test.tsx` · `base/components/navigation/test/CommonPagination.test.tsx` | `base/components/**` đang bị việc song song sửa (`git status`: `CommonListTable.tsx`, `CommonSearchGroup.tsx`, `listTableFormat.ts`, `CellText.tsx`, `tokens.ts`, `icons/index.ts`… đều `M`). |
| 5 file `src/legacy/**` | Vùng khóa, đỏ sẵn. |
| 3 file `base/domainKit/catalog/**` · `ReportShowcase` · `AcquireTokenCard` | Đỏ ở lượt chạy song song, **xanh khi chạy lại** — flaky, đúng cảnh báo `client/CLAUDE.md §13`. |

> Không dùng `git stash` để dựng mốc so sánh: cây làm việc đang có **rất nhiều** thay đổi chưa commit
> của người khác (`menuRegistry`, `base/components/**`, `chungTuBanHang/api|fields|i18n`,
> `muaHang/**`…), stash là nuốt mất việc của họ (`client/CLAUDE.md §14`). Việc quy trách nhiệm ở trên
> làm bằng cách đọc `git diff` của từng file liên quan.

### 6.3. Kiểm tay những luật lint KHÔNG bắt được

`client/CLAUDE.md §11.3` nói rõ `no-explicit-any` chỉ ở mức `warn` nên `any` **lọt** qua `npm run lint`.
Đã soát tay trên toàn module:

| Luật | Kết quả |
| :-- | :-- |
| `any` · `@ts-ignore` · `@ts-expect-error` · `as unknown as` | **0** ✅ |
| `eslint-disable` (§5 cổng nghiệm thu cấm dùng để dập lint) | **0** ✅ |
| `../../` trong module (luật cứng 3) | **0** ✅ |
| File ở GỐC module (luật cứng 1 — chỉ được `index.ts`) | đúng **1** file `index.ts` ✅ |
| Cân bằng khóa i18n vi ⇄ en (luật 2) | **313 = 313**, không khóa nào lệch ✅ |

> **Cổng cây commit (§15.1):** chưa commit gì (`client/CLAUDE.md §14` — không tự commit).
> **Trước khi commit phải:** `git add` toàn bộ file mới **TRƯỚC**, rồi mới sửa barrel/import trỏ tới
> chúng; `git status` sạch (không còn `??` trong `src/`); chạy `npm run check:committed`.
> Danh sách file mới xem mục 2 — đặc biệt **`features/banHang/_shared/constants/banHangTabs.ts`**,
> vì `chungTuBanHang/constants/paths.ts` (file đã commit) nay import từ nó: quên `git add` file này
> là **xanh 100% ở local, đỏ 100% ở deploy** đúng lớp lỗi §15.1 mô tả.

---

## 7. BR đã áp dụng / chưa đạt

### Quy chuẩn chung (`pmkt-docs/ba/Common/business_rules.md`)

| BR | Áp dụng ở đâu |
| :-- | :-- |
| BR1 phân trang | `DEFAULT_PAGE_SIZE = 20` · `PAGE_SIZE_OPTIONS` · phân trang server-side |
| BR2 hiển thị & sắp xếp | `fields/columns.ts` — `sorter: 'server'` cho 7 cột BA đánh `Y` |
| BR7 precision & làm tròn | `helpers/tinhToan.ts` · `money: true` trên mọi ô tiền |
| BR8 khoảng thời gian | phễu ngày `useListFilter({ defaultPreset: MONTH_TO_DATE })` |
| BR11 tìm kiếm/lọc | `hoaDonAdvFilterFields` + `toSearchRequest` + `persistKey` (giữ bộ lọc) |
| BR13.1 nút thao tác | `HoaDonBanHangListTable` — Thêm mới · Tìm · Làm mới · Xóa lọc · mắt · ⋮ |
| BR13.2 nút trên form | footer `CommonModalShell` — Hủy · Lưu (Xem: Cập nhật · Đóng) |
| BR14 chế độ form | một popup, ba `mode` (`create`/`edit`/`view`) |
| BR15 validation | `helpers/kiemTra.ts` + `rules` trên field; message "…không được để trống" theo BR15.1 |
| BR16 cảnh báo nghiệp vụ | popup MSG_055 (xóa) · MSG_056 (sửa) qua `CommonConfirmModal` |
| BR18 ngoại tệ | `(đk-LT)` — tỷ giá + toàn bộ cột/khối quy đổi |
| BR24 tooltip | `viewTooltip` · `moreTooltip` · tooltip tay nắm panel |
| BR25 phân quyền | `constants/permissions.ts` (`LapHoaDonBan.*`) + `gates` trong `HoaDonBanHangTab` |
| BR26 toast | `useToast` cho mọi thành công/lỗi |
| BR30 ẩn/hiện cột | `showSettings` + `COLUMN_CONFIG_KEY` |
| BR31 dòng tổng | `summary` từ server, `totalOf()` ưu tiên nó hơn tổng trang |
| BR34 sửa từ màn xem | footer màn Xem có nút "Cập nhật" → `onEditFromView` |
| BR43 trim | `chu()` trong `api/payload.ts` |
| BR44 truncate | `textMode: 'identity' \| 'long'` trên cột |
| BR45 thao tác hàng loạt | xóa hàng loạt: bỏ qua bản không hợp lệ + popup kết quả + reload |
| BR46 trường hệ thống | `updatedAt` round-trip làm token khóa lạc quan |

### BR chưa đạt (kèm lý do)

| BR | Lý do |
| :-- | :-- |
| **BR39 xuất Excel** | PYC không yêu cầu; `SCR_HDBanHang_DanhSach` §Chức năng không có nút Xuất Excel, và `DanhSachQuyen.md` B4.3 bỏ trống cột "Xuất Excel". |
| **BR32 copy · BR38 group** | Ngoài phạm vi PYC; BA không nêu. |
| **BR17 kỳ kế toán · BR36 ghi sổ · BR37 ngày hạch toán · BR42 bỏ ghi sổ** | **Không áp dụng** — hóa đơn bán hàng là chứng từ thương mại, KHÔNG hạch toán (BR04 của epic). |
| **BR19 kiểm tra trùng · BR20 số chứng từ** | Là luật SERVER (check trùng Số HĐ + Ký hiệu + Mẫu số — MSG_006). FE hiển thị message của server chứ không tự kiểm — không có endpoint kiểm trùng. |
| **BR45 §3 cấu trúc popup lỗi hàng loạt** | Lệch có chủ ý: theo epic `SCR_HDBanHang_Xoa` — xem mục 4.2 #8. |
| **BR21 grid chi tiết con** | Đã dùng `CommonEditableGrid`; các mục nhỏ của BR21 chưa đối chiếu từng dòng. |

### BR của epic (`SCR_HDBanHang_*`)

| BR | Trạng thái |
| :-- | :-- |
| DanhSach BR01 cột chức năng | ✅ `helpers/trangThai.coTheSua/coTheXoa` |
| DanhSach BR02 · BR03 trạng thái | ✅ `constants` + `fields/status.ts` |
| DanhSach BR04 lập chứng từ bán hàng | ⚠ Nút có, gác đúng trạng thái + quyền; **hành động báo "đang phát triển"** vì màn Thêm mới CTBH nằm ở leaf anh em (không import được) |
| DanhSach BR05 lập chứng từ bán dịch vụ | ⚠ Như trên; điều kiện "≥1 dòng dịch vụ" **đã kiểm** trước khi báo |
| DanhSach BR06 trạng thái hóa đơn | ✅ 5 trạng thái, nhãn theo BR (không theo Figma) |
| DanhSach BR07 hóa đơn liên quan | ⚠ Hiện TEXT, chưa bấm được — nợ N5 |
| ThemMoi BR01 auto-fill KH/mã hàng | ✅ `dongBo.autoFillTheoKhachHang` + `chiTietFields.chonMaHang` |
| ThemMoi BR02 tham chiếu CTBH (CK · KM · thuế · ĐVT · SL-ĐG-TT · thêm dòng · quy đổi) | ✅ toàn bộ `helpers/` |
| ThemMoi BR03 check trùng hóa đơn | ⚠ Luật server; FE hiển thị MSG_006 từ server |
| ThemMoi BR04 lưu & trạng thái | ✅ Không gửi `ghiSo`; mock đặt "Chưa phát hành"/"Chưa lập chứng từ" khi tạo |
| ThemMoi BR05 theo dõi SL đã xuất | ⚠ Logic + message MSG_019 đã có; thiếu nguồn cấp trần — nợ N7 |
| CapNhat BR01 validate | ✅ dùng chung |
| CapNhat BR02 cảnh báo khi mở form | ✅ MSG_056 qua `CommonConfirmModal`, chọn Hủy thì không mở form |
| Xoa BR1–BR5 popup xác nhận | ✅ `CommonConfirmModal` tone `danger` |
| Xoa BR7–BR9 xóa hàng loạt | ✅ bỏ qua bản không hợp lệ · luôn hiện popup kết quả · đóng thì reload |
| Xoa BR10 hệ quả khi đã lập chứng từ | ✅ đổi câu cảnh báo sang MSG_055 |
