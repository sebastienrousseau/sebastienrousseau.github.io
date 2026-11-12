---
title: "LibMake: generátor lešení pro knihovny v Rustu"
subtitle: "LibMake: generátor kódu v Rustu, který od prvního dne vynucuje osvědčené postupy"
description: "LibMake je nástroj CLI v Rustu, který z jediného příkazu nebo verzovaného konfiguračního souboru TOML/YAML vygeneruje kompletní lešení knihovny: Cargo.toml, src/lib.rs se šablonami dokumentace, testovací a benchmarkové sady a CI v GitHub Actions."
date: "October 26, 2023"
language: "cs-CZ"
locale: "cs_CZ"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Obří bílé sloupy"
keywords: "LibMake, generátor kódu v Rustu, lešení cargo, šablona knihovny v Rustu, šablonování Tera, GitHub Actions pro Rust, cargo-audit, Rust API Guidelines, generátor standardního kódu, pracovní postup CI v Rustu"
---


[**LibMake ⧉**][00] je open-source CLI a knihovna v Rustu, která z jediného vyvolání vygeneruje kompletní lešení projektu knihovny. Zaměřuje se na mezeru mezi `cargo new --lib` (které vytvoří pouze minimální Cargo.toml a src/lib.rs) a nastavením knihovny připraveným pro produkci (které vyžaduje ruční doplnění dokumentačních komentářů, CI, testovacích sad, struktury benchmarků, souboru CONTRIBUTING.md a licenčních souborů).

Tento článek popisuje, co LibMake generuje, jak fungují režimy konfiguračního souboru a CLI, strukturu generovaného CI a systém šablonování.

## Instalace a základní použití

LibMake je publikován na [crates.io](https://crates.io/crates/libmake) a instaluje se přes Cargo:

```bash
cargo install libmake
```

Minimální vyvolání CLI vygeneruje pojmenovanou knihovnu v aktuálním adresáři:

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

Mezi další volitelné přepínače patří `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme` a `--build`.

## Režim konfiguračního souboru

Pro týmové použití lze všechny přepínače CLI vyjádřit v konfiguračním souboru TOML:

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

Vyvolá se takto:

```bash
libmake --config libmake.toml
```

LibMake přijímá také konfigurační formáty JSON, YAML a CSV prostřednictvím přepínačů `--config-json`, `--config-yaml` a `--config-csv`. Zařazení souboru `libmake.toml` do kořene repozitáře poskytne každému přispěvateli reprodukovatelný výchozí stav lešení a změny v konfiguraci šablon jsou viditelné v Git diffech.

## Struktura generovaného projektu

Vyvolání LibMake vytvoří následující rozvržení:

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

Generovaný `src/lib.rs` obsahuje dokumentační komentář na úrovni crate, `#![deny(missing_docs)]`, `#![doc = include_str!("../README.md")]` pro zahrnutí souboru README do rustdoc a veřejný typ jako zárodek s přidruženým dokumentačním komentářem. Tyto volby odpovídají požadavku Rust API Guidelines, aby všechny veřejné položky měly dokumentaci.

Generovaný `benches/lib_benchmarks.rs` používá [Criterion.rs](https://github.com/bheisler/criterion.rs) a vyžaduje přidání `criterion` jako vývojové závislosti, kterou LibMake automaticky vloží do `Cargo.toml`.

## Pracovní postup CI v GitHub Actions

Generovaný `.github/workflows/release.yml` spouští při každém pushi a pull requestu pět úloh:

| Úloha | Toolchain | Co kontroluje |
|---|---|---|
| `test` | stable, beta, nightly (matrix) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (cargo-audit se instaluje v úloze) |
| `doc` | stable | `cargo doc --no-deps` (selže při chybějící dokumentaci) |

Úloha nightly má `continue-on-error: true`, takže regrese v nightly neblokuje slučování, a přesto se selhání v běhu pracovního postupu zobrazí.

## Šablonování pomocí Tera

LibMake používá šablonovací engine [Tera](https://keats.github.io/tera/), syntaxi podobnou Jinja2 pro Rust, k vykreslení všech generovaných souborů. Každá šablona dostává jako kontext celou konfigurační strukturu:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

Vlastní adresáře se šablonami jsou podporovány přes přepínač `--template`:

```bash
libmake --config libmake.toml --template ./my_templates/
```

Vlastní adresář musí zrcadlit výchozí strukturu šablon (stejné názvy souborů). Jakýkoli soubor přítomný ve vlastním adresáři přepíše odpovídající vestavěnou šablonu; soubory, které ve vlastním adresáři chybí, se vrátí k vestavěné verzi. To umožňuje částečné přepisy, například nahrazení pouze šablony pracovního postupu CI při zachování výchozích šablon src/lib.rs a Cargo.toml.

## Často kladené otázky

**Čím se LibMake liší od `cargo new --lib`?**
`cargo new --lib` vytvoří minimální projekt pouze se soubory `Cargo.toml` a `src/lib.rs` (obsahující jediný blok `#[cfg(test)]`). LibMake vygeneruje úplnou strukturu: integrační testy, benchmarky, CI, CONTRIBUTING.md, soubory s duální licencí a řádně zdokumentovaný src/lib.rs, nakonfigurovanou se skutečnými metadaty projektu namísto zástupných hodnot.

**Lze LibMake použít s existujícím pracovním prostorem Cargo?**
LibMake generuje samostatný adresář crate. Chcete-li generovaný crate přidat do existujícího pracovního prostoru, přidejte výstupní cestu do pole `members` pracovního prostoru v kořenovém `Cargo.toml`. LibMake neupravuje existující soubory pracovního prostoru.

**Mohu aktualizovat šablony lešení po počátečním vygenerování?**
LibMake generuje soubory jednorázově; dříve vygenerované projekty nesleduje ani neaktualizuje. Pro převzetí aktualizovaných šablon je doporučeným postupem znovu spustit LibMake do dočasného adresáře, výsledek porovnat (diff) s existujícím crate a požadované změny uplatnit výběrově.

**Které edice Rustu a hodnoty MSRV LibMake podporuje?**
LibMake přijímá pro `--edition` a `--rustversion` jakýkoli řetězec a zapisuje hodnoty přímo do `Cargo.toml`. Neověřuje, zda je zadaná edice nebo MSRV skutečnou verzí Rustu, takže za dodání správných hodnot odpovídá volající.

## Reference

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake: generátor lešení knihoven pro Rust"
