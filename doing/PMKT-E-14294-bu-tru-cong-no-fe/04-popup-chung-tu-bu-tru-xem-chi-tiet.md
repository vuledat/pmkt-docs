# 04 — Popup Chứng từ bù trừ công nợ (Xem chi tiết · Ghi sổ · Bỏ ghi)

| | |
|---|---|
| **Mã màn** | `SCR_BTCN_ChungTu_XemChiTiet` |
| **UC nguồn** | PMKT-U-14691 (Xem chi tiết) · PMKT-U-14693 (Ghi sổ / Bỏ ghi) · PMKT-U-14692 (Xóa — mở [popup 05](05-popup-xac-nhan-xoa.md)) |
| **SCR nguồn** | `5.screens/SCR_BTCN_ChungTu_XemChiTiet.md` |
| **Matrix** | `Matrix/PMKT-E-14294_BuTruCongNo/SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md` |
| **Figma** | ⚠ **KHÔNG có frame riêng** — xem §2 |
| **Route** | `/tong-hop/bu-tru-cong-no/:id` (mới, 2026-08-21) |
| **Đường vào** | ✅ **ĐÃ NỐI ĐƯỢC (2026-08-21)** — danh sách Phiếu KTTH `/tong-hop/phieu-ke-toan-tong-hop` điều hướng sang route `/tong-hop/bu-tru-cong-no/:id` khi dòng có `loaiPhieu = 'BU_TRU_CONG_NO'` (D11 ở [00 §−1](00-ke-hoach-tong.md)) · link tham chiếu từ chứng từ công nợ đã tham gia bù trừ |
| **Component gốc** | `components/ChungTuBuTruModal.tsx` với `mode='view'` (**cùng component với [file 03](03-popup-chung-tu-bu-tru-them-moi.md)** — D8) |

---

## 1. Bố cục

Giống hệt [file 03 §1](03-popup-chung-tu-bu-tru-them-moi.md), khác đúng ba điểm:

1. Tiêu đề: `"Chứng từ bù trừ công nợ"` + **[Số chứng từ]** (`SCR_BTCN_ChungTu_XemChiTiet.md:5`) —
   nhưng Figma đặt tên popup Thêm mới là *"Phiếu kế toán tổng hợp"* ⇒ conflict **C1 / Q3**.
2. **Toàn bộ control disabled** (`:5`).
3. Footer đổi bộ nút theo **trạng thái chứng từ** (§3).

---

## 2. Đặc tả UI từ Figma

⚠ **Figma không có frame "Xem chi tiết" cho chứng từ bù trừ.** Đã rà toàn bộ 8 frame cấp 1 của
section `41322:649030`: `Danh sách` · `Bù trừ công nợ` ×2 · `Thêm mới` ×2 · `Tab chứng từ công nợ` ×2 ·
`Dropdown Menu bù trừ`. Không frame nào là màn chỉ-xem.

Hai thứ Figma **có** cho luồng xem/ghi sổ:

| Figma có gì | Node | Dùng được cho |
|---|---|---|
| **Panel xem nhanh** dưới danh sách — 4 tab (Hạch toán · Chứng từ công nợ · Đính kèm · Tham chiếu) + "Số chứng từ: DB-2023-114" + dòng Tổng + phân trang riêng | trong `41322:651294` | Chứng minh 2 tab của popup **dùng lại được** ở panel xem nhanh (xem [01 §8](01-danh-sach-chung-tu-bu-tru.md)) |
| **Menu ⋮ trên dòng**: Xem chi tiết · Ghi sổ · Bỏ ghi sổ · **Xóa** (đỏ) | `41322:650973` (150×144, mỗi mục 142×32) | Bộ hành động và **thứ tự** hiển thị |

⇒ **Đặc tả UI của màn này là suy ra từ SCR + popup Thêm mới, phải review lại khi Design bổ sung frame.**
→ **Q6** ở [file 00](00-ke-hoach-tong.md).

| Thành phần | Component `@base` | Ghi chú |
|---|---|---|
| Khung popup | `CommonModalShell` `mode='custom'` — `base/index.ts:264` | `dirty = false` (không sửa được ⇒ không cần guard đóng) |
| Toàn bộ trường | như file 03, thêm `disabled` | BR14.1 *"Xem: điền sẵn data, tất cả control disabled"* |
| Footer theo trạng thái | `CommonModalFooter` — `base/index.ts:271` | §3 |
| Popup xác nhận Bỏ ghi | `CommonConfirmModal` `tone='warning'` — `base/index.ts:276` | §5.2 |
| Badge trạng thái trên header | `CommonStatusTag` — `base/index.ts:593` | BR33 — SCR không yêu cầu, **đề xuất thêm** vì người dùng cần biết đang xem chứng từ trạng thái nào để hiểu bộ nút → đưa vào Q6 |

---

## 3. Ma trận ẩn/hiện · required · disabled

Dịch nguyên vẹn từ `SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md:35-47`. Trục cột = **Trạng thái chứng từ**.
Chiều **Loại tiền** không mở thêm cột mà đi bằng marker `(đk-LT)`: cột "…quy đổi" và "Chênh lệch tỷ giá"
chỉ hiển thị khi `Loại tiền ≠ đồng tiền hạch toán`, ngoài điều kiện → **Ẩn**.

| Vùng | Trường / Thành phần | C1 (Chưa ghi sổ) | C2 (Đã ghi sổ) |
|---|---|:--:|:--:|
| Thông tin chung | Đối tượng · Lý do · TK phải thu · TK phải trả · Ngày bù trừ · Ngày hạch toán · Ngày chứng từ · Số chứng từ · Tham chiếu · Số tiền bù trừ · Loại tiền | Disable | Disable |
| Tab Hạch toán | Diễn giải · TK Nợ · TK Có · Số tiền | Disable | Disable |
| Tab Hạch toán | Số tiền quy đổi | Disable *(đk-LT)* | Disable *(đk-LT)* |
| Tab Chứng từ công nợ · Nhóm phải thu | Loại chứng từ · Ngày chứng từ · Số chứng từ · Số hóa đơn · Hạn thanh toán · Số tiền · Số chưa thu · Số bù trừ | Disable | Disable |
| Tab Chứng từ công nợ · Nhóm phải trả | Loại chứng từ · Ngày chứng từ · Số chứng từ · Số hóa đơn · Hạn thanh toán · Số tiền · Số còn nợ · Số bù trừ | Disable | Disable |
| Tab Chứng từ công nợ | Các cột quy đổi · Chênh lệch tỷ giá | Disable *(đk-LT)* | Disable *(đk-LT)* |
| **Nút** | Điều hướng trước/sau · In · Tiện ích | Show | Show |
| **Nút** | **Ghi sổ** | **Show** | **Hide** |
| **Nút** | **Xóa** | **Show** | **Hide** |
| **Nút** | **Bỏ ghi** | **Hide** | **Show** |

**Không có nút "Sửa" ở mọi trạng thái** (`SCR_BTCN_ChungTu_XemChiTiet.md:56`) ⇒ **không render**,
không phải render rồi disable. Muốn thay đổi thì Bỏ ghi → Xóa → bù trừ lại.

⚠ **Điều hướng trước/sau · In · Tiện ích: NGOÀI phạm vi** — không có Figma, và SCR ghi rõ về nút In:
*"Nghiệp vụ in sẽ được mô tả ở tài liệu riêng (chưa xử lý trong phạm vi này)"* (`:38`). → **Q6**.

⚠ Ma trận tự hỏi ở *"Điểm cần xác nhận"* mục 3 (`SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md:66`):
**màn có nút "Đóng" riêng không?** Kế hoạch tạm dựng nút **Đóng** ở góc trái footer theo BR3
(*"Nút Đóng luôn hiển thị trong popup"*) → cần BA chốt.

**Đọc ma trận thành code** — bổ sung vào `helpers/anHien.ts`:

```ts
export interface CoNutChungTu {
  ghiSo: boolean      // trangThai = 'Chưa ghi sổ' && has('PhieuKeToan.Post')
  xoa: boolean        // trangThai = 'Chưa ghi sổ' && has('PhieuKeToan.Delete')
  boGhi: boolean      // trangThai = 'Đã ghi sổ'   && has('PhieuKeToan.Unpost')
}
```

Nền tảng là **máy trạng thái kernel**, không tự viết luật: `tinhTrangThaiHanhDong` + `LuatModule`
(`base/domainKit/chungTu/index.ts:37-49`), và chuỗi trạng thái đi qua `BanDoTrangThai`/`docTrangThai`
(`:12-31`) — engine **cấm hardcode** chuỗi trạng thái wire
(`base/domainKit/chungTu/api/ChungTuDescriptor.ts:151`).

Luật riêng của module (`LuatModule`): **cấm SỬA ở mọi trạng thái** — đây là điểm chứng từ bù trừ chặt
hơn BR12 (BR12 cho sửa khi Chưa ghi sổ).

---

## 4. Bảng cột / trường

Danh sách trường và cột **lấy nguyên** từ [file 03](03-popup-chung-tu-bu-tru-them-moi.md) — cùng một
component, cùng một bộ `fields/*` (D8). Ma trận Xem chi tiết cũng dựng danh sách trường từ chính
`SCR_BTCN_ChungTu_ThemMoi.md` (`SCR_BTCN_ChungTu_XemChiTiet_MaTranAnHien.md:3`). Ở đây chỉ ghi
**những gì khác** khi `mode='view'`:

| Nhóm | Nguồn định nghĩa | Khác gì so với `mode='create'` |
|---|---|---|
| Thông tin chung (12 trường) | [03 §4](03-popup-chung-tu-bu-tru-them-moi.md) | **Cả 5 trường vốn enable** (Lý do · Ngày hạch toán · Ngày chứng từ · Số chứng từ · Diễn giải) chuyển sang `disabled`. Không trường nào còn `required` vì không submit gì |
| Tab Hạch toán (6 cột) | [03 §5](03-popup-chung-tu-bu-tru-them-moi.md) — `fields/hachToanColumns.ts` | Cột `Diễn giải` bỏ editor, render text thuần. Số dòng (1 hay 2) **đọc từ dữ liệu BE trả**, không dựng lại bằng `helpers/hachToan.ts` |
| Tab Chứng từ công nợ (2 nhóm × 11 cột + Chênh lệch tỷ giá) | [03 §6](03-popup-chung-tu-bu-tru-them-moi.md) — `fields/chungTuCongNoColumns.ts` | Giống hệt (tab này vốn đã chỉ-xem ở `mode='create'`). Các cặp ghép **đọc từ `capGhep` của BE**, không dựng lại bằng `helpers/ghepCap.ts` |

**Điểm phải giữ đúng:** số liệu ở tab Chứng từ công nợ là **snapshot tại thời điểm bù trừ**
(`SCR_BTCN_ChungTu_ThemMoi.md:74,86` — *"Số chưa thu tại thời điểm bù trừ"*, *"Số còn nợ tại thời
điểm bù trừ"*), **không** phải số dư hiện tại. FE hiển thị nguyên giá trị BE trả, tuyệt đối không
gọi lại `lay-du-lieu` để "làm mới" các cột này.

Cột duy nhất FE vẫn tự tính ở chế độ xem: các cột `…QuyDoi` (`giá trị × tyGia`, `helpers/quyDoi.ts`) —
với điều kiện BE trả `tyGia` trong `capGhep` (xem [06 §1.5](06-hop-dong-api-va-i18n.md)).

**Thêm một trường chỉ có ở chế độ xem:** tiêu đề popup mang **Số chứng từ**
(`SCR_BTCN_ChungTu_XemChiTiet.md:5`) — khoá `chungTu.titleXem` với interpolation `{{soChungTu}}`.

---

## 5. Hành vi & sự kiện

### 5.1. Nút **Ghi sổ**

| | |
|---|---|
| Điều kiện hiện | Trạng thái = **Chưa ghi sổ** **và** quyền `PhieuKeToan.Post` (thiếu quyền → **ẩn**, BR25.2) |
| Confirm | **Không** — BR13.2: *"Thực hiện ghi sổ trực tiếp (không hiển thị popup xác nhận)"* |
| Việc làm | `POST /api/tong-hop/bu-tru-cong-no/{id}/ghi-so` (path khai qua `ChungTuEndpoints` — `ChungTuDescriptor.ts:37`) |
| BE kiểm | ① kỳ kế toán (BR17) → `MSG_..._019` · ② số dư các chứng từ tham gia → `MSG_..._018` |
| BE làm | Ghi từng dòng bút toán vào Sổ cái (**không gộp** — BR36) · cập nhật trạng thái thanh toán từng chứng từ công nợ (*Thanh toán một phần* / *Đã thanh toán*) · chuyển chứng từ sang **Đã ghi sổ** |
| Toast | ✅ `MSG_..._002` *"Ghi sổ chứng từ bù trừ công nợ thành công"* · ❌ `MSG_..._017` |
| Sau đó | Popup **giữ nguyên**, đổi trạng thái ⇒ bộ nút đổi sang C2; invalidate danh sách + chi tiết + các chứng từ công nợ tham gia |

### 5.2. Nút **Bỏ ghi**

| | |
|---|---|
| Điều kiện hiện | Trạng thái = **Đã ghi sổ** **và** quyền `PhieuKeToan.Unpost` (BR42.2) |
| Confirm | ✅ **Có** — popup `MSG_PMKT-E-14294_102`: *"Bạn có chắc chắn muốn bỏ ghi sổ chứng từ bù trừ công nợ? Hệ thống sẽ hoàn trả số dư công nợ của các chứng từ liên quan"* |
| | ⚠ Đây là **ngoại lệ có chủ đích** so với BR13.2 (*"bỏ ghi sổ trực tiếp, không hiển thị popup xác nhận"*). Epic thắng trong đúng phạm vi epic — `SCR_BTCN_ChungTu_XemChiTiet.md:40`, `UC_BTCN_GhiSoBoGhi.md:17`, và BR16 vốn cho phép cảnh báo nghiệp vụ có mã MSG riêng. **Đã ghi rõ là đang lệch BR13.2.** |
| Việc làm | Xác nhận → `POST /api/tong-hop/bu-tru-cong-no/{id}/bo-ghi-so` |
| BE kiểm | Kỳ kế toán (BR17) → `MSG_..._019` |
| BE làm | Gỡ **toàn bộ** bút toán khỏi Sổ cái · hoàn trả Số chưa thu / Số còn nợ và trạng thái thanh toán từng chứng từ công nợ về **trước khi bù trừ** · chuyển sang **Chưa ghi sổ** |
| Toast | ✅ `MSG_..._003` *"Bỏ ghi chứng từ bù trừ công nợ thành công"* · ❌ `MSG_..._017` |
| Sau đó | Bộ nút đổi sang C1 (enable Ghi sổ, Xóa) |
| Hủy xác nhận | Đóng popup xác nhận, **giữ nguyên** trạng thái chứng từ (`UC_BTCN_GhiSoBoGhi.md:64-67`) |

### 5.3. Nút **Xóa**

Mở [popup 05](05-popup-xac-nhan-xoa.md). Điều kiện hiện: Chưa ghi sổ + `PhieuKeToan.Delete`.

### 5.4. Link trong nội dung

| Link | Hành vi |
|---|---|
| **Tham chiếu** (Thông tin chung) | Mở chứng từ gốc — `UC_BTCN_XemChiTiet.md:17` |
| **Số chứng từ / Số hóa đơn** (tab Chứng từ công nợ, cả 2 nhóm) | Mở chứng từ / hóa đơn gốc |

⚠ Đích của các link này nằm ở module khác (`chungTuBanHang`, `chungTuMuaHang`, hóa đơn…). Leaf
**không** với được leaf anh em và **không** với được domain khác (`client/CLAUDE.md:108-109`)
⇒ điều hướng bằng **URL** (`navigate(path)`), không import component của module kia. Đường dẫn đích
lấy từ `paths.ts` của module đó (deep-import `constants/paths.ts` là ngoại lệ hợp lệ,
`client/CLAUDE.md:338-344`) — cần liệt kê đủ khi code, phụ thuộc BE trả `loaiChungTu` để chọn đích.
→ ghi vào [06 §1](06-hop-dong-api-va-i18n.md).

### 5.5. Ngoại lệ

| Trường hợp | Xử lý | Message |
|---|---|---|
| Không có quyền `PhieuKeToan.View.Detail` | Chặn mở chi tiết | `MSG_..._005` |
| Chứng từ không tồn tại (đã bị xóa) | Hiển thị thông báo, quay về danh sách | `MSG_..._021` |
| Lỗi hệ thống khi Ghi sổ / Bỏ ghi | Giữ nguyên trạng thái chứng từ | `MSG_..._017` |

---

## 6. Validation phía FE

**Không có** — màn chỉ xem, không nhập liệu. Mọi kiểm tra (kỳ kế toán BR17, số dư, trạng thái
`MSG_COMMON_001`) do **BE** thực hiện; FE hiển thị thông báo BE trả về qua `describeApiError`
(`@platform`), map 7 mã lỗi kernel bằng `moTaLoiChungTu` (`base/domainKit/chungTu/index.ts:52-54`).

FE **chỉ** chặn ở tầng hiển thị nút: không hiện nút thì không gọi được hành động sai trạng thái (BR13.2).

---

## 7. Luồng xử lý

1. Danh sách Phiếu KTTH → Xem chi tiết / double-click dòng có `LoaiPhieu = Bù trừ công nợ`
   → mở `ChungTuBuTruModal mode='view'` với `id`.
2. `queries.useChiTiet(id)` → `GET /api/tong-hop/bu-tru-cong-no/{id}`, Zod parse.
   - Đang tải: `busy` của `CommonModalShell` (khoá popup + spinner).
   - Không tìm thấy: toast `MSG_..._021`, đóng popup, về danh sách.
3. Render Thông tin chung + 2 tab, **toàn bộ disabled**.
4. `helpers/anHien.ts` + máy trạng thái kernel tính bộ nút từ `{ trangThai, quyền }`.
5. Bấm nút → §5 → `useBuTruActions` gọi API, toast, invalidate.
6. Sau Ghi sổ / Bỏ ghi: **không đóng popup**, chỉ nạp lại chi tiết ⇒ bộ nút tự đổi.
   Sau Xóa: đóng popup, về danh sách và làm mới (`SCR_BTCN_PopupXacNhanXoa.md:34`).

---

## 8. Phân bổ file

| Việc | File |
|---|---|
| Popup ở `mode='view'` (dùng lại nguyên component của file 03) | `components/ChungTuBuTruModal.tsx` |
| Footer động theo trạng thái + quyền | `components/ChungTuBuTruModal.tsx` (ráp) + `helpers/anHien.ts` (tính cờ) |
| Popup xác nhận Bỏ ghi | `components/XacNhanBuTruModal.tsx` |
| Ghi sổ · Bỏ ghi · Xóa (mutation + confirm + toast + invalidate) | `hooks/useBuTruActions.ts` |
| `GET /{id}` + Zod | `api/buTruCongNoApi.ts` · `api/model.ts` · `api/queries.ts` |
| Đường dẫn ghi sổ / bỏ ghi / xóa | `constants/constants.ts` (hoặc `api/`, theo `ChungTuEndpoints`) |
| Chữ: tiêu đề, nhãn 5 nút, `msg.102`, `msg.003`, `msg.002` | `i18n/vi.ts` · `i18n/en.ts` |

---

## 9. Kiểm thử (`test/`)

### `anHien.test.ts` — bộ nút theo trạng thái × quyền

| # | Trạng thái | Quyền | Kỳ vọng |
|---|---|---|---|
| B1 | Chưa ghi sổ | đủ 3 quyền | Hiện **Ghi sổ · Xóa**; **ẩn** Bỏ ghi; **không có** nút Sửa |
| B2 | Đã ghi sổ | đủ 3 quyền | Hiện **Bỏ ghi**; **ẩn** Ghi sổ, Xóa; **không có** nút Sửa |
| B3 | Chưa ghi sổ | thiếu `PhieuKeToan.Delete` | Hiện Ghi sổ; **ẩn** Xóa (ẩn, **không** disable — BR25.2) |
| B4 | Đã ghi sổ | thiếu `PhieuKeToan.Unpost` | **Ẩn** Bỏ ghi ⇒ footer chỉ còn nút Đóng |
| B5 | Mọi trạng thái | mọi quyền | Không bao giờ render nút "Sửa" |

### `chungTuBuTru.view.render.test.tsx`

| # | Input | Kỳ vọng |
|---|---|---|
| V1 | `mode='view'` | **Mọi** input/select/date đều `disabled`; kể cả 5 trường vốn enable ở `mode='create'` |
| V2 | `mode='view'`, `coQuyDoi=false` | Không có cột quy đổi lẫn cột "Chênh lệch tỷ giá" trong DOM |
| V3 | Bấm **Bỏ ghi** | Hiện popup xác nhận với **nguyên văn** `MSG_..._102`; chưa gọi API |
| V4 | Popup xác nhận → bấm Đóng | Không gọi API; trạng thái chứng từ giữ nguyên |
| V5 | Bấm **Ghi sổ** | Gọi API **ngay**, **không** hiện popup xác nhận (BR13.2) |
| V6 | API Ghi sổ trả lỗi kỳ đã khóa | Toast hiển thị **nguyên văn** message BE trả (`MSG_..._019` có `{ngày khóa sổ}`), popup không đóng |

---

## 10. BR đã áp dụng

BR3 (popup: Đóng/×/Esc, nút xác nhận phải – hủy trái) · BR4 · BR09 (link tham chiếu) ·
BR12 (vòng đời trạng thái + quy tắc bất biến) · BR13.2 (bộ nút theo chế độ Xem; Ghi sổ không hỏi xác nhận) ·
BR14.1 (chế độ Xem — toàn bộ disabled) · BR16 (cảnh báo nghiệp vụ có mã MSG riêng cho Bỏ ghi) ·
BR17 (kỳ kế toán — BE kiểm, FE hiển thị) · BR18.4 (ẩn cột quy đổi khi = ĐTHT) ·
BR25 (ẩn nút khi thiếu quyền) · BR26 (toast) · BR31 (dòng Tổng) · BR33 (badge trạng thái) ·
BR36 (không gộp bút toán — ràng buộc BE) · BR41 (tham chiếu chéo — **lưu ý**: quan hệ bù trừ là
*ràng buộc nghiệp vụ*, **không** thuộc BR41; BR41 tự loại trừ "đối trừ/bù trừ công nợ" khỏi phạm vi,
`business_rules.md:922`) · BR42 (Bỏ ghi chỉ với Đã ghi sổ; ẩn nút với Chưa ghi sổ).

**Lệch BR có chủ đích (đã ghi rõ):**
**BR13.2** nói *"Bỏ ghi sổ: thực hiện trực tiếp, không hiển thị popup xác nhận"*, nhưng epic bắt phải
có popup `MSG_..._102` (`SCR_BTCN_ChungTu_XemChiTiet.md:40`; `UC_BTCN_GhiSoBoGhi.md:17`).
→ **Theo epic** trong đúng phạm vi epic này, vì bỏ ghi bù trừ có tác dụng phụ nặng (hoàn trả số dư
công nợ nhiều chứng từ) và BR16 cho phép cảnh báo nghiệp vụ có mã MSG riêng.

**Chưa xử lý:**
- **Điều hướng trước/sau · In · Tiện ích** — không có Figma, không có đặc tả (SCR tự ghi nút In để
  tài liệu riêng). → **Q6**.
- **BR34** (Chỉnh sửa từ màn Xem) — **không áp dụng**: chứng từ bù trừ không cho sửa ở mọi trạng thái.
- **MSG_PMKT-E-14294_101** (chặn Bỏ ghi sổ chứng từ công nợ đang tham gia bù trừ) — thuộc màn chứng từ
  bán hàng / mua hàng, ngoài module này. → **Q8**.
