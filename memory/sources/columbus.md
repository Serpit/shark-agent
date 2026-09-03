# 数据源:哥伦布(columbus.tools)

> **定位**:AI 工具站的**增长样本库**——收录数千个 AI 站,逐站标注流量曲线、变现方式、SEO 打法、头部关键词。
> 它回答的是现有工具回答不了的一个问题:**「有多少个独立站长已经在打这个词/这条赛道,谁在涨谁在跌」**。
>
> **2026-08-14 更新:已接入 MCP,取代旧的 ego-browser 取数流程。** 工具前缀 `mcp__columbus__*`:
> `list_sites` / `list_keywords` / `get_keyword_sites` / `get_site_detail` / `list_backlink_domains` /
> `list_filter_options` / `list_model_releases`。**不用登录态、不用开浏览器、结构化 JSON 直接返回。**
> **2026-08-25 复测:鉴权与四个主力端点(`list_filter_options` / `list_sites` / `list_keywords` /
> `get_site_detail`)全部正常,数据快照到 2026-07;但 `list_sites` 的参数表有变动,见下方 ⚠️。**
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
| **结构化事实** | 命中某词的站点名单、注册时间(`registDate`)、技术栈、广告网络、结构化数据类型、变现方式(`tags.monetization`)/SEO 打法(`tags.seo_playbook`)标签 | **可直接参考的观察** | 标来源即可,不必与 GSC 对质(它陈述的是"谁在做什么",不是量级) |
| **AI 生成段** | 网页版站点详情页底部「AI 分析 → 市场定位 / 观察」(**MCP 不返回这段**) | **他人观点**,页面自己也标了"仅供参考" | **不可直接落 memory**,同 `seo-advisor` 规则,须过 [`methods/axiom-scan.md`](../methods/axiom-scan.md) |

数据自称"人工整理 + 公开数据源和第三方流量估算服务交叉印证"。
`list_sites` / `get_keyword_sites` 每月更新一次全量,`list_model_releases` 每 5 分钟更新(与选词无关,不接入)。
**引用估算值时把拉取日期记下来**,数字是当月快照,不是实时值。

## 六个 MCP 工具与实际字段

| 工具 | 对应旧网页版 | 关键字段 |
|---|---|---|
| `list_filter_options(dimension="cat"/"sub"/"model"/"mv")` | 一级/二级分类筛选弹窗 | `value`(筛选用 slug)、`nameZh`/`nameEn`、`siteCount` |
| `list_sites(cat=, sub=, model=, mv=, type=, emd=, mom=, reg=, dr=, visits=, organic=, sem=, search=, status=, q=, read=, sort=, order=, page=)` | `/ai-rank` 榜单 | domain / name / 一句话描述 / `registDate` / `visits` / `visitsMom` / `estOrganic` / DR / categories / 3 月趋势 |
| `get_site_detail(domain=, sections=[])` | `/site/<domain>` | 月访问/增长/3月CAGR/自然搜索占比/DR/注册时间、全部标签、近12月流量、Top10关键词、变现摘要;`sections` 可加 `keywords_full`/`traffic_full`/`teardown`/`country_shares`/`traffic_meta`/`backlinks` |
| `list_keywords(contains=, min_frequency=, min_volume=, sort=, limit=)` | `/ai-keyword-rank` 榜单 | keyword / `frequency`(命中站点数)/ volume / cpc |
| `get_keyword_sites(keyword=)` | `/ai-keyword-rank` →「查看命中网站」弹窗 | 每个命中站的 volume/cpc/estimatedValue/visits/`visitsMom`/`registDate`/`tsSearchOrganic`/3 月趋势,按 MoM 倒序 |
| `list_backlink_domains(dr=, visits=, organic=, sort=, page=)` | `/ai-backlink-rank` — **仍不接入**,理由见下 |

`list_model_releases`(模型发布时间线)与选词无关,不接入。

> **⚠️ 2026-08-25 实测:`list_sites` 的 `money=` / `seo=` / `genai=` 三个筛选参数已从 MCP schema 中消失。**
> 变现方式和 SEO 打法标签**不再能用来筛榜单**,只能逐站用 `get_site_detail` 读 `tags.monetization`
> 和 `tags.seo_playbook`(实测 `imagetostl.org` 返回 `monetization: [credits, freemium, subscription]`、
> `seo_playbook: [model_pages, tool_cluster]`,字段本身仍在)。
> **影响**:下方硬边界 3 的"先用 `money=` 筛再复核"流程作废,改为「先按流量/增长筛出候选 → 逐站拉 detail 看标签」。
> 新增可用参数:`model=` / `mv=`(按 AI 模型家族/具体版本筛)、`search=`(总搜索流量占比)、`read=`(已读标记)。

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

## ⚠️ 七条硬边界(2026-08-11 实跑一次完整选站流程后补,2026-08-12 加第 4 条,2026-08-13 加第 5 条,2026-08-25 加第 6 条,2026-08-26 加第 7 条并订正第 3 条;MCP 切换后规则不变)

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

### 3. 变现方式标签不可信,**必须用「广告网络」字段复核**

> **2026-08-25 修订**:原来这条讲的是 `list_sites` 的 `money=` 筛选参数,该参数已下线(见上方 ⚠️)。
> 现在拿变现标签只有一条路——逐站 `get_site_detail` 读 `tags.monetization`。**结论不变,只是入口变了**:
> 标签仍是 OR 逻辑,仍必须复核。

`tags.monetization` 里出现「订阅制 / 积分制」的站,仍可能同时挂广告——
标签只表示"命中其中一种",不表示"不含其他"。
实例:`phonkmaker.com` 标签是「免费增值 + 订阅制」、定价 $9/$18/$29.9,
但 `get_site_detail(sections=["teardown"])` 的技术栈字段明写 AdSense;`astrocarto.org` 更甚,
网页版 AI 分析直接点出它"meta 声明 no ads 但实际检测到 AdSense"。

**规则:要找纯非广告站,以 `get_site_detail` 的 teardown 段「广告网络」字段为准,该字段为空才算数。**

> **2026-08-13 实测误报率:5 抽 2,约 40%。**(当时还能用 `money=subscription,credits,one_time` 筛)5 个站里,
> `describemusic.net` 和 `detectvideo.ai` 广告网络明写 **AdSense**,且**定价线索只有 `Free`** —— 根本没有付费产品。
> **加一个更快的判据:先看「定价线索」字段。只有 `Free` 而无任何价格档 = 没有付费产品,不必再看别的。**

> **⚠️ 2026-08-26 订正:上面这条快判据会产生假阴性,不能单用。**
> `teardown` **只扫首页**。实测 10 个站,`pricing_hints` 只有 `Free`(或为空)的那批,
> `word_count` 全在 **239–1,387**;而有完整价格阶梯的 `datephotos.ai` / `coprep.ai` / `hinoter.com`
> 是 **1,293–3,286**。买量型站的首页是转化漏斗不是内容页,定价在 /pricing 或登录后,扫不到。
> 一个站每月投 $2.6–11 万买流量却「没有付费产品」,不成立 —— 那是检测边界,不是事实。
> **修正后的用法:`pricing_hints` 只有 `Free` + `word_count` < 1,000 + 付费流量占比高
> → 判「定价扫不到」,不是判「没有付费产品」;要定论必须人工开站看。**

### 4. 环比增长排序会把「非搜索流量站」顶到最前,**必须同看两个字段**

`sort=visits_mom&order=desc` 排出来的三位数增长里混着大量**根本不是 SEO 起量**的站。
实例(2026-08-12):`seedance-25.ai` 月访问 3.4K / **环比 +968%**,看筛选列表像黑马;
点进详情页,**自然搜索占比 0.0%、头部关键词带来的流量全是 0、94.1% 流量来自 Nigeria**。

**规则:任何三位数环比的候选,先看「自然搜索占比」和「主要国家分布」两个字段。**
占比 0% → 不是 SEO 样本,别拿它当打法证据;单一非英语区国家 >80% → 流量近乎无变现价值。
完整拆解见 [`risks.md` 模型词域名站](../risks.md#模型词域名站入口靠抢时间留存靠改品牌两头都不占违反准公理-a)。

> **⚠️ 2026-08-27 补:这条排序还有一个反向盲区。**
> 按环比倒序会把**上一版的老站系统性排到最后**——`nano banana` 全量 34 站里,
> `nanobanana.io`(130 万月访问)因为环比 -1.8% 排在末尾,而 `nano-banana2.org`(8.4 万)因 +1077% 排最前。
> **要判断一个品类是不是在死,必须看母词搜索量,不能看站的环比。**
> 站的环比只反映需求在版本之间的**轮转**,母词量才反映品类总盘。

### 5. 头部词 CPC 普遍 < $4,**这个库不适合用来找付费生意**

2026-08-13 拆的 5 个站分属音频处理 / 游戏资源 / 翻译 / 音乐识别 / AI 检测五个不相干品类,
头部词 CPC 全落在 **$0.18–3.56**;对照 `csv to qbo` 的 **$17.63**,差 5–90 倍。
最硬的读数:`describemusic.net` 头部词 `song finder` 月搜 **102.5K**、做到 147.2K 月访问、13 个月站龄,
**仍然只能挂 AdSense**。

**规则:想找付费方向不要从这个库出发。** 哥伦布擅长回答「谁在打这个词、谁在涨谁在死」,
不擅长回答「哪里有人愿意付钱」—— 它的分母本身就是一个低付费意愿池。
**反向用法仍成立**:要找广告/联盟变现的流量站打法,它是合适的样本库。

> **✅ 2026-08-25 全库普查,这条从抽样结论升级为封顶结论。**
> `list_keywords(sort="cpc", min_volume=200, min_frequency=2)` → `totalMatched=370`,
> **CPC > $4 的只有 3 个词**,且其中 2 个是别人的品牌名(`bland ai` $17.96、`peec ai` $12.84),
> 唯一可建站的通用词是 `ai ad creatives`($25.46 / 36,460)。
> 频次榜(所谓 validated demand)则是纯模型词域名站:`nano banana` 35 站、`seedance` 25 站,CPC $0.18–1.42。
> **2026-08-27 订正**:高频次意味着**高竞争**,不意味着**短窗口**——`nano banana` 母词 12 个月不衰减(211 万/月)。
> 否掉这批词的是 CPC 和 KD,不是窗口期。
> **不必再重跑"换个筛法说不定有"—— 全库 CPC 倒序已经是最强口径,答案是没有。**

### 6. 覆盖边界:非 AI 品类的词**一个都没有**(2026-08-25 实测)

`list_keywords(contains="stl")` → `totalMatched=0`;`contains="3d"` 只返回 3 个词,全是 AI 生成类
(`ai 3d model generator` / `hunyuan 3d` / `image to 3d model free`),**没有任何格式转换/修复词**。

**规则:partfit3d 这类非 AI 工具站的选词,不要来哥伦布找**,走 Semrush + [`gefei-kd`](gefei-kd.md) + Trends。
反过来,哥伦布对某个词返回空**不代表这个词没需求**,只代表它不在 AI 工具站样本库里。
完整拆解见 [`risks.md` AI 工具站 CPC 系统性偏低](../risks.md#ai-工具站品类的-cpc-系统性低-1-2-个数量级用它找付费生意是池子选错违反公理-4)。

> **反过来说一条正面结论**:曾实测同一天 `astrocartography` 哥伦布 39.9K/CPC $1.06 vs Semrush 49.5K/$0.96
> —— 量差 24%、CPC 差 10%,**同量级可信**。比 [`seo-competitor`](../../.claude/skills/seo-competitor/SKILL.md)
> 里记的"两个估算源差 5.5 倍"那次靠谱得多。**它的量级数据可用于粗筛,只是不能替代意图和 KD。**

### 7. `sem=` 是这个库唯一「从支出侧倒推」的入口(2026-08-26 首次使用)

`list_sites(sem=["high"|"mid"|"low"])` 按**付费搜索流量占比**分桶。它回答的问题跟其他所有字段都不同:
**谁在花钱买流量** —— 持续买量是揭示性偏好,比「挂了 AdSense」硬得多(后者是被动的,放着不花钱)。

**全库读数(2026-08-26 拉取,快照 2026-07)**:`sem=high` 仅 **118 / 4,630 = 2.5%**;
叠加 `reg=["12m"]` 后 **56 个**,其中约 32 个在涨、18 个在跌。**买量是少数派打法。**

**深拆 10 站后,这 2.5% 内部分成相反的两型 —— 混用会得出错误结论:**

| 站 | 付费合计 | 自然搜索 | 停留 | 定价线索 | 首页字数 | MoM | 型 |
|---|---|---|---|---|---|---|---|
| `aimusicai.co` | **92.8%** | **0.02%** | 104s | 仅 Free | 239 | **-37%** | A |
| `voice2texts.com` | **91.0%** | 2.5% | 114s | 仅 Free | 1387 | -13.7% | A |
| `yumepik.com` | **89.8%** | 3.0% | 128s | 仅 Free | 825 | +9.4% | A |
| `wann.ai` | **59.2%** | 3.8% | 566s | 空 | 368 | +493% | A |
| `whispertranscribe.ai` | 39.5% | 13.4% | 117s | 仅 Free | 1892 | +38% | A |
| `senzia.cc` | 34.8% | 35.0% | 164s | 仅 Free | 812 | +152% | A/B |
| `solmi.ai` | 30.6% | 36.1% | 77s | 空 | 12 | +146% | A/B |
| `datephotos.ai` | 16.4% | **47.2%** | 65s | **$29–800** | 3286 | -3% | **B** |
| `coprep.ai` | 15.6% | **41.6%** | 76s | **$12–72/月** | 3209 | +18% | **B** |
| `hinoter.com` | 12.2% | 28.0% | 65s | **$2 / $600** | 1293 | +65% | **B** |

**A 型(品牌词截流套利)**:买竞品和模型的品牌词广告位 ——
`suno` 3,049,530 / **$0.23**、`suno ai` 1,514,380 / **$0.18**、`higgsfield` 3,368,900 / **$0.36**、
`whisper` 351,810 / **$0.77**。CPC 比 `csv to qbo` 的 $7–15 便宜 10–80 倍,CAC 数学因此成立。
**三个否决项**:①窗口由品牌方单方面控制(Suno 开始投自己的词,成本一夜涨 10 倍,准公理 B);
②入场券 = 付费访问 × CPC 倒推 **$2.6–11 万/月**(我的推算,非读数),不是独立开发者量级;
③地理与合规集中(`aimusicai` **99.99% 日本**;`sem=high` 榜单里 `.ru` 域名扎堆、NSFW/陪伴类占相当比例)。

**B 型(正常生意 + 付费补量)**:自然搜索 28–47% 是主体,付费只占 12–16% 做增量,有真实价格阶梯。
**这才是可攒的形态**,其中 `datephotos.ai` 最值得当模板:9 个月、DR 33、
`programmatic_seo` + `affiliate_program` + 533 引用域 49% dofollow、客单 $29–800。

**规则**:
- 用 `sem=` 找「谁在赚钱」有效,但**必须配 `traffic_meta.sources` + `pricing_hints` + `word_count` 三个字段分型**,
  只看 `sem=high` 会把套利盘当成生意样本
- **A 型的打法不可抄** —— 买别人商标词的位置,风险和窗口都不在自己手上
- 想验 A 型的核心未知(**转化率**),$500 × CPC $0.20 = 2,500 点击就够,**买到的是真值**

> **顺带一条正面证据**(用于反驳「个人开发者做不动出海 web」):本轮 10 站里,
> 注册 **4–12 个月**、DR **0–33** 就做到几万至几十万月访问的有 8 个 ——
> `senzia.cc` 7 个月 380,681(DR 0)、`whispertranscribe.ai` 9 个月 181,200(DR 2.2)、
> `yumepik.com` 11 个月 147,391(DR 0)。**这个库同时是「做不成」的证据库和「做得成」的证据库,
> 取决于你问它哪个问题。**

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
