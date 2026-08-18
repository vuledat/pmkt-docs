# 06 — Ghi sổ / Bỏ ghi sổ (đơn + hàng loạt)

| | |
|---|---|
| **Phiên bản** | **v2 — 2026-08-15** (đồng bộ BA commit `1a928c53b`) |
| **UC nguồn** | `UC_CTbanDichVu_GhiSo` (PMKT-U-06449) · `UC_CTbanDichVu_BoGhiSo` (PMKT-U-06451) |
| **SCR nguồn** | **Không có SCR riêng** — thao tác nằm trên lưới ([01](01-danh-sach-dung-chung.md)) và popup Xem chi tiết ([04](04-popup-xem-chi-tiet.md)) |
| **Ma trận** | Không có |
| **Figma** | Không có frame riêng |
| **Quyền** | `BanDichVu.Post` (ghi sổ) · `BanDichVu.Unpost` (bỏ ghi sổ) |

---

## 1. Bố cục

Không có màn mới. Hai popup dùng chung:

- **Popup xác nhận** — `CommonConfirmModal`, tiêu đề "Xác nhận ghi sổ" / "Xác nhận bỏ ghi sổ".
- **Popup kết quả hàng loạt** — `components/KetQuaHangLoatModal.tsx` (dùng chung với
  [05](05-popup-xac-nhan-xoa.md)), cấu trúc BR45.3.

> ⚠ **Mâu thuẫn nguồn về popup xác nhận — cần BA chốt.**
> `UC_CTbanDichVu_GhiSo.md` Luồng chính bước 3: *"Hệ thống hiển thị popup xác nhận ghi sổ"* (tương tự
> cho Bỏ ghi sổ). Nhưng **BR13.2** ghi *"Ghi sổ … Thực hiện ghi sổ **trực tiếp (không hiển thị popup
> xác nhận)**"*, tương tự cho Bỏ ghi sổ.
> **Xử lý đề xuất:** theo **UC** (có popup xác nhận) — epic thắng trong phạm vi epic; và popup là
> hành vi an toàn hơn cho một thao tác ghi vào sổ cái. **Ghi rõ là đang lệch BR13.2.**
> *(Lưu ý phân biệt: nút "Lưu và ghi sổ" **trên form** thì đúng là không hỏi xác nhận — BR13.2 và UC
> khớp nhau ở điểm đó.)*

## 2. Ghi sổ — đơn lẻ

| Bước | Việc |
|---|---|
| 1 | Nút "Ghi sổ" hiện khi **`ChungTuBan.TrangThaiGhiSo`** = "Chưa ghi sổ" **AND** có `BanDichVu.Post`; thiếu quyền ⇒ **ẩn** (BR25.2). Helper đã có: `helpers/trangThai.ts:53 coTheGhiSo` |
| 2 | Click ⇒ popup xác nhận |
| 3 | Xác nhận ⇒ `POST …/{id}/ghi-so` |
| 4 | BE: validate → sinh bút toán ([02 §7.4](02-popup-them-moi.md), **không gộp** — BR36 chung · **BR20** của CTBH) → cập nhật sổ cái/công nợ → cộng dồn `SoLuongDaBan` + `SoLuongDaXuat` cho Đơn đặt hàng liên kết (**BR05** của SCR ThemMoi) → `TrangThaiGhiSo` = "Đã ghi sổ" |
| 5 | Thành công ⇒ toast **MSG_PMKT-E-06195_004** "Lưu và ghi sổ chứng từ thành công" → invalidate → lưới nạp lại |
| 6 | Lỗi ⇒ toast đỏ (§4), trạng thái **giữ nguyên** "Chưa ghi sổ" |

**Sau khi ghi sổ:** popup Xem chi tiết (nếu đang mở) đổi bộ nút sang C2 — ẩn Chỉnh sửa/Ghi sổ/Xóa,
hiện Bỏ ghi sổ (+ Lập hóa đơn theo `(đk-HĐ)`). Xem [04 §3](04-popup-xem-chi-tiet.md).

**Ghi sổ duy nhất (BR12):** chứng từ đã ghi sổ ⇒ không sinh bút toán lần nữa; nếu bị gọi ép qua API ⇒
**MSG_PMKT-E-06195_016**.

## 3. Bỏ ghi sổ — đơn lẻ

| Bước | Việc |
|---|---|
| 1 | Nút "Bỏ ghi sổ" hiện khi **`ChungTuBan.TrangThaiGhiSo`** = "Đã ghi sổ" **AND** có `BanDichVu.Unpost` (BR42.2). Helper: `helpers/trangThai.ts:58 coTheBoGhiSo` |
| 2 | Click ⇒ popup xác nhận |
| 3 | Xác nhận ⇒ `POST …/{id}/bo-ghi-so` |
| 4 | BE kiểm điều kiện: (a) chứng từ **chưa lập hóa đơn** (**`ChungTuBan.TrangThaiLapHoaDon`** = "Chưa lập"); (b) chứng từ **"Thu tiền sau"** đã có phiếu thu riêng tham chiếu ⇒ **cấm** |
| 5 | Hợp lệ ⇒ **xóa toàn bộ định khoản đã sinh** khỏi Sổ cái → hoàn sổ công nợ → trừ `SoLuongDaBan`/`SoLuongDaXuat` của Đơn đặt hàng (**BR05**) → `TrangThaiGhiSo` = "Chưa ghi sổ" |
| 6 | Thành công ⇒ toast **MSG_PMKT-E-06195_009** "Bỏ ghi sổ chứng từ bán dịch vụ thành công" → invalidate |
| 7 | Lỗi ⇒ toast đỏ, trạng thái **giữ nguyên** "Đã ghi sổ" |

> Điều kiện (a) và (b) đòi dữ liệu tham chiếu chéo mà lưới không có ⇒ **BE kiểm, FE hiển thị lỗi**.
> Đây là đề xuất, cần BA xác nhận — [00 §12 Q7](00-ke-hoach-tong.md).
>
> ⚠ **v2 — điều kiện (b) có thể không còn tồn tại.** `SCR_CTbanDichVu_ThemMoi.md:35` (mới thêm) nói
> chứng từ bán dịch vụ *"tự nó đóng vai phiếu thu — **không sinh bản ghi `ENT_PhieuThu`**"*. Nếu đúng
> vậy thì tình huống "đã có phiếu thu riêng tham chiếu" (MSG_..._010) **không xảy ra** với bán dịch
> vụ. Nhưng `UC_CTbanDichVu_BoGhiSo.md` vẫn giữ nguyên luật này, và `3.crud-matrix.md:22` vẫn để
> `ENT_PhieuThu` = D ở UC_BoGhiSo. ⇒ [00 §12 Q10](00-ke-hoach-tong.md). **Chốt trước khi code.**

## 4. Thao tác hàng loạt (BR45 + BR42.3)

| | Ghi sổ hàng loạt | Bỏ ghi sổ hàng loạt |
|---|---|---|
| Điều kiện nút | ≥1 dòng tích chọn (BR13.1) | ≥1 dòng tích chọn |
| Endpoint | `POST …/ghi-so-hang-loat` | `POST …/bo-ghi-so-hang-loat` |
| Bỏ qua | chứng từ **đã ghi sổ** | chứng từ **chưa ghi sổ** (BR42.3) |
| Thành công 100% | toast *"Đã ghi sổ thành công {X} chứng từ."* (BR45.1) | toast *"Đã bỏ ghi sổ thành công {X} chứng từ."* |
| Có bản lỗi | popup kết quả (BR45.3), tiêu đề *"Thông báo kết quả Ghi sổ"* | tiêu đề *"Thông báo kết quả Bỏ ghi sổ"* |
| Cảnh báo trước khi chạy | **MSG_PMKT-E-06195_106** "Có {n} chứng từ đã ghi sổ trong số chứng từ được chọn" | BR42.3: *"Bỏ ghi sổ thành công X/Y chứng từ. Đã bỏ qua Z chứng từ chưa ghi sổ."* |
| Đóng popup kết quả | reload lưới, giữ lọc/sort/trang (BR45.4) | như bên |

> **MSG_..._106 là `Warning`** (theo `6.messages.md`), tức cảnh báo **trước** khi chạy — hiển thị
> trong popup xác nhận ghi sổ hàng loạt khi tập chọn có lẫn chứng từ đã ghi sổ. Không thay thế popup
> kết quả BR45.3.

## 5. Message

| Tình huống | Message | Mã | Loại | Ai kiểm |
|---|---|---|---|---|
| Ghi sổ thành công | "Lưu và ghi sổ chứng từ thành công" | MSG_..._004 | Success | — |
| Bỏ ghi sổ thành công | "Bỏ ghi sổ chứng từ bán dịch vụ thành công" | MSG_..._009 | Success | — |
| Lỗi khi ghi sổ | "Lỗi khi ghi sổ chứng từ" | MSG_..._015 | Error | BE |
| Ghi sổ chứng từ đã ghi sổ | "Không thể ghi sổ chứng từ đã ghi sổ" | MSG_..._016 | Error | BE |
| Lỗi khi bỏ ghi sổ | "Lỗi khi bỏ ghi sổ chứng từ" | MSG_..._017 | Error | BE |
| Bỏ ghi sổ chứng từ chưa ghi sổ | "Không thể bỏ ghi sổ chứng từ chưa ghi sổ" | MSG_..._023 | Error | BE |
| Chứng từ "Thu tiền sau" có phiếu thu riêng | "Chứng từ \"Thu tiền sau\" đã có phiếu thu riêng tham chiếu, không được bỏ ghi sổ" | MSG_..._010 | Error | BE |
| Chứng từ không tồn tại | "Chứng từ không tồn tại" | MSG_..._012 | Error | BE |
| Có chứng từ đã ghi sổ trong tập chọn | "Có {n} chứng từ đã ghi sổ trong số chứng từ được chọn" | MSG_..._106 | Warning | FE (đếm tại chỗ) |
| Kỳ kế toán đã khóa | *(message BE)* | BR17 | Error | BE |

Toast theo BR26: góc phải trên, tự ẩn 3–5s, tối đa 3 toast chồng, màu theo loại.

## 6. Validation phía FE

FE **chỉ** kiểm hai thứ (đủ để ẩn/hiện nút và cảnh báo trước):
1. `trangThaiChungTu` — qua `coTheGhiSo` / `coTheBoGhiSo` (`helpers/trangThai.ts:53,58`).
2. Quyền `.Post` / `.Unpost`.

Mọi điều kiện nghiệp vụ còn lại (kỳ kế toán BR17 · đã lập hóa đơn · có phiếu thu tham chiếu · tài
khoản hạch toán đủ) do **BE** kiểm; FE hiển thị nguyên văn message trả về.

## 7. Luồng xử lý

```
Lưới / popup Xem ──(Ghi sổ)──▶ CommonConfirmModal
      │                              └─(Xác nhận)─▶ POST /{id}/ghi-so
      │                                                ├─ 2xx ─▶ toast MSG_004 ─▶ invalidate:'all'
      │                                                └─ lỗi ─▶ toast đỏ, trạng thái giữ nguyên
      └──(Ghi sổ hàng loạt)──▶ đếm dòng đã ghi sổ ─▶ ConfirmModal (+ cảnh báo MSG_106 nếu có)
                                     └─(Xác nhận)─▶ POST /ghi-so-hang-loat
                                                      ├─ 100% ok ─▶ toast BR45.1
                                                      └─ có lỗi ─▶ KetQuaHangLoatModal ─(Đóng)─▶ reload
```

Bỏ ghi sổ: sơ đồ đối xứng.

Trong lúc mutation chạy: nút xác nhận `loading`, khóa để không double-submit; dòng đang xử lý không
cần khóa riêng (invalidate sẽ nạp lại toàn bộ).

## 8. Phân bổ file

| Việc | File |
|---|---|
| Điều kiện trạng thái (thuần) | `helpers/trangThai.ts` — `coTheGhiSo:53`, `coTheBoGhiSo:58` **đã có, dùng lại**; đổi tên field sang `TrangThaiGhiSo` |
| Đếm dòng đã/chưa ghi sổ trong tập chọn (thuần) | `helpers/hangLoat.ts` 🆕 |
| Endpoint ghi sổ / bỏ ghi sổ / hàng loạt + Zod `KetQuaHangLoatDto` | `api/chungTuBanHangApi.ts` · `api/model.ts` — **resource sẵn có**, không tạo adapter mới ([00 D2](00-ke-hoach-tong.md)) |
| Mutation + invalidate | `api/queries.ts` |
| State + điều phối | `hooks/useHangLoat.ts` 🆕 |
| Popup xác nhận | `components/GhiSoConfirmModal.tsx` 🆕 (bọc `@base CommonConfirmModal` + cảnh báo MSG_106) |
| Popup kết quả | `components/KetQuaHangLoatModal.tsx` 🆕 (dùng chung với [05](05-popup-xac-nhan-xoa.md)) |
| Chữ | `i18n/vi.ts` · `en.ts` |

> Hiện `ChungTuBanHangTab.tsx:288-301` đang route mọi entry ⋮ không phải edit/delete sang
> `toast.info(comingSoon)`. Phiếu này thay 2 nhánh `ghiSo` / `boGhiSo` bằng luồng thật —
> **cho cả hai loại chứng từ**, vì lưới dùng chung. Đây là chỗ duy nhất phiếu này **mở rộng phạm vi
> sang E-06194**; nếu BA muốn giữ E-06194 nguyên trạng thì phải gate theo `loaiChungTu` —
> hỏi khi review.

## 9. Kiểm thử

| # | Input | Kỳ vọng |
|---|---|---|
| T1 | dòng "Chưa ghi sổ", có `.Post` | nút Ghi sổ hiện; Bỏ ghi sổ ẩn |
| T2 | dòng "Đã ghi sổ", có `.Unpost` | nút Bỏ ghi sổ hiện; Ghi sổ ẩn |
| T3 | dòng "Chưa ghi sổ", không `.Post` | Ghi sổ **ẩn** (không disable) |
| T4 | ghi sổ thành công | toast MSG_..._004; lưới nạp lại; trạng thái dòng đổi |
| T5 | BE trả MSG_..._016 | toast đỏ nguyên văn; trạng thái **không** đổi |
| T6 | bỏ ghi sổ chứng từ "Thu tiền sau" có phiếu thu | toast MSG_..._010 |
| T7 | tích 5 dòng, 2 đã ghi sổ, bấm Ghi sổ hàng loạt | popup xác nhận kèm cảnh báo MSG_..._106 với `n = 2` |
| T8 | ghi sổ hàng loạt 5 dòng, 1 lỗi | popup kết quả "Thực hiện thành công 4/5 chứng từ. Thất bại 1 chứng từ." + bảng 1 dòng |
| T9 | đóng popup kết quả | reload, giữ nguyên lọc/sort/trang |
| T10 | `helpers/hangLoat.ts` đếm | trả đúng số dòng "Đã ghi sổ" / "Chưa ghi sổ" trong tập chọn |

## 10. BR đã áp dụng

BR3 · BR12 (vòng đời + ghi sổ duy nhất) · BR13.1 · BR16 · BR25 · BR26 · BR33 · BR36 (không gộp bút
toán) · BR42 (toàn bộ) · BR45 (toàn bộ).

Của CTBH: **BR20** (sinh bút toán, không gộp) · **BR21** (ghi sổ / bỏ ghi sổ) · **BR23** (theo dõi số
lượng đã xuất).

**Chưa đạt / lệch:**
- **BR13.2** — UC yêu cầu popup xác nhận, BR13.2 nói "không hiển thị popup xác nhận". Theo UC, ghi rõ
  là lệch ⇒ §1.
- **BR17 kỳ kế toán** — BE kiểm, FE chỉ hiển thị lỗi.
- **BR41 tham chiếu chéo** — điều kiện bỏ ghi sổ dựa vào tham chiếu chéo, do BE ⇒
  [00 §12 Q7](00-ke-hoach-tong.md) và **Q10** (`ENT_PhieuThu` có sinh hay không).
