# Đánh số migration theo timestamp

> Áp dụng cho **mọi service Java có Flyway**: `../../cell-app`, `../../tenant-provisioning`,
> `../../integration-platform`. Có hiệu lực từ 2026-08-20.

## 1. Luật

**File migration mới đặt tên:**

```
V<yyyyMMddHHmmss>__<prefix>_<mo_ta_snake_case>.sql
```

Ví dụ: `V20260820143012__sal_them_cot_nhan_vien_ban_hang.sql`

Lấy version bằng chính lệnh này, **không tự gõ tay, không đếm `max + 1`**:

```bash
date +V%Y%m%d%H%M%S
```

- `<prefix>` vẫn là tiền tố bảng của module (`acc_`, `sal_`, `pur_`, `iam_`, `inv_`, `fa_`, `cp_`…).
- Timestamp là **giờ local lúc tạo file**, 14 chữ số, không có dấu phân cách.
- Một PR cần nhiều migration → mỗi file một timestamp riêng, chạy `date` lại cho từng file.

## 2. Vì sao đổi

Cách cũ (`V<max+1>`) buộc mọi người đọc cùng một con số toàn cục. Hai nhánh mở song song đều thấy
`max = 1031` và cùng đẻ ra `V1032__…` → merge xong có **hai file cùng version**, Flyway chết ngay lúc
boot với `Found more than one migration with version 1032`. Sửa được thì phải rename file đã chạy
trên DB dev, kéo theo `flyway_schema_history` lệch và checksum mismatch cho cả đội.

Timestamp có 14 chữ số theo giây ⇒ hai nhánh không bao giờ trùng version, và không ai phải hỏi
"số mới nhất là bao nhiêu" trước khi viết SQL.

## 3. File cũ giữ nguyên — KHÔNG rename

`cell-app` đang có `V1`, `V2`, `V3`, `V1000`…`V1031`; `tenant-provisioning` có `V1`…`V12`;
`integration-platform` có `V1`…`V5`. **Tuyệt đối không đổi tên chúng sang timestamp.**

Version của một migration đã chạy được ghi vào bảng `flyway_schema_history` của **mọi** DB đã áp
(dev, staging, từng tenant). Đổi tên file = Flyway thấy "applied migration not resolved locally" +
"resolved migration not applied to database" và chặn boot toàn bộ môi trường. Không có cách sửa nào
rẻ hơn là đổi tên lại như cũ.

Timestamp 14 chữ số luôn **lớn hơn** mọi version cũ (`20260820143012` > `1031`), nên file mới vẫn
chạy sau file cũ theo đúng thứ tự — hai cách đánh số sống chung được, không cần baseline lại.

## 4. Thứ tự áp dụng & out-of-order

Timestamp diệt được **va chạm version**, nhưng không diệt được **áp dụng lệch thứ tự**: nhánh A merge
trước với `V20260820…`, nhánh B merge sau với `V20260819…` (tạo sớm hơn) → DB đã ở version cao hơn,
Flyway báo `Detected resolved migration not applied to database` và chặn boot.

Cấu hình hiện tại đã xử lý sẵn, khác nhau theo môi trường — **không cần đổi gì**:

| Môi trường | `out-of-order` | Hành vi |
|---|---|---|
| Máy dev (profile `local`) | `true` mặc định (`application.yml`, khối profile `local`) | apply bù được, không chặn boot |
| Prod / k8s / worker | `false` mặc định (`application.yml`, khối gốc) | validate nghiêm ngặt, chặn boot |

Ghi đè từng lần bằng `SPRING_FLYWAY_OUT_OF_ORDER=…`. **Không** bật `true` cố định trên môi trường
chung ngoài dev: apply lệch thứ tự khiến DB dev và DB prod có lịch sử migrate khác nhau.
Riêng checksum mismatch thì dùng `FLYWAY_REPAIR_ON_BOOT=true`, out-of-order không sửa được.

### 4.1 Cạm bẫy: DB rỗng chạy theo thứ tự TẠO FILE, không theo thứ tự merge

Trên DB rỗng hoặc DB tụt hậu (prod deploy đầu, tenant mới, CI dựng DB sạch), Flyway sắp theo version
= **thời điểm tạo file**. Nhánh sống lâu vì thế đảo được thứ tự so với lúc merge:

```
nhánh A: tạo 20/08 → V20260820090000__acc_tao_bang_x.sql       (merge NGÀY 25)
nhánh B: tạo 22/08 → V20260822140000__acc_them_cot_vao_x.sql   (merge NGÀY 23)
```

DB dev chạy theo thứ tự merge (A rồi B); DB rỗng chạy theo timestamp — cũng A rồi B, nên ví dụ này
an toàn. Nhưng nếu A tạo **sau** B mà merge **trước**, DB dev xanh còn DB rỗng chạy B trước A và đỏ.
Với `max + 1` chuyện này gần như không xảy ra vì số lấy ngay trước lúc merge.

Hai luật để tránh:

1. **Mỗi migration tự đủ** — không phụ thuộc migration của nhánh khác trong cùng đợt.
2. **Renumber lúc rebase** — trước khi merge, nếu timestamp file mới nhỏ hơn version lớn nhất đã có
   trên `master`, chạy lại `date +V%Y%m%d%H%M%S` và **`git mv`** (không `mv` trần). File chưa merge
   nên chưa nằm trong `flyway_schema_history` của prod; đổi tên lúc này là an toàn — chỉ cần
   `FLYWAY_REPAIR_ON_BOOT=true` một lượt trên DB dev nếu bản cũ đã chạy ở đó.

## 5. Cổng kiểm

`cell-app/src/test/java/vn/vtt/pmkt/cell/arch/MigrationNamingArchTest.java` (`@Tag("unit")`) quét
thư mục `db/migration` và bắt lỗi ngay ở `./gradlew unitTest` nếu:

- có file mới không theo dạng 14 chữ số (vd ai đó vẫn đặt `V1032__…`);
- timestamp không phải ngày giờ có thật (vd `V20261345000000__…`);
- có hai file trùng version;
- một file legacy bị đổi tên hoặc xoá (danh sách legacy đóng băng trong test).

## 6. Checklist khi thêm migration

- [ ] `date +V%Y%m%d%H%M%S` → dùng đúng chuỗi đó làm version.
- [ ] Tên file có `<prefix>` của module và mô tả không dấu, `snake_case`.
- [ ] `git add` file migration **cùng commit** với code dùng nó.
- [ ] Không sửa / không rename bất kỳ file migration nào đã merge.
- [ ] `cd cell-app && ./gradlew unitTest` xanh.
