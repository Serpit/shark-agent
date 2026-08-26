# memory/INDEX.md

> **本仓库的项目记忆入口。** Claude 会话开始时,先读这份索引,再按需打开具体文件。
> 所有记忆都以 markdown 存放在项目目录内,不依赖任何 agent 的本地缓存。

## 长期不变(画像与节奏)

- [profile.md](profile.md) — 用户画像、出海主线、试错容忍度、人脉关注点、公理锚点
- [axioms.md](axioms.md) — 公理底座（dbs 6 公理 + shark 3 准公理，两级分层）
- [timeline.md](timeline.md) — 季度计划、当前阶段、节奏提醒触发条件

## 摄入产物(随文章增长)

- [findings/_processed.md](findings/_processed.md) — 已摄入文章的清单(文件名 + 内容哈希 + 摄入时间)
- [findings/](findings/) — 每篇被保留文章的三段式提炼(一篇一个 md)

## 信号摄入(随风向标增长,由 `/signals` 触发)

- [signals/_processed.md](signals/_processed.md) — 已评估风向标清单(防重 + 判定一览)
- [signals/](signals/) — 每条值得记录的风向标的三段式评估:适配度 / 市场逻辑 / 真伪与风险

## 聚合视图(随认知演进)

- [principles.md](principles.md) — 跨方向通用的理念与方法论,为方向选择与动作决策提供准则
- [themes.md](themes.md) — 出海方向候选与对应证据线索
- [experiments.md](experiments.md) — 从候选方向拆出的最小验证实验队列
- [todos.md](todos.md) — 跨实验/跨方向的具体待办与进度跟踪(颗粒度 = 单次能干完的动作)
- [connections.md](connections.md) — 值得连接的人 / 社群 / 关键节点
- [risks.md](risks.md) — 过时/诈骗/夸大模式库,新文章对照排雷

## 咨询记录

- [talks/](talks/) — 教练咨询记录（/talk 命令产物，6 段式：问题/分类/公理扫描/追问/消解/行动）

## 外部顾问建议(随咨询增长,由 `seo-advisor` skill 触发)

> 与 `findings/`(他人经验)、`signals/`(机会情报)平行的第三条管道:**他人观点**。
> **观点不是数据**——必须过公理扫描 + 与 GSC 实测对质才能落盘,且**不可回流 principles.md**。

- [advice/_processed.md](advice/_processed.md) — 已评估建议清单(问题 / 来源 / 采纳判定)
- [advice/](advice/) — 每条建议的三段式:原始建议 / 公理扫描与辩证 / 采纳判定

## 数据源接入手册(怎么拿到数据)

> 与 `methods/`(怎么判断)分层:这里只讲**取数路径、字段含义、已知陷阱**。
> 每个源都带一条硬约束:**拉数前先说清结果会落到哪个动作,答不上来就不查**(公理 6)。

- [sources/gsc.md](sources/gsc.md) — Google Search Console(**自有真值**,与第三方估算冲突时以它为准),工具 [`scripts/gsc.py`](../scripts/gsc.py)
- [sources/ga4.md](sources/ga4.md) — Google Analytics 4(**自有真值**,管"点进来之后发生了什么",与 GSC 互补),工具 [`scripts/ga4.py`](../scripts/ga4.py)
- [sources/columbus.md](sources/columbus.md) — 哥伦布 columbus.tools(**第三方估算**,4630 个 AI 工具站的增长样本库),独有能力:按词看"谁在打这个词、谁在涨谁在死";走 MCP 工具直连,免浏览器
- [sources/gefei-kd.md](sources/gefei-kd.md) — 哥飞版关键词难度 **MCP**(**第三方估算**),给英文词的难度分 + 进入前十的链接预算 + 前十竞争盘面表;**不给搜索量和 CPC**,链接预算是曲线插值不是实测
- [sources/payment-growth.md](sources/payment-growth.md) — 支付平台引荐表(**第三方估算**,SimilarWeb API 直连),**唯一「从钱倒推」的源**:看谁的钱已经在流过 Stripe/PayPal/Paddle/Lemon Squeezy 结账页;工具 [`scripts/payment-growth/`](../scripts/payment-growth/),skill `payment-growth`
- [sources/daily-report.md](sources/daily-report.md) — 每日飞书日报(GSC + GA4,每天 10:00 推送),工具 [`scripts/report_daily.py`](../scripts/report_daily.py)
- [sources/waffo.md](sources/waffo.md) — **收款通道**(不是数据源)Waffo Pancake MoR 接入手册:注册三关(开户/KYB/KYC)、全成本费率、
  资金流时间线、四条集成路径、12 条已知陷阱。**大陆个人身份证 + 国内银行卡即可收全球款**,解除「无 Stripe 资质」硬约束。
  当前为**官方文档口径,非自有实测**,开通后回填「实测校准」段
- [sources/backlink-ledger.md](sources/backlink-ledger.md) — **外链台账**(不是数据源)飞书 Base:partfit3d + aidepixelate
  两站的提交流水与渠道池,工具 [`scripts/backlink_ledger.py`](../scripts/backlink_ledger.py)。
  核心纪律:**提交数 ≠ 外链数** —— 129 次提交里 `published` 只有 5 条,真正传权重的仅 1 条

**取数入口已封装成 skill**(会话中按话题自动触发,不用手动记路径):

| skill | 管什么 | 信任等级 |
|---|---|---|
| `seo-data` | GSC 自有站数据 | **真值** |
| `seo-competitor` | Ahrefs / Semrush / SimilarWeb(3ue 面板) | 第三方估算 |
| `seo-advisor` | 哥飞 SEO Agent 问答 | **他人观点,需辩证** |

**编排层 skill**(调用上面三个,不自己取数):

| skill | 管什么 |
|---|---|
| `keyword-hunt` | 新站**出单导向**选词流水线,6 步。是 [methods/search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) 的变体——一号筛从月搜索量换成 CPC + 竞争密度,验证终点从看排名换成看联盟后台点击。**2026-08-09 首次跑通 Step 0-5**,产出见 [experiments.md](experiments.md#ai-小说写作联盟词族出单导向选词2026-08-09-跑完-keyword-hunt-step-0-5);实测修正见 [risks.md](risks.md#成熟-saas-品类的-alternatives--vs-词被厂商内容营销占据不是联盟站的地盘) |

## 方法论库(可执行 SOP)

- [methods/axiom-scan.md](methods/axiom-scan.md) — 公理扫描 SOP（摄入文章/signals/教练对话三场景,9 条逐项问句）
- [methods/community-demand-discovery.md](methods/community-demand-discovery.md) — 社群平台需求挖掘 SOP(小红书 / Reddit / X 通用,6 步)
- [methods/search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) — 搜索引擎需求发现 SOP(Web/SaaS 出海,6 步,与社群版对位)
- [methods/benchmark-five-filters.md](methods/benchmark-five-filters.md) — themes 候选五重过滤（骨架版，同模式/同阶段/同合规/同需求层/同验证）
- [methods/x-tweet-writing-templates.md](methods/x-tweet-writing-templates.md) — X 推文起草 SOP(4 开头 + 10 模板 + 3 Thread + 发布前三问)
- [methods/x-cold-start-and-amplification.md](methods/x-cold-start-and-amplification.md) — X 冷启动与放大 SOP(Premium/置顶推文/大 V 互动/信息监控/变现优先级)

## 维护规则

- 每条新增/更新都要顺手把这份 INDEX 同步上,避免出现孤立文件。
- 一篇文章只在 `findings/` 写一次,聚合视图(themes/connections/risks)以**引用链接**指回 finding,不要复制内容。
- 文件名用稳定的英文 slug(必要时加日期前缀),不要用会变的标题文本,避免历史断裂。
