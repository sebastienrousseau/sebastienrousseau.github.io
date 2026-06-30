---
title: "LibMake: Generator Scaffold Pustaka Rust"
subtitle: "LibMake: pembuat kode Rust yang menerapkan praktik terbaik sejak hari pertama."
description: "LibMake adalah alat CLI Rust yang menghasilkan scaffold pustaka lengkap - Cargo.toml, src/lib.rs dengan template dokumentasi, harness pengujian dan benchmark, serta CI GitHub Actions - dari satu perintah atau file konfigurasi TOML/YAML berversi."
date: "Oct 26, 2023"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Pilar-pilar putih raksasa"
keywords: "LibMake, generator kode Rust, scaffold cargo, template pustaka Rust, templating Tera, GitHub Actions Rust, cargo-audit, Rust API Guidelines, generator boilerplate, workflow CI Rust"
---

![Pilar-pilar putih raksasa](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

<!-- lead-start -->
<aside class="post-lead" aria-label="Ringkasan artikel">
<p class="post-lead-tldr"><strong>TL;DR.</strong> LibMake adalah alat CLI Rust yang menghasilkan scaffold pustaka lengkap - Cargo.toml, src/lib.rs dengan template dokumentasi, harness pengujian dan benchmark, serta CI GitHub Actions - dari satu perintah atau file konfigurasi TOML/YAML berversi.</p>
<p class="post-lead-heading"><strong>Kesimpulan utama</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Instalasi dan penggunaan dasar.</strong> LibMake diterbitkan di crates.io dan dipasang melalui Cargo.</li>
  <li><strong>Mode file konfigurasi.</strong> Untuk penggunaan tim, semua flag CLI dapat dinyatakan dalam file konfigurasi TOML.</li>
  <li><strong>Struktur proyek yang dihasilkan.</strong> Satu pemanggilan LibMake membuat layout pustaka Rust yang siap dikembangkan.</li>
  <li><strong>Workflow CI GitHub Actions.</strong> File .github/workflows/release.yml yang dihasilkan menjalankan lima job pada setiap push dan pull request.</li>
</ul>
</aside>
<!-- lead-end -->

[**LibMake ⧉**][00] adalah CLI dan pustaka Rust sumber terbuka yang menghasilkan scaffold proyek pustaka lengkap dari satu pemanggilan. Alat ini mengisi celah antara `cargo new --lib`, yang hanya membuat Cargo.toml dan src/lib.rs minimal, dan setup pustaka siap produksi, yang biasanya membutuhkan penambahan manual berupa komentar dokumentasi, CI, harness pengujian, struktur benchmark, CONTRIBUTING.md, dan file lisensi.

Artikel ini menjelaskan apa yang dihasilkan LibMake, bagaimana mode file konfigurasi dan CLI bekerja, struktur CI yang dihasilkan, serta sistem templating-nya.

## Instalasi dan Penggunaan Dasar

LibMake diterbitkan di [crates.io](https://crates.io/crates/libmake) dan dipasang melalui Cargo:

```bash
cargo install libmake
```

Pemanggilan CLI minimal menghasilkan pustaka bernama di direktori saat ini:

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

Flag opsional tambahan mencakup `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme`, dan `--build`.

## Mode File Konfigurasi

Untuk penggunaan tim, semua flag CLI dapat dinyatakan dalam file konfigurasi TOML:

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

Dijalankan sebagai:

```bash
libmake --config libmake.toml
```

LibMake juga menerima format konfigurasi JSON, YAML, dan CSV melalui flag `--config-json`, `--config-yaml`, dan `--config-csv`. Menyimpan `libmake.toml` di root repositori memberi setiap kontributor baseline scaffold yang dapat direproduksi, dan perubahan pada konfigurasi template terlihat jelas dalam diff Git.

## Struktur Proyek yang Dihasilkan

Satu pemanggilan LibMake membuat layout berikut:

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

File `src/lib.rs` yang dihasilkan mencakup komentar dokumentasi tingkat crate, `#![deny(missing_docs)]`, `#![doc = include_str!("../README.md")]` untuk menarik README ke rustdoc, serta tipe publik stub dengan komentar dokumentasi terkait. Pilihan ini mengikuti Rust API Guidelines yang mewajibkan semua item publik memiliki dokumentasi.

File `benches/lib_benchmarks.rs` yang dihasilkan menggunakan [Criterion.rs](https://github.com/bheisler/criterion.rs) dan membutuhkan `criterion` sebagai dev-dependency, yang otomatis dimasukkan LibMake ke `Cargo.toml`.

## Workflow CI GitHub Actions

File `.github/workflows/release.yml` yang dihasilkan menjalankan lima job pada setiap push dan pull request:

| Job | Toolchain | Yang diperiksa |
|---|---|---|
| `test` | stable, beta, nightly (matrix) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (cargo-audit dipasang di job) |
| `doc` | stable | `cargo doc --no-deps` (gagal jika dokumentasi hilang) |

Job nightly memiliki `continue-on-error: true`, sehingga regresi nightly tidak memblokir merge, tetapi tetap terlihat di workflow run.

## Templating dengan Tera

LibMake menggunakan engine template [Tera](https://keats.github.io/tera/) - sintaks mirip Jinja2 untuk Rust - untuk merender semua file yang dihasilkan. Setiap template menerima struct konfigurasi penuh sebagai konteks:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

Direktori template khusus didukung melalui flag `--template`:

```bash
libmake --config libmake.toml --template ./my_templates/
```

Direktori khusus harus mencerminkan struktur template default dengan nama file yang sama. Setiap file yang ada di direktori khusus menggantikan template bawaan terkait; file yang tidak ada akan memakai versi bawaan. Ini memungkinkan override parsial, misalnya hanya mengganti template workflow CI sambil tetap memakai template default untuk src/lib.rs dan Cargo.toml.

## Pertanyaan yang Sering Diajukan

**Apa perbedaan LibMake dengan `cargo new --lib`?**

`cargo new --lib` membuat proyek minimal hanya dengan `Cargo.toml` dan `src/lib.rs` yang berisi satu blok `#[cfg(test)]`. LibMake menghasilkan struktur penuh: integration tests, benchmarks, CI, CONTRIBUTING.md, file dual-licence, dan `src/lib.rs` yang terdokumentasi dengan benar, dikonfigurasi menggunakan metadata proyek yang sebenarnya, bukan placeholder.

**Bisakah LibMake digunakan dengan workspace Cargo yang sudah ada?**

LibMake menghasilkan direktori crate standalone. Untuk menambahkan crate yang dihasilkan ke workspace yang sudah ada, tambahkan path output ke array `members` di root `Cargo.toml` workspace. LibMake tidak memodifikasi file workspace yang sudah ada.

**Bisakah saya memperbarui template scaffold setelah generasi awal?**

LibMake menghasilkan file satu kali; alat ini tidak melacak atau memperbarui proyek yang pernah dihasilkan sebelumnya. Untuk mengadopsi template baru, pendekatan yang disarankan adalah menjalankan ulang LibMake ke direktori sementara, lalu membandingkan hasilnya dengan crate yang sudah ada dan menerapkan perubahan yang diinginkan secara selektif.

**Edisi Rust dan nilai MSRV apa yang didukung LibMake?**

LibMake menerima string apa pun untuk `--edition` dan `--rustversion`, lalu menulis nilainya langsung ke `Cargo.toml`. Alat ini tidak memvalidasi apakah edisi atau MSRV yang diberikan adalah versi Rust yang nyata, sehingga pemanggil bertanggung jawab memberikan nilai yang benar.

## Referensi

1. Rousseau, S. *LibMake - A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera - A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Rust library scaffold generator"
