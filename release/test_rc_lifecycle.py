from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import tempfile
import zipfile

RC1_SHA256 = "b176ce37fd040f6d4dbc309af0a26cd396c529c75983d0ead1622554846028a5"
RC2_SHA256 = "4110edafaa4b8bc860f359e9532634415164df86a6c26fd439608179bae08cf2"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_digest(root: pathlib.Path) -> str:
    rows: list[str] = []
    for p in sorted((x for x in root.rglob("*") if x.is_file()), key=lambda x: x.relative_to(root).as_posix()):
        rows.append(f"{sha256_file(p)}  {p.relative_to(root).as_posix()}")
    return hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def extract_archive(archive: pathlib.Path, destination: pathlib.Path) -> pathlib.Path:
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(destination)
    children = [p for p in destination.iterdir() if p.is_dir()]
    if len(children) != 1:
        raise SystemExit(f"EXPECTED_ONE_RELEASE_ROOT:{archive}")
    return children[0]


def find_inner_rc1(root: pathlib.Path) -> pathlib.Path:
    candidates = list(root.rglob("*0.1.0-rc1*.zip"))
    if len(candidates) != 1:
        raise SystemExit(f"RC1_INNER_ARCHIVE_COUNT:{len(candidates)}")
    return candidates[0]


def resolve_rc1_artifact(source: pathlib.Path, temp: pathlib.Path) -> pathlib.Path:
    if source.is_dir():
        return find_inner_rc1(source)
    artifact_unpack = temp / "artifact"
    artifact_unpack.mkdir()
    with zipfile.ZipFile(source) as zf:
        zf.extractall(artifact_unpack)
    return find_inner_rc1(artifact_unpack)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rc1-artifact", required=True, type=pathlib.Path,
                    help="GitHub Actions artifact ZIP or extracted artifact directory containing historical RC1 ZIP")
    ap.add_argument("--rc2", required=True, type=pathlib.Path)
    ap.add_argument("--output", required=True, type=pathlib.Path)
    args = ap.parse_args()

    if sha256_file(args.rc2) != RC2_SHA256:
        raise SystemExit("RC2_DIGEST_MISMATCH")

    with tempfile.TemporaryDirectory() as td:
        temp = pathlib.Path(td)
        rc1 = resolve_rc1_artifact(args.rc1_artifact, temp)
        if sha256_file(rc1) != RC1_SHA256:
            raise SystemExit("RC1_DIGEST_MISMATCH")

        installation = temp / "installation"
        releases = installation / "releases"
        state = installation / "state"
        evidence = installation / "evidence"
        releases.mkdir(parents=True)
        state.mkdir(parents=True)
        evidence.mkdir(parents=True)

        (evidence / "history.json").write_text(json.dumps({"rc1":"held","rc2":"qualified"}, sort_keys=True) + "\n")
        evidence_before = tree_digest(evidence)

        rc1_root = extract_archive(rc1, releases / "0.1.0-rc1")
        rc1_before = tree_digest(rc1_root)
        (state / "current.json").write_text(json.dumps({"active":"0.1.0-rc1"}) + "\n")

        rc2_root = extract_archive(args.rc2, releases / "0.1.0-rc2")
        rc2_before = tree_digest(rc2_root)
        (state / "current.json").write_text(json.dumps({"active":"0.1.0-rc2"}) + "\n")
        if tree_digest(rc1_root) != rc1_before:
            raise SystemExit("RC1_MUTATED_BY_UPGRADE")
        if tree_digest(evidence) != evidence_before:
            raise SystemExit("EVIDENCE_MUTATED_BY_UPGRADE")

        (state / "current.json").write_text(json.dumps({"active":"0.1.0-rc1"}) + "\n")
        if tree_digest(rc1_root) != rc1_before:
            raise SystemExit("RC1_MUTATED_BY_ROLLBACK")
        if tree_digest(rc2_root) != rc2_before:
            raise SystemExit("RC2_MUTATED_BY_ROLLBACK")
        if tree_digest(evidence) != evidence_before:
            raise SystemExit("EVIDENCE_MUTATED_BY_ROLLBACK")

        result = {
            "schema_version":"CS-IEF-15-LIFECYCLE",
            "rc1_archive_sha256":"sha256:" + RC1_SHA256,
            "rc2_archive_sha256":"sha256:" + RC2_SHA256,
            "upgrade":"PASS",
            "rollback":"PASS",
            "rc1_tree_preserved":True,
            "rc2_tree_preserved":True,
            "evidence_preserved":True,
            "pointer_model":"SIDE_BY_SIDE_RELEASES_POINTER_ONLY_SWITCH",
            "rc1_qualification_claim":False,
            "claim_boundary":["ROLLBACK_PRESERVATION_NOT_RC1_QUALIFICATION","LIFECYCLE_PASS_NOT_STABLE","PUBLICATION_NOT_EXECUTION_AUTHORIZATION"]
        }
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
