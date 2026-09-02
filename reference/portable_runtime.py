"""CS-IEF-09 provider-neutral portable/local bootstrap reference.

Demonstrates deterministic release manifests, integrity verification,
qualification-aware mode selection, and knowledge-only installation.
It does not assign empirical provider assurance.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Mapping, Sequence

MODES = (
    "OMEGA_KNOWLEDGE_ONLY",
    "OMEGA_POLICY_ONLY",
    "IEF_HOST_PROCESS",
    "IEF_CONTAINER",
    "IEF_MICROVM",
    "IEF_REMOTE",
)

class BootstrapRejected(ValueError):
    pass


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + sha256(canonical_json(value)).hexdigest()


def bytes_digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def build_release_manifest(*, release_id: str, release_version: str,
                           spec_root: str, omega_version: str,
                           distribution_bundle_digest: str,
                           compiler_id: str, compiler_version: str,
                           artifacts: Mapping[str, bytes],
                           source_graph_digest: str,
                           supported_platform_classes: Sequence[str] = ("portable",)) -> dict:
    rows = [
        {"path": p, "type": "file", "digest": bytes_digest(artifacts[p])}
        for p in sorted(artifacts)
    ]
    core = {
        "schema_version": "CS-IEF-09",
        "release_id": release_id,
        "release_version": release_version,
        "spec_root": spec_root,
        "omega_version": omega_version,
        "distribution_bundle_digest": distribution_bundle_digest,
        "compiler": {"id": compiler_id, "version": compiler_version},
        "artifacts": rows,
        "supported_platform_classes": sorted(set(supported_platform_classes)),
        "required_bootstrap_capabilities": [],
        "optional_provider_adapters": [],
        "provider_qualification_requirements": [],
        "source_graph_digest": source_graph_digest,
        "license_metadata": {},
        "build_provenance_ref": None,
    }
    return {**core, "release_digest": digest(core)}


def verify_release(manifest: Mapping[str, object], artifacts: Mapping[str, bytes]) -> None:
    for row in manifest.get("artifacts", []):
        path = row["path"]
        if path not in artifacts:
            raise BootstrapRejected(f"MISSING_ARTIFACT:{path}")
        if bytes_digest(artifacts[path]) != row["digest"]:
            raise BootstrapRejected(f"INTEGRITY_MISMATCH:{path}")


def select_mode(*, requested_mode: str, providers: Sequence[Mapping[str, object]],
                allow_fallback: bool = False) -> tuple[str, str | None, list[str]]:
    if requested_mode not in MODES:
        raise BootstrapRejected("UNKNOWN_MODE")
    if requested_mode in {"OMEGA_KNOWLEDGE_ONLY", "OMEGA_POLICY_ONLY"}:
        return requested_mode, None, []

    for provider in providers:
        modes = set(provider.get("qualified_modes", []))
        if requested_mode in modes and provider.get("qualification_current") is True:
            return requested_mode, str(provider.get("provider_id")), []

    if allow_fallback:
        return "OMEGA_KNOWLEDGE_ONLY", None, [f"mode:{requested_mode}->OMEGA_KNOWLEDGE_ONLY"]
    raise BootstrapRejected("NO_QUALIFIED_PROVIDER_FOR_REQUESTED_MODE")


def install_knowledge_only(*, release_manifest: Mapping[str, object], artifacts: Mapping[str, bytes],
                           installation_id: str, platform_facts: object, configuration: object) -> dict:
    verify_release(release_manifest, artifacts)
    core = {
        "schema_version": "CS-IEF-09",
        "release_digest": release_manifest["release_digest"],
        "distribution_bundle_digest": release_manifest["distribution_bundle_digest"],
        "installation_id": installation_id,
        "platform_facts_digest": digest(platform_facts),
        "configuration_digest": digest(configuration),
        "discovered_providers": [],
        "qualification_refs": [],
        "requested_mode": "OMEGA_KNOWLEDGE_ONLY",
        "effective_mode": "OMEGA_KNOWLEDGE_ONLY",
        "selected_provider": None,
        "omissions": ["execution_provider:NONE"],
        "degradations": [],
        "phase_outcomes": {"VERIFY":"PASS","INSTANTIATE":"PASS","DISCOVER":"PASS","QUALIFY":"NOT_REQUIRED","SELECT_MODE":"PASS","INSTALL":"PASS","READY":"PASS"},
        "installed_artifact_manifest_digest": digest(release_manifest["artifacts"]),
        "terminal_state": "READY",
    }
    return {**core, "receipt_digest": digest(core)}
