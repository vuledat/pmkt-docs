# 03 · Bảng chỉnh *Thông tin đầu trang* và *Tiêu đề bản in*

| | |
|---|---|
| Mã màn | `SCR_ThietLapMauIn` — hai mục của cột phải |
| Nguồn SCR | `SCR:118-140` · `SCR:280-283` |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` |
| Figma | frame **4** `72163:26808` (Thông tin đầu trang) · frame **5** `72163:27460` (Tiêu đề) |
| File chính | `components/inspector/DauTrangInspector.tsx` · `components/inspector/TieuDeInspector.tsx` |
| Luật phủ | `R-TLMI-076…084` (nhóm F) · `R-TLMI-085…091` (nhóm G) |

---

# PHẦN A — *Thông tin đầu trang* (Figma frame 4)

## A1. Bố cục

```
Thông tin đầu trang
─────────────────────────────────────────────────────
☑ In khối Thông tin đầu trang trên mẫu này
Dòng in ra                         Theo thiết lập chung  ← link ĐỎ, mức NHÓM
☑ Tên đơn vị
   CÔNG TY CP CÔNG NGHỆ BIZ                             ← giá trị THẬT, chữ mờ
☑ Địa chỉ
   Tầng 6, Tòa nhà Tech, Số 1 Đường ABC, Phường X, Quận Y, TP Hà Nội
☑ Mã số thuế
   0101234567
☑ Số điện thoại
   024 3333 6666
☐ Email
   ketoan@biz.vn
☐ Tài khoản ngân hàng
   0011002233445 – Vietcombank CN Hà Nội
☑ Logo
   [LOGO] cỡ vừa
Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in    ← link ĐỎ
```

## A2. Đặc tả UI

| Thành phần | Component | Ghi chú | Luật |
|---|---|---|---|
| Ô tick khối | `CommonCheckbox` (`base/index.ts:255`) | nguyên văn `In khối Thông tin đầu trang trên mẫu này` | `R-TLMI-076` |
| Nhóm `Dòng in ra` | `PropSection` (`base/index.ts:226`) | slot phải = link `Theo thiết lập chung` | `R-TLMI-043` |
| 7 ô tick dòng | `CommonCheckbox` × 7 | mỗi ô **kèm giá trị thật** hiển thị mờ bên dưới | `R-TLMI-077` · `R-TLMI-081` |
| Link | `CommonButton` variant link | nguyên văn `Mở Cấu hình báo cáo chứng từ › Thông tin trên bản in` | `R-TLMI-051` |

## A3. Bảy dòng — **thứ tự CỐ ĐỊNH** (`R-TLMI-083`)

| # | Nhãn | Nguồn giá trị | Mặc định | Luật |
|---|---|---|---|---|
| 1 | `Tên đơn vị` | hồ sơ đơn vị của **chi nhánh ghi trên chứng từ** | theo chung | `R-TLMI-078` |
| 2 | `Địa chỉ` | như trên | theo chung | `R-TLMI-078` |
| 3 | `Mã số thuế` | như trên | theo chung | `R-TLMI-078` |
| 4 | `Số điện thoại` | như trên | theo chung | `R-TLMI-078` |
| 5 | `Email` | như trên | theo chung | `R-TLMI-078` |
| 6 | `Tài khoản ngân hàng` | như trên | theo chung | `R-TLMI-078` |
| 7 | `Logo` | ⚠ **CHƯA CÓ TRƯỜNG Ở BE** — Q5 | theo chung | `R-TLMI-082` · chốt **C03** |

⚠ **Logo là một trong bảy ô tick mà mẫu sửa riêng được** — chốt **C03** đóng mục này, ba nguồn đồng
thuận (`SCR:125`, `MT:77`, Figma frame 4). Nhưng `CompanyInfoResponse` **không có trường logo**
(§2.5 của `00-ke-hoach-tong.md`) ⇒ **Q5**.

## A4. Kế thừa — **bảy ô tick cũng theo cơ chế D5**

| Luật | Nội dung |
|---|---|
| `R-TLMI-036` | mỗi ô trong bảy ô tick có **hai trạng thái** theo chung / riêng |
| `R-TLMI-043` | nút `Theo thiết lập chung` của khối đưa **cả bảy** ô về theo chung |
| `R-TLMI-077` | bảy ô tick **mặc định theo thiết lập chung** |
| `R-TLMI-049` | **định dạng** khối đầu trang (căn lề khối, lặp trang sau) **LUÔN** theo chung — mẫu không sửa được |
| `R-TLMI-084` | thiết lập chung bật lặp đầu trang ⇒ khối **lặp lại ở trang sau** — chỉ đọc |

⚠ Ô tick `In khối Thông tin đầu trang trên mẫu này` (`R-TLMI-076`) là **RIÊNG của mẫu**, không kế thừa —
đây là cờ bật/tắt khối, trùng ý nghĩa với `👁` ở cột trái.

## A5. Hành vi

| Thao tác | Việc làm | Luật |
|---|---|---|
| Bỏ tick một dòng | dòng đó **không in** | `R-TLMI-077` |
| Bỏ tick **cả bảy** dòng | khối **không in gì** — **không** phải lỗi | `R-TLMI-080` |
| Dòng đã tick nhưng hồ sơ **để trống** | **bỏ qua dòng** đó khi in — không in dòng rỗng, không báo lỗi | `R-TLMI-079` |
| Bỏ tick ô `In khối…` | cả khối không in; tương đương tắt `👁` ở cột trái | `R-TLMI-076` · `R-TLMI-207` |
| Bấm `Theo thiết lập chung` | xoá bảy khoá tick; **một bước undo** | `R-TLMI-043` · `R-TLMI-041` |
| Vị trí logo khi căn lề ≠ Trái | logo **luôn bên trái khối**, cùng hàng với dòng đầu tiên; căn lề áp cho **cả cụm** | chốt **C29** |

## A6. Validation

**Không có dòng nào** trong bảng 17 dòng của `R-TLMI-239` thuộc khối này. Khối này **không bao giờ lỗi**.

---

# PHẦN B — *Tiêu đề bản in* (Figma frame 5)

## B1. Bố cục

```
Tiêu đề bản in
─────────────────────────────────────────────────────
Nội dung *
[ Chứng từ bán hàng                                  ]
Cỡ chữ (pt, 10–36)       Căn
[ 18 ]                   [ Giữa            ▾ ]
☑ IN HOA
☑ In đậm
☑ Dòng ngày tháng ngay dưới tiêu đề
In nghiêng "Ngày 27 tháng 08 năm 2026" — lấy theo ngày chứng từ.   ← ghi chú chữ mờ
```

## B2. Bảng trường

| Trường | Khoá i18n | Field API | Kiểu | Ràng buộc | Mặc định | Luật |
|---|---|---|---|---|---|---|
| `Nội dung` * | `tieuDe.noiDung` | `khoi.tieuDe.noiDung` | string | **không trống, tối đa 255 ký tự** | **tên loại chứng từ** | `R-TLMI-085` |
| `Cỡ chữ (pt, 10–36)` | `tieuDe.coChu` | `khoi.tieuDe.coChu` | int | 10-36 | **18** | `R-TLMI-086` |
| `Căn` | `tieuDe.can` | `khoi.tieuDe.can` | `'TRAI'\|'GIUA'\|'PHAI'` | select | `GIUA` | `R-TLMI-087` |
| `IN HOA` | `tieuDe.inHoa` | `khoi.tieuDe.inHoa` | bool | — | `true` | `R-TLMI-088` |
| `In đậm` | `tieuDe.inDam` | `khoi.tieuDe.inDam` | bool | — | `true` | `R-TLMI-089` |
| `Dòng ngày tháng ngay dưới tiêu đề` | `tieuDe.dongNgayThang` | `khoi.tieuDe.dongNgayThang` | bool | — | `true` | `R-TLMI-090` |

⚠ **`Nội dung` tối đa 255 ký tự**, KHÔNG phải 80. Bản code cũ đặt `độ dài tiêu đề ≤ 80` trong
`client/src/base/domainKit/mauIn/constants/gioiHan.ts` (A5 §4.2) ⇒ **phải sửa**.

## B3. Hành vi

| Thao tác | Việc làm | Luật |
|---|---|---|
| Đổi `Căn` | áp cho **cả dòng tiêu đề VÀ dòng ngày tháng** | `R-TLMI-087` |
| Bật `IN HOA` | in hoa dòng tiêu đề (dòng ngày tháng **không** bị in hoa) | `R-TLMI-088` |
| Bật `In đậm` | đậm dòng tiêu đề | `R-TLMI-089` |
| Bật `Dòng ngày tháng` | in **ngay dưới** tiêu đề, **in nghiêng**, lấy **ngày chứng từ** | `R-TLMI-090` |
| Xoá trống `Nội dung`, rời ô | báo `MSG_201` tại chỗ, badge → `Có lỗi` | `R-TLMI-085` · `R-TLMI-230` |
| Tắt `👁` khối Tiêu đề rồi để `Nội dung` trống | **bỏ qua validate** của khối này (chốt **C18**); bật lại ⇒ validate ngay | `R-TLMI-207` |

⚠ **Số chứng từ KHÔNG thuộc khối Tiêu đề** (`R-TLMI-091`) — muốn in số chứng từ thì đặt trường `Số`
vào một **khối tự do**. Xem **X2 / Q6**: Figma frame 0 lại in `Số: SO000123 · Ngày 27 tháng 08 năm 2026`
ngay dưới tiêu đề.

## B4. Validation

| # | Trường | Điều kiện | Message (nguyên văn) | Thời điểm | Tầng | Luật |
|---|---|---|---|---|---|---|
| V01 | `Nội dung` | không trống, ≤ 255 ký tự | `Tiêu đề bản in không được để trống, tối đa 255 ký tự` | rời ô, khi Lưu | Client/Server | `R-TLMI-085` |
| V02 | `Cỡ chữ` | số nguyên 10-36 | `Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36` | rời ô, khi Lưu | Client/Server | `R-TLMI-086` |

---

## 5. Phân bổ file

| Việc | File |
|---|---|
| Panel Thông tin đầu trang | `components/inspector/DauTrangInspector.tsx` |
| Panel Tiêu đề bản in | `components/inspector/TieuDeInspector.tsx` (giữ, sửa `80 → 255`) |
| Kế thừa 7 ô tick | `helpers/keThua.ts` |
| Render khối đầu trang + tiêu đề trên giấy | `components/BanInPaper.tsx` |
| Ràng V01/V02 | `helpers/kiemTraMau.ts` |
| Hằng `GIOI_HAN_TIEU_DE = { max: 255 }` · `GIOI_HAN_CO_CHU_TIEU_DE = { min: 10, max: 36, macDinh: 18 }` · `THU_TU_DONG_DAU_TRANG` (7) | `constants/constants.ts` |

---

## 6. Kiểm thử

### `test/DauTrangInspector.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-076 · ô tick In khối Thông tin đầu trang` | render → có ô tick với nguyên văn nhãn |
| `R-TLMI-077 · bảy ô tick, mặc định theo thiết lập chung` | mẫu rỗng → 7 ô tick, trạng thái lấy từ `chung` |
| `R-TLMI-081 · mỗi dòng hiển thị kèm giá trị thật` | `chung.hoSo.tenDonVi='CÔNG TY A'` → dòng `Tên đơn vị` có chữ mờ `CÔNG TY A` |
| `R-TLMI-082 · Logo là ô tick thứ bảy` | → đúng 7 ô, ô cuối nhãn `Logo` |
| `R-TLMI-083 · thứ tự bảy dòng cố định` | → thứ tự đúng: Tên đơn vị · Địa chỉ · Mã số thuế · Số điện thoại · Email · Tài khoản ngân hàng · Logo |
| `R-TLMI-079 · dòng đã tick nhưng hồ sơ trống thì bỏ qua` | `diaChi=''`, tick → `BanInPaper` **không** render dòng địa chỉ, **không** báo lỗi |
| `R-TLMI-080 · bỏ tick cả bảy thì khối không in gì` | bỏ tick 7 ô → khối rỗng trên giấy, badge **không** thành `Có lỗi` |
| `R-TLMI-043 · nút Theo thiết lập chung đưa cả bảy ô về chung` | sửa 3 ô rồi bấm → cả 7 khoá **vắng** khỏi `mau` |
| `R-TLMI-051 · link Thông tin trên bản in` | → có link với nguyên văn nhãn |
| `C29 · logo luôn bên trái, căn lề áp cả cụm` | `can='GIUA'` → cụm (logo + chữ) căn giữa, logo vẫn bên trái trong cụm |

### `test/TieuDeInspector.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-085 · nội dung mặc định là tên loại chứng từ` | mẫu chuẩn của `BH` → ô `Nội dung` = `Chứng từ bán hàng` |
| `R-TLMI-085 · trống thì báo MSG_201` | xoá trống, blur → `Tiêu đề bản in không được để trống, tối đa 255 ký tự` |
| `R-TLMI-085 · 255 ký tự hợp lệ, 256 không` | 255 → không lỗi; 256 → `MSG_201` |
| `R-TLMI-086 · cỡ chữ mặc định 18` | mẫu chuẩn → ô hiện `18` |
| `R-TLMI-086 · biên 10 và 36 hợp lệ, 9 và 37 không` | → `MSG_202` cho 9 và 37 |
| `R-TLMI-087 · Căn áp cho cả dòng tiêu đề và dòng ngày` | `can='PHAI'` → cả hai dòng có `text-align: right` |
| `R-TLMI-088 · IN HOA chỉ áp dòng tiêu đề` | bật → tiêu đề `text-transform: uppercase`, dòng ngày **không** |
| `R-TLMI-089 · In đậm khối Tiêu đề` | bật → tiêu đề `font-weight: bold` |
| `R-TLMI-090 · dòng ngày in nghiêng ngay dưới tiêu đề, lấy ngày chứng từ` | dữ liệu `ngayChungTu='2026-08-27'` → render `Ngày 27 tháng 08 năm 2026`, `font-style: italic` |
| `R-TLMI-091 · số chứng từ KHÔNG thuộc khối Tiêu đề` | → `BanInPaper` khối Tiêu đề **không** chứa số chứng từ |
| `C18 · khối Tiêu đề đang ẩn thì bỏ qua validate` | tắt `👁`, `Nội dung` trống → badge **không** thành `Có lỗi`; bật lại → thành `Có lỗi` ngay |

---

## 7. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR8 | dòng `Ngày … tháng … năm …` lấy theo **ngày chứng từ** |
| BR13 | ô `Nội dung` bắt buộc, có dấu `*`; kiểm khi rời ô |
| BR30 | chốt **C18** — khối ẩn thì bỏ qua validate |
| BR50.7 (Phase 2) | hồ sơ đơn vị đọc theo **chi nhánh ghi trên chứng từ** (`R-TLMI-078`, Q-14 / L-7) |
