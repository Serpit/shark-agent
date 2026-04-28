# shark-agent

帮助从「生财有术」社群文章和风向标里提炼出有价值信息的私人 agent。

输入是社群里的文章原文与圈友风向标,输出是一份**结构化记忆**——所有判断、方向、风险、人脉线索都沉淀在项目目录内,跟着项目走。

agent 协议入口:[`CLAUDE.md`](CLAUDE.md)(Claude Code) / [`AGENTS.md`](AGENTS.md)(Codex 等),两份内容等价。

## 使用方式

agent 接收三类输入,分别对应不同的处理路径:

### 1. 摄入文章(自然语言触发)

把文章先存到 `raw/` 目录(可以是 markdown、URL 转存的 docx 内容、纯文本等),然后跟 agent 说:

```
摄入 raw/<文件名>
```

或者更宽泛地:「分析这批文章」、「处理一下 raw 里新加的几篇」。

agent 会:
1. 算 sha256 查重(`memory/findings/_processed.md`),已处理过的直接跳过
2. 按 `memory/profile.md` 的权重判断**保留 / 丢弃 / 标记风险**
3. 保留的产出三段式 finding(价值标签 / 核心 SOP 或原理 / 风险提示)
4. 回流到聚合视图(themes、principles、connections、risks)
5. 登记到 `_processed.md`

### 2. 评估风向标(`/signals`)

风向标是社群圈友的「最新发现/机会洞察」,通常一两段话,真伪混杂。直接把内容贴进命令:

```
/signals 听说东南亚某平台正在补贴新店家入驻,首月 0 抽成......
```

agent 会从三个角度做客观评估:
- **适配度** —— 对照 `profile.md` 的四维权重,判定「高 / 中 / 低 适配」
- **市场逻辑** —— 需求真实性、规模、护城河、关键变量;信息不足处明确标注
- **真伪与风险** —— 对照 `risks.md` 已知套路,判定「可信 / 存疑 / 疑似炒作」

最终给出**深入研究 / 持续观察 / 不跟**三选一的行动建议,并把评估文件落到 `memory/signals/`。

### 3. 记一闪而过的灵感(`/idea`)

```
/idea 也许可以把 finding 里的 SOP 自动转成 checklist 模板
```

只追加到根目录 `ideas.md`,不触发任何分析、不更新 memory。纯记录。

## 如何看分析结果

**总入口是 [`memory/INDEX.md`](memory/INDEX.md)**——它是所有记忆文件的导航地图。下面是常用入口和适用场景:

| 想看什么 | 去哪里 |
|---|---|
| 我现在的偏好/权重表 | [`memory/profile.md`](memory/profile.md) |
| 当前阶段和节奏提醒 | [`memory/timeline.md`](memory/timeline.md) |
| 已处理过哪些文章 | [`memory/findings/_processed.md`](memory/findings/_processed.md) |
| 单篇文章的提炼结果 | [`memory/findings/<slug>.md`](memory/findings/) |
| 已评估过哪些风向标 | [`memory/signals/_processed.md`](memory/signals/_processed.md) |
| 单条风向标的评估 | [`memory/signals/<slug>.md`](memory/signals/) |
| **当前在跟的出海方向候选** | [`memory/themes.md`](memory/themes.md) |
| 当前准备执行的最小验证实验 | [`memory/experiments.md`](memory/experiments.md) |
| 跨方向通用的方法论/决策准则 | [`memory/principles.md`](memory/principles.md) |
| 值得连接的人 / 社群 | [`memory/connections.md`](memory/connections.md) |
| 已识别的过时/夸大/骗局模式 | [`memory/risks.md`](memory/risks.md) |
| 临时灵感(未沉淀) | [`ideas.md`](ideas.md) |

**两条阅读路径,看你的目的**:

- **找方向**:从 `themes.md` 进 → 顺着候选条目里的 finding 链接钻进具体证据 → 决定哪个方向值得加码或下掉。
- **找方法**:从 `principles.md` 进 → 看哪些跨方向的认知已经积累、信心等级如何 → 用作具体动作的决策准则。

`themes` 和 `principles` 都只放结论 + 链接,不复述原文,所以阅读成本低。要看细节再点进 `findings/` 或 `signals/` 看完整三段式。

## 幂等保证

- 文章用 sha256 前 12 位查重,同一篇重复摄入只会处理一次
- 风向标用 sha256(原文 trim 后) 前 12 位查重
- 文件命名都用稳定英文 slug + 必要的日期前缀,避免标题改动导致历史断裂

## 维护

下面这些是**用户手动更新**的,不会被 agent 自动覆盖:

- `memory/profile.md` —— 偏好变化时改
- `memory/timeline.md` —— 阶段切换、计划调整时改
- `memory/INDEX.md` —— 新增 memory 文件时顺手加一条索引

agent 自动写入的部分:`findings/`、`signals/`、`themes.md`、`principles.md`、`connections.md`、`risks.md` 中的条目。

如果发现某条 memory 已经过时(例如某篇 finding 的市场环境已变),直接编辑或删除——memory 不是不可变历史,是当下最佳判断的快照。
