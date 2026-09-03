from reference.trust_policy import evaluate_trust, policy_activation_ready


def base_policy(**overrides):
    p = {
        "status":"CONSTITUTION_READY_AWAITING_SIGNER",
        "artifact_scopes":["codexstation-omega-portable"],
        "threshold":1,
        "accepted_signers":[],
        "policy_digest":"sha256:" + "0"*64,
    }
    p.update(overrides)
    return p


def signer(key_id="sha256:" + "1"*64, status="ACTIVE"):
    return {
        "signer_id":"operator-1",
        "key_id":key_id,
        "algorithm":"ed25519",
        "status":status,
        "artifact_scopes":["codexstation-omega-portable"],
    }


def test_empty_bootstrap_policy_cannot_activate():
    d = policy_activation_ready(base_policy())
    assert not d.trusted
    assert "THRESHOLD_NOT_SATISFIABLE" in d.reasons


def test_active_signer_can_satisfy_activation_threshold():
    d = policy_activation_ready(base_policy(accepted_signers=[signer()]))
    assert d.trusted


def test_valid_signature_under_inactive_policy_is_not_trusted():
    p = base_policy(accepted_signers=[signer()])
    d = evaluate_trust(policy=p, scope="codexstation-omega-portable", cryptographically_valid_key_ids=[signer()["key_id"]])
    assert not d.trusted
    assert "POLICY_NOT_ACTIVE" in d.reasons


def test_active_policy_requires_threshold_satisfying_accepted_signer():
    p = base_policy(status="ACTIVE", accepted_signers=[signer()])
    d = evaluate_trust(policy=p, scope="codexstation-omega-portable", cryptographically_valid_key_ids=[signer()["key_id"]])
    assert d.trusted


def test_revoked_signer_does_not_count():
    s = signer(status="REVOKED")
    p = base_policy(status="ACTIVE", accepted_signers=[s])
    d = evaluate_trust(policy=p, scope="codexstation-omega-portable", cryptographically_valid_key_ids=[s["key_id"]])
    assert not d.trusted
    assert "TRUST_THRESHOLD_NOT_MET" in d.reasons


def test_scope_mismatch_rejected():
    p = base_policy(status="ACTIVE", accepted_signers=[signer()])
    d = evaluate_trust(policy=p, scope="another-artifact", cryptographically_valid_key_ids=[signer()["key_id"]])
    assert not d.trusted
    assert "SCOPE_NOT_ACCEPTED" in d.reasons
