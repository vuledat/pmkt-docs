# 01 · Modal Thiết lập mẫu in — khung màn, cột trái, thanh xem trước, chân màn

| | |
|---|---|
| Mã màn | `SCR_ThietLapMauIn` |
| Nguồn SCR | `SCR:18-81` · `SCR:201-253` · `SCR:306-337` |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` |
| Figma | frame **1** `71956:288872` · frame **1b** `72218:690704` · (bố cục chung ở cả 6 frame) |
| Route | **KHÔNG CÓ** — modal toàn màn (D1) |
| File chính | `@domain-kit/mauIn/pages/ThietLapMauInScreen.tsx` · `components/modal/ThietLapMauInModal.tsx` |
| Luật phủ | `R-TLMI-015…020` · `R-TLMI-201…216` · `R-TLMI-217…229` · `R-TLMI-240…257` |

---

## 1. Bố cục

```
┌──────────────────────────────────────────────────────────────────────────── 1420 ×1007 ───┐
│ Thiết lập mẫu in: {tên nghiệp vụ}   [badge]                                    (?)   (✕)  │ 52
├─────────────────┬─────────────────────────────────────────┬───────────────────────────────┤
│ BỐ CỤC MẪU      │ ↶ ↷ │Khổ giấy▾│Hướng giấy▾│☑ Hiện lưới  │  {Tên khối đang chọn}         │
│                 │       căn chỉnh │ − 70% + │ Vừa khung │                                 │
│ ⚙ Thiết lập mẫu │─────────────────────────────────────────│  (bảng chỉnh đổi theo khối)   │
│ ⠿👁 Thông tin…  │                                         │                               │
│ ⠿👁 Tiêu đề     │        ┌───────────────────────┐        │                               │
│ ⠿👁 Thông tin…✕ │        │                       │        │                               │
│ ⠿👁 Bảng hàng…  │        │     TRANG GIẤY        │        │                               │
│ ⠿👁̶ Bảng thuế   │        │   (nền trắng, bóng)   │        │                               │
│ ⠿👁 Tổng hợp  ✕ │        │                       │        │                               │
│ ⠿👁 Chữ ký      │        └───────────────────────┘        │                               │
│ ⠿👁 Ghi chú…  ✕ │                                         │                               │
│ ┌─────────────┐ │                                         │                               │
│ │+ Thêm khối  │ │                                         │                               │
│ │  tự do      │ │                                         │                               │
│ └─────────────┘ │                                         │                               │
│ • Mẫu chuẩn…    │                                         │                               │
│ • Có thể thao…  │                                         │                               │
├─────────────────┴─────────────────────────────────────────┴───────────────────────────────┤
│ [Đóng]                                           [Đặt lại mẫu chuẩn]  [Lưu]                │ 56
└────────────────────────────────────────────────────────────────────────────────────────────┘
      280 px                     co giãn                            ~390 px
```

Số đo lấy từ Figma frame 1 (viewport 1440×1024, modal 1420×1007, header 52, thân 899, chân ~56).

---

## 2. Đặc tả UI từ Figma

| Thành phần | Component `@base` | Số đo / trạng thái | Luật |
|---|---|---|---|
| Vỏ modal | `CommonModalShell` (`base/index.ts:355`) | toàn màn 1420×1007; đóng bằng `✕` hoặc `Esc` | `R-TLMI-251` · `R-TLMI-256` |
| Header | `CommonModalHeader` (`base/index.ts:377`) | cao **52**; tiêu đề `Thiết lập mẫu in: {tên nghiệp vụ}`; badge **cạnh tiêu đề**; bên phải icon `?` và `✕` | `R-TLMI-245` |
| Badge trạng thái | **mới** `BadgeTrangThai.tsx` | `Chưa lưu` cam · `Đã lưu` xám · `Có lỗi` đỏ | `R-TLMI-240/241/242` |
| Cột trái | **mới** `BoCucMauPane.tsx` | **280 px**, tiêu đề `BỐ CỤC MẪU` chữ nhỏ hoa | `R-TLMI-201` |
| Dòng "Thiết lập mẫu" | **mới** `BoCucMauPane.tsx` | icon bánh răng; **không** handle kéo, **không** mắt, **không** `✕`; là mục **đầu** danh sách | `R-TLMI-202` |
| Dòng khối | **mới** `DongKhoiBoCuc.tsx` | `⠿` · `👁` · tên · `●` đỏ nếu lỗi · `✕` nếu xoá được | `R-TLMI-203` · `R-TLMI-232` |
| Dòng đang chọn | CSS | nền hồng nhạt + vạch đỏ bên trái | `R-TLMI-213` |
| Nút thêm khối | `CommonButton` (`base/index.ts:124`) | viền **đứt**, chữ **đỏ**, nguyên văn `+ Thêm khối tự do` | `R-TLMI-120` |
| Chú thích cuối cột | **mới** `ChuThichBoCuc.tsx` | 2 gạch đầu dòng, chữ xám nhỏ | — |
| Thanh xem trước | **mới** `ThanhXemTruoc.tsx` | một hàng, **tự xuống hàng** khi hẹp (X9) | `R-TLMI-228` |
| Cột giữa | **mới** `XemTruocPane.tsx` | co giãn; nền xám nhạt; cuộn dọc | `R-TLMI-217` |
| Trang giấy | **mới** `BanInPaper.tsx` | nền trắng, bóng đổ; khối đang chọn viền **đỏ nét đứt**; khối khác viền **xám nét đứt** khi bật lưới căn chỉnh | `R-TLMI-177` |
| Cột phải | **mới** `inspector/InspectorPane.tsx` (giữ khung cũ `inspector/InspectorPane.tsx:1-76`) | **~390 px**; tiêu đề = tên khối đang chọn; khối tự do có badge `khối tự do` | `R-TLMI-216` |
| Chân màn | `CommonModalFooter` (`base/index.ts:367`) | cao ~56; `Đóng` **trái**; `Đặt lại mẫu chuẩn` + `Lưu` (nút đỏ chính) **phải** | `R-TLMI-257` |

---

## 3. Cột trái — *Bố cục mẫu*

### 3.1 Danh sách mục

| # | Mục | Kéo được | Mắt | Xoá được | Luật |
|---|---|---|---|---|---|
| 0 | `Thiết lập mẫu` (⚙) | ❌ | ❌ | ❌ | `R-TLMI-202` |
| 1..n | `Thông tin đầu trang` · `Tiêu đề` · `{Tên bảng}` (n khối) · `Chữ ký` | ✔ | ✔ | ❌ | `R-TLMI-206` · `R-TLMI-210` · `R-TLMI-212` |
| 1..n | khối tự do (`Thông tin chứng từ`, `Tổng hợp`, `Ghi chú giao hàng`…) | ✔ | ✔ | ✔ `✕` | `R-TLMI-211` |

⚠ **X5 / Q7** — Figma vẽ `Thông tin chứng từ` và `Tổng hợp` là **khối tự do có `✕`**, nhưng `R-TLMI-008`
nói mẫu chuẩn chỉ có **bốn loại khối**. Chờ BA.

⚠ **Tên khối chuẩn CỐ ĐỊNH** (`R-TLMI-212`) — không cho sửa. Khối tự do sửa tên được ở **cả hai chỗ**
(hộp `Đặt tên khối` khi thêm + ô `Tên khối` trên bảng chỉnh — chốt **C07**, `R-TLMI-127`).

### 3.2 Ma trận ẩn / hiện · disable (dịch từ luật, nguồn `MT`)

| Thành phần | Thiết lập mẫu | Đầu trang | Tiêu đề | Bảng | Khối tự do | Chữ ký | Luật |
|---|---|---|---|---|---|---|---|
| Cột trái *Bố cục mẫu* | Show | Show | Show | Show | Show | Show | `R-TLMI-201` |
| Thanh *Xem trước* (Khổ · Hướng · lưới · zoom · Vừa khung) | **Show** | **Show** | **Show** | **Show** | **Show** | **Show** | `R-TLMI-228` |
| Thanh công cụ khối tự do | Hide | Hide | Hide | Hide | **Show** `(đk-NG)` | Hide | `R-TLMI-170` |
| Menu chuột phải trên ô | Hide | Hide | Hide | Hide | **Show** | Hide | `R-TLMI-170/171` |
| Bảng chỉnh bên phải | *Thiết lập mẫu* | *Thông tin đầu trang* | *Tiêu đề bản in* | *{Tên bảng}* | *{Tên khối}* + badge | *Chữ ký* | `R-TLMI-216` |
| Nút `−  Dòng` / `− Cột` | — | — | — | — | **Disable** khi còn 1 dòng / 1 cột | — | `R-TLMI-135` |
| Nút `Gộp ô` | — | — | — | — | **Disable** khi vùng < 2 ô | — | `R-TLMI-174` · X7 |
| Nút `Tách ô` | — | — | — | — | **Disable** khi ô đang chọn không phải ô gộp | — | `R-TLMI-174` · X7 |
| Mọi nút thanh công cụ | — | — | — | — | **Disable** khi **chưa chọn ô nào** | — | `R-TLMI-162` |
| Nút `↶` Hoàn tác | **Disable** khi hết bước | như trái | | | | | `R-TLMI-226` |
| Nút `↷` Làm lại | **Disable** khi hết bước | như trái | | | | | `R-TLMI-226` |
| Nút `Lưu` | **Disable** khi trạng thái = `Đã lưu`; **bấm được** khi `Có lỗi` | | | | | | `R-TLMI-240` · `R-TLMI-243` |

`(đk-NG)` = điều kiện phụ theo vùng chọn / sàn lưới.

### 3.3 Hành vi

| Thao tác | Việc làm | Luật |
|---|---|---|
| Bấm một dòng khối | bảng chỉnh bên phải mở **đúng khối đó**; **chỉ** bảng chỉnh đổi, cột trái và trang xem trước giữ nguyên | `R-TLMI-213` · `R-TLMI-216` |
| Bấm một khối **trên trang xem trước** | như trên | `R-TLMI-214` |
| Rê chuột lên một khối trên trang | hiện **nhãn tên khối** nổi (đỏ) ở góc khối | `R-TLMI-215` |
| Kéo `⠿` của dòng khối | đổi thứ tự khối trong mẫu | `R-TLMI-204` |
| Kéo khối **trên trang xem trước** | cùng kết quả với kéo `⠿` | `R-TLMI-205` |
| Bấm `👁` | bật/tắt in khối. Tắt ⇒ **không in**, các khối sau **dồn lên**, nhưng **không mất thiết lập bên trong** | `R-TLMI-207/208/209` |
| Bấm `✕` trên dòng khối tự do | hỏi `MSG_403` trước | `R-TLMI-175` · `R-TLMI-211` |
| Bấm `+ Thêm khối tự do` | mở hộp `Đặt tên khối` (`MSG_206` nếu trống/quá 60); tạo lưới **1×2** toàn ô trống, đặt **ngay trước Chữ ký**, mở bảng chỉnh, **chọn sẵn ô đầu tiên**, toast `MSG_104` | `R-TLMI-120…124` |
| Bấm `+ Thêm khối tự do` khi đã đủ 10 | chặn, báo `MSG_207` | `R-TLMI-125` |
| Rê chuột lên dòng khối **đang lỗi** | hiện **nội dung lỗi** (tooltip) | `R-TLMI-233` |

⚠ **Khối đang ẩn thì bỏ qua validate của khối đó** (chốt **C18**); bật lại ⇒ validate lại ngay.
⚠ **Tên khối tự do KHÔNG in ra bản in** (`R-TLMI-126`) — chỉ dùng để nhận diện trên màn.

---

## 4. Thanh *Xem trước* (cột giữa, hàng trên)

| Điều khiển | Nguyên văn nhãn | Hành vi | Luật |
|---|---|---|---|
| `↶` | tooltip `Hoàn tác` | lùi một bước chỉnh, áp cho **toàn mẫu**; mờ khi hết bước | `R-TLMI-223` · `R-TLMI-226` |
| `↷` | tooltip `Làm lại` | tiến một bước; mờ khi hết bước | như trên |
| `Khổ giấy` | `Khổ giấy` | select `A3` / `A4` / `A5`; **đổi ở đây là đổi MẪU**, ô hoá **riêng** | `R-TLMI-044` · `R-TLMI-054` |
| `Hướng giấy` | `Hướng giấy` | select `Dọc` / `Ngang` / `Tự động`; như trên | `R-TLMI-044` · `R-TLMI-055` |
| ô tick | `Hiện lưới căn chỉnh` | **chỉ trên màn, KHÔNG lưu**, mặc định **Có** (⚠ Q14) | `R-TLMI-222` · `R-TLMI-177…179` |
| `−` `70%` `+` | — | thu / phóng, **không** ảnh hưởng bản in | `R-TLMI-221` |
| `Vừa khung` | `Vừa khung` | mức mặc định **khi mở màn** | `R-TLMI-221` |

**Hai ô Khổ / Hướng ở đây và ở panel *Thiết lập mẫu* là MỘT trường** — đồng bộ hai chiều tức thời
(chốt **C17**). Thanh này **luôn hiện ở mọi khối đang chọn** (`R-TLMI-228`).

**Lưới căn chỉnh khi bật:** mọi khối viền **xám nét đứt**, khối đang chọn viền **đỏ nét đứt**; ô trong
khối tự do cũng kẻ đứt. Dấu hiệu này **không in và không xuất PDF** (`R-TLMI-178`) ⇒ ẩn bằng
`@media print`, **không** bằng nhánh JS (D13). Bỏ tick ⇒ dấu hiệu biến mất, vùng chọn và thao tác **vẫn
dùng được** (`R-TLMI-179`).

---

## 5. Hoàn tác / Làm lại

| Luật | Nội dung | Hiện thực |
|---|---|---|
| `R-TLMI-223` | nhớ tối đa **60 bước** trong phiên đang mở | `zundo` `limit: 60` |
| `R-TLMI-224` | mỗi thao tác đổi mẫu là **một bước**, kể cả thêm/xoá dòng cột và gộp/tách ô; **gõ chữ trong một ô tính một bước khi rời ô**; bấm `Theo thiết lập chung` cũng là một bước | `handleSet` chốt checkpoint **khi blur**, không theo thời gian |
| `R-TLMI-225` | đóng màn ⇒ lịch sử **bị xoá** | Provider unmount ⇒ store biến mất (D4) |
| `R-TLMI-226` | hết bước ⇒ nút tương ứng **mờ** | `useStore(store.temporal, s => s.pastStates.length)` |
| `R-TLMI-227` | `Ctrl+Z` / `Ctrl+Y` tương đương | listener ở `ThietLapMauInScreen`, **tắt** khi đang mở hộp thoại con (`R-TLMI-256`) |
| `R-TLMI-041` | `Theo thiết lập chung` là một bước Hoàn tác được | nút gọi một action store duy nhất |
| ⚠ **Q10** | `Đặt lại mẫu chuẩn` có là một bước không? | tài liệu không nói — đề xuất **CÓ** |

**Không vào lịch sử:** chọn khối · chọn ô / vùng · zoom · `Hiện lưới căn chỉnh` · ô `Tìm cột` ·
ô `Tìm kiếm` kho trường. Thực hiện bằng `partialize: s => ({ mau: s.mau })`.

---

## 6. Chân màn — Đóng · Đặt lại mẫu chuẩn · Lưu

### 6.1 `Lưu`

```
bấm Lưu (hoặc Ctrl+S — R-TLMI-250)
 ├─ trạng thái = Đã lưu       → nút đang mờ, không xảy ra
 ├─ trạng thái = Có lỗi       → KHÔNG ghi
 │                              • báo lỗi ĐẦU TIÊN (thứ tự C21)
 │                              • mở bảng chỉnh của khối đó
 │                              • đưa con trỏ vào ô lỗi
 │                                (ô lưới ⇒ chọn ô đó trên trang xem trước)
 └─ trạng thái = Chưa lưu     → chạy chiaDeuVe100 cho mọi khối Bảng (R-TLMI-111)
                                → chuanHoaMau() xoá khoá undefined (D5)
                                → PUT …/mau-in
                                   ├─ 200  → toast MSG_101, badge → Đã lưu, màn GIỮ NGUYÊN
                                   ├─ 409  → MSG_COMMON_001 + hỏi nạp lại (C06, L-4)
                                   ├─ 403  → MSG_PMKT-E-14549_21_002
                                   └─ 5xx  → MSG_PMKT-E-14549_21_003, rollback phía BE
```

`R-TLMI-248`: Lưu thành công thì **báo, màn giữ nguyên** (không đóng).
`R-TLMI-247` / `R-TLMI-249`: transaction và rollback là việc **BE**; FE chỉ hiện lỗi trả về.

### 6.2 `Đặt lại mẫu chuẩn`

| Bước | Việc làm | Luật |
|---|---|---|
| 1 | hỏi `MSG_402` trước (`CommonConfirmModal`) | `R-TLMI-015` |
| 2 | không đồng ý ⇒ **giữ nguyên** mẫu đang chỉnh | `R-TLMI-020` |
| 3 | đồng ý ⇒ nạp lại **toàn bộ** mẫu chuẩn hệ thống | `R-TLMI-016` |
| 4 | toast `MSG_102`, badge → **Chưa lưu** | `R-TLMI-017` |
| 5 | **chỉ đổi trên màn** — chưa Lưu thì mẫu cũ trên server còn nguyên | `R-TLMI-018` · `R-TLMI-019` |

### 6.3 `Đóng` / `Esc`

```
bấm Đóng (hoặc Esc — R-TLMI-251)
 ├─ đang mở hộp thoại con      → Esc KHÔNG tác dụng với màn chính   (R-TLMI-256)
 ├─ không có thay đổi          → đóng NGAY, không hỏi                (R-TLMI-255)
 └─ có thay đổi chưa lưu       → MSG_401 với BA nút (D11):
      ├─ Lưu và đóng  → chạy nhánh Lưu; thành công ⇒ toast MSG_101 (C23) rồi đóng  (R-TLMI-252)
      ├─ Không lưu    → bỏ mọi thay đổi, đóng                                      (R-TLMI-253)
      └─ Ở lại        → đóng hộp, giữ nguyên màn                                   (R-TLMI-254)
```

Đóng xong ⇒ quay lại **đúng nơi vừa mở ra** (`R-TLMI-029`):
- vào từ **menu In trên form** ⇒ về form chứng từ;
- vào từ nút **Sửa mẫu** trên màn Xem trước ⇒ về màn Xem trước, và bản in **vẽ lại theo mẫu vừa lưu**
  (`R-TLMI-030`).

---

## 7. Validation phía FE (bảng 17 dòng — `R-TLMI-239`)

Đầy đủ ở [`08-hop-dong-api-va-i18n.md §4`](08-hop-dong-api-va-i18n.md); phần thuộc màn này:

| # | Trường | Điều kiện | Message | Thời điểm | Luật |
|---|---|---|---|---|---|
| V17 | Quyền Thiết lập mẫu in | có quyền | `MSG_002` | **Server** khi mở màn và khi Lưu | `R-TLMI-034` |

**Luật chỉ BE kiểm, FE chỉ hiển thị lỗi trả về:** V16 (cỡ chữ 8-20 — ô chọn từ danh sách nên FE không
nhập sai được), V17 (quyền), xung đột phiên bản (C06).

**Đánh dấu lỗi** (`R-TLMI-231…235`):
- ô không hợp lệ: viền đỏ **tại chỗ** + chữ lỗi đỏ nghiêng ngay dưới ô;
- khối chứa ô lỗi: **chấm đỏ ở dòng khối** (cột trái) **và** viền đỏ khối trên trang xem trước;
- rê chuột lên dòng khối / khối đang lỗi ⇒ hiện **nội dung lỗi**;
- sửa đúng ⇒ mọi dấu hiệu **tắt ngay** (`R-TLMI-234`);
- ô lưới khối tự do không hợp lệ ⇒ **viền đỏ ngay trên trang xem trước** (`R-TLMI-235`), chữ đỏ nghiêng
  nguyên văn (Figma frame 3): `Ô: Chữ tự do chưa có nội dung — nháy đúp để gõ`;
- **không có cảnh báo mềm** (`R-TLMI-238`) — chỉ có lỗi hoặc không lỗi.

---

## 8. Luồng xử lý — mở màn

```
1. Host (form chứng từ) render <NutInChungTu maLoaiChungTu maNghiepVu chungTuId …/>
2. Người dùng chọn "Thiết lập mẫu in…"  →  setMoThietLap(true)
3. <ThietLapMauInModal> mount
   3.1 useMauHieuLuc(maLoaiChungTu, maNghiepVu)   → GET  (mẫu + mẫu chuẩn + chung + kho trường + phiên bản)
   3.2 useDuLieuIn(chungTuId)                     → GET  (dữ liệu THẬT của chứng từ đang mở — R-TLMI-217)
   3.3 loading  → skeleton 3 cột
       lỗi      → toast MSG_003 + đóng modal
       403      → toast MSG_002 + đóng modal
   3.4 dựng store: napMau(mau ?? mauChuan), chung, khoTruong, goc = mau
       chưa có bản ghi ⇒ mẫu chuẩn hệ thống (R-TLMI-007), badge = "Đã lưu" (R-TLMI-240)
4. <ThietLapMauInScreen> render: header + BoCucMauPane + XemTruocPane + InspectorPane + footer
   toàn bộ bọc trong MỘT <DndContext> (D8)
5. Mọi thay đổi → store → BanInPaper vẽ lại NGAY (R-TLMI-218)
```

**Invalidate query khi Lưu thành công:** `mauInKeys.hieuLuc(maLoaiChungTu, maNghiepVu)` ⇒ mọi lần in
`Mẫu tùy chỉnh` sau đó dùng mẫu mới **ngay** (`R-TLMI-022`).

---

## 9. Phân bổ file

| Việc | File |
|---|---|
| Vỏ modal + Provider + nạp dữ liệu | `components/modal/ThietLapMauInModal.tsx` |
| Ráp header + 3 cột + chân + `DndContext` | `pages/ThietLapMauInScreen.tsx` |
| CSS 3 cột, trang giấy, lưới căn chỉnh, `@media print` | `pages/mauIn.css` |
| Cột trái | `components/BoCucMauPane.tsx` · `DongKhoiBoCuc.tsx` · `ChuThichBoCuc.tsx` |
| Thanh xem trước | `components/ThanhXemTruoc.tsx` |
| Khung cuộn + zoom | `components/XemTruocPane.tsx` |
| Renderer giấy | `components/BanInPaper.tsx` |
| Badge | `components/BadgeTrangThai.tsx` |
| Bộ chuyển bảng chỉnh | `components/inspector/InspectorPane.tsx` |
| Store + undo | `hooks/mauInStore.ts` · `MauInStoreProvider.tsx` · `useMauInStore.ts` |
| Lưu / Ctrl+S / 409 | `hooks/useLuuMau.ts` |
| Đóng / Esc / MSG_401 | `hooks/useDongMan.ts` |
| Đặt lại mẫu chuẩn | `hooks/useDatLaiMauChuan.ts` |
| Sắp xếp / ẩn hiện / xoá khối | `helpers/thaoTacKhoi.ts` |
| Kiểm tra + thứ tự lỗi đầu tiên | `helpers/kiemTraMau.ts` |
| Chuẩn hoá trước khi Lưu | `helpers/chuanHoaMau.ts` |
| 4 hộp xác nhận | `components/modal/HopThayDoiChuaLuuModal.tsx` · `XacNhanDatLaiModal.tsx` · `XacNhanXoaKhoiModal.tsx` · `XacNhanGopOModal.tsx` |

---

## 10. Kiểm thử

### `test/mauInStore.test.ts` (`node`)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-223 · nhớ tối đa 60 bước` | 61 thao tác đổi mẫu → `pastStates.length === 60`; undo 60 lần về trạng thái thứ 2, nút mờ ở lần 61 |
| `R-TLMI-224 · gõ chữ trong một ô = một bước khi rời ô` | gõ `a`,`ab`,`abc` rồi blur → đúng **1** bước |
| `R-TLMI-224 · thêm dòng là một bước` | `themDong()` → `pastStates.length` +1 |
| `R-TLMI-225 · đóng màn xoá lịch sử` | unmount Provider → store mới có `pastStates.length === 0` |
| `R-TLMI-226 · hết bước thì nút mờ` | store mới → `canUndo === false`, `canRedo === false` |
| `R-TLMI-041 · Theo thiết lập chung là một bước` | `veTheoChung(['giayVaChu'])` → +1 bước, undo khôi phục đúng giá trị riêng cũ |
| `R-TLMI-223 · chọn khối / zoom KHÔNG vào lịch sử` | `chonKhoi()`, `datZoom()` → `pastStates.length` không đổi |

### `test/chuanHoaMau.test.ts` (`node`)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-037 · ô theo chung KHÔNG có mặt trong payload` | mẫu có `trang.khoGiay === undefined` → `JSON.stringify(chuanHoa(mau))` **không chứa** khoá `khoGiay` |
| `C02 · mẫu bằng mẫu chuẩn thì chuẩn hoá ra chuỗi bằng nhau` | mở mẫu chuẩn, không sửa gì → `chuanHoa(mau) === chuanHoa(mauChuan)` |
| `C02 · bỏ id kỹ thuật` | hai mẫu khác `id` khối nhưng cùng nội dung → chuẩn hoá bằng nhau |
| `R-TLMI-164 · trường chưa đặt vào ô nào thì không lưu` | `truongDungChung` có `k='soTien'` nhưng không ô nào dùng → payload **không** có `soTien` |

### `test/ThietLapMauInScreen.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-240 · Đã lưu thì nút Lưu mờ` | store `mau === goc` → badge `Đã lưu`, nút `Lưu` `disabled` |
| `R-TLMI-241 · có thay đổi hợp lệ thì badge Chưa lưu` | sửa tiêu đề → badge `Chưa lưu`, nút `Lưu` **bấm được** |
| `R-TLMI-242 · còn ô lỗi thì badge Có lỗi` | xoá trống tiêu đề → badge `Có lỗi` |
| `R-TLMI-243 · Có lỗi mà bấm Lưu thì KHÔNG mờ nút và KHÔNG ghi` | badge `Có lỗi` → nút `Lưu` **không** `disabled`; bấm → API **không** được gọi, hiện `MSG_201` |
| `R-TLMI-243 · chỉ báo lỗi ĐẦU TIÊN` | 3 ô lỗi ở 3 khối → chỉ một message, của khối đứng trước nhất trong Bố cục mẫu |
| `R-TLMI-244 · mở khối và đưa con trỏ vào ô lỗi` | bấm Lưu khi lỗi ở khối Bảng → bảng chỉnh chuyển sang khối đó, ô lỗi có `document.activeElement` |
| `R-TLMI-245 · tiêu đề màn và vị trí badge` | render → tiêu đề `Thiết lập mẫu in: Chứng từ bán hàng`, badge nằm trong header |
| `R-TLMI-250 · Ctrl+S tương đương Lưu` | `keyDown ctrl+s` → gọi đúng hàm Lưu |
| `R-TLMI-251 · Đóng khi có thay đổi thì hỏi` | sửa rồi bấm `Đóng` → hiện `MSG_401` |
| `R-TLMI-251 · MSG_401 có ĐÚNG BA nút` | → 3 nút `Lưu và đóng` · `Không lưu` · `Ở lại` |
| `R-TLMI-252 · Lưu và đóng vẫn hiện MSG_101` | chọn `Lưu và đóng` → toast `MSG_101` **rồi** modal đóng |
| `R-TLMI-253 · Không lưu thì bỏ thay đổi` | chọn `Không lưu` → API **không** gọi, modal đóng |
| `R-TLMI-254 · Ở lại thì giữ nguyên` | chọn `Ở lại` → modal **không** đóng, thay đổi còn |
| `R-TLMI-255 · không có thay đổi thì đóng ngay` | bấm `Đóng` khi `Đã lưu` → **không** hiện `MSG_401` |
| `R-TLMI-256 · Esc không tác dụng khi đang mở hộp con` | mở `MSG_402` rồi `Esc` → chỉ hộp con đóng, modal chính còn |
| `R-TLMI-257 · vị trí ba nút chân màn` | → `Đóng` trái, `Đặt lại mẫu chuẩn` + `Lưu` phải |
| `R-TLMI-015/016/017 · Đặt lại mẫu chuẩn` | bấm → `MSG_402`; đồng ý → mẫu = mẫu chuẩn, toast `MSG_102`, badge `Chưa lưu` |
| `R-TLMI-020 · không đồng ý thì giữ nguyên` | bấm `Huỷ` trên `MSG_402` → mẫu không đổi |

### `test/BoCucMauPane.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-202 · mục đầu là Thiết lập mẫu, không kéo được` | render → dòng đầu `Thiết lập mẫu`, **không** có handle `⠿`, **không** có `👁`, **không** có `✕` |
| `R-TLMI-203 · dòng khối có đúng ba thành phần` | → mỗi dòng khối có `⠿`, `👁`, tên |
| `R-TLMI-207/208 · tắt mắt thì khối không in` | bấm `👁` → `BanInPaper` không render khối đó; khối sau dồn lên |
| `R-TLMI-209 · tắt mắt không mất thiết lập` | tắt rồi bật lại → thiết lập bên trong nguyên vẹn |
| `R-TLMI-210 · khối chuẩn không có nút xoá` | → 4 khối chuẩn không có `✕` |
| `R-TLMI-211 · khối tự do có nút xoá ở cả hai nơi` | → dòng khối có `✕`, bảng chỉnh có link `Xóa khối này` |
| `R-TLMI-212 · tên khối chuẩn cố định` | → không có ô nhập tên ở 4 khối chuẩn |
| `R-TLMI-213 · bấm dòng khối thì bảng chỉnh đổi` | bấm `Tiêu đề` → bảng chỉnh hiện `Tiêu đề bản in` |
| `R-TLMI-232 · khối lỗi có chấm đỏ ở dòng khối` | tạo lỗi → dòng khối hiện `●` đỏ |
| `R-TLMI-125 · đủ 10 khối tự do thì chặn` | 10 khối → bấm `+ Thêm khối tự do` hiện `MSG_207` |

### `test/ThanhXemTruoc.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-221 · zoom không ảnh hưởng bản in` | đổi zoom → `mau` **không** đổi, `pastStates` không tăng |
| `R-TLMI-221 · mặc định mở màn là Vừa khung` | mount → zoom = giá trị `vừa khung` |
| `R-TLMI-222 · Hiện lưới căn chỉnh không lưu, mặc định Có` | mount → ô tick **đã tick**; bỏ tick → `mau` không đổi |
| `R-TLMI-228 · thanh luôn hiện ở mọi khối` | chọn lần lượt 6 mục → thanh vẫn render |
| `R-TLMI-044 · đổi Khổ giấy ở thanh làm ô hoá riêng` | mẫu đang theo chung → đổi `A4`→`A5` → `mau.trang.khoGiay === 'A5'` (khoá **xuất hiện**) |
| `R-TLMI-179 · bỏ tick lưới vẫn thao tác được` | bỏ tick → click ô lưới vẫn chọn được ô |

---

## 11. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR3 | `MSG_402`/`403`/`404` dùng `CommonConfirmModal` 2 nút. ⚠ `MSG_401` **lệch BR3** (3 nút — D11, Q12) |
| BR13 | mọi ô của bảng chỉnh; kiểm **khi rời ô** (`R-TLMI-230`) |
| BR14 | `Ctrl+S`, `Ctrl+Z`, `Ctrl+Y`, `Esc` |
| BR25 | quyền mở màn / lưu; ẩn hẳn không disable |
| BR26.1 | toast `MSG_101` / `MSG_102` / `MSG_104` góc phải trên |
| BR30 | chốt **C18** — khối đang ẩn thì bỏ qua validate của khối đó |
| BR35 | `R-TLMI-029/030` — đóng màn quay lại đúng nơi vừa mở ra |
