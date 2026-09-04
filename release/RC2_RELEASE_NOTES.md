# CodexStation Ω Portable 0.1.0-rc2

Status: **qualified, identity-bound attested prerelease**.

This release candidate is the first CodexStation Ω portable package to satisfy the public CS-IEF release pipeline through reproducible build, cross-platform knowledge-only qualification, and GitHub/Sigstore identity-bound provenance.

## Exact identity

- source revision: `1c625a5ce59197ec991f3f6778a0ad63dc0b7002`
- archive SHA-256: `4110edafaa4b8bc860f359e9532634415164df86a6c26fd439608179bae08cf2`
- release digest: `sha256:3f05883dc5980ca921eadbf2536c5538027e08eb677ce8fc1d3475b0349edb13`
- distribution digest: `sha256:e20325d2555d04adf1896f911c0ab88f24cd8daca50d28daa746b29644789e6f`
- source-graph digest: `sha256:dd8f020f2e1c5ad4e8bfffcb531072d907678b2320df440137e54c2619e4467d`

## Evidenced properties

- BR3 independent-environment reproducibility across Linux and Windows.
- Byte-identical normalized ZIP across the measured Linux/Windows build environments.
- `QUALIFIED_KNOWLEDGE_ONLY` on Linux x86_64 and Windows x86_64.
- Provider-free baseline: `provider = NONE`.
- No EAC claim and no qualified execution-provider mode.
- GitHub artifact attestation ID `45196448`.
- GitHub Actions OIDC identity bound to `Ivan-Pasev/codexstation-ief/.github/workflows/attest-rc2.yml@refs/heads/main`.
- Public Good Sigstore certificate and Rekor transparency-log entry `2708913109`.

## Release witness

See:

- `release/RC2_BUILD_RESULT.json`
- `release/RC2_QUALIFICATION_RESULT.json`
- `release/RC2_ATTESTATION_RESULT.json`
- `release/RC2_RELEASE_WITNESS.json`
- `release/RC2.yaml`

## Claim boundary

This prerelease does **not** claim sovereign Ed25519 trust, arbitrary safety, stable-release status, execution authorization, Microsandbox qualification, or EAC-3.

`PUBLISHED != STABLE != SOVEREIGN_TRUSTED != EXECUTION_AUTHORIZED`

The separate sovereign trust constitution remains in `CONSTITUTION_READY_AWAITING_SIGNER` state.

## Historical RC1

RC1 remains preserved as historical evidence and is held for an installation-contract defect. Lifecycle rollback preservation involving RC1 does not qualify or recommend RC1 for normal operation.
