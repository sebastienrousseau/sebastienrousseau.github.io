---
title: "面向銀行的代理式工程：2026 年高管團隊與工程師藍圖"
subtitle: "代理式 AI 已從試點走向生產。70% 的銀行已使用，僅五分之一擁有成熟治理模型"
description: "代理式 AI 已在全球銀行業從試點走向生產；70% 機構在用，僅五分之一擁有成熟治理。"
date: "May 17, 2026"
language: "zh-Hant"
locale: "zh_TW"
banner: "https://cloudcdn.pro/stocks/images/hector-j-rivas-1FxMET2U5dU-unsplash.webp"
banner_alt: "銀行代理式工程架構圖——規範驅動的 AI 代理、治理控制平面、量子安全基質和遺留主機現代化流"
keywords: "代理式工程, 規範驅動開發, 銀行, 金融服務, AI 治理, 歐盟 AI 法案, DORA, SR 11-7, COBOL 現代化, Claude Code"
---

# 面向銀行的代理式工程：2026 年高管團隊與工程師藍圖

代理式 AI 已在全球銀行業從試點走向生產。70% 的機構已在某種程度上使用；僅五分之一擁有成熟治理模型。同時，自主對手以機器速度運營，新系統必須互操作的遺留 COBOL 資產是為 1960 年代的批處理假設而編寫的，歐盟 AI 法案的高風險截止日期還有 12 周。這就是銀行需要持有的工程與治理立場。

---

> **核心要點**
>
> - **從隨性編碼（vibe coding）到規範驅動開發（spec-driven development）的過渡不再是願景。** 2025 年 2 月創造"隨性編碼"一詞的 Andrej Karpathy，[一年後承認 ⧉](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/) 該時代正在結束，專業人士的新預設是 **代理式工程**——根據詳細規範編排代理並具有人類監督。
> - 銀行業採用真實且加速。[70% 的銀行業公司 ⧉](https://theuxda.com/blog/agentic-ai-banking-risk-next-financial-crisis-wont-be-human) 報告在某種程度上使用代理式 AI（EY 2026：16% 生產中，52% 試點中）；44% 的金融團隊今年將使用——Wolters Kluwer 報告同比增長 600%+。
> - **治理未跟上步伐。** Deloitte 的 AI 狀況 2026 發現，只有五分之一的公司擁有自主 AI 代理的成熟治理模型。Deloitte 對 MIT AI 風險資料庫的分析識別 [350 多種風險 ⧉](https://www.deloitte.com/us/en/insights/industry/financial-services/agentic-ai-risks-banking.html) 可能由自主或代理行為產生。
> - **威脅格局已工業化。** Anthropic 在 2025 年 11 月披露中國國家支援的 GTG-1002 組劫持 Claude Code 對約 30 個目標進行自主間諜活動，AI **自主處理 80-90% 的戰術運營**。Flashpoint 觀察到 [AI 相關非法討論增加 **1,500%** ⧉](https://www.hstoday.us/subject-matter-areas/cybersecurity/2026-global-threat-intelligence-report-highlights-rise-in-agentic-ai-cybercrime/)，僅在 2025 年 11 月至 12 月間。
> - **遺留資產是無聲約束。** 金融服務 IT 預算的 70-75% 被遺留維護消耗，63% 的銀行仍依賴 2000 年前編寫的程式碼，大多數銀行報告內部只有一兩個人能維護其核心平臺執行的 COBOL。代理式 AI 現在是縮小該差距的主導方法。
> - **監管棧正在收斂。** 歐盟 AI 法案下，**2026 年 8 月 2 日** 觸發高風險 AI 系統的完全可執行性（附件 III 明確包括信用評分和信用度評估）。DORA 已生效。SR 11-7 在監管實踐中已擴充套件到涵蓋 LLM 和代理式系統。違規罰款達 **3500 萬歐元或全球年營業額 7%**。
> - **人類監督不是單一概念。** **HITL**（人在迴路中，代理未經明確人類批准不能執行）與 **HOTL**（人在迴路上，代理在人類監督下自主執行）的區別現在是歐盟 AI 法案第 14 條合規的工作框架，每個高風險代理都需要明確立場說明哪種模型適用。
> - **大多數代理將被購買，而非構建。** DORA 下的第三方風險管理是 2026 年最響亮且未被充分認識的挑戰。供應商將提供銀行部署的大部分代理能力；監管義務仍在銀行，大多數現有供應商合同無法滿足第 13 條文件要求。
> - **代理式工程不是"ChatGPT 加 MCP 伺服器"。** 它是對機構端到端流的結構性所有權立場——客戶旅程、交易生命週期、控制平面、審計基質、量子安全密碼基礎——由機構自己的工程職能構建和運營，而非委託給聊天機器人。

---

## 代理式工程變得不可避免的一年

直到最近，關於金融服務 AI 的對話一直由兩個相鄰但不同的事物主導：生成式聊天介面（有幫助但有限）和層疊到企業資料上的檢索增強生成模式（有用但也有限）。2025 年末到 2026 年初變化的是第三類——自主代理，它們規劃、執行和完成多步驟工作流，人類監督有限——從技術演示轉向運營現實，並同時跨越企業和威脅行為者。

[2025 年 2 月創造"vibe coding"一詞 ⧉](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/) 的 Andrej Karpathy，在接下來的一年裡觀察專業工程師超越它。他的修訂——*"代理式工程"*——現在是整個行業的工作術語。轉變的實質直接：在 2026 年嚴肅的軟體工作中，工程師 99% 的時間不直接編寫程式碼。他們編排代理來做，同時擔任監督。

這一轉變聽起來像工程團隊對話。在銀行業不是。這是董事會層面的對話，因為正在重寫內部程式碼生成方式的相同代理能力，也在重寫外部對手的運營方式、監管機構期望監督執行的方式以及機構邊界的定義方式。

## 銀行業採用現狀

總體圖景明確。根據 2026 年多項調查的研究，[70% 的銀行高管 ⧉](https://thefinancialbrand.com/news/artificial-intelligence-banking/autonomous-ai-agents-redefine-banking-growth-196646) 報告其公司已在某種程度上使用代理式 AI。[Gartner 預測 ⧉](https://www.thenews.com.pk/latest/1385186-why-british-banks-push-for-agentic-ai-is-worrying-uk-regulators) 到 2026 年底約 40% 的金融服務公司將以某種形式執行 AI 代理。

執行圖景較不令人鼓舞。[KPMG 報告 ⧉](https://neurons-lab.com/article/agentic-ai-in-financial-services-2026/) 99% 的公司計劃將自主代理投入生產，但 **只有 11% 已這樣做**。EY 發現 34% 的領導者已開始使用 AI 代理，只有 14% 已完全實施。Forrester 發現 **57% 的組織認為缺乏內部能力** 利用代理式 AI。

英國金融行為監管局已 [公開提出關切 ⧉](https://www.thenews.com.pk/latest/1385186-why-british-banks-push-for-agentic-ai-is-worrying-uk-regulators) 部署速度超過治理成熟度——FCA 首席資料官 Jessica Rasu 將這種緊張定性為近期零售消費者風險。麥肯錫單獨 [警告 ⧉](https://www.unboxfuture.com/2026/05/the-autonomous-banker-how-ai-agents.html) 未能調整業務模式的銀行 **到 2030 年面臨侵蝕全球利潤高達 1700 億美元** 的風險。

## 銀行必須內化的三個風險向量

在任何架構對話之前，董事會的注意力應放在三個特定於代理式系統、比大多數銀行規劃得更早到達的風險上。

### 1. 自主對手

2026 年最令人迷失方向的發展是代理式 AI 在攻擊側的運營化。2025 年 8 月，Anthropic 披露了一類活動，稱為 [*vibe hacking* ⧉](https://www.anthropic.com/news/detecting-countering-misuse-aug-2025)：網路犯罪分子使用代理式 AI 大規模執行復雜攻擊，AI 嵌入偵察、憑證收集、網路滲透和被盜資料分析。[2025 年 11 月 ⧉](https://www.anthropic.com/news/disrupting-AI-espionage)，Anthropic 披露它已破壞由中國國家支援組（指定 **GTG-1002**）發起的活動，該組劫持 Claude Code 例項對 **約 30 個國防、能源和技術目標** 進行自主間諜活動，AI 處理 **80-90% 的戰術運營**，以 **每秒數千次請求** 執行——人類操作員不可能的速度。

2026 年 1 月，Step Finance——基於 Solana 的 DeFi 投資組合經理——以將裝置入侵轉變為 **2700-3000 萬美元損失** 的方式被攻破，因為該公司的 AI 交易代理有許可權在沒有人類批准的情況下執行大額轉賬。攻擊者對 AI 本身進行社會工程，聲稱在執行授權的漏洞懸賞計劃。

總趨勢是銀行必須內化的。Flashpoint 2026 全球威脅情報報告識別 [AI 相關非法討論增加 **1,500%** ⧉](https://www.hstoday.us/subject-matter-areas/cybersecurity/2026-global-threat-intelligence-report-highlights-rise-in-agentic-ai-cybercrime/)。摩根大通的 Jamie Dimon [公開明確 ⧉](https://www.cnbc.com/2026/05/08/anthropic-mythos-ai-cybersecurity-banks.html) 該技術的初始優勢在進攻，而非防禦。

### 2. 程式碼質量回歸

第二個向量是內部和較安靜的。在沒有規範紀律和嚴格驗證的情況下，LLM 生成的程式碼以實質上高於人類編寫程式碼的速率攜帶缺陷出貨。[SonarQube 對五個前沿 LLM 的分析 ⧉](https://www.augmentcode.com/guides/what-is-spec-driven-development) 生成 Java 程式碼發現，**Llama 3.2 90B 輸出中檢測到的漏洞中超過 70% 被評為 BLOCKER 嚴重性**。Pearce 等人（IEEE S&P）發現 **約 40% 的安全敏感語境中 LLM 生成的程式包含漏洞**。

對非監管行業，這是生產力稅。對銀行，這是複合的監管和運營風險。

### 3. 遺留錨

第三個向量是銀行已最瞭解的，代理式過渡使它同時更緊迫和更可處理。超過 **70% 的財富 500 強公司仍依賴大型機**，[Computer Weekly 分析指出 ⧉](https://www.computerweekly.com/opinion/AI-to-help-mainframes-remain-business-critical-in-2026)，通常建立在數十年交織的 COBOL 和 RPG 與自定義業務邏輯上。在金融服務中具體而言，遺留技術消耗 [**70-75% 的年度 IT 支出** ⧉](https://www.cio.com/article/4085184/using-ai-to-modernize-mainframes-turning-legacy-tech-into-a-strategic-advantage.html)。

2026 年 2 月發生的變化是可信代理工具用於遺留現代化的到來。Anthropic 宣佈 Claude Code [可以對映 COBOL 依賴、記錄工作流並識別風險 ⧉](https://www.cnbc.com/2026/02/23/ibm-is-the-latest-ai-casualty-shares-are-tanking-on-anthropic-cobol-threat.html)，人類分析師需要數月才能浮出。

## 為何隨性編碼不能成為銀行業預設

值得精確說明隨性編碼——短提示、觀察輸出、迭代——為何作為受監管資產中的預設工作流失敗。失敗模式不是明顯的（LLM 偶爾幻覺）。失敗模式是結構性的，在四個地方同時出現：**缺乏共享約定**、**上下文衰減**、**不可見缺陷累積** 和 **監管可追溯性問題**。

## 在受監管資產中的規範驅動開發

規範驅動開發（SDD）顛倒工作順序。團隊不直接跳入實現並與代理迭代，而是首先產生規範——架構決策、要求、介面契約、成功標準、安全約束——代理生成滿足規範的程式碼。驗證是結構化的：規範定義輸出必須做什麼，單獨的過程（測試生成、程式碼評審、適用時的形式驗證）檢查它是否已完成。

實際工具在 2025 年末和 2026 年初已合併。[GitHub 的 Spec Kit ⧉](https://www.cgi.com/en/blog/artificial-intelligence/spec-driven-development)（2025 年末釋出）在程式碼生成前形式化意圖。AWS 在其 Kiro IDE 中直接嵌入規範優先工作流。

對銀行，重要的變體是 Augment Code 的分析所稱的 **規範錨定開發**——規範優先，AI 生成受其約束的程式碼，額外治理層（憲法約束、監督檢查點、人類批准門）位於生成和合並之間。

## 現在適用的監管棧

2026 年銀行業 AI 周圍的監管邊界不再是檢查清單；它是需要一起推理的重疊義務棧。最重要的單一日期是 **2026 年 8 月 2 日**，歐盟 AI 法案的 [高風險系統義務變得完全可執行 ⧉](https://web.archive.org/web/20260218204305/https://ai2.work/economics/eu-ai-act-high-risk-rules-hit-august-2026-your-compliance-countdown/)。附件 III 明確將信用評分、信用度評估、壽險和健康險中的風險評估，以及個人金融立場的評估或分類分類為高風險。違規罰款達 **3500 萬歐元或全球年營業額 7%**。

與 AI 法案並存：

- **DORA**（數字運營韌性法案）自 2025 年 1 月起生效，建立明確涵蓋關鍵金融功能中使用的 AI 系統的 22 項 ICT 風險管理義務。
- **SR 11-7**——美聯儲和 OCC 的模型風險管理指南，最初於 2011 年編寫——已 [在監管實踐中擴充套件 ⧉](https://aegisaicompliance.com/ai-governance-for-banks/) 以涵蓋 LLM 和代理式系統。
- **NIST AI RMF**（1.0，2023 年 1 月）在美國是自願的，但被聯邦監管機構引用為基線。
- **ISO/IEC 42001**（2023 年 12 月釋出）是首個可認證的 AI 管理系統標準。
- **英國 SM&CR 和 Consumer Duty**——高階經理與認證制度現在要求為每個高風險 AI 系統指定問責。
- **G7 後量子路線圖**（2026 年 1 月）、NCSC 三階段遷移框架和 BIS Project Leap 發現與該棧並存。

## AI 輔助開發的三種模式比較

| 維度 | 隨性編碼 | 規範驅動開發 | 代理式工程 |
|---|---|---|---|
| 主要輸入 | 短提示 | 形式規範 | 規範 + 代理編排計劃 |
| 工程師角色 | 提示迭代者 | 規範作者 | 編排者和驗證者 |
| 輸出紀律 | 直接程式碼生成 | 受規範約束的程式碼 | 產生程式碼、測試、文件的多代理工作流 |
| 審計追蹤 | 聊天曆史（未持久化） | 規範 + 生成的程式碼 + 測試 | 規範 + 代理追蹤 + 驗證工件 |
| 缺陷率（僅 LLM） | 10-40% 漏洞率（文獻基線） | 受規範約束顯著降低 | 驗證門下最低 |
| 監管可追溯性 | 對高風險 AI 不足 | 與歐盟 AI 法案第 12 條相容 | 為第 12 條 + SR 11-7 + DORA 設計 |
| 適合銀行業？ | 否，對生產 | 是，帶治理 | 是，帶成熟治理 |
| 能力上限 | 受單次提示約束 | 受規範質量約束 | 受編排質量約束 |

*來源：Karpathy 評論 (2026)、[Augment Code SDD 分析 ⧉](https://www.augmentcode.com/guides/what-is-spec-driven-development) 和 LLM 程式碼生成漏洞率學術文獻的綜合。*

## 構建代理式銀行：架構檢視

這些工作流背後的戰略立場是高管團隊需要明確擁有的。銀行業代理式工程不是開發者生產力倡議。它是觸及端到端客戶旅程、整個交易生命週期以及兩者之下的密碼和審計基質的機構能力。該能力的四層值得直接執行關注，自上而下：

> **第 4 層 — 代理控制平面**
> 治理、審計、終止開關、行為異常檢測、人類覆蓋。每個代理類的 HITL 和 HOTL 監督配置。
>
> **第 3 層 — 代理式工作流**
> 客戶旅程、內部運營、開發管道。高風險流預設規範驅動。
>
> **第 2 層 — 資料和模型層**
> AIBOM（AI 物料清單）、模型登錄檔、檢索基質、提示模板版本控制、微調譜系。
>
> **第 1 層 — 量子安全基礎**
> ML-KEM、ML-DSA、混合 PKI、密碼敏捷性。每個更高層完整性宣告所依賴的基質。

## 實踐中的人類監督：HITL vs HOTL

監管機構在 2026 年最關注的第 4 層內的單一區別是兩種監督模型。兩者都是人類監督的形式；它們在延遲、規模以及監管機構願意授予的關於代理行為的假設上不同。

**人在迴路中（HITL）** 是代理未經明確人類批准不能執行後果行動的模型。代理準備決策、呈現並等待。

**人在迴路上（HOTL）** 是代理在有界引數內自主執行的模型，人類實時監控遙測並保留隨時停止代理的權威。

歐盟 AI 法案第 14 條不規定 HITL 與 HOTL；它要求人類監督是 **有意義的**。

## 購買 vs 構建：第三方代理問題

潛入大多數銀行的 2026 年現實是它們將不會主要 *構建* 代理能力。它們將 *購買* 它。

對於處於購買地位的銀行，三個實踐紀律適用：**向供應商要求 AIBOM**、**測試黑盒而非小冊子**、**根據第 13 條條款重新談判合同**。

## 按銀行型別意味著什麼

### 一級綜合銀行

具有 1 萬億美元以上資產負債表和全球存在的機構同時是最暴露的（最廣泛的監管邊界、最大的遺留資產、自主對手的最高價值目標）和資源最豐富的。戰略優先事項是首先構建控制平面——上面架構的第 4 層。

### 中型和區域銀行

二級銀行的競爭問題比一級銀行更尖銳。實際答案是在小套經審查的供應商上硬標準化（合同滿足第 13 條文件要求），投資規範驅動開發紀律。

### 金融科技、PSP 和加密鄰近機構

金融科技和支付機構部分有相反問題：敏捷度高，治理常低於同行銀行。戰略紀律是將 AI 治理視為產品就緒門而非合規疊加。

### 內部工程職能

對閱讀本文的工程師和研究者，重要的工作紀律是日常的。將工作的重心從輸入字元移到產生規範和驗證工具。

## 到 2026 年 8 月的 12 周行動計劃

對在現在到歐盟 AI 法案執行日期之間執行代理式工程專案的執行贊助者，工作壓縮為 12 周序列：

- **第 1-2 周 —— 製作 AIBOM。**
- **第 3-4 周 —— 按系統分類監督模型。**
- **第 5-6 周 —— 構建或強化代理控制平面。**
- **第 7-8 周 —— 供應商合同審查。**
- **第 9-10 周 —— 幹執行符合性評估。**
- **第 11-12 周 —— 截止前驗證和董事會簽字。**

## 結論

過去六個月在行業中結晶的尖銳觀察是，舊的企業級運營方式不是被新技術超越，而是被新工作模式超越。

內部擁有這一立場的機構——將代理式工程視為銀行的結構效能力而非從供應商採購的生產力疊加——將在未來兩年複合優勢。不這樣做的機構將在未來兩年透過事件報告和監管發現來發現它們應該構建什麼。

## 常見問題

**生成式 AI、代理式 AI 和代理式工程之間的區別是什麼？**

生成式 AI 響應提示產生內容；它是反應性的。代理式 AI 自主追求定義的目標，訪問資料、使用工具，並在多步驟工作流中採取行動，不需要在每一步都有人類提示。代理式工程——[Karpathy 在 2026 年採用的術語 ⧉](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/)——是根據詳細規範編排代理與人類監督的工作紀律。

**為何 2026 年 8 月歐盟 AI 法案截止日期對銀行如此重要？**

AI 法案附件 III 明確將幾個核心銀行 AI 用例分類為高風險：自然人的信用度評估和信用評分、壽險和健康險中的風險評估和定價，以及個人金融立場的評估或分類。

**HITL 和 HOTL 之間的實際區別是什麼？**

HITL 意味著代理未經明確人類批准不能執行後果行動。HOTL 意味著代理在有界引數內自主執行，人類監控遙測並保留隨時停止的權威。

**我們的大多數代理將來自供應商。我們如何為不是我們構建的系統滿足 DORA 和歐盟 AI 法案？**

監管義務在部署者，而非供應商。實際答案三方面：要求供應商在簽字前提供文件化 AIBOM、對代理進行行為測試、重新談判供應商合同以包括第 13 條文件權利。

**銀行實際應擔心代理式對手到什麼程度？**

誠實的答案是威脅是真實的，在運營上與之前的網路威脅不同。2025 年 11 月 Anthropic 披露的 GTG-1002 是規範例子。

**代理式 AI 僅僅是"ChatGPT 加 MCP 伺服器"嗎？**

不，這是當前市場中最重要的誤解之一。聊天介面增強 MCP 伺服器是在有界會話中檢索和處理資料的有用模式。代理式工程是機構的結構效能力。

**銀行在未來 12 周應做的最重要的事是什麼？**

三件事，依次：製作 AI 物料清單、為任何當前做出或實質影響客戶決策的 AI 系統構建代理控制平面、將內部工程文化從隨性編碼移到規範驅動開發。

## 參考資料

- Sebastien Rousseau, (2026). [保障賬簿：後量子遷移的董事會級指南](https://sebastienrousseau.com/2026-05-14-securing-the-ledger-post-quantum-migration-corporate-finance/index.html)。
- Sebastien Rousseau, (2026). [2026 年 11 月 pacs.008 結構化地址截止日期](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html)。
- Sebastien Rousseau, (2026). [量子閾值再次移動](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html)。
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber：量子時代的守護演算法](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)。
- Mansurova, M. (2026). [從隨性編碼到規範驅動開發 ⧉](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/)。Towards Data Science.
- CGI, (2026). [規範驅動開發 ⧉](https://www.cgi.com/en/blog/artificial-intelligence/spec-driven-development)。CGI.
- Augment Code, (2026). [什麼是規範驅動開發？完整指南 ⧉](https://www.augmentcode.com/guides/what-is-spec-driven-development)。Augment Code.
- Deloitte, (2026). [管理銀行業 AI 代理新風險浪潮 ⧉](https://www.deloitte.com/us/en/insights/industry/financial-services/agentic-ai-risks-banking.html)。Deloitte 金融服務中心.
- Anthropic, (2025). [檢測和應對 AI 濫用：2025 年 8 月 ⧉](https://www.anthropic.com/news/detecting-countering-misuse-aug-2025)。Anthropic.
- Anthropic, (2025). [破壞首次報告的 AI 編排網路間諜活動 ⧉](https://www.anthropic.com/news/disrupting-AI-espionage)。Anthropic.
- Flashpoint, (2026). [2026 全球威脅情報報告 ⧉](https://www.hstoday.us/subject-matter-areas/cybersecurity/2026-global-threat-intelligence-report-highlights-rise-in-agentic-ai-cybercrime/)。HSToday / Flashpoint.
- 歐盟委員會, (2024). 關於人工智慧的歐盟法規 (EU) 2024/1689（歐盟 AI 法案）。
- Regulativ, (2026). [歐盟 AI 法案 2026 年 8 月截止日期 ⧉](https://www.finextra.com/blogposting/31653/the-eu-ai-acts-august-2026-deadline-what-financial-services-firms-must-do-now)。Finextra.
- AegisAI Compliance, (2026). [銀行 AI 治理：SR 11-7 和歐盟 AI 法案合規指南 ⧉](https://aegisaicompliance.com/ai-governance-for-banks/)。AegisAI.
- The Financial Brand, (2026). [自主 AI 代理將如何真正重新定義銀行業增長 ⧉](https://thefinancialbrand.com/news/artificial-intelligence-banking/autonomous-ai-agents-redefine-banking-growth-196646)。The Financial Brand.
- Computer Weekly, (2026). [AI 幫助大型機在 2026 年保持業務關鍵 ⧉](https://www.computerweekly.com/opinion/AI-to-help-mainframes-remain-business-critical-in-2026)。Computer Weekly.
- CIO Magazine, (2025). [使用 AI 現代化大型機 ⧉](https://www.cio.com/article/4085184/using-ai-to-modernize-mainframes-turning-legacy-tech-into-a-strategic-advantage.html)。CIO Magazine.
- CNBC, (2026). [Anthropic 的 Mythos 引發網路安全"歇斯底里" ⧉](https://www.cnbc.com/2026/05/08/anthropic-mythos-ai-cybersecurity-banks.html)。CNBC.
