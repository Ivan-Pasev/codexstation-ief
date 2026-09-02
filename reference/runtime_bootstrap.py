"""CS-IEF-09 provider-neutral portable runtime bootstrap reference.

This module verifies semantic release inputs and selects only modes supported by
explicit qualification evidence. It never materializes an execution provider.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Mapping, Sequence


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + sha256(canonical_json(value)).hexdigest()


MODE_REQUIREMENTS = {
    "OMEGA_KNOWLEDGE_ONLY": None,
    "OMEGA_POLICY_ONLY": None,
    "IEF_HOST_PROCESS": 1,
    "IEF_CONTAINER": 2,
    "IEF_MICROVM": 3,
    "IEF_REMOTE": 4,
}


def verify_artifacts(*, declared: Sequence[Mapping[str, str]], observed: Mapping[str, str]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    for artifact in declared:
        path = artifact["path"]
        expected = artifact["digest"]
        actual = observed.get(path)
        if actual is None:
            failures.append(f"missing:{path}")
        elif actual != expected:
            failures.append(f"digest:{path}")
    return not failures, failures


def discover(descriptors: Sequence[Mapping[str, object]]) -> list[dict]:
    """Normalize explicit provider observations without assigning assurance."""
    return [
        {
            "provider_id": str(d["provider_id"]),
            "provider_version": str(d.get("provider_version", "UNKNOWN")),
            "adapter_abi": str(d.get("adapter_abi", "UNKNOWN")),
            "candidate_modes": sorted(str(x) for x in d.get("candidate_modes", [])),
            "capability_manifest_digest": d.get("capability_manifest_digest"),
            "health": str(d.get("health", "UNKNOWN")),
            "availability": str(d.get("availability", "UNKNOWN")),
        }
        for d in sorted(descriptors, key=lambda x: str(x["provider_id"]))
    ]


def select_mode(*, requested_mode: str, discovered: Sequence[Mapping[str, object]],
                qualifications: Mapping[str, Mapping[str, object]],
                permitted_fallbacks: Sequence[str] = ()) -> tuple[str, str | None, list[str]]:
    if requested_mode not in MODE_REQUIREMENTS:
        return "NONE", None, ["unsupported_mode"]
    if MODE_REQUIREMENTS[requested_mode] is None:
        return requested_mode, None, []

    candidates = [requested_mode] + [m for m in permitted_fallbacks if m != requested_mode]
    for mode in candidates:
        required = MODE_REQUIREMENTS.get(mode)
        if required is None:
            return mode, None, ([f"fallback:{requested_mode}->{mode}"] if mode != requested_mode else [])
        for provider in discovered:
            pid = str(provider["provider_id"])
            if mode not in provider.get("candidate_modes", []):
                continue
            q = qualifications.get(pid)
            if not q or not bool(q.get("current", False)):
                continue
            if int(q.get("assigned_eac", -1)) < required:
                continue
            if provider.get("health") != "READY" or provider.get("availability") != "AVAILABLE":
                continue
            degradations = [f"fallback:{requested_mode}->{mode}"] if mode != requested_mode else []
            return mode, pid, degradations
    return "NONE", None, ["qualification_or_provider_unavailable"]


def bootstrap(*, release_manifest: Mapping[str, object], observed_artifact_digests: Mapping[str, str],
              installation_id: str, platform_facts: object, configuration: object,
              provider_descriptors: Sequence[Mapping[str, object]], qualifications: Mapping[str, Mapping[str, object]],
              requested_mode: str, permitted_fallbacks: Sequence[str] = ()) -> dict:
    ok, failures = verify_artifacts(declared=release_manifest["artifacts"], observed=observed_artifact_digests)
    providers = discover(provider_descriptors)
    if not ok:
        effective_mode, selected, degradations, terminal = "NONE", None, [], "REJECTED"
    else:
        effective_mode, selected, degradations = select_mode(
            requested_mode=requested_mode, discovered=providers, qualifications=qualifications,
            permitted_fallbacks=permitted_fallbacks,
        )
        terminal = "READY" if effective_mode != "NONE" else "REJECTED"

    core = {
        "schema_version": "CS-IEF-09",
        "release_digest": release_manifest["release_digest"],
        "distribution_bundle_digest": release_manifest["distribution_bundle_digest"],
        "installation_id": installation_id,
        "platform_facts_digest": digest(platform_facts),
        "configuration_digest": digest(configuration),
        "discovered_providers": providers,
        "qualification_refs": sorted(str(q.get("qualification_digest")) for q in qualifications.values() if q.get("qualification_digest")),
        "requested_mode": requested_mode,
        "effective_mode": effective_mode,
        "selected_provider": selected,
        "omissions": failures,
        "degradations": degradations,
        "phase_outcomes": {"VERIFY": "PASS" if ok else "REJECTED", "DISCOVER": "PASS", "SELECT_MODE": "PASS" if effective_mode != "NONE" else "REJECTED"},
        "installed_artifact_manifest_digest": digest(observed_artifact_digests) if ok else None,
        "terminal_state": terminal,
    }
    return {**core, "receipt_digest": digest(core)}
