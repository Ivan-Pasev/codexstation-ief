# MicrosandboxProvider

Reference implementation target for the CS-IEF provider ABI.

## Boundary

This adapter translates provider-neutral CS-IEF contracts into Microsandbox runtime/SDK operations. Provider-specific types MUST NOT cross the IEF kernel boundary.

## Current status

- capability mapping: defined
- prior reproducibility anchor: `e36792dae06edcd9b6f86abd6b83da7a26c7cdf6`
- current upstream `main` observed 2026-09-04: `5eca4de8bf233e57f114140f8c076ea8c96f21ab`
- adapter implementation: pending/private-lab
- empirical qualification: `QUALIFICATION_BLOCKED_ENVIRONMENT`
- EAC assignment: `null`
- execution authorization: `false`

The observed newer upstream snapshot is not silently promoted to a qualified dependency pin. Exact source/runtime/host identity must be captured by CS-IEF-16 empirical qualification.

See [`../../specs/CS-IEF-04.md`](../../specs/CS-IEF-04.md), [`../../specs/CS-IEF-16.md`](../../specs/CS-IEF-16.md), and [`qualification-plan.yaml`](qualification-plan.yaml).

## Intended implementation direction

Rust is the preferred reference adapter because Microsandbox exposes a native Rust SDK and CS-IEF needs a stable provider boundary suitable for later native/sovereign providers. Public APIs remain provider-neutral even if the reference implementation is Rust.

## Qualification invariant

`FEATURE_PRESENT != CONTROL_ENFORCED != ISOLATION_QUALIFIED != EAC_ASSIGNED != EXECUTION_AUTHORIZED`

Microsandbox's microVM architecture makes it a candidate for strong isolation qualification; it does not itself assign EAC-3. CS-IEF requires active host/runtime evidence.

## Non-negotiable rules

1. Feature support is not assurance evidence.
2. No silent degradation.
3. No raw secret exposure when brokered/destination-bound semantics were requested.
4. Bind mounts and shared mutable storage require explicit authority.
5. Snapshot semantics are filesystem-state checkpoints unless proven otherwise.
6. Provider health/qualification may invalidate selection.
7. Known upstream defects relevant to the tested version/platform are part of the qualification risk ledger.
8. Missing microVM/backend capability yields `QUALIFICATION_BLOCKED_ENVIRONMENT`, never a simulated PASS.
9. Provider-backed execution remains fail-closed until a measured non-null EAC and Policy Compiler authorization exist.
