---
title: "LibMake: Γεννήτρια Σκελετού Βιβλιοθηκών Rust"
tags: "LibMake, RustCodeGenerator, CargoScaffold, RustLibraryTemplate, TeraTemplating, GitHubActionsRust, CargoAudit, RustAPIGuidelines, BoilerplateGenerator, RustCI, ISO 20022, post-quantum cryptography, AI, Rust, open source"
subtitle: "LibMake: μια γεννήτρια κώδικα Rust που επιβάλλει τις βέλτιστες πρακτικές από την πρώτη μέρα."
description: "Το LibMake είναι ένα εργαλείο CLI σε Rust που παράγει έναν πλήρη σκελετό βιβλιοθήκης - Cargo.toml, src/lib.rs με πρότυπα τεκμηρίωσης, υποδομές δοκιμών και συγκριτικών μετρήσεων, και CI μέσω GitHub Actions - από μία μόνο εντολή ή ένα εκδοσιοποιημένο αρχείο ρυθμίσεων TOML/YAML."
date: "Oct 26, 2023"
language: "el"
locale: "el_GR"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "Γιγάντιοι λευκοί κίονες"
keywords: "LibMake, γεννήτρια κώδικα Rust, σκελετός cargo, πρότυπο βιβλιοθήκης Rust, δημιουργία προτύπων Tera, GitHub Actions Rust, cargo-audit, Οδηγίες API της Rust, γεννήτρια boilerplate, ροή εργασίας CI για Rust"
---

Το [**LibMake ⧉**][00] είναι ένα CLI και μια βιβλιοθήκη ανοιχτού κώδικα σε Rust που παράγει έναν πλήρη σκελετό έργου βιβλιοθήκης από μία μόνο κλήση. Στοχεύει στο κενό ανάμεσα στο `cargo new --lib` (το οποίο δημιουργεί μόνο ένα ελάχιστο Cargo.toml και src/lib.rs) και σε μια έτοιμη για παραγωγή διαμόρφωση βιβλιοθήκης (η οποία απαιτεί τη χειροκίνητη προσθήκη σχολίων τεκμηρίωσης, CI, υποδομών δοκιμών, δομής συγκριτικών μετρήσεων, CONTRIBUTING.md και αρχείων άδειας χρήσης).

Αυτό το άρθρο περιγράφει τι παράγει το LibMake, πώς λειτουργούν οι λειτουργίες αρχείου ρυθμίσεων και CLI, τη δομή του παραγόμενου CI και το σύστημα δημιουργίας προτύπων.

## Εγκατάσταση και βασική χρήση

Το LibMake δημοσιεύεται στο [crates.io](https://crates.io/crates/libmake) και εγκαθίσταται μέσω του Cargo:

```bash
cargo install libmake
```

Η ελάχιστη κλήση του CLI παράγει μια επώνυμη βιβλιοθήκη στον τρέχοντα κατάλογο:

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

Πρόσθετα προαιρετικά ορίσματα περιλαμβάνουν τα `--categories`, `--keywords`, `--homepage`, `--documentation`, `--readme` και `--build`.

## Λειτουργία αρχείου ρυθμίσεων

Για χρήση σε ομάδες, όλα τα ορίσματα του CLI μπορούν να εκφραστούν σε ένα αρχείο ρυθμίσεων TOML:

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

Καλείται ως:

```bash
libmake --config libmake.toml
```

Το LibMake δέχεται επίσης μορφές ρυθμίσεων JSON, YAML και CSV μέσω των ορισμάτων `--config-json`, `--config-yaml` και `--config-csv` αντίστοιχα. Η υποβολή του `libmake.toml` στη ρίζα του αποθετηρίου παρέχει σε κάθε συνεισφέροντα μια αναπαραγώγιμη βάση σκελετού, ενώ οι αλλαγές στη διαμόρφωση των προτύπων είναι ορατές στα Git diffs.

## Δομή του παραγόμενου έργου

Μια κλήση του LibMake δημιουργεί την ακόλουθη διάταξη:

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

Το παραγόμενο `src/lib.rs` περιλαμβάνει ένα σχόλιο τεκμηρίωσης σε επίπεδο crate, `#![deny(missing_docs)]`, `#![doc = include_str!("../README.md")]` για να ενσωματώσει το README στο rustdoc, καθώς και έναν σκελετό δημόσιου τύπου με ένα σχετικό σχόλιο τεκμηρίωσης. Αυτές οι επιλογές ακολουθούν την απαίτηση των Οδηγιών API της Rust ότι όλα τα δημόσια στοιχεία πρέπει να διαθέτουν τεκμηρίωση.

Το παραγόμενο `benches/lib_benchmarks.rs` χρησιμοποιεί το [Criterion.rs](https://github.com/bheisler/criterion.rs) και απαιτεί την προσθήκη του `criterion` ως εξάρτηση ανάπτυξης (dev-dependency), την οποία το LibMake εισάγει αυτόματα στο `Cargo.toml`.

## Ροή εργασίας CI με GitHub Actions

Το παραγόμενο `.github/workflows/release.yml` εκτελεί πέντε εργασίες σε κάθε push και pull request:

| Εργασία | Αλυσίδα εργαλείων | Τι ελέγχει |
|---|---|---|
| `test` | stable, beta, nightly (matrix) | `cargo test --all-features` |
| `clippy` | stable | `cargo clippy -- -D warnings` |
| `fmt` | stable | `cargo fmt --check` |
| `audit` | stable | `cargo audit` (το cargo-audit εγκαθίσταται στην εργασία) |
| `doc` | stable | `cargo doc --no-deps` (αποτυγχάνει σε ελλιπή τεκμηρίωση) |

Η εργασία nightly έχει `continue-on-error: true`, ώστε μια παλινδρόμηση στη nightly να μην εμποδίζει τις συγχωνεύσεις, ενώ παράλληλα εμφανίζει την αποτυχία στην εκτέλεση της ροής εργασίας.

## Δημιουργία προτύπων με Tera

Το LibMake χρησιμοποιεί τη μηχανή προτύπων [Tera](https://keats.github.io/tera/) — μια σύνταξη τύπου Jinja2 για τη Rust — για την απόδοση όλων των παραγόμενων αρχείων. Κάθε πρότυπο λαμβάνει ολόκληρη τη δομή ρυθμίσεων ως πλαίσιο (context):

```
{{ name }}            → my_library
{{ author }}          → Jane Smith
{{ edition }}         → 2021
{{ description }}     → A Rust library for doing useful things
```

Υποστηρίζονται προσαρμοσμένοι κατάλογοι προτύπων μέσω του ορίσματος `--template`:

```bash
libmake --config libmake.toml --template ./my_templates/
```

Ο προσαρμοσμένος κατάλογος πρέπει να αντικατοπτρίζει την προεπιλεγμένη δομή προτύπων (τα ίδια ονόματα αρχείων). Οποιοδήποτε αρχείο υπάρχει στον προσαρμοσμένο κατάλογο υπερισχύει του αντίστοιχου ενσωματωμένου προτύπου· τα αρχεία που δεν υπάρχουν στον προσαρμοσμένο κατάλογο επανέρχονται στην ενσωματωμένη έκδοση. Αυτό επιτρέπει μερικές αντικαταστάσεις — για παράδειγμα, την αντικατάσταση μόνο του προτύπου της ροής εργασίας CI, διατηρώντας παράλληλα τα προεπιλεγμένα πρότυπα src/lib.rs και Cargo.toml.

## Συχνές ερωτήσεις

**Σε τι διαφέρει το LibMake από το `cargo new --lib`;**
Το `cargo new --lib` δημιουργεί ένα ελάχιστο έργο με μόνο `Cargo.toml` και `src/lib.rs` (που περιέχει ένα μόνο μπλοκ `#[cfg(test)]`). Το LibMake παράγει την πλήρη δομή — δοκιμές ολοκλήρωσης, συγκριτικές μετρήσεις, CI, CONTRIBUTING.md, αρχεία διπλής άδειας χρήσης και ένα σωστά τεκμηριωμένο src/lib.rs — διαμορφωμένη με τα πραγματικά μεταδεδομένα του έργου αντί για δεσμευτικά κείμενα (placeholders).

**Μπορεί το LibMake να χρησιμοποιηθεί με έναν υπάρχοντα χώρο εργασίας Cargo;**
Το LibMake παράγει έναν αυτόνομο κατάλογο crate. Για να προσθέσετε το παραγόμενο crate σε έναν υπάρχοντα χώρο εργασίας, προσθέστε τη διαδρομή εξόδου στον πίνακα `members` του χώρου εργασίας στο ριζικό `Cargo.toml`. Το LibMake δεν τροποποιεί υπάρχοντα αρχεία χώρου εργασίας.

**Μπορώ να ενημερώσω τα πρότυπα του σκελετού μετά την αρχική δημιουργία;**
Το LibMake παράγει αρχεία μία φορά· δεν παρακολουθεί ούτε ενημερώνει έργα που έχουν ήδη παραχθεί. Για να υιοθετήσετε ενημερωμένα πρότυπα, η συνιστώμενη προσέγγιση είναι να εκτελέσετε ξανά το LibMake σε έναν προσωρινό κατάλογο και να συγκρίνετε (diff) το αποτέλεσμα με το υπάρχον crate, εφαρμόζοντας επιλεκτικά τις επιθυμητές αλλαγές.

**Ποιες εκδόσεις (editions) της Rust και ποιες τιμές MSRV υποστηρίζει το LibMake;**
Το LibMake δέχεται οποιαδήποτε συμβολοσειρά για τα `--edition` και `--rustversion` και γράφει τις τιμές απευθείας στο `Cargo.toml`. Δεν επικυρώνει αν η καθορισμένη έκδοση ή το MSRV αντιστοιχούν σε πραγματική έκδοση της Rust, οπότε οι καλούντες είναι υπεύθυνοι για την παροχή σωστών τιμών.

## Αναφορές

1. Rousseau, S. *LibMake — A code generator to reduce repetitive tasks and build high-quality Rust libraries*. GitHub, 2023. https://github.com/sebastienrousseau/libmake
2. The Rust Programming Language. *Rust API Guidelines*. GitHub, 2023. https://rust-lang.github.io/api-guidelines/
3. The Cargo Book. *Package Layout*. The Rust Programming Language, 2023. https://doc.rust-lang.org/cargo/guide/project-layout.html
4. Keats, V. et al. *Tera — A template engine inspired by Jinja2 and Django templates*. GitHub, 2023. https://keats.github.io/tera/

[00]: https://github.com/sebastienrousseau/libmake "LibMake — Rust library scaffold generator"
