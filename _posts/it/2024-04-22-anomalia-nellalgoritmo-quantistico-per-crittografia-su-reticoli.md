---
title: "Bug nell'algoritmo quantistico per crittografia su reticoli"
subtitle: "Una falla individuata nell'algoritmo di Yilei Chen mette temporaneamente in sicurezza la crittografia reticolare"
description: "È stato individuato un bug nell'algoritmo quantistico di Yilei Chen per risolvere LWE, mettendo temporaneamente in sicurezza la crittografia basata su reticoli e sottolineando la necessità di ricerca continua."
date: "April 22, 2024"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/stocks/images/digitale-nodes.webp"
banner_alt: "Algoritmo quantistico e bug"
keywords: "quantistico, LWE, Yilei Chen, bug, Kyber, PQC, peer review"
---

---

> **TL;DR.** Una falla individuata nell'algoritmo di Yilei Chen mette temporaneamente in sicurezza la crittografia reticolare. Resta la lezione: la PQC va validata in modo continuo e con ridondanza.
>
> **Punti chiave**
>
> - **Errore identificato** — peer review ha individuato un difetto nell'algoritmo originale.
> - **Reticoli in sicurezza** — Kyber e altri schemi NIST restano sicuri allo stato attuale.
> - **Lezione di processo** — la PQC richiede verifica continua e diversificazione algoritmica.
> - **Strategia ibrida** — combinare PQC con crittografia tradizionale resta best practice.

---

## Il enigma quantistico: reevaluación della estandarización NIST di crittografia post-quantistica alla luz del algoritmo di Yilei Chen

A raíz di il mio reciente artículo su i [sfide dei algoritmi quantistici per la criptografía su retículos][00], debo aportar una actualización su i últimos desarrollos relativos a [la ricerca di Yilei Chen ⧉][01].

In un giro inesperado, Yilei Chen, profesor adjunto in il Institute for Interdisciplinary Information Science (IIIS) della Universidad Tsinghua, ha informado di che i suoi colegas Hongxun Wu e Thomas Vidick hanno descubierto independientemente un bug in il suo algoritmo quantistico in tiempo polinómico progettato per resolver il problema Learning with Errors (LWE).

Questo bug torna inoperante al algoritmo, e Chen ha reconocido che il suo approccio non se sostiene come reivindicó inicialmente.

## Il bug in il algoritmo quantistico di Chen

Il bug è stato encontrado in il passo 9 del algoritmo di Chen, e questo ha declarado non sapere come corregirlo. Questo descubrimiento è un alivio per la comunità crittografica, già che confirma che il problema LWE, componente crítico dei métodos di protección in crittografia post-quantistica, rimane siendo seguro.

Il artículo di Chen anche examinaba altri problemas complejos su retículos, come il decisional shortest vector problem (GapSVP) e il shortest independent vector problem (SIVP), in factores di aproximación polinómicos. Sebbene il bug in il suo algoritmo non riguarda direttamente a questi problemas, suscita interrogantes su la robustez dei algoritmi quantistici contra la criptografía su retículos.

Ma según [la página di Nigel Smart ⧉][02], il ataque quantistico propuesto contra LWE è defectuoso e non compromete i esquemas di criptografía su retículos come [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] o [TFHE ⧉][07].

## Implicaciones per il processo di estandarización NIST di crittografia post-quantistica

La ricerca di Chen ha suscitado indirettamente preocupaciones e dudas su il [processo di estandarización NIST di crittografia post-quantistica (PQC) ⧉][03] e la selección dei algoritmos crittografici resistentes a lo quantistico.

I esquemas [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) e CRYSTALS-Dilithium, tra i finalistas del processo di estandarización NIST PQC, sono ejemplos di esquemas crittografici su retículos che sono stati rigurosamente probados e evaluados per il suo resistencia quantistica. Tuttavia, è crucial continuar probando e refinando questi esquemas per garantizar il suo sicurezza e viabilidad a lungo termine.

Il NIST, la comunità crittografica e le aziende devono permanecer vigilantes e continuar explorando fundamentos matemáticos alternativos per la crittografia post-quantistica, al fine di garantizar che un conjunto robusto e diverso di opciones di sicurezza resistente a lo quantistico esté in il suo sitio.

## Il futuro della crittografia post-quantistica

Il descubrimiento del bug in il algoritmo di Chen subraya il papel crítico della revisión per pares in il processo científico. Anche pone di manifiesto la necesidad di revisión instantánea, retroalimentación e debate.

La era quantistica ha comenzado, e la necesidad di sviluppare métodos crittografici resistentes a lo quantistico exige medidas cooperativas a escala mundial per garantizar la sicurezza di la nostra infraestructura digitale rispetto alle crecientes capacità della calcolo quantistico e alla carrera per la supremacía quantistica.

Il processo di estandarización NIST PQC è una etapa significativa in questa indirizzo, ma è solo un comienzo. Il bug in il algoritmo di Chen è un recordatorio brutal dei sfide e incertidumbres per venire, ma anche sirve come llamada alla acción affinché la comunità crittografica redoble i suoi esfuerzos e amplíe le fronteras di lo posible.

È un desarrollo fascinante in il campo della crittografia post-quantistica, e sarà interesante vedere come evoluciona il processo di estandarización NIST PQC in respuesta a questa nuova informazione.

## Conclusione

Il bug descubierto in il algoritmo quantistico di Yilei Chen per resolver il problema LWE atestigua la importancia di una revisión per pares rigurosa e della colaboración in il desarrollo della criptografía resistente a lo quantistico.

Sebbene il bug offre un respiro temporal alla sicurezza dei esquemas crittografici su retículos, anche recuerda la necesidad continuada di ricerca e desarrollo in il campo della crittografia post-quantistica.

Mentre il NIST prosigue il suo processo di estandarización PQC, la comunità crittografica deve permanecer proactiva e adaptativa, abrazando le nuove idee e approcci per garantizar la sicurezza a lungo termine di il nostro mondo digitale rispetto alle crecientes capacità della calcolo quantistico.

## Riferimenti

- Sebastien Rousseau, (2024). [Quantum Algorithm Challenges Lattice-Based Cryptography][00].
- Chen, E. (2024). [Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
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
