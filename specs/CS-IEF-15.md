# CS-IEF-15 — Immutable RC Publication and Lifecycle Qualification

Status: implementation/qualification target

## Purpose

CS-IEF-15 governs publication of the already qualified and identity-bound-attested `codexstation-omega-portable 0.1.0-rc2` and qualifies preservation semantics for upgrade/rollback without converting publication into stability, sovereign trust, execution authorization, or provider assurance.

## Frozen subject

- release: `codexstation-omega-portable 0.1.0-rc2`
- source revision: `1c625a5ce59197ec991f3f6778a0ad63dc0b7002`
- archive SHA-256: `4110edafaa4b8bc860f359e9532634415164df86a6c26fd439608179bae08cf2`
- release digest: `sha256:3f05883dc5980ca921eadbf2536c5538027e08eb677ce8fc1d3475b0349edb13`
- provenance: GitHub attestation `45196448`, Rekor log index `2708913109`

## Publication invariant

`PUBLISHED != STABLE != SOVEREIGN_TRUSTED != EXECUTION_AUTHORIZED`

Publication may expose an immutable tag, prerelease record, exact archive, release notes and witness/provenance references. It does not alter the technical qualification of the artifact.

## Immutable tag contract

The RC tag is `v0.1.0-rc2` and MUST resolve to the frozen RC2 source revision, not to the later publication metadata commit.

If the tag already exists with another target, publication MUST fail closed. If the prerelease already exists, automation may verify it but MUST NOT silently replace the release asset or move the tag.

## Publication gates

Before creating or accepting a public prerelease, automation MUST:

1. rebuild RC2 from the frozen source revision;
2. reproduce the exact archive SHA-256;
3. independently verify the GitHub artifact attestation against repository identity;
4. execute the RC2 knowledge-only qualifier against the rebuilt archive;
5. execute lifecycle preservation checks using exact historical RC1 bytes and exact RC2 bytes;
6. verify publication notes/witness references belong to the current public trust/release state;
7. create or verify the immutable tag/release only after all previous gates pass.

## Lifecycle model

Release directories are immutable side-by-side objects. Runtime/operator state, evidence and active-selection metadata are separate.

Example:

```text
installation/
  releases/
    0.1.0-rc1/
    0.1.0-rc2/
  state/
    current.json
  evidence/
  config/
  cache/
```

Upgrade from RC1-held to RC2-qualified means install RC2 alongside RC1 and atomically change the active release pointer after RC2 verification. It does not rewrite RC1.

Rollback means change the active pointer back to RC1 while preserving both release trees and evidence. Because RC1 has a known installation-contract defect, rollback preservation evidence MUST NOT be described as RC1 platform qualification or recommendation for normal operation.

## Lifecycle preservation gates

- exact RC1 artifact identity retained;
- exact RC2 artifact identity retained;
- RC1 release-tree digest unchanged after upgrade;
- RC2 release-tree digest unchanged after rollback;
- evidence/operator-state digest unchanged across pointer transitions;
- upgrade points to RC2 only after RC2 verification;
- rollback restores RC1 pointer without mutating releases;
- no migration step may overwrite evidence implicitly.

## Trust/provenance boundary

CS-IEF-14B identity-bound provenance remains valid evidence for RC2. The separate sovereign Ed25519 trust constitution remains inactive until an accepted signer is explicitly activated.

`ATTESTED_IDENTITY_BOUND != SOVEREIGN_TRUSTED`

## Stable-readiness adjudication

RC2 may be publicly published as a prerelease when publication gates pass. Stable release remains blocked while any mandatory stable gate remains open, including sovereign trust policy requirements or deliberately required lifecycle/platform gates.

A prerelease publication therefore has one of these states:

- `PUBLISHED_PRERELEASE_QUALIFIED_ATTESTED`
- `PUBLICATION_HELD`

Stable readiness is separately:

- `STABLE_READY`
- `STABLE_BLOCKED`

## Closure criterion

CS-IEF-15 closes when the exact RC2 archive has an immutable prerelease publication bound to its frozen source, provenance verification passes during publication, real RC1/RC2 lifecycle preservation evidence passes, and a stable-readiness adjudication is emitted without exceeding the evidence ceiling.
