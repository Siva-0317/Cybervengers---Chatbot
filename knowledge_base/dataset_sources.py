# knowledge_base/dataset_sources.py
"""
Master registry of all datasets we pull.
Each entry defines: source type, identifier, how to parse it.
"""

HUGGINGFACE_DATASETS = [
    {
        "id":          "zefang-liu/secqa",
        "name":        "SecQA",
        "description": "Computer security Q&A — multiple choice, two difficulty levels",
        "config":      "v1",          # also pull v2
        "split":       "train",
        "type":        "qa"
    },
    {
        "id":          "zefang-liu/secqa",
        "name":        "SecQA v2",
        "description": "Advanced computer security Q&A",
        "config":      "v2",
        "split":       "train",
        "type":        "qa"
    },
    {
        "id":          "AlicanKiraz0/Cybersecurity-Dataset-v1",
        "name":        "Cybersecurity Defense Training v1",
        "description": "Broad cybersecurity defense Q&A pairs",
        "config":      None,
        "split":       "train",
        "type":        "qa"
    },
    {
        "id":          "AlicanKiraz0/Cybersecurity-Dataset-Fenrir-v2.0",
        "name":        "Fenrir Cybersecurity Dataset v2",
        "description": "250k+ docs: detection, SIEM, IR playbooks, threat hunting",
        "config":      None,
        "split":       "train",
        "type":        "instruction"
    },
    {
        "id":          "mrmoor/cyber-threat-intelligence",
        "name":        "Cyber Threat Intelligence",
        "description": "Threat intel reports and indicators",
        "config":      None,
        "split":       "train",
        "type":        "text"
    },
    {
        "id":          "tumeteor/Security-TTP-Mapping",
        "name":        "Security TTP Mapping",
        "description": "Annotated threat reports mapped to MITRE ATT&CK TTPs",
        "config":      None,
        "split":       "train",
        "type":        "text"
    },
    {
        "id":          "AlicanKiraz0/All-CVE-Records-Training-Dataset",
        "name":        "All CVE Records",
        "description": "Full CVE vulnerability records for training",
        "config":      None,
        "split":       "train",
        "type":        "cve",
        "max_records": 50000       # cap at 50k to avoid OOM
    },
    {
        "id":          "zeroshot/cybersecurity-corpus",
        "name":        "Cybersecurity Corpus",
        "description": "Large cybersecurity text corpus",
        "config":      None,
        "split":       "train",
        "type":        "text",
        "max_records": 30000
    },
]

# MITRE ATT&CK — downloaded as JSON from official source
MITRE_ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# NVD CVE 2.0 REST API — replaces deprecated 1.1 JSON feeds
NVD_CVE_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Year ranges to pull (pubStartDate / pubEndDate)
NVD_CVE_YEARS = [
    ("2024-01-01T00:00:00.000", "2024-12-31T23:59:59.999"),
    ("2023-01-01T00:00:00.000", "2023-12-31T23:59:59.999"),
    ("2022-01-01T00:00:00.000", "2022-12-31T23:59:59.999"),
]