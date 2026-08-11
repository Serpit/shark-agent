#!/bin/bash
# 把日报注册成 macOS launchd 定时任务(每天 10:00)。
#
#   bash scripts/install_daily_report.sh          # 安装 / 覆盖安装
#   bash scripts/install_daily_report.sh --at 9:30
#   bash scripts/install_daily_report.sh --uninstall
#
# 为什么用 launchd 而不是 cron:cron 在 Mac 睡眠期间错过的任务**不会补跑**,
# launchd 的 StartCalendarInterval 会在唤醒后立刻补一次。笔记本合盖是常态,这个差别是决定性的。
set -euo pipefail

# `pwd -P` 而不是 `pwd`:仓库在 ~/Desktop/space 下有一条符号链接,
# 走逻辑路径会把 Desktop 路径写进 plist,而 launchd 读不了 ~/Desktop(TCC 保护)。
# 必须解析到物理路径,见 memory/sources/daily-report.md「已知陷阱 3」。
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
LABEL="com.shark-agent.daily-report"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG_DIR="$HOME/Library/Logs/shark-agent"
HOUR=10
MINUTE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --uninstall)
      launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
      rm -f "$PLIST"
      echo "✅ 已卸载 $LABEL"
      exit 0
      ;;
    --at)
      HOUR="${2%%:*}"; MINUTE="${2##*:}"; shift 2 ;;
    *)
      echo "未知参数:$1" >&2; exit 1 ;;
  esac
done

mkdir -p "$LOG_DIR" "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$REPO/scripts/report_daily.py</string>
  </array>
  <key>WorkingDirectory</key><string>$REPO</string>
  <key>EnvironmentVariables</key>
  <dict>
    <!-- launchd 不继承登录 shell 的 PATH;lark-cli 在 /opt/homebrew/bin 下,必须显式给。 -->
    <key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>$HOUR</integer>
    <key>Minute</key><integer>$MINUTE</integer>
  </dict>
  <key>StandardOutPath</key><string>$LOG_DIR/daily-report.log</string>
  <key>StandardErrorPath</key><string>$LOG_DIR/daily-report.err.log</string>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
PLIST_EOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

printf '✅ 已注册 %s,每天 %02d:%02d 触发\n' "$LABEL" "$HOUR" "$MINUTE"
echo "   plist: $PLIST"
echo "   日志:  $LOG_DIR/daily-report.log"
echo
echo "立即试跑一次(不等到明天):"
echo "  launchctl kickstart -p gui/$(id -u)/$LABEL"
