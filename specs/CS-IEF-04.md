# CS-IEF-04 — MicrosandboxProvider Reference Mapping

Status: implementation mapping / qualification pending

## Purpose

Define the first reference adapter from the provider-neutral CS-IEF ABI to `superradcompany/microsandbox` while preserving the rule that Microsandbox is a provider, never the IEF core.

## Source anchor

Verified upstream snapshot: `e36792dae06edcd9b6f86abd6b83da7a26c7cdf6` on `main`.

This snapshot is a reproducibility anchor, not a permanent dependency pin.

## Verified feature mapping

| CS-IEF semantic capability | Microsandbox surface | Mapping status |
| --- | --- | --- |
| hardware-isolated execution candidate | microVM-backed sandbox with guest Linux kernel | VERIFIED FEATURE / EAC PENDING |
| CPU bounds | sandbox builder CPU configuration | VERIFIED FEATURE |
| memory bounds | sandbox builder memory configuration | VERIFIED FEATURE |
| OCI image root | image-based sandbox creation | VERIFIED FEATURE |
| alternate root inputs | bind-rootfs, disk-image, snapshot-based sandbox | VERIFIED FEATURE |
| collected execution | `exec` / shell | VERIFIED FEATURE |
| streaming execution | `exec_stream` events | VERIFIED FEATURE |
| guest filesystem | read/write/list/copy/stat/stream APIs | VERIFIED FEATURE |
| named persistent storage | named volumes | VERIFIED FEATURE |
| host coupling | bind mounts | VERIFIED FEATURE / ELEVATED POLICY REQUIRED |
| ephemeral memory fs | tmpfs mounts | VERIFIED FEATURE |
| disk mounts | disk-image mounts | VERIFIED FEATURE |
| no network interface | network disable | VERIFIED FEATURE |
| traffic policy | network policy objects/rules | VERIFIED FEATURE |
| DNS controls | DNS filtering | VERIFIED FEATURE |
| TLS mediation | TLS interception | VERIFIED FEATURE |
| secret mediation | destination-bound placeholder substitution | VERIFIED FEATURE |
| port exposure | port publishing | VERIFIED FEATURE |
| preboot mutation | rootfs patches | VERIFIED FEATURE |
| detached execution | detached sandboxes / reconnect | VERIFIED FEATURE |
| telemetry | metrics and logs | VERIFIED FEATURE |
| filesystem checkpoint | snapshots | VERIFIED FEATURE; NOT FULL VM STATE |
| interactive remote access | SSH/SFTP | VERIFIED FEATURE, optional feature |

## Stable adapter mapping

`identity()` → Microsandbox provider identity + runtime/SDK version.

`capabilities()` → normalized feature declaration derived from compiled SDK features and runtime discovery.

`health()` → runtime availability + backend readiness + stale-handle/lifecycle checks.

`qualify()` → CS-IEF conformance harness; MUST NOT derive EAC from product identity.

`plan(spec)` → map ExecutionSpec to Sandbox builder configuration, detect unsupported controls, emit degradations only when explicitly permitted.

`create(plan)` → create a sandbox from the authorized ProviderPlan.

`start(cell)` → connect/start according to lifecycle state.

`exec(cell, operation)` → collected or streaming execution.

`inspect(cell)` → lifecycle/status/configuration introspection.

`metrics(cell)` → normalized metrics/log evidence.

`checkpoint(cell)` → filesystem-state checkpoint/snapshot only unless future upstream semantics prove more.

`export(cell, contract)` → explicit controlled guest-to-host artifact export.

`stop(cell)` → graceful stop/request-stop + wait semantics.

`destroy(cell)` → destroy/remove while enforcing CS-IEF persistence policy.

## Security mappings

### Filesystem

Bind mounts and shared writable named volumes are explicit coupling capabilities and cannot be silently produced from lower-risk filesystem classes.

### Network

CS-IEF `network = NONE` maps to no network interface where available. A deny-all policy with an interface present is semantically distinct and must not be reported as identical.

### Secrets

Destination-bound host-side substitution is preferred over placing raw secret values in the guest environment. The adapter must expose any case in which a requested brokered-secret guarantee cannot be preserved.

### Snapshots

Microsandbox snapshots are mapped to `ExecutionCheckpoint::FILESYSTEM_STATE`. They must not be represented as full process/memory/network VM snapshots unless upstream semantics change and qualification verifies those semantics.

## Assurance rule

Microsandbox is a candidate EAC-3 provider because the upstream architecture exposes microVM-backed execution with a guest kernel. It is NOT assigned EAC-3 by this specification.

`EAC_effective = min(EAC_qualified(provider, host, runtime), EAC_permitted(effective_contract))`

Qualification must verify active hypervisor/backend, isolation boundary, lifecycle behavior, policy enforcement, and evidence collection in the actual environment.

## CS-IEF-04 conformance gates

1. Provider discovery and health.
2. CPU/memory constraint test.
3. default-deny/no-interface network tests.
4. allow/deny domain policy tests.
5. destination-bound secret non-exposure test.
6. immutable input and ephemeral workspace tests.
7. shared mutable coupling detection test.
8. host-bind elevated-authority test.
9. collected and streaming exec receipt tests.
10. lifecycle convergence + stale-handle test.
11. checkpoint semantic test.
12. destruction/persistence test.
13. metrics/log evidence test.
14. explicit degradation/fail-closed test.
15. provider-version/source-snapshot receipt test.

No EAC promotion occurs until the relevant qualification evidence passes.
