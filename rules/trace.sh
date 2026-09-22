#!/bin/sh
# trace.sh — cham DO PHU LUAT bang grep, khong bang tri nho.
#
#   ./docs/rules/trace.sh docs/doing/<slug>-spec            # ca BE lan FE
#   ./docs/rules/trace.sh docs/doing/<slug>-spec fe         # chi luat Tang = FE|CA HAI, quet client/src
#   ./docs/rules/trace.sh docs/doing/<slug>-spec be         # chi luat Tang = BE|CA HAI, quet cell-app/src
#   ./docs/rules/trace.sh docs/doing/<slug>-spec fe --missing   # chi in dong chua dat
#
# Nguyen ly: MOI luat R-xxx-nnn phai de lai chinh ma luat do trong code (comment/hang so/ten test).
# Khong tim thay ma luat = luat chua duoc hien thuc, bat ke code "trong co ve dung".
# Quy uoc dat ma luat: docs/rules/truy-vet-luat.md
#
# Ma trang thai in ra:
#   OK      co trong code VA co trong test
#   NO-TEST co trong code, THIEU test  -> luat P0 ma NO-TEST thi tinh la CHUA DAT
#   MISSING khong thay o dau ca        -> CHUA HIEN THUC
#   BLOCKED luat dang CHO (bi 01-conflict.md chan) -> DUNG code; neu thay trong code se bao VI PHAM

SPEC="$1"
[ -n "$SPEC" ] || { echo "Dung: ./docs/rules/trace.sh <thu-muc-spec> [be|fe] [--missing]" >&2; exit 1; }
case "$SPEC" in *Phase_2*) echo "TU CHOI: spec nam trong Phase_2." >&2; exit 2;; esac
RULES="$SPEC/02-rules.md"
[ -f "$RULES" ] || { echo "Khong tim thay $RULES" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LAYER="$(printf '%s' "${2:-all}" | tr 'A-Z' 'a-z')"
case "$LAYER" in --missing) LAYER=all; ONLY_MISSING=1;; esac
[ "$3" = "--missing" ] && ONLY_MISSING=1

case "$LAYER" in
  fe)  SCAN="$ROOT/client/src" ;;
  be)  SCAN="$ROOT/cell-app/src" ;;
  all) SCAN="$ROOT/client/src $ROOT/cell-app/src" ;;
  *)   echo "Tang phai la be | fe (hoac bo trong = ca hai)" >&2; exit 1 ;;
esac

# Bang chung: liet ke moi ma luat xuat hien trong code, kem duong dan.
HITS=$(mktemp); trap 'rm -f "$HITS"' EXIT
for d in $SCAN; do
  [ -d "$d" ] || continue
  if command -v rg >/dev/null 2>&1; then
    rg -o --no-heading --line-number \
       -g '!**/node_modules/**' -g '!**/build/**' -g '!**/dist/**' -g '!**/legacy/**' -g '!**/master_data/**' \
       '(R|INV)-[A-Z]+-[0-9]{3}|INV-[0-9]{3}' "$d" 2>/dev/null
  else
    grep -rnoE --exclude-dir=node_modules --exclude-dir=build --exclude-dir=dist \
      --exclude-dir=legacy --exclude-dir=master_data --exclude-dir=Phase_2 \
      '(R|INV)-[A-Z]+-[0-9]{3}|INV-[0-9]{3}' "$d" 2>/dev/null
  fi
done >> "$HITS"

is_test() { case "$1" in *"/test/"*|*.test.ts|*.test.tsx|*Test.java|*Tests.java|*"/src/test/"*) return 0;; esac; return 1; }

TOTAL=0; OK=0; NOTEST=0; MISSING=0; BLOCKED=0; VIOLATION=0

printf "%-14s %-7s %-4s %-8s %s\n" "LUAT" "TANG" "SEV" "TRANG" "BANG CHUNG"
printf -- "---------------------------------------------------------------------------------\n"

# Doc bang tong cua 02-rules.md: | ID | Ten | Tang | Sev | TT | Nguon |
awk -F'|' '/^\| *(R|INV)-/ {
    gsub(/^ +| +$/, "", $2); gsub(/^ +| +$/, "", $4); gsub(/^ +| +$/, "", $5); gsub(/^ +| +$/, "", $6)
    print $2 "\t" $4 "\t" $5 "\t" $6
  }' "$RULES" | while IFS="$(printf '\t')" read -r ID TANG SEV TT; do
    [ -n "$ID" ] || continue
    U_TANG=$(printf '%s' "$TANG" | tr 'a-z' 'A-Z')
    case "$LAYER" in
      fe) case "$U_TANG" in *FE*|*"CẢ HAI"*|*"CA HAI"*) ;; *) continue;; esac;;
      be) case "$U_TANG" in *BE*|*"CẢ HAI"*|*"CA HAI"*) ;; *) continue;; esac;;
    esac

    FOUND=$(grep -F "$ID" "$HITS" | cut -d: -f1 | sort -u)
    NF=$(printf '%s' "$FOUND" | grep -c . )
    HAS_TEST=0
    for f in $FOUND; do is_test "$f" && HAS_TEST=1; done

    case "$TT" in
      *CHỜ*|*CHO\ C*|*BLOCKED*)
        if [ "$NF" -gt 0 ]; then
          ST="VI-PHAM"; NOTE="luat dang CHO ma da co code: $(printf '%s' "$FOUND" | head -1)"
        else
          ST="BLOCKED"; NOTE="$TT — dung code cho toi khi 01-conflict.md chuyen CLOSED-BA"
        fi
        ;;
      *)
        if [ "$NF" -eq 0 ]; then ST="MISSING"; NOTE="khong thay ma luat trong code"
        elif [ "$HAS_TEST" -eq 0 ]; then ST="NO-TEST"; NOTE="$(printf '%s' "$FOUND" | head -1 | sed "s|$ROOT/||") (+$((NF-1)) noi)"
        else ST="OK"; NOTE="$(printf '%s' "$FOUND" | head -1 | sed "s|$ROOT/||") (+$((NF-1)) noi)"
        fi
        ;;
    esac

    if [ -z "$ONLY_MISSING" ] || [ "$ST" != "OK" ]; then
      printf "%-14s %-7s %-4s %-8s %s\n" "$ID" "$TANG" "$SEV" "$ST" "$NOTE"
    fi
    echo "$ST" >> "$HITS.stat"
  done

# Tong ket (chay ngoai subshell cua while nen dem qua file)
if [ -f "$HITS.stat" ]; then
  TOTAL=$(wc -l < "$HITS.stat" | tr -d ' ')
  OK=$(grep -c '^OK$' "$HITS.stat"); NOTEST=$(grep -c '^NO-TEST$' "$HITS.stat")
  MISSING=$(grep -c '^MISSING$' "$HITS.stat"); BLOCKED=$(grep -c '^BLOCKED$' "$HITS.stat")
  VIOLATION=$(grep -c '^VI-PHAM$' "$HITS.stat")
  rm -f "$HITS.stat"
  printf -- "---------------------------------------------------------------------------------\n"
  printf "Tong %s luat (tang=%s): OK %s · NO-TEST %s · MISSING %s · BLOCKED %s · VI-PHAM %s\n" \
    "$TOTAL" "$LAYER" "$OK" "$NOTEST" "$MISSING" "$BLOCKED" "$VIOLATION"
  if [ "$MISSING" -gt 0 ] || [ "$VIOLATION" -gt 0 ]; then
    printf "\nKET LUAN: CHUA DAT — con luat chua hien thuc hoac code cham vao luat bi chan.\n"
    exit 1
  fi
  if [ "$NOTEST" -gt 0 ]; then
    printf "\nKET LUAN: DAT MOT PHAN — con luat thieu test hoi quy.\n"
    exit 1
  fi
  printf "\nKET LUAN: DAT.\n"
fi
