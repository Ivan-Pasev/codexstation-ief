from reference.policy_compiler import EAC, Enforcement, Qualification, compile_policy


def base(**overrides):
    args = dict(
        required_eac=EAC.MICROVM,
        provider_ready=True,
        required_controls={"network.none": Enforcement.SOFTWARE_ENFORCED},
        qualified_controls={"network.none": Enforcement.SOFTWARE_ENFORCED},
        qualification=Qualification("q1", EAC.MICROVM, stale=False),
    )
    args.update(overrides)
    return compile_policy(**args)


def test_authorizes_exact_fit():
    d = base()
    assert d.authorized
    assert d.effective_eac == EAC.MICROVM


def test_missing_qualification_fails_closed():
    d = base(qualification=Qualification(None, None, stale=True))
    assert not d.authorized
    assert "QUALIFICATION_MISSING" in d.reasons


def test_stale_qualification_fails_closed():
    d = base(qualification=Qualification("q1", EAC.MICROVM, stale=True))
    assert not d.authorized
    assert "QUALIFICATION_STALE" in d.reasons


def test_assurance_insufficient():
    d = base(qualification=Qualification("q1", EAC.CONTAINER, stale=False))
    assert not d.authorized
    assert "ASSURANCE_INSUFFICIENT" in d.reasons


def test_enforcement_too_weak():
    d = base(qualified_controls={"network.none": Enforcement.DECLARED})
    assert not d.authorized
    assert "ENFORCEMENT_TOO_WEAK:network.none" in d.reasons


def test_semantic_substitution_rejected():
    d = base(semantic_mismatches=("network.none->deny_all_interface",))
    assert not d.authorized
    assert any(x.startswith("SEMANTIC_MISMATCH:") for x in d.reasons)


def test_unauthorized_degradation_rejected():
    d = base(unauthorized_degradations=("secret.brokered->raw_env",))
    assert not d.authorized
    assert any(x.startswith("UNAUTHORIZED_DEGRADATION:") for x in d.reasons)
