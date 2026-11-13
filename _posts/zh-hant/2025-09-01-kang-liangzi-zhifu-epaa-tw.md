---
title: "抗量子支付：行業必須立即行動（EPAA）"
subtitle: "為何支付行業必須現在採取行動應對量子威脅"
description: "EPAA 量子安全支付白皮書闡述支付行業為何必須立即採取行動應對量子威脅。"
date: "September 1, 2025"
language: "zh-Hant"
locale: "zh_TW"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "藍色光線下的量子計算電路板"
keywords: "EPAA, 抗量子支付, 後量子密碼學, ML-KEM, ML-DSA, SWIFT, SEPA, HNDL, NIST, FIPS 203"
---

## 量子對支付系統的威脅

現代支付基礎設施依賴公鑰密碼學——RSA、ECC 和 Diffie-Hellman——來認證交易、保護持卡人資料並保障金融機構之間的訊息安全。這些演算法支撐 SWIFT、SEPA、實時全額結算系統以及目前執行的幾乎所有卡組織。

執行 Shor 演算法的量子計算機將能夠破解這些密碼原語。雖然容錯量子機器尚未達到所需規模，但 IBM、Google 等所展示的硬體發展軌跡使這成為工程時間表問題而非理論問題。美國國家標準與技術研究院（NIST）已對此作出回應，定型了其首批後量子密碼標準（FIPS 203、204 和 205）。

## "現在收集、未來解密"的風險

威脅並不侷限於量子計算機達到足夠能力的未來日期。國家級行為者和資深對手已經在攔截並儲存今天的加密資料，意圖在量子資源可用時解密。這種"現在收集、未來解密"（HNDL）策略意味著任何具有長期敏感性的支付資料——監管記錄、合規檔案、合同義務——已經處於風險中。

金融監管機構已開始響應。新加坡金融管理局（MAS）已釋出關於量子就緒的指引。澳大利亞審慎監管局（APRA）已在其技術韌性框架中標記密碼風險。歐盟數字運營韌性法案（DORA）要求 ICT 風險管理必須考慮包括量子計算在內的新興威脅。

## 跨支付通道的影響

意義跨越支付基礎設施的全部廣度：

**SWIFT 訊息：** MT 和 MX 訊息格式依賴 TLS 和數字簽名保證完整性與認證。受損的金鑰基礎設施將破壞連線全球超過 11,000 家機構的信任模型。

**SEPA 和即時支付：** 歐洲支付理事會的 SEPA 即時信用轉賬方案在十秒內處理不可撤銷的交易。在此速度下的密碼學受損不會留下人工干預或手動驗證的視窗。

**實時支付系統：** 英國的 Faster Payments、美國的 FedNow 和澳大利亞的 NPP 都共享對經典密碼原語在訊息認證和參與者驗證上的依賴。

**合規與長壽命資料：** 出於監管目的保留的支付記錄——通常被要求保留 5 至 10 年或更長——將比保護它們的密碼學的安全保證活得更久。[ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) 遷移專案必須考慮其產生資料的密碼學保質期。

**區塊鏈與分散式賬本技術：** 依賴橢圓曲線密碼學的數字資產平臺和代幣化支付工具面臨來自量子演算法的直接且已知威脅。

## 組織現在必須做什麼

向量子安全密碼學的過渡不是單次升級，而是需要結構化準備的多年專案：

**密碼學清單：** 組織必須編目依賴經典公鑰密碼學的每個系統、協議和資料儲存。這包括 TLS 證書、API 認證、HSM 配置、金鑰管理系統和靜態資料加密。

**後量子演算法採用：** NIST 已標準化用於金鑰封裝的 ML-KEM（FIPS 203）和用於數字簽名的 ML-DSA（FIPS 204）。組織應開始在非生產環境中測試這些演算法，併為關鍵系統制定遷移路線圖。

**密碼學敏捷性：** 系統必須被設計——或重構——使密碼演算法可在不需要完全應用重新設計的情況下被替換。這一原則同樣適用於支付閘道器、訊息中介軟體和麵向客戶的 API。

**混合方法：** 在過渡期間，將經典與後量子演算法結合的混合密碼方案提供縱深防禦。這種方法保留向後相容性同時引入量子抗性。

## EPAA 工作組與行業協作

亞太新興支付協會（EPAA）成立了量子安全密碼學工作組，透過協調的行業行動應對這些挑戰。該工作組彙集了支付生態系統的參與者，包括 IBM、HSBC、KPMG、摩根大通和 PayPal 等。

透過在悉尼、香港和新加坡舉行的工作坊，工作組開發了一個用於評估支付系統量子風險並識別實用遷移路徑的共享框架。由此產生的白皮書 [Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa] 代表對挑戰緊迫性和範圍的共識立場。

工作組的分析得出結論：量子安全就緒是當前的基礎設施決策，而非未來的。延遲的組織有可能發現自己無法滿足監管期望、保護長壽命資料，或與已遷移的夥伴保持互操作性。

## 關於作者

Sebastien Rousseau 是 HSBC Bank plc 的高階數字產品經理，在 HSBC 商業與投資銀行內領導企業支付 API 產品。他為 EPAA 量子安全密碼學工作組做出貢獻，並研究後量子密碼學在金融服務中的應用。[閱讀更多關於 Sebastien 的資訊 ❯][00]

## 相關文章

- [[量子金鑰分發](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)：變革銀行業安全][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)：量子時代的守護演算法][rel2]

[00]: /about/index.html "關於 Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "EPAA 抗量子支付白皮書"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "量子金鑰分發：變革銀行業安全"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber：量子時代的守護演算法"
