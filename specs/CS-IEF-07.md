# CS-IEF-07 — Evidence / IRP Witness Bridge

Status: canonical specification layer / bridge contract

## Purpose

Bind CodexStation IEF execution evidence into an append-only witness graph covering observation, intent, authorization, execution planning, materialization, outcome, evidence assembly, and later adjudication without claiming semantic truth.

The bridge is a provenance and correspondence mechanism, not an oracle.

## Canonical witness sequence

`W0 Observation -> W1 Intent -> W2 Authorization -> W3 Outcome`

CS-IEF expands the internal evidence links without changing those four principal witness stages:

`W0 Observation`
`  -> IntentRecord`
`  -> ExecutionSpec`
`  -> PolicyDecision`
`  -> W2 AuthorizationRecord`
`  -> ProviderPlan`
`  -> MaterializationRecord`
`  -> ExecutionReceipt`
`  -> EvidenceBundle`
`  -> W3 OutcomeRecord`
`  -> optional AdjudicationRecord`

`W1` is the canonical intent witness and may bind the IntentRecord/ExecutionSpec digest pair.
`W2` is the canonical authorization witness and must bind the exact PolicyDecision and authorized ProviderPlan digest.
`W3` is the canonical observed outcome witness and must bind the terminal ExecutionReceipt plus resulting EvidenceBundle digest.

## Claim boundary

The bridge may establish evidence for:

- ordering and linkage;
- declared intent;
- authorization correspondence;
- policy-path disclosure;
- provider-plan correspondence;
- execution/outcome correspondence;
- artifact/evidence integrity;
- replay/replication linkage;
- externally anchored receipt digests where such anchoring is configured.

The bridge does NOT by itself establish:

- semantic truth;
- correctness of AI reasoning;
- scientific validity;
- legal compliance;
- ethical correctness;
- absence of compromise;
- mathematical novelty;
- causal truth.

`WITNESSED(x) != TRUE(x)`

## WitnessRecord

Every witness record is immutable after emission and contains at minimum:

- `record_id`
- `record_type`
- `schema_version`
- `trace_id`
- `parent_record_ids[]`
- `subject_digests[]`
- `actor_or_authority_ref`
- `timestamp_or_sequence`
- `previous_chain_digest` or null for genesis
- `record_digest`
- optional external anchor references

Timestamps are descriptive evidence. Ordering MUST NOT depend on wall-clock time alone; deterministic sequence/parent linkage is authoritative inside a trace.

## Record types

- `OBSERVATION`
- `INTENT`
- `POLICY_DECISION`
- `AUTHORIZATION`
- `PROVIDER_PLAN`
- `MATERIALIZATION`
- `EXECUTION_OUTCOME`
- `EVIDENCE_BUNDLE`
- `REJECTION`
- `REPLICATION`
- `ADJUDICATION`
- `ANCHOR`
- `REVOCATION`

Rejection is a first-class witness event. A rejected policy decision MUST NOT be rewritten as an execution failure.

## Trace graph

A trace is a directed acyclic provenance graph, not merely a flat log.

Required primary chain for executed work:

`Observation -> Intent -> Authorization -> ProviderPlan -> ExecutionOutcome -> EvidenceBundle`

Required primary chain for rejected work:

`Observation -> Intent -> PolicyDecision(REJECTED) -> Rejection`

Parallel replication branches MAY share the same originating intent while producing distinct ProviderPlan, ExecutionReceipt, and EvidenceBundle branches. A later ReplicationRecord may compare those branches without merging their raw provenance identities.

## Authorization correspondence

`W2 AuthorizationRecord` MUST bind:

- originating `ExecutionSpec` digest;
- `PolicyDecision` digest;
- authorized `ProviderPlan` digest;
- authority reference;
- explicit degradations if any;
- qualification digest;
- requested/qualified/effective EAC;
- compiler/policy version.

Materialization is admissible only when the provider-side TOCTOU revalidation matches the W2-bound plan state.

## Outcome correspondence

`W3 OutcomeRecord` MUST bind:

- exact `ProviderPlan` digest used;
- `ExecutionReceipt` digest;
- effective provider/runtime identity;
- terminal execution state;
- output/artifact manifest digest;
- `EvidenceBundle` digest;
- deviations/degradations observed after authorization;
- cleanup/persistence terminal state where relevant.

A process success code is evidence of process outcome only.

## Rejection receipts

Policy rejection emits a witnessable record containing:

- Intent/ExecutionSpec digest;
- PolicyDecision digest;
- rejection codes;
- provider/qualification inputs consulted;
- no-cell-created assertion;
- rejection record digest.

This permits audit of prevented actions without fabricating an execution receipt.

## Replication evidence

For CS-IEF-06 R3/R4 workflows, each run receives an independent branch identity. `ReplicationRecord` binds:

- parent research/proof intent;
- branch EvidenceBundle digests;
- declared independence dimensions;
- comparator identity/version;
- comparison outcome;
- comparison artifact digest.

Replication outcomes remain `MATCH`, `MATERIAL_DIFFERENCE`, `INCONCLUSIVE`, or `NOT_RUN`.

`MATCH` means match under the declared comparator, not universal scientific equivalence.

## Adjudication layer

Adjudication is intentionally later than evidence capture.

`AdjudicationRecord` MAY classify or interpret evidence but MUST preserve:

- adjudicator identity/class;
- evidence inputs/digests;
- rules/method/version;
- resulting classification;
- confidence/limitations where applicable;
- adjudication digest.

Adjudication never mutates prior witness records.

## Chain integrity

Canonical record serialization MUST be deterministic.

`record_digest = H(canonical_record_without_record_digest)`

A trace MAY maintain a linear convenience chain digest, but graph validity is determined from immutable record digests and explicit parent links.

External anchoring, including public ledgers or consensus networks, is optional and orthogonal:

`external_anchor(record_digest) -> anchoring evidence`

An anchor may prove that a digest was submitted/observed under the external system's semantics. It does not prove the semantic correctness of the underlying record.

## Privacy and disclosure

Witness records SHOULD commit to sensitive evidence by digest/reference rather than embedding private raw content.

Public witness surfaces must not require disclosure of:

- raw secrets;
- confidential prompts;
- private datasets;
- customer/personal data;
- private keys or signing material.

Redaction must not alter committed digests. A redacted disclosure is a view over committed evidence, not a rewritten original record.

## Failure and revocation

Append-only does not mean mistakes cannot be acknowledged. Corrections use new records.

`REVOCATION` or superseding `ADJUDICATION` records MAY mark earlier authority or interpretation as revoked/superseded while preserving the original evidence chain.

No record deletion is treated as semantic correction.

## AI-WITNESS / IRP-1 interoperability

The current public `Ivan-Pasev/AI-WITNESS` project is treated as an adjacent witness-protocol surface, not a dependency required by the IEF kernel.

The bridge intentionally aligns with its published claim boundary: bounded receipt integrity, authorization ordering, policy-path disclosure, action correspondence, and external consensus evidence may be made inspectable; semantic truth is not proven by the witness layer.

Integration class: `OPTIONAL_WITNESS_BACKEND`.

The stable CS-IEF witness schema must remain usable even if AI-WITNESS evolves independently or is absent.

## Security invariants

1. Witness order follows explicit parent/sequence linkage, not wall-clock time alone.
2. W2 binds the exact authorized ProviderPlan.
3. W3 binds the exact observed ExecutionReceipt and EvidenceBundle.
4. Rejection is not execution failure and creates no cell.
5. Append-only correction uses new records; prior records are not mutated.
6. External anchoring does not imply semantic truth.
7. Sensitive raw evidence is referenced/committed rather than unnecessarily embedded.
8. Replication branches preserve independent provenance.
9. Adjudication is downstream of evidence capture and never rewrites evidence.
10. `WITNESSED(x) != TRUE(x)`.

## CS-IEF-07 conformance gates

1. deterministic WitnessRecord serialization/digest
2. W0->W1->W2->W3 primary-chain validation
3. W2 exact ProviderPlan binding test
4. TOCTOU drift invalidates W2 materialization test
5. W3 exact ExecutionReceipt/EvidenceBundle binding test
6. policy rejection emits rejection witness and no execution receipt
7. parent-link tamper detection
8. graph branch/replication validation
9. R4 independence metadata preservation
10. adjudication append-only test
11. revocation/supersession append-only test
12. redacted disclosure retains committed digest references
13. external anchor treated as anchoring evidence only
14. process success cannot imply semantic/scientific truth
15. optional AI-WITNESS backend absence does not invalidate core witness graph

## Closure criterion

CS-IEF-07 closes when normative witness-graph semantics, machine-readable WitnessRecord/trace schemas, deterministic digest/reference implementation vectors, rejection/replication/adjudication record forms, and an optional IRP backend adapter contract exist. External ledger anchoring and production AI-WITNESS integration remain later implementation events.