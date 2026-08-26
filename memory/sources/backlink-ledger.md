# 外链台账(飞书 Base)

> **这不是数据源,是台账。** 记录「我们对外发了哪些外链、现在什么状态」,唯一真值是**可核验的公开
> listing URL**,不是提交回执。第三方给的 DR / Authority 值一律标来源 + 日期,按
> [CLAUDE.md 数据源使用纪律](../../CLAUDE.md) 归到「第三方估算」层。

**动作出口**:回答两个问题 —— ①哪些渠道到期该回核了(Review Due);②哪些渠道白干了、下次别再投
(Status=blocked / Link Attribute=nofollow)。答不上来就不要打开这张表。

## 1. 数据在哪

台账本体在飞书 Base(建表后把 token 回填到下面「Base 坐标」),行级数据由
[`scripts/backlink_ledger.py`](../../scripts/backlink_ledger.py) 从三个源归一化生成:

| 源 | 路径 | 内容 |
|---|---|---|
| partfit3d 提交流水 | `partfit3d/artifacts/seo/backlink-submissions-2026-07-31.jsonl` | 42 行,2026-07-31 → 08-07 |
| aidepixelate 提交流水 | `ai-image/research/backlinks/aidepixelate-2026-07-28/results.jsonl` | 84 行,2026-07-28 → 08-10 |
| shark 记忆补录 | 脚本内 `MANUAL_ROWS`(出处 [experiments.md](../experiments.md)) | 3 行,2026-08-11 那批 |
| 渠道池 | 上述两个项目的 `candidate-pool.csv` / `*-queue-*.csv` 共 5 份 | 120 行候选,含未提交原因 |

**源文件只读**,脚本不改它们;所有修正只发生在导入到 Base 的过程中。

```bash
python3 scripts/backlink_ledger.py build --stats
```

产物落 `artifacts/backlink-ledger/`(已 gitignore,可随时重建):`fields.json` 建字段用,
`submissions.batch*.json` / `channels.batch*.json` 是 `+record-batch-create` 的 `--json` 载荷,
`manifest.json` 记本次归一化的行数与全部告警。

## 2. Base 坐标

| 项 | 值 |
|---|---|
| 链接 | https://my.feishu.cn/base/OXvxbwoPDattP9sGAbPcZmNjnWb |
| Base token | `OXvxbwoPDattP9sGAbPcZmNjnWb` |
| 表 `外链记录` table_id | `tblBIw6xH6sLPn5c`(129 行) |
| 表 `渠道池` table_id | `tbleU8fQxMCFmOTi`(**739 行**,2026-08-26 从 147 增补 592) |
| 身份 | `--as user`(Base 属个人云空间,bot 身份看不到) |

视图(建于 2026-08-13):`外链记录` 默认视图按 Site 分组 + Recorded At 倒序;
另有 `① 已上线 published` / `② 待回核 link_attr 未知` / `③ 失败受阻` / `④ 到期回核`(Review Due 非空)。
`渠道池` 有 `未提交候选` / `A 级可直提`;2026-08-26 增建 `⑤ 悬赏榜 2026-08-26`(`vewXFqDOPp`,592 行)
与 `⑥ 悬赏榜 ≥2票 未入池`(`vewwjwkGZk`,**140 行**,按 `Bounty Votes` 倒序)。

⚠️ **`未提交候选` 视图已被稀释**:它按 `Submitted` 未勾选筛选,592 行悬赏数据全部落在里面。
要看你自己评估过的那批,改用 `A 级可直提`,或加 `Source URL 为空` 条件。

## 3. 字段含义(只列不自明的)

**外链记录**

| 字段 | 含义 / 坑 |
|---|---|
| `Status` | `published` 才算数。`pending_review` 是提交进了队列,`send_clicked` 是邮件发出去了没回音,`send_unknown` 是点了提交但页面没回执,`blocked` 是被墙/要付费/要登录做不下去 |
| `Link Attribute` | `dofollow` 才传权重。`tracking_redirect` 指目录站用站内跳转(如 WebsiteHunt `/go/23356/`)而非直链,权重≈0,**不要跟 dofollow 混算**。⚠️ **只有 `Status = published` 时这个值才是实测的**;其余状态下是平台声称或从目录现有条目推断的**预期值**(全表 18 行 dofollow 里只有 2 行是 published)。统计真实外链一律先按 Status 过滤 |
| `nofollow` 的行 | **照记不删**。三个理由:避免重复提交同一渠道、nofollow 仍有品牌信号与真人流量(如 DEV / Hashnode 的原创技术文)、它是「提交 N 次换回几条 dofollow」这个分母的一部分 |
| `Classification` | 候选池分级:A 免费直提 / B 需邮件或人工 / C 有条件 / D 受阻或不可用 |
| `Evidence Type` | 证据强度排序:`public_url` > `receipt` / `review_id` > `send_click` > `none`。`none` 意味着这行**没有任何可核验凭据** |
| `Recorded At` | 已统一转 UTC+8。源文件里混着 `Z` / `+00:00` / 纯日期三种格式 |
| `Review Due` | 回核到期日。到期动作:查 listing 是否上线 → 核 `Link Attribute` → 核 `Indexed` |
| `Site Corrected` | 见下方陷阱 1。为 `true` 的行,`Submitted URL` 不可信,回核以 `Platform URL` 为准 |
| `Cost USD` | 目前全为 0。付费插队($10 Startup Collections / $99 Launching Next)都拒绝过 |

**渠道池**:记评估过但**没提交**的渠道及原因,价值在于下次换站做外链时不重复踩坑。
`Submitted` 勾选表示该渠道已出现在「外链记录」表(按平台名归一化后交叉匹配)。

> **2026-08-13 增补 27 行(第二来源:对标站反推)**。前 120 行来自两站自己的候选池评估;
> 这 27 行来自[哥伦布对标站粗筛](../experiments.md#哥伦布对标站粗筛第二轮2026-08-13--已结束结论-no-go但产出两条可复用的东西)——
> 扒 `describemusic.net`(12 个月 → 147.2K 月访问)和 `cleanaudio.io`(5 个月 → 76.5K)详情页的**出站域名**字段,
> 得到它们冷启动实际用过的目录。**价值在于「有人用这批跑通过」,不是又一份目录名单。**
>
> 识别方式:`Platform` 是裸域名(前 120 行是友好名)、`Notes` 以 `[source=columbus-benchmark-2026-08-13]` 开头、
> `Source URL` 指向哥伦布详情页。四个与既有池重复的已剔除:Fazier / Uneed / Submit AI Tools / Product Hunt。
>
> ⚠️ **这 27 行全部未核**:`Route Type=unverified`、`Classification` 为空、`Submission URL` 为空 ——
> 只确认了"这些域名出现在对标站的出站链接里",**没有确认它们免费、可提交、或给 dofollow**。
> 提交前必须实访。唯一有先验的是 `twelve.tools`(标 C1):2026-08-11 partfit3d 轮次已实测**要求首页反链**。
>
> `ia-insights.fr` 是唯一同时出现在两个对标站出站域名里的,共现信号强于单次出现,值得优先核。
>
> **2026-08-26 增补 592 行(第三来源:web.cafe 悬赏榜众包)**。来自哥飞站的悬赏
> [「网站上线之后,你会去哪些地方提交外链?」](https://new.web.cafe/ask/bounty/wlhmhdaoqg)——
> 已开榜,181 人参与、592 个选项、701 条推荐理由。页面是 JS 渲染的,WebFetch 拿不到,用 ego-browser 扒
> (含点开 4 个「展开全部 N 条推荐理由」折叠区)。归一化脚本不管这批,载荷留在
> `artifacts/backlink-ledger/bounty/batch{1,2,3}.json`(已 gitignore,可重建)。
>
> 识别方式:`Source URL` = 悬赏页 URL、`Notes` 以 `[source=webcafe-bounty-2026-08-26]` 开头、
> `Route Type=unverified`、`Classification` 为空。新增 `Bounty Votes` 数字字段(`fld0DaSryP`)存推荐票数,
> 其余 147 行为空。
>
> ⚠️ **这是本表信任度最低的一批,属「他人观点」层**。免费/收费、dofollow/nofollow、DR 数值
> **全部是推荐人自述**,没有一条经过实访核验。而且 **592 条里 420 条是单票**——长尾没有交叉验证。
> 真正有多人背书的是 `⑥` 视图那 140 条(≥2 票且不与既有池重复);其中 68 条 ≥3 票,是唯一值得先实访的子集。
>
> 46 行域名与既有 147 行重复,**没有删,而是打 `Duplicate Status=dup-existing-pool`**——
> 悬赏行带票数和理由,既有行带 Classification,两边信息互补。回核时以既有行为准。
>
> 30 行没有 URL 也没有域名(`Notes` 带 `[no-url]`)。其中一部分压根不是站点而是打法描述
> (如「博客评论区」「看竞品在哪里提交」「导航站」),**当渠道用之前先看一眼 Platform**。
>
> **Source 字段留空是刻意的**:新增 select 选项需改字段 schema(PUT 全量替换,会波及既有 120 行),
> 权限策略拦截且拦得对。若要按来源筛选,需手动在 Base UI 给 `Source` 加一个 `columbus-benchmark-2026-08-13` 选项后回填。

## 4. 已知陷阱

1. **源文件归属字段大面积串位(129 行里 49 行)**。部分行的 `site_name` / `submitted_url` 写成了
   **目录站自己**(如 `Best-AI.org` / `https://findaitool.com/submit-tool`),而不是我们的站。
   每个 jsonl 本来就是单站一轮 campaign,所以**站点归属以源文件为准**,URL 只做交叉校验,
   不一致就打 `Site Corrected`。这类行的 `Submitted URL` 保留原值(可能实为目录页或 listing 页)。

2. **`Link Attribute` 有 99/129 是 `unknown`**(77%)。也就是绝大多数提交连是不是 dofollow 都没核过。
   **不核就永远不知道这些提交里有多少是白干的**——这是这张表最该先补的洞。

3. **提交数 ≠ 外链数**。129 次提交里 `published` 只有 5 条(2026-08-13 视图实读),其中 3 条 nofollow
   (Zearches / DEV Community / Hashnode),**真正 dofollow 的只有 2 条**:Wired Business(aidepixelate,
   但要求挂互链徽章)、noisework(partfit3d,是提交前就存在的自然链)。
   **也就是说两站主动发的 128 次提交,到今天只换回 1 条 dofollow。** 汇报外链进展时不要报 129。

4. **平台名在两张表里对不齐**。提交流水里常带 ` email outreach` / ` submission` 后缀,
   渠道池里没有。脚本用 `norm_platform()` 归一化后再交叉匹配,手工比对时注意。

5. **lark-cli 写这张表的三个坑**(2026-08-26 踩到):`+record-list` 默认输出 **markdown 表格不是 JSON**,
   且没有 `--json` 开关,要解析得自己切 `|`;`--json @file` **只认相对路径**,`/tmp/x.json` 会被拒,
   得先把载荷放进仓库目录再用 `./` 引;`+view-set-sort` 必须传 `{"sort_config":[...]}`,
   文档里说的裸数组形式会报 `sort_config: Provide a value of type array`。
   另外 `base:*` scope 会过期,报 `need_user_authorization` 时跑 `lark-cli auth login --domain base`。

6. **`Evidence URL` / `Platform URL` 混有 `mailto:` 和空值**,所以在 Base 里是**文本字段不是 URL 字段**
   ——URL 字段会因格式校验报 `1254068`。

## 5. 重新同步

两个项目继续发外链后,`results.jsonl` 会长。重跑 `build` 会生成**全量**载荷,直接批量写会产生重复行。
增量同步以 `Attempt ID` 为幂等键:先 `+record-list` 拉现有 `Attempt ID` 集合,再只写新增的行。
(`Attempt ID` 源文件自带;`MANUAL_ROWS` 的由 `site_url|platform|recorded_at` 哈希生成,稳定可复现。)
