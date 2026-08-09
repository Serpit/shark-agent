---
name: seo-data
description: 查四个自有站(baxianfans / partfit3d / aidepixelate / easyframes)的 Google Search Console 真实搜索数据——关键词排名、点击、曝光、CTR、收录状态、404、改动前后对比。当对话涉及"排名怎么样""有没有流量""CTR 为什么这么低""收录了吗""这个词表现如何""改完有没有效果""站点数据""搜索表现""GSC""Search Console"时使用。也用于任何需要用自有真实数据支撑决策的场景(选词复盘、变现路径判断、扩量决策)。
---

# 自有站搜索数据(GSC)

四个站的**真值来源**。第三方工具(SimilarWeb / SEMrush / Ahrefs)都是估算,**冲突时一律以本 skill 的数据为准**。

完整手册:[`memory/sources/gsc.md`](../../../memory/sources/gsc.md) —— 字段含义、5 个陷阱、property 类型说明在那里,本文件只放触发后的执行路径。

## 第一步:先问出口(不可跳过)

**拉数前必须先明确:这次查询的结果会落到哪个具体动作?**

答不上来就不要查,直接告诉用户"这个查询目前没有动作出口,先想清楚要拿它决定什么"。

依据 [`memory/axioms.md`](../../../memory/axioms.md) 公理 6:外部数据源天然会把节奏拉回「再调研一下」,而 [`timeline.md`](../../../memory/timeline.md) 从 2026-07 起已是试错阶段。用户连续要求拉数但说不出动作时,主动追问一次这是信息问题还是心理问题。

## 第二步:选路径

**优先走 API**(一条命令,可脚本化、可对比、可导出):

```bash
python3 scripts/gsc.py sites          # 先验证凭证是否可用
```

报「没找到凭证」或 HTTP 401/403 → 授权还没做,见下方「授权未完成时」。

### siteUrl 传参

四个站都是**网址前缀属性**,结尾斜杠不能省:

| 站 | 传这个 |
|---|---|
| baxianfans | `https://baxianfans.com/` |
| partfit3d | `https://partfit3d.com/` |
| aidepixelate | `https://aidepixelate.com/` |
| easyframes | `https://easyframes.app/` |

### 问题 → 命令

| 用户想知道 | 命令 |
|---|---|
| 哪些词排名够好但没人点(改 title 的优先级) | `ctr-losers <site> --days 90` |
| 关键词整体表现 | `queries <site> --days 90 --limit 100` |
| 哪些页面在跑 | `pages <site> --days 90` |
| 改完有没有效果 | `compare <site> --before A:B --after C:D`(两窗等长,改后至少等 2 周) |
| 某页为什么没收录 | `inspect <site> <url>` |

加 `--format csv` 导出,`--format json` 便于二次处理。

## 授权未完成时(当前状态)

**已知阻塞**:账号未开两步验证,Google Cloud 强制 MFA,建 OAuth 客户端那步走不了。
详见 [`memory/todos.md`](../../../memory/todos.md) blocked 段。

**这时不要停下来干等**——GSC 网页版不受影响,用 ego 读,数据同样是真值:

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('gsc read')
await openOrReuseTab('https://search.google.com/search-console/performance/search-analytics?resource_id=https%3A%2F%2Fpartfit3d.com%2F', { wait: true, timeout: 60 })
await wait(6)
// 默认只显示点击+曝光,必须先打开 CTR 与排名两个指标卡
await js(`
  ['平均点击率','平均排名'].forEach(w=>{
    const el=[...document.querySelectorAll('div,span')].find(e=>e.textContent.trim()===w);
    if(el){ let n=el; for(let i=0;i<6&&n;i++){ if(n.getAttribute&&n.getAttribute('role')==='button'){n.click();break;} n=n.parentElement; } }
  }); return 1;
`)
// 时间窗:按钮文本是 '7 天' / '28 天' / '3 个月'
await js(`
  const b=[...document.querySelectorAll('button,[role=button]')].find(e=>(e.textContent||'').trim().startsWith('3 个月'));
  b && b.click(); return !!b;
`)
await wait(7)
cliLog(await js(`
  const rows=[...document.querySelectorAll('[role=row],tr')].map(tr=>
    [...tr.querySelectorAll('[role=cell],[role=gridcell],td')].map(td=>td.textContent.trim())
  ).filter(r=>r.length>=5);
  return JSON.stringify(rows.slice(0,60));
`))
EOF
```

要点:
- 换站改 `resource_id` 的 URL 编码值
- 表格行在 DOM 里会重复出现,**去重后再算**
- 站点总计在指标卡上(`总点击次数` / `总曝光次数`),**与 query 表的和不相等是正常的**——query 维度被隐私过滤,差额通常占 40-60%
- 拿到行之后,CTR 漏损排序用 `scripts/gsc.py` 里的 `expected_ctr()` 算,不要另起一套标准

## 第三步:解读时必须带上的三条

1. **绝对量优先于比率**。CTR 从 0.4% 提到 2.6% 听起来翻了 6 倍,但如果曝光只有 253,那是多 5 次点击。**先算绝对增量再给建议**,不要用百分比制造进展幻觉。
2. **position 是曝光加权均值,不是排名**。`9.8` 可能是大部分时间第 6、少数时候第 20。曝光 <5 的行,position 基本是噪音,不要据此下结论。
3. **CTR 低 ≠ title 差**。也可能被 AI Overview / 富结果 / 广告截流。给出改 title 建议前,提醒用户无痕 + 美区 IP 实搜确认。

## 第四步:回写

| 拉到什么 | 写到哪 |
|---|---|
| 站点表现快照、query 级下钻结论 | [`experiments.md`](../../../memory/experiments.md) 对应实验的「结果记录」,**标注拉取日期 + 窗口** |
| 改动前后对比结论 | 同上,额外标改动日期 |
| 引出的具体动作 | [`todos.md`](../../../memory/todos.md) |
| 反复出现的判断规律 | [`principles.md`](../../../memory/principles.md) 或 `methods/` |

**不要**把原始表格整片粘进 memory,只写结论 + 日期 + 窗口。原始数据重跑命令即可。

## 相关

- 竞品/第三方流量估算 → `seo-competitor` skill(尚未建)
- 外部顾问观点 → `seo-advisor` skill(尚未建),观点**禁止直接落 memory**,必须过 [`methods/axiom-scan.md`](../../../memory/methods/axiom-scan.md)
