---
title: "KyberLib：抵御量子威胁的 Rust 盾牌"
subtitle: "稳健的量子安全 CRYSTALS-Kyber 算法实现，保护你的数据免受量子威胁与密码分析攻击"
description: "KyberLib 是基于 CRYSTALS-Kyber 的 Rust 抗量子密码库，适用于 no-std 与 WebAssembly 环境。"
date: "November 28, 2023"
language: "zh-Hans"
locale: "zh_CN"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "KyberLib：在量子时代赋能安全通信"
keywords: "KyberLib, Rust, CRYSTALS-Kyber, 后量子密码学, 量子安全, 格密码学, no-std, WebAssembly, NIST, 嵌入式系统"
---

[![KyberLib：在量子时代赋能安全通信](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` 是一个基于 Rust 的库，保护你的数据免受量子计算潜在威胁。`KyberLib` 构建在 **[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) 算法** 之上，提供卓越的安全性、效率与多功能性，可轻松集成到包括 `no-std` 环境在内的多种平台。

![分隔线][divider].class=\"m-10 w-100\"

## 在量子时代守护你的数据

量子计算的到来对传统密码安全措施构成重大威胁。为应对这一挑战，量子安全密码学（QSC）领域正在快速演进。

引领这场变革运动的是美国国家标准与技术研究院（NIST），它正主导 QSC 算法的标准化。

2023 年，NIST 入围了四种创新算法：

- [**[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** ⧉][01]（密钥封装机制）
- [**CRYSTALS-Dilithium** ⧉][02]（数字签名）
- [**FALCON** ⧉][03]（轻量级数字签名）
- [**SPHINCS+** ⧉][04]（基于哈希的数字签名）

这些开创性算法基于多种数学原理，包括基于格的密码学、基于哈希的密码学和基于编码的密码学，旨在为抵御量子攻击提供稳健防御。

## 探索基于格的密码学

基于格的密码学（LBC）正在 QSC 中崭露头角，提供一种有前景的后量子密码（PQC）方案。LBC 用途广泛，应用范围涵盖密钥封装机制（KEM）、数字签名和基于数学格的公钥加密方案。

格是数学中的基本概念，在密码学等多个领域都有应用。简单地说，格是空间中点的规则排列，形成网格状结构。这些点通过线连接，构成相互连接的单元网络。点的具体排列方式与点间距定义了格的独特特性。

### 带基向量的 3D 格表示

下图展示由三个基向量生成的 3D 格结构：

- `b1 = [1, 0, 0]`（红色）
- `b2 = [0, 1, 0]`（绿色）
- `b3 = [0, 0, 1]`（蓝色）

格上的每个点是通过将这些基向量按不同整数比例组合形成的，生成在所有三个空间维度上延伸的网格状图案。该可视化展现了 3D 格的本质，这是物理与数学中广泛用于表示空间点规则重复排列的概念。

![带基向量的 3D 格表示][06].class=\"img-fluid mx-auto d-block\"

在密码学中，格被用作某些密码算法的基础。基于格的密码学（LBC）利用格的数学特性创建抗量子计算机攻击的安全密码方案。量子计算机对传统密码学构成重大威胁，因为它们可以高效地破解依赖大数分解或离散对数求解的算法。

CRYSTALS-Kyber 体现了 LBC 的优势，提供对抗量子攻击的稳健抗性，并具备卓越的效率与密钥大小。它在多平台运行并与密码学兼容，是量子时代可靠的数据安全选项。

CRYSTALS-Kyber 当前规格如下：

- **Kyber512**：提供等同于 128 位 AES 加密的安全级别，以行业标准防护守护敏感数据。
- **Kyber768**：提供等同于 256 位 AES 加密的安全级别，确保高度敏感信息的机密性。
- **Kyber1024**：提供超过 256 位 AES 加密的安全级别，提供针对量子攻击的稳健防护，长远守护数据完整性。

### 经典算法与抗量子算法安全级别对比

下图柱状图说明 RSA-2048 和椭圆曲线数字签名算法（ECDSA）等经典密码算法相对于抗量子 CRYSTALS-Kyber 各规格（Kyber512、Kyber768、Kyber1024）的相对安全级别。

虽然图表提供视觉对比，但需要注意：由于基于不同数学原理，这些安全级别并不直接可比。

不过，该图为理解抗量子算法的安全级别提供了有用参考。

![基于格的密码学][05].class=\"img-fluid mx-auto d-block\"

![分隔线][divider].class=\"m-10 w-100\"

## KyberLib：用于抗量子密码学的 Rust 库

KyberLib 借助 CRYSTALS-Kyber 的力量，提供更强的内存安全与稳健的系统级安全。它支持多种 CRYSTALS-Kyber 规格（Kyber512、Kyber768、Kyber1024），提供多种安全级别以契合具体需求。其 `no_std` 兼容性使其成为嵌入式系统的理想选择，而 WebAssembly（WASM）兼容性也让它能无缝集成到 Web 应用中。

![分隔线][divider].class=\"m-10 w-100\"

## 用抗量子密码学保护 Web 应用

KyberLib 设计了最小的内存占用，非常适合嵌入式与资源受限系统，且不牺牲安全。其基于 Rust 的实现充分利用了语言的安全特性，强化了 CRYSTALS-Kyber 算法提供的安全性。

此外，KyberLib 的 WebAssembly 兼容性增强了其在 Web 应用中的实用性，确保它在密码学不断变化的领域仍是关键工具。

[立即开始使用 KyberLib！⧉][00] 安装轻松、个人与商业用途皆免费，KyberLib 是你抗量子密码学的首选方案。

[00]: https://kyberlib.com/getting-started/index.html "开始使用"
[01]: https://pq-crystals.org/kyber/ "Kyber：基于模格的 CCA 安全 KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium：基于格的 CCA 安全签名方案"
[03]: https://falcon-sign.info/ "FALCON：后量子签名方案"
[04]: https://sphincs.org/ "SPHINCS+：无状态的基于哈希签名方案"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "经典算法与抗量子算法安全级别对比"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "带基向量的 3D 格表示"
[07]: https://kyberlib.com/ "量子世界中的隐私与安全"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "分隔线"
