# Vulnerability & STIG Findings Normalizer

**Portfolio lab:** Transform synthetic scanner/STIG-style findings into a consistent, risk-prioritized remediation backlog using Python's standard library.

> All identifiers, hosts, titles, findings, and scan results are synthetic. This repository does not contain actual ACAS, Tenable, STIG Viewer, CUI, or classified exports; its mock input is not a claim of official scanner parsing capability.

## Use case
Analysts often merge inconsistent exports before translating observations to owners, deadlines, and draft POA&M entries. This demonstrator normalizes mock records, validates severity, deduplicates the same asset/finding pair, and prioritizes remediation.

## Run
```bash
python -m unittest discover -s tests -v
python -m src.normalize --input data/findings.json --output backlog.json
```

## Features
- Structured evidence ingestion with clear validation errors
- Severity ordering (Critical > High > Medium > Low)
- Duplicate collapse by `asset_id` and `finding_id`
- Count summary and ownership-aware remediation export
- Output keeps source evidence IDs for traceability

## Case study
**Problem:** Scanner outputs arrive in inconsistent formats and manual deduplication can skew remediation tracking.

**Engineering solution:** Created a deterministic transformation layer and test suite on fully synthetic findings.

**Lab result:** Four input observations become three unique remediation items, ordered by risk. No production time-saving or customer impact is claimed.

## Resume wording
> Developed a Python remediation-backlog prototype that standardizes mock vulnerability/STIG findings, deduplicates recurring observations, preserves evidence traceability, and prioritizes security remediation through automated tests.

For a richer end-to-end assessment workflow, see [GRC Automation Toolkit](https://github.com/zdawson-cyber/grc-automation-toolkit).
