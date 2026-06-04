<!-- SPDX-License-Identifier: Apache-2.0 -->

# WASM lab demos

Each subdirectory under `_wasm-demos/` is a self-contained Rust crate that
compiles to WebAssembly and ships an interactive companion page for one
of the libraries published under [github.com/sebastienrousseau](https://github.com/sebastienrousseau).

The pattern is intentionally minimal so it scales to the rest of the
portfolio (`pain001`, `kyberlib`, `dtt`, etc.) by copy-paste.

## Layout

```text
_wasm-demos/
  <name>/
    Cargo.toml          ← wasm-bindgen + the library being demoed
    src/lib.rs          ← #[wasm_bindgen] exports
    web/                ← standalone HTML/JS/CSS shell, no build step
      index.html
      demo.js
      demo.css
    pkg/                ← wasm-pack output, gitignored
```

## Build

`build.sh` does this for you (locally and in CI). To rebuild a single
crate by hand:

```sh
cd _wasm-demos/hsh-demo
wasm-pack build --target web --release
```

Outputs land under `pkg/`. The top-level build copies the artefacts plus
the `web/` shell into `public/labs/<name>/`, where the standard
postbuild + CSP pipeline takes over.

## CSP

The lab pages run under a hand-written meta-CSP that's tight by default:

```text
default-src 'self';
script-src 'self' 'wasm-unsafe-eval';
style-src 'self';
base-uri 'self';
object-src 'none';
frame-ancestors 'none';
form-action 'none';
upgrade-insecure-requests
```

`'wasm-unsafe-eval'` is the only loosening — it permits
`WebAssembly.instantiate()` while keeping arbitrary JS-eval disallowed.
The strict CSP test (`tests/validation/test_csp_strict.py`) tokenises the policy
and rejects only `'unsafe-eval'` as an exact token, so `'wasm-unsafe-eval'`
passes cleanly.

## Adding a new demo

1. Create `_wasm-demos/<your-crate>/{Cargo.toml,src/lib.rs}`.
2. Expose your Rust functions with `#[wasm_bindgen]`.
3. Copy `_wasm-demos/hsh-demo/web/` and adapt the HTML/JS to your API.
4. `./build.sh` — the rest is automatic.
5. Link to `/labs/<your-crate>/` from the relevant article in `_posts/`.

## hsh-demo

Wraps `sha2`, `blake3`, and `argon2` (the wasm-compatible siblings of the
algorithms exposed by the published [`hsh`](https://crates.io/crates/hsh)
crate). When `hsh` itself ships wasm-compatible transitive deps, the
`Cargo.toml` can swap to `hsh = "*"` and re-export from there without
touching the web shell.
