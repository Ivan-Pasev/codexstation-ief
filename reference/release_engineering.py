"""CS-IEF-10 release engineering reference helpers.

Provider-free utilities for deterministic build recipes, attestations, release
claim verification, and platform-qualification binding. No signing keys or
execution providers are embedded here.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Mapping, Sequence


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + sha256(canonical_json(value)).hexdigest()


def artifact_set_digest(artifacts: Mapping[str, str]) -> str:
    return digest(dict(sorted(artifacts.items())))


def build_attestation(*, build_recipe: object, source_revision: str, builder_class: str,
                      environment: object, input_manifest: object,
                      release_manifest_digest: str, artifacts: Mapping[str, str],
                      reproducibility_level: str = "BR1_RECIPE_BOUND",
                      independent_reproduction_refs: Sequence[str] = (),
                      normalization_policy: str = "CS-IEF-10-default",
                      build_policy_version: str = "CS-IEF-10") -> dict:
    core = {
        "schema_version":"CS-IEF-10",
        "build_recipe_digest":digest(build_recipe),
        "source_revision":source_revision,
        "builder_class":builder_class,
        "environment_digest":digest(environment),
        "input_manifest_digest":digest(input_manifest),
        "release_manifest_digest":release_manifest_digest,
        "artifact_set_digest":artifact_set_digest(artifacts),
        "reproducibility_level":reproducibility_level,
        "independent_reproduction_refs":sorted(independent_reproduction_refs),
        "normalization_policy":normalization_policy,
        "build_policy_version":build_policy_version,
        "observation_time":None,
    }
    return {**core,"attestation_digest":digest(core)}


def verify_attestation(*, attestation: Mapping[str, object], build_recipe: object,
                       release_manifest_digest: str, artifacts: Mapping[str, str]) -> list[str]:
    errors: list[str] = []
    if attestation.get("build_recipe_digest") != digest(build_recipe):
        errors.append("BUILD_RECIPE_MISMATCH")
    if attestation.get("release_manifest_digest") != release_manifest_digest:
        errors.append("RELEASE_MANIFEST_MISMATCH")
    if attestation.get("artifact_set_digest") != artifact_set_digest(artifacts):
        errors.append("ARTIFACT_SET_MISMATCH")
    core = dict(attestation)
    recorded = core.pop("attestation_digest", None)
    if recorded != digest(core):
        errors.append("ATTESTATION_DIGEST_MISMATCH")
    return errors


def verify_release_claims(*, signed: bool, signature_valid: bool | None,
                          trust_policy_accepted: bool | None,
                          platform_outcome: str,
                          execution_modes_qualified: Sequence[str]) -> dict:
    """Keep cryptographic, trust, platform and execution claims separate."""
    return {
        "built": True,
        "signed": signed,
        "signature_valid": signature_valid if signed else None,
        "trusted": bool(signed and signature_valid and trust_policy_accepted),
        "platform_qualified": platform_outcome not in {"UNTESTED", "FAILED"},
        "platform_outcome": platform_outcome,
        "execution_modes_qualified": sorted(set(execution_modes_qualified)),
        "authorized": False,
    }


def platform_record(*, platform_class: str, architecture: str, release_digest: str,
                    bootstrap_mode: str, outcome: str, test_results: Sequence[Mapping[str, object]],
                    os_runtime: str = "UNKNOWN", limitations: Sequence[str] = ()) -> dict:
    core = {
        "schema_version":"CS-IEF-10",
        "platform_class":platform_class,
        "architecture":architecture,
        "os_runtime":os_runtime,
        "installer_version":"REFERENCE",
        "verifier_version":"REFERENCE",
        "release_digest":release_digest,
        "bootstrap_mode":bootstrap_mode,
        "provider_mode":None,
        "test_results":[dict(x) for x in test_results],
        "limitations":list(limitations),
        "outcome":outcome,
    }
    return {**core,"qualification_digest":digest(core)}
