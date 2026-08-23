# 04 — Hợp đồng API và i18n

## 1. Hợp đồng với BE

Base path: `/api/ban-hang/hoa-don-ban-hang` (`api/hoaDonBanHangApi.ts:32`) — khớp
`@RequestMapping` của `HoaDonBanHangController.java:35`. Đi theo hợp đồng BASE-CRUD v1 của
`BaseCrudController` (`cell-app/CLAUDE.md`), **không phải hợp đồng đề xuất riêng** — đây là điểm khác
biệt lớn nhất so với ngày 12/08, khi cả 8 endpoint đều còn là "đề xuất FE".

| Method · Path | Trạng thái BE | Query key | Ghi chú |
| :-- | :-- | :-- | :-- |
| `POST /tim-kiem` | ✅ **THẬT** (từ 14/08) | `createSearchQueries` theo tenant (`api/queries.ts`) | lọc động, phân trang, `summary` (BR31), cột "Hóa đơn liên quan" (BR07) |
| `GET /cot` | ✅ THẬT | — | whitelist `@Searchable` cho bộ lọc nâng cao |
| `GET /{id}` | ⚠ THẬT nhưng **HEADER-ONLY** — `chiTiet` luôn `null` (`package-info.java:19-22`) | | dùng cho popup Xem chi tiết + panel Xem nhanh; lưới dòng hàng **chưa nạp được từ BE thật** |
| `POST /` (create) | ❌ 400 tường minh (`HoaDonBanHangController.java:72-75`) | | `LuuHoaDonBanHangBody` (FE) vẫn để mở `Record<string, unknown>` — siết kiểu khi BE lên |
| `PUT /{id}` (update) | ❌ 400 tường minh (dòng 77-80) | | mang `updatedAt` optimistic lock |
| `DELETE /{id}` | ❌ 400 tường minh (dòng 82-86) | | |
| `POST /xoa-hang-loat` | ❌ chưa có route ở BE (không nằm trong `BaseCrudController`, là endpoint riêng của module) | | FE gọi thẳng `http.post`, response parse qua `ketQuaXoaHangLoatSchema` |
| `POST /export` | ❌ 403 mọi user (kể cả Admin) — `LapHoaDonBan.Export` chưa seed | | Javadoc controller dòng 30-32 |

**Request mẫu `POST /tim-kiem`** (dựng từ `toSearchRequest`, `api/hoaDonBanHangApi.ts:80-106`):

```json
{
  "page": 0,
  "pageSize": 20,
  "sort": "ngayHoaDon:desc,soHoaDon:asc",
  "filters": [
    { "field": "ngayHoaDon", "op": "between", "value": ["2026-08-01", "2026-08-31"] },
    { "field": "trangThaiPhatHanhHoaDon", "op": "eq", "value": "CHUA_PHAT_HANH" }
  ]
}
```

**Response mẫu** (khớp `HoaDonBanHangDto.java:24-75`):

```json
{
  "data": [{
    "id": "…", "soHoaDon": "00000123", "kyHieuHoaDon": "1C25TAA",
    "mauSoHoaDonId": "…", "ngayHoaDon": "2026-08-20",
    "loaiNghiepVu": "TRONG_NUOC",
    "tenKhachHang": "…", "maSoThue": "…",
    "trangThaiLapChungTu": "CHUA_LAP", "trangThaiPhatHanhHoaDon": "CHUA_PHAT_HANH",
    "trangThaiHoaDon": "GOC",
    "hoaDonLienQuan": [],
    "tongTienThueGtgtQuyDoi": 1000000,
    "updatedAt": "2026-08-20T10:00:00Z"
  }],
  "pagination": { "totalPages": 3 },
  "summary": { "tongTienThueGtgt": 25000000 }
}
```

⚠ Giá trị enum trên wire là **TÊN HẰNG Java** (`CHUA_PHAT_HANH`, `GOC`…), không phải chuỗi tiếng Việt
— quy ước bắt buộc theo `package-info.java:26-30` (bộ lọc động dùng `Enum.valueOf(name)`). FE đã đúng
convention này ở `constants/constants.ts` — không cần sửa.

## 2. Trạng thái API

| Endpoint | Đã có thật | Ghi chú nợ |
| :-- | :-- | :-- |
| Danh sách / cột / chi tiết header | ✅ | `api/mock.ts` KHÔNG còn dùng cho 3 endpoint này (`HDBH_DUNG_MOCK=false`) |
| Dòng chi tiết hàng hóa (`chiTiet` của `GET /{id}`) | ❌ | Popup Xem chi tiết + Cập nhật hiện KHÔNG tải được lưới dòng hàng từ BE thật — vẫn phụ thuộc `api/mock.ts` qua nhánh chưa gỡ |
| Thêm / Sửa / Xóa / Xóa hàng loạt | ❌ | `api/mock.ts` (355 dòng) vẫn là đường đi thật của các luồng này khi test cục bộ; **không xoá** cho tới khi BE công bố |
| Kiểm trùng số HĐ (BR03) | ❌ | Không có endpoint riêng — dựa vào lỗi trả về của `POST /` khi BE lên |
| Xuất Excel | ❌ (403 cứng) | Ngoài phạm vi PYC — B4.3 không cấp quyền Export |

## 3. Bảng khoá i18n (trích các nhóm chính — đầy đủ ở `i18n/vi.ts` 518 dòng / `en.ts` 436 dòng)

| Khoá | `vi` | `en` |
| :-- | :-- | :-- |
| `hoaDonBanHang:menu.hoaDonBanHang` | Hóa đơn bán hàng | Sales invoice |
| `hoaDonBanHang:list.col.ngayHoaDon` | Ngày hóa đơn | Invoice date |
| `hoaDonBanHang:list.col.soHoaDon` | Số hóa đơn | Invoice number |
| `hoaDonBanHang:status.lapChungTu.chuaLap` | Chưa lập | Not created |
| `hoaDonBanHang:status.phatHanh.chuaPhatHanh` | Chưa phát hành | Not issued |
| `hoaDonBanHang:themMoi.tabs.xemDuLieuGhiSo` | Xem dữ liệu ghi sổ | View posting data |
| `hoaDonBanHang:xoa.ketQua.col.lyDo` | Lý do lỗi | Error reason |
| `hoaDonBanHang:msg.'MSG_PMKT-E-06196_001'` | Thêm mới Hóa đơn thành công | *(en tương ứng)* |
| `hoaDonBanHang:msg.'MSG_PMKT-E-06196_006'` | Hóa đơn đã tồn tại ({{soHD}}-{{kyHieuHD}}-{{mauSoHD}}) | *(interpolation `{{}}` — BA viết `{}`, đổi cú pháp cho i18next)* |
| `hoaDonBanHang:msg.'MSG_PMKT-E-06196_054'` | Xóa thành công {{x}}/{{n}} hóa đơn. {{y}} hóa đơn đã phát hành không được xóa. | |
| `hoaDonBanHang:msg.'MSG_PMKT-E-06196_055'` | Hóa đơn này đã được lập chứng từ bán hàng/dịch vụ… | |
| `hoaDonBanHang:msg.'MSG_PMKT-E-06196_056'` | Hóa đơn này đã được lập chứng từ bán hàng/dịch vụ. Việc thay đổi mã khách hàng… | |

Toàn bộ 17 mã `MSG_PMKT-E-06196_*` của `6.messages.md` đều có mặt (12/08); cân bằng vi/en 313=313
khoá — không phát hiện khoá thiếu khi rà lại 20/08 (không có message mới trong 2 commit BA nêu).

## 4. Hằng số nghiệp vụ (`constants/constants.ts`, 257 dòng)

| Hằng số | Giá trị wire | Nguồn |
| :-- | :-- | :-- |
| `LOAI_NGHIEP_VU.trongNuoc/xuatKhau/banDichVu` | enum tên hằng | trục cột ma trận |
| `TRANG_THAI_LAP_CHUNG_TU.chuaLap/daLapMotPhan/daLapDu` | enum | BR02 |
| `TRANG_THAI_PHAT_HANH.chuaPhatHanh/daPhatHanh` | `'CHUA_PHAT_HANH'`/`'DA_PHAT_HANH'` | BR03, khớp `package-info.java:26-30` |
| `HDBH_CO_GHI_SO` | `false` | cờ phạm vi (D1) |
| `HDBH_DUNG_MOCK` (ở `api/hoaDonBanHangApi.ts`) | `false` | công tắc nợ kỹ thuật (§2) |

## 5. Mã quyền (`constants/permissions.ts`)

| Hằng số | Mã | Khớp BE |
| :-- | :-- | :-- |
| `HOA_DON_BAN_HANG_PERM.view` | `LapHoaDonBan.View` | `MA_CHUC_NANG` = `"LapHoaDonBan"` (`HoaDonBanHangController.java:39`) |
| `.viewDetail` | `LapHoaDonBan.View.Detail` | |
| `.create` | `LapHoaDonBan.Create` | |
| `.edit` | `LapHoaDonBan.Edit` | |
| `.delete` | `LapHoaDonBan.Delete` | |
| `LAP_CHUNG_TU_PERM.banHangHoa` | `BanHangHoa.Create` (mã của B4.1, dùng bởi `chungTuBanHang`) | |
| `LAP_CHUNG_TU_PERM.banDichVu` | `BanDichVu.Create` (B4.2 — chưa có module FE đích) | |

## 6. Đường dẫn (`constants/paths.ts`)

```ts
HOA_DON_BAN_HANG_PATHS.hoaDonBanHang  // '/ban-hang/hoa-don-ban-hang'
```

Re-export từ `@features/banHang/_shared/constants/banHangTabs.ts` — **nguồn DUY NHẤT** của path nhóm
Bán hàng (§7 `client/CLAUDE.md`). Ngoài module deep-import thẳng file này, không qua `index.ts`.
