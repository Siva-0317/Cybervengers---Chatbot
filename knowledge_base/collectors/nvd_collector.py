# knowledge_base/collectors/nvd_collector.py
"""
Fetches CVEs from the NVD 2.0 REST API (replaces deprecated 1.1 JSON feeds).
Produces clean CVE knowledge records.
"""
import json
import logging
import os
import time
import urllib.request
from config.settings import KNOWLEDGE_BASE_DIR
from knowledge_base.dataset_sources import NVD_CVE_API_URL, NVD_CVE_YEARS

logger = logging.getLogger(__name__)

RESULTS_PER_PAGE = 2000   # NVD 2.0 max per request
REQUEST_DELAY    = 6      # seconds between requests (no API key = 5 req/30s)


def _fetch_page(start_date: str, end_date: str, start_index: int, api_key: str = None) -> dict:
    # Build URL manually — do NOT use urlencode; NVD API rejects %3A-encoded colons in dates
    query = (
        f"pubStartDate={start_date}"
        f"&pubEndDate={end_date}"
        f"&resultsPerPage={RESULTS_PER_PAGE}"
        f"&startIndex={start_index}"
    )
    url = f"{NVD_CVE_API_URL}?{query}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    if api_key:
        req.add_header("apiKey", api_key)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_nvd_feeds(api_key: str = None) -> list[dict]:
    """
    Fetches CVE entries for each configured year range via the NVD 2.0 API.
    Returns a flat list of raw NVD vulnerability dicts.
    """
    all_vulns = []
    api_key = api_key or os.environ.get("NVD_API_KEY")

    for start_date, end_date in NVD_CVE_YEARS:
        year = start_date[:4]
        start_index = 0
        year_total  = None
        logger.info(f"Fetching NVD CVEs for {year} via 2.0 API...")

        while True:
            try:
                data       = _fetch_page(start_date, end_date, start_index, api_key)
                vulns      = data.get("vulnerabilities", [])
                year_total = data.get("totalResults", 0)
                all_vulns.extend(vulns)
                fetched_so_far = start_index + len(vulns)
                logger.info(f"  {year}: fetched {fetched_so_far}/{year_total}")

                if fetched_so_far >= year_total or not vulns:
                    break

                start_index += RESULTS_PER_PAGE
                time.sleep(REQUEST_DELAY)

            except Exception as e:
                logger.warning(f"⚠️  Failed fetching NVD {year} at index {start_index}: {e}")
                break

        logger.info(f"  ✅ {year} done: {year_total} total available")

    logger.info(f"NVD 2.0 API: downloaded {len(all_vulns)} raw CVE entries")
    return all_vulns


def parse_nvd_feeds(max_per_feed: int = 15000) -> list[dict]:
    raw_vulns = download_nvd_feeds()
    records   = []
    count     = 0

    for entry in raw_vulns:
        if count >= max_per_feed * len(NVD_CVE_YEARS):
            break

        try:
            cve      = entry.get("cve", {})
            cve_id   = cve.get("id", "")

            # Description (English)
            descs = cve.get("descriptions", [])
            desc  = next((d["value"] for d in descs if d.get("lang") == "en"), "")
            if not desc or len(desc) < 30:
                continue

            # CVSS scores (prefer v3.1, fall back to v3.0 then v2.0)
            metrics  = cve.get("metrics", {})
            cvss31   = metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})
            cvss30   = metrics.get("cvssMetricV30", [{}])[0].get("cvssData", {})
            cvss2    = metrics.get("cvssMetricV2",  [{}])[0].get("cvssData", {})
            cvss     = cvss31 or cvss30 or cvss2
            score    = cvss.get("baseScore", "N/A")
            severity = cvss.get("baseSeverity", "N/A")
            vector   = cvss.get("vectorString", "")

            # CWE
            weaknesses = cve.get("weaknesses", [])
            cwes = []
            for w in weaknesses:
                for d in w.get("description", []):
                    val = d.get("value", "")
                    if val.startswith("CWE-"):
                        cwes.append(val)
            cwe_str = ", ".join(cwes) if cwes else "N/A"

            # Affected products via CPE
            configs   = cve.get("configurations", [])
            products  = []
            for cfg in configs[:2]:
                for node in cfg.get("nodes", [])[:2]:
                    for cpe_match in node.get("cpeMatch", [])[:2]:
                        cpe = cpe_match.get("criteria", "")
                        parts = cpe.split(":")
                        if len(parts) >= 5:
                            products.append(f"{parts[3]} {parts[4]}")
            prod_str = ", ".join(products) if products else "N/A"

            text = (
                f"CVE ID: {cve_id}\n"
                f"Description: {desc}\n"
                f"Severity: {severity} (Score: {score})\n"
                f"CVSS Vector: {vector}\n"
                f"CWE: {cwe_str}\n"
                f"Affected Products: {prod_str}\n"
            )

            records.append({
                "text":     text.strip(),
                "source":   "NVD CVE",
                "category": "cve",
                "metadata": {
                    "cve_id":   cve_id,
                    "severity": severity,
                    "score":    str(score),
                    "cwe":      cwe_str
                }
            })
            count += 1

        except Exception as e:
            logger.warning(f"⚠️  Error parsing CVE entry: {e}")

    logger.info(f"✅ NVD CVE parsed: {len(records)} records")
    return records