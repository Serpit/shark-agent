---
name: seo-competitor
description: 查关键词与竞品的外部数据——Semrush(月搜索量、KD、词族扩展、竞品流量)、SimilarWeb(站点流量估算、渠道构成)、Google Trends(趋势方向、上升相关词)。用 ego 浏览器驱动,不走 API。当对话涉及"这个词难做吗""KD 多少""搜索量够不够""词族有多大""竞品流量多少""对手站怎么样""这个词在涨还是在跌""趋势如何""SERP 头部是谁"时使用。也用于 search-engine-demand-discovery SOP 的 Step 2 三维探针。
---

# 关键词与竞品数据(Semrush / SimilarWeb / Google Trends)

**信任等级:第三方估算,不是真值。** 与 [`seo-data`](../seo-data/SKILL.md) 的 GSC 数据冲突时,**一律以 GSC 为准**。
落盘必须标注**工具名 + 拉取日期 + 「第三方估算」**。

> **⛔ 不使用 Ahrefs。** 面板里第一个「打开」按钮是 Ahrefs,**另计费,不要点**。
> KD / 搜索量一律走 Semrush。

## 入口(全部实测于 2026-08-09)

面板 `https://dash.3ue.co/zh-Hans/#/page/m/home`(账号 serpit,ego 已有登录态),
「我的订阅 → SEO Tools」下三张卡的「打开」按钮按 DOM 顺序 = `[0]Ahrefs(不用) [1]SimilarWeb [2]Semrush`。

**但不必走面板**——下面的直链已验证可用,省一跳:

### Semrush

```
关键词概览   https://sem.3ue.co/analytics/keywordoverview/?q=<词>&db=us
词族扩展     https://sem.3ue.co/analytics/keywordmagic/?q=<种子词>&db=us
竞品对比     https://sem.3ue.co/analytics/keywordgap/?db=us
```

- `db=us` 是美区,出海主线固定用这个
- **`sem.3ue.co/` 根路径是营销首页,不是应用**,必须直接进 `/analytics/...`
- 词族表(keywordmagic)列序已核对:`关键词 | 意图 | Relevance | 相关性 | **搜索量** | 趋势 | 潜在流量 | PKD% | **KD** | CPC | 竞争程度 | SF | 结果 | 已更新`
  → 取数用 **index 5 = 搜索量**、**index 9 = KD**

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('seo tools')
await openOrReuseTab('https://sem.3ue.co/analytics/keywordmagic/?q=3mf&db=us', { wait: true, timeout: 70 })
await wait(18)
cliLog(await js(`
  const rows=[...document.querySelectorAll('[role=row],tr')].map(tr=>
    [...tr.querySelectorAll('[role=cell],[role=gridcell],td')].map(td=>td.textContent.trim()).filter(Boolean)
  ).filter(r=>r.length>=3);
  return JSON.stringify(rows.slice(0,20));
`))
EOF
```

### SimilarWeb

```
站点总览  https://sim.3ue.co/#/digitalsuite/websiteanalysis/overview/website-performance/*/999/3m?webSource=Total&key=<域名>
```

`3m` 是 3 个月窗口。首次进 `sim.3ue.co/` 可能停在「激活设置页面」,直接用上面的直链可绕过。

### Google Trends

不在面板里,直接开,URL 完全参数化:

```
https://trends.google.com/trends/explore?date=today%2012-m&geo=US&q=<词1>,<词2>&hl=en-US
```

- 首次访问有 cookie 横幅,点掉 `OK, got it` 才渲染
- **图表是 canvas,accessibility 树里读不到「Interest over time」** —— 不要用这个字符串判断是否加载成功,
  改判 `document.body.innerText` 里有没有 `Past 12 months`
- **最有用的不是曲线,是「相关查询 → Rising」列表**(带 `+750%` / `Breakout` 增幅),
  它是词族扩展和新需求的信号源,从 `innerText` 里 `Rising` 之后直接切
- 页面有 `file_download` 导出按钮,需要精确时序数值时用它

## 使用前必看

- **先问出口**:这次查询的结果会落到哪个动作?答不上来就不查(公理 6,同 [`seo-data`](../seo-data/SKILL.md))。
- **订阅 2026-09-06 / 09-07 到期**(2026-08-07 启用)。过期后 Semrush / SimilarWeb 全失效,
  届时降级回 Google Trends(免费)+ GSC 实测。
- 面板卡片上有「API 今日配额」「API TOTAL 配额」,批量查词前扫一眼。

## 三个工具的实测边界(2026-08-09 亲测,别再重复踩)

1. **Semrush 收录不了极长尾工具词。** `split 3mf` 查询结果搜索量/KD/全球量**全是「不可用」**,
   但同一时间 `3d printing` 正常返回 246K / KD 93 —— **工具没坏,是词低于数据库门槛**。
   而 GSC 显示 `split 3mf` 近 90 天有 233 次真实曝光。
   **→ 判断极长尾工具词时,Semrush 的「无数据」不等于「没需求」,必须以 GSC 实测为准。**
2. **种子词能救回来。** 头词查不到时,把词根丢进 keywordmagic 查词族——
   `3mf` 种子拉出 `3mf to stl` 4,400/月 KD19 等一批有量的词。**头词无数据 ≠ 词族无量。**
3. **两个估算源会打架,而且差很多。** 同一天同一个词 `3mf to stl`:
   Semrush 4,400/月 KD19,哥飞 agent 工具实测 ~24,000/月 KD47.9 —— 量差 5.5x、难度差 2.5x。
   **→ 取方向不取绝对值。** 想要真值只有一条路:建页面上线,看 GSC。
4. **SimilarWeb 对小站不可用。** 靠采样外推,月访问低于几万时误差可达数倍。
   **只用来看竞品,永远不要用来看自己的四个站。**

## 已知历史教训

- **排名好 ≠ 有量**:partfit3d 多词进 Top 10,整站 3 个月仍只有 833 曝光。
  查竞品先看**曝光/流量的绝对量级**,再看排名和难度。同一模式已出现三次(羽毛球 / GPT Image 2 / partfit3d),
  见 [`risks.md`](../../../memory/risks.md)。
- **原 SOP 的「月搜索量 >500」红线对工具站不适用** —— 见 [`experiments.md`](../../../memory/experiments.md) 2026-08-09 补记。
  [`methods/search-engine-demand-discovery.md`](../../../memory/methods/search-engine-demand-discovery.md)
  Step 2 仍写着用 Ahrefs Free,**该 SOP 需要按本 skill 的实测修订**。

## 回写

| 拿到什么 | 写到哪 |
|---|---|
| 支持/反驳某方向的证据 | [`themes.md`](../../../memory/themes.md) |
| 候选词 KD / 搜索量验证结果 | [`experiments.md`](../../../memory/experiments.md) 候选关键词池 |
| 新风险模式 | [`risks.md`](../../../memory/risks.md) |
