---
title: "קריפטוגרפיה קוונטית מבוססת-סריגים: באג בהתקפת ה-LWE של Chen"
tags: "קריפטוגרפיה פוסט-קוונטית, NIST, אלגוריתמים קוונטיים, קריפטוגרפיה מבוססת-סריגים, בעיית LWE, מחשוב קוונטי, אבטחה קריפטוגרפית, עמידות קוונטית, מחקר קריפטוגרפי, ISO 20022, AI, Rust"
subtitle: "ביקורת עמיתים חושפת פגם בעבודתו פורצת-הדרך של Chen"
description: "באג באלגוריתם ה-LWE הקוונטי של Yilei Chen מעניק ארכה זמנית לקריפטוגרפיה מבוססת-סריגים. מה המשמעות עבור CRYSTALS-Kyber, Dilithium ומפת הדרכים של PQC."
date: "Apr 22, 2024"
language: "he-IL"
locale: "he_IL"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "תמונה שנוצרה באמצעות MidJourney - רשת של צמתים דיגיטליים בגוונים אדומים וכחולים."
keywords: "קריפטוגרפיה פוסט-קוונטית, NIST, תִקנון PQC, Yilei Chen, אלגוריתם קוונטי, קריפטוגרפיה מבוססת-סריגים, בעיית LWE, CRYSTALS-KYBER, CRYSTALS-Dilithium, קריפטוגרפיה עמידה לקוונטים"
---

## קריפטוגרפיה קוונטית מבוססת-סריגים: באג בהתקפת ה-LWE של Chen

## החידה הקוונטית: הערכה מחודשת של תִקנון NIST לקריפטוגרפיה פוסט-קוונטית לאור האלגוריתם של Yilei Chen

בהמשך למאמרי האחרון על [האתגרים באלגוריתמים קוונטיים לקריפטוגרפיה מבוססת-סריגים][00], עליי לספק עדכון על ההתפתחויות האחרונות ב[מחקרו של Yilei Chen ⧉][01].

בתפנית בלתי צפויה, Yilei Chen, פרופסור-חבר במכון למדעי המידע הבין-תחומיים (IIIS) באוניברסיטת Tsinghua, דיווח כי המדענים Hongxun Wu ו-Thomas Vidick גילו באופן עצמאי באג באלגוריתם הקוונטי שלו בזמן פולינומי, שתוכנן לפתור את בעיית Learning with Errors (LWE).

באג זה הופך את האלגוריתם לבלתי שמיש, ו-Chen הודה כי גישתו אינה עומדת במבחן כפי שנטען בתחילה.

## הבאג באלגוריתם הקוונטי של Chen

הבאג נמצא בשלב 9 של האלגוריתם של Chen, והוא הצהיר כי אינו יודע כיצד לתקנו. תגלית זו מהווה הקלה עבור קהילת הקריפטוגרפיה, שכן היא מאששת כי בעיית LWE, רכיב מהותי בשיטות ההגנה של הקריפטוגרפיה הפוסט-קוונטית, נותרת מאובטחת.

מאמרו של Chen בחן גם בעיות סריג מורכבות אחרות, כגון decisional shortest vector problem (GapSVP) ו-shortest independent vector problem (SIVP), במסגרת גורמי קירוב פולינומיים. אף שהבאג באלגוריתם שלו אינו משפיע ישירות על בעיות אלה, הוא מעלה שאלות בדבר החוסן של אלגוריתמים קוונטיים לקריפטוגרפיה מבוססת-סריגים.

אך על פי [עמודו של Nigel Smart ⧉][02], ההתקפה הקוונטית המוצעת על LWE פגומה ואינה מסכנת סכימות קריפטוגרפיה מבוססות-סריגים כגון [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] או [TFHE ⧉][07].

## השלכות על תהליך התִקנון של NIST לקריפטוגרפיה פוסט-קוונטית

מחקרו של Chen עורר בעקיפין חששות וספקות בנוגע ל[תהליך התִקנון של NIST לקריפטוגרפיה פוסט-קוונטית (PQC) ⧉][03] ולבחירת אלגוריתמים קריפטוגרפיים עמידים לקוונטים.

הסכימות [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) ו-CRYSTALS-Dilithium, הנמנות עם המועמדות הסופיות בתהליך התִקנון של NIST PQC, הן דוגמאות לסכימות קריפטוגרפיות מבוססות-סריגים שנבדקו והוערכו בקפדנות לעמידות קוונטית. עם זאת, חיוני להמשיך ולבחון ולשכלל סכימות אלה כדי להבטיח את אבטחתן וכדאיותן לטווח הארוך.

על NIST, קהילת הקריפטוגרפיה והחברות לשמור על ערנות ולהמשיך לחקור יסודות מתמטיים חלופיים לקריפטוגרפיה פוסט-קוונטית, כדי להבטיח קיומה של מערכת אפשרויות יציבה ומגוונת לאבטחה עמידה לקוונטים.

## עתיד הקריפטוגרפיה הפוסט-קוונטית

גילוי הבאג באלגוריתם של Chen מדגיש את התפקיד המהותי של ביקורת עמיתים בתהליך המדעי. הוא גם מבליט את הצורך בביקורת, במשוב ובדיון מיידיים.

העידן הקוונטי החל, והצורך לפתח שיטות קריפטוגרפיות עמידות לקוונטים מחייב צעדים משותפים בקנה מידה עולמי, כדי להבטיח את אבטחת התשתית הדיגיטלית שלנו אל מול יכולות המחשוב הקוונטי המתקדמות והמרוץ לעליונות קוונטית.

תהליך התִקנון של NIST PQC הוא צעד משמעותי בכיוון זה, אך הוא רק ההתחלה. הבאג באלגוריתם של Chen הוא תזכורת חדה לאתגרים ולאי-הוודאות שלפנינו, אך הוא גם משמש קריאה לפעולה לקהילת הקריפטוגרפיה להכפיל את מאמציה ולהרחיב את גבולות האפשר.

זוהי התפתחות מרתקת בתחום הקריפטוגרפיה הפוסט-קוונטית, ויהיה מעניין לראות כיצד יתפתח תהליך התִקנון של NIST PQC בתגובה למידע חדש זה.

## מסקנה

הבאג שהתגלה באלגוריתם הקוונטי של Yilei Chen לפתרון בעיית LWE מדגיש את חשיבותה של ביקורת עמיתים קפדנית ושל שיתוף פעולה בפיתוח קריפטוגרפיה עמידה לקוונטים.

אף שהבאג מספק הקלה זמנית לאבטחתן של סכימות קריפטוגרפיות מבוססות-סריגים, הוא גם משמש תזכורת לצורך המתמשך במחקר ובפיתוח בתחום הקריפטוגרפיה הפוסט-קוונטית.

ככל ש-NIST ממשיך בתהליך התִקנון של PQC, על קהילת הקריפטוגרפיה להישאר יוזמת ומסתגלת, ולאמץ רעיונות וגישות חדשים כדי להבטיח את האבטחה ארוכת-הטווח של עולמנו הדיגיטלי אל מול יכולות המחשוב הקוונטי המתקדמות.

## מקורות

- Sebastien Rousseau, (2024). [Quantum Algorithm Challenges Lattice-Based Cryptography][00].
- Chen, Y. (2024). [Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [On lattices, learning with errors, random linear codes, and cryptography. ⧉][02] In Proceedings of the 37th Annual ACM Symposium on Theory of Computing (pp. 84-93).
- Kuperberg, G. (2005). [A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "Challenges in Quantum Algorithms for Lattice-Based Cryptography"
[01]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "Post-Quantum Cryptography Standardization"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
