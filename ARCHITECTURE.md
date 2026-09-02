# Architecture

CodexStation IEF separates cognition from effects through a policy-mediated execution boundary.

## Fabric equation

`CodexStation = Cognition Fabric + Knowledge Fabric + Policy Fabric + Isolated Execution Fabric + Evidence Fabric`

## Execution path

`Intent -> Policy -> Capability Negotiation -> ProviderPlan -> Authorization -> ExecutionCell -> ExecutionReceipt -> Evidence/Witness`

## Provider doctrine

The IEF kernel is provider-neutral. A provider may implement host-process, container, microVM, remote sovereign, or attested/confidential execution, but provider-specific types must remain behind the stable ABI.

## Assurance classes

- EAC-0 NONE
- EAC-1 HOST_PROCESS
- EAC-2 CONTAINER
- EAC-3 MICROVM
- EAC-4 REMOTE_ATTESTED_VM
- EAC-5 CONFIDENTIAL_ATTESTED_EXECUTION

Reported assurance may never exceed measured qualified assurance.
