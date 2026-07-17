---
title: "LibMake: scaffold-generator för Rust-bibliotek"
subtitle: "LibMake: en Rust-kodgenerator som upprätthåller bästa praxis från dag ett."
description: "LibMake är ett Rust-CLI-verktyg som genererar en komplett biblioteksstruktur (Cargo.toml, src/lib.rs med dokumentationsmallar, test- och benchmarkramverk samt GitHub Actions-CI) från ett enda kommando eller en versionshanterad TOML/YAML-konfigurationsfil."
date: "October 26, 2023"
language: "sv-SE"
locale: "sv_SE"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Gigantiska vita pelare"
keywords: "LibMake, Rust-kodgenerator, cargo-scaffold, Rust-biblioteksmall, Tera-mallar, GitHub Actions Rust, cargo-audit, Rust API Guidelines, boilerplate-generator, Rust-CI-arbetsflöde"
---

![Gigantiska vita pelare](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

[**LibMake ⧉**][00] är ett Rust-CLI och bibliotek med öppen källkod som genererar en komplett projektstruktur för bibliotek från ett enda anrop. Verktyget riktar sig mot gapet mellan `cargo new --lib` (som endast skapar en minimal Cargo.toml och src/lib.rs) och en produktionsfärdig bibliotekskonfiguration (som kräver att man manuellt lägger till dokumentationskommentarer, CI, testramverk, benchmarkstruktur, CONTRIBUTING.md och licensfiler).

Denna artikel beskriver vad LibMake genererar, hur konfigurationsfils- och CLI-lägena fungerar, den genererade CI-strukturen samt mallsystemet.

## Installation och grundläggande användning

LibMake publiceras på [crates.io](https://crates.io/crates/libmake) och installeras via Cargo:

```bash
cargo install libmake
```

Det minimala CLI-anropet genererar ett namngivet bibliotek i den aktuella katalogen:

```bash
libmake \
  --author "Jane Smith" \
  --email "jane@example.com" \
  --name "my_library" \
  --description "A Rust library for doing useful things" \
  --version "0.1.0" \
  --licence "MIT OR Apache-2.0" \
  --repository "https://github.com/example/my_library" \
  --rustversion "1.70.0" \
  --edition "2021" \
  --output "my_library"
```

Ytterligare valfria flaggor inkluderar `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme` och `--build`.

## Konfigurationsfilsläge

För teamanvändning kan alla CLI-flaggor uttryckas i en TOML-konfigurationsfil:

```toml
# libmake.toml


author      = "Jane Smith"
email       = "jane@example.com"
name        = "my_library"
description = "A Rust library for doing useful things"
version     = "0.1.0"
licence     = "MIT OR Apache-2.0"
repository  = "https://github.com/example/my_library"
rustversion = "1.70.0"
edition     = "2021"
output      = "my_library"
categories  = ["algorithms", "data-structures"]
keywords    = ["rust", "library"]
```

Anropas som:

```bash
libmake --config libmake.toml
```

LibMake accepterar även konfigurationsformaten JSON, YAML och CSV via flaggorna `--config-json`, `--config-yaml` respektive `--config-csv`. Att checka in `libmake.toml` i repositoriets rot ger varje bidragsgivare en reproducerbar baslinje för strukturen, och ändringar i mallkonfigurationen syns i Git-diffar.

## Genererad projektstruktur

Ett LibMake-anrop skapar följande layout:

```
my_library/
├── .github/
│   └── workflows/
│       └── release.yml     # full CI matrix
├── benches/
│   └── lib_benchmarks.rs   # Criterion benchmark stub
├── src/
│   └── lib.rs              # doc-commented, deny(missing_docs)
├── tests/
│   └── lib_tests.rs        # integration test stub
├── CONTRIBUTING.md
├── Cargo.toml              # complete metadata
├── LICENSE-APACHE
├── LICENSE-MIT
└── README.md
```

Den genererade `src/lib.rs` innehåller en dokumentationskommentar på crate-nivå, `#![deny(missing_docs)]`, `#![doc = include_str!("../README.md")]` för att inkludera README-filen i rustdoc, samt en publik stubbtyp med tillhörande dokumentationskommentar. Dessa val följer kravet i Rust API Guidelines på att alla publika objekt ska ha dokumentation.

Den genererade `benches/lib_benchmarks.rs` använder [Criterion.rs](https://github.com/bheisler/criterion.rs) och kräver att `criterion` läggs till som dev-dependency, vilket LibMake infogar i `Cargo.toml` automatiskt.

## CI-arbetsflöde med GitHub Actions

Den genererade `.github/workflows/release.yml` kör fem jobb vid varje push och pull request:

| Jobb | Verktygskedja | Vad som kontrolleras |
|---|---|---|
| `test` | stable, beta, nightly (matris) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (cargo-audit installeras i jobbet) |
| `doc` | stable | `cargo doc --no-deps` (misslyckas vid saknad dokumentation) |

Nightly-jobbet har `continue-on-error: true` så att en nightly-regression inte blockerar sammanslagningar, samtidigt som felet fortfarande syns i arbetsflödeskörningen.

## Mallhantering med Tera

LibMake använder mallmotorn [Tera](https://keats.github.io/tera/), en Jinja2-liknande syntax för Rust, för att rendera alla genererade filer. Varje mall tar emot hela konfigurationsstrukturen som kontext:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

Anpassade mallkataloger stöds via flaggan `--template`:

```bash
libmake --config libmake.toml --template ./my_templates/
```

Den anpassade katalogen måste spegla standardmallstrukturen (samma filnamn). Varje fil som finns i den anpassade katalogen åsidosätter motsvarande inbyggda mall; filer som inte finns i den anpassade katalogen faller tillbaka på den inbyggda versionen. Detta möjliggör partiella åsidosättanden, till exempel att endast ersätta CI-arbetsflödesmallen medan standardmallarna för src/lib.rs och Cargo.toml behålls.

## Vanliga frågor

**Hur skiljer sig LibMake från `cargo new --lib`?**
`cargo new --lib` skapar ett minimalt projekt med endast `Cargo.toml` och `src/lib.rs` (som innehåller ett enda `#[cfg(test)]`-block). LibMake genererar hela strukturen (integrationstester, benchmarks, CI, CONTRIBUTING.md, dubbla licensfiler och en korrekt dokumenterad src/lib.rs), konfigurerad med projektets faktiska metadata i stället för platshållare.

**Kan LibMake användas med ett befintligt Cargo-workspace?**
LibMake genererar en fristående crate-katalog. För att lägga till den genererade craten i ett befintligt workspace lägger man till utdatasökvägen i arrayen `members` i rotens `Cargo.toml`. LibMake ändrar inte befintliga workspace-filer.

**Kan jag uppdatera strukturmallarna efter den första genereringen?**
LibMake genererar filer en gång; verktyget spårar eller uppdaterar inte tidigare genererade projekt. För att ta till sig uppdaterade mallar är det rekommenderade tillvägagångssättet att köra LibMake på nytt i en temporär katalog och jämföra resultatet med den befintliga craten, och därefter selektivt tillämpa önskade ändringar.

**Vilka Rust-utgåvor och MSRV-värden stöder LibMake?**
LibMake accepterar valfri sträng för `--edition` och `--rustversion` och skriver värdena direkt till `Cargo.toml`. Verktyget validerar inte om den angivna utgåvan eller MSRV-värdet är en verklig Rust-version, så anroparen ansvarar för att ange korrekta värden.

## Referenser

1. Rousseau, S. *LibMake: A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera: A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake: scaffold-generator för Rust-bibliotek"
