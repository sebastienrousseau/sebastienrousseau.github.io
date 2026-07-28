---
title: "Kvantový algoritmus jako výzva pro kryptografii na mřížkách"
subtitle: "Nový kvantový algoritmus s polynomiálním časem pro kryptografii na mřížkách"
description: "Nový kvantový algoritmus s polynomiálním časem od Yileie Chena míří na kryptografii na mřížkách. Důsledky pro postkvantové standardy včetně CRYSTALS-Kyber."
date: "April 15, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/digital-constellation.webp"
banner_alt: "Banner se síťovými uzly v digitálním modrém prostoru"
keywords: "kvantové výpočty, kvantový algoritmus, kryptografie na mřížkách, LWE, šifrování, postkvantová kryptografie, kybernetická bezpečnost, Yilei Chen, kryptografický výzkum, bezpečnostní hrozby"
---


## Shrnutí pro vedení

Tento článek popisuje práci [**Yileie Chena ⧉**][00], který vyvinul `polynomial-time quantum algorithm`, jenž může významně ovlivnit obtížnost matematického problému **Learning With Errors (LWE)**, zásadní výzvy kryptografie na mřížkách.

Mřížky jsou diskrétní podgrupy n-rozměrného eukleidovského prostoru, které hrají klíčovou roli v moderních kryptografických schématech. Problém LWE spočívá v nalezení tajného vektoru z množiny přibližných lineárních rovnic a je základním kamenem mnoha postkvantových kryptografických protokolů.

## Chenův kvantový algoritmus s polynomiálním časem

Chenův algoritmus nabízí řešení rozhodovacího `shortest vector problem (GapSVP)` a `shortest independent vector problem (SIVP)` pro mřížky libovolné dimenze. Dosahuje toho s polynomiální časovou složitostí, což je významné zlepšení oproti dřívějším řešením.

Mezi klíčové novinky jeho práce patří:

* **Gaussovské funkce s komplexními rozptyly:** Chen zavádí použití gaussovských funkcí s komplexními rozptyly do návrhu kvantového algoritmu. Tento přístup využívá vlastnosti komplexních gaussovských rozdělení k účinnější manipulaci s kvantovými stavy, což umožňuje efektivnější řešení problému LWE.

* **Okénková kvantová Fourierova transformace:** Algoritmus používá okénkovou kvantovou Fourierovu transformaci.

## Úvod do problémů na mřížkách a jejich význam v kryptografii

Problémy na mřížkách se týkají studia matematických struktur zvaných mřížky, což jsou diskrétní podgrupy n-rozměrného eukleidovského prostoru. Tyto problémy získaly v kryptografii značnou pozornost díky své předpokládané odolnosti vůči kvantovým útokům.

Nejvýznamnějším problémem na mřížkách je [**problém Learning With Errors (LWE) ⧉**][01], který představil Oded Regev. LWE je výpočetní problém, jenž spočívá v nalezení tajného vektoru z množiny přibližných lineárních rovnic.

Mnoho moderních kryptografických schémat, například Regevův kryptosystém a výměna klíčů Frodo, opírá svou bezpečnost o obtížnost řešení problému LWE.

## Klasické algoritmy pro problémy na mřížkách a jejich omezení

Klasické algoritmy pro řešení problémů na mřížkách, například **algoritmus Lenstra-Lenstra-Lovász (LLL)** a jeho varianty, byly v kryptografii rozsáhle studovány. Tyto algoritmy však čelí značným obtížím z hlediska výpočetní složitosti, zejména s rostoucí dimenzí mřížky.

Známé klasické algoritmy pro řešení problému LWE závisí exponenciálně na počtu proměnných, což je činí nepraktickými pro mřížky vysoké dimenze. Tato bariéra složitosti je klíčovým faktorem bezpečnosti kryptografických schémat založených na LWE.

## Dřívější pokusy o vývoj kvantových algoritmů pro LWE

Před Chenovou prací zkoumalo potenciál kvantových algoritmů pro řešení problému LWE několik výzkumníků.

Oded Regev úspěšně vyvinul kvantovou redukci z `GapSVP` na `LWE`. Stojí však za zmínku, že tato redukce vyžaduje kvantové orákulum pro řešení GapSVP, jehož existence dosud nebyla prokázána.

Kuperberg vytvořil [**kvantový algoritmus pro řešení LWE se subexponenciálním aproximačním faktorem ⧉**][02]. Tyto algoritmické přístupy se však buď opíraly o neověřené předpoklady, nebo vykazovaly nižší výpočetní rychlost. Naproti tomu Chenův algoritmus nabízí řešení v polynomiálním čase bez potřeby kvantového orákula.

## Chenův kvantový algoritmus s polynomiálním časem pro LWE

Kvantový algoritmus Yileie Chena pro řešení problému LWE v polynomiálním čase představuje významný průlom v oboru. Algoritmus využívá dvě nové techniky:

1. **Gaussovské funkce s komplexními rozptyly**: Chen zavádí použití gaussovských funkcí s komplexními rozptyly do návrhu kvantového algoritmu. Tento přístup využívá vlastnosti komplexních gaussovských rozdělení k účinnější manipulaci s kvantovými stavy, což umožňuje efektivnější řešení problému LWE.

2. **Okénková kvantová Fourierova transformace**: Algoritmus používá okénkovou kvantovou Fourierovu transformaci, která umožňuje současnou analýzu problému v časové i frekvenční oblasti. Tato technika umožňuje algoritmu efektivně zpracovat vysokorozměrnou strukturu mřížek a získat relevantní informace pro řešení LWE.

Chenův algoritmus kombinuje tyto techniky k řešení `LWE`, `GapSVP` a `SIVP` v polynomiálním čase pro všechny dimenze mřížek. To je zásadní zlepšení oproti dřívějším klasickým i kvantovým algoritmům.

## Důsledky, omezení a směry dalšího výzkumu

Chenův kvantový algoritmus má důsledky pro LWE a zpochybňuje představu, že kvantové útoky nedokážou prolomit LWE a podobné problémy na mřížkách. Tento předpoklad tvoří základ mnoha vznikajících kryptografických schémat. Je však nezbytné porozumět omezením algoritmu a jeho možnému dopadu na stávající šifrovací systémy založené na LWE.

Klíčovým problémem Chenova algoritmu je, že funguje optimálně, když velikost problému výrazně převyšuje přípustnou chybovou mez. V praktických kryptografických schématech založených na LWE se poměr modulu k šumu obvykle udržuje nízký z bezpečnostních důvodů. Chenův algoritmus naopak vyžaduje vyšší poměr, aby dosáhl svého polynomiálního běhu.

Toto omezení naznačuje, že stávající šifrovací schémata založená na LWE s nižším poměrem modulu k šumu mohou vůči Chenovu algoritmu v jeho současné podobě zůstat bezpečná. I když algoritmus představuje významný teoretický průlom, nepředstavuje tedy bezprostřední hrozbu pro bezpečnost všech kryptografických systémů založených na LWE.

Jeho práce zdůrazňuje potřebu dalšího výzkumu vývoje kryptografických primitiv odolných vůči kvantovým počítačům.

## Možná využití a pobídky

Vývoj efektivních kvantových algoritmů pro problémy na mřížkách má dalekosáhlé důsledky pro všechna odvětví závislá na bezpečné digitální komunikaci a ukládání dat. Chenův algoritmus zdůrazňuje všeobecnou potřebu šifrování odolného vůči kvantovým počítačům.

Patří sem odvětví jako:

* **Kybernetická bezpečnost:** Robustní šifrovací metody odolné vůči kvantovým počítačům jsou zásadní pro ochranu citlivých informací v éře kvantových výpočtů.

* **Státní správa a obrana:** Vlády mohou tyto pokroky využít k posílení bezpečnosti kritické infrastruktury a utajovaných komunikací a zmírnit tak možné hrozby plynoucí z protivníkových kvantových výpočetních schopností.

* **Finanční služby:** Finanční sektor se silně spoléhá na bezpečné komunikační kanály pro transakce a ochranu dat. Kryptografická primitiva odolná vůči kvantovým počítačům založená na problémech na mřížkách mohou pomoci zajistit dlouhodobou bezpečnost finančních systémů.

* **Zdravotnictví:** S rostoucí digitalizací zdravotnických dat je zajištění jejich důvěrnosti a integrity mimořádně důležité. Kvantově bezpečné šifrovací metody odvozené z Chenovy práce mohou pomoci chránit citlivé informace pacientů před budoucími kvantovými útoky.

* **Cloud computing:** S rostoucím využíváním cloudových služeb je bezpečnost dat uložených a zpracovávaných v cloudu zásadní otázkou. Šifrovací schémata odolná vůči kvantovým počítačům založená na problémech na mřížkách mohou poskytnout další vrstvu ochrany pro cloudové aplikace a ukládání dat.

## Závěr

Kvantový algoritmus Yileie Chena s polynomiálním časem pro řešení problému LWE představuje významný milník v oblasti kvantových výpočtů a kryptografie. Pomocí nových metod, jako jsou gaussovské funkce a okénkové kvantové Fourierovy transformace, Chen ukázal, jak mohou kvantové algoritmy efektivně řešit složité problémy na mřížkách. Je však nezbytné poznamenat, že tato práce je v současnosti teoretickým průlomem a k jejímu přiblížení praktické implementaci je zapotřebí další výzkum.

Vývoj kryptografie odolné vůči kvantovým počítačům není jen technickou výzvou, ale také strategickým imperativem pro podniky i vlády. Investice do výzkumu a vývoje v této oblasti mohou přinést významné dlouhodobé přínosy z hlediska bezpečnosti a soukromí dat.

## Reference

Chen, Y. (2024). [**Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉**][00]. *Journal of Quantum Computing and Cryptography*, 7(4), 112-135.

Regev, O. (2005). [**On lattices, learning with errors, random linear codes, and cryptography. ⧉**][01] In *Proceedings of the 37th Annual ACM Symposium on Theory of Computing* (pp. 84-93).

Kuperberg, G. (2005). [**A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉**][02] *SIAM Journal on Computing*, 35(1), 170-188.

[00]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[01]: https://arxiv.org/abs/2401.03703 "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"
[02]: https://arxiv.org/abs/quant-ph/0302112 "A subexponential-time quantum algorithm for the dihedral hidden subgroup problem"
