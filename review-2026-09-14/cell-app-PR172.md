# Review PR #172 — `ospgroupvn-pmkt/cell-app`

**Chế độ: NHANH** (chỉ đọc + kiểm tĩnh bằng git/grep). **KHÔNG** chạy test/build/gradlew,
**KHÔNG** tạo worktree, **KHÔNG** merge thử, **KHÔNG** đăng comment lên PR (user yêu cầu chỉ ghi file).

| Mục | Giá trị |
|---|---|
| Tiêu đề | `update chung tu mua hang va phan bo chi phi` |
| Tác giả | duccanh95hp |
| Head → Base | `feature/hoa-don-mua-hang-dich-vu-2.0` (`1b13273`) → `develop` (`aab533e`) |
| merge-base | `8b7fe3a` |
| Quy mô | 3 file · +49 / −5 · 1 commit |
| Migration trong diff | không có |
| Test trong diff | không có |

Toàn bộ diff nằm trong `cell-app/src/main/java/vn/vtt/pmkt/cell/chung_tu_mua_hang/internal/` —
không chạm `master_data/**`, `client/legacy/**`, `pmkt-docs/ba/Phase_2/**`.

## Tổng hợp findings

| Mức | Số lượng | Mã |
|---|---|---|
| Blocker | 2 | B1, B2 |
| Major | 5 | M1–M5 |
| Minor | 3 | m1–m3 |
| Nit | 2 | n1, n2 |

---

## Blocker

### B1 — CTE `source_cost` thiếu bộ lọc dòng CPMH ⇒ `tongChiPhiNguon` bị thổi phồng

`ChungTuMuaHangRepositoryImpl.java:841-855` (CTE `source_cost`)

Cùng một công thức "tổng chi phí nguồn" đã tồn tại ở **3 chỗ** trong chính file này, và cả 3 bản cũ
đều kèm đủ bộ lọc dòng chi phí mua hàng:

- `:766-800` (`nguonChiPhi`, nguồn dữ liệu của popup chọn chứng từ nguồn)
- `:1103-1122` (`khoaNguonChiPhi`, mốc kiểm "vượt số còn lại" khi lưu)

```
and d.loai_dong_hang=true
and lower(coalesce(d.loai_vat_tu, '')) in ('dichvu', 'dv')
and (coalesce(d.la_cpmh, false)=true or ct.loai_nghiep_vu in ('DichVu','DichVuChiPhi'))
```

CTE mới **chỉ giữ** `d.loai_dong_hang = true` (`:854`), bỏ cả `loai_vat_tu in ('dichvu','dv')` lẫn
`la_cpmh = true or loai_nghiep_vu in (...)`.

- **Trigger**: mở lại một chứng từ mua hàng đã lưu phân bổ, mà chứng từ nguồn có cả dòng hàng hoá
  thường (không phải dịch vụ / không `la_cpmh`).
- **Actual**: `tongChiPhiNguon` = tổng **mọi** dòng của chứng từ nguồn.
- **Expected**: đúng bằng `tongChiPhi` mà popup `nguonChiPhi` đang hiển thị cho cùng chứng từ đó.
- **Hậu quả**: cùng một chứng từ nguồn hiện **hai con số tiền khác nhau** trên cùng màn (popup chọn
  nguồn vs lưới phân bổ đã lưu); người dùng thấy "còn lại" ảo rồi bị BE chặn bằng
  `ALLOCATION_EXCEEDS_REMAINING` (`:949`) — vì mốc chặn dùng công thức đủ lọc ở `:1103`.

### B2 — CTE `source_allocated` không loại trừ chính chứng từ đang mở ⇒ `conLaiNguon` sai

`ChungTuMuaHangRepositoryImpl.java:856-861, 869`

Định nghĩa "đã phân bổ" dùng để tính **còn lại** ở hai nơi hiện có đều **loại trừ** chứng từ đích
hiện tại:

- `nguonChiPhi:788-793` — `and pb.chung_tu_mua_hang_id <> :targetDocumentId`
- `tongDaPhanBoKhac:1154-1167` — `and pb.chung_tu_mua_hang_id<>:targetDocumentId`

CTE mới cộng **toàn bộ** allocation của chứng từ nguồn, kể cả phần do chính chứng từ đang mở đã lưu.

- **Trigger**: mở lại chứng từ vừa lưu phân bổ hết số dư của một nguồn.
- **Actual**: `daPhanBoNguon` bao gồm cả phần của chính mình ⇒ `conLaiNguon` = 0
  (`greatest(sc.total - sa.total, 0)` ở `:869`).
- **Expected**: `conLai` giống popup chọn nguồn — tức số còn lại **chưa kể** phần của chứng từ này,
  để người dùng sửa/tăng được số đã phân bổ.
- **Hậu quả**: sửa chứng từ đã lưu luôn thấy "còn lại 0"; nếu FE dùng `conLaiNguon` để chặn nhập thì
  không sửa tăng được số phân bổ đã lưu. Đây là khác biệt ngữ nghĩa cần **BA chốt** (không có spec
  trong `docs/doing/` cho epic này — xem §Lớp C), nhưng dù chốt cách nào thì hai con số hiển thị
  cạnh nhau hiện đang mâu thuẫn.

---

## Major

### M1 — Định nghĩa thứ ba của "đã phân bổ": cột tiền khác với `capNhatLuyKeNguon`

`:857` dùng `sum(so_tien_phan_bo)`. `capNhatLuyKeNguon:1130-1137` — nơi ghi `luy_ke_da_phan_bo` vào
chứng từ nguồn — dùng `coalesce(nullif(so_tien_phan_bo_hach_toan,0), so_tien_phan_bo_quy_doi,
so_tien_phan_bo, 0)`. Chứng từ ngoại tệ (có `so_tien_phan_bo_hach_toan`) sẽ cho **hai giá trị
"đã phân bổ" khác nhau** giữa lưới phân bổ và cột luỹ kế của chứng từ nguồn. Chọn một định nghĩa
duy nhất và dùng lại (hàm/fragment SQL chung).

### M2 — Hai CTE quét toàn bảng, không lọc tenant và không thu hẹp theo chứng từ (lỗi hay gặp #4)

`:841-861`. `source_cost` gom nhóm **toàn bộ** `pur_chung_tu_mua_hang ⋈ ..._chi_tiet` của **mọi
tenant**; `source_allocated` gom **toàn bộ** `pur_phan_bo_chi_phi_mua_hang`. Chỉ sau đó mới lọc bằng
điều kiện join `sc.tenant_id=pb.tenant_id` (`:876-878`). Kết quả đúng, nhưng chi phí là một lần
aggregate toàn bảng **mỗi lần mở một chứng từ** (`phanBoChiPhi` được gọi ở
`ChungTuMuaHangCrudService:359` khi xem chi tiết và ở `khoaVaLayPhanBoDeGhiSo:1067` khi ghi sổ).
Cần `where tenant_id=:tenantId` trong cả hai CTE và thu hẹp theo tập `source_document_id` của chứng
từ đang mở (`where id in (select source_document_id from pur_phan_bo_chi_phi_mua_hang where
tenant_id=:tenantId and chung_tu_mua_hang_id=:documentId and da_xoa=false)`).

### M3 — Sửa `sourceLineId` ở `:989` đổi luôn ngữ nghĩa cột `chi_tiet_dich_vu_id`, trái javadoc, không có validate

`:978-989`. Tham số `:sourceLineId` được bind vào **hai cột** trong cùng INSERT: `chi_tiet_dich_vu_id`
(`:982`) và `source_line_id` (`:984`).

1. `LuuPhanBoChiPhiRequest` javadoc nói rõ *"sourceLineId được giữ để tương thích hợp đồng hiện tại
   và mang cùng giá trị với sourceDocumentId; **backend chuẩn hóa theo chứng từ khi lưu**"*. PR bỏ
   đúng bước chuẩn hoá đó nhưng **không sửa javadoc** — code và hợp đồng viết trong DTO nay mâu thuẫn.
2. Không có validate `sourceLineId` thuộc `sourceDocumentId`; giá trị client gửi vào thẳng DB, trong
   khi `chi_tiet_dich_vu_id` được khai là *XFK `pur_chi_tiet_chung_tu_mua_hang(id)`*
   (`V1__create_database.sql:15102`).
3. `NguonChiPhiMuaHangDto` (popup nguồn) **vẫn** trả `ct.id as source_line_id` (`:765`), nên ở luồng
   FE chuẩn giá trị không đổi ⇒ bản sửa này **không có tác dụng thực tế**, chỉ mở đường cho dữ liệu
   lạ. Hai đầu của cùng một hợp đồng đang lệch nhau.
4. Unique index `uq_pur_phan_bo_active_business_key` (`V1001__pur_bao_toan_identity_va_concurrency.sql:400-406`)
   dùng `coalesce(source_line_id, chi_tiet_dich_vu_id, ...)` làm business key. `source_line_id` trước
   đây luôn = document id nên chốt dedup ổn định; nay nó biến thiên ⇒ **nới lỏng** chốt chống trùng
   nguồn/đích/loại chi phí mà không có quyết định nghiệp vụ đi kèm.

Không có migration/data-fix cho các dòng đã lưu theo quy tắc cũ.

### M4 — Không có test cho thay đổi hành vi lẫn bug fix (checklist BE §G)

`git diff --name-only 8b7fe3a origin/pr/172 -- src/test` ⇒ rỗng. PR vừa đổi cách tính tiền (B1, B2)
vừa sửa một bug ghi dữ liệu (`:989`) mà không để lại test hồi quy `@Tag("unit")` nào. Bug `:989`
chính là loại lỗi phải có test chốt lại.

### M5 — Hardcode giá trị enum và nhân bản công thức (luật 1 · lỗi hay gặp #7)

`:845-847` chép nguyên literal `'TrongNuoc'` / `'NhapKhau'` — enum `HinhThucMuaHang` đã có
(`internal/model/HinhThucMuaHang.java:16`). Đây là **bản sao thứ tư** của cùng công thức tổng chi phí
trong một file (`:766`, `:845`, `:1103`), và chính việc nhân bản đã đẻ ra B1. Tách thành một hằng số
fragment SQL trong module (`internal/constant/`) rồi `formatted`/nối lại ở cả bốn nơi.

---

## Minor

- **m1** — `PhanBoChiPhiDto.java:23-28`: 6 field mới (`ngayHachToanNguon`, `ngayChungTuNguon`,
  `nhaCungCapNguon`, `tongChiPhiNguon`, `daPhanBoNguon`, `conLaiNguon`) là dữ liệu **denormalize** của
  chứng từ nguồn nhét vào record có javadoc "Bản ghi phân bổ đã lưu". Không field nào có javadoc;
  javadoc lớp không được cập nhật để nói record nay còn mang snapshot nguồn.
- **m2** — `:875`: `join pur_chung_tu_mua_hang src on src.id=pb.source_document_id` vẫn thiếu
  `src.tenant_id=pb.tenant_id` và `src.da_xoa=false` (lỗi có sẵn, nhưng PR này kéo thêm 3 cột
  `ngay_hach_toan`, `ngay_chung_tu`, `ten_nha_cung_cap` từ `src` nên phạm vi ảnh hưởng rộng hơn).
- **m3** — `NguonChiPhiMuaHangDto` thêm `ngayHachToan` nhưng bộ lọc `tuNgay`/`denNgay` và `order by`
  của `nguonChiPhi` (`:761-762`, `:806`) vẫn chỉ theo `ngay_chung_tu`. Nếu grid hiển thị ngày hạch
  toán thì lọc/sắp xếp lệch với cột người dùng nhìn thấy — cần BA xác nhận (BR8).

## Nit

- **n1** — `:826-827`, `:989`: thừa một dấu cách đầu dòng, vỡ canh lề so với các dòng xung quanh
  (khác biệt thuần format lẫn trong diff nghiệp vụ).
- **n2** — Commit `update chung tu mua hang va phan bo chi phi` không theo `<type>(<scope>): <mô tả>`
  (luật 8); PR body rỗng, không nêu phạm vi/nguồn nghiệp vụ.

---

## Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục Modulith | ✅ 3 file đều trong `chung_tu_mua_hang/internal/{dto,repository}`, package `vn.vtt.pmkt` đúng, không thêm `api/`, không file phẳng ra gốc module |
| 2 | Không đánh lại version migration | ✅ N/A — diff không có file `db/migration` (max trên `develop` = V1122, không tranh chấp) |
| 3 | Chưa test lại sau khi merge | ✅ N/A — `develop` đi trước 4 commit, `comm -12` giữa hai tập file thay đổi = **0 file giao nhau** |
| 4 | N+1 / chưa tối ưu | ⚠ **M2** (2 CTE aggregate toàn bảng, không lọc tenant/không thu hẹp theo chứng từ) |
| 5 | Chưa tận dụng BaseController / BaseEntity | ✅ N/A — không có controller/entity/repository mới; PR chỉ sửa `…RepositoryCustom` impl và 2 record DTO |
| 6 | Chưa tận dụng base FE | ✅ N/A — PR không chạm `client/` |
| 7 | Constant đặt sai chỗ | ⚠ **M5** (literal `'TrongNuoc'`/`'NhapKhau'` và công thức tổng chi phí nhân bản, không thành hằng số module) |

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng | ⚠ **M5** (hardcode magic value). Không secret; không đụng Controller/ApiResponse; không try/catch nuốt lỗi; không chạm vùng đóng băng |
| B — Kiến trúc & 7 lỗi | ⚠ **M2, M5** — chi tiết ở bảng trên |
| C — Nghiệp vụ & truy vết | ⚠ **B1, B2, M1, M3**. `trace.sh` / `msg.sh`: **NOT-RUN** — không có thư mục spec cho `chung_tu_mua_hang` / phân bổ chi phí trong `docs/doing/` (chỉ có `PMKT-E-00542-hoa-don-mua-hang-api`, không phải thư mục `…-spec` có `02-rules.md`), và diff không mang mã `R-…`/`MSG_…` mới. Không đoán bừa một PYC |
| D — Vệ sinh diff & Git | ⚠ **n1, n2**. Cổng cây commit: `git status --porcelain` **sạch**, không có file `??` trong `src/`; diff không đụng barrel/`index`; không có rename |

## BR đã đọc

- **BR7** (số liệu / làm tròn) — liên quan B1/B2/M1: BR7.3 yêu cầu lưu giá trị đầy đủ, chỉ làm tròn
  khi hiển thị; vấn đề ở đây không phải làm tròn mà là **ba định nghĩa khác nhau của cùng một số**.
- **BR19** (kiểm tra trùng) — liên quan M3.4: chốt dedup của bảng phân bổ bị nới lỏng.
- **Chưa đọc** (không cần cho các finding trên, nêu để minh bạch): BR4 9 12 17 33 36 37 41 42 48 49
  (chứng từ & hạch toán), BR8 (ngày tháng — chỉ chạm ở m3), BR18 20 28 29 46.

## Lệnh đã chạy

```
gh pr view 172 --json ...
git merge-base origin/develop origin/pr/172
git diff --stat|--name-status <MB> origin/pr/172
git diff <MB> origin/pr/172            # toàn bộ diff, 3 file
git show origin/pr/172:<file>          # đọc bản head của repository impl, DTO, migration
git grep -n "PhanBoChiPhiDto|NguonChiPhiMuaHangDto|sourceLineId|TrongNuoc" origin/pr/172 -- src
git ls-tree -r --name-only origin/develop -- src/main/resources/db/migration   # max = V1122
git rev-list --count <MB>..origin/develop            # = 4
comm -12 <(...develop...) <(...pr/172...)            # = rỗng
git status --porcelain                               # sạch
./docs/rules/br.sh 7 19
```

## Chưa làm

- Cổng `cd cell-app && ./gradlew unitTest`: **NOT-RUN — chế độ nhanh**.
- Không tạo worktree, không merge thử (§3a báo 0 file giao nhau), không đo baseline.
- Không kiểm được FE có dùng `conLaiNguon`/`tongChiPhiNguon` để chặn nhập hay không (repo `client/`
  ngoài phạm vi PR) — mức độ nghiêm trọng thực tế của B2 phụ thuộc điều này.

## Kết luận

**REJECT** — có Blocker: **B1**, **B2** (số tiền "tổng chi phí nguồn" và "còn lại" hiển thị khi mở
lại chứng từ mâu thuẫn với chính hai công thức chuẩn đang dùng ở nơi khác trong cùng file, trong đó
một cái là mốc chặn khi lưu).

Ngoài ra còn **M1, M2, M3, M4, M5** cần xử lý trước khi merge; **m1–m3** và **n1, n2** tuỳ tác giả.

⚠ Cổng test/build **chưa chạy** (chế độ nhanh) — kết luận này dựa hoàn toàn trên đọc code và kiểm
tĩnh bằng git. B2 và m3 chạm ngữ nghĩa nghiệp vụ chưa có spec ⇒ theo luật 9 cần **BA chốt**, không
tự quyết.

**Chưa đăng lên PR** — user yêu cầu rõ: chỉ ghi file, không `gh pr comment` / `gh pr review`.
