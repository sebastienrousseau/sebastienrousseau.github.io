---
title: "Resetarea criptografiei cuantice în 2026: standarde PQC, asigurarea QKD și lucrările de migrare pe care băncile nu le mai pot amâna"
subtitle: "Criptografia cuantică a trecut de la analiza de orizont la disciplina de implementare: standardele NIST PQC sunt gata, ghidul NCSC din Marea Britanie a îngustat opțiunile de algoritmi, lucrările protocolare ale IETF sunt încă în maturare, iar asigurarea QKD trece de la încrederea de laborator la limbajul certificării."
description: "Criptografia cuantică în 2026 nu mai este o dezbatere despre iminența calculatoarelor cuantice. Este un program de migrare care traversează criptografia post-cuantică, agilitatea criptografică, asigurarea distribuției cuantice a cheilor, standardele de protocol, pregătirea furnizorilor și datele financiare cu durată lungă de viață deja expuse riscului «harvest-now-decrypt-later»."
date: "May 18, 2026"
language: "ro-RO"
locale: "ro_RO"
banner: "https://cloudcdn.pro/stock/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Hartă a migrării către o criptografie rezistentă la cuantic pentru 2026 — standarde NIST PQC, lucrări asupra protocoalelor hibride, asigurare QKD, agilitate criptografică și niveluri de risc al datelor bancare"
keywords: "criptografie cuantică 2026, criptografie post-cuantică, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, schimb hibrid de chei, QKD, ETSI QKD, ISO IEC 23837, agilitate criptografică, harvest now decrypt later, HNDL, criptografie pentru servicii financiare, securitate bancară"
tags: "criptografie cuantică, criptografie post-cuantică, PQC, NIST, FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC, IETF, TLS, IPsec, QKD, ETSI, agilitate criptografică, HNDL, securitate bancară"
item_title: "Resetarea criptografiei cuantice în 2026: standarde PQC, asigurarea QKD și lucrările de migrare pe care băncile nu le mai pot amâna"
item_description: "Resetarea criptografiei cuantice 2026 — standardele NIST PQC, recomandările de migrare ale NCSC, maturitatea protocolară a IETF, asigurarea QKD, agilitatea criptografică și ce ar trebui să prioritizeze băncile săptămâna aceasta."
twitter_title: "Criptografia cuantică 2026: standarde PQC și migrarea bancară"
twitter_description: "Resetarea criptografiei cuantice 2026 — standardele NIST PQC, recomandările de migrare ale NCSC, maturitatea protocolară a IETF, asigurarea QKD, agilitatea criptografică și ce ar trebui să prioritizeze băncile săptămâna aceasta."
---

# Resetarea criptografiei cuantice în 2026: standarde PQC, asigurarea QKD și lucrările de migrare pe care băncile nu le mai pot amâna

Criptografia cuantică în 2026 s-a împărțit în două direcții practice. Criptografia post-cuantică este acum un program de implementare, pentru că NIST afirmă că trei standarde post-cuantice sunt gata pentru utilizare și că sistemele federale trebuie să le trateze drept standarde FIPS ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); distribuția cuantică a cheilor devine o problemă de asigurare și certificare, deoarece implementările QKD au nevoie de un limbaj de evaluare, profile de protecție și standarde operaționale, nu doar de demonstrații de laborator ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publică un profil de protecție QKD")).

---

> **Rezumat executiv / Concluzii cheie**
>
> - **NIST a trecut PQC în faza de implementare.** Standardele actuale sunt FIPS 203 pentru stabilirea cheilor ML-KEM, FIPS 204 pentru semnături ML-DSA și FIPS 205 pentru semnături SLH-DSA, NIST îndemnând organizațiile să identifice criptografia vulnerabilă și să înceapă migrarea acum ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **NCSC britanic a îngustat opțiunile practice.** Recomandă ML-KEM-768 și ML-DSA-65 pentru majoritatea cazurilor de utilizare, avertizând că sistemele trebuie să se bazeze pe implementări robuste ale standardelor finale, nu pe experimente compatibile cu schițe ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")).
> - **Pregătirea protocolară este neuniformă.** IETF actualizează TLS și IPsec pentru PQC și schimbul hibrid de chei, dar NCSC avertizează că sistemele operaționale ar trebui să prefere RFC-uri publicate în locul Internet Drafts în schimbare ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")).
> - **Hibridul este un mecanism de tranziție, nu o stare finală.** Schemele hibride cu cheie publică plus post-cuantic ajută la eșalonarea migrării și acoperă riscul de implementare, dar adaugă complexitate și pot necesita o a doua migrare către doar-PQC mai târziu ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")).
> - **QKD nu este un înlocuitor al PQC.** QKD poate servi legături specializate cu asigurare ridicată, dar relevanța sa bancară depinde de certificare, interoperabilitate, costul operațional și integrarea cu sistemele existente de gestionare a cheilor, nu doar de fizică ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publică un profil de protecție QKD")).
> - **Întrebarea la nivel de bancă este inventarul.** O instituție financiară care nu poate localiza RSA, ECDH, ECDSA, EdDSA, criptografia proprietară de VPN, șabloanele HSM, duratele de viață ale certificatelor și criptografia gestionată de furnizori nu poate migra, indiferent de standardele disponibile.
> - **Riscul este deja activ.** Atacurile harvest-now-decrypt-later fac ca datele financiare cu durată lungă de viață să fie vulnerabile înainte ca să existe calculatoare cuantice relevante criptografic, pentru că adversarul nu trebuie decât să colecteze textul cifrat astăzi.
> - **Agilitatea criptografică este controlul durabil.** Arhitectura câștigătoare nu este o schimbare punctuală de la RSA la ML-KEM; este capacitatea platformei de a roti algoritmi, parametri, biblioteci, certificate, politici hardware și moduri de protocol fără a reconstrui banca.
>
---

## De ce contează săptămâna aceasta

Conversația despre standarde a depășit punctul abstracției. Ghidul public NIST spune că organizațiile trebuie să înceapă să aplice noile standarde acum, să identifice unde sunt folosiți algoritmi vulnerabili și să planifice actualizările de produse, servicii și protocoale ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Acest limbaj contează pentru că transformă PQC dintr-un subiect de cercetare într-o dependență de înnoire tehnologică.

Calendarul contează și pentru că datele financiare au o semiviață de confidențialitate lungă. Materialele M&A, fluxurile de trezorerie, investigațiile privind sancțiunile, documentele de identitate ale clienților, metadatele de rutare a plăților și înregistrările de decontare wholesale pot rămâne sensibile ani de zile. Calculatorul cuantic care sparge criptografia clasică cu cheie publică nu trebuie să existe astăzi pentru ca expunerea să fie rațională astăzi.

## Baza criptografică 2026: patru fluxuri de lucru

### 1. Standardele PQC sunt destul de pregătite pentru a planifica

Prima bază este algoritmică. Programul PQC al NIST oferă acum liderilor tehnologici ținte nominalizate: ML-KEM pentru stabilirea cheilor, ML-DSA pentru semnături digitale generale și SLH-DSA pentru semnături bazate pe hash ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")). Impactul practic este că echipele de achiziții, arhitectură și management al furnizorilor pot înceta să întrebe dacă vor exista standarde PQC și să înceapă să întrebe când le va sprijini fiecare sistem.

Punctul mai delicat este compatibilitatea. NCSC avertizează că implementările bazate pe standarde în schiță pot să nu fie compatibile cu standardele finale, exact tipul de detaliu care deraiază migrările marilor bănci dacă este ignorat ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")). Băncile ar trebui deci să separe piloturile experimentale de traiectoriile de migrare în producție.

### 2. Protocoalele sunt blocajul

Algoritmii nu securizează singuri traficul bancar. TLS, IPsec, SSH, S/MIME, API-urile de plată, integrările HSM și stivele de management al certificatelor au nevoie de suport la nivel de protocol. NCSC afirmă că IETF actualizează protocoale folosite pe scară largă, precum TLS și IPsec, astfel încât algoritmii PQC să poată fi încorporați în mecanismele de schimb de chei și semnătură ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")).

Asta creează o problemă de implementare în etape. O bancă poate inventaria criptografia imediat, poate cere foi de parcurs furnizorilor imediat și poate proiecta agilitatea criptografică imediat, dar poate avea în continuare nevoie să aștepte implementări protocolare stabile înainte de a muta canalele de producție cu criticitate ridicată.

### 3. QKD devine o disciplină de asigurare

Distribuția cuantică a cheilor rămâne relevantă pentru legături foarte specializate, în special când instituția controlează capetele și rutele de rețea. Dezvoltarea importantă din 2026 nu este o nouă cutie QKD; este apariția unui limbaj de certificare, cu ETSI GS QKD 016 descris ca o piatră de hotar de profil de protecție pentru evaluarea produselor QKD ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publică un profil de protecție QKD")).

Pentru bănci, acest lucru deplasează conversația de achiziție. Întrebarea corectă nu mai este dacă QKD este în principiu sigur cuantic. Întrebarea corectă este dacă dispozitivul, integrarea, procesul de gestionare a cheilor, mediul operațional și dovezile de certificare îndeplinesc modelul de amenințare al băncii.

### 4. Agilitatea criptografică este arhitectura

Agilitatea criptografică este capacitatea de a schimba algoritmi fără a schimba tot sistemul. Acoperă bibliotecile software, negocierea de protocol, politica HSM, profilurile de certificate, duratele de viață ale cheilor, serviciile de semnare, dovezile de audit și căile de rollback. Fără ea, fiecare migrare criptografică devine un proiect făcut la comandă.

Aceasta este lecția arhitecturală centrală. Tranziția post-cuantică nu va fi ultima tranziție criptografică cu care se va confrunta sistemul financiar. Băncile care construiesc agilitate criptografică acum obțin un control plane reutilizabil pentru actualizări de algoritmi, risc de furnizor, revocare de urgență și dovezi pentru regulator.

## Ce trebuie să facă băncile acum

### Construirea inventarului de active criptografice

Primul livrabil este o listă de materiale criptografică. Trebuie să includă algoritmi cu cheie publică, lungimi de cheie, autorități de certificare, șabloane HSM, versiuni TLS, produse VPN, gateway-uri de plată, API-uri de la terți, SDK-uri mobile, învelișuri de criptare a datelor în repaus, chei de semnare, procese de semnare a firmware-ului și criptografia gestionată de furnizori.

Inventarul trebuie să distingă între confidențialitate și autenticitate. Datele criptate cu durată lungă de viață sunt expuse riscului harvest-now-decrypt-later, iar cheile de semnare cu durată lungă de viață creează risc viitor de falsificare dacă rămân ancorate în algoritmi cu cheie publică vulnerabili.

### Segmentarea după semiviața datelor

Nu toate datele au nevoie de aceeași ordine de migrare. Un mesaj de autorizare card în timp real poate avea o semiviață de confidențialitate diferită față de o investigație privind sancțiunile, un dosar de achiziție corporativă, un pachet de identitate de private banking sau un document de emisiune de datorie suverană. De aceea migrarea cuantică aparține clasificării datelor la fel de mult ca securității rețelei.

Prioritatea trebuie să fie sistemele care protejează date cu durată lungă de viață cu o stabilire a cheilor vulnerabilă. Acelea sunt sistemele în care colectarea de astăzi creează expunerea de mâine.

### Forțarea foilor de parcurs ale furnizorilor în contracte

NIST spune că produsele, serviciile și protocoalele au nevoie de actualizări pentru tranziție ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Asta înseamnă că limbajul achizițiilor trebuie să se schimbe. Furnizorii trebuie să dezvăluie termenele de suport PQC, compatibilitatea cu standardele finale, comportamentul în modul hibrid, constrângerile modulelor hardware, impactul asupra performanței, suportul profilurilor de certificate și controalele de fallback.

Un furnizor care spune doar „foaie de parcurs quantum-safe" nu a răspuns la întrebare. Banca are nevoie de date, algoritmi, frontiere de integrare și dovezi.

## PQC, QKD și hibrid: un tabel practic de decizie

| Control | Cea mai bună utilizare | Statut 2026 | Rezervă bancară |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Stabilirea cheilor pentru confidențialitate pe termen lung | Standardizat și gata pentru planificarea implementării ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Necesită suport de protocol și biblioteci înainte de rollout critic în producție |
| **ML-DSA / FIPS 204** | Semnături digitale generale | Recomandat de NCSC pentru majoritatea cazurilor generale de semnătură ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")) | Lanțurile de certificate și migrarea PKI sunt dificile operațional |
| **SLH-DSA / FIPS 205** | Semnături bazate pe hash pentru semnarea firmware-ului și a software-ului | Standard NIST final referențiat de NCSC ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")) | Semnăturile mai mari pot afecta mediile constrânse |
| **Scheme hibride PQ/T** | Migrare intermediară și interoperabilitate | Utile ca măsură de tranziție ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")) | Adaugă complexitate și pot necesita o a doua migrare |
| **QKD** | Legături specializate cu asigurare ridicată | Lucrările de asigurare maturizează prin activitatea de profil de protecție ETSI ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publică un profil de protecție QKD")) | Nu rezolvă autentificarea la scară internet și nici inventarul criptografic de întreprindere |

## Ce înseamnă acest lucru pe tip de instituție

### Băncile universale de prim rang

Băncile de prim rang au nevoie de un program office, nu de un proof of concept. Modelul țintă de operare trebuie să combine inventar criptografic, impunere către furnizori, gestionarea foii de parcurs HSM, medii de testare pentru TLS/IPsec hibrid și dovezi pregătite pentru regulator. Lucrarea timpurie cu cea mai mare valoare nu este schimbarea imediată a fiecărui cifru; este construirea control plane-ului care face schimbarea sigură.

### Băncile mijlocii și regionale

Băncile mijlocii ar trebui să trateze PQC ca pe un exercițiu de gestionare a furnizorilor și de standardizare a platformei. Pot evita lucrări costisitoare făcute la comandă concentrând sistemele în jurul bibliotecilor suportate, stive TLS standard, servicii de certificate gestionate și termene-limită clare pentru furnizori. Riscul cheie este criptografia ascunsă în aparate, gateway-uri de plată și middleware moștenit.

### Fintech-uri, PSP-uri și instituții crypto-adiacente

Fintech-urile pot să se miște mai repede pentru că de obicei au mai puține ancore moștenite de încredere. Riscul este complacența în API-uri terțe, valori implicite KMS în cloud, infrastructură de portofele și integrări de custodie. Firmele crypto-adiacente trebuie să fie deosebit de atente să nu confunde narațiunile de securitate native blockchain cu pregătirea post-cuantică.

### Inginerii și arhitecții de securitate

Disciplina de inginerie este concretă: adăugați metadate de algoritm la inventarele de servicii, jurnalizați modurile de protocol negociate, creați feature flag-uri sigure pentru testele hibride, scurtați duratele de viață ale certificatelor unde este posibil, eliminați presupunerile de algoritm hard-coded și faceți politica criptografică să poată fi implementată prin configurație și nu prin fork-uri de cod.

## Concluzie

Resetarea criptografiei cuantice nu este o achiziție tehnologică unică. Este un model operațional criptografic. NIST a oferit industriei o linie de bază a standardelor, NCSC a îngustat ghidul practic, organismele de protocol sunt încă în mișcare, iar asigurarea QKD se formalizează. Instituțiile bancare care vor câștiga această tranziție nu vor fi cele care anunță cel mai mare pilot. Vor fi instituțiile care știu unde își trăiește criptografia, care știu ce date au nevoie de protecție mai întâi și care pot schimba primitivele criptografice fără a reconstrui banca.

## Întrebări frecvente

**Este criptografia post-cuantică gata pentru a fi folosită de bănci?**

Este gata pentru planificare, angajament cu furnizorii, piloturi și lucrări selectate de implementare. NIST spune că trei standarde sunt gata pentru a fi implementate, în timp ce NCSC avertizează că utilizarea operațională trebuie să se bazeze pe implementări robuste ale standardelor finale și protocoale stabile ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Următorii pași pentru pregătirea PQC")).

**Elimină QKD nevoia de PQC?**

Nu. QKD poate fi util pentru legături controlate specializate, dar PQC este traiectoria de migrare scalabilă pentru software general, protocoale de internet, API-uri, certificate și sisteme de întreprindere. QKD depinde, de asemenea, de cadre de asigurare și certificare înainte de a putea fi tratat ca infrastructură de calitate bancară ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publică un profil de protecție QKD")).

**Ce ar trebui migrat mai întâi?**

Sistemele care protejează date sensibile cu durată lungă de viață ar trebui prioritizate. Aceasta include criptarea arhivelor, investigațiile de plăți, documentele de trezorerie și piețe de capital, înregistrările de identitate de private banking, fișierele de tranzacții strategice, autoritățile de certificare rădăcină, semnarea firmware-ului și canalele interbancare.

**Care este cea mai mare capcană de implementare?**

Cea mai mare capcană este să tratezi PQC ca pe un simplu schimb de algoritmi. Migrarea atinge protocoale, certificate, HSM-uri, furnizori, testare de performanță, răspuns la incidente, monitorizare și guvernanță. Fără agilitate criptografică, instituția pur și simplu recreează aceeași problemă de migrare pentru următoarea schimbare de algoritm.

## Referințe

- NIST, (2025). [Criptografie post-cuantică ⧉](https://www.nist.gov/pqc "Post-quantum cryptography").
- NCSC, (2024). [Următorii pași pentru pregătirea criptografiei post-cuantice ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC PQC guidance").
- NIST CSRC, (2026). [The NIST Post-Quantum Cryptography Project ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "The NIST PQC Project").
- ID Quantique, (2024). [ETSI publică primul profil de protecție mondial pentru QKD ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
<!-- enrich-start -->
<aside class="author-card" aria-label="Despre autor"><img alt="Portret al lui Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Tehnolog bancar senior, scrie despre IA aplicată, migrarea la ISO 20022, criptografie post-cuantică pentru serviciile financiare și transformarea structurală a plăților wholesale.</span><span class="author-credentials">Peste 20 de ani la HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Profil complet</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Ultima revizuire <time datetime="2026-05-18">2026-05-18</time>.</p>
<!-- enrich-end -->
