---
title: "Blockchain के पीछे की प्रौद्योगिकी को समझना"
subtitle: "वितरित बही, क्रिप्टोग्राफी और सहमति का परस्पर मेल"
description: "Blockchain वितरित बही, क्रिप्टोग्राफी और सहमति-तंत्रों को कैसे जोड़ती है — इसकी एक स्पष्ट व्याख्या।"
date: "January 9, 2018"
language: "hi-IN"
locale: "hi_IN"
banner: "https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp"
banner_alt: "नेटवर्क-कनेक्शन दर्शाता डिजिटल अमूर्त चित्र"
keywords: "blockchain, वितरित बही, क्रिप्टोग्राफी, सहमति, proof-of-work, smart contract, हैश, मर्कल वृक्ष, विकेंद्रीकरण, P2P"
---

![नेटवर्क-कनेक्शन दर्शाता डिजिटल अमूर्त चित्र](https://cloudcdn.pro/stocks/images/adam-smigielski-K5mPtONmpHM.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Blockchain वितरित बही, क्रिप्टोग्राफी और सहमति-तंत्रों को कैसे जोड़ती है — इसकी एक स्पष्ट व्याख्या। (DRAFT — मशीन-सहायता प्राप्त हिंदी अनुवाद; देशी समीक्षा लंबित।)
>
> **मुख्य निष्कर्ष**
>
> - यह लेख एक तकनीकी विषय का विश्लेषण प्रस्तुत करता है।
> - मुख्य अवधारणाएँ ऊपर परिभाषित की गई हैं।
> - बैंकिंग और वित्तीय निहितार्थ नीचे विवेचित हैं।
> - प्रौद्योगिकी, अंगीकार और जोखिमों पर दृष्टिकोण साझा किया गया है।
> - दीर्घकालिक रुझान निष्कर्ष में सारांशित हैं।


## दृष्टिकोण

La प्रौद्योगिकी blockchain है abierto वह puerta को एक नई था का अनुप्रयोग विकेंद्रीकृत (dApps) जो operan का forma independiente, बिना नियंत्रण centralizado. Ethereum proporciona एक प्लेटफ़ॉर्म potente के लिए रचना dApps complejas और smart contracts.

Uno का वे उपयोग अधिक prometedores का Ethereum है वह lanzamiento का क्रिप्टोकरेंसी और टोकन digitales personalizados. En यह guía completa examinaremos paso को paso cómo रचना उसका propio टोकन क्रिप्टोग्राफिक sobre Ethereum.

## विचार

Nuestro objetivo है निर्माण करना एक क्रिप्टोकरेंसी sencilla sobre Ethereum, ofreciéndole एक experiencia práctica का विकास blockchain. Estos हैं वे pasos कुंजी जो cubriremos:

### Diseñar वह क्रिप्टोकरेंसी

La पहली tarea crucial है diseñar उसका क्रिप्टोकरेंसी. Esto abarca वह definición का atributos कुंजी:

- **Nombre**: elija एक nombre único जो represente वह identidad और वह propósito के टोकन.
- **Símbolo**: elija एक símbolo corto जैसे BTC के लिए Bitcoin. Se उपयोग करता है में वे exchanges.
- **Oferta total**: determine वह número máximo का टोकन में circulación.
- **Decimales**: defina वह divisibilidad का उसका टोकन, जैसे 2 के लिए céntimos.
- **Funcionalidades adicionales**: añada opcionalmente extras जैसे minting, burning, freezing, etc.

### Escribir smart contracts

Para dar vida को उसका क्रिप्टोकरेंसी, deberá codificar smart contracts जो definan वह funcionalidad और वे reglas के टोकन. Los smart contracts हैं scripts programáticos almacenados में blockchain जो se ejecutan automáticamente जब se cumplen ciertas condiciones.

Estas हैं algunas capacidades कुंजी जो hacen जो वे smart contracts sean idóneos के लिए वे क्रिप्टोकरेंसी:

- **Autoejecución**: se activan automáticamente, बिना intervención का एक तीसरा.
- **Inmutabilidad**: एक vez desplegado, वह कोड नहीं puede modificarse. Esto सुनिश्चित करता है वह सुरक्षा.
- **Autonomía**: नहीं है आवश्यक कोई नहीं autoridad central के लिए gestionar वे smart contracts.
- **Transparencia**: cualquiera puede inspeccionar वह lógica का एक smart contract.
- **Automatización**: acciones जैसे वह transferencia का fondos pueden automatizarse mediante वह कोड के contrato.
- **Seguridad**: वे fondos depositados में एक contrato quedan protegidos hasta जो se cumplen वे condiciones का liberación.
- **Eficiencia**: वे smart contracts eliminan बिचौलिये, haciendo वे procesos अधिक rápidos और कम costosos.

Ejemplo का कोड का contrato में Solidity.

```solidity
pragma solidity ^0.8.0;

contract MyToken {

  string public name;
  string public symbol;
  uint256 public decimals;
  uint256 public totalSupply;

  constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _totalSupply) {
    name = _name;
    symbol = _symbol;
    decimals = _decimals;
    totalSupply = _totalSupply;
  }

}
```

Este contrato básico अनुमति देता है रचना एक टोकन के साथ propiedades जैसे nombre, símbolo, decimales और आपूर्ति total.

La función `constructor` inicializa ये parámetros में वह momento के despliegue के contrato.

Este ejemplo se limita को configurar propiedades básicas. Extendería वह contrato के लिए añadir अधिक funcionalidades:

- Transferencias का टोकन बीच direcciones
- Gestión का saldos
- Autorizaciones (allowances) के लिए gastar टोकन
- Minting और burning का टोकन
- Congelación या bloqueo का transferencias का टोकन
- Implementación का मानक का टोकन जैसे ERC-20
- Despliegue e interacción के साथ वह contrato

### Desarrollo और pruebas locales

Antes का desplegar उसका क्रिप्टोकरेंसी में blockchain Ethereum, है prudente realizar pruebas locales exhaustivas. Esto सुनिश्चित करता है जो उसका क्रिप्टोकरेंसी funcione जैसे se espera, बिना bugs ni vulnerabilidades imprevistas.

Para empezar, siga ये pasos:

#### Descargar Go-Ethereum (Geth)

Comience descargando [Go-Ethereum][00], भी llamado Geth, एक cliente Ethereum escrito में Go. Geth actúa जैसे interfaz का línea का comandos (CLI) Ethereum, ejecutable में Windows, Mac और Linux. Es एक उपकरण versátil जो अनुमति देता है माइन करना, रचना e interactuar के साथ smart contracts में वह नेटवर्क Ethereum.

#### Instalar Ethereum

Una vez descargado Geth, instale Ethereum. Para वे requisitos previos detallados e instrucciones का compilación completas, consulte वे [Installation Instructions][01] disponibles में उसका wiki oficial.

#### Configurar एक entorno का विकास

Para facilitar वह विकास का उसका क्रिप्टोकरेंसी, necesitará एक entorno का विकास, एक framework का pruebas और एक canalización का activos के लिए Ethereum. Las instrucciones detalladas के लिए instalar ये उपकरण esenciales se encuentran में वह wiki का Ethereum.

#### Desplegar में एक testnet

Una vez जो उसका क्रिप्टोकरेंसी supere वे pruebas locales, puede desplegarla में एक testnet. Una testnet है एक entorno seguro और controlado जो imita वह mainnet का Ethereum, permitiéndole evaluar वह निष्पादन का उसका क्रिप्टोकरेंसी में एक entorno real, बिना जोखिम वित्तीय real.

## प्रभाव

Al निर्माण करना एक क्रिप्टोकरेंसी basada में Ethereum desde cero, obtendrá:

- Un ज्ञान profundo का वे अनुप्रयोग विकेंद्रीकृत (dApps) और का वह programación का smart contracts
- Experiencia práctica के साथ वह programación में Solidity
- Una comprensión का वे प्रोटोकॉल का consenso का Ethereum
- Familiaridad के साथ मानक का टोकन जैसे ERC-20

Este aprendizaje le otorgará वे medios के लिए aprovechar वह प्रौद्योगिकी blockchain में समाधान innovadoras.

## प्रोत्साहन

Completar एक construcción का टोकन का extremo को extremo desbloquea एक experiencia práctica का पहली mano के साथ:

- La arquitectura blockchain
- La mecánica का वे क्रिप्टोकरेंसी
- El विकास का smart contracts
- Las capacidades और limitaciones का Ethereum

Adquirirá competencias valiosas के लिए hacer avanzar उसका carrera में programación blockchain.

## निष्कर्ष

En वह campo का वह प्रौद्योगिकी blockchain, वह comprensión se gana mejor के माध्यम से वह puesta में práctica. Construir एक क्रिप्टोकरेंसी sobre वह प्लेटफ़ॉर्म Ethereum प्रदान करता है एक अवसर única का adquirir experiencia का पहली mano के साथ वे capacidades और limitaciones का वह प्रौद्योगिकी. Esta guía le arma के साथ वे conocimientos और competencias के लिए emprender यह apasionante viaje, favoreciendo वह नवाचार और वह descubrimiento में वह universo में perpetua evolución के विकास blockchain और क्रिप्टो.

[00]: https://geth.ethereum.org/downloads/
[01]: https://geth.ethereum.org/docs/getting-started/installing-geth
