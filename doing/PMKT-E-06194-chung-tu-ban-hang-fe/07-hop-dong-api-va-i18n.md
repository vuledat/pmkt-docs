# 07 — Hợp đồng API & i18n

## 1. Hợp đồng với BE

Không đổi cho các endpoint đã có (xem `00-ke-hoach-tong.md` §2 bảng "API BE"). Việc mới của đợt này:

| Endpoint | Method | Trạng thái | Ghi chú |
|---|---|---|---|
| `{base}/lookup` | POST | ✅ Đã có | Không đổi — vẫn trả cả 3 giá trị `LoaiNghiepVu`, FE tự lọc (F1, đã đóng) |
| Danh mục Đơn đặt hàng (D5) | ? | ❓ Chưa xác nhận | Q2 — nếu chưa có, FE dùng placeholder `CHUA_CO_DANH_MUC` giống Hợp đồng |
| `acc_so_cai` theo nhóm chứng từ (D7, chế độ Dữ liệu sổ) | ? | ❓ Chưa xác nhận | Q7 ở `06-popup-xem-du-lieu-ghi-so.md` |
| `PUT {base}/{id}` (Sửa) | PUT | ❌ Chưa dựng | F12 — ngoài phạm vi, chặn bởi BE |

Zod schema hiện có (`api/model.ts`) — không đổi trường nào ở đợt này ngoại trừ thêm optional field cho D5:

```ts
// fields/types.ts — ChungTuBanHangLine, thêm 1 dòng (đối xứng hopDongId)
donDatHangId?: string
```

```ts
// api/model.ts — chungTuBanHangChiTietSchema, thêm 1 dòng (đối xứng hopDongId: z.string().nullish())
donDatHangId: z.string().nullish(),
```

**Không đổi tên field `trangThaiChungTu`** (D1/Q1) — giữ nguyên toàn bộ schema liên quan.

## 2. Trạng thái API

| Endpoint | Đã có / Chưa có | Ghi chú |
|---|---|---|
| `POST {base}` | Đã có | |
| `GET {base}/{id}` | Đã có | |
| `PUT {base}/{id}` | **Chưa có** | Nợ — không có `mock.ts` (module không dùng mock, đúng chuẩn), chỉ disable nút Lưu ở mode Sửa |
| `{base}/{id}/ghi-so`, `/bo-ghi-so` (+ hàng loạt) | Đã có | |
| `DELETE {base}/{id}`, `/xoa-hang-loat` | Đã có | |
| Danh mục Vụ việc, Hợp đồng | Chưa có | Placeholder `CHUA_CO_DANH_MUC` |
| Danh mục Đơn đặt hàng (D5) | Chưa xác nhận | Q2 |
| `acc_so_cai` theo nhóm (D7) | Chưa xác nhận | Q7 |

Module **không có `mock.ts`** — đúng chuẩn (`client/CLAUDE.md §4.1-4.3`, "còn `mock.ts` = còn nợ"); các phần chưa nối API dùng trạng thái UI "đang phát triển" (toast) thay vì dữ liệu giả.

## 3. Bảng khoá i18n (chỉ khoá MỚI của đợt này)

Namespace: `banHang` (duy nhất cho cả module, không mở namespace mới).

| Khoá | `vi` | `en` |
|---|---|---|
| `list.rowAction.lapPhieuXuat` | Lập phiếu xuất | Create goods issue note |
| `themMoi.grid.donDatHang` | Đơn đặt hàng | Purchase order |
| `themMoi.footer.xemDuLieuGhiSo` | Xem dữ liệu ghi sổ | View posting data |
| `xemDuLieuGhiSo.title` | Xem dữ liệu ghi sổ | View posting data |
| `xemDuLieuGhiSo.modeXemTruoc` | Xem trước | Preview |
| `xemDuLieuGhiSo.modeDuLieuSo` | Dữ liệu sổ | Posted data |
| `xemDuLieuGhiSo.empty` | Không có dữ liệu | No data |
| `xemDuLieuGhiSo.col.ngayHachToan` | Ngày hạch toán | Posting date |
| `xemDuLieuGhiSo.col.ngayChungTu` | Ngày chứng từ | Voucher date |
| `xemDuLieuGhiSo.col.soChungTu` | Số chứng từ | Voucher no. |
| `xemDuLieuGhiSo.col.maDoiTuong` | Mã đối tượng | Object code |
| `xemDuLieuGhiSo.col.tenDoiTuong` | Tên đối tượng | Object name |
| `xemDuLieuGhiSo.col.dienGiai` | Diễn giải | Description |
| `xemDuLieuGhiSo.col.taiKhoan` | Tài khoản | Account |
| `xemDuLieuGhiSo.col.taiKhoanDoiUng` | Tài khoản đối ứng | Contra account |
| `xemDuLieuGhiSo.col.phatSinhNo` | Phát sinh nợ | Debit |
| `xemDuLieuGhiSo.col.phatSinhCo` | Phát sinh có | Credit |
| `xemDuLieuGhiSo.col.vuViec` | Vụ việc | Case |
| `xemDuLieuGhiSo.col.khoanMucCP` | Khoản mục chi phí | Cost item |
| `xemDuLieuGhiSo.col.doiTuongTHCP` | Đối tượng THCP | Cost object |
| `xemDuLieuGhiSo.col.donVi` | Đơn vị | Unit |
| `xemDuLieuGhiSo.tongPSNo` | Tổng phát sinh nợ | Total debit |
| `xemDuLieuGhiSo.tongPSCo` | Tổng phát sinh có | Total credit |
| `common.button.dong` | Đóng | *(dùng lại khoá chung nếu đã có, không tạo khoá mới trùng nghĩa — kiểm tra `i18n/vi.ts` trước khi thêm)* | |

Giá trị `vi` lấy **nguyên văn** nhãn trong SCR (không tự diễn đạt lại), theo Luật 2 của `CLAUDE.md` gốc.

**Không thêm khoá cho `MSG_PMKT-E-06194_*`** (D3) — kể cả các mã mới `_052`, `_108` — vì hiển thị nguyên văn từ BE qua `apiError.ts`.

## 4. Hằng số nghiệp vụ

Không thêm hằng số magic-value mới cho đợt này — D4/D5/D7 đều dùng lại enum/hằng đã có (`TRANG_THAI_HOA_DON`, `TRANG_THAI_XUAT_HANG`, `LOAI_NGHIEP_VU` ở `helpers/trangThai.ts`, `constants/constants.ts`).

Riêng D4b cần 1 hằng cho tập trạng thái "còn xuất được", đặt cạnh `TRANG_THAI_CHUA_GHI_SO` (`helpers/trangThai.ts`):
```ts
export const TRANG_THAI_XUAT_HANG_CON_XUAT: readonly string[] = [
  TRANG_THAI_XUAT_HANG.chuaXuat,
  TRANG_THAI_XUAT_HANG.xuatMotPhan,
]
export const TRANG_THAI_HOA_DON_CON_LAP: readonly string[] = [
  TRANG_THAI_HOA_DON.chuaLap,
  TRANG_THAI_HOA_DON.daLapMotPhan,
]
```

## 5. Mã quyền

| Mã | Đã có | Ghi chú |
|---|---|---|
| `BAN_HANG_CHUNG_TU_PERM.lapHoaDon` = `LapHoaDonBan.Create` | ✅ | không đổi |
| `BAN_HANG_CHUNG_TU_PERM.lapPhieuXuat` | ❌ **Chờ Q3** | dự kiến `PhieuXuatKho.Create` — cần xác nhận với BE trước khi thêm vào `constants/permissions.ts` |

## 6. Đường dẫn

Không đổi — `constants/paths.ts` không có route mới (popup, không phải trang riêng).
