from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import shutil
import tempfile
import zipfile


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_module(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("packaged_portable_runtime", path)
    if spec is None or spec.loader is None:
        raise SystemExit("PACKAGED_RUNTIME_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def qualify(archive: pathlib.Path, platform_class: str, out: pathlib.Path) -> dict:
    name = archive.stem
    if name.endswith(".tar"):
        raise SystemExit("ZIP_REQUIRED")
    with tempfile.TemporaryDirectory(prefix="cs-ief-rc2-") as td:
        root = pathlib.Path(td)
        with zipfile.ZipFile(archive, "r") as zf:
            names = zf.namelist()
            if not names or not all(n.startswith(name + "/") for n in names):
                raise SystemExit("ARCHIVE_PREFIX_INVALID")
            zf.extractall(root)
        tree = root / name
        manifest = json.loads((tree / "MANIFEST.json").read_text(encoding="utf-8"))

        integrity_failures: list[str] = []
        for line in (tree / "INTEGRITY.sha256").read_text(encoding="utf-8").splitlines():
            expected, rel = line.split("  ", 1)
            actual = hashlib.sha256((tree / pathlib.PurePosixPath(rel)).read_bytes()).hexdigest()
            if actual != expected:
                integrity_failures.append(rel)
        if integrity_failures:
            raise SystemExit("INTEGRITY_FAILURE:" + ",".join(integrity_failures))

        runtime = load_module(tree / "reference" / "portable_runtime.py")
        artifacts = {
            row["path"]: (tree / pathlib.PurePosixPath(row["path"])).read_bytes()
            for row in manifest["artifacts"]
        }
        receipt = runtime.install_knowledge_only(
            release_manifest=manifest,
            artifacts=artifacts,
            installation_id=f"rc2-{platform_class}",
            platform_facts={"platform_class": platform_class, "qualification_scope": "OMEGA_KNOWLEDGE_ONLY"},
            configuration={"provider": "NONE"},
        )
        if receipt.get("terminal_state") != "READY":
            raise SystemExit("KNOWLEDGE_ONLY_NOT_READY")
        if receipt.get("effective_mode") != "OMEGA_KNOWLEDGE_ONLY":
            raise SystemExit("EFFECTIVE_MODE_INVALID")
        if receipt.get("selected_provider") is not None:
            raise SystemExit("PROVIDER_SHOULD_BE_NONE")

        result = {
            "schema_version": "CS-IEF-13-RC2-QUALIFICATION",
            "platform_class": platform_class,
            "archive_sha256": sha256_bytes(archive.read_bytes()),
            "release_digest": manifest["release_digest"],
            "distribution_bundle_digest": manifest["distribution_bundle_digest"],
            "integrity": "PASS",
            "packaged_runtime_import": "PASS",
            "knowledge_only_install": "PASS",
            "qualification": "QUALIFIED_KNOWLEDGE_ONLY",
            "provider": "NONE",
            "eac_claim": None,
            "installation_receipt": receipt,
        }
        out.mkdir(parents=True, exist_ok=True)
        (out / "QUALIFICATION_RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        (out / "INSTALLATION_RECEIPT.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("--platform-class", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = qualify(pathlib.Path(args.archive).resolve(), args.platform_class, pathlib.Path(args.output).resolve())
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
