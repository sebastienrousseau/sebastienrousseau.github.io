---
title: "LibMake: تولیدکننده داربست کتابخانه Rust"
tags: "LibMake, RustCodeGenerator, CargoScaffold, RustLibraryTemplate, TeraTemplating, GitHubActionsRust, CargoAudit, RustAPIGuidelines, BoilerplateGenerator, RustCI, ISO 20022, post-quantum cryptography, AI, Rust, open source"
subtitle: "LibMake: یک تولیدکننده کد Rust که از روز نخست بهترین شیوه‌ها را الزامی می‌کند."
description: "LibMake یک ابزار خط فرمان (CLI) Rust است که یک داربست کامل کتابخانه - Cargo.toml، src/lib.rs همراه با قالب‌های مستندسازی، هارنس‌های آزمون و بنچمارک، و CI مبتنی بر GitHub Actions - را از یک فرمان واحد یا یک فایل پیکربندی نسخه‌بندی‌شده TOML/YAML تولید می‌کند."
date: "Oct 26, 2023"
language: "fa"
locale: "fa_IR"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "ستون‌های سفید غول‌پیکر"
keywords: "LibMake، تولیدکننده کد Rust، داربست cargo، قالب کتابخانه Rust، قالب‌سازی Tera، GitHub Actions برای Rust، cargo-audit، راهنمای API‌ Rust، تولیدکننده کد قالبی، گردش‌کار CI‌ Rust"
---

[**LibMake ⧉**][00] یک CLI و کتابخانه متن‌باز Rust است که یک داربست کامل پروژه کتابخانه را از یک فراخوانی واحد تولید می‌کند. این ابزار شکاف میان `cargo new --lib` (که تنها یک Cargo.toml و src/lib.rs کمینه ایجاد می‌کند) و یک راه‌اندازی کتابخانه آماده تولید (که نیازمند افزودن دستی کامنت‌های مستندسازی، CI، هارنس‌های آزمون، ساختار بنچمارک، CONTRIBUTING.md و فایل‌های مجوز است) را هدف قرار می‌دهد.

این مقاله توضیح می‌دهد که LibMake چه چیزی تولید می‌کند، حالت‌های فایل پیکربندی و CLI چگونه کار می‌کنند، ساختار CI تولیدشده چیست، و سامانه قالب‌سازی چگونه است.

## نصب و کاربرد پایه

LibMake روی [crates.io](https://crates.io/crates/libmake) منتشر شده و از طریق Cargo نصب می‌شود:

```bash
cargo install libmake
```

فراخوانی کمینه CLI یک کتابخانه با نام مشخص را در دایرکتوری جاری تولید می‌کند:

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

پرچم‌های اختیاری دیگر شامل `--categories`، `--keywords`، `--homepage`، `--documentation`، `--readme` و `--build` هستند.

## حالت فایل پیکربندی

برای استفاده تیمی، تمام پرچم‌های CLI را می‌توان در یک فایل پیکربندی TOML بیان کرد:

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

که به این شکل فراخوانی می‌شود:

```bash
libmake --config libmake.toml
```

LibMake همچنین فرمت‌های پیکربندی JSON، YAML و CSV را به‌ترتیب از طریق پرچم‌های `--config-json`، `--config-yaml` و `--config-csv` می‌پذیرد. کامیت‌کردن `libmake.toml` در ریشه مخزن به هر مشارکت‌کننده یک مبنای داربست بازتولیدپذیر می‌دهد، و تغییرات در پیکربندی قالب در diffهای Git قابل مشاهده است.

## ساختار پروژه تولیدشده

یک فراخوانی LibMake چیدمان زیر را ایجاد می‌کند:

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

فایل `src/lib.rs` تولیدشده شامل یک کامنت مستندسازی در سطح crate، دستور `#![deny(missing_docs)]`، دستور `#![doc = include_str!("../README.md")]` برای وارد کردن README به rustdoc، و یک نوع عمومی نمونه (stub) همراه با کامنت مستندسازی مربوطه است. این انتخاب‌ها از الزام «راهنمای API‌ Rust» پیروی می‌کنند که می‌گوید همه آیتم‌های عمومی باید مستندسازی داشته باشند.

فایل `benches/lib_benchmarks.rs` تولیدشده از [Criterion.rs](https://github.com/bheisler/criterion.rs) استفاده می‌کند و نیازمند افزودن `criterion` به‌عنوان یک وابستگی توسعه (dev-dependency) است، که LibMake آن را به‌صورت خودکار در `Cargo.toml` درج می‌کند.

## گردش‌کار CI مبتنی بر GitHub Actions

فایل تولیدشده `.github/workflows/release.yml` روی هر push و هر pull request پنج کار (job) را اجرا می‌کند:

| کار | زنجیره‌ابزار | آنچه بررسی می‌کند |
|---|---|---|
| `test` | stable، beta، nightly (ماتریسی) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (cargo-audit در همان کار نصب می‌شود) |
| `doc` | stable | `cargo doc --no-deps` (در صورت نبود مستندات با خطا مواجه می‌شود) |

کار nightly دارای `continue-on-error: true` است تا یک واپس‌روی (regression) در nightly مانع ادغام‌ها نشود، در حالی که همچنان شکست را در اجرای گردش‌کار نمایان می‌کند.

## قالب‌سازی با Tera

LibMake از موتور قالب [Tera](https://keats.github.io/tera/) — یک نحو شبیه Jinja2 برای Rust — برای رندر کردن همه فایل‌های تولیدشده استفاده می‌کند. هر قالب کل ساختار پیکربندی را به‌عنوان زمینه (context) دریافت می‌کند:

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

دایرکتوری‌های قالب سفارشی از طریق پرچم `--template` پشتیبانی می‌شوند:

```bash
libmake --config libmake.toml --template ./my_templates/
```

دایرکتوری سفارشی باید ساختار قالب پیش‌فرض (همان نام‌های فایل) را بازتاب دهد. هر فایلی که در دایرکتوری سفارشی موجود باشد، قالب داخلی متناظر را بازنویسی می‌کند؛ فایل‌هایی که در دایرکتوری سفارشی موجود نباشند، به نسخه داخلی بازمی‌گردند. این امکان بازنویسی جزئی را فراهم می‌کند — برای مثال، جایگزین کردن تنها قالب گردش‌کار CI در حالی که قالب‌های پیش‌فرض src/lib.rs و Cargo.toml حفظ می‌شوند.

## پرسش‌های پرتکرار

**LibMake چه تفاوتی با `cargo new --lib` دارد؟**
`cargo new --lib` یک پروژه کمینه تنها با `Cargo.toml` و `src/lib.rs` (شامل یک بلوک `#[cfg(test)]` واحد) ایجاد می‌کند. LibMake ساختار کامل را تولید می‌کند — آزمون‌های یکپارچگی، بنچمارک‌ها، CI، CONTRIBUTING.md، فایل‌های مجوز دوگانه، و یک src/lib.rs که به‌درستی مستندسازی شده — که به‌جای مقادیر جای‌گیر (placeholder) با فراداده واقعی پروژه پیکربندی شده است.

**آیا می‌توان از LibMake با یک workspace موجود Cargo استفاده کرد؟**
LibMake یک دایرکتوری crate مستقل تولید می‌کند. برای افزودن crate تولیدشده به یک workspace موجود، مسیر خروجی را به آرایه `members` مربوط به workspace در `Cargo.toml` ریشه اضافه کنید. LibMake فایل‌های موجود workspace را تغییر نمی‌دهد.

**آیا می‌توانم قالب‌های داربست را پس از تولید اولیه به‌روزرسانی کنم؟**
LibMake فایل‌ها را یک بار تولید می‌کند؛ پروژه‌های پیش‌تر تولیدشده را ردیابی یا به‌روزرسانی نمی‌کند. برای اتخاذ قالب‌های به‌روزشده، رویکرد توصیه‌شده این است که LibMake را دوباره در یک دایرکتوری موقت اجرا کنید و نتیجه را با crate موجود مقایسه (diff) کنید و تغییرات دلخواه را به‌صورت گزینشی اعمال کنید.

**LibMake از چه نسخه‌ها (edition) و مقادیر MSRV زبان Rust پشتیبانی می‌کند؟**
LibMake هر رشته‌ای را برای `--edition` و `--rustversion` می‌پذیرد و مقادیر را مستقیماً در `Cargo.toml` می‌نویسد. این ابزار اعتبارسنجی نمی‌کند که آیا نسخه یا MSRV مشخص‌شده یک نسخه واقعی Rust است یا خیر، بنابراین مسئولیت تأمین مقادیر درست بر عهده فراخوانان است.

## منابع

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Rust library scaffold generator"
