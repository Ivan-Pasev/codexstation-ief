# Security Policy

CodexStation IEF treats isolation and authorization as separate properties.

## Security invariants

- No execution provider may bypass the policy membrane.
- Network authority is deny-by-default.
- Persistence is opt-in.
- Raw secrets do not belong in stable execution specifications.
- Shared mutable storage is explicit coupling.
- Unsupported controls fail closed or require explicit authorized degradation.
- Provider assurance must be measured in the current environment.

## Reporting

Until a dedicated security contact is published, use GitHub private vulnerability reporting if enabled for this repository. Do not publish active exploit details in a public issue.
