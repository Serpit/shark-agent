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

## 方法论库(可执行 SOP)

- [methods/axiom-scan.md](methods/axiom-scan.md) — 公理扫描 SOP（摄入文章/signals/教练对话三场景,9 条逐项问句）
- [methods/community-demand-discovery.md](methods/community-demand-discovery.md) — 社群平台需求挖掘 SOP(小红书 / Reddit / X 通用,6 步)
- [methods/search-engine-demand-discovery.md](methods/search-engine-demand-discovery.md) — 搜索引擎需求发现 SOP(Web/SaaS 出海,6 步,与社群版对位)
- [methods/benchmark-five-filters.md](methods/benchmark-five-filters.md) — themes 候选五重过滤（骨架版，同模式/同阶段/同合规/同需求层/同验证）

## 维护规则

- 每条新增/更新都要顺手把这份 INDEX 同步上,避免出现孤立文件。
- 一篇文章只在 `findings/` 写一次,聚合视图(themes/connections/risks)以**引用链接**指回 finding,不要复制内容。
- 文件名用稳定的英文 slug(必要时加日期前缀),不要用会变的标题文本,避免历史断裂。
