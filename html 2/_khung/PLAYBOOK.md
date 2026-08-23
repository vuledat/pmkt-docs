# Playbook sinh trang flow HTML cho MỘT epic

Bạn được giao **đúng một epic**. Nhiệm vụ: đọc tài liệu BA của epic đó rồi ghi ra **đúng một file**
`docs/html/<PYC>/<slug>-flow.src.html`.

**KHÔNG** render, **KHÔNG** publish Artifact, **KHÔNG** đụng `client/` hay `cell-app/`.
Bản standalone `.html` và Artifact do pipeline trung tâm lo — bạn chỉ ghi bản `.src.html`.

Gốc repo: `C:/Users/Admin/Desktop/code/vtt-osp`. Mọi đường dẫn dưới đây tính từ gốc repo.

---

## 1. Đọc tài liệu — đọc hết trước khi vẽ

Thư mục nguồn: `pmkt-docs/ba/<PYC>/`. Đọc theo đúng thứ tự:

| Bước | File | Rút ra |
|---|---|---|
| 1 | `1.function*-breakdown.md` | Phạm vi epic · chức năng con · mã `PMKT-U-*` |
| 2 | `2.usecase*.puml` · `3.crud-matrix.*` | Danh sách UC · entity bị C/R/U/D ở UC nào |
| 3 | `4.usecases/*/UC_*.md` | Luồng chính · luồng phụ · ngoại lệ · tiền/hậu điều kiện · quyền |
| 4 | `4.usecases/*/AD_*.puml` | **Xương sống của sơ đồ** — nhánh quyết định và thứ tự kiểm |
| 5 | `5.screens/**/SCR_*.md` | Toàn bộ `BR*` — điều kiện hiện nút, công thức, ràng buộc chặn |
| 6 | `6.messages.md` | Mã `MSG_*` gắn vào từng nhánh chặn |
| 7 | `Matrix/**` (nếu có) | Ma trận ẩn/hiện trường theo chế độ màn hình |

Tên file có thể lệch chút (`1.functions-breakdown.md` / `1.function-breakdown.md`, `2.usecase.puml` /
`2.usecases.puml`) — cứ `ls` thư mục rồi đọc theo thứ tự số.

Màn hình lớn (>1000 dòng): `grep -n '^#\{1,4\} '` lấy mục lục trước rồi đọc từng khối BR, không đọc
tràn cả file.

**Bắt buộc đối chiếu** `pmkt-docs/ba/Common/business_rules.md` cho phạm vi vừa đọc — BR chung
(BR1 phân trang · BR12 trạng thái · BR25 phân quyền · BR36 ghi sổ · BR29 chính sách xóa …) vẫn áp
dù epic không nhắc lại. File này rất dài: `grep -n '^## BR'` lấy mục lục rồi đọc đúng BR cần.

**Nguồn sự thật là tài liệu BA.** Không suy diễn luồng không có trong UC/AD/BR. Thiếu quy định thì
ghi rõ trong trang là *chưa có quy định*, không tự đặt luật.

**Vùng cấm:** không đọc `cell-app/**/master_data/**`, không đọc `client/src/legacy/**`.

---

## 2. Dàn ý section — một luồng, một section

Sắp theo **vòng đời chứng từ / bản ghi**, không theo thứ tự file:

```
00  Tổng quan       — bản đồ trạng thái + bảng trạng thái dẫn xuất
01  Xem danh sách   — màn điều phối, luật gác nút
02  Thêm mới        — tách 2 sơ đồ: chuỗi nhập liệu và chuỗi lưu
03  Quan hệ dữ liệu — bản ghi liên kết sinh ra, ai ghi sổ cái gì
04..n Nghiệp vụ đặc thù của epic (chiết khấu, phân bổ, quy đổi, khấu hao…)
n+1 Chỉnh sửa · Ghi sổ · Bỏ ghi sổ · Xóa · Xem chi tiết
n+2 Trường dẫn xuất / counter
n+3 Bảng tra: điều kiện chặn ↔ mã MSG · ma trận quyền
```

Epic không phải chứng từ (danh mục, cấu hình, báo cáo) thì đổi trục cho hợp: vòng đời bản ghi
(thêm · sửa · xóa · trạng thái hoạt động) hoặc vòng đời kỳ (chọn tham số · tính · kết xuất).

Quy mô mong muốn: **10–15 sơ đồ**, 10–14 section cho epic đủ tài liệu. Epic mỏng (<800 dòng BA) thì
ít hơn — vẽ đúng những gì tài liệu có, không bịa thêm cho đủ số.

Mỗi section gồm: `<h2>` + 1 câu `lede` + `<figure>` sơ đồ + `<figcaption>` **nêu đúng một khẳng định**
+ bảng tra hoặc callout nếu có ràng buộc dễ sai.

**Sơ đồ phải vẽ cơ chế, không vẽ tên gọi.** Nhánh quyết định lấy nguyên từ AD; nhãn cạnh ghi điều
kiện thật (`Chưa ghi sổ`, `Tồn kho đủ?`), không để mũi tên trống nghĩa.

---

## 3. Cấu trúc file phải ghi ra

File `docs/html/<PYC>/<slug>-flow.src.html` gồm **đúng hai phần**:

1. **Phần đầu — copy NGUYÊN VĂN** `docs/html/_khung/head.html` (143 dòng: `<title>` + `<link>` font
   + `<style>`). Chỉ được đổi **một** thứ: nội dung trong `<title>`.
   `<title>` là **tên**, 2–4 từ, không kèm giải thích sau dấu gạch. Ví dụ: `Luồng Phiếu thu tiền mặt`.
2. **Phần thân** — bắt đầu từ `<div class="wrap">` tới `</div>` cuối. Không `<!doctype>`, không
   `<html>`, không `<head>`, không `<body>`. Không thêm `<style>` thứ hai, không thêm `<script>`.

Cách ghép an toàn: ghi phần thân ra file tạm rồi
`cat docs/html/_khung/head.html file-than.html > docs/html/<PYC>/<slug>-flow.src.html`.

**Mẫu tham chiếu duy nhất — đọc trước khi viết:**
`docs/html/PMKT-E-06194_ChungTuBanHang/PMKT-E-06194-chung-tu-ban-hang-flow.src.html`
(masthead · nav rail · section · figure/plate · bảng `.tw` · chip · callout · footer).

Class có sẵn trong khung, dùng đúng tên: `.wrap` `.mast` `.eyebrow` `.meta` `.rail` `.snum` `.lede`
`.plate` `.tw` `.chip` `.c-msg` `.c-br` `.c-ok` `.c-warn` `.c-perm` `.note` `.note.stop` `.mono` `.num`.
**Không** tự thêm màu hardcode ngoài token — ngoại lệ duy nhất là chuỗi `themeVariables` của mermaid.

---

## 4. Sáu bẫy mermaid — vi phạm là trang hỏng

**Bẫy 1 — thiếu chuỗi init.** Mỗi block `<pre class="mermaid">` phải mở đầu bằng **đúng** dòng này,
không sửa một ký tự (đây là thứ giữ sơ đồ không bị co nhỏ và giữ font/màu khớp trang):

```
%%{init:{"flowchart":{"useMaxWidth":false},"theme":"base","themeVariables":{"primaryColor":"#ffffff","primaryTextColor":"#16202b","primaryBorderColor":"#2f6f8f","lineColor":"#6b7683","fontFamily":"Helvetica Neue, Helvetica, Arial, sans-serif","fontSize":"14px"}}}%%
```

**Bẫy 2 — ký tự phá cú pháp trong nhãn.**
- Nhãn chứa `(` `)` `,` `:` `-` → **bọc nháy kép**: `A["Ghi sổ (BR20)"]`.
- **Không** dùng `<` `>` trong nhãn — dùng `≤ ≥ →`.
- Xuống dòng bằng `<br/>`, không xuống dòng thật.
- Nhãn cạnh dài cũng bọc nháy: `A -- "Tồn kho đủ?" --> B`.
- Chỉ dùng thẻ HTML `<b>` `<br/>` `<i>` trong nhãn, không dùng thẻ khác.

**Bẫy 3 — sơ đồ quá rộng.** Mỗi SVG phải ≤ ~1800px. Hai `subgraph` cạnh nhau trong một block là công
thức sinh SVG rộng 4500px → **tách thành hai block**. Chuỗi validate tách khỏi chuỗi ghi dữ liệu;
luồng đơn tách khỏi luồng hàng loạt.

**Bẫy 4 — chọn sai hướng.**

| Hình dạng luồng | Hướng đúng |
|---|---|
| Nhiều nhánh song song, chuỗi nông (màn điều phối, danh sách nút) | `LR` |
| Chuỗi sâu, nhãn dài (chuỗi validate, chuỗi ghi dữ liệu) | `TD` |

**Bẫy 5 — `stateDiagram-v2` cắt nhãn.** Vẽ bản đồ trạng thái bằng `flowchart LR` với nhãn
`<b>TÊN TRẠNG THÁI</b><br/>…`.

**Bẫy 6 — nhãn quá dài.** Giữ mỗi dòng nhãn ≤ ~34 ký tự, cắt dòng bằng `<br/>`. Nhãn dài làm sơ đồ
phình ngang vượt ngưỡng 1800px.

Ba vai trò màu khai bằng `classDef` ở cuối mỗi block, **đúng bộ màu này**:

```
classDef err  fill:#fbeceb,stroke:#b23a2e,color:#7a2318;
classDef ok   fill:#e8f4ee,stroke:#2e7d5b,color:#1c4c38;
classDef warn fill:#fbf2e2,stroke:#a9761f,color:#6d4a12;
```

---

## 5. Tự kiểm trước khi báo xong

Chạy **đúng lệnh này** từ gốc repo (`cd C:/Users/Admin/Desktop/code/vtt-osp` trước):

```bash
node docs/html/_khung/check.mjs docs/html/<PYC>/<slug>-flow.src.html
```

Script kiểm: cân bằng thẻ · mọi block mermaid có chuỗi init · head copy nguyên văn · thân không thừa
thẻ · nhãn không chứa ký tự phá cú pháp · không dùng class lạ ngoài khung.
Phải ra `=== ĐẠT ===`. Dòng `cảnh báo:` không phải lỗi nhưng nên xử lý nếu dễ.

**Không tự viết lại đoạn kiểm bằng `node -e`** — quote lồng qua Bash trên Windows làm regex sai và
sinh dương tính giả.

---

## 6. Báo cáo khi xong

Trả về **một khối JSON** (không kèm văn xuôi dài):

```json
{
  "pyc": "...", "file": "docs/html/.../....src.html",
  "sections": 12, "diagrams": 14,
  "sources": {"uc": 6, "ad": 6, "screens": 8, "messages": 24},
  "brApplied": ["BR1","BR12","BR25","BR36"],
  "gaps": ["luồng X tài liệu BA chưa quy định rõ nên không vẽ"],
  "selfCheck": "mọi thẻ cân bằng, init đủ, head nguyên vẹn"
}
```
