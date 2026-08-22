# PMKT FE Class Naming Rule

## 1. Mục đích

Quy định cách FE sinh `class` cho các phần tử HTML theo **cấp độ semantic của màn hình và nghiệp vụ**, nhằm:

- Xác định được phần tử đang thuộc màn hình/nghiệp vụ nào.
- Có thể định vị phần tử theo cấu trúc semantic từ ngoài vào trong.
- Giữ class ổn định khi thay đổi layout, CSS framework hoặc UI component.
- Hỗ trợ automation test, debug DOM và truy vết phần tử.
- Phân biệt rõ `class` semantic với các class phục vụ styling của UI framework.

`class` semantic trong quy tắc này là **metadata định danh**, không phải class dùng để mô tả CSS presentation.

---

## 2. Nguyên tắc tổng quát

FE MUST sinh class semantic theo cấu trúc phân cấp:

```text
<domain>
  └── <screen>
        └── <surface/action>
              └── <field/item>
```

Ví dụ:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    <div class="create">
      <input class="so-chung-tu">
    </div>
  </div>
</div>
```

Trong đó:

| Cấp | Ý nghĩa | Ví dụ |
|---|---|---|
| 1 | Domain/nghiệp vụ | `ban-hang` |
| 2 | Màn hình/chức năng | `chung-tu-ban-hang` |
| 3 | Surface hoặc action | `create` |
| 4 | Field/item | `so-chung-tu` |

---

## 3. Quy tắc đặt tên

### 3.1. Domain

Class cấp domain xác định module/nghiệp vụ sở hữu màn hình.

Ví dụ:

```html
<div class="ban-hang">
```

```text
ban-hang
mua-hang
ke-toan
kho
cong-no
```

Tên domain MUST:

- viết lowercase;
- sử dụng kebab-case;
- thể hiện semantic nghiệp vụ;
- không phụ thuộc vào tên component kỹ thuật;
- không sử dụng tên thư viện UI.

---

### 3.2. Screen

Class cấp screen xác định màn hình/chức năng nghiệp vụ.

Ví dụ:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
```

`chung-tu-ban-hang` là semantic của màn hình, không phải tên React/Vue component.

Không đặt theo:

```text
Page
FormPage
InvoicePage
AntForm
Drawer
Modal
```

---

### 3.3. Surface / action

Class cấp tiếp theo xác định bề mặt hoặc thao tác chính.

Ví dụ:

```html
<div class="create">
```

Các action chuẩn:

```text
create
view
edit
delete
save
cancel
close
confirm
apply
search
filter
sort
clear
reset
reload
add-line
remove-line
open-picker
select
deselect
import
export
upload
download
print
post
unpost
lock
unlock
next
previous
expand
collapse
retry
```

Nếu một action đã có trong Controlled Vocabulary thì MUST sử dụng đúng canonical term.

Ví dụ:

```text
create   OK
add      KHÔNG dùng thay cho create

delete   OK
remove   KHÔNG dùng thay cho delete

reload   OK
refresh  KHÔNG dùng thay cho reload
```

---

## 4. Field / item

Class cấp field xác định trường dữ liệu hoặc item nghiệp vụ.

Ví dụ:

```html
<input class="so-chung-tu">
```

Tên field MUST lấy từ semantic nghiệp vụ:

```text
so-chung-tu
ngay-hach-toan
khach-hang
ma-hang
chi-tiet-hang-hoa
phan-bo-chiet-khau
```

Không đặt theo:

```text
input-1
input-2
field-1
ant-input
form-control
left-input
red-input
```

---

## 5. Quy tắc class theo DOM hierarchy

Class phải thể hiện được quan hệ semantic từ ngoài vào trong.

Ví dụ màn hình:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    <div class="create">
      <input class="so-chung-tu">
      <input class="ngay-hach-toan">

      <div class="chi-tiet-hang-hoa">
        <div class="row">
          <input class="ma-hang">
          <input class="so-luong">
        </div>
      </div>
    </div>
  </div>
</div>
```

Quan hệ semantic:

```text
ban-hang
└── chung-tu-ban-hang
    └── create
        ├── so-chung-tu
        ├── ngay-hach-toan
        └── chi-tiet-hang-hoa
            └── row
                ├── ma-hang
                └── so-luong
```

---

## 6. Class của element không bắt buộc chứa toàn bộ path

Class của một element chỉ chứa **semantic cấp của chính element đó**.

Ví dụ:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    <div class="create">
      <input class="so-chung-tu">
    </div>
  </div>
</div>
```

KHÔNG bắt buộc phải sinh:

```html
<input class="ban-hang-chung-tu-ban-hang-create-so-chung-tu">
```

Path đầy đủ được biểu diễn thông qua DOM hierarchy.

Điều này giúp:

- class ngắn;
- dễ đọc;
- giảm trùng lặp;
- vẫn truy được semantic bằng ancestor scope.

---

## 7. Element có nhiều semantic

Một element có thể mang nhiều class nếu nó đồng thời có nhiều vai trò.

Ví dụ:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    <div class="create">
      <button class="save action">
        Lưu
      </button>
    </div>
  </div>
</div>
```

Tuy nhiên, không được thêm class chỉ để phục vụ CSS nếu class đó được quy định là semantic locator.

---

## 8. Row và phần tử lặp

Với phần tử lặp, class xác định **loại phần tử**, không dùng index để tạo class.

Ví dụ:

```html
<div class="chi-tiet-hang-hoa">
  <div class="row">
    <input class="ma-hang">
    <input class="so-luong">
  </div>

  <div class="row">
    <input class="ma-hang">
    <input class="so-luong">
  </div>
</div>
```

KHÔNG sinh:

```html
<div class="row-1">
<div class="row-2">
```

hoặc:

```html
<input class="ma-hang-1">
<input class="ma-hang-2">
```

Instance cụ thể của phần tử lặp phải được xác định bằng cơ chế key riêng, không bằng index hoặc STT.

---

## 9. Portal / Popup / Picker

Nếu component được render qua portal và không còn nằm trực tiếp trong DOM hierarchy của owner, phải duy trì semantic liên kết với owner bằng metadata riêng.

Ví dụ:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    <div class="create">
      <div class="ma-hang">
        ...
      </div>
    </div>
  </div>
</div>

<div class="picker" data-pmkt-owner-key="row-a8f2">
  ...
</div>
```

Không cố gắng tạo class giả để mô phỏng DOM hierarchy không tồn tại.

---

## 10. Không dùng class kỹ thuật làm semantic locator

Các class sau không được xem là class semantic ổn định:

```text
ant-input
ant-btn
ant-form-item
MuiButton
MuiInput
form-control
flex
grid
w-full
mt-2
css-xxxxx
sc-xxxxx
```

Các class generated bởi framework/build tool cũng không được sử dụng làm locator ổn định.

Ví dụ:

```html
<input
  class="ant-input css-1abcxyz so-chung-tu"
/>
```

Trong đó:

```text
ant-input       → UI framework
css-1abcxyz     → generated CSS
so-chung-tu     → semantic class
```

---

## 11. Quy tắc cho component dùng chung

Shared component không được tự ý quyết định business semantic.

Feature sở hữu business semantic phải truyền context xuống component.

Ví dụ:

```jsx
<ChungTuBanHang>
  <DatePicker />
</ChungTuBanHang>
```

Feature quyết định:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    ...
  </div>
</div>
```

Shared component chỉ được nối thêm semantic suffix đã được chuẩn hóa khi cần:

```text
picker
option
action.clear
error
```

Không để shared component tự sinh class kiểu:

```text
common-component-1
shared-input
component-xyz
```

---

## 12. Độ ổn định

Semantic class MUST giữ nguyên khi chỉ thay đổi:

- layout;
- CSS;
- Modal ↔ Drawer ↔ inline;
- UI component library;
- cách render nội bộ;
- cấu trúc kỹ thuật của component;

miễn là **ý nghĩa nghiệp vụ không thay đổi**.

Ví dụ:

Trước:

```html
<div class="chung-tu-ban-hang">
  <div class="create">
    <input class="so-chung-tu">
  </div>
</div>
```

Sau khi đổi từ Modal sang Drawer:

```html
<div class="chung-tu-ban-hang">
  <div class="create">
    <input class="so-chung-tu">
  </div>
</div>
```

Semantic class không thay đổi.

---

## 13. Không dùng các yếu tố sau để đặt semantic class

Không được đặt class dựa trên:

- text hiển thị;
- vị trí;
- màu sắc;
- kích thước;
- CSS;
- tên component kỹ thuật;
- tên thư viện UI;
- DOM generated selector;
- index;
- STT;
- Figma node ID/layer name.

Ví dụ không hợp lệ:

```text
left-panel
red-button
input-1
row-3
ant-input
modal-content
css-abc123
```

---

## 14. Quy tắc mẫu chuẩn

### Màn hình tạo chứng từ

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    <div class="create">

      <input class="so-chung-tu">

      <input class="ngay-hach-toan">

      <div class="khach-hang">
        ...
      </div>

      <div class="chi-tiet-hang-hoa">
        <div class="row">
          <input class="ma-hang">
          <input class="so-luong">
          <button class="delete">
            Xóa
          </button>
        </div>
      </div>

      <button class="save">
        Lưu
      </button>

      <button class="cancel">
        Hủy
      </button>

    </div>
  </div>
</div>
```

Semantic tree:

```text
ban-hang
└── chung-tu-ban-hang
    └── create
        ├── so-chung-tu
        ├── ngay-hach-toan
        ├── khach-hang
        ├── chi-tiet-hang-hoa
        │   └── row
        │       ├── ma-hang
        │       ├── so-luong
        │       └── delete
        ├── save
        └── cancel
```

---

## 15. Acceptance Criteria

FE implementation được coi là đạt khi:

1. Các màn hình nghiệp vụ có semantic class theo hierarchy.
2. Class domain và screen được xác định bởi feature sở hữu.
3. Field/action dùng tên semantic nghiệp vụ.
4. Không sử dụng index/STT để tạo semantic class.
5. Không sử dụng class của UI framework làm semantic locator.
6. Không sử dụng generated CSS class làm semantic locator.
7. Semantic class không thay đổi khi thay đổi layout hoặc UI library nếu business semantic không đổi.
8. Shared component không tự quyết định business semantic.
9. DOM thực tế phản ánh được hierarchy semantic của màn hình.

---

## 16. Ví dụ cuối cùng

Input source:

```text
Domain: ban-hang
Screen: chung-tu-ban-hang
Mode: create
Field: so-chung-tu
```

FE phải sinh được DOM tương ứng:

```html
<div class="ban-hang">
  <div class="chung-tu-ban-hang">
    <div class="create">
      <input class="so-chung-tu">
    </div>
  </div>
</div>
```

**Nguyên tắc cốt lõi:**

```text
DOM hierarchy = business semantic hierarchy

class = semantic của node hiện tại
```
</content>
