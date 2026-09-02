# CS-IEF-10 — Release Engineering, Reproducible Build Attestation and Platform Qualification

Status: normative/reference release-engineering contract

## 1. Purpose

CS-IEF-10 defines the evidence boundary for producing, attesting, signing, verifying and qualifying portable Ω release candidates. It closes the gap between a CS-IEF-09 installable package and a release artifact whose provenance, reproducibility and platform support claims are inspectable.

The governing claim boundary is:

`BUILT != REPRODUCED != ATTESTED != SIGNED != TRUSTED != QUALIFIED != AUTHORIZED`

No stage silently upgrades into the next.

## 2. Release pipeline

`SOURCE_STATE -> BUILD_RECIPE -> BUILD -> ARTIFACT_SET -> ATTEST -> SIGN(optional) -> VERIFY -> PLATFORM_QUALIFY -> RELEASE_CANDIDATE`

Execution authorization remains outside this pipeline and still requires CS-IEF-05.

## 3. Reproducible build contract

A BuildRecipe binds all semantic build inputs needed to reproduce a release candidate:

- source repository and exact commit/ref;
- CS-IEF specification root;
- Ω manifest/version;
- compiler/runtime tool versions;
- selected source manifests and digests;
- surface profile and capability manifest digests;
- domain crystal selection;
- normalization policy;
- packaging format and deterministic metadata rules;
- dependency/toolchain lock identities;
- build command graph;
- expected output classes.

Time, hostname, absolute local path, filesystem enumeration order, archive timestamps and other non-semantic host facts MUST NOT influence the semantic release digest unless explicitly declared as inputs.

## 4. Build reproducibility levels

- `BR0_SINGLE_BUILD` — one observed build only.
- `BR1_RECIPE_BOUND` — one build with complete recipe/input digest binding.
- `BR2_REPEATABLE_SAME_ENV` — repeated build in same qualified environment yields matching semantic artifact digests.
- `BR3_REPRODUCIBLE_INDEPENDENT_ENV` — an independently instantiated environment reproduces the semantic artifact set from the same recipe.
- `BR4_DIVERSE_REPRODUCTION` — reproduction additionally varies a declared independent build dimension while preserving the declared semantic outputs.

`BR_REPORTED <= BR_EVIDENCED`.

Archive byte identity is a stronger optional claim than semantic artifact-set identity and MUST be stated separately.

## 5. Build attestation

A BuildAttestation is an append-only evidence object binding:

- BuildRecipe digest;
- source commit/tree identity;
- builder identity class;
- environment/toolchain digest;
- input manifest digest;
- output ReleaseManifest digest;
- artifact-set digest;
- reproducibility level evidenced;
- independent reproduction references where applicable;
- policy/normalization version;
- timestamp as observation metadata only;
- attestation digest.

Attestation asserts correspondence between declared build inputs/process and observed outputs. It does not prove absence of malicious source, toolchain compromise, semantic truth or product safety.

## 6. Signing and trust roots

Signing is optional at the specification layer but, when used, MUST bind the exact release digest and preferably the BuildAttestation digest.

A signature establishes possession/use of a signing key according to the verifier's cryptographic assumptions. It does not by itself establish that the signer is trusted or that the release is safe.

Trust policy therefore treats the following separately:

- `signature_valid`;
- `key_identity`;
- `trust_root`;
- `key_status` / revocation state;
- `release_policy_acceptance`.

`SIGNED(x) != TRUSTED(x)`.

## 7. Supply-chain evidence

The release candidate SHOULD publish machine-readable references for:

- source commit;
- BuildRecipe;
- BuildAttestation;
- ReleaseManifest;
- artifact digests;
- signature material or signature reference if present;
- SBOM/dependency inventory where applicable;
- source/license manifests;
- platform qualification records;
- known limitations and unsupported modes.

No secret, private-lab path or private qualification artifact is embedded in a public RC.

## 8. Platform qualification

Platform support is evidence-driven. Each platform qualification record binds at minimum:

- platform class and architecture;
- OS/runtime version range actually tested;
- installer/verifier version;
- release digest tested;
- bootstrap mode tested;
- provider mode tested, if any;
- test vector results;
- limitations;
- qualification outcome;
- evidence/receipt references.

Outcome classes:

- `UNTESTED`
- `PARTIAL`
- `QUALIFIED_KNOWLEDGE_ONLY`
- `QUALIFIED_POLICY_ONLY`
- `QUALIFIED_EXECUTION_MODE`
- `FAILED`

A platform may be qualified for knowledge-only operation while execution modes remain unqualified.

## 9. Offline verifier

A conformant verifier MUST be capable of checking, without network access when all required evidence is locally supplied:

1. ReleaseManifest integrity;
2. artifact digests;
3. BuildRecipe/BuildAttestation correspondence;
4. signature validity when a signature is supplied;
5. trust-policy acceptance separately from signature validity;
6. platform qualification record binding to the exact release digest;
7. claim-boundary consistency.

The verifier MUST report unavailable evidence rather than assuming it.

## 10. First release candidate

The first target is:

`codexstation-omega-portable 0.1.0-rc1`

Mandatory properties:

- provider = NONE;
- supported baseline mode = `OMEGA_KNOWLEDGE_ONLY`;
- deterministic semantic ReleaseManifest;
- reproducible build recipe;
- offline integrity verification;
- BuildAttestation schema and reference generator;
- no private-lab material or raw secrets;
- explicit unsupported execution modes;
- no EAC claim beyond qualification evidence.

The RC may be released unsigned while signing policy is being qualified, but this MUST be explicit in its metadata.

## 11. RC promotion criteria

An RC may be promoted only when:

- all mandatory release artifacts exist;
- semantic release digest rebuild is deterministic under the claimed level;
- tamper tests fail closed;
- offline verifier passes on the candidate artifact set;
- source/license/disclosure review passes;
- at least one declared platform qualification result is evidence-backed;
- no unsupported provider/platform claim is presented as qualified;
- release notes state signing/trust status explicitly.

## 12. Witness bridge

BuildRecipe, BuildAttestation, ReleaseManifest, signature verification, platform qualification and release promotion may each become CS-IEF-07 witness subjects. The witness graph preserves provenance and ordering without upgrading build or platform evidence into semantic truth.

## 13. Closure criterion

CS-IEF-10 closes at normative/reference level when the BuildAttestation schema, platform qualification schema/matrix, release recipe, offline verifier/reference builder, first portable RC manifest and release claim-boundary documentation are present. A public binary/archive release and empirical multi-platform qualification remain release operations requiring their own evidence.
