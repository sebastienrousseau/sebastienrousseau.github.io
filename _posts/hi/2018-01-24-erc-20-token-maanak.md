---
title: "ERC-20 टोकन-मानक"
subtitle: "Ethereum पर इंटरऑपरेबल टोकन का साझा फ्रेमवर्क"
description: "ERC-20: Ethereum पर टोकन के लिए मानक — टोकन कैसे जारी, अंतरित और परस्पर-संचालित होते हैं।"
date: "January 24, 2018"
language: "hi-IN"
locale: "hi_IN"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Ethereum और टोकन की कलात्मक प्रस्तुति"
keywords: "ERC-20, Ethereum, token, ICO, smart contract, क्रिप्टोकरेंसी, टोकनीकरण, मानक, इंटरऑपरेबिलिटी, blockchain"
---

![Ethereum और टोकन की कलात्मक प्रस्तुति](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

> **TL;DR.** ERC-20: Ethereum पर टोकन के लिए मानक — टोकन कैसे जारी, अंतरित और परस्पर-संचालित होते हैं। (DRAFT — मशीन-सहायता प्राप्त हिंदी अनुवाद; देशी समीक्षा लंबित।)
>
> **मुख्य निष्कर्ष**
>
> - यह लेख एक तकनीकी विषय का विश्लेषण प्रस्तुत करता है।
> - मुख्य अवधारणाएँ ऊपर परिभाषित की गई हैं।
> - बैंकिंग और वित्तीय निहितार्थ नीचे विवेचित हैं।
> - प्रौद्योगिकी, अंगीकार और जोखिमों पर दृष्टिकोण साझा किया गया है।
> - दीर्घकालिक रुझान निष्कर्ष में सारांशित हैं।


## दृष्टिकोण

### La necesidad का एक interfaz का टोकन estandarizada

Antes के advenimiento के मानक ERC-20 (Ethereum Request for Comments 20), blockchain Ethereum se parecía को Lejano Oeste का वे arquitecturas का टोकन. Cada नया टोकन acuñado tenía उसका propio conjunto único का reglas, funciones e interfaces. Esto imponía को वे डेवलपर एक curva का aprendizaje pronunciada और frenaba वह इंटरऑपरेबिलिटी का वे टोकन. En कुछ palabras, cada नया टोकन था जैसे एक नया idioma जो aprender, comprender e implementar. Esta fragmentación obstaculizaba वह मापनीयता और वह adopción masiva का टोकन में वह प्लेटफ़ॉर्म Ethereum.

La परिचय के मानक ERC-20 actuó जैसे एक lenguaje unificador, estableciendo एक conjunto común का reglas और funciones को वे जो सभी वे टोकन Ethereum deben ajustarse. A partir का entonces, वे डेवलपर disponen का एक interfaz coherente, sea cual sea वह टोकन. Esta estandarización fluidificó वे procesos का interacción के साथ वे टोकन, permitiendo एक integración अधिक fluida में diversas अनुप्रयोग और servicios. Como consecuencia, वे डेवलपर pueden interactuar का manera अधिक útil के साथ वे टोकन, propiciando एक entorno favorable को वह नवाचार और को विकास में वह तंत्र Ethereum.

#### El Lejano Oeste का वे arquitecturas का टोकन

La blockchain Ethereum se diseñó inicialmente के लिए soportar एक único tipo का टोकन: ETH. Pero को medida जो वह प्लेटफ़ॉर्म ganó popularidad, वे डेवलपर comenzaron को रचना उसके propios टोकन के लिए representar एक variedad का activos और conceptos. Esto dio lugar को एक proliferación का arquitecturas का टोकन diferentes, cada एक के साथ उसका propio conjunto único का reglas और funciones.

Esta fragmentación dificultaba को वे डेवलपर वह creación का अनुप्रयोग capaces का interactuar के साथ कई टोकन. También complicaba को वे उपयोगकर्ता वह gestión का उसके activos का टोकन में distintas प्लेटफ़ॉर्म.

#### El मानक ERC-20

El मानक ERC-20 se प्रस्तुत किया में 2015 के लिए responder को वे retos planteados द्वारा यह Lejano Oeste का arquitecturas का टोकन. El मानक define एक conjunto común का reglas और funciones को वे जो सभी वे टोकन Ethereum deben ajustarse. Esta estandarización facilita वह creación का अनुप्रयोग capaces का interactuar के साथ cualquier टोकन ERC-20, और भी simplifica वह gestión का वे activos का टोकन द्वारा parte का वे उपयोगकर्ता.

El मानक ERC-20 है sido ampliamente adoptado द्वारा वह समुदाय Ethereum. Hoy में día se contabilizan अधिक का 200.000 टोकन ERC-20 और वह मानक है उपयोग किया गया द्वारा एक gran variedad का अनुप्रयोग, incluidos exchanges विकेंद्रीकृत, प्लेटफ़ॉर्म का préstamo और dapps का juegos.

## विचार

### Un conjunto común का funciones और propiedades के लिए सभी वे टोकन

El मानक ERC-20 define एक conjunto का seis funciones esenciales जो सभी वे टोकन conformes को ERC-20 deben implementar. Estas funciones हैं:

- `transfer(address to, uint256 amount)`: transfiere एक importe का टोकन desde वह dirección के invocador hacia वह dirección especificada.
- `approve(address spender, uint256 amount)`: autoriza को वह dirección especificada को gastar एक importe का टोकन में nombre के invocador.
- `allowance(address owner, address spender)`: devuelve वह importe का टोकन जो वह «spender» especificado está autorizado को gastar में nombre के «owner» especificado.
- `totalSupply()`: devuelve वह número total का टोकन में circulación.
- `balanceOf(address owner)`: devuelve वह número का टोकन जो posee वह dirección especificada.
- `name()`: devuelve वह nombre के टोकन.
- `symbol()`: devuelve वह símbolo के टोकन.

El मानक ERC-20 भी define dos eventos जो deben emitirse tras वह ejecución exitosa का वे funciones correspondientes:

- `Transfer(address from, address to, uint256 amount)`: emitido जब एक importe का टोकन se transfiere का एक dirección को otra.
- `Approval(address owner, address spender, uint256 amount)`: emitido जब वह dirección especificada है autorizada को gastar एक importe का टोकन में nombre के «owner» especificado.

## प्रभाव

### El विकास का DeFi और वह adopción का Ethereum

El मानक ERC-20 है tenido एक impacto significativo में वह तंत्र Ethereum. Ha sido एक catalizador कुंजी के movimiento DeFi (वित्त विकेंद्रीकृत) और भी है contribuido को बढ़ाना वह adopción का Ethereum.

Las प्लेटफ़ॉर्म DeFi, जो प्रदान करते हैं toda एक gama का वित्तीय सेवाएँ जो van desde वह préstamo hasta वह gestión का activos, se apoyan masivamente में वे टोकन के लिए facilitar वे लेनदेन. Con ERC-20 actuando जैसे एक adaptador universal, se volvió mucho अधिक sencillo के लिए वे अनुप्रयोग DeFi integrar एक amplio abanico का टोकन बिना tener जो adaptar उसका कोड को cada uno.

El मानक ERC-20 भी है facilitado वह gestión का वे activos का टोकन द्वारा parte का वे उपयोगकर्ता. Con टोकन जो respetan वे mismas reglas básicas, को वे उपयोगकर्ता les resulta अधिक fácil transferir, gastar और gestionar उसके activos का टोकन में कई प्लेटफ़ॉर्म. Esta experiencia का उपयोगकर्ता mejorada है sido एक motor के वृद्धि का वे tasas का adopción का Ethereum.

## प्रोत्साहन

### Costes का विकास reducidos और सुरक्षा mejorada

La estandarización aportada द्वारा वह प्रोटोकॉल ERC-20 भी है tenido एक impacto económico directo. Al proporcionar एक plano probado और aprobado द्वारा वह समुदाय के लिए वह creación का टोकन, है reducido significativamente वह barrera का entrada के लिए वे डेवलपर. Ahora pueden रचना एक नया टोकन के साथ costes का विकास reducidos और एक plazo का comercialización अधिक corto, बिना tener जो reinventar वह rueda. El मानक fomenta भी indirectamente वह creación का DApps (अनुप्रयोग विकेंद्रीकृत) और servicios capaces का interactuar universalmente के साथ cualquier टोकन ERC-20, cultivando así एक तंत्र अधिक dinámico.

Otro beneficio notable: एक सुरक्षा reforzada. El मानक ERC-20 है sido sometido को एक examen riguroso द्वारा parte का वह समुदाय Ethereum, convirtiéndolo में एक मॉडल robusto और seguro के लिए वह implementación का टोकन. El respeto का यह मानक implica जो वे aspectos fundamentales के smart contract के टोकन जारी रखते हैं वे buenas prácticas aceptadas द्वारा वह समुदाय. Esto minimiza वह जोखिम का vulnerabilidades का सुरक्षा जो का otro modo podrían derivarse का एक मॉडल का टोकन mal diseñado. Aunque नहीं है एक garantía contra todo tipo का vulnerabilidades, है एक paso significativo hacia वह सुरक्षा वैश्विक का वे टोकन और, द्वारा extensión, का वे proyectos जो वे उपयोग करते हैं.
