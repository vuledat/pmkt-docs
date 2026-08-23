> ⚠ **CẬP NHẬT 2026-08-22 — đọc trước.** Phần **§4 Thiết kế Backend** của kế hoạch này (module
> `cell/dinh_kem_chung_tu` + bảng nối `att_chung_tu_dinh_kem`) **ĐÃ BỊ BỎ** theo quyết định của user
> và đã được xoá khỏi file. Thiết kế BE đang hiệu lực nằm ở
> [`02-plan-tich-hop-qua-storage-api.md`](02-plan-tich-hop-qua-storage-api.md).
> Phần **§5 Thiết kế Frontend** trở đi vẫn còn giá trị tham khảo, nhưng hiện trạng FE thật đã đi
> trước — xem [`IMPLEMENT.md`](IMPLEMENT.md).

# Kế hoạch: Common "Tệp đính kèm chứng từ" (tab Đính kèm dùng chung cho mọi màn chứng từ)

> Trạng thái: **BẢN KẾ HOẠCH — CHƯA CODE**. Cần chốt Q1–Q8 (§8) trước khi vào pha 1.
> Ngày lập: 2026-08-22. Anh em với [`tham-chieu-chung-tu-common`](../tham-chieu-chung-tu-common/00-ke-hoach-tong.md)
> — hai thành phần dùng chung cùng nằm trong `pmkt-docs/ba/Common/NguonDuLieu/`, cùng khuôn triển khai.

## 1. Mục tiêu

Một cơ chế **dùng chung duy nhất** cho tab "Đính kèm" của mọi màn chứng từ (danh sách · thêm mới ·
chỉnh sửa · xem chi tiết · panel xem nhanh): tải tệp lên, gắn vào chứng từ, xem, tải xuống, xóa mềm —
theo đúng màn dùng chung
[`SCR_FileDinhKem.md`](../../../pmkt-docs/ba/Common/NguonDuLieu/SCR_FileDinhKem.md).

Kết quả mong muốn: màn chứng từ mới **khai báo 1 lần** là có đủ tab Đính kèm (kéo–thả + tiến trình %
+ danh sách tệp + xem/tải/xóa + validation BR02 + chặn theo trạng thái ghi sổ), không viết lại UI,
không tạo bảng riêng, không tự nghĩ hợp đồng API.

## 2. Tài liệu đã đọc (cơ sở của kế hoạch)

| Tài liệu | Nội dung dùng |
|---|---|
| `Common/NguonDuLieu/SCR_FileDinhKem.md` | Toàn bộ đặc tả: 2 cột (Tên tệp · Dung lượng), 3 chức năng (Chọn tệp · Tải xuống · Xóa), **BR01–BR04** của màn, bảng Validation, 4 thông báo |
| `Common/business_rules.md` — **BR29.1** | Chỉ xóa mềm (`DaXoa`/`NgayXoa`), không xóa vật lý |
| **BR16.1** | `MSG_COMMON_001` — chặn thao tác không hợp lệ với trạng thái chứng từ (dùng cho "đã ghi sổ ⇒ không xóa tệp") |
| **BR46** | Bộ trường hệ thống bắt buộc trên MỌI entity + `TenantId`/`ChiNhanhId` (46.4) |
| **BR03 · BR14 · BR13.2** | Popup, chế độ form (Thêm/Sửa/Xem), nút trên form |
| **BR25 · BR28** | Phân quyền theo màn chủ · multi-tenant (RLS) |
| **BR44 · BR26 · BR12/BR33** | Truncate tên tệp dài · toast/notification · trạng thái chứng từ |
| `SCR_CTBH_DanhSach.md:201` | "Đính kèm — Luôn hiển thị, nội dung theo SCR_FileDinhKem" (panel xem nhanh cũng có tab này) |
| `UC_CTBH_ThemMoi.md:60` | Đính kèm là 1 trong 7 tab của popup Thêm mới |
| ⚠ `SCR_GhiTangTSCD_ThemMoi.md` | "**Chứng từ đính kèm**" là thứ KHÁC — tham chiếu chứng từ khác trong hệ thống, thuộc plan `tham-chieu-chung-tu-common`, **không** thuộc plan này |

## 3. Hiện trạng — vì sao phải làm common

### 3.1 Hạ tầng lưu trữ **đã có và tốt** — thiếu đúng một mắt xích

Module `cell/common/storage` (`vn.vtt.pmkt.cell.common.storage`) đã hoàn chỉnh:

| Đã có | Chi tiết |
|---|---|
| Bảng `str_file` | metadata tệp, RLS FORCE, xóa mềm, `content_hash` SHA-256, `status` UPLOADING/READY/FAILED |
| Object store | MinIO, object key `<tenantId>/<group>/<yyyy>/<mm>/<dd>/<HHmmssSSS>/<sha256>.<ext>` |
| Upload | `POST /api/storage/files` (1 tệp) · `POST /api/storage/files/upload-multiple` (nhiều tệp, mỗi tệp một `UploadResult`) |
| Đọc nội dung | `GET /api/storage/files/{id}/content` (streaming + HTTP Range) · presigned URL |
| Xóa | `DELETE /api/storage/files/{id}` — xóa mềm bản ghi, GIỮ object trên MinIO |
| Chống giả mạo | content type suy từ **magic bytes** (Apache Tika), KHÔNG tin header client khai |
| Cấu hình ngoài code | `pmkt.storage.groups.<group>.{max-size, content-types}` — đổi không cần build lại |
| Cổng Java in-JVM | `FileStorageApi` (`findById` · `findByIds` · `openContent` · `readAllBytes`) |

**Mắt xích thiếu: không có gì nối chứng từ ⇄ tệp.** `str_file` cố ý không có cột chủ sở hữu
(`package-info.java` ghi rõ: "must NOT depend on any business module"). Đúng **một** bảng nối tồn tại
trong toàn hệ thống — `cash_phieu_thu_chi_tep_dinh_kem` (V1013), và chính COMMENT của nó tự khai là
"bảng nối chứng từ ⇄ file **ĐẦU TIÊN** của hệ thống".

### 3.2 Backend: 1 bảng riêng lẻ, luồng ghi chưa thông

| Cụm | Bảng nối | Đọc | Ghi |
|---|---|---|---|
| Ngân quỹ (thu/chi TM + TG) | `cash_phieu_thu_chi_tep_dinh_kem` | `GET {base}/{id}/tep-dinh-kem` → `TepDinhKemDto` | ❌ **`CHUA_HO_TRO`** |
| Bán hàng, Mua hàng, Kho, CCDC, TSCĐ, CPTT, KTTH | **không có** | — | — |

Nghĩa là: hôm nay **chưa màn nào lưu được tệp đính kèm vào chứng từ**. Ngân quỹ đọc được vì bảng có
sẵn, nhưng không có đường ghi. Đây là điểm khác quan trọng so với plan Tham chiếu (7 bảng lệch nhau
phải hợp nhất): ở đây **gần như greenfield**, chỉ 1 bảng cũ phải xử lý.

### 3.3 Frontend: 4 bản `DinhKemTab.tsx`, 3 trong đó là **UI giả**

| Màn | File | Thực chất |
|---|---|---|
| `nganQuy/_shared` | `DinhKemTab.tsx` | `StorageUploadButton` — upload THẬT lên storage, nhưng `onUploaded` **không nối đi đâu** ⇒ tệp mồ côi |
| `nganQuy/_shared` | `DinhKemPanelTab.tsx` | `CommonListTable` + `useStoragePreview` — bản **chỉ đọc** đầy đủ nhất repo, đúng hướng |
| `congCuDungCu/dieuChuyen` | `DinhKemTab.tsx` | `StorageUploadButton`, cùng vấn đề mồ côi |
| `banHang/chungTuBanHang` | `DinhKemTab.tsx` | chỉ `CommonEmpty` — **rỗng, không upload** |
| `kho/_shared` | `DinhKemTab.tsx` | `CommonEmpty` + nút Thêm **`disabled`** — rỗng có chủ đích |
| CPTT, TSCĐ, Mua hàng, KTTH… | `TabChuaCoDuLieu` / khóa i18n suông | chưa có gì |

`@base/domainKit/storage` (TIER 2) đã có `useStorageUpload` · `useStoragePreview` ·
`StorageUploadButton` — nhưng đó là **nút upload chung chung**, KHÔNG phải "tab Đính kèm của chứng
từ": không có kéo–thả theo BR04, không có bảng 2 cột theo SCR, không biết chứng từ nào, không biết
trạng thái ghi sổ, không validate theo BR02 (5MB + 14 phần mở rộng).

### 3.4 Lệch giữa cấu hình hiện tại và BR02 — phải sửa BE

| BR02 yêu cầu | Hệ thống hiện tại | Việc phải làm |
|---|---|---|
| Tối đa **5 MB/tệp** | group `document` = **10 MB** | thêm group riêng, `max-size: 5MB` |
| 14 phần mở rộng: `.doc .docx .xls .xlsx .pdf` · `.jpg .jpeg .png .gif .bmp` · `.zip .rar .7z` · `.xml .txt .csv` | group `document` chỉ nhận 5 MIME: pdf, png, jpeg, xlsx, docx | mở rộng whitelist |
| — | `FileGroup.Mime.EXTENSION_BY_MIME` là `Map.of(...)` **8 cặp** và `extensionFor()` **NÉM** khi không map được | phải bổ sung ~9 cặp ⇒ `Map.of` (trần 10 cặp) đổi sang `Map.ofEntries`; **thiếu bước này thì upload .zip/.txt/.gif sẽ 500** |

## 4. Thiết kế Backend — ⛔ **ĐÃ BỎ, KHÔNG DÙNG**

Toàn bộ thiết kế BE cũ ở mục này (module Spring Modulith `cell/dinh_kem_chung_tu`, bảng nối
`att_chung_tu_dinh_kem` + migration `V1036`, `DinhKemChungTuApi`, SPI `ChuSoHuuDinhKemPort`,
controller `/api/chung-tu/dinh-kem`, móc `dongBoDinhKem` vào `ChungTuTemplate`) **đã bị gỡ khỏi kế
hoạch theo quyết định của user ngày 2026-08-22**: không code module riêng, không bảng nối — dùng
thẳng bộ API công khai `/api/storage/files` có sẵn, truyền **type riêng cho từng nghiệp vụ**
(`FileGroup`) và thêm 3 cột chủ sở hữu vào chính `str_file`.

👉 Thiết kế BE đang hiệu lực: **[`02-plan-tich-hop-qua-storage-api.md`](02-plan-tich-hop-qua-storage-api.md)**
(kèm khảo sát hiện trạng ở Phụ lục A và thay đổi FE chi tiết ở §4).

Nội dung cũ đã được xoá khỏi file này để không ai cài nhầm.


## 5. Thiết kế Frontend

### 5.1 Vị trí: `@domain-kit/dinhKem` (TIER 2)

Không đặt ở `@base` (base phải business-agnostic, mà tab này biết loại chứng từ, trạng thái ghi sổ,
BR01–BR04), không đặt ở `features/*/_shared` (phải dùng chung xuyên domain). Đúng chỗ là
`src/base/domainKit/dinhKem/`, cạnh `storage` (hạ tầng upload nó sẽ dùng lại) và `chungTu` (engine).

```
src/base/domainKit/dinhKem/
├── index.ts                        barrel (side-effect: đăng ký i18n namespace 'dinhKem')
├── api/        dinhKemApi.ts · dinhKemSchema.ts (Zod)
├── components/ DinhKemTab.tsx · DinhKemPanelTab.tsx · VungKeoTha.tsx · DongTep.tsx
├── constants/  constants.ts (DINH_KEM_NAME, group 'dinh-kem', 5MB, 14 đuôi, NHOM_1/NHOM_2)
├── fields/     cotDinhKem.ts (2 cột SCR) · types.ts
├── helpers/    kiemTraTep.ts (BR02) · datTenKhongTrung.ts (BR02) · doDungLuong.ts (KB/MB, 1 chữ số)
├── hooks/      useDinhKem.ts (state tệp + upload + xóa) · useXemTep.ts (BR01)
├── i18n/       vi.ts · en.ts · registerDinhKemI18n.ts
└── test/
```

### 5.2 Hợp đồng component

```tsx
<DinhKemTab
  loai="CHUNG_TU_BAN_HANG"       // enum khớp BE
  doiTuongId={id}                 // undefined khi Thêm mới ⇒ tab chạy thuần trên Form
  name={DINH_KEM_NAME}            // khóa trong Form của màn — lưu cùng payload chứng từ (§4.6)
  cheDo="SUA" | "XEM" | "PANEL"   // XEM: ẩn Chọn tệp + Xóa (BR02/BR03); PANEL: chỉ đọc, tự gọi GET
  daGhiSo={boolean}               // BR03 — ẩn nút Xóa
  t={t} locale={locale}
/>
```

`DinhKemPanelTab` **nâng thẳng từ** `features/nganQuy/_shared/components/DinhKemPanelTab.tsx` — bản
đó đã đúng khuôn (`CommonListTable` + `useStoragePreview` + `fillHeight` cho panel 280px + BR44
truncate + hàm `coKichThuoc` bậc 1024). Chỉ đổi nguồn API và bỏ phụ thuộc namespace `nganQuy`.

### 5.3 Ánh xạ SCR → hành vi (không được bịa thêm)

| SCR | Cài đặt |
|---|---|
| **BR04** trạng thái rỗng | chưa có tệp: *"Chưa có tệp đính kèm — kéo thả tệp vào đây"*; có tệp: danh sách + *"Kéo thả tệp vào đây để đính kèm"*. Thả ở **bất kỳ vị trí nào** trong khối đều nhận ⇒ vùng drop bọc cả khối, không chỉ ô trống |
| **BR02** tải lên | `Chọn tệp` (multiple) **hoặc** kéo–thả; kiểm **từng tệp độc lập**; tệp vi phạm **không** vào danh sách, chỉ hiện lỗi kèm tên tệp; tệp đang tải hiện **% tiến trình** ở cột Dung lượng và **chưa** xem/tải/xóa được |
| **BR02** tên trùng | `datTenKhongTrung()` — trùng trong **cùng chứng từ** thì thêm hậu tố ` (1)`, ` (2)`… trước phần mở rộng. Kết quả ghi vào `ten_hien_thi` (§4.2.1 #7) |
| **BR01** bấm tên tệp | **Nhóm 1** (`.doc .docx .xls .xlsx .pdf`) → mở trình xem trong hệ thống; **Nhóm 2** (còn lại, gồm ảnh) → tải về máy. Nút `Tải xuống` trên dòng **chỉ có ở Nhóm 1** |
| **BR03** xóa | chỉ Thêm/Sửa + có quyền sửa; đã ghi sổ ⇒ **ẩn**; có confirm; xóa mềm |
| **BR44** | tên tệp dài ⇒ clamp + tooltip |
| **BR26** | 4 thông báo ở §4.8 qua toast/notification chuẩn |

### 5.4 ⚠ Lỗ hổng BR01 chưa có lời giải — xem trực tiếp `.doc/.docx/.xls/.xlsx`

`useStoragePreview` hiện chỉ render được **ảnh** (`<img>`) và **PDF** (`<iframe>`) — đúng những gì
trình duyệt tự hiểu. BR01 đòi **toàn bộ Nhóm 1** phải xem trực tiếp được, và chính SCR đã ghi *"cần hệ
thống xử lý thêm phía server"*.

Ba đường, không đường nào miễn phí:

| Cách | Ưu | Nhược |
|---|---|---|
| **A. Chuyển đổi phía server** (LibreOffice headless / Gotenberg → PDF, cache lại vào `str_file`) | đúng BR01 100% | Gotenberg là **container** ⇒ **vi phạm luật cấm Docker** của repo; LibreOffice headless phải cài lên máy chủ, +~400MB, tiến trình nặng |
| **B. Nhúng viewer JS phía client** (SheetJS đọc `.xlsx`, `docx-preview` đọc `.docx`) | không cần server | **không đọc được `.doc`/`.xls`** (định dạng nhị phân cũ), độ trung thực thấp, +bundle |
| **C. Nhóm 1 = chỉ `.pdf`; Office → tải về** | làm được ngay, 0 rủi ro | **lệch BR01** — phải BA duyệt |

Đề xuất: **P4 làm theo C**, ghi rõ là lệch BR01; mở ticket riêng cho A/B sau khi BA chốt (Q3).

### 5.5 Dọn 4 bản `DinhKemTab` trùng

Sau khi common chạy: xóa `banHang/chungTuBanHang/components/DinhKemTab.tsx` (rỗng),
`kho/_shared/components/DinhKemTab.tsx` (rỗng + nút disabled), `congCuDungCu/dieuChuyen/components/DinhKemTab.tsx`
và `nganQuy/_shared/components/DinhKemTab.tsx` (upload mồ côi) — bốn file thay bằng một lời gọi
`<DinhKemTab …/>`. Riêng `nganQuy/_shared/components/DinhKemPanelTab.tsx` được **nâng lên**, không xóa
trắng (xem §5.2), và test `DinhKemPanelTab.test.tsx` di chuyển theo.

## 6–8. Phân pha · Rủi ro · Câu hỏi — ⛔ **ĐÃ THAY THẾ**

Ba mục cũ (phân pha P0–P7, rủi ro, câu hỏi Q1–Q8) đều dựng quanh thiết kế BE đã bỏ ở §4, nên đã được
xoá khỏi file này. Bản đang hiệu lực:

- **Phân pha + cổng nghiệm thu (P0–P8):** [`02-plan-tich-hop-qua-storage-api.md` §6](02-plan-tich-hop-qua-storage-api.md)
- **Rủi ro:** cùng file, §7
- **Câu hỏi cần chốt (Q1–Q5):** cùng file, §8
- **Hiện trạng FE đã code + nợ kỹ thuật thật:** [`IMPLEMENT.md`](IMPLEMENT.md)

Hai thứ của bản cũ vẫn còn nguyên giá trị và đã được chuyển sang bản mới: **lỗ hổng BR01 với
`.doc/.docx/.xls/.xlsx`** (§5.4 bên trên — FE đang đi theo phương án C, chờ BA chốt) và **`FileGroup`
phải sửa `EXTENSION_BY_MIME` kẻo upload `.zip/.txt/.gif` trả 500**.


## 9. BR sẽ áp dụng

**BR01–BR04 của `SCR_FileDinhKem`** (trọng tâm — tải lên · xem · xóa · trạng thái rỗng) · BR03 popup ·
BR12/BR33 trạng thái chứng từ · BR13.2 nút trên form · BR14 chế độ form · BR15 validation ·
BR16.1 `MSG_COMMON_001` · BR19 kiểm trùng · BR25 phân quyền · BR26 toast · BR28 multi-tenant ·
BR29.1 xóa mềm · BR29.2 xóa lan · BR34 sửa từ màn xem · BR43 trim · BR44 truncate · BR46 trường hệ thống.
