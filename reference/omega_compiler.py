"""CS-IEF-08 deterministic Ω distribution compiler reference skeleton.

This reference demonstrates invariant coverage, capability projection, explicit
omissions, and content-addressed bundle manifests. It intentionally does not
encode permanent knowledge of any vendor's live product capabilities.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable, Mapping, Sequence


class ConstitutionalDrift(ValueError):
    pass


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + sha256(canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class Artifact:
    path: str
    type: str
    content: str

    @property
    def content_digest(self) -> str:
        return "sha256:" + sha256(self.content.encode("utf-8")).hexdigest()


def compile_omega(*, omega_version: str, compiler_version: str,
                  surface_id: str, mandatory_invariants: Sequence[str],
                  canonical_invariants: Mapping[str, str],
                  requested_capabilities: Iterable[str],
                  available_capabilities: Iterable[str],
                  source_manifest: object, capability_manifest: object,
                  surface_profile: object, component_digests: Mapping[str, str],
                  domain_crystals: Sequence[str] = ()) -> dict:
    """Compile a provider-neutral semantic bundle manifest.

    The skeleton emits a semantic manifest rather than vendor-specific prompt
    text. Production emitters can generate target artifacts only after this
    invariant/capability projection succeeds.
    """
    missing = sorted(set(mandatory_invariants) - set(canonical_invariants))
    if missing:
        raise ConstitutionalDrift("CONSTITUTIONAL_DRIFT:" + ",".join(missing))

    requested = set(requested_capabilities)
    available = set(available_capabilities)
    unsupported = sorted(requested - available)
    effective = sorted(requested & available)

    semantic_manifest = {
        "surface": surface_id,
        "omega_version": omega_version,
        "invariants": {k: canonical_invariants[k] for k in sorted(mandatory_invariants)},
        "effective_capabilities": effective,
        "unsupported_capabilities": unsupported,
        "domain_crystals": sorted(domain_crystals),
        "component_digests": dict(sorted(component_digests.items())),
    }
    artifact = Artifact("MANIFEST.semantic.json", "semantic-manifest", canonical_json(semantic_manifest).decode())

    bundle_core = {
        "schema_version": "CS-IEF-08",
        "target_surface": surface_id,
        "omega_version": omega_version,
        "compiler_version": compiler_version,
        "source_graph_digest": digest(source_manifest),
        "capability_manifest_digest": digest(capability_manifest),
        "surface_profile_digest": digest(surface_profile),
        "artifacts": [{"path": artifact.path, "type": artifact.type, "digest": artifact.content_digest}],
        "omissions": [f"capability:{x}" for x in unsupported],
        "unsupported_capabilities": unsupported,
        "capability_degradations": [],
        "constitutional_equivalence": "PASS",
        "stale": False,
    }
    return {**bundle_core, "bundle_digest": digest(bundle_core)}


def is_stale(*, recorded_inputs: Mapping[str, str], current_inputs: Mapping[str, str]) -> bool:
    """Detect canonical/compiler/profile/source/capability drift by digest map."""
    return dict(recorded_inputs) != dict(current_inputs)
