---
title: "另一种名义下的稳定币收益：贝莱德 BRSRV 与 BSTBL 文件解码"
subtitle: "贝莱德的两份 SEC 注册——在 GENIUS 法案下作为货币市场基金而非稳定币运作"
description: "贝莱德 2026 年 5 月 8 日提交两份 SEC 注册——BRSRV 与 BSTBL——通过代币化货币市场基金绕开 GENIUS 法案对稳定币付息的禁令。"
date: "May 15, 2026"
language: "zh-Hans"
locale: "zh_CN"
banner: "https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp"
banner_alt: "贝莱德代币化货币市场基金架构图——BRSRV OnChain Shares 与 BSTBL ERC-20 份额类别，及 GENIUS 法案储备流"
keywords: "贝莱德, BRSRV, BSTBL, GENIUS 法案, 稳定币, 代币化, 货币市场基金, BUIDL, 以太坊, BNY Mellon"
---

GENIUS 法案下稳定币不能支付收益。2026 年 5 月 8 日，贝莱德为两个产品提交 SEC 注册，通过被监管为货币市场基金而非稳定币解决该约束——同时在钱包中表现得像公链上的生息美元。

---

> **核心要点**
>
> - **GENIUS 法案** 于 2025 年 7 月签署，现处于规则制定的最后几个月，禁止支付稳定币发行方仅因持有、使用或保留稳定币向持有者支付利息或收益。OCC 2026 年 3 月的提案进一步加强了这一点，对联属公司和第三方收益安排也违反禁令建立可反驳推定。
> - 由此产生的经济问题直接。约 **2810 亿美元支付稳定币流通** 加上多年高位的国债收益率，钱包持有者所获（零）与底层储备所得（约 4-5%）之间的差距现在每年达到数百亿美元。
> - **2026 年 5 月 8 日，贝莱德提交两份 SEC 注册声明**，在不违反收益禁令的情况下捕捉这一差距——因为两种产品在法律上都不是稳定币。
> - **BRSRV**（贝莱德每日再投资稳定币储备工具）是新货币市场基金，持有现金、93 天以内国债和隔夜国债回购。它通过许可多链框架发行 "OnChain Shares"，Securitize Transfer Agent LLC 作为所有权法律记录。最低投资：300 万美元。它被设计为在 GENIUS 法案下作为合格储备资产。
> - **BSTBL** 是架构上更重要的文件。它在贝莱德现有的 **60-70 亿美元 Select Treasury Based Liquidity Fund** 上加装 ERC-20 份额类别，BNY Mellon Investment Servicing 作为过户代理，在以太坊上记录股东。这是首次在贝莱德现有货币市场产品上添加公开以太坊份额类别。
> - 该模式现在在行业中可见。**代币化货币市场基金是 GENIUS 法案通过禁止稳定币收益使其不可避免的架构。** 140 亿美元代币化国债市场——贝莱德 BUIDL 约占 40% 份额——是下一波"钱包美元"所在的早期解读。

---

## 一份文件也是一种政策立场

贝莱德 2026 年 5 月 8 日的两份文件并非凭空到来。它们在贝莱德 [向货币监理署（OCC）提交十七页评论信 ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter) 的一周后到来——评论期的最后一天，针对 OCC 的 GENIUS 法案实施规则——并且在贝莱德 [在 X 上发布七项核心建议公开摘要 ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/) 后四天。

建议和新文件最好作为两部分的一份文件来阅读。评论信认为 OCC 应放弃其拟议的 20% 代币化储备资产上限，确认合格 ETF 获得与政府货币市场基金相同的待遇，并允许当日结算 GMMF 计入每周流动性下限。四天后的文件注册了从这些立场中受益的精确工具：一个新基金（BRSRV），明确设计为在 GENIUS 法案下作为合格储备，以及在公司现有 60-70 亿美元国债流动性基金之上的代币化份额类别（BSTBL）。

这是看似巧妙的法律工程的战略背景。它更准确地解读为世界上最大的资产管理公司宣布美国法律中"稳定币"与"代币化证券"之间的界线应该在哪里——并注册将位于该线两侧的产品。

## 为何稳定币不能支付收益

GENIUS 法案于 2025 年 7 月签署，现在是重叠的 OCC、FDIC 和美联储规则制定的基础，划出异常清晰的概念区分。该法案下的"支付稳定币"是旨在相对法定货币保持稳定价值、由高质量储备支持、按面值赎回的数字资产。"许可支付稳定币发行方"（PPSI）是被授权发行此类代币的联邦或州特许实体。[该法案第 4(a)(11) 节 ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act) 禁止任何 PPSI 仅因持有、使用或保留稳定币而向持有者支付利息或收益。

OCC 2026 年 3 月的 [拟议规则 ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act) 在操作上延伸了这一禁令。它建立了一种可反驳推定，即通过联属公司或相关第三方路由收益的安排——例如，加密交易所向特定稳定币持有者支付"忠诚奖励"——也违反禁令，由发行方承担证明否则的责任。

该禁令的经济理由有争议。银行业向 OCC 的提交认为，生息稳定币会从交易性银行存款中抽走资金——该市场由 [美国财政部咨询委员会估计约为 6.6 万亿美元 ⧉](https://www.congress.gov/crs-product/IF13174)。加密行业的提交，由 Coinbase 牵头，认为相反：激励是支付竞争的核心。

无论哪一方有更好的政策论点，目前的法律结果已定：GENIUS 法案监管意义上的稳定币不能向其持有者支付收益。然而，它不能做的是定义持有者下一步可以用他们的钱做什么。这里架构发生分歧。

## BRSRV 的架构

贝莱德每日再投资稳定币储备工具，在其管道上是一个不起眼的货币市场基金。它持有现金、到期 93 天或以下的美国国债证券，以及国债支持的隔夜回购协议。它与 1940 年投资公司法下的规则 2a-7 对齐——这是四十年来管理机构货币市场基金的相同监管架构。其收益与每个其他政府 MMF 一样，源自现行短期国债利率。

新颖的是份额类别。BRSRV 份额作为 ["OnChain Shares" 通过许可框架发行 ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/)，连接到多个公共区块链，[Securitize Transfer Agent LLC 作为官方过户代理 ⧉](https://www.crowdfundinsider.com/2026/05/278346-blackrock-focuses-on-tokenization-initiatives-with-blockchain-enabled-funds/)。链下身份系统——支持贝莱德现有 29 亿美元 [BUIDL 基金 ⧉](https://stablecoininsider.org/top-10-tokenized-treasury-funds-in-2026-buidl-benji-and-the-highest-yielding-on-chain-options/) 的相同 KYC 基础设施——将钱包地址链接到已验证投资者。最低投资：300 万美元。

该产品明确设计为在 GENIUS 法案下作为合格储备资产。目标买家不是零售钱包用户。是稳定币发行方（或将稳定币作为营运资金策略一部分的财库运营）——需要可在与稳定币本身相同区块链通道上以编程方式持有的国债收益工具。

对贝莱德，战略立场比表面看更锐利。其现有 BUIDL 基金已支持两个最大的"生息"稳定币邻近产品超过 90% 的储备——Ethena 的 USDtb 和 Solana 上的 Jupiter 的 JupUSD。BRSRV 是该角色的专门、GENIUS 感知扩展。

## BSTBL 的架构

第二份文件在操作上更有趣，在架构上更重要。BSTBL——贝莱德现有 Select Treasury Based Liquidity Fund 的链上份额类别——不是新基金。它是层叠到已管理约 60-70 亿美元资产的货币市场产品上的新份额类别，2025 年 10 月 [被改装为 GENIUS 合规配置 ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter)，截止下午 5 点东部时间交易，并具有国债主导授权，现在作为 ERC-20 代币扩展到以太坊上。

该份额类别的过户代理是 [BNY Mellon Investment Servicing ⧉](https://www.mexc.com/news/1080472)，它将使用 ERC-20 标准在以太坊上维护官方股东记录。与 BRSRV 的实质区别是链（以太坊，公共，ERC-20 代币作为份额表示）和过户代理（BNY 而非 Securitize）——以及这是首次在贝莱德现有货币市场基金上加装公开以太坊份额类别。

那最后细节值得驻足。贝莱德之前的代币化产品——最著名的 BUIDL——结构为具有链上原生架构的新基金。BSTBL 采取不同且可能更具影响的方法：通过添加新份额类别将现有的、大型的、传统的货币市场产品代币化，而不是构建并行结构。意义是任何现有贝莱德 MMF 原则上都可以遵循相同模式。任何现有竞争对手 MMF 也可以——Vanguard 的、Fidelity 的、摩根大通的、State Street 的。

行业背景：代币化美国国债已从约 20 亿美元增长到 [2026 年 5 月的 140 亿美元 ⧉](https://www.mexc.com/news/1080472)，贝莱德的 BUIDL 约占 40% 市场份额，富兰克林邓普顿的 BENJI/FOBXX 为 8.5 亿美元，Ondo Finance 的 OUSG 和 USDY 产品综合居第二。下一波 500-1000 亿美元可能已经通过 BSTBL 等文件在运动中。

## 支付稳定币 vs 代币化货币市场基金：重要的区别

对非专业读者，"稳定币"与"代币化货币市场基金份额"之间的区别可能看起来像监管技术细节。它不是。这两种工具在美国证券法中占据真正不同的位置，后果贯穿整个产品设计。

| 维度 | 支付稳定币（GENIUS 法案下） | 代币化 MMF 份额（BRSRV / BSTBL 模式） |
|---|---|---|
| 法律地位 | 支付工具 | 证券（基金份额） |
| 监管制度 | GENIUS 法案；OCC/FDIC/Fed 规则制定 | 1940 年投资公司法；规则 2a-7 |
| 发行方 | 许可支付稳定币发行方（PPSI） | SEC 注册基金（及过户代理） |
| 储备要求 | 现金、短期国债、回购——严格 | 现金、短期国债、回购——规则 2a-7 |
| 可向持有者支付收益 | **否**（第 4(a)(11) 节） | **是**（收益是份额的回报） |
| 赎回 | 按面值，按需 | 按 NAV，通常 T+0 或 T+1 |
| 所有权记录 | 发行方钱包/链上 | 过户代理（法律）；区块链（操作） |
| 最低投资 | 无（零售典型） | 实质（BRSRV 为 300 万美元；BSTBL 为机构） |
| 与 DeFi 的可组合性 | 高 | 高（BUIDL 是先例） |
| 钱包中的用户体验 | 持有 1 美元的代币 | 价值向收益累积的代币 |
| 银行存款替代风险 | 中央监管关切 | 实质上更低（证券，非类存款） |

*来源：GENIUS 法案文本、OCC 2026 年 3 月 NPRM、贝莱德 2026 年 5 月 8 日文件以及规则 2a-7 框架的综合。*

底行解释监管架构。支付收益的支付稳定币对银行监管者看起来像存款替代品。支付收益的代币化货币市场基金份额看起来像证券——证券与存款竞争不是新关切，因为传统货币市场基金正好做了 40 年。

## 这是漏洞吗？

诱人——自文件以来该框架已在 LinkedIn 和加密 Twitter 上广泛出现——称这是 GENIUS 法案的"漏洞"：稳定币不能支付收益，所以贝莱德提交了一些法律上不是稳定币的东西。该框架巧妙捕捉头条。作为法律特征化，它低估了实质。

GENIUS 法案中的收益禁令是具有特定目标的特定政策选择：对银行业的存款替代风险——来自旨在作为货币运作的一类工具。代币化货币市场基金不旨在作为货币运作；它们旨在作为基金份额运作，具有数十年来适用于该类别的所有监管重量（规则 2a-7、审计储备、NAV 披露、过户代理所有权法律记录）。

真正新颖的是用户体验。公链上钱包中的代币化 MMF 份额持有者拥有看起来*像*稳定币（可替代代币、点对点可转让、与 DeFi 基础设施可组合）但*行为*像证券（NAV 累积、持有者在 KYC 名单上、过户代理记录具有法律控制力）的东西。头条框架——"法律上不是稳定币"——就其而言是正确的。更深层的观察是 GENIUS 法案通过禁止支付稳定币类别的收益，有效地*要求*行业聚合到代币化 MMF 作为生息链上美元的载体。

## 按行业意味着什么

5 月 8 日文件的意义并不均匀。战略响应根据机构在价值链中的位置实质性变化。

### 稳定币发行方（PPSI）

对 Circle、Tether、PayPal 和下一代银行发行的支付稳定币，BRSRV 是迄今只有特别答案的问题的操作答案：储备何处坐落，当它们需要既国债收益又原生于与发行稳定币相同链上。

### 银行和货币市场基金运营商

对运营大型货币市场基金特许经营的银行——摩根大通、State Street、BNY Mellon、Northern Trust、Vanguard、Fidelity——BSTBL 是其自己产品可能必须做的操作模板。

### DeFi 协议和链上财库

对 DeFi 协议，BRSRV 和 BSTBL 扩展了 BUIDL 开始的模式：高质量国债抵押品从链下托管账户迁移到可与借贷、衍生品和结构化产品组合的链上工具。

### 监管机构

对 OCC、FDIC 和美联储，5 月 8 日文件澄清了监管边界被要求容纳什么。

## 结论

2026 年 5 月 8 日的文件本身不是范式转变。它们是来自单一资产管理公司的个别产品，在 OCC 规则制定打开的特定监管窗口提交。它们所捕捉的是自贝莱德 2024 年 3 月推出 BUIDL 以来可见的、GENIUS 法案现在加速而非约束的行业级过渡的形状。

GENIUS 法案意义上的稳定币将继续做稳定币一直擅长的：高效结算、近乎即时跨境支付、需要稳定记账单位的用例的可编程货币。在当前和拟议规则下，它们不会向其持有者支付收益。钱包中的生息美元——与稳定币采取相同形式因素但向持有者累积国债收益的产品——将是代币化货币市场基金份额，由注册基金发行，过户代理（Securitize、BNY Mellon 和可能的其他几家）作为所有权法律记录。BRSRV 和 BSTBL 是该模式的早期机构表达。它们不会是最后。

## 常见问题

**BRSRV/BSTBL 与 USDC 等稳定币之间的实际区别是什么？**

在钱包中，区别大部分不可见。每个都是公共区块链上的可替代代币，可赎回美元（或基础基金份额价值），与 DeFi 可组合。在法律上，区别是实质性的。USDC 是 GENIUS 法案下的支付稳定币，由许可支付稳定币发行方发行，禁止向持有者支付收益。BRSRV 和 BSTBL 是 1940 年投资公司法下注册货币市场基金的份额类别，在规则 2a-7 下监管，其中收益是份额的自然回报。

**如果两者都是以太坊上的代币化贝莱德基金，BSTBL 与 BUIDL 有何不同？**

BUIDL 于 2024 年 3 月推出，结构为从一开始就具有链上架构的新基金，Securitize 作为合作伙伴，设计原生于数字资产工作流。相比之下，BSTBL 是添加到现有 60-70 亿美元传统货币市场基金（Select Treasury Based Liquidity Fund）的新链上份额类别。BNY Mellon 作为过户代理。架构意义是 BSTBL 演示了如何将现有的、大型的、传统的货币市场产品带到链上而不将其重建为新基金。

**为何 OCC 对代币化储备的 20% 上限有争议？**

OCC 2026 年 3 月的提案漂浮了对稳定币发行方储备多少可以代币化形式持有的潜在 20% 限制。贝莱德的评论信认为这对 OCC 的监督目标"无关"，因为储备资产的风险概况由信用质量、期限和流动性驱动——而不是由是否在分布式账本上持有或转移驱动。

**BRSRV 文件不命名将支持的区块链意味着什么？**

这是早期 SEC 文件的常规特征而非战略模糊。该文件建立法律结构（注册基金通过 Securitize 作为过户代理的许可框架发行 OnChain Shares），而不承诺特定链——贝莱德可能将更接近发布时宣布。

**这是生息稳定币作为产品类别的终结吗？**

它是生息支付稳定币作为类别的终结，至少在美国联邦法下，除非国会修订 GENIUS 法案。它不是生息链上美元作为产品类别的终结——这是用户实际想要的。该类别现在正在迁移到代币化货币市场基金份额——BUIDL、BENJI、BRSRV、BSTBL、Ondo 的产品以及 BSTBL 模式可能催化的竞争代币化 MMF 浪潮。

## 参考资料

- Sebastien Rousseau, (2026). [2026 年 11 月 pacs.008 结构化地址截止日期](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html)。
- Sebastien Rousseau, (2018). [ERC-20：改变世界的以太坊代币接口](https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html)。
- Sebastien Rousseau, (2018). [理解区块链背后的技术](https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html)。
- Sebastien Rousseau, (2018). [推出新的加密货币和更快支付方案](https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html)。
- Unchained, (2026). [贝莱德为两个新代币化货币市场基金提交申请，目标稳定币资本 ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/)。Unchained.
- The Block, (2026). [贝莱德敦促 OCC 放弃代币化储备上限想法 ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter)。The Block.
- BeInCrypto, (2026). [贝莱德支持 GENIUS 法案下的 OCC 稳定币规则 ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/)。BeInCrypto.
- CoinDesk, (2026). [贝莱德加深代币化推进 ⧉](https://www.coindesk.com/business/2026/05/09/blackrock-deepens-tokenization-push-with-new-onchain-fund-offerings)。CoinDesk.
- Crypto Briefing, (2026). [贝莱德加倍代币化 ⧉](https://cryptobriefing.com/blackrock-tokenized-money-market-funds-stablecoins/)。Crypto Briefing.
- Latham & Watkins, (2026). [OCC 发布 GENIUS 法案实施提案 ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act)。Latham & Watkins.
- Nixon Peabody, (2026). [GENIUS 法案下支付稳定币的拟议 OCC 法规 ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act)。Nixon Peabody LLP.
- Morgan Lewis, (2026). [稳定币监管：GENIUS 法案下的 OCC 提案 ⧉](https://www.morganlewis.com/pubs/2026/04/occs-genius-act-proposal-what-prospective-issuers-need-to-know)。Morgan Lewis.
- 国会研究服务, (2026). [稳定币收益辩论 ⧉](https://www.congress.gov/crs-product/IF13174)。Congress.gov.
- MEXC News, (2026). [贝莱德为两个新代币化基金向 SEC 提交申请 ⧉](https://www.mexc.com/news/1080472)。MEXC News.
- Stellar 基金会, (2026). [富兰克林邓普顿 BENJI 五周年 ⧉](https://stellar.org/press/franklin-templeton-stellar-development-foundation-mark-five-years-of-benji-the-first-u-s-registered-tokenized-money-market-fund)。Stellar Development Foundation.
