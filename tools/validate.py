#!/usr/bin/env python3
"""Validate the reference database in data/.

Checks
  1. JSON schema conformance (data/schema/*.schema.json)
  2. Source admission: every source_ref points to a record in source_records.json
  3. Layer purity: interpretation and hypothesis records never carry certainty "fact"
  4. Referential integrity: work_id and fact_ids resolve, ids are unique

Usage: python3 tools/validate.py
Exit code 1 on any error. Warnings do not fail the run.
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMA = DATA / "schema"
COLLECTIONS = ["source_records", "works", "datings", "attributions", "interpretation_claims"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_registry():
    resources = []
    for p in SCHEMA.glob("*.schema.json"):
        resources.append((p.name, Resource.from_contents(load(p))))
    return Registry().with_resources(resources)


def main():
    registry = build_registry()
    errors, warnings = [], []
    records = {}

    for name in COLLECTIONS:
        rows = load(DATA / f"{name}.json")
        if not isinstance(rows, list):
            errors.append(f"{name}: top level must be an array")
            continue
        validator = Draft202012Validator(load(SCHEMA / f"{name}.schema.json"), registry=registry)
        for i, row in enumerate(rows):
            for e in validator.iter_errors(row):
                errors.append(f"{name}[{i}] {list(e.path)}: {e.message}")
        records[name] = rows

    all_ids = {}
    for name, rows in records.items():
        for row in rows:
            rid = row.get("id")
            if rid in all_ids:
                errors.append(f"duplicate id {rid} in {name} and {all_ids[rid]}")
            all_ids[rid] = name

    source_ids = {r.get("id") for r in records.get("source_records", [])}
    work_ids = {r.get("id") for r in records.get("works", [])}
    fact_ids = {r.get("id") for name in ("works", "datings") for r in records.get(name, [])
                if r.get("layer") == "fact"}

    for name, rows in records.items():
        for row in rows:
            rid = row.get("id")
            for key in ("source_refs", "supporting_refs"):
                for ref in row.get(key, []):
                    if ref.get("source_id") not in source_ids:
                        errors.append(f"{rid}: {ref.get('source_id')} is not an admitted source record")
            if "work_id" in row and row["work_id"] not in work_ids:
                errors.append(f"{rid}: unknown work_id {row['work_id']}")
            for fid in row.get("fact_ids", []):
                if fid not in fact_ids:
                    errors.append(f"{rid}: fact_ids entry {fid} is not a fact layer record")
            if row.get("layer") in ("interpretation", "hypothesis") and row.get("certainty") == "fact":
                errors.append(f"{rid}: layer {row['layer']} cannot have certainty 'fact'")
            if name == "interpretation_claims":
                if not row.get("falsification"):
                    warnings.append(f"{rid}: no falsification condition stated")
                if row.get("analysis_layer") == "geometric" and not row.get("verification"):
                    warnings.append(f"{rid}: geometric claim without verification script")
            if row.get("date_from") and row.get("date_to") and row["date_from"] > row["date_to"]:
                errors.append(f"{rid}: date_from is after date_to")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    total = sum(len(r) for r in records.values())
    print(f"{total} records, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
