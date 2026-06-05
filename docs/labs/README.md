# Web lab demos

> Last Updated: June 5, 2026

This directory houses web lab demos for the Sebastien Rousseau web platform, which features compiled Rust WebAssembly code and client JavaScript tools.

## Layout

The folder layout puts each demo inside its own directory. JavaScript tools stay in simple folders with basic web assets, while Rust tools contain Cargo files and source code.

## Build flow

The build script compiles and copies all files when you build the site. The builder runs wasm-pack for Rust code and copies JavaScript files directly.

## CSP rules

Each page runs under a tight security policy to keep visitors safe. WebAssembly needs the unsafe-eval rule, while other scripts run without dynamic code rights.

## Available labs

We ship several browser tools to show cryptographic ideas.

- **hsh-demo:** A Rust hashing tool that runs locally in the browser with WebAssembly.
- **pqc-key-sizes:** A JavaScript tool that computes post-quantum key sizes for comparison.
