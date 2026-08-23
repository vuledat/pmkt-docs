# Coding Convention — Frontend (`client`)

> Tách từ `conventions.md` (2026-08-23) để tác vụ FE và tác vụ Java không phải nạp phần của nhau.
> Nội dung giữ **nguyên văn**. Phần dùng chung cho cả hai: [`conventions-chung.md`](conventions-chung.md).

## 2. Coding Convention — Frontend (`client`)

Stack: React 19 · TypeScript (strict) · Vite · Ant Design · TanStack Query · i18next · Zod.

### 2.1 Quy ước đặt tên

| Đối tượng | Quy tắc | Ví dụ |
|---|---|---|
| File `.tsx` (component) | PascalCase | `UserProfile.tsx`, `ButtonPrimary.tsx` |
| File `.ts` (logic, hook, util) | camelCase | `formatDate.ts`, `useAuth.ts` |
| Thư mục | camelCase | `src/features/tienGui/`, `src/base/domainKit/` |
| Function, variable | camelCase | `const userData = …`, `function calculateTotal() {}` |
| Constant | SCREAMING_SNAKE_CASE | `const MAX_RETRY_COUNT = 3` |
| Component, Interface, Type, Enum | PascalCase | `interface UserProfileProps {}`, `enum UserRole {}` |
| Custom hook | camelCase, tiền tố `use` | `useFetchList.ts`, `useWindowSize.ts` |
| Prop sự kiện | `onXxx` | `<Button onClick={…} />`, `onSubmitForm` |
| Hàm xử lý sự kiện | `handleXxx` | `const handleClickSubmit = () => {}` |

```tsx
// ✅ Cặp prop/handler chuẩn
<Button onClick={handleClickSubmit} />
```

### 2.2 TypeScript — Type safety

- **KHÔNG ĐƯỢC dùng `any`** (kể cả `as any`, `any[]`, `Promise<any>`).
- Chưa biết kiểu → dùng `unknown` rồi thu hẹp (narrow) bằng type guard hoặc Zod.
- Dữ liệu từ API/`localStorage`/query param là **dữ liệu không tin cậy**: parse bằng Zod schema, không ép kiểu mù.
- **KHÔNG ĐƯỢC** dùng `@ts-ignore`. Trường hợp bất khả kháng dùng `@ts-expect-error` kèm comment lý do.

```ts
// ❌ SAI
const user = (await res.json()) as any

// ✅ ĐÚNG
const user = UserSchema.parse(await res.json())   // UserSchema: z.object({...})
```

### 2.3 i18n — Không hardcode text

Mọi chuỗi người dùng nhìn thấy (label, title, nút, thông báo lỗi, placeholder, tooltip, cột bảng)
**BẮT BUỘC** khai báo song ngữ trong `src/app/i18n/vi.ts` và `en.ts`.

**Key phân tầng theo module/feature:** `<module>.<màn hình>.<thành phần>`

```
auth.login.submitButton
common.label.cancel
tienGui.list.columnAmount
```

Chuỗi động **BẮT BUỘC** dùng interpolation, **KHÔNG ĐƯỢC** cộng chuỗi (cộng chuỗi sai trật tự từ ở ngôn ngữ khác):

```ts
// ❌ SAI
t('welcome') + ' ' + name

// ✅ ĐÚNG
t('welcome_user', { name })
```

Không cần i18n: log kỹ thuật, key nội bộ, mã lỗi backend.

### 2.4 Import & cấu trúc

**BẮT BUỘC dùng path alias**, KHÔNG ĐƯỢC dùng relative path vượt cấp (`../../..`).
Alias theo tầng của repo này:

| Alias | Tầng |
|---|---|
| `@core` / `@core/*` | tiện ích thuần, không phụ thuộc UI |
| `@base` / `@base/*` | thành phần dùng chung |
| `@domain-kit` / `@domain-kit/*` | khối nghiệp vụ dùng chung |
| `@platform` / `@platform/*` | hạ tầng: auth, http, query, tenant, rbac |
| `@features/*` | từng nghiệp vụ |
| `@app/*` | router, layout, provider, i18n |
| `@test/*` | tiện ích test |

```ts
// ❌ SAI
import { Button } from '../../../base/components/Button'

// ✅ ĐÚNG
import { Button } from '@base/components/Button'
```

**Luật tầng (tier boundary):** import chỉ được đi **xuống dưới**
(`app → features → platform → domain-kit → base → core`), không đi ngược, không đi ngang giữa hai `features`.
Luật này được ép bằng lint: `npm run lint:boundaries`.

**Export:** NÊN dùng **named export**; chỉ dùng `default` khi framework bắt buộc.

```ts
// ✅ export const UserCard = () => {}
// ❌ export default function UserCard() {}
```

### 2.5 Lệnh kiểm tra bắt buộc trước khi commit (`../../client`)

```bash
npm run typecheck        # không được có lỗi
npm run lint             # không được có error
npm run lint:boundaries  # luật tầng
npm run test             # test phải xanh
```

---
