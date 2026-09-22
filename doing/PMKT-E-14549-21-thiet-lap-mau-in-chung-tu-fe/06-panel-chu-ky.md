# 06 · Bảng chỉnh *Chữ ký*

| | |
|---|---|
| Mã màn | `SCR_ThietLapMauIn` — mục `Chữ ký` của cột phải |
| Nguồn SCR | `SCR:201-215` · `SCR:293-300` |
| UC | `PMKT-U-14549_21-01_ThietLapMauIn` |
| Figma | frame **6** `72163:28110` |
| File chính | `components/inspector/ChuKyInspector.tsx` · `OKyRow.tsx` |
| Luật phủ | `R-TLMI-182…200` (nhóm K) · `R-TLMI-046` · `R-TLMI-052` |

---

## 1. Bố cục (Figma frame 6)

```
Chữ ký
─────────────────────────────────────────────────────────────
┌──┬─┬──────────────────┬─────────────────┬────────────────┬─┐
│⠿ │☑│ Chức danh        │ Tiêu đề in ra   │ Dòng ghi chú   │ │
├──┼─┼──────────────────┼─────────────────┼────────────────┼─┤
│⠿ │☑│ Người lập phiếu  │[Người lập phiếu]│[(Ký, họ tên)  ]│ │
│  │ │ Nguyễn Văn An    │                 │                │ │  ← tên người ký, chữ MỜ
│⠿ │☑│ Kế toán trưởng   │[Kế toán trưởng ]│[(Ký, họ tên)  ]│ │
│  │ │ Lưu Đức Huy      │                 │                │ │
│⠿ │☑│ Giám đốc         │[Giám đốc      ]│[(Ký, họ tên, đón…]│ │
│  │ │ Lê Quang Dũng    │                 │                │ │
│⠿ │☐│ Thủ kho          │[Thủ kho       ]│[(Ký, họ tên)  ]│ │  ← TẮT sẵn
│  │ │ Phạm Văn Kho     │                 │                │ │
│⠿ │☑│ [tự do]          │[Thủ quỹ       ]│[(Ký, họ tên)  ]│✕│  ← ô ký TỰ DO
│  │ │ Thủ quỹ          │                 │                │ │
│⠿ │☑│ [            ]   │[              ] │[              ]│✕│  ← ô ký tự do MỚI, chưa nhập
└──┴─┴──────────────────┴─────────────────┴────────────────┴─┘
[+ Thêm ô ký tự do]   VD: "Người nhận hàng", "Bên thuê"
☑ Dòng "Ngày … tháng … năm …" phía trên
Chỗ trống ký
[ Vừa                ▾ ]
┌───────────────────────────────────────────────────────────┐
│ Tên người ký in ra hay không theo cờ "In tên người ký" ở  │
│ Thiết lập người ký (đang: Có). Đổi chức danh, tên người   │
│ ký tại đó.                                                │
└───────────────────────────────────────────────────────────┘
Thiết lập người ký                                            ← link ĐỎ
```

⚠ **X10** — dòng cuối của lưới trong Figma là **ô ký tự do vừa thêm, chưa nhập**, checkbox đã tick.
Kết hợp `R-TLMI-189`: đang bật + `Tiêu đề in ra` trống ⇒ **lỗi** `MSG_211`. Khớp luật, không cần hỏi.

---

## 2. Đặc tả UI

| Thành phần | Component | Ghi chú | Luật |
|---|---|---|---|
| Lưới ô ký | **mới** `OKyRow.tsx` trong `SortableList` (`components/SortableList.tsx`) | 6 cột: `⠿` · ☑ · `Chức danh` · `Tiêu đề in ra` · `Dòng ghi chú` · `✕` | `R-TLMI-182…192` |
| Cột `Chức danh` | text 2 dòng | chức danh + **tên người ký in MỜ bên dưới** | `R-TLMI-185` · `R-TLMI-186` |
| Badge `tự do` | tag nhỏ | thay cho tên chức danh ở ô ký tự do | `R-TLMI-185` |
| `Tiêu đề in ra` | `CommonInput` (`base/index.ts:251`) | **bắt buộc** với ô đang bật, ≤ 60 ký tự | `R-TLMI-188` · `R-TLMI-189` |
| `Dòng ghi chú` | `CommonInput` | mặc định `(Ký, họ tên)`; Giám đốc `(Ký, họ tên, đóng dấu)` | `R-TLMI-190` |
| `✕` | icon button | **CHỈ ô ký tự do** | `R-TLMI-192` |
| `+ Thêm ô ký tự do` | `CommonButton` | viền đứt, chữ đỏ; gợi ý nguyên văn `VD: "Người nhận hàng", "Bên thuê"` | `R-TLMI-193` |
| Ô tick dòng ngày | `CommonCheckbox` (`base/index.ts:255`) | nguyên văn `Dòng "Ngày … tháng … năm …" phía trên` | `R-TLMI-197` |
| `Chỗ trống ký` | `CommonSelect` (`base/index.ts:691`) | `Thấp` · `Vừa` · `Cao` | `R-TLMI-198` |
| Hộp ghi chú | box chữ mờ | nguyên văn, có tham số `{coInTen}` | `R-TLMI-196` |
| Link `Thiết lập người ký` | `CommonButton` variant link | **có đích thật** | `R-TLMI-052` |

---

## 3. Danh sách ô ký (`R-TLMI-182`)

**5 chức danh có sẵn + các ô ký tự do:**

| # | Chức danh | Mặc định bật? | Xoá được? | `Tên người ký` | Luật |
|---|---|---|---|---|---|
| 1 | `Người lập phiếu` | ✔ **bật** | ❌ chỉ tắt được | **chỉ đọc** (từ Thiết lập người ký) | `R-TLMI-184` · `R-TLMI-186` |
| 2 | `Kế toán trưởng` | ✔ **bật** | ❌ | chỉ đọc | như trên |
| 3 | `Giám đốc` | ✔ **bật** | ❌ | chỉ đọc | như trên |
| 4 | `Thủ kho` | ❌ **tắt** | ❌ | chỉ đọc | `R-TLMI-184` |
| 5 | `Thủ quỹ` | ❌ **tắt** | ❌ | chỉ đọc | `R-TLMI-184` |
| 6.. | ô ký **tự do** | — | ✔ `✕` | **gõ tay được** | `R-TLMI-187` · `R-TLMI-192` · `R-TLMI-193` |

`R-TLMI-184`: **mặc định bật ba, tắt hai.**
`R-TLMI-193`: **không giới hạn số ô ký tự do** — bản code cũ đặt trần 4 ô (`R-MAUIN-016`), **phải gỡ**.
`R-TLMI-183`: thứ tự mặc định như trên, **kéo thả đổi được** (`⠿`).

⚠ Figma frame 6 vẽ ô ký tự do có `Thủ quỹ` ở dòng tên người ký — đó là **tên tự gõ** của ô tự do, không
phải chức danh `Thủ quỹ` có sẵn (dòng 5 chưa xuất hiện trong ảnh vì đã bị kéo/tắt). Không mâu thuẫn.

---

## 4. Nguồn dữ liệu — **luôn** từ *Thiết lập người ký* (`R-TLMI-046`, chốt **C04**)

| Trường | Nguồn | Mẫu sửa được? | Luật |
|---|---|---|---|
| `Chức danh` (5 chức danh có sẵn) | Thiết lập người ký | ❌ | `R-TLMI-186` |
| `Tên người ký` (5 chức danh có sẵn) | Thiết lập người ký | ❌ chỉ đọc | `R-TLMI-186` |
| Cờ `In tên người ký` | Thiết lập người ký | ❌ | `R-TLMI-196` |
| `Tiêu đề in ra` | mặc định = `Tiêu đề người ký` của Thiết lập người ký | ✔ **SỬA ĐƯỢC** | `R-TLMI-188` · chốt **C04** |
| `Dòng ghi chú` | mặc định `(Ký, họ tên)` | ✔ | `R-TLMI-190` |
| `Tên người ký` của **ô ký tự do** | gõ tay | ✔ | `R-TLMI-187` |

**Đã có thật trong repo:** `client/src/features/heThong/thongTinCongTy/components/NguoiKyTable.tsx`;
BE `CompanyInfoResponse` có `tieuDeNguoiKyGiamDoc` / `tenNguoiKyGiamDoc`, `…KeToanTruong`, `…ThuKho`,
`…ThuQuy`, `…NguoiLapPhieu`, `inTenNguoiKyTrenChungTu`
(`cell-app/.../platform_iam/tenant/internal/controller/TenantConfigController.java:89`).
⇒ Panel này **không** cần API mới, chỉ cần BE gộp vào nhánh `chung` của A1.

**Chi nhánh nào?** Chốt **C05**: **chi nhánh ghi trên chứng từ**, giống khối đầu trang (`R-TLMI-199`,
Q-14 / L-7 — tạm đọc từ tenant, đi qua cổng `HoSoDonViPort.theoChiNhanh()`).

---

## 5. Bảng trường

| Trường | Khoá i18n | Field API | Kiểu | Ràng buộc | Mặc định | Luật |
|---|---|---|---|---|---|---|
| Thứ tự ô ký | — | thứ tự mảng `khoi.chuKy.o[]` | — | kéo thả | như §3 | `R-TLMI-183` |
| Bật / tắt | `chuKy.in` | `o[].hien` | bool | — | 3 bật / 2 tắt | `R-TLMI-184` · `R-TLMI-191` |
| `Chức danh` | `chuKy.chucDanh` | `o[].vaiTro` | enum \| `null` | chỉ đọc; `null` = ô tự do | — | `R-TLMI-185/186` |
| `Tiêu đề in ra` | `chuKy.tieuDeInRa` | `o[].tieuDe` | string | **không trống** (khi bật), ≤ 60 | tiêu đề người ký | `R-TLMI-188/189` |
| `Dòng ghi chú` | `chuKy.dongGhiChu` | `o[].ghiChu` | string | — | `(Ký, họ tên)` | `R-TLMI-190` |
| `Tên người ký` (ô tự do) | `chuKy.tenNguoiKy` | `o[].tenTuDo` | string | gõ tay | trống | `R-TLMI-187` |
| Dòng ngày | `chuKy.dongNgay` | `khoi.chuKy.dongNgay` | bool | — | ✔ | `R-TLMI-197` |
| `Chỗ trống ký` | `chuKy.choTrongKy` | `khoi.chuKy.choTrongKy` | `'THAP'\|'VUA'\|'CAO'` | select | `VUA` | `R-TLMI-198` |

---

## 6. Hành vi & sự kiện

| Thao tác | Điều kiện | Việc làm | Luật |
|---|---|---|---|
| Bỏ tick một ô ký | luôn | ô đó **không in** | `R-TLMI-191` |
| Bấm `✕` | **chỉ ô tự do** | xoá ô khỏi lưới; chức danh có sẵn **không có** `✕` | `R-TLMI-192` |
| Bấm `+ Thêm ô ký tự do` | luôn (**không giới hạn**) | thêm dòng mới, badge `tự do`, `Tiêu đề in ra` và `Tên người ký` trống | `R-TLMI-193` |
| Kéo `⠿` | luôn | đổi thứ tự ô ký | `R-TLMI-183` |
| Xoá trống `Tiêu đề in ra` của ô **đang bật** | luôn | báo `MSG_211` tại chỗ | `R-TLMI-189` |
| Xoá trống `Tiêu đề in ra` của ô **đang tắt** | luôn | **không** báo lỗi | `R-TLMI-189` |
| Tắt `👁` khối Chữ ký | luôn | khối không in; bỏ qua validate khối đó (C18) | `R-TLMI-207` |
| Bấm link `Thiết lập người ký` | luôn | mở màn Thông tin công ty › tab Người ký | `R-TLMI-052` |

**Trên bản in:**

| Luật | Nội dung |
|---|---|
| `R-TLMI-194` | khối Chữ ký in **chia đều**, mỗi ô rộng **tối thiểu 4 cm** |
| `R-TLMI-195` | hàng ô ký **hết chỗ** thì ô tiếp theo **tự xuống hàng** |
| `R-TLMI-196` | **in tên người ký** theo cờ `In tên người ký` của Thiết lập người ký |
| `R-TLMI-197` | dòng `Ngày … tháng … năm …` in **phía trên** khối Chữ ký khi bật |
| `R-TLMI-198` | `Chỗ trống ký` `Thấp` / `Vừa` / `Cao` đổi khoảng trắng giữa dòng ghi chú và tên người ký |
| `R-TLMI-200` | cuối trang **không đủ chỗ** thì **cả khối** Chữ ký sang trang mới (BE) |

CSS: `display: flex; flex-wrap: wrap` với `flex: 1 1 4cm; min-width: 4cm` ⇒ thoả `R-TLMI-194` + `195`
bằng một quy tắc.

---

## 7. Validation phía FE

| # | Trường | Điều kiện | Message (nguyên văn) | Thời điểm | Tầng | Luật |
|---|---|---|---|---|---|---|
| V12 | `Tiêu đề in ra` của ô ký **tự do đang bật** | không trống, ≤ 60 ký tự | `Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự` | rời ô, khi Lưu | Client/Server | `R-TLMI-189` |

⚠ Bảng 17 dòng (`R-TLMI-239` V12) chỉ nói **"ô ký tự do đang bật"**. Nhưng `R-TLMI-188` nói
`Tiêu đề in ra` **bắt buộc** cho **mọi** ô ký. Hai luật lệch phạm vi.
**Xử lý:** theo **bảng 17 dòng** (nguồn duy nhất của cổng kiểm tra) ⇒ chỉ kiểm ô **tự do đang bật**;
chức danh có sẵn luôn có tiêu đề mặc định từ Thiết lập người ký nên thực tế không trống được.
Ghi nhận là chỗ tài liệu lệch nhẹ — không chặn code.

---

## 8. Phân bổ file

| Việc | File |
|---|---|
| Panel Chữ ký | `components/inspector/ChuKyInspector.tsx` |
| Một dòng ô ký | `components/inspector/OKyRow.tsx` |
| Kéo thả ô ký | `components/SortableList.tsx` (dùng lại) |
| Render khối Chữ ký trên giấy (chia đều, ≥ 4 cm, wrap) | `components/BanInPaper.tsx` |
| Ràng V12 | `helpers/kiemTraMau.ts` |
| Hằng `VAI_TRO_KY` (5) · `GHI_CHU_KY_MAC_DINH` · `CHO_TRONG_KY` · `GIOI_HAN_TIEU_DE_O_KY = { max: 60 }` · `BE_RONG_O_KY_TOI_THIEU = '4cm'` | `constants/constants.ts` |
| Chữ in ra giấy `(Ký, họ tên)` · `(Ký, họ tên, đóng dấu)` · `Ngày {ngay} tháng {thang} năm {nam}` | `i18n/vi.ts` nhánh `banIn.*` (Q13) |

---

## 9. Kiểm thử — `test/ChuKyInspector.test.tsx` (DOM)

| Test | Input → Kỳ vọng |
|---|---|
| `R-TLMI-182 · danh sách gồm 5 chức danh và các ô ký tự do` | mẫu chuẩn → đúng 5 dòng chức danh |
| `R-TLMI-183 · thứ tự mặc định` | → `Người lập phiếu · Kế toán trưởng · Giám đốc · Thủ kho · Thủ quỹ` |
| `R-TLMI-183 · kéo thả đổi thứ tự` | kéo dòng 1 xuống dòng 3 → thứ tự mảng đổi |
| `R-TLMI-184 · mặc định bật ba, tắt hai` | → 3 ô đầu `hien=true`, `Thủ kho` và `Thủ quỹ` `hien=false` |
| `R-TLMI-185 · ô ký tự do mang nhãn "tự do"` | thêm ô tự do → có badge `tự do` |
| `R-TLMI-186 · chức danh có sẵn: Tên người ký chỉ đọc, không có nút xoá` | → text (không phải input), **không** có `✕` |
| `R-TLMI-187 · ô ký tự do: Tên người ký gõ tay được, có nút xoá` | → là input, có `✕` |
| `R-TLMI-188 · Tiêu đề in ra mặc định là Tiêu đề người ký` | `chung.nguoiKy.giamDoc.tieuDe='Giám đốc'` → ô hiện `Giám đốc` |
| `R-TLMI-188 · Tiêu đề in ra SỬA ĐƯỢC (chốt C04)` | gõ tên khác → giá trị vào `mau`, không bị ghi đè |
| `R-TLMI-189 · ô tự do đang BẬT mà tiêu đề trống thì MSG_211` | → `Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự` |
| `R-TLMI-189 · ô tự do đang TẮT mà tiêu đề trống thì KHÔNG lỗi` | bỏ tick → badge không thành `Có lỗi` |
| `R-TLMI-189 · 60 hợp lệ, 61 không` | → `MSG_211` cho 61 |
| `R-TLMI-190 · dòng ghi chú mặc định` | → `(Ký, họ tên)`; Giám đốc → `(Ký, họ tên, đóng dấu)` |
| `R-TLMI-191 · bỏ tick thì ô không in` | bỏ tick `Giám đốc` → `BanInPaper` không render ô đó |
| `R-TLMI-192 · chức danh chỉ tắt được, ô tự do xoá được` | → 5 dòng chức danh không có `✕`; ô tự do có |
| `R-TLMI-193 · thêm ô ký tự do không giới hạn` | bấm 12 lần → 12 ô tự do, **không** báo lỗi |
| `R-TLMI-194 · mỗi ô ký rộng tối thiểu 4 cm` | 6 ô bật → CSS `min-width: 4cm` |
| `R-TLMI-195 · hàng hết chỗ thì xuống hàng` | → container có `flex-wrap: wrap` |
| `R-TLMI-196 · in tên người ký theo cờ của Thiết lập người ký` | `inTenNguoiKy=false` → `BanInPaper` **không** in tên; `=true` → in |
| `R-TLMI-196 · hộp ghi chú hiện trạng thái cờ` | `=true` → text `… (đang: Có) …` |
| `R-TLMI-197 · dòng Ngày … phía trên` | bật → `BanInPaper` render `Ngày 27 tháng 08 năm 2026` trên khối |
| `R-TLMI-198 · Chỗ trống ký Thấp / Vừa / Cao` | select 3 option; đổi → chiều cao khoảng trắng đổi |
| `R-TLMI-046 · người ký luôn theo thiết lập chung` | `mau` **không** chứa tên người ký hay cờ in tên |
| `R-TLMI-052 · link Thiết lập người ký` | → có link, nguyên văn nhãn `Thiết lập người ký` |
| `C18 · khối Chữ ký đang ẩn thì bỏ qua validate` | tắt `👁`, ô tự do tiêu đề trống → badge không thành `Có lỗi` |

---

## 10. BR đã áp dụng

| BR | Áp ở đâu |
|---|---|
| BR8 | dòng `Ngày … tháng … năm …` |
| BR13 | ô `Tiêu đề in ra` bắt buộc khi bật; kiểm khi rời ô |
| BR30 | chốt **C18** — khối ẩn thì bỏ qua validate |
| BR50.7 (Phase 2) | hồ sơ đơn vị theo **chi nhánh ghi trên chứng từ** (chốt **C05**, Q-14 / L-7) |
