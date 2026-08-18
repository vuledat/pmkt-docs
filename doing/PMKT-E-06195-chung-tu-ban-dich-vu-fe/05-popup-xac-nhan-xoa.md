# 05 — Popup Xác nhận xóa (đơn + hàng loạt)

| | |
|---|---|
| **Phiên bản** | **v2 — 2026-08-15** (đồng bộ BA commit `1a928c53b`) |
| **SCR nguồn** | `5.screens/SCR_CTbanDichVu_Xoa.md` (+ `PMKT-E-06194/.../SCR_CTBH_PopupXacNhanXoa.md`) |
| **UC nguồn** | `UC_CTbanDichVu_Xoa` |
| **Ma trận** | Không có — `_scope.md` xếp **SKIP** (popup xác nhận, chỉ có nút + text tĩnh) |
| **Figma** | **Không có** — SCR ghi mục Nguyên mẫu là `[Đang bổ sung]` |
| **Quyền** | `BanDichVu.Delete` |

---

## 1. Bố cục

**A. Popup xác nhận xóa** — `CommonConfirmModal` (`src/base/index.ts:269`), biến thể destructive:

```
┌──────────────────────────────────────────────┐
│ ⚠ Xác nhận xóa chứng từ bán dịch vụ      [×] │
├──────────────────────────────────────────────┤
│ Bạn có chắc chắn muốn xóa chứng từ bán       │
│ dịch vụ này không?                           │
├──────────────────────────────────────────────┤
│ [Hủy]                          [Xác nhận]    │
└──────────────────────────────────────────────┘
```

**B. Popup Kết quả xóa hàng loạt** — component mới `KetQuaHangLoatModal.tsx`, cấu trúc theo **BR45.3**:

```
┌──────────────────────────────────────────────────────────┐
│ Thông báo kết quả Xóa                                [×] │
├──────────────────────────────────────────────────────────┤
│ **Thực hiện thành công X/N chứng từ. Thất bại Y chứng từ.**│
│ ┌ CommonListTable ─────────────────────────────────────┐ │
│ │ Số chứng từ (link) │ Ngày chứng từ │ Nguyên nhân     │ │
│ └──────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────┤
│                                              [Đóng]      │
└──────────────────────────────────────────────────────────┘
```

## 2. Đặc tả UI

Chưa có Figma. Dùng nguyên `CommonConfirmModal` (A) và `CommonModalShell` + `CommonListTable` (B) ở
kích thước mặc định của design system — **không phát minh số đo**. Nút xác nhận bên **phải**, nút
hủy bên **trái** (BR3).

## 3. Ma trận

Không áp dụng. Điều kiện hiển thị nút Xóa nằm ở [01 §5.2](01-danh-sach-dung-chung.md) và
[04 §5](04-popup-xem-chi-tiet.md).

## 4. Trường & thành phần

**Popup A** *(control lấy theo bảng Thành phần v2 — BA đã chuẩn hoá tên control thành
`TextField` / `Button`; nội dung chữ nay nằm ở §Thông báo của SCR, không còn trong cột Mô tả)*:

| Thành phần | Control (v2) | Nội dung | Khóa i18n |
|---|---|---|---|
| Tiêu đề popup | `TextField` | "Xác nhận xóa chứng từ bán dịch vụ" | `banHang:banDichVu.confirm.xoa.title` |
| Thông báo chính | `TextField` | **MSG_PMKT-E-06195_027** "Bạn có chắc chắn muốn xóa chứng từ bán dịch vụ này không?" | `…confirm.xoa.content` |
| Nút Xác nhận | `Button` | thực hiện xóa | `…confirm.xoa.ok` |
| Nút Hủy | `Button` | đóng, không xóa | dùng lại khóa chung |
| Biểu tượng đóng popup | `Button` | đóng, không xóa (BR3) | — |

> **Lệch BR3 (nhỏ, cố ý):** BR3 quy định nội dung popup xác nhận xóa chung là *"Bạn có chắc chắn
> muốn xóa **{Loại đối tượng}** **'{Tên/Số}'**? Thao tác này không thể hoàn tác."* — có tên/số bản
> ghi. Epic khai message riêng MSG_..._027 **không** có tên/số. **Epic thắng trong phạm vi epic**,
> dùng nguyên văn MSG_..._027. Nêu ở biên bản review.

**Popup B (cột bảng chi tiết lỗi — BR45.3):**

| Cột | Nguồn | Ghi chú |
|---|---|---|
| Số chứng từ | `soChungTu` | link mở popup Xem chi tiết |
| Ngày chứng từ | `ngayChungTu` | `DD/MM/YYYY` |
| Nguyên nhân | message BE trả về | nguyên văn (MSG_..._031 / _032 / _014 …) |

## 5. Hành vi & sự kiện

### 5.1 Xóa một chứng từ

| Bước | Việc |
|---|---|
| 1 | Nút "Xóa" trên dòng hiện khi **`ChungTuBan.TrangThaiGhiSo`** = "Chưa ghi sổ" **AND** có `BanDichVu.Delete`; không quyền ⇒ **ẩn** (BR25.2) |
| 2 | Click ⇒ mở popup A |
| 3 | Xác nhận ⇒ `DELETE /{id}` kèm `updatedAt` (optimistic lock) |
| 4 | Thành công ⇒ toast **MSG_PMKT-E-06195_030** "Xóa chứng từ thành công" → invalidate list → bỏ chọn dòng đó khỏi quick-detail và khỏi tập tích chọn |
| 5 | Thất bại ⇒ toast đỏ với message BE (§5.3) |

**Xóa mềm** (`IsDeleted = true`, BR29.1) — BE làm. Chứng từ con tự sinh (Hóa đơn bán hàng, Phiếu
thu) **cũng bị xóa mềm theo** (BR29.2, `UC_CTbanDichVu_Xoa.md` §Quy tắc xóa chứng từ) — BE làm, FE
không cần biết.

### 5.2 Xóa hàng loạt

| Bước | Việc |
|---|---|
| 1 | Nút "Xóa hàng loạt" hiện khi có **≥1** dòng tích chọn. **Luôn enabled** — không disable theo trạng thái/liên kết của dòng (`UC_CTbanDichVu_Xoa.md` §Quy tắc hiển thị nút "Xóa hàng loạt") |
| 2 | Click ⇒ popup A (nội dung số nhiều) |
| 3 | Xác nhận ⇒ `POST /xoa-hang-loat` với danh sách id |
| 4 | Thành công **100%** ⇒ toast *"Đã xóa thành công {X} chứng từ."* (BR45.1) |
| 5 | Có bản ghi lỗi ⇒ **popup B** với tổng kết + bảng chi tiết (BR45.2, BR45.3). BA cũng khai message **MSG_PMKT-E-06195_054** *"Xóa thành công {x}/{n} chứng từ. {y} chứng từ đã ghi sổ không được xóa."* — dùng làm dòng tổng kết |
| 6 | Đóng popup B ⇒ **tự reload danh sách**, giữ nguyên lọc/tìm kiếm/sắp xếp/phân trang (BR45.4) |

> **Lệch nhỏ cần chốt:** MSG_..._054 chỉ diễn đạt được **một** nguyên nhân ("đã ghi sổ"), trong khi
> UC liệt kê 4 nguyên nhân (đã ghi sổ · đã phát hành hóa đơn · đã tạo phiếu thu · đã được tham chiếu).
> Dùng MSG_..._054 làm dòng tổng kết + **bảng chi tiết BR45.3 để nêu đích danh từng nguyên nhân**.

### 5.3 Lỗi cần hiển thị nguyên văn

| Tình huống | Message | Mã | Ai kiểm |
|---|---|---|---|
| Chứng từ đã được sử dụng ở nghiệp vụ khác | "Chứng từ đã được sử dụng, không thể xóa" | MSG_..._014 | **BE** |
| Chứng từ đã ghi sổ | "Chứng từ đã ghi sổ, không thể xóa" | MSG_..._031 | **BE** (FE cũng đã ẩn nút, đây là chặn tầng hai) |
| Chứng từ đã phát hành hóa đơn | "Chứng từ đã phát hành hóa đơn, không thể xóa" | MSG_..._032 | **BE** |
| Lỗi khác | "Xóa chứng từ thất bại" | MSG_..._033 | **BE** |
| Không có quyền | "Không có quyền truy cập" | MSG_..._011 | **BE** |

> Ba điều kiện "đã được sử dụng" (đã phát hành hóa đơn / đã tạo phiếu thu / đã được tham chiếu bởi
> chứng từ khác) đòi dữ liệu tham chiếu chéo mà lưới **không** có ⇒ **BE kiểm, FE chỉ hiển thị**.
> UC ghi rõ: *"Nút Xóa vẫn hiển thị (nếu chưa ghi sổ) … Khi click → Hiển thị thông báo lỗi"*.

## 6. Validation phía FE

Không có nhập liệu. FE chỉ kiểm **hai** điều kiện hiển thị nút (trạng thái "Chưa ghi sổ" + quyền);
mọi điều kiện nghiệp vụ còn lại do BE.

## 7. Luồng xử lý

```
Lưới ──(⋮ Xóa)──▶ popup A ──(Xác nhận)──▶ DELETE /{id}
                                            ├─ 2xx ─▶ toast MSG_030 ─▶ invalidate ─▶ lưới nạp lại
                                            └─ lỗi ─▶ toast đỏ (message BE), popup đã đóng

Lưới ──(Xóa hàng loạt)──▶ popup A ──(Xác nhận)──▶ POST /xoa-hang-loat
                                                   ├─ toàn thành công ─▶ toast BR45.1 ─▶ reload
                                                   └─ có lỗi ─▶ popup B ─(Đóng)─▶ reload
```

## 8. Phân bổ file

| Việc | File |
|---|---|
| Mutation xóa đơn | `api/queries.ts` (`useDelete`) — đã có mẫu ở `ChungTuBanHangTab.tsx:265-282`. **Dùng resource sẵn có**, không tạo adapter mới ([00 D2](00-ke-hoach-tong.md)) |
| Endpoint xóa hàng loạt + Zod của `KetQuaHangLoatDto` | `api/chungTuBanHangApi.ts` · `api/model.ts` |
| State + điều phối hàng loạt | `hooks/useHangLoat.ts` 🆕 |
| Popup xác nhận | `@base CommonConfirmModal` (dùng lại) |
| Popup kết quả hàng loạt | `components/KetQuaHangLoatModal.tsx` 🆕 — đã kiểm `src/base/index.ts`, không có shell "kết quả hàng loạt" dựng sẵn |
| Cột bảng chi tiết lỗi | `fields/hangLoatColumns.ts` 🆕 |
| Chữ | `i18n/vi.ts` · `en.ts` |

> `KetQuaHangLoatModal` dùng chung cho **Xóa · Ghi sổ · Bỏ ghi sổ** ([06](06-ghi-so-bo-ghi-so.md)) —
> khác nhau đúng ở tiêu đề và dòng tổng kết, truyền qua prop. Nếu sau này màn khác cũng cần, đẩy lên
> `@base`.

## 9. Kiểm thử

| # | Input | Kỳ vọng |
|---|---|---|
| T0 | dòng bán dịch vụ, user có `BanDichVu.Delete` nhưng không có `BanHangHoa.Delete` | nút Xóa **hiện** (gate theo `loaiNghiepVu` — [01 §5.2](01-danh-sach-dung-chung.md)) |
| T1 | dòng "Chưa ghi sổ", có `.Delete` | nút Xóa hiện |
| T2 | dòng "Đã ghi sổ" | nút Xóa **ẩn** |
| T3 | không có `.Delete` | nút Xóa **ẩn** (không disable) |
| T4 | xác nhận xóa, BE 2xx | toast MSG_..._030; dòng biến mất khỏi lưới; quick-detail bỏ binding |
| T5 | xác nhận xóa, BE trả MSG_..._014 | toast đỏ nguyên văn message BE |
| T6 | tích 3 dòng, 1 dòng đã ghi sổ, xóa hàng loạt | popup B: "Thực hiện thành công 2/3 chứng từ. Thất bại 1 chứng từ." + 1 dòng bảng lỗi |
| T7 | tích 3 dòng hợp lệ | **không** mở popup B, chỉ toast "Đã xóa thành công 3 chứng từ." |
| T8 | đóng popup B | lưới reload, bộ lọc + trang + sắp xếp **giữ nguyên** |
| T9 | tích 0 dòng | nút Xóa hàng loạt không hiện |
| T10 | tích ≥1 dòng, tất cả đã ghi sổ | nút Xóa hàng loạt **vẫn enabled** (theo UC) |

## 10. BR đã áp dụng

BR3 · BR13.1 · BR25 · BR26 · BR29 (xóa mềm + cascade) · BR45 (toàn bộ 4 mục).

**Chưa đạt / lệch:**
- **BR3** — nội dung popup xác nhận xóa không có `{Tên/Số}` chứng từ (epic khai message riêng). Ghi
  rõ là lệch, epic thắng.
- **BR29.4** ("giữ nguyên vị trí trang sau khi sửa/xóa") — phụ thuộc hành vi reload của lưới dùng
  chung; cần kiểm lại khi nối API thật.
