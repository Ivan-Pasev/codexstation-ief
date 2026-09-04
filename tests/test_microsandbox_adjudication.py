import importlib.util
from pathlib import Path

P=Path(__file__).parents[1]/"providers"/"microsandbox"/"adjudicate.py"
s=importlib.util.spec_from_file_location("msb_adjudicate",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)

def base(status="PASS"):
    return {"host":{"system":"Linux","machine":"x86_64"},"microsandbox":{"binary":"/usr/bin/msb","version":{"stdout":"1.0"}},"gates":{f"G{i:02d}":{"status":status} for i in range(1,19)}}

def test_all_pass_still_does_not_invent_eac():
    r=m.adjudicate(base())
    assert r["qualification_complete"] is True
    assert r["assigned_eac"] is None
    assert r["execution_authorized"] is False

def test_unresolved_critical_gate_fails_closed():
    e=base(); e["gates"]["G05"]={"status":"UNRESOLVED"}
    r=m.adjudicate(e)
    assert "G05" in r["critical_nonpass_gates"]
    assert r["decision"]=="EAC_NULL"

def test_missing_identity_fails_closed():
    e=base(); e["microsandbox"]["binary"]=None
    r=m.adjudicate(e)
    assert r["identity_complete"] is False
    assert r["execution_authorized"] is False
