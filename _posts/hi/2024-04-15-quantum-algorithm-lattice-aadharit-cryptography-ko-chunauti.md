---
title: "एक क्वांटम-अल्गोरिदम लैटिस-आधारित क्रिप्टोग्राफी को चुनौती देता है"
subtitle: "Yilei Chen का दावा और पोस्ट-क्वांटम मानकों पर प्रभाव"
description: "Yilei Chen का क्वांटम-अल्गोरिदम लैटिस-आधारित क्रिप्टोग्राफी को कैसे चुनौती देता है — और इसके पोस्ट-क्वांटम मानकों पर निहितार्थ।"
date: "April 15, 2024"
language: "hi-IN"
locale: "hi_IN"
banner: "https://cloudcdn.pro/stocks/images/digital-constellation.webp"
banner_alt: "लैटिस-क्रिप्टोग्राफी की प्रतीकात्मक छवि"
keywords: "क्वांटम अल्गोरिदम, लैटिस, क्रिप्टोग्राफी, post-quantum, NIST, CRYSTALS-Kyber, Yilei Chen, LWE, MLWE, सुरक्षा"
---

> **TL;DR.** Yilei Chen का क्वांटम-अल्गोरिदम लैटिस-आधारित क्रिप्टोग्राफी को कैसे चुनौती देता है — और इसके पोस्ट-क्वांटम मानकों पर निहितार्थ। (DRAFT — मशीन-सहायता प्राप्त हिंदी अनुवाद; देशी समीक्षा लंबित।)
>
> **मुख्य निष्कर्ष**
>
> - यह लेख एक तकनीकी विषय का विश्लेषण प्रस्तुत करता है।
> - मुख्य अवधारणाएँ ऊपर परिभाषित की गई हैं।
> - बैंकिंग और वित्तीय निहितार्थ नीचे विवेचित हैं।
> - प्रौद्योगिकी, अंगीकार और जोखिमों पर दृष्टिकोण साझा किया गया है।
> - दीर्घकालिक रुझान निष्कर्ष में सारांशित हैं।


## सारांश ejecutivo

Este artículo explora वे trabajos का [**Yilei Chen ⧉**][00], quien है विकसित एक `algoritmo क्वांटम में tiempo polinómico` susceptible का impactar significativamente वह dificultad के समस्या matemático **Learning With Errors (LWE)**, एक चुनौती मूलभूत का वह क्रिप्टोग्राफी sobre retículos.

Los retículos हैं subgrupos discretos के espacio euclidiano का n dimensiones जो desempeñan एक papel crucial में वे esquemas क्रिप्टोग्राफिक modernos. El समस्या LWE consiste में encontrar एक vector secreto से शुरू होकर एक conjunto का ecuaciones lineales aproximadas, और constituye एक piedra angular का numerosos प्रोटोकॉल क्रिप्टोग्राफिक postcuánticos.

## El algoritmo क्वांटम में tiempo polinómico का Chen

El algoritmo का Chen प्रदान करता है एक समाधान को `decisional shortest vector problem (GapSVP)` और को `shortest independent vector problem (SIVP)` के लिए retículos का cualquier dimensión. Lo logra के साथ एक complejidad में tiempo polinómico, एक mejora significativa respecto को वे समाधान anteriores.

Las नवाचार कुंजी का उसका trabajo incluyen:

* **Funciones gaussianas के साथ varianzas complejas:** Chen प्रस्तुत करता है वह उपयोग का funciones gaussianas के साथ varianzas complejas में वह diseño के algoritmo क्वांटम. Este enfoque aprovecha वे propiedades का वे distribuciones gaussianas complejas के लिए manipular अधिक eficientemente वे estados क्वांटम, permitiendo एक समाधान अधिक दक्ष को समस्या LWE.

* **Transformada का Fourier क्वांटम के साथ ventana:** El algoritmo aplica एक transformada का Fourier क्वांटम के साथ ventana.

## परिचय को वे समस्याएँ sobre retículos और को उसका importancia में क्रिप्टोग्राफी

Los समस्याएँ sobre retículos implican वह estudio का estructuras matemáticas llamadas retículos, जो हैं subgrupos discretos के espacio euclidiano का n dimensiones. Estos समस्याएँ हैं ganado एक atención significativa में क्रिप्टोग्राफी के कारण उसका presunta resistencia को वे ataques क्वांटम.

El समस्या का retículo अधिक notable है वह [**समस्या Learning With Errors (LWE) ⧉**][01], introducido द्वारा Oded Regev. LWE है एक समस्या computacional जो consiste में encontrar एक vector secreto से शुरू होकर एक conjunto का ecuaciones lineales aproximadas.

Numerosos esquemas क्रिप्टोग्राफिक modernos, जैसे वह criptosistema का Regev और वह intercambio का कुंजियाँ Frodo, basan उसका सुरक्षा में वह dificultad का resolver वह समस्या LWE.

## Algoritmos clásicos के लिए वे समस्याएँ sobre retículos और उसके límites

Los algoritmos clásicos के लिए resolver वे समस्याएँ sobre retículos, जैसे वह algoritmo **Lenstra-Lenstra-Lovász (LLL)** और उसके variantes, हैं sido extensamente estudiados में क्रिप्टोग्राफी. Sin embargo, ये algoritmos afrontan चुनौतियाँ significativos में términos का complejidad computacional, में particular को medida जो वे dimensiones के retículo aumentan.

Los algoritmos clásicos bien conocidos के लिए resolver वह समस्या LWE dependen exponencialmente के número का variables, lo जो वे hace impracticables के लिए वे retículos का उच्च dimensión. Esta barrera का complejidad है एक factor कुंजी का वह सुरक्षा का वे esquemas क्रिप्टोग्राफिक basados में LWE.

## Intentos anteriores का algoritmos क्वांटम के लिए LWE

Antes के trabajo का Chen, कई investigadores habían explorado वह potencial का वे algoritmos क्वांटम के लिए resolver वह समस्या LWE.

Oded Regev desarrolló के साथ éxito एक reducción क्वांटम का `GapSVP` को `LWE`. Sin embargo, conviene señalar जो यह reducción आवश्यक है एक oráculo क्वांटम के लिए resolver GapSVP, cuya existencia queda द्वारा establecer.

Kuperberg creó [**एक algoritmo क्वांटम के लिए resolver LWE के साथ एक factor का aproximación subexponencial ⧉**][02]. Sin embargo, ये enfoques algorítmicos se apoyaban में hipótesis नहीं verificadas या presentaban एक velocidad computacional अधिक धीमी. Por contraste, वह algoritmo का Chen प्रदान करता है एक समाधान में tiempo polinómico बिना necesidad का एक oráculo क्वांटम.

## El algoritmo क्वांटम में tiempo polinómico का Chen के लिए LWE

El algoritmo क्वांटम का Yilei Chen के लिए resolver वह समस्या LWE में tiempo polinómico representa एक avance significativo में वह campo. El algoritmo emplea dos técnicas नई:

1. **Funciones gaussianas के साथ varianzas complejas**: Chen प्रस्तुत करता है वह उपयोग का funciones gaussianas के साथ varianzas complejas में वह diseño के algoritmo क्वांटम. Este enfoque aprovecha वे propiedades का वे distribuciones gaussianas complejas के लिए manipular अधिक eficientemente वे estados क्वांटम, permitiendo एक समाधान अधिक दक्ष को समस्या LWE.

2. **Transformada का Fourier क्वांटम के साथ ventana**: El algoritmo aplica एक transformada का Fourier क्वांटम के साथ ventana, जो अनुमति देता है वह análisis simultáneo के समस्या में वे dominios temporal और frecuencial. Esta técnica अनुमति देता है को algoritmo tratar eficientemente वह estructura का उच्च dimensión का वे retículos और extraer वह जानकारी pertinente के लिए resolver LWE.

El algoritmo का Chen combina ये técnicas के लिए resolver `LWE`, `GapSVP` और `SIVP` में tiempo polinómico के लिए सभी वे dimensiones का retículo. Esto है एक mejora महत्वपूर्ण respecto को वे algoritmos clásicos और क्वांटम anteriores.

## Implicaciones, limitaciones और ejes का investigación futuros

El algoritmo क्वांटम का Chen tiene implicaciones के लिए LWE, cuestionando वह noción का जो वे ataques क्वांटम नहीं pueden romper LWE और वे समस्याएँ similares sobre retículos. Esta hipótesis forma वह base का numerosos esquemas क्रिप्टोग्राफिक emergentes. Sin embargo, comprender वे límites के algoritmo और उसका impacto potencial sobre वे तंत्र का cifrado existentes basados में LWE है अत्यावश्यक.

Una cuestión कुंजी के साथ वह algoritmo का Chen है जो funciona का manera óptima जब वह tamaño के समस्या supera significativamente वह margen का error अनुमत. En वे esquemas क्रिप्टोग्राफिक prácticos basados में LWE, वह ratio módulo-ruido se mantiene típicamente निम्न द्वारा razones का सुरक्षा. Inversamente, वह algoritmo का Chen आवश्यक है एक ratio अधिक उच्च के लिए alcanzar उसका tiempo का ejecución polinómico.

Este límite sugiere जो वे esquemas का cifrado basados में LWE existentes के साथ ratios módulo-ruido अधिक pequeños podrían बने रहना seguros frente को algoritmo का Chen tal जैसे se presenta actualmente. Por consiguiente, यदि bien वह algoritmo marca एक avance teórico significativo, नहीं representa एक amenaza inmediata के लिए वह सुरक्षा का सभी वे तंत्र क्रिप्टोग्राफिक basados में LWE.

Su trabajo subraya वह necesidad का proseguir वह investigación sobre वह विकास का primitivas क्रिप्टोग्राफिक resistentes को lo क्वांटम.

## अनुप्रयोग potenciales e incentivos

El विकास का algoritmos क्वांटम eficientes के लिए वे समस्याएँ sobre retículos tiene implicaciones का gran alcance में सभी वे sectores जो se apoyan में वह comunicación डिजिटल segura और वह almacenamiento का डेटा. El algoritmo का Chen pone का manifiesto वह necesidad universal का cifrado resistente को lo क्वांटम.

Esto incluye industrias जैसे:

* **Ciberseguridad:** métodos का cifrado robustos और resistentes को lo क्वांटम हैं cruciales के लिए proteger वह जानकारी sensible में वह था का वह क्वांटम कंप्यूटिंग.

* **Sector सार्वजनिक और defensa:** वे सरकारें pueden aprovechar ये avances के लिए reforzar वह सुरक्षा का वे अवसंरचनाएँ críticas और वे comunicaciones clasificadas, mitigando वे amenazas potenciales planteadas द्वारा वे capacidades क्वांटम adversarias.

* **Servicios वित्तीय:** वह sector वित्तीय depende fuertemente का canales का comunicación seguros के लिए वे लेनदेन और वह protección का वे डेटा. Primitivas क्रिप्टोग्राफिक resistentes को lo क्वांटम basadas में वे समस्याएँ sobre retículos podrían contribuir को सुनिश्चित करना वह सुरक्षा को largo plazo का वे तंत्र वित्तीय.

* **Sanidad:** जब कि वे डेटा sanitarios se vuelven cada vez अधिक digitalizados, सुनिश्चित करना उसका confidencialidad e integridad है primordial. Métodos का cifrado क्वांटम-seguros derivados का वे trabajos का Chen podrían ayudar को proteger वह जानकारी sensible का वे pacientes contra वे futuros ataques क्वांटम.

* **Cloud computing:** के साथ वह creciente adopción का वे servicios cloud, वह सुरक्षा का वे डेटा almacenados और tratados में वह cloud है एक preocupación principal. Esquemas का cifrado resistentes को lo क्वांटम basados में वे समस्याएँ sobre retículos podrían proporcionar एक capa adicional का protección के लिए वे अनुप्रयोग और वह almacenamiento का डेटा में modo cloud.

## निष्कर्ष

El algoritmo क्वांटम में tiempo polinómico का Yilei Chen के लिए resolver वह समस्या LWE representa एक hito significativo में वह campo का वह क्वांटम कंप्यूटिंग और वह क्रिप्टोग्राफी. Utilizando नए métodos जैसे वे funciones gaussianas और वे transformadas का Fourier क्वांटम के साथ ventana, Chen है mostrado cómo वे algoritmos क्वांटम pueden resolver eficientemente समस्याएँ complejos sobre retículos. Sin embargo, है अत्यावश्यक señalar जो यह trabajo constituye actualmente एक avance teórico, और जो se necesita investigación adicional के लिए acercarlo को एक implementación práctica.

El विकास का वह क्रिप्टोग्राफी resistente को lo क्वांटम नहीं है solo एक चुनौती técnico, sino भी एक imperativo estratégico के लिए वे उद्यम और वे सरकारें. Invertir में I+D में यह campo podría producir beneficios significativos को largo plazo में términos का सुरक्षा और confidencialidad का वे डेटा.

## संदर्भ-स्रोत

Chen, Y. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] In *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (pp. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
