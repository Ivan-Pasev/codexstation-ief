# CodexStation Isolated Execution Fabric (IEF)

CodexStation IEF is a provider-neutral execution architecture for materializing bounded computational worlds under explicit authority.

It separates cognition authority from effect authority and defines stable contracts for execution specification, provider capability negotiation, assurance qualification, execution receipts, evidence capture, and reproducible research cells.

## Core invariant

`RUN(E) => AUTH(E) AND BOUND(E) AND TRACE(E)`

## Architecture

CodexStation = Cognition Fabric + Knowledge Fabric + Policy Fabric + Isolated Execution Fabric + Evidence Fabric.

Microsandbox is the initial reference provider, not the architectural core. Provider-specific implementations are hidden behind the stable IEF provider ABI.

## Current specification state

- CS-IEF-01 — architecture and execution-cell model
- CS-IEF-02 — ExecutionSpec and ExecutionReceipt
- CS-IEF-03 — provider ABI, capability negotiation, qualification and assurance
- CS-IEF-04 — MicrosandboxProvider reference adapter (next)

## Repository role

This public repository is the implementation/specification surface. Internal experiments and unpublished integration work live in the private `codexstation-ief-lab` repository and are promoted here only after review.

## Canonical principles

- Isolation is not authorization.
- Network authority is deny-by-default.
- Persistence is opt-in.
- Secrets are non-ambient by default.
- Shared mutable storage is an explicit coupling capability.
- Silent capability widening or assurance inflation is forbidden.
- Provider-specific types do not cross the stable IEF boundary.

## Status

Early specification and reference implementation phase. Public interfaces may evolve until the first stable release.
