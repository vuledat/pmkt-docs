# Đánh giá skill trên một epic PMKT

Chọn epic có spec và code thật. Ghi riêng kết quả vào `docs/doing/skills-evaluation/`;
không sửa spec/BA hay triển khai lại epic chỉ để có số đo. Mốc thử ban đầu:
`PMKT-E-06194-chung-tu-ban-hang-spec` (có cả code BE/FE và bốn file spec).

## Phiếu đo cho mỗi lượt

- Thời điểm, tên skill, tầng, phạm vi R/S, SHA của repo và trạng thái working tree.
- Hash hoặc phiên bản bộ skill; ghi lệnh và output/log làm bằng chứng.
- Số luật trong phạm vi, có code/test, chưa có mã, chưa có test, bị conflict chặn.
- Số finding được xác nhận sau review, phân biệt lỗi có sẵn và lỗi do thay đổi.
- Số scenario PASS/FAIL/BLOCKED/NOT-RUN; browser QA chỉ PASS khi thực sự thao tác.
- Số vòng phải sửa sau review; thời gian làm thực tế và thời gian chờ BA/môi trường riêng.
- Token/chi phí chỉ ghi nếu công cụ cung cấp; không suy từ độ dài hội thoại.

## Lệnh baseline

Chạy `sync-skills.py --check`, rồi `trace.sh <spec> be` và `trace.sh <spec> fe`.
Chạy `msg.sh <PYC-Phase-1> <tầng>` khi đánh giá message; trước khi dùng script hiện có,
kiểm tra nó loại trừ vùng đóng băng ở mọi nhánh thực thi. Không dùng fallback quét vùng cấm.
Mã R trong comment không chứng minh hành vi; kết quả trace OK phải qua `verify-spec`.

## Cách so sánh

Giữ cùng snapshot BA/spec, phạm vi, công cụ và loại nhiệm vụ. So bộ cũ/mới trên hai
checkout cô lập nếu cần thử triển khai; không cho lượt sau đọc kết luận của lượt trước.
Không tự sửa dữ liệu dùng chung hay chạy ghi sổ để tạo benchmark.

Đánh giá đạt khi không phát sinh vi phạm vùng cấm/nguồn nghiệp vụ, phát hiện đúng lỗi
có bằng chứng, giảm luật bỏ sót hoặc vòng sửa mà không bỏ cổng bắt buộc. Không đặt mục tiêu
phần trăm tùy ý. Chưa có lượt so sánh thì ghi **chưa đo hiệu quả**, không tuyên bố tiết kiệm.
