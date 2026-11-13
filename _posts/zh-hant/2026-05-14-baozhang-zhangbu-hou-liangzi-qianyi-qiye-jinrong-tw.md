---
title: "保障賬簿：後量子遷移面向企業金融的董事會級指南"
subtitle: "G7 路線圖與 BIS Project Leap 讓後量子遷移從研究興趣變為監管要求"
description: "G7 路線圖與 BIS Project Leap 讓後量子遷移從研究興趣變為監管要求，董事會必須制定明確時間表。"
date: "May 14, 2026"
language: "zh-Hant"
locale: "zh_TW"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "後量子密碼學遷移路線圖——企業銀行基礎設施從 RSA 過渡到 ML-KEM 與 ML-DSA"
keywords: "後量子密碼學, PQC, ML-KEM, ML-DSA, FIPS 203, FIPS 204, G7, BIS Project Leap, HNDL, Mosca 方程"
---

量子風險已從研究好奇心轉變為活躍的監管要求。隨著 2026 年 1 月釋出的 G7 路線圖、歐盟、英國和澳大利亞時間表的明確化，以及 BIS Project Leap 在實際支付系統中證明可行性，董事會的問題不再是是否遷移——而是遷移能否在當今資料的密碼保質期到期之前完成。

---

> **核心要點**
>
> - **2026 年是監管姿態加強的一年。** G7 網路專家組 1 月的路線圖、歐盟 NIS 合作組的協調時間表，以及英國 NCSC 的三階段計劃，已將對話從認識轉向執行。澳大利亞訊號局走得更遠，為經典非對稱密碼學設定了 2030 年的硬截止日期。
> - **暴露是不對稱的。** RSA、ECC 和 Diffie-Hellman 是直接問題——支撐 SWIFT 握手、TLS、PKI、程式碼簽名和清算網路認證的非對稱演算法。對稱加密（AES-256）如果保持金鑰長度則仍然穩定。董事會層面的關注必須放在非對稱表面。
> - **現在收集、未來解密不是未來場景。** 對手今天正在攔截並儲存加密的金融日誌、結算記錄、併購材料和跨境電匯資料，明確意圖是在密碼相關量子計算機（CRQC）存在後解密。對於需要 10-20 年保密的資料，該風險已經實現。
> - **行業現在有工作參考點。** 2025 年 12 月釋出的 [BIS Project Leap 第 2 階段 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems") 成功用後量子密碼學替換 TARGET2 實時流動性轉賬中的傳統數字簽名——並揭示了每個遷移專案都將面臨的具體工程成本（驗證延遲、包大小）。
> - **NIST 套件是全球錨點。** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final) 和 FIPS 204 (ML-DSA) 被每個主要司法管轄區引用，即使各國立場在引數集和混合要求上有所不同。董事會應將 ML-KEM-768/ML-DSA-65 視為底線，將 ML-KEM-1024/ML-DSA-87 視為長壽命資料的保守基線。
> - **混合是唯一可信路徑。** 任何主要權威機構都不建議純截轉。並行執行經典和量子抗性演算法是 NCSC、ANSSI、BSI 認可並在 Project Leap 中得到驗證的部署模式。它比任一替代方案都更重，但它是唯一同時應對今天的相容性和明天威脅的方法。

---

## 監管姿態加強的一年

在過去十年的大部分時間裡，後量子密碼學住在長期路線圖的舒適角落。量子計算機令人印象深刻但遙遠；支撐 RSA 和橢圓曲線的密碼數學被視為穩定基質；遷移對話主要侷限於專家工作組。這一立場已不再站得住腳。

2026 年 1 月，[G7 網路專家組釋出了其迄今最重要的宣告 ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20)，由美國財政部和英格蘭銀行共同主持。該檔案不是監管，但比典型指南更具分量：它代表 G7 司法管轄區財政部、央行和監管機構共享的觀點，即密碼過渡現在是系統性風險管理議題。路線圖將其規劃視野對齊到 2030 年代中期，鼓勵關鍵金融系統更早遷移——這種央行家謹慎措辭中訊號著期望而非建議。

兩個月前，BIS 創新中心和歐元體系釋出了 [Project Leap 第 2 階段 ⧉](https://www.bis.org/publ/othp107.htm) 結果，這是一項技術實驗，將義大利銀行、法蘭西銀行、德國聯邦銀行、Nexi-Colt 和 Swift 之間實時流動性轉賬中的傳統數字簽名替換為後量子密碼學。頭條結論是成功——量子抗性簽名轉賬透過實時支付系統端到端透過。

這兩個事件的組合——協調的 G7 政策框架和實際支付系統中可工作的證明點——產生了技術界等待十年的：對"這是真的嗎？"問題的明確答案。2026 年 5 月，答案是肯定的。剩下的問題是步伐。

## 應讓董事會關注的三個威脅向量

在討論遷移機制之前，精確說明具體什麼處於風險中是值得的。企業銀行業中的量子風險在密碼資產中不均勻，董事會的注意力最好指向暴露最嚴重的三個向量。

### 1. 現在收集、未來解密（HNDL）

最緊迫的關切不是未來。是現在。國家級和資深犯罪對手正在系統地攔截和儲存加密金融流量——電匯、SWIFT 報文流、併購通訊、跨境結算日誌、互換協議和 KYC 檔案——目前無法讀取它們。他們的目標直接：現在儲存，未來解密，一旦 CRQC 存在。正如 [國際清算銀行明確指出的 ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm)，這種收集已經在發生。

對董事會，意義令人不安但具體：在 CRQC 到來後保密要求延伸的、今天在經典非對稱加密下傳輸的任何敏感資料，必須已被視為暴露。HNDL 發生時沒有資料洩露通知。SIEM 中沒有警報。加密保持——目前——但資料已離開邊界。

### 2. 長期敏感性風險

企業銀行業資料具有異常長的機構保質期。戰略併購文件可能在十年內保持市場敏感。商業秘密通訊和智慧財產權估值可能保密 15 到 20 年。跨境結算日誌、中央對手方暴露和對手方信用評估在其即時交易生命週期之外仍保留商業敏感性。

[Mosca 方程 ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic) 由 Michele Mosca 最初闡述，現已嵌入每個嚴肅遷移框架中，將問題形式化。如果 **S** 是資料的保質期，**M** 是遷移保護它的系統所需時間，**Q** 是 CRQC 可用前的時間，則：

```
若 S + M > Q，資料已暴露。
```

對於具有 20 年保密視野和現實需要 5 到 7 年完成遷移專案的資料，董事會暗中押注的 Q 值至少在 25 年外。日益增長的專家評估表明該押注不安全。

### 3. 核心握手的脆弱性

第三個向量在架構上最顯著。對稱密碼（AES-256）仍相對穩定；Grover 演算法將有效安全水平減半，但金鑰長度加倍可恢復餘量。災難性暴露在於非對稱演算法——而這些正是支撐企業金融中每個認證握手的演算法：SWIFT 公鑰基礎設施中的 RSA、TLS 客戶端/伺服器認證中的 ECDSA、會話金鑰建立中的 ECDH，以及客戶端移動認證、API 簽名和程式碼簽名管道中的 ECC 變體。

執行 Shor 演算法的功能 CRQC 不會逐漸削弱這些系統。它打破它們。一旦 CRQC 執行，每個 RSA 保護的握手、每個 ECDSA 簽名和每個橢圓曲線金鑰交換都變得可恢復——不是經過數月的努力，而是在數小時內。從"安全"到"受損"的過渡是二元的，並跨使用受影響演算法的每個系統同時傳播。這是監管緊迫性所依賴的基礎。

## 監管收緊：分司法管轄區檢視

2026 年 5 月的全球監管圖景不再是建議拼湊。它是一組協調的時間表，嚴格性各異但收斂到同一目的地。在主要金融中心運營的跨國銀行現受到最嚴格適用的司法管轄區約束，而非最寬鬆的。

### 美國

美國對任何觸及聯邦系統的機構有最嚴格的立場。NSA 的 [商業國家安全演算法套件 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026) 強制為國家安全系統採用 ML-KEM-1024 和 ML-DSA-87，要求新系統從 2027 年 1 月起部署 PQC，併到 2035 年完成基礎設施遷移。OMB 備忘錄 M-23-02 將聯邦機構繫結到相同軌跡。

### 歐盟

歐盟在三層運作。[歐洲委員會的協調實施路線圖 ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/) 由 NIS 合作組在 2025 年 6 月詳述，設定階段性里程碑：2026 年（國家戰略）、2030 年（高風險系統已遷移）和 2035 年（完全過渡）。德國 BSI 強制混合金鑰交換並批准 ML-KEM、FrodoKEM 和 Classic McEliece 的保守組合。法國 ANSSI 要求金鑰封裝和簽名均混合。

### 英國

英國 NCSC 在 2025 年 3 月釋出了其權威指南，並透過 2025 年度審查重申。三階段時間表明確：

- **到 2028 年** —— 識別需要升級的密碼服務、構建遷移計劃併產生完整密碼清單。
- **2028 至 2031 年** —— 執行高優先順序升級，特別是關鍵系統和麵向網際網路的協議。
- **2031 至 2035 年** —— 跨所有系統、服務和產品完成遷移。

### 亞太地區

APAC 立場更碎片化但快速移動。澳大利亞 ASD 在全球持最嚴格立場：經典公鑰密碼學不得在 2030 年底之後使用，無混合建議，要求 ML-KEM-1024（ML-KEM-768 僅在 2030 年前可接受）。組織應在 2026 年底前有完善的過渡計劃。新加坡金管局已釋出正式量子安全就緒指南。

### 淨立場

對董事會，這些司法管轄立場的實際綜合是直接的。跨國銀行不能管理到任何單一監管機構的時間表；它必須管理到最嚴格適用的。對大多數主要機構，這意味著高風險系統的規劃視野到 2030 年底，長尾到 2035 年底。

## BIS Project Leap：行業實際證明了什麼

Project Leap 值得董事會關注，不是因為它是營銷里程碑，而是因為它是迄今後量子密碼學在實際金融支付系統中最可信的端到端演示。頭條結論直接：它工作。其下細節是運營意義所在。

第 1 階段於 2023 年完成，在法蘭西銀行和德國聯邦銀行 IT 系統之間建立了量子抗性 VPN。第 2 階段於 2025 年底完成，並在 [12 月報告 ⧉](https://www.bis.org/publ/othp107.htm)，走得更遠。該聯盟在 TARGET2（歐元體系實時全額結算系統）中流動性轉賬的執行中，用後量子簽名替換了傳統的基於 RSA 的數字簽名。

報告標記了每個遷移專案應內化的三個發現：

- **驗證延遲顯著更高。** 後量子簽名驗證在同一硬體上比基於 RSA 的驗證耗時顯著更長。對於圍繞亞秒級報文處理設計的 RTGS 系統，這不是邊際觀察；這是容量規劃輸入。
- **包大小需要系統重新開發。** PQC 簽名比 ECDSA 等價物大一個數量級。其內部佇列、監控工具和資料庫模式針對遺留報文尺寸大小化的支付系統無法在不重新設計的情況下容納新有效載荷。
- **混合是正確答案——但更重。** 並行執行經典和後量子演算法保留向後相容性並提供縱深防禦，但它使密碼處理開銷翻倍。這是過渡期間正確做 PQC 的運營成本；不能僅靠巧妙工程避免。

## NIST 工具包：ML-KEM 與 ML-DSA 比較

每個可信國家框架的技術核心是 NIST 在 2024 年 8 月釋出的後量子標準套件。其中兩個標準是企業銀行業的直接重點：用於金鑰封裝的 ML-KEM（FIPS 203）和用於數字簽名的 ML-DSA（FIPS 204）。它們共享數學基礎，但在密碼資產中扮演非常不同的角色。

### ML-KEM (FIPS 203) — 金鑰封裝

源自 [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) 的 ML-KEM 是協議中 ECDH 和 RSA-KEM 的替代品。NIST 定義三種引數集：ML-KEM-512（NIST 類別 1）、ML-KEM-768（類別 3）和 ML-KEM-1024（類別 5）。

### ML-DSA (FIPS 204) — 數字簽名

源自 CRYSTALS-Dilithium 的 ML-DSA 是 RSA 和 ECDSA 簽名的替代品。三種引數集是 ML-DSA-44、ML-DSA-65 和 ML-DSA-87，大致對應 NIST 類別 2、3 和 5。

### 大小與效能配置

對範圍遷移容量的 CIO，最重要的數字是工件大小。

| 演算法 | 公鑰 | 密文 / 簽名 | 最接近經典等價物 | 大小對比經典 |
|---|---|---|---|---|
| ML-KEM-512 | 800 位元組 | 768 位元組（密文） | ECDH P-256（約 32 位元組公鑰） | 約 25× 更大 |
| ML-KEM-768 | 1,184 位元組 | 1,088 位元組（密文） | ECDH P-384 | 約 25× 更大 |
| ML-KEM-1024 | 1,568 位元組 | 1,568 位元組（密文） | ECDH P-521 | 約 25× 更大 |
| ML-DSA-44 | 1,312 位元組 | 約 2,420 位元組（簽名） | ECDSA P-256（64 位元組簽名） | 約 38× 更大 |
| ML-DSA-65 | 1,952 位元組 | 約 3,293 位元組（簽名） | ECDSA P-384 | 約 50× 更大 |
| ML-DSA-87 | 2,592 位元組 | 約 4,595 位元組（簽名） | ECDSA P-521 | 約 70× 更大 |

*來源：[NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final) 和 FIPS 204 規範綜合，附獨立基準文獻的比較資料。*

### 選擇引數集

各司法管轄區在引數選擇上的立場不完全相同，但收斂清晰。ML-KEM-768 和 ML-DSA-65 是企業底線——英國 NCSC 認可作為英國組織的基線，並在大多數歐洲框架下可接受。ML-KEM-1024 和 ML-DSA-87 是保守上限——NSA CNSA 2.0 為美國國家安全系統強制要求，ASD 要求澳大利亞受監管實體到 2030 年。

### 共享數學基礎，共享風險

值得在董事會層面注意：ML-KEM 和 ML-DSA 都從同一族格問題獲得安全性。未來對 Module-LWE 的密碼分析突破將同時影響兩個標準。這正是為什麼幾個國家權威——特別是德國 BSI 和法國 ANSSI——建議用基於雜湊的簽名（SLH-DSA，FIPS 205）補充基於格的棧。

## 邏輯遷移路徑：發現 → 分類 → 混合部署

對批准多年 PQC 專案的董事會，運營問題是如何分階段工作而不承擔不可接受的服務可用性風險。在 G7 路線圖、NCSC 框架、BIS Project Leap 和主要國家指南文件中出現的模式收斂於三個階段。

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. 發現與 CBOM      │ → │  2. 分類（Mosca）    │ → │  3. 混合部署         │
│  跨所有系統的        │   │  按資料保質期        │   │  雙重信封            │
│  密碼清單            │   │  基於風險優先順序      │   │  經典 + PQC，密碼敏捷│
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### 階段 1 —— 發現與密碼物料清單（CBOM）

遷移無法為未被對映的密碼資產規劃。第一階段因此是產生密碼物料清單——組織中每個非對稱密碼例項的結構化清單，每個例項都標記演算法、金鑰長度、協議上下文、資料敏感性和系統所有者。

### 階段 2 —— 使用 Mosca 方程的風險分類

有了 CBOM，機構可以逐資產應用 Mosca 框架。對每個密碼依賴，問題是 **S + M > Q** 是否成立——資料的保質期加上遷移時間是否超過估計的 CRQC 時間。不等式最嚴重的資產去佇列前面。

### 階段 3 —— 混合部署

一旦優先資產被識別，部署應遵循 Project Leap 中證明並由 NCSC、ANSSI、BSI 和 G7 路線圖認可的混合模式。混合部署並行執行經典演算法和後量子演算法，將其輸出組合成單一信封。複合對經典攻擊（經典演算法今天有效）和量子攻擊（PQC 演算法明天有效）都安全。

## 這要花多少錢以及什麼都不做花得更多

Mastercard 的分析在 [2026 年初報告 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy) 將全球金融部門 PQC 遷移成本估計為 280-420 億美元。這是巨大數字。然而，它們不是相關比較。

相關比較是單一追溯解密事件的成本。對一個其收集的電匯流量、併購通訊或對手方暴露資料在 2032 年變得對對手可讀的機構，運營和聲譽成本不受遷移資本支出線限制。它由相關十年戰略資訊的價值限制——對任何系統重要機構，這實質上大於任何合理的遷移預算。

## 結論

將後量子遷移視為 2026 年董事會級優先事項的理由不是建立在 CRQC 臨近性上。它建立在另外三個不確定的觀察上。

首先，現在收集、未來解密今天正在發生，具有十年以上保密要求的資料無論 CRQC 何時到達都已暴露。其次，主要金融機構密碼資產的遷移即使有足夠資金和領導聚焦也需要 5-7 年——意味著 2026 年開始的專案在 2031 年左右完成，這在 CRQC 機率分佈的保守端內。第三，監管期望在過去 12 個月內實質性加強，2026 年董事會會議記錄中記錄明確 PQC 專案的機構將處於實質上更強的位置。

現在開始的機構有選擇優勢。等待的機構將面對相同的工作但時間更緊。早行動的成本是已知的；晚行動的成本以風險管理設計的方式不對稱。

## 常見問題

**密碼相關量子計算機實際何時存在？**

可信估計差別很大。截至 2026 年初，公開量子演示已達到約 24 到 28 個邏輯量子位元，而 CRQC 估計需要約 6,000 個邏輯量子位元，由 10 萬到數百萬個物理量子位元支撐。專家共識將 CRQC 機率到 2028 年定為一個百分點以下，到 2037-2040 年約 50%。

**為何混合部署而非純後量子？**

三個原因。首先，ML-KEM 和 ML-DSA 雖然經過充分審查，但密碼分析歷史比 RSA 和 ECC 短。混合方案在任一元件成立時仍安全；純 PQC 方案在格問題意外被削弱時暴露。其次，混合保留與尚未遷移的對手方的向後相容性——在多年行業過渡中至關重要。第三，澳大利亞訊號局外的每個主要權威都明確推薦混合用於過渡期：NCSC、ANSSI、BSI、NLNCSA 和 G7 框架。

**我們需要 ML-KEM 和 ML-DSA 兩者，還是可以選一個？**

兩者。ML-KEM 和 ML-DSA 服務不同的密碼角色。ML-KEM 替換 TLS、VPN、移動認證等協議中的金鑰建立原語。ML-DSA 替換 PKI 證書、程式碼簽名、文件簽名、SWIFT 風格認證訊息和身份斷言中的數字簽名原語。

**我們如何衡量這麼大專案的進展？**

三個指標實用且與主要監管框架對齊。**CBOM 覆蓋率**——機構非對稱密碼例項已被清點、分類和標記的百分比。**高風險資產的遷移覆蓋率**——Mosca S + M > Q 條件成立的資產中已移到混合 PQC 的百分比。**密碼敏捷性覆蓋率**——可在不改程式碼、僅配置的情況下交換演算法的密碼依賴系統的百分比。

**再等一年的成本是什麼？**

不是零，也不對稱。等待一年放棄對長壽命資料一年的 HNDL 保護——保密要求延伸到 2040 年的資料比必要長暴露一年。它針對固定監管截止日期（ASD 2030、NSA CNSA 2.0 里程碑、歐盟 2030 關鍵系統目標）壓縮遷移視窗，這轉化為更高的交付風險和更少的排序靈活性。

## 參考資料

- Sebastien Rousseau, (2026). [量子閾值再次移動](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html)。
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber：量子時代的守護演算法](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)。
- Sebastien Rousseau, (2023). [量子金鑰分發：變革銀行業安全](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)。
- Sebastien Rousseau, (2023). [KyberLib：抵禦量子威脅的 Rust 盾牌](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html)。
- G7 網路專家組, (2026). [推進金融部門後量子密碼學過渡的協調路線圖 ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20)。GOV.UK.
- 國際清算銀行, (2025). [Project Leap 第 2 階段：支付系統的量子防護 ⧉](https://www.bis.org/publ/othp107.htm)。BIS.
- NIST, (2024). [FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final)。NIST.
- UK NCSC, (2025). [向後量子密碼學遷移的時間表 ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines)。UK NCSC.
- CMORG, (2025). [後量子密碼學指南 ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf)。CMORG.
- PQCC, (2025). [國際 PQC 要求 ⧉](https://pqcc.org/international-pqc-requirements/)。PQCC.
- PQShield, (2025). [PQC 路線圖與過渡指南 ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/)。PQShield.
- Forrester, (2025). [2026 年亞太預測 ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/)。Forrester.
