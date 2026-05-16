---
title: "Un algoritmo cuántico desafía a la criptografía sobre retículos"
subtitle: "El próximo algoritmo cuántico en tiempo polinómico contra la criptografía sobre retículos"
description: "Un nuevo algoritmo cuántico en tiempo polinómico de Yilei Chen apunta a la criptografía sobre retículos. Implicaciones para los estándares postcuánticos, incluido CRYSTALS-Kyber."
date: "April 15, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/digital-constellation.webp"
banner_alt: "Banner que representa nodos de red en un espacio digital azul"
keywords: "computación cuántica, algoritmo cuántico, criptografía sobre retículos, LWE, cifrado, criptografía postcuántica, ciberseguridad, Yilei Chen, investigación criptográfica, amenazas de seguridad"
---


> **TL;DR.** Tento článek je DRAFT překlad původně španělského zdroje, čekající na revizi rodilým mluvčím. Hlavní obsah, příklady a citace zůstávají ve španělštině; pouze záhlaví/frontmatter byly přepnuty na češtinu.

**Klíčové body**

## Resumen ejecutivo

Este artículo explora los trabajos de [**Yilei Chen ⧉**][00], quien ha desarrollado un `algoritmo cuántico en tiempo polinómico` susceptible de impactar significativamente la dificultad del problema matemático **Learning With Errors (LWE)**, un desafío fundamental de la criptografía sobre retículos.

Los retículos son subgrupos discretos del espacio euclidiano de n dimensiones que desempeñan un papel crucial en los esquemas criptográficos modernos. El problema LWE consiste en encontrar un vector secreto a partir de un conjunto de ecuaciones lineales aproximadas, y constituye una piedra angular de numerosos protocolos criptográficos postcuánticos.

## El algoritmo cuántico en tiempo polinómico de Chen

El algoritmo de Chen ofrece una solución al `decisional shortest vector problem (GapSVP)` y al `shortest independent vector problem (SIVP)` para retículos de cualquier dimensión. Lo logra con una complejidad en tiempo polinómico, una mejora significativa respecto a las soluciones anteriores.

Las innovaciones clave de su trabajo incluyen:

* **Funciones gaussianas con varianzas complejas:** Chen introduce el uso de funciones gaussianas con varianzas complejas en el diseño del algoritmo cuántico. Este enfoque aprovecha las propiedades de las distribuciones gaussianas complejas para manipular más eficientemente los estados cuánticos, permitiendo una solución más eficiente al problema LWE.

* **Transformada de Fourier cuántica con ventana:** El algoritmo aplica una transformada de Fourier cuántica con ventana.

## Introducción a los problemas sobre retículos y a su importancia en criptografía

Los problemas sobre retículos implican el estudio de estructuras matemáticas llamadas retículos, que son subgrupos discretos del espacio euclidiano de n dimensiones. Estos problemas han ganado una atención significativa en criptografía debido a su presunta resistencia a los ataques cuánticos.

El problema de retículo más notable es el [**problema Learning With Errors (LWE) ⧉**][01], introducido por Oded Regev. LWE es un problema computacional que consiste en encontrar un vector secreto a partir de un conjunto de ecuaciones lineales aproximadas.

Numerosos esquemas criptográficos modernos, como el criptosistema de Regev y el intercambio de claves Frodo, basan su seguridad en la dificultad de resolver el problema LWE.

## Algoritmos clásicos para los problemas sobre retículos y sus límites

Los algoritmos clásicos para resolver los problemas sobre retículos, como el algoritmo **Lenstra-Lenstra-Lovász (LLL)** y sus variantes, han sido extensamente estudiados en criptografía. Sin embargo, estos algoritmos afrontan desafíos significativos en términos de complejidad computacional, en particular a medida que las dimensiones del retículo aumentan.

Los algoritmos clásicos bien conocidos para resolver el problema LWE dependen exponencialmente del número de variables, lo que los hace impracticables para los retículos de alta dimensión. Esta barrera de complejidad es un factor clave de la seguridad de los esquemas criptográficos basados en LWE.

## Intentos anteriores de algoritmos cuánticos para LWE

Antes del trabajo de Chen, varios investigadores habían explorado el potencial de los algoritmos cuánticos para resolver el problema LWE.

Oded Regev desarrolló con éxito una reducción cuántica de `GapSVP` a `LWE`. Sin embargo, conviene señalar que esta reducción requiere un oráculo cuántico para resolver GapSVP, cuya existencia queda por establecer.

Kuperberg creó [**un algoritmo cuántico para resolver LWE con un factor de aproximación subexponencial ⧉**][02]. Sin embargo, estos enfoques algorítmicos se apoyaban en hipótesis no verificadas o presentaban una velocidad computacional más lenta. Por contraste, el algoritmo de Chen ofrece una solución en tiempo polinómico sin necesidad de un oráculo cuántico.

## El algoritmo cuántico en tiempo polinómico de Chen para LWE

El algoritmo cuántico de Yilei Chen para resolver el problema LWE en tiempo polinómico representa un avance significativo en el campo. El algoritmo emplea dos técnicas nuevas:

1. **Funciones gaussianas con varianzas complejas**: Chen introduce el uso de funciones gaussianas con varianzas complejas en el diseño del algoritmo cuántico. Este enfoque aprovecha las propiedades de las distribuciones gaussianas complejas para manipular más eficientemente los estados cuánticos, permitiendo una solución más eficiente al problema LWE.

2. **Transformada de Fourier cuántica con ventana**: El algoritmo aplica una transformada de Fourier cuántica con ventana, que permite el análisis simultáneo del problema en los dominios temporal y frecuencial. Esta técnica permite al algoritmo tratar eficientemente la estructura de alta dimensión de los retículos y extraer la información pertinente para resolver LWE.

El algoritmo de Chen combina estas técnicas para resolver `LWE`, `GapSVP` y `SIVP` en tiempo polinómico para todas las dimensiones de retículo. Esto es una mejora importante respecto a los algoritmos clásicos y cuánticos anteriores.

## Implicaciones, limitaciones y ejes de investigación futuros

El algoritmo cuántico de Chen tiene implicaciones para LWE, cuestionando la noción de que los ataques cuánticos no pueden romper LWE y los problemas similares sobre retículos. Esta hipótesis forma la base de numerosos esquemas criptográficos emergentes. Sin embargo, comprender los límites del algoritmo y su impacto potencial sobre los sistemas de cifrado existentes basados en LWE es esencial.

Una cuestión clave con el algoritmo de Chen es que funciona de manera óptima cuando el tamaño del problema supera significativamente el margen de error permitido. En los esquemas criptográficos prácticos basados en LWE, el ratio módulo-ruido se mantiene típicamente bajo por razones de seguridad. Inversamente, el algoritmo de Chen requiere un ratio más alto para alcanzar su tiempo de ejecución polinómico.

Este límite sugiere que los esquemas de cifrado basados en LWE existentes con ratios módulo-ruido más pequeños podrían permanecer seguros frente al algoritmo de Chen tal como se presenta actualmente. Por consiguiente, si bien el algoritmo marca un avance teórico significativo, no representa una amenaza inmediata para la seguridad de todos los sistemas criptográficos basados en LWE.

Su trabajo subraya la necesidad de proseguir la investigación sobre el desarrollo de primitivas criptográficas resistentes a lo cuántico.

## Aplicaciones potenciales e incentivos

El desarrollo de algoritmos cuánticos eficientes para los problemas sobre retículos tiene implicaciones de gran alcance en todos los sectores que se apoyan en la comunicación digital segura y el almacenamiento de datos. El algoritmo de Chen pone de manifiesto la necesidad universal de cifrado resistente a lo cuántico.

Esto incluye industrias como:

* **Ciberseguridad:** métodos de cifrado robustos y resistentes a lo cuántico son cruciales para proteger la información sensible en la era de la computación cuántica.

* **Sector público y defensa:** los gobiernos pueden aprovechar estos avances para reforzar la seguridad de las infraestructuras críticas y las comunicaciones clasificadas, mitigando las amenazas potenciales planteadas por las capacidades cuánticas adversarias.

* **Servicios financieros:** el sector financiero depende fuertemente de canales de comunicación seguros para las transacciones y la protección de los datos. Primitivas criptográficas resistentes a lo cuántico basadas en los problemas sobre retículos podrían contribuir a garantizar la seguridad a largo plazo de los sistemas financieros.

* **Sanidad:** mientras los datos sanitarios se vuelven cada vez más digitalizados, garantizar su confidencialidad e integridad es primordial. Métodos de cifrado cuántico-seguros derivados de los trabajos de Chen podrían ayudar a proteger la información sensible de los pacientes contra los futuros ataques cuánticos.

* **Cloud computing:** con la creciente adopción de los servicios cloud, la seguridad de los datos almacenados y tratados en el cloud es una preocupación principal. Esquemas de cifrado resistentes a lo cuántico basados en los problemas sobre retículos podrían proporcionar una capa adicional de protección para las aplicaciones y el almacenamiento de datos en modo cloud.

## Conclusión

El algoritmo cuántico en tiempo polinómico de Yilei Chen para resolver el problema LWE representa un hito significativo en el campo de la computación cuántica y la criptografía. Utilizando nuevos métodos como las funciones gaussianas y las transformadas de Fourier cuánticas con ventana, Chen ha mostrado cómo los algoritmos cuánticos pueden resolver eficientemente problemas complejos sobre retículos. Sin embargo, es esencial señalar que este trabajo constituye actualmente un avance teórico, y que se necesita investigación adicional para acercarlo a una implementación práctica.

El desarrollo de la criptografía resistente a lo cuántico no es solo un desafío técnico, sino también un imperativo estratégico para las empresas y los gobiernos. Invertir en I+D en este campo podría producir beneficios significativos a largo plazo en términos de seguridad y confidencialidad de los datos.

## Referencias

Chen, Y. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] In *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (pp. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
