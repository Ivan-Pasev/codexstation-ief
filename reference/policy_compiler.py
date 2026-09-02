"""Provider-neutral CS-IEF-05 policy compiler reference skeleton.

This module intentionally does not call any execution provider. It demonstrates
fail-closed decision ordering and keeps assurance evidence separate from identity.
"""
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any


class EAC(IntEnum):
    NONE = 0
    HOST_PROCESS = 1
    CONTAINER = 2
    MICROVM = 3
    REMOTE_ATTESTED_VM = 4
    CONFIDENTIAL_ATTESTED_EXECUTION = 5


class Enforcement(IntEnum):
    UNSUPPORTED = 0
    DECLARED = 1
    SOFTWARE_ENFORCED = 2
    HARDWARE_ENFORCED = 3
    ATTESTED = 4


@dataclass(frozen=True)
class Qualification:
    digest: str | None
    qualified_eac: EAC | None
    stale: bool = True


@dataclass(frozen=True)
class Decision:
    authorized: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)
    effective_eac: EAC | None = None
    mapped_controls: tuple[tuple[str, Any], ...] = field(default_factory=tuple)


def compile_policy(*, required_eac: EAC, provider_ready: bool,
                   required_controls: dict[str, Enforcement],
                   qualified_controls: dict[str, Enforcement],
                   qualification: Qualification,
                   semantic_mismatches: tuple[str, ...] = (),
                   unauthorized_degradations: tuple[str, ...] = ()) -> Decision:
    """Return authorization only when every mandatory invariant passes.

    Production implementations must additionally canonicalize/hash inputs, apply
    policy profiles, bind explicit degradation grants, and emit ProviderPlan and
    PolicyDecision digests.
    """
    reasons: list[str] = []
    if not provider_ready:
        reasons.append("PROVIDER_NOT_READY")
    if qualification.digest is None or qualification.qualified_eac is None:
        reasons.append("QUALIFICATION_MISSING")
    elif qualification.stale:
        reasons.append("QUALIFICATION_STALE")
    elif qualification.qualified_eac < required_eac:
        reasons.append("ASSURANCE_INSUFFICIENT")

    for control, minimum in sorted(required_controls.items()):
        actual = qualified_controls.get(control, Enforcement.UNSUPPORTED)
        if actual == Enforcement.UNSUPPORTED:
            reasons.append(f"CAPABILITY_MISSING:{control}")
        elif actual < minimum:
            reasons.append(f"ENFORCEMENT_TOO_WEAK:{control}")

    reasons.extend(f"SEMANTIC_MISMATCH:{x}" for x in semantic_mismatches)
    reasons.extend(f"UNAUTHORIZED_DEGRADATION:{x}" for x in unauthorized_degradations)

    if reasons:
        return Decision(False, tuple(reasons))

    assert qualification.qualified_eac is not None
    return Decision(
        True,
        effective_eac=min(required_eac, qualification.qualified_eac),
        mapped_controls=tuple(sorted(qualified_controls.items())),
    )
