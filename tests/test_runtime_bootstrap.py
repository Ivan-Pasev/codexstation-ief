from reference.runtime_bootstrap import bootstrap, digest, discover, select_mode


def manifest():
    artifacts = [{"path":"00_CORE/core.txt","type":"core","digest":digest("core") }]
    core = {
        "schema_version":"CS-IEF-09","release_id":"omega-portable","release_version":"0.1.0",
        "spec_root":"CS-IEF-09","omega_version":"0.2.0","distribution_bundle_digest":digest("bundle"),
        "compiler":{"id":"reference","version":"0.1"},"artifacts":artifacts,
        "supported_platform_classes":["portable"],"source_graph_digest":digest("sources")
    }
    return {**core, "release_digest":digest(core)}


def test_knowledge_only_needs_no_provider():
    m = manifest()
    r = bootstrap(release_manifest=m, observed_artifact_digests={"00_CORE/core.txt":digest("core")},
                  installation_id="i1", platform_facts={}, configuration={}, provider_descriptors=[],
                  qualifications={}, requested_mode="OMEGA_KNOWLEDGE_ONLY")
    assert r["terminal_state"] == "READY"
    assert r["effective_mode"] == "OMEGA_KNOWLEDGE_ONLY"
    assert r["selected_provider"] is None


def test_tamper_fails_closed():
    m = manifest()
    r = bootstrap(release_manifest=m, observed_artifact_digests={"00_CORE/core.txt":digest("tampered")},
                  installation_id="i2", platform_facts={}, configuration={}, provider_descriptors=[],
                  qualifications={}, requested_mode="OMEGA_KNOWLEDGE_ONLY")
    assert r["terminal_state"] == "REJECTED"
    assert r["effective_mode"] == "NONE"


def test_discovery_does_not_assign_eac():
    p = discover([{"provider_id":"p","candidate_modes":["IEF_MICROVM"],"health":"READY","availability":"AVAILABLE"}])[0]
    assert "assigned_eac" not in p


def test_missing_qualification_blocks_execution():
    p = discover([{"provider_id":"p","candidate_modes":["IEF_MICROVM"],"health":"READY","availability":"AVAILABLE"}])
    mode, provider, _ = select_mode(requested_mode="IEF_MICROVM", discovered=p, qualifications={})
    assert mode == "NONE" and provider is None


def test_current_qualification_allows_bounded_mode():
    p = discover([{"provider_id":"p","candidate_modes":["IEF_CONTAINER"],"health":"READY","availability":"AVAILABLE"}])
    q = {"p":{"current":True,"assigned_eac":2,"qualification_digest":digest("q")}}
    mode, provider, _ = select_mode(requested_mode="IEF_CONTAINER", discovered=p, qualifications=q)
    assert mode == "IEF_CONTAINER" and provider == "p"


def test_permitted_fallback_is_visible():
    p = discover([])
    mode, provider, degradations = select_mode(requested_mode="IEF_MICROVM", discovered=p, qualifications={}, permitted_fallbacks=["OMEGA_KNOWLEDGE_ONLY"])
    assert mode == "OMEGA_KNOWLEDGE_ONLY" and provider is None
    assert degradations == ["fallback:IEF_MICROVM->OMEGA_KNOWLEDGE_ONLY"]
