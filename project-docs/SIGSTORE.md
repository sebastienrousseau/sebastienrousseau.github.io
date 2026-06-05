# Sigstore — Content Signing Runbook

> Last Updated: June 4, 2026

Every dated article on this Shokunin static site is signed using Sigstore, and this runbook explains how to setup, use, and check these signatures.

The signing pass — `scripts/sigstore_sign.py` — is wired into the build script. It is a no-op until `_data/sigstore/config.json` exists, which means the build stays green for any writer without a key setup. Signatures only get made on the machine that holds the private key.

## Why sign content

Signatures check the truth and safety of published articles across the Sebastien Rousseau web platform, which is built on the Shokunin static site generator.

- **Tamper proof.** A reader can prove that the files they got are the files the author signed, protecting against edge server changes.
- **Source proof.** The signature ties the article to an identity, which helps when AI search engines or web crawlers read your articles.
- **Public log proof.** Sigstore writes signing events to a public log, and this allows anyone to verify that the article existed at that time.

## One-time activation

Setting up the signing keys establishes the signature identity on your local computer. You need this once per machine that will run the build with signing enabled.

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

The key file is ignored by git, and you should treat it like a private key. Store the password safely in a password manager.

### 3. Publish the public key

```sh
# Mirror it into the deployed site so verifiers can fetch it from the site itself
mkdir -p docs/sigstore
cp _data/sigstore/cosign.pub docs/sigstore/cosign.pub
# Commit + push:
git add docs/sigstore/cosign.pub
git commit -m "chore(sigstore): publish cosign public key"
git push
```

The public key is served at a stable link so that external readers can easily verify the signatures.

### 4. Activate the config

```sh
cp _data/sigstore/config.example.json _data/sigstore/config.json
# Open _data/sigstore/config.json and confirm the identity is correct.
```

The config file is ignored by git because it contains local settings. The example config remains committed for reference.

### 5. Set the env vars in your build shell

```sh
export COSIGN_KEY_PATH="$(pwd)/_data/sigstore/cosign.key"
export COSIGN_PASSWORD='your-passphrase-here'   # avoid quotes leaking it to shell history
./build.sh
```

After the build completes, the signature and bundle files will be generated for every article.

## Verifying a signature (as a reader)

Readers check the truth of signed articles by running the cosign tool against the public key bundle.

```sh
# Fetch the article HTML and the bundle
curl -O https://sebastienrousseau.com/2026-05-19-global-wholesale-payments-economics-2026/index.html
curl -O https://sebastienrousseau.com/sigstore/2026-05-19-global-wholesale-payments-economics-2026.bundle

# Fetch the public key
curl -O https://sebastienrousseau.com/sigstore/cosign.pub

# Verify
cosign verify-blob   --bundle 2026-05-19-global-wholesale-payments-economics-2026.bundle   --key cosign.pub   index.html
```

The output should confirm the signature, but if the content was changed after signing, the check tool will fail.

## Operational notes

Operational steps for the Shokunin static site generator define how signatures are managed during automated builds.

- **Re-signing on rebuild is expected.** Every full build re-renders every page, which produces fresh files and new signatures.
- **Footer link.** The site footer carries a check link, which points users to the main explanation page.
- **Daily-publishing routine.** The automated daily routine does not sign articles because it lacks access to your private key.
- **Key rotation.** When rotating keys, keep both the old and new public keys published so old signatures remain valid.

## Why this matters for AI / agentic consumers

Artificial intelligence agents and language models use signatures to verify original content source.

When models republish your content, the link from the original author is usually broken. A signed bundle gives the agent a clear way to prove the safety of the read data. This represents a simple step that greatly improves content safety.
