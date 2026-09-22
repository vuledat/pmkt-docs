# Review PR #282 — `client` · feat/mau-in → develop (lượt 2)

> **Chế độ: NHANH** (mặc định). Không chạy cổng `test`/`build`/`typecheck`, không worktree,
> không đo baseline, không merge thử. Kết luận giới hạn trong phạm vi đã đọc.

| | |
|---|---|
| PR | [ospgroupvn-pmkt/client#282](https://github.com/ospgroupvn-pmkt/client/pull/282) |
| Head | `2b28a398a` · Base `develop` · merge-base `a538216aa` |
| Quy mô | 125 file · +19 401 / −21 |
| Working tree | sạch (`git status --porcelain` = 0 dòng) |
| Lượt trước | head `14085f0ce` — 5 commit mới kể từ đó (4 fix + 1 merge develop) |

---

## Kết luận

**REQUEST CHANGES** — 1 Major mới (`M1`). Không có Blocker.

Ba Blocker và bốn Major của hai lượt review trước **đã đóng và đã kiểm lại bằng bằng chứng**
(xem §Đối chiếu). Major duy nhất còn lại là hệ quả **do chính lượt merge này sinh ra**: màn đích
mà hai luật `R-TLMI-050/051` đang chờ đã theo `develop` về repo, nhưng hai liên kết vẫn ẩn và có
một test đang ghim đúng tiền đề đã hết đúng.

---

## Findings

### ⚠️ M1 — Màn đích của `R-TLMI-050` · `R-TLMI-051` đã có sau merge, hai liên kết vẫn ẩn

`components/GiayVaChuGroup.tsx:239` · `components/DauTrangInspector.tsx:97` ·
`hooks/useLienKetNgoai.ts` · test ghim ở `src/test/mauInLienKetNgoai.test.ts:30`

**Nguồn:** `02-rules.md` R-TLMI-050 (*"Mở Cấu hình báo cáo chứng từ"*) · R-TLMI-051
(*"… › Thông tin trên bản in"*) — cả hai `FE · P2 · CHỐT`.

**Tiền đề cũ, nay đã sai.** Code và test đều nói màn đích *chưa có trong repo* (`01-conflict.md §C12`):

```ts
// src/test/mauInLienKetNgoai.test.ts:30
it('hai liên kết sang epic _20 vẫn để trống vì màn đích chưa tồn tại', () => {
  expect(LIEN_KET_NGOAI_MAC_DINH.cauHinhBaoCao).toBeUndefined()
```

Sau `2b28a398a`, `develop` mang về đủ cả ba mảnh:

```
src/features/heThong/cauHinhBaoCaoChungTu/            (module đầy đủ)
src/features/heThong/paths.ts:7   cauHinhBaoCaoChungTu: '/he-thong/cau-hinh-bao-cao-chung-tu'
src/features/heThong/routes.tsx:55  path: HE_THONG_PATHS.cauHinhBaoCaoChungTu   → sống qua gateByHandle
cauHinhBaoCaoChungTu/i18n/vi.ts:11  thongTinBanIn: 'Thông tin trên bản in'      → đúng mục R-TLMI-051 trỏ tới
```

**Hậu quả kép.** (1) Hai luật P2 không có hành vi, trong khi lý do hoãn đã hết. (2) Nguy hiểm hơn:
`trace.sh` vẫn chấm **`R-TLMI-050 OK` · `R-TLMI-051 OK`** và kết luận `DAT` — vì nó chỉ soi mã luật
có xuất hiện trong code/test hay không, không soi hành vi. Ai đọc cổng sẽ tưởng epic đã đủ.

**Đề nghị:** nối hai liên kết (đã có sẵn khuôn ở `R-TLMI-052`, nó dùng `HE_THONG_PATHS.thongTinCongTy`
theo đúng cách này), và sửa `mauInLienKetNgoai.test.ts` để canh **liên kết khớp route thật** thay vì
canh `undefined`. Nếu chưa làm trong PR này thì phải ghi vào phần *Còn treo* của PR — đừng để cổng
`DAT` nói hộ.

---

### 🔸 m1 — Bản vá `M1` lượt trước (tên nghiệp vụ theo dòng) không có test hồi quy

`hooks/useInTuDanhSach.ts` (`ChungTuDangIn.tenNghiepVu`) · `components/ModalInTuDanhSach.tsx:58` ·
`features/banHang/chungTuBanHang/components/ChungTuBanHangTab.tsx`

```
grep -rln "ModalInTuDanhSach|useInTuDanhSach" src/base/domainKit/mauIn/test/ \
     src/features/banHang/chungTuBanHang/test/     →  (không file nào)
```

Mọi test đang truyền cứng `tenNghiepVu="Chứng từ bán hàng"`, nên không bài nào phân biệt được dòng
*Bán hàng* với dòng *Bán dịch vụ*. Bug gốc (so `maNghiepVu` với nhãn phân loại dòng) đúng loại mà một
test render sẽ bắt ngay. Sửa xong mà không để lại cọc thì lần sau nó về y nguyên.

---

### 🔸 m2 — `Chia đều về 100%` vẫn chưa có thông báo khi bảng vượt 33 cột in

`helpers/doRongCot.ts` · chặn ở `helpers/kiemTraMau.ts:141`

Lượt này đã ghim ngưỡng thành hằng `SO_COT_IN_CHIA_DUOC_TOI_DA = 33` và ba test canh hành vi
(tổng vẫn 100, không số âm, nhưng có cột tụt dưới sàn 3). **Hành vi cho người dùng thì chưa đổi**:
vượt ngưỡng vẫn là không Lưu được và bấm lại nút cũng không thoát ra.

Đúng là không tự đặt luật được (R-TLMI-114/115 không phủ ca này — luật 9). Nhưng vậy thì nó là một
mục phải **hỏi BA**, không phải một mục đã xong. Giữ mở cho tới khi có câu chữ.

---

### 🔸 m3 — PR vẫn trộn hai việc không liên quan

`1a4792655 fix(auth): làm mới access token chủ động` — 4 file `src/app/providers/**`.
Lớp D: *"PR trộn `feat` + `refactor`"*. Phần auth viết tốt và có test riêng, nhưng nó là quyết định
hạ tầng phiên đăng nhập, không nên đi ké 19k dòng mẫu in. Nêu lại vì chưa xử lý.

---

### 💬 Nit

| | |
|---|---|
| `n1` | `helpers/inBanIn.tsx:65` — lệnh in nằm ở `<body onload="…">`, tức một inline handler. Repo hiện **không** đặt `Content-Security-Policy` ở đâu (đã tìm `client/`, `front-door/`, `cell-gateway/`) nên chạy tốt; nhưng blob document kế thừa CSP của trang tạo ra nó, nên ngày ai đó siết `script-src` thì In lại chết câm đúng như bug vừa vá. Một dòng ghi chú ở chỗ đặt CSP sau này là đủ. |
| `n2` | `components/RiengCuaMauGroup.tsx:71` — `TODO nợ` vẫn chưa mang mã ticket. Đã có hint ra giao diện nên hết phần "sai lặng lẽ", chỉ còn phần theo dõi công việc. |
| `n3` | `components/NutInChungTu.tsx:117` — host không truyền `onInMauCoDinh` thì mọi mục mẫu cố định hiện ra disable vĩnh viễn, không kèm lời giải thích. |
| `n4` | Ảnh nền: hint đã có (*"Ảnh nền chưa được tải lên máy chủ…"*, vi + en), nợ A3 `POST /api/mau-in/anh-nen` phía BE vẫn còn. Không phải việc của PR này, nhưng nên nằm trong *Còn treo* của PR. |

---

## Bảy lỗi hay gặp

| # | Mục | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ✅ Gốc `mauIn/` chỉ có `index.ts`; `components/modal/` là thư mục con duy nhất; `../../` chỉ còn trong `components/modal/` (đã kiểm lại trên head). Hai hằng tiền tố id kéo–thả đã về `constants/`. Không `mock.ts`. |
| 2 | Version migration | ✅ N/A — repo FE, không có `db/migration`. |
| 3 | Chưa test lại sau merge | ✅ **Đã đóng** — `git rev-list --count 2b28a398a..origin/develop` = **0**, không còn file giao nhau. Merge giữ đủ cả hai phía: `base/index.ts` có cả `CommonTreeSelect*` (develop) lẫn `CommonSegmented*`/`PropField*`; `icons/index.ts` có cả `PrinterIcon`/`TreeStructureIcon` lẫn `FloppyDiskIcon`; `chungTuBanHang/i18n/vi.ts` có cả `thieuDiaChi` lẫn `tenNghiepVu`. |
| 4 | N+1 / request thừa | ✅ Query key ổn định (`khoa` bọc `useMemo`); không có request trong vòng lặp render. |
| 5 | Chưa tận dụng BaseController / BaseEntity | ✅ N/A — repo FE. |
| 6 | Chưa tận dụng base FE | ✅ 5/5 hộp thoại đi qua `CommonConfirmModal`/`CommonModalShell`; `HopChonTruongO` đã chuyển sang `CommonSelectBox`. |
| 7 | Constant đặt sai chỗ | ✅ Đủ ba file `constants/{constants,paths,permissions}.ts`; `SO_COT_IN_CHIA_DUOC_TOI_DA` khai cạnh nơi dùng; `ariaLabel` đã chuyển sang interpolation. |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| **A — cổng cứng** | ✅ Không secret · không `any`/`@ts-ignore`/`eslint-disable` mới · không `axios` trần · không `../../` vượt cấp · không chạm vùng đóng băng · i18n `vi`/`en` **201 = 201**, không lệch một khoá · Zod parse toàn bộ phản hồi BE · nhánh `feat/mau-in` hợp lệ. |
| **B — kiến trúc** | Bảng bảy lỗi ở trên. |
| **C — nghiệp vụ & truy vết** | `trace.sh … fe` → **244/244 OK**, `KET LUAN: DAT`. ⚠ Con số này **không đủ tin** cho `R-TLMI-050/051` — xem `M1`. `01-conflict.md` 0 mục OPEN. BR25.2 áp đúng (thiếu quyền là ẩn hẳn). BR3 qua `@base`. BR7.1 đã sửa về `decimal(18,3)` cho Số lượng. |
| **D — vệ sinh diff & Git** | Cây commit sạch (0 dòng `git status`, 0 file `??`). Commit message 4 lượt mới đều đúng chuẩn `<type>(<scope>)`. ⚠ `m3` trộn việc. |

## Đối chiếu ba lượt review

| Mã | Nguồn | Trạng thái |
|---|---|---|
| 🚫 B1 — `window.open(…, 'noopener')` luôn trả null, In không chạy | lượt 2 | ✅ **Đóng** ở `efd49a38a` — bỏ cờ `noopener`, chuyển `print()` vào `onload` của chính tài liệu; 4 test ở `test/inBanIn.test.tsx`, trong đó có bài canh thẳng *"không truyền cờ noopener"*. |
| 🚫 B2 — `components/inspector/` ép `../../` | lượt 1+2 | ✅ **Đóng** ở `700fb4544`; kiểm lại trên head: `../../` chỉ còn trong `components/modal/`. |
| 🚫 B3 — chưa retest sau merge | lượt 2 | ✅ **Đóng** ở `2b28a398a` — 0 commit sau, 0 file giao nhau. Đáng ghi: **trước** merge, `dauSaoBatBuoc.render.test.tsx` đỏ 2 test ("Mã khách hàng" mang 2 dấu sao); **sau** merge xanh. Đúng thứ lỗi #3 cảnh báo. |
| ⚠️ M — tiêu đề nghiệp vụ sai ở dòng Bán dịch vụ | lượt 2 | ✅ **Đóng** ở `9930f5ed3` — thêm `ChungTuDangIn.tenNghiepVu`, đọc `row.loaiNghiepVu` ngay tại `onRowActionThem`. ⚠ chưa có test → `m1`. |
| ⚠️ M — Ctrl+S gọi Lưu chồng | lượt 1+2 | ✅ **Đóng** ở `14085f0ce` — guard `dangGhiRef` + test hồi quy giữ request treo. |
| ⚠️ M — 3 lỗi lint mới | lượt 2 | ✅ **Đóng** ở `efd49a38a` + `cdf501f81` — `eslint src/base/domainKit/mauIn src/app/providers` nay **exit 0**. |
| ⚠️ M — ảnh nền không tải lên, chưa disclose | lượt 2 | 🟡 **Giảm xuống Nit** (`n4`) — đã có hint ra giao diện ở `728fda488`; nợ BE còn nguyên. |
| ⚠️ M — spec epic nằm ở `pmkt-docs/ba/Phase_2/` | lượt 2 | ⏳ **Vẫn mở** — không phải việc của code, cần BA/PM xác nhận đã duyệt build. Không đọc tài liệu Phase 2 trong lượt này. |
| 🔸 m — ≥34 cột in | lượt 2 | 🟡 **Một phần** — đã ghim ngưỡng + test, hành vi chưa đổi → `m2`. |
| 🔸 m — cộng chuỗi `ariaLabel` | lượt 2 | ✅ **Đóng** ở `728fda488` — khoá `tuDo.nhanTheoTruong` có interpolation. |
| 💬 n — BR7.1 số lẻ | lượt 2 | ✅ **Đóng** ở `728fda488` — `SO_LE_BR7 = { tien: 2, soLuong: 3 }`. |
| 🔸 m — PR trộn hai việc · 💬 n — TODO thiếu ticket · 💬 n — mục mẫu cố định disable | lượt 2 | ⏳ **Vẫn mở** → `m3` · `n2` · `n3`. |

## Lệnh đã chạy

```
gh pr view 282 --json ...
git merge-base / rev-list --count / comm -12 / diff --name-status / grep
./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-...-spec fe   -> 244/244 OK, DAT
./docs/rules/br.sh 3 7 25            (lượt trước; BR trong phạm vi không đổi)
```

## Chưa chạy / chưa đọc

- **`npm run test` · `vite build` · `typecheck` · `lint:boundaries`** — `NOT-RUN — chế độ nhanh`.
  (Số liệu lint `exit 0` trích ở §Đối chiếu là kết quả đo trong phiên sửa code trước đó, không phải
  cổng của lượt review này.)
- **`msg.sh`** — `NOT-RUN`: thư mục PYC chỉ tồn tại dưới `pmkt-docs/ba/Phase_2/**` (vùng đóng băng).
  **Không đọc tài liệu Phase 2 trong lượt này.**
- **`check:committed`** — không chạy; thay bằng `git status --porcelain` (0 dòng).
- **Chưa đọc chi tiết**: `pages/mauIn.css` (1 407 dòng) · `components/BanInPaper.tsx` (618) ·
  `api/adapter.ts` (540) · `hooks/mauInStore.ts` (530) · `hooks/useVungChon.ts` (319) ·
  `helpers/luoiTuDo.ts` (343) · 22 file `test/` · 3 fixture JSON · toàn bộ phần `develop` kéo về
  qua merge (5 PR khác — ngoài phạm vi PR này, chỉ kiểm phần giao nhau).
- **BR đã đọc:** BR3 · BR7 · BR25. **Chưa đọc:** BR4 · BR8 · BR13 · BR16.1 · BR24.
