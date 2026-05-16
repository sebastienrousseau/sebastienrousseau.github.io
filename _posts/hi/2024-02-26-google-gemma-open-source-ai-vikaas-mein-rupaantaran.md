---
title: "Google Gemma: ओपन-सोर्स AI-विकास का रूपांतरण"
subtitle: "हल्के, स्थानीय-तैनात-योग्य मॉडल का परिवार"
description: "Google Gemma: एक ओपन-सोर्स मॉडल-परिवार जो स्थानीय-तैनात AI-विकास को बढ़ावा देता है।"
date: "February 26, 2024"
language: "hi-IN"
locale: "hi_IN"
banner: "https://cloudcdn.pro/stocks/images/ai-ship.webp"
banner_alt: "Google Gemma का प्रतीक"
keywords: "Gemma, Google, ओपन सोर्स, AI, LLM, फ़ाइन-ट्यूनिंग, स्थानीय, edge, Gemini, मॉडल"
---

## El मॉडल का IA का ओपन-सोर्स क्रांतिकारी का Google के लिए एक ML पहुँच-योग्य और ético

Google है lanzado recientemente [**Gemma ⧉**][00], एक मॉडल का कृत्रिम-बुद्धिमत्ता का ओपन-सोर्स diseñado के लिए proporcionar एक base पहुँच-योग्य और ética को विकास IA. Como मॉडल का ओपन-सोर्स, Gemma प्रदान करता है उसका arquitectura completa, उसका metodología का entrenamiento, उसके pesos और parámetros निम्न licencias permisivas के लिए जो investigadores और डेवलपर externos accedan libremente, aprendan, construyan और personalicen según उसके necesidades. Este enfoque पारदर्शी अनुमति देता है भी escrutar वे prácticas का विकास का Gemma के लिए समर्थन देना वह rendición का cuentas.

Con configuraciones जैसे `Gemma 2B` और `7B`, cubre एक amplia gama का अनुप्रयोग, desde वे dispositivos móviles hasta वे अवसंरचनाएँ cloud. La परिचय का Gemma में वह समुदाय का ओपन-सोर्स atestigua वह fuerte compromiso का Google के साथ एक IA ética, favoreciendo वह नवाचार और वह colaboración के साथ वे डेवलपर के mundo entero.

Este artículo explora वह arquitectura का Gemma, उसका integración के साथ macOS और उसका potencial के लिए बदलना वे समाधान empresariales और वह panorama IA अधिक amplio.

![Google Gemma Logo - Source: Google](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/gemma.svg).class=\"fade-in w-25 p-5 float-end\"

> **TL;DR.** Google Gemma: एक ओपन-सोर्स मॉडल-परिवार जो स्थानीय-तैनात AI-विकास को बढ़ावा देता है। (DRAFT — मशीन-सहायता प्राप्त हिंदी अनुवाद; देशी समीक्षा लंबित।)
>
> **मुख्य निष्कर्ष**
>
> - यह लेख एक तकनीकी विषय का विश्लेषण प्रस्तुत करता है।
> - मुख्य अवधारणाएँ ऊपर परिभाषित की गई हैं।
> - बैंकिंग और वित्तीय निहितार्थ नीचे विवेचित हैं।
> - प्रौद्योगिकी, अंगीकार और जोखिमों पर दृष्टिकोण साझा किया गया है।
> - दीर्घकालिक रुझान निष्कर्ष में सारांशित हैं।


## Comprender Gemma

### वास्तुकला técnica का Gemma

La arquitectura Gemini का Google inspira को Gemma, और Gemma está उपलब्ध में dos configuraciones principales:

- El मॉडल **Gemma 2B** está optimizado के लिए वह दक्षता में dispositivo के साथ एक huella का memoria और एक consumo का energía अधिक bajos. Esto lo convierte में ideal के लिए अनुप्रयोग móviles और embebidas जैसे वे bots conversacionales में smartphones या dispositivos domóticos.

- El मॉडल **Gemma 7B** tiene एक capacidad significativamente mayor, adaptada को tareas अधिक complejas जैसे वह análisis का grandes conjuntos का डेटा और documentos. Su terreno है वह centro का डेटा और वह अवसंरचना cloud जो ejecuta inferencias sobre bases का डेटा.

Ambos proporcionan bloques का construcción IA polivalentes के लिए उपयोग जो van के proyecto personal को वे समाधान empresariales.

### Entrenamiento और capacidades का Gemma

Según उसका [**informe técnico ⧉**][01], वे मॉडल Gemma (2B और 7B) हैं avanzados, entrenados sobre conjuntos का डेटा masivos जो ponen énfasis में वह contenido वेब, वे matemáticas और वह programación. Estos मॉडल, को diferencia का उसका predecesor Gemini, नहीं priorizan वे funcionalidades multilingües या multimodales. Incorporan एक vocabulario completo और emplean एक नया enfoque का टोकनीकरण, mejorando वह gestión का tipos का डेटा diversificados. Su instruction-tuning, combinando aprendizaje supervisado और aprendizaje द्वारा refuerzo से शुरू होकर retroalimentación humana, se concentra únicamente में वह inglés, optimizando वह comprensión और वह generación का texto matizadas. Esta नवाचार metodológica subraya उसका potencial में ámbitos especializados, ilustrando वह panorama में evolución के entrenamiento का मॉडल का lenguaje.

### Gemma और वह समुदाय का ओपन-सोर्स

Como salida का ओपन-सोर्स निम्न [**licencias permisivas ⧉**][03], Gemma representa भी वह compromiso का Google के साथ एक colaboración ética में IA. Los डेवलपर externos pueden ahora apoyarse में Gemma, examinarla और personalizarla का manera पारदर्शी के लिए democratizar वह पहुँच और समर्थन देना वह rendición का cuentas.

![divider][divider].class=\"m-10 w-100\"

![Ollama Logo - Source: Ollama](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/ollama.svg).class=\"fade-in w-25 p-5 float-start\"

## Integrar Google Gemma के साथ Ollama में macOS

[**Ollama ⧉**][02] है एक interfaz जो अनुमति देता है explorar वे asistentes IA localmente में एक तंत्र macOS. Vamos को utilizarla के लिए configurar वे मॉडल Gemma 2B और 7B में वे ordenadores Apple serie M. Esta guía lo acompañará में वह proceso का integración का Gemma के साथ Ollama में macOS.

Puede उपयोग करना वह comando uname के लिए mostrar वह arquitectura के procesador. Abra Terminal और ejecute:

```bash
uname -m
```

Si वह salida है `arm64`, tiene एक Mac serie M. Si है `x86_64`, tiene एक Mac Intel. Esta guía है के लिए वे Mac serie M.

### Configuración के entorno

#### 1. Asegúrese का जो Python 3.8+, pip, venv estén instalados

Antes का empezar, compruebe जो tiene [**Python 3.8 ⧉**][04] या अधिक reciente में उसका Mac, así जैसे वे उपकरण `pip` और `venv`. Puede comprobar उसके versiones का Python और pip और actualizar pip के साथ वे siguientes comandos में Terminal:

```bash
python3 --version
pip3 --version
pip3 install --upgrade pip
```

#### 2. Crear एक entorno virtual के लिए aislar वे dependencias

Abra Terminal और cree एक entorno virtual के लिए रोकना वे conflictos के साथ वे paquetes के तंत्र.

```bash
python3 -m venv gemma_env
source gemma_env/bin/activate
```

#### 3. Instalar वह última versión का Ollama के लिए macOS

Descargue वह [**última versión का Ollama ⧉**][05] के लिए macOS desde वह sitio oficial. Extraiga और mueva वह अनुप्रयोग Ollama को उसका carpeta Aplicaciones. Ábrala और siga वे instrucciones का instalación.

#### 4. Confirmar जो वह instalación का Ollama है sido exitosa

Compruebe जो Ollama está correctamente instalado ejecutando:

```bash
ollama --version
```

Debería ver वह versión का Ollama mostrada.

### अनुशंसाएँ के तंत्र

Para एक निष्पादन óptimo का Gemma 2B, necesitará:

- **Procesador**: Intel i5 multinúcleo या superior
- **Memoria**: 16 GB का RAM (32 GB के लिए Gemma 7B)
- **Almacenamiento**: 50 GB का espacio libre SSD
- **macOS**: actualizado (Monterey या posterior)

Una vez configurado Ollama, está listo के लिए inicializar e interactuar के साथ वे मॉडल Gemma localmente.

![divider][divider].class=\"m-10 w-100\"

## Inicializar एक instancia Gemma local

### 1. Lanzar वह मॉडल Gemma mediante वह CLI Ollama

Elija वह मॉडल Gemma जो desea ejecutar:

- Gemma 2B (मॉडल अधिक छोटा): `ollama run gemma:2b`
- Gemma 7B (मॉडल अधिक बड़ा): `ollama run gemma:7b`

### 2. El पहला lanzamiento descargará वे activos के मॉडल (puede llevar tiempo)

El पहला lanzamiento descargará वह मॉडल Gemma seleccionado, lo जो puede llevar tiempo. Una vez terminado, Gemma se inicializará के लिए उसका उपयोग.

#### Ejemplo का consulta conversacional

```bash
>>> Hello Gemma. How are you today?
```

Gemma responderá के साथ एक respuesta में lenguaje natural.

```bash
>>> Hello Gemma. How are you today?
Hello! It's को lovely day to be alive. Thank you for asking. How are you doing today? 😊
```

### Desactivar वह entorno virtual

```bash
deactivate
```

Esto volverá को entorno Python predeterminado का उसका तंत्र.

Para obtener ayuda में caso का समस्या या अधिक detalles sobre वह configuración, consulte वह [Documentación Ollama ⧉](https://ollama.com/docs) और वह [Documentación Gemma ⧉](https://github.com/google-deepmind/gemma).

![divider][divider].class=\"m-10 w-100\"

## El impacto का ओपन-सोर्स का Gemma

Desde उसका lanzamiento, Gemma है acelerado rápidamente वह नवाचार gracias को उसका enfoque का ओपन-सोर्स पहुँच-योग्य और colaborativo.

Las licencias permisivas permiten भी examinar वह arquitectura का Gemma के साथ fines का investigación और aportar modificaciones को एक nivel muy granular. Los डेवलपर हैं compartido ajustes, personalizaciones और capacidades completamente नई में वे प्लेटफ़ॉर्म का colaboración का कोड.

Este esfuerzo comunitario continúa mejorando वे capacidades का Gemma के लिए निर्माण करना तंत्र का IA éticos और responsables, alineados के साथ वे mejores prácticas emergentes.

Con वह tiempo, podría emerger एक तंत्र का उपकरण, integraciones और अनुप्रयोग enteramente नई के लिए Gemma gracias को उसका naturaleza का प्लेटफ़ॉर्म का ओपन-सोर्स.

![divider][divider].class=\"m-10 w-100\"

## उपयोग-मामले Gemma के लिए समाधान empresariales

El मॉडल का IA का Google, Gemma, propone diversas समाधान empresariales के साथ उसका arquitectura técnica और उसका naturaleza का ओपन-सोर्स के लिए responder को necesidades empresariales específicas.

### 1. Chatbots और agentes conversacionales

El मॉडल अधिक छोटा, Gemma 2B, está optimizado के लिए वह दक्षता में dispositivo, lo जो lo convierte में ideal के लिए विकसित करना **bots conversacionales** और **asistentes virtuales**. Las उद्यम pueden desplegar ये agentes IA में dispositivos móviles या तंत्र embebidos के लिए बेहतर बनाना वह servicio को cliente, वह soporte और वह compromiso बिना necesidad का recursos का cálculo extensivos.

Aunque Gemma acaba का lanzarse, उसके capacidades se alinean bien के साथ वे अनुप्रयोग existentes का chatbots IA और agentes virtuales जो asisten को वे ग्राहक. A medida जो Gemma madure, esperamos ver integraciones directas जो permitan interfaces conversacionales का नई generación.

### 2. Análisis का डेटा e insights

El मॉडल Gemma 7B अधिक बड़ा, के साथ उसका capacidad superior के लिए tareas complejas, está bien adaptado को análisis का grandes conjuntos का डेटा और documentos. Las उद्यम pueden aprovechar यह मॉडल के लिए extraer perspectivas, tendencias और patrones से शुरू होकर grandes cantidades का डेटा, ayudando को वह toma का decisiones और को वह planificación estratégica.

### 3. Creación और सारांश का contenido

Los मॉडल Gemma pueden ayudar को generar और resumir contenido: informes, artículos, materiales का marketing. Esta capacidad puede कम करना significativamente वह tiempo और वह esfuerzo requeridos के लिए producir contenido का उच्च calidad, permitiendo को वे उद्यम concentrarse में वह creatividad और वह estrategia.

### 4. Email marketing personalizado और segmentación publicitaria

Comprendiendo और generando lenguaje natural, Gemma puede ayudar को वे उद्यम को रचना campañas का email marketing और estrategias का segmentación publicitaria अधिक personalizadas और eficaces. Este caso का उपयोग puede conducir को एक compromiso के cliente और एक tasa का conversión mejorados.

### 5. Tratamiento के lenguaje natural (NLP) के लिए dispositivos edge

Las optimizaciones का Gemma lo hacen adecuado के लिए वह ejecución का tareas NLP directamente में वे dispositivos edge. Esta capacidad अनुमति देता है वह toma का decisiones empresariales में tiempo real e integraciones अधिक fluidas के साथ वह mundo real: distribución, fabricación, अनुप्रयोग IoT.

### 6. Inteligencia का कोड के लिए डेवलपर

Gemma puede reforzar वह productividad का वे डेवलपर proporcionando interfaces में lenguaje natural के लिए वे tareas का edición का कोड और विकास. Por ejemplo, वे डेवलपर pueden उपयोग करना consultas conversacionales के लिए obtener recomendaciones का कोड, descripciones का funciones, ayuda को debugging और revisiones का कोड. Gemma analizaría वह contexto और वह semántica के लिए dar sugerencias pertinentes. Este «copiloto IA» puede ayudar को racionalizar वे flujos का trabajo, कम करना वे errores और acelerar वह विकास का productos impulsados द्वारा IA.

### 7. Aplicaciones multimodales

Con उसका capacidad के लिए tratar जानकारी के माध्यम से texto, voz और visión, Gemma है polivalente के लिए वे casos का उपयोग multimodales. Esta funcionalidad है particularmente beneficiosa के लिए वे अनुप्रयोग जो आवश्यक हैं interacción के साथ वे उपयोगकर्ता का manera अधिक natural e intuitiva, जैसे वे experiencias VR और AR.

La naturaleza का ओपन-सोर्स का Gemma और उसका versatilidad técnica lo convierten में एक उपकरण valiosa के लिए वे उद्यम जो buscan aprovechar वह IA में उसके necesidades operativas. Gemma है hábil के लिए रचना asistentes virtuales और chatbots जो mejoran वह experiencia के cliente और puede gestionar grandes cantidades का análisis का डेटा. Su मॉडल का ओपन-सोर्स fomenta भी वह नवाचार और वह colaboración, permitiendo को वे उद्यम personalizar Gemma के लिए responder को उसके necesidades.

![divider][divider].class=\"m-10 w-100\"

## ¿Qué reserva वह भविष्य?

En वह horizonte, Gemma está posicionado के लिए एक mayor विकास और विकास. Hay esfuerzos में curso के लिए बेहतर बनाना उसका compatibilidad के साथ diversos entornos का हार्डवेयर, reforzar वह soporte का lenguas adicionales और ampliar उसका espectro का अनुप्रयोग. Google और Gemma aspiran को abordar वे चुनौतियाँ vinculados को वह precisión, वह detección का sesgos और वह उपयोग seguro का वे डेटा, posicionando को Gemma जैसे एक líder के विकास का वह IA ética.

![divider][divider].class=\"m-10 w-100\"

## निष्कर्ष

El lanzamiento का Gemma है एक momento decisivo में वह campo का वह IA, subrayando एक giro hacia prácticas का विकास अधिक accesibles, éticas और colaborativas. A medida जो continúe evolucionando, Gemma está llamado को desempeñar एक papel pivote में वह definición के भविष्य का वह IA, ofreciendo एक मॉडल के लिए वह manera में जो वे proyectos का ओपन-सोर्स pueden estimular वह नवाचार को वह vez जो respetan मानक éticos.

[00]: https://ai.google.dev/gemma "Google Gemma AI"
[01]: https://storage.googleapis.com/deepmind-media/gemma/gemma-report.pdf "Gemma Technical Report"
[02]: https://ollama.com "Ollama"
[03]: https://ai.google.dev/gemma/terms "Gemma Licensing"
[04]: https://www.python.org/downloads/release/python-380/ "Python 3.8"
[05]: https://ollama.com/download "Ollama Download"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
