---
title: "LibMake: Rust நூலகச் சட்டக உருவாக்கி"
tags: "LibMake, RustCodeGenerator, CargoScaffold, RustLibraryTemplate, TeraTemplating, GitHubActionsRust, CargoAudit, RustAPIGuidelines, BoilerplateGenerator, RustCI, ISO 20022, post-quantum cryptography, AI, Rust, open source"
subtitle: "LibMake: முதல் நாளிலிருந்தே சிறந்த நடைமுறைகளை நடைமுறைப்படுத்தும் ஒரு Rust குறியீட்டு உருவாக்கி."
description: "LibMake என்பது ஒரு Rust CLI கருவியாகும் - ஒரே கட்டளையிலிருந்து அல்லது பதிப்பிடப்பட்ட TOML/YAML கட்டமைப்புக் கோப்பிலிருந்து முழுமையான நூலகச் சட்டகத்தை உருவாக்குகிறது: Cargo.toml, ஆவணப் படிமங்களுடன் src/lib.rs, சோதனை மற்றும் அளவீட்டு அமைப்புகள், மற்றும் GitHub Actions CI."
date: "Oct 26, 2023"
language: "ta"
locale: "ta_IN"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "பிரம்மாண்டமான வெள்ளைத் தூண்கள்"
keywords: "LibMake, Rust குறியீட்டு உருவாக்கி, cargo சட்டகம், Rust நூலகப் படிமம், Tera டெம்ப்ளேட்டிங், GitHub Actions Rust, cargo-audit, Rust API வழிகாட்டுதல்கள், boilerplate உருவாக்கி, Rust CI பணிப்பாய்வு"
---

[**LibMake ⧉**][00] என்பது ஒரு திறந்த-மூல Rust CLI மற்றும் நூலகமாகும் — ஒரே அழைப்பிலிருந்து முழுமையான நூலகத் திட்டச் சட்டகத்தை உருவாக்குகிறது. இது `cargo new --lib` (இது குறைந்தபட்ச Cargo.toml மற்றும் src/lib.rs ஐ மட்டுமே உருவாக்குகிறது) மற்றும் உற்பத்திக்குத் தயாரான நூலக அமைப்பு (இதற்கு ஆவணக் குறிப்புகள், CI, சோதனை அமைப்புகள், அளவீட்டு அமைப்பு, CONTRIBUTING.md மற்றும் உரிமக் கோப்புகளைக் கைமுறையாகச் சேர்க்க வேண்டும்) ஆகியவற்றுக்கு இடையேயுள்ள இடைவெளியைக் குறிவைக்கிறது.

இந்தக் கட்டுரை LibMake என்ன உருவாக்குகிறது, கட்டமைப்புக்-கோப்பு மற்றும் CLI முறைகள் எவ்வாறு செயல்படுகின்றன, உருவாக்கப்பட்ட CI அமைப்பு, மற்றும் டெம்ப்ளேட்டிங் அமைப்பு ஆகியவற்றை விவரிக்கிறது.

## நிறுவலும் அடிப்படைப் பயன்பாடும்

LibMake [crates.io](https://crates.io/crates/libmake) இல் வெளியிடப்பட்டு Cargo வழியாக நிறுவப்படுகிறது:

```bash
cargo install libmake
```

குறைந்தபட்ச CLI அழைப்பு தற்போதைய அடைவில் பெயரிடப்பட்ட ஒரு நூலகத்தை உருவாக்குகிறது:

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

கூடுதல் விருப்பக் கொடிகளில் `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme`, மற்றும் `--build` ஆகியவை அடங்கும்.

## கட்டமைப்புக்-கோப்பு முறை

குழுப் பயன்பாட்டிற்கு, அனைத்து CLI கொடிகளையும் ஒரு TOML கட்டமைப்புக் கோப்பில் வெளிப்படுத்த முடியும்:

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

இவ்வாறு அழைக்கப்படுகிறது:

```bash
libmake --config libmake.toml
```

LibMake முறையே `--config-json`, `--config-yaml`, மற்றும் `--config-csv` கொடிகள் வழியாக JSON, YAML மற்றும் CSV கட்டமைப்பு வடிவங்களையும் ஏற்கிறது. களஞ்சிய மூலத்தில் `libmake.toml` ஐ கமிட் செய்வது ஒவ்வொரு பங்களிப்பாளருக்கும் மீண்டும் உருவாக்கக்கூடிய சட்டக அடிப்படையை வழங்குகிறது, மேலும் டெம்ப்ளேட் கட்டமைப்பில் செய்யப்படும் மாற்றங்கள் Git diff களில் தெரிகின்றன.

## உருவாக்கப்பட்ட திட்ட அமைப்பு

ஒரு LibMake அழைப்பு பின்வரும் அமைப்பை உருவாக்குகிறது:

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

உருவாக்கப்பட்ட `src/lib.rs` இல் ஒரு கிரேட்-நிலை ஆவணக் குறிப்பு, `#![deny(missing_docs)]`, README ஐ rustdoc இற்குள் இழுக்கும் `#![doc = include_str!("../README.md")]`, மற்றும் தொடர்புடைய ஆவணக் குறிப்புடன் கூடிய ஒரு stub பொது வகை ஆகியவை அடங்கும். இந்தத் தேர்வுகள், அனைத்துப் பொது உருப்படிகளுக்கும் ஆவணப்படுத்தல் இருக்க வேண்டும் என்ற Rust API வழிகாட்டுதல்களின் தேவையைப் பின்பற்றுகின்றன.

உருவாக்கப்பட்ட `benches/lib_benchmarks.rs` [Criterion.rs](https://github.com/bheisler/criterion.rs) ஐப் பயன்படுத்துகிறது, மேலும் `criterion` ஐ ஒரு dev-dependency ஆகச் சேர்க்க வேண்டும் — இதை LibMake தானாகவே `Cargo.toml` இல் செருகுகிறது.

## GitHub Actions CI பணிப்பாய்வு

உருவாக்கப்பட்ட `.github/workflows/release.yml` ஒவ்வொரு push மற்றும் pull request இலும் ஐந்து பணிகளை இயக்குகிறது:

| பணி | கருவித்தொகுப்பு | அது சரிபார்ப்பது |
|---|---|---|
| `test` | stable, beta, nightly (matrix) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (cargo-audit பணியில் நிறுவப்படுகிறது) |
| `doc` | stable | `cargo doc --no-deps` (ஆவணங்கள் இல்லாவிட்டால் தோல்வியடையும்) |

nightly பணியில் `continue-on-error: true` இருப்பதால், ஒரு nightly பின்னடைவு merge களைத் தடுக்காது, அதே நேரத்தில் அந்தத் தோல்வியை பணிப்பாய்வு இயக்கத்தில் இன்னும் வெளிப்படுத்துகிறது.

## Tera உடன் டெம்ப்ளேட்டிங்

LibMake அனைத்து உருவாக்கப்பட்ட கோப்புகளையும் வழங்க [Tera](https://keats.github.io/tera/) டெம்ப்ளேட் இயந்திரத்தைப் பயன்படுத்துகிறது — இது Rust இற்கான Jinja2-போன்ற தொடரியல் ஆகும். ஒவ்வொரு டெம்ப்ளேட்டும் முழு கட்டமைப்பு struct ஐ சூழலாகப் பெறுகிறது:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

`--template` கொடி வழியாக தனிப்பயன் டெம்ப்ளேட் அடைவுகள் ஆதரிக்கப்படுகின்றன:

```bash
libmake --config libmake.toml --template ./my_templates/
```

தனிப்பயன் அடைவு இயல்புநிலை டெம்ப்ளேட் அமைப்பை (அதே கோப்புப் பெயர்கள்) பிரதிபலிக்க வேண்டும். தனிப்பயன் அடைவில் உள்ள எந்தக் கோப்பும் தொடர்புடைய உள்ளமைந்த டெம்ப்ளேட்டை மேலெழுதுகிறது; தனிப்பயன் அடைவில் இல்லாத கோப்புகள் உள்ளமைந்த பதிப்பிற்குப் பின்வாங்குகின்றன. இது பகுதி மேலெழுதல்களை அனுமதிக்கிறது — உதாரணமாக, இயல்புநிலை src/lib.rs மற்றும் Cargo.toml டெம்ப்ளேட்களை வைத்திருந்தபடியே CI பணிப்பாய்வு டெம்ப்ளேட்டை மட்டும் மாற்றுவது.

## அடிக்கடி கேட்கப்படும் கேள்விகள்

**LibMake `cargo new --lib` இலிருந்து எவ்வாறு வேறுபடுகிறது?**
`cargo new --lib` ஒரு குறைந்தபட்ச திட்டத்தை உருவாக்குகிறது — `Cargo.toml` மற்றும் `src/lib.rs` (ஒரே `#[cfg(test)]` தொகுதியைக் கொண்டது) மட்டுமே. LibMake முழு அமைப்பையும் உருவாக்குகிறது — ஒருங்கிணைப்புச் சோதனைகள், அளவீடுகள், CI, CONTRIBUTING.md, இரட்டை-உரிமக் கோப்புகள், மற்றும் சரியாக ஆவணப்படுத்தப்பட்ட src/lib.rs — இடம்பிடிப்பான்களுக்குப் பதிலாக திட்டத்தின் உண்மையான மேனிலைத் தரவுடன் கட்டமைக்கப்பட்டது.

**LibMake ஐ ஏற்கனவே உள்ள Cargo பணியிடத்துடன் பயன்படுத்த முடியுமா?**
LibMake ஒரு தனித்த கிரேட் அடைவை உருவாக்குகிறது. உருவாக்கப்பட்ட கிரேட்டை ஏற்கனவே உள்ள பணியிடத்தில் சேர்க்க, மூல `Cargo.toml` இல் உள்ள பணியிட `members` அணிக்கு வெளியீட்டுப் பாதையைச் சேர்க்கவும். LibMake ஏற்கனவே உள்ள பணியிடக் கோப்புகளை மாற்றாது.

**முதல் உருவாக்கத்திற்குப் பிறகு சட்டக டெம்ப்ளேட்களை நான் புதுப்பிக்க முடியுமா?**
LibMake கோப்புகளை ஒரு முறை உருவாக்குகிறது; அது முன்பு உருவாக்கப்பட்ட திட்டங்களைக் கண்காணிக்கவோ புதுப்பிக்கவோ இல்லை. புதுப்பிக்கப்பட்ட டெம்ப்ளேட்களைப் பயன்படுத்த, பரிந்துரைக்கப்படும் அணுகுமுறை என்னவென்றால், LibMake ஐ ஒரு தற்காலிக அடைவிற்கு மீண்டும் இயக்கி, முடிவை ஏற்கனவே உள்ள கிரேட்டுடன் diff செய்து, விரும்பிய மாற்றங்களைத் தேர்ந்தெடுத்துப் பயன்படுத்துவதாகும்.

**LibMake எந்த Rust பதிப்புகள் மற்றும் MSRV மதிப்புகளை ஆதரிக்கிறது?**
LibMake `--edition` மற்றும் `--rustversion` இற்கு எந்தச் சரத்தையும் ஏற்று அந்த மதிப்புகளை நேரடியாக `Cargo.toml` இல் எழுதுகிறது. குறிப்பிடப்பட்ட பதிப்பு அல்லது MSRV உண்மையான Rust பதிப்பா என்பதை அது சரிபார்க்காது, எனவே சரியான மதிப்புகளை வழங்குவது அழைப்பாளர்களின் பொறுப்பாகும்.

## குறிப்புகள்

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Rust library scaffold generator"
