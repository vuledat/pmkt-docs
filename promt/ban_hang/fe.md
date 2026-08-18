
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