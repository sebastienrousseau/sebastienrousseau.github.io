---
title: "Proteger os dados em a era quântica: a biblioteca Hash (HSH)"
subtitle: "Una biblioteca Rust resistente a lo quântico para o hashing e a verificação criptográficos"
description: "HSH se apoya em primitivas criptográficas resistentes a lo quântico para proteger seus dados frente a os avances futuros de a computação quântica."
date: "October 16, 2023"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-7ej8VWfwFsg.webp"
banner_alt: "Ilustración creativa sobre ou tema de a computação quântica"
keywords: "criptografia resistente a lo quântico, biblioteca Hash, HSH, Rust, pós-quântica, PQC, KDF, Argon2i, BScrypt, Scrypt, serviços financeiros, segurança, NIST"
---

![Ilustración creativa sobre ou tema de a computação quântica](https://cloudcdn.pro/stocks/images/galina-nelyubova-7ej8VWfwFsg.webp).class=\"img-fluid clearfix\"

En este artigo examinaré os usos de a criptografia resistente a lo quântico, centrándome específicamente em a biblioteca Rust Hash (HSH) que tenho desenvolvido. Esta biblioteca está totalmente optimizada para as funciones de hashing e verificação criptográficos.

## Perspectiva

### La amenaza emergente de a computação quântica

A medida que o panorama digital evolui, as organizações de serviços financeiros devem adotar novas tecnologias para seguir siendo competitivas. De no hacerlo, corren o riesgo de quedarse atrás, já que a transformação digital afecta a todos os sectores.

La computação quântica anuncia um giro mayor: promete acelerar os avances em sectores diversos, incluídos ou setor bancário e os serviços financeiros. Pero conlleva um riesgo formidable para a segurança digital, devido a seu capacidade para descifrar os códigos mais complejos.

La computação quântica vuelve obsoletas ciertas técnicas de criptografia tradicionais, já que pode resolver problemas matemáticos inaccesibles para os computadores clásicos.

Hoy, Alice e Bob podem comunicarse de forma segura mediante claves criptográficas, impidiendo que Eve decodifique seus mensajes. Pero a segurança absoluta de a distribución e o almacenamiento de claves nunca está totalmente garantizada. Los computadores quânticos suponen, pues, uma amenaza significativa para o criptografia e a segurança digital.

#### Seguros mas vulnerables: navegar por os retos criptográficos em a era quântica

![Diagrama de secuencia][01].class=\"img-fluid clearfix\"

##### Leyenda

* *Alice rumo a Eve — Alice envia um mensaje criptografia*
* *Eve intercepta — Eve intercepta o mensaje de Alice*
* *Eve intenta descifrar — Eve lo intenta mas no alcança descifrar*
* *Eve rumo a Bob — Eve envia um mensaje criptografia a Bob*
* *Bob rumo a Eve — Bob envia uma resposta cifrada a Eve*
* *Eve intercepta — Eve intercepta a resposta de Bob*
* *Eve intenta descifrar — Eve no alcança descifrar de novo*
* *Eve rumo a Alice — Eve envia um mensaje criptografia a Alice*

##### Explicación

###### Criptografia actual

Los algoritmos de criptografia actuales utilizados por Alice e Bob são eficaces para impedir que Eve descifre seus mensajes. Sin embargo, a computação quântica constituye uma amenaza potencial para seu segurança.

###### Riesgo quântico potencial

Los computadores quânticos são muito mais rápidos que os computadores tradicionais para ciertos tipos de cálculo, incluídos os que servem para romper determinados algoritmos de criptografia. Si Eve tuviera acceso a um computador quântico, potencialmente poderia quebrar o criptografia e leer os mensajes de Alice e Bob.

###### Riesgos vinculados a a distribución e o almacenamiento de claves

Aunque Alice e Bob utilicen um criptografia robusto, seus mensajes poderiam verse comprometidos si as claves utilizadas para cifrar e descifrar são comprometidas. Las claves podem serlo de múltiples maneras: robo, pirateo ou ataques de ingeniería social.

###### Necesidad de uma criptografia pós-quântica

La criptografia pós-quântica é um novo campo diseñado para resistir os ataques quânticos. Los algoritmos de criptografia pós-quântico ainda estão em desenvolvimento, mas têm o potencial de proteger os dados frente a os ataques quânticos.

### Introducción a a criptografia resistente a lo quântico

La criptografia resistente a lo quântico, também llamada criptografia pós-quântica (PQC) ou criptografia «quantum-safe», designa a os algoritmos criptográficos considerados seguros frente a os ataques de computadores quânticos.

Las organizações devem tomar as precauciones necessárias para proteger seus dados frente a os peligros de a computação quântica. Implementar criptografia resistente a lo quântico e estrategias de entrelazamiento quântico pode oferecer a as empresas de serviços financeiros uma capa adicional de segurança.

* La **criptografia resistente a lo quântico** é um novo tipo de criptografia capaz de resistir os ataques de computadores quânticos. Sus algoritmos podem acelerar o tratamiento de dados e incrementar a precisión, convirtiéndola em uma opção mais eficiente.

* El **entrelazamiento quântico** permite criar sistemas de [distribución quântica de claves](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) ([QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)), capaces de generar e distribuir claves criptográficas seguras a largas distancias. Los sistemas QKD são inmunes a os ataques de computador quântico, lo que os faz ideales para proteger dados financeiros sensibles.

## Idea

### La biblioteca Hash (HSH): interoperabilidade pionera em criptografia resistente a lo quântico

La biblioteca Hash (HSH) oferece uma solução ligera, eficiente e fácil de usar para proteger os dados com criptografia resistente a lo quântico. Permite a os desenvolvedores utilizar algoritmos resistentes a lo quântico em seus aplicações sem requerer uma comprensión detallada de os algoritmos criptográficos subyacentes.

La biblioteca está construida com o lenguaje Rust, reconocido por seu rapidez e eficiência, idóneamente adaptado a a criptografia e a a confiabilidade a longo prazo.

## Impacto

### Los beneficios de a biblioteca de hash resistente a lo quântico

La [biblioteca Hash (HSH) ⧉][00] aporta uma rica paleta de primitivas criptográficas modernas, levantando uma barrera sólida frente a as complejidades de a era quântica. Su importancia reside em a protección de os dados sensibles em uma época em que a computação quântica supone um riesgo significativo para a segurança digital.

La biblioteca oferece a as organizações e instituições financeiras o nivel mais alto de protección disponible online, com uma selección de algoritmos que incluem Argon2i, BScrypt e Scrypt. Trata-se de funciones de derivación de claves seguras a partir de senha (PBKDF). Las PBKDF servem para convertir senhas em claves criptográficas. Diseñadas para ser lentas e exigentes em memoria, são difíciles de romper por fuerza bruta.

Por outro lado, a biblioteca garantiza no solo resultados seguros e eficientes, mas sim também perfectamente adaptados a as aplicações empresariales, extensibles e fáciles de usar.

## Incentivos

### Navegar por o paisaje de a computação quântica com segurança

* **Garantía de segurança**: utilizar a biblioteca Hash (HSH) da a as organizações a garantía de que seus dados permanecen seguros.

* **Perdurabilidad**: adotar hoje algoritmos resistentes a lo quântico protegerá a as organizações frente a as vulnerabilidades futuras.

* **Eficiencia econômica**: a biblioteca Hash (HSH) é de código aberto e pode utilizarse sem licencia onerosa ni suscripción. Una opção atractiva para as organizações que deseen controlar seus costes a a vez que acceden a uma computação quântica segura.

### Mantener a confiança de os consumidores

* **Proteger os dados de os clientes**: asegurar os dados de os clientes frente a os ataques de computadores quânticos refuerza a confiança em a capacidade de as organizações para proteger a informação.

* **Cumplimiento e adhesión normativa**: aplicar métodos criptográficos avanzados ayuda a respetar leyes e reglamentos estrictos de protección de dados, evitando consecuencias jurídicas e multas.

### HSH: a biblioteca de hash definitiva resistente a lo quântico

* **Alto rendimiento**: aproveitar a [biblioteca Hash (HSH) ⧉][00] basada em Rust aporta segurança, eficiência e rendimiento.
Coherencia multiplataforma: a biblioteca Hash (HSH) protege os dados em todas as plataformas e aplicações.

* **Facilidad de implementación**: a biblioteca Hash (HSH) proporciona a os desenvolvedores uma ferramenta sencilla de integrar, bajando a barrera de adoção de algoritmos resistentes a lo quântico.

## Conclusión

La [biblioteca Hash (HSH) ⧉][00] oferece uma solução ligera, eficiente e fácil de usar para proteger os dados com criptografia resistente a lo quântico. Facilita a actualización de os protocolos criptográficos de os desenvolvedores para hacerlos resistentes a lo quântico sem exigir uma comprensión profunda de os algoritmos.

La criptografia resistente a lo quântico é um campo em rápida evolução, e a biblioteca HSH se compromete a mantenerse a a vanguarda. Se actualiza periódicamente com novos algoritmos e funcionalidades para proteger frente a as amenazas emergentes.

El [National Institute of Standards and Technology (NIST) ⧉][02] define atualmente um conjunto de estándares de algoritmos criptográficos pós-quânticos através de seu [projeto Post-Quantum Cryptography (PQC) ⧉][03].

Proteger seus dados frente a os ataques de a computação quântica é esencial para toda organização que maneje dados sensibles. La [biblioteca Hash (HSH) ⧉][00] é uma ferramenta potente que pode ayudarle a proteger seus dados frente a esta amenaza emergente.

[00]: https://crates.io/crates/hsh "The Hash Library (HSH) - Quantum-Resistant Cryptographic Hash Library for Password Hashing and Verification"
[01]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-encryption.svg "Seguros mas vulnerables: navegar por os retos criptográficos em a era quântica"
[02]: https://www.nist.gov/ "National Institute of Standards and Technology"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography "Post-Quantum Cryptography PQC"
