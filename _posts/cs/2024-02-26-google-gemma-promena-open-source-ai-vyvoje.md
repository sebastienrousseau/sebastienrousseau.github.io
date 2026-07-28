---
title: "Google Gemma AI: proměna vývoje open-source AI"
subtitle: "Pohled zevnitř na schopnosti, open-source příspěvky a další vývoj"
description: "Model Gemma AI od Googlu: open-source projekt nabízející etická AI řešení pro osobní i firemní použití."
date: "February 26, 2024"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/ai-ship.webp"
banner_alt: "Futuristická modrá kosmická loď s neonovými světly"
keywords: "Google Gemma AI, open-source AI model, technická architektura Gemma, Gemma 2B 7B, etická AI, integrace AI na macOS, firemní AI řešení, konverzační AI, AI pro analýzu dat, AI pro edge zařízení"
---


## Open-source AI model Google pro dostupný a etický vývoj ML

Google nedávno uvedl [**Gemma ⧉**][00], open-source model umělé inteligence navržený tak, aby poskytl dostupný a etický základ pro vývoj AI. Jako open-source model Gemma zpřístupňuje svou úplnou architekturu, tréninkovou metodiku, váhy a parametry pod povolujícími licencemi, aby k nim externí výzkumníci a vývojáři měli volný přístup, mohli se z nich učit, stavět na nich a přizpůsobovat si je vlastním potřebám. Tento transparentní přístup rovněž umožňuje prověřovat vývojové postupy Gemmy a udržovat odpovědnost.

S konfiguracemi jako `Gemma 2B` a `7B` pokrývá širokou škálu použití od mobilních zařízení po cloudové infrastruktury. Uvedení Gemmy do open-source komunity dokládá silný závazek Googlu k etické AI a podporuje inovace a spolupráci s vývojáři po celém světě.

Tento článek popisuje architekturu Gemmy, její integraci s macOS a její potenciál proměnit firemní řešení i širší oblast AI.

![Logo Google Gemma - zdroj: Google](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/gemma.svg).class=\"fade-in w-25 p-5 float-end\"

## Porozumění Gemmě

### Technická architektura Gemmy

Gemmu inspiruje architektura Gemini od Googlu a je dostupná ve dvou hlavních konfiguracích:

- Model **Gemma 2B** je optimalizovaný pro efektivitu přímo na zařízení s nižšími nároky na paměť a spotřebu energie. To jej činí vhodným pro mobilní a vestavěné aplikace, jako jsou konverzační boti na chytrých telefonech nebo zařízeních chytré domácnosti.

- Model **Gemma 7B** má výrazně vyšší kapacitu vhodnou pro složitější úlohy, jako je analýza velkých datových sad a dokumentů. Jeho místem jsou datová centra a cloudová infrastruktura provádějící inference nad databázemi.

Oba poskytují všestranné stavební bloky AI pro použití od osobních projektů po firemní řešení.

### Trénink a schopnosti Gemmy

Podle její [**technické zprávy ⧉**][01] jsou modely Gemma (2B a 7B) pokročilé, trénované na rozsáhlých datových sadách s důrazem na webový obsah, matematiku a programování. Tyto modely na rozdíl od svého předchůdce Gemini nekladou důraz na vícejazyčné ani multimodální funkce. Zahrnují rozsáhlý slovník a používají nový přístup k tokenizaci, čímž zlepšují práci s různorodými typy dat. Jejich ladění podle instrukcí, které kombinuje učení s učitelem a posilované učení z lidské zpětné vazby, se zaměřuje výhradně na angličtinu a optimalizuje jemné porozumění textu i jeho generování. Tato metodická inovace zdůrazňuje jejich potenciál ve specializovaných doménách a poukazuje na vyvíjející se způsoby trénování jazykových modelů.

### Gemma a open-source komunita

Jako open-source vydání pod [**povolujícími licencemi ⧉**][03] Gemma rovněž představuje závazek Googlu podporovat etickou spolupráci v oblasti AI. Externí vývojáři nyní mohou na Gemmě stavět, zkoumat ji a přizpůsobovat ji transparentním způsobem, který demokratizuje přístup a udržuje odpovědnost.

![divider][divider].class=\"m-10 w-100\"

![Logo Ollama - zdroj: Ollama](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/ollama.svg).class=\"fade-in w-25 p-5 float-start\"

## Integrace Google Gemma s Ollama na macOS

[**Ollama ⧉**][02] je rozhraní, které umožňuje zkoumat AI asistenty lokálně na systému macOS. Použijeme jej k nastavení modelů Gemma 2B a 7B na počítačích Apple řady M. Tento návod vás provede procesem integrace Gemmy s Ollama na macOS.

Architekturu procesoru počítače vypíšete příkazem uname. Otevřete Terminál a spusťte:

```bash
uname -m
```

Pokud je výstupem `arm64`, máte Mac řady M. Pokud je to `x86_64`, máte Mac s procesorem Intel. Tento návod je určen pro Macy řady M.

### Nastavení prostředí

#### 1. Ujistěte se, že jsou nainstalovány Python 3.8+, pip a venv

Než začnete, ověřte, že máte na Macu [**Python 3.8 ⧉**][04] nebo novější a také nástroje `pip` a `venv`. Verze Pythonu a pip zkontrolujete a pip aktualizujete následujícími příkazy v Terminálu:

```bash
python3 --version
pip3 --version
pip3 install --upgrade pip
```

#### 2. Vytvořte virtuální prostředí pro izolaci závislostí

Otevřete Terminál a vytvořte virtuální prostředí, abyste předešli konfliktům s balíčky celého systému.

```bash
python3 -m venv gemma_env
source gemma_env/bin/activate
```

#### 3. Nainstalujte nejnovější Ollama pro macOS

Stáhněte [**nejnovější Ollama ⧉**][05] pro macOS z oficiálních stránek. Rozbalte aplikaci Ollama a přesuňte ji do složky Aplikace. Otevřete ji a postupujte podle pokynů k nastavení.

#### 4. Ověřte, že instalace Ollama proběhla úspěšně

Správnou instalaci Ollama ověříte spuštěním:

```bash
ollama --version
```

Měli byste vidět vypsanou verzi Ollama.

### Doporučení pro systém

Pro optimální výkon Gemma 2B budete potřebovat:

- **Procesor**: vícejádrový Intel i5 nebo lepší
- **Paměť**: 16 GB RAM (32 GB pro Gemma 7B)
- **Úložiště**: 50 GB volného místa na SSD
- **macOS**: aktuální (Monterey nebo novější)

S nastavenou Ollama jste připraveni lokálně inicializovat modely Gemma a pracovat s nimi.

![divider][divider].class=\"m-10 w-100\"

## Inicializace lokální instance Gemma

### 1. Spuštění modelu Gemma přes CLI Ollama

Vyberte model Gemma, který chcete spustit:

- Gemma 2B (menší model): `ollama run gemma:2b`
- Gemma 7B (větší model): `ollama run gemma:7b`

### 2. První spuštění stáhne prostředky modelu (může chvíli trvat)

První spuštění stáhne vybraný model Gemma, což může chvíli trvat. Po dokončení se Gemma inicializuje k použití.

#### Ukázka konverzačního dotazu

```bash
>>> Hello Gemma. How are you today?
```

Gemma odpoví přirozeným jazykem.

```bash
>>> Hello Gemma. How are you today?
Hello! It's a lovely day to be alive. Thank you for asking. How are you doing today? 😊
```

### Deaktivace virtuálního prostředí

```bash
deactivate
```

Tím se vrátíte k výchozímu prostředí Pythonu ve vašem systému.

Pro pomoc s řešením potíží nebo více podrobností o nastavení nahlédněte do [dokumentace Ollama ⧉](https://ollama.com/docs) a [dokumentace Gemma ⧉](https://github.com/google-deepmind/gemma).

![divider][divider].class=\"m-10 w-100\"

## Dopad Gemmy na open source

Od svého uvedení Gemma rychle urychlila inovace díky svému dostupnému a kolaborativnímu open-source přístupu.

Povolující licencování rovněž umožňuje zkoumat samotnou architekturu Gemmy pro výzkumné účely a provádět úpravy na velmi jemné úrovni. Vývojáři sdílejí úpravy, přizpůsobení a zcela nové schopnosti na platformách pro spolupráci na kódu.

Toto společné úsilí neustále zlepšuje schopnosti Gemmy budovat etické a odpovědné systémy AI v souladu s nově vznikajícími osvědčenými postupy.

Postupem času by díky povaze Gemmy jako open-source platformy mohl vzniknout ekosystém nástrojů, integrací i zcela nových aplikací.

![divider][divider].class=\"m-10 w-100\"

## Případy použití Gemmy pro firemní řešení

Model AI od Googlu, Gemma, nabízí díky své technické architektuře a open-source povaze různá firemní řešení, která odpovídají konkrétním obchodním potřebám.

### 1. Chatboti a konverzační agenti

Menší model Gemma 2B je optimalizovaný pro efektivitu přímo na zařízení, což jej činí vhodným pro vývoj **konverzačních botů** a **virtuálních asistentů**. Podniky mohou tyto agenty poháněné AI nasadit na mobilních zařízeních nebo vestavěných systémech a zlepšit tak zákaznický servis, podporu a zapojení bez potřeby rozsáhlých výpočetních zdrojů.

Ačkoli byla Gemma teprve uvedena, její schopnosti dobře odpovídají stávajícím aplikacím AI chatbotů a virtuálních agentů, kteří pomáhají zákazníkům. Jak bude Gemma zrát, očekáváme přímé integrace umožňující konverzační rozhraní nové generace.

### 2. Analýza dat a poznatky

Větší model Gemma 7B se svou vyšší kapacitou pro složité úlohy je dobře vhodný pro analýzu velkých datových sad a dokumentů. Podniky mohou tento model využít k získávání poznatků, trendů a vzorců z velkých objemů dat, což napomáhá rozhodovacím procesům a strategickému plánování.

### 3. Tvorba a shrnutí obsahu

Modely Gemma mohou pomáhat s generováním a shrnutím obsahu, jako jsou zprávy, články a marketingové materiály. Tato schopnost může výrazně snížit čas a úsilí potřebné k produkci kvalitního obsahu a umožnit podnikům soustředit se na kreativitu a strategii.

### 4. Personalizovaný e-mailový marketing a cílení reklamy

Díky porozumění přirozenému jazyku a jeho generování může Gemma podnikům pomoci vytvářet personalizovanější a účinnější e-mailové marketingové kampaně a strategie cílení reklamy. Tento případ použití může vést k lepšímu zapojení zákazníků a vyšší míře konverze.

### 5. Zpracování přirozeného jazyka (NLP) pro edge zařízení

Optimalizace Gemmy ji činí vhodnou pro provádění úloh NLP přímo na edge zařízeních. Tato schopnost umožňuje rozhodování v podnikání v reálném čase a plynulejší integrace s reálným světem, například v maloobchodu, výrobě a aplikacích IoT.

### 6. Kódová inteligence pro vývojáře

Gemma může zvýšit produktivitu vývojářů tím, že poskytuje rozhraní v přirozeném jazyce pro úpravy kódu a vývojové úlohy. Vývojáři mohou například pomocí konverzačních dotazů získat doporučení kódu, popisy funkcí, pomoc s laděním a revize kódu. Gemma by analyzovala kontext a sémantiku, aby poskytla relevantní návrhy. Tento „AI programátorský parťák" může pomoci zefektivnit pracovní postupy, snížit chybovost a urychlit vývoj produktů poháněných AI.

### 7. Multimodální aplikace

Díky schopnosti zpracovávat informace napříč textem, hlasem a obrazem je Gemma všestranná pro případy použití napříč modalitami. Tato vlastnost je obzvláště přínosná pro aplikace, které vyžadují interakci s uživateli přirozenějším a intuitivnějším způsobem, jako jsou zážitky ve virtuální realitě (VR) a rozšířené realitě (AR).

Open-source povaha Gemmy a její technická všestrannost z ní činí hodnotný nástroj pro podniky, které chtějí využít AI napříč provozními potřebami. Gemma je zdatná ve vytváření virtuálních asistentů a chatbotů, kteří zlepšují zákaznickou zkušenost, a zvládá velké objemy analýzy dat. Její open-source model rovněž podporuje inovace a spolupráci a umožňuje podnikům přizpůsobit si Gemmu svým potřebám.

![divider][divider].class=\"m-10 w-100\"

## Co přinese budoucnost?

Do budoucna je Gemma připravena na další růst a rozvoj. Probíhá práce na zlepšení její kompatibility s různými hardwarovými prostředími, na lepší podpoře dalších jazyků a na rozšíření spektra jejích aplikací. Google a Gemma chtějí řešit výzvy v oblasti přesnosti, detekce zkreslení a bezpečného využití dat a postavit Gemmu do role lídra v etickém vývoji AI.

![divider][divider].class=\"m-10 w-100\"

## Závěr

Uvedení Gemmy je zlomovým okamžikem v oblasti AI a zdůrazňuje posun k dostupnějším, etičtějším a kolaborativnějším vývojovým postupům. Jak se bude dále vyvíjet, Gemma sehraje zásadní roli při utváření budoucnosti AI a nabízí předlohu toho, jak mohou open-source projekty podporovat inovace při dodržování etických standardů.

[00]: https://ai.google.dev/gemma "Google Gemma AI"
[01]: https://storage.googleapis.com/deepmind-media/gemma/gemma-report.pdf "Technická zpráva Gemma"
[02]: https://ollama.com "Ollama"
[03]: https://ai.google.dev/gemma/terms "Licencování Gemma"
[04]: https://www.python.org/downloads/release/python-380/ "Python 3.8"
[05]: https://ollama.com/download "Stažení Ollama"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Oddělovač"
