---
title: "保障账簿：后量子迁移面向企业金融的董事会级指南"
subtitle: "G7 路线图与 BIS Project Leap 让后量子迁移从研究兴趣变为监管要求"
description: "G7 路线图与 BIS Project Leap 让后量子迁移从研究兴趣变为监管要求，董事会必须制定明确时间表。"
date: "May 14, 2026"
language: "zh-Hans"
locale: "zh_CN"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "后量子密码学迁移路线图——企业银行基础设施从 RSA 过渡到 ML-KEM 与 ML-DSA"
keywords: "后量子密码学, PQC, ML-KEM, ML-DSA, FIPS 203, FIPS 204, G7, BIS Project Leap, HNDL, Mosca 方程"
---

量子风险已从研究好奇心转变为活跃的监管要求。随着 2026 年 1 月发布的 G7 路线图、欧盟、英国和澳大利亚时间表的明确化，以及 BIS Project Leap 在实际支付系统中证明可行性，董事会的问题不再是是否迁移——而是迁移能否在当今数据的密码保质期到期之前完成。

---

> **核心要点**
>
> - **2026 年是监管姿态加强的一年。** G7 网络专家组 1 月的路线图、欧盟 NIS 合作组的协调时间表，以及英国 NCSC 的三阶段计划，已将对话从认识转向执行。澳大利亚信号局走得更远，为经典非对称密码学设定了 2030 年的硬截止日期。
> - **暴露是不对称的。** RSA、ECC 和 Diffie-Hellman 是直接问题——支撑 SWIFT 握手、TLS、PKI、代码签名和清算网络认证的非对称算法。对称加密（AES-256）如果保持密钥长度则仍然稳定。董事会层面的关注必须放在非对称表面。
> - **现在收集、未来解密不是未来场景。** 对手今天正在拦截并存储加密的金融日志、结算记录、并购材料和跨境电汇数据，明确意图是在密码相关量子计算机（CRQC）存在后解密。对于需要 10-20 年保密的数据，该风险已经实现。
> - **行业现在有工作参考点。** 2025 年 12 月发布的 [BIS Project Leap 第 2 阶段 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems") 成功用后量子密码学替换 TARGET2 实时流动性转账中的传统数字签名——并揭示了每个迁移项目都将面临的具体工程成本（验证延迟、包大小）。
> - **NIST 套件是全球锚点。** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final) 和 FIPS 204 (ML-DSA) 被每个主要司法管辖区引用，即使各国立场在参数集和混合要求上有所不同。董事会应将 ML-KEM-768/ML-DSA-65 视为底线，将 ML-KEM-1024/ML-DSA-87 视为长寿命数据的保守基线。
> - **混合是唯一可信路径。** 任何主要权威机构都不建议纯截转。并行运行经典和量子抗性算法是 NCSC、ANSSI、BSI 认可并在 Project Leap 中得到验证的部署模式。它比任一替代方案都更重，但它是唯一同时应对今天的兼容性和明天威胁的方法。

---

## 监管姿态加强的一年

在过去十年的大部分时间里，后量子密码学住在长期路线图的舒适角落。量子计算机令人印象深刻但遥远；支撑 RSA 和椭圆曲线的密码数学被视为稳定基质；迁移对话主要局限于专家工作组。这一立场已不再站得住脚。

2026 年 1 月，[G7 网络专家组发布了其迄今最重要的声明 ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20)，由美国财政部和英格兰银行共同主持。该文件不是监管，但比典型指南更具分量：它代表 G7 司法管辖区财政部、央行和监管机构共享的观点，即密码过渡现在是系统性风险管理议题。路线图将其规划视野对齐到 2030 年代中期，鼓励关键金融系统更早迁移——这种央行家谨慎措辞中信号着期望而非建议。

两个月前，BIS 创新中心和欧元体系发布了 [Project Leap 第 2 阶段 ⧉](https://www.bis.org/publ/othp107.htm) 结果，这是一项技术实验，将意大利银行、法兰西银行、德国联邦银行、Nexi-Colt 和 Swift 之间实时流动性转账中的传统数字签名替换为后量子密码学。头条结论是成功——量子抗性签名转账通过实时支付系统端到端通过。

这两个事件的组合——协调的 G7 政策框架和实际支付系统中可工作的证明点——产生了技术界等待十年的：对"这是真的吗？"问题的明确答案。2026 年 5 月，答案是肯定的。剩下的问题是步伐。

## 应让董事会关注的三个威胁向量

在讨论迁移机制之前，精确说明具体什么处于风险中是值得的。企业银行业中的量子风险在密码资产中不均匀，董事会的注意力最好指向暴露最严重的三个向量。

### 1. 现在收集、未来解密（HNDL）

最紧迫的关切不是未来。是现在。国家级和资深犯罪对手正在系统地拦截和存储加密金融流量——电汇、SWIFT 报文流、并购通信、跨境结算日志、互换协议和 KYC 文件——目前无法读取它们。他们的目标直接：现在存储，未来解密，一旦 CRQC 存在。正如 [国际清算银行明确指出的 ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm)，这种收集已经在发生。

对董事会，意义令人不安但具体：在 CRQC 到来后保密要求延伸的、今天在经典非对称加密下传输的任何敏感数据，必须已被视为暴露。HNDL 发生时没有数据泄露通知。SIEM 中没有警报。加密保持——目前——但数据已离开边界。

### 2. 长期敏感性风险

企业银行业数据具有异常长的机构保质期。战略并购文档可能在十年内保持市场敏感。商业秘密通信和知识产权估值可能保密 15 到 20 年。跨境结算日志、中央对手方暴露和对手方信用评估在其即时交易生命周期之外仍保留商业敏感性。

[Mosca 方程 ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic) 由 Michele Mosca 最初阐述，现已嵌入每个严肃迁移框架中，将问题形式化。如果 **S** 是数据的保质期，**M** 是迁移保护它的系统所需时间，**Q** 是 CRQC 可用前的时间，则：

```
若 S + M > Q，数据已暴露。
```

对于具有 20 年保密视野和现实需要 5 到 7 年完成迁移项目的数据，董事会暗中押注的 Q 值至少在 25 年外。日益增长的专家评估表明该押注不安全。

### 3. 核心握手的脆弱性

第三个向量在架构上最显著。对称密码（AES-256）仍相对稳定；Grover 算法将有效安全水平减半，但密钥长度加倍可恢复余量。灾难性暴露在于非对称算法——而这些正是支撑企业金融中每个认证握手的算法：SWIFT 公钥基础设施中的 RSA、TLS 客户端/服务器认证中的 ECDSA、会话密钥建立中的 ECDH，以及客户端移动认证、API 签名和代码签名管道中的 ECC 变体。

运行 Shor 算法的功能 CRQC 不会逐渐削弱这些系统。它打破它们。一旦 CRQC 运行，每个 RSA 保护的握手、每个 ECDSA 签名和每个椭圆曲线密钥交换都变得可恢复——不是经过数月的努力，而是在数小时内。从"安全"到"受损"的过渡是二元的，并跨使用受影响算法的每个系统同时传播。这是监管紧迫性所依赖的基础。

## 监管收紧：分司法管辖区视图

2026 年 5 月的全球监管图景不再是建议拼凑。它是一组协调的时间表，严格性各异但收敛到同一目的地。在主要金融中心运营的跨国银行现受到最严格适用的司法管辖区约束，而非最宽松的。

### 美国

美国对任何触及联邦系统的机构有最严格的立场。NSA 的 [商业国家安全算法套件 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026) 强制为国家安全系统采用 ML-KEM-1024 和 ML-DSA-87，要求新系统从 2027 年 1 月起部署 PQC，并到 2035 年完成基础设施迁移。OMB 备忘录 M-23-02 将联邦机构绑定到相同轨迹。

### 欧盟

欧盟在三层运作。[欧洲委员会的协调实施路线图 ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/) 由 NIS 合作组在 2025 年 6 月详述，设定阶段性里程碑：2026 年（国家战略）、2030 年（高风险系统已迁移）和 2035 年（完全过渡）。德国 BSI 强制混合密钥交换并批准 ML-KEM、FrodoKEM 和 Classic McEliece 的保守组合。法国 ANSSI 要求密钥封装和签名均混合。

### 英国

英国 NCSC 在 2025 年 3 月发布了其权威指南，并通过 2025 年度审查重申。三阶段时间表明确：

- **到 2028 年** —— 识别需要升级的密码服务、构建迁移计划并产生完整密码清单。
- **2028 至 2031 年** —— 执行高优先级升级，特别是关键系统和面向互联网的协议。
- **2031 至 2035 年** —— 跨所有系统、服务和产品完成迁移。

### 亚太地区

APAC 立场更碎片化但快速移动。澳大利亚 ASD 在全球持最严格立场：经典公钥密码学不得在 2030 年底之后使用，无混合建议，要求 ML-KEM-1024（ML-KEM-768 仅在 2030 年前可接受）。组织应在 2026 年底前有完善的过渡计划。新加坡金管局已发布正式量子安全就绪指南。

### 净立场

对董事会，这些司法管辖立场的实际综合是直接的。跨国银行不能管理到任何单一监管机构的时间表；它必须管理到最严格适用的。对大多数主要机构，这意味着高风险系统的规划视野到 2030 年底，长尾到 2035 年底。

## BIS Project Leap：行业实际证明了什么

Project Leap 值得董事会关注，不是因为它是营销里程碑，而是因为它是迄今后量子密码学在实际金融支付系统中最可信的端到端演示。头条结论直接：它工作。其下细节是运营意义所在。

第 1 阶段于 2023 年完成，在法兰西银行和德国联邦银行 IT 系统之间建立了量子抗性 VPN。第 2 阶段于 2025 年底完成，并在 [12 月报告 ⧉](https://www.bis.org/publ/othp107.htm)，走得更远。该联盟在 TARGET2（欧元体系实时全额结算系统）中流动性转账的执行中，用后量子签名替换了传统的基于 RSA 的数字签名。

报告标记了每个迁移项目应内化的三个发现：

- **验证延迟显著更高。** 后量子签名验证在同一硬件上比基于 RSA 的验证耗时显著更长。对于围绕亚秒级报文处理设计的 RTGS 系统，这不是边际观察；这是容量规划输入。
- **包大小需要系统重新开发。** PQC 签名比 ECDSA 等价物大一个数量级。其内部队列、监控工具和数据库模式针对遗留报文尺寸大小化的支付系统无法在不重新设计的情况下容纳新有效载荷。
- **混合是正确答案——但更重。** 并行运行经典和后量子算法保留向后兼容性并提供纵深防御，但它使密码处理开销翻倍。这是过渡期间正确做 PQC 的运营成本；不能仅靠巧妙工程避免。

## NIST 工具包：ML-KEM 与 ML-DSA 比较

每个可信国家框架的技术核心是 NIST 在 2024 年 8 月发布的后量子标准套件。其中两个标准是企业银行业的直接重点：用于密钥封装的 ML-KEM（FIPS 203）和用于数字签名的 ML-DSA（FIPS 204）。它们共享数学基础，但在密码资产中扮演非常不同的角色。

### ML-KEM (FIPS 203) — 密钥封装

源自 [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) 的 ML-KEM 是协议中 ECDH 和 RSA-KEM 的替代品。NIST 定义三种参数集：ML-KEM-512（NIST 类别 1）、ML-KEM-768（类别 3）和 ML-KEM-1024（类别 5）。

### ML-DSA (FIPS 204) — 数字签名

源自 CRYSTALS-Dilithium 的 ML-DSA 是 RSA 和 ECDSA 签名的替代品。三种参数集是 ML-DSA-44、ML-DSA-65 和 ML-DSA-87，大致对应 NIST 类别 2、3 和 5。

### 大小与性能配置

对范围迁移容量的 CIO，最重要的数字是工件大小。

| 算法 | 公钥 | 密文 / 签名 | 最接近经典等价物 | 大小对比经典 |
|---|---|---|---|---|
| ML-KEM-512 | 800 字节 | 768 字节（密文） | ECDH P-256（约 32 字节公钥） | 约 25× 更大 |
| ML-KEM-768 | 1,184 字节 | 1,088 字节（密文） | ECDH P-384 | 约 25× 更大 |
| ML-KEM-1024 | 1,568 字节 | 1,568 字节（密文） | ECDH P-521 | 约 25× 更大 |
| ML-DSA-44 | 1,312 字节 | 约 2,420 字节（签名） | ECDSA P-256（64 字节签名） | 约 38× 更大 |
| ML-DSA-65 | 1,952 字节 | 约 3,293 字节（签名） | ECDSA P-384 | 约 50× 更大 |
| ML-DSA-87 | 2,592 字节 | 约 4,595 字节（签名） | ECDSA P-521 | 约 70× 更大 |

*来源：[NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final) 和 FIPS 204 规范综合，附独立基准文献的比较数据。*

### 选择参数集

各司法管辖区在参数选择上的立场不完全相同，但收敛清晰。ML-KEM-768 和 ML-DSA-65 是企业底线——英国 NCSC 认可作为英国组织的基线，并在大多数欧洲框架下可接受。ML-KEM-1024 和 ML-DSA-87 是保守上限——NSA CNSA 2.0 为美国国家安全系统强制要求，ASD 要求澳大利亚受监管实体到 2030 年。

### 共享数学基础，共享风险

值得在董事会层面注意：ML-KEM 和 ML-DSA 都从同一族格问题获得安全性。未来对 Module-LWE 的密码分析突破将同时影响两个标准。这正是为什么几个国家权威——特别是德国 BSI 和法国 ANSSI——建议用基于哈希的签名（SLH-DSA，FIPS 205）补充基于格的栈。

## 逻辑迁移路径：发现 → 分类 → 混合部署

对批准多年 PQC 项目的董事会，运营问题是如何分阶段工作而不承担不可接受的服务可用性风险。在 G7 路线图、NCSC 框架、BIS Project Leap 和主要国家指南文档中出现的模式收敛于三个阶段。

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. 发现与 CBOM      │ → │  2. 分类（Mosca）    │ → │  3. 混合部署         │
│  跨所有系统的        │   │  按数据保质期        │   │  双重信封            │
│  密码清单            │   │  基于风险优先级      │   │  经典 + PQC，密码敏捷│
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### 阶段 1 —— 发现与密码物料清单（CBOM）

迁移无法为未被映射的密码资产规划。第一阶段因此是产生密码物料清单——组织中每个非对称密码实例的结构化清单，每个实例都标记算法、密钥长度、协议上下文、数据敏感性和系统所有者。

### 阶段 2 —— 使用 Mosca 方程的风险分类

有了 CBOM，机构可以逐资产应用 Mosca 框架。对每个密码依赖，问题是 **S + M > Q** 是否成立——数据的保质期加上迁移时间是否超过估计的 CRQC 时间。不等式最严重的资产去队列前面。

### 阶段 3 —— 混合部署

一旦优先资产被识别，部署应遵循 Project Leap 中证明并由 NCSC、ANSSI、BSI 和 G7 路线图认可的混合模式。混合部署并行运行经典算法和后量子算法，将其输出组合成单一信封。复合对经典攻击（经典算法今天有效）和量子攻击（PQC 算法明天有效）都安全。

## 这要花多少钱以及什么都不做花得更多

Mastercard 的分析在 [2026 年初报告 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy) 将全球金融部门 PQC 迁移成本估计为 280-420 亿美元。这是巨大数字。然而，它们不是相关比较。

相关比较是单一追溯解密事件的成本。对一个其收集的电汇流量、并购通信或对手方暴露数据在 2032 年变得对对手可读的机构，运营和声誉成本不受迁移资本支出线限制。它由相关十年战略信息的价值限制——对任何系统重要机构，这实质上大于任何合理的迁移预算。

## 结论

将后量子迁移视为 2026 年董事会级优先事项的理由不是建立在 CRQC 临近性上。它建立在另外三个不确定的观察上。

首先，现在收集、未来解密今天正在发生，具有十年以上保密要求的数据无论 CRQC 何时到达都已暴露。其次，主要金融机构密码资产的迁移即使有足够资金和领导聚焦也需要 5-7 年——意味着 2026 年开始的项目在 2031 年左右完成，这在 CRQC 概率分布的保守端内。第三，监管期望在过去 12 个月内实质性加强，2026 年董事会会议记录中记录明确 PQC 项目的机构将处于实质上更强的位置。

现在开始的机构有选择优势。等待的机构将面对相同的工作但时间更紧。早行动的成本是已知的；晚行动的成本以风险管理设计的方式不对称。

## 常见问题

**密码相关量子计算机实际何时存在？**

可信估计差别很大。截至 2026 年初，公开量子演示已达到约 24 到 28 个逻辑量子比特，而 CRQC 估计需要约 6,000 个逻辑量子比特，由 10 万到数百万个物理量子比特支撑。专家共识将 CRQC 概率到 2028 年定为一个百分点以下，到 2037-2040 年约 50%。

**为何混合部署而非纯后量子？**

三个原因。首先，ML-KEM 和 ML-DSA 虽然经过充分审查，但密码分析历史比 RSA 和 ECC 短。混合方案在任一组件成立时仍安全；纯 PQC 方案在格问题意外被削弱时暴露。其次，混合保留与尚未迁移的对手方的向后兼容性——在多年行业过渡中至关重要。第三，澳大利亚信号局外的每个主要权威都明确推荐混合用于过渡期：NCSC、ANSSI、BSI、NLNCSA 和 G7 框架。

**我们需要 ML-KEM 和 ML-DSA 两者，还是可以选一个？**

两者。ML-KEM 和 ML-DSA 服务不同的密码角色。ML-KEM 替换 TLS、VPN、移动认证等协议中的密钥建立原语。ML-DSA 替换 PKI 证书、代码签名、文档签名、SWIFT 风格认证消息和身份断言中的数字签名原语。

**我们如何衡量这么大项目的进展？**

三个指标实用且与主要监管框架对齐。**CBOM 覆盖率**——机构非对称密码实例已被清点、分类和标记的百分比。**高风险资产的迁移覆盖率**——Mosca S + M > Q 条件成立的资产中已移到混合 PQC 的百分比。**密码敏捷性覆盖率**——可在不改代码、仅配置的情况下交换算法的密码依赖系统的百分比。

**再等一年的成本是什么？**

不是零，也不对称。等待一年放弃对长寿命数据一年的 HNDL 保护——保密要求延伸到 2040 年的数据比必要长暴露一年。它针对固定监管截止日期（ASD 2030、NSA CNSA 2.0 里程碑、欧盟 2030 关键系统目标）压缩迁移窗口，这转化为更高的交付风险和更少的排序灵活性。

## 参考资料

- Sebastien Rousseau, (2026). [量子阈值再次移动](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html)。
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber：量子时代的守护算法](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)。
- Sebastien Rousseau, (2023). [量子密钥分发：变革银行业安全](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)。
- Sebastien Rousseau, (2023). [KyberLib：抵御量子威胁的 Rust 盾牌](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html)。
- G7 网络专家组, (2026). [推进金融部门后量子密码学过渡的协调路线图 ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20)。GOV.UK.
- 国际清算银行, (2025). [Project Leap 第 2 阶段：支付系统的量子防护 ⧉](https://www.bis.org/publ/othp107.htm)。BIS.
- NIST, (2024). [FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final)。NIST.
- UK NCSC, (2025). [向后量子密码学迁移的时间表 ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines)。UK NCSC.
- CMORG, (2025). [后量子密码学指南 ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf)。CMORG.
- PQCC, (2025). [国际 PQC 要求 ⧉](https://pqcc.org/international-pqc-requirements/)。PQCC.
- PQShield, (2025). [PQC 路线图与过渡指南 ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/)。PQShield.
- Forrester, (2025). [2026 年亚太预测 ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/)。Forrester.
