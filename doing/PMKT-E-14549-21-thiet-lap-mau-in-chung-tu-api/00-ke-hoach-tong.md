# PMKT-E-14549_21 Thiết lập mẫu in chứng từ — Kế hoạch triển khai API (BE)

| | |
|---|---|
| Trạng thái | **BẢN NHÁP CHỜ REVIEW** — chưa code dòng nào |
| Ngày lập | 2026-09-19 |
| Người lập | AI (`/plan-be`) |
| Người review | Dev BE ☐ · BA ☐ |
| Phiếu yêu cầu | `PMKT-E-14549_21_ThietLapMauInChungTu` (tài liệu gốc nằm trong vùng đóng băng `pmkt-docs/ba/Phase_2/**` — **kế hoạch này KHÔNG mở lại**, chỉ dùng spec đã biên dịch) |
| Đặc tả nguồn | `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/` — `00-source-map.md` · `01-conflict.md` · `02-rules.md` (271 luật + 12 bất biến) · `03-scenarios.md` · **`04-quyet-dinh-ban-giao.md`** |
| Use case | `PMKT-U-14549_21-01` Thiết lập mẫu in · `PMKT-U-14549_21-02` In chứng từ bằng mẫu tùy chỉnh |
| Module BE | `cell-app` › `cell/mau_in/` (Spring Modulith, tiền tố bảng `prn_`) |
| Bảng DB chạm | `prn_mau_in_tuy_chinh` (sửa) · `prn_mau_in_lich_su` (sửa) · `iam_tenant` (thêm cột logo) · `cfg_cau_hinh_he_thong` (dùng lại, không đổi cấu trúc) |
| Migration mới | `V1158` · `V1159` · `V1160` — xem [08-thiet-ke-db.md](08-thiet-ke-db.md) |
| Cổng đặc tả | `01-conflict.md` — **36 mục · 0 `OPEN`** (32 `CLOSED-BA` Dat · 2026-09-19 + 4 `CLOSED-AUTO`) ⇒ **cổng MỞ, được code toàn bộ** |

> **Thứ tự ưu tiên tài liệu khi mâu thuẫn:** `04-quyet-dinh-ban-giao.md` > `01-conflict.md` > `02-rules.md` > `03-scenarios.md` > code hiện có.

---

## Mục lục file con

| File | Nội dung |
|---|---|
| [01-hop-dong-json-mau-in.md](01-hop-dong-json-mau-in.md) | **JSON schema đầy đủ của mẫu in** — hợp đồng kỹ thuật thay cho ERD (quyết định C09) |
| [02-hop-dong-json-thiet-lap-chung.md](02-hop-dong-json-thiet-lap-chung.md) | JSON schema của **thiết lập chung tối thiểu** + `HoSoDonViPort` (Q-03, Q-14) |
| [03-api-thiet-lap-mau-in.md](03-api-thiet-lap-mau-in.md) | `F01` — mở màn & lưu mẫu (UC01) |
| [04-api-anh-nen-va-logo.md](04-api-anh-nen-va-logo.md) | `F02` — tải ảnh nền của mẫu và logo đơn vị (`multipart`) |
| [05-api-in-mau-tuy-chinh.md](05-api-in-mau-tuy-chinh.md) | `F03` — dựng bản in & menu In (UC02) |
| [06-provider-nghiep-vu-va-kho-truong.md](06-provider-nghiep-vu-va-kho-truong.md) | `F04` — cơ chế provider theo nghiệp vụ, mẫu chuẩn hệ thống, kho trường |
| [07-chuan-hoa-kiem-tra-va-thuat-toan.md](07-chuan-hoa-kiem-tra-va-thuat-toan.md) | `F05` — chuẩn hoá · 17 dòng kiểm tra · chia đều 100% · hướng Tự động · cộng gộp dòng |
| [08-thiet-ke-db.md](08-thiet-ke-db.md) | Thiết kế DB + SQL đầy đủ của `V1158`…`V1160` |
| [09-tai-dung-va-bo-code-cu.md](09-tai-dung-va-bo-code-cu.md) | **Bảng tái dùng / bỏ cho từng file trong 29 file chưa commit** |
| [10-truy-vet-luat-va-test.md](10-truy-vet-luat-va-test.md) | Bảng truy vết `R-TLMI-… → file → test` cho **mọi luật tầng BE** + danh sách unit test |

---

## §0. Quyết định đã chốt `D1…D14`

Mỗi quyết định ghi **hệ quả lên code** và **vì sao không chọn phương án kia**.

### D1 · Một bản ghi, một cột `jsonb` — không dựng 5 bảng quan hệ

Nguồn: `04-quyet-dinh-ban-giao.md` §1 Q-01 `[USER]`.

- Giữ **`prn_mau_in_tuy_chinh`** (đã tồn tại, `V1148`) với cột `cau_hinh jsonb`.
- 5 "entity" của `3.crud-matrix.md` (`cfg_mau_in_chung_tu` · `_khoi` · `_khoi_cot` · `_khoi_o` · `_khoi_chu_ky`) trở thành **5 nhánh trong JSON schema** — xem [01-hop-dong-json-mau-in.md](01-hop-dong-json-mau-in.md).
- Hệ quả code: **không** có `@Entity` cho khối/cột/ô/chữ ký; chỉ 1 entity `MauInTuyChinh` + 1 entity `MauInLichSu`. Mọi biến đổi mẫu là biến đổi **record Java bất biến** rồi ghi lại cả cụm (`R-TLMI-247` "xóa hết bản cũ, ghi bản mới" thỏa mãn tự nhiên vì ghi đè một cột).
- **Vì sao không chọn 5 bảng quan hệ:** `01-conflict.md` C09 ghi rõ tài liệu BA **không có file entity/ERD** cho 5 bảng đó — cấu trúc cột phải tự bịa, đúng thứ `CLAUDE.md` luật 9 cấm. Ngoài ra `R-TLMI-247` bắt "xóa hết bản cũ ghi bản mới" trong một transaction: với 5 bảng là 5 `DELETE` + 5 `INSERT` hàng loạt mỗi lần Lưu, còn với một cột `jsonb` là một `UPDATE`.
- **Giá phải trả (ghi nhận):** không truy vấn được "mẫu nào đang dùng trường X" bằng SQL thường — phải dùng toán tử `jsonb`. Chưa có yêu cầu nào như vậy trong 271 luật.

### D2 · Khoá nghiệp vụ = `(tenant_id, ma_loai_chung_tu, ma_nghiep_vu)` — migration MỚI

- `R-TLMI-004` bắt khoá duy nhất theo **cặp** *(loại chứng từ, nghiệp vụ)*; bảng hiện có chỉ khoá `(tenant_id, ma_loai_chung_tu)` — `V1148__prn_mau_in_tuy_chinh.sql:40-42`.
- `V1148` `V1149` `V1150` **đã nằm trên `origin/develop` và `origin/staging`** (commit `018d444f`; xác nhận lại 2026-09-19: nhánh `feat/mau-in` đã fast-forward lên `origin/develop` `37303112`). ⇒ **cấm sửa tại chỗ**, mọi thay đổi đi bằng migration mới, đánh số từ **`V1158`** (cập nhật 2026-09-21: develop đã lên `86cada67`, số lớn nhất là `V1157__cst_phan_bo_chi_phi_them_co_da_luu_thiet_lap.sql`; bản kế hoạch gốc 2026-09-19 ghi `V1155` khi develop còn ở `V1154`).
- **Vì sao không sửa `V1148`:** Flyway đã ghi checksum của `V1148` trên develop/staging; sửa tại chỗ ⇒ `Migration checksum mismatch` và môi trường chết ngay lần deploy sau.
- Q-16: **mọi API nhận đủ cặp** `(maLoaiChungTu, maNghiepVu)`, kể cả loại chứng từ chỉ có một nghiệp vụ — khi đó `maNghiepVu = MaNghiepVuMauIn.MAC_DINH` (`"MAC_DINH"`), đúng `R-TLMI-003`.

### D3 · BE giải nghĩa, FE dựng trang — ranh giới rõ ràng

BE trả **"mẫu đã hợp nhất"** (trong code gọi là *mẫu hiệu lực*): mọi khoá vắng đã điền từ thiết lập chung, hướng giấy `TU_DONG` đã giải thành `DOC`/`NGANG`, dòng đã cộng gộp, hồ sơ đơn vị đã tra theo chi nhánh, giá trị từng trường đã điền. FE **chỉ** đo chữ, ngắt trang, vẽ.

| Loại luật | Chủ | Ví dụ |
|---|---|---|
| Quyết định **NỘI DUNG** bản in | **BE** | `R-TLMI-038` · `058` · `059` · `079` · `119` · `262` · `264` · `266` · `267` |
| Quyết định **PIXEL / NGẮT TRANG** | **FE** (BE cấp đủ dữ liệu) | `R-TLMI-180` · `181` · `194` · `195` · `200` · `263` · `265` |

- **Vì sao không dựng PDF ở BE:** repo **không có Jasper** cho mẫu theo khối — ranh giới này đã ghi sẵn trong `cell/mau_in/package-info.java`. Viết bộ dựng trang thứ hai ở BE để phủ `R-TLMI-180…200` nghĩa là hai engine phải ra **cùng một pixel**; chi phí không tương xứng ở giai đoạn này. Xuất PDF phía máy chủ là việc của một phiếu sau.
- **Ghi nhận rủi ro:** `02-rules.md` gán 7 luật trên tầng `BE`. Kế hoạch này **cố ý lệch** và đánh dấu chúng là `BE-CẤP-DỮ-LIỆU` trong [10-truy-vet-luat-va-test.md](10-truy-vet-luat-va-test.md) — xem **§12 Q3**.

### D4 · Ô "theo thiết lập chung" = **KHOÁ VẮNG MẶT trong JSON**

- `R-TLMI-037`: ô theo chung ghi **trống**, tuyệt đối không copy giá trị đang hiển thị. `INV-TLMI-003`.
- `R-TLMI-038`: đọc lại thiết lập chung **tại lúc in / lúc vẽ xem trước** — không đóng băng giá trị.
- Hệ quả code:
  - Mọi record JSON của nhóm kế thừa dùng **kiểu boxed** (`Integer`, `Double`, `Boolean`, `String`) và `@JsonInclude(NON_NULL)`.
  - **Cấm** đặt `default` cho nhóm khoá này ở BE và ở Zod của FE.
  - Hợp nhất là một hàm riêng `HopNhatThietLapChung.hopNhat(mauJson, thietLapChung)` — **chỉ gọi lúc ĐỌC**, không bao giờ gọi trước khi ghi.
  - `ChuanHoaMau` phải **xoá** mọi khoá `null` trước khi so sánh và trước khi ghi.
- **Vì sao không dùng sentinel (`kho = "THEO_CHUNG"`):** sentinel làm kiểu dữ liệu của ô nở ra một giá trị giả, và mọi nơi đọc phải nhớ lọc nó; quên một chỗ là in ra chữ `THEO_CHUNG`. Khoá vắng mặt thì `null` tự lan truyền và `COALESCE` là phép hợp nhất duy nhất.
- **Vì sao không lưu thêm cờ `laRieng` song song với giá trị:** hai nguồn sự thật cho một ô ⇒ lệch nhau là chuyện sớm muộn, và `R-TLMI-037` nói thẳng là **không ghi giá trị đang hiển thị**.

### D5 · Lưu = chuẩn hoá → so với mẫu chuẩn → bằng thì **XOÁ bản ghi**

Quyết định C02 phương án (A) *so sánh nội dung*.

Thứ tự bắt buộc trong `MauInService.luu(...)`:

1. Đọc JSON thô → `MauInJsonCodec` (mapper **chặt**, thuộc tính lạ ⇒ lỗi).
2. `KiemTraMau` — 17 dòng của `R-TLMI-239`, **cả ở server** (`R-TLMI-246`). Có lỗi ⇒ trả **lỗi đầu tiên** theo thứ tự `R-TLMI-243` + C21, không ghi gì.
3. `ChuanHoaMau` — chia lại độ rộng về 100 (`R-TLMI-111`), sắp khoá cố định, bỏ khoá `null`, bỏ id kỹ thuật, bỏ cờ `moi`, bỏ ô `TRONG` không có định dạng.
4. `MauChuanBuilder.dung(catalog)` → mẫu chuẩn hệ thống, **cũng chạy qua `ChuanHoaMau`**.
5. So sánh **hai chuỗi JSON đã chuẩn hoá**. Bằng nhau ⇒ `DELETE` bản ghi (nếu có), **không tạo mới**; trả `nguon = MAU_CHUAN`.
6. Khác nhau ⇒ `INSERT`/`UPDATE` một bản ghi.
7. Ghi `prn_mau_in_lich_su` (chỉ THÊM) với `hanh_dong ∈ {LUU, XOA}`.

- **Vì sao không chọn phương án (B) "chỉ xoá khi đến từ nút Đặt lại":** cần một cờ phiên sống suốt từ lúc bấm Đặt lại tới lúc Lưu, FE phải mang cờ đó lên, và người dùng Hoàn tác tay về đúng mẫu chuẩn thì vẫn còn bản ghi rác — bất biến `INV-TLMI-002` ("mẫu bằng chuẩn ⇒ không tồn tại bản ghi") **vỡ**. Với JSON, so sánh sâu chỉ là `String.equals` trên hai chuỗi đã chuẩn hoá, rẻ.
- **Bẫy đã biết:** bước 4 phải chạy `ChuanHoaMau` trên mẫu chuẩn; nếu không thì mọi lần Lưu-không-sửa đều đẻ ra một bản ghi vì thứ tự khoá khác nhau.

### D6 · Khoá lạc quan bằng `phienBan` khi Lưu

- Quyết định C06. `prn_mau_in_tuy_chinh.phien_ban` đã có (`V1148__prn_mau_in_tuy_chinh.sql:21`), `LuuMauInRequest` đã mang `phienBan` (`cell/mau_in/internal/dto/LuuMauInRequest.java`).
- Payload `phienBan` **lệch** bản đang có ⇒ **không ghi**, trả `409` + `MSG_COMMON_001`, FE hỏi nạp lại (`R-TLMI-258`).
- `phienBan` của một mẫu **chưa tồn tại** = `null`; client gửi `null` mà bản ghi đã tồn tại ⇒ cũng là xung đột.
- **Vì sao không khoá bi quan:** cần thêm API giữ/nhả khoá và một mã message BA chưa cấp; mẫu in không phải chứng từ, xác suất đụng độ thấp.
- **Nợ BA:** chưa có mã `MSG_` riêng — `04-quyet-dinh-ban-giao.md` §7.1.

### D7 · Ảnh nền và logo là **cột nhị phân**, không phải JSON

Quyết định C08 + Q-03.

| Dữ liệu | Nơi lưu | Endpoint |
|---|---|---|
| Ảnh nền **của một mẫu** | `prn_mau_in_tuy_chinh.anh_nen bytea` + `anh_nen_kieu_tep` + `anh_nen_ten_tep` (`V1159`) | `A5`–`A7` — `multipart` |
| **Logo đơn vị** | `iam_tenant.logo bytea` + `logo_kieu_tep` + `logo_ten_tep` (`V1160`) | `A12` — `multipart` |

- JSON chỉ giữ **cờ** `trang.nen.kieu = "ANH"`; không có `anhId`, không có base64.
- **Vì sao không base64 trong JSON:** ảnh 1 MB thành ~1,37 MB base64, và `cau_hinh` bị đọc **mỗi lần** nạp mẫu kể cả khi chỉ cần bố cục.
- **Vì sao không bảng riêng `prn_anh_mau_in`:** một mẫu tối đa một ảnh, một tenant tối đa một logo ⇒ quan hệ 1-1, bảng riêng chỉ thêm một `JOIN`. Và user đã quyết **không dựng bảng mới**.
- **Vì sao logo lên `iam_tenant` chứ không `cfg_cau_hinh_he_thong`:** cột `gia_tri` của bảng đó là `text` ⇒ lại quay về base64. `iam_tenant` đã là chỗ ở của toàn bộ hồ sơ doanh nghiệp (`V203`, xem `platform_iam/tenant/internal/entity/Tenant.java:40-66`).

### D8 · Thiết lập chung tối thiểu lưu **JSON trên `cfg_cau_hinh_he_thong`** — không bảng mới

Quyết định Q-03 `[USER]`.

- Bảng `cfg_cau_hinh_he_thong` (`V1__create_database.sql:6134-6155`) đã có ràng buộc `kieu_du_lieu` cho phép `'JSON'` (`:6154`) và cột `gia_tri text` (`:6140`), đã bật `FORCE ROW LEVEL SECURITY` (`:6157`).
- Một dòng cho mỗi tenant: `ma_cau_hinh = 'IN_CHUNG_CHUNG_TU'`, `nhom = 'IN'`, `kieu_du_lieu = 'JSON'`, `gia_tri` = JSON ở [02](02-hop-dong-json-thiet-lap-chung.md).
- **Không seed** dòng này trong migration: **thiếu dòng = mọi khoá theo mặc định hệ thống**, đúng nguyên tắc D4. Tránh phải backfill cho mọi tenant.
- **Vì sao không thêm cột `cau_hinh_in jsonb` vào `iam_tenant`:** `iam_tenant` thuộc module `platform_iam`; nhét cấu hình in vào đó là kéo một khái niệm của `mau_in` sang module khác. `cfg_cau_hinh_he_thong` đúng là nơi dành cho cấu hình key-value cấp tenant, và **không cần migration nào**.
- **Vì sao không dựng `cfg_tenant` / `cfg_chi_nhanh` như tài liệu:** `cfg_chi_nhanh` **không tồn tại trong repo** (`grep "cfg_chi_nhanh"` trên `cell-app/src`, `super-admin-service/src`, `tenant-provisioning/src` ⇒ 0 kết quả), BR50 Chi nhánh thuộc Phase 2. User đã quyết không dựng.

### D9 · Một cổng duy nhất cho hồ sơ đơn vị — `HoSoDonViPort` (Q-14)

```java
public interface HoSoDonViPort {
    /** R-TLMI-078 · R-TLMI-267 — hồ sơ của CHI NHÁNH GHI TRÊN CHỨNG TỪ. */
    HoSoDonVi theoChiNhanh(UUID chiNhanhId);
}
```

- Bản hiện tại `HoSoDonViTheoTenant implements HoSoDonViPort` **bỏ qua tham số** và trả hồ sơ tenant (quyết định L-7).
- Mọi nơi cần hồ sơ đơn vị — khối Thông tin đầu trang (`R-TLMI-078`), khối Chữ ký (`R-TLMI-199`), kho trường (`R-TLMI-165`) — **bắt buộc** đi qua cổng này. **Cấm** gọi thẳng `TenantConfigApi` từ tầng dựng bản in.
- Khi `cfg_chi_nhanh` ra đời: viết `HoSoDonViTheoChiNhanh`, đổi bean, **không đụng** tầng trên.
- Ngoại lệ tài liệu: **logo luôn của pháp nhân**, chi nhánh không có logo riêng (`R-TLMI-078` Ghi chú) ⇒ `HoSoDonVi.logo` lấy từ tenant kể cả khi sau này hiện thực theo chi nhánh.

### D10 · Quyền hai tầng, gom vào một hằng số (C13 + Q-15)

| Tầng | Mã | Áp cho |
|---|---|---|
| (a) Màn thiết lập | `HTMauIn.View` / `HTMauIn.Edit` — **đã seed** `V1149`, đang trên develop | mở màn · lưu mẫu · ảnh nền |
| (b) Dữ liệu nghiệp vụ | `<MaChucNang của nghiệp vụ>.View.Detail` | mọi endpoint chạm dữ liệu chứng từ thật |
| (c) In | `<MaChucNang của nghiệp vụ>.<hanhDongIn()>` (provider khai; mặc định `Print`) | dựng bản in · menu In |

- Gom vào `internal/model/MaQuyenMauIn.java` — đổi sang mã theo nghiệp vụ sau này chỉ sửa một file (Q-15).
- **Không tự seed** `<ChucNang>.PrintConfig`: thêm mã vào ma trận phân quyền là quyết định BA (`04-quyet-dinh-ban-giao.md` C13).
- `R-TLMI-034` — gọi thẳng API mà thiếu quyền ⇒ server chặn `403` + `MSG_PMKT-E-14549_21_002`.
- `R-TLMI-035` — có quyền ở **một** chi nhánh là sửa được mẫu dùng chung mọi chi nhánh; truy vấn **không** lọc `chi_nhanh_id` (`INV-TLMI-011`).

### D11 · Schema JSON lên **version 2**, xoá sạch dữ liệu v1

- Mô hình mới khác v1 ở **cấu trúc khối** (7 loại → 4 chuẩn + tự do), **lưới ô khối tự do** (danh sách trường → ma trận ô có `gopDong`/`gopCot`), **ngữ nghĩa kế thừa** (khoá vắng mặt). Không có đường nâng cấp tự động nào đọc được ý định người dùng.
- Dữ liệu v1 **chưa từng tồn tại ngoài máy dev**: toàn bộ code Java của module `mau_in` **chưa commit** (xác nhận bằng `git -C cell-app status` 2026-09-19 — 19 mục `??`, trong đó có cả thư mục `cell/mau_in/`) ⇒ develop/staging có bảng nhưng **không có endpoint nào** ghi vào. `V1158` xoá sạch hai bảng là an toàn.
- `schema_version` chuyển **1 → 2**; `MauInJsonCodec` từ chối mọi JSON mang `schemaVersion != 2`.
- **Vì sao không viết bộ nâng cấp v1→v2:** không có bản ghi nào để nâng cấp; viết bộ chuyển đổi cho tập rỗng là code chết.

### D12 · Không có endpoint `DELETE` mẫu

- Bản cũ có `A4 DELETE /api/mau-in/{ma}` (`cell/mau_in/internal/controller/MauInController.java:79-85`). Đặc tả mới **không có** thao tác này: *Đặt lại mẫu chuẩn* chỉ đổi trên màn, **bấm Lưu mới có hiệu lực** (`R-TLMI-018`), và việc xoá bản ghi nằm **bên trong** `PUT` (`R-TLMI-021`).
- Giữ `DELETE` là cấp cho FE một đường vòng qua `R-TLMI-018` ⇒ **bỏ**.

### D13 · Mẫu chuẩn hệ thống sinh tại chỗ, không có bản ghi, không đi qua super-admin

- `R-TLMI-006`: mẫu chuẩn là **dữ liệu cố định sinh từ đặc tả form**, **không có entity riêng**.
- ⇒ Bỏ toàn bộ tầng "mặc định hệ thống" qua super-admin của bản cũ (`internal/client/MacDinhHeThong*`, cột `mac_dinh_nguon`, `mac_dinh_phien_ban`, trường `coMacDinhMoi`, `ProxyTargetId.SUPER_ADMIN`) khỏi **phạm vi phiếu này**. Chi tiết ở [09-tai-dung-va-bo-code-cu.md](09-tai-dung-va-bo-code-cu.md).
- **Vì sao không giữ cho chắc:** ba tầng mẫu (hệ thống → đóng gói → tuỳ chỉnh) làm `R-TLMI-021` (so với "mẫu chuẩn") mất nghĩa đơn trị — so với tầng nào? Đặc tả mới chỉ có **hai** trạng thái: có bản ghi / không có bản ghi (`R-TLMI-007`).

### D14 · Cộng gộp dòng: khoá **có thuế suất**, phạm vi **3 loại chứng từ**

Quyết định C01 + C30.

- Khoá gộp = *mã hàng + đơn vị tính + đơn giá + **thuế suất*** (+ *số lô, hạn sử dụng* nếu vật tư theo dõi theo lô).
- **Chỉ** áp cho **Hoá đơn · phiếu xuất kho · phiếu nhập kho** — giới hạn của BR51.5; `SCR:281` không nhắc lại **không** có nghĩa là mở rộng.
- Provider khai `boolean thuocDienCongGop()` (mặc định `false`) — xem [06](06-provider-nghiep-vu-va-kho-truong.md).
- Gộp chạy **TRƯỚC** khi dựng bảng (`R-TLMI-119`), trên bản sao `DuLieuChungTu`, không đụng dữ liệu gốc (`R-TLMI-271`).

---

## §1. Phạm vi

### Trong phạm vi

| Mã | Chức năng | UC | File con |
|---|---|---|---|
| `F01` | Mở màn Thiết lập mẫu in · Lưu mẫu · Xem trước sống | `PMKT-U-14549_21-01` | [03](03-api-thiet-lap-mau-in.md) |
| `F02` | Ảnh nền của mẫu · Logo đơn vị | `-01` (`R-TLMI-069`…`074`, `082`) | [04](04-api-anh-nen-va-logo.md) |
| `F03` | Menu In · Dựng bản in bằng mẫu tùy chỉnh | `PMKT-U-14549_21-02` | [05](05-api-in-mau-tuy-chinh.md) |
| `F04` | Provider theo nghiệp vụ · catalog · mẫu chuẩn hệ thống · kho trường | `-01` (`R-TLMI-006`, `009`, `165`) | [06](06-provider-nghiep-vu-va-kho-truong.md) |
| `F05` | Chuẩn hoá · kiểm tra 17 dòng · 3 thuật toán | `-01`, `-02` | [07](07-chuan-hoa-kiem-tra-va-thuat-toan.md) |
| `F06` | Thiết lập chung tối thiểu (giấy-chữ · 7 dòng đầu trang + Logo · 3 quy tắc in) | Q-03 `[USER]`, vốn thuộc epic `_20` | [02](02-hop-dong-json-thiet-lap-chung.md), [03](03-api-thiet-lap-mau-in.md) |

### NGOÀI phạm vi

| Không làm | Vì sao |
|---|---|
| Màn *Danh sách báo cáo* · *Tùy chỉnh báo cáo* · *Báo cáo yêu thích* · mở rộng/thu gọn nhóm báo cáo | Thuộc epic `PMKT-E-14549_20`; `04-quyet-dinh-ban-giao.md` §1 Q-03 bảng "Không làm" |
| Dựng PDF / ngắt trang / đo chữ phía máy chủ | D3 — FE dựng ở giai đoạn này |
| Kênh **super-admin** mẫu mặc định hệ thống (`MacDinhHeThong*`, `mac_dinh_nguon`, `coMacDinhMoi`) | D13 — `R-TLMI-006` nói mẫu chuẩn không có entity |
| **Lịch sử phiên bản** (`A8`/`A9` bản cũ) | 271 luật **không có luật nào** về lịch sử phiên bản. Bảng `prn_mau_in_lich_su` giữ lại (đã lên develop) và **vẫn ghi** để không mất dấu vết, nhưng **không lộ endpoint** — §12 `Q5` |
| Bảng danh mục chi nhánh `cfg_chi_nhanh` | Chưa tồn tại trong repo; đi qua `HoSoDonViPort` (D9) |
| Mẫu in cố định theo quy định (01-TT, 02-VT…) | `R-TLMI-013` — không sửa được, in như cũ; provider chỉ **trộn** chúng vào menu In qua `mauCoDinh(UUID)` |
| Seed mã quyền theo nghiệp vụ (`<ChucNang>.PrintConfig`, `.Print`) | D10 — quyết định BA |
| Hệ `bieuMau` (biểu mẫu động) | Quyết định C38 — hai chức năng độc lập, chỉ dùng lại kỹ thuật |

---

## §2. Hiện trạng đã khảo sát

### 2.1 Lệnh đã chạy và kết quả thật

```
$ git -C cell-app rev-parse --abbrev-ref HEAD
feat/mau-in
$ git -C cell-app log --oneline -1
37303112 feat(report): đăng ký quyền báo cáo phát sinh cặp định khoản (PMKT-E-10362) (#220)
$ git -C cell-app log --oneline -1 origin/develop
37303112  …                     ← nhánh ĐÃ fast-forward, không lệch develop
$ git -C cell-app status --porcelain | wc -l
29                              ← 10 dòng ' M'/'RM' + 19 dòng '??'
$ ls cell-app/src/main/resources/db/migration | sort -V | tail -3
V1152__cst_chung_tu_gia_thanh_xoa_cot_trang_thai_cu.sql
V1154__mst_loai_chung_tu_khop_ban_chuan_ba.sql       ← số lớn nhất LÚC ĐÓ ⇒ khi đó dự kiến V1155
$ find cell-app/src/main/java/vn/vtt/pmkt/cell/mau_in -name '*.java' | wc -l
57                              ← 3.848 dòng
```

> ⚠ `V1153` **khuyết** trong dãy (V1152 → V1154). Không phải lỗi của phiếu này; ghi nhận để người review không hoảng.
>
> ⚠ **Cập nhật 2026-09-21** — develop đã đi tiếp lên `86cada67` và chiếm mất `V1155` `V1156` `V1157`
> (`backfill_cay_tai_khoan_cap_3`, `fa_thoi_tam_dung_het_han_function`, `cst_phan_bo_chi_phi_them_co_da_luu_thiet_lap`).
> Ba migration của phiếu này đã đổi số **`V1155`→`V1158`**, **`V1156`→`V1159`**, **`V1157`→`V1160`**.

### 2.2 DB hiện có

| Bảng | Migration / `file:dòng` | Trạng thái với phiếu này |
|---|---|---|
| `prn_mau_in_tuy_chinh` | `V1148__prn_mau_in_tuy_chinh.sql:11-29` (15 cột) · unique một phần `(tenant_id, ma_loai_chung_tu) WHERE da_xoa=false` `:40-42` · RLS `tenant_isolation` `:44-48` · `GRANT … TO pmkt_app` `:50` | **Giữ, sửa bằng `V1158`/`V1159`** — thêm `ma_nghiep_vu`, đổi unique index, thêm 3 cột ảnh nền |
| `prn_mau_in_lich_su` | `V1150__prn_mau_in_lich_su.sql:14-53` | **Giữ**, thêm `ma_nghiep_vu`, dựng lại index (`V1158`) |
| `iam_quyen` + cây quyền | `V1149__iam_quyen_ht_mau_in.sql` — seed `HTMauIn.View` + `HTMauIn.Edit`, cây `D2.6`, có khối `DO $$` chốt đủ 2 mã | **Dùng lại nguyên** — không seed thêm (D10) |
| `iam_tenant` | `V1__create_database.sql` + `V203__iam_tenant_cau_hinh_columns.sql`; entity `platform_iam/tenant/internal/entity/Tenant.java:26-27` | **Thêm 3 cột logo** (`V1160`) |
| `cfg_cau_hinh_he_thong` | `V1__create_database.sql:6134-6157` — `kieu_du_lieu` cho phép `'JSON'` (`:6154`), `gia_tri text` (`:6140`), RLS bật (`:6157`) | **Dùng lại, KHÔNG đổi cấu trúc** (D8) |
| `cfg_chi_nhanh` | **không tồn tại** — `grep` 3 service ⇒ 0 kết quả | Đi qua `HoSoDonViPort` (D9) |

### 2.3 Base đã có — cần gì, lấy ở đâu

| Cần | Đã có ở base | `file:dòng` |
|---|---|---|
| Bọc response `ApiResponse<T>` | ✔ | `cell/core/response/ApiResponse.java` — đang dùng ở `cell/mau_in/internal/controller/MauInController.java:58` |
| Kiểm quyền `<MaChucNang>.<HanhDong>` | ✔ | `cell/core/controller/QuyenChecker.java:51-63` (`check`, không ném) · `:66-70` (`require`, ném `AccessDeniedException` → 403) |
| Hằng hành động chuẩn | ✔ | `cell/core/controller/QuyenChecker.java:29-46` — `VIEW` `VIEW_DETAIL` `CREATE` `EDIT` … |
| Mã chức năng màn thiết lập | ✔ | `cell/common/constant/MaChucNang.java:170` — `HT_MAU_IN = "HTMauIn"` |
| Khoá lạc quan kiểu JPA `@Version` | ✔ (mẫu tham chiếu) | `platform_iam/tenant/internal/entity/Tenant.java:20-24` — đã map sang `409 STALE_DATA` ở `GlobalExceptionHandler` |
| Entity gốc có audit + `da_xoa` | ✔ | `cell/mau_in/internal/entity/MauInTuyChinh.java:21-39` kế thừa `AggregateRootEntity` |
| Tra danh mục loại chứng từ / đơn vị gốc mà **không** chạm `master_data` | ✔ | `cell/mau_in/internal/repository/TraCuuMauInRepository.java` — native query trên `mst_*`; ngoại lệ có chủ ý ghi ở `cell/mau_in/package-info.java` |
| Hồ sơ doanh nghiệp + 5 người ký + cờ *In tên người ký* | ✔ | `platform_iam/tenant/internal/dto/CompanyInfoResponse.java:11-36`; endpoint `platform_iam/tenant/internal/controller/TenantConfigController.java:89` (`HTThongTinCongTy.View.Detail`) và `:95` (`.Edit`) |
| Đọc số thành chữ (*Số tiền bằng chữ*, `R-TLMI-165`) | ✔ | `cell/core/shared/text/SoTienBangChu.java` (vừa chuyển từ `tien_mat_tien_gui`, đang `RM` staged) |
| **Logo đơn vị** | ❌ **CHƯA CÓ** | `CompanyInfoResponse.java:11-36` không có trường logo ⇒ `V1160` + `A12` |
| **Thiết lập chung về giấy và chữ** | ❌ **CHƯA CÓ** | chỉ tồn tại bên trong từng mẫu (`cell/mau_in/internal/model/json/TrangJson.java:53-62`) ⇒ `F06` |
| `BaseCrudController` / `@Searchable` | ✔ nhưng **không dùng** | lý do đã ghi sẵn ở `MauInController.java:31-34` — không phải CRUD trên một entity tìm kiếm được |
| `ChungTuTemplate` · `GhiSoApi` | ✔ nhưng **không dùng** | phiếu này **không** tạo/ghi sổ chứng từ; `R-TLMI-271` cấm đổi dữ liệu |

### 2.4 Vùng cấm đã tôn trọng

- `cell/master_data/**` — **không đọc, không lấy làm mẫu**. Nhu cầu tra `mst_loai_chung_tu` đi bằng native query trong `TraCuuMauInRepository.java` (ngoại lệ đã ghi ở `cell/mau_in/package-info.java`); kế hoạch này giữ nguyên cách đó.
- `pmkt-docs/ba/Phase_2/**` — **không mở**; nguyên văn lấy từ `02-rules.md` và bản sao tạm mà `/audit-spec` đã kéo về thư mục tạm.

---

## §3. Kiến trúc

### 3.1 Phân tầng

```
Controller  (package-private; chỉ gate quyền + gọi service + bọc ApiResponse)
   ↓
Service     (MauInService · XemTruocService · DungBanInService · ThietLapChungService · AnhService)
   ↓
business/   (MauChuanBuilder · HopNhatCatalog · HopNhatThietLapChung · KiemTraMau ·
             ChuanHoaMau · ChiaDeuDoRong · GiaiHuongGiay · CongGopDong · DungKhoiDauTrang ·
             DungKhoiChuKy · MauInJsonCodec · DangKyProvider)
   ↓
repository/ (MauInTuyChinhRepository · MauInLichSuRepository · TraCuuMauInRepository)
   ↓
entity/     (MauInTuyChinh · MauInLichSu)        port/ (HoSoDonViPort → HoSoDonViTheoTenant)
```

Controller **không** chứa business logic, **không** gọi repository, **không** trả entity (luật 5 của `CLAUDE.md`).

### 3.2 Cây thư mục module (Modulith)

```
cell/mau_in/
├── package-info.java                      @ApplicationModule(displayName = "mau_in")
├── api/                                   @NamedInterface("api")     ← module NGHIỆP VỤ cài SPI
│   ├── package-info.java
│   ├── MauInProvider.java                 SPI
│   └── dto/                               @NamedInterface("api_dto")
│       ├── package-info.java
│       ├── MoTaMauIn.java · DuLieuChungTu.java · ChungTuTomTat.java · MucMenuIn.java
│       ├── KieuTruong.java · VaiTroKy.java
│       └── NghiepVuMauIn.java             MỚI — khai (maNghiepVu, tên) của một loại chứng từ
└── internal/
    ├── controller/   MauInController · ThietLapChungInController      (package-private)
    ├── dto/          MauInManHinhResponse · LuuMauInRequest · KetQuaLuuDto ·
    │                 XemTruocResponse · BanInResponse · MucMenuInDto · ThietLapChungDto · …
    ├── entity/       MauInTuyChinh · MauInLichSu
    ├── model/        LoaiKhoi · LoaiO · MaLoiMauIn · GioiHanMauIn · MaQuyenMauIn ·
    │   │             MaNghiepVuMauIn · HanhDongLichSu · NguonMau
    │   └── json/     MauInJson · TrangJson · KhoiJson(sealed) · KhoiDauTrangJson ·
    │                 KhoiTieuDeJson · KhoiBangJson · KhoiChuKyJson · KhoiTuDoJson ·
    │                 OLuoiJson · ThuocTinhTruongJson · ThietLapChungJson
    ├── port/         HoSoDonViPort · HoSoDonVi                        MỚI (Q-14)
    ├── repository/   MauInTuyChinhRepository · MauInLichSuRepository · TraCuuMauInRepository
    └── service/
        ├── MauInService · XemTruocService · DungBanInService · ThietLapChungService · AnhService
        ├── adapter/  HoSoDonViTheoTenant                              (hiện thực port)
        └── business/ MauChuanBuilder · HopNhatCatalog · HopNhatThietLapChung ·
                      KiemTraMau · ChuanHoaMau · ChiaDeuDoRong · GiaiHuongGiay ·
                      CongGopDong · DungKhoiDauTrang · DungKhoiChuKy ·
                      MauInJsonCodec · DangKyProvider · KetQuaKiemTra · LoiMau
```

Ba luật Modulith đã tuân:

1. Mặc định `internal/` — `api/` **chỉ** chứa SPI mà module nghiệp vụ phải cài, đúng lý do tồn tại của một `api/`.
2. `api/` và `api/dto/` **mỗi package một `package-info.java` khai `@NamedInterface`** — đã có sẵn, giữ nguyên.
3. Không đổ file phẳng ra gốc module.

### 3.3 Chiều phụ thuộc

```
ban_hang/… · chung_tu_mua_hang/… · tien_mat_tien_gui/…      (module NGHIỆP VỤ)
        │  cài MauInProvider (bean)
        ▼
    mau_in  ──► core · common.constant · platform_iam.tenant.api · platform_iam.nguoi_dung.api
```

`mau_in` **không import** module chứng từ nào — chỉ thu bean theo interface. Ranh giới này đang được `cell-app/src/test/java/vn/vtt/pmkt/cell/arch/MauInModularityTest.java` giữ; **giữ nguyên test đó**.

---

## §4. Danh mục API mục tiêu `A1…A12`

Base path **`/api/mau-in`**. Khoá nghiệp vụ nằm trên path theo Q-16: `{maLoai}/{maNghiepVu}`; loại chứng từ không chia nghiệp vụ dùng hằng `MaNghiepVuMauIn.MAC_DINH = "MAC_DINH"` (`R-TLMI-003`).

| # | Method · Path | Chức năng | Quyền gate | File con |
|---|---|---|---|---|
| `A1` | `GET /api/mau-in/{maLoai}/{maNghiepVu}` | Mở màn: mẫu hiệu lực + mẫu chuẩn + catalog + thiết lập chung | `HTMauIn.View` **+** `<ChucNang>.View.Detail` | [03](03-api-thiet-lap-mau-in.md) |
| `A2` | `PUT /api/mau-in/{maLoai}/{maNghiepVu}` | Lưu mẫu (kiểm → chuẩn hoá → so mẫu chuẩn → ghi hoặc xoá) | `HTMauIn.Edit` **+** `<ChucNang>.View.Detail` | [03](03-api-thiet-lap-mau-in.md) |
| `A3` | `GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu/{chungTuId}/xem-truoc` | Mẫu đã hợp nhất + dữ liệu thật để vẽ trang xem trước | `HTMauIn.View` **+** `<ChucNang>.View.Detail` | [03](03-api-thiet-lap-mau-in.md) |
| `A4` | `GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu-gan-day?q=&gioiHan=` | Chọn chứng từ nguồn để xem thử | `HTMauIn.View` **+** `<ChucNang>.View` | [03](03-api-thiet-lap-mau-in.md) |
| `A5` | `POST /api/mau-in/{maLoai}/{maNghiepVu}/anh-nen` (`multipart/form-data`) | Tải ảnh nền của mẫu | `HTMauIn.Edit` | [04](04-api-anh-nen-va-logo.md) |
| `A6` | `GET /api/mau-in/{maLoai}/{maNghiepVu}/anh-nen` | Tải về ảnh nền (bytes) | `HTMauIn.View` | [04](04-api-anh-nen-va-logo.md) |
| `A7` | `DELETE /api/mau-in/{maLoai}/{maNghiepVu}/anh-nen` | Bỏ ảnh nền | `HTMauIn.Edit` | [04](04-api-anh-nen-va-logo.md) |
| `A8` | `GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu/{chungTuId}/menu-in` | Menu In (mẫu cố định → Mẫu tùy chỉnh → Thiết lập mẫu in…) + cờ cấm in | `<ChucNang>.<hanhDongIn()>` | [05](05-api-in-mau-tuy-chinh.md) |
| `A9` | `GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu/{chungTuId}/ban-in` | Dựng bản in bằng mẫu tùy chỉnh | `<ChucNang>.<hanhDongIn()>` | [05](05-api-in-mau-tuy-chinh.md) |
| `A10` | `GET /api/mau-in/thiet-lap-chung` | Đọc thiết lập chung tối thiểu | `HTThongTinCongTy.View.Detail` | [03](03-api-thiet-lap-mau-in.md) |
| `A11` | `PUT /api/mau-in/thiet-lap-chung` | Ghi thiết lập chung tối thiểu | `HTThongTinCongTy.Edit` | [03](03-api-thiet-lap-mau-in.md) |
| `A12` | `POST` · `GET` · `DELETE /api/mau-in/thiet-lap-chung/logo` | Logo đơn vị (`multipart`) | `.Edit` / `.View.Detail` | [04](04-api-anh-nen-va-logo.md) |

**Endpoint bản cũ bị bỏ:**

| Bỏ | Vì sao |
|---|---|
| `GET /api/mau-in/loai-chung-tu` (A1 cũ, `MauInController.java:55-59`) | Đặc tả mới **không có** màn danh sách 47 loại; lối vào là **từ chính form chứng từ** (`R-TLMI-028`) |
| `DELETE /api/mau-in/{ma}` (A4 cũ, `:79-85`) | D12 |
| `GET /{ma}/lich-su` · `GET /{ma}/lich-su/{id}` (A8/A9 cũ, `:116-127`) | §1 NGOÀI phạm vi — 271 luật không có luật nào về lịch sử phiên bản |

---

## §5. Ma trận UC → endpoint → tài liệu

| UC | Bước | Endpoint | Luật chính |
|---|---|---|---|
| `PMKT-U-14549_21-01` Thiết lập mẫu in | Mở màn từ menu In hoặc nút *Sửa mẫu* | `A1` | `R-TLMI-011` · `012` · `028` · `031` · `034` |
| | Vẽ trang xem trước bằng dữ liệu chứng từ đang mở | `A3` | `R-TLMI-217` · `218` · `219` · `038` |
| | Đổi chứng từ nguồn xem thử | `A4` | `R-TLMI-217` |
| | Tải / bỏ ảnh nền | `A5` · `A6` · `A7` | `R-TLMI-069` · `071` |
| | Đặt lại mẫu chuẩn (chỉ trên màn) | — *(mẫu chuẩn đã nằm trong `A1`)* | `R-TLMI-016` · `018` · `019` |
| | Lưu | `A2` | `R-TLMI-021` · `037` · `111` · `239` · `243` · `246` · `247` · `258` |
| `PMKT-U-14549_21-02` In bằng mẫu tùy chỉnh | Mở menu In | `A8` | `R-TLMI-023` · `024` · `033` · `261` |
| | Chọn *Mẫu tùy chỉnh* → dựng bản in | `A9` | `R-TLMI-259` · `260` · `262` · `264` · `266` · `267` · `271` |
| Q-03 (nền, vốn thuộc epic `_20`) | Đọc / ghi thiết lập chung + logo | `A10` · `A11` · `A12` | `R-TLMI-036`…`052` · `077` · `196` |

Mọi UC trong `4.usecases/` đều xuất hiện đúng một lần ở bảng trên (epic chỉ có hai UC).

---

## §6. Luồng tổng thể

### 6.1 Lưu mẫu (`A2`)

```
FE PUT {mau, phienBan}
  │
  ├─1 MauInJsonCodec.doc(mau)            mapper CHẶT — thuộc tính lạ ⇒ 400
  ├─2 provider(maLoai, maNghiepVu)       chưa có provider ⇒ 404 MAU_IN_NGHIEP_VU_CHUA_HO_TRO
  ├─3 KiemTraMau.kiem(mau, catalog)      17 dòng R-TLMI-239, CẢ Ở SERVER (R-TLMI-246)
  │      └─ có lỗi ⇒ 422 + LỖI ĐẦU TIÊN theo thứ tự R-TLMI-243 + C21, KHÔNG ghi gì
  ├─4 ChuanHoaMau.chuan(mau)             chia lại 100% (R-TLMI-111) · sắp khoá · bỏ null ·
  │                                      bỏ id kỹ thuật · bỏ cờ moi · bỏ ô TRONG không định dạng
  ├─5 MauChuanBuilder.dung(catalog) → ChuanHoaMau.chuan(...)
  ├─6 hai chuỗi JSON bằng nhau?
  │      ├─ CÓ  ⇒ DELETE bản ghi (nếu có) · lịch sử hanh_dong=XOA · nguon=MAU_CHUAN
  │      └─ KHÔNG ⇒ kiểm phienBan (D6) ⇒ INSERT/UPDATE · lịch sử hanh_dong=LUU
  └─7 @Transactional bao trọn bước 6 (R-TLMI-247 · INV-TLMI-012); lỗi ⇒ rollback (R-TLMI-249)
```

### 6.2 Dựng bản in (`A9`)

```
GET .../ban-in
  ├─1 quyen.require(<ChucNang>, provider.hanhDongIn())        R-TLMI-034
  ├─2 ThietLapChungService.doc()                              đọc TẠI LÚC IN (R-TLMI-038 · 264)
  ├─3 hai quy tắc cấm in (chưa ghi sổ · đã khoá sổ)           R-TLMI-261 · 266(a)(b)
  │      └─ bị cấm ⇒ 409 + key i18n tooltip, KHÔNG dựng bản in
  ├─4 đọc bản ghi mẫu theo (tenant, maLoai, maNghiepVu)
  │      └─ KHÔNG có ⇒ MauChuanBuilder + cảnh báo MSG_PMKT-E-14549_21_103   R-TLMI-007 · 260
  ├─5 HopNhatThietLapChung.hopNhat(mau, thietLapChung)        điền mọi khoá vắng (R-TLMI-038)
  ├─6 GiaiHuongGiay.giai(mau)                                 TU_DONG → DOC/NGANG (R-TLMI-058 · 059)
  ├─7 provider.duLieuIn(chungTuId)                            dữ liệu thật, qua service module chủ
  ├─8 CongGopDong.gop(duLieu, thietLapChung, provider)        TRƯỚC khi dựng bảng (R-TLMI-119 · 266c)
  ├─9 HoSoDonViPort.theoChiNhanh(chungTu.chiNhanhId)          R-TLMI-078 · 267
  ├─10 lọc khối hien=true, giữ thứ tự mảng                    R-TLMI-262 · 207 · 208
  └─11 trả BanInResponse — KHÔNG ghi gì vào DB                R-TLMI-271
```

---

## §7. Migration dự kiến

> Repo này đánh số migration **tăng dần** (`V1148`…`V1157`), **không** dùng timestamp — biểu mẫu chung của `/plan-be` ghi timestamp nhưng thực tế repo không theo. Số lớn nhất trên `origin/develop` (`86cada67`, 2026-09-21) là `V1157` ⇒ phiếu này bắt đầu từ **`V1158`**.

| Version | Tên file | Nội dung | Ghi chú |
|---|---|---|---|
| `V1158` | `V1158__prn_mau_in_khoa_nghiep_vu.sql` | Xoá sạch dữ liệu v1 ở hai bảng · thêm `ma_nghiep_vu` vào `prn_mau_in_tuy_chinh` + `prn_mau_in_lich_su` · dựng lại unique index và index lịch sử · chuyển `schema_version` mặc định 2 | D2 · D11 |
| `V1159` | `V1159__prn_mau_in_anh_nen.sql` | `anh_nen bytea` · `anh_nen_kieu_tep` · `anh_nen_ten_tep` trên `prn_mau_in_tuy_chinh` + CHECK kiểu tệp | D7 · C08 |
| `V1160` | `V1160__iam_tenant_logo.sql` | `logo bytea` · `logo_kieu_tep` · `logo_ten_tep` trên `iam_tenant` | D7 · Q-03 |

SQL đầy đủ, RLS và `GRANT` theo đúng mẫu `V1148:44-50`: [08-thiet-ke-db.md](08-thiet-ke-db.md).

**Không có migration nào** cho thiết lập chung — dùng `cfg_cau_hinh_he_thong` sẵn có, không seed (D8).

---

## §8. Thứ tự thi công — 6 lô, 4 lô chia song song được

| Lô | Nội dung | Phụ thuộc | Song song? |
|---|---|---|---|
| **L0** — nền | `V1158`…`V1160` · `MaNghiepVuMauIn` · `MaQuyenMauIn` · viết lại `GioiHanMauIn` theo đặc tả mới · `MaLoiMauIn` đổi sang mã `MSG_PMKT-E-14549_21_nnn` · entity thêm `maNghiepVu` | — | ❌ phải xong trước |
| **L1** — hợp đồng JSON | 11 record `internal/model/json/**` theo [01](01-hop-dong-json-mau-in.md) · `MauInJsonCodec` · `ChuanHoaMau` | L0 | ✅ song song với L2 |
| **L2** — thiết lập chung + cổng đơn vị | `ThietLapChungJson` · `ThietLapChungService` · `A10` `A11` · `HoSoDonViPort` + `HoSoDonViTheoTenant` · logo (`A12`) | L0 | ✅ song song với L1 |
| **L3** — nghiệp vụ mẫu | (a) `KiemTraMau` 17 dòng · (b) `ChiaDeuDoRong` + `GiaiHuongGiay` + `CongGopDong` · (c) `MauChuanBuilder` + `HopNhatCatalog` + `HopNhatThietLapChung` | L1 + L2 | ✅ 3 nhánh (a)(b)(c) độc lập |
| **L4** — API | (a) `MauInController` `A1`–`A4` · (b) `AnhService` + `A5`–`A7` · (c) `DungBanInService` + `A8` `A9` | L3 | ✅ 3 nhánh độc lập |
| **L5** — provider đợt đầu | Cập nhật 4 provider sẵn có (`MDV` · `BH` · `PT` · `PC`) sang SPI mới: khai `maNghiepVu`, `thuocDienCongGop()`, catalog theo lưới | L3 | ✅ 4 provider độc lập nhau |

**Cổng bắt buộc trước khi báo xong bất kỳ lô nào:**

```bash
cd cell-app && ./gradlew unitTest                     # chỉ @Tag("unit"), ~1 phút, KHÔNG cần Docker
./docs/rules/trace.sh docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec be
git -C cell-app status                                # KHÔNG còn dòng '??' trong src/
```

`msg.sh` — xem §12 `Q6`, cổng này chưa chạy được vì PYC nằm trong vùng đóng băng.

---

## §9. Rủi ro kỹ thuật `R1…R9`

| # | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| `R1` | **8 luật vẫn mang trạng thái `CHỜ C<nn>` + dấu ⛔ trong `02-rules.md`** (`021` `046` `082` `119` `188` `199` `258` `266`) dù `01-conflict.md` đã `CLOSED-BA` hết. `docs/rules/truy-vet-luat.md §4`: code chạm luật `CHỜ` ⇒ `trace.sh` in **`VI-PHAM`** và trả exit ≠ 0 | **CAO** | **Trước khi chạy `/gen-be`**: cập nhật 8 luật đó trong `02-rules.md` từ `CHỜ C<nn>` → `CHỐT`, gỡ dòng `⛔ BỊ CHẶN`, thêm một dòng trỏ sang `04-quyet-dinh-ban-giao.md`. Không làm bước này thì cổng `trace.sh` đỏ dù code đúng |
| `R2` | 29 file chưa commit; CI `git reset --hard` rồi build trên **cây commit** ⇒ xanh local, đỏ deploy | **CAO** | `git add` **trước** khi sửa bất kỳ import/barrel nào trỏ tới file mới; `git status` sạch trước khi báo xong. (FE: `npm run check:committed` báo lỗi giả trên Windows — dùng `git status` thay, `client/CLAUDE.md §15.1`) |
| `R3` | Bốn bản sao cùng một model JSON (`cell-app` · `super-admin-service` · `client` domainKit · `client-admin` domainKit) | **CAO** | Phiếu này **cắt** kênh super-admin (D13) ⇒ còn 2 bản (BE + FE `client`). Hằng `GioiHanMauIn.java` là gương của `gioiHan.ts`; mọi thay đổi phải sửa cả hai + fixture vàng |
| `R4` | Đóng băng giá trị "theo chung" lúc Lưu — lỗi kinh điển của epic (`R-TLMI-038` Ghi chú: *"Đây là chỗ dễ code sai nhất của epic"*) | **CAO** | `HopNhatThietLapChung` là hàm **chỉ đọc**, không có đường gọi nào từ `MauInService.luu`. Bổ sung test `INV_TLMI_003_luu_o_theo_chung_thi_khoa_vang_mat` đọc thẳng chuỗi `cau_hinh` |
| `R5` | Thuật toán chia đều 100% sai làm tròn (`R-TLMI-114`) | TRUNG BÌNH | Ba ca chốt của BA làm test bắt buộc: `40/40/40 → 33/33/34`, `50/30 → 62/38`, `10/10/10/10 → 25/25/25/25`. Làm tròn **XUỐNG**, dồn phần thiếu vào **cột in cuối cùng**, cột `< 3` nâng lên `3` và **trừ vào cột rộng nhất** |
| `R6` | Cộng gộp dòng áp nhầm sang mọi loại chứng từ | TRUNG BÌNH | `provider.thuocDienCongGop()` mặc định `false`; chỉ hoá đơn / phiếu xuất kho / phiếu nhập kho trả `true`. Test khẳng định `PC` (phiếu chi) **không** gộp |
| `R7` | `mau_in` phải đọc `mst_loai_chung_tu` trong khi `master_data` đóng băng | TRUNG BÌNH | Giữ nguyên cách đã có: native query trong `TraCuuMauInRepository.java`, ngoại lệ ghi ở `cell/mau_in/package-info.java`. **Không** import `master_data` |
| `R8` | Không chạy được Testcontainers (máy cấm Docker) ⇒ không có test controller/repository thật | TRUNG BÌNH | Toàn bộ nghiệp vụ đẩy xuống `business/` để unit-test thuần; migration kiểm bằng `MauInMigrationTest` (đọc nội dung file `.sql`). **Báo rõ** phần Testcontainers chưa chạy khi bàn giao |
| `R9` | Đổi `schema_version` 1→2 trong khi `V1148`…`V1150` đã trên staging | THẤP | `V1158` xoá sạch dữ liệu; an toàn vì chưa endpoint nào ghi (D11). Nếu đến lúc deploy mà **đã có** bản ghi thật ⇒ **dừng, hỏi user**, không xoá |

---

## §10. Quyền

| Mã | Hành động | Đã seed? | Nguồn |
|---|---|---|---|
| `HTMauIn.View` | Danh sách | ✔ **đã seed** | `V1149__iam_quyen_ht_mau_in.sql` (nhóm *Tiện ích, thiết lập*, cây `D2.6`), đang trên `origin/develop` |
| `HTMauIn.Edit` | Chỉnh sửa | ✔ **đã seed** | như trên |
| `<MaChucNang nghiệp vụ>.View.Detail` | Xem chi tiết chứng từ | ✔ theo từng nghiệp vụ | `cell/common/constant/MaChucNang.java` |
| `<MaChucNang nghiệp vụ>.Print` | In | ⚠ **nhiều nghiệp vụ chưa có** — `MDV` và `BH` đang tạm gate bằng `View.Detail` | provider khai qua `hanhDongIn()` |
| `HTThongTinCongTy.View.Detail` / `.Edit` | Thiết lập chung + logo | ✔ đã seed | `TenantConfigController.java:91` · `:97` |

- **Không seed thêm mã nào** trong phiếu này (D10). Chưa seed ⇒ phải cấp quyền thủ công trước khi test (BR25).
- `R-TLMI-031` — quyền xét theo **nghiệp vụ tại chi nhánh đang làm việc**; `R-TLMI-035` — nhưng **mẫu áp mọi chi nhánh**. Hai điều này không mâu thuẫn: gate ở tầng quyền, truy vấn ở tầng dữ liệu **không lọc chi nhánh** (`INV-TLMI-011`).
- `R-TLMI-033` — không có quyền *Thiết lập mẫu in* nhưng có quyền *In* thì **vẫn in được** Mẫu tùy chỉnh ⇒ `A8`/`A9` **không** gate `HTMauIn.*`.

---

## §11. Mã thông báo (nguyên văn `6.messages.md`)

Chỉ liệt kê mã mà **BE** phát ra.

| Mã | Nguyên văn | Loại | BE phát khi |
|---|---|---|---|
| `MSG_PMKT-E-14549_21_002` | Bạn không có quyền thực hiện tác vụ này | Error | `403` — `R-TLMI-034` |
| `MSG_PMKT-E-14549_21_003` | Lỗi hệ thống, vui lòng thử lại sau | Error | `500` — `R-TLMI-249` · `R-TLMI-270` |
| `MSG_PMKT-E-14549_21_101` | Lưu mẫu in thành công! | Success | `A2` commit xong — `R-TLMI-248` |
| `MSG_PMKT-E-14549_21_103` | Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in theo mẫu chuẩn hệ thống | Info | `A9` khi chưa có bản ghi — `R-TLMI-260` |
| `MSG_PMKT-E-14549_21_201` | Tiêu đề bản in không được để trống, tối đa 255 ký tự | Error | V01 |
| `MSG_PMKT-E-14549_21_202` | Cỡ chữ tiêu đề phải là số nguyên từ 10 đến 36 | Error | V02 |
| `MSG_PMKT-E-14549_21_203` | Bảng "{TenBang}" phải giữ lại ít nhất 1 cột hiển thị | Error | V03 |
| `MSG_PMKT-E-14549_21_204` | Tên hiển thị của cột không được để trống, tối đa 100 ký tự | Error | V04 |
| `MSG_PMKT-E-14549_21_205` | Độ rộng cột phải là số nguyên từ 3 đến 90 | Error | V05 |
| `MSG_PMKT-E-14549_21_206` | Tên khối tự do không được để trống, tối đa 60 ký tự | Error | V06 |
| `MSG_PMKT-E-14549_21_207` | Mỗi mẫu tối đa 10 khối tự do | Error | V07 |
| `MSG_PMKT-E-14549_21_208` | Mỗi khối tự do tối đa 20 dòng | Error | V08 |
| `MSG_PMKT-E-14549_21_209` | Ảnh nền phải là tệp jpg hoặc png, dung lượng tối đa 1MB | Error | V10 — `A5` |
| `MSG_PMKT-E-14549_21_210` | Mã màu phải có dạng #rrggbb | Error | V11 |
| `MSG_PMKT-E-14549_21_211` | Tiêu đề ô ký tự do không được để trống, tối đa 60 ký tự | Error | V12 |
| `MSG_PMKT-E-14549_21_212` | Tên hiển thị và chữ tự do tối đa 255 ký tự | Error | V13 |
| `MSG_PMKT-E-14549_21_213` | Căn lề phải là số từ 0 đến 5 cm | Error | V14 |
| `MSG_PMKT-E-14549_21_214` | Số cột để tự động in ngang phải là số nguyên từ 1 đến 50 | Error | V15 |
| `MSG_PMKT-E-14549_21_215` | Cỡ chữ phải là số nguyên từ 8 đến 20 | Error | V16 — **chỉ chặn phía máy chủ** (`R-TLMI-063`) |
| `MSG_PMKT-E-14549_21_216` | Mỗi khối tự do tối đa 6 cột | Error | V09 |

**Mã tạm (BA chưa cấp — `04-quyet-dinh-ban-giao.md` §5 L-4, §7.1):**

| Tình huống | Mã dùng tạm |
|---|---|
| Xung đột phiên bản khi Lưu (`R-TLMI-258`, D6) | `MSG_COMMON_001` + key i18n riêng cho câu hướng dẫn |
| Thiếu quyền **In** (C15) | `MSG_COMMON_003` — "Bạn không có quyền thực hiện chức năng {tên chức năng}…" (BR25.2) |
| 2 tooltip nút In disable (C14) | **không có mã** — chỉ key i18n, nguyên văn: *"Đơn vị không cho phép in chứng từ chưa ghi sổ"* · *"Đơn vị không cho phép in chứng từ đã khóa sổ"* |

> ⚠ Toàn bộ hằng `MSG_MAUIN_001…018` của bản code cũ (`cell/mau_in/internal/model/MaLoiMauIn.java`) là **mã tạm tự đặt**, phải thay bằng bộ `MSG_PMKT-E-14549_21_nnn` ở trên — xem [09](09-tai-dung-va-bo-code-cu.md).

---

## §12. ⚠️ Điểm cần BA / user xác nhận `Q1…Q8`

| # | Câu hỏi | Vì sao hỏi | Chặn code? |
|---|---|---|---|
| `Q1` | **Danh sách nghiệp vụ đợt đầu** và **mã quyền** của từng nghiệp vụ | `R-TLMI-014`: epic `_21` cố ý không khai. `04-quyet-dinh-ban-giao.md` §7.6 còn nợ. Kế hoạch tạm lấy 4 loại đã có provider (`MDV` `BH` `PT` `PC`) | ❌ — làm được với 4 loại tạm |
| `Q2` | **`maNghiepVu` của 4 loại đợt đầu là gì?** `mst_loai_chung_tu` chỉ có `code` cấp loại, không có cột nghiệp vụ | `R-TLMI-002`: nghiệp vụ = giá trị ô *Loại nghiệp vụ* trên form, **do epic nghiệp vụ định nghĩa** — epic `_21` không liệt kê | ⚠ **có** — provider phải khai; tạm dùng `MAC_DINH` cho cả 4 |
| `Q3` | Xác nhận **D3**: 7 luật layout gán tầng `BE` trong `02-rules.md` chuyển sang FE dựng (`R-TLMI-180` `181` `194` `195` `200` `263` `265`) | Đây là luật pixel; BE không có engine dựng trang | ❌ — nhưng `/verify-spec` sẽ chấm khác nếu không chốt |
| `Q4` | Thiết lập chung dùng quyền `HTThongTinCongTy.*` có đúng không, hay cần mã riêng | Q-03 làm thêm tầng thuộc epic `_20`; epic đó chưa khai mã quyền nào | ❌ |
| `Q5` | **Còn giữ lịch sử phiên bản mẫu không?** 271 luật không có luật nào về nó, nhưng bảng `prn_mau_in_lich_su` đã lên develop/staging | Bỏ hẳn thì bảng thành rác trên staging; giữ thì là tính năng ngoài đặc tả | ❌ — kế hoạch tạm **vẫn ghi**, **không lộ endpoint** |
| `Q6` | `msg.sh` cần đường dẫn PYC trong `pmkt-docs/ba/` — nhưng PYC này nằm trong **vùng đóng băng** `Phase_2` | Cổng `msg.sh` của `CLAUDE.md` không chạy được nếu không gỡ chặn | ⚠ — user quyết: bỏ qua cổng `msg.sh` cho phiếu này, hay chạy với `PMKT_ALLOW_PHASE2=1` |
| `Q7` | Cấp mã `MSG_` cho: xung đột phiên bản · thiếu quyền In · 2 tooltip nút In disable | `04-quyet-dinh-ban-giao.md` §7.1 | ❌ — có mã tạm |
| `Q8` | Ngoài hoá đơn / phiếu xuất kho / phiếu nhập kho, còn loại chứng từ nào thuộc diện **cộng gộp mặt hàng**? Map sang `mst_loai_chung_tu.code` nào? | `R-TLMI-119` Ghi chú giới hạn theo BR51.5 nhưng dùng tên chung, chưa map sang mã | ⚠ — provider phải khai đúng |

> **Không mục nào trong `01-conflict.md` còn `OPEN`.** Tám câu hỏi trên là **câu hỏi mới phát sinh khi lập kế hoạch**, không phải mâu thuẫn tài liệu — không mở lại cổng đặc tả.

---

## §13. Điều kiện nghiệm thu

**BA xác nhận:**

- ☐ `Q1`…`Q8` đã trả lời hoặc chấp nhận phương án tạm.
- ☐ JSON schema ở [01](01-hop-dong-json-mau-in.md) phủ đủ 5 nhánh logic của `3.crud-matrix.md` + lưới ô khối tự do.
- ☐ Nguyên văn tiếng Việt của 20 message giữ đúng `6.messages.md`.
- ☐ Chấp nhận 8 mục lệch tài liệu ở `04-quyet-dinh-ban-giao.md` §5 (L-1…L-8) + D3 của kế hoạch này.

**Dev xác nhận:**

- ☐ `cd cell-app && ./gradlew unitTest` xanh.
- ☐ `./docs/rules/trace.sh <spec> be` — **0 dòng `MISSING`** với luật `P0`; dòng `NO-TEST` được ghi nợ tường minh.
- ☐ `git -C cell-app status` **sạch** — không còn `??` trong `src/`.
- ☐ `V1158`…`V1160` có RLS + `GRANT … TO pmkt_app` đúng mẫu `V1148:44-50`; `MauInMigrationTest` đọc và khẳng định được.
- ☐ Ba ca chốt của `R-TLMI-114` xanh.
- ☐ Không file nào import `cell/master_data/**`; `MauInModularityTest` xanh.
- ☐ Postman collection xuất ra `docs/json/` (yêu cầu của `/gen-be`).

---

## §14. Quy chuẩn nghiệp vụ (BR) áp dụng

> ⚠ Epic này chạy theo bộ **BR Phase 2** cho riêng chức năng này (`04-quyet-dinh-ban-giao.md` §1 Q-02 `[USER]`). `BR50` · `BR51` **không có** trong bản Phase 1 mà `br.sh` đọc.

| BR | Bản | Áp ở đâu |
|---|---|---|
| **BR50.6** — phạm vi dữ liệu theo chi nhánh | Phase 2 | D2 · `INV-TLMI-011` — mẫu xếp **nhóm 1 (cấu hình hệ thống)**, không khai `ChiNhanhId` (quyết định C26) |
| **BR50.7** — thông tin in lấy theo chi nhánh ghi trên bản ghi | Phase 2 | D9 `HoSoDonViPort` · `R-TLMI-078` · `267` |
| **BR51.5** — quy tắc in chứng từ, cộng gộp mặt hàng, hướng giấy tự động | Phase 2 | D14 · `R-TLMI-058` · `119` · `266` |
| BR7 — precision & làm tròn | Phase 1 | `ChiaDeuDoRong` làm tròn **xuống**; `rong` là `Integer`, không `double` |
| BR20 — mã danh mục | Phase 1 | `ma_loai_chung_tu varchar(20)` · `ma_nghiep_vu varchar(50)` |
| BR25 — quyền | Phase 1 | §10 · `R-TLMI-031`…`035` · `MSG_COMMON_003` cho thiếu quyền In |
| BR26 — thông báo | Phase 1 | §11 — toast góc phải trên, sống độc lập với màn |
| BR28 — multi-tenant | Phase 1 | RLS `tenant_isolation` giữ nguyên trên cả hai bảng `prn_*`; cột mới không phá policy |
| BR29 — chính sách xoá | Phase 1 | ⚠ **lệch có chủ ý**: `R-TLMI-021` bắt **xoá thật** bản ghi khi mẫu bằng mẫu chuẩn, vì *vắng bản ghi* chính là trạng thái nghiệp vụ (`R-TLMI-007`, `INV-TLMI-002`). Lý do và cách xử lý cột `da_xoa`: [08](08-thiet-ke-db.md) §6 |
| BR46 — trường hệ thống bắt buộc | Phase 1 | Áp cho **bản ghi**, không áp cho từng nhánh JSON (`04-quyet-dinh-ban-giao.md` §1 Q-01) |

**BR chưa xử lý được:**

| BR | Vì sao |
|---|---|
| BR50 (Chi nhánh) đầy đủ | `cfg_chi_nhanh` chưa tồn tại trong repo — Q-14 để sẵn điểm nối, không hiện thực |
| BR51.5 phần "quy tắc đọc số chung" cho *Số tiền bằng chữ* | `R-TLMI-165` nhắc "theo quy tắc đọc số chung" nhưng **không trích mã BR nào** (`02-rules.md` §Z). Dùng lại `cell/core/shared/text/SoTienBangChu.java` đã có trong repo |

---

## §15. Tài liệu tham chiếu

| Loại | Đường dẫn |
|---|---|
| Quyết định bàn giao (**đè mọi thứ khác**) | `docs/doing/PMKT-E-14549-21-thiet-lap-mau-in-chung-tu-spec/04-quyet-dinh-ban-giao.md` |
| Sổ mâu thuẫn | `…-spec/01-conflict.md` (36 mục · 0 `OPEN`) |
| Luật & bất biến | `…-spec/02-rules.md` (271 luật `R-TLMI-001…271` + 12 `INV-TLMI-001…012`) |
| Kịch bản | `…-spec/03-scenarios.md` |
| Bản đồ nguồn | `…-spec/00-source-map.md` |
| Khung kiến trúc BE | `docs/rules/be-khung-kien-truc-chuan.md` · `cell-app/CLAUDE.md` · `CLAUDE.md` gốc |
| Quy ước truy vết | `docs/rules/truy-vet-luat.md` |
| Kế hoạch bản cũ (đối chiếu delta) | `docs/doing/mau-in-chung-tu/00-plan-tong-the.md` · `docs/doing/mau-in-chung-tu/01-hop-dong-json-va-api-v1.md` |
