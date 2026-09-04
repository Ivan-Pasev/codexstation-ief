# CS-IEF-16 — MicrosandboxProvider Empirical Qualification

Status: OPEN / QUALIFICATION BLOCKED PENDING ACTIVE HOST EVIDENCE

## Purpose

Move the Microsandbox reference provider from feature-surface mapping toward measured CS-IEF assurance without deriving assurance from product identity, documentation, architecture claims, or upstream marketing.

## Upstream observation

Current observed upstream `main` at qualification-track opening:

- repository: `superradcompany/microsandbox`
- observed snapshot: `5eca4de8bf233e57f114140f8c076ea8c96f21ab`
- observation time: 2026-09-04
- prior CS-IEF reproducibility anchor: `e36792dae06edcd9b6f86abd6b83da7a26c7cdf6`

The newer snapshot is an observation candidate, not automatically a qualified replacement pin.

## Assurance invariant

`FEATURE_PRESENT != CONTROL_ENFORCED != ISOLATION_QUALIFIED != EAC_ASSIGNED != EXECUTION_AUTHORIZED`

`EAC_effective = min(EAC_qualified(provider, host, runtime), EAC_permitted(effective_contract))`

Until active-environment evidence exists, `assigned_eac = null` and provider-backed execution remains unauthorized.

## Required qualification evidence

The harness MUST bind every result to provider source/version, runtime binary identity where obtainable, host OS/kernel/architecture, virtualization backend, configuration, test vector, timestamps and raw evidence digests.

Mandatory gates:

1. provider discovery and runtime health;
2. active virtualization/backend identity;
3. guest/host boundary observation;
4. CPU and memory enforcement;
5. network NONE semantics and interface observation;
6. network allow/deny enforcement;
7. destination-bound secret non-exposure;
8. immutable-input and ephemeral-workspace behavior;
9. shared mutable storage coupling detection;
10. bind-mount elevated-authority enforcement;
11. collected and streaming execution receipts;
12. lifecycle convergence, stale-handle and incarnation safety;
13. checkpoint semantics bounded to filesystem state unless stronger semantics are evidenced;
14. destruction and persistence behavior;
15. metrics/log evidence completeness;
16. unsupported-control degradation is explicit and fail-closed;
17. provider/source/runtime identity is receipt-bound;
18. known upstream risk ledger is evaluated against the exact tested version/platform.

## Adversarial risk ledger

Qualification MUST explicitly consider current upstream defects/limitations relevant to CS-IEF semantics. At track opening these include recent reports concerning Windows startup regressions, lifecycle incarnation identity/TOCTOU, network/IPv6 behavior, filesystem/volume behavior, and runtime relay liveness. Presence of an upstream report is not proof that the tested snapshot is vulnerable; absence of reproduction is not proof of arbitrary safety. Each applicable risk receives `PASS`, `FAIL`, `NOT_APPLICABLE`, or `UNRESOLVED` with evidence.

## EAC adjudication

No EAC value is preselected. The adjudicator consumes only measured gates and the CS-IEF assurance definition. Any mandatory `FAIL`, missing environment identity, or unresolved isolation-critical gate holds EAC at null.

A successful subset may produce a bounded provider qualification record without execution authorization.

## First ExecutionCell rule

The first provider-backed ResearchCell may execute only after:

1. an active-environment qualification record assigns a non-null EAC;
2. Policy Compiler authorizes the exact ExecutionSpec under that measured EAC;
3. provider identity/qualification freshness matches the runtime actually selected;
4. the resulting ProviderPlan contains no silent degradation;
5. execution emits an ExecutionReceipt and EvidenceBundle.

No simulated execution or prose-only qualification is permitted.

## Closure criterion

CS-IEF-16 closes only when a real supported host executes the empirical harness against an exact Microsandbox runtime/source identity and the resulting evidence is adjudicated. If the available environment cannot run the required microVM backend, the correct state is `QUALIFICATION_BLOCKED_ENVIRONMENT`, not PASS.