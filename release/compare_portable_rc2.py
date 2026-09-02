from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import zipfile


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def archive_facts(path: pathlib.Path) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        names = sorted(zf.namelist(), key=lambda x: x.encode("utf-8"))
        prefix = names[0].split("/", 1)[0] + "/"
        manifest = json.loads(zf.read(prefix + "MANIFEST.json"))
        tree = {
            name[len(prefix):]: sha256_bytes(zf.read(name))
            for name in names
            if name.startswith(prefix) and not name.endswith("/")
        }
    return {
        "archive_sha256": sha256_bytes(path.read_bytes()),
        "release_digest": manifest["release_digest"],
        "distribution_bundle_digest": manifest["distribution_bundle_digest"],
        "source_graph_digest": manifest["source_graph_digest"],
        "tree": tree,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("linux_archive")
    parser.add_argument("windows_archive")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    linux = archive_facts(pathlib.Path(args.linux_archive))
    windows = archive_facts(pathlib.Path(args.windows_archive))
    result = {
        "schema_version": "CS-IEF-13-RC2-CROSS-PLATFORM",
        "linux_archive_sha256": linux["archive_sha256"],
        "windows_archive_sha256": windows["archive_sha256"],
        "archive_byte_identical": linux["archive_sha256"] == windows["archive_sha256"],
        "release_digest_identical": linux["release_digest"] == windows["release_digest"],
        "distribution_bundle_digest_identical": linux["distribution_bundle_digest"] == windows["distribution_bundle_digest"],
        "source_graph_digest_identical": linux["source_graph_digest"] == windows["source_graph_digest"],
        "extracted_tree_identical": linux["tree"] == windows["tree"],
        "release_digest": linux["release_digest"] if linux["release_digest"] == windows["release_digest"] else None,
    }
    if not all((result["release_digest_identical"], result["distribution_bundle_digest_identical"], result["source_graph_digest_identical"], result["extracted_tree_identical"])):
        raise SystemExit("RC2_CROSS_PLATFORM_SEMANTIC_REPRODUCTION_FAIL:" + json.dumps(result, sort_keys=True))
    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
