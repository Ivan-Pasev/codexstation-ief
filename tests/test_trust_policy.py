import unittest

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


class TrustPolicyTests(unittest.TestCase):
    def test_empty_bootstrap_policy_cannot_activate(self):
        d = policy_activation_ready(base_policy())
        self.assertFalse(d.trusted)
        self.assertIn("THRESHOLD_NOT_SATISFIABLE", d.reasons)

    def test_active_signer_can_satisfy_activation_threshold(self):
        d = policy_activation_ready(base_policy(accepted_signers=[signer()]))
        self.assertTrue(d.trusted)

    def test_valid_signature_under_inactive_policy_is_not_trusted(self):
        p = base_policy(accepted_signers=[signer()])
        d = evaluate_trust(policy=p, scope="codexstation-omega-portable", cryptographically_valid_key_ids=[signer()["key_id"]])
        self.assertFalse(d.trusted)
        self.assertIn("POLICY_NOT_ACTIVE", d.reasons)

    def test_active_policy_requires_threshold_satisfying_accepted_signer(self):
        p = base_policy(status="ACTIVE", accepted_signers=[signer()])
        d = evaluate_trust(policy=p, scope="codexstation-omega-portable", cryptographically_valid_key_ids=[signer()["key_id"]])
        self.assertTrue(d.trusted)

    def test_revoked_signer_does_not_count(self):
        s = signer(status="REVOKED")
        p = base_policy(status="ACTIVE", accepted_signers=[s])
        d = evaluate_trust(policy=p, scope="codexstation-omega-portable", cryptographically_valid_key_ids=[s["key_id"]])
        self.assertFalse(d.trusted)
        self.assertIn("TRUST_THRESHOLD_NOT_MET", d.reasons)

    def test_scope_mismatch_rejected(self):
        p = base_policy(status="ACTIVE", accepted_signers=[signer()])
        d = evaluate_trust(policy=p, scope="another-artifact", cryptographically_valid_key_ids=[signer()["key_id"]])
        self.assertFalse(d.trusted)
        self.assertIn("SCOPE_NOT_ACCEPTED", d.reasons)


if __name__ == "__main__":
    unittest.main()
