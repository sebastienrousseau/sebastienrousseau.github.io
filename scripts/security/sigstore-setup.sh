#!/usr/bin/env bash
# Activate (or re-activate) Sigstore signing for this repo, end-to-end.
#
# Idempotent:
#   - If a keypair already exists and passes verification, just runs the
#     signing pass.
#   - If verification fails, offers to regenerate the keypair.
#   - If no keypair exists, generates one.
#
# Usage: scripts/security/sigstore-setup.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SIGSTORE_DIR="$REPO_ROOT/_data/sigstore"
KEY_FILE="$SIGSTORE_DIR/cosign.key"
PUB_FILE="$SIGSTORE_DIR/cosign.pub"
PUB_PUBLISHED="$REPO_ROOT/docs/sigstore/cosign.pub"
CONFIG="$SIGSTORE_DIR/config.json"
CONFIG_TEMPLATE="$SIGSTORE_DIR/config.example.json"

# --- helpers ------------------------------------------------------------

say() { printf '\n\033[1m▸ %s\033[0m\n' "$*"; }
ok()  { printf '  \033[32m✓\033[0m %s\n' "$*"; }
warn(){ printf '  \033[33m!\033[0m %s\n' "$*"; }
die() { printf '  \033[31m✗\033[0m %s\n' "$*" >&2; exit 1; }

prompt_passphrase() {
  # Securely read a passphrase into $COSIGN_PASSWORD without echoing it.
  printf '  cosign passphrase: '
  read -rs COSIGN_PASSWORD
  echo
  [ -n "$COSIGN_PASSWORD" ] || die "passphrase cannot be empty"
  export COSIGN_PASSWORD
}

verify_passphrase() {
  # Round-trip: sign a tiny test blob with the key + current
  # COSIGN_PASSWORD. If it succeeds, the password is correct.
  local tmp_blob tmp_bundle
  tmp_blob=$(mktemp)
  tmp_bundle=$(mktemp)
  echo "verify" > "$tmp_blob"
  if cosign sign-blob \
        --key "$KEY_FILE" \
        --bundle "$tmp_bundle" \
        --yes "$tmp_blob" >/dev/null 2>&1; then
    rm -f "$tmp_blob" "$tmp_bundle"
    return 0
  fi
  rm -f "$tmp_blob" "$tmp_bundle"
  return 1
}

# --- step 1: cosign installed ------------------------------------------

say "Checking cosign"
command -v cosign >/dev/null || die "cosign not on PATH. Install: brew install cosign"
ok "cosign $(cosign version --json 2>/dev/null | grep -oE '"GitVersion": *"[^"]+"' | head -1 | cut -d'"' -f4)"

# --- step 2: ensure scaffold directories --------------------------------

say "Preparing _data/sigstore + docs/sigstore"
mkdir -p "$SIGSTORE_DIR" "$REPO_ROOT/docs/sigstore"
ok "directories present"

# --- step 3: keypair --------------------------------------------------

say "Keypair check"
if [ -f "$KEY_FILE" ] && [ -f "$PUB_FILE" ]; then
  ok "existing keypair found at _data/sigstore/{cosign.key,cosign.pub}"
  prompt_passphrase
  if verify_passphrase; then
    ok "passphrase matches existing key"
  else
    warn "passphrase does not match existing key"
    printf '  Regenerate keypair? Old signatures (if any) will not verify against the new key. [y/N]: '
    read -r ans
    if [[ "$ans" =~ ^[Yy]$ ]]; then
      rm -f "$KEY_FILE" "$PUB_FILE" "$PUB_PUBLISHED"
      ok "removed old keypair"
    else
      die "aborted — re-run with the correct passphrase"
    fi
  fi
fi

if [ ! -f "$KEY_FILE" ]; then
  say "Generating new keypair"
  if [ -z "${COSIGN_PASSWORD:-}" ]; then
    prompt_passphrase
  fi
  # cosign reads COSIGN_PASSWORD from env to encrypt the new key.
  ( cd "$SIGSTORE_DIR" && cosign generate-key-pair >/dev/null )
  ok "wrote _data/sigstore/cosign.key (encrypted, gitignored)"
  ok "wrote _data/sigstore/cosign.pub"
fi

# --- step 4: publish public key into deployed tree ---------------------

say "Publishing public key into docs/sigstore/"
cp "$PUB_FILE" "$PUB_PUBLISHED"
ok "docs/sigstore/cosign.pub up to date"

# --- step 5: activate config ------------------------------------------

say "Activating config"
if [ ! -f "$CONFIG" ]; then
  [ -f "$CONFIG_TEMPLATE" ] || die "missing $CONFIG_TEMPLATE — re-pull main"
  cp "$CONFIG_TEMPLATE" "$CONFIG"
  ok "copied config.example.json → config.json"
else
  ok "config.json already present"
fi

# --- step 6: run the build with signing on -----------------------------

export COSIGN_KEY_PATH="$KEY_FILE"
say "Running ./build.sh (signing every dated article)"
if ./build.sh >/tmp/sigstore-build.log 2>&1; then
  ok "build succeeded — log at /tmp/sigstore-build.log"
else
  warn "build returned non-zero. Tail:"
  tail -20 /tmp/sigstore-build.log >&2
  die "build failed — see /tmp/sigstore-build.log"
fi

# --- step 7: verify outputs ------------------------------------------

say "Verifying signature output"
n=$(find docs/sigstore -name '*.bundle' -type f 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -lt 1 ]; then
  die "no .bundle files in docs/sigstore — signing did not run. Check $CONFIG and the sigstore line of /tmp/sigstore-build.log"
fi
ok "$n signed bundle(s) in docs/sigstore/"

# --- step 8: commit prompt -----------------------------------------

say "Ready to commit"
echo "  Files staged for review:"
git status --short docs/sigstore/ _data/sigstore/.gitignore _data/sigstore/config.example.json project-docs/SIGSTORE.md 2>/dev/null | sed 's/^/    /'
echo
echo "  To publish:"
echo "    git add docs/sigstore/ _data/sigstore/.gitignore _data/sigstore/config.example.json project-docs/SIGSTORE.md"
echo "    git commit -m 'chore(sigstore): activate signing — per-article bundles'"
echo "    git push"
echo
echo "  Then run scripts/security/sigstore-setup.sh again any time you rebuild — it's idempotent."

unset COSIGN_PASSWORD
ok "passphrase scrubbed from shell env"
