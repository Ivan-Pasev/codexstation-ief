from reference.portable_runtime import (
    BootstrapRejected, build_release_manifest, install_knowledge_only,
    select_mode, verify_release,
)


def fixture():
    artifacts = {"00_CORE/CORE.md": b"constitutional core", "MANIFEST.semantic.json": b"{}"}
    manifest = build_release_manifest(
        release_id="codexstation-omega-portable",
        release_version="0.1.0",
        spec_root="CS-IEF-09",
        omega_version="0.2.0",
        distribution_bundle_digest="sha256:" + "1" * 64,
        compiler_id="reference",
        compiler_version="0.1.0",
        artifacts=artifacts,
        source_graph_digest="sha256:" + "2" * 64,
    )
    return artifacts, manifest


def test_same_release_inputs_same_digest():
    a, m1 = fixture()
    _, m2 = fixture()
    assert m1["release_digest"] == m2["release_digest"]


def test_tamper_rejected():
    artifacts, manifest = fixture()
    bad = dict(artifacts)
    bad["00_CORE/CORE.md"] = b"tampered"
    try:
        verify_release(manifest, bad)
        assert False
    except BootstrapRejected as e:
        assert "INTEGRITY_MISMATCH" in str(e)


def test_missing_artifact_rejected():
    artifacts, manifest = fixture()
    del artifacts["00_CORE/CORE.md"]
    try:
        verify_release(manifest, artifacts)
        assert False
    except BootstrapRejected as e:
        assert "MISSING_ARTIFACT" in str(e)


def test_knowledge_only_requires_no_provider():
    artifacts, manifest = fixture()
    receipt = install_knowledge_only(
        release_manifest=manifest,
        artifacts=artifacts,
        installation_id="local-test",
        platform_facts={"os":"test"},
        configuration={},
    )
    assert receipt["terminal_state"] == "READY"
    assert receipt["effective_mode"] == "OMEGA_KNOWLEDGE_ONLY"
    assert receipt["selected_provider"] is None


def test_discovered_but_unqualified_provider_cannot_activate_microvm():
    providers = [{"provider_id":"candidate","qualified_modes":[],"qualification_current":False}]
    try:
        select_mode(requested_mode="IEF_MICROVM", providers=providers)
        assert False
    except BootstrapRejected as e:
        assert str(e) == "NO_QUALIFIED_PROVIDER_FOR_REQUESTED_MODE"


def test_explicit_fallback_only_narrows_to_knowledge_only():
    mode, provider, degradations = select_mode(
        requested_mode="IEF_MICROVM", providers=[], allow_fallback=True
    )
    assert mode == "OMEGA_KNOWLEDGE_ONLY"
    assert provider is None
    assert degradations == ["mode:IEF_MICROVM->OMEGA_KNOWLEDGE_ONLY"]


def test_current_qualification_can_select_exact_requested_mode():
    providers = [{"provider_id":"p1","qualified_modes":["IEF_CONTAINER"],"qualification_current":True}]
    mode, provider, degradations = select_mode(requested_mode="IEF_CONTAINER", providers=providers)
    assert mode == "IEF_CONTAINER"
    assert provider == "p1"
    assert degradations == []
