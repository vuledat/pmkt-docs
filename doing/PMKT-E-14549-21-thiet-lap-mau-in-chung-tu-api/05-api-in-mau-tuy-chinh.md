# 05 · `F03` — API In chứng từ bằng mẫu tùy chỉnh (UC02)

| | |
|---|---|
| Mã chức năng | `F03` |
| UC nguồn | `PMKT-U-14549_21-02` In chứng từ bằng mẫu tùy chỉnh |
| Endpoint phụ trách | `A8` (menu In) · `A9` (dựng bản in) |
| Quyết định gốc | `D3` (BE giải nghĩa, FE dựng trang) · `D9` (`HoSoDonViPort`) · `D14` (cộng gộp dòng) |
| Luật phủ | `R-TLMI-023`…`035` · `259`…`271` |

---

## §1. `A8` — Menu In của một chứng từ

```
GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu/{chungTuId}/menu-in
```

**Quyền:** `<MaChucNang của nghiệp vụ>.<provider.hanhDongIn()>` — **KHÔNG** gate `HTMauIn.*`, vì *không có quyền Thiết lập mẫu in nhưng có quyền In thì vẫn in được Mẫu tùy chỉnh* (`R-TLMI-033`).

### Response — `ApiResponse<MenuInResponse>`

```json
{
  "data": {
    "choPhepIn": false,
    "lyDoCam": "CHUA_GHI_SO",
    "muc": [
      { "loai": "CO_DINH",    "ma": "01-TT",  "ten": "Mẫu 01-TT" },
      { "loai": "CO_DINH",    "ma": "02-VT",  "ten": "Mẫu 02-VT" },
      { "loai": "DUONG_KE" },
      { "loai": "TUY_CHINH", "ma": "TUY_CHINH", "ten": "Mẫu tùy chỉnh" },
      { "loai": "THIET_LAP", "ma": "THIET_LAP", "ten": "Thiết lập mẫu in…", "hien": true }
    ]
  }
}
```

| Trường | Ý nghĩa | Luật |
|---|---|---|
| `choPhepIn` | `false` ⇒ FE **disable nút In**, **cả menu không mở được**, kể cả mục *Mẫu tùy chỉnh* | `R-TLMI-261` |
| `lyDoCam` | `CHUA_GHI_SO` · `DA_KHOA_SO` · `null` — FE dùng để chọn **đúng tooltip** | `R-TLMI-261` |
| `muc[]` | Thứ tự **cố định**: các mẫu cố định → **đường kẻ** → *Mẫu tùy chỉnh* → *Thiết lập mẫu in…* | `R-TLMI-023` |
| `muc[THIET_LAP].hien` | `false` khi thiếu `HTMauIn.View` ⇒ **ẩn hẳn**, không disable | `R-TLMI-032` |

**Nguyên văn tên hai mục** — dùng đúng cho **mọi nghiệp vụ**, không đổi theo loại chứng từ (`R-TLMI-024`):

> **Mẫu tùy chỉnh** · **Thiết lập mẫu in…**

**Nguyên văn tooltip khi `choPhepIn = false`** (BA chưa cấp mã `MSG_` — quyết định **C14**, chỉ có key i18n):

| `lyDoCam` | Tooltip |
|---|---|
| `CHUA_GHI_SO` | *"Đơn vị không cho phép in chứng từ chưa ghi sổ"* |
| `DA_KHOA_SO` | *"Đơn vị không cho phép in chứng từ đã khóa sổ"* |

Các mẫu cố định (`loai = CO_DINH`) lấy từ `provider.mauCoDinh(chungTuId)` — mẫu jrxml sẵn có của module chủ; `mau_in` chỉ **trộn** vào menu, **không đụng** (`R-TLMI-013`).

> ⚠ Quy tắc *"đã khóa sổ"* **chỉ tác động nút In của chứng từ** — **không** tác động báo cáo và **không** tác động Xuất Excel (`R-TLMI-261` Ghi chú). Đừng đem `choPhepIn` sang chỗ khác.
>
> ⚠ Form **thêm mới** không có nút In; menu In chỉ có ở form **sửa** và form **xem chi tiết** (`R-TLMI-025`) — kiểm ở FE, BE chỉ cần `chungTuId` tồn tại.

---

## §2. `A9` — Dựng bản in bằng mẫu tùy chỉnh

```
GET /api/mau-in/{maLoai}/{maNghiepVu}/chung-tu/{chungTuId}/ban-in
```

**Quyền:** `<MaChucNang>.<provider.hanhDongIn()>` — thiếu ⇒ `403` + `MSG_COMMON_003` *"Bạn không có quyền thực hiện chức năng {tên chức năng}…"* (BR25.2, quyết định **C15**; **không** dùng `MSG_PMKT-E-14549_21_002` vì mã đó dành riêng cho quyền *Thiết lập mẫu in*).

### Response — `ApiResponse<BanInResponse>`

```json
{
  "data": {
    "nguon": "MAU_CHUAN",
    "mauHieuLuc": { "schemaVersion": 2, "trang": { "kho": "A4", "huong": "NGANG", "...": "ĐÃ hợp nhất" }, "khoi": [ ] },
    "duLieu": {
      "donVi":   { "tenDonVi": "…", "diaChi": "…", "mst": "…", "soDienThoai": null, "email": null,
                   "taiKhoanNganHang": "…", "coLogo": true },
      "truong":  { "soChungTu": "PT0001", "ngayChungTu": "2026-09-19", "soTienBangChu": "…" },
      "bang":    { "dinhKhoan": [ { "dienGiai": "…", "tkNo": "111", "soTien": 1000000 } ] },
      "nguoiKy": { "GIAM_DOC": { "tieuDe": "GIÁM ĐỐC", "ten": "Nguyễn Văn A" } },
      "inTenNguoiKy": true
    },
    "huongGiayThucTe": "NGANG",
    "coAnhNen": false,
    "canhBao": [ { "ma": "MSG_PMKT-E-14549_21_103",
                   "noiDung": "Đơn vị chưa thiết lập mẫu tùy chỉnh cho nghiệp vụ này, đang in theo mẫu chuẩn hệ thống" } ]
  }
}
```

| Trường | Ý nghĩa | Luật |
|---|---|---|
| `nguon` | `TUY_CHINH` khi có bản ghi, `MAU_CHUAN` khi không | `R-TLMI-007` · `259` · `260` |
| `mauHieuLuc` | Mẫu **đã hợp nhất thiết lập chung tại LÚC IN**, chỉ còn **khối `hien = true`**, đúng thứ tự `khoi[]` | `R-TLMI-038` · `262` · `264` |
| `duLieu.donVi` | Hồ sơ của **chi nhánh ghi trên chứng từ**; trường rỗng ⇒ `null` ⇒ FE **bỏ qua dòng** | `R-TLMI-078` · `079` · `267` |
| `duLieu.bang` | Dòng **đã cộng gộp** nếu thuộc diện (D14) | `R-TLMI-119` · `266`(c) |
| `duLieu.nguoiKy` | Tiêu đề + tên của 5 chức danh, đọc từ `HoSoDonViPort` | `R-TLMI-186` · `188` · `199` |
| `duLieu.inTenNguoiKy` | Cờ chung — `false` ⇒ FE không in dòng tên | `R-TLMI-196` |
| `huongGiayThucTe` | Kết quả `GiaiHuongGiay` — `DOC`/`NGANG`, không bao giờ `TU_DONG` | `R-TLMI-058` · `059` · `060` |
| `canhBao[]` | `MSG_…_103` **một lần** mỗi lần mở màn xem trước bản in (quyết định **C22**) | `R-TLMI-260` |

### Luồng — xem [00 §6.2](00-ke-hoach-tong.md)

### Bảng mã lỗi

| Tình huống | HTTP | Mã message | Luật |
|---|---|---|---|
| Thiếu quyền In | `403` | `MSG_COMMON_003` (tạm — C15) | `R-TLMI-034` |
| Nghiệp vụ chưa có provider | `404` | — | — |
| Chứng từ không tồn tại / khác tenant | `404` | — | BR28 |
| Bị cấm in (chưa ghi sổ / đã khoá sổ) | `409` | — (key i18n tooltip, C14) | `R-TLMI-261` |
| Lỗi hệ thống khi dựng bản in | `500` | `MSG_PMKT-E-14549_21_003` — FE **KHÔNG mở** màn xem trước | `R-TLMI-270` |

**Không báo lỗi** khi chưa có mẫu tùy chỉnh: vẫn mở màn xem trước bình thường, chỉ kèm `MSG_…_103` (`R-TLMI-260`).

### Bất biến của endpoint này

> **`A9` là endpoint CHỈ ĐỌC.** Không `INSERT`, không `UPDATE`, không ghi lịch sử, không chạm `prn_mau_in_tuy_chinh` (`R-TLMI-271`). Đánh dấu `@Transactional(readOnly = true)` và có test khẳng định `phien_ban` + `ngay_cap_nhat` không đổi sau khi gọi.

---

## §3. Ranh giới BE / FE khi dựng bản in (`D3`)

| Việc | Chủ | Luật | Ghi chú |
|---|---|---|---|
| Chọn khối nào được in, thứ tự nào | **BE** | `R-TLMI-262` · `207` · `208` | Lọc `hien=true`, giữ thứ tự mảng |
| Giải `huong = TU_DONG` | **BE** | `R-TLMI-058` · `059` | [07 §4](07-chuan-hoa-kiem-tra-va-thuat-toan.md) |
| Hợp nhất ô kế thừa | **BE** | `R-TLMI-038` · `264` | Đọc lại thiết lập chung **tại lúc in** |
| Cộng gộp dòng bảng | **BE** | `R-TLMI-119` · `266` | [07 §5](07-chuan-hoa-kiem-tra-va-thuat-toan.md) |
| Tra hồ sơ đơn vị theo chi nhánh chứng từ | **BE** | `R-TLMI-078` · `267` | `HoSoDonViPort` |
| Điền giá trị từng trường, đọc *Số tiền bằng chữ* | **BE** | `R-TLMI-144` · `165` | `cell/core/shared/text/SoTienBangChu.java` |
| Bỏ qua dòng đầu trang có hồ sơ trống | **BE** | `R-TLMI-079` | Trả `null` cho FE |
| Vẽ hình nền dưới cùng | FE | `R-TLMI-075` · `263` | |
| Đo chữ, ngắt trang, lặp tiêu đề cột | FE | `R-TLMI-099` · `265` | BE chỉ trả cờ `lapTieuDeMoiTrang` |
| Ô gộp chiếm đúng số dòng/cột; ô cùng hàng cao bằng nhau | FE | `R-TLMI-180` · `181` | BE trả `gopDong`/`gopCot` |
| Chia đều ô ký, tối thiểu 4 cm, tự xuống hàng | FE | `R-TLMI-194` · `195` | BE trả danh sách ô ký đang bật |
| Cả khối Chữ ký sang trang mới khi thiếu chỗ | FE | `R-TLMI-200` | |
| Mở màn xem trước có nút In / Xuất file / Sửa mẫu | FE | `R-TLMI-268` · `269` | |

> ⚠ 7 luật ở nhóm FE được `02-rules.md` gán tầng `BE`. Đây là **lệch có chủ ý** — §12 `Q3` của [00](00-ke-hoach-tong.md).

---

## §4. Kiểm thử

| Test | Input → kỳ vọng | Luật |
|---|---|---|
| `R_TLMI_259_dungBanInTheoMauCuaNghiepVuChungTuDangMo` | Chứng từ có `maNghiepVu = X` → dùng mẫu của `X`, không phải của `Y` | `R-TLMI-259` |
| `R_TLMI_260_chuaCoMauThiInMauChuanVaBaoMotLan` | Không có bản ghi → `nguon=MAU_CHUAN` + đúng **một** cảnh báo `MSG_…_103`, **không** lỗi | `R-TLMI-260` |
| `R_TLMI_261_camInThiTraChoPhepInFalse` | `quyTacIn.choInChuaGhiSo=false` + chứng từ chưa ghi sổ → `A8` trả `choPhepIn=false`, `lyDoCam=CHUA_GHI_SO`; `A9` trả `409` | `R-TLMI-261` |
| `R_TLMI_262_chiDungKhoiDangBatTheoThuTuBoCuc` | Khối thứ 2 `hien=false` → `mauHieuLuc.khoi` không chứa khối đó, thứ tự các khối còn lại giữ nguyên | `R-TLMI-262` · `208` |
| `R_TLMI_264_oTheoChungLayGiaTriLucIn` | Mẫu `trang.kho` vắng; thiết lập chung `A5` → `mauHieuLuc.trang.kho = "A5"`; đổi thành `A3` rồi gọi lại → `A3` | `R-TLMI-264` · `038` |
| `R_TLMI_266_apBaQuyTacInCuaThietLapChung` | 3 cờ bật/tắt → đúng hành vi (a)(b)(c) | `R-TLMI-266` |
| `R_TLMI_267_docHoSoTheoChiNhanhGhiTrenChungTu` | Chứng từ chi nhánh B, phiên làm việc chi nhánh A → gọi `theoChiNhanh(B)` | `R-TLMI-267` |
| `R_TLMI_271_inKhongDoiDuLieu` | Gọi `A9` → `phien_ban` và `ngay_cap_nhat` của bản ghi không đổi | `R-TLMI-271` |
| `R_TLMI_033_khongQuyenThietLapVanInDuocMauTuyChinh` | Có `<ChucNang>.Print`, **không** có `HTMauIn.View` → `A8`/`A9` `200`; `muc[THIET_LAP].hien=false` | `R-TLMI-033` · `032` |
| `R_TLMI_023_thuTuMenuIn` | `muc[]` đúng thứ tự: cố định → đường kẻ → Mẫu tùy chỉnh → Thiết lập mẫu in… | `R-TLMI-023` |
| `R_TLMI_024_tenHaiMucGiongNhauMoiNghiepVu` | Hai provider khác nhau → cùng chuỗi *"Mẫu tùy chỉnh"* và *"Thiết lập mẫu in…"* | `R-TLMI-024` |
| `R_TLMI_270_loiHeThongThiKhongMoManXemTruoc` | `provider.duLieuIn` ném lỗi → `500` `MSG_…_003`, response **không** có `mauHieuLuc` | `R-TLMI-270` |

## §5. BR đã áp dụng

| BR | Bước |
|---|---|
| BR25 (quyền) | `A8`/`A9` gate bằng quyền **In của nghiệp vụ**, không phải `HTMauIn.*` (`R-TLMI-033`) |
| BR26 (thông báo) | `MSG_…_103` là **Info**, hiện một lần trên màn xem trước; `MSG_…_003` là Error |
| BR28 (multi-tenant) | Chứng từ khác tenant ⇒ `404`, không lộ tồn tại |
| BR50.7 (Phase 2) | `HoSoDonViPort.theoChiNhanh(chungTu.chiNhanhId)` |
| BR51.5 (Phase 2) | Ba quy tắc in chứng từ; cộng gộp giới hạn 3 loại chứng từ |
