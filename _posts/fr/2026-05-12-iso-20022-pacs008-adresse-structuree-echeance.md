---
title: "La deadline pacs.008 « adresse structurée » de novembre 2026 : vue à six mois"
subtitle: "À mi-novembre 2026, SWIFT CBPR+ rejettera les adresses postales non structurées dans les messages pacs.008 et messages de paiement transfrontaliers associés."
description: "À mi-novembre 2026, SWIFT CBPR+ rejettera les adresses postales non structurées dans les messages pacs.008 et messages associés. Avec environ 65 % des messages encore non conformes et 44 % des banques en retard, la fenêtre de remédiation se referme plus vite que la plupart des programmes de préparation ne sont conçus pour le gérer."
date: "May 12, 2026"
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/markus-winkler-IrRbSND5EUc-unsplash.webp"
banner_alt: "Schéma d'un message de paiement transfrontalier à adresse structurée, avec TwnNm et Ctry surlignés"
keywords: "ISO 20022, pacs.008, pacs.009, pacs.004, pacs.003, pain.001, CBPR+, SWIFT, SR2026, adresse structurée, SEPA, EPC, paiements transfrontaliers, criblage de sanctions, pacs008"
---

À partir de mi-novembre 2026, SWIFT CBPR+ rejettera les adresses postales non structurées dans les messages pacs.008 et messages de paiement transfrontaliers associés. Avec environ 65 % des messages encore non conformes et 44 % des banques en retard, la fenêtre de remédiation se referme plus vite que la plupart des programmes de préparation ne sont conçus pour le gérer.

---

> **Points clés**
>
> - À partir de **novembre 2026**, SWIFT CBPR+ n'acceptera plus les adresses postales non structurées dans les messages de paiement transfrontaliers. Le changement s'applique à **pacs.008** (virement client), **pacs.009** (virement interbancaire), **pacs.004** (retours) et **pacs.003** (prélèvements), ainsi qu'aux flux **pain.001** en amont qui les alimentent.
> - Au minimum, le **nom de la ville (TwnNm)** et le **pays (Ctry)** doivent être présents dans des champs structurés dédiés. Le **nom de rue (StrtNm)** et soit le **numéro de bâtiment (BldgNb)**, soit la **boîte postale (PstBx)** sont fortement recommandés. Les lignes d'adresse en texte libre (AdrLine) seules ne satisferont plus l'exigence pour les champs de parties clés.
> - Le changement améliore la précision du criblage de sanctions, réduit les taux de réparation manuelle et protège le straight-through processing — mais uniquement pour les institutions qui ont remédié à leurs données client en amont, pas seulement à leurs moteurs de messages.
> - La préparation industrielle est inégale. En mars 2026, environ **65 % des messages CBPR+ portent encore des adresses non structurées**, **44 % des banques** ne sont pas en bonne voie pour la deadline, et **32 % des enregistrements d'adresse client** demeurent non structurés en moyenne.
> - Un outillage open source — incluant **[pacs008](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API")**, une bibliothèque Python et un service FastAPI pour générer, valider et orchestrer les flux de messages pacs.008 — peut comprimer les délais de remédiation en automatisant la validation de schéma, les contrôles de qualité d'adresse et l'application au niveau CI avant que les messages n'atteignent le réseau SWIFT.

---

## Une deadline qui était toujours en route

L'exigence d'adresse structurée de novembre 2026 n'est pas un coup de butoir réglementaire soudain. Elle figure sur la feuille de route SWIFT CBPR+ depuis l'annonce initiale de la migration [ISO 20022](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html), et elle suit la fin de la cohabitation MT/MX en novembre 2025. Ce qui a changé en 2026, c'est la proximité. Avec environ six mois restants, l'industrie opère désormais à l'intérieur de la fenêtre où les problèmes de qualité de données non résolus deviennent un risque opérationnel.

Les chiffres racontent l'histoire clairement. La mise à jour communautaire SWIFT de mars 2026 note que [environ 65 % des messages de paiement contiennent encore des adresses non structurées ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"), et que l'adoption reste inégale selon les géographies et les types d'institutions. Une [enquête RedCompass Labs de mars 2026 auprès de 308 professionnels seniors des paiements ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022") a constaté que 44 % des banques ne sont pas actuellement en bonne voie pour respecter la deadline d'adresse structurée, en dépit d'avoir dépensé en moyenne 20 millions de dollars — et dans les plus grandes institutions plus de 30 millions — sur la préparation 2026, avec une moyenne de 13 collaborateurs supplémentaires affectés aux programmes ISO 20022. La même enquête a constaté que 32 % des enregistrements d'adresse client restent non structurés en moyenne, et que 60 % des banques signalent des lacunes dans les systèmes core banking lorsqu'il s'agit de supporter les champs d'adresse structurés.

Ce n'est donc pas un problème qui peut être résolu par un mois de plus de travail sur le moteur de messages. C'est un problème de qualité de données qui remonte du couche message vers les systèmes d'onboarding, les processus KYC, les canaux corporate et des décennies de données maîtres client en texte libre accumulées.

## Ce que la règle exige réellement

Sous la SWIFT CBPR+ Standards Release 2026 (SR2026), l'exigence clé est simple en principe et impardonnable dans le détail. À partir de mi-novembre 2026, [le nom de la ville et le pays doivent être fournis dans leurs champs structurés dédiés ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed") pour tous les agents et parties dans les messages de paiement CBPR+, avec des exceptions très limitées (relevés et notifications dans camt.052, camt.053, camt.054, plus quelques messages administratifs restent hors de l'exigence stricte). Pour les agents, l'usage continu du BIC seul reste une alternative valable à name-and-address.

Deux formats d'adresse sont autorisés après la bascule :

- **Entièrement structuré** — chaque composant de l'adresse postale est mappé à son élément ISO 20022 dédié : StrtNm (nom de rue), BldgNb (numéro de bâtiment) ou BldgNm (nom de bâtiment), PstCd (code postal), TwnNm (nom de ville), CtrySubDvsn (subdivision pays), Ctry (pays, en code ISO 3166-1 alpha-2). C'est le format que SWIFT identifie explicitement comme l'option la plus souhaitable lorsque c'est possible.
- **Hybride** — Nom de ville et pays sont renseignés dans leurs champs structurés, tandis que le reste de l'adresse peut utiliser jusqu'à deux éléments AdrLine non structurés. Important : [les éléments structurés ne doivent pas être répétés à l'intérieur des lignes non structurées ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025") ; pour un composant donné, l'adresse est l'un ou l'autre.

Les adresses entièrement non structurées — où l'adresse complète se trouve dans des éléments AdrLine sans TwnNm ni Ctry — ne seront acceptées pour aucun des champs de partie concernés. L'European Payments Council a aligné son rulebook SEPA sur la même bascule, donc [à partir du 15 novembre 2026, le format non structuré est également banni dans SCT, SDD et SCT Inst ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now"). L'alignement est délibéré : SWIFT et l'EPC ont conçu un week-end de bascule industriel unique.

Pour lever toute ambiguïté, la [documentation pacs008 liste directement les messages concernés ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008") : pacs.008 (débiteur et créancier dans les virements clients), pacs.009 (adresses d'institution dans les virements FI et les paiements de couverture), pacs.004 (adresses de partie dans les retours), et pacs.003 (prélèvements). L'exigence remonte également en amont : les fichiers pain.001 corporate portant des adresses non structurées bloqueront la génération conforme de pacs.008 chez la banque réceptrice.

## Pourquoi l'industrie en a fait une priorité

L'argument en faveur des adresses structurées n'est pas esthétique. Il est opérationnel, et il se manifeste à trois endroits.

**Criblage des sanctions.** Le bénéfice pratique le plus important est que les adresses structurées permettent aux systèmes de criblage de séparer le nom de partie des données de localisation. Les blocs d'adresse en texte libre causent régulièrement de faux positifs lorsqu'un nom de ville chevauche un token de nom de personne sanctionnée, ou lorsqu'un pays noyé dans le texte libre est totalement manqué. Les champs structurés permettent aux moteurs de criblage d'appliquer des règles de risque pays-spécifiques de manière déterministe, et ils rendent possible l'application du matching de liste de sanctions contre le code pays plutôt que de deviner sur une chaîne parsée. L'analyse CGI UK publiée en mars 2026 souligne ce point explicitement : [les données d'adresse structurées deviennent centrales pour la résilience opérationnelle, et non simplement une obligation de conformité ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement").

**Taux de réparation manuelle.** Les paiements transfrontaliers d'aujourd'hui portent un coût opérationnel significatif sous forme d'enquêtes manuelles, de gestion d'exceptions et de files de réparation — en grande partie motivés par des adresses que les systèmes de criblage ou de routage ne peuvent pas parser avec confiance. Les banques qui sont déjà passées aux adresses structurées rapportent des réductions matérielles d'exceptions STP, en particulier dans les flux de mi-corridor où les agents intermédiaires devaient auparavant interpréter des données en texte libre qu'ils n'avaient pas générées.

**Application au niveau réseau.** SR2026 durcit la validation au niveau du réseau SWIFT. Certains des nouveaux contrôles opéreront initialement en mode non bloquant — signalant des problèmes de qualité de données sans arrêter les paiements — mais la trajectoire est claire, et après la bascule, [les messages non conformes seront rejetés purement et simplement ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). Plusieurs rails de paiement américains (Fedwire, CHIPS) et SWIFT CBPR+ convergent essentiellement sur le même calendrier, ce qui supprime l'option d'une bascule échelonnée que certaines institutions avaient supposée dans les plans antérieurs.

## La vue par champ : ce qui change dans le message

Le message pacs.008 supporte les adresses structurées depuis que les premières directives d'usage CBPR+ sont entrées en vigueur en mars 2023. Ce qui change en novembre 2026 n'est pas le schéma — c'est la validation. Jusqu'à maintenant, les banques ont été autorisées à peupler les éléments AdrLine avec du texte libre et à le faire passer sur le réseau. À partir de la deadline, les contenus des blocs de partie doivent satisfaire les exigences minimales de champs structurés.

### Requis, recommandé et retiré

| Élément | XPath (sous `PstlAdr`) | Statut après nov. 2026 | Notes |
|---|---|---|---|
| Nom de ville | `<TwnNm>` | **Obligatoire** | Au moins un nom de ville structuré par partie concernée |
| Pays | `<Ctry>` | **Obligatoire** | Code ISO 3166-1 alpha-2 |
| Nom de rue | `<StrtNm>` | Fortement recommandé | Requis pour le format entièrement structuré |
| Numéro de bâtiment | `<BldgNb>` | Recommandé | Soit BldgNb, soit PstBx, pas les deux |
| Boîte postale | `<PstBx>` | Recommandé | Alternative à BldgNb |
| Code postal | `<PstCd>` | Recommandé | Requis par certains schemes locaux |
| Subdivision pays | `<CtrySubDvsn>` | Optionnel | État, région, province |
| Ligne d'adresse (texte libre) | `<AdrLine>` | **Restreint** | Max 2 lignes en hybride ; jamais aux côtés du même composant dans les champs structurés |
| Type d'adresse | `<AdrTp>` | Optionnel | Usage de `ADDR` recommandé pour les adresses postales |

*Source : synthèse des directives d'usage SWIFT CBPR+ pour SR2026 et de la [documentation adresse structurée pacs008.com ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008").*

L'implication pratique est que toute institution qui s'appuie encore sur AdrLine seule — que ce soit dans sa propre génération de message, dans les fichiers pain.001 reçus de clients corporate, ou dans les enregistrements de données maîtres utilisés pour enrichir les paiements en flux — doit migrer ces données vers les champs structurés avant la bascule. Le service de traduction en vol de SWIFT peut aider en transit, mais [il subit des surtaxes à partir de janvier 2026 ⧉](https://www.pcbb.com/products/international-banking/international-payments/iso20022-faq "ISO 20022 FAQ — PCBB") et ne peut pas parser de manière fiable tous les formats d'adresse. SWIFT a également publié [un modèle d'IA open source de structuration d'adresse ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model") entraîné sur des données de plus de 200 pays pour inférer ville et pays à partir de données héritées non structurées avec des scores de confiance, mais c'est explicitement une aide à la remédiation, pas un substitut à long terme aux données propres en amont.

## Comment pacs008.com aide à comprimer le calendrier

Pour les institutions qui ont besoin d'industrialiser leurs pipelines de qualité d'adresse et de validation de messages rapidement, [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") fournit une boîte à outils open source sous licence MIT et un service FastAPI conçus spécifiquement pour le workflow de virement client FI-à-FI. Il adresse les trois couches où les programmes de remédiation calent le plus souvent : validation de données, génération XML et application par pipeline.

Les capacités d'adresse structurée de la boîte à outils sont alignées aux exigences SR2026 :

- **Validation pré-génération** des champs d'adresse postale structurés et hybrides, pour que les données non conformes soient interceptées avant qu'aucun XML ne soit produit ou envoyé.
- **Marquage des données d'adresse non structurées** qui échoueraient après la deadline de novembre 2026, avec une distinction claire entre cas acceptables en hybride et cas entièrement non structurés.
- **Support double format** pour les formats hybrides pré-deadline et les configurations entièrement structurées post-deadline, permettant aux institutions de migrer progressivement sans casser l'interopérabilité avec les contreparties qui n'ont pas encore achevé leurs propres transitions.
- **Intégration en pipeline CI** afin que les contrôles de qualité d'adresse fassent partie du processus de build, et non un afterthought en fin de flux — la réponse pratique à l'observation CGI selon laquelle [la gouvernance des données doit être un principe de conception fondamental ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement") plutôt qu'une surcouche de conformité.

Au-delà des adresses, la boîte à outils couvre la surface plus large de validation que la version SR2026 durcit : validation JSON Schema contre 20 schémas spécifiques aux messages, vérification de format IBAN et checksum à travers 75 pays, validation XSD du XML généré contre les schémas officiels ISO 20022, et génération version-aware à travers l'ensemble des 13 révisions pacs.008 supportées (pacs.008.001.01 à pacs.008.001.13). Pour les équipes opérationnelles et conformité, elle inclut également la prévention XXE via defusedxml, la protection stricte contre le path traversal, et le masquage PII dans les journaux JSON structurés pour supporter les exigences RGPD et PCI DSS — le type de contrôles non négociables dans les flux de paiement en production mais souvent rajoutés tardivement dans les migrations menées par fournisseur.

La bibliothèque est disponible [sur PyPI ⧉](https://pypi.org/project/pacs008/ "pacs008 on PyPI") sous forme de package `pip install pacs008` et sur [GitHub ⧉](https://github.com/sebastienrousseau/pacs008 "pacs008 on GitHub") avec une transparence totale du code source. Pour les institutions qui évaluent leurs options, cela importe : l'outillage open source permet aux équipes internes d'auditer la logique de validation, de l'intégrer dans des socles Python ou FastAPI existants sans négociations de licence, et de contribuer des correctifs à mesure que leurs propres cas-limites apparaissent.

Il vaut la peine d'être précis sur le périmètre. pacs008 est une boîte à outils couche message ; elle ne remplace pas un moteur de paiements, un système de criblage, ou la remédiation des données maîtres client qu'une institution doit encore faire à la source. Ce qu'elle fait, c'est prendre ce travail de remédiation et le rendre exécutoire — transformer la conformité d'adresse structurée d'une revue manuelle en fin de longue chaîne en une porte automatisée au point de génération. Pour les programmes en manque de temps, cette porte fait la différence entre une bascule propre et une vague de rejets post-bascule.

## Le paysage de l'outillage

pacs008 s'inscrit dans un écosystème plus large d'outillage de messages ISO 20022, et le choix de l'approche dépend de la stack, de l'échelle et de la philosophie de migration de l'institution. Le paysage open source et commercial inclut [pyiso20022 ⧉](https://github.com/phoughton/pyiso20022 "pyiso20022 — an ISO 20022 message generator and parser") (large bibliothèque Python multi-catégories avec validation en bêta), la bibliothèque [pain001 ⧉](https://pain001.com/ "Pain001 — Automate ISO 20022-compliant payment file creation") associée pour l'initiation de paiement en amont, [Prowide ISO 20022 ⧉](https://www.prowidesoftware.com/development-tools/iso20022 "Prowide ISO 20022 — open source MX message parser for Java") (une bibliothèque Java exhaustive Apache 2.0 avec une couche commerciale pour la validation et les traductions CBPR+), et un certain nombre de plateformes commerciales — Mambu, Kyriba, PaymentComponents et d'autres — qui empaquètent la capacité ISO 20022 dans des offres plus larges de trésorerie ou de plateforme de paiements.

Le compromis est familier. Les plateformes commerciales réduisent la charge d'ingénierie interne mais lient l'institution à une feuille de route fournisseur qui peut ne pas correspondre à la sienne. Les bibliothèques multi-catégories exhaustives couvrent une surface plus large mais demandent plus de travail d'intégration pour un type de message donné. Les bibliothèques open source focalisées — pacs008 pour le virement client FI-à-FI, [pain001](/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html) pour l'initiation de paiement — minimisent le temps d'intégration pour les institutions qui ont besoin d'adresser rapidement des goulots d'étranglement spécifiques, et elles laissent l'institution maîtresse de ses propres règles de validation. Pour le problème d'adresse structurée en particulier, une approche focalisée a l'avantage que les règles appliquées sont étroites, bien définies et peu susceptibles de changer avant la bascule.

## Ce que cela signifie par secteur

La deadline de novembre 2026 n'affecte pas toutes les institutions de manière égale. La bonne réponse dépend du volume de trafic transfrontalier, de la maturité du domaine de données existant et du rôle joué par l'institution dans la chaîne de paiement.

### Grandes banques correspondantes et transfrontalières

Pour les banques de premier rang opérant un trafic CBPR+ significatif, l'exigence d'adresse structurée est un chantier au sein d'un programme de préparation SR2026 bien plus large qui couvre également exceptions et investigations, durcissement BAH, et (aux États-Unis) la migration simultanée de Fedwire et CHIPS. Les données RedCompass Labs suggèrent que la plupart de ces institutions dépensent 20–30 millions de dollars sur la préparation 2026, avec des équipes de livraison de 10 à 20 spécialistes. Le risque pour ce groupe n'est pas la capacité technique — c'est la capacité de livraison. Avec plusieurs chantiers parallèles se disputant les mêmes fenêtres de release, la remédiation de qualité d'adresse peut silencieusement glisser derrière des chantiers plus visibles jusqu'à ce qu'elle devienne un problème de semaine de bascule. Le palliatif pratique est de remonter la validation d'adresse plus haut dans le pipeline, pour que les défaillances émergent en environnements de développement et de test des mois avant d'avoir atteint la production.

### Banques de moyenne taille et institutions de paiement

Pour les banques de moyenne taille et les institutions EMI/PI, l'exigence d'adresse structurée est souvent l'obligation 2026 la plus matérielle qu'elles affrontent, parce qu'elles ne portent pas la même charge de chantiers concomitants que les banques de premier rang. Le défi ici est habituellement la qualité de données en amont. Les processus d'onboarding client qui ont capturé les adresses en texte libre pendant des décennies produisent des domaines de données maîtres qui ne sont pas immédiatement parsables. La remédiation automatisée — utilisant le modèle de structuration d'adresse open source de SWIFT, des services commerciaux de nettoyage d'adresse, ou une combinaison — peut adresser une part substantielle des enregistrements, mais une longue traîne résiduelle d'adresses internationales complexes nécessitera une revue manuelle. Plus tôt ce travail commence, plus petite cette traîne devient.

### Corporates et prestataires de services de paiement

Les corporates initiant des paiements via pain.001 sont en amont de la génération pacs.008 par la banque mais ne sont pas exemptés de l'exigence d'adresse structurée. Les banques ne peupleront pas rétroactivement les adresses bénéficiaires au nom des clients corporate ; les données structurées doivent provenir des systèmes propres au corporate. Pour les trésoriers d'entreprise, cela signifie s'assurer que les systèmes ERP et trésorerie capturent les adresses bénéficiaires sous forme structurée, que les informations de signataire et de débiteur ultime sont également structurées, et que les templates d'initiation de paiement n'abandonnent pas silencieusement des champs lors de la génération de fichier. La validation pré-vol des fichiers pain.001 — en utilisant soit l'outillage propre au corporate, soit des services exposés par la banque — devient le point de contrôle pratique.

### Fournisseurs, fintechs et intégrateurs

Pour les fournisseurs construisant sur les rails de paiement, la deadline est une fonction de forçage pour la capacité ISO 20022 qui aurait pu être repoussée à des phases ultérieures. Les fintechs qui routent ou initient des paiements transfrontaliers via des partenaires bancaires doivent faire remonter la capture d'adresse structurée dans leurs propres UI et API, ou accepter que les fichiers pain.001 conformes ne puissent pas être produits à partir de leurs données. L'opportunité, pour les fournisseurs capables de bouger vite, est d'absorber la charge de remédiation au nom des clients corporate — transformer un problème de conformité en service.

## Conclusion

La deadline d'adresse structurée de novembre 2026 est, en un sens, un changement étroit : deux champs obligatoires, quelques recommandés, et le retrait d'une option en texte libre qui n'aurait jamais dû être utilisée pour des données pertinentes au criblage des sanctions au premier chef. En un autre sens, c'est le jalon ISO 20022 le plus significatif opérationnellement depuis la migration CBPR+ originelle, parce qu'elle force la donnée structurée non seulement dans la couche message mais dans les systèmes en amont qui l'alimentent.

Le tableau de préparation au niveau industrie, à six mois de l'échéance, n'est pas encourageant. Deux tiers des messages CBPR+ portent encore des adresses non structurées. Près de la moitié des banques ne sont pas en bonne voie. Près d'un tiers des enregistrements d'adresse client restent non parsables. Le financement est en place — les enquêtes montrent constamment des investissements à huit et neuf chiffres — mais le travail ne l'est pas, et la dimension qualité de données du problème ne peut pas être résolue par les seules dépenses dans les derniers mois.

Ce qui aide maintenant, c'est l'automatisation au point de validation : pousser les règles dans des pipelines qui interceptent les problèmes avant qu'ils n'atteignent le réseau, plutôt qu'après. Pour les institutions opérant des socles Python ou FastAPI, l'outillage open source comme [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") fournit une manière pratique d'opérer ce basculement sans cycle de sélection de fournisseur. Pour tout le monde, indépendamment de la stack, le point stratégique est le même : les institutions qui industrialisent le changement maintenant seront dans une position bien plus forte que celles qui s'appuient sur une conformité de dernière minute — pour emprunter le phrasé des recherches RedCompass Labs qui ont cadré une grande partie de la conversation 2026.

Le week-end de bascule en novembre fermera un chapitre. Les institutions qui y arriveront avec des données propres, une validation automatisée et une compréhension opérationnelle de ce que les adresses structurées font réellement pour le criblage des sanctions passeront ce week-end à surveiller le trafic. Celles qui y arriveront sans ces choses le passeront au téléphone.

## Foire aux questions

**Que change exactement la deadline de novembre 2026 ?**

À partir de mi-novembre 2026, SWIFT CBPR+ rejettera les messages pacs.008, pacs.009, pacs.004 et pacs.003 dont les champs de partie contiennent uniquement des adresses postales non structurées. L'exigence structurée minimale est le nom de ville dans l'élément TwnNm et le pays dans l'élément Ctry (en utilisant le code ISO 3166-1 alpha-2). Les adresses hybrides restent permises — ville et pays en champs structurés, plus jusqu'à deux éléments AdrLine en texte libre pour les composants restants — mais le même composant ne peut pas figurer à la fois dans les champs structurés et non structurés. Les adresses entièrement structurées sont le format préféré. L'European Payments Council a aligné les schémas SEPA (SCT, SDD, SCT Inst) sur la même date de bascule.

**Quels messages et quels champs de partie sont concernés ?**

Pour pacs.008, l'exigence s'applique aux adresses postales du débiteur et du créancier. Pour pacs.009, elle s'applique aux adresses d'institution dans les virements FI et les paiements de couverture. Pour pacs.004, elle s'applique aux adresses de partie dans les retours de paiement. Pour pacs.003, elle s'applique aux adresses créancier et débiteur dans les prélèvements clients. Les messages de relevé et de notification (camt.052, camt.053, camt.054) et certains messages administratifs restent en dehors de l'exigence stricte. Les messages pain.001 en amont des clients corporate ne sont pas directement régis par CBPR+, mais les adresses non structurées dans les fichiers pain.001 bloqueront la génération conforme de pacs.008 en aval et sont donc effectivement dans le périmètre.

**Quelle est la différence entre adresse structurée, hybride et non structurée ?**

Une adresse entièrement structurée mappe chaque composant à son élément ISO 20022 dédié : StrtNm, BldgNb ou PstBx, PstCd, TwnNm, CtrySubDvsn, Ctry. Une adresse hybride a le nom de ville et le pays en champs structurés, le reste de l'adresse dans jusqu'à deux éléments AdrLine en texte libre ; le même composant ne doit pas figurer dans les deux. Une adresse non structurée a l'adresse postale entière dans des éléments AdrLine sans TwnNm ni Ctry structurés — c'est le format retiré en novembre 2026 pour les champs de partie concernés.

**Comment pacs008.com aide-t-il à cette transition ?**

La bibliothèque [pacs008 ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API") valide les champs d'adresse postale structurés et hybrides avant la génération XML, marque les données non structurées qui échoueraient après la deadline, supporte les formats hybrides pré-deadline et entièrement structurés post-deadline, et s'intègre dans les pipelines CI et workflows de validation par lot. Elle génère du XML pour les 13 versions pacs.008 supportées, valide contre les schémas XSD officiels ISO 20022, et expose un service FastAPI pour l'orchestration automatisée. Elle est open source sous licence de type MIT, disponible sur PyPI et conçue spécifiquement pour les workflows de virement client FI-à-FI — les règles de validation sont donc calibrées sur les directives d'usage SWIFT CBPR+ SR2026 plutôt qu'abstraites sur de nombreux types de messages.

**Que se passe-t-il si mon institution n'est pas prête en novembre 2026 ?**

Les messages avec adresses non structurées dans les champs de partie concernés seront rejetés au niveau réseau après la bascule. En pratique, cela se traduit par des échecs de paiement, des volumes d'exceptions accrus, des poussées de réparation manuelle et un impact client probable. Le service de traduction en vol de SWIFT est disponible pour certains cas transitoires mais subit des surtaxes à partir de janvier 2026 et ne peut pas parser de manière fiable tous les formats d'adresse. SWIFT a également publié un modèle d'IA open source de structuration d'adresse qui infère ville et pays à partir de données héritées non structurées, mais il est conçu pour la remédiation et le pré-traitement, non comme substitut permanent aux données propres en amont. Les institutions qui arrivent à la deadline sans un domaine de données maîtres remédié et un pipeline de validation automatisé devraient s'attendre à une semaine de bascule difficile et à une hausse opérationnelle significative dans les mois qui suivent.

## Références

- Sebastien Rousseau, (2023). [Automating ISO 20022-Compliant Payment File Creation with Pain001](https://sebastienrousseau.com/2023-09-29-automating-iso-20022-compliant-payment-file-creation-with-pain001/index.html "Automating ISO 20022-Compliant Payment File Creation with Pain001").
- pacs008, (2026). [November 2026 structured-address deadline ⧉](https://pacs008.com/structured-address/ "November 2026 structured-address deadline — pacs008"). pacs008.com.
- pacs008, (2026). [pacs008 — ISO 20022 pacs.008 Toolkit and API ⧉](https://pacs008.com/ "pacs008 — ISO 20022 pacs.008 Toolkit and API"). pacs008.com.
- SWIFT, (2026). [ISO 20022 milestone for November 2026: Unstructured addresses to be removed ⧉](https://www.swift.com/news-events/news/iso-20022-milestone-november-2026-unstructured-addresses-be-removed "ISO 20022 milestone for November 2026: Unstructured addresses to be removed"). SWIFT.
- SWIFT, (2026). [ISO 20022 for Financial Institutions ⧉](https://www.swift.com/standards/iso-20022/iso-20022-financial-institutions-focus-payments-instructions "ISO 20022 for Financial Institutions"). SWIFT.
- SWIFT, (2026). [The Swift AI address structuring model ⧉](https://www.swift.com/standards/iso-20022/iso-20022-faqs/swift-ai-address-structuring-model "ISO 20022: The Swift AI address structuring model"). SWIFT.
- RedCompass Labs, (2026). [Nearly Half of Banks Are Behind on ISO 20022 ⧉](https://financialit.net/news/banking/nearly-half-banks-are-behind-iso-20022 "Nearly Half of Banks Are Behind on ISO 20022"). Financial IT.
- RedCompass Labs, (2026). [ISO 20022 is arriving all at once for US banks ⧉](https://www.redcompasslabs.com/insights/iso-20022-is-arriving-all-at-once-for-us-banks/ "ISO 20022 is arriving all at once for US banks"). RedCompass Labs.
- ClearingPost, (2026). [The November 2026 Structured Address Deadline: What Every PSP Needs to Do Now ⧉](https://clearingpost.com/insights/iso-20022-structured-address-deadline-november-2026/ "The November 2026 Structured Address Deadline"). ClearingPost.
- CGI UK, (2026). [2026: A defining year for ISO 20022 and structured data enforcement ⧉](https://www.cgi.com/uk/en-gb/blog/banking-and-financial-markets/2026-defining-year-iso-20022-and-structured-data-enforcement "2026: A defining year for ISO 20022 and structured data enforcement"). CGI UK.
- J.P. Morgan, (2026). [ISO 20022 Migration: Guidance, Messaging & More ⧉](https://www.jpmorgan.com/insights/payments/fx-cross-border/iso-20022-migration "ISO 20022 Migration: Guidance, Messaging & More"). J.P. Morgan.
- ING, (2026). [FAQ Swift ISO 20022 ⧉](https://www.ingwb.com/en/service/payments-and-collections/swift-iso20022/faq-swift-iso-20022 "FAQ Swift ISO 20022 — ING"). ING Wholesale Banking.
- Mambu, (2026). [CBPR+ is live: what ISO 20022 means in practice ⧉](https://mambu.com/en/insights/articles/cbpr-is-live-what-iso-20022-means-in-practice "CBPR+ is live: what ISO 20022 means in practice"). Mambu.
- Kyriba, (2026). [ISO 20022 migration: what every treasury team needs to know about what's next ⧉](https://www.kyriba.com/blog/iso-20022-corporate-treasury-2026/ "ISO 20022 migration: what every treasury team needs to know about what's next"). Kyriba.
- Standard Chartered, (2025). [ISO 20022 – Standard Chartered Address Guidelines (H2H and API) ⧉](https://www.sc.com/en/uploads/sites/66/content/docs/sc-cib-tb-ISO-20022%E2%80%93CBPR-Address-guidelines-H2H-and-API-sept-2025.pdf "Standard Chartered ISO 20022 Address Guidelines"). Standard Chartered.
- State Street, (2025). [Client Guide to ISO 20022 ⧉](https://www.statestreet.com/web/insights/articles/documents/state-street-client-guide-to-iso-20022-2025.pdf "State Street Client Guide to ISO 20022 2025"). State Street.
- ISO 20022, (2026). [Message Definitions Catalogue ⧉](https://www.iso20022.org/iso-20022-message-definitions "ISO 20022 Message Definitions"). ISO 20022.
