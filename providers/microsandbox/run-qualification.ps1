$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Out = Join-Path $Root 'qualification-evidence'
python (Join-Path $Root 'qualify_host.py') --out $Out
Write-Host "CS-IEF-16A evidence emitted to $Out"
Write-Host "Do not infer EAC or execution authorization unless qualification.json explicitly records them."
