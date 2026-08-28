---
author: "contact@sebastienrousseau.com (Sebastien Rousseau)"
banner_alt: "Latar belakang teknis abstrak yang merepresentasikan peta jalan arsitektural sebuah static site generator kelas enterprise."
banner_height: "1280"
banner_width: "1920"
banner: "https://cloudcdn.pro/stocks/images/gemini-background.webp"
cdn: "https://cloudcdn.pro"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2025 - 2026 - Sebastien Rousseau. All rights reserved."
date: "July 22, 2026"
description: "Analisis mendalam static-site generator Rust: keamanan saat kompilasi, gerbang WCAG dan AI lokal, celah di v0.0.41, serta peta jalan enterprise menuju 1.0."
format-detection: "telephone=no"
hreflang: "id"
icon: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/id/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
image_alt: "Potret Hitam Putih Sebastien Rousseau"
image_height: "162"
image_width: "162"
image: "https://cloudcdn.pro/stocks/images/sebastienrousseau.webp"
keywords: "static site generator, Rust, forbid unsafe_code, WCAG 2.2 AA, Content Security Policy, Subresource Integrity, SLSA, SBOM CycloneDX, pipeline LLM lokal, DORA, build inkremental, lol_html, kotak pasir plugin WASM, pencarian vektor semantik, MiniJinja, Ollama"
language: "id"
last_reviewed: "2026-07-22"
layout: "report"
locale: "id_ID"
logo_alt: "Logo Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
menu: ""
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/id/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
rating: "general"
referrer: "no-referrer"
robots: "index, follow"
schema: "FAQPage, Article"
seo_title: "Static Site Generator: Jalan Menuju 1.0"
short_name: "sebastienrousseau"
subtitle: "Audit arsitektural dan peta jalan untuk static-site generator Rust yang dibangun sebagai infrastruktur secure-by-default: apa yang benar-benar dikirim v0.0.41 versus yang dijanjikan README, lima kapabilitas enterprise yang hilang, dan jalur bertahap menuju 1.0 yang selaras dengan DORA dan EAA."
tags: "static site generator, Rust, keamanan web, aksesibilitas, DORA, rantai pasokan, SLSA, AI lokal, WCAG, saat kompilasi, peta jalan, enterprise"
theme-color: "0, 83, 191"
title: "Static Site Generator (SSG): Analisis Mendalam Strategis Kelas Enterprise dan Peta Jalan Arsitektural"
url: "https://sebastienrousseau.com/id/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
atom_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Static Site Generator (SSG) (version 0.0.26)"
item_description: "Analisis mendalam static-site generator Rust: keamanan saat kompilasi, gerbang WCAG dan AI lokal, celah di v0.0.41, serta peta jalan enterprise menuju 1.0."
item_guid: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_link: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap/rss.xml"
item_pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
item_title: "SSG: Analisis Mendalam Strategis & Peta Jalan Kelas Enterprise"
last_build_date: "Wed, 22 Jul 2026 06:06:06 +0000"
managing_editor: "contact@sebastienrousseau.com (Sebastien Rousseau)"
pub_date: "Wed, 22 Jul 2026 07:07:07 +0000"
ttl: "60"
type: "article"
webmaster: "contact@sebastienrousseau.com"
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "SSG Jalan ke 1.0"
apple-touch-fullscreen: "yes"
msapplication-navbutton-color: "0, 83, 191"
twitter_card: "summary_large_image"
twitter_creator: "@wwdseb"
twitter_description: "Gerbang WCAG saat kompilasi, SRI SHA-384, injeksi CSP, dan pipeline LLM lokal membedakan mesin Rust ini. Analisis celah jujur v0.0.41 dan jalan menuju 1.0."
twitter_image: "https://cloudcdn.pro/clients/sebastienrousseau/v1/logos/sebastienrousseau.svg"
twitter_image_alt: "Logo Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Static Site Generator: Jalan Menuju 1.0"
twitter_url: "https://sebastienrousseau.com/2026-07-22-ssg-enterprise-strategic-deep-dive-architectural-roadmap"
excerpt: "Gerbang WCAG saat kompilasi, SRI SHA-384, injeksi CSP, dan pipeline LLM lokal membedakan mesin Rust ini. Ini analisis celah jujur dan jalan menuju 1.0."
author_website: "https://sebastienrousseau.com"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Terima kasih telah membaca!"
site_last_updated: "2026-07-22"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
---

# Static Site Generator (SSG): Analisis Mendalam Strategis Kelas Enterprise dan Peta Jalan Arsitektural

*Tanggal riset: 2026-06-22. Berdasarkan inspeksi basis kode `static-site-generator` pada v0.0.41 dan riset web atas lanskap SSG 2026.*

**Bagi penerbit yang teregulasi, static site generator bukan lagi sekadar alat desain; ia adalah bagian dari perimeter risiko operasional.** [static-site-generator](https://github.com/sebastienrousseau/static-site-generator) Rust yang open-source dibangun di atas premis itu, memindahkan keamanan, aksesibilitas, internasionalisasi, dan pipeline konten AI ke waktu kompilasi sehingga pemeriksaan yang gagal menghentikan build alih-alih mencapai produksi. Analisis ini memisahkan apa yang benar-benar dikirim versi 0.0.41 dari apa yang masih hanya dijanjikan dokumentasinya, menguraikan lima kapabilitas enterprise yang belum dimilikinya, dan mengusulkan jalur bertahap menuju rilis 1.0 yang selaras dengan DORA, European Accessibility Act, dan standar rantai pasokan modern.

<!-- lead-start -->
<aside class="post-lead" aria-label="Ringkasan artikel">
<p class="post-lead-tldr"><strong>TL;DR.</strong> <code>static-site-generator</code> Rust memperlakukan penerbitan web sebagai pipeline perangkat lunak yang dapat diaudit dan secure-by-default: <code>forbid(unsafe_code)</code> di seluruh workspace, Subresource Integrity SHA-384, ekstraksi Content Security Policy, gerbang WCAG 2.2 AA saat kompilasi, dan pipeline LLM lokal. Inspeksi kode v0.0.41 menunjukkan beberapa fitur yang terdokumentasi masih bersifat aspiratif, di antaranya minifikasi native, rebuild inkremental, dan AVIF. Inilah analisis celah yang jujur dan peta jalan bertahap menuju 1.0 kelas enterprise.</p>
<p class="post-lead-heading"><strong>Poin-poin utama</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>Model keamanan dan aksesibilitasnya nyata.</strong> SRI saat kompilasi, ekstraksi CSP, rilis bertanda tangan dengan atestasi Sigstore dan SBOM CycloneDX, ditambah gerbang WCAG 2.2 AA yang menghentikan build, diimplementasikan dalam kode, bukan sekadar didokumentasikan.</li>
  <li><strong>Beberapa fitur unggulan tidak demikian.</strong> Minifier hanyalah pengecil spasi, graf dependensi yang seharusnya menggerakkan build inkremental tidak pernah diisi di produksi, dan enkoding AVIF adalah stub yang mengembalikan vektor kosong.</li>
  <li><strong>Lima kapabilitas enterprise masih hilang.</strong> Kotak pasir plugin WASM, penulis-ulang HTML zero-copy streaming, pencarian semantik lokal, cache inferensi deterministik, dan I/O file asinkron.</li>
  <li><strong>Peta jalan diurutkan berdasarkan risiko.</strong> Patch kebenaran (0.0.42), minor kredibilitas-dan-inkremental (0.1.0), lalu major enterprise (1.0.0) yang membawa kotak pasir, pencarian semantik, dan provenans SLSA v1.1.</li>
</ul>
<p class="post-lead-related"><strong>Bacaan terkait:</strong> <a href="https://sebastienrousseau.com/2026-07-03-emerging-technology-risk-horizon-banks-2026">The Emerging-Technology Risk Horizon for Banks</a>, <a href="https://sebastienrousseau.com/2026-07-07-corporate-banking-api-standard-agentic-mcp-2026">A Corporate Banking API Standard for Agentic MCP</a>.</p>
</aside>
<!-- lead-end -->

> **Ringkasan Eksekutif**
>
> - **Penerbitan kini menjadi perimeter risiko operasional.** Di bawah DORA, European Accessibility Act, dan GDPR, setiap aset yang menghadap publik adalah titik masuk potensial untuk kompromi rantai pasokan, defacement, dan paparan regulasi. Model saat kompilasi mempersempit perimeter itu dengan menolak keluaran yang tidak patuh sebelum dikirim.
> - **Pembeda mesin ini ditegakkan oleh compiler, bukan aspirasi yang didokumentasikan.** `forbid(unsafe_code)` di seluruh workspace, SRI SHA-256/384 yang sesungguhnya, ekstraksi CSP otomatis, dan gerbang WCAG 2.2 AA saat build mengubah keamanan dan aksesibilitas dari audit pasca-fakta menjadi kegagalan build yang keras.
> - **Versi 0.0.41 memiliki celah antara dokumentasi dan kode.** Minifikasi native, rebuild inkremental via graf dependensi, dan dukungan AVIF dideskripsikan tetapi tidak berfungsi; artikel ini menamai setiap celah terhadap lokasi sumber yang persis.
> - **Jalur menuju 1.0 adalah sebuah urutan, bukan daftar keinginan.** Ketahanan lebih dulu (0.0.42), lalu kebenaran inkremental (0.1.0), kemudian kapabilitas enterprise, kotak pasir WASM, pencarian semantik lokal, dan provenans SLSA yang dapat diverifikasi, yang dibutuhkan pembeli teregulasi (1.0.0).

## Kekuatan Saat Ini

Basis kode `static-site-generator` memperlihatkan beberapa keputusan rekayasa yang khas dan membedakannya dari mesin JavaScript dan Go warisan:

- **Postur keamanan saat kompilasi:** `#![forbid(unsafe_code)]` di seluruh workspace memberikan jaminan keamanan memori saat kompilasi. Pipeline build menghasilkan hash Subresource Integrity (SRI) SHA-256/SHA-384 yang sesungguhnya (`src/plugins/assets.rs`) dan melakukan ekstraksi Content Security Policy (CSP) otomatis yang menghapus skrip dan gaya unsafe-inline. Rilis ditandatangani, membawa atestasi Sigstore, dan menghasilkan SBOM CycloneDX 1.5 pada setiap build.  
- **Gerbang aksesibilitas yang ditegakkan compiler:** Pemeriksaan Web Content Accessibility Guidelines (WCAG) 2.2 Level AA berjalan di dalam pipeline kompilasi melalui parser axe-core saat build yang digerakkan Playwright. Aksesibilitas menjadi gerbang build yang keras alih-alih audit pasca-publikasi: jika sebuah halaman gagal, kompilasi berhenti dengan kesalahan bernomor baris yang persis.  
- **Pipeline AI berdaulat-data:** Pipeline terjemahan dan ekstraksi metadata berbasis LLM lokal (via endpoint Ollama atau llama.cpp lokal) memungkinkan sebuah institusi mengotomatiskan peringkasan konten, pembuatan skema JSON-LD, dan terjemahan multibahasa tanpa mengirim pengungkapan pra-laba atau kekayaan intelektual sensitif ke API AI cloud publik.  
- **Kompilasi terparalelisasi:** Jaminan keamanan memori Rust menjadi dasar pipeline HTML dan aset terparalelisasi yang digerakkan Rayon (`src/core/pipeline.rs`). Pipeline plugin menjalankan transformasi terfusi, dengan `SearchPlugin`, `SeoPlugin`, `CanonicalPlugin`, dan `JsonLdPlugin` beroperasi di atas `par_iter()`, sehingga setiap halaman dibaca dan ditulis ke disk sekali saja.  
- **Higiene rantai pasokan dan dependensi:** Migrasi mesin templat dari Tera ke MiniJinja (`v0.0.37`) mengurangi ukuran biner, menghapus dependensi transitif seperti `rand` saat kompilasi, dan menghasilkan jejak dependensi yang ringkas sehingga menurunkan paparan rantai pasokan perangkat lunak.

---

## Celah dan Realitas Dunia Nyata

Meskipun memiliki kekuatan-kekuatan luar biasa ini, inspeksi basis kode v0.0.41 yang ketat mengungkap beberapa celah arsitektural, fungsional, dan pengalaman pengembang antara klaim dokumentasinya dan kode rust yang sebenarnya:

### Celah Arsitektural

- **Pengecilan Spasi vs. Minifikasi Native:** Meskipun README menjanjikan "minifikasi JS/CSS native," `MinifyPlugin` (`src/plugins/plugins.rs:96-116`) hanya berfungsi sebagai pengecil spasi yang naif. Ia berhenti-singkat pada elemen `<pre>` dan mengecilkan rentetan spasi di HTML, tetapi tidak melakukan minifikasi CSS atau JS native yang sadar-sintaksis. Lebih jauh, ia hanya memproses halaman tingkat atas dan tidak menelusuri subdirektori secara rekursif (seperti `/blog/` atau `/tags/`), sehingga halaman-halaman dalam tidak terminifikasi.  
- **Infrastruktur Inkremental Mati:** Graf pelacakan dependensi (`DepGraph` di `src/core/depgraph.rs`) dikompilasi dan dimuat ke `PluginContext.dep_graph` tetapi tidak pernah benar-benar diisi dalam kode produksi. Metode `add_dep()` hanya dipanggil dalam uji unit, sehingga klaim README tentang "rebuild inkremental via graf dependensi" saat ini bersifat aspiratif.  
- **Kompilasi Terbatch vs. Kompilasi Streaming:** Modul `streaming::compile_batch` (`src/core/streaming.rs`) tidak benar-benar melakukan streaming. Sebaliknya, ia mengompilasi halaman dalam batch ke direktori sementara, menjalankan `staticdatagen::compile` dari nol untuk setiap batch, dan menggabungkan keluarannya. Ini menghasilkan overhead I/O disk yang signifikan dan parsing yang berlebihan, menyimpang dari arsitektur streaming sejati.  
- **Pelanggaran Fase Siklus Hidup Plugin:** Plugin yang menghasilkan halaman HTML baru selama proses build, seperti `TaxonomyPlugin`, `PaginationPlugin`, dan `I18nPlugin`, menulis langsung ke disk pada `after_compile` alih-alih menggunakan siklus hidup `transform_html`. Akibatnya, halaman yang dihasilkan plugin ini melewati plugin pasca-pemrosesan yang kritis (seperti `CanonicalPlugin`, `JsonLdPlugin`, `RobotsPlugin`, dan `AccessibilityPlugin`) jika plugin-plugin itu terdaftar lebih awal. Ini membuat halaman tag, kategori, dan terpaginasi tanpa tautan kanonik yang benar, skema JSON-LD, atau validasi aksesibilitas.  
- **Memanggil `curl` di `LlmPlugin`:** Pipeline konten LLM lokal (`src/plugins/llm.rs`) memanggil langsung biner `curl` host untuk mengueri endpoint lokal. Ini memperkenalkan bug lintas-platform yang parah (misalnya, pada host Windows tanpa curl di PATH), menimbulkan risiko keamanan (vektor injeksi shell), dan gagal di lingkungan CI yang terkunci atau terisolasi jaringan.  
- **Manipulasi String Naif dalam Penulisan-Ulang HTML:** Ekstraktor `image_plugin.rs` dan `search.rs` menulis-ulang string HTML menggunakan operasi `str::find` dan `str::rfind` yang rapuh. Pendekatan ini sangat rentan terhadap tag HTML yang rusak, tag `<img>` di dalam komentar, entitas karakter dalam teks alt, atau properti `srcset` yang sudah ada sebelumnya, yang dapat menghasilkan keluaran yang korup.  
- **Dukungan AVIF Belum Diimplementasikan:** Meskipun enkoding gambar AVIF didokumentasikan secara luas, implementasi di `image_plugin.rs` adalah stub yang membuat `avif_variants` sekadar mengembalikan `Vec::new()`, sehingga fitur ini tidak berfungsi.  
- **Watcher Berbasis Polling:** Watcher pada server pengembangan lokal (`src/server/watch.rs`) menggunakan polling alih-alih API peristiwa sistem berkas, yang menyebabkan penggunaan CPU idle yang berlebihan dan latensi modifikasi sub-detik.

### Celah Fungsional & DX

- **Tanpa Pelacakan Dependensi Transitif:** Graf dependensi tidak dapat melacak dependensi bersarang (misalnya, perubahan pada sub-templat yang memengaruhi tata letak yang memengaruhi halaman), sebagaimana diverifikasi oleh uji unit `transitive_not_tracked`.  
- **Tanpa Flag CLI Kompilasi Inkremental:** Tidak ada flag CLI `--incremental` yang terhubung ke compiler eksekusi, sehingga pengembang tidak dapat menggunakan build yang di-cache.  
- **HMR Terbatas pada CSS:** Hot Module Replacement (HMR) hanya mendukung CSS; setiap modifikasi pada file HTML, tata letak, atau markdown memicu muat-ulang halaman penuh, yang menurunkan kecepatan pengembang.  
- **Kekurangan Subperintah:** Pengembang harus secara manual meneruskan flag yang bertele-tele (`ssg -s public -w`) karena subperintah standar seperti `ssg dev`, `ssg build`, `ssg check`, dan `ssg lint` tidak ada.

---

## Celah Arsitektural yang Kita Lewatkan (Temuan Baru)

Di luar celah pada v0.0.41, menilai proyek ini terhadap profil risiko kelas keuangan memunculkan beberapa kapabilitas yang belum disediakannya tetapi akan dibutuhkan oleh pembeli enterprise:

### 1. Kotak Pasir Plugin WebAssembly (Ekstensi Zero-Trust)

Meskipun biner compiler itu sendiri ditulis dalam Rust yang aman, membiarkan plugin pihak ketiga sembarangan dieksekusi secara native pada sistem host memperkenalkan kerentanan rantai pasokan yang parah. Plugin pihak ketiga yang terkompromi dapat dengan mudah mengakses sistem berkas host, membaca file Markdown milik institusi, atau mengeksfiltrasi kredensial privat.

* **Kapabilitas yang Hilang:** Lingkungan eksekusi berkotak pasir. Untuk mencapai kompilasi zero-trust, compiler seharusnya mengeksekusi plugin pihak ketiga di dalam runtime WebAssembly tertanam (seperti `wasmtime`). Plugin seharusnya berinteraksi dengan host semata-mata melalui WebAssembly System Interface (WASI) yang dibatasi, membatasi aksesnya secara ketat hanya pada halaman yang sedang ditransformasikan.

### 2. Parsing HTML Zero-Copy via AST Streaming (`lol_html`)

Migrasi lapisan parsing HTML ke pustaka DOM in-memory penuh (seperti Kuchiki atau html5ever) memperkenalkan overhead memori yang signifikan dan jeda pemrosesan saat menangani situs dengan lebih dari 100.000 halaman.

* **Kapabilitas yang Hilang:** Penulis-ulang HTML streaming zero-copy. Memanfaatkan `lol_html` dari Cloudflare (Low-Output-Latency HTML rewriter) memungkinkan compiler mem-parsing, memeriksa, dan memodifikasi elemen HTML dalam satu lintasan streaming dengan alokasi memori mendekati-nol, sesuai dengan target compiler streaming paralel untuk build sub-detik.

### 3. Pencarian Vektor Semantik Lokal (RAG Lokal)

Indeks pencarian saat ini (`SearchPlugin`) menghasilkan indeks JSON datar yang berat dan melakukan pencocokan string sisi-klien sederhana, tanpa dukungan untuk pencarian fuzzy, stemming, atau kueri semantik. Pagefind adalah perbaikan, tetapi ia masih bergantung pada pengunduhan indeks yang besar.

* **Kapabilitas yang Hilang:** Pencarian semantik tertanam. Compiler seharusnya memanfaatkan model embedding vektor lokal yang ringan dan native-Rust (seperti model MiniLM-L6 yang dieksekusi via `candle` atau `ort` / ONNX Runtime) pada waktu build. Ia seharusnya menghasilkan embedding vektor padat untuk setiap paragraf halaman dan mengeluarkan indeks vektor yang ringkas. Widget pencarian sisi-klien, yang dikompilasi ke WASM, kemudian dapat melakukan pencarian semantik luring sejati langsung di peramban.

### 4. Cache Terjemahan dan Inferensi Deterministik

Karena inferensi LLM lokal (misalnya, via Ollama atau Llama.cpp) sangat intensif CPU/GPU, menerjemahkan atau menghasilkan metadata untuk ribuan halaman pada setiap build secara komputasional tidak terjangkau.

* **Kapabilitas yang Hilang:** Cache inferensi berbasis hash-konten. Compiler harus memelihara cache deterministik untuk semua operasi LLM. Jika hash SHA-256 dari konten file markdown dan parameter terjemahannya cocok dengan entri cache, compiler seharusnya menggunakan kembali terjemahan dan metadata yang di-cache, melewati inferensi lokal yang berlebihan.

### 5. I/O File Asinkron untuk Penskalaan Paralel

Meskipun pipeline plugin terparalelisasi via Rayon, penulisan disk sinkron standar memblokir thread OS milik Rayon, menciptakan hambatan I/O saat menulis puluhan ribu halaman.

* **Kapabilitas yang Hilang:** I/O disk asinkron dan non-pemblokiran. Compiler seharusnya memisahkan tugas intensif-CPU (parsing Markdown, minifikasi) dari penulisan terikat-disk, menggunakan kolam thread I/O asinkron atau ikatan `io_uring` Linux (via `rio` atau `tokio`) untuk menulis halaman terkompilasi secara paralel tanpa memblokir eksekutor CPU paralel.

---

## Peta Jalan Strategis 1.0

Peta jalan berikut mengintegrasikan baik celah yang telah diselesaikan maupun kapabilitas kelas enterprise yang baru ditemukan ke dalam kerangka rilis yang terstruktur dan kronologis.

### Fase 1: 0.0.42 (Patch Ketahanan dan Kebenaran, 1 hingga 2 minggu)

1. **Rekonstruksi `MinifyPlugin`:** Integrasi `minify-html`, `oxc_minifier`, dan `lightningcss` untuk minifikasi HTML, JS, dan CSS native yang sadar-sintaksis. Pastikan plugin menelusuri secara rekursif semua direktori bersarang di bawah `site_dir`.  
2. **Amankan Pipeline AI:** Migrasikan `LlmPlugin` dari pemanggilan shell `curl` native ke `ureq` (klien HTTP Rust yang ringan, sinkron, dan aman) untuk memastikan kompatibilitas lintas-platform dan menghilangkan kerentanan injeksi shell.  
3. **Selesaikan Implementasi AVIF:** Sambungkan `ravif` langsung ke pipeline aset gambar, mengaktifkan enkoding AVIF berkinerja tinggi berdampingan dengan WebP dan PNG.  
4. **Otomatiskan HrefLang dan Pemetaan Multi-Lokal:** Deteksi secara otomatis halaman terjemahan paralel dalam build multibahasa dan injeksikan tag standar `<link rel="alternate" hreflang="..." />` yang patuh-Google ke dalam head setiap file HTML terkompilasi.  
5. **Dukungan JSON Feed 1.1:** Kirimkan emitter JSON Feed 1.1 khusus berdampingan dengan kanal sindikasi standar RSS 2.0 dan Atom 1.0.

### Fase 2: 0.1.0 (Minor Kredibilitas dan Inkremental, 2 hingga 3 bulan)

1. **Isi `DepGraph` dan Aktifkan `--incremental`:** Sambungkan `DepGraph` sepenuhnya untuk melacak dependensi templat-ke-halaman dan markdown-ke-halaman. Implementasikan lapisan invalidasi cache dan sambungkan flag CLI `--incremental`, menargetkan rebuild sub-200ms untuk lingkungan cache-hangat.  
2. **Penulisan-Ulang AST Streaming via `lol_html`:** Ganti penulisan-ulang string yang rapuh di `image_plugin.rs`, `search.rs`, dan injeksi CSP dengan penulis-ulang HTML streaming zero-copy yang ditenagai `lol_html`.  
3. **Watcher Berbasis-Peristiwa dan HMR Komponen:** Migrasikan modul watch dari polling ke crate `notify` berbasis-peristiwa, dan implementasikan muat-ulang panas khusus-CSS dan HTML-parsial untuk pembaruan peramban sub-100ms.  
4. **CLI Perintah Terpadu:** Arsitektur ulang antarmuka compiler untuk mendukung subperintah standar: `ssg dev`, `ssg build`, `ssg check` (audit aksesibilitas/SEO), dan `ssg deploy`.  
5. **Cache Inferensi Deterministik:** Implementasikan lapisan caching berbasis hash-konten untuk semua tugas terjemahan, peringkasan, dan ekstraksi metadata LLM lokal.

### Fase 3: 1.0.0 (Major Enterprise dan Produksi, 6 hingga 12 bulan)

1. **Kotak Pasir Plugin WASM Zero-Trust:** Tanamkan runtime WebAssembly (`wasmtime` atau `wasmer`) untuk mengeksekusi plugin pihak ketiga di lingkungan berkotak pasir penuh dengan akses sistem berkas dan jaringan berbasis-kapabilitas.  
2. **Pencarian Vektor Semantik Lokal (RAG Lokal):** Tanamkan model embedding native-Rust lokal (via `candle` atau `ort`) untuk mengompilasi embedding paragraf padat menjadi indeks yang ringkas, mengaktifkan pencarian semantik sisi-klien yang privat.  
3. **Server Islands dan Target Edge WASM:** Implementasikan eksekusi komponen `<ssg-island>` pada runtime edge (seperti Cloudflare Workers, Vercel Edge, atau Netlify Edge) yang dibangun di atas inti `ssg-wasm` terkompilasi.  
4. **Mesin I/O Paralel Asinkron:** Arsitektur ulang modul penulisan sistem berkas untuk menggunakan kolam thread I/O asinkron dan ikatan `io_uring`, menghilangkan pemblokiran pekerja CPU selama penulisan paralel.  
5. **Provenans Build SLSA v1.1 & Kepatuhan SPDX 3.0:** Sediakan provenans build SLSA Level 3 yang dapat diverifikasi secara matematis dan hasilkan SBOM yang patuh SPDX 3.0, sepenuhnya memenuhi standar keamanan rantai pasokan perangkat lunak modern.

---

## Matriks Pesaing (Lanskap 2026)

Matriks berikut membandingkan `static-site-generator` (target v1.0) terhadap mesin penerbitan web terkemuka pada 2026:

| Kapabilitas | static-site-generator v1.0 | Hugo v0.155+ | Zola v0.19+ | Astro 5 | Eleventy 3 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| **Bahasa / Runtime** | Rust (Zero Unsafe) | Go | Rust | JS (Node/V8) | JS (Node/V8) |
| **Gerbang Build A11y** | Validasi AST Saat Build | Tidak Ada | Tidak Ada | Linter Pasca-build | Linter Pasca-build |
| **Pengerasan Keamanan** | SRI SHA-384 & Injeksi CSP | Manual | Manual | Manual | Manual |
| **Keamanan Rantai Pasokan** | SLSA L3 \+ SPDX 3.0 \+ Kotak Pasir WASM | Minimal | Minimal | Pohon NPM Berat | Pohon NPM Berat |
| **Pipeline Konten AI** | Privat, Local-First (LLM Lokal) | Tidak Ada | Tidak Ada | Hanya API Publik | Hanya API Publik |
| **Kecepatan Inkremental** | \<200ms (Cache Hangat) | \<100ms | \<150ms | \~1.5s | \~140ms |
| **Interaktivitas Dinamis** | Server Islands (Target WASM) | Tidak Ada | Tidak Ada | Server Islands (JS) | Islands (JS) |
| **Mesin Pencari** | Pencarian Semantik WASM Lokal | String Sederhana | String Sederhana | Pagefind (JS) | Pagefind (JS) |

---

## Pemosisian pada 1.0

Pada 1.0, pemosisian yang dituju adalah static site generator yang direkayasa sebagai infrastruktur perangkat lunak secure-by-default: penulisan yang didukung pipeline AI local-first; kompilasi 100.000-plus halaman melalui pipeline streaming paralel; WCAG 2.2 AA serta CSP dan SRI ketat yang ditegakkan sebagai gerbang build; dan dynamic islands berkotak pasir, semuanya dalam satu biner Rust yang aman-memori. Setiap klausa dalam pernyataan itu memetakan ke item spesifik dalam peta jalan di atas alih-alih ke aspirasi pemasaran.

---

## Integrasi Regulasi dan Kepatuhan

Di sektor enterprise dan keuangan berisiko tinggi, perangkat lunak dievaluasi melalui lensa kepatuhan dan modal risiko. Peta jalan arsitektural `static-site-generator` selaras langsung dengan mandat regulasi utama:

- **DORA Pasal 6 (Manajemen Risiko TIK):** Kalkulasi saat kompilasi dan injeksi hash SRI SHA-384 serta Content Security Policy yang ketat memenuhi persyaratan untuk melindungi kanal penerbitan digital dari injeksi rantai pasokan, defacement web, dan vektor cross-site scripting (XSS).  
- **DORA Pasal 7 (Ketahanan Sistem TIK):** Dengan beralih ke aset statis yang tak-berubah dan terverifikasi saat kompilasi, institusi keuangan menghilangkan kerentanan basis data dan server runtime, menurunkan pengali risiko operasional dan mengurangi cadangan modal risiko yang diwajibkan di bawah Basel III.  
- **Direktif European Accessibility Act (EAA) (EU) 2019/882:** Menggeser audit aksesibilitas ke kiri ke dalam pipeline kompilasi sebagai gerbang compiler yang keras menjamin kepatuhan 100% sebelum penerapan, menghilangkan risiko kerusakan merek dan litigasi perdata di bawah EAA dan ADA Title III.  
- **GDPR Pasal 25 (Privacy-by-Design):** Menjalankan pipeline terjemahan dan metadata pada perangkat keras lokal yang terisolasi jaringan menjaga draf milik institusi, metrik keuangan, dan data pribadi keluar dari penyedia LLM cloud pihak ketiga publik, mendukung kepatuhan pada prinsip kedaulatan data.

---

## Pertanyaan yang Sering Diajukan

**Apa yang sebenarnya dikirim versi 0.0.41 hari ini, versus apa yang diklaim README?**
Model keamanan dan aksesibilitas nyata dan ditegakkan dalam kode: `forbid(unsafe_code)` di seluruh workspace, pembuatan SRI SHA-256/384, ekstraksi CSP, rilis bertanda tangan dengan atestasi Sigstore dan SBOM CycloneDX, serta gerbang WCAG 2.2 AA yang menghentikan build. Tiga fitur yang terdokumentasi tidak berfungsi di v0.0.41. `MinifyPlugin` adalah pengecil spasi alih-alih minifier yang sadar-sintaksis; `DepGraph` yang seharusnya menggerakkan rebuild inkremental dikompilasi tetapi tidak pernah diisi dalam kode produksi; dan enkoding AVIF adalah stub yang `avif_variants`-nya mengembalikan vektor kosong.

**Apakah gerbang aksesibilitas itu gerbang compiler yang sesungguhnya atau linter pasca-build?**
Ia adalah gerbang build. Pemeriksaan WCAG 2.2 AA berjalan di dalam pipeline kompilasi melalui parser axe-core saat build yang digerakkan Playwright, dan halaman yang gagal menghentikan kompilasi dengan kesalahan bernomor baris yang persis alih-alih mengeluarkan peringatan setelah fakta. Itulah properti yang dibutuhkan kewajiban European Accessibility Act: keluaran yang tidak patuh tidak dapat mencapai penerapan.

**Mengapa pemanggilan `curl` di plugin LLM penting?**
Pipeline LLM lokal (`src/plugins/llm.rs`) memanggil biner `curl` host untuk menjangkau endpoint lokal. Itu mengaitkan build ke sebuah executable host, gagal pada sistem tanpa `curl` di PATH, memperkenalkan permukaan injeksi-shell, dan rusak di CI yang terisolasi jaringan. Memigrasikan panggilan ke klien HTTP Rust seperti `ureq` menghilangkan dependensi eksternal dan vektor injeksi, itulah alasannya menjadi item kedua dalam patch 0.0.42.

**Apa item tunggal yang paling penting dalam jalan menuju 1.0?**
Mengisi `DepGraph` dan menyambungkan flag `--incremental`. Rebuild inkremental adalah celah kredibilitas antara mesin yang terdokumentasi dan yang sebenarnya, dan setiap klaim hilir tentang build sub-detik pada 100.000-plus halaman bergantung pada graf dependensi yang melacak tepi templat-ke-halaman dan markdown-ke-halaman alih-alih tetap menjadi infrastruktur khusus-uji.

## Referensi

- [Cloudflare, *lol-html: Low-Output-Latency streaming HTML rewriter*](https://github.com/cloudflare/lol-html "Cloudflare lol-html — penulis-ulang HTML streaming") ⧉. [Penulis-ulang HTML streaming zero-copy yang diusulkan untuk menggantikan manipulasi string yang rapuh pada fase 0.1.0.]
- [W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/ "W3C — Rekomendasi WCAG 2.2") ⧉. [Kriteria sukses Level AA yang ditegakkan oleh gerbang aksesibilitas saat kompilasi.]
- [Uni Eropa, *Regulation (EU) 2022/2554 (DORA)*](https://eur-lex.europa.eu/eli/reg/2022/2554/oj "EUR-Lex — Digital Operational Resilience Act") ⧉. [Pasal-pasal manajemen risiko dan ketahanan TIK yang dipetakan oleh postur keamanan.]
- [OpenSSF, *Supply-chain Levels for Software Artifacts (SLSA) v1.0*](https://slsa.dev/spec/v1.0/ "SLSA — spesifikasi v1.0") ⧉. [Kerangka provenans build yang ditargetkan untuk atestasi Level 3 yang dapat diverifikasi pada 1.0.]
- [Armin Ronacher, *MiniJinja template engine*](https://github.com/mitsuhiko/minijinja "MiniJinja — mesin Jinja2 minimal untuk Rust") ⧉. [Mesin ringan-dependensi yang menggantikan Tera dan memangkas pohon transitif.]
- [CycloneDX, *Software Bill of Materials specification v1.5*](https://cyclonedx.org/docs/1.5/ "CycloneDX — spesifikasi SBOM v1.5") ⧉. [Format SBOM yang dikeluarkan pada setiap build untuk audit rantai pasokan.]
- [Uni Eropa, *Directive (EU) 2019/882 (European Accessibility Act)*](https://eur-lex.europa.eu/eli/dir/2019/882/oj "EUR-Lex — European Accessibility Act") ⧉. [Kewajiban aksesibilitas yang dirancang untuk dipenuhi oleh gerbang WCAG saat build.]

*Terakhir ditinjau Juli 2026. Analisis asli berdasarkan inspeksi basis kode `static-site-generator` pada v0.0.41; sumber dikutip, bukan direproduksi. Nomor versi dan status fitur bergerak cepat, verifikasi terhadap repositori sebelum penerbitan ulang. Dilisensikan di bawah CC-BY-4.0.*
