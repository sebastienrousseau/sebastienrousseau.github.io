---
title: "Um algoritmo quântico desafía a a criptografia sobre retículos"
subtitle: "El próximo algoritmo quântico em tempo polinómico contra a criptografia sobre retículos"
description: "Um novo algoritmo quântico em tempo polinómico de Yilei Chen apunta a a criptografia sobre retículos. Implicaciones para os estándares pós-quânticos, incluído CRYSTALS-Kyber."
date: "April 15, 2024"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/digital-constellation.webp"
banner_alt: "Banner que representa nodos de red em um espacio digital azul"
keywords: "computação quântica, algoritmo quântico, criptografia sobre retículos, LWE, criptografia, criptografia pós-quântica, ciberseguridad, Yilei Chen, investigación criptográfica, amenazas de segurança"
---

## Resumen ejecutivo

Este artigo explora os trabalhos de [**Yilei Chen ⧉**][00], quem desenvolveu um `algoritmo quântico em tempo polinómico` susceptible de impactar significativamente a dificuldade do problema matemático **Learning With Errors (LWE)**, um desafío fundamental de a criptografia sobre retículos.

Los retículos são subgrupos discretos do espacio euclidiano de n dimensões que desempeñan um papel crucial em os esquemas criptográficos modernos. El problema LWE consiste em encontrar um vector secreto a partir de um conjunto de ecuaciones lineales aproximadas, e constituye uma piedra angular de numerosos protocolos criptográficos pós-quânticos.

## El algoritmo quântico em tempo polinómico de Chen

El algoritmo de Chen oferece uma solução ao `decisional shortest vector problem (GapSVP)` e ao `shortest independent vector problem (SIVP)` para retículos de cualquier dimensão. Lo alcança com uma complexidade em tempo polinómico, uma mejora significativa respecto a as soluções anteriores.

Las innovaciones clave de seu trabalho incluem:

* **Funciones gaussianas com varianzas complejas:** Chen introduz o uso de funciones gaussianas com varianzas complejas em o diseño do algoritmo quântico. Este enfoque aproveita as propriedades de as distribuciones gaussianas complejas para manipular mais eficientemente os estados quânticos, permitiendo uma solução mais eficiente ao problema LWE.

* **Transformada de Fourier quântica com ventana:** El algoritmo aplica uma transformada de Fourier quântica com ventana.

## Introducción a os problemas sobre retículos e a seu importancia em criptografia

Los problemas sobre retículos implican o estudo de estructuras matemáticas llamadas retículos, que são subgrupos discretos do espacio euclidiano de n dimensões. Estos problemas têm ganado uma atención significativa em criptografia devido a seu presunta resistencia a os ataques quânticos.

El problema de retículo mais notable é o [**problema Learning With Errors (LWE) ⧉**][01], introducido por Oded Regev. LWE é um problema computacional que consiste em encontrar um vector secreto a partir de um conjunto de ecuaciones lineales aproximadas.

Numerosos esquemas criptográficos modernos, como o criptosistema de Regev e o intercambio de claves Frodo, basan seu segurança em a dificuldade de resolver o problema LWE.

## Algoritmos clásicos para os problemas sobre retículos e seus límites

Los algoritmos clásicos para resolver os problemas sobre retículos, como o algoritmo **Lenstra-Lenstra-Lovász (LLL)** e seus variantes, foram extensamente estudiados em criptografia. Sin embargo, estes algoritmos afrontan desafíos significativos em términos de complexidade computacional, em particular à medida que as dimensões do retículo aumentan.

Los algoritmos clásicos bien conhecidos para resolver o problema LWE dependen exponencialmente do número de variables, lo que os faz impracticables para os retículos de alta dimensão. Esta barrera de complexidade é um factor clave de a segurança de os esquemas criptográficos basados em LWE.

## Intentos anteriores de algoritmos quânticos para LWE

Antes do trabalho de Chen, vários investigadores tinham explorado o potencial de os algoritmos quânticos para resolver o problema LWE.

Oded Regev desenvolveu com éxito uma reducción quântica de `GapSVP` a `LWE`. Sin embargo, conviene señalar que esta reducción requer um oráculo quântico para resolver GapSVP, cuya existencia queda por establecer.

Kuperberg criou [**um algoritmo quântico para resolver LWE com um factor de aproximación subexponencial ⧉**][02]. Sin embargo, estes enfoques algorítmicos se apoyaban em hipótesis no verificadas ou presentaban uma velocidade computacional mais lenta. Por contraste, o algoritmo de Chen oferece uma solução em tempo polinómico sem necessidade de um oráculo quântico.

## El algoritmo quântico em tempo polinómico de Chen para LWE

El algoritmo quântico de Yilei Chen para resolver o problema LWE em tempo polinómico representa um avance significativo em o campo. El algoritmo emplea dois técnicas novas:

1. **Funciones gaussianas com varianzas complejas**: Chen introduz o uso de funciones gaussianas com varianzas complejas em o diseño do algoritmo quântico. Este enfoque aproveita as propriedades de as distribuciones gaussianas complejas para manipular mais eficientemente os estados quânticos, permitiendo uma solução mais eficiente ao problema LWE.

2. **Transformada de Fourier quântica com ventana**: El algoritmo aplica uma transformada de Fourier quântica com ventana, que permite o análisis simultáneo do problema em os dominios temporal e frecuencial. Esta técnica permite ao algoritmo tratar eficientemente a estructura de alta dimensão de os retículos e extraer a informação pertinente para resolver LWE.

El algoritmo de Chen combina estas técnicas para resolver `LWE`, `GapSVP` e `SIVP` em tempo polinómico para todas as dimensões de retículo. Esto é uma mejora importante respecto a os algoritmos clásicos e quânticos anteriores.

## Implicaciones, limitaciones e ejes de investigación futuros

El algoritmo quântico de Chen tem implicaciones para LWE, cuestionando a noción de que os ataques quânticos no podem romper LWE e os problemas similares sobre retículos. Esta hipótesis forma a base de numerosos esquemas criptográficos emergentes. Sin embargo, compreender os límites do algoritmo e seu impacto potencial sobre os sistemas de criptografia existentes basados em LWE é esencial.

Una questão clave com o algoritmo de Chen é que funciona de maneira óptima quando o tamaño do problema supera significativamente o margen de error permitido. En os esquemas criptográficos práticos basados em LWE, o ratio módulo-ruido se mantém típicamente sob por razões de segurança. Inversamente, o algoritmo de Chen requer um ratio mais alto para alcançar seu tempo de execução polinómico.

Este límite sugiere que os esquemas de criptografia basados em LWE existentes com ratios módulo-ruido mais pequeños poderiam permanecer seguros frente ao algoritmo de Chen tal como se presenta atualmente. Por consiguiente, si bien o algoritmo marca um avance teórico significativo, no representa uma amenaza inmediata para a segurança de todos os sistemas criptográficos basados em LWE.

Su trabalho subraya a necessidade de proseguir a investigación sobre ou desenvolvimento de primitivas criptográficas resistentes a lo quântico.

## Aplicaciones potenciales e incentivos

El desenvolvimento de algoritmos quânticos eficientes para os problemas sobre retículos tem implicaciones de gran alcance em todos os sectores que se apoyan em a comunicação digital segura e o almacenamiento de dados. El algoritmo de Chen coloca de manifiesto a necessidade universal de criptografia resistente a lo quântico.

Esto inclui industrias como:

* **Ciberseguridad:** métodos de criptografia robustos e resistentes a lo quântico são cruciales para proteger a informação sensible em a era de a computação quântica.

* **Sector público e defensa:** os governos podem aproveitar estes avances para reforzar a segurança de as infraestruturas críticas e as comunicações clasificadas, mitigando as amenazas potenciales planteadas por as capacidades quânticas adversarias.

* **Serviços financeiros:** o sector financeiro depende fuertemente de canales de comunicação seguros para as transações e a protección de os dados. Primitivas criptográficas resistentes a lo quântico basadas em os problemas sobre retículos poderiam contribuir a garantizar a segurança a longo prazo de os sistemas financeiros.

* **Sanidad:** enquanto os dados sanitarios se vuelven cada vez mais digitalizados, garantizar seu confidencialidad e integridad é primordial. Métodos de criptografia quântico-seguros derivados de os trabalhos de Chen poderiam ayudar a proteger a informação sensible de os pacientes contra os futuros ataques quânticos.

* **Cloud computing:** com a creciente adoção de os serviços cloud, a segurança de os dados almacenados e tratados em o cloud é uma preocupação principal. Esquemas de criptografia resistentes a lo quântico basados em os problemas sobre retículos poderiam proporcionar uma capa adicional de protección para as aplicações e o almacenamiento de dados em modo cloud.

## Conclusión

El algoritmo quântico em tempo polinómico de Yilei Chen para resolver o problema LWE representa um hito significativo em o campo de a computação quântica e a criptografia. Utilizando novos métodos como as funciones gaussianas e as transformadas de Fourier quânticas com ventana, Chen mostrou cómo os algoritmos quânticos podem resolver eficientemente problemas complejos sobre retículos. Sin embargo, é esencial señalar que este trabalho constituye atualmente um avance teórico, e que se precisa investigación adicional para acercarlo a uma implementación prática.

El desenvolvimento de a criptografia resistente a lo quântico no é solo um desafío técnico, mas sim também um imperativo estratégico para as empresas e os governos. Invertir em I+D em este campo poderia producir beneficios significativos a longo prazo em términos de segurança e confidencialidad de os dados.

## Referencias

Chen, Y. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] In *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (pp. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
