---
title: "Los umbrales quânticos vuelven a moverse"
subtitle: "Um novo artigo sugiere que o algoritmo de Shor poderia ejecutarse com solo 10.000 qubits. El umbral de a computação quântica criptográficamente relevante cae mais rápido de lo que a maioria suponía."
description: "Um novo artigo sugiere que o algoritmo de Shor poderia ejecutarse com solo 10.000 qubits. El umbral de a computação quântica criptográficamente relevante cae mais rápido de lo que a maioria suponía."
date: "April 11, 2026"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp"
banner_alt: "Esquema do umbral de qubits para o algoritmo de Shor. Placa de circuito de computação quântica com reflejos azules"
keywords: "algoritmo de Shor, qubits, computação quântica, ECC, RSA-2048, átomos neutros reconfigurables, códigos de corrección de errores, CRYSTALS-Kyber, CRYSTALS-Dilithium, PQC, criptografia pós-quântica"
---

## Los umbrales quânticos vuelven a moverse

Um novo artigo sugiere que o algoritmo de Shor poderia ejecutarse com solo 10.000 qubits. El umbral de a computação quântica criptográficamente relevante cae mais rápido de lo que a maioria suponía.

> **TL;DR.** Um novo artigo propone que o algoritmo de Shor pueda ejecutarse com solo 10.000 qubits físicos —perto de cien vezes menos que as estimaciones consensuadas anteriores—. La barrera ya no é puramente teórica: é de ingeniería. Los estándares de criptografia pós-quântica ya estão finalizados; a prioridad agora é acelerar a migración.
>
> **Principais Conclusões**
>
> - Um novo artigo propone que o algoritmo de Shor pueda ejecutarse com solo **10.000 qubits físicos**, em torno de cien vezes menos que as estimaciones consensuadas anteriores.
> - La reducción está impulsionada por três avances convergentes: códigos de corrección de errores quânticos de alto rendimiento, retículos de átomos neutros reconfigurables e paralelismo aumentado.
> - La amenaza no é uniforme. La **criptografia de curva elíptica (ECC)** é mais vulnerable a bajos números de qubits; RSA-2048 requer tempos de execução significativamente mais largos a escalas comparables.
> - Trata-se de uma **proyección teórica**, no de uma demostración operativa. Sigue existiendo uma brecha de ingeniería sustancial entre ou hardware actual e a execução tolerante a fallos a essa escala.
> - Los estándares de criptografia pós-quântica ya estão finalizados. La prioridad agora é **acelerar a migración**, no esperar a que aparezca um sistema quântico.

## Una hipótesis familiar, agora sob presión

A lo largo de a última década, as discusiones em torno de a computação quântica e a criptografia têm seguido um arco familiar. Las máquinas quânticas eram reconocidas como teóricamente potentes, mas consideradas impracticables a gran escala. Romper os sistemas criptográficos modernos habría exigido millones de qubits físicos, e o calendario permanecía cómodamente lejano. Esta hipótesis está agora sob presión seria.

Um artigo reciente, [«Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits» ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), propone algo mais consecuente que um simple avance. Sugiere que o umbral de a computação quântica criptográficamente relevante poderia ser inferior em um orden de magnitud ao que se creía. No millones de qubits, mas sim decenas de miles. La distinción importa, e a direção que implica é difícil de ignorar.

## La convergencia que impulsiona este desplazamiento: corrección de errores, arquitectura e paralelismo

El resultado no emerge de um descubrimiento único. Refleja uma convergencia de mejoras em várias capas de a pila de a computação quântica que, tomadas juntas, desplazan a frontera de lo que parece factible.

La primeira mejora se refiere a a corrección de errores. Los enfoques tradicionais exigían grandes sobrecostes —frequentemente cientos de qubits físicos para representar um solo qubit lógico—. El artigo se apoya em cambio em códigos de corrección de errores quânticos de alto rendimiento, que reducen significativamente esse sobrecoste ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")). La segunda se refiere a a arquitectura. El sistema está construido sobre retículos reconfigurables de átomos neutros, que podem reorganizarse durante o cálculo para permitir uma conectividad mais flexible e uma execução mais eficiente ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La tercera é o paralelismo: aumentar o número de qubits permite ejecutar mais operações simultáneamente, reduciendo o tempo de execução global.

Ninguna de estas ideias é nova aisladamente. Combinadas, no entanto, redefinen lo que antes se trataba como um límite duro.

## De millones a decenas de miles: lo que as cifras significan realmente

Durante anos, a estimación consensuada para ejecutar o algoritmo de Shor a escalas criptográficas exigía millones de qubits físicos. El novo análisis sugiere que, sob ciertas hipótesis, esse número poderia caer a em torno de 10.000 ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Esta cifra, no entanto, no é a imagem completa.

En o extremo sob de esse rango, os tempos de execução seguem siendo largos. Factorizar RSA-2048 ao número mínimo de qubits poderia ainda llevar anos de funcionamiento continuo. Una execução mais rápida requer mais qubits, potencialmente decenas de miles. La relação entre ou número de qubits e o tempo de execução no é lineal, e o artigo se cuida de presentar esto como um espectro em vez de um umbral fijo. Lo que cambia é a direção: a barrera ya no é puramente teórica. Es agora uma questão de ingeniería.

### Antiguas hipótesis frente a novas realidades

| Dimensión | Antigua hipótesis | Nueva realidade |
|---|---|---|
| Qubits físicos requeridos (algoritmo de Shor) | ~1.000.000+ | ~10.000–26.000 |
| Tiempo para romper RSA-2048 (ao mínimo de qubits) | Inviable esta década | Años (com 10.000 qubits); mais rápido com mais |
| Tiempo para romper ECC-256 | Inviable esta década | Días (estimado com ~26.000 qubits) |
| Paradigma de hardware dominante | Qubits superconductores | Retículos de átomos neutros reconfigurables |
| Sobrecoste de corrección de errores | Cientos de qubits físicos por qubit lógico | Reducido significativamente mediante códigos de alto rendimiento |
| Naturaleza de a barrera | Teórica | Ingeniería |
| Urgencia de migración | Planificación a longo prazo | Despliegue activo requerido agora |

*Fuente: análisis a partir de [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) e de a literatura anterior.*

## Tiempo, escala e vulnerabilidad desigual de os sistemas criptográficos

Una de as contribuciones mais significativas do artigo é o matiz que introduz em torno do tempo. La ventaja quântica no llega de golpe. Existe ao longo de um espectro determinado por a escala do sistema e a naturaleza do objetivo criptográfico.

Con em torno de 26.000 qubits, os autores estiman que romper a criptografia de curva elíptica poderia llevar uns días em condiciones favorables ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Para RSA-2048, os prazos são considerablemente mais largos. Esta asimetría é importante. Sugiere que distintos sistemas criptográficos podem volverse vulnerables em momentos diferentes, em vez de simultáneamente, e que a transición rumo a os estándares pós-quânticos probablemente no será um acontecimiento único com uma fecha límite única.

Este esquema é coherente com uma cobertura mais amplia. Análisis de os últimos meses sugieren que sistemas quânticos capaces de desafiar o criptografia ampliamente utilizado poderiam emerger antes do final de a década ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")). Los governos e os organismos de normalización planifican ya as transiciones a a criptografia pós-quântica, com calendarios de implementación que se extienden até a década de 2030 ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La discussão tem passado de «si» a «cuándo».

## La brecha de ingeniería que persiste

Conviene ser preciso sobre lo que representa este artigo. Es uma proyección, no uma demostración. Los sistemas propuestos dependen de hipótesis sobre tasas de error, estabilidade do hardware e comportamiento a a escala que ainda no foram validadas a a escala requerida. Los experimentos actuales operan em o nivel de cientos a algunos miles de qubits, no de decenas de miles funcionando de maneira tolerante a fallos durante periodos prolongados ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits")).

Sigue existiendo uma brecha de ingeniería sustancial. El camino de um modelo teórico convincente a um sistema funcional capaz de operação sostenida e tolerante a fallos a essa escala implica desafíos que ainda no se compreendem plenamente, e muito menos se resuelven. Lo que mudou no é a proximidad de uma máquina operativa, mas sim a credibilidad do objetivo. La brecha se estrecha, e a direção do progreso é coherente.

## Por que o calendario que se comprime exige atención agora

La importancia de este trabalho no é que a criptografia vaya a romperse a curto prazo. Es que o calendario se comprime de maneira que afecta a as decisões tomadas hoje. Los sistemas de segurança se diseñan com largos ciclos de vida em mente. Los dados cifrados hoje podem tener que permanecer confidenciales durante décadas. Las decisões de infraestrutura tomadas este ano serão difíciles de invertir em uma ventana de cinco anos. Si as capacidades quânticas llegan antes de lo esperado, estas hipótesis se vuelven frágiles.

Por eso a criptografia pós-quântica ya se está desplegando em os sectores críticos. No porque a amenaza sea inmediata, mas sim porque a transición lleva tempo e o coste de llegar tarde é asimétrico. Hay um patrón recurrente em a historia de a informática: o progreso parece lento hasta que de repente deja de serlo. Lo que comienza como uma mejora teórica se convierte em uma restricción prática, e lo que antes se descartaba como lejano se convierte em algo que há que planificar. La computação quântica poderia seguir exactamente esta trayectoria, no mediante um único avance dramático, mas sim mediante reducciones regulares de coste, complexidade e escala.

## Lo que esto significa por sector: uma guía prática

Las implicaciones de esta investigación no são uniformes em todos os sectores. La resposta apropiada depende do tipo de activos criptográficos em juego, de a sensibilidad e longevidad de os dados implicados, e do ritmo ao que evoluem as expectativas normativas.

### Serviços financeiros e FinTech

Las instituições financeiras afrontan um riesgo compuesto: poseen dados sensibles a longo prazo, operan sobre infraestruturas com ciclos de reemplazo lentos e estão sometidas a um escrutinio normativo creciente em torno de a resiliencia criptográfica. ECC se utiliza ampliamente em as conexões TLS, a autenticação móvel e as firmas digitais em os rails de pago: a categoría criptográfica que o artigo identifica como a mais vulnerable a bajos números de qubits. Las instituciones que ainda no têm comenzado um inventario criptográfico ni têm iniciado uma folha de ruta de migración pós-quântica deveriam tratar este artigo como um incentivo para acelerar, no como um motivo de pánico. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) e CRYSTALS-Dilithium, agora estandarizados por o NIST, são os objetivos de migración apropiados para a encapsulación de claves e as firmas digitais respectivamente.

### Sector público e defensa

Los actores estatales têm a motivación mais fuerte —e, em muitos casos, os recursos— para acelerar o desenvolvimento de hardware quântico mais allá de lo que se conhece públicamente. Los governos que custodian comunicações sensibles, dados de inteligencia ou claves de infraestrutura crítica devem suponer que os adversarios cosechan ya dados cifrados com vistas a um decifragem futuro, uma estrategia comúnmente llamada «harvest now, decrypt later». Para as organizações do sector público, o cumplimiento de os mandatos nacionales de preparación quântica se vuelve cada vez mais ineludible, e a ventana de migración proactiva se estrecha.

### Sanidad e infraestruturas críticas

Los historiales médicos, os sistemas de control de serviços públicos e as redes industriales comparten uma vulnerabilidad común: dados e sistemas com uma vida operativa muito larga, protegidos por estándares criptográficos diseñados para um modelo de amenaza precuántico. Um historial médico criptografia hoje pode tener que permanecer privado durante cincuenta anos. Um sistema de control certificado este ano pode permanecer em serviço durante dois décadas. Para estes sectores, o calendario que se comprime no é uma preocupação abstracta. Es um desafío directo a as hipótesis fundacionales de as arquitecturas de segurança actuales.

## Conclusión

El aspecto mais importante de este artigo no é o número específico de qubits que presenta. Es a direção que esse número implica. La questão ya no é si os computadores quânticos podem desafiar a criptografia moderna. Es a que velocidade podem construirse os sistemas requeridos, e si as organizações que dependen de os estándares actuales reaccionan lo bastante rápido.

Por o momento, as respostas seguem siendo inciertas. Pero o margen para diferir a questão se estrecha, e o coste de esperar cresce com cada reducción creíble do umbral teórico. La comunidade criptográfica, os responsables de segurança e as industrias que dependen de eles harían bien em tratar este artigo no como um motivo de alarma, mas sim como um incentivo serio para acelerar transiciones ya em curso.

## Preguntas frecuentes

**Pueden realmente 10.000 qubits romper o criptografia RSA?**

Teóricamente, sim, com matices importantes. Aunque as estimaciones anteriores sugerían millones de qubits físicos requeridos, novas investigaciones sobre códigos de corrección de errores de alto rendimiento e retículos de átomos neutros reconfigurables sugieren que o umbral é significativamente mais sob. Sin embargo, com 10.000 qubits, o tempo de execução estimado para factorizar RSA-2048 segue siendo extremadamente largo: potencialmente anos de funcionamiento continuo. Los ataques mais rápidos exigen mais qubits, probablemente em o rango de as decenas de miles. El artigo representa uma proyección basada em hipótesis modeladas, no uma demostración em um sistema operativo.

**Qué criptografia está mais em riesgo frente a a computação quântica?**

La criptografia de curva elíptica (ECC) é geralmente mais vulnerable a bajos números de qubits que RSA-2048. El artigo estima que romper ECC poderia llevar algunos días utilizando em torno de 26.000 qubits reconfigurables em condiciones favorables. RSA-2048 requer um tempo de execução significativamente mais largo com números de qubits comparables. Esta asimetría significa que os sistemas dependientes de ECC —comunes em TLS, autenticação móvel e blockchain— podem afrontar o riesgo em um calendario mais corto que as infraestruturas basadas em RSA.

**Qué é um qubit de átomo neutro reconfigurable?**

Los qubits de átomos neutros são átomos individuales —típicamente rubidio ou cesio— atrapados e manipulados mediante luz láser em uma cámara de vacío. «Reconfigurable» significa que a disposición de os átomos pode modificarse dinâmicamente durante o cálculo, permitiendo uma execução mais eficiente de circuitos quânticos complejos. Esta flexibilidade reduce o número de qubits físicos necessários para implementar operações lógicas tolerantes a fallos, e é uma razão clave por a que o novo artigo alcança estimaciones de qubits mais bajas que os trabalhos anteriores basados em as arquitecturas de qubits superconductores.

**Qué é a criptografia pós-quântica, e por que se está desplegando agora?**

La criptografia pós-quântica (PQC) designa os algoritmos criptográficos que se pensam seguros tanto contra computadores clásicos como quânticos. El NIST finalizó seu primer juego de estándares PQC em 2024, incluído [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) para a encapsulación de claves e CRYSTALS-Dilithium para as firmas digitais. El despliegue comienza agora —muito antes de que os computadores quânticos representen uma amenaza inmediata— porque as transiciones criptográficas são lentas. Reemplazar estándares incrustados em toda a infraestrutura mundial lleva típicamente uma década ou mais, e os dados cifrados hoje podem tener que permanecer confidenciales muito depois de que as capacidades quânticas hayan llegado a a madurez.

**Cuántos qubits tem hoje o computador quântico mais potente?**

A principios de 2026, os sistemas quânticos punteros operan em o rango de cientos a algunos miles de qubits físicos. De forma crucial, a maioria ainda no são tolerantes a fallos: operan por embaixo de os umbrales de corrección de errores requeridos para um cálculo lógico sostenido e fiable. La brecha entre ou hardware actual e as decenas de miles de qubits lógicos tolerantes a fallos de alta fidelidad descritos em o novo artigo segue siendo significativa, embora ou ritmo do progreso através de as plataformas superconductora, de átomos neutros e de iones atrapados se acelera.

## Referencias

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
