# 06 · `F04` — Cơ chế provider theo nghiệp vụ, mẫu chuẩn hệ thống, kho trường

| | |
|---|---|
| Mã chức năng | `F04` |
| Luật phủ | `R-TLMI-002` · `003` · `006` · `009` · `013` · `014` · `092` · `093` · `101` · `106` · `107` · `109` · `165` · `166` · `167` · `169` · `182` |
| Quyết định gốc | `D2` (khoá theo cặp) · `D13` (mẫu chuẩn không có entity) · `D14` (cộng gộp) |
| Code hiện có | `cell/mau_in/api/MauInProvider.java:21-51` · `cell/mau_in/api/dto/MoTaMauIn.java:23-138` · `cell/mau_in/internal/service/business/DangKyProvider.java` |

---

## §1. Nguyên tắc: provider **MÔ TẢ**, `mau_in` **DỰNG**

`R-TLMI-006` — mẫu chuẩn hệ thống là *"dữ liệu cố định **sinh từ đặc tả form của epic nghiệp vụ**, **không có entity riêng**"*.

```
module nghiệp vụ                     mau_in
─────────────────                    ──────
MauInProvider (bean)   ──moTa()──►   MoTaMauIn (catalog)
                                          │
                                          ▼
                                   MauChuanBuilder.dung(catalog)
                                          │
                                          ▼
                                   MauInJson  ← mẫu chuẩn hệ thống, dựng TẠI CHỖ mỗi lần cần
```

Provider **không** tự viết JSON mẫu. Nhờ vậy 47 loại chứng từ dùng **cùng một cách dựng**, và đổi quy tắc dựng (ví dụ thứ tự khối) chỉ sửa một chỗ.

**Cấm đưa mẫu chuẩn xuống DB dưới bất kỳ hình thức nào** (cache bảng, seed, snapshot). Lý do: `INV-TLMI-002` định nghĩa *có bản ghi ⇔ đã tuỳ chỉnh*; một bản ghi "mẫu chuẩn" làm bất biến đó vô nghĩa.

---

## §2. SPI `MauInProvider` — bản v2

```java
public interface MauInProvider {

    /** R-TLMI-001 — mã mst_loai_chung_tu.code: "MDV", "BH", "PT", "PC"… */
    String maLoaiChungTu();

    /**
     * MỚI (Q-16) — R-TLMI-002 · R-TLMI-003.
     * Danh sách nghiệp vụ của loại chứng từ này. Loại KHÔNG chia nghiệp vụ trả đúng một phần tử
     * NghiepVuMauIn(MaNghiepVuMauIn.MAC_DINH, <tên loại>).
     */
    List<NghiepVuMauIn> nghiepVu();

    /** R-TLMI-006 · R-TLMI-009 — catalog của MỘT nghiệp vụ. */
    MoTaMauIn moTa(String maNghiepVu);

    /** R-TLMI-014 — hành động kiểm quyền khi in. Mặc định "Print". */
    default String hanhDongIn() { return "Print"; }

    /**
     * MỚI (D14) — R-TLMI-119 · R-TLMI-266(c).
     * Loại chứng từ có thuộc diện "Cộng gộp mặt hàng khi in" không (BR51.5:
     * CHỈ hoá đơn, phiếu xuất kho, phiếu nhập kho).
     */
    default boolean thuocDienCongGop() { return false; }

    /**
     * MỚI (D3) — R-TLMI-261 · R-TLMI-266(a)(b).
     * Trạng thái ghi sổ / khoá sổ của chứng từ, để mau_in áp hai quy tắc cấm in
     * mà KHÔNG phải biết bảng nào của module chủ.
     */
    TrangThaiInChungTu trangThaiIn(UUID chungTuId);

    /** R-TLMI-217 — dữ liệu THẬT, phải đi qua đúng service của module chủ. */
    DuLieuChungTu duLieuIn(UUID chungTuId);

    /** A4 — chứng từ gần đây để chọn xem thử. */
    List<ChungTuTomTat> chungTuGanDay(String tuKhoa, int gioiHan);

    /** R-TLMI-013 · R-TLMI-023 — mẫu in cố định theo quy định (01-TT, 02-VT…) để trộn vào menu In. */
    default List<MucMenuIn> mauCoDinh(UUID chungTuId) { return List.of(); }
}

/** R-TLMI-002 — một nghiệp vụ của loại chứng từ. */
public record NghiepVuMauIn(String ma, String ten) {}

/** R-TLMI-261 — hai cờ để áp quy tắc cấm in; chiNhanhId để tra hồ sơ đơn vị (R-TLMI-267). */
public record TrangThaiInChungTu(boolean daGhiSo, boolean daKhoaSo, UUID chiNhanhId) {}
```

### 2.1 Thay đổi so với bản đang có

| Thay đổi | Vì sao | Luật |
|---|---|---|
| **Thêm** `nghiepVu()` | Khoá mẫu là **cặp** (loại, nghiệp vụ); bản cũ chỉ biết loại | `R-TLMI-002` · `003` · Q-16 |
| `moTa()` → `moTa(String maNghiepVu)` | Hai nghiệp vụ của cùng loại có thể có **lưới khác nhau** ⇒ catalog khác nhau | `R-TLMI-009` · `092` |
| **Thêm** `thuocDienCongGop()` | Phạm vi cộng gộp giới hạn 3 loại chứng từ; không có cờ thì code phải hardcode danh sách mã ở `mau_in` | `R-TLMI-119` · C30 |
| **Thêm** `trangThaiIn(UUID)` | `mau_in` không được import module chứng từ; hai quy tắc cấm in cần trạng thái ghi sổ/khoá sổ + `chiNhanhId` | `R-TLMI-261` · `267` |
| **Bỏ** `duLieuMau()` | *"Không có chế độ dữ liệu mẫu"* — trang xem trước **luôn** vẽ bằng dữ liệu thật | `R-TLMI-219` |

> `duLieuMau()` của bản cũ được dùng cho màn danh sách 47 loại và cho editor phía super-admin. Cả hai đều **ngoài phạm vi** phiếu này (D13, §1 của [00](00-ke-hoach-tong.md)) ⇒ bỏ khỏi SPI. Nếu sau này super-admin quay lại thì thêm một SPI riêng, không nhét ngược vào đây.

### 2.2 Đăng ký & fail-fast

`DangKyProvider` (đã có) gom bean theo interface và **fail-fast** khi: mã trống · trùng `maLoaiChungTu` · `moTa().maLoaiChungTu()` lệch mã. **Bổ sung ba kiểm mới:**

1. `nghiepVu()` rỗng ⇒ lỗi khởi động.
2. Hai phần tử `nghiepVu()` trùng `ma` ⇒ lỗi khởi động.
3. `moTa(ma)` ném lỗi với một `ma` có trong `nghiepVu()` ⇒ lỗi khởi động.

`can(maLoai, maNghiepVu)` không tìm thấy ⇒ `404` `MAU_IN_NGHIEP_VU_CHUA_HO_TRO`.

---

## §3. Catalog `MoTaMauIn` — bản v2

Giữ khung của bản đang có (`cell/mau_in/api/dto/MoTaMauIn.java:23-33`), **sửa ba chỗ**:

```java
public record MoTaMauIn(
        String maLoaiChungTu,
        String maNghiepVu,                 // MỚI
        String ten,                        // tên loại chứng từ — mặc định của khoi[TIEU_DE].noiDung
        String nhom,
        String maChucNang,                 // mã kiểm quyền: <maChucNang>.View.Detail, .<hanhDongIn>
        String basePath,
        List<TruongCatalog> truong,        // KHO TRƯỜNG — R-TLMI-165
        List<LuoiCatalog> luoi,            // đổi tên từ `bang` — R-TLMI-092
        List<VaiTroKy> vaiTroKy,
        MacDinhMauIn macDinh) {

    /** R-TLMI-165 · R-TLMI-166 — một trường trong kho trường. */
    public record TruongCatalog(String k, String nhan, KieuTruong kieu) {}

    /** R-TLMI-092 — một LƯỚI trên form ⇒ một khối Bảng. */
    public record LuoiCatalog(String k, String ten, List<CotCatalog> cot) {}

    /**
     * R-TLMI-101 · R-TLMI-105 · R-TLMI-106 · R-TLMI-107 · R-TLMI-109.
     * @param rongForm độ rộng cột TRÊN LƯỚI FORM (đơn vị tuỳ ý) — dùng để suy độ rộng mặc định
     */
    public record CotCatalog(String k, String nhan, KieuTruong kieu, int rongForm) {}

    /** R-TLMI-085 · R-TLMI-095 — gợi ý dựng mẫu chuẩn. */
    public record MacDinhMauIn(String tieuDe, List<String> tenLuoi) {}
}
```

| Thay đổi | Vì sao | Luật |
|---|---|---|
| **Bỏ** `tongHop` | Không còn khối `TONG_HOP` — *"Thông tin chung / tổng tiền phải tự dựng bằng khối tự do"* | `R-TLMI-008` · `010` |
| **Gộp** `tongHop` vào `truong` | Kho trường = **mọi ô trên form trừ cột trong các lưới** — gồm cả ô tổng cuối form và `soTienBangChu` | `R-TLMI-165` |
| **Bỏ** `TruongCatalog.nhom` | Kho trường là **danh sách phẳng, KHÔNG chia nhóm**, xếp theo thứ tự các ô trên form | `R-TLMI-166` |
| **Bỏ** `CotCatalog.can` / `congDuoc` | Suy được từ `kieu`: cột số ⇒ căn `PHAI`, cột khác ⇒ `TRAI`; chỉ cột số có ô Cộng; cột **tiền** mặc định `cong = true` | `R-TLMI-105` · `106` · `107` |
| **Thêm** `CotCatalog.rongForm` | Độ rộng mặc định lấy **theo tỷ lệ độ rộng cột trên lưới form**, quy về 100 | `R-TLMI-109` |
| **Rút gọn** `MacDinhMauIn` | Mẫu chuẩn mới rất đơn giản: 4 loại khối thứ tự cố định, mọi lưới bật, mọi cột gốc in | `R-TLMI-008` · `009` |

---

## §4. Kho trường (`R-TLMI-165`) — provider khai gì

> **Kho trường = mọi ô trên form của nghiệp vụ TRỪ cột trong các lưới.**

| Nhóm ô | Ví dụ khoá | Bắt buộc có |
|---|---|---|
| Ô nhập đầu form | `soChungTu` · `ngayChungTu` · `ngayHachToan` · `maDoiTuong` · `tenDoiTuong` · `diaChi` · `dienGiai` | ✔ **gồm cả `soChungTu` và `ngayChungTu`** (`R-TLMI-165`) |
| Ô tổng cuối form | `tongTienHang` · `tongThueGTGT` · `tongThanhToan` | ✔ |
| *Số tiền bằng chữ* | `soTienBangChu` | ✔ — đọc từ ô **tổng thanh toán** theo quy tắc đọc số chung, dùng `cell/core/shared/text/SoTienBangChu.java` |
| Thông tin đơn vị | `donVi.ten` · `donVi.diaChi` · `donVi.mst` · `donVi.dienThoai` | ✔ — của **chi nhánh ghi trên chứng từ**, `mau_in` tự ghép từ `HoSoDonViPort`, **provider không khai** |

**Không** đưa vào kho trường: cột của các lưới (chúng thuộc khối Bảng — `R-TLMI-165`).

**Hai luật vòng đời:**

- Ô mới ở phiên bản sau **tự vào kho trường**, nhưng **không tự chen vào** khối tự do đã lưu (`R-TLMI-167`).
- Cột *Trường dữ liệu* trên màn **luôn chỉ đọc** — lấy theo catalog, không phải dữ liệu của mẫu (`R-TLMI-169` · `101`).

---

## §5. `MauChuanBuilder` — dựng mẫu chuẩn từ catalog

Đầu vào: `MoTaMauIn`. Đầu ra: `MauInJson` theo [01](01-hop-dong-json-mau-in.md), **đã chạy `ChuanHoaMau`**.

| Bước | Sinh gì | Luật |
|---|---|---|
| 1 | `trang` = **chỉ** `{ mauChu: "#000000", nen: { kieu: "KHONG" } }` — toàn bộ nhóm Giấy và chữ **để trống ⇒ theo thiết lập chung** | `R-TLMI-036` · `064` · `067` |
| 2 | `khoi[0]` = `DAU_TRANG`, `hien = true`, `dong = {}` (cả 7 ô theo chung) | `R-TLMI-008` · `076` · `077` |
| 3 | `khoi[1]` = `TIEU_DE`, `noiDung = moTa.macDinh().tieuDe()` (mặc định = **tên loại chứng từ**), `coChu = 18`, `can = GIUA`, `inHoa = true`, `inDam = true`, `dongNgayThang = true` | `R-TLMI-085`…`090` |
| 4 | Với mỗi `LuoiCatalog` (đúng thứ tự): một khối `BANG`, `ten = "Bảng " + luoi.ten()`, `hien = true`, `maLuoi = luoi.k()`, `inStt = true`, `dongCong = true`, `lapTieuDeMoiTrang = true`, `keO = DAY_DU`. `tenBang` = **trống** cho lưới **đầu tiên**, `= luoi.ten()` cho lưới sau | `R-TLMI-009` · `094` · `095` · `096` · `097` · `099` · `100` · `212` |
| 5 | Mỗi cột của lưới: `in = true`, `tenHienThi = cot.nhan()`, `can` suy từ `kieu` (số ⇒ `PHAI`), `cong = true` với cột **tiền**, `rong` = `cot.rongForm()` quy về tổng 100 bằng `ChiaDeuDoRong` | `R-TLMI-102`…`109` |
| 6 | Khối cuối = `CHU_KY`, `hien = true`, `dongNgayThang = true`, `choTrongKy = VUA`, 5 ô chức danh đúng thứ tự `NGUOI_LAP · KE_TOAN_TRUONG · GIAM_DOC · THU_KHO · THU_QUY`, `in` = `true·true·true·false·false`, `ghiChu` mặc định, `tieuDe` **vắng** (theo Thiết lập người ký) | `R-TLMI-182`…`190` |
| 7 | `truong = {}` · **không có khối `TU_DO`** | `R-TLMI-164` · `010` |

**Thứ tự khối cố định** — Thông tin đầu trang → Tiêu đề → các Bảng → Chữ ký; *"không có khối nào khác"* (`R-TLMI-008`, `INV-TLMI-008`).

**Xác định**: cùng một `MoTaMauIn` ⇒ cùng một chuỗi JSON, mọi lần gọi. Đây là điều kiện để phép so sánh ở `D5` chạy đúng. Có test ghim (`MauChuanBuilderTest`).

---

## §6. `HopNhatCatalog` — form đổi thì mẫu đã lưu xoay xở thế nào

| Tình huống | Xử lý | Luật |
|---|---|---|
| **Cột mới** trên lưới | Thêm vào **cuối** khối Bảng, `in = true`, gắn cờ `moi` cho FE; độ rộng lấy phần chia của `ChiaDeuDoRong` | `R-TLMI-093` |
| **Trường mới** trên form | Vào **kho trường**; **không** tự chen vào khối tự do nào | `R-TLMI-167` |
| **Lưới mới** trên form | Thêm một khối `BANG` mới vào **trước khối `CHU_KY`** (vị trí tự nhiên của bảng) | `R-TLMI-009` |
| **Cột bị xoá** khỏi lưới | Mở màn: hiện **mờ + nhãn "không còn trên form"**, đưa vào `canhBao[]` của `A1`; **Lưu: loại khỏi mẫu**. Dựng bản in: **bỏ qua im lặng**, không lỗi, không vỡ bản in | quyết định **C10** |
| **Trường bị xoá** khỏi form | Ô trong khối tự do trở thành **ô trống** khi in; mở màn thì mờ + nhãn; Lưu thì loại | quyết định **C10** |
| **Lưới bị xoá** khỏi form | Khối `BANG` tương ứng không in; mở màn thì mờ; Lưu thì loại | quyết định **C10** |

> **Nguyên tắc chốt (C10): bản in không bao giờ được vỡ vì cấu hình cũ.** `HopNhatCatalog` chỉ **lọc** — không bao giờ ném lỗi khi dựng bản in.
>
> Cờ `moi` là **cờ hiển thị của FE**, `ChuanHoaMau` **xoá** nó trước khi ghi ⇒ không lọt vào DB, không làm hỏng phép so sánh ở `D5`. (Bản cũ đã làm đúng việc này ở `MauInService.boCoMoi(...)`.)

---

## §7. Provider đợt đầu

> ⚠ **§12 `Q1` · `Q2` · `Q8` chưa có câu trả lời của BA.** Bảng dưới là **đề xuất tạm** dựa trên 4 provider đã tồn tại trong code chưa commit.

| Mã loại | Nghiệp vụ tạm | `maChucNang` | `hanhDongIn()` | `thuocDienCongGop()` | Class provider (`cell/…`) |
|---|---|---|---|---|---|
| `MDV` Chứng từ mua dịch vụ | `MAC_DINH` | `MuaDichVu` | `View.Detail` ⚠ chưa có `.Print` | `false` | `chung_tu_mua_hang/internal/service/business/MdvMauInProvider.java` |
| `BH` Chứng từ bán hàng | `MAC_DINH` ⚠ *(loại này có ô Loại nghiệp vụ trên form — cần BA chốt, `Q2`)* | `BanHangHoa` | `View.Detail` ⚠ | ⚠ **cần `Q8`** — nếu "Hoá đơn" thì `true` | `ban_hang/chung_tu_ban_hang/internal/service/business/BhMauInProvider.java` |
| `PT` Phiếu thu tiền mặt | `MAC_DINH` | `ThuTienTM` | `Print` | `false` | `tien_mat_tien_gui/internal/service/business/PhieuThuTienMatMauInProvider.java` |
| `PC` Phiếu chi tiền mặt | `MAC_DINH` | `ChiTienTM` | `Print` | `false` | `tien_mat_tien_gui/internal/service/business/PhieuChiTienMatMauInProvider.java` |

**43 loại còn lại chưa có provider** ⇒ `A1` trả `404`, menu In không có mục *Mẫu tùy chỉnh*. Đúng `R-TLMI-014` — nghiệp vụ nào có chức năng này là do **epic nghiệp vụ** khai báo.

**Thêm một provider = ba việc** (giữ nguyên quy trình đã có):

1. Một bean `MauInProvider` trong module chủ.
2. Một dòng trong `cell-app/src/test/java/vn/vtt/pmkt/cell/mau_in/XuatCatalogMauInTest.java` (hằng `CATALOG`).
3. Chạy `docs/doing/mau-in-chung-tu/sync-catalog.sh` để sinh lại snapshot catalog.

---

## §8. Kiểm thử

| Test | Input → kỳ vọng | Luật |
|---|---|---|
| `R_TLMI_006_mauChuanSinhTuCatalogKhongCoEntity` | Không có bản ghi nào trong DB; gọi `MauChuanBuilder` hai lần → **cùng một chuỗi JSON** | `R-TLMI-006` |
| `R_TLMI_008_mauChuanCoDungBonLoaiKhoiTheoThuTu` | Catalog 2 lưới → `khoi` = `DAU_TRANG, TIEU_DE, BANG, BANG, CHU_KY`, **không loại nào khác** | `R-TLMI-008` · `INV-TLMI-008` |
| `R_TLMI_009_nLuoiThiNKhoiBang` | Catalog 3 lưới → 3 khối `BANG`, mỗi khối đủ cột gốc, `hien=true` | `R-TLMI-009` |
| `R_TLMI_095_tenBangTrongChoLuoiDauTien` | Lưới 1 → `tenBang=""`; lưới 2 → `tenBang = tên lưới` | `R-TLMI-095` |
| `R_TLMI_107_congMacDinhCoVoiCotTien` | Cột `KieuTruong.TIEN` → `cong=true`; cột `SO` → `cong=false`; cột `CHUOI` → **không có khoá `cong`** | `R-TLMI-106` · `107` |
| `R_TLMI_109_doRongMacDinhTheoTyLeCotTrenForm` | `rongForm = 60/20/20` → `rong = 60/20/20`; `rongForm = 3/1/1` → `rong = 60/20/20` | `R-TLMI-109` |
| `R_TLMI_165_khoTruongGomMoiOTruCotLuoi` | Catalog có 5 trường + 1 lưới 4 cột → kho trường **5 phần tử**, không chứa khoá cột | `R-TLMI-165` |
| `R_TLMI_165_khoTruongCoSoChungTuVaSoTienBangChu` | Kho trường chứa `soChungTu`, `ngayChungTu`, `soTienBangChu` | `R-TLMI-165` · `091` |
| `R_TLMI_093_cotMoiVaoCuoiBangVaMacDinhIn` | Catalog thêm cột → mẫu đã lưu có cột mới ở **cuối**, `in=true`, cờ `moi=true` | `R-TLMI-093` |
| `R_TLMI_167_truongMoiKhongChenVaoKhoiTuDo` | Catalog thêm trường → `khoi[TU_DO].o` **không đổi** | `R-TLMI-167` |
| `R_TLMI_092_cotKhongConTrenFormThiBoQuaKhiIn` | Mẫu tham chiếu cột đã xoá → `A9` dựng được bản in, cột đó **vắng**, **không** lỗi | C10 |
| `R_TLMI_002_haiNghiepVuCungLoaiCoHaiCatalogKhacNhau` | `moTa("A")` và `moTa("B")` khác số lưới → hai mẫu chuẩn khác nhau | `R-TLMI-002` · `009` |
| `R_TLMI_003_loaiKhongChiaNghiepVuThiMotMau` | `nghiepVu()` một phần tử `MAC_DINH` → khoá mẫu dùng `MAC_DINH` | `R-TLMI-003` |
| `DangKyProviderTest_nghiepVuRongThiKhongKhoiDongDuoc` | `nghiepVu()` trả `List.of()` → lỗi khởi động | §2.2 |
| `DangKyProviderTest_trungMaNghiepVuThiKhongKhoiDongDuoc` | Hai `NghiepVuMauIn` trùng `ma` → lỗi khởi động | §2.2 |
| `R_TLMI_013_mauCoDinhVanTronVaoMenuVaKhongSuaDuoc` | Provider trả 2 `mauCoDinh` → `A8` có 2 mục `CO_DINH`, không có endpoint nào sửa được chúng | `R-TLMI-013` |

## §9. BR đã áp dụng

| BR | Bước |
|---|---|
| BR7 (precision) | `rongForm` quy về 100 bằng số nguyên, làm tròn **xuống** (§5 bước 5) |
| BR20 (mã danh mục) | `maLoaiChungTu` phải có thật trong `mst_loai_chung_tu` (bộ mã sau `V1032`); bean trùng mã ⇒ không khởi động |
| BR25 (quyền) | `moTa().maChucNang()` là nguồn duy nhất của mã quyền nghiệp vụ |
| BR50.7 (Phase 2) | Thông tin đơn vị trong kho trường do `mau_in` ghép từ `HoSoDonViPort`, provider không khai |
