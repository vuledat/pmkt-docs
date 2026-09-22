#!/usr/bin/env bash
# Đồng bộ snapshot catalog + fixture mẫu in sinh từ cell-app sang các nơi tiêu thụ (D3 · D8).
#
#   cd cell-app && ./gradlew unitTest --tests 'vn.vtt.pmkt.cell.mau_in.XuatCatalogMauInTest'   # sinh build/mau-in/*.json
#   bash docs/doing/mau-in-chung-tu/sync-catalog.sh                                              # chép đi
#
# Nguồn sự thật là code Java (MoTaMauIn của từng provider). File JSON ở đích chỉ là bản chép — sửa ở đích là mất.
set -euo pipefail

GOC="$(cd "$(dirname "$0")/../../.." && pwd)"
NGUON="$GOC/cell-app/build/mau-in"

if [ ! -f "$NGUON/catalog.json" ]; then
  echo "Chưa có $NGUON/catalog.json — chạy XuatCatalogMauInTest trong cell-app trước." >&2
  exit 1
fi

# 1. Tài liệu / fixture vàng dùng chung.
mkdir -p "$GOC/docs/doing/mau-in-chung-tu/fixtures"
cp "$NGUON"/*.json "$GOC/docs/doing/mau-in-chung-tu/fixtures/"

# 2. Snapshot cho super-admin-service (catalog của mọi loại đã có provider).
if [ -d "$GOC/super-admin-service/src/main/resources" ]; then
  mkdir -p "$GOC/super-admin-service/src/main/resources/mau-in"
  cp "$NGUON/catalog.json" "$GOC/super-admin-service/src/main/resources/mau-in/catalog.json"
fi

# 3. Fixture cho test engine FE (client và bản sao ở client-admin) — chỉ các file theo loại (mdv.*, bhh.*, …).
for app in client client-admin; do
  dich="$GOC/$app/src/base/domainKit/mauIn/test/fixtures"
  if [ -d "$dich" ]; then
    find "$NGUON" -maxdepth 1 -name '*.json' ! -name 'catalog.json' -exec cp {} "$dich/" \;
  fi
done

echo "Đã đồng bộ từ $NGUON:"
ls -1 "$NGUON"/*.json | sed 's|.*/|  |'
