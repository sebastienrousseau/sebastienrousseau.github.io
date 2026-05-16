---
title: "Google Gemma: açık kaynak yapay zeka geliştirmeyi dönüştürmek"
subtitle: "Sorumlu yapay zeka için Google'ın açık modelleri Gemma"
description: "Gemma, Gemini ile aynı araştırma ve teknolojiyle inşa edilen Google'ın yeni hafif açık modeller ailesidir."
date: "February 26, 2024"
language: "tr-TR"
locale: "tr_TR"
banner: "https://cloudcdn.pro/stocks/images/ai-ship.webp"
banner_alt: "Gemma logosu"
keywords: "Gemma, Google, açık kaynak, yapay zeka, LLM, üretken yapay zeka"
---


---

> **TL;DR.** Gemma porta in open source una famiglia di modelli leggeri derivati da Gemini. I pesi sono scaricabili, abilitando ricerca, fine-tuning e deployment on-device su scala.
>
> **Önemli Çıkarımlar**
>
> - **Pesi aperti** — modelli scaricabili per ricerca e deployment.
> - **Dimensioni efficienti** — 2B e 7B parametri, adatti a inferenza on-device.
> - **Licenza permissiva** — uso commerciale consentito con clausole responsibility.
> - **Caso d'uso bancario** — fine-tuning locale per compliance senza esportare dati verso fornitori cloud.

---

## Il modello di IA di open source revolucionario di Google per un ML accesible e ético

Google ha lanzado recientemente [**Gemma ⧉**][00], un modello di intelligenza artificiale di open source progettato per fornire una base accesible e ética al desarrollo IA. Come modello di open source, Gemma offre il suo arquitectura completa, il suo metodología di entrenamiento, i suoi pesos e parámetros sotto licencias permisivas affinché ricercatori e sviluppatori externos accedan libremente, aprendan, construyan e personalicen según i suoi necesidades. Questo approccio transparente consente anche escrutar le pratiche di desarrollo di Gemma per apoyar la rendición di cuentas.

Con configuraciones gibi `Gemma 2B` e `7B`, copre una amplia gama di applicazioni, da i dispositivos móviles fino a le infraestructuras cloud. La introducción di Gemma in la comunità di open source atestigua il fuerte compromiso di Google con una IA ética, favoreciendo la innovación ve colaboración con i sviluppatori ın mondo entero.

Questo artículo explora la arquitectura di Gemma, il suo integración con macOS ve suo potencial per transformar le soluzioni empresariales ve panorama IA daha çok amplio.

![Gemma logosu](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/gemma.svg).class=\"fade-in w-25 p-5 float-end\"

## Comprender Gemma

### Arquitectura tecnica di Gemma

La arquitectura Gemini di Google inspira a Gemma, e Gemma è disponible in dos configuraciones principali:

- Il modello **Gemma 2B** è optimizado için eficiencia in dispositivo con una huella di memoria e un consumo di energía daha çok bajos. Esto lo converte in ideal per applicazioni móviles e embebidas gibi i bots conversacionales in smartphones o dispositivos domóticos.

- Il modello **Gemma 7B** ha una capacità significativamente mayor, adaptada a tareas daha çok complejas gibi il análisis di grandi conjuntos di dati e documentos. Il suo terreno è il centro di dati ve infraestructura cloud che ejecuta inferencias su bases di dati.

Ambos forniscono blocchi di construcción IA polivalentes per usos che van ın progetto personal alle soluzioni empresariales.

### Entrenamiento e capacità di Gemma

Según il suo [**rapporto tecnico ⧉**][01], i modelli Gemma (2B e 7B) sono avanzados, entrenados su conjuntos di dati masivos che ponen énfasis in il contenuto web, le matemáticas ve programación. Questi modelli, a differenza di il suo predecesor Gemini, non priorizan le funzionalità multilingües o multimodales. Incorporan un vocabulario completo e emplean un nuovo approccio di tokenización, mejorando la gestión di tipos di dati diversificados. Il suo instruction-tuning, combinando aprendizaje supervisado e apprendimento per rinforzo a partire da retroalimentación humana, se concentra únicamente in il inglés, optimizando la comprensión ve generación di texto matizadas. Questa innovación metodológica subraya il suo potencial in ámbitos especializados, ilustrando il panorama in evolución ın entrenamiento di modelli di linguaggio.

### Gemma ve comunità di open source

Come salida di open source sotto [**licencias permisivas ⧉**][03], Gemma rappresenta anche il compromiso di Google con una colaboración ética in IA. I sviluppatori externos possono ora apoyarse in Gemma, examinarla e personalizarla in modo transparente per democratizar il acceso e apoyar la rendición di cuentas.

![divider][divider].class=\"m-10 w-100\"

![Ollama Logo - Source: Ollama](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/ollama.svg).class=\"fade-in w-25 p-5 float-start\"

## Integrar Google Gemma con Ollama in macOS

[**Ollama ⧉**][02] è una interfaz che consente explorar i asistentes IA localmente in un sistema macOS. Vamos a utilizarla per configurar i modelli Gemma 2B e 7B in i ordenadores Apple serie M. Questa guía lo acompañará in il processo di integración di Gemma con Ollama in macOS.

Può utilizzare il comando uname per mostrare la arquitectura ın procesador. Abra Terminal e ejecute:

```bash
uname -m
```

Se la salida è `arm64`, ha un Mac serie M. Se è `x86_64`, ha un Mac Intel. Questa guía è için Mac serie M.

### Configuración ın entorno

#### 1. Asegúrese di che Python 3.8+, pip, venv estén instalados

Antes di empezar, compruebe che ha [**Python 3.8 ⧉**][04] o daha çok reciente in il suo Mac, così gibi le strumenti `pip` e `venv`. Può comprobar i suoi versiones di Python e pip e actualizar pip con i seguenti comandos in Terminal:

```bash
python3 --version
pip3 --version
pip3 install --upgrade pip
```

#### 2. Crear un entorno virtual per aislar le dependencias

Abra Terminal e cree un entorno virtual per evitar i conflictos con i paquetes ın sistema.

```bash
python3 -m venv gemma_env
source gemma_env/bin/activate
```

#### 3. Instalar la última versión di Ollama per macOS

Descargue la [**última versión di Ollama ⧉**][05] per macOS da il sitio oficial. Extraiga e mueva la applicazione Ollama a il suo carpeta Aplicaciones. Ábrala e siga le instrucciones di instalación.

#### 4. Confirmar che la instalación di Ollama è stato exitosa

Compruebe che Ollama è correctamente instalado ejecutando:

```bash
ollama --version
```

Debería vedere la versión di Ollama mostrada.

### Öneriler ın sistema

Per un prestazioni óptimo di Gemma 2B, necesitará:

- **Procesador**: Intel i5 multinúcleo o superior
- **Memoria**: 16 GB di RAM (32 GB per Gemma 7B)
- **Almacenamiento**: 50 GB di espacio libre SSD
- **macOS**: actualizado (Monterey o posterior)

Una vez configurado Ollama, è listo per inicializar e interactuar con i modelli Gemma localmente.

![divider][divider].class=\"m-10 w-100\"

## Inicializar una instancia Gemma locale

### 1. Lanzar il modello Gemma mediante la CLI Ollama

Elija il modello Gemma che desea ejecutar:

- Gemma 2B (modello daha çok pequeño): `ollama run gemma:2b`
- Gemma 7B (modello daha çok grande): `ollama run gemma:7b`

### 2. Il primer lanzamiento descargará i activos ın modello (può llevar tiempo)

Il primer lanzamiento descargará il modello Gemma seleccionado, lo che può llevar tiempo. Una vez terminado, Gemma se inicializará için suo uso.

#### Ejemplo di consulta conversacional

```bash
>>> Hello Gemma. How are you today?
```

Gemma responderá con una respuesta in lenguaje natural.

```bash
>>> Hello Gemma. How are you today?
Hello! It's a lovely day to be alive. Thank you for asking. How are you doing today? 😊
```

### Desactivar il entorno virtual

```bash
deactivate
```

Esto volverá al entorno Python predeterminado di il suo sistema.

Per obtener ayuda in caso di problema o daha çok dettagli su la configuración, consulte la [Documentación Ollama ⧉](https://ollama.com/docs) ve [Documentación Gemma ⧉](https://github.com/google-deepmind/gemma).

![divider][divider].class=\"m-10 w-100\"

## Il impacto di open source di Gemma

Da il suo lanzamiento, Gemma ha acelerado rapidamente la innovación gracias a il suo approccio di open source accesible e colaborativo.

Le licencias permisivas consentono anche examinar la arquitectura di Gemma con fines di ricerca e aportar modificaciones a un livello molto granular. I sviluppatori hanno compartido ajustes, personalizaciones e capacità completamente nuove in le piattaforme di colaboración di código.

Questo esfuerzo comunitario continúa mejorando le capacità di Gemma per costruire sistemi di IA éticos e responsables, alineados con le mejores pratiche emergentes.

Con il tiempo, potrebbe emerger un ecosistema di strumenti, integraciones e applicazioni enteramente nuove per Gemma gracias a il suo naturaleza di piattaforma di open source.

![divider][divider].class=\"m-10 w-100\"

## Casos di uso Gemma per soluzioni empresariales

Il modello di IA di Google, Gemma, propone diversas soluzioni empresariales con il suo arquitectura tecnica ve suo naturaleza di open source per responder a necesidades empresariales específicas.

### 1. Chatbots e agentes conversacionales

Il modello daha çok pequeño, Gemma 2B, è optimizado için eficiencia in dispositivo, lo che lo converte in ideal per sviluppare **bots conversacionales** e **asistentes virtuales**. Le aziende possono desplegar questi agentes IA in dispositivos móviles o sistemi embebidos per migliorare il servizio al cliente, il soporte ve compromiso senza necesidad di recursos di cálculo extensivos.

Sebbene Gemma acaba di lanzarse, i suoi capacità se alinean bene con le applicazioni existentes di chatbots IA e agentes virtuales che asisten ai clienti. A medida che Gemma madure, esperamos vedere integraciones directas che permitan interfaces conversacionales di nuova generación.

### 2. Análisis di dati e insights

Il modello Gemma 7B daha çok grande, con il suo capacità superior per tareas complejas, è bene adaptado al análisis di grandi conjuntos di dati e documentos. Le aziende possono aprovechar questo modello per extraer prospettive, tendencias e patrones a partire da grandi cantidades di dati, ayudando alla toma di decisiones e alla planificación estratégica.

### 3. Creación e resumen di contenuto

I modelli Gemma possono ayudar a generare e resumir contenuto: rapporti, artículos, materiales di marketing. Questa capacità può reducir significativamente il tiempo ve esfuerzo requeridos per producir contenuto di alta qualità, permitiendo alle aziende concentrarse in la creatividad ve estrategia.

### 4. Email marketing personalizado e segmentación publicitaria

Comprendiendo e generando lenguaje natural, Gemma può ayudar alle aziende a creare campañas di email marketing e estrategias di segmentación publicitaria daha çok personalizadas e eficaces. Questo caso d'uso può conducir a un compromiso ın cliente e una tasa di conversión mejorados.

### 5. Tratamiento ın lenguaje natural (NLP) per dispositivos edge

Le optimizaciones di Gemma lo hacen adecuado için ejecución di tareas NLP direttamente in i dispositivos edge. Questa capacità consente la toma di decisiones empresariales in tiempo real e integraciones daha çok fluidas con il mondo real: distribución, fabricación, applicazioni IoT.

### 6. Inteligencia di código per sviluppatori

Gemma può reforzar la productividad ın sviluppatori proporcionando interfaces in lenguaje natural per le tareas di edición di código e desarrollo. Ad esempio, i sviluppatori possono utilizzare consultas conversacionales per obtener recomendaciones di código, descripciones di funciones, ayuda al debugging e revisiones di código. Gemma analizaría il contexto ve semántica per dar sugerencias pertinentes. Questo "copiloto IA" può ayudar a racionalizar i flujos di trabajo, reducir i errores e acelerar il desarrollo di prodotti impulsados per IA.

### 7. Aplicaciones multimodales

Con il suo capacità per tratar informazione attraverso texto, voz e visione, Gemma è polivalente için quasi d'uso multimodales. Questa funzionalità è particularmente beneficiosa per le applicazioni che richiedono interacción con i utenti in modo daha çok natural e intuitiva, gibi le experiencias VR e AR.

La naturaleza di open source di Gemma ve suo versatilidad tecnica lo convertono in una strumento valiosa per le aziende che buscan aprovechar la IA in i suoi necesidades operativas. Gemma è hábil per creare asistentes virtuales e chatbots che mejoran la experiencia ın cliente e può gestire grandi cantidades di análisis di dati. Il suo modello di open source fomenta anche la innovación ve colaboración, permitiendo alle aziende personalizar Gemma per responder a i suoi necesidades.

![divider][divider].class=\"m-10 w-100\"

## Qué reserva il futuro?

In il horizonte, Gemma è posicionado per un mayor crecimiento e desarrollo. C'è esfuerzos in curso per migliorare il suo compatibilidad con diversos entornos di hardware, reforzar il soporte di lenguas adicionales e ampliar il suo espectro di applicazioni. Google e Gemma aspiran a abordar i sfide vinculados alla precisión, la detección di sesgos ve uso seguro ın dati, posicionando a Gemma gibi un líder ın desarrollo ın IA ética.

![divider][divider].class=\"m-10 w-100\"

## Sonuç

Il lanzamiento di Gemma è un momento decisivo in il campo ın IA, subrayando un giro verso pratiche di desarrollo daha çok accesibles, éticas e colaborativas. A medida che continúe evolucionando, Gemma è llamado a desempeñar un papel pivote in la definición ın futuro ın IA, ofreciendo un modello için manera in che i progetti di open source possono estimular la innovación allo stesso tempo che respetan standard éticos.

[00]: https://ai.google.dev/gemma "Google Gemma AI"
[01]: https://storage.googleapis.com/deepmind-media/gemma/gemma-report.pdf "Gemma Technical Report"
[02]: https://ollama.com "Ollama"
[03]: https://ai.google.dev/gemma/terms "Gemma Licensing"
[04]: https://www.python.org/downloads/release/python-380/ "Python 3.8"
[05]: https://ollama.com/download "Ollama Download"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
