# Phân trang — mọi API danh sách (bắt buộc cho cả FE và BE)

Chốt 2026-10-08, sau đợt rà soát `docs/ra-soat-phan-trang-2026-10-07*.md` (≈50 chỗ tải hết / cắt top-N
im lặng / phân trang trong RAM). Nghiệp vụ: **BR1** (phân trang) · **BR40** (cây) · BR5 (combogrid) ·
BR11 (tìm/lọc) · BR31 (dòng tổng) · BR45 (thao tác hàng loạt) — `./docs/rules/br.sh 1 40 5 11 31 45`.

Bản áp riêng cho từng repo (đọc trong repo là đủ): `client/docs/rules/phan-trang.md`,
`client-admin/docs/rules/phan-trang.md`, `rules/phan-trang.md` ở `cell-app`, `super-admin-service`,
`report-service`, `notification`, `audit-logs-service`, `tenant-provisioning`, `identity`,
`integration-platform` — mỗi bản có chuẩn riêng của repo + nợ đã biết. Sửa luật chung thì sửa cả các bản đó.

## 1. Luật

> **Mọi API trả về danh sách mà số dòng tăng theo dữ liệu tenant đều phải phân trang ở server (DB).
> FE gọi theo trang và hiển thị theo trang. Không có ngoại lệ ngầm — ngoại lệ phải nằm trong §4 và
> được ghi lý do bằng comment ngay tại chỗ.**

"Danh sách" gồm: lưới màn danh sách, lưới trong popup/drawer, popup chọn chứng từ/nguồn/ứng viên,
combogrid/select/picker danh mục, lưới xem trước có thể lớn, log/lịch sử, kết quả tìm kiếm.

## 2. BE (`cell-app` và các service Java)

| Hạng mục | Chuẩn |
|---|---|
| Request | POST tìm kiếm: `core.request.SearchRequest` (`page`, `pageSize`, `sort`, `keyword`, `filters`). GET: `@RequestParam Integer page, Integer pageSize` → `PhanTrang.cua(page, pageSize)` |
| Mặc định / trần | `page` 1-based; `pageSize` mặc định **20** (`PhanTrang.CO_TRANG_MAC_DINH`), trần **200** (`PhanTrang.CO_TRANG_TOI_DA`). Field `pageSize` trong DTO request phải có `@Max(PhanTrang.CO_TRANG_TOI_DA)` |
| Response | `core.response.PageResponse<T>` — `data` + `pagination{page,pageSize,totalItems,totalPages}` + `summary`. Bọc `ApiResponse<PageResponse<T>>` theo luật 6, hoặc trả thẳng như `BaseCrudController.search` — giữ đúng cách của các endpoint cùng controller/module |
| Nơi cắt trang | **Ở DB**: `Pageable`/`PageRequest`, hoặc `COUNT(*)` + `LIMIT/OFFSET` (native/JdbcTemplate). Lọc, sắp xếp, tìm kiếm cũng ở DB **trước** khi cắt |
| Thứ tự | `ORDER BY` luôn có khoá phụ duy nhất (`id`) để trang ổn định khi trùng khoá chính |
| Dòng tổng (BR31) | Tính trên **toàn tập đã lọc** bằng SQL aggregate, trả trong `summary` — không cộng trên trang |
| Gộp nhiều nguồn | Ưu tiên một câu SQL `UNION ALL` + `LIMIT/OFFSET`. Không được thì mỗi nguồn trả `count` + `top(offset + pageSize)` đã sắp, gộp merge-sort rồi cắt; tổng = Σ count. Có unit test cho phép gộp |
| Cây (BR40) | Đếm và cắt trang theo **nút gốc**; con/cháu của các gốc trong trang trả kèm, không áp `pageSize` cho cấp con. Có từ khoá ⇒ trả phẳng hoặc giữ cha của dòng khớp theo BR22 |
| "Chọn tất cả" (BR45) | Không tải hết dòng: thêm endpoint trả **danh sách id** theo cùng bộ lọc (vd `/ids`), hoặc endpoint thao tác nhận thẳng bộ lọc |
| Nhãn cho trang | Tra tên/mã danh mục **theo tập id của trang** (`WHERE id IN (...)`), không nạp cả bảng danh mục để map |
| Cổng liên module | Port/API trả danh sách cho module khác phải nhận tham số trang (`PhanTrang`/offset+limit) và trả kèm tổng. Thêm method mới, không phá method cũ đang có caller |

**Cấm (BE):**
- `repository.findAll()` / `findBy…()` không `Pageable` làm nguồn cho endpoint danh sách.
- Trả `List<T>` / `ApiResponse<List<T>>` cho dữ liệu tăng theo tenant.
- `PageResponse.ofList(...)` / `subList` trên tập **đã tải hết** (phân trang giả) — trừ §4.
- Lấy hết bằng cỡ lớn: `PageRequest.of(0, 1000)`, `Integer.MAX_VALUE`, `setMaxResults(5000)`, `LIMIT NULL`.
- Top-N không tổng (`gioiHan`, `limit 200`) cho popup — người dùng mất dòng mà không biết.
- Tham số cỡ không có trần (`int pageSize` / `gioiHan` thiếu `@Max`).
- N+1 khi dựng dòng của trang (truy vấn trong vòng lặp từng dòng) — gom theo tập id.

## 3. FE (`client`, `client-admin`)

| Hạng mục | Chuẩn |
|---|---|
| Gọi API | Luôn gửi `page`/`pageSize`; parse `PageResponse` bằng zod (`pageResponseSchema` của `@platform/search`). Không parse `z.array(...)` cho dữ liệu tăng theo tenant |
| Lưới | `CommonListTable` với `pagination` **controlled** (`current`, `pageSize`, `total = pagination.totalItems`, `onChange`) — engine `chungTu`/`catalog` (`serverList`)/`useServerListState`. Mặc định `BR1_PAGE_SIZE` (20), cỡ `BR1_PAGE_SIZE_OPTIONS` ([10,20,50,100]), hiện "đầu–cuối trên tổng", ô "Tới … Trang" khi > 5 trang |
| Đổi bộ lọc / từ khoá / cỡ trang | Về trang 1. Tìm kiếm và lọc cột gửi lên server, không lọc trên trang đang có |
| Combogrid / picker danh mục master-data | `@domain-kit` `danhMucComboGrid` (`useNguonDanhMucTrang`) — tìm + trang server, vẫn **tải trễ** (§17 `client/CLAUDE.md`) |
| Combogrid nguồn tuỳ biến | `CommonComboGrid` chế độ `serverPagination` + hook `useServerComboGrid` |
| Popup chọn tham chiếu / nguồn | `ReferencePickerModal` chế độ `server`; nguồn chọn nhanh dùng `SourcePagedSearch` |
| Giữ lựa chọn xuyên trang | Lưu id (và bản ghi) đã tick ngoài dữ liệu trang; "chọn tất cả" hỏi endpoint id của BE |
| Nhãn của giá trị đang giữ | Dùng mã/tên trên DTO (snapshot) hoặc tra **một** bản ghi theo id — không tải cả danh mục chỉ để hiện nhãn |
| Dòng tổng | Lấy `summary` từ BE, không cộng trên trang |

**Cấm (FE):**
- Vòng lặp tải hết mọi trang (`fetchAllPages`, `napHet`, `napTatCaTrang`, `duyetHetTrang`…) làm nguồn cho lưới/ô chọn.
- `pageSize: 1000` / `9999` / cỡ lớn để "lấy hết"; gọi endpoint `tim-kiem` mà **không gửi `page`** (BE trả trang 1 ⇒ mất dòng im lặng).
- `createSearchApi.listAll` ngoài Xuất Excel.
- Phân trang client (`pagination` không có `total` từ server, `slice`) hoặc `pagination={false}` trên dữ liệu tăng theo tenant.
- `CommonComboGrid`/`CommonSelectBox` với `rows`/`options` nạp sẵn toàn bộ danh mục tăng theo tenant.

## 4. Ngoại lệ được phép (ghi comment lý do tại chỗ)

| Trường hợp | Điều kiện |
|---|---|
| Danh mục nhỏ, cố định của hệ thống | Enum, loại chứng từ, tỉnh/thành, cấu hình cột (`/cot`), quyền — số dòng không tăng theo dữ liệu tenant |
| Dòng chi tiết của **một** chứng từ (BR21) | Bị chặn bởi id cha (lưới nhập liệu, tab hạch toán/thuế/tham chiếu/đính kèm của 1 chứng từ). Cho phép `PageResponse.ofList` hoặc phân trang client |
| Xem dữ liệu ghi sổ / thông tin hạch toán / xem trước của 1 chứng từ | Giữ như hiện tại (chốt 2026-10-07) |
| Xuất Excel / in / báo cáo tổng hợp | Được tải toàn tập (vd `listAll`, `pageSize = null` ⇒ toàn tập) nhưng **phải có trần** (vd 100.000 dòng) và chỉ dùng cho file xuất, không cho lưới |
| Nghiệp vụ cần toàn tập để tính | Vd tự phân bổ/đối trừ trên các khoản còn lại của **một** đối tượng. Phải ghi rõ vì sao và tập bị chặn bởi gì; ưu tiên đẩy phép tính lên BE |
| Tài khoản (`/tai-khoan`) | Đang chấp nhận nạp cả bảng (`useNguonDanhMucCaBang`) vì cỡ vài trăm dòng — chỉ đến khi BE master-data mở phân trang |

Ngoại lệ ngoài bảng này → **hỏi user**, không tự đặt.

## 5. Kiểm tra trước khi báo hoàn thành

- BE: unit test `@Tag("unit")` cho mỗi endpoint danh sách mới/sửa — trang 2 trả đúng `offset`, `totalItems` là tổng thật, `pageSize` vượt trần bị chặn, `summary` tính trên toàn tập.
- FE: test hồi quy — request có `page`/`pageSize`; bấm sang trang 2 gửi `page: 2`; hiện "đầu–cuối trên tổng"; giữ lựa chọn xuyên trang (nếu có chọn).
- Soát nhanh code mình vừa viết (không quét cả repo):

```bash
# BE — dấu hiệu tải hết / phân trang giả trong file vừa sửa
git diff --name-only | grep '\.java$' | xargs grep -nE 'findAll\(\)|PageRequest\.of\(0, *[0-9]{4,}|Integer\.MAX_VALUE|ofList\(|LIMIT NULL|ApiResponse<List<'
# FE — dấu hiệu tải hết / phân trang client trong file vừa sửa
git diff --name-only | grep -E '\.tsx?$' | xargs grep -nE 'pageSize: *[0-9]{3,}|fetchAll|napHet|napTatCaTrang|listAll\(|pagination=\{false\}|z\.array\('
```

Mỗi dòng khớp phải thuộc §4 (có comment lý do), hoặc sửa.

## 6. Khi review (`/review-code`)

Endpoint/lưới/picker danh sách mới không phân trang ở server, hoặc rơi vào một mục "Cấm" ở §2/§3 mà
không có lý do thuộc §4 ⇒ **Major**. Trả `List` cho dữ liệu tăng theo tenant ở endpoint public ⇒ **Blocker**.
