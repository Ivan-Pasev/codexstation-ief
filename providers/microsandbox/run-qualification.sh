#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUT="$ROOT/qualification-evidence"
python3 "$ROOT/qualify_host.py" --out "$OUT"
printf 'CS-IEF-16A evidence emitted to %s\n' "$OUT"
printf '%s\n' 'Do not infer EAC or execution authorization unless qualification.json explicitly records them.'
