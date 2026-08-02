import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_live_contract_has_six_claims_and_12_points():
    claims = json.loads((ROOT / 'contract/live_claims.json').read_text())
    assert len(claims) == 6
    manifest = json.loads((ROOT / 'contract/contract_manifest.json').read_text())
    assert manifest['openreview_id'] == 'aeeo8ZAftQ'
    assert manifest['maximum_points'] == 12


def test_pinned_source_manifest_is_current():
    manifest = ROOT / 'evidence/source/SHA256SUMS'
    for line in manifest.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        name = name.lstrip('* ')
        assert hashlib.sha256((manifest.parent / name).read_bytes()).hexdigest() == digest
