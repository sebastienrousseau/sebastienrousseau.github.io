---
title: "CRYSTALS-Kyber: o algoritmo de protección em a era quântica"
subtitle: "CRYSTALS-Kyber, o estándar NIST FIPS 203 para a encapsulación de claves pós-quântica"
description: "Cómo CRYSTALS-Kyber, algoritmo de criptografia resistente a lo quântico, revoluciona o mundo de a criptografia e nos prepara para a era quântica."
date: "November 19, 2023"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp"
banner_alt: "Um computador quântico moderno e depurado"
keywords: "computação quântica, criptografia resistente a lo quântico, CRYSTALS-Kyber, criptografia, segurança, banca, finanzas, criptografia, protección de dados, perdurabilidad"
---

![AI, Artificial Intelligence concept,3d rendering,conceptual image](https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp).class=\"img-fluid clearfix\"

## Perspectiva

### Navegar por a ameaça quântica: a génesis de CRYSTALS-Kyber

En meu artigo anterior, [Proteger os dados em a era quântica ⧉][03], me sumergí em a amenaza inminente de a computação quântica para a segurança digital e examiné cómo a criptografia resistente a lo quântico (QRC) pode responder a ela. Ahora voy a explorar `CRYSTALS-Kyber`, um algoritmo QRC revolucionário que transforma o panorama de a segurança.

Los computadores quânticos, com seu capacidade para realizar ciertos cálculos muito mais rápido que os computadores clásicos, plantean um riesgo significativo para os algoritmos de criptografia actuales. Esto suscita inquietudes sobre a segurança de a informação sensible: transações financeiras, historiales médicos e comunicações personales.

Para mitigar esta amenaza, os criptógrafos desenvolveram algoritmos QRC como `CRYSTALS-Kyber`. Este algoritmo é um mecanismo de encapsulación de claves (KEM) diseñado para intercambiar de forma segura claves secretas entre partes.

Hoy, `CRYSTALS-Kyber` é um líder do proceso de padronização pós-quântica do [National Institute of Standards and Technology (NIST) ⧉][05], demostrando seu potencial como solução de segurança robusta em a era digital.

### CRYSTALS-Kyber: segurança inquebrantable frente a a computação quântica

La segurança de `CRYSTALS-Kyber` reposa em a dificuldade inherente a resolver o problema `Learning With Errors (LWE)` sobre retículos de módulos. Este desafío matemático complejo, considerado computacionalmente intratable incluso para os computadores quânticos, serve de zócalo a a resistencia de `CRYSTALS-Kyber` frente a os ataques quânticos.

### CRYSTALS-Kyber: um cambio de paradigma em segurança digital

`CRYSTALS-Kyber` pertenece a a suite de algoritmos CRYSTALS (Cryptographic Suite for Algebraic Lattices) e porta com orgullo a distinción de algoritmo quântico-seguro (QSA).

Si bien o concepto de utilizar problemas sobre retículos com fines criptográficos no é enteramente novo, `CRYSTALS-Kyber` eleva esse concepto a niveles de eficiência sem parangón. Su capacidade para generar claves criptográficas com tamaños mais pequeños e velocidades de criptografia/decifragem mais rápidas lo convierten em uma elección ideal para as aplicações reales, em particular em o exigente mundo de as finanzas.

![Divider][01].class=\"m-10 w-100\"

## Idea

### Comprender a mecánica de CRYSTALS-Kyber: a encapsulación de claves em o núcleo

En o núcleo do diseño revolucionário de `CRYSTALS-Kyber` se encontra seu enfoque innovador de a encapsulación de claves, componente crítico de a comunicação segura. Aprovecha a potencia de a criptografia sobre retículos, método reconocido por seu resistencia frente a os ataques quânticos. Esta técnica sofisticada saca partido de estructuras geométricas em um espacio multidimensional para establecer claves criptográficas.

`CRYSTALS-Kyber` emplea um tipo específico de problema sobre retículos, conhecido por seus propriedades de eficiência e segurança, para generar as claves criptográficas. Esto garantiza a protección de os dados sensibles incluso frente a os avances de a computação quântica.

#### Encapsulación de claves segura: a esencia de CRYSTALS-Kyber

La encapsulación de claves é semejante a guardar um mensaje em uma caja de maneira segura, onde solo o destinatario previsto posee a llave para abrirla. En criptografia, este proceso implica criar um par de claves: uma clave pública, que pode compartirse abiertamente, e uma clave privada, que deve mantenerse secreta. El brillo de `CRYSTALS-Kyber` reside em seu capacidade para generar e utilizar estas claves de uma maneira que garantiza uma segurança sem parangón.

Veamos cómo `CRYSTALS-Kyber` utiliza a encapsulación de claves para establecer uma comunicação segura entre dois partes, Alice e Bob. El diagrama de secuencia seguinte ilustra os pasos involucrados, utilizando `CRYSTALS-Kyber`, um KEM diseñado para proporcionar um intercambio de claves seguro para os protocolos criptográficos. El KyberServer desempeña aqui um papel pivote em este proceso, generando e distribuyendo as claves criptográficas requeridas.

![CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)][04].class=\"img-fluid clearfix\"

##### Leyenda

- Alice: emisor do mensaje.
- Bob: receptor do mensaje.
- KyberServer: servidor que genera e distribuye as claves criptográficas.

##### Explicación

###### Intercambio de clave pública

- Alice inicia o proceso solicitando seu clave pública ao KyberServer.
- El KyberServer responde enviando a clave pública de Alice, um valor matemático que pode compartirse públicamente sem comprometer a segurança de a clave privada de Alice.
- Alice comparte depois seu clave pública com Bob, permitiéndole cifrar mensajes que solo Alice pode descifrar.

###### Encapsulación e desencapsulación

- Bob solicita uma clave de encapsulación ao KyberServer. Esta clave temporal servirá para cifrar a clave secreta compartida antes de enviarla a Alice.
- El KyberServer envia a clave de encapsulación a Bob.
- Bob utiliza a clave pública de Alice e a clave de encapsulación para cifrar a clave secreta compartida, criando uma cápsula cifrada.
- Bob envia a cápsula cifrada a Alice.
- Alice solicita uma clave de decifragem ao KyberServer. Esta clave temporal servirá para descifrar a cápsula e revelar a clave secreta compartida.
- El KyberServer envia a clave de decifragem a Alice.

###### Intercambio de clave secreta compartida

- Alice utiliza seu clave privada e a clave de decifragem para descifrar a cápsula, revelando a clave secreta compartida.
- Alice comparte a clave secreta compartida com Bob, permitiéndole descifrar os mensajes cifrados com esta clave.

###### Comunicación segura

El diagrama ilustra eficazmente as etapas complejas de establecimiento de um canal de comunicação seguro, subrayando o papel crucial do KyberServer em a geração e distribución de as claves criptográficas. Al emplear o KEM `CRYSTALS-Kyber`, Alice e Bob podem proteger seu informação sensible e manter uma comunicação segura incluso frente a adversarios potenciales.

### Criptografia sobre retículos: um fundamento robusto para a resistencia quântica

`CRYSTALS-Kyber` emplea um enfoque basado em retículos, método reconocido por seu potencial de resistencia a os ataques quânticos. El principio subyacente de a criptografia sobre retículos implica estructuras geométricas em um espacio multidimensional. Si bien navegar por estas estructuras complejas pode parecer intimidante, `CRYSTALS-Kyber` lo simplifica. Utiliza um tipo específico de problema sobre retículos, conhecido por seus propriedades de eficiência e segurança, para criar claves criptográficas.

#### Tamaños de clave eficientes: equilibrio entre segurança e rendimiento

Una de as características destacadas de `CRYSTALS-Kyber` é o tamaño de seus claves. Comparado com otros algoritmos pós-quânticos, `CRYSTALS-Kyber` oferece tamaños de clave significativamente mais pequeños, haciéndolo mais prático para as aplicações reales. `CRYSTALS-Kyber` propone três niveles de segurança, cada uno com seu próprio tamaño de clave:

- **Kyber512**: nivel de segurança de 128 bits, com tamaños de clave de 1.632 bytes para as claves secretas, 800 bytes para as claves públicas e 768 bytes para os criptogramas.
- **Kyber768**: nivel de segurança de 192 bits, com tamaños de clave de 2.400 bytes para as claves secretas, 1.184 bytes para as claves públicas e 1.088 bytes para os criptogramas.
- **Kyber1024**: nivel de segurança de 256 bits, com tamaños de clave de 3.168 bytes para as claves secretas, 1.568 bytes para as claves públicas e 1.568 bytes para os criptogramas.

Estos tamaños relativamente pequeños fazem que `CRYSTALS-Kyber` sea atractivo para os dispositivos com recursos limitados: smartphones e dispositivos IoT. Reducen também o ancho de banda requerido para transmitir as claves, lo que pode ser beneficioso para as aplicações com conectividad de red limitada.

#### Velocidad inquebrantable: um faro em o panorama financeiro veloz

Otro aspecto do atractivo de `CRYSTALS-Kyber` é seu velocidade. En o setor bancário e financeiro veloz, a velocidade cuenta tanto como a segurança. El diseño do algoritmo garantiza que opere rapidamente, facilitando procesos de criptografia e decifragem veloces. Esta eficiência no tem-sece a costa de a segurança; mais bien é um resultado directo de os fundamentos matemáticos sofisticados do algoritmo.

### CRYSTALS-Kyber: uma simbiosis de segurança, eficiência e velocidade

`CRYSTALS-Kyber` tem emergido como um líder em a pesquisa de criptografia resistente a lo quântico, ofreciendo uma combinación única de segurança, eficiência e velocidade. Su enfoque innovador basado em retículos, seus tamaños de clave mais pequeños e seu diseño optimizado lo convierten em uma elección ideal para proteger a informação sensible em ou setor bancário e os serviços financeiros. Mientras o mundo continúa abrazando as tecnologias digitais, `CRYSTALS-Kyber` se posiciona para desempenhar um papel pivote em a protección de nossos dados em os próximos anos.

![Divider][01].class=\"m-10 w-100\"

## Impacto

### CRYSTALS-Kyber: ventajas para ou setor bancário e os serviços financeiros

La industria bancária e financeira está em uma carrera constante por adelantarse a ciberamenazas cada vez mais sofisticadas. En este contexto, `CRYSTALS-Kyber` se distingue no solo por seus propriedades resistentes a lo quântico (QR) mas sim também por os beneficios tangibles que oferece a esta industria. Esta sección detalla as ventajas práticas de `CRYSTALS-Kyber`, subrayando por que é particularmente adecuado para as necessidades únicas de as instituições financeiras.

- **Seguridad reforzada com claves mais pequeñas**: uma de as ventajas mais significativas de `CRYSTALS-Kyber` é seu capacidade para criar claves de criptografia mais pequeñas sem sacrificar a segurança. En um sector onde as brechas de dados podem tener consecuencias catastróficas, uma segurança robusta no é negociable. Los tamaños de clave mais pequeños de `CRYSTALS-Kyber` simplifican os procesos de gestión de claves, factor crítico em os grandes sistemas bancários onde miles de claves estão em juego. Esto no solo refuerza a segurança, mas sim que também optimiza a eficiência de almacenamiento e transmissão, factor crucial em uma época em que a velocidade e o espacio são valiosos.

- **Velocidad e eficiência**: em os serviços financeiros, onde as transações se producen em milisegundos, a velocidade de as operações criptográficas é crucial. `CRYSTALS-Kyber` sobresale em este aspecto, ofreciendo procesos rápidos de geração de claves, encapsulación e desencapsulación. Esta velocidade garantiza que as medidas de segurança no se conviertan em um cuello de botella em os entornos de trading de alta frecuencia ou durante transações a gran escala. Além disso, a eficiência de `CRYSTALS-Kyber` se traduce em uma reducción de os recursos de cálculo, conduciendo a ahorros de coste e a operações mais respetuosas com o meio ambiente.

- **Perdurabilidad frente a as ameaças quânticas**: com o advenimiento de a computação quântica, a industria afronta um futuro em o que os métodos criptográficos tradicionais poderiam quedar obsoletos. Al adotar `CRYSTALS-Kyber`, as instituições financeiras no solo aseguran seu presente mas sim que também se preparan para um mundo pós-quântico. Este enfoque proactivo de a ciberseguridad demuestra um compromiso com a protección a longo prazo de os dados, consideración esencial para as partes interesadas e os clientes que priorizan a segurança.

- **Cumplimiento normativo e ventaja competitiva**: à medida que os reguladores mundiales empiezan a reconocer a ameaça quântica, é probable que impongan a adoção de algoritmos resistentes a lo quântico. La adoção temprana de `CRYSTALS-Kyber` posiciona a as instituições financeiras como líderes em cumplimiento e segurança. Além disso, oferece uma ventaja competitiva, tranquilizando a clientes e socios sobre ou compromiso de a institución com práticas de segurança punteras.

![Divider][01].class=\"m-10 w-100\"

## Incentivos

### El caso para a adoção de CRYSTALS-Kyber

En um panorama onde a ciberseguridad no é solo uma necessidade mas sim um diferenciador competitivo, a industria bancária e financeira se encontra em um ponto crítico. La adoção de `CRYSTALS-Kyber` representa um movimiento estratégico, alineándose tanto com as necessidades de segurança actuales como com os giros tecnológicos futuros. Esta última sección describe os incentivos convincentes para integrar `CRYSTALS-Kyber` em a infraestrutura criptográfica de os serviços financeiros.

- **Adelantarse a as tendencias de ciberseguridad**: o auge de a computação quântica plantea uma amenaza significativa para os algoritmos tradicionais de criptografia, haciéndolos vulnerables ao decifragem por os futuros computadores quânticos. Al adotar `CRYSTALS-Kyber`, as instituições financeiras podem proteger seus dados sensibles e infraestruturas críticas frente a estas amenazas emergentes.

- **Eficiencia operativa e rentabilidade**: os tamaños de clave compactos e os algoritmos eficientes de `CRYSTALS-Kyber` conducen a ahorros sustanciales de coste. Comparado com os algoritmos tradicionais, `CRYSTALS-Kyber` reduce as necessidades de almacenamiento hasta em um 50 % e o consumo de ancho de banda hasta em um 30 %, generando ahorros significativos para as instituições financeiras com grandes volúmenes de dados.

- **Alineación normativa e gestión de riesgos**: com vários organismos reguladores —entre olos o NIST e a European Union Agency for Cybersecurity (ENISA)— recomendando activamente a adoção de soluções criptográficas resistentes a lo quântico, os adoptantes tempranos de `CRYSTALS-Kyber` estarán bien posicionados para cumplir as futuras exigencias normativas e mitigar os riesgos jurídicos potenciales.

- **Reforzar a confiança do cliente e a reputación institucional**: instituições financeiras de primer nivel como Barclays e Deutsche Bank têm adotado `CRYSTALS-Kyber` para proteger os dados de clientes e asegurar transações financeiras críticas. Este compromiso com uma segurança avanzada no solo tem protegido a estas instituciones de potenciales ciberataques, mas sim que também tem reforzado seu reputación como guardianes de confiança de a informação sensible.

![Divider][01].class=\"m-10 w-100\"

## Conclusión

### Asegurar o futuro financeiro com CRYSTALS-Kyber

Ante a evolução de as amenazas de ciberseguridad, a industria bancária e financeira afronta uma elección crítica. Los algoritmos tradicionais de criptografia, antaño considerados seguros, são agora vulnerables frente a a potencia emergente de a computação quântica. `CRYSTALS-Kyber` emerge como um faro de segurança, ofreciendo uma solução robusta, eficiente e perdurable para proteger os activos digitais do sector financeiro.

Con seu combinación única de funcionalidades QR, eficiência operativa e tamaños de clave mais pequeños, `CRYSTALS-Kyber` é um game-changer para a segurança financeira. Al adotar `CRYSTALS-Kyber`, as instituciones no solo aseguran seus operações actuales mas sim que também se preparan para um futuro em o que a computação quântica redefine a ciberseguridad. Este enfoque proactivo demuestra um compromiso com os mais altos estándares de segurança, reforzando a confiança do cliente e a resistencia de a industria frente a as amenazas em evolução.

En um mundo cada vez mais interconectado e digital, `CRYSTALS-Kyber` se alza como um testimonio do poder de as soluções innovadoras e orientadas ao futuro. Su adoção por instituições financeiras de primer nivel como Barclays e Deutsche Bank é um fuerte respaldo a seus capacidades e uma señal clara a a industria para abrazar esta solução criptográfica resistente a lo quântico.

![Divider][01].class=\"m-10 w-100\"

En conclusão, espero que esta exploração de `CRYSTALS-Kyber` haya iluminado o profundo impacto de a criptografia resistente a lo quântico em o sector financeiro. Si desea sumergirse mais profundamente em esta tecnologia revolucionária ou tem perguntas, le invito a contactarme em [LinkedIn ⧉][02] ou através de a [página de contacto][00].

Gracias de novo por seu tempo, espero tener noticias suyas.

[00]: /contact/index.html "Contact"
[01]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[02]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau on LinkedIn"
[03]: /2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html "Protecting Data in the Quantum Age: The Hash Library (HSH)"
[04]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-kyber.svg "CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)"
[05]: https://www.nist.gov/ "The National Institute of Standards and Technology (NIST)"
