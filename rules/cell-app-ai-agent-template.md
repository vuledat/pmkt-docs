# `cell-app` — Prompt / Template chuẩn cho AI Agent

> **Mục tiêu:** dùng AI Agent để phát triển PYC trong `cell-app` nhưng vẫn **đi đúng kiến trúc thư mục**, **tái sử dụng code base hiện có**, và **không sửa code base gốc ngoài phạm vi cho phép**.
>
> **Phạm vi tài liệu này:** quy trình và template giao việc cho AI. Không thay thế `../../CLAUDE.md`, `../../cell-app/CLAUDE.md` hay `conventions.md`; đây là lớp ràng buộc bổ sung để AI làm đúng trong `cell-app`.
>
> **Tình trạng:** dùng được ngay cho các PYC kiểu `chung_tu_*`, đặc biệt các module greenfield như `chung_tu_mua_hang/`.

---

## 1. Nguyên tắc vận hành

AI Agent chỉ được coi là **người triển khai trong khung kiến trúc đã có**, không phải người tự thiết kế lại kiến trúc của `cell-app`.

Ba nguyên tắc cứng:

1. **Tuân thủ kiến trúc thư mục hiện hành**
   - mẫu đúng để tham khảo: `accounting_core/`, `chung_tu_ban_hang/`, `platform_iam/`, `integration_ops/`;
   - module mới đi theo kiểu modulith có `internal/`, và nếu có hợp đồng công khai thì dùng `package-info.java` / `@NamedInterface` đúng chỗ.

2. **Tái sử dụng code base trước khi viết mới**
   - ưu tiên kế thừa / composition từ base class, DTO base, entity base, service base;
   - không copy-paste pattern từ module khác rồi đổi tên thủ công.

3. **Không sửa code base dùng chung nếu chưa chứng minh là bắt buộc**
   - mặc định `core/` và `accounting_core/` là vùng chỉ-đọc để tham chiếu contract;
   - chỉ được đề xuất sửa khi đã chứng minh không giải được bằng extension point trong module nghiệp vụ.

---

## 2. Nguồn quy ước phải bám

Trước khi AI sinh kế hoạch hoặc code, phải đọc và tuân thủ theo đúng thứ tự ưu tiên sau:

1. `../../CLAUDE.md`
2. `../../cell-app/CLAUDE.md`
3. `conventions.md`
4. tài liệu kế hoạch/BA của đúng PYC đang làm
5. module mẫu gần nhất về mặt kiến trúc, thường là `cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/**`

> Nếu có mâu thuẫn, ưu tiên theo thứ tự trên và **báo rõ mâu thuẫn** thay vì tự chọn im lặng.

---

## 3. Vùng tham khảo được phép và vùng cấm

### 3.1 Được phép tham khảo

- `cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/**`
- `cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/**`
- `cell-app/src/main/java/vn/dopai/pmkt/cell/platform_iam/**`
- `cell-app/src/main/java/vn/dopai/pmkt/cell/integration_ops/**`
- `cell-app/src/main/java/vn/dopai/pmkt/cell/core/**`
- `docs/**`
- `pmkt-docs/ba/**`

### 3.2 Cấm đọc / cấm dùng làm mẫu

`cell-app/src/main/java/vn/dopai/pmkt/cell/master_data/**`

Lý do đã được chốt trong `../../CLAUDE.md` và `../../cell-app/CLAUDE.md`:

- đây là kiến trúc cũ, phẳng, không còn là mẫu chuẩn;
- đọc vào sẽ kéo AI sang pattern sai;
- kết quả grep rơi vào đây phải bị loại khỏi quá trình suy luận kiến trúc hiện hành.

### 3.3 Ngoại lệ rất hẹp

Chỉ được chạm `master_data/**` khi:

1. user yêu cầu sửa trực tiếp vùng đó; hoặc
2. module khác lỗi biên dịch vì đang phụ thuộc API công khai của nó.

Khi đó AI phải:

- báo rõ đang chạm vùng đóng băng;
- chỉ đọc đúng chữ ký/API cần dùng;
- tuyệt đối không mang kiến trúc ở đó sang code mới.

---

## 4. Kiến trúc mặc định cho PYC trong `cell-app`

Với một PYC greenfield cho chứng từ, AI mặc định phải nghĩ theo cấu trúc sau:

```text
cell-app/src/main/java/vn/dopai/pmkt/cell/<domain>/
├── package-info.java
└── internal/
    ├── controller/
    ├── dto/
    ├── entity/
    ├── model/
    ├── repository/
    └── service/
```

Nếu use case chỉ là tra cứu/listing, có thể chưa cần đủ mọi tầng, nhưng AI phải giải thích rõ vì sao tầng nào chưa xuất hiện.

### 4.1 Quy tắc phân tầng bắt buộc

```text
Controller → Service → Repository → Entity
```

- Controller không gọi Repository trực tiếp.
- Controller không chứa business logic.
- Service chứa nghiệp vụ và transaction boundary.
- Repository là nơi duy nhất chạm dữ liệu.
- Entity không trả thẳng ra API; luôn map sang DTO.

### 4.2 Quy tắc modulith

- phần `internal/` là implementation detail;
- chỉ package public contract mới được expose ra ngoài;
- nếu module ngoài cần dùng contract dùng chung của chứng từ thì ưu tiên contract ở `accounting_core/chung_tu/**` thay vì import chéo `internal/**` của module khác.

---

## 5. Thứ tự ưu tiên tái sử dụng code base

Khi AI định sinh code mới, phải xét theo đúng thứ tự sau:

1. **Dùng base class / contract sẵn có**
2. **Override / implement extension point sẵn có**
3. **Thêm class mới trong module nghiệp vụ**
4. **Thêm adapter / mapper / repository riêng trong module nghiệp vụ**
5. **Chỉ sau cùng mới đề xuất sửa `accounting_core/` hoặc `core/`**

### 5.1 Các điểm tái sử dụng ưu tiên cao cho nhóm chứng từ

- `accounting_core/chung_tu/controller/BaseChungTuController.java`
- `accounting_core/chung_tu/service/AbstractChungTuCrudService.java`
- `accounting_core/chung_tu/service/HangLoatChungTuService.java`
- `accounting_core/chung_tu/dto/BaseChungTuRequest.java`
- `accounting_core/chung_tu/dto/BaseChiTietChungTuRequest.java`
- `core/entity/BaseChungTuEntity.java`
- `core/entity/BaseChiTietChungTuEntity.java`
- `core/repository/BaseRepository.java`

### 5.2 Mẫu tham chiếu gần nhất

Khi chưa chắc tổ chức module thế nào, AI phải so với:

- `chung_tu_ban_hang/internal/controller/ChungTuBanHangController.java`
- `chung_tu_ban_hang/internal/service/ChungTuBanHangCrudService.java`
- `chung_tu_ban_hang/internal/service/business/**`

> AI được phép **tham chiếu pattern**, không được sao chép mù quáng cả hành vi nếu PYC hiện tại chưa cần cùng phạm vi.

---

## 6. Chính sách phạm vi sửa (`change policy`)

Mọi PYC giao cho AI phải khai báo rõ vùng được sửa.

### 6.1 Mức thay đổi

#### Mức A — Feature-only

- chỉ tạo/sửa trong module nghiệp vụ đích, ví dụ `chung_tu_mua_hang/**`;
- không sửa `core/`, `accounting_core/`, `master_data/`.

Đây là mức mặc định và là mức an toàn nhất để AI tự triển khai.

#### Mức B — Feature + integration

- có thể sửa thêm wiring, package exposure, migration, constant hoặc quyền liên quan đến module mới;
- vẫn **không** sửa base class dùng chung nếu chưa có phê duyệt rõ.

#### Mức C — Base / platform change

- đụng `core/`, `accounting_core/`, base DTO/entity/service, shared contract.

Ở mức này AI **không được nhảy thẳng vào code**. Trước hết phải dừng ở bước:

1. impact analysis,
2. lý do không dùng extension point,
3. danh sách module bị ảnh hưởng,
4. đề xuất thay đổi backward-compatible hay breaking.

### 6.2 Vùng mặc định read-only

Nếu ticket không ghi khác, coi các vùng sau là chỉ-đọc:

- `cell-app/src/main/java/vn/dopai/pmkt/cell/core/**`
- `cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/**`
- `cell-app/src/main/java/vn/dopai/pmkt/cell/master_data/**`

---

## 7. Quy trình làm việc bắt buộc với AI Agent

AI phải làm theo **2 pha**, không được bỏ qua pha plan.

### 7.1 Pha 1 — Architecture plan

Trước khi sinh code, AI phải trả lời đủ các mục sau:

1. PYC này thuộc module/package nào?
2. Domain concept là gì?
3. File nào sẽ tạo mới?
4. File cũ nào buộc phải sửa?
5. Những base class / contract nào sẽ reuse?
6. Mức thay đổi là A / B / C?
7. Có chạm `core/` hoặc `accounting_core/` không? Nếu có, vì sao không tránh được?
8. Có migration / quyền / messageId / Postman / test nào phải đi kèm không?

Nếu thiếu một trong các mục trên thì plan chưa hợp lệ.

### 7.2 Pha 2 — Implementation

Chỉ sau khi plan được chấp nhận, AI mới được code.

Nguyên tắc khi code:

- ưu tiên thêm file mới trong module nghiệp vụ;
- chỉ sửa file cũ khi cần nối vào hạ tầng/chuỗi tích hợp;
- không mở rộng diff sang code cũ ngoài phạm vi PYC;
- không tự ý refactor hàng loạt nhân tiện.

---

## 8. Checklist tự kiểm của AI trước khi code

AI phải tự trả lời “Có/Không” cho toàn bộ checklist này:

### 8.1 Kiến trúc

- [ ] Đã xác định đúng module đích chưa?
- [ ] Đã dùng đúng pattern `internal/` chưa?
- [ ] Có vô tình import `internal/**` của module khác không?
- [ ] Có tạo đường ghi ngoài quy trình nghiệp vụ chuẩn không?

### 8.2 Tái sử dụng

- [ ] Đã kiểm tra base/controller/service/entity/dto sẵn có chưa?
- [ ] Có chỗ nào đang copy-paste mà lẽ ra có thể kế thừa không?
- [ ] Có dùng lại hợp đồng `accounting_core/chung_tu` khi phù hợp không?

### 8.3 Phạm vi sửa

- [ ] Có chạm `core/` không?
- [ ] Có chạm `accounting_core/` không?
- [ ] Có chạm `master_data/` không?
- [ ] Nếu có chạm vùng dùng chung, ticket đã cho phép chưa?

### 8.4 Dữ liệu và API

- [ ] Response có theo `ApiResponse<T>` / `PageResponse` hiện hành không?
- [ ] Có giữ phân tầng `Controller → Service → Repository → Entity` không?
- [ ] Có hardcode text hiển thị hoặc magic value không?

---

## 9. Template giao việc cho AI Agent

Đây là mẫu nên dùng cho mọi PYC mới trong `cell-app`.

```md
Nhiệm vụ: phát triển PYC <PYC_CODE> cho `cell-app`.

## Mục tiêu
- Implement đúng phạm vi PYC.
- Tuân thủ kiến trúc hiện hành của `cell-app`.
- Reuse tối đa code base sẵn có.
- Không sửa code base dùng chung ngoài phạm vi cho phép.

## Domain context
- domain: <ten_domain>
- module_root: cell-app/src/main/java/vn/dopai/pmkt/cell/<ten_domain>
- use_case_docs:
  - <doc_1>
  - <doc_2>

## Reference modules / contracts bắt buộc tham chiếu
- cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_ban_hang/**
- cell-app/src/main/java/vn/dopai/pmkt/cell/accounting_core/chung_tu/**
- cell-app/src/main/java/vn/dopai/pmkt/cell/core/entity/BaseChungTuEntity.java
- cell-app/src/main/java/vn/dopai/pmkt/cell/core/entity/BaseChiTietChungTuEntity.java
- <them file khac neu can>

## Forbidden paths
- cell-app/src/main/java/vn/dopai/pmkt/cell/master_data/**

## Change policy
- allow_new_files: true
- allow_edit_feature_module: true
- allow_edit_common_constants: <true|false>
- allow_edit_migration: <true|false>
- allow_edit_accounting_core: false
- allow_edit_core: false
- allow_edit_master_data: false

## Output phase 1 — plan bắt buộc
1. Xác định module/package đích.
2. Liệt kê class base/contract sẽ reuse.
3. Liệt kê file mới.
4. Liệt kê file cũ cần sửa.
5. Phân loại mức thay đổi A/B/C.
6. Nêu rõ vì sao mọi thay đổi ngoài module đích là không tránh được.

## Output phase 2 — implementation
- Chỉ code sau khi plan đã được chấp nhận.
- Ưu tiên thêm file trong `<ten_domain>/internal/**`.
- Không refactor code cũ ngoài phạm vi ticket.
- Nếu phát hiện phải sửa `accounting_core/` hoặc `core/`, dừng lại và báo impact analysis trước.
```

---

## 10. Template YAML ngắn cho PYC

Nếu team thích metadata ngắn gọn hơn, dùng mẫu này:

```yaml
pyc_code: PMKT-XXXX
module: chung_tu_mua_hang
module_root: cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_mua_hang
scope: feature-only
reference_modules:
  - chung_tu_ban_hang
public_contracts:
  - accounting_core/chung_tu/controller/BaseChungTuController.java
  - accounting_core/chung_tu/service/AbstractChungTuCrudService.java
  - accounting_core/chung_tu/dto/BaseChungTuRequest.java
  - accounting_core/chung_tu/dto/BaseChiTietChungTuRequest.java
  - core/entity/BaseChungTuEntity.java
  - core/entity/BaseChiTietChungTuEntity.java
forbidden_paths:
  - master_data/**
change_policy:
  allow_new_files: true
  allow_edit_feature_module: true
  allow_edit_accounting_core: false
  allow_edit_core: false
  allow_edit_master_data: false
deliverables:
  - source_code
  - migration_sql
  - unit_tests
  - postman_collection
```

---

## 11. Cổng kiểm cuối trước khi chấp nhận kết quả từ AI

### 11.1 Kiểm diff

Reviewer hoặc chính AI phải trả lời:

- Diff có tạo đúng module mới không?
- Diff có đụng `master_data/**` không?
- Diff có sửa `core/**` / `accounting_core/**` trái policy không?
- Diff có xuất hiện code copy từ module cũ thay vì reuse base không?

### 11.2 Kiểm kiến trúc

- Controller có gọi Repository trực tiếp không?
- Entity có bị trả thẳng ra API không?
- Có endpoint ghi nào bị mở nhầm do kế thừa sai base controller không?
- Có import xuyên ranh giới modulith không?

### 11.3 Kiểm build

Nếu có sửa Java trong `cell-app`, bắt buộc chạy lệnh phù hợp với project con:

```bash
cd cell-app && ./gradlew build
```

Nếu môi trường không chạy hết integration test, phải báo trung thực lane nào xanh, lane nào bị chặn bởi môi trường.

---

## 12. Áp dụng nhanh cho `chung_tu_mua_hang`

Ví dụ nếu giao AI làm module `chung_tu_mua_hang`, mặc định nên chốt như sau:

- **module đích:** `cell-app/src/main/java/vn/dopai/pmkt/cell/chung_tu_mua_hang/`
- **module tham chiếu:** `chung_tu_ban_hang/`, `accounting_core/chung_tu/`
- **vùng cấm:** `master_data/**`
- **phạm vi sửa mặc định:**
  - được tạo file mới trong `chung_tu_mua_hang/**`
  - được thêm migration mới của riêng PYC
  - có thể sửa hằng quyền / messageId nếu ticket ghi rõ
  - không sửa `core/**` và `accounting_core/**`

---

## 13. Tiêu chí thành công

Template này được coi là phát huy tác dụng khi AI:

1. tạo code mới đúng module nghiệp vụ;
2. bám pattern `internal/` và contract modulith hiện có;
3. dùng base class / base DTO / base entity thay vì phát minh tầng mới;
4. không đụng `master_data/**`;
5. không sửa `core/` hay `accounting_core/` nếu ticket không cho phép;
6. luôn đi qua bước plan trước khi code;
7. báo rõ impact nếu phát hiện thiếu extension point.

---

## 14. Khuyến nghị vận hành cho team

Nếu muốn áp dụng ngay với hiệu quả cao, nên làm đồng thời 3 việc:

1. dùng chính tài liệu này làm **prompt nền** cho AI Agent khi làm `cell-app`;
2. mọi ticket/PYC đều phải có **`reference_modules` + `change_policy`**;
3. review AI output theo đúng 3 cổng: **kiến trúc → diff → build**.

Khi đó AI sẽ bị buộc phải đi theo code base hiện có, thay vì ngẫu hứng mở rộng hoặc sửa nền tảng dùng chung.