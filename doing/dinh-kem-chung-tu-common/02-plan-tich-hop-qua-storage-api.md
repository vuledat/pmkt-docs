# Plan — Đính kèm chứng từ qua **`/api/storage/files` có sẵn**, type riêng cho từng nghiệp vụ

> Ngày: 2026-08-22 · **Quyết định của user:** không code module `cell/dinh_kem_chung_tu`, không bảng
> nối. Dùng thẳng bộ REST công khai `/api/storage/files` (`FileStorageController`), **truyền type
> riêng cho từng nghiệp vụ**.
> Khảo sát hiện trạng mọi API đang dùng `str_file`: **Phụ lục A** cuối tài liệu.
> FE hiện trạng: [`IMPLEMENT.md`](IMPLEMENT.md).
> **Tài liệu KẾ HOẠCH — chưa code.**

---

## 1. Hình dạng lời giải

**"Type riêng cho từng nghiệp vụ" = `FileGroup`, và mã group LÀ mã chức năng của màn
(`MaChucNang`).** `file_group` vốn đã là (a) phân vùng logic, (b) khoá tra **giới hạn dung lượng +
whitelist MIME riêng**, (c) đoạn thứ 2 của `object_key`, (d) hàng rào chặn client bịa thư mục — thêm
đúng một điều: giá trị không tự đặt mà lấy từ `MaChucNang`, cùng chuỗi đang định danh màn đó trong
`iam_quyen` và trong mọi `QuyenChecker.require(...)`. Một màn một tên; hai tên là hai thứ sẽ trôi
khỏi nhau ngay lần đổi tên đầu tiên. Mỗi nghiệp vụ một hằng số enum:
`BAN_HANG_HOA(MaChucNang.BAN_HANG_HOA)` → `"BanHangHoa"`, rồi `THU_CHI`, `NHAP_KHO`…

**Thiếu đúng một mảnh:** `str_file` không biết tệp thuộc **chứng từ nào**. Group cho biết *loại*
nghiệp vụ, không cho biết *bản ghi*. ⇒ thêm **3 cột** vào `str_file` và **1 filter** vào endpoint
`GET` đã có.

```
Trước:  str_file( … , file_group )                     ← biết "tệp của bán hàng"
Sau:    str_file( … , file_group , doi_tuong_id , ten_hien_thi , thu_tu )
                                   ↑ biết "của ĐÚNG chứng từ nào"
```

Không bảng mới · không module mới · không controller mới (chỉ **một** endpoint bổ sung vào chính
`FileStorageController`, xem §3.3).

### 1.1 Ba hệ quả phải chấp nhận — nêu trước, không giấu ở cuối

| # | Hệ quả | Vì sao không tránh được | Đối phó |
|---|---|---|---|
| 1 | **Một tệp chỉ thuộc MỘT chứng từ** | `str_file` là bảng 1-dòng-1-object; không có bảng nối thì không có quan hệ N–N. Gắn cùng một hợp đồng vào 2 chứng từ ⇒ phải tải lên 2 lần | BR02/BR04 không đòi tái dùng tệp ⇒ không mất chức năng nào của SCR |
| 2 | **"Gỡ tệp khỏi chứng từ" = xoá tệp** | Không có dòng nối để xoá riêng ⇒ `DELETE /api/storage/files/{id}` xoá mềm chính `str_file` | Đúng BR03 ("Gỡ tệp khỏi chứng từ") + BR29.1 (xoá mềm, object trên MinIO vẫn giữ) |
| 3 | ⚠ **BR03 không chặn được ở tầng API** — "chứng từ đã ghi sổ ⇒ chặn xoá, báo `MSG_COMMON_001`" | `common/storage` **không được** phụ thuộc module nghiệp vụ (`package-info.java`); nó không thể hỏi "chứng từ này ghi sổ chưa" mà không phá đúng bất biến đó — cũng chính là thứ khiến ta bỏ module riêng | FE **đã** ẩn nút Xoá khi `daGhiSo` (đã code). Chốt chặn phía server **để lại**, ghi rõ là lệch BR03 ở lớp API. Xem **Q3** |

`str_file` không phải chỗ giữ nghiệp vụ, nên hệ quả 3 là cái giá thật của việc bỏ module nghiệp vụ.
Đó là đánh đổi có chủ ý, không phải sót.

---

## 2. Thay đổi Backend

### 2.1 Migration `V1036__str_file_doi_tuong.sql` (+ rollback)

Mới nhất hiện tại là `V1035`.

```sql
ALTER TABLE public.str_file
    ADD COLUMN doi_tuong_id   uuid,
    ADD COLUMN ten_hien_thi   varchar(255),
    ADD COLUMN thu_tu         integer;
```

| Cột | Kiểu | Null | Ý nghĩa |
|---|---|---|---|
| `doi_tuong_id` | `uuid` | **NULL được** | Id bản ghi nghiệp vụ sở hữu tệp. **XFK đa hình — KHÔNG enforce** (ADR-05: một cột không FK tới 20 bảng). `NULL` = **tệp chưa gắn** (vừa tải lên, người dùng chưa bấm Lưu) — đây cũng là marker cho job dọn ở §5 |
| `ten_hien_thi` | `varchar(255)` | NULL | Tên sau khử trùng BR02 (`hoadon.pdf` → `hoadon (1).pdf`). **Bắt buộc tách khỏi `original_name`**: cột đó `updatable = false` (entity `StoredFile:34`) và là tên gốc người dùng tải lên, dùng cho `Content-Disposition`. `NULL` ⇒ đọc rơi về `original_name` |
| `thu_tu` | `integer` | NULL | Thứ tự hiển thị trong tab. Lưu thật, không `row_number()` lúc đọc |

Ba cột **nullable**, không default ⇒ **không đụng** dòng cũ và mọi consumer khác (notice, avatar,
report, invoice) không thấy gì thay đổi.

Index:

```sql
-- Chiều đọc chính: tab Đính kèm của MỘT chứng từ
CREATE INDEX idx_str_file_doi_tuong
    ON public.str_file (tenant_id, file_group, doi_tuong_id)
    WHERE da_xoa = false AND doi_tuong_id IS NOT NULL;

-- Job dọn tệp mồ côi (§5) — quét đúng nhánh chưa gắn
CREATE INDEX idx_str_file_chua_gan
    ON public.str_file (tenant_id, file_group, ngay_tao)
    WHERE da_xoa = false AND doi_tuong_id IS NULL;
```

Kèm `COMMENT ON COLUMN` cho cả ba, nêu rõ: `doi_tuong_id` là XFK **mềm** (DB không chặn xoá chứng từ
còn tệp, không cascade), và `NULL` nghĩa là *chưa gắn*, không phải *không có chủ*.

**Không cần** đụng RLS/policy/trigger/GRANT — bảng đã có đủ từ V331.

### 2.2 `FileGroup` — một hằng số cho mỗi nghiệp vụ

```java
CHUNG_TU_BAN_HANG("chung-tu-ban-hang"),
PHIEU_THU_CHI("phieu-thu-chi"),
PHIEU_NHAP_KHO("phieu-nhap-kho"),
// … thêm dần theo từng màn được đấu nối
```

Đợt này **chỉ thêm `CHUNG_TU_BAN_HANG`** (màn thí điểm). Mỗi group tự khai giới hạn ở
`application.yml` — đây chính là chỗ BR02 sống:

```yaml
pmkt:
  storage:
    groups:
      chung-tu-ban-hang:
        max-size: ${STORAGE_GROUP_CTBH_MAX_SIZE:5MB}          # BR02
        content-types: ${STORAGE_GROUP_CTBH_CONTENT_TYPES:application/pdf,\
          application/msword,application/vnd.ms-excel,\
          application/vnd.openxmlformats-officedocument.wordprocessingml.document,\
          application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,\
          image/jpeg,image/png,image/gif,image/bmp,\
          application/zip,application/x-rar-compressed,application/x-7z-compressed,\
          application/xml,text/xml,text/plain,text/csv}
```

Lợi thế của "type theo nghiệp vụ": mai kia ngân quỹ muốn 10MB, kho muốn chỉ nhận PDF — đổi YAML, không đụng code.

### 2.3 ⚠ `FileGroup.Mime.EXTENSION_BY_MIME` — không sửa là **500**

`EXTENSION_BY_MIME` hiện là `Map.of(...)` với **8 cặp** (pdf, png, jpg, webp, xml×2, xlsx, docx) và
`extensionFor()` **NÉM** `IllegalArgumentException` khi không map được. BR02 có 16 phần mở rộng ⇒
upload `.zip/.txt/.csv/.gif/.bmp/.doc/.xls/.rar/.7z` sẽ trả **500** ngay lần đầu.

Việc: đổi sang `Map.ofEntries` (trần của `Map.of` là 10 cặp) + bổ sung **9 cặp**:
`doc · xls · gif · bmp · zip · rar · 7z · txt · csv`.

### 2.4 Kiểm **phần mở rộng** — cộng thêm, không thay kiểm MIME

BR02 và cả hai message lỗi của SCR đều phát biểu theo **phần mở rộng**, trong khi Tika đọc magic
bytes nên `.csv` và `.txt` đều ra `text/plain`, còn `.docx/.xlsx` đều là ZIP container.

Luật: **cả hai phải qua** — phần mở rộng ∈ danh sách của group **và** MIME (Tika) ∈ whitelist. Giữ
nguyên khả năng chống giả mạo hiện có (đổi tên `.exe` → `.png` vẫn bị chặn ở lớp MIME).

Khai danh sách đuôi cùng chỗ với MIME: `pmkt.storage.groups.<group>.extensions`.

### 2.5 `FileDto` — 4 trường mới

```java
public record FileDto(
        UUID id, String group, String objectKey, String name, String contentType, long size,
        String contentHash, String status, Instant createdAt, Instant updatedAt, UUID createdBy,
        String downloadUrl,
        // ── mới ──────────────────────────────────────────────
        UUID doiTuongId,        // null = chưa gắn
        String tenHienThi,      // null ⇒ client rơi về `name`
        Integer thuTu,
        String nguoiTaoTen) {}  // họ tên, KHÔNG phải uuid — cho cột "Người tải lên" của Figma
```

`nguoiTaoTen` lấy qua `NguoiDungLookupApi.hoTenTheoId(Collection<UUID>)` — cổng in-JVM **đã có sẵn**
(`@NamedInterface("nguoi_dung_api")`), gọi **một lượt cho cả trang**, không N+1.

⚠ Đây là phụ thuộc mới `common.storage → platform_iam.nguoi_dung.api`. Là IAM chứ không phải nghiệp
vụ kế toán, nhưng vẫn phải khai trong `package-info.java` của storage và cập nhật javadoc "must NOT
depend on any **business** module". Không muốn phụ thuộc này thì bỏ `nguoiTaoTen`, đổi lại **mất cột
"Người tải lên"** của Figma — xem **Q2**.

`FileDto` là record, thêm trường ⇒ mọi `new FileDto(...)` phải cập nhật. Đã kiểm: chỉ dựng ở
`FileStorageServiceImpl.toDto` và `withDownloadUrl`. `common/notice` chỉ **đọc** `FileDto` ⇒ không vỡ.

---

## 3. Hợp đồng REST sau thay đổi

Cột **Đổi gì** so với hôm nay:

| Method | Path | Quyền | Đổi gì |
|---|---|---|---|
| `POST` | `/api/storage/files?group=…` + form `doiTuongId?` | `File.Create` | **thêm** tham số `doiTuongId` tuỳ chọn (màn Sửa: chứng từ đã có id ⇒ gắn ngay). Bỏ trống ⇒ tệp ở trạng thái *chưa gắn* |
| `GET` | `/api/storage/files?group=…&doiTuongId=…` | `File.View` | **thêm** filter `doiTuongId` — đây là lời gọi của tab Đính kèm |
| `POST` | `/api/storage/files/gan-doi-tuong` | `File.Create` | **MỚI** — xem §3.3 |
| `GET` | `/api/storage/files/{id}/content` | `File.View.Detail` | *không đổi* — xem/tải xuống |
| `DELETE` | `/api/storage/files/{id}` | `File.Delete` | *không đổi* — xoá mềm = gỡ tệp khỏi chứng từ (hệ quả 2) |
| `GET` `/{id}` · `POST /find-by-ids` · `/upload-multiple` | | | *không đổi*, tab không dùng |

### 3.1 `GET` — thêm đúng 2 predicate

`FileStorageTxOps.search` đã dựng bằng **Specification** (cố ý, javadoc giải thích vì sao không dùng
JPQL `:param IS NULL`), nên thêm filter là 6 dòng đúng chỗ:

```java
if (doiTuongId != null) {
    predicates.add(cb.equal(root.get("doiTuongId"), doiTuongId));
}
```

Chuỗi ký: `search(String group, String search, UUID doiTuongId, Pageable)` → `FileStorageService.list`
→ `FileStorageController.list`. Vẫn trả `PageResponse<FileDto>` như cũ.

⚠ Specification hiện **ép `status = READY`** — đúng cho tab (tệp `UPLOADING`/`FAILED` không nên hiện).

### 3.2 Thứ tự đọc

Tab đọc theo `thu_tu` rồi `ngay_tao`. Endpoint `GET` hiện sort mặc định `ngayTao DESC` ở controller.
⇒ khi có `doiTuongId`, đổi sang `Sort.by(ASC, "thuTu", "ngayTao")`.

### 3.3 `POST /api/storage/files/gan-doi-tuong` — endpoint MỚI, và vì sao **bắt buộc**

Luồng **Thêm mới**: người dùng thả tệp **trước** khi chứng từ tồn tại (BR02 đòi tiến trình % và xem
trước ngay lúc thả) ⇒ lúc upload **chưa có `doiTuongId`**. Id chứng từ do DB sinh
(`gen_random_uuid()`), FE không đặt trước được. ⇒ phải có một lời gọi **gắn sau khi Lưu**.

```jsonc
POST /api/storage/files/gan-doi-tuong
{
  "group": "chung-tu-ban-hang",
  "doiTuongId": "uuid-của-chứng-từ-vừa-lưu",
  "tep": [ { "fileId": "uuid", "tenHienThi": "hoadon.pdf", "thuTu": 1 } ]
}
→ ApiResponse<Void>
```

Ngữ nghĩa **ĐỒNG BỘ (ghi đè)** cho đúng cặp `(group, doiTuongId)`:
1. tệp trong `tep` mà chưa gắn ⇒ set `doi_tuong_id` + `ten_hien_thi` + `thu_tu`;
2. tệp trong `tep` đã gắn đúng `doiTuongId` ⇒ chỉ cập nhật `ten_hien_thi`/`thu_tu`;
3. tệp đang gắn `doiTuongId` này nhưng **không** có trong `tep` ⇒ **xoá mềm** (người dùng đã gỡ);
4. `fileId` thuộc tenant khác / đã gắn chứng từ khác ⇒ **400**, không âm thầm cướp tệp.

Khử trùng `ten_hien_thi` (BR02) làm **ở đây** — server là nguồn sự thật; FE chỉ khử trước cho mượt,
hai tab mở song song thì chỉ server thấy cả hai.

⚠ **Không nằm trong transaction lưu chứng từ.** Lưu xong mà `gan-doi-tuong` hỏng (mạng, 403) ⇒ chứng
từ có nhưng tệp chưa gắn. Đối phó: FE báo lỗi rõ và cho bấm lại; tệp chưa gắn bị job §5 dọn sau 24h
nên không rác vĩnh viễn. Đây là cái giá của việc **không** móc vào `ChungTuTemplate`. Xem **Q4**.

### 3.4 Quyền

Toàn bộ tab chạy bằng `File.Create` · `File.View` · `File.View.Detail` · `File.Delete`
(`iam_quyen`, `la_he_thong = true`, seed `V2__seed_data.sql`).

⚠ **Phải kiểm và cấp 4 quyền này cho các vai trò kế toán ở P0**, nếu không tab **403 với mọi người
dùng thường** dù code đã xong. Và lưu ý: quyền là **theo tệp, không theo màn** ⇒ ai có `File.View` thì
đọc được tệp của mọi nghiệp vụ (kèm `group` + `doiTuongId` đúng). Lệch BR25 — xem **Q3**.

---

## 4. Thay đổi Frontend — chi tiết từng file

Base `@domain-kit/dinhKem` đã code xong theo hợp đồng cũ (`/api/chung-tu/dinh-kem`). Đổi sang hợp
đồng này chạm **7 file base + 4 file CTBH**. Cấu trúc, UI, i18n, BR01–BR04 **giữ nguyên** — chỉ đổi
tầng `api/` và một prop.

### 4.1 `constants/constants.ts`

| Bỏ | Thêm / đổi |
|---|---|
| `DINH_KEM_API_PATH` | — |
| `STORAGE_GROUP_DINH_KEM = 'document'` | bỏ hẳn — group giờ do **màn chủ truyền vào** (type theo nghiệp vụ) |
| | `STORAGE_GAN_PATH = '/api/storage/files/gan-doi-tuong'` |
| | `DINH_KEM_FETCH_SIZE = 100` — `GET` trả `PageResponse`; tab phân trang **client-side** (Figma vẽ phân trang trong tab), nên kéo một trang lớn |

`DUOI_TEP_CHO_PHEP` (16) · `DUNG_LUONG_TOI_DA_MB` (5) · `DUOI_NHOM_1` · `COT_WIDTH` **giữ nguyên**.

### 4.2 `api/dinhKemSchema.ts` — parse `FileDto`, không còn `DinhKemDto`

```ts
export const tepDinhKemSchema = z.object({
  id: z.string(),                    // = fileId. Không còn id dòng nối riêng
  name: z.string(),                  // original_name
  tenHienThi: z.string().nullish(),  // null ⇒ rơi về name
  size: z.number().nullish(),
  contentType: z.string().nullish(),
  status: z.string().nullish(),
  thuTu: z.number().nullish(),
  doiTuongId: z.string().nullish(),
  createdAt: z.string().nullish(),
  nguoiTaoTen: z.string().nullish(),
})
/** GET trả PageResponse — bọc thêm một lớp so với hợp đồng cũ. */
export const trangTepSchema = z.object({ data: z.array(tepDinhKemSchema) })
```

### 4.3 `api/dinhKemApi.ts`

| Hàm cũ | Thành |
|---|---|
| `docDinhKem(loai, doiTuongId)` → `GET /api/chung-tu/dinh-kem` | `docDinhKem(group, doiTuongId)` → `GET /api/storage/files?group=&doiTuongId=&pageSize=100&sort=` |
| `xoaDinhKem(id)` → `DELETE /api/chung-tu/dinh-kem/{id}` | `xoaDinhKem(fileId)` → `DELETE /api/storage/files/{fileId}` — **id giờ là fileId** |
| `taiTepLen(tep, group, onTienDo)` | `taiTepLen(tep, group, doiTuongId | null, onTienDo)` — gửi kèm `doiTuongId` khi đang Sửa |
| — | **mới** `ganDinhKem(group, doiTuongId, dong[])` → `POST /api/storage/files/gan-doi-tuong` |
| `docNoiDungTep(fileId)` | *không đổi* |
| `dinhKemQueryKey(loai, id)` | `dinhKemQueryKey(group, id)` |

### 4.4 `fields/types.ts`

- `DongDinhKem.id` và `.fileId` **gộp làm một** (`id === fileId`). Giữ cả hai tên để `cotDinhKem` và
  `useXemTep` không phải sửa, nhưng ghi rõ trong javadoc là cùng một giá trị.
- `GanDinhKemLenh` giữ nguyên `{ fileId, tenHienThi, thuTu }` — giờ là thân của `gan-doi-tuong`
  thay vì một nhánh của payload chứng từ.
- `GiaTriDinhKem.daLuu` đổi kiểu `DinhKemDto[]` → `TepDinhKem[]` (hình dạng `FileDto`).

### 4.5 `helpers/dongDinhKem.ts`

- `dungDongDinhKem`: đọc `tenHienThi ?? name`, `size`, `nguoiTaoTen`, `createdAt` thay vì
  `tenHienThi/dungLuong/nguoiTaiLen/thoiGianTaiLen`.
- `dinhKemGuiLen` **giữ nguyên chữ ký và test** — chỉ đổi nơi tiêu thụ: thân `gan-doi-tuong`.
- Thêm `coTepChuaGan(giaTri)` → dùng để quyết định có phải gọi `gan-doi-tuong` sau khi Lưu không.

### 4.6 `hooks/useDinhKem.ts`

- Nhận `group` thay `loai`; truyền `doiTuongId` vào `taiTepLen` khi có.
- `xacNhanXoa`: dòng **đã gắn** ⇒ `DELETE /api/storage/files/{id}`; tệp mới trong phiên ⇒ vẫn phải
  gọi `DELETE` (tệp đã nằm trên MinIO rồi!) **cộng** bỏ khỏi `moi`. **Khác bản hiện tại** — hiện tệp
  mới chỉ bị bỏ khỏi mảng và để job dọn; gọi `DELETE` ngay thì sạch hơn và người dùng thấy đúng.
- Thêm `ganSauKhiLuu(doiTuongId)` — màn chủ gọi sau khi Lưu thành công.

### 4.7 `components/DinhKemTab.tsx` · `DinhKemPanelTab.tsx`

- Prop `loai: string` → **`group: string`** (bắt buộc). Đây là "type riêng cho từng nghiệp vụ" mà FE truyền lên.
- Không đổi UI, không đổi i18n, không đổi luật ẩn/hiện.

### 4.8 `index.ts`

Export thêm `ganDinhKem` / `ganSauKhiLuu`; bỏ export `DINH_KEM_NAME` khỏi nhóm "payload" nếu CTBH
không còn nhét vào thân request (xem 4.10).

### 4.9 `test/`

- `dinhKemHelpers.test.ts`: đổi fixture `daLuu` sang hình dạng `FileDto`. **19 ca giữ nguyên ý nghĩa.**
- `dinhKemTab.render.test.tsx`: đổi prop `loai` → `group`. **8 ca giữ nguyên.**
- **Thêm** ca: gọi `gan-doi-tuong` đúng một lần sau khi Lưu, và không gọi khi không có tệp nào.

### 4.10 CTBH — 4 file

| File | Đổi gì |
|---|---|
| `constants/constants.ts` | `LOAI_DOI_TUONG_DINH_KEM = 'CHUNG_TU_BAN_HANG'` → `STORAGE_GROUP_CTBH = 'chung-tu-ban-hang'` (khớp `FileGroup.CHUNG_TU_BAN_HANG.code`) |
| `api/payload.ts` | **BỎ** `dinhKem: dinhKemGuiLen(...)` khỏi thân request — chứng từ không còn mang tệp; **bỏ 2 ca test** vừa thêm ở `payload.test.ts`, thay bằng ca ở tầng modal |
| `fields/types.ts` | giữ `dinhKem?: GiaTriDinhKem` trong form store (tab vẫn sống trong Form) |
| `components/ChungTuBanHangThemMoiModal.tsx` | sau khi `createMut`/`updateMut` trả về id ⇒ `await ganDinhKem(STORAGE_GROUP_CTBH, id, dinhKemGuiLen(form.getFieldValue('dinhKem')))`; hỏng thì **báo lỗi và không đóng popup**, để người dùng bấm Lưu lại |
| `components/DinhKemTab.tsx` (lớp nối) | đổi prop `loai` → `group` |

**Không đổi:** `XemNhanhTabs.tsx` (chỉ đổi tên prop), `chungTuModule.tsx`, i18n, CSS.

---

## 5. Job dọn tệp chưa gắn — đơn giản hẳn so với plan cũ

Không còn phải join hai bảng: **`doi_tuong_id IS NULL` chính là marker**.

```sql
UPDATE str_file SET da_xoa = true, ngay_xoa = now()
 WHERE da_xoa = false AND status = 'READY'
   AND doi_tuong_id IS NULL
   AND file_group IN (:cacGroupDinhKem)
   AND ngay_tao < now() - interval '24 hours';
```

`idx_str_file_chua_gan` phục vụ đúng truy vấn này. Ngưỡng 24h để không cắt ngang một popup mở lâu.
Khuôn job đã có sẵn: `accounting_core/khoa_so/internal/job` (`@ConfigurationProperties` + `@Scheduled`
chỉ bật ở profile `worker`).

**Bắt buộc có.** Người dùng thả 5 tệp rồi đóng popup ⇒ 5 object nằm lại MinIO vĩnh viễn.

---

## 6. Phân pha & cổng nghiệm thu

| Pha | Nội dung | Cổng |
|---|---|---|
| **P0** | Chốt Q1–Q5 (§8) · **kiểm quyền `File.*` đã cấp cho vai trò kế toán chưa** | user duyệt |
| ~~**P1 — BE storage lõi**~~ ✅ **XONG 2026-08-22** | `FileGroup.BAN_HANG_HOA(MaChucNang.BAN_HANG_HOA)` + config group `"[BanHangHoa]"` (5MB + 16 đuôi) + `Map.ofEntries` (+11 cặp) + kiểm phần mở rộng | `./gradlew unitTest` **BUILD SUCCESSFUL** — 1925 test, 0 đỏ; `DinhKemBanHangBr02Test` 7 ca + `FileStorageServiceImplTest` 27 ca |
| **P2 — BE schema + đọc** | `V1036` + rollback · 3 cột vào `StoredFile` · `FileDto` +4 trường · filter `doiTuongId` ở Specification · sort `thuTu` · `nguoiTaoTen` qua `NguoiDungLookupApi` | `unitTest` xanh · `ApplicationModules.verify()` (phụ thuộc mới sang `platform_iam`) |
| **P3 — BE gắn** | `POST /gan-doi-tuong` (4 nhánh ngữ nghĩa §3.3) + khử trùng `ten_hien_thi` + Postman `docs/json/dinh-kem-storage.postman.json` | `unitTest` xanh + gọi thử qua IntelliJ run config |
| **P4 — FE base** | 7 file `@domain-kit/dinhKem` theo §4.1–4.9 | `npx vitest run src/base/domainKit/dinhKem` + `npx vite build` |
| **P5 — FE CTBH** | 4 file theo §4.10 | cổng nhẹ FE + `npx vitest run src/features/banHang/chungTuBanHang` |
| **P6 — Nghiệm thu end-to-end** | Thêm mới: thả 3 tệp → Lưu → mở lại thấy đủ · Sửa: thêm/xoá tệp · Xem: chỉ đọc · panel Xem nhanh · BR02 chặn 6MB và `.exe` | user nghiệm thu trên màn thật (cần MinIO — **Q5**) |
| **P7 — Job dọn** | §5 | `unitTest` xanh + log một lượt chạy |
| **P8 — *(ticket riêng)*** | thêm `FileGroup` cho ngân quỹ/kho/CCDC… và đấu tab; backfill `cash_phieu_thu_chi_tep_dinh_kem` → `str_file.doi_tuong_id` rồi drop bảng nối cũ | đối soát số dòng trước/sau |

Chạy code **qua IntelliJ MCP, không Docker**. Test Testcontainers **không chạy được** trên máy này —
báo cáo phải ghi rõ.

---

## 7. Rủi ro

1. **`extensionFor()` ném ⇒ 500** (§2.3) — chặn bằng unit test duyệt đủ 16 đuôi. Đây là rủi ro số 1
   vì nó nổ ngay lần upload `.zip` đầu tiên.
2. **`gan-doi-tuong` ngoài transaction lưu chứng từ** (§3.3) — chứng từ có mà tệp chưa gắn. Giảm
   thiểu: FE không đóng popup khi bước gắn hỏng + job §5.
3. **BR03 không chặn được ở API** (§1.1 hệ quả 3) — chỉ FE ẩn nút. Ai gọi thẳng API vẫn xoá được tệp
   của chứng từ đã ghi sổ.
4. **Quyền theo tệp, không theo màn** (§3.4) — lệch BR25.
5. **`FileDto` là record dùng chung** — thêm trường phải cập nhật mọi nơi khởi tạo (đã kiểm: chỉ 2
   chỗ trong `FileStorageServiceImpl`), nhưng `common/notice` đọc nó ⇒ chạy lại test notice.
6. **`str_file` giờ mang dữ liệu nghiệp vụ** — javadoc "must NOT depend on any business module" phải
   sửa cho khớp sự thật, nếu không người sau đọc sẽ tưởng ba cột mới là nhầm lẫn.
7. **Tika ≠ phần mở rộng**: `.csv` bị nhận `text/plain` ⇒ `object_key` thành `.txt`. Vô hại (tên hiển
   thị lấy từ `ten_hien_thi`) nhưng phải ghi javadoc.

---

## 8. Câu hỏi cần chốt

- **Q1 — Một group cho mỗi nghiệp vụ, hay một group `dinh-kem` dùng chung + cột `doi_tuong_loai`?**
  Plan này theo vế đầu (đúng chữ "type riêng cho từng nghiệp vụ"): mỗi màn một `FileGroup`, giới hạn
  BR02 khai riêng từng group. Vế sau ít hằng số enum hơn nhưng mất khả năng đặt giới hạn riêng.
- **Q2 — `nguoiTaoTen`:** cho `common/storage` phụ thuộc `platform_iam.nguoi_dung.api` để có cột
  "Người tải lên" của Figma, hay bỏ cột đó?
- **Q3 — BR03 & BR25 ở tầng API:** chấp nhận chỉ chặn ở FE (hệ quả 3 · §3.4), hay sau này bổ sung một
  `ChuSoHuuPort` để storage hỏi ngược module nghiệp vụ (đúng thứ vừa quyết định bỏ)?
- **Q4 — Gắn tệp:** gọi `gan-doi-tuong` **sau khi Lưu** (plan này), hay để thân request chứng từ mang
  `dinhKem` rồi `ChungTuTemplate` gọi trong cùng transaction (an toàn hơn, nhưng lại đụng kernel)?
- **Q5 — MinIO local** có chạy được để nghiệm thu P6 không (`pmkt.minio.*`)?

---

## 9. Đánh đổi của lời giải này

Không có module nghiệp vụ, không bảng nối, không đụng `ChungTuTemplate` (21 lớp con) — đổi lại **hai
thứ mất đi**, đã nêu ở §1.1 và §7:

1. **BR03 · BR25 không chốt chặn được ở tầng API** — chỉ FE ẩn nút. Gọi thẳng API vẫn xoá được tệp
   của chứng từ đã ghi sổ, và quyền là theo tệp chứ không theo màn.
2. **Bước gắn tệp không cùng transaction với lưu chứng từ** — lưu xong mà `gan-doi-tuong` hỏng thì
   chứng từ có nhưng tệp chưa gắn. Job §5 dọn phần rác sau 24h.

Cả hai chấp nhận được với phạm vi hiện tại; nếu sau này nghiệp vụ đòi chốt chặn thật ở server thì
phải mở lại **Q3**.

---

## Phụ lục A — khảo sát: mọi thứ đang dùng `str_file` (kiểm chứng trên nhánh hiện tại)

### A.1 Bảng `str_file` (V1 · gốc V331)

```
id · tenant_id · file_group · object_key · original_name · content_type · size
content_hash · status(UPLOADING|READY|FAILED) · branch_id
+ bộ hệ thống BR46: phien_ban · ngay_tao · nguoi_tao · ngay_cap_nhat · nguoi_cap_nhat
                    da_xoa · ngay_xoa · nguoi_xoa
RLS ENABLE + FORCE · CHECK size >= 0 · CHECK status
```

**Không có cột chủ sở hữu** — đó chính là mảnh §2.1 bù vào.

### A.2 REST công khai — `/api/storage/files` (`FileStorageController`)

| Method | Path | Quyền | Trả về |
|---|---|---|---|
| `POST` | `/api/storage/files` | `File.Create` | `ApiResponse<FileDto>` · 201 · multipart `group`+`file` |
| `POST` | `/api/storage/files/upload-multiple` | `File.Create` | `ApiResponse<List<UploadResult>>` · **luôn 200**, mỗi tệp một kết quả |
| `GET` | `/api/storage/files` | `File.View` | `PageResponse<FileDto>` lọc `group`/`search`, ép `status = READY` |
| `GET` | `/api/storage/files/{id}` | `File.View.Detail` | `FileDto` **có** `downloadUrl` presigned |
| `POST` | `/api/storage/files/find-by-ids` | `File.View.Detail` | `List<FileDto>` (batch, `downloadUrl` = null) |
| `GET` | `/api/storage/files/{id}/content` | `File.View.Detail` | streaming, **HTTP Range**, `Content-Disposition` |
| `DELETE` | `/api/storage/files/{id}` | `File.Delete` | xoá **mềm** bản ghi, **GIỮ** object trên MinIO |

### A.3 REST nội bộ — `/internal/storage/files`

`GET /{id}` · `POST /find-by-ids` · `GET /{id}/content` — service-to-service, `tenantId` tường minh.
**Không dùng cho FE.**

### A.4 Cổng in-JVM — `FileStorageApi` (`@NamedInterface`)

`findById` · `findByIds` · `findByObjectKeys` · `openContent` · `readAllBytes`.

### A.5 Hai consumer đang chạy

| Consumer | Cách nối tới `str_file` | Trạng thái |
|---|---|---|
| **Ngân quỹ** (`tien_mat_tien_gui`) | bảng riêng `cash_phieu_thu_chi_tep_dinh_kem` (V1013) giữ `phieu_id` + `file_id` (XFK mềm); đọc metadata bằng **native query theo TÊN BẢNG** (`TraCuuDanhMucThuChiRepository`): `SELECT id, original_name, size, content_type, status FROM str_file WHERE id IN (:ids)` | Đọc: `GET {base}/{id}/tep-dinh-kem`. **Ghi: `CHUA_HO_TRO`** |
| **Notice** (`common/notice`) | `FileStorageApi.findByIds` / `findByObjectKeys` in-JVM; hợp đồng trên dây đi theo **`object_key`** (quyết định riêng của module, V353) | đang chạy |

Bảng của ngân quỹ là bảng nối chứng từ ⇄ tệp **duy nhất** từng tồn tại, và luồng ghi của nó chưa từng
được cài. P8 (§6) backfill nó sang `str_file.doi_tuong_id` rồi drop.

### A.6 Chi tiết cài đặt đáng nhớ khi sửa

| Nơi | Điều đáng nhớ |
|---|---|
| `FileStorageTxOps.search` | dựng bằng **Specification** (cố ý — javadoc giải thích vì sao không dùng JPQL `:param IS NULL`: PostgreSQL suy `bytea` rồi nổ `lower(bytea)`). Thêm filter = thêm predicate, 6 dòng |
| `StoredFile` entity | `group` · `objectKey` · `originalName` · `contentType` · `size` · `contentHash` đều `updatable = false` — đó là lý do phải có cột `ten_hien_thi` riêng |
| `FileStorageServiceImpl.buildObjectKey` | phần mở rộng suy từ `contentType`, **không** từ tên tệp người dùng (chặn path traversal) |
| `delete` | xoá mềm bản ghi, **cố ý giữ** object trên MinIO |
| `FileDto` | record — thêm trường phải sửa mọi nơi khởi tạo (chỉ 2 chỗ: `toDto`, `withDownloadUrl`) |
