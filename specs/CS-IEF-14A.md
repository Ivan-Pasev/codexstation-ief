# CS-IEF-14A — Public Trust Constitution

Status: CLOSED at public-constitution level / signer activation pending

## Purpose

CS-IEF-14A defines the public trust-root constitution for CodexStation IEF releases. It establishes signer identity, public-key representation, artifact scope, threshold semantics, custody boundaries, revocation, rotation, compromise response, and bootstrap-to-active transition without generating or storing private signing material.

The trust plane evaluates evidence. It does not grant execution authority and it does not convert a valid signature into a claim of safety or semantic correctness.

## Core separation

`SIGNATURE_VALID != TRUSTED != SAFE != PLATFORM_QUALIFIED != EXECUTION_AUTHORIZED`

A signature proves only that a holder of the corresponding private key produced a signature over the bound payload. Trust additionally requires an ACTIVE signer accepted by the current TrustRootPolicy, correct artifact scope, threshold satisfaction, non-revocation, and policy/version correspondence.

## Signer public record

An accepted signer is represented only by public verification material:

- `signer_id` — stable human/organizational signer identity;
- `key_id` — `sha256` fingerprint derived from canonical public-key bytes;
- `algorithm` — initially `ed25519`;
- `public_key` — raw public key bytes encoded as base64;
- `status` — `ACTIVE`, `REVOKED`, `EXPIRED`, or `PENDING`;
- `valid_from`, optional `valid_until`;
- `artifact_scopes` — explicit release families the signer may sign;
- `identity_statement` — bounded public statement of who controls the signing identity;
- optional external identity/provenance references.

Private key material is never part of this record.

## Private-key boundary

Private signing material MUST NOT be stored in:

- the public repository;
- the private lab repository;
- a release archive;
- the canonical Google Drive working tree;
- release evidence bundles;
- workflow logs;
- public witness records.

Generation and custody are operator-controlled outside public project surfaces, preferably offline or hardware-backed. CS-IEF-14A does not authorize CI secret storage. A later explicit operational policy may authorize a separate signing service or hardware-backed automation.

## Initial algorithm profile

The first constitutional profile permits `ed25519` public keys and detached signatures. Algorithm agility is preserved by versioning the signer record and signature envelope schemas rather than silently changing verification semantics.

## Key identifier

`key_id = sha256(canonical_public_key_bytes)`

The key identifier is a fingerprint, not a secret and not a signer identity by itself.

## Artifact scope

The initial trust scope is:

`codexstation-omega-portable`

A signer accepted for this scope is not automatically accepted for other repositories, provider binaries, research evidence, or unrelated GILC artifacts.

## Threshold semantics

The initial threshold is `1`. Trust is satisfied only when the number of distinct valid signatures from ACTIVE, in-scope, non-revoked accepted signers is greater than or equal to the current policy threshold.

Changing threshold semantics requires a TrustRootPolicy version change and new policy digest.

## Signature payload binding

The first detached-signature envelope MUST bind at least:

- release family / artifact scope;
- release ID;
- release version;
- exact archive SHA-256;
- semantic release digest;
- exact source revision;
- trust-policy ID/version/digest;
- signer key ID.

The signature does not sign mutable download URLs, timestamps, mirrors, or UI labels unless explicitly included by a later envelope version.

## Revocation

Revocation is append-only. A revocation record identifies the affected `key_id`, effective time/epoch, reason class, authority/provenance reference, and record digest.

A revoked key cannot satisfy new trust decisions after the effective revocation point. Historical verification may preserve the fact that a signature was cryptographically valid before revocation, but current trust evaluation must expose the revocation state.

## Compromise response

Suspected private-key compromise triggers:

1. immediate signer status transition to `REVOKED` or emergency hold;
2. publication of a revocation record;
3. prohibition on new trust decisions using the affected key;
4. generation of a replacement signer identity/key record outside repository surfaces;
5. explicit policy update and version bump if accepted signer membership changes;
6. re-signing of future releases only after the replacement signer is ACTIVE.

Existing release bytes are never rewritten to erase historical signatures.

## Rotation

Planned rotation may temporarily allow old and new ACTIVE public signer records to overlap. Old-key retirement is explicit. A new key never inherits trust merely because it belongs to the same person or organization; it must appear in the accepted signer set under a versioned policy.

## Bootstrap-to-active transition

TrustRootPolicy v0.2 remains `CONSTITUTION_READY_AWAITING_SIGNER` while `accepted_signers` is empty.

The policy may transition to `ACTIVE` only when all of the following hold:

1. at least one signer public record exists and validates;
2. at least one signer is `ACTIVE` for `codexstation-omega-portable`;
3. the policy threshold can be satisfied by the accepted signer set;
4. the policy digest is published;
5. reference trust-policy validation tests pass;
6. no private-key material is present in public/canonical project surfaces.

Activation is a public policy-state change, not an implicit consequence of key generation.

## RC2 boundary

`codexstation-omega-portable 0.1.0-rc2` remains a valid qualified unsigned release candidate under the current unsigned-RC policy. CS-IEF-14A does not retroactively require RC2 signing and does not alter its qualification evidence.

## Stable-release boundary

The current policy allows unsigned RCs but forbids unsigned stable releases. A stable release therefore requires an ACTIVE trust policy and a threshold-satisfying detached signature set, in addition to its independent technical qualification gates.

## Closure criterion

CS-IEF-14A closes when the public constitution, machine-readable signer/trust-policy schemas, reference policy evaluator, and test vectors exist, while private-key generation and first release signing remain explicitly outside this phase.

Next: CS-IEF-14B — signer activation, detached signature envelope, exact RC signature verification, ReleaseWitness binding, and trust adjudication.