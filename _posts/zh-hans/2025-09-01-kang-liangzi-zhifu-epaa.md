---
title: "抗量子支付：行业必须立即行动（EPAA）"
subtitle: "为何支付行业必须现在采取行动应对量子威胁"
description: "EPAA 量子安全支付白皮书阐述支付行业为何必须立即采取行动应对量子威胁。"
date: "September 1, 2025"
language: "zh-Hans"
locale: "zh_CN"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "蓝色光线下的量子计算电路板"
keywords: "EPAA, 抗量子支付, 后量子密码学, ML-KEM, ML-DSA, SWIFT, SEPA, HNDL, NIST, FIPS 203"
---

## 量子对支付系统的威胁

现代支付基础设施依赖公钥密码学——RSA、ECC 和 Diffie-Hellman——来认证交易、保护持卡人数据并保障金融机构之间的消息安全。这些算法支撑 SWIFT、SEPA、实时全额结算系统以及目前运行的几乎所有卡组织。

运行 Shor 算法的量子计算机将能够破解这些密码原语。虽然容错量子机器尚未达到所需规模，但 IBM、Google 等所展示的硬件发展轨迹使这成为工程时间表问题而非理论问题。美国国家标准与技术研究院（NIST）已对此作出回应，定型了其首批后量子密码标准（FIPS 203、204 和 205）。

## "现在收集、未来解密"的风险

威胁并不局限于量子计算机达到足够能力的未来日期。国家级行为者和资深对手已经在拦截并存储今天的加密数据，意图在量子资源可用时解密。这种"现在收集、未来解密"（HNDL）策略意味着任何具有长期敏感性的支付数据——监管记录、合规档案、合同义务——已经处于风险中。

金融监管机构已开始响应。新加坡金融管理局（MAS）已发布关于量子就绪的指引。澳大利亚审慎监管局（APRA）已在其技术韧性框架中标记密码风险。欧盟数字运营韧性法案（DORA）要求 ICT 风险管理必须考虑包括量子计算在内的新兴威胁。

## 跨支付通道的影响

意义跨越支付基础设施的全部广度：

**SWIFT 消息：** MT 和 MX 消息格式依赖 TLS 和数字签名保证完整性与认证。受损的密钥基础设施将破坏连接全球超过 11,000 家机构的信任模型。

**SEPA 和即时支付：** 欧洲支付理事会的 SEPA 即时信用转账方案在十秒内处理不可撤销的交易。在此速度下的密码学受损不会留下人工干预或手动验证的窗口。

**实时支付系统：** 英国的 Faster Payments、美国的 FedNow 和澳大利亚的 NPP 都共享对经典密码原语在消息认证和参与者验证上的依赖。

**合规与长寿命数据：** 出于监管目的保留的支付记录——通常被要求保留 5 至 10 年或更长——将比保护它们的密码学的安全保证活得更久。[ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) 迁移项目必须考虑其产生数据的密码学保质期。

**区块链与分布式账本技术：** 依赖椭圆曲线密码学的数字资产平台和代币化支付工具面临来自量子算法的直接且已知威胁。

## 组织现在必须做什么

向量子安全密码学的过渡不是单次升级，而是需要结构化准备的多年项目：

**密码学清单：** 组织必须编目依赖经典公钥密码学的每个系统、协议和数据存储。这包括 TLS 证书、API 认证、HSM 配置、密钥管理系统和静态数据加密。

**后量子算法采用：** NIST 已标准化用于密钥封装的 ML-KEM（FIPS 203）和用于数字签名的 ML-DSA（FIPS 204）。组织应开始在非生产环境中测试这些算法，并为关键系统制定迁移路线图。

**密码学敏捷性：** 系统必须被设计——或重构——使密码算法可在不需要完全应用重新设计的情况下被替换。这一原则同样适用于支付网关、消息中间件和面向客户的 API。

**混合方法：** 在过渡期间，将经典与后量子算法结合的混合密码方案提供纵深防御。这种方法保留向后兼容性同时引入量子抗性。

## EPAA 工作组与行业协作

亚太新兴支付协会（EPAA）成立了量子安全密码学工作组，通过协调的行业行动应对这些挑战。该工作组汇集了支付生态系统的参与者，包括 IBM、HSBC、KPMG、摩根大通和 PayPal 等。

通过在悉尼、香港和新加坡举行的工作坊，工作组开发了一个用于评估支付系统量子风险并识别实用迁移路径的共享框架。由此产生的白皮书 [Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa] 代表对挑战紧迫性和范围的共识立场。

工作组的分析得出结论：量子安全就绪是当前的基础设施决策，而非未来的。延迟的组织有可能发现自己无法满足监管期望、保护长寿命数据，或与已迁移的伙伴保持互操作性。

## 关于作者

Sebastien Rousseau 是 HSBC Bank plc 的高级数字产品经理，在 HSBC 商业与投资银行内领导企业支付 API 产品。他为 EPAA 量子安全密码学工作组做出贡献，并研究后量子密码学在金融服务中的应用。[阅读更多关于 Sebastien 的信息 ❯][00]

## 相关文章

- [[量子密钥分发](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)：变革银行业安全][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)：量子时代的守护算法][rel2]

[00]: /about/index.html "关于 Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "EPAA 抗量子支付白皮书"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "量子密钥分发：变革银行业安全"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber：量子时代的守护算法"
