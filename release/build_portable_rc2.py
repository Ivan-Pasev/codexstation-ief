from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERSION = "0.1.0-rc2"
NAME = f"codexstation-omega-portable-{VERSION}"
COMPILER_ID = "codexstation-ief.release.build_portable_rc2"
COMPILER_VERSION = "1.0.0"

INCLUDE_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "SECURITY.md",
    "GOVERNANCE.md",
    "llms.txt",
    "surfaces/portable.yaml",
    "distributions/OMEGA_MANIFEST.yaml",
    "reference/portable_runtime.py",
    "release/RC2_DECLARATION.json",
]
INCLUDE_DIRS = ["specs", "schemas"]


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def normalized_bytes(path: pathlib.Path) -> bytes:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        return text.encode("utf-8")
    except UnicodeDecodeError:
        return data


def source_paths() -> list[str]:
    rows: list[str] = []
    for rel in INCLUDE_FILES:
        p = ROOT / rel
        if not p.is_file():
            raise SystemExit(f"MISSING_REQUIRED:{rel}")
        rows.append(rel)
    for directory in INCLUDE_DIRS:
        for p in (ROOT / directory).rglob("*"):
            if p.is_file():
                rows.append(p.relative_to(ROOT).as_posix())
    return sorted(set(rows), key=lambda x: x.encode("utf-8"))


def load_portable_runtime():
    path = ROOT / "reference" / "portable_runtime.py"
    spec = importlib.util.spec_from_file_location("cs_ief_portable_runtime", path)
    if spec is None or spec.loader is None:
        raise SystemExit("PORTABLE_RUNTIME_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_manifest_shape(manifest: dict) -> None:
    schema = json.loads((ROOT / "schemas" / "release-manifest.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    missing = sorted(required - set(manifest))
    if missing:
        raise SystemExit("MANIFEST_REQUIRED_MISSING:" + ",".join(missing))
    allowed = set(schema["properties"])
    extra = sorted(set(manifest) - allowed)
    if extra:
        raise SystemExit("MANIFEST_ADDITIONAL_PROPERTY:" + ",".join(extra))
    if manifest["schema_version"] != "CS-IEF-09":
        raise SystemExit("MANIFEST_SCHEMA_VERSION")
    for row in manifest["artifacts"]:
        if set(row) != {"path", "type", "digest"}:
            raise SystemExit("MANIFEST_ARTIFACT_SHAPE")
        if not str(row["digest"]).startswith("sha256:") or len(str(row["digest"])) != 71:
            raise SystemExit("MANIFEST_ARTIFACT_DIGEST")
    for key in ("distribution_bundle_digest", "source_graph_digest", "release_digest"):
        value = str(manifest[key])
        if not value.startswith("sha256:") or len(value) != 71:
            raise SystemExit(f"MANIFEST_DIGEST:{key}")


def build(source_revision: str, outroot: pathlib.Path) -> dict:
    runtime = load_portable_runtime()
    if outroot.exists():
        shutil.rmtree(outroot)
    tree = outroot / NAME
    tree.mkdir(parents=True)

    artifacts: dict[str, bytes] = {}
    for rel in source_paths():
        data = normalized_bytes(ROOT / rel)
        artifacts[rel] = data
        dst = tree / pathlib.PurePosixPath(rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)

    version_bytes = (VERSION + "\n").encode("utf-8")
    artifacts["VERSION"] = version_bytes
    (tree / "VERSION").write_bytes(version_bytes)

    source_rows = [
        {"path": path, "digest": sha256_bytes(artifacts[path])}
        for path in sorted(artifacts, key=lambda x: x.encode("utf-8"))
    ]
    source_graph_digest = sha256_bytes(canonical_json(source_rows))

    distribution_binding = {
        "schema_version": "CS-IEF-13-DISTRIBUTION-BINDING",
        "target_surface": "portable",
        "omega_manifest_digest": sha256_bytes(artifacts["distributions/OMEGA_MANIFEST.yaml"]),
        "surface_profile_digest": sha256_bytes(artifacts["surfaces/portable.yaml"]),
        "source_graph_digest": source_graph_digest,
        "compiler": {"id": COMPILER_ID, "version": COMPILER_VERSION},
    }
    distribution_binding_bytes = json.dumps(distribution_binding, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    distribution_bundle_digest = sha256_bytes(canonical_json(distribution_binding))
    artifacts["DISTRIBUTION_BINDING.json"] = distribution_binding_bytes
    (tree / "DISTRIBUTION_BINDING.json").write_bytes(distribution_binding_bytes)

    manifest = runtime.build_release_manifest(
        release_id="codexstation-omega-portable",
        release_version=VERSION,
        spec_root="CS-IEF-13",
        omega_version="0.2.0",
        distribution_bundle_digest=distribution_bundle_digest,
        compiler_id=COMPILER_ID,
        compiler_version=COMPILER_VERSION,
        artifacts=artifacts,
        source_graph_digest=source_graph_digest,
        supported_platform_classes=("linux-x86_64", "windows-x86_64", "portable"),
    )
    validate_manifest_shape(manifest)
    manifest_bytes = json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    (tree / "MANIFEST.json").write_bytes(manifest_bytes)

    integrity_rows = [
        f"{sha256_bytes(artifacts[path]).split(':', 1)[1]}  {path}"
        for path in sorted(artifacts, key=lambda x: x.encode("utf-8"))
    ]
    integrity_rows.append(f"{hashlib.sha256(manifest_bytes).hexdigest()}  MANIFEST.json")
    integrity_bytes = ("\n".join(integrity_rows) + "\n").encode("utf-8")
    (tree / "INTEGRITY.sha256").write_bytes(integrity_bytes)

    archive = outroot / f"{NAME}.zip"
    files = [p for p in tree.rglob("*") if p.is_file()]
    files.sort(key=lambda p: p.relative_to(tree).as_posix().encode("utf-8"))
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in files:
            rel = f"{NAME}/{p.relative_to(tree).as_posix()}"
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            zf.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    result = {
        "schema_version": "CS-IEF-13-RC2-BUILD",
        "source_revision": source_revision,
        "archive": archive.name,
        "archive_sha256": sha256_bytes(archive.read_bytes()),
        "release_digest": manifest["release_digest"],
        "distribution_bundle_digest": distribution_bundle_digest,
        "source_graph_digest": source_graph_digest,
        "manifest_shape_validation": "PASS",
        "provider": "NONE",
        "baseline_mode": "OMEGA_KNOWLEDGE_ONLY",
        "eac_claim": None,
    }
    (outroot / "BUILD_RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output", default="rc2-out")
    args = parser.parse_args()
    result = build(args.source_revision, pathlib.Path(args.output).resolve())
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
