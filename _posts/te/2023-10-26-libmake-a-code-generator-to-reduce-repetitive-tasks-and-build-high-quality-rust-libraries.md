---
title: "LibMake: Rust లైబ్రరీ స్కాఫోల్డ్ జనరేటర్"
tags: "LibMake, RustCodeGenerator, CargoScaffold, RustLibraryTemplate, TeraTemplating, GitHubActionsRust, CargoAudit, RustAPIGuidelines, BoilerplateGenerator, RustCI, ISO 20022, post-quantum cryptography, AI, Rust, open source"
subtitle: "LibMake: మొదటి రోజు నుండే ఉత్తమ పద్ధతులను అమలు చేసే ఒక Rust కోడ్ జనరేటర్."
description: "LibMake అనేది ఒక Rust CLI సాధనం, ఇది ఒకే ఆదేశం నుండి లేదా వెర్షన్‌తో కూడిన TOML/YAML కాన్ఫిగ్ ఫైల్ నుండి పూర్తి లైబ్రరీ స్కాఫోల్డ్‌ను - Cargo.toml, డాక్ టెంప్లేట్‌లతో కూడిన src/lib.rs, పరీక్ష మరియు బెంచ్‌మార్క్ హార్నెస్‌లు, మరియు GitHub Actions CI - రూపొందిస్తుంది."
date: "Oct 26, 2023"
language: "te"
locale: "te_IN"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "పెద్ద తెల్లని స్తంభాలు"
keywords: "LibMake, Rust కోడ్ జనరేటర్, cargo స్కాఫోల్డ్, Rust లైబ్రరీ టెంప్లేట్, Tera టెంప్లేటింగ్, GitHub Actions Rust, cargo-audit, Rust API మార్గదర్శకాలు, బాయిలర్‌ప్లేట్ జనరేటర్, Rust CI వర్క్‌ఫ్లో"
---

[**LibMake ⧉**][00] అనేది ఒక ఓపెన్-సోర్స్ Rust CLI మరియు లైబ్రరీ, ఇది ఒకే ఆహ్వానం నుండి పూర్తి లైబ్రరీ ప్రాజెక్ట్ స్కాఫోల్డ్‌ను రూపొందిస్తుంది. ఇది `cargo new --lib` (ఇది కేవలం ఒక కనీస Cargo.toml మరియు src/lib.rs మాత్రమే సృష్టిస్తుంది) మరియు ఒక ఉత్పత్తికి-సిద్ధమైన లైబ్రరీ సెటప్ (దీనికి డాక్ వ్యాఖ్యలు, CI, పరీక్ష హార్నెస్‌లు, బెంచ్‌మార్క్ నిర్మాణం, CONTRIBUTING.md, మరియు లైసెన్స్ ఫైల్‌లను చేతితో జోడించాల్సి ఉంటుంది) — వీటి మధ్య ఉన్న అంతరాన్ని లక్ష్యంగా చేసుకుంటుంది.

ఈ వ్యాసం LibMake ఏమి రూపొందిస్తుంది, కాన్ఫిగ్-ఫైల్ మరియు CLI మోడ్‌లు ఎలా పనిచేస్తాయి, రూపొందించబడిన CI నిర్మాణం, మరియు టెంప్లేటింగ్ వ్యవస్థ గురించి వివరిస్తుంది.

## ఇన్‌స్టాలేషన్ మరియు ప్రాథమిక వినియోగం

LibMake [crates.io](https://crates.io/crates/libmake) పై ప్రచురించబడింది మరియు Cargo ద్వారా ఇన్‌స్టాల్ చేయబడుతుంది:

```bash
cargo install libmake
```

కనీస CLI ఆహ్వానం ప్రస్తుత డైరెక్టరీలో పేరు పెట్టబడిన లైబ్రరీని రూపొందిస్తుంది:

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

అదనపు ఐచ్ఛిక ఫ్లాగ్‌లలో `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme`, మరియు `--build` ఉన్నాయి.

## కాన్ఫిగ్-ఫైల్ మోడ్

బృంద వినియోగం కోసం, అన్ని CLI ఫ్లాగ్‌లను ఒక TOML కాన్ఫిగ్ ఫైల్‌లో వ్యక్తీకరించవచ్చు:

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

ఇలా ఆహ్వానించబడుతుంది:

```bash
libmake --config libmake.toml
```

LibMake వరుసగా `--config-json`, `--config-yaml`, మరియు `--config-csv` ఫ్లాగ్‌ల ద్వారా JSON, YAML, మరియు CSV కాన్ఫిగ్ ఫార్మాట్‌లను కూడా అంగీకరిస్తుంది. `libmake.toml` ను రిపాజిటరీ మూలానికి కమిట్ చేయడం ద్వారా ప్రతి కంట్రిబ్యూటర్‌కు ఒక పునరుత్పాదక స్కాఫోల్డ్ ప్రాతిపదిక లభిస్తుంది, మరియు టెంప్లేట్ కాన్ఫిగరేషన్‌లో మార్పులు Git డిఫ్‌లలో కనిపిస్తాయి.

## రూపొందించబడిన ప్రాజెక్ట్ నిర్మాణం

ఒక LibMake ఆహ్వానం కింది నిర్మాణాన్ని సృష్టిస్తుంది:

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

రూపొందించబడిన `src/lib.rs` లో ఒక క్రేట్-స్థాయి డాక్ వ్యాఖ్య, `#![deny(missing_docs)]`, README ను rustdoc లోకి లాగడానికి `#![doc = include_str!("../README.md")]`, మరియు అనుబంధ డాక్ వ్యాఖ్యతో కూడిన ఒక స్టబ్ పబ్లిక్ టైప్ ఉంటాయి. అన్ని పబ్లిక్ అంశాలకు డాక్యుమెంటేషన్ ఉండాలనే Rust API మార్గదర్శకాల అవసరాన్ని ఈ ఎంపికలు అనుసరిస్తాయి.

రూపొందించబడిన `benches/lib_benchmarks.rs` [Criterion.rs](https://github.com/bheisler/criterion.rs) ను ఉపయోగిస్తుంది మరియు `criterion` ను ఒక dev-dependency గా జోడించాల్సి ఉంటుంది, దీన్ని LibMake స్వయంచాలకంగా `Cargo.toml` లోకి చొప్పిస్తుంది.

## GitHub Actions CI వర్క్‌ఫ్లో

రూపొందించబడిన `.github/workflows/release.yml` ప్రతి పుష్ మరియు పుల్ రిక్వెస్ట్‌పై ఐదు జాబ్‌లను నడుపుతుంది:

| జాబ్ | టూల్‌చైన్ | ఇది ఏమి తనిఖీ చేస్తుంది |
|---|---|---|
| `test` | stable, beta, nightly (మ్యాట్రిక్స్) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (జాబ్‌లో cargo-audit ఇన్‌స్టాల్ చేయబడుతుంది) |
| `doc` | stable | `cargo doc --no-deps` (లేని డాక్‌ల వద్ద విఫలమవుతుంది) |

nightly జాబ్‌కు `continue-on-error: true` ఉంది, తద్వారా ఒక nightly రిగ్రెషన్ మెర్జ్‌లను నిరోధించదు, అయినప్పటికీ వర్క్‌ఫ్లో రన్‌లో వైఫల్యాన్ని బయటపెడుతుంది.

## Tera తో టెంప్లేటింగ్

LibMake అన్ని రూపొందించబడిన ఫైల్‌లను రెండర్ చేయడానికి [Tera](https://keats.github.io/tera/) టెంప్లేట్ ఇంజన్ — Rust కోసం Jinja2 వంటి సింటాక్స్ — ను ఉపయోగిస్తుంది. ప్రతి టెంప్లేట్ పూర్తి కాన్ఫిగ్ struct ను కాంటెక్స్ట్‌గా అందుకుంటుంది:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

`--template` ఫ్లాగ్ ద్వారా అనుకూల టెంప్లేట్ డైరెక్టరీలు మద్దతు ఇవ్వబడతాయి:

```bash
libmake --config libmake.toml --template ./my_templates/
```

అనుకూల డైరెక్టరీ తప్పనిసరిగా డిఫాల్ట్ టెంప్లేట్ నిర్మాణాన్ని (అదే ఫైల్‌పేర్లు) ప్రతిబింబించాలి. అనుకూల డైరెక్టరీలో ఉన్న ఏ ఫైల్ అయినా సంబంధిత అంతర్నిర్మిత టెంప్లేట్‌ను అధిగమిస్తుంది; అనుకూల డైరెక్టరీలో లేని ఫైల్‌లు అంతర్నిర్మిత వెర్షన్‌కు తిరిగి వస్తాయి. ఇది పాక్షిక అధిగమనలను అనుమతిస్తుంది — ఉదాహరణకు, డిఫాల్ట్ src/lib.rs మరియు Cargo.toml టెంప్లేట్‌లను ఉంచుతూనే కేవలం CI వర్క్‌ఫ్లో టెంప్లేట్‌ను మాత్రమే భర్తీ చేయడం.

## తరచుగా అడిగే ప్రశ్నలు

**LibMake `cargo new --lib` నుండి ఎలా భిన్నంగా ఉంటుంది?**
`cargo new --lib` కేవలం `Cargo.toml` మరియు `src/lib.rs` (ఒకే `#[cfg(test)]` బ్లాక్‌ను కలిగి ఉంటుంది) తో కూడిన కనీస ప్రాజెక్ట్‌ను సృష్టిస్తుంది. LibMake పూర్తి నిర్మాణాన్ని — ఇంటిగ్రేషన్ పరీక్షలు, బెంచ్‌మార్క్‌లు, CI, CONTRIBUTING.md, ద్వంద్వ-లైసెన్స్ ఫైల్‌లు, మరియు సరిగ్గా డాక్యుమెంట్ చేయబడిన src/lib.rs — ప్లేస్‌హోల్డర్‌ల బదులు ప్రాజెక్ట్ యొక్క వాస్తవ మెటాడేటాతో కాన్ఫిగర్ చేసి రూపొందిస్తుంది.

**LibMake ను ఇప్పటికే ఉన్న Cargo వర్క్‌స్పేస్‌తో ఉపయోగించవచ్చా?**
LibMake ఒక స్వతంత్ర క్రేట్ డైరెక్టరీని రూపొందిస్తుంది. రూపొందించబడిన క్రేట్‌ను ఇప్పటికే ఉన్న వర్క్‌స్పేస్‌కు జోడించడానికి, మూల `Cargo.toml` లోని వర్క్‌స్పేస్ `members` శ్రేణికి అవుట్‌పుట్ మార్గాన్ని జోడించండి. LibMake ఇప్పటికే ఉన్న వర్క్‌స్పేస్ ఫైల్‌లను మార్చదు.

**ప్రారంభ రూపకల్పన తర్వాత స్కాఫోల్డ్ టెంప్లేట్‌లను నేను నవీకరించవచ్చా?**
LibMake ఫైల్‌లను ఒకసారి మాత్రమే రూపొందిస్తుంది; ఇది గతంలో రూపొందించబడిన ప్రాజెక్ట్‌లను ట్రాక్ చేయదు లేదా నవీకరించదు. నవీకరించబడిన టెంప్లేట్‌లను స్వీకరించడానికి, సిఫార్సు చేయబడిన విధానం ఏమిటంటే LibMake ను ఒక తాత్కాలిక డైరెక్టరీలోకి మళ్లీ నడిపి, ఫలితాన్ని ఇప్పటికే ఉన్న క్రేట్‌తో డిఫ్ చేసి, కావలసిన మార్పులను ఎంపిక చేసుకుని వర్తింపజేయడం.

**LibMake ఏ Rust ఎడిషన్‌లు మరియు MSRV విలువలకు మద్దతు ఇస్తుంది?**
LibMake `--edition` మరియు `--rustversion` కోసం ఏ స్ట్రింగ్‌నైనా అంగీకరిస్తుంది మరియు విలువలను నేరుగా `Cargo.toml` లో వ్రాస్తుంది. పేర్కొన్న ఎడిషన్ లేదా MSRV నిజమైన Rust వెర్షన్ కాదా అని ఇది ధృవీకరించదు, కాబట్టి సరైన విలువలను అందించే బాధ్యత కాలర్‌లదే.

## సూచనలు

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Rust library scaffold generator"
