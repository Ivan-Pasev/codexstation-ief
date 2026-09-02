# MicrosandboxProvider

Reference implementation target for the CS-IEF provider ABI.

## Boundary

This adapter translates provider-neutral CS-IEF contracts into Microsandbox runtime/SDK operations. Provider-specific types MUST NOT cross the IEF kernel boundary.

## Current status

- capability mapping: defined
- source snapshot: `e36792dae06edcd9b6f86abd6b83da7a26c7cdf6`
- adapter implementation: pending/private-lab
- conformance qualification: pending
- EAC assignment: pending

See [`../../specs/CS-IEF-04.md`](../../specs/CS-IEF-04.md).

## Intended implementation direction

Rust is the preferred reference adapter because Microsandbox exposes a native Rust SDK and CS-IEF needs a stable provider boundary suitable for later native/sovereign providers. Public APIs remain provider-neutral even if the reference implementation is Rust.

## Non-negotiable rules

1. Feature support is not assurance evidence.
2. No silent degradation.
3. No raw secret exposure when brokered/destination-bound semantics were requested.
4. Bind mounts and shared mutable storage require explicit authority.
5. Snapshot semantics are filesystem-state checkpoints unless proven otherwise.
6. Provider health/qualification may invalidate selection.
