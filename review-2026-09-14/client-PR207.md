# Review PR #207 — `ospgroupvn-pmkt/client` · [Bugfix] Cấu hình ban đầu

| | |
|---|---|
| **Chế độ** | **NHANH** — chỉ đọc + kiểm tĩnh bằng git/grep. KHÔNG chạy test/build/npm, KHÔNG worktree, KHÔNG sửa code, KHÔNG đăng comment lên PR (theo yêu cầu người gọi). |
| PR | https://github.com/ospgroupvn-pmkt/client/pull/207 · tác giả `truongnq98` · state OPEN |
| Nhánh | `bugfix/bug-sheet-onboarding-cau-hinh` → `develop` ✅ đúng chuẩn `loại-nhánh/tên-mo-ta` |
| head | `acb62d7c070f8cde41860df265f20dfbb10d4d48` |
| merge-base | `39e0582c9af7885d3571378d917e61ddee3e4347` |
| Diff | 21 file · +237 / −51 · 1 file mới (`LogoutConfirmModal.tsx`) |
| Working tree | `git status --porcelain` = 0 dòng ✅ |
| Epic liên quan | `pmkt-docs/ba/PMKT-E-14549_CauHinhBanDau` |

**KẾT LUẬN: REJECT** — 1 Blocker (B1), 4 Major (M1–M4).
Cổng `typecheck / lint / lint:boundaries / test / build` **chưa chạy** (chế độ nhanh) → kết luận này
chỉ dựa trên phần đã đọc.

---

## Bảng đếm finding

| Mức | Số lượng | Mã |
|---|---|---|
| **Blocker** | 1 | B1 |
| **Major** | 4 | M1 · M2 · M3 · M4 |
| **Minor** | 8 | m1 … m8 |
| **Nit** | 5 | n1 … n5 |
| **Tổng** | **18** | |

---

## Blocker

### B1 — Mặc định "Đồng tiền hạch toán = VNĐ" bị mất do hai lần `setStep2` cùng một render

`src/features/heThong/onboarding/hooks/useOnboardingWizard.ts:148-170`

**Nguồn**: `pmkt-docs/ba/PMKT-E-14549_CauHinhBanDau/5.screens/SCR_CauHinhBanDau/SCR_CauHinhBanDau_ThietLap.md:46`
— hàng *Đồng tiền hạch toán · Giá trị mặc định = **VNĐ*** (BR7 nội bộ màn).

**Cơ chế**: PR thêm khối render-phase thứ hai ngay sau khối VND sẵn có. Cả hai gate đều mở trong
**cùng một render** (render đầu tiên sau khi `restored` lật `true`), và cả hai gọi `setStep2(<object>)`
với **giá trị thuần**, không phải updater:

```ts
if (restored && !vndDefaulted && loaiTienQuery.data != null && step2.loaiTienId == null) {
  setVndDefaulted(true)
  const next = { ...step2, loaiTienId: vnd.id }              // A
  setStep2(next)
}
if (restored && !phuongPhapDefaulted && step2.phuongPhapTinhGiaXuatKho == null) {
  setPhuongPhapDefaulted(true)
  const next = { ...step2, phuongPhapTinhGiaXuatKho: ... }   // B — dựng từ CÙNG `step2` cũ
  setStep2(next)
}
```

Hàng đợi `useState` với action không phải hàm ⇒ **action cuối thắng**: `next` của khối B (dựng từ
`step2` trước khi A ghi) ghi đè A. `loaiTienId` quay về `null`, mà `vndDefaulted` đã bị đặt `true`
nên **không bao giờ điền lại**.

**Trigger**: `loaiTienQuery` đã có dữ liệu (cache React Query ấm — vào lại wizard, hoặc catalog về
trước `status`) tại đúng render `restored` lật true — tức là đường đi thường gặp nhất.

**Actual**: ô Đồng tiền hạch toán trống, người dùng phải tự chọn; bấm "Hoàn tất" thì rơi vào
`validation.missingRequiredStep2` (MSG_PMKT-E-14549_202).
**Expected**: VNĐ được điền sẵn theo SCR.

**Hậu quả**: mất một mặc định BA đã chốt, ngay trên luồng onboarding lần đầu.
**Không có test nào phủ** — `src/features/heThong/onboarding/test/` không hề nhắc `VND` /
`DEFAULT_LOAI_TIEN_MA`, nên "66/66 xanh" trong PR body không chứng minh được điều ngược lại.

**Hướng sửa**: dùng updater cho cả hai khối — `setStep2((s) => ({ ...s, loaiTienId: vnd.id }))` và
`setStep2((s) => ({ ...s, phuongPhapTinhGiaXuatKho: ... }))`, tương ứng cho `setSnapshot`.

---

## Major

### M1 — Bấm nút lần thứ hai với cùng lỗi: không toast, không chữ đỏ, không phản hồi gì

`src/features/heThong/onboarding/OnboardingWizardPage.tsx:111-116` (toast) ·
`:313` và `:446` (hai dòng `{wizard.stepXError && <span …>}` bị **xóa**)

```ts
const stepError = wizard.step === 1 ? wizard.step1Error : wizard.step2Error
useEffect(() => { if (stepError) toast.error(stepError) }, [stepError, toast])
```

**Trigger**: bấm "Tiếp tục" khi thiếu Lĩnh vực hoạt động → toast hiện. Không sửa gì, bấm lần hai.
`setStep1Error(<cùng chuỗi>)` ⇒ state không đổi ⇒ effect không chạy lại ⇒ **không có toast mới**.
Đồng thời PR đã gỡ dòng chữ đỏ cuối form, nên **không còn bất kỳ phản hồi nào**.

**Actual**: nút trông như hỏng — đúng triệu chứng mà PR này đang đi sửa.
**Expected**: mỗi lần bấm mà còn thiếu dữ liệu đều phải có phản hồi (BR26.1 toast, hoặc giữ lại
dòng lỗi tại chỗ).

**Ghi chú**: `invalidField` không dính lỗi này vì effect gọi `clearInvalidField()` đưa về `null`, nên
cuộn + focus vẫn chạy lần hai. Chỉ riêng thông báo là mất.

### M2 — Đổi nguyên văn MSG_PMKT-E-14549_203 mà tài liệu BA chưa đổi

`src/features/heThong/onboarding/i18n/vi.ts:126` · `cauHinhChiTiet/i18n/vi.ts:118` (+ 2 file `en.ts`)

**Nguồn**: `pmkt-docs/ba/PMKT-E-14549_CauHinhBanDau/6.messages.md:23`

```
| MSG_PMKT-E-14549_203 | … Vui lòng chọn ngày bắt đầu dữ liệu >= {NgayHieuLuc} | Error | … |
```

**Actual**: `… Vui lòng chọn ngày bắt đầu dữ liệu từ {{ngayHieuLuc}} trở đi`
**Expected**: nguyên văn tiếng Việt của tài liệu (CLAUDE.md §BR: *"giữ nguyên văn tiếng Việt của BR
làm giá trị trong `vi.ts`, không tự diễn đạt lại"*).

PR body thừa nhận đây là lệch cố ý do tester chốt, nhưng **không có bản chốt BA kèm tên + ngày** và
tài liệu chưa được cập nhật ⇒ vi phạm luật 9 và Cổng đặc tả luật 2 (*không tự đặt luật mới*).
Cần BA duyệt + sửa `6.messages.md` trước khi merge, hoặc revert về `>=`.

### M3 — Mặc định "Phương pháp = Bình quân cuối kỳ" trái với SCR (ô mặc định để trống)

`src/features/heThong/onboarding/hooks/useOnboardingWizard.ts:40` và `:165-170` ·
`OnboardingWizardPage.tsx:188-193` (đảo thứ tự option)

**Nguồn**: `SCR_CauHinhBanDau_ThietLap.md:50` — hàng *Phương pháp · Select · **Giá trị mặc định = `-`***
(BR9 nội bộ màn). Trường này bắt buộc khi `LoaiPhuongPhap = "Tất cả vật tư dùng chung một phương pháp"`.

**Actual**: form khởi tạo `phuongPhapTinhGiaXuatKho = binhQuanCuoiKy`, và giá trị này còn được ghi
**vào cả `snapshot`** ⇒ `dirty = false` ⇒ hệ thống coi như người dùng đã chủ động chọn.
**Expected**: để trống, bắt người dùng chọn (đó là lý do trường được đánh dấu bắt buộc).

**Hậu quả**: phương pháp tính giá xuất kho là tham số kế toán rất khó đổi sau khi đã có phát sinh;
điền sẵn thay người dùng trên một trường bắt buộc là quyết định nghiệp vụ, phải do BA chốt chứ không
phải tester. Chưa có nguồn ⇒ thuộc mục "Nghiệp vụ tự bịa" của Lớp A.

### M4 — `useCauHinhChiTietForm`: đổi "fill khi bật checkbox" thành "fill khi mở màn", nhưng không đánh `dirty`

`src/features/heThong/cauHinhChiTiet/hooks/useCauHinhChiTietForm.ts:146-149`

```ts
useEffect(() => {
  if (!coPhatSinhNgoaiTe || taiKhoanQuery.data == null) return
  fillCltgDefaults()
}, [coPhatSinhNgoaiTe, taiKhoanQuery.data])
```

Trước PR, javadoc ghi rõ *"pre-fill 515/635 ONLY for fields still empty, **only on the ON transition**"*.
Nay effect chạy:

1. **Ngay khi mở màn** với tenant đã có `CoPhatSinhNgoaiTe = true` và 4 ô TK CLTG còn trống;
2. **Mỗi lần `taiKhoanQuery.data` đổi tham chiếu** (refetch on focus của React Query).

`form.setFieldsValue()` **không** kích `onValuesChange` ⇒ `handleValuesChange()` không chạy ⇒
`setDirty(…)` không chạy.

**Actual**: màn tự ghi TK 515/635 vào form, `dirty` vẫn `false`. Người dùng mở màn, không chạm gì,
thoát ra — guard "còn thay đổi chưa lưu" im lặng. Nếu sau đó họ sửa một trường khác rồi Lưu, 515/635
được **gửi lên và lưu vĩnh viễn** mà chưa bao giờ có quyết định của người dùng.
**Expected**: hoặc đánh `dirty` để guard cảnh báo, hoặc giữ nguyên "chỉ fill khi người dùng bật
checkbox" như javadoc/BR12 đang mô tả.

Đây là tài khoản hạch toán chênh lệch tỷ giá — ghi sai là sai sổ, không chỉ sai hiển thị. Mở rộng
phạm vi BR12 cần BA chốt.

---

## Minor

| Mã | File:dòng | Nội dung |
|---|---|---|
| **m1** | `useCauHinhChiTietForm.ts:149` | Dep array thiếu `fillCltgDefaults` → `react-hooks/exhaustive-deps`. Cổng `npm run lint` **chưa chạy** (chế độ nhanh) nên chưa biết là warn hay error. |
| **m2** | `OnboardingWizardPage.tsx:111-112` | Comment *"giữ nguyên dòng chữ đỏ tại chỗ"* mâu thuẫn với chính diff (xóa cả `step1Error` lẫn `step2Error` span). Comment sai còn tệ hơn không có. |
| **m3** | `onboarding/i18n/{vi,en}.ts` khối `logoutConfirm` | Popup xác nhận mới, 4 chuỗi người dùng thấy, **không có mã `MSG_PMKT-E-14549_nnn`** và không có hàng tương ứng trong `6.messages.md`. BR16 yêu cầu cảnh báo hiển thị popup xác nhận phải khai mã message. |
| **m4** | `OnboardingWelcomePage.tsx:200-204` | `onConfirm={() => void logout()}` — modal **không đóng** trước khi logout, khác với `OnboardingWizardPage.handleLogout()` (gọi `setConfirmingLogout(false)` trước). Logout chậm/lỗi ⇒ dialog treo trên màn. Hai caller của cùng một modal cư xử khác nhau. |
| **m5** | `DongTienPicker.tsx:33` | `rows={xepUuTienLenDau(rows)}` chạy **mỗi render**: copy + sort toàn danh mục và tạo tham chiếu mảng mới mỗi lần gõ phím, phá memo bên trong `CommonComboGrid`. Nên `useMemo` theo `rows`. |
| **m6** | `onboarding/` · `thongTinCongTy/` | Vi phạm "gốc module chỉ có `index.ts`": `OnboardingWelcomePage.tsx`, `OnboardingWizardPage.tsx`, `types.ts`, `paths.ts`, `ThongTinCongTyPage.tsx` nằm ở gốc module. **Có trước PR**, nhưng PR bồi thêm ~70 dòng vào các file gốc đó thay vì dời về `pages/`. Không chặn merge; nên mở ticket riêng. |
| **m7** | — | `./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-14549_CauHinhBanDau fe` → **OK 0 · LECH 0 · CHUA-DAT 8 · THIEU 12** (20 message). Tồn tại từ trước, nhưng PR sửa nội dung 2 trong số đó mà vẫn không gắn mã. |
| **m8** | `onboarding/test/`, `cauHinhChiTiet/test/` | 21 lỗi được sửa, **0 test mới**. File test duy nhất bị chạm chỉ đổi nhãn `'Tỉnh thành phố'` → `'Tỉnh/Thành phố'`. Mặc định VND (B1), mặc định Phương pháp (M3), toast lặp (M1), auto-fill CLTG (M4) đều không có lưới an toàn. |

## Nit

| Mã | File:dòng | Nội dung |
|---|---|---|
| n1 | `OnboardingWizardPage.tsx:312`, `:445` | Dòng trống thừa còn lại đúng chỗ vừa xóa span lỗi. |
| n2 | `OnboardingWizardPage.tsx:41-42` | `import type { InvalidField } from './types'` chèn giữa cụm import component, phá thứ tự nhóm của file. |
| n3 | `OnboardingWizardPage.tsx:122` | `querySelector('input, textarea, [tabindex]')` — anchor `linhVuc` chứa card/checkbox tuỳ biến, khả năng cao không khớp selector ⇒ chỉ cuộn, không focus. |
| n4 | `OnboardingShell.tsx:132`, `GroupCard.tsx:25` | Màu hex và chuỗi padding vẫn viết thẳng (`'#f4f4f5'`, `'24px 16px'`, `'#e2e8f0'`). Pattern có sẵn của module, không do PR sinh ra. |
| n5 | `NganhNghePicker.tsx:42-45` · `DongTienPicker.tsx:50-53` | Hai dòng `popupWidth="field"` + `suffixIcon` kèm **comment giống hệt nhau** lặp ở 2 file. Nên thành mặc định của `ComboGridField` (`features/heThong/_shared`). |

---

## Lớp A — Cổng cứng

| Mục | Kết quả |
|---|---|
| Secret trong diff | ✅ không |
| Hardcode magic value | ✅ các giá trị mới đều là hằng có tên (`MA_UU_TIEN`, `DATE_MASK`, `FIELD_ANCHOR`, `CONTINUE_BUTTON_STYLE`, `BACK_BUTTON_STYLE`, `LABEL_COL`) |
| i18n đủ `vi.ts` **và** `en.ts` | ✅ khối `logoutConfirm` có ở cả hai; `thongTinCongTy/vi.ts` chỉ sửa nội dung nhãn sẵn có, không thêm key mới |
| Cộng chuỗi thay `t('key', {…})` | ✅ không |
| `any` / `@ts-ignore` mới | ✅ không — `InvalidField` là union string, `ValidationFailure` là interface |
| Import `../../` vượt cấp | ✅ không; alias `@base` / `@platform` / `@features/heThong/_shared` dùng đúng |
| Chạm vùng đóng băng (`legacy/`, `master_data/`, `Phase_2/`) | ✅ không |
| Commit thẳng `master`/`develop` | ✅ không — nhánh `bugfix/…` |
| PR trộn feat + refactor + format | ✅ không — thuần bugfix |
| **Nghiệp vụ không có nguồn** | ⚠️ **M3** (mặc định Phương pháp), **M4** (mở rộng phạm vi BR12), **m3** (text popup logout) |

## Lớp B — 7 lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ⚠️ **m6** — file lạc gốc module (có trước PR) |
| 2 | Không đánh lại version migration | ✅ N/A — repo FE, không có thư mục migration |
| 3 | Chưa test lại sau khi merge | ✅ N/A — nhánh tụt **16 commit** so với `origin/develop`, nhưng `comm -12` giữa hai tập file thay đổi = **0 file giao nhau** |
| 4 | N+1 / request trong vòng lặp render | ⚠️ **m5** — không phải request, nhưng có sort toàn danh mục mỗi render |
| 5 | Chưa tận dụng BaseController/BaseEntity | ✅ N/A — repo FE |
| 6 | Chưa tận dụng base FE | ✅ dùng lại `CommonConfirmModal`, `CommonDateInput`, `CommonComboGrid`, `FieldLabel`, `CommonButton`; đã xác minh `popupWidth`/`suffixIcon` tồn tại trên `CommonComboGridProps` (`src/base/components/picker/CommonComboGrid.tsx:143,151`), `format` trên `CommonDateInput`, `CaretDownIcon` re-export qua `src/base/index.ts:734`. Không sửa file nào trong `src/base/` ✅ |
| 7 | Constant đặt sai chỗ | ⚠️ nhẹ — `MA_UU_TIEN`, `DATE_MASK`, `FIELD_ANCHOR`, `*_BUTTON_STYLE` đặt cạnh nơi dùng chứ không ở `constants/`; luật 1 cho phép *"đặt gần nơi dùng nhất"* ⇒ chấp nhận. Mã `MSG_…` chưa thành hằng/khoá ⇒ **m7** |

## Lớp C — Nghiệp vụ & truy vết

- `trace.sh`: **NOT-RUN** — không có thư mục `docs/doing/*-spec` nào cho `PMKT-E-14549_CauHinhBanDau`
  (đã liệt kê `docs/doing/`). Không dựng spec chỉ để có cái mà chấm.
- `msg.sh pmkt-docs/ba/PMKT-E-14549_CauHinhBanDau fe`: **đã chạy** → OK 0 · LECH 0 · CHUA-DAT 8 ·
  THIEU 12 (m7). Trạng thái có trước PR.
- `01-conflict.md`: **N/A** — không có spec.
- BR **đã đọc** qua `br.sh`: BR5, BR6, BR8, BR16, BR26.
  BR **chưa đọc** (liên quan nhưng chưa mở): BR3, BR7, BR9, BR12, BR14, BR15, BR27.
  ⚠ Lưu ý: `BR1…BR13` trích trong `SCR_CauHinhBanDau_ThietLap.md` là **BR nội bộ màn**, không phải
  BR chung của `business_rules.md` — các dẫn chiếu BR7/BR9/BR12 ở trên là BR nội bộ màn.
- Điểm **đúng** đáng ghi nhận: đổi glyph kính lúp → caret ở hai combogrid **không** đi ngược tài liệu
  như PR body lo ngại — BR5 §"Bổ sung · Cấu trúc combogrid" ghi rõ *"nút mũi tên xuống để mở danh
  sách"*. Tương tự, `getLabel` chỉ hiện Tên ở `TinhThanhPhoPicker`/`PhuongXaPicker` khớp BR5
  (*"Ô hiển thị giá trị đã chọn (thường là tên/mã)"*), lưới vẫn giữ cột Mã.
- Nguồn tài liệu đã đối chiếu trực tiếp:
  `SCR_CauHinhBanDau_ThietLap.md:30-52` (bảng trường + giá trị mặc định) · `6.messages.md:1-30`.

## Lớp D — Vệ sinh diff & Git

| Mục | Kết quả |
|---|---|
| Commit message / branch | ✅ `bugfix/bug-sheet-onboarding-cau-hinh` đúng chuẩn |
| Code debug / TODO không ticket | ✅ không |
| Boy-scout đúng phạm vi | ✅ diff bám đúng 21 lỗi tester |
| **Cổng cây commit** | ✅ `git status --porcelain` sạch (0 dòng); file mới `LogoutConfirmModal.tsx` đã nằm trong cây commit của `origin/pr/207`; không có barrel/`index.ts` nào được sửa nên không có nguy cơ `UNRESOLVED_IMPORT` |
| Rename bằng `mv` trần | ✅ N/A |
| Comment sai lệch so với code | ⚠️ **m2** |

---

## Cổng chưa chạy (chế độ nhanh)

`NOT-RUN — chế độ nhanh`, tất cả:
`npm run typecheck` · `npm run lint` · `npm run lint:boundaries` · `npm run test` · `npm run build` ·
`npm run check:committed`.

PR body tự khai `vite build` ✅ và `vitest run src/features/heThong` ✅ 66/66 (cả trước và sau khi
merge `origin/develop`) — **chưa được kiểm chứng độc lập ở lượt này**.

## Phần chưa đọc

Đã đọc toàn bộ 21 file trong diff. Chưa đọc:
`src/base/components/picker/CommonComboGrid.tsx` (chỉ grep xác nhận prop) ·
`src/base/components/modal/CommonConfirmModal.tsx` ·
`UC_CauHinhBanDau_Onboarding.md` · `UC_CauHinhChiTiet_ChinhSua.md` ·
`SCR_CauHinhChiTiet_*.md` · `Matrix/**` · BR3/7/9/12/14/15/27.

## Lệnh đã chạy

```bash
gh pr view 207 --repo ospgroupvn-pmkt/client --json …
git merge-base origin/develop origin/pr/207
git diff --stat / --name-status <MB>..origin/pr/207
git diff <MB>..origin/pr/207 -- <từng nhóm file>
git show origin/pr/207:<path>
git rev-list --count <MB>..origin/develop            # 16
comm -12 (git diff --name-only <MB> origin/develop) (git diff --name-only <MB> origin/pr/207)   # rỗng
git status --porcelain                                # rỗng
./docs/rules/br.sh 5 6 8 16 26
./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-14549_CauHinhBanDau fe
grep/sed trên src/base/**, pmkt-docs/ba/PMKT-E-14549_CauHinhBanDau/**
```

---

**Chưa đăng lên PR — người gọi yêu cầu rõ KHÔNG đăng comment (`gh pr comment` / `gh pr review`).**
