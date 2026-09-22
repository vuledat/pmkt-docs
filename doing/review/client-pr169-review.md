# Review PR #169 — repo `client`, nhánh `feat/tscd` → `develop`

- Nguồn diff: ref `review/pr-169` · merge-base `f2372f71179465a2f08a93823d603df0289c386e` · ~130 commit (101 không-merge) · ~250 file đổi.
- Phạm vi: 8 module `src/features/taiSanCoDinh/*` + `_shared`, engine mới `@domain-kit/dinhDangSo`, chỉnh `@base` (entry/table/modal/fields/filter), `@platform/http/apiError`, `app/pages/baoCao`, i18n app.
- Ngày review: 2026-09-06 · quy trình: review-code-fanout (5 lát cắt + phản biện + cổng test riêng).

## 1. Kết luận

**REJECT** — 8 BLOCKER · 7 MAJOR · 9 MINOR · 2 NIT (tổng 26 finding).

Căn cứ: ≥1 Blocker → REJECT (SKILL §5.1). Cổng test cũng FAIL với 1 lỗi quy được cho diff
(`TinhKhauHaoTab1.render.test.tsx` flaky — file mới), tự nó đã đủ REQUEST CHANGES.

Điểm sáng ghi nhận: không có `any`/`@ts-ignore` mới; grid/form đều qua `@base`; phần lớn API mới
có Zod đúng chuẩn; mock của khaiBaoSanLuong + tinhKhauHaoTSCD đã khử sạch; docblock trích nguồn
BA/Matrix rất kỹ. Các Blocker dưới đây đều sửa được khu trú, không phải đập lại kiến trúc.

## 2. BLOCKER (8)

| # | Finding | file:dòng | Rule nguồn | Hậu quả |
|---|---|---|---|---|
| B1 | Engine MỚI `dinhDangSo` đổ file phẳng ra gốc module: `api.ts`, `lamTronTien.ts` (helper), `useSoChuSoThapPhanTienQuyDoi.ts` (hook) nằm cạnh `index.ts`, chỉ `test/` đúng ngăn. Đúng ra `api/api.ts`, `helpers/lamTronTien.ts`, `hooks/useSoChuSoThapPhanTienQuyDoi.ts`. 5 engine cũ phẳng là nợ ghi nhận — code mới phải tuân thủ 100%. | `src/base/domainKit/dinhDangSo/api.ts:1` | client/CLAUDE.md §5 luật cứng 1 (áp cả `src/base/domainKit/**`) · checklist-fe §B | Nhân shape phẳng đã đóng băng vào domainKit; module sau chép engine mới nhất sẽ sai tiếp |
| B2 | 10 import tương đối MỚI vượt ranh giới module với tới `_shared` của domain: `../../../_shared/api/useSoChungTuGoiY` (DieuChuyenThemMoiModal.tsx:45, NgungKhauHaoThemMoiModal.tsx:24), `../../../_shared/components/ThamChieuChungTuTab` + `.../api/thamChieuChungTu` (GhiGiamThemMoiModal.tsx:39-40), `../../../_shared/constants/paths` (TinhKhauHaoModal.tsx:105), `../../_shared/hooks/useLocCotTscd` (5 file `*Tab.tsx`). Code sẵn có cùng domain đều dùng alias `@features/taiSanCoDinh/_shared/...`. | `src/features/taiSanCoDinh/dieuChuyenTSCD/components/modal/DieuChuyenThemMoiModal.tsx:45` (+9 chỗ) | CLAUDE.md gốc luật 4 · client/CLAUDE.md §5 luật cứng 3 · checklist-fe §A | Vi phạm luật cứng "không `../../`"; di chuyển file trong module gãy hàng loạt đường dẫn 3 cấp |
| B3 | Hook mới đọc `sessionStorage` rồi ép mù `parsed as Record<string, ColumnFilterState>` — chỉ kiểm vỏ object, không Zod/type guard cho giá trị bên trong. | `src/features/taiSanCoDinh/_shared/hooks/useLocCotTscd.ts:45` | client/CLAUDE.md §11.2 (BẮT BUỘC parse Zod dữ liệu ngoài) · checklist-fe §A | Bản ghi hỏng / format cũ chui thẳng vào `CommonListTable.columnFilters` + `toWireColumnFilters` → vỡ màn danh sách hoặc gửi filter rác; dùng chung nên hỏng lan cả cụm TSCĐ |
| B4 | Toàn khối `themMoi.msg.*` mới (vi.ts:318–338) lệch nguyên văn 6.messages.md PMKT-E-02578 hàng loạt dù docblock tự nhận "lấy NGUYÊN VĂN": soChungTuTrong≠_005 ("Số BB giao nhận…"), soChungTuTrung≠_006, nguoiGiaoTrong≠_009 ("Người bàn giao"), nguoiNhanTrong≠_010, khongCoChiTiet≠_012, donViNhanTrungHienTai≠_018 (**khác cả NGHĨA**: "khác Đơn vị hiện tại" vs "khác đơn vị bàn giao"), trungMaTaiSan≠_028, chungTuSau≠_103, ngayTruocGhiTang≠_104, trangThaiKhongHopLe≠_107, kyDaKhoaSo≠_108, khongCoQuyen≠_013, loiHeThong≠_014, thanhCong≠_001. Key tự đặt tên thay vì mã `MSG_…` (khaiBaoSanLuong cùng PR làm đúng chuẩn messageCode). | `src/features/taiSanCoDinh/dieuChuyenTSCD/i18n/vi.ts:319` | checklist-fe §F (Blocker khi lệch nguyên văn) + §D · CLAUDE.md §BR (giữ nguyên văn) + luật 9 | User thấy message khác đặc tả BA duyệt, _018 sai điều kiện so sánh; msg.sh chấm LECH toàn bộ; tooling truy vết không đối chiếu được |
| B5 | Key `themMoi.msg.capNhatThanhCong` (MSG_PMKT-E-02578_002) có ở vi.ts:340 và ĐANG dùng tại DieuChuyenThemMoiModal.tsx:240 nhưng KHÔNG có trong en.ts (khối msg kết thúc ở `thanhCong` dòng 297). Đo bằng script flatten: vi=228 key, en=226 key. | `src/features/taiSanCoDinh/dieuChuyenTSCD/i18n/en.ts:297` | CLAUDE.md luật 2 · checklist-fe §F mục 1 | Locale EN sửa phiếu điều chuyển xong hiện raw key / fallback tiếng Việt |
| B6 | Chuỗi UI hardcode tiếng Việt bằng template literal: `` {`(còn ${fmt(conLaiSauLuu)} sau khi lưu)`} `` trong ô "SL còn lại" của lưới nhập — không có key trong vi.ts/en.ts, đúng dạng "cộng chuỗi thay vì `t('key', {…})`". | `src/features/taiSanCoDinh/khaiBaoSanLuong/components/modal/KhaiBaoSanLuongThemMoiModal.tsx:145` | CLAUDE.md luật 2 · checklist-fe §A + §F mục 3 | Không dịch được sang EN, locale EN vẫn thấy tiếng Việt |
| B7 | Label hardcode `` `Tháng ${i + 1}` `` (dòng 223, thangOptions của CommonSelect) và `` `Tháng ${thang}` `` (dòng 444, ReadonlyKy mode edit) trong khi module ĐÃ có key sẵn: vi.ts:28 `thang`, vi.ts:102 `kyValue: 'Tháng {{thang}}/{{nam}}'`. | `src/features/taiSanCoDinh/khaiBaoSanLuong/components/modal/KhaiBaoSanLuongThemMoiModal.tsx:223` | CLAUDE.md luật 2 · checklist-fe §A + §F mục 3 | Dropdown Tháng cứng tiếng Việt ở mọi locale; bản dịch en.ts có sẵn nhưng không bao giờ được dùng |
| B8 | 61/101 commit không-merge sai định dạng bắt buộc `<type>(<scope>): <mô tả>` — câu văn trần ("Name the row that is missing an asset...", "Khử mock trong màn TSCĐ..."); chỉ ~40 commit đúng chuẩn. Khắc phục không cần sửa code: **squash-merge với message chuẩn** hoặc rebase reword trước merge. | `git log f2372f71..review/pr-169` (vd 7a64748c, 06cb3f19, e28103ec, 924d620f, cba11bdb) | CLAUDE.md luật 8 · conventions-chung.md §4.1 | Đổ 61 commit lệch chuẩn vào lịch sử develop, phá lọc theo type/scope và sinh changelog |

## 3. MAJOR (7)

| # | Finding | file:dòng | Rule nguồn | Hậu quả |
|---|---|---|---|---|
| M1 | Gắn SAI mã luật: file/hàm/test tên "Br12", docblock ghi "BR12 (business_rules.md:180-200)" — nhưng dải dòng đó (Phase 1) là "Cảnh báo ghi sổ chi phí SX cho nhiều đối tượng" thuộc **BR6**; BR12 chung là "Trạng thái chứng từ", và chính epic PMKT-E-02600 dùng "BR12" theo nghĩa đó (UC_TinhKhauHaoTSCD_ChinhSua.md:10). Test cùng tên mang mã sai. | `src/features/taiSanCoDinh/tinhKhauHaoTSCD/helpers/idPhieuCanXacNhanBr12.ts:7` | docs/rules/truy-vet-luat.md + BR6 (business_rules.md:180-200) | Truy vết bị đầu độc: grep BR6 không thấy hiện thực, grep BR12 ra logic không liên quan; người sau "đối chiếu BR12" rồi sửa sai hành vi |
| M2 | queryKey lưới "Chọn nguồn" chứa `tuKhoa` bind thẳng vào onChange (dòng 298), không debounce/nút Áp dụng: gõ k ký tự = k lần đổi key = k GET `nguon-hinh-thanh-kha-dung` (endpoint trả full list không phân trang). Phụ: `tuKhoa` chưa trim trong key nhưng queryFn trim → 2 cache entry cho cùng request. Fix: debounce/`useDeferredValue`, hoặc pattern appliedSearch của `useServerListState`; trim trước khi vào key. | `src/features/taiSanCoDinh/ghiTangTSCD/components/modal/GhiTangChonNguonModal.tsx:114` | checklist-fe §E (query thiếu key ổn định → refetch bão; hiệu năng & request thừa) | Bão request: "hóa đơn xăng" = 12 GET full-list; bảng nhấp nháy theo phím; cache phình mỗi tiền tố một entry |
| M3 | "VNĐ" hardcode trong JSX (KyCard.tsx:179, NamCard.tsx:79) — module không có key, trong khi module anh em cùng PR (dieuChinhTSCD/i18n) đặt key và dịch KHÁC giữa locale (vi "VNĐ" / en "VND") → là text cần i18n, không phải ký hiệu bất biến. | `src/features/taiSanCoDinh/tinhKhauHaoTSCD/components/KyCard.tsx:179` | CLAUDE.md luật 2 · checklist-fe §F mục 1 | Locale EN thấy "VNĐ" cạnh số khấu hao, lệch với các màn TSCĐ khác hiển thị "VND" |
| M4 | Magic string nghiệp vụ `'HoatDong'` copy thành literal lần 2, lần 3 trong cùng file (dòng 63, 75; lần 1 sẵn ở dòng 46) không đặt constant — cùng dòng đó lại làm đúng với `LOOKUP_PAGE_SIZE`. | `src/app/pages/baoCao/reportLookupOptions.ts:63` | CLAUDE.md luật 1 · checklist-fe §D mục 3 | BE đổi mã trạng thái phải sửa 3 chỗ; lệch một chỗ là lookup lặng lẽ sai bộ lọc |
| M5 | `'MSG_PMKT-E-03000_103': 'Vượt sản lượng còn lại'` LỆCH nguyên văn 6.messages.md ("Cảnh báo vượt tổng sản lượng"). Comment có ghi lý do (dùng inline cạnh mã tài sản) nhưng là FE tự diễn đạt lại message đã đặc tả, chưa qua BA chốt. | `src/features/taiSanCoDinh/khaiBaoSanLuong/i18n/vi.ts:163` | checklist-fe §D + §F · CLAUDE.md luật 9 | msg.sh fail mã _103; câu cảnh báo popup khác câu BA duyệt |
| M6 | `boGhiSoThanhCong: 'Bỏ ghi sổ chứng từ ghi giảm thành công'` tự chèn "ghi giảm" so với nguyên văn MSG_PMKT-E-02547_080 "Bỏ ghi sổ chứng từ thành công" — dù comment cạnh key trỏ đúng mã _080. | `src/features/taiSanCoDinh/ghiGiamTSCD/i18n/vi.ts:81` | checklist-fe §D + §F · CLAUDE.md §BR | msg.sh cho PMKT-E-02547 fail ở _080 |
| M7 | Commit trộn feat + fix + platform/config, vi phạm "1 commit = 1 ý nghĩa": d0f22f87 (116 file, +14.316 dòng: feat 8 module + fix useT.ts + vite.config.ts — tự khai trong tiêu đề), 924d620f (67 file: khử mock + refactor apiError tầng platform), c39fd624 (82 file), 37bfdd38 (63 file). | commit `d0f22f87`, `c39fd624`, `924d620f`, `37bfdd38` | conventions-chung.md §4.1 ("Không trộn feat + refactor…") | Không revert/cherry-pick riêng phần platform khỏi khối 14k dòng; bisect hồi quy đổ về một commit 116 file |

## 4. MINOR (9)

| # | Finding | file:dòng | Rule nguồn | Ghi chú |
|---|---|---|---|---|
| N1 | `envelopeOf` mới `JSON.parse` rồi ép `as EnvelopeBody`, không Zod. MINOR vì mọi field optional + optional chaining downstream, và trùng pattern `bodyOf` sẵn có cùng file (nợ baseline). Rủi ro còn lại: `message` không phải string → `raw?.replace` ném TypeError ngay trong đường xử lý lỗi, nuốt thông báo gốc. | `src/platform/http/apiError.ts:124` | client/CLAUDE.md §11.2 · checklist-fe §A | |
| N2 | `fetchLoaiTaiSanOptions` (dòng 61) + `fetchBoPhanOptions` (dòng 73) tin shape chỉ bằng generic `http.get<…>`, không Zod — trong khi api mới khác cùng PR (taiSanLookup.ts, catalogLookup.ts) đều Zod. MINOR vì lặp pattern fetcher sẵn có cùng file, blast radius hẹp. | `src/app/pages/baoCao/reportLookupOptions.ts:61` | client/CLAUDE.md §11.2 · checklist-fe §A | BE đổi tên field → option rỗng âm thầm |
| N3 | Gỡ `'kiemKe'` khỏi ENABLED_TABS khoá tab Kiểm kê (PMKT-E-02588). Phản biện đã hạ mức: màn chạy 100% mock, quy ước ENABLED_TABS = "tab đã có route thật" đã tài liệu hoá sẵn tại merge-base + design doc §10, lý do ĐÃ ghi docblock. Giữ MINOR để **xin BA xác nhận** thay đổi hiển thị. | `src/features/taiSanCoDinh/_shared/components/TaiSanCoDinhTabs.tsx:67` | CLAUDE.md luật 9 + Cổng đặc tả luật 2 | Test được viết lại ghim hành vi này |
| N4 | `lamTronTien` cục bộ hardcode scale 2 cho "Mức KH tháng/đơn vị SP Sau ĐC" thay vì đọc `soChuSoThapPhanTienQuyDoi` (hook cùng PR dựng sẵn; các helper anh em đều nhận soChuSo). Phản biện đã hạ mức: field display-only — `toChiTietRequest` KHÔNG gửi lên BE, DB không có cột → không thể lệch FE↔BE; chỉ lệch cosmetic BR7.2 khoản 1 với tenant scale 0; lý do có trong docblock. | `src/features/taiSanCoDinh/dieuChinhTSCD/components/modal/DieuChinhThemMoiModal.tsx:196` | BR7.2 khoản 1-2 | |
| N5 | Nhánh `tongGoc === 0` dồn TOÀN BỘ `tongMoi` vào dòng ĐẦU — comment tự nhận quyết định riêng, ngược quy ước "dồn phần dư vào dòng CUỐI" của BR_GTTSCD_20 mà chính docblock trích; không có nguồn BE mirror cho ca này. | `src/features/taiSanCoDinh/tinhKhauHaoTSCD/helpers/chiaLaiTheoTiTrong.ts:32` | BR_GTTSCD_20 (SCR_GhiTangTSCD_ThemMoi:293) + CLAUDE.md luật 9 | Mọi dòng gốc = 0 + user sửa tổng → preview FE có thể khác BE lưu |
| N6 | `Math.round(n*heSo)/heSo` là HALF_UP về +∞, không phải Commercial Rounding (HALF_UP xa 0) như BR7.2 khoản 2 + `setScale(HALF_UP)` BE: `lamTronTien(-0.5, 0) = 0` vs BE `-1`. Docblock có ghi giới hạn "cho tiền ≥ 0" nhưng hàm export chung `@domain-kit`; Điều chỉnh TSCĐ vốn có chênh lệch âm. | `src/base/domainKit/dinhDangSo/lamTronTien.ts:10` | BR7.2 khoản 2 | Consumer tương lai truyền tiền âm lệch 1 đơn vị tại biên .5, không guard nào |
| N7 | queryFn "Số chứng từ gợi ý" (staleTime 0) gộp luôn `loaiChungTuApi.listAll({pageSize:200})` drain full catalog chỉ để đổi mã cố định → UUID; mỗi lần mở popup = 1 request catalog thừa. Cùng module có mẫu tránh được: `tinhKhauHaoTSCD/api/catalogLookup.ts` truyền thẳng `maLoaiChungTu`. Shape lặp ở ghiGiamTSCD + dieuChinhTSCD `masterDataLookup.ts`. | `src/features/taiSanCoDinh/_shared/api/useSoChungTuGoiY.ts:77` | checklist-fe §E (request thừa) | Fix: tách code→id sang cache staleTime dài, hoặc truyền mã trực tiếp |
| N8 | `'MSG_PMKT-E-03000_204'` không tồn tại trong 6.messages.md của PMKT-E-03000 (bảng dừng _201/_202 rồi nhảy _301…) — mã không có nguồn dù comment claims "Nguyên văn". Hoặc doc thiếu cập nhật hoặc FE tự đặt mã → hỏi BA. | `src/features/taiSanCoDinh/khaiBaoSanLuong/i18n/vi.ts:170` | checklist-fe §D mục 2 · CLAUDE.md luật 9 | |
| N9 | 5 nhánh con đã merge đặt tên theo username (`truongnq98/tscd-danh-sach`…) thay vì `loại-nhánh/tên-mô-tả`. Nhánh chính `feat/tscd` đúng chuẩn; tên nhánh con chỉ còn trong tiêu đề merge commit — squash-merge PR thì hậu quả tự biến mất. | merge commit `01c8719e`, `ba4b6778`, `52188eee`, `eba2a7e3`, `fd576e7b` | conventions-chung.md §4.3 + CLAUDE.md luật 8 | |

## 5. NIT (2)

| # | Finding | file:dòng | Rule nguồn |
|---|---|---|---|
| T1 | Diff sửa đúng dòng import `from '../../../utils'` (thêm `foldAccent`) nhưng giữ đường dẫn tương đối thay vì chuyển `@core` — §10 ghi "đụng file nào sửa file đó". | `src/base/components/filter/TimeRangeFields.tsx:18` | client/CLAUDE.md §10 · CLAUDE.md luật 4 |
| T2 | File .tsx mới tên camelCase (`themMoiFields.tsx`, `cotKhauHao.tsx`) trong khi quy ước ".tsx PascalCase". Chỉ NIT: 34 file fields/*.tsx camelCase có sẵn trước diff; mẫu chungTuBanHang né bằng fields .ts. | `src/features/taiSanCoDinh/dieuChuyenTSCD/fields/themMoiFields.tsx:1` | CLAUDE.md §Quy ước đặt tên · checklist-fe §G |

## 6. Bảng 7 lỗi hay gặp (lớp B)

| # | Lỗi hay gặp | Kết quả | Finding |
|---|---|---|---|
| 1 | Sai kiến trúc thư mục | ❌ | B1 — engine `dinhDangSo` đổ file phẳng ra gốc module. (Các module features còn lại đặt đúng ngăn api/components/modal/fields/helpers/hooks/constants/test) |
| 2 | Không đánh lại version migration | ✅ không áp dụng | Repo `client` không có db/migration. (Các finding Git gắn nhãn lát cắt này — B8, M7, N9 — báo ở lớp D, không phải lỗi migration) |
| 3 | Chưa test lại sau khi merge code | ✅ | Độ tụt `review/pr-169..origin/develop` = 0, file giao nhau = rỗng → cổng test trên nhánh PR là đủ (lay-diff §4) |
| 4 | Code chưa tối ưu, tiềm ẩn N+1 / request thừa (FE) | ❌ | M2 — bão request theo phím gõ ở GhiTangChonNguonModal; N7 — drain full catalog mỗi lần mở popup (x3 module). Không có N+1 dạng gọi API trong vòng lặp per-row (đã soát SoTienKhauHaoCell, GhiTangSoTienPhanBoCell — react-query dedupe đúng) |
| 5 | Chưa tận dụng BaseController / BaseEntity (BE) | ✅ không áp dụng | Diff chỉ thuộc repo client |
| 6 | Chưa tận dụng base FE | ✅ | Mọi grid mới qua CommonListTable / CommonEditableGrid / CommonGroupedEditableGrid; không Table AntD trần; không axios/fetch trần; http qua @platform |
| 7 | Constant đặt sai chỗ / mã MSG_ không thành hằng số-key | ❌ | M4 — 'HoatDong' literal x3; B4 — key msg tự đặt tên thay vì mã MSG_ (dieuChuyenTSCD); cùng cụm i18n: B5, B6, B7, M3, M5, M6, N8 |

## 7. Nghiệp vụ không có nguồn

- **N5** (`chiaLaiTheoTiTrong.ts:32`): ca `tongGoc === 0` dồn vào dòng đầu là quyết định riêng của FE, ngược quy ước dồn dòng cuối của BR_GTTSCD_20 — cần BA/BE chốt.
- **N8** (`khaiBaoSanLuong/i18n/vi.ts:170`): mã `MSG_PMKT-E-03000_204` không có trong 6.messages.md — cần xác nhận doc thiếu hay FE tự đặt.
- **N3** (`TaiSanCoDinhTabs.tsx:67`): khoá tab Kiểm kê theo quy ước kỹ thuật có sẵn (tab chưa có route/BE thật) — hợp lệ về quy ước repo nhưng nên báo BA vì thay đổi hiển thị.
- Các điểm đã soi nhưng KHÔNG lập finding vì có nguồn/đã khai lệch đúng quy trình: ghiGiamTSCD bỏ nút "Lưu" riêng (trích SCR bảng Chức năng + BE POST luôn DA_GHI_SO, có pin test nêu lý do); ô khoá tab Thời gian đè Matrix theo BA chốt A3; `slTongSanLuong` show→disable có 3 nguồn thống nhất; khoá `thaoTac` theo `cheDo='xem'` khớp BR12; `canhBaoNamTuongLai` có đánh dấu [CXM] chờ chốt.

## 8. Kết quả cổng lệnh thật (agent test riêng — dán nguyên trạng)

**Kết quả: FAIL** (như-đã-chạy: có treo + có file đỏ). **Sau khi trừ baseline, phần quy cho diff chỉ còn 1 mục.**

- Test sau merge: **KHÔNG ÁP DỤNG** — `git rev-list --count review/pr-169..origin/develop` = 0 (độ tụt 0, không có gì để merge thử).
- `npx vite build` (worktree review): `✓ built in 2.21s` — exit 0.
- Vitest theo 10 lô trên `review/pr-169` (~2.290 test):
  - ghiGiam 5/5 file · 43/43 pass · dieuChinh 9/9 · 199/199 · dieuChuyen 10/10 · 134/134 · ngungKhauHao 11/11 · 68/68 · khaiBao+kiemKe+_shared 5/5 · 49/49 · platform+baoCao 5/5 · 84/84
  - tinhKhauHao: `Test Files 1 failed | 18 passed` · `Tests 1 failed | 183 passed`
  - base-components: `2 failed | 59 passed` (846 test) · base-domainKit: `2 failed | 45 passed` (621 test)
  - ghiTang: lô gộp EXIT=124; chạy từng file 22/24 pass, `GhiTangThemMoiModal.render.test.tsx` treo (EXIT=124), `ghiTangTscd.render.test.tsx` còn 1 fail ("Task 10")

**Lỗi quy được cho diff (duy nhất):**
- `src/features/taiSanCoDinh/tinhKhauHaoTSCD/test/TinhKhauHaoTab1.render.test.tsx` (file MỚI) — **FLAKY**: fail 2/3 lần khi chạy cùng module ("AC #9 — xóa 1 trong N>1 TSCĐ", "BR11 — nút Xóa ở dòng con" timeout 5000ms), pass khi chạy một mình. Cổng chuẩn `npx vitest run src/features/taiSanCoDinh/tinhKhauHaoTSCD` đỏ vì file này; không có baseline để trừ vì file mới.

**Đã trừ baseline (fail y hệt tại merge-base f2372f71, KHÔNG tính cho diff):**
1. `GhiTangThemMoiModal.render.test.tsx` treo vô hạn (EXIT=124 cả hai phía; chính nó làm 2 lần chạy gộp đầu treo >60 phút — ai chạy full suite sẽ gặp).
2. `ghiTangTscd.render.test.tsx` › "Task 10 — saving qua modal… reuses the AC #12 reload callback" timeout cả hai phía.
3. `stickyHaiTang.test.ts` › "COMPACT: mốc bám của hàng con" AssertionError cả hai phía.

**Flake do máy tải nặng lúc chạy lô** (pass khi chạy lại cô lập trên chính review/pr-169, pass ở baseline): CommonListTable "Case 3: full CRUD" · catalog "behavior.system hides add and delete" · catalogGates "rowReadOnly rows HIDE" · ghiTangTscd.render "AC #12 — Làm mới".

**Không chạy:** `npm run check:committed` (lệnh cấm theo memory — ~5133 báo động giả Windows); các lệnh nặng `npm run test`/`lint` full (baseline đỏ nền có sẵn, đã đo qua worktree merge-base thay thế).

## 9. trace.sh / msg.sh

- `trace.sh`: **KHÔNG CHẠY ĐƯỢC** — `docs/doing/` không có thư mục `*-spec` nào cho các epic TSCĐ (02547/02569/02578/02588/02600/02606/03000/02535). Toàn bộ truy vết đối chiếu tay qua trích dẫn docblock (diff trích nguồn kỹ: Matrix dòng cụ thể, mã MSG_, câu trả lời BA A3/A5/A6/A7 ngày 2026-08-25). Khuyến nghị: chạy `/audit-spec` bổ sung rồi `/verify-spec` cho cụm epic TSCĐ.
- `msg.sh`: **KHÔNG CHẠY** — cần chỉ định từng PYC, PR phủ ~7 epic. Kết luận LECH ở B4, M5, M6 dựa trên đối chiếu tay từng câu với 6.messages.md/7.messages.md Phase 1. Hai epic 02606, 02569 và các mã 02600 khớp verbatim (không finding).

## 10. BR đã đối chiếu (br.sh, bản Phase 1)

1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 24, 26, 27, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 48, 49.

## 11. Ghi chú ngoài phạm vi tính điểm

- `src/features/taiSanCoDinh/kiemKe/api/mockData.ts` vẫn còn (module còn UI-mock, PR không chạm) — ngoài diff, không thành finding.
- `dieuChuyenTSCD/i18n/vi.ts:101` `modal.comingSoon` chỉ có ở vi (thiếu en) — tồn tại từ TRƯỚC merge-base, nợ baseline.
- Barrel "xanh local đỏ deploy": đã duyệt toàn bộ import tương đối của các `index.ts` (base, domainKit, dinhDangSo, chungTu, icons) trên cây commit `review/pr-169` bằng `git cat-file` — không import nào trỏ file thiếu.
- Cast `as unknown as` chỉ xuất hiện trong file test, trùng pattern mock của mẫu tham chiếu chungTuBanHang/test — không finding.

## 12. Dọn dẹp

- Worktree `../review-test-pr169`: đã gỡ (agent test tự dọn, junction node_modules gỡ trước).
- Worktree `review-merge-*`: không tồn tại (độ tụt 0, không merge thử).
- Nhánh tạm `review/pr-169`: **CHƯA xoá** — lệnh `git branch -D review/pr-169` bị permission classifier từ chối (coi là ref dùng chung của orchestrator). Orchestrator/user tự xoá khi đóng phiên review: `cd client && git branch -D review/pr-169`.
- Worktree `client-mb-review` (baseline) và `client-pr170-review` thuộc phiên review khác — giữ nguyên.
