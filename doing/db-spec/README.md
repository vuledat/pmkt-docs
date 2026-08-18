# Đặc tả bảng dữ liệu — sinh từ `ba/Common/LDM_update`

> **Trạng thái:** `CHỜ REVIEW`  ·  Kế hoạch tổng: [`../plan-gen-db.md`](../plan-gen-db.md)
> Đọc [`00-chuan-chung.md`](00-chuan-chung.md) **trước** — mọi file dưới đây dựa trên chuẩn ở đó.

## Cách dùng

| Bạn muốn | Mở file |
|---|---|
| Xem chuẩn chung: trường base · domain type · quy tắc đặt tên · hạ tầng bắt buộc | [`00-chuan-chung.md`](00-chuan-chung.md) |
| Xem chi tiết trường của một phân hệ | file phân hệ ở bảng dưới |
| Xem toàn cảnh 206 entity × bảng DB × code, kèm hành động | [`90-doi-chieu.md`](90-doi-chieu.md) |

## Nhóm

| Nhóm | Nghĩa | Chi phí sửa |
|---|---|---|
| **A** | Có LDM · có schema · **có code** | **Cao** — ALTER + sửa entity + sửa FE + migrate dữ liệu |
| **B** | Có LDM · có schema · **chưa có code** | **Thấp** — sửa tự do, chưa có dữ liệu thật |
| **C** | Có LDM · **chưa có schema** | Thấp — CREATE mới |
| **?** | Chưa rà được | Pha 1 đối chiếu tay |

## Danh sách phân hệ

| File | Phân hệ | Bảng | A | B | C | ? | Trường | LDM chưa mô tả |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| [`10-acc-soketoan-update.md`](10-acc-soketoan-update.md) | Sổ kế toán (sổ cái · sổ kho) | 2 | 1 | 1 | · | · | 91 | · |
| [`11-iam-hethong.md`](11-iam-hethong.md) | Hệ thống · Tenant · Vai trò | 6 | 4 | · | 2 | · | 83 | · |
| [`12-iam-authentication.md`](12-iam-authentication.md) | Xác thực · Người dùng | 10 | 1 | · | 9 | · | 74 | 6 |
| [`13-iam-profilemanagement.md`](13-iam-profilemanagement.md) | Hồ sơ người dùng trong tenant | 2 | 1 | · | 1 | · | 19 | 2 |
| [`14-cfg-khoaso-update.md`](14-cfg-khoaso-update.md) | Khóa sổ kế toán | 3 | 3 | · | · | · | 17 | · |
| [`20-inv-kho-update.md`](20-inv-kho-update.md) | Kho | 28 | · | 16 | 12 | · | 355 | 3 |
| [`30-pur-muahang-update.md`](30-pur-muahang-update.md) | Mua hàng | 8 | 2 | 6 | · | · | 174 | · |
| [`31-pur-tralaihangmua.md`](31-pur-tralaihangmua.md) | Trả lại hàng mua | 3 | · | 2 | 1 | · | 63 | · |
| [`32-pur-dieuchinhgiahangmua.md`](32-pur-dieuchinhgiahangmua.md) | Điều chỉnh giá hàng mua | 2 | · | 2 | · | · | 53 | · |
| [`33-pur-doitrucongno-update.md`](33-pur-doitrucongno-update.md) | Đối trừ công nợ | 2 | · | 2 | · | · | 18 | 1 |
| [`40-sal-banhang-update.md`](40-sal-banhang-update.md) | Bán hàng | 9 | 2 | 1 | 6 | · | 348 | 7 |
| [`41-sal-tralaihangban.md`](41-sal-tralaihangban.md) | Trả lại hàng bán | 2 | · | 2 | · | · | 63 | 2 |
| [`42-sal-dieuchinhgiahangban.md`](42-sal-dieuchinhgiahangban.md) | Điều chỉnh giá hàng bán | 2 | · | 2 | · | · | 70 | 2 |
| [`50-cb-nganquy-update.md`](50-cb-nganquy-update.md) | Ngân quỹ (tiền mặt · tiền gửi) | 7 | · | 5 | 2 | · | 136 | 4 |
| [`60-fa-taisancodinh-update.md`](60-fa-taisancodinh-update.md) | Tài sản cố định | 27 | · | 26 | 1 | · | 248 | 19 |
| [`61-ccdc-ccdc.md`](61-ccdc-ccdc.md) | Công cụ dụng cụ | 18 | · | 15 | 2 | 1 | 117 | · |
| [`62-cptt-chiphitratruoc-update.md`](62-cptt-chiphitratruoc-update.md) | Chi phí trả trước | 6 | · | 5 | 1 | · | 68 | · |
| [`70-cst-giathanh.md`](70-cst-giathanh.md) | Giá thành | 18 | · | 14 | 4 | · | 125 | · |
| [`80-ktth-phieuktth.md`](80-ktth-phieuktth.md) | Phiếu kế toán tổng hợp | 3 | · | 3 | · | · | 61 | · |
| [`81-ktth-ketchuyenlailo.md`](81-ktth-ketchuyenlailo.md) | Kết chuyển lãi lỗ | 3 | · | · | 3 | · | 14 | · |
| [`82-fx-danhgialaingoaite.md`](82-fx-danhgialaingoaite.md) | Đánh giá lại ngoại tệ | 5 | · | · | 5 | · | 64 | · |
| [`83-sdbd-sodubandau.md`](83-sdbd-sodubandau.md) | Số dư ban đầu | 9 | · | 9 | · | · | 82 | · |
| [`85-tax-thue-update.md`](85-tax-thue-update.md) | Thuế | 21 | · | 1 | 20 | · | 232 | 7 |
| [`86-rpt-baocaotaichinh.md`](86-rpt-baocaotaichinh.md) | Báo cáo tài chính | 10 | · | 9 | 1 | · | 100 | · |
| **Tổng** | | **206** | **14** | **121** | **70** | **1** | **2675** | **53** |

## Ba điểm phải đọc trước khi review

1. **Trường base không lặp trong khối "Trường nghiệp vụ".** Mỗi bảng có khối *Trường base* riêng bên dưới — đó là bộ trường hệ thống theo BR46, hệ thống tự quản lý, không hiển thị trên form nhập.

2. **Cột "DB có — LDM không khai" không đồng nghĩa "phải xóa".** Ba khả năng: cột hạ tầng không thuộc LDM (giữ) · LDM đặt tên khác cho cùng khái niệm (đổi tên) · cột chết (DROP). Phải phân loại tay.

3. **53/206 bảng LDM chưa mô tả chức năng** — đánh dấu `⚠ LDM chưa mô tả bảng này` ở cả mục lục và khối *Mục đích*. Đây là khoảng trống ở tài liệu nguồn: BA cần thêm dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml`, sinh lại là tự cập nhật. Nặng nhất: `fa_` 19/27 · `tax_` 7/21 · `sal_` 7/9 · `iam_` 6/10.

4. **Kiểu dữ liệu có 60 trường gắn `⚠`** — hệ thống không suy được từ tên, đang tạm để `numeric(18,4)`. Đây là danh sách ngắn nhất cần anh chốt tay. Thêm 383 trường gắn `≈` (suy theo tên) nên soát lướt.

## Sinh lại

Mọi file `1x-…`–`8x-…` và `90-doi-chieu.md` **sinh tự động từ `.puml`**. Sửa LDM rồi sinh lại — **không sửa tay**, sửa tay sẽ mất ở lần sinh sau. Chỉ `00-chuan-chung.md` và `README.md` viết tay.

```bash
python3 docs/doing/db-spec/_gen.py
```

Script [`_gen.py`](_gen.py) đọc `.puml`, dựng lại schema hiện tại từ toàn bộ migration, rồi sinh 24 file phân hệ + ma trận đối chiếu. Map `CURRENT` trong script là **bảng chốt tay** LDM entity → bảng DB đang có — sửa ở đó khi rà thêm được entity mới.
