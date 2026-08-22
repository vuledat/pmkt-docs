# F10 — Sinh bút toán hạch toán & bộ chứng từ kèm

| Mục | Nội dung |
|---|---|
| Mã chức năng | **F10** |
| UC nguồn | `PMKT-U-06475` §"Chi tiết bút toán tự động khi ghi sổ" (`UC_GhiSoTraLaiHangBan.md:365-374,419-446`) |
| Màn hình | `SCR_ThemMoiTraLaiHangBan.md:539-564` (bút toán 3 bước) · `README.md` §**BR19** (vòng đời bộ chứng từ) |
| Endpoint phụ trách | **không có endpoint riêng** — là thành phần của A7/A8/A12 (`sauKhiLuu`) và của `dinhKhoan[]` trong A4 |
| Nhóm chức năng BA | `1.function-breakdown.md` §Nhóm Hạch toán · §Nhóm Nhập kho · §Nhóm Hóa đơn |
| **Trạng thái** | ☐ chưa code |

## 1. Quyết định riêng

| # | Quyết định | Vì sao KHÔNG chọn phương án kia |
|---|---|---|
| 1.1 | Bảng mapping bút toán khai **dưới dạng dữ liệu**: `QuyTacTraLaiHangBan implements BoQuyTacButToan` | Mẫu `QuyTacBanHang.java:32-58`. Không tự viết vòng lặp ghép Nợ/Có: `TaoDinhKhoanApi.java:9-19` đã gom việc đó và bảo đảm BR36 |
| 1.2 | TK trả lại (5212) dùng vai trò **`VaiTroTaiKhoan.TK_NO`** | `VaiTroTaiKhoan.java:19-20` ghi rõ *"TK Nợ (vế Nợ chính, cũng là TK giảm giá / **TK trả lại**)"*; `:14-15` cấm nhầm với `TK_CHIET_KHAU`. **Không** tạo vai trò mới |
| 1.3 | Điều kiện áp dụng của từng nghiệp vụ thể hiện bằng **CÓ NẠP SỐ TIỀN hay không**, không phải `if` trong bảng quy tắc | `QuyTacBanHang.java:24-26`; `DinhKhoanBanHang.java:23-26` — nghiệp vụ nào không có tiền thì quy tắc tương ứng **tự** bị bỏ qua |
| 1.4 | **Đợt 1 KHÔNG sinh chứng từ con** (PNK · PC/UNC/Séc · HĐĐC); cờ vẫn lưu, bút toán vẫn sinh | §0-D6 |
| 1.5 | Bút toán bước 3 (giá vốn) **vẫn sinh** khi `kiemPhieuNhapKho = true` dù không tạo Phiếu nhập kho | Ghi nhận **giá trị** vào sổ cái ≠ biến động **số lượng** tồn kho. UC nói *"Bút toán 2: Nhập lại kho giảm Giá vốn (chỉ sinh khi tick 'Kiêm phiếu nhập kho')"* (`UC:372`) — điều kiện là **cờ**, không phải "phiếu đã tồn tại" |

---

## 2. Bảng mapping bút toán — `QuyTacTraLaiHangBan`

Nguồn: `UC_GhiSoTraLaiHangBan.md:365-374,430-446` + `SCR_ThemMoiTraLaiHangBan.md:539-558`.

| # | Nghiệp vụ (nhãn tab Hạch toán) | Vai trò Nợ | Vai trò Có | Số tiền | Điều kiện nạp tiền |
|---|---|---|---|---|---|
| 1 | **Giảm trừ doanh thu** | `TK_NO` (TK trả lại 5212) | `TK_CONG_NO` (131) | `thanhTien − chietKhau` từng dòng | luôn, khi `> 0` |
| 2 | **Thuế GTGT đầu ra** | `TK_THUE_GTGT` (33311) | `TK_CONG_NO` (131) | `tienThueGtgt` từng dòng | khi `> 0` |
| 3 | **Chi tiền ngay** | `TK_CONG_NO` (131) | `TK_TIEN` (111/112) | `thanhTien − chietKhau + tienThueGtgt` từng dòng | chỉ khi `thanhToanNgay = true` |
| 4 | **Nhập lại kho, giảm giá vốn** | `TK_KHO` (156/155) | `TK_GIA_VON` (632) | `soLuong × donGiaVon` từng dòng | chỉ khi `kiemPhieuNhapKho = true`, khi `> 0` |

```java
@Component
public class QuyTacTraLaiHangBan implements BoQuyTacButToan {

    private static final List<QuyTacButToan> QUY_TAC = List.of(
            new QuyTacButToan(DinhKhoanTraLai.NV_GIAM_TRU_DOANH_THU,
                    VaiTroTaiKhoan.TK_NO,        VaiTroTaiKhoan.TK_CONG_NO),
            new QuyTacButToan(DinhKhoanTraLai.NV_THUE_GTGT,
                    VaiTroTaiKhoan.TK_THUE_GTGT, VaiTroTaiKhoan.TK_CONG_NO),
            new QuyTacButToan(DinhKhoanTraLai.NV_CHI_TIEN,
                    VaiTroTaiKhoan.TK_CONG_NO,   VaiTroTaiKhoan.TK_TIEN),
            new QuyTacButToan(DinhKhoanTraLai.NV_GIA_VON,
                    VaiTroTaiKhoan.TK_KHO,       VaiTroTaiKhoan.TK_GIA_VON));

    @Override public String maLoaiChungTu() { return TraLaiSupport.MA_LOAI_CHUNG_TU; }
    @Override public List<QuyTacButToan> quyTac() { return QUY_TAC; }
}
```

### 2.1 So sánh với chứng từ bán hàng — bút toán trả lại là **chiều ngược**

| Nghiệp vụ | Bán hàng (`QuyTacBanHang.java:34-48`) | **Trả lại hàng bán** |
|---|---|---|
| Doanh thu / công nợ | Nợ `TK_CONG_NO` / Có `TK_DOANH_THU_PB` | **Nợ `TK_NO` (5212) / Có `TK_CONG_NO`** — đảo chiều |
| Thuế GTGT | Nợ `TK_CONG_NO` / Có `TK_THUE_GTGT` | **Nợ `TK_THUE_GTGT` / Có `TK_CONG_NO`** — đảo chiều |
| Giá vốn | Nợ `TK_GIA_VON` / Có `TK_KHO` | **Nợ `TK_KHO` / Có `TK_GIA_VON`** — đảo chiều |
| Tiền | Nợ `TK_TIEN` / Có `TK_CONG_NO` (thu) | **Nợ `TK_CONG_NO` / Có `TK_TIEN`** (chi) — đảo chiều |

⇒ Trả lại hàng bán là **bút toán đảo** của bán hàng ở cả 4 nghiệp vụ. Đây là kiểm tra chéo tốt khi review: nếu một cặp trùng chiều với bán hàng thì đã sai.

**Không dùng `TK_DOANH_THU_PB` cho vế Nợ**: TK trả lại là `5212` (*Hàng bán bị trả lại* — tài khoản giảm trừ doanh thu riêng theo TT200), không phải chính TK doanh thu `511x`. Vai trò `TK_NO` đúng theo LDM (`VaiTroTaiKhoan.java:19-20`).

---

## 3. `DinhKhoanTraLai` — phẳng hoá dòng chi tiết thành vai trò + số tiền

Mẫu 1:1 `DinhKhoanBanHang.java:63-134`.

```java
/** Phẳng hoá MỘT dòng chi tiết thành vai trò tài khoản + số tiền theo nghiệp vụ. */
private DongHachToan dungDong(ChungTuTraLaiHangBan ct, ChiTietTraLaiHangBan dong) {
    DongHachToan kq = DongHachToan.cua(dong.getId())
            .voiTaiKhoan(VaiTroTaiKhoan.TK_NO,        dong.getTaiKhoanTraLaiId())
            .voiTaiKhoan(VaiTroTaiKhoan.TK_CONG_NO,   dong.getTaiKhoanCongNoId())
            .voiTaiKhoan(VaiTroTaiKhoan.TK_THUE_GTGT, dong.getTaiKhoanThueGtgtId())
            .voiTaiKhoan(VaiTroTaiKhoan.TK_KHO,       dong.getTaiKhoanKhoId())
            .voiTaiKhoan(VaiTroTaiKhoan.TK_GIA_VON,   taiKhoanGiaVon(dong))   // §3.1
            .voiTaiKhoan(VaiTroTaiKhoan.TK_TIEN,      ct.getTaiKhoanTienId())
            .voiDienGiai(dong.getMoTa())
            .voiDienGiaiRieng(NV_THUE_GTGT, dong.getDienGiaiThue());

    // #1 — giảm trừ doanh thu: Thành tiền − Tiền CK
    BigDecimal giamTru     = TinhToanTraLai.giaTriHachToanQuyDoi(dong);   // đồng tiền hạch toán
    BigDecimal giamTruGoc  = TinhToanTraLai.giaTriHachToan(dong);         // nguyên tệ
    kq = napNeuDuong(kq, NV_GIAM_TRU_DOANH_THU, giamTru, giamTruGoc);

    // #2 — thuế GTGT đầu ra
    kq = napNeuDuong(kq, NV_THUE_GTGT, dong.getTienThueGtgtQuyDoi(), dong.getTienThueGtgt());

    // #4 — giá vốn: CHỈ khi kiêm phiếu nhập kho (1.5)
    if (ct.laKiemPhieuNhapKho()) {
        kq = napNeuDuong(kq, NV_GIA_VON, dong.getGiaVonQuyDoi(), dong.getGiaVon());
    }

    // #3 — chi tiền ngay: nạp số CÓ DẤU để bộ sinh tự đảo chiều khi âm
    if (ct.laThanhToanNgay()) {
        kq = kq.voiSoTien(NV_CHI_TIEN, TinhToanTraLai.phaiTraQuyDoi(dong), phaiTraNguyenTe(dong));
    }
    return kq;
}
```

Công thức số tiền:

```
giaTriHachToan(dong)  = thanhTien − chietKhau          // #1 · SCR:543 "Tổng tiền hàng − Tổng chiết khấu"
phaiTra(dong)         = thanhTien − chietKhau + tienThueGtgt   // #3 · SCR:552 "Tổng thanh toán"
giaVon(dong)          = soLuong × donGiaVon            // #4 · SCR:558
<x>QuyDoi             = <x> × tyGia                     // BR18
```

`napNeuDuong` (mẫu `DinhKhoanBanHang.java:136-143`): nạp **chỉ khi dương** — nghiệp vụ ngoài "Chi tiền ngay" không có nghĩa nghiệp vụ khi âm (thuế âm, giá vốn âm) ⇒ bỏ qua thay vì để bộ sinh đảo chiều thành một bút toán vô nghĩa. Riêng #3 nạp **số có dấu**: chứng từ có dòng chiết khấu thương mại lớn hơn tiền hàng → phải trả âm → bộ sinh tự đảo thành Nợ tiền / Có công nợ.

`dung(ct)` chỉ duyệt **dòng hàng** (`loaiDongHang = true`); dòng ghi chú không sinh bút toán ([02 §2-A5](02-xem-chi-tiet.md)).

`dung(ct)` **cố ý không ném lỗi** khi dòng thiếu tài khoản (`DinhKhoanBanHang.java:63-69`): hàm này còn phục vụ **tab Hạch toán của màn đang nhập dở** (`dinhKhoan[]` của A4). Việc bắt buộc đủ tài khoản khi ghi sổ do `KiemTraTraLai.kiemTraTruocGhiSo` lo ([07 §4](07-ghi-so.md) V53) — ở đúng chỗ chỉ ra được dòng nào thiếu ô nào.

### 3.1 TK giá vốn mặc định — luật riêng của epic

`UC:443-445` (nguyên văn): *"TK giá vốn lấy trong danh mục vật tư hh, Tuy nhiên nếu dm VTHH không có TK giá vốn thì lấy mặc định **632**"*
`SCR:457`: *"Ngầm định theo DM VTHH; nếu trống thì **632x đầu tiên**"*

```java
private UUID taiKhoanGiaVon(ChiTietTraLaiHangBan dong) {
    return dong.getTaiKhoanGiaVonId();   // FE đã resolve theo DM VTHH → 632x (constants.ts:121)
}
```

**Ai resolve mặc định 632x?** FE đã làm (`hooks/useDanhMucTraLai.ts` — *"TK ngầm định theo tiền tố"*, `IMPLEMENT.md:52`; hằng `TIEN_TO_TAI_KHOAN.giaVon = '632'`, `constants.ts:121`). BE **không** resolve lại: dòng đã ghi sổ phải giữ đúng TK người dùng thấy trên màn hình, và tra lại danh mục lúc ghi sổ có thể cho TK khác nếu danh mục vừa đổi.
BE chỉ **kiểm bắt buộc có** khi `kiemPhieuNhapKho = true` (V53 `_112`/`_113`).

> ⚠ Nếu BA muốn BE tự resolve (phòng client gửi thiếu): thêm một bước trong `truocKhiLuu` tra `mst_vat_tu.tai_khoan_gia_von_id` → fallback `632x` đầu tiên. **Không** làm mặc định — sẽ che mất lỗi thiếu dữ liệu. Ghi vào báo cáo.

---

## 4. Chuyển sang `DinhKhoan` của kernel

Mẫu 1:1 `DinhKhoanBanHang.java:146-166`:

```java
public List<DinhKhoan> sangDinhKhoan(ChungTuTraLaiHangBan ct, List<ButToan> butToan) {
    boolean ngoaiTe = ct.getTyGia() != null && ct.getTyGia().compareTo(BigDecimal.ONE) != 0;
    List<DinhKhoan> kq = new ArrayList<>(butToan.size());
    for (ButToan bt : butToan) {
        DinhKhoan dk = DinhKhoan
                .cua(bt.taiKhoanNoId(), bt.taiKhoanCoId(), bt.soTien(), bt.dienGiai())
                .voiChiTiet(bt.chiTietChungTuId())      // BẮT BUỘC trước khi ghi sổ
                .voiDoiTuong(ct.getKhachHangId());      // đối tượng công nợ
        if (ngoaiTe && SoTien.duong(bt.soTienNguyenTe())) {
            dk = dk.voiNgoaiTe(ct.getLoaiTienId(), ct.getTyGia(), bt.soTienNguyenTe());
        }
        kq.add(dk);
    }
    return kq;
}
```

Ba bất biến của kernel (`DinhKhoan.java:8-23`):

1. **`soTien` LUÔN là đồng tiền hạch toán** — sổ cái tổng hợp trên cột đó. Phần nguyên tệ chỉ đính kèm khi `tyGia ≠ 1`; gắn nguyên tệ cho chứng từ VND chỉ làm mọi dòng sổ cái mang thêm một bộ ba giá trị trùng lặp.
2. **`chiTietChungTuId` bắt buộc** — vừa là cột `NOT NULL` của `acc_so_cai`, vừa nằm trong khoá chống ghi trùng. Id này chỉ có **sau** khi lưu ⇒ định khoản dựng ở `sauKhiLuu`.
3. **Kernel tách mỗi `DinhKhoan` thành 2 dòng** `acc_so_cai` (vế Nợ + vế Có, hoán vị tài khoản/đối ứng) ⇒ cân đối Nợ/Có đúng **theo cấu trúc**, không tồn tại đường nào ghi được một vế mồ côi.

---

## 5. Bộ chứng từ (BR19) — vòng đời và trạng thái đợt 1

`README.md` §BR19 định nghĩa **bộ chứng từ**: chứng từ trả lại + tối đa 3 chứng từ con.

| Chứng từ con | Điều kiện tạo | Bảng đích | Module Java | Đợt 1 |
|---|---|---|---|---|
| Phiếu nhập kho | `kiemPhieuNhapKho = true` | `inv_phieu_nhap_kho` (`V1` có) | ❌ | **400 `NOT_SUPPORTED_YET`** · `_206` |
| Phiếu chi / UNC / Séc | `thanhToanNgay = true` + phương thức | `cb_phieu_chi` (`V1` có) | ❌ | **400 `NOT_SUPPORTED_YET`** |
| Hóa đơn điều chỉnh | `lapKemHoaDonDieuChinh = true` | `sal_dieu_chinh_hoa_don_ban_hang` (`V1:16706`) | ❌ | **400 `NOT_SUPPORTED_YET`** |

Cột liên kết **đã có sẵn** trên header: `phieu_nhap_kho_id`, `phieu_chi_id`, `dieu_chinh_hoa_don_ban_hang_id`, `so_chung_tu_phieu_chi`, `tai_khoan_tien_id`, `muc_dich_thu_chi_id` (`V1:16480+`, kèm COMMENT giải thích rõ mục đích từng cột) ⇒ **không** phải thêm cột cho phần này, chỉ cần điền khi module ra đời.

### 5.1 Vòng đời bộ chứng từ (ghi lại để lần sau cài đúng)

Nguyên văn `README.md` §BR19 — **không cài đợt 1**, nhưng phải giữ đúng khi làm:

| Thao tác | Tác động lên bộ |
|---|---|
| **Lưu** (chưa ghi sổ) | Toàn bộ chứng từ con được tạo ở trạng thái "Chưa ghi sổ" |
| **Ghi sổ** | Toàn bộ chứng từ con được ghi sổ **đồng bộ** |
| **Bỏ ghi sổ** | Toàn bộ chứng từ con được bỏ ghi sổ (nếu HĐ điện tử chưa ký) |
| **Xóa** | Cập nhật trạng thái "Đã xóa" cho **toàn bộ** bộ (soft delete) |
| **Sửa** | Chỉ sửa trên chứng từ cha; chứng từ con **tự động cập nhật** theo |

Toggle checkbox "Kiêm phiếu nhập kho" khi **chưa ghi sổ**:

| Sự kiện | Hành vi |
|---|---|
| **tick** + Lưu | tạo Phiếu nhập kho liên kết, trạng thái "Chưa ghi sổ" |
| **bỏ tick** + Lưu (đã từng tick và lưu) | soft delete Phiếu nhập kho liên kết. *"Thao tác này diễn ra ngầm — không hiển thị popup xác nhận"* |
| Lưu mà không đổi checkbox | không thay đổi Phiếu nhập kho |

Nguyên tắc (nguyên văn): *"Ghi sổ / Xóa / Bỏ ghi sổ luôn tác động toàn bộ bộ chứng từ, không thể thao tác riêng lẻ trên chứng từ con. Chỉ **sửa chi tiết** (kho nhập, số lô, …) mới cho phép thao tác riêng trên chứng từ con, miễn là chưa ghi sổ."*

⇒ Khi cài, chỗ đúng là các hook `sauKhiLuu` / `luuEntity` của 5 template + mở rộng V42/V62 để đọc **trạng thái** chứng từ con (hiện chặn rộng hơn — [05 §4](05-xoa.md), [08 §4](08-bo-ghi-so.md)).

### 5.2 BR16 · BR17 của SCR — map sang Hóa đơn điều chỉnh (không cài đợt 1)

`SCR:660-697` mô tả rất chi tiết cách map chứng từ trả lại → hóa đơn điều chỉnh. Ghi lại **hai luật số học** quan trọng nhất để lần sau không phải đọc lại 40 dòng:

```
HĐĐC.SoLuong(dòng)   = − SL trả lại                    // SCR:695 — "VD nếu trên CT hàng bán trả lại 2 thì trên HĐ điều chỉnh là -2"
HĐĐC.ThanhTien(dòng) = − thành tiền dòng trên CT trả lại // SCR:696
```
Các trường Tổng tiền hàng / Tổng CK / Tổng thuế / Tổng thanh toán trên HĐĐC **tự tính** theo quy tắc của màn HĐĐC, không copy (`SCR:672`).
Header HĐĐC lấy từ **tab Hóa đơn** của chứng từ trả lại (`SCR:690-693`), không phải từ tab Ghi giảm công nợ.

Cảnh báo khi sửa HĐĐC sinh kèm (`SCR:673`): *"Hóa đơn này được lập đồng thời với chứng từ trả lại hàng bán số &lt;BGG00001&gt;. Nếu muốn sửa, bạn phải sửa chứng từ trả lại hàng bán. Bạn có muốn xem chứng từ trả lại hàng bán không?"* — thuộc module hóa đơn.

---

## 6. Kiểm thử

### 6.1 Unit (`@Tag("unit")`) — **đây là nhóm test quan trọng nhất của epic**

| Lớp test | Case | Input → kỳ vọng |
|---|---|---|
| `QuyTacTraLaiHangBanTest` | 4 quy tắc | `quyTac().size() == 4`; đúng cặp vai trò §2 |
| | đảo chiều so với bán hàng | với mỗi nghiệp vụ tương ứng, cặp (Nợ, Có) là **hoán vị** của `QuyTacBanHang` (§2.1) |
| | `maLoaiChungTu` | khớp `TraLaiSupport.MA_LOAI_CHUNG_TU` (nếu lệch, `TaoDinhKhoanApi` ném 400 "chưa khai bảng quy tắc" — `TaoDinhKhoanApi.java:36-37`) |
| `DinhKhoanTraLaiTest` | **bước 1 luôn sinh** | 1 dòng: `thanhTien=10tr, chietKhau=500k` → bút toán Nợ `5212` / Có `131` = **9.5tr** |
| | **bước 1b thuế** | `tienThueGtgt=950k` → Nợ `33311` / Có `131` = 950k |
| | thuế = 0 | `tienThueGtgt=0` → **không** sinh bút toán thuế (`napNeuDuong`) |
| | **bước 2a giảm trừ công nợ** | `thanhToanNgay=false` → **KHÔNG** có bút toán nào cho `NV_CHI_TIEN` (SCR:550) |
| | **bước 2b chi tiền ngay** | `thanhToanNgay=true` → Nợ `131` / Có `111` = `9.5tr + 950k = 10.45tr` |
| | chi tiền âm | phải trả âm → bộ sinh **đảo** thành Nợ `111` / Có `131` |
| | **bước 3 giá vốn** | `kiemPhieuNhapKho=true`, `SL=2, ĐGvốn=3.5tr` → Nợ `156` / Có `632` = **7tr** |
| | không kiêm PNK | `kiemPhieuNhapKho=false` → **không** có bút toán giá vốn |
| | **BR36 không gộp** | 2 dòng chi tiết cùng cặp TK → **2 bút toán riêng**, không cộng thành 1 (`TaoDinhKhoanApi.java:22-27` gộp **chỉ trong phạm vi một dòng**) |
| | dòng ghi chú | `loaiDongHang=false` → không sinh bút toán nào |
| | thiếu tài khoản | dòng thiếu `taiKhoanTraLaiId` → nghiệp vụ #1 bị bỏ qua, **không** ném lỗi (§3) |
| | `chiTietChungTuId` | mọi `DinhKhoan` có `chiTietChungTuId ≠ null` |
| | đối tượng công nợ | mọi `DinhKhoan.doiTuongId == ct.khachHangId` |
| | ngoại tệ | `tyGia=24000` → `soTien` = VND, `soTienNguyenTe` = nguyên tệ, `loaiTienId` gắn |
| | VND | `tyGia=1` → `loaiTienId`/`tyGia`/`soTienNguyenTe` == `null` (không gắn nguyên tệ vô ích) |
| | tổng cân đối | `Σ soTien` các bút toán vế Nợ == `Σ` vế Có (kiểm chéo trước khi kernel kiểm) |
| `KiemTraTraLaiTest` | V53 chặn thiếu TK | xem [07 §8.1](07-ghi-so.md) |
| `TraLaiHangBanControllerTest` | V28 ba cờ | bật từng cờ → 400 `NOT_SUPPORTED_YET`, `messageId = _206` cho PNK (§5) |

### 6.2 Tích hợp (cần Docker — chưa chạy được, R8)

| Lớp | Kiểm gì |
|---|---|
| `DinhKhoanTraLaiIT` | ghi sổ chứng từ 1 dòng, kiêm PNK, thanh toán ngay → `acc_so_cai` có **8 dòng** (4 định khoản × 2 vế) |
| | `Σ ps_no == Σ ps_co` (trigger cân đối DB) |
| | mỗi dòng có `chung_tu_id`, `chi_tiet_chung_tu_id`, `doi_tuong_id` đúng |
| | chứng từ ngoại tệ → cột nguyên tệ + tỷ giá được ghi |
| | 3 dòng chi tiết cùng cặp TK → 3 × 2 = 6 dòng sổ cái, **không** gộp (BR36) |
| | `A6 GET /{id}/thong-tin-hach-toan` trả đúng các dòng vừa ghi |
| | `dinhKhoan[]` của A4 (dự kiến) **khớp** dòng sổ cái thật của A6 sau khi ghi sổ |

---

## 7. Điểm cần xác nhận (bổ sung cho §12 file gốc)

| # | Vấn đề | Bằng chứng | Xử lý tạm |
|---|---|---|---|
| a | **Vế Nợ của bước 1 dùng `TK_NO` hay `TK_DOANH_THU_PB`?** | (a) `VaiTroTaiKhoan.java:19-20`: `TK_NO` = *"vế Nợ chính, cũng là TK giảm giá / TK trả lại"* ⇒ dùng `TK_NO`; (b) `QuyTacBanHang.java:39-40` dùng `TK_DOANH_THU_PB` cho dòng chiết khấu thương mại (cũng là giảm trừ doanh thu) ⇒ có thể đọc là tiền lệ ngược | Dùng **`TK_NO`** (1.2) — javadoc nói đích danh "TK trả lại". Dev BE chốt khi review |
| b | **BE có tự resolve TK giá vốn mặc định 632x không?** | `UC:443-445` + `SCR:457` nói *"nếu trống thì lấy mặc định 632"* — không nói ai resolve; FE đã resolve (`constants.ts:121`) | BE **không** resolve, chỉ kiểm bắt buộc có (§3.1) |
| c | **`SCR:546` group-by** — *"Nếu có nhiều dòng chi tiết, hệ thống group-by theo từng cặp [TK Nợ] - [TK Có] trước khi sinh bút toán"* — **XUNG ĐỘT với BR36** | (a) `SCR:546` yêu cầu **group-by giữa các dòng**; (b) `business_rules.md:904-906` (BR36): *"hệ thống **không thực hiện gộp** các dòng bút toán có cùng tài khoản hạch toán… Mỗi cặp tài khoản phát sinh trên chứng từ phải được sinh thành 2 dòng bút toán riêng biệt"*; (c) `TaoDinhKhoanApi.java:26-27` gộp **chỉ trong phạm vi một dòng chi tiết** | Theo **BR36** (không gộp giữa các dòng) vì đó là quy chuẩn chung và kernel đã cài đúng vậy. **Đây là epic lệch BR — phải báo BA**: nếu BA giữ `SCR:546` thì phải sửa `TaoDinhKhoanApi` (kernel dùng chung, đụng cả bán hàng/mua hàng) ⇒ ticket riêng |

---

## 8. BR đã áp dụng

| BR | Áp ở bước nào |
|---|---|
| BR4 loại chứng từ | `maLoaiChungTu()` là khoá tra bảng quy tắc (`TaoDinhKhoanApi.java:33`) |
| BR7 precision & làm tròn | số tiền `decimal(18,2)` VND / `(18,4)` ngoại tệ; làm tròn ở kết quả cuối |
| BR9 mã chứng từ | §12-Q2 file gốc |
| BR12 trạng thái | bút toán chỉ sinh khi ghi sổ |
| BR16 cảnh báo nghiệp vụ | `_205` khi kernel từ chối định khoản |
| BR17 kỳ kế toán | kernel kiểm khi INSERT sổ cái |
| BR18 ngoại tệ | §4 — `soTien` = đồng tiền hạch toán, nguyên tệ đính kèm khi `tyGia ≠ 1` |
| **BR36 ghi nhận bút toán vào Sổ cái** | §2, §3, §6.1; ⚠ **lệch `SCR:546`** — xem §7-c |
| BR19 (README) bộ chứng từ | §5 — ghi lại đầy đủ, **không cài đợt 1** |
| BR41 tham chiếu chéo | không áp dụng |
| BR46 trường hệ thống | `nguoi_ghi_so`/`thoi_gian_ghi_so` do base |

**BR / chức năng chưa đạt đợt này** (khớp `1.function-breakdown.md`):

| Nhóm chức năng BA | Mục | Trạng thái |
|---|---|---|
| Nhóm Hạch toán | Tự động sinh bút toán hạch toán | ✅ |
| | Kiểm tra cân đối kế toán | ✅ (kernel + trigger DB) |
| | Xem bút toán chi tiết | ✅ (A4 `dinhKhoan[]` dự kiến + A6 sổ cái thật) |
| Nhóm Nhập kho | Kiểm tra hàng tồn kho · Lập phiếu nhập kho trả lại · In phiếu nhập kho | ❌ **không có module kho** |
| Nhóm Hóa đơn | Tạo hóa đơn điều chỉnh · Ký và phát hành · Theo dõi trạng thái | ❌ **không có module hóa đơn** |
