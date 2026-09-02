import pytest

from reference.omega_compiler import ConstitutionalDrift, compile_omega, is_stale


INVARIANTS = {
    "EFFECTIVE_AUTHORITY_SUBSET_AUTHORIZED": "EffectiveAuthority <= AuthorizedAuthority",
    "ISOLATION_NOT_AUTHORIZATION": "Isolation != Authorization",
    "WITNESSED_NOT_TRUE": "WITNESSED(x) != TRUE(x)",
    "NO_SILENT_EAC_PROMOTION": "Reported assurance never exceeds qualified assurance",
    "NO_AMBIENT_SECRETS": "Secrets are non-ambient",
}


def build(**overrides):
    args = dict(
        omega_version="0.2.0",
        compiler_version="0.1.0",
        surface_id="portable",
        mandatory_invariants=tuple(INVARIANTS),
        canonical_invariants=INVARIANTS,
        requested_capabilities=("execution", "sources"),
        available_capabilities=("sources",),
        source_manifest={"sources": ["public-core"]},
        capability_manifest={"sources": True, "execution": False},
        surface_profile={"surface": "portable"},
        component_digests={"core": "sha256:core", "ief": "sha256:ief"},
    )
    args.update(overrides)
    return compile_omega(**args)


def test_same_inputs_same_bundle_digest():
    assert build()["bundle_digest"] == build()["bundle_digest"]


def test_missing_invariant_fails_closed():
    bad = dict(INVARIANTS)
    bad.pop("WITNESSED_NOT_TRUE")
    with pytest.raises(ConstitutionalDrift):
        build(canonical_invariants=bad)


def test_unavailable_capability_is_disclosed_not_simulated():
    b = build()
    assert "execution" in b["unsupported_capabilities"]
    assert "capability:execution" in b["omissions"]


def test_capability_change_changes_bundle():
    a = build()
    b = build(available_capabilities=("sources", "execution"), capability_manifest={"sources": True, "execution": True})
    assert a["bundle_digest"] != b["bundle_digest"]


def test_source_change_changes_bundle():
    a = build()
    b = build(source_manifest={"sources": ["public-core", "extra"]})
    assert a["bundle_digest"] != b["bundle_digest"]


def test_domain_crystal_change_changes_bundle():
    assert build(domain_crystals=())["bundle_digest"] != build(domain_crystals=("physics",))["bundle_digest"]


def test_drift_detection():
    assert is_stale(recorded_inputs={"core": "a"}, current_inputs={"core": "b"})
    assert not is_stale(recorded_inputs={"core": "a"}, current_inputs={"core": "a"})
