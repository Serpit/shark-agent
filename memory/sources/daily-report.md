# 每日飞书日报

> **定位**:把 [GSC](gsc.md) + [GA4](ga4.md) 的关键数字**每天 10:00 主动推到飞书**,
> 让「看数据」从一个需要下决心的动作变成一条读完就走的消息。
>
> **为什么值得做**:这是 [axioms.md](../axioms.md) 公理 6 的合规出口。
> 主动去查数据天然会滑向「再调研一下」;定时推送反过来——**固定成本、固定时长、不占决策带宽**。
> 但它也有反面风险,见下方「这份日报不该变成什么」。

## 现状

| 项 | 状态 |
|---|---|
| 覆盖站点 | partfit3d(单站起步,验证跑通再扩) |
| 数据源 | GSC ✅ `https://partfit3d.com/` · GA4 ✅ property `547995195` |
| 投递 | 飞书机器人私聊,app `cli_a9658b283db91cd2`,走 `lark-cli` bot 身份 |
| 触发 | macOS launchd,每天 10:00 |
| 全链路验证 | 2026-08-11 launchd 实跑 exit 0,飞书收到卡片 |

> **GA4 property 一览**(`ga4.py props` 2026-08-11 拉取):
> `547995195` partfit3d · `546393618` FrameDrop。两个都在 `Serpit` 账号下。
> 其余三站(baxianfans / aidepixelate / easyframes)**没有 GA4 property**,扩站前要先建。

## 组成

| 文件 | 作用 |
|---|---|
| [`scripts/report_daily.py`](../../scripts/report_daily.py) | 取数 + 渲染飞书卡片 + 投递 |
| [`scripts/_google.py`](../../scripts/_google.py) | GSC/GA4 共享 OAuth,凭证 `~/.config/shark-agent/google.json` |
| [`scripts/install_daily_report.sh`](../../scripts/install_daily_report.sh) | 注册/卸载 launchd 定时任务 |
| `~/.config/shark-agent/report.json` | **投递目标与站点配置**(仓库外——本仓库是 public,飞书 open_id 不能入库) |
| [`scripts/report_targets.example.json`](../../scripts/report_targets.example.json) | 上面那份的模板 |

## 装 / 改 / 卸

```bash
bash scripts/install_daily_report.sh              # 装(每天 10:00)
bash scripts/install_daily_report.sh --at 9:30    # 改时间
bash scripts/install_daily_report.sh --uninstall  # 卸
```

试跑与排查:

```bash
python3 scripts/report_daily.py --dry-run                     # 只打印,不发飞书
python3 scripts/report_daily.py                               # 立刻发一条
launchctl kickstart -p gui/$(id -u)/com.shark-agent.daily-report   # 模拟定时触发
tail -50 ~/Library/Logs/shark-agent/daily-report.err.log      # 定时任务的报错在这
```

## 卡片内容

- **GSC 段**:最新可用日(T-3)的点击/曝光/CTR/均位;近 7 天 vs 前 7 天;近 7 天 Top 5 词
- **GA4 段**:昨日活跃用户/新用户/会话/浏览量 + 环比;近 7 天 vs 前 7 天;渠道构成;Top 5 页

## 设计约定(改脚本前先看这几条)

1. **永远发出一条消息。** 任何一段取数失败都降级成卡片里的告警行,不让整条日报静默消失——
   静默失败的定时任务等于没有定时任务,而且比没有更糟(你以为它在跑)。
2. **凭证失效单独成卡。** refresh_token 挂掉时发「⚠️ Google 凭证失效」而不是空数据,
   否则会被误读成"流量归零"。
3. **两个数据源的时间基准不同,卡片上必须标出来。** GSC 是 T-3,GA4 是 T-1。
   不标注就会出现"同一张卡上两个数字对不上"的困惑。
4. **用 launchd 不用 cron。** Mac 睡眠期间 cron 错过的任务不补跑,launchd 唤醒后会补。
   笔记本合盖是常态,这个差别是决定性的。
5. **配置在仓库外。** 本仓库 public,`report.json` 里有飞书 open_id,权限 600。

## 已知陷阱

1. **OAuth 测试模式 refresh_token 只活 7 天。** 定时任务会在第 8 天开始每天发一张
   「凭证失效」卡。根治办法是把 GCP OAuth 应用**发布到生产状态**(个人用途无需 Google 审核)。
2. **GSC 和 GA4 的数字对不上是正常的**,原因见 [ga4.md 陷阱 1](ga4.md#陷阱)。
   日报把它们并排放,是为了看**各自的趋势**,不是为了让它们相等。
3. **launchd 读不了 `~/Desktop` / `~/Documents` / `~/Downloads`(macOS TCC)。**
   2026-08-11 踩到:仓库原本在 `~/Desktop/space/shark-agent`,定时任务报
   `can't open file ... Operation not permitted`。**注意 `ls` 能过、`open()` 不能**——
   TCC 放行 stat 但拦截读取,用 `ls` 探测会误判成"权限没问题",白绕一圈。
   **已解法**:整个 `space` 目录移到 `~/space`,`~/Desktop/space` 留符号链接指回去。
   所以 `install_daily_report.sh` 必须用 `pwd -P` 解析**物理路径**——
   从符号链接那侧调用时,`pwd` 会把 Desktop 路径写回 plist,坑立刻复发。
   **这条对以后任何定时任务都成立**,不只是日报。
4. **站点刚起量时,同比变化率是假信号。** 2026-08-11 首跑撞到:partfit3d 的 GSC 数据
   **从 2026-07-31 才开始**,"前 7 天"只有 2 天有数,算出来曝光 `▲872%`——
   看着像爆发,实际只是基线缺了 5 天。GA4 更极端,前 7 天 0/7 天有数据。
   脚本已加保护:上期窗口不满 7 天有数据时**不给百分比**,改显示「基线不完整」+ 一行 ⚠️。
   **等两边都攒够 14 天(GSC 约 2026-08-14、GA4 看 property 建立日)之后,同比才开始有意义。**
5. **自己的访问会淹没 GA4(小流量站的头号数据污染源)。**
   2026-08-11 首跑:近 7 天 Direct 30 会话 vs Organic Search 2,
   `/admin/depixelate` 排到浏览量第 2 —— 用户确认是自己点的。
   日均 15 活跃用户的量级下,**自己点几次就能改变整张卡的结论**。
   脚本侧只做了 Top 页排除内部路径(`ga4_exclude_paths`),
   **会话数/用户数没法在脚本侧修**,必须在 GA4 侧过滤,否则这段一直不可信。
6. **机器不开机就不会推。** launchd 只在开机且登录后触发;
   连续几天没收到日报,先确认是任务坏了还是机器没开。

## 这份日报不该变成什么

日报的价值在**触发动作**,不在"我今天看过数据了"这个心理安慰。
连续 2 周日报没有引出任何 [todos.md](../todos.md) 条目 → 说明它已经退化成噪音,
要么改指标(现在这几个不驱动决策),要么降频到周报,要么直接砍掉。

按 [timeline.md](../timeline.md) 当前阶段,partfit3d 的核心矛盾是
**排名有了、点击和变现没跟上**——所以日报里最该盯的不是曝光总量,是 **CTR 和 GA 的会话数**。
