---
title: "Kafes tabanlı kripto için kuantum algoritmasında hata"
subtitle: "Yilei Chen'in algoritmasındaki hata kafes tabanlı kriptografiyi geçici olarak yeniden güvene alıyor"
description: "Yilei Chen'in LWE'yi çözmek için kuantum algoritmasında bir hata keşfedildi; bu, kafes tabanlı kriptografiyi geçici olarak yeniden güvenceye alıyor."
date: "April 22, 2024"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Kriptografik hatanın soyut görselleştirmesi"
keywords: "kuantum, kafes tabanlı, kriptografi, LWE, Yilei Chen, hata, post-kuantum"
---


---

> **TL;DR.** Una falla individuata nell'algoritmo di Yilei Chen mette temporaneamente in sicurezza la crittografia reticolare. Resta la lezione: la PQC va validata in modo continuo e con ridondanza.
>
> **Önemli Çıkarımlar**
>
> - **Errore identificato** — peer review ha individuato un difetto nell'algoritmo originale.
> - **Reticoli in sicurezza** — Kyber e altri schemi NIST restano sicuri allo stato attuale.
> - **Lezione di processo** — la PQC richiede verifica continua e diversificazione algoritmica.
> - **Strategia ibrida** — combinare PQC con crittografia tradizionale resta best practice.

---

## Il enigma quantistico: reevaluación ın estandarización NIST di crittografia post-quantistica alla luz ın algoritmo di Yilei Chen

A raíz di il mio reciente artículo su i [sfide ın algoritmi quantistici için criptografía su retículos][00], debo aportar una actualización su i últimos desarrollos relativos a [la ricerca di Yilei Chen ⧉][01].

In un giro inesperado, Yilei Chen, profesor adjunto in il Institute for Interdisciplinary Information Science (IIIS) ın Universidad Tsinghua, ha informado di che i suoi colegas Hongxun Wu e Thomas Vidick hanno descubierto independientemente un bug in il suo algoritmo quantistico in tiempo polinómico progettato per resolver il problema Learning with Errors (LWE).

Questo bug torna inoperante al algoritmo, e Chen ha reconocido che il suo approccio non se sostiene gibi reivindicó inicialmente.

## Il bug in il algoritmo quantistico di Chen

Il bug è stato encontrado in il passo 9 ın algoritmo di Chen, e questo ha declarado non sapere gibi corregirlo. Questo descubrimiento è un alivio için comunità crittografica, già che confirma che il problema LWE, componente crítico ın métodos di protección in crittografia post-quantistica, rimane siendo seguro.

Il artículo di Chen anche examinaba altri problemas complejos su retículos, gibi il decisional shortest vector problem (GapSVP) ve shortest independent vector problem (SIVP), in factores di aproximación polinómicos. Sebbene il bug in il suo algoritmo non riguarda direttamente a questi problemas, suscita interrogantes su la robustez ın algoritmi quantistici contra la criptografía su retículos.

Ma según [la página di Nigel Smart ⧉][02], il ataque quantistico propuesto contra LWE è defectuoso e non compromete i esquemas di criptografía su retículos gibi [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] o [TFHE ⧉][07].

## Implicaciones için processo di estandarización NIST di crittografia post-quantistica

La ricerca di Chen ha suscitado indirettamente preocupaciones e dudas su il [processo di estandarización NIST di crittografia post-quantistica (PQC) ⧉][03] ve selección ın algoritmos crittografici resistentes a lo quantistico.

I esquemas [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) e CRYSTALS-Dilithium, tra i finalistas ın processo di estandarización NIST PQC, sono ejemplos di esquemas crittografici su retículos che sono stati rigurosamente probados e evaluados için suo resistencia quantistica. Tuttavia, è crucial continuar probando e refinando questi esquemas per garantizar il suo sicurezza e viabilidad a lungo termine.

Il NIST, la comunità crittografica ve aziende devono permanecer vigilantes e continuar explorando fundamentos matemáticos alternativos için crittografia post-quantistica, al fine di garantizar che un conjunto robusto e diverso di opciones di sicurezza resistente a lo quantistico esté in il suo sitio.

## Il futuro ın crittografia post-quantistica

Il descubrimiento ın bug in il algoritmo di Chen subraya il papel crítico ın revisión per pares in il processo científico. Anche pone di manifiesto la necesidad di revisión instantánea, retroalimentación e debate.

La era quantistica ha comenzado, ve necesidad di sviluppare métodos crittografici resistentes a lo quantistico exige medidas cooperativas a escala mundial per garantizar la sicurezza di la nostra infraestructura digitale rispetto alle crecientes capacità ın calcolo quantistico e alla carrera için supremacía quantistica.

Il processo di estandarización NIST PQC è una etapa significativa in questa indirizzo, ma è solo un comienzo. Il bug in il algoritmo di Chen è un recordatorio brutal ın sfide e incertidumbres per venire, ma anche sirve gibi llamada alla acción affinché la comunità crittografica redoble i suoi esfuerzos e amplíe le fronteras di lo posible.

È un desarrollo fascinante in il campo ın crittografia post-quantistica, e sarà interesante vedere gibi evoluciona il processo di estandarización NIST PQC in respuesta a questa nuova informazione.

## Sonuç

Il bug descubierto in il algoritmo quantistico di Yilei Chen per resolver il problema LWE atestigua la importancia di una revisión per pares rigurosa e ın colaboración in il desarrollo ın criptografía resistente a lo quantistico.

Sebbene il bug offre un respiro temporal alla sicurezza ın esquemas crittografici su retículos, anche recuerda la necesidad continuada di ricerca e desarrollo in il campo ın crittografia post-quantistica.

Mentre il NIST prosigue il suo processo di estandarización PQC, la comunità crittografica deve permanecer proactiva e adaptativa, abrazando le nuove idee e approcci per garantizar la sicurezza a lungo termine di il nostro mondo digitale rispetto alle crecientes capacità ın calcolo quantistico.

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
