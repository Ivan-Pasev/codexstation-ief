from reference.release_engineering import (
    artifact_set_digest, build_attestation, digest, platform_record,
    verify_attestation, verify_release_claims,
)


def test_attestation_is_deterministic_without_wallclock():
    kwargs = dict(
        build_recipe={"release":"rc1"}, source_revision="abc", builder_class="REFERENCE",
        environment={"python":"x"}, input_manifest={"a":"b"},
        release_manifest_digest=digest("manifest"), artifacts={"a":digest("a")},
    )
    a = build_attestation(**kwargs)
    b = build_attestation(**kwargs)
    assert a["attestation_digest"] == b["attestation_digest"]


def test_artifact_mutation_breaks_attestation_correspondence():
    recipe = {"release":"rc1"}
    att = build_attestation(
        build_recipe=recipe, source_revision="abc", builder_class="REFERENCE",
        environment={}, input_manifest={}, release_manifest_digest=digest("manifest"),
        artifacts={"a":digest("a")},
    )
    errors = verify_attestation(
        attestation=att, build_recipe=recipe,
        release_manifest_digest=digest("manifest"), artifacts={"a":digest("tampered")},
    )
    assert "ARTIFACT_SET_MISMATCH" in errors


def test_signed_is_not_automatically_trusted_or_authorized():
    claims = verify_release_claims(
        signed=True, signature_valid=True, trust_policy_accepted=False,
        platform_outcome="UNTESTED", execution_modes_qualified=[],
    )
    assert claims["signature_valid"] is True
    assert claims["trusted"] is False
    assert claims["authorized"] is False


def test_platform_knowledge_only_does_not_qualify_execution():
    claims = verify_release_claims(
        signed=False, signature_valid=None, trust_policy_accepted=None,
        platform_outcome="QUALIFIED_KNOWLEDGE_ONLY", execution_modes_qualified=[],
    )
    assert claims["platform_qualified"] is True
    assert claims["execution_modes_qualified"] == []


def test_platform_record_binds_exact_release_digest():
    r1 = platform_record(
        platform_class="linux", architecture="x86_64", release_digest=digest("r1"),
        bootstrap_mode="OMEGA_KNOWLEDGE_ONLY", outcome="QUALIFIED_KNOWLEDGE_ONLY",
        test_results=[{"id":"offline_verify","outcome":"PASS","evidence_ref":None}],
    )
    r2 = platform_record(
        platform_class="linux", architecture="x86_64", release_digest=digest("r2"),
        bootstrap_mode="OMEGA_KNOWLEDGE_ONLY", outcome="QUALIFIED_KNOWLEDGE_ONLY",
        test_results=[{"id":"offline_verify","outcome":"PASS","evidence_ref":None}],
    )
    assert r1["qualification_digest"] != r2["qualification_digest"]


def test_artifact_set_digest_ignores_mapping_insertion_order():
    assert artifact_set_digest({"b":"2","a":"1"}) == artifact_set_digest({"a":"1","b":"2"})
