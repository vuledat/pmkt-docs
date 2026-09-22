# 07 · Lối vào (menu In · nút Sửa mẫu) và màn Xem trước bản in

| | |
|---|---|
| Mã màn | menu In trên form chứng từ · `SCR_XemTruocBanIn` |
| Nguồn SCR | `SCR:3-17` · `SCR:244-253` · `SCR:357-377` |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` · `PMKT-U-14549_21-02_InMauTuyChinh` |
| Figma | frame **0** `71956:289768` |
| File chính | `components/NutInChungTu.tsx` · `components/modal/XemTruocBanInModal.tsx` |
| Luật phủ | `R-TLMI-023…035` (nhóm B) · `R-TLMI-259…271` (nhóm P) |

---

# PHẦN A — Menu In trên form chứng từ

## A1. Thứ tự menu (`R-TLMI-023`)

```
┌──────────────────────────────┐
│ 01-TT Phiếu thu              │  ← các mẫu CỐ ĐỊNH của loại (nếu có)
│ 02-VT Phiếu xuất kho         │
├──────────────────────────────┤  ← ĐƯỜNG KẺ
│ Mẫu tùy chỉnh                │  ← nhãn CỐ ĐỊNH cho mọi nghiệp vụ
│ Thiết lập mẫu in…            │  ← nhãn CỐ ĐỊNH; ẨN HẲN khi thiếu quyền
└──────────────────────────────┘
```

`R-TLMI-024`: **hai mục dùng đúng tên `Mẫu tùy chỉnh` và `Thiết lập mẫu in…` cho MỌI nghiệp vụ** —
không đổi chữ theo nghiệp vụ.

## A2. Điều kiện hiện nút In

| Điều kiện | Kết quả | Luật |
|---|---|---|
| Form **thêm mới** | **KHÔNG có nút In**; menu In chỉ ở form **sửa** và form **xem chi tiết** | `R-TLMI-025` |
| Nghiệp vụ có In từ danh sách | menu In cũng xuất hiện trên **màn danh sách** | `R-TLMI-026` |
| Thiếu quyền `HTMauIn.Edit` hoặc `<ChucNang>.View.Detail` | mục `Thiết lập mẫu in…` **ẩn hẳn**, **KHÔNG** disable | `R-TLMI-032` |
| Thiếu quyền `HTMauIn.*` nhưng **có** quyền In | vẫn in được `Mẫu tùy chỉnh` | `R-TLMI-033` |
| Thiếu quyền **In** | `MSG_COMMON_003` (BR25.2) — chốt **C15**, lệch **L-4** | `R-TLMI-033` |
| Hai quy tắc cấm in của thiết lập chung | **cả menu In KHÔNG mở được**, kể cả `Mẫu tùy chỉnh` | `R-TLMI-261` |

### A2.1 Hai tooltip nút In bị disable — **nguyên văn, chưa có mã `MSG_`** (L-5, Q1)

| Điều kiện | Tooltip (nguyên văn, `S20:155-156`) | Khoá i18n |
|---|---|---|
| Đơn vị không cho phép in chứng từ **chưa ghi sổ**, và chứng từ chưa ghi sổ | `Đơn vị không cho phép in chứng từ chưa ghi sổ` | `mauIn:menuIn.tooltipChuaGhiSo` |
| Đơn vị không cho phép in chứng từ **đã khoá sổ**, và chứng từ đã khoá sổ | `Đơn vị không cho phép in chứng từ đã khóa sổ` | `mauIn:menuIn.tooltipDaKhoaSo` |

⚠ Quy tắc "đã khoá sổ" **chỉ tác động nút In của chứng từ** — **không** tác động báo cáo và **không**
tác động `Xuất Excel` (`S20:157`).
⚠ `msg.sh` sẽ báo `THIEU` cho hai chuỗi này cho tới khi BA cấp mã — **đã ghi nhận** (L-5).

## A3. Hai lối vào — **cùng một màn, cùng một mẫu** (`R-TLMI-028`)

```
Lối vào 1: Form chứng từ ─ menu In ─ "Thiết lập mẫu in…"  ──┐
                                                            ├─→ <ThietLapMauInModal>
Lối vào 2: Màn Xem trước bản in ─ nút "Sửa mẫu"           ──┘
```

| Luật | Nội dung |
|---|---|
| `R-TLMI-011` | mở màn từ một chứng từ ⇒ mở **đúng mẫu của nghiệp vụ chứng từ đó** |
| `R-TLMI-012` | đổi `Loại nghiệp vụ` trên form rồi mở lại ⇒ mở **một mẫu KHÁC** |
| `R-TLMI-028` | hai lối vào cho **cùng một màn và cùng một mẫu** |
| `R-TLMI-029` | đóng màn ⇒ quay lại **đúng nơi vừa mở ra** |
| `R-TLMI-030` | quay lại màn xem trước sau khi lưu ⇒ bản in **vẽ lại theo mẫu vừa lưu** |
| `R-TLMI-013` | mẫu in **cố định theo quy định** (01-TT, 02-VT…) **không sửa được**, vẫn in như cũ |

⇒ `NutInChungTu` giữ state `moThietLap: { nguon: 'MENU' | 'XEM_TRUOC' } | null`; đóng modal thì
`nguon === 'XEM_TRUOC'` ⇒ mở lại `XemTruocBanInModal` và **invalidate** query dữ liệu in.

## A4. Props của `NutInChungTu` — ranh giới engine ↔ nghiệp vụ

```ts
interface NutInChungTuProps {
  maLoaiChungTu: string          // vd 'BH'
  maNghiepVu: string             // Q-16: LUÔN gửi cặp, kể cả khi loại chỉ có một nghiệp vụ
  chungTuId: string
  tieuDeBanIn: string            // "<Tên loại> <Số chứng từ>"
  quyenXemChiTiet: string        // C13 — vd 'BanHang.View.Detail'
  cheDoForm: 'SUA' | 'XEM'       // R-TLMI-025: form THEM_MOI không render nút này
  onInMauCoDinh?: (ma: string) => Promise<void>
  size?: …; variant?: …; testId?: string
}
```

Engine **không** biết gì về bán hàng. Mọi thứ riêng nghiệp vụ đi vào qua props.

⚠ **Bỏ** prop `onMoThietLap` của bản cũ
(`client/src/base/domainKit/mauIn/components/NutInChungTu.tsx:632` phía host gọi `navigate(...)`) —
modal mở **tại chỗ** (D1).
⚠ **Bỏ** literal `const QUYEN_THIET_LAP = 'HTMauIn.Edit'` ở
`client/src/base/domainKit/mauIn/components/NutInChungTu.tsx:26` ⇒ vào `constants/permissions.ts` (Q-15).

---

# PHẦN B — Màn Xem trước bản in (Figma frame 0)

## B1. Bố cục

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ Xem trước bản in: {tên nghiệp vụ} {số chứng từ}   🖶 In │🗎 Xuất file│✎ Sửa mẫu│(?)│(✕)│
├────────────────────────────────────────────────────────────────────────────────────┤
│ ☰ {tên nghiệp vụ}         Trang 1 / 1    − 100% +                        🖶    🗎  │
├──────────┬─────────────────────────────────────────────────────────────────────────┤
│ ┌──────┐ │                    ┌─────────────────────────┐                          │
│ │thumb-│ │                    │                         │                          │
│ │nail  │ │                    │      TRANG GIẤY         │                          │
│ │      │ │                    │      (bản in thật)      │                          │
│ └──────┘ │                    │                         │                          │
│    1     │                    └─────────────────────────┘                          │
└──────────┴─────────────────────────────────────────────────────────────────────────┘
```

Trang hiện tại có **viền đỏ** ở thumbnail, số trang bên dưới.

## B2. Đặc tả UI

| Thành phần | Component | Nguyên văn nhãn | Luật |
|---|---|---|---|
| Vỏ modal | `CommonModalShell` (`base/index.ts:355`) | tiêu đề `Xem trước bản in: {tenNghiepVu} {soChungTu}` | `R-TLMI-268` |
| Nút `In` | `CommonButton` (`base/index.ts:124`) | `In` | `R-TLMI-268` |
| Nút `Xuất file` | `CommonButton` | `Xuất file` | — (ngoài phạm vi FE, gọi BE) |
| Nút **`Sửa mẫu`** | `CommonButton` | `Sửa mẫu` — **ẩn hẳn** khi thiếu quyền | `R-TLMI-027` · `R-TLMI-269` |
| Cột thumbnail | **mới** | trang hiện tại viền đỏ, số trang bên dưới | Figma frame 0 |
| `Trang 1 / 1` | text | interpolation `{hienTai}` `{tong}` | Figma frame 0 |
| `− 100% +` | **mới** | zoom — **không** ảnh hưởng bản in | `R-TLMI-221` (tương tự) |
| Trang giấy | `BanInPaper.tsx` với `tuongTac={false}` | **một renderer duy nhất** (D13) | `R-TLMI-262…265` |

## B3. Luồng in `Mẫu tùy chỉnh`

```
Menu In › "Mẫu tùy chỉnh"
 ├─ nút In bị disable (2 quy tắc cấm in)  → cả menu KHÔNG mở được + tooltip   (R-TLMI-261)
 ├─ thiếu quyền In                        → MSG_COMMON_003                     (C15, L-4)
 ├─ GET dữ liệu in + mẫu hiệu lực
 │   ├─ lỗi hệ thống  → MSG_003 và **KHÔNG** mở màn xem trước                  (R-TLMI-270)
 │   └─ OK
 │        ├─ CHƯA CÓ bản ghi mẫu → in theo MẪU CHUẨN + toast MSG_103 MỘT LẦN   (R-TLMI-260)
 │        └─ có bản ghi         → dựng theo mẫu của nghiệp vụ chứng từ đang mở (R-TLMI-259)
 └─ mở <XemTruocBanInModal>                                                    (R-TLMI-268)
```

⚠ **`MSG_103` hiện "một lần"** = **một lần mỗi lần mở màn xem trước bản in** (chốt **C22**).
Không nhớ qua phiên, không nhớ theo người dùng ⇒ state cục bộ của modal, **không** `localStorage`.

Nguyên văn `MSG_103`:
`Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in theo mẫu chuẩn hệ thống`

## B4. Dựng bản in — phần FE vẽ được

| Luật | Tầng | FE làm gì |
|---|---|---|
| `R-TLMI-262` dựng từ trên xuống theo Bố cục mẫu, **chỉ khối đang bật** | BE | `BanInPaper` render `khoi.filter(k => k.hien)` theo thứ tự mảng |
| `R-TLMI-263` hình nền vẽ **dưới cùng** | BE | lớp nền `z-index` thấp nhất |
| `R-TLMI-264` chữ, đường kẻ, giấy-chữ theo mẫu; **ô theo chung lấy giá trị lúc in** | BE | `giaTriHieuDung(mau, chung, khoa)` (D5) |
| `R-TLMI-265` bảng dài tràn trang; khối sau in **tiếp ngay dưới** dòng cuối | BE | CSS `break-inside: auto` cho bảng, khối sau là block kế tiếp |
| `R-TLMI-266` áp ba quy tắc in chứng từ của thiết lập chung | BE | **không** FE (chốt **C01** + **C30**) |
| `R-TLMI-267` đọc hồ sơ đơn vị theo **chi nhánh ghi trên chứng từ** | BE | FE nhận sẵn trong `duLieuIn.hoSoDonVi` (Q-14 / L-7) |
| `R-TLMI-271` in không thay đổi dữ liệu chứng từ hay mẫu | BE | FE **không** gọi mutation nào khi in |
| `R-TLMI-180` ô gộp chiếm đúng số dòng, số cột | BE | `rowSpan` / `colSpan` của `<td>` |
| `R-TLMI-181` giá trị dài **tự xuống dòng**, ô cùng hàng **cao bằng nhau** | BE | `word-break: break-word`; `<tr>` tự cân chiều cao |
| `R-TLMI-194/195/200` khối Chữ ký | BE | `flex-wrap` + `min-width: 4cm`; `break-inside: avoid` cho cả khối |

---

## C. Ma trận ẩn / hiện · disable

| Thành phần | Có quyền Thiết lập | Thiếu quyền Thiết lập | Nút In bị disable | Luật |
|---|---|---|---|---|
| Nút `In ▾` trên form **sửa/xem** | Show | Show | **Disable** + tooltip | `R-TLMI-025` · `R-TLMI-261` |
| Nút `In ▾` trên form **thêm mới** | **Hide** | **Hide** | — | `R-TLMI-025` |
| Mục `Mẫu tùy chỉnh` | Show | **Show** | menu không mở được | `R-TLMI-033` · `R-TLMI-261` |
| Mục `Thiết lập mẫu in…` | Show | **Hide** (ẩn hẳn) | menu không mở được | `R-TLMI-032` |
| Nút `Sửa mẫu` trên màn Xem trước | Show | **Hide** (ẩn hẳn) | — | `R-TLMI-027` · `R-TLMI-032` · `R-TLMI-269` |

---

## D. Validation

| # | Trường | Điều kiện | Message (nguyên văn) | Tầng | Luật |
|---|---|---|---|---|---|
| V17 | Quyền Thiết lập mẫu in | có quyền | `Bạn không có quyền thực hiện tác vụ này` | **Server** | `R-TLMI-034` |
| — | Quyền **In** | có quyền | `MSG_COMMON_003` (BR25.2) — chốt **C15** | Client/Server | `R-TLMI-033` |
| — | Lỗi hệ thống khi dựng bản in | — | `Lỗi hệ thống, vui lòng thử lại sau` + **KHÔNG** mở màn xem trước | Cả hai | `R-TLMI-270` |

---

## E. Gắn vào Chứng từ bán hàng (pilot — D3)

```
client/src/features/banHang/chungTuBanHang/
├── components/ChungTuBanHangThemMoiModal.tsx
│     import { NutInChungTu } from '@domain-kit/mauIn'
│     <NutInChungTu
│        maLoaiChungTu={MA_LOAI_CHUNG_TU_BAN_HANG}    // 'BH' — A5 §7.3
│        maNghiepVu={form.loaiNghiepVu}               // R-TLMI-002 · Q-16
│        chungTuId={id}
│        tieuDeBanIn={t('banHang:chungTuBanHang.tieuDeBanIn', { so })}
│        quyenXemChiTiet={BAN_HANG_CHUNG_TU_PERM.viewDetail}
│        cheDoForm={cheDo}                            // R-TLMI-025
│     />
└── constants/permissions.ts
      viewDetail: 'BanHang.View.Detail'               // C13
```

⚠ **Mã loại bán hàng là `BH`** (theo `mst_loai_chung_tu.code` sau `V1032`), **không** phải `BHH`/`CTBH`
(A5 §7.3).

Các nghiệp vụ còn lại (lô 6): `MuaDichVu` (đang có ở
`client/src/features/muaHang/chungTuMuaHang/components/modal/MuaDichVuModal.tsx:627`), phiếu thu `PT`,
phiếu chi `PC` — BE đã có provider nhưng FE **chưa nối** (A5 §7.5).

---

## F. Phân bổ file

| Việc | File |
|---|---|
| Split button `In ▾` + menu + gate quyền | `components/NutInChungTu.tsx` |
| Modal Xem trước bản in | `components/modal/XemTruocBanInModal.tsx` |
| Renderer giấy (dùng chung) | `components/BanInPaper.tsx` |
| Mở tab in + `window.print` | `helpers/inBanIn.tsx` (giữ nguyên) |
| Query dữ liệu in / menu in / mẫu hiệu lực | `api/queries.ts` |
| Mã quyền | `constants/permissions.ts` |
| 2 tooltip + 2 nhãn menu | `i18n/vi.ts` · `en.ts` nhánh `menuIn.*` |

---

## G. Kiểm thử — `test/NutInChungTu.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-023 · thứ tự menu: mẫu cố định → đường kẻ → Mẫu tùy chỉnh → Thiết lập mẫu in…` | menu 2 mẫu cố định → thứ tự đúng, có 1 divider |
| `R-TLMI-024 · hai mục dùng đúng tên cho mọi nghiệp vụ` | render với `BH` và `MDV` → cùng nhãn `Mẫu tùy chỉnh` / `Thiết lập mẫu in…` |
| `R-TLMI-025 · form thêm mới không có nút In` | `cheDoForm` không truyền / host không render → không có nút |
| `R-TLMI-026 · nghiệp vụ có In từ danh sách thì menu In ở màn danh sách` | render trong context danh sách → nút hiện |
| `R-TLMI-027 · màn xem trước có nút Sửa mẫu` | mở `XemTruocBanInModal` với quyền đủ → có nút `Sửa mẫu` |
| `R-TLMI-028 · hai lối vào mở CÙNG một modal và cùng mẫu` | vào từ menu và từ `Sửa mẫu` → cùng `queryKey` mẫu hiệu lực |
| `R-TLMI-029 · đóng màn quay lại đúng nơi vừa mở ra` | vào từ `Sửa mẫu`, đóng → `XemTruocBanInModal` mở lại; vào từ menu, đóng → về form |
| `R-TLMI-030 · quay lại xem trước sau khi lưu thì vẽ lại theo mẫu vừa lưu` | lưu rồi đóng → query dữ liệu in bị invalidate |
| `R-TLMI-032 · thiếu quyền thì mục menu và nút Sửa mẫu ẨN HẲN` | không có `HTMauIn.Edit` → mục `Thiết lập mẫu in…` **không có trong DOM** (không phải `disabled`) |
| `R-TLMI-033 · thiếu quyền Thiết lập nhưng có quyền In thì vẫn in Mẫu tùy chỉnh` | → mục `Mẫu tùy chỉnh` vẫn bấm được |
| `R-TLMI-031 · quyền xét theo nghiệp vụ tại chi nhánh đang làm việc` | đổi chi nhánh → gate quyền tính lại |
| `R-TLMI-260 · chưa có bản ghi mẫu thì in theo mẫu chuẩn và báo MỘT LẦN` | `nguon='CHUAN'` → toast `MSG_103` đúng **một** lần mỗi lần mở xem trước (C22) |
| `R-TLMI-260 · mở lại xem trước thì báo lại` | đóng rồi mở lại → toast hiện lại |
| `R-TLMI-261 · nút In disable thì cả menu KHÔNG mở được` | `camIn='CHUA_GHI_SO'` → click nút không mở dropdown |
| `R-TLMI-261 · tooltip chưa ghi sổ` | hover → `Đơn vị không cho phép in chứng từ chưa ghi sổ` |
| `R-TLMI-261 · tooltip đã khoá sổ` | hover → `Đơn vị không cho phép in chứng từ đã khóa sổ` |
| `R-TLMI-268 · mở màn xem trước như các mẫu cố định` | chọn `Mẫu tùy chỉnh` → `XemTruocBanInModal` mở với tiêu đề `Xem trước bản in: Chứng từ bán hàng SO000123` |
| `R-TLMI-269 · nút Sửa mẫu ẩn khi thiếu quyền` | → không có trong DOM |
| `R-TLMI-270 · lỗi hệ thống thì KHÔNG mở màn xem trước` | API 500 → toast `Lỗi hệ thống, vui lòng thử lại sau`, modal **không** mở |
| `R-TLMI-012 · đổi Loại nghiệp vụ rồi mở lại thì mở mẫu khác` | đổi `maNghiepVu` → `queryKey` đổi |
| `R-TLMI-013 · mẫu cố định không sửa được` | menu → mục mẫu cố định **không** có `⚙` |

## H. Kiểm thử — `test/BanInPaper.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-262 · dựng theo thứ tự Bố cục mẫu, chỉ khối đang bật` | 3 khối, khối 2 `hien=false` → render 2 khối đúng thứ tự |
| `R-TLMI-263 · hình nền vẽ dưới cùng` | → lớp nền `z-index` nhỏ nhất |
| `R-TLMI-264 · ô theo chung lấy giá trị lúc in` | `mau.trang.font` vắng, `chung.font='Arial'` → giấy dùng Arial |
| `R-TLMI-180 · ô gộp chiếm đúng số dòng/cột` | ô `rowSpan=2 colSpan=3` → `<td rowspan="2" colspan="3">` |
| `R-TLMI-181 · giá trị dài tự xuống dòng` | chuỗi 300 ký tự → ô có `word-break: break-word` |
| `R-TLMI-178 · dấu hiệu lưới căn chỉnh không in` | `tuongTac=false` → không render class lưới |
| `R-TLMI-143 · ô trống không in gì nhưng chiếm chỗ` | ô `TRONG` → `<td>` rỗng vẫn tồn tại |

---

## I. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR7 | định dạng số / tiền trên bản in |
| BR8 | dòng ngày tháng trên bản in |
| BR25 | BR25.2 **ẩn hẳn** khi thiếu quyền; `MSG_COMMON_003` cho thiếu quyền In (chốt **C15**) |
| BR26.1 | toast `MSG_103` góc phải trên |
| BR35 | `R-TLMI-029/030` — quay lại đúng nơi vừa mở ra, vẽ lại theo mẫu vừa lưu |
| BR51.5 · BR51.6 (Phase 2) | mẫu dùng chung đơn vị; ba quy tắc in chứng từ (**BE**) |
