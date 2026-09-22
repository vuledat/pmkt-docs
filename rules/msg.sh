#!/bin/sh
# msg.sh — doi chieu 6.messages.md cua PYC voi ma thong bao that trong code.
#
#   ./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang           # ca FE lan BE
#   ./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang fe        # chi quet client/src
#   ./docs/rules/msg.sh pmkt-docs/ba/PMKT-E-06194_ChungTuBanHang be        # chi quet cell-app/src
#   ./docs/rules/msg.sh <PYC> fe --missing                                 # chi in dong chua dat
#
# Vi sao: BR + luat 2 cua CLAUDE.md bat text hien thi phai NGUYEN VAN tai lieu. Dien dat lai mot chu
# la lech nghiep vu. Script so tung ky tu (sau khi chuan hoa {{x}} -> {x} va khoang trang).
#
# Trang thai:
#   OK       ma co trong code, noi dung khop nguyen van
#   LECH     ma co trong code nhung chu khac tai lieu   -> phai sua code theo tai lieu
#   CHUA-DAT ma chi duoc nhac trong comment, chua thanh gia tri i18n / hang so
#   THIEU    khong thay ma trong code

PYC="$1"
[ -n "$PYC" ] || { echo "Dung: ./docs/rules/msg.sh <thu-muc-PYC> [fe|be] [--missing]" >&2; exit 1; }
case "$PYC" in *Phase_2*) echo "TU CHOI: PYC nam trong Phase_2 — vung dong bang." >&2; exit 2;; esac

MSGFILE=$(find "$PYC" -maxdepth 1 -iname "*messages*.md" | head -1)
[ -n "$MSGFILE" ] || { echo "Khong tim thay file messages trong $PYC" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LAYER="$(printf '%s' "${2:-all}" | tr 'A-Z' 'a-z')"
case "$LAYER" in --missing) LAYER=all; ONLY_MISSING=1;; esac
[ "$3" = "--missing" ] && ONLY_MISSING=1
case "$LAYER" in
  fe)  SCAN="$ROOT/client/src" ;;
  be)  SCAN="$ROOT/cell-app/src" ;;
  all) SCAN="$ROOT/client/src $ROOT/cell-app/src" ;;
  *)   echo "Tang phai la be | fe" >&2; exit 1 ;;
esac

CODE=$(mktemp); STAT=$(mktemp); trap 'rm -f "$CODE" "$STAT"' EXIT
for d in $SCAN; do
  [ -d "$d" ] || continue
  grep -rn --exclude-dir=node_modules --exclude-dir=build --exclude-dir=dist \
    --exclude-dir=legacy --exclude-dir=master_data --exclude-dir=Phase_2 \
    "MSG_PMKT-E-[0-9]*_[0-9]*" "$d" 2>/dev/null
done > "$CODE"

norm() { printf '%s' "$1" | sed 's/{{ *\([A-Za-z0-9_]*\) *}}/{\1}/g; s/  */ /g; s/^ //; s/ $//'; }

printf "%-26s %-9s %s\n" "MA MESSAGE" "TRANG" "GHI CHU"
printf -- "--------------------------------------------------------------------------------\n"

awk -F'|' '/^\| *MSG_PMKT-E-[0-9]+_[0-9]+/ {
    gsub(/^ +| +$/, "", $2); gsub(/^ +| +$/, "", $3); print $2 "\t" $3
  }' "$MSGFILE" | while IFS="$(printf '\t')" read -r ID TXT; do
    [ -n "$ID" ] || continue
    LINES=$(grep -F "$ID" "$CODE")
    if [ -z "$LINES" ]; then
      ST="THIEU"; NOTE="chua xuat hien trong code"
    else
      # dong dinh nghia gia tri: 'MSG_x': 'noi dung'  hoac  = "MSG_x";
      # CHI so nguyen van voi vi.ts — en.ts la ban dich, khong phai nguon su that.
      VI=$(printf '%s\n' "$LINES" | grep '/vi\.ts:')
      VAL=$(printf '%s\n' "$VI" | sed -n "s/.*['\"]$ID['\"] *: *['\"]\(.*\)['\"] *,\{0,1\} *$/\1/p" | head -1)
      # Prettier xuong dong khi chuoi dai: khoa o mot dong, gia tri o DONG NGAY SAU.
      #   'MSG_x':
      #     'noi dung dai...',
      # Khong xu ly ca nay thi bao THIEU-VI oan cho moi message dai hon printWidth.
      if [ -z "$VAL" ]; then
        VIHIT=$(printf '%s\n' "$VI" | sed -n "/['\"]$ID['\"] *: *$/p" | head -1)
        if [ -n "$VIHIT" ]; then
          VIFILE=${VIHIT%%:*}; VIREST=${VIHIT#*:}; VILINE=${VIREST%%:*}
          case "$VILINE" in
            *[!0-9]*|'') : ;;
            *) VAL=$(sed -n "$((VILINE + 1))p" "$VIFILE" \
                   | sed -n "s/^ *['\"]\(.*\)['\"] *,\{0,1\} *$/\1/p") ;;
          esac
        fi
      fi
      EN=$(printf '%s\n' "$LINES" | grep -c '/en\.ts:')
      DEF=$(printf '%s\n' "$LINES" | grep -c "= *\"$ID\"")
      if [ -z "$VAL" ] && [ "$EN" -gt 0 ] && [ "$DEF" -eq 0 ]; then
        ST="THIEU-VI"; NOTE="co key trong en.ts nhung khong co trong vi.ts (CLAUDE.md luat 2: phai co CA HAI)"
      elif [ -n "$VAL" ]; then
        if [ "$(norm "$VAL")" = "$(norm "$TXT")" ]; then
          ST="OK"; NOTE="$(printf '%s\n' "$LINES" | head -1 | cut -d: -f1 | sed "s|$ROOT/||")"
        else
          ST="LECH"; NOTE="tai lieu: \"$TXT\" | code: \"$VAL\""
        fi
      elif [ "$DEF" -gt 0 ]; then
        ST="OK"; NOTE="hang so BE: $(printf '%s\n' "$LINES" | grep "= *\"$ID\"" | head -1 | cut -d: -f1 | sed "s|$ROOT/||")"
      else
        ST="CHUA-DAT"; NOTE="chi nam trong comment/javadoc, chua thanh gia tri"
      fi
    fi
    [ -z "$ONLY_MISSING" ] || [ "$ST" != "OK" ] && printf "%-26s %-9s %s\n" "$ID" "$ST" "$NOTE"
    echo "$ST" >> "$STAT"
  done

printf -- "--------------------------------------------------------------------------------\n"
T=$(wc -l < "$STAT" | tr -d ' ')
printf "Tong %s message (tang=%s): OK %s · LECH %s · THIEU-VI %s · CHUA-DAT %s · THIEU %s\n" \
  "$T" "$LAYER" "$(grep -c '^OK$' "$STAT")" "$(grep -c '^LECH$' "$STAT")" \
  "$(grep -c '^THIEU-VI$' "$STAT")" "$(grep -c '^CHUA-DAT$' "$STAT")" "$(grep -c '^THIEU$' "$STAT")"
[ "$(grep -c '^LECH$' "$STAT")" -gt 0 ] && { printf "\nCO MESSAGE LECH NGUYEN VAN — phai sua code theo tai lieu (CLAUDE.md luat 2).\n"; exit 1; }
exit 0
