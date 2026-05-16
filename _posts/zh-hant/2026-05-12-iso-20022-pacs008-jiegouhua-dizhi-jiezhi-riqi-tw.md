---
title: "2026 年 11 月 pacs.008 結構化地址截止日期：六個月視角"
subtitle: "SWIFT CBPR+ 將拒絕非結構化郵政地址——結構化地址截止日期對跨境支付的影響"
description: "2026 年 11 月起 SWIFT CBPR+ 拒絕 pacs.008 中的非結構化地址。約 65% 報文仍不合規，44% 銀行進度滯後。"
date: "May 12, 2026"
language: "zh-Hant"
locale: "zh_TW"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "ISO 20022 pacs.008 結構化地址圖——突出 TwnNm 和 Ctry 欄位的跨境支付報文"
keywords: "ISO 20022, pacs.008, 結構化地址, SWIFT, CBPR+, SR2026, 跨境支付, 制裁篩查, pain.001, 銀行業"
---

自 2026 年 11 月中旬起，SWIFT CBPR+ 將拒絕 pacs.008 與相關跨境支付報文中的非結構化郵政地址。約 65% 報文仍不合規，44% 銀行進度滯後，整改視窗比多數就緒專案設計的更快關閉。

---

> **核心要點**
>
> - 從 **2026 年 11 月** 起，SWIFT CBPR+ 將不再接受跨境支付報文中的非結構化郵政地址。該變化適用於 **pacs.008**（客戶信用轉賬）、**pacs.009**（FI 信用轉賬）、**pacs.004**（退回）、**pacs.003**（直接借記），以及向其供數的上游 **pain.001** 流。
> - 至少 **城市名（TwnNm）** 和 **國家（Ctry）** 必須存在於專用結構化欄位中。**街道名（StrtNm）** 以及 **建築編號（BldgNb）** 或 **郵政信箱（PstBx）** 強烈建議提供。僅靠自由文字地址行（AdrLine）將不再滿足關鍵當事方欄位的要求。
> - 該變化提高制裁篩查準確性、降低人工修復率並保護直通處理——但僅對那些已整改上游客戶資料（而不僅是報文引擎）的機構有效。
> - 行業就緒情況不平衡。截至 2026 年 3 月，約 **65% 的 CBPR+ 報文仍承載非結構化地址**，**44% 的銀行** 進度滯後，平均 **32% 的客戶地址記錄** 仍未結構化。
> - 開源工具——包括 **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 工具包和 API")**，一個用於生成、驗證和編排 pacs.008 報文流的 Python 庫和 FastAPI 服務——可在報文到達 SWIFT 網路前透過自動化模式驗證、地址質量檢查和 CI 級強制執行壓縮整改時間線。

---

## 一個早就要來的截止日期

2026 年 11 月的結構化地址要求並非突然的監管舉措。它從原始 [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) 遷移宣佈以來一直在 SWIFT CBPR+ 路線圖上，緊隨 2025 年 11 月 MT/MX 共存的結束。2026 年改變的是臨近度。約剩六個月，業界現處於未解決資料質量問題成為運營風險的視窗內。

資料明白地講述故事。SWIFT 自身 2026 年 3 月社群更新指出 [約 65% 支付報文仍包含非結構化地址 ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed)，且採用在地域與機構型別間不均。2026 年 3 月 [RedCompass Labs 對 308 位資深支付專業人士的調查 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022) 發現，44% 的銀行目前進度滯後，無法滿足結構化地址截止日期——儘管平均花費 2000 萬美元（最大機構超 3000 萬美元）於 2026 年就緒，平均額外指派 13 名員工到 ISO 20022 專案。同項調查發現平均 32% 的客戶地址記錄仍未結構化，60% 的銀行報告核心銀行系統在支援結構化地址欄位時存在缺口。

換言之，這不是再加一個月報文引擎工作就能解決的問題。這是從報文層向上遊執行到入網系統、KYC 流程、企業渠道及數十年累積的自由文字客戶主資料中的資料質量問題。

## 規則實際要求什麼

根據 SWIFT CBPR+ 標準釋出 2026（SR2026），關鍵要求原則上簡單明瞭，細節上不容差錯。從 2026 年 11 月中旬起，CBPR+ 支付報文中所有代理和當事方的 [城市名和國家必須在指定結構化欄位中提供 ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed)，例外極為有限（camt.052、camt.053、camt.054 的對賬單和通知，加上少數行政報文仍在嚴格要求之外）。對代理，僅繼續使用 BIC 仍是名稱-地址的有效替代。

截轉後允許兩種地址格式：

- **完全結構化** —— 郵政地址每個元件對映到其專用 ISO 20022 元素：StrtNm（街道名）、BldgNb（建築編號）或 BldgNm（建築名）、PstCd（郵政編碼）、TwnNm（城市名）、CtrySubDvsn（國家細分）、Ctry（國家，ISO 3166-1 alpha-2 程式碼）。這是 SWIFT 明確確定為可能時更可取的選項格式。
- **混合** —— 城市名和國家填充於其結構化欄位，地址其餘部分可使用最多兩個非結構化 AdrLine 元素。重要的是，[結構化元素不得在非結構化行中重複 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf)；對任何給定元件，地址只能是其一。

完全非結構化地址——整個地址坐落於 AdrLine 元素中且無 TwnNm 或 Ctry——將不被接受用於任何受影響當事方欄位。歐洲支付理事會已將其 SEPA 規則書對齊至同一截轉，因此 [從 2026 年 11 月 15 日起，SCT、SDD 和 SCT Inst 也將禁止非結構化格式 ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/)。對齊是刻意的：SWIFT 和 EPC 已設計了單一行業截轉週末。

為消除疑慮，[pacs008 文件直接列出受影響報文 ⧉](https://pacs008.com/structured-address/)：pacs.008（客戶信用轉賬中的債務人和債權人）、pacs.009（FI 信用轉賬和代付中的機構地址）、pacs.004（退回中的當事方地址）和 pacs.003（直接借記）。要求也流向上游：承載非結構化地址的企業 pain.001 檔案將在收款行阻塞合規 pacs.008 生成。

## 為何行業將此作為優先事項

結構化地址的理由不是美學。是運營性的，並體現在三處。

**制裁篩查。** 單一最大的實際收益是結構化地址讓篩查系統將當事方名稱與位置資料分開。自由文字地址塊在城市名碰巧與被制裁人名 token 重疊或自由文字中嵌入的國家被完全錯過時常造成誤報。結構化欄位讓篩查引擎確定性地應用國家特定風險規則，使針對國家程式碼而非猜測解析字串執行制裁名單匹配成為可能。CGI UK 2026 年 3 月釋出的分析明確強調這一點：[結構化地址資料正在成為運營韌性的核心，而不僅是合規義務 ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement)。

**人工修復率。** 今天的跨境支付以人工調查、異常處理和修復佇列形式承擔顯著運營成本——其中很多由篩查或路由系統無法自信解析的地址驅動。已遷移到結構化地址的銀行報告直通處理異常顯著降低，特別是在中間走廊流，其中中介代理此前必須解釋他們未發起的自由文字資料。

**網路級強制執行。** SR2026 在 SWIFT 網路層加強驗證。一些新檢查最初將以非阻塞模式執行——標記資料質量問題但不停止支付——但軌跡明確，截轉後，[不符合規範的報文將被直接拒絕 ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/)。幾個美國支付通道（Fedwire、CHIPS）和 SWIFT CBPR+ 正趨同於本質上相同的時間表，消除了一些機構在早期計劃中假定的分階段截轉選項。

## 欄位級檢視：報文中變化的內容

pacs.008 報文自 2023 年 3 月初始 CBPR+ 使用指南上線以來就已承載結構化地址支援。2026 年 11 月變化的不是模式——是驗證。迄今為止，銀行被允許用自由文字填充 AdrLine 元素並透過網路傳遞。從截止日起，當事方塊的內容必須滿足最低結構化欄位要求。

### 必需、推薦與停用

| 元素 | XPath（在 `PstlAdr` 下） | 2026 年 11 月後狀態 | 註釋 |
|---|---|---|---|
| 城市名 | `<TwnNm>` | **強制** | 每受影響當事方至少一個結構化城市名 |
| 國家 | `<Ctry>` | **強制** | ISO 3166-1 alpha-2 程式碼 |
| 街道名 | `<StrtNm>` | 強烈推薦 | 完全結構化格式所需 |
| 建築編號 | `<BldgNb>` | 推薦 | BldgNb 或 PstBx 二者其一，不能同時 |
| 郵政信箱 | `<PstBx>` | 推薦 | BldgNb 的替代 |
| 郵政編碼 | `<PstCd>` | 推薦 | 某些本地方案要求 |
| 國家細分 | `<CtrySubDvsn>` | 可選 | 州、地區、省份 |
| 地址行（自由文字） | `<AdrLine>` | **受限** | 混合下最多 2 行；從不與結構化欄位中相同元件並存 |
| 地址型別 | `<AdrTp>` | 可選 | 郵政地址推薦使用 `ADDR` |

*來源：SR2026 SWIFT CBPR+ 使用指南與 [pacs008.com 結構化地址文件 ⧉](https://pacs008.com/structured-address/) 的綜合。*

實際意義是：任何仍僅依賴 AdrLine 的機構——無論是自己的報文生成、從企業客戶接收的 pain.001 檔案中，或是飛行中豐富支付所用的主資料記錄——都需要在截轉前將該資料遷移到結構化欄位。SWIFT 的飛行中翻譯服務可在過境中幫助，但 [自 2026 年 1 月起收取附加費 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq)，且無法可靠解析每種地址格式。SWIFT 也釋出了 [一個開源 AI 地址結構化模型 ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model)，基於 200 多個國家資料訓練，可從非結構化遺留資料推斷城市和國家並附帶信心分數，但它明確是整改輔助工具，而非乾淨上游資料的長期替代。

## pacs008.com 如何幫助壓縮時間線

對需要快速工業化其地址質量和報文驗證管道的機構，[pacs008 ⧉](https://pacs008.com/) 提供專門為 FI 到 FI 客戶信用轉賬工作流設計的 MIT 許可開源工具包和 FastAPI 服務。它解決整改專案最常停滯的三層：資料驗證、XML 生成和管道強制執行。

該工具包的結構化地址能力與 SR2026 要求一致：

- **預生成驗證** 結構化和混合郵政地址欄位，使不合規資料在任何 XML 產生或傳送前被捕獲。
- **標記非結構化地址資料**——會在 2026 年 11 月截止日期後失敗的資料，明確區分混合可接受和完全非結構化情況。
- **雙格式支援** 既支援截止日期前混合格式，也支援截止日期後完全結構化佈局，讓機構能在不破壞與尚未完成自身過渡的對手方互操作性的情況下漸進遷移。
- **CI 管道整合**，使地址質量檢查成為構建過程的一部分，而不是流程末端的事後想法——這是對 [CGI 觀察的實際答覆，即資料治理必須是基礎設計原則 ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement) 而非合規疊加。

除地址外，工具包涵蓋 SR2026 釋出所加強的更廣泛驗證表面：針對 20 個報文特定模式的 JSON 模式驗證、跨 75 個國家的 IBAN 格式和校驗和驗證、針對官方 ISO 20022 模式生成 XML 的 XSD 驗證，以及跨所有 13 個支援 pacs.008 修訂（pacs.008.001.01 到 pacs.008.001.13）的版本感知生成。對運營和合規團隊，它還包括透過 defusedxml 防止 XXE、嚴格路徑遍歷保護以及結構化 JSON 日誌中的 PII 遮蔽以支援 GDPR 和 PCI DSS 要求——這是生產支付流中不可協商但常被供應商主導遷移晚期改裝的控制。

該庫 [在 PyPI 上 ⧉](https://pypi.org/project/pacs008/) 作為 `pip install pacs008` 包提供，並在 [GitHub ⧉](https://github.com/sebastienrousseau/pacs008) 上提供完整原始碼透明度。

需要精確說明範圍。pacs008 是報文層工具包；它不替代支付引擎、篩查系統或機構仍需在源頭進行的客戶主資料整改。它做的是把整改工作變得可強制執行——將結構化地址合規從長管道末端的人工審查變為生成點的自動門。對時間緊迫的專案，該門是乾淨截轉與截轉後激增拒絕之間的差別。

## 工具景觀

pacs008 位於 ISO 20022 報文工具更廣生態系統中，方法選擇取決於機構的棧、規模和遷移哲學。開源和商業景觀包括 [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022)（廣泛多類別 Python 庫，帶 beta 驗證）、相關的 [pain001 ⧉](https://pain001.com/) 庫用於上游支付發起、[Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022)（帶 CBPR+ 驗證和翻譯商業層的全面 Apache 2.0 Java 庫）以及多個商業平臺——Mambu、Kyriba、PaymentComponents 等——它們將 ISO 20022 能力捆綁到更廣財庫或支付平臺產品中。

權衡是熟悉的。商業平臺降低內部工程負擔但將機構繫結到可能不匹配自身的供應商路線圖。全面多類別庫覆蓋更廣表面但要求任何單一報文型別更多整合工作。聚焦開源庫——pacs008 用於 FI 到 FI 客戶信用轉賬，[pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) 用於支付發起——最小化需要快速解決特定瓶頸的機構的整合時間，讓機構掌控自己的驗證規則。

## 按行業意味著什麼

2026 年 11 月截止日期對所有機構影響不均。正確響應取決於跨境流量量、現有資料資產成熟度以及機構在支付鏈中扮演的角色。

### 大型代理和跨境銀行

對執行顯著 CBPR+ 流量的一級銀行，結構化地址要求是更大 SR2026 就緒專案中的一個工作流，該專案還涵蓋異常和調查、BAH 強化以及（在美國）Fedwire 和 CHIPS 的同時遷移。RedCompass Labs 資料顯示大多數這些機構在 2026 年就緒上花費 2000–3000 萬美元，交付團隊 10–20 名專家。該組的風險不是技術能力——是交付容量。

### 中型銀行和支付機構

對中型銀行和 EMI/PI 機構，結構化地址要求通常是它們面臨的最重大 2026 義務，因為它們不承擔像一級銀行同樣的周圍工作流負擔。這裡的挑戰通常是上游資料質量。

### 企業和支付服務提供商

透過 pain.001 發起支付的企業位於銀行 pacs.008 生成上游，但不豁免結構化地址要求。銀行不會代表企業客戶追溯填充受益人地址；結構化資料必須源於企業自己的系統。

### 供應商、金融科技和系統整合商

對在支付通道之上構建的供應商，截止日期是 ISO 20022 能力的強制功能，這能力可能被推遲到稍後階段。

## 結論

2026 年 11 月結構化地址截止日期在一種意義上是狹窄變化：兩個必需欄位、幾個推薦欄位，以及一個本不應用於制裁相關資料的自由文字選項的退役。在另一意義上，它是原始 CBPR+ 遷移以來運營上最顯著的 ISO 20022 里程碑，因為它強制結構化資料不僅進入報文層，還進入向其供數的上游系統。

六個月前的行業級就緒圖景並不令人鼓舞。三分之二的 CBPR+ 報文仍承載非結構化地址。近一半的銀行進度滯後。近三分之一的客戶地址記錄仍無法解析。資金已到位——調查一致顯示八位和九位數投資——但工作尚未完成，問題的資料質量維度無法僅靠最後幾個月的支出解決。

現在有幫助的是驗證點的自動化：將規則推到管道中，在問題到達網路前而不是之後捕獲它們。對執行 Python 或 FastAPI 資產的機構，[pacs008 ⧉](https://pacs008.com/) 等開源工具提供無需供應商選擇週期就能做出該轉變的實用方式。

11 月的截轉週末將關閉一章。帶著乾淨資料、自動化驗證和對結構化地址實際為制裁篩查所做工作的工作理解到達的機構將在該週末監控流量。沒有這些到達的機構將在電話上度過它。

## 常見問題

**2026 年 11 月截止日期到底變化什麼？**

從 2026 年 11 月中旬起，SWIFT CBPR+ 將拒絕其當事方欄位包含僅非結構化郵政地址的 pacs.008、pacs.009、pacs.004 和 pacs.003 報文。最低結構化要求是 TwnNm 元素中的城市名和 Ctry 元素中的國家（使用 ISO 3166-1 alpha-2 程式碼）。仍允許混合地址——城市和國家在結構化欄位中，加上最多兩個用於其餘元件的自由文字 AdrLine 元素——但同一元件不能同時出現在結構化和非結構化欄位中。完全結構化地址是首選格式。

**哪些報文和哪些當事方欄位受影響？**

對 pacs.008，要求適用於債務人和債權人郵政地址。對 pacs.009，適用於 FI 信用轉賬和代付中的機構地址。對 pacs.004，適用於支付退回中的當事方地址。對 pacs.003，適用於客戶直接借記中的債權人和債務人地址。對賬單和通知報文（camt.052、camt.053、camt.054）和某些行政報文仍在嚴格要求之外。

**結構化、混合和非結構化地址有何區別？**

完全結構化地址將每個元件對映到其專用 ISO 20022 元素：StrtNm、BldgNb 或 PstBx、PstCd、TwnNm、CtrySubDvsn、Ctry。混合地址在結構化欄位中有城市名和國家，地址其餘部分在最多兩個自由文字 AdrLine 元素中；同一元件不得同時出現在兩者中。非結構化地址在 AdrLine 元素中有整個郵政地址而無結構化 TwnNm 或 Ctry——這是 2026 年 11 月針對受影響當事方欄位被退役的格式。

**pacs008.com 如何幫助這一過渡？**

[pacs008 ⧉](https://pacs008.com/) 庫在 XML 生成前驗證結構化和混合郵政地址欄位，標記在截止日期後會失敗的非結構化資料，支援截止日期前混合和截止日期後完全結構化格式，並整合到 CI 管道和批次驗證工作流。它為所有 13 個支援 pacs.008 版本生成 XML，驗證官方 ISO 20022 XSD 模式，並暴露 FastAPI 服務用於自動編排。

**如果我的機構在 2026 年 11 月未就緒會怎樣？**

截轉後，受影響當事方欄位中帶非結構化地址的報文將在網路級被拒絕。實際上這轉化為支付失敗、異常量增加、人工修復激增以及可能的客戶影響。SWIFT 的飛行中翻譯服務對一些過渡情況可用但自 2026 年 1 月起收取附加費且無法可靠解析每種地址格式。

## 參考資料

- Sebastien Rousseau, (2023). [用 pain001 自動化 ISO 20022 合規支付檔案建立](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html)。
- pacs008, (2026). [2026 年 11 月結構化地址截止日期 ⧉](https://pacs008.com/structured-address/)。pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 工具包和 API ⧉](https://pacs008.com/)。pacs008.com.
- SWIFT, (2026). [2026 年 11 月 ISO 20022 里程碑：非結構化地址將被移除 ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed)。SWIFT.
- SWIFT, (2026). [面向金融機構的 ISO 20022 ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions)。SWIFT.
- SWIFT, (2026). [SWIFT AI 地址結構化模型 ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model)。SWIFT.
- RedCompass Labs, (2026). [近一半銀行 ISO 20022 進度滯後 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022)。Financial IT.
- RedCompass Labs, (2026). [ISO 20022 對美國銀行一齊到來 ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/)。RedCompass Labs.
- ClearingPost, (2026). [2026 年 11 月結構化地址截止日期 ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/)。ClearingPost.
- CGI UK, (2026). [2026 年：ISO 20022 和結構化資料強制的決定性一年 ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement)。CGI UK.
- J.P. Morgan, (2026). [ISO 20022 遷移：指導、報文及更多 ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration)。J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022)。ING Wholesale Banking.
- Mambu, (2026). [CBPR+ 已上線 ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice)。Mambu.
- Kyriba, (2026). [ISO 20022 遷移：每個財庫團隊需要了解的下一步 ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/)。Kyriba.
- Standard Chartered, (2025). [ISO 20022 – 渣打地址指南 ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf)。Standard Chartered.
- State Street, (2025). [客戶 ISO 20022 指南 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf)。State Street.
- ISO 20022, (2026). [報文定義目錄 ⧉](https://www.iso20022.org/iso-20022-message-definitions)。ISO 20022.
