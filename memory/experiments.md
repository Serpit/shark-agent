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
    - **选词方法实际已换轨**:原 SOP 是"用户报候选词 → Ahrefs 验证",连续两次全池 NO-GO(GPT Image 2 / 羽毛球)后停摆;实际跑通的 4 个站选的是**极长尾工具型词**(`split 3mf` / `depixelate` / `all wishes come true`),这类词 Ahrefs Free 大概率也显示 <100/月却真实有量。**原 SOP 的"月搜索量 >500"红线对工具站不适用**,需要修订。

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

    1. **CTR 修复有硬天花板**:把所有漏损点修到位,3 个月也只多约 **10 次点击(≈3 次/月)**。
       原 todo 说它是"全盘最大漏损点"——**相对成立,绝对量微不足道**。仍值得修(1-2 小时,一次性),
       但**不要期待它改变任何事**,更不能拿它当 M4 的主线动作。
    2. **真问题是量级,不是转化**:整站 3 个月 833 曝光。41 个 query 里
       `split3mf` / `split3dmf` / `spli3mf` / `slit3mf` / `slipt3mf` / `splt3mf` / `spilt3mf` /
       `3mfsplit` / `split.3mf` / `split 3 mf` / `3mf split` **全是同一个词的拼写变体**——
       整站实际建立在**一个**月曝光约 84 次的词上。这与 [risks.md](risks.md) 里羽毛球那条是同一个模式的复发:
       **排名好 ≠ 有量**,只不过这次是"选词选对了但池子太小",上次是"整个赛道没量"。
    3. **品牌词 `partfit` 只排 4.4 位、15 曝光 0 点击** —— 自己的品牌名没排到第 1,
       说明站点权重/实体识别不足。这条是独立问题,和 title 无关。

    **对 M4 的含义**:`partfit3d` 这个站的天花板已经可测——即使 `split 3mf` 打到第 1 位
    (CTR ~27%),3 个月也就 ~70 次点击。**扩量必须靠加词族或加站,不可能靠修这一个站的转化。**
    变现路径决策应基于这个量级来定,不要按"再优化优化就起来了"的假设推进。

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
    对照 `split 3mf` 实测约 84 曝光/月,**相邻词族大一个数量级**。

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

## CSV → QBO 转换器(付费工具站,2026-08-10 跑完 keyword-hunt 第二轮 Step 0-5)

- **状态**:planned(Step 1-5 完成,等 Step 6)
- **关联方向**:[themes.md 付费工具站 + 自有收款](themes.md#付费工具站--自有收款waffo)
- **前置变更**:2026-08-10 用户确认开通 **Waffo**(MoR,个人无需 LLC,直接打款到银行账户)。
  **「无 Stripe 资质」这个卡了三个多月的硬约束解除**,变现载体从联盟佣金换成自有收款,
  上一条「AI 小说写作联盟词族」实验随之作废(见下方 stopped 记录)。
- **待验证假设**:用户能在一个「输出进入用户工作流」的付费工具词上,拿到第一笔自有收款 ≥ $1。
- **GO 标准**:**第一笔非自己产生的、可提现收入到账 ≥ $1**(经 Waffo)。
- **时间盒**:MVP 1-2 周 + 等 4-8 周
- **预算上限**:域名 $10 + Waffo 按成功交易计费,其余 $0
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
