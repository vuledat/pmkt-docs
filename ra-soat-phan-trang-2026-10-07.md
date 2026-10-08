# Rà soát danh sách chưa phân trang — 2026-10-07

Phạm vi: `cell-app` (trừ `master_data/**`), 10 service BE khác, `client/src` (trừ `legacy/**`), `client-admin/src`.
Chuẩn đối chiếu: **BR1** (phân trang server, mặc định 20, cỡ 10/20/50/100, hiện tổng), **BR40** (cây phân trang theo cấp gốc).
Chỉ đọc code, chưa sửa gì.

Mức: **Cao** = dữ liệu tăng theo tenant, không giới hạn / bị cắt im lặng · **TB** = tải hết vào RAM rồi cắt, hoặc trần size lớn · **Thấp** = có giới hạn tự nhiên nhưng không có trần.
Cột "Phía": BE / FE / BE+FE (phải sửa cả hai đầu).

Đường dẫn BE rút gọn: `cell/…` = `cell-app/src/main/java/vn/vtt/pmkt/cell/…`.

---

## A. Tầng dùng chung FE — sửa 1 chỗ, nhiều màn hưởng

| ID | Mức | Thành phần | Vị trí | Hiện trạng | Phạm vi ảnh hưởng |
|---|---|---|---|---|---|
| A1 | Cao | `CommonComboGrid` | `client/src/base/components/picker/CommonComboGrid.tsx:112,442-450,793-809` | Chỉ có phân trang client trên `rows` nạp sẵn; không có chế độ trang server | 61 file feature (chỉ 10 có `onSearch`, 2 có `onLoadMore`) |
| A2 | TB | Helper "tải hết danh mục, lặp trang 200" chép ~15 nơi | `banHang/{chungTuBanHang,hoaDonBanHang,traLaiHangBan,dieuChinhGiaHangBan}/api/lookups.ts`, `muaHang/_shared/api/purchaseLookupsApi.ts:72`, `kho/_shared/api/danhMucApi.ts:75` (`napHet`), `nganQuy/_shared/api/lookupsApi.ts:72`, `tongHop/phieuKeToanTongHop/api/lookups.ts:87`, `taiSanCoDinh/{ghiTangTSCD,dieuChuyenTSCD}/api/*`, `giaThanh/ketChuyenChiPhi/api/lookups.ts:69`, `soDuBanDau/{khachHang,nhaCungCap}/api/lookups.ts`, `chiPhiTraTruoc/khaiBao/api/danhMucPhanBo.ts:48`, `danhMuc/**/lookups.ts` | Kéo hết `doi-tuong`, `vat-tu`, `nhan-vien`, `kho`, `co-cau-to-chuc`… vào RAM, lọc client | Mọi form chứng từ bán/mua/kho/ngân quỹ/KTTH/TSCĐ. Mẫu đúng đã có: `danhMucComboGrid/useNguonDanhMucTrang`, `traLaiHangMua/useDanhMucTheoTrang` |
| A3 | TB | Mặc định 10/trang (BR1 = 20) | `CommonListTable.tsx:962`, `catalog/useCatalog.ts:150`, `list/useServerListState.ts:57`, `CommonPagination.tsx:45` | Màn quên truyền `pageSize` là ra 10 | 19 file `CommonListTable` không truyền `pageSize`; 4 catalog đang để 10 (`doiTuong/_shared`, `nhanVien`, `doiTuongTapHopChiPhi`, `butToanKetChuyen`); `nhapKhoThanhPham` cố định 10 |
| A4 | TB | `createSearchApi.listAll` dùng sai làm nguồn lookup | `platform/search/createSearchApi.ts:118`; dùng sai ở `taiSanCoDinh/ghiGiamTSCD/api/masterDataLookup.ts:182`, `dieuChinhTSCD/api/masterDataLookup.ts:392`, `_shared/api/useSoChungTuGoiY.ts:77` | Helper dành cho xuất Excel (lặp tới 100k dòng) | 3 chỗ |
| A5 | TB | `ReferencePickerModal` | `base/components/modal/ReferencePickerModal.tsx:137,268` | `rows` nạp sẵn, phân trang client | `taiSanCoDinh/ghiGiamTSCD/components/ThamChieuTab.tsx` |
| A6 | TB | `chungTuNguon.SourceSearch` / `makeSourceSearch` | `base/domainKit/chungTuNguon/types.ts:37`, `quickSearch.ts:62-85` | Hợp đồng chỉ trả mảng, cắt `slice(0,20)` client, không zod | `banHang/dieuChinhGiaHangBan` |
| A7 | TB | `useLookupAllRows` (tham số báo cáo dạng cây) | `base/domainKit/report/useReportLookup.ts:341-363` | Lặp hết trang 200 để dựng cây tài khoản | Mọi báo cáo có tham số cây — lệch BR40, cần BA chốt |
| A8 | TB | Admin `CommonListTable` nhánh server | `client-admin/src/base/components/table/CommonListTable.tsx:1671-1675` | Không gắn `showTotal`/ô nhảy trang → **cả 6 lưới admin không hiện tổng bản ghi** | 6 màn admin |
| A9 | Thấp | `dinhKem.docDinhKem` | `base/domainKit/dinhKem/api/dinhKemApi.ts:23-28` | Chỉ đọc trang 1, 100 tệp | ~66 file dùng tab Đính kèm |

## B. Popup chọn chứng từ / chọn nguồn

| ID | Mức | Phía | Popup | BE | FE | Hiện trạng |
|---|---|---|---|---|---|---|
| B1 | Cao | BE+FE | Tham chiếu — Chọn chứng từ (dùng chung, ~41 màn) | POST `/api/chung-tu/tham-chieu/ung-vien` — `cell/tham_chieu_chung_tu/internal/controller/ThamChieuChungTuController.java:75` | `base/domainKit/thamChieu/components/ChonChungTuPanel.tsx:329-400` | BE top-500/nguồn, `gioiHan` không `@Max`; FE phân trang client 10; dòng 501+ **mất im lặng** |
| B2 | Cao | BE+FE | Đối trừ công nợ phải thu/phải trả | GET `…/doi-tru-chung-tu/lookups` (cả bảng KH/NCC + TK) — `cell/ke_toan_tong_hop/doi_tru_cong_no/internal/controller/DoiTruPhaiThuController.java:119`, `DoiTruPhaiTraController.java:120`; POST `…/chung-tu-kha-dung` (:125/:126) | `base/domainKit/doiTruCongNo/components/DoiTruModal.tsx:308,860`, `DoiTruOffsetTable.tsx:95-145` | Lookup trả hết đối tượng; lưới chứng từ phân trang client, mặc định 10, cỡ [10,20,50]. Tổng BR03 tính trên mọi dòng → BE phải trả kèm summary |
| B3 | Cao | FE | Chọn hóa đơn điều chỉnh (Trả lại hàng bán) | `/hoa-don-ban-hang/tim-kiem` (đã phân trang) | `banHang/traLaiHangBan/api/traLaiHangBanApi.ts:260-274` | **Không gửi page → chỉ nhận 20 dòng đầu**, phần còn lại mất |
| B4 | Cao | FE | Chọn hóa đơn gốc (Hóa đơn bán hàng) | như trên | `banHang/hoaDonBanHang/components/ChonHoaDonGocModal.tsx:167-178` | Như B3, cắt ở 20 |
| B5 | Cao | FE | Chọn hóa đơn gốc (Điều chỉnh giá bán) | như trên | `banHang/dieuChinhGiaHangBan/api/hoaDonGocApi.ts:41,132` | pageSize 100 cố định, phân trang client |
| B6 | Cao | BE+FE | Chọn nguồn — Trả lại hàng bán & Điều chỉnh giá bán | POST `/api/ban-hang/{tra-lai-hang-ban,dieu-chinh-gia-hang-ban}/nguon/tim-kiem` + `/nguon/chung-tu` — `TraLaiHangBanController.java:155,162`, `DieuChinhGiaHangBanController.java:164,172` | `traLaiHangBan/api/nguonApi.ts:189`, `dieuChinhGiaHangBan/api/nguonApi.ts:202` | BE top-N (200, max 500) không trang/tổng; combo "chọn chứng từ" gom từ tập đã cắt nên có thể sót |
| B7 | Cao | BE+FE | Chọn chứng từ chi phí (Mua hàng) | GET `/api/mua-hang/chung-tu-mua-hang/nguon-chi-phi` — `cell/chung_tu_mua_hang/internal/controller/ChungTuMuaHangController.java:359` → repo `ChungTuMuaHangRepositoryImpl.java:755` (không LIMIT) | `chungTuMuaHang/components/modal/CostSourcePickerModal.tsx:161` (`pagination={false}`) | Mọi bộ lọc tuỳ chọn → có thể trả toàn bộ chứng từ |
| B8 | Cao | BE+FE | Chọn chứng từ nguồn (Hóa đơn mua) | POST `/api/mua-hang/hoa-don-mua/nguon/tim-kiem` — `HoaDonMuaController.java:160`, SQL `limit 200` `HoaDonMuaService.java:591` | `hoaDonMua/components/modal/HoaDonMuaVoucherPickerModal.tsx:89-238` | Top 200, FE vẽ hết, không phân trang |
| B9 | Cao | FE | Chọn nguồn điều chỉnh giá mua | (list mua hàng, đã phân trang) | `dieuChinhGiaHangMua/components/modal/ChonNguonDieuChinhGiaModal.tsx:147`, `DieuChinhGiaModal.tsx:1232` | `fetchAllMuaHang` lặp hết, lọc NCC/trạng thái client; ô tìm **lặp hết mỗi lần gõ phím** |
| B10 | Cao | BE | Đối tượng phân bổ (Mua dịch vụ) | GET `/api/mua-hang/chung-tu-mua-dich-vu/{id}/doi-tuong-phan-bo` — `ChungTuMuaDichVuController.java:253` → `PhanBoChiPhiDichVuRepository.java:86` | — | Trả mọi dòng hàng của mọi chứng từ mua trong tenant; `{id}` chỉ dùng trong `NOT EXISTS` |
| B11 | Cao | BE+FE | Chọn chứng từ gốc (Chi phí trả trước) | POST `/api/chi-phi-tra-truoc/khai-bao/chung-tu-goc/ung-vien` — `KhaiBaoCpttController.java:210` (trần 500/port) | `chiPhiTraTruoc/khaiBao/components/modal/ChonChungTuGocModal.tsx:343` | Không trang, FE client 10 |
| B12 | Cao | BE | Chọn nguồn hình thành (Ghi tăng TSCĐ) | GET `/api/tai-san-co-dinh/ghi-tang-tscd/nguon-hinh-thanh-kha-dung` — `TaiSanCoDinhController.java:316` → `PhieuChiNguonApiImpl.java:55`, `ChungTuMuaHangNguonAdapter:524`, `PhieuKeToanTongHopNguonApiImpl:52` | — | `tuNgay/denNgay` không bắt buộc, không LIMIT; còn nạp **toàn bộ id đã dùng** vào `Set` (`NguonDaDungRepository.java:20-27`) |
| B13 | Cao | BE+FE | Xem hóa đơn giảm thuế mua vào / bán ra (Tờ khai GTGT) | POST `/api/thue/to-khai-gtgt/phu-luc/giam-thue/{mua-vao,ban-ra}/hoa-don-xem` — `ToKhai01GtgtController.java:206,214` | `thue/toKhai01Gtgt/components/modal/XemHoaDonGiamThue{MuaVao,BanRa}Modal.tsx` | BE nạp mọi dòng hóa đơn kỳ rồi lọc 8% bằng vòng for; FE client 20, không chọn cỡ trang |
| B14 | TB | BE | Chọn hóa đơn mua vào / bán ra / không tính thuế | POST `…/to-khai-gtgt/{mua-vao,ban-ra}/hoa-don`, `…/ban-ra/hoa-don-khong-tinh-thue` — `ToKhai01GtgtController.java:108,129,150` | (FE đã server) | Tải hết rồi `subList`; 2 request bán ra **thiếu `@Max` pageSize**; `hoaDonDaChon` trả hết |
| B15 | Cao | BE+FE | Phân loại nghiệp vụ / hoạt động (Lập BCTC) | POST `/api/lap-bao-cao-tai-chinh/phan-loai/mau/{maMau}/{nghiep-vu,hoat-dong}` — `PhanLoaiController.java:51,58` → `ChungTuPhanLoaiQuery.java:47-93` | `lapBaoCaoTaiChinh/baoCao/components/modal/PhanLoaiModal.tsx:266` | Mọi dòng sổ cái trong kỳ, không LIMIT (kỳ năm có thể hàng chục nghìn) |
| B16 | Cao | BE+FE | Số dư hoạt động bước 1 (Lập BCTC) | POST `…/so-du/buoc-1` — `PhanLoaiController.java:75` | `baoCao/components/modal/SoDuHoatDongModal.tsx:533` | Mỗi cặp (TK, đối tượng) một dòng, không LIMIT. Bước 2 (:82) — Thấp |
| B17 | Cao | BE+FE | Chọn chứng từ xuất bán (Phiếu xuất kho) | GET `/api/kho/nguon-xuat-ban` — `NguonXuatBanController.java:54` → `ChiTietChungTuBanHangRepository.java:81` | `kho/_shared/api/danhMucApi.ts:506` | Nạp mọi dòng chứng từ bán rồi lọc Java |
| B18 | Cao | BE | Nguồn phiếu xuất theo vật tư | GET `/api/kho/nguon-phieu-xuat?vatTuId` — `NguonPhieuXuatController.java:44` → `NguonPhieuXuatRepository.java:60` | — | Mọi dòng xuất của 1 vật tư toàn thời gian |
| B19 | TB | BE+FE | Nguồn nhập trả lại / ứng viên phiếu xuất điều chuyển / Drawer chọn nguồn nhập | GET `/api/kho/nguon-nhap-tra-lai` (`ofList`), GET `/api/kho/phieu-nhap-dieu-chuyen/ung-vien-phieu-xuat` (RAM cắt 200) | `kho/phieuNhapKho/components/modal/ChonNguonNhapDrawer.tsx:175` (lọc cột → `napHet` 500) | Phân trang giả |
| B20 | TB | BE | Chứng từ chờ xử lý (Khoá sổ) | POST `/api/he-thong/khoa-so/chung-tu-cho-xu-ly/search` — `ChungTuChoXuLyController.java:61` | — | Không có page, tới 5000 dòng/lượt, `PageInfo` giả |
| B21 | TB | BE | Lọc giá trị cột (mọi lưới chứng từ) | POST `<chứng từ>/gia-tri-cot` — `accounting_core/chung_tu/controller/BaseChungTuController.java:99` | — | DISTINCT tối đa 1000, không trang. report-service `/gia-tri-cot` cũng tải 50k rồi cắt RAM |

## C. Picker / combogrid danh mục — BE trả cả bảng

| ID | Mức | Phía | Picker | BE | FE |
|---|---|---|---|---|---|
| C1 | Cao | BE+FE | Mã TSCĐ (Điều chuyển TSCĐ) | GET `/api/tai-san-co-dinh/dieu-chuyen-tscd/tai-san` — `DieuChuyenTaiSanController.java:121` → repo `:149-159` | `dieuChuyenTSCD/api/taiSanLookup.ts:75,102` |
| C2 | Cao | BE+FE | TSCĐ đủ điều kiện (Khai báo sản lượng) — **kèm N+1** (2 query/tài sản, `KhaiBaoSanLuongCrudService.java:240-247`) | GET `…/khai-bao-san-luong/tai-san-du-dieu-kien` — `KhaiBaoSanLuongController.java:95` | `khaiBaoSanLuong/components/modal/KhaiBaoSanLuongThemMoiModal.tsx:213` |
| C3 | Cao | BE+FE | Vật tư (Tính giá xuất kho) | GET `/api/kho/tinh-gia-xuat-kho/vat-tu` — `TinhGiaXuatKhoController.java:35` → repo `:46-66` | `kho/tinhGiaXuatKho/components/VatTuPickerModal.tsx:140` |
| C4 | Cao | BE | Tồn kho toàn tenant | GET `/api/kho/ton-kho` — `TonKhoController.java:44` → `TonKhoRepository.java:117` (quét toàn `acc_so_kho`) | `kho/_shared/api/tonKhoApi.ts:63`, `useNguonNhapCuonLuot.ts:90` |
| C5 | Cao | BE | Cặp đối tượng THCP – vật tư | GET `/api/kho/phieu-nhap-kho/doi-tuong-thcp-vat-tu` — `PhieuNhapKhoController.java:154` | — |
| C6 | Cao | BE | 5 danh mục phân bổ CCDC (TK, đơn vị, công trình, KMCP, ĐT THCP) — nhúng cả vào `/tinh-thu`, `/{id}/tinh-lai` | GET `/api/cong-cu-dung-cu/phan-bo-ccdc/danh-muc` — `PhanBoCcdcController.java:447` | — |
| C7 | Cao | FE | Người dùng (popup phân quyền vai trò) | (`/nguoi-dung` đã phân trang) | `phanQuyen/quanLy/phanQuyen/api/phanQuyenApi.ts:61`, `RolePermissionModal.tsx:170` — tải song song mọi trang |
| C8 | TB | BE | Hệ thống tài khoản trả mảng trần (CPTT khai báo/phân bổ, giá thành, master-data `/tai-khoan`) | `KhaiBaoCpttController.java:189`, `PhanBoCpttController.java:141`, `CauHinhGiaThanhTaiKhoanController.java:40` | `useNguonDanhMucCaBang` + ~11 nơi — FE đã chấp nhận mẫu này; dữ liệu vài trăm dòng |
| C9 | TB | FE | Chọn TSCĐ (Ngừng KH: 200 trang 1), lookup Tính KH (`pageSize: 1000`, BE trần 200 → **bị cắt**), `DoiTuongPicker` (1 trang 200), số dư NV/TK NH/Excel vật tư (trần 200/200/500), combo chứng từ tham chiếu KTTH (200 trang 1) | — | `ngungKhauHaoTSCD/api/ngungKhauHaoTscdApi.ts:79`, `tinhKhauHaoTSCD/api/catalogLookup.ts:73`, `danhMuc/doiTuong/_shared/pickers/DoiTuongPicker.tsx:89`, `soDuBanDau/{nhanVien,taiKhoanNganHang}/api/*`, `tongHop/phieuKeToanTongHop/api/lookups.ts:657` |
| C10 | TB | BE | Map tên đơn vị trong DS người dùng / chi tiết vai trò | `platform_iam/nguoi_dung/internal/…/NguoiDungTxOps.java:702`, `VaiTroServiceImpl.java:374` — `PageRequest.of(0, 1000)` | — (tenant >1000 đơn vị mất tên im lặng) |
| C11 | Thấp | BE | Đơn vị (Điều chuyển CCDC) — `LIMIT NULL` | `DieuChuyenCcdcController.java:233` → `DieuChuyenCcdcChonQuery.java:263,365` | — |

## D. Lưới màn chính

| ID | Mức | Phía | Màn | BE | FE | Hiện trạng |
|---|---|---|---|---|---|---|
| D1 | Cao | BE+FE | Hạch toán chi phí (5 hạng mục + chi phí khác) | POST `/api/cst-gia-thanh/{pp}/hach-toan-chi-phi/{hangMuc}/search`, `/chi-phi-khac/search` — `HachToanChiPhiBaseController.java:52,63` | `giaThanh/hachToanChiPhi/components/HachToanChiPhiListTable.tsx:51` | Tên "search" nhưng request chỉ có `kyId`; nạp mọi dòng sổ cái của kỳ |
| D2 | Cao | BE | Xem chứng từ (Phân bổ chi phí giá thành) | GET `…/phan-bo-chi-phi/{id}/xem-chung-tu` — `PhanBoChiPhiBaseController.java:110` | — | Không LIMIT |
| D3 | Cao | BE | Webhook log | GET `/api/integration-ops/webhook-log` — `cell/integration_ops/webhook_log/internal/controller/WebhookLogController.java:43` | — | `repository.findAll()`, không bọc `ApiResponse` |
| D4 | TB | BE+FE | Phân bổ chi phí — danh sách theo kỳ / Nhập kho thành phẩm chi tiết & phiếu bị loại | `NhapKhoThanhPhamBaseController.java:53,68` (RAM) | `giaThanh/phanBoChiPhi/hooks/usePhanBoChiPhiData.ts:58` | Tải hết rồi cắt |
| D5 | TB | BE | Số dư ban đầu — tài khoản | POST `/api/so-du-ban-dau/tai-khoan/search` — `SoDuBanDauTaiKhoanController.java:89` | — | Dựng cây toàn bộ rồi `subList` (bị chặn bởi hệ thống TK) |
| D6 | TB | FE | Bù trừ công nợ — lưới chứng từ | POST `/api/tong-hop/bu-tru-cong-no/lay-du-lieu` | `tongHop/buTruCongNo/components/ChungTuBuTruTable.tsx:160` | Phân trang client; tổng BR31 trên toàn bộ |
| D7 | (ghi chú) | FE | 8 danh mục cây trong `features/danhMuc` (nhóm KH/NCC, HTTK, cơ cấu tổ chức, công trình, loại TSCĐ, loại CCDC, loại công trình, KMCP) | — | `danhMuc/**/api.ts` | Tải hết / `pageSize: 1000`; riêng `nhomKhNcc/api.ts:53` không gửi page. **Nhưng `features/danhMuc` là nhánh chết** (client/CLAUDE.md: `/danh-muc/*` do legacy phục vụ) → màn đang chạy thật nằm ở vùng đóng băng, chưa quét |
| D8 | Thấp | BE | Giá thành theo kỳ: `tinh-gia-thanh/danh-sach`, `ky-tinh-gia-thanh/{id}/chi-tiet-gia-thanh`, `cau-hinh-he-so-ty-le`, `ket-chuyen-chi-phi/xem-truoc`, `do-dang-cuoi-ky/san-pham-theo-doi-tuong` | `TinhGiaThanhBaseController.java:40`, `KyTinhGiaThanhBaseController.java:86`, `CauHinhHeSoTyLeController.java:51`, `KetChuyenChiPhiBaseController.java:69`, `DoDangCuoiKyBaseController.java:165` | — | Giới hạn theo kỳ, tăng theo số thành phẩm × ĐT THCP |

## E. Xem dữ liệu ghi sổ / dòng của 1 chứng từ — phân trang giả (`PageResponse.ofList`)

| ID | Mức | Endpoint | Ghi chú |
|---|---|---|---|
| E1 | TB | GET `/api/tai-san-co-dinh/khau-hao-tscd/{id}/xem-du-lieu-ghi-so` — `KhauHaoTaiSanController.java:254` | 1 chứng từ khấu hao = bút toán mọi tài sản trong kỳ → có thể hàng nghìn dòng |
| E2 | Thấp | `ghi-giam-tscd/{id}/xem-du-lieu-ghi-so` (:251), `dieu-chinh-tscd/{id}/xem-du-lieu-ghi-so` (:229), `tien-mat|tien-gui/chung-tu/{id}/{dong-chi-tiet,thong-tin-hach-toan}` (4 endpoint) | Giới hạn bởi 1 chứng từ |
| E3 | Thấp | FE `base/domainKit/xemDuLieuGhiSo` — `duyetHetTrang` lặp trang 200, client 50, cỡ [50,100,200] | Lệch BR1 nhưng có ghi chú theo SCR 6 epic → cần BA chốt |
| E4 | Thấp | POST `/api/tai-san-co-dinh/khau-hao-tscd/tinh-truoc` — lưới xem trước gồm mọi TSCĐ cần KH | Chi tiết 1 chứng từ đang lập |

## F. Service khác & client-admin

| ID | Mức | Phía | Endpoint | Vị trí | Hiện trạng |
|---|---|---|---|---|---|
| F1 | Cao | BE+FE | Danh sách công ty cho ô chọn: GET `/api/admin/log-tac-dong/cong-ty`, `/api/admin/cau-hinh/danh-muc`, `/api/admin/thiet-lap/danh-muc` | `super-admin-service/…/LogTacDongController.java:118`, `CauHinhController.java:97`, `ThietLapChungController.java:61` → `TenantRepository.java:25`; FE `client-admin/…/BoLocLogPanel.tsx:76`, `cauHinhApi.ts:33`, `thietLapApi.ts:48` | Trả mọi tenant ACTIVE. Ngoài ra 3 hàm search (cấu hình, log, blacklist) cũng nạp hết tenant mỗi lần chỉ để gắn tên |
| F2 | Cao | BE | GET `/api/control-plane/tenants` | `tenant-provisioning/…/provisioning/internal/controller/TenantController.java:43` | `findAll()`; internal-token, hiện chưa có caller trong main |
| F3 | TB | BE | POST `/api/admin/user-super-admin/tim-kiem` | `UserSuperAdminController.java:63` → `KeycloakAdminRealmClient.java:84` | Nạp tới 2000 user Keycloak rồi phân trang RAM |
| F4 | TB | BE | POST `/api/reports/{reportId}/run` | `report-service/…/ReportController.java:95` → `ReportRunService.java:1133` + ~10 report definition `subList` | Nhóm phía engine nạp tới 50.000 dòng rồi cắt RAM |
| F5 | TB | BE+FE | GET `/api/admin/mau-in/{ma}/lich-su` / report-service `/api/bieu-mau/{id}/phien-ban` | `MauInMacDinhController.java:90`, `BieuMauController.java:119`; FE `LichSuMauInModal.tsx:148` | Lịch sử phiên bản không trang |
| F6 | Thấp | BE | GET `/api/v1/audit-events/entities/{table}/{id}/history` | `audit-logs-service/…/AuditQueryController.java:119` | Cắt 200 im lặng. **Kèm: `/export` dùng chung hàm nên chỉ xuất được 200 dòng** (nhiều khả năng là bug) |
| F7 | Thấp | FE | Admin: `timCongTy` (1 trang 100), cỡ trang cấu hình/blacklist thiếu 10 | `client-admin/…/quanLyUser/api/userApi.ts:86`, `cauHinh/constants/constants.ts:25`, `thietLapChung/constants/constants.ts:35` | |

## G. Thấp — gom chung (có giới hạn tự nhiên)

- Thuế địa bàn: `xa-phuong` (cả nước khi không lọc tỉnh), `chi-cuc-thue`, `co-quan-thue` — `DanhMucDiaBanThueController.java:52,59,66`
- RBAC console nội bộ: `/internal/rbac/danh-muc/{tai-khoan,don-vi}`, `/internal/rbac/mau`, `/mau/{id}/xem-truoc` — `RbacConsoleController.java:159,171`, `MauVaiTroController.java:55,105`
- Tổ chức nhóm: `/api/iam/to-chuc-nhom/{cong-ty-thanh-vien,cay,chi-nhanh}` — `ToChucNhomController.java:41,47,59`
- Lỗi lượt tính giá xuất kho: `/api/kho/tinh-gia-xuat-kho/luot-tinh/{id}/loi` — `TinhGiaXuatKhoController.java:59`
- Khoá sổ loại chứng từ lookup (RAM, danh mục nhỏ) — `KhoaSoLookupController.java:35`
- Kho `danh-muc-nguon`: hợp đồng `*LookupPort.danhSachChon()` không có tham số trang (hiện chưa có bean) — `DanhMucNguonKhoController.java:42`
- `so_cong_no`: `SoCongNoService.khoanChoConLai :158` / `khoanNoConLai :184` nạp toàn bộ phát sinh lịch sử của (TK, đối tượng, loại tiền) — nuôi đối trừ/bù trừ
- `tongHop/buTruCongNo/api/danhMucApi.ts:162` lọc vai trò **sau khi** đã phân trang → trang có thể ít hơn 20 hoặc rỗng
- Mock chưa có BE: Kiểm kê TSCĐ, Khai báo CPTT, Cấu hình hệ số tỷ lệ

---

## Ngoài phạm vi phân trang — thấy khi quét (nên biết)

1. **`BieuMauProxyController` đang tắt `@PreAuthorize`** từ 2026-09-09 ("tạm để test") → proxy `/api/bieu-mau/**` (GET/POST/PUT/DELETE) không kiểm quyền. File: `cell/bieu_mau_proxy/**/BieuMauProxyController.java` (đã xác minh).
2. `super-admin-service` gọi `POST /internal/identity/users/search` nhưng **endpoint này không có trong `identity/src/main/java`** (đã grep, không thấy) → màn Quản lý user admin có thể đang hỏng.
3. `PhanBoChiPhiCrudService.java:167-179`: GET `/danh-sach` lại ghi DB (`timHoacTaoDong`, `capNhatTongChiPhi`).
4. Audit log `/export` chỉ xuất được tối đa 200 dòng (F6).
