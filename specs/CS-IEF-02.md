# CS-IEF-02 — ExecutionSpec and ExecutionReceipt

Status: canonical specification layer.

## Purpose

`ExecutionSpec` declares requested authority before materialization. `ExecutionReceipt` records the effective observed contract and execution outcome.

## Invariants

- Requested and effective contracts are distinct.
- Silent widening is forbidden.
- Unsupported controls fail closed or require explicit authorized degradation.
- Raw secrets are excluded from the stable spec.
- Persistence is opt-in.
- Network authority is deny-by-default.
- Machine contracts require deterministic canonicalization and digests.

## Core relation

`EffectiveAuthority(E) ⊆ AuthorizedAuthority(E)`
