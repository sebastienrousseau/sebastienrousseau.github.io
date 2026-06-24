---
title: "Il reset della crittografia quantistica nel 2026: standard PQC, garanzia QKD e il lavoro di migrazione che le banche non possono più rimandare"
subtitle: "La crittografia quantistica è passata dalla prospettiva alla disciplina di implementazione: gli standard NIST PQC sono pronti, la guida del NCSC britannico ha ristretto le scelte di algoritmo, il lavoro protocollare dell'IETF è ancora in maturazione, e la garanzia QKD passa dalla fiducia di laboratorio al linguaggio della certificazione."
description: "La crittografia quantistica nel 2026 non è più un dibattito su quando arriveranno i computer quantistici. È un programma di migrazione che attraversa la crittografia post-quantum, la crypto-agility, la garanzia della distribuzione quantistica di chiavi, gli standard di protocollo, la maturità dei fornitori e i dati finanziari di lunga durata già esposti al rischio «harvest-now-decrypt-later»."
date: "May 18, 2026"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/stocks/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Mappa di migrazione verso una crittografia resistente al quantum per il 2026 — standard NIST PQC, lavoro sui protocolli ibridi, garanzia QKD, crypto-agility e livelli di rischio dei dati bancari"
keywords: "crittografia quantistica 2026, crittografia post-quantum, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, scambio di chiavi ibrido, QKD, ETSI QKD, ISO IEC 23837, crypto-agility, harvest now decrypt later, HNDL, crittografia per i servizi finanziari, sicurezza bancaria"
tags: "crittografia quantistica, crittografia post-quantum, PQC, NIST, FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC, IETF, TLS, IPsec, QKD, ETSI, crypto-agility, HNDL, sicurezza bancaria"
item_title: "Il reset della crittografia quantistica nel 2026: standard PQC, garanzia QKD e il lavoro di migrazione che le banche non possono più rimandare"
item_description: "Il reset della crittografia quantistica 2026 — standard NIST PQC, raccomandazioni di migrazione del NCSC, maturità protocollare dell'IETF, garanzia QKD, crypto-agility e cosa dovrebbero prioritizzare le banche questa settimana."
twitter_title: "Crittografia quantistica 2026: standard PQC e migrazione bancaria"
twitter_description: "Il reset della crittografia quantistica 2026 — standard NIST PQC, raccomandazioni di migrazione del NCSC, maturità protocollare dell'IETF, garanzia QKD, crypto-agility e cosa dovrebbero prioritizzare le banche questa settimana."
---

# Il reset della crittografia quantistica nel 2026: standard PQC, garanzia QKD e il lavoro di migrazione che le banche non possono più rimandare

La crittografia quantistica nel 2026 si è divisa in due percorsi pratici. La crittografia post-quantum è ormai un programma di implementazione, perché il NIST afferma che tre standard post-quantum sono pronti all'uso e i sistemi federali devono trattarli come standard FIPS ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); la distribuzione quantistica di chiavi sta diventando un problema di garanzia e certificazione, perché le implementazioni QKD richiedono linguaggio di valutazione, profili di protezione e standard operativi, e non solo dimostrazioni di laboratorio ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI pubblica un profilo di protezione QKD")).

---

> **Sintesi esecutiva / Punti chiave**
>
> - **Il NIST ha portato la PQC in fase di implementazione.** Gli standard correnti sono FIPS 203 per lo stabilimento di chiavi ML-KEM, FIPS 204 per le firme ML-DSA e FIPS 205 per le firme SLH-DSA, con il NIST che esorta le organizzazioni a identificare la crittografia vulnerabile e avviare subito la migrazione ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **Il NCSC britannico ha ristretto le scelte pratiche.** Raccomanda ML-KEM-768 e ML-DSA-65 per la maggior parte dei casi d'uso, avvertendo che i sistemi devono affidarsi a implementazioni robuste degli standard finali, non a esperimenti compatibili con bozze ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")).
> - **La maturità dei protocolli è disomogenea.** L'IETF sta aggiornando TLS e IPsec per PQC e scambio di chiavi ibrido, ma il NCSC avverte che i sistemi operativi dovrebbero preferire RFC pubblicati a Internet Draft in evoluzione ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")).
> - **L'ibrido è un meccanismo di transizione, non uno stato finale.** Gli schemi ibridi chiave pubblica più post-quantum aiutano a scaglionare la migrazione e a coprire il rischio di implementazione, ma aggiungono complessità e possono richiedere una seconda migrazione verso il solo-PQC in seguito ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")).
> - **QKD non è un sostituto della PQC.** Il QKD può servire collegamenti specializzati ad alta garanzia, ma la sua rilevanza bancaria dipende da certificazione, interoperabilità, costo operativo e integrazione con i sistemi di gestione delle chiavi esistenti, non dalla sola fisica ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI pubblica un profilo di protezione QKD")).
> - **La domanda a livello di banca è l'inventario.** Un'istituzione finanziaria che non localizza RSA, ECDH, ECDSA, EdDSA, crittografia VPN proprietaria, template HSM, durate dei certificati e crittografia gestita dai fornitori non può migrare, qualunque sia lo standard disponibile.
> - **Il rischio è già attivo.** Gli attacchi harvest-now-decrypt-later rendono vulnerabili oggi i dati finanziari di lunga durata, prima che esistano computer quantistici crittograficamente rilevanti, perché all'avversario basta raccogliere il testo cifrato oggi.
> - **La crypto-agility è il controllo duraturo.** L'architettura vincente non è un singolo cambio da RSA a ML-KEM; è una capacità di piattaforma di ruotare algoritmi, parametri, librerie, certificati, policy hardware e modalità di protocollo senza ricostruire la banca.
>
---

## Perché questa settimana conta

La conversazione sugli standard ha superato il punto dell'astrazione. La guida pubblica del NIST dice che le organizzazioni devono iniziare ad applicare i nuovi standard ora, identificare dove si usano algoritmi vulnerabili e pianificare gli aggiornamenti di prodotti, servizi e protocolli ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Questo linguaggio conta perché trasforma la PQC da tema di ricerca in dipendenza di rinnovo tecnologico.

Anche il calendario conta perché i dati finanziari hanno un'emivita di riservatezza lunga. Materiali M&A, flussi di tesoreria, indagini sulle sanzioni, documenti di identità dei clienti, metadati di instradamento dei pagamenti e registri di settlement wholesale possono restare sensibili per anni. Il computer quantistico che rompe la crittografia classica a chiave pubblica non deve esistere oggi perché l'esposizione sia razionale oggi.

## La base crittografica 2026: quattro filoni di lavoro

### 1. Gli standard PQC sono abbastanza pronti per pianificare

La prima base è algoritmica. Il programma PQC del NIST offre ora ai responsabili tecnologici obiettivi nominati: ML-KEM per lo stabilimento di chiavi, ML-DSA per firme digitali generali e SLH-DSA per firme basate su hash ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")). L'impatto pratico è che i team di procurement, architettura e gestione fornitori possono smettere di chiedere se esisteranno standard PQC e iniziare a chiedere quando ogni sistema li supporterà.

Il punto più delicato è la compatibilità. Il NCSC avverte che le implementazioni basate su bozze possono non essere compatibili con gli standard finali, esattamente il tipo di dettaglio che fa deragliare le migrazioni nelle grandi banche se ignorato ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")). Le banche dovrebbero quindi separare pilot sperimentali da traiettorie di migrazione in produzione.

### 2. I protocolli sono il collo di bottiglia

Gli algoritmi da soli non proteggono il traffico bancario. TLS, IPsec, SSH, S/MIME, API di pagamento, integrazioni HSM e stack di gestione dei certificati hanno bisogno di supporto a livello di protocollo. Il NCSC afferma che l'IETF sta aggiornando protocolli ampiamente usati come TLS e IPsec affinché gli algoritmi PQC possano essere incorporati nei meccanismi di scambio di chiavi e firma ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")).

Ciò crea un problema di implementazione a fasi. Una banca può inventariare la crittografia subito, esigere roadmap dai fornitori subito e progettare la crypto-agility subito, ma potrebbe ancora dover attendere implementazioni protocollari stabili prima di spostare canali di produzione ad alta criticità.

### 3. Il QKD diventa disciplina di garanzia

La distribuzione quantistica di chiavi rimane rilevante per collegamenti altamente specializzati, in particolare quando l'istituzione controlla endpoint e rotte di rete. Lo sviluppo importante del 2026 non è una nuova scatola QKD; è la comparsa di un linguaggio di certificazione, con ETSI GS QKD 016 descritto come una pietra miliare di profilo di protezione per la valutazione di prodotti QKD ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI pubblica un profilo di protezione QKD")).

Per le banche ciò sposta la conversazione di acquisto. La domanda corretta non è più se il QKD sia quantum-sicuro in linea di principio. La domanda corretta è se il dispositivo, l'integrazione, il processo di gestione delle chiavi, l'ambiente operativo e l'evidenza di certificazione soddisfino il modello di minaccia della banca.

### 4. La crypto-agility è l'architettura

La crypto-agility è la capacità di cambiare algoritmi senza cambiare l'intero sistema. Copre librerie software, negoziazione di protocollo, policy HSM, profili dei certificati, durate delle chiavi, servizi di firma, evidenze di audit e percorsi di rollback. Senza, ogni migrazione crittografica diventa un progetto su misura.

Questa è la lezione architetturale centrale. La transizione post-quantum non sarà l'ultima transizione crittografica che il sistema finanziario affronterà. Le banche che costruiscono crypto-agility ora ottengono un control plane riutilizzabile per aggiornamenti di algoritmi, rischio fornitore, revoca d'emergenza ed evidenza per il regolatore.

## Cosa devono fare le banche ora

### Costruire l'inventario degli asset crittografici

Il primo deliverable è una bill of materials crittografica. Deve includere algoritmi a chiave pubblica, lunghezze di chiave, autorità di certificazione, template HSM, versioni TLS, prodotti VPN, gateway di pagamento, API di terze parti, SDK mobili, wrapper di crittografia dei dati a riposo, chiavi di firma, processi di firma del firmware e crittografia gestita dai fornitori.

L'inventario deve distinguere riservatezza e autenticità. I dati cifrati di lunga durata sono esposti al rischio harvest-now-decrypt-later, mentre le chiavi di firma di lunga durata creano un rischio futuro di falsificazione se restano ancorate ad algoritmi a chiave pubblica vulnerabili.

### Segmentare per emivita dei dati

Non tutti i dati richiedono lo stesso ordine di migrazione. Un messaggio di autorizzazione carta in tempo reale può avere un'emivita di riservatezza diversa da un'indagine sulle sanzioni, da un file di acquisizione aziendale, da un pack di identità private banking o da un documento di emissione di debito sovrano. Per questo la migrazione quantistica appartiene alla classificazione dei dati tanto quanto alla sicurezza di rete.

La priorità deve andare ai sistemi che proteggono dati di lunga durata con uno stabilimento di chiavi vulnerabile. Sono i sistemi in cui la raccolta di oggi crea l'esposizione di domani.

### Imporre le roadmap dei fornitori nei contratti

Il NIST dice che prodotti, servizi e protocolli hanno bisogno di aggiornamenti per la transizione ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Significa che il linguaggio del procurement deve cambiare. I fornitori devono comunicare tempistiche di supporto PQC, compatibilità con gli standard finali, comportamento in modalità ibrida, vincoli dei moduli hardware, impatti prestazionali, supporto dei profili dei certificati e controlli di fallback.

Un fornitore che dice solo «roadmap quantum-safe» non ha risposto alla domanda. La banca ha bisogno di date, algoritmi, confini di integrazione ed evidenza.

## PQC, QKD e ibrido: una tabella pratica di decisione

| Controllo | Uso migliore | Stato 2026 | Avvertenza bancaria |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Stabilimento di chiavi per riservatezza a prova di futuro | Standardizzato e pronto per la pianificazione dell'implementazione ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Richiede supporto di protocollo e librerie prima del rollout critico in produzione |
| **ML-DSA / FIPS 204** | Firme digitali generali | Raccomandato dal NCSC per la maggior parte dei casi generali di firma ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")) | Le catene di certificati e la migrazione PKI sono operativamente difficili |
| **SLH-DSA / FIPS 205** | Firme basate su hash per firma di firmware e software | Standard NIST finale referenziato dal NCSC ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")) | Firme più grandi possono impattare ambienti vincolati |
| **Schemi ibridi PQ/T** | Migrazione intermedia e interoperabilità | Utile come misura di transizione ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")) | Aggiunge complessità e può richiedere una seconda migrazione |
| **QKD** | Collegamenti specializzati ad alta garanzia | Il lavoro di garanzia matura attraverso l'attività di profilo di protezione ETSI ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI pubblica un profilo di protezione QKD")) | Non risolve l'autenticazione a scala internet né l'inventario crittografico aziendale |

## Cosa significa per tipo di istituzione

### Banche universali di prima fascia

Le banche di prima fascia hanno bisogno di un program office, non di un proof of concept. Il modello operativo target deve combinare inventario crittografico, enforcement sui fornitori, gestione della roadmap HSM, ambienti di test per TLS/IPsec ibridi ed evidenza pronta per il regolatore. Il lavoro iniziale di maggior valore non è cambiare immediatamente ogni cifrario; è costruire il control plane che rende sicuro il cambiamento.

### Banche di fascia intermedia e regionali

Le banche di fascia intermedia dovrebbero trattare la PQC come esercizio di gestione dei fornitori e standardizzazione di piattaforma. Possono evitare costoso lavoro su misura concentrando i sistemi attorno a librerie supportate, stack TLS standard, servizi di certificati gestiti e scadenze chiare per i fornitori. Il rischio chiave è la crittografia nascosta dentro appliance, gateway di pagamento e middleware legacy.

### Fintech, PSP e istituzioni crypto-adiacenti

Le fintech possono muoversi più velocemente perché di solito hanno meno ancore di fiducia ereditate. Il rischio è l'autocompiacimento in API di terze parti, default dei KMS cloud, infrastruttura wallet e integrazioni di custodia. Le società crypto-adiacenti dovrebbero stare particolarmente attente a non confondere narrative di sicurezza native blockchain con prontezza post-quantum.

### Ingegneri e architetti della sicurezza

La disciplina di ingegneria è concreta: aggiungere metadati di algoritmo agli inventari di servizio, registrare le modalità di protocollo negoziate, creare feature flag sicuri per i test ibridi, accorciare le durate dei certificati quando possibile, rimuovere assunzioni di algoritmo hard-coded e rendere la policy crittografica deployabile via configurazione anziché via fork di codice.

## Conclusione

Il reset della crittografia quantistica non è un singolo acquisto tecnologico. È un modello operativo crittografico. Il NIST ha dato all'industria una baseline di standard, il NCSC ha ristretto la guida pratica, gli organismi protocollari sono ancora in movimento e la garanzia QKD si sta formalizzando. Le istituzioni bancarie che vinceranno questa transizione non saranno quelle che annunciano il pilot più grande. Saranno le istituzioni che sanno dove vive la propria crittografia, sanno quali dati hanno bisogno di protezione per primi e possono cambiare le primitive crittografiche senza ricostruire la banca.

## Domande frequenti

**La crittografia post-quantum è pronta per essere usata dalle banche?**

È pronta per pianificazione, ingaggio dei fornitori, pilot e lavoro di implementazione selezionato. Il NIST dice che tre standard sono pronti per essere implementati, mentre il NCSC avverte che l'uso operativo deve basarsi su implementazioni robuste degli standard finali e protocolli stabili ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Prossimi passi per preparare la PQC")).

**Il QKD elimina la necessità della PQC?**

No. Il QKD può essere utile per collegamenti controllati specializzati, ma la PQC è la traiettoria di migrazione scalabile per software generale, protocolli internet, API, certificati e sistemi aziendali. Anche il QKD dipende da framework di garanzia e certificazione prima di poter essere trattato come infrastruttura di livello bancario ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI pubblica un profilo di protezione QKD")).

**Cosa dovrebbe essere migrato per primo?**

Devono essere prioritizzati i sistemi che proteggono dati sensibili di lunga durata. Ciò include la crittografia degli archivi, le indagini sui pagamenti, i documenti di tesoreria e mercati dei capitali, i record di identità del private banking, i file di deal strategici, le autorità di certificazione root, la firma del firmware e i canali interbancari.

**Qual è la più grande trappola di implementazione?**

La più grande trappola è trattare la PQC come uno scambio di algoritmi. La migrazione tocca protocolli, certificati, HSM, fornitori, test di prestazioni, gestione degli incidenti, monitoraggio e governance. Senza crypto-agility, l'istituzione semplicemente ricrea lo stesso problema di migrazione per il prossimo cambio di algoritmo.

## Riferimenti

- NIST, (2025). [Crittografia post-quantum ⧉](https://www.nist.gov/pqc "Post-quantum cryptography").
- NCSC, (2024). [Prossimi passi per preparare la crittografia post-quantum ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC PQC guidance").
- NIST CSRC, (2026). [The NIST Post-Quantum Cryptography Project ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "The NIST PQC Project").
- ID Quantique, (2024). [ETSI pubblica il primo profilo di protezione mondiale per QKD ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
<!-- enrich-start -->
<aside class="author-card" aria-label="Informazioni sull'autore"><img alt="Ritratto di Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastienrousseau.webp" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Senior banking technologist, scrive di IA applicata, migrazione a ISO 20022, crittografia post-quantum per i servizi finanziari e trasformazione strutturale dei pagamenti wholesale.</span><span class="author-credentials">Oltre 20 anni in HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Profilo completo</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Ultima revisione <time datetime="2026-05-18">2026-05-18</time>.</p>
<!-- enrich-end -->
