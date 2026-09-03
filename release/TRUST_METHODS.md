# CS-IEF-14A Trust Method Profiles

The TrustRootPolicy is method-agnostic at the constitutional level. Two initial operational profiles are recognized.

## Profile A — identity-bound keyless attestation (preferred automation path)

Use an identity-bound, short-lived signing credential with transparency/provenance evidence, such as Sigstore keyless signing or GitHub Artifact Attestations where the release workflow and repository permissions support it.

Policy evaluation MUST validate both the cryptographic attestation and the accepted signer/workflow identity. Repository or workflow identity is not trusted merely because an attestation exists.

This profile avoids storing a long-lived private signing key in CI and is preferred for automated release provenance.

## Profile B — sovereign offline Ed25519 detached signature

Use an operator-controlled Ed25519 key generated and held outside GitHub, Google Drive, release bundles, CI logs, and project repositories. Publish only the SignerPublicRecord and detached signature envelope.

This profile is appropriate when a long-lived sovereign trust root is intentionally desired and its custody can be protected independently of CI.

## Combination

A future policy version may require both an identity-bound build attestation and a sovereign release signature. Their meanings remain distinct:

- build/workflow attestation: who/what build identity produced or attested the artifact;
- release signature: accepted release authority signed the exact release identity;
- trust decision: policy adjudication over accepted identities/signers, scope, threshold and revocation state.

No method may imply `SAFE`, `PLATFORM_QUALIFIED`, or `EXECUTION_AUTHORIZED` by itself.
