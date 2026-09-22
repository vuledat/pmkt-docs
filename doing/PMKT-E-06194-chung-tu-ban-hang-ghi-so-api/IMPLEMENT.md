# IMPLEMENT — PMKT-E-06194 ghi sổ chứng từ bán hàng

## 1. Ngày và phạm vi

- Ngày triển khai: 2026-09-08.
- Đã triển khai phần chắc chắn của plan: truyền các chiều phân tích đã tồn tại trên dòng CTBH vào `DinhKhoan` và khóa hồi quy bằng unit test.
- Chưa triển khai Q2 (đối tượng tập hợp chi phí/đơn đặt hàng) vì plan yêu cầu BA xác nhận nguồn dữ liệu trước khi thêm cột.
- Chưa thay đổi contract endpoint hoặc nghiệp vụ ghi sổ nhóm; luồng hiện có đã dùng `ChungTuTemplate`/`GhiSoApi`.

## 2. File đã sửa/tạo

| File | Vai trò |
|---|---|
| `cell-app/src/main/java/vn/vtt/pmkt/cell/ban_hang/chung_tu_ban_hang/internal/service/business/DinhKhoanBanHang.java` | Truyền `donViId`, `vuViecId`, `hopDongId`, diễn giải dòng từ chi tiết sang `DinhKhoan`. |
| `cell-app/src/test/java/vn/vtt/pmkt/cell/ban_hang/chung_tu_ban_hang/internal/service/business/QuyTacMoiBanHang2026Test.java` | Test `R-CTBH-093` bảo đảm chiều phân tích đi theo từng dòng. |
| `docs/json/PMKT-E-06194-chung-tu-ban-hang-ghi-so.postman_collection.json` | Collection kiểm tra các endpoint ghi sổ kế thừa. |

## 3. Đã kế thừa

- `ChungTuTemplate`: transaction, kiểm quyền, ghi sổ và rollback.
- `TaoDinhKhoanApi`/`TaoDinhKhoanService`: tạo nhiều cặp tài khoản, gộp/bù trừ cặp đảo chiều.
- `GhiSoApi`/`GhiSoService`: duy nhất tạo hai dòng Nợ/Có trong `acc_so_cai`.
- `DinhKhoan`: các builder `voiDonVi`, `voiVuViec`, `voiHopDong`, `voiDienGiaiDong`.

Không viết repository hoặc endpoint mới vì không cần mở rộng contract API.

## 4. Migration

Không thêm migration. Schema `acc_so_cai` đã có chiều phân tích; các field được triển khai đã tồn tại trên `sal_chung_tu_ban_hang_chi_tiet`. Hai field chưa có nguồn (`doiTuongTapHopChiPhiId`, `donDatHangId`) chờ Q2.

## 5. Lệch so với plan

- Plan dự kiến có thể thêm hai field Q2; chưa làm vì câu hỏi BA chưa được trả lời, theo cổng gen-be không được tự đặt nguồn dữ liệu.
- Chưa bổ sung integration test DB nhóm vì môi trường cấm Docker; cần chạy ở CI/IntelliJ có datasource.

## 6. Nợ kỹ thuật

- Cần test integration S-067, S-070, S-071, S-075 trên DB thật.
- Cần BA chốt Q1 về fallback #6/#7 và Q2 về hai chiều phân tích còn thiếu.
- Ghi sổ hàng loạt partial success R-CTBH-096 chưa thuộc lát cắt triển khai này.

## 7. Kết quả cổng

- Targeted unit tests: `./gradlew unitTest --tests '*QuyTacMoiBanHang2026Test' --tests '*TinhToanVaDinhKhoanBanHangTest'` — **BUILD SUCCESSFUL**.
- Full `./gradlew unitTest`: **BUILD SUCCESSFUL** trong 2m 56s.
- Testcontainers/integration DB: chưa chạy vì môi trường cấm Docker.

## 8. Postman

`docs/json/PMKT-E-06194-chung-tu-ban-hang-ghi-so.postman_collection.json` gồm 5 request: ghi sổ, bỏ ghi sổ, xem hạch toán, ghi sổ hàng loạt và tìm kiếm.

## 9. BR/truy vết

Đã áp dụng trực tiếp: R-CTBH-093, R-CTBH-095; kế thừa kernel cho R-CTBH-094, INV-001, INV-002 và nhóm R-CTBH-097–099. Các luật còn thiếu test integration được báo là nợ kỹ thuật, không kết luận hoàn thành toàn bộ.

Kết quả script cổng hiện tại:

- `trace.sh ... be`: `Tong 93 luat (tang=be): OK 0 · NO-TEST 2 · MISSING 84 · BLOCKED 7 · VI-PHAM 0`.
- `msg.sh ... be`: `Tong 60 message (tang=be): OK 31 · LECH 0 · THIEU-VI 0 · CHUA-DAT 0 · THIEU 29`.

Các trạng thái `MISSING`/`BLOCKED` là phần truy vết của toàn epic hoặc phụ thuộc câu hỏi BA, không phải lỗi phát sinh trong lát cắt đã triển khai; không có `VI-PHAM`.
