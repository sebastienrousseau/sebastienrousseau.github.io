---
title: "Sécuriser le registre : guide à l'usage des conseils d'administration sur la migration post-quantique en banque de financement"
subtitle: "Le risque quantique est passé de la curiosité académique à un mandat réglementaire actif. La feuille de route du G7, BIS Project Leap et les calendriers UE/UK/Australie posent désormais la question non plus du quand, mais du comment."
description: "Le risque quantique est passé de la curiosité académique au mandat réglementaire. Avec la feuille de route du G7 de janvier 2026, des calendriers UE, UK et australien désormais clarifiés, et BIS Project Leap qui a fait la démonstration de la faisabilité en système de paiement réel, la question pour les conseils d'administration n'est plus celle de la migration, mais celle des délais."
date: "May 14, 2026"
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp"
banner_alt: "Porte de coffre ouverte baignée de lumière dorée — métaphore visuelle de la protection cryptographique des archives financières"
keywords: "cryptographie post-quantique, ML-KEM, ML-DSA, FIPS 203, FIPS 204, BIS Project Leap, G7 CEG, NCSC, ANSSI, BSI, ASD, CNSA 2.0, agilité cryptographique, banque de financement, paiements wholesale"
---

Le risque quantique est passé de la curiosité académique au mandat réglementaire actif. Avec la feuille de route du G7 publiée en janvier 2026, les calendriers de l'UE, du Royaume-Uni et de l'Australie désormais clarifiés, et BIS Project Leap qui a fait la démonstration de la faisabilité en système de paiement réel, la question pour les conseils d'administration n'est plus de savoir s'il faut migrer — c'est de savoir si la migration peut être achevée avant que la durée de conservation cryptographique des données d'aujourd'hui n'expire.

---

> **Points clés**
>
> - **2026 est l'année où la posture réglementaire s'est durcie.** La feuille de route de janvier du Cyber Expert Group du G7, le calendrier coordonné du Groupe de coopération NIS de l'UE et le plan en trois phases du NCSC britannique ont fait passer la conversation de la sensibilisation à l'exécution. L'Australian Signals Directorate va plus loin encore en fixant une date butoir ferme à 2030 pour la cryptographie asymétrique classique.
> - **L'exposition est asymétrique.** RSA, ECC et Diffie–Hellman constituent le problème immédiat — les algorithmes asymétriques qui sous-tendent les poignées de main SWIFT, TLS, les PKI, la signature de code et l'authentification des réseaux de compensation. Le chiffrement symétrique (AES-256) reste stable si la longueur des clés est maintenue. L'attention du conseil doit se porter sur la surface asymétrique.
> - **« Moissonner maintenant, déchiffrer plus tard » n'est pas un scénario futur.** Des adversaires interceptent et stockent dès aujourd'hui des journaux financiers chiffrés, des registres de règlement, des dossiers M&A et des données de virement transfrontalier, avec l'intention explicite de les déchiffrer une fois qu'un ordinateur quantique cryptographiquement pertinent (CRQC) existera. Pour des données soumises à une exigence de confidentialité de 10 à 20 ans, ce risque est déjà réalisé.
> - **L'industrie dispose désormais d'un point de référence opérationnel.** [BIS Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), publié en décembre 2025, a remplacé avec succès les signatures numériques traditionnelles par de la cryptographie post-quantique dans des transferts de liquidité en production via TARGET2 — et a fait remonter les coûts d'ingénierie spécifiques (latence de vérification, taille de paquets) auxquels tout programme de migration sera confronté.
> - **La suite NIST est l'ancre mondiale.** [FIPS 203 (ML-KEM) ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") et FIPS 204 (ML-DSA) sont référencés par toutes les juridictions majeures, même lorsque les positions nationales divergent sur les jeux de paramètres et les exigences hybrides. Les conseils d'administration devraient considérer ML-KEM-768 / ML-DSA-65 comme plancher et ML-KEM-1024 / ML-DSA-87 comme référence conservatrice pour les données à longue durée de vie.
> - **L'hybride est la seule voie crédible.** Aucune autorité majeure ne recommande la bascule directe. Faire fonctionner classique et résistant au quantique en parallèle est le schéma de déploiement validé par le NCSC, l'ANSSI, le BSI, et démontré dans Project Leap. C'est plus lourd que l'une ou l'autre alternative, mais c'est la seule qui adresse à la fois la compatibilité d'aujourd'hui et la menace de demain.

---

## L'année où la posture réglementaire s'est durcie

Pendant la majeure partie de la dernière décennie, la cryptographie post-quantique vivait dans un coin confortable de la feuille de route long terme. Les ordinateurs quantiques étaient impressionnants mais lointains ; les mathématiques cryptographiques sous-jacentes à RSA et aux courbes elliptiques étaient traitées comme un substrat stable ; et la conversation sur la migration restait largement cantonnée à des groupes de travail spécialisés. Cette position n'est plus tenable.

En janvier 2026, le [Cyber Expert Group du G7 a publié sa déclaration la plus conséquente à ce jour ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement on Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector"), coprésidée par le Trésor américain et la Banque d'Angleterre. Le document n'est pas une réglementation, mais il pèse plus qu'une orientation classique : il représente la position partagée des ministères des Finances, des banques centrales et des autorités de supervision des juridictions du G7, selon laquelle la transition cryptographique est désormais une question de gestion des risques systémiques. La feuille de route aligne son horizon de planification sur le milieu des années 2030, en encourageant les systèmes financiers critiques à migrer plus tôt — une formulation qui, dans l'idiome prudent des banquiers centraux, signale une attente plutôt qu'une suggestion.

Deux mois plus tôt, le BIS Innovation Hub et l'Eurosystème ont publié les résultats de [Project Leap Phase 2 ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), une expérimentation technique qui a remplacé les signatures numériques traditionnelles par de la cryptographie post-quantique dans des transferts de liquidité en production entre la Banca d'Italia, la Banque de France, la Deutsche Bundesbank, Nexi-Colt et Swift. La conclusion principale a été un succès — des transferts signés résistants au quantique ont franchi de bout en bout un système de paiement opérationnel. Le détail sous le titre est plus instructif, et il est examiné plus loin dans cet article.

La combinaison de ces deux événements — un cadre politique coordonné du G7 et une preuve opérationnelle dans un système de paiement réel — a produit ce que la communauté technique attendait depuis une décennie : une réponse définitive à la question « est-ce que c'est concret ? ». La réponse, en mai 2026, est oui. La question qui demeure est celle du rythme.

## Trois vecteurs de menace qui doivent préoccuper le conseil

Avant de discuter de la mécanique de migration, il est utile d'être précis sur ce qui est concrètement en jeu. Le risque quantique en banque de financement n'est pas uniforme à travers le parc cryptographique, et l'attention du conseil se porte au mieux sur les trois vecteurs où l'exposition est la plus aiguë.

### 1. Moissonner maintenant, déchiffrer plus tard (HNDL)

La préoccupation la plus immédiate n'est pas future. Elle est présente. Des adversaires de niveau étatique et des organisations criminelles sophistiquées interceptent et stockent systématiquement le trafic financier chiffré — virements, flux de messages SWIFT, communications M&A, journaux de règlement transfrontalier, contrats de swap et fichiers KYC — sans capacité actuelle de les lire. Leur objectif est simple : stocker maintenant, déchiffrer plus tard, une fois qu'un CRQC existera. Comme l'a [explicitement noté la Banque des règlements internationaux ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"), cette collecte est déjà en cours.

Pour les conseils, l'implication est inconfortable mais précise : toute donnée sensible transmise aujourd'hui sous chiffrement asymétrique classique, dont l'exigence de confidentialité s'étend au-delà de l'arrivée d'un CRQC, doit déjà être considérée comme exposée. Il n'y a pas de notification de violation quand un HNDL se produit. Il n'y a pas d'alerte SIEM. Le chiffrement tient — pour l'instant — mais les données ont déjà quitté le périmètre.

### 2. Risque de sensibilité à long terme

Les données de banque de financement ont des durées de vie institutionnelles inhabituellement longues. La documentation M&A stratégique peut rester sensible au marché pendant une décennie. Les communications sur les secrets industriels et les évaluations de propriété intellectuelle peuvent rester confidentielles pendant quinze à vingt ans. Les journaux de règlement transfrontalier, les expositions de contreparties centrales et les évaluations de crédit de contreparties conservent une sensibilité commerciale bien au-delà de leur vie transactionnelle immédiate.

L'[équation de Mosca ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography — Part 3"), formulée à l'origine par Michele Mosca et désormais intégrée à tout cadre de migration sérieux, formalise le problème. Si **S** est la durée de conservation des données, **M** est le temps nécessaire pour migrer les systèmes qui les protègent et **Q** est le temps avant qu'un CRQC ne soit disponible, alors :

```
Si S + M > Q, les données sont déjà exposées.
```

Pour des données dont l'horizon de confidentialité est de vingt ans et un programme de migration nécessitant raisonnablement cinq à sept ans, la valeur Q implicite sur laquelle le conseil parie est d'au moins 25 ans. Un corpus croissant d'évaluations d'experts — les [prédictions APAC 2026 de Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"), les enquêtes annuelles du Global Risk Institute et un article d'architecture de février 2026 qui propose un CRQC à environ 100 000 qubits physiques en utilisant des codes QLDPC — suggère que ce pari est imprudent.

### 3. La vulnérabilité des poignées de main centrales

Le troisième vecteur est le plus significatif sur le plan architectural. Les chiffrements symétriques (AES-256) restent comparativement stables ; l'algorithme de Grover divise par deux le niveau de sécurité effectif, mais doubler la longueur de clé restaure la marge. L'exposition catastrophique concerne les algorithmes asymétriques, et ce sont précisément les algorithmes qui sous-tendent toute poignée de main authentifiée en banque de financement : RSA dans l'infrastructure à clés publiques SWIFT, ECDSA dans l'authentification client/serveur TLS, ECDH dans l'établissement de clés de session, et les variantes ECC partout dans l'authentification mobile client, les signatures d'API et les chaînes de signature de code.

Un CRQC fonctionnel exécutant l'algorithme de Shor n'affaiblit pas progressivement ces systèmes. Il les casse. Une fois un CRQC opérationnel, toute poignée de main protégée par RSA, toute signature ECDSA et tout échange de clé par courbe elliptique deviennent récupérables — non pas après des mois d'effort, mais en quelques heures. La transition de « sûr » à « compromis » est binaire, et elle se propage simultanément à travers chaque système utilisant l'algorithme concerné. C'est le fondement sur lequel repose l'urgence réglementaire.

## Durcissement réglementaire : un panorama par juridiction

Le paysage réglementaire mondial en mai 2026 n'est plus une mosaïque de suggestions. C'est un ensemble coordonné de calendriers qui varient en rigueur mais convergent vers la même destination. Une banque multinationale opérant dans les principales places financières est désormais soumise à la juridiction applicable la plus stricte, non à la plus permissive.

### États-Unis

Les États-Unis ont la position la plus prescriptive pour toute institution touchant aux systèmes fédéraux. La [Commercial National Security Algorithm Suite 2.0 ⧉](https://informedclearly.com/en/technology/46563/quantum-encryption-race-post-quantum-security-standards-2026 "Quantum-Encryption Race 2026") de la NSA impose ML-KEM-1024 et ML-DSA-87 pour les systèmes de sécurité nationale, les nouveaux systèmes devant déployer la PQC à partir de janvier 2027 et la migration de l'infrastructure devant être achevée d'ici 2035. Le Mémorandum OMB M-23-02 lie les agences fédérales à la même trajectoire. Pour les banques commerciales, l'exposition immédiate passe par les chaînes d'achats fédérales, les contrats adjacents aux NSS, et la pression indirecte que les orientations de la NSA exercent sur le marché plus large.

### Union européenne

L'UE opère sur trois couches. La [feuille de route coordonnée de mise en œuvre de la Commission européenne ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"), élaborée par le Groupe de coopération NIS en juin 2025, fixe des jalons phasés à 2026 (stratégies nationales), 2030 (systèmes à haut risque migrés) et 2035 (transition complète). Le Cyber Resilience Act imposera des mises à niveau de sécurité à l'état de l'art pour les produits numériques à partir de fin 2027. NIS2 renforce la gestion des risques ICT, bien qu'aucune des deux directives ne contienne d'exigence PQC explicite. Les régulateurs nationaux, eux, ont devancé la Commission. Le BSI allemand impose l'échange de clés hybride et approuve un panier conservateur de ML-KEM, FrodoKEM et Classic McEliece. L'ANSSI française exige l'hybride à la fois pour l'encapsulation de clés et les signatures. La NLNCSA néerlandaise et les autorités norvégiennes se sont alignées sur ML-KEM-1024 comme référence conservatrice pour les données à longue durée de vie.

### Royaume-Uni

Le NCSC britannique a publié ses orientations définitives en mars 2025 et les a réaffirmées via l'Annual Review 2025. Le calendrier en trois phases est explicite :

- **Jusqu'à 2028** — Identifier les services cryptographiques nécessitant une mise à niveau, construire le plan de migration et produire un inventaire cryptographique complet.
- **2028 à 2031** — Exécuter les mises à niveau prioritaires, en particulier sur les systèmes critiques et les protocoles Internet exposés.
- **2031 à 2035** — Achever la migration sur l'ensemble des systèmes, services et produits.

Pour les institutions financières britanniques, les [orientations PQC du CMORG (Cross-Market Operational Resilience Group) ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") s'inscrivent à côté du cadre NCSC, traitent les banques comme infrastructure nationale critique et mettent l'accent sur la disponibilité des fournisseurs et l'alignement de la chaîne d'approvisionnement.

### Asie-Pacifique

La posture APAC est plus fragmentée mais évolue vite. L'ASD australienne a la position la plus dure mondialement : la cryptographie à clé publique classique ne doit plus être utilisée au-delà de fin 2030, pas de recommandation hybride, et ML-KEM-1024 requis (ML-KEM-768 acceptable uniquement jusqu'à 2030). Les organisations devraient disposer d'un plan de transition affiné d'ici fin 2026. La Monetary Authority de Singapour a publié des orientations formelles de préparation quantique. Le Japon et la Corée du Sud investissent substantiellement, bien que les deux pays disposent de filières algorithmiques nationales (la Corée a sélectionné NTRU+ et SMAUG-T comme KEM, ALMer et HAETAE comme signatures). La National Quantum Mission indienne, dotée d'une enveloppe gouvernementale de 6 003,65 crores de roupies, identifie explicitement les services bancaires et financiers comme priorité stratégique. Les [prédictions APAC 2026 de Forrester ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC predictions") évaluent à plus de 90 % le nombre d'entreprises régionales devant investir dans les technologies post-quantiques cette année.

### La position nette

Pour un conseil d'administration, la synthèse pratique de ces positions juridictionnelles est directe. Une banque multinationale ne peut pas gérer le calendrier d'un seul régulateur ; elle doit gérer le plus strict applicable. Pour la plupart des grandes institutions, cela signifie un horizon de planification de fin 2030 pour les systèmes à haut risque et fin 2035 pour la longue traîne — les entités exposées à l'ASD visant la PQC pure d'ici 2030 et celles exposées à la CNSA visant la même fenêtre avec ML-KEM-1024 et ML-DSA-87 spécifiquement.

## BIS Project Leap : ce que l'industrie a réellement prouvé

Project Leap mérite l'attention du conseil non pas parce que c'est un jalon marketing, mais parce qu'il s'agit de la démonstration de bout en bout la plus crédible à ce jour de la cryptographie post-quantique dans un système de paiement financier en production. La conclusion principale est directe : ça fonctionne. Le détail sous-jacent est là où résident les implications opérationnelles.

La Phase 1, achevée en 2023, a établi un VPN résistant au quantique entre les systèmes IT de la Banque de France et de la Deutsche Bundesbank, avec des messages de paiement transmis entre Paris et Francfort sous un schéma de chiffrement hybride. La Phase 2, achevée fin 2025 et [publiée en décembre ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"), est allée considérablement plus loin. Le consortium a remplacé les signatures numériques traditionnelles fondées sur RSA par des signatures post-quantiques dans l'exécution de transferts de liquidité via TARGET2, le système de règlement brut en temps réel de l'Eurosystème. Les participants — le BIS Innovation Hub Eurosystem Centre, la Banca d'Italia, la Banque de France, la Deutsche Bundesbank, Nexi-Colt (qui fournit la connectivité TARGET2) et Swift — représentent précisément les institutions dont l'infrastructure devra éventuellement migrer.

Le rapport a fait remonter trois constats que tout programme de migration devrait intégrer :

- **La latence de vérification est sensiblement plus élevée.** La vérification de signature post-quantique a pris matériellement plus de temps que la vérification basée sur RSA sur le même matériel. Pour un système RTGS conçu autour d'un traitement de messages sous la seconde, ce n'est pas une observation marginale ; c'est une donnée de planification de capacité.
- **Les tailles de paquets exigent une refonte du système.** Les signatures PQC sont d'un ordre de grandeur plus grandes que les équivalents ECDSA (voir plus bas). Les systèmes de paiement dont les files d'attente internes, les outils de supervision et les schémas de base de données ont été dimensionnés pour des messages de taille héritée ne peuvent pas accommoder la nouvelle charge utile sans refonte. Project Leap a explicitement constaté que TARGET2 ne pouvait pas « facilement accommoder » le modèle hybride sans réingénierie substantielle.
- **L'hybride est la bonne réponse — mais plus lourd.** Exécuter classique et post-quantique en parallèle a préservé la rétrocompatibilité et fourni une défense en profondeur, mais a doublé le coût de traitement cryptographique. C'est le coût opérationnel de faire de la PQC correctement durant la transition ; il n'est pas évitable par la seule ingénierie astucieuse.

Pour un directeur financier examinant un dossier d'investissement PQC, les constats de Project Leap sont utiles précisément parce qu'ils sont précis. Le coût de la migration post-quantique n'est pas une ligne capex unique. C'est une latence de vérification qui se propage dans les contrats SLA, une expansion de la taille des messages qui touche les budgets de stockage et de bande passante, et une période transitoire d'opérations cryptographiques dupliquées qui affecte la planification de capacité de calcul. Aucun de ces points n'est spéculatif. Ils ont été mesurés dans un système de banque centrale en production.

## La boîte à outils NIST : ML-KEM et ML-DSA comparés

La pièce maîtresse technique de tout cadre national crédible est la suite NIST de standards post-quantiques publiée en août 2024. Deux de ces standards sont au cœur de l'attention pour la banque de financement : ML-KEM (FIPS 203) pour l'encapsulation de clés et ML-DSA (FIPS 204) pour les signatures numériques. Ils partagent un fondement mathématique — tous deux reposent sur la difficulté des problèmes Module Learning With Errors (ML-LWE) et Module Short Integer Solution sur des réseaux structurés — mais ils jouent des rôles très différents dans le parc cryptographique, et leurs profils de performance et de taille diffèrent matériellement.

### ML-KEM (FIPS 203) — encapsulation de clés

ML-KEM, dérivé de [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html), est le remplaçant d'ECDH et de RSA-KEM dans les protocoles où deux parties doivent établir une clé symétrique partagée sur un canal non sûr. C'est, en pratique, là où vont les poignées de main TLS après le retrait de RSA et d'ECDH. NIST définit trois jeux de paramètres à force de sécurité croissante et performance décroissante : ML-KEM-512 (NIST Catégorie 1), ML-KEM-768 (Catégorie 3) et ML-KEM-1024 (Catégorie 5).

### ML-DSA (FIPS 204) — signatures numériques

ML-DSA, dérivé de CRYSTALS-Dilithium, est le remplaçant des signatures RSA et ECDSA. Il prend en charge la signature de certificats, la signature de code, la signature de documents et l'authentification. Les trois jeux de paramètres sont ML-DSA-44, ML-DSA-65 et ML-DSA-87, correspondant en gros aux NIST Catégories 2, 3 et 5.

### Profil de taille et de performance

Pour un DSI qui dimensionne la capacité de migration, les chiffres les plus importants sont les tailles d'artefacts. Ce sont les entrées pour la planification de capacité réseau, les projections de stockage et les tests au niveau protocolaire.

| Algorithme | Clé publique | Cryptogramme / Signature | Équivalent classique le plus proche | Taille vs classique |
|---|---|---|---|---|
| ML-KEM-512 | 800 octets | 768 octets (cryptogramme) | ECDH P-256 (~32 octets clé pub) | ~25× plus grand |
| ML-KEM-768 | 1 184 octets | 1 088 octets (cryptogramme) | ECDH P-384 | ~25× plus grand |
| ML-KEM-1024 | 1 568 octets | 1 568 octets (cryptogramme) | ECDH P-521 | ~25× plus grand |
| ML-DSA-44 | 1 312 octets | ~2 420 octets (signature) | ECDSA P-256 (sig 64 octets) | ~38× plus grand |
| ML-DSA-65 | 1 952 octets | ~3 293 octets (signature) | ECDSA P-384 | ~50× plus grand |
| ML-DSA-87 | 2 592 octets | ~4 595 octets (signature) | ECDSA P-521 | ~70× plus grand |

*Source : synthèse des spécifications [NIST FIPS 203 ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard") et FIPS 204, avec données comparatives issues de la littérature de benchmarking indépendante.*

Trois implications opérationnelles en découlent directement. **Premièrement**, la taille de signature est la contrainte limitante pour la plupart des déploiements d'entreprise. Une signature ML-DSA-65 fait environ cinquante fois la taille d'une signature ECDSA P-256, et les chaînes de certificats TLS portant des CA intermédiaires croissent proportionnellement. Les travaux de capacité sur cette surface ne sont pas optionnels — ils sont structurants. **Deuxièmement**, ML-KEM est compétitif en calcul avec ECDH et, dans certaines implémentations, matériellement plus rapide, en particulier sur du matériel disposant d'un support vectoriel pour l'arithmétique de réseaux sous-jacente. **Troisièmement**, la vérification ML-DSA est constamment rapide (souvent plus rapide que la vérification ECDSA), mais la signature ML-DSA implique une boucle de rejection sampling qui peut nécessiter plusieurs tentatives sur du matériel contraint. Pour les services de signature à haut débit, c'est un benchmark à vérifier plutôt qu'à présumer.

### Choisir les jeux de paramètres

Les positions juridictionnelles sur le choix des paramètres ne sont pas identiques, mais la convergence est claire. ML-KEM-768 et ML-DSA-65 constituent le plancher entreprise — validés par le NCSC britannique comme référence pour les organisations britanniques et acceptables dans la plupart des cadres européens. ML-KEM-1024 et ML-DSA-87 sont le plafond conservateur — imposés par la CNSA 2.0 de la NSA pour les systèmes de sécurité nationale américains et requis par l'ASD pour les entités australiennes régulées d'ici 2030. Pour les données à sensibilité extrêmement longue — journaux de règlement souverains, propriété intellectuelle à horizon décennal, registres de conservation pour instruments à longue échéance — les jeux de paramètres supérieurs sont la valeur par défaut défendable.

### Un fondement mathématique partagé, un risque partagé

Un point digne de l'attention du conseil : ML-KEM et ML-DSA tirent tous deux leur sécurité de la même famille de problèmes sur réseaux. Une percée cryptanalytique future contre Module-LWE affecterait les deux standards simultanément. C'est précisément pour cela que plusieurs autorités nationales — notamment le BSI allemand et l'ANSSI française — recommandent de compléter la pile fondée sur les réseaux par des signatures fondées sur des fonctions de hachage (SLH-DSA, FIPS 205) pour les cas d'usage de signature à long terme et de signature de code. L'agilité cryptographique, dans ce sens, n'est pas seulement la capacité de remplacer RSA par ML-KEM. C'est la capacité de remplacer un algorithme PQC par un autre lorsque le paysage cryptanalytique évolue.

## Un chemin de migration logique : Découverte → Triage → Déploiement hybride

Pour un conseil approuvant un programme PQC pluriannuel, la question opérationnelle est de savoir comment phaser le travail sans prendre un risque inacceptable de disponibilité de service. Le schéma qui a émergé à travers la feuille de route du G7, le cadre NCSC, BIS Project Leap et les documents d'orientation nationaux majeurs converge sur trois phases.

```
┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  1. DÉCOUVERTE & CBOM│ → │  2. TRIAGE (MOSCA)   │ → │  3. DÉPLOIEMENT      │
│  Inventaire crypto   │   │  Priorisation par    │   │     HYBRIDE          │
│  à travers tous les  │   │  risque selon durée  │   │  Double enveloppe    │
│  systèmes            │   │  de conservation     │   │  classique + PQC,    │
│                      │   │                      │   │  crypto-agile        │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘
```

### Phase 1 — Découverte et nomenclature cryptographique (CBOM)

On ne peut pas planifier la migration d'un parc cryptographique qui n'a pas été cartographié, et la plupart des institutions ne disposent pas d'une carte exacte. La première phase est donc la production d'une Cryptographic Bill of Materials — un inventaire structuré de chaque instance de cryptographie asymétrique dans l'organisation, chaque instance étant étiquetée par algorithme, longueur de clé, contexte protocolaire, sensibilité des données et propriétaire du système. Le scanning automatisé sur les bases de code, applications web, images de conteneurs, configurations de bases de données, magasins de certificats, modules HSM et interfaces fournisseurs est le mécanisme pratique ; l'inventaire manuel des systèmes hérités et des protocoles propriétaires est le complément inévitable.

La sortie de la Phase 1 n'est pas glamour, mais c'est le seul fondement sur lequel les Phases 2 et 3 peuvent reposer. C'est aussi le livrable que la plupart des fonctions d'audit interne et des régulateurs externes chercheront en premier lorsque les attestations de conformité PQC commenceront à être demandées.

### Phase 2 — Triage des risques avec l'équation de Mosca

Une fois la CBOM en main, l'institution peut appliquer le cadre de Mosca actif par actif. Pour chaque dépendance cryptographique, la question est de savoir si **S + M > Q** — si la durée de conservation des données plus le temps de migration dépasse le temps estimé jusqu'à un CRQC. Les actifs où l'inégalité est la plus aiguë — données sensibles à longue durée de vie sur une infrastructure qui prend des années à migrer — passent en tête de file. Les actifs avec des durées de vie de données courtes ou une infrastructure déjà modernisée peuvent être séquencés plus tard dans le programme.

C'est la phase où l'appétit pour le risque du conseil est le plus visible. La valeur Q que l'institution choisit comme cible de planification est, en effet, un pari stratégique sur le rythme des progrès du matériel quantique. Un Q conservateur (milieu des années 2030) produit un plan de migration plus agressif et une ligne capex à court terme plus élevée. Un Q optimiste (post-2040) produit un plan plus détendu et une exposition résiduelle plus élevée aux données déjà moissonnées. Ni l'un ni l'autre n'est faux ; les deux devraient être des décisions explicites du conseil, non des défauts implicites de la fonction technologique.

### Phase 3 — Déploiement hybride

Une fois les actifs prioritaires identifiés, le déploiement devrait suivre le schéma hybride démontré dans Project Leap et validé par le NCSC, l'ANSSI, le BSI et la feuille de route du G7. Un déploiement hybride fait fonctionner un algorithme classique et un algorithme post-quantique en parallèle, en combinant leurs sorties dans une enveloppe unique. Le composite est sûr contre les attaques classiques (l'algorithme classique tient aujourd'hui) et contre les attaques quantiques (l'algorithme PQC tient demain). Concrètement, le schéma habituel est X25519 combiné à ML-KEM-768 ou ML-KEM-1024 pour l'encapsulation de clés, et ECDSA combiné à ML-DSA pour les signatures lorsque les doubles signatures sont opérationnellement faisables.

Le constat de Project Leap selon lequel l'hybride est « beaucoup, beaucoup plus lourd » que l'une ou l'autre approche pure est le contrepoids honnête à cette recommandation. Les conseils devraient anticiper une hausse de capacité de calcul et de stockage, des poignées de main plus longues et une complexité additionnelle de chaînes de certificats durant la transition. Le compromis : l'hybride supprime la plus grande source unique de risque de migration — la bascule abrupte d'un fondement cryptographique à un autre en environnement de production.

## Combien cela coûte et pourquoi ne rien faire coûte plus cher

L'analyse de Mastercard, [rapportée début 2026 ⧉](https://www.qnulabs.com/blog/bank-2030-expiry-date-q-day-fatal-strategy "Your Bank's 2030 Expiry — QNu Labs"), a chiffré le coût mondial de la migration PQC du secteur financier à 28–42 milliards de dollars. À l'intérieur de cet agrégat, les [recherches RedCompass Labs et CMORG ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography") qui suivent les dépenses institutionnelles réelles suggèrent que les banques de premier rang engagent 20–30 millions de dollars par an dans des programmes de préparation, avec des calendriers d'implémentation couvrant plusieurs cycles de leadership. Ce sont des montants substantiels. Ce n'est cependant pas la comparaison pertinente.

La comparaison pertinente est le coût d'un seul événement de déchiffrement rétroactif. Pour une institution dont le trafic de virements moissonné, la correspondance M&A ou les données d'exposition aux contreparties deviennent lisibles à un adversaire en 2032, le coût opérationnel et réputationnel n'est pas borné par la ligne capex de migration. Il est borné par la valeur de la décennie d'informations stratégiques sous-jacentes — qui, pour toute institution systémique, est matériellement supérieure à tout budget de migration plausible. Le cadrage du G7 selon lequel la transition cryptographique est une question de gestion des risques systémiques plutôt qu'une mise à niveau technologique est correct, et les conseils devraient l'aborder sur cette base.

Il y a une seconde ligne de coût qui mérite d'être séparée. La migration vers la PQC est une fonction de forçage pour l'agilité cryptographique — la capacité architecturale à remplacer les algorithmes cryptographiques sans reconstruire les systèmes qui en dépendent. La plupart des institutions n'ont pas aujourd'hui d'agilité cryptographique ; leurs dépendances RSA et ECC sont profondément intégrées dans les PKI, les chaînes de signature de code, les intégrations fournisseurs et les protocoles maison accumulés au fil des décennies. L'investissement dans l'agilité, fait sous la pression de la transition PQC, est durable. Il sera mobilisé à nouveau lorsque la prochaine transition cryptographique arrivera — qu'il s'agisse d'un successeur à la PQC fondée sur les réseaux, d'une surcouche de QKD ou d'autre chose qui n'est pas encore à la feuille de route des standards. Traité correctement, le capex de migration PQC est un investissement ponctuel qui rapporte une optionalité récurrente.

## Conclusion

L'argument en faveur du traitement de la migration post-quantique comme une priorité de conseil 2026 ne repose pas sur l'imminence d'un CRQC. Les estimations à ce sujet restent réellement incertaines — l'opinion scientifique crédible place la probabilité d'un CRQC d'ici 2028 bien en dessous d'un pour cent, montant à environ cinquante pour cent à l'horizon 2037–2040. L'argument repose sur trois autres observations qui, elles, ne sont pas incertaines.

Premièrement, le HNDL se produit aujourd'hui, et les données ayant une exigence de confidentialité d'au moins une décennie sont exposées indépendamment du moment où le CRQC arrivera. Deuxièmement, la migration du parc cryptographique d'une grande institution financière prend cinq à sept ans même avec un financement adéquat et une attention de direction — ce qui signifie que le programme entamé en 2026 se termine vers 2031, soit bien à l'intérieur de l'extrémité conservatrice de la distribution de probabilité du CRQC. Troisièmement, les attentes réglementaires se sont durcies matériellement au cours des douze derniers mois, et les institutions dont les procès-verbaux de conseil 2026 consigneront un programme PQC clair seront dans une position sensiblement plus forte que celles dont les procès-verbaux ne consigneront qu'une veille attentive.

Les institutions qui démarrent maintenant ont l'avantage du choix. Elles peuvent séquencer le travail sur plusieurs cycles de leadership, l'intégrer à des initiatives de résilience plus larges et absorber les coûts opérationnels du déploiement hybride dans une planification capitalistique normale. Les institutions qui attendent feront face au même travail sous des délais plus serrés, avec moins de marge de séquencement, et sur fond de contraintes d'approvisionnement en matériel PQC, expertise et capacité fournisseurs. Le coût d'agir tôt est connu ; le coût d'agir tard est asymétrique précisément de la manière que la gestion des risques est conçue pour éviter.

Pour mettre cet article en perspective sur ce site, l'[article d'avril 2026 sur la compression des seuils quantiques](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again") examinait la trajectoire matérielle sous-jacente, l'[analyse de novembre 2023 sur CRYSTALS-Kyber](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age") couvrait les fondements mathématiques désormais standardisés sous ML-KEM, l'[article de décembre 2023 sur la distribution de clés quantique](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking") traitait de la surcouche [QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) complémentaire, et l'[implémentation de référence open source KyberLib](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats") fournit une implémentation Rust opérationnelle des primitives sous-jacentes pour les institutions souhaitant inspecter directement la surface cryptographique. Engager le détail pratique et technique — pas seulement les titres réglementaires — est la manière dont les conseils distinguent un programme de migration crédible d'un théâtre de conformité.

## Foire aux questions

**Quand un ordinateur quantique cryptographiquement pertinent existera-t-il réellement ?**

Les estimations crédibles varient largement. Début 2026, les démonstrations quantiques publiques ont atteint environ 24 à 28 qubits logiques, tandis qu'un CRQC est estimé nécessiter environ 6 000 qubits logiques sous-tendus par entre 100 000 et plusieurs millions de qubits physiques, selon l'approche de correction d'erreurs. Le consensus expert place la probabilité d'un CRQC à moins d'un pour cent d'ici 2028, autour de cinquante pour cent à l'horizon 2037–2040, avec une variabilité significative entre prévisions. Les récentes réductions des estimations théoriques de ressources — de 20 millions de qubits il y a quelques années à moins d'un million dans les travaux de Gidney en 2025, et à environ 100 000 dans l'article QLDPC de février 2026 — ont comprimé l'horizon de planification. Pour les besoins d'un conseil, l'hypothèse de planification appropriée est milieu des années 2030 pour les systèmes à haut risque, fin de la décennie 2030 comme point médian conservateur, et plus tôt si l'exposition HNDL est la préoccupation limitante.

**Pourquoi un déploiement hybride plutôt que post-quantique pur ?**

Trois raisons. Premièrement, ML-KEM et ML-DSA, bien que sérieusement validés, ont des historiques cryptanalytiques plus courts que RSA et ECC. Un schéma hybride reste sûr si l'un ou l'autre composant tient ; un schéma PQC pur est exposé si le problème sur réseaux est inopinément affaibli. Deuxièmement, l'hybride préserve la rétrocompatibilité avec les contreparties qui n'ont pas encore migré — critique dans une transition industrielle pluriannuelle. Troisièmement, toute autorité majeure en dehors de l'Australian Signals Directorate recommande explicitement l'hybride pour la période de transition : NCSC, ANSSI, BSI, NLNCSA et le cadre G7 valident tous l'approche en double enveloppe. Le compromis, comme Project Leap l'a quantifié, est un surcoût matériellement plus élevé en calcul et stockage. C'est le prix de l'optionalité.

**Faut-il à la fois ML-KEM et ML-DSA, ou peut-on choisir ?**

Les deux. ML-KEM et ML-DSA jouent des rôles cryptographiques distincts. ML-KEM remplace les primitives d'établissement de clé dans TLS, les VPN, l'authentification mobile et les protocoles similaires où deux parties doivent convenir d'une clé symétrique partagée. ML-DSA remplace les primitives de signature numérique dans les certificats PKI, la signature de code, la signature de documents, la messagerie authentifiée de type SWIFT et les assertions d'identité. Le parc cryptographique d'une institution utilise les deux types de primitives à différents endroits ; la migration doit couvrir les deux. La taille de signature significativement plus grande de ML-DSA (50–70× ECDSA) est habituellement le plus exigeant des deux sur le plan opérationnel ; le travail de planification réseau et stockage pour ML-DSA domine la plupart des évaluations de capacité de migration.

**Comment mesurer l'avancement d'un programme de cette taille ?**

Trois indicateurs sont pratiques et s'alignent avec les principaux cadres réglementaires. **Couverture de la CBOM** — quel pourcentage des instances cryptographiques asymétriques de l'institution a été inventorié, classifié et étiqueté pour priorité de migration. **Couverture de migration des actifs à haut risque** — quel pourcentage des actifs où la condition S + M > Q de Mosca est vraie a été migré vers la PQC hybride. **Couverture d'agilité cryptographique** — quel pourcentage des systèmes à dépendance cryptographique peut remplacer les algorithmes sans changement de code, par configuration seule. La feuille de route G7 CEG, le cadre en trois phases du NCSC et la feuille de route coordonnée UE se rattachent tous à ces trois mesures, même lorsqu'ils utilisent une terminologie différente.

**Quel est le coût d'attendre encore une année ?**

Il n'est pas nul, et il n'est pas symétrique. Attendre un an renonce à une année de protection HNDL sur les données à longue durée de vie — les données dont l'exigence de confidentialité s'étend à 2040 sont exposées une année de plus que nécessaire. Cela comprime la fenêtre de migration face à des échéances réglementaires fixes (ASD 2030, jalons NSA CNSA 2.0, cible UE 2030 pour les systèmes critiques), ce qui se traduit par un risque de livraison plus élevé et une flexibilité de séquencement réduite. Cela expose l'institution à des contraintes d'approvisionnement en fournisseurs et talents qui sont déjà visibles sur le marché et qui s'aggraveront lorsque les plus grands acteurs de l'industrie passeront de la planification à l'exécution. Le coût n'est pas catastrophique sur une seule année, mais il se compose, et l'environnement réglementaire converge vers une position où les conseils devront expliquer le retard plutôt que la dépense.

## Références

- Sebastien Rousseau, (2026). [Quantum Thresholds Are Moving Again](https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again/index.html "Quantum Thresholds Are Moving Again").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Sebastien Rousseau, (2023). [Quantum Key Distribution Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [KyberLib: A Rust-Powered Shield Against Quantum Threats](https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html "KyberLib: A Rust-Powered Shield Against Quantum Threats").
- G7 Cyber Expert Group, (2026). [Advancing a Coordinated Roadmap for the Transition to Post-Quantum Cryptography in the Financial Sector ⧉](https://www.gov.uk/government/publications/advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector/g7-cyber-expert-group-statement-on-advancing-a-coordinated-roadmap-for-the-transition-to-post-quantum-cryptography-in-the-financial-sector-january-20 "G7 CEG Statement, January 2026"). GOV.UK.
- Bank for International Settlements, (2025). [Project Leap Phase 2: Quantum-Proofing Payment Systems ⧉](https://www.bis.org/publ/othp107.htm "Project Leap phase 2: quantum-proofing payment systems"). BIS.
- Bank for International Settlements, (2025). [Project Leap: Quantum-Proofing the Financial System ⧉](https://www.bis.org/about/bisih/topics/cyber_security/leap.htm "Project Leap: quantum-proofing the financial system"). BIS.
- NIST, (2024). [FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard ⧉](https://csrc.nist.gov/pubs/fips/203/final "FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard"). NIST.
- UK NCSC, (2025). [Timelines for Migration to Post-Quantum Cryptography ⧉](https://www.ncsc.gov.uk/guidance/pqc-migration-timelines "Timelines for migration to post-quantum cryptography — NCSC"). UK National Cyber Security Centre.
- CMORG, (2025). [Guidance for Post-Quantum Cryptography ⧉](https://www.cmorg.org.uk/sites/default/files/2025-06/CMORG%20-%20Guidance%20for%20Post-Quantum%20Cryptography%20-%20April%202025%20-%20TLP%20CLEAR%20(1).pdf "CMORG Guidance for Post-Quantum Cryptography"). Cross-Market Operational Resilience Group.
- Post-Quantum Cryptography Coalition, (2025). [International PQC Requirements ⧉](https://pqcc.org/international-pqc-requirements/ "International PQC Requirements — Post-Quantum Cryptography Coalition"). PQCC.
- PQShield, (2025). [PQC Roadmaps and Transition Guidance ⧉](https://pqshield.com/pqc-transition-roadmaps-and-guidance/ "PQC Roadmaps and Transition Guidance"). PQShield.
- Banking.Vision, (2026). [The Year of Quantum Computing: 2026 ⧉](https://banking.vision/en/the-year-of-quantum-computing/ "The Year of Quantum Computing 2026"). Banking.Vision / msg for banking.
- The Quantum Insider, (2026). [How to Prep For Post-Quantum Cryptography: G7 Releases Roadmap ⧉](https://thequantuminsider.com/2026/01/15/how-to-prep-for-post-quantum-crytography-g7-releases-roadmap-to-help-financial-sector-navigate-transition-to-quantum-era/ "How to Prep For Post-Quantum Cryptography — The Quantum Insider"). The Quantum Insider.
- Quantum Computing Report, (2026). [Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates ⧉](https://quantumcomputingreport.com/shor-qldpc-codes-and-the-compression-of-rsa-2048-resource-estimates-part-i/ "Shor, QLDPC Codes, and the Compression of RSA-2048 Resource Estimates"). Quantum Computing Report.
- Cryptomathic, (2025). [A Banker's Guide to Quantum Safe Cryptography — Roadmap to PQC Migration for Financial Institutions ⧉](https://www.cryptomathic.com/a-bankers-guide-to-quantum-safe-cryptography-part-3-roadmap-to-pqc-migration-for-financial-institutions-cryptomathic "A Banker's Guide to Quantum Safe Cryptography"). Cryptomathic.
- Forrester, (2025). [2026 Asia Pacific Predictions: Quantum Security ⧉](https://www.forrester.com/press-newsroom/forrester-apac-2026-predictions/ "Forrester's 2026 APAC Predictions"). Forrester Research.
- The Asian Banker, (2025). [Building Resilience for a Quantum-Ready Financial System ⧉](https://www.theasianbanker.com/updates-and-articles/building-resilience-for-a-quantum-ready-financial-system "Building resilience for a quantum-ready financial system"). The Asian Banker.
