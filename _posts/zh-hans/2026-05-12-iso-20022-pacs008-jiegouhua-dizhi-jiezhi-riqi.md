---
title: "2026 年 11 月 pacs.008 结构化地址截止日期：六个月视角"
subtitle: "SWIFT CBPR+ 将拒绝非结构化邮政地址——结构化地址截止日期对跨境支付的影响"
description: "2026 年 11 月起 SWIFT CBPR+ 拒绝 pacs.008 中的非结构化地址。约 65% 报文仍不合规，44% 银行进度滞后。"
date: "May 12, 2026"
language: "zh-Hans"
locale: "zh_CN"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "ISO 20022 pacs.008 结构化地址图——突出 TwnNm 和 Ctry 字段的跨境支付报文"
keywords: "ISO 20022, pacs.008, 结构化地址, SWIFT, CBPR+, SR2026, 跨境支付, 制裁筛查, pain.001, 银行业"
---

自 2026 年 11 月中旬起，SWIFT CBPR+ 将拒绝 pacs.008 与相关跨境支付报文中的非结构化邮政地址。约 65% 报文仍不合规，44% 银行进度滞后，整改窗口比多数就绪项目设计的更快关闭。

---

> **核心要点**
>
> - 从 **2026 年 11 月** 起，SWIFT CBPR+ 将不再接受跨境支付报文中的非结构化邮政地址。该变化适用于 **pacs.008**（客户信用转账）、**pacs.009**（FI 信用转账）、**pacs.004**（退回）、**pacs.003**（直接借记），以及向其供数的上游 **pain.001** 流。
> - 至少 **城市名（TwnNm）** 和 **国家（Ctry）** 必须存在于专用结构化字段中。**街道名（StrtNm）** 以及 **建筑编号（BldgNb）** 或 **邮政信箱（PstBx）** 强烈建议提供。仅靠自由文本地址行（AdrLine）将不再满足关键当事方字段的要求。
> - 该变化提高制裁筛查准确性、降低人工修复率并保护直通处理——但仅对那些已整改上游客户数据（而不仅是报文引擎）的机构有效。
> - 行业就绪情况不平衡。截至 2026 年 3 月，约 **65% 的 CBPR+ 报文仍承载非结构化地址**，**44% 的银行** 进度滞后，平均 **32% 的客户地址记录** 仍未结构化。
> - 开源工具——包括 **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 工具包和 API")**，一个用于生成、验证和编排 pacs.008 报文流的 Python 库和 FastAPI 服务——可在报文到达 SWIFT 网络前通过自动化模式验证、地址质量检查和 CI 级强制执行压缩整改时间线。

---

## 一个早就要来的截止日期

2026 年 11 月的结构化地址要求并非突然的监管举措。它从原始 [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) 迁移宣布以来一直在 SWIFT CBPR+ 路线图上，紧随 2025 年 11 月 MT/MX 共存的结束。2026 年改变的是临近度。约剩六个月，业界现处于未解决数据质量问题成为运营风险的窗口内。

数据明白地讲述故事。SWIFT 自身 2026 年 3 月社区更新指出 [约 65% 支付报文仍包含非结构化地址 ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed)，且采用在地域与机构类型间不均。2026 年 3 月 [RedCompass Labs 对 308 位资深支付专业人士的调查 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022) 发现，44% 的银行目前进度滞后，无法满足结构化地址截止日期——尽管平均花费 2000 万美元（最大机构超 3000 万美元）于 2026 年就绪，平均额外指派 13 名员工到 ISO 20022 项目。同项调查发现平均 32% 的客户地址记录仍未结构化，60% 的银行报告核心银行系统在支持结构化地址字段时存在缺口。

换言之，这不是再加一个月报文引擎工作就能解决的问题。这是从报文层向上游运行到入网系统、KYC 流程、企业渠道及数十年累积的自由文本客户主数据中的数据质量问题。

## 规则实际要求什么

根据 SWIFT CBPR+ 标准发布 2026（SR2026），关键要求原则上简单明了，细节上不容差错。从 2026 年 11 月中旬起，CBPR+ 支付报文中所有代理和当事方的 [城市名和国家必须在指定结构化字段中提供 ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed)，例外极为有限（camt.052、camt.053、camt.054 的对账单和通知，加上少数行政报文仍在严格要求之外）。对代理，仅继续使用 BIC 仍是名称-地址的有效替代。

截转后允许两种地址格式：

- **完全结构化** —— 邮政地址每个组件映射到其专用 ISO 20022 元素：StrtNm（街道名）、BldgNb（建筑编号）或 BldgNm（建筑名）、PstCd（邮政编码）、TwnNm（城市名）、CtrySubDvsn（国家细分）、Ctry（国家，ISO 3166-1 alpha-2 代码）。这是 SWIFT 明确确定为可能时更可取的选项格式。
- **混合** —— 城市名和国家填充于其结构化字段，地址其余部分可使用最多两个非结构化 AdrLine 元素。重要的是，[结构化元素不得在非结构化行中重复 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf)；对任何给定组件，地址只能是其一。

完全非结构化地址——整个地址坐落于 AdrLine 元素中且无 TwnNm 或 Ctry——将不被接受用于任何受影响当事方字段。欧洲支付理事会已将其 SEPA 规则书对齐至同一截转，因此 [从 2026 年 11 月 15 日起，SCT、SDD 和 SCT Inst 也将禁止非结构化格式 ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/)。对齐是刻意的：SWIFT 和 EPC 已设计了单一行业截转周末。

为消除疑虑，[pacs008 文档直接列出受影响报文 ⧉](https://pacs008.com/structured-address/)：pacs.008（客户信用转账中的债务人和债权人）、pacs.009（FI 信用转账和代付中的机构地址）、pacs.004（退回中的当事方地址）和 pacs.003（直接借记）。要求也流向上游：承载非结构化地址的企业 pain.001 文件将在收款行阻塞合规 pacs.008 生成。

## 为何行业将此作为优先事项

结构化地址的理由不是美学。是运营性的，并体现在三处。

**制裁筛查。** 单一最大的实际收益是结构化地址让筛查系统将当事方名称与位置数据分开。自由文本地址块在城市名碰巧与被制裁人名 token 重叠或自由文本中嵌入的国家被完全错过时常造成误报。结构化字段让筛查引擎确定性地应用国家特定风险规则，使针对国家代码而非猜测解析字符串执行制裁名单匹配成为可能。CGI UK 2026 年 3 月发布的分析明确强调这一点：[结构化地址数据正在成为运营韧性的核心，而不仅是合规义务 ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement)。

**人工修复率。** 今天的跨境支付以人工调查、异常处理和修复队列形式承担显著运营成本——其中很多由筛查或路由系统无法自信解析的地址驱动。已迁移到结构化地址的银行报告直通处理异常显著降低，特别是在中间走廊流，其中中介代理此前必须解释他们未发起的自由文本数据。

**网络级强制执行。** SR2026 在 SWIFT 网络层加强验证。一些新检查最初将以非阻塞模式运行——标记数据质量问题但不停止支付——但轨迹明确，截转后，[不符合规范的报文将被直接拒绝 ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/)。几个美国支付通道（Fedwire、CHIPS）和 SWIFT CBPR+ 正趋同于本质上相同的时间表，消除了一些机构在早期计划中假定的分阶段截转选项。

## 字段级视图：报文中变化的内容

pacs.008 报文自 2023 年 3 月初始 CBPR+ 使用指南上线以来就已承载结构化地址支持。2026 年 11 月变化的不是模式——是验证。迄今为止，银行被允许用自由文本填充 AdrLine 元素并通过网络传递。从截止日起，当事方块的内容必须满足最低结构化字段要求。

### 必需、推荐与停用

| 元素 | XPath（在 `PstlAdr` 下） | 2026 年 11 月后状态 | 注释 |
|---|---|---|---|
| 城市名 | `<TwnNm>` | **强制** | 每受影响当事方至少一个结构化城市名 |
| 国家 | `<Ctry>` | **强制** | ISO 3166-1 alpha-2 代码 |
| 街道名 | `<StrtNm>` | 强烈推荐 | 完全结构化格式所需 |
| 建筑编号 | `<BldgNb>` | 推荐 | BldgNb 或 PstBx 二者其一，不能同时 |
| 邮政信箱 | `<PstBx>` | 推荐 | BldgNb 的替代 |
| 邮政编码 | `<PstCd>` | 推荐 | 某些本地方案要求 |
| 国家细分 | `<CtrySubDvsn>` | 可选 | 州、地区、省份 |
| 地址行（自由文本） | `<AdrLine>` | **受限** | 混合下最多 2 行；从不与结构化字段中相同组件并存 |
| 地址类型 | `<AdrTp>` | 可选 | 邮政地址推荐使用 `ADDR` |

*来源：SR2026 SWIFT CBPR+ 使用指南与 [pacs008.com 结构化地址文档 ⧉](https://pacs008.com/structured-address/) 的综合。*

实际意义是：任何仍仅依赖 AdrLine 的机构——无论是自己的报文生成、从企业客户接收的 pain.001 文件中，或是飞行中丰富支付所用的主数据记录——都需要在截转前将该数据迁移到结构化字段。SWIFT 的飞行中翻译服务可在过境中帮助，但 [自 2026 年 1 月起收取附加费 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq)，且无法可靠解析每种地址格式。SWIFT 也发布了 [一个开源 AI 地址结构化模型 ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model)，基于 200 多个国家数据训练，可从非结构化遗留数据推断城市和国家并附带信心分数，但它明确是整改辅助工具，而非干净上游数据的长期替代。

## pacs008.com 如何帮助压缩时间线

对需要快速工业化其地址质量和报文验证管道的机构，[pacs008 ⧉](https://pacs008.com/) 提供专门为 FI 到 FI 客户信用转账工作流设计的 MIT 许可开源工具包和 FastAPI 服务。它解决整改项目最常停滞的三层：数据验证、XML 生成和管道强制执行。

该工具包的结构化地址能力与 SR2026 要求一致：

- **预生成验证** 结构化和混合邮政地址字段，使不合规数据在任何 XML 产生或发送前被捕获。
- **标记非结构化地址数据**——会在 2026 年 11 月截止日期后失败的数据，明确区分混合可接受和完全非结构化情况。
- **双格式支持** 既支持截止日期前混合格式，也支持截止日期后完全结构化布局，让机构能在不破坏与尚未完成自身过渡的对手方互操作性的情况下渐进迁移。
- **CI 管道集成**，使地址质量检查成为构建过程的一部分，而不是流程末端的事后想法——这是对 [CGI 观察的实际答复，即数据治理必须是基础设计原则 ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement) 而非合规叠加。

除地址外，工具包涵盖 SR2026 发布所加强的更广泛验证表面：针对 20 个报文特定模式的 JSON 模式验证、跨 75 个国家的 IBAN 格式和校验和验证、针对官方 ISO 20022 模式生成 XML 的 XSD 验证，以及跨所有 13 个支持 pacs.008 修订（pacs.008.001.01 到 pacs.008.001.13）的版本感知生成。对运营和合规团队，它还包括通过 defusedxml 防止 XXE、严格路径遍历保护以及结构化 JSON 日志中的 PII 屏蔽以支持 GDPR 和 PCI DSS 要求——这是生产支付流中不可协商但常被供应商主导迁移晚期改装的控制。

该库 [在 PyPI 上 ⧉](https://pypi.org/project/pacs008/) 作为 `pip install pacs008` 包提供，并在 [GitHub ⧉](https://github.com/sebastienrousseau/pacs008) 上提供完整源代码透明度。

需要精确说明范围。pacs008 是报文层工具包；它不替代支付引擎、筛查系统或机构仍需在源头进行的客户主数据整改。它做的是把整改工作变得可强制执行——将结构化地址合规从长管道末端的人工审查变为生成点的自动门。对时间紧迫的项目，该门是干净截转与截转后激增拒绝之间的差别。

## 工具景观

pacs008 位于 ISO 20022 报文工具更广生态系统中，方法选择取决于机构的栈、规模和迁移哲学。开源和商业景观包括 [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022)（广泛多类别 Python 库，带 beta 验证）、相关的 [pain001 ⧉](https://pain001.com/) 库用于上游支付发起、[Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022)（带 CBPR+ 验证和翻译商业层的全面 Apache 2.0 Java 库）以及多个商业平台——Mambu、Kyriba、PaymentComponents 等——它们将 ISO 20022 能力捆绑到更广财库或支付平台产品中。

权衡是熟悉的。商业平台降低内部工程负担但将机构绑定到可能不匹配自身的供应商路线图。全面多类别库覆盖更广表面但要求任何单一报文类型更多集成工作。聚焦开源库——pacs008 用于 FI 到 FI 客户信用转账，[pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) 用于支付发起——最小化需要快速解决特定瓶颈的机构的集成时间，让机构掌控自己的验证规则。

## 按行业意味着什么

2026 年 11 月截止日期对所有机构影响不均。正确响应取决于跨境流量量、现有数据资产成熟度以及机构在支付链中扮演的角色。

### 大型代理和跨境银行

对运行显著 CBPR+ 流量的一级银行，结构化地址要求是更大 SR2026 就绪项目中的一个工作流，该项目还涵盖异常和调查、BAH 强化以及（在美国）Fedwire 和 CHIPS 的同时迁移。RedCompass Labs 数据显示大多数这些机构在 2026 年就绪上花费 2000–3000 万美元，交付团队 10–20 名专家。该组的风险不是技术能力——是交付容量。

### 中型银行和支付机构

对中型银行和 EMI/PI 机构，结构化地址要求通常是它们面临的最重大 2026 义务，因为它们不承担像一级银行同样的周围工作流负担。这里的挑战通常是上游数据质量。

### 企业和支付服务提供商

通过 pain.001 发起支付的企业位于银行 pacs.008 生成上游，但不豁免结构化地址要求。银行不会代表企业客户追溯填充受益人地址；结构化数据必须源于企业自己的系统。

### 供应商、金融科技和系统集成商

对在支付通道之上构建的供应商，截止日期是 ISO 20022 能力的强制功能，这能力可能被推迟到稍后阶段。

## 结论

2026 年 11 月结构化地址截止日期在一种意义上是狭窄变化：两个必需字段、几个推荐字段，以及一个本不应用于制裁相关数据的自由文本选项的退役。在另一意义上，它是原始 CBPR+ 迁移以来运营上最显著的 ISO 20022 里程碑，因为它强制结构化数据不仅进入报文层，还进入向其供数的上游系统。

六个月前的行业级就绪图景并不令人鼓舞。三分之二的 CBPR+ 报文仍承载非结构化地址。近一半的银行进度滞后。近三分之一的客户地址记录仍无法解析。资金已到位——调查一致显示八位和九位数投资——但工作尚未完成，问题的数据质量维度无法仅靠最后几个月的支出解决。

现在有帮助的是验证点的自动化：将规则推到管道中，在问题到达网络前而不是之后捕获它们。对运行 Python 或 FastAPI 资产的机构，[pacs008 ⧉](https://pacs008.com/) 等开源工具提供无需供应商选择周期就能做出该转变的实用方式。

11 月的截转周末将关闭一章。带着干净数据、自动化验证和对结构化地址实际为制裁筛查所做工作的工作理解到达的机构将在该周末监控流量。没有这些到达的机构将在电话上度过它。

## 常见问题

**2026 年 11 月截止日期到底变化什么？**

从 2026 年 11 月中旬起，SWIFT CBPR+ 将拒绝其当事方字段包含仅非结构化邮政地址的 pacs.008、pacs.009、pacs.004 和 pacs.003 报文。最低结构化要求是 TwnNm 元素中的城市名和 Ctry 元素中的国家（使用 ISO 3166-1 alpha-2 代码）。仍允许混合地址——城市和国家在结构化字段中，加上最多两个用于其余组件的自由文本 AdrLine 元素——但同一组件不能同时出现在结构化和非结构化字段中。完全结构化地址是首选格式。

**哪些报文和哪些当事方字段受影响？**

对 pacs.008，要求适用于债务人和债权人邮政地址。对 pacs.009，适用于 FI 信用转账和代付中的机构地址。对 pacs.004，适用于支付退回中的当事方地址。对 pacs.003，适用于客户直接借记中的债权人和债务人地址。对账单和通知报文（camt.052、camt.053、camt.054）和某些行政报文仍在严格要求之外。

**结构化、混合和非结构化地址有何区别？**

完全结构化地址将每个组件映射到其专用 ISO 20022 元素：StrtNm、BldgNb 或 PstBx、PstCd、TwnNm、CtrySubDvsn、Ctry。混合地址在结构化字段中有城市名和国家，地址其余部分在最多两个自由文本 AdrLine 元素中；同一组件不得同时出现在两者中。非结构化地址在 AdrLine 元素中有整个邮政地址而无结构化 TwnNm 或 Ctry——这是 2026 年 11 月针对受影响当事方字段被退役的格式。

**pacs008.com 如何帮助这一过渡？**

[pacs008 ⧉](https://pacs008.com/) 库在 XML 生成前验证结构化和混合邮政地址字段，标记在截止日期后会失败的非结构化数据，支持截止日期前混合和截止日期后完全结构化格式，并集成到 CI 管道和批量验证工作流。它为所有 13 个支持 pacs.008 版本生成 XML，验证官方 ISO 20022 XSD 模式，并暴露 FastAPI 服务用于自动编排。

**如果我的机构在 2026 年 11 月未就绪会怎样？**

截转后，受影响当事方字段中带非结构化地址的报文将在网络级被拒绝。实际上这转化为支付失败、异常量增加、人工修复激增以及可能的客户影响。SWIFT 的飞行中翻译服务对一些过渡情况可用但自 2026 年 1 月起收取附加费且无法可靠解析每种地址格式。

## 参考资料

- Sebastien Rousseau, (2023). [用 pain001 自动化 ISO 20022 合规支付文件创建](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)。
- pacs008, (2026). [2026 年 11 月结构化地址截止日期 ⧉](https://pacs008.com/structured-address/)。pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 工具包和 API ⧉](https://pacs008.com/)。pacs008.com.
- SWIFT, (2026). [2026 年 11 月 ISO 20022 里程碑：非结构化地址将被移除 ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed)。SWIFT.
- SWIFT, (2026). [面向金融机构的 ISO 20022 ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions)。SWIFT.
- SWIFT, (2026). [SWIFT AI 地址结构化模型 ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model)。SWIFT.
- RedCompass Labs, (2026). [近一半银行 ISO 20022 进度滞后 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022)。Financial IT.
- RedCompass Labs, (2026). [ISO 20022 对美国银行一齐到来 ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/)。RedCompass Labs.
- ClearingPost, (2026). [2026 年 11 月结构化地址截止日期 ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/)。ClearingPost.
- CGI UK, (2026). [2026 年：ISO 20022 和结构化数据强制的决定性一年 ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement)。CGI UK.
- J.P. Morgan, (2026). [ISO 20022 迁移：指导、报文及更多 ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration)。J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022)。ING Wholesale Banking.
- Mambu, (2026). [CBPR+ 已上线 ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice)。Mambu.
- Kyriba, (2026). [ISO 20022 迁移：每个财库团队需要了解的下一步 ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/)。Kyriba.
- Standard Chartered, (2025). [ISO 20022 – 渣打地址指南 ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf)。Standard Chartered.
- State Street, (2025). [客户 ISO 20022 指南 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf)。State Street.
- ISO 20022, (2026). [报文定义目录 ⧉](https://www.iso20022.org/iso-20022-message-definitions)。ISO 20022.
