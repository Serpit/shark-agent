# 数据源:Google Analytics 4

> **定位**:自有站的**站内行为真值**——用户/会话/浏览量/渠道构成/落地页。
> 与 [GSC](gsc.md) 互补:GSC 管「搜索结果页发生了什么」(曝光、点击、排名),
> GA4 管「点进来之后发生了什么」(停留、路径、渠道)。两者的点击数**天然对不上**,见下方陷阱。
>
> **信任等级**:自有真值,与 GSC 同级。第三方估算冲突时以这两个为准。
> **工具**:[`scripts/ga4.py`](../../scripts/ga4.py),零依赖纯 stdlib。
> **凭证**:与 GSC **共用** `~/.config/shark-agent/google.json`,不需要单独授权。

## 使用前提(硬约束)

同 [gsc.md](gsc.md#使用前提硬约束):**拉数前先回答这次查询会落到哪个具体动作**,答不上来就不查。
GA4 的仪表盘感尤其强,是「再看看数据」这种心理卡点([axioms.md](../axioms.md) 公理 6)的高发区。

**日报是这条约束的合规出口**:它不是"想看就看",是固定节奏推送、看完就走,不占用决策时间。

## 一次性配置

授权由 `gsc.py auth` 统一完成——scope 里已经带上了 `analytics.readonly`
(见 [`scripts/_google.py`](../../scripts/_google.py) 的 `SCOPES`)。除此之外只需两步:

1. 在 GCP 项目 `shark-gsc` 里启用两个 API:
   - **Google Analytics Data API**(跑报表)
   - **Google Analytics Admin API**(列 property,`ga4.py props` 靠它)
2. 重跑授权(scope 变了,旧 token 不带 Analytics 权限):

```bash
python3 scripts/gsc.py auth --client-secret-file ~/Downloads/client_secret_xxx.json
```

验证:

```bash
python3 scripts/ga4.py props
```

返回的 `property_id` 就是后续所有命令的 `<prop>` 参数(纯数字,不是 `G-XXXXXXX` 那个测量 ID)。

> ⚠️ **测量 ID ≠ property ID**。网页埋点里的 `G-ABCD123456` 是 data stream 的测量 ID,
> API 用的是 property 的数字 ID(如 `412345678`)。填错会报 404。

## 常用查询

```bash
python3 scripts/ga4.py props                                  # 列出所有可访问 property
python3 scripts/ga4.py totals <prop> --days 7                 # 汇总:活跃用户/新用户/会话/浏览量
python3 scripts/ga4.py breakdown <prop> --days 7              # 默认按渠道(sessionDefaultChannelGroup)
python3 scripts/ga4.py breakdown <prop> --dimension country   # 换任意维度
python3 scripts/ga4.py pages <prop> --days 7                  # 页面级(pagePath)
```

`--metrics` 逗号分隔可换指标,`--format csv|json` 可导出。

常用维度:`sessionDefaultChannelGroup`(渠道)、`pagePath`、`country`、`deviceCategory`、
`sessionSource` / `sessionMedium`、`landingPage`。
常用指标:`activeUsers`、`newUsers`、`sessions`、`screenPageViews`、
`averageSessionDuration`、`bounceRate`、`engagementRate`。

## 陷阱

1. **GA4 的「Organic Search 会话」和 GSC 的「点击」永远对不上**,通常 GA4 更低。
   原因:广告拦截器 / 未同意 cookie / JS 没加载完就跳出 / GSC 把同一次搜索的多次点击算多次。
   **差 20-40% 是正常的**,不要当成埋点坏了。哪个是"真值"取决于问题:
   问"Google 给了多少流量"看 GSC,问"进来的人干了什么"看 GA4。
2. **没有 3 天延迟,但「今天」不完整** —— 脚本默认窗口结束日 = 昨天(`DATA_LAG_DAYS = 1`)。
   GA4 数据基本准实时,但当天仍在累积,直接查会看起来像腰斩。
3. **低流量站会触发数据阈值(data thresholding)** —— 当某个维度组合的用户数太少时,
   GA4 会直接**隐去整行**以防身份反推。partfit3d 这种量级下,细维度拆分经常"少了几行",
   加起来对不上总数。这不是 bug,是设计。想拿全量就少拆维度。
4. **property 没数据时 API 返回空 rows,不报错** —— `totals()` 会给全 0。
   看到全 0 先确认是"真没人来"还是"埋点没生效",别直接下结论。
5. **配额**:Data API 每 property 每天 20 万次 token 消耗、每小时 4 万。日报这种用量远够。

## 结果往哪写

| 拉到什么 | 回写位置 |
|---|---|
| 某次完整的站点行为快照 | [experiments.md](../experiments.md) 对应实验的「结果记录」 |
| 渠道构成变化(如 Organic 占比跃迁) | 同上,标注拉取日期与窗口 |
| 由数据引出的具体动作 | [todos.md](../todos.md) |
| 反复出现的判断规律 | [principles.md](../principles.md) 或 `methods/` |

**不要**把原始表格整片粘进 memory —— 只写结论 + 拉取日期 + 窗口。
