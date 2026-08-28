---
title: "LibMake: Rust könyvtárváz-generátor"
tags: "LibMake, RustCodeGenerator, CargoScaffold, RustLibraryTemplate, TeraTemplating, GitHubActionsRust, CargoAudit, RustAPIGuidelines, BoilerplateGenerator, RustCI, ISO 20022, post-quantum cryptography, AI, Rust, open source"
subtitle: "LibMake: Rust kódgenerátor, amely az első naptól kezdve érvényesíti a legjobb gyakorlatokat."
description: "A LibMake egy Rust CLI-eszköz, amely egyetlen parancsból vagy egy verziózott TOML/YAML konfigurációs fájlból teljes könyvtárvázat generál: Cargo.toml, dokumentációs sablonokkal ellátott src/lib.rs, teszt- és benchmarkkeretek, valamint GitHub Actions CI."
date: "Oct 26, 2023"
language: "hu"
locale: "hu_HU"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Óriási fehér oszlopok"
keywords: "LibMake, Rust kódgenerátor, cargo váz, Rust könyvtársablon, Tera sablonozás, GitHub Actions Rust, cargo-audit, Rust API Guidelines, sablonkód-generátor, Rust CI munkafolyamat"
---

A [**LibMake ⧉**][00] egy nyílt forráskódú Rust CLI és könyvtár, amely egyetlen hívásból teljes könyvtárprojekt-vázat generál. A `cargo new --lib` (amely csak egy minimális Cargo.toml és src/lib.rs fájlt hoz létre) és egy éles használatra kész könyvtárbeállítás (amelyhez kézzel kell hozzáadni a dokumentációs megjegyzéseket, a CI-t, a tesztkereteket, a benchmarkstruktúrát, a CONTRIBUTING.md fájlt és a licencfájlokat) közötti rést célozza meg.

Ez a cikk leírja, hogy mit generál a LibMake, hogyan működik a konfigurációsfájl- és a CLI-mód, milyen a generált CI-struktúra, valamint a sablonozási rendszert.

## Telepítés és alapvető használat

A LibMake a [crates.io](https://crates.io/crates/libmake) oldalon jelenik meg, és a Cargón keresztül telepíthető:

```bash
cargo install libmake
```

A minimális CLI-hívás egy megnevezett könyvtárat generál az aktuális könyvtárban:

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

A további opcionális kapcsolók közé tartozik a `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme` és `--build`.

## Konfigurációsfájl-mód

Csapatmunkához minden CLI-kapcsoló kifejezhető egy TOML konfigurációs fájlban:

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

A hívás módja:

```bash
libmake --config libmake.toml
```

A LibMake JSON, YAML és CSV konfigurációs formátumokat is elfogad a `--config-json`, `--config-yaml`, illetve `--config-csv` kapcsolókon keresztül. A `libmake.toml` fájl beküldése a tároló gyökerébe minden közreműködőnek reprodukálható vázalapot biztosít, a sablonkonfiguráció változásai pedig láthatóak a Git-diffekben.

## A generált projektstruktúra

Egy LibMake-hívás a következő elrendezést hozza létre:

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

A generált `src/lib.rs` tartalmaz egy crate szintű dokumentációs megjegyzést, a `#![deny(missing_docs)]` és a `#![doc = include_str!("../README.md")]` direktívát, amely a README-t behúzza a rustdocba, valamint egy nyilvános típusvázat a hozzá tartozó dokumentációs megjegyzéssel. Ezek a döntések a Rust API Guidelines azon követelményét követik, hogy minden nyilvános elemnek rendelkeznie kell dokumentációval.

A generált `benches/lib_benchmarks.rs` a [Criterion.rs](https://github.com/bheisler/criterion.rs) csomagot használja, és megköveteli a `criterion` fejlesztési függőségként való hozzáadását, amelyet a LibMake automatikusan beszúr a `Cargo.toml` fájlba.

## GitHub Actions CI munkafolyamat

A generált `.github/workflows/release.yml` minden push és pull request esetén öt feladatot futtat:

| Feladat | Eszközlánc | Mit ellenőriz |
|---|---|---|
| `test` | stable, beta, nightly (mátrix) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (a cargo-audit a feladatban települ) |
| `doc` | stable | `cargo doc --no-deps` (hiányzó dokumentáció esetén hibázik) |

A nightly feladatnál `continue-on-error: true` van beállítva, így egy nightly regresszió nem blokkolja a merge-öket, miközben a hiba továbbra is megjelenik a munkafolyamat futásában.

## Sablonozás Terával

A LibMake a [Tera](https://keats.github.io/tera/) sablonmotort használja, amely egy Jinja2-höz hasonló szintaxis Rusthoz, az összes generált fájl előállításához. Minden sablon a teljes konfigurációs struktúrát kapja meg kontextusként:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

Az egyéni sablonkönyvtárak a `--template` kapcsolón keresztül támogatottak:

```bash
libmake --config libmake.toml --template ./my_templates/
```

Az egyéni könyvtárnak tükröznie kell az alapértelmezett sablonstruktúrát (ugyanazokat a fájlneveket). Az egyéni könyvtárban jelen lévő bármely fájl felülírja a megfelelő beépített sablont; a nem jelen lévő fájlok visszaesnek a beépített változatra. Ez lehetővé teszi a részleges felülírásokat, például csak a CI munkafolyamat sablonjának cseréjét, miközben az alapértelmezett src/lib.rs és Cargo.toml sablonok megmaradnak.

## Gyakran ismételt kérdések

**Miben különbözik a LibMake a `cargo new --lib` parancstól?**
A `cargo new --lib` egy minimális projektet hoz létre, amely csak a `Cargo.toml` és a `src/lib.rs` fájlt tartalmazza (utóbbiban egyetlen `#[cfg(test)]` blokkal). A LibMake a teljes struktúrát generálja: integrációs teszteket, benchmarkokat, CI-t, CONTRIBUTING.md fájlt, kettős licencfájlokat és egy megfelelően dokumentált src/lib.rs fájlt, mindezt a projekt tényleges metaadataival konfigurálva, helykitöltők helyett.

**Használható a LibMake meglévő Cargo-munkaterülettel?**
A LibMake egy önálló crate könyvtárat generál. A generált crate hozzáadásához egy meglévő munkaterülethez add hozzá a kimeneti útvonalat a gyökér `Cargo.toml` fájlban lévő munkaterületi `members` tömbhöz. A LibMake nem módosítja a meglévő munkaterületi fájlokat.

**Frissíthetem a vázsablonokat a kezdeti generálás után?**
A LibMake a fájlokat egyszer generálja; nem követi nyomon és nem frissíti a korábban generált projekteket. A frissített sablonok átvételéhez az ajánlott megközelítés a LibMake újrafuttatása egy ideiglenes könyvtárba, majd az eredmény összehasonlítása a meglévő crate-tel, a kívánt módosításokat szelektíven alkalmazva.

**Milyen Rust-kiadásokat és MSRV-értékeket támogat a LibMake?**
A LibMake bármely karakterláncot elfogad az `--edition` és `--rustversion` kapcsolókhoz, és az értékeket közvetlenül a `Cargo.toml` fájlba írja. Nem ellenőrzi, hogy a megadott kiadás vagy MSRV valós Rust-verzió-e, ezért a hívók felelősek a helyes értékek megadásáért.

## Hivatkozások

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Rust könyvtárváz-generátor"

