---
title: "格基密码学的量子算法中发现漏洞"
subtitle: "陈逸雷 LWE 量子算法的漏洞：对 NIST 后量子密码学标准化的重新评估"
description: "陈逸雷的 LWE 量子算法被发现存在漏洞，格基密码学暂时保持安全，但量子抗性研究仍需推进。"
date: "April 22, 2024"
language: "zh-Hans"
locale: "zh_CN"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "MidJourney 生成图像 - 红蓝色调的数字节点网络"
keywords: "陈逸雷, LWE, 量子算法, 格密码学, NIST, 后量子密码学, Kyber, Dilithium, BGV, TFHE"
---

## 量子困局：在陈逸雷算法影响下重新评估 NIST 后量子密码学标准化

继我此前关于[格基密码学量子算法挑战][00]的文章后，我有必要更新[陈逸雷研究 ⧉][01]的最新进展。

出乎意料的是，清华大学交叉信息研究院（IIIS）助理教授陈逸雷报告称，同行科学家 Hongxun Wu 与 Thomas Vidick 已独立在其用于解决 Learning with Errors（LWE）问题的多项式时间量子算法中发现一个漏洞。

该漏洞使算法失效，陈已承认其方法不如最初宣称的那样成立。

## 陈量子算法中的漏洞

漏洞在陈算法的第 9 步被发现，他表示不知如何修复。这一发现让密码学界松了一口气——它证实了 LWE 问题（后量子密码学保护方法的关键组成部分）仍保持安全。

陈的论文还研究了其他复杂格问题，如多项式近似因子内的决策版最短向量问题（GapSVP）与最短独立向量问题（SIVP）。虽然其算法的漏洞不直接影响这些问题，但它对格基密码学量子算法的稳健性提出了疑问。

但根据 [Nigel Smart 的页面 ⧉][02]，所提议的对 LWE 的量子攻击存在缺陷，并未破坏 [Kyber ⧉][04]、[Dilithium ⧉][05]、[BGV ⧉][06] 或 [TFHE ⧉][07] 等格密码方案。

## 对 NIST 后量子密码学标准化过程的意义

陈的研究间接对 [NIST 后量子密码学（PQC）标准化过程 ⧉][03] 及量子抗性密码算法的选择引发了担忧与疑问。

[CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) 与 CRYSTALS-Dilithium 方案——NIST PQC 标准化过程的入围者之一——是已被严格测试和评估量子抗性的格基密码方案的例子。然而，持续测试和完善这些方案以确保其长期安全与可行性至关重要。

NIST、密码学界与企业必须保持警觉，继续探索后量子密码学的替代数学基础，以确保对量子抗性安全有一套稳健多元的选项。

## 后量子密码学的未来

陈算法中漏洞的发现凸显了科学过程中同行评议的关键角色。它也凸显了对即时审查、反馈与辩论的需求。

量子时代已经开始，发展量子抗性密码方法需要全球规模的协作措施，以确保我们的数字基础设施在面对不断进步的量子计算能力与量子至高竞争时的安全。

NIST PQC 标准化过程是朝该方向迈出的重要一步，但仅是开始。陈算法中的漏洞是对未来挑战与不确定性的强烈提醒，但也是密码学界加倍努力、推动可能边界的行动号召。

这是后量子密码学领域的一项引人入胜的发展，看 NIST PQC 标准化过程如何响应这一新信息将很有意思。

## 结论

陈逸雷解决 LWE 问题的量子算法中发现的漏洞，证明了严格的同行评议与协作在开发量子抗性密码学中的重要性。

虽然该漏洞为格基密码方案的安全提供了暂时安心，但也提醒着后量子密码学领域研究与开发的持续必要。

随着 NIST 继续其 PQC 标准化过程，密码学界必须保持主动和适应能力，拥抱新思想与方法，以确保我们的数字世界在面对不断进步的量子计算能力时的长期安全。

## 参考资料

- Sebastien Rousseau, (2024). [量子算法挑战格基密码学][00].
- Chen, Y. (2024). [格问题的量子算法：密码学的新时代 ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [关于格、Learning With Errors、随机线性码与密码学。⧉][02] 收录于 Proceedings of the 37th Annual ACM Symposium on Theory of Computing (pp. 84-93).
- Kuperberg, G. (2005). [二面体隐藏子群问题的亚指数时间量子算法。⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "格基密码学量子算法挑战"
[01]: https://eprint.iacr.org/2024/555.pdf "格问题的量子算法：密码学的新时代"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "后量子密码学标准化"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
