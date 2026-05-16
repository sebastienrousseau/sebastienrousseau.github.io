---
title: "CRYSTALS-Kyber: el algoritmo de protección en la era cuántica"
subtitle: "CRYSTALS-Kyber, el estándar NIST FIPS 203 para la encapsulación de claves postcuántica"
description: "Cómo CRYSTALS-Kyber, algoritmo de criptografía resistente a lo cuántico, revoluciona el mundo de la criptografía y nos prepara para la era cuántica."
date: "November 19, 2023"
language: "th-TH"
locale: "th_TH"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp"
banner_alt: "Un ordenador cuántico moderno y depurado"
keywords: "computación cuántica, criptografía resistente a lo cuántico, CRYSTALS-Kyber, criptografía, seguridad, banca, finanzas, cifrado, protección de datos, perdurabilidad"
---


> **TL;DR.** บทความนี้เป็น DRAFT แปลจากต้นฉบับภาษาสเปน รอการตรวจสอบโดยเจ้าของภาษา เนื้อหาหลัก ตัวอย่าง และการอ้างอิงยังคงเป็นภาษาสเปน เฉพาะ frontmatter เท่านั้นที่ถูกเปลี่ยนเป็นภาษาไทย

**ประเด็นสำคัญ**

![AI, Artificial Intelligence concept,3d rendering,conceptual image](https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp).class=\"img-fluid clearfix\"

## Perspectiva

### Navegar por la amenaza cuántica: la génesis de CRYSTALS-Kyber

En mi artículo anterior, [Proteger los datos en la era cuántica ⧉][03], me sumergí en la amenaza inminente de la computación cuántica para la seguridad digital y examiné cómo la criptografía resistente a lo cuántico (QRC) puede responder a ella. Ahora voy a explorar `CRYSTALS-Kyber`, un algoritmo QRC revolucionario que transforma el panorama de la seguridad.

Los ordenadores cuánticos, con su capacidad para realizar ciertos cálculos mucho más rápido que los ordenadores clásicos, plantean un riesgo significativo para los algoritmos de cifrado actuales. Esto suscita inquietudes sobre la seguridad de la información sensible: transacciones financieras, historiales médicos y comunicaciones personales.

Para mitigar esta amenaza, los criptógrafos han desarrollado algoritmos QRC como `CRYSTALS-Kyber`. Este algoritmo es un mecanismo de encapsulación de claves (KEM) diseñado para intercambiar de forma segura claves secretas entre partes.

Hoy, `CRYSTALS-Kyber` es un líder del proceso de estandarización postcuántica del [National Institute of Standards and Technology (NIST) ⧉][05], demostrando su potencial como solución de seguridad robusta en la era digital.

### CRYSTALS-Kyber: seguridad inquebrantable frente a la computación cuántica

La seguridad de `CRYSTALS-Kyber` reposa en la dificultad inherente a resolver el problema `Learning With Errors (LWE)` sobre retículos de módulos. Este desafío matemático complejo, considerado computacionalmente intratable incluso para los ordenadores cuánticos, sirve de zócalo a la resistencia de `CRYSTALS-Kyber` frente a los ataques cuánticos.

### CRYSTALS-Kyber: un cambio de paradigma en seguridad digital

`CRYSTALS-Kyber` pertenece a la suite de algoritmos CRYSTALS (Cryptographic Suite for Algebraic Lattices) y porta con orgullo la distinción de algoritmo cuántico-seguro (QSA).

Si bien el concepto de utilizar problemas sobre retículos con fines criptográficos no es enteramente nuevo, `CRYSTALS-Kyber` eleva ese concepto a niveles de eficiencia sin parangón. Su capacidad para generar claves criptográficas con tamaños más pequeños y velocidades de cifrado/descifrado más rápidas lo convierten en una elección ideal para las aplicaciones reales, en particular en el exigente mundo de las finanzas.

![Divider][01].class=\"m-10 w-100\"

## Idea

### Comprender la mecánica de CRYSTALS-Kyber: la encapsulación de claves en el núcleo

En el núcleo del diseño revolucionario de `CRYSTALS-Kyber` se encuentra su enfoque innovador de la encapsulación de claves, componente crítico de la comunicación segura. Aprovecha la potencia de la criptografía sobre retículos, método reconocido por su resistencia frente a los ataques cuánticos. Esta técnica sofisticada saca partido de estructuras geométricas en un espacio multidimensional para establecer claves criptográficas.

`CRYSTALS-Kyber` emplea un tipo específico de problema sobre retículos, conocido por sus propiedades de eficiencia y seguridad, para generar las claves criptográficas. Esto garantiza la protección de los datos sensibles incluso frente a los avances de la computación cuántica.

#### Encapsulación de claves segura: la esencia de CRYSTALS-Kyber

La encapsulación de claves es semejante a guardar un mensaje en una caja de manera segura, donde solo el destinatario previsto posee la llave para abrirla. En criptografía, este proceso implica crear un par de claves: una clave pública, que puede compartirse abiertamente, y una clave privada, que debe mantenerse secreta. El brillo de `CRYSTALS-Kyber` reside en su capacidad para generar y utilizar estas claves de una manera que garantiza una seguridad sin parangón.

Veamos cómo `CRYSTALS-Kyber` utiliza la encapsulación de claves para establecer una comunicación segura entre dos partes, Alice y Bob. El diagrama de secuencia siguiente ilustra los pasos involucrados, utilizando `CRYSTALS-Kyber`, un KEM diseñado para proporcionar un intercambio de claves seguro para los protocolos criptográficos. El KyberServer desempeña aquí un papel pivote en este proceso, generando y distribuyendo las claves criptográficas requeridas.

![CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)][04].class=\"img-fluid clearfix\"

##### Leyenda

- Alice: emisor del mensaje.
- Bob: receptor del mensaje.
- KyberServer: servidor que genera y distribuye las claves criptográficas.

##### Explicación

###### Intercambio de clave pública

- Alice inicia el proceso solicitando su clave pública al KyberServer.
- El KyberServer responde enviando la clave pública de Alice, un valor matemático que puede compartirse públicamente sin comprometer la seguridad de la clave privada de Alice.
- Alice comparte después su clave pública con Bob, permitiéndole cifrar mensajes que solo Alice puede descifrar.

###### Encapsulación y desencapsulación

- Bob solicita una clave de encapsulación al KyberServer. Esta clave temporal servirá para cifrar la clave secreta compartida antes de enviarla a Alice.
- El KyberServer envía la clave de encapsulación a Bob.
- Bob utiliza la clave pública de Alice y la clave de encapsulación para cifrar la clave secreta compartida, creando una cápsula cifrada.
- Bob envía la cápsula cifrada a Alice.
- Alice solicita una clave de descifrado al KyberServer. Esta clave temporal servirá para descifrar la cápsula y revelar la clave secreta compartida.
- El KyberServer envía la clave de descifrado a Alice.

###### Intercambio de clave secreta compartida

- Alice utiliza su clave privada y la clave de descifrado para descifrar la cápsula, revelando la clave secreta compartida.
- Alice comparte la clave secreta compartida con Bob, permitiéndole descifrar los mensajes cifrados con esta clave.

###### Comunicación segura

El diagrama ilustra eficazmente las etapas complejas de establecimiento de un canal de comunicación seguro, subrayando el papel crucial del KyberServer en la generación y distribución de las claves criptográficas. Al emplear el KEM `CRYSTALS-Kyber`, Alice y Bob pueden proteger su información sensible y mantener una comunicación segura incluso frente a adversarios potenciales.

### Criptografía sobre retículos: un fundamento robusto para la resistencia cuántica

`CRYSTALS-Kyber` emplea un enfoque basado en retículos, método reconocido por su potencial de resistencia a los ataques cuánticos. El principio subyacente de la criptografía sobre retículos implica estructuras geométricas en un espacio multidimensional. Si bien navegar por estas estructuras complejas puede parecer intimidante, `CRYSTALS-Kyber` lo simplifica. Utiliza un tipo específico de problema sobre retículos, conocido por sus propiedades de eficiencia y seguridad, para crear claves criptográficas.

#### Tamaños de clave eficientes: equilibrio entre seguridad y rendimiento

Una de las características destacadas de `CRYSTALS-Kyber` es el tamaño de sus claves. Comparado con otros algoritmos postcuánticos, `CRYSTALS-Kyber` ofrece tamaños de clave significativamente más pequeños, haciéndolo más práctico para las aplicaciones reales. `CRYSTALS-Kyber` propone tres niveles de seguridad, cada uno con su propio tamaño de clave:

- **Kyber512**: nivel de seguridad de 128 bits, con tamaños de clave de 1.632 bytes para las claves secretas, 800 bytes para las claves públicas y 768 bytes para los criptogramas.
- **Kyber768**: nivel de seguridad de 192 bits, con tamaños de clave de 2.400 bytes para las claves secretas, 1.184 bytes para las claves públicas y 1.088 bytes para los criptogramas.
- **Kyber1024**: nivel de seguridad de 256 bits, con tamaños de clave de 3.168 bytes para las claves secretas, 1.568 bytes para las claves públicas y 1.568 bytes para los criptogramas.

Estos tamaños relativamente pequeños hacen que `CRYSTALS-Kyber` sea atractivo para los dispositivos con recursos limitados: smartphones y dispositivos IoT. Reducen también el ancho de banda requerido para transmitir las claves, lo que puede ser beneficioso para las aplicaciones con conectividad de red limitada.

#### Velocidad inquebrantable: un faro en el panorama financiero veloz

Otro aspecto del atractivo de `CRYSTALS-Kyber` es su velocidad. En el sector bancario y financiero veloz, la velocidad cuenta tanto como la seguridad. El diseño del algoritmo garantiza que opere rápidamente, facilitando procesos de cifrado y descifrado veloces. Esta eficiencia no se hace a costa de la seguridad; más bien es un resultado directo de los fundamentos matemáticos sofisticados del algoritmo.

### CRYSTALS-Kyber: una simbiosis de seguridad, eficiencia y velocidad

`CRYSTALS-Kyber` ha emergido como un líder en la búsqueda de criptografía resistente a lo cuántico, ofreciendo una combinación única de seguridad, eficiencia y velocidad. Su enfoque innovador basado en retículos, sus tamaños de clave más pequeños y su diseño optimizado lo convierten en una elección ideal para proteger la información sensible en la banca y los servicios financieros. Mientras el mundo continúa abrazando las tecnologías digitales, `CRYSTALS-Kyber` se posiciona para desempeñar un papel pivote en la protección de nuestros datos en los próximos años.

![Divider][01].class=\"m-10 w-100\"

## Impacto

### CRYSTALS-Kyber: ventajas para la banca y los servicios financieros

La industria bancaria y financiera está en una carrera constante por adelantarse a ciberamenazas cada vez más sofisticadas. En este contexto, `CRYSTALS-Kyber` se distingue no solo por sus propiedades resistentes a lo cuántico (QR) sino también por los beneficios tangibles que ofrece a esta industria. Esta sección detalla las ventajas prácticas de `CRYSTALS-Kyber`, subrayando por qué es particularmente adecuado para las necesidades únicas de las instituciones financieras.

- **Seguridad reforzada con claves más pequeñas**: una de las ventajas más significativas de `CRYSTALS-Kyber` es su capacidad para crear claves de cifrado más pequeñas sin sacrificar la seguridad. En un sector donde las brechas de datos pueden tener consecuencias catastróficas, una seguridad robusta no es negociable. Los tamaños de clave más pequeños de `CRYSTALS-Kyber` simplifican los procesos de gestión de claves, factor crítico en los grandes sistemas bancarios donde miles de claves están en juego. Esto no solo refuerza la seguridad, sino que también optimiza la eficiencia de almacenamiento y transmisión, factor crucial en una época en que la velocidad y el espacio son valiosos.

- **Velocidad y eficiencia**: en los servicios financieros, donde las transacciones se producen en milisegundos, la velocidad de las operaciones criptográficas es crucial. `CRYSTALS-Kyber` sobresale en este aspecto, ofreciendo procesos rápidos de generación de claves, encapsulación y desencapsulación. Esta velocidad garantiza que las medidas de seguridad no se conviertan en un cuello de botella en los entornos de trading de alta frecuencia o durante transacciones a gran escala. Además, la eficiencia de `CRYSTALS-Kyber` se traduce en una reducción de los recursos de cálculo, conduciendo a ahorros de coste y a operaciones más respetuosas con el medio ambiente.

- **Perdurabilidad frente a las amenazas cuánticas**: con el advenimiento de la computación cuántica, la industria afronta un futuro en el que los métodos criptográficos tradicionales podrían quedar obsoletos. Al adoptar `CRYSTALS-Kyber`, las instituciones financieras no solo aseguran su presente sino que también se preparan para un mundo postcuántico. Este enfoque proactivo de la ciberseguridad demuestra un compromiso con la protección a largo plazo de los datos, consideración esencial para las partes interesadas y los clientes que priorizan la seguridad.

- **Cumplimiento normativo y ventaja competitiva**: a medida que los reguladores mundiales empiezan a reconocer la amenaza cuántica, es probable que impongan la adopción de algoritmos resistentes a lo cuántico. La adopción temprana de `CRYSTALS-Kyber` posiciona a las instituciones financieras como líderes en cumplimiento y seguridad. Además, ofrece una ventaja competitiva, tranquilizando a clientes y socios sobre el compromiso de la institución con prácticas de seguridad punteras.

![Divider][01].class=\"m-10 w-100\"

## Incentivos

### El caso para la adopción de CRYSTALS-Kyber

En un panorama donde la ciberseguridad no es solo una necesidad sino un diferenciador competitivo, la industria bancaria y financiera se encuentra en un punto crítico. La adopción de `CRYSTALS-Kyber` representa un movimiento estratégico, alineándose tanto con las necesidades de seguridad actuales como con los giros tecnológicos futuros. Esta última sección describe los incentivos convincentes para integrar `CRYSTALS-Kyber` en la infraestructura criptográfica de los servicios financieros.

- **Adelantarse a las tendencias de ciberseguridad**: el auge de la computación cuántica plantea una amenaza significativa para los algoritmos tradicionales de cifrado, haciéndolos vulnerables al descifrado por los futuros ordenadores cuánticos. Al adoptar `CRYSTALS-Kyber`, las instituciones financieras pueden proteger sus datos sensibles e infraestructuras críticas frente a estas amenazas emergentes.

- **Eficiencia operativa y rentabilidad**: los tamaños de clave compactos y los algoritmos eficientes de `CRYSTALS-Kyber` conducen a ahorros sustanciales de coste. Comparado con los algoritmos tradicionales, `CRYSTALS-Kyber` reduce las necesidades de almacenamiento hasta en un 50 % y el consumo de ancho de banda hasta en un 30 %, generando ahorros significativos para las instituciones financieras con grandes volúmenes de datos.

- **Alineación normativa y gestión de riesgos**: con varios organismos reguladores —entre ellos el NIST y la European Union Agency for Cybersecurity (ENISA)— recomendando activamente la adopción de soluciones criptográficas resistentes a lo cuántico, los adoptantes tempranos de `CRYSTALS-Kyber` estarán bien posicionados para cumplir las futuras exigencias normativas y mitigar los riesgos jurídicos potenciales.

- **Reforzar la confianza del cliente y la reputación institucional**: instituciones financieras de primer nivel como Barclays y Deutsche Bank han adoptado `CRYSTALS-Kyber` para proteger los datos de clientes y asegurar transacciones financieras críticas. Este compromiso con una seguridad avanzada no solo ha protegido a estas instituciones de potenciales ciberataques, sino que también ha reforzado su reputación como guardianes de confianza de la información sensible.

![Divider][01].class=\"m-10 w-100\"

## Conclusión

### Asegurar el futuro financiero con CRYSTALS-Kyber

Ante la evolución de las amenazas de ciberseguridad, la industria bancaria y financiera afronta una elección crítica. Los algoritmos tradicionales de cifrado, antaño considerados seguros, son ahora vulnerables frente a la potencia emergente de la computación cuántica. `CRYSTALS-Kyber` emerge como un faro de seguridad, ofreciendo una solución robusta, eficiente y perdurable para proteger los activos digitales del sector financiero.

Con su combinación única de funcionalidades QR, eficiencia operativa y tamaños de clave más pequeños, `CRYSTALS-Kyber` es un game-changer para la seguridad financiera. Al adoptar `CRYSTALS-Kyber`, las instituciones no solo aseguran sus operaciones actuales sino que también se preparan para un futuro en el que la computación cuántica redefine la ciberseguridad. Este enfoque proactivo demuestra un compromiso con los más altos estándares de seguridad, reforzando la confianza del cliente y la resistencia de la industria frente a las amenazas en evolución.

En un mundo cada vez más interconectado y digital, `CRYSTALS-Kyber` se alza como un testimonio del poder de las soluciones innovadoras y orientadas al futuro. Su adopción por instituciones financieras de primer nivel como Barclays y Deutsche Bank es un fuerte respaldo a sus capacidades y una señal clara a la industria para abrazar esta solución criptográfica resistente a lo cuántico.

![Divider][01].class=\"m-10 w-100\"

En conclusión, espero que esta exploración de `CRYSTALS-Kyber` haya iluminado el profundo impacto de la criptografía resistente a lo cuántico en el sector financiero. Si desea sumergirse más profundamente en esta tecnología revolucionaria o tiene preguntas, le invito a contactarme en [LinkedIn ⧉][02] o a través de la [página de contacto][00].

Gracias de nuevo por su tiempo, espero tener noticias suyas.

[00]: /contact/index.html "Contact"
[01]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[02]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau on LinkedIn"
[03]: /2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html "Protecting Data in the Quantum Age: The Hash Library (HSH)"
[04]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-kyber.svg "CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)"
[05]: https://www.nist.gov/ "The National Institute of Standards and Technology (NIST)"
