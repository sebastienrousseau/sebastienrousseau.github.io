# Fuzz targets

Coverage-guided fuzzing (atheris/libFuzzer) for the parsers in this repo that
consume input the author does not fully control: article front-matter, the
romanisation tables that build URL slugs, and the JSON-LD validator that reads
whatever a page emits.

These are the places where a malformed input should produce a clear failure
rather than a crash, a hang, or a silently wrong slug that becomes a live URL.

Run one locally:

```sh
pip install atheris
python3 fuzz/fuzz_slugify.py -atheris_runs=20000
```

`.github/workflows/fuzz.yml` runs each target for a bounded time on pull
requests and nightly. A crash reproducer is uploaded as an artifact.
