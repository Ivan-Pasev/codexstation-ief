# CS-IEF-05 — Policy Compiler and EAC Verifier

Status: canonical specification layer / implementation pending

## Purpose

Define the deterministic membrane that converts an `ExecutionSpec` plus qualified `ProviderCapabilities` into either an immutable authorized `ProviderPlan` or a fail-closed rejection.

The policy compiler does not execute workloads. It decides whether requested authority can be materialized without silent widening.

## Inputs

- canonical `ExecutionSpec` and digest
- provider identity and ABI version
- immutable `ProviderCapabilities` and digest
- current provider health
- current qualification record and digest
- policy profile / organizational constraints
- explicit degradation permissions from the originating authority chain

## Outputs

Exactly one of:

1. `AUTHORIZED(ProviderPlan)` — immutable plan with effective controls and deterministic digest.
2. `REJECTED(PolicyDecision)` — machine-readable denial with failed invariants and unsupported requirements.

No third implicit fallback state exists.

## Core compiler relation

`COMPILE(E,p,Q,P) -> AuthorizedPlan | Rejection`

Authorization is valid iff:

`HEALTH(p)=READY`

`CAP(p) >= REQUIRED_CONTROLS(E)`

`EAC_QUALIFIED(p,Q) >= EAC_REQUIRED(E)`

`EFFECTIVE_AUTHORITY <= REQUESTED_AUTHORITY + EXPLICITLY_AUTHORIZED_DEGRADATIONS`

`POLICY_PROFILE(P)` permits every effective control.

## Compiler phases

1. Canonicalize and hash all inputs.
2. Resolve requested controls into mandatory and optional requirements.
3. Intersect requirements with provider capabilities.
4. Apply organizational/profile restrictions.
5. Evaluate requested assurance against qualification evidence.
6. Compute effective controls and candidate effective EAC.
7. Detect widening, weakening, unsupported semantics, stale qualification, and health failure.
8. Reject on any unapproved mismatch.
9. Bind accepted mappings and explicit degradations into `ProviderPlan`.
10. Deterministically hash and freeze the plan before materialization.

## Authority invariant

`EFFECTIVE_AUTHORITY(plan) <= AUTHORIZED_AUTHORITY(spec, degradation_grants)`

The compiler may narrow authority automatically. It may not widen authority automatically.

Examples of narrowing that are normally safe when semantics remain satisfied include lower CPU ceilings, lower memory ceilings, shorter runtime deadlines, read-only conversion, and stricter network denial.

Semantic substitution is not ordinary narrowing. For example, `no network interface` cannot silently become `interface present + deny-all policy`; brokered destination-bound secrets cannot silently become raw guest environment variables; ephemeral storage cannot silently become persistent shared storage.

## Degradation object

Every permitted weakening MUST be explicit and digest-bound:

- control identifier
- requested semantic
- effective semantic
- reason
- enforcement class before/after
- approving authority reference
- security consequence

If an authority reference is absent, the degradation is unauthorized.

## EAC verifier

The verifier is evidence-driven rather than provider-name-driven.

`EAC_REPORTED <= EAC_EFFECTIVE <= EAC_QUALIFIED <= EAC_POTENTIAL`

`EAC_EFFECTIVE = min(EAC_QUALIFIED(provider, host, runtime, qualification_digest), EAC_PERMITTED(effective_contract))`

A provider claiming microVM architecture therefore remains below EAC-3 until the active environment has qualification evidence sufficient for EAC-3.

### Staleness

Qualification MUST be invalidated or re-evaluated when material identity changes, including relevant provider/runtime version, backend/hypervisor class, host security environment, capability digest, qualification harness version, or a policy-significant configuration change.

A stale qualification record cannot authorize its former EAC.

## Enforcement-class verifier

For each mandatory control, the compiler verifies the minimum enforcement class requested by `ExecutionSpec` against the qualified effective class:

`UNSUPPORTED < DECLARED < SOFTWARE_ENFORCED < HARDWARE_ENFORCED < ATTESTED`

A higher architectural EAC does not compensate for an insufficient per-control enforcement class.

## Fail-closed rejection codes

- `PROVIDER_NOT_READY`
- `CAPABILITY_MISSING`
- `ENFORCEMENT_TOO_WEAK`
- `ASSURANCE_INSUFFICIENT`
- `QUALIFICATION_MISSING`
- `QUALIFICATION_STALE`
- `POLICY_FORBIDDEN`
- `UNAUTHORIZED_DEGRADATION`
- `AUTHORITY_WIDENING`
- `SEMANTIC_MISMATCH`
- `NONDETERMINISTIC_INPUT`
- `ABI_INCOMPATIBLE`

Rejections are evidence objects and should be receipted without creating a cell.

## Determinism

Given equal canonical inputs and equal policy/compiler version:

`digest(COMPILE(inputs))` MUST be stable.

Time-varying health or qualification data must enter as explicit hashed inputs rather than ambient state.

## TOCTOU membrane

Authorization and materialization are separate phases. Immediately before `create(plan)`, the runtime MUST verify that provider identity, capability digest, qualification digest, relevant health epoch, and plan digest still match the authorized plan. Material mismatch invalidates authorization and requires recompilation.

## Receipt obligations

Execution receipts MUST identify:

- compiler version
- policy profile/version
- ExecutionSpec digest
- ProviderPlan digest
- provider/capability digest
- qualification digest
- requested, qualified and effective EAC
- explicit degradations
- TOCTOU revalidation result

## Security invariants

1. Isolation is not authorization.
2. Provider identity is not assurance evidence.
3. No silent widening.
4. No silent semantic substitution.
5. Optional degradation requires explicit prior permission.
6. Stale qualification cannot authorize execution.
7. Mandatory control enforcement is checked independently of aggregate EAC.
8. Provider-specific types do not cross the stable kernel boundary.
9. Rejection is a valid, evidence-bearing terminal result.
10. The authorized plan is immutable before provider materialization.

## CS-IEF-05 conformance gates

1. deterministic compile/hash test
2. missing-capability fail-closed test
3. enforcement-class downgrade rejection test
4. insufficient-EAC rejection test
5. stale-qualification rejection test
6. explicit-degradation authorization test
7. unauthorized-degradation rejection test
8. network semantic-substitution test
9. secret semantic-substitution test
10. filesystem coupling/widening test
11. stricter-authority narrowing test
12. policy-profile prohibition test
13. ABI incompatibility test
14. TOCTOU capability/qualification drift test
15. rejection-receipt provenance test

## Closure criterion

CS-IEF-05 closes when the normative compiler/verifier contract, machine-readable policy decision schema, deterministic test vectors, and a provider-neutral reference implementation skeleton exist, while empirical EAC assignment remains delegated to qualification evidence.