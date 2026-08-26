# 待办与进度

> 具体可执行的 TODO 跟踪,跨实验/跨方向。**颗粒度 = 单次或几次能干完的动作**。
>
> | 该写哪 | 内容 |
> |---|---|
> | `todos.md`(本文件) | 单次能干完的具体动作:切美区 IP / 注册域名 / 验证某关键词 / 联系某人 |
> | [`experiments.md`](experiments.md) | 实验级目标,带 GO/NO-GO 标准、时间盒、预算 |
> | [`timeline.md`](timeline.md) | 阶段切换、月度节奏、降级触发 |
> | `ideas.md`(由 `/idea` 维护) | 跨会话灵感,未必转 TODO |

## 状态约定

- `todo` 待开始
- `doing` 进行中(同时最多 2-3 项,避免散乱)
- `blocked` 阻塞,必须标**原因**和**解阻条件**
- `done` 已完成(保留 14 天后清理或归档到对应 experiment 的结果记录)

## 当前

> **2026-08-09 重置**:记忆断档 3 个月,期间 4 站上线跑通。旧 TODO(等热词候选 / 分发生态自检 / 切美区 IP 跑 SERP)已随选词方式换轨作废,见下方「已作废」。新 TODO 全部来自 Search Console 实测数据。

### doing

- [ ] **2026-08-26** · M4 · 复跑三件夹具,验证 partfit3d 颜色拆分的 Prusa 修复
  - **为什么**:08-26 端到端验收 Bambu PASS / Orca PASS / **Prusa 产品级 FAIL**(filament 颜色被 fallback 替换、导出 STL 有非流形边却误报 watertight、UI 把 `mmu_segmentation` 错标为 `paint_color`)。三处代码已改并提交(`2a25698`),**但未复验**
  - **动作**:用官方 issue 夹具(PrusaSlicer #7134 / BambuStudio #2411 / OrcaSlicer #12426)重跑,逐件检查 ①slot 颜色是否按原 index 保留 ②导出件 `edge multiplicity != 2` 与重复三角是否归零 ③UI source label 是否正确
  - **⚠️ 这是 Step 3b 的前置**:带非流形边的导出接到已有曝光页,比没有功能更伤
  - **关联**:[experiments.md 颜色拆分 A 路线](experiments.md#partfit3d-颜色拆分功能a-路线2026-08-25-立项)
  - **预计耗时**:1 小时

- [ ] **2026-08-26 起** · M5 前置 · 用新判据筛 [themes.md](themes.md) 的 6 个支付引荐候选
  - **新判据(前四次一条都没用过)**:① [CPC 分层](principles.md#用-cpc-分层识别付费意愿大流量低-cpc-是免费用户池)——量最大的词 CPC < $1 就是流量池不是生意池;② [做在被定价为 0 的那一层](risks.md) 三问;③ **能不能在 2 周内验证付费意愿**——答不上来直接淘汰,不管词多好打
  - **进度**:6 个候选桌面筛选已完成,**直接克隆候选 0 个**;只保留 `AI 建站发布防错 + 持续 SEO 巡检`作为相邻命题,下一步写一页 offer 并向 15 个目标用户收 $19 refundable deposit
  - **边界**:现在批准的是第五站的选题/访谈/预售/付费探针,不是注册域名和开发;候选必须先同时通过三条新判据才进入 MVP
  - **2026-08-26 补跑**:哥伦布线**已结案**(`ai ad creatives` 实际仅 26 点击/月;全库 374 词复核,封顶结论成立)。
    但补跑意外发现 `sem=high` 桶里的**买量型第二模型**,并拆出 A/B 两型 ——
    **B 型(`datephotos.ai` 形态:明确场景 + 客单 $29 起 + 自然搜索承接 + programmatic SEO)是新的选题模板**
  - **关联**:[experiments.md 第五站候选筛选与付费意愿验证](experiments.md#第五站候选筛选与付费意愿验证m5-前置2026-08-26)、[sources/columbus.md 硬边界 7](sources/columbus.md)

- [ ] **2026-08-26** · M5 前置 · 拆 `datephotos.ai` 形态做第五站选题模板
  - **为什么**:本轮 10 站里唯一同时满足「个人量级 + 自然搜索为主体 + 有真实价格阶梯」的样本 ——
    9 个月、DR 33、47.2% 自然搜索、客单 **$29–800**、533 引用域 49% dofollow
  - **动作**:人工开站,拆 ①场景怎么切窄的(约会软件头像,不是"AI 写真")②价格阶梯怎么分档
    ③programmatic SEO 生成的是什么页 ④affiliate program 怎么设计
  - **边界**:拆的是**形态模板**,不是克隆这个站(约会头像品类不进候选)
  - **预计耗时**:1 小时

### todo

- [ ] **2026-08-26** · M4 · 把 A 路线时间盒从 09-08 改到 09-13
  - **原因**:Step 3b 最早 08-30(要等 TDK 读数)上线,Step 4 要求「Step 3b 上线后重新锁 14 天窗口」→ 08-30+14 = **09-13**,原时间盒 09-08 物理上达不到
  - **动作**:改 [experiments.md 颜色拆分 A 路线](experiments.md#partfit3d-颜色拆分功能a-路线2026-08-25-立项)的时间盒字段;GO 标准(CTR 0.3%→≥1.5%)不变
  - **预计耗时**:5 分钟

- [ ] **2026-08-30** · M4 · TDK 读数 → Step 3b:把颜色入口接到已有曝光页
  - **动作**:① 拉 `/tools/3mf-splitter-online/` 的 TDK 实验读数(14 天窗口到期)② 读完立即把颜色模式接到该页(3,808 曝光)与 `/`(1,876 曝光)③ 重新锁 14 天窗口
  - **前置**:上方「复跑三件夹具」必须先完成
  - **说明**:在 Step 3b 之前,原假设「转化现成 ~3,000 曝光/月」**尚未开始验证**;独立页 `/tools/3mf-color-splitter` 新上线无基线,单独看收录/query,不与旧页混算

- [ ] **2026-09-13** · M4 · partfit3d A 路线 GO/NO-GO + 按退出条件收尾
  - **GO**(词族 page 维度 CTR ≥1.5%)→ 记下「补功能转化现成曝光」这个方法可复用,**站转维护态,不再投入新功能**
  - **NO-GO**(CTR <0.8%)→ 确认那 3,000 曝光是纯品牌导航(在找 split3mf.com 这个牌子),**直接停,不转 B 路线**(stl-repair 同样是免费商品 + 同样的分母问题)
  - **两种情况都不再为 partfit3d 做变现** —— 它的产出是方法,不是钱。依据见 [risks.md 做在被定价为 0 的那一层](risks.md)

- [ ] **2026-08-12 早上** · M4 · 复核 `CSV → QBO` 关键词数据,作为市场基准保留(**不启动 MVP**)
  - **动作**:① 两个估算源复核核心词 Volume / KD / CPC ② 无痕美区 SERP 重扫 Top 10 收费站与价格 ③ 查 Intuit Web Connect 对 FID / Financial Institution partner ID 的官方要求 ④ 记录结论为「数据成立 / 数据不成立」
  - **定位**:这个词的商业信号仍然好,但会计用户与当前 X / 独立开发圈不重叠,**不适合作为 Build in Public 主产品**;本轮只校验数据,不注册域名、不写代码
  - **关联**:[experiments.md CSV → QBO 转换器](experiments.md#csv--qbo-转换器付费工具站2026-08-10-跑完-keyword-hunt-第二轮-step-0-5)
  - **预计耗时**:1-2 小时

- [ ] ~~**2026-08-09**(2026-08-11 升回优先)· M4 · 修 partfit3d 的 title + meta description~~ —
  **2026-08-12 被更精确的 TDK 单页实验取代**(见下方 2026-08-12 条目,基于同日 SERP 诊断给出具体文案)
  - 原动作:按序改 `split 3mf` → `split3mf` → `split3dmf` 的落地页 title/meta,加动作词与差异点(免费 / 无需上传 / 浏览器内完成)。主战场是 `/tools/3mf-splitter-online/` 一页——它单页占 486 曝光
  - **⚠️ 2026-08-11 期望订正**:原写"3 个月上限 +10 次点击,做完就走"——**那个数字算错了分母**。
    `split 3mf` 实测约 **1,180 曝光/月**、当前 CTR 仅 0.3%,同样的修复对应的是**几十次点击/月**
  - **关联**:[experiments.md 2026-08-11 曝光量订正](experiments.md#结果记录)

- [ ] **2026-08-10**(2026-08-12 动作细化)· M4 · 验证 `.qbo` 能被 QuickBooks 实际导入(**前置风险,阻塞建站**)
  - **动作**:~~查条款~~ → **改为实测**:手搓一份 20 笔交易的 `.qbo`(OFX 1.0.2 SGML,叶子标签**不闭合**),
    用 QuickBooks 试用账号走 `File → Import → Web Connect` 实际导一次。重点看三件事:
    ① `INTU.BID` 填任意值会不会被拒 ② `FITID` 重复是否被静默去重 ③ Desktop 与 Online 行为差异
  - **⚠️ 为什么改**:2026-08-12 问了哥飞,它在这一问上给的 `INTU.BID=3256`「通用标识符」无依据,
    且把 OFX **请求**报文当成导入文件结构贴出来 —— **顾问回答不能替代实测,反而降低了该问的可信度**。
    见 [advice/2026-08-12](advice/2026-08-12-csv-to-qbo-serp-assessment.md)
  - **旁证(不构成结论)**:ProperSoft、MoneyThumb、accountingconverter 商业化多年说明路是通的
  - **关联**:[experiments.md CSV → QBO 转换器](experiments.md#csv--qbo-转换器付费工具站2026-08-10-跑完-keyword-hunt-第二轮-step-0-5)
  - **预计耗时**:30-60 分钟(含注册试用账号)

- [ ] **2026-08-10**(2026-08-12 拆细)· M4 · 开通 Waffo Pancake 收款(**并行,不阻塞建站**)
  - ✅ **资料核实已完成**(2026-08-12):费率 / 资质 / 地区 / 结算周期已查清并落盘 → [sources/waffo.md](sources/waffo.md),
    profile.md 支付通道条目已回写。**剩下的是实操,不是调研。**
  - **① 今天就能做(零成本、零审核、30 分钟)**:OAuth 注册 → 建 Store → 建一个测试产品 →
    用测试卡 `4576750000000110` 跑通一次 checkout。**这一步不需要网站、不需要 KYB、不需要身份证**,
    纯验证技术链路可行 + 拿到 Merchant ID / API Key
  - **② 建站前必须先定的两件事**(顺序错了会返工):
    - **终版域名** —— KYB 批准后**域名锁死**,只能找客服改
    - `support@<终版域名>` —— 支持邮箱与网站同域可**一键验证域名**,省掉 DNS 步骤(Cloudflare Email Routing 免费转发即可)
  - **③ 站上线后提交 KYB**(1–3 工作日):产品可用无登录墙 + 定价页公开 + Privacy/ToS 免登录可访问 +
    支持邮箱显示在站上且与提交一致 + **不撞 Intuit 商标**
  - **④ KYC 绑卡**(可与 ③ 并行):身份证 18 位,**legal full name 逐字符核对** —— 首次提现后该字段永久锁定
  - **⚠️ 运营纪律**:提现费 1% 但**最低 $10/笔**,**攒到 ≥$1,000 再提现**;$20 提一次等于交 50% 手续费
  - **预计耗时**:① 30 分钟 · ③④ 各 30 分钟(不含等审核)

- [ ] **2026-08-10**(2026-08-12 重新定性)· M4 · 做 CSV → QBO 转换器 MVP —— **目标是验证 Waffo 收款闭环,不是赚钱**
  - **⚠️ 2026-08-12 用户决策:零外链预算,只做免费 SEO。** 天花板已用 Ahrefs 实测封顶
    (排第 1 = 551 UV/月 → **$15–70/月**),不值得投外链钱。$2–5K 外链预算留给新标准下的下一个站
  - **动作**:注册域名 + Astro/Cloudflare;**主攻 `csv to qbo converter` 系列,不要主攻头词 `csv to qbo`**
    —— Ahrefs 实测头词 Top 10 是 AI Overview + How-to 文章主导(仅 1 个 Tool 页),
    而 converter 词标 `I C T` 三意图且 Tool 页排第一。**这是本轮最重要的策略订正**
  - **免费额度定为每月 3 次完整转换**(锚点:够簿记员试一次当月的账)。⛔ 不做输出文件加水印
  - **定价**:订阅制,排除一次性买断。锚点 $15/$25/$39,**不要定 $1-5**([risks.md 低价陷阱](risks.md#独立开发者低价定价陷阱))
  - **⛔ 域名不要选 `easyqbo.com` 这类锁死单一格式的**(相邻 IIF 词族约 2,400/月装不进去)
  - **预计耗时**:1-2 周
  - **前置**:`.qbo` 导入实测 + Waffo 注册两条

- [ ] **2026-08-12**(新约束框架下的第一件事)· M4 · 按新标准重跑 keyword-hunt 找**大站**候选词
  - **前置**:[keyword-hunt skill](../.claude/skills/keyword-hunt/SKILL.md) 的 Step 3 / Step 5 阈值已标失效,
    **改写后才能整轮跑**(新阈值:KD < 55 · Volume > 2,000/月 · 词族 > 20K · 引用域折算成预算而非否决线)
  - **新约束**:$2,000–5,000 外链预算 / 手段不设限 / 目标大搜索量 + 付费收入。见 [timeline.md](timeline.md)
  - **三条必须带进筛选的边界**:① 判可打性用**页面级**引用域,判成本用域名级 ② 每 UV 价值 > 搜索量
    ③ 若考虑付费广告,必须单独算 CAC/LTV,不可沿用 csv-to-qbo 的结论
  - **第一个可查的具体动作**:扒 `accountingconverter.com` 的 410 个引用域来源,反推批量目录套餐的实际单价
    —— 这是本项目第一次有真实外链报价参照
  - **预计耗时**:skill 改写 1 小时 + 整轮 8.5 小时
  - **⚠️ 2026-08-13 新增边界**:再跑之前先读 [risks.md CPC 系统性偏低](risks.md#ai-工具站品类的-cpc-系统性低-1-2-个数量级用它找付费生意是池子选错违反公理-4)。
    **不要再从哥伦布 AI 工具站库出发找付费方向** —— 08-11 / 08-13 两轮换了 `visits` 上限和分类锁定,撞的是同一堵墙

- [x] **2026-08-13 完成** · M4 · 把对标站的冷启动目录补进外链台账渠道池
  - **实际做了**:展开 `describemusic.net` 全部 28 个出站域名 + `cleanaudio.io` 4 个,与既有 120 行逐条比对,
    剔除 4 个重复(Fazier / Uneed / Submit AI Tools / Product Hunt),**写入 27 行,渠道池 120 → 147**
  - **⚠️ 全部未核**:只确认了"这些域名出现在对标站出站链接里",没确认免费/可提交/dofollow。
    提交前必须实访。`twelve.tools` 已标 C1(2026-08-11 实测要求首页反链)
  - **⚠️ Source 字段留空**:加 select 选项要改字段 schema(PUT 全量替换会波及既有 120 行),权限策略拦截且拦得对。
    出处已全部写进 `Notes`(以 `[source=columbus-benchmark-2026-08-13]` 开头)+ `Source URL`
  - **关联**:[backlink-ledger.md 渠道池段](sources/backlink-ledger.md) · [experiments.md 粗筛第二轮](experiments.md#哥伦布对标站粗筛第二轮2026-08-13--已结束结论-no-go但产出两条可复用的东西)

- [ ] **2026-08-13**(承接上条)· M4 · 实访核这 27 个新渠道,优先 `ia-insights.fr`
  - **动作**:开[渠道池](sources/backlink-ledger.md),筛 `Route Type = unverified` 的 27 行,逐个开站看:
    ①有没有公开提交入口 ②免费还是付费 ③已有 listing 是不是 dofollow。回填 `Classification` / `Submission URL` / `Free Status` / `Route Type`
  - **优先级**:`ia-insights.fr` 排第一 —— **它是唯一同时出现在两个对标站出站域名里的**,共现信号强于单次出现
  - **⚠️ 提交数 ≠ 外链数**:台账里 129 次提交只有 5 条 `published`、真 dofollow 仅 2 条。
    **核完再提交,别再往里灌无效提交**
  - **预计耗时**:分批做,首批 10 个约 1 小时

- [ ] **2026-08-13**(优先级低,可直接跳过)· M4 · cleanaudio.io 进 Step 2 验证
  - **动作**:Semrush 查 `audio cleaner` / `noise remover` / `remove background noise` 的意图占比与 KD;
    **同时做去 `visits` 上限的赛道竞争复查**(08-11 教训,不可跳过)
  - **⚠️ 预期通过率低**:它是 5 个候选里唯一定价健康的($16.99/mo + 积分包、广告网络为空、输出进播客/视频剪辑工作流),
    但头部词 CPC 仅 **$0.19–0.53**、印度占比 **35.9%** 高于美国。**按上面那条 CPC 闸门,它大概率在 Step 2 被否。**
    列在这里是为了留一个可证伪的记录,不是因为看好它
  - **预计耗时**:40 分钟

- [ ] ~~**2026-08-09** · 注册 Sudowrite 联盟 + 发 `best ai for novel writing` 长文~~ — **2026-08-10 作废**,Waffo 通道打通后变现载体从联盟换成自有收款,联盟路径整体降级(数据保留在 [experiments.md](experiments.md))

- [x] **2026-08-15 上线** · M4 · partfit3d 新建 `/tools/stl-repair` 页面
  - **原动作**:一页一词族,主攻 `stl repair`(1,900/月 KD18)+ `stl fixer`(1,000/月 KD14)+ `repair stl files`(720/月 KD9),TDK 命中 "free online stl repair tool"
  - **为什么排第一**:量级(9,000+/月)与转换词族(11,190/月)相近,但 SERP 实查后**竞争强度差一个量级**——转换词前排卡着 zamzar.com(687万月访问通用权威站)+ meshy.ai(融资公司),修复词前排全是与 partfit3d 同量级的 indie 单功能工具站。KD 数字接近但真实难度不同,详见 [experiments.md 2026-08-14 赛道扫描](experiments.md#结果记录)
  - **难度交叉验证**:`gefei-kd` + Trends + Ahrefs 三源确认过——难度分 30.2(三词最低)、最弱竞品 `justfixstl.com` 只用 10 个 dofollow 域名就排第 2,门票是三词里最低最扎实的。但盘面标注这是"专门死磕这个词的红海",产品质量要跟上,别只求有页面。详见 [experiments.md 2026-08-15 交叉验证](experiments.md#结果记录)
  - **✅ 已实测确认(2026-08-15)**:页面已上线且**优于预期**——完全浏览器内处理(无需上传),不是退而求其次的服务端方案;TDK 与本轮规划完全吻合(`Repair STL Files Online — Fix Holes & Flip Normals`);检测破洞/非流形边/内翻壳体/重复面,一键修复;导航已加 `STL Repair` 入口
  - **下一步**:提交 GSC 索引(参照 partfit3d TDK 实验的流程,先手动点"请求编入索引"),4-6 周后拉曝光/点击数据核实词是否真实带来流量
  - **关联**:[experiments.md 2026-08-15 交叉验证](experiments.md#结果记录)

- [x] **2026-08-15 完成** · M4 · `/tools/stl-repair` 提交 GSC 索引
  - **实测确认**(`gsc.py inspect`):`coverageState` = **已提交,且已编入索引**,`verdict` = PASS,`robotsTxtState` = ALLOWED——收录本身没问题
  - **⚠️ 发现一个眼熟的信号,待查**:`googleCanonical` 是 `https://partfit3d.com/tools/stl-repair`(不带斜杠),
    但 `userCanonical`(页面自己声明的)是 `https://partfit3d.com/tools/stl-repair/`(**带**斜杠)——
    和 08-11 诊断出的 [trailing slash 冲突](experiments.md#结果记录)是同一个模式(canonical 带斜杠 vs 服务器/Google 判定不带斜杠)。
    当时那轮修复是不是没覆盖到新页面模板,还是这页单独遗漏了,需要回去确认;目前 Google 自己判对了(用不带斜杠版本),
    没有阻塞收录,**不紧急,但别当没看见**
  - **内链检查还没做**:`/tools/3mf-splitter-online` 页面正文是否加了链回 stl-repair 的交叉链接,只确认了导航栏有,没查正文
  - **关联**:[experiments.md 2026-08-15 交叉验证](experiments.md#结果记录)

- [ ] **2026-09-中 视 GSC 收录情况定**· M4 · `/tools/stl-repair` 4-6 周数据回收,判定是否达标
  - **动作**:`python3 scripts/gsc.py queries "https://partfit3d.com/tools/stl-repair"`,核对 `stl repair` / `stl fixer` / `repair stl files` 三个词的曝光/点击/位置是否达到预期(参照 justfixstl.com 门票:10 个 dofollow 域名能排第 2,partfit3d 目前 0 外链,预期会比它慢)
  - **判定线**:有曝光但排名靠后 → 正常,继续观察;完全 0 曝光 → 词或收录有问题,回头查;这一步也顺带验证"红海词但 indie 站能打"的假设在自己身上是否成立
  - **关联**:[experiments.md 2026-08-15 交叉验证](experiments.md#结果记录)

- [x] **2026-08-15 完成** · M4 · `3mf to stl` 优先级裁决——用 Ahrefs 查真实 dofollow 引荐域名后解决,**排第二,预算顾虑解除**
  - **原触发**:`gefei-kd` + Trends 交叉验证发现 `3mf to stl` 需求盘子(Trends 相对热度 61)比 `stl repair`(54)更大,
    但 `gefei-kd` 模型给的链接预算(中值 80)比 stl-repair(35)高,一度怀疑要不要动用 $2-5K 新约束外链预算才够
  - **最后确认**:Ahrefs 查最弱竞品 `imagetostl.org` 真实 dofollow 引荐域名 **67 个**(总域名 524,dofollow 占 12.8%),
    比 `gefei-kd` 估算(80)还低,更比"目录型放大到 200-480"温和得多——**67 个域名量级用现有免费渠道池 + outreach
    就有希望够到,不必升级到大站付费预算**,先按免费节奏推进,不够再考虑加钱
  - **对比**:`stl repair` 最弱竞品 `justfixstl.com` 真实只要 10 个 dofollow 域名(DR14、6 个月新站排第 2),
    是三词里门票最低、证据最扎实的一个,继续排第一
  - **最终排序确认**:stl-repair(第一,~10 域名量级)> 3mf-to-stl(第二,~67 域名量级)> glb-to-stl(第三,数据失真见下)
  - **关联**:[experiments.md 2026-08-15 Ahrefs 最后确认](experiments.md#结果记录)

- [ ] **2026-08-14 新增(用户从 Google Trends 自己发现的线索)**· M4 · partfit3d 新建 `/tools/glb-to-stl` 页面
  - **动作**:主攻 `glb to stl`(1,300/月 KD8)+ `.glb to .stl`(390/月 KD5)+ `convert glb to stl`(260/月 KD6),这批词 KD 全部 <11,是三批候选里难度最低的
  - **为什么**:用户看 Trends 三词对比(3mf to stl / glb to stl / image to stl)发现上升相关查询全指向 meshy/tripo(AI 生成 3D 模型的融资公司)——这是 AI 生成 3D 内容爆发带出的下游刚需(生成出 GLB → 要转 STL/3MF 才能打印),处于早期增长阶段,不是存量红海
  - **产品定位**:接在"AI 生成模型 → **GLB 转 STL/3MF** → 修复网格 → 拆分打印机"链路的第二环,与 stl-repair、拆分工具三个页面站内互链,不单独作为独立方向
  - **⚠️ 排序是 agent 判断,未经用户确认**:因 KD 最低暂排在 stl-repair 之后、转换页之前,但绝对量级(2,520/月)明显小于另外两批(9K+/11K+),这是早期押注不是确定收益,用户可按实际精力调整顺序
  - **⚠️ 2026-08-15 数据质量提醒**:用 Ahrefs 查最弱竞品 `magic3d.io` 的引荐域名想再确认一次预算,结果失真(902 个 dofollow 域名)——
    它是多功能大站("Free AI Creative Studio",417 页),glb-to-stl 只是蹭了整站权重的一个长尾页,不能代表这个词的真实门槛。
    **排序维持第三不变**,但真实成本仍未知,上线后只能靠 GSC 实测,不要拿 902 这个数字做任何预算判断
  - **关联**:[experiments.md 2026-08-14(晚)glb to stl 候选发现](experiments.md#结果记录)、[experiments.md 2026-08-15 Ahrefs 最后确认](experiments.md#结果记录)
  - **预计耗时**:1-2 小时(复用现有转换/拆分技术栈)

- [ ] **2026-08-09**(2026-08-11 重新定性,08-14 降为第三梯队)· M4 · partfit3d 新建 `/3mf-to-stl` + `/stl-to-3mf` 两个页面
  - **动作**:一页一词,TDK 精准命中(`Convert 3MF to STL Online Free` 这类),拆分工具做站内互链导流。后端逻辑与现有拆分功能复用率高
  - **为什么**:相邻转换词族 Semrush 口径 ~10K+/月、KD 13-24,比当前词族(实测 ~1,180 曝光/月)约大 8 倍
  - **⚠️ 2026-08-11 定性变更**:原写「`split 3mf` 约 84 曝光/月**是死路**,必须换主攻词」——**前提数字错了**。
    当前词族活着且在涨,这条**从"救命动作"降为常规扩量选择**,与上面的 title/meta 修复**并行,不冲突**
  - **⚠️ 两个第三方源打架**(Semrush `3mf to stl` 4400/KD19 vs 哥飞实测 24000/KD47.9),**不要按任一数字做预期**,上线后用 GSC 验真
  - **关联**:[experiments.md 3MF 词族扩展](experiments.md#结果记录) · [advice 部分采纳](advice/2026-08-09-partfit3d-pivot-or-abandon.md)
  - **预计耗时**:两个页面各 2-3 小时

- [ ] **2026-08-11** · M4 · 回测 KGR/intitle,决定它在 SOP 里留还是删
  - **动作**:对 4 个已知结局的主攻词跑 `intitle:"关键词"` —— `split 3mf`(跑出量)/ `depixelate`(跑出量)/ `all wishes come true`(跑出量)/ `framdrop`(几乎无量),算 KGR,看它能否分辨出这三类。分母取不到的词只记 intitle 绝对值
  - **为什么**:该方法目前在 [SOP Step 2](methods/search-engine-demand-discovery.md) 里挂着 🚧 待验证标记,**不能作 GO 依据**。回测通过才摘标记,不通过就删掉——不留"看着有道理但没验过"的条目
  - **关联**:[advice/2026-08-11-gefei-kgr-intitle.md](advice/2026-08-11-gefei-kgr-intitle.md)
  - **预计耗时**:30-40 分钟(4 次 Google 查询 + 查已有的搜索量数据)

- [x] **2026-08-12 完成** · M4 · 跑 partfit3d 的 `split 3mf` TDK 单页实验(title + description 已上线)
  - **动作**:`/`(即 `/tools/3mf-splitter-online/` 对应首页)title 已改为 `Split 3MF to Fit Your Printer — Free Online Tool`,description 已改为「Fit oversized STL and 3MF models to your 3D printer. Orient, cut, verify every part, and export slicer-ready 3MF or STL files. No uploads or CAD required.」——curl 实读确认已生效
  - **H1 明确不改**:用户 2026-08-12 决定这轮先不动 H1(仍是旧文案 `Split STL & 3MF Files Online / No Uploads Required.`)。原因:H1 不进 SERP 摘要,不影响 CTR,改了也测不出这次实验的效果,反而混淆"CTR 变化到底是不是 title/description 带来的"这个归因。H1 改法已想好(`Auto-Split STL & 3MF to Fit Your Printer` + `No Uploads Required.`),留到这轮 CTR 结果出来后再单独决定要不要做(那时候是奔着降跳出率去,不是奔着 CTR)
  - **验证**:上线后请求重抓;Google 展示新标题后等 14 天,用等长窗口比较 `split 3mf`。平均位置不变差时 CTR ≥1% 算第一档成功,2-3% 为目标
  - **为什么升级**:截至 2026-08-09 最近 7 天该词已有 360 曝光,比前 7 天约 99 曝光增长 264%;旧判断「只多 3 次点击/月」来自新站早期小样本,已失效。按当前曝光,CTR 到 1% 可多约 2-3 点击/周,到 3% 可多约 10 点击/周
  - **SERP 约束**:美区非个性化结果前两名是精确匹配工具站,随后有 AI Overview;当前 PartFit 未稳定在首屏。因此 title 要强调独有结果「fit your printer」,后续仍要并行改善排名,不能把所有低 CTR 都归因于文案
  - **关联**:[experiments.md partfit3d query 级下钻](experiments.md#结果记录)

- [x] **2026-08-15 已不需要**(重抓已自然发生于 2026-08-14T10:20Z,见上)· M4 · ~~去 Search Console 网页版手动点「请求编入索引」~~
  - **动作**:登录 `search.google.com/search-console`,选 `partfit3d.com` property,URL 检查工具输入 `https://partfit3d.com/`,点「请求编入索引」。2026-08-12 用 `gsc.py inspect` 确认 `lastCrawlTime` 还停在 `2026-08-11T00:45`(改动前),说明 Google 还没抓到新标题
  - **为什么现在做**:14 天对比窗口必须从 Google 真正展示新标题开始算,不然会把"旧标题还在跑"的时间也算进实验窗口,拉低看到的效果
  - **预计耗时**:5 分钟

- [x] **2026-08-15 完成** · M4 · 确认 Google 已用新标题重抓 partfit3d
  - **结果**:`gsc.py inspect` 实测 `lastCrawlTime` = **2026-08-14T10:20:46Z**,晚于 08-12 上线时间,**重抓已发生**
  - **因此 14 天对比窗口的真正起点 = 2026-08-14**,终点 08-27;GSC 数据有 2-3 天延迟(逐日实测确认数据只到 08-12),**最早 2026-08-30 才能拉到完整窗口**
  - **关联**:[experiments.md 2026-08-15 TDK 中期检查](experiments.md#结果记录)

- [x] **2026-08-24 完成** · M4 · 决定 TDK 实验的测量口径 —— 双页混合归因问题
  - **问题**:改的是 `/`(新 title),但 `/tools/3mf-splitter-online/` **还挂着旧 title**;同期 `split 3mf` 单词的曝光被这两页分掉
  - **裁决:选 ② —— page 维度只看 `/`,并把 `/tools/3mf-splitter-online/` 当对照组**
  - **⚠️ 修正 08-15 的记法**:当时把 ② 写成「保住归因但**样本减半**」——**这个判断不成立**。旧 title 那页一直没动,它就是同站、同词族、同期曝光同涨的**天然对照组**,page 维度不是减半,是**能做差分**。选 ① 反而会把这个对照组毁掉,因此 ① 明确否掉
  - **08-24 中期数据(9/14 天)已验证 query 维度确实读不出东西**:`split 3mf` 4 点击 / 1515 曝光 / **0.3%** @ 8.8,与基线 0.3% 完全一致 —— 混合归因污染兑现
  - **关联**:[experiments.md 2026-08-24 TDK 中期读数与口径裁决](experiments.md#结果记录)

- [ ] **2026-08-30** · M4 · 回收时按差分口径拉两页,并记录两页位置变化
  - **动作**:`gsc.py pages` 分别取 `/`(实验组)与 `/tools/3mf-splitter-online/`(对照组)在 before 07-31:08-13 / after 08-14:08-27 两窗的 点击 / 曝光 / CTR / 平均位置,做差分
  - **为什么要记位置**:08-24 中期读数里两页平均位置**走向相反**(`/` 10.3→9.1 变好,对照 9.6→10.4 变差),位置变化本身能解释一部分 CTR 差,**不记位置的差分不干净**
  - **关联**:上一条口径裁决 · [experiments.md 2026-08-24 中期读数](experiments.md#结果记录)

- [ ] **2026-08-30**(08-15 按实际重抓日 08-14 改准)· M4 · 回收 partfit3d TDK 实验数据,判定 GO/NO-GO
  - **动作**:`python3 scripts/gsc.py compare https://partfit3d.com/ --before 2026-07-31:2026-08-13 --after 2026-08-14:2026-08-27`,**按 08-24 定好的口径 = page 维度只看 `/`**(不是 query 维度)
  - **⚠️ 基线跟着口径换(2026-08-24 重锁)**:page 维度 `/` 改前 07-31~08-13 = **15 点击 / 960 曝光 / CTR 1.6% / pos 10.3**。
    ~~08-15 锁的 query 维度 `split 3mf` 基线 1,245 曝光 / 4 点击 / 0.3% / pos 9.1~~ —— 那是混合归因口径,**换 page 维度后作废**
  - **对照组基线**:`/tools/3mf-splitter-online/` 改前 = 12 点击 / 1644 曝光 / CTR 0.7% / pos 9.6
  - **判定线**:平均位置未明显变差 + CTR ≥1% = 第一档成功;≥2-3% = 目标线;若 CTR 仍 <0.5% 且位置未变,判定文案不是主因,回头看 SERP 结构
  - **⚠️ 判定纪律(防自我欺骗)**:曝光爬坡期新增的多是长尾低意图曝光,**天然压 CTR**。**不能只看 CTR 百分比,必须同时看点击绝对数** —— CTR 持平但点击明显上升,不判 NO-GO;CTR 上升但曝光腰斩,也不算 GO
  - **⚠️ 2026-08-25 追加的硬约束(必须写进判定)**:`split 3mf` 的 SERP 意图是「按颜色拆分上色 3MF」,
    partfit3d 只做「按平面切开」——**即便读出 GO,CTR 天花板也被意图错配锁死,不能把 GO 外推成
    「这套文案可以复制到别的词」**。TDK 从"主要抓手"降级为"顺手做过的一次微调";
    真正的抓手已转为[颜色拆分功能](experiments.md#partfit3d-颜色拆分功能a-路线2026-08-25-立项)。
    依据见 [experiments.md 2026-08-25 词族意图诊断](experiments.md#结果记录)
  - **结果无论好坏都要回写**:[experiments.md](experiments.md#结果记录) 结果记录段 + 本文件对应条目转 done/blocked
  - **预计耗时**:15 分钟

- [x] **2026-08-15 提前完成**(原定 08-18)· M4 · 确认 ~3,780 曝光/月 是水位还是尖峰 —— **不是尖峰,还在往上走**
  - **非重叠周对比**(`split 3mf`):07-30~08-05 **219 曝光 / 0 点击 / pos 9.7** → 08-06~08-12 **1,026 曝光 / 4 点击 / CTR 0.4% / pos 8.9**,**+369%**,而位置只微升
  - **排除了数据回填的可能**:复拉 08-02~08-08 得到 276 曝光,与 08-11 当时记录的数字**完全一致** → 是真实增长,不是 GSC 延迟回填造成的错觉
  - **含义**:[experiments.md 08-11 订正](experiments.md#结果记录)的速率结论**成立且偏保守**,不需要按尖峰改写
  - **关联**:[experiments.md 2026-08-15 TDK 中期检查](experiments.md#结果记录)

- [ ] **2026-08-09** · M4 · 查 partfit3d 品牌词 `partfit` 为什么只排 4.4 位
  - **动作**:自己的品牌名没排到第 1(15 曝光 0 点击),是站点权重/实体识别问题,与 title 无关。查:首页是否有明确品牌实体标记(Organization schema / about 页 / 一致的 brand naming)、`partfit` 这个词是否被其他实体占据
  - **为什么值得单列**:品牌词排不上第 1 通常意味着 Google 还没把这个站当成一个"实体",影响的是整站信任信号,不只是一个词
  - **预计耗时**:1 小时

- [ ] **2026-08-25** · M4 · 回查 partfit3d 免费目录外链审核状态
  - **动作**:检查 Startup Collections 与 [WebsiteHunt](https://www.websitehunt.co/websites/partfit-3d) 是否通过审核、是否形成可抓取直链;结果直接更新[外链台账](sources/backlink-ledger.md)「④ 到期回核」视图里那两行的 Status / Link Attribute,不再单独回写 experiments.md
  - **降级路径**:若仍未上线,不付费插队,转向 3D-printing 资源页 outreach / Show HN(需现成 HN 登录)
  - **预计耗时**:15 分钟

- [ ] **2026-08-13** · M4 · 回核外链台账里 99 行 `link_attr = unknown`(**外链这条线 ROI 最高的一个动作**)
  - **动作**:开[外链台账](sources/backlink-ledger.md)「② 待回核 link_attr 未知」视图,逐条查 listing 是否已公开、链接是不是 dofollow,回填 Link Attribute / Published At / Indexed。优先查 `Evidence Type = public_url` 和 `receipt` 的行(有凭据,最可能已上线),`none` 的行直接判死
  - **为什么**:129 次提交里 `published` 只有 5 条、dofollow 只有 2 条,而 77% 的行连是不是 dofollow 都没核过。**不核就永远不知道这两个月的外链投入有多少是白干的**,也没法判断该不该继续投免费目录这条路
  - **预计耗时**:分批做,首批 20 行约 1 小时

- [x] **2026-08-25 完成**(2026-08-11 立项)· M4 · 修 partfit3d 的 trailing slash 冲突(**解 34 条未收录,ROI 最高**)
  - **✅ 已部署验证(生产实测 2026-08-25)**:commit `76432be`,Worker 版本 `93dd1b48`。
    `/tools/stl-repair/` → **301** → `/tools/stl-repair`;canonical 与 og:url 均**不带**斜杠、与 200 地址一致;
    sitemap 全部 `<loc>` 去斜杠且根路径保留 `/`;`/` 不跳转
  - **307 根因**:不是 Cloudflare,是 TanStack Router —— `router-core/dist/esm/redirect.js:3` 的
    `statusCode = ... || 307`,**无配置开关**。解法是在 Worker 入口 `src/server.ts` 于请求进 router 前拦截返回 301,
    守卫:根路径不跳、只对 GET/HEAD 用 301(POST 用 301 会被客户端改写成 GET)
  - **og:url 无需单独修**:`seo()` 一次算出 url 同时喂 canonical / og:url / twitter:url,改一个函数覆盖全部
  - **下一步**:GSC 重新提交 sitemap;约 2-4 周后复查 9 对重复 URL 是否合并、`how-to-split-stl-for-3d-printing`
    合并后的位置(合并前 249+244 曝光分别趴在 pos 44.1 / 41.8)

  - **⚠️ 拖了 4 个数据周期的真正原因:不是"没修",是"修完忘了发"。**
    `src/lib/urls.ts` 与 `src/routes/sitemap[.]xml.ts` 的去斜杠逻辑早就写好,只是从未提交(working tree `M`),
    线上一直跑旧构建。08-11 诊断 / 08-15 复现 / 08-24 复现 / 08-25 再复现,每次都当成"还没做"
  - **关联**:[experiments.md 词族意图诊断 ⑤](experiments.md#结果记录)

- [x] **2026-08-25 完成** · M4 · 发布 partfit3d 两个转换页(**同样是"写了没发"**)
  - **✅ 生产实测**:`/tools/3mf-to-stl`、`/tools/stl-to-3mf` 均返回 200,已进 sitemap;
    `/tools/3mf-splitter-online` 加了指向两页的内链
  - **为什么**:08-14 定的转换词族(`3mf to stl` 合计 ≈11,190/月,KD 13-17)页面早就写好了,一天曝光都没吃到
  - **未提交**:这两页及 `converter-workspace.tsx` / `stl-export.ts`(共 1,064 行)仍是未跟踪文件 ——
    **已部署但未入 git**,下次改动前先补一次提交
  - **下一步**:GSC 手动请求编入索引,4-6 周后拉曝光核实转换词族是否真实带量
  - **关联**:[experiments.md 词族意图诊断 ⑤](experiments.md#结果记录)
  - **预计耗时**:30 分钟

- [ ] **2026-08-25** · M4 · A 路线 Step 0 · 补查颜色拆分词族量级(**不再阻塞独立页,只校准 SEO 预期**)
  - **动作**:用 `seo-competitor` 查 `3mf color splitter` / `split 3mf by color` / `separate colors 3mf` /
    `3mf color separator` 的量级与 KD,决定是否另开 `/tools/3mf-color-splitter/` 独立页
  - **动作出口**:决定做「一页两模式」还是「一页两模式 + 独立页」
  - **关联**:[experiments.md partfit3d 颜色拆分功能](experiments.md#partfit3d-颜色拆分功能a-路线2026-08-25-立项)
  - **预计耗时**:30 分钟

- [x] **2026-08-26 完成** · M4 · A 路线主体 · 实现颜色解析 + 按色分组 / 封盖 / 导出,上线独立页
  - **生产验收**:`/tools/3mf-color-splitter` 的站内三色样例可拆出 3 个 watertight parts;colour-tagged 3MF 与 3 STL ZIP 下载均进入可用状态
  - **范围边界**:目前只上线独立页;已有约 3,000 曝光/月的 `/` 与 `/tools/3mf-splitter-online` 尚未承接颜色功能,所以原 CTR 假设还没有开始验证
  - **下一步**:08-30 回收旧 TDK 数据后,给两个已有曝光页接入颜色入口,并从该次上线日重新锁 14 天窗口
  - **关联**:[experiments.md partfit3d 颜色拆分功能](experiments.md#partfit3d-颜色拆分功能a-路线2026-08-25-立项)

- [ ] **2026-08-11** · M4 · 修 partfit3d 三类链接生成 bug(**25 个 404 的真正成因**)
  - **动作**:① `$slug` 未插值(14 条)—— 查 `/printers` 列表页链接生成 ② 相对链接缺前导斜杠导致路径段重复(8 条)—— 全局搜 `href="` 后不是 `/` 或 `http` 的 ③ route group 括号泄漏(3 条)—— `(pages)` `(legals)` 不该出现在 URL 里
  - **⚠️ 原待办方向是错的**:写的是「能 301 的 301」,但**没有一条是真死链**。改完 bug 让 Google 重抓,25 条自然消失,不需要任何重定向
  - **前置**:同上,需要仓库路径
  - **预计耗时**:1-2 小时

- [ ] ~~**2026-08-09** · 清理 partfit3d 的 25 个 404~~ — **2026-08-11 拆分并修正**,见上面两条(诊断发现零死链,是链接生成 bug + trailing slash 冲突)

- [ ] **2026-08-09** · M4 · 定工具站的变现路径(**决策项,阻塞其他扩量动作**)
  - **动作**:确认 AdSense 当前状态(已申请?已过?被拒?);若工具站过审困难,评估替代路径:内容站 baxianfans 单独申请 AdSense / 工具站走付费额度 / Lemon Squeezy
  - **为什么优先**:原计划的 AdSense 假设建立在"内容站"上,实际 3/4 是工具站,**这个决定影响后面所有动作的方向**
  - **预计耗时**:1 小时调研 + 1 次决策

- [ ] **2026-08-11** · M4 · 修 baxianfans 的 soft 404 catch-all + 无效 sitemap
  - **动作**:① 让不存在的路由真正返回 404(现在任意 URL 返回 200 + 首页内容 + canonical 指向首页)② 让 `/sitemap.xml` 输出真 XML(现在 `content-type: text/html`,被 catch-all 吞了,**GSC 读不到**)
  - **⚠️ 修正原动作方向**:原待办写「补内容厚度 + 内链」,对 baxianfans 无效 —— 根因是站点没有多页结构 + sitemap 无效,不是内容薄
  - **关联**:[experiments.md 四站 URL 规范化横向体检](experiments.md#结果记录)
  - **预计耗时**:1-2 小时

- [ ] **2026-08-09** · M4 · 提 aidepixelate / easyframes 收录率
  - **动作**:两站 URL 规范化已实测正确(canonical / sitemap / 重定向三方一致),**排除了配置问题**,未收录才可能真是内容厚度/内链问题。补内容 + 内链 + 重新提交 sitemap
  - **预计耗时**:每站 2-3 小时

- [ ] ~~**2026-08-09** · 提三站收录率~~ — **2026-08-11 拆分**,baxianfans 是配置问题另立一条,另两站保留原动作

- [ ] **2026-08-09** · IP · 把 4 站上线全过程补成内容
  - **动作**:真实素材已经有了(选词换轨、7 月才收录、CTR 0.6% 的坑),X 停在 1 条。先发 1 条:"4 个站,1338 次曝光,31 次点击 —— 排名不是问题,点击才是"
  - **预计耗时**:30 分钟/条

### blocked

- [ ] **2026-08-26** · M5 前置 · $500 投放测试验 A 型转化率
  - **动作**:$500 × CPC $0.20 = 2,500 点击。若 1% 转化到 $10/月订阅 = 25 订户 = $250/月,两个月回本。
    **这是本项目第一个能产出「转化率真值」的动作**——目前所有转化假设都是第三方估算外推
  - **⛔ 阻塞原因**:[timeline.md 2026-08-12](timeline.md) 定的 **$2–5K/站外链预算,至今 14 天一分未花**,
    每一轮筛选实际仍按「免费能不能做到」跑。这笔钱是真能花还是纸上的,**未确认**
  - **解阻条件**:用户明确回答三选一 —— ①钱是真的可以花 → 本测试立即跑,且整个筛选函数按新预算重写;
    ②钱是纸上的 → **撤回 08-12 框架**,别让它继续在 timeline 里制造错觉;③要先见到第一笔收入才肯花 →
    优先级让给 [fast-payment-validation](methods/fast-payment-validation.md) 的 Fiverr 路径
  - **⚠️ 选词不可抄 A 型**:买别人商标词的位置,风险和窗口都不在自己手上;用 B 型思路选词
  - **关联**:[experiments.md 第五站补跑](experiments.md#第五站候选筛选与付费意愿验证m5-前置2026-08-26)

### 已作废(2026-08-26)

- ~~注册 3D 打印服务联盟,在拆分完成页加 CTA~~ — **2026-08-26 撤销,同日提出同日否掉**。两个问题:
  ①**受众反了**——会来拆分模型的人,是因为模型放不下**自己的**打印床,他拆分恰恰是为了自己能打;颜色拆分用户更是一定有 AMS 多色打印机;
  ②**分母不够**——54 点击/月(A 路线 GO 后乐观 ~100),漏斗算下来 0.02–0.18 单/月,14 天窗口期望值 0.01–0.09 单,**这个测量点测不出任何东西**
- ~~aidepixelate 换词族到 photo restoration + 投放广告验证~~ — **2026-08-26 判 NO-GO(用户选 C)**。
  Etsy 实测:全价位段($8 / $24.5 / $28)卖家**一致强调「by hand / not AI」**,Bestseller 原话
  「restored by the real person, quality miles ahead of anything AI tools can offer」,且他们自己把 AI 当内部工具。
  **市场已把 AI 修复定价为 0,溢价全部归给「不是 AI」。** 广告侧另有独立否决:$4.90 客单价配 ~$2 CPC,CAC 20 倍倒挂。
  → **aidepixelate 停,Waffo 收款底座保留备用。** 详见 [experiments.md 2026-08-26 选词复盘](experiments.md#结果记录)

### 已作废(2026-08-09)

- ~~等用户提供下一个热词候选跑三维探针~~ — 实际选词已换轨到极长尾工具词,不再走热词路径
- ~~选词前置做分发生态自检~~ — 判断已内化,4 站选词均未踩该坑
- ~~切美区 IP 跑 SERP 维度~~ — 建站已跑通,该阻塞不再挡路

## 最近完成(近 14 天)

- [x] **2026-08-26 完成** · M4 · 修 partfit3d 颜色拆分的 Prusa 三个 bug + 提交 10 个未跟踪文件
  - **修复**:① `Slic3r_PE.config` filament 颜色按原 slot index 映射(`three-mf-color.ts`)② 拓扑判定扩为 `multiplicity`(`color-splitter.ts`)③ `mmu_segmentation` source label 区分(`three-mf-paint.ts`)
  - **顺带止损**:整个颜色拆分功能(路由页 / 解析 / 封盖 / 转换页共 10 个文件)此前**从未提交过 git**,线上活着但代码只在工作区。已提交 `2a25698`,工作区清空。**这是「写了没发」同型问题第 5 次**
  - **⚠️ 未完成**:复跑夹具验证(已移入 doing)

- [x] **2026-08-26 完成** · M4 · 接入并内化 payment-growth 数据源
  - **产出**:`scripts/payment-growth/`(vendored,CLAUDE.md 零依赖约定的明文例外)+ `payment-growth` skill + [手册 8 条陷阱](sources/payment-growth.md);`seo-competitor` 新增 SimilarWeb API 直连作 KD 第三口径
  - **本地 3 个补丁**:py3.9 `fromisoformat` 小数秒崩溃 / traffic-trend 批量+退避重试 / env 候选链加 `~/.config/shark-agent/.env`
  - **首轮实战**:四平台 8/8 完整快照(4,908 行),品类涨跌 + 6 个候选(全部挂起);实战修订了 2 处 SOP 设计缺陷
  - **沉淀**:[principles.md 用 CPC 分层识别付费意愿](principles.md) + [risks.md 免费 loss-leader 挤压 / 做在被定价为 0 的那一层](risks.md)

- [x] **2026-08-11 完成** · M4 · 找 1 个 Build in Public「卖铲子」方向
  - **结果**:首选「SEO 工具站 Starter Kit + 自动防错规则」进入 48 小时预售验证;不是直接 GO。
  - **证据**:TrustMRR 验证收入 + 哥伦布增长产品 + 官网价格交叉;淘汰 App 拒审预检、RevenueCat doctor、通用移动 UI kit。
  - **关联**:[experiments.md](experiments.md#seo-工具站-starter-kitbip-卖铲子2026-08-11-桌面筛选完成)

- [x] **2026-08-09 完成** · M4 · GSC API 授权打通
  - **过程**:账号开 2SV → 建 GCP 项目 `shark-gsc` → 启用 Search Console API → 配 OAuth 同意屏幕(外部/测试,加测试用户)→ 建桌面客户端 `shark-gsc-cli` → `gsc.py auth`
  - **验证**:`sites` 返回四站均 `siteOwner`;`ctr-losers` API 结果与当天 ego 爬网页版结果**词序与量级一致**,两条路径互为交叉验证
  - **注意**:测试模式下 refresh_token **有效期 7 天**,过期重跑 `auth` 即可

- [x] **2026-08-09 完成** · M4 · 搭 GSC 取数链路 + 跑出 partfit3d 漏损队列
  - **产出**:[`scripts/gsc.py`](../scripts/gsc.py)(6 子命令,零依赖)+ [`sources/gsc.md`](sources/gsc.md) 手册;协议层加「数据源使用纪律」信任分级
  - **API 路径受阻**(见 blocked),改用 ego 读 GSC 网页版补齐数据,结论同样落盘
  - **结果**:漏损队列已出,但**最大收获不是队列本身**——是发现 CTR 修复天花板只有 ≈10 次点击/3 个月,整站建立在一个词的拼写变体族上。详见 [experiments.md partfit3d query 级下钻](experiments.md#结果记录)

- [x] **2026-05-02 完成** · SEO M1 · 羽毛球教学/装备 8 个候选词 Step 1+2(Trends + Ahrefs Free)
  - **结果**:**0/8 通过红线**——7 个 "No keyword ideas",最强商业词 `best badminton overgrip` 也 < 100/月。**整个赛道 NO-GO,本方向归档**
  - **教训**:① dogfood 触感 ≠ Google 搜索量;② 垂直运动(亚洲主流非英语区)+ 英文教学型 SEO = 三重生态错配陷阱
  - **沉淀**:[risks.md 新条目](risks.md#垂直运动--英文教学装备型-seo-内容站陷阱亚洲主流运动尤甚) + [talks 6 段最终结论](talks/2026-05-02-overseas-badminton-community-idea.md#最终结论本方向-no-go归档)

- [x] **2026-05-01 完成** · SEO M1 · `GPT Image 2` 候选词三维探针(Trends + Ahrefs)
  - **结果**:**整个候选池 NO-GO**——父级与 12 个变体全部 <100/月,触发 SOP 红线
  - **教训**:社交热度 ≠ 搜索热度,X 曝光不等于 Google 搜索量
  - **回写**:[experiments.md 候选关键词池](experiments.md#候选关键词池待-step-2-3-验证) `GPT Image 2` 段已更新

---

## 内容输出节奏(持续型 TODO)

> 与上面一次性 TODO 区分:推文/长文是节奏驱动的循环输出,单独追累计进度。

### 当前周期(2026-08 重启)

> **2026-05-01 ~ 05-14 周期已作废**:实际停在 X `1/12` · 长文 `0/1`,之后 3 个月无记录。IP 实验事实上暂停了一个季度,精力全在建站上。**这不算失败——建站跑通了,而且现在攒下了真实素材**。

- **起止**:2026-08-09 ~ 2026-08-22(待用户确认是否重启)
- **目标**:待定,建议**降门槛重启**——原来 12 条/2 周的目标在 4 站并行时不现实,先定 X ≥6 条/2 周
- **进度**:X `0/?` · 长文 `0/?`
- **素材库(现成的,不用编)**:4 站上线全过程 / 选词从热词换轨到极长尾 / 7 月才收录的等待期 / CTR 0.6% 的第一页陷阱 / 工具站 vs 内容站的变现差异
- **节奏触发**(来自 [timeline.md](timeline.md#节奏提醒触发条件)):
  - 周中检查:若 X 周更新 < 5 条或连续 2 天断更 → 砍小红书/公众号,保 X
  - 周期末检查:若 X < 12 条 → 重新校准 [profile.md 硬约束](profile.md#硬约束)

### 待发推文(草稿队列)

> 已成型草稿(2026-04-29 提交,见 [drafts/x/2026-04-29-direction-iteration.md](../drafts/x/2026-04-29-direction-iteration.md))。**起点 2026-05-01,所有发出后回填到下方「本周期已发」表 + 进度计数 +1**。
> 10 条首发选题清单见 [experiments.md X 首发框架](experiments.md#x-首发框架)。
> **起草 SOP**:每条按 [methods/x-tweet-writing-templates.md](methods/x-tweet-writing-templates.md) 走 Step 1-5;发布前过三问(钩子 / 带走什么 / 换名字还成立吗)。

| # | 草稿 | 类型 | 目标结构 | 推荐开头型 | 计划发布 | 状态 |
|---|---|---|---|---|---|---|
| 2 | 单条原则:Web 产品别用 App 评论挖需求 | 单条 | 认知颠覆 | 直接宣言型 | 2026-05-01(周五,首发) | ✅ 已发 2026-05-02 |
| 1 | 决策迭代线程(5 条):4 月主线 4 次推翻 | Thread | 故事型 Thread | 数字锚定型(4 次推翻+留白) | 2026-05-04(周日) | 待发 |
| 3 | App vs Web 路径数据对比 | 图文/表格 | 对比分析 | 数字锚定型 | M2 前段(SEO 站第一篇上线时) | 待发(M2) |
| 4 | 支付通道现实(Stripe/Lemon/AdSense) | 单条引讨论 | 框架输出 / 认知颠覆 | 反差型 | M2 前段 | 待发(M2) |

### 本周期已发(滚动)

| 日期 | 平台 | 主题 / 一句话 | 结构 | 链接 | 反馈(互动/线索) |
|---|---|---|---|---|---|
| 2026-05-02 | X | Web 产品别用 App 评论挖需求(草稿 2 v2) | 认知颠覆 + 直接宣言型 | [推文](https://x.com/gserpit/status/2050590833922224538) | *(待观察)* |

### 长文 / 阶段总结

| 计划周末 | 主题 | 来源 | 状态 | 链接 |
|---|---|---|---|---|
| 2026-05-04 (周日) | 4 月主线 4 次推翻 — 决策迭代复盘 | 草稿 1(线程 5 条) | todo | - |
| 2026-05-11 (周日) | *(待选,可从首发选题 10 条挑)* | - | todo | - |

---

## 维护规则

- 每条 TODO 至少含:**日期 / 关联(实验或主线) / 具体动作**
- `blocked` 必须标原因 + 解阻条件,否则会变成"看着没动但不知道为啥"的僵尸项
- `done` 14 天后清理,重要结果同步到对应 experiment 的「结果记录」段
- 一个 TODO 拖延超过 2 周仍是 todo → 应该回头问:**它是不是其实不重要**?或者**是不是应该升级成 experiment**?
- **推文每日发完**:把当条加到「本周期已发」表 + 累计数 +1;周期结束时整体清空,只保留最有反馈的 1-2 条作为存档线索
