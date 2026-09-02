from __future__ import annotations

import argparse
import json
import pathlib

import jsonschema


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--schema", default="schemas/release-manifest.schema.json")
    args = parser.parse_args()
    manifest = json.loads(pathlib.Path(args.manifest).read_text(encoding="utf-8"))
    schema = json.loads(pathlib.Path(args.schema).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(instance=manifest, schema=schema, cls=jsonschema.Draft202012Validator)
    print(json.dumps({"schema_validation":"PASS","schema_version":manifest["schema_version"],"release_digest":manifest["release_digest"]}, sort_keys=True))


if __name__ == "__main__":
    main()
