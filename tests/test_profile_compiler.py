import pytest
from reference.profile_compiler import ProfileError, compile_profile, formal_proof_status, verify_reproducibility

PROFILE = {
    "profile_id": "research.reproducible",
    "profile_version": "0.1.0",
    "profile_type": "RESEARCH",
    "network_default": "NONE",
    "reproducibility_mode": "R2_PINNED_TOOLCHAIN",
    "evidence_requirements": ["execution_receipt_digest"],
}


def test_profile_defaults_are_restrictive():
    out = compile_profile(PROFILE, {})
    assert out["network"]["mode"] == "NONE"
    assert out["persistence"]["mode"] == "EPHEMERAL"


def test_network_requires_explicit_authority():
    with pytest.raises(ProfileError, match="NETWORK_AUTHORITY_NOT_EXPLICIT"):
        compile_profile(PROFILE, {"network": {"mode": "ALLOWLIST"}})


def test_raw_guest_secret_rejected():
    with pytest.raises(ProfileError, match="RAW_GUEST_SECRETS_FORBIDDEN"):
        compile_profile(PROFILE, {"secrets": {"raw_guest_secrets": True}})


def test_mutable_host_bind_rejected():
    with pytest.raises(ProfileError, match="MUTABLE_HOST_BIND_FORBIDDEN_BY_PROFILE"):
        compile_profile(PROFILE, {"filesystem": {"mutable_host_bind": True}})


def test_reproducibility_overclaim_rejected():
    with pytest.raises(ProfileError, match="REPRODUCIBILITY_OVERCLAIM"):
        verify_reproducibility("R3_DETERMINISTIC_REPLAY", "R2_PINNED_TOOLCHAIN")


def test_formal_proof_requires_full_external_evidence():
    assert formal_proof_status(exit_code=0, target_matched=True, pinned_toolchain=True, pinned_dependencies=True) == "FORMALLY_CHECKED"
    assert formal_proof_status(exit_code=1, target_matched=True, pinned_toolchain=True, pinned_dependencies=True) == "NOT_FORMALLY_CHECKED"
    assert formal_proof_status(exit_code=0, target_matched=True, pinned_toolchain=False, pinned_dependencies=True) == "NOT_FORMALLY_CHECKED"
