# memory/INDEX.md

> **本仓库的项目记忆入口。** Claude 会话开始时,先读这份索引,再按需打开具体文件。
> 所有记忆都以 markdown 存放在项目目录内,不依赖任何 agent 的本地缓存。

## 长期不变(画像与节奏)

- [profile.md](profile.md) — 用户画像、出海主线、试错容忍度、人脉关注点
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
- [connections.md](connections.md) — 值得连接的人 / 社群 / 关键节点
- [risks.md](risks.md) — 过时/诈骗/夸大模式库,新文章对照排雷

## 维护规则

- 每条新增/更新都要顺手把这份 INDEX 同步上,避免出现孤立文件。
- 一篇文章只在 `findings/` 写一次,聚合视图(themes/connections/risks)以**引用链接**指回 finding,不要复制内容。
- 文件名用稳定的英文 slug(必要时加日期前缀),不要用会变的标题文本,避免历史断裂。
