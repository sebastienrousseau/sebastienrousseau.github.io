---
title: "Los umbrales cuánticos vuelven a moverse"
subtitle: "Un nuevo artículo sugiere que el algoritmo de Shor podría ejecutarse con solo 10.000 qubits. El umbral de la computación cuántica criptográficamente relevante cae más rápido de lo que la mayoría suponía."
description: "Un nuevo artículo sugiere que el algoritmo de Shor podría ejecutarse con solo 10.000 qubits. El umbral de la computación cuántica criptográficamente relevante cae más rápido de lo que la mayoría suponía."
date: "April 11, 2026"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/leo_visions-Q_y8ZzhQ2_s-unsplash.webp"
banner_alt: "Esquema del umbral de qubits para el algoritmo de Shor. Placa de circuito de computación cuántica con reflejos azules"
keywords: "algoritmo de Shor, qubits, computación cuántica, ECC, RSA-2048, átomos neutros reconfigurables, códigos de corrección de errores, CRYSTALS-Kyber, CRYSTALS-Dilithium, PQC, criptografía postcuántica"
---


> **TL;DR.** Tento článek je DRAFT překlad původně španělského zdroje, čekající na revizi rodilým mluvčím. Hlavní obsah, příklady a citace zůstávají ve španělštině; pouze záhlaví/frontmatter byly přepnuty na češtinu.

**Klíčové body**

## Los umbrales cuánticos vuelven a moverse

Un nuevo artículo sugiere que el algoritmo de Shor podría ejecutarse con solo 10.000 qubits. El umbral de la computación cuántica criptográficamente relevante cae más rápido de lo que la mayoría suponía.

> **TL;DR.** Un nuevo artículo propone que el algoritmo de Shor pueda ejecutarse con solo 10.000 qubits físicos —cerca de cien veces menos que las estimaciones consensuadas anteriores—. La barrera ya no es puramente teórica: es de ingeniería. Los estándares de criptografía postcuántica ya están finalizados; la prioridad ahora es acelerar la migración.
>
> **Conclusiones clave**
>
> - Un nuevo artículo propone que el algoritmo de Shor pueda ejecutarse con solo **10.000 qubits físicos**, alrededor de cien veces menos que las estimaciones consensuadas anteriores.
> - La reducción está impulsada por tres avances convergentes: códigos de corrección de errores cuánticos de alto rendimiento, retículos de átomos neutros reconfigurables y paralelismo aumentado.
> - La amenaza no es uniforme. La **criptografía de curva elíptica (ECC)** es más vulnerable a bajos números de qubits; RSA-2048 requiere tiempos de ejecución significativamente más largos a escalas comparables.
> - Se trata de una **proyección teórica**, no de una demostración operativa. Sigue existiendo una brecha de ingeniería sustancial entre el hardware actual y la ejecución tolerante a fallos a esa escala.
> - Los estándares de criptografía postcuántica ya están finalizados. La prioridad ahora es **acelerar la migración**, no esperar a que aparezca un sistema cuántico.

## Una hipótesis familiar, ahora bajo presión

A lo largo de la última década, las discusiones en torno a la computación cuántica y la criptografía han seguido un arco familiar. Las máquinas cuánticas eran reconocidas como teóricamente potentes, pero consideradas impracticables a gran escala. Romper los sistemas criptográficos modernos habría exigido millones de qubits físicos, y el calendario permanecía cómodamente lejano. Esta hipótesis está ahora bajo presión seria.

Un artículo reciente, [«Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits» ⧉](https://arxiv.org/pdf/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (PDF)"), propone algo más consecuente que un simple avance. Sugiere que el umbral de la computación cuántica criptográficamente relevante podría ser inferior en un orden de magnitud a lo que se creía. No millones de qubits, sino decenas de miles. La distinción importa, y la dirección que implica es difícil de ignorar.

## La convergencia que impulsa este desplazamiento: corrección de errores, arquitectura y paralelismo

El resultado no emerge de un descubrimiento único. Refleja una convergencia de mejoras en varias capas de la pila de la computación cuántica que, tomadas juntas, desplazan la frontera de lo que parece factible.

La primera mejora se refiere a la corrección de errores. Los enfoques tradicionales exigían grandes sobrecostes —a menudo cientos de qubits físicos para representar un solo qubit lógico—. El artículo se apoya en cambio en códigos de corrección de errores cuánticos de alto rendimiento, que reducen significativamente ese sobrecoste ([Emergent Mind ⧉](https://www.emergentmind.com/papers/2603.28627 "Shor's Algorithm with 10000 Atomic Qubits")). La segunda se refiere a la arquitectura. El sistema está construido sobre retículos reconfigurables de átomos neutros, que pueden reorganizarse durante el cálculo para permitir una conectividad más flexible y una ejecución más eficiente ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La tercera es el paralelismo: aumentar el número de qubits permite ejecutar más operaciones simultáneamente, reduciendo el tiempo de ejecución global.

Ninguna de estas ideas es nueva aisladamente. Combinadas, sin embargo, redefinen lo que antes se trataba como un límite duro.

## De millones a decenas de miles: lo que las cifras significan realmente

Durante años, la estimación consensuada para ejecutar el algoritmo de Shor a escalas criptográficas exigía millones de qubits físicos. El nuevo análisis sugiere que, bajo ciertas hipótesis, ese número podría caer a alrededor de 10.000 ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Esta cifra, sin embargo, no es la imagen completa.

En el extremo bajo de ese rango, los tiempos de ejecución siguen siendo largos. Factorizar RSA-2048 al número mínimo de qubits podría aún llevar años de funcionamiento continuo. Una ejecución más rápida requiere más qubits, potencialmente decenas de miles. La relación entre el número de qubits y el tiempo de ejecución no es lineal, y el artículo se cuida de presentar esto como un espectro en lugar de un umbral fijo. Lo que cambia es la dirección: la barrera ya no es puramente teórica. Es ahora una cuestión de ingeniería.

### Antiguas hipótesis frente a nuevas realidades

| Dimensión | Antigua hipótesis | Nueva realidad |
|---|---|---|
| Qubits físicos requeridos (algoritmo de Shor) | ~1.000.000+ | ~10.000–26.000 |
| Tiempo para romper RSA-2048 (al mínimo de qubits) | Inviable esta década | Años (con 10.000 qubits); más rápido con más |
| Tiempo para romper ECC-256 | Inviable esta década | Días (estimado con ~26.000 qubits) |
| Paradigma de hardware dominante | Qubits superconductores | Retículos de átomos neutros reconfigurables |
| Sobrecoste de corrección de errores | Cientos de qubits físicos por qubit lógico | Reducido significativamente mediante códigos de alto rendimiento |
| Naturaleza de la barrera | Teórica | Ingeniería |
| Urgencia de migración | Planificación a largo plazo | Despliegue activo requerido ahora |

*Fuente: análisis a partir de [arXiv:2603.28627 ⧉](https://arxiv.org/abs/2603.28627) y de la literatura anterior.*

## Tiempo, escala y vulnerabilidad desigual de los sistemas criptográficos

Una de las contribuciones más significativas del artículo es el matiz que introduce en torno al tiempo. La ventaja cuántica no llega de golpe. Existe a lo largo de un espectro determinado por la escala del sistema y la naturaleza del objetivo criptográfico.

Con alrededor de 26.000 qubits, los autores estiman que romper la criptografía de curva elíptica podría llevar unos días en condiciones favorables ([arXiv ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits")). Para RSA-2048, los plazos son considerablemente más largos. Esta asimetría es importante. Sugiere que distintos sistemas criptográficos pueden volverse vulnerables en momentos diferentes, en lugar de simultáneamente, y que la transición hacia los estándares postcuánticos probablemente no será un acontecimiento único con una fecha límite única.

Este esquema es coherente con una cobertura más amplia. Análisis de los últimos meses sugieren que sistemas cuánticos capaces de desafiar el cifrado ampliamente utilizado podrían emerger antes del final de la década ([Nature ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption")). Los gobiernos y los organismos de normalización planifican ya las transiciones a la criptografía postcuántica, con calendarios de implementación que se extienden hasta la década de 2030 ([The Quantum Insider ⧉](https://thequantuminsider.com/2026/03/31/oratomic-launches-to-build-utility-scale-quantum-computers/ "Oratomic Launches to Build Utility-scale Quantum Computers")). La discusión ha pasado de «si» a «cuándo».

## La brecha de ingeniería que persiste

Conviene ser preciso sobre lo que representa este artículo. Es una proyección, no una demostración. Los sistemas propuestos dependen de hipótesis sobre tasas de error, estabilidad del hardware y comportamiento a la escala que aún no han sido validadas a la escala requerida. Los experimentos actuales operan en el nivel de cientos a algunos miles de qubits, no de decenas de miles funcionando de manera tolerante a fallos durante periodos prolongados ([Phys.org ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits")).

Sigue existiendo una brecha de ingeniería sustancial. El camino de un modelo teórico convincente a un sistema funcional capaz de operación sostenida y tolerante a fallos a esa escala implica desafíos que aún no se comprenden plenamente, y mucho menos se resuelven. Lo que ha cambiado no es la proximidad de una máquina operativa, sino la credibilidad del objetivo. La brecha se estrecha, y la dirección del progreso es coherente.

## Por qué el calendario que se comprime exige atención ahora

La importancia de este trabajo no es que la criptografía vaya a romperse a corto plazo. Es que el calendario se comprime de manera que afecta a las decisiones tomadas hoy. Los sistemas de seguridad se diseñan con largos ciclos de vida en mente. Los datos cifrados hoy pueden tener que permanecer confidenciales durante décadas. Las decisiones de infraestructura tomadas este año serán difíciles de invertir en una ventana de cinco años. Si las capacidades cuánticas llegan antes de lo esperado, estas hipótesis se vuelven frágiles.

Por eso la criptografía postcuántica ya se está desplegando en los sectores críticos. No porque la amenaza sea inmediata, sino porque la transición lleva tiempo y el coste de llegar tarde es asimétrico. Hay un patrón recurrente en la historia de la informática: el progreso parece lento hasta que de repente deja de serlo. Lo que comienza como una mejora teórica se convierte en una restricción práctica, y lo que antes se descartaba como lejano se convierte en algo que hay que planificar. La computación cuántica podría seguir exactamente esta trayectoria, no mediante un único avance dramático, sino mediante reducciones regulares de coste, complejidad y escala.

## Lo que esto significa por sector: una guía práctica

Las implicaciones de esta investigación no son uniformes en todos los sectores. La respuesta apropiada depende del tipo de activos criptográficos en juego, de la sensibilidad y longevidad de los datos implicados, y del ritmo al que evolucionan las expectativas normativas.

### Servicios financieros y FinTech

Las instituciones financieras afrontan un riesgo compuesto: poseen datos sensibles a largo plazo, operan sobre infraestructuras con ciclos de reemplazo lentos y están sometidas a un escrutinio normativo creciente en torno a la resiliencia criptográfica. ECC se utiliza ampliamente en las conexiones TLS, la autenticación móvil y las firmas digitales en los rails de pago: la categoría criptográfica que el artículo identifica como la más vulnerable a bajos números de qubits. Las instituciones que aún no han comenzado un inventario criptográfico ni han iniciado una hoja de ruta de migración postcuántica deberían tratar este artículo como un incentivo para acelerar, no como un motivo de pánico. [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) y CRYSTALS-Dilithium, ahora estandarizados por el NIST, son los objetivos de migración apropiados para la encapsulación de claves y las firmas digitales respectivamente.

### Sector público y defensa

Los actores estatales tienen la motivación más fuerte —y, en muchos casos, los recursos— para acelerar el desarrollo de hardware cuántico más allá de lo que se conoce públicamente. Los gobiernos que custodian comunicaciones sensibles, datos de inteligencia o claves de infraestructura crítica deben suponer que los adversarios cosechan ya datos cifrados con vistas a un descifrado futuro, una estrategia comúnmente llamada «harvest now, decrypt later». Para las organizaciones del sector público, el cumplimiento de los mandatos nacionales de preparación cuántica se vuelve cada vez más ineludible, y la ventana de migración proactiva se estrecha.

### Sanidad e infraestructuras críticas

Los historiales médicos, los sistemas de control de servicios públicos y las redes industriales comparten una vulnerabilidad común: datos y sistemas con una vida operativa muy larga, protegidos por estándares criptográficos diseñados para un modelo de amenaza precuántico. Un historial médico cifrado hoy puede tener que permanecer privado durante cincuenta años. Un sistema de control certificado este año puede permanecer en servicio durante dos décadas. Para estos sectores, el calendario que se comprime no es una preocupación abstracta. Es un desafío directo a las hipótesis fundacionales de las arquitecturas de seguridad actuales.

## Conclusión

El aspecto más importante de este artículo no es el número específico de qubits que presenta. Es la dirección que ese número implica. La cuestión ya no es si los ordenadores cuánticos pueden desafiar la criptografía moderna. Es a qué velocidad pueden construirse los sistemas requeridos, y si las organizaciones que dependen de los estándares actuales reaccionan lo bastante rápido.

Por el momento, las respuestas siguen siendo inciertas. Pero el margen para diferir la cuestión se estrecha, y el coste de esperar crece con cada reducción creíble del umbral teórico. La comunidad criptográfica, los responsables de seguridad y las industrias que dependen de ellos harían bien en tratar este artículo no como un motivo de alarma, sino como un incentivo serio para acelerar transiciones ya en curso.

## Preguntas frecuentes

**¿Pueden realmente 10.000 qubits romper el cifrado RSA?**

Teóricamente, sí, con matices importantes. Aunque las estimaciones anteriores sugerían millones de qubits físicos requeridos, nuevas investigaciones sobre códigos de corrección de errores de alto rendimiento y retículos de átomos neutros reconfigurables sugieren que el umbral es significativamente más bajo. Sin embargo, con 10.000 qubits, el tiempo de ejecución estimado para factorizar RSA-2048 sigue siendo extremadamente largo: potencialmente años de funcionamiento continuo. Los ataques más rápidos exigen más qubits, probablemente en el rango de las decenas de miles. El artículo representa una proyección basada en hipótesis modeladas, no una demostración en un sistema operativo.

**¿Qué cifrado está más en riesgo frente a la computación cuántica?**

La criptografía de curva elíptica (ECC) es generalmente más vulnerable a bajos números de qubits que RSA-2048. El artículo estima que romper ECC podría llevar algunos días utilizando alrededor de 26.000 qubits reconfigurables en condiciones favorables. RSA-2048 requiere un tiempo de ejecución significativamente más largo con números de qubits comparables. Esta asimetría significa que los sistemas dependientes de ECC —comunes en TLS, autenticación móvil y blockchain— pueden afrontar el riesgo en un calendario más corto que las infraestructuras basadas en RSA.

**¿Qué es un qubit de átomo neutro reconfigurable?**

Los qubits de átomos neutros son átomos individuales —típicamente rubidio o cesio— atrapados y manipulados mediante luz láser en una cámara de vacío. «Reconfigurable» significa que la disposición de los átomos puede modificarse dinámicamente durante el cálculo, permitiendo una ejecución más eficiente de circuitos cuánticos complejos. Esta flexibilidad reduce el número de qubits físicos necesarios para implementar operaciones lógicas tolerantes a fallos, y es una razón clave por la que el nuevo artículo alcanza estimaciones de qubits más bajas que los trabajos anteriores basados en las arquitecturas de qubits superconductores.

**¿Qué es la criptografía postcuántica, y por qué se está desplegando ahora?**

La criptografía postcuántica (PQC) designa los algoritmos criptográficos que se piensan seguros tanto contra ordenadores clásicos como cuánticos. El NIST finalizó su primer juego de estándares PQC en 2024, incluido [CRYSTALS-Kyber](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) para la encapsulación de claves y CRYSTALS-Dilithium para las firmas digitales. El despliegue comienza ahora —mucho antes de que los ordenadores cuánticos representen una amenaza inmediata— porque las transiciones criptográficas son lentas. Reemplazar estándares incrustados en toda la infraestructura mundial lleva típicamente una década o más, y los datos cifrados hoy pueden tener que permanecer confidenciales mucho después de que las capacidades cuánticas hayan llegado a la madurez.

**¿Cuántos qubits tiene hoy el ordenador cuántico más potente?**

A principios de 2026, los sistemas cuánticos punteros operan en el rango de cientos a algunos miles de qubits físicos. De forma crucial, la mayoría aún no son tolerantes a fallos: operan por debajo de los umbrales de corrección de errores requeridos para un cálculo lógico sostenido y fiable. La brecha entre el hardware actual y las decenas de miles de qubits lógicos tolerantes a fallos de alta fidelidad descritos en el nuevo artículo sigue siendo significativa, aunque el ritmo del progreso a través de las plataformas superconductora, de átomos neutros y de iones atrapados se acelera.

## Referencias

- Sebastien Rousseau, (2025). [Quantum-Safe Payments: Why the Payments Industry Must Act Now](https://sebastienrousseau.com/2025-09-01-quantum-safe-payments-epaa/index.html "Quantum-Safe Payments: Why the Payments Industry Must Act Now").
- Sebastien Rousseau, (2023). [Quantum Key Distribution: Revolutionising Security in Banking](https://sebastienrousseau.com/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html "Quantum Key Distribution: Revolutionising Security in Banking").
- Sebastien Rousseau, (2023). [CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age](https://sebastienrousseau.com/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html "CRYSTALS-Kyber: The Safeguarding Algorithm in a Quantum Age").
- Anonymous, (2026). [Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits ⧉](https://arxiv.org/abs/2603.28627 "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits"). arXiv preprint arXiv:2603.28627.
- Castelvecchi, D. (2026). [Quantum-computing breakthroughs pose risks to encryption ⧉](https://www.nature.com/articles/d41586-026-01054-1 "Quantum-computing breakthroughs pose risks to encryption"). Nature.
- Phys.org, (2026). [Useful quantum computers could be built with as few as 10,000 qubits ⧉](https://phys.org/news/2026-04-quantum-built-qubits-team.html "Useful quantum computers could be built with as few as 10,000 qubits"). Phys.org.
