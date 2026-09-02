# CS-IEF-08 — Ω Multi-Surface Distribution Compiler

Status: canonical specification layer / reference compiler contract

## Purpose

Compile one canonical CodexStation IEF source graph into deterministic, integrity-bound distributions for heterogeneous public-LLM and portable surfaces without allowing surface-specific adapters to rewrite constitutional semantics.

`Canonical Ω + SurfaceProfile + CapabilityManifest + SourceManifest -> DistributionBundle`

A distribution is a projection, not an independent fork of the canon.

## Canonical Ω composition

`Ω = K + A + IEF + P + S + X + D + I`

Where:

- `K` — constitutional/invariant kernel;
- `A` — architecture crystal;
- `IEF` — execution/policy/evidence semantics;
- `P` — provider/tool capability manifest;
- `S` — explicit source graph;
- `X` — target surface adapter;
- `D` — optional removable domain crystals;
- `I` — version/integrity metadata.

## Compilation invariant

For canonical invariant set `K` and target surface `s`:

`SEMANTICS_K(COMPILE(Ω,s)) == SEMANTICS_K(Ω)`

Surface projection may reduce available features or representation density. It may not change authority, security, provenance, assurance, witness, or claim-boundary semantics.

## Inputs

Every compile operation MUST bind:

- canonical Ω manifest/version;
- canonical component digests;
- compiler id/version;
- target surface profile id/version;
- target capability manifest and digest;
- source manifest and digest;
- selected domain crystal ids/digests;
- build policy/version;
- output format policy;
- deterministic compile options.

Ambient, undeclared tool availability is forbidden as a compilation input.

## Outputs

A successful compile emits `DistributionBundle` containing:

- distribution id/version;
- target surface;
- canonical Ω version;
- compiler version;
- source graph digest;
- capability manifest digest;
- surface profile digest;
- selected component manifest;
- generated artifacts[] with path/type/digest;
- omissions[];
- capability degradations[];
- unsupported capabilities[];
- constitutional equivalence result;
- bundle digest.

A compile that cannot preserve mandatory constitutional semantics MUST fail closed.

## Surface classes

Initial profiles:

- `chatgpt`
- `gemini`
- `gemini-notebook`
- `portable`

Additional surfaces may be introduced by adding profile definitions without changing canonical Ω semantics.

## Capability-aware projection

The compiler MUST distinguish:

1. canonical semantics that must always be represented;
2. capabilities available on the target surface;
3. capabilities absent on the target surface;
4. capabilities available only through connected tools/providers;
5. capabilities deliberately excluded by the build policy.

Unavailable capability MUST be represented as unavailable/unsupported or omitted with an explicit omission record. The distribution MUST NOT simulate operational capability through prose.

`CAPABILITY_ABSENT != CAPABILITY_SIMULATED`

## Surface adapter constraints

A SurfaceProfile MAY define:

- preferred artifact layout;
- instruction density/partitioning;
- source presentation strategy;
- supported tool-routing metadata;
- source-link/reference behavior;
- context-size budget;
- chunking strategy;
- optional human-readable index files;
- target-specific bootstrap instructions.

A SurfaceProfile MUST NOT:

- weaken security invariants;
- grant provider/effect authority;
- raise EAC or reproducibility claims;
- remove claim boundaries;
- alter witness semantics;
- embed secrets;
- convert unavailable capabilities into claimed available capabilities.

## Canonical and generated zones

The repository/distribution model SHOULD distinguish:

- `canonical/` — immutable inputs or canonical references;
- `generated/` — compiler outputs;
- `surface/` — target-specific adapter/configuration;
- `sources/` — source manifests;
- `capabilities/` — declared runtime/tool capability manifests;
- `integrity/` — bundle/artifact digests and compile receipt.

Generated artifacts MUST NOT be edited as the new source of truth. Changes are made upstream in canonical components or SurfaceProfile and recompiled.

## Source graph

Source entries SHOULD include:

- source id;
- type;
- URI/repository;
- immutable ref/digest where required;
- role;
- trust class;
- license;
- ingestion policy;
- required/optional status;
- compatibility/review status.

Gemini Notebook projection is source-first and SHOULD expose repository/source references directly where the target supports them.

## Surface profiles

### ChatGPT

Emphasize concise constitutional kernel, tool routing, policy membrane, source discipline, execution/evidence semantics, and connected-surface capability negotiation. Connected tools are runtime facts and are not embedded as permanent assumptions.

### Gemini

Emphasize portable constitutional and architecture crystals, provider-neutral semantics, source graph references, explicit capability negotiation, and deterministic handoff state.

### Gemini Notebook

Source-first projection. Prefer direct public-source manifests, repository URLs/refs, specs, schemas, release notes, and compact instructions that define how the sources are to be interpreted. Minimize dependence on conversational memory.

### Portable

Emit a self-describing filesystem package suitable for import into an arbitrary capable LLM or local environment. Portable output MUST function as documentation/source substrate even when no execution provider is available.

## Portable layout

Recommended baseline:

`00_CORE/`
`01_ARCHITECTURE/`
`02_IEF/`
`03_CAPABILITIES/`
`04_SOURCES/`
`05_DOMAIN_CRYSTALS/`
`06_SURFACE/`
`MANIFEST.yaml`
`VERSION`
`INTEGRITY.sha256`

## Drift detection

The compiler MUST detect:

- generated artifact modified without canonical input change;
- source ref change;
- surface profile change;
- capability manifest change;
- canonical component digest change;
- compiler version change.

Every such change produces a new distribution digest.

A generated bundle whose recorded inputs no longer match current canonical inputs is `STALE` and MUST NOT be represented as current.

## Constitutional equivalence gate

Each SurfaceProfile defines mandatory invariant identifiers. Compile succeeds only if all mandatory invariant ids are present in the generated semantic manifest.

`K_required ⊆ K_emitted`

Absence or mutation of any mandatory invariant results in `CONSTITUTIONAL_DRIFT` rejection.

This gate checks declared semantic identity/invariant coverage; it is not a formal proof that arbitrary natural-language paraphrases are semantically identical. High-assurance surfaces SHOULD prefer canonical text fragments or structured invariant objects rather than free paraphrase.

## Compilation receipt

Every build emits an append-only `DistributionCompileReceipt` binding:

- canonical Ω manifest digest;
- component digests;
- source manifest digest;
- capability manifest digest;
- SurfaceProfile digest;
- compiler/version;
- selected domain crystals;
- omissions/degradations;
- artifact digests;
- constitutional-equivalence gate result;
- final bundle digest.

The receipt may be bridged into CS-IEF-07 witness semantics as a build/evidence record.

## Security and privacy

1. Secrets are never compiler inputs that can enter generated artifacts.
2. Private/internal sources are excluded from public distributions unless explicitly promoted/redacted under policy.
3. Provider/tool availability is declared, not inferred from prose.
4. Capability manifests are runtime/build facts and carry scope/freshness metadata.
5. Generated public source manifests MUST respect source licensing and disclosure constraints.
6. A public bundle MUST be useful without access to the private lab repository.

## Determinism

Given equal canonical inputs, compiler version, SurfaceProfile, CapabilityManifest, SourceManifest, build policy, and selected domain crystals, generated artifact bytes/digests SHOULD be reproducible.

Non-deterministic metadata such as build wall-clock timestamps MUST be excluded from content-addressed semantic digests or normalized into explicitly non-semantic receipt fields.

## Reference implementation boundary

The public reference compiler may demonstrate:

- canonical manifest normalization;
- invariant coverage checking;
- capability projection;
- explicit omission generation;
- deterministic artifact manifests;
- bundle digest generation;
- stale/drift detection primitives.

It does not claim that current ChatGPT/Gemini product capabilities are permanently known. Actual surface capability manifests must be supplied at compile time.

## CS-IEF-08 conformance gates

1. same inputs -> same semantic bundle digest
2. target adapter cannot mutate mandatory invariant ids
3. missing mandatory invariant -> CONSTITUTIONAL_DRIFT
4. unavailable capability is disclosed, not simulated
5. capability manifest change -> new distribution digest
6. source ref/digest change -> new distribution digest
7. selected domain crystal change -> new distribution digest
8. generated artifact drift detection
9. secret-like/private input cannot enter public bundle
10. private-lab source excluded by default
11. ChatGPT surface profile compiles
12. Gemini surface profile compiles
13. Gemini Notebook source-first profile compiles
14. Portable filesystem manifest compiles
15. generated bundle remains provider-neutral when provider unavailable
16. build receipt binds all effective compile inputs
17. bundle can be represented as a CS-IEF-07 witness subject without implying semantic truth

## Closure criterion

CS-IEF-08 closes when the normative multi-surface compiler contract, machine-readable Ω/surface/distribution schemas, baseline profiles for ChatGPT/Gemini/Gemini Notebook/portable, a deterministic reference compiler, and compile/drift test vectors exist. Production packaging and local runtime installation remain CS-IEF-09.