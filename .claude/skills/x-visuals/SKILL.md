---
name: x-visuals
description: 给 X 推文/Thread 配图——头图(hero)、数据卡(datacard)、工具原生截图三类,统一深色视觉,零依赖用 headless Chrome 渲染 PNG。当用户说"配个头图""做张图""推文配图""封面图""带上数据截图""补个截图""这条推文的图"时使用。也在起草任何一条带数据的推文时主动建议配图。
---

# X 推文配图(hero / datacard / 工具截图)

**定位**:[`methods/x-tweet-writing-templates.md`](../../../memory/methods/x-tweet-writing-templates.md)
起草 SOP 的**视觉层**。文案 SOP 管"说什么",这个 skill 管"配什么图、怎么出图"。

> **默认行为**:任何一条带数字的推文,起草完成后**主动出图**,不用等用户开口。
> 用户 2026-08-12 明确要求:"以后都要这样"。

## 三类图,不要混用

| 类型 | 何时用 | 承载什么 | 模板 |
|---|---|---|---|
| **hero 头图** | Thread 第 1 条 / 单条推文首图 | **一句主张** + 3-4 个关键数字。给不点开的人看 | [`templates/hero.html`](templates/hero.html) |
| **datacard 数据卡** | 论点需要多源对照、结论需要压缩 | 高信息密度:分栏对照 / 条形图 / 表格 | [`templates/datacard.html`](templates/datacard.html) |
| **工具原生截图** | 需要**证据**,证明数字不是编的 | SimilarWeb / Semrush / 哥伦布 / GSC 原生界面 | 见下方「工具截图 SOP」 |

**自制图 ≠ 证据。** 结论用自制卡,取证一律上原生截图——这是可信度的分水岭。
一条拆解型 Thread 的典型配置:`hero ×1 + 原生截图 ×2-3 + datacard ×1`。

## 出图流程

### 1. 写 HTML

复制对应模板到 `drafts/x/<YYYY-MM-DD>-<slug>-hero.html`,改文案和数字。
**画布固定 1600×900**(16:9,X 展示比例最佳),不要改尺寸。

### 2. 渲染 PNG

```bash
bash .claude/skills/x-visuals/render.sh drafts/x/2026-08-12-foo-hero.html
```

等价于(`--force-device-scale-factor=2` 出 2x 图,X 上不糊):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --force-device-scale-factor=2 \
  --window-size=1600,900 --screenshot="out.png" "file://$PWD/in.html"
```

### 3. 自检(strict)

渲染后**必须 Read 一次 PNG 肉眼确认**,不要直接交付。最常见的两个问题:

- **底部内容被裁**:内容高度超过 900px。压缩 padding / 字号 / 行高,不要加高画布
- **中文换行难看**:主标题手动加 `<br>` 控制断句,不要靠自动折行

## 设计规范(所有图共用,保证系列感)

```
背景        #0d1117        卡片      #161b22
主文字      #e6edf3        次级      #8b949e      三级/来源  #6e7681
分隔线      #21262d        边框      #30363d
强调(橙)    #f0883e   ← 主强调色,一张图里只强调 2-3 处
正向(绿)    #3fb950   ← 增长、成功
负向(红)    #f85149   ← 问题、缺失、0
信息(蓝)    #58a6ff   ← 数据源名、标签
字体        -apple-system, "PingFang SC", "Helvetica Neue", sans-serif
数字        font-variant-numeric: tabular-nums   ← 必加,否则数字对不齐
```

**克制**:一张图最多一个视觉焦点。四个数字全用橙色 = 没有重点。

## 数据标注(硬规则,不可省)

每张带数据的图,**底部必须有来源行**,含三要素:

```
数据  <工具名> · <拉取日期> · <信任等级>
```

对齐项目的[数据源使用纪律](../../../CLAUDE.md):

| 来源 | 图上必须写 |
|---|---|
| GSC / GA4 | 可不标等级(真值) |
| SimilarWeb / Semrush / 哥伦布 | **第三方估算** |
| 站点源码 / robots / 埋点实读 | **一手** |

**同源不算交叉验证**:哥伦布的流量构成与 SimilarWeb 数字一致(实测 2026-08-12),
两者是同源估算。图上**不要**写"多个数据源互相印证"。

## 脱敏约束(用户 2026-08-12 定)

| 项 | 规则 |
|---|---|
| 自有站**实测数字** | ✅ 可出现(曝光数、Top 10 词数、站点数量) |
| 自有站**域名** | ❌ 不出现 |
| 自有站**主攻关键词** | ❌ 不出现 |
| 共享面板账号名 / 头像 | ❌ 截图前隐藏(见下方 SOP) |
| 竞品域名 | 由用户逐次决定;公开投放中的站点非隐私信息,点名更可信 |

## 工具截图 SOP(ego-browser)

用 `captureScreenshot()`,**踩过的坑全在这**:

```bash
ego-browser nodejs <<'EOF'
await useOrCreateTaskSpace('seo tools')     # 不先选 task space 会报 "Task space not selected"
await openOrReuseTab('<url>', { wait: true, timeout: 90 })
await wait(28)                               # SPA 渲染慢,给足时间
cliLog('SHOT='+await captureScreenshot())    # 返回临时文件路径,不是图片数据
EOF
cp /var/folders/.../ego-browser-shot-<pid>-1.png drafts/x/foo.png
```

**四个硬坑**:

1. **ego 的 node 是只读文件系统** —— `fs.copyFileSync` 会 `EROFS`。
   必须 `cliLog` 出路径,**在 ego 外面用 shell `cp`**。临时文件名带 pid,pid 会变,每次照抄输出里的路径
2. **`require` + top-level await 冲突** —— 用 `import fs from 'node:fs'`,不要 `require`
3. **滚动容器常常不是 window** —— 如 SimilarWeb 是 `.sw-layout-scrollable-element`。
   先探:`[...document.querySelectorAll('*')].filter(e=>e.scrollHeight>e.clientHeight+200 && e.clientHeight>400)`
4. **React 合成事件** —— `js()` 里调 `.click()` 触发不了,要用 ego 的 `click()` helper

**清理遮罩层**(试用期弹窗 / 配额提示 / 引导条):

```js
[...document.querySelectorAll('body *')].forEach(e=>{
  const s=getComputedStyle(e), r=e.getBoundingClientRect();
  if((s.position==='fixed'||s.position==='absolute') && parseInt(s.zIndex||0)>=100
     && r.width>400 && r.height>200) e.remove();
});
```

**账号脱敏**(共享面板必做):

```js
[...document.querySelectorAll('*')].forEach(e=>{
  if(e.children.length===0 && /<账号名>/i.test(e.textContent)) e.style.visibility='hidden';
});
document.querySelectorAll('header img, nav img, [class*="avatar"]').forEach(e=>e.style.visibility='hidden');
```

**取证要把口径截进去**:排序条件、时间窗口、地区、总量。
实例:哥伦布"榜首"必须让「排序=环比增长」出现在图里——按访问量排它根本不是第一,
不截口径就等着被人拿数据打脸。

## 发布形态

**X 单条推文的图片只能附在正文末尾**(2×2 网格),插不进正文中间。

| 情况 | 做法 |
|---|---|
| 正文短、图 ≤2 张 | 单条,图附末尾 |
| 正文长、图 3-4 张 | **拆 Thread**,每条带对应的图,图跟着论点走 |

图多且走单条时,正文里要用「(图 2)」显式指代,否则读者对不上——但这是下策。

## 产物落点

- HTML 与 PNG 一起放 `drafts/x/`,同名不同后缀,**HTML 要留着**(下次改数字直接复用)
- 在推文草稿 md 的「配图」表里登记:文件名 + 作用 + 顺序
- 发布后照常回填 [`todos.md` 本周期已发](../../../memory/todos.md#本周期已发滚动)
