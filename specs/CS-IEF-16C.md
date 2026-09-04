# CS-IEF-16C — Empirical Evidence-to-EAC Constitution

Status: CONSTITUTION_DEFINED / NO PROVIDER PROMOTION

## Purpose

Define the only admissible path from empirical provider qualification evidence to an Execution Assurance Class (EAC). This document does not assign Microsandbox an EAC.

## Assurance classes

- EAC-0 — no qualified execution isolation. Knowledge/policy-only operation.
- EAC-1 — bounded host-process execution with measured resource/lifecycle controls; no isolation-security claim.
- EAC-2 — container/process isolation with empirically enforced filesystem, network, secret, resource and lifecycle controls; host-kernel sharing remains explicit.
- EAC-3 — hardware-virtualized guest boundary with empirically bound hypervisor/backend identity plus all EAC-2 control families and guest/host escape-resistance probes in the tested configuration.
- EAC-4 — reserved. Requires a future constitution covering independently replicated high-assurance isolation evidence; not assignable by CS-IEF-16C.

## Promotion law

`assigned_eac = min(architecture_ceiling, empirical_control_floor, evidence_quality_ceiling)`.

No class may be inferred from product name, documentation, claimed architecture, availability of `/dev/kvm`, or a single successful sandbox execution.

### EAC-1 minimum
G01, G04, G11, G12, G14, G15, G16, G17 and G18 PASS. Other isolation gates may be NOT_APPLICABLE only when the requested contract makes no isolation claim.

### EAC-2 minimum
All EAC-1 gates plus G05, G06, G07, G08, G09 and G10 PASS. G02/G03 must establish the actual isolation boundary used; if the provider shares the host kernel this must be recorded and architecture_ceiling <= 2.

### EAC-3 minimum
G01-G18 PASS except gates explicitly declared NOT_APPLICABLE by the canonical qualification plan. G02 must bind the active hardware-virtualization backend to the tested cell. G03 must provide empirical guest/host boundary evidence. G12 must include stale-handle/incarnation adversarial testing. G14 must demonstrate destruction/persistence semantics. G17 binds provider/runtime/source/host/backend identities into the qualification receipt. G18 must contain the exact-version risk ledger and unresolved critical risks must be zero.

## Evidence-quality ceiling

- documentation or feature map only -> EAC-0 ceiling
- local observation without bound raw evidence -> EAC-0 ceiling
- single-host reproducible empirical evidence -> maximum EAC-3, subject to gates
- cross-host independent replication -> may strengthen confidence but does not create EAC-4

## Authorization separation

`assigned_eac > 0` never sets `execution_authorized=true` by itself. Authorization additionally requires an ExecutionContract, policy decision, capability grant, provider plan, and receipt binding the qualification digest.

## Fail closed

Any mandatory FAIL, unresolved isolation-critical gate, missing environment identity, stale qualification, provider/runtime mismatch, or qualification digest mismatch results in EAC-0/null for the requested execution path.

## Microsandbox current state

No real-host G01-G18 evidence bundle has been admitted. `assigned_eac=null`; `execution_authorized=false`.
