# PMKT-E-14549_21 — Kế hoạch triển khai FE · Thiết lập mẫu in chứng từ

> 🟡 **BẢN NHÁP CHỜ REVIEW — CHƯA CODE GÌ.** Tài liệu này chỉ để BA + Dev FE + Design soát.

| | |
|---|---|
| Trạng thái | `NHÁP` — chờ review |
| Ngày lập | 2026-09-19 |
| Người review | 1 BA (chưa gán) · 1 Dev FE (chưa gán) · 1 Design (chưa gán) |
| Phiếu yêu cầu | `PMKT-E-14549_21_ThietLapMauInChungTu` (đọc qua bản sao tạm — **KHÔNG mở `pmkt-docs/ba/Phase_2/**`**) |
| Đặc tả nguồn | [`docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/`](../PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/) — 271 luật · 12 bất biến · 36 mục mâu thuẫn · **0 OPEN** |
| Biên bản chốt | [`04-quyet-dinh-ban-giao.md`](../PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/04-quyet-dinh-ban-giao.md) — Q-01…Q-16, L-1…L-8 |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` · `PMKT-U-14549_21-02_InMauTuyChinh` |
| Màn hình | **1 modal toàn màn** (Thiết lập mẫu in) + **1 modal xem trước bản in** + 6 hộp thoại con |
| Figma | file `ymMyg329ejsgCWg28CNmGl`, section `71956:288871` — **8 frame 1440×1024** |
| Module FE | `client/src/base/domainKit/mauIn/` (**TIER 2.5 — engine dùng chung**) |
| Domain gắn vào | `client/src/features/banHang/chungTuBanHang/` (pilot) — sau đó mọi nghiệp vụ có mẫu in |
| API phụ thuộc | `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-api/` — **CHƯA LẬP** (`/plan-be` chưa chạy) |
| Luật FE phải phủ | **237 / 271** (108 `FE` + 129 `CẢ HAI`); 34 luật thuần `BE` ngoài phạm vi file này |

---

## §0. Quyết định đã chốt `D1…D14`

### D1 · Màn là **MODAL TOÀN MÀN mở từ form chứng từ**, KHÔNG phải route riêng

**Quyết định.** Bỏ hẳn route `/he-thong/thiet-lap-mau-in` và `/he-thong/thiet-lap-mau-in/:ma`. Màn dựng
bằng `CommonModalShell` toàn màn, mount ngay trong cây của form chứng từ đang mở.

**Căn cứ.** `R-TLMI-011` (mở màn từ một chứng từ thì mở đúng mẫu của nghiệp vụ chứng từ đó) ·
`R-TLMI-028` (hai lối vào cho **cùng một màn**) · `R-TLMI-029` (đóng màn thì quay lại **đúng nơi vừa mở
ra**) · `R-TLMI-217` (trang xem trước vẽ bằng **dữ liệu thật của chứng từ đang mở**) · `R-TLMI-219`
(**không có chế độ dữ liệu mẫu**). Figma frame 1/1b/2/3/4/5/6 đều vẽ modal `1420×1007` trong viewport
`1440×1024`, header `Thiết lập mẫu in: {tên nghiệp vụ}`, nút `✕` góc phải.

**Vì sao KHÔNG chọn route.** Route độc lập không có chứng từ đang mở ⇒ phải bịa "nguồn xem thử", trái
`R-TLMI-219`; và `R-TLMI-029` không thực hiện được (history back không phân biệt được hai lối vào).

**Hệ quả lên code:**
- Xoá `client/src/features/heThong/thietLapMauIn/` (20 file, chưa commit) — xem §3.3-D.
- Revert `client/src/features/heThong/routes.tsx` (dòng 14-15, 61-80) về bản `origin/develop`.
- Revert `client/src/app/layouts/shell/menuRegistry.tsx:46-47, 502-507` (mục menu Hệ thống › Thiết lập mẫu in).
- Revert `client/src/app/i18n/vi.ts:256` và `client/src/app/i18n/en.ts:233`.
- Revert `client/src/app/layouts/AppLayout.tsx` (cờ `fullBleed` chỉ sinh ra để phục vụ route editor).
- Bỏ `duongDanThietLapMauIn()` ở `client/src/base/domainKit/mauIn/constants/gioiHan.ts:212`.

### D2 · Toàn bộ màn nằm ở **engine `@domain-kit/mauIn`**, không tạo feature module mới

**Quyết định.** Một module duy nhất `client/src/base/domainKit/mauIn/` theo **đúng khung module PMKT**
(`docs/rules/fe-khung-kien-truc-chuan.md:78` nói rõ khung này *"Áp cho cả `src/features/**` và
`src/base/domainKit/**`"*). Phần gắn vào từng nghiệp vụ chỉ còn **hai chỗ** trong module chứng từ đó.

**Vì sao không đặt ở `features/`.** Luật tầng (`client/eslint.boundaries.js`) cho import **chỉ đi
xuống**: `features → domain-kit → base/platform → core`. Màn này phải được mount từ **nhiều** module
`features/*` (bán hàng, mua hàng, phiếu thu, phiếu chi…). Đặt ở `features/heThong/` thì
`features/banHang/` phải import ngang sang `features/heThong/` — vi phạm ranh giới và `lint:boundaries`
sẽ chặn.

**Vì sao không tách hai module** (`mauIn` engine + `thietLapMauIn` màn): màn **là** engine — không có
dòng nghiệp vụ nào riêng của bán hàng hay mua hàng. Tách ra chỉ đẻ thêm một cửa ra và một namespace i18n
thứ hai (bản cũ đã làm thế: 154 khoá `mauIn` + 95 khoá `thietLapMauIn`, có khoá trùng ý).

**Trả lời trực tiếp câu hỏi "gốc chỉ có `index.ts`, `pages/` để đâu khi màn là modal":**
`pages/ThietLapMauInScreen.tsx` **vẫn tồn tại** và vẫn là nơi "chỉ ráp" — nó ráp header + 3 cột + chân
màn, **không có chrome của modal**. Vỏ modal (`CommonModalShell` + Provider) là
`components/modal/ThietLapMauInModal.tsx`. Tách như vậy để test `Screen` không cần portal.

### D3 · Pilot đổi sang **Chứng từ bán hàng**

Figma vẽ `Chứng từ bán hàng` (frame 0-6, tiêu đề `CHỨNG TỪ BÁN HÀNG`, số `SO000123`). Bản code cũ pilot
`Chứng từ mua dịch vụ` (`client/src/features/muaHang/chungTuMuaHang/components/modal/MuaDichVuModal.tsx:627`).
⇒ **Lô 5** gắn nút In vào `client/src/features/banHang/chungTuBanHang/components/ChungTuBanHangThemMoiModal.tsx`
trước; mua dịch vụ giữ lại nhưng chuyển sang API mới ở lô 6.

### D4 · State = **zustand vanilla + immer + zundo**, một store cho mỗi lần mở

`zustand ^5.0.15` · `immer ^11.1.18` · `zundo ^2.3.0` đều đã có (`client/package.json:39, 30, 38`).
Store dựng trong `hooks/`, cấp qua Provider, **không singleton**. `zundo` cấu hình `limit: 60` — trùng
đúng `R-TLMI-223` và chốt **C32**. Đóng modal ⇒ Provider unmount ⇒ lịch sử biến mất, thoả `R-TLMI-225`
mà không cần code dọn.

**Khác bản cũ (1):** bản cũ **không dùng immer** —
`client/src/base/domainKit/mauIn/store/mauInStore.ts:9-10` chỉ import `zustand` + `zundo`. Lưới ô kiểu
Excel có gộp/tách/chèn dòng cột — cập nhật lồng sâu, viết tay spread sẽ dài và dễ sót. ⇒ thêm `immer`.

**Khác bản cũ (2):** thư mục `store/` **bỏ**, đưa vào `hooks/` — `store/` không nằm trong 9 thư mục chuẩn
của khung module PMKT. Đây là dọn đúng phạm vi đang sửa, không phải refactor mở rộng.

**Cấu hình `zundo` cụ thể:**
```ts
temporal(creator, {
  limit: 60,                                   // R-TLMI-223 · chốt C32
  partialize: (s) => ({ mau: s.mau }),         // R-TLMI-223: chỉ theo dõi mẫu; chọn khối / zoom / lưới KHÔNG vào lịch sử
  equality: (a, b) => JSON.stringify(a) === JSON.stringify(b),
  handleSet: (set) => debounceTheoRoiO(set),   // R-TLMI-224: gõ chữ trong một ô = MỘT bước, chốt khi rời ô
})
```

### D5 · Ô "theo thiết lập chung" ⇒ **khoá VẮNG MẶT trong payload**

`R-TLMI-037` nói **tuyệt đối không copy giá trị đang hiển thị**; chốt **C28** dịch sang mô hình JSON:
*"khoá **vắng mặt** = theo chung"*.

**Hệ quả lên code — đây là chỗ dễ code sai nhất của cả phiếu:**
- Zod dùng `.optional()`, **KHÔNG** `.default(...)`. `.default()` sẽ âm thầm điền giá trị ⇒ ô hoá "riêng".
- Store giữ **hai lớp tách rời**: `mau.trang` (chỉ khoá **riêng**) và `chung` (giá trị thiết lập chung,
  **chỉ đọc**, không nằm trong `mau`). UI hiển thị `mau.trang.khoGiay ?? chung.khoGiay`.
  **Không bao giờ** ghi `chung` vào `mau`.
- `helpers/keThua.ts` cấp đúng ba hàm:
  `giaTriHieuDung(mau, chung, khoa)` · `laTheoChung(mau, khoa)` · `veTheoChung(mau, nhomKhoa[])`.
- Payload gửi BE: `helpers/chuanHoaMau.ts` **xoá mọi khoá `undefined`** trước `JSON.stringify`.
- Nút `Theo thiết lập chung` = `delete` cả nhóm khoá, **một bước undo** (`R-TLMI-040/041/043`).
- Đổi Khổ/Hướng trên thanh Xem trước = **ghi khoá** ⇒ ô hoá riêng (`R-TLMI-044`). Hai ô Khổ/Hướng ở thanh
  Xem trước và ở panel `Thiết lập mẫu` là **MỘT trường**, đồng bộ hai chiều tức thời (chốt **C17**).
- `R-TLMI-045`: **không** có nhãn riêng từng ô cho biết ô đang theo chung hay riêng — không tự thêm UI.

### D6 · **Tên hiển thị** và **In đậm** là thuộc tính **CỦA TRƯỜNG**; `Căn` là **theo Ô**

`R-TLMI-156` vs `R-TLMI-161` — hai luật đối lập nhau có chủ ý, `R-TLMI-156 §Ghi chú` nói thẳng
*"Đối lập trực tiếp với **Căn** vốn đặt theo ô"*.

**Hệ quả lên code:**
- Thêm một nhánh JSON **cấp mẫu**: `truongDungChung: Record<string, { nhan?: string; dam?: boolean }>`
  — **không** để trong khối. Sửa ở khối tự do A ⇒ ô dùng cùng trường ở khối B đổi theo ngay.
- `Căn` và `Nghiêng` nằm trên **từng ô** (`OTuDo.can`, `OTuDo.nghieng`) — `R-TLMI-160/161`.
- Nút `B` / `I` / `Trái·Giữa·Phải` trên thanh công cụ áp **theo vùng chọn** (`R-TLMI-163`): `B` ghi vào
  `truongDungChung[k].dam` cho mọi ô-trường trong vùng; `I` và `Căn` ghi vào từng `OTuDo`.
- `R-TLMI-164`: trường **chưa đặt vào ô nào** thì `truongDungChung[k]` **KHÔNG lưu** ⇒
  `chuanHoaMau()` phải quét mọi khối tự do, thu tập `k` đang dùng, rồi lọc `truongDungChung`.
- Đậm ô-trường ⇒ **chỉ đậm `Tên hiển thị`**, giá trị luôn in thường (`R-TLMI-158`). Ô `Chữ tự do` + đậm
  ⇒ đậm **cả chữ** (`R-TLMI-159`). Hai nhánh render khác nhau trong `BanInPaper.tsx`.
- `R-TLMI-145`: `Tên hiển thị` bị xoá trống ⇒ **chỉ in giá trị** (không in `: `). Figma frame 3 hiển thị
  placeholder nguyên văn `Trống = chỉ in giá…` ở ô Tên hiển thị của trường `Số tiền bằng chữ`.

### D7 · Khối tự do = **lưới ô thưa theo ô neo (anchor)**, tối đa 20 × 6

```ts
type NoiDungO =
  | { loai: 'TRONG' }
  | { loai: 'TRUONG'; k: string }
  | { loai: 'CHU_TU_DO'; chu: string }

interface OTuDo {
  id: string                        // ổn định qua gộp/tách để React key và undo không nhảy
  dong: number; cot: number         // 0-based, góc TRÊN-TRÁI của ô
  rowSpan: number; colSpan: number  // >= 1
  noiDung: NoiDungO
  can: 'TRAI' | 'GIUA' | 'PHAI'
  nghieng: boolean
}

interface KhoiTuDo {
  id: string; loai: 'TU_DO'; ten: string; hien: boolean
  soDong: number                    // 1…20   R-TLMI-129 · sàn 1 theo chốt C20
  soCot: number                     // 1…6    R-TLMI-130 · sàn 1 theo chốt C20
  o: OTuDo[]                        // CHỈ ô neo; ô bị phủ KHÔNG có bản ghi
}
```

**Vì sao ô neo chứ không ma trận đặc.** Gộp/tách chỉ là sửa `rowSpan/colSpan` + thêm/xoá vài bản ghi;
JSON không phình theo `soDong × soCot`; `R-TLMI-143` (ô trống **không in gì nhưng chiếm chỗ**) tự đúng vì
ô trống vẫn là một bản ghi neo. Ma trận đặc buộc phải giữ cờ "bị phủ" trên mọi ô — thừa và dễ lệch.

**Bảng phủ dẫn xuất.** `helpers/luoiTuDo.ts` dựng `bangPhu: (string | null)[][]` (`[dong][cot] → oId`)
bằng `useMemo`. Mọi thuật toán vùng chọn / gộp / tách / chèn / xoá chạy trên bảng phủ rồi ghi ngược ra `o[]`.

**Khối tự do mới** (`R-TLMI-123`): lưới **1 dòng × 2 cột** toàn ô trống, đặt **ngay trước khối Chữ ký**
(`R-TLMI-122`), mở bảng chỉnh và **chọn sẵn ô đầu tiên** (`R-TLMI-124`).

### D8 · Kéo thả: **chỉ `@dnd-kit/core`**, KHÔNG thêm package

`client/package.json:18` có `@dnd-kit/core ^6.3.1`; **không có** `@dnd-kit/sortable`. Máy không chạy được
`npm install` ⇒ **cấm sửa `package.json`**. Bản cũ đã tự dựng sortable ở
`client/src/base/domainKit/mauIn/components/SortableList.tsx:1-45` (kéo bằng tay cầm grip, có
`KeyboardSensor`: focus tay cầm → Space nhấc → ↑↓ dời → Space thả) — **giữ nguyên, dùng lại**.

Bốn loại kéo thả của màn này, tất cả trong **một** `DndContext` ở `pages/ThietLapMauInScreen.tsx`:

| # | Kéo gì | Cơ chế | Luật |
|---|---|---|---|
| K1 | Đổi thứ tự khối (cột trái) · cột bảng · ô ký | `SortableList.tsx` (đã có) | `R-TLMI-204` · `R-TLMI-115` · `R-TLMI-183` |
| K2 | Kéo **dòng trường** ở bảng chỉnh thả vào **ô lưới** trên trang xem trước | `useDraggable` ở dòng trường + `useDroppable` ở mỗi ô neo | `R-TLMI-149` |
| K3 | Kéo **ô có nội dung** thả lên **ô khác** ⇒ hai ô **đổi** nội dung | ô neo vừa `useDraggable` vừa `useDroppable` | `R-TLMI-154` |
| K4 | Kéo **khối** trên trang xem trước để đổi thứ tự | `useDraggable` ở bọc khối + `useDroppable` ở khe giữa khối | `R-TLMI-205` · `R-TLMI-206` |

Phân biệt bằng `data.current.loai: 'khoi' | 'cot' | 'oKy' | 'truong' | 'oLuoi'` — **bắt buộc**, xem R1.

`R-TLMI-117`: **đang lọc ở ô `Tìm cột` thì KHÔNG cho kéo thả cột** ⇒ `SortableList` nhận `disabled`.

### D9 · Tổng độ rộng cột `≠ 100` **không phải lỗi**; thuật toán chia đều cố định

`R-TLMI-110` chỉ hiện dòng tổng dưới lưới cột; `R-TLMI-111` tự chia lại **khi Lưu**. Bảng kiểm
`R-TLMI-239` **không có dòng nào** cho tổng độ rộng ⇒ **không** vào trạng thái `Có lỗi`.

`helpers/doRongCot.ts` · `chiaDeuVe100(cot: CotBang[]): CotBang[]` — bốn bước **đúng thứ tự**
(`R-TLMI-114`):
1. chỉ xét cột **đang tick in**; cột bỏ tick **giữ nguyên số cũ** (`R-TLMI-112`);
2. `mới = floor(cũ ÷ tổngCũ × 100)` — **làm tròn XUỐNG**;
3. phần còn thiếu để đủ 100 cộng vào **cột đang in CUỐI CÙNG**;
4. cột `< 3` nâng lên `3`, trừ phần nâng vào **cột rộng nhất**.

⚠ `ELSE` của luật viết hoa: **"GIỮ NGUYÊN TỶ LỆ giữa các cột — KHÔNG chia bằng nhau."** Tên nút
`Chia đều về 100%` gây hiểu nhầm; đọc kỹ ba ca chốt của BA thì rõ.

Ba ca chốt phải thành test: `40/40/40 → 33/33/34` · `50/30 → 62/38` · `10/10/10/10 → 25/25/25/25`.
Ca chạm sàn của `S-TLMI-024`: `90/70/2 → 54/43/3`.
Chốt **C31**: nút áp cho **mọi cột đang tick in**, không phụ thuộc ô `Tìm cột`.

Ba dịp gọi: bấm nút · tự chạy khi **Lưu** (`R-TLMI-111`) · khi có **cột mới** ở phiên bản sau (`R-TLMI-093`).

### D10 · Trạng thái & Lưu

| Trạng thái | Điều kiện | Nút Lưu | Luật |
|---|---|---|---|
| `Đã lưu` (badge **xám**) | mẫu **bằng** bản đã lưu (hoặc bằng mẫu chuẩn khi chưa có bản ghi) | **Disable** | `R-TLMI-240` |
| `Chưa lưu` (badge **cam**) | có thay đổi **và** mọi ô hợp lệ | bấm được, ghi | `R-TLMI-241` |
| `Có lỗi` (badge **đỏ**) | còn ≥ 1 ô không hợp lệ | **bấm được**, nhưng **KHÔNG ghi** | `R-TLMI-242` · `R-TLMI-243` |

⚠ **Nút Lưu chỉ mờ khi `Đã lưu`. KHÔNG mờ khi `Có lỗi`** — `R-TLMI-243 §Ghi chú` trích `MT:106`.
Đây là bẫy dễ code sai: bản năng sẽ là "có lỗi thì khoá nút Lưu".

Bấm Lưu khi `Có lỗi` ⇒ **không ghi** · báo **lỗi ĐẦU TIÊN** · mở bảng chỉnh của khối đó · đưa **con trỏ
vào ô lỗi** (`R-TLMI-244`); lỗi ở **ô lưới khối tự do** ⇒ **chọn ô đó trên trang xem trước**.
Thứ tự "đầu tiên" theo chốt **C21**: thứ tự **khối trong Bố cục mẫu** → trong một khối: **ô ở bảng chỉnh
trước** (trên xuống) → **rồi ô lưới trên trang xem trước** (trái→phải, trên→dưới).

Badge trạng thái nằm **cạnh tiêu đề màn**; nút Lưu ở **chân màn** (`R-TLMI-245`, Figma header 52 px).

### D11 · `MSG_401` có **BA** nút — cố ý lệch BR3

`MSG_PMKT-E-14549_21_401` = *"Mẫu đã có thay đổi chưa lưu. Bạn muốn làm gì?"* với **3 nút**:
`Lưu và đóng` · `Không lưu` · `Ở lại` (`R-TLMI-251…254`). BR3 chung chỉ quy định 2 nút.
⇒ **không dùng** `CommonConfirmModal` (`client/src/base/index.ts:375`, 2 nút) cho hộp này; dựng
`components/modal/HopThayDoiChuaLuuModal.tsx` trên `CommonModalShell` + `CommonModalFooter`.
Ghi rõ đang lệch **BR3** — xem §14 và Q12.

`Lưu và đóng` **vẫn hiện toast `MSG_101`** rồi mới đóng (chốt **C23**).
`R-TLMI-256`: đang mở **hộp thoại con** thì `Esc` **không tác dụng** với màn chính.

### D12 · Ô trống trong khối tự do **không bao giờ là lỗi**

`R-TLMI-236` · `R-TLMI-237` (xét lỗi chỉ xét ô **có nội dung**) · `R-TLMI-176` (khối tự do đang bật mà
**mọi ô đều trống** thì **vẫn lưu được**) · `R-TLMI-148` (chọn `Chữ tự do` mà rời ô khi chưa gõ ⇒ ô **tự
về Ô trống**, không báo lỗi).

⇒ `helpers/kiemTraMau.ts` khi duyệt khối tự do phải `if (o.noiDung.loai === 'TRONG') continue` **trước
mọi phép kiểm khác**. Bản cũ có luật "khối rỗng là lỗi"
(`client/src/base/domainKit/mauIn/helpers/kiemTraMau.ts`, 401 dòng) — **phải gỡ**.

Tương tự, chốt **C18**: **khối đang ẩn thì bỏ qua validate của khối đó**; bật lại thì validate ngay.

### D13 · Renderer **một bản duy nhất** cho cả trang xem trước lẫn bản in

Giữ nguyên ý bản cũ (`client/src/base/domainKit/mauIn/components/MauInPaper.tsx`, 578 dòng): **một**
component vẽ giấy, dùng cho canvas (có tương tác) và cho bản in, khác nhau bằng prop `tuongTac?: boolean`.

`R-TLMI-178` (dấu hiệu lưới căn chỉnh **không in và không xuất PDF**) thực hiện bằng
`@media print { .mauIn-luoiCanChinh { display: none } }` chứ **không** bằng nhánh JS — tránh lệch hai
đường vẽ. `R-TLMI-218`: bất kỳ thay đổi nào thì trang xem trước **vẽ lại ngay** ⇒ render thẳng từ store,
không cache.

### D14 · Tách `helpers/` thuần khỏi React để test chạy `environment: node`

Mọi thuật toán nặng (lưới ô, chia độ rộng, kế thừa, kiểm tra, chuẩn hoá, mẫu chuẩn) là **hàm thuần** trong
`helpers/` — không React, không mạng, không `t()`. Test `*.test.ts` với `// @vitest-environment node`.
Chỉ `components/` và `pages/` cần DOM (`*.test.tsx`). Test **không** import barrel `@base`.

Mọi `it()` mang **chính mã luật** để `trace.sh` đếm được.

---

## §1. Phạm vi

### Trong phạm vi

| # | Chức năng | UC | Nhóm luật |
|---|---|---|---|
| F1 | Modal toàn màn **Thiết lập mẫu in** — 3 cột (Bố cục mẫu · Xem trước · Bảng chỉnh) | UC01 | L, N (`201…216`, `240…257`) |
| F2 | Bảng chỉnh **Thiết lập mẫu** — Giấy và chữ (kế thừa) + Riêng của mẫu | UC01 | C, D, E (`036…075`) |
| F3 | Bảng chỉnh **Thông tin đầu trang** — 7 ô tick kế thừa | UC01 | F (`076…084`) |
| F4 | Bảng chỉnh **Tiêu đề bản in** | UC01 | G (`085…091`) |
| F5 | Bảng chỉnh **Bảng** — cột in ra, kẻ ô, chia đều 100% | UC01 | H (`092…119`) |
| F6 | **Khối tự do** — lưới ô kiểu Excel 20×6, gộp/tách, thanh công cụ, menu chuột phải | UC01 | I (`120…181`) |
| F7 | Bảng chỉnh **Chữ ký** — 5 chức danh + ô ký tự do | UC01 | K (`182…200`) |
| F8 | Thanh **Xem trước** — undo/redo 60 bước, zoom, Vừa khung, Hiện lưới căn chỉnh | UC01 | M (`217…229`) |
| F9 | **Kiểm tra & trạng thái** — 17 dòng validate, badge, Lưu, Đóng, Đặt lại | UC01 | A, N (`015…020`, `230…257`) |
| F10 | **Lối vào** — menu In trên form chứng từ, nút Sửa mẫu trên màn xem trước | UC01/UC02 | B (`023…035`) |
| F11 | **Modal Xem trước bản in** — thumbnail trang, zoom, In, Xuất file, Sửa mẫu | UC02 | P (`259…271`) |
| F12 | Gắn F10 vào **Chứng từ bán hàng** (pilot) | — | `R-TLMI-014` |

### NGOÀI phạm vi (nêu đích danh)

| Bị loại | Vì sao |
|---|---|
| Epic `PMKT-E-14549_20_CauHinhBaoCaoChungTu` — màn *Danh sách báo cáo*, *Tùy chỉnh báo cáo*, báo cáo yêu thích, mở rộng/thu gọn nhóm báo cáo | Q-03: chỉ làm **phần `_21` cần**, không làm cả epic `_20` |
| Màn **Thiết lập người ký** | Đã tồn tại ở `client/src/features/heThong/thongTinCongTy/components/NguoiKyTable.tsx` — F7 chỉ **đọc** và cấp **link mở** (`R-TLMI-052`) |
| 34 luật thuần `BE`: `R-TLMI-001, 004, 005, 006, 021, 022, 034, 035, 037, 038, 039, 047, 048, 049, 058, 059, 060, 064, 065, 075, 078, 083, 084, 119, 199, 246, 247, 248, 249, 258, 259, 262…267, 271` (danh sách chuẩn ở `09-truy-vet-va-kiem-thu.md`) | thuộc `/plan-be` |
| Màn **danh sách 47 loại chứng từ** của bản code cũ | D1 — không có trong tài liệu BA lẫn Figma |
| Popup **Lịch sử phiên bản mẫu** của bản code cũ (`HopLichSuMauIn.tsx`, 240 dòng) | không có luật `R-TLMI-*` nào; sinh từ mock HTML |
| **Kéo mép cột trên giấy** (`ThanhKeoCot` · `RaiCot` · `NutDongCot`, 151 dòng) | `R-TLMI-108` nhập độ rộng bằng **ô số ở bảng chỉnh**; Figma frame 2 chỉ có ô `Rộng %` |
| Kênh **super-admin** (`client-admin/src/features/quanTri/mauInMacDinh/`) | không có trong PYC `_21` |
| Hệ **biểu mẫu động** `client/src/features/bieuMau/` | chốt **C38**: hai chức năng độc lập, chỉ dùng lại kỹ thuật |
| **Xuất PDF phía FE** | `R-TLMI-178` chỉ nói dấu hiệu lưới không xuất PDF; nút `Xuất file` (Figma frame 0) là việc của BE |

---

## §2. Hiện trạng đã khảo sát

Mọi dòng dưới đây là **lệnh đã chạy thật** ngày 2026-09-19 trên `C:\Users\DatVL\Desktop\code\vtt-osp`.

### 2.1 Bốn câu hỏi bắt buộc (`fe-khung-kien-truc-chuan.md §4`)

| # | Câu hỏi | Trả lời | Bằng chứng |
|---|---|---|---|
| 0 | Code ở đâu? | `client/src/base/domainKit/mauIn/` — **không** `features/` (D2) | `docs/rules/fe-khung-kien-truc-chuan.md:78` |
| 1 | Màn loại nào? | **Không** thuộc 3 loại (danh mục / chứng từ / báo cáo). Là **trình soạn mẫu in** — engine riêng | `client/src/base/domainKit/index.ts:6-19` liệt kê 14 engine, `mauIn` nằm trong đó |
| 2 | Đã có engine chưa? | **CÓ, nhưng sai kiến trúc** — 48 file dựng từ mock HTML, chưa commit | `git status --porcelain` → `?? src/base/domainKit/mauIn/` |
| 3 | Component đã có ở `@base` chưa? | phần lớn có — bảng đầy đủ ở §3.1 | `grep -n … client/src/base/index.ts` (763 dòng) |
| 4 | Domain đang chạy không? | `banHang` chạy; form chứng từ bán hàng là **modal** | `client/src/features/banHang/routes.tsx:57-60`; `client/src/features/banHang/chungTuBanHang/components/ChungTuBanHangThemMoiModal.tsx` |

### 2.2 Trạng thái repo `client`

```
$ cd client && git branch --show-current
feat/mau-in
$ git log --oneline -1
aba54c41a fix(auth): gộp đợt UAT Auth — STT 1,2,3,4,5,6,8,9 + CN-5 Đổi mật khẩu (#204)
$ git status --porcelain      # 11 M + 7 ?? = 18 mục
```

| Mục | Trạng thái |
|---|---|
| `src/app/i18n/en.ts` · `src/app/i18n/vi.ts` · `src/app/layouts/AppLayout.tsx` · `src/app/layouts/shell/menuRegistry.tsx` | ` M` |
| `src/base/domainKit/index.ts` · `src/base/icons/index.ts` · `src/base/index.ts` | ` M` |
| `src/features/heThong/routes.tsx` | ` M` |
| `src/features/muaHang/chungTuMuaHang/components/modal/MuaDichVuModal.tsx` · `constants/constants.ts` · `constants/permissions.ts` | ` M` |
| `src/base/components/fields/CommonColorPicker.tsx` · `CommonSegmented.tsx` | `??` |
| `src/base/components/layout/PropField.tsx` · `PropSection.tsx` · `propField.css` | `??` |
| `src/base/domainKit/mauIn/` (48 file) | `??` |
| `src/features/heThong/thietLapMauIn/` (20 file) | `??` |

⚠ **Cổng cây commit đang đỏ**: `src/base/index.ts` và `src/base/domainKit/index.ts` đã sửa để trỏ tới
file còn `??`. Phải `git add` file mới **trước** khi commit barrel (`CLAUDE.md §Cổng cây commit`).

### 2.3 Thư viện có sẵn — **KHÔNG được thêm gói mới**

```
$ grep -nE '"(zustand|immer|zundo|@dnd-kit/core|@dnd-kit/sortable|antd|zod)"' client/package.json
18:    "@dnd-kit/core": "^6.3.1",
21:    "@tanstack/react-query": "^5.100.14",
22:    "antd": "^6.4.3",
30:    "immer": "^11.1.18",
37:    "zod": "^4.4.3",
38:    "zundo": "^2.3.0",
39:    "zustand": "^5.0.15"
```
`@dnd-kit/sortable` **không có**. Máy dev không chạy được `npm install` ⇒ **cấm sửa `package.json`**.

### 2.4 API BE — **CHƯA CÓ ENDPOINT NÀO ĐÚNG HỢP ĐỒNG MỚI**

| Endpoint bản cũ | Có thật ở đâu | Đúng hợp đồng mới? |
|---|---|---|
| A1…A9 dưới `/api/mau-in` | FE `client/src/base/domainKit/mauIn/api/mauInApi.ts:28` khai `MAU_IN_ENDPOINT='/api/mau-in'`; BE `cell-app/src/main/java/vn/vtt/pmkt/cell/mau_in/internal/controller/MauInController.java` | ❌ khoá là `maLoaiChungTu` **đơn**, thiếu `maNghiepVu` (Q-16); thiếu nhánh `chung` (thiết lập chung); thiếu kho trường của form |

⇒ **Nợ**: `api/mock.ts` tạm cho tới khi `/plan-be` + `/gen-be` xong. **Còn `mock.ts` = còn nợ.**
Hợp đồng dự kiến ở [`08-hop-dong-api-va-i18n.md`](08-hop-dong-api-va-i18n.md) §1.

### 2.5 "Thiết lập chung" — có gì, chưa có gì

| Hạng mục | Trạng thái | Bằng chứng |
|---|---|---|
| Thông tin công ty (tên, MST, ĐT, email, địa chỉ, TK ngân hàng) | ✅ **ĐÃ CÓ** | `cell-app/.../platform_iam/tenant/internal/controller/TenantConfigController.java:89` `GET /api/iam/me/tenant-config/company-info`; FE `client/src/features/heThong/thongTinCongTy/` |
| **Logo đơn vị** | ❌ **CHƯA CÓ** | `CompanyInfoResponse` không có trường logo → **R4 / Q5** |
| Thiết lập người ký (5 chức danh + cờ `inTenNguoiKyTrenChungTu`) | ✅ **ĐÃ CÓ** — nằm **trong** màn Thông tin công ty | `client/src/features/heThong/thongTinCongTy/components/NguoiKyTable.tsx` |
| Giấy và chữ chung (khổ · hướng · lề · font · cỡ chữ) cấp đơn vị | ❌ **CHƯA CÓ** | chỉ tồn tại **bên trong từng mẫu in** → **R3 / Q3** |
| Cấu hình báo cáo chứng từ (epic `_20`) | ❌ **CHƯA CÓ** | `grep -i "cauHinhBaoCao\|baoCaoChungTu"` ⇒ 0 kết quả → **Q4** |
| `cfg_chi_nhanh` | ❌ **KHÔNG TỒN TẠI** | Q-14 / L-7: tạm đọc hồ sơ đơn vị từ tenant, để sẵn cổng `HoSoDonViPort.theoChiNhanh()` |

---

## §3. Kế hoạch reuse

### 3.1 Dùng lại từ `@base` / `@core` / `@platform`

| Cần | Có sẵn ở đâu (`file:dòng`) | Dùng lại hay viết mới | Lý do |
|---|---|---|---|
| Vỏ modal toàn màn | `client/src/base/index.ts:355` `CommonModalShell` (+ `CommonModalSize` `:361`, `CommonModalPlacement` `:362`) | **Dùng lại** | có sẵn hệ kích thước; thiếu cỡ `fullscreen` thì **thêm prop vào `@base`**, không copy ra module |
| Header modal có badge | `client/src/base/index.ts:377` `CommonModalHeader` | **Dùng lại** | slot tiêu đề nhận ReactNode ⇒ nhét badge trạng thái cạnh tiêu đề (`R-TLMI-245`) |
| Chân modal | `client/src/base/index.ts:367` `CommonModalFooter` | **Dùng lại** | `Đóng` trái · `Đặt lại mẫu chuẩn` + `Lưu` phải (`R-TLMI-257`) |
| Hộp xác nhận 2 nút | `client/src/base/index.ts:375` `CommonConfirmModal` | **Dùng lại** cho `MSG_402/403/404` | 3 nút của `MSG_401` **không** dùng được (D11) |
| Nhóm thuộc tính cột phải | `client/src/base/index.ts:226` `PropSection` · `:228` `PropField` (chưa commit) | **Dùng lại** | đúng bố cục nhãn-trên/ô-dưới của Figma cột phải; `PropSection` có slot phải cho link `Theo thiết lập chung` |
| Cụm căn Trái/Giữa/Phải | `client/src/base/index.ts:267` `CommonSegmented` (chưa commit) | **Dùng lại** | đúng cụm `Căn` Figma frame 2 và thanh công cụ frame 3 |
| Bảng màu + hex | `client/src/base/index.ts:269` `CommonColorPicker` (chưa commit) | **Dùng lại, SỬA** | Figma frame 1 đếm được **10 ô màu** + ô `#000000`; phải khớp `R-TLMI-066` và ràng `MSG_210` |
| Ô số min/max | `client/src/base/index.ts:235` `CommonNumberInput` | **Dùng lại** | cỡ chữ, độ rộng %, lề, độ đậm, số cột tự động in ngang |
| Ô chữ | `client/src/base/index.ts:251` `CommonTextBox as CommonInput` | **Dùng lại** | |
| Ô chọn | `client/src/base/index.ts:691` `CommonSelectBox` / `CommonSelect` | **Dùng lại** | Khổ giấy · Hướng giấy · Font · Cỡ chữ cơ sở · Chỗ trống ký · Hình nền |
| Checkbox / Radio | `client/src/base/index.ts:255` · `:257` | **Dùng lại** | 7 ô tick đầu trang · `Kẻ ô` · `Căn ảnh` |
| Nút | `client/src/base/index.ts:124` `CommonButton` | **Dùng lại** | |
| Split button `In ▾` | `client/src/base/index.ts:151` `CommonDropdownButtonTwofold` | **Dùng lại** | đã dùng ở `client/src/base/domainKit/mauIn/components/NutInChungTu.tsx:16` |
| Dropdown (bọc thành menu chuột phải) | `client/src/base/index.ts:149` `CommonDropdownBasic` | **Dùng lại, BỌC** | không nhận `contextmenu` sẵn ⇒ bọc chứ **không** viết dropdown mới |
| Toast | `client/src/base/index.ts:116` `useToast` | **Dùng lại** | `MSG_101/102/104` (BR26.1, góc phải trên) |
| Trạng thái rỗng | `client/src/base/index.ts:732` `CommonEmpty` | **Dùng lại** | kho trường / lưới cột lọc không ra kết quả |
| Lọc không phân biệt dấu | `client/src/utils/text/quickSearch.ts:8` `foldAccent` · `:20` `matchesQuickSearch` | **Dùng lại** | `R-TLMI-116` · `R-TLMI-151` · `R-TLMI-168` |
| Quyền | `client/src/platform/index.ts:54` `useHasPermission` · `:55` `Can` | **Dùng lại** | `R-TLMI-031/032` — **ẩn hẳn**, không disable |
| i18n | `client/src/platform/index.ts:115` `useT` · `:102` `addTranslations` | **Dùng lại** | |
| Query | `client/src/platform/index.ts:91` `createResourceKeys` · `:93` `invalidateResource` | **Dùng lại** | |
| Icon | `client/src/base/icons/index.ts` (đã bổ sung 18 icon: `EyeSlashIcon`, `ArrowUUpRightIcon`, `ArrowCounterClockwiseIcon`, `TextAlignLeftIcon`…) | **Dùng lại** | trúng đúng nhóm icon Figma frame 1-6 dùng |
| Sortable tự dựng | `client/src/base/domainKit/mauIn/components/SortableList.tsx:1-45` | **Dùng lại NGUYÊN** | D8 — không có `@dnd-kit/sortable`, không cài thêm được |

### 3.2 Phải viết mới (mỗi dòng kèm "đã kiểm, không có sẵn vì…")

| Viết mới | Đặt ở | Đã kiểm `@base` / `@domain-kit` — không có vì |
|---|---|---|
| `LuoiTuDo.tsx` + `OLuoi.tsx` — lưới ô kiểu Excel, gộp/tách, vùng chọn Shift, phím tắt | `@domain-kit/mauIn/components/` | `grep -n "CommonTable\|Grid" client/src/base/index.ts` chỉ ra bảng dữ liệu (`CommonTableSummaryRow:440`), **không** có lưới ô có `rowSpan/colSpan` sửa được tại chỗ. `client/src/features/bieuMau/thietKeBieuMau/helpers/luoi.ts` là hệ khác (chốt **C38**) và nằm ở `features/` ⇒ tầng dưới không import lên được |
| `ThanhCongCuTuDo.tsx` — 2 hàng, 15 nút theo Figma frame 3 | `…/components/` | `@base` không có thanh công cụ ngữ cảnh nào |
| `MenuChuotPhaiO.tsx` — 10 mục, 3 nhóm ngăn cách | `…/components/` | bọc `CommonDropdownBasic`, phần `contextmenu` + `Sửa chữ`/`Chọn trường dữ liệu…` (`R-TLMI-172`) là riêng |
| `BanInPaper.tsx` — renderer giấy | `…/components/` | riêng nghiệp vụ mẫu in |
| `BoCucMauPane.tsx` · `DongKhoiBoCuc.tsx` · `ChuThichBoCuc.tsx` | `…/components/` | cột trái đặc thù (⠿ · 👁 · tên · chấm đỏ · ✕) |
| `ThanhXemTruoc.tsx` · `XemTruocPane.tsx` | `…/components/` | `@base` không có thanh zoom/undo nào |
| `BadgeTrangThai.tsx` | `…/components/` | 3 trạng thái riêng của màn; `@base` không export `CommonTag` |
| `helpers/luoiTuDo.ts` · `doRongCot.ts` · `keThua.ts` · `kiemTraMau.ts` · `chuanHoaMau.ts` · `mauChuan.ts` · `truongDungChung.ts` | `…/helpers/` | thuật toán nghiệp vụ thuần |
| `hooks/mauInStore.ts` (+ Provider) · `useVungChon` · `useKeoThaO` · `useLuuMau` · `useDongMan` · `useDatLaiMauChuan` | `…/hooks/` | state riêng của editor |

### 3.3 **18 mục chưa commit: giữ gì / bỏ gì**

#### A. 11 file đã sửa (` M`)

| # | File | Xử lý | Vì sao |
|---|---|---|---|
| 1 | `src/app/i18n/vi.ts:256` (`thietLapMauIn: 'Thiết lập mẫu in'`) | ❌ **BỎ — revert** | D1: không còn mục menu |
| 2 | `src/app/i18n/en.ts:233` (`'Print templates'`) | ❌ **BỎ — revert** | như trên |
| 3 | `src/app/layouts/AppLayout.tsx` (thêm cờ `fullBleed`, `padding: fullBleed ? 0 : 16`, `overflow: fullBleed ? 'hidden' : 'auto'`) | ❌ **BỎ — revert** | cờ chỉ sinh ra để phục vụ route editor; modal không dùng padding của AppLayout |
| 4 | `src/app/layouts/shell/menuRegistry.tsx:46-47, 502-507` | ❌ **BỎ — revert** | D1 |
| 5 | `src/base/domainKit/index.ts` (`export * from './mauIn'`) | ✅ **GIỮ** | engine vẫn ở đúng chỗ |
| 6 | `src/base/icons/index.ts` (+18 icon) | ✅ **GIỮ** | Figma frame 1-6 dùng đúng nhóm icon này |
| 7 | `src/base/index.ts` (export `CommonSegmented:267` · `CommonColorPicker:269` · `PropSection:226` · `PropField:228`) | ✅ **GIỮ** | cả 4 component đều trúng Figma |
| 8 | `src/features/heThong/routes.tsx:14-15, 61-80` | ❌ **BỎ — revert** | D1 |
| 9 | `src/features/muaHang/chungTuMuaHang/components/modal/MuaDichVuModal.tsx:35, 627, 632` | ⚠️ **SỬA** — giữ chỗ gắn `<NutInChungTu>`; **bỏ** `onMoThietLap={(ma) => void navigate(duongDanThietLapMauIn(ma))}`, đổi sang mở modal tại chỗ | D1 + D3: mua dịch vụ xuống lô 6, bán hàng lên pilot |
| 10 | `src/features/muaHang/chungTuMuaHang/constants/constants.ts` | ❌ **BỎ — revert** | diff chỉ xoá một dòng trắng |
| 11 | `src/features/muaHang/chungTuMuaHang/constants/permissions.ts` (`viewDetail: 'MuaDichVu.View.Detail'`) | ✅ **GIỮ** | chốt **C13** vẫn gate bằng `<ChucNang>.View.Detail` |

#### B. 5 base component mới (`??`)

| File | Xử lý | Vì sao |
|---|---|---|
| `src/base/components/fields/CommonSegmented.tsx` | ✅ **GIỮ** | cụm `Căn` (Figma frame 2 lưới cột, frame 3 thanh công cụ) |
| `src/base/components/fields/CommonColorPicker.tsx` | ⚠️ **GIỮ + SỬA** | Figma frame 1/1b vẽ **10 ô màu** + ô hex; `R-TLMI-066` cũng nói 10. Phải soát số ô preset và ràng `#rrggbb` (`MSG_210`) |
| `src/base/components/layout/PropSection.tsx` | ✅ **GIỮ** | nhóm `Giấy và chữ` / `Riêng của mẫu` / `Dòng in ra` / `Cột in ra`, có slot phải cho link đỏ |
| `src/base/components/layout/PropField.tsx` | ✅ **GIỮ** | mọi ô của cột phải |
| `src/base/components/layout/propField.css` | ✅ **GIỮ** | |

#### C. Engine `src/base/domainKit/mauIn/` — 48 file

| Phần (dòng đo được) | Xử lý | Vì sao |
|---|---|---|
| `components/SortableList.tsx` (113) | ✅ **GIỮ NGUYÊN** | D8 — sortable tự dựng trên `@dnd-kit/core`, có `KeyboardSensor`; không có gói thay thế |
| `components/MauInPaper.tsx` (578) | ⚠️ **GIỮ KHUNG, VIẾT LẠI THÂN** → `BanInPaper.tsx` | D13 giữ ý "một renderer"; nhưng 7 khối cũ (`DON_VI/TIEU_DE/THONG_TIN/BANG/TONG_HOP/CHU_KY/TU_DO`) ≠ **4 khối chuẩn + n khối tự do** của `R-TLMI-008/009/010` |
| `components/MauInEditor.tsx` (176) · `CanvasPane.tsx` (220) · `OutlinePane.tsx` (186) | ⚠️ **GIỮ Ý 3 CỘT, VIẾT LẠI** | đúng bố cục Figma (280 / co giãn / ~390) nhưng thiếu thanh Xem trước, thiếu badge, thiếu 2 dòng chú thích cuối cột trái, thiếu `+ Thêm khối tự do` |
| `components/ThanhKeoCot.tsx` (92) · `RaiCot.tsx` (34) · `NutDongCot.tsx` (25) | ❌ **BỎ** | kéo mép cột là luật `R-MAUIN-100` của bản cũ; `R-TLMI-108` nhập độ rộng bằng **ô số**, Figma frame 2 chỉ có ô `Rộng %` |
| `components/NutInChungTu.tsx` (121) | ⚠️ **GIỮ, SỬA NẶNG** | đúng ý split button + ẩn mục khi thiếu quyền (`R-TLMI-032`). Phải đổi: thứ tự menu (`R-TLMI-023`), nhãn cố định `Mẫu tùy chỉnh` / `Thiết lập mẫu in…` (`R-TLMI-024`), gate `R-TLMI-025` (form **thêm mới** không có nút In), `R-TLMI-261` (In disable ⇒ **cả menu không mở được**), `onMoThietLap` mở **modal tại chỗ** chứ không `navigate`, và `QUYEN_THIET_LAP` literal ở `:26` chuyển vào `constants/permissions.ts` |
| `components/HopXemTruocBanIn.tsx` (133) + css | ⚠️ **GIỮ, SỬA** → `modal/XemTruocBanInModal.tsx` | thiếu cột thumbnail, `Trang 1 / 1`, zoom `− 100% +`, `Xuất file`, và **nút `Sửa mẫu`** (`R-TLMI-027/269`) — Figma frame 0 |
| `components/HopLichSuMauIn.tsx` (240) + css | ❌ **BỎ** | không có luật `R-TLMI-*` nào; sinh từ mock HTML |
| `components/inspector/InspectorPane.tsx` (76) · `dieuKhien.tsx` (100) | ✅ **GIỮ KHUNG** | bộ chuyển bảng chỉnh theo khối đang chọn (`R-TLMI-213/214/216`) |
| `components/inspector/TrangInspector.tsx` (147) | ⚠️ **VIẾT LẠI** → `ThietLapMauInspector.tsx` | chưa có khái niệm **kế thừa** (D5); thiếu link `Theo thiết lập chung`, `Số cột để tự động in ngang`, `Căn ảnh`, link `Mở Cấu hình báo cáo chứng từ` |
| `components/inspector/DonViInspector.tsx` (57) | ⚠️ **VIẾT LẠI** → `DauTrangInspector.tsx` | 5 dòng → **7 ô tick** kèm giá trị thật hiển thị mờ (`R-TLMI-077/081/082`, Figma frame 4) |
| `components/inspector/TieuDeInspector.tsx` (63) | ✅ **GIỮ, SỬA NHẸ** | gần đúng; đổi `noiDung` từ **80 → 255** ký tự (`R-TLMI-085`) |
| `components/inspector/BangInspector.tsx` (122) | ⚠️ **GIỮ, SỬA NẶNG** | thiếu `Lặp tiêu đề mỗi trang`, cột `Cộng`, cụm `Căn`, ô `Tìm cột`, dòng tổng độ rộng, link `Chia đều về 100%` |
| `components/inspector/KhoiTruongInspector.tsx` (149) | ❌ **BỎ** | mô hình cũ là "danh sách trường theo dòng"; mô hình mới là **lưới ô** (D7) |
| `components/inspector/TongHopInspector.tsx` (55) | ❌ **BỎ** | `R-TLMI-010`: tổng tiền **phải tự dựng bằng khối tự do** — không còn khối `TONG_HOP` |
| `components/inspector/ChuKyInspector.tsx` (124) | ⚠️ **VIẾT LẠI** | bản cũ tự khai ≤4 ô ký; mới là **5 chức danh từ Thiết lập người ký** + ô ký tự do **không giới hạn** (`R-TLMI-182/193`) |
| `components/inspector/KiemTraPanel.tsx` (58) | ❌ **BỎ** | `R-TLMI-231/232/233`: lỗi đánh dấu **tại chỗ** + chấm đỏ ở dòng khối + tooltip khi rê chuột — **không** có panel liệt kê lỗi |
| `components/inspector/CoChuKhoiField.tsx` (50) | ❌ **BỎ** | `coChu` theo từng khối không có trong luật `R-TLMI-*` (là bổ sung riêng của bản cũ, A5 §4.4-1) |
| `api/schemas.ts` (403) | ⚠️ **VIẾT LẠI** → `api/model.ts` | đổi 7 khối → 4 + n; thêm `truongDungChung`, lưới ô neo, `maNghiepVu`; mọi ô kế thừa chuyển `.optional()` (D5) |
| `api/mauInApi.ts` (106) | ⚠️ **GIỮ KHUNG, ĐỔI HỢP ĐỒNG** | khoá `(maLoaiChungTu, maNghiepVu)` (Q-16); A8/A9 (lịch sử) bỏ |
| `constants/gioiHan.ts` (214) | ⚠️ **GIỮ ~40%** → `constants/constants.ts` | giữ cách làm (một chỗ khai mọi hằng). Đổi gần hết số: tiêu đề 80→**255**, ô ký ≤4→**không giới hạn**; thêm 20 dòng / 6 cột / 10 khối / 60 bước undo / lề 0-5 / cỡ chữ 8-20 / tiêu đề 10-36 / rộng cột 3-90 / số cột ngang 1-50. **Bỏ** `duongDanThietLapMauIn():212` |
| `constants/boCucCot.ts` (31) | ❌ **BỎ** | phục vụ kéo mép cột đã bỏ |
| `helpers/kiemTraMau.ts` (401) | ⚠️ **VIẾT LẠI** | phải bám **đúng 17 dòng** của `R-TLMI-239`; gỡ luật "khối rỗng là lỗi" (D12); thêm thứ tự lỗi đầu tiên (C21) |
| `helpers/chuanHoaMau.ts` (131) | ⚠️ **GIỮ Ý, VIẾT LẠI** | chốt **C02**: chuẩn hoá = sắp khoá theo thứ tự cố định + bỏ khoá `null`/`undefined` + bỏ id kỹ thuật, rồi so với mẫu chuẩn |
| `helpers/hopNhatVoiCatalog.ts` (235) | ✅ **GIỮ, SỬA** | đúng ý `R-TLMI-093` (cột mới xuất hiện **cuối bảng**) · `R-TLMI-167` (ô mới vào kho trường, **không** tự chen vào khối tự do) · chốt **C10** (phần tử bị xoá: mờ + nhãn "không còn trên form", loại khi Lưu) |
| `helpers/thaoTacKhoi.ts` (273) | ⚠️ **GIỮ ~50%** | giữ `sapXepKhoi` · `diChuyenKhoi` · `anHienKhoi` · `xoaKhoi`; **bỏ** `keoRongCot` · `keoRongCotBang` · `cotBuTru` |
| `helpers/khoiMoi.ts` (116) · `trangGiay.ts` (19) · `thoiDiem.ts` (23) · `dinhDangGiaTri.ts` (72) | ✅ **GIỮ, SỬA NHẸ** | tiện ích thuần |
| `helpers/inBanIn.tsx` (151) | ✅ **GIỮ** | mở tab in + `window.print`; không đụng luật mới |
| `store/mauInStore.ts` (150) · `mauInStoreContext.ts` (35) · `MauInStoreProvider.tsx` | ⚠️ **GIỮ KIẾN TRÚC, VIẾT LẠI, CHUYỂN SANG `hooks/`** | giữ "một store mỗi lần mở" + `zundo`; thêm `immer`, đặt `limit: 60`, bỏ ~10 action mô hình cũ (`themDongTuDo`, `xoaDongTuDo`, `capNhatTruongTongHop`, `sapXepTruongTongHop`, `keoRongCot`…), thêm ~14 action lưới ô |
| `hooks/useBoCucCot.ts` | ❌ **BỎ** | phục vụ kéo mép cột |
| `i18n/vi.ts` (190 dòng · 154 khoá) · `en.ts` (181) · `registerMauInI18n.ts` (13) | ⚠️ **GIỮ NAMESPACE `mauIn`, THAY NỘI DUNG** | chữ mới phải **nguyên văn BA** (`6.messages.md` + `02-rules.md`); khoá cũ sinh từ mock HTML. Thêm nhóm chữ **in ra giấy** vốn đang hardcode trong `gioiHan.ts` (Q13) |
| `test/` — 13 file | ❌ **BỎ 11, GIỮ 2** | giữ `mauInStore.test.ts` và `schemasVaDinhDang.test.ts` làm **khung mẫu**; 11 file còn lại mang mã `R-MAUIN-*` đã hết hiệu lực |
| `test/fixtures/mdv.catalog.json` · `mdv.mau-chuan.json` · `mdv.du-lieu-mau.json` | ❌ **BỎ** | fixture Mua dịch vụ; pilot mới là Bán hàng (D3) ⇒ dựng `fixtures/bh.*.json` |

#### D. Feature `src/features/heThong/thietLapMauIn/` — 20 file

| Phần | Xử lý | Vì sao |
|---|---|---|
| **Toàn bộ 20 file** | ❌ **BỎ** | D1 — không còn màn danh sách, không còn route. Module tồn tại **chỉ** để phục vụ route |
| `pages/ThietLapMauInPage.tsx` · `pages/ChinhSuaMauInPage.tsx` · `pages/thietLapMauIn.css` | ❌ **BỎ** | hai màn có route |
| `fields/danhSachFields.tsx` · `helpers/locLoaiChungTu.ts` | ❌ **BỎ** | phục vụ lưới 47 loại chứng từ |
| `components/ChonChungTuXemThu.tsx` | ❌ **BỎ** | `R-TLMI-219`: **không có chế độ dữ liệu mẫu** ⇒ "chọn chứng từ xem thử" là ngược luật |
| `components/TrangThaiMauTag.tsx` | ⚠️ **CHUYỂN Ý** → `@domain-kit/mauIn/components/BadgeTrangThai.tsx` | 3 trạng thái mới là `Đã lưu / Chưa lưu / Có lỗi` (`R-TLMI-240/241/242`), không phải "chuẩn / tuỳ chỉnh" |
| `api/queries.ts` (8 hook) | ⚠️ **CHUYỂN Ý** → `@domain-kit/mauIn/api/queries.ts` | giữ cách đặt query key, bỏ 4 hook của danh sách + lịch sử |
| `i18n/` (95 khoá × 2) | ❌ **BỎ** | gộp về namespace `mauIn` duy nhất (D2) |
| `test/ThietLapMauInPage.test.tsx` (6 it) · `test/ChinhSuaMauInPage.test.tsx` (8 it) | ❌ **BỎ** | test của màn có route |

**Tổng kết đếm được:**

| | Số mục |
|---|---|
| ✅ Giữ nguyên | **9** (SortableList · InspectorPane+dieuKhien · inBanIn · 4 base component mới · domainKit barrel · icons barrel) |
| ⚠️ Giữ và sửa | **16** |
| ❌ Bỏ | **21 nhóm file engine + 6 file `M` revert + toàn bộ 20 file feature** |

---

## §4. Kiến trúc module — cây thư mục sẽ sinh

```
client/src/base/domainKit/mauIn/                      ← TIER 2.5, MỘT module, cây PHẲNG một bậc
├── index.ts                                          ← FILE DUY NHẤT ở gốc module
├── api/
│   ├── mauInApi.ts                                   gọi HTTP (A1…A6)
│   ├── model.ts                                      Zod + type (MauIn · KhoiTuDo · OTuDo · ThietLapChung · KhoTruong)
│   ├── queries.ts                                    query key + hook TanStack
│   └── mock.ts                                       ⚠ NỢ — xoá khi BE xong
├── components/
│   ├── BoCucMauPane.tsx                              cột trái  (Figma: BỐ CỤC MẪU)
│   ├── DongKhoiBoCuc.tsx                             một dòng khối: ⠿ · 👁 · tên · chấm đỏ · ✕
│   ├── ChuThichBoCuc.tsx                             2 gạch đầu dòng cuối cột trái
│   ├── ThanhXemTruoc.tsx                             ↶ ↷ · Khổ · Hướng · ☐ lưới · − % + · Vừa khung
│   ├── XemTruocPane.tsx                              cột giữa: khung cuộn + trang giấy
│   ├── BanInPaper.tsx                                renderer giấy DUY NHẤT (canvas + bản in)
│   ├── LuoiTuDo.tsx                                  lưới ô kiểu Excel (chọn · Shift-vùng · phím tắt)
│   ├── OLuoi.tsx                                     một ô neo (draggable + droppable)
│   ├── ThanhCongCuTuDo.tsx                           thanh 2 hàng, 15 nút
│   ├── MenuChuotPhaiO.tsx                            menu 10 mục / 3 nhóm
│   ├── BadgeTrangThai.tsx                            Đã lưu · Chưa lưu · Có lỗi
│   ├── NutInChungTu.tsx                              split button In ▾ (gắn vào form chứng từ)
│   ├── inspector/
│   │   ├── InspectorPane.tsx                         bộ chuyển theo khối đang chọn
│   │   ├── ThietLapMauInspector.tsx                  ráp 2 nhóm dưới
│   │   ├── GiayVaChuGroup.tsx                        6 ô kế thừa + link Theo thiết lập chung
│   │   ├── RiengCuaMauGroup.tsx                      màu chữ · hình nền · độ đậm · căn ảnh · ảnh
│   │   ├── DauTrangInspector.tsx                     7 ô tick + giá trị thật
│   │   ├── TieuDeInspector.tsx
│   │   ├── BangInspector.tsx · BangCotRow.tsx
│   │   ├── KhoiTuDoInspector.tsx · KhoTruongRow.tsx
│   │   └── ChuKyInspector.tsx · OKyRow.tsx
│   └── modal/                                        ← thư mục con DUY NHẤT được phép trong components/
│       ├── ThietLapMauInModal.tsx                    vỏ CommonModalShell toàn màn + Provider
│       ├── XemTruocBanInModal.tsx                    màn Xem trước bản in (lối vào 2)
│       ├── HopDatTenKhoiModal.tsx                    MSG_206
│       ├── HopChonTruongO.tsx                        hộp chọn cạnh ô (Ô trống · Chữ tự do · kho trường)
│       ├── HopThayDoiChuaLuuModal.tsx                MSG_401 — BA nút (D11)
│       ├── XacNhanDatLaiModal.tsx                    MSG_402
│       ├── XacNhanXoaKhoiModal.tsx                   MSG_403
│       └── XacNhanGopOModal.tsx                      MSG_404
├── constants/
│   ├── constants.ts                                  GIOI_HAN_* · ZOOM · MA_MSG_* · KHO_GIAY · FONT · MAU_PRESET
│   ├── paths.ts                                      CHỈ endpoint API (KHÔNG có route màn — D1)
│   └── permissions.ts                                MA_QUYEN_MAU_IN (Q-15)
├── fields/
│   ├── types.ts                                      type UI thuần (VungChon · ViTriO · LoaiNoiDungO · TrangThaiMau)
│   ├── boCucKhoiFields.tsx                           icon + nhãn từng loại khối
│   ├── cotBangFields.tsx                             cột của lưới "Cột in ra"
│   ├── chuKyFields.tsx                               cột của lưới ô ký
│   ├── khoTruongFields.tsx                           cột của lưới kho trường
│   └── texts.ts                                      map mã lỗi → khoá i18n
├── helpers/
│   ├── luoiTuDo.ts                 ⭐ bangPhu · chonVung · noiVungTheoOGop · gopO · tachO · themDong · themCot · xoaDong · xoaCot · doiNoiDungHaiO
│   ├── doRongCot.ts                ⭐ chiaDeuVe100 · tongDoRong
│   ├── keThua.ts                   ⭐ giaTriHieuDung · laTheoChung · veTheoChung
│   ├── truongDungChung.ts             gom/lọc truongDungChung (R-TLMI-156/164)
│   ├── kiemTraMau.ts               ⭐ 17 dòng của R-TLMI-239 + thứ tự lỗi đầu tiên (C21)
│   ├── chuanHoaMau.ts                 chuẩn hoá để so với mẫu chuẩn (C02)
│   ├── mauChuan.ts                    dựng mẫu chuẩn từ đặc tả form (R-TLMI-006…010)
│   ├── hopNhatVoiCatalog.ts           cột/trường mới · phần tử bị xoá (C10)
│   ├── thaoTacKhoi.ts                 sắp xếp · ẩn/hiện · xoá khối
│   ├── dinhDangGiaTri.ts · thoiDiem.ts · trangGiay.ts
│   └── inBanIn.tsx                    mở tab in
├── hooks/
│   ├── mauInStore.ts                  zustand + immer + zundo(limit 60)
│   ├── MauInStoreProvider.tsx · useMauInStore.ts
│   ├── useVungChon.ts                 vùng chọn lưới + phím tắt (R-TLMI-132/173)
│   ├── useKeoThaO.ts                  DndContext cho K1…K4
│   ├── useLuuMau.ts                   Lưu · Ctrl+S · 409 · MSG_101
│   ├── useDatLaiMauChuan.ts           MSG_402 · MSG_102
│   └── useDongMan.ts                  Đóng · Esc · MSG_401 (3 nhánh)
├── i18n/
│   ├── vi.ts · en.ts                  MỘT namespace `mauIn`
│   └── registerMauInI18n.ts
├── pages/
│   ├── ThietLapMauInScreen.tsx        CHỈ RÁP: header · 3 cột · chân màn · DndContext
│   └── mauIn.css
└── test/
    ├── fixtures/{bh.catalog.json, bh.mau-chuan.json, bh.chung.json, bh.du-lieu.json}
    └── (13 file test — §13.1)
```

**Kiểm khung PMKT:**

| Luật cứng | Kết quả |
|---|---|
| Gốc module **chỉ có `index.ts`** | ✅ |
| Không tách màn theo hành vi; mọi popup ở `components/modal/` | ✅ 8 popup |
| Không `../../` — trong module dùng `./`, ra ngoài dùng `@base` · `@platform` · `@core` | ✅ |
| 9 thư mục chuẩn, không thừa | ✅ `store/` cũ đã gộp vào `hooks/` |
| `helpers/` thuần: không React, không mạng, không `t()` | ✅ (trừ `inBanIn.tsx` đã có sẵn, dùng `ReactDOM` để dựng tab in — giữ nguyên hiện trạng) |
| `routes.tsx` | ➖ **Không có** — màn không có route (D1). Khác biệt **duy nhất** so với module có route |

**Phần gắn vào từng nghiệp vụ** (ngoài engine) — đúng **2 chỗ** mỗi nghiệp vụ:

```
client/src/features/banHang/chungTuBanHang/
├── components/ChungTuBanHangThemMoiModal.tsx    +1 import từ '@domain-kit/mauIn'
│                                                +1 <NutInChungTu … /> trong thanh hành động
│                                                (chỉ ở chế độ Sửa / Xem — R-TLMI-025)
└── constants/permissions.ts                     +1 hằng  viewDetail: 'BanHang.View.Detail'   (C13)
```

Engine **không** biết gì về bán hàng: mọi thứ riêng nghiệp vụ đi vào qua props của `NutInChungTu`
(`maLoaiChungTu`, `maNghiepVu`, `chungTuId`, `tieuDeBanIn`, `quyenXemChiTiet`, `onInMauCoDinh`).

---

## §5. Checklist artefact (`fe-khung-kien-truc-chuan.md §5`)

| # | Artefact | Bắt buộc | Kế hoạch |
|---|---|---|---|
| 1 | `index.ts` gốc module | ✔ | cửa ra: `ThietLapMauInModal` · `XemTruocBanInModal` · `NutInChungTu` · `registerMauInI18n` · type công khai |
| 2 | `api/` Zod + hook | ✔ | `model.ts` · `mauInApi.ts` · `queries.ts` · `mock.ts` (**nợ**) |
| 3 | `components/` | ✔ | 12 component + 12 inspector |
| 4 | `components/modal/` | ✔ | 8 popup |
| 5 | `constants/constants.ts` | ✔ | mọi giới hạn số, mã `MSG_`, khổ giấy, font, 10 màu preset |
| 6 | `constants/paths.ts` | ✔ | chỉ endpoint API |
| 7 | `constants/permissions.ts` | ✔ | `MA_QUYEN_MAU_IN` (Q-15) |
| 8 | `fields/types.ts` | ✔ | type UI thuần |
| 9 | `fields/*Fields.tsx` | ✔ | 4 mô tả lưới + `texts.ts` |
| 10 | `helpers/` thuần | ✔ | 13 file |
| 11 | `hooks/` | ✔ | store + Provider + 5 hook |
| 12 | `i18n/vi.ts` + `en.ts` + register | ✔ | **một** namespace `mauIn`, ~215 khoá × 2 |
| 13 | `pages/<Tên>.tsx` + css | ✔ | `ThietLapMauInScreen.tsx` chỉ ráp |
| 14 | `test/` | ✔ | 13 file, mọi `it()` mang mã `R-TLMI-…` |
| 15 | route + quyền | ➖ | **Route: không áp dụng** (D1). Quyền gate ở `NutInChungTu.tsx` + `constants/permissions.ts` |

---

## §6. Route & quyền

**Route: Không áp dụng — màn là modal, không có URL riêng (D1).** Cả hai route ở
`client/src/features/heThong/routes.tsx:61-80` bị revert; mục menu ở
`client/src/app/layouts/shell/menuRegistry.tsx:502-507` bị revert.

### Quyền (BR25 · chốt **C13** · Q-15)

| Hành vi | Mã quyền | Luật |
|---|---|---|
| Hiện mục menu `Thiết lập mẫu in…` và nút `Sửa mẫu` | `HTMauIn.Edit` **VÀ** `<ChucNang>.View.Detail` của nghiệp vụ đang mở | `R-TLMI-031` · `R-TLMI-032` · `R-TLMI-269` |
| Mở màn (đọc mẫu) | `HTMauIn.View` | `R-TLMI-031` |
| Lưu mẫu | `HTMauIn.Edit` | `R-TLMI-034` (BE chặn, FE chỉ hiện lỗi) |
| In `Mẫu tùy chỉnh` | `<ChucNang>.View.Detail` — **không cần** `HTMauIn.*` | `R-TLMI-033` |

- **Thiếu quyền ⇒ ẩn hẳn, KHÔNG disable** (`R-TLMI-032`) ⇒ dùng `Can` / `useHasPermission`, render `null`.
- Mọi mã quyền **đặt một chỗ** `constants/permissions.ts` (Q-15). Bản cũ để literal
  `const QUYEN_THIET_LAP = 'HTMauIn.Edit'` ở
  `client/src/base/domainKit/mauIn/components/NutInChungTu.tsx:26` ⇒ chuyển vào `constants/permissions.ts`.
- Thiếu quyền **In** ⇒ `MSG_COMMON_003` theo BR25.2 (chốt **C15**, lệch **L-4**) — **không** dùng
  `MSG_PMKT-E-14549_21_002` (mã đó chỉ dành cho quyền *Thiết lập mẫu in*).
- `R-TLMI-035`: có quyền ở **một** chi nhánh là sửa được mẫu dùng chung cho **mọi** chi nhánh; chốt **C24**
  quyết **không thêm cảnh báo** — không tự thêm hộp thoại ngoài đặc tả.

---

## §7. Bản đồ màn ↔ file con ↔ SCR ↔ UC ↔ Matrix

| File con | Màn / vùng | Figma frame | Nguồn `SCR` | UC | Nhóm luật |
|---|---|---|---|---|---|
| [`01-modal-thiet-lap-mau-in.md`](01-modal-thiet-lap-mau-in.md) | Khung modal: header · 3 cột · chân · cột trái *Bố cục mẫu* · thanh *Xem trước* | 1, 1b | `SCR:18-81` · `SCR:201-253` · `SCR:306-317` | UC01 | L, M, N |
| [`02-panel-thiet-lap-mau.md`](02-panel-thiet-lap-mau.md) | Bảng chỉnh *Thiết lập mẫu* — Giấy và chữ + Riêng của mẫu | 1, 1b | `SCR:88-160` · `SCR:254-279` | UC01 | C, D, E |
| [`03-panel-dau-trang-va-tieu-de.md`](03-panel-dau-trang-va-tieu-de.md) | Bảng chỉnh *Thông tin đầu trang* + *Tiêu đề bản in* | 4, 5 | `SCR:118-140` · `SCR:280-283` | UC01 | F, G |
| [`04-panel-bang.md`](04-panel-bang.md) | Bảng chỉnh *{Tên bảng}* — cột in ra, chia đều 100% | 2 | `SCR:141-175` · `SCR:277-279` | UC01 | H |
| [`05-khoi-tu-do-luoi-o.md`](05-khoi-tu-do-luoi-o.md) | Khối tự do: lưới ô, thanh công cụ, menu chuột phải, kho trường | 3 | `SCR:176-200` · `SCR:284-292` | UC01 | I |
| [`06-panel-chu-ky.md`](06-panel-chu-ky.md) | Bảng chỉnh *Chữ ký* | 6 | `SCR:201-215` · `SCR:293-300` | UC01 | K |
| [`07-loi-vao-va-xem-truoc-ban-in.md`](07-loi-vao-va-xem-truoc-ban-in.md) | Menu In trên form · nút *Sửa mẫu* · modal *Xem trước bản in* | 0 | `SCR:3-17` · `SCR:244-253` · `SCR:357-377` | UC01, UC02 | B, P |
| [`08-hop-dong-api-va-i18n.md`](08-hop-dong-api-va-i18n.md) | Hợp đồng Zod + bảng khoá i18n đầy đủ + hằng số + quyền | — | — | — | — |
| [`09-truy-vet-va-kiem-thu.md`](09-truy-vet-va-kiem-thu.md) | Bảng truy vết **237 luật** + danh sách test chi tiết | — | — | — | tất cả |

Bảng truy vết ở [`09-truy-vet-va-kiem-thu.md §1`](09-truy-vet-va-kiem-thu.md) **sinh bằng máy** từ
`02-rules.md` — **không sửa tay**; cách sinh lại ở `09-…md §4`.

⚠ Phiếu này chỉ có **một** file `SCR_ThietLapMauIn.md`; ma trận ẩn/hiện ở
`Matrix/PMKT-E-14549_21_ThietLapMauInChungTu/SCR_ThietLapMauIn_MaTranAnHien.md` (`MT`) đã được
`/audit-spec` dịch thành các luật `R-TLMI-*` có trích `MT:nn` ⇒ mỗi file con dịch lại từ luật, **không**
mở lại `Matrix/**`.

---

## §8. i18n — **MỘT namespace `mauIn`** cho cả module

```
mauIn:
├── man.*            tiêu đề màn · 3 badge trạng thái · 3 nút chân màn · nút ? và ✕
├── boCuc.*          cột trái: tiêu đề · tên 4 khối chuẩn · nút thêm khối · 2 dòng chú thích
├── thanhXemTruoc.*  hoàn tác · làm lại · Khổ giấy · Hướng giấy · Hiện lưới căn chỉnh · Vừa khung
├── thietLapMau.*    Giấy và chữ · Riêng của mẫu · Theo thiết lập chung · 2 link mở cấu hình
├── dauTrang.*       ô tick khối · 7 ô tick dòng · link
├── tieuDe.*         Nội dung · Cỡ chữ · Căn · IN HOA · In đậm · Dòng ngày tháng · ghi chú
├── bang.*           Tên bảng in ra · In cột STT · Dòng Cộng · Lặp tiêu đề mỗi trang · Kẻ ô · lưới cột · Chia đều về 100%
├── tuDo.*           Tên khối · Tìm kiếm · kho trường · thanh công cụ (15) · menu chuột phải (10) · nhãn ngữ cảnh
├── chuKy.*          lưới ô ký · Thêm ô ký tự do · Dòng Ngày… · Chỗ trống ký · hộp ghi chú · link
├── banIn.*          màn Xem trước bản in · chữ in ra giấy ((Ký, họ tên) · Cộng · STT · Tổng: · Ngày…)
├── menuIn.*         Mẫu tùy chỉnh · Thiết lập mẫu in… · 2 tooltip nút In disable
└── msg.*            26 mã MSG_PMKT-E-14549_21_* + 2 mã MSG_COMMON_* dùng lại
```

- **Chuỗi `vi` là NGUYÊN VĂN tiếng Việt của BA** — chép từ `6.messages.md` và `02-rules.md`, **cấm diễn
  đạt lại** (luật 2 của `CLAUDE.md`).
- Chuỗi động dùng interpolation: `t('mauIn:msg.e203', { TenBang })`, **không cộng chuỗi**.
- Bảng đầy đủ **mọi khoá** kèm `vi` / `en` ở [`08-hop-dong-api-va-i18n.md §3`](08-hop-dong-api-va-i18n.md).
- ⚠ Nhóm chữ **in ra giấy** (`(Ký, họ tên)` · `(Ký, họ tên, đóng dấu)` · `Cộng` · `STT` · `Tổng:` ·
  `Ngày … tháng … năm …`) vẫn phải có khoá i18n vì người dùng **thấy** chúng trên trang xem trước. Bản cũ
  để cứng trong `constants/gioiHan.ts` ⇒ đưa hết vào `i18n/`. Xem **Q13** về giá trị `en`.

---

## §9. Thứ tự thực hiện — chia lô làm song song được

```
Lô 0 ── Lô 1 ─┬─ Lô 2 ─┬─ Lô 5 ── Lô 6
              ├─ Lô 3 ─┤
              └─ Lô 4 ─┘
```

| Lô | Nội dung | Phụ thuộc | Song song với | Ước lượng |
|---|---|---|---|---|
| **0** | Dọn nền: revert 6 file ` M` (route/menu/AppLayout/i18n app), xoá `features/heThong/thietLapMauIn/`, xoá các file engine đã chốt BỎ ở §3.3-C. **`git add` phần giữ lại TRƯỚC khi đụng barrel** | — | — | 0,5 ngày |
| **1** | Nền dữ liệu: `api/model.ts` (Zod), `constants/constants.ts`, `helpers/mauChuan.ts` · `keThua.ts` · `chuanHoaMau.ts`, `hooks/mauInStore.ts` (immer + zundo 60), `i18n/` đủ 2 ngôn ngữ, fixture `bh.*`, `api/mock.ts` | Lô 0 | — | 2 ngày |
| **2** | Khung màn: `pages/ThietLapMauInScreen.tsx`, `components/modal/ThietLapMauInModal.tsx`, `BoCucMauPane` + `DongKhoiBoCuc` + `ChuThichBoCuc`, `ThanhXemTruoc`, `XemTruocPane`, `BanInPaper`, `BadgeTrangThai`, `hooks/useLuuMau` · `useDongMan` · `useDatLaiMauChuan`, `helpers/kiemTraMau.ts`, 4 modal xác nhận | Lô 1 | 3, 4 | 3 ngày |
| **3** | Bốn bảng chỉnh khối chuẩn: `ThietLapMauInspector` (+`GiayVaChuGroup` +`RiengCuaMauGroup`), `DauTrangInspector`, `TieuDeInspector`, `BangInspector` (+`BangCotRow` +`helpers/doRongCot.ts`), `ChuKyInspector` (+`OKyRow`) | Lô 1 | 2, 4 | 3 ngày |
| **4** | **Khối tự do** (lô nặng nhất, tách riêng được): `helpers/luoiTuDo.ts` · `truongDungChung.ts`, `LuoiTuDo` + `OLuoi`, `ThanhCongCuTuDo`, `MenuChuotPhaiO`, `HopChonTruongO`, `HopDatTenKhoiModal`, `KhoiTuDoInspector` + `KhoTruongRow`, `hooks/useVungChon` · `useKeoThaO` | Lô 1 | 2, 3 | 4 ngày |
| **5** | Lối vào + xem trước: `NutInChungTu` (sửa), `XemTruocBanInModal`, gắn vào **Chứng từ bán hàng** | 2, 3, 4 | — | 1,5 ngày |
| **6** | Nối nghiệp vụ còn lại (mua dịch vụ…), gỡ `api/mock.ts` khi BE xong, vòng `/qa-flow` trên trình duyệt thật | 5 | — | 1 ngày |

**Điểm chốt giữa các lô (hợp đồng nội bộ để 3 lô chạy song song không đụng nhau):**
- Lô 1 chốt **type** trong `api/model.ts` và **tên action** trong `hooks/mauInStore.ts` trước tiên.
- Lô 2 sở hữu `pages/`, `components/*.tsx` cấp 1, `components/modal/*` trừ `HopChonTruongO`/`HopDatTenKhoiModal`.
- Lô 3 sở hữu `components/inspector/*` trừ `KhoiTuDoInspector` + `KhoTruongRow`.
- Lô 4 sở hữu `LuoiTuDo` · `OLuoi` · `ThanhCongCuTuDo` · `MenuChuotPhaiO` · `KhoiTuDoInspector` ·
  `KhoTruongRow` · `HopChonTruongO` · `HopDatTenKhoiModal` · `helpers/luoiTuDo.ts` · `truongDungChung.ts`.
- `i18n/vi.ts` và `en.ts` bị **cả ba lô** đụng ⇒ chia theo nhánh khoá (`boCuc.*` lô 2 · `thietLapMau.*`
  `dauTrang.*` `tieuDe.*` `bang.*` `chuKy.*` lô 3 · `tuDo.*` lô 4) để merge không xung đột.

⚠ **Lô 4 phụ thuộc BE về kho trường**: `R-TLMI-165` nói kho trường = mọi ô trên form trừ cột lưới — do BE
suy từ đặc tả form. Trước khi có API, dùng `api/mock.ts` với fixture `bh.catalog.json`.

---

## §10. Rủi ro

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| **R1** | **Kéo thả tự dựng** trên `@dnd-kit/core` phải phục vụ 4 ca (K1-K4) trong **một** `DndContext`; sai `data.current` ⇒ thả nhầm | Cao | Phân loại bằng type liền `{ loai: 'khoi' \| 'cot' \| 'oKy' \| 'truong' \| 'oLuoi' }`; test riêng từng ca; `SortableList.tsx` đã chạy được là bằng chứng khả thi |
| **R2** | Ô "theo chung" bị **ghi giá trị đang hiển thị** ⇒ mẫu đóng băng, thiết lập chung đổi không ăn | Cao | D5; test `R-TLMI-037` so payload phải **vắng khoá**; Zod cấm `.default()` trên nhóm kế thừa; code review bắt buộc soát `api/model.ts` |
| **R3** | **Thiết lập chung** (epic `_20`) chưa tồn tại trong repo — không bảng, không màn (§2.5) | Cao | Q-03 làm "tầng tối thiểu"; FE chỉ đọc qua `GET …/thiet-lap-chung`; **Q3** |
| **R4** | **Logo đơn vị chưa có trường** ở `CompanyInfoResponse` nhưng là 1 trong 7 ô tick (chốt C03) | Cao | **Q5** — BE phải bổ sung; FE vẫn vẽ ô tick + hiện `[LOGO] cỡ vừa` như Figma frame 4 |
| **R5** | `R-TLMI-044` (đổi Khổ/Hướng trên thanh xem trước = **đổi mẫu**) gây bất ngờ cho người dùng | Trung bình | Chốt **C17** giữ đúng tài liệu nhưng ghi nhận là **rủi ro UX**; **Q2** |
| **R6** | `R-TLMI-042` không cho hoàn lại **riêng một ô** về theo chung; chỉ có nút mức nhóm | Trung bình | Chốt **C16** giữ đúng tài liệu; **Q2**. Giảm đau bằng `R-TLMI-041` (nút là một bước **Hoàn tác được**) |
| **R7** | 3 migration `V1148-V1150` **đã lên `origin/develop` + `origin/staging`** với khoá cũ `(tenant, maLoaiChungTu)` | Cao | Việc của `/plan-be`: migration **MỚI** thêm `ma_nghiep_vu` (Q-01). FE **luôn** gửi cặp `(maLoaiChungTu, maNghiepVu)` (Q-16), kể cả khi loại chỉ có một nghiệp vụ |
| **R8** | 4 bản sao cùng model (cell-app · super-admin · client · client-admin) — đổi schema phải sửa 4 chỗ + fixture vàng | Trung bình | Phiếu này **không** đụng kênh super-admin (§1 ngoài phạm vi); chốt lại khi `_21` ổn định |
| **R9** | `npm run check:committed` báo lỗi giả trên Windows (script dùng `path.join`) | Thấp | Dùng `git status --porcelain` thay thế (memory `check-committed-loi-tren-windows.md`) |
| **R10** | 5 chuỗi chưa có mã `MSG_` (L-4, L-5) ⇒ `msg.sh` sẽ báo `THIEU` | Thấp | Đã ghi nhận ở `04-quyet-dinh-ban-giao.md §7.1`; **Q1** |
| **R11** | Chưa từng chạy trên trình duyệt thật | Trung bình | Lô 6 kết thúc bằng một vòng `/qa-flow` trên dev server cổng 5173 của user (dùng lại, **không** dựng thêm) |
| **R12** | Lưới 20 × 6 = tối đa 120 ô, mỗi ô là droppable ⇒ re-render nhiều khi kéo | Trung bình | `OLuoi` bọc `memo`; vùng chọn giữ ở `useVungChon` (ngoài store undo) nên đổi vùng chọn **không** tạo bước undo (`R-TLMI-223 partialize`) |
| **R13** | `R-TLMI-218` (vẽ lại **ngay** mọi thay đổi) + lưới 120 ô + `BanInPaper` toàn trang ⇒ gõ chữ có thể giật | Trung bình | `BanInPaper` chia nhỏ theo khối, mỗi khối `memo` theo tham chiếu khối; immer giữ tham chiếu ổn định cho khối không đổi |

---

## §11. Conflict Figma ↔ Matrix / tài liệu chữ

### 11.1 Bảy điểm Figma lệch **bản code cũ** (đã xử lý trong plan)

| # | Figma | Bản code 2026-09-17 | Xử lý |
|---|---|---|---|
| 1 | Modal toàn màn trong form chứng từ | route `/he-thong/thiet-lap-mau-in` | **D1** — theo Figma + `R-TLMI-011/028/029/217/219` |
| 2 | Thanh xem trước có `↶ ↷`, zoom %, `Vừa khung`, `Hiện lưới căn chỉnh` | không có | **D4 / F8** — `R-TLMI-217…229` |
| 3 | Khối tự do = lưới ô Excel 20 × 6 có gộp/tách + menu chuột phải | danh sách trường theo dòng | **D7 / F6** — `R-TLMI-120…181` |
| 4 | Chữ ký lấy từ *Thiết lập người ký* (chức danh + tên in mờ) + ô ký tự do | tự khai ≤4 ô ký | **F7** — `R-TLMI-182…196` |
| 5 | Giấy-và-chữ + Đầu trang **kế thừa động**, link `Theo thiết lập chung` **mức nhóm** | không có kế thừa | **D5 / F2 / F3** — `R-TLMI-036…052` |
| 6 | Bảng có `Kẻ ô`, `Lặp tiêu đề mỗi trang`, cột có `Cộng` + `Căn`, nút `Chia đều về 100%` | thiếu cả bốn | **D9 / F5** — `R-TLMI-092…119` |
| 7 | Pilot **Chứng từ bán hàng** | pilot **Chứng từ mua dịch vụ** | **D3** |

### 11.2 Chỗ **Figma và tài liệu chữ lệch nhau** — phát hiện thêm khi soát 8 ảnh

| # | Điểm | Figma nói gì | Tài liệu / luật nói gì | Xử lý |
|---|---|---|---|---|
| **X1** | Số ô màu preset | Frame 1 + 1b: đếm được **10 ô màu** + ô hex `#000000` | `R-TLMI-066` "**10 ô màu** hoặc gõ mã `#rrggbb`" ✔ · nhưng ghi chú khảo sát `A0-figma.md §4.1` chép nhầm **"9 ô màu preset"** | **10 ô**. Sửa ghi chú khảo sát, không sửa luật. `CommonColorPicker` phải có đúng 10 preset |
| **X2** | Số chứng từ trên bản in | Frame 0 in `Số: SO000123 · Ngày 27 tháng 08 năm 2026` **cùng một dòng, ngay dưới tiêu đề** | `R-TLMI-091` nói **"Số chứng từ KHÔNG thuộc khối Tiêu đề"**; frame 1/2/4/5 chỉ in `Ngày 25 tháng 08 năm 2026`, **không** có `Số:` | ⚠ **Q6 — hỏi BA.** Đề xuất: theo `R-TLMI-091` (số chứng từ là trường của **khối tự do**); frame 0 là mẫu đã tuỳ chỉnh, có khối tự do đặt `Số` cạnh ngày |
| **X3** | Ngày trên bản in | Frame 0: `27 tháng 08` · Frame 1-5 (cùng chứng từ `SO000123`): `25 tháng 08` | `R-TLMI-090` "lấy **ngày chứng từ**" — một chứng từ chỉ có một ngày | Lỗi hình thức của Figma, **không chặn code**. Ghi nhận để Design sửa |
| **X4** | Nhãn cột lưới | Frame 3 (kho trường) ghi **`Tên hiển thị`**; frame 2 (lưới cột) ghi **`Tiêu hiển thị`** — thiếu chữ "u" | `R-TLMI-102` gọi là **"Tên hiển thị của cột"**; `MSG_204` cũng "Tên hiển thị của cột" | Lỗi chính tả Figma ⇒ dùng **`Tên hiển thị`** cho cả hai. Ghi nhận để Design sửa |
| **X5** | `Thông tin chứng từ` và `Tổng hợp` ở cột trái | Frame 1-6: hai khối này **có nút `✕`** ⇒ chúng là **khối tự do** | `R-TLMI-010` xác nhận thông tin chung / tổng tiền **phải tự dựng bằng khối tự do** ✔ — nhưng `R-TLMI-008` nói mẫu chuẩn có **đúng bốn loại khối, không khối nào khác** | ⚠ **Q7 — hỏi BA**: mẫu chuẩn hệ thống sinh ra **có kèm sẵn 2 khối tự do** hay người dùng phải tự thêm? Figma nói có sẵn; `R-TLMI-008` nói không |
| **X6** | `Bảng thuế` ở cột trái | Frame 1-6: icon mắt **gạch chéo** = **đang ẩn**; không có `✕` | `R-TLMI-009`: form có n lưới thì mẫu chuẩn có n khối Bảng, **mọi lưới bật** | ⚠ **Q8 — hỏi BA**: Figma vẽ `Bảng thuế` **tắt sẵn**, lệch `R-TLMI-009`. Hoặc đây là mẫu **đã tuỳ chỉnh** chứ không phải mẫu chuẩn (ăn khớp với X5) |
| **X7** | `Gộp ô` / `Tách ô` khi chưa chọn vùng | Frame 3: cả hai vẽ **mờ (disable)**, vẫn **hiện** | `R-TLMI-174` viết *"nút Gộp ô **Show**; ngược lại **Disable**"* — trộn Show / Disable | Theo Figma: **luôn hiện, mờ khi không áp dụng được**. `R-TLMI-162` cũng nói "chưa chọn ô nào thì mọi nút thanh công cụ đều **mờ**" ⇒ **mờ, không ẩn** |
| **X8** | Nhãn ngữ cảnh thanh công cụ | Frame 3: đầu hàng 1 có nhãn `Ghi chú giao hàng · ô dòng 2, cột 3` | `R-TLMI-170` liệt kê 15 nút, **không** nhắc nhãn ngữ cảnh | Theo Figma (**UI thắng**): thêm nhãn, khoá i18n `tuDo.nhanNguCanh` với interpolation `{tenKhoi}` `{dong}` `{cot}` |
| **X9** | Thanh xem trước xuống hàng | Frame 6: `Vừa khung` rơi xuống hàng 2 (thanh hẹp hơn vì cột phải rộng hơn) | — | Thanh **tự xuống hàng** (`flex-wrap`), không cố định một hàng |
| **X10** | Ô ký cuối lưới Chữ ký | Frame 6: dòng cuối là **hàng trống, checkbox đã tick**, không nhãn chức danh | `R-TLMI-193` "Thêm ô ký tự do — không giới hạn số ô ký" | Đó là ô ký tự do vừa thêm, chưa nhập. Kết hợp `R-TLMI-189`: đang bật + tiêu đề trống ⇒ **lỗi** `MSG_211`. Khớp luật, không cần hỏi |
| **X11** | Badge trạng thái ở frame 2/4/5/6 | Ba frame khác nhau hiện `Đã lưu` (xám), frame 1/1b hiện `Chưa lưu` (cam), frame 3 hiện `Có lỗi` (đỏ) | `R-TLMI-240/241/242` — đúng 3 trạng thái | Khớp. Xác nhận **màu**: xám / cam / đỏ (Figma là nguồn màu) |

**Nguyên tắc xử lý (theo skill `/plan-fe`):** **behavior theo Matrix/luật · UI theo Figma.**
Mọi dòng ⚠ ở trên đã đưa vào §12.

---

## §12. ⚠️ Điểm cần BA / Design xác nhận

| # | Câu hỏi | Bằng chứng phía A | Bằng chứng phía B | Chặn lô nào |
|---|---|---|---|---|
| **Q1** | Cấp mã `MSG_` cho: xung đột phiên bản khi Lưu · thiếu quyền In · 2 tooltip nút In disable | `04-quyet-dinh-ban-giao.md §7.1` (nợ BA) | `L-4`, `L-5` — đang mượn `MSG_COMMON_001/003` và key i18n cục bộ | không chặn; `msg.sh` báo `THIEU` |
| **Q2** | Xác nhận **C16** (không hoàn lại riêng một ô về theo chung) và **C17** (đổi Khổ/Hướng ở thanh xem trước = đổi mẫu) là **chủ ý** hay **sót đặc tả** | `R-TLMI-042` · `R-TLMI-044` · `SCR:79` *"đổi ở đây là đổi mẫu, không phải chỉ đổi cách xem"* | Figma frame 1 **không** có dấu hiệu nào cho người dùng biết ô đã hoá "riêng" (`R-TLMI-045` cấm thêm nhãn) | Lô 2, 3 — đã có phương án, chỉ cần xác nhận |
| **Q3** | **Thiết lập chung** lấy từ đâu ở bản này? Hình dạng `GET …/thiet-lap-chung` gồm những trường nào? | Q-03 làm "tầng tối thiểu" trên cấu hình tenant hiện có | §2.5: **không có** bảng/màn "thiết lập in chung"; `cfg_chi_nhanh` **không tồn tại** | **Lô 1** |
| **Q4** | Link `Mở Cấu hình báo cáo chứng từ` và `… › Thông tin trên bản in` trỏ đi đâu khi epic `_20` chưa có màn? | `R-TLMI-050` · `R-TLMI-051`; Figma frame 1 + 4 vẽ link đỏ | §2.5: `grep -i "cauHinhBaoCao"` ⇒ **0 kết quả** | Lô 3 — đề xuất: **ẩn link** khi chưa có màn, **không** để link chết |
| **Q5** | **Logo đơn vị** — BE bổ sung trường ở đâu, trả về dạng gì (URL / base64 / id)? | `R-TLMI-082` + chốt **C03**: Logo là 1 trong 7 ô tick; Figma frame 4 vẽ rõ, giá trị `[LOGO] cỡ vừa` | §2.5: `CompanyInfoResponse` **không có** trường logo | Lô 3 — FE vẫn vẽ được ô tick, chỉ thiếu ảnh thật |
| **Q6** | **Số chứng từ** in ở đâu? (X2) | `R-TLMI-091`: số chứng từ **không** thuộc khối Tiêu đề | Figma frame 0 in `Số: SO000123 · Ngày 27 tháng 08 năm 2026` ngay dưới tiêu đề | Lô 2 |
| **Q7** | Mẫu chuẩn hệ thống có **kèm sẵn khối tự do** không? (X5) | `R-TLMI-008`: mẫu chuẩn có **đúng bốn loại khối**, không khối nào khác | Figma frame 1-6 vẽ mẫu có `Thông tin chứng từ` và `Tổng hợp` là **khối tự do có nút ✕** | **Lô 1** — quyết định hình dạng mẫu chuẩn |
| **Q8** | Mẫu chuẩn có bật **mọi** khối Bảng không? (X6) | `R-TLMI-009`: "**mọi lưới bật**" | Figma frame 1-6: `Bảng thuế` mắt gạch chéo = **đang tắt** | Lô 1 |
| **Q9** | Bấm `In đậm` trên thanh công cụ với vùng chọn **trộn** ô-trường và ô-Chữ tự do thì ra gì? | `R-TLMI-156 §Ghi chú` ghi rõ tài liệu **không quy định** | — | Lô 4 — đề xuất: áp cho **mọi ô trong vùng**, theo đúng bản chất từng ô (`R-TLMI-158` cho ô-trường, `R-TLMI-159` cho ô-Chữ tự do) |
| **Q10** | `Đặt lại mẫu chuẩn` có phải **một bước Hoàn tác được** không? | `R-TLMI-224 §Ghi chú` ghi tài liệu **không nói** | `R-TLMI-018` "Đặt lại chỉ đổi trên màn, bấm Lưu mới có hiệu lực" ⇒ là một thay đổi như mọi thay đổi khác | Lô 2 — đề xuất: **CÓ**, một bước |
| **Q11** | Tên hai nút của hộp `MSG_404` (gộp ô) | `R-TLMI-138 §Ghi chú`: tài liệu **không nêu tên hai nút** | — | Lô 4 — đề xuất: `Tiếp tục` / `Huỷ` (khớp cách hỏi "…Tiếp tục?" của nội dung message) |
| **Q12** | Ba nút `MSG_401` **lệch BR3** (BR3 chỉ 2 nút) | `R-TLMI-251…254`: `Lưu và đóng` · `Không lưu` · `Ở lại` | BR3 (Phase 1 và Phase 2) quy định hộp xác nhận 2 nút | Lô 2 — **epic thắng trong phạm vi epic**; đã ghi lệch ở §14 |
| **Q13** | Chữ **in ra giấy** (`(Ký, họ tên)`, `Cộng`, `STT`, `Tổng:`) có đổi theo ngôn ngữ giao diện không? | A5 §3.6: bản cũ cố ý để cứng tiếng Việt vì "in ra giấy" | Luật 2 `CLAUDE.md`: **mọi chuỗi người dùng thấy** phải có khoá i18n ở cả `vi.ts` và `en.ts` | Lô 1 — đề xuất: **có khoá i18n**; `en.ts` giữ tiếng Việt cho nhãn chứng từ pháp lý, dịch cho nhãn giao diện |
| **Q14** | `Hiện lưới căn chỉnh` mặc định = **Có** (`R-TLMI-222`) nhưng Figma frame 1/1b vẽ ô tick **chưa tick** | `R-TLMI-222`: "mặc định = **Có**" | Figma frame 1, 1b: ô `Hiện lưới căn chỉnh` **trống**; frame 2, 3, 4, 5, 6: **đã tick** | Lô 2 — đề xuất: theo luật (**mặc định Có**); frame 1/1b là trạng thái người dùng vừa bỏ tick |

---

## §13. Kiểm thử + cổng nghiệm thu

### 13.1 Danh sách file test (13 file) — **mọi `it()` mang chính mã luật**

| File | Môi trường | Bao phủ |
|---|---|---|
| `test/luoiTuDo.test.ts` | `node` | `R-TLMI-123, 129…143, 148, 152…155, 180, 181` |
| `test/doRongCot.test.ts` | `node` | `R-TLMI-108…114, 118` (3 ca chốt BA + ca chạm sàn) |
| `test/keThua.test.ts` | `node` | `R-TLMI-036, 040…045, 049, 053, 077` |
| `test/kiemTraMau.test.ts` | `node` | `R-TLMI-230…239, 243` (đủ 17 dòng V01-V17) |
| `test/chuanHoaMau.test.ts` | `node` | `R-TLMI-018, 019` + chốt **C02** |
| `test/mauChuan.test.ts` | `node` | `R-TLMI-002, 003, 007…010, 013, 093, 167` |
| `test/truongDungChung.test.ts` | `node` | `R-TLMI-156…159, 164` |
| `test/mauInStore.test.ts` | `node` | `R-TLMI-041, 223…227` |
| `test/ThietLapMauInScreen.test.tsx` | DOM | `R-TLMI-240…245, 250…257` |
| `test/LuoiTuDo.test.tsx` | DOM | `R-TLMI-132, 144…151, 161, 173, 177…179, 235, 236` |
| `test/ThanhCongCuTuDo.test.tsx` | DOM | `R-TLMI-162, 163, 170…176` |
| `test/inspectors.test.tsx` | DOM | `R-TLMI-053…091, 094…107, 116, 117, 182…200` |
| `test/NutInChungTu.test.tsx` | DOM | `R-TLMI-023…033, 260, 261, 268, 269` |

Quy ước tên test (để `trace.sh` đếm được):
```ts
it('R-TLMI-114 · chia đều 40/40/40 thành 33/33/34', () => { … })
it('R-TLMI-037 · ô theo chung KHÔNG có mặt trong payload', () => { … })
```

Chi tiết từng ca (input → kỳ vọng) ở [`09-truy-vet-va-kiem-thu.md`](09-truy-vet-va-kiem-thu.md) §2.

### 13.2 Cổng nghiệm thu

**Cổng nhẹ — chạy mỗi lô:**
```bash
cd client && npx vitest run src/base/domainKit/mauIn --reporter=dot
cd client && npx vite build
```

**Cổng đầy đủ — trước khi báo hoàn thành:**
```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test && npm run build
git -C client status --porcelain      # thay cho check:committed (lỗi giả trên Windows — R9)
```

**Cổng truy vết — BẮT BUỘC trước khi báo xong `/gen-fe`:**
```bash
./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec fe
./docs/rules/msg.sh   pmkt-docs/ba/<PYC> fe     # ⚠ PYC nằm vùng đóng băng — xem Q1/L-5
```

⚠ `msg.sh` sẽ báo `THIEU` cho 5 chuỗi chưa có mã `MSG_` (L-4, L-5) — **đã ghi nhận, chấp nhận**.

⚠ **Không chạy Docker / Testcontainers** — FE không cần; dev server dùng lại cổng 5173 của user.

---

## §14. BR áp dụng

⚠ **Chức năng này chạy bộ BR Phase 2** (quyết định **Q-02** của user), **không** phải BR1…BR49 mà
`br.sh` đọc. `br.sh` **không** in được BR50/BR51.

| BR | Áp ở đâu |
|---|---|
| **BR50.6** (phạm vi dữ liệu theo chi nhánh) | `R-TLMI-004/005/035` — mẫu **không** khai `ChiNhanhId`; chốt **C26** xếp nhóm 1 (cấu hình hệ thống) |
| **BR50.7** (kho trường của form) | `R-TLMI-165/166` — kho trường = mọi ô form **trừ** cột trong các lưới, danh sách **phẳng**, không chia nhóm |
| **BR51.5** (một mẫu cho cả đơn vị) | `R-TLMI-001/005` |
| **BR51.6** (cộng gộp mặt hàng) | `R-TLMI-119/266` — **BE**, ngoài phạm vi FE |
| **BR3** (hộp xác nhận) | `MSG_402/403/404` dùng `CommonConfirmModal` 2 nút. ⚠ `MSG_401` **lệch BR3** — 3 nút (D11, Q12) |
| **BR7** (số liệu / tiền tệ) | `BanInPaper.tsx` định dạng số cột `Cộng` và giá trị tiền trên bản in |
| **BR8** (ngày tháng) | `R-TLMI-090` dòng `Ngày … tháng … năm …` dưới tiêu đề; `R-TLMI-197` dòng ngày của khối Chữ ký |
| **BR13** (form nhập liệu / popup) | mọi bảng chỉnh bên phải; `R-TLMI-230` kiểm **khi rời ô** |
| **BR14** (phím tắt / hành vi ô) | `R-TLMI-173` mũi tên · Delete · Enter/F2; `R-TLMI-250` Ctrl+S; `R-TLMI-227` Ctrl+Z / Ctrl+Y |
| **BR25** (quyền) | `R-TLMI-031…035`; BR25.2 **ẩn hẳn** không disable; `MSG_COMMON_003` cho thiếu quyền In |
| **BR26** (thông báo & cảnh báo) | BR26.1 toast góc phải trên cho `MSG_101/102/104`; `R-TLMI-238` **không có cảnh báo mềm** |
| **BR30** (ẩn trường không đổi rule) | chốt **C18** — khối **đang ẩn** thì bỏ qua validate của khối đó (`R-TLMI-207/208/209`) |
| **BR35** (giữ ngữ cảnh khi điều hướng) | `R-TLMI-029/030` — đóng màn quay lại **đúng nơi vừa mở ra**; quay lại xem trước thì **vẽ lại theo mẫu vừa lưu** |
| BR2 (danh mục dạng cây) · BR5/6/10 (combogrid) · BR21 (grid chi tiết con) | **Không áp dụng** — màn không có cây, không có combogrid, không có grid chi tiết con |

**BR chưa xử lý được / cố ý lệch:**

| BR | Vì sao |
|---|---|
| **BR3** (2 nút) | `MSG_401` cần **3 nút** — epic thắng trong phạm vi epic (D11, Q12). Đã ghi nhận ở `01-conflict.md` |
| **BR1…BR49 bản Phase 1** | Q-02: chức năng này chạy bộ BR **Phase 2**. Nếu dự án sau này quyết `_21` thuộc Phase 1 thì **phải soát lại 26 mục** (23 luật + 3 bất biến) đứng trên nền BR50/BR51 |
| **BR46** (trường hệ thống bắt buộc) | áp cho **bản ghi**, không áp cho từng nhánh JSON (Q-01) — việc của BE |
| **BR47** (danh mục dữ liệu mặc định) | không áp dụng — mẫu chuẩn **sinh từ đặc tả form**, không có entity riêng (`R-TLMI-006`) |

---

## §15. Tài liệu tham chiếu

| Loại | Đường dẫn |
|---|---|
| Đặc tả nguyên tử | `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/00-source-map.md` · `01-conflict.md` · `02-rules.md` · `03-scenarios.md` · `04-quyet-dinh-ban-giao.md` |
| Quy tắc gốc | `CLAUDE.md` · `client/CLAUDE.md` |
| Khung FE | `docs/rules/fe-khung-kien-truc-chuan.md` |
| Quy ước | `docs/rules/conventions-chung.md` · `docs/rules/conventions-fe.md` |
| Truy vết luật | `docs/rules/truy-vet-luat.md` — `trace.sh` · `msg.sh` |
| Module tham chiếu | `client/src/features/banHang/chungTuBanHang/` |
| Luật tầng ép bằng máy | `client/eslint.boundaries.js` |
| Ghi chú Figma (bản tạm phiên audit) | `scratchpad/extract/A0-figma.md` + 8 PNG ở `scratchpad/figma/` |
| Kiểm kê code hiện có (bản tạm) | `scratchpad/extract/A5-hien-trang-code.md` |
