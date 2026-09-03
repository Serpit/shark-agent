# 数据源:支付平台引荐流量(SimilarWeb API 直连)

> **定位**:从 Stripe / PayPal / Paddle / Lemon Squeezy 四个支付平台的**完整导入引荐表**,
> 反推**谁的钱已经在流过结账页**——出现在那张表里,说明它真有人在付款。
>
> 这是本项目里**唯一一个"从钱倒推",而不是从搜索量正推**的数据源。
> 其余所有工具(Semrush / 哥飞 / 哥伦布 / Trends)回答的都是"这个词有多少人搜、多难打";
> 只有它回答"**谁已经收到钱了**"。
>
> **不是**关键词工具:不给词族、不给 SERP 排名。那些仍归 [`seo-competitor`](../../.claude/skills/seo-competitor/SKILL.md)。

## 为什么引进(2026-08-26)

四站上线 3 个月、十几个词进 Top 10、总计 31 点击、**0 收入**。
[`keyword-hunt`](../../.claude/skills/keyword-hunt/SKILL.md) 已判定瓶颈从流量换位到变现,
且"工具站天然没有付款动作可挂"是**形态问题不是优化问题**。

这个源的价值就在这一点上:它跳过"选词 → 建站 → 排名 → 也许有钱"这条长链,
直接观察链路末端**已经在发生的付款行为**,再往回找是什么产品、什么形态、卖多少钱。

## 接入方式

代码在仓库内:`scripts/payment-growth/`,两层结构。

| 层 | 路径 | 职责 |
|---|---|---|
| 数据客户端 | `scripts/payment-growth/similarweb/scripts/similarweb_client.py` | 登录 + token 缓存 + 所有 SimilarWeb 接口 |
| 业务层 | `scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py` | 采集 / 对比 / 富化 / 出机会清单 |

> ⚠️ **这是本仓库唯一有 pip 依赖的脚本**(`requests` + `python-dotenv`),
> 是 CLAUDE.md「`scripts/` 一律零依赖纯 stdlib」的**明文例外**。
> 5500 行 vendored 代码,改写成 stdlib 不划算。两个依赖本机已装,不需要 venv。

**凭证**:`~/.config/shark-agent/.env`(仓库外,`chmod 600`),键名 `SIMILARWEB_USERNAME` / `SIMILARWEB_PASSWORD`。
`SIMILARWEB_TOKEN` 留空——**它只是账号登录失败或撞登录次数上限时的兜底**,正常路径用不到。

服务端:`dash.3ue.com` 认证 + `sim.3ue.com` 取数,账号 `serpit`(与 ego 面板同一个账号)。
`.com` 与 `.co` 是同一账号体系,**两边都能登**,不必改域名。

## 核心命令

```bash
# 0. 验证凭证(换机后先跑这个)
python3 scripts/payment-growth/similarweb/scripts/similarweb_client.py login

# 1. 采集:每个平台每个月独立拉全表
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py collect --month 2026-06 --month 2026-07

# 2. 出机会清单
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py report --previous-month 2026-06 --current-month 2026-07 --limit 20

# 3. 整站流量二次验证(给候选加第二层证据)
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py traffic-enrich --previous-month 2026-06 --current-month 2026-07 --start-month 2026-02 --end-month 2026-07 --limit 2000

# 4. RDAP 域名年龄(判"是不是新站")
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py enrich --previous-month 2026-06 --current-month 2026-07 --limit 20
```

不传 `--target` 时默认四个平台全打。`rolling-report` / `rolling-enrich` 做 3 个月以上滚动,
**要求区间内每个平台每个月都有 `complete=true` 的快照**,缺一个月直接报错而不是静默降级。

快照落 `scripts/payment-growth/payment-growth-discovery/state/payment_growth.sqlite3`(已 gitignore)。

## 输出字段与读法

`report` 出两类结论,**不要混为一谈**:

| 段 | 是什么 | 怎么用 |
|---|---|---|
| `category_conclusions.gainers/.decliners` | 名义上是品类级支付意图涨跌 | ⛔ **不看**——2026-08-28 实测是单站伪装成品类,见[陷阱 6](#6-category_conclusions-是单站伪装成品类不要当赛道信号读2026-08-28-实测) |
| `fast_rank_growth` | **表尾冲刺榜**。位次上升的产品,按位次增幅排序,不设流量下限 | 看,但**必须配「头部增长榜」**,见陷阱 5 |
| `new_product_growth` | 上月不在表里、本月出现的产品 | 找新面孔 |
| `traffic_gainers` / `newcomers` / `rank_risers` | 兼容用的旧口径列表 | 一般不看 |
| `young_growth_candidates` | 上面几类里 RDAP 域龄 ≤730 天的 | **必须先跑 `enrich`,否则恒为 0** |

**为什么要看位次**:位次上升不受基数影响。一个从 13 访问涨到 1303 的站,绝对量仍然很小,
但它在全表里从第 236 位冲到第 22 位——这个位移比"涨了 1290 次访问"更有意义。

**但位次不能单独用**:`rank_gain` 的上限由起始位次决定,已在头部的大玩家永远上不了这张榜。
两张榜一起看才完整,见[陷阱 5](#5-fast_rank_growth-有结构性偏差会漏掉最大的鱼)。

`website_traffic.trend` 是第二层证据,取值 `sustained_growth` / `sustained_decline` / `growing` /
`declining` / `insufficient_data` / `unavailable`。**缺月永远是 `unavailable`,不会被当成 0**。

判读优先级:**位次升 + 引荐访问涨 + 整站流量 `sustained_growth`** 三项齐了才值得开站细看;
只有位次升而整站流量在跌,是**矛盾线索**,优先级下调。

## 信任等级

**第三方估算**,与 Semrush / SimilarWeb / 哥伦布 / gefei-kd 同层。
落盘必须标「SimilarWeb 引荐表 + 拉取日期」,与 GSC 冲突时**一律以 GSC 为准**。

三条口径红线:

1. **引荐访问 ≠ 成功付款**。它只是"有人从这个站点走到了结账页",可能付了也可能没付。只取相对量级和方向。
2. **PayPal 的表最脏**。它混了大量消费端钱包活动,不只是商家结账。PayPal 来的候选要更严的产品与结账证据。
3. **RDAP 注册时间 ≠ 上线时间**。它描述的是当前注册对象,不能证明首次注册、不能推断运营方身份。

## ⚠️ 已知陷阱

### 1. 限流会伪装成「登录过期」——最容易误判的一条

批量任务失败时,上游返回的**不是错误码,是 HTTP 200 加一个 HTML 跳转页**:

```
location.href = 'https://dash.3ue.com?msg=登录过期或无效,请重新登录'
```

`sim.3ue.com` 是转售代理,被限流时就吐这个页面冒充登录失效。
**看到"莫名其妙失败"先怀疑限流,不要去重配凭证。** 实测同一条请求可以先 8/8 全败、隔几分钟再 3/3 全成。
`traffic-enrich` 已内置 3 次退避重试(3s / 6s),仍失败就是真的被限了,等一会儿再跑。

### 2. 两个接口是死的,改不了

| 接口 | 状态 | 影响 |
|---|---|---|
| `fetch-website-analysis-bundle` | 稳定 **502** | **流量渠道构成拿不到** —— 这一项仍须走 ego 网页版 |
| `fetch-search-landing-pages-overview-query` | 稳定 **400** | 无影响,`fetch-landing-pages-query` 覆盖同类数据且更细 |

502 是网关错误,通常意味着服务商没买这个模块或已下线。**真正丢失的能力只有「渠道构成」一项。**

### 3. 引荐表混了「结账流量」和「平台自家营销页流量」——首次实战即踩(2026-08-26)

`lemonsqueezy.com` 这张表里,既有真结账(`<store>.lemonsqueezy.com`),
也有 Lemon Squeezy **自己官网营销页**的导流(`lemonsqueezy.com/wedges`、`/pricing` 等)。
两者在表里长得一模一样,但后者**跟付款毫无关系**。

实例:`premiumpixels.com` 位次 198→9(+189),看起来是最强线索之一。
实际它是 LS 联合创始人 Orman Clark 的个人免费素材站,全站无任何自有商品,
`/pricing` 和 `/shop` 均 404,唯一 CTA 指向 LS 官网的免费 Figma 资源页。**纯假阳性。**

**判据**:候选站的引荐访问数如果**接近或超过它自己的整站总访问量**,基本可以判定数据有问题
(premiumpixels:引荐 1985 vs 整站 2.2K,物理上不成立)。

**SOP 补丁**:Step 4 人工开站时,**必须确认它的出站链接落在结账路径而不是营销页**,
否则位次再漂亮也要剔除。这一步不能省。

### 4. `traffic-enrich` 不能一次跑大 `--limit`

它把所有结果**攒在内存里、最后才落库**——中途任何一次 403/限流失败,
**整批 0 行持久化**,前面拉到的全白费。2026-08-26 实战 `--limit 2000` 首批即挂。

**正确做法**:按 10 个域名一块分批跑,失败重试。分块后 10/10 全成。

### 5. `fast_rank_growth` 有结构性偏差,会漏掉最大的鱼

`rank_gain` 的上限由起始位次决定,所以这张榜**只筛得出"从表尾冲进中部"的小基数玩家**,
且**偏向大表**(Stripe 971 行能产生 +700,LS 254 行物理上不可能)。

2026-08-26 实证:排序前 15 名的上月起始位次**全部落在 653–957**。
而 `forgegui.com` 位次 41→16(仅 +25,上不了榜)、引荐访问 114,316 → 264,309,
绝对量比榜上任何一个都大一个数量级。

**必须补一张「头部增长榜」**:当前位次 ≤50 且引荐访问增幅 ≥50%,直接查 SQLite。
详见 [skill Step 2](../../.claude/skills/payment-growth/SKILL.md)。

### 6. `category_conclusions` 是「单站伪装成品类」——不要当赛道信号读(2026-08-28 实测)

2026-08-28 对 Stripe 表 06→07 逐品类拆解,**7 个涨榜品类 + 7 个跌榜品类,全部由单站贡献 76–124% 的变化量**:

| 品类 | 表面结论 | 实际 |
|---|---|---|
| 电脑/电子/科技 +37.8% | "AI 付款意图在加速" | `higgsfield.ai` 一家占 **81%** |
| 音乐 +122.9% | "音乐付款在涨" | `dearkellyfilm.com` 一家占 **105%**(其余全在跌) |
| 影视/流媒体 +127.0% | 同上 | `covergirl.maxim.com` 占 **104%** |
| 邮件 +50.6% | — | `my.brain.fm` 占 **79%**(而且它是助眠音频,不是邮件) |
| 体育 +49.9% | — | `arenaclub.com` 占 **76%** |
| 金融/投资 -24.3% | "投资付款意图在退潮" | `portal.nousresearch.com` 一家占 **111%** |
| 电脑硬件 -75.6% | — | 该品类**全表只有 1 个域名**(`console.sakana.ai`) |

两个独立成因,都不可修:

1. **样本量太小**:多数品类在全表 968 行里只占 1–30 行,单站波动直接淹没品类信号。
2. **SimilarWeb 的分类标签本身大量错标**:`app.kiro.dev`(AI IDE)标 Banking、`my.brain.fm`(助眠音频)标 Email、
   `console.sakana.ai`(AI 实验室)标 Computer Hardware、`pslscale.com`(面部评分)标 Video Games、
   `g.alipayplus.com`(支付)标 Beauty_and_Cosmetics。**错标 + 小样本叠加,品类聚合没有意义。**

**处置**:`category_conclusions` 从「Step 2 必看两段之一」**降级为不看**。
真要判品类冷热,只能人工归类前 50 行再聚合,而不是用它自带的 `category` 字段。

> ⚠️ 这条**推翻了 2026-08-26 首轮落在 [`themes.md`](../themes.md) 的品类结论**
> (「AI 工具付款意图 +37.9%,与『AI 已经卷完了』相反」)——那 37.9% 是 higgsfield 一家。已在 themes 就地更正。

### 7. `complete=true` 是硬门槛,别绕过

采集器只在上游明确报全表拉完时才存快照,拉不全就报错而不是存半张表。
**不要为了省事去改这个逻辑**——半张表做出来的位次对比是错的,而且错得看不出来。

### 8. 密码走 URL query

登录是 `GET /api/account/login?username=...&password=...`(`similarweb_client.py:1679`)。
上游设计如此,改不了。**别用在别处复用的重要密码。**

### 9. 本地打过 3 个补丁,换版本要重打

vendored 代码,升级或重新解包时以下改动会丢:

| 位置 | 改了什么 | 为什么 |
|---|---|---|
| `payment_growth.py` `_normalize_fractional_seconds` | 小数秒补齐到 6 位 | Python 3.9 的 `fromisoformat` 只吃 3/6 位,RDAP 返回 `.71` / `.0` 会崩。**症状很阴险**:`report` 一开始能跑,一旦 `enrich` 往缓存里写进这种时间戳就开始崩 |
| `payment_growth.py` `MAX_TRAFFIC_TREND_BATCH` | 10 → 5,并加 3 次退避重试 | 见陷阱 1 |
| `shared/env_loader.py` | 候选链加 `~/.config/shark-agent/.env` | 对齐仓库凭证纪律 |

本机只有 Xcode 自带的 **Python 3.9.6**,没有 3.11+。若将来换 3.11+,第一个补丁可以撤。

## 与其他数据源的分工

| 问题 | 用谁 |
|---|---|
| **谁已经在收钱** | **本源** —— 唯一能回答的 |
| 哪个品类的付款意图在涨/在跌 | **本源** `category_conclusions` |
| 这个候选站有多大、在涨还是在死 | **本源** `traffic-enrich`(SimilarWeb 整站流量) |
| 这个站是不是新站 | **本源** `enrich`(RDAP) |
| 这个词多大 / CPC 多少 / 词族有哪些 | Semrush([`seo-competitor`](../../.claude/skills/seo-competitor/SKILL.md)) |
| 这个词多难打 / 要多少外链 | [gefei-kd](gefei-kd.md) |
| 这个 AI 品类谁在做 | [哥伦布](columbus.md) |
| 竞品的流量渠道构成 | **仍走 ego 网页版** —— 本源该接口 502 |
| 我自己的站表现如何 | GSC([`seo-data`](../../.claude/skills/seo-data/SKILL.md))—— **唯一真值** |

## 使用前提

拉数前先答一句:**这次查询的结果会落到哪个具体动作?**

本源尤其危险——它一次能吐出几十个"看起来很有机会"的域名,
是 [`axioms.md`](../axioms.md) **公理 6**(多数卡点是心理问题)最好的温床:
看候选比做产品舒服得多。

**硬约束**:一轮 `report` 之后**最多留 3-5 个标的**往下走,其余全部丢弃,不要建"待研究池"。
判断依据以人工开站为准,RDAP 域龄只作辅助。

## 结果往哪写

| 拿到什么 | 回写位置 |
|---|---|
| 某个品类的付款意图在涨/在跌 | [`themes.md`](../themes.md),标「SimilarWeb 引荐表 + 拉取日期」 |
| 值得跟进的具体产品(已开站验证 + 收入区间估算) | [`themes.md`](../themes.md),过[五重过滤](../methods/benchmark-five-filters.md) |
| 决定要打的方向 | 升级为 [`experiments.md`](../experiments.md) 实验,带 GO/NO-GO 条件 |
| 新发现的骗局/刷量模式 | [`risks.md`](../risks.md) |

**不回流 `principles.md`** —— 方法论只从自有实践和 findings 沉淀,机会情报不算。
