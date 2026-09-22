# -*- coding: utf-8 -*-
"""
Sinh seed biểu mẫu hệ thống + nguồn dữ liệu mẫu từ file Excel tham chiếu.

    python3 docs/doing/bieu-mau-dong/tools/sinh_seed_tu_excel.py

Đầu vào : docs/doing/bieu-mau-dong/mau/To_khai_thue_GTGT_khau_tru_01GTGT.xlsx
Đầu ra  : report-service/src/main/resources/bieu_mau/seed/<MA>.json   (11 biểu mẫu)
          report-service/src/main/resources/bieu_mau/nguon/<ma>.json  (nguồn dữ liệu mẫu)

Định nghĩa theo hợp đồng docs/doing/bieu-mau-dong/01-hop-dong-v1.md §1. Script là công cụ tái sinh
(idempotent) — sửa CONFIG rồi chạy lại, đừng sửa tay file JSON sinh ra.
"""
import json
import os
import re
import sys
from collections import Counter, OrderedDict
from datetime import date, datetime

from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string, get_column_letter

sys.stdout.reconfigure(encoding="utf-8")

GOC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
FILE_XLSX = os.path.join(GOC, "docs", "doing", "bieu-mau-dong", "mau", "To_khai_thue_GTGT_khau_tru_01GTGT.xlsx")
THU_MUC_SEED = os.path.join(GOC, "report-service", "src", "main", "resources", "bieu_mau", "seed")
THU_MUC_NGUON = os.path.join(GOC, "report-service", "src", "main", "resources", "bieu_mau", "nguon")

PT_MOI_KY_TU = 7 * 0.75          # rộng cột Excel (ký tự) → pt
CAO_DONG_MAC_DINH = 15.0
PT_MOI_INCH = 72
FONT_MAC_DINH = "Times New Roman"
FONT_THAY_THE = {"Arial": FONT_MAC_DINH, "Calibri": FONT_MAC_DINH, "Microsoft Sans Serif": FONT_MAC_DINH,
                 "Tahoma": FONT_MAC_DINH, "Segoe UI": FONT_MAC_DINH}
DO_DAY_VIEN = {"thin": 0.5, "hair": 0.25, "medium": 1.0, "thick": 1.5, "double": 1.0}
KHO_GIAY = {9: "A4", 8: "A3", 11: "A5", 1: "LETTER"}
NGAY_HIEU_LUC = "2020-01-01"
NHOM_THUE = "THUE_GTGT"
THAM_SO_TO_KHAI = [{"ma": "toKhaiId", "ten": "Tờ khai", "kieu": "uuid", "batBuoc": False}]
NGUON_HEADER_01 = {"ma": "header", "loai": "CATALOG", "provider": "thue.toKhai01.header",
                   "dangDong": "MOT_DONG", "thamSo": {"toKhaiId": "param.toKhaiId"}}


def nguon(ma, provider, dang="NHIEU_DONG"):
    return {"ma": ma, "loai": "CATALOG", "provider": provider, "dangDong": dang,
            "thamSo": {"toKhaiId": "param.toKhaiId"}}


# ───────────────────────────── cấu hình từng sheet ─────────────────────────────
# oCongThuc: toạ độ → công thức (thay text). dongLoai: số dòng → thuộc tính dòng. nhom: DongNhom.
# themO: dòng → danh sách ô tạo mới (khi sheet gốc để trống). ghiDe: toạ độ/dòng → ghi đè style.
CONFIG = [
    {  # 0
        "ma": "TO_KHAI_01_GTGT", "ten": "Tờ khai thuế giá trị gia tăng (Mẫu 01/GTGT)",
        "moTa": "Tờ khai thuế GTGT khấu trừ theo Thông tư 80/2021/TT-BTC — khối chỉ tiêu [21]…[43].",
        "nguon": [NGUON_HEADER_01],
        "oCongThuc": {
            "C5": '"Kỳ tính thuế: " & header.kyTinhThueChu',
            "E11": 'IF(header.ct21, "X", "")',
            "H12": "header.ct22", "E15": "header.ct23", "H15": "header.ct24", "E16": "header.ct23a",
            "H16": "header.ct24a", "H18": "header.ct25", "E20": "header.ct26", "E21": "header.ct27",
            "H21": "header.ct28", "E22": "header.ct29", "E23": "header.ct30", "H23": "header.ct31",
            "E24": "header.ct32", "H24": "header.ct33", "E25": "header.ct32a", "E26": "header.ct34",
            "H26": "header.ct35", "H27": "header.ct36", "H29": "header.ct37", "H30": "header.ct38",
            "H31": "header.ct39a", "H33": "header.ct40a", "H34": "header.ct40b", "H35": "header.ct40",
            "H36": "header.ct41", "H37": "header.ct42", "H39": "header.ct43",
        },
        "themO": {
            2: [{"cot": "A", "gopDen": "H", "congThuc": '"Tên người nộp thuế: " & header.tenNnt & "   —   Mã số thuế: " & header.mst',
                 "ghiDe": {"co": 10, "canNgang": "TRAI", "canDoc": "GIUA"}}],
        },
        "dongLoai": {8: {"loai": "HEADER", "lapMoiTrang": True}, 9: {"loai": "HEADER", "lapMoiTrang": True},
                     10: {"loai": "HEADER", "lapMoiTrang": True}},
    },
    {  # 1
        "ma": "BANG_KE_BAN_RA_01_1_GTGT", "ten": "Bảng kê hoá đơn, chứng từ hàng hoá, dịch vụ bán ra (01-1/GTGT)",
        "moTa": "Bảng kê bán ra chia 4 nhóm theo thuế suất, dòng tổng nhóm và tổng cuối bảng.",
        "cotToi": "I", "trang": {"huong": "NGANG"},
        "nguon": [NGUON_HEADER_01, nguon("bkbrNhom", "thue.bangKeBanRa.nhom"), nguon("bkbr", "thue.bangKeBanRa.dong")],
        "themO": {3: [{"cot": "A", "gopDen": "I", "congThuc": '"Kỳ tính thuế: " & header.kyTinhThueChu & "   —   " & header.tenNnt & " — MST " & header.mst',
                       "ghiDe": {"co": 10, "nghieng": True, "canNgang": "GIUA", "canDoc": "GIUA"}}]},
        "dongLoai": {4: {"loai": "HEADER", "lapMoiTrang": True}, 5: {"loai": "HEADER", "lapMoiTrang": True},
                     16: {"loai": "CHI_TIET", "nguon": "bkbr", "loc": "row.nhom = nhom.nhom",
                          "sapXep": "row.ngayHoaDon ASC, row.soHoaDon ASC", "danhSoLai": True, "tuDan": True}},
        "nhom": [{"id": "g1", "nguonNhom": "bkbrNhom", "tu": 6, "den": 36, "dau": [6], "than": [16], "cuoi": [8]}],
        "oCongThuc": {
            "A6": "nhom.tieuDe",
            "A8": '"Tổng nhóm " & nhom.nhom', "G8": "GROUP_SUM(bkbr.doanhThu)", "H8": "GROUP_SUM(bkbr.thueGtgt)",
            "A16": "ROW_INDEX()", "B16": "row.soHoaDon", "C16": "row.ngayHoaDon", "D16": "row.tenNguoiMua",
            "F16": "row.mstNguoiMua", "G16": "row.doanhThu", "H16": "row.thueGtgt", "I16": "row.ghiChu",
            "E37": "SUMIF(bkbr.doanhThu, bkbr.nhom <> 1)", "E38": "SUMIF(bkbr.thueGtgt, bkbr.nhom <> 1)",
        },
        "ghiDe": {16: {"co": 9}, "C16": {"dinhDangNgay": "dd/MM/yyyy"}},
    },
    {  # 2
        "ma": "BANG_KE_MUA_VAO_01_2_GTGT", "ten": "Bảng kê hoá đơn, chứng từ của hàng hoá, dịch vụ mua vào (01-2/GTGT)",
        "moTa": "Bảng kê mua vào chia 4 nhóm theo tính chất thuế, tổng nhóm, 5 dòng tổng cuối bảng.",
        "cotToi": "N", "trang": {"huong": "NGANG"},
        "nguon": [NGUON_HEADER_01, nguon("bkmvNhom", "thue.bangKeMuaVao.nhom"), nguon("bkmv", "thue.bangKeMuaVao.dong")],
        "themO": {3: [{"cot": "A", "gopDen": "N", "congThuc": '"Kỳ tính thuế: " & header.kyTinhThueChu & "   —   " & header.tenNnt & " — MST " & header.mst',
                       "ghiDe": {"co": 10, "nghieng": True, "canNgang": "GIUA", "canDoc": "GIUA"}}]},
        "dongLoai": {4: {"loai": "HEADER", "lapMoiTrang": True}, 5: {"loai": "HEADER", "lapMoiTrang": True},
                     7: {"loai": "CHI_TIET", "nguon": "bkmv", "loc": "row.nhom = nhom.nhom",
                         "sapXep": "row.ngayHoaDon ASC, row.soHoaDon ASC", "danhSoLai": True, "tuDan": True}},
        "nhom": [{"id": "g1", "nguonNhom": "bkmvNhom", "tu": 6, "den": 27, "dau": [6], "than": [7], "cuoi": [18]}],
        "oCongThuc": {
            "A6": "nhom.tieuDe",
            "A7": "ROW_INDEX()", "B7": "row.soHoaDon", "C7": "row.ngayHoaDon", "E7": "row.tenNguoiBan",
            "H7": "row.mstNguoiBan", "I7": "row.giaTri", "J7": "row.thueGtgt", "K7": 'IF(row.laNhapKhau, "X", "")',
            "M7": "row.ghiChu",
            "A18": '"Tổng nhóm " & nhom.nhom', "I18": "GROUP_SUM(bkmv.giaTri)", "J18": "GROUP_SUM(bkmv.thueGtgt)",
            "D28": "SUM(bkmv.giaTri)", "D29": "SUMIF(bkmv.giaTri, bkmv.laNhapKhau = TRUE)",
            "G30": "SUM(bkmv.thueGtgt)", "G31": "SUMIF(bkmv.thueGtgt, bkmv.nhom <> 4)",
            "F32": "SUMIF(bkmv.thueGtgt, bkmv.laNhapKhau = TRUE)",
        },
        "ghiDe": {"C7": {"dinhDangNgay": "dd/MM/yyyy"}, "A7": {"co": 9}},
    },
    {  # 3
        "ma": "PL_01_6_GTGT_VT", "ten": "Phụ lục 01-6/GTGT — Bảng phân bổ thuế GTGT phải nộp (viễn thông cước trả sau)",
        "moTa": "Phân bổ số thuế phải nộp cho từng tỉnh của dịch vụ viễn thông cước trả sau.",
        "trang": {"huong": "NGANG"},
        "nguon": [nguon("pl016", "thue.phuLuc016.header", "MOT_DONG"), nguon("chiTiet", "thue.phuLuc016.chiTiet"),
                  nguon("theoTinh", "thue.phuLuc016.theoTinh")],
        "dongLoai": {8: {"loai": "HEADER", "lapMoiTrang": True}, 9: {"loai": "HEADER", "lapMoiTrang": True},
                     10: {"loai": "CHI_TIET", "nguon": "chiTiet", "tuDan": True, "cao": 18},
                     12: {"loai": "CHI_TIET", "nguon": "theoTinh", "tuDan": True}},
        "themO": {
            10: [{"cot": "A", "congThuc": "ROW_INDEX()", "kieuDang": "_oGiua"}, {"cot": "B", "congThuc": "row.tenCoSo", "kieuDang": "_oChu"},
                 {"cot": "C", "congThuc": "row.mst", "kieuDang": "_oChu"}, {"cot": "D", "congThuc": "row.huyen", "kieuDang": "_oChu"},
                 {"cot": "E", "congThuc": "row.tinh", "kieuDang": "_oChu"}, {"cot": "F", "congThuc": "row.xaPhuong", "kieuDang": "_oChu"},
                 {"cot": "G", "congThuc": "row.cqt", "kieuDang": "_oChu"}, {"cot": "H", "congThuc": "row.dt5", "kieuDang": "_oSo"},
                 {"cot": "I", "congThuc": "row.dt10", "kieuDang": "_oSo"}, {"cot": "J", "congThuc": "row.dt5 + row.dt10", "kieuDang": "_oSo"},
                 {"cot": "K", "gopDen": "L", "congThuc": "row.thuePp1", "kieuDang": "_oSo"}],
            12: [{"cot": "A", "congThuc": "ROW_INDEX()", "kieuDang": "_oGiua"}, {"cot": "B", "gopDen": "J", "congThuc": "row.tinh", "kieuDang": "_oChu"},
                 {"cot": "K", "gopDen": "L", "congThuc": "row.thuePp1", "kieuDang": "_oSo"}],
        },
        "oCongThuc": {"K6": "pl016.soThuePhaiNop", "K7": "pl016.tongDoanhThu", "K13": "SUM(theoTinh.thuePp1)", "K14": "pl016.ct20"},
    },
    {  # 4
        "ma": "PL_01_6_GTGT_CSSX", "ten": "Phụ lục 01-6/GTGT — Bảng phân bổ thuế GTGT phải nộp (cơ sở sản xuất)",
        "moTa": "Phân bổ số thuế phải nộp cho từng tỉnh nơi có cơ sở sản xuất; hai phương pháp [17]/[21].",
        "trang": {"huong": "NGANG"},
        "nguon": [nguon("pl016", "thue.phuLuc016.header", "MOT_DONG"), nguon("chiTiet", "thue.phuLuc016.chiTiet"),
                  nguon("theoTinh", "thue.phuLuc016.theoTinh")],
        "dongLoai": {8: {"loai": "HEADER", "lapMoiTrang": True}, 9: {"loai": "HEADER", "lapMoiTrang": True},
                     10: {"loai": "HEADER", "lapMoiTrang": True}, 11: {"loai": "HEADER", "lapMoiTrang": True},
                     12: {"loai": "CHI_TIET", "nguon": "chiTiet", "tuDan": True},
                     14: {"loai": "CHI_TIET", "nguon": "theoTinh", "tuDan": True}},
        "oCongThuc": {
            "L6": "pl016.soThuePhaiNop", "L7": "pl016.tongDoanhThu",
            "A12": "ROW_INDEX()", "B12": "row.tenCoSo", "C12": "row.mst", "D12": "row.huyen", "E12": "row.tinh",
            "F12": "row.xaPhuong", "G12": "row.cqt", "H12": "row.dt5", "I12": "row.dt10", "J12": "row.dt5 + row.dt10",
            "K12": "row.thuePp1", "L12": "row.thuePp2",
            "A14": "ROW_INDEX()", "B14": "row.tinh", "K14": "row.thuePp1", "L14": "row.thuePp2",
            "K15": "SUM(theoTinh.thuePp1)", "L15": "SUM(theoTinh.thuePp2)",
            "K16": "pl016.ct20", "L16": "pl016.ct24",
        },
    },
    {  # 5
        "ma": "PL_GIAM_THUE_204", "ten": "Phụ lục giảm thuế GTGT theo Nghị quyết 204/2025/QH15",
        "moTa": "Mục I hàng mua vào 8%, Mục II hàng bán ra được giảm, Mục III chênh lệch.",
        "trang": {"kho": "A4", "huong": "DOC"},
        "nguon": [nguon("mucI", "thue.plGiamThue.muaVao"), nguon("mucII", "thue.plGiamThue.banRa")],
        "dongLoai": {8: {"loai": "HEADER", "lapMoiTrang": False},
                     9: {"loai": "CHI_TIET", "nguon": "mucI", "tuDan": True},
                     15: {"loai": "HEADER", "lapMoiTrang": False},
                     16: {"loai": "CHI_TIET", "nguon": "mucII", "tuDan": True}},
        "oCongThuc": {
            "A9": "ROW_INDEX()", "C9": "row.tenHhdv", "I9": "row.giaTri", "L9": "row.thueKhauTru",
            "I10": "SUM(mucI.giaTri)", "L10": "SUM(mucI.thueKhauTru)",
            "A16": "ROW_INDEX()", "C16": "row.tenHhdv", "F16": "row.giaTri", "G16": "row.thueSuat",
            "J16": "row.thueSuatSauGiam", "M16": "row.thueDuocGiam",
            "F17": "SUM(mucII.giaTri)", "M17": "SUM(mucII.thueDuocGiam)",
            "A19": "SUM(mucII.thueDuocGiam) - SUM(mucI.thueKhauTru)",
        },
    },
    {  # 6
        "ma": "TO_KHAI_BO_SUNG_01_KHBS", "ten": "Tờ khai bổ sung (Mẫu 01/KHBS)",
        "moTa": "Xác định tăng/giảm số thuế phải nộp, khấu trừ, đề nghị hoàn; số thuế thu hồi hoàn và tiền chậm nộp.",
        "nguon": [nguon("header", "thue.toKhaiBoSung.header", "MOT_DONG"), nguon("phaiNop", "thue.toKhaiBoSung.phaiNop"),
                  nguon("phanBo", "thue.toKhaiBoSung.phanBo"), nguon("khauTru", "thue.toKhaiBoSung.khauTru"),
                  nguon("deNghiHoan", "thue.toKhaiBoSung.deNghiHoan")],
        "dongLoai": {10: {"loai": "CHI_TIET", "nguon": "phaiNop", "tuDan": True},
                     17: {"loai": "CHI_TIET", "nguon": "phanBo", "tuDan": True},
                     26: {"loai": "CHI_TIET", "nguon": "khauTru", "tuDan": True},
                     32: {"loai": "CHI_TIET", "nguon": "deNghiHoan", "tuDan": True}},
        "token": {
            "AdditionDetail_hkbs01_01_SortOrder": "ROW_INDEX()", "AdditionDetail_hkbs01_01_SubsectionName": "row.tenTieuMuc",
            "AdditionDetail_hkbs01_01_TaxPaymentAmount": "row.soTien",
            "AdditionDetail_adjustment_SortOrderDisplay": "ROW_INDEX()", "AdditionDetail_adjustment_AppendixName": "row.tenDonVi",
            "AdditionDetail_adjustment_TaxCodeOrTaxAddress": "row.mst", "AdditionDetail_adjustment_District": "row.huyen",
            "AdditionDetail_adjustment_Provincial": "row.tinh", "AdditionDetail_adjustment_TaxAuthorities": "row.cqt",
            "AdditionDetail_adjustment_TaxPaymentAmount": "row.soTien", "TaxPaymentAdjust02Amount": "SUM(phanBo.soTien)",
            "SupplementDateKHBS": "header.ngayChamNopDen", "DelayDayToDate": "header.soNgayChamNop",
            "AmountLatePayment": "header.tienChamNop",
            "AdditionDetail_hkbs01_02_SortOrder": "ROW_INDEX()", "AdditionDetail_hkbs01_02_SubsectionName": "row.tenTieuMuc",
            "AdditionDetail_hkbs01_02_TaxPaymentAmount": "row.soTien",
            "AdditionDetail_hkbs01_03_SortOrder": "ROW_INDEX()", "AdditionDetail_hkbs01_03_SubsectionName": "row.tenTieuMuc",
            "AdditionDetail_hkbs01_03_TaxPaymentAmount": "row.soTien",
            "RefundAmount": "header.soTienThuHoiHoan", "TaxRefundNo": "header.quyetDinhHoanSo",
            "TaxRefundDicisionDate": "header.quyetDinhHoanNgay", "TaxBranchOffice": "header.cqtBanHanh",
            "provincekhbs": "header.tinhTp", "precinctkhbs": "header.xaPhuong", "TaxRefundOrderNo": "header.lenhHoanSo",
            "EffectDateTaxRefund": "header.lenhHoanNgay", "CountDayReceiveTaxRefund": "header.soNgayNhanTienHoan",
            "DelayMoneyPaymentAmount": "header.tienChamNopThuHoi",
        },
        "oCongThuc": {"AC11": "SUM(phaiNop.soTien)", "AC27": "SUM(khauTru.soTien)", "AC33": "SUM(deNghiHoan.soTien)"},
        "ghiDe": {"K20": {"dinhDangNgay": "dd/MM/yyyy"}, "S37": {"dinhDangNgay": "dd/MM/yyyy"}, "S39": {"dinhDangNgay": "dd/MM/yyyy"},
                  "I37": {"dinhDangSo": ""}, "E38": {"dinhDangSo": ""}, "AA38": {"dinhDangSo": ""}, "F39": {"dinhDangSo": ""}},
    },
    {  # 7
        "ma": "BAN_GIAI_TRINH_01_1_KHBS", "ten": "Bản giải trình khai bổ sung (Mẫu 01-1/KHBS)",
        "moTa": "Thông tin khai bổ sung theo từng chỉ tiêu điều chỉnh và tài liệu kèm theo.",
        "nguon": [nguon("header", "thue.giaiTrinhKhbs.header", "MOT_DONG"), nguon("gt", "thue.giaiTrinhKhbs.dong")],
        "dongLoai": {6: {"loai": "HEADER", "lapMoiTrang": True}, 7: {"loai": "HEADER", "lapMoiTrang": True},
                     8: {"loai": "CHI_TIET", "nguon": "gt", "tuDan": True}},
        "token": {
            "AdditionDetail_hkbs011_SortOrderDisplay": "row.stt", "AdditionDetail_hkbs011_DescriptionName": "row.tenChiTieu",
            "AdditionDetail_hkbs011_Code": "row.maChiTieu", "AdditionDetail_hkbs011_OrgAmount": "row.soDaKeKhai",
            "AdditionDetail_hkbs011_AdjustAmount": "row.soDieuChinh", "AdditionDetail_hkbs011_DiffAmount": "row.chenhLech",
            "AdditionDetail_hkbs011_AdjustmentAmountTax": "row.dieuChinhNghiaVu", "AdditionDetail_hkbs011_Reason": "row.lyDo",
            "TotalAdjustmentAmountTax40": "header.tongPhaiNop", "TotalAdjustmentAmountTax41": "header.tongKhauTru",
            "TotalAdjustmentAmountTax42": "header.tongDeNghiHoan", "attachment": "header.taiLieuKemTheo",
        },
        "ghiDe": {"D8": {"dinhDangSo": "#,##0;(#,##0)"}, "E8": {"dinhDangSo": "#,##0;(#,##0)"}, 13: {"xuongDong": True, "canDoc": "TREN"}},
        "dongThuocTinh": {13: {"tuDan": True}},
    },
    {  # 8
        "ma": "BANG_KE_01_5_GTGT", "ten": "Bảng kê số thuế GTGT đã nộp của doanh thu kinh doanh xây dựng, lắp đặt, bán hàng bất động sản ngoại tỉnh (01-5/GTGT)",
        "moTa": "Bảng kê chứng từ nộp thuế vãng lai ngoại tỉnh.",
        "trang": {"kho": "A4"},
        "nguon": [nguon("pl015", "thue.pl015.dong")],
        "dongLoai": {7: {"loai": "HEADER", "lapMoiTrang": True}, 8: {"loai": "CHI_TIET", "nguon": "pl015", "tuDan": True}},
        "token": {"AdditionDetail_015gtgt_SortOrder": "ROW_INDEX()", "AdditionDetail_015gtgt_ItemTaxNo": "row.soChungTu",
                  "AdditionDetail_015gtgt_ItemTaxDate": "row.ngayNop", "AdditionDetail_015gtgt_TaxAddress": "row.noiNop",
                  "AdditionDetail_015gtgt_TaxCompanyDecisionName": "row.cqtQuanLy", "AdditionDetail_015gtgt_TaxAmount": "row.soTien",
                  "Total015gtgtTaxAmount": "SUM(pl015.soTien)"},
        "ghiDe": {"C8": {"dinhDangNgay": "dd/MM/yyyy"}},
    },
    {  # 9
        "ma": "BANG_PHAN_BO_01_7_GTGT", "ten": "Bảng phân bổ số thuế GTGT phải nộp cho các địa phương nơi có công trình xây dựng, lắp đặt liên tỉnh (01-7/GTGT)",
        "moTa": "Phân bổ thuế GTGT theo công trình liên tỉnh.",
        "trang": {"kho": "A4"},
        "nguon": [nguon("pl017", "thue.pl017.dong")],
        "dongLoai": {7: {"loai": "HEADER", "lapMoiTrang": True}, 8: {"loai": "HEADER", "lapMoiTrang": True},
                     9: {"loai": "CHI_TIET", "nguon": "pl017", "tuDan": True}},
        "token": {"AdditionDetail_017gtgt_SortOrder": "ROW_INDEX()", "AdditionDetail_017gtgt_ProjectWorkName": "row.tenCongTrinh",
                  "AdditionDetail_017gtgt_SaleAmount": "row.doanhThu", "AdditionDetail_017gtgt_TaxCompanyDecisionName": "row.cqtDiaPhuong",
                  "AdditionDetail_017gtgt_AllocationRate": "row.tyLe", "AdditionDetail_017gtgt_TaxAmount": "row.soThue",
                  "Total017gtgtTaxAmount": "SUM(pl017.soThue)"},
        "ghiDe": {"E9": {"dinhDangSo": "#,##0.00"}},
    },
    {  # 10
        "ma": "PL_GIAM_THUE_406", "ten": "Phụ lục giảm thuế GTGT theo Nghị quyết 406/NQ-UBTVQH15",
        "moTa": "Giảm 30 % thuế suất cho hàng hoá, dịch vụ theo NQ 406.",
        "trang": {"kho": "A4"},
        "nguon": [nguon("pl406", "thue.pl406.dong")],
        "dongLoai": {6: {"loai": "HEADER", "lapMoiTrang": True}, 7: {"loai": "HEADER", "lapMoiTrang": True},
                     8: {"loai": "CHI_TIET", "nguon": "pl406", "tuDan": True}},
        "token": {"AdditionDetail_406gtgt_SortOrder": "ROW_INDEX()", "AdditionDetail_406gtgt_InventoryItemName": "row.tenHhdv",
                  "AdditionDetail_406gtgt_Amount": "row.giaTri", "AdditionDetail_406gtgt_TaxRate": "row.thueSuat",
                  "AdditionDetail_406gtgt_VatRate406": "row.thueSuatSauGiam", "AdditionDetail_406gtgt_DeductionsTaxAmount": "row.thueDuocGiam",
                  "Total406gtgtDeductionsTaxAmount": "SUM(pl406.thueDuocGiam)"},
        "ghiDe": {"D8": {"dinhDangSo": "#,##0.00"}, "E8": {"dinhDangSo": "#,##0.00"}},
    },
]

# style bổ sung dùng cho ô tạo mới (themO) — tên bắt đầu bằng "_" để không trùng s1..sn
KIEU_DANG_THEM = [
    {"ma": "_oChu", "co": 9, "canNgang": "TRAI", "canDoc": "GIUA", "xuongDong": True, "vien": "LRTB"},
    {"ma": "_oGiua", "co": 9, "canNgang": "GIUA", "canDoc": "GIUA", "vien": "LRTB"},
    {"ma": "_oSo", "co": 9, "canNgang": "PHAI", "canDoc": "GIUA", "vien": "LRTB", "dinhDangSo": "#,##0;(#,##0)"},
]


# ───────────────────────────── đọc style ô ─────────────────────────────
def mau(color):
    if color is None:
        return None
    rgb = getattr(color, "rgb", None)
    if isinstance(rgb, str) and len(rgb) == 8 and rgb not in ("FF000000", "00000000"):
        return "#" + rgb[2:]
    return None


def chuan_hoa_pattern(fmt):
    if not fmt or fmt == "General":
        return None
    fmt = fmt.replace("\\", "")
    if fmt in ("@",):
        return None
    if fmt.lower() in ("m/d/yyyy", "dd/mm/yyyy", "d/m/yyyy"):
        return ("ngay", "dd/MM/yyyy")
    return ("so", fmt)


def kieu_dang_cua(c):
    f, a, b = c.font, c.alignment, c.border
    kd = OrderedDict()
    ten_font = FONT_THAY_THE.get(f.name, f.name) if f.name else None
    if ten_font and ten_font != FONT_MAC_DINH:
        kd["font"] = ten_font
    if f.sz:
        kd["co"] = float(f.sz)
    if f.b:
        kd["dam"] = True
    if f.i:
        kd["nghieng"] = True
    if f.u:
        kd["gachChan"] = True
    mc = mau(f.color)
    if mc:
        kd["mauChu"] = mc
    if c.fill and c.fill.fill_type == "solid":
        mn = mau(c.fill.fgColor)
        if mn:
            kd["mauNen"] = mn
    if a.horizontal in ("left", "center", "right"):
        kd["canNgang"] = {"left": "TRAI", "center": "GIUA", "right": "PHAI"}[a.horizontal]
    if a.vertical in ("top", "center", "bottom"):
        kd["canDoc"] = {"top": "TREN", "center": "GIUA", "bottom": "DUOI"}[a.vertical]
    else:
        kd["canDoc"] = "GIUA"
    if a.wrap_text:
        kd["xuongDong"] = True
    if a.indent:
        kd["thutLe"] = float(a.indent) * 6
    vien = ""
    do_day = None
    for k, ch in (("left", "L"), ("right", "R"), ("top", "T"), ("bottom", "B")):
        s = getattr(b, k).style
        if s:
            vien += ch
            do_day = do_day or DO_DAY_VIEN.get(s, 0.5)
    if vien:
        kd["vien"] = vien
        if do_day and do_day != 0.5:
            kd["doDayVien"] = do_day
    p = chuan_hoa_pattern(c.number_format)
    if p:
        kd["dinhDangSo" if p[0] == "so" else "dinhDangNgay"] = p[1]
    return kd


class BangKieuDang:
    def __init__(self):
        self.theo_khoa = OrderedDict()

    def ma(self, kd):
        khoa = json.dumps(kd, sort_keys=True, ensure_ascii=False)
        if khoa not in self.theo_khoa:
            self.theo_khoa[khoa] = "s%d" % (len(self.theo_khoa) + 1)
        return self.theo_khoa[khoa]

    def danh_sach(self):
        return [dict(ma=m, **json.loads(k)) for k, m in self.theo_khoa.items()]


# ───────────────────────────── dựng định nghĩa ─────────────────────────────
def gia_tri_chu(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, (datetime, date)):
        return v.strftime("%d/%m/%Y")
    return str(v)


def dung_dinh_nghia(ws, cf):
    bang = BangKieuDang()
    # vùng in
    r1, c1, r2, c2 = 1, 1, ws.max_row, ws.max_column
    if ws.print_area:
        vung = ws.print_area.split("!")[-1].replace("$", "")
        a, b = vung.split(":")
        c1, r1 = column_index_from_string(re.match(r"[A-Z]+", a).group()), int(re.search(r"\d+", a).group())
        c2, r2 = column_index_from_string(re.match(r"[A-Z]+", b).group()), int(re.search(r"\d+", b).group())
    if cf.get("cotToi"):
        c2 = column_index_from_string(cf["cotToi"])
    c1 = 1
    r2 = max(r2, ws.max_row) if not ws.print_area else r2
    # cột
    cot = []
    for ci in range(c1, c2 + 1):
        chu = get_column_letter(ci)
        dim = ws.column_dimensions.get(chu)
        rong = (dim.width if dim and dim.width else 8.43) * PT_MOI_KY_TU
        cot.append({"ma": chu, "rong": round(rong, 1)})
    tap_cot = {c["ma"] for c in cot}
    # gộp ô
    gop = {}
    for rg in ws.merged_cells.ranges:
        if rg.min_row < r1 or rg.min_row > r2:
            continue
        toa = "%s%d" % (get_column_letter(rg.min_col), rg.min_row)
        gop[toa] = (min(rg.max_col, c2), min(rg.max_row, r2))
    trong_gop = set()
    for rg in ws.merged_cells.ranges:
        for rr in range(rg.min_row, rg.max_row + 1):
            for cc in range(rg.min_col, rg.max_col + 1):
                if (rr, cc) != (rg.min_row, rg.min_col):
                    trong_gop.add((rr, cc))
    # dòng
    dong_loai = cf.get("dongLoai", {})
    o_cong_thuc = cf.get("oCongThuc", {})
    token_map = cf.get("token", {})
    ghi_de = cf.get("ghiDe", {})
    them_o = cf.get("themO", {})
    dong_thuoc_tinh = cf.get("dongThuocTinh", {})
    dong_theo_so = OrderedDict()
    fonts = Counter()
    for r in range(r1, r2 + 1):
        dim = ws.row_dimensions.get(r)
        cao = dim.height if dim and dim.height else CAO_DONG_MAC_DINH
        d = OrderedDict(id="r%d" % r, loai="TINH", cao=round(float(cao), 2))
        d.update(dong_loai.get(r, {}))
        d.update(dong_thuoc_tinh.get(r, {}))
        o_ds = []
        for ci in range(c1, c2 + 1):
            if (r, ci) in trong_gop:
                continue
            c = ws.cell(row=r, column=ci)
            toa = c.coordinate
            co_vien = any(getattr(c.border, k).style for k in ("left", "right", "top", "bottom"))
            gia_tri = c.value
            if gia_tri is None and not co_vien and toa not in gop and toa not in o_cong_thuc:
                continue
            o = OrderedDict(cot=get_column_letter(ci))
            if toa in gop:
                mc, mr = gop[toa]
                if mc > ci:
                    o["gopDen"] = get_column_letter(mc)
                if mr > r:
                    o["gopDenDong"] = "r%d" % mr
            chuoi = gia_tri_chu(gia_tri).strip("\n")
            ct = None
            m = re.fullmatch(r"\s*##(.+?)##\s*", chuoi)
            if toa in o_cong_thuc:
                ct = o_cong_thuc[toa]
            elif m:
                ct = token_map.get(m.group(1), 'TOKEN("%s")' % m.group(1))
            elif chuoi.startswith("="):
                ct = None
                chuoi = ""
            if ct:
                o["congThuc"] = ct
            else:
                if chuoi:
                    o["text"] = chuoi
            if c.font and c.font.name:
                fonts[FONT_THAY_THE.get(c.font.name, c.font.name)] += 1
            kd = kieu_dang_cua(c)
            for k in (r, toa):
                if k in ghi_de:
                    kd.update(ghi_de[k])
            kd = OrderedDict((k, v) for k, v in kd.items() if v not in ("", None))
            o["kieuDang"] = bang.ma(kd)
            o_ds.append(o)
        for o in them_o.get(r, []):
            o = OrderedDict(o)
            o.setdefault("kieuDang", "s1")
            # ô tạo thêm thay ô cùng cột, và nuốt các ô nằm trong vùng gộp của nó
            c_tu = column_index_from_string(o["cot"])
            c_den = column_index_from_string(o.get("gopDen", o["cot"]))
            o_ds = [x for x in o_ds if not (c_tu <= column_index_from_string(x["cot"]) <= c_den)]
            o_ds.append(o)
        o_ds.sort(key=lambda x: column_index_from_string(x["cot"]))
        d["o"] = o_ds
        dong_theo_so[r] = d
    # nhóm
    dong = []
    da_dung = set()
    nhom_cf = {n["tu"]: n for n in cf.get("nhom", [])}
    for r, d in dong_theo_so.items():
        if r in da_dung:
            continue
        if r in nhom_cf:
            n = nhom_cf[r]
            for rr in range(n["tu"], n["den"] + 1):
                da_dung.add(rr)
            g = OrderedDict(id=n["id"], loai="NHOM", nguonNhom=n["nguonNhom"], anKhiRong=False,
                            dau=[dong_theo_so[x] for x in n["dau"]], than=[dong_theo_so[x] for x in n["than"]],
                            cuoi=[dong_theo_so[x] for x in n["cuoi"]])
            dong.append(g)
            continue
        dong.append(d)
    # trang
    ps = ws.page_setup
    kho = KHO_GIAY.get(ps.paperSize, "A4")
    if kho == "LETTER":
        kho = "A4"
    trang = OrderedDict(kho=kho, huong="NGANG" if ps.orientation == "landscape" else "DOC",
                        le=OrderedDict(tren=round(ws.page_margins.top * PT_MOI_INCH), duoi=round(ws.page_margins.bottom * PT_MOI_INCH),
                                       trai=round(ws.page_margins.left * PT_MOI_INCH), phai=round(ws.page_margins.right * PT_MOI_INCH)),
                        coGiuTrang="VUA_CHIEU_RONG")
    trang.update(cf.get("trang", {}))
    font_md = fonts.most_common(1)[0][0] if fonts else FONT_MAC_DINH
    dn = OrderedDict(schemaVersion=1, ma=cf["ma"], ten=cf["ten"], trang=trang,
                     font=OrderedDict(macDinh=font_md, coMacDinh=9),
                     thamSo=THAM_SO_TO_KHAI, nguonDuLieu=cf["nguon"], bien=[],
                     kieuDang=bang.danh_sach() + KIEU_DANG_THEM, cot=cot, dong=dong, phanTuNoi=[])
    # kiểm tra nhanh: gopDenDong trỏ dòng còn tồn tại?
    ids = set()

    def thu(ds):
        for x in ds:
            if x["loai"] == "NHOM":
                thu(x["dau"]); thu(x["than"]); thu(x["cuoi"])
            else:
                ids.add(x["id"])
    thu(dong)
    for d in [x for x in dong if x["loai"] != "NHOM"]:
        for o in d["o"]:
            if "gopDenDong" in o and o["gopDenDong"] not in ids:
                del o["gopDenDong"]
    return dn


# ───────────────────────────── nguồn dữ liệu mẫu ─────────────────────────────
def so(v):
    if v in (None, ""):
        return 0
    try:
        return int(str(v).replace(",", ""))
    except ValueError:
        return float(str(v).replace(",", ""))


def ngay(v):
    if isinstance(v, (datetime, date)):
        return v.strftime("%Y-%m-%d")
    d, m, y = str(v).split("/")
    return "%s-%02d-%02d" % (y, int(m), int(d))


def truong(*cap):
    return [{"ma": m, "ten": t, "kieu": k} for m, t, k in cap]


def nguon_json(ma, ten, dang, tr, du_lieu, nhom_hien_thi="Thuế GTGT"):
    return OrderedDict(ma=ma, ten=ten, nhom=nhom_hien_thi, dangDong=dang, truong=tr,
                       thamSo=[{"ma": "toKhaiId", "ten": "Tờ khai", "kieu": "uuid", "batBuoc": False}],
                       duLieuMau=du_lieu)


def sinh_nguon(wb):
    ws0, ws1, ws2, ws4, ws5 = wb.worksheets[0], wb.worksheets[1], wb.worksheets[2], wb.worksheets[4], wb.worksheets[5]
    ds = []
    ct = {k: so(ws0[c].value) for k, c in {
        "ct22": "H12", "ct23": "E15", "ct24": "H15", "ct23a": "E16", "ct24a": "H16", "ct25": "H18", "ct26": "E20",
        "ct27": "E21", "ct28": "H21", "ct29": "E22", "ct30": "E23", "ct31": "H23", "ct32": "E24", "ct33": "H24",
        "ct32a": "E25", "ct34": "E26", "ct35": "H26", "ct36": "H27", "ct37": "H29", "ct38": "H30", "ct39a": "H31",
        "ct40a": "H33", "ct40b": "H34", "ct40": "H35", "ct41": "H36", "ct42": "H37", "ct43": "H39"}.items()}
    header = OrderedDict(tenNnt="Công ty Cổ phần Dược phẩm Minh Đức (Demo)", mst="0100101114", kyTinhThueChu="Tháng 12 năm 2025",
                         lanDau=True, lanBoSung=0, ngayKy="2026-01-15", nguoiKy="Nguyễn Văn A", tenDaiLy="", mstDaiLy="",
                         hopDongSo="", ngayHopDong=None, diaChi="Số 1 Trần Hưng Đạo", xaPhuong="Phường Hoàn Kiếm", tinhTp="Thành phố Hà Nội",
                         ct21=False, ct42a=0, ct42b=0)
    header.update(ct)
    tr_header = truong(("tenNnt", "Tên người nộp thuế", "CHU"), ("mst", "Mã số thuế", "CHU"), ("kyTinhThueChu", "Kỳ tính thuế (chữ)", "CHU"),
                       ("lanDau", "Lần đầu", "LOGIC"), ("lanBoSung", "Bổ sung lần thứ", "SO"), ("ngayKy", "Ngày ký", "NGAY"),
                       ("nguoiKy", "Người ký", "CHU"), ("tenDaiLy", "Tên đại lý thuế", "CHU"), ("mstDaiLy", "MST đại lý thuế", "CHU"),
                       ("hopDongSo", "Số hợp đồng đại lý", "CHU"), ("ngayHopDong", "Ngày hợp đồng đại lý", "NGAY"),
                       ("diaChi", "Địa chỉ", "CHU"), ("xaPhuong", "Xã/Phường/Đặc khu", "CHU"), ("tinhTp", "Tỉnh/Thành phố", "CHU"),
                       ("ct21", "[21] Không phát sinh", "LOGIC")) + \
        [{"ma": k, "ten": "Chỉ tiêu [%s]" % k[2:], "kieu": "SO"} for k in
         ["ct22", "ct23", "ct23a", "ct24", "ct24a", "ct25", "ct26", "ct27", "ct28", "ct29", "ct30", "ct31", "ct32", "ct32a", "ct33",
          "ct34", "ct35", "ct36", "ct37", "ct38", "ct39a", "ct40a", "ct40b", "ct40", "ct41", "ct42", "ct42a", "ct42b", "ct43"]]
    ds.append(nguon_json("thue.toKhai01.header", "Tờ khai 01/GTGT — thông tin chung & chỉ tiêu", "MOT_DONG", tr_header, [header]))

    # bảng kê bán ra
    nhom_bkbr = [
        {"nhom": 1, "tieuDe": "1. Hàng hóa, dịch vụ không chịu thuế giá trị gia tăng (GTGT):", "thueSuat": 0},
        {"nhom": 2, "tieuDe": "2. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 0%:", "thueSuat": 0},
        {"nhom": 3, "tieuDe": "3. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 5%:", "thueSuat": 5},
        {"nhom": 4, "tieuDe": "4. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 10%:", "thueSuat": 10},
    ]
    ds.append(nguon_json("thue.bangKeBanRa.nhom", "Bảng kê bán ra — 4 nhóm thuế suất", "NHIEU_DONG",
                         truong(("nhom", "Số nhóm", "SO"), ("tieuDe", "Tiêu đề nhóm", "CHU"), ("thueSuat", "Thuế suất %", "SO")), nhom_bkbr))
    bkbr = []
    for r in range(16, 36):
        if ws1.cell(row=r, column=2).value is None:
            continue
        bkbr.append(OrderedDict(nhom=4, soHoaDon=str(ws1["B%d" % r].value), ngayHoaDon=ngay(ws1["C%d" % r].value),
                                tenNguoiMua=ws1["D%d" % r].value or "", mstNguoiMua=ws1["F%d" % r].value or "",
                                doanhThu=so(ws1["G%d" % r].value), thueGtgt=so(ws1["H%d" % r].value), ghiChu="",
                                maTraCuu="", duongDanTraCuu="", soDonHang="", sanTmdt="", tenShop=""))
    bkbr.append(OrderedDict(nhom=3, soHoaDon="12", ngayHoaDon="2026-12-05", tenNguoiMua="Công ty TNHH Nông sản Xanh (Demo)",
                            mstNguoiMua="0101234567", doanhThu=120000000, thueGtgt=6000000, ghiChu="", maTraCuu="", duongDanTraCuu="",
                            soDonHang="", sanTmdt="", tenShop=""))
    ds.append(nguon_json("thue.bangKeBanRa.dong", "Bảng kê bán ra — dòng hoá đơn", "NHIEU_DONG",
                         truong(("nhom", "Nhóm thuế suất (1-4)", "SO"), ("soHoaDon", "Số hoá đơn", "CHU"), ("ngayHoaDon", "Ngày lập hoá đơn", "NGAY"),
                                ("tenNguoiMua", "Tên người mua", "CHU"), ("mstNguoiMua", "MST người mua", "CHU"),
                                ("doanhThu", "Doanh thu chưa thuế", "SO"), ("thueGtgt", "Thuế GTGT", "SO"), ("ghiChu", "Ghi chú", "CHU"),
                                ("maTraCuu", "Mã tra cứu HĐĐT", "CHU"), ("duongDanTraCuu", "Đường dẫn tra cứu", "CHU"),
                                ("soDonHang", "Số đơn hàng", "CHU"), ("sanTmdt", "Sàn TMĐT", "CHU"), ("tenShop", "Tên shop", "CHU")), bkbr))

    # bảng kê mua vào
    nhom_bkmv = [
        {"nhom": 1, "tieuDe": ws2["A6"].value}, {"nhom": 2, "tieuDe": ws2["A19"].value},
        {"nhom": 3, "tieuDe": ws2["A22"].value}, {"nhom": 4, "tieuDe": ws2["A25"].value},
    ]
    ds.append(nguon_json("thue.bangKeMuaVao.nhom", "Bảng kê mua vào — 4 nhóm tính chất", "NHIEU_DONG",
                         truong(("nhom", "Số nhóm", "SO"), ("tieuDe", "Tiêu đề nhóm", "CHU")), nhom_bkmv))
    bkmv = []
    for r in range(7, 18):
        bkmv.append(OrderedDict(nhom=1, soHoaDon=str(ws2["B%d" % r].value), ngayHoaDon=ngay(ws2["C%d" % r].value),
                                tenNguoiBan=ws2["E%d" % r].value or "", mstNguoiBan=ws2["H%d" % r].value or "",
                                giaTri=so(ws2["I%d" % r].value), thueGtgt=so(ws2["J%d" % r].value),
                                laNhapKhau=(ws2["K%d" % r].value or "").strip() == "X", ghiChu="", maTraCuu="", duongDanTraCuu=""))
    ds.append(nguon_json("thue.bangKeMuaVao.dong", "Bảng kê mua vào — dòng hoá đơn", "NHIEU_DONG",
                         truong(("nhom", "Nhóm tính chất (1-4)", "SO"), ("soHoaDon", "Số hoá đơn", "CHU"), ("ngayHoaDon", "Ngày lập hoá đơn", "NGAY"),
                                ("tenNguoiBan", "Tên người bán", "CHU"), ("mstNguoiBan", "MST người bán", "CHU"),
                                ("giaTri", "Giá trị chưa thuế", "SO"), ("thueGtgt", "Thuế GTGT", "SO"), ("laNhapKhau", "Là chứng từ nhập khẩu", "LOGIC"),
                                ("ghiChu", "Ghi chú", "CHU"), ("maTraCuu", "Mã tra cứu HĐĐT", "CHU"), ("duongDanTraCuu", "Đường dẫn tra cứu", "CHU")), bkmv))

    # PL 01-6
    ds.append(nguon_json("thue.phuLuc016.header", "PL 01-6/GTGT — chỉ tiêu tổng", "MOT_DONG",
                         truong(("soThuePhaiNop", "[06] Số thuế phải nộp", "SO"), ("tongDoanhThu", "[07] Tổng doanh thu chưa thuế", "SO"),
                                ("ct20", "[20] Số thuế nộp nơi trụ sở chính (PP1)", "SO"), ("ct24", "[24] Số thuế nộp nơi trụ sở chính (PP2)", "SO")),
                         [OrderedDict(soThuePhaiNop=so(ws4["L6"].value), tongDoanhThu=so(ws4["L7"].value), ct20=so(ws4["K16"].value), ct24=so(ws4["L16"].value))]))
    ds.append(nguon_json("thue.phuLuc016.chiTiet", "PL 01-6/GTGT — chi tiết cơ sở sản xuất", "NHIEU_DONG",
                         truong(("tenCoSo", "Chỉ tiêu (tên cơ sở)", "CHU"), ("mst", "MST/Mã ĐĐKD", "CHU"), ("huyen", "Huyện", "CHU"),
                                ("tinh", "Tỉnh/TP", "CHU"), ("xaPhuong", "Xã/Phường/Đặc khu", "CHU"), ("cqt", "CQT quản lý địa bàn", "CHU"),
                                ("dt5", "Doanh thu HH 5%", "SO"), ("dt10", "Doanh thu HH 10%", "SO"), ("thuePp1", "[17] Thuế phải nộp PP1", "SO"),
                                ("thuePp2", "[21] Thuế phải nộp PP2", "SO")),
                         [OrderedDict(tenCoSo="Nhà máy Cần Thơ (Demo)", mst="0100101114-001", huyen="", tinh=ws4["E12"].value, xaPhuong=ws4["F12"].value,
                                      cqt=ws4["G12"].value, dt5=so(ws4["H12"].value), dt10=so(ws4["I12"].value), thuePp1=so(ws4["K12"].value), thuePp2=so(ws4["L12"].value)),
                          OrderedDict(tenCoSo="Chi nhánh Đà Nẵng (Demo)", mst="0100101114-002", huyen="", tinh="Thành phố Đà Nẵng", xaPhuong="Phường Hải Châu",
                                      cqt="Chi cục Thuế khu vực XII", dt5=250000000, dt10=1200000000, thuePp1=26500000, thuePp2=0)]))
    ds.append(nguon_json("thue.phuLuc016.theoTinh", "PL 01-6/GTGT — cộng theo từng tỉnh", "NHIEU_DONG",
                         truong(("tinh", "Tỉnh/TP", "CHU"), ("thuePp1", "[18] Thuế phải nộp PP1", "SO"), ("thuePp2", "[22] Thuế phải nộp PP2", "SO")),
                         [OrderedDict(tinh=ws4["B14"].value, thuePp1=so(ws4["K14"].value), thuePp2=so(ws4["L14"].value)),
                          OrderedDict(tinh="Thành phố Đà Nẵng", thuePp1=26500000, thuePp2=0)]))

    # PL giảm thuế
    ds.append(nguon_json("thue.plGiamThue.muaVao", "PL giảm thuế — Mục I HHDV mua vào 8%", "NHIEU_DONG",
                         truong(("tenHhdv", "Tên hàng hoá, dịch vụ", "CHU"), ("giaTri", "Giá trị chưa thuế", "SO"), ("thueKhauTru", "Thuế GTGT được khấu trừ", "SO")),
                         [OrderedDict(tenHhdv="Dịch vụ vận chuyển (Demo)", giaTri=50000000, thueKhauTru=4000000),
                          OrderedDict(tenHhdv="Vật tư đóng gói (Demo)", giaTri=12500000, thueKhauTru=1000000)]))
    ds.append(nguon_json("thue.plGiamThue.banRa", "PL giảm thuế — Mục II HHDV bán ra", "NHIEU_DONG",
                         truong(("tenHhdv", "Tên hàng hoá, dịch vụ", "CHU"), ("giaTri", "Giá trị chưa thuế", "SO"), ("thueSuat", "Thuế suất theo quy định %", "SO"),
                                ("thueSuatSauGiam", "Thuế suất sau giảm %", "SO"), ("thueDuocGiam", "Thuế GTGT được giảm", "SO")),
                         [OrderedDict(tenHhdv=ws5["C16"].value, giaTri=so(ws5["F16"].value), thueSuat=so(ws5["G16"].value), thueSuatSauGiam=so(ws5["J16"].value), thueDuocGiam=so(ws5["M16"].value)),
                          OrderedDict(tenHhdv="Sữa tươi tiệt trùng (Demo)", giaTri=3200000, thueSuat=10, thueSuatSauGiam=8, thueDuocGiam=64000)]))

    # Tờ khai bổ sung
    ds.append(nguon_json("thue.toKhaiBoSung.header", "Tờ khai bổ sung 01/KHBS — chỉ tiêu đơn", "MOT_DONG",
                         truong(("ngayChamNopDen", "Số ngày chậm nộp tính đến ngày", "NGAY"), ("soNgayChamNop", "[a] Số ngày chậm nộp", "SO"),
                                ("tienChamNop", "[b] Số tiền chậm nộp", "SO"), ("soTienThuHoiHoan", "Số tiền thu hồi hoàn", "SO"),
                                ("quyetDinhHoanSo", "Quyết định hoàn thuế số", "CHU"), ("quyetDinhHoanNgay", "Ngày quyết định hoàn", "NGAY"),
                                ("cqtBanHanh", "CQT ban hành quyết định", "CHU"), ("tinhTp", "Tỉnh/Thành phố", "CHU"), ("xaPhuong", "Xã/Phường/Đặc khu", "CHU"),
                                ("lenhHoanSo", "Lệnh hoàn thuế số", "CHU"), ("lenhHoanNgay", "Ngày lệnh hoàn", "NGAY"),
                                ("soNgayNhanTienHoan", "Số ngày nhận được tiền hoàn", "SO"), ("tienChamNopThuHoi", "Số tiền chậm nộp (thu hồi hoàn)", "SO")),
                         [OrderedDict(ngayChamNopDen="2026-02-10", soNgayChamNop=21, tienChamNop=63000, soTienThuHoiHoan=0, quyetDinhHoanSo="",
                                      quyetDinhHoanNgay=None, cqtBanHanh="", tinhTp="", xaPhuong="", lenhHoanSo="", lenhHoanNgay=None,
                                      soNgayNhanTienHoan=0, tienChamNopThuHoi=0)]))
    tr_tm = truong(("tenTieuMuc", "Tên tiểu mục", "CHU"), ("soTien", "Số tiền tăng/giảm", "SO"))
    ds.append(nguon_json("thue.toKhaiBoSung.phaiNop", "01/KHBS — A.I.1 số thuế phải nộp điều chỉnh", "NHIEU_DONG", tr_tm,
                         [OrderedDict(tenTieuMuc="1701 - Thuế giá trị gia tăng hàng sản xuất, kinh doanh trong nước", soTien=10000000)]))
    ds.append(nguon_json("thue.toKhaiBoSung.phanBo", "01/KHBS — A.I.2 phân bổ điều chỉnh", "NHIEU_DONG",
                         truong(("tenDonVi", "Tên đơn vị/địa bàn", "CHU"), ("mst", "MST/Mã ĐĐKD", "CHU"), ("huyen", "Huyện", "CHU"), ("tinh", "Tỉnh", "CHU"),
                                ("cqt", "CQT quản lý địa bàn", "CHU"), ("soTien", "Số tiền điều chỉnh", "SO")),
                         [OrderedDict(tenDonVi="Nhà máy Cần Thơ (Demo)", mst="0100101114-001", huyen="", tinh="Thành phố Cần Thơ", cqt="Chi cục Thuế Doanh nghiệp lớn", soTien=100000)]))
    ds.append(nguon_json("thue.toKhaiBoSung.khauTru", "01/KHBS — A.II số thuế khấu trừ điều chỉnh", "NHIEU_DONG", tr_tm,
                         [OrderedDict(tenTieuMuc="Thuế GTGT còn được khấu trừ chuyển kỳ sau", soTien=-2500000)]))
    ds.append(nguon_json("thue.toKhaiBoSung.deNghiHoan", "01/KHBS — A.III số thuế đề nghị hoàn điều chỉnh", "NHIEU_DONG", tr_tm,
                         [OrderedDict(tenTieuMuc="Thuế GTGT đề nghị hoàn", soTien=0)]))

    # Bản giải trình
    ds.append(nguon_json("thue.giaiTrinhKhbs.header", "01-1/KHBS — tổng cộng & tài liệu kèm theo", "MOT_DONG",
                         truong(("tongPhaiNop", "[07] Tổng cộng phải nộp", "SO"), ("tongKhauTru", "[08] Tổng cộng khấu trừ", "SO"),
                                ("tongDeNghiHoan", "[09] Tổng cộng đề nghị hoàn", "SO"), ("taiLieuKemTheo", "Tài liệu kèm theo", "CHU")),
                         [OrderedDict(tongPhaiNop=10000000, tongKhauTru=-2500000, tongDeNghiHoan=0, taiLieuKemTheo="1. Hoá đơn điều chỉnh số 0001234 ngày 05/01/2026\n2. Biên bản điều chỉnh")]))
    ds.append(nguon_json("thue.giaiTrinhKhbs.dong", "01-1/KHBS — dòng giải trình", "NHIEU_DONG",
                         truong(("stt", "STT (1, 1.1…)", "CHU"), ("tenChiTieu", "Tên chỉ tiêu điều chỉnh", "CHU"), ("maChiTieu", "Mã số chỉ tiêu", "CHU"),
                                ("soDaKeKhai", "Số đã kê khai", "SO"), ("soDieuChinh", "Số điều chỉnh", "SO"), ("chenhLech", "Chênh lệch", "SO"),
                                ("dieuChinhNghiaVu", "Điều chỉnh tăng/giảm nghĩa vụ thuế", "SO"), ("lyDo", "Lý do", "CHU")),
                         [OrderedDict(stt="1", tenChiTieu="Tờ khai 01/GTGT", maChiTieu="", soDaKeKhai=None, soDieuChinh=None, chenhLech=None, dieuChinhNghiaVu=None, lyDo=""),
                          OrderedDict(stt="1.1", tenChiTieu="Hàng hóa, dịch vụ bán ra chịu thuế suất 10%", maChiTieu="[32]", soDaKeKhai=21761982091, soDieuChinh=21861982091, chenhLech=100000000, dieuChinhNghiaVu=0, lyDo="Bổ sung hoá đơn bỏ sót"),
                          OrderedDict(stt="1.2", tenChiTieu="Thuế GTGT của HHDV bán ra chịu thuế suất 10%", maChiTieu="[33]", soDaKeKhai=2176198209, soDieuChinh=2186198209, chenhLech=10000000, dieuChinhNghiaVu=10000000, lyDo="")]))

    ds.append(nguon_json("thue.pl015.dong", "01-5/GTGT — chứng từ nộp thuế ngoại tỉnh", "NHIEU_DONG",
                         truong(("soChungTu", "Số chứng từ nộp tiền", "CHU"), ("ngayNop", "Ngày nộp thuế", "NGAY"), ("noiNop", "Nơi nộp (KBNN)", "CHU"),
                                ("cqtQuanLy", "CQT quản lý hoạt động", "CHU"), ("soTien", "Số tiền thuế đã nộp", "SO")),
                         [OrderedDict(soChungTu="GNT-00012", ngayNop="2025-12-10", noiNop="KBNN Cần Thơ", cqtQuanLy="Chi cục Thuế khu vực XVIII", soTien=15000000)]))
    ds.append(nguon_json("thue.pl017.dong", "01-7/GTGT — công trình liên tỉnh", "NHIEU_DONG",
                         truong(("tenCongTrinh", "Tên công trình", "CHU"), ("doanhThu", "Doanh thu", "SO"), ("cqtDiaPhuong", "CQT địa phương quản lý", "CHU"),
                                ("tyLe", "Tỷ lệ phân bổ (%)", "SO"), ("soThue", "Số thuế GTGT phải nộp", "SO")),
                         [OrderedDict(tenCongTrinh="Cầu vượt sông Hậu (Demo)", doanhThu=5000000000, cqtDiaPhuong="Chi cục Thuế khu vực XVIII", tyLe=1, soThue=50000000)]))
    ds.append(nguon_json("thue.pl406.dong", "PL giảm thuế NQ 406 — dòng", "NHIEU_DONG",
                         truong(("tenHhdv", "Tên hàng hoá, dịch vụ", "CHU"), ("giaTri", "Giá trị chưa thuế", "SO"), ("thueSuat", "Thuế suất theo quy định %", "SO"),
                                ("thueSuatSauGiam", "Thuế suất sau giảm %", "SO"), ("thueDuocGiam", "Thuế GTGT được giảm", "SO")),
                         [OrderedDict(tenHhdv="Dịch vụ lưu trú (Demo)", giaTri=80000000, thueSuat=10, thueSuatSauGiam=7, thueDuocGiam=2400000)]))
    return ds


def ghi(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    wb = load_workbook(FILE_XLSX)
    for cf, ws in zip(CONFIG, wb.worksheets):
        dn = dung_dinh_nghia(ws, cf)
        seed = OrderedDict(ma=cf["ma"], ten=cf["ten"], nhom=NHOM_THUE, moTa=cf.get("moTa", ""), hieuLucTu=NGAY_HIEU_LUC, dinhNghia=dn)
        ghi(os.path.join(THU_MUC_SEED, cf["ma"] + ".json"), seed)
        so_dong = sum(1 if d["loai"] != "NHOM" else len(d["dau"]) + len(d["than"]) + len(d["cuoi"]) for d in dn["dong"])
        print("seed %-28s cột=%2d dòng=%2d kiểuDáng=%2d rộng=%.0fpt" % (cf["ma"], len(dn["cot"]), so_dong, len(dn["kieuDang"]), sum(c["rong"] for c in dn["cot"])))
    for n in sinh_nguon(wb):
        ghi(os.path.join(THU_MUC_NGUON, n["ma"] + ".json"), n)
        print("nguồn %-30s %s dòng=%d" % (n["ma"], n["dangDong"], len(n["duLieuMau"])))


if __name__ == "__main__":
    main()
