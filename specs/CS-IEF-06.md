# CS-IEF-06 — ResearchCell and FormalProofCell Profiles

Status: canonical specification layer / reference profiles

## Purpose

Define purpose-constrained `ExecutionSpec` constructors for reproducible scientific computation and formal verification. Profiles are not providers and do not bypass CS-IEF-05 policy compilation.

`Profile + Inputs -> constrained ExecutionSpec -> Policy Compiler -> ProviderPlan`

A profile may narrow authority and add mandatory evidence obligations. It may not silently widen authority beyond the originating request.

## Common profile contract

Every profile MUST bind:

- profile id and version
- purpose and expected result class
- source/input manifest digests
- runtime/image/toolchain identity
- dependency lock/pin evidence
- compute/resource ceiling
- filesystem policy
- network policy
- secret policy
- persistence/checkpoint policy
- evidence requirements
- reproducibility mode
- canonical profile digest

### Reproducibility modes

- `R0_EXPLORATORY` — environment captured; exact replay not promised.
- `R1_PINNED_INPUTS` — inputs and sources content-addressed/pinned.
- `R2_PINNED_TOOLCHAIN` — R1 plus runtime/toolchain/dependencies pinned.
- `R3_DETERMINISTIC_REPLAY` — R2 plus deterministic settings/seeds and replay comparison contract.
- `R4_INDEPENDENT_REPLICATION` — R3 plus independent cell/provider/toolchain replication requirement.

A profile MUST NOT report a higher mode than its evidence bundle supports.

## ResearchCell

Purpose: execute a falsifiable computational experiment, simulation, numerical/symbolic analysis, data transformation, or independent replication under a declared hypothesis/experiment manifest.

### Required research manifest

- `research_id`
- `question`
- `hypothesis` or null for non-hypothesis computational work
- `method`
- `expected_observables`
- `acceptance_or_falsification_criteria`
- `inputs[]` with digests and provenance
- `source_refs[]` with immutable refs where available
- `software_toolchain[]` with versions/digests
- `randomness` declaration: none | fixed_seed | captured_seed | nondeterministic
- `reproducibility_mode`
- `artifact_contract`

### Default authority profile

- network: NONE unless source acquisition or remote service use is explicitly authorized
- persistence: EPHEMERAL unless checkpoint/export is explicitly requested
- raw secrets: forbidden
- mutable host bind: forbidden by default
- shared mutable storage: forbidden by default
- output export: allowlisted paths/artifact classes only

### Research evidence bundle

Must contain, where applicable:

- canonical research manifest + digest
- ExecutionSpec and ProviderPlan digests
- provider/qualification/effective EAC record
- image/runtime/toolchain/dependency identities
- input/source manifest digests
- exact command/notebook/script entrypoint identity
- environment variables excluding secret values
- randomness/seed record
- stdout/stderr or normalized log digests
- metrics/resource record
- output artifact manifest and digests
- exit/terminal state
- deviations/degradations
- replay/replication comparison result

A successful process exit is not equivalent to scientific validation. `ExecutionReceipt` records execution correspondence; scientific interpretation remains a separate adjudication layer.

## FormalProofCell

Purpose: externally check a formal theorem/proof artifact using a declared prover/toolchain and dependency set.

### Required proof manifest

- `proof_id`
- `theorem_name`
- `formal_language`
- `prover`
- `prover_version`
- `entrypoint`
- `source_digest`
- `dependency_manifest_digest`
- `expected_theorem_status`
- `reproducibility_mode` (minimum R2 for a verification claim)

### Supported profile families

Initial names are descriptive profiles, not claims of installed availability:

- Lean 4 / mathlib
- Rocq/Coq
- Isabelle/HOL
- Agda
- Metamath
- SMT profiles such as Z3 or cvc5 where the result class is appropriate

Provider availability and image/toolchain existence remain capability/qualification questions.

### Formal verification rule

A theorem may be reported by IEF as `FORMALLY_CHECKED` only if all mandatory proof-profile requirements are satisfied and the external prover terminates successfully with the expected theorem target under the pinned toolchain/dependency contract.

`FORMALLY_CHECKED` does not mean the theorem's assumptions are physically true, empirically validated, novel, or publication-ready.

### Proof evidence bundle

Must include:

- proof manifest + digest
- source artifact digest
- prover/runtime/image identity
- dependency lock/manifest digest
- exact invocation
- prover exit status
- normalized prover output digest
- theorem target/result
- ExecutionSpec/ProviderPlan/ExecutionReceipt digests
- qualification/effective EAC record
- deviations/degradations

## Profile compilation

`PROFILE_COMPILE(profile, user_intent) -> ExecutionSpec`

The constructor MUST:

1. canonicalize the profile and intent;
2. merge only explicitly permitted user authority;
3. apply profile defaults as restrictions;
4. inject mandatory evidence obligations;
5. enforce minimum reproducibility requirements for claimed result classes;
6. produce a deterministic `profile_digest` and `execution_spec_digest`.

If a requested result class requires stronger reproducibility than the supplied manifest supports, compilation fails before provider selection.

## EvidenceBundle

An `EvidenceBundle` is an append-only manifest over evidence objects, not a claim that those objects are scientifically correct.

Required common fields:

- bundle id/version/type
- profile id/version/digest
- intent/authorization trace reference
- ExecutionSpec digest
- PolicyDecision/ProviderPlan digest
- ExecutionReceipt digest
- source/input manifest digests
- runtime/toolchain manifest digest
- artifact entries with content digests
- reproducibility mode claimed and achieved
- deviations/degradations
- bundle digest

## Independent replication

For R4, independent replication MUST vary at least one declared independence dimension, such as provider instance, execution host, toolchain implementation, or independently rebuilt environment. Merely rerunning the same mutable cell is not independent replication.

Replication outcomes:

- `MATCH`
- `MATERIAL_DIFFERENCE`
- `INCONCLUSIVE`
- `NOT_RUN`

The comparison method itself is part of the profile contract.

## Claim boundaries

IEF may attest to:

- declared inputs/toolchain
- execution policy/assurance correspondence
- process/prover outcome
- artifact/evidence integrity
- replay/replication comparison under the specified comparator

IEF does not by itself attest to:

- empirical truth
- mathematical novelty
- correctness of informal assumptions
- peer-review status
- causal interpretation
- scientific significance

## Security invariants

1. Profiles only constrain/construct ExecutionSpec; they do not call providers directly.
2. Network remains deny-by-default.
3. Secrets remain non-ambient.
4. Source acquisition is distinct from experiment execution and should be pre-staged where possible.
5. Mutable host/shared storage is elevated authority and disallowed by default.
6. Reproducibility claims are bounded by captured evidence.
7. Formal proof status is bounded by external prover evidence and exact target/dependency identity.
8. Evidence integrity is not semantic truth.
9. R4 replication requires a declared independence dimension.
10. Every result remains traceable to intent, policy decision, provider plan, execution receipt, and evidence bundle.

## CS-IEF-06 conformance gates

1. deterministic ResearchCell profile compilation
2. deterministic FormalProofCell profile compilation
3. profile cannot widen originating authority
4. network default-deny test
5. raw-secret rejection test
6. mutable-host/shared-storage default rejection
7. reproducibility-mode overclaim rejection
8. source/toolchain pin completeness test
9. randomness/seed evidence test
10. controlled artifact export test
11. proof target/toolchain/dependency identity test
12. failed prover cannot yield FORMALLY_CHECKED
13. successful prover receipt does not imply empirical/scientific truth
14. R3 replay comparison evidence test
15. R4 independence-dimension enforcement test
16. EvidenceBundle digest/provenance test

## Closure criterion

CS-IEF-06 closes when normative ResearchCell/FormalProofCell contracts, machine-readable profile/evidence schemas, safe reference profiles, and deterministic profile-construction test vectors exist. Actual scientific/proof runs remain separate execution and qualification events.