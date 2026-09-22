# Triển khai bộ skill PMKT — 2026-09-06

## Đã thực hiện

- Chọn `.claude/skills` làm nguồn, đồng bộ 12 skill / 41 tài nguyên sang `.agents/skills`.
  Đã đối chiếu các bản cũ: bản Claude bổ sung cổng spec, truy vết và sửa đường dẫn module;
  không thấy phần riêng của bản Agents cần giữ ngoài nguồn đó.
- Bổ sung năm skill còn thiếu ở Agents: audit-spec, verify-spec, review-code, fix-bug-be,
  fix-bug-fe; thêm qa-flow cho cả hai môi trường.
- Rút gọn entrypoint review-code, chuyển bốn lớp PMKT vào reference; bổ sung review hành vi,
  lỗi biên, rollback, tương tranh, bằng chứng phản biện và QA theo scenario.
- Loại cơ chế tự chốt mâu thuẫn theo bậc nguồn; giữ ngoại lệ ưu tiên epic/BR của CLAUDE.md.
  Không sửa quyết định trong spec cũ hoặc nội dung BA.
- Thay phụ thuộc Workflow cố định và hướng dẫn stash bằng công cụ hiện có/worktree riêng.
  Dẫn cổng FE về quy tắc client; giữ ngoại lệ cổng nhẹ. Bỏ chữ ký model cố định trong commit.
- Sửa frontmatter push-code chưa hợp lệ do dấu hai chấm trong description.
- Tạo sync-skills.py: check drift, kiểm reference, phát hiện sửa riêng ở bản sinh,
  không xóa file dư, từ chối đường dẫn liên kết. Manifest chứa SHA-256 từng tài nguyên.
- Sửa phạm vi quét của msg.sh và nhánh grep dự phòng của trace.sh: exclude trước khi đọc.
  Thêm chặn đầu vào Phase_2 ở trace.sh. Không thay cách chấm nội dung của hai script.

## Kiểm chứng

- quick_validate.py của skill-creator: cả 12 skill hợp lệ. PyYAML cài vào thư mục tạm,
  không thêm dependency ứng dụng.
- sync-skills.py --check: OK, 41 tài nguyên khớp.
- test_skills_tooling.py: 10 ca, 9 PASS, 1 SKIP do Windows không cho tạo symbolic link
  trong sandbox. Các ca chạy gồm ghi/đọc đồng bộ, giữ local edit, adoption ban đầu,
  thiếu reference, file dư, quét nguồn hợp lệ, loại vùng đóng băng và chặn Phase_2.
- Không chạy build/test ứng dụng: chỉ thay skill, hướng dẫn và script kiểm tra.

## Baseline epic thật

Nguồn: `PMKT-E-06194-chung-tu-ban-hang-spec`; output đầy đủ ở trace-be.log,
trace-fe.log, msg-be.log, msg-fe.log. Thời điểm UTC và trạng thái Git ở baseline.json.
Hai repo đều có thay đổi chưa commit; số liệu thuộc working tree, không chỉ SHA HEAD.

| Kiểm tra | Tổng | Kết quả |
|---|---:|---|
| Trace BE | 93 luật | 0 OK, 86 MISSING, 7 BLOCKED |
| Trace FE | 72 luật | 0 OK, 1 NO-TEST, 65 MISSING, 6 BLOCKED |
| Message BE | 60 | 31 OK, 29 THIEU |
| Message FE | 60 | 6 OK, 4 CHUA-DAT, 50 THIEU |

Trace trả exit 1; message trả exit 0 dù còn THIEU: không dùng exit code đơn lẻ làm
điều kiện nghiệm thu. Kết quả chỉ đo mã truy vết/định nghĩa message tìm thấy, chưa
chứng minh hành vi đúng/sai. Chưa review từng R/S, chưa chạy QA trình duyệt, chưa
đo thời gian/token/vòng sửa trước và sau bộ skill. Không kết luận mức tiết kiệm.

## Sử dụng tiếp

Theo `docs/rules/skills-workflow.md` và `docs/rules/skills-evaluation.md`.
Chỉnh nguồn rồi chạy --write, --check trước khi chia sẻ. Không cài BMAD/gstack,
không tạo Git repo hay CI service để quản lý thư mục cha. Chưa commit/push.
