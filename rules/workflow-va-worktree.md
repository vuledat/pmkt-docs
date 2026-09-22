# Workflow nhiều agent & git worktree — dùng khi nào, dùng thế nào

> Hai công cụ này giải hai bài toán khác nhau:
> **workflow** = chia một việc quá lớn cho một context thành nhiều context sạch chạy song song;
> **worktree** = cho nhiều nhánh code cùng tồn tại trên đĩa để không phải `git stash` qua lại.
> Dùng sai chỗ thì cả hai đều chỉ tốn token và dung lượng.

---

## Phần 1 — Workflow

### 1.1 Khi nào đáng dùng

| Việc | Workflow? | Vì sao |
|---|---|---|
| `/audit-spec` một epic có file SCR > 40 KB | ✅ **rất đáng** | `SCR_CTBH_ThemMoi.md` 187 KB / 1.630 dòng / 291 lần nhắc BR — một context không giữ nổi cả tài liệu lẫn luật đã trích. Đây chính là nguyên nhân rơi luật |
| `/verify-spec` spec > 40 luật | ✅ **rất đáng** | 112 luật chấm trong một context thì càng về cuối càng hạ chuẩn bằng chứng; thêm được vòng phản biện độc lập |
| Rà toàn bộ ~50 epic xem epic nào chưa có spec / chưa có plan | ✅ | fan-out thuần, mỗi agent một epic |
| Đối chiếu chéo BE ↔ FE cùng một `02-rules.md` | ✅ | hai agent độc lập rồi so kết quả, bắt được chỗ hai tầng hiểu khác nhau |
| `/gen-be`, `/gen-fe` một màn | ❌ | code phải nhất quán trong một đầu; nhiều agent viết song song vào cùng module = xung đột và lệch phong cách |
| Sửa một bug, thêm một cột | ❌ | chi phí điều phối lớn hơn việc |

⚠ **Workflow chỉ chạy khi user yêu cầu rõ** (nói "chạy workflow", "ultracode", hoặc gọi tên workflow).
Một lần chạy có thể ngốn hàng chục agent — không tự ý bật.

### 1.2 Hai workflow đã dựng sẵn

| Tên | File | Gọi thế nào |
|---|---|---|
| `audit-spec-fanout` | `.claude/workflows/audit-spec-fanout.js` | args: `{"pyc":"pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang","slug":"PMKT-E-06194-chung-tu-ban-hang","viet_tat":"CTBH"}` |
| `verify-spec-fanout` | `.claude/workflows/verify-spec-fanout.js` | args: `{"spec":"docs/doing/PMKT-E-06194-chung-tu-ban-hang-spec","tang":"fe","pyc":"pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang"}` |

**`audit-spec-fanout`** — khảo sát (1 agent đo `scr.sh --stat/--list/--br/--links` rồi chia file lớn
thành cụm) → trích luật (mỗi agent MỘT cụm, trả luật thô có `file:dòng`) → đối chiếu (gom theo
`chu_de`, chủ đề nào có ≥2 nguồn thì một agent đọc lại nguyên văn cả hai phía để kết luận khớp hay
mâu thuẫn) → hợp nhất (đánh mã `R-`/`INV-`/`S-`, ghi 4 file spec).

**`verify-spec-fanout`** — quét `trace.sh` + `msg.sh` lấy khung → chia luật thành lô 12 → mỗi lô một
agent context sạch (bị cấm đọc plan và `IMPLEMENT.md`) → **lô nào chấm xong thì phản biện ngay**
(pipeline, không chờ lô chậm nhất): một agent khác thử **bác bỏ** mọi kết luận ĐẠT → tổng hợp.

Sửa workflow: sửa thẳng file `.js` rồi chạy lại; không cần chép lại nội dung vào prompt.

### 1.3 Ba luật khi viết workflow mới cho repo này

1. **Nền bối cảnh phải nhắc lại trong prompt mỗi agent** — subagent không kế thừa `CLAUDE.md` theo
   cách ta tưởng. Tối thiểu: cấm `Phase_2`, cấm `Read` cả file SCR (dùng `scr.sh`), cấm sửa
   `pmkt-docs/`, bắt buộc `file:dòng`, cấm tự đặt luật mới.
2. **`pipeline()` thay vì `parallel()`** trừ khi bước sau thật sự cần toàn bộ kết quả bước trước
   (khử trùng lặp, đếm tổng). Barrier làm agent nhanh ngồi chờ agent chậm.
3. **Việc phán xét thì tách agent khác** — agent vừa sinh kết luận không tự phản biện được kết luận
   của mình. Đây là lý do `verify-spec-fanout` có pha *Phản biện* riêng.

---

## Phần 2 — Git worktree

### 2.1 Bối cảnh repo PMKT

Gốc `vtt-osp/` **không phải** git repo. Mỗi service là một repo độc lập
(`client`, `cell-app`, `pmkt-docs`, …), hiện đều đứng ở `develop`. Vì vậy worktree luôn là
**worktree của một service**, không bao giờ của cả `vtt-osp/`.

Chi phí thật đã đo trên máy này:

| Repo | Thứ không nằm trong git nhưng cần để chạy | Dung lượng |
|---|---|---|
| `client` | `node_modules/` | **471 MB** |
| `cell-app` | `build/` + `.gradle/` | 68 MB + 19 MB |

Đây là lý do worktree **không miễn phí**: cây mới clone từ git sẽ thiếu đúng những thứ nặng nhất.

### 2.2 Khi nào đáng tạo worktree

| Tình huống | Worktree? |
|---|---|
| Làm 2 epic song song, không muốn `stash` qua lại | ✅ |
| Cần so sánh hành vi nhánh cũ ↔ nhánh mới cạnh nhau | ✅ |
| Thử một refactor rủi ro, muốn vứt đi sạch sẽ | ✅ |
| Chạy agent song song cùng sửa file (workflow `isolation: 'worktree'`) | ✅ nhưng chỉ với `cell-app`; với `client` phải xử lý `node_modules` trước |
| Sửa một màn, một API | ❌ — `git switch` là đủ |

### 2.3 Cách làm trên máy này

```bash
# 1. Tạo worktree cho cell-app (rẻ — Gradle cache dùng chung ở ~/.gradle)
git -C cell-app worktree add ../wt-cell-app-feat-x -b feat/x develop

# 2. Tạo worktree cho client (đắt — phải xử lý node_modules)
git -C client worktree add ../wt-client-feat-x -b feat/x develop
```

`client` không có `node_modules` trong worktree mới. **Không** chạy `npm ci` (mạng chậm, ~471 MB);
tạo **junction** trỏ về cây chính — đã kiểm chứng chạy được, **không cần quyền admin**:

```bash
powershell -NoProfile -Command "New-Item -ItemType Junction \
  -Path 'C:\Users\Admin\Desktop\code\wt-client-feat-x\node_modules' \
  -Target 'C:\Users\Admin\Desktop\code\vtt-osp\client\node_modules'"
```

Điều kiện an toàn của junction: **hai cây cùng `package-lock.json`**. Nhánh có đổi dependency thì
phải `npm ci` thật trong worktree đó, đừng dùng chung.

Dọn:

```bash
git -C client worktree remove ../wt-client-feat-x     # gỡ junction trước nếu remove kêu bận
git -C client worktree list
```

### 2.4 Bốn cái bẫy đã biết

1. **IntelliJ chỉ mở `vtt-osp/`.** Worktree đặt ngoài cây đó thì `mcp__idea__*` (build, run config,
   SQL) **không thấy**. Mà `CLAUDE.md` bắt chạy code qua IntelliJ, **cấm Docker** → worktree hợp cho
   *đọc/sửa/so sánh*, còn *chạy* thì về cây chính. Muốn chạy trong worktree thì phải mở nó như một
   project IntelliJ riêng.
2. **Cùng một DB.** Các service dùng chung một database dev; hai worktree chạy Flyway cùng lúc là
   giẫm chân nhau. Một cây chạy migration tại một thời điểm.
3. **`client` có baseline đỏ sẵn** (tsc + test). So sánh hai worktree phải đo baseline từng cây
   trước, đừng quy kết cho diff.
4. **Cổng cây commit vẫn áp trong worktree**: file mới phải `git add`; `npm run check:committed`
   trên máy này cho báo động giả hàng loạt — đừng coi là chặn.

### 2.5 Kết hợp với workflow

`agent(..., { isolation: 'worktree' })` chỉ đáng dùng khi nhiều agent **cùng ghi file**. Trong quy
trình PMKT, các workflow ở §1.2 đều là **đọc + phân tích**, nên **không** bật `isolation` — bật vào
là mỗi agent tốn thêm một cây git mà chẳng tránh được xung đột nào.
