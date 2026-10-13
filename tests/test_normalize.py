import unittest
from src.normalize import normalize

def fixture():
    return {"findings": [
        {"asset_id": "a", "finding_id": "1", "evidence_id": "e1", "severity": "High", "title": "x", "owner": "t"},
        {"asset_id": "a", "finding_id": "1", "evidence_id": "e2", "severity": "High", "title": "x", "owner": "t"},
        {"asset_id": "b", "finding_id": "2", "evidence_id": "e3", "severity": "Critical", "title": "y", "owner": "t"}
    ]}

class NormalizeTests(unittest.TestCase):
    def test_deduplicate_and_rank(self):
        output = normalize(fixture())
        self.assertEqual(output["unique_count"], 2)
        self.assertEqual(output["backlog"][0]["severity"], "Critical")
        self.assertEqual(output["backlog"][1]["evidence_ids"], ["e1", "e2"])

    def test_conflicting_duplicate_rejected(self):
        doc = fixture()
        doc["findings"][1]["severity"] = "Low"
        with self.assertRaises(ValueError):
            normalize(doc)

    def test_invalid_severity_rejected(self):
        doc = fixture()
        doc["findings"][0]["severity"] = "Unknown"
        with self.assertRaises(ValueError):
            normalize(doc)

if __name__ == "__main__":
    unittest.main()
