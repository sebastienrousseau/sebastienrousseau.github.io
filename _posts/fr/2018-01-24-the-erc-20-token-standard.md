---
title: "La norme de token ERC-20"
subtitle: "L'interface unifiée qui a permis à l'écosystème Ethereum de prospérer"
description: "ERC-20 : le type de token le plus répandu sur la blockchain Ethereum, souvent décrit comme un contrat numérique intelligent (smart contract)."
date: "January 24, 2018"
language: "fr"
locale: "fr_FR"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Ordinateur portable éteint sur une table en bois marron"
keywords: "ERC-20, Ethereum, token, smart contract, DeFi, EIP, blockchain, interoperabilité, DApps, standard"
---

![Ordinateur portable éteint sur une table en bois marron](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Aperçu

### Le besoin d'une interface de token standardisée

Avant l'avènement de la norme ERC-20 (Ethereum Request for Comments 20), la blockchain Ethereum ressemblait au Far West des architectures de tokens. Chaque nouveau token frappé avait son propre ensemble unique de règles, fonctions et interfaces. Cela imposait aux développeurs une courbe d'apprentissage redoutable et freinait l'interopérabilité des tokens. En clair, chaque nouveau token était comme une nouvelle langue à apprendre, comprendre et implémenter. Cette fragmentation entravait la scalabilité et l'adoption massive des tokens sur la plateforme Ethereum.

L'introduction de la norme ERC-20 a agi comme un langage unificateur, posant un ensemble commun de règles et de fonctions auxquelles tous les tokens Ethereum doivent se conformer. Désormais, les développeurs disposent d'une interface cohérente, quel que soit le token. Cette standardisation a fluidifié les processus d'interaction avec les tokens, permettant une intégration plus transparente dans diverses applications et services. En conséquence, les développeurs peuvent interagir plus utilement avec les tokens, favorisant un environnement propice à l'innovation et à la croissance dans l'écosystème Ethereum.

#### Le Far West des architectures de tokens

La blockchain Ethereum avait été initialement conçue pour supporter un seul type de token : ETH. Mais à mesure que la plateforme gagnait en popularité, les développeurs ont commencé à créer leurs propres tokens pour représenter une variété d'actifs et de concepts. Cela a entraîné une prolifération d'architectures de tokens différentes, chacune avec son propre ensemble unique de règles et de fonctions.

Cette fragmentation rendait difficile pour les développeurs la création d'applications capables d'interagir avec plusieurs tokens. Elle compliquait aussi pour les utilisateurs la gestion de leurs actifs de token sur différentes plateformes.

#### La norme ERC-20

La norme ERC-20 a été introduite en 2015 pour répondre aux défis posés par ce Far West des architectures de tokens. La norme définit un ensemble commun de règles et de fonctions auxquelles tous les tokens Ethereum doivent se conformer. Cette standardisation facilite la création d'applications capables d'interagir avec n'importe quel token ERC-20, et simplifie aussi la gestion des actifs de token par les utilisateurs.

La norme ERC-20 a été largement adoptée par la communauté Ethereum. Aujourd'hui, on dénombre plus de 200 000 tokens ERC-20 et la norme est utilisée par une grande variété d'applications, dont les échanges décentralisés, les plateformes de prêt et les dapps de gaming.

## Idée

### Un ensemble commun de fonctions et de propriétés pour tous les tokens

La norme ERC-20 définit un ensemble de six fonctions essentielles que tous les tokens conformes ERC-20 doivent implémenter. Ces fonctions sont :

- `transfer(address to, uint256 amount)` : transfère un montant de tokens de l'adresse de l'appelant vers l'adresse spécifiée.
- `approve(address spender, uint256 amount)` : autorise l'adresse spécifiée à dépenser un montant de tokens pour le compte de l'appelant.
- `allowance(address owner, address spender)` : retourne le montant de tokens que le « spender » spécifié est autorisé à dépenser pour le compte de l'« owner » spécifié.
- `totalSupply()` : retourne le nombre total de tokens en circulation.
- `balanceOf(address owner)` : retourne le nombre de tokens détenus par l'adresse spécifiée.
- `name()` : retourne le nom du token.
- `symbol()` : retourne le symbole du token.

La norme ERC-20 définit également deux événements qui doivent être émis lors de l'exécution réussie des fonctions correspondantes :

- `Transfer(address from, address to, uint256 amount)` : émis lorsqu'un montant de tokens est transféré d'une adresse à une autre.
- `Approval(address owner, address spender, uint256 amount)` : émis lorsque l'adresse spécifiée est autorisée à dépenser un montant de tokens pour le compte de l'« owner » spécifié.

## Impact

### La croissance de la DeFi et l'adoption d'Ethereum

La norme ERC-20 a eu un impact significatif sur l'écosystème Ethereum. Elle a été un catalyseur clé du mouvement DeFi (finance décentralisée) et a aussi contribué à accroître l'adoption d'Ethereum.

Les plateformes DeFi, qui offrent toute une gamme de services financiers allant du prêt à la gestion d'actifs, s'appuient massivement sur les tokens pour faciliter les transactions. Avec ERC-20 agissant comme un adaptateur universel, il est devenu bien plus simple pour les applications DeFi d'intégrer un large éventail de tokens sans avoir à adapter leur code à chacun.

La norme ERC-20 a aussi facilité la gestion des actifs de token par les utilisateurs. Avec des tokens respectant les mêmes règles de base, les utilisateurs trouvent plus facile de transférer, dépenser et gérer leurs actifs de token sur plusieurs plateformes. Cette expérience utilisateur améliorée a été un moteur de l'augmentation des taux d'adoption d'Ethereum.

## Incitations

### Coûts de développement réduits et sécurité améliorée

La standardisation apportée par le protocole ERC-20 a également eu un impact économique direct. En fournissant un schéma directeur éprouvé et approuvé par la communauté pour la création de tokens, elle a significativement réduit la barrière à l'entrée pour les développeurs. Ils peuvent désormais créer un nouveau token avec des coûts de développement réduits et un délai de mise sur le marché plus court, sans avoir à réinventer la roue. La norme encourage aussi indirectement la création de DApps (applications décentralisées) et de services pouvant interagir universellement avec n'importe quel token ERC-20, cultivant ainsi un écosystème plus dynamique.

Autre bénéfice notable : une sécurité renforcée. La norme ERC-20 a été soumise à un examen rigoureux par la communauté Ethereum, en faisant un modèle robuste et sûr pour l'implémentation de tokens. Le respect de cette norme implique que les aspects fondamentaux du smart contract du token suivent les bonnes pratiques acceptées par la communauté. Cela minimise le risque de vulnérabilités de sécurité qui pourraient autrement découler d'un modèle de token mal conçu. Bien que ce ne soit pas une garantie contre tous les types de vulnérabilités, c'est une étape significative vers la sécurité globale des tokens et, par extension, des projets qui les utilisent.
