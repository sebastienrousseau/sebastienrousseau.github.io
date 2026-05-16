---
title: "KyberLib：抵禦量子威脅的 Rust 盾牌"
subtitle: "穩健的量子安全 CRYSTALS-Kyber 演算法實現，保護你的資料免受量子威脅與密碼分析攻擊"
description: "KyberLib 是基於 CRYSTALS-Kyber 的 Rust 抗量子密碼庫，適用於 no-std 與 WebAssembly 環境。"
date: "November 28, 2023"
language: "zh-Hant"
locale: "zh_TW"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/github/github-kyberlib.svg"
banner_alt: "KyberLib：在量子時代賦能安全通訊"
keywords: "KyberLib, Rust, CRYSTALS-Kyber, 後量子密碼學, 量子安全, 格密碼學, no-std, WebAssembly, NIST, 嵌入式系統"
---

[![KyberLib：在量子時代賦能安全通訊](https://cloudcdn.pro/clients/kyberlib/v1/github/github-kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` 是一個基於 Rust 的庫，保護你的資料免受量子計算潛在威脅。`KyberLib` 構建在 **[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) 演算法** 之上，提供卓越的安全性、效率與多功能性，可輕鬆整合到包括 `no-std` 環境在內的多種平臺。

![分隔線][divider].class=\"m-10 w-100\"

## 在量子時代守護你的資料

量子計算的到來對傳統密碼安全措施構成重大威脅。為應對這一挑戰，量子安全密碼學（QSC）領域正在快速演進。

引領這場變革運動的是美國國家標準與技術研究院（NIST），它正主導 QSC 演算法的標準化。

2023 年，NIST 入圍了四種創新演算法：

- [**[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** ⧉][01]（金鑰封裝機制）
- [**CRYSTALS-Dilithium** ⧉][02]（數字簽名）
- [**FALCON** ⧉][03]（輕量級數字簽名）
- [**SPHINCS+** ⧉][04]（基於雜湊的數字簽名）

這些開創性演算法基於多種數學原理，包括基於格的密碼學、基於雜湊的密碼學和基於編碼的密碼學，旨在為抵禦量子攻擊提供穩健防禦。

## 探索基於格的密碼學

基於格的密碼學（LBC）正在 QSC 中嶄露頭角，提供一種有前景的後量子密碼（PQC）方案。LBC 用途廣泛，應用範圍涵蓋金鑰封裝機制（KEM）、數字簽名和基於數學格的公鑰加密方案。

格是數學中的基本概念，在密碼學等多個領域都有應用。簡單地說，格是空間中點的規則排列，形成網格狀結構。這些點透過線連線，構成相互連線的單元網路。點的具體排列方式與點間距定義了格的獨特特性。

### 帶基向量的 3D 格表示

下圖展示由三個基向量生成的 3D 格結構：

- `b1 = [1, 0, 0]`（紅色）
- `b2 = [0, 1, 0]`（綠色）
- `b3 = [0, 0, 1]`（藍色）

格上的每個點是透過將這些基向量按不同整數比例組合形成的，生成在所有三個空間維度上延伸的網格狀圖案。該視覺化展現了 3D 格的本質，這是物理與數學中廣泛用於表示空間點規則重複排列的概念。

![帶基向量的 3D 格表示][06].class=\"img-fluid mx-auto d-block\"

在密碼學中，格被用作某些密碼演算法的基礎。基於格的密碼學（LBC）利用格的數學特性建立抗量子計算機攻擊的安全密碼方案。量子計算機對傳統密碼學構成重大威脅，因為它們可以高效地破解依賴大數分解或離散對數求解的演算法。

CRYSTALS-Kyber 體現了 LBC 的優勢，提供對抗量子攻擊的穩健抗性，並具備卓越的效率與金鑰大小。它在多平臺執行並與密碼學相容，是量子時代可靠的資料安全選項。

CRYSTALS-Kyber 當前規格如下：

- **Kyber512**：提供等同於 128 位 AES 加密的安全級別，以行業標準防護守護敏感資料。
- **Kyber768**：提供等同於 256 位 AES 加密的安全級別，確保高度敏感資訊的機密性。
- **Kyber1024**：提供超過 256 位 AES 加密的安全級別，提供針對量子攻擊的穩健防護，長遠守護資料完整性。

### 經典演算法與抗量子演算法安全級別對比

下圖柱狀圖說明 RSA-2048 和橢圓曲線數字簽名演算法（ECDSA）等經典密碼演算法相對於抗量子 CRYSTALS-Kyber 各規格（Kyber512、Kyber768、Kyber1024）的相對安全級別。

雖然圖表提供視覺對比，但需要注意：由於基於不同數學原理，這些安全級別並不直接可比。

不過，該圖為理解抗量子演算法的安全級別提供了有用參考。

![基於格的密碼學][05].class=\"img-fluid mx-auto d-block\"

![分隔線][divider].class=\"m-10 w-100\"

## KyberLib：用於抗量子密碼學的 Rust 庫

KyberLib 藉助 CRYSTALS-Kyber 的力量，提供更強的記憶體安全與穩健的系統級安全。它支援多種 CRYSTALS-Kyber 規格（Kyber512、Kyber768、Kyber1024），提供多種安全級別以契合具體需求。其 `no_std` 相容性使其成為嵌入式系統的理想選擇，而 WebAssembly（WASM）相容性也讓它能無縫整合到 Web 應用中。

![分隔線][divider].class=\"m-10 w-100\"

## 用抗量子密碼學保護 Web 應用

KyberLib 設計了最小的記憶體佔用，非常適合嵌入式與資源受限系統，且不犧牲安全。其基於 Rust 的實現充分利用了語言的安全特性，強化了 CRYSTALS-Kyber 演算法提供的安全性。

此外，KyberLib 的 WebAssembly 相容性增強了其在 Web 應用中的實用性，確保它在密碼學不斷變化的領域仍是關鍵工具。

[立即開始使用 KyberLib！⧉][00] 安裝輕鬆、個人與商業用途皆免費，KyberLib 是你抗量子密碼學的首選方案。

[00]: https://kyberlib.com/getting-started/index.html "開始使用"
[01]: https://pq-crystals.org/kyber/ "Kyber：基於模格的 CCA 安全 KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium：基於格的 CCA 安全簽名方案"
[03]: https://falcon-sign.info/ "FALCON：後量子簽名方案"
[04]: https://sphincs.org/ "SPHINCS+：無狀態的基於雜湊簽名方案"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "經典演算法與抗量子演算法安全級別對比"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "帶基向量的 3D 格表示"
[07]: https://kyberlib.com/ "量子世界中的隱私與安全"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "分隔線"
