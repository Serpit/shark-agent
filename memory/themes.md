# 出海方向候选

聚合视图。每条候选方向用一个二级标题,内容只放结论与证据**链接**,不要复制 finding 原文。

## 模板

```
## <方向名,例如:东南亚 TikTok 选品代运营>
- **状态**:explore / validating / parked
- **核心需求假设**:一句话写清楚要满足谁的什么需求
- **画像匹配**:高 / 中 / 低,说明与 profile.md 的时间、预算、能力、资源约束是否匹配
- **验证成本**:低 / 中 / 高,说明 1-2 周 MVP、3 个月回报周期、1 万预算内是否可验证
- **可行性证据**:[finding-链接](findings/xxx.md), [finding-链接](findings/yyy.md)
- **风险/未知**:列出还需验证的关键变量
- **下一步动作**:具体到"读什么、问谁、试什么"
```

## 当前候选

## 技术型出海小工具 / B2B 微 SaaS

- **状态**:explore(2026-04-29 调整:**降为并行 BRD**,不再要求 M1-M3 必出 GO 候选;主线让位给 SEO 内容站矩阵。降级原因见下方"决策依据"段)
- **核心需求假设**:海外开发者、企业内部团队、小团队或个体商家存在足够具体的效率/自动化/开发流程痛点,可以用 1-2 周 MVP 小工具解决,并通过订阅、按量计费、一次性付费或 App 内购变现。
- **画像匹配**:高。用户核心能力是技术开发,在海外创业公司做 App 开发,懂海外产品上线与基础盈利模式;时间约 18 小时/周、预算 1 万、目标 3 个月内找到真实付费用户,与小工具/Micro SaaS 验证节奏匹配。
- **验证成本**:低-中。可先用 3 小时 BRD 法验证需求,再做 1-2 周 MVP;冷启动可走 Reddit/社区、Product Hunt、App Store、Chrome Store、SEO、冷邮件等免费或低成本渠道。
- **可行性证据**:[2026-04-indie-saas-3h-brd-validation.md](findings/2026-04-indie-saas-3h-brd-validation.md)(给出写代码前的 6 步 BRD 调研 SOP、GO/NO-GO 框架、定价和痛点验证方法);[2026-04-do-it-yourself-mindset.md](findings/2026-04-do-it-yourself-mindset.md)(强调方向要靠最小验证打出来,不是长期空想);[youtube-ai-faceless-channel-sop.md](findings/youtube-ai-faceless-channel-sop.md)(可借用"抄 MVP、具象化需求、自动化前算时间成本"等通用方法);[2026-04-wechat-miniprogram-ai-matrix.md](findings/2026-04-wechat-miniprogram-ai-matrix.md)(国内小程序矩阵实战印证"AI 让单产品试错成本降到几天 + 几十元,可跑矩阵";选需求三标准/AI 三句话开发可直接平移到 Chrome Extension / 轻 SaaS / 小工具 App);[2026-04-claude-code-sideline-100k.md](findings/2026-04-claude-code-sideline-100k.md)(作者把外链自动化方法论 + Skill 包 + 平台流程库打包卖了几千块,印证"经验产品化"路径——不必非做 SaaS,把高频痛苦可复用流程整理出来就是小产品;eat your own dog food 是最好的 idea 来源)
- **风险/未知**:
  - 目前还没有具体子赛道,不能停留在"做一个小工具"这种空泛层面
  - 用户缺少互联网以外的垂直行业知识,进入强行业垂直前必须先补 domain insight
  - 最大风险不是技术实现,而是找不到真实痛点、付费用户和稳定获客渠道
  - 需要避免独立开发者低价陷阱,不要靠免费/极低价吸引无付费意愿用户
- **决策依据(2026-04-29 降级)**:
  - **支付通道现实约束**:用户当前无 Stripe 资质,SaaS 直接收款链路不通(详见 [profile.md 支付通道约束](profile.md#能力与资源))。在解决 Lemon Squeezy / Paddle 等 Merchant of Record 主体之前,SaaS 月订阅模式无法闭环。
  - **建站能力前置缺失**:用户尚未走过完整建站流程(选词 / Astro / Cloudflare / 外链 / SEO),这是出海主线的基础能力,需要先在低风险载体(SEO 内容站)上跑通,再迁移到 SaaS。
  - **SEO 内容站的双重价值**:既能积累建站能力,又能在收款受限期通过 AdSense 拿到第一笔小额自然收入,且与 Web SaaS 共享技术栈(Astro + Cloudflare + 关键词分析)。
- **下一步动作**:
  - **产品形态优先级:Web-first**(Web SaaS / Chrome Extension / 开发者工具站点)。App 形态降权,只保留 `mobile subscription app` 作为订阅商业化研究素材,不作为自建 MVP 候选。
  - **当前阶段不强求出 GO 候选**——SEO 内容站矩阵跑通后,根据流量观察 + 支付通道进展,再决定是否启动 SaaS BRD。
  - **并行允许的轻量动作**:在跑 SEO 站时若发现某个关键词背后是 SaaS 需求(transactional intent + 现有付费产品),记录到候选池,等支付通道解决后再启动 BRD。
  - 长期保留的 BRD 方法论:[search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) + [2026-04-indie-saas-3h-brd-validation.md](findings/2026-04-indie-saas-3h-brd-validation.md) 钦哥 6 步法。

## 外贸 B2B 小语种深度本地化(中东 + 西语美洲)

- **状态**:parked(单点证据,且与当前 profile 的资源约束不匹配;除非找到小语种/供应链合伙人,否则不作为近期主线)
- **核心需求假设**:阿拉伯语区(沙特/阿联酋/埃及)和西语区(墨西哥/哥伦比亚/智利)当地不擅英语的中小 B 商家,需要懂母语 + 懂本地认证 + 懂本地宗教文化的「中国供应链顾问」,不只是报价发货。这群客户长期被只讲英语的主流外贸服务商忽视。
- **画像匹配**:低。用户暂无小语种、海外本地、供应链、外贸资源;当前只能兼职,且希望 3 个月内通过 MVP 找到付费用户,与该方向的商务沟通、供应链绑定和交付周期不匹配。
- **验证成本**:高。需要小语种商务能力、柔性工厂、样品/认证/打样预算和长周期 BD,不适合作为 1 万预算内的近期主线。
- **可行性证据**:[2026-04-foreign-trade-b2b-newbie-sop.md](findings/2026-04-foreign-trade-b2b-newbie-sop.md)(作者给出三个机会窗口判断 + 七步开单 SOP + 启动案例「中东高端酒店定制灯具,2-3 万启动」)
- **风险/未知**:
  - 「小语种深度商务沟通能力」是硬门槛,SOHO 一人作战不可行,需要先解决合伙人/团队问题
  - 启动案例(中东酒店灯具)是作者推演而非已验证案例,真实可行性待打样
  - 作者本人 SOHO 2.0 (25-09 起)仅 2 个客户、利润 3 万多,SOP 框架未在小语种方向被自验证
  - 需要验证:GCC/NOM 认证的实际周期和成本是多少?柔性工厂愿意接 5000 元打样单的占比有多大?
- **下一步动作**:
  - 找 1-2 篇专门讲中东市场 / 西语美洲市场实战的 finding 做交叉印证
  - 调研生财社群里有没有阿拉伯语/西语背景的圈友可以合作
  - 核算「单人 SOHO 起步是否真的需要小语种合伙人」——如果是,这条方向需要降权或改为「先搭班子再启动」

## 制造业转移配套(东南亚)

- **状态**:parked(同一篇 finding 的次要证据,信心更弱;与当前资源/预算/周期不匹配)
- **核心需求假设**:印尼/越南/泰国新迁入工厂需要生产工具/耗材/零配件(B 端「弹药供应商」);制造业带动消费阶层升级,催生设计感家居/小家电/个护需求(C 端「新市民供应商」)。
- **画像匹配**:低。用户没有供应链、当地市场和外贸资源,且方向更依赖线下供应链、资金周转和 B 端交付。
- **验证成本**:高。订单特征是小单、多样、要货急,验证需要供应链协同、样品和客户开发,难以在 1-2 周 MVP 或 3 个月兼职周期内低成本验证。
- **可行性证据**:[2026-04-foreign-trade-b2b-newbie-sop.md](findings/2026-04-foreign-trade-b2b-newbie-sop.md)
- **风险/未知**:
  - 订单特征是「小单、多样、要货急」,对资金周转和柔性供应链要求高,纯个人 SOHO 难以支撑
  - 缺乏具体子赛道判断(具体哪类工具/哪类家居)
- **下一步动作**:暂时 parking,优先做小语种方向

## 英文 SEO 内容站矩阵 + AdSense 变现

- **状态**:**partially validated(2026-08-09 更新)**——**建站与排名链路已用自有数据验证通过**,变现链路未验证。2026-08-09 从 Search Console 实拉:4 站上线、近 90 天合计 31 点击 / 1338 曝光 / 十几个关键词进 Google Top 10。**但实际做出来的 3/4 是工具站而非内容站,AdSense 变现假设需重新对齐**。实测数据见 [experiments.md 4 站实测数据](experiments.md#4-站实测数据2026-08-09-从-search-console-拉取)
  - **自有证据推翻的一条原假设**:原 SOP 红线"月搜索量 <200 即使 KD=0 也撑不起流量"对**工具型极长尾词不成立**——`split 3mf`、`depixelate` 这类词 Ahrefs Free 大概率显示 <100/月,实际单站已跑出 833 次曝光。工具站选词应看**意图明确度**而非绝对搜索量
  - *(历史)* 2026-04-29 升级为 M1-M3 主线候选——支付通道约束 + 建站能力前置 两重原因,从原本"M3 之后并行练手"提前为"现在就启动"
- **核心需求假设**:针对**最近才出现搜索量、竞争度低**的英文长尾关键词需求(工具型/查询型/换算型/小众场景)做内容站矩阵,通过 AI 批量生成内容 + 人工校验 + 外链打权重,排名起来后通过 Google AdSense 持续变现。**核心假设**:在英文搜索生态里仍存在足量"大厂没做或做得烂、有真实搜索量、低权重新站可短期内打到首页"的细分长尾。
- **画像匹配**:中-高。**优点**:技术开发能力可直接套 Astro + Tailwind + Cloudflare Pages 模板批量化;Claude Code Skill / Agent / Hook 工作流让单站从选词到上线压缩到一个下午;符合 profile "免费/低成本冷启动渠道"和"长期复利型资产";不消耗用户当前 IP 实验时间盒(完全可后台跑)。**缺点**:与"找到真实付费用户"目标不直接对齐(广告分成≠用户付费),不能验证 profile 最优先的"找需求"能力;且短期 ROI 远低于工具型 SaaS,M1-M3 阶段不应作为主线。
- **验证成本**:中。建站成本几乎为 0(Cloudflare Pages 免费额度足够),但**外链建设是真金白银的时间成本**——作者半自动化外链系统跑下来 6 站 2 周 300+ 外链,需要 Ahrefs 订阅($99-249/月)和持续投入;**资产成型周期 9-18 个月**,与 profile "3 个月内看到反馈"硬约束冲突。
- **可行性证据**:[2026-04-claude-code-sideline-100k.md](findings/2026-04-claude-code-sideline-100k.md)(作者 4 个月上线二三十个英文 SEO 站,Astro + Tailwind + Cloudflare Pages 模板单站 2-3 小时上线,半自动化外链系统让 DR 从 0 突破 40-50,目前月广告收入"几十美金且在涨";SOP 涵盖选词/建站/内容/外链/变现五个环节);[2026-04-hot-keyword-quick-site.md](findings/2026-04-hot-keyword-quick-site.md)(**第二证据**:热词快站 SOP 与百年路径形成战略互补——百年=长期复利(低 KD 长尾词+9-18月起势),热词=窗口套利(新热词 1-4 周窗口+抢早期红利);26 词根库 + 评论截流打法可直接吸收;作者引用 Dan 案例 2024 末 Product Hunt 第 4 + 最高峰月 20 万点击,但需警惕幸存者偏差);[2026-05-new-keyword-5days-146k-impressions.md](findings/2026-05-new-keyword-5days-146k-impressions.md)(**第三证据**:独立开发者第 7 站起量复盘,5 天 146K GSC 展示;关键贡献=「Reddit 爆贴 → Trends 验证 → 注册域名」选词信号源 + 「翻评论提炼用户原话喂 AI 做 SEO」需求挖掘 SOP + 「day 1 GSC 没反应是常态」预期管理;**前 6 站全平第 7 站起 = 心理建设活样本**,可直接喂回 [timeline.md M3 期望校准](timeline.md#期望校准关键);本 finding 同时反向暴露作者 SOP 缺口=「Trends 上升 + 没做 Ahrefs 绝对值」——本项目 2026-05-01 在 GPT Image 2 上踩同款坑,反推作者前 2 次失败大概率也是这个原因);[2026-05-reddit-need-mining-sop.md](findings/2026-05-reddit-need-mining-sop.md)(**第四证据**:把"找小而美需求"工具链化——SEMrush 选词(KD 0-14 + CPC > 0.01)→ Reddit Answers + Atlas 总结被采纳答案(为什么选/反复理由/情绪词)→ 八爪鱼 RPA 自动监控 Subreddit 落到飞书多维表;**与既有证据的差异点**=系统化产出"候选需求池",可直接喂入选词 SOP 上游;CPC > 0.01 这个筛子本身就是公理 4 的具体化——避免找到"有流量没收入"的伪需求);[2026-05-overseas-site-backlink-full-guide.md](findings/2026-05-overseas-site-backlink-full-guide.md)(**第五证据 / 外链环节补全**:20+ 实战者综合的外链全链路 SOP——六维好外链标准 / 5 找链法 / 9 建链打法 / 7 问筛选清单 / 10 平台对比 / 6 大坑;Andy 600 美金 PMF 后投外链路径 + 鸭老师起步节奏 10-20 条/周可直接平移;补齐百年 finding 中"半自动化外链"未展开的具体方法,弥补 [search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) 只到选词不到外链的方法论缺口);[2026-05-seo-site-demand-conversion-chain.md](findings/2026-05-seo-site-demand-conversion-chain.md)(**第六证据 / 需求到转化链路补全**:作者 10 个月 10 站、最佳站日自然 UV 1264 / 月入约 300 美元 / 付费转化约 1%,关键贡献是把 SEO 站拆成"需求 → 内页 → 外链 → 交互转化"四环链路,并给出关键词意图分类、SERP Top10 交付物拆解、用户原声三次重复、首屏 CTA / 示例输入输出 / 付费点放在价值最强时刻等转化检查清单)
- **风险/未知**:
  - 资产周期与 profile "3 个月反馈"硬约束冲突——若投入此方向必须明确"这是 9-18 个月才见效的并行实验,不能挤占 M1-M3 主线时间"
  - 双证据(百年 + ai_xiaomu),但仍需 2025-2026 年 Google 算法变化后的交叉印证,尤其是 Vercel 商用禁令(必须锁死 Cloudflare Pages)
  - Google AdSense 单价对小流量站极低,二三十个站才月入几十美金,放大到月千美金需要更多站点 + 流量爆款 + 持续外链投入
  - 外链建设有"灰色"边界——作者明确放弃博客评论 spam,但行业大量"PBN / 私域博客网络"打法本质是规则边缘;用户应锁死在"白帽 + 半自动化"路径
  - 英文内容质量门槛——AI 生成 + 人工校验里"人工校验"对非母语者是真实成本
- **下一步动作(2026-04-29 升级为主线后)**:
  - **期望重新校准**:M1-M3 不追求收入达标,目标是"流程跑通 + 5-10 站上线 + DR 起势 + 第一笔 AdSense 入账(哪怕几美金)"。**3 个月反馈 = 流程闭环验证 + 第一波关键词收录,不是钱**。如果到 M3 末仍把"月入几十美金"当不达标,会陷入心理负反馈,违反 [principles.md#不要裸辞创业](principles.md#不要裸辞创业-心态急是反模式)
  - **执行节奏**:跟百年的 SOP 走——Astro + Tailwind + Cloudflare Pages 模板;选词用 [search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) SOP;外链建设吸收百年的"竞品外链 + 半自动化提交"思路(M2 启动);AdSense 申请放在 M2-M3
  - **Claude Code 工程化范式**:作者的 Skill / Agent / Hook 模式直接套用——选词 Skill / 建站 Agent / 提交 Hook,把 shark-agent 项目本身就升级为 SEO 工作台
  - **风险锁死**:坚持白帽 + 半自动化,不碰 PBN / 博客评论 spam(原文已警告,见 [risks.md](risks.md))
  - 具体启动动作见 [experiments.md 英文 SEO 内容站矩阵起步](experiments.md#英文-seo-内容站矩阵起步)

## SEO 工具站 Starter Kit + 自动防错规则

- **状态**:validating(2026-08-11 完成桌面筛选,只进入 48 小时预售验证,暂不开发)
- **核心需求假设**:正在用 AI / Astro / Cloudflare 批量做小工具站的独立开发者,愿意为一套已经处理好
  canonical、sitemap、真 404、pSEO、GSC 和部署防错的生产底座付一次性费用,避免上线后才发现整站未收录。
- **画像匹配**:**高**。买家与 X / 独立开发 / 出海建站圈重叠;用户已上线 4 站并亲历索引 bug,
  技术与内容素材都现成;1-2 周可做 MVP,不依赖 GPU、重抓数或人工交付。
- **验证成本**:**极低(预售) / 低(MVP)**。预售页 + 3 张演示图约 8-12 小时、$0-10;
  通过后 MVP 约 32-40 小时,现金成本约 $10-40。
- **可行性证据**:
  - **验证收入,相邻品类**:TrustMRR 显示 ShipFast 累计约 **$1.3M**;TanStarter 累计 **$26,178**、
    近 30 天 **$2,086**、售价 $159,渠道为 X;Directory Launch 累计 **$1,604**、售价 $199;
    React Bits Pro 近 30 天约 **$32K**。这些证明独立开发者会为「省去重复搭建」付费。
  - **自有问题证据**:[experiments.md partfit3d 索引诊断](experiments.md#结果记录) 已发现 canonical / sitemap /
    307 冲突卡住 34 条 URL、三类链接 bug 生成 25 个 404;这些可直接固化为自动测试。
  - **顾问输入(部分采纳)**:[advice/2026-08-11-build-in-public-shovel-categories.md](advice/2026-08-11-build-in-public-shovel-categories.md)
- **风险/未知**:
  - 本细分**尚无直接收入证据**;当前证据来自 boilerplate / 组件品类,不能据此宣布市场已验证。
  - Astro + Cloudflare 技术栈可能过窄;过早兼容 Next.js 会把两周范围撑爆。
  - AI 能生成模板,付费点不能是「代码多」,必须是**经过真实站点验证的发布规则 + 自动测试 + 持续更新**。
  - 用户自己的 4 站只有 31 点击 / 1338 曝光,暂时不能卖「流量结果」;只能卖上线速度和防错,宣传不可越界。
- **下一步动作**:做 48 小时预售验证:一页英文 landing + 3 张真实 bug 前后对比图 + $19 refundable deposit;
  向 15 个正在公开做工具站的人发低压力文字邀请。满足「≥3 个非熟人留邮箱且 ≥1 个付 deposit」才进入两周 MVP。

## 付费工具站 + 自有收款(Waffo)

- **状态**:validating(2026-08-10 由 `keyword-hunt` 第二轮跑出,Step 1-5 完成,等 Step 6)
- **前提变更**:用户确认开通 **Waffo**(MoR,Pancake 面向个人、无需 LLC、直打银行账户)。**「无 Stripe 资质」这条卡了三个多月的硬约束解除**,自有收款首次可闭环。见 [profile.md](profile.md#能力与资源)。
- **核心需求假设**:存在这样一类工具词 —— **输出进入用户的工作流**(不是拿完就走)、用户按月重复使用、SERP 上已有多家独立小站在直接收费、且最弱竞品的引用域 < 30。在这类词上,DR 0 新站能拿到第一笔自有收款。
- **与 4 个旧站失败的关系**:这是**对失败原因的直接修正**。partfit3d(3MF 拆分)/ aidepixelate(去像素化)的用户是 hobbyist,输出即终点,无复购,不进任何工作流 —— 所以 1338 曝光换来 0 收入不是排名问题,是**收钱场景选错**。
- **画像匹配**:高。纯前端可做、复用现有 Astro/Cloudflare 技术栈、1-2 周 MVP、目标用户是簿记员/会计(B2B professional,付费意愿明确)。
- **验证成本**:低。域名 $10 + Waffo 按成功交易计费(**3.9% + $0.50/笔**,无月费无开通费;完整费率与陷阱见 [sources/waffo.md](sources/waffo.md))。
- ⚠️ **2026-08-12 通道核实带出的两条约束**:① 提现费 **最低 $10/笔**,单价 $1-5 的定价在这条通道下几乎无毛利,与 [risks.md 低价陷阱](risks.md) 同向;
  ② Waffo KYB 审核查**商标冲突**,产品名/域名含 QuickBooks 有被拒风险。
- **可行性证据**:
  - **自有实测(最强)**:[experiments.md CSV → QBO 转换器](experiments.md#csv--qbo-转换器付费工具站2026-08-10-跑完-keyword-hunt-第二轮-step-0-5) —— 词族 ~10K/月、KD 1-14、头词 CPC $17.63;Top 10 有 **6 家独立站在收费**($15/$25/$39 订阅 + credits);最弱竞品 `toqbo.com` 仅 **24 引用域**、`filetailored.com` **26 引用域跑出 11.3K 月流量**
  - **窗口期证据**:`forgegui.com` 2026-03 注册,5 个月、DR 28 进 Stripe 收银台引荐榜第 38 位
  - **窗口期证据(同赛道内,更强)**:`accountingconverter.com` **2026-02-22 注册,5.5 个月排到 `csv to qbo converter` 第 1 名**,DR 4.6、月流量 3,782 且 +126% MoM —— 起步条件与本项目几乎相同。⚠️ 数据来自哥飞站内工具(第三方估算),**上线前用 whois 独立验注册时间**。见 [advice/2026-08-12](advice/2026-08-12-csv-to-qbo-serp-assessment.md)
  - **风险已澄清(部分采纳)**:会计类词的 **YMYL 门槛不适用** —— 文件转换是「工具功能页」不是「财务建议页」,DR 5 的 5 个月新站能排第 1 即是反证。纪律:落地页不写 financial advice 风格内容
  - **反向证据(界定边界)**:同批 `dst to pes` / `embroidery converter` 量级不成立;`supplement facts label maker` KD 2 但 CPC 仅 $1.57 → 降为备选
  - **顾问输入(部分采纳)**:[advice/2026-08-10-paid-tool-category.md](advice/2026-08-10-paid-tool-category.md)
- **风险/未知**:
  - **Intuit Web Connect(.qbo)条款未查** —— 前置阻塞项,做之前必须确认
  - **词族约 23% 是 `free` 词**,免费额度设计是成败核心变量,不是附属决定
  - **转化率 0.1-0.5% 是社群数据不是自有实测**,月 UV 1000-3000 才出第一单的门槛需要自己验
  - 竞品里有 `docuclipper.com`、`receipt-bot.com` 这类做得较大的,**不是无人区**,是「有钱但还没被大站锁死」
- **下一步动作**:见 [todos.md](todos.md) 三条 —— 查 Intuit 条款 → 开通 Waffo → 做 MVP。

## 英文联盟内容站(affiliate content site,变现导向)

- **状态**:**parked(2026-08-10)** —— Waffo 打通后自有收款优先级高于联盟。**不删**:Step 4 挖出的「厂商内容营销占据 alternatives 词」是可复用的结构性发现,联盟条款表(Kit / Surfer / Jasper / Sudowrite / Squibler 五字段)未来做联盟变现时可直接取用。
- ~~**状态**:validating(2026-08-09 由 `keyword-hunt` 流水线跑出,Step 1-5 完成,等 Step 6 实测)~~
- **核心需求假设**:在**窄场景 + 创作者向**的 SaaS 品类里(而非成熟大品类),存在 KD < 25 且 Top 10 有独立发布者在赚联盟佣金的决策词。DR 0 新发布者可以在这类词上拿到第一笔可提现佣金。
- **与「SEO 内容站矩阵 + AdSense」的关系**:是它的**变现路径替换版**,不是新方向。原路径假设 AdSense,但实际做出 3/4 是工具站,AdSense 过审难 + 量级不匹配;联盟是当前**唯一「1 次转化即验证」**的载体(无 Stripe 资质,见 [profile.md 支付通道约束](profile.md#能力与资源))。
- **画像匹配**:高。18h/周可承担(链接预算中值 25 引用域,通过时间盘硬否决);预算 $0-10;佣金 recurring 可复利。
- **验证成本**:**极低**。Step 6 用平台发布(Medium/Substack)测,1-2 小时 + $0,收录以天计。
- **可行性证据**:
  - **自有实测**(强度最高):[experiments.md AI 小说写作联盟词族](experiments.md#ai-小说写作联盟词族出单导向选词2026-08-09-跑完-keyword-hunt-step-0-5) —— 6 个词逐个扫 Top 10 出站链接,`best ai for novel writing` 有 2 个独立发布者挂 Sudowrite / Squibler 联盟链接,SERP 里排着 Authority Score 8 的极小站
  - **反向证据**(界定边界):同批 5 个高 CPC 词($7-25)联盟链接 0-1 条 → [risks.md 厂商内容营销占据 alternatives 词](risks.md#成熟-saas-品类的-alternatives--vs-词被厂商内容营销占据不是联盟站的地盘)
  - **顾问输入**(部分采纳):[advice/2026-08-09-affiliate-category-selection.md](advice/2026-08-09-affiliate-category-selection.md)
- **风险/未知**:
  - **词族量级小**:单词月量 50-260,合计约 1.3K-1.5K/月。够不够撑出第一笔佣金**未知,只有 Step 6 能答**
  - **Sudowrite 有 60 天持有期**,即使转化了,到账也要多等两个月 —— 与「3 个月看反馈」硬约束擦边
  - **10 个 EMD 域名全部可注册** 是双刃:窗口期开着,也可能意味着没人觉得这个盘子值得做
  - 平台发布(Medium/Substack)是**验证载体不是资产载体**,违反准公理 A(形态决定复利)。第 3 层出现点击后必须迁到自有域名
- **下一步动作**:见 [experiments.md 执行步骤](experiments.md#执行步骤step-6唯一产生真值的一步)。**注册 Sudowrite Rewardful 联盟 → 写一篇长文发 Medium/Substack → 等 4-6 周看第 3 层。**

## YouTube 中文 AI 不出镜频道(faceless)

- **状态**:parked(可作为低成本练手,但不作为主线)
- **核心需求假设**:面向全球华人受众(主在北美/东南亚/港台),用 AI 文本+AI 图/视频+AI 配音 0 出镜批量产出宗教、预言、玄学等高情绪类内容,通过 YouTube YPP 广告分成变现。
- **画像匹配**:中-低。该方向低成本、可兼职,但不匹配用户"通过 MVP 找真实付费用户"的目标;收益依赖平台流量和广告分成,不是清晰的 B2B/开发者/企业客户付费。
- **验证成本**:中。单号内容生产成本低,但 YPP 门槛、封号风险、内容生产和账号养护会拉长验证周期,且 2026 年红利已收窄。
- **可行性证据**:[youtube-ai-faceless-channel-sop.md](findings/youtube-ai-faceless-channel-sop.md)(作者 0 经验 13 天开 YPP,单视频成本 3-5 RMB,头部账号月入过万)
- **风险/未知**:
  - 红利窗口已收窄(2024-11 启动 vs 2026-04 当前):该作者后续连载提到自家 50 万粉账号已被封,YouTube 对 AI 低质内容打压在加强
  - 需要验证:今天新号开 YPP 的中位时间是多少?宗教/预言细分赛道还能不能进?
  - 平台单点依赖极重,需账号矩阵 + 跨平台分发设计
- **下一步动作**:
  - 找 2025 年下半年 / 2026 年的同赛道实操贴(尤其封号后重起的复盘),确认现在还能不能入
  - 调研 YPP 政策更新(2025 年 7 月 YouTube 收紧"reused content"规则的影响)
  - 如果决定试错,可以套作者的五术框架做一次低成本演练(单号月成本可控在 500 RMB 内)

## 支付引荐扫描:品类与候选(2026-08-26 首轮)

- **信心等级**:低(仅两个月对比,未做人工开站与收入估算)
- **数据源**:[支付引荐表](sources/payment-growth.md),SimilarWeb 第三方估算,拉取 2026-08-26。
  四平台 × 2026-06/07,8/8 快照 `complete=true`,4908 行。
- **口径提醒**:引荐访问 = 有人走到结账页,**不等于付款、不等于收入**。只取方向和相对量级。

### ~~品类级(付款意图)~~ —— **2026-08-28 全段作废**

~~电脑/电子/科技 +37.9%「AI 付款意图仍在加速,与『AI 已经卷完了』相反」~~

**2026-08-28 逐站拆解后推翻**:那 +37.9% 里 **81% 是 `higgsfield.ai` 一家**。
复核 Stripe 表 06→07 的 14 个涨跌品类,**每一个**都由单站贡献 76–124% 的变化量,
且 SimilarWeb 的 `category` 字段大量错标(助眠音频标 Email、AI IDE 标 Banking、面部评分标 Video Games)。

**这个数据源给不出品类级结论**,只能给单站线索。
详见 [sources/payment-growth.md 陷阱 6](sources/payment-growth.md)。

### 候选(进入人工核查,不构成推荐)

| 候选 | 证据 | 相关度 |
|---|---|---|
| **outrank.so** | Stripe 位次 957→307,引荐 4.8k→17.9k,整站 16.6 万 growing;**已人工核查** | **高价值对标、非直接克隆候选**。$99/月卖 SEO 结果托管,但自然搜索只占 19.8% 且其中 51% 为品牌词;公开案例显示从 $400 MRR 到七位数 ARR 的关键是战略分发合伙人。详见[第五站实验](experiments.md#第五站候选筛选与付费意愿验证m5-前置2026-08-26) |
| **forgegui.com** | 位次 41→16,引荐 26.4 万,整站 6 个月 3.8k→63.4 万,域龄 **171 天**;**已人工核查** | 收费层成立,但靠游戏开发生态、品牌与社区起量;不进入第五站探针 |
| **trustmrr.com** | Stripe + LS **双平台**同向上升,整站 76万→92万,域龄 299 天;**已人工核查** | 保留为收入证据库 / 曝光渠道;数据验证与双边市场不可冷启动复制 |
| adspirer.ai | 整站 6 个月 64 倍,Stripe 位次 640→171;**已人工核查** | 保留“AI 客户端委派高价值操作、按 task 收费”的形态;广告代理本身不做 |
| app.tryatria.com | Stripe+Paddle 双平台,整站 24.8万→36.6万;**已人工核查** | $129–959/月卖创意运营闭环;数据、集成与服务壁垒过重,不进入探针 |
| 3daistudio.com | LS 位次 189→12,整站 72 万 sustained_growth | 已开站,见 [experiments.md](experiments.md)——**结论是竞品情报,不是候选** |

**已剔除**:位次升但整站在跌的矛盾线索(kaze.ai / toolify.ai / theresanaiforthat.com 等)、
盗版站(asurascans)、PayPal 独家来源的巨头(rakuten / vinted / skyscanner)。

**观察到的一个变现形态**:toolify.ai / theresanaiforthat.com / betalist.com / trustmrr.com /
landingpage.fyi / saaspo.com 这批**目录站集体在 Lemon Squeezy 侧上升**——通常意味着目录在卖付费收录位,
而且是"目录 → LS 结账"这条极短的付款链路。**待验证,未开站。**

- **下一步(2026-08-26 桌面筛选已收口)**:⛔ 不扩大候选池。直接克隆候选为 0;仅保留
  `AI 建站发布防错 + 持续 SEO 巡检`进入 offer / 访谈 / deposit 探针,未批准注册域名或开发。
  证据与门槛见[第五站实验](experiments.md#第五站候选筛选与付费意愿验证m5-前置2026-08-26)。

## 支付引荐扫描:Stripe 单平台复跑(2026-08-28 第二轮)

- **信心等级**:低(第三方估算,两月对比,收入估算为宽区间)
- **数据源**:[支付引荐表](sources/payment-growth.md),SimilarWeb,**拉取 2026-08-28**。
  `checkout.stripe.com` 2026-07 快照 `complete=true` / 968 行(2026-08 上游尚未发布,406)
- **本轮唯一的方法论产出**:`category_conclusions` 判死(见上一节的作废说明 + 陷阱 6)

### 唯一带走的候选:**照片 / 形象「评分诊断」**(不是修图)

两个独立站在同一张表上同期上冲,一新一老,互为交叉证据:

| 站 | 证据 | 形态 |
|---|---|---|
| `pslscale.com` | 位次 927→278(+649),引荐 4,975→19,231,整站 15.0万→20.5万,域龄 **8 个月** | 上传照片出面部评分 + 改进建议,**按次积分**(基础 10 分、AI 报告 +20 分),新号送 10 分 |
| `photofeeler.com` | 位次 903→213(+690),引荐 5,172→24,007,整站 68.7万→90.9万,域龄 **13 年** | 真人投票给约会/职业/社交照片打分,免费靠互投换额度,付费买加速 |

**为什么它过了 [08-26 三道新判据](todos.md)**:
① 用户是为"看自己几分"付费,不是为"省下一次修图"付费——**虚荣消费,不是工序**;
② **不在被定价为 0 的那一层**——[aidepixelate 复盘](risks.md)证明市场把 AI *修复*定价为 0,
   但 photofeeler 靠真人评价活了 13 年,说明「评价」这一层没被 AI 挤掉;
③ 2 周内可验——同 [fast-payment-validation](methods/fast-payment-validation.md) 的 Fiverr 路径。

**⚠️ 未做的事**:没查搜索量 / CPC / KD,没验证英文词族,没估流量来源构成。
在做这些之前它只是"值得开一次探针",不是方向。

### 全部丢弃(不建待研究池)

| 站 | 引荐 07 | 丢弃理由 |
|---|---|---|
| `higgsfield.ai` / `elevenlabs.io` / `suno.com` / `platform.kimi.ai` / `midjourney.com` | 15万–269万 | 融资巨头,形态不可复制 |
| `dearkellyfilm.com` | 22.4万(NEW 进表即第 24) | 单片纪录片自建站直销($5.55 租 / $15.55 买),**一次性事件不可复制**;但可作"自建 checkout 卖数字内容仍成立"的旁证 |
| `lightreel.ai` | 2.9万 | $199/月,6 个月新站,但**引荐 28,977 vs 整站 48,726 = 59%**,触发[陷阱 3 快速排雷](sources/payment-growth.md);数据存疑 |
| `app.uare.ai` | 19.5万 | 同上,**引荐 19.5 万 > 整站 3.1 万**,物理上不成立;且已融 $10.3M |
| `hyperagent.com` | 13.7万 | 整站 6 个月 2.0万→67.5万,但 2005 年老域名 + 403 拒抓,查不动 |
| `outrank.so` / `forgegui.com` / `adspirer.ai` | — | **08-26 首轮已人工核查并否掉**,本轮重复命中,结论不变 |
| `arenaclub.com` / `mage.space` / `csfloat.com` 等 | — | 品类(球星卡/AI 绘图/CS 皮肤)与本项目能力和受众无交集 |

## 模型词入口 + 通用品牌(「改名逃逸」,2026-08-27)

> **这不是一个方向候选,是一个可迁移的冷启动形态。** 从[禁区 1 复核](findings/2026-08-27-columbus-post-update-audit.md)
> 里剥出来的唯一符合准公理 A 的动作。

- **状态**:explore(未验证,来自第三方估算样本观察)
- **信心等级**:低——哥伦布快照 2026-07,单品类(`nano banana`)34 站观察,**无自有实测**
- **核心假设**:热词/模型词只当**入口流量**用,域名和品牌从第一天就用通用词,
  等入口词衰减时站已经靠通用词承接住,不跟着词一起死。
- **证据(哥伦布 `nano banana` 全量,2026-05→07)**:

  | 域名 | 注册 | 07 月访问 | 环比 |
  |---|---|---|---|
  | `imageeditorai.ai` | 2026-06-18 | 61,149 | 起步月 |
  | `eimg.ai` | 2026-07-09 | 29,247 | 起步月 |
  | `kimg.ai` | 2026-01-29 | 120,940 | +23% |
  | `imagify.ru` | 2026-02-18 | 226,879 | +21.7% |
  | 对照:`nanobanana.io` | 2025-08-14 | 1,365,436 | **-1.8%,连跌 3 月** |

  **最直接的一条**:`nano-banana.com`(2025-08-14 注册,SERP pos 10)标题已改成
  「Nano Banana AI Image Editor – Free Online **| EIMG AI**」——**老玩家自己在往通用品牌迁**。

- **为什么可能对本项目有用**:自有四站的选词逻辑一直是「找一个不会死的小词」,
  这条给的是另一种解法——**允许用会死的大词做冷启动**,只要品牌层不绑死在那个词上。
  与 [risks.md 做在被定价为 0 的那一层](risks.md) 不冲突:它解决的是获客,不解决变现。
- **风险/未知**:
  - ① **没有一个样本证明这条路走通了** —— `imageeditorai.ai` 只有 1 个月数据,`eimg.ai` 抓取返 `301`。
    观察到的是**动作**,不是**结果**。
  - ② 入口词本身要能进得去。`nano banana` 的入场券是 KD 78 / 310 引用域 / SERP 4 位归厂商,**这个词本身进不去**。
    形态可迁移,词不可迁移。
  - ③ 与准公理 A 只是**看起来**兼容:通用品牌是不是真能在入口词衰减后接住流量,未验证。
- **不做的事**:⛔ 不因为这条去抢注模型词域名(禁区 1 未解除);
  ⛔ 不进第五站候选池——第五站已按 [08-26 三条新判据](todos.md)收口,本条不满足「2 周内验证付费意愿」。
- **下一步动作**:等 3 个月后复拉 `imageeditorai.ai` / `eimg.ai` / `kimg.ai` 的流量与自然搜索占比。
  **若三者在入口词衰减后仍增长 → 形态成立,再考虑迁移;若同步下跌 → 这只是同一个脉冲换了个域名,本条作废。**
- **关联**:[risks.md 模型词域名站](risks.md#模型词域名站入口靠抢时间留存靠改品牌两头都不占违反准公理-a)、
  [findings 08-27 禁区 1](findings/2026-08-27-columbus-post-update-audit.md)

## 电商 / 房产「工序型」图像处理(2026-08-28,来自 enhancecraft 拆解)

- **状态**:候选,**唯一同时通过第五站三道门的方向**,待付费探针
- **核心假设**:AI 图像处理里,**买家拿它去做生意的那几道工序**(ghost mannequin / virtual staging /
  day-to-dusk / 产品阴影)有真实的按张成交价,而 upscale / denoise / remove background 那一层已被定价为 0。
  这个价差**同一个站里就能看到**,不需要跨品类比较。
- **证据**:
  - **人工服务公开报价**(BoxBrownie 等,2026):`image enhancement $2/张` · `day-to-dusk $5/张` ·
    **`virtual staging $30/张`**,行业均价 $20–40/张;物理 staging 一套房 $2,000–5,000。
  - **CPC 对齐**(SimilarWeb API,2026-07 美区):`virtual staging` 上限 **$11.93**(SERP 20.9% 广告位)、
    `ghost mannequin` 上限 **$7.74** —— 比 [risks.md 记录的 AI 品类水位](risks.md) 高一个数量级。
  - **可打性**(gefei-kd):`ghost mannequin` 难度 **26.8/100**、月搜 4,310、
    进前十 **20–45 引用域**;前十第 2 名 `adworker.ai` **域龄 6 个月 / DR 3**,靠产品力站住。
    与 `stl repair`(justfixstl.com 10 个 dofollow 域排第 2)同量级门票。
  - 反例同时成立:`virtual staging` 难度 59–75、链接预算 85–190 引用域、
    第 1 名是域名直拼 + DR 59 + 3.7 年的 `virtualstagingai.app` —— **头词不可打,只能打房型/平台长尾**。
- **对标站**:[enhancecraft.com 拆解](findings/2026-08-28-teardown-enhancecraft.md)
  —— ⚠️ **它本身是反面教材**:7 个月域龄、DR 0、自然搜索 0、月访问 3,548 且疑似发布脉冲。
  **拆的是它选的需求层和页面结构,不是它的成绩。**
- **风险/未知**:
  - ① **买家圈层与 X / 独立开发圈完全不重叠**(电商卖家、房产经纪),
    与 [csv-to-qbo 圈层错配](timeline.md) 同型 —— 只能靠 SEO 冷启动,Build in Public 带不动。
  - ② 上游模型开源,零护城河;竞争会把单价压向 0(与 [aidepixelate Etsy 复盘](experiments.md) 同一机制)。
  - ③ 正边际成本(GPU 推理),免费档必须设计得能挡住白嫖。
- **下一步动作**:**先测钱,不建站**。按 [fast-payment-validation](methods/fast-payment-validation.md)
  在 Fiverr 挂 ghost mannequin 修图服务,14 天看有没有真实订单。有单再谈工具站。
