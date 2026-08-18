Nhiệm vụ: lập KẾ HOẠCH triển khai API cho use case <TÊN UC> thuộc PYC <PMKT-E-xxxxx_...>.
CHƯA code — pha này chỉ xuất tài liệu để dev và BA review.

## Nguồn nghiệp vụ (đọc hết trước khi viết plan)
- pmkt-docs/ba/<Điền EPIC>/4.usecases/<UseCase>/UC_*.md + AD_*.puml
- pmkt-docs/ba/<Điền EPIC>/5.screens/SCR_*.md
- pmkt-docs/ba/<Điền EPIC>/6.messages.md        ← lấy messageId, KHÔNG bịa mã mới
- pmkt-docs/ba/<Điền EPIC>/3.crud-matrix.puml
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