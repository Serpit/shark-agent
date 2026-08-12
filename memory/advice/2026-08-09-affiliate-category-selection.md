# 做联盟内容站该选哪个品类,以及 AI 小说写作词族的可打性

> 咨询时间:2026-08-09 (UTC+8) · 来源:哥飞 SEO Agent (deepseek-v4-flash) · 两轮,合计消耗约 118 积分
> **性质:他人观点,非数据。**
> 产生场景:`keyword-hunt` 流水线 Step 1 与 Step 5,一轮流水线合并为本文件。

## 1. 原始建议

### 第一轮(Step 1 · 品类候选)

1. **主推 AI 写作工具**:称 `best ai writing tools` KD **28.5**「容易」、需 25-50 引用域,SERP 第 1 名是 reddit 帖=内容真空,G2/Capterra/TechRadar 未出现。
2. **第二梯队网站托管 / 邮件营销**:泛词红海(`best web hosting for small business` KD 48.3、`email marketing software` KD 49.6),但地域/comparator 长尾 KD 12-25 是蓝海。
3. **明确否掉 VPN / CRM**:`best vpn` KD 62.3、`best crm for small business` KD 59.8,DR 0 拿不到。
4. **佣金数据自己承认没核实到** —— 工具调用到上限,Jasper/Hostinger/Kit 的官方佣金率与 cookie 一个都没查证,唯一有实证的是社群内产品 Pollo.ai(30% recurring + 二次分销)。
5. 附带方法:用 `rel="sponsored"` 标联盟链接;用 Stripe Partners 目录 + SimilarWeb 子域名反查「谁在赚佣金」。

### 第二轮(Step 5 · 外链预算与窗口期)

**回答被工具调用上限截断,没有产出完整结论**,但中间进度里漏出四个可用数字:

6. `sudowrite alternatives` **链接预算中值仅 25 个引用域**
7. AI 小说词族 Top 10 里**有 DR 2~6 的站**
8. 10 个候选 EMD 域名**全部可注册**(无人布局)
9. 它跑了 `Stripe 收银台引荐:sudowrite.com`,但结论未输出

## 2. 公理扫描与辩证

### ⚠️ 公理 4 部分冲突(第一轮)

我在提问里把「佣金结构」写死为必答项,它仍然把 KD 数据当主体交付,**变现闸门一个都没验**。这印证了 [`seo-advisor`](../../.claude/skills/seo-advisor/SKILL.md) 记录的结构性盲区:它的工具箱全在流量侧。四个联盟计划的 5 个字段全部由本项目自行核实(见下)。

### ⚠️ 与 Semrush 实测冲突:KD 差 1.6 倍

| 词 | 哥飞口径 | Semrush 口径(2026-08-09,美区) |
|---|---|---|
| `best ai writing tools` | KD **28.5**「容易」 | KD **45**、1.3K/月、CPC $3.63、Com 0.67 |

按 Semrush,它的首选推荐**直接死在 `keyword-hunt` Step 3 的 KD<25 门槛上**。这是本项目第二次记录到两源打架(第一次是 `3mf to stl`,量差 5.5x、难度差 2.5x,见 [experiments.md](../experiments.md))。**结论不变:两个都是估算,只取排序不取绝对值。**

### ⚠️ 与自有 SERP 实测冲突:最关键的一条

它说 AI 写作 / 邮件营销 / 托管的 alternatives 与 comparator 长尾是「蓝海」。本项目对 6 个词做了 Top 10 出站链接实扫,发现:

**这些词的 SERP 被竞品厂商的内容营销占据,不是被联盟站占据。** 联盟链接数量:`surfer seo alternatives` 0、`convertkit alternatives` 1、`convertkit vs mailchimp` 0、`best email marketing software for small business` 0、`best ai tool for proposal writing` 0。

「KD 低 = 蓝海」在这里不成立 —— KD 量的是外链门槛,量不到**厂商内容团队的持续投入**。已沉淀为 [risks.md 新条目](../risks.md#成熟-saas-品类的-alternatives--vs-词被厂商内容营销占据不是联盟站的地盘)。

### ⚡ 命中 risks.md「热词窗口幸存者偏差」

第一轮的候选品类 4 是哥飞社群自己生态里的 Pollo.ai,案例来自 2025-03「新词新站比赛」,群友佣金截图作背书。**利益相关 + 幸存者偏差双重问题**,直接降权,不进候选池。

### ⚠️ 「库内蓝海词」大概率是零量合成词

它给的 `ai writing tool comparator`、`email marketing tool comparator`、`cold email automation free`(KD 6.9-15.7)—— `comparator` 不是英语母语者的自然搜索用词。它自己也补了一句「KD 合适但搜索量为 0 的词不值得做」。**不采纳,不进候选池。**

### ✅ 公理 1 无冲突

两轮都主动给了 input 要求(25-50 引用域 / 15-35 / 25),没有回避成本。第二轮的 25 引用域是本轮唯一被采纳的核心数字。

### ⚡ 准公理 B:窗口期信号双刃

「10 个 EMD 域名全部可注册,无人布局」既可读作窗口期开着,也可读作**没人觉得这个盘子值得做**(词族单词月量仅 50-260)。不作为 GO 依据,只作为「不是红海」的旁证。

## 3. 采纳判定

**判定:部分采纳**

### 采纳

| 采纳内容 | 落到哪个动作 |
|---|---|
| `sudowrite alternatives` 链接预算中值 **25 个引用域** | 通过 [`keyword-hunt`](../../.claude/skills/keyword-hunt/SKILL.md) Step 5「引用域 > 30 直接 pass」的硬否决,是本轮唯一过线的方向 → [experiments.md AI 小说写作联盟词族](../experiments.md) |
| novel 词族 Top 10 有 **DR 2~6 的站** | 与自测 `thewritingasylum.com`(AS 8 / 引用域 135 / 流量 331)相互印证,DR 0 新站有位置 |
| 联盟链接要加 `rel="sponsored"` | 写入 Step 6 建页动作 |
| 用 Stripe Partners 目录 + SimilarWeb 反查「谁在赚佣金」 | 方法本身可用,但本轮改用更直接的 **SERP 出站链接实扫**,效果更好,已内化为 Step 4 做法 |

### 不采纳

| 不采纳内容 | 理由 |
|---|---|
| **主推 AI 写作工具泛词** | Semrush KD 45 ≠ 它说的 28.5,超 Step 3 门槛;且 SERP 实扫显示赚钱的是 Substack/Medium 页面而非独立站 |
| **网站托管品类** | Hostinger 联盟申请要求「博客/社媒有 IT 主题 + 至少 1000 流量」,当前 4 站 90 天 31 点击过不了审;泛词被 CNET(DR 91)/Forbes(DR 94) 占死 |
| **邮件营销 alternatives / comparator 词** | SERP 实扫 0-1 条联盟链接,被 sender.net / beehiiv / brevo / selzy 等厂商官方站占据 |
| **候选品类 4(Pollo.ai / AI 工具泛品类)** | 利益相关 + 幸存者偏差,命中 risks.md 已知模式 |
| **全部「库内蓝海词」** | `comparator` 类合成词,大概率零搜索量 |

### 本项目自行核实的联盟条款(哥飞未提供,补齐 Step 1 五字段)

| 产品 | 佣金 | Recurring | Cookie | 允许 SEO 引流 | 打款/起付 |
|---|---|---|---|---|---|
| Kit(原 ConvertKit) | 50% 前 12 个月,之后 10/15/20% 永久 | ✅ | 未公开 | ✅ 鼓励自然流量 | 未公开 |
| Surfer SEO | 月付首笔 75%(可到 125%);年付 15-25% | ❌ | 90 天 | ✅ | PartnerStack,**$5** |
| Jasper | 25% recurring 12 个月(100 单后 30%) | ✅ | 45 天 | ✅ | PayPal,$25 |
| Hostinger | 40% 起,阶梯上浮 | ❌ | 30 天 | ⚠️ 申请门槛 1000 流量 | PayPal $100 / 电汇 $500 |
| **Sudowrite** | **25% recurring 12 个月** | ✅ | 30 天(Rewardful) | ✅ | PayPal 月结,**60 天持有期** |
| **Squibler** | 20% | 部分 | 未公开 | ✅ | Wise,**起付 $100** |

> 前四个来自 Step 1,后两个是 Step 4 实扫出赚钱路径后补验的,是本轮真正入选的载体。
