---
title: "תשואת סטייבלקוין בשם אחר: פענוח בקשות הרישום BRSRV ו-BSTBL של BlackRock"
tags: "BlackRock, BRSRV, BSTBL, BUIDL, GENIUS Act, OCC, סטייבלקוינים, קרן כספית מבוססת-אסימונים, Securitize, BNY Mellon, ERC-20, Ethereum, תשלומים, רגולציה, ISO 20022, קריפטוגרפיה פוסט-קוונטית, AI, פיקדונות מבוססי-אסימונים, תשלומים חוצי גבולות"
subtitle: "סטייבלקוינים אינם יכולים לשלם תשואה תחת GENIUS Act. ב-8 במאי 2026 הגישה BlackRock שני מוצרים שאינם, מבחינה משפטית, סטייבלקוינים, ומסוגלים לשלם תשואה, בארנק, על בלוקצ׳יין ציבורי."
description: "סטייבלקוינים אינם יכולים לשלם תשואה תחת GENIUS Act. ב-8 במאי 2026 הגישה BlackRock שתי בקשות רישום ל-SEC עבור מוצרים שפותרים מגבלה זו בכך שהם מפוקחים כקרנות כספיות ולא כסטייבלקוינים, ובה בעת מתנהגים, בארנק, כדולרים נושאי תשואה. קריאה מדוקדקת של BRSRV, BSTBL והתקינה של OCC שאליה הם מגיבים."
date: "May 15, 2026"
language: "he-IL"
locale: "he_IL"
banner: "https://cloudcdn.pro/stocks/images/alev-takil-7ojyp-IXW7w-unsplash.webp"
banner_alt: "תרשים ארכיטקטורה של קרן כספית מבוססת-אסימונים של BlackRock: OnChain Shares של BRSRV ומחלקת מניות ERC-20 של BSTBL עם זרימות רזרבה תחת GENIUS Act"
keywords: "BlackRock, BRSRV, BSTBL, BUIDL, GENIUS Act, OCC, סטייבלקוין, קרן כספית מבוססת-אסימונים, OnChain Shares, Securitize"
---

## תשואת סטייבלקוין בשם אחר: פענוח בקשות הרישום BRSRV ו-BSTBL של BlackRock

סטייבלקוינים אינם יכולים לשלם תשואה תחת GENIUS Act. ב-8 במאי 2026 הגישה BlackRock שתי בקשות רישום ל-SEC עבור מוצרים שפותרים מגבלה זו בכך שהם מפוקחים כקרנות כספיות ולא כסטייבלקוינים, ובה בעת מתנהגים, בארנק, כדולרים נושאי תשואה על בלוקצ׳יין ציבורי.

---

> **עיקרי המסקנות**
>
> - **GENIUS Act**, שנחתם ביולי 2025 ונמצא כעת בחודשים האחרונים של גיבוש התקינה שלו, אוסר על מנפיקי payment stablecoins לשלם ריבית או תשואה למחזיקים אך ורק בעבור החזקה, שימוש או שמירה של סטייבלקוין. הצעת OCC ממרץ 2026 הידקה זאת עוד יותר עם חזקה הניתנת לסתירה שגם הסדרי תשואה דרך חברות קשורות וצדדים שלישיים מפרים את האיסור.
> - הבעיה הכלכלית שנוצרת פשוטה. עם כ-**281 מיליארד דולר של payment stablecoins במחזור** ותשואות Treasury בשיא של שנים רבות, הפער בין מה שמחזיק ארנק מקבל (אפס) לבין מה שמרוויחות הרזרבות הבסיסיות (כ-4-5%) מגיע כעת לעשרות מיליארדי דולרים בשנה.
> - ב-**8 במאי 2026 הגישה BlackRock שתי הצהרות רישום ל-SEC** התופסות פער זה מבלי להפר את איסור התשואה, מפני שאף אחד מהמוצרים אינו, מבחינה משפטית, סטייבלקוין.
> - **BRSRV** (BlackRock Daily Reinvestment Stablecoin Reserve Vehicle) היא קרן כספית חדשה המחזיקה מזומן, Treasuries לפחות מ-93 יום, ו-overnight Treasury repos. היא מנפיקה "OnChain Shares" דרך מסגרת רב-שרשראתית מורשית, כאשר Securitize Transfer Agent LLC משמשת כרשומת הבעלות המשפטית. השקעת מינימום: 3 מיליון דולר. היא מהונדסת כדי להיחשב נכס רזרבה כשיר תחת GENIUS Act.
> - **BSTBL** היא הבקשה המשמעותית יותר מבחינה ארכיטקטונית. היא מחברת מחלקת מניות ERC-20 אל **Select Treasury Based Liquidity Fund הקיימת של BlackRock בהיקף 6-7 מיליארד דולר**, כאשר BNY Mellon Investment Servicing משמשת כסוכן העברה הרושם בעלי מניות על Ethereum. זו הפעם הראשונה שמחלקת מניות על Ethereum ציבורי נוספת למוצר כספי קיים של BlackRock.
> - התבנית גלויה כעת ברחבי הענף. **קרנות כספיות מבוססות-אסימונים הן הארכיטקטורה ש-GENIUS Act, באוסרו תשואה על סטייבלקוינים, הפך לבלתי נמנעת.** שוק ה-Treasury מבוסס-האסימונים בהיקף 14 מיליארד דולר, שבראשו BUIDL של BlackRock בנתח של כ-40%, הוא הקריאה המוקדמת של המקום שבו יושב הגל הבא של "דולרי הארנק".

---

## בקשה שהיא גם עמדת מדיניות

שתי הבקשות של BlackRock מ-8 במאי 2026 לא הגיעו בחלל ריק. הן הגיעו שבוע לאחר ש-BlackRock הגישה [מכתב הערות בן שבעה-עשר עמודים ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea, expand eligible assets in GENIUS Act comment letter") אל Office of the Comptroller of the Currency ביום האחרון של חלון ההערות לכללי היישום של GENIUS Act, וארבעה ימים לאחר ש-[BlackRock פרסמה תקציר ציבורי ב-X ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/ "BlackRock Backs OCC Stablecoin Rules Under GENIUS Act") של שבע המלצותיה המרכזיות לרשות.

את ההמלצות ואת הבקשות החדשות מוטב לקרוא כמסמך אחד בשני חלקים. מכתב ההערות טען ש-OCC צריכה לבטל את מגבלת 20% המוצעת שלה על נכסי רזרבה מבוססי-אסימונים, לאשר ש-ETFs כשירים מקבלים אותו טיפול כמו קרנות כספיות ממשלתיות, ולאפשר ל-GMMFs עם סליקה באותו יום להיספר לעבר רצפת הנזילות השבועית. הבקשות, ארבעה ימים לאחר מכן, רשמו בדיוק את המכשירים הנהנים מעמדות אלה: קרן חדשה (BRSRV) המהונדסת במפורש כדי להיחשב רזרבה כשירה תחת GENIUS Act, ומחלקת מניות מבוססת-אסימונים (BSTBL) מעל קרן נזילות ה-Treasury הקיימת של החברה בהיקף 6-7 מיליארד דולר. בין אם OCC תאמץ את עמדות BlackRock בכלל הסופי ובין אם לאו, החברה מיקמה כעת את מוצריה בדיון המדיניות ברמת פירוט שקשה לרגולטור להתעלם ממנה.

זהו הרקע האסטרטגי למה שנראה, בקריאה ראשונה, כמו פיסת הנדסה משפטית מתוחכמת. מדויק יותר לקרוא זאת כמנהל הנכסים הגדול בעולם המכריז היכן צריך לשבת הקו בין "סטייבלקוין" ל"נייר ערך מבוסס-אסימונים" בחוק האמריקני, ורושם את המוצרים שיחיו משני צדי הקו הזה.

## מדוע סטייבלקוינים אינם יכולים לשלם תשואה

GENIUS Act, שנחתם ביולי 2025 וכעת מהווה בסיס לתקינות חופפות של OCC, FDIC ו-Federal Reserve, משרטט הבחנה מושגית נקייה באופן חריג. "payment stablecoin" תחת החוק הוא נכס דיגיטלי המתוכנן לשמור על ערך יציב ביחס למטבע פיאט, מגובה ברזרבות איכותיות, בר-פדיון בערך נקוב. "permitted payment stablecoin issuer" (PPSI) הוא ישות בעלת רישיון פדרלי או מדינתי המורשית להנפיק אסימון כזה. ו[סעיף 4(a)(11) של החוק ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act "OCC Issues Proposal to Implement the GENIUS Act") אוסר על כל PPSI לשלם ריבית או תשואה למחזיקים אך ורק בעבור החזקה, שימוש או שמירה של הסטייבלקוין.

[הכלל המוצע ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act "Proposed OCC regulations for payment stablecoins under the GENIUS Act") של OCC ממרץ 2026 הרחיב איסור זה מבחינה תפעולית. הוא ביסס חזקה הניתנת לסתירה שהסדרים המנתבים תשואה דרך חברה קשורה או צד שלישי קשור, למשל בורסת קריפטו המשלמת "תגמולי נאמנות" למחזיקי סטייבלקוין מסוים, מפרים אף הם את האיסור, כאשר נטל ההוכחה מוטל על המנפיק להראות אחרת. הסדרי white-label, שבהם PPSI מנפיק נכסים דיגיטליים הנושאים מותג של שותף המשלם לאחר מכן תשואה, נחשבים במפורש למתחמקים בחזקה. Office of the Comptroller [רמז בתחילת 2026 ⧉](https://www.compliancecorylated.com/news/us-occ-closes-genius-act-loophole-allowing-yield-bearing-stablecoins/ "US OCC closes GENIUS Act loophole allowing yield-bearing stablecoins") שמסגור ה"פרצה" של מודל המנפיק-משלם-דרך-חברה-קשורה לא ישרוד את גיבוש הכללים הסופי בשום צורה מתירנית.

ההיגיון הכלכלי מאחורי איסור זה שנוי במחלוקת. הגשות מצד ענף הבנקאות אל OCC טענו בעד האיסור המחמיר על בסיס שסטייבלקוינים נושאי תשואה ירוקנו פיקדונות בנקאיים עסקאתיים, שוק שהוערך על ידי [המועצה המייעצת של US Treasury בכ-6.6 טריליון דולר ⧉](https://www.congress.gov/crs-product/IF13174 "The Stablecoin Yield Debate — Congressional Research Service"), שממנו נתח משמעותי "בסיכון" מתחרות עם תחליפי דולר נושאי תשואה. הגשות מצד ענף הקריפטו, בהובלת Coinbase, טענו את ההפך: שתמריצים הם מרכזיים לתחרות בתשלומים, ושאיסור רחב יטיל עלויות רווחה נטו מבלי להשפיע מהותית על ההלוואות הבנקאיות.

לאיזה צד שלא תהיה הטענה המדיניותית הטובה יותר, התוצאה המשפטית לעת עתה מיושבת: סטייבלקוין במובן הרגולטורי של GENIUS Act אינו יכול לשלם למחזיקו תשואה. אך מה שאין ביכולתו לעשות הוא להגדיר מה יכול מחזיק לעשות עם כספו בהמשך. וכאן הארכיטקטורה מתפצלת.

## הארכיטקטורה של BRSRV

BlackRock Daily Reinvestment Stablecoin Reserve Vehicle היא, מבחינת האינסטלציה שלה, קרן כספית בלתי מרשימה. היא מחזיקה מזומן, ניירות ערך של US Treasury במועדי פירעון של 93 יום או פחות, והסכמי רכש חוזר overnight מגובים ב-Treasuries. היא מיושרת עם Rule 2a-7 תחת Investment Company Act of 1940, אותה ארכיטקטורה רגולטורית שמשלה בקרנות כספיות מוסדיות ארבעה עשורים. תשואתה, כמו כל MMF ממשלתי אחר, נגזרת משיעור ה-Treasury קצר-הטווח השורר.

מה שחדשני הוא מחלקת המניות. מניות BRSRV מונפקות כ-["OnChain Shares" דרך מסגרת מורשית ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/ "BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital") המתחברת לבלוקצ׳יינים ציבוריים מרובים, כאשר [Securitize Transfer Agent LLC משמשת כסוכן ההעברה הרשמי ⧉](https://www.crowdfundinsider.com/2026/05/278346-blackrock-focuses-on-tokenization-initiatives-with-blockchain-enabled-funds/ "BlackRock Focuses On Tokenization Initiatives With Blockchain Enabled Funds"). מערכות זהות off-chain, אותו סוג של תשתית KYC המגבה את [קרן BUIDL ⧉](https://stablecoininsider.org/top-10-tokenized-treasury-funds-in-2026-buidl-benji-and-the-highest-yielding-on-chain-options/ "Top 10 Tokenized Treasury Funds in 2026") הקיימת של BlackRock בהיקף 2.9 מיליארד דולר, מקשרות כתובות ארנק למשקיעים מאומתים. השקעת מינימום: 3 מיליון דולר. הבקשה אינה נוקבת עדיין באילו בלוקצ׳יינים הקרן תתמוך בהשקה.

המוצר מהונדס במפורש, [כפי שמקורות רבים ציינו ⧉](https://cryptobriefing.com/blackrock-tokenized-money-market-funds-stablecoins/ "BlackRock doubles down on tokenization with new stablecoin reserve funds"), כדי להיחשב נכס רזרבה כשיר תחת GENIUS Act. הקונה המיועד אינו משתמש ארנק קמעונאי. זהו מנפיק סטייבלקוין (או מערך אוצר המחזיק סטייבלקוינים כחלק מאסטרטגיית הון חוזר) הזקוק למכשיר נושא תשואת Treasury שיוכל להחזיק באופן תוכנתי על אותן מסילות בלוקצ׳יין כמו הסטייבלקוינים עצמם. המסר, מפושט למשפט אחד, הוא: החזק את הרזרבות שלך on-chain, הרווח את תשואת ה-Treasury, ספק את הרגולטור.

עבור BlackRock, העמדה האסטרטגית חדה יותר משהיא נראית. קרן BUIDL הקיימת שלה כבר מגבה יותר מ-90% מהרזרבות של שניים מהמוצרים "נושאי התשואה" הצמודים לסטייבלקוין הגדולים ביותר: USDtb של Ethena ו-JupUSD של Jupiter מבוסס-Solana. BRSRV היא ההרחבה הייעודית והמודעת ל-GENIUS של תפקיד זה: מוצר תשואת ה-Treasury הסיטונאי הבנוי במיוחד לזרימת עבודת ניהול הרזרבה של כל PPSI שיתקיים תחת המשטר החדש.

## הארכיטקטורה של BSTBL

הבקשה השנייה מעניינת יותר מבחינה תפעולית וחשובה יותר מבחינה ארכיטקטונית. BSTBL, מחלקת המניות on-chain של Select Treasury Based Liquidity Fund הקיימת של BlackRock, אינה קרן חדשה. זו מחלקת מניות חדשה הממוקמת מעל מוצר כספי המנהל כבר כ-6-7 מיליארד דולר בנכסים, [עבר כיול מחדש באוקטובר 2025 ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea") לתצורה תואמת GENIUS עם מועד מסחר אחרון בשעה 5 אחר הצהריים ET ומנדט כבד ב-Treasury, ומורחב כעת אל Ethereum כאסימון ERC-20.

סוכן ההעברה עבור מחלקת מניות זו הוא [BNY Mellon Investment Servicing ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"), שישמור על רשומות בעלי המניות הרשמיות על Ethereum באמצעות תקן ERC-20. תשתית KYC off-chain מקשרת ארנקים לרשומות זהות המשקיע, כפי שהיא עושה עבור BUIDL ועבור כל קרן מבוססת-אסימונים תואמת אחרת בשוק כיום. ההבחנה המהותית מ-BRSRV היא השרשרת (Ethereum, ציבורי, עם אסימון ERC-20 כייצוג המניה) וסוכן ההעברה (BNY במקום Securitize), והעובדה שזו הפעם הראשונה שמחלקת מניות על Ethereum ציבורי חוברה לקרן כספית קיימת של BlackRock.

אותה תפאורה אחרונה היא זו שראוי להתעכב עליה. המוצרים מבוססי-האסימונים הקודמים של BlackRock, ובראשם BUIDL, נבנו כקרנות חדשות עם ארכיטקטורה on-chain מקורית. BSTBL נוקטת גישה שונה, וניתן לטעון בעלת השלכות רבות יותר: להפוך מוצר כספי קיים, גדול ומסורתי למבוסס-אסימונים על ידי הוספת מחלקת מניות חדשה, במקום לבנות מבנה מקביל. המשמעות היא שכל MMF קיים של BlackRock יכול, עקרונית, לעקוב אחר אותה תבנית. וכך גם כל MMF מתחרה קיים, של Vanguard, של Fidelity, של JPMorgan, של State Street. המחסום הארכיטקטוני להפיכת ענף הקרנות הכספיות המסורתי למבוסס-אסימונים נמוך, לאחר BSTBL, מכפי שהיה אי פעם.

להקשר ענפי: US Treasuries מבוססי-אסימונים צמחו מכ-2 מיליארד דולר אל [14 מיליארד דולר נכון למאי 2026 ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"), כאשר BUIDL של BlackRock מחזיק בכ-40% נתח שוק, BENJI/FOBXX של Franklin Templeton ב-850 מיליון דולר, ומוצרי OUSG ו-USDY המשולבים של Ondo Finance במקום השני. 50-100 מיליארד הדולר הבאים כבר נמצאים ככל הנראה בתנועה דרך בקשות כמו BSTBL.

## Payment Stablecoin מול קרן כספית מבוססת-אסימונים: ההבחנה שחשובה

עבור קורא שאינו מומחה, ההבחנה בין "סטייבלקוין" ל"מניית קרן כספית מבוססת-אסימונים" יכולה להיראות כטכניקה רגולטורית. אין זה כך. שני המכשירים תופסים עמדות שונות באמת בחוק ניירות הערך האמריקני וההשלכות זורמות דרך כל תכנון המוצר.

| ממד | Payment Stablecoin (תחת GENIUS Act) | מניית MMF מבוססת-אסימונים (תבנית BRSRV / BSTBL) |
|---|---|---|
| מעמד משפטי | מכשיר תשלום | נייר ערך (מניית קרן) |
| משטר שולט | GENIUS Act; תקינות OCC/FDIC/Fed | Investment Company Act 1940; Rule 2a-7 |
| מנפיק | Permitted Payment Stablecoin Issuer (PPSI) | קרן רשומה ב-SEC (וסוכן העברה) |
| דרישות רזרבה | מזומן, Treasuries קצרים, repos, מחמירות | מזומן, Treasuries קצרים, repos, לפי Rule 2a-7 |
| יכולת לשלם תשואה למחזיק | **לא** (סעיף 4(a)(11)) | **כן** (התשואה היא התשואה על המניה) |
| פדיון | בערך נקוב, על פי דרישה | לפי NAV, בדרך כלל T+0 או T+1 |
| רשומת בעלות | ארנק המנפיק / on-chain | סוכן העברה (משפטי); בלוקצ׳יין (תפעולי) |
| השקעת מינימום | אין (קמעונאי טיפוסי) | משמעותית (3 מיליון דולר ל-BRSRV; מוסדי ל-BSTBL) |
| יכולת הרכבה עם DeFi | גבוהה | גבוהה (BUIDL הוא תקדים) |
| חוויית משתמש בארנק | אסימון המחזיק דולר אחד | אסימון שערכו נצבר לעבר תשואה |
| סיכון תחליף פיקדון בנקאי | הדאגה הרגולטורית המרכזית | נמוך מהותית (נייר ערך, לא דמוי-פיקדון) |

*מקור: סינתזה של נוסח GENIUS Act, OCC March 2026 NPRM, בקשות BlackRock מ-8 במאי 2026, ומסגרת Rule 2a-7.*

השורה התחתונה היא זו שמסבירה את הארכיטקטורה הרגולטורית. payment stablecoin שמשלם תשואה נראה, לרגולטור בנקאי, כתחליף פיקדון. מניית קרן כספית מבוססת-אסימונים שמשלמת תשואה נראית כנייר ערך, וניירות ערך המתחרים בפיקדונות אינם דאגה חדשה, מפני שקרנות כספיות מסורתיות עשו בדיוק זאת במשך ארבעים שנה. GENIUS Act משרטט את קו הגבול שלו בדאגת תחליף-הפיקדון. כל מה שיושב בבירור בצד נייר-הערך של הקו הזה נמצא, מעצם הבנייתו, מחוץ לאיסור התשואה של החוק.

## האם זו פרצה?

זה מפתה, והמסגור צף באופן נרחב ב-LinkedIn וב-crypto-Twitter מאז הבקשה, לכנות זאת "פרצה" ב-GENIUS Act: סטייבלקוינים אינם יכולים לשלם תשואה, ולכן BlackRock הגישה משהו שמבחינה משפטית אינו סטייבלקוין. המסגור לוכד את הכותרת בחוכמה. כאִפיון משפטי הוא ממעיט בערך המהות.

איסור התשואה ב-GENIUS Act היה בחירת מדיניות ספציפית עם יעד ספציפי: סיכון תחליף-הפיקדון לסקטור הבנקאי מסוג מכשיר המתוכנן לתפקד ככסף. קרנות כספיות מבוססות-אסימונים אינן מתוכננות לתפקד ככסף; הן מתוכננות לתפקד כמניות קרן, על כל המשקל הרגולטורי (Rule 2a-7, רזרבות מבוקרות, גילוי NAV, רשומות בעלות משפטיות של סוכן העברה) שחל על אותה קטגוריה במשך עשורים. העובדה שמניות קרן אלה מסתלקות כעת במקרה על Ethereum או על שרשרת ציבורית אחרת אינה משנה את מה שהן בחוק ניירות הערך. [הכלל המוצע ⧉](https://www.morganlewis.com/pubs/2026/04/occs-genius-act-proposal-what-prospective-issuers-need-to-know "Stablecoin Regulation: OCC Proposal Under the GENIUS Act") של OCC עצמה שוקל במפורש רזרבות מבוססות-אסימונים כקטגוריה לגיטימית; הדיון הפתוח הוא מגבלת ה-20%, לא קיומה של מחלקת הנכסים.

מה שחדשני באמת הוא חוויית המשתמש. מחזיק של מניית MMF מבוססת-אסימונים, בארנק על שרשרת ציבורית, מחזיק במשהו ש*נראה* כמו סטייבלקוין (אסימון בר-החלפה, ניתן להעברה עמית-לעמית, בר-הרכבה עם תשתית DeFi) אך *מתנהג* כנייר ערך (ה-NAV נצבר, המחזיק ברשימת KYC, רשומות סוכן ההעברה הן השולטות משפטית). מסגור הכותרת, "מבחינה משפטית אינו סטייבלקוין", נכון עד כמה שהוא מגיע. התובנה העמוקה יותר היא ש-GENIUS Act, באוסרו תשואה על קטגוריית payment stablecoin, *חייב* למעשה את הענף להתכנס אל MMFs מבוססי-אסימונים כנושא לדולרים on-chain נושאי תשואה. החוק שרטט קו; הענף, באופן צפוי, בנה מוצרים היושבים בצד המועדף יותר שלו. זו אינה פרצה. זהו תכנון הארכיטקטורה הרגולטורית שעובד פחות או יותר כמתוכנן, גם אם המהירות שבה הוא מייצר מוצרים מוסדיים גבוהה משציפו רוב המשתתפים.

## מה משמעות הדבר לפי סקטור

ההשלכות של בקשות 8 במאי אינן אחידות. התגובה האסטרטגית משתנה מהותית בהתאם למקום שבו יושב מוסד בשרשרת הערך.

### מנפיקי Stablecoins (PPSIs)

עבור Circle, Tether, PayPal והדור הבא של payment stablecoins המונפקים על ידי בנקים, BRSRV היא התשובה התפעולית לשאלה שהיו לה עד כה רק תשובות אד-הוק: היכן יושבות הרזרבות כשהן צריכות להיות גם נושאות תשואת Treasury וגם באופן מקורי על אותה שרשרת כמו הסטייבלקוין המונפק? החזקה ישירה של T-bills עובדת בקנה מידה של הנפקה אך כבדה תפעולית. החזקת BUIDL עובדת, אך מבנה BUIDL לא תוכנן במיוחד סביב מסגרת הרזרבה של GENIUS Act. BRSRV כן. התוצאה התחרותית היא ש-Circle, Tether ו-PPSIs המונפקים על ידי בנקים מחזיקים כעת במוצר סיטונאי אמין ומהונדס-GENIUS לחיבור אל ניהול הרזרבה שלהם, והעלות השולית של העברת רזרבות אל מוצר של BlackRock נמוכה, מבנית, מכפי שהייתה אי פעם.

### בנקים ומפעילי קרנות כספיות

עבור בנקים המפעילים זכיינות קרנות כספיות גדולות, JPMorgan, State Street, BNY Mellon, Northern Trust, Vanguard, Fidelity, BSTBL היא התבנית התפעולית למה שמוצריהם שלהם ככל הנראה יידרשו לעשות. התבנית הארכיטקטונית גלויה כעת: קח MMF קיים, רשום מחלקת מניות on-chain חדשה ב-SEC, מנה סוכן העברה לשמירת רשומות בעלי המניות על Ethereum (או שרשרת ציבורית מרכזית אחרת), וגדר את הגישה דרך KYC off-chain. מחסום הכניסה למחלקת מניות מבוססת-אסימונים על MMF קיים בהיקף 10-50 מיליארד דולר הוא, בתבנית BSTBL, בעיקר רגולטורי ותפעולי ולא טכני. תפקידה של BNY Mellon כסוכן ההעברה של BSTBL, הרושם בעלי מניות על Ethereum באמצעות ERC-20, הוא כשלעצמו אות לכך שתשתית סוכני ההעברה המסורתית מורחבת אל שרשראות ציבוריות בדיוק על ידי המוסדות שניהלו את הרשומה המשפטית של בעלות הקרן במשך עשורים.

### פרוטוקולי DeFi ואוצר on-chain

עבור פרוטוקולי DeFi, BRSRV ו-BSTBL מרחיבים תבנית ש-BUIDL החל: הגירת בטוחות Treasury איכותיות מחשבונות משמורת off-chain אל מכשירים on-chain שניתן להרכיב עם הלוואות, נגזרים ומוצרים מובנים. USDtb של Ethena ו-JupUSD של Jupiter הם הדוגמאות המקדימות; מרחב התכנון שמאחוריהם גדול כעת באופן ניכר. שיקול הסיכון, והוא אינו זניח, הוא שהמכשירים הבסיסיים מגודרים ב-KYC ומורשים, מה שמגביל את מידת ההרכבה "נטולת-ההרשאה" שמערכות מקוריות ל-DeFi יכולות להסתמך עליה. תבניות האינטגרציה שיצוצו בשנים-עשר החודשים הבאים יקבעו באיזו נקיות MMFs מבוססי-אסימונים יהפכו לשכבת בטוחות ראשית של הכלכלה ה-on-chain.

### רגולטורים

עבור OCC, FDIC ו-Federal Reserve, בקשות 8 במאי מבהירות מה מתבקש המתחם הרגולטורי להכיל. איסור התשואה ב-GENIUS Act לא עצר בבירור תשואת on-chain מלהגיע למחזיקי ארנקים; הוא היגר את הארכיטקטורה למסירת אותה תשואה מקטגוריית payment stablecoin (שהרגולטורים מפקחים עליה ישירות) אל קטגוריית הקרן הרשומה (שעליה מפקחת SEC). אין זו בהכרח תוצאה רעה, קרנות רשומות הן קטגוריה רגולטורית מובנת היטב, אך משמעות הדבר היא ששאלת התיאום הבין-רשותי הופכת חדה יותר מבחינה תפעולית. הכלל הסופי של OCC, הצפוי עד ינואר 2027, יקבע האם מגבלת 20% על רזרבות מבוססות-אסימונים תשרוד בצורה כלשהי, והאם הקו בין "payment stablecoin" ל"מניית MMF מבוססת-אסימונים" יישמר ברמת המנפיק או יורשה להיטשטש עוד ברמת הארנק.

## סיכום

בקשות 8 במאי 2026 אינן, כשלעצמן, שינוי פרדיגמה. הן מוצרים בודדים ממנהל נכסים יחיד, שהוגשו בחלון הרגולטורי הספציפי שפתחה תקינת OCC. אך מה שהן תופסות הוא צורתו של מעבר ברמת הענף שהיה גלוי מאז ש-BlackRock השיקה את BUIDL במרץ 2024, ואשר GENIUS Act האיץ כעת ולא ריסן.

סטייבלקוינים, במובן GENIUS Act, ימשיכו לעשות את מה שסטייבלקוינים תמיד היו טובים בו: סליקה יעילה, תשלום חוצה-גבולות כמעט-מיידי, כסף בר-תכנות למקרי שימוש הזקוקים ליחידת חשבון יציבה. הם לא ישלמו, תחת הכללים הנוכחיים והמוצעים, תשואה למחזיקיהם. הדולר נושא-התשואה בארנק, המוצר שלובש את אותה צורת מבנה כמו סטייבלקוין אך צובר תשואת Treasury למחזיקו, יהיה מניית קרן כספית מבוססת-אסימונים, המונפקת על ידי קרן רשומה, עם סוכן העברה (Securitize, BNY Mellon, וככל הנראה כמה אחרים) כרשומת הבעלות המשפטית. BRSRV ו-BSTBL הם הביטויים המוסדיים המוקדמים של אותה תבנית. הם לא יהיו האחרונים.

להקשר קודם באתר זה, ה[מאמר מינואר 2018 על מחסנית הטכנולוגיה של Ethereum ⧉](https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html "Understanding the Technology behind Blockchain") סקר את המצע שעליו יושבת כעת BSTBL, ה[מאמר מינואר 2018 על תקן ERC-20 ⧉](https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html "ERC-20: The Ethereum Token Interface That Changed the World") סקר את ייצוג מחלקת המניות ש-BlackRock בחרה, ה[ניתוח מפברואר 2018 של מטבעות קריפטו לתשלום מהיר יותר ⧉](https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html "Unveiling a New Cryptocurrency and Faster Payment Solution") סקר את בעיית חוויית המשתמש שמכשירים on-chain נושאי תשואה פותרים כעת בחלקה, וה[מאמר האחרון על מועד היעד של כתובת מובנית ב-SWIFT CBPR+](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html "The November 2026 pacs.008 Structured-Address Deadline") יושב סמוך בשיחת מודרניזציית התשלומים הרחבה יותר שבקשות BlackRock הן גם חלק ממנה. הנקודה בשילוב-משולש של אלה אינה לטעון שארכיטקטורה יחידה כלשהי ניצחה. היא שהמערכות הפיננסיות המוסדיות וה-on-chain, ב-2026, מתכנסות על פרימיטיבים משותפים מהר יותר משכל אחת מהן צפתה אפילו לפני שנה.

## שאלות נפוצות

**מהו ההבדל בפועל בין BRSRV/BSTBL לבין סטייבלקוין כמו USDC?**

בארנק, ההבדל בלתי נראה ברובו. כל אחד מהם אסימון בר-החלפה על בלוקצ׳יין ציבורי, בר-פדיון לדולרים (או לערך מניית הקרן הבסיסי), בר-הרכבה עם DeFi. בחוק, ההבדל מהותי. USDC הוא payment stablecoin תחת GENIUS Act, המונפק על ידי Permitted Payment Stablecoin Issuer, אסור עליו לשלם תשואה למחזיקים. BRSRV ו-BSTBL הם מחלקות מניות של קרנות כספיות רשומות תחת Investment Company Act of 1940, מפוקחות תחת Rule 2a-7, שבהן התשואה היא התשואה הטבעית על המניה. מחזיק של BRSRV הוא, מבחינה משפטית, בעל מניה בקרן. מחזיק של USDC הוא, מבחינה משפטית, מחזיק של מכשיר תשלום.

**מדוע BSTBL שונה מ-BUIDL אם שניהם קרנות BlackRock מבוססות-אסימונים על Ethereum?**

BUIDL, שהושק במרץ 2024, נבנה כקרן חדשה עם ארכיטקטורה on-chain מלכתחילה, עם Securitize כשותף והתכנון מקורי לזרימת עבודת הנכסים הדיגיטליים. BSTBL, לעומת זאת, היא מחלקת מניות on-chain חדשה שנוספה לקרן כספית מסורתית קיימת בהיקף 6-7 מיליארד דולר, Select Treasury Based Liquidity Fund. BNY Mellon משמשת כסוכן ההעברה. המשמעות הארכיטקטונית היא ש-BSTBL מדגימה כיצד להביא מוצר כספי גדול, מסורתי וקיים אל on-chain מבלי לבנותו מחדש כקרן חדשה. תבנית זו, אם היא עובדת, ניתנת להעברה לכל MMF מסורתי בענף.

**מדוע מגבלת 20% של OCC על רזרבות מבוססות-אסימונים שנויה במחלוקת?**

הצעת OCC ממרץ 2026 העלתה מגבלה אפשרית של 20% על כמה מרזרבות מנפיק סטייבלקוין ניתן להחזיק בצורה מבוססת-אסימונים. מכתב ההערות של BlackRock טען שזה יהיה "חיצוני" למטרות הפיקוח של OCC, מפני שפרופיל הסיכון של נכס רזרבה מונע מאיכות אשראי, משך זמן ונזילות, לא מהשאלה האם הוא מוחזק או מועבר על פנקס מבוזר. מבחינה תפעולית, המגבלה תרסן את תפקיד BUIDL כגיבוי הרזרבה הראשי של מוצרים כמו USDtb של Ethena ו-JupUSD של Jupiter, ששניהם מסתמכים כיום על BUIDL עבור יותר מ-90% מהרזרבות שלהם. הכלל הסופי של OCC, הצפוי עד ינואר 2027, יקבע האם המגבלה תשרוד, תועלה או תבוטל.

**מה המשמעות של כך שבקשת BRSRV אינה נוקבת בבלוקצ׳יינים שבהם תתמוך?**

זו תכונה שגרתית של בקשות SEC בשלב מוקדם ולא עמימות אסטרטגית. הבקשה מבססת את המבנה המשפטי (קרן רשומה המנפיקה OnChain Shares דרך מסגרת מורשית עם Securitize כסוכן העברה) מבלי להתחייב לשרשראות ספציפיות, שעליהן BlackRock ככל הנראה תכריז קרוב יותר להשקה. BUIDL עצמו הושק על Ethereum והורחב לאחר מכן ל-Polygon, Avalanche, Optimism, Aptos ו-Arbitrum; BRSRV סביר ביותר שיעקוב אחר תבנית רב-שרשראתית דומה בהינתן ההתייחסות המפורשת ל"בלוקצ׳יינים ציבוריים מרובים" בבקשה.

**האם זה סוף הסטייבלקוינים נושאי התשואה כקטגוריית מוצר?**

זהו סוף ה-payment stablecoins נושאי התשואה כקטגוריה, לפחות תחת החוק הפדרלי האמריקני, אלא אם כן Congress יתקן את GENIUS Act. זהו אינו סוף הדולרים on-chain נושאי התשואה כקטגוריית מוצר, וזה מה שמשתמשים באמת רוצים. קטגוריה זו מהגרת כעת אל מניות קרן כספית מבוססות-אסימונים, BUIDL, BENJI, BRSRV, BSTBL, מוצרי Ondo, וגל ה-MMFs מבוססי-האסימונים המתחרים שתבנית BSTBL סבירה שתזרז. המכשירים ייראו שונים מעט בארנק (ערך האסימון ישקף תשואה מצטברת במקום להחזיק 1.00 דולר קבוע), אך הפונקציה הכלכלית, חשיפה שוות-דולר עם תשואת Treasury, מסתלקת על שרשרת ציבורית, נשמרת דרך מסלול רגולטורי שונה.

## מקורות

- Sebastien Rousseau, (2026). [The November 2026 pacs.008 Structured-Address Deadline: A Six-Month View](https://sebastienrousseau.com/2026-05-12-iso-20022-pacs008-structured-address-deadline/index.html "The November 2026 pacs.008 Structured-Address Deadline").
- Sebastien Rousseau, (2018). [ERC-20: The Ethereum Token Interface That Changed the World](https://sebastienrousseau.com/2018-01-24-the-erc-20-token-standard/index.html "ERC-20: The Ethereum Token Interface That Changed the World").
- Sebastien Rousseau, (2018). [Understanding the Technology behind Blockchain](https://sebastienrousseau.com/2018-01-09-understanding-the-technology-behind-blockchain/index.html "Understanding the Technology behind Blockchain").
- Sebastien Rousseau, (2018). [Unveiling a New Cryptocurrency and Faster Payment Solution](https://sebastienrousseau.com/2018-02-04-unveiling-a-new-cryptocurrency-and-offering-future-faster-payment-solution/index.html "Unveiling a New Cryptocurrency and Faster Payment Solution").
- Unchained, (2026). [BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital ⧉](https://unchainedcrypto.com/blackrock-files-for-two-new-tokenized-money-market-funds-targeting-stablecoin-capital/ "BlackRock Files for Two New Tokenized Money-Market Funds Targeting Stablecoin Capital"). Unchained.
- The Block, (2026). [BlackRock urges OCC to drop tokenized reserve cap idea, expand eligible assets in GENIUS Act comment letter ⧉](https://www.theblock.co/post/399812/blackrock-urges-occ-to-drop-tokenized-reserve-cap-idea-expand-eligible-assets-in-genius-act-comment-letter "BlackRock urges OCC to drop tokenized reserve cap idea"). The Block.
- BeInCrypto, (2026). [BlackRock Backs OCC Stablecoin Rules Under GENIUS Act ⧉](https://beincrypto.com/blackrock-occ-stablecoin-genius-act-comment/ "BlackRock Backs OCC Stablecoin Rules Under GENIUS Act"). BeInCrypto.
- Markets Media, (2026). [BlackRock Fires 'Starting Gun for a New Financial Era' ⧉](https://www.marketsmedia.com/blackrock-fires-starting-gun-for-a-new-financial-era/ "BlackRock Fires 'Starting Gun for a New Financial Era'"). Markets Media.
- Crowdfund Insider, (2026). [BlackRock Focuses On Tokenization Initiatives With Blockchain Enabled Funds ⧉](https://www.crowdfundinsider.com/2026/05/278346-blackrock-focuses-on-tokenization-initiatives-with-blockchain-enabled-funds/ "BlackRock Focuses On Tokenization Initiatives With Blockchain Enabled Funds"). Crowdfund Insider.
- CoinDesk, (2026). [BlackRock Deepens Tokenization Push with New Onchain Fund Offerings ⧉](https://www.coindesk.com/business/2026/05/09/blackrock-deepens-tokenization-push-with-new-onchain-fund-offerings "BlackRock Deepens Tokenization Push with New Onchain Fund Offerings"). CoinDesk.
- Crypto Briefing, (2026). [BlackRock doubles down on tokenization with new stablecoin reserve funds ⧉](https://cryptobriefing.com/blackrock-tokenized-money-market-funds-stablecoins/ "BlackRock doubles down on tokenization with new stablecoin reserve funds"). Crypto Briefing.
- Latham & Watkins, (2026). [OCC Issues Proposal to Implement the GENIUS Act ⧉](https://www.lw.com/en/insights/occ-issues-proposal-to-implement-the-genius-act "OCC Issues Proposal to Implement the GENIUS Act"). Latham & Watkins.
- Nixon Peabody, (2026). [Proposed OCC Regulations for Payment Stablecoins Under the GENIUS Act ⧉](https://www.nixonpeabody.com/insights/alerts/2026/04/02/proposed-occ-regulations-for-payment-stablecoins-under-the-genius-act "Proposed OCC regulations for payment stablecoins under the GENIUS Act"). Nixon Peabody LLP.
- Morgan Lewis, (2026). [Stablecoin Regulation: OCC Proposal Under the GENIUS Act ⧉](https://www.morganlewis.com/pubs/2026/04/occs-genius-act-proposal-what-prospective-issuers-need-to-know "Stablecoin Regulation: OCC Proposal Under the GENIUS Act"). Morgan Lewis.
- American Banker, (2026). [Stablecoin yield debate dominates GENIUS rule comments ⧉](https://www.americanbanker.com/news/stablecoin-yield-debate-dominates-genius-rule-comments "Stablecoin yield debate dominates GENIUS rule comments"). American Banker.
- Congressional Research Service, (2026). [The Stablecoin Yield Debate ⧉](https://www.congress.gov/crs-product/IF13174 "The Stablecoin Yield Debate"). Congress.gov.
- Compliance Corylated, (2026). [US OCC closes GENIUS Act loophole allowing yield-bearing stablecoins ⧉](https://www.compliancecorylated.com/news/us-occ-closes-genius-act-loophole-allowing-yield-bearing-stablecoins/ "US OCC closes GENIUS Act loophole allowing yield-bearing stablecoins"). Compliance Corylated.
- CryptoSlate, (2025). [Tokenized US Treasuries just broke DeFi's most sacred rule ⧉](https://cryptoslate.com/tokenized-us-treasuries-silently-replaced-defis-foundation-and-you-missed-the-critical-9-billion-shift/ "Tokenized US Treasuries — CryptoSlate"). CryptoSlate.
- MEXC News, (2026). [BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum ⧉](https://www.mexc.com/news/1080472 "BlackRock files for two new tokenized funds with the U.S. SEC on Ethereum"). MEXC News.
- Stellar Foundation, (2026). [Franklin Templeton, Stellar Development Foundation Mark Five Years of BENJI ⧉](https://stellar.org/press/franklin-templeton-stellar-development-foundation-mark-five-years-of-benji-the-first-u-s-registered-tokenized-money-market-fund "Five Years of BENJI"). Stellar Development Foundation.
