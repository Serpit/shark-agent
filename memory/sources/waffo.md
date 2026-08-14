# Waffo Pancake 收款通道接入手册

> **性质**:这不是数据源,是**收款通道**。放在 `sources/` 是因为它同样属于「怎么接进来、字段是什么、有哪些坑」这一层。
> **信任等级**:官方文档口径(2026-08-12 实拉 `docs.waffo.ai`),**不是自有实测**。
> 开通并跑通首笔后,把实际到手数字回写本文件「实测校准」段,并覆盖此处的文档口径。
>
> **本次核实解决的是 [profile.md](../profile.md#能力与资源) 2026-08-11 挂的「资质要求 / 费率 / 支持地区待核实」。**

## 一、它是什么

**Merchant of Record(MoR)模式**:Waffo 在法律上是卖方,替你收单、算税、报税、开票、结算;你保持产品所有权,钱最终打到你的账户。
**Pancake** 是它面向个人开发者 / 初创 / Agent 的产品线。

对本项目的意义:**「中国大陆个人无海外主体 → 无法自有收款」这条卡了三个多月的硬约束,在文档层面确认可解除**——
不需要 LLC、不需要公司注册、不需要海外银行账户,身份证 + 国内银行卡/支付宝即可收款。

- 官网:waffo.ai · 商户后台:https://pancake.waffo.ai/merchant/dashboard
- 文档:https://docs.waffo.ai · 全文喂 AI:https://docs.waffo.ai/llms-full.txt · 页面索引:https://docs.waffo.ai/llms.txt

## 二、注册的硬性条件(三关,按顺序过)

三关是**独立**的,不要混为一谈。第 1 关只要邮箱,第 2 关卡的是**你的站**,第 3 关卡的是**你的身份**。

### 第 1 关 · 开户(几分钟,零门槛)

| 项 | 要求 |
|---|---|
| 注册方式 | Google OAuth / GitHub OAuth / Magic Link |
| 信用卡 | **不需要** |
| 公司主体 | **不需要**("No LLC needed") |
| 产出 | 建 Store → 建 Product → 拿到永久 checkout 链接 `https://checkout.waffo.ai/{store-slug}/{product-slug}` |

开完户即可用**测试模式**跑通全流程(建品、下单、webhook),**不需要任何审核**。
测试卡:成功 `4576 7500 0000 0110`,拒付 `4576 7500 0000 0220`(Visa,任意未来有效期 + 任意 CVC)。

### 第 2 关 · KYB 店铺审核(1–3 个工作日,**卡住生产收款**)

入口:Dashboard → Settings → Business Details → Submit for review。**这一关卡的是你的网站,不是你的身份。**

**要填的字段**:

| 字段 | 必填 | 说明 |
|---|---|---|
| About your product | ✅ | 卖什么,一段话 |
| Product website | ✅ | **公开可访问**的产品 URL |
| Contact email | ✅ | 审核沟通 + store 支持邮箱(需先验证 6 位码) |
| Seller type | ✅ | **Individual / Solo developer** 或 Registered business,**两者同标准审核,个人不吃亏** |
| Product readiness | ✅ | building / launched |
| Existing customers | ✅ | 是否已有付费用户 |
| 合规声明 | ✅ | 非禁售类目 / 定价页公开 / 不侵犯商标 |

**过审 checklist(逐条都得满足,「changes requested」几乎全出在这几条)**:

- [ ] **产品是活的** —— 提交的 URL 必须公开可达,**没有登录墙、没有密码、没有 "coming soon" 占位**
- [ ] **一眼看懂卖什么** —— 首次访客能理解产品、用途、怎么用
- [ ] **定价公开可见** —— 在进 checkout **之前**就能看到要收多少钱
- [ ] **Privacy Policy + Terms of Service** —— 两个页面都存在、**无需登录即可访问**(官方给了 [ToS](https://docs.waffo.ai/mor/account-reviews/tos.md) / [Privacy](https://docs.waffo.ai/mor/account-reviews/privacy-policy.md) / [AUP](https://docs.waffo.ai/mor/account-reviews/aup.md) 模板)
- [ ] **支持邮箱** —— 真实、有人看、**显示在网站上**,且与提交的 contact email **一致**
- [ ] **不造假** —— 无假评价、假证言、灌水用户数
- [ ] **不撞商标** —— 产品名 / 店铺名不侵犯他人商标、不引起品牌混淆
- [ ] **不在禁售清单上**(见第五节)

**返工原因 Top 5**:网站有密码/爬虫墙 · 法务页缺失或需登录 · 支持邮箱对不上 · 产品是占位页 · 描述夸大失实。
返工不用重开店,改完**同一个 store 重新提交**,再等 1–3 个工作日。
**审核通过后再改 Business Details 会触发重审**(重审期间生产功能不中断)。

### 第 3 关 · KYC 身份验证 + 域名验证(卡住提现,不卡收款)

**身份**(Profile 页,提现前必须完成):

| 字段 | 格式 |
|---|---|
| First / Last name | 拉丁字母(拼音),1–64 / 1–80 字符 |
| **Legal full name** | **本地文字(如 张三)**,必须与证件**逐字符一致** —— 每笔提现的收款人名就取这个字段 |
| Nationality | ISO 3166-1 alpha-2(如 CN) |
| ID type | **中国大陆用身份证(National ID)**,其他国籍用护照 |
| ID number | 身份证 18 位 / 护照 7–13 位字母数字 |

⚠️ **公司主体收款「coming soon」,当前只能走个人身份**。
⚠️ **一旦有过一笔提现,legal name / ID number / 国籍 / 证件类型全部锁定**,只能联系客服改。**首次填写务必逐字符核对。**

**域名验证**(KYB 批准前必须完成,四选一):

| 方式 | 耗时 | 适用 |
|---|---|---|
| 支持邮箱同域自动匹配 | **即时** | `support@example.com` ↔ `https://example.com`,一键验证 |
| DNS TXT 记录 | 5–30 分钟 | 最通用 |
| HTML `<meta>` 标签 | 1–2 分钟 | 静态站 |
| `.well-known` 文件 | 1–2 分钟 | 静态站 |

⚠️ **KYB 批准后域名被锁死**,要改只能联系客服。→ **别拿临时域名/测试域名提交审核。**

## 三、费率与资金流(全成本,别只看 3.9%)

### 手续费全表

| 项目 | 费用 |
|---|---|
| 卡 / Apple Pay / Google Pay 成功交易 | **3.9% + $0.50** |
| 微信支付成功交易 | 3.9%(**无固定费**) |
| 失败交易(已触发 3DS) | **$0.30 / 次尝试**(未走到 3DS 的会话免费) |
| 退款处理 | **$1.00 / 笔**,且**原交易费不退**(全额退款也不退) |
| 提现 | **1%,最低 $10.00 / 笔** |
| 拒付(chargeback) | 首次 $25 · 申诉重提 $10 · 预仲裁 $25 |
| 月费 / 开通费 | **$0** |

税务计算、代收、代缴、发票、欺诈防护、Dashboard、Consumer Portal、Webhook/API **全含,不另收费**。

### ⚠️ 最大的坑:提现最低 $10 手续费

`1% 与 $10 取大` 意味着提现费率随金额剧烈变化:

| 提现金额 | 实际手续费 | 实际费率 |
|---|---|---|
| $20(最低门槛) | $10 | **50%** |
| $100 | $10 | 10% |
| $500 | $10 | 2% |
| **$1,000** | **$10** | **1%(拐点)** |
| $2,000 | $20 | 1% |

**结论:提现额低于 $1,000 就是在多付钱。运营纪律 = 攒到 ≥$1,000 再提一次现。**

### 单笔到手测算

| 售价 | 交易费 | 净收 | 到手比例 |
|---|---|---|---|
| $9.90 | $0.89 | $9.01 | 91.0% |
| $19.00 | $1.24 | $17.76 | 93.5% |
| $29.00 | $1.63 | $27.37 | 94.4% |

叠加提现(按攒够 $1,000 算,+1%)后,**全链路综合成本约 5.6%–10%,单价越低越吃亏**。
→ 与 [risks.md 低价定价陷阱](../risks.md) 同向:**$1–5 的定价在 MoR 通道下几乎没有毛利**。

### 与竞品对比(文档自述口径,**未独立核实**)

| 通道 | 交易费 | 月费 |
|---|---|---|
| **Waffo Pancake** | 3.9% + $0.50 | $0 |
| Paddle | 5% + $0.50 | $0 |
| Lemon Squeezy | 5% + $0.50 | $0 |
| Gumroad | ~10% | $0 |

⚠️ **辩证**:Waffo 交易费低 1.1pp,但**多了 1% + $10 最低的提现费**。
按月流水 $1,000 / 单价 $29 估算,Waffo ≈ 6.55%,Paddle ≈ 6.6% —— **两者基本持平**。
Waffo 的真实优势不在费率,而在**中国大陆个人可直接开通 + 人民币直接到卡/支付宝**这条通道本身。

### 资金流与时间线

```
买家付款
  ↓ 约 10 个工作日(留退款 / 拒付窗口)
自动结算进 merchant balance(所有 store 汇总)
  ↓ 手动发起提现,最低 $20 USD 等值
提现到账
  ↓ 1–3 个工作日(pending 3–5 天算正常)
人民币到银行卡 / 支付宝
```

**从首笔成交到手上有钱 ≈ 3 周。** 提现是**按需手动**,没有固定周期。
测试模式**不影响提现**——Finance 与 Payout History 永远读真实数据,无法模拟提现。

### 收款地区与货币

| 项 | 现状 |
|---|---|
| **提现地区** | **仅中国大陆**,结算 **CNY**,支持多数大陆主流银行 |
| **提现方式** | 银行卡 / 支付宝(收款人名自动取 KYC 的 legal name,**不可改**) |
| 买家可用支付方式 | Visa / Mastercard 全球;Apple Pay / Google Pay 按地区;微信支付 |
| 税务覆盖 | 美国 45+ 州销售税 · 欧盟 VAT · 英国 · 其余按当地要求 |
| 封禁国家 | 23 个受制裁国家(阿富汗、古巴、伊朗、朝鲜、俄罗斯、叙利亚等) |

## 四、集成方式(四条路径,按投入从低到高)

### 路径 A · 零代码:永久 checkout 链接

建完产品自动生成 `https://checkout.waffo.ai/{store-slug}/{product-slug}`,**永不过期,改产品也不失效**。
直接贴在落地页按钮上就能收钱。**MVP 阶段首选,一行代码都不用写。**

### 路径 B · Next.js SDK(最快的有代码方案)

```bash
npm install @waffo/pancake-nextjs   # 需 @waffo/pancake-ts 作为 peer dep,Next.js 14+ App Router
```

提供 `CheckoutButton` 组件、`useCheckout()` / `useBuyer()` 等 hooks、`createCheckoutAction()` 等 Server Actions、
以及自动验签分发的 `Webhook` Route Handler。

### 路径 C · TypeScript SDK(任意 Node 框架)

```bash
npm install @waffo/pancake-ts       # 零运行时依赖,ESM + CJS,Node >= 20
```

```typescript
import { WaffoPancake } from "@waffo/pancake-ts";

const client = new WaffoPancake({
  merchantId: process.env.WAFFO_MERCHANT_ID!,   // Dashboard → API & Development
  privateKey: process.env.WAFFO_PRIVATE_KEY!,   // RSA 私钥,PEM / base64 / raw 均可
});

const result = await client.checkout.authenticated.create({
  productId: "PROD_xxx",
  currency: "USD",
  buyerIdentity: "userIdInYourSystem",   // 你系统里的稳定用户标识
});
// 跳转 result.checkoutUrl
```

命名空间:`stores` / `onetimeProducts` / `subscriptionProducts` / `subscriptionProductGroups` /
`orders` / `checkout` / `graphql` / `auth` / `webhooks`。写操作走 REST,读操作走 GraphQL。

### 路径 D · 直接调 API

REST 管写、GraphQL 管读,自己实现签名与验签。SDK 目前只有 TS / Next.js,**Python / Go / PHP 仍在 roadmap**。

### 让 AI 直接接:官方 Skill

官方为编码 agent 准备了 `SKILL.md`:

- Skill:https://docs.waffo.ai/integrate/skill.md
- 全文文档(喂给 agent):https://docs.waffo.ai/llms-full.txt

推荐 prompt:

```
读 https://docs.waffo.ai/llms-full.txt,加载 https://docs.waffo.ai/integrate/skill 的官方 skill,
把 Waffo Pancake 支付集成到当前项目,然后测试:从 Dashboard 拿 Merchant ID、创建 API Key、装 SDK、
写 checkout 与 webhook 端点、用测试卡 4576750000000110 下单、确认 webhook 收到 order.completed。
```

### 有没有 CLI?(2026-08-12 查 npm registry)

**没有官方的通用 CLI。** 日常运营(建店 / 建品 / 看订单 / 提现)只有三条路:**Dashboard 网页** · **SDK** · **REST/GraphQL API**。
npm 上 `@waffo/*` 一共 4 个带 `bin` 的包,但**都是单一用途的一次性工具,不是管理台**:

| 包 | 命令 | 用途 | 与本项目相关性 |
|---|---|---|---|
| `@waffo/pancake-migrate` | `npx @waffo/pancake-migrate` | **从 Stripe / Creem 迁移**产品、价格、图片、webhook、品牌信息到 Pancake。有交互模式和 `--dry-run` | ❌ 新站没有可迁的东西 |
| `@waffo/waffo-integrate` | `npx @waffo/waffo-integrate` | 给 Claude Code / Cursor 安装集成 skill(Node/Java/Go/Python) | ⚠️ **是 Waffo PSP 产品线,不是 Pancake**,别装错 |
| `@waffo/waffo-stripe-migrate` | — | Stripe-Java 商户迁移 skill | ❌ 同上,PSP 线 |
| `@waffo/pancake-plugin` | `openclaw-setup` / `hermes-setup` | Pancake webhook 投递到 OpenClaw / Hermes | ❌ 不用这两个平台就无关 |

⚠️ **Waffo 有两条产品线,npm 包混在一个 scope 下,极易装错**:
- **Waffo PSP**(`@waffo/waffo-node`、`@waffo/payment-sdk`、`waffo-integrate`)—— 传统收单,需要真实商户资质
- **Waffo Pancake**(`@waffo/pancake-ts`、`@waffo/pancake-nextjs`、`pancake-migrate`)—— **MoR,本项目要用的是这条**

**判断标准:包名里有 `pancake` 才是我们要的。**

想让 AI 直接接,正确做法不是装 CLI,而是把官方 skill 文本喂进来 —— 见上一小节的 prompt。

### New API(已有 LLM 网关项目才相关)

[QuantumNous/new-api](https://github.com/QuantumNous/new-api) 已内建 Waffo Pancake 支付通道:
升级到最新版 → 开启通道 → 后台配置凭证。**与本项目当前主线(工具站)无关,仅备录。**

## 五、禁售与受限类目

**完全禁止**:违禁品与管制药物 · 侵权与假货 · 欺诈与欺骗性经营 · 成人内容与性服务 ·
枪支弹药与危险品 · 赌博与体育博彩 · 无监管加密货币交易所与投机性 NFT · 平台滥用(假身份、拆单规避)。

**受限(需额外审核)**:技能类游戏 · 流媒体 · **AI 生成内容** · 在线教育 · 奢侈品 · 食品 · 酒类 ·
游戏虚拟道具 · **VPN/VPS** · IPTV · **订阅服务**(须有清晰取消条款 + 自动续费明示同意) ·
隐形眼镜 · **软件商店(须为正版授权软件)** · 远程医疗 · 越南数字游戏。

### AIGC 专项合规(只要产品含 AI 生成能力就适用)

1. **独立品牌** —— 不得把自己包装成某个 AI 模型品牌,不得用模型名当产品名
2. **诚实营销** —— 不得夸大能力,不得暗示模型厂商背书
3. **模型披露** —— 必须在 About / Pricing 页或 UI 中明示实际使用的模型,且必须是真实、具体、主流的模型
4. **内容审核是硬要求** —— 生成前(prompt)、生成后展示前、公开发布后三个节点都要扫;需维护涵盖色情/CSAM/版权/暴力/仇恨/深度伪造的屏蔽词表
5. **公开 AUP** —— 必须逐条列出 6 类禁止内容 + 执行机制 + 用户举报渠道 + 审核流程说明

Waffo 提供 **Prompt Sift** 内容安全 API(`/api-reference/endpoints/content-safety/scan-prompt`),返回 Pass / Block / Pending。

## 六、已知陷阱清单

| # | 陷阱 | 规避 |
|---|---|---|
| 1 | **提现 $10 最低费** | 攒到 ≥$1,000 再提;$20 提一次等于交 50% |
| 2 | **KYB 批准后域名锁死** | **先定终版域名再提交审核**,别用临时域名 |
| 3 | **首次提现后身份字段锁死** | legal full name 逐字符核对身份证 |
| 4 | **收款人名不可编辑** | 银行卡 / 支付宝必须与 KYC 本人同名,差一个空格都会失败 |
| 5 | **原交易费不随退款返还**,还另收 $1 | 退款率直接吃毛利,免费额度设计要挡住"试完就退" |
| 6 | Webhook 验签必须用**原始字节** | Next.js 用 `request.text()`,Express 用 `express.raw()`,**绝不能用 `.json()`** |
| 7 | 本地联调用 **localtunnel 会剥掉自定义 header**,`X-Waffo-Signature` 根本收不到 | 换隧道工具。⚠️ 官方两处文档打架:[ai-integration](https://docs.waffo.ai/integrate/ai-integration.md) 推 `cloudflared tunnel --url http://localhost:3000`,[SKILL.md](https://docs.waffo.ai/integrate/skill.md) 推 `ngrok http 3000` —— **两个都行,别用 localtunnel 就对了** |
| 8 | 产品不调 `.publish()` 上不了生产 | 上线前检查;测试产品需同步到生产 |
| 9 | GraphQL 变量类型 | ID 一律用 `String!`,不是 `ID!` |
| 10 | 匿名 checkout 可被刷试用 | 已知买家一律用 `checkout.authenticated.create()` + `buyerIdentity` |
| 11 | **支付宝大额提现会被要求补材料**(24 小时内、最多 10 个文件) | 备好:[Developer Terms](https://www.waffo.ai/developer-terms) + 交易导出 + 发票 + 定价页截图;服务类型选「软件服务」。被拒可**改用银行卡绕过** |
| 12 | 7 天试用订阅首期约亏 $0.50 | $0 授权校验成本,定价时计入 |

## 七、对本项目的落地判定

### ✅ 确认可行

profile.md 记录了三个多月的「无 Stripe 资质 → 自有收款不可闭环」在文档层面成立解除:
**大陆个人 + 身份证 + 国内银行卡 = 可收全球美元、可提现人民币,无需任何海外主体。**

### ⚠️ 需要连带修正的三处

1. **[experiments.md](../experiments.md) CSV → QBO 实验的 GO 标准**
   原文:「第一笔非自己产生的、**可提现**收入到账 ≥ $1」。
   **在 Waffo 下这个标准无法按字面兑现** —— 提现门槛 $20 + 最低 $10 手续费 + 10 个工作日 hold。
   → GO 标准应改为「**Waffo 后台出现一笔非自己产生的 `order.completed`,金额 ≥ $1**」,把「提现」与「验真」解耦。

2. **[profile.md](../profile.md#能力与资源) 里「支持 70+ 币种、300+ 支付方式」这句与文档对不上。**
   文档口径只有:Visa / Mastercard / Apple Pay / Google Pay / 微信支付,checkout 支持 19 种语言。
   → 按文档口径订正,不要拿这条做方向判断。

3. **CSV → QBO 产品撞 Intuit 商标的风险与 KYB 审核直接相关。**
   KYB 明确查 "No trademark conflicts"。QBO / QuickBooks 是 Intuit 商标 ——
   **域名、店铺名、产品名含 QuickBooks 有被拒风险**;把 QBO 当文件格式名描述 + 页面挂
   "not affiliated with Intuit" 免责声明是常规做法。这条与 todos 里「查 Intuit 条款」是**同一件事的两面**,一并解决。

### 推荐的落地顺序(把三关的依赖理顺)

1. **先注册 + 测试模式跑通全链路**(零门槛,不需要任何审核,能立刻验证技术可行性)
2. **定终版域名**(域名批准后锁死)→ 配 `support@<终版域名>`(Cloudflare Email Routing 免费转发即可)
3. **建站**:产品可用 + 定价页公开 + Privacy Policy + ToS(用官方模板)+ 支持邮箱显示在页面上
4. **验证支持邮箱**(6 位码)→ 同域自动解锁**一键域名验证**,省掉 DNS 步骤
5. **提交 KYB**,等 1–3 个工作日
6. **KYC 身份 + 绑卡**(可与 KYB 并行,逐字符核对姓名)
7. 上线收款 → 攒够 $1,000 再提现

第 1 步**今天就能做且零成本**,第 3 步才是真正的工作量所在。

## 实测校准

> 开通后回填:实际过审耗时 / 是否一次过 / 首笔到账时间 / 实际到手金额 / 提现实测。
> **在有实测数字之前,本文件所有内容都只是文档口径,不是真值。**

_(待填)_

---

**最后核实**:2026-08-12 · 来源 `docs.waffo.ai`(官方文档,非自有实测)
