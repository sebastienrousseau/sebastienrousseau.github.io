---
title: "Paiements quantique-résistants : pourquoi l'industrie doit agir maintenant"
subtitle: "La cryptographie post-quantique est désormais une décision d'infrastructure actuelle, et non future. Le livre blanc EPAA expose le risque structurel et le besoin urgent de migration."
description: "Le calcul quantique menace la cryptographie des systèmes de paiement. Le livre blanc EPAA expose le risque structurel et plaide pour une migration urgente vers la cryptographie post-quantique."
date: "September 01, 2025"
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "Circuit imprimé de calcul quantique baigné de lumière bleue"
keywords: "paiements quantique-résistants, cryptographie post-quantique, SEPA, SWIFT gpi, ISO 20022, sécurité des services financiers, EPAA, harvest-now decrypt-later, agilité cryptographique, Sebastien Rousseau"
---

## La menace quantique sur les systèmes de paiement

L'infrastructure de paiement moderne repose sur la cryptographie à clé publique — RSA, ECC et Diffie-Hellman — pour authentifier les transactions, protéger les données des porteurs de cartes et sécuriser la messagerie entre institutions financières. Ces algorithmes sous-tendent SWIFT, SEPA, les systèmes de règlement brut en temps réel et pratiquement chaque schéma de cartes en activité aujourd'hui.

Les ordinateurs quantiques exécutant l'algorithme de Shor seront capables de casser ces primitives cryptographiques. Bien que les machines quantiques tolérantes aux pannes n'existent pas encore à l'échelle requise, la trajectoire du développement matériel — démontrée par IBM, Google et d'autres — fait de cela une question de calendrier d'ingénierie plutôt que de théorie. Le National Institute of Standards and Technology (NIST) a déjà finalisé son premier jeu de standards de cryptographie post-quantique (FIPS 203, 204 et 205) en réponse.

## Le risque « moissonner maintenant, déchiffrer plus tard »

La menace n'est pas confinée à une date future à laquelle les ordinateurs quantiques atteindront une capacité suffisante. Des acteurs étatiques et des adversaires sophistiqués interceptent et stockent déjà aujourd'hui des données chiffrées, avec l'intention de les déchiffrer une fois les ressources quantiques disponibles. Cette stratégie « harvest-now decrypt-later » (HNDL) signifie que toute donnée de paiement à sensibilité longue — registres réglementaires, archives de conformité, obligations contractuelles — est déjà à risque.

Les régulateurs financiers ont commencé à réagir. La Monetary Authority of Singapore (MAS) a publié des orientations sur la préparation quantique. L'Australian Prudential Regulation Authority (APRA) a signalé le risque cryptographique dans son cadre de résilience technologique. Le Digital Operational Resilience Act (DORA) de l'Union européenne impose une gestion des risques ICT devant tenir compte des menaces émergentes, y compris le calcul quantique.

## Impact sur l'ensemble des rails de paiement

Les implications couvrent l'ensemble de l'infrastructure de paiement :

**Messagerie SWIFT :** Les formats de messages MT et MX reposent sur TLS et les signatures numériques pour l'intégrité et l'authentification. Une infrastructure de clés compromise saperait le modèle de confiance qui relie plus de 11 000 institutions à l'échelle mondiale.

**SEPA et paiements instantanés :** Le schéma SEPA Instant Credit Transfer du European Payments Council traite des transactions irrévocables en moins de dix secondes. Une compromission cryptographique à cette vitesse ne laisse aucune fenêtre pour une intervention humaine ou une vérification manuelle.

**Systèmes de paiement en temps réel :** Faster Payments (UK), FedNow (US) et NPP (Australie) partagent tous la même dépendance aux primitives cryptographiques classiques pour l'authentification des messages et la vérification des participants.

**Conformité et données à longue durée de vie :** Les enregistrements de paiement conservés à des fins réglementaires — souvent imposés pour cinq à dix ans ou plus — survivront aux garanties de sécurité de la cryptographie qui les protégeait au moment de leur création. Les programmes de migration [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) doivent prendre en compte la durée de conservation cryptographique des données qu'ils produisent.

**Blockchain et registres distribués :** Les plateformes d'actifs numériques et les instruments de paiement tokenisés qui dépendent de la cryptographie sur courbe elliptique font face à une menace directe et bien comprise des algorithmes quantiques.

## Ce que les organisations doivent faire maintenant

La transition vers une cryptographie quantique-résistante n'est pas une mise à jour unique mais un programme pluriannuel qui exige une préparation structurée :

**Inventaire cryptographique :** Les organisations doivent cataloguer chaque système, protocole et entrepôt de données qui dépend de la cryptographie à clé publique classique. Cela inclut les certificats TLS, l'authentification d'API, les configurations HSM, les systèmes de gestion de clés et le chiffrement des données au repos.

**Adoption d'algorithmes post-quantiques :** Le NIST a standardisé ML-KEM (FIPS 203) pour l'encapsulation de clés et ML-DSA (FIPS 204) pour les signatures numériques. Les organisations devraient commencer à tester ces algorithmes dans des environnements hors production et développer des feuilles de route de migration pour les systèmes critiques.

**Agilité cryptographique :** Les systèmes doivent être conçus — ou refactorisés — de sorte que les algorithmes cryptographiques puissent être remplacés sans nécessiter de refonte applicative complète. Ce principe s'applique aussi bien aux passerelles de paiement, qu'à la messagerie intermédiaire et aux API clients.

**Approches hybrides :** Durant la période de transition, les schémas cryptographiques hybrides qui combinent algorithmes classiques et post-quantiques offrent une défense en profondeur. Cette approche préserve la rétrocompatibilité tout en introduisant la résistance quantique.

## Groupe de travail EPAA et collaboration industrielle

L'Emerging Payments Association Asia (EPAA) a établi son Groupe de travail Quantum Safe Cryptography pour adresser ces défis par une action industrielle coordonnée. Le groupe de travail rassemble des participants de l'ensemble de l'écosystème des paiements, incluant IBM, HSBC, KPMG, JPMorgan Chase et PayPal, entre autres.

Lors d'ateliers tenus à Sydney, Hong Kong et Singapour, le groupe de travail a développé un cadre partagé pour évaluer le risque quantique dans les systèmes de paiement et identifier des voies de migration pratiques. Le livre blanc qui en résulte — [Quantum-Safe Payments: Why the Payments Industry Must Act Now][epaa] — représente une position consensuelle sur l'urgence et l'ampleur du défi.

L'analyse du groupe de travail conclut que la préparation quantique-résistante est une décision d'infrastructure actuelle, et non future. Les organisations qui temporisent s'exposent à ne plus pouvoir satisfaire aux attentes réglementaires, à protéger les données à longue durée de vie, ou à maintenir l'interopérabilité avec des partenaires déjà migrés.

## À propos de l'auteur

Sebastien Rousseau est Senior Digital Product Manager chez HSBC Bank plc, où il dirige les produits d'API de paiements corporate au sein de la Commercial & Investment Bank de HSBC. Il a contribué au Groupe de travail EPAA Quantum Safe Cryptography et étudie l'application de la cryptographie post-quantique aux services financiers. [En savoir plus sur Sebastien ❯][00]

## Articles connexes

- [[Distribution de clés quantique](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) : révolutionner la sécurité bancaire][rel1]
- [[CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) : l'algorithme de protection à l'ère quantique][rel2]

[00]: /about/index.html "À propos de Sebastien Rousseau"
[epaa]: https://emergingpaymentsasia.org/wp-content/uploads/2025/09/Quantum-Safe-Payments-Why-the-Payments-Industry-Must-Act-Now.pdf "Livre blanc EPAA Quantum-Safe Payments"
[rel1]: /2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking"
[rel2]: /2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age"
