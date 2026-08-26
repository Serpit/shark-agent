# 实验队列

把 `themes.md` 中值得推进的方向转成最小验证动作。这里不记录泛泛想法,只记录能在限定时间内执行、能产出 GO / NO-GO 判断的实验。

## 模板

```
## <实验名>
- **状态**:planned / running / done / stopped
- **关联方向**:[themes.md#方向名](themes.md#方向名)
- **待验证假设**:一句话说明要证明什么
- **时间盒**:例如 3 小时 / 2 天 / 1 周 / 2 周
- **预算上限**:人民币或美元
- **成功标准**:满足什么条件算 GO
- **失败标准**:出现什么情况算 NO-GO
- **执行步骤**:具体动作
- **结果记录**:完成后写结论、数据和下一步
```

## 当前实验

## 个人 IP 定位与内容主线验证

- **状态**:running(M1 启动,见 [timeline.md](timeline.md#m12026-05ip-起势--brd-第一轮))
- **关联方向**:个人 IP 优先,创业探索并行
- **待验证假设**:用户可以围绕"技术开发视角的海外创业探索"建立一个可持续输出的个人 IP,并通过内容吸引同频人、需求线索、潜在用户和合作机会。
- **时间盒**:第一轮 2 周。
- **预算上限**:0 元。
- **成功标准**:
  - 明确 1 个主定位和 2-3 个内容支柱
  - 2 周内 X 累计 ≥12 条小推文 + ≥1 篇长文/总结,且无连续 2 天断更
  - 至少获得 3 次有效互动(评论、私信、交流、需求反馈、同频连接)
  - 内容过程能反哺创业探索,产出至少 3 条需求/产品/人群观察
- **失败标准**:
  - 定位过泛,无法解释"别人为什么关注我"
  - 内容只记录情绪或流水账,不能沉淀专业判断
  - 输出节奏不可持续
  - 与创业探索完全割裂,无法带来用户/需求/机会线索
- **执行步骤**:
  - 明确目标受众:想吸引谁、帮谁解决什么问题、让谁信任你
  - 选择内容边界:技术开发、独立开发出海、海外 App / 订阅商业化、AI 提效与创业验证
  - 设计 2 周内容实验:每周 3-5 条,优先文字/图文/录屏,露脸渐进式推进
  - 每条内容记录:主题、目标读者、发布渠道、反馈、是否产生需求线索
  - 2 周后复盘是否继续、收窄或换定位
- **结果记录**:
  - 2026-04-28:用户确认可以把四个方向都要,但不能四条并列当主线。最终确认主定位为`技术开发视角的海外创业探索`,三条内容支柱为`独立开发出海`、`海外 App / 订阅商业化拆解`、`AI 提效与创业验证`;个人 IP 作为承接这些内容的外壳,不单独作为空泛主题展开。
  - 2026-04-28:为降低 X / 小红书每日内容生产成本,完成 GitHub skill 初筛。推荐组合:`twitter-reader`用于抓取/分析 X 样本,`viral-tweet`用于优化 X 钩子,`xiaohongshu-ops-skill`用于小红书选题/账号分析/复刻,`humanize-writing`用于去 AI 味;小红书自动发布类 skill 需谨慎使用,避免账号风控,优先用于分析与草稿。
  - 2026-05-19:摄入 [X 平台 AI 自媒体冷启动与放大](findings/2026-05-x-ai-media-cold-start.md),沉淀 [X 冷启动与放大 SOP](methods/x-cold-start-and-amplification.md)。关键调整:用户不应复制泛 AI 自媒体定位,而应把 X 当作个人 IP 信任资产和同频连接入口;平台创作者分成因 Stripe/地区/规则时效问题只作为附加正反馈,不作为 M1 目标。

### 首月内容节奏草案

- **频率**:工作日每天都做小内容输出,周末做长文和阶段总结。
- **工作日节奏**:
  - `X`:每天发小推文,记录当天的观察、判断、踩坑或一个小结论
  - `小红书`:同步做轻量化产出,优先用 AI 辅助,作为低成本分发实验
  - `创业探索记录`:每天都要留素材,哪怕只是一条观察、一段评论、一张截图或一个结论
- **周末节奏**:
  - 产出 1 篇长文或长总结
  - 把一周的零散记录整理成一个完整判断
  - 从工作日的小内容里提炼出可复用的方法、问题和下一步验证点
- **表达形式**:优先短文字 + 图文/录屏,避免一上来就追求长视频或复杂制作。
- **选题原则**:
  - 每条都要能回答一个问题:这和技术开发、海外创业、独立开发、订阅商业化、AI 提效有什么关系?
  - **铁律:只发已经发生的事**(本日真实动作、观察、卡点、决策),不为发内容反向造选题。如果今天创业探索 0 推进,就把卡点本身发出来,不要编。
- **复盘指标**:是否持续输出、是否有人互动、是否带来需求线索、是否能自然沉淀为后续文章/产品/实验素材。
- **平台分工**:
  - `X`:主战场,适合短推文和长文,优先承接思考密度和个人判断
  - `公众号`:练长文能力,适合系统拆解和阶段复盘;每两周 1 篇即可,作为 X 长文的中文沉淀,不单独造内容
  - `小红书`:最低优先级,AI 辅助轻量尝试,有空发、没空跳过,不与 X 抢精力
  - `YouTube`:**M2 末启动,M1 不动**。理由:单条视频制作成本可吞掉一周时间预算;M1 也尚无 MVP 复盘素材,产不出有质感的视频。等到 M2 末用 MVP 上线复盘做首支视频更合理

### 可用栏目名

- `海外创业笔记`
- `独立开发出海实验室`
- `订阅商业化观察`
- `AI 提效与创业验证`
- `海外产品拆解`
- `技术人出海记录`

### X 首发框架

- **账号定位一句话**:一个技术开发者在海外 App 和独立开发路上的真实创业记录,重点分享技术视角下的海外产品、AI 提效和创业试错。
- **3 个固定栏目**:
  - `创业记录`:记录自己在做什么、学到什么、踩了什么坑
  - `产品拆解`:拆海外 App、订阅商业化、独立开发案例
  - `方法总结`:把调研、判断、提效、验证过程提炼成可复用方法
- **起草 SOP**:每条推文按 [methods/x-tweet-writing-templates.md](methods/x-tweet-writing-templates.md) 走 Step 1-5(选题 → 选结构 → 填内容 → 改第一行 → 发布前三问)。10 条首发选题的推荐结构见下表(可调,作为起草锚点):

| # | 选题 | 推荐结构 | 推荐开头型 |
|---|---|---|---|
| 1 | 为什么我把 `技术开发视角的海外创业探索` 作为主线 | 观点宣言 | 直接宣言型 |
| 2 | 我为什么更想做 X,而不是先追求大而全的个人 IP | 认知颠覆 | 反差型 |
| 3 | 海外 App 开发里,最容易被低估的不是技术而是什么 | 认知颠覆 / 框架输出 | 反差型 |
| 4 | 独立开发出海:适合谁,不适合谁 | 对比分析 | 直接宣言型 |
| 5 | 一个技术人如何把 AI 用在调研、写作和开发里 | 清单 / 教学实操 | 数字锚定型 |
| 6 | 为什么我现在更关注"真实付费用户"而不是"流量" | 观点宣言 / 认知颠覆 | 直接宣言型 |
| 7 | 海外产品商业化里,订阅模式为什么值得继续研究 | 观点宣言 | 直接宣言型 |
| 8 | 程序员想做个人品牌,第一步应该先做什么 | 教学实操 / 框架输出 | 直接宣言型 |
| 9 | 我对"创业探索"这件事的边界和节奏 | 框架输出 | 反差型 |
| 10 | 未来 3 个月,我会怎么验证一个方向值不值得做 | 过程透明 / 教学实操 | 数字锚定型 |

- **发布前三问铁律**(摘自 method,strict):① 第一行能让人停下来吗?② 读完能带走一个具体的东西吗?③ 把署名换成别人还成立吗?**第三问能成立 → 回去加只有你知道的细节 + 只有你会下的判断**。
- **置顶自我介绍草稿**:我是一名做海外 App 开发的技术人,正在记录自己的创业探索、独立开发尝试和 AI 提效实践。这里不卖成功学,只记录真实的判断、试错和复盘。

## 技术型出海小工具候选池调研(Web-first)

- **状态**:**parked(2026-04-29 转,等支付通道解决 + SEO 站跑通后再启动)**
- **关联方向**:[技术型出海小工具 / B2B 微 SaaS](themes.md#技术型出海小工具--b2b-微-saas)
- **待验证假设**:在开发者、海外 App 用户、企业内部效率、小团队营销获客这几个入口中,能找到至少 1 个适合 1-2 周 **Web** MVP、3 个月内触达真实付费用户的小工具方向。
- **时间盒**:第一轮 1 周,调研 2-3 个候选方向;每个候选 3-6 小时。
- **预算上限**:0-500 元,只用于必要的工具查询或小额验证;不做大额投放。
- **产品形态约束**:Web-first(Web SaaS / Chrome Extension / 开发者工具站点),不评估 App 形态候选。理由见 [profile.md 方向筛选权重](profile.md#方向筛选权重)。
- **成功标准**:
  - 至少 1 个候选方向满足 3 个不同平台/来源验证的真实痛点
  - 有明确目标用户和付费理由
  - Web MVP 能在 1-2 周内完成,域名 + Cloudflare Pages + Stripe 三件套即可上线
  - 有至少 1 条低成本冷启动渠道(SEO / Reddit / PH / Chrome Store / 冷邮件)
  - 收费模式能覆盖服务器、API、工具成本
- **失败标准**:
  - 找不到跨平台重复出现的痛点
  - 竞品免费且体验足够好,没有明确切入点
  - 获客渠道不可达或完全依赖烧钱投放
  - MVP 范围超过 2 周,或需要用户侧重度集成/迁移
- **执行步骤**:
  - **需求发现路径**:跑 [search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) SOP,**从搜索引擎(Google)挖需求**,而非从 App 评论挖。理由见 [principles.md#需求发现路径要匹配产品分发生态](principles.md#需求发现路径要匹配产品分发生态)
  - **Step A**:用 SOP 第 1 步从用户自己的搜索行为列 3-5 个候选关键词(15 分钟)
  - **Step B**:跑 SOP 第 2-3 步三维探针 + SERP 缺口验证,过滤到 2 个候选(每个 30 分钟)
  - **Step C**:对 2 个候选跑 SOP 第 4-6 步,产出每个候选 1 页 BRD(每个候选 3-6 小时)
  - 选 1 个 GO 候选进入 1-2 周 Web MVP 实验
- **候选池参考(非锁定,需用 SOP 跑过)**:
  - `expense tracker (Web)` — 上轮保留,但 SERP 头部多为 Mint/QuickBooks 大厂,需要找细分场景(freelancer multi-currency / SaaS founder ARR tracker 之类)才有缺口
  - `i18n 翻译管理工具` — 关键词如 `i18n tool open source` / `translation management for indie devs`,需 SOP 验证 SERP 缺口
  - **从 SOP Step 1 跑出的新候选**(用户自己最近在 Google 搜过、没找到满意结果的关键词)
- **不再作为候选**(需求源与产品形态错配,违反 [principles.md#需求发现路径要匹配产品分发生态](principles.md#需求发现路径要匹配产品分发生态)):
  - ~~海外 App 评论/差评分析工具~~ — 需求源是 App Store 评论,用户群在 App 生态内
  - ~~订阅 App dashboard / 分析工具~~ — 需求源是 App 订阅数据,用户群在 App 生态内
  - ~~Reddit 热帖监控~~ — 这是社群驱动需求(对应 community-demand-discovery SOP),不是 search-first
  - ~~API mock / 调试工具~~ — 路径上偏 Web,但 Postman/Insomnia/Bruno 已饱和,SERP 缺口几乎为零
- **结果记录**:
  - 2026-04-28:用户暂时没有明确的开发者自我痛点,因此不从"自我痛点"硬切入;第一轮改用外部观察法。用户熟悉/愿意研究的海外产品类型包括 note app、expense tracker、mobile subscription app、language learning app。初筛后决定优先调研 `mobile subscription app` 和 `expense tracker`,因为前者贴近 App 开发/订阅商业化背景,后者与付费意愿和明确痛点更相关。
  - 2026-04-29(早):基于 App 上架 vs 建站成本对比研究(App Store 首次拒绝率 25-40%、迭代周期 1-3 周、抽成 15-30%;Web 当天部署 + Stripe 3% + 无审核),用户决定**主打 Web 建站为产品形态,App 路径降权**。`mobile subscription app` 移出 BRD 主候选(降为订阅商业化研究素材,服务于个人 IP 内容支柱);`expense tracker` 改 Web 形态后保留;新增 4 个 Web 候选进候选池。
  - 2026-04-29(晚):用户进一步指出"从 app 差评找到的需求,基本还是在 app 生态里面,不会转移到网页侧",决定**需求发现路径换为搜索引擎驱动**(对应新建的 [search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) SOP)。原候选池中"海外 App 评论分析工具"+"订阅 App dashboard"两个 dogfood 候选移出(需求源在 App 生态内,违反路径匹配原则);Reddit 监控/API mock 移出(路径不匹配/SERP 已饱和);`expense tracker (Web)` 与 `i18n 翻译管理工具` 仍待 SOP 验证。
  - 2026-04-29(深):用户基于两条现实约束(**支付通道无 Stripe 资质** + **建站能力前置缺失**),决定**主线切换到百年的 SEO 内容站矩阵 + AdSense**。本实验整体转 parked,等以下两个条件满足后再考虑重启:① SEO 站跑通,建站能力闭环;② 支付通道方案确定(Lemon Squeezy / Paddle 主体 / 海外 LLC)。SaaS 候选不删除,等条件满足后从 SEO 站观察到的 transactional intent 关键词中筛 1 个 BRD 起步。详见 [profile.md 支付通道约束](profile.md#能力与资源) + [themes.md 决策依据](themes.md#技术型出海小工具--b2b-微-saas)。新主线见下方「英文 SEO 内容站矩阵起步」实验。

## 英文 SEO 内容站矩阵起步

- **状态**:running(2026-04-29 启动,M1-M3 主线)
- **关联方向**:[英文 SEO 内容站矩阵 + AdSense 变现](themes.md#英文-seo-内容站矩阵--adsense-变现)
- **待验证假设**:用户(技术开发背景 + 18h/周 + 0 建站经验)能否在 3 个月内跑通"选词 → Astro 建站 → 内容生产 → 外链 → AdSense"的完整 SEO 站闭环,并产出 5-10 站矩阵 + 第一笔 AdSense 入账(几美金即 GO)。
- **时间盒**:3 个月(2026-05 至 2026-07),M1/M2/M3 各有阶段产出
- **预算上限**:
  - M1:**0-200 元**(域名 + 基础工具,Cloudflare Pages 免费)
  - M2:**0-500 元**(可能 Ahrefs Lite / 关键词工具订阅 1 个月做选词)
  - M3:**0-500 元**(继续选词 + 必要时小额外链投入)
  - 全程合计 < 1500 元,远低于 1 万预算上限
- **成功标准(3 个月分阶段)**:
  - M1:**1 站上线**——域名注册、Astro + Tailwind + Cloudflare Pages 模板跑通、5-10 篇内容已发布、Google Search Console 已提交、至少 1 个关键词被收录
  - M2:**3-5 站铺开**——单站上线时间压到 4-6 小时;启动外链系统(Claude Code Skill 化);AdSense 申请提交
  - M3:**5-10 站矩阵 + 第一笔 AdSense 入账**——DR 突破 10-20;AdSense 已通过且有几美金入账;至少 3 个关键词进 Google Top 50
- **失败标准**:
  - M1 末第一站未上线 → 建站流程门槛超出 18h/周可承担范围,降级到更轻载体(Carrd / Notion 公开页)
  - M2 末仍是 1 站 → 不是产能问题,是模板没跑顺,**不要继续上量,先解决模板复用**
  - M3 末 0 站收录 Google → 关键词选错,必须重跑 [search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) Step 2-3 收紧门槛(KD<10 + 月搜索量>500)
- **执行步骤(三阶段)**:

  ### Stage 1(M1 = 2026-05):第一站上线,流程跑通
  1. **选词**(Week 1):跑 [search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) Step 1-3,从用户自己最近 google 过的关键词 + Ahrefs Free Keyword Generator 中筛出 1 个 KD<20 + 月搜索量 500-2K + SERP 头部不是大厂的关键词
  2. **域名 + 模板**(Week 1-2):注册域名(Cloudflare 自带或 Namecheap);克隆 Astro + Tailwind 模板(可参考 [Astro 官方模板库](https://astro.build/themes/));部署到 Cloudflare Pages
  3. **首版内容**(Week 2-3):AI 生成 5-10 篇内容初版(主关键词 1 篇 + 长尾 4-9 篇);**人工校验**事实准确度、本地表达自然度、主关键词出现位置(标题/H2/首段/最后一段)
  4. **基础 SEO**(Week 3-4):提交 Google Search Console + Bing Webmaster;sitemap.xml 自动生成;robots.txt 配置;每页 meta description 唯一
  5. **第一周观察**(Week 4):看 Search Console 是否开始收录;Google Trends 验证选词时的趋势是否稳定

  ### Stage 2(M2 = 2026-06):3-5 站 + 外链系统
  6. 模板 Skill 化:把 Stage 1 的建站流程封装成 Claude Code Skill(选词输入 + 自动 scaffold + 内容初版生成),目标单站上线 4-6 小时
  7. 选 2-4 个新关键词,平行铺站
  8. 启动外链系统:吸收百年的"竞品外链 + 半自动化提交"思路,**先手动跑 30-50 个高质量站点**(资源站 / 行业 directory),再考虑自动化
  9. AdSense 申请:每站独立申请或主站申请(规则常变,M2 中段查最新)

  ### Stage 3(M3 = 2026-07):矩阵铺开 + 数据决策
  10. 站点扩到 5-10 个,DR 目标 10-20
  11. 月底 review 数据:哪类关键词收录快、哪类卡住、哪些站权重起得快
  12. **SaaS 路径决策**:回头评估 SEO 站观察期间是否有 transactional intent 关键词背后能升级 SaaS;同时启动 Lemon Squeezy / Paddle 主体调研

### 候选关键词池(待 Step 2-3 验证)

> 等可切美区 IP 后,挨个跑三维探针(Trends / Ahrefs KD / SERP 头部形态)再决定是否建站。

#### 订阅型 SaaS 选词第一轮(2026-08-11,Semrush 美区,第三方估算)

**筛选轴**(与之前的工具站选词不同,新增两条准入):① 需求必须**复发**(一次性转换器撑不起订阅);
② 意图必须 C/T 为主(对齐 [risks.md informational 伪机会](risks.md));③ CPC 作为付费意愿直读数。

| 候选词 | US 量/月 | KD | CPC | 意图 | 词族 | SERP 头部形态 | 判定 |
|---|---|---|---|---|---|---|---|
| `competitor price monitoring` | 590 | **12** | **$40.46** | **交易** | 224 词 / 3.2K | pricefy.io(AS33)/ prisync(AS41)/ price2spy(AS35)/ Reddit roast-my-startup **全是 indie 量级,无大厂** | ⭐ **首选** |
| `llm seo tool` | 1.0K | 32 | $9.38 | 商务 | 172 词 / 8.7K,`best llm seo *` 12 个变体 KD 5-28 | llmrefs(AS36)/ llmclicks(AS25)/ promptrush(AS23)产品页直接进 Top10 | ⭐ 备选,**窗口期风险** |
| `ai visibility tracker` | 880 | 40 | $12.42 | 商务 | 1.8K 词 / 28.8K | zapier(75)/ seranking(59)/ **ahrefs(73)/ neilpatel(60)** 已占位 | 降级——大厂已进场 |
| `website change monitor` | 480 | 50 | $5.60 | 商务 | 274 词 / 5.3K | — | 观察 |
| `uptime monitoring` | 1.6K | 52 | $19.69 | 商务 | 1.4K 词 / 17.7K | UptimeRobot/BetterStack/Pingdom | pass(红海) |
| `ssl certificate monitoring` | 720 | **27** | $15.34 | 信息 | 163 词 / 3.5K | **SolarWinds / Datadog / Dynatrace / Zabbix / ManageEngine 全是 AS 47-59 企业监控套件** | **pass** |
| `email verification tool` | 6.6K | 66 | $4.74 | 商务 | 176 词 / 11.7K | ZeroBounce 系,需数据基建 | pass |
| `keyword rank tracker` | 5.4K | 65 | $12.10 | 商务 | 1.7K 词 / 46.7K | 红海 | pass |
| `app store optimization tool` | 260 | 67 | $11.26 | 信息 | 80 词 / 1.9K | 美区量太小 | pass |
| `ai humanizer` | 673K | 87 | $0.96 | 商务 | 10.8K 词 / 2.5M | — | pass(KD 87 + CPC $0.96) |
| `dynamic qr code` | 1.6K | 35 | $5.89 | 信息 94% | 607 词 / 15.3K | generator 词 KD 88 | pass |

**本轮最重要的方法论产出**:`ssl certificate monitoring` 是 **KD 低但 SERP 全大厂**的活标本——
Semrush 给 KD 27「容易」,实际 Top10 是 SolarWinds / Datadog / Dynatrace / Grafana / Zabbix / ManageEngine。
**KD 数值不能替代 SERP 实看**,[SOP Step 3](methods/search-engine-demand-discovery.md#step-3--验证serp-缺口和交付物匹配15-分钟) 不可跳过。

**存疑标记**:`best llm seo checker / checkers / checking tool / checking tools / checking software`
等 12 个近义变体在 Semrush 里全部落在 390 或 480 这两个整数上,**疑似 AI 生成的合成 query 模式**,
不排除数据库噪音。该词族取方向不取绝对值,上线后以 GSC 验真。

#### AI 订阅方向:哥伦布种子 → Semrush 验证(2026-08-11,**结构性 NO-GO**)

**方法修正**:上一轮我从自己脑子里列词根(用户当场纠正:「种子应该来自哥伦布的收入」)。
本轮改为 `columbus.tools/ai-rank?money=subscription&organic=high&sort=visits_mom` → 485 站,
拉 10 页、本地按 `关键词驱动` 过滤 → 76 站,剔除模型名依赖站 / All-In-One / NSFW / 赌球,
按重复出现的簇取头词 → Semrush 定生死。

**簇分布**(关键词驱动 + 订阅制 + 高自然搜索,快照 2026-08):
音频/音乐 14 站 · 图像编辑 9 站 · 视频工具 8 站 · 3D 4 站 · 字幕/漫画翻译 4 站 · AI 检测/人性化 3 站 · 开发者工具 3 站

| 头词 | US 量 | KD | **CPC** | 意图 | SERP 头部 | 判定 |
|---|---|---|---|---|---|---|
| `image to stl` | 3.6K | **17** | $1.48 | 信息 | imagetostl.com AS45 / .org AS25 / sloyd AS40 —— **全 indie** | 可打,但**一次性转换,撑不起订阅**;是 partfit3d 的扩量词 |
| `manga translator` | 3.6K | 58 | $0.76 | **交易 71%** | Chrome 扩展 / ichigoreader AS22 / **GitHub 开源在 Top10** | pass(CPC $0.76 + 开源压价 + 版权风险) |
| `vocal remover` | 60.5K | 61 | **$0.50** | 信息 | vocalremover.org AS60 / lalal.ai / **Canva 免费捆绑** | pass(量最大、CPC 最低) |
| `subtitle translator` | 1.3K | 51 | $1.82 | 信息 | 个人项目页 AS34 / **GitHub 开源排第 2** | pass(斯里兰卡/印度/印尼 量均高于美国) |
| `youtube thumbnail generator` | 1.6K | 65 | $1.27 | 商务 | **Canva / Adobe / ChatGPT 占前 5** | pass |
| `image to 3d model` | 6.6K | 50 | $1.31 | 信息 | meshy.ai AS50 / tripo3d —— 融资公司 | pass(印度 8.1K > 美国 6.6K) |
| `ai color analysis` | 1.3K | 35 | $1.01 | 信息 | Reddit SideProject 帖 #1 / manus.im | pass |
| `token calculator` | 880 | 31 | **$0** | 信息 87% | OpenAI 官方 tokenizer #1 | pass |
| `ai video ad generator` | 390 | 41 | **$9.31** | 信息 94% | creatify AS47 / HeyGen AS65 / invideo AS67 | pass(CPC 好但量太小 + 融资公司占位) |

### 结论一:C 端 AI 工具词的 CPC 比 B2B 监控类**低一个数量级**

本轮 9 个 AI 词 CPC 全落在 **$0-1.8**;上一轮同日拉的 B2B 词:
`competitor price monitoring` $40.46 · `brand monitoring tool` $25.66 · `uptime monitoring` $19.69 · `llm seo tool` $9.38。

哥伦布里那些 AI 订阅站能活,靠的是 **10 万-60 万月访问 × 低转化率**,不是高付费意愿。
**DR 0 + 18h/周拿不到那个流量基数。**

> ⚠️ **CPC 低要分两种,不要一刀切**:成熟品类里 CPC 低 = 市场已给出答案(`vocal remover` 存在多年、$0.50);
> **全新品类里 CPC 低只是广告主还没跟上**(`best llm seo *` 系列 CPC $0,但头词 `llm seo tool` 有 $9.38)。
> 判别锚点:**看头词有没有 CPC**,不要只看长尾。

### 结论二(更硬):B2B AI 订阅站在哥伦布里**几乎全是「品牌驱动」**

按 `营销与销售 / 邮件与客服 / 商业与金融 / 招聘与人力 / 数据分析 / 法律` 过滤出 ~44 个订阅站,
**只有 3 个标记为「关键词驱动」**(lebenslauf.de 德国简历 / bilingualjobs.io / realistichandwriting.com 且 -16.8%)。
其余全是品牌驱动 —— 流量来自 PH / X / 融资 PR / 社群,[columbus.md](sources/columbus.md) 明写**不可当 SEO 对标**。

**「AI + 订阅 + SEO 获客」是个三角冲突**:
- AI 里能靠 SEO 拿量的 → C 端创作工具 → 付费意愿薄
- AI 里付费意愿强的 → B2B → 品牌驱动获客,不是 SEO

~~**交集只有一处:AI 相关 + 服务 B2B + 仍能靠 SEO 拿量** —— 即 `llm seo tool` / AEO-GEO 赛道。
哥伦布独立印证:`gracker.ai` 122.7K 月访问 · 51.1% 自然搜索 · DR 58。两个独立数据源指向同一处。~~
**(同日拆解后作废,见下。)**

### 结论三:`gracker.ai` 拆解 —— **上面那条"独立印证"不成立,已推翻**

拆 [`columbus.tools/site/gracker.ai`](https://columbus.tools/site/gracker.ai) 详情页 + Semrush 域名交叉验证(2026-08-11)。

**它的头部关键词一个 AEO 词都没有:**

| 关键词 | 搜索量 | CPC | 带来流量 |
|---|---|---|---|
| `have i been pwned` | 392.3K | $0.76 | 2.1K |
| `dehashed` | 26.3K | $1.79 | 660 |
| `publicwww` | 15.8K | $4.64 | 630 |
| `basic linux privillege escalation g0tmilk` | 590 | — | 500 |
| `dnsdumpster` | 12.7K | $2.24 | 460 |

**全是别人的安全工具品牌词。** Semrush 侧确认结构:**1.8K 页面 / 10,310 关键词**,
流量最大的页是 `/questions/what-are-the-two-types-of-search-engine-marketing`(占全站 **13.42%**)
和 `/questions/what-are-examples-of-search-engine-marketing`(5.03%)——**纯 informational 问答页**。
第一自然搜索竞对是 `cybersectools.com`(网络安全工具目录站),而真正的 AEO 工具 `aeoengine.ai` 只有 4% 重合度。

更离谱的是**缩写碰撞流量**:`scanning electron microscope models`(扫描电镜)排在那个 "search engine marketing" 页上;
`definition of tbt`(6.6K)、`tbt meaning recurpost` 排在 `/dmg/tbt` 页上。**这部分流量与产品完全无关。**

**gracker.ai 是一个网络安全工具目录 + SEO 问答内容中心,顺带挂了个 AEO 产品。**
它的 SEO 打法标签也自证:`替代品对比页` + `内容中心` + `工具集群` + `场景页矩阵` + `联盟计划`。
互动指标同向:停留 **24s** / 页均 2.0 / 跳出 40%,美国仅占 **8.3%**(印度 4.4% 德国 4.4% 越南 4.0%);
自嘲式细节 —— 一个卖 AI 可见度监控的站,自己的 **AI 助手引荐只占 1.5%**;定价线索 `Free`。

**对判断的影响(必须同时改两条)**:

1. **它不能证明 AEO 赛道能靠 SEO 拿量** —— 它证明的是「安全工具目录 + 问答页矩阵能拿量」,与 AEO 无关。
   `llm seo tool` 方向**回落为 Semrush 单一数据源支撑**,而该词族本身已有存疑标记
   (12 个近义变体全落在 390/480 两个整数上)。**证据强度比原判断弱得多。**
2. 它跑出来的那套打法是**内容站 + 联盟/广告变现**,正是本轮要排除的模式。

**方法论沉淀**:哥伦布的「月访问量 + 自然搜索占比」只说明**站在涨**,不说明**靠什么涨**。
把一个站的流量规模当成它主打赛道的证据,是本次差点犯的错。
**规则:引用某站作为"某赛道能靠 SEO 起量"的证据前,必须先看它的头部关键词表,确认流量与产品同源。**
已补进 [risks.md](risks.md)。

### 附带观察(不作候选,备查)

- **AI 面试作弊助手簇正在死**:beyz.ai -1% / linkjob.ai -2.2% / interviewbee -4.8% / interviewcoder -22.4% /
  meetassist -14.5% / liveinterview -26.4% —— 6 个站齐跌,且主打"防检测/屏幕共享不可见",
  撞 [profile.md](profile.md) 明确不做的灰色地带。**整簇排除**
- `champsignal.com`(早期 B2B SaaS 创始人的竞争情报监控,183.9K,**-19.1%**)—— 与上一轮首选
  `competitor price monitoring` 是邻居需求,**它在跌**,评估该方向时要一起看
- `costgoat.com`(监控 AI/云/SaaS 订阅成本与额度,187.2K,-3.3%,DR39)—— 复发需求 + 开发者向,但在跌

#### 长尾路径候选 — 羽毛球教学/装备(2026-05-02 录入,源自 [talks/2026-05-02-overseas-badminton-community-idea.md](talks/2026-05-02-overseas-badminton-community-idea.md))

**信号源**:用户作为 6 年球龄爱好者列出 5 个中文教学查询(高远球 / 握拍 / 发力 / 步伐 / 劈杀),agent 翻译并扩展为英文词族 + 商业衍生。**变现路径**:AdSense + Amazon Affiliate(教学:装备 内容比例建议 7:3)。**预警**:基础术语(badminton clear / footwork / grip)头部被 Badminton Insight / Badminton Bible / Badminton Famly 等 DR 30-50 站占据,新站短期打不进——**必须挑长尾 + commercial 衍生词**。

**优先验证子集(8 个,Step 2 三维探针)**:

| #   | 候选词                                  | 类型         | 假设                    |
| --- | ------------------------------------ | ---------- | --------------------- |
| 1   | `panhandle grip badminton`           | 教学长尾       | 具体握法,头部空,小众但精准        |
| 2   | `badminton footwork drills`          | 教学长尾       | 训练动作型,可能 KD<20        |
| 3   | `how to do slice smash in badminton` | 教学长尾       | 进阶技术,头部少              |
| 4   | `badminton wrist snap drills`        | 教学长尾       | 发力具体动作                |
| 5   | `best badminton shoes for footwork`  | commercial | **变现核心,Affiliate 入口** |
| 6   | `best badminton racket for clear`    | commercial | **变现核心,Affiliate 入口** |
| 7   | `best badminton overgrip`            | commercial | **变现核心,小额复购**         |
| 8   | `how to hit deeper badminton clears` | 教学长尾       | 痛点清晰(打不远)             |

**完整词族备选**(Step 2 子集 NO-GO 后从此池继续抽):
- 高远球:`badminton clear` / `how to do a badminton clear` / `badminton overhead clear technique` / `badminton clear vs drop`
- 握拍:`badminton grip` / `how to hold a badminton racket` / `badminton forehand grip` / `badminton backhand grip` / `how to switch grip in badminton`
- 发力:`how to hit harder in badminton` / `badminton power generation` / `badminton finger power` / `badminton kinetic chain` / `how to generate power in badminton smash`
- 步伐:`badminton footwork` / `basic badminton footwork` / `badminton footwork patterns` / `how to improve badminton footwork`
- 劈杀:`badminton slice smash` / `badminton cut smash` / `badminton slice smash technique` / `slicing smash badminton`

**结果记录**:
- 2026-05-02 Step 1 完成:候选词族登记
- 2026-05-02 Step 2 完成 — **整池 NO-GO,本方向归档**:
  - 8/8 全部 NO-GO:7 个 "No keyword ideas",`badminton footwork drills` <100/Easy KD,`best badminton overgrip` <100/N/A KD
  - 触发 SOP 红线"<200/月即使 KD=0 也撑不起流量"
  - **结构性归因**:垂直运动 + 英文教学/装备型 SEO 三重生态错配(亚洲非英语区用户基础盘 / 教学媒介是 YouTube 而非 Google / 欧美羽毛球小众)
  - **沉淀**:[risks.md 新条目「垂直运动 + 英文教学/装备型 SEO 内容站陷阱」](risks.md#垂直运动--英文教学装备型-seo-内容站陷阱亚洲主流运动尤甚)+ [talks/2026-05-02-overseas-badminton-community-idea.md](talks/2026-05-02-overseas-badminton-community-idea.md) 第 6 段
  - **教训叠加 GPT Image 2**:两次 NO-GO 共同根因 = "不同信号源的热度不能跨生态外推"——社交热度/dogfood 触感 ≠ Google 搜索量,**唯一作数指标 = Ahrefs Free 美区绝对月搜索量**
  - **不再回看完整词族备选** — 整个赛道生态错配,继续抽词只是浪费时间

### 4 站实测数据(2026-08-09 从 Search Console 拉取)

> 数据窗口:各站首次有曝光之日 ~ 2026-08-07。**4 个站的曝光全部始于 2026-07 中下旬**,说明收录起效比计划晚约 2 个月。

| 站 | 类型 | 首次曝光 | 点击 | 曝光 | CTR | 平均排名 | 已收录/未收录 |
|---|---|---|---|---|---|---|---|
| [baxianfans.com](https://baxianfans.com/) | 内容站(华语动画《八仙》英文信息) | 2026-07-13 | **22** | 450 | 4.9% | **8.8** | 3 / 11 |
| [partfit3d.com](https://partfit3d.com/) | 工具站(3MF/STL 拆分) | 2026-07-30 | 5 | **833** | **0.6%** | 20.4 | **44** / 58 |
| [aidepixelate.com](https://aidepixelate.com/) | 工具站(AI 去像素化) | 2026-07-25 | 2 | 32 | 6.2% | 26.8 | 1 / 9 |
| [easyframes.app](https://easyframes.app/) | 工具站(相框) | 2026-07-20 | 2 | 23 | 8.7% | 8.2 | 2 / 6 |
| **合计** | | | **31** | **1338** | — | — | **50 / 84** |

**Top 关键词排名(近 90 天)**

- `baxianfans`:`all wishes come true` 9.1 位/126 曝光;`all wishes come true 2026` 6.9 位;`~ chinese animation` 6.9 位;共 21 个查询,**多数在 Top 10**
- `partfit3d`:`split 3mf` 9.8 位/**253 曝光但仅 1 点击**;`split3mf` 6.3 位;`partfit` 4.4 位;`split3dmf` 4.1 位;`cut stl` 4.0 位;共 41 个查询
- `aidepixelate`:`depixelate` 3.5 位;`depixelation` 7.3 位;但 `depixelizer` 系列 78-95 位(基本没进前 5 页)
- `easyframes`:仅 1 个查询 `framdrop`,2 曝光

**从数据读出的 4 个结论**

1. **「3 个关键词进 Google Top 50」大幅超额达成** — 实际有十几个词在 **Top 10**。选词+建站这条链路已经跑通,不再是瓶颈。
2. **partfit3d 的 CTR 0.6% 是当前最大漏损** — `split 3mf` 排第 9.8 位、253 次曝光只换来 1 次点击。排名在第一页却几乎没人点,典型原因是 title/meta 没吸引力,或 SERP 上方被 AI Overview / 在线工具富结果截流。**修这个比再建一个站 ROI 高得多**。
3. **收录率整体偏低(50/84)** — 除 partfit3d 外三站主要卡在「已发现 - 尚未编入索引」(7 / 11 / 6 页),这是内容量与质量信号不足的典型表现,不是技术问题。
4. **partfit3d 有 25 个 404 + 29 个重复规范页** — 站内死链在浪费抓取预算,是纯技术债,修起来最快。

#### 热词路径候选

- **领域词:`GPT Image 2`**(2026-04-30 录入,信号源:用户在 X / 媒体观察到热度大;**2026-05-01 NO-GO**)
  - **NO-GO 数据(2026-05-01)**:Ahrefs Free 美区数据,父级 `gpt image 2` 月搜索量 <100,12 个相关变体全部 <100/月,`gpt image 2 prompts` 显示 No keyword ideas;Trends 4-22 峰值 100 → 5-01 衰减到 28(9 天 -72%)。整个候选池触发 SOP 红线(搜索量 <200/月即使 KD=0 也撑不起流量),pass。
  - **教训**:社交热度 ≠ 搜索热度。X / 媒体观察到的"热度大"是采购信号,但建站需要的是 Google 搜索流量,必须用 Ahrefs 验证绝对月搜索量才作数。用户讨论 GPT Image 2 时实际可能搜的是父级老词(chatgpt image generator / openai image ai)或直接在 ChatGPT 内使用,根本不搜。
  - **判断(失效,留作历史记录)**:OpenAI 官方词,搜索量大但官方页 SEO 权重极高,**只能挑官方不会做的子需求**(prompts 库 / 对比 / alternative / examples gallery)
  - **候选关键词组合**(按 ROI 排):
    - ⭐⭐⭐ `gpt image 2 prompt generator`(transactional,联盟 + AdSense 入口强)
    - ⭐⭐⭐ `gpt image 2 prompts`(prompt 库,可做长页 + 分类)
    - ⭐⭐⭐ `gpt image 2 vs midjourney` / `vs flux` / `vs nano banana`(commercial,联盟变现强)
    - ⭐⭐ `gpt image 2 alternative`(commercial,提前占位防限流/收费)
    - ⭐⭐ `gpt image 2 examples` / `gallery`(吸量,变现弱)
    - ⭐ `gpt image 2 watermark remover`(先确认是否真有水印再做)
  - **直接 pass**:`gpt image 2 generator`(官方就是答案,打不过 openai.com)
  - **未做的验证(等切美区 IP 后补)**:
    - Google Trends 7 天 / 30 天走势(看是否上升)
    - Ahrefs Free Keyword Generator 月搜索量 + KD
    - 无痕窗口 google.com 美区 IP,看 SERP 头部 10 位是否被 OpenAI 官方 + 大博客占满

- **结果记录**:
  - 2026-04-29:实验启动。状态切 running,主线由"Web SaaS BRD"调整为"SEO 内容站矩阵起步"。等待用户在 M1 第一周完成关键词筛选(SOP Step 1-3 输出)。
  - 2026-04-30:用户选定**热词路径**为先行尝试方向(与百年长尾路径互补)。录入第一个领域词候选 `GPT Image 2` + 7 个候选关键词组合。三维探针验证因当前网络环境不便切美区 IP 推迟,候选池入库待后续推进。
  - 2026-05-01:跑 Ahrefs Free 三维探针(Trends + Volume,SERP 维度因 VPN blocked 跳过)。**`GPT Image 2` 候选池整体 NO-GO**:父级与 12 个变体全部 <100/月,触发 SOP 红线。教训沉淀:**社交热度 ≠ 搜索热度**——X / 媒体的曝光度是社群指标,Google 搜索量才是建站可变现的指标,二者经常背离。新候选池等用户下一个热词输入。
  - **2026-08-09 补记(记忆断档 2026-05-15 ~ 2026-08-09,数据源:Google Search Console 实拉)**:用户在断档期实际**上线并验证了 4 个站**,但未回写记忆。见下方「4 站实测数据」。**M1 / M2 阶段目标实际已达成**(1 站上线 ✅ / 3-5 站铺开 ✅ / 关键词进 Top 50 ✅ 且大幅超额),M3 未达成(站数 4 < 5-10;AdSense 状态未知)。
    - **重大形态偏离**:计划记录的是「英文 SEO **内容**站 + AdSense」,实际做出来的 4 个站里 **3 个是工具站**(aidepixelate / easyframes / partfit3d),只有 baxianfans 是内容站。工具站内容薄,AdSense 过审难度高于内容站——**变现路径假设需要重新对齐**,不能沿用原计划的 AdSense 主路径。
    - **选词方法实际已换轨**:原 SOP 是"用户报候选词 → Ahrefs 验证",连续两次全池 NO-GO(GPT Image 2 / 羽毛球)后停摆;实际跑通的 4 个站选的是**极长尾工具型词**(`split 3mf` / `depixelate` / `all wishes come true`),这类词在 Semrush / Ahrefs Free 常常直接返回"不可用"。
    - > **2026-08-11 订正**:本条原写作「**原 SOP 的"月搜索量 >500"红线对工具站不适用**,需要修订」——**这个结论是错的,不要按它改 SOP**。
      > `split 3mf` 实测约 **1,180 曝光/月**(见下方 08-11 订正),远在 200 红线之上、也落在 500-10K 理想区间内,从来没有低于过红线。
      > 真正的漏洞不是阈值,而是**第三方工具返回"不可用"被当成了 0**。已按此改 [SOP Step 2](methods/search-engine-demand-discovery.md#step-2--三维探针每个关键词-15-分钟)。

  - **2026-08-11 · partfit3d 索引诊断(数据源:GSC「网页索引编制」报告 + curl 实测,agent 用 ego 实读)**

    **已编入索引 43 / 未编入索引 60**,四类原因:

    | 原因 | 数量 | 实质 |
    |---|---:|---|
    | 备用网页(有适当的规范标记) | **30** | trailing slash 与 canonical 冲突 |
    | 未找到 (404) | 25 | 三类代码 bug 生成的幽灵 URL |
    | 已发现-尚未编入索引 | 4 | 同一批页面的带斜杠版本 |
    | 已抓取-尚未编入索引 | 1 | `/guides/meshy-to-3d-print/` |

    **根因:三处配置自相矛盾,构成死循环**(curl 实测验证)

    - 服务器(Cloudflare Pages):`/about/` → **307** → `/about`(去斜杠)
    - 页面 canonical + og:url:`https://partfit3d.com/about/`(**带**斜杠)
    - sitemap.xml(40 条 loc):全部**带**斜杠

    Google 抓 sitemap 里的 `/about/` 被 307 跳到 `/about`,而 `/about` 的 canonical 又指回 `/about/`。
    **没有任何一个 URL 能自我声明为 canonical** → 不带斜杠那版判「备用网页」(30 条),
    带斜杠那版停在「已发现」(4 条)。**一个配置矛盾吃掉 60 条未收录里的 34 条。**
    且 307 是临时重定向,不传递权重,应为 301。

    被卡住的是**全部内容页**:21 个 `/printers/*`、全部 `/guides/*`、2 个 `/compare/*`、`/about`,
    **连工具主页 `/tools/3mf-splitter-online` 都在内**。

    **25 个 404 的真实构成 —— 零条真死链,全是链接生成 bug**

    | 类型 | 数量 | 样例 |
    |---|---:|---|
    | 模板变量 `$slug` 未插值 | 14 | `/printers/$slug/printers/creality-k1c` |
    | 相对链接缺前导斜杠 → 路径段重复 | 8 | `/guides/cut-stl-file-into-parts/guides/cut-stl-file-into-parts` |
    | Next.js route group 括号泄漏进 URL | 3 | `/(pages)/about`、`/(legals)/privacy` |

    > **⚠️ 修正 todos.md 原动作**:原待办写的是「判断死链还是已删页,能 301 的 301」。**方向错了** ——
    > 没有页面需要 301,需要的是修三处链接生成逻辑。改完 bug 让 Google 重抓,25 条自然消失。

    **对 partfit3d 判断的影响**:2026-08-09 下钻算出的「CTR 修复天花板 ≈10 次点击/3 个月」,
    是在**全部内容页未收录**的前提下测得的。天花板结论本身不变(主攻词族确实小),
    但「整站只有拼写变体族在跑」这个观察,**部分是收录 bug 造成的,不全是选词问题**。
    修复后应重测一次再定 partfit3d 的去留。

    **修复优先级**:① 统一 trailing slash(解 34 条,最省事是把 canonical/og:url/sitemap 全改成不带斜杠,
    与 Cloudflare 现有去斜杠行为对齐,不动服务器;顺手 307→301)② 修 `$slug` 未插值 ③ 修相对链接 ④ 修 route group 泄漏。
    **源码不在 `~/workspace` 下,代码级修复待用户提供仓库路径。**

  - **2026-08-11 · 四站 URL 规范化横向体检(curl 实测)**

    | 站 | 服务器对 `/x/` | canonical | sitemap | 判定 |
    |---|---|---|---|---|
    | partfit3d | 307 去斜杠 | **带**斜杠 | **带**斜杠 | ❌ 三方打架(见上条) |
    | aidepixelate | 307 去斜杠 | 不带 | 不带 | ✅ 一致 |
    | easyframes | 308 去斜杠 | 不带 | 不带 | ✅ 一致(308 永久跳,优于 307) |
    | baxianfans | 不跳,全 200 | **恒等于首页** | **不是 XML** | ❌ soft 404 catch-all |

    - **partfit3d 的 trailing slash bug 是单点回归,不是技术栈通病** —— 另两个工具站配置正确。
    - **baxianfans 是另一种病**:任意不存在 URL(实测 `/zzz-not-a-real-page-9987`)返回 **200 + 首页内容 + canonical 指向首页**,
      典型 soft 404 catch-all;且 `sitemap.xml` 被 catch-all 吞掉,`content-type: text/html` 返回首页 HTML,**GSC 读不到**。
    - **⚠️ 修正 todos.md「提三站收录率」的动作方向**:原写的是「补内容厚度 + 内链 + 重新提交 sitemap」。
      对 baxianfans **无效** —— 它的未收录根因是站点没有多页结构 + sitemap 不是有效 XML,不是内容薄。
      aidepixelate / easyframes 的未收录才可能是内容/内链问题,需分开处理。

  - **2026-08-11 · GA4 两项目拆分(数据源:Google Analytics 网页版,agent 用 ego 实读)**
    - 配置发现:`partfit3d` 媒体资源下同时挂了两个网站数据流——`https://partfit3d.com/` 与 `https://aidepixelate.com/`。因此原始「报告概况」会把两个项目混合统计,但数据可按 `主机名` 拆开。
    - 已在 GA4 保存两个可复用比较对象:`PartFit3D` = 主机名完全匹配 `partfit3d.com`;`AIDepixelate` = 主机名包含 `aidepixelate.com`(含子域名)。此后任意标准报告都可直接应用这两个比较对象。
    - **过去 28 天(2026-07-14 ~ 2026-08-10)拆分基线**:

      | 项目 | 活跃用户 | 新用户 | 平均互动时长/活跃用户 | 事件数 | 可见会话来源合计 |
      |---|---:|---:|---:|---:|---:|
      | PartFit3D | 3 | 3 | 0 秒 | 21 | 4(`direct` 3 + `test` 1) |
      | AIDepixelate | 28 | 28 | 8 秒 | 116 | 34(`direct` 25 + Cloudflare Access referral 6 + organic 2 + ziyk referral 1) |

    - **数据质量提醒**:`AIDepixelate` 当前含 `admin.aidepixelate.com`,且出现 6 个 `sweet-glitter-0a6e.cloudflareaccess.com / referral`;`PartFit3D` 有 1 个 `test /` 会话。若要把 GA 当实验真值,下一步应排除后台/测试/内部访问,否则小样本下会明显虚高。两个项目均未显示关键事件,当前只能看流量与互动,不能据此判断转化。

  - **2026-08-09 · partfit3d query 级下钻(数据源:GSC 网页版近 3 个月,agent 用 ego 实读)**

    > ### ⚠️ 2026-08-11 订正:本段所有"每月"数字作废
    >
    > 本段把 90 天报表的总量除以 3 得出"约 84 曝光/月",**但这个站 2026-07-26 才第一次有曝光**,
    > 实际活跃期只有约两周。**分母用了报表窗口长度,不是实际有数据的天数**,低估约 14 倍。
    >
    > 由此推出的两条结论——「池子太小」和「天花板 3 个月 ~70 次点击」——**均不成立**,
    > 已在下方逐条标注。三条结论里**只有第 3 条(品牌词)不受影响**。
    > 方法论漏洞已沉淀为 [risks.md 「按报表窗口摊平均」](risks.md)。

    | 口径 | 点击 | 曝光 | CTR | 平均排名 |
    |---|---|---|---|---|
    | 站点总计 | 5 | 833 | 0.6% | 20.4 |
    | query 表可见(41 词) | 3 | 379 | 0.8% | — |

    差额 454 次曝光被 GSC 隐私过滤,散在不具名长尾里(占 55%),**不是 bug**。

    **CTR 漏损排序**(按预估损失点击,含义见 [sources/gsc.md](sources/gsc.md#1-找漏损点--排名够好但没人点)):

    | query | 曝光 | 点击 | CTR | 该位置经验 CTR | 排名 | 预估损失点击 |
    |---|---|---|---|---|---|---|
    | `split 3mf` | 253 | 1 | 0.4% | 2.6% | 9.8 | **5.6** |
    | `split3mf` | 24 | 0 | 0% | 4.9% | 6.2 | 1.2 |
    | `partfit`(品牌词) | 15 | 0 | 0% | 8.0% | 4.4 | 1.2 |
    | `split3dmf` | 12 | 0 | 0% | 8.0% | 4.1 | 1.0 |
    | 其余 3 词 | 34 | 0 | 0% | — | 6.7–9.8 | 1.0 |
    | **合计** | | | | | | **≈9.9** |

    **三个结论(比"修 CTR"本身重要)**:

    1. ~~**CTR 修复有硬天花板**:把所有漏损点修到位,3 个月也只多约 **10 次点击(≈3 次/月)**~~
       **(08-11 作废)**。该数字用错分母。按订正后的曝光基数,同一批漏损点对应的是**几十次点击/月**量级。
       **修 title/meta 从"做完就走的小事"升回值得优先做的动作。**
    2. ~~**真问题是量级,不是转化**……整站实际建立在**一个**月曝光约 84 次的词上~~
       **(08-11 部分作废)**。拼写变体族的观察**仍然成立**:41 个 query 里
       `split3mf` / `split3dmf` / `spli3mf` / `slit3mf` / `slipt3mf` / `splt3mf` / `spilt3mf` /
       `3mfsplit` / `split.3mf` / `split 3 mf` / `3mf split` 确实全是同一个词的拼写变体。
       **但"池子太小"的判断不成立**——该词族实测约 1,180 曝光/月,不是 84。
       与羽毛球那条**不是同一个模式**,不应并列。
    3. **品牌词 `partfit` 只排 4.4 位、15 曝光 0 点击** —— 自己的品牌名没排到第 1,
       说明站点权重/实体识别不足。这条是独立问题,和 title 无关。**(08-11 复核:仍成立,
       最新数据 20 曝光 / pos 4.7 / 0 点击,情况未变。)**

    ~~**对 M4 的含义**:`partfit3d` 这个站的天花板已经可测……扩量必须靠加词族或加站,
    不可能靠修这一个站的转化。~~ **(08-11 作废,见下方 08-11 订正段。)**

  - **2026-08-12 · partfit3d CTR 复测与 SERP 诊断(数据源:GSC API + Google 美区非个性化 SERP)**

    `split 3mf` 在截至 2026-08-09 的最近 14 天累计 **459 曝光 / 1 点击 / CTR 0.2% / 平均位置 9.4**;
    其中最近 7 天已占 **360 曝光 / 1 点击 / CTR 0.3% / 平均位置 9.4**。前 7 天只有约 99 次曝光,
    因此曝光周环比约 **+264%**。这推翻了 2026-08-09 用首次小样本外推的「月曝光约 84、CTR 修复只多
    3 次/月」判断:页面仍在新站放量期,按最近 7 天静态折算已约 1,500 曝光/月,不可再用早期累计均值估天花板。

    当前工具页整体为 **573 曝光 / 5 点击 / CTR 0.9% / 平均位置 9.2**。按位置 9 的 3% 经验 CTR 粗排,
    `split 3mf` 当前累计漏损约 **13 点击**;若最近 7 天曝光维持,把该词 CTR 从 0.3% 拉到 1% 可多约
    2-3 点击/周,拉到 3% 可多约 10 点击/周。绝对量已经足以做一次 TDK 实验,优先级从「降级」恢复为
    **本周一次性高 ROI 动作**,但仍不替代扩相邻词族。

    美区非个性化 SERP 的结构是:前两名为精确匹配工具站 `split3mf.com`、`3dsplitter.com`,随后出现
    AI Overview;首屏竞品直接说明 `by color / object / plane`,而 PartFit 当前标题
    `Split 3MF Files Online — Free 3MF Splitter (No Upload)` 只说通用品类,没有在标题里表达独有结果
    「按打印机尺寸自动切成可打印零件」。当前实搜 PartFit 未稳定出现在首屏,说明 GSC 9.4 是不同地区/设备的
    曝光加权平均,不是稳定第 9 名;低 CTR 同时受首屏底部位置、AI Overview 和搜索意图分流影响。

    **本轮实验口径**:只改 3MF 工具页的 title / description / H1,建议 title
    `Split 3MF to Fit Your Printer — Free Online Tool`,description 明说「上传 3MF/STL → 选打印机 → 自动切 oversized model →
    本地浏览器处理」;请求重抓后等 14 天,用等长窗口比较 `split 3mf`。第一档成功线为在平均位置没有明显上升
    (变差)的前提下 CTR ≥1%;目标线 2-3%。

    **2026-08-12 · 上线状态确认(curl 实读)**:title 与 description 已生效,与建议文案一致(description 用词略有出入但
    信息点齐全)。**H1 用户决定这轮不改**(仍是旧文案),理由:H1 不进 SERP 摘要,不影响 CTR,这轮实验只测 title/description
    对 CTR 的影响,H1 留到 CTR 结果出来后再单独评估(那是降跳出率的动作,不是这次要测的变量)。
    `gsc.py inspect` 显示 `lastCrawlTime` 仍是 `2026-08-11T00:45`(上线前),**Google 还没用新标题重抓**,
    14 天对比窗口的起点必须等重抓确认后才能定,不能从代码上线日算。待办见 [todos.md](todos.md#todo)。

  - **2026-08-09 · 3MF 词族扩展(数据源:Semrush keywordmagic,第三方估算)**

    **起因**:上一条结论说"扩量必须靠加词族",于是用 `3mf` 做种子词查词族。结果推翻了"这个站没救"的直觉。

    先说方法上的发现:**`split 3mf` 在 Semrush 里搜索量/KD/全球量全是「不可用」**,
    但同一时间 `3d printing` 正常返回 246K/KD93 —— 工具没坏,是**这个词低于 Semrush 收录门槛**。
    而 GSC 显示它近 90 天有 233 次真实曝光。**头词查不到,不代表词族没量。**

    | 关键词 | Semrush 月搜索量 | KD | 意图 |
    |---|---|---|---|
    | `3mf to stl` | **4,400** | 19 | IC |
    | `.3mf file` | 2,400 | 24 | I |
    | `.3mf to stl` | 2,400 | 19 | I |
    | `3mf file` | 1,900 | 26 | I |
    | `3mf file format` | 1,300 | 30 | I |
    | `convert 3mf to stl` | 1,300 | 16 | I |
    | `3mf to stl converter` | 1,000 | 17 | I |
    | `stl to 3mf` | 880 | 17 | I |
    | `3mf viewer` | 320 | 15 | I |
    | `convert stl to 3mf` | 320 | 13 | I |

    **转换类词合计 ~10K+/月,KD 13-24 —— 全在独立开发者可打区间。**
    ~~对照 `split 3mf` 实测约 84 曝光/月,**相邻词族大一个数量级**。~~
    > **2026-08-11 订正**:`split 3mf` 实测是约 **1,180 曝光/月**,不是 84。
    > 转换词族(Semrush 口径 ~10K/月)仍然更大,但**只大约 8 倍,不是 100 倍**。
    > 换主攻词的理由从"当前词是死路"降级为"隔壁池子更大"——**依然值得做,但不再是救命动作**。

    **⚠️ 数据打架,不可当真值**:同日就同一批词咨询哥飞 SEO Agent,它的工具实测给出
    `3mf to stl` **~24,000/月 · KD 47.9**——量差 5.5x、难度差 2.5x
    (见 [advice/2026-08-09-partfit3d-pivot-or-abandon.md](advice/2026-08-09-partfit3d-pivot-or-abandon.md))。
    **两个都是估算。只取方向不取绝对值:这个词族确实大得多,但具体多大只有上线后看 GSC 才知道。**

    **结论修订**:上一条说"天花板已可测",指的是**当前这一个词**的天花板。
    站本身不该弃——**partfit3d DR=0、无权重积累、沉没成本约等于零,换主攻词的代价极低**。
    根因是**先建站再定词**,顺序反了。

    **下一步**:新建 `/3mf-to-stl` 与 `/stl-to-3mf` 两个页面(一页一词),拆分工具做站内互链。
    这是唯一能验真词族量级的办法。**但变现路径仍未定——词族再大,不解决工具站怎么赚钱,
    只是换了个更大的分母。** 变现决策仍是 M4 的第一阻塞项。

  - **2026-08-11 · partfit3d 曝光量订正(数据源:`scripts/gsc.py` API 实拉,真值)**

    起因:核对 08-09 那条"84 曝光/月"时发现,多个回看窗口返回的数字完全相同。

    | 回看窗口 | 起止 | 站点曝光 | `split 3mf` 曝光 |
    |---|---|---|---|
    | 近 7 天 | 08-02 ~ 08-08 | **882** | **276** |
    | 近 14 天 | 07-26 ~ 08-08 | 972 | 307 |
    | 近 30 天 | 07-10 ~ 08-08 | 972 | 307 |
    | 近 90 天 | 05-11 ~ 08-08 | 972 | 307 |

    **14 / 30 / 90 天三档数字完全一致 → 2026-07-26 之前为零曝光。**
    08-09 那次拿 90 天报表的 253 除以 3 得出 84/月,分母错了约 14 倍。

    **当前真实速率**(按最近完整一周外推):

    | 口径 | 周曝光 | 月速率 |
    |---|---|---|
    | 站点合计(36 页) | 882 | **≈ 3,780** |
    | `split 3mf` 单词 | 276 | **≈ 1,180** |

    query 表可见 42 词 / 468 曝光 / 4 点击;其余 504 次(52%)被 GSC 隐私过滤。
    页面级集中度极高:`/tools/3mf-splitter-online/` 一页占 486 曝光(pos 9.4),
    两篇 guides 各 ~92 曝光但排名在 31-37 位。

    **对 M4 的含义(替代 08-09 那段)**:
    1. `split 3mf` 若打到第 1 位(CTR ~27%),对应 **~300 次点击/月**,不是"3 个月 70 次"。
       这个站**没有到天花板**,当前 CTR 0.3% 说明漏的全是转化,不是流量。
    2. **修 title/meta 的优先级应当升回来** —— 基数放大 14 倍后,同样的动作对应几十次点击/月。
    3. 换主攻词到转换词族**仍然值得**(隔壁池子约 8 倍大),但**不再是"这个站没救所以必须换"**,
       而是常规的扩量选择。两件事可以并行,不用二选一。

    > ⚠️ **本条数据的保留**:882 曝光只有一周(前一周仅 90 次,周环比 +880%)。
    > 位置未变(pos 9.8)而曝光暴涨,可能是收录成熟后的自然爬坡,也可能是一次性尖峰。
    > **~3,780/月 这个速率需要 2026-08-18 复拉确认**;若回落,以复拉值为准。
    > 但"84/月 是算错的"这一点与后续走势无关,已确定。

  - **2026-08-11 · partfit3d 免费外链首批提交(目录 + 现有链接核验,agent 用 ego 实操)**

    **动作出口**:给 partfit3d 补品牌/发现信号,并建立可复查的提交记录;不把外链当作 canonical/404 修复的替代。

    **已核验现有链接**:`https://tg.noisework.cn/posts/11353` 已被 Google 收录,页面有 2 个直达
    `https://partfit3d.com/` 的链接,`rel="noopener"`,无 `nofollow`。

    | 渠道 | 提交状态 | 链接形态 | 备注 |
    |---|---|---|---|
    | Startup Collections | ✅ 2026-08-11 进入免费审核队列 | 待审核,暂无公开 listing URL | 表单回执“您的回复已记录”;未付 $10 插队费 |
    | WebsiteHunt | ✅ 已建公开详情页,`Pending review` | 免费版使用站内追踪跳转 `/go/23356/`,不是直链 | [PartFit 3D](https://www.websitehunt.co/websites/partfit-3d);免费队列约 12+ 月 |

    **剔除记录**:twelve.tools(要求首页反链)、SimpleLister / What Launched Today / ToolsFine
    (免费名额关闭或付费)、Unloc / 700.tools / Wewaat(失效)、Toolbase(受众强制限定公司阶段,
    与个人 maker 不匹配)、HN / 10words(无现成登录或需新建密码)。

    **判断**:本轮目标是拿到“可核验的真实提交记录”,不是堆数量。立即生效的高质量直链仍只有
    noisework;两条新目录提交要等审核,WebsiteHunt 免费追踪链的 SEO 权重低。

    **复查节点**:2026-08-25 回查 Startup Collections / WebsiteHunt 审核状态;若未上线,不加钱插队,
    转向 3D-printing 资源页 outreach / Show HN(需用户现成 HN 登录)。

  - **2026-08-14 · 围绕 partfit3d 的"3D 模型处理"赛道全景扫描(数据源:Semrush keywordmagic 美区 + Google 无痕 SERP 实查 + SimilarWeb,第三方估算)**

    **动作出口**:决定 partfit3d 下一个扩展页面主攻哪个词族。**未用 Ahrefs**——`seo-competitor` skill 明确禁止(面板里 Ahrefs 单独计费,一律走 Semrush)。

    **转换类词族(3mf ↔ stl,已知方向复核)**

    | 词 | 月量 | KD | CPC | 意图 |
    |---|---|---|---|---|
    | `3mf to stl` | 4,400 | 15 | $3.17 | I |
    | `.3mf to stl` | 2,900 | 13 | $3.17 | I |
    | `convert 3mf to stl` | 1,300 | 16 | $2.30 | I |
    | `3mf to stl converter` | 1,000 | 17 | $2.15 | I |
    | `stl to 3mf` | 880 | 17 | $3.10 | I |
    | `stl to 3mf converter` | 390 | 15 | $2.30 | I |
    | `convert stl to 3mf` | 320 | 13 | $4.06 | I |

    合计 ≈ 11,190/月,KD 13-17。与 08-09 数据方向一致(小幅波动属正常估算误差)。

    **修复类词族(stl repair/fix,新发现,此前未探)**

    | 词 | 月量 | KD | CPC | 意图 |
    |---|---|---|---|---|
    | `stl repair` | 1,900 | 18 | $1.42 | C |
    | `stl fixer` | 1,000 | 14 | $1.42 | I |
    | `repair stl files` | 720 | 9 | $2.60 | I |
    | `repair stl` | 590 | 25 | $2.03 | I |
    | `fix stl` | 590 | 15 | $1.38 | I |
    | `stl fix` | 480 | 11 | $2.03 | I |
    | `fixing stl files` | 480 | 14 | $2.03 | I |
    | `stlfix` | 390 | 28 | $4.04 | N |
    | `stl model repair` | 320 | 12 | $1.42 | I |
    | `stl repair online` | 320 | 12 | $1.80 | C |
    | `stl file repair` / `repair stl file` | 260×2 | 14/11 | $2.03 | I |
    | `fix stl online` / `repair stl files online` | 260×2 | 12 | $2.15 | I |
    | `repairing stl files` | 260 | 9 | $2.03 | I |
    | `stl repair tool` / `online stl repair` | 210 | 10/9 | ~$1.8 | I |

    合计 ≈ 9,000+/月,KD 9-28(多数 <18),明显偏「online/free」修饰词,工具型意图纯度高。

    **关键发现 —— SERP 实查推翻"KD 相近所以难度相近"的直觉**

    | 词 | Google 美区无痕 SERP 头部 |
    |---|---|
    | `3mf to stl` | imagetostl.com(indie)/ **meshy.ai(融资公司)**/ Reddit / YouTube / anycubic.com、snapmaker.com(打印机厂商博客)/ **zamzar.com** |
    | `stl repair` | formware.co / justfixstl.com / remeshy.com / nano3dtech.com(全 indie 单功能工具站)/ meshinspector.com(小众软件商)/ Reddit / 2 篇工具榜单博客 |

    SimilarWeb 实测 `zamzar.com`(通用文件转换权威站,占了 `3mf to stl` 第一梯队位置):
    **687万月访问 · 全球排名 #28,210 · 73.67% 来自非品牌自然搜索**。`justfixstl.com` 小到 SimilarWeb
    直接拉不出数据——**和 partfit3d 现在的量级同一档**。

    **结论:两个词族 KD 数字都在 13-25 区间、看着难度相近,但 SERP 真实竞争强度完全不同。**
    转换类前排卡着一个 687 万访问的通用权威站 + 一家融资 AI 公司;修复类前排全是与 partfit3d
    同量级的 indie 单功能工具站,**结构与 `split 3mf` 当初能进 Top 10 的 SERP 一致**(前排是弱站,不是巨头)。
    这是继 `ssl certificate monitoring`(KD27「容易」但头部全企业级监控站)之后,第二次验证
    **KD 数值不能替代 SERP 实看**,已按此更新排序判断。

    **排除/待定**

    - `resize stl` / `scale stl` / `resize 3d model` — Semrush **无数据**(低于数据库收录门槛,
      不代表无需求——`split 3mf` 当初也是这个状态,实测后有 1,180 曝光/月)。不能直接判死,
      只能标记"需上线后用 GSC 验",不进本轮排序。
    - `mesh repair` — 头词语义被医疗(疝气网片手术)完全占据,不可用,种子词换回 `stl repair`/`fix stl`。

    **对 M4 待办的修正**:原计划优先建 `/3mf-to-stl` `/stl-to-3mf`。**本轮建议调整优先级**——
    先建 `/tools/stl-repair`(量级相近、KD 相近或更低、SERP 实际竞争弱得多、与拆分工具用户高度重合:
    同一批人先修网格再拆分打印),转换页面保留为第二梯队,不取消,只是不再排第一。

  - **2026-08-14(晚)· `glb to stl` 候选发现(信号源:用户自己看 Google Trends 发现,agent 用 Semrush + SERP 实查验证)**

    **发现过程**:用户直接甩来一条 Google Trends 三词对比链接(`3mf to stl` / `glb to stl` / `image to stl`,
    Worldwide、近 12 个月),让 agent 看有没有启发——这条线索不是从 SOP 候选池里排出来的,是用户自己在
    对着已知词族琢磨时顺手查到的。

    **Trends 原始数据**(2026-08-14 拉取):三词近 12 月相对热度均值 `image to stl` 71 >
    `3mf to stl` 49 > `glb to stl` 16。`image to stl`、`3mf to stl` 全年稳步上涨,2026-05 前后有明显跳升;
    `glb to stl` 基数低但也在抬头;近 3 周(7月下旬-8月)三条线都略回落,样本太短暂不下结论。

    **真正的信号在"相关查询·上升"榜**:
    - `3mf to stl` 上升榜:**meshy(Breakout)、meshy ai(Breakout)**、image to 3d model(+350%）、glb to stl(+250%)
    - `glb to stl` 上升榜:**tripo ai(+1,100%)、meshy(+800%)、tripo(+600%)、meshy ai(+600%)**、fbx to obj(+400%)

    **解读**:meshy 和 tripo 是做"图片/文字生成 3D 模型"的 AI 融资公司(meshy.ai 已在 08-14 早些时候的
    `3mf to stl` SERP 实查里出现过)。三个转换词共同的增长驱动**不是存量的手工格式转换需求,是 AI 生成
    3D 内容爆发带出的下游刚需**:用户用 Meshy/Tripo 生成模型 → 工具默认吐出 **GLB**(网页/AR 标准格式)
    → 打印机软件要 STL/3MF → 搜索转换词。**这是增量需求,处于早期(还在从低基数暴涨)**,不是存量红海。

    **`glb to stl` 硬数据(Semrush 美区,2026-08-14)**

    | 词 | 月量 | KD | CPC |
    |---|---|---|---|
    | `glb to stl` | 1,300 | **8** | $3.14 |
    | `.glb to .stl` | 390 | 5 | $3.34 |
    | `convert glb to stl` | 260 | 6 | $3.32 |
    | `glb to stl converter` | 260 | 9 | $2.41 |
    | `.glb to stl` | 170 | 3 | $3.34 |
    | `stl to glb` | 140 | 11 | — |

    合计 ≈ 2,520/月,**KD 3-11,是这三批词族(转换 13-17 / 修复 9-28 / 这批 3-11)里最低的一档**。
    绝对量级明显小于前两批,是早期押注,不是确定收益。

    **SERP 头部实查**(Google 美区无痕):imagetostl.com、convert3d.org、**meshy.ai**、furnimesh.com、
    customuse.com、**sloyd.ai**、magic3d.io、**zamzar.com**(同一个 687万月访问的通用转换权威站,又出现了)、Reddit。

    两个新观察:
    1. **meshy.ai 和 sloyd.ai 自己上了转换工具**——这两家做 AI 生成 3D 模型,提供转换器是为了**堵自己用户
       的下一步流失**(用户拿着 AI 生成的 GLB 想打印,不能让他们跑去第三方站),不是主动来抢这个词的流量。
       这条反过来印证了上面的需求解读。
    2. **imagetostl.com / convert3d.org / furnimesh.com / customuse.com 在 `3mf to stl` 和 `glb to stl`
       两个 SERP 里重复出现**——大概率是同一操盘手用同一套转换引擎批量铺的"格式对矩阵站"(一个引擎,
       几十个域名各占一个格式对)。**这不是跟单个对手竞争,是跟一套可复制的模板打法竞争**,但也说明这套
       打法本身跑得通,partfit3d 可以借鉴同样思路——同一套转换/修复/拆分技术底座,铺多个一词一页。

    **与 `image to 3d model` 的边界(重要,避免误判)**:`image to 3d model` 是 AI **生成**步骤本身,
    2026-08-11 已经因为 meshy.ai/tripo3d 融资公司占位而 pass 掉(见上方「哥伦布种子」段)。`glb to stl`
    是生成**之后**的格式转换步骤,技术门槛完全不同(纯几何格式转换 vs AI 3D 生成),partfit3d 现有拆分/
    修复技术栈能直接接,**这条不是重新捡回被 pass 的候选,是同一条需求链上更下游、更适合的一段**。

    **结论**:不单独立项,并入 partfit3d 工具矩阵的第四块拼图。完整用户流程:
    AI 生成模型(在 Meshy/Tripo 上,拿不到这步)→ **GLB 转 STL/3MF**(可以拿)→ 修复网格 → 拆分适配打印机。
    四步做站内互链。`glb to stl` 页面成本低(KD 3-11,复用现有转换逻辑),现在量小,但 Trends 显示还在
    早期爆发阶段,值得顺手做、提前卡位。

    **过程记录 · 一次工具使用风险**:本轮查询中途,3ue 面板弹出系统消息(08-13 13:04)
    "严禁任何用户使用或部署任何形式的第三方脚本、自动化工具(Bot)辅助工具对本平台进行访问、操作或数据抓取",
    且用户手动接管过一次浏览器任务空间。不确定是否针对本次查询频率触发,但该面板订阅同时支撑四站的
    SEO 数据源,**后续用 ego-browser 自动化查询 Semrush/SimilarWeb 时应控制频率和批量大小**,不要为了
    抠单个词的精确数字做不必要的连续查询(呼应协议里的"公理 6:拉数前先想清落到哪个动作")。

  - **2026-08-15 · 用 `gefei-kd` MCP + Google Trends 三词联查,交叉验证 08-14 的排序(数据源:哥飞版难度模型 + Google Trends,第三方估算)**

    **动作出口**:核实 08-14 仅凭 Semrush 数字 + SERP 肉眼判断给出的"先建 stl-repair"排序是否站得住,
    此前完全没用过 `gefei-kd`(独立难度模型)和覆盖 `stl repair` 的 Trends 对比。

    **`gefei-kd` 难度分交叉验证**(2026-08-13/14 计算,US):

    | 词 | 难度分 | 判定 | 月量(哥飞口径) | 链接预算(中值) | 对应 DR |
    |---|---|---|---|---|---|
    | `stl repair` | **30.2** | 容易 | 2,090 | 35 个引用域 | DR 24 |
    | `glb to stl` | **34.4** | 容易 | 9,950 | 45 个引用域 | DR 26 |
    | `3mf to stl` | **48.6** | 中等 | 25,000 | 80 个引用域(目录型放大到 200-480) | DR 31 |

    **方向结论与 08-14 一致**:难度排序 stl-repair < glb-to-stl < 3mf-to-stl,与昨天纯肉眼判断 SERP 强弱的结论同向,
    不是巧合——两个独立方法论(SERP 站点体量目测 vs 哥飞的 DR/流量/行为数据加权模型)指向同一个排序。

    **但哥飞的盘面拆解给出一条 08-14 没有的重要修正**:stl-repair 虽然难度分最低,但**判断原因里明确标注
    "8/9 个结果是专门为这个词制作的页面……不是'大站顺路排名'的机会盘面,而是被正面争夺的红海词"(+10 分)**。
    昨天"竞品都是 indie 小站 = 好打"的判断只对了一半——小站数量多且都在**专门死磕这个词**,
    不是"随便做做就能上",门票是做出和 `justfixstl.com`(DR14、6 个月新站排第 2)同等水平的产品,不是躺赢。

    **两源搜索量对质,再次印证"取方向不取绝对值"**:

    | 词 | Semrush(08-14) | `gefei-kd` | 倍差 |
    |---|---|---|---|
    | `stl repair` | 1,900 | 2,090 | **1.1×,两源少见地接近** |
    | `3mf to stl` | 4,400 | 25,000 | 5.7×(与历史已知的 5.5× 分歧幅度一致,不是新异常) |
    | `glb to stl` | 1,300 | 9,950 | 7.7× |

    `stl repair` 是三个词里唯一两源高度吻合的,置信度明显更高;另外两个词继续按"只取排序不取绝对值"处理。

    **Google Trends 三词联查**(`stl repair` / `3mf to stl` / `glb to stl`,US,近 12 个月,2026-08-15 拉取)——
    **这是 08-14 遗漏的一环,当时只查了 `glb to stl` 所在的三词组,没把 `stl repair` 放进同一张图对比**:

    - 12 个月平均相对热度:`3mf to stl` **61** > `stl repair` **54** >> `glb to stl` **5**
    - `3mf to stl` 全年多次冲到峰值 100(2025-12-21 附近),波动更大但整体热度**高于** `stl repair`
    - `glb to stl` 2025 年 11 月前长期为 0,之后断续出现,**确认"早期爆发中"的判断,但目前体量仍明显小一个量级**
    - Rising 相关查询:`3mf to stl` 后面跟着 `onshape`(Breakout)/`png to svg`(Breakout)/`image to stl`(+300%)/
      `obj to stl`(+120%)共 5 条,需求扩散面明显更广;`stl repair` 只挂了 1 条(`microsoft 3d builder` +350%),
      热度扩散信号弱很多

    **关键新发现(修正 08-14 的隐含假设)**:08-14 把"转换类"和"修复类"两个词族当成量级相近来比较
    (Semrush 分别 11,190/月 和 9,000+/月),但 **Trends 的相对热度显示两者不是同一量级**——
    `3mf to stl` 的真实搜索兴趣明显高于 `stl repair`,且需求扩散面(rising queries 数量)也更广。
    换句话说:**难度上 stl-repair 更好打,但需求盘子上 3mf-to-stl 更大**,08-14 的排序只考虑了"好不好打",
    没有把这条"盘子谁更大"的独立证据放进去。

    **对优先级排序的影响(留待用户判断,不单方面改 todos 顺序)**:
    - 若继续按"先拿一个快胜"的逻辑 → **stl-repair 仍应排第一**,难度最低、两源搜索量高度吻合、置信度最高,
      唯一要调整预期的是:别指望"随便糊一个页面就能进前十",竞品是专门死磕这个词的一批 indie 站,产品质量要跟上
    - 若愿意为更大的盘子多担一点风险 → **3mf-to-stl 值得重新评估**,难度分 48.6 落在
      [timeline.md 新约束](timeline.md#2026-08-12约束框架转向用户决策取代-m1-m4-的零预算新站能打前提)
      允许的 KD 45-55 区间内,链接预算中值 80(远高于 stl-repair 的 35),但 Trends 显示它是三个词里
      **真实需求最大、扩散面最广**的一个;⚠️ **这条新约束框架当初是为"大站/新站"场景定的,partfit3d 是现有小站增页,
      是否要为一个页面动用付费外链预算,是个需要用户确认的范围问题,不能直接套用**
    - `glb-to-stl` 排序不变,继续排在 stl-repair 之后、3mf-to-stl 之前,难度(34.4)和链接预算(45)都介于两者之间,
      Trends 确认早期但体量仍小,维持"顺手做、提前卡位"的定位

    **产出**:排序方向没有反转,但补全了 08-14 缺失的两个信号源,且发现一条此前没考虑过的变量(需求盘子大小 vs 难度的取舍)。

  - **2026-08-15(续)· 用 Ahrefs 查三个"最弱竞品"的真实引荐域名,最后确认(数据源:Ahrefs Site Explorer,经 3ue 面板,第三方估算但比 `gefei-kd` 插值更接近真值)**

    **动作出口**:`gefei-kd` 的链接预算是从难度分沿 Ahrefs 曲线插值出来的,不是数出来的
    (见 [`sources/gefei-kd.md`](sources/gefei-kd.md#2-链接预算是曲线插值不能替代查竞品实际引用域));
    这一步去查 `gefei-kd` 盘面表点名的最弱竞品的**真实**引荐域名,作最后确认。
    ⚠️ 本次用 ego-browser 自动化访问了 Ahrefs(3ue 面板),面板首页有 08-13 的系统消息禁止自动化访问 Semrush/SimilarWeb,
    用户已知情并明确同意继续。

    | 词族 | 最弱竞品 | DR | 引荐域名(总) | **引荐域名(dofollow)** | `gefei-kd` 预算(中值) |
    |---|---|---|---|---|---|
    | stl-repair | justfixstl.com | 14 | 427 | **10**(2.3%) | 35 |
    | 3mf-to-stl | imagetostl.org | 25 | 524 | **67**(12.8%) | 80 |
    | glb-to-stl | magic3d.io | 5 | 1,113 | **902**(81.0%) | 45 |

    **关键发现:三个词的"总引荐域名"都比 `gefei-kd` 估算高出 6-25 倍,但 dofollow 占比天差地别,
    真实门槛要看 dofollow 数,不是总数**——这条比总数差异更重要,`sources/gefei-kd.md` 已有的
    "Semrush 引用域实测低估达 16 倍"结论现在多了一个更细的推论:**`gefei-kd` 的插值预算量级上更接近
    dofollow 数,而不是总引荐域名数**(35 vs 10 同量级、80 vs 67 同量级),只有 glb-to-stl 例外。

    **glb-to-stl 例外的原因,而且这条修正了 08-14/08-15 早些时候的排序假设**:
    magic3d.io 不是单功能站,是"Free AI Creative Studio"(417 个已抓取页面,多个 AI 生成功能),
    902 个 dofollow 域名是**整站**多年积累的域权重,glb-to-stl 只是它其中一个长尾页面在蹭站内权重,
    **不代表挑战这个词需要 900 个域**——这个"最弱竞品"其实不是一个真正可比的单功能对标站,
    Step 5a/5b 的方法论假设("挑最弱的那个站当参照")在这个词上失效了,因为它筛出的是"大站的小页面",不是"小站的主页面"。

    **stl-repair 和 3mf-to-stl 的对标站是真正可比的**(都是单功能小站,和 partfit3d 同类型):
    - `justfixstl.com`:DR14、6 个月新站、**只用 10 个 dofollow 域名**就排到 stl-repair 第 2 位——
      这是三个词里唯一有"小站真实做到了"这个直接证据的,**门票比想象中低得多**
    - `imagetostl.org`:DR25、**67 个 dofollow 域名**排进 3mf-to-stl 前排——量级明显高于 stl-repair,
      但仍在"单站可积累"的区间内,不是遥不可及

    **结论:排序不变,但置信度和成本认知都更新了**:
    1. **stl-repair 维持第一优先级,而且比 08-14/08-15 早些时候预期的更划算**——真实门票只要约 10 个 dofollow 域名,
       这是本轮三个数字里最扎实的一个(单功能对标站直接实测)
    2. **3mf-to-stl 的真实成本(67 个 dofollow 域名)比 `gefei-kd` 估算(80)更低,也比"目录型放大到 200-480"温和得多**——
       这条**弱化了此前"要不要动用 $2-5K 外链预算"的顾虑**,67 个域名量级用免费/低成本渠道(现有渠道池+outreach)
       也有希望够到,不一定需要升级到大站级付费预算,值得先按现有免费节奏试,不够再考虑加钱
    3. **glb-to-stl 的"最弱竞品"数据失真,不能用它判断真实门槛**——建议维持"顺手做、提前卡位"的低优先级定位不变,
       但不要再用 magic3d.io 的数字做任何预算判断;真实门槛需要等页面上线后用 GSC 实测,或换一个更小的单功能站重新筛一次最弱竞品

    **产出**:三个候选优先级排序最终确认为 stl-repair > 3mf-to-stl > glb-to-stl 不变,
    但 3mf-to-stl 的外链预算顾虑基本解除(可先按免费节奏推进),glb-to-stl 的最弱竞品判断方法论存在缺陷,
    需要在下次用 Step 5a/5b 判"最弱竞品"时补一条边界:**先确认该竞品是单功能站还是大站的一个子页面,是后者就换一个**。

  - **2026-08-24 · partfit3d TDK 中期读数(9/14 天)与测量口径裁决(数据源:`scripts/gsc.py` API 实拉 = 真值)**

    **一句话**:**还不能判定(窗口 9/14 天),但 08-15 挂着的口径缺陷现在定掉了 —— 而且结论跟当时想的相反。**

    **① 时间:数据只到 08-22,回收日 08-30 不变**

    逐日实测:08-22 有数据,08-23 返回「无数据」→ GSC 延迟约 2 天。
    窗口 08-14~08-27,**最早 2026-08-29/30 拉得到完整对比**,08-15 定的 08-30 回收日期准确,不需再顺延。

    **② 口径裁决:选 ②(page 维度只看 `/`),并推翻 08-15 对 ② 的定性**

    | 页面 | title | 改前 07-31~08-13(14天) | 改后 08-14~08-22(9天) |
    |---|---|---|---|
    | `/` | ✅ **新** | 15 点击 / 960 曝光 / **1.6%** / pos 10.3 | 15 点击 / 874 曝光 / **1.7%** / pos 9.1 |
    | `/tools/3mf-splitter-online/` | ❌ **旧**(始终没动) | 12 点击 / 1644 曝光 / **0.7%** / pos 9.6 | 4 点击 / 1984 曝光 / **0.2%** / pos 10.4 |

    08-15 把选项 ② 记成「保住干净归因,**但样本减半**」——**这个定性错了**。
    旧 title 那页一直没改,它是同站、同词族、同期曝光同涨的**天然对照组**;
    page 维度不是样本减半,是**多拿到一组差分**。反过来,选 ① 去同步另一页的 TDK 会**毁掉这个对照组**,因此 ① 明确否掉。

    > **可复用的方法论(下次设单页 SEO 实验时先想一遍)**:同站同词族里有一个"忘了改"的页面,
    > 不是污染源而是免费对照组 —— 判断前先问"这个未处理页能不能当 control",再决定要不要把它也改掉。

    **③ query 维度确实读不出东西(08-15 的预判兑现)**

    `split 3mf` 改后 9 天:**4 点击 / 1515 曝光 / CTR 0.3% / pos 8.8** —— 与改前基线 0.3% **完全一致**。
    原因就是曝光被两页分掉,且旧 title 那页曝光(1984)反而压过新 title 那页(874),加权后新文案的信号被稀释掉了。
    **08-30 判定不能用 query 维度。**

    **④ 中期信号:CTR 持平,但点击速率上升;对照组同期塌了**

    | 指标 | `/`(实验组) | `/tools/...`(对照组) |
    |---|---|---|
    | CTR 改前 → 改后 | 1.6% → **1.7%**(持平) | 0.7% → **0.2%**(腰斩) |
    | 点击/天 | 1.07 → **1.67**(+56%) | 0.86 → **0.44**(−49%) |
    | 曝光/天 | 68.6 → 97.1(+42%) | 117.4 → 220.4(+88%) |

    按 08-15 写下的判定纪律(「CTR 持平但点击明显上升,不判 NO-GO」),实验组这一档是过的。
    对照组「曝光大涨而点击下降」正好是纪律里预设的那个现象——**曝光爬坡期新增长尾低意图曝光天然压 CTR**;
    实验组顶住了这个压力,对照组没顶住。

    **⚠️ 这不是结论,差分还不干净**:两页平均位置**走向相反**(`/` 10.3→9.1 变好,对照 9.6→10.4 变差),
    位置变化本身就能解释一部分 CTR 差。**08-30 判定必须同时记两页的位置变化**,否则会把排名红利算成文案功劳。

    **⑤ trailing slash bug 仍未修**

    页面报表里 `/tools/3mf-splitter-online/` 现在是**带斜杠**的(08-15 记录的是不带),
    且 `how-to-split-stl-for-3d-printing` 带/不带斜杠**仍各占一行**(52 + 79 曝光)。
    [08-11 诊断](#结果记录)的问题至今没动,持续在分散信号。

  - **2026-08-25 · 哥伦布全库普查(数据源:Columbus MCP,快照 2026-07,第三方估算)——两个结论,一个否定一个修正**

    **动作出口**:用户要"看 AI 关键词榜单找有机会的站"。因 08-11 / 08-13 已在同一个库撞过两次墙,
    本轮**不翻榜**,改跑一个可证伪的口径:`list_keywords(sort="cpc")` 对全库按 CPC 倒序排一遍,
    问「这个库的付费天花板到底在哪」。结论已封顶,回写 [risks.md CPC 系统性偏低](risks.md#ai-工具站品类的-cpc-系统性低-1-2-个数量级用它找付费生意是池子选错违反公理-4)。

    **① 对 partfit3d 这条线,哥伦布完全无覆盖**:`list_keywords(contains="stl")` → `totalMatched=0`。
    整个 3D 格式转换/修复词族**一个词都不在这个库里**。含义:**partfit3d 的选词不要再来这里找**,
    继续走 Semrush + `gefei-kd` + Trends 三源。这一条以前没验证过,今天算是把边界划清了。

    **② 修正 08-14「AI 生成 3D 爆发带出下游刚需」的时点判断——上游正在降温,不是在爆发**

    库里只有 3 个 3D 相关词,`ai 3d model generator`(29,410/月 CPC $1.71)命中站的 07 月快照:

    | 站 | 月访问 | 环比 | 自然搜索占比 | 注册 |
    |---|---|---|---|---|
    | `ideal.house` | 680,663 | **+10.0%** | 64.4% | 2025-01 |
    | `fast3d.io` | 150,101 | **−18.7%** | 59.4% | 2025-05 |
    | `magic3d.io` | 101,423 | **−21.1%** | 64.9% | 2025-09 |

    三家里两家在两位数下滑,`magic3d.io` 正是 08-15 那条 902 dofollow 域名失真读数的来源站。
    **这不否定 `glb to stl` 页面(它 KD 3-11、成本 1-2 小时、复用现有技术栈,顺手做仍划算),
    但要下调对"早期爆发窗口"的期待**——08-14 的解读建立在 Trends 上升榜(相对值、无量级),
    现在有了绝对量级,上游生成器品类的 07 月快照是**收缩**的。
    **排序维持第三不变,但定性从「提前卡位早期增量」改为「低成本补齐工具矩阵拼图」**,
    不要因为它而挤掉 stl-repair 的数据回收。

  - **2026-08-25 · partfit3d trailing slash 修复上线(agent 执行 + 生产 curl 实测 = 真值)**

    **动作出口**:解掉拖了 4 个数据周期的 674 曝光信号分散问题。commit `76432be`,Worker 版本 `93dd1b48`。

    **307 的根因不是 Cloudflare,是 TanStack Router** —— `router-core/dist/esm/redirect.js:3` 的
    `statusCode = opts.statusCode || opts.code || 307`,**没有配置开关**。
    解法:在 Worker 入口 `src/server.ts` 于请求进 router 之前拦截,返回 301。
    两个守卫:根路径 `/` 不跳;只对 GET/HEAD 用 301(POST 用 301 会被客户端改写成 GET)。

    **`og:url` 不需要单独修** —— `src/lib/seo.ts` 的 `seo()` 一次算出 url,
    同时喂 `rel=canonical`、`og:url`、`twitter:url`,改 `getCanonicalUrl()` 一个函数覆盖全部。

    **生产实测(2026-08-25 部署后)**

    | 检查项 | 结果 |
    |---|---|
    | `/tools/stl-repair/` | **301** → `/tools/stl-repair`(原为 307) |
    | `/guides/how-to-split-stl-for-3d-printing/` | **301** → 去斜杠版 |
    | `/` | 200,**不跳转**(根路径守卫生效) |
    | canonical / og:url | 均不带斜杠,与返回 200 的地址一致 |
    | sitemap 全部 `<loc>` | 去斜杠,根路径保留 `/` |
    | `/tools/3mf-to-stl`、`/tools/stl-to-3mf` | 200,同批上线 |

    **同批发布的还有**:两个转换页(1,064 行,08-14 定的方向,同样是"写了没发")+ navbar/homepage/footer
    等界面改动。`/tools/3mf-splitter-online` 加了指向转换页的内链,但**未碰 `seo()` 的 title/description**
    —— TDK 实验的自变量没动,且窗口 08-27 就结束,Google 来不及重抓到影响读数。

    ⚠️ 两个转换页及其依赖仍是**未跟踪文件 —— 已部署但未入 git**。

    **复查节点**:GSC 重新提交 sitemap;2-4 周后查 9 对重复 URL 是否合并,
    重点看 `how-to-split-stl-for-3d-printing`(合并前 249+244 曝光分别趴在 pos 44.1 / 41.8)。

  - **2026-08-25 · partfit3d 词族意图诊断(数据源:GSC 网页版导出 xlsx 07-30~08-22 = 真值 + split3mf.com / SERP 实读)——推翻 TDK 实验的前提**

    **动作出口**:回答用户「这样子的数据还有什么优化」。结论直接改写 08-30 TDK 判定的读法,
    并成为[「颜色拆分功能」实验](#partfit3d-颜色拆分功能a-路线2026-08-25-立项)的立项依据。

    **① 88% 的曝光押在一个不属于自己的词上**

    24 天(07-30~08-22)站点合计 **52 点击 / 6,093 曝光 / CTR 0.85%**。查询表 4,315 曝光拆族:

    | 词族 | 曝光 | 点击 | CTR |
    |---|---:|---:|---:|
    | `split 3mf` / `split 3 mf` 主词 | 3,012 | 9 | **0.30%** |
    | 品牌错拼族(25 个) | 775 | 6 | 0.77% |
    | 修复类(`stl repair` 等 25 词) | 30 | 0 | — |
    | 拆分 / `cut stl` 类(72 词) | 415 | 5 | 1.2% |

    错拼族:`spli3mf` `slit3mf` `slipt3mf` `splt3mf` `spilt3mf` `plit3mf` `split3ms` `sprit3mf`
    `www.split3mf.com`。**没有人会把通用需求打错成 `spli3mf`** —— 这 775 曝光是纯导航意图,在找牌子。

    **② 更致命的是意图错配,不是文案**

    实读 split3mf.com:它做的是**把上色的 3MF 按颜色拆成多个零件(AMS 多色打印)**,
    partfit3d 做的是**按平面切开放不下的模型**。`split 3mf` 的 SERP 前排
    (split3mf.com / [PlainMesh](https://www.plainmesh.com/tools/fill-and-split) /
    [Obloid](https://obloid.app/tools/color-3mf-splitter) /
    [PrintNexus](https://printnexus.io/tools/free-3mf-splitter) /
    [ColorSplit3mf](https://github.com/mocsy/ColorSplit3mf))**全是颜色拆分**。

    > **partfit3d 在第 8.9 位拿 0.3% CTR,不是标题不够吸引人,是搜的人要的东西站上没有。**

    **③ CTR 塌陷 100% 集中在巴西 + 意大利**

    | 分组 | 曝光 | 点击 | CTR |
    |---|---:|---:|---:|
    | 巴西 + 意大利 | 3,385(**55.6%**) | 12 | **0.35%** |
    | 其余 101 国 | 2,708 | 40 | **1.48%** |

    其余国家在 pos ~9 拿 1.48% 是**正常水平**,异常只在那两国。而 split3mf.com **带 pt / it 语言版本**,
    partfit3d 纯英文 —— 品牌导航 + 语言错配两个因素叠在同一批曝光上。

    **④ 对 08-30 TDK 判定的硬约束(必须执行)**

    即便实验组读出 GO,`split 3mf` 的 CTR 天花板已被意图错配锁死,
    **不能把 GO 外推成「这套文案可以复制到别的词」**。TDK 从"主要抓手"降级为"顺手做过的一次微调"。

    **⑤ trailing slash 的真实状态订正:不是"没修",是"修完忘了发"**

    9 对重复 URL 合计 674 曝光(`how-to-split-stl-for-3d-printing` 249+244=493 是最大一处,
    两个都趴在第 4-5 页)。但 curl 实测 + 读 `~/space/partfit3d` 仓库发现:
    `src/lib/urls.ts` 与 `src/routes/sitemap[.]xml.ts` 的去斜杠逻辑**已经写好但从未提交**
    (working tree `M`,最后一次提交 `00cb9ef` 不含它们)。线上仍是旧构建:
    canonical / og:url / sitemap 全带斜杠,而带斜杠的 URL **307** 跳向不带斜杠版 ——
    canonical 指着一个会跳走的地址,Google 直接丢弃后自行猜测。还差一步:**307 改 301**。

    另发现 `src/routes/tools/3mf-to-stl.tsx`、`stl-to-3mf.tsx`、`src/lib/stl-export.ts` 是未跟踪文件
    —— 08-14 定的转换页也是**写了没发**。

    > **可复用教训**:待办标"未完成"之前先 `git status` 一眼。这条拖了 4 轮数据周期
    > (08-11 诊断 / 08-15 复现 / 08-24 复现 / 08-25 再复现),实际代码早就写完了。

    **⑥ 顺带两条**

    - **首页在蚕食工具页**:`/` 1,834 曝光 / 30 点击 / **1.64%** / pos 9.74;
      `/tools/3mf-splitter-online/` 3,628 曝光 / 16 点击 / **0.44%** / pos 10.05。同词族两页互相稀释,
      首页转化好 3.7 倍。**但工具页是 TDK 对照组,08-30 拉完数再合并。**
    - **`/printers/` 31 页 = 161 曝光 / 2 点击**(2.6% 曝光占了 1/3 页面数),多数 0 点击,还含 5 对斜杠双份。
      薄内容吃抓取预算,对后续申 AdSense 也是负分。建议合并成一张「打印机幅面对照表」单页。

  - **2026-08-15 · partfit3d TDK 实验中期检查(数据源:`scripts/gsc.py` API 实拉 = 真值 + curl 实读页面)**

    > **⚠️ 2026-08-24 部分订正**:本条 ② 里对「选项 ②(page 维度)= 样本减半」的定性已被推翻,
    > ③ 里锁的 query 维度基线(1,245 / 4 / 0.3% / 9.1)随口径改为 page 维度而作废。见上一条。

    **一句话**:**这轮实验现在读不出结果,而且实验设计有一处必须先修的缺陷。**

    **① 时间上:有效数据 0 天**

    | 事件 | 日期 |
    |---|---|
    | title/description 代码上线 | 2026-08-12 |
    | Google 用新标题重抓(`gsc.py inspect` 的 `lastCrawlTime`) | **2026-08-14 10:20 UTC** |
    | GSC 数据可用截止(逐日实测,08-13/08-14 均返回「无数据」) | **2026-08-12** |

    重抓已确认(解掉 [todos.md](todos.md) 那条阻塞项),但**重抓之后一天数据都还没进 GSC**。
    14 天窗口真正起点 = **2026-08-14**,终点 2026-08-27,加 GSC 2-3 天延迟,
    **最早 2026-08-30 才能拉到完整对比**。todos 里占位的 08-26 回收日期要顺延。

    **② 设计缺陷:改的页面不是曝光最大的那一页**(本条最重要)

    curl 实读两页当前 title:

    | 页面 | title | 08-06~08-12 曝光 | 平均位置 |
    |---|---|---:|---:|
    | `/` | `Split 3MF to Fit Your Printer — Free Online Tool` ✅ **新** | 795 | 10.1 |
    | `/tools/3mf-splitter-online` | `Split 3MF Files Online — Free 3MF Splitter (No Upload) \| PartFit 3D` ❌ **旧** | **972** | **9.1** |

    同期 `split 3mf` 单词 1,026 曝光 —— **这个词的曝光被两页分掉了**,而**没改的那一页曝光更多、位置更好**。
    两页是真正的两个页面(H1 不同、canonical 各自指向自己),不是同一页的两个 URL。

    **后果:14 天后按 query 维度拉出来的 `split 3mf` CTR,是新旧两套标题的加权混合,归因不成立。**
    要么把 `/tools/3mf-splitter-online` 的 TDK 同步成同一套口径(测"这套文案有没有用",牺牲 A/B 对照),
    要么改用 **page 维度只看 `/`**(保住干净归因,但样本减半)。**这个选择必须在 08-30 拉数之前定。**

    附带发现:`/tools/3mf-splitter-online` 的 canonical 仍是**带斜杠**版本,而 URL 不带 ——
    [08-11 诊断的 trailing slash 冲突还没修](#结果记录),和 08-15 在 `/tools/stl-repair` 上看到的是同一个模式。
    页面级报表里 `/guides/how-to-split-stl-for-3d-printing`(82 曝光)与其带斜杠版(125 曝光)**各占一行**,
    这是该 bug 在流量侧分散信号的直接证据。

    **③ 基线要重锁,旧的那个偏低 2.7 倍**

    | 基线口径 | 曝光 | 点击 | CTR | 平均位置 |
    |---|---:|---:|---:|---:|
    | 记录里在用的(07-27~08-09) | 459 | 1 | 0.2% | 9.4 |
    | **改前最后 14 天(07-31~08-13,应作为新基线)** | **1,245** | **4** | **0.3%** | **9.1** |

    用旧基线去比会得到假性利好。**08-30 判定时必须用 1,245 / 4 / 0.3% / 9.1 这组。**

    **④ 曝光仍在爬坡,是最大的归因污染源**

    非重叠周对比(`split 3mf`):

    | 窗口 | 曝光 | 点击 | CTR | 平均位置 |
    |---|---:|---:|---:|---:|
    | 07-30 ~ 08-05 | 219 | 0 | 0.0% | 9.7 |
    | 08-06 ~ 08-12 | **1,026** | **4** | 0.4% | 8.9 |

    **+369% 曝光,位置只从 9.7 微升到 8.9**,且这全部发生在改 title **之前**。

    > 顺带解掉 [todos.md 08-18 复拉待办](todos.md) 的一半:**~3,780 曝光/月 不是一次性尖峰,还在往上走。**
    > 复拉 08-02~08-08 得到 `split 3mf` 276 曝光,与 08-11 当时记录的数字**完全一致** ——
    > 说明不是 GSC 数据回填造成的错觉,**是真实增长**。

    **判定纪律(写在前面,免得 08-30 自我欺骗)**:曝光暴涨期新增的多是更长尾、更低意图的曝光,
    **天然压低 CTR**。08-30 判定不能只看 CTR 百分比,**必须同时看点击绝对数**;
    若 CTR 持平而点击数明显上升,不能判 NO-GO;若 CTR 上升但曝光同时腰斩,也不算 GO。

    **⑤ 一个已经能读的正向信号(与 title 无关)**

    `split 3mf` 点击 0 → 4,`split3mf` 0 → 2。这个站**从"排在第一页但一次点击都没有"变成了有点击**。
    但这是曝光基数放大带来的,不是文案带来的 —— 改动那时还没生效。

    另:`split3mf`(无空格)CTR **2.1%** @ pos 6.6,而 `split 3mf`(有空格)只有 0.3% @ pos 9.1。
    同站同页,差 7 倍。位置差 2.5 位解释不了全部差距,**头词 SERP 上方的 AI Overview / 精确匹配工具站
    截流才是主因** —— 与 08-12 SERP 实查的结论一致,再次说明 title 不是唯一变量。

  - **2026-08-26 · partfit3d 变现侧竞品盘面(数据源:[支付引荐表](sources/payment-growth.md) 第三方估算 + gefei-kd + 站点实读)——A 路线解决不了的那一半**

    **动作出口**:回答用户「下一步计划是什么」。结论不改 A 路线的执行,但**补上它的盲区**:
    A 路线的 GO 标准(CTR ≥1.5%)是流量指标,拿到 GO 收入仍是 0。

    **① 转换/拆分是别人的免费获客资产,不是产品**

    用支付引荐表反查 Lemon Squeezy,`3daistudio.com`(AI 3D 生成,自报 ARR $3.3M,整站 72 万月访问
    且 `sustained_growth`)位次 189→12。开站实读:它的 `/convert` 下有 **56 个页面,39 个命中 3mf/stl/glb**,
    标题即 `Free, Private, No Signup`,**浏览器本地跑,服务器成本 0**。
    它的钱挂在转换完成页的意图转向 CTA:`Need a new model to print, not just a new format?`

    不是孤例:`3mf to stl` 的 SERP 第 2 名是 `meshy.ai`(DR 75),同一种商业模型。
    **面对的是一整类 AI 3D 生成商——转换对它们是获客成本,不是收入。** 已记入
    [risks.md 「免费 loss-leader 挤压」](risks.md#免费-loss-leader-挤压你的整个产品是别人的获客成本违反公理-4--准公理-b)。

    **② `3mf to stl` 前十盘面(gefei-kd,2026-08-26,force 重算)**

    难度 **46.2/100**,链接预算 **50–110 个引用域(中值 75)**,对应 **DR 30** 量级。
    9/10 是专门为这个词做的页面 —— 正面争夺的红海词,不是"大站顺路排名"。
    但有缝:第 8 名 `triposrai.com` **DR 仅 13**、体验分 27 垫底(停留 19s)、域龄 2.3 年,是脆弱占位者。

    | # | 域名 | DR | 月流量 | 备注 |
    |---|---|---|---|---|
    | 1 | imagetostl.com | 48 | 149 万 | 垄断第一,该词单站拿约 1.7 万 |
    | 2 | **meshy.ai** | 75 | 2518 万 | AI 3D 生成商,免费送转换 |
    | 4 | convert3d.org | 37 | 64 万 | |
    | 8 | **triposrai.com** | **13** | 4.2 万 | 最弱占位者 |
    | 9 | imagetostl.org | 22 | 11 万 | 域龄 14 个月 |

    **③ 搜索量口径再次打架(第三次)**

    `3mf to stl`:Semrush **4,400/月 KD 19** vs gefei-kd **2.5 万/月 难度 46.2** —— 量差 5.7 倍、难度差 2.4 倍。
    同型分歧此前已出现两次。**取方向不取绝对值,真值只能靠 GSC 单页实测。**

    **④ 对 A 路线的硬约束(不改执行,只补口径)**

    A 路线即便 GO,证明的也只是「补功能能把曝光转成点击」,**不能外推成「这条线能赚钱」**。
    变现出口必须并行准备,否则 09-08 拿到 GO 后仍是 0 收入。
    当前唯一低成本出口:**在拆分/转换完成页接 3D 打印服务联盟**(Craftcloud / JLC3DP / Treatstock)——
    那是用户唯一一次明确知道自己接下来要打印的时刻。**明确不要做**:给转换/拆分本身加收费墙。

  - **2026-08-26 · aidepixelate 选词复盘:词错了,产品没错(数据源:GSC = 真值 + gefei-kd + SimilarWeb 关键词概览 + 哥伦布,后三者第三方估算)**

    **动作出口**:回答用户「能赚钱的是不是要看第五个站」。结论是**不必建第五个站**——
    aidepixelate 的产品与收款已建成,缺的是把它指向对的词族。

    **① 站点真实状态(GSC 近 28 天 2026-07-27~08-23)**

    16 点击 / 约 1,100 曝光,主力词位置 **60–90 位**(第 7–9 页)。
    唯一进过前 5 的 `depixelate` **从 pos 4.0 掉到 26.7**(前后两个 14 天窗口对比)。
    产品侧:**积分包一次性购买,不是订阅**——Free 每天 2 张 / $4.90-100 credits / $12.90-400 / $29-1,200,
    credits never expire,通道 Waffo。**用户 2026-08-26 确认:今天才配好收款,零付费用户,且无新增用户。**
    → **付费闭环是"建好但未验证",不是资产。**

    **② `depixelate` 这个词选错了两次**

    - **量太小**:哥飞盘面 **SERP 只有 7 条**凑不满十;「未能从排名站点的主力流量词中取得该词搜索量」;
      「前十中 7 个有关键词数据的域名,主力流量词均不包含此词」。前七名是 picsart / canva / airbrush /
      github / pixelcut / reddit / photogrid,**全是大站顺路内页,没人专门经营**。工具自己警告"体量过小的词不值得做"。
    - **意图脏**:用户实测反馈——本意做老照片修复,**后台收到大量打码色情图**。
      技术上做不到(打码是信息销毁不是隐藏),合规上不能碰。**用一个吸引 NSFW 的词,去承接一个老照片修复的产品。**

    **③ 正确词族就在旁边:photo restoration(SimilarWeb 关键词概览,2026-08-26)**

    | 词 | 近 6 月搜索量 | 24 月均值 | 难度 | CPC |
    |---|---|---|---|---|
    | photo restoration | 6.5K–12.8K | 13,120 | 66 | $0.01–**5.83** |
    | old photo restoration | 6.2K–10.1K | 11,444 | 67 | $0.01–**5.26** |
    | restore old photos | 4.2K–9.9K | 15,252 | 62 | $0.01–**5.26** |

    比 `depixelate` 大一个数量级,且 **CPC 高**——落在带明确付费意愿的一侧,
    与 [profile.md 2026-08-11 决策](profile.md#硬约束)(自有收款 > 联盟 > AdSense)方向一致。
    aidepixelate 站上写的本来就是 "photo restorations"。

    **④ 推翻了哥飞给的"最强证据"——按 [risks.md 流量与产品不同源](risks.md) 纪律复核**

    哥飞称 `ezenhancer.ai`(DR 14 / 域龄 8 个月 / 132 万月流量 / 排第 6)是"此词可做的最强证据"。
    **查它的头部词后不成立**:主力词是 `image enhancer` 38.5 万、`photo enhancer` 26.3 万、
    俄语 `улучшить качество фото` 14.7 万 —— **它靠的是 image enhancer 大词族 + 12 种语言,不是老照片修复**。
    另两条:**1,400 个引用域**(不是零外链自然起量);`pricingHints: ["Free"]`、`paymentProviders` 为空——**至今不收钱**。
    → 它证明"能拿流量",不证明"这个词能做",更不证明"能赚钱"。这条差点被当成决策依据,**纪律生效了一次**。

    **⑤ 由此沉淀的方法论**

    → [principles.md「用 CPC 分层识别付费意愿」](principles.md#用-cpc-分层识别付费意愿大流量低-cpc-是免费用户池)。
    四站 0 收入的共同根因:选词只看"能不能排上去",**从未看过 CPC**。

    **⑥ 待定的下一步(未立项)**

    两个站现状:partfit3d 有流量无收费点;aidepixelate 有产品+收款无流量。**两个都无法验证收入。**
    但 [profile.md](profile.md#阶段目标) 写明当前最优先验证能力是「找需求 + 付费意愿」,
    而 **SEO 是验证付费意愿最慢的渠道**(3–6 个月,与"3 个月内看到有效反馈"的硬约束冲突)。
    候选路径:用现成产品到需求聚集地(修复类社群/求助帖)做零成本付费意愿验证,
    拿到第 1 笔收款再决定要不要为 photo restoration 词族投入 SEO。**待用户裁决后立项。**

## partfit3d 颜色拆分功能(A 路线,2026-08-25 立项)

- **状态**:running
- **关联方向**:[themes.md 英文 SEO 工具站矩阵](themes.md)
- **立项依据**:[2026-08-25 词族意图诊断](#结果记录)——`split 3mf` 的 SERP 意图是「按颜色拆分上色 3MF」,
  partfit3d 只做「按平面切开」,所以在第 8.9 位只能拿 0.3% CTR
- **待验证假设**:**补功能比补排名快**。站上已有 ~3,000 曝光/月 卡在 pos 9,
  把颜色拆分做出来能把这批现成曝光转成点击;而 `/tools/stl-repair` 要从 pos 65 爬到 pos 10 需要外链和时间
- **时间盒**:2 周,至 **2026-09-08**
- **预算上限**:0 元
- **成功标准(GO)**:上线后 14 天,`split 3mf` 词族在 **page 维度** CTR 从 0.3% → **≥1.5%**(约 +35 点击/月)
- **失败标准(NO-GO)**:CTR 仍 <0.8% → 说明这批曝光是纯品牌导航(在找 split3mf.com 这个牌子本身),
  功能补齐也拿不到 → 转 **B 路线**,全力做 [stl-repair 词族](#结果记录)

### 技术现状与四步

`src/lib/three-mf.ts`(138 行)现在:JSZip 解包 + three 的 `ThreeMFLoader` 读几何,**上色数据整个丢掉**;
导出写的是裸 `<triangle v1 v2 v3/>`,无任何颜色。要补:

1. **读** — 自己解 `3D/3dmodel.model`(Bambu/Orca 拆分文件还要读 `3D/Objects/object_*.model`),
   抓 `<triangle>` 上的 `paint_color`(Bambu/Orca)或 `slic3rpe:mmu_segmentation`(Prusa)。
   两者**编码相同**,只是命名空间不同。`ThreeMFLoader` 不给这个,必须并行解一遍 XML。
2. **解码** — 该属性不是挤出机编号,是**位打包的递归三角形细分**编码:短值(`"4"`/`"8"`)= 整片着色,
   长 hex = 三角形内被笔刷切成子区域。**无官方文档**([PrusaSlicer #13900](https://github.com/prusa3d/PrusaSlicer/issues/13900) 就是在要这份文档,至今没有)。
3. **分组** — 按挤出机 id 把三角形分堆 → 每堆一个 `BufferGeometry`。比现有的平面切割**简单**,不需要求交。
4. **导出** — 扩 `exportThreeMf`,用官方 **Materials & Properties Extension `<m:colorgroup>`**(可移植)。
   ⚠️ 坑:Bambu Studio **按顺序**把 color group 映射到 AMS 槽位(group 0 → 槽 1),不是按 hex 值。

### 三个风险点

1. **三角形索引对不上**(最大风险)——`ThreeMFLoader` 可能重排/合并顶点,而 `paint_color` 按原始三角形顺序给。
   MVP 建议**绕开 loader**,直接从 XML 建几何。
2. **子细分三角形** —— MVP 只处理整片着色,遇长 hex 取**主导颜色**近似,页面明说"请在切片器里核对"。
3. **不封盖** —— 拆出的色块是开放壳不是实体,竞品(Obloid)会封盖成可打印实体。MVP 可不封,但必须写明。

### ⚠️ 授权约束

[ColorSplit3mf](https://github.com/mocsy/ColorSplit3mf) 是 **GPL-3.0**,PrusaSlicer 的 `TriangleSelector` 是 **AGPL**
—— **只能读思路,不能抄代码**,否则整站要跟着开源。
参考实现看 [mmu-remapper](https://github.com/monomyth/mmu-remapper)(同时处理两种属性形式),用前先确认其 license。

### 页面安排与时序

- **主战场** = `/tools/3mf-splitter-online/`(3,628 曝光)和 `/`(1,834 曝光),做成同一页的一个模式,
  直接转化已有排名;
- 是否另开 `/tools/3mf-color-splitter/` 吃颜色词族(`3mf color splitter` / `split 3mf by color` /
  `separate colors 3mf`),**待查量级后定**。
- **时序冲突的解法**:`/tools/3mf-splitter-online/` 是 TDK 实验对照组,08-30 前动它会污染读数。
  但这个功能本来也做不完 5 天 —— **现在建,08-30 读完数再上线**,不需要提前砍实验。

### 执行步骤

- [x] Step 0 · 已决定另开 `/tools/3mf-color-splitter` 独立页;颜色词族量级仍待补查,只用于判断独立页 SEO 预期,不再影响页面形态
- [x] Step 1 · 已实现颜色数据解析与自建几何(线上页面宣称支持 Bambu Studio / OrcaSlicer / PrusaSlicer)
- [x] Step 2 · 已实现按色分组、封盖、连接件与 colour-tagged 3MF / STL 导出
- [x] Step 3a · 2026-08-26 独立页 `/tools/3mf-color-splitter` 已上线
- [ ] Step 3b · 08-30 TDK 读数后,把颜色入口接到已有曝光页 `/tools/3mf-splitter-online/` 与 `/`;在这一步完成前,原假设「转化现成 ~3,000 曝光/月」尚未开始验证
- [ ] Step 4 · Step 3b 上线后重新锁 14 天窗口,按已有曝光页的 page 维度拉 GSC 判 GO/NO-GO;独立页因新上线、无基线,单独看收录 / query / 点击,不与旧页混算

### 结果记录

- 2026-08-25:立项。
- 2026-08-26:用户确认颜色拆分已上线。浏览器生产验收确认:
  - 独立页 `https://partfit3d.com/tools/3mf-color-splitter` 返回正常,canonical 自指;title = `Split 3MF by Color Online — Free Color Splitter | PartFit 3D`,H1 = `Split a Painted 3MF by Color`,GA4 已加载。
  - 站内三色样例成功进入结果态:识别 Standard 3MF colour groups,拆成 3 个 filament parts,分别显示 5 / 8 / 3 个 triangles、seams capped、watertight;colour-tagged 3MF 与 3 STL ZIP 下载按钮均启用。
  - **边界校准**:已有曝光页 `/tools/3mf-splitter-online` 线上仍是「按平面切成 printable parts」,没有颜色模式,仅页脚新增独立页链接。因此「功能做完」已完成,但「用功能承接现成 `split 3mf` 曝光」尚未完成;不能从独立新页上线日直接启动原 CTR 实验。
- 2026-08-26:三类真实涂色 3MF 线上端到端验收(产品仓库只读,夹具与下载产物位于 `/private/tmp/partfit3d-color-e2e-20260826/`):
  - **Bambu PASS**:官方 BambuStudio issue #2411 的复杂文件(`Application=BambuStudio-01.07.04.52`,约 163,947 个 `paint_color`)成功拆成 2 个 UI-watertight parts;输入 slot 颜色 `#FFF144/#161616` 保留;实际下载的 3MF 含 2 bases/2 objects 且 pindex 正确,STL ZIP 含 2 文件。
  - **Orca PASS**:官方 OrcaSlicer issue #12426 的最小复现文件(12 个 `paint_color`)成功拆成 2 个 parts;3MF/STL ZIP 实际下载成功;独立边检查两件均 boundary=0、nonmanifold=0、无重复三角。该文件没有 slicer 颜色配置,使用 fallback 色属合理。
  - **Prusa 产品级 FAIL**:官方 PrusaSlicer issue #7134 文件(`Application=PrusaSlicer-2.4.0-alpha3`,45,893 个 `slic3rpe:mmu_segmentation`)约 5 秒解析成 3 parts并可下载,但存在三项错误:① 输入 slot 2/3/5 的 `#00FF00/#FF8000/#FFFF00` 被替换成 fallback 色;② 导出 STL 的三件分别有 2/14/5 条 multiplicity=4 非流形边及 9/14/3 组重复三角,页面仍误报 watertight;③ UI 把 Prusa `mmu_segmentation` 错标为 `paint_color`。
  - **GUI 重导入 BLOCKED**:本机未安装 Bambu Studio / OrcaSlicer / PrusaSlicer,未验证导出物在三款 GUI 中的重新导入;不得把「下载结构正确」外推成 GUI 兼容性已通过。
  - **修复顺序**:先补 Prusa `Slic3r_PE.config` filament colour 分号列表并按原 slot index 映射;再把拓扑判定从只看 open edges 扩为 `edge multiplicity != 2` + 重复/重叠三角;最后按实际属性显示 source label。修完后复跑同三件夹具,再考虑推广与接入已有曝光页。

## SEO 工具站 Starter Kit(BIP 卖铲子,2026-08-11 桌面筛选完成)

- **状态**:planned(只批准 48 小时预售,未批准产品开发)
- **关联方向**:[themes.md SEO 工具站 Starter Kit](themes.md#seo-工具站-starter-kit--自动防错规则)
- **待验证假设**:AI 建站的独立开发者会为「工具站上线底座 + SEO 发布防错」支付一次性费用,
  且 Build in Public 内容能带来首批名单和预售。
- **唯一 GO 标准**:48 小时内获取 **≥3 个非熟人有效邮箱 + ≥1 笔 $19 refundable deposit**。
  只有点赞、投票、口头说想要均不算 GO。
- **NO-GO 标准**:触达 15 个明确在做工具站的人后,0 deposit;停止开发,保留内容素材。
- **预算上限**:预售 $0-10;GO 后 MVP 现金 $10-40,总工时 32-40 小时(约两周)。

### 桌面筛选结论

| 候选 | 直接信号 | 反证 | 判定 |
|---|---|---|---|
| App Store 拒审预检 | AcceptMyApp $29.99/单 App、$149/年 | 已覆盖清单、风险、拒审回复、截图 | NO-GO,正面占位 |
| RevenueCat 配置 doctor | 订阅 App 痛点强 | RevenueCat 2026 AI Toolkit 已能诊断常见配置 | NO-GO,官方下场 |
| 通用移动 UI / 增长组件包 | NativewindUI $99/季、$299 终身;3,000+ devs 自报 | WithFrame / NativewindUI 已含 paywall、onboarding | NO-GO,需堆数量 |
| 通用 SaaS boilerplate | ShipFast / TanStarter 验证收入强 | 强竞品多,维护面广 | 不直接做 |
| **SEO 工具站 Starter Kit** | 相邻品类验证收入 + 自有 4 站 bug/流程 | 本细分无直接预售证据 | **进入 48h 验证** |

### 付费与增长证据(2026-08-11 拉取)

- **TrustMRR,API key 验证收入**:ShipFast 累计约 $1.3M / 近 30 天 $3.5K;TanStarter 累计
  $26,178 / 近 30 天 $2,086 / $159 一次性 / X 渠道;Directory Launch 累计 $1,604 /
  近 30 天 $199 / $199 一次性;React Bits Pro 近 30 天约 $32K。
- **哥伦布第三方估算**:AppLaunchFlow 31.7K 月访问、+142%;LaunchShots 18.5K、+79.5%;
  两者 Columbus 均显示自然流量接近 0,说明这类面向 maker 的产品可由品牌 / 社媒 / 社群驱动,
  但访问量不是收入。
- **BIP 边界**:TrustMRR 全站数据中收入与创始人 X 粉丝相关性仅 **r=0.29(n=4,538)**。
  社媒是启动渠道,不是市场本身;因此预售必须收 deposit,不能拿互动数代替付费。

### 两周 MVP 范围(GO 后才做)

1. Astro + Cloudflare Pages 单仓库 starter,含一个纯前端工具示例。
2. canonical / og:url / sitemap / redirect 统一策略;真 404;robots 和结构化数据。
3. 内容集合 + pSEO 页面模板 + 站内互链配置。
4. 发布前测试脚本:扫 trailing slash 循环、canonical 自指、sitemap 状态码、相对链接、soft 404。
5. GSC 接入清单 + Codex / Claude 的项目规则文件;不做后台、不做多框架、不做托管服务。

### 成本账

| 项目 | 预售 | 两周 MVP | 持续/月 |
|---|---:|---:|---:|
| 时间 | 8-12h | 32-40h | 4-6h 更新/支持 |
| 域名 | $0-10 | 已含 | ~$1 摊销 |
| Cloudflare / GitHub | $0 | $0 | $0(早期额度) |
| Waffo | 按成交费率 | 按成交费率 | 按成交费率 |
| 其他工具 / API | $0 | $0-30 | $0-20 |
| **合计现金** | **$0-10** | **$10-40** | **$0-20 + 交易费** |

### 定价假设

- 预售 deposit:$19,GO 后抵扣。
- Launch:个人 $59 一次性(首 20 名),标准价 $99;Agency $199。
- 不承诺永久无限维护;标准价含 12 个月更新,避免一次性收费承担永久客服。

### 结果记录

- 2026-08-11:完成首轮桌面筛选。**结论不是「方向已 GO」,而是「它最值得拿 48 小时验证权」**。
  直接淘汰三个看似匹配但已被占位的方向;顾问建议经公理扫描后仅保留「重复流程产品化」结构。

## 非广告变现 AI 工具站方向筛选(2026-08-11 · 已结束,结论 NO-GO)

- **状态**:done(否定结论,不再重跑同一批候选)
- **关联方向**:英文 SEO 工具站变现路径 — 从"靠流量吃 AdSense"转向"靠付费意愿吃直接收入"
- **待验证假设**:能否从哥伦布 4,630 个 AI 站里筛出一条**非广告变现**、且 18h/周 + 1 万预算可复刻的赛道
- **时间盒**:约 4 小时(实际耗时接近预估)
- **预算上限**:0 元(哥伦布 + Semrush 均为已有订阅)
- **成功标准**:至少 1 个候选通过五重过滤 + 公理扫描,可转成建站实验
- **失败标准**:全部候选在 Semrush 意图/KD 关卡被否
- **结果**:**失败标准命中,0 个候选通过。**

### 执行路径与实际数据

**Step 1 · 哥伦布粗筛**(URL 见 [sources/columbus.md](sources/columbus.md)):
`money=subscription,credits,one_time` + `organic=high` + `visits=lt50k` + `reg=12m` + 按环比增长倒序 → **83 个站**。
砍掉模型名依赖站(nano-banana*/seedream*/gemini*/grok* 约 20 个)、All In One 全家桶、环比下滑的,进详情页拆了 7 个。

**Step 2 · 详情页拆解**,头号候选 `astrocarto.net`(占星地图工具):

| 指标 | 值 |
|---|---|
| 注册 / 月访问 / 环比 | 2026-03-09(4 个月)/ 28.4K / **+883%** |
| 自然搜索 / DR / 美国占比 | 73.1% / 43 / **63.6%** |
| 互动 | 停留 116s · 页均 4.3 · 跳出 31.3%(7 个候选最佳) |
| 变现 | **一次性买断,广告网络字段为空** |

付费探针三条全中:①定价被迭代过(哥伦布 6 月快照 $19.9/$29.9 → 8-11 实开页面 $19.9/**$39.9**,高档涨 34%);
②收款通道真实(页面检出 Creem + Stripe + PayPal);
> ⚠️ **2026-08-11 用户订正:Creem 已不可用,不要再作为收款候选。** 当前待评估通道是 Waffo,见 [profile.md 支付通道约束](profile.md)。
③冷启动外链全来自 AI 导航站提交(theresanaiforthat / toolfame / twelve.tools / fazier / startupfa.me)。

**Step 4 · 交叉验证 —— 结论在这一步被完整推翻**(数据源:Semrush 美区 + Google Trends,2026-08-11 拉取,第三方估算):

| 校验 | 结果 |
|---|---|
| Trends 12 个月 | 前 12 周均值 **51.9** vs 后 12 周均值 **51.9** —— **品类零增长**。astrocarto.net 的 +883% 是抢存量,不是吃增量 |
| Semrush 头部词 | `astrocartography` **49.5K/月 · KD 58(困难,需 36 个引荐域名) · 意图 93% informational** |
| Semrush 词族 | 1,768 词 / 141.1K,但**三层错位**:头部 KD 58-60 打不动 / 中部词里带 `free` / 长尾 KD 19-25 全是 how-to |
| 去掉 visits 上限重搜赛道 | `nextastrology.com` **324.4K**、`hiastro.in` **186.8K**、`astrocarto.org` **72.8K**(与 .net 仅差后缀、早注册 4 个月、流量 2.6 倍)—— **整个头部原本在视野外** |
| Trends Rising | `getlora` / `upastrology` 全部 **Breakout**,哥伦布**两个都未收录** |
| 头部玩家变现 | `astrocarto.org` 72.8K/月、DR41、74% 自然搜索,**仍挂 AdSense** |

**第二候选 `mcskin.app`(Minecraft AI 皮肤)同样否掉**:
`minecraft skin generator` 美区 **880/月 · KD 30(可打)· 但 CPC $0**,词族总量仅 5.5K。
KD 低是真的,CPC 归零也是真的——广告主一分钱不出价,是付费意愿的直接读数。
它 5.1K/月 + 跳出率 17.6% + 页均 4.7 的漂亮数据**验证的是产品好用,不是生意能赚钱**(公理 4)。

### 排除理由(占星方向,按权重排序)

1. **决定性 —— 词族结构是死的**:能变现的词打不动(KD 58-60),能打的词不变现(how-to)。
   把长尾全吃下来只能得到一个内容站靠 AdSense 变现,**正好回到本次要排除的模式**。这是结构性问题,选词技巧绕不过去。
2. **品类零增长**:进去是从 5 个成熟站手里抢存量,而启动资源比它们少。
3. **头部到了规模仍靠广告**:`astrocarto.org` 是该赛道最大的纯 SEO 玩家,7 万月访问依然挂 AdSense
   —— **品类付费意愿不足的最硬读数**,直接对撞"非广告收入"这个原始目标。
4. **对标剥离不掉 boost**:astrocarto.net 4 个月做到 DR43,不是自然长出来的(疑似买链或站群互链——
   它与 `graffitigenerator.io` 出站域名互指,同一操盘手另铺 `destinymatrixai.com` / `saturnreturn.app` / `toon-tone.cc`)。
   [五重过滤](methods/benchmark-five-filters.md)**第 2 层「同阶段」和第 5 层「同验证」双否**。

> **不构成排除理由**:占星在部分收款通道属受限类目。用户 2026-08-11 明确指示"不用管支付工具",
> 故未参与判断;且即便收款无障碍,上述四条依然成立。

### 真正的产出 —— 三个方法论漏洞(比候选值钱)

1. **筛选上限自蔽** → 已沉淀为 [risks.md](risks.md) 独立条目 + [search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) Step 2 操作纪律
2. **informational intent 高量词族伪机会** → 已沉淀为 [risks.md](risks.md) 独立条目 + SOP Step 2 **第三条红线**
3. **哥伦布只能发现候选不能做 GO 决策** → 已沉淀为 [sources/columbus.md](sources/columbus.md) 三条硬边界

### 未做 / 下一步

- **未问哥飞**(`seo-advisor`)。原计划问"KD58 的玄学词还有没有机会",但两条红线已明确,
  不需要第二意见确认一个清楚的否定。**真正值得问的换成**:
  「informational intent 占比 >90% 的高量词族,有没有靠**非广告**方式变现成功的反例?」
  —— 这才是能推翻本结论的问题。若要问,输出按规矩落 `advice/`,先过公理扫描。
- **不重跑同一批候选**。若要继续找非广告方向,换一级分类重跑 Step 1,
  且**必须在 Step 1 之后立刻做去上限的赛道竞争复查**,不要等到 Step 4 才发现头部。

## CSV → QBO 转换器(付费工具站,2026-08-10 跑完 keyword-hunt 第二轮 Step 0-5)

- **状态**:parked(2026-08-11 不作为 Build in Public 主线;Step 1-5 数据保留,2026-08-12 复核)
- **关联方向**:[themes.md 付费工具站 + 自有收款](themes.md#付费工具站--自有收款waffo)
- **前置变更**:2026-08-10 用户确认开通 **Waffo**(MoR,个人无需 LLC,直接打款到银行账户)。
  **「无 Stripe 资质」这个卡了三个多月的硬约束解除**,变现载体从联盟佣金换成自有收款,
  上一条「AI 小说写作联盟词族」实验随之作废(见下方 stopped 记录)。
- **待验证假设**:用户能在一个「输出进入用户工作流」的付费工具词上,拿到第一笔自有收款 ≥ $1。
- **GO 标准**(**2026-08-12 订正**):**Waffo 后台出现一笔非自己产生的 `order.completed`,金额 ≥ $1。**
  - ⚠️ 原文写「可**提现**收入到账 ≥ $1」——查完文档后确认这个措辞**无法按字面兑现**:
    Waffo 成交后有 **~10 个工作日** hold,提现门槛 **$20**,且提现费 **最低 $10/笔**(见 [sources/waffo.md](sources/waffo.md#三费率与资金流别只看-39))。
    按原措辞,验真要等 3 周还得倒贴手续费。**把「验真」与「提现」解耦**:后台确认到账即算 GO,提现是后续运营动作。
- **时间盒**:MVP 1-2 周 + 等 4-8 周
- **预算上限**:域名 $10 + Waffo 按成功交易计费,其余 $0
- ⚠️ **KYB 连带风险(2026-08-12 新增)**:Waffo 上线审核明确查 **"No trademark conflicts"**。
  QBO / QuickBooks 是 Intuit 商标 —— **域名、店铺名、产品名含 QuickBooks 有被拒风险**。
  这与 todos 里「查 Intuit 条款」是同一件事的两面,合并处理:把 QBO 当**文件格式名**描述 + 页面挂
  "not affiliated with Intuit" 免责声明。
- **失败标准**:上线 8 周后自然月 UV > 1000 但 0 付费 → 不是流量问题是产品路径问题(付费墙时机 / 免费额度 / 登录时机),改路径再测一轮;月 UV < 300 → 选词或收录问题

### 为什么是这个词(全流程数据,2026-08-10)

**Step 1 新闸门**(取代上一轮的「找联盟计划」):付费工具四标准 —— ① 输出**进入用户工作流** ② 输出**本身值钱** ③ **持续产出**适合订阅 ④ 帮用户**避免损失/合规**。
来源 [advice 2026-08-10](advice/2026-08-10-paid-tool-category.md),依据是 Stripe 收银台引荐榜实测。

> **关键反直觉判据**:哥飞指出「Stripe 收银台榜上没有一个『输出即终点』的格式转换站」。
> `csv to qbo` **恰恰是格式转换**,但它进的是**会计工作流** —— 簿记员不转就没法把银行流水导进 QuickBooks,
> 而且**每月都要做**。这是标准 ① 的胜利,不是对判据的反驳。**边界在「输出去哪」,不在「是不是转换」。**
> 与 partfit3d 的对照:3MF 拆完就走,hobbyist,无复购,不进任何工作流。

**Step 2-3 词族(Semrush 美区,2026-08-10,第三方估算)**

| 关键词 | 月量 | KD | CPC | Com |
|---|---|---|---|---|
| **`csv to qbo`** | **1,900** | **10** | **$17.63** | 0.11 |
| **`csv to qbo converter`** | **1,300** | **6** | **$17.22** | 0.13 |
| `export qbo to csv` | 1,000 | 10 | — | — |
| `import csv to qbo` | 880 | 31 | — | — |
| `qbo to csv` | 880 | 14 | $6.41 | 0.21 |
| `csv to qbo converter free` | 590 | **3** | $6.65 | 0.48 |
| `qbo to csv converter` | 590 | **3** | $6.79 | 0.05 |
| `upload csv to qbo` | 590 | 34 | — | — |
| `csv to qbo converter free online` | 480 | **1** | — | — |
| `csv to qbo free` | 480 | 6 | — | 0.08 |
| `qbo to csv converter free` | 390 | 6 | $8.47 | 0.52 |
| `qbo to csv converter online` | 390 | **2** | — | — |
| `quickbooks qbo csv to iif converter` | 320 | 10 | — | — |

**词族合计约 10,000/月,主体 KD 1-14,头词 CPC $17.63。**

> ⚠️ **`free` 词占比约 23%**(`...free` 系列合计约 2,300/月)。Step 3 词型硬过滤本来把 `free X` 判 ❌。
> 这里保留,但**定位为引流词不是转化词**:免费额度承接 free 系列,头词 `csv to qbo` / `csv to qbo converter`
> (合计 3,200/月、不带 free、CPC $17)承接付费意图。**免费额度设计是本实验的核心变量,不是附属决定。**

**同批被否掉的候选**:`dst to pes`(Semrush 全「不可用」或 0-20/月,死)、`embroidery converter`(最高 170/月,CPC $1.36-2.77,双低)、
`supplement facts label maker`(880/月 KD 2 很好,但 **CPC 仅 $1.57**、SERP 收费者定价 $160 偏重 B2B → **降为备选**)。

**Step 4 · 变现验证(新形态:扫 Top 10 有没有人直接收费)**

`csv to qbo converter` Top 10 —— **6 个独立工具站明确收费,价格带直接可见**:

| 站 | 收费证据 |
|---|---|
| `accountingconverter.com` | `/pricing` · **$39 / $39·mo / $25·mo / $15·mo** · credits 体系 |
| `docuclipper.com` | `/pricing/` · **$39/mo** · free trial |
| `propersoft.net` | `/purchase/` · free trial |
| `filetailored.com` | `/pricing` · Subscribe |
| `receipt-bot.com` | `/pricing` · Purchase · Credits · Subscribe |
| `toqbo.com` | Free Trial |
| `moneythumb.com` | credits |

其余是 `quickbooks.intuit.com`(平台官方)和 reddit。**没有 G2 / Capterra / 大媒体。**

> 对照组 `supplement facts label maker`:4 个在收费(foodlabelmaker / recipal **$160** / menusano / trustwell 用 FastSpring),
> 但价位高、偏重 B2B。**同样通过 Step 4,但 MVP 成本高于 csv-to-qbo。**

**Step 5 · 可打性(Semrush 实测,不是估算)**

| 站 | Authority Score | **引用域** | 自然流量 | 自然关键词 |
|---|---|---|---|---|
| **`toqbo.com`** | **7** | **24** | 81/月 | 73 |
| **`filetailored.com`** | **13** | **26** | **11.3K/月** | 3.9K |
| `accountingconverter.com` | 22 | 53 | 1.3K/月 | 769 |

**`filetailored.com` 用 26 个引用域跑出 11.3K 月流量;`toqbo.com` AS 7 / 24 引用域,现在就在 Top 10 里。**
**24-26 远低于 Step 5 的 30 硬否决线**,且这次是 Semrush 实测(上一轮联盟方向的 25 是顾问估算,实测最弱站要 135)。

### 期望校准(来自 advice,社群数据非自有实测)

- 注册 → 付费转化率量级 **0.1%~0.5%**
- 第一单出现的流量门槛:**月 UV 1000-3000**
- 定价锚点:竞品实测 **$15 / $25 / $39 月订阅 + credits 包 + 一次性买断**。
  按 [risks.md 独立开发者低价定价陷阱](risks.md#独立开发者低价定价陷阱),取品类中位数中偏上,**不要定 $1-5**

### 执行步骤(Step 6)

1. **先确认 Intuit 条款**(⚠️ 前置风险,30 分钟):QBO = Intuit Web Connect 格式(OFX/SGML 系)。
   ProperSoft / MoneyThumb 已商业化多年说明路通,但上线前查一次 Web Connect 的 FID / 使用条款,避免做完才发现有授权问题
2. 注册域名 + 用现有 Astro/Cloudflare 技术栈做 MVP(CSV → QBO 生成,纯前端可做)
3. 一页一词:`/csv-to-qbo`、`/qbo-to-csv`、`/csv-to-qbo-converter-free`,站内互链
4. **免费额度设计(核心变量)**:免费 N 笔/月,超出走 Waffo 付费。额度校准到「用户每月用完一次」——
   既感受到质量又有升级动力(见 risks.md 低价陷阱条目的同款方法)
5. 接 Waffo Pancake 收款,提交 GSC
6. 等 4-8 周,三层读数:① GSC 曝光 ② 点击 ③ **Waffo 后台首笔到账**

### 结果记录

- 2026-08-10:Step 0-5 完成。**这是 keyword-hunt 跑过的两轮里数据最硬的一次** ——
  第一次出现「KD 6-10 + CPC $17 + 词族 10K/月 + Top 10 有 6 家在收费 + 最弱竞品仅 24 引用域」的组合。
  与第一轮联盟方向的关键差异:**钱直接流向独立工具站,不经过任何中间人**,
  不像联盟方向那样被厂商内容营销拦截(见 [risks.md](risks.md#成熟-saas-品类的-alternatives--vs-词被厂商内容营销占据不是联盟站的地盘))。
- 2026-08-11:用户补充新的**分发约束**:Build in Public 要借助社媒和圈层流量为产品带量,
  会计/簿记用户与当前 X 独立开发圈不重叠,因此即使 `csv to qbo` 搜索与付费数据成立,
  也不作为 BIP 主产品。**本候选 parked,不进入 Step 6**;2026-08-12 仅复核数据并保留为市场基准,
  下一轮改找开发者/站长/创作者/独立创业者使用的「卖铲子」方向。

- **2026-08-12:Step 6 前找了第二意见**(哥飞 agent,[advice 全文](advice/2026-08-12-csv-to-qbo-serp-assessment.md),判定**部分采纳**)。对本实验参数的实际影响:

  | 参数 | 变化 |
  |---|---|
  | **免费额度** | 从「免费 N 笔/月」**定为 MVP 初始值 3 次完整转换/月**(锚点:够簿记员试一次这个月的账) |
  | **收费形态** | **确定订阅,排除一次性买断**(用户每月做账 / 竞品全订阅已训练心智 / 个人开发者撑不起终身更新承诺) |
  | **外链预算** | **上调**:顾问估 5-15 个引用域,按实测 **24-30** 规划。同型低估已第二次,沉淀为 [risks.md 顾问外链门槛估算系统性偏低](risks.md#顾问外链门槛估算系统性偏低把链接预算当可执行数字方法论错误) |
  | **转化率** | **维持 0.1-0.5% 不上调**。顾问本次给 0.5-2%,与它自己两天前的 0.1-0.5% 冲突且无新证据 |
  | **YMYL 风险** | 澄清为**不适用**(工具功能页 ≠ 财务建议页),新增纪律:落地页不写 financial advice 风格 |
  | **产品体验** | 升为一级变量。反面教材 `toqbo.com`:进了 Top 10 但停留 **0 秒**、月流量 **-37%** —— **进 SERP ≠ 站得住** |

  ⛔ **三条明确否掉**:① `INTU.BID=3256`「通用标识符」无依据疑似幻觉,且同段把 OFX **请求**报文
  (`SONRQ` + `USERID`/`USERPASS`)当成导入文件结构贴出来 —— 导入文件是**响应**结构(`SONRS`),该问整体降权;
  ② 「免费版 .qbo 里加 memo 水印」—— 技术上不影响导入,但**会进入簿记员客户的正式账本**,专业场景下是产品事故;
  ③ 三档定价具体数字算反了(年付 $180/年 贵于月付 $144/年),结构可用、数字重设。

  **结论:Intuit 那条前置阻塞不解除。** 顾问在这一问上出现两处技术错误,反而强化了必须自己实测。

- **2026-08-12(同日晚)Ahrefs 终验 —— 实验重新定性,GO 标准与预期全部下调**。
  三条预设否决线技术上全过(CPS 1.36–1.74 远高于 0.4 线;SERP 第 1 名单页 551 UV 险过 500 线;无买链跳升),
  **但查出了否决线没覆盖的四件事**:

  | 项 | 原记录 | **Ahrefs 实测(2026-08-12)** |
  |---|---|---|
  | `csv to qbo` 搜索量 | 1,900(Semrush) | **450**(4.2x 虚高) |
  | `csv to qbo converter` 搜索量 | 1,300 | **600**(2.2x) |
  | `accountingconverter.com` 自然流量 | 1.3K–3,782 | **574/月**(自然关键词仅 21 个) |
  | `filetailored.com` 自然流量 | 11.3K–15.5万 | **2,500/月**(575 个页面,平均 4.3 UV/页) |
  | 竞品引用域 | 24–53 | **410 / 433**(见 [risks.md](risks.md) 16 倍低估条目) |

  **① 词族按裁决规则(取较低值)从 10.7K 降到约 2.5–5K。**
  **② 天花板已被两个样本量死**:排到第 1 = 551 UV/月 → 按 0.1–0.5% 转化 × $25 = **$14–69/月**;
  即使把 iif/qfx/qif 全做完并全排前 3,乐观上限约 1,500–2,000 UV → **$40–250/月**。
  **哥飞算的 $225–750/月基于虚高 2–4 倍的搜索量,不成立。**
  **③ 意图判断此前是错的**:`csv to qbo` 的 Top 10 是 **AI Overview + 3 篇 How-to + 2 个社区帖 + 1 个 YouTube,
  只有 1 个 Tool 页**,Ahrefs 也标 `I`。**但 `csv to qbo converter` 标 `I C T` 且 Tool 页排第一
  → 主攻词必须是 converter 系列,不是头词。**
  ④ 头词趋势预测 **−6%**,converter 词 **+14%**。用户最初「AI 是不是吃掉了这个需求」的疑问,答案是**没被吃掉,也没在长**。

  **✅ 唯一变强的证据**:排第 1 的 `accountingconverter.com/tools/csv-to-qbo` 页面
  **只有 1 个引用域、1 条反向链接、UR 5**,Ahrefs KD = **0**。**页面级进入成本极低。**
  三个竞品注册时间经 whois 全部验证属实。

- **2026-08-12 用户决策:实验保留,但转为零外链预算。**
  定位从「找一个能规模化的方向」改为**「用 $10 验证 Waffo 自有收款闭环」**,只做免费 SEO。
  GO 标准维持「第一笔非自己产生的收入 ≥ $1」——551 UV 够得着。
  **预期正式下调为 $15–70/月,不再引用任何更高的测算。**
  真正的产出是**收款/定价/免费额度设计的实操经验**,复用到新约束框架下的下一个站
  (见 [timeline.md 2026-08-12 约束框架转向](timeline.md#2026-08-12约束框架转向用户决策取代-m1-m4-的零预算新站能打前提))。

## AI 小说写作联盟词族(出单导向选词,2026-08-09 跑完 keyword-hunt Step 0-5)

- **状态**:**stopped(2026-08-10 作废)** —— 用户确认可开通 Waffo 自有收款,
  变现载体从联盟佣金换成自有收款,本实验的前提(无 Stripe → 只能靠联盟)不再成立。
  **数据不删**:Step 4 挖出的「厂商内容营销占据 alternatives 词」是本项目最有价值的结构性发现之一,
  已沉淀为 [risks.md 正式条目](risks.md#成熟-saas-品类的-alternatives--vs-词被厂商内容营销占据不是联盟站的地盘);
  Sudowrite / Kit / Surfer / Jasper 的联盟条款表也保留,**未来做联盟变现时可直接复用**。
- ~~**状态**:planned(Step 1-5 已完成,等 Step 6 实测)~~
- **关联方向**:[themes.md 联盟内容站](themes.md#英文联盟内容站-affiliate-content-site变现导向)
- **待验证假设**:在 AI 小说/虚构写作这个窄场景里,DR 0 新发布者能拿到第一笔联盟佣金 ≥ $1。
- **GO 标准(Step 0 定义,全流程唯一判据)**:**第一笔非自己产生的、可提现的收入到账,金额 ≥ $1。**
  不是曝光、不是点击、不是 AdSense 待付余额。
- **时间盒**:Step 6 建页 1-2 小时 + 等 4-6 周
- **预算上限**:$0(平台发布);若第 3 层出现点击再花 $10 注册 EMD 域名
- **失败标准**:第 3 层(联盟后台点击)= 0 且前两层正常 → 选的是流量词不是决策词,回 Step 4 重挑

### 全流程数据(2026-08-09)

**Step 1 · 联盟计划(本项目自行核实,哥飞未提供)**

| 产品 | 佣金 | Recurring | Cookie | 允许 SEO 引流 | 打款/起付 |
|---|---|---|---|---|---|
| Kit(原 ConvertKit) | 50% 前 12 个月,之后 10/15/20% 永久 | ✅ | 未公开 | ✅ | 未公开 |
| Surfer SEO | 月付首笔 75%(可到 125%);年付 15-25% | ❌ | 90 天 | ✅ | PartnerStack,**$5** |
| Jasper | 25% recurring 12 个月 | ✅ | 45 天 | ✅ | PayPal,$25 |
| Hostinger | 40% 起 | ❌ | 30 天 | ⚠️ 申请需 1000 流量,**当前过不了审** | PayPal $100 |
| **Sudowrite** ← 入选载体 | **25% recurring 12 个月** | ✅ | 30 天(Rewardful) | ✅ | PayPal 月结,**60 天持有期** |
| **Squibler** ← 备选 | 20% | 部分 | 未公开 | ✅ | Wise,**起付 $100** |

**Step 3 · 候选池(Semrush 美区,2026-08-09,第三方估算)** — 12 词全部通过 CPC/KD/意图/量四维筛

| 关键词 | 月量 | KD | CPC | Com | Step 4 判定 |
|---|---|---|---|---|---|
| `surfer seo alternatives` | 880 | 21 | $10.72 | 0.13 | ❌ 0 联盟链接 |
| `convertkit vs mailchimp` | 720 | 22 | $7.85 | 0.29 | ❌ 0 |
| `surfer seo alternative` | 590 | 23 | $7.40 | 0.11 | — |
| `surfer seo reviews` | 590 | 22 | $8.02 | 0.19 | — |
| `convertkit review` | 480 | 25 | $9.78 | 0.18 | — |
| `convertkit alternatives` | 320 | 17 | $13.13 | 0.30 | ⚠️ 仅 1 条 |
| `mailerlite vs convertkit` | 320 | 21 | $7.30 | 0.43 | — |
| `surfer seo vs semrush` | 320 | 14 | $6.26 | 0.12 | — |
| `jasper ai alternatives` | 260 | 17 | $4.89 | 0.14 | ❌(全是竞品站) |
| `convertkit alternative` | 140 | 24 | **$14.50** | 0.06 | — |
| `surfer seo free trial` | 140 | 26 | **$24.65** | 0.42 | — |
| `best ai tool for proposal writing` | 110 | 23 | **$16.59** | 0.39 | ❌ 0,全是厂商官网 |

**⚠️ 一处阈值校准(偏离 SOP 原文,已记录)**:SOP 的 `Com. > 0.5` 会误杀整个池子。
`Com.` 量的是广告主竞价密度,品牌词天然只有少数几家竞品在投。改为 **CPC 单独作一号筛,Com. 降为参考**。

**Step 4 · 变现验证(核心步,砍掉 10/12)** — 逐词开 Top 10 扫全部出站链接找联盟链接特征

| 词 | Top 10 联盟链接 | 判定 |
|---|---|---|
| `best ai writing tools`(1.3K / KD **45** / $3.63) | **2** ✅ | KD 超 Step 3 门槛 |
| **`best ai for novel writing`**(110 / KD **22** / $2.77 / Com 0.62) | **2** ✅ | ✅ **强信号,入选** |
| 其余 5 词 | 0-1 | ❌ pass |

赚钱的两个独立发布者:`aimadesimple0.substack.com` → `sudowrite.com/?via=nitin`、`rytr.me/?via=nitin-sharma`;
`medium.com/@anangsha` → `sudowrite/?via=anangsha`、`squibler.io/?via=anangsha`、`simplified.com/?fpr=anangsha43`、`originality.ai/?via=anangsha`。
**两人都在平台上,不在自有域名上。**

**Step 5 · 可打性**

| 来源 | 数字 |
|---|---|
| Semrush | 最弱独立站 `thewritingasylum.com`:**AS 8** / 引用域 135 / 流量 331 月(**+119%**) |
| Semrush | 天花板站 `inkfluenceai.com`:AS 27 / 引用域 **334** / 流量 7.6K 月 |
| 哥飞 | `sudowrite alternatives` **链接预算中值 25 个引用域** ← 唯一通过 Step 5「>30 即 pass」硬否决的方向 |
| 哥飞 | novel 词族 Top 10 有 **DR 2~6** 的站;10 个候选 EMD 域名全部可注册 |

### 定标词族(合计约 1.3K-1.5K/月)

| 关键词 | 月量 | KD | CPC | Com |
|---|---|---|---|---|
| `sudowrite vs novelcrafter` | 260 | 24 | — | — |
| `novelcrafter vs sudowrite` | 260 | 27 | — | — |
| `novel writing ai` | 170 | 51 | $2.42 | 0.61 |
| **`best ai for novel writing`** ← 主攻 | 110 | **22** | $2.77 | **0.62** |
| `best novel writing ai` | 110 | 29 | $2.79 | 0.65 |
| `sudowrite alternatives` | 110 | **22** | $2.51 | 0.48 |
| `sudowrite review` | 110 | 24 | $3.15 | 0.19 |
| `sudowrite promo code` | 90 | **8** | $5.79 | 0.30 |
| `squibler vs sudowrite` | 70 | **16** | $2.02 | 0.15 |
| `best ai novel writing software` | 50 | 34 | $3.57 | 0.70 |

> 量级参照:partfit3d 整站 3 个月 833 曝光;3MF 转换词族 Semrush 口径 ~10K/月。
> 本词族介于两者之间,**比现有主攻词大一个数量级,比 3MF 词族小一个数量级**。

### 执行步骤(Step 6,唯一产生真值的一步)

1. 发一篇 Medium 或 Substack 长文,主攻 `best ai for novel writing`,覆盖 `sudowrite vs novelcrafter` / `sudowrite alternatives` 两个次词
2. 挂 Sudowrite 的 Rewardful 联盟链接,**加 `rel="sponsored"`**
3. 等 4-6 周,三层读数:①平台/GSC 曝光 ②点击 ③**Rewardful 后台点击数**
4. 第 3 层出现任何点击 → 注册 EMD 域名升级独立站;第 3 层 0 而前两层正常 → 回 Step 4 重挑

**⚠️ 为什么不按 SOP 原文在 partfit3d / baxianfans 上开页**:partfit3d 是 3D 打印、baxianfans 是华语动画,
挂 AI 小说写作页面主题严重不相关,大概率不收录不排名,拿不到干净读数。
改用平台发布的依据是 **Step 4 实扫结果本身** —— 这个 SERP 里两个真正在赚联盟佣金的人用的就是 Substack 和 Medium。
成本 $0、收录以天计(对照 partfit3d 等了 2 个月),且**直接测第 3 层**,那才是当前的真瓶颈。
自有域名等第 3 层有点击再注册 —— **顺序不能反,这正是 partfit3d「先建站再定词」踩过的坑**。

### 结果记录

- 2026-08-09:Step 0-5 完成。**最大产出不是选到的词,是 Step 4 挖出的结构性发现** ——
  成熟 SaaS 品类的 alternatives / vs 词被厂商内容营销占据,CPC 最高的那几个词联盟链接一条都没有。
  已沉淀为 [risks.md 正式条目](risks.md#成熟-saas-品类的-alternatives--vs-词被厂商内容营销占据不是联盟站的地盘)。
  这条直接修正了 `keyword-hunt` Step 3 的一号筛:**CPC > $1 之后必须再问一句「是谁在买这个点击」**。

## 哥伦布对标站粗筛第二轮(2026-08-13 · 已结束,结论 NO-GO,但产出两条可复用的东西)

- **状态**:done(否定结论)
- **关联方向**:[timeline.md 2026-08-12 新约束](timeline.md#2026-08-12约束框架转向用户决策取代-m1-m4-的零预算新站能打前提)——
  $2–5K 外链预算 / KD 45–55 / 自有收款 / 大搜索量 + 付费收入
- **待验证假设**:在**新约束**下,能否从哥伦布筛出一个可对标的付费 SaaS AI 工具站
- **与上一轮(2026-08-11)的区别**:刻意错开两个参数——`visits` 从 `lt50k` 抬到 **`50k-200k`**
  (修正[筛选上限自蔽](risks.md#筛选上限自蔽用带上限的结果判断赛道竞争方法论错误));不锁一级分类,全量横扫
- **时间盒**:约 1.5 小时(实际)
- **结果**:**0 个候选够格当新约束下的对标站。**

### Step 1 · 粗筛漏斗(哥伦布快照 2026年7月,拉取 2026-08-13,第三方估算)

筛选串:`money=subscription,credits,one_time` + `organic=high` + `visits=50k-200k` + `reg=12m` + `sort=visits_mom&order=desc` → **125 站 / 3 页**

| 层 | 剩余 | 淘汰依据 |
|---|---|---|
| 初始 | 125 | — |
| 砍品牌驱动 / 目录站 / 其他 | ~46 | 起量不在 SEO,五重过滤第 1 层 |
| 砍 All In One | ~30 | 18h/周不可复刻 + 流量无法归因到单一功能 |
| 砍模型版本号抢注域名 | ~17 | [risks.md 已立条目](risks.md#模型版本号抢注域名窗口期--一个模型版本周期违反准公理-b) |
| 砍负增长 + NSFW | **11** | — |

**通过率 8.8%。** 一个额外的分布观察:11 个主候选里 **6 个是音频**(占 55%),
而音频在哥伦布全库只占 16%(749/4630)——富集度 3.4 倍。但拆完发现这不是机会信号,原因见下。

### Step 2 · 5 个详情页实拆

| | cleanaudio.io | spritesheets.ai | ai-manga-translator | describemusic.net | detectvideo.ai |
|---|---|---|---|---|---|
| 广告网络 | 空 | 空 | 空 | **AdSense** | **AdSense** |
| 定价 | Free / **$16.99/mo** + 积分包 | Free / $3.50/mo | 积分 $0.01–0.02/次 | 仅 Free | 仅 Free |
| 美国占比 | 28.8%(India **35.9%** 居首) | 17.9% | 21.0%(Korea 20.4%) | 17.2% | **51.9%** |
| 头部词 / 量 / CPC | audio cleaner 5.5K / **$0.45** | sprite sheet 18.7K / $1.23 | manga translator 16.4K / $0.48 | **song finder 102.5K** / $0.64 | ai video detector 6.0K / $1.95 |
| 互动 | 50s / 4.2 / 32.3% | 58s / 3.5 / 37.0% | 46s / 3.1 / 39.0% | **31s** / 3.4 / 43.3% | 53s / **2.5** / 31.3% |
| DR / 外链动作 | 28 / PH + theresanaiforthat | **0.2** / 只有 discord | 8 / discord+x+reddit | 21 / **28 个目录站** | 20 / 出站仅 1 |
| 月访问 / 站龄 | 76.5K / 5 个月 | 56.1K / 8 个月 | 100.7K / 5 个月 | 147.2K / 12 个月 | 99.3K / 10 个月 |

### 三条结论

1. **哥伦布「非广告变现」筛选的误报率约 40%**(5 抽 2)。`describemusic` / `detectvideo` 变现标签带积分制、API 收费,
   实际广告网络字段明写 AdSense、定价线索只有 `Free` —— **根本没有付费产品**。
   [columbus.md 硬边界 3](sources/columbus.md) 写过这条规则,这轮给出了误报率量级:**不进详情页看「广告网络」字段,四成粗筛结果是假的。**

2. **CPC 是结构性硬伤,不是选词失误** → 已沉淀为 [risks.md 独立条目](risks.md#ai-工具站品类的-cpc-系统性低-1-2-个数量级用它找付费生意是池子选错违反公理-4)。
   5 个站分属 5 个不相干品类,CPC 全落在 $0.18–3.56,而 `csv to qbo` 是 $17.63。
   最硬的读数是 `describemusic.net`:头部词月搜 **102.5K**、做到 147.2K 月访问、13 个月站龄,**仍然只能挂 AdSense**。

3. **「DR 0 也能起量」不构成新发现 —— 这是本轮我自己推错又收回的一条。**
   `spritesheets` DR 0.2 零外链做 32K 自然搜索、`detectvideo` 出站仅 1 个做 82.1K,数据都对,
   但它们打的是 `audio cleaner` / `sprite sheet generator` 这类低 KD 词。
   **「没外链也能起量」和「词好打」是同一件事的两面**,不是独立发现。
   $2–5K 外链预算买的是「打 KD 45–55 的能力」,而这批站压根不在那个战场上 ——
   所以它们**既不能证明也不能证伪外链预算的必要性**,只能说明这批站不是新约束下的对标对象。

### 真正的产出:一份可直接抄的冷启动外链清单

`describemusic.net`(5 个月 → 147.2K)出站 28 个目录站,明牌可抄:
`startupfa.me` / `dang.ai` / `tinylaunch.com` / `toolpilot.ai` / `turbo0.com` / `neeed.directory` /
`goodfirms.co` / `indie.deals` / `launchigniter.com`;`cleanaudio.io` 走 `producthunt` + `theresanaiforthat`。
→ 补进 [外链台账](sources/backlink-ledger.md)渠道池,给 partfit3d / aidepixelate 用。

### 方法论沉淀

- **CPC 应当前置到 KD 和搜索量之前**,作为品类付费意愿的第一道闸门。
  这与 2026-08-09 那条「CPC > $1 之后必须再问一句『是谁在买这个点击』」互补:
  先看**有没有人出价**,再看**出价的是谁**。
- **换参数不等于换池子。** 08-11 和 08-13 两轮把 `visits` 上限、分类锁定都换过了,撞的是同一堵墙。
  下一轮若还要找付费方向,该换的是**样本库本身**,不是筛选串。
