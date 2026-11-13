---
title: "CRYSTALS-Kyber: l'algoritmo di protezione nell'era quantistica"
subtitle: "Il meccanismo di incapsulamento delle chiavi resistente al quantum selezionato dal NIST"
description: "Come CRYSTALS-Kyber, il meccanismo di incapsulamento delle chiavi resistente al quantum selezionato dal NIST, sta ridisegnando la crittografia per l'era quantistica."
date: "November 19, 2023"
language: "it-IT"
locale: "it_IT"
banner: "https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp"
banner_alt: "Un computer quantistico moderno ed elegante"
keywords: "CRYSTALS-Kyber, NIST, PQC, post-quantistica, KEM, incapsulamento chiavi, crittografia, FIPS 203"
---

![Un computer quantistico moderno ed elegante](https://cloudcdn.pro/stocks/images/galina-nelyubova-V70-ng4FuiA.webp).class=\"img-fluid clearfix\"

---

> **TL;DR.** CRYSTALS-Kyber è il KEM (Key Encapsulation Mechanism) post-quantistico standardizzato dal NIST (FIPS 203). Ridisegna la crittografia a chiave pubblica per resistere agli attacchi di Shor su computer quantistici scalati.
>
> **Punti chiave**
>
> - **Standard NIST FIPS 203** — selezionato dopo anni di competizione pubblica come KEM post-quantistico per uso generale.
> - **Basato su reticoli** — sicurezza dimostrabile su problemi reticolari (Module-LWE) ritenuti difficili anche per i computer quantistici.
> - **Prestazioni pragmatiche** — chiavi e ciphertext di dimensioni accettabili per integrazione in TLS, SSH e protocolli di pagamento.
> - **Roadmap di adozione** — già in deployment in TLS sperimentale, presto obbligatorio per il governo USA e i servizi finanziari.

---

## Prospettiva

### Navegar per la minaccia quantistica: la génesis di CRYSTALS-Kyber

In il mio artículo anterior, [Proteger i dati in la era quantistica ⧉][03], me sumergí in la amenaza inminente della calcolo quantistico per la sicurezza digitale e examiné come la criptografía resistente a lo quantistico (QRC) può responder a ella. Ahora voy a explorar `CRYSTALS-Kyber`, un algoritmo QRC revolucionario che transforma il panorama della sicurezza.

I computer quantistici, con il suo capacità per realizar ciertos cálculos molto più rápido che i ordenadores clásicos, plantean un rischio significativo per i algoritmos di cifrado actuales. Esto suscita inquietudes su la sicurezza della informazione sensible: transazioni finanziarie, historiales médicos e comunicaciones personales.

Per mitigar questa amenaza, i criptógrafos hanno sviluppato algoritmos QRC come `CRYSTALS-Kyber`. Questo algoritmo è un mecanismo di encapsulación di chiavi (KEM) progettato per intercambiar in modo segura chiavi secretas tra partes.

Hoy, `CRYSTALS-Kyber` è un líder del processo di estandarización post-quantistica del [National Institute of Standards and Technology (NIST) ⧉][05], demostrando il suo potencial come soluzione di sicurezza robusta in la era digitale.

### CRYSTALS-Kyber: sicurezza inquebrantable rispetto alla calcolo quantistico

La sicurezza di `CRYSTALS-Kyber` reposa in la dificultad inherente a resolver il problema `Learning With Errors (LWE)` su retículos di módulos. Questo sfida matemático complejo, considerado computacionalmente intratable incluso per i computer quantistici, sirve di zócalo alla resistencia di `CRYSTALS-Kyber` rispetto ai ataques quantistici.

### CRYSTALS-Kyber: un cambiamento di paradigma in sicurezza digitale

`CRYSTALS-Kyber` pertenece alla suite di algoritmos CRYSTALS (Cryptographic Suite for Algebraic Lattices) e porta con orgullo la distinción di algoritmo quantistico-seguro (QSA).

Se bene il concepto di utilizzare problemas su retículos con fines crittografici non è enteramente nuovo, `CRYSTALS-Kyber` eleva quello concepto a livelli di eficiencia senza parangón. Il suo capacità per generare chiavi crittografiche con tamaños più pequeños e velocidades di cifrado/descifrado più rápidas lo convertono in una elección ideal per le applicazioni reales, in particolare in il exigente mondo delle finanzas.

![Divider][01].class=\"m-10 w-100\"

## Idea

### Comprender la mecánica di CRYSTALS-Kyber: la encapsulación di chiavi in il núcleo

In il núcleo del diseño revolucionario di `CRYSTALS-Kyber` se encuentra il suo approccio innovador della encapsulación di chiavi, componente crítico della comunicación segura. Aprovecha la potencia della criptografía su retículos, método reconocido per il suo resistencia rispetto ai ataques quantistici. Questa tecnica sofisticada saca partido di estructuras geométricas in un espacio multidimensional per establecer chiavi crittografiche.

`CRYSTALS-Kyber` emplea un tipo específico di problema su retículos, conocido per i suoi propiedades di eficiencia e sicurezza, per generare le chiavi crittografiche. Esto garantisce la protección dei dati sensibles incluso rispetto ai progressi della calcolo quantistico.

#### Encapsulación di chiavi segura: la esencia di CRYSTALS-Kyber

La encapsulación di chiavi è semejante a guardar un messaggio in una caja in modo segura, dove solo il destinatario previsto posee la llave per abrirla. In criptografía, questo processo implica creare un par di chiavi: una chiave pública, che può compartirse abiertamente, e una chiave privada, che deve mantenerse secreta. Il brillo di `CRYSTALS-Kyber` reside in il suo capacità per generare e utilizzare queste chiavi di una manera che garantisce una sicurezza senza parangón.

Veamos come `CRYSTALS-Kyber` utilizza la encapsulación di chiavi per establecer una comunicación segura tra dos partes, Alice e Bob. Il diagrama di secuencia seguente ilustra i passi involucrados, utilizando `CRYSTALS-Kyber`, un KEM progettato per fornire un intercambio di chiavi seguro per i protocolos crittografici. Il KyberServer desempeña aquí un papel pivote in questo processo, generando e distribuyendo le chiavi crittografiche requeridas.

![CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)][04].class=\"img-fluid clearfix\"

##### Leyenda

- Alice: emisor del messaggio.
- Bob: receptor del messaggio.
- KyberServer: servidor che genera e distribuye le chiavi crittografiche.

##### Explicación

###### Intercambio di chiave pública

- Alice avvia il processo solicitando il suo chiave pública al KyberServer.
- Il KyberServer responde enviando la chiave pública di Alice, un valore matemático che può compartirse públicamente senza comprometer la sicurezza della chiave privada di Alice.
- Alice comparte dopo il suo chiave pública con Bob, permitiéndole cifrar messaggi che solo Alice può descifrar.

###### Encapsulación e desencapsulación

- Bob solicita una chiave di encapsulación al KyberServer. Questa chiave temporal servirá per cifrar la chiave secreta compartida prima di enviarla a Alice.
- Il KyberServer envía la chiave di encapsulación a Bob.
- Bob utilizza la chiave pública di Alice e la chiave di encapsulación per cifrar la chiave secreta compartida, creando una cápsula cifrada.
- Bob envía la cápsula cifrada a Alice.
- Alice solicita una chiave di descifrado al KyberServer. Questa chiave temporal servirá per descifrar la cápsula e revelar la chiave secreta compartida.
- Il KyberServer envía la chiave di descifrado a Alice.

###### Intercambio di chiave secreta compartida

- Alice utilizza il suo chiave privada e la chiave di descifrado per descifrar la cápsula, revelando la chiave secreta compartida.
- Alice comparte la chiave secreta compartida con Bob, permitiéndole descifrar i messaggi cifrados con questa chiave.

###### Comunicación segura

Il diagrama ilustra eficazmente le etapas complejas di establecimiento di un canal di comunicación seguro, subrayando il papel crucial del KyberServer in la generación e distribución delle chiavi crittografiche. Al impiegare il KEM `CRYSTALS-Kyber`, Alice e Bob possono proteger il suo informazione sensible e mantener una comunicación segura incluso rispetto a adversarios potenciales.

### Criptografía su retículos: un fundamento robusto per la resistencia quantistica

`CRYSTALS-Kyber` emplea un approccio basato in retículos, método reconocido per il suo potencial di resistencia ai ataques quantistici. Il principio subyacente della criptografía su retículos implica estructuras geométricas in un espacio multidimensional. Se bene navegar per queste estructuras complejas può parecer intimidante, `CRYSTALS-Kyber` lo simplifica. Utiliza un tipo específico di problema su retículos, conocido per i suoi propiedades di eficiencia e sicurezza, per creare chiavi crittografiche.

#### Tamaños di chiave eficientes: equilibrio tra sicurezza e prestazioni

Una delle caratteristiche destacadas di `CRYSTALS-Kyber` è il tamaño di i suoi chiavi. Comparado con altri algoritmos post-quantisticos, `CRYSTALS-Kyber` offre tamaños di chiave significativamente più pequeños, haciéndolo più pratico per le applicazioni reales. `CRYSTALS-Kyber` propone tres livelli di sicurezza, ognuno con il suo propio tamaño di chiave:

- **Kyber512**: livello di sicurezza di 128 bits, con tamaños di chiave di 1.632 bytes per le chiavi secretas, 800 bytes per le chiavi públicas e 768 bytes per i criptogramas.
- **Kyber768**: livello di sicurezza di 192 bits, con tamaños di chiave di 2.400 bytes per le chiavi secretas, 1.184 bytes per le chiavi públicas e 1.088 bytes per i criptogramas.
- **Kyber1024**: livello di sicurezza di 256 bits, con tamaños di chiave di 3.168 bytes per le chiavi secretas, 1.568 bytes per le chiavi públicas e 1.568 bytes per i criptogramas.

Questi tamaños relativamente pequeños hacen che `CRYSTALS-Kyber` sea atractivo per i dispositivos con recursos limitados: smartphones e dispositivos IoT. Reducen anche il ancho di banda requerido per transmitir le chiavi, lo che può essere beneficioso per le applicazioni con conectividad di rete limitada.

#### Velocidad inquebrantable: un faro in il panorama finanziario veloz

Altro aspecto del atractivo di `CRYSTALS-Kyber` è il suo velocità. In il settore bancario e finanziario veloz, la velocità cuenta tanto come la sicurezza. Il diseño del algoritmo garantisce che opere rapidamente, facilitando processi di cifrado e descifrado veloces. Questa eficiencia non è statoce a costa della sicurezza; più bene è un resultado directo dei fundamentos matemáticos sofisticados del algoritmo.

### CRYSTALS-Kyber: una simbiosis di sicurezza, eficiencia e velocità

`CRYSTALS-Kyber` ha emergido come un líder in la ricerca di criptografía resistente a lo quantistico, ofreciendo una combinación única di sicurezza, eficiencia e velocità. Il suo approccio innovador basato in retículos, i suoi tamaños di chiave più pequeños e il suo diseño optimizado lo convertono in una elección ideal per proteger la informazione sensible in la banca e i servizi finanziari. Mentre il mondo continúa abrazando le tecnologie digitali, `CRYSTALS-Kyber` se posiciona per desempeñar un papel pivote in la protección di i nostri dati in i próximos años.

![Divider][01].class=\"m-10 w-100\"

## Impatto

### CRYSTALS-Kyber: vantaggi per la banca e i servizi finanziari

La industria bancaria e finanziaria è in una carrera constante per adelantarse a ciberamenazas ogni volta più sofisticadas. In questo contexto, `CRYSTALS-Kyber` se distingue non solo per i suoi propiedades resistentes a lo quantistico (QR) sino anche per i beneficios tangibles che offre a questa industria. Questa sección dettaglia le vantaggi pratiche di `CRYSTALS-Kyber`, subrayando perché è particularmente adecuado per le necesidades únicas delle istituzioni finanziarie.

- **Seguridad reforzada con chiavi più pequeñas**: una delle vantaggi più significative di `CRYSTALS-Kyber` è il suo capacità per creare chiavi di cifrado più pequeñas senza sacrificar la sicurezza. In un settore dove le brechas di dati possono avere consecuencias catastróficas, una sicurezza robusta non è negociable. I tamaños di chiave più pequeños di `CRYSTALS-Kyber` simplifican i processi di gestión di chiavi, factor crítico in i grandi sistemi bancari dove miles di chiavi sono in juego. Esto non solo refuerza la sicurezza, sino che anche optimiza la eficiencia di almacenamiento e transmisión, factor crucial in una época in che la velocità e il espacio sono valiosos.

- **Velocidad e eficiencia**: in i servizi finanziari, dove le transazioni se producen in milisegundos, la velocità delle operazioni crittografiche è crucial. `CRYSTALS-Kyber` sobresale in questo aspecto, ofreciendo processi rápidos di generación di chiavi, encapsulación e desencapsulación. Questa velocità garantisce che le medidas di sicurezza non se conviertan in un cuello di botella in i entornos di trading di alta frecuencia o durante transazioni il suo larga scala. Inoltre, la eficiencia di `CRYSTALS-Kyber` se traduce in una reducción dei recursos di cálculo, conduciendo a risparmi di costo e a operazioni più respetuosas con il medio ambiente.

- **Perdurabilidad rispetto alle minacce quantistiche**: con il advenimiento della calcolo quantistico, la industria afronta un futuro in il che i métodos crittografici tradicionales potrebbero quedar obsoletos. Al adoptar `CRYSTALS-Kyber`, le istituzioni finanziarie non solo aseguran il suo presente sino che anche se preparan per un mondo post-quantistico. Questo approccio proactivo della ciberseguridad demuestra un compromiso con la protección a lungo termine dei dati, consideración esencial per le partes interesadas e i clienti che priorizan la sicurezza.

- **Cumplimiento normativo e vantaggio competitiva**: man mano che i reguladores mundiales empiezan a reconocer la minaccia quantistica, è probable che impongan la adopción di algoritmos resistentes a lo quantistico. La adopción temprana di `CRYSTALS-Kyber` posiciona alle istituzioni finanziarie come líderes in conformità e sicurezza. Inoltre, offre una vantaggio competitiva, tranquilizando a clienti e socios su il compromiso della istituzione con pratiche di sicurezza punteras.

![Divider][01].class=\"m-10 w-100\"

## Incentivi

### Il caso per la adopción di CRYSTALS-Kyber

In un panorama dove la ciberseguridad non è solo una necesidad sino un diferenciador competitivo, la industria bancaria e finanziaria se encuentra in un punto crítico. La adopción di `CRYSTALS-Kyber` rappresenta un movimiento estratégico, alineándose tanto con le necesidades di sicurezza actuales come con i giros tecnológicos futuros. Questa última sección describe i incentivos convincentes per integrar `CRYSTALS-Kyber` in la infraestructura crittografica dei servizi finanziari.

- **Adelantarse alle tendencias di ciberseguridad**: il auge della calcolo quantistico plantea una amenaza significativa per i algoritmos tradicionales di cifrado, haciéndolos vulnerables al descifrado per i futuros computer quantistici. Al adoptar `CRYSTALS-Kyber`, le istituzioni finanziarie possono proteger i suoi dati sensibles e infraestructuras críticas rispetto a queste amenazas emergentes.

- **Eficiencia operativa e rentabilidad**: i tamaños di chiave compactos e i algoritmos eficientes di `CRYSTALS-Kyber` conducen a risparmi sustanciales di costo. Comparado con i algoritmos tradicionales, `CRYSTALS-Kyber` reduce le necesidades di almacenamiento fino a in un 50 % e il consumo di ancho di banda fino a in un 30 %, generando risparmi significativi per le istituzioni finanziarie con grandi volúmenes di dati.

- **Alineación normativa e gestión di rischi**: con diversi organismos reguladores —tra ellos il NIST e la European Union Agency for Cybersecurity (ENISA)— recomendando activamente la adopción di soluzioni crittografiche resistentes a lo quantistico, i adoptantes tempranos di `CRYSTALS-Kyber` saranno bene posicionados per soddisfare le futuras exigencias normativas e mitigar i rischi jurídicos potenciales.

- **Reforzar la confianza del cliente e la reputación institucional**: istituzioni finanziarie di primo livello come Barclays e Deutsche Bank hanno adoptado `CRYSTALS-Kyber` per proteger i dati clienti e asegurar transazioni finanziarie críticas. Questo compromiso con una sicurezza avanzada non solo ha protegido a queste istituzioni di potenciales ciberataques, sino che anche ha reforzado il suo reputación come guardianes di confianza della informazione sensible.

![Divider][01].class=\"m-10 w-100\"

## Conclusione

### Asegurar il futuro finanziario con CRYSTALS-Kyber

Ante la evolución delle amenazas di ciberseguridad, la industria bancaria e finanziaria afronta una elección crítica. I algoritmos tradicionales di cifrado, antaño considerados seguros, sono ora vulnerables rispetto alla potencia emergente della calcolo quantistico. `CRYSTALS-Kyber` emerge come un faro di sicurezza, ofreciendo una soluzione robusta, eficiente e perdurable per proteger i activos digitali del settore finanziario.

Con il suo combinación única di funzionalità QR, eficiencia operativa e tamaños di chiave più pequeños, `CRYSTALS-Kyber` è un game-changer per la sicurezza finanziaria. Al adoptar `CRYSTALS-Kyber`, le istituzioni non solo aseguran i suoi operazioni actuales sino che anche se preparan per un futuro in il che la calcolo quantistico redefine la ciberseguridad. Questo approccio proactivo demuestra un compromiso con i più altos standard di sicurezza, reforzando la confianza del cliente e la resistencia della industria rispetto alle amenazas in evolución.

In un mondo ogni volta più interconectado e digitale, `CRYSTALS-Kyber` se alza come un testimonio del potere delle soluzioni innovadoras e orientadas al futuro. Il suo adopción per istituzioni finanziarie di primo livello come Barclays e Deutsche Bank è un fuerte respaldo a i suoi capacità e una señal chiara alla industria per abrazar questa soluzione crittografica resistente a lo quantistico.

![Divider][01].class=\"m-10 w-100\"

In conclusión, espero che questa exploración di `CRYSTALS-Kyber` haya iluminado il profundo impacto della criptografía resistente a lo quantistico in il settore finanziario. Se desea sumergirse più profundamente in questa tecnologia revolucionaria o ha preguntas, le invito a contactarme in [LinkedIn ⧉][02] o attraverso la [página di contacto][00].

Gracias di nuovo per il suo tiempo, espero avere noticias suyas.

[00]: /contact/index.html "Contact"
[01]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
[02]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau on LinkedIn"
[03]: /2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html "Protecting Data in the Quantum Age: The Hash Library (HSH)"
[04]: https://cloudcdn.pro/stocks/diagrams/alice-bob-eve-kyber.svg "CRYSTALS-Kyber Key Encapsulation Mechanism (KEM)"
[05]: https://www.nist.gov/ "The National Institute of Standards and Technology (NIST)"
