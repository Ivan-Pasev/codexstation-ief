"""CS-IEF-07 deterministic witness graph reference helpers.

This module demonstrates append-only digest chaining and graph validation. It does
not sign, anchor externally, or claim semantic truth.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Iterable


@dataclass(frozen=True)
class WitnessRecord:
    schema_version: str
    record_id: str
    record_type: str
    trace_id: str
    parent_record_ids: tuple[str, ...]
    subject_digests: tuple[str, ...]
    actor_or_authority_ref: str
    sequence: int
    previous_chain_digest: str | None = None
    timestamp: str | None = None
    metadata: dict | None = None
    record_digest: str = ""


def canonical_bytes(record: WitnessRecord) -> bytes:
    payload = asdict(record)
    payload.pop("record_digest", None)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_record(record: WitnessRecord) -> str:
    return "sha256:" + sha256(canonical_bytes(record)).hexdigest()


def seal(record: WitnessRecord) -> WitnessRecord:
    return WitnessRecord(**{**asdict(record), "record_digest": digest_record(record)})


def validate_graph(records: Iterable[WitnessRecord]) -> list[str]:
    records = list(records)
    by_id = {r.record_id: r for r in records}
    errors: list[str] = []

    if len(by_id) != len(records):
        errors.append("DUPLICATE_RECORD_ID")

    for r in records:
        if r.record_digest != digest_record(r):
            errors.append(f"DIGEST_MISMATCH:{r.record_id}")
        for p in r.parent_record_ids:
            if p not in by_id:
                errors.append(f"MISSING_PARENT:{r.record_id}:{p}")
            elif by_id[p].trace_id != r.trace_id:
                errors.append(f"CROSS_TRACE_PARENT:{r.record_id}:{p}")
            elif by_id[p].sequence >= r.sequence:
                errors.append(f"NON_FORWARD_PARENT:{r.record_id}:{p}")
    return errors


def validate_primary_execution_chain(records: Iterable[WitnessRecord]) -> list[str]:
    records = list(records)
    kinds = {r.record_type for r in records}
    required = {"OBSERVATION", "INTENT", "AUTHORIZATION", "PROVIDER_PLAN", "EXECUTION_OUTCOME", "EVIDENCE_BUNDLE"}
    missing = sorted(required - kinds)
    return [f"MISSING_PRIMARY_STAGE:{x}" for x in missing]


def witnessed_implies_truth() -> bool:
    """The witness layer never asserts semantic truth from witness presence."""
    return False
