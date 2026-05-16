---
title: "Proteger los datos en la era cuántica: la biblioteca Hash (HSH)"
subtitle: "Una biblioteca Rust resistente a lo cuántico para el hashing y la verificación criptográficos"
description: "HSH se apoya en primitivas criptográficas resistentes a lo cuántico para proteger sus datos frente a los avances futuros de la computación cuántica."
date: "October 16, 2023"
language: "th-TH"
locale: "th_TH"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-7ej8VWfwFsg.webp"
banner_alt: "Ilustración creativa sobre el tema de la computación cuántica"
keywords: "criptografía resistente a lo cuántico, biblioteca Hash, HSH, Rust, postcuántica, PQC, KDF, Argon2i, BScrypt, Scrypt, servicios financieros, seguridad, NIST"
---


> **TL;DR.** บทความนี้เป็น DRAFT แปลจากต้นฉบับภาษาสเปน รอการตรวจสอบโดยเจ้าของภาษา เนื้อหาหลัก ตัวอย่าง และการอ้างอิงยังคงเป็นภาษาสเปน เฉพาะ frontmatter เท่านั้นที่ถูกเปลี่ยนเป็นภาษาไทย

**ประเด็นสำคัญ**

![Ilustración creativa sobre el tema de la computación cuántica](https://cloudcdn.pro/stocks/images/galina-nelyubova-7ej8VWfwFsg.webp).class=\"img-fluid clearfix\"

En este artículo examinaré los usos de la criptografía resistente a lo cuántico, centrándome específicamente en la biblioteca Rust Hash (HSH) que he desarrollado. Esta biblioteca está totalmente optimizada para las funciones de hashing y verificación criptográficos.

## Perspectiva

### La amenaza emergente de la computación cuántica

A medida que el panorama digital evoluciona, las organizaciones de servicios financieros deben adoptar nuevas tecnologías para seguir siendo competitivas. De no hacerlo, corren el riesgo de quedarse atrás, ya que la transformación digital afecta a todos los sectores.

La computación cuántica anuncia un giro mayor: promete acelerar los avances en sectores diversos, incluidos la banca y los servicios financieros. Pero conlleva un riesgo formidable para la seguridad digital, debido a su capacidad para descifrar los códigos más complejos.

La computación cuántica vuelve obsoletas ciertas técnicas de cifrado tradicionales, ya que puede resolver problemas matemáticos inaccesibles para los ordenadores clásicos.

Hoy, Alice y Bob pueden comunicarse de forma segura mediante claves criptográficas, impidiendo que Eve decodifique sus mensajes. Pero la seguridad absoluta de la distribución y el almacenamiento de claves nunca está totalmente garantizada. Los ordenadores cuánticos suponen, pues, una amenaza significativa para el cifrado y la seguridad digital.

#### Seguros pero vulnerables: navegar por los retos criptográficos en la era cuántica

![Diagrama de secuencia][01].class=\"img-fluid clearfix\"

##### Leyenda

* *Alice hacia Eve — Alice envía un mensaje cifrado*
* *Eve intercepta — Eve intercepta el mensaje de Alice*
* *Eve intenta descifrar — Eve lo intenta pero no logra descifrar*
* *Eve hacia Bob — Eve envía un mensaje cifrado a Bob*
* *Bob hacia Eve — Bob envía una respuesta cifrada a Eve*
* *Eve intercepta — Eve intercepta la respuesta de Bob*
* *Eve intenta descifrar — Eve no logra descifrar de nuevo*
* *Eve hacia Alice — Eve envía un mensaje cifrado a Alice*

##### Explicación

###### Cifrado actual

Los algoritmos de cifrado actuales utilizados por Alice y Bob son eficaces para impedir que Eve descifre sus mensajes. Sin embargo, la computación cuántica constituye una amenaza potencial para su seguridad.

###### Riesgo cuántico potencial

Los ordenadores cuánticos son mucho más rápidos que los ordenadores tradicionales para ciertos tipos de cálculo, incluidos los que sirven para romper determinados algoritmos de cifrado. Si Eve tuviera acceso a un ordenador cuántico, potencialmente podría quebrar el cifrado y leer los mensajes de Alice y Bob.

###### Riesgos vinculados a la distribución y el almacenamiento de claves

Aunque Alice y Bob utilicen un cifrado robusto, sus mensajes podrían verse comprometidos si las claves utilizadas para cifrar y descifrar son comprometidas. Las claves pueden serlo de múltiples maneras: robo, pirateo o ataques de ingeniería social.

###### Necesidad de una criptografía postcuántica

La criptografía postcuántica es un nuevo campo diseñado para resistir los ataques cuánticos. Los algoritmos de cifrado postcuántico aún están en desarrollo, pero tienen el potencial de proteger los datos frente a los ataques cuánticos.

### Introducción a la criptografía resistente a lo cuántico

La criptografía resistente a lo cuántico, también llamada criptografía postcuántica (PQC) o criptografía «quantum-safe», designa a los algoritmos criptográficos considerados seguros frente a los ataques de ordenadores cuánticos.

Las organizaciones deben tomar las precauciones necesarias para proteger sus datos frente a los peligros de la computación cuántica. Implementar cifrado resistente a lo cuántico y estrategias de entrelazamiento cuántico puede ofrecer a las empresas de servicios financieros una capa adicional de seguridad.

* La **criptografía resistente a lo cuántico** es un nuevo tipo de cifrado capaz de resistir los ataques de ordenadores cuánticos. Sus algoritmos pueden acelerar el tratamiento de datos e incrementar la precisión, convirtiéndola en una opción más eficiente.

* El **entrelazamiento cuántico** permite crear sistemas de [distribución cuántica de claves](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html) ([QKD](/2023-12-11-quantum-key-distribution-revolutionising-security-in-banking/index.html)), capaces de generar y distribuir claves criptográficas seguras a largas distancias. Los sistemas QKD son inmunes a los ataques de ordenador cuántico, lo que los hace ideales para proteger datos financieros sensibles.

## Idea

### La biblioteca Hash (HSH): interoperabilidad pionera en criptografía resistente a lo cuántico

La biblioteca Hash (HSH) ofrece una solución ligera, eficiente y fácil de usar para proteger los datos con criptografía resistente a lo cuántico. Permite a los desarrolladores utilizar algoritmos resistentes a lo cuántico en sus aplicaciones sin requerir una comprensión detallada de los algoritmos criptográficos subyacentes.

La biblioteca está construida con el lenguaje Rust, reconocido por su rapidez y eficiencia, idóneamente adaptado a la criptografía y a la fiabilidad a largo plazo.

## Impacto

### Los beneficios de la biblioteca de hash resistente a lo cuántico

La [biblioteca Hash (HSH) ⧉][00] aporta una rica paleta de primitivas criptográficas modernas, levantando una barrera sólida frente a las complejidades de la era cuántica. Su importancia reside en la protección de los datos sensibles en una época en que la computación cuántica supone un riesgo significativo para la seguridad digital.

La biblioteca ofrece a las organizaciones e instituciones financieras el nivel más alto de protección disponible en línea, con una selección de algoritmos que incluyen Argon2i, BScrypt y Scrypt. Se trata de funciones de derivación de claves seguras a partir de contraseña (PBKDF). Las PBKDF sirven para convertir contraseñas en claves criptográficas. Diseñadas para ser lentas y exigentes en memoria, son difíciles de romper por fuerza bruta.

Por otra parte, la biblioteca garantiza no solo resultados seguros y eficientes, sino también perfectamente adaptados a las aplicaciones empresariales, extensibles y fáciles de usar.

## Incentivos

### Navegar por el paisaje de la computación cuántica con seguridad

* **Garantía de seguridad**: utilizar la biblioteca Hash (HSH) da a las organizaciones la garantía de que sus datos permanecen seguros.

* **Perdurabilidad**: adoptar hoy algoritmos resistentes a lo cuántico protegerá a las organizaciones frente a las vulnerabilidades futuras.

* **Eficiencia económica**: la biblioteca Hash (HSH) es de código abierto y puede utilizarse sin licencia onerosa ni suscripción. Una opción atractiva para las organizaciones que deseen controlar sus costes a la vez que acceden a una computación cuántica segura.

### Mantener la confianza de los consumidores

* **Proteger los datos de los clientes**: asegurar los datos de los clientes frente a los ataques de ordenadores cuánticos refuerza la confianza en la capacidad de las organizaciones para proteger la información.

* **Cumplimiento y adhesión normativa**: aplicar métodos criptográficos avanzados ayuda a respetar leyes y reglamentos estrictos de protección de datos, evitando consecuencias jurídicas y multas.

### HSH: la biblioteca de hash definitiva resistente a lo cuántico

* **Alto rendimiento**: aprovechar la [biblioteca Hash (HSH) ⧉][00] basada en Rust aporta seguridad, eficiencia y rendimiento.
Coherencia multiplataforma: la biblioteca Hash (HSH) protege los datos en todas las plataformas y aplicaciones.

* **Facilidad de implementación**: la biblioteca Hash (HSH) proporciona a los desarrolladores una herramienta sencilla de integrar, bajando la barrera de adopción de algoritmos resistentes a lo cuántico.

## Conclusión

La [biblioteca Hash (HSH) ⧉][00] ofrece una solución ligera, eficiente y fácil de usar para proteger los datos con criptografía resistente a lo cuántico. Facilita la actualización de los protocolos criptográficos de los desarrolladores para hacerlos resistentes a lo cuántico sin exigir una comprensión profunda de los algoritmos.

La criptografía resistente a lo cuántico es un campo en rápida evolución, y la biblioteca HSH se compromete a mantenerse a la vanguardia. Se actualiza periódicamente con nuevos algoritmos y funcionalidades para proteger frente a las amenazas emergentes.

El [National Institute of Standards and Technology (NIST) ⧉][02] define actualmente un conjunto de estándares de algoritmos criptográficos postcuánticos a través de su [proyecto Post-Quantum Cryptography (PQC) ⧉][03].

Proteger sus datos frente a los ataques de la computación cuántica es esencial para toda organización que maneje datos sensibles. La [biblioteca Hash (HSH) ⧉][00] es una herramienta potente que puede ayudarle a proteger sus datos frente a esta amenaza emergente.

[00]: https://crates.io/crates/hsh "The Hash Library (HSH) - Quantum-Resistant Cryptographic Hash Library for Password Hashing and Verification"
[01]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-encryption.svg "Seguros pero vulnerables: navegar por los retos criptográficos en la era cuántica"
[02]: https://www.nist.gov/ "National Institute of Standards and Technology"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography "Post-Quantum Cryptography PQC"
