---
title: "Le soglie quantistiche si muovono di nuovo"
subtitle: "L'algoritmo di Shor potrebbe richiedere appena 10.000 qubit"
description: "Un nuovo articolo suggerisce che l'algoritmo di Shor possa essere eseguito con appena 10.000 qubit. La soglia del calcolo quantistico crittograficamente rilevante sta scendendo rapidamente."
date: "April 11, 2026"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp"
banner_alt: "Soglie quantistiche"
keywords: "Shor, qubit, RSA, ECC, PQC, soglia quantistica, harvest now decrypt later"
---

## I umbrales quantistici tornano a moverse

Un nuovo artículo sugiere che il algoritmo di Shor potrebbe ejecutarse con solo 10.000 qubits. Il umbral della calcolo quantistico criptográficamente relevante cae più rápido di lo che la mayoría suponía.

> **TL;DR.** La soglia di qubit necessari per eseguire l'algoritmo di Shor contro RSA-2048 continua a scendere. Le stime recenti parlano di 10.000 qubit, dimezzando le previsioni di pochi anni fa. La finestra di migrazione PQC si restringe.
>
> **Punti chiave**
>
> - **Stime in calo** — i requisiti hardware per Shor sono scesi di un ordine di grandezza in pochi anni.
> - **Pressione su PQC** — accelera l'urgenza della migrazione crittografica nei servizi finanziari.
> - **Harvest now, decrypt later** — gli attacchi di raccolta dati sono già in corso.
> - **Implicazioni** — i piani di migrazione devono essere accorciati, non solo prolungati.

## Una hipótesis familiar, ora sotto presión

A lo largo della última década, le discusiones attorno alla calcolo quantistico e la criptografía hanno seguido un arco familiar. Le máquinas quantistiche erano reconocidas come teóricamente potentes, ma consideradas impracticables il suo larga scala. Romper i sistemi crittografici modernos habría exigido millones di qubits físicos, e il calendario permanecía cómodamente lejano. Questa hipótesis è ora sotto presión seria.

Un artículo reciente, ["Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits" ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), propone algo più consecuente che un simple progresso. Sugiere che il umbral della calcolo quantistico criptográficamente relevante potrebbe essere inferior in un orden di magnitud a lo che se creía. Non millones di qubits, sino decenas di miles. La distinción importa, e la indirizzo che implica è difícil di ignorar.

## La convergencia che impulsa questo desplazamiento: corrección di errores, arquitectura e paralelismo

Il resultado non emerge di un descubrimiento único. Refleja una convergencia di mejoras in diverse capas della pila della calcolo quantistico che, tomadas juntas, desplazan la frontera di lo che parece factible.

La primera mejora se riferisce alla corrección di errores. I approcci tradicionales exigían grandi sobrecostes —spesso cientos di qubits físicos per representar un solo qubit lógico—. Il artículo se apoya in cambiamento in códigos di corrección di errores quantistici di alto prestazioni, che reducen significativamente quello sobrecoste ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")). La segunda se riferisce alla arquitectura. Il sistema è costruito su retículos reconfigurables di átomos neutros, che possono reorganizarse durante il cálculo per consentire una conectividad più flexible e una ejecución più eficiente ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La tercera è il paralelismo: aumentar il número di qubits consente ejecutar più operazioni simultáneamente, reduciendo il tiempo di ejecución globale.

Ninguna di queste idee è nuova aisladamente. Combinadas, tuttavia, redefinen lo che prima se trattaba come un límite duro.

## Di millones a decenas di miles: lo che le cifras significano realmente

Durante años, la estimación consensuada per ejecutar il algoritmo di Shor a escalas crittografiche exigía millones di qubits físicos. Il nuovo análisis sugiere che, sotto ciertas hipótesis, quello número potrebbe caer a alrededor di 10.000 ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Questa cifra, tuttavia, non è la imagen completa.

In il extremo sotto di quello rango, i tiempos di ejecución rimangono siendo largos. Factorizar RSA-2048 al número mínimo di qubits potrebbe ancora llevar años di funcionamiento continuo. Una ejecución più rápida richiede più qubits, potencialmente decenas di miles. La relación tra il número di qubits e il tiempo di ejecución non è lineal, e il artículo se cuida di presentare esto come un espectro invece di un umbral fijo. Lo che cambia è la indirizzo: la barrera già non è puramente teórica. È ora una cuestión di ingeniería.

### Antiguas hipótesis rispetto a nuove realidades

| Dimensión | Antigua hipótesis | Nueva realidad |
|---|---|---|
| Qubits físicos requeridos (algoritmo di Shor) | ~1.000.000+ | ~10.000–26.000 |
| Tiempo per romper RSA-2048 (al mínimo di qubits) | Inviable questa década | Años (con 10.000 qubits); più rápido con più |
| Tiempo per romper ECC-256 | Inviable questa década | Días (estimado con ~26.000 qubits) |
| Paradigma di hardware dominante | Qubits superconductores | Retículos di átomos neutros reconfigurables |
| Sobrecoste di corrección di errores | Cientos di qubits físicos per qubit lógico | Reducido significativamente mediante códigos di alto prestazioni |
| Naturaleza della barrera | Teórica | Ingeniería |
| Urgencia di migración | Planificación a lungo termine | Despliegue activo requerido ora |

*Fuente: análisis a partire da [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) e della literatura anterior.*

## Tiempo, escala e vulnerabilidad desigual dei sistemi crittografici

Una delle contribuciones più significative del artículo è il matiz che introduce attorno al tiempo. La vantaggio quantistica non arriva di golpe. Existe lungo un espectro determinado per la escala del sistema e la naturaleza del objetivo crittografico.

Con alrededor di 26.000 qubits, i autori estiman che romper la criptografía di curva elíptica potrebbe llevar alcuni días in condiciones favorables ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Per RSA-2048, i scadenze sono considerablemente più largos. Questa asimetría è importante. Sugiere che diversi sistemi crittografici possono volverse vulnerables in momentos diferentes, invece di simultáneamente, e che la transición verso i standard post-quantisticos probablemente non sarà un acontecimiento único con una fecha límite única.

Questo esquema è coherente con una cobertura più amplia. Análisis dei últimos meses sugieren che sistemi quantistici capaces di desafiar il cifrado ampliamente utilizzato potrebbero emerger prima del final della década ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")). I governi e i organismos di normalización planifican già le transiciones alla crittografia post-quantistica, con calendarios di implementación che se extienden fino a la década di 2030 ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La discusión ha pasado di "se" a "cuándo".

## La brecha di ingeniería che persiste

Conviene essere preciso su lo che rappresenta questo artículo. È una proyección, non una demostración. I sistemi propuestos dependen di hipótesis su tasas di error, estabilidad del hardware e comportamiento alla escala che ancora non sono stati validadas alla escala requerida. I experimentos actuales operano in il livello di cientos a alcuni miles di qubits, non di decenas di miles funcionando in modo tolerante a fallos durante periodos prolongados ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits")).

Rimane existiendo una brecha di ingeniería sustancial. Il percorso di un modello teórico convincente a un sistema funcional capaz di operazione sostenida e tolerante a fallos a quella escala implica sfide che ancora non se comprenden plenamente, e molto meno se resuelven. Lo che ha cambiado non è la proximidad di una máquina operativa, sino la credibilidad del objetivo. La brecha se estrecha, e la indirizzo del progreso è coherente.

## Perché il calendario che se comprime exige atención ora

La importancia di questo trabajo non è che la criptografía vaya a romperse a breve termine. È che il calendario se comprime in modo che riguarda alle decisiones tomadas hoy. I sistemi di sicurezza se diseñan con largos ciclos di vida in mente. I dati cifrados hoy possono avere che permanecer confidenciales durante décadas. Le decisiones di infraestructura tomadas questo año saranno difíciles di invertir in una ventana di cinco años. Se le capacità quantistiche arrivano prima di lo esperado, queste hipótesis se tornano frágiles.

Per eso la crittografia post-quantistica già viene desplegando in i settori críticos. Non perché la amenaza sea inmediata, sino perché la transición porta tiempo e il costo di arrivare tarde è asimétrico. C'è un patrón recurrente in la historia della informática: il progreso parece lento fino a che di repente deja di serlo. Lo che comienza come una mejora teórica diventa in una restricción pratica, e lo che prima se descartaba come lejano diventa in algo che bisogna planificar. La calcolo quantistico potrebbe seguir exactamente questa trayectoria, non mediante un único progresso dramático, sino mediante reducciones regulares di costo, complejidad e escala.

## Lo che esto significa per settore: una guía pratica

Le implicaciones di questa ricerca non sono uniformes in tutti i settori. La respuesta apropiada depende del tipo di activos crittografici in juego, della sensibilidad e longevidad dei dati implicados, e del ritmo al che evolucionan le expectativas normativas.

### Servicios finanziari e FinTech

Le istituzioni finanziarie afrontan un rischio compuesto: poseen dati sensibles a lungo termine, operano su infraestructuras con ciclos di reemplazo lentos e sono sometidas a un escrutinio normativo creciente attorno alla resiliencia crittografica. ECC viene utilizzato ampliamente in le conexiones TLS, la autenticación móvil e le firmas digitali in i rails di pagamento: la categoría crittografica che il artículo identifica come la più vulnerable a bajos números di qubits. Le istituzioni che ancora non hanno comenzado un inventario crittografico ni hanno iniciado una roadmap di migración post-quantistica dovrebbero tratar questo artículo come un incentivo per acelerar, non come un motivo di pánico. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) e CRYSTALS-Dilithium, ora estandarizados per il NIST, sono i objetivos di migración apropiados per la encapsulación di chiavi e le firmas digitali respectivamente.

### Sector público e defensa

I actores estatales hanno la motivación più fuerte —e, in molti casos, i recursos— per acelerar il desarrollo di hardware quantistico più allá di lo che è noto públicamente. I governi che custodian comunicaciones sensibles, dati di inteligencia o chiavi di infraestructura crítica devono suponer che i adversarios cosechan già dati cifrados con vistas a un descifrado futuro, una estrategia comúnmente llamada "harvest now, decrypt later". Per le organizaciones del settore público, il conformità dei mandatos nazionali di preparación quantistica se torna ogni volta più ineludible, e la ventana di migración proactiva se estrecha.

### Sanidad e infraestructuras críticas

I historiales médicos, i sistemi di control di servizi públicos e le reti industriales comparten una vulnerabilidad común: dati e sistemi con una vida operativa molto larga, protegidos per standard crittografici progettati per un modello di amenaza precuántico. Un historial médico cifrado hoy può avere che permanecer privado durante cincuenta años. Un sistema di control certificado questo año può permanecer in servizio durante dos décadas. Per questi settori, il calendario che se comprime non è una preocupación abstracta. È un sfida directo alle hipótesis fundacionales delle arquitecturas di sicurezza actuales.

## Conclusione

Il aspecto più importante di questo artículo non è il número específico di qubits che presenta. È la indirizzo che quello número implica. La cuestión già non è se i computer quantistici possono desafiar la criptografía moderna. È a che cosa velocità possono construirse i sistemi requeridos, e se le organizaciones che dependen dei standard actuales reaccionan lo bastante rápido.

Per il momento, le respuestas rimangono siendo inciertas. Ma il margen per diferir la cuestión se estrecha, e il costo di esperar crece con ogni reducción creíble del umbral teórico. La comunità crittografica, i responsables di sicurezza e le industrias che dependen di ellos harían bene in tratar questo artículo non come un motivo di alarma, sino come un incentivo serio per acelerar transiciones già in curso.

## Domande frequenti

**Possono realmente 10.000 qubits romper il cifrado RSA?**

Teóricamente, sí, con matices importanti. Sebbene le estimaciones anteriores sugerían millones di qubits físicos requeridos, nuove ricerche su códigos di corrección di errores di alto prestazioni e retículos di átomos neutros reconfigurables sugieren che il umbral è significativamente più sotto. Tuttavia, con 10.000 qubits, il tiempo di ejecución estimado per factorizar RSA-2048 rimane siendo extremadamente largo: potencialmente años di funcionamiento continuo. I ataques più rápidos exigen più qubits, probablemente in il rango delle decenas di miles. Il artículo rappresenta una proyección basata in hipótesis modeladas, non una demostración in un sistema operativo.

**Qué cifrado è più in rischio rispetto alla calcolo quantistico?**

La criptografía di curva elíptica (ECC) è generalmente più vulnerable a bajos números di qubits che RSA-2048. Il artículo estima che romper ECC potrebbe llevar alcuni días utilizando alrededor di 26.000 qubits reconfigurables in condiciones favorables. RSA-2048 richiede un tiempo di ejecución significativamente più largo con números di qubits comparables. Questa asimetría significa che i sistemi dependientes di ECC —comunes in TLS, autenticación móvil e blockchain— possono affrontare il rischio in un calendario più corto che le infraestructuras basate in RSA.

**Qué è un qubit di átomo neutro reconfigurable?**

I qubits di átomos neutros sono átomos individuales —típicamente rubidio o cesio— atrapados e manipulados mediante luz láser in una cámara di vacío. "Reconfigurable" significa che la disposición dei átomos può modificarse dinámicamente durante il cálculo, permitiendo una ejecución più eficiente di circuitos quantistici complejos. Questa flexibilidad reduce il número di qubits físicos necesarios per implementar operazioni lógicas tolerantes a fallos, e è una razón chiave per la che il nuovo artículo alcanza estimaciones di qubits più bajas che i trabajos anteriores basati in le arquitecturas di qubits superconductores.

**Qué è la crittografia post-quantistica, e perché viene desplegando ora?**

La crittografia post-quantistica (PQC) designa i algoritmos crittografici che se piensan seguros tanto contra ordenadores clásicos come quantistici. Il NIST finalizó il suo primer juego di standard PQC in 2024, incluido [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) per la encapsulación di chiavi e CRYSTALS-Dilithium per le firmas digitali. Il despliegue comienza ora —molto prima di che i computer quantistici representen una amenaza inmediata— perché le transiciones crittografiche sono lentas. Reemplazar standard incrustados in tutta la infraestructura mundial porta típicamente una década o più, e i dati cifrados hoy possono avere che permanecer confidenciales molto dopo di che le capacità quantistiche hayan llegado alla madurez.

**Cuántos qubits ha hoy il computer quantistico più potente?**

A principios di 2026, i sistemi quantistici punteros operano in il rango di cientos a alcuni miles di qubits físicos. Di forma crucial, la mayoría ancora non sono tolerantes a fallos: operano al di sotto di i umbrales di corrección di errores requeridos per un cálculo lógico sostenido e fiable. La brecha tra il hardware actual e le decenas di miles di qubits lógicos tolerantes a fallos di alta fidelidad descritos in il nuovo artículo rimane siendo significativa, sebbene il ritmo del progreso attraverso le piattaforme superconductora, di átomos neutros e di iones atrapados se acelera.

## Riferimenti

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
