---
title: "Cifratura completamente omomorfica nell'era quantistica bancaria"
subtitle: "Calcolo su dati cifrati come difesa contro le minacce dell'era quantistica"
description: "Come la cifratura completamente omomorfica (FHE) rivoluziona la sicurezza dei dati nel banking e nei servizi finanziari, preservando la privacy contro le minacce dell'era quantistica."
date: "March 25, 2024"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/stocks/images/fully-homomorphic-encryption.webp"
banner_alt: "Cifratura omomorfica e quantum"
keywords: "FHE, cifratura omomorfica, banking, post-quantistica, privacy, calcolo sicuro"
---

---

> **TL;DR.** La cifratura completamente omomorfica permette di calcolare su dati cifrati senza decifrarli. Combinata con la PQC, costituisce una difesa stratificata che preserva la privacy dei dati anche di fronte al calcolo quantistico.
>
> **Punti chiave**
>
> - **Calcolo sicuro** — operazioni aritmetiche su ciphertext senza accesso al plaintext.
> - **Privacy preservata** — il fornitore di calcolo non vede mai i dati in chiaro.
> - **Casi d'uso bancari** — credit scoring delegato, ML su dati sensibili, audit conformi.
> - **Sfide pratiche** — overhead computazionale ancora elevato, ma in calo rapido.

---

Il **cifrado completamente homomórfico (FHE — Fully Homomorphic Encryption)** promete redefinir la sicurezza dei dati in la banca e le finanzas. Permitiendo cálculos su dati cifrados, il FHE protege la confidencialidad rispetto alle amenazas convencionales e quantistiche.

## Introducción

La implementación del FHE in il settore finanziario non è solo teórica; viene convirtiendo in una realidad pratica, transformando i standard di sicurezza e confidencialidad dei dati. Questo artículo explora i usos pratici, le consideraciones normativas, i posibles inconvenientes e i progressi di ricerca del cifrado completamente homomórfico in finanzas e in le applicazioni di intelligenza artificiale (IA).

## Comprender il cifrado completamente homomórfico

### Le bases del cifrado

Il cifrado è un método di transformación di dati legibles (texto chiaro) in un formato ilegible (criptograma) per medio di un algoritmo e una chiave di cifrado. Il objetivo principale è asegurar che solo le partes autorizadas puedan acceder ai dati originales descifrando il criptograma con la ayuda di una chiave di descifrado.

### Métodos di cifrado tradicionales

I métodos di cifrado tradicionales possono categorizarse ampliamente in dos tipos: simétrico e asimétrico. Il cifrado simétrico utilizza una sola chiave allo stesso tempo per il cifrado e il descifrado. Questa eficiencia ha un costo in sicurezza, in particolare quando la distribución delle chiavi plantea problemas. Il cifrado asimétrico, anche llamado criptografía di chiave pública, utilizza dos chiavi: una per il cifrado e altra per il descifrado. Questo método è più seguro ma più lento che il cifrado simétrico.

### I límites del cifrado convencional per il cálculo

Sebbene i métodos tradicionales aseguran eficazmente i dati in reposo o in tránsito, fracasan quando se tratta di efectuar cálculos su dati cifrados. Típicamente, per tratar o analizar dati cifrados, bisogna descifrarlos primero, efectuar le operazioni necesarias e luego tornare a cifrarlos. Questa etapa di descifrado plantea un rischio significativo per la confidencialidad, in particolare in entornos non confiables o di cloud computing.

![divider][divider].class=\"m-10 w-100\"

## Il progresso del cifrado homomórfico

Il **cifrado homomórfico (HE)** resuelve i límites del cifrado convencional. Permite efectuar ciertos cálculos direttamente su i dati cifrados (criptogramas). Il resultado descifrado è idéntico ai dati originales (texto chiaro) dopo di che è statoyan efectuado le stesse operazioni. Il HE se declina in tres grandi variedades: Partially Homomorphic Encryption (PHE), Somewhat Homomorphic Encryption (SHE) e Fully Homomorphic Encryption (FHE).

- **Partially Homomorphic Encryption (PHE):** soporta operazioni ilimitadas di un solo tipo (adición o multiplicación) su i criptogramas.
- **Somewhat Homomorphic Encryption (SHE):** soporta un número limitado di operazioni, combinando adición e multiplicación, ma solo fino a una cierta profundidad.
- **Fully Homomorphic Encryption (FHE):** la forma più avanzada, autorizando operazioni ilimitadas di adición e multiplicación su i criptogramas.

### La ingeniosidad tecnica del FHE

Il FHE reposa su estructuras matemáticas complejas, come la criptografía su retículos. La criptografía su retículos è un tipo di cifrado che utilizza estructuras matemáticas llamadas retículos.

Un retículo è una disposición regular di puntos in il espacio, e la criptografía su retículos se apoya in la dificultad di resolver ciertos problemas matemáticos vinculados a queste estructuras. Esto fa sì che la criptografía su retículos sea segura e resistente ai ataques, incluidos i procedentes dei computer quantistici.

In 2009, Craig Gentry ha sviluppato un método, descrito in il suo artículo [**A Fully Homomorphic Encryption Scheme ⧉**][00], per creare un sistema capaz di efectuar una evaluación homomórfica di il suo propio circuito di descifrado. Questo diseño autorreferencial consente ai esquemas FHE efectuar cálculos arbitrarios su dati cifrados.

### Il processo del algoritmo FHE

![FHE Operational Flow][fhe].class=\"m-10 w-100\"

Il diagrama anterior ilustra il flujo operativo di un algoritmo FHE.

- Il processo di cifrado comienza con i dati in texto chiaro, che se cifran con la ayuda di una chiave di cifrado per generare un criptograma.

- Questi dati cifrados possono entonces someterse a diversos cálculos direttamente su il criptograma mediante un processo conocido come bootstrapping.

- Questa capacità única del FHE consente ai dati permanecer cifrados durante tutto il processo. Una vez efectuadas le operazioni necesarias, il processo di descifrado può reconvertir il criptograma modificado in texto chiaro gracias al esquema FHE.

La vantaggio principale del FHE reside in il suo capacità per efectuar cálculos su il criptograma senza richiedere descifrado, garantizando así il mantenimiento della confidencialidad e la sicurezza dei dati durante tutto il cálculo.

### La resistencia quantistica del FHE

I métodos di cifrado tradicionales sono spesso vulnerables ai algoritmi quantistici. Questi algoritmos possono resolver rapidamente problemas come la factorización di enteros e i logaritmos discretos, che constituyen i fundamentos di questi métodos. Per contraste, il FHE emplea problemas su retículos che se cree difíciles di resolver per computer quantistici. Questa resistencia quantistica hace del FHE un método di cifrado prometedor per la era post-quantistica.

Il FHE su retículos è resistente ai ataques quantistici perché i problemas matemáticos subyacentes, come il Shortest Vector Problem (SVP) e il Closest Vector Problem (CVP), se consideran difíciles di resolver incluso per i computer quantistici. Se bene algoritmi quantistici come il di Shor possono romper i métodos di cifrado tradicionales che reposan in la factorización di grandi números o i logaritmos discretos, non se sabe che ofrezcan vantaggi significative in la resolución dei problemas su retículos. Questa caratteristica hace del FHE su retículos un candidato prometedor per la crittografia post-quantistica.

![divider][divider].class=\"m-10 w-100\"

## Il impacto del FHE in la banca e le finanzas

### Confidencialidad e sicurezza dei dati reforzadas

La applicazione del FHE in il settore finanziario promete un refuerzo significativo della confidencialidad. I bancos possono ora emprender evaluaciones di rischi, la detección di fraude e análisis di dati completi al tiempo che garantiscono la confidencialidad absoluta della informazione dei clienti. Questo progresso tecnológico mitiga il rischio di brechas di dati, reforzando la integridad delle piattaforme bancarie digitali e le transazioni finanziarie.

### Cloud computing e externalización

Un ámbito di applicazione principale del cifrado homomórfico è il tratamiento seguro dei dati in la nube. I bancos possono aprovechar i servizi di cloud computing per tratar dati cifrados senza comprometer il suo confidencialidad. Esto consente alle istituzioni finanziarie aprovechar la escalabilidad e la rentabilidad del cloud al tiempo che mantienen la confidencialidad di informazione finanziaria sensible.

Il movimiento verso il cloud computing e la externalización di tareas computacionales per parte dei bancos subraya la pertinencia del FHE. Con un cloud computing seguro, le istituzioni finanziarie possono acceder a recursos externos al tiempo che protegen i dati cifrados sensibles mediante il FHE. Il FHE consente ai bancos aprovechar i servizi cloud in modo segura al tiempo che se garantisce che i dati cifrados sensibles permanezcan protegidos in tutto momento.

![divider][divider].class=\"m-10 w-100\"

## Prepararse per il futuro quantistico

Il advenimiento inminente della calcolo quantistico anuncia una potencial crisis per le metodologías di cifrado tradicionales. Il FHE su retículos è intrínsecamente resistente ai ataques quantistici, ofreciendo una defensa robusta contra la amenaza che la calcolo quantistico plantea alla sicurezza dei dati.

### Cifrado resistente a lo quantistico

Il FHE fornisce una capa formidable di protección contra le amenazas della calcolo quantistico. Empleando tecniche crittografiche su retículos, il FHE garantisce che i dati finanziari e i activos permanezcan seguros incluso rispetto a adversarios quantistici.

La resistencia quantistica del FHE è dovuto a problemas matemáticos subyacentes complejos come il Shortest Vector Problem (SVP) e il Closest Vector Problem (CVP). Se supone che questi problemas sono intratables incluso per i computer quantistici, lo che hace del FHE su retículos un candidato ideal per la crittografia post-quantistica.

Utilizar un cifrado resistente a lo quantistico, come il FHE, è crucial non solo per proteger i activos finanziari sino anche per mantener la confianza dei clienti in la era digitale. A medida che la calcolo quantistico progresa, le istituzioni finanziarie che prioricen un cifrado robusto saranno mejor posicionadas per navegar i sfide e oportunidades futuros.

![divider][divider].class=\"m-10 w-100\"

## Il futuro del FHE in la banca e le finanzas

La trayectoria del FHE all'interno dil settore finanziario è prometedora, ma ancora afronta sfide. Il settore bancario può explotar il pleno potencial del FHE mejorando la tecnologia, integrándola in le operazioni finanziarie cotidianas e cooperando con i reguladores.

Il FHE può utilizarse in diversas applicazioni bancarie e finanziarie, come:

- **Análisis seguro di dati finanziari**: il FHE consente ai bancos analizar dati finanziari cifrados come transazioni, puntuaciones di crédito e carteras di inversión, senza comprometer la confidencialidad del cliente, garantizando un tratamiento seguro della informazione sensible.

- **Aprendizaje automático preservando la confidencialidad**: il FHE consente ai bancos entrenar e desplegar modelli di machine learning su dati cifrados, permitiéndoles aprovechar la IA per la detección di fraude, la evaluación di rischi e la segmentación di clienti allo stesso tempo che mantienen la confidencialidad.

- **Cálculo multipartícipe seguro**: il FHE consente una colaboración segura tra diverse istituzioni finanziarie, permitiéndoles efectuar cálculos conjuntos su dati cifrados senza compartir informazione sensible, facilitando le transazioni interbancarias seguras e il conformità.

- **Seguridad delle API**: il FHE può asegurar le API cifrando i dati sensibles prima della transmisión, garantizando che la informazione dei clienti permanezca confidencial durante i intercambios tra bancos e servizi terceros.

- **Cloud computing seguro**: il FHE consente ai bancos externalizar in modo segura i cálculos e il almacenamiento di dati verso piattaforme cloud senza comprometer la confidencialidad, già che i dati permanecen cifrados durante tutto il processo, ampliando il uso di servizi cloud rentables e escalables.

- **Cumplimiento normativo preservando la confidencialidad**: il FHE consente ai bancos compartir dati cifrados con le autoridades reguladoras, permitiendo il conformità delle exigencias di reporting senza exponer informazione sensible, simplificando il processo di conformità al tiempo che se mantiene la confidencialidad.

Queste applicazioni revelan il potere transformador del FHE in la banca e le finanzas e subrayan il suo potencial per revolucionar i standard di sicurezza e confidencialidad.

![divider][divider].class=\"m-10 w-100\"

## Superar i sfide di adopción del FHE

### Desafíos di prestazioni e optimización

Abordar il sobrecoste computacional intrínseco al FHE rimane siendo un sfida pivote. I recientes progresos in optimización di algoritmos e in desarrollo di aceleradores di hardware especializados reducen la brecha di prestazioni tra il cálculo tradicional e il FHE.

### Estandarización e colaboración

La vía verso una adopción generalizada del FHE depende della estandarización dei protocolos e di una colaboración reforzada tra le partes interesadas del ecosistema finanziario. Un approccio unificado per abrazar il FHE può acelerar significativamente il suo integración con i servizi finanziari generalistas.

### Regolamentazione e conformità

I organismos reguladores desempeñan un papel crítico in la adopción del FHE, con leyes su la confidencialidad dei dati che imponen il suo uso. Un impulso normativo potrebbe servire come catalizador per la adopción completa del FHE in tutta la industria bancaria e finanziaria, allo stesso tempo che se garantisce il conformità delle normativas di protección di dati.

Il panorama normativo attorno alla confidencialidad e la sicurezza dei dati desempeña un papel significativo in la adopción del FHE in il settore bancario. Normativas estrictas come il RGPD (General Data Protection Regulation) e il CCPA (California Consumer Privacy Act) imponen medidas robustas di protección di dati e subrayan il diritto individual alla vida privada. Il FHE, con il suo capacità per tratar dati cifrados senza descifrado, se alinea bene con la orientación centrada in la confidencialidad di queste normativas. A medida che le leyes su la confidencialidad se tornano più estrictas, il FHE offre una soluzione convincente che consente ai bancos efectuar i cálculos e análisis necesarios al tiempo che se respetan le exigencias di conformità.

![divider][divider].class=\"m-10 w-100\"

## Asegurar i grandi modelli di linguaggio con il FHE

I grandi modelli di linguaggio (LLM) sono potentes strumenti di IA. Ma il suo uso suscita preocupaciones di confidencialidad, in particolare quando tratan dati di utente sensibles. Il FHE offre una soluzione che protege la confidencialidad del utente e preserva la propiedad intelectual dei propietarios di modelli permitiendo cálculos su dati cifrados.

### Desafíos di confidencialidad con i LLM

Desplegar un LLM in locale per mantener la confidencialidad dei dati plantea sfide come costi elevados e la exposición potencial di una propiedad intelectual valiosa. Il FHE aborda questi sfide permitiendo ai LLM funcionar su dati di utente cifrados, garantizando la confidencialidad e la sicurezza del modello simultáneamente.

### Il approccio LLM cifrado di Zama

[**Zama ⧉**][01], una azienda di tecnologie di confidencialidad, ha demostrado la viabilidad di costruire un LLM cifrado con la ayuda del FHE. Il suo approccio, che combina FHE e altre tecnologie che refuerzan la confidencialidad, alcanza rendimientos comparables ai modelli non cifrados con solo un aumento modesto del sobrecoste computacional.

### Mejorar la confidencialidad del utente con LLM cifrados

La integración del FHE con i LLM ha il potencial di transformar la confidencialidad del utente, in particolare in le applicazioni che tratan informazione personal o profesional sensible. A medida che la IA se concentra più in la confidencialidad, è importante che sviluppatori, utenti e reguladores trabajen juntos. Questa colaboración è chiave per costruire un ecosistema di IA che ponga la sicurezza e la confidencialidad in primer lugar.

![divider][divider].class=\"m-10 w-100\"

## Conclusione

Il **cifrado completamente homomórfico (FHE)** è una tecnologia di sicurezza dei dati revolucionaria che offre una confidencialidad e una sicurezza excepcionales alla banca e le finanzas.

A medida che la calcolo quantistico avanza, il FHE se torna ancora più crucial. Il suo adopción remodelará la ciberseguridad in i servizi finanziari, haciendo la banca digitale più digna di confianza e più segura in il nostro mondo ogni volta più conectado.

Il advenimiento del FHE anche ha aperto nuove posibilidades di uso seguro e privado dei grandi modelli di linguaggio. Permitiendo LLM cifrados, il FHE garantisce che i dati del utente permanezcan confidenciales al tiempo che se benefician delle capacità avanzadas di questi modelli.

La era della calcolo quantistico se aproxima. I bancos devono evaluar proactivamente il suo infraestructura di cifrado, identificare le vulnerabilidades potenciales e sviluppare una roadmap chiara per la adopción del FHE al fine di proteger i dati e mantener la confianza del cliente.

[00]: https://crypto.stanford.edu/craig/ "The original paper by Craig Gentry on Fully Homomorphic Encryption"
[01]: https://zama.ai/ "Zama - Fully Homomorphic Encryption"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[fhe]: https://cloudcdn.pro/stocks/diagrams/fhe_algorithm_diagram.webp "FHE Architecture"
