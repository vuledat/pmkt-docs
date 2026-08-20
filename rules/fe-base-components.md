# FE — mục lục component `@base`

Tách khỏi `../../client/CLAUDE.md` §6 (2026-08-14). Bảng này mục nhanh — **nguồn sự thật vẫn là
barrel `../../client/src/base/index.ts`** và route `/__components` khi chạy dev.


**Luôn tìm trong `base/components` trước khi tự viết component.** Chỉ tự tạo khi thật sự không có, hoặc
cái có sẵn không đáp ứng được yêu cầu.

21 họ · **219 file `.tsx`** ở `base/components` · **290 dòng export** ở barrel `@base` (đo 2026-08-08;
số trong ngoặc dưới đây là số file `.tsx` của họ đó):

| Họ | Dùng cho |
|---|---|
| `table` (35) | `CommonListTable` · `ListTable` · `ReportTable` · `CommonEditableGrid` · `CommonTableSummaryRow` · `RowActionButtons` · `ColumnConfigDrawer` |
| `fields` (27) | `CommonTextBox` · `CommonNumberInput` · `CommonDateInput` · `CommonSelectBox` · `CommonCheckbox` · `CommonRadio` · `CommonSlider` |
| `modal` (24) | `CommonFormModal` · `CommonConfirmModal` · `CommonDetailModal` · `CommonModalShell` · `WizardSteps` · footer các loại |
| `navigation` (22) | `CommonMenu` · `CommonBreadcrumb` · `CommonSteps` · `TabMenu2Level` · `PageHeader` |
| `status` (16) | `CommonStatusTag` · `ListTag` · `BasicTag` · `CommonStatusSwitch` |
| `chart` (10) | `BarChartCard` · `LineChartCard` · `DonutChartCard` · `RankedBarChart` |
| `filter` (9) · `layout` (9) | `CommonFilterPanel` · `CommonComboGrid` · các khối bố cục trang |
| `dropdown` (8) | `CommonDropdownBasic` · `CommonDropdownButtonBasic` · `UiSplitButton` |
| `feedback` (7) · `entry` (7) · `motion` (7) · `picker` (7) | `CommonAlert` · `UiToast` · `UiSpin` · `UiPopconfirm` · `CommonTreeSelect` |
| `button` (6) · `dataDisplay` (6) · `typography` (6) · `upload` (4) · `dataEntry` (3) · `display` (3) · `hub` (2) · `placeHolder` (1) | `CommonButton` · `DragDropUpload` · `CommonText` … |

Cách tra: mở barrel `src/base/index.ts`, hoặc chạy dev rồi vào `/__components` (bàn thử toàn bộ
`base/components`) và `/__design-system`.

Nếu component có sẵn thiếu một prop nhỏ → **thêm prop vào component ở `base`**, đừng copy ra feature. Chỉ
dựng component riêng trong `<module>/components/` khi nó mang **logic nghiệp vụ của riêng màn đó** —
component thuần trình bày mà dùng được ≥2 màn thì thuộc về `base`.
