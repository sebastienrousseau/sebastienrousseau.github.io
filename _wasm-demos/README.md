# WASM lab demos

> Last Updated: June 4, 2026

These directories house Rust projects that compile to WebAssembly for the Sebastien Rousseau web platform. Each module demonstrates interactive tools directly in the user browser.

## Layout

The folder structure separates the Rust source code from the HTML wrapper to make the build pipeline simple. The Cargo configuration tracks the compilation settings and the web folder loads the binary.

## Build

The main build script compiles these crates when you run the site build tool. You can also build each crate manually from its own directory.

## CSP

Each demo page runs with a tight security policy that allows compiled WebAssembly code to execute safely. The test script checks these headers to keep the page secure.

## Adding a new demo

To add a new demo, create a Rust crate with exported functions and add a companion page in the web folder. The build tool will find and compile the project automatically.

## hsh-demo

The first demo uses standard hash functions to show the cryptographic tools in the browser. When the main library supports WebAssembly, the crate can import it.
