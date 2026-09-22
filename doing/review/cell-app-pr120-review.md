# Review PR #120 — `cell-app` · Sổ công nợ P1 integration

- **Chế độ**: **SÂU** — PR trước merge, diff chạm migration (`V1099`) và base class dùng chung
  (`ChungTuTemplate`). Đã chạy cổng `unitTest` trên đúng snapshot head + đo baseline.
- **Kết luận**: **REQUEST CHANGES** (2 Major nghiệp vụ, 2 Major kiến trúc/hợp đồng; cổng `unitTest`
  đỏ 2 test tuy không quy được cho diff).

## 1. Phạm vi

| Mục | Giá trị |
|---|---|
| Repo | `cell-app` (`https://github.com/ospgroupvn-pmkt/cell-app`) |
| Head | `8d64461f5bc47064da2dcb60f5c950ba657148f6` (nhánh `origin/feat/so-cong-no-p1-integration`) |
| Base giả định | `origin/develop` — **giả định**, không có `gh` trên máy nên không đọc được metadata PR; đã xác minh ref tồn tại và nhánh head chỉ nằm trên nhánh này |
| Merge-base | `cfc18545cd29f47f34bba835a29faa8efb7e0c7f` |
| Diff | 32 commit · **143 file** · +16.631 / −433 |
| Working tree | sạch (`git status --porcelain` rỗng) |
| Vùng đóng băng | **0 file** — không chạm `master_data/`, `legacy/`, tài liệu Phase 2 |
| develop đi trước merge-base | **1 commit** (`622dd2d9`) · **0 file giao nhau** với diff |

Tài liệu nguồn đã đọc: `pmkt-docs/ba/Common/TaiLieuMappingSoCongNo.md` (656 dòng, toàn bộ) — đây là
authority duy nhất mà diff viện dẫn (§3 · §4 · §5.1–§5.14 · §6). **BR đã đọc**: BR7 (số liệu/tiền
tệ). **BR chưa đọc**: BR4 · BR9 · BR12 · BR17 · BR33 · BR36 · BR37 · BR41 · BR42 · BR48 · BR49
(nhóm "chứng từ & hạch toán") — diff không nhắc mã BR nào trong nhóm đó và mọi luật nó cài đều trích
`TaiLieuMappingSoCongNo.md`, nên bỏ lại có chủ đích, ghi ra đây để người sau biết.

### Phần ĐÃ đọc / CHƯA đọc

- **Đã đọc kỹ**: `accounting_core/ChungTuTemplate` · toàn bộ `so_cong_no/**` (api + service + 2
  repository) · `V1099` (và đối chiếu `V1097`, `V1049`) · `tien_mat_tien_gui/**` ·
  `kho/internal/congno/CongNoPhieuKhoService` + hai `LuuPhieu*KhoTemplate` + hai `GhiSoPhieu*Kho` ·
  ba lớp `GiamKhoanNo*` · `so_du_ban_dau/internal/hach_toan/GhiSoCongNoSoDuBanDau` ·
  `hoa_don_mua/HoaDonMuaService` · `chung_tu_mua_hang/cong_no/MuaHangCongNoBridge` ·
  `tra_lai_hang_mua/CongNoTraLaiHangMuaService`.
- **Chỉ lướt / CHƯA đọc**: các `*Mapper` của ban_hang · dieu_chinh_gia (bán và mua) · `CongNoKtthService`
  nội bộ · ba `SoDu*CongNoMapper` · **46 file test**. Kết luận dưới đây không phủ những phần này.

## 2. Findings

### Major

#### M1 — "Lưu và ghi sổ" phiếu nhập/xuất kho KHÔNG ghi Sổ công nợ (§5.13)

- **File**: `src/main/java/vn/vtt/pmkt/cell/kho/nhap_kho/internal/service/business/LuuPhieuNhapKhoTemplate.java:63`
  và `.../kho/xuat_kho/internal/service/business/LuuPhieuXuatKhoTemplate.java:61`
- **Nguồn**: `TaiLieuMappingSoCongNo.md` §5.13 — "Bút toán dòng hàng chạm TK công nợ … vế thuận →
  **GỐC**"; §6 — "Ghi sổ chứng từ → Sinh dòng gốc … **cùng giao dịch**".
- **Trigger**: lập phiếu nhập (hoặc xuất) kho có dòng hạch toán thẳng vào TK công nợ, bấm **"Lưu và
  ghi sổ"** (`request.laLuuVaGhiSo() = true`).
- **Expected**: phiếu ghi sổ ⇒ sinh dòng GỐC trong `acc_phat_sinh_cong_no`.
- **Actual**: `luongTao`/`luongSua` → `phanGhiSo` → `phanGhiCongNo` → `coSinhCongNo()` trả `false`
  (mặc định của base) ⇒ **không ghi gì**. Hai `LuuPhieu*KhoTemplate` không có một chữ `CongNo` nào
  (`grep -c CongNo` = 0), trong khi `GhiSoPhieuNhapKho.java:148` và `GhiSoPhieuXuatKho.java:152`
  (nút "Ghi sổ" rời) khai `coSinhCongNo() = true` và cài `ghiCongNo`.
- **Hậu quả**: phiếu ở `DA_GHI_SO`, sổ cái đủ bút toán, sổ công nợ RỖNG. Không exception, không log
  — đúng mô tả mà commit cuối của chính PR này (`8d64461f`) dùng để vá ca tương đương bên thu-chi:
  *"trông y hệt 'producer chưa làm', và chỉ lộ ra khi có người đối chiếu số còn nợ"*. Đây là **cùng
  một lớp lỗi, còn sót ở hai module**.
- **Đối chiếu**: bốn module còn lại đã phủ cả hai đường — `LuuChungTuBanHangTemplate:242`,
  `LuuDieuChinhGiaTemplate:153`, `LuuTraLaiHangBanTemplate:185`, `LuuPhieuKtthTemplate:219` đều
  override `ghiCongNo`. Kho là ngoại lệ duy nhất.

#### M2 — Thu/chi ghi công nợ ngoài hook mà chính PR này vừa dựng

- **File**: `src/main/java/vn/vtt/pmkt/cell/tien_mat_tien_gui/internal/service/business/LuuPhieuThuChiTemplate.java:477-491`
- **Hợp đồng bị phá**: `ChungTuTemplate` (cũng do PR này thêm) chốt tường minh —
  *"Vì sao vẫn phải là hook của base chứ không để mỗi lớp con tự gọi trong `sauKhiLuu`… Để lớp con
  tự chọn chỗ gọi là để mỗi module chọn một chỗ khác nhau, và ca sai chỉ lộ ra khi dữ liệu đã lệch."*
- **Actual**: `LuuPhieuThuChiTemplate` gọi `ptc.ghiSoCongNo().ghi(...)` trong thân `sauKhiLuu`, không
  khai `coSinhCongNo()`, không override `ghiCongNo`. `XoaPhieuThuChi` cũng không override
  `goCongNo`/`kiemTraCongNoTruocKhiGo`.
- **Vì sao đây là finding chứ không phải lựa chọn**: comment tại chỗ nói phải đặt **trước**
  `tinhLaiTrangThaiNguon`, mà hook `phanGhiCongNo` của base chạy **sau** `sauKhiLuu`. Tức là hook
  base đặt sai mốc cho ca này, hoặc thu-chi đặt sai chỗ — **một trong hai**, và hiện tại tồn tại hai
  định nghĩa khác nhau của "mốc ghi công nợ" trong cùng một PR. Module thứ bảy lên sau sẽ chọn theo
  cái nó đọc trúng trước.
- **Đề nghị**: hoặc thêm hook chạy trong `phanGhiSo` **trước** `sauKhiLuu` cho ca này, hoặc ghi rõ
  ngay trong javadoc `coSinhCongNo()` rằng thu-chi là ngoại lệ đã biết và vì sao.

#### M3 — Mã lỗi Sổ công nợ nhân bản literal ở 8 producer, 5 biến thể tên cho cùng một nghiệp vụ

- **File** (mẫu, tất cả đều là file MỚI của PR):
  - `kho/internal/congno/CongNoPhieuKhoService.java:151,186,197` → `DEBT_ROW_REFERENCED` ·
    `DEBT_CURRENCY_UNRESOLVED` · `POSTING_ACCOUNT_REQUIRED`, `maThongBao = null`
  - `ke_toan_tong_hop/internal/service/congno/CongNoKtthService.java:136,227,248` → cùng ba mã, `null`
  - `tra_lai_hang_mua/internal/congno/CongNoTraLaiHangMuaService.java:128,210,226` →
    `PAYABLE_ROW_REFERENCED` · `PAYABLE_CURRENCY_UNRESOLVED`, `null`
  - `ban_hang/tra_lai_hang_ban/.../CongNoTraLaiHangBanService.java:165,180` → `RECEIVABLE_*`, `null`
  - `ban_hang/dieu_chinh_gia_hang_ban/internal/congno/CongNoDieuChinhGiaService.java:157,184,199`
  - `dieu_chinh_gia_hang_mua/internal/congno/CongNoDieuChinhGiaMuaService.java:149,222,251` →
    `PAYABLE_*` với `"MSG_PMKT-E-06768_002"`
  - `hoa_don_mua/.../CongNoHoaDonMuaService.java:107` · `CongNoHoaDonMuaMapper.java:159,178` →
    `"MSG_PMKT-E-00542_022"`
  - `chung_tu_mua_hang/.../MuaHangCongNoService.java:287` → `MaLoiMuaHang.MSG_LOI_HE_THONG`
- **Luật**: CLAUDE.md luật 1 (không hardcode magic value, constant có tên đặt gần nơi dùng) và
  bảng bảy lỗi **#7** ("mã message `MSG_…` không thành hằng số/key" → mặc định **Major**).
- **Bằng chứng nội tại**: chính PR này đã tạo `chung_tu_mua_hang/.../MaLoiCongNoMuaHang.java` làm
  đúng việc đó cho **một** module — rồi bảy module còn lại viết literal, và `MuaHangCongNoService`
  vẫn còn một literal `"PAYABLE_ROW_REFERENCED"` ngay cạnh lớp hằng số của chính nó.
- **Hậu quả cụ thể (không chỉ là văn phong)**: cùng một tình huống nghiệp vụ — "khoản nợ/khoản chờ
  đang bị chứng từ khác đối trừ" — trả về FE **ba mã khác nhau** (`DEBT_` / `PAYABLE_` /
  `RECEIVABLE_ROW_REFERENCED`), và **5/8 chỗ truyền `maThongBao = null`** trong khi 3 chỗ kia truyền
  mã `MSG_PMKT-E-*`. FE không viết được một handler chung, và người dùng nhận thông điệp lúc có
  lúc không tuỳ module.
- **Ghi chú công bằng**: literal mã lỗi là **kiểu đã tồn tại rộng khắp repo** (≈116 KB kết quả
  `git grep`), nên đây không phải PR đơn phương phá luật; điều tính vào PR là nó **thêm 8 bản mới**
  và **không đồng nhất với chính hằng số nó vừa tạo**.

#### M4 — Hai file 205 dòng trùng nhau 100 %, javadoc trỏ sai lớp gốc

- **File**: `tra_lai_hang_mua/internal/congno/GiamKhoanNoChungTuMuaGoc.java` và
  `dieu_chinh_gia_hang_mua/internal/congno/GiamKhoanNoChungTuMuaGocDcg.java`
- **Actual**: `diff` hai file cho đúng **3 dòng lệch** — package, tên lớp, tên constructor. Cả hai
  cùng là bản sao của `ban_hang/internal/congno/GiamKhoanNoTheoChungTuGoc.java`.
- **Bằng chứng copy-paste đã trôi ngay tại lần chép đầu**:
  1. Javadoc cả hai file viết *"BẢN SAO CÓ CHỦ ĐÍCH của `ban_hang.internal.congno.GiamKhoanNoChungTuMuaGoc`"*
     — lớp đó **không tồn tại**; bản `Dcg` còn tự trỏ về `…GiamKhoanNoChungTuMuaGocDcg` trong
     `ban_hang`, cũng không tồn tại. Tên thật là `GiamKhoanNoTheoChungTuGoc`.
  2. Cả hai file có **hai khối javadoc liên tiếp** (`GiamKhoanNoChungTuMuaGoc.java:19-37` rồi
     `:38-64`) — khối đầu là javadoc **mồ côi**, không gắn với khai báo nào.
- **Lý do nhân bản được nêu trong file** (ranh giới Modulith, không có module trung lập) là **có
  thật**, và file đã ghi sẵn đường xoá (`FOUNDATION_FOLLOW_UP`: thêm `nhomGoc` vào
  `LenhDoiTruTheoChungTu`). Finding không đòi bỏ bản sao ngay — nó đòi (a) sửa hai tham chiếu javadoc
  sai, (b) gộp hai khối javadoc, (c) ticket hoá đường xoá thay vì để `TODO` không mã.

### Minor

#### m5 — Sentinel "TK đối ứng trống" lọt ra khỏi module qua `traDongGocTheoChungTu`

- **File**: `so_cong_no/internal/repository/PhatSinhCongNoRepositoryImpl.java:120-124`
  (`SELECT_DONG_GOC` dựng thẳng `new KhoanNo(… p.tkDoiUngId, p.tkDoiUng …)`)
- **Bất biến bị phá**: `so_cong_no/internal/service/business/TaiKhoanDoiUngTrong.java` — *"Sentinel
  KHÔNG BAO GIỜ ra khỏi module… và không có lối tắt nào đọc thẳng `getTkDoiUngId()` vào một DTO công
  khai. Bỏ sót một đường đọc là để lộ `00000000-…` lên màn hình."*
- **Trigger**: `GhiSoCongNoSoDuBanDau.ghi` ghi `LenhGhiKhoanNo(… tkDoiUng = null …)` (§5.12) ⇒ DB
  lưu `tk_doi_ung_id = 00000000-0000-0000-0000-000000000000`, `tk_doi_ung = ''`. Sau đó gọi
  `SoCongNoApi.traDongGocTheoChungTu(chungTuId = id bản ghi `sdbd_*`, tkCongNoId)`.
- **Actual**: trả UUID toàn 0 và chuỗi rỗng, không qua `idCongKhai`/`maCongKhai`. Ba đường đọc kia
  (`khoanNoConLai`, `khoanChoConLai`, `khoanNoTheoChungTu`) đều đã scrub đúng.
- **Vì sao Minor chứ không Major**: hai caller hiện có (`PhanBoCongNoService:115`,
  `GhiSoCongNoThuChi` — chỗ này PR vừa gỡ) **không đọc** `tkDoiUngId`/`tkDoiUng` của `KhoanNo`, nên
  chưa lộ ra dữ liệu sai. Đây là lỗ hợp đồng chờ caller thứ ba.

#### m6 — `khoanNoTheoChungTu` bị gọi từng-chứng-từ-một, trái đúng hợp đồng của nó

- **File**: `ban_hang/internal/congno/GiamKhoanNoTheoChungTuGoc.java:166`
  (`soCongNoApi.khoanNoTheoChungTu(List.of(lenh.chungTuGocId()))`) và hai bản sao tương ứng
  (`GiamKhoanNoChungTuMuaGoc.java` · `…Dcg.java`).
- **Hợp đồng**: `SoCongNoApi.khoanNoTheoChungTu` javadoc — *"Theo LÔ và chỉ theo lô: một lượt bỏ ghi
  sổ hoặc một phiếu chi chạm nhiều chứng từ gốc, và **một truy vấn mỗi chứng từ là N+1 ngay tại
  luồng ghi sổ**."*
- **Actual**: `CongNoTraLaiHangMuaService.ghi:87` lặp trên `nhom` (khoá = chứng từ mua × TK công nợ ×
  loại × TK đối ứng) và gọi `giam()` mỗi vòng ⇒ **một query `timDongGocTheoChungTu` mỗi nhóm**.
  Cùng dạng ở `CongNoTraLaiHangBanService` · `CongNoDieuChinhGiaService` · `…GiaMuaService`.
- **Hậu quả**: N nhỏ (số chứng từ gốc trên một phiếu trả lại / điều chỉnh), nên tác động thực tế
  thấp — nhưng nó đúng là kiểu gọi mà API vừa được thiết kế để tránh, và sẽ xấu đi khi có phiếu trả
  lại gộp nhiều chứng từ.

#### m7 — `V1099` đụng độ với một nhánh khác đang mở

- **File**: `src/main/resources/db/migration/V1099__ktth_btcn_chi_nhanh_theo_v1097.sql` (mới)
- **Kiểm chứng**: `max` migration trên `origin/develop` = `V1098` ⇒ **đánh số hợp lệ so với nhánh
  đích**. Nhưng quét toàn bộ remote branch: `origin/feature/thuchimodulemua` đang giữ
  `V1099__cash_map_vat_tu_id.sql`. Cả hai đều **chưa** vào develop.
- **Hậu quả**: nhánh nào merge sau sẽ làm Flyway ném *"Found more than one migration with version
  1099"* trên mọi môi trường đã chạy nhánh trước — đỏ 100 % ở deploy, xanh 100 % ở local.
- **Nội dung migration thì ĐÚNG** — đã đối chiếu: `fn_chi_tiet_chep_chi_nhanh` của `V1097:217` nhận
  `TG_ARGV[0] = bảng header`, `TG_ARGV[1] = cột FK`, và `V1099` truyền
  `('ktth_phieu_ke_toan_tong_hop', 'phieu_ktth_id')` — đúng thứ tự; entity
  `ChiTietBuTruCongNo` thật sự `extends BaseChiTietChungTuEntity` với
  `@JoinColumn(name = "phieu_ktth_id")`; khuôn cột-nullable + backfill + trigger giữ nguyên `V1097`.

### Nit

- **n8** — `CongNoPhieuKhoService.ghiVe` (`kho/internal/congno/CongNoPhieuKhoService.java:139`)
  dựng `taiKhoanDoiUng(...)` — hàm này **ném** `POSTING_ACCOUNT_REQUIRED` khi `tkDoiUngId == null` —
  **trước** phép kiểm vế thuận/ngược ở dòng 145 (`if (veNo != vaiTro.laDuNo()) return;`). Một bút
  toán thiếu TK ở vế lẽ ra bị bỏ qua sẽ ném 400 thay vì được bỏ qua lặng. Hiện chưa tới được vì
  `GhiSoPhieuNhapKho.butToanCongNo` đã lọc dòng thiếu tài khoản; đảo hai dòng là xong.
- **n9** — Hai commit dùng type ngoài quy ước `<type>(<scope>): <mô tả>`:
  `checkpoint(so-cong-no): iteration-1 hooks…` và bốn commit `wip(so-cong-no): …`.
- **n10** — `V1049:220` ghi *"KHÔNG nhân lại `ps_no × ty_gia`"* (đúng cho dòng GỐC), trong khi
  `SoCongNoService.dongDoiTruTheoGoc` cố ý nhân `phanNguyenTe × goc.getTyGia()` cho dòng ĐỐI TRỪ
  theo §5.8. Hai luật không mâu thuẫn nhưng comment cột không nói rõ nó chỉ áp cho dòng gốc — dễ bị
  người sau đọc thành cấm chung.

## 3. Bảng bảy lỗi hay gặp

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục (BE) | ✅ Không vi phạm. Mọi file mới nằm dưới `internal/`; DTO mới thêm vào `so_cong_no/api/dto` đã có `package-info` `@NamedInterface` sẵn; không có file phẳng mới ở gốc module. `ban_hang/internal/congno/` là code dùng chung của các sub-module `ban_hang` — đúng shape. |
| 2 | Không đánh lại version migration | ⚠ **m7** — hợp lệ so với `develop` (max `V1098`) nhưng **đụng `origin/feature/thuchimodulemua`**. |
| 3 | Chưa test lại sau khi merge | ✅ N/A — `develop` chỉ đi trước merge-base **1 commit** (`622dd2d9`) và **0 file giao nhau** với diff. |
| 4 | N+1 | ⚠ **m6** — `khoanNoTheoChungTu` gọi một-chứng-từ-mỗi-lần trong vòng lặp producer. Các đường khác (`dinhTuyenTaiKhoan`, `tongPhanBoTheoGoc`, `TraCuuTaiKhoanThueNguonRepository`) đều theo lô, đúng. |
| 5 | Chưa tận dụng BaseController/BaseEntity/Template | ⚠ **M1 + M2** — hook `coSinhCongNo/ghiCongNo/goCongNo` được dựng đúng ở `ChungTuTemplate` nhưng kho không dùng (M1) và thu-chi đi vòng (M2). Phần còn lại dùng đúng: `ChungTuTemplate`, `GhiSoApi`, `BaseChiTietChungTuEntity`. Ngoại lệ `chung_tu_mua_hang` đi qua `MuaHangCongNoBridge` — **đã khai báo tường minh** là cầu tạm kèm đường xoá 3 bước, chấp nhận được. |
| 6 | Chưa tận dụng base FE | ✅ N/A — diff không có file `client/`. |
| 7 | Constant / mã message đặt sai chỗ | ⚠ **M3**. |

## 4. Lớp A — cổng cứng

| Mục | Kết quả |
|---|---|
| Secret trong diff | ✅ Không có |
| Hardcode magic value | ⚠ mã lỗi literal — **M3** |
| Vùng đóng băng | ✅ 0 file |
| Controller chứa business logic / gọi Repository / trả Entity | ✅ Không — diff không thêm controller nào |
| `ApiResponse<T>` · `@RestControllerAdvice` | ✅ Không đường nào tự bắt-và-trả lỗi; mọi lỗi đi qua `ApiException` |
| Nuốt exception | ✅ Không thấy `catch` rỗng trong phần đã đọc |
| Commit thẳng `master`/`develop` | ✅ Không |
| **Nghiệp vụ tự bịa** | ✅ **Không tìm thấy.** Hai điểm nghi ngờ đều được kiểm và **có nguồn**: (a) bỏ cờ `la_tk_cong_no` khỏi tiêu chí định tuyến — §3 chốt tiêu chí duy nhất là `VaiTroDoiTuongTheoDoi` có giá trị, *"không viết cứng số hiệu"*; (b) `laDongGocThue` suy loại gốc từ `tkDoiUngId` — §5.4/§5.5 khai thẳng *"dòng gốc có `TKDoiUng` = TK thuế"*, và tập TK thuế do producer truyền vào chứ không đoán theo số hiệu. Ngược lại, `CongNoPhieuKhoService` **từ chối** ghi vế ngược thành khoản chờ và ghi rõ đó là khoảng trống chờ BA mở §5.13 — đúng luật 9 (không tự quyết nghiệp vụ). |

⚠ **Thay đổi hành vi cần BA/DBA biết**: bỏ `la_tk_cong_no` nghĩa là mọi tài khoản có
`doi_tuong_lien_quan` khai giá trị **nay sinh dòng sổ công nợ**, kể cả tài khoản trước đây có
`la_tk_cong_no = false`. Đúng §3, nhưng là thay đổi tập dữ liệu trên hệ đang chạy — nên đối chiếu
`mst_he_thong_tai_khoan` xem có bao nhiêu tài khoản rơi vào ca lệch cờ trước khi deploy.

## 5. Cổng đã chạy

| Cổng | Lệnh | Kết quả |
|---|---|---|
| `unitTest` trên head | `git worktree add --detach .review-pr120 8d64461f` → `./gradlew unitTest --console=plain` | 🔴 **BUILD FAILED** — 3.945 test, **2 fail**, 2 skip (3 phút 50) |
| Baseline tại merge-base `cfc18545` | cùng lệnh, worktree detached riêng | ⛔ **KHÔNG ĐO ĐƯỢC** — `compileTestJava` FAILED (2 error) |
| Baseline tại `origin/develop` `622dd2d9` | cùng lệnh | ⛔ **KHÔNG ĐO ĐƯỢC** — `compileTestJava` FAILED, cùng 2 error |
| `trace.sh` / `msg.sh` | — | ⛔ **NOT-RUN** — không có `docs/doing/<slug>-spec/` cho Sổ công nợ (`ls docs/doing` chỉ có spec của PMKT-E-06194), và diff trải trên >10 epic nên không có một thư mục PYC đơn để truyền vào `msg.sh`. |
| Cổng FE | — | N/A — không có diff `client/` |
| Testcontainers | — | **KHÔNG chạy** (cần Docker, bị cấm). Nhiều test tích hợp mới của PR (`*IntegrationTest`, `*VongDoiIT`) nằm ngoài `@Tag("unit")` nên **chưa được kiểm chứng ở lượt review này**. |

### Hai test đỏ — phân tích

```
HoaDonMuaControllerPermissionTest > luuVaGhiSoYeuCauThemQuyenPost() FAILED
  Wanted: quyenChecker.require("NhanHoaDon", "Post")
  Actual: quyenChecker.require("NhanHoaDon", "Create")   (BaseCrudController.create:192)

LoaiChungTuChuDongBoCheckTest > enum_va_check_constraint_khop_nhau() FAILED
  Whitelist SQL thiếu "CASH_CHUYEN_TIEN_NOI_BO" so với enum LoaiChungTuChu
```

**Không quy được cho diff PR**, dựa trên ba bằng chứng:
1. Cả hai file test **và** code chủ thể của chúng (`HoaDonMuaController`, enum `LoaiChungTuChu`,
   migration whitelist) đều **không nằm trong diff** (`git diff --name-only … -- '*HoaDonMuaController*' '*LoaiChungTuChu*'` rỗng).
2. Nội dung assertion không liên quan sổ công nợ: một là quyền `Post` của màn Nhận hoá đơn, một là
   đồng bộ enum ↔ CHECK constraint của loại chứng từ chủ.
3. Cả hai chạm phần do `64b1787c Tiền mặt tiền gửi update (#100)` mang vào — commit của develop mà
   nhánh này chỉ **merge vào** (`f3360dd1`), không sửa.

**Nhưng vẫn chặn merge**: `unitTest` là cổng nghiệm thu bắt buộc và nó đang đỏ trên head. Đề nghị
tách một fix riêng cho `CASH_CHUYEN_TIEN_NOI_BO` (thêm vào whitelist SQL) và cho quyền `Post` của
`NhanHoaDon`, hoặc xác nhận với chủ #100 rằng hai test này đã được ai đó nhận.

⚠ **Lưu ý về sức khoẻ nhánh đích**: `origin/develop` (622dd2d9) hiện **không compile nổi test** —
`DoiTruChungTuServiceTest.java:163,758` gọi `new KhoanNo(...)` 18 tham số trong khi record cần 19.
PR này **sửa đúng file đó** và đưa cổng từ "không build được" lên "3.945 test, 2 đỏ". Đó là cải
thiện thật, và cũng là lý do không có baseline để so từng lỗi.

## 6. Điểm làm tốt (ghi để không bị sửa nhầm)

- Chuỗi `tra → sắp → KHOÁ (`PESSIMISTIC_WRITE`, sắp theo id) → đọc lại số dư → trải → ghi` gói trọn
  trong `SoCongNoService.ghiNhanDoiTruTheoChungTuGoc` — đúng cách chống hai transaction cùng đọc
  thấy còn nợ; `kiemTraCungLoaiTien` chặn ca trừ 100 USD vào khoản nợ 100 VND mà phép kiểm vượt số
  dư không bắt được.
- Phần vượt số dư **trả về** thay vì ném/tự ghi khoản chờ: §5.4/§5.5 muốn CHỜ, §5.8/§5.9 muốn CHẶN
  — để module chủ tự chọn một trong hai là đoán hộ producer. Quyết định này đúng và có lập luận.
- `V1099` vá đúng bảng thứ 24 mà danh sách viết tay của `V1097` bỏ sót, giữ nguyên khuôn (cột
  nullable → backfill có tắt trigger audit → trigger chép header dùng lại hàm chung).
- `TraCuuTaiKhoanThueNguonRepository` tra TK thuế theo **cột danh mục** của chứng từ nguồn thay vì so
  `so_tai_khoan` với `"1331"` — đúng §3 "không viết cứng số hiệu".
- Ba javadoc "khoảng trống ĐƯỢC BIẾT" (vế ngược phiếu kho, thứ tự tiền hàng/thuế của
  `ORDER_TRA_GOC`, cầu tạm mua hàng) được ghi ra thay vì tự quyết — đúng luật 9.

## 7. Kết luận

**REQUEST CHANGES.**

- Chặn: **M1** (mất dòng sổ công nợ ở luồng "Lưu và ghi sổ" của phiếu nhập/xuất kho) là lỗi số liệu
  im lặng, cùng lớp với lỗi mà commit cuối của PR vừa vá cho thu-chi.
- Chặn: cổng `unitTest` đỏ trên head. Không quy cho tác giả PR về mặt nguyên nhân, nhưng phải xanh
  trước merge.
- Cần xử lý trước merge: **m7** (đụng `V1099` với `origin/feature/thuchimodulemua` — chốt ai đổi số).
- Cần xử lý trong PR hoặc ticket theo sau, có ghi rõ: **M2**, **M3**, **M4**, **m5**, **m6**, n8–n10.

Không APPROVE được ở lượt này kể cả khi các mục trên được vá, cho tới khi bộ test tích hợp
(`*IntegrationTest` · `*VongDoiIT`) chạy được — đó mới là chỗ chứng minh các luật §5.x mà PR này
cài, và lượt review này **không chạy được chúng** (cần Docker).

---
*Chỉ đọc. Không sửa code, không comment GitHub, không commit. Worktree tạm
`.review-pr120` / `.review-pr120-base` và ref tạm `refs/tmp/pr120-review` do lượt này tạo — đã dọn.*
