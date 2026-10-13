"""Normalize mock security findings into deduplicated remediation records."""
import argparse
import json
from pathlib import Path

RANK = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

def normalize(document):
    findings = document["findings"]
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")
    items = {}
    for row in findings:
        if not isinstance(row, dict):
            raise ValueError("finding must be an object")
        required = ("asset_id", "finding_id", "evidence_id", "title", "owner", "severity")
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in required):
            raise ValueError("all required finding fields must be nonempty strings")
        if row["severity"] not in RANK:
            raise ValueError(f"Unsupported severity: {row['severity']}")
        key = (row["asset_id"], row["finding_id"])
        if key not in items:
            items[key] = {k: row[k] for k in required if k != "evidence_id"}
            items[key]["evidence_ids"] = []
        else:
            prior = items[key]
            if any(prior[k] != row[k] for k in ("title", "owner", "severity")):
                raise ValueError(f"Conflicting duplicate finding: {key}")
        if row["evidence_id"] not in items[key]["evidence_ids"]:
            items[key]["evidence_ids"].append(row["evidence_id"])
    backlog = sorted(items.values(), key=lambda x: (-RANK[x["severity"]], x["asset_id"], x["finding_id"]))
    return {"input_count": len(findings), "unique_count": len(backlog), "backlog": backlog,
            "disclaimer": "Synthetic examples; draft prioritization requires human review"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("backlog.json"))
    args = parser.parse_args()
    try:
        result = normalize(json.loads(args.input.read_text(encoding="utf-8")))
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"{result['input_count']} observations -> {result['unique_count']} remediation items")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Invalid input: {exc}\n")

if __name__ == "__main__":
    main()
