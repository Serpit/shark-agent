---
name: seo-competitor
description: 查关键词与竞品的外部数据——Semrush(月搜索量、KD、词族扩展、竞品流量)、SimilarWeb(站点流量估算、渠道构成)、Google Trends(趋势方向、上升相关词)、Columbus(AI 工具站关键词竞争格局、竞品流量/增长/注册日期,MCP 直连,仅覆盖 AI 品类)。Semrush 与 Trends 用 ego 浏览器驱动;SimilarWeb 优先走脚本 API(站点流量趋势、KD/CPC/24 月搜索量历史,渠道构成除外);Columbus 走 MCP 工具调用。当对话涉及"这个词难做吗""KD 多少""搜索量够不够""词族有多大""竞品流量多少""对手站怎么样""这个词在涨还是在跌""趋势如何""SERP 头部是谁""这个 AI 工具品类谁在做"时使用。也用于 search-engine-demand-discovery SOP 的 Step 2 三维探针。
---

# 关键词与竞品数据(Semrush / SimilarWeb / Google Trends / Columbus)

**信任等级:第三方估算,不是真值。** 与 [`seo-data`](../seo-data/SKILL.md) 的 GSC 数据冲突时,**一律以 GSC 为准**。
落盘必须标注**工具名 + 拉取日期 + 「第三方估算」**。

> **⛔ 不使用 Ahrefs。** 面板里第一个「打开」按钮是 Ahrefs,**另计费,不要点**。
> KD / 搜索量一律走 Semrush。
>
> **引用域也不必动 Ahrefs(2026-08-27 交叉验证)**:Columbus `get_site_detail` 的
> `backlinks.refdomains` × `dofollowRefdomainsPct` 与 Ahrefs 实测差 **<10%** ——
> `magic3d.io` Columbus 口径 1,203×82%≈**986 dofollow**,Ahrefs 2026-08-15 实测 **902 dofollow**。
> **AI 品类查引用域优先走 Columbus。** 非 AI 品类仍无替代源,此时才考虑动 Ahrefs(需用户明确批准)。

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

### SimilarWeb API 直连(2026-08-26 新增,优先于上面的 ego 路径)

同一个 `serpit` 账号还有一条**脚本路径**,不用开浏览器。代码与凭证见
[`memory/sources/payment-growth.md`](../../../memory/sources/payment-growth.md)。

```bash
# 多域名 × 多月 整站访问量趋势 —— 一次请求拿完
python3 scripts/payment-growth/similarweb/scripts/similarweb_client.py fetch-website-traffic-trend-query \
  --domain <域名1> --domain <域名2> --from-month 2026-02 --to-month 2026-07

# 关键词概览 —— KD / CPC / 24 个月搜索量历史 / SERP 竞品
python3 scripts/payment-growth/similarweb/scripts/similarweb_client.py fetch-keyword-overview-bundle \
  --keyword "<英文词>" --month 2026-07
```

**相对 ego 的优势不在"能拿到什么",而在可复现、可落库、可对比**——
ego 是人肉点浏览器,拉完就散;脚本路径能存快照,下个月再跑一次自动比出变化。

⚠️ **一次最多 5 个域名**,再多会撞上游限流(伪装成"登录过期"的 HTML 跳转页,不是错误码)。

⛔ **渠道构成仍须走上面的 ego 路径。** API 的网站分析大包(`fetch-website-analysis-bundle`)
稳定 502,拿不到直接/搜索/社交/引荐/邮件/广告的占比拆分。

#### KD 与搜索量:这是第三口径,不是替换

`fetch-keyword-overview-bundle` 给的 `Difficulty` / `CPCRangeMin-Max` 是 **SimilarWeb 的数**,
与 Semrush、[gefei-kd](../../../memory/sources/gefei-kd.md) 是三家不同厂商的三套数字。

**本 skill 顶部「KD / 搜索量一律走 Semrush」的规则不变。** SimilarWeb 口径的用途是交叉验证:

| 场景 | 用法 |
|---|---|
| 三家 KD 接近 | 可信度上升,按 Semrush 数走 |
| 三家差 ≥2 倍 | 记进 experiments 分歧标记,**真值只能靠 GSC 单页实测** |
| Semrush 报"无数据"的极长尾词 | 换 SimilarWeb 口径再问一次,可能有 24 个月历史量 |

它比 Semrush 多给的一样东西:**逐月搜索量历史(约 24 个月)**,判季节性和长期趋势比 Trends 的相对指数更实。

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

### Columbus(AI 工具站关键词与竞品,MCP 直连)

> **2026-08-14 更新:哥伦布已接入 MCP,取代下方旧的 ego-browser 取数流程。**
> 榜单浏览类需求(按分类/增长/变现方式筛黑马站、看 AI 分析段落)仍可能要开页面看,
> 那部分手册留在 [`memory/sources/columbus.md`](../../../memory/sources/columbus.md);
> 但**选词与竞品数据一律走本节的 MCP 工具**,不再用 ego-browser 爬 `columbus.tools` 页面。

**范围边界:只覆盖 Columbus 收录的「AI 时代」工具站(有真实流量的 AI 品类站点)。**
非 AI 品类不在库里——已实测 `get_site_detail("partfit3d.com")` 返回 `Site not found`(3D 打印工具站,非 AI 品类)。
判断新方向是否适用:先用 `list_sites` 或 `list_filter_options(dimension="cat")` 查该品类是否存在,不存在就回退 Semrush。

**不走浏览器,MCP 工具直连,免爬取、免登录态、不受 3ue 订阅到期(2026-09-06)影响**——
AI 工具站方向的选词/竞品分析应**优先用这条**,Semrush/SimilarWeb 降级为它查不到时的补充源。

| 工具 | 用途 | 替代了什么 |
|---|---|---|
| `list_filter_options(dimension="cat"/"sub"/"model"/"mv")` | 查有效品类/模型筛选值(**筛之前必须先查**,slug 错了会静默查不到) | 新增,无对应旧步骤 |
| `list_sites(cat=, sub=, type=, mom=, reg=, dr=, visits=, organic=, model=, mv=, ...)` | 按品类 + 站点类型 + 增长/流量/DR 筛 AI 工具站列表。**`money=` 变现方式筛选已下线(2026-08-25 实测)**,要看变现标签只能逐站 `get_site_detail` 读 `tags.monetization` | Step 1 手工翻聚合平台找同类站的一部分 |
| `list_keywords(contains=, min_frequency=, min_volume=, sort=)` | AI 工具词库排行:`frequency` = 有多少个站在打这个词(已验证需求信号),自带 volume/cpc | Semrush keywordmagic 词族扩展 |
| `get_keyword_sites(keyword=)` | 单词竞争格局:每个竞品站的 volume/cpc/estimatedValue/**visits**/**MoM 增长**/**域名注册日期**/organic share/3 月趋势,按 MoM 排序(涨得最快的排最前) | Semrush KD + SimilarWeb 流量 + 问哥飞「竞品新注册动向」,**一次调用三合一** |
| `get_site_detail(domain=, sections=[...])` | 单站深挖:DR、月流量、增长、Top 10 关键词、变现方式摘要 | Semrush Domain Overview |
| `list_backlink_domains(dr=, visits=, organic=, sort=)` | AI 工具站最常见的外链来源域排行 | 外链预算调研的一部分 |

已实测(2026-08-14)`get_keyword_sites("ai image editor")`:一次调用返回 15 个竞品站的
volume/cpc/visits/MoM 增长/注册日期/组织流量占比 + 3 个月趋势。旧流程里这份信息要分别问
Semrush(词数据)、SimilarWeb(流量,且仅对大站可用)、哥飞(注册时间)三次才能拼出来。

**局限**:`get_keyword_sites` 只列「已被 Columbus 索引站」在打这个词,不代表 SERP Top 10 的全貌
(可能有未被 Columbus 收录的小站也在排名);Step 4 变现验证维仍需按原方法无痕实看 SERP。
`estimatedValue`/`visits` 与 SimilarWeb 同属流量估算法,不是真值,信任等级仍是「第三方估算」。

## 使用前必看

- **先问出口**:这次查询的结果会落到哪个动作?答不上来就不查(公理 6,同 [`seo-data`](../seo-data/SKILL.md))。
- **订阅 2026-09-06 / 09-07 到期**(2026-08-07 启用)。过期后 Semrush / SimilarWeb 全失效,
  非 AI 品类降级回 Google Trends(免费)+ GSC 实测;**AI 工具品类不受影响**,直接切 Columbus 为主源。
- 面板卡片上有「API 今日配额」「API TOTAL 配额」,批量查词前扫一眼。

## 四个工具的实测边界(2026-08-09 / 08-14 亲测,别再重复踩)

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
5. **Columbus 只收录 AI 品类站,且要有真实流量。** `get_site_detail("partfit3d.com")` 直接返回
   `Site not found`(未被索引)。**用它之前先确认目标品类在 `list_filter_options(dimension="cat")` 里存在**,
   不存在就说明这条路不适用,回退 Semrush/SimilarWeb。

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
