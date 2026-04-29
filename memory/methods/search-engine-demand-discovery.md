# 搜索引擎需求发现 SOP(Web/SaaS 出海)

> **定位**:从 Google 搜索行为反推 Web 产品需求的可执行方法论。**面向 Web/SaaS 出海主线**,与 [community-demand-discovery.md](community-demand-discovery.md)(社群驱动)形成对位——同一套底层逻辑,信号源换成搜索引擎。
>
> **来源**:本 SOP 在教练对话中整合而成(2026-04-29),底层 6 步框架与 [community-demand-discovery.md](community-demand-discovery.md) 同构,关键替换是把"平台搜索/收藏/评论"换成"Google 搜索量/SERP 缺口/People also ask";与 [`2026-04-indie-saas-3h-brd-validation.md`](../findings/2026-04-indie-saas-3h-brd-validation.md) 的 6 步 BRD 法对接(本 SOP 是 BRD 的"找需求"前置)。

## 底层逻辑

搜索引擎机制让用户**主动键入诉求**,留下可量化的需求信号:

| 信号源 | 含义 | 工具 |
|---|---|---|
| **关键词搜索量** | 多少人主动找这个答案 | Google Trends / Ahrefs Free Keyword Generator / Keywords Everywhere |
| **关键词难度 KD** | 现有内容/产品的竞争烈度 | Ahrefs / SEMrush / Mangools |
| **SERP 现状** | 头部排名是 listicle / 旧工具 / 大厂占位 / 真空白 | 直接 google + 无痕窗口 |
| **People also ask** | 用户后续追问 = 产品扩展空间 | Google 搜索结果右侧 / AnswerThePublic |
| **Reddit / Quora SERP 排名帖** | 用户原始抱怨场景 | "<keyword> reddit" / "<keyword> quora" |

**关键判别**:
- **transactional intent**(用户搜"X tool / X converter / X calculator")= 工具型需求强信号
- **informational intent**(用户搜"how to X / what is X")= 内容型需求,适合内容站不适合 SaaS
- **commercial intent**(用户搜"best X / X alternative / X vs Y")= 决策辅助需求,可做工具+内容混合

## 6 步 SOP(每个候选约 1 小时)

### Step 1 · 选 3-5 个候选关键词(15 分钟)

**不凭空想**,从你**有触感的搜索行为**出发:
- 你过去 1 个月在 Google 自己搜过、但没找到满意结果的关键词
- 你工作流中重复执行的动作(转格式 / 查询 / 校验 / 对比 / 计算)对应的搜索词
- 海外同事 / Reddit / Indie Hackers / r/SaaS 反复抱怨"is there a tool that..."

**词根联想法(高 ROI)**(来源:[2026-04-hot-keyword-quick-site.md](../findings/2026-04-hot-keyword-quick-site.md)):
格式:`[领域词] + [需求词根]`,例如 `AI + generator → AI generator`、`Sora + watermark remover → Sora AI Watermark Remover`。

**26 个常用需求词根库**:
generator, creator, maker, builder, helper, assistant, tool, directory, template, converter, editor, optimizer, checker, detector, humanizer, planner, tracker, summarizer, transcriber, writer, viewer, monitor, simulator, comparator, solver, extractor

**热词信号源(用于发现新词根组合)**(来源同上):
| 方法 | 动作 |
|---|---|
| Google Trends 词根联想 | 用词根组合先看"过去 7 天"找上升趋势,再拉"过去 30 天"验证长期潜力 |
| Twitter/X 监控账号 | @op7418(歸藏)、@dotey(宝玉)、@imxiaohu(小互) + OpenAI/Anthropic 官号 |
| Hugging Face Spaces | huggingface.co/spaces — AI 公司常在此首发新模型 |

**反例**:凭空想"AI 教育工具有没有市场" — 太宏大无法挖。

**输出**:3-5 个具体关键词,例如 `expense tracker for freelancers`、`json to csv converter no signup`、`subscription dashboard for indie devs`。

### Step 2 · 三维探针(每个关键词 15 分钟)

| 动作 | 看什么 | 判定阈值 |
|---|---|---|
| Google Trends 5 年走势 | 趋势是上升 / 平稳 / 下降 | **下降中直接 pass**;平稳/上升才进 Step 3 |
| 搜索量 + KD(Ahrefs Free) | 月搜索量 + 难度 0-100 | **理想区间**:搜索量 500-10K + KD < 30(独立开发可打) |
| People also ask | 列出 4-8 个相关追问 | 追问越具体越好,代表用户场景已成熟 |

**两个红线**:
- **搜索量 < 200/月**:即使 KD=0 也撑不起流量,pass
- **KD > 50 + 头部全是大厂**:1-2 年内打不进 SERP,pass

### Step 3 · 验证"SERP 缺口"(15 分钟)

需求真实之后看供给质量。**用无痕窗口 google + 美区 IP**:

| SERP 头部 10 位的形态 | 判定 |
|---|---|
| Listicle("10 best X tools")+ 旧工具(界面 2015 年风格)+ Reddit 帖 | **强机会**,直接进 Step 4 |
| 1-2 个 indie 工具(< $20/月,UI 一般)+ Listicle 占多数 | **中等机会**,可切差异化 |
| Notion / Stripe / Google / Microsoft 的子页 | pass(几乎打不动) |
| 完全没结果 | **谨慎乐观**——可能真空白也可能没需求,看搜索量是否 > 1K 决策 |

### Step 4 · 抓 1 条"具象搜索意图"(10 分钟)

**从笼统关键词到产品需求文档**的桥:

- ❌ "expense tracker" — 太笼统,大厂占满
- ✅ "expense tracker for freelancers with multi-currency invoicing" — 这就是 PRD

**信号源**:
- Google 搜结果里 **第 1-3 条 Reddit/Quora 帖** — 看原帖问题描述 + 高赞回答里被吐槽的现有方案
- AnswerThePublic 把关键词扩成问句聚合
- "<keyword> alternative" / "<keyword> free" / "<keyword> for <niche>" 后缀搜索

**至少看 5 条头部帖子**,同一具象痛点出现 **≥3 次** 才算真信号(对齐「差评是金矿」原则)。

### Step 5 · 套"选需求三标准"做过滤

| 标准 | 含义 | 反例 |
|---|---|---|
| 功能单一 | 一个产品只解决一个搜索意图 | 全家桶 SaaS |
| 场景清晰 | 一句话描述用户什么时候 google | "效率工具"(无场景) |
| 没有头部产品 | SERP 头部不是 Notion/Stripe/Google 子页 | 通用 expense tracker(Mint/QuickBooks 已饱和) |

三标准全过 → Step 6;任一不过 → pass。

### Step 6 · 1 页 BRD(对接 [钦哥 6 步法](../findings/2026-04-indie-saas-3h-brd-validation.md))

到这步与已有 BRD SOP 对齐,3 小时内产出:

- 竞品表(SERP 前 10 + Product Hunt 同类)
- 用户画像(从 Reddit/Quora 帖子里扒昵称/职业/痛点描述)
- 痛点频次表(关键词 + 出现平台 + 出现次数)
- MVP 范围
- 收费方式(Stripe 月订阅 / 一次性付费 / freemium)
- 首批获客渠道(SEO 长尾 + Product Hunt + Reddit + 冷邮件)

## 工具清单(免费优先)

| 用途 | 免费工具 | 付费工具(必要时) |
|---|---|---|
| 趋势走势 | [Google Trends](https://trends.google.com) | — |
| 关键词扩展 | [AnswerThePublic](https://answerthepublic.com)(每天 3 次免费)/ [Keyword Tool.io](https://keywordtool.io) | Ahrefs Keywords Explorer($99/月) |
| 搜索量 + KD | [Ahrefs Free Keyword Generator](https://ahrefs.com/keyword-generator)(每月 100 次) | Ahrefs / SEMrush |
| SERP 现状 | 无痕 google + [SimilarWeb 浏览器插件](https://www.similarweb.com) | Mangools SERPChecker |
| 用户原话 | "<keyword> reddit" / "<keyword> quora" 直搜 | — |

## 4 个避坑

1. **搜索量 ≠ 付费意愿** — 很多 informational intent 关键词搜索量大,但用户不为工具付费(eg. "what is API"),只为内容付费。**只挖 transactional / commercial intent**
2. **AdWords 数据反映广告价值不反映自然流量价值** — Ahrefs 的 KD 才是自然 SEO 难度,不要被 CPC 高低误导
3. **回音壁与算法个性化** — 你越搜某词推荐越多,容易高估市场。**用无痕窗口 + 美区 IP(VPN 切节点)**做探针
4. **中文搜索习惯 ≠ 英文搜索习惯** — 海外赛道必须用英文关键词探针;百度/谷歌的搜索分布也不同,出海主线只看 Google.com 美区数据

## 何时使用

- 启动新 Web 产品方向 BRD 之前(Step 1-5 是 BRD 的"找需求"前置)
- 已有 Web 候选但想交叉验证流量天花板时
- 个人 IP 选题时——同样可用来挖**英文 SEO 内容选题**

## 何时不适用

- App 产品方向 — 用 [community-demand-discovery.md](community-demand-discovery.md) 配合 App Store 评论挖掘
- 全新品类(没有现有搜索量)— 需要换成用户访谈
- 强行业垂直方向(行业内幕在 Google 显示不出来)— 需要 LinkedIn / 行业垂直社区
- 完全本土化中文产品 — 用 [community-demand-discovery.md](community-demand-discovery.md) 的小红书 + 微信版本
