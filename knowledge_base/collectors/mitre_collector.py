# knowledge_base/collectors/mitre_collector.py
"""
Parses MITRE ATT&CK enterprise JSON into clean knowledge records.
Covers: Tactics, Techniques, Sub-techniques, Mitigations, Groups, Software.
"""
import json
import logging
import os
import urllib.request
from config.settings import KNOWLEDGE_BASE_DIR
from knowledge_base.dataset_sources import MITRE_ATTACK_URL

logger = logging.getLogger(__name__)

MITRE_LOCAL_PATH = os.path.join(KNOWLEDGE_BASE_DIR, "mitre_attack.json")


def download_mitre():
    if os.path.exists(MITRE_LOCAL_PATH):
        logger.info("MITRE ATT&CK already downloaded")
        return
    logger.info("Downloading MITRE ATT&CK enterprise JSON...")
    urllib.request.urlretrieve(MITRE_ATTACK_URL, MITRE_LOCAL_PATH)
    logger.info(f"✅ MITRE ATT&CK saved to {MITRE_LOCAL_PATH}")


def parse_mitre() -> list[dict]:
    if not os.path.exists(MITRE_LOCAL_PATH):
        download_mitre()

    with open(MITRE_LOCAL_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    objects = data.get("objects", [])

    for obj in objects:
        obj_type = obj.get("type", "")
        name     = obj.get("name", "")
        desc     = obj.get("description", "")
        ext_refs = obj.get("external_references", [])

        # Get ATT&CK ID (e.g. T1059)
        attack_id = ""
        for ref in ext_refs:
            if ref.get("source_name") == "mitre-attack":
                attack_id = ref.get("external_id", "")
                break

        if obj_type == "attack-pattern":   # Technique / Sub-technique
            platforms  = ", ".join(obj.get("x_mitre_platforms", []))
            tactics    = ", ".join([p.get("phase_name","") for p in obj.get("kill_chain_phases",[])])
            detection  = obj.get("x_mitre_detection", "")
            text = (
                f"MITRE ATT&CK Technique: {name} ({attack_id})\n"
                f"Tactic: {tactics}\n"
                f"Platforms: {platforms}\n"
                f"Description: {desc}\n"
            )
            if detection:
                text += f"Detection: {detection}\n"

        elif obj_type == "course-of-action":  # Mitigation
            text = (
                f"MITRE Mitigation: {name} ({attack_id})\n"
                f"Description: {desc}\n"
            )

        elif obj_type == "intrusion-set":     # Threat Group (APT)
            aliases = ", ".join(obj.get("aliases", []))
            text = (
                f"Threat Group: {name} ({attack_id})\n"
                f"Also known as: {aliases}\n"
                f"Description: {desc}\n"
            )

        elif obj_type == "malware":
            text = (
                f"Malware: {name} ({attack_id})\n"
                f"Description: {desc}\n"
            )

        elif obj_type == "tool":
            text = (
                f"Tool: {name} ({attack_id})\n"
                f"Description: {desc}\n"
            )

        else:
            continue  # skip relationship objects etc.

        if text.strip() and len(desc) > 20:
            records.append({
                "text":     text.strip(),
                "source":   "MITRE ATT&CK",
                "category": obj_type,
                "metadata": {"attack_id": attack_id, "name": name}
            })

    logger.info(f"✅ MITRE ATT&CK parsed: {len(records)} records")
    return records