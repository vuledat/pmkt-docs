# Truy vết luật nghiệp vụ vào code — quy ước bắt buộc

> Vì sao có file này: spec `PMKT-E-06194` có **112 luật `R-CTBH-xxx`**, code có **0** lần nhắc tới
> chúng. Bảng truy vết mà `CLAUDE.md` bắt buộc khi báo hoàn thành vì thế chỉ viết được bằng trí nhớ
> của phiên làm việc — không ai kiểm chứng được, luật rơi không ai phát hiện.
> Quy ước dưới đây biến "đã đủ nghiệp vụ chưa" từ **cảm tính** thành **một lệnh grep**.

## 1. Luật gốc

**Mỗi luật `R-…` trong `02-rules.md` phải để lại chính mã luật đó trong code.**
Không tìm thấy mã luật ⇒ `/verify-spec` chấm **CHƯA HIỆN THỰC**, kể cả khi code nhìn có vẻ đúng.

Kiểm bằng:

```bash
./docs/rules/trace.sh docs/doing/<slug>-spec fe      # hoặc be, hoặc bỏ trống = cả hai
./docs/rules/trace.sh docs/doing/<slug>-spec be --missing   # chỉ in dòng chưa đạt
```

## 2. Gắn mã ở đâu — đúng **hai** chỗ cho mỗi luật

| Chỗ | Bắt buộc | Ghi chú |
|---|---|---|
| **Nơi hiện thực chính** | ✅ | đúng hàm/nhánh quyết định hành vi, không phải file barrel/type |
| **Test hồi quy** | ✅ với luật `P0`; nên có với `P1` | test phải **đỏ** khi luật bị phá |

Không rải mã luật khắp nơi. Một luật gắn 1–2 điểm là đủ; gắn tràn lan làm `trace.sh` mất tác dụng
phân biệt "nơi hiện thực" với "nơi đi ngang qua".

## 3. Cú pháp

### Frontend (`client/`)

```ts
// helpers/chietKhau.ts
/** R-CTBH-045 — Dòng CKTM mang Thành tiền âm (nguồn: ThemMoi BR09.b). */
export function tinhThanhTienCKTM(dong: DongChiTiet): number { … }
```

Trong test — **đưa mã luật vào tên test**, để log CI đọc được:

```ts
describe('R-CTBH-045 · dòng CKTM mang Thành tiền âm', () => {
  it('nhập 100.000 ở dòng CKTM → Thành tiền = -100.000', () => { … })
})
```

Với luật chỉ thể hiện qua cấu hình (cột, field, permission), gắn ở đúng dòng cấu hình:

```ts
// fields/columns.ts
{ key: 'chiNhanh', title: t('cot.chiNhanh') },   // R-CTBH-013
```

### Backend (`cell-app`)

```java
/** R-CTBH-030 — Sinh số chứng từ theo Cấu hình đánh số (nguồn: ThemMoi BR25). */
private String sinhSoChungTu(…) { … }
```

Test JUnit:

```java
@Test
@Tag("unit")
@DisplayName("R-CTBH-030 · sinh số chứng từ theo cấu hình đánh số")
void R_CTBH_030_sinhSoChungTu_theoCauHinh() { … }
```

### Bất biến `INV-…`

Gắn ở nơi **cưỡng chế** bất biến (validator, constraint, service guard), không phải nơi gọi:

```java
/** INV-007 — tổng tiền chứng từ luôn = tổng dòng chi tiết sau chiết khấu. */
```

## 4. Luật `CHỜ` — cấm để lại mã trong code

Luật có trạng thái `CHỜ C<nn>` trong `02-rules.md` đang bị một mục P0/P1 `OPEN` của
`01-conflict.md` chặn. Code chạm vào luật đó ⇒ `trace.sh` in **`VI-PHAM`** và trả exit code ≠ 0.
Đúng quy trình là **để trống, ghi vào `IMPLEMENT.md` mục nợ**, chờ BA chốt.

## 5. Trạng thái `trace.sh` in ra

| Trạng thái | Nghĩa | Được báo "xong" không |
|---|---|---|
| `OK` | có trong code **và** có trong test | ✅ |
| `NO-TEST` | có code, thiếu test hồi quy | ❌ với P0 · ⚠ với P1/P2 (ghi nợ) |
| `MISSING` | không thấy mã luật ở đâu | ❌ |
| `BLOCKED` | luật đang `CHỜ`, đúng ra chưa code | ✅ (nếu đã liệt kê trong báo cáo) |
| `VI-PHAM` | đã code luật đang bị chặn | ❌ — phải gỡ hoặc xin BA chốt |

## 6. Thông báo — khoá theo mã `MSG_…`, đối chiếu bằng `msg.sh`

Mã thông báo trong `6.messages.md` là **khoá**, không phải chú thích:

- **FE**: key i18n **chính là mã** — `'MSG_PMKT-E-06194_043': '% Chiết khấu không được vượt quá 100%'`
  trong `vi.ts`, bản dịch tương ứng trong `en.ts`.
- **BE**: hằng số trong `internal/constant/MaLoi<Module>.java` —
  `public static final String MSG_CK_VUOT_100 = "MSG_PMKT-E-06194_043";`

Nội dung `vi.ts` phải **trùng từng chữ** với cột *Nội dung message* của tài liệu (`en.ts` là bản
dịch, không phải nguồn sự thật — script chỉ so nguyên văn với `vi.ts`).

```bash
./docs/rules/msg.sh <thư-mục-PYC>            # ví dụ pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang
./docs/rules/msg.sh <thư-mục-PYC> fe --missing
```

| Trạng thái | Nghĩa |
|---|---|
| `OK` | mã có trong code, nội dung khớp nguyên văn |
| `LECH` | mã có nhưng chữ khác tài liệu → **sửa code theo tài liệu** |
| `THIEU-VI` | có key ở `en.ts` mà thiếu ở `vi.ts` (vi phạm luật 2) |
| `CHUA-DAT` | mã chỉ nằm trong comment, chưa thành giá trị/hằng số |
| `THIEU` | mã chưa xuất hiện ở đâu |

## 7. Code đã có từ trước quy ước này

Module đã hoàn thành trước 2026-08-30 chưa gắn mã luật (ví dụ `banHang/chungTuBanHang` — 112 luật,
0 mã). **Không** mở đợt gắn ngược hàng loạt. Quy tắc như code cũ vi phạm convention:
gắn mã **trong đúng phạm vi đang sửa**, mỗi lần chạm vào một luật thì gắn luật đó. Muốn đóng nợ
toàn module thì mở ticket riêng.
