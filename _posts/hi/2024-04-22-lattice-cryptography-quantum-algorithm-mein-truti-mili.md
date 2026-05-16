---
title: "लैटिस-आधारित क्रिप्टो के क्वांटम-अल्गोरिदम में त्रुटि मिली"
subtitle: "अद्यतन: मूल दावा निरस्त — लैटिस-मानक सुरक्षित बने रहते हैं"
description: "Yilei Chen के क्वांटम-अल्गोरिदम में त्रुटि — लैटिस-आधारित पोस्ट-क्वांटम मानक सुरक्षित बने रहते हैं।"
date: "April 22, 2024"
language: "hi-IN"
locale: "hi_IN"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "क्रिप्टोग्राफिक त्रुटि की प्रतीकात्मक छवि"
keywords: "क्वांटम अल्गोरिदम, लैटिस, क्रिप्टोग्राफी, post-quantum, NIST, Yilei Chen, त्रुटि, बग, सुरक्षा, MLWE"
---

> **TL;DR.** Yilei Chen के क्वांटम-अल्गोरिदम में त्रुटि — लैटिस-आधारित पोस्ट-क्वांटम मानक सुरक्षित बने रहते हैं। (DRAFT — मशीन-सहायता प्राप्त हिंदी अनुवाद; देशी समीक्षा लंबित।)
>
> **मुख्य निष्कर्ष**
>
> - यह लेख एक तकनीकी विषय का विश्लेषण प्रस्तुत करता है।
> - मुख्य अवधारणाएँ ऊपर परिभाषित की गई हैं।
> - बैंकिंग और वित्तीय निहितार्थ नीचे विवेचित हैं।
> - प्रौद्योगिकी, अंगीकार और जोखिमों पर दृष्टिकोण साझा किया गया है।
> - दीर्घकालिक रुझान निष्कर्ष में सारांशित हैं।


## El enigma क्वांटम: reevaluación का वह estandarización NIST का क्रिप्टोग्राफी पोस्ट-क्वांटम को वह luz के algoritmo का Yilei Chen

A raíz का mi reciente artículo sobre वे [चुनौतियाँ का वे algoritmos क्वांटम के लिए वह क्रिप्टोग्राफी sobre retículos][00], debo aportar एक actualización sobre वे últimos desarrollos relativos को [वह investigación का Yilei Chen ⧉][01].

En एक giro inesperado, Yilei Chen, profesor adjunto में वह Institute for Interdisciplinary Information Science (IIIS) का वह Universidad Tsinghua, है informado का जो उसके colegas Hongxun Wu और Thomas Vidick हैं descubierto independientemente एक bug में उसका algoritmo क्वांटम में tiempo polinómico diseñado के लिए resolver वह समस्या Learning with Errors (LWE).

Este bug vuelve inoperante को algoritmo, और Chen है reconocido जो उसका enfoque नहीं se sostiene जैसे reivindicó inicialmente.

## El bug में वह algoritmo क्वांटम का Chen

El bug se है encontrado में वह paso 9 के algoritmo का Chen, और यह है declarado नहीं saber cómo corregirlo. Este descubrimiento है एक alivio के लिए वह समुदाय क्रिप्टोग्राफिक, क्योंकि confirma जो वह समस्या LWE, componente गंभीर का वे métodos का protección में क्रिप्टोग्राफी पोस्ट-क्वांटम, जारी रखता है siendo seguro.

El artículo का Chen भी examinaba otros समस्याएँ complejos sobre retículos, जैसे वह decisional shortest vector problem (GapSVP) और वह shortest independent vector problem (SIVP), में factores का aproximación polinómicos. Aunque वह bug में उसका algoritmo नहीं afecta directamente को ये समस्याएँ, suscita interrogantes sobre वह robustez का वे algoritmos क्वांटम contra वह क्रिप्टोग्राफी sobre retículos.

Pero según [वह página का Nigel Smart ⧉][02], वह ataque क्वांटम propuesto contra LWE है defectuoso और नहीं compromete वे esquemas का क्रिप्टोग्राफी sobre retículos जैसे [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] या [TFHE ⧉][07].

## Implicaciones के लिए वह proceso का estandarización NIST का क्रिप्टोग्राफी पोस्ट-क्वांटम

La investigación का Chen है suscitado indirectamente preocupaciones और dudas sobre वह [proceso का estandarización NIST का क्रिप्टोग्राफी पोस्ट-क्वांटम (PQC) ⧉][03] और वह selección का वे algoritmos क्रिप्टोग्राफिक resistentes को lo क्वांटम.

Los esquemas [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) और CRYSTALS-Dilithium, बीच वे finalistas के proceso का estandarización NIST PQC, हैं ejemplos का esquemas क्रिप्टोग्राफिक sobre retículos जो हैं sido rigurosamente probados और evaluados द्वारा उसका resistencia क्वांटम. Sin embargo, है crucial continuar probando और refinando ये esquemas के लिए सुनिश्चित करना उसका सुरक्षा और viabilidad को largo plazo.

El NIST, वह समुदाय क्रिप्टोग्राफिक और वे उद्यम deben बने रहना vigilantes और continuar explorando fundamentos matemáticos alternativos के लिए वह क्रिप्टोग्राफी पोस्ट-क्वांटम, के साथ वह fin का सुनिश्चित करना जो एक conjunto robusto और diverso का opciones का सुरक्षा resistente को lo क्वांटम esté में उसका sitio.

## El भविष्य का वह क्रिप्टोग्राफी पोस्ट-क्वांटम

El descubrimiento के bug में वह algoritmo का Chen subraya वह papel गंभीर का वह revisión द्वारा पीयर में वह proceso científico. También pone का manifiesto वह necesidad का revisión instantánea, retroalimentación और debate.

La था क्वांटम है comenzado, और वह necesidad का विकसित करना métodos क्रिप्टोग्राफिक resistentes को lo क्वांटम exige medidas cooperativas को escala विश्व-स्तरीय के लिए सुनिश्चित करना वह सुरक्षा का nuestra अवसंरचना डिजिटल frente को वे crecientes capacidades का वह क्वांटम कंप्यूटिंग और को वह carrera द्वारा वह supremacía क्वांटम.

El proceso का estandarización NIST PQC है एक etapa significativa में यह dirección, परंतु है solo एक comienzo. El bug में वह algoritmo का Chen है एक recordatorio brutal का वे चुनौतियाँ e incertidumbres द्वारा venir, परंतु भी sirve जैसे llamada को वह acción के लिए जो वह समुदाय क्रिप्टोग्राफिक redoble उसके esfuerzos और amplíe वे fronteras का lo संभव.

Es एक विकास fascinante में वह campo का वह क्रिप्टोग्राफी पोस्ट-क्वांटम, और होगा interesante ver cómo evoluciona वह proceso का estandarización NIST PQC में respuesta को यह नई जानकारी.

## निष्कर्ष

El bug descubierto में वह algoritmo क्वांटम का Yilei Chen के लिए resolver वह समस्या LWE atestigua वह importancia का एक revisión द्वारा पीयर rigurosa और का वह colaboración में वह विकास का वह क्रिप्टोग्राफी resistente को lo क्वांटम.

Aunque वह bug प्रदान करता है एक respiro temporal को वह सुरक्षा का वे esquemas क्रिप्टोग्राफिक sobre retículos, भी recuerda वह necesidad continuada का investigación और विकास में वह campo का वह क्रिप्टोग्राफी पोस्ट-क्वांटम.

Mientras वह NIST prosigue उसका proceso का estandarización PQC, वह समुदाय क्रिप्टोग्राफिक debe बने रहना proactiva और adaptativa, abrazando वे नई ideas और enfoques के लिए सुनिश्चित करना वह सुरक्षा को largo plazo का nuestro mundo डिजिटल frente को वे crecientes capacidades का वह क्वांटम कंप्यूटिंग.

## संदर्भ-स्रोत

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
