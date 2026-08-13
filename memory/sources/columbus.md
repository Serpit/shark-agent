# 数据源:哥伦布(columbus.tools)

> **定位**:AI 工具站的**增长样本库**——收录数千个 AI 站,逐站标注流量曲线、变现方式、SEO 打法、头部关键词。
> 它回答的是现有工具回答不了的一个问题:**「有多少个独立站长已经在打这个词/这条赛道,谁在涨谁在跌」**。
>
> **2026-08-14 更新:已接入 MCP,取代旧的 ego-browser 取数流程。** 工具前缀 `mcp__columbus__*`:
> `list_sites` / `list_keywords` / `get_keyword_sites` / `get_site_detail` / `list_backlink_domains` /
> `list_filter_options` / `list_model_releases`。**不用登录态、不用开浏览器、结构化 JSON 直接返回。**
> `seo-competitor` skill 的 [Columbus 章节](../../.claude/skills/seo-competitor/SKILL.md#columbusai-工具站关键词与竞品mcp-直连)
> 是主要执行入口;本文件只补充字段含义、分类体量参考和三条硬边界,不重复列已在那边的调用示例。
>
> 网页版 `https://columbus.tools`(账号 `Serpit G`,专业版)仍在,**只在需要「AI 分析」自由文本段落时才用**——
> 见下方「MCP 覆盖不到的一层」。

## 使用前提(硬约束)

**每次拉数据前先回答一句:这次查询的结果会落到哪个具体动作?**

答不上来就不要查。哥伦布的榜单极易变成"再逛逛还有什么赛道"的无底洞——
候选多、翻页快,每一页都长得像机会。这正是 [axioms.md](../axioms.md) **公理 6** 的典型陷阱形态。
[timeline.md](../timeline.md) 从 2026-07 起已是试错阶段,**看榜不是动作,建页面才是**。

## 信任等级(分三类,不要混用)

| 类型 | 具体字段 | 信任等级 | 落盘要求 |
|---|---|---|---|
| **估算值** | 月访问量(`visits`)、环比增长(`visitsMom`)、自然搜索占比(`tsSearchOrganic`)、DR、国家分布、跳出率 | **第三方估算**(同 SimilarWeb/Semrush 层) | 必须标「哥伦布 + 拉取日期」;与 GSC 冲突时**一律以 GSC 为准** |
| **结构化事实** | 命中某词的站点名单、注册时间(`registDate`)、技术栈、广告网络、结构化数据类型、变现方式(`money`)/SEO 打法(`seo`)标签 | **可直接参考的观察** | 标来源即可,不必与 GSC 对质(它陈述的是"谁在做什么",不是量级) |
| **AI 生成段** | 网页版站点详情页底部「AI 分析 → 市场定位 / 观察」(**MCP 不返回这段**) | **他人观点**,页面自己也标了"仅供参考" | **不可直接落 memory**,同 `seo-advisor` 规则,须过 [`methods/axiom-scan.md`](../methods/axiom-scan.md) |

数据自称"人工整理 + 公开数据源和第三方流量估算服务交叉印证"。
`list_sites` / `get_keyword_sites` 每月更新一次全量,`list_model_releases` 每 5 分钟更新(与选词无关,不接入)。
**引用估算值时把拉取日期记下来**,数字是当月快照,不是实时值。

## 六个 MCP 工具与实际字段

| 工具 | 对应旧网页版 | 关键字段 |
|---|---|---|
| `list_filter_options(dimension="cat"/"sub"/"model"/"mv")` | 一级/二级分类筛选弹窗 | `value`(筛选用 slug)、`nameZh`/`nameEn`、`siteCount` |
| `list_sites(cat=, sub=, money=, seo=, type=, emd=, mom=, reg=, dr=, visits=, organic=, sem=, genai=, status=, q=, sort=, order=, page=)` | `/ai-rank` 榜单 | domain / name / 一句话描述 / `regist_date` / `visits` / `visits_mom` / `est_organic` / DR / categories / 3 月趋势 |
| `get_site_detail(domain=, sections=[])` | `/site/<domain>` | 月访问/增长/3月CAGR/自然搜索占比/DR/注册时间、全部标签、近12月流量、Top10关键词、变现摘要;`sections` 可加 `keywords_full`/`traffic_full`/`teardown`/`country_shares`/`traffic_meta` |
| `list_keywords(contains=, min_frequency=, min_volume=, sort=, limit=)` | `/ai-keyword-rank` 榜单 | keyword / `frequency`(命中站点数)/ volume / cpc |
| `get_keyword_sites(keyword=)` | `/ai-keyword-rank` →「查看命中网站」弹窗 | 每个命中站的 volume/cpc/estimatedValue/visits/`visitsMom`/`registDate`/`tsSearchOrganic`/3 月趋势,按 MoM 倒序 |
| `list_backlink_domains(dr=, visits=, organic=, sort=, page=)` | `/ai-backlink-rank` — **仍不接入**,理由见下 |

`list_model_releases`(模型发布时间线)与选词无关,不接入。

**站点类型**(`list_sites` 的 `type` 参数)最有用的两个值:
- `emd`(关键词驱动)—— 靠 SEO 长尾词起量,**这类才是可复刻对标**
- `brand`(品牌驱动)—— 靠品牌词/外部流量,起量原因往往不在 SEO,**不要拿它当 SEO 对标**

其余还有 `directory`(目录站)、`other`。

**一级分类体量参考**(`list_filter_options(dimension="cat")`,实读于 2026-08-14):

图像生成 1784 · 视频制作 1389 · 文本生成 1372 · 编程与开发 1126 · 生产力与办公 1104 · 音频与语音 897 ·
营销与销售 751 · 平台与基础设施 643 · 聊天与陪伴 444 · 设计 508 · 教育 421 · 社交媒体 359 ·
生活与娱乐 265 · 商业与金融 333 · 邮件与客服 270 · AI检测与人性化 198 · 招聘与人力 181 ·
成人/NSFW 116 · 3D建模 105 · 数据分析 76 · 游戏 54 · 健康与医疗 49 · 法律 26

**外链榜单(`list_backlink_domains`)暂不接入执行流程**:memory 里还没有对应的外链建设 SOP,拉了没有动作出口,
按上方硬约束应该先放着。等真的排到"做外链"那一步再回来用(工具已就绪,不用重新接入)。

## MCP 覆盖不到的一层:AI 生成的「市场定位 / 观察」段

网页版 `/site/<domain>` 详情页底部有一段 AI 生成的自由文本(目标受众、市场定位、观察),
**`get_site_detail` 不返回这段**(它的 `sections` 参数里没有对应选项)。
只有需要读这段定性描述时才开网页(ego 浏览器,登录态已在),其余场景一律用 MCP。

## ⚠️ 三条硬边界(2026-08-11 实跑一次完整选站流程后补,踩过才写的;MCP 切换后规则不变)

### 1. 哥伦布只能发现候选,**绝不能做 GO 决策**

它**不提供关键词意图和 KD**,而这两个恰恰决定成败。
实例:靠哥伦布筛出 `astrocarto.net`(4 个月 0→28.4K、+883%、73.1% 自然搜索、无广告、一次性买断),
每个数字都对,看着是金矿。**过 Semrush 后当场毙掉**——头部词 KD 58、意图 93% informational。

**规则:哥伦布出候选 → Semrush 查 KD + 意图 → Trends 查趋势,三关全过才进 [五重过滤](../methods/benchmark-five-filters.md)。**
跳过 Semrush 这一关的判断一律不可信。

### 2. 月度更新有滞后,**看不见最新的竞争者**

同一次实跑:Google Trends 的 Rising 列表里 `getlora` 和 `upastrology` 已经是 **Breakout**(用户开始搜品牌词),
**哥伦布两个都未收录**。MCP 化不改变这一点——底层数据源仍是月度快照。

**规则:判断"谁在抢这条赛道"时,Trends 的 Rising 相关查询比哥伦布更早暴露新入场者,两个都要看。**

### 3. 变现方式标签是 OR 逻辑,**必须用「广告网络」字段复核**

`list_sites` 的 `money` 参数筛出的站,仍可能同时挂广告——
标签只表示"命中其中一种",不表示"不含其他"。
实例:`phonkmaker.com` 标签是「免费增值 + 订阅制」、定价 $9/$18/$29.9,
但 `get_site_detail(sections=["teardown"])` 的技术栈字段明写 AdSense;`astrocarto.org` 更甚,
网页版 AI 分析直接点出它"meta 声明 no ads 但实际检测到 AdSense"。

**规则:要找纯非广告站,以 `get_site_detail` 的 teardown 段「广告网络」字段为准,该字段为空才算数。**

> **反过来说一条正面结论**:曾实测同一天 `astrocartography` 哥伦布 39.9K/CPC $1.06 vs Semrush 49.5K/$0.96
> —— 量差 24%、CPC 差 10%,**同量级可信**。比 [`seo-competitor`](../../.claude/skills/seo-competitor/SKILL.md)
> 里记的"两个估算源差 5.5 倍"那次靠谱得多。**它的量级数据可用于粗筛,只是不能替代意图和 KD。**

## 结果往哪写

| 拿到什么 | 回写位置 |
|---|---|
| 某个分类下的黑马站(环比增长高 + 注册时间新 + 关键词驱动) | 过 [`methods/benchmark-five-filters.md`](../methods/benchmark-five-filters.md) → 通过的进 [`themes.md`](../themes.md) |
| 某站的变现方式 / SEO 打法标签,值得当机会评估 | 走 `/signals` 三段式,落 [`signals/`](../signals/) —— **不是照抄打法** |
| 候选词的"出现频次 + 命中站点涨跌" | [`experiments.md`](../experiments.md) 候选关键词池,标注哥伦布 + 拉取日期 |
| AI 分析段点出的可疑打法(伪造更新时间戳、内容农场特征等) | 过公理扫描后,新模式补进 [`risks.md`](../risks.md) |

**不要**把返回的整段 JSON 粘进 memory —— 只写结论 + 拉取日期。数据每月更新,粘贴的表格一个月就过期。

## 与其他数据源的分工

| 问题 | 用谁 |
|---|---|
| 这个词多大 / 多难(KD) | Semrush(`seo-competitor`) |
| 这个词在涨还是在跌 | Google Trends(`seo-competitor`) |
| **这个词已经被谁占了、谁在涨谁在死** | **哥伦布** `get_keyword_sites` |
| **这条赛道有多少站、黑马长什么样、用什么打法变现** | **哥伦布** `list_sites` + `get_site_detail` |
| 我自己的站表现如何 | GSC(`seo-data`)—— **唯一真值** |
