#!/usr/bin/env bash
# 打包要上傳到廠商伺服器的檔案。
# 只包網站本體，不包 build.py、tools/、README、Cloudflare 專用檔與 git。
set -euo pipefail
cd "$(dirname "$0")/.."
python3 build.py >/dev/null
out="../易向官網_上傳用_$(date +%Y%m%d).zip"
rm -f "$out"
zip -qr "$out" . \
  -x ".git/*" ".gitignore" "build.py" "README.md" "tools/*" \
     "_headers" "_redirects" ".nojekyll" "*.DS_Store" "*.zip"
echo "已打包：$out（$(du -h "$out" | cut -f1)）"
unzip -l "$out" | tail -1
