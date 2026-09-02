from reference.witness_graph import WitnessRecord, seal, validate_graph, validate_primary_execution_chain, witnessed_implies_truth


def rec(record_id, record_type, sequence, parents=()):
    return seal(WitnessRecord(
        schema_version="CS-IEF-07",
        record_id=record_id,
        record_type=record_type,
        trace_id="t1",
        parent_record_ids=tuple(parents),
        subject_digests=(f"sha256:{record_id}",),
        actor_or_authority_ref="test",
        sequence=sequence,
    ))


def test_primary_execution_chain_valid():
    records = [
        rec("w0", "OBSERVATION", 0),
        rec("w1", "INTENT", 1, ("w0",)),
        rec("w2", "AUTHORIZATION", 2, ("w1",)),
        rec("p", "PROVIDER_PLAN", 3, ("w2",)),
        rec("w3", "EXECUTION_OUTCOME", 4, ("p",)),
        rec("e", "EVIDENCE_BUNDLE", 5, ("w3",)),
    ]
    assert validate_graph(records) == []
    assert validate_primary_execution_chain(records) == []


def test_missing_parent_detected():
    r = rec("x", "INTENT", 1, ("missing",))
    assert any(x.startswith("MISSING_PARENT") for x in validate_graph([r]))


def test_tamper_detected():
    r = rec("x", "OBSERVATION", 0)
    tampered = WitnessRecord(**{**r.__dict__, "actor_or_authority_ref": "other"})
    assert any(x.startswith("DIGEST_MISMATCH") for x in validate_graph([tampered]))


def test_witness_does_not_imply_truth():
    assert witnessed_implies_truth() is False
