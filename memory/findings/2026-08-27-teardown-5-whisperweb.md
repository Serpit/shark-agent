# 拆解报告 ⑤:whisperweb.dev

> **拉取日期**:2026-08-27 · **数据源**:Columbus MCP / SimilarWeb API 直连 —— **全部第三方估算**
> **形态**:零推理成本本地工具 · **审计判定**:❌ **淘汰。第三个「伪装站」,标签与实际业务完全不符。**

## ⚠️ 先说结论

总审计把它列为**形态 E(零推理成本本地工具)的代表样本**,理由是:

> 「主打浏览器本地运行、文件不上传。**推理成本 ≈ 0**(跑在用户机器上,连中转站都不用),
> 隐私是卖点不是成本。DR 16 / 357,776 / +235%。」

**拉出头部词后,这个站根本不是做语音转文字的。**

## 一、头部词 —— 4/5 是西语 YouTube 下载词

| 词 | 月搜 | CPC | 该站估值 |
|---|---|---|---|
| **`descargar videos de youtube`** | **551,890** | $0.46 | **$5,760** |
| **`youtube mp4`** | **512,730** | $0.78 | $1,990 |
| **`descargar video de youtube`** | **289,640** | $0.46 | $1,650 |
| `whisper web` | 10,690 | $2.02 | $1,340 |
| **`descargar video youtube`** | **219,910** | $0.71 | $1,220 |

**「descargar videos de youtube」= 西班牙语「下载 YouTube 视频」。**

真正与产品相符的 `whisper web`(10,690)只排第 4,估值 $1,340,
而三个西语下载词合计 **106 万月搜、估值 $8,630**。

**这跟 `clumi.ai`(标签 AI 音频人声分离,实为 `youtube to mp3` 站)、
`thumblifyai.com`(标签 AI 缩略图,实为 `youtube shorts download` 站)是同一模式。
本次审计已抓到第三个。**

## 二、国家分布印证

| 国家 | 占比 |
|---|---|
| 西班牙 | **14.79%** |
| 巴西 | **12.25%** |
| 墨西哥 | **9.21%** |
| 秘鲁 | **8.91%** |
| 美国 | **6.81%** |

**西语 + 葡语区合计约 45%,美国仅 6.81%** —— 是本次审计所有样本里美国占比最低的
(对照 `thefacereport` 51.3%)。一个「基于 OpenAI Whisper 的英文转录工具」不会长成这个地域结构。

## 三、互动数据印证

| 指标 | 读数 | 对照 |
|---|---|---|
| 跳出率 | **57.98%** | `thefacereport` 35.3% |
| 页/次 | **1.41** | `thefacereport` 4.43 |
| 停留 | **51 秒** | `thefacereport` 122 秒 |

**页/次 1.41 = 进来一个页面,转完就走。** 与 `clumi.ai`(页/次 1.73、跳出 60.5%)几乎一致
——**这是下载站的行为指纹,不是工具站的。**

## 四、外链画像 —— 评论区 spam,不是生态引用

指向它的站点:

| 来源 | DR | 页面内容 | 锚文本 |
|---|---|---|---|
| bakerella.com | **70** | 糖果巧克力曲奇食谱 | **`Lucas Hammond`** |
| madrimasd.org | **73** | 西班牙数学博客「造物主如何用三角形构建宇宙」 | **`Whisper Web Team`** |
| repeatcrafterme.com | **62** | 钩针编织鳄梨 | `WhisperWeb` |
| dinnerwithjulie.com | 51 | 植物基巧克力蛋糕 | `WhisperWeb` |
| pierfishing.com | 40 | 加州码头钓鱼「Halfmoon」 | `GGJames` |
| jacofallthings.com | 36 | 如何去除衣服上的草莓渍 | **`Owen Bradley`** |
| lilistravelplans.com | 43 | 坦桑尼亚温泉 | `WhisperWeb` |
| wonderfulmalaysia.com | 45 | 吉隆坡最好的菜市场 | — |
| allnaturalandgood.com | 7 | 自制肉桂威士忌 | **`Ava Lawson`** |
| reneeroaming.com | 43 | 新英格兰秋季公路旅行 | `WhisperWeb` |

**烘焙、钓鱼、钩针、旅游、去污渍——与语音转文字零相关,而锚文本是人名**
(Lucas Hammond / Owen Bradley / Ava Lawson / Sarah Mitchell / Minh Nguyen / Dian Pramudita)。

**这是典型的博客评论区 / 作者署名注入 spam。** 这些博客 DR 不低(70/73/62),
所以能撑出「558 引用域 / dofollow 26%」的表面数据。

**真外链只有 2 条**:

| 来源 | DR | 说明 |
|---|---|---|
| **windowsforum.com** | **68** | 「Best Free Notta.ai Alternative — Private & Local」→ `/alternative-to-notta` |
| voicescriber.com | 5 | 「Best Free Audio-to-Text Converters That Do Not Upload Your Files」 |

这两条对应它 `seo_playbook` 里的 `alternatives_pages` —— **产品那一半是真的,只是不是流量来源。**

## 五、基本盘(供参考)

| 项 | 读数 |
|---|---|
| 注册 | 2026-02-03(**6 个月**) |
| 月访问 | 357,776(+235%) |
| DR | 16 |
| 自然搜索 | 65.59% |
| **gen_ai** | **11.42%** ← 全会话最高 |
| 定价 | Free / **$10/mo** / **$20/mo** / **$120** |
| 外链 | 5,675 条 / 558 引用域 / dofollow 26%(条)/ 9%(域) |
| 技术栈 | Next.js,首页 874 词,**0 张图** |
| 外链出站 | chatgpt.com / github.com / openai.com / huggingface.co |

### 流量曲线

| 月份 | 访问 |
|---|---|
| 2026-02 | 4 |
| 2026-03 | 1,544 |
| 2026-04 | 24,935 |
| 2026-05 | 55,010 |
| 2026-06 | 106,897 |
| 2026-07 | **357,776**(3.3 倍跳变) |

## 六、品类词难度(顺带取得)

| 词 | SimilarWeb KD | CPC | 意图 | AIO |
|---|---|---|---|---|
| `speech to text` | **91.0** | **$0.00–0.00** | 100% Informational | 有 |

**CPC 全零 —— 没有任何广告主愿意为这个词出价。** 月量 219,837,自然点击 150,751。
**KD 91 + CPC $0 = 极难打且完全不值钱**,与[risks.md 音频类品类结论](../risks.md)一致。

## 七、判定

**❌ 淘汰。三条理由**:

1. **业务与标签不符**:主力流量是西语 YouTube 下载,不是语音转录。
   撞[伪装站禁区](2026-08-27-columbus-post-update-audit.md)与平台 ToS 风险。
2. **外链是 spam**:558 引用域主要来自无关博客的评论区人名注入。
3. **即使产品那一半是真的,它所在的品类词 `speech to text` CPC $0.00、KD 91** —— 不值得打。

## 八、但它留下两条有用的东西

1. **`gen_ai` 11.42% 是全会话最高。** ChatGPT / Perplexity 等 AI 助手正在成为可观的引流渠道
   (对照:`thefacereport` 4.15%、`fontvibe` 3.80%、`jobsuit` 1.34%)。
   **这是一个还没被系统研究过的新渠道,值得单开一次调研。**
2. **`alternatives_pages` 打法有效**:`windowsforum.com`(DR 68)那条真外链,
   来自它的 `/alternative-to-notta` 页面被论坛讨论引用。
   **「做 X 的免费替代品」页面能自然吸引论坛引用**,这条可迁移。

## 九、形态 E 的替补

原「零推理成本本地工具」形态还有两个未拆的样本,若要保留这个形态需先验它们的头部词:

- `bulkpictools.com`(DR 10 / 225,538 / +289%)
- `removevocals.ai`(DR 0 / 64,698 / **+1224%**)

**在验完之前,形态 E 应从可执行清单中摘除。**

---

**关联**:[总审计报告](2026-08-27-columbus-post-update-audit.md) · [risks.md 音频品类 CPC](../risks.md) · [columbus.md 硬边界](../sources/columbus.md)
