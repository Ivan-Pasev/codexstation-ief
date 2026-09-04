# CS-IEF-16A — Microsandbox Host Qualification Runner

Status: RUNNER_BOOTSTRAPPED / REAL_HOST_EXECUTION_REQUIRED

## Objective

Turn CS-IEF-16's G01–G18 qualification lattice into a portable evidence-producing host runner for Windows and Linux/WSL2 without granting assurance from feature discovery alone.

## Current implementation

`providers/microsandbox/qualify_host.py` captures host, virtualization and Microsandbox CLI identity and emits canonical JSON plus a human-readable report. Platform launchers are provided for PowerShell and POSIX shells.

The bootstrap runner intentionally leaves empirical isolation/enforcement gates BLOCKED until dedicated probes are implemented and executed against a real Microsandbox runtime.

## Fail-closed invariant

`assigned_eac = null` and `execution_authorized = false` unless the complete required empirical qualification set is bound to evidence and passes the governing adjudicator.

OBSERVED is not PASS. Feature discovery is not enforcement evidence. `/dev/kvm` presence is not proof that Microsandbox actually used KVM for the tested cell.

## Evidence outputs

- `qualification-evidence/qualification.json`
- `qualification-evidence/REPORT.md`
- canonical SHA-256 over the pre-digest evidence object

## Host invocation

Windows PowerShell:

```powershell
.\providers\microsandbox\run-qualification.ps1
```

Linux/WSL2:

```sh
sh providers/microsandbox/run-qualification.sh
```

## Next implementation increment

Replace bootstrap BLOCKED states with provider-bound probes for G01–G18. Each probe must bind runtime version, backend identity, cell identity, timestamps, requested control, observed result, raw evidence references and cleanup result. Isolation-critical failures remain non-overridable.

The first authorized ResearchCell may only be attempted after the adjudicator records a non-null EAC sufficient for the requested ExecutionContract and `execution_authorized=true`.
