//! In-browser companion to the `hsh` crate — wraps the same algorithm
//! family (SHA-256, BLAKE3, Argon2id) for live interactive demos on the
//! hsh project page. The published `hsh` crate cannot yet be linked
//! against here because two of its transitive dependencies don't build
//! for `wasm32-unknown-unknown` (bcrypt's getrandom binding + argon2rs
//! age); the modern equivalents wrap the same algorithms with
//! wasm-friendly crates.

use argon2::{password_hash::{PasswordHasher, SaltString}, Argon2};
use rand_core::OsRng;
use sha2::{Digest, Sha256};
use wasm_bindgen::prelude::*;

/// SHA-256 hex digest of an arbitrary UTF-8 string.
#[wasm_bindgen]
pub fn sha256_hex(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    hex::encode(hasher.finalize())
}

/// BLAKE3 hex digest of an arbitrary UTF-8 string.
#[wasm_bindgen]
pub fn blake3_hex(input: &str) -> String {
    blake3::hash(input.as_bytes()).to_hex().to_string()
}

/// Argon2id password hash in PHC string format. Salt is generated from
/// `OsRng`; in the browser `getrandom` plugs into `crypto.getRandomValues`
/// via the `js` feature.
#[wasm_bindgen]
pub fn argon2id_phc(password: &str) -> Result<String, JsValue> {
    let salt = SaltString::generate(&mut OsRng);
    Argon2::default()
        .hash_password(password.as_bytes(), &salt)
        .map(|h| h.to_string())
        .map_err(|e| JsValue::from_str(&format!("{e}")))
}
