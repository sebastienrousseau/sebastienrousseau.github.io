---
title: "Racionalizar o desenvolvimento de bibliotecas Rust mediante a geração de código"
subtitle: "LibMake: um generador de código Rust que impone as buenas práticas desde ou primer día"
description: "Impulse o desenvolvimento de bibliotecas Rust com LibMake: uma ferramenta de geração de código que impone as buenas práticas e produce o código inicial, ahorrando tempo e esfuerzo."
date: "October 26, 2023"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Grandes columnas blancas"
keywords: "Rust, biblioteca, desenvolvimento, código, generador, boilerplate, buenas práticas, qualidade, fiable"
---

![Giant white pillars](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

## Perspectiva

### Desafíos do desenvolvimento de bibliotecas Rust

Desarrollar bibliotecas Rust pode ser uma tarea difícil, em particular para os principiantes. Uno de os mayores desafíos consiste em colocar em pie uma estructura de projeto eficiente e escribir tudo o código boilerplate necessário. Esto pode ser costoso em tempo e repetitivo, e desviar a atención de os aspectos mais creativos e estratégicos do desenvolvimento.

### Beneficios de utilizar um generador de código

Utilizar um generador de código pode racionalizar o proceso ao automatizar a geração de boilerplate e otras tareas repetitivas. Esto pode ahorrar a os desenvolvedores um tempo e um esfuerzo significativos, liberándolos para concentrarse em os aspectos mais importantes: diseño, implementación e pruebas.

## Idea

### LibMake: um generador de código para bibliotecas Rust

[LibMake ⧉][00] é uma ferramenta de geração de código concebida para ayudar a criar rapidamente bibliotecas Rust de alta qualidade generando um conjunto de arquivos modelados e prerrellenados. Esta ferramenta de scaffolding boilerplate «opinionada» aspira a reducir significativamente o tempo de desenvolvimento e minimizar as tareas repetitivas, permitiéndole concentrarse em seu lógica de negocio ao tempo que impone estándares, buenas práticas e coherencia, e proporciona guías de estilo para seu biblioteca.

LibMake é flexible e extensible, e pode utilizarse para criar bibliotecas de cualquier tamaño ou complexidade. También admite diversas opções de configuración, permitiendo a os desenvolvedores adaptarlo a seus necessidades específicas.

### Ejemplo de uso de LibMake

Para utilizar LibMake, os desenvolvedores devem simplesmente ejecutar o seguinte comando:

```bash
libmake \
    --author "John Smith" \
    --build "build.rs" \
    --categories "['category 1', 'category 2', 'category 3']" \
    --description "A Rust library for doing cool things" \
    --documentation "https://docs.rs/my_library" \
    --edition "2021" \
    --email "john.smith@example.com" \
    --homepage "https://my_library.rs" \
    --keywords "['rust', 'library', 'cool']" \
    --license "MIT" \
    --name "my_library" \
    --output "my_library" \
    --readme "README.md" \
    --repository "https://github.com/example/my_library" \
    --rustversion "1.69.0" \
    --version "0.1.0" \
    --website "https://example.com/john-smith"
```

Esto creará um novo directorio para a biblioteca, e LibMake generará o código boilerplate necessário e a estructura de documentación. Los desenvolvedores podrán então añadir seu próprio código a a biblioteca e comenzar a desenvolver.

## Impacto

### Tiempo e esfuerzo de desenvolvimento reducidos

LibMake reduce o tempo e o esfuerzo requeridos para desenvolver bibliotecas Rust automatizando a geração de código e otras tareas. Esto faz ganar tempo a os desenvolvedores. Pueden concentrarse em as partes importantes: diseño, implementación e pruebas.

### Calidad e confiabilidade mejoradas

LibMake pode da mesma forma ayudar a os desenvolvedores a mejorar a qualidade e confiabilidade de seus bibliotecas proporcionando plantillas predefinidas que seguem as buenas práticas. Esto pode ayudar a reducir o número de errores e fallos em as bibliotecas, e hacerlas mais robustas e fiables.

## Incentivos

### Imponer as buenas práticas e generar o código inicial

LibMake pode ayudar a os desenvolvedores a imponer as buenas práticas proporcionando plantillas predefinidas que seguem essas práticas. También pode generar código inicial para as funcionalidades comunes de biblioteca, lo que pode ahorrar um tempo significativo.

LibMake oferece as seguintes funcionalidades e beneficios:

- Cree seu biblioteca Rust facilmente desde a linha de comandos ou proporcionando um arquivo de configuración em formato CSV, JSON, TOML ou YAML.
- Genere rapidamente novos projetos de biblioteca com uma estructura predefinida e código boilerplate que pode personalizar com seu própria plantilla.
- Genere um workflow GitHub Actions predefinido para ayudar a automatizar o desenvolvimento e as pruebas de seu biblioteca.
- Genere automaticamente funciones, métodos e macros básicos para empezar.
- Imponga buenas práticas e estándares mediante documentación de partida, suites de pruebas e benchmarks diseñados para ponerle em marcha rapidamente.

Con LibMake, pode generar facilmente uma nova estructura de código Rust com todos os arquivos, layouts, configuraciones de build, código, pruebas, benchmarks, documentación e muito mais, em questão de segundos.

### Pruebe LibMake hoje

Si é desenvolvedor, le animo a probar [LibMake ⧉][00] para ver cómo pode racionalizar seu proceso de desenvolvimento. LibMake é gratuito e de código aberto, e está disponible para seu descarga desde ou [repositorio GitHub ⧉][00].

[00]: https://github.com/sebastienrousseau/libmake "LibMake: A code generator to reduce repetitive tasks and build high-quality Rust libraries"
