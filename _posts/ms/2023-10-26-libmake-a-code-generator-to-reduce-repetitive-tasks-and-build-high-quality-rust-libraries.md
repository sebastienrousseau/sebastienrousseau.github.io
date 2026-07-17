---
title: "LibMake: Penjana Rangka Pustaka Rust"
tags: "LibMake, RustCodeGenerator, CargoScaffold, RustLibraryTemplate, TeraTemplating, GitHubActionsRust, CargoAudit, RustAPIGuidelines, BoilerplateGenerator, RustCI, ISO 20022, post-quantum cryptography, AI, Rust, open source"
subtitle: "LibMake: penjana kod Rust yang menguatkuasakan amalan terbaik dari hari pertama."
description: "LibMake ialah alat CLI Rust yang menjana rangka pustaka lengkap - Cargo.toml, src/lib.rs dengan templat dokumentasi, rangka kerja ujian dan penanda aras, serta CI GitHub Actions - daripada satu arahan tunggal atau fail konfigurasi TOML/YAML berversi."
date: "Oct 26, 2023"
language: "ms"
locale: "ms_MY"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Tiang-tiang putih gergasi"
keywords: "LibMake, penjana kod Rust, rangka cargo, templat pustaka Rust, templat Tera, GitHub Actions Rust, cargo-audit, Garis Panduan API Rust, penjana boilerplate, aliran kerja CI Rust"
---

[**LibMake ⧉**][00] ialah CLI dan pustaka Rust sumber terbuka yang menjana rangka projek pustaka lengkap daripada satu seruan tunggal. Ia menyasarkan jurang antara `cargo new --lib` (yang hanya mencipta Cargo.toml dan src/lib.rs yang minimum) dengan penyediaan pustaka sedia pengeluaran (yang memerlukan penambahan manual komen dokumentasi, CI, rangka kerja ujian, struktur penanda aras, CONTRIBUTING.md, dan fail lesen).

Artikel ini menerangkan apa yang dijana oleh LibMake, cara mod fail konfigurasi dan mod CLI berfungsi, struktur CI yang dijana, dan sistem templat.

## Pemasangan dan Penggunaan Asas

LibMake diterbitkan di [crates.io](https://crates.io/crates/libmake) dan dipasang melalui Cargo:

```bash
cargo install libmake
```

Seruan CLI yang minimum menjana pustaka bernama dalam direktori semasa:

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

Bendera pilihan tambahan termasuk `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme`, dan `--build`.

## Mod Fail Konfigurasi

Untuk kegunaan pasukan, semua bendera CLI boleh dinyatakan dalam fail konfigurasi TOML:

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

Diseru sebagai:

```bash
libmake --config libmake.toml
```

LibMake juga menerima format konfigurasi JSON, YAML, dan CSV melalui bendera `--config-json`, `--config-yaml`, dan `--config-csv` masing-masing. Melakukan commit `libmake.toml` ke akar repositori memberi setiap penyumbang satu garis dasar rangka yang boleh dihasilkan semula, dan perubahan pada konfigurasi templat dapat dilihat dalam Git diff.

## Struktur Projek yang Dijana

Satu seruan LibMake mencipta susun atur berikut:

```
my_library/
├── .github/
│   └── workflows/
│       └── release.yml     # matriks CI penuh
├── benches/
│   └── lib_benchmarks.rs   # stub penanda aras Criterion
├── src/
│   └── lib.rs              # berkomen dokumentasi, deny(missing_docs)
├── tests/
│   └── lib_tests.rs        # stub ujian penyepaduan
├── CONTRIBUTING.md
├── Cargo.toml              # metadata lengkap
├── LICENSE-APACHE
├── LICENSE-MIT
└── README.md
```

Fail `src/lib.rs` yang dijana merangkumi komen dokumentasi peringkat crate, `#![deny(missing_docs)]`, `#![doc = include_str!("../README.md")]` untuk menarik README ke dalam rustdoc, serta satu jenis awam stub dengan komen dokumentasi yang berkaitan. Pilihan-pilihan ini mematuhi keperluan Garis Panduan API Rust bahawa semua item awam mesti mempunyai dokumentasi.

Fail `benches/lib_benchmarks.rs` yang dijana menggunakan [Criterion.rs](https://github.com/bheisler/criterion.rs) dan memerlukan penambahan `criterion` sebagai kebergantungan pembangunan (dev-dependency), yang dimasukkan oleh LibMake ke dalam `Cargo.toml` secara automatik.

## Aliran Kerja CI GitHub Actions

Fail `.github/workflows/release.yml` yang dijana menjalankan lima tugas pada setiap push dan pull request:

| Tugas | Rantai alat | Apa yang disemak |
|---|---|---|
| `test` | stabil, beta, nightly (matriks) | `cargo test --all-features` |
| `clippy` | stabil | `cargo clippy -- -D warnings` |
| `fmt` | stabil | `cargo fmt --check` |
| `audit` | stabil | `cargo audit` (cargo-audit dipasang dalam tugas) |
| `doc` | stabil | `cargo doc --no-deps` (gagal jika dokumentasi hilang) |

Tugas nightly mempunyai `continue-on-error: true` supaya regresi nightly tidak menghalang penggabungan (merge), sambil tetap menyerlahkan kegagalan tersebut dalam larian aliran kerja.

## Templat dengan Tera

LibMake menggunakan enjin templat [Tera](https://keats.github.io/tera/) — sintaks serupa Jinja2 untuk Rust — bagi memaparkan semua fail yang dijana. Setiap templat menerima keseluruhan struct konfigurasi sebagai konteks:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

Direktori templat tersuai disokong melalui bendera `--template`:

```bash
libmake --config libmake.toml --template ./my_templates/
```

Direktori tersuai mesti mencerminkan struktur templat lalai (nama fail yang sama). Mana-mana fail yang hadir dalam direktori tersuai akan mengatasi templat terbina dalam yang sepadan; fail yang tiada dalam direktori tersuai akan kembali kepada versi terbina dalam. Ini membolehkan pengatasan separa — sebagai contoh, menggantikan hanya templat aliran kerja CI sambil mengekalkan templat src/lib.rs dan Cargo.toml lalai.

## Soalan Lazim

**Bagaimana LibMake berbeza daripada `cargo new --lib`?**
`cargo new --lib` mencipta projek minimum dengan hanya `Cargo.toml` dan `src/lib.rs` (yang mengandungi satu blok `#[cfg(test)]` sahaja). LibMake menjana struktur penuh — ujian penyepaduan, penanda aras, CI, CONTRIBUTING.md, fail lesen berkembar, dan src/lib.rs yang didokumentasikan dengan betul — yang dikonfigurasikan dengan metadata sebenar projek dan bukannya ruang letak.

**Bolehkah LibMake digunakan dengan ruang kerja (workspace) Cargo yang sedia ada?**
LibMake menjana direktori crate berdiri sendiri. Untuk menambah crate yang dijana ke ruang kerja sedia ada, tambahkan laluan output ke dalam tatasusunan `members` ruang kerja dalam `Cargo.toml` akar. LibMake tidak mengubah suai fail ruang kerja yang sedia ada.

**Bolehkah saya mengemas kini templat rangka selepas penjanaan awal?**
LibMake menjana fail sekali sahaja; ia tidak menjejak atau mengemas kini projek yang telah dijana sebelum ini. Untuk menerima pakai templat yang dikemas kini, pendekatan yang disyorkan adalah menjalankan semula LibMake ke dalam direktori sementara dan membandingkan (diff) hasilnya dengan crate sedia ada, lalu menggunakan perubahan yang diingini secara terpilih.

**Edisi Rust dan nilai MSRV apakah yang disokong oleh LibMake?**
LibMake menerima sebarang rentetan untuk `--edition` dan `--rustversion` serta menulis nilai tersebut terus ke `Cargo.toml`. Ia tidak mengesahkan sama ada edisi atau MSRV yang dinyatakan itu merupakan versi Rust yang sebenar, jadi pemanggil bertanggungjawab untuk membekalkan nilai yang betul.

## Rujukan

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Penjana rangka pustaka Rust"
