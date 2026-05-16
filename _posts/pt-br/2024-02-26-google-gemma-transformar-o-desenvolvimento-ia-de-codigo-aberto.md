---
title: "Google Gemma: transformar o desenvolvimento de a IA de código aberto"
subtitle: "Una mirada desde dentro a as capacidades, as contribuciones de código aberto e lo que viene"
description: "Descubra o modelo Gemma de Google: um projeto de código aberto que propone soluções de IA ética para uso personal e empresarial."
date: "February 26, 2024"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/ai-ship.webp"
banner_alt: "Nave futurista azul com neones"
keywords: "Google Gemma, modelo de IA de código aberto, arquitectura técnica Gemma, Gemma 2B 7B, IA ética, integração IA macOS, soluções IA para empresa, IA conversacional, análisis de dados IA, IA para dispositivos edge"
---

## El modelo de IA de código aberto revolucionário de Google para um ML accesible e ético

Google lançou recentemente [**Gemma ⧉**][00], um modelo de inteligência artificial de código aberto diseñado para proporcionar uma base accesible e ética ao desenvolvimento IA. Como modelo de código aberto, Gemma oferece seu arquitectura completa, seu metodología de entrenamiento, seus pesos e parámetros sob licencias permisivas para que investigadores e desenvolvedores externos accedan libremente, aprendan, construyan e personalicen conforme seus necessidades. Este enfoque transparente permite também escrutar as práticas de desenvolvimento de Gemma para apoyar a rendición de cuentas.

Con configuraciones como `Gemma 2B` e `7B`, cubre uma amplia gama de aplicações, desde os dispositivos móveles até as infraestruturas cloud. La introdução de Gemma em a comunidade de código aberto atestigua o fuerte compromiso de Google com uma IA ética, favoreciendo a innovación e a colaboração com os desenvolvedores do mundo entero.

Este artigo explora a arquitectura de Gemma, seu integração com macOS e seu potencial para transformar as soluções empresariales e o panorama IA mais amplio.

![Google Gemma Logo - Source: Google](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/gemma.svg).class=\"fade-in w-25 p-5 float-end\"

## Comprender Gemma

### Arquitectura técnica de Gemma

La arquitectura Gemini de Google inspira a Gemma, e Gemma está disponible em dois configuraciones principales:

- El modelo **Gemma 2B** está optimizado para a eficiência em dispositivo com uma huella de memoria e um consumo de energía mais bajos. Esto lo convierte em ideal para aplicações móveles e embebidas como os bots conversacionales em smartphones ou dispositivos domóticos.

- El modelo **Gemma 7B** tem uma capacidade significativamente mayor, adaptada a tareas mais complejas como o análisis de grandes conjuntos de dados e documentos. Su terreno é o centro de dados e a infraestrutura cloud que ejecuta inferencias sobre bancos de dados.

Ambos proporcionan bloques de construcción IA polivalentes para usos que van do projeto personal a as soluções empresariales.

### Entrenamiento e capacidades de Gemma

Según seu [**informe técnico ⧉**][01], os modelos Gemma (2B e 7B) são avanzados, entrenados sobre conjuntos de dados masivos que colocam énfasis em o contenido web, as matemáticas e a programación. Estos modelos, a diferença de seu predecesor Gemini, no priorizan as funcionalidades multilingües ou multimodales. Incorporan um vocabulario completo e emplean um novo enfoque de tokenización, mejorando a gestión de tipos de dados diversificados. Su instruction-tuning, combinando aprendizado supervisado e aprendizado por reforço a partir de retroalimentación humana, se concentra unicamente em o inglés, optimizando a comprensión e a geração de texto matizadas. Esta innovación metodológica subraya seu potencial em ámbitos especializados, ilustrando o panorama em evolução do entrenamiento de modelos de linguagem.

### Gemma e a comunidade de código aberto

Como saída de código aberto sob [**licencias permisivas ⧉**][03], Gemma representa também o compromiso de Google com uma colaboração ética em IA. Los desenvolvedores externos podem agora apoyarse em Gemma, examinarla e personalizarla de maneira transparente para democratizar o acceso e apoyar a rendición de cuentas.

![divider][divider].class=\"m-10 w-100\"

![Ollama Logo - Source: Ollama](https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/ollama.svg).class=\"fade-in w-25 p-5 float-start\"

## Integrar Google Gemma com Ollama em macOS

[**Ollama ⧉**][02] é uma interfaz que permite explorar os asistentes IA localmente em um sistema macOS. Vamos a utilizarla para configurar os modelos Gemma 2B e 7B em os computadores Apple serie M. Esta guía lo acompañará em o proceso de integração de Gemma com Ollama em macOS.

Puede utilizar o comando uname para mostrar a arquitectura do procesador. Abra Terminal e ejecute:

```bash
uname -m
```

Si a saída é `arm64`, tem um Mac serie M. Si é `x86_64`, tem um Mac Intel. Esta guía é para os Mac serie M.

### Configuración do entorno

#### 1. Asegúrese de que Python 3.8+, pip, venv estén instalados

Antes de empezar, compruebe que tem [**Python 3.8 ⧉**][04] ou mais reciente em seu Mac, assim como as ferramentas `pip` e `venv`. Puede comprobar seus versiones de Python e pip e actualizar pip com os seguintes comandos em Terminal:

```bash
python3 --version
pip3 --version
pip3 install --upgrade pip
```

#### 2. Crear um entorno virtual para aislar as dependencias

Abra Terminal e crê um entorno virtual para evitar os conflictos com os paquetes do sistema.

```bash
python3 -m venv gemma_env
source gemma_env/bin/activate
```

#### 3. Instalar a última versión de Ollama para macOS

Descargue a [**última versión de Ollama ⧉**][05] para macOS desde ou sitio oficial. Extraiga e mueva a aplicação Ollama a seu pasta Aplicaciones. Ábrala e siga as instrucciones de instalación.

#### 4. Confirmar que a instalación de Ollama foi exitosa

Compruebe que Ollama está correctamente instalado ejecutando:

```bash
ollama --version
```

Debería ver a versión de Ollama mostrada.

### Recomendaciones do sistema

Para um rendimiento óptimo de Gemma 2B, necesitará:

- **Procesador**: Intel i5 multinúcleo ou superior
- **Memoria**: 16 GB de RAM (32 GB para Gemma 7B)
- **Almacenamiento**: 50 GB de espacio libre SSD
- **macOS**: actualizado (Monterey ou posterior)

Una vez configurado Ollama, está listo para inicializar e interactuar com os modelos Gemma localmente.

![divider][divider].class=\"m-10 w-100\"

## Inicializar uma instancia Gemma local

### 1. Lanzar o modelo Gemma mediante a CLI Ollama

Elija o modelo Gemma que desea ejecutar:

- Gemma 2B (modelo mais pequeño): `ollama run gemma:2b`
- Gemma 7B (modelo mais grande): `ollama run gemma:7b`

### 2. El primer lanzamiento descargará os activos do modelo (pode llevar tempo)

El primer lanzamiento descargará o modelo Gemma seleccionado, lo que pode llevar tempo. Una vez terminado, Gemma se inicializará para seu uso.

#### Ejemplo de consulta conversacional

```bash
>>> Hello Gemma. How are you today?
```

Gemma responderá com uma resposta em lenguaje natural.

```bash
>>> Hello Gemma. How are you today?
Hello! It's a lovely day to be alive. Thank you for asking. How are you doing today? 😊
```

### Desactivar o entorno virtual

```bash
deactivate
```

Esto volverá ao entorno Python predeterminado de seu sistema.

Para obtener ayuda em caso de problema ou mais detalles sobre a configuración, consulte a [Documentación Ollama ⧉](https://ollama.com/docs) e a [Documentación Gemma ⧉](https://github.com/google-deepmind/gemma).

![divider][divider].class=\"m-10 w-100\"

## El impacto de código aberto de Gemma

Desde seu lanzamiento, Gemma tem acelerado rapidamente a innovación gracias a seu enfoque de código aberto accesible e colaborativo.

Las licencias permisivas permitem também examinar a arquitectura de Gemma com fines de investigación e aportar modificações a um nivel muito granular. Los desenvolvedores têm compartido ajustes, personalizaciones e capacidades completamente novas em as plataformas de colaboração de código.

Este esfuerzo comunitario continúa mejorando as capacidades de Gemma para construir sistemas de IA éticos e responsables, alineados com as melhores práticas emergentes.

Con o tempo, poderia emerger um ecosistema de ferramentas, integrações e aplicações enteramente novas para Gemma gracias a seu naturaleza de plataforma de código aberto.

![divider][divider].class=\"m-10 w-100\"

## Casos de uso Gemma para soluções empresariales

El modelo de IA de Google, Gemma, propone diversas soluções empresariales com seu arquitectura técnica e seu naturaleza de código aberto para responder a necessidades empresariales específicas.

### 1. Chatbots e agentes conversacionales

El modelo mais pequeño, Gemma 2B, está optimizado para a eficiência em dispositivo, lo que lo convierte em ideal para desenvolver **bots conversacionales** e **asistentes virtuales**. Las empresas podem desplegar estes agentes IA em dispositivos móveles ou sistemas embebidos para mejorar o serviço ao cliente, o soporte e o compromiso sem necessidade de recursos de cálculo extensivos.

Aunque Gemma acaba de lanzarse, seus capacidades se alinean bien com as aplicações existentes de chatbots IA e agentes virtuales que asisten a os clientes. A medida que Gemma madure, esperamos ver integrações directas que permitan interfaces conversacionales de nova geração.

### 2. Análisis de dados e insights

El modelo Gemma 7B mais grande, com seu capacidade superior para tareas complejas, está bien adaptado ao análisis de grandes conjuntos de dados e documentos. Las empresas podem aproveitar este modelo para extraer perspectivas, tendencias e patrones a partir de grandes cantidades de dados, ayudando a a tomada de decisões e a a planificación estratégica.

### 3. Creación e resumen de contenido

Los modelos Gemma podem ayudar a generar e resumir contenido: informes, artigos, materiales de marketing. Esta capacidade pode reducir significativamente o tempo e o esfuerzo requeridos para producir contenido de alta qualidade, permitiendo a as empresas concentrarse em a criatividade e a estrategia.

### 4. Email marketing personalizado e segmentación publicitaria

Comprendiendo e generando lenguaje natural, Gemma pode ayudar a as empresas a criar campañas de email marketing e estrategias de segmentación publicitaria mais personalizadas e eficaces. Este caso de uso pode conducir a um compromiso do cliente e uma tasa de conversión mejorados.

### 5. Tratamiento do lenguaje natural (NLP) para dispositivos edge

Las optimizaciones de Gemma lo fazem adecuado para a execução de tareas NLP directamente em os dispositivos edge. Esta capacidade permite a tomada de decisões empresariales em tempo real e integrações mais fluidas com o mundo real: distribución, fabricación, aplicações IoT.

### 6. Inteligencia de código para desenvolvedores

Gemma pode reforzar a produtividade de os desenvolvedores proporcionando interfaces em lenguaje natural para as tareas de edición de código e desenvolvimento. Por exemplo, os desenvolvedores podem utilizar consultas conversacionales para obtener recomendaciones de código, descripciones de funciones, ayuda ao debugging e revisiones de código. Gemma analizaría o contexto e a semántica para dar sugerencias pertinentes. Este «copiloto IA» pode ayudar a racionalizar os flujos de trabalho, reducir os errores e acelerar o desenvolvimento de productos impulsados por IA.

### 7. Aplicaciones multimodales

Con seu capacidade para tratar informação através de texto, voz e visão, Gemma é polivalente para os casos de uso multimodales. Esta funcionalidad é particularmente beneficiosa para as aplicações que requerem interacción com os usuários de maneira mais natural e intuitiva, como as experiências VR e AR.

La naturaleza de código aberto de Gemma e seu versatilidad técnica lo convierten em uma ferramenta valiosa para as empresas que buscam aproveitar a IA em seus necessidades operativas. Gemma é hábil para criar asistentes virtuales e chatbots que mejoran a experiência do cliente e pode gestionar grandes cantidades de análisis de dados. Su modelo de código aberto fomenta também a innovación e a colaboração, permitiendo a as empresas personalizar Gemma para responder a seus necessidades.

![divider][divider].class=\"m-10 w-100\"

## Qué reserva o futuro?

En o horizonte, Gemma está posicionado para um mayor crescimento e desenvolvimento. Hay esfuerzos em curso para mejorar seu compatibilidade com diversos entornos de hardware, reforzar o soporte de lenguas adicionales e ampliar seu espectro de aplicações. Google e Gemma aspiran a abordar os desafíos vinculados a a precisión, a detección de sesgos e o uso seguro de os dados, posicionando a Gemma como um líder do desenvolvimento de a IA ética.

![divider][divider].class=\"m-10 w-100\"

## Conclusión

El lanzamiento de Gemma é um momento decisivo em o campo de a IA, subrayando um giro rumo a práticas de desenvolvimento mais accesibles, éticas e colaborativas. A medida que continúe evoluindo, Gemma está llamado a desempenhar um papel pivote em a definición do futuro de a IA, ofreciendo um modelo para a maneira em que os projetos de código aberto podem estimular a innovación a a vez que respetan estándares éticos.

[00]: https://ai.google.dev/gemma "Google Gemma AI"
[01]: https://storage.googleapis.com/deepmind-media/gemma/gemma-report.pdf "Gemma Technical Report"
[02]: https://ollama.com "Ollama"
[03]: https://ai.google.dev/gemma/terms "Gemma Licensing"
[04]: https://www.python.org/downloads/release/python-380/ "Python 3.8"
[05]: https://ollama.com/download "Ollama Download"

[divider]: https://cloudcdn.pro/clients/common/images/elements/divider.svg "Divider"
