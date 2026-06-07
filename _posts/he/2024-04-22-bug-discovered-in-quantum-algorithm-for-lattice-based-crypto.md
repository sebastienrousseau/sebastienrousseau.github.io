---
title: "التشفير الكمومي القائم على الشبكات: خلل في هجوم Chen على LWE"
tags: "קריפטוגרפיה פוסט-קוונטית, NIST, quantum algorithms, Lattice-Based Cryptography, LWE Problem, מחשוב קוונטי, Cryptographic Security, Quantum Resistance, Cryptography Research, ISO 20022, AI, Rust"
subtitle: "مراجعة الأقران تكشف عن خلل في عمل Chen الرائد"
description: "خلل في الخوارزمية الكمومية لـLWE من Yilei Chen يمنح التشفير القائم على الشبكات مهلةً مؤقّتة. ما يعنيه ذلك لـCRYSTALS-Kyber وDilithium وخارطة طريق PQC."
date: "Apr 22, 2024"
language: "he-IL"
locale: "he_IL"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "صورة مُولَّدة باستخدام MidJourney — شبكة من العُقَد الرقمية بألوان حمراء وزرقاء."
keywords: "التشفير ما بعد الكمومي, NIST, توحيد PQC القياسي, Yilei Chen, الخوارزمية الكمومية, التشفير القائم على الشبكات, مسألة LWE, CRYSTALS-KYBER, CRYSTALS-Dilithium, التشفير المقاوم للكمومية"
---

## التشفير الكمومي القائم على الشبكات: خلل في هجوم Chen على LWE

## اللغز الكمومي: إعادة تقييم توحيد NIST القياسي للتشفير ما بعد الكمومي على ضوء خوارزمية Yilei Chen

في أعقاب مقالي الأخير حول [تحدّيات الخوارزميات الكمومية للتشفير القائم على الشبكات][00]، يتعيّن عليّ تقديم تحديث بشأن آخر التطوّرات المتعلّقة بـ[بحث Yilei Chen ⧉][01].

في تحوّل غير متوقَّع، أفاد Yilei Chen، الأستاذ المساعد في معهد العلوم المعلوماتية متعدّدة التخصّصات (IIIS) بجامعة Tsinghua، بأنّ زميليه العالمَين Hongxun Wu وThomas Vidick قد اكتشفا، كلٌّ على حدة، خللاً في خوارزميته الكمومية في الزمن المتعدّد الحدود المُصمَّمة لحلّ مسألة Learning with Errors (LWE).

ويجعل هذا الخلل الخوارزمية غير صالحة للعمل، وقد أقرّ Chen بأنّ نهجه لا يصمد كما اُدّعي في البداية.

## الخلل في خوارزمية Chen الكمومية

عُثر على الخلل في الخطوة 9 من خوارزمية Chen، وقد صرّح بأنّه لا يعرف كيفية إصلاحه. وهذا الاكتشاف يُمثّل ارتياحاً للمجتمع التشفيري، إذ يُؤكِّد أنّ مسألة LWE، وهي مكوّن حاسم في طرق الحماية التشفيرية ما بعد الكمومية، تظلّ آمنة.

كما تناولت ورقة Chen مسائل شبكية معقّدة أخرى، كـdecisional shortest vector problem (GapSVP) وshortest independent vector problem (SIVP) في إطار عوامل تقريب متعدّدة الحدود. ورغم أنّ الخلل في خوارزميته لا يؤثّر مباشرةً في هذه المسائل، فإنّه يُثير تساؤلات حول متانة الخوارزميات الكمومية ضدّ التشفير القائم على الشبكات.

ولكن وفقاً لـ[صفحة Nigel Smart ⧉][02]، فإنّ الهجوم الكمومي المقترح على LWE معيب ولا يُعرّض للخطر مخطّطات التشفير على الشبكات كـ[Kyber ⧉][04] أو [Dilithium ⧉][05] أو [BGV ⧉][06] أو [TFHE ⧉][07].

## التبعات على عملية توحيد NIST القياسي للتشفير ما بعد الكمومي

أثار بحث Chen، بشكل غير مباشر، مخاوف وشكوكاً حول [عملية توحيد NIST القياسي للتشفير ما بعد الكمومي (PQC) ⧉][03] واختيار خوارزميات تشفير مقاومة للكمومية.

ومخطّطا [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) وCRYSTALS-Dilithium، اللذان يُعدّان من المرشَّحين النهائيين في عملية توحيد NIST PQC، مثالان على مخطّطات تشفيرية قائمة على الشبكات اختُبرت وقُيِّمت بصرامة بحثاً عن مقاومتها للكمومية. غير أنّه من الجوهري مواصلة اختبار هذه المخطّطات وتنقيحها لضمان أمنها وقابليتها للحياة على المدى الطويل.

ويجب على NIST والمجتمع التشفيري والشركات الحفاظ على اليقظة ومواصلة استكشاف أُسس رياضية بديلة للتشفير ما بعد الكمومي لضمان توافر مجموعة متينة ومتنوّعة من الخيارات للأمن المقاوم للكمومية.

## مستقبل التشفير ما بعد الكمومي

يُؤكِّد اكتشاف الخلل في خوارزمية Chen الدور الحاسم لمراجعة الأقران في العملية العلمية. كما يُبرز الحاجة إلى المراجعة الفورية والملاحظات والنقاش.

لقد بدأ العصر الكمومي، والحاجة إلى تطوير طرق تشفير مقاومة للكمومية تتطلّب تدابير تعاونية على نطاق عالمي لضمان أمن بنيتنا التحتية الرقمية في مواجهة قدرات الحوسبة الكمومية المتقدّمة والسباق نحو التفوّق الكمومي.

وعملية توحيد NIST PQC القياسي خطوة مهمّة في هذا الاتّجاه، ولكنّها مجرّد بداية. والخلل في خوارزمية Chen تذكير صارخ بالتحدّيات والشكوك التي تلوح في الأفق، ولكنّه يُمثّل أيضاً نداءً للعمل للمجتمع التشفيري كي يُضاعف جهوده ويُوسِّع حدود الممكن.

هذا تطوّر مُذهل في ميدان التشفير ما بعد الكمومي، وسيكون من المثير للاهتمام رؤية كيف ستتطوّر عملية توحيد NIST PQC القياسي استجابةً لهذه المعلومات الجديدة.

## الخاتمة

الخلل المكتشَف في خوارزمية Yilei Chen الكمومية لحلّ مسألة LWE شاهد على أهمّية مراجعة الأقران الصارمة والتعاون في تطوير التشفير المقاوم للكمومية.

ورغم أنّ الخلل يُوفِّر مهلةً مؤقّتة لأمن المخطّطات التشفيرية القائمة على الشبكات، فإنّه يُذكِّر أيضاً بالحاجة المستمرّة إلى البحث والتطوير في ميدان التشفير ما بعد الكمومي.

ومع مواصلة NIST عملية توحيد PQC القياسي، يجب على المجتمع التشفيري أن يبقى استباقياً ومتكيِّفاً، مُحتضِناً الأفكار والنهج الجديدة لضمان الأمن طويل الأمد لعالمنا الرقمي في مواجهة قدرات الحوسبة الكمومية المتقدّمة.

## المراجع

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
