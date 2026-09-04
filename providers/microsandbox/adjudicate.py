#!/usr/bin/env python3
"""Independent CS-IEF-16C evidence-to-EAC adjudicator.

EAC assignment is evidence-derived. It never authorizes execution.
"""
import argparse, hashlib, json
from pathlib import Path

ALL={f"G{i:02d}" for i in range(1,19)}
CRITICAL={"G02","G03","G04","G05","G06","G07","G08","G09","G10","G12","G13","G14","G16","G17","G18"}
EAC1={"G01","G04","G11","G12","G14","G15","G16","G17","G18"}
EAC2=EAC1|{"G05","G06","G07","G08","G09","G10"}
EAC3=ALL

def passed(gates, required):
    return all(gates.get(g,{}).get("status")=="PASS" for g in required)

def adjudicate(e):
    gates=e.get("gates",{})
    missing=sorted(ALL-set(gates))
    nonpass=sorted(g for g in ALL if gates.get(g,{}).get("status") not in {"PASS","NOT_APPLICABLE"})
    critical_nonpass=sorted(CRITICAL & set(nonpass))
    host=e.get("host",{}); runtime=e.get("microsandbox",{}); virt=e.get("virtualization",{})
    identity_complete=bool(host.get("system") and host.get("machine") and runtime.get("binary") and runtime.get("version"))
    backend_bound=bool(runtime.get("active_backend_identity") or virt.get("active_backend_identity"))
    raw_bound=bool(e.get("raw_evidence_manifest_digest"))
    risk=e.get("risk_ledger",{})
    risks_clear=(risk.get("unresolved_critical",1)==0)
    evidence_quality=3 if raw_bound and identity_complete else 0
    architecture_ceiling=3 if backend_bound else (2 if runtime.get("host_kernel_shared") is True else 1)
    empirical=0
    if identity_complete and passed(gates,EAC1): empirical=1
    if identity_complete and passed(gates,EAC2): empirical=2
    if identity_complete and backend_bound and raw_bound and risks_clear and passed(gates,EAC3): empirical=3
    assigned=min(architecture_ceiling,empirical,evidence_quality) if evidence_quality else 0
    decision=f"EAC_{assigned}" if assigned else "EAC_NULL"
    return {
      "constitution":"CS-IEF-16C",
      "qualification_complete": not missing and not nonpass and identity_complete,
      "identity_complete":identity_complete,"backend_bound":backend_bound,"raw_evidence_bound":raw_bound,"critical_risks_clear":risks_clear,
      "missing_gates":missing,"nonpass_gates":nonpass,"critical_nonpass_gates":critical_nonpass,
      "architecture_ceiling":architecture_ceiling,"empirical_control_floor":empirical,"evidence_quality_ceiling":evidence_quality,
      "assigned_eac":assigned if assigned>0 else None,"execution_authorized":False,"decision":decision,
      "reason":"EAC is bounded by architecture, empirical controls, and evidence quality. Execution authorization requires a separate policy/capability decision."
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("evidence"); ap.add_argument("--out",default=None); a=ap.parse_args()
    e=json.loads(Path(a.evidence).read_text(encoding="utf-8")); result=adjudicate(e)
    raw=json.dumps(result,sort_keys=True,separators=(",",":")).encode(); result["adjudication_digest"]="sha256:"+hashlib.sha256(raw).hexdigest()
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.out: Path(a.out).write_text(text,encoding="utf-8")
    print(text,end="")
if __name__=="__main__": main()
