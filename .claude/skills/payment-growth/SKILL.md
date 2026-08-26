---
name: payment-growth
description: 从 Stripe / PayPal / Paddle / Lemon Squeezy 四个支付平台的完整导入引荐表,反推谁的钱已经在流过结账页——找正在起量的产品、判断哪个品类的付款意图在涨或在跌、估算候选产品的月收入区间。这是唯一「从钱倒推」而不是从搜索量正推的数据源。当用户说"谁在赚钱""什么产品在起量""这个赛道有人付费吗""哪个品类在涨""有没有新产品冒出来""找找机会""别人靠什么变现""这东西能不能赚到钱"时使用。也在选词/选方向卡在「有流量没收入」时主动建议。⛔ 查关键词搜索量/KD/词族不走这里,去 seo-competitor。
---

# 支付引荐发现:谁已经在收钱

**这个 skill 回答一个别的工具都回答不了的问题:钱正在流向谁。**

其余所有数据源(Semrush / gefei-kd / 哥伦布 / Trends)回答的是"这个词有多少人搜、多难打"。
本 skill 跳过整条推断链,直接观察**结账页收到的引荐流量**——一个域名出现在 Stripe 的引荐表里,
说明有真实的人从它那里走到了付款环节。

取数路径、字段含义、陷阱全在 [`memory/sources/payment-growth.md`](../../../memory/sources/payment-growth.md),
**本文件只定义顺序、阈值、裁决规则和退出条件**,不重复那些内容。

## 为什么需要它

[`keyword-hunt`](../keyword-hunt/SKILL.md) 已把瓶颈判定为**变现形态问题**:
四站 3 个月十几个词进 Top 10、31 点击、0 收入,工具站天然没有付款动作可挂。

`keyword-hunt` 的解法是从联盟变现载体倒推选词。本 skill 是**更靠前的一步**——
先看清楚"哪些形态的产品真的在收钱",再决定要不要做那个形态。

## Step 0 · 先答动作出口(不可跳过)

**这次查询的结果会落到哪个具体动作?** 答不上来就不要跑。

本 skill 比其他数据源更危险:一轮 `report` 吐出几十个"看起来很有机会"的域名,
看候选比做产品舒服得多。这是 [`axioms.md`](../../../memory/axioms.md) **公理 6** 最好的温床。

用户连续要求跑但说不出动作时,**主动追问一次:这是信息问题还是心理问题?**

## Step 1 · 采集(每月每平台独立全表)

```bash
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py collect --month <上月> --month <本月>
```

不传 `--target` = 四个平台全打。**必须看到每个快照都是 `complete: true`**,否则数据不可用——
半张表做出来的位次对比是错的,而且错得看不出来。

失败先怀疑限流(上游用 HTTP 200 + HTML 跳转页伪装成"登录过期"),等几分钟重跑,不要动凭证。

## Step 2 · 出机会清单

```bash
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py report --previous-month <上月> --current-month <本月> --limit 20
```

**只看两段,其余忽略**:

| 段 | 读什么 | 阈值 |
|---|---|---|
| `category_conclusions` | 哪个品类的付款意图在涨/在跌 | 看方向,不看绝对值 |
| `fast_rank_growth` | **表尾冲刺榜**,按 `rank_gain` 排序 | 位次增幅 ≥50 |

`new_product_growth` 作补充(找新面孔)。`traffic_gainers` / `newcomers` / `rank_risers` 是兼容用的旧口径,**不看**。

### ⚠️ 必须同时看第二张榜,否则会漏掉最大的鱼

**`rank_gain` 有结构性偏差,2026-08-26 首轮实战验证**:排序前 15 名的**上月起始位次全部落在 653–957**。
这不是巧合——`rank_gain` 的上限由起始位次决定,只有表尾条目才有空间产生 +600 的位移。
后果有两条:

1. 它**天然只筛得出"从表尾冲进中部"的小基数玩家**(引荐访问从 ~5000 涨到 ~2-3 万)
2. 它**结构性偏向大表**(Stripe 971 行 / PayPal 924 行)。LS 只有 254 行,物理上产生不了 +600

实例:`forgegui.com` 位次 41→16(仅 +25,进不了 rank_gain 前 15),但引荐访问
**114,316 → 264,309**——绝对量比榜上任何一个都大一个数量级,且它已经在全表前 20。

**所以 Step 2 必须跑两张榜**:

| 榜 | 怎么取 | 抓什么 |
|---|---|---|
| A 表尾冲刺 | `fast_rank_growth` 按 `rank_gain` | 从无到有的新玩家 |
| B **头部增长** | 从 `report` 里筛 **当前位次 ≤50** 且引荐访问增幅 ≥50% 的条目 | 已成规模、还在加速的 |

榜 B 没有现成字段,直接查 SQLite(`referral_rows` join `referral_snapshots`,比两个月的 `position` 与 `total_visits`)。
**两张榜合并去重后再进 Step 3。**

## Step 3 · 二次证据(两条并行)

```bash
# 整站流量趋势 —— 判"引荐涨是不是真的产品在长"
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py traffic-enrich --previous-month <上月> --current-month <本月> --start-month <6个月前> --end-month <本月> --limit 2000

# RDAP 域名年龄 —— 判"是不是新站"
python3 scripts/payment-growth/payment-growth-discovery/scripts/payment_growth.py enrich --previous-month <上月> --current-month <本月> --limit 20
```

⚠️ **`enrich` 不跑,`young_growth_candidates` 恒为 0**,不是"没有年轻站"。

裁决规则:

| 组合 | 判定 |
|---|---|
| 位次升 + 引荐涨 + 整站 `sustained_growth` | **强线索**,进 Step 4 |
| 位次升 + 整站 `declining` | **矛盾线索**,优先级下调 |
| 位次升 + 整站 `unavailable` | 站太小 SimilarWeb 没覆盖,**不等于 0**,靠人工判断 |
| 来自 PayPal 且无其他平台佐证 | **降级**,PayPal 混了大量消费端钱包活动 |

## Step 4 · 人工开站(不可跳过,优先级高于所有自动信号)

默认看 Step 3 筛出来的**前 10 个**,逐个开站确认:

- 产品是活的,不是停放页 / 模板站 / 空壳
- 首页说得清在卖什么
- **公开定价、计费周期、免费档、结账币种**
- 可见牵引力:客户数、评价、changelog、社区活跃
- ⚠️ **出站链接落在哪个路径**:必须是结账域(如 `<store>.lemonsqueezy.com`),
  而不是支付平台自己的营销页(如 `lemonsqueezy.com/wedges`)。**这一步不能省**——
  2026-08-26 首次实战即因此误判 `premiumpixels.com`(位次 198→9,实为 LS 联创的免费素材站,
  全站零商品)。详见 [`sources/payment-growth.md`](../../../memory/sources/payment-growth.md) 陷阱 3。

**快速排雷**:候选的引荐访问数若接近或超过它自己的整站总访问量,数据必有问题,直接剔除。

**人工判断压过 RDAP 域龄。** 域龄只作辅助证据。

## Step 5 · 估月收入(区间,不给单点数字)

只在开过站之后估。输出必须是区间 + 模型 + 假设 + 置信度:

| 收入模型 | 算法 |
|---|---|
| 订阅 | 估算付费用户数 × 月均单账户收入 |
| 一次性 | 估算月订单数 × 客单价 |
| 市场抽成 | 估算月 GMV × 抽成率 |
| 混合 | 分别算再求和 |

**绝不把引荐访问直接当成付款数。** 它只用来约束相对量级和方向。
非美元定价要标 `original_currency` + 汇率 + 汇率日期。

## Step 6 · 收敛与回写

**硬约束:一轮最多留 3-5 个标的,其余全部丢弃。不要建"待研究池"。**

| 拿到什么 | 写到哪 |
|---|---|
| 品类付款意图涨跌 | [`themes.md`](../../../memory/themes.md),标「SimilarWeb 引荐表 + 拉取日期」 |
| 值得跟进的产品(已开站 + 收入区间) | [`themes.md`](../../../memory/themes.md),过[五重过滤](../../../memory/methods/benchmark-five-filters.md) |
| 决定要打的方向 | 升级为 [`experiments.md`](../../../memory/experiments.md) 实验,带 GO/NO-GO |
| 新的骗局/刷量模式 | [`risks.md`](../../../memory/risks.md) |

**不回流 `principles.md`** —— 与 `/signals` 同规则,方法论只从自有实践和 findings 沉淀。

## 信任等级

**第三方估算**。落盘必标工具名 + 拉取日期。与 [`seo-data`](../seo-data/SKILL.md) 的 GSC 冲突时**一律以 GSC 为准**。

三条不可越界:引荐访问 ≠ 成功付款;PayPal 表最脏;RDAP 注册时间 ≠ 上线时间、≠ 运营方身份。

## 与其他 skill 的分工

| 问题 | 用谁 |
|---|---|
| **谁已经在收钱、什么形态在收钱** | **本 skill** |
| 新站该选哪个词才能出单 | [`keyword-hunt`](../keyword-hunt/SKILL.md) |
| 这个词多大 / 多难 / 词族多广 | [`seo-competitor`](../seo-competitor/SKILL.md) |
| 竞品的流量渠道构成 | [`seo-competitor`](../seo-competitor/SKILL.md) 的 ego 路径(本 skill 该接口 502) |
| 我自己的站表现如何 | [`seo-data`](../seo-data/SKILL.md) —— 唯一真值 |
| 该怎么打(策略判断) | [`seo-advisor`](../seo-advisor/SKILL.md) —— 他人观点,须过公理扫描 |
