# Vận hành bộ skill PMKT

## Nguồn quản lý và đồng bộ

`.claude/skills/<tên>/` là nguồn quản lý. `.agents/skills/<tên>/` là bản sinh từ nguồn đó,
gồm cả references/scripts/assets; không sửa trực tiếp bản sinh. Giữ tên skill giống nhau
để dùng cùng quy trình trên các agent. Không nhập BMAD/gstack làm bộ điều phối thứ hai.

Từ gốc workspace, với Python 3:

```powershell
python docs/rules/sync-skills.py --check
python docs/rules/sync-skills.py --write
python docs/rules/test_skills_tooling.py
```

`--check` không ghi file, trả mã khác 0 khi thiếu/lệch file hoặc reference nội bộ bị hỏng;
dùng làm bước kiểm tra trước khi chia sẻ bộ skill hoặc trong CI của repo quản lý cấu hình.
`--write` kiểm tra thay đổi ở bản sinh bằng manifest trước khi ghi, không xóa file dư,
không ghi đè chỉnh sửa riêng chưa đối chiếu. Khi khởi tạo và có hai bản khác nhau,
đọc diff trước rồi dùng `--write --adopt-source` để chọn nguồn. Cờ này chỉ dùng cho lần
khởi tạo; sau đó chuyển thay đổi cần giữ về nguồn trước khi đồng bộ.

Workspace gốc hiện không phải Git repo. Không tạo workflow CI ở service ứng dụng chỉ để
quản lý skill ở thư mục cha; lệnh kiểm tra trên sẵn sàng dùng khi cấu hình được đưa vào Git.

## Luồng và đầu ra

| Nhu cầu | Skill | Bằng chứng đầu ra |
|---|---|---|
| Soát BA | `audit-spec` | 4 file spec, nguồn thật, câu hỏi OPEN |
| Lập kế hoạch | `plan-be`, `plan-fe` | Plan tham chiếu R/INV/S của cùng spec |
| Triển khai | `gen-be`, `gen-fe` | Code, test, IMPLEMENT và kết quả trace/message |
| Kiểm tra nghiệp vụ | `verify-spec` | Bảng Rule → Code → Test, phần chưa kiểm được |
| Review thay đổi | `review-code` | Finding có điều kiện gây lỗi và bằng chứng |
| QA màn hình | `qa-flow` | Scenario → thao tác → thực tế → bằng chứng |
| Sửa lỗi | `fix-bug-be`, `fix-bug-fe` | Cơ chế lỗi và bằng chứng trước/sau |
| Commit/push theo yêu cầu | `push-code` | Commit/ref và trạng thái push thật |

Đọc `CLAUDE.md` gốc và quy tắc con của phạm vi trước khi thực hiện. Quy tắc con áp dụng
trong phạm vi của nó; ví dụ cổng FE ở `client/CLAUDE.md` và
`docs/rules/fe-cong-nghiem-thu.md`. Skill dẫn tới quy tắc, không tạo một bộ cổng song song.
Số lỗi nền hay thời gian chạy ghi trong tài liệu cũ không chứng minh trạng thái hiện tại.
So baseline bằng cùng lệnh, cùng môi trường trên ref xác định; so từng lỗi, không chỉ tổng số.

## Công cụ giữa các môi trường

- Tên công cụ trong ví dụ thể hiện năng lực cần dùng. Kiểm tra công cụ đang có trước khi gọi;
  không giả lập `Workflow`, `run_in_background`, `preview_start` hay tên MCP không được cung cấp.
- Có shell PowerShell: dùng cú pháp PowerShell; script `.sh` chạy bằng Bash đã cài với cwd
  gốc workspace. Không dán cú pháp `$()`/`&&` của Bash vào chuỗi PowerShell tùy tiện.
- Service, SQL và test cần IDE: dùng IntelliJ connector theo `CLAUDE.md`, luôn xác định
  projectPath. Thiếu connector thì làm tiếp phần đọc/code được phép và báo phần chạy bị thiếu.
- Trình duyệt: dùng công cụ đang được cung cấp và đọc hướng dẫn công cụ/skill tương ứng.
  Dùng lại dev server. Không tự dựng môi trường thay thế khi thiếu quyền hay dữ liệu.
- Review lớn: chia theo tầng/nhóm file và lưu bảng đã đọc. Chỉ dùng nhiều agent khi phiên
  cho phép và có công cụ phù hợp; không phụ thuộc một workflow có tên cố định.
- Baseline/merge thử dùng worktree riêng, detached tại SHA đã ghi nhận. Không stash/reset/
  checkout cây làm việc của user để đo. Chỉ dọn worktree do mình tạo sau khi xác minh đúng
  đường dẫn và không có dữ liệu cần giữ; không dùng `--force` để vượt lỗi dọn dẹp.
- Không tự thêm chữ ký của một model/nhà cung cấp khác vào commit. Theo cấu hình tác giả
  và quy định thực tế của phiên. Skill không cấp quyền gửi comment, commit hay push ngoài yêu cầu.

## Đánh giá trên epic

Dùng `docs/rules/skills-evaluation.md`. Phép đo truy vết tĩnh là baseline cấu trúc;
chỉ tính hiệu quả thực tế sau khi có review/QA và ca triển khai với cùng phạm vi.
