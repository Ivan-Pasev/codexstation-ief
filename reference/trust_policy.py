"""CS-IEF-14A public trust-policy reference evaluator.

This module evaluates public policy state only. It does not generate keys,
handle private key material, or perform detached signature verification.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class TrustDecision:
    trusted: bool
    reasons: tuple[str, ...]


def signer_eligible(signer: Mapping[str, object], *, scope: str) -> bool:
    return (
        signer.get("status") == "ACTIVE"
        and scope in set(signer.get("artifact_scopes", []))
        and signer.get("algorithm") == "ed25519"
        and isinstance(signer.get("key_id"), str)
        and str(signer.get("key_id")).startswith("sha256:")
    )


def policy_activation_ready(policy: Mapping[str, object]) -> TrustDecision:
    reasons: list[str] = []
    signers = list(policy.get("accepted_signers", []))
    threshold = int(policy.get("threshold", 1))
    scope = str(next(iter(policy.get("artifact_scopes", [])), ""))
    eligible = [s for s in signers if signer_eligible(s, scope=scope)]
    if len(eligible) < threshold:
        reasons.append("THRESHOLD_NOT_SATISFIABLE")
    if not str(policy.get("policy_digest", "")).startswith("sha256:"):
        reasons.append("POLICY_DIGEST_MISSING")
    if not scope:
        reasons.append("ARTIFACT_SCOPE_MISSING")
    if policy.get("status") == "REVOKED":
        reasons.append("POLICY_REVOKED")
    return TrustDecision(not reasons, tuple(reasons))


def evaluate_trust(*, policy: Mapping[str, object], scope: str,
                   cryptographically_valid_key_ids: Iterable[str]) -> TrustDecision:
    reasons: list[str] = []
    if policy.get("status") != "ACTIVE":
        reasons.append("POLICY_NOT_ACTIVE")
    if scope not in set(policy.get("artifact_scopes", [])):
        reasons.append("SCOPE_NOT_ACCEPTED")
    threshold = int(policy.get("threshold", 1))
    valid_ids = set(cryptographically_valid_key_ids)
    eligible_ids = {
        str(s.get("key_id"))
        for s in policy.get("accepted_signers", [])
        if signer_eligible(s, scope=scope)
    }
    if len(valid_ids & eligible_ids) < threshold:
        reasons.append("TRUST_THRESHOLD_NOT_MET")
    return TrustDecision(not reasons, tuple(reasons))
