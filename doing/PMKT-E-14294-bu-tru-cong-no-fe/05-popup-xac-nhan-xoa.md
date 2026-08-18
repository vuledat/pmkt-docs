# 05 — Popup xác nhận Xóa chứng từ bù trừ công nợ

| | |
|---|---|
| **Mã màn** | `SCR_BTCN_PopupXacNhanXoa` |
| **UC nguồn** | PMKT-U-14692 — `UC_BTCN_Xoa.md` |
| **SCR nguồn** | `5.screens/SCR_BTCN_PopupXacNhanXoa.md` |
| **Matrix** | **SKIP** — `_scope.md:11` (popup xác nhận, không có input động) |
| **Figma** | ❌ **"Không có figma"** — BA ghi rõ tại `SCR_BTCN_PopupXacNhanXoa.md:7` |
| **Đường vào** | Nút **Xóa** ở [popup 04](04-popup-chung-tu-bu-tru-xem-chi-tiet.md) · mục **Xóa** trên menu ⋮ của danh sách |
| **Component gốc** | `components/XacNhanBuTruModal.tsx` — bọc `CommonConfirmModal` |

---

## 1. Bố cục

Popup xác nhận **chuẩn hệ thống** theo BR3, không có bố cục riêng:

```
┌──────────────────────────────────────────────────┐
│ ⚠  Xác nhận xóa                            [×]   │
├──────────────────────────────────────────────────┤
│ Bạn có chắc chắn muốn xóa chứng từ bù trừ công   │
│ nợ 'BTCN-20895048'? Thao tác này không thể       │
│ hoàn tác                                          │
├──────────────────────────────────────────────────┤
│ [Đóng]                            [Xác nhận]     │
└──────────────────────────────────────────────────┘
```

---

## 2. Đặc tả UI

**Không có Figma** ⇒ toàn bộ trình bày lấy theo **component chuẩn** `CommonConfirmModal`
(`base/index.ts:276`) với `tone='danger'` — cùng cách màn Chứng từ bán hàng đang dùng cho popup xóa
(`features/banHang/chungTuBanHang/components/ChungTuBanHangTab.tsx:339-348`), nên hình thức đã nhất
quán với phần còn lại của hệ thống mà không cần Design bổ sung.

| Thành phần (SCR) | Ánh xạ vào `CommonConfirmModal` | Nguồn |
|---|---|---|
| Tiêu đề "Xác nhận xóa" **kèm icon cảnh báo** | `title` + `tone='danger'` (component tự vẽ icon) | `SCR_BTCN_PopupXacNhanXoa.md:20`; BR3 |
| Nội dung | `message` = `MSG_PMKT-E-14294_103` | `:21` |
| Nút **Đóng** — bên trái | `closeLabel` | `:22`; BR3 (*"nút hủy/đóng luôn ở bên trái"*) |
| Nút **Xác nhận** — bên phải, primary | nút confirm mặc định của component | `:23` |
| Đang gọi API | `loading` | — |

Không viết component mới. *(Đã kiểm `@base`: `CommonConfirmModal` đủ dùng, không thiếu prop nào.)*

---

## 3. Ma trận ẩn/hiện · required · disabled

**Không áp dụng** — `_scope.md:11`: *"Popup xác nhận Xóa — chỉ có tiêu đề + cảnh báo tĩnh + 2 nút
Đóng/Xác nhận (không có input động)"*.

Điều kiện **mở được** popup này (chính là điều kiện hiện nút Xóa, xem [04 §3](04-popup-chung-tu-bu-tru-xem-chi-tiet.md)):

| Điều kiện | Nguồn |
|---|---|
| Chứng từ ở trạng thái **Chưa ghi sổ** (mới Lưu hoặc đã Bỏ ghi) | `SCR_BTCN_PopupXacNhanXoa.md:12`; BR12; BR13.1/13.2 |
| Người dùng có quyền `PhieuKeToan.Delete` | `:11`; BR25 — thiếu quyền → **ẩn nút**, không disable |

---

## 4. Bảng trường

Không có trường nhập liệu. Một tham số hiển thị duy nhất:

| Tham số | Nguồn | Dùng ở |
|---|---|---|
| `soChungTu` | `PhieuKeToanTongHop.SoChungTu` của chứng từ đang xóa | Nội suy vào `MSG_..._103` |

---

## 5. Hành vi & sự kiện

| Thao tác | Việc làm | Toast | Invalidate |
|---|---|---|---|
| **Xác nhận** | `DELETE /api/tong-hop/bu-tru-cong-no/{id}` (mang theo token khoá lạc quan `updatedAt` — BR12 *"Chống sửa đổi đồng thời"*) | ✅ `MSG_..._004` *"Xóa chứng từ bù trừ công nợ thành công"* | Danh sách Phiếu KTTH + các chứng từ công nợ liên quan |
| | Thành công → **đóng popup xác nhận và đóng cả popup chi tiết**, quay về danh sách và **làm mới** (`SCR_BTCN_PopupXacNhanXoa.md:34`) | | |
| **Đóng** / `×` / `Esc` / click ra ngoài | Hủy thao tác, đóng popup xác nhận, **giữ nguyên** màn hình hiện tại (`:22`; BR3) | — | — |

### 5.1. BE làm gì khi xóa (BR01 của SCR)

1. Kiểm chứng từ tồn tại — không tồn tại → `MSG_..._021`.
2. Kiểm trạng thái **Chưa ghi sổ** (chứng từ Đã ghi sổ không hiện nút Xóa; gọi ép qua API →
   `MSG_COMMON_001`, BR16.1).
3. **Xóa mềm** (BR29.1) chứng từ + toàn bộ chi tiết: `ENT_PhieuKeToanTongHop` ·
   `ENT_BuTruCongNo` · `ENT_ChiTietPhieuKTTH_HachToan` · `ENT_ChiTietBuTruCongNo_ChungTu`
   (`UC_BTCN_Xoa.md:40`).
4. **Gỡ tham chiếu đối ứng** (`ENT_ChungTuLienQuan`) trên các chứng từ công nợ liên quan.
5. Số dư công nợ **không đổi** — chứng từ chỉ xóa được khi Chưa ghi sổ, nên công nợ chưa bị ảnh hưởng
   (hoặc đã được hoàn trả khi Bỏ ghi) — `SCR_BTCN_PopupXacNhanXoa.md:37`.

⇒ Sau khi xóa, các chứng từ công nợ **xuất hiện trở lại** khi Lấy dữ liệu ở [popup 02](02-popup-bu-tru-cong-no.md)
(`UC_BTCN_Xoa.md:72`). FE phải invalidate cả query `lay-du-lieu` nếu popup 02 còn mở.

### 5.2. Ngoại lệ

| Trường hợp | Xử lý | Message |
|---|---|---|
| Không có quyền `PhieuKeToan.Delete` | Ẩn nút Xóa; gọi ép qua API → chặn | `MSG_..._005` |
| Chứng từ ở trạng thái Đã ghi sổ | Không hiển thị nút Xóa | — |
| Chứng từ không tồn tại (người khác đã xóa) | Đóng popup, quay về danh sách | `MSG_..._021` |
| Lỗi hệ thống khi xóa | **Giữ nguyên** chứng từ, popup xác nhận đóng lại | `MSG_..._020` *"Lỗi khi xóa chứng từ bù trừ công nợ"* |

---

## 6. Validation phía FE

**Không có.** Toàn bộ điều kiện (tồn tại · trạng thái · quyền · khoá lạc quan) do **BE** kiểm;
FE chỉ (a) không hiện nút khi không đủ điều kiện, (b) hiển thị lỗi BE trả về.

---

## 7. Luồng xử lý

1. Bấm **Xóa** (popup 04 hoặc menu ⋮ danh sách) → `setXoaTarget(row)`.
2. Render `<XacNhanBuTruModal open tone="danger" message={t('buTruCongNo:msg.xacNhanXoa', { soChungTu })} />`.
3. Bấm **Xác nhận** → `useBuTruActions().xoa.mutateAsync({ id, ctx: { updatedAt } })`,
   `loading` bật trên nút xác nhận.
4. Thành công → toast `MSG_..._004` → invalidate → đóng popup xác nhận **và** popup chi tiết →
   về danh sách, làm mới. **Giữ nguyên trang hiện tại** của danh sách (BR29.4).
5. Thất bại → toast lỗi (`MSG_..._020` hoặc message BE trả) → `setXoaTarget(null)`, giữ nguyên dữ liệu.

---

## 8. Phân bổ file

| Việc | File |
|---|---|
| Popup xác nhận (bọc `CommonConfirmModal`, dùng chung cho Xóa và Bỏ ghi) | `components/XacNhanBuTruModal.tsx` |
| Mutation xóa + toast + invalidate | `hooks/useBuTruActions.ts` |
| `DELETE /{id}` + Zod parse response | `api/buTruCongNoApi.ts` · `api/queries.ts` |
| Chữ: `xoa.title`, `xoa.dong`, `xoa.xacNhan`, `msg.xacNhanXoa`, `msg.xoaThanhCong`, `msg.loiXoa` | `i18n/vi.ts` · `i18n/en.ts` |

**Không** sinh file `fields/`, `helpers/`, `constants/` riêng cho popup này — nó không có cột, không
có công thức, không có hằng số riêng.

---

## 9. Kiểm thử (`test/`)

`xacNhanXoa.render.test.tsx`:

| # | Input | Kỳ vọng |
|---|---|---|
| X1 | Mở popup với `soChungTu = 'BTCN-20895048'` | Nội dung hiển thị **nguyên văn** `MSG_..._103` có nội suy đúng số chứng từ; **không** cộng chuỗi |
| X2 | Bấm **Đóng** | Không gọi API; popup đóng; popup chi tiết **vẫn mở** |
| X3 | Bấm **Xác nhận** | Gọi `DELETE` đúng 1 lần với `id` và `updatedAt` |
| X4 | API trả 200 | Toast `MSG_..._004`; đóng cả 2 popup; `invalidateQueries` được gọi cho danh sách |
| X5 | API trả lỗi | Toast lỗi; popup chi tiết **vẫn mở**; chứng từ không bị gỡ khỏi state |
| X6 | Đang gọi API | Nút Xác nhận ở trạng thái `loading`, bấm lần hai không tạo request thứ hai |
| X7 | Nhấn `Esc` | Tương đương bấm Đóng (BR3) |

---

## 10. BR đã áp dụng

**BR3** — popup xác nhận xóa: tiêu đề *"Xác nhận xóa"* + icon cảnh báo, nút hủy trái / xác nhận phải,
`Esc` = Đóng, click ra ngoài = hủy, focus không thoát khỏi popup.
Cấu trúc câu của BR3 (*"Bạn có chắc chắn muốn xóa **{Loại đối tượng}** **'{Tên/Số}'**? Thao tác này
không thể hoàn tác."*) khớp **nguyên văn** `MSG_PMKT-E-14294_103` ✅.

**BR12** — chỉ xóa được chứng từ Chưa ghi sổ; chống sửa đổi đồng thời (mang `updatedAt` khi xóa).
**BR13.1 / BR13.2** — điều kiện hiện nút Xóa theo trạng thái.
**BR16.1** — `MSG_COMMON_001` khi gọi ép qua API với chứng từ sai trạng thái.
**BR25.2** — thiếu quyền → **ẩn** nút Xóa (không disable).
**BR26** — toast thành công (xanh lá) / lỗi (đỏ).
**BR29.1** — xóa mềm (ràng buộc **BE**).
**BR29.2** — xóa lan mềm sang các bảng chi tiết (ràng buộc **BE**).
**BR29.4** — sau khi xóa, danh sách **giữ nguyên trang hiện tại**.

**Chưa xử lý:**
- **BR45** (xóa hàng loạt) — thuộc màn danh sách Phiếu KTTH, ngoài phạm vi (D3).
- **BR41** — **không áp dụng**: quan hệ bù trừ là *ràng buộc nghiệp vụ*, BR41 tự loại trừ
  *"đối trừ/bù trừ công nợ"* khỏi phạm vi tham chiếu mềm (`business_rules.md:922`). Việc gỡ
  `ENT_ChungTuLienQuan` khi xóa là quy tắc riêng của epic, do BE làm.
