# Build in Public「卖铲子」品类建议

> 咨询时间:2026-08-11 (UTC+8) · 来源:哥飞 SEO Agent (deepseek-v4-flash)
> **性质:他人观点,非数据。** 本轮用于扩候选,最终判断以 TrustMRR 验证收入、哥伦布增长数据和官网价格为准。

## 1. 原始建议

顾问给出四类候选:

1. 窄技术栈 SaaS boilerplate,引用 ShipFast 作为付费证据。
2. 目录提交 / 外链助手,引用 Submify、TinyLaunch 等产品存在性。
3. 轻量 GSC 分析器,把 DataFast 的收入当作「分析工具有人付费」的旁证。
4. Chrome SEO 开发者工具,优点是两周可做,但没有给出直接收入证据。

它同时提示了反证:boilerplate 维护与开源竞争重;目录清单会失效且容易遇到反爬;
GSC / Chrome 工具容易形成免费使用习惯。

## 2. 公理扫描与辩证

### ⚠️ 公理 4:跨品类收入不能当直接付费证据

DataFast 是创业者收入分析,不等于「轻量 GSC 分析器」有人付费。后续实查还发现
[SEO Receipts](https://seoreceipts.com/pro/) 已用 GSC 真数据做公开 receipt + 私有行动建议,
官网价格为 $9/月、$29/月。它能证明 GSC shareable analytics 有付费供给,也同时说明直接复制已经拥挤。

### ⚠️ 公理 5:目录与 Chrome 候选缺少可核算定价

顾问没有给出这两类的验证收入、付费人数或可对照成本。只能作为候选词,不能进 MVP。
目录提交还带持续维护、人工审核、反爬和清单腐烂成本,不符合两周 MVP 的低维护要求。

### ✅ boilerplate 的付费逻辑被独立数据补强

顾问的方向本身可保留,但证据换成 TrustMRR API key 验证收入:

- ShipFast:累计收入约 $1.3M,近 30 天约 $3.5K。
- TanStarter:累计 $26,178,近 30 天 $2,086,定价 $159,营销渠道明确为 X。
- Directory Launch:累计 $1,604,近 30 天 $199,定价 $199;创始人仅 134 个 X 粉丝。
- React Bits Pro:近 30 天约 $32K,说明「开发者组件 / 模板」也能直接收费。

### ⚡ 准公理 C:不能在通用 boilerplate 里硬卷

ShipFast、TanStarter、AstroKit、LaunchFast 等已覆盖通用 SaaS 底座。可采纳的是「重复流程产品化」,
不是再造一个 auth + payments + dashboard 大礼包。必须收窄到用户已有自有实践的工作流。

## 3. 采纳判定

**判定:部分采纳**

### 采纳

- 采纳「卖重复开发流程的底座」这一结构。
- 收窄为 **SEO 工具站 Starter Kit + 自动防错规则**:Astro / Cloudflare、canonical、sitemap、
  真 404、pSEO 页面、GSC 接入和发布前检查。
- 理由:与用户已上线 4 站、正在修的索引 bug 直接同源;公开修 bug / 发模板 / 对比 GSC
  本身就是内容和获客,目标买家与 X 独立开发圈重叠。

### 不采纳

- 不做通用 SaaS boilerplate:强竞品多,维护面过宽。
- 不做 GSC shareable analyzer:SEO Receipts 已正面占位。
- 不做目录代提交:运营和清单维护重,直接付费证据不足。
- 不做 Chrome SEO 工具:免费替代多,顾问未提供直接收入证据。

### 保留的关键未知

「SEO 工具站 Starter Kit」只有**相邻品类收入证据**,还没有本品类预售证据。因此当前只能进入
48 小时预售验证,不能直接开两周开发。
