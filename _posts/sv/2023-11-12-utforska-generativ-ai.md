---
title: "Generativ AI 2023: hur den fungerar och var den landar"
subtitle: "Tillämpad artificiell intelligens inom bank och finansiella tjänster."
description: "Utforska generativ AI 2023: hur den fungerar, var den först landar inom finansiella tjänster och de etiska och arkitektoniska frågor som är värda att ställa."
date: "November 12, 2023"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp"
banner_alt: "Abstrakt visualisering av ett neuralt nätverk i blå och lila toner som representerar AI-bearbetning"
keywords: "generativ AI, stor språkmodell, transformerarkitektur, GPT-4, AI inom finansiella tjänster, hallucination, retrieval-augmented generation, AI-styrning, grundmodell, finjustering"
---

![Abstrakt visualisering av ett neuralt nätverk i blå och lila toner som representerar AI-bearbetning](https://cloudcdn.pro/stocks/images/getty-images-aTWKwJllPOA.webp).class=\"img-fluid clearfix\"

> **Sammanfattning / viktigaste slutsatser**
>
> - **Arkitekturen som förändrade allt.** Transformerartikeln från 2017 introducerade self-attention: en mekanism som beräknar relevansvikter mellan varje par av tokens i indata och ersätter RNN:ernas sekventiella bearbetning med parallelliserbara matrisoperationer. Varje större språkmodell 2023 är en transformervariant ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762 "Attention Is All You Need")).
> - **GPT-4 som 2023 års riktmärke.** GPT-4, som släpptes i mars 2023, placerade sig i 90:e percentilen på det amerikanska advokatprovet, 99:e på GRE Verbal, och uppvisade flerstegsresonemang över långa dokument. Den satte det kapacitetsriktmärke som efterföljande modeller siktade på att nå eller överträffa ([OpenAI, 2023](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report")).
> - **Modeller med öppna vikter demokratiserade tillgången.** Metas Llama 2 (juli 2023) och Mistral AI:s Mistral 7B (september 2023) visade att modeller i klass med GPT-3.5 kunde köras på privat infrastruktur, vilket adresserade de reglerade branschernas krav på datalokalisering.
> - **Piloter inom finansiella tjänster 2023.** Breda driftsättningar i slutet av 2023 omfattade granskning av juridiska avtal (JPMorgans DocLLM-forskning), bevakning av regelverksändringar och produktivitetsverktyg för utvecklare. Goldman Sachs rapporterade intern användning av AI-kodassistenter bland 10 000 utvecklare.
> - **Hallucination är ett produktionshinder.** LLM:er genererar rimligt klingande men faktamässigt felaktiga utdata i icke försumbar omfattning. I reglerade användningsfall (kreditbeslut, efterlevnadsutlåtanden, kundinformation) är hallucination inte en kosmetisk brist; det är en regulatorisk risk och en ansvarsrisk som kräver arkitektoniska motåtgärder som retrieval-augmented generation (RAG).

---

## Hur transformerarkitekturen fungerar

Varje betydande språkmodell som driftsattes 2023 (GPT-4, Claude 2, Llama 2, Mistral, Falcon) bygger på den transformerarkitektur som introducerades i 2017 års artikel "Attention Is All You Need". Att förstå kärnmekanismen förklarar både varför dessa modeller fungerar och var de misslyckas.

**Tokens och inbäddningar.** Modellen börjar med att dela upp indatatext i deltokens (vanligen med byte-pair encoding). Varje token avbildas på en högdimensionell vektor (en inbäddning) som kodar dess semantiska relationer till andra tokens, inlärda under förträningen.

**Self-attention.** För varje token beräknar modellen tre vektorer: en Query (vad denna token söker efter), en Key (vad denna token erbjuder) och en Value (vad denna token bidrar med). Uppmärksamhetspoäng beräknas genom att ta skalärprodukten av varje Query mot alla Keys, tillämpa softmax för att producera vikter och summera Values viktade med dessa poäng. Det innebär att varje token uppmärksammar varje annan token i kontextfönstret samtidigt: den mekanism som ger transformermodeller deras förmåga att hantera långväga beroenden.

**Multi-head attention.** Flera uppmärksamhetshuvuden körs parallellt, där vart och ett lär sig olika typer av relationer (syntaktiska, semantiska, positionella). Deras utdata sammanfogas och projiceras linjärt.

**Feed-forward-lager.** Efter uppmärksamheten passerar varje position genom två linjära transformationer med en icke-linjär aktivering. Detta lager utför beräkning per token oberoende av övriga och fångar lokala särdragstransformationer.

**Skala.** GPT-4 uppskattas till över en biljon parametrar (obekräftat av OpenAI). Llama 2 70B använder 70 miljarder. Mistral 7B använder 7 miljarder, med grouped-query attention och sliding window attention för effektivitet. Större modeller uppvisar i allmänhet bättre zero-shot- och few-shot-resonemang: de emergenta förmågor som gör dem användbara för uppgifter de inte uttryckligen tränats på.

## Modellandskapet 2023

2023 producerade fler betydande modellsläpp än något tidigare år:

**GPT-4 (OpenAI, mars 2023).** Multimodal (text- och bildindata), kontextfönster på upp till 128 000 tokens i den senare varianten GPT-4 Turbo, starkt flerstegsresonemang. Satte riktmärket för uppgifter inom professionella domäner.

**Claude 2 (Anthropic, juli 2023).** Kontextfönster på 100 000 tokens (längst vid lanseringen), stark prestanda på uppgifter med långa dokument som avtalsgranskning och regelverksanalys. Constitutional AI-träning för färre skadliga utdata.

**Llama 2 (Meta, juli 2023).** Släppt med öppna vikter i varianterna 7B, 13B, 34B och 70B parametrar. Kommersiell användning tillåten. Möjliggjorde driftsättning på egen infrastruktur för reglerade branscher. Gav upphov till hundratals finjusterade varianter (Code Llama, Vicuna, WizardLM).

**Mistral 7B (Mistral AI, september 2023).** 7 miljarder parametrar som överträffar Llama 2 13B på de flesta riktmärken. Grouped-query attention och sliding window attention sänker inferenskostnaden. Den första betydande europeiska frontmodellen, relevant med tanke på GDPR och EU:s AI-förordning.

**Falcon 180B (TII, september 2023).** Modell med öppna vikter och 180 miljarder parametrar, tränad på 3,5 biljoner tokens RefinedWeb-data. Visade att modeller med öppna vikter kunde närma sig skalan hos GPT-4-klassen.

## Var generativ AI först landade inom finansiella tjänster

I slutet av 2023 hade finansinstituten gått från interna experiment till strukturerade pilotprogram i flera distinkta användningsfall:

**Utvecklarproduktivitet.** Kodgenereringsverktyg (GitHub Copilot, Amazon CodeWhisperer, internt finjusterade modeller) blev den bredast driftsatta kategorin. Goldman Sachs rapporterade att 10 000 utvecklare hade tillgång till AI-kodassistans. Morgan Stanley driftsatte GPT-4 internt för att hjälpa finansiella rådgivare att hämta information ur en kunskapsbas med 100 000 dokument.

**Bearbetning av juridiska och regulatoriska dokument.** Extraktion av avtalsklausuler, bevakning av regelverksändringar och efterlevnadskartläggning var piloterna med högst värde. JPMorgans forskning kring DocLLM visade att språkmodeller medvetna om dokumentlayout överträffade generiska LLM:er på uppgifter som gäller förståelse av finansiella dokument.

**Förstärkt kundservice.** Banker driftsatte LLM-drivna assistenter för kundfrågor i första linjen, med eskalering till människa för reglerad rådgivning. Centrala begränsningar: modellen får inte ge reglerad rådgivning, får inte hallucinera produktvillkor och måste vara granskningsbar.

**Generering av KYC- och AML-berättelser.** Att sammanfatta komplexa transaktionsmönster och kundprofiler för analytikergranskning, som ersättning för vad som tidigare varit manuellt skrivarbete, framträdde som ett trovärdigt användningsfall med lägre hallucinationsrisk eftersom modellen sammanfattar tillhandahållna data i stället för att generera nya påståenden.

## Riskerna som produktionen blottlade

Att gå från demo till produktion inom finansiella tjänster synliggjorde en uppsättning risker som krävde arkitektoniska svar:

**Hallucination.** LLM:er genererar felaktiga utdata som låter säkra, i en omfattning som varierar med uppgiftstyp och modell. På uppgifter som gäller faktaåtergivning hallucinerar även GPT-4 i en omfattning som är oacceptabel för efterlevnadsutlåtanden eller kreditinformation. Den främsta motåtgärden är retrieval-augmented generation (RAG): förankra modellens utdata i hämtade, verifierbara dokument i stället för att enbart förlita sig på parametrisk kunskap.

**Promptinjektion.** Fientliga indata inbäddade i dokument eller användarmeddelanden kan styra om modellens beteende. Inom finansiella tjänster, där LLM:er bearbetar icke betrodda dokument (avtal, e-post, kundinlämningar), är promptinjektion en säkerhetsrisk i produktion, inte en teoretisk sådan.

**Dataläckage.** Modeller som finjusterats eller promptats på konfidentiella data kan återge dessa data i utdata: en väsentlig risk för personuppgifter, handelspositioner och kundinformation. Arkitektoniska kontroller (privat driftsättning, hantering av data i kontexten, utdatafiltrering) är ett krav, inte ett tillval.

**Modellproveniens och granskningsbarhet.** Tillsynsmyndigheter förväntar sig att finansinstitut kan förklara automatiserade beslut. En LLM som producerar en kreditbedömning utan ett granskningsbart resonemangsspår uppfyller inte förklarbarhetskraven i GDPR artikel 22, bestämmelserna om AI-system med hög risk i EU:s AI-förordning eller FCA:s befintliga vägledning om modellrisk.

**Föråldrad kunskap.** LLM:er har brytdatum för träningsdata. En modell tränad på data fram till början av 2023 känner inte till regelverksändringar, räntebeslut eller marknadshändelser efter det datumet: en betydande begränsning för användningsfall som gäller regelefterlevnad i realtid eller marknadskommentarer, utan RAG eller realtidshämtning.

## Styrningskrav före driftsättning

Praktiker inom finansiella tjänster väntade 2023 inte på regulatorisk visshet före driftsättning, men ledande institut antog ramverk för modellriskhantering (MRM) anpassade från vägledningen i SR 11-7 och SS3/18:

**Modellinventering och dokumentation.** LLM:er som driftsätts för affärsfunktioner kräver dokumentation av träningsdatas proveniens, finjusteringsmetodik, kända felmoder och prestanda på domänspecifika valideringsuppsättningar.

**Kontrollpunkter med människa i loopen.** För reglerade utdata (kreditbeslut, efterlevnadsutlåtanden, kundinformation) förblev mänsklig granskning obligatorisk 2023. Automatisering tillämpades på utkast och sammanfattning; det slutliga godkännandet förblev mänskligt.

**Leverantörsrisk.** Att använda ett tredjeparts-API för modeller (OpenAI, Anthropic, Google) medför koncentrationsrisk mot leverantören, risk kring datalokalisering och risk för modelländringar (leverantörer kan uppdatera modeller i tysthet). Företagsavtal och privata driftsättningar mildrar dessa delvis.

**Dialog med tillsynsmyndigheter.** FCA, PRA, ECB och FINRA publicerade alla rapporter eller tal om AI-styrning under 2023. Det genomgående budskapet: befintliga ramverk för modellrisk gäller för AI, och företag bör vara proaktiva med att dokumentera sin styrningsansats i väntan på formell vägledning.

## Vanliga frågor

**Vad är skillnaden mellan en stor språkmodell och en grundmodell?**

En stor språkmodell (LLM) är en modell tränad på textdata i stor skala för att förutsäga och generera språk. Grundmodell är ett bredare begrepp för varje stor förtränad modell som kan anpassas (finjusteras eller promptas) för flera nedströmsuppgifter: det inkluderar LLM:er men även bildmodeller, kodmodeller och multimodala modeller. GPT-4 är både en LLM och en grundmodell. DALL-E 3 är en grundmodell men inte en LLM. I praktiken används begreppen ofta synonymt när man talar om textgenererande system.

**Vad är retrieval-augmented generation och varför är det viktigt för finansiella tjänster?**

RAG kombinerar en språkmodell med ett hämtningssystem: i stället för att enbart förlita sig på modellens parametriska kunskap (det den lärde sig under träningen) hämtar RAG relevanta dokument vid inferens och tillhandahåller dem som kontext. Detta minskar hallucinationer avsevärt på faktauppgifter eftersom modellen syntetiserar tillhandahållen text i stället för att återkalla inlärda fakta. För finansiella tjänster möjliggör RAG användningsfall som bevakning av regelverksändringar (hämtar alltid gällande regler) och avtalsgranskning (förankrar modellen i den faktiska avtalstexten) som skulle vara alltför hallucinationsbenägna med en ren genereringsansats.

**Hur bör finansinstitut hantera EU:s AI-förordning i förhållande till driftsättningar av generativ AI 2023?**

EU:s AI-förordning befann sig fortfarande i lagstiftningsprocessen 2023 (antogs av Europaparlamentet i mars 2024, trädde i kraft i augusti 2024). Institut med EU-verksamhet eller EU-kunder utvärderade dock redan sina pipelines. AI-system med hög risk inom kreditvärdering, anställningsbeslut och kritisk infrastruktur kräver bedömningar av överensstämmelse, mekanismer för mänsklig tillsyn och granskningsloggning. AI-modeller för allmänna ändamål (GPAI), vilket inkluderar grundmodeller som GPT-4, har en egen kravnivå kring transparens och systemrisk. Företag som påbörjade dokumentations- och styrningsarbetet 2023 var bättre positionerade inför genomförandefristerna.

**Vad är den praktiska skillnaden mellan finjustering och promptutformning för LLM-driftsättningar i företag?**

Finjustering modifierar modellens vikter genom fortsatt träning på domänspecifika data: den lär modellen ny kunskap och nya beteendemönster. Den kräver märkta träningsdata, beräkningsbudget och löpande underhåll när basmodellerna uppdateras. Promptutformning (inklusive few-shot-exempel och systemprompter) formar beteendet vid inferens utan att ändra vikterna: snabbare att införa och uppdatera, men begränsad av vad basmodellen redan kan. För de flesta driftsättningar inom finansiella tjänster 2023 var RAG plus promptutformning den föredragna startpunkten; finjustering reserverades för fall där modellen behövde lära sig proprietär terminologi eller följa strikta utdataformat.

## Referenser

- Vaswani, A., et al., (2017). [Attention Is All You Need ⧉](https://arxiv.org/abs/1706.03762 "Attention Is All You Need").
- OpenAI, (2023). [GPT-4 Technical Report ⧉](https://arxiv.org/abs/2303.08774 "GPT-4 Technical Report").
- Touvron, H., et al., Meta AI, (2023). [Llama 2: Open Foundation and Fine-Tuned Chat Models ⧉](https://arxiv.org/abs/2307.09288 "Llama 2").
- Jiang, A., et al., Mistral AI, (2023). [Mistral 7B ⧉](https://arxiv.org/abs/2310.06825 "Mistral 7B").
