#!/usr/bin/env python3
"""Independent CS-IEF-16B qualification adjudicator."""
import argparse, hashlib, json
from pathlib import Path

CRITICAL={"G02","G03","G04","G05","G06","G07","G08","G09","G10","G12","G13","G14","G16","G17","G18"}
ALL={f"G{i:02d}" for i in range(1,19)}

def adjudicate(e):
    gates=e.get("gates",{})
    missing=sorted(ALL-set(gates))
    nonpass=sorted(g for g in ALL if gates.get(g,{}).get("status")!="PASS")
    critical_nonpass=sorted(CRITICAL & set(nonpass))
    env=e.get("host",{})
    runtime=e.get("microsandbox",{})
    identity_complete=bool(env.get("system") and env.get("machine") and runtime.get("binary") and runtime.get("version"))
    # EAC mapping is deliberately not enabled until CS-IEF defines empirical threshold vectors.
    return {
      "qualification_complete": not missing and not nonpass and identity_complete,
      "identity_complete":identity_complete,
      "missing_gates":missing,"nonpass_gates":nonpass,"critical_nonpass_gates":critical_nonpass,
      "assigned_eac":None,"execution_authorized":False,
      "decision":"EAC_NULL",
      "reason":"Empirical EAC threshold mapping is not activated; qualification evidence cannot authorize execution yet."
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("evidence"); ap.add_argument("--out",default=None); a=ap.parse_args()
    e=json.loads(Path(a.evidence).read_text(encoding="utf-8")); result=adjudicate(e)
    raw=json.dumps(result,sort_keys=True,separators=(",",":")).encode(); result["adjudication_digest"]="sha256:"+hashlib.sha256(raw).hexdigest()
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.out: Path(a.out).write_text(text,encoding="utf-8")
    print(text,end="")
if __name__=="__main__": main()
