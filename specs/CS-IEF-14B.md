# CS-IEF-14B — RC2 Identity-Bound Attestation and Release Witness

Status: CLOSED at GitHub identity-bound attestation level

## Subject

- release: `codexstation-omega-portable 0.1.0-rc2`
- frozen source revision: `1c625a5ce59197ec991f3f6778a0ad63dc0b7002`
- archive SHA-256: `sha256:4110edafaa4b8bc860f359e9532634415164df86a6c26fd439608179bae08cf2`
- release digest: `sha256:3f05883dc5980ca921eadbf2536c5538027e08eb677ce8fc1d3475b0349edb13`

## Attestation execution

GitHub Actions run `33852664106` executed `.github/workflows/attest-rc2.yml` from `refs/heads/main`.

The workflow checked out the frozen RC2 source revision, rebuilt the portable archive, and verified the exact frozen archive digest before attestation. The attestation step then created GitHub artifact attestation `45196448` for the exact archive digest.

The attestation used GitHub Actions OIDC identity and a certificate issued through the Public Good Sigstore instance. The signature was uploaded to the Rekor transparency log at log index `2708913109` and the attestation was uploaded to the repository.

## Verified identity binding

The attestation provenance records:

- repository: `Ivan-Pasev/codexstation-ief`
- workflow: `.github/workflows/attest-rc2.yml`
- workflow ref: `refs/heads/main`
- run: `33852664106`
- runner environment: GitHub-hosted
- event: `push`
- attestation workflow commit: `601a1835ba1d0da6b7679e73f83c4800cb8dbeb4`
- subject digest: exact RC2 archive SHA-256 above

## Claim boundary

This evidence supports the state:

`ATTESTED_IDENTITY_BOUND`

It establishes cryptographically backed build provenance and repository/workflow identity for the frozen RC2 subject.

It does **not** by itself establish:

- sovereign Ed25519 trust-root activation;
- semantic truth;
- safety;
- execution authorization;
- EAC assignment;
- provider qualification;
- platform qualification beyond the independent CS-IEF-13 evidence already recorded.

The CS-IEF-14A sovereign trust policy remains `CONSTITUTION_READY_AWAITING_SIGNER` because `accepted_signers` is empty. GitHub/Sigstore identity-bound attestation is a distinct trust mechanism and does not mutate that signer registry.

## Release witness relation

`RC2_BUILD_RESULT + RC2_QUALIFICATION_RESULT + GitHub_Attestation_45196448 -> RC2_RELEASE_WITNESS`

The witness binds build identity, reproducibility, platform qualification, attestation identity, subject digest, and bounded trust adjudication without conflating provenance with authorization or semantic truth.

## Closure

CS-IEF-14B is CLOSED at the GitHub identity-bound provenance level.

Next layer: CS-IEF-15 — immutable GitHub release/tag publication, release-note/witness publication, upgrade/rollback qualification, and stable-release readiness adjudication while sovereign signer activation remains an optional independent track.
