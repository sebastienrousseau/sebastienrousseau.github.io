---
title: "Kvantgitterkrypto: fel i Chens LWE-attack"
subtitle: "Peer review avslöjar ett fel i Chens uppmärksammade arbete"
description: "Ett fel i Yilei Chens kvant-LWE-algoritm ger gitterbaserad kryptografi ett tillfälligt andrum. Vad det betyder för CRYSTALS-Kyber, Dilithium och färdplanen för PQC."
date: "April 22, 2024"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Bild genererad med MidJourney: ett nätverk av digitala noder i röda och blå toner."
keywords: "postkvantkryptografi, NIST, PQC-standardisering, Yilei Chen, kvantalgoritm, gitterbaserad kryptografi, LWE-problemet, CRYSTALS-KYBER, CRYSTALS-Dilithium, kvantresistent kryptografi"
---

## Kvantgåtan: en omvärdering av NIST:s standardisering av postkvantkryptografi i ljuset av Yilei Chens algoritm

Efter min nyligen publicerade artikel om [utmaningarna med kvantalgoritmer för gitterbaserad kryptografi][00] vill jag lämna en uppdatering om den senaste utvecklingen i [Yilei Chens forskning ⧉][01].

I en oväntad vändning har Yilei Chen, biträdande professor vid Tsinghua-universitetets Institute for Interdisciplinary Information Science (IIIS), rapporterat att forskarkollegorna Hongxun Wu och Thomas Vidick oberoende av varandra har upptäckt ett fel i hans kvantalgoritm i polynomisk tid, utformad för att lösa problemet Learning with Errors (LWE).

Felet gör algoritmen obrukbar, och Chen har medgett att hans metod inte håller på det sätt han först hävdade.

## Felet i Chens kvantalgoritm

Felet upptäcktes i steg 9 i Chens algoritm, och han har uppgett att han inte vet hur det ska åtgärdas. Upptäckten är en lättnad för den kryptografiska gemenskapen, eftersom den bekräftar att LWE-problemet, en kritisk komponent i postkvantkryptografins skyddsmetoder, förblir säkert.

Chens artikel undersökte även andra komplexa gitterproblem, såsom decisional shortest vector problem (GapSVP) och shortest independent vector problem (SIVP), inom polynomiska approximationsfaktorer. Även om felet i hans algoritm inte direkt påverkar dessa problem väcker det frågor om robustheten hos kvantalgoritmer för gitterbaserad kryptografi.

Men enligt [Nigel Smarts sida ⧉][02] är den föreslagna kvantattacken mot LWE bristfällig och äventyrar inte gitterkryptografiska system som [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06] eller [TFHE ⧉][07].

## Konsekvenser för NIST:s standardiseringsprocess för postkvantkryptografi

Chens forskning väckte indirekt oro och tvivel kring [NIST:s standardiseringsprocess för postkvantkryptografi (PQC) ⧉][03] och urvalet av kvantresistenta kryptografiska algoritmer.

Systemen [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) och CRYSTALS-Dilithium, som hör till finalisterna i NIST:s PQC-standardiseringsprocess, är exempel på gitterbaserade kryptografiska system som har testats och utvärderats noggrant med avseende på kvantresistens. Det är dock avgörande att fortsätta testa och förfina dessa system för att säkerställa deras säkerhet och livskraft på lång sikt.

NIST, den kryptografiska gemenskapen och företagen måste förbli vaksamma och fortsätta utforska alternativa matematiska grundvalar för postkvantkryptografi, så att det finns en robust och mångsidig uppsättning alternativ för kvantresistent säkerhet på plats.

## Framtiden för postkvantkryptografi

Upptäckten av felet i Chens algoritm understryker peer reviewens avgörande roll i den vetenskapliga processen. Den belyser också behovet av omedelbar granskning, återkoppling och debatt.

Kvanteran har inletts, och behovet av att utveckla kvantresistenta kryptografiska metoder kräver samordnade åtgärder på global nivå för att trygga säkerheten i vår digitala infrastruktur inför en allt kraftfullare kvantberäkning och kapplöpningen mot kvantöverlägsenhet.

NIST:s PQC-standardiseringsprocess är ett betydande steg i den riktningen, men den är bara en början. Felet i Chens algoritm är en skarp påminnelse om de utmaningar och den osäkerhet som ligger framför oss, men det är också en uppmaning till den kryptografiska gemenskapen att fördubbla sina ansträngningar och flytta fram gränserna för det möjliga.

Detta är en fascinerande utveckling inom postkvantkryptografin, och det ska bli intressant att se hur NIST:s PQC-standardiseringsprocess utvecklas till följd av denna nya information.

## Slutsats

Felet som upptäckts i Yilei Chens kvantalgoritm för att lösa LWE-problemet visar tydligt hur viktig noggrann peer review och samverkan är för utvecklingen av kvantresistent kryptografi.

Även om felet ger de gitterbaserade kryptografiska systemens säkerhet ett tillfälligt andrum, påminner det också om det fortsatta behovet av forskning och utveckling inom postkvantkryptografin.

När NIST fortsätter sin PQC-standardiseringsprocess måste den kryptografiska gemenskapen förbli proaktiv och anpassningsbar och ta till sig nya idéer och angreppssätt för att trygga den långsiktiga säkerheten i vår digitala värld inför en allt kraftfullare kvantberäkning.

## Referenser

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
