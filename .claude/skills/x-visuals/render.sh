#!/usr/bin/env bash
# 把推文配图 HTML 渲染成 2x PNG(1600x900 画布 → 3200x1800 输出)
# 用法: bash .claude/skills/x-visuals/render.sh drafts/x/2026-08-12-foo-hero.html [更多.html ...]
# 零依赖,只要本机装了 Chrome。输出为同目录同名 .png
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "找不到 Chrome: $CHROME" >&2; exit 1; }
[ $# -ge 1 ] || { echo "用法: render.sh <file.html> [file2.html ...]" >&2; exit 1; }

for html in "$@"; do
  [ -f "$html" ] || { echo "跳过(不存在): $html" >&2; continue; }
  abs="$(cd "$(dirname "$html")" && pwd)/$(basename "$html")"
  png="${abs%.html}.png"
  "$CHROME" --headless --disable-gpu \
    --force-device-scale-factor=2 --window-size=1600,900 \
    --screenshot="$png" "file://$abs" 2>/dev/null
  echo "✓ $png"
done

echo
echo "下一步(strict): Read 一次 PNG 肉眼确认,重点看底部有没有被裁、中文断句是否难看。"
