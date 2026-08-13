---
name: seo-advisor
description: 向哥飞 SEO Agent(seo.web.cafe)提问并**辩证评估**其回答——SEO 策略、外链打法、选词判断、站点诊断、变现路径。当用户说"问问哥飞""问一下那个 SEO agent""哥飞怎么说""让顾问看看""外部意见"时使用。也在自己给不出高置信度判断、需要第二意见时主动建议使用。**关键约束:该 agent 的输出是他人观点,不是数据,禁止直接落 memory,必须先过公理扫描。**
---

# 外部顾问:哥飞 SEO Agent

**信任等级:他人观点。** 这是本项目里唯一一个**默认不可信**的信息源——不是说它错,
而是它的输出性质是判断而非事实,必须经过与 findings / signals 同级的甄别流程才能进入记忆。

底层模型是 `deepseek-v4-flash`(页面上可见,可切),**不是强推理模型**。
它的价值在于覆盖面和 SEO 领域语料,不在于推理深度。据此调整期望。

## 入口(实测于 2026-08-09)

`https://seo.web.cafe/chat/`(登录态已在 ego 里)

- 输入框:`textarea#q`
- **发送:文本为「发送」的按钮。⛔ 不是 `⏎`** —— 页面明写「Enter 换行,点『发送』或 Ctrl+Enter 提交」。
  点 `⏎` 不会提交,而且**不报错**,只会静默什么都不发生(第一次试就踩了这个坑,查配额没扣才发现)
- 新开对话:`＋ 新对话` 按钮
- 历史检索:`input#convSearch`
- 同站工具:`/kd/` 关键词难度、`/worth/` 网站估值

**计费**:VIP 每日 500 积分。每条消息 2 分 + 每次工具查询 1 分 + 长答复加价。
实测一个带数据的复杂问题(它自动跑了 8 次工具查询 + 知识库检索)**消耗 41 积分**。
提问前后可从 `innerText` 里读 `今日已用 N/500` 核对。

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('seo advisor')
await openOrReuseTab('https://seo.web.cafe/chat/', { wait: true, timeout: 60 })
await wait(6)
await js(`[...document.querySelectorAll('button')].find(b=>b.textContent.trim().startsWith('＋'))?.click(); return 1;`)
await wait(3)
await fillInput('textarea#q', '<问题>')
await wait(1)
await js(`[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='发送')?.click(); return 1;`)

// 结束判定:轮询 innerText 长度,连续 3 次不变即认为生成完成
let prev=0, stable=0
for (let i=0;i<36;i++){
  await wait(5)
  const n = Number(await js(`return document.body.innerText.length;`))
  if(n===prev){ stable++; if(stable>=3) break } else { stable=0; prev=n }
}
cliLog(await js(`return document.body.innerText.slice(-4000);`))
EOF
```

要点:
- **提交成功的判据**:`textarea#q` 被清空 + 「发送」按钮消失。别只看正文长度
- 复杂问题它会先输出「已完成:xxx」的工具调用清单再给结论,**中途文本会长时间不变**,
  所以 stable 阈值不能设太低(3 次 × 5 秒 = 15 秒),总轮询窗口留够 3 分钟
- 回答很长时用 `innerText.slice(-4000)` 取尾部;左侧历史列表会混进 `innerText`,按问题原文定位起点

**先搜历史再提问**:用 `input#convSearch` 查同类问题是否已问过。已有大量历史对话,
其中包含对自有站的诊断(`partfit3d` / `aidepixelate` 都问过),**不要重复消耗积分**。

## 提问原则

- **一次一个具体问题**,带上真实数据。"partfit3d 三个月 833 曝光 5 点击,主词 `split 3mf` 排 9.8 位,
  下一步该扩词族还是修转化?" 远好于 "帮我分析这个站"。
- **把 GSC 实测数据贴进去**——它看不到你的后台,不给数据它只能给通用答案。
- **不要问它做决定**,问它提供你没想到的选项和反面证据。决定权在用户和本项目的公理体系。

## 收到回答后:强制辩证流程(不可跳过)

### Step 1 · 公理扫描

按 [`methods/axiom-scan.md`](../../../memory/methods/axiom-scan.md) 9 条逐项过。SEO 建议高频触发这几条:

| 公理 | 在 SEO 建议里的典型形态 |
|---|---|
| **公理 3**(智力不直接变现) | 只给"要提升权重""要做好内容"这类框架,没有可执行步骤 → 价值接近 0 |
| **公理 4**(流量≠收入) | 用排名/流量指标替代收入指标,不谈变现闭环 |
| **准公理 B**(窗口期优先) | **SEO 领域过期最快**——引用的打法是哪年的?平台规则变了吗?算法更新后还成立吗? |
| **公理 1**(模式独立于人) | 是否回避 input 要求(需要多少时间/预算/外链资源)? |

触发 ≥2 条 → 判定为不可用建议,**不写 advice 文件**,只在对话里告知用户为什么否掉。

### Step 2 · 与自有数据对质

**建议与 GSC 实测冲突时,以 GSC 为准。** 例如它说"这个词有量、值得做",而 GSC 显示该词族
3 个月 833 曝光——以实测为准,并把这个冲突本身记下来,它比建议更有信息量。

### Step 3 · 与既有记忆对质

- 与 [`principles.md`](../../../memory/principles.md) 冲突 → 是建议错了,还是原则该更新?**明确选一个**,不要含糊带过。
- 命中 [`risks.md`](../../../memory/risks.md) 已知模式 → 直接标注并降权。
- 与 [`profile.md`](../../../memory/profile.md) 硬约束冲突(18h/周、1 万预算、无 Stripe)→ 不可执行,否掉。

### Step 4 · 落盘

通过前三步才写 `memory/advice/YYYY-MM-DD-<slug>.md`:

```markdown
# <一句话问题>

> 咨询时间:YYYY-MM-DD (UTC+8) · 来源:哥飞 SEO Agent (deepseek-v4-flash)
> **性质:他人观点,非数据。**

## 1. 原始建议
要点式,≤5 条。不复述全文。

## 2. 公理扫描与辩证
逐条列触发的公理及理由;与 GSC 实测 / principles / risks 的冲突点。
没有冲突也要明确写「无冲突」,不要省略。

## 3. 采纳判定
**判定**:采纳 / 部分采纳 / 不采纳

采纳的部分 → 落到哪个具体动作(必须能指向 todos 或 experiments 的一条)。
不采纳的部分 → 为什么。
```

登记到 `memory/advice/_processed.md`(问题摘要 / 日期 / 判定 / 链接)。

**回流限制**(与 `/signals` 同规则):
- 可回流 [`themes.md`](../../../memory/themes.md)、[`risks.md`](../../../memory/risks.md)、[`connections.md`](../../../memory/connections.md)
- **不可回流 [`principles.md`](../../../memory/principles.md)** —— 方法论从自有实践和 findings 沉淀,顾问观点不够格

## 实测到的质量特征(2026-08-09,首次真实提问)

比预期好,但有一个稳定盲区:

- ✅ **会自己调工具**,不是纯语言模型输出——一个问题触发了 8 次实时查询(域名概况 / 4 个词的 KD / 3 次知识库检索)+ 域名可用性查询
- ✅ **主动给 input 要求**(外链需 55-120 个引用域、域名成本),没有回避成本
- ✅ **主动给窗口期信号**(竞品域名 26 天前刚注册)
- ✅ **给可执行步骤**,不是空框架
- ⚠️ ~~**稳定盲区:公理 4(流量≠收入)**~~ → **2026-08-11 修正:不是稳定盲区,取决于你问不问。**
  首次(08-09)整篇只谈流量排名;但 08-11 那次**在问题里显式加了「这类流量能不能支撑订阅制」**之后,
  它给出了三个回答里最扎实的一段:主动拆停留时长/页均/跳出率、指出产品-流量错配、
  用 CPC 反推付费意愿、引用"看出站有没有 Stripe 判断赚钱"。
  **→ 结论:它不会主动谈变现,但问了就会认真答。把变现问题写进提问里,不要事后自己补。**
- ⚠️ **真正的稳定盲区是准公理 B(窗口期)的样本污染**。2026-08-11 它用三个 Omegle 替代站
  (DR 2.6 做出 603 万访问)论证"低 DR 也能打赢品牌词",而 Omegle 已于 2023-11 关站——
  **它检索到的是历史快照,不会去查那个词的官网还在不在**。
  **→ 收到任何"低权重站逆袭"样本,先自查主攻词的官网状态。** 见
  [`risks.md` 平台猝死遗产词](../../../memory/risks.md)。
- ⚠️ **它的数字与 Semrush 差很多**(同词量差 5.5x、难度差 2.5x)。两个都是估算,
  **不要因为它"跑了实时工具"就当成真值**

**喂数据能显著提升回答质量**:带上 GSC 实测数字提问,拿到的是针对性诊断;
不带数据就只能得到通用答案(历史对话里"帮我分析这个站"那类问题的回答明显更空)。

## 什么时候不该用

- 用户已经有 GSC 实测数据能回答的问题 → 用 [`seo-data`](../seo-data/SKILL.md),不要问顾问
- 用户在纠结要不要行动而非缺信息 → 这是心理卡点(公理 6),再问一个顾问只会延长拖延
- 决策已经做过、只是想找人背书 → 直说,不要陪着找
