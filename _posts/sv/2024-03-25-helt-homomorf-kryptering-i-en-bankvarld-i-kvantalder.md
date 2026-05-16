---
title: "El cifrado completamente homomórfico (FHE) en la era bancaria cuántica"
subtitle: "Reforzar la seguridad de los datos, mejorar la confidencialidad de la IA y construir la confianza del cliente en la era de la computación cuántica con el FHE"
description: "Cómo el cifrado completamente homomórfico revoluciona la seguridad de los datos en la banca y las finanzas, garantizando la confidencialidad frente a las amenazas de la computación cuántica."
date: "March 25, 2024"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/fully-homomorphic-encryption.webp"
banner_alt: "Banner del cifrado completamente homomórfico"
keywords: "cifrado completamente homomórfico, seguridad bancaria, computación cuántica, cifrado de datos financieros, FHE, RGPD, CCPA, cumplimiento, computación cloud, IA y confidencialidad, LLM cifrado, Zama, Gentry"
---

El **cifrado completamente homomórfico (FHE — Fully Homomorphic Encryption)** promete redefinir la seguridad de los datos en la banca y las finanzas. Permitiendo cálculos sobre datos cifrados, el FHE protege la confidencialidad frente a las amenazas convencionales y cuánticas.

## Introducción

La implementación del FHE en el sector financiero no es solo teórica; se está convirtiendo en una realidad práctica, transformando los estándares de seguridad y confidencialidad de los datos. Este artículo explora los usos prácticos, las consideraciones normativas, los posibles inconvenientes y los avances de investigación del cifrado completamente homomórfico en finanzas y en las aplicaciones de inteligencia artificial (IA).

## Comprender el cifrado completamente homomórfico

### Las bases del cifrado

El cifrado es un método de transformación de datos legibles (texto claro) en un formato ilegible (criptograma) por medio de un algoritmo y una clave de cifrado. El objetivo principal es asegurar que solo las partes autorizadas puedan acceder a los datos originales descifrando el criptograma con la ayuda de una clave de descifrado.

### Métodos de cifrado tradicionales

Los métodos de cifrado tradicionales pueden categorizarse ampliamente en dos tipos: simétrico y asimétrico. El cifrado simétrico utiliza una sola clave a la vez para el cifrado y el descifrado. Esta eficiencia tiene un coste en seguridad, en particular cuando la distribución de las claves plantea problemas. El cifrado asimétrico, también llamado criptografía de clave pública, utiliza dos claves: una para el cifrado y otra para el descifrado. Este método es más seguro pero más lento que el cifrado simétrico.

### Los límites del cifrado convencional para el cálculo

Aunque los métodos tradicionales aseguran eficazmente los datos en reposo o en tránsito, fracasan cuando se trata de efectuar cálculos sobre datos cifrados. Típicamente, para tratar o analizar datos cifrados, hay que descifrarlos primero, efectuar las operaciones necesarias y luego volver a cifrarlos. Esta etapa de descifrado plantea un riesgo significativo para la confidencialidad, en particular en entornos no confiables o de cloud computing.

![divider][divider].class=\"m-10 w-100\"

## El avance del cifrado homomórfico

El **cifrado homomórfico (HE)** resuelve los límites del cifrado convencional. Permite efectuar ciertos cálculos directamente sobre los datos cifrados (criptogramas). El resultado descifrado es idéntico a los datos originales (texto claro) después de que se hayan efectuado las mismas operaciones. El HE se declina en tres grandes variedades: Partially Homomorphic Encryption (PHE), Somewhat Homomorphic Encryption (SHE) y Fully Homomorphic Encryption (FHE).

- **Partially Homomorphic Encryption (PHE):** soporta operaciones ilimitadas de un solo tipo (adición o multiplicación) sobre los criptogramas.
- **Somewhat Homomorphic Encryption (SHE):** soporta un número limitado de operaciones, combinando adición y multiplicación, pero solo hasta una cierta profundidad.
- **Fully Homomorphic Encryption (FHE):** la forma más avanzada, autorizando operaciones ilimitadas de adición y multiplicación sobre los criptogramas.

### La ingeniosidad técnica del FHE

El FHE reposa sobre estructuras matemáticas complejas, como la criptografía sobre retículos. La criptografía sobre retículos es un tipo de cifrado que utiliza estructuras matemáticas llamadas retículos.

Un retículo es una disposición regular de puntos en el espacio, y la criptografía sobre retículos se apoya en la dificultad de resolver ciertos problemas matemáticos vinculados a estas estructuras. Esto hace que la criptografía sobre retículos sea segura y resistente a los ataques, incluidos los procedentes de los ordenadores cuánticos.

En 2009, Craig Gentry desarrolló un método, descrito en su artículo [**A Fully Homomorphic Encryption Scheme ⧉**][00], para crear un sistema capaz de efectuar una evaluación homomórfica de su propio circuito de descifrado. Este diseño autorreferencial permite a los esquemas FHE efectuar cálculos arbitrarios sobre datos cifrados.

### El proceso del algoritmo FHE

![FHE Operational Flow][fhe].class=\"m-10 w-100\"

El diagrama anterior ilustra el flujo operativo de un algoritmo FHE.

- El proceso de cifrado comienza con los datos en texto claro, que se cifran con la ayuda de una clave de cifrado para generar un criptograma.

- Estos datos cifrados pueden entonces someterse a diversos cálculos directamente sobre el criptograma mediante un proceso conocido como bootstrapping.

- Esta capacidad única del FHE permite a los datos permanecer cifrados durante todo el proceso. Una vez efectuadas las operaciones necesarias, el proceso de descifrado puede reconvertir el criptograma modificado en texto claro gracias al esquema FHE.

La ventaja principal del FHE reside en su capacidad para efectuar cálculos sobre el criptograma sin requerir descifrado, garantizando así el mantenimiento de la confidencialidad y la seguridad de los datos durante todo el cálculo.

### La resistencia cuántica del FHE

Los métodos de cifrado tradicionales son a menudo vulnerables a los algoritmos cuánticos. Estos algoritmos pueden resolver rápidamente problemas como la factorización de enteros y los logaritmos discretos, que constituyen los fundamentos de estos métodos. Por contraste, el FHE emplea problemas sobre retículos que se cree difíciles de resolver por ordenadores cuánticos. Esta resistencia cuántica hace del FHE un método de cifrado prometedor para la era postcuántica.

El FHE sobre retículos es resistente a los ataques cuánticos porque los problemas matemáticos subyacentes, como el Shortest Vector Problem (SVP) y el Closest Vector Problem (CVP), se consideran difíciles de resolver incluso para los ordenadores cuánticos. Si bien algoritmos cuánticos como el de Shor pueden romper los métodos de cifrado tradicionales que reposan en la factorización de grandes números o los logaritmos discretos, no se sabe que ofrezcan ventajas significativas en la resolución de los problemas sobre retículos. Esta característica hace del FHE sobre retículos un candidato prometedor para la criptografía postcuántica.

![divider][divider].class=\"m-10 w-100\"

## El impacto del FHE en la banca y las finanzas

### Confidencialidad y seguridad de los datos reforzadas

La aplicación del FHE en el sector financiero promete un refuerzo significativo de la confidencialidad. Los bancos pueden ahora emprender evaluaciones de riesgos, la detección de fraude y análisis de datos completos al tiempo que garantizan la confidencialidad absoluta de la información de los clientes. Este avance tecnológico mitiga el riesgo de brechas de datos, reforzando la integridad de las plataformas bancarias digitales y las transacciones financieras.

### Cloud computing y externalización

Un ámbito de aplicación principal del cifrado homomórfico es el tratamiento seguro de los datos en la nube. Los bancos pueden aprovechar los servicios de cloud computing para tratar datos cifrados sin comprometer su confidencialidad. Esto permite a las instituciones financieras aprovechar la escalabilidad y la rentabilidad del cloud al tiempo que mantienen la confidencialidad de información financiera sensible.

El movimiento hacia el cloud computing y la externalización de tareas computacionales por parte de los bancos subraya la pertinencia del FHE. Con un cloud computing seguro, las instituciones financieras pueden acceder a recursos externos al tiempo que protegen los datos cifrados sensibles mediante el FHE. El FHE permite a los bancos aprovechar los servicios cloud de manera segura al tiempo que se garantiza que los datos cifrados sensibles permanezcan protegidos en todo momento.

![divider][divider].class=\"m-10 w-100\"

## Prepararse para el futuro cuántico

El advenimiento inminente de la computación cuántica anuncia una potencial crisis para las metodologías de cifrado tradicionales. El FHE sobre retículos es intrínsecamente resistente a los ataques cuánticos, ofreciendo una defensa robusta contra la amenaza que la computación cuántica plantea a la seguridad de los datos.

### Cifrado resistente a lo cuántico

El FHE proporciona una capa formidable de protección contra las amenazas de la computación cuántica. Empleando técnicas criptográficas sobre retículos, el FHE garantiza que los datos financieros y los activos permanezcan seguros incluso frente a adversarios cuánticos.

La resistencia cuántica del FHE se debe a problemas matemáticos subyacentes complejos como el Shortest Vector Problem (SVP) y el Closest Vector Problem (CVP). Se supone que estos problemas son intratables incluso para los ordenadores cuánticos, lo que hace del FHE sobre retículos un candidato ideal para la criptografía postcuántica.

Utilizar un cifrado resistente a lo cuántico, como el FHE, es crucial no solo para proteger los activos financieros sino también para mantener la confianza de los clientes en la era digital. A medida que la computación cuántica progresa, las instituciones financieras que prioricen un cifrado robusto estarán mejor posicionadas para navegar los desafíos y oportunidades futuros.

![divider][divider].class=\"m-10 w-100\"

## El futuro del FHE en la banca y las finanzas

La trayectoria del FHE dentro del sector financiero es prometedora, pero todavía afronta desafíos. El sector bancario puede explotar el pleno potencial del FHE mejorando la tecnología, integrándola en las operaciones financieras cotidianas y cooperando con los reguladores.

El FHE puede utilizarse en diversas aplicaciones bancarias y financieras, como:

- **Análisis seguro de datos financieros**: el FHE permite a los bancos analizar datos financieros cifrados como transacciones, puntuaciones de crédito y carteras de inversión, sin comprometer la confidencialidad del cliente, garantizando un tratamiento seguro de la información sensible.

- **Aprendizaje automático preservando la confidencialidad**: el FHE permite a los bancos entrenar y desplegar modelos de aprendizaje automático sobre datos cifrados, permitiéndoles aprovechar la IA para la detección de fraude, la evaluación de riesgos y la segmentación de clientes a la vez que mantienen la confidencialidad.

- **Cálculo multipartícipe seguro**: el FHE permite una colaboración segura entre varias instituciones financieras, permitiéndoles efectuar cálculos conjuntos sobre datos cifrados sin compartir información sensible, facilitando las transacciones interbancarias seguras y el cumplimiento.

- **Seguridad de las API**: el FHE puede asegurar las API cifrando los datos sensibles antes de la transmisión, garantizando que la información de los clientes permanezca confidencial durante los intercambios entre bancos y servicios terceros.

- **Cloud computing seguro**: el FHE permite a los bancos externalizar de manera segura los cálculos y el almacenamiento de datos hacia plataformas cloud sin comprometer la confidencialidad, ya que los datos permanecen cifrados durante todo el proceso, ampliando el uso de servicios cloud rentables y escalables.

- **Cumplimiento normativo preservando la confidencialidad**: el FHE permite a los bancos compartir datos cifrados con las autoridades reguladoras, permitiendo el cumplimiento de las exigencias de reporting sin exponer información sensible, simplificando el proceso de cumplimiento al tiempo que se mantiene la confidencialidad.

Estas aplicaciones revelan el poder transformador del FHE en la banca y las finanzas y subrayan su potencial para revolucionar los estándares de seguridad y confidencialidad.

![divider][divider].class=\"m-10 w-100\"

## Superar los desafíos de adopción del FHE

### Desafíos de rendimiento y optimización

Abordar el sobrecoste computacional intrínseco al FHE sigue siendo un desafío pivote. Los recientes progresos en optimización de algoritmos y en desarrollo de aceleradores de hardware especializados reducen la brecha de rendimiento entre el cálculo tradicional y el FHE.

### Estandarización y colaboración

La vía hacia una adopción generalizada del FHE depende de la estandarización de los protocolos y de una colaboración reforzada entre las partes interesadas del ecosistema financiero. Un enfoque unificado para abrazar el FHE puede acelerar significativamente su integración con los servicios financieros generalistas.

### Regulación y cumplimiento

Los organismos reguladores desempeñan un papel crítico en la adopción del FHE, con leyes sobre la confidencialidad de los datos que imponen su uso. Un impulso normativo podría servir como catalizador para la adopción completa del FHE en toda la industria bancaria y financiera, a la vez que se garantiza el cumplimiento de las normativas de protección de datos.

El panorama normativo en torno a la confidencialidad y la seguridad de los datos desempeña un papel significativo en la adopción del FHE en el sector bancario. Normativas estrictas como el RGPD (General Data Protection Regulation) y el CCPA (California Consumer Privacy Act) imponen medidas robustas de protección de datos y subrayan el derecho individual a la vida privada. El FHE, con su capacidad para tratar datos cifrados sin descifrado, se alinea bien con la orientación centrada en la confidencialidad de estas normativas. A medida que las leyes sobre la confidencialidad se vuelven más estrictas, el FHE ofrece una solución convincente que permite a los bancos efectuar los cálculos y análisis necesarios al tiempo que se respetan las exigencias de cumplimiento.

![divider][divider].class=\"m-10 w-100\"

## Asegurar los grandes modelos de lenguaje con el FHE

Los grandes modelos de lenguaje (LLM) son potentes herramientas de IA. Pero su uso suscita preocupaciones de confidencialidad, en particular cuando tratan datos de usuario sensibles. El FHE ofrece una solución que protege la confidencialidad del usuario y preserva la propiedad intelectual de los propietarios de modelos permitiendo cálculos sobre datos cifrados.

### Desafíos de confidencialidad con los LLM

Desplegar un LLM en local para mantener la confidencialidad de los datos plantea desafíos como costes elevados y la exposición potencial de una propiedad intelectual valiosa. El FHE aborda estos desafíos permitiendo a los LLM funcionar sobre datos de usuario cifrados, garantizando la confidencialidad y la seguridad del modelo simultáneamente.

### El enfoque LLM cifrado de Zama

[**Zama ⧉**][01], una empresa de tecnologías de confidencialidad, ha demostrado la viabilidad de construir un LLM cifrado con la ayuda del FHE. Su enfoque, que combina FHE y otras tecnologías que refuerzan la confidencialidad, alcanza rendimientos comparables a los modelos no cifrados con solo un aumento modesto del sobrecoste computacional.

### Mejorar la confidencialidad del usuario con LLM cifrados

La integración del FHE con los LLM tiene el potencial de transformar la confidencialidad del usuario, en particular en las aplicaciones que tratan información personal o profesional sensible. A medida que la IA se concentra más en la confidencialidad, es importante que desarrolladores, usuarios y reguladores trabajen juntos. Esta colaboración es clave para construir un ecosistema de IA que ponga la seguridad y la confidencialidad en primer lugar.

![divider][divider].class=\"m-10 w-100\"

## Conclusión

El **cifrado completamente homomórfico (FHE)** es una tecnología de seguridad de los datos revolucionaria que ofrece una confidencialidad y una seguridad excepcionales a la banca y las finanzas.

A medida que la computación cuántica avanza, el FHE se vuelve aún más crucial. Su adopción remodelará la ciberseguridad en los servicios financieros, haciendo la banca digital más digna de confianza y más segura en nuestro mundo cada vez más conectado.

El advenimiento del FHE también ha abierto nuevas posibilidades de uso seguro y privado de los grandes modelos de lenguaje. Permitiendo LLM cifrados, el FHE garantiza que los datos del usuario permanezcan confidenciales al tiempo que se benefician de las capacidades avanzadas de estos modelos.

La era de la computación cuántica se aproxima. Los bancos deben evaluar proactivamente su infraestructura de cifrado, identificar las vulnerabilidades potenciales y desarrollar una hoja de ruta clara para la adopción del FHE con el fin de proteger los datos y mantener la confianza del cliente.

[00]: https://crypto.stanford.edu/craig/ "The original paper by Craig Gentry on Fully Homomorphic Encryption"
[01]: https://zama.ai/ "Zama - Fully Homomorphic Encryption"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[fhe]: https://cloudcdn.pro/stocks/diagrams/fhe_algorithm_diagram.webp "FHE Architecture"
