# Sigstore — Content Signing Runbook

Every dated article on this site **can** be signed with [Sigstore](https://www.sigstore.dev/) using `cosign`, producing a detached signature + bundle that anyone can verify against the public key. This document explains how to activate it.

The signing pass — `scripts/sigstore_sign.py` — is already wired into `build.sh`. It is a **no-op** until `_data/sigstore/config.json` exists. So the build stays green for any contributor without a cosign setup; signatures only get emitted on the machine that holds the key.

## Why sign content

- **Tamper evidence.** A reader can prove the bytes they fetched are the bytes the author signed. Useful against an MITM-modified mirror, a malicious CDN edge, or an inadvertent re-write.
- **Provenance.** The signature ties the article to an identity (email or DID). When AI engines or aggregators republish, the bundle travels with the content.
- **Transparency-log inclusion.** Sigstore writes signing events to a public, append-only log ([Rekor](https://docs.sigstore.dev/logging/overview/)). Even without trusting the key, anyone can confirm the article was signed at a specific time.

## One-time activation

You need this once per machine that will run the build with signing on.

### 1. Install `cosign`

```sh
brew install cosign      # macOS
# or: go install github.com/sigstore/cosign/v2/cmd/cosign@latest
cosign version
```

### 2. Generate the keypair

```sh
cd _data/sigstore
cosign generate-key-pair
# Prompts for a passphrase. Use a strong one — this is your signing identity.
# Writes cosign.key (private) + cosign.pub (public) into the current dir.
```

`cosign.key` is **gitignored**. Treat it like an SSH private key — never commit, never paste, never email. Store the passphrase in a password manager.

### 3. Publish the public key

The public key needs a stable, fetchable URL so verifiers can find it.

```sh
# Mirror it into the deployed site so verifiers can fetch it from the site itself
mkdir -p docs/sigstore
cp _data/sigstore/cosign.pub docs/sigstore/cosign.pub
# Commit + push:
git add docs/sigstore/cosign.pub
git commit -m "chore(sigstore): publish cosign public key"
git push
```

The published URL will be `https://sebastienrousseau.com/sigstore/cosign.pub`.

### 4. Activate the config

```sh
cp _data/sigstore/config.example.json _data/sigstore/config.json
# Open _data/sigstore/config.json and confirm the identity is correct.
```

The `_data/sigstore/config.json` file is **gitignored** (it's machine-local activation, not source). The example file is committed for reference.

### 5. Set the env vars in your build shell

```sh
export COSIGN_KEY_PATH="$(pwd)/_data/sigstore/cosign.key"
export COSIGN_PASSWORD='your-passphrase-here'   # avoid quotes leaking it to shell history
./build.sh
```

After the build completes, `public/sigstore/<slug>.sig` + `public/sigstore/<slug>.bundle` should exist for every dated article, then get mirrored into `docs/sigstore/` by the build's final `rsync` step.

## Verifying a signature (as a reader)

```sh
# Fetch the article HTML and the bundle
curl -O https://sebastienrousseau.com/2026-05-19-global-wholesale-payments-economics-2026/index.html
curl -O https://sebastienrousseau.com/sigstore/2026-05-19-global-wholesale-payments-economics-2026.bundle

# Fetch the public key
curl -O https://sebastienrousseau.com/sigstore/cosign.pub

# Verify
cosign verify-blob \
  --bundle 2026-05-19-global-wholesale-payments-economics-2026.bundle \
  --key cosign.pub \
  index.html
```

Output should be `Verified OK`. If the article HTML was modified after signing (mirror tampering, MITM rewrite, accidental re-render), verification fails and `cosign` prints a non-zero exit code with the digest mismatch.

## Operational notes

- **Re-signing on rebuild is expected.** Every full `./build.sh` re-renders every page, producing fresh bytes and therefore fresh signatures. The signing pass is idempotent in the sense that running it twice on an unchanged tree produces identical bundles.
- **Footer link.** The site footer carries a "Verify signatures" link to `/sigstore/index.html`. That page is currently a stub; once signing is active, populate it with the verification command above and a one-paragraph explainer.
- **Daily-publishing routine.** When the cloud `/schedule` routine runs `/publish-today`, it does **not** have access to the local cosign key, so PRs opened by the routine ship unsigned. The signing pass runs once the PR is merged + your laptop pulls and rebuilds (or, alternatively, you can run signing after merge on any machine that has the key + env vars set).
- **Key rotation.** To rotate: generate a new keypair, publish both `cosign.pub` (current) and `cosign-prev.pub` (previous) so existing signatures remain verifiable through the transition window. Old signatures stay valid; new ones use the new key.

## Why this matters for AI / agentic consumers

When LLMs republish your content (RAG indexers, summarisers, agent toolchains), the chain of provenance from "the bytes the author published" to "the bytes the agent ingested" is normally broken — agents fetch through opaque caches, intermediate stores, or third-party crawlers. A signed bundle gives the agent a deterministic way to prove that what they served downstream matches the original. Few personal sites do this. It's a small operational lift that ranks high on supply-chain hygiene.
