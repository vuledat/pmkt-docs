# Review — client PR #191 «Feature/hoa don mua hang dich vu 1.0»

**Chế độ:** NHANH (chỉ đọc + kiểm tĩnh bằng git — KHÔNG chạy typecheck/lint/test/build)
**head** `6d759400` · **base** `origin/develop` = `31d7f8a2` · **merge-base** `31d7f8a2`
**Phạm vi:** 1 file · +15 −56 — `src/features/muaHang/chungTuMuaHang/components/MuaHangHoaQuickDetail.tsx`
**Nguồn đối chiếu:** `pmkt-docs/ba/PMKT-E-00485_ChungTuMuaHangDN/5.screens/SCR_CTMH_DanhSach.md` §BR_CTMH_DS_05
**BR chung đã đọc:** không cần — thay đổi thuần cấu trúc tab, mọi luật cần dùng nằm trong BR nội bộ màn.

| Mức | Số | Mã |
|---|---|---|
| 🚫 Blocker | 1 | B1 |
| ⚠️ Major | 0 | — |
| 🔸 Minor | 1 | m1 |
| 💬 Nit | 2 | n1, n2 |

---

## 🚫 B1 — `useState` không còn được dùng ⇒ `noUnusedLocals` làm typecheck/build đỏ

**File:** `src/features/muaHang/chungTuMuaHang/components/MuaHangHoaQuickDetail.tsx:2`
**Nguồn:** `client/tsconfig.app.json:20` → `"noUnusedLocals": true`; CLAUDE.md §Trước khi báo hoàn thành (`npm run typecheck` là cổng bắt buộc).
**Trigger:** biên dịch file này — diff xóa `const [postingPage, setPostingPage] = useState(1)` nhưng giữ nguyên import.
**Actual / Expected:**

```
$ git show <head>:…/MuaHangHoaQuickDetail.tsx | grep -n useState
2:import { useMemo, useState } from 'react'        ← chỉ còn đúng dòng import, 0 nơi dùng
```

`import { useMemo, useState }` / `import { useMemo }`.
**Hậu quả:** `TS6133: 'useState' is declared but its value is never read` ⇒ `npm run typecheck` và `npm run build` đỏ, CI chặn. Sửa một ký tự.

*(Chưa chạy `tsc` — chế độ nhanh. Bằng chứng ở trên là tĩnh: cờ compiler bật + 0 nơi dùng.)*

---

## 🔸 m1 — Constant nghiệp vụ đặt trong `components/` thay vì `constants/`

**File:** `MuaHangHoaQuickDetail.tsx:21` — `const STORAGE_GROUP_CHUNG_TU_MUA_HANG = 'chung-tu-mua-hang'`
**Nguồn:** CLAUDE.md §Cấu trúc module FE mục 1 + lỗi hay gặp #7 — constant nghiệp vụ phải ở `constants/`.
**Trigger:** module đã có `chungTuMuaHang/constants/`; `'chung-tu-mua-hang'` là **khóa nhóm lưu trữ đính kèm** phía server, dùng chung với popup Thêm/Sửa sau này.
**Hậu quả:** popup nhập liệu khi làm tab Đính kèm sẽ khai lại chuỗi thứ hai; hai chuỗi lệch nhau thì file đính kèm xem-nhanh và file trong popup trỏ hai nhóm khác nhau, không ai bắt được.

---

## 💬 n1 — Bốn key i18n thành mồ côi sau khi bỏ tab Hạch toán

`chungTuMuaHang/i18n/vi.ts:75` `postingPreviewTab` và `vi.ts:111–114` `extraCol.taiKhoan` ·
`doiUng` · `phatSinhNo` · `phatSinhCo` (cùng vị trí trong `en.ts`) không còn chỗ gọi nào
(`git grep -c` → 0 ngoài chính hai file i18n). Comment `:100` vẫn ghi *"Chi phí / Thuế / **Hạch toán**
/ Tham chiếu"*. Dọn cả key lẫn comment trong cùng diff — đúng phạm vi đang sửa, không phải mở rộng.

## 💬 n2 — Commit message không theo chuẩn

`update giao dien mua hang`, `update phan bo`, `giao diện phân bổ chi phí mua hàng` — chuẩn
(9 luật §8) là `<type>(<scope>): <mô tả>`. Ba commit nội dung + 3 merge develop cho một file 15 dòng
⇒ nên squash.

---

## Điểm đúng — đáng ghi nhận

Bỏ tab **Hạch toán** khỏi panel xem nhanh và thay bằng **Đính kèm** là **đúng đặc tả**, không phải
mất chức năng: `SCR_CTMH_DanhSach.md` §BR_CTMH_DS_05 liệt kê đủ bộ tab của section chi tiết —
Chi tiết hàng hóa/dịch vụ · Chi phí mua hàng · Phí trước HQ · Phí hàng về kho · Thuế · **Đính kèm** ·
Tham chiếu — **không có** tab Hạch toán. Test `chungTuMuaHang/test/visibility.test.ts:41` cũng đã
khẳng định `expect(result.detailTabs).not.toContain('hachToan')`. Thứ tự Đính kèm trước Tham chiếu
khớp bảng. Dữ liệu ghi sổ vẫn xem được qua `MuaHangPostingDataModal` (SCR_CTMH_XemDuLieuGhiSo), và
hook `useMuaHangPostingEntries` vẫn còn caller ở đó ⇒ không thành code chết.
Component dùng `DinhKemPanelTab` từ `@domain-kit` (`src/base/domainKit/dinhKem/index.ts:13`) đúng
lỗi #6 (tận dụng base), i18n `muaHang:quickDetail.tabs.dinhKem` có đủ ở **cả** `vi.ts:80` và
`en.ts:65` ⇒ luật 2 đạt.

---

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ✅ Không secret · không `any`/`@ts-ignore` mới · không `../../` (dùng `@base`, `@domain-kit`, `@platform`, `@features/*`) · text UI đều qua `t()` với key có ở cả `vi.ts` và `en.ts` · không chạm vùng đóng băng. |
| B — Kiến trúc & 7 lỗi | xem bảng dưới |
| C — Nghiệp vụ & truy vết | ✅ Khớp BR_CTMH_DS_05. `trace.sh`/`msg.sh` `NOT-RUN` — chưa có thư mục `docs/doing/*-spec` cho PMKT-E-00485, không đoán bừa PYC. |
| D — Vệ sinh diff & Git | ⚠ n1, n2. Cây commit sạch (`git status --porcelain` rỗng), không file `??` trong `src/`, không sửa barrel/`index.ts`, không rename. |

## Bảy lỗi hay gặp

| # | Mục | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ File nằm đúng `components/`, gốc module vẫn chỉ có `index.ts`, không tách màn theo hành vi. |
| 2 | Version migration | ✅ N/A — repo FE, không có migration. |
| 3 | Chưa test lại sau merge | ✅ N/A — `git rev-list --count 31d7f8a2..origin/develop` = **0**, 0 file giao nhau. |
| 4 | N+1 / request trong vòng lặp render | ✅ Giảm đi — bỏ hẳn một query phân trang khỏi panel; `DinhKemPanelTab` tự quản request của nó. |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ N/A — không phải BE. |
| 6 | Chưa tận dụng base FE | ✅ Dùng `DinhKemPanelTab` của `@domain-kit` thay vì tự dựng bảng đính kèm. |
| 7 | Constant đặt sai chỗ | ⚠ m1. |

## Cổng đã chạy

| Cổng | Kết quả |
|---|---|
| `git status --porcelain` | sạch |
| `git rev-list --count <merge-base>..origin/develop` | 0 |
| `comm -12` file giao nhau với develop | 0 file |
| đọc diff barrel/`index.ts` | N/A — diff không chạm barrel |
| `trace.sh` / `msg.sh` | `NOT-RUN` — chưa có thư mục spec cho PMKT-E-00485 |
| `typecheck` · `lint` · `lint:boundaries` · `test` · `build` · `check:committed` | `NOT-RUN` — chế độ nhanh |

**Chưa đọc / chưa kiểm:** không có — diff gồm đúng một file và đã đọc trọn ở head.
Chưa xác thực bằng trình duyệt việc tab Đính kèm render đúng dữ liệu (`qa-flow` chưa chạy).

---

## Kết luận: 🔴 **REJECT** — B1 (import thừa làm đỏ cổng typecheck/build)

Ngoài B1, thay đổi đúng hướng và đúng đặc tả; m1/n1/n2 là dọn nhỏ trong cùng phạm vi.
Cổng typecheck/lint/test/build **chưa chạy** (chế độ nhanh) — không dùng báo cáo này để APPROVE.
