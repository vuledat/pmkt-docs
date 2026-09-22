# F01 — Ghi sổ chứng từ bán hàng và nhóm chứng từ lập kèm

| Mục | Nội dung |
|---|---|
| Mã chức năng | F01 |
| UC | `PMKT-U-06430`, `UC_CTBH_ThemMoi` — Lưu và ghi sổ |
| Endpoint | Dùng endpoint ghi sổ/lưu và ghi sổ kế thừa từ `BaseChungTuController` |
| Quyền | `BanHangHoa.Post`, `BanHangHoa.Create` |
| Code hiện có | `GhiSoChungTuBanHang.java`, `LuuChungTuBanHangTemplate.java`, `DinhKhoanBanHang.java` |

## 1. Mục tiêu

Hoàn thiện luồng từ dữ liệu từng dòng CTBH đến `DinhKhoan`, rồi để `GhiSoApi` tạo `acc_so_cai`. Một chứng từ bán hàng có thể có nhiều nghiệp vụ trên cùng dòng; mỗi nghiệp vụ được giữ bằng `sttButToan`, mỗi dòng nguồn bằng `sttDongChiTiet` và `chiTietChungTuId`.

## 2. Hợp đồng dữ liệu nội bộ

### 2.1 `DongHachToan` của một dòng

`DinhKhoanBanHang.dungDong()` phải truyền đủ vai trò:

```text
TK_CONG_NO          ← ChiTiet.taiKhoanNoId
TK_DOANH_THU_PB    ← ChiTiet.taiKhoanCoId
TK_CHIET_KHAU      ← ChiTiet.taiKhoanChietKhauId
TK_THUE_GTGT       ← ChiTiet.taiKhoanThueGtgtId
TK_THUE_XUAT_KHAU  ← ChiTiet.taiKhoanThueXkId
TK_GIA_VON         ← ChiTiet.taiKhoanGiaVonId
TK_KHO             ← ChiTiet.taiKhoanKhoId
TK_TIEN            ← ChungTu.taiKhoanTienId
```

Không được tra lại tài khoản từ danh mục khi dòng đã có tài khoản; đây là R-CTBH-093.

### 2.2 Điều kiện tạo nghiệp vụ

| Bút toán | Điều kiện | Số tiền | TK Nợ/Có |
|---|---|---|---|
| #1 | Dòng không phải CKTM và `ThanhTien > 0` | `ThanhTienQuyDoi` | Công nợ / Doanh thu |
| #2 | `TienChietKhau > 0` | `ChietKhauQuyDoi` | Chiết khấu / Công nợ |
| #3 | Dòng CKTM | `ABS(ThanhTienQuyDoi)` | Doanh thu / Công nợ |
| #4 | Trong nước và `TienThueGtgt > 0` | `TienThueGtgtQuyDoi` | Công nợ / Thuế GTGT |
| #5 | Xuất khẩu và `TienThueXk > 0` | `TienThueXkQuyDoi` | Doanh thu / Thuế XK |
| #6 | Có cờ kiêm PXK nhưng **chưa có PXK gánh** | `TongGiaTriVonQuyDoi` | Giá vốn / Kho |
| #7 | Có cờ thu tiền ngay nhưng **chưa có phiếu thu gánh** | `PhaiThuQuyDoi` | Tiền / Công nợ |

#6/#7 chỉ là fallback tương thích dữ liệu cũ. Với chứng từ lập kèm đầy đủ bộ, `coPhieuXuatKho(ct)` và `coPhieuThu(ct)` phải làm #6/#7 biến mất khỏi CTBH.

## 3. Ánh xạ `DinhKhoan` → `acc_so_cai`

| `DinhKhoan` | `acc_so_cai` | Quy tắc |
|---|---|---|
| `chiTietChungTuId` | `chi_tiet_chung_tu_id` | ID dòng nguồn, không được null với CTBH đã lưu |
| `sttDongChiTiet` | `stt_dong_chi_tiet` | `ChiTiet.thuTu` nếu phân biệt được; trùng thì để kernel cấp |
| `sttButToan` | `stt_but_toan` | #1–#7 theo bảng mapping |
| `taiKhoanNoId` | một vế `tai_khoan_id` | TK snapshot lúc ghi sổ |
| `taiKhoanCoId` | `tai_khoan_doi_ung_id` | Đảo chiều ở dòng Có |
| `soTien` | `ps_no` hoặc `ps_co` | Chỉ một vế có số tiền |
| `soTienNguyenTe` | `ps_no_nt`/`ps_co_nt` | Chỉ có khi tỷ giá khác 1 |
| `doiTuongId` | `doi_tuong_id` | Khách hàng |
| `khoanMucChiPhiId` | `khoan_muc_chi_phi_id` | Lấy từ dòng |
| `donViId`, `vuViecId`, `hopDongId` | chiều phân tích tương ứng | Phải truyền từ dòng sau D1 |
| `chiNhanhId` | `chi_nhanh_id` | Lấy từ header trong `GhiSoRequest` |

`GhiSoService.taoDongSoCai()` luôn tạo đúng 2 entity cho một `DinhKhoan`; không sửa kernel để sinh 1 hoặc 3 dòng.

## 4. Các bước code

### Bước 1 — Chuẩn hóa mapping chiều phân tích

Sửa `DinhKhoanBanHang.sangDinhKhoan()`:

```java
dk = dk.voiDoiTuong(ct.getKhachHangId())
       .voiKhoanMucChiPhi(dong.getKhoanMucChiPhiId())
       .voiDonVi(dong.getDonViId())
       .voiVuViec(dong.getVuViecId())
       .voiHopDong(dong.getHopDongId())
       .voiDienGiaiDong(dong.getMoTa());
```

Không gán `donViId` từ `ct.getChiNhanhId()`; `acc_so_cai` đã tách chi nhánh và đơn vị qua V1064.

### Bước 2 — Chốt hai chiều chưa có nguồn

Nếu Q2 xác nhận cần lưu:

1. Thêm field vào `LuuChiTietChungTuBanHangRequest`.
2. Thêm field vào `ChiTietChungTuBanHang`.
3. Map request → entity và entity → DTO.
4. Tạo migration `ALTER TABLE sal_chung_tu_ban_hang_chi_tiet ADD COLUMN ... uuid`.
5. Truyền `.voiDoiTuongTapHopChiPhi(...)` và `.voiDonDatHang(...)`.
6. Bổ sung index nếu có query báo cáo tương ứng; không thêm index không có query.

Nếu Q2 không xác nhận, giữ `NULL` và ghi rõ trong compliance report là giới hạn nguồn dữ liệu.

### Bước 3 — Giữ đúng semantics nhóm chứng từ

Trong `LuuChungTuBanHangTemplate.sauKhiLuu()` giữ thứ tự:

1. Đồng bộ PXK.
2. Đồng bộ phiếu thu.
3. Đồng bộ hóa đơn.
4. Chốt liên kết hóa đơn.
5. Nếu ghi sổ, dựng định khoản CTBH rồi ghi sổ chứng từ con.

Không gọi `ghiSoTheoNguon` cho hóa đơn. Hóa đơn lập kèm chỉ được tạo/liên kết và giữ vòng đời riêng.

### Bước 4 — Kiểm tra lỗi nhóm và rollback

Trước khi ghi sổ child, validate dữ liệu child trong cùng `ChungTuTemplate`. Nếu PXK thiếu tồn hoặc phiếu thu thiếu tài khoản, ném lỗi trước commit; transaction phải rollback cả `acc_so_cai`, trạng thái header và trạng thái child.

### Bước 5 — Không thay đổi gộp cặp trong kernel

`TaoDinhKhoanService` đã:

- Bỏ nghiệp vụ không có tiền.
- Đảo chiều khi số tiền âm.
- Gộp cặp cùng chiều.
- Bù trừ cặp ngược chiều.
- Bỏ cặp sau bù trừ bằng 0.

Chỉ bổ sung test để khóa hành vi này cho dữ liệu CTBH.

## 5. Test unit bắt buộc

Tất cả test mới gắn `@Tag("unit")`, đặt song ánh module.

| Test | Input | Expected |
|---|---|---|
| `R093_sinhNamButToanNoiDia` | 1 dòng bán trong nước, CK + GTGT | #1/#2/#4, đúng TK trên dòng |
| `R093_sinhThueXuatKhau` | dòng xuất khẩu | có #5, không #4 |
| `R093_boQuaGiaVonKhiPxkGanh` | `giaVonDoPhieuXuatGhi=true` | không có #6 |
| `R093_boQuaThuTienKhiPhieuThuGanh` | `thuTienDoPhieuThuGhi=true` | không có #7 |
| `R094_moiDinhKhoanHaiDongSoCai` | 3 định khoản | mỗi định khoản 2 vế đảo nhau |
| `R095_moiDongKhongGopGiuaDong` | 2 dòng cùng TK | giữ `chiTietChungTuId`/`sttDongChiTiet` riêng |
| `R095_gopCapDaoChieuTrongMotDong` | cùng dòng, cặp ngược chiều | số tiền net đúng, không đẩy payload xung đột |
| `R020_truyenChieuPhanTich` | dòng có đơn vị/vụ việc/hợp đồng | `DinhKhoan` giữ đủ ID |
| `INV001_canDoi` | nhiều nghiệp vụ | tổng `soTien` Nợ = Có |

## 6. Test tích hợp DB/nhóm

Các test này cần DB thật và chạy ở CI/IntelliJ; không chạy Docker trong môi trường hiện tại.

| Scenario | Kiểm tra |
|---|---|
| S-067 | đúng 6 dòng `acc_so_cai`, cùng `chung_tu_id`, dòng D1, STT #1/#2/#4 |
| S-068 | đúng #5, không #4 |
| S-070 | CTBH + PXK + phiếu thu đều `Đã ghi sổ`; hóa đơn không đổi trạng thái; không duplicate #6/#7 |
| S-071 | PXK thiếu tồn → rollback cả nhóm; không còn dòng sổ cái mới |
| S-075 | bỏ ghi sổ nhóm xóa sổ cái/sổ kho/sổ công nợ của nhóm; hóa đơn không bị đụng |
| ngoại tệ | PSNo/PSCo quy đổi đúng, cột nguyên tệ chỉ có khi tỷ giá khác 1 |
| idempotency | gọi ghi sổ lặp cùng payload không sinh dòng trùng; payload khác bị chặn |

## 7. Điều kiện hoàn thành F01

- [ ] R-CTBH-093/094/095 và INV-001/002 có code + test tương ứng.
- [ ] Mỗi cặp tài khoản trên cùng dòng được truyền thành một `DinhKhoan` riêng trước khi kernel gộp/bù trừ.
- [ ] CTBH lập kèm đầy đủ bộ không ghi trùng giá vốn/thu tiền.
- [ ] Hóa đơn lập kèm không bị ghi sổ đồng bộ.
- [ ] Chiều phân tích đã có nguồn được ghi xuống `acc_so_cai`; hai chiều chưa có nguồn được BA chốt.
- [ ] Unit test xanh; integration test có bằng chứng CI/IntelliJ.
- [ ] `trace.sh` không còn `MISSING` cho nhóm R093–R099 sau khi code.

