# CS-IEF-12 — Independent Reproduction, Platform Qualification and RC Adjudication

Status: canonical empirical qualification/adjudication layer

## Purpose

CS-IEF-12 defines the evidence process that decides whether a built portable Omega release candidate may be promoted, held or rejected after independent-environment reproduction and real platform bootstrap attempts.

The central separation is:

`BUILT != REPRODUCED != INSTALLABLE != PLATFORM_QUALIFIED != SIGNED != TRUSTED != AUTHORIZED`

## RC1 empirical record

Target: `codexstation-omega-portable 0.1.0-rc1`

Exact source revision: `2c433220ecdfbb977a3d4c96b6c326649147c3e9`

Cross-environment qualification run: GitHub Actions run `33679584508`.

Ubuntu and Windows runners independently rebuilt the exact source revision with the same normalized semantic build algorithm. Both completed successfully and independently passed archive-internal integrity verification.

Observed semantic release digest on both platforms:

`sha256:54641842fbbc2096b9ec17d55f58ae0617794e79e01a4e309e314ee4191025b5`

Observed archive digests:

- Linux: `sha256:b176ce37fd040f6d4dbc309af0a26cd396c529c75983d0ead1622554846028a5`
- Windows: `sha256:f0fde599a3b1e8f4f597c3d5fe2244308f535a778f3b426d94738aba3ea33071`

The extracted file trees are byte-identical. The ZIP archives are not byte-identical because entry ordering differs across platform `pathlib` sorting semantics. Therefore RC1 evidences independent-environment semantic reproduction but not cross-platform byte-identical archive reproduction.

Evidenced reproducibility class:

`BR3_REPRODUCIBLE_INDEPENDENT_ENV_SEMANTIC`

## Platform installation result

A separate Linux extraction/integrity/install attempt was run against the exact RC1 bytes stored from the successful CI build.

Archive integrity passed. The packaged `reference/portable_runtime.py` then failed before `READY` because the generated `MANIFEST.json` does not satisfy the runtime/canonical ReleaseManifest contract.

Blocking defects:

1. Artifact records in generated `MANIFEST.json` use key `sha256`, while the canonical release schema and packaged runtime use `digest`.
2. Generated `MANIFEST.json` omits `distribution_bundle_digest`, which the packaged runtime requires.
3. The generated manifest also omits canonical ReleaseManifest fields including `compiler`, `supported_platform_classes`, and `source_graph_digest`.
4. Cross-platform ZIP entry ordering is not explicitly normalized by relative POSIX path, preventing byte-identical archive reproduction.

The first three defects block `QUALIFIED_KNOWLEDGE_ONLY` for RC1. The fourth does not invalidate semantic reproduction but blocks a stronger archive-byte reproducibility claim.

## Promotion decision

`RC1 -> HOLD_INSTALL_CONTRACT_DEFECT`

RC1 MUST NOT be represented as platform-qualified, installable, signed, trusted, execution-qualified or EAC-bearing.

## Required corrective candidate

The next candidate is `0.1.0-rc2` and MUST:

1. generate a ReleaseManifest conforming to `schemas/release-manifest.schema.json`;
2. use canonical `digest` artifact fields;
3. bind `distribution_bundle_digest`, compiler identity/version, supported platform classes and source graph digest;
4. validate manifest contract before archive creation;
5. run the packaged `install_knowledge_only()` path during CI, not merely archive-integrity checks;
6. sort archive entries explicitly by POSIX relative path independent of host path semantics;
7. reproduce on Linux and Windows;
8. compare semantic release digest, extracted tree and archive digest separately;
9. qualify at least one exact platform for `QUALIFIED_KNOWLEDGE_ONLY` before promotion;
10. remain provider-free and carry no EAC claim.

## Claim boundaries

- Same release digest does not imply byte-identical archive.
- Byte-identical extracted trees do not imply packaged runtime compatibility.
- Archive integrity does not imply schema conformance.
- Cross-platform build success does not imply platform installation qualification.
- Platform knowledge-only qualification does not imply execution-provider qualification.
- Signing does not repair a defective artifact.
- Trust policy does not override failed technical qualification.

## Closure

CS-IEF-12 closes with RC1 held, BR3 semantic reproduction evidenced across Linux/Windows, platform installation qualification not achieved, and a concrete corrective RC2 gate defined.
