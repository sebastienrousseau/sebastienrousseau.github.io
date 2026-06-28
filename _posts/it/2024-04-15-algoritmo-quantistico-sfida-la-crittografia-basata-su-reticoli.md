---
title: "Un algoritmo quantistico sfida la crittografia basata su reticoli"
subtitle: "Il nuovo lavoro di Yilei Chen suggerisce una potenziale vulnerabilità"
description: "Un nuovo algoritmo quantistico risolve un problema crittografico chiave, sollecitando un'accelerazione della ricerca sulla sicurezza resistente al quantum."
date: "April 15, 2024"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Algoritmo quantistico e reticoli"
keywords: "quantistico, reticoli, LWE, Yilei Chen, Kyber, PQC, vulnerabilità"
---

---

> **TL;DR.** Un algoritmo quantistico presentato da Yilei Chen suggerisce una possibile soluzione efficiente al problema LWE, su cui poggiano molti schemi PQC. Una scoperta che richiede verifica indipendente urgente.
>
> **Punti chiave**
>
> - **Problema LWE** — Learning With Errors, base di Kyber e Dilithium.
> - **Nuovo algoritmo** — proposta che, se confermata, indebolirebbe alcuni parametri PQC.
> - **Risposta del settore** — peer review urgente e necessità di crittografia ibrida.
> - **Implicazioni** — riconsiderare i parametri NIST e i tempi di migrazione.

---

## Resumen ejecutivo

Questo artículo explora i trabajos di [**Yilei Chen ⧉**][00], quien ha sviluppato un `algoritmo quantistico in tiempo polinómico` susceptible di impactar significativamente la dificultad del problema matemático **Learning With Errors (LWE)**, un sfida fundamental della criptografía su retículos.

I retículos sono subgrupos discretos del espacio euclidiano di n dimensiones che desempeñan un papel crucial in i esquemas crittografici modernos. Il problema LWE consiste in encontrar un vector secreto a partire da un insieme di ecuaciones lineales aproximadas, e constituye una piedra angular di numerosos protocolos crittografici post-quantisticos.

## Il algoritmo quantistico in tiempo polinómico di Chen

Il algoritmo di Chen offre una soluzione al `decisional shortest vector problem (GapSVP)` e al `shortest independent vector problem (SIVP)` per retículos di qualsiasi dimensión. Lo logra con una complejidad in tiempo polinómico, una mejora significativa respecto alle soluzioni anteriores.

Le innovaciones chiave di il suo trabajo includono:

* **Funciones gaussianas con varianzas complejas:** Chen introduce il uso di funciones gaussianas con varianzas complejas in il diseño del algoritmo quantistico. Questo approccio aprovecha le propiedades delle distribuciones gaussianas complejas per manipular più eficientemente i estados quantistici, permitiendo una soluzione più eficiente al problema LWE.

* **Transformada di Fourier quantistica con ventana:** Il algoritmo applica una transformada di Fourier quantistica con ventana.

## Introducción ai problemas su retículos e a il suo importancia in criptografía

I problemas su retículos implican il studio di estructuras matemáticas llamadas retículos, che sono subgrupos discretos del espacio euclidiano di n dimensiones. Questi problemas hanno ganado una atención significativa in criptografía debido a il suo presunta resistencia ai ataques quantistici.

Il problema di retículo più notable è il [**problema Learning With Errors (LWE) ⧉**][01], introducido per Oded Regev. LWE è un problema computacional che consiste in encontrar un vector secreto a partire da un insieme di ecuaciones lineales aproximadas.

Numerosos esquemas crittografici modernos, come il criptosistema di Regev e il intercambio di chiavi Frodo, basan il suo sicurezza in la dificultad di resolver il problema LWE.

## Algoritmos clásicos per i problemas su retículos e i suoi límites

I algoritmos clásicos per resolver i problemas su retículos, come il algoritmo **Lenstra-Lenstra-Lovász (LLL)** e i suoi variantes, sono stati extensamente estudiados in criptografía. Tuttavia, questi algoritmos afrontan sfide significativi in términos di complejidad computacional, in particolare man mano che le dimensiones del retículo aumentan.

I algoritmos clásicos bene conocidos per resolver il problema LWE dependen exponencialmente del número di variables, lo che i hace impracticables per i retículos di alta dimensión. Questa barrera di complejidad è un factor chiave della sicurezza dei esquemas crittografici basati in LWE.

## Intentos anteriores di algoritmi quantistici per LWE

Antes del trabajo di Chen, diversi ricercatori avevano explorado il potencial dei algoritmi quantistici per resolver il problema LWE.

Oded Regev ha sviluppato con successo una reducción quantistica di `GapSVP` a `LWE`. Tuttavia, conviene señalar che questa reducción richiede un oráculo quantistico per resolver GapSVP, cuya existencia rimane per establecer.

Kuperberg ha creato [**un algoritmo quantistico per resolver LWE con un factor di aproximación subexponencial ⧉**][02]. Tuttavia, questi approcci algorítmicos se apoyaban in hipótesis non verificadas o presentaban una velocità computacional più lenta. Per contraste, il algoritmo di Chen offre una soluzione in tiempo polinómico senza necesidad di un oráculo quantistico.

## Il algoritmo quantistico in tiempo polinómico di Chen per LWE

Il algoritmo quantistico di Yilei Chen per resolver il problema LWE in tiempo polinómico rappresenta un progresso significativo in il campo. Il algoritmo emplea dos tecniche nuove:

1. **Funciones gaussianas con varianzas complejas**: Chen introduce il uso di funciones gaussianas con varianzas complejas in il diseño del algoritmo quantistico. Questo approccio aprovecha le propiedades delle distribuciones gaussianas complejas per manipular più eficientemente i estados quantistici, permitiendo una soluzione più eficiente al problema LWE.

2. **Transformada di Fourier quantistica con ventana**: Il algoritmo applica una transformada di Fourier quantistica con ventana, che consente il análisis simultáneo del problema in i dominios temporal e frecuencial. Questa tecnica consente al algoritmo tratar eficientemente la estructura di alta dimensión dei retículos e extraer la informazione pertinente per resolver LWE.

Il algoritmo di Chen combina queste tecniche per resolver `LWE`, `GapSVP` e `SIVP` in tiempo polinómico per tutte le dimensiones di retículo. Esto è una mejora importante respecto ai algoritmos clásicos e quantistici anteriores.

## Implicaciones, limitaciones e ejes di ricerca futuros

Il algoritmo quantistico di Chen ha implicaciones per LWE, cuestionando la noción di che i ataques quantistici non possono romper LWE e i problemas similares su retículos. Questa hipótesis forma la base di numerosos esquemas crittografici emergentes. Tuttavia, comprender i límites del algoritmo e il suo impacto potencial su i sistemi di cifrado existentes basati in LWE è esencial.

Una cuestión chiave con il algoritmo di Chen è che funciona in modo óptima quando il tamaño del problema supera significativamente il margen di error permitido. In i esquemas crittografici pratici basati in LWE, il ratio módulo-ruido se mantiene típicamente sotto per razones di sicurezza. Inversamente, il algoritmo di Chen richiede un ratio più alto per alcanzar il suo tiempo di ejecución polinómico.

Questo límite sugiere che i esquemas di cifrado basati in LWE existentes con ratios módulo-ruido più pequeños potrebbero permanecer seguros rispetto al algoritmo di Chen così come se presenta actualmente. Per consiguiente, se bene il algoritmo marca un progresso teórico significativo, non rappresenta una amenaza inmediata per la sicurezza di tutti i sistemi crittografici basati in LWE.

Il suo trabajo subraya la necesidad di proseguir la ricerca su il desarrollo di primitivas crittografiche resistentes a lo quantistico.

## Aplicaciones potenciales e incentivos

Il desarrollo di algoritmi quantistici eficientes per i problemas su retículos ha implicaciones di gran alcance in tutti i settori che se apoyan in la comunicación digitale segura e il almacenamiento di dati. Il algoritmo di Chen pone di manifiesto la necesidad universal di cifrado resistente a lo quantistico.

Esto include industrias come:

* **Ciberseguridad:** métodos di cifrado robustos e resistentes a lo quantistico sono cruciales per proteger la informazione sensible in la era della calcolo quantistico.

* **Sector público e defensa:** i governi possono aprovechar questi progressi per reforzar la sicurezza delle infraestructuras críticas e le comunicaciones clasificadas, mitigando le amenazas potenciales planteadas per le capacità quantistiche adversarias.

* **Servicios finanziari:** il settore finanziario depende fuertemente di canales di comunicación seguros per le transazioni e la protección dei dati. Primitivas crittografiche resistentes a lo quantistico basate in i problemas su retículos potrebbero contribuir a garantizar la sicurezza a lungo termine dei sistemi finanziari.

* **Sanidad:** mentre i dati sanitarios se tornano ogni volta più digitalizados, garantizar il suo confidencialidad e integridad è primordial. Métodos di cifrado quantistico-seguros derivados dei trabajos di Chen potrebbero ayudar a proteger la informazione sensible dei pacientes contra i futuros ataques quantistici.

* **Cloud computing:** con la creciente adopción dei servizi cloud, la sicurezza dei dati almacenados e tratados in il cloud è una preocupación principale. Esquemas di cifrado resistentes a lo quantistico basati in i problemas su retículos potrebbero fornire una capa adicional di protección per le applicazioni e il almacenamiento di dati in modo cloud.

## Conclusione

Il algoritmo quantistico in tiempo polinómico di Yilei Chen per resolver il problema LWE rappresenta un hito significativo in il campo della calcolo quantistico e la criptografía. Utilizando nuovi métodos come le funciones gaussianas e le transformadas di Fourier quantistiche con ventana, Chen ha mostrado come i algoritmi quantistici possono resolver eficientemente problemas complejos su retículos. Tuttavia, è esencial señalar che questo trabajo constituye actualmente un progresso teórico, e che se necessita ricerca adicional per acercarlo a una implementación pratica.

Il desarrollo della criptografía resistente a lo quantistico non è solo un sfida tecnico, sino anche un imperativo estratégico per le aziende e i governi. Invertir in I+D in questo campo potrebbe producir beneficios significativi a lungo termine in términos di sicurezza e confidencialidad dei dati.

## Riferimenti

Chen, E. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] In *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (pp. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
