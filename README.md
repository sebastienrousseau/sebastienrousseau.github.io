# SebastienRousseau.com - Official Website 🌏

Welcome to the repository for
[sebastienrousseau.com](https://sebastienrousseau.com), the digital presence of
[**Sebastien Rousseau**](https://github.com/sebastienrousseau).

Dive deep into explorations and applications of Artificial Intelligence (AI),
Post-Quantum Cryptography (PQC), and Blockchain technology, all tailored to
craft the future of banking and financial services.

## Quick Start Guide

Setting up and running the website locally is easy and quick with the
[Shokunin Static Site Generator (SSG)][00].

### Prerequisites

Ensure you have the **Rust toolchain** installed. If not, follow the guide on
the [Rust website][01] to set it up.

### Installation & Usage

1. Install Shokunin SSG:

```shell
cargo install ssg
```

2. Clone the repository

```shell
git clone https://github.com/sebastienrousseau/sebastienrousseau.github.io.git
```

3. Generate the static site for sebastienrousseau.com

```shell
ssg -n=docs -c=_posts -t=_layouts -o=output -s=public
```


[00]: https://shokunin.one "Shokunin Static Site Generator"
[01]: https://www.rust-lang.org/learn/get-started "Rust"
