# `pur_` — Mua hàng

> Sinh tự động từ [`ldm-MuaHang-Update.puml`](../../../pmkt-docs/ba/Common/LDM_update/ldm-MuaHang-Update.puml) — **không sửa tay**, sửa LDM rồi sinh lại.
> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).
> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.

**8 bảng.**

## Phân hệ này phục vụ nghiệp vụ gì

> Nhóm chức năng thuộc luồng: PMKT-E-00485 Chứng từ mua hàng, PMKT-E-00519 Chứng từ mua dịch vụ, PMKT-E-00542 Hóa đơn mua hàng. File chứa chứng từ ghi nhận việc mua vào, hóa đơn đầu vào, và phân bổ chi phí mua hàng vào giá trị hàng nhập kho. Chưa thuộc phạm vi file: PMKT-E-06758 Chứng từ trả lại hàng mua và PMKT-E-06768 Chứng từ điều chỉnh giá hàng mua — dựng lại khi hai nhóm chức năng này vào

**Epic nguồn:** PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768

| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |
|---|---|---|---|---|---|
| 1 | `ChungTuMuaHang` | `pur_chung_tu_mua_hang` | `pur_chung_tu_mua_hang` | A — có code | Đầu chứng từ — Chứng từ ghi nợ nhà cung cấp. Bốn giá trị LoaiNghiepVu ứng với bốn nghiệp vụ: mua hàng nhập kho, mua hàng không qua kho, mua… |
| 2 | `ChiTietChungTuMuaHang` | `pur_chung_tu_mua_hang_chi_tiet` | `pur_chi_tiet_chung_tu_mua_hang` | A — có code | Dòng chi tiết của `pur_chung_tu_mua_hang` — vào cùng hai thuộc tính VatTuId và TenVatTu. Dòng ghi chú là dòng thêm qua nút Thêm ghi chú: chỉ nhập TenVatTu, mọi cột nghiệp… |
| 3 | `HoaDonMua` | `pur_hoa_don_mua` | `pur_hoa_don_mua` | B — có schema, chưa code | Đầu chứng từ — Một entity cho cả hóa đơn lập kèm chứng từ và hóa đơn nhận về sau. Không khai bộ thuộc tính đầu chứng từ: số và ngày là của… |
| 4 | `ChungTuNhanHoaDon` | `pur_chung_tu_nhan_hoa_don` | `pur_chung_tu_nhan_hoa_don` | B — có schema, chưa code | Đầu chứng từ — Chứng từ nhận hóa đơn về sau Mỗi đợt nhận hóa đơn tạo đúng một bản ghi, mang số và ngày chứng từ riêng. Bút toán thuế GTGT… |
| 5 | `ChiTietHoaDon` | `pur_hoa_don_mua_chi_tiet` | `pur_chi_tiet_hoa_don` | B — có schema, chưa code | Dòng chi tiết của `pur_hoa_don_mua` — Dòng chi tiết hóa đơn nhận về sau Dòng hàng đọc từ chứng từ ghi nợ gốc và chỉ đọc; màn chỉ cho cập nhật thông tin thuế. |
| 6 | `ChiPhiMuaHang` | `pur_chi_phi_mua_hang` | `pur_chi_phi_mua_hang` | B — có schema, chưa code | Dòng chi tiết của `pur_chung_tu_mua_hang` — Dòng chi phí chờ phân bổ — chi phí mua hàng và phí hàng về kho Một bản ghi cho một chứng từ chi phí nguồn được đưa vào tab chi… |
| 7 | `ChiPhiNhapKhau` | `pur_chi_phi_nhap_khau` | `pur_chi_phi_nhap_khau` | B — có schema, chưa code | Dòng chi tiết của `pur_chung_tu_mua_hang` — Dòng chi phí chờ phân bổ — phí trước hải quan Tách khỏi ChiPhiMuaHang vì phải theo dõi song song nguyên tệ và quy đổi: phần… |
| 8 | `PhanBoChiPhiMuaHang` | `pur_phan_bo_chi_phi_mua_hang` | `pur_phan_bo_chi_phi_mua_hang` | B — có schema, chưa code | Dòng chi tiết của `pur_chung_tu_mua_hang` — Một bản ghi cho một cặp chứng từ chi phí nguồn và dòng hàng đích. Nhiều nguồn phân bổ cùng lúc thì mỗi nguồn chạy công thức… |

---

## 1. `pur_chung_tu_mua_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuMuaHang` |
| Base class | `BaseChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `pur_chung_tu_mua_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chứng từ ghi nợ nhà cung cấp. Bốn giá trị LoaiNghiepVu ứng với bốn nghiệp vụ: · mua hàng nhập kho, mua hàng không qua kho, mua dịch vụ, mua dịch vụ là chi phí · mua hàng. Hai giá trị đầu thuộc PMKT-E-00485, hai giá trị sau thuộc · PMKT-E-00519; màn danh sách dùng chung. |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng con | `pur_chung_tu_mua_hang_chi_tiet` · `pur_hoa_don_mua` · `pur_chi_phi_mua_hang` · `pur_chi_phi_nhap_khau` · `pur_phan_bo_chi_phi_mua_hang` |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải chứng từ |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | Loại tiền giao dịch (reference ENT_LoaiTien) `FK` |
| 3 | `TyGia` | `ty_gia` | `exchange_rate` | N | `1` | Tỷ giá quy đổi về đồng tiền hạch toán. Bản sao tại thời điểm lập chứng từ, không đổi khi danh mục đổi |
| 4 | `TrangThaiGhiSo` | `trang_thai_ghi_so` | `text` CHECK | N | — | Trạng thái ghi sổ (ChuaGhiSo \| DaGhiSo \| DaHuy) |
| 5 | `LoaiNghiepVu` | `loai_nghiep_vu` | `text` CHECK | N | — | **[Điều khiển nghiệp vụ]** Loại nghiệp vụ (MuaHangNhapKho \| MuaHangKhongQuaKho \| MuaDichVu \| MuaDichVuChiPhi) |
| 6 | `HinhThuc` | `hinh_thuc` | `text` CHECK | N | — | **[Điều khiển nghiệp vụ]** Hình thức mua (TrongNuoc \| NhapKhau) |
| 7 | `TrangThaiHoaDon` | `trang_thai_hoa_don` | `text` CHECK | N | — | **[Điều khiển nghiệp vụ]** Trạng thái hóa đơn tại thời điểm lập chứng từ (DaCoHoaDon \| ChuaCoHoaDon \| KhongCoHoaDon) |
| 8 | `NhieuHoaDon` | `nhieu_hoa_don` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Chế độ nhập nhiều hóa đơn trên một chứng từ |
| 9 | `ThanhToanNgay` | `thanh_toan_ngay` | `boolean` | Y | `false` | **[Điều khiển nghiệp vụ]** Thanh toán ngay cho nhà cung cấp |
| 10 | `HinhThucThanhToan` | `hinh_thuc_thanh_toan` | `text` CHECK | Y | — | **[Điều khiển nghiệp vụ]** Hình thức thanh toán (TienMat \| UyNhiemChi \| SecTienMat \| SecChuyenKhoan) |
| 11 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | N | — | **[Nhà cung cấp]** Nhà cung cấp (reference ENT_DoiTuong). Đối tượng phải có bản ghi DoiTuong_VaiTro với VaiTro = NhaCungCap `FK` |
| 12 | `TenNhaCungCap` | `ten_nha_cung_cap` | `text` | N | — | **[Nhà cung cấp]** Tên nhà cung cấp. Bản sao DoiTuong.Ten tại thời điểm lập chứng từ, cho phép sửa tay |
| 13 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Nhà cung cấp]** Địa chỉ nhà cung cấp. Bản sao DoiTuong.DiaChiDayDu tại thời điểm lập chứng từ |
| 14 | `NhanVienMuaHangId` | `nhan_vien_mua_hang_id` | `uuid` | Y | — | **[Nhà cung cấp]** Nhân viên mua hàng (reference ENT_DoiTuong). Đối tượng phải có bản ghi DoiTuong_VaiTro với VaiTro = NhanVien `FK` |
| 15 | `DieuKhoanThanhToanId` | `dieu_khoan_thanh_toan_id` | `uuid` | Y | — | **[Điều khoản thanh toán: dùng khi ThanhToanNgay = false]** Điều khoản thanh toán (reference ENT_DieuKhoanThanhToan). Tự điền từ DoiTuong_VaiTro.DieuKhoanThanhToanId của vai trò NhaCungCap `FK` |
| 16 | `SoNgayDuocNo` | `so_ngay_duoc_no` | `integer` | Y | `0` | **[Điều khoản thanh toán: dùng khi ThanhToanNgay = false]** Số ngày được nợ. Tự điền theo điều khoản thanh toán, cho phép sửa tay |
| 17 | `HanThanhToan` | `han_thanh_toan` | `date` | Y | — | **[Điều khoản thanh toán: dùng khi ThanhToanNgay = false]** Hạn thanh toán |
| 18 | `LoaiChietKhau` | `loai_chiet_khau` | `text` CHECK | N | — | **[Chiết khấu]** Loại chiết khấu (KhongChietKhau \| TheoMatHang \| TheoPhanTramHoaDon \| TheoSoTienTongHoaDon) |
| 19 | `TyLeChietKhau` | `ty_le_chiet_khau` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu áp cho toàn chứng từ, đơn vị phần trăm, từ 0 đến 100 |
| 20 | `SoTienChietKhau` | `so_tien_chiet_khau` | `money_foreign` ≈ | Y | `0` | **[Chiết khấu]** Số tiền chiết khấu nhập trên popup phân bổ chiết khấu |
| 21 | `PhieuNhapKhoId` | `phieu_nhap_kho_id` | `uuid` | Y | — | **[Chứng từ con sinh kèm]** Phiếu nhập kho sinh kèm (reference ENT_PhieuNhapKho) `FK` |
| 22 | `PhieuChiId` | `phieu_chi_id` | `uuid` | Y | — | **[Chứng từ con sinh kèm]** Phiếu chi, ủy nhiệm chi hoặc séc sinh kèm (reference ENT_PhieuChi) `FK` |
| 23 | `TongTienHangHoa` | `tong_tien_hang_hoa` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền hàng của các dòng hàng hóa, dịch vụ |
| 24 | `TongTienHangHoaQuyDoi` | `tong_tien_hang_hoa_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền hàng quy đổi |
| 25 | `TongTienChietKhau` | `tong_tien_chiet_khau` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền chiết khấu |
| 26 | `TongTienChietKhauQuyDoi` | `tong_tien_chiet_khau_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền chiết khấu quy đổi |
| 27 | `TongTienThueGTGT` | `tong_tien_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền thuế GTGT |
| 28 | `TongTienThueGTGTQuyDoi` | `tong_tien_thue_gtgt_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền thuế GTGT quy đổi |
| 29 | `TongTienThanhToan` | `tong_tien_thanh_toan` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền phải thanh toán cho nhà cung cấp |
| 30 | `TongTienThanhToanQuyDoi` | `tong_tien_thanh_toan_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng tiền thanh toán quy đổi |
| 31 | `ChiPhi` | `chi_phi` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng chi phí mua hàng đã phân bổ vào các dòng hàng |
| 32 | `ChiPhiQuyDoi` | `chi_phi_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng chi phí mua hàng quy đổi |
| 33 | `TongGiaTriNhapKho` | `tong_gia_tri_nhap_kho` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng giá trị nhập kho, là Tổng giá trị khi mua không qua kho |
| 34 | `TongGiaTriNhapKhoQuyDoi` | `tong_gia_tri_nhap_kho_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp: nguyên tệ và quy đổi về đồng tiền hạch toán]** Tổng giá trị nhập kho quy đổi |
| 35 | `SoTienDaThanhToan` | `so_tien_da_thanh_toan` | `money_foreign` ≈ | Y | `0` | **[Thanh toán]** Số tiền đã thanh toán cho chứng từ, theo đồng tiền giao dịch |
| 36 | `SoTienDaThanhToanQuyDoi` | `so_tien_da_thanh_toan_quy_doi` | `money_vnd` | Y | `0` | **[Thanh toán]** Số tiền đã thanh toán quy đổi |
| 37 | `TrangThaiNhanHoaDon` | `trang_thai_nhan_hoa_don` | `text` CHECK | N | — | **[Trạng thái]** Trạng thái nhận hóa đơn (DaNhanDu \| ChuaNhan \| KhongCoHoaDon) |
| 38 | `TrangThaiThanhToan` | `trang_thai_thanh_toan` | `text` CHECK | N | — | **[[Chịu trách nhiệm] Luồng Mua hàng]** Trạng thái thanh toán (DaThanhToan \| ChuaThanhToan \| DaThanhToanMotPhan) |
| 39 | `TinhTrangPhanBo` | `tinh_trang_phan_bo` | `text` CHECK | Y | — | **[[Chịu trách nhiệm] Luồng Tiền và luồng Công nợ]** Tình trạng phân bổ khi chứng từ đóng vai trò nguồn chi phí (ChuaPhanBo \| PhanBoMotPhan \| HoanThanhPhanBo). Trống khi chứng từ không có dòng nào tích Là CPMH |

**Trường base — `BaseChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4 |
| `phien_ban` | `integer` | N | `1` | Khóa lạc quan `@Version`. `AggregateRootEntity` |
| `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4 |
| `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4 |
| `giao_dich_chung_tu_id` | `uuid` | Y | — | Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity` |
| `so_chung_tu` | `varchar(50)` | N | — | Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20 |
| `ngay_chung_tu` | `date` | N | — | Ngày lập chứng từ. `BaseChungTuEntity` |
| `ngay_hach_toan` | `date` | N | — | Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37 |
| `status` | `text` | N | `NHAP` | Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12 |
| `nguoi_duyet_id` | `uuid` | Y | — | Người duyệt. `BaseChungTuEntity` |
| `ngay_duyet` | `timestamptz` | Y | — | Thời điểm duyệt. `BaseChungTuEntity` |
| `nguoi_ghi_so` | `uuid` | Y | — | Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `thoi_gian_ghi_so` | `timestamptz` | Y | — | Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo, gán một lần. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo, gán một lần. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_chung_tu_mua_hang` (70 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 20 | `trang_thai_ghi_so`, `nhieu_hoa_don`, `nhan_vien_mua_hang_id`, `ty_le_chiet_khau`, `so_tien_chiet_khau`, `tong_tien_hang_hoa`, `tong_tien_hang_hoa_quy_doi`, `tong_tien_chiet_khau`, `tong_tien_chiet_khau_quy_doi`, `tong_tien_thue_gtgt`, `tong_tien_thue_gtgt_quy_doi`, `tong_tien_thanh_toan`, `tong_tien_thanh_toan_quy_doi`, `chi_phi`, `chi_phi_quy_doi`, `tong_gia_tri_nhap_kho`, `tong_gia_tri_nhap_kho_quy_doi`, `so_tien_da_thanh_toan`, `so_tien_da_thanh_toan_quy_doi`, `tinh_trang_phan_bo` |
| DB có — LDM **không khai** | 38 | `gia_tri_chiet_khau`, `tong_tien_hang_nt`, `tong_chi_phi_nt`, `tong_thue_gtgt_nt`, `tong_tien_thanh_toan_nt`, `gia_tri_nhap_kho_nt`, `tai_khoan_tien_id`, `muc_dich_thu_chi_id`, `so_chung_tu_phieu_chi`, `so_con_no_vnd`, `so_con_no_nt`, `tong_no_phai_tra_vnd`, `tong_no_phai_tra_nt`, `luy_ke_da_phan_bo`, `trang_thai_phan_bo`, `ma`, `ten`, `trang_thai`, `nguoi_nhan_tien`, `tai_khoan_chi_id`, `ten_ngan_hang_chi`, `tai_khoan_nhan_id`, `ten_ngan_hang_nhan`, `so_cccd`, `ngay_cap`, `noi_cap`, `ly_do_chi`, `so_tai_khoan_nhan`, `ngay_chung_tu_phieu_chi`, `doi_tuong_nhan_tien_id`, `nguoi_giao_hang`, `so_dien_thoai_giao_hang`, `nhan_vien_mua_id`, `tong_tien_hang_vnd`, `tong_chi_phi_vnd`, `tong_thue_gtgt_vnd`, `tong_tien_thanh_toan_vnd`, `gia_tri_nhap_kho_vnd` |

---

## 2. `pur_chung_tu_mua_hang_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietChungTuMuaHang` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | A — có code |
| Bảng hiện có | `pur_chi_tiet_chung_tu_mua_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | vào cùng hai thuộc tính VatTuId và TenVatTu. · Dòng ghi chú là dòng thêm qua nút Thêm ghi chú: chỉ nhập TenVatTu, mọi cột nghiệp · vụ khác để trống, không tham gia tính toán và không sinh bút toán. Các ràng buộc · bắt buộc bên dưới chỉ áp cho dòng hàng. |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_chung_tu_mua_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_chung_tu_mua_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | N | — | Chứng từ mua hàng (reference ENT_ChungTuMuaHang) `FK` |
| 2 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | Dòng hàng khi true, dòng ghi chú khi false |
| 3 | `VatTuId` | `vat_tu_id` | `uuid` | Y | — | **[Hàng hóa, dịch vụ]** Mã hàng, mã dịch vụ (reference ENT_VatTu) `FK` |
| 4 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa, dịch vụ]** Tên hàng. Tự điền theo VatTu.TenMua, trống thì theo VatTu.Ten; là nội dung ghi chú khi LoaiDongHang = false |
| 5 | `LoaiVatTuId` | `loai_vat_tu_id` | `uuid` | Y | — | **[Hàng hóa, dịch vụ]** Tính chất hàng hóa dịch vụ của mã hàng (reference ENT_LoaiVatTu). Điều khiển ẩn hiện cột kho và quyền tích Là CPMH `FK` |
| 6 | `LaCPMH` | `la_cpmh` | `boolean` | Y | `false` | **[Hàng hóa, dịch vụ]** Dòng là chi phí mua hàng, tham gia phân bổ vào giá vốn dòng hàng của chứng từ khác |
| 7 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hàng hóa, dịch vụ]** Diễn giải dòng, ngầm định theo TenVatTu, không hiển thị trên lưới |
| 8 | `KhoId` | `kho_id` | `uuid` | Y | — | **[Kho và tài khoản hạch toán]** Kho nhập (reference ENT_Kho) `FK` |
| 9 | `TaiKhoanNoId` | `tai_khoan_no_id` | `uuid` | Y | — | **[Kho và tài khoản hạch toán]** Tài khoản Nợ (reference ENT_HeThongTaiKhoan). Là tài khoản kho khi mua hàng nhập kho, tài khoản chi phí khi mua không qua kho hoặc mua dịch vụ `FK` |
| 10 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | Y | — | **[dùng tự chọn từ hệ thống tài khoản]** Tài khoản công nợ phải trả (reference ENT_HeThongTaiKhoan) `FK` |
| 11 | `DonViTinhId` | `don_vi_tinh_id` | `uuid` | Y | — | **[Đơn vị tính và quy đổi đơn vị tính]** Đơn vị tính nhập liệu (reference ENT_DonViTinh) `FK` |
| 12 | `DonViTinhChinhId` | `don_vi_tinh_chinh_id` | `uuid` | Y | — | **[Đơn vị tính và quy đổi đơn vị tính]** Đơn vị tính chính của vật tư (reference ENT_DonViTinh) `FK` |
| 13 | `HeSoQuyDoi` | `he_so_quy_doi` | `exchange_rate` ≈ | Y | `0` | **[Đơn vị tính và quy đổi đơn vị tính]** Hệ số quy đổi về đơn vị tính chính |
| 14 | `SoLuongTheoDVC` | `so_luong_theo_dvc` | `quantity` | Y | `0` | **[[Chịu trách nhiệm] Luồng Mua hàng]** Số lượng theo đơn vị tính chính, dùng theo dõi tồn kho và giá vốn |
| 15 | `DonGiaTheoDVC` | `don_gia_theo_dvc` | `money_foreign` ≈ | Y | `0` | **[[Chịu trách nhiệm] Luồng Mua hàng]** Đơn giá theo đơn vị tính chính |
| 16 | `SoLuong` | `so_luong` | `quantity` | Y | `0` | **[Số lượng và giá trị]** Số lượng theo đơn vị tính đã chọn, không âm. Dòng hàng hóa yêu cầu lớn hơn 0, dòng dịch vụ cho phép bằng 0 |
| 17 | `DonGia` | `don_gia` | `money_foreign` ≈ | Y | `0` | **[Số lượng và giá trị]** Đơn giá theo đồng tiền giao dịch, không âm |
| 18 | `ThanhTien` | `thanh_tien` | `money_foreign` ≈ | Y | `0` | **[Số lượng và giá trị]** Thành tiền, bằng SoLuong nhân DonGia. Sửa tay thì tính ngược DonGia khi SoLuong lớn hơn 0 |
| 19 | `ThanhTienQuyDoi` | `thanh_tien_quy_doi` | `money_vnd` | Y | `0` | **[Số lượng và giá trị]** Thành tiền quy đổi, bằng ThanhTien nhân TyGia |
| 20 | `ChietKhauPhanTram` | `chiet_khau_phan_tram` | `percent_rate` | Y | `0` | **[Chiết khấu]** Tỷ lệ chiết khấu của dòng, đơn vị phần trăm, từ 0 đến 100 |
| 21 | `ChietKhau` | `chiet_khau` | `numeric(18,4)` ⚠ | Y | `0` | **[Chiết khấu]** Tiền chiết khấu của dòng, không vượt quá ThanhTien. Tính hai chiều với ChietKhauPhanTram |
| 22 | `ChietKhauQuyDoi` | `chiet_khau_quy_doi` | `money_vnd` | Y | `0` | **[Chiết khấu]** Tiền chiết khấu quy đổi |
| 23 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | **[Thuế GTGT]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC). Tự điền theo VatTu.ThueSuatGTGTMacDinh |
| 24 | `GiaTriThueGTGT` | `gia_tri_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Thuế GTGT]** Giá trị thuế suất GTGT thực tế dùng tính tiền thuế, đơn vị phần trăm |
| 25 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[[Chịu trách nhiệm] Luồng Mua hàng]** Tiền thuế GTGT, bằng ThanhTien trừ ChietKhau rồi nhân GiaTriThueGTGT chia 100 |
| 26 | `TienThueGTGTQuyDoi` | `tien_thue_gtgt_quy_doi` | `money_vnd` | Y | `0` | **[[Chịu trách nhiệm] Luồng Mua hàng]** Tiền thuế GTGT quy đổi |
| 27 | `TaiKhoanThueGTGTId` | `tai_khoan_thue_gtgt_id` | `uuid` | Y | — | **[[Chịu trách nhiệm] Luồng Mua hàng]** Tài khoản thuế GTGT được khấu trừ (reference ENT_HeThongTaiKhoan) `FK` |
| 28 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[[Chịu trách nhiệm] Luồng Mua hàng]** Diễn giải thuế |
| 29 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | **[[Chịu trách nhiệm] Luồng Mua hàng]** Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5) |
| 30 | `TyGiaHaiQuan` | `ty_gia_hai_quan` | `exchange_rate` | Y | `1` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tỷ giá hải quan, dùng quy đổi giá trị tính thuế và các sắc thuế nhập khẩu |
| 31 | `GiaFOB` | `gia_fob` | `numeric(18,4)` ⚠ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Giá mua tại cửa khẩu xuất tính bằng nguyên tệ |
| 32 | `ChiPhiTruocHQNgoaiTe` | `chi_phi_truoc_hq_ngoai_te` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Phí trước hải quan bằng ngoại tệ của dòng, nhận từ phân bổ |
| 33 | `ChiPhiTruocHQHachToan` | `chi_phi_truoc_hq_hach_toan` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Phí trước hải quan bằng đồng tiền hạch toán của dòng, nhận từ phân bổ |
| 34 | `GiaTriTinhThueNK` | `gia_tri_tinh_thue_nk` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Trị giá tính thuế nhập khẩu, bằng GiaFOB cộng ChiPhiTruocHQNgoaiTe nhân TyGiaHaiQuan cộng ChiPhiTruocHQHachToan |
| 35 | `PhanTramThueNK` | `phan_tram_thue_nk` | `percent_rate` | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Thuế suất nhập khẩu theo tờ khai hải quan, đơn vị phần trăm |
| 36 | `TienThueNK` | `tien_thue_nk` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tiền thuế nhập khẩu, bằng GiaTriTinhThueNK nhân PhanTramThueNK chia 100 |
| 37 | `TaiKhoanThueNKId` | `tai_khoan_thue_nk_id` | `uuid` | Y | — | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tài khoản thuế nhập khẩu (reference ENT_HeThongTaiKhoan) `FK` |
| 38 | `PhanTramThueTTDB` | `phan_tram_thue_ttdb` | `percent_rate` | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Thuế suất tiêu thụ đặc biệt, đơn vị phần trăm |
| 39 | `TienThueTTDB` | `tien_thue_ttdb` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tiền thuế tiêu thụ đặc biệt, bằng GiaTriTinhThueNK cộng TienThueNK rồi nhân PhanTramThueTTDB chia 100 |
| 40 | `TaiKhoanThueTTDBNKId` | `tai_khoan_thue_ttdbnk_id` | `uuid` | Y | — | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tài khoản thuế tiêu thụ đặc biệt hàng nhập khẩu (reference ENT_HeThongTaiKhoan) `FK` |
| 41 | `TaiKhoanThueTTDBId` | `tai_khoan_thue_ttdb_id` | `uuid` | Y | — | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tài khoản thuế tiêu thụ đặc biệt phải nộp (reference ENT_HeThongTaiKhoan) `FK` |
| 42 | `PhanTramThueCBPG` | `phan_tram_thue_cbpg` | `percent_rate` | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Thuế suất chống bán phá giá, đơn vị phần trăm |
| 43 | `TienThueCBPG` | `tien_thue_cbpg` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tiền thuế chống bán phá giá, bằng GiaTriTinhThueNK nhân PhanTramThueCBPG chia 100, không cộng tiền thuế nhập khẩu |
| 44 | `TaiKhoanThueCBPGId` | `tai_khoan_thue_cbpg_id` | `uuid` | Y | — | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tài khoản thuế chống bán phá giá (reference ENT_HeThongTaiKhoan) `FK` |
| 45 | `TienThueBVMT` | `tien_thue_bvmt` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tiền thuế bảo vệ môi trường, nhập tay |
| 46 | `TaiKhoanThueBVMTId` | `tai_khoan_thue_bvmt_id` | `uuid` | Y | — | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tài khoản thuế bảo vệ môi trường (reference ENT_HeThongTaiKhoan) `FK` |
| 47 | `TaiKhoanDoiUngThueGTGTId` | `tai_khoan_doi_ung_thue_gtgt_id` | `uuid` | Y | — | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Tài khoản đối ứng thuế GTGT hàng nhập khẩu (reference ENT_HeThongTaiKhoan) `FK` |
| 48 | `ChiPhiTruocHQTinhGiaXK` | `chi_phi_truoc_hq_tinh_gia_xk` | `money_foreign` ≈ | Y | `0` | **[Hàng nhập khẩu: chỉ dùng khi HinhThuc = NhapKhau]** Phí trước hải quan tính vào giá trị nhập kho, xác định theo tỷ giá hạch toán tại thời điểm phân bổ, không đổi khi sửa TyGiaHaiQuan |
| 49 | `ChiPhi` | `chi_phi` | `money_foreign` ≈ | Y | `0` | **[Chi phí nhận từ phân bổ và giá trị nhập kho]** Chi phí mua hàng đã phân bổ vào dòng |
| 50 | `ChiPhiHangVeKho` | `chi_phi_hang_ve_kho` | `money_foreign` ≈ | Y | `0` | **[Chi phí nhận từ phân bổ và giá trị nhập kho]** Phí hàng về kho đã phân bổ vào dòng |
| 51 | `GiaTriNhapKho` | `gia_tri_nhap_kho` | `money_foreign` ≈ | Y | `0` | **[Chi phí nhận từ phân bổ và giá trị nhập kho]** Giá trị nhập kho của dòng, là Tổng giá trị khi mua không qua kho |
| 52 | `DaNhanHoaDon` | `da_nhan_hoa_don` | `boolean` | N | `false` | **[Nhận hóa đơn]** Dòng đã nhận hóa đơn |
| 53 | `HoaDonMuaId` | `hoa_don_mua_id` | `uuid` | Y | — | **[Nhận hóa đơn]** Hóa đơn mua của dòng (reference ENT_HoaDonMua). Dùng cho chứng từ nhiều hóa đơn và luồng nhận hóa đơn về sau `FK` |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_chi_tiet_chung_tu_mua_hang` (73 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 15 | `ten_vat_tu`, `loai_vat_tu_id`, `dien_giai`, `tai_khoan_no_id`, `tai_khoan_co_id`, `don_vi_tinh_chinh_id`, `so_luong_theo_dvc`, `don_gia_theo_dvc`, `chiet_khau_phan_tram`, `chiet_khau`, `chiet_khau_quy_doi`, `gia_tri_thue_gtgt`, `tien_thue_gtgt_quy_doi`, `tai_khoan_thue_ttdbnk_id`, `chi_phi_truoc_hq_tinh_gia_xk` |
| DB có — LDM **không khai** | 25 | `gia_fob_nt`, `gia_tri_tinh_thue_nk_nt`, `tien_thue_nk_nt`, `tien_thue_ttdb_nt`, `tien_thue_cbpg_nt`, `tien_thue_bvmt_nt`, `gia_tri_tinh_thue_gtgt`, `gia_tri_tinh_thue_gtgt_nt`, `thue_suat_gtgt_nk`, `tien_thue_gtgt_nk`, `tien_thue_gtgt_nk_nt`, `chi_phi_ctdv`, `doi_tuong_tap_hop_chi_phi_id`, `tai_khoan_thue_ttdb_nk_id`, `so_lo`, `han_su_dung`, `ma_hang`, `ten_hang`, `loai_vat_tu`, `tai_khoan_kho_id`, `tai_khoan_cong_no_id`, `ty_le_chiet_khau`, `tien_chiet_khau`, `chi_phi_truoc_hq`, `phien_ban` |

---

## 3. `pur_hoa_don_mua`

| Mục | Nội dung |
|---|---|
| Entity LDM | `HoaDonMua` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_hoa_don_mua` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Một entity cho cả hóa đơn lập kèm chứng từ và hóa đơn nhận về sau. Không khai · bộ thuộc tính đầu chứng từ: số và ngày là của hóa đơn nhà cung cấp, đã có ở · SoHoaDon và NgayHoaDon; ngày hạch toán và trạng thái ghi sổ nằm ở chứng từ mang · hóa đơn — ChungTuNhanHoaDon khi LaHDVeSau = true, ChungTuMuaHang khi lập kèm. |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Bảng cha | `pur_chung_tu_mua_hang` — FK `ON DELETE CASCADE` |
| Bảng con | `pur_hoa_don_mua_chi_tiet` |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `LaHDVeSau` | `la_hd_ve_sau` | `boolean` | N | `false` | Hóa đơn nhận về sau khi true, hóa đơn lập kèm chứng từ khi false |
| 2 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | Y | — | **[Chứng từ liên quan]** Chứng từ mua hàng gốc (reference ENT_ChungTuMuaHang). Chỉ có giá trị khi hóa đơn gom đúng một chứng từ `FK` |
| 3 | `ChungTuNhanHoaDonId` | `chung_tu_nhan_hoa_don_id` | `uuid` | Y | — | **[Chứng từ liên quan]** Chứng từ nhận hóa đơn (reference ENT_ChungTuNhanHoaDon). Chỉ có giá trị khi LaHDVeSau = true `FK` |
| 4 | `NhaCungCapId` | `nha_cung_cap_id` | `uuid` | N | — | **[Nhà cung cấp trên hóa đơn, cho phép khác nhà cung cấp của chứng từ ghi nợ]** Nhà cung cấp phát hành hóa đơn (reference ENT_DoiTuong). Đối tượng phải có bản ghi DoiTuong_VaiTro với VaiTro = NhaCungCap `FK` |
| 5 | `TenNhaCungCap` | `ten_nha_cung_cap` | `text` | N | — | **[Nhà cung cấp trên hóa đơn, cho phép khác nhà cung cấp của chứng từ ghi nợ]** Tên nhà cung cấp. Bản sao DoiTuong.Ten |
| 6 | `MaSoThue` | `ma_so_thue` | `varchar(50)` | Y | — | **[Nhà cung cấp trên hóa đơn, cho phép khác nhà cung cấp của chứng từ ghi nợ]** Mã số thuế nhà cung cấp. Bản sao DoiTuong.MaSoThue |
| 7 | `DiaChi` | `dia_chi` | `text` | Y | — | **[Nhà cung cấp trên hóa đơn, cho phép khác nhà cung cấp của chứng từ ghi nợ]** Địa chỉ nhà cung cấp. Bản sao DoiTuong.DiaChiDayDu |
| 8 | `NhanVienMuaHangId` | `nhan_vien_mua_hang_id` | `uuid` | Y | — | **[Nhà cung cấp trên hóa đơn, cho phép khác nhà cung cấp của chứng từ ghi nợ]** Nhân viên mua hàng (reference ENT_DoiTuong). Đối tượng phải có bản ghi DoiTuong_VaiTro với VaiTro = NhanVien `FK` |
| 9 | `SoHoaDon` | `so_hoa_don` | `varchar(50)` | N | — | **[Thông tin hóa đơn]** Số hóa đơn do nhà cung cấp phát hành |
| 10 | `MauSoHoaDonId` | `mau_so_hoa_don_id` | `uuid` | Y | — | **[Thông tin hóa đơn]** Mẫu số hóa đơn (reference ENT_MauSoHoaDon) `FK` |
| 11 | `KyHieuHoaDon` | `ky_hieu_hoa_don` | `text` | Y | — | **[Thông tin hóa đơn]** Ký hiệu hóa đơn |
| 12 | `NgayHoaDon` | `ngay_hoa_don` | `date` | N | — | **[Thông tin hóa đơn]** Ngày phát hành hóa đơn |
| 13 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Thông tin hóa đơn]** Diễn giải hóa đơn |
| 14 | `DieuKhoanThanhToanId` | `dieu_khoan_thanh_toan_id` | `uuid` | Y | — | **[Điều khoản thanh toán: dùng cho hóa đơn nhận về sau]** Điều khoản thanh toán (reference ENT_DieuKhoanThanhToan) `FK` |
| 15 | `SoNgayDuocNo` | `so_ngay_duoc_no` | `integer` | Y | `0` | **[Điều khoản thanh toán: dùng cho hóa đơn nhận về sau]** Số ngày được nợ |
| 16 | `HanThanhToan` | `han_thanh_toan` | `date` | Y | — | **[Điều khoản thanh toán: dùng cho hóa đơn nhận về sau]** Hạn thanh toán |
| 17 | `TongTienTruocThue` | `tong_tien_truoc_thue` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp]** Tổng giá trị hàng hóa dịch vụ chưa thuế, đã trừ chiết khấu |
| 18 | `TongTienTruocThueQuyDoi` | `tong_tien_truoc_thue_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp]** Tổng giá trị chưa thuế quy đổi |
| 19 | `TongTienThueGTGT` | `tong_tien_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp]** Tổng tiền thuế GTGT |
| 20 | `TongTienThueGTGTQuyDoi` | `tong_tien_thue_gtgt_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp]** Tổng tiền thuế GTGT quy đổi |
| 21 | `TongTienSauThue` | `tong_tien_sau_thue` | `money_foreign` ≈ | Y | `0` | **[Tổng hợp]** Tổng tiền sau thuế |
| 22 | `TongTienSauThueQuyDoi` | `tong_tien_sau_thue_quy_doi` | `money_vnd` | Y | `0` | **[Tổng hợp]** Tổng tiền sau thuế quy đổi |

**Trường base — `BaseChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4 |
| `phien_ban` | `integer` | N | `1` | Khóa lạc quan `@Version`. `AggregateRootEntity` |
| `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4 |
| `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4 |
| `giao_dich_chung_tu_id` | `uuid` | Y | — | Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity` |
| `so_chung_tu` | `varchar(50)` | N | — | Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20 |
| `ngay_chung_tu` | `date` | N | — | Ngày lập chứng từ. `BaseChungTuEntity` |
| `ngay_hach_toan` | `date` | N | — | Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37 |
| `status` | `text` | N | `NHAP` | Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12 |
| `nguoi_duyet_id` | `uuid` | Y | — | Người duyệt. `BaseChungTuEntity` |
| `ngay_duyet` | `timestamptz` | Y | — | Thời điểm duyệt. `BaseChungTuEntity` |
| `nguoi_ghi_so` | `uuid` | Y | — | Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `thoi_gian_ghi_so` | `timestamptz` | Y | — | Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo, gán một lần. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo, gán một lần. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_hoa_don_mua` (35 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 7 | `dien_giai`, `tong_tien_truoc_thue`, `tong_tien_truoc_thue_quy_doi`, `tong_tien_thue_gtgt`, `tong_tien_thue_gtgt_quy_doi`, `tong_tien_sau_thue`, `tong_tien_sau_thue_quy_doi` |
| DB có — LDM **không khai** | 10 | `ghi_chu`, `mau_so_hoa_don`, `loai_tien_id`, `ty_gia`, `tong_truoc_thue_vnd`, `tong_thue_gtgt_vnd`, `tong_sau_thue_vnd`, `trang_thai`, `trang_thai_thanh_toan`, `so_con_no_vnd` |

---

## 4. `pur_chung_tu_nhan_hoa_don`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChungTuNhanHoaDon` |
| Base class | `BaseChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chung_tu_nhan_hoa_don` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Chứng từ nhận hóa đơn về sau · Mỗi đợt nhận hóa đơn tạo đúng một bản ghi, mang số và ngày chứng từ riêng. Bút · toán thuế GTGT được khấu trừ ghi trên chứng từ này, không ghi trên chứng từ gốc. · LoaiTienId và TyGia đồng bộ từ chứng từ gốc và chỉ đọc. |
| Vai trò | Đầu chứng từ (header) |
| Đơn vị 1 dòng | 1 dòng = 1 chứng từ |
| Dùng để làm gì | Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42). |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `DienGiai` | `dien_giai` | `text` | Y | — | Diễn giải chứng từ |
| 2 | `LoaiTienId` | `loai_tien_id` | `uuid` | N | — | Loại tiền giao dịch (reference ENT_LoaiTien) `FK` |
| 3 | `TyGia` | `ty_gia` | `exchange_rate` | N | `1` | Tỷ giá quy đổi về đồng tiền hạch toán. Bản sao tại thời điểm lập chứng từ, không đổi khi danh mục đổi |
| 4 | `TrangThaiGhiSo` | `trang_thai_ghi_so` | `text` CHECK | N | — | Trạng thái ghi sổ (ChuaGhiSo \| DaGhiSo \| DaHuy) |
| 5 | `TrangThaiThanhToan` | `trang_thai_thanh_toan` | `text` CHECK | Y | — | Trạng thái thanh toán (DaThanhToan \| ChuaThanhToan \| DaThanhToanMotPhan) |

**Trường base — `BaseChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4 |
| `phien_ban` | `integer` | N | `1` | Khóa lạc quan `@Version`. `AggregateRootEntity` |
| `chi_nhanh_id` | `uuid` | N | — | Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4 |
| `loai_chung_tu_id` | `uuid` | N | — | Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4 |
| `giao_dich_chung_tu_id` | `uuid` | Y | — | Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity` |
| `so_chung_tu` | `varchar(50)` | N | — | Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20 |
| `ngay_chung_tu` | `date` | N | — | Ngày lập chứng từ. `BaseChungTuEntity` |
| `ngay_hach_toan` | `date` | N | — | Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37 |
| `status` | `text` | N | `NHAP` | Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12 |
| `nguoi_duyet_id` | `uuid` | Y | — | Người duyệt. `BaseChungTuEntity` |
| `ngay_duyet` | `timestamptz` | Y | — | Thời điểm duyệt. `BaseChungTuEntity` |
| `nguoi_ghi_so` | `uuid` | Y | — | Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `thoi_gian_ghi_so` | `timestamptz` | Y | — | Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo, gán một lần. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo, gán một lần. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_chung_tu_nhan_hoa_don` (19 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 2 | `trang_thai_ghi_so`, `trang_thai_thanh_toan` |
| DB có — LDM **không khai** | 3 | `nha_cung_cap_id`, `tong_thue_gtgt_vnd`, `trang_thai` |

---

## 5. `pur_hoa_don_mua_chi_tiet`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiTietHoaDon` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chi_tiet_hoa_don` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng chi tiết hóa đơn nhận về sau · Dòng hàng đọc từ chứng từ ghi nợ gốc và chỉ đọc; màn chỉ cho cập nhật thông tin · thuế. |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_hoa_don_mua` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_hoa_don_mua` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `HoaDonMuaId` | `hoa_don_mua_id` | `uuid` | N | — | Hóa đơn mua (reference ENT_HoaDonMua) `FK` |
| 2 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | Y | — | Chứng từ ghi nợ gốc của dòng (reference ENT_ChungTuMuaHang) `FK` |
| 3 | `ChiTietChungTuMuaHangId` | `chi_tiet_chung_tu_mua_hang_id` | `uuid` | Y | — | Dòng hàng gốc trên chứng từ ghi nợ (reference ENT_ChiTietChungTuMuaHang) `FK` |
| 4 | `LoaiDongHang` | `loai_dong_hang` | `boolean` | N | `false` | Dòng hàng khi true, dòng ghi chú khi false |
| 5 | `VatTuId` | `vat_tu_id` | `uuid` | Y | — | **[Hàng hóa, dịch vụ: chỉ đọc, lấy từ dòng gốc]** Mã hàng, mã dịch vụ (reference ENT_VatTu) `FK` |
| 6 | `TenVatTu` | `ten_vat_tu` | `text` | N | — | **[Hàng hóa, dịch vụ: chỉ đọc, lấy từ dòng gốc]** Tên hàng |
| 7 | `DienGiai` | `dien_giai` | `text` | Y | — | **[Hàng hóa, dịch vụ: chỉ đọc, lấy từ dòng gốc]** Diễn giải dòng, tự điền từ dòng gốc, không hiển thị trên lưới |
| 8 | `ThanhTienTruocThue` | `thanh_tien_truoc_thue` | `money_foreign` ≈ | Y | `0` | **[Hàng hóa, dịch vụ: chỉ đọc, lấy từ dòng gốc]** Giá trị hàng hóa dịch vụ chưa thuế, bằng ThanhTien trừ ChietKhau của dòng gốc |
| 9 | `ThanhTienTruocThueQuyDoi` | `thanh_tien_truoc_thue_quy_doi` | `money_vnd` | Y | `0` | **[Hàng hóa, dịch vụ: chỉ đọc, lấy từ dòng gốc]** Giá trị chưa thuế quy đổi |
| 10 | `ThueSuatGTGT` | `thue_suat_gtgt` | `text` CHECK | Y | — | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Thuế suất GTGT (0 \| 5 \| 8 \| 10 \| KCT \| KKKNT \| KHAC) |
| 11 | `GiaTriThueGTGT` | `gia_tri_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Giá trị thuế suất GTGT thực tế, đơn vị phần trăm |
| 12 | `TienThueGTGT` | `tien_thue_gtgt` | `money_foreign` ≈ | Y | `0` | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Tiền thuế GTGT, bằng ThanhTienTruocThue nhân GiaTriThueGTGT chia 100. Cho phép sửa tay, không tính ngược thuế suất |
| 13 | `TienThueGTGTQuyDoi` | `tien_thue_gtgt_quy_doi` | `money_vnd` | Y | `0` | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Tiền thuế GTGT quy đổi |
| 14 | `TaiKhoanThueGTGTId` | `tai_khoan_thue_gtgt_id` | `uuid` | Y | — | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Tài khoản thuế GTGT được khấu trừ (reference ENT_HeThongTaiKhoan) `FK` |
| 15 | `TaiKhoanCoId` | `tai_khoan_co_id` | `uuid` | Y | — | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Tài khoản công nợ phải trả (reference ENT_HeThongTaiKhoan) `FK` |
| 16 | `NhomHHDVMuaVao` | `nhom_hhdv_mua_vao` | `text` CHECK | Y | — | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Nhóm hàng hóa dịch vụ mua vào (Nhom1 \| Nhom2 \| Nhom3 \| Nhom4 \| Nhom5) |
| 17 | `DienGiaiThue` | `dien_giai_thue` | `text` | Y | — | **[Thuế GTGT: phần duy nhất được sửa trên màn]** Diễn giải thuế, tự điền từ dòng gốc, cho phép sửa tay |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_chi_tiet_hoa_don` (27 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 8 | `loai_dong_hang`, `vat_tu_id`, `ten_vat_tu`, `dien_giai`, `thanh_tien_truoc_thue`, `thanh_tien_truoc_thue_quy_doi`, `gia_tri_thue_gtgt`, `tien_thue_gtgt` |
| DB có — LDM **không khai** | 8 | `tinh_chat_thue_gtgt_id`, `thue_suat_gtgt_id`, `ma_hang`, `ten_hang`, `gia_tri_chua_thue_vnd`, `gia_tri_chua_thue_quy_doi`, `tien_thue_gtgt_vnd`, `phien_ban` |

---

## 6. `pur_chi_phi_mua_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiPhiMuaHang` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chi_phi_mua_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng chi phí chờ phân bổ — chi phí mua hàng và phí hàng về kho · Một bản ghi cho một chứng từ chi phí nguồn được đưa vào tab chi phí của một · chứng từ mua hàng đích. Theo dõi số tiền bằng đồng tiền hạch toán. |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_chung_tu_mua_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_chung_tu_mua_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | N | — | Chứng từ mua hàng đích nhận chi phí (reference ENT_ChungTuMuaHang) `FK` |
| 2 | `ChungTuChiPhiId` | `chung_tu_chi_phi_id` | `uuid` | N | — | Chứng từ chi phí nguồn (reference ENT_ChungTuMuaHang) `FK` |
| 3 | `LoaiChiPhi` | `loai_chi_phi` | `text` CHECK | N | — | Loại chi phí (ChiPhiMuaHang \| PhiHangVeKho) |
| 4 | `TongChiPhi` | `tong_chi_phi` | `money_foreign` ≈ | N | `0` | Tổng chi phí cần phân bổ của chứng từ nguồn, theo đồng tiền hạch toán |
| 5 | `LuyKeSoDaPhanBo` | `luy_ke_so_da_phan_bo` | `money_foreign` ≈ | N | `0` | Số tiền chứng từ nguồn đã phân bổ cho các chứng từ mua hàng khác, không tính chứng từ đang lập |
| 6 | `SoPhanBoLanNay` | `so_phan_bo_lan_nay` | `money_foreign` ≈ | N | `0` | Số tiền phân bổ lần này |
| 7 | `TrangThaiPhanBo` | `trang_thai_phan_bo` | `text` CHECK | N | — | Trạng thái phân bổ của dòng (ChuaPhanBo \| DaPhanBo) |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_chi_phi_mua_hang` (17 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 5 | `chung_tu_chi_phi_id`, `loai_chi_phi`, `tong_chi_phi`, `luy_ke_so_da_phan_bo`, `so_phan_bo_lan_nay` |
| DB có — LDM **không khai** | 6 | `ct_dich_vu_id`, `dien_giai`, `tai_khoan_chi_phi_id`, `so_tien`, `so_tien_quy_doi`, `phien_ban` |

---

## 7. `pur_chi_phi_nhap_khau`

| Mục | Nội dung |
|---|---|
| Entity LDM | `ChiPhiNhapKhau` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_chi_phi_nhap_khau` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Dòng chi phí chờ phân bổ — phí trước hải quan · Tách khỏi ChiPhiMuaHang vì phải theo dõi song song nguyên tệ và quy đổi: phần · nguyên tệ cấu thành giá trị tính thuế nhập khẩu. Chỉ nhận chứng từ chi phí chọn · tại chứng từ mua hàng, không nhận phân bổ từ chứng từ mua dịch vụ. |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_chung_tu_mua_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_chung_tu_mua_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | N | — | Chứng từ mua hàng đích nhận chi phí (reference ENT_ChungTuMuaHang) `FK` |
| 2 | `ChungTuChiPhiId` | `chung_tu_chi_phi_id` | `uuid` | N | — | Chứng từ chi phí nguồn (reference ENT_ChungTuMuaHang) `FK` |
| 3 | `TongChiPhi` | `tong_chi_phi` | `money_foreign` ≈ | N | `0` | Tổng chi phí cần phân bổ theo nguyên tệ của chứng từ nguồn |
| 4 | `TongChiPhiQD` | `tong_chi_phi_qd` | `money_foreign` ≈ | N | `0` | Tổng chi phí quy đổi, bằng TongChiPhi nhân tỷ giá của chứng từ nguồn |
| 5 | `SoPhanBoLanNay` | `so_phan_bo_lan_nay` | `money_foreign` ≈ | N | `0` | Số tiền phân bổ lần này theo nguyên tệ |
| 6 | `SoPhanBoLanNayQD` | `so_phan_bo_lan_nay_qd` | `money_foreign` ≈ | N | `0` | Số tiền phân bổ lần này quy đổi |
| 7 | `LuyKeSoDaPhanBo` | `luy_ke_so_da_phan_bo` | `money_foreign` ≈ | N | `0` | Số tiền nguyên tệ đã phân bổ cho các chứng từ mua hàng khác |
| 8 | `LuyKeSoDaPhanBoQD` | `luy_ke_so_da_phan_bo_qd` | `money_foreign` ≈ | N | `0` | Số tiền quy đổi đã phân bổ cho các chứng từ mua hàng khác |
| 9 | `TrangThaiPhanBo` | `trang_thai_phan_bo` | `text` CHECK | N | — | Trạng thái phân bổ của dòng (ChuaPhanBo \| DaPhanBo) |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_chi_phi_nhap_khau` (24 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 5 | `chung_tu_chi_phi_id`, `tong_chi_phi`, `tong_chi_phi_qd`, `luy_ke_so_da_phan_bo`, `luy_ke_so_da_phan_bo_qd` |
| DB có — LDM **không khai** | 11 | `loai_chi_phi`, `ma_dich_vu_id`, `ten_dich_vu`, `nha_cung_cap_id`, `loai_tien_id`, `ty_gia`, `thanh_tien`, `thanh_tien_quy_doi`, `luy_ke_da_phan_bo`, `luy_ke_da_phan_bo_quy_doi`, `phien_ban` |

---

## 8. `pur_phan_bo_chi_phi_mua_hang`

| Mục | Nội dung |
|---|---|
| Entity LDM | `PhanBoChiPhiMuaHang` |
| Base class | `BaseChiTietChungTuEntity` |
| Nhóm | B — có schema, chưa code |
| Bảng hiện có | `pur_phan_bo_chi_phi_mua_hang` |

**Mục đích & phạm vi nghiệp vụ**

| Mục | Nội dung |
|---|---|
| Mô tả (LDM) | Một bản ghi cho một cặp chứng từ chi phí nguồn và dòng hàng đích. Nhiều nguồn · phân bổ cùng lúc thì mỗi nguồn chạy công thức độc lập, tổng các bản ghi của một · nguồn bằng số phân bổ lần này của nguồn đó. Phân bổ không sinh bút toán, chỉ · cộng vào giá trị nhập kho của dòng hàng đích. |
| Vai trò | Dòng chi tiết |
| Đơn vị 1 dòng | 1 dòng = 1 dòng chi tiết trên `pur_chung_tu_mua_hang` |
| Dùng để làm gì | Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái (giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`. |
| Bảng cha | `pur_chung_tu_mua_hang` — FK `ON DELETE CASCADE` |
| Epic nghiệp vụ | PMKT-E-00485 · PMKT-E-00519 · PMKT-E-00542 · PMKT-E-06758 · PMKT-E-06768 |

**Trường nghiệp vụ**

| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|---|---|
| 1 | `ChungTuChiPhiId` | `chung_tu_chi_phi_id` | `uuid` | N | — | Chứng từ chi phí nguồn (reference ENT_ChungTuMuaHang) `FK` |
| 2 | `ChungTuMuaHangId` | `chung_tu_mua_hang_id` | `uuid` | N | — | Chứng từ mua hàng đích (reference ENT_ChungTuMuaHang) `FK` |
| 3 | `ChiTietChungTuMuaHangId` | `chi_tiet_chung_tu_mua_hang_id` | `uuid` | N | — | Dòng hàng đích nhận chi phí (reference ENT_ChiTietChungTuMuaHang) `FK` |
| 4 | `LoaiChiPhi` | `loai_chi_phi` | `text` CHECK | N | — | Loại chi phí phân bổ (ChiPhiMuaHang \| PhiTruocHaiQuan \| PhiHangVeKho) |
| 5 | `PhuongThucPhanBo` | `phuong_thuc_phan_bo` | `text` CHECK | N | — | Phương thức phân bổ (TheoSoLuong \| TheoThanhTien \| TheoThanhTienSauCK \| ThuCong \| TuNhapPhanTram \| TuNhapGiaTri) |
| 6 | `TyLePhanBo` | `ty_le_phan_bo` | `percent_rate` | Y | `0` | **[Kết quả phân bổ chi phí mua hàng và phí hàng về kho]** Tỷ lệ phân bổ của dòng, đơn vị phần trăm |
| 7 | `ChiPhiPhanBo` | `chi_phi_phan_bo` | `money_foreign` ≈ | Y | `0` | **[Kết quả phân bổ chi phí mua hàng và phí hàng về kho]** Chi phí phân bổ theo nguyên tệ |
| 8 | `ChiPhiPhanBoQuyDoi` | `chi_phi_phan_bo_quy_doi` | `money_vnd` | Y | `0` | **[Kết quả phân bổ chi phí mua hàng và phí hàng về kho]** Chi phí phân bổ quy đổi, là giá trị cộng vào dòng hàng đích |
| 9 | `TyLePhanBoNgoaiTe` | `ty_le_phan_bo_ngoai_te` | `percent_rate` | Y | `0` | **[Kết quả phân bổ phí trước hải quan: ba trục giá trị độc lập]** Tỷ lệ phân bổ của nhóm phí bằng ngoại tệ, đơn vị phần trăm |
| 10 | `PhiTruocHQNgoaiTe` | `phi_truoc_hq_ngoai_te` | `numeric(18,4)` ⚠ | Y | `0` | **[Kết quả phân bổ phí trước hải quan: ba trục giá trị độc lập]** Phí trước hải quan theo nguyên tệ của dòng |
| 11 | `PhiTruocHQNgoaiTeQuyDoi` | `phi_truoc_hq_ngoai_te_quy_doi` | `money_vnd` | Y | `0` | **[Kết quả phân bổ phí trước hải quan: ba trục giá trị độc lập]** Phí trước hải quan bằng ngoại tệ, quy đổi theo tỷ giá hạch toán |
| 12 | `TyLePhanBoHachToan` | `ty_le_phan_bo_hach_toan` | `percent_rate` | Y | `0` | **[Kết quả phân bổ phí trước hải quan: ba trục giá trị độc lập]** Tỷ lệ phân bổ của nhóm phí bằng tiền hạch toán, đơn vị phần trăm |
| 13 | `PhiTruocHQHachToan` | `phi_truoc_hq_hach_toan` | `numeric(18,4)` ⚠ | Y | `0` | **[Kết quả phân bổ phí trước hải quan: ba trục giá trị độc lập]** Phí trước hải quan bằng đồng tiền hạch toán của dòng |
| 14 | `TongPhiTruocHQTinhGiaNhapKho` | `tong_phi_truoc_hq_tinh_gia_nhap_kho` | `money_foreign` ≈ | Y | `0` | **[Kết quả phân bổ phí trước hải quan: ba trục giá trị độc lập]** Tổng phí trước hải quan tính vào giá trị nhập kho, bằng PhiTruocHQNgoaiTeQuyDoi cộng PhiTruocHQHachToan |

**Trường base — `BaseChiTietChungTuEntity`** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*

| Cột DB | Kiểu | Null | Mặc định | Mô tả |
|---|---|---|---|---|
| `id` | `uuid` | N | `gen_random_uuid()` | Khóa chính. `BaseEntity` |
| `tenant_id` | `uuid` | N | — | Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4 |
| `thu_tu` | `integer` | Y | — | Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2 |
| `ngay_tao` | `timestamptz` | N | `now()` | Thời điểm tạo. `BaseEntity` · BR46 |
| `nguoi_tao` | `uuid` | Y | — | Người tạo. `BaseEntity` · BR46 |
| `ngay_cap_nhat` | `timestamptz` | Y | — | Thời điểm sửa gần nhất. `BaseEntity` · BR46 |
| `nguoi_cap_nhat` | `uuid` | Y | — | Người sửa gần nhất. `BaseEntity` · BR46 |
| `da_xoa` | `boolean` | N | `false` | Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46 |
| `ngay_xoa` | `timestamptz` | Y | — | Thời điểm xóa mềm. `BaseEntity` · BR46 |
| `nguoi_xoa` | `uuid` | Y | — | Người xóa mềm. `BaseEntity` · BR46 |

**Đối chiếu `pur_phan_bo_chi_phi_mua_hang` (24 cột hiện có)**

| Chiều | Số cột | Danh sách |
|---|---:|---|
| LDM có — DB **thiếu** | 9 | `chung_tu_chi_phi_id`, `chi_phi_phan_bo`, `chi_phi_phan_bo_quy_doi`, `ty_le_phan_bo_ngoai_te`, `phi_truoc_hq_ngoai_te`, `phi_truoc_hq_ngoai_te_quy_doi`, `ty_le_phan_bo_hach_toan`, `phi_truoc_hq_hach_toan`, `tong_phi_truoc_hq_tinh_gia_nhap_kho` |
| DB có — LDM **không khai** | 10 | `ct_dich_vu_id`, `chi_tiet_dich_vu_id`, `tai_khoan_nguon_id`, `la_tu_dich_vu`, `so_tien_phan_bo_ngoai_te`, `so_tien_phan_bo_hach_toan`, `chi_phi_mua_hang_id`, `so_tien_phan_bo`, `so_tien_phan_bo_quy_doi`, `phien_ban` |

