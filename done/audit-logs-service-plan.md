# Kế hoạch triển khai Audit Logs Service

## 1. Mục tiêu

Xây dựng một service Spring Boot độc lập để tập trung, tra cứu và xuất lịch sử tác động dữ liệu kế toán theo tenant. Service nhận audit do PostgreSQL tạo nguyên tử cùng giao dịch nghiệp vụ, vận chuyển qua Debezium/Kafka và lưu read model trong MongoDB. Bản lưu tuân thủ dài hạn phải nằm trên Object Storage có Object Lock/WORM; MongoDB không phải nguồn chứng cứ duy nhất.

## 2. Căn cứ và nguyên tắc tuân thủ

- Luật Kế toán 88/2015/QH13: tài liệu quản lý tối thiểu 5 năm; chứng từ dùng trực tiếp để ghi sổ, sổ kế toán và báo cáo tài chính tối thiểu 10 năm; tài liệu quan trọng có thể lưu vĩnh viễn.
- Nghị định 174/2016/NĐ-CP: phân loại tài liệu, thời điểm tính thời hạn, nơi lưu và thủ tục tiêu hủy.
- Luật Giao dịch điện tử 20/2023/QH15: bảo đảm khả năng truy cập và tính toàn vẹn của dữ liệu điện tử.
- Quy định bảo vệ dữ liệu cá nhân hiện hành: giới hạn mục đích, phân quyền, mã hóa, ghi nhận truy cập và không đưa secret vào audit.

Audit log là một biện pháp chứng minh; để tuân thủ còn cần retention matrix, quy chế lưu trữ/hủy, backup/restore, kiểm soát truy cập và bằng chứng vận hành được pháp chế/kế toán trưởng phê duyệt.

## 3. Kiến trúc mục tiêu

```text
Cell PostgreSQL transaction
  ├─ cập nhật dữ liệu nghiệp vụ
  └─ trigger ghi aud_audit_log (cùng transaction)
                 │
              Debezium
                 │
         Kafka audit topic
          ├─ Audit Logs Service ── MongoDB read model ── Query/Export API
          └─ S3 Sink ── Object Storage Object-Lock/WORM ── 5/10 năm/vĩnh viễn
```

### Ranh giới trách nhiệm

- `cell-app`: tạo data audit và business audit; bind `tenant_id`, `user_id`, request metadata.
- Debezium/Kafka: vận chuyển at-least-once và tách tải khỏi transaction nghiệp vụ.
- `audit-logs-service`: parse, validate, chống trùng, mask, lập chỉ mục, phân quyền và tra cứu.
- MongoDB: read model có thể rebuild.
- WORM archive: bản lưu dài hạn chống sửa/xóa, kèm manifest và checksum.

Không gửi REST đồng bộ từ mọi business service để thay trigger DB; lỗi mạng không được làm mất audit hoặc làm giao dịch kế toán phụ thuộc audit service.

## 4. Event model

Field tối thiểu:

| Nhóm | Field |
|---|---|
| Định danh | `event_id`, `schema_version`, `cell_id`, `tenant_id` |
| Actor | `actor_type`, `user_id`, `system_identity` |
| Đối tượng | `table_name`, `entity_type`, `record_id` |
| Hành động | `action`, `business_action`, `reason` |
| Dữ liệu | `before_data`, `after_data`, `changed_fields`, `data_classification` |
| Request | `request_id`, `trace_id`, `session_id`, `source_ip`, `user_agent`, `source_service` |
| CDC | `transaction_id`, `lsn`, `source_topic`, `partition`, `offset`, `commit_time` |
| Toàn vẹn | `payload_hash`, `previous_hash`, `signature` |
| Lưu trữ | `retention_class`, `retain_until`, `legal_hold` |

Không được lưu password, password hash, token, private key hoặc secret. CCCD, tài khoản ngân hàng và dữ liệu cá nhân nhạy cảm phải mask hoặc mã hóa theo field policy.

## 5. MongoDB

Collection `audit_events`; `_id = event_id` để ingest idempotent. Index bắt đầu bằng tenant:

- `{tenantId: 1, occurredAt: -1}`
- `{tenantId: 1, tableName: 1, recordId: 1, occurredAt: -1}`
- `{tenantId: 1, userId: 1, occurredAt: -1}`
- `{tenantId: 1, action: 1, occurredAt: -1}`
- unique `{eventId: 1}` thông qua `_id`

MongoDB production dùng replica set, TLS, encryption at rest, private network, backup định kỳ và credential read/write tách biệt. Nếu sharding, ưu tiên hashed tenant và đánh giá tenant nóng trước khi chốt shard key.

## 6. Kafka và Debezium

Giai đoạn đầu service có thể đọc topic raw `pmkt-cell-*.public.aud_audit_log`. Giai đoạn production nên tách audit lane và contract `pmkt.audit.v1` dùng Avro/Protobuf với Schema Registry.

Yêu cầu production:

- 3 broker, replication factor 3, `min.insync.replicas=2`.
- Không compact audit topic; retention Kafka chỉ phục vụ replay/outage, đề xuất 14–30 ngày.
- TLS/SASL và ACL producer/consumer.
- Replication slot/publication audit riêng khi tải đủ lớn.
- Retry hữu hạn, DLQ riêng, cảnh báo DLQ và consumer lag.
- DLQ mặc định `pmkt.audit.dlq.v1`; hạ tầng phải tạo topic với số partition tương thích source trước rollout.
- Theo dõi WAL retained size để Kafka/Connect outage không làm đầy PostgreSQL.

## 7. API và bảo mật

API MVP:

- `GET /api/v1/audit-events`
- `GET /api/v1/audit-events/{eventId}`
- sau MVP: history theo entity/request, export và verify.

Tenant lấy từ `X-Tenant-Id` nhưng bắt buộc phải xuất hiện trong claim `tenant_id` đã ký. Role tối thiểu: `AUDIT_VIEWER`, `AUDIT_EXPORTER`, `AUDIT_ADMIN`. Tenant user không được query tenant tùy ý. Truy cập chi tiết, export, verify và thao tác break-glass cũng phải sinh audit.

## 8. Kế hoạch phát triển

### Sprint 1 — Nền tảng và ingestion

- Scaffold Java 21/Spring Boot theo conventions repo.
- Kafka consumer đọc Debezium schema-less JSON.
- Validate các field bắt buộc; thiếu tenant đưa sang error handling/DLQ.
- Ghi Mongo bằng insert và `_id=event_id` để chống duplicate.
- Tạo index tenant/time/entity/user.
- Health, readiness, Prometheus.
- Unit test parser, duplicate delivery và malformed event.

### Sprint 2 — Query và tenant isolation

- API filter thời gian, user, bảng, record và action.
- Phân trang có giới hạn kích thước.
- API chi tiết không tiết lộ sự tồn tại của event tenant khác.
- JWT resource server, role và tenant allowlist.
- Policy mask dữ liệu theo bảng/field/role.
- Integration test Mongo, Kafka và cross-tenant.

Trạng thái code hiện tại: search, detail, entity history, recursive diff, checksum verification,
CSV/JSON export, Swagger/OpenAPI và Postman collection đã được triển khai. Integration test với
Kafka/Mongo thật và audit ngược thao tác xem/export vẫn thuộc bước hardening môi trường.

### Sprint 3 — Contract và compliance archive

- Canonical `AuditEventV1`, Schema Registry và compatibility policy.
- Audit lane/topic/DLQ riêng.
- S3 sink sang bucket bật Object Lock ngay từ lúc tạo.
- Retention class 5 năm/10 năm/vĩnh viễn; legal hold.
- File Avro/Parquet, manifest ngày/tenant/cell, SHA-256 và ký manifest bằng KMS/HSM.
- Object replication sang failure domain khác.
- Job đối soát DB/Kafka/Mongo/archive.

### Sprint 4 — Production hardening

- Bổ sung request/trace/IP/user-agent/actor-type vào nguồn audit.
- Mask/encrypt field nhạy cảm trước Kafka hoặc tại nguồn.
- Query history, diff, export và verify signature.
- Load test, Kafka/Mongo/Postgres failover, replay và restore drill.
- Dashboard connector status, slot lag, consumer lag, DLQ, archive delay và reconciliation gap.
- Runbook outage, WAL growth, replay, credential/key rotation, legal hold và tiêu hủy.
- Pilot một tenant, shadow reconciliation rồi rollout từng cell.

## 9. Kiểm thử nghiệm thu

1. Transaction thành công sinh đúng audit; rollback không sinh audit.
2. Kafka/Mongo ngừng không làm mất bản audit đã commit trong PostgreSQL.
3. Replay/duplicate không tạo thêm document logic.
4. Tenant A không đọc được event tenant B, kể cả biết event ID.
5. Secret và field bị cấm không xuất hiện trong Kafka, Mongo, DLQ hoặc log.
6. Debezium restart/failover không tạo gap; slot lag có cảnh báo.
7. Object WORM không thể bị application/operator thông thường xóa hoặc rút ngắn retention.
8. Hash/manifest phát hiện được object bị thay đổi.
9. Có thể rebuild Mongo từ archive và đối soát đủ số lượng/checksum.
10. Có biên bản restore drill, retention matrix và quy trình hủy được phê duyệt.

## 10. Ước lượng

| Hạng mục | Thời gian |
|---|---:|
| Scaffold, ingestion, Mongo | 1–2 tuần |
| Query API, tenant security, masking | 1–2 tuần |
| Canonical contract, audit lane, WORM | 2 tuần |
| Hardening, test, monitoring, rollout | 2–3 tuần |
| Tổng production-ready | 6–9 tuần |

## 11. Definition of Done

- Build/test xanh và có integration test phù hợp.
- API response/exception đúng chuẩn repo.
- Không hardcode secret; cấu hình qua environment/config properties.
- Có metrics, alert và runbook.
- Có bằng chứng tenant isolation, idempotency, replay, restore và WORM enforcement.
- Pháp chế/kế toán trưởng xác nhận retention matrix; Security xác nhận data classification và access model.
