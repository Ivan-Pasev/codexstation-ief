"""CS-IEF-06 reference profile compiler.

Profiles only constrain/construct ExecutionSpec-like dictionaries. They do not
call providers and must never widen originating authority.
"""
from copy import deepcopy

ORDER = {
    "R0_EXPLORATORY": 0,
    "R1_PINNED_INPUTS": 1,
    "R2_PINNED_TOOLCHAIN": 2,
    "R3_DETERMINISTIC_REPLAY": 3,
    "R4_INDEPENDENT_REPLICATION": 4,
}


class ProfileError(ValueError):
    pass


def compile_profile(profile: dict, intent: dict) -> dict:
    out = deepcopy(intent)
    out["profile_id"] = profile["profile_id"]
    out["profile_version"] = profile["profile_version"]
    out["profile_type"] = profile["profile_type"]

    # Restrictive defaults.
    requested_net = out.get("network", {}).get("mode", "NONE")
    if profile.get("network_default") == "NONE" and requested_net != "NONE":
        if not out.get("authority", {}).get("network_explicitly_authorized", False):
            raise ProfileError("NETWORK_AUTHORITY_NOT_EXPLICIT")
    out.setdefault("network", {})["mode"] = requested_net if requested_net != "NONE" else "NONE"

    if out.get("secrets", {}).get("raw_guest_secrets"):
        raise ProfileError("RAW_GUEST_SECRETS_FORBIDDEN")
    if out.get("filesystem", {}).get("mutable_host_bind"):
        raise ProfileError("MUTABLE_HOST_BIND_FORBIDDEN_BY_PROFILE")
    if out.get("filesystem", {}).get("shared_mutable"):
        raise ProfileError("SHARED_MUTABLE_FORBIDDEN_BY_PROFILE")

    out.setdefault("persistence", {})["mode"] = "EPHEMERAL"
    out.setdefault("evidence", {})["required"] = list(profile["evidence_requirements"])
    out["reproducibility_mode"] = profile["reproducibility_mode"]
    return out


def verify_reproducibility(claimed: str, achieved: str) -> None:
    if ORDER[achieved] < ORDER[claimed]:
        raise ProfileError("REPRODUCIBILITY_OVERCLAIM")


def formal_proof_status(*, exit_code: int, target_matched: bool,
                        pinned_toolchain: bool, pinned_dependencies: bool) -> str:
    if exit_code == 0 and target_matched and pinned_toolchain and pinned_dependencies:
        return "FORMALLY_CHECKED"
    return "NOT_FORMALLY_CHECKED"
