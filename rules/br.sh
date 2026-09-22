#!/bin/sh
# br.sh — in ra ĐÚNG các mục BR cần dùng từ pmkt-docs/ba/Common/business_rules.md
#
#   ./docs/rules/br.sh 7 30 39        -> in BR7, BR30, BR39
#   ./docs/rules/br.sh BR7 BR30       -> chấp nhận cả tiền tố "BR"
#   ./docs/rules/br.sh --list         -> in mục lục (số + tiêu đề), ~2 KB
#
# Vì sao có script này: business_rules.md nặng ~183 KB (~50k token). Đọc cả file
# trước mỗi tác vụ là nguyên nhân chính khiến phiên làm việc chậm. Script trích
# theo heading nên KHÔNG lệch khi file BR được BA sửa (không hardcode số dòng).

# PHAM VI: repo dang lam PHASE 1. SRC duoi day co y tro vao ban Phase 1 (BR1..BR49).
# Ban 'pmkt-docs/ba/Phase_2/Common/business_rules.md' (50 BR, them BR50 Chi nhanh) la VUNG DONG BANG
# — KHONG doc, KHONG tro sang. Doi Phase thi sua dung dong SRC nay, dung sua rai rac.
SRC="$(cd "$(dirname "$0")/../.." && pwd)/pmkt-docs/ba/Common/business_rules.md"
[ -f "$SRC" ] || { echo "Khong tim thay $SRC" >&2; exit 1; }
case "$SRC" in *Phase_2*) echo "br.sh dang tro vao tai lieu Phase 2 — sai pham vi, dung lai." >&2; exit 2;; esac

if [ $# -eq 0 ] || [ "$1" = "--list" ] || [ "$1" = "-l" ]; then
  grep -n '^## BR' "$SRC" | sed 's/^[0-9]*:## /  /'
  exit 0
fi

for raw in "$@"; do
  n=$(printf '%s' "$raw" | sed 's/^[Bb][Rr]//; s/^0*//')
  awk -v n="$n" '
    BEGIN { on = 0; found = 0 }
    /^## BR/ {
      # tach so BR khoi heading, bo so 0 dau va dau cham
      h = $0
      sub(/^## [Bb][Rr]0*/, "", h)
      sub(/[^0-9].*$/, "", h)
      if (h == n) { on = 1; found = 1; print; next }
      else if (on) { on = 0 }
    }
    on { print }
    END { if (!found) print "  (khong co BR" n " trong business_rules.md)" > "/dev/stderr" }
  ' "$SRC"
  echo
done
