# PMKT-E-06194 Chứng từ bán hàng — Luật nghiệp vụ nguyên tử

| | |
|---|---|
| Commit tài liệu | `8cf9606ea` |
| Ngày soát | 2026-08-28 |
| Tổng | **112 luật** (`R-CTBH-001…112`) · **14 bất biến** (`INV-001…014`) |
| Trạng thái | 105 `CHỐT` · **7 `CHỜ`** (bị chặn bởi `C01` `C03` `C04` `C05` `C06` `C07` `C10`) |

> **File này là nguồn sự thật duy nhất để code.** `/plan-be` · `/gen-be` lọc `Tầng = BE|CẢ HAI`;
> `/plan-fe` · `/gen-fe` lọc `Tầng = FE|CẢ HAI`. Mọi đường dẫn nguồn tính từ
> `pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang/`.
>
> Luật `CHỜ C<nn>` → **cấm code** cho tới khi mục `C<nn>` trong [`01-conflict.md`](01-conflict.md)
> chuyển `CLOSED-BA`.

---

## Bảng tổng

| ID | Tên luật | Tầng | Sev | TT | Nguồn |
|---|---|---|---|---|---|
| R-CTBH-001 | Quyền vào màn danh sách | CẢ HAI | P1 | CHỐT | UC_DanhSach AC1 |
| R-CTBH-002 | Lọc mặc định đầu tháng → hiện tại | CẢ HAI | P2 | CHỐT | SCR_DanhSach BR02 |
| R-CTBH-003 | Giữ bộ lọc lần truy cập trước | FE | P2 | CHỐT | SCR_DanhSach BR02 |
| R-CTBH-004 | Danh sách dùng chung bán hàng + bán dịch vụ | BE | P1 | CHỐT | SCR_DanhSach BR01 |
| R-CTBH-005 | Sắp xếp mặc định 3 khóa | BE | P2 | CHỐT | SCR_DanhSach §Sắp xếp |
| R-CTBH-006 | Cột tiền hiển thị theo đồng tiền hạch toán | CẢ HAI | P0 | CHỐT | SCR_DanhSach BR01 |
| R-CTBH-007 | Số hóa đơn hiển thị danh sách nhiều HĐ | BE | P2 | CHỐT | SCR_DanhSach BR01 |
| R-CTBH-008 | Nút Sửa/Ghi sổ/Xóa chỉ khi Chưa ghi sổ | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR04 |
| R-CTBH-009 | Nút Bỏ ghi chỉ khi Đã ghi sổ | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR04 |
| R-CTBH-010 | Nút Thu tiền theo trạng thái thanh toán | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR04 |
| R-CTBH-011 | Nút Lập hóa đơn theo trạng thái lập HĐ | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR04 |
| R-CTBH-012 | Nút Lập phiếu xuất theo trạng thái xuất hàng | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR04 |
| R-CTBH-013 | Dòng tổng cộng cuối danh sách | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR05 |
| R-CTBH-014 | Trạng thái xuất hàng để trống với bán dịch vụ | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR03 |
| R-CTBH-015 | Quyền xem chi tiết | CẢ HAI | P1 | CHỐT | UC_XemChiTiet AC1 |
| R-CTBH-016 | Xem chi tiết readonly toàn bộ | FE | P1 | CHỐT | SCR_XemChiTiet §17 |
| R-CTBH-017 | Bộ nút màn Xem chi tiết | FE | P1 | CHỐT | SCR_XemChiTiet BR1 |
| R-CTBH-018 | Khu chi tiết dưới lưới — 4 tab | CẢ HAI | P1 | CHỐT | SCR_DanhSach BR08 |
| R-CTBH-019 | Nút Lập phiếu xuất kho trên Xem chi tiết | FE | P1 | **CHỜ C07** | — |
| R-CTBH-020 | Khu chi tiết kiểm quyền trước khi trả dữ liệu | BE | P0 | CHỐT | SCR_DanhSach BR08 |
| R-CTBH-021 | Nguồn khách hàng — vai trò KhachHang | BE | P1 | CHỐT | ThemMoi BR01.1 |
| R-CTBH-022 | Auto-fill thông tin khách hàng theo tab | CẢ HAI | P1 | CHỐT | ThemMoi BR01.2a |
| R-CTBH-023 | Auto-fill TK công nợ dòng đầu tiên | CẢ HAI | P0 | CHỐT | ThemMoi BR01.2b |
| R-CTBH-024 | Template diễn giải đầu chứng từ | CẢ HAI | P2 | CHỐT | ThemMoi BR01.c1 |
| R-CTBH-025 | Validate định dạng MST tổ chức | CẢ HAI | P1 | CHỐT | ThemMoi BR01.d |
| R-CTBH-026 | Validate định dạng CCCD cá nhân | CẢ HAI | P1 | CHỐT | ThemMoi BR01.d |
| R-CTBH-027 | Đồng bộ trường chung giữa các tab | FE | P1 | CHỐT | ThemMoi BR02.a |
| R-CTBH-028 | Tab Hóa đơn đồng bộ một chiều | FE | P1 | CHỐT | ThemMoi BR02.b |
| R-CTBH-029 | Đồng bộ Ngày hạch toán, không đồng bộ Ngày chứng từ | CẢ HAI | P0 | CHỐT | ThemMoi BR02.c |
| R-CTBH-030 | Sinh số chứng từ theo quy tắc đánh số | BE | P0 | CHỐT | ThemMoi BR25 |
| R-CTBH-031 | Auto-calc Hạn thanh toán + cơ chế ngắt | FE | P1 | CHỐT | ThemMoi BR03 |
| R-CTBH-032 | Đồng bộ Hình thức TT sang tab Hóa đơn | FE | P1 | CHỐT | ThemMoi BR04 |
| R-CTBH-033 | Loại trừ 2 checkbox hóa đơn | FE | P1 | CHỐT | ThemMoi BR05.1 |
| R-CTBH-034 | Tự tích "Đã lập hóa đơn" khi có HĐ lập sau | BE | P1 | CHỐT | ThemMoi BR05.3 |
| R-CTBH-035 | Ẩn cả cột nhóm kho khi không phát sinh kho | FE | P1 | CHỐT | ThemMoi BR17 |
| R-CTBH-036 | Chặn lưu khi toàn dòng Dịch vụ mà tích kiêm PXK | CẢ HAI | P1 | **CHỜ C10** | ThemMoi BR18.2 |
| R-CTBH-037 | Xác định dòng phát sinh xuất kho | BE | P0 | CHỐT | ThemMoi BR17 |
| R-CTBH-038 | Auto-fill từ danh mục vật tư | CẢ HAI | P1 | CHỐT | ThemMoi BR07 |
| R-CTBH-039 | Trường tự do trên dòng chi tiết | CẢ HAI | P2 | CHỐT | ThemMoi §Trường tự do + BR6 chung |
| R-CTBH-040 | Thêm dòng — giá trị mặc định | FE | P1 | CHỐT | ThemMoi BR08 |
| R-CTBH-041 | Thêm dòng sau dòng KM/CKTM — chỉ chép TK | FE | P1 | CHỐT | ThemMoi BR08 |
| R-CTBH-042 | Dòng ghi chú không tham gia tính toán | CẢ HAI | P0 | CHỐT | ThemMoi BR08 |
| R-CTBH-043 | Hai checkbox KM/CKTM loại trừ nhau | FE | P1 | CHỐT | ThemMoi BR09 |
| R-CTBH-044 | Dòng KM ghi nhận đúng giá trị nhập | CẢ HAI | P0 | CHỐT | ThemMoi BR09.a |
| R-CTBH-045 | Dòng CKTM mang Thành tiền âm | CẢ HAI | P0 | CHỐT | ThemMoi BR09.b |
| R-CTBH-046 | Công thức Thành tiền 2 chiều | CẢ HAI | P0 | CHỐT | ThemMoi BR11.1 |
| R-CTBH-047 | Số lượng = 0 → ép Đơn giá 0, giữ Thành tiền | CẢ HAI | P0 | CHỐT | ThemMoi BR11.2 |
| R-CTBH-048 | Đơn vị tính quy đổi — 3 cột hiển thị | CẢ HAI | P1 | CHỐT | ThemMoi BR10 |
| R-CTBH-049 | Chiết khấu theo mặt hàng — tính 2 chiều | CẢ HAI | P0 | CHỐT | ThemMoi BR12.a |
| R-CTBH-050 | CK theo mặt hàng — nhập tay, tính 2 chiều | CẢ HAI | P0 | CHỐT | ThemMoi BR12.d · C08 |
| R-CTBH-051 | CK theo hóa đơn — cơ sở sau CK mặt hàng | CẢ HAI | P0 | CHỐT | ThemMoi BR12.d · C08 |
| R-CTBH-052 | Chiết khấu theo % hóa đơn — nút Áp dụng | CẢ HAI | P0 | CHỐT | ThemMoi BR12.b |
| R-CTBH-053 | Dòng tổng lưới chi tiết — bỏ dòng ghi chú | CẢ HAI | P1 | CHỐT | ThemMoi §Dòng tổng tiền |
| R-CTBH-054 | Ràng buộc Tiền CK ≤ Thành tiền dòng | CẢ HAI | P0 | CHỐT | ThemMoi BR12.f |
| R-CTBH-055 | PBCK — phân bổ theo giá trị / số lượng | CẢ HAI | P0 | CHỐT | PBCK BR1, BR2 · C09 |
| R-CTBH-056 | PBCK — phân bổ thủ công, 2 cột enable | CẢ HAI | P0 | CHỐT | PBCK BR3 · C09 |
| R-CTBH-057 | PBCK — dòng cuối bù chênh lệch làm tròn | BE | P0 | CHỐT | PBCK BR7 |
| R-CTBH-058 | PBCK — bỏ qua dòng KM/CKTM | CẢ HAI | P0 | CHỐT | PBCK BR4, BR5 |
| R-CTBH-059 | PBCK — validate tổng tỷ lệ = 100% | CẢ HAI | P1 | CHỐT | PBCK BR6 |
| R-CTBH-060 | Counter HĐ khởi tạo khi LapKemHoaDon | BE | P0 | CHỐT | ThemMoi BR23.4 |
| R-CTBH-061 | Counter HĐ khởi tạo khi DaLapHoaDon | BE | P0 | CHỐT | ThemMoi BR23.4 |
| R-CTBH-062 | Counter kho khởi tạo khi KiemPhieuXuatKho | BE | P0 | CHỐT | ThemMoi BR23.4 |
| R-CTBH-063 | Counter = 0 khi checkbox không chọn | BE | P0 | CHỐT | ThemMoi BR23.4 |
| R-CTBH-064 | Khởi tạo counter chỉ chạy lần lưu đầu | BE | P0 | CHỐT | ThemMoi BR23.4 |
| R-CTBH-065 | Sinh bản ghi chứng từ con khi Lưu | BE | P0 | CHỐT | ThemMoi BR18.1 |
| R-CTBH-066 | Bỏ tích checkbox → xóa bản ghi con | BE | P0 | CHỐT | ThemMoi BR18.1 |
| R-CTBH-067 | Phiếu con tự cấp số theo loại của nó | BE | P0 | CHỐT | ThemMoi BR18.3, BR25 |
| R-CTBH-068 | Ngày hạch toán dùng chung 3 phần | BE | P0 | CHỐT | ThemMoi BR18.3 |
| R-CTBH-069 | Tài khoản lấy theo định khoản ngầm định | BE | P0 | CHỐT | ThemMoi BR16 |
| R-CTBH-070 | Chỉ chọn tài khoản cấp cuối trong bộ lọc | CẢ HAI | P0 | CHỐT | ThemMoi BR16.4 |
| R-CTBH-071 | Hai luồng tiền tệ độc lập | CẢ HAI | P0 | CHỐT | ThemMoi BR11.5, BR14 |
| R-CTBH-072 | Tổng thanh toán cộng dồn từng dòng | CẢ HAI | P0 | CHỐT | ThemMoi §Tổng hợp #5 |
| R-CTBH-073 | Công thức Tiền thuế GTGT | CẢ HAI | P0 | CHỐT | ThemMoi BR13.3 |
| R-CTBH-074 | Lưu là một transaction, lỗi thì rollback hết | BE | P0 | CHỐT | UC_ThemMoi AC5 |
| R-CTBH-075 | Giữ nguyên dữ liệu form khi lỗi | FE | P1 | CHỐT | UC_ThemMoi §Trạng thái biểu mẫu |
| R-CTBH-076 | Nút Sửa chỉ khi Chưa ghi sổ + có quyền | CẢ HAI | P1 | CHỐT | UC_ChinhSua AC1 |
| R-CTBH-077 | Màn Sửa hiện 4 trường theo dõi số lượng | FE | P1 | CHỐT | SCR_CapNhat §Điểm khác biệt |
| R-CTBH-078 | Điều kiện sửa chứng từ đã có liên kết | CẢ HAI | P0 | **CHỜ C06** | — |
| R-CTBH-079 | Disable checkbox HĐ khi hệ thống tự tích | FE | P1 | CHỐT | SCR_CapNhat §Điểm khác biệt |
| R-CTBH-080 | Sửa CTBH → cập nhật lại phiếu con, giữ số | BE | P0 | CHỐT | ThemMoi BR18.6 |
| R-CTBH-081 | Ràng buộc SoLuong_moi ≥ MAX(counter) | BE | P0 | **CHỜ C06** | — |
| R-CTBH-082 | Chứng từ đã ghi sổ không sửa SoLuong | BE | P0 | CHỐT | ThemMoi BR23.9 |
| R-CTBH-083 | Quyền xóa `BanHangHoa.Delete` | CẢ HAI | P1 | CHỐT | UC_Xoa §Tiền điều kiện |
| R-CTBH-084 | Popup xác nhận trước khi xóa | FE | P1 | CHỐT | SCR_PopupXacNhanXoa §Thành phần |
| R-CTBH-085 | Chỉ xóa chứng từ Chưa ghi sổ | CẢ HAI | P0 | CHỐT | SCR_PopupXacNhanXoa BR01 |
| R-CTBH-086 | Chính sách xóa hàng loạt | CẢ HAI | P0 | **CHỜ C01** | — |
| R-CTBH-087 | Trạng thái nút Xóa hàng loạt | FE | P0 | **CHỜ C01** | — |
| R-CTBH-088 | Điều kiện "đã sử dụng ở nghiệp vụ khác" | CẢ HAI | P0 | **CHỜ C02 C03 C04** | — |
| R-CTBH-089 | Cascade xóa mềm chứng từ con | BE | P0 | **CHỜ C05** | — |
| R-CTBH-090 | Counter và điều kiện chặn xóa | BE | P0 | **CHỜ C04** | — |
| R-CTBH-091 | Quyền ghi sổ `BanHangHoa.Post` | CẢ HAI | P1 | CHỐT | UC_GhiSo §Tiền điều kiện |
| R-CTBH-092 | Chặn ghi sổ vào kỳ đã khóa | BE | P0 | CHỐT | BR17 chung · C11 |
| R-CTBH-093 | Sinh bút toán chứng từ bán — 5 bút toán | BE | P0 | CHỐT | ThemMoi BR20.1 |
| R-CTBH-094 | Mỗi bút toán sinh 2 bản ghi sổ cái | BE | P0 | CHỐT | ThemMoi BR20.2 |
| R-CTBH-095 | Bút toán gắn đúng dòng chi tiết | BE | P0 | CHỐT | ThemMoi BR20.1 |
| R-CTBH-096 | Ghi sổ hàng loạt — partial success | CẢ HAI | P0 | CHỐT | UC_GhiSo AC3 · BR45 chung |
| R-CTBH-097 | Ghi sổ đồng bộ cả nhóm chứng từ liên kết | BE | P0 | CHỐT | ThemMoi BR21.3 |
| R-CTBH-098 | Một chứng từ trong nhóm lỗi → chặn cả nhóm | BE | P0 | CHỐT | ThemMoi BR21.3 |
| R-CTBH-099 | Hóa đơn không đồng bộ ghi sổ | BE | P0 | CHỐT | ThemMoi BR21.3 |
| R-CTBH-100 | Quyền bỏ ghi sổ `BanHangHoa.Unpost` | CẢ HAI | P1 | CHỐT | UC_BoGhiSo §Tiền điều kiện |
| R-CTBH-101 | Chặn bỏ ghi sổ khi phiếu thu lập riêng đã ghi sổ | BE | P0 | CHỐT | ThemMoi BR21.4 |
| R-CTBH-102 | Chặn bỏ ghi sổ khi đang tham gia đối trừ | BE | P0 | CHỐT | ThemMoi BR21.4 |
| R-CTBH-103 | PXK lập riêng không chặn bỏ ghi sổ | BE | P0 | CHỐT | ThemMoi BR21.4 |
| R-CTBH-104 | Bỏ ghi sổ xóa toàn bộ định khoản | BE | P0 | CHỐT | ThemMoi BR20.6 |
| R-CTBH-105 | Bỏ ghi sổ không đổi trạng thái xuất hàng / lập HĐ | BE | P0 | CHỐT | ThemMoi BR21.5, BR22 |
| R-CTBH-106 | Bỏ ghi sổ trừ lại SoTienDaThanhToan | BE | P0 | CHỐT | ThemMoi BR22.2 |
| R-CTBH-107 | Nút Xem dữ liệu ghi sổ luôn hiển thị | FE | P2 | CHỐT | XemDuLieuGhiSo BR01 |
| R-CTBH-108 | Hai chế độ dữ liệu theo trạng thái ghi sổ | CẢ HAI | P0 | CHỐT | XemDuLieuGhiSo BR02 |
| R-CTBH-109 | Chế độ Xem trước không ghi dữ liệu | BE | P0 | CHỐT | XemDuLieuGhiSo BR02 |
| R-CTBH-110 | Phạm vi bút toán = cả nhóm liên kết | BE | P0 | CHỐT | XemDuLieuGhiSo BR03 |
| R-CTBH-111 | Xem trước thiếu TK → bỏ bút toán đó, không chặn | CẢ HAI | P1 | CHỐT | XemDuLieuGhiSo BR04 |
| R-CTBH-112 | Thứ tự sắp xếp bút toán, không gộp | CẢ HAI | P1 | CHỐT | XemDuLieuGhiSo BR05 |

---

## Nhóm 1 — Màn danh sách (`R-CTBH-001…014`)

### R-CTBH-001 · Quyền vào màn danh sách
```
Tầng      CẢ HAI          Sev  P1
Nguồn     UC_CTBH_DanhSach.md:10 (bậc 3) · BR25 chung
BR chung  BR25 — áp nguyên vẹn
WHEN      người dùng không có quyền BanHangHoa.View
THEN      chặn truy cập màn danh sách; API trả lỗi quyền
Lỗi       MSG_PMKT-E-06194_007
Kịch bản  S-030
```

### R-CTBH-002 · Lọc mặc định đầu tháng → hiện tại
```
Tầng      CẢ HAI          Sev  P2
Nguồn     SCR_CTBH_DanhSach.md:127 (BR02, bậc 4)
WHEN      người dùng vào màn danh sách lần đầu (chưa có bộ lọc lưu)
THEN      NgayHachToan BETWEEN ngày đầu tháng hiện tại AND ngày hiện tại
Lỗi       —               Bất biến  —          Kịch bản  S-001
```

### R-CTBH-003 · Giữ bộ lọc lần truy cập trước
```
Tầng      FE              Sev  P2
Nguồn     SCR_CTBH_DanhSach.md:128 (BR02)
WHEN      người dùng vào lại màn danh sách và đã có bộ lọc + sắp xếp lưu của lần trước
THEN      khôi phục đúng bộ lọc và sắp xếp đó, không áp lại lọc mặc định của R-CTBH-002
Kịch bản  S-002
```

### R-CTBH-004 · Danh sách dùng chung bán hàng + bán dịch vụ
```
Tầng      BE              Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:98 (BR01) · ThemMoi BR24 (:1560)
WHEN      truy vấn danh sách
THEN      lấy mọi bản ghi sal_chung_tu_ban của tenant, KHÔNG lọc theo LoaiNghiepVu
          (3 giá trị: Bán hàng trong nước · Bán hàng xuất khẩu · Bán dịch vụ)
Kịch bản  S-003
```

### R-CTBH-005 · Sắp xếp mặc định 3 khóa
```
Tầng      BE              Sev  P2
Nguồn     SCR_CTBH_DanhSach.md:89
WHEN      không có sắp xếp do người dùng chọn
THEN      ORDER BY NgayHachToan DESC, NgayChungTu DESC, SoChungTu ASC
BR chung  BR2 · BR11 (không sắp xếp đồng thời nhiều cột do người dùng chọn)
Kịch bản  S-001
```

### R-CTBH-006 · Cột tiền hiển thị theo đồng tiền hạch toán
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_DanhSach.md:124 (BR01)
WHEN      chứng từ có LoaiTienId ≠ đồng tiền hạch toán của tenant
THEN      4 cột tiền lấy TongTienHangQuyDoi · TongChietKhauQuyDoi · TongThueGTGTQuyDoi
          · TongThanhToanQuyDoi
ELSE      lấy 4 cột nguyên tệ tương ứng
Bất biến  INV-013         Kịch bản  S-004
```

### R-CTBH-007 · Số hóa đơn hiển thị danh sách nhiều HĐ
```
Tầng      BE              Sev  P2
Nguồn     SCR_CTBH_DanhSach.md:109 (BR01)
WHEN      chứng từ có ≥ 1 hóa đơn liên kết (sal_hoa_don_ban_hang.ChungTuBanId = Id)
THEN      cột Số hóa đơn = danh sách SoHoaDon nối bằng dấu phẩy
ELSE      để trống
Kịch bản  S-005
```

### R-CTBH-008 · Nút Sửa / Ghi sổ / Xóa chỉ khi Chưa ghi sổ
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:139 (BR04) · SCR_CTBH_PopupXacNhanXoa.md:45-50 (BR03)
WHEN      TrangThaiGhiSo = "Chưa ghi sổ" AND có quyền tương ứng
THEN      hiện nút Sửa · Ghi sổ · Xóa trên dòng
ELSE      ẩn nút
Ghi chú   chứng từ "đã sử dụng ở nghiệp vụ khác" VẪN hiện nút Xóa — chặn khi bấm (R-CTBH-088)
Kịch bản  S-006
```

### R-CTBH-009 · Nút Bỏ ghi chỉ khi Đã ghi sổ
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:140 (BR04)
WHEN      TrangThaiGhiSo = "Đã ghi sổ" AND có quyền BanHangHoa.Unpost
THEN      hiện nút Bỏ ghi          ELSE ẩn
Kịch bản  S-006
```

### R-CTBH-010 · Nút Thu tiền theo trạng thái thanh toán
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:141 (BR04)
WHEN      TrangThaiGhiSo = "Đã ghi sổ"
          AND TrangThaiThanhToan ∈ {Chưa thanh toán, Đã thanh toán một phần}
          AND có quyền thu tiền
THEN      hiện nút Thu tiền → mở màn Tìm kiếm chứng từ thanh toán (BR06 SCR_DanhSach)
ELSE      ẩn
Kịch bản  S-007
```

### R-CTBH-011 · Nút Lập hóa đơn theo trạng thái lập HĐ
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:142 (BR04) · ThemMoi BR23.5.1 (:1491)
WHEN      TrangThaiLapHoaDon ∈ {Chưa lập, Đã lập một phần} AND có quyền lập hóa đơn
THEN      hiện nút Lập hóa đơn — KHÔNG phụ thuộc TrangThaiGhiSo
ELSE      ẩn
Kịch bản  S-008
```

### R-CTBH-012 · Nút Lập phiếu xuất theo trạng thái xuất hàng
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:143 (BR04) · ThemMoi BR23.6.1 (:1520)
WHEN      TrangThaiXuatHang ∈ {Chưa xuất hàng, Đã xuất một phần}
          AND LoaiNghiepVu ≠ "Bán dịch vụ" AND có quyền lập phiếu xuất
THEN      hiện nút Lập phiếu xuất — KHÔNG phụ thuộc TrangThaiGhiSo
ELSE      ẩn
Kịch bản  S-009
```

### R-CTBH-013 · Dòng tổng cộng cuối danh sách
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:145-151 (BR05) · BR31 chung
WHEN      kết quả lọc có ≥ 1 chứng từ
THEN      hiện dòng tổng: Σ Tiền chiết khấu · Σ Tiền thuế GTGT · Σ Tổng tiền thanh toán
          — tính trên TOÀN BỘ chứng từ trong bộ lọc, không chỉ trang hiện tại
ELSE      ẩn dòng tổng
Kịch bản  S-010
```

### R-CTBH-014 · Trạng thái xuất hàng để trống với bán dịch vụ
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:117,134 (BR01, BR03) · ThemMoi BR22 (:1382)
WHEN      chứng từ không có dòng nào Loại hàng hóa = Hàng hóa
THEN      TrangThaiXuatHang = NULL, cột hiển thị để trống
Bất biến  INV-009         Kịch bản  S-011
```

---

## Nhóm 2 — Xem chi tiết (`R-CTBH-015…020`)

### R-CTBH-015 · Quyền xem chi tiết
```
Tầng      CẢ HAI          Sev  P1
Nguồn     UC_CTBH_XemChiTiet.md:8,27
WHEN      thiếu quyền BanHangHoa.View.Detail
THEN      ẩn nút Xem chi tiết; truy cập trực tiếp → chặn
Lỗi       MSG_PMKT-E-06194_007          Kịch bản  S-030
```

### R-CTBH-016 · Xem chi tiết readonly toàn bộ
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_XemChiTiet.md:18-19
WHEN      mở màn Xem chi tiết
THEN      mọi trường readonly; ẩn hẳn nút Thêm dòng · Xóa dòng · Áp dụng · Phân bổ
Kịch bản  S-012
```

### R-CTBH-017 · Bộ nút màn Xem chi tiết
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_XemChiTiet.md:23-41 (bảng Chức năng + BR1)
WHEN      mở màn Xem chi tiết
THEN      hiện đúng bộ nút: Chỉnh sửa (R-CTBH-008) · Ghi sổ (R-CTBH-008) ·
          Bỏ ghi sổ (R-CTBH-009) · Lập hóa đơn (R-CTBH-011) ·
          Xem dữ liệu ghi sổ (luôn hiện, R-CTBH-107) · Đóng (luôn hiện)
Ghi chú   nút "Lập phiếu xuất kho" — xem R-CTBH-019, đang CHỜ C07
Kịch bản  S-012
```

### R-CTBH-018 · Khu chi tiết dưới lưới — 4 tab
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_DanhSach.md:171-212 (BR08)
WHEN      người dùng đổi tiêu điểm dòng trên lưới danh sách
THEN      khu chi tiết nạp lại theo dòng tiêu điểm, gồm 4 tab: Chi tiết hàng hóa (mặc định)
          · Thuế · Đính kèm · Tham chiếu; toàn bộ chỉ đọc; phân trang riêng
ELSE      tích/bỏ tích checkbox KHÔNG đổi tiêu điểm
Kịch bản  S-013
```

### R-CTBH-019 · Nút "Lập phiếu xuất kho" trên Xem chi tiết
```
Tầng      FE              Sev  P1        Trạng thái  CHỜ C07
Nguồn     — (hai nguồn bậc 4 mâu thuẫn, xem 01-conflict.md#c07)
CẤM CODE cho tới khi C07 chuyển CLOSED-BA.
```

### R-CTBH-020 · Khu chi tiết kiểm quyền trước khi trả dữ liệu
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_DanhSach.md:175-177 (BR08)
WHEN      client gọi API lấy dữ liệu khu chi tiết mà không có BanHangHoa.View.Detail
THEN      API từ chối, KHÔNG trả dữ liệu — không được chỉ ẩn ở giao diện
Lỗi       MSG_PMKT-E-06194_007          Kịch bản  S-030
```

---

## Nhóm 3 — Thêm mới (`R-CTBH-021…075`)

### R-CTBH-021 · Nguồn khách hàng — vai trò KhachHang
```
Tầng      BE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:392-395 (BR01.1)
WHEN      combogrid "Mã khách hàng" truy vấn danh sách (mọi tab)
THEN      lọc mst_doi_tuong có bản ghi mst_doi_tuong_vai_tro với iam_vai_tro = KhachHang;
          tìm theo mst_doi_tuong.Code hoặc .Ten
Ghi chú   đối tượng kiêm vai trò NCC/Nhân viên vẫn xuất hiện nếu có vai trò KhachHang
BR chung  BR5 · BR6 (combogrid)          Kịch bản  S-014
```

### R-CTBH-022 · Auto-fill thông tin khách hàng theo tab
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:405-458 (BR01.2a — 5 bảng ánh xạ theo tab)
WHEN      người dùng chọn Mã khách hàng ở tab bất kỳ
THEN      điền các trường theo đúng bảng ánh xạ của tab đó; LoaiDoiTuong = ToChuc lấy
          MaSoThue/NguoiLienHe, = CaNhan lấy SoCCCD/Ten
ELSE      đổi Mã khách hàng → điền lại theo khách hàng mới (BR01.d)
Ghi chú   trường auto-fill vẫn cho người dùng sửa
Kịch bản  S-014
```

### R-CTBH-023 · Auto-fill TK công nợ dòng đầu tiên
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:465-471 (BR01.2b)
WHEN      chọn Mã khách hàng AND mst_doi_tuong_vai_tro.TaiKhoanCongNoPhaiThuId có giá trị
THEN      TK công nợ của DÒNG ĐẦU TIÊN lưới chi tiết := giá trị đó
ELSE      lấy theo định khoản ngầm định (R-CTBH-069)
Bất biến  INV-012         Kịch bản  S-014
```

### R-CTBH-024 · Template diễn giải đầu chứng từ
```
Tầng      CẢ HAI          Sev  P2
Nguồn     SCR_CTBH_ThemMoi.md:475-493 (BR01.c1)
WHEN      chọn khách hàng / nhập số hóa đơn
THEN      3 trường điền theo template [Prefix] + "bán hàng" + [{TenKhachHang}]
          + [theo hóa đơn số {SoHoaDon}]; Prefix = "" (ghi nợ) / "Xuất kho " (PXK) /
          "Thu tiền " (phiếu thu, giấy báo có)
Ghi chú   giữ NGUYÊN VĂN chuỗi tiếng Việt làm giá trị i18n
Kịch bản  S-015
```

### R-CTBH-025 · Validate định dạng MST tổ chức
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:500 (BR01.d) · :1597 (Validation)
WHEN      khách hàng LoaiDoiTuong = ToChuc AND người dùng nhập tay MaSoThueCCCD
          AND giá trị KHÔNG khớp (10 chữ số) HOẶC (10 số + "-" + 3 số)
THEN      chặn lưu
Lỗi       MSG_PMKT-E-06194_050          Kịch bản  S-016
```

### R-CTBH-026 · Validate định dạng CCCD cá nhân
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:500 (BR01.d) · :1598
WHEN      khách hàng LoaiDoiTuong = CaNhan AND nhập tay MaSoThueCCCD ≠ đúng 12 chữ số
THEN      chặn lưu
Lỗi       MSG_PMKT-E-06194_051          Kịch bản  S-016
```

### R-CTBH-027 · Đồng bộ trường chung giữa các tab
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:505-508 (BR02.a)
WHEN      người dùng sửa một trường thuộc nhóm Thông tin chung tại một trong 4 tab
          (Chứng từ ghi nợ · Phiếu xuất kho · Phiếu thu · Giấy báo có)
THEN      cập nhật trường tương ứng sang các tab còn lại CÓ trường đó
ELSE      tab không có trường tương ứng thì bỏ qua
Kịch bản  S-017
```

### R-CTBH-028 · Tab Hóa đơn đồng bộ một chiều
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:510-518 (BR02.b)
WHEN      sửa tại Tab Hóa đơn
THEN      KHÔNG cập nhật ngược các tab khác
WHEN      sửa tại tab khác AND Mã KH tab Hóa đơn = Mã KH tab đó
THEN      sửa Mã KH → auto-fill lại toàn bộ tab Hóa đơn; sửa trường khác → chỉ cập nhật
          nếu trường đó đang GIỐNG nhau giữa hai tab
ELSE      Mã KH khác nhau → không cập nhật tab Hóa đơn
Kịch bản  S-017
```

### R-CTBH-029 · Đồng bộ Ngày hạch toán, không đồng bộ Ngày chứng từ
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:520-531 (BR02.c, BR02.d)
WHEN      người dùng đổi Ngày hạch toán tại một trong 4 tab
THEN      cập nhật Ngày hạch toán sang cả 3 tab còn lại (một ngày hạch toán cho cả bộ)
ELSE      đổi Ngày chứng từ tại một tab → KHÔNG đồng bộ sang tab khác
Ghi chú   Ngày hóa đơn: mặc định = Ngày chứng từ tab ghi nợ; chỉ cập nhật theo khi hai
          giá trị đang bằng nhau
Bất biến  INV-010         Kịch bản  S-018
```

### R-CTBH-030 · Sinh số chứng từ theo quy tắc đánh số
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1577 (BR25) · BR20 chung
WHEN      mở màn Thêm mới
THEN      sinh SoChungTu theo cfg_quy_tac_danh_so của LoaiChungTuId suy từ màn khởi tạo —
          Chứng từ bán hàng → tiền tố "BH"; Chứng từ bán dịch vụ → "BDV"
ELSE      KHÔNG hard-code tiền tố; khả năng sửa số theo cfg_quy_tac_danh_so.ChoPhepSuaSo
Lỗi       MSG_PMKT-E-06194_035 (trùng số)
Kịch bản  S-019
```

### R-CTBH-031 · Auto-calc Hạn thanh toán + cơ chế ngắt
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:537-542 (BR03)
WHEN      Ngày chứng từ hoặc Số ngày được nợ thay đổi AND người dùng CHƯA sửa tay Hạn thanh toán
THEN      Hạn thanh toán := Ngày chứng từ + Số ngày được nợ
ELSE      đã sửa tay → ngừng auto-calc vĩnh viễn; sửa tay Hạn thanh toán KHÔNG tính ngược
          ra Số ngày được nợ
Kịch bản  S-020
```

### R-CTBH-032 · Đồng bộ Hình thức TT sang tab Hóa đơn
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:544-554 (BR04)
WHEN      ThuTienNgay = false
THEN      Hình thức TT tab Hóa đơn := "TM/CK"
WHEN      ThuTienNgay = true
THEN      Hình thức TT tab Hóa đơn := Hình thức thanh toán ở Header (Tiền mặt / Chuyển khoản)
ELSE      người dùng đã sửa tay Hình thức TT → ngừng nhận đồng bộ
Ghi chú   Header có 2 giá trị, tab Hóa đơn có 3 giá trị + cho nhập tay ngoài combo
Kịch bản  S-021
```

### R-CTBH-033 · Loại trừ 2 checkbox hóa đơn
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:558-561 (BR05.1)
WHEN      DaLapHoaDon = checked
THEN      disable và uncheck LapKemHoaDon
ELSE      DaLapHoaDon = unchecked → enable LapKemHoaDon
Ghi chú   checkbox "Đã lập hóa đơn" chỉ hiện khi LapKemHoaDon = unchecked
Kịch bản  S-022
```

### R-CTBH-034 · Tự tích "Đã lập hóa đơn" khi có HĐ lập sau
```
Tầng      BE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:568-575 (BR05.3, BR05.4)
WHEN      chứng từ có LapKemHoaDon = false AND DaLapHoaDon = false
          AND lưu hóa đơn ĐẦU TIÊN chọn nguồn là chứng từ này
THEN      DaLapHoaDon := true (hệ thống tự tích) → disable cả 2 checkbox ở màn Sửa
ELSE      xóa TẤT CẢ hóa đơn lập từ chứng từ → DaLapHoaDon := false
Ghi chú   tự tích này KHÔNG kích hoạt khởi tạo counter (R-CTBH-064)
Kịch bản  S-023
```

### R-CTBH-035 · Ẩn cả cột nhóm kho khi không phát sinh kho
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:965-971 (BR17)
WHEN      LoaiNghiepVu = "Bán dịch vụ" OR KiemPhieuXuatKho = false
THEN      ẩn HẲN cột (không render): Kho · Tự nhập đơn giá · Đơn giá vốn · Tiền vốn ·
          TK giá vốn · TK kho · Số lô · Hạn sử dụng
ELSE      cột đang hiện mà dòng có Loại hàng hóa = Dịch vụ → ô của dòng đó để trống,
          không cho nhập
Ghi chú   dùng ẩn, KHÔNG dùng disable
Kịch bản  S-024
```

### R-CTBH-036 · Chặn lưu khi toàn dòng Dịch vụ mà tích kiêm PXK
```
Tầng      CẢ HAI          Sev  P1        Trạng thái  CHỜ C10 (chỉ phần message)
Nguồn     SCR_CTBH_ThemMoi.md:1013 (BR18.2) · :1303 (BR21.1)
WHEN      KiemPhieuXuatKho = true AND KHÔNG có dòng nào Loại hàng hóa = Hàng hóa
THEN      chặn lưu
Lỗi       MSG_PMKT-E-06194_109 — MÃ NÀY KHÔNG TỒN TẠI trong 6.messages.md, xem C10
Ghi chú   điều kiện chặn đã rõ, code được; nội dung message thì CHỜ BA
Kịch bản  S-025
```

### R-CTBH-037 · Xác định dòng phát sinh xuất kho
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:977-989 (BR17, bảng 5 dòng)
WHEN      KiemPhieuXuatKho = true, xét TỪNG DÒNG lưới chi tiết
THEN      dòng phát sinh xuất kho + tính giá vốn ⟺ Loại hàng hóa = Hàng hóa
          AND KHÔNG tích Chiết khấu thương mại AND LoaiDongHang = true
          (dòng Hàng khuyến mại VẪN phát sinh xuất kho và VẪN tính giá vốn)
ELSE      không đưa vào phiếu xuất kho, không tính giá vốn
Bất biến  INV-008         Kịch bản  S-026, S-027
```

### R-CTBH-038 · Auto-fill từ danh mục vật tư
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:592-605 (BR07, bảng 10 dòng)
WHEN      chọn Mã hàng hóa trên một dòng
THEN      điền Tên hàng hóa (TenBan, trống thì Ten) · ĐVT · Kho · TK doanh thu ·
          TK giá vốn · TK kho · Tài khoản CK · % thuế GTGT · Giá trị thuế GTGT · % Thuế XK
          theo đúng bảng ánh xạ ENT_mst_vat_tu
ELSE      vật tư không cấu hình trường nào → để trống trường đó
Ghi chú   Loại hàng hóa suy từ mst_loai_vat_tu: "Dịch vụ" → Dịch vụ; còn lại → Hàng hóa
Kịch bản  S-026
```

### R-CTBH-039 · Trường tự do trên dòng chi tiết
```
Tầng      CẢ HAI          Sev  P2
Nguồn     SCR_CTBH_ThemMoi.md:255-262 · BR6 chung
WHEN      render lưới chi tiết
THEN      có 6 cột tự do: Đối tượng THCP · Vụ việc · Đơn vị · Khoản mục chi phí ·
          Đơn đặt hàng · Hợp đồng bán hàng — không bắt buộc, cho sửa, quy tắc theo BR6 chung
Kịch bản  S-026
```

### R-CTBH-040 · Thêm dòng — giá trị mặc định
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:614-623 (BR08)
WHEN      bấm "Thêm dòng" AND lưới đã có ≥ 1 dòng AND dòng cuối là dòng hàng thường
THEN      dòng mới: SoLuong = 1, DonGia = 0, ThanhTien = 0; chép từ dòng cuối:
          Mã hàng hóa · Tên hàng hóa · TK công nợ · TK doanh thu · ĐVT · % thuế GTGT · TK Thuế GTGT
ELSE      lưới rỗng → chỉ đặt mặc định cơ bản
Kịch bản  S-028
```

### R-CTBH-041 · Thêm dòng sau dòng KM/CKTM — chỉ chép TK
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:624-628 (BR08)
WHEN      dòng cuối có LaHangKhuyenMai = true OR LaChietKhauThuongMai = true
THEN      dòng mới CHỈ chép các cột tài khoản (TK công nợ · TK doanh thu · Tài khoản CK ·
          TK Thuế GTGT · TK giá vốn · TK kho · TK Thuế XK); mọi thông tin khác về mặc định
ELSE      dòng cuối là dòng ghi chú → không chép gì
Ghi chú   2 checkbox KM và CKTM LUÔN unchecked ở dòng mới
Kịch bản  S-028
```

### R-CTBH-042 · Dòng ghi chú không tham gia tính toán
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:299 · :833 · :888
WHEN      LoaiDongHang = false (dòng ghi chú)
THEN      disable toàn bộ cột trừ Tên hàng hóa; KHÔNG tính vào Σ nào; KHÔNG sinh bút toán;
          KHÔNG áp ràng buộc bắt buộc; DienGiai = NULL
Bất biến  INV-011         Kịch bản  S-029
```

### R-CTBH-043 · Hai checkbox KM/CKTM loại trừ nhau
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:633 (BR09)
WHEN      tích LaHangKhuyenMai trên một dòng
THEN      disable LaChietKhauThuongMai của dòng đó (và ngược lại)
ELSE      cả hai loại dòng đều disable Tỷ lệ CK (%) · Tiền CK · Tiền CK quy đổi
Kịch bản  S-031
```

### R-CTBH-044 · Dòng KM ghi nhận đúng giá trị nhập
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:635-645 (BR09.a) · :1253 (BR20.3)
WHEN      dòng có LaHangKhuyenMai = true
THEN      mở khóa Đơn giá / Thành tiền / Tiền thuế GTGT (gợi ý 0, cho sửa); hạch toán
          ĐÚNG giá trị người dùng nhập — Thành tiền > 0 thì sinh bút toán doanh thu,
          Tiền thuế GTGT > 0 thì sinh bút toán thuế
ELSE      Thành tiền = 0 → không ghi nhận doanh thu
Ghi chú   % thuế GTGT VẪN bắt buộc chọn; dòng KM vẫn vào PXK và vẫn tính giá vốn
Kịch bản  S-031, S-032
```

### R-CTBH-045 · Dòng CKTM mang Thành tiền âm
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:647-651 (BR09.b) · :1161 (BR20 #3)
WHEN      dòng có LaChietKhauThuongMai = true
THEN      ThanhTien lưu giá trị ÂM; hiển thị trên lưới ở dạng dương;
          bút toán #3 dùng ABS(ThanhTien) — Nợ TK Doanh thu / Có TK Công nợ
ELSE      disable Kho · TK kho · TK giá vốn · Đơn giá vốn · Tiền vốn — không phát sinh giá vốn
Bất biến  INV-008         Kịch bản  S-033
```

### R-CTBH-046 · Công thức Thành tiền 2 chiều
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:682-684 (BR11.1)
WHEN      người dùng sửa SoLuong hoặc DonGia
THEN      ThanhTien := SoLuong × DonGia
WHEN      người dùng sửa trực tiếp ThanhTien AND SoLuong > 0
THEN      DonGia := ThanhTien / SoLuong
ELSE      SoLuong = 0 → xem R-CTBH-047
BR chung  BR7 (precision & làm tròn)          Kịch bản  S-034
```

### R-CTBH-047 · Số lượng = 0 → ép Đơn giá 0, giữ Thành tiền
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:686-691 (BR11.2)
WHEN      người dùng nhập SoLuong = 0
THEN      DonGia := 0 NGAY LẬP TỨC và GIỮ NGUYÊN ThanhTien hiện có
ELSE      KHÔNG tính lại ThanhTien = 0 × DonGia; KHÔNG chia cho 0
Ghi chú   dòng SoLuong = 0 mà ThanhTien ≠ 0 VẪN cộng vào Tổng tiền hàng
Kịch bản  S-035
```

### R-CTBH-048 · Đơn vị tính quy đổi — 3 cột hiển thị
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:657-678 (BR10)
WHEN      ĐVT đã chọn ≠ ĐVT cơ bản của vật tư
THEN      hiện 3 cột tính tại chỗ (KHÔNG lưu DB): Hệ số quy đổi = HeSo ·
          Số lượng quy đổi = SoLuong × HeSo · Đơn giá quy đổi = DonGia / HeSo
ELSE      ĐVT = ĐVT cơ bản → hệ số = 1, ẩn 3 cột; HeSo = 0 → Đơn giá quy đổi = 0, không chia
Kịch bản  S-036
```

### R-CTBH-049 · Chiết khấu theo mặt hàng — tính 2 chiều
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:713-721 (BR12.a)
WHEN      LoaiChietKhau = "Theo mặt hàng" AND người dùng nhập TyLeChietKhau
THEN      TienChietKhau := ThanhTien × TyLeChietKhau
WHEN      người dùng nhập TienChietKhau AND ThanhTien > 0
THEN      TyLeChietKhau := TienChietKhau / ThanhTien
ELSE      ThanhTien = 0 → TyLeChietKhau := 0 (tránh chia 0)
Ghi chú   Giá trị tính thuế dòng i = ThanhTien − TienChietKhau
Kịch bản  S-037
```

### R-CTBH-050 · CK theo mặt hàng — nhập tay, tính 2 chiều
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:747-754 (BR12.d bước 1-2) — chốt theo C08 (CLOSED-AUTO)
WHEN      LoaiChietKhau = "Theo mặt hàng và hóa đơn" AND chọn Mã hàng hóa có cấu hình
          Tỷ lệ CK theo mặt hàng trên ENT_mst_vat_tu
THEN      auto-fill TyLeChietKhauTheoHang cho dòng đó
WHEN      người dùng nhập TyLeChietKhauTheoHang
THEN      TienChietKhauTheoHang := ThanhTien × TyLeChietKhauTheoHang
ELSE      nhập TienChietKhauTheoHang AND ThanhTien > 0 → tính ngược ra tỷ lệ;
          ThanhTien = 0 → tỷ lệ := 0
Kịch bản  S-038
```

### R-CTBH-051 · CK theo hóa đơn — cơ sở sau CK mặt hàng
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:755-762 (BR12.d bước 3-4) — chốt theo C08
WHEN      đã hoàn tất CK theo mặt hàng
THEN      Thành tiền sau CK mặt hàng (i) = ThanhTien(i) − TienChietKhauTheoHang(i);
          TienChietKhauTheoHoaDon(i) = Thành tiền sau CK mặt hàng (i) × TyLeChietKhauTheoHoaDon;
          TienChietKhau(i) = TienChietKhauTheoHang(i) + TienChietKhauTheoHoaDon(i);
          TyLeChietKhau(i) = TienChietKhau(i) / ThanhTien(i) × 100 (ThanhTien > 0)
ELSE      2 cột tổng hợp (TienChietKhau, TyLeChietKhau) là DISABLED; sửa tay chúng KHÔNG
          cập nhật ngược 4 cột thành phần
Ghi chú   bỏ qua dòng KM và CKTM
Bất biến  INV-006         Kịch bản  S-038
```

### R-CTBH-052 · Chiết khấu theo % hóa đơn — nút Áp dụng
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:723-729 (BR12.b)
WHEN      LoaiChietKhau = "Theo % hóa đơn" AND người dùng nhập X% rồi bấm "Áp dụng"
THEN      TienChietKhau(i) := ThanhTien(i) × X% cho MỌI dòng hàng
ELSE      bỏ qua dòng KM và dòng CKTM; 2 cột Tiền CK / Tỷ lệ CK trên lưới DISABLED
Lỗi       MSG_PMKT-E-06194_043 (% CK > 100)
Kịch bản  S-039
```

### R-CTBH-053 · Dòng tổng lưới chi tiết — bỏ dòng ghi chú
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_ThemMoi.md:266-301 (bảng 19 chỉ tiêu)
WHEN      render dòng tổng cuối lưới Chi tiết hàng hóa
THEN      Σ trên TẤT CẢ dòng hàng, BỎ dòng ghi chú (LoaiDongHang = false); nhóm Đơn giá và
          nhóm tỷ lệ % KHÔNG có dòng tổng
ELSE      LoaiTien = đồng tiền hạch toán → ẩn cột quy đổi và ẩn luôn dòng tổng tương ứng;
          cột Tiền vốn chỉ hiện khi KiemPhieuXuatKho = true; cột thuế XK chỉ hiện khi
          LoaiNghiepVu = Bán hàng xuất khẩu
BR chung  BR31            Kịch bản  S-040
```

### R-CTBH-054 · Ràng buộc Tiền CK ≤ Thành tiền dòng
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:784-790 (BR12.f)
WHEN      dòng hàng THƯỜNG có TienChietKhau > ThanhTien của dòng
THEN      CHẶN LƯU
WHEN      dòng KM hoặc CKTM có TienChietKhau > ThanhTien
THEN      chỉ CẢNH BÁO Yes/No (tiếp tục / hủy), KHÔNG chặn lưu
ELSE      dòng có TienChietKhau ≠ 0 mà chưa nhập TaiKhoanChietKhauId → chặn lưu
Lỗi       MSG_PMKT-E-06194_044 · MSG_PMKT-E-06194_010 {tenTruong} = Tài khoản CK
Bất biến  INV-006         Kịch bản  S-041, S-042
```

### R-CTBH-055 · PBCK — phân bổ theo giá trị / số lượng
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_PBCK.md:48-56 (BR1, BR2) — trạng thái cột chốt theo C09
WHEN      phương thức = "Theo giá trị"
THEN      TienCK(i) = Số tiền × ThanhTien(i) / Σ ThanhTien; Tỷ lệ phân bổ(i) =
          ThanhTien(i) / Σ ThanhTien × 100; hai cột Tỷ lệ phân bổ và Tiền CK phân bổ DISABLE
WHEN      phương thức = "Theo số lượng"
THEN      TienCK(i) = Số tiền × SoLuong(i) / Σ SoLuong; tỷ lệ tương ứng; hai cột DISABLE
Ghi chú   PBCK_MHHD dùng "Thành tiền sau CK mặt hàng" thay cho "Thành tiền"
Kịch bản  S-043
```

### R-CTBH-056 · PBCK — phân bổ thủ công, 2 cột enable
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_PBCK.md:58-64 (BR3) — chốt theo C09 (CLOSED-AUTO)
WHEN      phương thức = "Thủ công"
THEN      cả Tỷ lệ phân bổ và Tiền CK phân bổ ENABLE; sửa Tỷ lệ → Tiền CK = Số tiền × Tỷ lệ / 100;
          sửa Tiền CK → Tỷ lệ = Tiền CK / Số tiền × 100
ELSE      sửa "Số tiền" thì phải bấm "Phân bổ" để tính lại theo tỷ lệ hiện tại
Kịch bản  S-043
```

### R-CTBH-057 · PBCK — dòng cuối bù chênh lệch làm tròn
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_PBCK.md:79-85 (BR7)
WHEN      phân bổ theo giá trị hoặc theo số lượng
THEN      tính cho mọi dòng TRỪ dòng cuối theo công thức; Tiền CK dòng cuối =
          Số tiền − Σ(Tiền CK các dòng trước); Tỷ lệ dòng cuối = 100 − Σ(tỷ lệ trước)
Bất biến  INV-007         Kịch bản  S-044
```

### R-CTBH-058 · PBCK — bỏ qua dòng KM/CKTM
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_PBCK.md:66-72 (BR4, BR5)
WHEN      dựng lưới phân bổ
THEN      dòng LaHangKhuyenMai = true hoặc LaChietKhauThuongMai = true KHÔNG hiển thị và
          KHÔNG được phân bổ
Kịch bản  S-043
```

### R-CTBH-059 · PBCK — validate tổng tỷ lệ = 100%
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_PBCK.md:74-77 (BR6)
WHEN      bấm "Áp dụng" AND Σ Tỷ lệ phân bổ ≠ 100
THEN      chặn, MSG_PMKT-E-06194_048
WHEN      Tỷ lệ phân bổ của một dòng ngoài [0, 100]
THEN      chặn, MSG_PMKT-E-06194_047
ELSE      Số tiền CK > Σ Thành tiền → chặn, MSG_PMKT-E-06194_044
Ghi chú   `_044` vốn là message MỨC DÒNG nhưng BR6 dùng cho lỗi MỨC TỔNG — sai ngữ nghĩa,
          BA nên rà (không chặn code)
Kịch bản  S-045
```

### R-CTBH-060 · Counter HĐ khởi tạo khi LapKemHoaDon
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1482 (BR23.4) · UC_CTBH_ThemMoi.md:26 (khớp)
WHEN      lưu chứng từ LẦN ĐẦU AND LapKemHoaDon = true
THEN      với MỖI DÒNG HÀNG: SoLuongDaXuatHoaDon := SoLuong (mức DÒNG, không mức chứng từ)
Bất biến  INV-005         Kịch bản  S-046
```

### R-CTBH-061 · Counter HĐ khởi tạo khi DaLapHoaDon
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1483 (BR23.4)
WHEN      lưu chứng từ LẦN ĐẦU AND DaLapHoaDon = true (do NGƯỜI DÙNG tự tích)
THEN      với mỗi dòng hàng: SoLuongDaXuatHoaDon := SoLuong
ELSE      DaLapHoaDon do HỆ THỐNG tự tích (R-CTBH-034) → KHÔNG chạy luật này
Bất biến  INV-005         Kịch bản  S-047
```

### R-CTBH-062 · Counter kho khởi tạo khi KiemPhieuXuatKho
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1484 (BR23.4)
WHEN      lưu chứng từ LẦN ĐẦU AND KiemPhieuXuatKho = true
THEN      với mỗi dòng có Loại hàng hóa = Hàng hóa: SoLuongDaXuatKho := SoLuong
ELSE      dòng Dịch vụ không đặt counter kho
Bất biến  INV-004         Kịch bản  S-046
```

### R-CTBH-063 · Counter = 0 khi checkbox không chọn
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1485 (BR23.4)
WHEN      checkbox tương ứng = false lúc lưu lần đầu
THEN      counter tương ứng giữ = 0
Kịch bản  S-048
```

### R-CTBH-064 · Khởi tạo counter chỉ chạy lần lưu đầu
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1479 (BR23.4 — khối "Phạm vi của mục 4")
WHEN      lưu SỬA chứng từ đã tồn tại
THEN      KHÔNG khởi tạo lại counter; counter chỉ đổi qua tạo/sửa/xóa hóa đơn (BR23.5)
          hoặc phiếu xuất kho (BR23.6)
ELSE      chạy lại sẽ ép counter = SoLuong dù hóa đơn mới lập một phần
Bất biến  INV-005         Kịch bản  S-049
```

### R-CTBH-065 · Sinh bản ghi chứng từ con khi Lưu
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:997-1005 (BR18.1) · UC_CTBH_ThemMoi.md:25
WHEN      Lưu chứng từ (kể cả chỉ "Lưu", chưa ghi sổ)
THEN      KiemPhieuXuatKho = true → sinh ENT_inv_phieu_xuat_kho + chi tiết, với
            inv_phieu_xuat_kho.NguonId = sal_chung_tu_ban.Id, LoaiChungTuNguon = ChungTuBan;
          ThuTienNgay = true → sinh ENT_cash_phieu_thu + chi tiết, liên kết qua
            cash_phieu_thu_chi_tiet.ChungTuBanId;
          LapKemHoaDon = true → sinh ENT_sal_hoa_don_ban_hang + chi tiết, liên kết qua
            sal_hoa_don_ban_hang.ChungTuBanId và …_chi_tiet.ChiTietChungTuBanId
ELSE      các bản ghi con cũng ở trạng thái "Chưa ghi sổ"
Bất biến  INV-002         Kịch bản  S-046, S-050
```

### R-CTBH-066 · Bỏ tích checkbox → xóa bản ghi con
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1007 (BR18.1)
WHEN      bỏ tích checkbox rồi Lưu lại AND phiếu con đang "Chưa ghi sổ"
THEN      xóa bản ghi phần tương ứng
ELSE      phiếu con đang "Đã ghi sổ" → không xóa được, phải bỏ ghi sổ trước (BR21)
Kịch bản  S-051
```

### R-CTBH-067 · Phiếu con tự cấp số theo loại của nó
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1021 (BR18.3) · :1578 (BR25)
WHEN      sinh phiếu con
THEN      mỗi phiếu tự cấp số theo cfg_quy_tac_danh_so của LOẠI CHỨNG TỪ CỦA CHÍNH NÓ —
          Phiếu xuất kho "PXK" · Phiếu thu tiền mặt "PT" · Giấy báo có "GBC";
          số lưu tại inv_phieu_xuat_kho.SoChungTu / cash_phieu_thu.SoChungTu
ELSE      chứng từ bán KHÔNG lưu số của phiếu con
Kịch bản  S-046
```

### R-CTBH-068 · Ngày hạch toán dùng chung 3 phần
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1023 (BR18.3)
WHEN      sinh phiếu con
THEN      NgayHachToan của cả 3 phần = sal_chung_tu_ban.NgayHachToan
ELSE      NgayChungTu của từng phiếu lấy giá trị người dùng nhập trên tab tương ứng
Bất biến  INV-010         Kịch bản  S-018
```

### R-CTBH-069 · Tài khoản lấy theo định khoản ngầm định
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:900-945 (BR16 mục 1-3)
WHEN      xác định giá trị mặc định của một cột tài khoản trên dòng
THEN      lấy theo thứ tự, gặp giá trị đầu tiên thì dừng:
          (1) cấu hình riêng trên danh mục (mst_vat_tu / mst_doi_tuong_vai_tro)
          (2) cfg_tai_khoan_ngam_dinh_chi_tiet.TaiKhoanMacDinhId của dòng vai trò tương ứng
          (3) để trống
ELSE      đổi LoaiNghiepVu / ThuTienNgay / HinhThucThanhToan → tra lại định khoản và áp lại
          cho các dòng CHƯA bị người dùng sửa tay; dòng đã sửa tay giữ nguyên
Ghi chú   tổ hợp tra định khoản theo bảng 8 dòng tại BR16 mục 1
Kịch bản  S-052
```

### R-CTBH-070 · Chỉ chọn tài khoản cấp cuối trong bộ lọc
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:947-952 (BR16.4)
WHEN      mở dropdown một cột tài khoản
THEN      chỉ hiện tài khoản nằm trong cfg_tai_khoan_ngam_dinh_chi_tiet.LocTaiKhoan của
          dòng vai trò đó AND có ChoPhepHachToan = Có
ELSE      LocTaiKhoan trống → cho chọn toàn bộ ENT_mst_he_thong_tai_khoan (vẫn chỉ cấp cuối)
WHEN      giá trị đang chọn không còn hợp lệ lúc lưu
THEN      chặn lưu, MSG_PMKT-E-06194_107
BR chung  BR28 (tenant)   Bất biến  INV-012          Kịch bản  S-053
```

### R-CTBH-071 · Hai luồng tiền tệ độc lập
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:702-709 (BR11.5) · :866,877 (BR14) · :843 (BR13.6)
WHEN      tính bất kỳ cột quy đổi nào
THEN      cột quy đổi tính TỪ các cột quy đổi, cột nguyên tệ tính từ cột nguyên tệ —
          KHÔNG nhân tỷ giá lần nữa lên số đã quy đổi
ELSE      người dùng sửa trực tiếp cột quy đổi → KHÔNG tính ngược Giá trị gốc / Tỷ giá,
          lưu đúng giá trị người dùng nhập
Ghi chú   Tiền thuế GTGT quy đổi = (ThanhTienQuyDoi − TienChietKhauQuyDoi) × Thuế suất,
          KHÔNG dùng "giá trị gốc × tỷ giá"
BR chung  BR18 chung (ngoại tệ) · BR7
Bất biến  INV-013         Kịch bản  S-054
```

### R-CTBH-072 · Tổng thanh toán cộng dồn từng dòng
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:364 (Section Tổng hợp #5)
WHEN      tính TongThanhToan
THEN      = Σ theo TỪNG DÒNG của (Thành tiền − Tiền CK + Tiền thuế GTGT) — cộng dồn từng
          dòng để không làm tròn nhiều lần; KHÔNG cộng thuế XK
ELSE      giá trị âm → hiển thị màu đỏ trong ngoặc đơn
BR chung  BR7             Bất biến  INV-003          Kịch bản  S-055
```

### R-CTBH-073 · Công thức Tiền thuế GTGT
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:810-817 (BR13.3)
WHEN      tính TienThueGTGT của một dòng
THEN      = (ThanhTien − TienChietKhau) × Thuế suất, trong đó Thuế suất =
          Giá trị thuế GTGT / 100 nếu % thuế = KHAC; 0 nếu KCT hoặc KKKNT;
          giá trị enum / 100 cho các mức số
ELSE      người dùng sửa trực tiếp TienThueGTGT → KHÔNG cập nhật ngược Thuế suất
Ghi chú   LoaiNghiepVu = Bán hàng xuất khẩu → ẩn hẳn cột Tiền thuế GTGT / quy đổi /
          TK Thuế GTGT và cả Tab Thuế (BR13.5); cột % thuế GTGT vẫn hiện
Kịch bản  S-056
```

### R-CTBH-074 · Lưu là một transaction, lỗi thì rollback hết
```
Tầng      BE              Sev  P0
Nguồn     UC_CTBH_ThemMoi.md:34,95 (AC5 + Hậu điều kiện)
WHEN      bất kỳ bước nào lỗi (validate / sinh phiếu xuất / hóa đơn / phiếu thu / ghi sổ)
THEN      KHÔNG lưu chứng từ bán VÀ không giữ lại bất kỳ chứng từ liên quan nào sinh trong
          phiên đó — rollback toàn bộ trong một giao dịch
Bất biến  INV-002         Kịch bản  S-057
```

### R-CTBH-075 · Giữ nguyên dữ liệu form khi lỗi
```
Tầng      FE              Sev  P1
Nguồn     UC_CTBH_ThemMoi.md:88 · UC_CTBH_ChinhSua.md:80
WHEN      validate / lưu / ghi sổ thất bại
THEN      giữ nguyên toàn bộ dữ liệu đã nhập trên form, không reset, không đóng form;
          highlight trường vi phạm
ELSE      form chỉ đóng khi lưu thành công hoặc người dùng bấm "Đóng"
Kịch bản  S-057
```

---

## Nhóm 4 — Chỉnh sửa (`R-CTBH-076…082`)

### R-CTBH-076 · Nút Sửa chỉ khi Chưa ghi sổ + có quyền
```
Tầng      CẢ HAI          Sev  P1
Nguồn     UC_CTBH_ChinhSua.md:8 · SCR_CTBH_XemChiTiet.md:37 (BR1)
WHEN      TrangThaiGhiSo = "Chưa ghi sổ" AND có quyền BanHangHoa.Edit
THEN      hiện nút Sửa          ELSE ẩn
Lỗi       MSG_PMKT-E-06194_016 (khi truy cập trực tiếp chứng từ đã ghi sổ)
Kịch bản  S-058
```

### R-CTBH-077 · Màn Sửa hiện 4 trường theo dõi số lượng
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_CapNhat.md:22 · ThemMoi BR23.8 (:1544)
WHEN      mở màn Sửa (hoặc Xem chi tiết)
THEN      hiện readonly trên lưới: Số lượng đã xuất HĐ · Số lượng đã xuất kho ·
          Số lượng còn lại xuất HĐ (= SoLuong − SoLuongDaXuatHoaDon) ·
          Số lượng còn lại xuất kho (= SoLuong − SoLuongDaXuatKho)
ELSE      màn Thêm mới ẩn 4 trường này
Kịch bản  S-059
```

### R-CTBH-078 · Điều kiện sửa chứng từ đã có liên kết
```
Tầng      CẢ HAI          Sev  P0        Trạng thái  CHỜ C06
Nguồn     — (UC_ChinhSua AC1 vs BR23.9, xem 01-conflict.md#c06)
CẤM CODE cho tới khi C06 chuyển CLOSED-BA.
```

### R-CTBH-079 · Disable checkbox HĐ khi hệ thống tự tích
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_CapNhat.md:23-26 · ThemMoi BR05.4 (:572-575)
WHEN      DaLapHoaDon đang tích DO HỆ THỐNG tự tích (đã tồn tại hóa đơn sinh từ chứng từ)
THEN      disable cả DaLapHoaDon lẫn LapKemHoaDon
ELSE      đang unchecked, hoặc đang tích do NGƯỜI DÙNG tự tích → cho sửa lại
Kịch bản  S-060
```

### R-CTBH-080 · Sửa CTBH → cập nhật lại phiếu con, giữ số
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1051 (BR18.6)
WHEN      sửa chứng từ bán đang "Chưa ghi sổ"
THEN      cập nhật lại phiếu xuất kho / phiếu thu liên kết theo dữ liệu mới;
          SoChungTu đã cấp của phiếu GIỮ NGUYÊN
Bất biến  INV-002         Kịch bản  S-061
```

### R-CTBH-081 · Ràng buộc SoLuong_moi ≥ MAX(counter)
```
Tầng      BE              Sev  P0        Trạng thái  CHỜ C06
Nguồn     — (BR23.9 mô tả luật này nhưng UC_ChinhSua cấm sửa, xem C06)
CẤM CODE cho tới khi C06 chuyển CLOSED-BA.
Ghi chú   nếu C06 chốt phương án A: SoLuong_moi ≥ MAX(SoLuongDaXuatHoaDon, SoLuongDaXuatKho)
          — dùng MAX, KHÔNG dùng tổng (hai counter theo dõi cùng lượng hàng vật lý)
```

### R-CTBH-082 · Chứng từ đã ghi sổ không sửa SoLuong
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1553 (BR23.9)
WHEN      TrangThaiGhiSo = "Đã ghi sổ"
THEN      không cho sửa SoLuong trên dòng hàng
ELSE      muốn sửa phải Bỏ ghi sổ trước
Kịch bản  S-062
```

---

## Nhóm 5 — Xóa (`R-CTBH-083…090`)

### R-CTBH-083 · Quyền xóa
```
Tầng      CẢ HAI          Sev  P1
Nguồn     UC_CTBH_Xoa.md:29 · SCR_CTBH_PopupXacNhanXoa.md:45-47 (BR03)
WHEN      không có quyền BanHangHoa.Delete
THEN      ẩn nút Xóa và Xóa hàng loạt
Lỗi       MSG_PMKT-E-06194_007          BR chung  BR25.2
Kịch bản  S-030
```

### R-CTBH-084 · Popup xác nhận trước khi xóa
```
Tầng      FE              Sev  P1
Nguồn     SCR_CTBH_PopupXacNhanXoa.md:17-19
WHEN      bấm Xóa hoặc Xóa hàng loạt
THEN      hiện popup chuẩn BR3 chung: tiêu đề "Xác nhận xóa", icon cảnh báo, nội dung,
          nút Đồng ý / Hủy; bản hàng loạt nêu SỐ chứng từ được chọn
ELSE      người dùng hủy → đóng popup, không xóa
Kịch bản  S-063
```

### R-CTBH-085 · Chỉ xóa chứng từ Chưa ghi sổ
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_PopupXacNhanXoa.md:32-36 (BR01) · :71-77 (BR06 — thứ tự kiểm)
WHEN      TrangThaiGhiSo = "Đã ghi sổ"
THEN      chặn xóa (kiểm ĐẦU TIÊN, trước kiểm "đã sử dụng")
Lỗi       MSG_PMKT-E-06194_013
Bất biến  INV-001         Kịch bản  S-064
```

### R-CTBH-086 · Chính sách xóa hàng loạt
```
Tầng      CẢ HAI          Sev  P0        Trạng thái  CHỜ C01
CẤM CODE cho tới khi C01 chuyển CLOSED-BA.
```

### R-CTBH-087 · Trạng thái nút Xóa hàng loạt
```
Tầng      FE              Sev  P0        Trạng thái  CHỜ C01
CẤM CODE cho tới khi C01 chuyển CLOSED-BA.
```

### R-CTBH-088 · Điều kiện "đã sử dụng ở nghiệp vụ khác"
```
Tầng      CẢ HAI          Sev  P0        Trạng thái  CHỜ C02 · C03 · C04
CẤM CODE cho tới khi cả ba mục chuyển CLOSED-BA. Đây là luật bị chặn bởi nhiều mục nhất —
xóa chứng từ là chức năng không code được ở đợt này nếu BA chưa chốt.
```

### R-CTBH-089 · Cascade xóa mềm chứng từ con
```
Tầng      BE              Sev  P0        Trạng thái  CHỜ C05
CẤM CODE cho tới khi C05 chuyển CLOSED-BA.
Ghi chú   phần KHÔNG tranh chấp, code được ngay: xóa mềm (IsDeleted = true) theo BR29.1
          chung, KHÔNG xóa vật lý — SCR_CTBH_PopupXacNhanXoa.md:68
```

### R-CTBH-090 · Counter và điều kiện chặn xóa
```
Tầng      BE              Sev  P0        Trạng thái  CHỜ C04
CẤM CODE cho tới khi C04 chuyển CLOSED-BA.
```

---

## Nhóm 6 — Ghi sổ (`R-CTBH-091…099`)

### R-CTBH-091 · Quyền ghi sổ
```
Tầng      CẢ HAI          Sev  P1
Nguồn     UC_CTBH_GhiSo.md:29 · UC_CTBH_ThemMoi.md:30 (AC5)
WHEN      không có BanHangHoa.Post
THEN      ẩn nút Ghi sổ; nút "Lưu và ghi sổ" chỉ hiện khi có ĐỒNG THỜI Create/Edit và Post
Lỗi       MSG_PMKT-E-06194_007          Kịch bản  S-065
```

### R-CTBH-092 · Chặn ghi sổ vào kỳ đã khóa
```
Tầng      BE              Sev  P0
Nguồn     business_rules.md BR17 (bậc 5) — epic im lặng, chốt theo C11 (CLOSED-AUTO)
WHEN      NgayHachToan của chứng từ thuộc kỳ kế toán đã khóa
THEN      chặn ghi sổ / bỏ ghi sổ / xóa
Lỗi       theo BR17 chung (MSG_PMKT-E-07528_026) — KHÔNG tự đặt mã mới trong namespace 06194
Bất biến  INV-014         Kịch bản  S-066
```

### R-CTBH-093 · Sinh bút toán chứng từ bán — 5 bút toán
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1157-1164 (BR20.1) · :1227-1234 (BR20.2c)
WHEN      ghi sổ, quét TỪNG DÒNG HÀNG
THEN      sinh các bút toán thỏa điều kiện:
          #1 Nợ TaiKhoanCongNoId / Có TaiKhoanDoanhThuId = ThanhTien — khi ThanhTien > 0
             và dòng không phải CKTM
          #2 Nợ TaiKhoanChietKhauId / Có TaiKhoanCongNoId = TienChietKhau — khi TienCK > 0
          #3 Nợ TaiKhoanDoanhThuId / Có TaiKhoanCongNoId = ABS(ThanhTien) — dòng CKTM
          #4 Nợ TaiKhoanCongNoId / Có TaiKhoanThueGTGTId = TienThueGTGT — bán trong nước,
             TienThueGTGT > 0
          #5 Nợ TaiKhoanDoanhThuId / Có TaiKhoanThueXKId = TienThueXK — bán hàng xuất khẩu
ELSE      TK lấy ĐÚNG giá trị cột TK trên dòng, KHÔNG tra lại định khoản ngầm định (BR16.5)
Ghi chú   giá vốn do PHIẾU XUẤT KHO sinh, thu tiền do PHIẾU THU sinh — chứng từ bán không
          sinh hộ (BR18.4, BR20.4)
Bất biến  INV-001, INV-002          Kịch bản  S-067, S-068
```

### R-CTBH-094 · Mỗi bút toán sinh 2 bản ghi sổ cái
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1169 (BR20.2) · :1206-1215 (bảng b)
WHEN      sinh một bút toán
THEN      tạo 2 bản ghi acc_so_cai cùng STTButToan: bản vế Nợ có TKId = TK Nợ,
          TKDoiUngId = TK Có, PSNo/PSNoQuyDoi = số tiền, PSCo = PSCoQuyDoi = 0;
          bản vế Có đảo ngược
ELSE      TK / TKDoiUng lưu snapshot SỐ HIỆU tài khoản lúc ghi sổ
Bất biến  INV-001         Kịch bản  S-067
```

### R-CTBH-095 · Bút toán gắn đúng dòng chi tiết
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1151 (BR20.1) · :1237
WHEN      sinh bản ghi acc_so_cai
THEN      ChiTietChungTuId := sal_chung_tu_ban_chi_tiet.Id của dòng sinh ra nó;
          STTDongChiTiet := .ThuTu; MỖI DÒNG sinh bút toán riêng, KHÔNG cộng dồn giữa các dòng
ELSE      số bản ghi của một dòng = số bút toán thỏa điều kiện × 2
Bất biến  INV-002         Kịch bản  S-067
```

### R-CTBH-096 · Ghi sổ hàng loạt — partial success
```
Tầng      CẢ HAI          Sev  P0
Nguồn     UC_CTBH_GhiSo.md:17 (AC3) · SCR_CTBH_DanhSach.md:82 · BR45 chung
WHEN      ghi sổ hàng loạt và có chứng từ không hợp lệ
THEN      ghi sổ các chứng từ hợp lệ, BỎ QUA chứng từ lỗi, không dừng tiến trình;
          hiện popup kết quả MSG_PMKT-E-06194_108 kèm số thành công / thất bại
ELSE      tất cả thành công → không hiện popup cảnh báo
Ghi chú   cấu trúc popup theo BR45 mục 3 chung
Kịch bản  S-069
```

### R-CTBH-097 · Ghi sổ đồng bộ cả nhóm chứng từ liên kết
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1317-1330 (BR21.3)
WHEN      ghi sổ hoặc bỏ ghi sổ BẤT KỲ chứng từ nào trong nhóm kiêm
          (chứng từ bán · phiếu xuất kho kiêm · phiếu thu kiêm)
THEN      áp cho TOÀN NHÓM trong MỘT giao dịch; mỗi chứng từ ghi bút toán của mình
ELSE      phiếu LẬP RIÊNG không thuộc nhóm — trạng thái độc lập
Bất biến  INV-002         Kịch bản  S-070
```

### R-CTBH-098 · Một chứng từ trong nhóm lỗi → chặn cả nhóm
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1332 (BR21.3)
WHEN      một chứng từ trong nhóm không hợp lệ
THEN      chặn thao tác cho CẢ NHÓM, không ghi sổ một phần
Bất biến  INV-002         Kịch bản  S-071
```

### R-CTBH-099 · Hóa đơn không đồng bộ ghi sổ
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1334 (BR21.3) · :1069 (BR18.8)
WHEN      ghi sổ / bỏ ghi sổ chứng từ bán
THEN      KHÔNG đụng tới trạng thái hóa đơn lập kèm — hóa đơn có vòng đời và trạng thái
          phát hành riêng, KHÔNG sinh bút toán
Kịch bản  S-070
```

---

## Nhóm 7 — Bỏ ghi sổ (`R-CTBH-100…106`)

### R-CTBH-100 · Quyền bỏ ghi sổ
```
Tầng      CẢ HAI          Sev  P1
Nguồn     UC_CTBH_BoGhiSo.md:28
WHEN      không có BanHangHoa.Unpost → ẩn nút; truy cập trực tiếp → chặn
Lỗi       MSG_PMKT-E-06194_007
WHEN      chứng từ đang "Chưa ghi sổ" mà gọi bỏ ghi sổ → chặn, MSG_PMKT-E-06194_023
Kịch bản  S-030
```

### R-CTBH-101 · Chặn bỏ ghi sổ khi phiếu thu lập riêng đã ghi sổ
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1338 (BR21.4) · :1423 (BR22.2) · UC_CTBH_BoGhiSo.md:52
WHEN      tồn tại phiếu thu / giấy báo có LẬP RIÊNG (luồng Thu tiền theo hóa đơn, nhận diện
          qua cash_chung_tu_cong_no_phieu_thu.ChungTuBanId) đang ở trạng thái "Đã ghi sổ"
THEN      chặn bỏ ghi sổ, yêu cầu bỏ ghi sổ phiếu đó trước
Lỗi       MSG_PMKT-E-06194_049
ELSE      phần thu tiền KIÊM (ThuTienNgay = true) KHÔNG chặn — gỡ đồng thời theo R-CTBH-097
Kịch bản  S-072
```

### R-CTBH-102 · Chặn bỏ ghi sổ khi đang tham gia đối trừ
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1339 (BR21.4) · UC_CTBH_BoGhiSo.md:53
WHEN      tồn tại ktth_chung_tu_doi_tru_chi_tiet.ChungTuCongNoId trỏ tới chứng từ này
THEN      chặn bỏ ghi sổ, yêu cầu XÓA phiếu đối trừ trước
Lỗi       MSG_PMKT-E-06194_052
ELSE      hệ thống KHÔNG tự xóa phiếu đối trừ (một phiếu ghép nhiều chứng từ nguồn)
Kịch bản  S-073
```

### R-CTBH-103 · PXK lập riêng không chặn bỏ ghi sổ
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1340 (BR21.4) · :1348-1355 (BR21.5.1)
WHEN      tồn tại phiếu xuất kho LẬP RIÊNG liên kết, ở bất kỳ trạng thái nào
THEN      KHÔNG chặn bỏ ghi sổ chứng từ bán — hai chứng từ có trạng thái ghi sổ độc lập
Kịch bản  S-074
```

### R-CTBH-104 · Bỏ ghi sổ xóa toàn bộ định khoản
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1286 (BR20.6) · :1341 (BR21.4)
WHEN      bỏ ghi sổ hợp lệ
THEN      xóa TOÀN BỘ bản ghi acc_so_cai của chứng từ; xóa các dòng sổ công nợ có
          ChungTuId = chứng từ; phiếu kiêm bỏ ghi sổ đồng thời và tự xóa bút toán của mình
          (gỡ khỏi Sổ kho, xóa bút toán giá vốn, xóa bút toán thu tiền);
          TrangThaiGhiSo := "Chưa ghi sổ"
Lỗi       MSG_PMKT-E-06194_005 (thành công) · MSG_PMKT-E-06194_022 (lỗi hệ thống)
Bất biến  INV-002         Kịch bản  S-075
```

### R-CTBH-105 · Bỏ ghi sổ không đổi trạng thái xuất hàng / lập HĐ
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1381-1382 (BR22) · :1352-1359 (BR21.5) · UC_CTBH_BoGhiSo.md:71
WHEN      ghi sổ hoặc bỏ ghi sổ
THEN      TrangThaiLapHoaDon và TrangThaiXuatHang KHÔNG đổi — counter chỉ đổi khi
          tạo/sửa/xóa hóa đơn hoặc phiếu xuất kho liên kết
Bất biến  INV-004, INV-005          Kịch bản  S-074
```

### R-CTBH-106 · Bỏ ghi sổ trừ lại SoTienDaThanhToan
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_ThemMoi.md:1421-1424 (BR22.2)
WHEN      bỏ ghi sổ chứng từ bán có phần thu tiền KIÊM
THEN      gỡ luôn phần thu tiền, trừ lại đúng số đã cộng vào SoTienDaThanhToan trong
          CÙNG giao dịch; tính lại TrangThaiThanhToan theo BR22 mục 1
ELSE      SoTienDaThanhToan = 0 → "Chưa thanh toán"; ≥ TongThanhToan → "Đã thanh toán";
          0 < x < TongThanhToan → "Đã thanh toán một phần"
Bất biến  INV-003         Kịch bản  S-076
```

---

## Nhóm 8 — Xem dữ liệu ghi sổ (`R-CTBH-107…112`)

### R-CTBH-107 · Nút Xem dữ liệu ghi sổ luôn hiển thị
```
Tầng      FE              Sev  P2
Nguồn     SCR_CTBH_XemDuLieuGhiSo.md:97 (BR01)
WHEN      ở màn Thêm mới / Chỉnh sửa / Xem chi tiết
THEN      nút "Xem dữ liệu ghi sổ" LUÔN hiện, không phụ thuộc trạng thái ghi sổ;
          form không có mã quyền riêng
Kịch bản  S-077
```

### R-CTBH-108 · Hai chế độ dữ liệu theo trạng thái ghi sổ
```
Tầng      CẢ HAI          Sev  P0
Nguồn     SCR_CTBH_XemDuLieuGhiSo.md:100-117 (BR02)
WHEN      chứng từ "Chưa ghi sổ" (kể cả chưa Lưu lần nào)
THEN      chế độ Xem trước — tính tại chỗ theo BR20, CÙNG thuật toán với chức năng Ghi sổ,
          nguồn là dữ liệu đang có trên form
WHEN      chứng từ "Đã ghi sổ"
THEN      chế độ Dữ liệu sổ — đọc trực tiếp acc_so_cai, KHÔNG tính lại
ELSE      chế độ chọn theo TRẠNG THÁI CHỨNG TỪ, không theo màn gọi
Kịch bản  S-077, S-078
```

### R-CTBH-109 · Chế độ Xem trước không ghi dữ liệu
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_XemDuLieuGhiSo.md:111,116 (BR02)
WHEN      ở chế độ Xem trước
THEN      KHÔNG tạo bản ghi acc_so_cai, KHÔNG cấp số chứng từ; bút toán trả về không có
          Id / ChungTuId / ChiTietChungTuId
Bất biến  INV-002         Kịch bản  S-077
```

### R-CTBH-110 · Phạm vi bút toán = cả nhóm liên kết
```
Tầng      BE              Sev  P0
Nguồn     SCR_CTBH_XemDuLieuGhiSo.md:119-136 (BR03)
WHEN      dựng dữ liệu form
THEN      gồm bút toán của CẢ NHÓM: chứng từ bán (luôn) + phiếu xuất kho (khi
          KiemPhieuXuatKho) + phiếu thu (khi ThuTienNgay); hóa đơn KHÔNG sinh bút toán
ELSE      chế độ Dữ liệu sổ lọc acc_so_cai theo CẶP (ChungTuId, LoaiChungTuId) — ChungTuId
          là FK đa hình, chỉ duy nhất khi đi kèm loại chứng từ
Ghi chú   acc_so_kho KHÔNG thuộc phạm vi form
Kịch bản  S-078
```

### R-CTBH-111 · Xem trước thiếu TK → bỏ bút toán đó, không chặn
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_XemDuLieuGhiSo.md:138-142 (BR04)
WHEN      ở chế độ Xem trước, dòng hàng chưa chọn đủ TK của một bút toán
THEN      KHÔNG sinh bút toán đó, các bút toán còn lại vẫn hiển thị
ELSE      form KHÔNG chặn và KHÔNG hiện thông báo validate — validate chỉ ở nút Lưu /
          Lưu và ghi sổ của màn gọi; chưa có Số chứng từ → cột để trống
Kịch bản  S-079
```

### R-CTBH-112 · Thứ tự sắp xếp bút toán, không gộp
```
Tầng      CẢ HAI          Sev  P1
Nguồn     SCR_CTBH_XemDuLieuGhiSo.md:144-149 (BR05)
WHEN      hiển thị lưới bút toán
THEN      nhóm theo chứng từ: chứng từ bán → phiếu xuất kho → phiếu thu; trong mỗi chứng từ
          sắp xếp tăng dần STTDongChiTiet → STTButToan; hai vế của cùng bút toán đứng liền
          nhau, vế Nợ trước
ELSE      KHÔNG gộp bút toán giống nhau — mỗi bản ghi acc_so_cai là một dòng lưới
Kịch bản  S-078
```

---

## Bất biến (`INV-001…014`)

### INV-001 · Cân đối Nợ = Có
```
Phát biểu       Với mọi chứng từ đã ghi sổ: Σ PSNo = Σ PSCo và Σ PSNoQuyDoi = Σ PSCoQuyDoi
Nguồn           SCR_CTBH_ThemMoi.md:1169 (BR20.2) — mỗi bút toán sinh đúng 2 bản ghi đối ứng
Luật liên quan  R-CTBH-093, R-CTBH-094
Cách kiểm       ghi sổ chứng từ đủ 5 loại bút toán → tổng hai vế bằng nhau
```

### INV-002 · Ghi sổ và sinh chứng từ con là nguyên tử
```
Phát biểu       Không tồn tại trạng thái trung gian: hoặc chứng từ bán + mọi chứng từ con
                cùng tồn tại/cùng ghi sổ, hoặc không có gì
Nguồn           UC_CTBH_ThemMoi.md:34,95 · SCR_CTBH_ThemMoi.md:1319 (BR21.3)
Luật liên quan  R-CTBH-065, R-CTBH-074, R-CTBH-097, R-CTBH-098
Cách kiểm       ép lỗi ở bước sinh phiếu thu → không còn bản ghi nào của chứng từ bán
```

### INV-003 · SoTienDaThanhToan không âm và khớp trạng thái
```
Phát biểu       0 ≤ SoTienDaThanhToan; TrangThaiThanhToan luôn suy đúng từ cặp
                (SoTienDaThanhToan, TongThanhToan) theo BR22 mục 1
Nguồn           SCR_CTBH_ThemMoi.md:1398-1401 (BR22.1)
Luật liên quan  R-CTBH-072, R-CTBH-106
Cách kiểm       ghi sổ rồi bỏ ghi sổ phiếu thu nhiều lần → giá trị về đúng 0
```

### INV-004 · SoLuongDaXuatKho ≤ SoLuong
```
Phát biểu       Với MỌI dòng chi tiết, mọi thời điểm: SoLuongDaXuatKho ≤ SoLuong
Nguồn           SCR_CTBH_ThemMoi.md:1527 (BR23.6.2)
Luật liên quan  R-CTBH-062, R-CTBH-105
Cách kiểm       test tương tranh S-080
```

### INV-005 · SoLuongDaXuatHoaDon ≤ SoLuong
```
Phát biểu       Với MỌI dòng chi tiết, mọi thời điểm: SoLuongDaXuatHoaDon ≤ SoLuong
Nguồn           SCR_CTBH_ThemMoi.md:1499,1509 (BR23.5.2, 5.3)
Luật liên quan  R-CTBH-060, R-CTBH-061, R-CTBH-064
Cách kiểm       test tương tranh S-081
```

### INV-006 · Tiền CK không vượt Thành tiền (dòng thường)
```
Phát biểu       Với dòng hàng thường (không KM, không CKTM): TienChietKhau ≤ ThanhTien
Nguồn           SCR_CTBH_ThemMoi.md:786 (BR12.f)
Luật liên quan  R-CTBH-051, R-CTBH-054
Cách kiểm       nhập Tiền CK vượt → chặn lưu với MSG_…_044
```

### INV-007 · Tổng phân bổ khớp số tiền nhập
```
Phát biểu       Sau phân bổ: Σ Tiền CK phân bổ các dòng = Số tiền CK nhập ở header (chính xác
                tuyệt đối sau làm tròn) và Σ Tỷ lệ phân bổ = 100
Nguồn           SCR_CTBH_PBCK.md:79-85 (BR7)
Luật liên quan  R-CTBH-057, R-CTBH-059
Cách kiểm       phân bổ 100.000 cho 3 dòng lẻ → tổng đúng 100.000, không lệch 1 đồng
```

### INV-008 · Dòng CKTM và dòng Dịch vụ không phát sinh giá vốn
```
Phát biểu       Dòng có LaChietKhauThuongMai = true hoặc Loại hàng hóa = Dịch vụ không xuất
                hiện trong inv_phieu_xuat_kho_chi_tiet và không sinh bút toán giá vốn
Nguồn           SCR_CTBH_ThemMoi.md:977-989 (BR17) · :651 (BR09.b)
Luật liên quan  R-CTBH-037, R-CTBH-045
Cách kiểm       chứng từ 1 dòng hàng + 1 dòng CKTM + 1 dòng dịch vụ → PXK chỉ có 1 dòng
```

### INV-009 · Trạng thái xuất hàng NULL khi không có dòng hàng hóa
```
Phát biểu       Chứng từ không có dòng nào Loại hàng hóa = Hàng hóa → TrangThaiXuatHang = NULL
Nguồn           SCR_CTBH_ThemMoi.md:1394 (BR22.1)
Luật liên quan  R-CTBH-014
Cách kiểm       chứng từ bán dịch vụ thuần → trường trả null, FE không vỡ khi parse
```

### INV-010 · Một ngày hạch toán cho cả bộ chứng từ
```
Phát biểu       sal_chung_tu_ban.NgayHachToan = inv_phieu_xuat_kho.NgayHachToan =
                cash_phieu_thu.NgayHachToan của cùng bộ chứng từ kiêm
Nguồn           SCR_CTBH_ThemMoi.md:1023 (BR18.3) · :520-524 (BR02.c)
Luật liên quan  R-CTBH-029, R-CTBH-068
Cách kiểm       đổi ngày hạch toán ở tab phiếu thu rồi lưu → cả 3 bản ghi cùng ngày
```

### INV-011 · Dòng ghi chú trung lập với mọi tổng
```
Phát biểu       Dòng LoaiDongHang = false không đóng góp vào bất kỳ Σ nào và không sinh
                bản ghi acc_so_cai nào
Nguồn           SCR_CTBH_ThemMoi.md:299 · :833
Luật liên quan  R-CTBH-042, R-CTBH-053
Cách kiểm       thêm dòng ghi chú vào chứng từ đã tính → mọi tổng không đổi
```

### INV-012 · Mọi tài khoản hạch toán là tài khoản cấp cuối
```
Phát biểu       Mọi TKId / TKDoiUngId trong acc_so_cai trỏ tới tài khoản có ChoPhepHachToan = Có
Nguồn           SCR_CTBH_ThemMoi.md:950-952 (BR16.4)
Luật liên quan  R-CTBH-023, R-CTBH-069, R-CTBH-070
Cách kiểm       đổi tài khoản trên danh mục thành tài khoản cha rồi lưu → chặn MSG_…_107
```

### INV-013 · Hai luồng tiền tệ không trộn
```
Phát biểu       Với chứng từ cùng đồng tiền hạch toán: PSNo = PSNoQuyDoi và TyGia = 1.
                Với chứng từ ngoại tệ: PSNoQuyDoi = PSNo × acc_so_cai.TyGia
Nguồn           SCR_CTBH_ThemMoi.md:1279-1280 (BR20.5)
Luật liên quan  R-CTBH-006, R-CTBH-071
Cách kiểm       chứng từ USD tỷ giá 25.000 → hai cột lệch đúng hệ số, không lệch làm tròn
```

### INV-014 · Không hạch toán vào kỳ đã khóa
```
Phát biểu       Không tồn tại bản ghi acc_so_cai có NgayHachToan thuộc kỳ kế toán đã khóa
Nguồn           business_rules.md BR17 (bậc 5) — chốt qua C11
Luật liên quan  R-CTBH-092
Cách kiểm       khóa kỳ rồi ghi sổ chứng từ trong kỳ → chặn
```
