# CS-IEF-09 — Portable / Local Runtime and Release Packaging

Status: canonical specification layer / bootstrap contract

## Purpose

Turn a verified CS-IEF-08 DistributionBundle into an installable, inspectable, provider-neutral local CodexStation substrate without allowing installation convenience to bypass authority, qualification, provenance, or assurance boundaries.

`DistributionBundle -> VERIFY -> INSTANTIATE -> DISCOVER -> QUALIFY -> SELECT_MODE -> INSTALL -> READY`

Installation is not authorization. Provider discovery is not provider qualification. Provider qualification is not execution authorization.

## Runtime modes

Initial modes:

- `OMEGA_KNOWLEDGE_ONLY`
- `OMEGA_POLICY_ONLY`
- `IEF_HOST_PROCESS`
- `IEF_CONTAINER`
- `IEF_MICROVM`
- `IEF_REMOTE`

A runtime MAY expose multiple discovered modes, but MUST enter only a mode whose prerequisites and policy gates are satisfied.

## Bootstrap invariants

1. Bundle integrity MUST verify before installation.
2. Mandatory Ω invariants MUST pass the CS-IEF-08 constitutional-equivalence gate.
3. No secret may be embedded in the release bundle or installation receipt.
4. Provider discovery MUST NOT assign EAC.
5. EAC assignment requires current qualification evidence under CS-IEF-03/04/05 semantics.
6. Runtime mode selection MUST NOT silently widen authority.
7. Knowledge-only mode MUST remain useful when no execution provider exists.
8. Installation MUST be reproducible from the same release manifest and supported platform inputs, modulo explicitly non-semantic host facts.
9. Installation state and runtime state are distinct.
10. Generated/install state MUST NOT become canonical source truth.

## ReleaseBundle

A release SHOULD contain:

- `MANIFEST.yaml` — release identity and component graph;
- `VERSION` — semantic release version;
- `INTEGRITY.sha256` — content digest list;
- `00_CORE/` — constitutional kernel;
- `01_ARCHITECTURE/` — architecture/specification surfaces;
- `02_IEF/` — execution/policy/evidence contracts;
- `03_CAPABILITIES/` — declared capability/profile templates;
- `04_SOURCES/` — public source manifests;
- `05_DOMAIN_CRYSTALS/` — optional domain modules;
- `06_SURFACE/` — local/portable adapter;
- `07_RUNTIME/` — bootstrap/runtime metadata;
- `INSTALLATION_RECEIPT.json` after installation, outside immutable release payload where practical.

## Release manifest

The release manifest MUST bind:

- release id/version;
- CS-IEF specification root;
- Ω version and DistributionBundle digest;
- compiler id/version;
- artifact path/digest/type;
- supported platform classes;
- required bootstrap capabilities;
- optional provider adapters;
- provider qualification requirements;
- source graph digest;
- license/disclosure metadata;
- build provenance reference;
- release digest.

## Bootstrap phases

### B0 VERIFY

Verify release manifest, artifact digests, DistributionBundle digest, mandatory invariant coverage, schema versions, and disclosure constraints. Failure is terminal and produces a rejection receipt.

### B1 INSTANTIATE

Create local immutable release view plus separate mutable state directories. Canonical/release bytes MUST NOT be silently rewritten by runtime state.

Recommended split:

- `release/` immutable or integrity-monitored;
- `state/` mutable runtime state;
- `evidence/` append-only receipts/evidence;
- `cache/` disposable derived data;
- `config/` explicit operator configuration;
- `secrets/` external secret references or OS/provider-backed secret material, excluded from release artifacts.

### B2 DISCOVER

Discover host facts and provider candidates. Discovery records facts such as OS/architecture, runtime availability, provider identity/version, and adapter presence. Discovery MUST NOT infer assurance from provider name.

### B3 QUALIFY

Apply current provider/environment qualification evidence. Missing, stale, incompatible, or insufficient evidence leaves the provider unqualified for the requested EAC/mode.

### B4 SELECT_MODE

Select the highest operator-requested mode that is both policy-permitted and qualified. Automatic fallback MAY narrow to a lower-authority mode only when policy explicitly permits it and the transition is recorded. Upward fallback is forbidden.

### B5 INSTALL

Materialize configuration, indexes, adapters, source references, and runtime launch metadata. Installation MUST remain provider-neutral until a qualified provider is selected.

### B6 READY

Emit `InstallationReceipt` with effective mode, provider status, qualification references, release digest, configuration digest, omissions/degradations, and runtime-state root. READY means bootstrap succeeded; it does not authorize arbitrary execution.

## Provider discovery contract

Provider candidates SHOULD expose:

- provider id/version;
- adapter ABI version;
- candidate runtime modes;
- capability manifest digest;
- health state;
- qualification reference/digest if present;
- freshness/host binding;
- availability state.

`DISCOVERED(provider) != QUALIFIED(provider)`

## Mode lattice

Mode selection is a partial order of effect authority, not a marketing tier. Knowledge/policy-only modes carry no execution authority. Execution modes require the CS-IEF policy membrane.

A bootstrap implementation MUST NOT claim that `HOST_PROCESS < CONTAINER < MICROVM < REMOTE` is a universal assurance ordering solely from names. Effective EAC remains evidence-driven.

## Secrets

Release packages contain no raw secrets. Bootstrap may resolve secret references only through explicit operator/runtime configuration. Secret presence MUST NOT alter release content digests. Secret material MUST NOT be copied into evidence records.

## InstallationReceipt

A receipt SHOULD bind:

- receipt schema/version;
- release digest;
- DistributionBundle digest;
- installation id;
- platform facts digest;
- configuration digest;
- discovered providers;
- qualification references;
- requested/effective runtime mode;
- selected provider if any;
- omissions/degradations;
- bootstrap phase outcomes;
- installed artifact manifest digest;
- terminal state: `READY` or `REJECTED`;
- receipt digest.

The receipt MAY become a CS-IEF-07 witness subject. It proves installation correspondence/integrity only within its evidence semantics; it does not prove semantic truth or runtime security beyond captured evidence.

## Portable knowledge-only baseline

The first conformant release MUST support installation with no execution provider:

`provider = NONE`
`mode = OMEGA_KNOWLEDGE_ONLY`

This baseline verifies that Ω is independently useful as a constitutional/source/specification substrate and that execution remains an additional authorized capability.

## Packaging

Reference packaging SHOULD support a deterministic directory/tar/zip payload where platform tooling permits. Archive metadata that would break deterministic content digests SHOULD be normalized or excluded from the semantic release digest.

Package verification MUST be possible without network access when all required public source payloads are embedded. Source-reference-only releases MUST disclose which operations require network access.

## Upgrade contract

Upgrade is a new release installation, not mutation of canon in place.

`R_n -> VERIFY(R_n+1) -> MIGRATION_PLAN -> INSTALL(R_n+1) -> VERIFY_STATE -> PROMOTE`

Rollback MUST preserve prior release/evidence bytes. Mutable state migration must be explicit and receipt-bound.

## Uninstall contract

Uninstall MUST distinguish immutable release payload, disposable cache, mutable operator state, evidence records, and externally managed secrets. Evidence and operator data MUST NOT be deleted implicitly merely because executable/runtime files are removed.

## Reference implementation boundary

The public reference runtime may demonstrate:

- deterministic release manifest generation;
- artifact integrity verification;
- knowledge-only installation;
- provider candidate discovery from explicit descriptors;
- qualification-aware mode selection;
- installation receipt generation;
- fail-closed bootstrap rejection.

It MUST NOT claim empirical container/microVM/remote assurance without qualification evidence.

## CS-IEF-09 conformance gates

1. tampered artifact -> VERIFY rejection
2. missing mandatory artifact -> VERIFY rejection
3. knowledge-only install succeeds with provider NONE
4. provider discovery alone never assigns EAC
5. stale/missing qualification cannot activate qualified execution mode
6. requested execution mode cannot silently widen authority
7. explicitly permitted fallback may narrow and is receipt-recorded
8. raw secret-like release input is rejected
9. release and mutable state are separated
10. same semantic release inputs -> same release digest
11. installation receipt binds release/config/platform/provider state
12. generated installation state is not canonical source
13. upgrade preserves prior release/evidence history
14. uninstall does not implicitly destroy evidence/operator data
15. installation receipt can be bridged to CS-IEF-07 without truth promotion

## Closure criterion

CS-IEF-09 closes when the normative portable/local bootstrap contract, ReleaseManifest and InstallationReceipt schemas, a deterministic packager/verifier, a provider-neutral knowledge-only installer, qualification-aware mode-selection reference logic, and bootstrap test vectors exist. Empirical provider qualification and production-grade platform installers remain implementation/release tracks.