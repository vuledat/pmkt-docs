# `ChungTuTemplate` — kế hoạch tách `thucThi` thành 5 luồng theo hành động

> **v2 — PR1 + PR2 ĐÃ TRIỂN KHAI** (chưa commit). Tình trạng và các điểm lệch so với kế hoạch: **§12**.
> PR0 (nợ entity/V341) và PR3 (đặc tả) CHƯA làm.
> `cell-app` · package `vn.dopai.pmkt.cell.accounting_core.chung_tu` · Cập nhật: 2026-08-05.
>
> ⚠️ **Có 3 điều chỉnh nghiệp vụ được yêu cầu mà bằng chứng trong repo nói ngược lại** — xem §7.1,
> §7.2, §7.3. Không tự ý làm theo bên nào; cần chủ dự án chốt.
>
> ⛔ **Chặn cứng**: `:cell-app:compileTestJava` đang FAIL 28 lỗi ⇒ không test nào chạy được ⇒ không
> chứng minh được "không hồi quy". Xem §9 PR0.

---

## 1. Mục tiêu

Biến mỗi hành động chứng từ (TAO / SUA / XOA / GHI_SO / BO_GHI_SO) thành **một method đọc được từ
trên xuống**, thay cho một chuỗi 13 lời gọi dùng chung điều khiển bằng cờ rải rác.

Không đổi: điểm vào duy nhất `thucThi`, `@Transactional`, các bước chạm sổ cái vẫn `private`
(lớp con không đảo được thứ tự, không bỏ được bước).

## 2. Hiện trạng — đánh giá lại

### 2.1 Năm hành động ĐÃ tách lớp từ trước

| Hành động | Lớp | Số override |
|---|---|---|
| TAO | `TaoChungTuBanHang` | 3 |
| SUA | `SuaChungTuBanHang` | 4 |
| XOA | `XoaChungTuBanHang` | 9 |
| GHI_SO | `GhiSoChungTuBanHang` | 12 |
| BO_GHI_SO | `BoGhiSoChungTuBanHang` | 9 |
| (chung TAO+SUA) | `LuuChungTuBanHangTemplate` | 10 |

Vậy **business logic không bị dồn vào một method**. Cái `thucThi` đang gánh là **trình tự**, và điểm
đau thật nằm ở chỗ khác: *"hành động" không phải là một thực thể trong code*.

### 2.2 Hành động bị mã hoá thành cờ, rải 4 chỗ

| Nơi | Điều kiện | Ý nghĩa ngầm |
|---|---|---|
| `ChungTuTemplate.java:210` | `if (ctx.chungTuId() == null) return;` | "bỏ khoá khi TAO" |
| `ChungTuTemplate.java:227` | `if (!ctx.hanhDong().coHoanTac())` | "chỉ SUA/XOA/BO_GHI_SO mới gỡ" |
| `ChungTuTemplate.java:264` | `if (coSinhButToan() && !dinhKhoan().isEmpty())` | "có gì để ghi không" |
| `ChungTuTemplate.java:275` | `if (!ctx.hanhDong().ghiMoi()) return;` | "XOA/BO_GHI_SO không kiểm kỳ" |

Muốn trả lời "bấm *Bỏ ghi sổ* thì chạy đúng những bước nào" phải đọc 3 file và tự chạy 7 điều kiện
trong đầu. Thêm hành động thứ 6 (DUYET / BO_DUYET / HUY — `BaseChungTuEntity.java:155-190` và V341
đã có sẵn 5 trạng thái) là phải thêm cờ và rà lại toàn bộ các `if` đọc nó.

Bằng chứng cờ đặt sai chỗ: javadoc của `HanhDongChungTu.coHoanTac()` (`:34-42`) và `ghiMoi()`
(`:47-54`) phải mô tả **"bước 5"**, **"bước 9"** của lớp cha. Enum mà phải biết số thứ tự bước của
template là dấu hiệu hành vi bị đẩy ngược lên dữ liệu.

### 2.3 Ba khiếm khuyết phát hiện khi soát

| # | Khiếm khuyết | Bằng chứng |
|---|---|---|
| K1 | `kiemTraDaGhiNhanChungTu` là **code chết** — javadoc `:112-114` hứa template kiểm sau `saveEntity`, thực tế không nơi nào gọi. Quên `ghiNhanChungTu` ⇒ đẩy `GhiSoRequest` với `chungTuId = null` xuống kernel, và `kiemTraKyMo(null, …)` rơi vào nhánh **fail-open** | `ChungTuTemplate.java:245` (grep toàn `src` ra đúng 1 dòng khai báo); `KyKeToanChecker.java:73-74`. Lời gọi bị xoá ở commit `fd3fbda`, bản `bcaf367` còn có |
| K2 | Tên bước lệch tài liệu: javadoc gọi bước 5 là `hoanTacTacDongCu`, code tên `boGhiSo`; và `boGhiSo` còn làm cả hoàn tồn kho. Comment `:94` ghi *"Chỉ được thực thi khi ctx đang đánh dấu Bỏ ghi sổ"* — sai, nó chạy cho cả SUA và XOA | `ChungTuTemplate.java:31` vs `:226-242` |
| K3 | `ghiSo` và `kyKeToan` để `protected final` ⇒ lớp con gọi thẳng kernel được, không test/ArchUnit nào chặn. Rào "bước chạm sổ cái là private" chỉ chặn được một nửa | `ChungTuTemplate.java:62-65` |

## 3. Quy tắc nghiệp vụ — đối chiếu đặc tả

Năm điều chỉnh do chủ dự án chốt, đối chiếu với đặc tả:

| # | Điều chỉnh | Đặc tả | Nguồn |
|---|---|---|---|
| A | "Lưu" (tạo mới) **không** ghi sổ cái; chỉ *Ghi sổ* / *Lưu và ghi sổ* mới sinh bút toán | ✅ **ĐÚNG** | `SCR_CTBH_ThemMoi.md:775` (BR13 §1 "Không phát sinh bút toán, không cập nhật Sổ cái"); `UC_CTBH_ThemMoi.md:25` vs `:32` |
| B | Sửa: đã ghi sổ thì không sửa; phải Bỏ ghi sổ trước | ✅ **ĐÚNG** | `UC_CTBH_ChinhSua.md:93`, `:86`, `:8` |
| C | Xoá: đã ghi sổ thì không xoá | ✅ **ĐÚNG** — và còn **một vế nữa chưa nêu**: đã dùng ở nghiệp vụ khác thì không xoá *kể cả khi đã bỏ ghi sổ* | `UC_CTBH_Xoa.md:111`, `:82`, `:103` |
| D | Ghi sổ: kiểm tra kỳ kế toán | ✅ ĐÚNG theo BR17 dùng chung — ⚠️ nhưng **kernel đã tự kiểm rồi**, xem §7.2 | `business_rules.md:510`; `GhiSoService.java:61` |
| E | Bỏ ghi sổ: xoá cứng bản ghi trong DB + kiểm kỳ | ✅ ĐÚNG — **"xoá cứng" = xoá dòng SỔ CÁI `acc_so_cai`**, KHÔNG phải xoá bản ghi chứng từ (chứng từ giữ nguyên, chỉ đổi trạng thái). ⚠️ Phần kiểm kỳ: kernel đã kiểm, và kiểm **chặt hơn** — xem §7.3 | `UC_CTBH_BoGhiSo.md:65`, `:38`, `:54`; `TaiLieuMappingSoCai.md:1549`; `V56__acc_so_cai_unpost_physical_delete.sql` |

> ⚠️ **Bẫy đọc tài liệu**: tồn tại HAI hệ đánh số BR khác nghĩa nhau. `BR17` của Common là *"Kiểm tra
> kỳ kế toán"* (`business_rules.md:497`); `BR17` của epic CTBH là *"Theo dõi số lượng đã xuất"*
> (`SCR_CTBH_ThemMoi.md`). Comment trong code (`LuuChungTuBanHangTemplate.java:79` "BR17 §4") đang
> dùng hệ RIÊNG.

> ⚠️ **Khoảng trống đặc tả**: toàn bộ epic PMKT-E-06194 **không có một chữ nào** về "kỳ kế toán" /
> "khoá sổ" (grep 0 kết quả trên cả `..` lẫn `../../pmkt-docs/ba`); `UC_CTBH_BoGhiSo.md:43-50` chỉ
> liệt kê 4 ngoại lệ, không có kỳ khoá. Ràng buộc kỳ hiện chỉ tồn tại ở BR17 Common. Nên bổ sung
> 1 dòng ngoại lệ + 1 messageId vào epic (§9 PR4).

> ⚠️ Epic CTBH có **2 bản sao đã lệch nhau** (`docs/PMKT-E-06194_ChungTuBanHang` và
> `../../pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang`, khác ở 4 file, số dòng lệch 1). Sửa một nơi là tạo hai
> nguồn sự thật.

## 4. Thiết kế mục tiêu

### 4.1 Điểm vào

```java
@Transactional
public R thucThi(C lenh) {
    ChungTuContext<C> ctx = new ChungTuContext<>(lenh, hanhDong());
    kiemTraDauVao(ctx);
    kiemTraQuyen(ctx);
    chuanBiChungTu(ctx);

    // switch EXPRESSION, KHÔNG có default: thêm hành động mới mà quên viết luồng là LỖI BIÊN DỊCH.
    // Dạng câu lệnh (statement) KHÔNG được javac 21 cưỡng chế vét cạn — đã đo, xem §6.3.
    return switch (ctx.hanhDong()) {
        case TAO       -> { luongTao(ctx);     yield taoKetQua(ctx); }
        case SUA       -> { luongSua(ctx);     yield taoKetQua(ctx); }
        case XOA       -> { luongXoa(ctx);     yield taoKetQua(ctx); }
        case GHI_SO    -> { luongGhiSo(ctx);   yield taoKetQua(ctx); }
        case BO_GHI_SO -> { luongBoGhiSo(ctx); yield taoKetQua(ctx); }
    };
}
```

> ⛔ Tuyệt đối **không** thêm `default -> throw`: `default` làm switch expression luôn "vét cạn" và
> giết mất chính cái kiểm tra biên dịch này.

### 4.2 Năm luồng

```java
/** TẠO MỚI — nút "Lưu" KHÔNG chạm sổ cái; nút "Lưu và ghi sổ" mới đi tiếp qua phanGhiSo. */
private void luongTao(ChungTuContext<C> ctx) {
    kiemTraNghiepVu(ctx);
    truocKhiLuu(ctx);
    luuChungTu(ctx);                                   // + chốt định danh (K1)
    sauKhiLuu(ctx);
    if (coGhiSoNgay(ctx)) phanGhiSo(ctx);
    else                  kiemTraKyKeToan(ctx);        // BR17.1 — nháp cũng bị chặn nếu kỳ đã khoá
    ghiNhatKyKiemToan(ctx);
    dangKyThongBaoSauCommit(ctx);
}

/** SỬA — chỉ sửa được chứng từ CHƯA ghi sổ ⇒ không tồn tại dòng sổ cái nào để gỡ. */
private void luongSua(ChungTuContext<C> ctx) {
    doiHoiDinhDanh(ctx);
    khoaChungTu(ctx);
    kiemTraNghiepVu(ctx);        // lớp con chặn "đã ghi sổ" — giữ messageId riêng (§6.5)
    doiSoatVoiSoCai(ctx);        // lưới an toàn: cờ nói chưa ghi sổ mà acc_so_cai còn dòng ⇒ nổ
    truocKhiLuu(ctx);
    luuChungTu(ctx);
    sauKhiLuu(ctx);
    if (coGhiSoNgay(ctx)) phanGhiSo(ctx);
    else                  kiemTraKyKeToan(ctx);
    ghiNhatKyKiemToan(ctx);
    dangKyThongBaoSauCommit(ctx);
}

/** XOÁ MỀM — chỉ xoá được chứng từ CHƯA ghi sổ và chưa bị nghiệp vụ khác dùng. */
private void luongXoa(ChungTuContext<C> ctx) {
    doiHoiDinhDanh(ctx);
    khoaChungTu(ctx);
    kiemTraNghiepVu(ctx);
    doiSoatVoiSoCai(ctx);
    truocKhiLuu(ctx);
    luuChungTu(ctx);             // đánh dấu da_xoa cho header + TOÀN BỘ dòng chi tiết
    sauKhiLuu(ctx);
    ghiNhatKyKiemToan(ctx);
    dangKyThongBaoSauCommit(ctx);
    // KHÔNG chạm sổ cái, KHÔNG kiểm kỳ: không có bút toán nào tồn tại để gỡ.
}

/** GHI SỔ — chứng từ đã lưu, việc duy nhất là sinh bút toán và chuyển trạng thái. */
private void luongGhiSo(ChungTuContext<C> ctx) {
    doiHoiDinhDanh(ctx);
    khoaChungTu(ctx);
    kiemTraNghiepVu(ctx);        // lớp con chặn "đã ghi sổ rồi"
    truocKhiLuu(ctx);
    luuChungTu(ctx);
    sauKhiLuu(ctx);              // dựng định khoản
    phanGhiSo(ctx);              // kernel tự kiểm kỳ; nhánh 0 bút toán thì template kiểm
    ghiNhatKyKiemToan(ctx);
    dangKyThongBaoSauCommit(ctx);
}

/** BỎ GHI SỔ — XOÁ VẬT LÝ dòng sổ cái (V56), rồi trả trạng thái về Chưa ghi sổ. */
private void luongBoGhiSo(ChungTuContext<C> ctx) {
    doiHoiDinhDanh(ctx);
    khoaChungTu(ctx);
    kiemTraNghiepVu(ctx);        // chứng từ liên quan (PXK/HĐ/phiếu thu) phải còn Chưa ghi sổ
    xoaButToanSoCai(ctx);        // kernel kiểm kỳ theo TỪNG ngày của dòng cũ rồi DELETE
    hoanTacTonKho(ctx);
    truocKhiLuu(ctx);
    luuChungTu(ctx);             // đổi trạng thái về Chưa ghi sổ
    sauKhiLuu(ctx);
    ghiNhatKyKiemToan(ctx);
    dangKyThongBaoSauCommit(ctx);
}
```

### 4.3 Khối chạm sổ cái — viết ĐÚNG MỘT LẦN

```java
/**
 * Khối duy nhất trong file được phép chạm sổ cái. Ba luồng gọi nó (TAO/SUA khi "Lưu và ghi sổ",
 * và GHI_SO) — không chép ba bản, để mai sau thêm bước không vá được 2/3 chỗ.
 */
private void phanGhiSo(ChungTuContext<C> ctx) {
    if (coSinhButToan() && !ctx.dinhKhoan().isEmpty()) {
        ghiSoCai(ctx);           // kernel: tự khoá + TỰ kiểm kỳ + idempotent theo vân tay SHA-256
    } else {
        kiemTraKyKeToan(ctx);    // không đi qua kernel ⇒ template phải tự kiểm (chứng từ giá trị 0)
    }
    capNhatTonKho(ctx);
}
```

> Guard `!ctx.dinhKhoan().isEmpty()` là **bắt buộc giữ**: kernel từ chối danh sách rỗng bằng lỗi 400
> (`DinhKhoanValidator.java:57`). Bỏ guard ⇒ chứng từ bán hàng giá trị 0 bấm "Ghi sổ" ăn 400.

### 4.4 Hai bất biến được cưỡng chế lại

```java
/** Vá K1 — gọi ngay trong luuChungTu, cả 5 luồng. */
private void luuChungTu(ChungTuContext<C> ctx) {
    luuEntity(ctx);                                    // hook lớp con
    kiemTraDaGhiNhanChungTu(ctx);                      // hết là code chết
}

/** Các luồng chạy trên bản ghi đã tồn tại đều đòi định danh từ bước chuanBiChungTu. */
private void doiHoiDinhDanh(ChungTuContext<C> ctx) {
    if (ctx.chungTuId() == null) {
        throw new IllegalStateException(String.format(
                "%s: hành động %s chạy trên bản ghi đã có nhưng chưa biết chứng từ nào — "
                        + "chuanBiChungTu phải gọi ctx.ghiNhanChungTu(...)",
                getClass().getSimpleName(), ctx.hanhDong()));
    }
}
```

### 4.5 `doiSoatVoiSoCai` — lưới an toàn thay cho bước gỡ đã bỏ

Bỏ bước gỡ bút toán khỏi SUA/XOA là **hệ quả tất yếu** của quy tắc B/C, nhưng nó xoá mất đường dọn
`acc_so_cai` duy nhất của hệ thống (`SoCaiRepository.java:52-54` là lệnh DELETE **duy nhất** trong
toàn repo, chỉ gọi từ `GhiSoService.java:99`, chỉ gọi từ bước 5 của template). Thay thế bằng một
bước đối soát rẻ hơn và bắt lỗi sớm hơn:

```java
/**
 * Đối soát cờ trạng thái với SỔ CÁI — nguồn sự thật thật sự.
 *
 * <p>Chạy SAU kiemTraNghiepVu để lớp con còn kịp ném messageId riêng của mình cho ca thường gặp;
 * bước này chỉ nổ ở ca LỆCH: cờ nói "chưa ghi sổ" mà acc_so_cai vẫn còn dòng. Trước đây ca đó được
 * bước gỡ âm thầm dọn hộ; giờ nó phải lộ ra.
 */
private void doiSoatVoiSoCai(ChungTuContext<C> ctx) {
    if (!coSinhButToan()) return;
    if (ghiSo.daGhiSo(ctx.chungTuId())) {
        throw new IllegalStateException(String.format(
                "%s %s: trạng thái nói CHƯA ghi sổ nhưng sổ cái còn dòng — dữ liệu lệch, "
                        + "phải Bỏ ghi sổ trước", bangGoc(), ctx.soChungTu()));
    }
}
```

Chi phí: đúng một `SELECT` (`GhiSoApi.daGhiSo` → `soCai.timTatCa(id).isEmpty()`), **bằng đúng** chi
phí của bước gỡ cũ ở ca "chưa từng ghi sổ" (`GhiSoService.java:83-92` cũng chỉ SELECT rồi trả 0).

## 5. Bảng đổi tên

Template đang **pha trộn hai ngôn ngữ**: 8 hook tiếng Anh + 12 hook tiếng Việt, và
`ChungTuTemplate.java:88` đã có sẵn `TODO: Đặt lên tiếng Việt cho dễ hiểu`.

### 5.1 Hook `protected` — API với lớp con

| Cũ | Mới | Ý nghĩa |
|---|---|---|
| `validateInput` | `kiemTraDauVao` | Bean validation trên lệnh đầu vào |
| `checkPermission` | `kiemTraQuyen` | Quyền `<maChucNang>.<hành động>` |
| `loadData` | **`chuanBiChungTu`** | *Nạp* bản ghi đang có **hoặc dựng mới từ lệnh* — luồng TAO không nạp gì (`TaoChungTuBanHang.java:35-38`), nên "nạp dữ liệu" là tên sai |
| `validateBusiness` | `kiemTraNghiepVu` | Kiểm tra nghiệp vụ, ném messageId riêng của module |
| `beforeSave` | `truocKhiLuu` | Sinh số, tính tổng, chốt trạng thái |
| `saveEntity` | `luuEntity` | Ghi header + dòng chi tiết; PHẢI gọi `ghiNhanChungTu` |
| `afterSave` | `sauKhiLuu` | Dựng định khoản (cần id dòng chi tiết), cập nhật chứng từ liên quan |
| `buildResult` | **`taoKetQua`** | Không dùng `dungKetQua`: `dung` không dấu đọc được thành *dùng/dựng/đúng/dừng*, và repo đã dùng `dinhKhoan().dung(ct)` với nghĩa *dựng* |

Giữ nguyên: `bangGoc`, `maChucNang`, `maLoaiChungTu`, `hanhDong`, `dienGiaiChung`, `moTaAudit`,
`ghiNhatKy`, `guiThongBao`, `apDungTonKho`, `hoanTacTonKho`, `coSinhButToan`, `coAnhHuongTonKho`.

> ⛔ **KHÔNG đổi `maChucNang` / `maLoaiChungTu`** dù có ý định gom: hai tên này còn tồn tại ở
> `BaseCrudController.java:89`, `ChungTuBanHangController.java:76` và là tham số của
> `QuyenChecker.java:38`. Đổi ⇒ hai tên khác nhau cho cùng một khái niệm.

### 5.2 Bước `private` — nội bộ template

| Cũ | Mới | Ghi chú |
|---|---|---|
| `boGhiSo` | **`xoaButToanSoCai`** | Tên cũ trùng với **ba** thứ khác: `GhiSoApi.boGhiSo` (kernel), `BaseChungTuEntity.boGhiSo()` (đổi cờ), và hành động `BO_GHI_SO`. Tên mới nói đúng việc: xoá vật lý dòng sổ cái theo V56. **Phần hoàn tồn kho tách ra thành lời gọi riêng** |
| `generateJournal` | `ghiSoCai` | |
| `updateInventory` | **`capNhatTonKho`** | ⚠️ Không đặt `apTonKho`: đứng cạnh hook `apDungTonKho` (`:335`), hai tên cách nhau 3 ký tự ở hai tầng khác nhau |
| `writeAuditLog` | **`ghiNhatKyKiemToan`** | ⚠️ Không đặt `ghiAuditLog`: hook nó gọi là `ghiNhatKy`, lớp phụ trách là `NhatKyKiemToan` — 3 tên cho 1 khái niệm ở 3 mức Việt hoá |
| `publishNotification` | **`dangKyThongBaoSauCommit`** | ⛔ **KHÔNG đổi thành `guiThongBao`** — trùng **hoàn toàn tên + chữ ký** với hook `protected void guiThongBao(ChungTuContext<C>)` ở `:359` ⇒ `error: method guiThongBao(ChungTuContext) is already defined`. Tên mới cũng đúng việc hơn: bước này chỉ *đăng ký* `TransactionSynchronization`, không gửi gì |
| `khoaChungTu` | giữ | |

### 5.3 Bẫy khi đổi tên

1. **Tên hook nằm trong chuỗi thông báo lỗi** — 5 chỗ: `:233`, `:248`, `:336`, `:346`, `:380`.
   `Rename Method` của IDE **bỏ sót hết**. Test assert lại đúng các chuỗi đó (33 string literal).
   ⇒ Đổi tên xong sẽ **compile xanh mà test đỏ**.
2. **Không được `sed` toàn repo**: `beforeSave`/`afterSave` còn là hook của `AbstractCrudService.java:214/217`;
   `boGhiSo` xuất hiện 26 dòng nhưng chỉ 3 dòng thuộc method cần đổi.
3. Phạm vi thực tế: **8 hook + 6 bước private ≈ 110 dòng / 8 file**, trong đó 72% nằm ở
   `ChungTuTemplate.java` + `ChungTuTemplateTest.java`.

## 6. Ưu điểm khi chuyển đổi

### 6.1 Đọc một luồng là biết trọn trình tự

Hiện phải ghép 4 điều kiện rải ở `:227`, `:264`, `:275`, `:286` mới hình dung được một hành động
chạy những bước nào. Đọc `TaoChungTuBanHang` **không thể** biết nó có ghi sổ hay không.
Sau chuyển đổi: 5 method, mỗi method 8–11 dòng, lý do "vì sao luồng này không có bước X" nằm ngay
cạnh luồng chứ không phải là một `if` ở file khác.

### 6.2 Bỏ được hai cờ đặt sai chỗ

`HanhDongChungTu` còn đúng `hanhDongQuyen()`. Enum vẫn tồn tại vì 3 lý do độc lập: ánh xạ catalog
quyền đã seed (V82), giá trị `.name()` **đã nằm trong `aud_audit_log`**, và là biến chọn của switch.

### 6.3 Thêm hành động mới trở thành lỗi biên dịch

Đã kiểm chứng bằng `javac 21.0.6` (toolchain của repo, `build.gradle.kts:11-15`): switch **statement**
trên enum thiếu case ⇒ **biên dịch sạch, không cảnh báo**, kể cả `-Xlint:all`, và hằng thiếu rơi
thẳng qua switch. Áp vào đây: thêm `DUYET` mà quên case ⇒ `thucThi` chạy 3 bước đầu rồi
`return taoKetQua(ctx)` ⇒ **API trả HTTP 200 "duyệt thành công" mà không lưu, không audit, không ghi sổ**.
Switch **expression** không có `default` ⇒ `error: the switch expression does not cover all possible input values`.

Đây không phải rủi ro xa: `BaseChungTuEntity.java:155-190` đã có sẵn `duyet()`/`boDuyet()`, V341 đã
có 5 trạng thái `NHAP/CHO_DUYET/DA_DUYET/DA_GHI_SO/HUY`.

### 6.4 Xoá được ba bản chép của khối chạm sổ cái

`phanGhiSo` viết một lần, ba luồng gọi. Nguyên tắc: *mọi thứ chạm sổ cái chỉ được viết MỘT lần
trong file*. Không có nó, thiết kế mới tự mâu thuẫn với lời hứa ở `ChungTuTemplate.java:41-44`
("Không lớp con nào đảo được thứ tự hay bỏ bước") — chặn được lớp con lệch, nhưng mở cửa cho chính
lớp cha lệch với chính nó.

### 6.5 Quy tắc "chỉ thao tác đúng trạng thái" có chốt chặn ở base

Hiện quy tắc bị chép tay ở 4 nơi (`SuaChungTuBanHang.java:50`, `XoaChungTuBanHang.java:68`,
`GhiSoChungTuBanHang.java:71`, `BoGhiSoChungTuBanHang.java:71`) — module thứ hai quên một chỗ là
không ai biết. `doiSoatVoiSoCai` ở base đối soát với **sổ cái** (nguồn sự thật) thay vì với cờ.

> **Giữ nguyên guard nghiệp vụ ở lớp con.** Bốn luồng đang ném **bốn messageId khác nhau** —
> `MSG_PMKT-E-06194_013/016/021/023` (`MaLoiBanHang.java:25-31`), và javadoc gọi đây là *"HỢP ĐỒNG
> với client"*. `ChungTuTemplate` nằm ở `accounting_core`, không biết `MaLoiBanHang`, nên nếu base
> chặn trước thì FE mất khả năng hiển thị đúng câu cho từng thao tác. Vì vậy `doiSoatVoiSoCai` chạy
> **sau** `kiemTraNghiepVu` và ném lỗi **kỹ thuật**, không thay thế lỗi nghiệp vụ.

### 6.6 Vá được K1, K2, K3 trong cùng đợt

`kiemTraDaGhiNhanChungTu` sống lại (K1); `boGhiSo` → `xoaButToanSoCai` + tách hoàn tồn kho (K2);
hạ `ghiSo`/`kyKeToan` xuống `private final` (K3).

### 6.7 Những gì KHÔNG đổi (và đó là điều tốt)

- Một `@Transactional` duy nhất, `thucThi` **không** `final` (proxy CGLIB), toàn kernel
  `Propagation.MANDATORY` ⇒ không tồn tại đường ghi sổ cái commit độc lập với chứng từ.
- Audit **trong** transaction, thông báo **sau** commit và nuốt lỗi.
- Hàng loạt vẫn "lỗi từng phần": `ChungTuBanHangHangLoatService` cố ý không `@Transactional`
  (`javadoc :22-26`) ⇒ mỗi chứng từ một transaction. Thiết kế mới **không đổi** điều này —
  `ghiNhatKyKiemToan`/`dangKyThongBaoSauCommit` vẫn được gọi *bên trong* `thucThi`.

## 7. Nhược điểm & rủi ro khi chuyển đổi

### 7.1 ⚠️ Yêu cầu "luongTao/luongSua chưa có ghi sổ cái" — nếu hiểu là bỏ luôn kiểm kỳ thì trái BR17.1

| | |
|---|---|
| **Đặc tả** | `business_rules.md:508` — *"Lưu (Thêm/Sửa) \| Ngày hạch toán thuộc kỳ đóng (đã khóa) \| **Chặn, không cho phép lưu**"* — mức chặn cứng, không phải cảnh báo |
| **Hiện tại** | TAO/SUA có `ghiMoi()=true` ⇒ `ChungTuTemplate.java:275-278` gọi `kiemTraKyMo` **kể cả khi `dinhKhoan` rỗng`. `LuuChungTuBanHangTemplate.java:110-112` ghi rõ chủ ý. Test `tao_moi_khong_sinh_but_toan_van_kiem_tra_ky_ke_toan` khoá hành vi |
| **Nếu bỏ** | Kỳ 07/2026 đã khoá. Người dùng tạo chứng từ `ngayHachToan = 2026-07-15`, bấm **Lưu** ⇒ lưu thành công vào kỳ đã khoá, và **sẽ không bao giờ ghi sổ được** |
| **Xử lý trong bản thiết kế** | Đã **GIỮ** `kiemTraKyKeToan` ở nhánh `else` của `luongTao`/`luongSua` (§4.2) |
| **Cần chốt** | Nút "Lưu" thuần có phải chặn kỳ đã khoá không? Nếu chủ dự án quyết **bỏ**, phải sửa kèm `business_rules.md:508` — không để code và đặc tả nói ngược nhau |

> Lo ngại "chặn muộn thì tiêu mất số chứng từ" là **không có cơ sở**: bộ đếm tăng bằng
> `SELECT … FOR UPDATE` trong cùng transaction, rollback thì số rollback theo
> (`ChungTuTemplate.java:179-181`).

### 7.2 ⚠️ Yêu cầu "luongGhiSo: check trong kỳ" — kernel đã làm, thêm bước nữa là kiểm hai lần

`GhiSoService.java:61` — `kyKeToan.kiemTraKyMo(request.ngayHachToan(), request.maLoaiChungTu())`
nằm **bên trong** `ghiSo()`, chạy sau khi khoá chứng từ và trước khi đọc trạng thái sổ cái.

⇒ **Yêu cầu của anh đã được đáp ứng**, nhưng bởi kernel chứ không phải bằng một bước mới ở template.
Thêm `kiemTraKyKeToan` ngay trước `ghiSoCai` là:
- thừa 1 round-trip DB (`KyKeToanChecker` chạy native query, không cache);
- hai lần đọc **không nguyên tử** ở READ COMMITTED;
- và nếu đặt trước `luuChungTu` thì `ctx.ngayHachToan()` còn `null` ⇒ rơi vào nhánh **fail-open**
  `KyKeToanChecker.java:73-74` (`if (ngayHachToan == null) return null;`) — an toàn giả.

Bản thiết kế §4.3 giữ đúng một cổng kiểm cho mỗi thao tác: đi qua kernel thì kernel kiểm; không đi
qua kernel (chứng từ 0 bút toán) thì template kiểm.

### 7.3 ⚠️ Yêu cầu "luongBoGhiSo: check trong kỳ" — kernel kiểm CHẶT HƠN, thêm ở template có thể chặn nhầm

| | |
|---|---|
| **Kernel làm gì** | `GhiSoService.java:93-98` — `for (LocalDate ngay : ngayHachToanRieng(dong)) kyKeToan.kiemTraKyMo(ngay, maLoai);` — kiểm **TỪNG ngày hạch toán riêng biệt** của các dòng đang gỡ, mã loại **tra ngược từ chính sổ cái**. Test chốt: `GhiSoServiceTest.java:203-219` `containsExactly(NGAY, NGAY.plusDays(5))` |
| **Template kiểm được gì** | Đúng **một** ngày: `ctx.ngayHachToan()` của header, với `maLoaiChungTu()` là hằng |
| **Chặn nhầm** | Chứng từ có dòng 15/07 và 20/08, header ghi 20/08, kỳ khoá tới 31/07: pre-check theo 20/08 **PASS**, kernel mới bắt đúng dòng 15/07. Ngược lại header 15/07 mà dòng đều 20/08: pre-check **chặn nhầm** một thao tác gỡ hợp lệ |
| **Ngõ cụt mới** | Chứng từ giá trị 0 bấm "Lưu và ghi sổ" ⇒ cờ = *Đã ghi sổ* nhưng `acc_so_cai` rỗng (`LuuChungTuBanHangTemplate.java:85-87` đặt `DA_GHI_SO` **vô điều kiện**, `:264` bỏ qua ghi sổ khi định khoản rỗng). Kỳ đó khoá lại ⇒ pre-check chặn ⇒ **khoá chết vĩnh viễn**. Hôm nay ca này gỡ được vì kernel thoát sớm ở `:88-92` **trước khi** kiểm kỳ |
| **Ngược quyết định đã ghi thành văn** | `HanhDongChungTu.java:47-53` và `ChungTuTemplate.java:257-261` ghi rõ: *"kiểm thêm ở đây theo ngày của bản ghi cũ là chặn nhầm chính thao tác gỡ hợp lệ"*. Test `bo_ghi_so_chi_go_khong_kiem_ky_theo_ngay_cu` khoá bằng `assertThat(kyKeToan.ngayDaKiem).isEmpty()` |
| **Xử lý trong bản thiết kế** | **KHÔNG** thêm bước; để kernel kiểm. Nếu muốn thông điệp lỗi thân thiện hơn thì nâng cấp `PeriodLockedException` ở `@RestControllerAdvice`, đừng dựng cổng kiểm thứ hai yếu hơn |
| **Cần chốt** | Chấp nhận để kernel kiểm (khuyến nghị), hay vẫn muốn pre-check ở template và chấp nhận 2 ca chặn nhầm ở trên? |

### 7.4 Bỏ bước gỡ ở SUA/XOA — mất đường tự lành, phải bù bằng đối soát

`delete from acc_so_cai where chung_tu_id = ?` là đường xoá **duy nhất** của hệ thống. Sau thiết kế
mới nó chỉ còn ở `luongBoGhiSo`, mà `luongBoGhiSo` lại bị chặn nếu cờ nói "chưa ghi sổ".

Kịch bản kẹt: chứng từ có cờ `CHUA_GHI_SO` nhưng còn dòng `acc_so_cai` ⇒ BO_GHI_SO từ chối
("chưa ghi sổ"), SUA/XOA không còn gỡ ⇒ **bút toán mồ côi vĩnh viễn**, và hệ thống **không có bất kỳ
truy vấn đối chiếu hàng loạt nào** để phát hiện (`GhiSoApi.daGhiSo` chỉ hỏi từng chứng từ một).

Giảm nhẹ đã đưa vào thiết kế: `doiSoatVoiSoCai` (§4.5) bắt lệch **ngay ở cửa** thay vì để lệch trôi đi.

Còn thiếu, nên làm kèm: một truy vấn/màn quản trị tìm *chứng từ không ở trạng thái Đã ghi sổ (hoặc
đã xoá mềm) mà còn dòng `acc_so_cai`*.

> ✅ Về mặt thiết kế lưu trữ, chiều lệch này **không thể sinh ra từ code hiện tại**: không có bảng/cột
> nào lưu bút toán của chứng từ chưa ghi sổ, `acc_so_cai` chỉ ghi qua `GhiSoApi` trong đúng
> transaction của chứng từ. Rủi ro nằm ở **dữ liệu cũ / migration / bug tương lai**.
>
> ⚠️ Chiều lệch NGƯỢC LẠI thì **có thật ngay hôm nay**: cờ *Đã ghi sổ* mà sổ cái rỗng (§7.3).

### 7.5 `khoaChungTu → chan…` chỉ an toàn về hình thức

`chuanBiChungTu` đọc entity **trước** khi lấy khoá, và không chỗ nào đọc lại sau khoá.

Cửa sổ race: T2 chạy `SuaChungTuBanHang.loadData` lúc t0, đọc `CHUA_GHI_SO` vào persistence context;
`khoaChungTu` chặn vì T1 (GHI_SO cùng chứng từ) đang giữ khoá; T1 commit (cờ → `DA_GHI_SO`, sổ cái có
dòng); T2 được cấp khoá, `chanNeuDaGhiSo` đọc `ct.daGhiSo()` — **so sánh trường trong bộ nhớ**
(`ChungTuBanHang.java:321-322`), vẫn thấy `CHUA_GHI_SO` ⇒ đi tiếp.

Thứ thật sự chặn là `@Version` lúc flush — tức **hậu kiểm**, và trả sai mã lỗi (`STALE_DATA` thay vì
"đã ghi sổ").

Xử lý: `doiSoatVoiSoCai` (§4.5) hỏi thẳng sổ cái nên **miễn nhiễm** với ảnh chụp cũ. Nếu muốn guard
theo cờ cũng đúng thì phải `em.refresh(ct)` ngay sau `khoaChungTu`.

### 7.6 Bề mặt API cho lớp con **không** thu hẹp

Lớp cha phình thêm ~40 lời gọi trong một file đã 383 dòng, trong khi vẫn 20 hook (+1 `coGhiSoNgay`),
mỗi lớp con chỉ dùng 3–12 cái. 8/20 hook hiện **chưa có lớp production nào override**
(`guiThongBao`, `ghiNhatKy`, `apDungTonKho`, `hoanTacTonKho`, `coSinhButToan`, `coAnhHuongTonKho`,
`validateInput`; `checkPermission` chỉ 1 lần).

### 7.7 Toàn bộ hành vi phụ thuộc một giá trị: `hanhDong()` của lớp con

Lớp con khai nhầm (copy `GhiSoChungTuBanHang` để làm BoGhiSo mà quên đổi) ⇒ **chạy nhầm cả luồng**.
Hôm nay khai nhầm chỉ làm sai quyền và audit. Không có gì chặn.

### 7.8 Quy tắc riêng của một epic bị chôn vào base dùng chung

`accounting_core.chung_tu` tự khai là base cho **mọi** chứng từ kế toán. Quy tắc "chỉ sửa được chứng
từ chưa ghi sổ" là của epic CTBH. Loại chứng từ sau muốn khác (phiếu nhập kho luôn ghi sổ ngay,
không có nút "Lưu" nháp) phải mở lại base.

Cách giảm nhẹ: giữ guard nghiệp vụ ở `kiemTraNghiepVu` của lớp con (§6.5); base chỉ có
`doiSoatVoiSoCai` — thứ đúng cho mọi loại chứng từ.

### 7.9 Vùng bị tác động mạnh nhất đang **trần trụi**

`grep` toàn `../../cell-app/src/test`: **0 test** chạm `TaoChungTuBanHang` / `SuaChungTuBanHang` /
`XoaChungTuBanHang` / `GhiSoChungTuBanHang` / `BoGhiSoChungTuBanHang` / `ChungTuBanHangCrudService`.
Năm lớp con sẽ bị đổi tên 13 method mà **không test nào bắt lỗi ngữ nghĩa** — chỉ có `javac` bắt
`@Override`.

### 7.10 Điểm vỡ khi có loại chứng từ thứ hai

| # | Điểm vỡ | Bằng chứng ngay ở loại đầu tiên |
|---|---|---|
| a | `bangGoc`/`maChucNang`/`maLoaiChungTu` bị chép y hệt cho mỗi lớp hành động | **4 bản chép** rồi: `LuuChungTuBanHangTemplate.java:37-49`, `GhiSoChungTuBanHang.java:44-56`, `BoGhiSoChungTuBanHang.java:45-57`, `XoaChungTuBanHang.java:42-54` — tất cả chỉ đọc hằng từ `BanHangSupport`. Sai một chỗ `maLoaiChungTu` là *"vô hiệu hoá lặng lẽ một nửa cơ chế khoá sổ"* (`ChungTuTemplate.java:130-132`) |
| b | `coGhiSoNgay` mặc định `false` ⇒ loại chứng từ mới **không bao giờ** chạm sổ cái ở luồng TAO cho tới khi ai đó nhớ override — thất bại im lặng theo đúng chiều nguy hiểm | |
| c | Loại không có nút "Lưu và ghi sổ" thì cả mô hình cờ thành nhiễu | |

Hướng xử lý (đợt sau, không nhét vào đợt này): gom `DacTaChungTu` (record: `bangGoc`, `maChucNang`,
`maLoaiChungTu`, `coSinhButToan`, `coAnhHuongTonKho`) tiêm qua constructor — xoá luôn 12 override rác.

### 7.11 Đã cân nhắc và **loại**: sealed hierarchy 5 lớp base theo hành động

`LuuChungTuBanHangTemplate` là cha chung của Tao+Sua với **10 override dùng chung**. Chia hierarchy
theo hành động thì `Tao extends TaoTemplate`, `Sua extends SuaTemplate` — **Java đơn kế thừa xoá mất
lớp chung đó**, 10 override phải chép đôi.

Bài toán là **hai trục**: 5 hành động × N loại chứng từ. Trục hành động **cố định** (5–8 giá trị),
trục loại chứng từ mới là trục tăng trưởng ⇒ chọn trục hành động làm hierarchy là chọn sai trục.
**Giữ switch** cho trục hành động (dữ liệu, không phải kiểu); tách trục loại chứng từ bằng
composition (§7.10).

## 8. Ảnh hưởng test

`ChungTuTemplateTest` có 16 test. Sau chuyển đổi: **16/16 fail biên dịch** (hai lớp giả override theo
tên cũ, và `TemplateGia.loadData:432` gọi `ctx.hanhDong().coHoanTac()` — cờ bị xoá), trong đó
**9 test đổi nghĩa**, không chỉ đổi nhãn.

| Test | Tình trạng | Việc phải làm |
|---|---|---|
| `chay_du_va_dung_thu_tu_moi_buoc` | Đổi nghĩa | Viết lại `TRINH_TU_TAO` (bỏ `ghiSo`/`apDungTonKho` vì "Lưu" thuần không chạm sổ cái) |
| `hanh_dong_tao_khong_hoan_tac_khong_khoa` | Chỉ đổi nhãn | |
| `hanh_dong_sua_khoa_chung_tu_truoc_khi_go_va_ghi` | Đổi nghĩa | Bỏ `boGhiSo` khỏi subsequence; đổi tên test |
| `hanh_dong_sua_go_tac_dong_cu_truoc_khi_luu` | **Xoá** | Thay bằng `sua_khong_cham_so_cai` + `sua_chung_tu_da_ghi_so_bi_chan` |
| `hanh_dong_can_hoan_tac_ma_loadData_khong_ghi_nhan_id…` | Đổi nghĩa | Guard chuyển lên `doiHoiDinhDanh`; message → `chuanBiChungTu phải gọi ctx.ghiNhanChungTu` |
| `saveEntity_khong_ghi_nhan_chung_tu_thi_bao_loi_ro_rang` | **Đang hỏng sẵn** (K1) | Vá bằng §4.4; message → `luuEntity phải gọi…` |
| `khai_co_anh_huong_ton_kho_ma_khong_cai_apDungTonKho…` | Đổi nghĩa | Bật `coGhiSoNgay()=true` hoặc chuyển sang luồng GHI_SO |
| `tao_moi_day_dung_lenh_ghi_so_sang_kernel` | Đổi nghĩa | **Tách 2 test**: `luu_thuan_tuy_khong_cham_so_cai` + `luu_va_ghi_so_day_dung_lenh_sang_kernel` |
| `tao_moi_khong_sinh_but_toan_van_kiem_tra_ky_ke_toan` | Phụ thuộc §7.1 | Giữ nguyên nếu chốt "giữ kiểm kỳ khi Lưu" |
| `xoa_chi_go_khong_kiem_ky_theo_ngay_cu` | Đổi nghĩa | Đảo assertion đầu thành `chungTuDaBoGhi).isEmpty()`; đổi tên |
| `bo_ghi_so_chi_go_khong_kiem_ky_theo_ngay_cu` | **Giữ nguyên** nếu chốt §7.3 theo khuyến nghị | |
| `ghi_so_dung_quyen_post` | Đổi nghĩa | `TemplateGia.loadData` phải ghi nhận id cho **mọi** hành động ≠ TAO |
| `thieu_quyen_thi_dung_truoc_khi_cham_du_lieu` | Chỉ đổi nhãn | |
| `thong_bao_chi_gui_sau_khi_commit` | Giữ nguyên | Điều kiện: bước private **không** tên `guiThongBao` |
| `thong_bao_loi_khong_lam_hong_nghiep_vu_da_commit` | Giữ nguyên | |
| `lenh_khong_hop_le_bi_chan_ngay_buoc_dau` | Chỉ đổi nhãn | ⛔ Không đổi `MaLoiChungTu.VALIDATION_FAILED` — hợp đồng FE |

## 9. Kế hoạch triển khai — 4 PR, KHÔNG gộp

`docs/conventions.md:270`: *"1 commit = 1 ý nghĩa. Không trộn feat + refactor + format"*.
Diff gộp ước tính 15–17 file / 700–900 dòng, trong đó chỉ ~120 dòng là đổi hành vi thật — reviewer
đọc 900 dòng sẽ bỏ lọt đúng 3 dòng quan trọng.

### PR0 — `bugfix/ctbh-base-entity` ⛔ BẮT BUỘC TRƯỚC TIÊN

Không chạm template. Mục tiêu: `:cell-app:build` xanh trở lại.

- 28 lỗi biên dịch, **toàn bộ** trong `VongDoiChungTuBanHangTest.java` (các dòng 39–155), do test viết
  theo entity đích V309 (`BaseChungTuEntity`/`BaseChiTietChungTuEntity`) trong khi
  `ChungTuBanHang.java:44` vẫn `extends AggregateRootEntity`.
- ⚠️ **Nợ nghiêm trọng hơn**: `V341__sal_ctbh_chuan_cot_chung_tu.sql:117-118` đã
  `DROP COLUMN trang_thai_chung_tu`, `:69` thêm `status`, `:54-60` đổi `ngay_tao→thoi_gian_tao`,
  `thu_tu→stt` — nhưng entity vẫn map tên cột **CŨ**. `ddl-auto: none` nên Hibernate không phát hiện;
  chạy trên DB thật sẽ lỗi `column does not exist`.
- ⇒ Hoặc hoàn tất chuyển entity sang `BaseChungTuEntity`, hoặc revert V341. **Phải chốt trước.**
- `base-chung-tu-entity-plan.md` §6.3 tuyên bố việc này "đã làm" — **thực tế chưa**; §6.5 tự thừa
  nhận "ánh xạ entity ⇄ schema chưa được Hibernate xác thực".

### PR0.5 — test mốc cho 5 lớp production

Viết khi chúng **còn hành vi cũ**, dùng làm mốc đối chiếu. Tối thiểu: SUA và BO_GHI_SO
(§7.9 — hiện 0 test).

### PR1 — `refactor/chung-tu-5-luong` (đổi hành vi, ~120 dòng)

Tách 5 luồng + `phanGhiSo` + `doiSoatVoiSoCai` + bỏ `coHoanTac()`/`ghiMoi()` + thêm `coGhiSoNgay` +
vá K1 + hạ `ghiSo`/`kyKeToan` xuống `private`. **Giữ nguyên tên 13 method.**

File: `ChungTuTemplate.java`, `HanhDongChungTu.java`, `ChungTuContext.java` (javadoc), 6 lớp con,
`ChungTuTemplateTest.java`.

### PR2 — `refactor/chung-tu-doi-ten` (0 đổi hành vi)

Bảng §5. Dùng `Rename Method` của IDE, **tuyệt đối không `sed`**. Bước 2 bắt buộc: sửa 5 chuỗi thông
báo lỗi + 33 string literal trong test (§5.3).

### PR3 — `docs`

Cập nhật javadoc còn nói "12 bước", "bước 5/9"; bổ sung ngoại lệ kỳ khoá + messageId vào
`UC_CTBH_GhiSo` và `UC_CTBH_BoGhiSo` ở **cả hai** bản sao epic; chốt `../../pmkt-docs/ba` là nguồn sự thật.

### ⚠️ Xung đột nhánh — chốt thứ tự merge TRƯỚC

| Nhánh | Ngày | Đụng gì |
|---|---|---|
| `origin/feat/chung-tu-ban-hang-base` (`0835b83`) | 04/08 | Sửa **đúng khối `thucThi`**: đổi `boGhiSo(ctx)` → `hoanTacTacDongCu(ctx)` **và thêm lại** `kiemTraDaGhiNhanChungTu(ctx)`. Còn move package `internal/model` → `domain`: 25 file / 51 dòng |
| `origin/refactor/accounting-core-base` (`a807fe7`) | 03/08 | Cũng chạm `accounting_core` |
| `origin/develop` | | **KHÔNG hề có** package `accounting_core/chung_tu` (diff `master...origin/develop` = 54 file / 7586 dòng xoá) |

⇒ Chốt base branch trước, nếu không PR không merge được về đâu cả. Đóng hai nhánh kia vào trước, rồi
mới mở PR tách luồng; PR đổi tên đi sau cùng.

### Checklist trước khi báo hoàn thành

```bash
cd cell-app && ./gradlew build
```

Cộng: rà `../conventions.md` §5, và **grep lại 5 tên còn trùng hierarchy khác** (`maChucNang`,
`maLoaiChungTu`, `hanhDong`, `beforeSave`, `afterSave`) trước khi commit.

## 10. Điểm phải chốt trước khi code

| # | Câu hỏi | Khuyến nghị |
|---|---|---|
| Q1 | Nút "Lưu" thuần có phải chặn kỳ đã khoá không? (BR17.1 nói **CÓ**; hiểu theo nghĩa hẹp của điều chỉnh thì **KHÔNG**) | **Giữ chặn** — đã đưa vào §4.2. Nếu bỏ, phải sửa kèm `business_rules.md:508` |
| Q2 | `luongBoGhiSo` có thêm `kiemTraKyKeToan` ở template không? | **Không** — kernel kiểm theo từng ngày dòng cũ, chặt hơn và không tạo ngõ cụt (§7.3) |
| Q3 | `luongGhiSo` có thêm `kiemTraKyKeToan` không? | **Không** — kernel đã kiểm với đúng cặp tham số nó sắp INSERT (§7.2) |
| Q4 | Sau khi bỏ bước gỡ ở SUA/XOA, chấp nhận rằng tính đúng đắn sổ cái phụ thuộc vào cờ? | **Không chấp nhận trần** — bù bằng `doiSoatVoiSoCai` (§4.5) + một truy vấn đối chiếu hàng loạt |
| Q5 | 4 messageId `013/016/021/023` có còn là hợp đồng với FE? | Nếu **có** ⇒ base không được ném lỗi nghiệp vụ (§6.5) |
| Q6 | XOÁ chứng từ chưa ghi sổ trong kỳ đã khoá: cho hay chặn? | Hôm nay **cho**. BR17 Common không liệt kê "Xoá". Cần BA xác nhận |
| Q7 | Chứng từ có `coGhiSoNgay = true` nhưng không sinh được bút toán nào (giá trị 0): trạng thái cuối là *Đã ghi sổ* hay *Chưa ghi sổ*? | Hôm nay trả lời *"Đã ghi sổ mà không có dòng nào"* — câu trả lời tệ, là nguồn của lệch §7.3 |
| Q8 | PR0: hoàn tất chuyển entity sang `BaseChungTuEntity`, hay revert V341? | Cần chốt trước mọi việc khác |
| Q9 | Tồn kho áp khi **LƯU** hay khi **GHI SỔ**? (bản triển khai đang là "khi ghi sổ" — xem §12.2c) | "Khi ghi sổ" — nhất quán với sổ cái, và nháp thì chưa nên động vào kho |

## 11. Việc nên làm kèm (chi phí thấp, cùng vùng code)

- Đặt `lock_timeout` cho datasource — `pg_advisory_xact_lock` chặn **vô hạn**, không `NOWAIT`
  (`ChungTuKhoaService.java:25-26`), pool chỉ 10 connection ⇒ 10 request cùng một chứng từ là cạn pool.
  Dịch SQLSTATE `55P03` sang 409 (`GlobalExceptionHandler.java:84-87` đã có handler).
- Siết 3 nhánh **fail-open** của `KyKeToanChecker` (ngày `null` `:74-76`, tenant `null` `:77-82`,
  mã loại `null` `:48-49`): ở đường GHI phải ném lỗi cấu hình thay vì lặng lẽ coi như kỳ đang mở.
- Bắt riêng vi phạm `uq_sal_ctbh_so_ct` và dịch thành `TRUNG_SO_CHUNG_TU` — hai người cùng nhập tay
  cùng số chứng từ hiện ăn lỗi 500 thô.
- Thêm một `ModularityTest` (`ApplicationModules.of(CellApplication.class).verify()`) — `cell-app`
  hiện **không có** test spring-modulith nào, ranh giới `accounting_core` ⇄ `chung_tu_ban_hang` đang
  chỉ được kiểm bằng mắt.

## 12. Tình trạng triển khai (cập nhật 2026-08-05)

### 12.1 Đã làm

| Hạng mục | Tình trạng |
|---|---|
| PR1 — tách 5 luồng, bỏ `coHoanTac()`/`ghiMoi()`, thêm `coGhiSoNgay`, `phanGhiSo`, `doiSoatVoiSoCai`, vá K1 (`kiemTraDaGhiNhanChungTu`), hạ `ghiSo`/`kyKeToan` xuống `private` | ✅ |
| PR2 — đổi tên 8 hook + 6 bước private theo §5 | ✅ (gộp cùng PR1, xem §12.4) |
| `ChungTuTemplateTest` viết lại | ✅ **25 test, xanh** |
| Cập nhật javadoc còn nói "bước 1..12" | ✅ 11 điểm |
| PR0 — nợ entity `BaseChungTuEntity` / V341 | ❌ **CHƯA** — chỉ gỡ chặn tạm (§12.3) |
| PR3 — bổ sung đặc tả kỳ khoá vào epic CTBH | ❌ chưa |

### 12.2 Ba điểm LỆCH so với thiết kế §4 — đã cân nhắc, cần biết

**a) `doiSoatVoiSoCai` ném `ApiException.conflict` (409), KHÔNG phải `IllegalStateException` (500).**
§4.5 viết là lỗi kỹ thuật. Sai: ca thường gặp nhất không phải dữ liệu hỏng mà là **tranh chấp** —
`kiemTraNghiepVu` của lớp con đọc cờ trạng thái từ entity nạp TRƯỚC khi có khoá nên không thấy người
khác vừa ghi sổ xong; bước đối soát hỏi thẳng sổ cái nên thấy. Cả hai ca xử lý được bằng cùng một
hành động (tải lại → Bỏ ghi sổ trước), nên 409 đúng hơn 500.
Thêm mã mới: `MaLoiChungTu.SO_CAI_LECH` / `MSG_CORE_CT_002` — **cần báo FE**.

**b) Thêm bước `luuNhap` chặn "có định khoản mà không ghi sổ".**
Không có trong §4. Lý do: `coGhiSoNgay` mặc định `false` biến "quên override" thành *im lặng không ghi
sổ* — module chứng từ thứ hai dựng đủ định khoản ở `sauKhiLuu` nhưng quên override sẽ nhận HTTP 200,
audit ghi "thành công", `acc_so_cai` trống, định khoản bị vứt đi không một dòng log. Nay nổ ngay.

**c) ⚠️ Tồn kho nay chỉ áp KHI GHI SỔ, không áp khi "Lưu" thuần.**
Bản cũ chạy `updateInventory` **vô điều kiện** cho TAO/SUA/GHI_SO; bản mới đặt `capNhatTonKho` bên
trong `phanGhiSo`. Đây là **quy tắc nghiệp vụ thứ 6**, không nằm trong 5 điều đã chốt — nó theo đúng
§4.2 nhưng chưa được xác nhận tường minh.
Hôm nay **không có hồi quy sống**: không module nào khai `coAnhHuongTonKho() = true`
(`chung_tu_ban_hang/package-info.java:21` khai `false`), hai hook vẫn ném lỗi mặc định.
👉 **Cần chốt Q9**: kho áp khi LƯU hay khi GHI SỔ? Nếu trả lời "khi LƯU" thì phải kéo `capNhatTonKho`
ra khỏi `phanGhiSo`.

### 12.3 Nợ gỡ chặn tạm — PHẢI dọn

`build.gradle.kts` thêm một dòng loại trừ `VongDoiChungTuBanHangTest` khỏi test source set, kèm
comment và trỏ về §9 PR0. Không sửa test về entity cũ vì làm vậy sẽ khoá chặt lại đúng schema mà V341
muốn bỏ (`V341:118` `DROP COLUMN trang_thai_chung_tu`, `:59-60` `thu_tu → stt`, và `:160-166` có khối
`DO $$` chủ động `RAISE EXCEPTION` nếu còn sót cột cũ ⇒ không có đường lui).

⛔ **Không merge diff này trước khi chốt Q8.** Entity đang map cột schema đã DROP — chạy thật sẽ hỏng
ở tầng JPA bất kể template đúng hay sai.

### 12.4 `./gradlew :cell-app:build` — CHƯA XANH

| Lane | Kết quả |
|---|---|
| `compileJava` | ✅ |
| `build -x test` (assemble + `checkstyleMain` + `checkstyleTest`) | ✅ |
| `ChungTuTemplateTest` | ✅ 25/25 |
| `unitTest` (toàn bộ) | ❌ **256 test / 1 fail** |
| `test` (tích hợp) | ⛔ không chạy được — Docker daemon không chạy, Testcontainers |

Test đỏ là `HandlerAuthorizationArchTest.everyHandlerIsAuthorizationGated`, báo
`ChungTuBanHangController#create` và `#update` không có cổng phân quyền. **Đây là lỗi CÓ SẴN, không do
đợt này**: đã dựng git worktree ở `HEAD` sạch, chỉ thêm đúng dòng loại trừ ở §12.3, chạy lại → fail y
hệt với đúng hai handler đó. Nguyên nhân thật: hai method này *có* `quyen.require(...)`
(`ChungTuBanHangController.java:96`, `:107`) nhưng chúng override method generic của
`BaseCrudController` nên javac sinh **bridge method**; `callsOwnerNamed` soi bridge (rỗng) và
`describe()` gộp chung tên với method thật. Sửa đúng: cho rule bỏ qua bridge/synthetic — **không**
thêm hai entry vào `REVIEWED_EXEMPT` vì chúng thật sự đã được gate.

### 12.5 Chưa làm: tách commit

§9 yêu cầu 4 PR riêng. Bản triển khai đang là **một working tree chưa commit**, gộp PR1 + PR2.
Tách được thành 2 commit (đổi tên thuần / đổi hành vi) khi cần. Ràng buộc thứ tự merge với
`origin/feat/chung-tu-ban-hang-base` và `origin/refactor/accounting-core-base` (§9) **vẫn chưa giải
quyết** — hai nhánh đó sửa đúng khối `thucThi`.

### 12.6 Đã kiểm chứng bằng thực nghiệm, không phải suy luận

1. Thêm `DUYET` vào `HanhDongChungTu` → `error: the switch expression does not cover all possible
   input values`. Lời hứa ở §6.3 là thật.
2. Gỡ `doiSoatVoiSoCai(ctx)` khỏi `luongXoa` → test đỏ. (Trước khi bổ sung test, mutation này **sống
   sót** — lỗ hổng do phản biện tìm ra và đã vá.)
3. Lỗi ArchUnit tái hiện trên baseline sạch ⇒ có sẵn (§12.4).

---

## Phụ lục — nguồn bằng chứng

Kết luận trong tài liệu này dựa trên 6 hướng điều tra + 4 góc phản biện độc lập chạy trực tiếp trên
repo (đọc code, chạy `javac`/`gradle`, `git diff` các nhánh remote, đối chiếu `../../pmkt-docs/ba`).
Mọi khẳng định đều kèm `file:dòng`. Ba khẳng định được **đo trực tiếp** chứ không suy luận:

1. `javac 21.0.6` không cưỡng chế vét cạn switch statement trên enum (kể cả `-Xlint:all`) — §6.3.
2. `:cell-app:compileTestJava` FAIL 28 lỗi, toàn bộ trong một file — §9 PR0.
3. `kiemTraDaGhiNhanChungTu` không có lời gọi nào trong `../../cell-app/src`; bản `bcaf367` còn có, `fd3fbda`
   đã xoá — §2.3 K1.
