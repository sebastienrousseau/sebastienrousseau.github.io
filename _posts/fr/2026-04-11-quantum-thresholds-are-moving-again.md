---
title: "Les seuils quantiques bougent à nouveau"
subtitle: "Un nouvel article suggère que l'algorithme de Shor pourrait s'exécuter sur seulement 10 000 qubits. Le seuil du calcul quantique cryptographiquement pertinent chute plus vite que la plupart ne le supposaient."
description: "Un nouvel article suggère que l'algorithme de Shor pourrait s'exécuter sur seulement 10 000 qubits. Le seuil du calcul quantique cryptographiquement pertinent chute plus vite que la plupart ne le supposaient."
date: "April 11, 2026"
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp"
banner_alt: "Schéma du seuil de qubits pour l'algorithme de Shor. Circuit imprimé de calcul quantique aux reflets bleus"
keywords: "algorithme de Shor, qubits, calcul quantique, ECC, RSA-2048, atomes neutres reconfigurables, codes de correction d'erreurs, CRYSTALS-Kyber, CRYSTALS-Dilithium, PQC, cryptographie post-quantique"
---

## Les seuils quantiques bougent à nouveau

Un nouvel article suggère que l'algorithme de Shor pourrait s'exécuter sur seulement 10 000 qubits. Le seuil du calcul quantique cryptographiquement pertinent chute plus vite que la plupart ne le supposaient.

> **Points clés**
>
> - Un nouvel article propose que l'algorithme de Shor puisse s'exécuter sur seulement **10 000 qubits physiques** — environ cent fois moins que les estimations consensuelles précédentes.
> - La réduction est portée par trois avancées convergentes : codes de correction d'erreurs quantiques à haut rendement, réseaux d'atomes neutres reconfigurables, et parallélisme accru.
> - La menace n'est pas uniforme. La **cryptographie sur courbe elliptique (ECC)** est plus vulnérable à faibles nombres de qubits ; RSA-2048 nécessite des temps d'exécution significativement plus longs à des échelles comparables.
> - Il s'agit d'une **projection théorique**, non d'une démonstration opérationnelle. Un écart d'ingénierie substantiel demeure entre le matériel actuel et l'exécution tolérante aux pannes à cette échelle.
> - Les standards de cryptographie post-quantique sont déjà finalisés. La priorité est désormais d'**accélérer la migration**, pas d'attendre qu'un système quantique apparaisse.

## Une hypothèse familière, désormais sous pression

Au cours de la dernière décennie, les discussions autour du calcul quantique et de la cryptographie ont suivi un arc familier. Les machines quantiques étaient reconnues comme théoriquement puissantes, mais considérées comme impraticables à grande échelle. Casser les systèmes cryptographiques modernes aurait demandé des millions de qubits physiques, et le calendrier restait confortablement lointain. Cette hypothèse est désormais sous pression sérieuse.

Un article récent, [« Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits » ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), propose quelque chose de plus conséquent qu'une simple percée. Il suggère que le seuil du calcul quantique cryptographiquement pertinent pourrait être inférieur d'un ordre de grandeur à ce que l'on croyait. Non pas des millions de qubits, mais des dizaines de milliers. La distinction compte, et la direction qu'elle implique est difficile à ignorer.

## La convergence qui porte ce déplacement : correction d'erreurs, architecture et parallélisme

Le résultat n'émerge pas d'une découverte unique. Il reflète une convergence d'améliorations à plusieurs couches de la pile du calcul quantique qui, prises ensemble, déplacent la frontière de ce qui paraît faisable.

La première amélioration concerne la correction d'erreurs. Les approches traditionnelles exigeaient de gros surcoûts — souvent des centaines de qubits physiques pour représenter un seul qubit logique. L'article s'appuie plutôt sur des codes de correction d'erreurs quantiques à haut rendement, qui réduisent significativement ce surcoût ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")). La deuxième concerne l'architecture. Le système est construit sur des réseaux reconfigurables d'atomes neutres, qui peuvent être réarrangés durant le calcul pour permettre une connectivité plus flexible et une exécution plus efficace ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La troisième est le parallélisme : augmenter le nombre de qubits permet d'exécuter plus d'opérations simultanément, réduisant le temps d'exécution global.

Aucune de ces idées n'est nouvelle isolément. Combinées, cependant, elles redéfinissent ce qui était auparavant traité comme une limite dure.

## Des millions aux dizaines de milliers : ce que les chiffres signifient réellement

Pendant des années, l'estimation consensuelle pour exécuter l'algorithme de Shor à des échelles cryptographiques exigeait des millions de qubits physiques. La nouvelle analyse suggère que, sous certaines hypothèses, ce nombre pourrait tomber à environ 10 000 ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Ce chiffre, cependant, n'est pas l'image complète.

À l'extrémité basse de cette fourchette, les temps d'exécution restent longs. Factoriser RSA-2048 au nombre minimal de qubits pourrait encore prendre des années de fonctionnement continu. Une exécution plus rapide nécessite plus de qubits — potentiellement des dizaines de milliers. La relation entre le nombre de qubits et le temps d'exécution n'est pas linéaire, et l'article prend soin de présenter cela comme un spectre plutôt qu'un seuil fixe. Ce qui change, c'est la direction : la barrière n'est plus purement théorique. C'est désormais une question d'ingénierie.

### Anciennes hypothèses contre nouvelles réalités

| Dimension | Ancienne hypothèse | Nouvelle réalité |
|---|---|---|
| Qubits physiques requis (algorithme de Shor) | ~1 000 000+ | ~10 000–26 000 |
| Temps pour casser RSA-2048 (au minimum de qubits) | Infaisable cette décennie | Années (à 10 000 qubits) ; plus rapide avec plus |
| Temps pour casser ECC-256 | Infaisable cette décennie | Jours (estimé à ~26 000 qubits) |
| Paradigme matériel dominant | Qubits supraconducteurs | Réseaux d'atomes neutres reconfigurables |
| Surcoût de correction d'erreurs | Centaines de qubits physiques par qubit logique | Réduit significativement via codes haut rendement |
| Nature de la barrière | Théorique | Ingénierie |
| Urgence de migration | Planification long terme | Déploiement actif requis maintenant |

*Source : analyse à partir de [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) et de la littérature antérieure.*

## Temps, échelle et vulnérabilité inégale des systèmes cryptographiques

L'une des contributions les plus significatives de l'article est la nuance qu'il introduit autour du temps. L'avantage quantique n'arrive pas tout d'un coup. Il existe le long d'un spectre déterminé par l'échelle du système et la nature de la cible cryptographique.

Avec environ 26 000 qubits, les auteurs estiment que casser la cryptographie sur courbe elliptique pourrait prendre quelques jours dans des conditions favorables ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Pour RSA-2048, les délais sont considérablement plus longs. Cette asymétrie est importante. Elle suggère que différents systèmes cryptographiques peuvent devenir vulnérables à différents moments, plutôt que simultanément, et que la transition vers les standards post-quantiques ne sera vraisemblablement pas un événement unique avec une échéance unique.

Ce schéma est cohérent avec une couverture plus large. Des analyses des derniers mois suggèrent que des systèmes quantiques capables de défier le chiffrement largement utilisé pourraient émerger avant la fin de la décennie ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")). Les gouvernements et les organismes de normalisation planifient déjà les transitions vers la cryptographie post-quantique, avec des calendriers d'implémentation s'étendant jusque dans les années 2030 ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La discussion est passée de « si » à « quand ».

## L'écart d'ingénierie qui demeure

Il importe d'être précis sur ce que représente cet article. C'est une projection, non une démonstration. Les systèmes proposés dépendent d'hypothèses sur les taux d'erreur, la stabilité matérielle et le comportement à l'échelle qui n'ont pas encore été validées à l'échelle requise. Les expériences actuelles opèrent au niveau de centaines à quelques milliers de qubits, non pas des dizaines de milliers fonctionnant de manière tolérante aux pannes sur des périodes prolongées ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits")).

Un écart d'ingénierie substantiel demeure. Le chemin d'un modèle théorique convaincant à un système fonctionnel capable d'opération soutenue, tolérante aux pannes à cette échelle, implique des défis qui ne sont pas encore pleinement compris, encore moins résolus. Ce qui a changé n'est pas la proximité d'une machine opérationnelle, mais la crédibilité de la cible. L'écart se rétrécit, et la direction du progrès est cohérente.

## Pourquoi le calendrier qui se comprime exige de l'attention maintenant

L'importance de ce travail n'est pas que la cryptographie sera cassée à court terme. C'est que le calendrier se comprime de manière qui affecte les décisions prises aujourd'hui. Les systèmes de sécurité sont conçus avec de longs cycles de vie en tête. Les données chiffrées aujourd'hui peuvent devoir rester confidentielles pendant des décennies. Les décisions d'infrastructure prises cette année seront difficiles à inverser dans une fenêtre de cinq ans. Si les capacités quantiques arrivent plus tôt qu'attendu, ces hypothèses deviennent fragiles.

C'est pourquoi la cryptographie post-quantique est déjà déployée dans les secteurs critiques. Non parce que la menace est immédiate, mais parce que la transition prend du temps et que le coût d'être en retard est asymétrique. Il y a un schéma récurrent dans l'histoire de l'informatique : le progrès paraît lent jusqu'à ce qu'il ne le soit subitement plus. Ce qui commence comme une amélioration théorique devient une contrainte pratique, et ce qui était autrefois écarté comme lointain devient quelque chose qu'il faut planifier. Le calcul quantique pourrait suivre exactement cette trajectoire — non par une percée dramatique unique, mais par des réductions régulières de coût, de complexité et d'échelle.

## Ce que cela signifie par secteur : un guide pratique

Les implications de cette recherche ne sont pas uniformes selon les secteurs. La réponse appropriée dépend du type d'actifs cryptographiques en jeu, de la sensibilité et de la longévité des données impliquées, et du rythme auquel les attentes réglementaires évoluent.

### Services financiers et FinTech

Les institutions financières font face à un risque composé : elles détiennent des données sensibles à long terme, opèrent sur des infrastructures à cycles de remplacement lents, et sont soumises à un examen réglementaire croissant autour de la résilience cryptographique. ECC est largement utilisée dans les connexions TLS, l'authentification mobile et les signatures numériques à travers les rails de paiement — la catégorie cryptographique que l'article identifie comme la plus vulnérable à faibles nombres de qubits. Les institutions qui n'ont pas encore commencé un inventaire cryptographique ni amorcé une feuille de route de migration post-quantique devraient traiter cet article comme une incitation à accélérer, et non comme un motif de panique. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) et CRYSTALS-Dilithium, désormais standardisés par le NIST, sont les cibles de migration appropriées pour l'encapsulation de clés et les signatures numériques respectivement.

### Secteur public et défense

Les acteurs étatiques ont la motivation la plus forte — et, dans bien des cas, les ressources — pour accélérer le développement matériel quantique au-delà de ce qui est publiquement connu. Les gouvernements détenant des communications sensibles, des données de renseignement ou des clés d'infrastructure critique doivent supposer que des adversaires moissonnent déjà des données chiffrées en vue d'un déchiffrement futur — une stratégie communément appelée « harvest now, decrypt later ». Pour les organisations du secteur public, la conformité aux mandats nationaux de préparation quantique devient de plus en plus incontournable, et la fenêtre de migration proactive se rétrécit.

### Santé et infrastructures critiques

Les dossiers médicaux, les systèmes de contrôle de services publics et les réseaux industriels partagent une vulnérabilité commune : des données et systèmes à très longue durée de vie opérationnelle, protégés par des standards cryptographiques conçus pour un modèle de menace pré-quantique. Un dossier médical chiffré aujourd'hui peut devoir rester privé pendant cinquante ans. Un système de contrôle certifié cette année peut rester en service pendant deux décennies. Pour ces secteurs, le calendrier qui se comprime n'est pas une préoccupation abstraite. C'est un défi direct aux hypothèses fondatrices des architectures de sécurité actuelles.

## Conclusion

L'aspect le plus important de cet article n'est pas le nombre de qubits spécifique qu'il présente. C'est la direction que ce nombre implique. La question n'est plus de savoir si les ordinateurs quantiques peuvent défier la cryptographie moderne. C'est de savoir à quelle vitesse les systèmes requis peuvent être construits, et si les organisations qui dépendent des standards actuels réagissent assez vite.

Pour l'instant, les réponses demeurent incertaines. Mais la marge pour différer la question se rétrécit, et le coût d'attendre croît à chaque réduction crédible du seuil théorique. La communauté cryptographique, les responsables de la sécurité et les industries qui en dépendent feraient bien de traiter cet article non pas comme un motif d'alarme, mais comme une incitation sérieuse à accélérer des transitions déjà en cours.

## Foire aux questions

**10 000 qubits peuvent-ils réellement casser le chiffrement RSA ?**

Théoriquement, oui — avec des nuances importantes. Alors que les estimations précédentes suggéraient des millions de qubits physiques requis, de nouvelles recherches sur les codes de correction d'erreurs à haut rendement et les réseaux d'atomes neutres reconfigurables suggèrent que le seuil est significativement plus bas. Cependant, à 10 000 qubits, le temps d'exécution estimé pour factoriser RSA-2048 reste extrêmement long — potentiellement des années de fonctionnement continu. Des attaques plus rapides demandent plus de qubits, vraisemblablement dans la fourchette des dizaines de milliers. L'article représente une projection fondée sur des hypothèses modélisées, non une démonstration sur un système opérationnel.

**Quel chiffrement est le plus à risque face au calcul quantique ?**

La cryptographie sur courbe elliptique (ECC) est généralement plus vulnérable à faibles nombres de qubits que RSA-2048. L'article estime que casser ECC pourrait prendre quelques jours en utilisant environ 26 000 qubits reconfigurables dans des conditions favorables. RSA-2048 demande un temps d'exécution significativement plus long à des nombres de qubits comparables. Cette asymétrie signifie que les systèmes dépendants d'ECC — courants dans TLS, l'authentification mobile et la blockchain — peuvent faire face au risque sur un calendrier plus court que les infrastructures fondées sur RSA.

**Qu'est-ce qu'un qubit à atome neutre reconfigurable ?**

Les qubits à atomes neutres sont des atomes individuels — typiquement rubidium ou césium — piégés et manipulés à l'aide de lumière laser dans une chambre à vide. « Reconfigurable » signifie que l'arrangement des atomes peut être modifié dynamiquement durant le calcul, permettant une exécution plus efficace de circuits quantiques complexes. Cette flexibilité réduit le nombre de qubits physiques nécessaires pour implémenter des opérations logiques tolérantes aux pannes, et c'est une raison clé pour laquelle le nouvel article atteint des estimations de qubits plus basses que les travaux antérieurs fondés sur les architectures à qubits supraconducteurs.

**Qu'est-ce que la cryptographie post-quantique, et pourquoi est-elle déployée maintenant ?**

La cryptographie post-quantique (PQC) désigne les algorithmes cryptographiques que l'on pense sûrs à la fois contre les ordinateurs classiques et quantiques. Le NIST a finalisé son premier jeu de standards PQC en 2024, incluant [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) pour l'encapsulation de clés et CRYSTALS-Dilithium pour les signatures numériques. Le déploiement commence maintenant — bien avant que les ordinateurs quantiques ne représentent une menace immédiate — parce que les transitions cryptographiques sont lentes. Remplacer des standards enchâssés à travers l'infrastructure mondiale prend typiquement une décennie ou plus, et les données chiffrées aujourd'hui peuvent devoir rester confidentielles longtemps après que les capacités quantiques sont arrivées à maturité.

**Combien de qubits possède l'ordinateur quantique le plus puissant aujourd'hui ?**

Début 2026, les systèmes quantiques de pointe opèrent dans la fourchette des centaines à quelques milliers de qubits physiques. Crucialement, la plupart ne sont pas encore tolérants aux pannes — ils opèrent en dessous des seuils de correction d'erreurs requis pour un calcul logique soutenu et fiable. L'écart entre le matériel d'aujourd'hui et les dizaines de milliers de qubits logiques tolérants aux pannes à haute fidélité décrits dans le nouvel article demeure significatif, bien que le rythme de progrès à travers les plateformes supraconductrice, atomes neutres et ions piégés s'accélère.

## Références

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
