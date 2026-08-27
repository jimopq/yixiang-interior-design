#!/usr/bin/env bash
# 易向室內設計 — 產生網頁用的多尺寸圖片
#
# 用法：把新作品的原圖（越大越好）丟進 assets/works/ 或 assets/case/，
#       然後在專案根目錄執行：
#
#   bash tools/make-thumbs.sh
#
# 腳本會把主目錄的圖統一縮到 1600px（給燈箱用），
# 並產生 400 / 800 / 1200 三階縮圖給格線使用。
# 已存在且較新的縮圖會跳過，重跑很快。

set -euo pipefail
cd "$(dirname "$0")/.."

gen () {                     # gen <目錄> <階梯...>
  local dir=$1; shift
  [ -d "$dir" ] || return 0
  echo "── $dir"
  # 主目錄統一 1600px（sips -Z 只縮不放大）
  for f in "$dir"/*.jpg; do
    [ -e "$f" ] || continue
    w=$(sips -g pixelWidth "$f" | awk -F': ' '/pixelWidth/{print $2}')
    if [ "${w:-0}" -gt 1600 ]; then
      sips -Z 1600 -s formatOptions 74 "$f" --out "$f" >/dev/null
      echo "   縮至 1600  $(basename "$f")"
    fi
  done
  # 各階縮圖
  for size in "$@"; do
    mkdir -p "$dir/$size"
    local q=70
    [ "$size" -le 400 ] && q=66
    [ "$size" -ge 1200 ] && q=72
    for f in "$dir"/*.jpg; do
      [ -e "$f" ] || continue
      local out="$dir/$size/$(basename "$f")"
      if [ ! -e "$out" ] || [ "$f" -nt "$out" ]; then
        sips -Z "$size" -s formatOptions "$q" "$f" --out "$out" >/dev/null
      fi
    done
    echo "   $size px  →  $(ls "$dir/$size" | wc -l | tr -d ' ') 檔  $(du -sh "$dir/$size" | cut -f1)"
  done
}

gen assets/works 400 800 1200
gen assets/case  800 1200
gen assets/hero  900 1600

echo
echo "完成。別忘了把新作品加進 data/works.json。"
