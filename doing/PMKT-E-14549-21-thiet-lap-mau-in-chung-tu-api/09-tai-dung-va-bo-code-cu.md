# 09 · 29 file chưa commit — tái dùng gì, bỏ gì

| | |
|---|---|
| Nhánh | `cell-app` › `feat/mau-in`, HEAD `37303112` = `origin/develop` (đã fast-forward) |
| Trạng thái | `git status --porcelain` ⇒ **29 dòng**: 8 ` M` + 2 `RM` (đã staged) + 19 `??` |
| Nguồn của bản code cũ | Đợt 2026-09-17, dựng từ **mock HTML** + hỏi đáp trực tiếp với user; spec nội bộ `docs/doing/mau-in-chung-tu-spec/` (77 luật `R-MAUIN-*`) — **không** bắt nguồn từ tài liệu BA |
| Nguyên tắc | Bản cũ **hơn 70 % dùng lại được** ở phần khung; phần **mô hình dữ liệu và luật nghiệp vụ** phải viết lại theo `02-rules.md` |

> ⛔ **`R2` của [00 §9](00-ke-hoach-tong.md):** CI làm `git reset --hard` rồi build trên **cây commit**. 19 mục `??` ⇒ build local xanh, deploy đỏ. **`git add` file mới TRƯỚC khi sửa bất kỳ import nào trỏ tới nó.**

---

## §0. ⛔ BLOCKER phải xử lý trước mọi thứ khác

`src/main/resources/application.yml` (` M`) đưa **một token thật** làm giá trị mặc định, ở **hai chỗ**:

```yaml
        auth:
          type: INTERNAL_TOKEN
-          value: ${PMKT_INTERNAL_TOKEN:}
+          value: ${PMKT_INTERNAL_TOKEN:423654b07d1d57f92269322e2640a70054c1c239d5931394a6e2950dae598c64}
```

(một ở `pmkt.proxy.targets.control-plane.auth.value`, một ở khối `super-admin` mới thêm)

- **Vi phạm luật 7 của `CLAUDE.md`** — *Không commit secret*.
- Nếu commit lên GitHub thì token phải coi như **đã lộ** và phải **thu hồi**, không chỉ xoá dòng.

**Xử lý bắt buộc trước khi `git add`:**

1. Trả hai dòng về `value: ${PMKT_INTERNAL_TOKEN:}`.
2. Đặt token thật vào env local (`.env` / Run Configuration của IntelliJ), **không** vào `application.yml`.
3. Xác nhận với user token này đã dùng ở đâu; nếu từng nằm trong một commit nào đó thì **thu hồi và cấp lại**.

---

## §1. Tổng kết theo số

| Nhóm | Số file | Tái dùng nguyên | Sửa rồi dùng | Bỏ |
|---|---|---|---|---|
| Khung module `mau_in` (`api/`, `internal/` trừ model & business) | 21 | 8 | 10 | 3 |
| Model JSON (`internal/model/json/`) | 12 | 0 | 5 | 7 |
| Nghiệp vụ (`internal/service/business/`) | 8 | 2 | 5 | 1 |
| Kênh super-admin (`internal/client/`) | 3 | 0 | 0 | **3** |
| Lịch sử phiên bản | 6 | 4 | 0 | 2 (endpoint) |
| Provider + repository tra cứu (4 module nghiệp vụ) | 9 | 2 | 7 | 0 |
| Test | 22 | 5 | 12 | 5 |
| File sửa ngoài module | 9 | 5 | 3 | 1 (⛔ §0) |

---

## §2. Module `cell/mau_in/` — bảng chi tiết

### 2.1 `api/` — SPI

| File | Quyết định | Vì sao |
|---|---|---|
| `package-info.java` · `api/dto/package-info.java` | ✅ **TÁI DÙNG NGUYÊN** | `@NamedInterface` đã khai đúng cho cả hai package — đúng luật 2 của Modulith |
| `MauInProvider.java` | 🔧 **SỬA** | Thêm `nghiepVu()`, `moTa(String)`, `thuocDienCongGop()`, `trangThaiIn(UUID)`; bỏ `duLieuMau()` — [06 §2](06-provider-nghiep-vu-va-kho-truong.md) |
| `dto/MoTaMauIn.java` | 🔧 **SỬA NHIỀU** | Bỏ `tongHop`, bỏ `TruongCatalog.nhom`, bỏ `CotCatalog.can`/`congDuoc`, thêm `maNghiepVu` và `CotCatalog.rongForm`, rút gọn `MacDinhMauIn` — [06 §3](06-provider-nghiep-vu-va-kho-truong.md) |
| `dto/DuLieuChungTu.java` | ✅ **TÁI DÙNG NGUYÊN** | Hình dạng `{truong, bang, tongHop, kieu}` vẫn đúng; **nguyên tắc "giá trị thô, có kiểu, BE không định dạng hộ"** (ghi ở `:10-13`) đúng với đặc tả mới |
| `dto/KieuTruong.java` | ✅ **TÁI DÙNG NGUYÊN** | `CHUOI · SO · TIEN · NGAY · LOGIC` — đủ để suy căn lề (`R-TLMI-105`) và ô Cộng (`R-TLMI-106` · `107`) |
| `dto/VaiTroKy.java` | ✅ **TÁI DÙNG NGUYÊN** | Đúng 5 vai trò của `R-TLMI-182`, đúng cả thứ tự mặc định `R-TLMI-183` |
| `dto/MucMenuIn.java` | 🔧 **SỬA** | Enum `Loai` thêm `DUONG_KE` và `THIET_LAP` để phủ `R-TLMI-023` (thứ tự menu có **đường kẻ**) |
| `dto/ChungTuTomTat.java` | ✅ **TÁI DÙNG NGUYÊN** | Dùng cho `A4` |
| `dto/NghiepVuMauIn.java` · `dto/TrangThaiInChungTu.java` | ➕ **MỚI** | Q-16 · `R-TLMI-261` |

### 2.2 `internal/model/json/` — mô hình dữ liệu

| File | Quyết định | Vì sao |
|---|---|---|
| `MauInJson.java` | 🔧 **SỬA** | Thêm `maNghiepVu`, thêm `truong` (map thuộc tính trường), `schemaVersion = 2` |
| `TrangJson.java` | 🔧 **SỬA NHIỀU** | 4 lề **phẳng** thay vì `Le` lồng ([01 §3.1](01-hop-dong-json-mau-in.md)); thêm `soCotTuDongNgang`; `nen` đổi `{kieu, doDam, phu, anhId}` → `{kieu, doDam, canAnh}`; **bỏ** `logo` (chuyển thành ô tick của khối đầu trang) và `chanTrang` (đặc tả mới không có) |
| `KhoiJson.java` | 🔧 **SỬA** | Sealed interface còn **5** nhánh (`DAU_TRANG` `TIEU_DE` `BANG` `CHU_KY` `TU_DO`); bỏ `coChu()` và `khoa()` khỏi phần chung ([01 §4.0](01-hop-dong-json-mau-in.md)) |
| `KhoiDonViJson.java` | 🔧 **VIẾT LẠI** → `KhoiDauTrangJson` | 5 dòng có nhãn + in đậm → **map 7 khoá `Boolean`** kế thừa từng ô (`R-TLMI-077` · `049`) |
| `KhoiTieuDeJson.java` | 🔧 **SỬA** | Thêm `inHoa`, `dongNgayThang`; giới hạn tiêu đề **80 → 255** (`R-TLMI-085`) |
| `KhoiBangJson.java` | 🔧 **SỬA** | `nguon` → `maLuoi`; `TieuDe{noiDung,hien,dam,can}` → **một chuỗi `tenBang`**; `Cot` bỏ `moi` khi ghi, `nhan` → `tenHienThi`, `hien` → `in` |
| `KhoiChuKyJson.java` | 🔧 **SỬA** | Bỏ `inTen` (luôn theo thiết lập chung — `R-TLMI-196`); `O` tách rõ ô chức danh / ô tự do; **bỏ trần 4 ô** (`R-TLMI-193`) |
| `KhoiTuDoJson.java` | ❌ **BỎ, VIẾT LẠI** | Bản cũ là **danh sách trường** rải vào lưới; đặc tả mới cần **ma trận ô có toạ độ** (`dong`/`cot`/`gopDong`/`gopCot`) để gộp/tách ô, thêm/xoá dòng-cột, kéo ô đổi chỗ. Danh sách tuần tự **không biểu diễn được** ô gộp 2×3 giữa lưới |
| `TruongInJson.java` | ❌ **BỎ** | Thay bằng `OLuoiJson` (một ô của lưới) + `ThuocTinhTruongJson` (thuộc tính của trường, dùng chung cả mẫu — `R-TLMI-156`) |
| `BoCucBangJson.java` | ❌ **BỎ** | `soCot`/`keO`/`rongNhan` của khối trường — khối tự do mới **cột rộng bằng nhau, không kẻ ô riêng** (`R-TLMI-131`) |
| `KhoaJson.java` | ❌ **BỎ** | `{viTri, xoa}` suy được từ `loai` khối ([01 §4.0](01-hop-dong-json-mau-in.md)) |
| `KhoiThongTinJson.java` · `KhoiTongHopJson.java` | ❌ **BỎ** | `R-TLMI-008` *"không có khối nào khác"*; `R-TLMI-010` *"Thông tin chung / tổng tiền phải tự dựng bằng khối tự do"* |
| `OLuoiJson.java` · `ThuocTinhTruongJson.java` · `ThietLapChungJson.java` | ➕ **MỚI** | [01 §4.5](01-hop-dong-json-mau-in.md) · [01 §5](01-hop-dong-json-mau-in.md) · [02 §2](02-hop-dong-json-thiet-lap-chung.md) |

### 2.3 `internal/model/` — hằng số & enum

| File | Quyết định | Vì sao |
|---|---|---|
| `GioiHanMauIn.java` (110 dòng) | 🔧 **VIẾT LẠI PHẦN LỚN** | Bảng đối chiếu ở §3 dưới — **13 hằng lệch đặc tả mới** |
| `MaLoiMauIn.java` | 🔧 **SỬA** | Thay toàn bộ `MSG_MAUIN_001…018` (mã **tạm tự đặt**) bằng `MSG_PMKT-E-14549_21_nnn` của `6.messages.md` — [00 §11](00-ke-hoach-tong.md) |
| `LoaiKhoi.java` | 🔧 **SỬA** | 7 → 5 giá trị; `DON_VI` → `DAU_TRANG` |
| `NguonMau.java` | 🔧 **SỬA** | Còn **hai** giá trị `MAU_CHUAN` · `TUY_CHINH` (bỏ tầng `MAC_DINH_HE_THONG`/`MAC_DINH_DONG_GOI` — `D13`) |
| `HanhDongLichSu.java` | ✅ **TÁI DÙNG NGUYÊN** | `LUU` · `XOA` khớp CHECK của `V1150` |
| `GioiHanLichSuMauIn.java` | ✅ **TÁI DÙNG NGUYÊN** | Trần 50 bản/loại |
| `LoaiO.java` · `MaQuyenMauIn.java` · `MaNghiepVuMauIn.java` | ➕ **MỚI** | `TRONG`/`TRUONG`/`CHU` · Q-15 · Q-16 |

### 2.4 `internal/service/` và `business/`

| File | Quyết định | Vì sao |
|---|---|---|
| `business/MauInJsonCodec.java` | ✅ **TÁI DÙNG** (đổi `schemaVersion` 1→2) | Mapper **chặt**, thuộc tính lạ ⇒ lỗi — đúng thứ `D4` và `R-TLMI-246` cần |
| `business/DangKyProvider.java` | 🔧 **SỬA** | Gom bean + fail-fast đã đúng; thêm 3 kiểm mới cho `nghiepVu()` ([06 §2.2](06-provider-nghiep-vu-va-kho-truong.md)); `can(ma)` → `can(ma, nghiepVu)` |
| `business/KetQuaKiemTra.java` · `business/LoiMau.java` | ✅ **TÁI DÙNG** | Thêm trường `duongDan` để FE nhảy tới ô lỗi (`R-TLMI-244`) |
| `business/KiemTraMau.java` (465 dòng) | 🔧 **VIẾT LẠI LUẬT, GIỮ KHUNG** | Khung "gom lỗi rồi trả danh sách" giữ; **17 dòng luật thay hoàn toàn** theo `R-TLMI-239`; thêm thứ tự lỗi đầu tiên `R-TLMI-243` + C21 |
| `business/ChuanHoaMau.java` (162 dòng) | 🔧 **SỬA NHIỀU** | Thêm: xoá khoá `null`, đánh số lại id, xoá ô `TRONG`, xoá `gop*`=1, xoá `truong` mồ côi, `trim()`, hạ `mauChu` về chữ thường — [07 §1](07-chuan-hoa-kiem-tra-va-thuat-toan.md) |
| `business/MauChuanBuilder.java` (269 dòng) | 🔧 **VIẾT LẠI** | Mẫu chuẩn mới đơn giản hơn nhiều: 4 loại khối, toàn bộ nhóm Giấy-và-chữ **để trống** (kế thừa), không khối `THONG_TIN`/`TONG_HOP` — [06 §5](06-provider-nghiep-vu-va-kho-truong.md) |
| `business/HopNhatCatalog.java` (267 dòng) | 🔧 **SỬA** | Logic thêm/bớt cột, cờ `moi` **dùng lại được**; bỏ phần hợp nhất `THONG_TIN`/`TONG_HOP`; thêm quyết định C10 (mờ + nhãn "không còn trên form") |
| `MauInService.java` (260 dòng) | 🔧 **SỬA NHIỀU** | Giữ khung; đổi khoá sang cặp; **thêm** so sánh với mẫu chuẩn để xoá bản ghi (`D5`); **bỏ** `danhSachLoai()`, `xoa()` |
| `GiaiMauHieuLuc.java` (121 dòng) | ❌ **BỎ** | Chuỗi **3 tầng** (hệ thống → đóng gói → tuỳ chỉnh) — `D13` chỉ còn **2** trạng thái. Thay bằng `HopNhatThietLapChung` (khác bản chất: hợp nhất **ô**, không phải chọn **tầng**) |
| `DonViInService.java` (116 dòng) | 🔧 **CHUYỂN THÀNH PORT** | Nội dung tra hồ sơ đơn vị + người ký **dùng lại được gần hết**; đổi thành `service/adapter/HoSoDonViTheoTenant implements HoSoDonViPort` (`D9` · Q-14) |
| `MauInLichSuService.java` (139 dòng) | ✅ **GIỮ phần ghi**, ❌ **bỏ phần đọc** | Vẫn ghi lịch sử (§1 [00](00-ke-hoach-tong.md)); bỏ `danhSach()` / `chiTiet()` vì không lộ endpoint (§12 `Q5`) |
| `business/ChiaDeuDoRong` · `GiaiHuongGiay` · `CongGopDong` · `HopNhatThietLapChung` · `DungKhoiDauTrang` · `DungKhoiChuKy` | ➕ **MỚI** | [07](07-chuan-hoa-kiem-tra-va-thuat-toan.md) |
| `XemTruocService` · `DungBanInService` · `ThietLapChungService` · `AnhService` | ➕ **MỚI** | [03](03-api-thiet-lap-mau-in.md) · [04](04-api-anh-nen-va-logo.md) · [05](05-api-in-mau-tuy-chinh.md) |

### 2.5 `internal/client/` — kênh super-admin

| File | Quyết định | Vì sao |
|---|---|---|
| `MacDinhHeThongClient.java` · `MacDinhHeThongRest.java` · `MacDinhHeThongCache.java` | ❌ **BỎ KHỎI PHẠM VI PHIẾU NÀY** | `D13` — `R-TLMI-006`: mẫu chuẩn là dữ liệu cố định sinh từ đặc tả form, **không có entity riêng** ⇒ không có tầng mặc định nào để tải về |

> **Không xoá khỏi đĩa ngay.** Ba file này chưa commit; nếu sau này super-admin quay lại thì chúng còn nguyên giá trị (`ProxyClient` + ETag + cache TTL đã chạy). Đề xuất: **để lại ở một nhánh riêng** `feat/mau-in-super-admin` rồi bỏ khỏi `feat/mau-in`, thay vì xoá mất.

### 2.6 `internal/controller/`, `dto/`, `entity/`, `repository/`

| File | Quyết định | Vì sao |
|---|---|---|
| `controller/MauInController.java` | 🔧 **VIẾT LẠI ĐƯỜNG DẪN, GIỮ CÁCH GATE** | Cách gọi `quyen.require(...)` tường minh trong thân method là đúng (lý do ghi ở `QuyenChecker.java:15-23`); path đổi sang `{maLoai}/{maNghiepVu}`; `A1` cũ, `A4` cũ, `A8`/`A9` cũ **bỏ** — [00 §4](00-ke-hoach-tong.md) |
| `entity/MauInTuyChinh.java` | 🔧 **SỬA** | Thêm `maNghiepVu` + 3 cột ảnh nền; bỏ map `mac_dinh_*`; **thêm `@Version`** cho `phienBan` (`D6`) |
| `entity/MauInLichSu.java` | 🔧 **SỬA** | Thêm `maNghiepVu` |
| `repository/MauInTuyChinhRepository.java` | 🔧 **SỬA** | Truy vấn theo **cặp** khoá; thêm projection `MauInBanGon` để `A1` không kéo ảnh ([08 §7](08-thiet-ke-db.md)) |
| `repository/MauInLichSuRepository.java` | 🔧 **SỬA** | Thêm `maNghiepVu` vào truy vấn ghi |
| `repository/TraCuuMauInRepository.java` (92 dòng) | ✅ **TÁI DÙNG NGUYÊN** | Native query trên `mst_*` — **cách duy nhất đúng** để tra danh mục mà không chạm vùng đóng băng `master_data`; ngoại lệ đã ghi ở `package-info.java` |
| `dto/LuuMauInRequest.java` | ✅ **TÁI DÙNG NGUYÊN** | `{mau: JsonNode @NotNull, phienBan: Integer}` — đúng hợp đồng `A2` |
| `dto/KetQuaLuuDto.java` | 🔧 **SỬA** | Thêm `mauDaChuanHoa` ([03 §2](03-api-thiet-lap-mau-in.md)) |
| `dto/MauInHieuLucDto.java` | 🔧 **VIẾT LẠI** → `MauInManHinhResponse` | Bỏ `macDinh{}`, `coMacDinhMoi`, `thayDoi`; thêm `mauChuan`, `thietLapChung`, `coAnhNen` |
| `dto/DuLieuInDto.java` · `DuLieuInResponse.java` | 🔧 **SỬA** | Đổi thành `BanInResponse` / `XemTruocResponse`; `donVi` lấy từ `HoSoDonViPort` |
| `dto/LoaiChungTuMauInDto.java` | ❌ **BỎ** | Màn danh sách 47 loại không có trong đặc tả mới (`R-TLMI-028`) |
| `dto/MauInLichSuDto.java` · `MauInLichSuChiTietDto.java` | ❌ **BỎ** | Không lộ endpoint lịch sử (§12 `Q5`) |
| `package-info.java` (gốc module) | 🔧 **SỬA GHI CHÚ** | Cập nhật ranh giới: bỏ dòng về `ProxyTargetId.SUPER_ADMIN`; giữ nguyên ngoại lệ native query `mst_*` |

---

## §3. `GioiHanMauIn.java` — 13 hằng lệch đặc tả mới

| Hằng | Bản cũ | Đặc tả mới | Luật |
|---|---|---|---|
| `SCHEMA_VERSION` | `1` | **`2`** | `D11` |
| `TIEU_DE_MAX_LEN` | `80` | **`255`** | `R-TLMI-085` |
| `KHO` | `{A4, A5}` | **`{A3, A4, A5}`** | `R-TLMI-054` |
| `HUONG` | `{DOC, NGANG}` | **`{DOC, NGANG, TU_DONG}`** | `R-TLMI-055` |
| `FONT_CHO_PHEP` | 6 font | **`{Times New Roman, Arial}`** | `R-TLMI-062` |
| `O_KY_TOI_DA` | `4` | **bỏ trần** | `R-TLMI-193` |
| `NEN_DO_DAM_CANH_BAO` | `60` | **bỏ** — *"không có cảnh báo mềm"* | `R-TLMI-238` |
| độ đậm nền | `0…100` | **`5…100`** | `R-TLMI-072` |
| `SAI_SO_TONG_RONG` | `0.5` | **bỏ** — tổng **đúng bằng** 100 sau khi chia lại | `R-TLMI-111` · `INV-TLMI-005` |
| `SO_COT_MIN/MAX` (khối trường) | `1…4` | **`1…6`** (số cột khối tự do) | `R-TLMI-130` |
| `SPAN_DOC_MIN/MAX` | `1…4` | **`gopDong` tới `soDong`**, `gopCot` tới `soCot` | `R-TLMI-136` |
| `RONG_NHAN_*` | `15…60` | **bỏ** — khối tự do không có độ rộng nhãn | `R-TLMI-131` |
| `DONG_DON_VI` | 5 khoá | **7 khoá** (thêm `taiKhoanNganHang`, `logo`) | `R-TLMI-077` · C03 |

Thêm mới: `SO_DONG_TU_DO_MAX = 20` · `SO_COT_TU_DO_MAX = 6` · `KHOI_TU_DO_MAX = 10` · `TEN_KHOI_TU_DO_MAX = 60` · `TEN_HIEN_THI_COT_MAX = 100` · `TEN_HIEN_THI_TRUONG_MAX = 255` · `CHU_TU_DO_MAX = 255` · `TIEU_DE_O_KY_MAX = 60` · `SO_COT_TU_DONG_NGANG_MIN/MAX = 1/50` · `ANH_MAX_BYTE = 1 MB`.

> ⚠ `GioiHanMauIn.java` là **gương** của `client/src/base/domainKit/mauIn/constants/gioiHan.ts`. Mọi dòng trên phải sửa **cả hai bên**, fixture vàng là chỗ phát hiện lệch.

---

## §4. Chín file sửa ngoài module

| File | Trạng thái | Quyết định |
|---|---|---|
| `common/constant/MaChucNang.java` (+8) | ` M` | ✅ **GIỮ** — thêm `HT_MAU_IN = "HTMauIn"` ở `:170`, khớp seed `V1149`. Chỉ **sửa javadoc**: bỏ tham chiếu `docs/doing/mau-in-chung-tu-spec`, trỏ sang spec mới |
| `platform_iam/tenant/api/TenantConfigApi.java` (+30) | ` M` | 🔧 **SỬA** — record `ThongTinDonViIn` + `NguoiKyDonVi` **dùng lại được nguyên**; chỉ đổi javadoc từ `R-MAUIN-080…083` sang `R-TLMI-078` · `186` · `196`. Đây chính là nguồn của `HoSoDonViTheoTenant` (`D9`) |
| `platform_iam/tenant/internal/adapter/TenantConfigAdapter.java` (+20) | ` M` | ✅ **GIỮ** — hiện thực `thongTinDonViIn()`; bổ sung trả `coLogo` sau `V1160` |
| `core/shared/text/SoTienBangChu.java` (`RM`, staged) | `RM` | ✅ **GIỮ** — chuyển từ `tien_mat_tien_gui` sang `core/shared/text` là **đúng**: `R-TLMI-165` bắt kho trường của **mọi** nghiệp vụ có `soTienBangChu`. ⚠ Dùng `git mv`, **không** `mv` trần (đã đúng — trạng thái là `RM`) |
| `tien_mat_tien_gui/.../DuLieuInPhieuThuChi.java` (+36) | ` M` | 🔧 **SỬA** — dùng lại logic dựng `DuLieuChungTu`; đổi theo SPI mới |
| `integration_ops/proxy/api/dto/ProxyTargetId.java` (+2) | ` M` | ❌ **HOÀN TÁC** — hằng `SUPER_ADMIN` chỉ phục vụ kênh super-admin đã bỏ (`D13`). Giữ lại là để một hằng chết trong `api/` của module khác |
| `bieu_mau_proxy/.../BieuMauProxyRest.java` (+7) | ` M` | ✅ **GIỮ — nhưng TÁCH COMMIT RIÊNG.** Đây là **sửa lỗi thật, không liên quan mẫu in**: `@ConditionalOnProperty` thoả cả khi giá trị **rỗng** ⇒ bean sinh ra với `baseUrl=""` và vỡ lúc chạy bằng `500 "URI is not absolute"` (log 2026-09-18, màn `/bieu-mau` chết). Commit riêng `fix(bieu-mau): …` |
| `reporting/.../ReportServiceRest.java` (+6) | ` M` | ✅ **GIỮ — TÁCH COMMIT RIÊNG** cùng lý do trên |
| `src/main/resources/application.yml` (+27) | ` M` | 🔧 **SỬA + ⛔ §0** — (a) **bỏ token thật** khỏi hai chỗ; (b) **bỏ** khối `pmkt.mau-in.super-admin` và `pmkt.proxy.targets.super-admin` (`D13`); (c) **GIỮ** `pmkt.report-service.url` default `http://localhost:8083` — cùng bản vá với hai file trên; (d) **THÊM** `spring.servlet.multipart.max-file-size: 2MB` cho `A5`/`A12` ([04 §4](04-api-anh-nen-va-logo.md)) |

---

## §5. Provider và repository tra cứu của 4 module nghiệp vụ

| File | Quyết định | Vì sao |
|---|---|---|
| `chung_tu_mua_hang/.../MdvMauInProvider.java` | 🔧 **SỬA** | Cài SPI mới: `nghiepVu()`, `moTa(String)`, `trangThaiIn(UUID)`, `thuocDienCongGop()`; bỏ `duLieuMau()` |
| `chung_tu_mua_hang/.../MdvMoTaMauIn.java` | 🔧 **SỬA** | Catalog theo `MoTaMauIn` v2: gộp `tongHop` vào `truong`, bỏ `nhom`, thêm `rongForm` |
| `chung_tu_mua_hang/.../TraCuuInMuaHangRepository.java` | ✅ **TÁI DÙNG NGUYÊN** | Truy vấn dữ liệu in bổ sung, không phụ thuộc mô hình mẫu |
| `ban_hang/.../BhMauInProvider.java` · `BhMoTaMauIn.java` | 🔧 **SỬA** | Như `MDV`. ⚠ `BH` có thể có **nhiều nghiệp vụ** — §12 `Q2` |
| `ban_hang/.../TraCuuInBanHangRepository.java` | ✅ **TÁI DÙNG NGUYÊN** | |
| `tien_mat_tien_gui/.../AbstractPhieuThuChiMauInProvider.java` | 🔧 **SỬA** | Giữ `mauCoDinh(UUID)` gọi `InPhieuThuChiService.danhSachMau(phieu)` — **đúng `R-TLMI-013` · `023`**: trộn mẫu jrxml sẵn có vào menu In |
| `tien_mat_tien_gui/.../PhieuThuTienMatMauInProvider.java` · `PhieuChiTienMatMauInProvider.java` | 🔧 **SỬA** | Như trên |
| `tien_mat_tien_gui/.../PhieuThuChiMoTaMauIn.java` | 🔧 **SỬA** | Catalog v2 cho `PT` và `PC` |

---

## §6. 22 file test

| Test | Quyết định | Vì sao |
|---|---|---|
| `arch/MauInModularityTest.java` | ✅ **TÁI DÙNG NGUYÊN** | Giữ ranh giới Modulith của `mau_in` — càng quan trọng sau khi thêm `port/` |
| `mau_in/MauInMigrationTest.java` | 🔧 **MỞ RỘNG** | Thêm khẳng định cho `V1158`…`V1160` — [08 §10](08-thiet-ke-db.md) |
| `mau_in/MauInTestData.java` | 🔧 **VIẾT LẠI** | Fixture theo schema v2 |
| `mau_in/XuatCatalogMauInTest.java` | 🔧 **SỬA** | Hằng `CATALOG` 4 dòng giữ; thêm `maNghiepVu` |
| `internal/client/MacDinhHeThongCacheTest.java` · `MacDinhHeThongRestTest.java` | ❌ **BỎ** cùng code | `D13` — theo `MacDinhHeThong*` sang nhánh riêng |
| `internal/controller/MauInControllerQuyenTest.java` | 🔧 **SỬA** | Khung test gate quyền **rất dùng được**; đổi danh sách endpoint và thêm tầng quyền (b) `<ChucNang>.View.Detail` |
| `internal/service/MauInServiceTest.java` (13 test) | 🔧 **SỬA NHIỀU** | Đổi tên test sang `R_TLMI_*`; thêm case xoá bản ghi (`D5`), lệch phiên bản (`D6`) |
| `internal/service/MauInLichSuServiceTest.java` (8) | 🔧 **RÚT GỌN** | Chỉ giữ phần **ghi** lịch sử |
| `internal/service/GiaiMauHieuLucTest.java` (5) | ❌ **BỎ** | Theo `GiaiMauHieuLuc` (`D13`) |
| `internal/service/DonViInServiceTest.java` (4) | 🔧 **ĐỔI TÊN** → `HoSoDonViTheoTenantTest` | Nội dung fallback `mst_don_vi` dùng lại được |
| `business/KiemTraMauTest.java` (13) | 🔧 **VIẾT LẠI CASE** | Khung giữ; 17 dòng của `R-TLMI-239` thay hoàn toàn |
| `business/ChuanHoaMauTest.java` (5) | 🔧 **MỞ RỘNG** | Thêm case xoá `null`, đánh số lại id, xoá ô `TRONG` |
| `business/HopNhatCatalogTest.java` (6) | 🔧 **SỬA** | Bỏ case `THONG_TIN`/`TONG_HOP` |
| `business/MauChuanBuilderTest.java` (5) | 🔧 **VIẾT LẠI** | Mẫu chuẩn mới |
| `business/MauInJsonCodecTest.java` (4) | ✅ **TÁI DÙNG** | "Thuộc tính lạ ⇒ lỗi" là hành vi vẫn cần |
| `business/DangKyProviderTest.java` (2) | 🔧 **MỞ RỘNG** | Thêm 3 kiểm `nghiepVu()` |
| `ban_hang/.../BhMauInProviderTest.java` · `BhMoTaMauInTest.java` · `BanHangInFixture.java` | 🔧 **SỬA** | Theo catalog v2 |
| `chung_tu_mua_hang/.../MdvMoTaMauInTest.java` | 🔧 **SỬA** | như trên |
| `tien_mat_tien_gui/.../PhieuThuChiMauInProviderTest.java` · `PhieuThuChiMoTaMauInTest.java` | 🔧 **SỬA** | như trên |
| `bieu_mau_proxy/internal/adapter/BieuMauProxyRestTest.java` | ✅ **GIỮ — TÁCH COMMIT RIÊNG** | Test của bản vá `baseUrl` rỗng (§4), không liên quan mẫu in |

**Test mới cần thêm:** `ChiaDeuDoRongTest` · `GiaiHuongGiayTest` · `CongGopDongTest` · `HopNhatThietLapChungTest` · `ThietLapChungServiceTest` · `AnhServiceTest` · `DungBanInServiceTest` · `XemTruocServiceTest` · `DungKhoiDauTrangTest` · `DungKhoiChuKyTest` — danh sách đầy đủ ở [10](10-truy-vet-luat-va-test.md).

---

## §7. Thứ tự dọn — làm đúng trình tự này

| # | Việc | Vì sao phải đúng thứ tự |
|---|---|---|
| 1 | **⛔ Gỡ token khỏi `application.yml`** (§0) | Không được để lọt vào bất kỳ commit nào |
| 2 | Tách 3 file bản vá `report-service`/`bieu-mau` thành **commit riêng** và push trước | Chúng đang sửa một lỗi production thật, không nên bị kẹt trong PR mẫu in |
| 3 | Đưa `MacDinhHeThong*` + test sang nhánh `feat/mau-in-super-admin` rồi **xoá khỏi `feat/mau-in`** | Giữ lại công đã làm mà không kéo `D13` vào phạm vi |
| 4 | Hoàn tác `ProxyTargetId.SUPER_ADMIN` và khối `super-admin` trong `application.yml` | Phụ thuộc bước 3 |
| 5 | Viết `V1158`…`V1160` và `git add` **ngay** | Migration là nền của mọi thứ (`L0`) |
| 6 | Sửa `GioiHanMauIn` · `MaLoiMauIn` · `LoaiKhoi` · `NguonMau` rồi `git add` | Mọi file khác import chúng |
| 7 | Viết lại model JSON, `git add` **trước** khi sửa các file import chúng | ⛔ `R2` — thêm file mới rồi mới sửa import, không làm ngược |
| 8 | Phần còn lại theo lô `L1`…`L5` của [00 §8](00-ke-hoach-tong.md) | |
| 9 | `git status` phải **sạch** trước khi báo xong | ⛔ `R2` |
