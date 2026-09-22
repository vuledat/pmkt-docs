#!/bin/sh
# scr.sh — doc dac ta man hinh (SCR_*.md) THEO MUC, khong nuot ca file.
#
#   ./docs/rules/scr.sh <file.md> --list              muc luc heading + so dong (mac dinh)
#   ./docs/rules/scr.sh <file.md> --sec "<tu khoa>"   trich cac muc co heading khop (khong phan biet hoa thuong)
#   ./docs/rules/scr.sh <file.md> --lines 400 700     in dung dai dong 400..700 (co so dong)
#   ./docs/rules/scr.sh <file.md> --links             liet ke link cheo ../.. phai mo them
#   ./docs/rules/scr.sh <file.md> --stat              so dong / KB / so lan nhac BR / so link cheo
#   ./docs/rules/scr.sh <file.md> --br                liet ke cac BRxx duoc nhac, kem so dong
#
# Vi sao co script nay: SCR_CTBH_ThemMoi.md = 192 KB / 1630 dong / 291 lan nhac BR / 16 link cheo.
# Read ca file thi tran context va van rung luat o nua sau. Doc theo muc + ghi lai dai dong da doc
# la cach duy nhat chung minh duoc do phu (xem 00-source-map.md cua /audit-spec).

usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

SRC="$1"
[ -n "$SRC" ] || usage 1
[ -f "$SRC" ] || { echo "Khong tim thay file: $SRC" >&2; exit 1; }
case "$SRC" in
  *Phase_2*) echo "TU CHOI: '$SRC' nam trong pmkt-docs/ba/Phase_2/** — vung dong bang, repo dang lam Phase 1." >&2; exit 2;;
esac
shift

MODE="${1:---list}"
shift 2>/dev/null

case "$MODE" in
  --list|-l)
    awk 'BEGIN{n=0}
      /^#{1,6} / { printf "%6d  %s\n", NR, $0; n++ }
      END { if (n==0) print "  (file khong co heading markdown)" }' "$SRC"
    printf "\n  -> tong %s dong. Trich mot muc: --sec \"<tu khoa>\" | --lines A B\n" "$(wc -l < "$SRC" | tr -d ' ')"
    ;;

  --sec|-s)
    PAT="$1"
    [ -n "$PAT" ] || { echo "Thieu tu khoa cho --sec" >&2; exit 1; }
    awk -v pat="$PAT" '
      BEGIN { IGNORECASE=1; on=0; lvl=0; found=0 }
      function level(s,   i) { i=0; while (substr(s,i+1,1)=="#") i++; return i }
      /^#{1,6} / {
        L = level($0)
        if (on && L <= lvl) { on = 0 }
        if (!on && index(tolower($0), tolower(pat)) > 0) {
          on = 1; lvl = L; found = 1
          printf "\n===== %s  (dong %d) =====\n", $0, NR
          next
        }
      }
      on { printf "%6d| %s\n", NR, $0 }
      END { if (!found) print "  (khong co heading nao chua \"" pat "\")" > "/dev/stderr" }
    ' "$SRC"
    ;;

  --lines|-n)
    A="$1"; B="$2"
    [ -n "$A" ] && [ -n "$B" ] || { echo "Dung: --lines <tu> <den>" >&2; exit 1; }
    awk -v a="$A" -v b="$B" 'NR>=a && NR<=b { printf "%6d| %s\n", NR, $0 }' "$SRC"
    ;;

  --links)
    grep -n '](\.\./[^)]*)' "$SRC" \
      | sed 's/^\([0-9]*\):.*](\(\.\.[^)]*\)).*/\1\t\2/' \
      | sort -u -k2 \
      || echo "  (khong co link cheo)"
    echo
    echo "  -> MOI link tren la mot nguon nghiep vu KHAC file nay. /audit-spec phai liet ke het"
    echo "     trong 00-source-map.md va ghi ro da mo hay co y bo qua (kem ly do)."
    ;;

  --br)
    echo "== A. BR NOI BO MAN — dinh nghia ngay trong file nay (day la DANH SACH LUAT PHAI PHU) =="
    awk '/^#{2,6} +BR[0-9]+/ {
           tag = $2; sub(/:$/, "", tag)
           printf "%6d  %s\n", NR, $0
         }' "$SRC" | sed 's/  #\{2,6\} / /'
    echo
    echo "   so lan duoc bang/truong tham chieu toi:"
    grep -o 'BR[0-9]\{1,2\}' "$SRC" | sort | uniq -c | sort -rn | head -30 | sed 's/^/     /'
    echo
    echo "== B. BR CHUNG — tham chieu sang business_rules.md, doc bang br.sh =="
    grep -o 'business_rules\.md#br[0-9]*' "$SRC" | sed 's/.*#br//' | sort -nu | tr '\n' ' ' | sed 's/^/     ./docs/rules/br.sh /'
    echo
    echo
    echo "  ! BR01..BRnn o cot 'Tham chieu' cua bang la BR NOI BO MAN (phan A), KHONG phai BR chung."
    echo "    Muon doc dinh nghia mot BR noi bo: scr.sh <file> --sec \"BR18:\""
    ;;

  --stat)
    L=$(wc -l < "$SRC" | tr -d ' ')
    B=$(wc -c < "$SRC" | tr -d ' ')
    NBR=$(grep -c 'BR[0-9]' "$SRC")
    NLK=$(grep -o '](\.\./[^)]*)' "$SRC" | sort -u | wc -l | tr -d ' ')
    NHD=$(grep -c '^#\{1,6\} ' "$SRC")
    printf "  file      : %s\n" "$SRC"
    printf "  dong      : %s\n" "$L"
    printf "  kich thuoc: %s KB\n" "$((B / 1024))"
    printf "  heading   : %s\n" "$NHD"
    printf "  nhac BR   : %s lan\n" "$NBR"
    printf "  link cheo : %s\n" "$NLK"
    [ "$B" -gt 40960 ] && printf "\n  ! File > 40 KB — CAM Read ca file. Doc theo --sec / --lines va ghi dai dong da doc.\n"
    ;;

  -h|--help) usage 0 ;;
  *) echo "Khong hieu tuy chon: $MODE" >&2; usage 1 ;;
esac
