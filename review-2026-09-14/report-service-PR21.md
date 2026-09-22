# Review PR #21 — `ospgroupvn-pmkt/report-service`

**Tiêu đề:** `feat: init bao cao CCDC` · tác giả `tichvd-osp` · `feat/bao-cao-ccdc` → `develop`
**Head:** `c80af9804d6a95c94ab12cd1b68fe8188d0aa29e` · **merge-base:** `caec7c306deb41b2e060f3d8b344a2e7a6dec29c` (= tip `origin/develop`, nhánh KHÔNG tụt)
**Diff:** 12 file · +4.533 / −9 · **Chế độ: NHANH** (chỉ đọc + kiểm tĩnh; KHÔNG chạy test/build, KHÔNG worktree, KHÔNG sửa code, KHÔNG đăng comment lên PR theo yêu cầu người gọi)

Phạm vi: hai báo cáo mới trong `report-service` — Báo cáo chi tiết CCDC (PMKT-E-10810) và Bảng tính phân bổ CCDC (PMKT-E-14616).

## Tổng kết

| Mức | Số lượng |
|---|---|
| Blocker | 0 |
| Major | 5 |
| Minor | 7 |
| Nit | 3 |

**Kết luận: REQUEST CHANGES** — 5 Major, chủ yếu là lệch chữ BA đang chờ BA chốt và khối SQL chưa từng được thực thi. Cổng test/build (`./gradlew :report-service:build`, `unitTest`) **chưa chạy** ở lượt này.

## Bốn lớp

| Lớp | Kết quả |
|---|---|
| A — Cổng cứng (9 luật) | OK — không secret, không hardcode text (mọi label qua `messages.properties`), không Controller mới, không Entity lộ ra ngoài, không đụng vùng đóng băng, không commit thẳng `develop` |
| B — 7 lỗi hay gặp | xem bảng dưới |
| C — Nghiệp vụ & truy vết | CÓ VẤN ĐỀ: M1–M4, m1, m4 |
| D — Vệ sinh diff & Git | CÓ VẤN ĐỀ: m5, m6, m7, n1–n3 |

## Bảng bảy lỗi

| # | Lỗi | Kết quả |
|---|---|---|
| 1 | Sai kiến trúc thư mục | OK — definition vào `internal/service/definitions/`, repository vào `internal/repository/`, đúng shape 9 báo cáo hiện có; không tạo `api/` thừa |
| 2 | Không đánh lại version migration | N/A — `report-service/src/main/resources/db/` chỉ có `bieu_mau/`, PR không thêm migration nào |
| 3 | Chưa test lại sau khi merge | N/A — `git rev-list --count <merge-base>..origin/develop` = **0** (merge-base chính là tip develop) nên 0 file giao nhau |
| 4 | N+1 / chưa tối ưu | OK — native SQL, không query trong vòng lặp, không lazy ngoài transaction; `@Transactional(readOnly = true)` có ở cả `fetchRows`/`dataVersion` (bắt buộc cho RLS). Chi phí truy vấn: n3 |
| 5 | Chưa tận dụng Base BE | OK — dùng `ReportDefinition`, `ReportDefinitionSupport.periodParams`/`rememberKey`, `PeriodLockFingerprint`, `NativeQueryMappers`; không tự viết controller |
| 6 | Chưa tận dụng base FE | N/A — PR thuần backend |
| 7 | Constant đặt sai chỗ | OK — mọi khóa cột/tham số/literal SQL đều là `private static final` đặt ngay trong lớp dùng, theo đúng khuôn các definition cũ. Mã `MSG_…` của epic: xem m4 |

## Kết quả công cụ tĩnh

| Công cụ | Kết quả |
|---|---|
| `trace.sh` | **NOT-RUN** — không có `docs/doing/*-spec/` cho PMKT-E-10810 lẫn PMKT-E-14616 (chưa chạy `/audit-spec`) |
| `msg.sh pmkt-docs/ba/PMKT-E-14616_BangTinhPhanBoCCDC be` | 6 message: **THIEU 6**, OK 0 — xem m4 (tool quét `cell-app`, không quét `report-service`) |
| i18n cross-check (`messages.properties` @head vs 2 definition) | **0 MISSING, 0 UNUSED** — 24 + 30 khóa khớp đúng |
| Compile-break do đổi chữ ký (`NativeQueryMappers.idsFilter/bindIds`: `List<UUID>` → `List<?>`) | OK — 3 caller cũ (`BangCanDoiTaiKhoan`, `BangKeChungTu`, `BaoCaoChiPhiTheoBoPhan`) đều truyền `List<UUID>` |
| API surface dùng trong diff (`ReportColumn` 20 component, `ReportColumnLink` 6, `ReportParamField` 14, `ReportGrouping` 5, `ReportLayout` 4, `ReportRow.detail`, `ReportPage.of`, `ReportDataVersion.open`, `PeriodLockFingerprint.tryFrozen`, `ReportParams.flag/uuid/stringList`) | khớp hết |
| Quyền `BCChiTietCCDC.View` / `BCPhanBoCCDC.View` | đã seed — `cell-app/src/main/resources/db/migration/V2__seed_data.sql:11280, 11356-11358` |
| Cổng cây commit | `git status --porcelain` sạch; PR là commit trên remote, không có file `??` |
