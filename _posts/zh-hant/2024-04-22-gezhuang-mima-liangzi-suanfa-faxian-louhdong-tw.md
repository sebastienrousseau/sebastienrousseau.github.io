---
title: "格基密碼學的量子演算法中發現漏洞"
subtitle: "陳逸雷 LWE 量子演算法的漏洞：對 NIST 後量子密碼學標準化的重新評估"
description: "陳逸雷的 LWE 量子演算法被發現存在漏洞，格基密碼學暫時保持安全，但量子抗性研究仍需推進。"
date: "April 22, 2024"
language: "zh-Hant"
locale: "zh_TW"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "MidJourney 生成影象 - 紅藍色調的數字節點網路"
keywords: "陳逸雷, LWE, 量子演算法, 格密碼學, NIST, 後量子密碼學, Kyber, Dilithium, BGV, TFHE"
---

## 量子困局：在陳逸雷演算法影響下重新評估 NIST 後量子密碼學標準化

繼我此前關於[格基密碼學量子演算法挑戰][00]的文章後，我有必要更新[陳逸雷研究 ⧉][01]的最新進展。

出乎意料的是，清華大學交叉資訊研究院（IIIS）助理教授陳逸雷報告稱，同行科學家 Hongxun Wu 與 Thomas Vidick 已獨立在其用於解決 Learning with Errors（LWE）問題的多項式時間量子演算法中發現一個漏洞。

該漏洞使演算法失效，陳已承認其方法不如最初宣稱的那樣成立。

## 陳量子演算法中的漏洞

漏洞在陳演算法的第 9 步被發現，他表示不知如何修復。這一發現讓密碼學界鬆了一口氣——它證實了 LWE 問題（後量子密碼學保護方法的關鍵組成部分）仍保持安全。

陳的論文還研究了其他複雜格問題，如多項式近似因子內的決策版最短向量問題（GapSVP）與最短獨立向量問題（SIVP）。雖然其演算法的漏洞不直接影響這些問題，但它對格基密碼學量子演算法的穩健性提出了疑問。

但根據 [Nigel Smart 的頁面 ⧉][02]，所提議的對 LWE 的量子攻擊存在缺陷，並未破壞 [Kyber ⧉][04]、[Dilithium ⧉][05]、[BGV ⧉][06] 或 [TFHE ⧉][07] 等格密碼方案。

## 對 NIST 後量子密碼學標準化過程的意義

陳的研究間接對 [NIST 後量子密碼學（PQC）標準化過程 ⧉][03] 及量子抗性密碼演算法的選擇引發了擔憂與疑問。

[CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) 與 CRYSTALS-Dilithium 方案——NIST PQC 標準化過程的入圍者之一——是已被嚴格測試和評估量子抗性的格基密碼方案的例子。然而，持續測試和完善這些方案以確保其長期安全與可行性至關重要。

NIST、密碼學界與企業必須保持警覺，繼續探索後量子密碼學的替代數學基礎，以確保對量子抗性安全有一套穩健多元的選項。

## 後量子密碼學的未來

陳演算法中漏洞的發現凸顯了科學過程中同行評議的關鍵角色。它也凸顯了對即時審查、反饋與辯論的需求。

量子時代已經開始，發展量子抗性密碼方法需要全球規模的協作措施，以確保我們的數字基礎設施在面對不斷進步的量子計算能力與量子至高競爭時的安全。

NIST PQC 標準化過程是朝該方向邁出的重要一步，但僅是開始。陳演算法中的漏洞是對未來挑戰與不確定性的強烈提醒，但也是密碼學界加倍努力、推動可能邊界的行動號召。

這是後量子密碼學領域的一項引人入勝的發展，看 NIST PQC 標準化過程如何響應這一新資訊將很有意思。

## 結論

陳逸雷解決 LWE 問題的量子演算法中發現的漏洞，證明了嚴格的同行評議與協作在開發量子抗性密碼學中的重要性。

雖然該漏洞為格基密碼方案的安全提供了暫時安心，但也提醒著後量子密碼學領域研究與開發的持續必要。

隨著 NIST 繼續其 PQC 標準化過程，密碼學界必須保持主動和適應能力，擁抱新思想與方法，以確保我們的數字世界在面對不斷進步的量子計算能力時的長期安全。

## 參考資料

- Sebastien Rousseau, (2024). [量子演算法挑戰格基密碼學][00].
- Chen, Y. (2024). [格問題的量子演算法：密碼學的新時代 ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [關於格、Learning With Errors、隨機線性碼與密碼學。⧉][02] 收錄於 Proceedings of the 37th Annual ACM Symposium on Theory of Computing (pp. 84-93).
- Kuperberg, G. (2005). [二面體隱藏子群問題的亞指數時間量子演算法。⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "格基密碼學量子演算法挑戰"
[01]: https://eprint.iacr.org/2024/555.pdf "格問題的量子演算法：密碼學的新時代"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "後量子密碼學標準化"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
