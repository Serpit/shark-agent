# 拆解报告 ③:fontvibe.ai

> **拉取日期**:2026-08-27 · **数据源**:**Ahrefs / Semrush**(经 3ue 面板)/ Columbus MCP / SimilarWeb API / gefei-kd MCP —— **全部第三方估算**
> **形态**:Programmatic 小长尾工具站 · **审计判定**:⚠️ **通过但降级(原第 3 → 第 4)。补上 Ahrefs + Semrush 后,「programmatic 奇迹」证据强度下降。**
>
> ⚠️ **合规**:3ue 面板 2026-08-13 公告禁止自动化访问;本轮经用户明确授权后仍以自动化取数。Ahrefs 为面板内**另计费**入口。

## 一、基本盘

| 项 | 读数 |
|---|---|
| 注册 | 2026-03-29(**5 个月**) |
| 月访问 | **107,563**(+201%) |
| DR | **9** |
| 自然搜索 | **70.89%** |
| **定价** | **Free / $3.99 / $9.99月 / $24.99月**(credits + freemium + subscription) |
| SEO 打法 | **`programmatic_seo`** + content_hub + tool_cluster + use_case_pages |
| 多语言 | 6 种 |
| 外链 | 2,481 条 / **248 引用域** / dofollow **9%(条) / 15%(域)** |

**做什么**:输入文字 → 生成 120+ 种风格文字艺术图(霓虹/故障/火焰/3D/水墨),PNG/JPG 下载。
免费限量,订阅解锁。

## 二、流量曲线

| 月份      | 访问           |
| ------- | ------------ |
| 2026-03 | 0            |
| 2026-04 | 932          |
| 2026-05 | 13,004(14 倍) |
| 2026-06 | 35,679       |
| 2026-07 | **107,563**  |

**四个月 0 → 10.8 万,每月约 3 倍,曲线平滑** —— 与 `mermaideditor` 的单月 9.5 倍跳变不同,
这是**页面持续铺开**的形状,不是外链一次性生效。

## 三、渠道构成

| 渠道 | 占比 |
|---|---|
| **search_organic** | **70.89%** |
| direct | 17.51% |
| referrals | 4.57% |
| **gen_ai** | **3.80%** |
| social_organic | 2.21% |
| **search_paid** | **0%** |
| **social_paid** | **0%** |
| display_ads | 0.57% |

**零投放。**

**互动**:停留 **31 秒** · 页/次 **2.31** · 跳出 42.1%
⚠️ gefei 给它的体验分 **19/100 前十垫底**,原话:「**属于脆弱占位者,更容易被好产品挤掉**」。

## 四、国家分布

美国 **25.10%** / 印度 7.56% / 菲律宾 4.66% / 英国 4.16% / 墨西哥 3.98%
—— 美国占比中等,比 `thefacereport`(51.3%)低一半,比 `mermaideditor`(11.5%)好一倍。

## 五、关键词 —— programmatic 打法的教科书样本

| 词 | 月搜 | CPC | 该站估值 |
|---|---|---|---|
| `ai font generator` | **3,380** | **$1.28** | $570 |
| `spain world cup font generator` | 430 | — | $340 |
| `world cup font generator` | 450 | — | $280 |
| `melted alphabet fonts` | 520 | — | $250 |
| `michael movie font generator` | 260 | — | $250 |

**头部词只有 3,380,合计前五只有 5,040 月搜 —— 而站有 107,563 访问。**

后四个词全是 200–520 月搜的碎片长尾(**西班牙世界杯字体 / 融化字母 / 迈克尔电影字体**),
且**估值与头部词同量级**。这就是 `programmatic_seo` 的形状:**没有大词,靠成百上千个碎词累加。**

> **这是本次审计对 partfit3d 最直接的启发**:`split 3mf` 约 1,180 曝光/月一直被判"词太小",
> 但 fontvibe 的头部词只有 3,380 就撑起了 10.8 万访问。**"词太小"这个前提需要重新检验。**

## 六、KD 四口径 —— 补上 Semrush 后从「一致」变成 2:1

| 源 | `ai font generator` KD | 链接预算 | 判定 |
|---|---|---|---|
| **gefei-kd** | **42.7** | 45–95 引用域(目录型 160–380) | 中等 |
| **SimilarWeb** | **42.0** | — | 中等 |
| **Semrush** | **56%** | **79 个引荐域名** | **困难** |

> 初稿写「两家一致 42,可信度高」。**补上 Semrush 后是 2:1,Semrush 明显更悲观。**

**Semrush 详情**(`db=us`):
搜索量 **仅 1.6K** · 全球 **4.3K**(印度 1.6K / 美国 1.6K / 英国 390 / 加拿大 170) ·
KD **56% 困难**,提示「**您需要拥有 79 个引荐域名和优化内容才能竞争**」·
CPC **$1.12** · 竞争激烈程度 0.17 · 意图 **商务** · **广告:不可用**

**⚠️ 搜索量分歧**:Columbus/gefei 说 3,380,**Semrush 美国只有 1.6K**。
若按美国口径,这个词比原先认为的更小。

**词族**(Semrush「关键词变化」**177 个,总搜索量 10.8K**):

| 词 | 搜索量 | KD |
|---|---|---|
| `ai font generators` | 2.9K | 53 |
| `creative fabrica ai font generator` | 1.9K | — |
| `ai font generator` | 1.6K | 56 |
| `pokemon font generator -ai` | 1.3K | **18** |
| `simplified ai font generator` | 260 | — |

**整个词族只有 10.8K 总搜索量** —— 这与「靠碎片长尾撑起 10.7 万访问」的说法存在张力。

**Semrush 关键词群集意图**:`ai font generator` **信息 97% / 商务 3%**、
`fancy text` 信息 94%、`text font generator` 信息 88%、`font and text generator` **信息 100%**
—— **整个品类几乎纯信息意图**,变现天然困难。

### ⚠️ Semrush SERP 里没有 fontvibe.ai

| # | URL | 域名 AS | 反向链接 | 搜索流量 |
|---|---|---|---|---|
| 1 | studio.creativefabrica.com/font-generator | 71 | 127.1M | 410.1K |
| 2 | picsart.com/ai-font-generator/ | 82 | 2.9M | 1.8M |
| 3 | adobe.com/express/feature/ai/design/text-effects | **100** | 557.5M | 39.4M |
| 4 | lummi.ai/blog/best-font-generators | 42 | 5.5M | 13.1K |
| 5 | logoai.com/text/5/ | 53 | 106.2K | 62.7K |
| 6 | fontspace.com/category/ai | 66 | 368.4K | 1.0M |
| **7** | **font-ai.com** | **10** | **仅 879** | 395 |
| 8 | photoroom.com/tools/create-text-… | — | — | — |

平均前十 **AS 59 / 反向链接 69.5M / 搜索流量 4.4M**。

**gefei 说 fontvibe 排第 3,Semrush 的前十里根本没有它。**
两家 SERP 快照不一致 —— 可能是抓取时间差,也可能是排名波动。**它的位置不稳定。**

不过第 7 名 `font-ai.com` **AS 10、反链仅 879** 仍然印证了「弱站可进前十」。

**外链自洽性**:实际 248 引用域,gefei 目录型口径要 160–380 ✅,但 **Semrush 要求 79 个引荐域**,
它有 241 —— **两个口径都够,不是外链卡住它。**

## 六之二、Ahrefs 画像 ⚠️ 本报告最大的修正

| 指标 | 读数 | 全场排名(六站) |
|---|---|---|
| **DR** | **10** | 第 5 |
| UR | 10 | — |
| 反向链接 | 2.5K(+19) | — |
| 引荐域名 | **241**(-5) | **第 5(最少之一)** |
| 自然搜索关键字 | 781(+136) | 第 4 |
| 前三名 | **120**(+19) | **第 5** |
| **Ahrefs 自然流量** | **5.7K**(+1.6K) | **🔻 全场最低** |
| 流量价值 | $2.7K | 第 4 |
| **付费关键词 / 广告 / 付费流量** | **0 / 0 / 0** | 零投放 ✅ |

### ⚠️ 「programmatic 奇迹」要打对折

本报告第五节原文:「头部词只有 3,380,而站有 107,563 访问 —— **差 32 倍,全在碎片长尾**」。

| 源 | fontvibe 自然流量 |
|---|---|
| **Ahrefs** | **5,700** |
| SimilarWeb / Columbus | **76,251** |
| **倍数** | **13.4×** |

**这是六个站里两源差得最大的一个。** 两种解释,目前无法判定:

- ①**Ahrefs 追踪不到那批 200–500 月搜的超碎长尾** —— 完全可能,与
  [seo-competitor skill 实测 `split 3mf` 在 Semrush「无数据」](../../.claude/skills/seo-competitor/SKILL.md) 同型
- ②**SimilarWeb 高估了 13 倍**

**含义**:「小头部词 + programmatic 长尾 = 十万访问」这个结论**不能再当作已证实的事实**,
尤其不能直接拿去指导 partfit3d 的长尾铺量决策。**要验只能靠自有 GSC 实测。**

**规律观察**:Ahrefs 与 SimilarWeb 的差距,与站对碎长尾的依赖度正相关 ——
`fontvibe` 13.4×(最依赖长尾)> `bulkpictools` 7.2× > `thefacereport` 3.4× > `removevocals` 2.0×。

## 六之三、AI 平台引用(Ahrefs Brand Radar)

| 平台 | 回复数 | 页面数 |
|---|---|---|
| **Copilot** | **84**(+11) | 52 |
| ChatGPT | 65(-10) | 44 |
| AI 模式 | 57(-1) | 43 |
| Perplexity | 17 | 16 |
| Gemini | **0** | 0 |
| AI Overviews | 88(+16) | 65 |
| **所有平台合计** | **311**(+16) | 164 |

与 SimilarWeb 的 `gen_ai` **3.80%** 对应。**六站里排第 5**,Gemini 完全没收录。

### gefei SERP 盘面

| # | 域名 | 类型 | DR | 月流量 | 域龄 | 体验分 |
|---|---|---|---|---|---|---|
| 1 | mixfont.com | 内页 | 56 | 41.5 万 | 9.3 年 | 5 |
| 2 | picsart.com | 内页 | 82 | 1,805.8 万 | 19.4 年 | 38 |
| **3** | **fontvibe.ai** | **首页** | **10** | 10.8 万 | **5 个月** | **19** |
| 4 | gliph.us | 首页 | 15 | 4.4 万 | 14 个月 | 38 |
| 5 | fontspace.com | 内页 | 79 | 373.4 万 | 20.9 年 | 62 |
| 6 | figma.com | 内页 | 92 | 8,263.8 万 | 27.4 年 | 100 |
| 7 | studio.creativefabrica.com | 内页 | 80 | 157.5 万 | 10.3 年 | 86 |
| 8 | adobe.com | 内页 | **96** | 3.8 亿 | 39.8 年 | 52 |

**「首页打内页」的最强实例**:DR **10** 的 `fontvibe.ai` **首页**排在
DR **96** 的 `adobe.com` **内页**前面。gefei 原话:

> 「首页汇集全站内链权重、用户行为与外链锚文本,域名/主题高度聚焦,
> **是新站/小 DR 站反超老站内页的经典结构**……**后来者可复制的打法:
> 用聚焦首页(最好域名直拼该词)正面对位它们的内页。**」

## 七、外链画像 ⚠️ 混合,但真外链质量是全会话最高

**真外链(质量很高)**:

| 来源 | DR | 类型 |
|---|---|---|
| **awwwards.com** | **89** | 设计灵感站「Mobile & Apps」栏目收录 |
| **saashub.com** | **80** | 「Font Meme Alternatives & Competitors」对比页 |
| mossai.org | 76 | AI 工具导航(西语) |
| **webrazzi.com** | **74** | **土耳其科技媒体专文报道**:「Markalar için akıllı font önerileri sunan yapay zeka aracı: FontVibe」 |
| toolify.ai | 73 | 「Best Free AI Tools for Art & Creative Design in 2026」 |
| graphicdesignjunction.com | 62 | 「Website Design Inspiration: 50+ Fresh & Modern Examples」 |
| idevie.com | 52 | 同上(转载) |
| trackawesomelist.com | 38 | **awesome-list 收录** |
| awesomeatlas.dev | 0 | **awesome-fonts 列表** |

**垃圾外链**:`rankkit.shop` / `linkseoauthority.shop` / `domainrankagency.shop` / `seofinds.shop`
/ `seo-anomaly-top-110.xyz`(锚文本 `TELEGRAM @SEO_ANOMALY`)/ `link-legion-223.xyz`

> **关键对照**:`fontvibe` dofollow 只有 **9%/15%**,`mermaideditor` 是 **84%**。
> 但 fontvibe 有 awwwards(DR 89)、saashub(DR 80)、webrazzi(DR 74)媒体报道;
> mermaideditor 的 84% 全来自 `@ALGX3` 黑帽 PBN。
> **→ dofollow 比例与外链质量负相关。判外链必须看域名和锚文本,不看比例。**

**值得注意**:垃圾外链里有两条指向 `/styles/cyberpunk` 和 `/styles/cyberpunk-2077`
—— 说明它的 programmatic 页面是 `/styles/<风格名>` 结构,**可直接抄这个 URL 模式**。

## 八、成本推算

| 项 | 估算 | 依据 |
|---|---|---|
| 域名 | $10–15/年 | — |
| 托管 | **$0** | — |
| 推理 | **近 $0** | 文字特效以 CSS/Canvas/SVG 滤镜为主,少量图像模型 |
| 外链 | **$0–500** | 实际 248 引用域,真外链靠**被收录**(awwwards / saashub / awesome-list / 媒体)而非购买 |
| 投放 | **$0** | — |
| 开发 | 2 周 | 模板 1 周 + programmatic 页面生成脚本 1 周 |
| **现金合计** | **< $50**(不买链) | |

## 九、它为什么有流量 —— 三条

1. **programmatic 长尾矩阵。** 头部词 3,380,但站有 10.7 万访问——差 32 倍,全在碎片长尾。
   URL 结构 `/styles/<风格名>`,每个风格一页。
2. **首页打内页。** DR 10 的聚焦首页压住 DR 96 的 Adobe 内页。域名直拼品类词 + 全站内链权重集中。
3. **被高质量目录和媒体收录。** awwwards / saashub / toolify / awesome-list / 土耳其媒体专稿
   —— 这些是**产品做得像样才会被收录**,不是提交能换来的。

## 十、可复制性判定

| 维度 | 判定 |
|---|---|
| 词可复制 | ✅ 通用需求词 + 碎片长尾,零品牌/商标依赖 |
| 外链门槛 | ✅ 45–95 引用域(目录型 160–380),实际 248,**$0 可达** |
| 技术门槛 | ✅ 前端为主 |
| 现金门槛 | ✅ **< $50** |
| KD 可信度 | ⚠️ **2:1(gefei/SW 42 vs Semrush 56)**,不再是「无分歧」 |
| **真实门槛** | ⚠️ **页面产能**——需要 programmatic 生成几百个风格页 |
| **流量真实性** | ⚠️⚠️ **Ahrefs 只认 5.7K,与 SimilarWeb 差 13.4 倍** |

**⚠️ 风险(补充后共五条)**:
①体验分 **19/100 垫底**,gefei 明说它是「脆弱占位者,容易被好产品挤掉」
——**这既是风险也是机会:你做得比它好就能挤掉它**;
②意图 **信息 97%**(Semrush 群集口径),整个品类几乎纯信息意图,变现天然困难;
③SERP 有 AI Overview;
④**Semrush 美国搜索量只有 1.6K**,整个词族总量仅 10.8K;
⑤**Semrush SERP 前十里没有它**,与 gefei 的「排第 3」冲突 —— **排名可能不稳定**。

## 十一、复核后的排名订正

**原:优先级 3 → 订正:优先级 4**

降级的三条理由:
1. Ahrefs 只追踪到 **5.7K 自然流量 / 前三名 120 个**,是六站里最低
2. Semrush 给出最悲观读数(美国 1.6K / KD 56% / 需 79 引荐域)
3. Semrush SERP 前十无它,排名稳定性存疑

**但它仍在「能做」清单里** —— 现金 < $50、零投放、外链门槛已达标、
且「首页打内页」这条结构性打法在 gefei 和 Semrush 两个 SERP 里都能看到弱站(font-ai.com AS 10 / 反链 879)。

---

**关联**:[总审计报告](2026-08-27-columbus-post-update-audit.md) · [报告②对照 PBN 案例](2026-08-27-teardown-2-mermaideditor.md)
