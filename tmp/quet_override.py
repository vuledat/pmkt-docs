# Quét lớp con của base CRUD/chứng từ: method nào ĐANG override (@Override), có gọi super không.
import os, re, collections

ROOT = r"C:/Users/Admin/Desktop/code/vtt-osp/cell-app/src/main/java/vn/vtt/pmkt/cell"
OUT = r"C:/Users/Admin/Desktop/code/vtt-osp/docs/tmp/override_report.txt"

BASES = {
    "BaseCrudController": {
        "khung": ["search", "cot", "get", "create", "update", "delete", "export", "importExcel"],
        "hook": ["tenFileExport", "cotMacDinh", "nhapDuLieu", "thongBaoTao", "thongBaoSua",
                 "thongBaoXoa", "service", "maChucNang", "maManHinh"],
    },
    "BaseChungTuController": {
        "khung": ["giaTriCot", "ghiSo", "boGhiSo", "nhanBan", "thongTinHachToan", "dongChiTiet",
                  "ghiSoHangLoat", "boGhiSoHangLoat", "xoaHangLoat"],
        "hook": ["hangLoat", "tenChungTu", "messageId"],
    },
    "AbstractCrudService": {
        "khung": ["search", "moTaCot", "get", "create", "update", "delete", "duLieuExport",
                  "giaTriCot", "kiemTraLock", "load"],
        "hook": ["notFound", "defaultSortAlias", "defaultSortDirection", "validateCreate",
                 "validateUpdate", "validateDelete", "beforeSave", "afterSave", "summary",
                 "specCuaRequest"],
    },
    "AbstractChungTuCrudService": {
        "khung": ["kiemTraTonTai"],
        "hook": ["ghiSo", "boGhiSo", "nhanBan", "layDongChiTiet", "traSoChungTu"],
    },
    "ChungTuTemplate": {
        "khung": ["thucThi", "kiemTraDauVao", "kiemTraQuyen", "yeuCauChungTu"],
        "hook": ["chuanBiChungTu", "kiemTraNghiepVu", "truocKhiLuu", "luuEntity", "sauKhiLuu",
                 "taoKetQua", "bangGoc", "maChucNang", "maLoaiChungTu", "hanhDong", "coGhiSoNgay",
                 "dienGiaiChung", "chungTuDangLuu", "soChungTuNguoiDungGo", "apDungTonKho",
                 "hoanTacTonKho", "ghiNhatKy", "guiThongBao", "coSinhButToan", "coAnhHuongTonKho",
                 "moTaAudit"],
    },
}
KHUNG = {b: set(v["khung"]) for b, v in BASES.items()}
TATCA = {b: set(v["khung"]) | set(v["hook"]) for b, v in BASES.items()}

files = []
for dirpath, _, filenames in os.walk(ROOT):
    if "master_data" in dirpath.replace("\\", "/"):
        continue
    files += [os.path.join(dirpath, f) for f in filenames if f.endswith(".java")]

CLS_RE = re.compile(r"\b(?:class|interface)\s+(\w+)(?:<[^>]*>)?\s*(?:extends\s+([\w.]+))?")
# @Override, các annotation xen giữa, rồi chữ ký method. Kiểu trả về KHÔNG được chứa ngoặc tròn —
# nếu cho phép thì regex nuốt luôn "@Transactional(readOnly = true)" và đọc tên method là
# "Transactional".
OV_RE = re.compile(
    r"@Override\b[ \t]*(?:\r?\n)"
    r"(?:[ \t]*@\w+(?:\([^\n]*\))?[ \t]*(?:\r?\n))*"
    r"[ \t]*((?:public|protected|private)[ \t]+[^;{}()]*?\b(\w+)[ \t]*\([^;{}]*?\))[ \t\r\n]*"
    r"(?:throws [\w, .\r\n\t]+?)?\{")

supers = {}
for path in files:
    src = open(path, encoding="utf-8").read()
    for m in CLS_RE.finditer(src):
        if m.group(2):
            supers[m.group(1)] = m.group(2).split(".")[-1]

def chain(cls):
    out, seen, cur = [], set(), supers.get(cls)
    while cur and cur not in seen:
        seen.add(cur); out.append(cur); cur = supers.get(cur)
    return out

def than(src, i):
    """Thân method bắt đầu từ dấu { tại i."""
    d, j = 0, i
    while j < len(src):
        if src[j] == "{": d += 1
        elif src[j] == "}":
            d -= 1
            if d == 0: return src[i:j + 1]
        j += 1
    return src[i:]

rows = collections.defaultdict(list)
for path in files:
    rel = path.replace("\\", "/").split("/vn/vtt/pmkt/cell/")[-1]
    src = open(path, encoding="utf-8").read()
    marks = [(m.start(), m.group(1)) for m in CLS_RE.finditer(src)]
    for m in OV_RE.finditer(src):
        cls = None
        for pos, name in marks:
            if pos < m.start(): cls = name
        if cls is None: continue
        bases = [b for b in chain(cls) if b in TATCA]
        if not bases: continue
        name = m.group(2)
        base = next((b for b in bases if name in TATCA[b]), None)
        if base is None: continue
        body = than(src, src.index("{", m.end() - 1))
        rows[(base, name)].append({
            "file": rel, "line": src[:m.start()].count("\n") + 2, "cls": cls,
            "super": f"super.{name}(" in body,
            "quyen": "quyen.require(" in body,
            "sig": " ".join(m.group(1).split())[:110],
            "loc": body.count("\n") + 1,
        })

out = ["# Lớp con override method của base — chỉ tính method có @Override", ""]
out.append("## Tổng hợp")
out.append(f"{'base.method':<48} {'loại':<7} {'#override':>9} {'#không super':>13}")
for (base, name), it in sorted(rows.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    loai = "KHUNG" if name in KHUNG[base] else "hook"
    out.append(f"{base + '.' + name + '()':<48} {loai:<7} {len(it):>9} "
               f"{sum(1 for x in it if not x['super']):>13}")

out += ["", "## Chi tiết các method KHUNG bị override"]
for (base, name), it in sorted(rows.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    if name not in KHUNG[base]:
        continue
    out.append(f"\n### {base}.{name}()  — {len(it)} nơi")
    for x in it:
        out.append(f"  {'no-super' if not x['super'] else 'super  '} "
                   f"{'quyen' if x['quyen'] else '     '} {x['loc']:>4} dòng  {x['file']}:{x['line']}")

open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("OK", len(files), "files,", sum(len(v) for v in rows.values()), "override")
