<h1 align="center">Web lab demos</h1>

<p align="center">
  Interactive, client-side demos for sebastienrousseau.com — Rust → WebAssembly
  and vanilla JavaScript, each sandboxed under a strict CSP.
</p>

---

## Layout

Each demo lives in its own directory. JavaScript demos hold plain web assets; Rust demos add a `Cargo.toml` and `src/`.

## Build flow

`build.sh` compiles and stages every demo: `wasm-pack` for Rust crates, direct copy for JavaScript.

## CSP

Each page runs under a tight policy. WebAssembly demos add `'wasm-unsafe-eval'`; JavaScript demos run with no dynamic-code rights.

## Available labs

| Lab | Stack | What it shows |
| :--- | :--- | :--- |
| `hsh-demo` | Rust + WASM | In-browser multi-algorithm hashing |
| `pqc-key-sizes` | JavaScript | Post-quantum key-size comparison |

## License

Licensed under [Apache-2.0](../LICENSE).

<p align="right"><a href="#web-lab-demos">Back to Top</a></p>
