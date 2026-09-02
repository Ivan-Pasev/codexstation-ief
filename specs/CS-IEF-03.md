# CS-IEF-03 — Provider ABI and Capability Negotiation

Status: canonical specification layer.

## Admissibility

`ADMISSIBLE(p,E) iff CAP(p) ⊇ REQ(E) and EAC_measured(p) >= EAC_required(E) and HEALTH(p) = READY`

Only admissible providers may be ranked.

## Stable provider operations

`identity, capabilities, health, qualify, plan, create, start, exec, inspect, metrics, checkpoint, export, stop, destroy`

## Enforcement classes

- UNSUPPORTED
- DECLARED
- SOFTWARE_ENFORCED
- HARDWARE_ENFORCED
- ATTESTED

## Degradation

Any weakening of the requested contract requires explicit authorization. Silent substitution is forbidden.

## ProviderPlan

The immutable ProviderPlan binds the ExecutionSpec digest to provider identity/version, capability and qualification digests, projected effective assurance, control mappings, degradations and provider extensions.
