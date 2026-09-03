# 拆解报告:enhancecraft.com

> **拉取日期**:2026-08-28 · **数据源**:Columbus MCP / SimilarWeb API 直连 / gefei-kd MCP / 站点实读
> —— 除站点实读外**全部第三方估算**,未与任何 GSC 真值交叉
> **形态**:AI 图像工具 all-in-one(24 工具)+ 积分订阅 · **判定**:**整站不可克隆,单点可切**

## 一句话结论

**这不是一个成功案例,是一个上线两个月、还没被验证的实验。**
它 7 个月域龄、DR 0、自然搜索 0、月访问 3,548 —— 比我们自己的 partfit3d 好不到哪去。
**它真正值钱的地方不是它的成绩,是它选的那一层需求。**

---

## 一、基本盘

| 项 | 读数 | 来源 |
|---|---|---|
| 域名注册 | **2026-01-19**(7 个月) | Columbus |
| 月访问 | 2026-06 **26** → 2026-07 **3,548** | Columbus + SimilarWeb 双源一致 |
| 自然搜索占比 | **0**(`estOrganic` = 0 / `tsSearchOrganic` = 0) | Columbus |
| DR | **0** | Columbus |
| 引用域 / 外链 | 466 / 525,**dofollow 仅 8% / 9%** | Columbus |
| 全球排名 | 4,751,344 | SimilarWeb |
| 国家分布 | 美国 **88.7%** / 印度 8.1% / 菲律宾 2.6% | SimilarWeb |
| 互动 | 跳出 38.8% · 2.19 页/次 · **停留 28 秒** | SimilarWeb |
| 定价 | Free(25 积分/月)/ **$9 / $24 / $59** 月订阅 + PAYG 积分 | 站点实读 |
| 收款通道 | **未检出**(Columbus 的 `paymentProviders` 为空;可能在登录后) | Columbus teardown |
| 技术栈 | Next.js · GA4 · 无广告网络 · 无联盟链接 | Columbus teardown |

**⚠️ 停留 28 秒 / 2.19 页**:这是"进来看一眼就走"的数字,不是"上传图片等 10-30 秒再下载"的数字。
真正用了工具的会话应该显著更长。**这 3,548 次访问里大部分人没有用产品。**

---

## 二、流量来源:**它没有 SEO 流量**

这是全篇最重要的一条,也是最容易看反的一条。

| 假设 | 证据 | 结论 |
|---|---|---|
| 靠 SEO 起来的 | `estOrganic` = 0、DR 0、124 页上线不到 2 个月 | ❌ |
| 靠外链权重 | 466 引用域**几乎全是 SEO 垃圾站** | ❌ |
| 靠发布平台 / 目录 | 有 `wellfound.com`(DR 87)公司页、UIComet launch 收录 | ✅ 最可能 |

### 那 466 个引用域是什么

拉出前 20 条,**只有 2 条是真的**(`wellfound.com` 公司页、`analyticshaven.top` 统计站),
其余全是同一批 `.shop` / `.store` 自动生成的 SEO 服务垃圾页,锚文本长这样:

> "I remember when enhancecraft.com was barely getting any traffic. A friend recommended
> SEOExpress.org…"(同一段文案出现在 8 个不同域名上)

> "Rank enhancecraft.com higher with high-quality backlinks, guest posts…"

这**不是它买的外链**,是任何新域名一旦进入某些数据库就会自动收到的爬虫垃圾。
`backlinker.shop`(DR 65)那条标题里直接写着 "All Niches Allowed (Gambling Included)"。

**→ 复用 [mermaideditor 拆解](2026-08-27-teardown-2-mermaideditor.md) 的判据并反向补充一条:
dofollow 比例低(8%)也不等于健康 —— 要看引用域的名字。这里是「466 个域名,真外链 2 个」。**

### 所以 3,548 访问从哪来

最可能是 **Product Hunt / UIComet 等发布平台 + 目录收录的一次性脉冲**。
特征吻合:单月从 26 跳到 3,548、美国占 88.7%、停留 28 秒、自然搜索 0。

**这类流量不复利。** 下个月的读数才是真正的分水岭 —— 掉回几百就是纯发布脉冲。

---

## 三、需求是什么:**它的 24 个工具分属三个完全不同的定价层**

这是整个拆解里唯一真正有价值的东西。把它的工具按**市场已有的成交价**排开:

| 层 | 工具 | 市场成交价(BoxBrownie 公开报价) | 判定 |
|---|---|---|---|
| **零元层** | crop / resize / convert / compress | $0 | 免费引流,无收入意义 |
| **准零元层** | upscale / denoise / deblur / dehaze / remove background / face restore | **image enhancement $2/张** | ⚠️ 已被定价为 0 |
| **有钱层** | **virtual staging $30/张** · **ghost mannequin** · day-to-dusk $5/张 · item removal $5 起 | 人工服务 **$16–75/张**,均价 $20–40 | ✅ 真钱在这里 |

> 物理 staging 一套房 $2,000–5,000;虚拟 staging 一张 $16–75。
> **这是一个买家已经在付钱、且付的是每张几十美金的市场。**

### 对照我们自己的两条已有结论

- **[risks.md「做在被定价为 0 的那一层」](../risks.md)**:它的**前两层完全踩中**
  —— `remove background`(月搜 430 万)、`ai image enhancer`(月搜 15.4 万)是流量最大的词,
  也正是被 Canva / remove.bg / Photoroom 免费捆绑掉的那一层。
- **[risks.md「AI 工具站 CPC 系统性低」](../risks.md)**:**这次是例外,必须记下来**。
  `virtual staging` CPC 上限 **$11.93**、SERP 里 **20.9% 是广告位**;
  `ghost mannequin` CPC 上限 **$7.74**。
  两个都远高于 08-13 记的「AI 品类 CPC $0.5–1.5」。
  **→ 差别不在"是不是 AI",在"买家是不是拿它做生意"。房产经纪和电商卖家是在花钱赚钱。**

### 它自己的定价把这层砸穿了

$24/月 800 积分,virtual staging 6 积分/张 → **约 133 张/月 ≈ $0.18/张**。
人工同一张 **$30**。**它在用 1/167 的价格卖同一个交付物。**

这既是它的全部理由,也是它的全部风险:
一旦买家把"AI 虚拟布置"当成一个 $0.18 的东西,这一层就会走上和 upscale 完全一样的路
—— 这正是 [aidepixelate 复盘](../experiments.md) 里 Etsy 卖家强调「by hand / not AI」的同一个机制。

---

## 四、SEO 策略:结构教科书,执行未验证

sitemap 124 个 URL,拆开看结构非常干净:

| 页型 | 数量 | 例子 | 意图 |
|---|---|---|---|
| 独立工具页 `/free-*` | **24** | `/free-virtual-staging`、`/free-ghost-mannequin` | 一页一词族,主攻 `free X` |
| 博客 | 42 | 24 篇工具指南 + 7 篇 `enhancecraft-vs-*` + 11 篇行业内容 | 内容中心 |
| **场景页矩阵** `/upscale/{用途}` | 10 | `/upscale/passport-photo`、`/upscale/wedding-photos` | programmatic SEO |
| **平台页矩阵** `/remove-background/{平台}` | 10 | `/shopify`、`/amazon`、`/etsy`、`/poshmark`、`/depop` | 买家在哪就建哪一页 |
| **房型页矩阵** `/virtual-staging/{房型}` | 5 | `/living-room`、`/bedroom`、`/kids-room` | 长尾避开头词 |
| **替代品页** `/alternatives/{竞品}` | 7 | magnific / remini / vanceai / photoroom / pixelcut | 蹭竞品品牌词 |
| 对比页 `/vs/{竞品}` | 4 | topaz-labs / remove-bg / lets-enhance | 同上 |
| 人群页 `/for/{人群}` | 3 | ecommerce / photographers / real-estate | 承接三条工作流 |

**几个具体做法值得直接抄:**

1. **免登录可用 + 水印限制**:`/free-virtual-staging` 不登录**每天可用 2 次、带水印**,
   注册送 25 积分换"无水印 + 全分辨率"。转化路径踩在产品价值上,不是登录墙。
   ✅ 这条同时满足 [Waffo KYB 的「产品可用无登录墙」要求](../sources/waffo.md)。
2. **免费档限长边 1200px**:不给输出加水印卖钱,而是**限分辨率**
   —— 对电商/房产买家(必须交高分辨率)是硬约束,对随手玩的人没影响。
   比我们 csv-to-qbo 定的"每月 3 次"更精准地把付费人群切了出来。
3. **合规当卖点**:虚拟布置输出**强制打 "Virtually Staged" 标**,并写明"listing compliance"。
   房产广告有披露要求 —— 把合规做成默认行为,同时是差异点。
4. **替代品页写法是「承认对手强」**:`/alternatives/photoroom` 里明写
   "When Photoroom is the better choice: …excellent for fast, template-driven…"。
   有对比表 + FAQ + Schema。**不是把对手写臭,是划边界。**
5. Schema 打满:`SoftwareApplication` / `AggregateOffer` / `FAQPage` / `HowTo` 全上,图片 alt 0 缺失。

**但要清醒:这套结构目前 0 自然流量。** 结构对不等于结构有效 —— 它只是把牌摆好了,牌还没开。

---

## 五、我能不能做:分三个问题回答

### ❌ 问题 1:能不能克隆整站(24 工具 all-in-one)

**不能,四条独立否决:**

1. **头词打不动**:`remove background` 月搜 430 万 / 难度 **93**;`ai image enhancer` 月搜 15.4 万 / 难度 **86**。
2. **零护城河**:上游全是开源模型 —— 与 [2026-08-27 image-to-3D NO-GO](../experiments.md) 完全同型
   (Hunyuan3D 开源 → 零护城河 + 正边际成本)。这次是 Real-ESRGAN / SAM / rembg / SDXL inpaint。
3. **正边际成本**:24 个工具全部走 GPU 推理,免费档 25 积分/月 × 用户数是真金白银的支出。
4. **它自己还没证明这条路走得通**。拿一个 DR 0、自然搜索 0 的站当对标,是把「摆好的牌」当成「赢了的牌」。

### ✅ 问题 2:能不能切单点 —— **`ghost mannequin` 是本会话第一个三门全过的候选**

| 门 | 判据 | 读数 | 过? |
|---|---|---|---|
| **CPC 分层** | 头词 CPC > $2 | 上限 **$7.74**,人工服务 $16–30/张 | ✅ |
| **不在被定价为 0 的层** | 市场有没有人在为它付钱 | BoxBrownie 等按张收费多年 | ✅ |
| **2 周内能验付费** | 有没有现成的收钱通道 | Fiverr 上 ghost mannequin 修图是成熟品类,可直接挂单测 | ✅ |

**可打性(gefei-kd,2026-08-26 缓存)**:难度 **26.8/100(容易)**、月搜 4,310、
进前十链接预算 **20–45 引用域**(目录型放大到 80–190)。

盘面里最硬的证据:**第 2 名 `adworker.ai` 域龄 6 个月、DR 3**,靠内页排到第 2,
体验分 62(停留 1分26秒)。gefei 模型原话:「不是蜜月期侥幸,而是新站正在赢下这个词」。
**门票是做出与它同等水平的产品,不是外链。**

对照 `stl repair`(最弱竞品 justfixstl.com 只用 10 个 dofollow 域排第 2)—— **同一个量级的门票。**
这是我们已经验证过能打的档位。

### ⚠️ 问题 3:`virtual staging` 呢 —— **需求最好,但不要正面打头词**

| 项 | 读数 |
|---|---|
| 月搜索量 | gefei 3,110 / SimilarWeb 6,070(**两源差 2 倍,取方向不取绝对值**) |
| 难度 | gefei **59.1** / SimilarWeb **75** —— 两源都说难 |
| CPC 上限 | **$11.93**,SERP 20.9% 是广告位 |
| 链接预算 | **85–190 引用域**(中值 120);目录型 **310–750** |
| SERP 结构 | 第 1 名 `virtualstagingai.app`(域名直拼 + DR 59 + 3.7 年 + 首页正面经营),
第 5 名 `boxbrownie.com`(DR 71),第 6 名 `play.google.com` |

**以我们当前 0 真外链 / 18h 周 → 头词不可打。**
但 EnhanceCraft 自己已经示范了绕法:`/virtual-staging/{房型}` 5 个长尾页。
房型词 + 风格词 + "virtual staging for {平台}" 是可打的口子。

**⛔ 但这不改变结论:即便打进去,买家是房产经纪,与 X / 独立开发圈完全不重叠。**
与 [csv-to-qbo 的圈层错配](../timeline.md) 同型问题。按 [2026-08-14 用户裁决](../timeline.md),
两条线并行不强制二选一,所以这不是否决,**是必须提前知道的分发代价:它只能靠 SEO / 冷启动,
Build in Public 带不动它。**

---

## 六、公理扫描

| # | 公理 | 判定 |
|---|---|---|
| 1 | 模式独立于人 | ✅ 无归因个人 |
| 2 | 模式决定道德 | ✅ 有合规披露标 |
| 3 | 智力不直接变现 | ✅ 有可执行结构 |
| 4 | **流量≠收入** | ⚠️ **3,548 访问 + 停留 28 秒 + 收款通道未检出,零收入证据。不可把它当赚钱案例** |
| 5 | **定价即产品** | ⚠️ **$9/$24/$59 档位健康(不踩低价陷阱),但单位价格 $0.18/张 vs 人工 $30/张,
自己在砸自己那层的定价** |
| 6 | 多数卡点是心理 | — |
| A | 形态决定复利 | ✅ 资产型 |
| B | **窗口期优先** | ⚠️ **只有 2 个月数据,窗口期未知。这是进行中的实验,不是结论** |
| C | 模式 vs 努力 | ⚠️ all-in-one 24 工具在零护城河品类里硬卷 |

**触发 4 条 ⚠️(公理 4 / 5 / B / C)。按 [axiom-scan SOP](../methods/axiom-scan.md),
≥2 条冲突 → 不作为可对标案例,但结构性观察保留。**

---

## 七、三条可复用的东西(与这个站的成败无关)

1. **同一个"AI 图像"品类里,CPC 差一个数量级 —— 分界线是买家拿它赚不赚钱。**
   `remove background` / `ai image enhancer`(C 端,CPC 低)vs `virtual staging` / `ghost mannequin`
   (房产经纪 / 电商卖家,CPC $7.7–11.9)。
   **→ 这是对 [risks.md「AI 品类 CPC 系统性低」](../risks.md) 的重要限定条件,已单独回写。**
2. **免费档限「分辨率」比限「次数」更精准切人群。** 电商/房产必须要高分辨率,随手玩的人不在意。
   我们 csv-to-qbo 定的"每月 3 次"可以照这个思路重想。
3. **用市场上的人工服务报价当定价锚**,而不是用同类 AI 工具的订阅价。
   BoxBrownie 那张价目表(enhancement $2 / day-to-dusk $5 / staging $30)本身就是一张
   **「哪一层被定价为 0」的现成地图**。任何做图像处理的方向都该先去看它。

---

## 八、下一步(如果要推进)

**不建议**再对这个站做任何补充调研 —— 它的数据已经拉到底了,再拉不会改变判断。

若要推进 `ghost mannequin`,按 [fast-payment-validation SOP](../methods/fast-payment-validation.md):

1. Fiverr 挂一个 ghost mannequin 修图服务(手工 + AI 辅助),定价 $3–5/张,看 14 天内有没有真实订单
2. 有单 → 说明付费意愿真,再决定要不要做成工具站
3. 无单 → 说明这个词的量在信息意图上,不在成交意图上,**直接停,不要建站**

**先测钱,再建站。** 这是四站 0 收入之后唯一该改的顺序。
