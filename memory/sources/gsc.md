# 数据源:Google Search Console

> **定位**:四个站的**自有真实数据**,是全项目唯一的搜索表现真值来源。
> 第三方工具(SimilarWeb / SEMrush / Ahrefs)的数字都是估算,**与 GSC 冲突时一律以 GSC 为准**。
>
> **工具**:[`scripts/gsc.py`](../../scripts/gsc.py),零依赖纯 stdlib,不需要 venv。
> **凭证**:`~/.config/shark-agent/google.json`(仓库外,权限 600,**不进 git**)。
> 与 [GA4](ga4.md) **共用同一次授权**——同一个 GCP 项目下的同一个 OAuth 客户端,scope 里带两个 API。
> 共享层在 [`scripts/_google.py`](../../scripts/_google.py)。旧路径 `gsc.json` 仍可读,只为兼容。

## 使用前提(硬约束)

**每次拉数据前先回答一句:这次查询的结果会落到哪个具体动作?**

答不上来就不要查。三个新信息源(GSC / ego 面板 / 顾问 agent)天然会把节奏拉回「再调研一下」,
而 [timeline.md](../timeline.md) 从 2026-07 起已经是试错阶段。
这条约束对应 [axioms.md](../axioms.md) **公理 6**——用"数据还不够"伪装成理性分析,是最常见的心理卡点形态。

## 一次性配置

> ✅ **已完成(2026-08-09)**,凭证在 `~/.config/shark-agent/gsc.json`,以下步骤**不用再跑**,留作重装时参考。
>
> 实际配置:GCP 项目 `shark-gsc` · OAuth 客户端 `shark-gsc-cli`(桌面应用)· 发布状态「测试」·
> 测试用户已加 `gserpit@gmail.com` · 四站均为 `siteOwner` 权限。
>
> **踩过的坑**:Google Cloud 自 2025-12-25 起强制两步验证(2SV),账号没开时
> console.cloud.google.com **所有页面**都被拦在「无法访问 Google Cloud」,建项目那步就走不了。
> 2026-08-09 开启 2SV 后放行。**这个限制只影响 Google Cloud**,Search Console 网页版从头到尾不受影响。
>
> **测试模式的后果**:应用未经 Google 验证,授权时会出现「未验证应用」警告页(点「继续」即可);
> refresh_token 在测试模式下**有效期 7 天**,过期后重跑 `auth` 即可。要长期免重授权需把应用「发布」到生产状态。

Google Cloud 那几步只做一次,约 5 分钟:

1. 打开 [console.cloud.google.com](https://console.cloud.google.com) → 新建项目(名字随意,如 `shark-gsc`)
2. 「API 和服务」→「库」→ 搜 **Google Search Console API** → 启用
3. 「API 和服务」→「OAuth 权限请求页面」→ 用户类型选 **外部** → 填应用名和邮箱 →
   在「测试用户」里**把自己的 Google 账号加进去**(不加会报 `access_denied`)
4. 「凭据」→「创建凭据」→「OAuth 客户端 ID」→ 应用类型选 **桌面应用** → 下载 JSON
5. 回到终端:

```bash
python3 scripts/gsc.py auth --client-secret-file ~/Downloads/client_secret_xxx.json
```

浏览器会弹授权页(测试模式下会有「Google 未验证此应用」警告,点「高级」→「继续」)。
成功后 refresh_token 存盘,**以后不用再授权**。这一次授权同时覆盖 GA4,见 [ga4.md](ga4.md)。

验证:

```bash
python3 scripts/gsc.py sites
```

## Property 清单

> **这是全项目唯一维护此列表的地方。** `.claude/skills/seo-data/SKILL.md` 等其他文件一律链接过来,不复制表格——避免新增/下线站点时要改多处、漏改导致文档和实际 property 不一致。
>
> **新增站点时**:1) 在 GSC 网页版把新站加为 property(网址前缀,记下带尾斜杠的完整 URL);2) 在下表加一行;3) 跑 `python3 scripts/gsc.py sites` 核对返回的 property 列表与本表一致。

**全部是「网址前缀」属性**(2026-08-09 从 GSC 网页版实读确认),不是域名属性。
后续所有命令的 `<site>` 参数原样传下表第二列,**结尾斜杠不能省**:

| 站 | siteUrl(命令里传这个) | 类型 |
|---|---|---|
| baxianfans | `https://baxianfans.com/` | 内容站 |
| partfit3d | `https://partfit3d.com/` | 工具站 |
| aidepixelate | `https://aidepixelate.com/` | 工具站 |
| easyframes | `https://easyframes.app/` | 工具站 |

明细见 [experiments.md 4 站实测数据](../experiments.md#4-站实测数据2026-08-09-从-search-console-拉取)。

> **网址前缀属性的含义**:只涵盖**该协议 + 该主机名**的 URL。
> `https://baxianfans.com/` 不包含 `https://www.baxianfans.com/` 也不包含 `http://` 版本——
> 如果站点有 www 或 http 流量且没做 301 收敛,那部分数据**根本不会出现在这个属性里**。
> 域名属性(写法是 `sc-domain:baxianfans.com`)才涵盖全部子域与协议,但当前四个站都不是这种。
> 后续如果发现数据比预期少,先查这一条。

## 四类固化查询

### 1. 找漏损点 —— 排名够好但没人点

**对应 todo**:修 partfit3d 的 title + meta

```bash
python3 scripts/gsc.py ctr-losers https://partfit3d.com/ --days 28
```

输出按 `lost`(预估损失点击 = 曝光 × CTR 差)降序,**这一列就是改 title/meta 的优先级队列**。
筛选条件:曝光 ≥30、排名 ≤20、CTR 低于该位置经验值的 50%。想放宽就调
`--min-impressions` / `--max-position` / `--threshold`。

`exp_ctr` 是位置对应的**行业经验均值**,只用来排序,不是目标值——不要拿它当 KPI。

### 2. 关键词 / 页面级全表

```bash
python3 scripts/gsc.py queries https://partfit3d.com/ --days 90 --limit 100
python3 scripts/gsc.py pages   https://partfit3d.com/ --days 90
```

`--format csv > out.csv` 可以导出;`--format json` 便于二次处理。

### 3. 改动前后对比

**对应用途**:改完 title/meta 之后验证到底有没有用

```bash
python3 scripts/gsc.py compare https://partfit3d.com/ \
  --before 2026-07-10:2026-08-06 --after 2026-08-14:2026-09-10
```

按 `Δclk` 绝对值排序。**两个窗口天数要一样长**,否则没有可比性。
改动后至少等 **2 周**再看——Google 重新抓取 + 排名波动需要时间。

### 4. 单页收录诊断

**对应 todo**:提三站收录率(24 页卡在「已发现-尚未编入索引」)

```bash
python3 scripts/gsc.py inspect https://baxianfans.com/ https://baxianfans.com/some-page
```

看 `coverageState` 和 `verdict`。常见值的含义:

| coverageState | 含义 | 该做什么 |
|---|---|---|
| `Submitted and indexed` | 正常 | — |
| `Discovered - currently not indexed` | Google 知道但没抓 | **内容厚度/质量信号不足**,补内容 + 加内链,不是技术问题 |
| `Crawled - currently not indexed` | 抓了但没收 | 质量判断没过,通常是薄内容或重复 |
| `Duplicate without user-selected canonical` | 重复页 | 补 canonical 标签 |
| `Not found (404)` | 死链 | 能 301 就 301,否则从 sitemap 移除 |

配额:每 property 每天 2000 次、每分钟 600 次。批量查要自己加节流。

## 陷阱

1. **数据延迟 3 天** —— 脚本默认把窗口结束日往前推 3 天(`DATA_LAG_DAYS`)。
   直接查"今天"会拿到不完整的尾部数据,看起来像流量暴跌。
2. **position 是加权平均,不是排名** —— 一个词在不同查询里位置不同,GSC 给的是曝光加权均值。
   `9.8` 不代表"稳定第 9.8 位",可能是大部分时间第 6、少数时候第 20。
3. **CTR 低 ≠ 一定是 title 差** —— 也可能是 SERP 上方被 AI Overview / 富结果 / 广告截流。
   看到漏损点之后,**必须无痕窗口 + 美区 IP 实搜一次确认**,再决定改 title 还是放弃这个词。
4. **query 维度会被采样和隐私过滤** —— 低频长尾词不会出现在 query 报表里,
   所以 query 行的点击总和**永远小于**站点总点击。差额不是 bug。
5. **`--days` 超过 16 个月无效** —— GSC 只保留 16 个月数据。
6. **窗口长度 ≠ 有数据的天数(算月均前必查)** —— 新站/新页面在窗口的大部分时间里是零曝光,
   拿总量除以窗口月数会严重低估。**判别法:同一指标拉 7 / 14 / 30 / 90 天四档,
   若后几档数字完全相同,说明数据全集中在最短那档之内**,只能用最近一个完整周期外推。
   实证:partfit3d 2026-08-09 按 90 天摊出"84 曝光/月",实际约 1,180 曝光/月,**低估 14 倍**,
   并直接导致两条 TODO 优先级判反。详见 [risks.md 「按报表窗口摊平均」](../risks.md)。

## 结果往哪写

| 拉到什么 | 回写位置 |
|---|---|
| 某次完整的站点表现快照 | [experiments.md](../experiments.md) 对应实验的「结果记录」 |
| 改动前后对比结论(有效/无效) | 同上,**并标注改动日期与对比窗口** |
| 由数据引出的具体动作 | [todos.md](../todos.md) |
| 反复出现的判断规律 | [principles.md](../principles.md) 或 `methods/` |

**不要**把原始表格整片粘进 memory —— 只写结论 + 拉取日期 + 窗口。
原始数据需要时重跑命令即可,这是脚本化相对手动导出的主要收益。
