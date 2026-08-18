#!/usr/bin/env python3
"""Sinh đặc tả bảng DB từ ba/Common/LDM_update/*.puml.

Nguồn duy nhất = file .puml. Không gõ tay field nào.
"""
import re, os, sys, json, collections

ROOT = "/Users/macbook/Documents/VTT/Code/osp/vtt-osp"
LDM = f"{ROOT}/pmkt-docs/ba/Common/LDM_update"
MIG = f"{ROOT}/cell-app/src/main/resources/db/migration"
OUT = f"{ROOT}/docs/doing/db-spec"

# ---------------------------------------------------------------- snake_case
def snake(n):
    n = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', n)
    n = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', n)
    n = re.sub(r'([a-zA-Z])([0-9])', r'\1_\2', n)
    n = re.sub(r'_+', '_', n)
    return n.lower().strip('_')

# ---------------------------------------------------------------- parse puml
FIELD_RE = re.compile(
    r'^\s*(?P<pk>\*)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*'
    r'(?P<type>[A-Za-z]+)(?P<req>!)?\s*(?P<tags>(?:<<[^>]*>>\s*)*)'
    r'(?:-\s*(?P<desc>.*))?$')
# biến thể "Name        type" (khối tham khảo trong ldm-Authentication)
FIELD_RE2 = re.compile(r'^\s{2,}(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s{2,}'
                       r'(?P<type>uuid|string|numeric|date|datetime|boolean|enum|text|json)\s*$')

def parse_puml(path):
    ents, cur, sect = [], None, None
    # comment gom theo KHỐI (ngăn nhau bởi dòng trống):
    #   doc của entity = khối cuối cùng đứng trước nó
    #   header file    = các khối còn lại trước entity đầu tiên
    curblock, blocks, header, seen_entity = [], [], [], False
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        s = line.strip()
        m = re.match(r'^entity\s+([A-Za-z0-9_]+)\s*\{?\s*$', s)
        if m:
            if curblock:
                blocks.append(curblock); curblock = []
            usable = [b for b in blocks
                      if b and not re.match(r'^(NOTE|Note|Ghi chú)\b', b[0])]
            doc = usable[-1] if usable else []
            if not seen_entity:
                header.extend([x for b in blocks[:-1] for x in b])
            cur = {'name': m.group(1), 'fields': [], 'note': [], 'doc': doc[-4:]}
            ents.append(cur); sect = None; blocks = []; seen_entity = True; continue
        if cur is None and s.startswith("'"):
            c = s.strip("' ").strip('-=#').strip()
            if c and not set(c) <= set('-=# '):
                curblock.append(re.sub(r'^Entity\s*:\s*', '', c))
            continue
        if cur is None and not s:
            if curblock:
                blocks.append(curblock); curblock = []
            continue
        if cur is None:
            continue
        if s == '}':
            cur = None; sect = None; continue
        if s.startswith("'"):
            c = s.lstrip("' ").strip('-').strip()
            if c and cur is not None:
                sect = c
            continue
        if not s or s == '{':
            continue
        m = FIELD_RE.match(line)
        if m:
            cur['fields'].append({
                'name': m.group('name'),
                'type': m.group('type'),
                'pk': bool(m.group('pk')),
                'req': bool(m.group('req')),
                'tags': re.findall(r'<<([^>]*)>>', m.group('tags') or ''),
                'desc': (m.group('desc') or '').strip(),
                'sect': sect})
            sect = None if False else sect
            continue
        m = FIELD_RE2.match(line)
        if m:
            cur['fields'].append({
                'name': m.group('name'), 'type': m.group('type'), 'pk': False,
                'req': False, 'tags': [], 'desc': '', 'sect': sect})
    return ents, [h for h in header if h]

# ---------------------------------------------------------------- kiểu dữ liệu
MONEY_TOK = ('dongia', 'thanhtien', 'tientue', 'tienthue', 'tongtien', 'sotien',
             'giatri', 'psno', 'psco', 'chiphi', 'thue', 'tien', 'tong', 'no', 'co',
             'doanhthu', 'giavon', 'sodathu', 'sodachi', 'thucthu', 'luyke', 'sodu',
             'khauhao', 'phanbo', 'nguyengia', 'dutoan', 'conlai')
INT_TOK = ('stt', 'thutu', 'sochuso', 'songay', 'sothang', 'sonam', 'nam', 'thang',
           'ky', 'solan', 'sodem', 'bodem', 'phienban', 'port', 'soluongdong')

def map_type(f, ent):
    n, t = f['name'], f['type'].lower()
    ln = n.lower()
    if t == 'uuid':   return 'uuid', ''
    if t == 'date':   return 'date', ''
    if t == 'datetime': return 'timestamptz', ''
    if t == 'boolean': return 'boolean', ''
    if t == 'enum':   return 'text', 'CHECK'
    if t in ('json',): return 'jsonb', ''
    if t in ('string', 'text'):
        if ln in ('sochungtu', 'ma', 'code', 'sohoadon', 'sodonhang', 'sohopdong',
                  'masothue', 'solo', 'sohieu', 'maquyen', 'mavatu'):
            return 'varchar(50)', 'BR20'
        return 'text', ''
    if t == 'numeric':
        if 'tygia' in ln:                       return 'exchange_rate', ''
        if 'hesoquydoi' in ln or ln == 'heso':  return 'exchange_rate', '≈'
        if ln.startswith('soluong') or 'soluong' in ln: return 'quantity', ''
        if any(k in ln for k in ('tyle', 'phantram', 'thuesuat', 'tysuat')): return 'percent_rate', ''
        if any(ln.startswith(k) or ln == k for k in INT_TOK): return 'integer', ''
        if ln.endswith('quydoi'):               return 'money_vnd', ''
        if any(k in ln for k in MONEY_TOK):     return 'money_foreign', '≈'
        return 'numeric(18,4)', '⚠'
    return t, '⚠'

def default_of(f, dbtype):
    if f['pk']: return '`gen_random_uuid()`'
    if dbtype == 'exchange_rate' and 'tygia' in f['name'].lower(): return '`1`'
    if dbtype == 'boolean': return '`false`'
    if dbtype in ('money_vnd', 'money_foreign', 'quantity', 'exchange_rate',
                  'percent_rate', 'integer') or dbtype.startswith('numeric'):
        return '`0`'
    return '—'

# ---------------------------------------------------------------- bảng hiện có
def load_db_columns():
    cols = collections.defaultdict(list)
    for fn in sorted(os.listdir(MIG)):
        if not fn.endswith('.sql'): continue
        txt = open(os.path.join(MIG, fn), encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'create\s+table\s+(?:if\s+not\s+exists\s+)?(?:public\.)?'
                             r'([a-z0-9_]+)\s*\((.*?)\n\s*\)\s*(?:partition|;)',
                             txt, re.I | re.S):
            tbl, body = m.group(1), m.group(2)
            for ln in body.split('\n'):
                ln = ln.split('--')[0].strip().rstrip(',')
                cm = re.match(r'^([a-z0-9_]+)\s+([a-z0-9_.()," ]+)', ln, re.I)
                if not cm: continue
                c = cm.group(1).lower()
                if c in ('primary', 'constraint', 'unique', 'foreign', 'check', 'like', 'partition'):
                    continue
                if c not in [x[0] for x in cols[tbl]]:
                    cols[tbl].append((c, cm.group(2).strip().split(' NOT')[0].strip()))
        for m in re.finditer(r'alter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?(?:public\.)?'
                             r'([a-z0-9_]+)\s+add\s+column\s+(?:if\s+not\s+exists\s+)?'
                             r'([a-z0-9_]+)\s+([a-z0-9_.()," ]+)', txt, re.I):
            tbl, c, ty = m.group(1), m.group(2).lower(), m.group(3).strip()
            if c not in [x[0] for x in cols[tbl]]:
                cols[tbl].append((c, ty.split(' NOT')[0].strip()))
    dropped = set()
    for fn in os.listdir(MIG):
        txt = open(os.path.join(MIG, fn), encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'drop\s+table\s+(?:if\s+exists\s+)?(?:public\.)?([a-z0-9_]+)', txt, re.I):
            dropped.add(m.group(1).lower())
    return cols, dropped

# ---------------------------------------------------------------- cấu hình module
MODULE = {
 'ldm-SoKeToan-Update':      ('acc',  'Sổ kế toán (sổ cái · sổ kho)', '10'),
 'ldm-HeThong':              ('iam',  'Hệ thống · Tenant · Vai trò',  '11'),
 'ldm-Authentication':       ('iam',  'Xác thực · Người dùng',        '12'),
 'ldm-ProfileManagement':    ('iam',  'Hồ sơ người dùng trong tenant','13'),
 'ldm-KhoaSo-Update':        ('cfg',  'Khóa sổ kế toán',              '14'),
 'ldm-Kho-Update':           ('inv',  'Kho',                          '20'),
 'ldm-MuaHang-Update':       ('pur',  'Mua hàng',                     '30'),
 'ldm-TraLaiHangMua':        ('pur',  'Trả lại hàng mua',             '31'),
 'ldm-DieuChinhGiaHangMua':  ('pur',  'Điều chỉnh giá hàng mua',      '32'),
 'ldm-DoiTruCongNo-Update':  ('pur',  'Đối trừ công nợ',              '33'),
 'ldm-BanHang-Update':       ('sal',  'Bán hàng',                     '40'),
 'ldm-TraLaiHangBan':        ('sal',  'Trả lại hàng bán',             '41'),
 'ldm-DieuChinhGiaHangBan':  ('sal',  'Điều chỉnh giá hàng bán',      '42'),
 'ldm-NganQuy-Update':       ('cb',   'Ngân quỹ (tiền mặt · tiền gửi)','50'),
 'ldm-TaiSanCoDinh-Update':  ('fa',   'Tài sản cố định',              '60'),
 'ldm-CCDC':                 ('ccdc', 'Công cụ dụng cụ',              '61'),
 'ldm-ChiPhiTraTruoc-Update':('cptt', 'Chi phí trả trước',            '62'),
 'ldm-GiaThanh':             ('cst',  'Giá thành',                    '70'),
 'ldm-PhieuKTTH':            ('ktth', 'Phiếu kế toán tổng hợp',       '80'),
 'ldm-KetChuyenLaiLo':       ('ktth', 'Kết chuyển lãi lỗ',            '81'),
 'ldm-DanhGiaLaiNgoaiTe':    ('fx',   'Đánh giá lại ngoại tệ',        '82'),
 'ldm-SoDuBanDau':           ('sdbd', 'Số dư ban đầu',                '83'),
 'ldm-Thue-Update':          ('tax',  'Thuế',                         '85'),
 'ldm-BaoCaoTaiChinh':       ('rpt',  'Báo cáo tài chính',            '86'),
}

# tên bảng chốt tay (khác snake(entity) mặc định)
TABLE_OVERRIDE = {
 'SoCai': 'acc_so_cai', 'SoKho': 'acc_so_kho',
 'Tenant': 'iam_tenant', 'Tenant_LinhVucHoatDong': 'iam_tenant_linh_vuc_hoat_dong',
 'VaiTro': 'iam_vai_tro', 'VaiTroQuyen': 'iam_vai_tro_quyen',
 'NguoiDungVaiTro': 'iam_tai_khoan_vai_tro', 'NguoiDung': 'iam_tai_khoan',
 'NguoiDung_Tenant': 'iam_tai_khoan_tenant', 'CauHinhEmail': 'cfg_cau_hinh_email',
 'ThietLapKhoaSo': 'cfg_thiet_lap_khoa_so',
 'ChiTietThietLapKhoaSoChungTu': 'cfg_thiet_lap_khoa_so_chung_tu',
 'ChiTietThietLapKhoaSoNguoiDung': 'cfg_thiet_lap_khoa_so_nguoi_dung',
 'ChungTuBan': 'sal_chung_tu_ban_hang',
 'ChiTietChungTuBan': 'sal_chung_tu_ban_hang_chi_tiet',
 'HoaDonBan': 'sal_hoa_don_ban_hang', 'ChiTietHoaDonBan': 'sal_hoa_don_ban_hang_chi_tiet',
 'ChungTuMuaHang': 'pur_chung_tu_mua_hang',
 'ChiTietChungTuMuaHang': 'pur_chung_tu_mua_hang_chi_tiet',
 'HoaDonMua': 'pur_hoa_don_mua', 'ChiTietHoaDon': 'pur_hoa_don_mua_chi_tiet',
 'PhieuNhapKho': 'inv_phieu_nhap_kho', 'ChiTietPhieuNhapKho': 'inv_phieu_nhap_kho_chi_tiet',
 'PhieuXuatKho': 'inv_phieu_xuat_kho', 'ChiTietPhieuXuatKho': 'inv_phieu_xuat_kho_chi_tiet',
 'TonKho': 'inv_ton_kho', 'CostLayer': 'inv_lop_gia_von',
 # chốt tay: luật hậu tố cho ra tên lặp/sai cha
 'ChiTietApGiaXuatKho': 'inv_ket_qua_tinh_gia_xuat_kho_chi_tiet',
 'NguoiKiemKeCCDC': 'ccdc_phieu_kiem_ke_nguoi_kiem_ke',
 'LichSuDieuChuyenTaiSan': 'fa_tai_san_co_dinh_lich_su_dieu_chuyen',
 'PhuLuc01_6GTGT': 'tax_phu_luc_01_6_gtgt',
 'PhuLuc01_6GTGT_TheoTinh': 'tax_phu_luc_01_6_gtgt_theo_tinh',
 'PhuLuc01_6GTGT_ChiTiet': 'tax_phu_luc_01_6_gtgt_chi_tiet',
 'ChiTietTonKhoSnapShot': 'inv_phieu_kiem_ke_kho_ton_kho_snapshot',
 'HeSoPhanBoCongCuDungCu': 'ccdc_he_so_phan_bo',
}

# bảng đang có JPA entity
def coded_tables():
    import subprocess
    out = subprocess.run(
        ['grep', '-rhoE', r'@Table\([^)]*name[[:space:]]*=[[:space:]]*"[a-z0-9_]+"',
         '--include=*.java', f'{ROOT}/cell-app/src/main/java'],
        capture_output=True, text=True).stdout
    return set(re.findall(r'"([a-z0-9_]+)"', out))


# ---------------------------------------------------------------- mục đích bảng
VAI_TRO = {
 'chungtu': ('Đầu chứng từ (header)',
   'Người dùng lập trực tiếp trên màn hình nghiệp vụ. Khi **ghi sổ**, chứng từ này là nguồn '
   'sinh bút toán vào `acc_so_cai` (và dòng biến động vào `acc_so_kho` nếu có dòng vật tư). '
   'Bị khóa sửa/xóa sau khi ghi sổ cho tới khi bỏ ghi sổ (BR12 · BR42).'),
 'chitiet': ('Dòng chi tiết',
   'Tồn tại phụ thuộc chứng từ cha — xóa cha thì xóa con (`ON DELETE CASCADE`). '
   'Mỗi dòng là một đơn vị hạch toán: một dòng sinh ra một hoặc nhiều bút toán sổ cái '
   '(giá vốn · doanh thu · thuế…), phân biệt bằng `stt_but_toan`.'),
 'so': ('Sổ kế toán — append-only',
   'KHÔNG do người dùng nhập. Chỉ kernel ghi sổ được ghi vào, và chỉ khi chứng từ chuyển sang '
   '`DA_GHI_SO`. Bảng bất biến (`@Immutable`) + partition theo `ngay_hach_toan`. '
   'Là **nguồn duy nhất** cho mọi sổ sách, báo cáo và tra cứu số dư.'),
 'thuong': ('Bảng nghiệp vụ', ''),
}
CFG_TOK = ('ThietLap', 'CauHinh', 'DangKy', 'QuyTac', 'DinhMuc', 'KhaiBao')
KQ_TOK  = ('KetQua', 'TonKho', 'LichSu', 'CostLayer', 'GiaThanh', 'LuotTinh', 'SnapShot',
           'PhanBoChungTu', 'DoDang', 'KeHoach')

def vai_tro_of(ent, kind):
    """(vai trò, giải thích) — dùng chung cho mục lục và khối mô tả chi tiết."""
    n = ent['name']
    role, giai_thich = VAI_TRO[kind]
    if kind == 'thuong':
        if any(t in n for t in CFG_TOK):
            role = 'Bảng cấu hình / thiết lập'
            giai_thich = ('Dữ liệu do người dùng khai báo một lần rồi dùng lại; không phát sinh bút toán. '
                          'Nghiệp vụ đọc bảng này để lấy tham số khi lập và khi ghi sổ chứng từ.')
        elif any(t in n for t in KQ_TOK):
            role = 'Bảng kết quả / số dư luân chuyển'
            giai_thich = ('Không do người dùng nhập — hệ thống tính và cập nhật tại chỗ sau mỗi lần ghi sổ '
                          'hoặc mỗi lần chạy tính toán theo kỳ. Dùng cho tra cứu nhanh, không thay thế sổ gốc.')
        elif '_' in n or (len([f for f in ent['fields'] if f['name'].endswith('Id')]) >= 2
                          and len(ent['fields']) <= 5):
            role = 'Bảng liên kết N–N'
            giai_thich = 'Chỉ mang cặp khóa ngoại; cần UNIQUE trên cặp khóa để chống trùng.'
        else:
            giai_thich = 'Bảng dữ liệu nghiệp vụ của phân hệ.'
    return role, giai_thich


ROLE_NGAN = {
 'Đầu chứng từ (header)': 'Đầu chứng từ',
 'Dòng chi tiết': 'Dòng chi tiết',
 'Sổ kế toán — append-only': 'Sổ kế toán (append-only)',
 'Bảng cấu hình / thiết lập': 'Cấu hình / thiết lập',
 'Bảng kết quả / số dư luân chuyển': 'Kết quả / số dư luân chuyển',
 'Bảng liên kết N–N': 'Liên kết N–N',
 'Bảng nghiệp vụ': 'Bảng nghiệp vụ',
}

def chuc_nang(ent, kind, doc, parent_tbl):
    """Một câu cho cột Chức năng ở mục lục."""
    role, _ = vai_tro_of(ent, kind)
    short = ROLE_NGAN.get(role, role)
    if kind == 'chitiet' and parent_tbl:
        short = f'Dòng chi tiết của `{parent_tbl}`'
    # gộp cả khối comment thành một đoạn (LDM hay xuống dòng giữa câu)
    para = re.sub(r'\s+', ' ', ' '.join(d.strip() for d in doc)).strip()
    banner = re.match(r'^(?:KHỐI|PHẦN|BLOCK)\s*[0-9A-Z]*\s*[—\-:]\s*(.+)$', para)
    if banner:
        rest = banner.group(1).strip()
        # banner chỉ là tiêu đề mục (không có phần mô tả trong ngoặc/sau dấu hai chấm)
        if len(rest) < 40 and '(' not in rest:
            return f'{short} — ⚠ *LDM chưa mô tả bảng này* (mục LDM: {rest})'
        para = rest
    txt = para
    if txt:
        txt = re.sub(r'\s+', ' ', txt).replace('|', '\\|')
        if len(txt) > 130:
            txt = txt[:127].rsplit(' ', 1)[0] + '…'
        return f'{short} — {txt}'
    return f'{short} — ⚠ *LDM chưa mô tả bảng này*' 


def muc_dich(ent, kind, tbl, parent_tbl, children, doc, epics):
    n = ent['name']
    role, giai_thich = vai_tro_of(ent, kind)
    grain = {'chungtu': '1 dòng = 1 chứng từ',
             'chitiet': f'1 dòng = 1 dòng chi tiết trên `{parent_tbl}`' if parent_tbl else '1 dòng = 1 dòng chi tiết',
             'so': '1 dòng = 1 bút toán Nợ/Có' if n == 'SoCai' else '1 dòng = 1 dòng biến động kho',
             'thuong': '1 dòng = 1 bản ghi'}[kind]
    out = ["**Mục đích & phạm vi nghiệp vụ**", "", "| Mục | Nội dung |", "|---|---|"]
    if doc:
        out.append(f"| Mô tả (LDM) | {' · '.join(d.replace('|', chr(92)+'|') for d in doc)} |")
    else:
        out.append("| Mô tả (LDM) | ⚠ **LDM chưa mô tả bảng này** — BA cần bổ sung "
                   "dòng `' Entity: <mô tả>` ngay trước khai báo entity trong `.puml` |")
    out.append(f"| Vai trò | {role} |")
    out.append(f"| Đơn vị 1 dòng | {grain} |")
    if giai_thich:
        out.append(f"| Dùng để làm gì | {giai_thich} |")
    if parent_tbl:
        out.append(f"| Bảng cha | `{parent_tbl}` — FK `ON DELETE CASCADE` |")
    if children:
        out.append("| Bảng con | " + ' · '.join(f'`{c}`' for c in children) + " |")
    if epics:
        out.append(f"| Epic nghiệp vụ | {' · '.join(epics)} |")
    out.append("")
    return out

# ---------------------------------------------------------------- base fields
BASE_ROWS = {
 'chungtu': [
  ('id','uuid','N','`gen_random_uuid()`','Khóa chính. `BaseEntity`'),
  ('tenant_id','uuid','N','—','Đơn vị kế toán sở hữu bản ghi; gán từ `TenantContext` lúc persist, không sửa. Khóa RLS. `TenantedEntity` · BR46.4'),
  ('phien_ban','integer','N','`1`','Khóa lạc quan `@Version`. `AggregateRootEntity`'),
  ('chi_nhanh_id','uuid','N','—','Chi nhánh phát sinh nghiệp vụ. Service gán tường minh, không lấy từ context. `BaseChungTuEntity` · BR46.4'),
  ('loai_chung_tu_id','uuid','N','—','Loại chứng từ. Nguồn: `mst_loai_chung_tu`. `BaseChungTuEntity` · BR4'),
  ('giao_dich_chung_tu_id','uuid','Y','—','Loại giao dịch của chứng từ. Nguồn: `mst_giao_dich_chung_tu`. `BaseChungTuEntity`'),
  ('so_chung_tu','varchar(50)','N','—','Số chứng từ, cấp theo quy tắc đánh số. `BaseChungTuEntity` · BR9 · BR20'),
  ('ngay_chung_tu','date','N','—','Ngày lập chứng từ. `BaseChungTuEntity`'),
  ('ngay_hach_toan','date','N','—','Ngày ghi sổ, có thể khác ngày chứng từ. `BaseChungTuEntity` · BR37'),
  ('status','text','N','`NHAP`','Trạng thái vòng đời: `NHAP`·`CHO_DUYET`·`DA_DUYET`·`DA_GHI_SO`·`HUY`. `BaseChungTuEntity` · BR12'),
  ('nguoi_duyet_id','uuid','Y','—','Người duyệt. `BaseChungTuEntity`'),
  ('ngay_duyet','timestamptz','Y','—','Thời điểm duyệt. `BaseChungTuEntity`'),
  ('nguoi_ghi_so','uuid','Y','—','Người ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46'),
  ('thoi_gian_ghi_so','timestamptz','Y','—','Thời điểm ghi sổ; về `null` khi bỏ ghi sổ. `BaseChungTuEntity` · BR42 · BR46'),
  ('ngay_tao','timestamptz','N','`now()`','Thời điểm tạo, gán một lần. `BaseEntity` · BR46'),
  ('nguoi_tao','uuid','Y','—','Người tạo, gán một lần. `BaseEntity` · BR46'),
  ('ngay_cap_nhat','timestamptz','Y','—','Thời điểm sửa gần nhất. `BaseEntity` · BR46'),
  ('nguoi_cap_nhat','uuid','Y','—','Người sửa gần nhất. `BaseEntity` · BR46'),
  ('da_xoa','boolean','N','`false`','Cờ xóa mềm; bản ghi `true` bị loại khỏi mọi danh sách/báo cáo. `BaseEntity` · BR29.1 · BR46'),
  ('ngay_xoa','timestamptz','Y','—','Thời điểm xóa mềm. `BaseEntity` · BR46'),
  ('nguoi_xoa','uuid','Y','—','Người xóa mềm. `BaseEntity` · BR46'),
 ],
 'chitiet': [
  ('id','uuid','N','`gen_random_uuid()`','Khóa chính. `BaseEntity`'),
  ('tenant_id','uuid','N','—','Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4'),
  ('thu_tu','integer','Y','—','Thứ tự dòng trong phiếu; đánh lại liên tục sau khi chèn/xóa. `BaseChiTietChungTuEntity` · BR21.2'),
  ('ngay_tao','timestamptz','N','`now()`','Thời điểm tạo. `BaseEntity` · BR46'),
  ('nguoi_tao','uuid','Y','—','Người tạo. `BaseEntity` · BR46'),
  ('ngay_cap_nhat','timestamptz','Y','—','Thời điểm sửa gần nhất. `BaseEntity` · BR46'),
  ('nguoi_cap_nhat','uuid','Y','—','Người sửa gần nhất. `BaseEntity` · BR46'),
  ('da_xoa','boolean','N','`false`','Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46'),
  ('ngay_xoa','timestamptz','Y','—','Thời điểm xóa mềm. `BaseEntity` · BR46'),
  ('nguoi_xoa','uuid','Y','—','Người xóa mềm. `BaseEntity` · BR46'),
 ],
 'thuong': [
  ('id','uuid','N','`gen_random_uuid()`','Khóa chính. `BaseEntity`'),
  ('tenant_id','uuid','N','—','Đơn vị kế toán sở hữu bản ghi. Khóa RLS. `TenantedEntity` · BR46.4'),
  ('ngay_tao','timestamptz','N','`now()`','Thời điểm tạo. `BaseEntity` · BR46'),
  ('nguoi_tao','uuid','Y','—','Người tạo. `BaseEntity` · BR46'),
  ('ngay_cap_nhat','timestamptz','Y','—','Thời điểm sửa gần nhất. `BaseEntity` · BR46'),
  ('nguoi_cap_nhat','uuid','Y','—','Người sửa gần nhất. `BaseEntity` · BR46'),
  ('da_xoa','boolean','N','`false`','Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46'),
  ('ngay_xoa','timestamptz','Y','—','Thời điểm xóa mềm. `BaseEntity` · BR46'),
  ('nguoi_xoa','uuid','Y','—','Người xóa mềm. `BaseEntity` · BR46'),
 ],
 'so': [
  ('id','uuid','N','`gen_random_uuid()`','Khóa chính. Bảng partition ⇒ PK là `(id, ngay_hach_toan)`. `BaseEntity`'),
  ('tenant_id','uuid','N','—','Đơn vị kế toán sở hữu dòng sổ. Khóa RLS. `TenantedEntity` · BR46.4'),
  ('request_hash','varchar(64)','N','—','Vân tay nội dung của lần ghi sổ — nền tảng **idempotency**. UNIQUE trên cột trần (bảng partition không nhận unique index dạng biểu thức/partial). *(không có trong LDM — hạ tầng bắt buộc)*'),
  ('ngay_tao','timestamptz','N','`now()`','Thời điểm tạo dòng sổ (LDM: `ThoiGianTao`). `BaseEntity` · BR46'),
  ('nguoi_tao','uuid','N','—','Người tạo dòng sổ (LDM: `NguoiTaoId`). `BaseEntity` · BR46'),
  ('da_xoa','boolean','N','`false`','Cờ xóa mềm. `BaseEntity` · BR29.1 · BR46'),
  ('ngay_xoa','timestamptz','Y','—','Thời điểm xóa mềm. `BaseEntity` · BR46'),
  ('nguoi_xoa','uuid','Y','—','Người xóa mềm. `BaseEntity` · BR46'),
 ],
}
BASE_NAMES = {k: set(r[0] for r in v) for k, v in BASE_ROWS.items()}
BASE_CLASS = {'chungtu': '`BaseChungTuEntity`', 'chitiet': '`BaseChiTietChungTuEntity`',
              'thuong': '`TenantedEntity`',
              'so': '`TenantedEntity` + `@Immutable` (bảng sổ — append-only, partition theo `ngay_hach_toan`)'}
LEDGER = {'SoCai', 'SoKho'}

# trường LDM đã nằm trong base ⇒ không lặp lại ở phần nghiệp vụ
LDM_BASE_FIELD = {
 'id','tenant_id','chi_nhanh_id','loai_chung_tu_id','giao_dich_chung_tu_id','so_chung_tu',
 'ngay_chung_tu','ngay_hach_toan','nguoi_tao_id','nguoi_tao','thoi_gian_tao','ngay_tao',
 'nguoi_cap_nhat_id','nguoi_cap_nhat','thoi_gian_cap_nhat','ngay_cap_nhat','da_xoa',
 'nguoi_xoa_id','nguoi_xoa','thoi_gian_xoa','ngay_xoa','nguoi_ghi_so_id','nguoi_ghi_so',
 'thoi_gian_ghi_so','nguoi_duyet_id','ngay_duyet','thu_tu','stt','phien_ban'}


# ---------------------------------------------------------------- đặt tên bảng
# Luật 1 (chuan-hoa-ten-bang-chung-tu.md §1): `chi_tiet` là HẬU TỐ.
#   tên bảng con = <tên bảng cha>_<vai trò>, vai trò mặc định = chi_tiet
# Luật 2: không viết tắt trong phần nghiệp vụ, không lặp lại tiền tố module.
EXPAND = {'tscd': 'tai_san_co_dinh', 'hd': 'hoa_don', 'dv': 'dich_vu',
          'nvl': 'nguyen_vat_lieu', 'ktth': 'ke_toan_tong_hop',
          'sdbd': 'so_du_ban_dau', 'kh': 'khach_hang', 'ncc': 'nha_cung_cap',
          'tk': 'tai_khoan'}
# token lặp lại tiền tố module ⇒ bỏ (luật 2)
DROP_REPEAT = {'ccdc': {'ccdc'}, 'ktth': {'ktth'}, 'sdbd': {'sdbd'}}

def biz_name(entname, prefix):
    """Phần nghiệp vụ của tên bảng: snake + giãn viết tắt + bỏ lặp tiền tố."""
    out = []
    drop = DROP_REPEAT.get(prefix, set())
    parts = snake(entname).split('_')
    for i, t in enumerate(parts):
        if t in drop and len(parts) > 1:
            continue
        out.append(EXPAND.get(t, t))
    return '_'.join(out) or snake(entname)

def parent_of(ent, by_name):
    """Entity cha — FK ĐẦU TIÊN trỏ tới một entity không phải bảng con.

    LDM khai FK về header ngay sau Id; các FK sau là liên kết nguồn
    (ChiTietDonDatHangId trên dòng hợp đồng...) nên KHÔNG được coi là cha.
    """
    for f in ent['fields']:
        n = f['name']
        if not n.endswith('Id'):
            continue
        cand = n[:-2]
        if cand in by_name and cand != ent['name'] and not is_detail(cand):
            return cand
    return None

def is_detail(name):
    return name.startswith('ChiTiet') or '_ChiTiet' in name

def child_role(entname, parentname, n_siblings=1):
    """Vai trò của bảng con so với bảng cha.

    Hậu tố sau `_` (ChiTietSDBD_KH_HoaDon → HoaDon) CHỈ được dùng làm vai trò khi
    bảng cha có NHIỀU bảng chi tiết cần phân biệt (PhieuKTTH: HachToan vs HoaDon).
    Cha chỉ có đúng một bảng chi tiết thì hậu tố đó chỉ mô tả nội dung dòng,
    không phải vai trò ⇒ vai trò là `chi_tiet`.
    """
    rem = entname[7:] if entname.startswith('ChiTiet') else entname
    if '_' in rem:
        if entname.startswith('ChiTiet') and n_siblings <= 1:
            return 'chi_tiet'
        return snake(rem.rsplit('_', 1)[1])
    if not parentname:
        return 'chi_tiet'
    if rem == parentname or parentname.endswith(rem):
        return 'chi_tiet'
    if rem.endswith(parentname):          # NguonVonTaiSanCoDinh + cha TaiSanCoDinh → NguonVon
        rem = rem[:-len(parentname)]
    return snake(rem) or 'chi_tiet' 

def table_name(ent, prefix, by_name, resolved):
    n = ent['name']
    if n in TABLE_OVERRIDE:
        return TABLE_OVERRIDE[n]
    par = parent_of(ent, by_name)
    if is_detail(n) or (par and n.startswith(('NguoiKiemKe', 'ThanhVien', 'HachToan',
                                              'LichSu', 'DauVao', 'ThanhPham'))):
        if par:
            base = resolved.get(par) or f"{prefix}_{biz_name(par, prefix)}"
            nsib = sum(1 for x in by_name.values()
                       if is_detail(x['name']) and parent_of(x, by_name) == par)
            role = child_role(n, par, nsib)
            if base.endswith('_' + role) or role == 'chi_tiet' and base.endswith('_chi_tiet'):
                return base if base != resolved.get(par) else base + '_chi_tiet'
            return f"{base}_{role}"
    if par and '_' in n:                 # PhieuKiemKeCCDC_DonVi → <cha>_don_vi
        base = resolved.get(par) or f"{prefix}_{biz_name(par, prefix)}"
        return f"{base}_{snake(n.rsplit('_', 1)[1])}"
    return f"{prefix}_{biz_name(n, prefix)}"

STOP = {'chi', 'tiet', 'chi_tiet', 'ent', 'chung', 'tu', 'phieu', 'bang'}

def toks(s):
    return set(t for t in s.split('_') if len(t) > 1)


# Bảng DB HIỆN CÓ tương ứng entity LDM — CHỐT TAY, không đoán.
# '' = đã rà, xác nhận chưa có bảng.  Thiếu key = chưa rà (in ra "? cần đối chiếu tay").
CURRENT = {
 # --- acc ---
 'SoCai':'acc_so_cai', 'SoKho':'acc_so_xuat_nhap_tong_hop',
 # --- iam / cfg ---
 'Tenant':'iam_tenant', 'Tenant_LinhVucHoatDong':'', 'VaiTro':'iam_vai_tro',
 'VaiTroQuyen':'iam_vai_tro_quyen', 'NguoiDungVaiTro':'iam_tai_khoan_vai_tro',
 'CauHinhEmail':'', 'NguoiDung':'iam_tai_khoan', 'NguoiDung_Tenant':'iam_tai_khoan_tenant',
 'YeuCauXoaTaiKhoan':'', 'GoiDichVu':'', 'Subscription':'', 'TenantModule':'',
 'NhatKyWebhookHub':'', 'TokenXacThuc':'', 'OTP':'', 'PhienDangNhap':'',
 'NhatKyHoatDong':'', 'ThamSoHeThong':'',
 'ThietLapKhoaSo':'cfg_thiet_lap_khoa_so',
 'ChiTietThietLapKhoaSoChungTu':'cfg_thiet_lap_khoa_so_chung_tu',
 'ChiTietThietLapKhoaSoNguoiDung':'cfg_thiet_lap_khoa_so_nguoi_dung',
 # --- inv ---
 'PhieuNhapKho':'inv_phieu_nhap_kho_module_kho','ChiTietPhieuNhapKho':'inv_chi_tiet_phieu_nhap_kho',
 'TonKho':'inv_ton_kho','CostLayer':'',
 'PhieuXuatKho':'inv_phieu_xuat_kho_module_kho','ChiTietPhieuXuatKho':'inv_chi_tiet_phieu_xuat_kho',
 'PhieuXuatDieuChuyen':'inv_phieu_xuat_dieu_chuyen',
 'ChiTietPhieuXuatDieuChuyen':'inv_chi_tiet_phieu_xuat_dieu_chuyen',
 'PhieuNhapDieuChuyen':'inv_phieu_nhap_dieu_chuyen',
 'ChiTietPhieuNhapDieuChuyen':'inv_chi_tiet_phieu_nhap_dieu_chuyen',
 'PhieuDieuChuyenDieuChinh':'inv_phieu_dieu_chuyen_dieu_chinh',
 'ChiTietPhieuDieuChuyenDieuChinh':'inv_chi_tiet_phieu_dieu_chuyen_dieu_chinh',
 'PhieuKiemKeKho':'inv_phieu_kiem_ke','ChiTietPhieuKiemKeKho':'inv_chi_tiet_kiem_ke',
 'ChiTietNguoiKiemKe':'','ChiTietTonKhoSnapShot':'',
 'LenhLapRapThaoDo':'','DauVaoLenhLapRapThaoDo':'','ThanhPhamSauLapRapThaoDo':'',
 'LuotTinhGiaXuatKho':'inv_luot_tinh_gia_xuat_kho',
 'KetQuaTinhGiaXuatKho':'inv_ket_qua_tinh_gia_xuat_kho',
 'ChiTietApGiaXuatKho':'inv_chi_tiet_ap_gia_xuat_kho',
 'DinhMucNVL':'','ChiTietDinhMucNVL':'','LenhSanXuat':'',
 'ChiTietLenhSanXuat_ThanhPham':'','ChiTietLenhSanXuat_NguyenVatLieu':'',
 'LoaiTruNguyenVatLieuLenhSanXuat':'',
 # --- pur ---
 'ChungTuMuaHang':'pur_chung_tu_mua_hang','ChiTietChungTuMuaHang':'pur_chi_tiet_chung_tu_mua_hang',
 'HoaDonMua':'pur_hoa_don_mua','ChungTuNhanHoaDon':'pur_chung_tu_nhan_hoa_don',
 'ChiTietHoaDon':'pur_chi_tiet_hoa_don','ChiPhiMuaHang':'pur_chi_phi_mua_hang',
 'ChiPhiNhapKhau':'pur_chi_phi_nhap_khau','PhanBoChiPhiMuaHang':'pur_phan_bo_chi_phi_mua_hang',
 'ChungTuTraLaiHangMua':'pur_chung_tu_tra_lai_hang_mua','PhieuXuatKhoTraLaiHangMua':'',
 'ChiTietChungTuTraLaiHangMua':'pur_chi_tiet_chung_tu_tra_lai_hang_mua',
 'ChungTuDieuChinhGiaHangMua':'pur_chung_tu_dieu_chinh_gia_mua',
 'ChiTietChungTuDieuChinhGiaHangMua':'pur_chi_tiet_dieu_chinh_gia_mua',
 'ChungTuDoiTru':'pur_chung_tu_doi_tru','ChiTietChungTuDoiTru':'pur_chi_tiet_chung_tu_doi_tru',
 # --- sal ---
 'HopDongBanHang':'','ChiTietHopDongBanHang':'','DieuKhoanThanhToanHopDong':'',
 'DonDatHang':'','ChiTietDonDatHang':'',
 'ChungTuBan':'sal_chung_tu_ban_hang','ChiTietChungTuBan':'sal_chi_tiet_chung_tu_ban_hang',
 'HoaDonBan':'','ChiTietHoaDonBan':'sal_chi_tiet_hd_ban_hang',
 'ChungTuTraLaiHangBan':'sal_chung_tu_tra_lai_hang_ban',
 'ChiTietTraLaiHangBan':'sal_chi_tiet_chung_tu_tra_lai_hang_ban',
 'ChungTuDieuChinhGiaHangBan':'sal_dieu_chinh_gia_hang_ban',
 'ChiTietDieuChinhGiaHangBan':'sal_chi_tiet_dieu_chinh_gia_hang_ban',
 # --- cb ---
 'PhieuThu':'cb_phieu_thu','ChiTietPhieuThu':'cb_chi_tiet_phieu_thu',
 'PhieuChi':'cb_phieu_chi','ChiTietPhieuChi':'cb_chi_tiet_phieu_chi',
 'ChiTietBangKeHoaDon':'cb_chi_tiet_bang_ke_hoa_don','ChuyenTienNoiBo':'','ChiTietChuyenTienNoiBo':'',
 # --- fa ---
 'ChungTuGhiGiamTSCD':'fa_chung_tu_ghi_giam_tscd','ChiTietGhiGiamTSCD':'fa_chi_tiet_ghi_giam_tscd',
 'HachToanGhiGiamTSCD':'fa_hach_toan_ghi_giam_tscd','ChungTuNgungKhauHao':'fa_chung_tu_ngung_khau_hao',
 'ChiTietNgungKhauHao':'fa_chi_tiet_ngung_khau_hao','KiemKeTaiSanCoDinh':'fa_kiem_ke_tai_san_co_dinh',
 'ChiTietKiemKeTaiSanCoDinh':'fa_chi_tiet_kiem_ke_tai_san_co_dinh',
 'ThanhVienKiemKeTaiSanCoDinh':'fa_thanh_vien_kiem_ke_tai_san_co_dinh',
 'DieuChinhTaiSanCoDinh':'fa_dieu_chinh_tai_san_co_dinh',
 'ThanhVienDieuChinhTaiSanCoDinh':'fa_thanh_vien_dieu_chinh_tai_san_co_dinh',
 'ChiTietDieuChinhTaiSanCoDinh':'fa_chi_tiet_dieu_chinh_tai_san_co_dinh',
 'HachToanDieuChinhTaiSanCoDinh':'fa_hach_toan_dieu_chinh_tai_san_co_dinh',
 'TaiSanCoDinh':'fa_tai_san_co_dinh','ChiTietNguonVonTaiSanCoDinh':'fa_tai_san_co_dinh_nguon_von',
 'ChiTietPhanBoTaiSanCoDinh':'fa_tai_san_co_dinh_phan_bo','LichSuPhanBoTaiSanCoDinh':'fa_lich_su_phan_bo',
 'PhuTungTaiSanCoDinh':'fa_tai_san_co_dinh_phu_tung',
 'BoPhanCauThanhTaiSanCoDinh':'fa_tai_san_co_dinh_bo_phan_cau_thanh',
 'ThongTinKhacTaiSanCoDinh':'fa_tai_san_co_dinh_thong_tin_khac',
 'LienKetChungTuTaiSanCoDinh':'fa_tai_san_co_dinh_lien_ket_chung_tu',
 'KhaiBaoSanLuong':'fa_khai_bao_san_luong','ChiTietKhaiBaoSanLuong':'fa_chi_tiet_khai_bao_san_luong',
 'DieuChuyenTaiSan':'fa_dieu_chuyen_tai_san','ChiTietDieuChuyenTaiSan':'fa_chi_tiet_dieu_chuyen',
 'LichSuDieuChuyenTaiSan':'','KhauHaoTaiSan':'fa_khau_hao_tai_san',
 'ChiTietKhauHaoTaiSan':'fa_chi_tiet_khau_hao_tai_san',
 # --- ccdc ---
 'CongCuDungCu':'ccdc_cong_cu_dung_cu','DonViQuanLyCCDC':'ccdc_don_vi_quan_ly_ccdc',
 'NhomHeSoPhanBoCCDC':'','HeSoPhanBoCongCuDungCu':'ccdc_he_so_phan_bo_ccdc',
 'PhieuKiemKeCCDC':'ccdc_phieu_kiem_ke_ccdc','PhieuKiemKeCCDC_DonVi':'',
 'NguoiKiemKeCCDC':'ccdc_chi_tiet_nguoi_kiem_ke','ChiTietKiemKeCCDC':'ccdc_chi_tiet_kiem_ke_ccdc',
 'PhieuDieuChinhCCDC':'ccdc_phieu_dieu_chinh_ccdc',
 'ChiTietPhieuDieuChinhCCDC':'ccdc_chi_tiet_phieu_dieu_chinh_ccdc',
 'PhieuDieuChuyenCCDC':'ccdc_phieu_dieu_chuyen_ccdc',
 'ChiTietPhieuDieuChuyenCCDC':'ccdc_chi_tiet_phieu_dieu_chuyen_ccdc',
 'PhieuGhiGiamCCDC':'ccdc_phieu_ghi_giam_ccdc',
 'ChiTietPhieuGhiGiamCCDC':'ccdc_chi_tiet_phieu_ghi_giam_ccdc',
 'PhieuPhanBoCCDC':'ccdc_phieu_phan_bo_ccdc',
 'ChiTietPhieuPhanBoCCDC':'ccdc_chi_tiet_phieu_phan_bo_ccdc',
 'TamDungPhanBoCCDC':'ccdc_tam_dung_phan_bo_ccdc',
 # --- cptt ---
 'KhaiBaoChiPhiTraTruoc':'cptt_khai_bao_chi_phi_tra_truoc',
 'ChungTuGocKhaiBaoChiPhiTraTruoc':'cptt_chung_tu_goc_khai_bao',
 'ThietLapPhanBoChiPhiTraTruoc':'cptt_thiet_lap_phan_bo_chi_phi',
 'KeHoachPhanBoChiPhiTraTruoc':'',
 'ChungTuPhanBoChiPhiTraTruoc':'cptt_chung_tu_phan_bo_chi_phi',
 'ChiTietPhanBoChiPhiTraTruoc':'cptt_chi_tiet_phan_bo_chi_phi',
 # --- cst ---
 'CauHinhGiaThanh':'cst_cau_hinh_gia_thanh','ThietLapHeSoTyLe':'cst_thiet_lap_he_so_ty_le',
 'KyTinhGiaThanh':'cst_ky_tinh_gia_thanh','DoDangDauKy':'cst_do_dang_dau_ky',
 'DoDangCuoiKy':'cst_do_dang_cuoi_ky','ChiTietDoDangCuoiKy':'cst_chi_tiet_do_dang_cuoi_ky',
 'PhanBoChiPhi':'cst_phan_bo_chi_phi','PhanBoChiPhi_DoiTuong':'','HeSoPhanBo':'cst_he_so_phan_bo',
 'ChiTietPhanBoChiPhi':'cst_chi_tiet_phan_bo_chi_phi','PhanBoChungTu':'cst_phan_bo_chung_tu',
 'GiaThanhSanPham':'cst_gia_thanh_san_pham','ChungTuGiaThanh':'cst_chung_tu_gia_thanh',
 'ChiTietChungTuGiaThanh':'cst_chi_tiet_chung_tu_gia_thanh','GiaThanhCongTrinh':'',
 'PhieuNghiemThuCongTrinh':'','ChiTietPhieuNghiemThuCongTrinh':'',
 'DinhMucGiaThanh':'cst_dinh_muc_gia_thanh',
 # --- ktth ---
 'PhieuKeToanTongHop':'ktth_phieu_ke_toan_tong_hop',
 'ChiTietPhieuKTTH_HachToan':'ktth_chi_tiet_phieu_ktth_hach_toan',
 'ChiTietPhieuKTTH_HoaDon':'ktth_chi_tiet_phieu_ktth_hoa_don',
 'ButToanKetChuyen':'','PhieuKetChuyenLaiLo':'','ChiTietPhieuKetChuyenLaiLo':'',
 # --- sdbd ---
 'SoDuBanDauTaiKhoan':'sdbd_so_du_ban_dau_tai_khoan','ChiTietSDBD_TaiKhoan':'sdbd_chi_tiet_sdbd_tai_khoan',
 'SoDuBanDauTKNganHang':'sdbd_so_du_ban_dau_tk_ngan_hang',
 'SoDuBanDauKhachHang':'sdbd_so_du_ban_dau_khach_hang','ChiTietSDBD_KH_HoaDon':'sdbd_chi_tiet_sdbd_kh_hoa_don',
 'SoDuBanDauNCC':'sdbd_so_du_ban_dau_ncc','ChiTietSDBD_NCC_HoaDon':'sdbd_chi_tiet_sdbd_ncc_hoa_don',
 'SoDuBanDauNhanVien':'sdbd_so_du_ban_dau_nhan_vien','SoDuBanDauVatTu':'sdbd_so_du_ban_dau_vat_tu',
 # --- rpt ---
 'BaoCaoTaiChinh':'rpt_bao_cao_tai_chinh',
 'BaoCaoTinhHinhTaiChinhChiTiet':'rpt_bc_tinh_hinh_tai_chinh_chi_tiet',
 'BaoCaoKetQuaHoatDongKinhDoanhChiTiet':'rpt_bc_ket_qua_hdkd_chi_tiet',
 'BaoCaoLuuChuyenTienTeTrucTiepChiTiet':'',
 'BaoCaoLuuChuyenTienTeGianTiepChiTiet':'rpt_bc_luu_chuyen_tt_gian_tiep_chi_tiet',
 'ThietLapChiTieu':'rpt_thiet_lap_chi_tieu','ThietLapCongThuc':'rpt_thiet_lap_cong_thuc',
 'HoatDongChungTu':'rpt_hoat_dong_chung_tu','HoatDongSoDuCongNo':'rpt_hoat_dong_so_du_cong_no',
 'HoatDongSoDuTaiKhoan':'rpt_hoat_dong_so_du_tai_khoan',
 # --- tax ---
 'ToKhaiThue01GTGT':'tax_to_khai_thue_01_gtgt',
 # --- tax: đã rà toàn bộ prefix tax_, chỉ tồn tại đúng 1 bảng ---
 'ThietLapThongTinThue':'','DangKyToKhaiThue':'','KhoiTaoToKhai':'','BangKeBanRa':'',
 'BangKeMuaVao':'','PhuLucGiamThue':'','PhuLucGiamThue_MuaVao':'','PhuLucGiamThue_BanRa':'',
 'PhuLuc01_6GTGT':'','PhuLuc01_6GTGT_TheoTinh':'','PhuLuc01_6GTGT_ChiTiet':'',
 'ToKhaiBoSung01KHBS':'','ToKhaiBoSung01KHBS_PhuLucPhanBo':'','BanGiaiTrinh01_1KHBS':'',
 'BanGiaiTrinh01_1KHBS_TaiLieuDinhKem':'','ToKhaiThue04GTGT':'',
 'ChiTietToKhai04GTGT_ChiTieu':'','ChiTietToKhai04GTGT_KhoanThuHo':'',
 'PhuLucGiamThue04GTGT':'','ChiTietPhuLucGiamThue04GTGT':'',
 # --- ccdc: 1 entity chưa chốt được, cố ý để '?' cho Pha 1 ---

 # --- fx (chưa có bảng nào) ---
 'PhieuDanhGiaLaiNgoaiTe':'','ChiTietDanhGiaLaiNgoaiTe_SoDu':'',
 'ChiTietDanhGiaLaiNgoaiTe_CongNo':'','ChiTietDanhGiaLaiNgoaiTe_HachToan':'',
 'KetQuaTinhTyGiaXuatQuy':'',
}

RESERVED = set(TABLE_OVERRIDE.values())
# bảng đã ALTER ... RENAME TO (không xuất hiện ở CREATE TABLE nên phải khai riêng)
RENAMED_IN = {'ccdc_cong_cu_dung_cu', 'mst_doi_tuong_tap_hop_vat_tu', 'mst_doi_tuong_tap_hop_chi_phi'}

def match_table(entname, proposed, prefix, live, used):
    """Khớp entity LDM với bảng DB hiện có — CHỈ theo map chốt tay CURRENT.

    Không đoán: entity chưa có trong CURRENT trả về cờ '?' để Pha 1 rà tay.
    """
    if entname not in CURRENT:
        return '?', 0.0
    cur = CURRENT[entname]
    if cur and cur not in live and cur not in RENAMED_IN:
        return '?', 0.0
    return cur, 1.0


AUDIT_ONLY = {
 'id','tenant_id','nguoi_tao_id','nguoi_tao','thoi_gian_tao','ngay_tao',
 'nguoi_cap_nhat_id','nguoi_cap_nhat','thoi_gian_cap_nhat','ngay_cap_nhat','da_xoa',
 'nguoi_xoa_id','nguoi_xoa','thoi_gian_xoa','ngay_xoa','phien_ban'}

def base_filter(kind):
    """Trường LDM nào được coi là đã nằm trong base ⇒ không lặp ở phần nghiệp vụ.

    Bảng sổ (kind='so') CHỈ lọc trường audit: so_chung_tu / ngay_chung_tu /
    ngay_hach_toan / loai_chung_tu_id trên dòng sổ là dữ liệu denormalized thật,
    không phải trường base kế thừa."""
    return AUDIT_ONLY if kind == 'so' else LDM_BASE_FIELD


def kind_of(ent, fields, by_name=None, file_khai_tenant=True):
    """Loại bảng.

    Quy ước LDM (header ldm-Kho-Update / ldm-BanHang-Update): *"TenantId, ChiNhanhId khai
    trực tiếp ở entity đầu chứng từ; entity chi tiết thừa hưởng qua entity cha"*.
    ⇒ Có TenantId = bảng gốc, KHÔNG phải bảng chi tiết — kể cả khi mang FK về một
    chứng từ khác (HoaDonBan giữ ChungTuBanId nhưng là chứng từ riêng).

    File nào không khai TenantId ở entity nào (LDM ghi "field hệ thống dùng chung không
    khai báo trong từng entity") thì quay về suy theo tên + FK cha.
    """
    n = ent['name']
    if n in LEDGER:
        return 'so'
    fnames = {snake(f['name']) for f in fields}
    if file_khai_tenant:
        goc = 'tenant_id' in fnames
        if goc:
            if fnames & {'so_chung_tu', 'ngay_chung_tu', 'ngay_hach_toan',
                         'so_hoa_don', 'ngay_hoa_don'}:
                return 'chungtu'
            return 'thuong'
        if by_name is not None and parent_of(ent, by_name):
            return 'chitiet'
        return 'thuong' 
    is_detail = (n.startswith('ChiTiet') or '_ChiTiet' in n
                 or any(re.match(r'^(chung_tu|phieu|hoa_don|don_dat_hang|hop_dong|lenh|to_khai|bao_cao|phu_luc)\w*_id$', x)
                        for x in fnames if x not in ('loai_chung_tu_id', 'giao_dich_chung_tu_id')))
    has_ct = {'so_chung_tu', 'ngay_chung_tu'} & fnames
    if has_ct and not n.startswith('ChiTiet'):
        return 'chungtu'
    if is_detail:
        return 'chitiet'
    return 'thuong'

# ---------------------------------------------------------------- sinh file
def main():
    dbcols, dropped = load_db_columns()
    live = {t: c for t, c in dbcols.items() if t not in dropped}
    coded = coded_tables()
    os.makedirs(OUT, exist_ok=True)
    index = []
    for fn in sorted(os.listdir(LDM)):
        if not fn.endswith('.puml') or 'DanhMuc' in fn:
            continue
        key = fn[:-5]
        prefix, title, num = MODULE.get(key, ('x', key, '99'))
        ents, header = parse_puml(os.path.join(LDM, fn))
        epics = sorted(set(re.findall(r'PMKT-[EU]-\d+', ' '.join(header))))
        ent_docs = {d for x in ents for d in x.get('doc', [])}
        scope = [h for h in header
                 if len(h) > 30 and not h.startswith(('Quy ước', '- '))
                 and re.sub(r'^Entity\s*:\s*', '', h) not in ent_docs][:6]
        out = [f"# `{prefix}_` — {title}", "",
               f"> Sinh tự động từ [`{fn}`](../../../pmkt-docs/ba/Common/LDM_update/{fn}) — "
               f"**không sửa tay**, sửa LDM rồi sinh lại.",
               f"> Chuẩn chung (trường base, domain type, hạ tầng): [`00-chuan-chung.md`](00-chuan-chung.md).",
               f"> Ký hiệu kiểu: `≈` = suy luận theo tên trường · `⚠` = **không suy được, phải chốt tay**.",
               "", f"**{len(ents)} bảng.**", ""]
        if scope:
            para = re.sub(r'\s+', ' ', ' '.join(scope)).strip()
            out += ["## Phân hệ này phục vụ nghiệp vụ gì", "", f"> {para}", ""]
            if epics:
                out += [f"**Epic nguồn:** {' · '.join(epics)}", ""]
        # mục lục
        out.append("| # | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Chức năng |")
        out.append("|---|---|---|---|---|---|")
        rows = []
        used = set()
        by_name = {x['name']: x for x in ents}
        khai_tenant = any('tenant_id' in {snake(f['name']) for f in x['fields']}
                          for x in ents)
        resolved = {}
        for e in ents:                       # lượt 1: bảng cha
            if not is_detail(e['name']):
                resolved[e['name']] = table_name(e, prefix, by_name, resolved)
        for e in ents:                       # lượt 2: bảng con
            if e['name'] not in resolved:
                resolved[e['name']] = table_name(e, prefix, by_name, resolved)
        for i, e in enumerate(ents, 1):
            tbl = resolved[e['name']]
            exist, score = match_table(e['name'], tbl, prefix, live, used)
            if exist and exist != '?':
                used.add(exist)
            if exist == '?':
                grp = '**? — chưa rà, Pha 1 đối chiếu tay**'
            elif exist in coded:
                grp = 'A — có code'
            elif exist:
                grp = 'B — có schema, chưa code'
            else:
                grp = 'C — tạo mới'
            rows.append((e, tbl, exist, grp))
            _kind = kind_of(e, e['fields'], by_name, khai_tenant)
            _par = parent_of(e, by_name)
            _cn = chuc_nang(e, _kind, e.get('doc') or [],
                            resolved.get(_par) if _par else None)
            out.append(f"| {i} | `{e['name']}` | `{tbl}` | "
                       f"{'`'+exist+'`' if exist and exist!='?' else ('*?*' if exist=='?' else '—')} "
                       f"| {grp} | {_cn} |")
        out.append("")
        for i, (e, tbl, exist, grp) in enumerate(rows, 1):
            kind = kind_of(e, e['fields'], by_name, khai_tenant)
            out.append("---"); out.append("")
            out.append(f"## {i}. `{tbl}`")
            out.append("")
            out.append(f"| Mục | Nội dung |")
            out.append(f"|---|---|")
            out.append(f"| Entity LDM | `{e['name']}` |")
            out.append(f"| Base class | {BASE_CLASS[kind]} |")
            out.append(f"| Nhóm | {grp} |")
            out.append(f"| Bảng hiện có | {'`'+exist+'`' if exist and exist!='?' else ('*chưa rà — Pha 1*' if exist=='?' else '*(chưa có)*')} |")
            out.append("")
            par = parent_of(e, by_name)
            kids = [resolved[x['name']] for x in ents
                    if parent_of(x, by_name) == e['name'] and x['name'] != e['name']]
            out += muc_dich(e, kind, tbl, resolved.get(par) if par else None,
                            kids, e.get('doc') or [], epics)
            # --- trường nghiệp vụ
            out.append("**Trường nghiệp vụ**")
            out.append("")
            out.append("| # | Trường LDM | Cột DB | Kiểu | Null | Mặc định | Mô tả |")
            out.append("|---|---|---|---|---|---|---|")
            k = 0
            biz_cols = []
            for f in e['fields']:
                c = snake(f['name'])
                if c in base_filter(kind) or c in BASE_NAMES[kind]:
                    continue
                k += 1
                ty, flag = map_type(f, e)
                nul = 'N' if (f['req'] or f['pk']) else 'Y'
                dfl = default_of(f, ty)
                desc = f['desc'].replace('|', '\\|') or '*(LDM chưa mô tả)*'
                if f['sect']:
                    desc = f"**[{f['sect']}]** {desc}"
                tags = ' '.join(f"`{t}`" for t in f['tags'] if t not in ('PK',))
                tyc = f"`{ty}`" + (f" {flag}" if flag and flag not in ('BR20',) else '')
                biz_cols.append(c)
                out.append(f"| {k} | `{f['name']}` | `{c}` | {tyc} | {nul} | {dfl} | {desc} {tags}".rstrip() + " |")
            if k == 0:
                out.append("| — | *(entity chỉ gồm trường base)* | | | | | |")
            out.append("")
            # --- trường base
            out.append(f"**Trường base — {BASE_CLASS[kind]}** *(hệ thống tự quản lý, không hiển thị trên form — BR46)*")
            out.append("")
            out.append("| Cột DB | Kiểu | Null | Mặc định | Mô tả |")
            out.append("|---|---|---|---|---|")
            for c, ty, nul, dfl, d in BASE_ROWS[kind]:
                out.append(f"| `{c}` | `{ty}` | {nul} | {dfl} | {d} |")
            out.append("")
            # --- đối chiếu bảng hiện có
            if exist and exist != '?' and exist in live:
                have = [c for c, _ in live[exist]]
                want = set(biz_cols) | BASE_NAMES[kind]
                missing = [c for c in biz_cols if c not in have]
                extra = [c for c in have if c not in want]
                out.append(f"**Đối chiếu `{exist}` ({len(have)} cột hiện có)**")
                out.append("")
                out.append("| Chiều | Số cột | Danh sách |")
                out.append("|---|---:|---|")
                out.append(f"| LDM có — DB **thiếu** | {len(missing)} | " +
                           (', '.join(f'`{c}`' for c in missing) or '*(không)*') + " |")
                out.append(f"| DB có — LDM **không khai** | {len(extra)} | " +
                           (', '.join(f'`{c}`' for c in extra) or '*(không)*') + " |")
                out.append("")
        open(f"{OUT}/{num}-{prefix}-{key.replace('ldm-','').lower()}.md", 'w',
             encoding='utf-8').write('\n'.join(out) + '\n')
        index.append((num, prefix, title, key, len(ents),
                      f"{num}-{prefix}-{key.replace('ldm-','').lower()}.md", rows))
    json.dump([[i[0], i[1], i[2], i[3], i[4], i[5]] for i in index],
              open('/tmp/idx.json', 'w'))
    # ma trận đối chiếu
    mx = ["# Ma trận đối chiếu — LDM entity × bảng DB × code", "",
          "> Sinh tự động. `A` = đã code (sửa đắt) · `B` = có schema chưa code (sửa rẻ) · `C` = phải tạo mới.", ""]
    tot = collections.Counter()
    mx.append("| Module | Entity LDM | Bảng đề xuất | Bảng hiện có | Nhóm | Hành động |")
    mx.append("|---|---|---|---|---|---|")
    for num, prefix, title, key, n, path, rows in index:
        for e, tbl, exist, grp in rows:
            g = grp[0]
            tot[g] += 1
            act = ('RÀ TAY' if g == '*' else 'VÁ + sửa code' if g == 'A' else
                   ('ĐỔI TÊN + VÁ' if (g == 'B' and exist != tbl) else
                    ('VÁ' if g == 'B' else 'TẠO MỚI')))
            mx.append(f"| {title} | `{e['name']}` | `{tbl}` | {'`'+exist+'`' if exist else '—'} | {g} | {act} |")
    mx.insert(3, f"**Tổng: {sum(tot.values())} entity — A: {tot['A']} · B: {tot['B']} · C: {tot['C']}**\n")
    open(f"{OUT}/90-doi-chieu.md", 'w', encoding='utf-8').write('\n'.join(mx) + '\n')
    print(f"OK — {sum(tot.values())} entity | A={tot['A']} B={tot['B']} C={tot['C']}")
    for num, prefix, title, key, n, path, rows in index:
        print(f"  {path:<44} {n:>3} bảng")

main()
