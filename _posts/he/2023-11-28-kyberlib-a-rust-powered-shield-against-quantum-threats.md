---
title: "KyberLib: CRYSTALS-Kyber ב-Rust לעידן הפוסט-קוונטי"
tags: "KyberLib, Rust, CRYSTALS-Kyber, קריפטוגרפיה פוסט-קוונטית, lattice-based cryptography, key encapsulation mechanism, NIST, libsignal, cryptography, ISO 20022, מחשוב קוונטי, AI"
subtitle: "KyberLib, מימוש Rust יציב של CRYSTALS-Kyber לעידן הקוונטי."
description: "מימוש קריפטוגרפי יציב ובטוח-קוונטית של אלגוריתם CRYSTALS-Kyber, להגנה על הנתונים שלכם מפני איומים קוונטיים והתקפות קריפטואנליזה."
date: "Nov 28, 2023"
language: "he-IL"
locale: "he_IL"
banner: "https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg"
banner_alt: "העצמת תקשורת מאובטחת בעידן הקוונטי עם KyberLib"
keywords: "KyberLib, Rust CRYSTALS-Kyber, קריפטוגרפיה פוסט-קוונטית, קריפטוגרפיה מבוססת-סריגים, חילופי מפתחות עמידים לקוונטים, NIST FIPS 203, Sebastien Rousseau, KEM, אימות תשלומים, ספריית PQC"
---

## KyberLib: CRYSTALS-Kyber ב-Rust לעידן הפוסט-קוונטי

[![העצמת תקשורת מאובטחת בעידן הקוונטי עם KyberLib](https://cloudcdn.pro/clients/kyberlib/v1/logos/kyberlib.svg).class=\"img-fluid clearfix\"][07]

`KyberLib` היא ספרייה מבוססת-Rust המגנה על הנתונים שלכם מפני האיום הפוטנציאלי של המחשוב הקוונטי. בנויה על **אלגוריתם [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)**, `KyberLib` מספקת אבטחה, יעילות וגמישות יוצאות דופן, ומשתלבת בקלות במגוון פלטפורמות, לרבות סביבות `no-std`.

![divider][divider].class=\"m-10 w-100\"

## אבטחת הנתונים שלכם בעידן הקוונטי

הופעת המחשוב הקוונטי הציבה איום משמעותי על אמצעי האבטחה הקריפטוגרפיים המקובלים. כדי להתמודד עם אתגר זה, תחום הקריפטוגרפיה הבטוחה-קוונטית (QSC) מתפתח במהירות.

בחזית תנועה זו עומד המכון הלאומי לתקנים וטכנולוגיה (NIST), המוביל את תִקנון אלגוריתמי ה-QSC.

בשנת 2023 בחר NIST ארבעה אלגוריתמים חדשניים לרשימה הקצרה:

- [**[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html)** ⧉][01] (מנגנון עטיפת מפתחות)
- [**CRYSTALS-Dilithium** ⧉][02] (חתימות דיגיטליות)
- [**FALCON** ⧉][03] (חתימות דיגיטליות קלות-משקל)
- [**SPHINCS+** ⧉][04] (חתימות דיגיטליות מבוססות-hash)

אלגוריתמים פורצי-דרך אלה מבוססים על עקרונות מתמטיים מגוונים, ובהם קריפטוגרפיה מבוססת-סריגים, קריפטוגרפיה מבוססת-hash וקריפטוגרפיה מבוססת-קודים, במטרה לספק הגנה יציבה מפני התקפות קוונטיות.

## מבט על קריפטוגרפיה מבוססת-סריגים

קריפטוגרפיה מבוססת-סריגים (LBC) מתבססת כמובילה בתחום ה-QSC, ומציעה פתרון מבטיח לקריפטוגרפיה פוסט-קוונטית (PQC). ה-LBC רב-תכליתית, ויישומיה נעים ממנגנוני עטיפת מפתחות (KEMs), דרך חתימות דיגיטליות ועד סכימות הצפנה במפתח ציבורי, כולם מושתתים על סריגים מתמטיים.

סריגים הם מושג יסודי במתמטיקה שמצא יישומים בתחומים רבים, ובהם הקריפטוגרפיה. במילים פשוטות, סריג הוא סידור סדיר של נקודות במרחב, היוצר מבנה דמוי-רשת. הנקודות מחוברות בקווים ויוצרות רשת של תאים קשורים זה בזה. הסידור המדויק של הנקודות והמרווח ביניהן מגדירים את התכונות הייחודיות של הסריג.

### ייצוג תלת-ממדי של סריג באמצעות וקטורי בסיס

גרף זה מציג מבנה סריג תלת-ממדי הנוצר משלושה וקטורי בסיס:

- `b1 = [1, 0, 0]` באדום,
- `b2 = [0, 1, 0]` בירוק, ו-
- `b3 = [0, 0, 1]` בכחול.

כל נקודה בסריג נוצרת מצירוף וקטורי הבסיס הללו ביחסים שלמים שונים, ויוצרת תבנית דמוית-רשת המשתרעת בשלושת הממדים המרחביים. ההמחשה לוכדת את מהות הסריג התלת-ממדי, מושג הנפוץ בפיזיקה ובמתמטיקה לתיאור הסידור הסדיר והחוזר של נקודות במרחב.

![ייצוג תלת-ממדי של סריג באמצעות וקטורי בסיס][06].class=\"img-fluid mx-auto d-block\"

בקריפטוגרפיה, הסריגים משמשים בסיס לאלגוריתמים קריפטוגרפיים מסוימים. הקריפטוגרפיה מבוססת-הסריגים (LBC) מנצלת את התכונות המתמטיות של הסריגים כדי ליצור סכימות קריפטוגרפיות מאובטחות העמידות בפני התקפות של מחשבים קוונטיים. מחשבים קוונטיים מציבים איום משמעותי על הקריפטוגרפיה המקובלת, שכן הם מסוגלים לשבור ביעילות אלגוריתמים המסתמכים על פירוק מספרים גדולים לגורמים או על פתרון בעיות לוגריתם בדיד.

[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) מדגים את יתרונות ה-LBC, ומספק עמידות יציבה מפני התקפות קוונטיות לצד יעילות וגודל מפתח יוצאי דופן. תמיכתו בפלטפורמות מרובות ותאימותו לקריפטוגרפיה הופכות אותו לאפשרות אמינה לאבטחת נתונים בעידן הקוונטי.

המפרטים הנוכחיים של [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) הם כדלקמן:

- **Kyber512**: מספק רמת אבטחה שקולה להצפנת AES של 128 סיביות, ומגן על נתונים רגישים בהגנה בסטנדרט התעשייה.
- **Kyber768**: מספק רמת אבטחה שקולה להצפנת AES של 256 סיביות, ומבטיח את סודיות המידע הרגיש במיוחד.
- **Kyber1024**: מספק רמת אבטחה העולה על הצפנת AES של 256 סיביות, ומציע הגנה יציבה מפני התקפות קוונטיות ושמירה על שלמות הנתונים הרחק אל העתיד.

### השוואת רמות אבטחה בין אלגוריתמים קלאסיים לאלגוריתמים עמידים לקוונטים

תרשים העמודות ממחיש את רמות האבטחה היחסיות של אלגוריתמים קריפטוגרפיים קלאסיים כגון RSA-2048 ואלגוריתם החתימה הדיגיטלית בעקומה אליפטית (ECDSA), בהשוואה למפרטי הווריאנטים העמידים-לקוונטים של אלגוריתם [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) (Kyber512, Kyber768 ו-Kyber1024).

אף שהתרשים מספק השוואה חזותית, חשוב לציין כי רמות האבטחה אינן ניתנות להשוואה ישירה, משום שהן מבוססות על עקרונות מתמטיים שונים.

עם זאת, התרשים אכן מספק נקודת ייחוס מועילה להבנת רמות האבטחה של אלגוריתמים עמידים לקוונטים.

![קריפטוגרפיה מבוססת-סריגים][05].class=\"img-fluid mx-auto d-block\"

![divider][divider].class=\"m-10 w-100\"

## KyberLib: ספריית Rust לקריפטוגרפיה עמידה לקוונטים

KyberLib רותמת את עוצמת [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) כדי לספק בטיחות זיכרון משופרת ואבטחה יציבה ברמת המערכת. היא תומכת במפרטים מרובים של [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) (Kyber512, Kyber768, Kyber1024), ומציעה טווח של רמות אבטחה המתאימות לצרכים הספציפיים שלכם. תאימותה ל-`no_std` הופכת אותה לבחירה אידיאלית למערכות משובצות, בעוד תאימותה ל-WebAssembly (WASM) מאפשרת שילוב חלק בתוך יישומי ווב.

![divider][divider].class=\"m-10 w-100\"

## הגנה על יישומי ווב באמצעות קריפטוגרפיה עמידה לקוונטים

KyberLib, המתוכננת לצריכת זיכרון מזערית, אידיאלית למערכות משובצות ומוגבלות-משאבים ללא פשרה על האבטחה. המימוש שלה מבוסס-Rust מנצל את מאפייני הבטיחות של השפה, ומחזק את האבטחה שמספק אלגוריתם [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html).

נוסף על כך, תאימות KyberLib ל-WebAssembly מגבירה את התועלת שלה ביישומי ווב, ומבטיחה שהיא תישאר כלי חיוני בתחום הקריפטוגרפיה הדינמי.

[התחילו עם KyberLib עכשיו! ⧉][00] קלה להתקנה, חינמית לשימוש אישי ומסחרי כאחד, KyberLib היא הפתרון המועדף שלכם לקריפטוגרפיה עמידה לקוונטים.

[00]: https://kyberlib.com/getting-started/index.html "Getting Started"
[01]: https://pq-crystals.org/kyber/ "Kyber: A CCA-secure module-lattice-based KEM"
[02]: https://pq-crystals.org/dilithium/ "Dilithium: A CCA-secure lattice-based signature scheme"
[03]: https://falcon-sign.info/ "FALCON: A post-quantum signature scheme"
[04]: https://sphincs.org/ "SPHINCS+: A stateless hash-based signature scheme"
[05]: https://cloudcdn.pro/stocks/diagrams/kyber-vs-classical.svg "Comparison of Security Levels between Classical and Quantum-Resistant Algorithms"
[06]: https://cloudcdn.pro/stocks/diagrams/3D-lattice-graph.svg "3D Lattice Representation with Basis Vectors"
[07]: https://kyberlib.com/ "Privacy and Security in a Quantum World"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
