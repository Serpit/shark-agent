# dbskill 整合改造方案（Phase 版）

> 起草日期：2026-04-30
> 目的：把 dontbesilent 的 dbskill（https://github.com/dontbesilent2025/dbskill）公理与方法整合进 shark-agent，作为底座加固判定层。
> 状态：**草稿，未实施**。每个 Phase 标注确认状态，下次会话从这里继续。

---

## 总策略（确认状态：✅ 已确认）

走 **B 路线「全量重构（B1 阶段先做）」**，分两阶段：

- **B1（本轮要做）**：公理升格为底座 + 重组 principles + 重构 risks + 新增 diagnoses 目录 + 改写 CLAUDE/AGENTS 协议。**不动 finding 三段式。**
- **B2（B1 跑顺一个月后再决定）**：是否回填 7 篇旧 finding 到新三段式（增加"问题分类 / 公理扫描"两段）。

理由：dbs 公理在「聚合判断层」（principles/risks）接管收益最大；finding 是文章摄入产物，硬塞 dbs 模板可能"为公理而公理"。

---

## 重构后目录形状（确认状态：🟡 大方向已确认，命名细节待定）

```
shark-agent/
├── CLAUDE.md / AGENTS.md             ← 协议改写：公理是底座，不是附加
├── memory/
│   ├── INDEX.md                      ← 同步
│   ├── profile.md                    ← 新增「公理锚点」section
│   ├── timeline.md                   ← 不变
│   │
│   ├── axioms.md                     ← 🆕 公理底座
│   ├── principles.md                 ← 重组：每条挂公理
│   ├── risks.md                      ← 重构：按公理编号归档
│   │
│   ├── findings/                     ← 三段式不变（B1 不动）
│   ├── signals/                      ← 三段式不变，真伪判定加公理扫描
│   ├── talks/                    ← 🆕 咨询记录
│   ├── themes.md / experiments.md / todos.md / connections.md  ← 不变
│   └── methods/
│       ├── community-demand-discovery.md      ← 不变
│       ├── search-engine-demand-discovery.md  ← 不变
│       ├── axiom-scan.md                      ← 🆕 公理扫描 SOP
│       └── benchmark-five-filters.md          ← 🆕 themes 候选过滤
└── .claude/commands/
    ├── idea.md                        ← 不变
    ├── signals.md                     ← 改：加公理扫描步
    └── talk.md                    ← 🆕 /talk 触发咨询模式
```

---

# Phase 1：axioms.md（公理底座）

**确认状态：🟡 内容已逐条对齐，最终撰写未做**

**文件**：`shark-agent/memory/axioms.md`（新建）

## 1.1 dbs 6 公理改写版（已逐条表决）

| 编号 | 主题 | 采纳形态 | 状态 |
|---|---|---|---|
| 公理 1 | 模式独立于人 | **改写**：保留"模式 > 个人"，加 "input 含能力门槛" 限定 | ✅ |
| 公理 2 | 模式决定道德 | **直接采纳 dbs 原版** | ✅ |
| 公理 3 | 智力不直接变现 | **改写**：区分「底层认知（必要）」vs「过度分析（逃避）」 | ✅ |
| 公理 4 | 流量≠收入 | **改写**："99%" → "多数情况" | ✅ |
| 公理 5 | 定价即产品 | **改写**：倍数按品类分（知识付费 5-15x / SaaS 2-5x） | ✅ |
| 公理 6 | 多数卡点是心理问题 | **改写**："99%" → "多数（经验上约 2/3 起）" + 加判定方式 | ✅ |

## 1.2 shark 自己的准公理 A/B/C（用户已认可加入）

| 编号 | 主题 | 来源证据 | 状态 |
|---|---|---|---|
| 准公理 A | 形态决定复利——副业必须选"人不在也跑"的形态 | 已有 principle「副业要做能离开人也跑的事」 | ✅ |
| 准公理 B | 窗口期优先于复制案例——所有"X 个月赚 Y"案例先问窗口期 | risks「热词窗口幸存者偏差」+「YouTube AI faceless 红利已过」 | ✅ |
| 准公理 C | 模式 vs 努力的分层判断——出现"我比别人努力 X 倍"先问模式天花板 | risks「在差模式里硬卷」+ principle「副业要做能离开人也跑的事」 | ✅ |

## 1.3 待确认细节

- ✅ A/B/C 与 dbs 6 条**分两层**：第一层 dbs 公理 1-6（普适商业规律），第二层 shark 应用层准公理 A/B/C（出海/副业语境的启发式）。理由：普适性不同 + A/B/C 未来可能扩充淘汰，分层后改 A/B/C 不动 dbs 底座 + 扫描时判定权重不同（dbs 冲突→大概率 anti-pattern；A/B/C 冲突→打问号追问）。
- ✅ 公理 6 写"多数（经验上约 2/3 起）"。理由：需要数量级锚点供 /talk 心理 vs 信息分类用；同时用"经验上"明确这是判断启发式而非实证数据。
- ✅ axioms.md 每条用**两段结构**：「表述」+「触发判定」（每条 ~5 行）。理由：方案 A 沦为目录、使用摩擦大；方案 B 与 axiom-scan.md 双份维护风险高；方案 C 让 axioms.md 单文件可用，axiom-scan.md 专做"扫描流程按场景分组"（摄入文章 / signals / diagnose），职责不重叠。

---

# Phase 2：methods/axiom-scan.md（公理扫描 SOP）

**确认状态：🟡 设计骨架已对齐，最终撰写未做**

**文件**：`shark-agent/memory/methods/axiom-scan.md`（新建）

## 2.1 已确认设计

把 axioms.md 6+3 条变成可执行清单，给 finding/signal 评估时强制对照。使用时机：
- 摄入文章：finding 三段式写完后扫一遍，触发的公理在「风险提示」段标注
- 评估风向标：`/signals` 第 3 步「真伪与风险」前必扫
- 教练对话：用户提商业问题时，先用公理 1/3/6 做问题分类

## 2.2 待确认细节 ⬜

- **公理扫描的"硬度"阈值**：摄入文章时冲突 ≥2 条 → 直接 anti-pattern 不写 finding。这个阈值合理吗？计划跑 5 篇新文章后调整。
- 输出格式：finding 风险段标注 `⚠️ 公理 4 冲突：作者声称"3 个月涨粉 10 万"但未披露任何收入或转化数据`——是否所有冲突都用统一格式？

---

# Phase 3：principles.md 重组（每条挂公理）

**确认状态：🟡 重组方向已确认，"挂公理"细节未对齐**

**文件**：`shark-agent/memory/principles.md`

## 3.1 已确认动作

- 现有 8 条 principles 每条标注「**根公理**：公理 X / 准公理 Y」字段
- 区分两层：**底层公理**（axioms.md）vs **应用方法论**（principles.md）
- 新增 1 条 principle：
  - 「先问问题成不成立——消解优于回答」（根公理：公理 6，关联：公理 3）
- 删除候选「99% 卡点是心理问题」——与公理 6 完全重复，合入 axioms.md，不重复成 principle
- 升级 1 条 principles：「先验需求再投产能 BRD 优于 IDE」适用边界追加"与公理 6 联动"

## 3.2 待确认细节

- ✅ 标注结构：**根公理 1 条 + 关联公理 N 条（不限数量，全挂上）**。根公理判定用"必要条件"——违反它这条 principle 就不成立；关联公理列出所有真实相关的，不强求精简。理由：principles 本来就是多公理交叉的产物，关联越全公理扫描时召回越准。
- ✅ 13 条 principles 根公理映射（已确认）：

  | # | Principle | 根公理 | 关联公理 |
  |---|---|---|---|
  | 1 | 抄出 MVP——别在验证期搞创新 | 公理 1 | 公理 3 |
  | 2 | 具象化需求——AI 时代的核心生产力 | 公理 3 | 公理 1 |
  | 3 | 先发再迭代——做出 v0.1 优于完美计划 | 公理 3 | 公理 6 |
  | 4 | 自动化前先核算时间成本 | 公理 3 | 准公理 A |
  | 5 | 卖解决方案，而非卖产品 | 公理 5 | 准公理 A |
  | 6 | 供应链优先于产品（B2B 特化） | 公理 1 | 准公理 B |
  | 7 | 先验需求再投产能 BRD 优于 IDE | 公理 3 | 公理 6、公理 4 |
  | 8 | 差评是金矿，3-4 星是 PRD | 公理 4 | 公理 1 |
  | 9 | 用数量博概率——做 N 个 v0.1 | 准公理 A | 公理 3、公理 1 |
  | 10 | 流程数据 > 代码——工具产品护城河 | 公理 5 | 公理 1 |
  | 11 | 副业要做能离开人也跑的事 | 准公理 A | — |
  | 12 | 需求发现路径要匹配产品分发生态 | 公理 1 | — |
  | 13 | 不要裸辞创业——心态急是反模式 | 公理 6 | 公理 3、准公理 B |
  | 14（新增）| 先问问题成不成立——消解优于回答 | 公理 6 | 公理 3 |
- ✅ "99% 卡点心理问题" **删除**，不独立成 principle（与公理 6 完全重复）。

---

# Phase 4：risks.md 重构（按公理编号归档 + 清重复 + 新增 4 条）

**确认状态：🟡 重构方向已确认，归档格式未对齐**

**文件**：`shark-agent/memory/risks.md`

## 4.1 已确认动作

- 清理现有 3 处「热词窗口幸存者偏差」重复条目（保留首次出现的）
- 现有 5 条 risks 每条标注「**违反公理**：X」字段
- 新增 4 条「公理派生」反模式：
  - 「认知贩卖」叙事（违反公理 3）
  - 「粉丝数=成功」流量神话归因（违反公理 4）
  - 「在差模式里硬卷」叙事（违反公理 2）
  - 无定价分层的"产品成功"案例（违反公理 5）

## 4.2 实际是 6 条 risks 的违反公理映射（已确认 ✅）

| # | Risk | 根公理（违反） | 关联公理 |
|---|---|---|---|
| 1 | YouTube AI 低质内容红利已过 + 高封号 | 准公理 B | 公理 1（input 复刻假设失效——平台规则变了） |
| 2 | 热词窗口幸存者偏差（候选） | 准公理 B | 公理 1（缺失 input 自检）、公理 4（流量数据被夸大） |
| 3 | "AI 编程是工业革命"焦虑营销 | 公理 6 | 准公理 C（"再不上车就晚了"误把时机当模式天花板） |
| 4 | "外贸普惠红利还在"叙事 | 准公理 B | 公理 1（能力门槛缺失）、公理 6（焦虑推动） |
| 5 | 独立开发者低价定价陷阱 | 公理 5 | 准公理 C（在差定价里硬卷） |
| 6 | 数字模板"做一次卖无数次" | 公理 4 | 公理 5（成本核算缺失）、准公理 A（伪资产型） |

## 4.3 归档格式（已确认 ✅）

- ✅ **方案 B**：现有标题不变，每条加「**违反根公理**：X」+「**关联公理**：Y、Z」字段。理由：与 principles.md 同构（按主题组织、字段标注公理映射）；多公理关联在分组式里放不下；改动小、不影响现有锚点；分组式视觉效率交给 axiom-scan.md 的反查索引解决。

---

# Phase 5：profile.md 注入「公理锚点」section

**确认状态：🟡 方向确认，具体放置位置和文案未定**

**文件**：`shark-agent/memory/profile.md`

**位置**：「方向筛选权重」section 之后、「偏好与禁区」之前新增一节。

**已确认**：profile.md 是判定 finding/signal 保留与否的权重表，需要把公理作为底层判定锚点列出来，并指向 axioms.md 和 axiom-scan.md。

**已确认 ✅**：
- 方案 B：只放索引 + 关键判定动作（dbs 1-6 + 准公理 A/B/C 的简短摘要 + 链接到 axioms.md / methods/axiom-scan.md）。理由：单一真相源避免双份维护；agent 启动协议已有"读 axioms.md"步骤，profile.md 自包含没必要。

---

# Phase 6：CLAUDE.md / AGENTS.md 重写（同步等价）

**确认状态：⬜ 整体方向有，具体改动条目未对齐**

**文件**：`shark-agent/CLAUDE.md` 和 `AGENTS.md`

## 6.1 计划改动

1. 「Agent 的职责」第 1 条「降噪过滤」追加：判定锚点引用 axioms.md + axiom-scan.md
2. 「文章摄入工作流」第 2 步后插入新子步骤 2.5「公理扫描」
3. 「会话启动协议（教练晨报）」加载步骤新增「读 axioms.md」+「读 talks/ 最近 3 条未结转」
4. 新增「外部工具援引（dbskill 联动）」section：场景信号 → 推荐 dbs skill 表
5. 新增「心理卡点识别（公理 6 联动）」行为约束

## 6.2 待确认细节

- ✅ 教练晨报输出格式：**方案 A+B**——不增加新行，仅在 [提醒] 行扩展能力支持公理派生提醒（如公理 6 心理卡点）；talks 未结转不单独占行，仅在与当前对话主题同源时按需召回（如"这个问题在 YYYY-MM-DD talk 已分类为心理问题"）。
- ✅ 「公理 6 心理卡点提醒」触发频率（方案 C）：
  - **单轮信号词触发**：用户出现"我担心"、"会不会失败"、"还没准备好"、"再调研一下"、"等 XX 之后"等延后/逃避词 → 当轮提醒
  - **跨轮纠结触发**：同话题连续 ≥2 轮回到"还没决定/再想想" → 第 2 轮末尾追加"这是信息问题还是心理问题？"问句
  - **冷却**：同话题触发后冷却 3 轮不再重复
  - **退出**：用户明确说"我知道是心理问题"或"先放着" → 标记已识别，本会话不再触发
- ✅ dbskill 联动：**方案 B**——shark 完全独立，dbskill 公理已内化为 axioms.md；不在协议里安排读外部仓库；GitHub 链接仅作为 axioms.md 头部「来源说明」的引用，不作为 agent 运行时的网络读取目标。理由：保持"项目内记忆系统"自洽、可离线；dbskill 未来更新由 shark 主动 review 决定吸收，不自动同步。

---

# Phase 7：新增 /talk command + talks/ 目录

**确认状态：⬜ 整体设计有，命名和模板未定**

**文件**：
- `shark-agent/.claude/commands/talk.md`（新建）
- `shark-agent/memory/talks/`（新建目录 + README）

## 7.1 已确认设计

- 第三个工作流入口（与 摄入文章 / `/signals` 平级）
- 流程：模式选择（问诊/体检）→ 问题分类（信息/模式/心理/假问题）→ 调用对应方法 → 落到行动 → 写 diagnoses 文件 → TODO 自动捕获
- 不依赖 dbs plugin（独立实现，plugin 作为可选援引）

## 7.2 待确认细节

- ✅ **命令命名**：`/talk`（入口名不纠结，全文需把 `/talk` 替换为 `/talk`，diagnoses 目录是否同步改名见下）
- ✅ **目录名**：`memory/talks/`（与 `/talk` 命令同名，避免割裂）
- ✅ **文件颗粒度**：中等（6 段：问题 / 分类 / 公理扫描结果 / 关键追问 / 消解 / 行动），第一条实际写完后 review 模板
- ✅ **slug 命名约定**：`YYYY-MM-DD-<topic-slug>.md`。同主题在不同时间重新评估 → 开新文件（保留判断演变），新文件头部链接到旧文件；同一次 talk 跨多轮对话推进 → 仍是同一文件（中途更新）。同一天同主题多次开新 talk 用 `-1/-2` 后缀。

---

# Phase 8：改 .claude/commands/signals.md

**确认状态：✅ 改动很小，方案已定**

**文件**：`shark-agent/.claude/commands/signals.md`

## 已确认改动

1. 第 2 步「读权重与风险库」追加一行：
   > - `memory/methods/axiom-scan.md` — 拿到 9 条公理逐项问句，第 3 步真伪判定时强制对照
2. 第 3 步 signal 文件模板的「3. 真伪与风险」段，描述前追加：
   > 必须先按公理清单 9 条扫一遍，触发哪几条标注「公理 X 冲突」；之后再对照 `risks.md` 已知模式。

---

# Phase 9：新增 methods/benchmark-five-filters.md

**确认状态：🟡 骨架已定，是否扩成完整 SOP 待定**

**文件**：`shark-agent/memory/methods/benchmark-five-filters.md`（新建）

## 9.1 已确认设计

五重过滤（同模式 / 同阶段 / 同合规 / 同需求层 / 同验证），用于 themes.md 候选评估。

## 9.2 已确认细节 ✅

- ✅ 方案 B（骨架版）：五重过滤名 + 一句话定义 + 1 个示例 + 「待迭代」段。理由：B1 阶段五重过滤还没在 shark themes 评估里实战过，避免"为公理而公理"过度设计；第一次实战时回填判定问句更准。
- ✅ themes.md 模板**不**硬性要求"过滤记录"段——只在新增 theme 候选时手动调用，避免老 theme 显得不规范。

---

# Phase 10：INDEX.md 同步

**确认状态：✅ 改动机械化，方案已定**

**文件**：`shark-agent/memory/INDEX.md`

新增三个入口：
- `axioms.md` — 公理底座（顶级位置，置于 profile.md 之上或同级）
- `methods/axiom-scan.md` — 公理扫描 SOP
- `methods/benchmark-five-filters.md` — themes 候选过滤
- `talks/` — 咨询记录目录

---

# Phase 11（可选）：安装 dbs plugin

**确认状态：⬜ 暂不决定**

```bash
claude plugin marketplace add dontbesilent2025/dbskill
claude plugin install dbs@dontbesilent-skills
```

**已确认**：B1 重构后 shark 完全独立，安装与否不影响功能。`/talk` 识别到心理卡点 → 主动建议 `/dbs-action`；识别到概念模糊 → 建议 `/dbs-deconstruct`。这些建议是"软联动"，不安装 plugin 时降级为"读 dbskill 仓库知识包"。

---

# Phase 12（B2 阶段，远期）：finding 三段式回填

**确认状态：⬜ B1 跑顺一个月后再决定**

把 finding 三段式从「价值标签 / 核心 SOP / 风险提示」改为「**问题分类 / 公理扫描结果 / 可复用 SOP / 风险提示**」，回填 7 篇旧 finding。

**未决依据**：B1 一个月使用情况——如果新摄入文章在公理扫描层已经覆盖大部分判断，B2 不必做。

---

# Phase 13（远期可选）：atoms.jsonl 作为 RAG 旁路

**确认状态：⬜ 远期，B1+B2 完成后再评估**

把 dbskill 4,176 条结构化原子接入 shark 作为相似案例检索源。预期收益边际递减（公理已覆盖 80% 价值）。

---

## 实施工作量估算（B1 阶段，Phase 1-10）

| Phase | 工作量 |
|---|---|
| 1. axioms.md | 30 分钟 |
| 2. methods/axiom-scan.md | 30 分钟 |
| 3. principles.md 重组 | 1 小时 |
| 4. risks.md 重构 | 30 分钟 |
| 5. profile.md 公理锚点 | 10 分钟 |
| 6. CLAUDE.md / AGENTS.md 重写 | 1 小时 |
| 7. /talk + talks/ | 30 分钟 |
| 8. signals.md 修改 | 10 分钟 |
| 9. benchmark-five-filters.md | 20 分钟 |
| 10. INDEX.md 同步 | 10 分钟 |
| **合计 B1** | **~4.5 小时** |

---

## 实施顺序建议（B1 阶段）

1. **Phase 1**（axioms.md） — 因为后续 principles/risks 的"挂公理"动作依赖 axioms 的最终编号
2. **Phase 2**（axiom-scan.md） — 公理变成可执行 SOP
3. **Phase 4**（risks.md 重构） — 先做改动小、风险低的
4. **Phase 3**（principles.md 重组） — 8 条逐条标
5. **Phase 5**（profile.md 锚点）
6. **Phase 6**（CLAUDE/AGENTS） — 协议层最后改，避免反复
7. **Phase 7**（/talk）
8. **Phase 8**（signals.md）
9. **Phase 9**（benchmark-five-filters.md）
10. **Phase 10**（INDEX.md 同步收尾）

---

## 风险与回滚预案

- **风险**：B1 重构后第一周 agent 行为可能不稳定（教练晨报多了公理触发，可能噪音偏多）
- **回滚预案**：所有改动都在 git 里。B1 跑一周如不顺：
  - axioms.md 和 talks/ 可保留（独立增益）
  - principles/risks 重组可 revert 回旧版本
  - CLAUDE/AGENTS 改动可 revert
- **不可回滚的**：finding 三段式（B2 才动），这也是 B1 不动 finding 的核心理由

---

## 待确认问题汇总（下次会话从这里开始）

按优先级列出，每条解决后才能进入对应 Phase 实施：

### P0（必须先解决，影响 Phase 1）
1. ✅ axioms.md 中 A/B/C 与 dbs 6 条**分两层**（dbs 1-6 底座 / A/B/C shark 应用层）
2. ✅ 公理 6 写法："多数（经验上约 2/3 起）"
3. ✅ axioms.md 每条用两段结构（表述 + 触发判定）

### P1（影响 Phase 3-4）
4. ✅ 13 条 principles 根公理映射（含新增第 14 条，见 §3.2 表格）
4b. ✅ "99% 卡点心理问题" 删除，不独立成 principle
5. ✅ 实际 6 条 risks 的违反公理映射（见 §4.2 表格）
6. ✅ risks.md 归档格式：方案 B（标注字段，标题不变）
7. ✅ "99% 卡点心理问题" 删除（已在 P1-4b 解决）

### P2（影响 Phase 6-7）
8. ✅ 「公理 6 心理卡点提醒」触发：方案 C（信号词 + 跨轮纠结 + 冷却 3 轮）
9. ✅ 命令命名：`/talk`
10. ✅ talks 目录名 `memory/talks/`，文件颗粒度中等（6 段）

### P3（影响 Phase 5、9）
11. ✅ profile.md 公理锚点 section：方案 B（只放索引 + 链接）
12. ✅ benchmark-five-filters.md：方案 B（骨架版） + themes.md 不硬性要求过滤记录段

---

## 下一步（恢复时从这里继续）

### 状态：所有决策已锁定（2026-04-30），可直接进入实施

P0-P3 + Phase 6/7 内部细节全部确认完毕，参见上文各 Phase 的 ✅ 标注。

### B1 实施任务清单（已拆 7 个 task）

新会话恢复时，告诉 agent：

> 读 `shark-agent/drafts/dbskill-integration-plan.md`，然后 `TaskList` 找 pending 且 blockedBy 为空的 task，按 task description 执行。

| Task | Phase | 依赖 | 预估 |
|---|---|---|---|
| **#4** | Phase 1+2：axioms.md + methods/axiom-scan.md | 无 | 1h |
| #3 | Phase 4：risks.md 重构 | #4 | 30m |
| #5 | Phase 3：principles.md 重组 | #4 | 1h |
| #7 | Phase 5+10：profile.md 公理锚点 + INDEX.md 同步 | #4 | 20m |
| #2 | Phase 7+8：/talk command + talks/ 目录 + 改 signals.md | #4 | 40m |
| #1 | Phase 9：methods/benchmark-five-filters.md（骨架版）| #4 | 20m |
| #6 | Phase 6：CLAUDE.md + AGENTS.md 重写 | #4、#2 | 1h |

### 执行顺序

1. **必须先做 Task #4**（其他所有 task 都依赖它确定的公理编号）
2. #4 完成后，#3 / #5 / #7 / #2 / #1 可并行（互不依赖）
3. **最后做 Task #6**（CLAUDE/AGENTS 协议改写要等 /talk 入口和 talks/ 目录就位）

### 恢复时的快速 checklist

新会话开始前：
- [ ] `git status` 确认工作树干净
- [ ] 读 draft 顶部「总策略」+ 当前 Phase 的「确认状态」段
- [ ] `TaskList` 看哪些 task 已完成、哪些 pending、哪些 blocked
- [ ] 选定一个 pending + blockedBy=空 的 task，`TaskUpdate status=in_progress`
- [ ] 完成后 `TaskUpdate status=completed`，进入下一个

### B1 跑顺一个月后

回头评估 Phase 12（finding 三段式回填）和 Phase 13（atoms.jsonl RAG 旁路）是否启动。
