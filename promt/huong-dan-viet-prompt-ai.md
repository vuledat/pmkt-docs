# Hướng dẫn viết prompt cho AI gen code — PMKT

> **Dành cho:** dev mới vào dự án, cần dùng AI Agent (Claude Code / Copilot / Cursor…) để sinh code
> **đúng quy tắc kiến trúc** và **đủ nghiệp vụ theo phiếu yêu cầu (PYC)** ngay từ ngày đầu.
>
> **Không thay thế:** [CLAUDE.md](../../CLAUDE.md) · [docs/conventions.md](../conventions.md) ·
> [cell-app/CLAUDE.md](../../cell-app/CLAUDE.md) · [client/CLAUDE.md](../../client/CLAUDE.md).
> Tài liệu này chỉ dạy **cách gói các quy tắc đó vào prompt** để AI không đi lệch.
>
> **Nguyên tắc gốc:** AI không tự thiết kế lại kiến trúc. AI là **người triển khai trong khung đã có**.
> Prompt của bạn chính là cái khung đó — prompt thiếu ràng buộc thì AI **tự bịa ra ràng buộc**.

---

## 1. Ba sự thật phải nhớ trước khi gõ prompt

| # | Sự thật | Hệ quả lên cách viết prompt |
|---|---|---|
| 1 | AI **không tự đọc hết** tài liệu BA. Nó chỉ đọc file bạn trỏ đường dẫn. | Phải liệt kê **đường dẫn tuyệt đối/tương đối từ repo root** của UC, SCR, messages, ma trận. |
| 2 | AI **mặc định copy pattern** từ file nó grep thấy đầu tiên — rất dễ rơi vào vùng đóng băng (`master_data/**`, `client/src/legacy/**`) hoặc nhánh chết. | Phải ghi rõ **module mẫu được phép tham chiếu** và **vùng cấm**. |
| 3 | Tài liệu epic **chỉ mô tả phần đặc thù**; phần chung nằm ở `business_rules.md` (BR1…BR46). Epic không nhắc BR ≠ được bỏ BR. | Phải liệt kê **danh sách BR** theo bảng tra cứu trong `../../CLAUDE.md`. |

---

## 2. Quy trình bắt buộc — 2 pha, không được gộp

```
PYC / tài liệu BA
      │
      ├── PHA 1 · PROMPT PLAN ──► AI xuất 1 file .md kế hoạch trong docs/doing/
      │                            (theo mẫu docs/_bieu-mau-plan-api.md)
      │                            → Dev + BA review, chốt các câu hỏi mở
      │
      └── PHA 2 · PROMPT CODE ──► AI code theo đúng plan đã chốt
                                   → chạy cổng nghiệm thu → PR
```

**Vì sao không được gộp:** nếu bảo AI "code luôn", nó sẽ vừa đoán schema DB, vừa đoán hợp đồng API,
vừa đoán quy tắc nghiệp vụ — và bạn chỉ phát hiện sai sau khi đã có 30 file. Pha 1 rẻ hơn pha 2
khoảng một bậc độ lớn.

**Ngoại lệ duy nhất được gộp:** sửa lỗi nhỏ trong 1–2 file đã biết chính xác vị trí.

---

## 3. Bộ khung 8 khối của một prompt tốt

Mọi prompt (BE lẫn FE) đều nên có đủ 8 khối. Thiếu khối nào thì ghi rõ "không áp dụng — <lý do>",
đừng bỏ trống.

| # | Khối | Trả lời câu hỏi | Ví dụ |
|---|---|---|---|
| **B1** | **Nhiệm vụ + phạm vi** | Làm gì, **KHÔNG** làm gì | "Chỉ luồng Thêm mới. Không đụng Sửa/Xóa/Ghi sổ." |
| **B2** | **Nguồn nghiệp vụ** | Đọc tài liệu nào | `4.usecases/ThemMoi/`, `5.screens/SCR_*.md`, `6.messages.md`, `Matrix/**` |
| **B3** | **BR bắt buộc** | Quy chuẩn chung nào áp | "BR3, BR13.2, BR14, BR15, BR24, BR43" |
| **B4** | **Khung kiến trúc** | Code đặt ở đâu, kế thừa gì | module đích + base class / cây thư mục `<module>/` |
| **B5** | **Vùng cấm + change policy** | Được sửa tới đâu | `master_data/**` cấm · `core/`, `accounting_core/` read-only · mức A/B/C |
| **B6** | **Output mong đợi** | Sản phẩm là gì | 1 file plan `.md` / danh sách file code / migration / test / Postman |
| **B7** | **Cổng nghiệm thu** | Lệnh nào phải xanh | `./gradlew unitTest` · `npm run typecheck && lint && lint:boundaries && test` |
| **B8** | **Cách báo cáo** | Báo lại thế nào | "Liệt kê BR đã áp dụng / chưa đạt + lệnh nào đỏ (dán output thật)" |

> 📌 **Mẹo:** dán nguyên khối B3–B5 vào mọi prompt của cùng một epic. Chúng gần như không đổi giữa
> các use case, chỉ B1/B2/B6 thay.

---

## 4. Template prompt — Backend (`cell-app`)

### 4.1 PHA 1 — Prompt sinh kế hoạch

```md
Nhiệm vụ: lập KẾ HOẠCH triển khai API cho use case <TÊN UC> thuộc PYC <PMKT-E-xxxxx_...>.
CHƯA code — pha này chỉ xuất tài liệu để dev và BA review.

## Nguồn nghiệp vụ (đọc hết trước khi viết plan)
- pmkt-docs/ba/<EPIC>/4.usecases/<UseCase>/UC_*.md + AD_*.puml
- pmkt-docs/ba/<EPIC>/5.screens/SCR_*.md
- pmkt-docs/ba/<EPIC>/6.messages.md        ← lấy messageId, KHÔNG bịa mã mới
- pmkt-docs/ba/<EPIC>/3.crud-matrix.puml
- pmkt-docs/ba/Common/business_rules.md    ← các BR: <liệt kê đích danh, vd BR3, BR7, BR15, BR19, BR20, BR28, BR46>

## Khung kiến trúc bắt buộc
- Module đích: cell-app/src/main/java/vn/dopai/pmkt/cell/<domain>/  (cấu trúc modulith có internal/)
- Kế thừa luồng base đã xây:
  - cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/**
  - cell-app/src/main/java/vn/dopai/pmkt/cell/core/**
- Module mẫu được phép tham chiếu: chung_tu_ban_hang/, accounting_core/, integration_ops/
- Phân tầng: Controller → Service → Repository → Entity. Response bọc ApiResponse<T>.
- Quy ước bổ sung: docs/cell-app-ai-agent-template.md, docs/conventions.md, cell-app/CLAUDE.md

## Vùng cấm / change policy
- CẤM đọc và CẤM lấy làm mẫu: cell-app/**/master_data/**
- core/** và accounting_core/** là READ-ONLY. Nếu bắt buộc phải sửa → DỪNG, xuất impact analysis
  (mức C) chứ không tự sửa.
- Mức thay đổi mặc định: <A feature-only | B feature+integration>

## Output — 1 file duy nhất
Ghi ra: docs/doing/<ten-nghiep-vu>-plan.md
Theo ĐÚNG biểu mẫu docs/_bieu-mau-plan-api.md (giữ nguyên đánh số mục 0→20).
Yêu cầu chất lượng:
- Mọi khẳng định về code/DB phải trỏ được `file:dòng` thật (đã grep, không suy đoán).
- §9 thiết kế DB phải đủ: kiểu, NULL, default, AI GHI (client gửi / server tính / base tự quản),
  precision-scale theo BR7. §10 migration chỉ là bản dịch của §9 sang SQL.
- Mỗi lựa chọn thiết kế kèm "vì sao KHÔNG chọn phương án kia".
- §12: liệt kê điểm mâu thuẫn tài liệu BA, trích bằng chứng CẢ HAI phía để BA phán quyết.
- §13: vẽ luồng xử lý bằng mermaid sequenceDiagram cho luồng chính.

## Báo cáo
Kết thúc, liệt kê: BR đã áp dụng · câu hỏi đang chặn BA · số migration mới dự kiến
(kiểm số hiệu lớn nhất hiện có trong cell-app/src/main/resources/db/migration/ và cả các plan
đang giữ chỗ trong docs/doing/).
```

### 4.2 PHA 2 — Prompt code

```md
Nhiệm vụ: implement theo kế hoạch ĐÃ CHỐT tại docs/doing/<ten-nghiep-vu>-plan.md.

## Ràng buộc
- Bám đúng §4 (hợp đồng API), §9 (DB), §10 (migration), §15 (messageId) của plan.
- Nếu thực tế code lệch plan → DỪNG, báo chỗ lệch và đề xuất, không tự đổi thiết kế.
- Không refactor code cũ ngoài phạm vi. Không mở rộng diff.
- Vùng cấm và change policy giữ nguyên như pha 1.

## Thứ tự thực hiện
migration + hằng → model/enum → entity → repository → service (+ unit test) → controller → Postman

## Cổng nghiệm thu (chạy thật, dán output)
```bash
cd cell-app && ./gradlew unitTest
```
Máy chưa cài Docker thì `./gradlew build` sẽ đỏ ở các test Testcontainers — báo trung thực lane nào
xanh, lane nào bị chặn bởi môi trường, đừng ghi "đã xong".

## Báo cáo hoàn thành
- Bảng file mới / file sửa.
- BR đã áp dụng · BR chưa đạt (kèm lý do).
- Checklist §19 của plan, mục nào chưa đạt phải nói rõ.
```

---

## 5. Template prompt — Frontend (`client`)

```md
Nhiệm vụ: xây màn hình <TÊN MÀN> theo PYC <PMKT-E-xxxxx_...>.

## Đường dẫn truy cập trong app
<Menu cấp 1> → <Menu cấp 2> → <hành động mở màn>
(vd: Bán hàng → Chứng từ bán hàng → nút "Thêm" → màn Thêm chứng từ bán hàng)

## Nguồn nghiệp vụ
- pmkt-docs/ba/<EPIC>/5.screens/SCR_*.md          ← bố cục, trường, validate
- pmkt-docs/ba/<EPIC>/4.usecases/<UseCase>/       ← luồng
- pmkt-docs/ba/<EPIC>/Matrix/**/*_MaTranAnHien.md ← ma trận ẩn/hiện trường & nút
- pmkt-docs/ba/<EPIC>/6.messages.md               ← messageId cho toast/cảnh báo
- pmkt-docs/ba/Common/business_rules.md — BR: <vd BR3, BR5, BR6, BR7, BR13.2, BR14, BR15, BR21, BR24, BR26, BR43>
- Figma: <link + node-id>   (nếu chỉ dùng làm tham chiếu thị giác thì nói rõ: token/spacing lấy
  theo @base, KHÔNG hardcode giá trị px từ Figma)

## Khung kiến trúc bắt buộc — đọc trước khi gõ dòng đầu tiên
- docs/fe-khung-kien-truc-chuan.md (SSOT: client/CLAUDE.md, luật tầng ép ở client/eslint.boundaries.js)
- Code mới đặt tại: client/src/features/<domain>/<nhóm>/<module>/ theo đúng cây chuẩn
  (index.ts · <Tên>Page.tsx · types.ts · constants.ts · api/ · components/ · fields/ · helpers/
   · hooks/ · i18n/ · test/). Chỉ 4 file được nằm ở gốc module.
- Màn chứng từ → dùng engine @domain-kit/chungTu bằng descriptor, KHÔNG dựng lại khung.
- Component: tái sử dụng barrel @base (client/src/base/index.ts — ~130 component/21 họ).
  Thiếu prop nhỏ → thêm prop vào @base, KHÔNG copy component ra feature.
- Import bằng alias @core/@base/@platform/@domain-kit/@features/*/@app/*, chỉ đi xuống tầng dưới.
- Mọi dữ liệu từ API phải Zod parse. Không any, không @ts-ignore.
- Mọi chuỗi UI phải có key i18n ở CẢ vi.ts và en.ts; text theo BR giữ NGUYÊN VĂN tiếng Việt của BR.

## Vùng cấm
- client/src/legacy/**  — không đọc, không lấy làm mẫu, không mở màn mới.
- Nhánh features/ không có trong client/src/app/router/RootRoutes.tsx là nhánh chết — không tham chiếu.

## Sản phẩm bàn giao
Đủ 15 artefact theo §5 docs/fe-khung-kien-truc-chuan.md, gồm cả permissions.ts, paths.ts,
routes.tsx và nối tay vào RootRoutes.tsx (không có cơ chế tự nạp route).

## Cổng nghiệm thu (chạy thật, dán output)
```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test
```
Repo có baseline đỏ sẵn — luật: không làm xấu hơn baseline, file mình chạm phải sạch 0 lỗi,
không dùng eslint-disable để dập lint.

## Báo cáo hoàn thành
Bảng file mới/sửa · BR đã áp dụng và BR chưa đạt · lệnh nào đỏ (dán output thật).
```

---

## 6. Phân tích 2 prompt mẫu hiện có — sửa gì để dùng lại được

### 6.1 Prompt BE mẫu

> "Kế hoạch thực hiện để phát triển API hoàn thành mục …/4.usecases/ThemMoi, …/5.screens/SCR_CTBH_ThemMoi.md
> trong phiếu yêu cầu … Hãy xuất chi tiết kế hoạch thực hiện, luồng xử lý ra 1 file .md trong docs để
> dev và ba review trước. Code luồng xử lý cần kế thừa luồng base đã được xây dựng trong accounting_core,
> core. Đảm bảo tuân thủ khung kiến trúc của BE"

| Điểm | Đánh giá |
|---|---|
| ✅ Tách pha plan trước khi code | Đúng nguyên tắc §2 |
| ✅ Trỏ đích danh UC + SCR + chỉ định base để kế thừa | Đủ B2 và một phần B4 |
| ❌ Không nhắc `6.messages.md` | AI sẽ **bịa messageId** — FE tra không ra |
| ❌ Không liệt kê BR | Phần nghiệp vụ chung (BR7 precision, BR19 chống trùng, BR20 cấp số, BR28 multi-tenant, BR46 trường hệ thống) rơi rụng |
| ❌ "xuất ra 1 file .md trong docs" — không nói theo mẫu nào, không nói thư mục nào | Kết quả không so sánh được giữa các PYC. Đúng ra: `docs/doing/<ten>-plan.md` theo `docs/_bieu-mau-plan-api.md` |
| ❌ Không khai vùng cấm / change policy | AI có thể tự sửa `accounting_core/` (mức C) mà không báo |
| ❌ Không có cổng nghiệm thu & cách báo cáo | Không có cơ sở nghiệm thu |

→ **Bản viết lại:** dùng nguyên template §4.1, điền `<EPIC>` = `PMKT-E-06194_ChungTuBanHang`,
`<UseCase>` = `ThemMoi`, `<domain>` = `chung_tu_ban_hang`.

### 6.2 Prompt FE mẫu

> "Build màn hình Thêm chứng từ bán hàng theo link Figma …, dùng ngôn ngữ theo project quy định,
> tái sử dụng component trong src/components/ui: refer /Users/leminhanh/Desktop/PMKT/pmkt-dev/client-v2/src/base/components
> … Chức năng: ghi rõ các bước truy cập … Ref ma trận ẩn hiện: ba/…/Matrix/…"

| Điểm | Đánh giá |
|---|---|
| ✅ Có Figma + node-id, có ma trận ẩn/hiện, có đường dẫn truy cập màn | Ba thứ FE hay thiếu nhất |
| 🔴 **`src/components/ui` không tồn tại** trong repo này | Thư mục đúng là `client/src/base` (barrel `@base`). Prompt sai đường dẫn ⇒ AI tự tạo thư mục mới, vi phạm luật tầng |
| 🔴 **`/Users/leminhanh/Desktop/...` là đường dẫn máy người khác** | AI không đọc được. Mọi đường dẫn phải **tương đối từ repo root** |
| ❌ Không nói code đặt ở đâu | Thiếu B4 — AI rất dễ đẻ file vào `src/legacy/` hoặc nhánh chết |
| ❌ Không nhắc engine `@domain-kit/chungTu` | Màn chứng từ mà không dùng engine ⇒ viết lại khung lọc/phân trang/toast đã có |
| ❌ Không nhắc i18n vi+en, Zod, cấm `any` | Ba luật cứng hay bị vi phạm nhất ở FE |
| ❌ Không nhắc `permissions.ts` / `paths.ts` / nối `RootRoutes.tsx` | Màn build xong **không truy cập được** |
| ❌ "giữ đúng spacing/token" nhưng không nói token lấy từ đâu | Phải nói rõ: token theo `@base`/theme, không hardcode px từ Figma |
| ❌ Không có cổng nghiệm thu | — |

→ **Bản viết lại:** dùng nguyên template §5, thay `src/components/ui` → `@base`
(`client/src/base/index.ts`), bỏ đường dẫn máy cá nhân.

---

## 7. Bảng tra nhanh — PYC của bạn thuộc loại nào thì nhét BR nào vào prompt

Trích từ `CLAUDE.md`; dán đúng dòng tương ứng vào khối **B3**.

| Loại việc | BR phải ghi vào prompt |
|---|---|
| Màn danh sách (grid) | BR1 · BR2 · BR11 · BR13.1 · BR30 · BR31 · BR32 · BR38 · BR39 · BR44 · BR45 |
| Danh mục dạng cây | BR2 · BR22 · BR40 · BR23 |
| Form nhập liệu / popup | BR3 · BR13.2 · BR14 · BR15 · BR24 · BR34 · BR43 |
| Combogrid / chọn dữ liệu | BR5 · BR6 · BR10 |
| Chứng từ & hạch toán | BR4 · BR9 · BR12 · BR17 · BR33 · BR36 · BR37 · BR41 · BR42 |
| Số liệu / tiền tệ | BR7 · BR18 |
| Ngày tháng / kỳ báo cáo | BR8 |
| Thông báo & cảnh báo | BR16 · BR26 · BR27 |
| Entity / DB / API | BR7 · BR19 · BR20 · BR28 · BR29 · BR46 |
| Quyền | BR25 |
| Grid chi tiết con | BR21 |

---

## 8. Anti-pattern — 10 câu prompt làm hỏng kết quả

| Prompt hỏng | Vì sao hỏng | Viết lại |
|---|---|---|
| "Làm màn thêm mới chứng từ bán hàng" | Không có nguồn, AI bịa nghiệp vụ | Kèm đường dẫn UC + SCR + Matrix + messages |
| "Xem cách dự án đang làm rồi làm tương tự" | AI grep trúng `master_data/**` hoặc `legacy/` | Chỉ đích danh module mẫu được phép |
| "Tự do refactor cho sạch" | Diff phình, review không nổi | "Không refactor ngoài phạm vi PYC" |
| "Làm nhanh, bỏ qua test" | Không có cổng nghiệm thu → không nghiệm thu được | Ghi rõ lệnh phải xanh |
| "Tạo bảng DB phù hợp" | AI tự chọn kiểu/precision sai BR7 | Yêu cầu §9 plan: kiểu, NULL, default, ai ghi, precision-scale |
| "Trả về message lỗi phù hợp" | AI bịa messageId | "Lấy từ `6.messages.md` của ĐÚNG epic, không bịa mã" |
| "Dùng component UI có sẵn" | Mơ hồ, AI tự tạo component mới | "Tái sử dụng barrel `@base`; thiếu prop → thêm prop vào `@base`" |
| Dán đường dẫn máy cá nhân (`/Users/<ai đó>/...`) | AI không đọc được | Đường dẫn tương đối từ repo root |
| "Sửa base cho tiện" | Mức C không kiểm soát, vỡ module khác | "core/, accounting_core/ read-only. Phải sửa → dừng, xuất impact analysis" |
| "Xong chưa? Báo hoàn thành đi" | AI báo xanh dù chưa chạy lệnh | "Dán output thật của lệnh; lệnh nào đỏ phải nói rõ" |

---

## 9. Checklist

### 9.1 Trước khi **gửi** prompt

- [ ] Đã có đủ 8 khối B1→B8 (§3)?
- [ ] Mọi đường dẫn đều tương đối từ repo root và **tồn tại thật**?
- [ ] Đã liệt kê BR theo bảng §7?
- [ ] Đã trỏ `6.messages.md` (nếu có message) và `Matrix/**` (nếu có ẩn/hiện)?
- [ ] Đã ghi vùng cấm + mức thay đổi A/B/C?
- [ ] Đã nói rõ output là **plan** hay **code**?

### 9.2 Trước khi **chấp nhận** kết quả từ AI

**Kiến trúc**
- [ ] Đúng module đích, đúng cây thư mục (`internal/` ở BE, cây §3 ở FE)?
- [ ] BE: Controller không gọi Repository, Entity không lọt ra API, response bọc `ApiResponse<T>`?
- [ ] FE: import bằng alias, chỉ đi xuống tầng, không deep-import `internal`/`antd/es/*`?
- [ ] Có tái sử dụng base/engine thay vì copy-paste không?

**Diff**
- [ ] Có đụng `master_data/**` hay `client/src/legacy/**` không?
- [ ] Có sửa `core/**` / `accounting_core/**` trái policy không?
- [ ] Diff có phình ngoài phạm vi PYC không?

**Nghiệp vụ**
- [ ] messageId có tra được trong `6.messages.md` của đúng epic không?
- [ ] Ma trận ẩn/hiện đã áp đủ chưa?
- [ ] Báo cáo có **liệt kê BR đã áp dụng / chưa đạt** không?

**Build** — có output thật, không phải lời hứa:

```bash
cd cell-app && ./gradlew unitTest
```

```bash
cd client && npm run typecheck && npm run lint && npm run lint:boundaries && npm run test
```

> ⚠️ `../../cell-app` là Gradle project độc lập (wrapper riêng) — repo root **không có** `gradlew`, nên
> `./gradlew :cell-app:build` sẽ báo "no such file or directory". Máy chưa cài Docker thì
> `./gradlew build` luôn đỏ ở các test Testcontainers; phải đối chiếu danh sách lớp lỗi trước khi
> kết luận là hồi quy.

---

## 10. Tài liệu tham chiếu

| Tài liệu | Dùng khi |
|---|---|
| [CLAUDE.md](../../CLAUDE.md) | 8 luật cứng, vùng đóng băng, bảng tra BR |
| [docs/conventions.md](../conventions.md) | Quy ước đầy đủ + checklist trước commit |
| [docs/_bieu-mau-plan-api.md](_bieu-mau-plan-api.md) | Biểu mẫu plan BE (pha 1) |
| [docs/cell-app-ai-agent-template.md](cell-app-ai-agent-template.md) | Change policy A/B/C, điểm reuse base BE |
| [docs/fe-khung-kien-truc-chuan.md](fe-khung-kien-truc-chuan.md) | Cây thư mục FE, 15 artefact, cổng DoD |
| [pmkt-docs/ba/Common/business_rules.md](../pmkt-docs/ba/Common/business_rules.md) | BR1…BR46 |
| [docs/doing/ctbh-them-moi-api-plan.md](doing/ctbh-them-moi-api-plan.md) | **Ví dụ plan đạt chuẩn** — đọc để biết mức chi tiết cần đạt |
| `cell-app/CLAUDE.md` · `client/CLAUDE.md` | Rule đặc thù module (cộng dồn với rule gốc) |
