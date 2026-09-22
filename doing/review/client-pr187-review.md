# Review client PR #187 — Chi phí trả trước (CPTT)

**Chế độ: NHANH** (mặc định). Chỉ đọc + kiểm tĩnh bằng `git` / `grep` / `msg.sh`.
**KHÔNG chạy** test, build, typecheck, lint, worktree, merge thử → xem §Cổng chưa chạy.
Kết luận tối đa của chế độ này là "không thấy lỗi trong phạm vi đã đọc", **không APPROVE**.

## 0. Phạm vi & giả định

| Mục | Giá trị |
|---|---|
| Repo | `client/` (git repo riêng) |
| Head | `07a8fd49b1395586acf3edd4f97bea6826720ca5` (`refs/tmp/pr187-review`) |
| Base | `origin/develop` = `39e0582c9af7885d3571378d917e61ddee3e4347` |
| merge-base(develop, head) | `39e0582…` — **trùng đúng tip develop** |
| merge-base(master, head) | `35011087…`, cách head **242 commit** |
| Diff | 89 file · +5.783 / −784 |
| Commit | `a478806b feat: init chi phi tra truoc` · `07a8fd49 fix: sửa một số lỗi CPTT` |
| Working tree | `git status --porcelain` **rỗng** |

⚠ **Giả định phải ghi rõ:** máy này **không có `gh` CLI**, không đọc được metadata PR (base branch,
tên nhánh, mô tả, reviewer). Base `origin/develop` là **suy ra rồi xác minh bằng số đo**: merge-base
với `develop` bằng đúng tip `develop` (0 commit lệch), còn merge-base với `master` cách head 242
commit — `develop` gần hơn hẳn nên là base đúng. Tên nhánh nguồn **không kiểm được**, luật 8 về
`loại-nhánh/tên-mo-ta` vì thế ghi `NOT-RUN`.

Không file nào của diff rơi vào vùng đóng băng (`src/legacy/**`, `master_data/**`, `Phase_2/**`).
Mọi `grep`/`rg` trong lượt này đều thu hẹp `path` về `client/src` hoặc `docs/`.

---

## 1. Findings

### Blocker

Không có Blocker xác nhận được ở chế độ nhanh. Hai mục **M4** và **M6** là *nghiệp vụ không có
nguồn* — nếu BA xác nhận lệch tài liệu thì chúng lên Blocker theo Lớp A.

### Major

#### M1 · Ép kiểu mù dữ liệu API sang union nghiệp vụ
`src/features/chiPhiTraTruoc/khaiBao/helpers/giaTriBanDauSua.ts:148`

```ts
const kieuPhanBo = (row.kieuPhanBo ?? KIEU_PHAN_BO.theoThang) as KieuPhanBo
```

- **Nguồn:** `client/CLAUDE.md` §11.1 *"Không ép kiểu chỉ để TypeScript hết báo lỗi"*, §11.2.
- **Trigger:** mở popup Chỉnh sửa/Xem một khai báo mà BE trả `kieuPhanBo` ngoài hai giá trị đã biết.
  Schema khai `kieuPhanBo: z.string().nullish()` (`api/khaiBaoCPTTSchema.ts:191`) → chuỗi bất kỳ.
- **Actual:** chuỗi lạ được ép thẳng vào union. **Expected:** thu hẹp bằng type guard — **chính file
  này** làm đúng như vậy cho `loaiChungTu` ở dòng 115 (`laMaLoaiNguon`) và giải thích rõ vì sao.
- **Hậu quả:** `khoaNhom` (:54) rơi vào nhánh `TheoThang` ⇒ gom nhóm sai khoá ⇒ lượt Lưu kế tiếp
  `DiffThietLapPhanBo` bên BE ghép nhầm `id` giữa các dòng (chính rủi ro mà javadoc :81-82 cảnh báo).
  Sai âm thầm, không có thông báo nào.

#### M2 · Bản ghi "Ngừng hoạt động" bị CHẶN chọn — lệch BR5
`khaiBao/api/danhMucPhanBo.ts:174` · `khaiBao/hooks/useNguonTaiKhoanCPTT.ts:111`

```ts
disabled: d.trangThai === NGUNG_HOAT_DONG      // danhMucPhanBo.ts:174
disabled: d.ngungHoatDong                       // useNguonTaiKhoanCPTT.ts:111
```

- **Nguồn:** BR5 §"Chọn bản ghi theo trạng thái": *"Cho phép người dùng chọn bản ghi ở **cả 2 trạng
  thái**… hiển thị **cảnh báo nhưng không chặn**: 'Bản ghi đang ở trạng thái Ngừng hoạt động. Bạn có
  chắc chắn muốn sử dụng?'"*
- **Trigger:** chọn Tài khoản chi phí / Đơn vị / Vụ việc / Khoản mục / Đối tượng THCP đã ngừng hoạt động.
- **Actual:** ô bị khoá cứng. **Expected:** chọn được, kèm popup cảnh báo không chặn.
- **Kèm theo, cùng BR5:** sắp xếp chỉ theo mã/nhãn
  (`danhMucPhanBo.ts:176`, `danhMucTaiKhoan.ts:145`), **không** đẩy "Ngừng hoạt động" xuống cuối và
  không tô xám như BR5 §"Sắp xếp theo trạng thái" yêu cầu.
- **Hậu quả:** khai báo cũ dùng tài khoản/danh mục nay ngừng hoạt động thì mở ra sửa xong **không
  lưu lại được đúng giá trị cũ** ở ô đó.

#### M3 · Vét danh mục bằng vòng lặp request tuần tự (N+1 phía client)
`khaiBao/api/danhMucTaiKhoan.ts:124` · `khaiBao/api/danhMucPhanBo.ts:156`

```ts
for (let trang = 1; trang <= MAX_TRANG; trang++) {
  const { data } = await http.get<unknown>(TAI_KHOAN_BASE, { params: { page: trang, pageSize: 200 } })
```

- **Nguồn:** lỗi hay gặp #4 (`bon-lop.md`) — `checklist-fe` §E *"Gọi API trong vòng lặp"*.
- **Trigger:** mở popup Thêm mới / Chỉnh sửa / Xem
  (`pages/KhaiBaoCPTTPage.tsx:144,158` bật cả `useNguonTaiKhoanCPTT` lẫn `useNguonDanhMucPhanBo`).
- **Actual:** `await` nằm **trong** vòng lặp ⇒ các trang đi nối tiếp, không song song. Một danh mục
  tối đa 50 lượt; `useNguonDanhMucPhanBo` chạy **4 danh mục** + 1 danh mục tài khoản = tối đa **250
  request nối tiếp theo nhóm** cho một lần mở popup.
- **Expected:** BE trả cả tập trong một lượt, hoặc lấy `totalPages` ở lượt 1 rồi `Promise.all` các
  trang còn lại, hoặc dùng tìm kiếm phía server của combogrid.
- **Giảm nhẹ:** `staleTime: 5 * 60_000` nên chỉ trả giá ở lượt mở đầu / sau 5 phút. Không xoá được finding.

#### M4 · Nghiệp vụ không có nguồn — `locTaiKhoanIds` bị vô hiệu hoá âm thầm
`khaiBao/hooks/useNguonTaiKhoanCPTT.ts:69`

```ts
return thu.length > 0 ? thu : danhMuc   // lọc không khớp id nào ⇒ trả NGUYÊN danh mục
```

- **Nguồn:** BR02 của epic (trích trong chính javadoc :16-20 của file): *"LocTaiKhoan giới hạn danh
  sách TK chờ PB"*, và javadoc đó tự khẳng định *"ngày nó được seed thì cấu hình của tenant phải có
  hiệu lực"*.
- **Trigger:** tenant đã seed `mst_tai_khoan_ngam_dinh_chi_tiet.loc_tai_khoan` trỏ tới tài khoản
  **không nằm trong cửa sổ đã tải** (bị `MAX_TRANG` cắt — xem m4 — hoặc id đã đổi).
- **Actual:** ô chọn mở ra **toàn bộ** hệ thống tài khoản. **Expected:** đúng phạm vi tenant cấu hình.
- **Hậu quả:** người dùng chọn được tài khoản mà cấu hình đã cấm; server chặn sau, nhưng thông báo
  không nói được vì sao ô lại cho chọn. Luật *"thà rộng còn hơn chết"* ở javadoc :58-60 là **luật do
  code tự đặt**, tài liệu không có — CLAUDE.md luật 9 / Lớp A. **Cần BA chốt.**

#### M5 · Mã message không thành key i18n → cổng nguyên văn không đo được
`khaiBao/i18n/vi.ts` & `en.ts` (khoá `m003`, `m016`, `m027`…) · `khaiBao/api/khaiBaoCPTTModule.ts:104`

- **Nguồn:** `checklist-fe` §D: *"Mã message `MSG_PMKT-E-xxxxx_nnn` **là key i18n** trong `i18n/vi.ts`
  + `en.ts`"* · `docs/rules/truy-vet-luat.md`.
- **Actual:** module `khaiBao` dùng khoá rút gọn `m0xx` và để mã đầy đủ trong `/** … */` phía trên;
  ba module `phanBo` thì dùng **mã đầy đủ** làm khoá (`useChonKyPhanBo.ts:161`
  `t('msg.MSG_PMKT-E-05853_029')`, `chungTuPhanBo/helpers/kiemTra.ts:5-10`). Hai lối trong cùng một PR.
- **Số đo `msg.sh` chạy trên đúng head 07a8fd4** (59 message, tầng `fe`):

  | | OK | LECH | THIEU-VI | CHUA-DAT | THIEU |
  |---|---|---|---|---|---|
  | base `39e0582` | 8 | 0 | 17 | 4 | 30 |
  | head `07a8fd4` | 8 | 0 | 19 | 9 | 23 |

  Độ phủ **có tiến** (THIEU 30 → 23) nhưng **không thêm được một message OK nào**: 19 `THIEU-VI` +
  9 `CHUA-DAT` là do khoá không mang mã, chứ **không** phải thiếu `vi.ts`. Kiểm chéo riêng cho thấy
  vi/en **cân bằng khoá tuyệt đối** (khaiBao 201/201 · cacKy 39/39 · chungTuPhanBo 58/58 · theoNam
  33/33) và mọi mã `MSG_` xuất hiện trong `vi.ts` **nhiều hơn hoặc bằng** `en.ts`.
- **Hậu quả:** với 28/59 message, cổng *"nguyên văn tiếng Việt của BR"* **không chấm được** — lệch
  chữ so với `6.messages.md` sẽ không ai phát hiện.

#### M6 · Mã loại chứng từ lạ rơi âm thầm về "Mua dịch vụ", rồi được GỬI LÊN server
`khaiBao/api/ungVienChungTuGoc.ts:130-135`

```ts
function maLoai(gia: string): MaLoaiChungTuNguon {
  return hopLe.includes(gia) ? (gia as MaLoaiChungTuNguon) : LOAI_CHUNG_TU_NGUON.muaDichVu
}
```

- **Trigger:** BE thêm loại chứng từ nguồn thứ tư (chính ca mà `dongSchema.loaiChungTu: z.string()`
  ở :21 cố ý mở đường cho).
- **Actual:** dòng bị **gán nhãn sai** thành `muaDichVu`, rồi `api/dungPayloadThemMoi.ts:157`
  (`loaiChungTu: row.loaiChungTu ?? ''`) **gửi chính giá trị bịa đó** lên `POST /them-moi`.
- **Expected:** như `giaTriBanDauSua.ts:115-117` đã làm — mã lạ ⇒ `undefined`, và loại dòng khỏi danh
  sách hoặc báo lỗi. **Nguồn thay thế phải do BA chốt**, code không được tự chọn.
- **Hậu quả:** chứng từ nguồn lưu sai loại trong DB, chạy êm cho tới lúc quyết toán. Lớp A
  *"nghiệp vụ tự bịa"*.

### Minor

- **m1 · Nới rộng thêm shape nhóm trung gian.** `features/chiPhiTraTruoc/phanBo/` chứa **ba** màn
  (`cacKy` · `theoNam` · `chungTuPhanBo`) trong **một** element `leaf`, trái §5 luật 2 *"MỘT màn hình =
  MỘT module, không tầng `<nhóm>` trung gian"*. Nợ này **có sẵn ở base**, nhưng PR nhân thêm: file mới
  `phanBo/constants/duongDanApi.ts` và import chéo sub
  `phanBo/cacKy/hooks/useDanhSachCacKy.ts:16` → `'../../theoNam/helpers/namHopLe'` (§5 luật 3 cấm
  `../../` trong module). `lint:boundaries` không bắt vì `phanBo` mới là `leaf` — đúng cảnh báo §3
  của `client/CLAUDE.md` *"lint không chặn, nhưng đó là shape đã bị gỡ"*.
- **m2 · Hai lối import chéo-sub không nhất quán.** `useDanhSachCacKy.ts:16` dùng `../../theoNam/…`
  còn `cacKy/hooks/useThaoTacChungTu.ts:30` dùng `@features/chiPhiTraTruoc/phanBo/theoNam`. Cùng một
  quan hệ, hai cách viết.
- **m3 · Fixture test nằm trong tầng production.** `khaiBao/api/adapterChuaCoBE.ts` (chỉ 4 file
  trong `test/` import) và `phanBo/constants/duLieuMauFigma.ts` (chỉ 1 test import) đã hết vai trò
  nguồn dữ liệu màn — javadoc của cả hai tự khai điều đó. `checklist-fe` §B: *"còn `mock` = còn nợ,
  ghi finding"*. Chỗ đúng là `test/`.
- **m4 · `MAX_TRANG = 50` cắt danh mục âm thầm.** `danhMucTaiKhoan.ts:42` · `danhMucPhanBo.ts:66`.
  Quá 10.000 dòng thì phần dư biến mất, **không lỗi, không cảnh báo**, và là một trong hai đường dẫn
  tới M4.
- **m5 · Mở rộng API `@base` chưa có người tiêu thụ.** `base/components/table/CommonListTable.tsx:652`
  nới `rowUnselectableTooltip` sang `string | ((record) => string | undefined)`, nhưng **cả hai**
  caller đều truyền chuỗi (`banHang/hoaDonBanHang/components/ChonHoaDonGocModal.tsx:358`,
  `khaiBao/components/modal/ChonChungTuGocModal.tsx:338`). Sửa component TIER 2 dùng chung mà nhánh
  mới không chạy ở đâu = mở rộng diff.
- **m6 · Ép kiểu object rỗng.** `khaiBao/hooks/useNguonDanhMucPhanBo.ts:76`
  `const gom = {} as NguonDanhMucPhanBo`. Điền đủ ngay sau đó nên vô hại lúc chạy, nhưng vẫn là `as`
  (§11.1). Thay bằng `Object.fromEntries` + kiểu trả về là xong.
- **m7 · Commit message thiếu `<scope>`.** `feat: init chi phi tra truoc` và
  `fix: sửa một số lỗi CPTT` — chuẩn là `<type>(<scope>): <mô tả>` (luật 8). Mô tả thứ hai
  ("một số lỗi") cũng không cho biết đã sửa gì.

### Nit

- **n1 ·** Trong cùng thư mục `khaiBao/test/`, có test import qua alias tuyệt đối
  (`@features/chiPhiTraTruoc/khaiBao/api/adapterChuaCoBE`) và test khác import tương đối
  (`../api/adapterChuaCoBE`). Chọn một lối.
- **n2 ·** 6 chỗ `toast.info(t('khaiBaoCPTT:chuaDung'))` trong `pages/KhaiBaoCPTTPage.tsx` (nút
  "Phân bổ" trên toolbar :381, `onMoChungTuGoc` :504/:539/:583, nhánh mặc định của
  `onRowActionThem` :427, `onMoForm` :456). Nợ đã biết và có chú thích, nhưng không có mã ticket nào
  đi kèm.

---

## 2. Bốn lớp

| Lớp | Kết quả |
|---|---|
| **A — Cổng cứng** | ⚠ `as` trên dữ liệu API (**M1**, m6). Không secret, không `any`/`@ts-ignore`/`eslint-disable` mới (grep dòng `+` chỉ khớp trong comment), không hardcode text UI, không chạm vùng đóng băng, không commit thẳng `develop`. Hai mục *"nghiệp vụ tự bịa"* → **M4**, **M6** |
| **B — Kiến trúc & 7 lỗi** | ⚠ m1 (#1) · ⚠ **M3** (#4) · ⚠ **M5** (#7). Xem bảng §3 |
| **C — Nghiệp vụ & truy vết** | ⚠ **M2** lệch BR5 · **M4** lệch BR02 epic · `trace.sh` NOT-RUN (không có thư mục spec) · `msg.sh` đã chạy trên head, số đo ở **M5** |
| **D — Vệ sinh diff & Git** | ⚠ m5 (mở rộng diff sang `@base`) · m7 (commit message) · **Cổng cây commit ✅**: `git status --porcelain` rỗng; barrel duy nhất trong diff là `phanBo/theoNam/index.ts` (thêm `danhSachTheoNamCPTTKey`), và kiểm bằng script: **0/89 file có import tương đối không giải được ở head** ⇒ không có bẫy `UNRESOLVED_IMPORT`. Không thấy dấu vết `mv` trần (không có cặp add/delete cùng nội dung) |

## 3. Bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | ⚠ **m1** — `phanBo/` là tầng nhóm trung gian, PR thêm file + import `../../` vào đó. Gốc bốn module đều **chỉ có `index.ts`** (đã kiểm `git ls-tree`), mọi lớp `api/ components/ constants/ fields/ helpers/ hooks/ i18n/ pages/ test/` đặt đúng ngăn |
| 2 | Không đánh lại version migration | ✅ **N/A** — diff FE thuần, không file nào trong `db/migration` |
| 3 | Chưa test lại sau khi merge | ✅ **N/A kèm số đo** — `git rev-list --count 39e0582..origin/develop` = **0** (merge-base *là* tip develop); `comm -12` hai danh sách file = **0 file giao nhau** |
| 4 | Code chưa tối ưu / N+1 | ⚠ **M3**. Ngoài ra ✅: mọi `queryKey` đi qua `createResourceKeys(scope, …)` ổn định; không `useEffect` reset state (mount có điều kiện, đúng luật lint `set-state-in-effect`); `staleTime` chia đúng theo tính chất dữ liệu (danh mục 5 phút vs ứng viên chứng từ `0`) |
| 5 | Chưa tận dụng BaseController / BaseEntity | ✅ **N/A** — không có Java trong diff |
| 6 | Chưa tận dụng base FE | ✅ — dùng `CommonComboGrid` (`ThongTinPhanBoTab.tsx:164`), `CommonSelectBox`, `CommonConfirmModal`, `CommonListTable`, engine `@domain-kit/chungTu` (`khaiBaoCPTTModule`) và `@domain-kit/dinhKem`. Mở rộng engine đi đúng đường điểm-mở-rộng (`confirmTitleKeys`/`successMessageKeys` thuần cộng thêm, mặc định không đổi). Trừ hao m5 |
| 7 | Constant đặt sai chỗ | ⚠ **M5** (mã message không thành key). Còn lại ✅: hằng nghiệp vụ nằm trong `constants/` đúng ba file chuẩn; màu/kích thước Figma gom vào `cacKy/constants/constants.ts` kèm node nguồn thay vì rải trong JSX; `PHAN_BO_CPTT_BASE` gỡ được 3 bản sao đường REST |

## 4. i18n — kiểm riêng (luật 2)

| Phép kiểm | Kết quả |
|---|---|
| Khoá `vi.ts` vs `en.ts` từng module | ✅ cân bằng tuyệt đối: khaiBao **201/201** · cacKy **39/39** · chungTuPhanBo **58/58** · theoNam **33/33** |
| Mọi khoá `t('ns:key')` trong file production của diff có mặt ở **cả** vi và en | ✅ **0 khoá thiếu** |
| Chuỗi tiếng Việt hardcode trong `.ts`/`.tsx` production | ✅ không có — mọi kết quả grep đều rơi vào javadoc/comment |
| Cộng chuỗi thay `t(key, { name })` | ✅ không có; interpolation dùng đúng (`{ maChiPhi }`, `{{soChungTu}}`) |
| Một module = một namespace, đăng ký qua `registerXxxI18n.ts` | ✅ bốn namespace `khaiBaoCPTT` · `phanBoCPTT` · `chungTuPhanBoCPTT` · `phanBoTheoNamCPTT` |
| Mã message làm khoá | ⚠ **M5** |

## 5. Truy vết luật

| Cổng | Kết quả |
|---|---|
| `trace.sh` | **NOT-RUN** — không tồn tại thư mục spec nào cho CPTT trong `docs/doing/` (đã liệt kê: chỉ có các epic Bán hàng / Mua hàng / Bù trừ công nợ). Chưa chạy `/audit-spec` cho epic này. Review là lượt đọc, không dựng đặc tả thay. |
| `msg.sh` | ✅ **đã chạy đúng ref head** (`pmkt-docs/ba/PMKT-E-05853_ChiPhiTraTruoc` · `fe`). Vì `msg.sh` neo `ROOT` theo vị trí script, phải bung snapshot `git archive 07a8fd4 src` vào một root tạm rồi chạy — working tree hiện đứng ở `ee328086` (nhánh `feat/chung-tu-ban-hang-2`, **không** phải hậu duệ của head PR), chạy tại chỗ sẽ cho số của nhánh khác. Số đo ở **M5**. |
| Phủ nhiều epic | Diff chạm ít nhất `PMKT-E-05853` (khai báo) và cụm phân bổ (`PMKT-U-07464/07465`, `PMKT-U-09942`, `PMKT-U-05859/05860`). Chỉ chấm được PYC `PMKT-E-05853`. |

## 6. BR đã đọc / chưa đọc

**Đã đọc** (`br.sh --list` + `br.sh 5 13 25`):

- **BR5** — Hiển thị Combogrid → nguồn của **M2**.
- **BR13** — Hiển thị nút thao tác: 13.2 *"thiếu quyền ⇒ **ẩn**, không disable"*. ✅ code tuân thủ:
  `cacKy/helpers/matranHienThi.ts` gác `hienNutPhanBoNgay` sau `quyen.taoVaTinhLai`, mục ⋮ "Bỏ ghi sổ"
  gác sau `quyen.boGhiSo`; `KhaiBaoCPTTPage.tsx:377,395,408` ẩn hẳn theo quyền thay vì disable.
  `khoaNutPhanBoNgay` là disable theo **thứ tự kỳ** — trục BR13 không phủ, không tính vi phạm.
- **BR25** — Phân quyền (đọc kèm BR13.2 qua tham chiếu chéo).

**Chưa đọc** (được nhắc trong diff, ngoài ngân sách lượt này — nếu cần chấm sâu thì mở tiếp):
BR3 · BR7 · BR8 · BR11 · BR14 · BR15 · BR16 · BR19 · BR21 · BR24 · BR34 · BR37 · BR42 · BR43.

⚠ `BR01`/`BR02`/`BR03`/`BR05`/`BR06`/`BR07`/`BR08`/`BR15` xuất hiện dày trong diff (BR6: 38 lần,
BR01: 26 lần) là **BR nội bộ màn** của `SCR_*` epic CPTT, **không** phải BR chung của
`business_rules.md`. Chưa mở file `SCR_*` tương ứng ở lượt này.

## 7. Lệnh đã chạy

```bash
git rev-parse refs/tmp/pr187-review origin/develop origin/master
git merge-base origin/develop refs/tmp/pr187-review      # = 39e0582 (tip develop)
git merge-base origin/master  refs/tmp/pr187-review      # = 3501108, 242 commit
git log --oneline 39e0582..07a8fd4
git diff --stat|--name-status 39e0582 07a8fd4
git status --porcelain                                    # rỗng
git rev-list --count 39e0582..origin/develop              # 0
comm -12 <(...develop) <(...head)                         # 0 file giao nhau
git ls-files | tr 'A-Z' 'a-z' | sort | uniq -d            # rỗng — không lệch case
git diff … | grep -E 'any|@ts-ignore|@ts-expect-error|eslint-disable'
git diff … | grep -E "^\+.*from '\.\./\.\./"
git ls-tree --name-only 07a8fd4 src/features/chiPhiTraTruoc/**   # gốc module
git grep -n <TabChuaCoDuLieu|hienKhoiUocTinh|rowUnselectableTooltip|…> 07a8fd4 -- src
python3  # 3 script tạm: đối chiếu khoá vi/en · đối chiếu khoá t() · giải import tương đối
sh /tmp/pr187root/docs/rules/msg.sh <PYC> fe   # trên snapshot head 07a8fd4
sh /tmp/pr187base/docs/rules/msg.sh <PYC> fe   # trên snapshot base 39e0582
./docs/rules/br.sh --list ; ./docs/rules/br.sh 5 13 25
```

Tài nguyên lượt này tạo: hai thư mục snapshot tạm dưới `/tmp` và ba script `.py` trong `%TEMP%`.
**Không** tạo worktree, **không** đụng ref của user, **không** sửa/commit/push file nào trong repo
ngoài chính báo cáo này.

## 8. Cổng chưa chạy (chế độ nhanh)

| Cổng | Trạng thái |
|---|---|
| `npm run typecheck` | **NOT-RUN — chế độ nhanh** (nền ~179-192 lỗi, xem MEMORY) |
| `npm run lint` · `lint:boundaries` | **NOT-RUN — chế độ nhanh**. ⚠ lint **không** chặn `any`; kiểm bằng mắt đã làm, kết quả sạch |
| `npx vitest run src/features/chiPhiTraTruoc` | **NOT-RUN — chế độ nhanh**. PR thêm 9 file test mới và sửa 11 file — **chưa file nào được chạy trong lượt này** |
| `npx vite build` | **NOT-RUN — chế độ nhanh** |
| `npm run check:committed` | **NOT-RUN** — cây sạch nên rủi ro thấp; cổng này còn đang cho báo động giả trên Windows |
| Baseline / merge thử | **NOT-RUN** — không cần: 0 file giao nhau với nhánh đích |

## 9. Phần chưa đọc

Đã đọc trọn: 4 file `src/base/**`; toàn bộ file mới của `khaiBao/api` + `khaiBao/helpers` +
`khaiBao/hooks`; `pages/KhaiBaoCPTTPage.tsx`; `phanBo/cacKy/helpers/thuTuKy.ts` +
`constants/constants.ts`; `phanBo/theoNam/hooks/useChonKyPhanBo.ts` + `helpers/namHopLe.ts`;
`phanBo/chungTuPhanBo/helpers/kiemTra.ts`; diff của `matranHienThi.ts` (cả hai bản),
`useThaoTacChungTu.ts`, `useChungTuPhanBo.ts`; toàn bộ 4 cặp `i18n/vi.ts`+`en.ts` (qua trình đối
chiếu khoá).

**Chưa đọc chi tiết** — liệt kê để người merge biết chỗ trống:

- `khaiBao/components/modal/KhaiBaoCPTTModal.tsx` (+208) · `modal/ChonChungTuGocModal.tsx` (+116) ·
  `components/DinhKemTab.tsx` (mới) · `components/ThietLapPhanBoTab.tsx` · `components/tabsXemNhanh.tsx`
- `khaiBao/hooks/useFormKhaiBaoCPTT.ts` (+111) · `helpers/matranThemMoi.ts` (+155) ·
  `helpers/thietLapNhom.ts` · `fields/luoiThietLapPhanBo.tsx`
- `phanBo/cacKy/components/CardKyPhanBo.tsx` · `pages/PhanBoCPTTCacKyPage.tsx` · `pages/phanBoCPTT.css`
- `phanBo/theoNam/components/modal/PopupChonKyPhanBoCPTT.tsx` · `pages/PhanBoCPTTTheoNamPage.tsx`
- **Toàn bộ 20 file `test/`** — chỉ đọc tên, không đọc assert. Chưa xác nhận được test có assert đúng
  expected state hay chỉ đếm lời gọi mock (`review-hanh-vi.md` §Test).
- Tài liệu BA: chưa mở file `SCR_*` nào của `PMKT-E-05853` — mọi trích dẫn BR nội bộ màn trong báo
  cáo này lấy từ **javadoc trong code**, chưa đối chiếu ngược lên tài liệu gốc.

---

## Kết luận

**REQUEST CHANGES** — có 6 Major (**M1** M2 **M3** M4 M5 **M6**), trong đó **M4** và **M6** là
*nghiệp vụ không có nguồn*: nếu BA xác nhận lệch tài liệu thì lên **Blocker** theo Lớp A.

Không có Blocker xác nhận được ở chế độ nhanh. Bốn cổng cứng dễ vỡ nhất đều **sạch**: cây commit
sạch và 0 import gãy, 0 lệch case tên file, 0 file giao nhau với nhánh đích, i18n vi/en cân bằng
tuyệt đối. Chất lượng chú thích và lý-do-thiết-kế trong code ở mức cao bất thường; phần lớn finding
ở trên là *lệch nguồn* hoặc *nới rộng nợ có sẵn*, không phải lỗi cẩu thả.

⚠ **Cổng test/build/typecheck/lint CHƯA CHẠY** — kết luận này chỉ nói về phạm vi đã đọc bằng mắt và
các phép kiểm tĩnh bằng `git`. 9 file test mới của PR chưa được chạy lần nào trong lượt review này.
