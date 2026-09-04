# CS-IEF-15 — Immutable RC Publication and Lifecycle Qualification

Status: **CLOSED at digest/tag-bound prerelease publication + lifecycle-evidence level**

## Purpose

CS-IEF-15 governs publication of the qualified and identity-bound-attested `codexstation-omega-portable 0.1.0-rc2` and qualifies preservation semantics for upgrade/rollback without converting publication into stability, sovereign trust, execution authorization, or provider assurance.

## Frozen subject

- release: `codexstation-omega-portable 0.1.0-rc2`
- source revision: `1c625a5ce59197ec991f3f6778a0ad63dc0b7002`
- archive SHA-256: `4110edafaa4b8bc860f359e9532634415164df86a6c26fd439608179bae08cf2`
- release digest: `sha256:3f05883dc5980ca921eadbf2536c5538027e08eb677ce8fc1d3475b0349edb13`
- provenance: GitHub attestation `45196448`, Rekor log index `2708913109`

## Publication invariant

`PUBLISHED != STABLE != SOVEREIGN_TRUSTED != EXECUTION_AUTHORIZED`

Publication exposes a frozen tag target, exact digest-bound archive, prerelease record, release notes and witness/provenance references. It does not alter the technical qualification of the artifact.

## Tag and publication contract

The RC tag is `v0.1.0-rc2` and resolves to the frozen RC2 source revision, not to later publication-metadata commits.

If the tag exists with another target, publication fails closed. If the prerelease exists, automation verifies it and refuses silent asset replacement or tag movement.

GitHub currently reports the release object itself as `immutable: false`. Accordingly, CS-IEF-15 claims **digest/tag-bound publication with policy immutability**, not platform-enforced immutable-release mode. Artifact identity is independently bound by archive digest, provenance attestation, release witness and tag target.

## Executed publication gates

GitHub Actions run `33864229370` passed all substantive gates:

1. rebuilt RC2 from frozen source revision — PASS;
2. reproduced exact archive SHA-256 — PASS;
3. independently verified GitHub artifact attestation — PASS;
4. re-executed packaged RC2 knowledge-only qualifier — PASS;
5. downloaded exact retained RC1 workflow artifact and executed lifecycle preservation test — PASS;
6. created/verified tag `v0.1.0-rc2` at exact RC2 source commit — PASS;
7. created GitHub prerelease and attached exact RC2 asset — PASS;
8. re-downloaded published asset and verified SHA-256 — PASS;
9. emitted CS-IEF-15 publication/lifecycle evidence artifact — PASS.

## Published prerelease

- GitHub Release ID: `382647993`
- tag: `v0.1.0-rc2`
- tag target: `1c625a5ce59197ec991f3f6778a0ad63dc0b7002`
- release asset ID: `544183662`
- release asset SHA-256: `sha256:4110edafaa4b8bc860f359e9532634415164df86a6c26fd439608179bae08cf2`
- publication state: `PUBLISHED_PRERELEASE_QUALIFIED_ATTESTED`
- GitHub release object immutable flag: `false`

## Lifecycle model

Release directories are immutable side-by-side objects. Runtime/operator state, evidence and active-selection metadata are separate.

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

Upgrade from RC1-held to RC2-qualified installs RC2 alongside RC1 and changes only the active release pointer after RC2 verification. Rollback changes the pointer back to RC1 while preserving both release trees and evidence.

Because RC1 has a known installation-contract defect, rollback preservation evidence does not qualify or recommend RC1 for normal operation.

## Executed lifecycle evidence

Using the exact retained RC1 workflow artifact and exact RC2 archive:

- RC1 archive digest verified — PASS;
- RC2 archive digest verified — PASS;
- RC1 tree preserved through upgrade — PASS;
- RC2 tree preserved through rollback — PASS;
- evidence state preserved through both transitions — PASS;
- upgrade pointer transition — PASS;
- rollback pointer transition — PASS.

Lifecycle result: `SIDE_BY_SIDE_RELEASES_POINTER_ONLY_SWITCH`.

## Trust/provenance boundary

CS-IEF-14B identity-bound provenance remains valid evidence for RC2. The separate sovereign Ed25519 trust constitution remains inactive until an accepted signer is explicitly activated.

`ATTESTED_IDENTITY_BOUND != SOVEREIGN_TRUSTED`

## Stable-readiness adjudication

Current publication state:

`PUBLISHED_PRERELEASE_QUALIFIED_ATTESTED`

Current stable readiness:

`STABLE_BLOCKED`

Current mandatory blocker:

- `SOVEREIGN_TRUST_POLICY_NOT_ACTIVE`

Observed platform property:

- GitHub release object reports `immutable: false`.

No execution mode is authorized and no provider/EAC qualification is inferred.

## Machine evidence

- `release/RC2_PUBLICATION_RESULT.json`
- `release/RC2_LIFECYCLE_RESULT.json`
- `release/RC2_ATTESTATION_RESULT.json`
- `release/RC2_RELEASE_WITNESS.json`
- `release/RC2.yaml`

Workflow evidence artifact:

- run: `33864229370`
- artifact ID: `9933306966`
- artifact digest: `sha256:68477cb255898e6b0f421f2ef4539b94a83865c7fc440a69a56302aaac3758fa`

## Closure

CS-IEF-15 is closed at the measured publication/lifecycle level. The exact RC2 artifact is publicly available as a qualified, identity-bound-attested prerelease; the tag is bound to the frozen RC2 source; lifecycle preservation passed using real RC1 and RC2 artifacts; and stable readiness remains explicitly blocked rather than inferred from publication.
