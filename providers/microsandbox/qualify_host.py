#!/usr/bin/env python3
"""CS-IEF-16A fail-closed Microsandbox host qualification runner.

This runner captures host/runtime evidence and emits deterministic JSON + Markdown.
It never promotes EAC: unimplemented empirical gates remain BLOCKED/UNRESOLVED.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, shutil, subprocess
from pathlib import Path
from datetime import datetime, timezone

GATES = [f"G{i:02d}" for i in range(1, 19)]
CRITICAL = {"G02","G03","G04","G05","G06","G07","G08","G09","G10","G12","G13","G14","G16","G17","G18"}

def run(cmd):
    try:
        p=subprocess.run(cmd, text=True, capture_output=True, timeout=20)
        return {"cmd":cmd,"rc":p.returncode,"stdout":p.stdout.strip(),"stderr":p.stderr.strip()}
    except Exception as e:
        return {"cmd":cmd,"rc":None,"stdout":"","stderr":repr(e)}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out", default="qualification-evidence")
    ap.add_argument("--expected-source", default="5eca4de8bf233e57f114140f8c076ea8c96f21ab")
    a=ap.parse_args(); out=Path(a.out); out.mkdir(parents=True, exist_ok=True)
    ms=shutil.which("microsandbox") or shutil.which("msb")
    evidence={
      "schema":"CS-IEF-16A/host-qualification-evidence-v1",
      "captured_at":datetime.now(timezone.utc).isoformat(),
      "host":{"system":platform.system(),"release":platform.release(),"machine":platform.machine(),"python":platform.python_version()},
      "virtualization":{}, "microsandbox":{}, "expected_source_snapshot":a.expected_source,
      "gates":{}, "assigned_eac":None, "execution_authorized":False
    }
    if platform.system()=="Linux":
        evidence["virtualization"]["cpu_flags"] = run(["sh","-lc","grep -m1 -E 'flags|Features' /proc/cpuinfo || true"])
        evidence["virtualization"]["kvm_device"] = {"exists":Path('/dev/kvm').exists(),"readable":os.access('/dev/kvm',os.R_OK),"writable":os.access('/dev/kvm',os.W_OK)}
        evidence["virtualization"]["systemd_detect_virt"] = run(["sh","-lc","command -v systemd-detect-virt >/dev/null && systemd-detect-virt || true"])
    elif platform.system()=="Windows":
        evidence["virtualization"]["systeminfo"] = run(["cmd","/c","systeminfo"])
    evidence["microsandbox"]["binary"] = ms
    if ms:
        evidence["microsandbox"]["version"] = run([ms,"--version"])
        evidence["gates"]["G01"]={"status":"OBSERVED","reason":"Microsandbox CLI discovered; runtime health still requires provider probe."}
    else:
        evidence["gates"]["G01"]={"status":"BLOCKED","reason":"Microsandbox CLI not found on PATH."}
    for g in GATES:
        evidence["gates"].setdefault(g,{"status":"BLOCKED","reason":"Empirical gate not yet implemented/executed by this bootstrap runner."})
    # G02 can only become OBSERVED, never PASS, from host capability discovery alone.
    if platform.system()=="Linux" and Path('/dev/kvm').exists():
        evidence["gates"]["G02"]={"status":"OBSERVED","reason":"/dev/kvm exists; active Microsandbox backend identity still must be proven."}
    evidence["adjudication"]={
      "critical_gate_fail_closed":True,
      "critical_gates":sorted(CRITICAL),
      "result":"QUALIFICATION_INCOMPLETE",
      "rule":"No EAC assignment or execution authorization until all required empirical gates PASS with bound evidence."
    }
    digest=hashlib.sha256(canonical(evidence)).hexdigest(); evidence["evidence_digest"]="sha256:"+digest
    (out/"qualification.json").write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    lines=["# CS-IEF-16A Host Qualification Report","",f"Evidence digest: `sha256:{digest}`","",f"Host: `{evidence['host']['system']} {evidence['host']['release']} {evidence['host']['machine']}`",f"Microsandbox binary: `{ms}`","","## Adjudication","","- result: `QUALIFICATION_INCOMPLETE`","- assigned EAC: `null`","- execution authorized: `false`","","## Gates",""]
    lines += [f"- {g}: **{evidence['gates'][g]['status']}** — {evidence['gates'][g]['reason']}" for g in GATES]
    (out/"REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"evidence":str(out/'qualification.json'),"digest":"sha256:"+digest,"assigned_eac":None,"execution_authorized":False}))

if __name__=="__main__": main()
